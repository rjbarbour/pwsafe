#!/usr/bin/env python3
"""PWS-07: gate on new or changed code: complexity, CRAP, changed-line coverage (fork-only).

Judges only what the pull request changes, comparing HEAD with its merge base.

Complexity and CRAP (lizard), for the functions that changed lines touch:
  * a new function (its lizard long name is not in the base version of the file) fails if its CCN
    is above --ccn (10), its lizard cognitive complexity is above --cog (15), or, under src/core or
    src/os, its CRAP score is above --crap (30);
  * an existing function fails only as a ratchet failure: its modified CCN (lizard -m, a switch
    counts once) or its cognitive complexity rises and ends above the limit. Legacy functions above
    a limit that the diff leaves alone, or edits that raise neither figure, do not fail.
  CRAP = CCN^2 * (1 - cov)^3 + CCN, with cov the share of the function's instrumented lines that
  Coretests executed. A new function in the measured coverage scope with no instrumented lines (an
  inline or template function that Coretests never uses, or a file outside the coverage build) counts
  as 0% covered; elsewhere under src/core or src/os such a function has no CRAP score and is listed.

Changed-line coverage (gcovr JSON from tools/quality/coverage.sh; settings in coverage-gate.toml):
  * every changed C/C++ file under src/ is classified: measured (src/core, src/os/unix and the
    top-level src/os headers), not measured (src/ui, src/os/mac, src/os/windows: listed as
    "not measured: reviewed by hand"), or outside the coverage scope (tests, tools);
  * a changed or new source file in the measured scope that is missing from the coverage report
    fails (none of its changed lines can be covered by Coretests);
  * a changed line inside a function (as lizard finds it) that has no instrumented line in the
    report, such as an unused inline or template function in a header, counts as an uncovered
    changed line; declaration-only header changes have no executable lines and are listed only;
  * per-metric figures over the measured changed lines: line, and branch and condition when gcovr's
    JSON has them. A metric with a threshold in coverage-gate.toml is enforced; today that is line
    coverage only, at 80% (PWS-07 AC 2).

Duplication: lizard -Eduplicate over src/ (vendored code excluded); every duplicate block with a
location on a changed line is listed with the other locations. Report only: never fails.

Usage: gate_changed.py --base REF [--coverage coverage.json] [--config TOML] [--repo DIR]
Writes a Markdown report to stdout and exits 1 on any failure.
"""
import argparse
import csv
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib

from gitdiff import changed_lines, git, merge_base

HERE = os.path.dirname(os.path.abspath(__file__))
LIZARD = os.environ.get('LIZARD', 'lizard')
EXTENSIONS = ('.c', '.cc', '.cpp', '.cxx', '.h', '.hpp', '.inl')
SOURCES = ('.c', '.cc', '.cpp', '.cxx')
CRAP_SCOPE = ('src/core/', 'src/os/')
METRICS = ('line', 'branch', 'condition')


def changed_cxx(repo, base):
    """{path: set(new line numbers)} for C/C++ files under src/, vendored code excluded."""
    mb = merge_base(base, repo)
    pathspec = ['src', ':(exclude)src/core/pugixml', ':(exclude)src/core/crypto/external']
    return mb, {f: v for f, v in changed_lines(mb, pathspec, repo).items() if f.endswith(EXTENSIONS)}


def lizard_functions(path):
    """Functions in one file: CCN, modified CCN, cognitive complexity, lines."""
    runs = []
    for extra in ([], ['-m']):
        r = subprocess.run([LIZARD, '-l', 'cpp', '-Ecognitive', '--csv', *extra, path],
                           capture_output=True, text=True)
        runs.append([row for row in csv.reader(io.StringIO(r.stdout)) if len(row) >= 12])
    return [dict(ccn=int(p[1]), mccn=int(m[1]), name=p[7], long=p[8], start=int(p[9]), end=int(p[10]),
                 cog=int(p[11])) for p, m in zip(*runs)]


