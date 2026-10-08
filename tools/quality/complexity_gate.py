#!/usr/bin/env python3
"""PWS-07: complexity and CRAP gate on new or changed functions (fork-only; never upstream).

Judges only the functions that the pull request's changed lines touch, comparing the head of the
branch with the merge base:
  * a new function (its lizard long name is not in the base version of the file) fails if its
    CCN is above --ccn (10), its lizard cognitive complexity is above --cog (15), or, under
    src/core or src/os, its CRAP score is above --crap (30);
  * an existing function that the diff touches fails only as a ratchet failure: its modified CCN
    (lizard -m, a switch counts once) or its cognitive complexity rises and ends above the limit.
    Legacy functions above a limit that the diff leaves alone, or edits without raising either
    figure, do not fail.
  CRAP = CCN^2 * (1 - cov)^3 + CCN, with cov the share of the function's instrumented lines that
  Coretests executed (gcovr JSON from tools/quality/coverage.sh). A function with no instrumented
  lines (not compiled into the coverage build, for example macOS- or Windows-only code) has no CRAP
  score; the summary says so and it does not fail.
Coverage scope: a changed source file under src/core or src/os that is missing from the coverage
report fails (none of its changed lines is covered by Coretests), unless it is macOS- or Windows-only
or an existing file the Linux build does not compile; changed GUI and platform files are listed as
not measured. The changed-line percentage itself is diff-cover's job (workflow step).
Duplication: lizard -Eduplicate over src/ (vendored code excluded); every duplicate block with a
location on a changed line is listed with all of its locations. Report only: never fails the gate.

Usage: complexity_gate.py --base REF [--coverage coverage.json] [--build DIR] [--repo DIR]
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

from gitdiff import changed_lines, git, merge_base

LIZARD = os.environ.get('LIZARD', 'lizard')
EXTENSIONS = ('.c', '.cc', '.cpp', '.cxx', '.h', '.hpp', '.inl')
CRAP_SCOPE = ('src/core/', 'src/os/')


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
    if not path:
        return None
    lines = {}
    with open(path, encoding='utf-8') as fh:
        for f in json.load(fh)['files']:
            d = lines.setdefault(f['file'], {})
            for l in f['lines']:
                d[l['line_number']] = max(d.get(l['line_number'], 0), l.get('count', 0))
    return lines


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
    return found


NOT_LINUX = ('src/os/mac/', 'src/os/windows/')


def coverage_scope(repo, mb, changed, cov, built):
    """Changed files the coverage figures cannot see.

    Returns (missing, unmeasured): missing are changed source files under src/core or src/os that
    are absent from the coverage report although the Linux build compiles them, or that the pull
    request adds (a new file coretest never links); they fail. Unmeasured are changed C/C++ files
    outside src/core and src/os, under the macOS and Windows directories, or existing src/core files
    the Linux build does not compile; they are listed for review by hand and do not fail.
    """
    missing, unmeasured = [], []
    for path, lines in sorted(changed.items()):
        if not os.path.isfile(os.path.join(repo, path)):
            continue
        if not path.startswith(CRAP_SCOPE) or path.startswith(NOT_LINUX):
            unmeasured.append(path)
            continue
        if path in cov or not path.endswith(('.c', '.cc', '.cpp', '.cxx')):
            continue
        is_new = subprocess.run(['git', '-C', repo, 'cat-file', '-e', f'{mb}:{path}'],
                                capture_output=True).returncode != 0
        if is_new or built is None or path in built:
            missing.append((path, len(lines)))
        else:
            unmeasured.append(path)
    return missing, unmeasured


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n', 1)[0])
    ap.add_argument('--repo', default='.')
    ap.add_argument('--base', default='origin/master')
    ap.add_argument('--coverage')
    ap.add_argument('--build', help='build directory with compile_commands.json (to list changed sources the Linux build does not compile)')
    ap.add_argument('--ccn', type=int, default=10)
    ap.add_argument('--cog', type=int, default=15)
    ap.add_argument('--crap', type=float, default=30)
    a = ap.parse_args()

    mb, changed = changed_cxx(a.repo, a.base)
    cov = load_coverage(a.coverage)
    rows, fails, unmeasured = [], [], []
    for path, lines in sorted(changed.items()):
        full = os.path.join(a.repo, path)
        if not os.path.isfile(full):
            continue
        old = base_functions(a.repo, mb, path)
        for fn in lizard_functions(full):
            if not lines & set(range(fn['start'], fn['end'] + 1)):
                continue
            prev = old.get(fn['long'])
            covered = crap = None
            if cov is not None and path.startswith(CRAP_SCOPE):
                inst = [n for n in cov.get(path, {}) if fn['start'] <= n <= fn['end']]
                if inst:
                    covered = sum(cov[path][n] > 0 for n in inst) / len(inst)
                    crap = fn['ccn'] ** 2 * (1 - covered) ** 3 + fn['ccn']
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
          + (f', CRAP <= {a.crap:g} under src/core and src/os' if cov is not None else ' (no coverage given: CRAP not checked)')
          + '; an existing function fails only if its modified CCN or cognitive complexity rises above the limit (ratchet).\n')
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
        print('\nNew functions with no instrumented lines in the coverage build (no CRAP score; not a failure):')
        for u in unmeasured:
            print(f'- {u}')
    built = None
    if a.build and os.path.isfile(os.path.join(a.build, 'compile_commands.json')):
        root = os.path.realpath(a.repo)
        with open(os.path.join(a.build, 'compile_commands.json'), encoding='utf-8') as fh:
            built = {os.path.relpath(os.path.realpath(e['file']), root) for e in json.load(fh)}
    if cov is not None:
        missing, unmeasured_files = coverage_scope(a.repo, mb, changed, cov, built)
        print('\n### Coverage scope (changed files)\n')
        for path, n in missing:
            msg = (f'`{path}`: not in the coverage report, so none of its {n} changed line(s) is covered by '
                   'Coretests (changed-line coverage limit under src/core and src/os); add it to the build '
                   'that coretest links')
            print(f'- **FAIL**: {msg}')
            fails.append(msg)
        if unmeasured_files:
            print('- Not measured by Coretests (GUI or platform code the Linux coretest build does not '
                  'instrument; reviewed by hand): ' + ', '.join(f'`{p}`' for p in unmeasured_files))
        if not missing and not unmeasured_files:
            print('- Every changed C/C++ file is in the coverage scope.')
    dups = duplicates(a.repo, changed)
    print('\n### Duplication (lizard -Eduplicate, report only)\n')
    if dups:
        fmt = lambda ls: ', '.join(f'`{p}:{s}-{e}`' for p, s, e in ls)
        for hit, others in dups:
            print(f'- changed {fmt(hit)} duplicates {fmt(others) if others else "each other"}')
    else:
        print('No duplicate block touches the changed lines.')
    if fails:
        print(f'\n**Complexity/CRAP: FAIL** ({len(fails)} function(s))\n')
        for f in fails:
            print(f'- {f}')
    else:
        print('\n**Complexity/CRAP: PASS**')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