def base_functions(repo, mb, path):
    try:
        text = git('show', f'{mb}:{path}', repo=repo)
    except subprocess.CalledProcessError:
        return {}
    with tempfile.NamedTemporaryFile('w', suffix=os.path.splitext(path)[1], delete=False) as tmp:
        tmp.write(text)
    try:
        funcs = {}
        for f in lizard_functions(tmp.name):
            prev = funcs.get(f['long'])
            if prev is None or (f['mccn'], f['cog']) > (prev['mccn'], prev['cog']):
                funcs[f['long']] = f
        return funcs
    finally:
        os.unlink(tmp.name)


def load_coverage(path):
    """{file: {line: {'count', 'branch': [covered, total], 'condition': [covered, total]}}}."""
    if not path:
        return None
    cov = {}
    with open(path, encoding='utf-8') as fh:
        for f in json.load(fh)['files']:
            d = cov.setdefault(f['file'], {})
            for l in f['lines']:
                e = d.setdefault(l['line_number'], {'count': 0, 'branch': [0, 0], 'condition': [0, 0]})
                e['count'] = max(e['count'], l.get('count', 0))
                for b in l.get('branches', []):   # summed over instances (templates, inline copies)
                    e['branch'][0] += b.get('count', 0) > 0
                    e['branch'][1] += 1
                for c in l.get('conditions', []):  # gcovr with GCC -fcondition-coverage only
                    e['condition'][0] += c.get('covered', 0)
                    e['condition'][1] += c.get('count', 0)
    return cov


def complexity(repo, mb, changed, cov, a, scope):
    rows, fails, unmeasured = [], [], []
    for path, lines in sorted(changed.items()):
        full = os.path.join(repo, path)
        if not os.path.isfile(full):
            continue
        old = base_functions(repo, mb, path)
        for fn in lizard_functions(full):
            if not lines & set(range(fn['start'], fn['end'] + 1)):
                continue
            prev = old.get(fn['long'])
            covered = crap = None
            if cov is not None and path.startswith(CRAP_SCOPE):
                inst = [n for n in cov.get(path, {}) if fn['start'] <= n <= fn['end']]
                if inst:
                    covered = sum(cov[path][n]['count'] > 0 for n in inst) / len(inst)
                    crap = fn['ccn'] ** 2 * (1 - covered) ** 3 + fn['ccn']
                elif prev is None and classify(path, scope) == 'measured':
                    covered = 0.0   # never compiled or instantiated by Coretests
                    crap = fn['ccn'] ** 2 + fn['ccn']
                elif prev is None:
                    unmeasured.append(f"`{path}:{fn['start']}` `{fn['name']}`")
            why = []
            if prev is None:
                if fn['ccn'] > a.ccn:
                    why.append(f"CCN {fn['ccn']} > {a.ccn}")
                if fn['cog'] > a.cog:
                    why.append(f"cognitive complexity {fn['cog']} > {a.cog}")
                if crap is not None and crap > a.crap:
                    why.append(f'CRAP {crap:.1f} > {a.crap:g}')
            else:
                if fn['mccn'] > prev['mccn'] and fn['mccn'] > a.ccn:
                    why.append(f"ratchet failure: modified CCN {prev['mccn']} -> {fn['mccn']} (limit {a.ccn})")
                if fn['cog'] > prev['cog'] and fn['cog'] > a.cog:
                    why.append(f"ratchet failure: cognitive complexity {prev['cog']} -> {fn['cog']} (limit {a.cog})")
            rows.append((path, fn, prev, covered, crap, why))
            if why:
                fails.append(f"`{path}:{fn['start']}` `{fn['name']}`: {'; '.join(why)}")

    print(f'### Complexity and CRAP (functions on changed lines since {mb[:9]})\n')
    print(f'Limits: new functions CCN <= {a.ccn}, lizard cognitive complexity <= {a.cog}'
          + (f', CRAP <= {a.crap:g} under src/core and src/os' if cov is not None
             else ' (no coverage given: CRAP not checked)')
          + '; an existing function fails only if its modified CCN or cognitive complexity rises above '
          'the limit (ratchet).\n')
    if rows:
        print('| Function | Kind | CCN (modified) | Cognitive | Coverage | CRAP | Result |')
        print('|---|---|---|---|---|---|---|')
        for path, fn, prev, covered, crap, why in rows:
            was = '' if prev is None else f" (was {prev['ccn']} ({prev['mccn']}) / {prev['cog']})"
            print(f"| `{path}:{fn['start']}` `{fn['name']}` | {'new' if prev is None else 'changed'}{was} "
                  f"| {fn['ccn']} ({fn['mccn']}) | {fn['cog']} | {'' if covered is None else f'{covered:.0%}'} "
                  f"| {'' if crap is None else f'{crap:.1f}'} | {'**FAIL**: ' + '; '.join(why) if why else 'ok'} |")
    else:
        print('No function under src/ is touched by the changed lines.')
    if unmeasured:
        print('\nNew functions with no instrumented lines in the coverage build (no CRAP score; not a failure): '
              + ', '.join(unmeasured))
    return fails


def classify(path, scope):
    if path.startswith(tuple(scope['measured'])) or re.fullmatch(r'src/os/[^/]+\.(h|hpp)', path):
        return 'measured'
    if path.startswith(tuple(scope['not_measured'])):
        return 'not measured'
    return 'outside'


def code_like(text):
    t = text.strip()
    return bool(t) and not t.startswith(('//', '/*', '*')) and t not in ('{', '}', '};', '});')


def uninstrumented(repo, path, lines, inst):
    """Changed code lines inside functions with no instrumented line in the coverage report."""
    full = os.path.join(repo, path)
    if not os.path.isfile(full):
        return set()
    with open(full, encoding='utf-8', errors='replace') as fh:
        text = fh.read().split('\n')
    out = set()
    for fn in lizard_functions(full):
        body = set(range(fn['start'], fn['end'] + 1))
        if lines & body and not inst & body:
            out |= {n for n in lines & body if n <= len(text) and code_like(text[n - 1])}
    return out


def coverage(repo, changed, cov, config):
    thresholds = config.get('thresholds', {})
    unknown = set(thresholds) - set(METRICS)
    if unknown:
        sys.exit(f'coverage-gate.toml: unknown metric(s) {sorted(unknown)}; known: {METRICS}')
    groups = {'measured': [], 'not measured': [], 'outside': []}
    for path in sorted(changed):
        groups[classify(path, config['scope'])].append(path)
    fails, missing = [], []
    totals = {m: [0, 0] for m in METRICS}
    per_file = []
    declarations = []
    for path in groups['measured']:
        if path not in cov and path.endswith(SOURCES):
            missing.append(path)
            continue
        report = cov.get(path, {})
        dark = uninstrumented(repo, path, changed[path], set(report))
        if path not in cov and not dark:
            declarations.append(path)   # no changed line inside a function body
            continue
        f = {m: [0, 0] for m in METRICS}
        f['line'][1] += len(dark)       # counted as uncovered
        for n in changed[path]:
            e = report.get(n)
            if e is None:
                continue   # not an executable line
            f['line'][0] += e['count'] > 0
            f['line'][1] += 1
            for m in ('branch', 'condition'):
                f[m][0] += e[m][0]
                f[m][1] += e[m][1]
        for m in METRICS:
            totals[m][0] += f[m][0]
            totals[m][1] += f[m][1]
        uncovered = sorted(n for n in changed[path] if n in report and report[n]['count'] == 0)
        per_file.append((path, f, uncovered, sorted(dark)))

    enforced = ', '.join(f'{m} {v:g}%' for m, v in thresholds.items()) or 'none'
    print('\n### Changed-line coverage (Coretests, gcovr; settings in tools/quality/coverage-gate.toml)\n')
    print(f"Measured scope: {', '.join(config['scope']['measured'])} and the top-level src/os headers. "
          f'Enforced: {enforced}; other metrics are report only.\n')
    for path in missing:
        msg = (f'`{path}`: missing from the coverage report, so none of its {len(changed[path])} changed '
               'line(s) can be covered by Coretests; add it to the build that coretest links')
        print(f'- **FAIL**: {msg}')
        fails.append(msg)
    for metric in METRICS:
        cov_n, tot = totals[metric]
        limit = thresholds.get(metric)
        if tot == 0:
            if limit is not None:
                print(f'- {metric} coverage: nothing measurable on the changed lines in the measured scope (passes)')
            continue
        pct = 100.0 * cov_n / tot
        verdict = ('report only' if limit is None
                   else ('PASS' if pct >= limit else f'**FAIL** (below {limit:g}%)'))
        print(f'- {metric} coverage of changed code: {cov_n}/{tot} = {pct:.1f}%: {verdict}')
        if limit is not None and pct < limit:
            fails.append(f'{metric} coverage of changed code {pct:.1f}% < {limit:g}%')
    if per_file:
        print('\n| File | Lines covered | Uncovered changed lines | In functions with no instrumented line (counted as uncovered) |')
        print('|---|---|---|---|')
        for path, f, uncovered, dark in per_file:
            c, t = f['line']
            print(f"| `{path}` | {c}/{t} | {compress(uncovered) or '-'} | {compress(dark) or '-'} |")
    if declarations:
        print('\nChanged headers in the measured scope with no changed line inside a function body '
              '(declarations only; nothing to cover): ' + ', '.join(f'`{p}`' for p in declarations))
    if groups['not measured']:
        print('\nNot measured: reviewed by hand (GUI or platform code the Linux coretest build does not '
              'instrument): ' + ', '.join(f'`{p}`' for p in groups['not measured']))
    if groups['outside']:
        print('\nOutside the coverage scope (test or tool code): ' + ', '.join(f'`{p}`' for p in groups['outside']))
    if not changed:
        print('No C/C++ file under src/ changed.')
    return fails


def compress(nums):
    out, start, prev = [], None, None
    for n in nums:
        if start is None:
            start = prev = n
        elif n == prev + 1:
            prev = n
        else:
            out.append(f'{start}' if start == prev else f'{start}-{prev}')
            start = prev = n
    if start is not None:
        out.append(f'{start}' if start == prev else f'{start}-{prev}')
    return ', '.join(out)


def duplicates(repo, changed):
    """Duplicate blocks (lizard -Eduplicate over src/) with a location on a changed line."""
    cmd = [LIZARD, '-l', 'cpp', '-Eduplicate', '-w', '-C', '9999', '-L', '999999', '-a', '999',
           '-x', './src/core/pugixml/*', '-x', './src/core/crypto/external/*', 'src']
    # No -t: lizard's duplicate extension is very slow with worker processes.
    out = subprocess.run(cmd, cwd=repo, capture_output=True, text=True).stdout
    found = []
    for block in out.split('Duplicate block:')[1:]:
        locs = re.findall(r'^(\S+):(\d+) ~ (\d+)$', block, re.M)
        locs = [(os.path.normpath(p), int(s), int(e)) for p, s, e in locs]
        hit = [l for l in locs if l[0] in changed and changed[l[0]] & set(range(l[1], l[2] + 1))]
        if hit and len(locs) > 1:
            found.append((hit, [l for l in locs if l not in hit]))
    print('\n### Duplication (lizard -Eduplicate, report only)\n')
    if found:
        fmt = lambda ls: ', '.join(f'`{p}:{s}-{e}`' for p, s, e in ls)
        for hit, others in found:
            print(f'- changed {fmt(hit)} duplicates {fmt(others) if others else "each other"}')
    else:
        print('No duplicate block touches the changed lines.')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n', 1)[0])
    ap.add_argument('--repo', default='.')
    ap.add_argument('--base', default='origin/master')
    ap.add_argument('--coverage', help='gcovr JSON from tools/quality/coverage.sh')
    ap.add_argument('--config', default=os.path.join(HERE, 'coverage-gate.toml'))
    ap.add_argument('--ccn', type=int, default=10)
    ap.add_argument('--cog', type=int, default=15)
    ap.add_argument('--crap', type=float, default=30)
    a = ap.parse_args()
    with open(a.config, 'rb') as fh:
        config = tomllib.load(fh)

    mb, changed = changed_cxx(a.repo, a.base)
    cov = load_coverage(a.coverage)
    fails = complexity(a.repo, mb, changed, cov, a, config['scope'])
    if cov is not None:
        fails += coverage(a.repo, changed, cov, config)
    duplicates(a.repo, changed)
    if fails:
        print(f'\n**Complexity, CRAP and coverage: FAIL** ({len(fails)} problem(s))\n')
        for f in fails:
            print(f'- {f}')
    else:
        print('\n**Complexity, CRAP and coverage: PASS**')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
