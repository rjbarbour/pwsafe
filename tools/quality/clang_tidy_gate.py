#!/usr/bin/env python3
"""PWS-07: clang-tidy gate (fork-only; never part of an upstream pull request).

Two runs, both from the repository root against the build's compile_commands.json:
  1. changed lines: `git diff -U0 <merge-base> HEAD` over the gated paths is piped into clang-tidy-diff
     with tools/quality/clang-tidy-gate.yaml (bugprone-, cert-, clang-analyzer-); only findings on
     changed lines are reported;
  2. added files: clang-tidy with tools/quality/clang-tidy-new-files.yaml (readability-, modernize-)
     on the whole of each C++ file `git diff --diff-filter=A` lists against the merge base.
Any finding from either run fails the gate. Exceptions, listed in the summary but not failing:
  * a compile error (clang-diagnostic-error) in a header that clang-tidy-diff or the added-file run
    processed on its own: Password Safe's wxWidgets headers are not self-contained (they rely on the
    precompiled header), so they do not compile alone. Their changed lines are still checked when a
    changed source file that includes them is analysed.
  A compile error in a source file does fail: that file could not be analysed.
Gated paths: gitdiff.GATED (what the Linux build compiles).

Writes <out>/clang-tidy.sarif (all enabled checks as rules, results with repository-relative paths)
and <out>/clang-tidy.md, prints the Markdown summary, and exits 1 on any failing finding.

Usage: clang_tidy_gate.py --base REF --build DIR --out DIR [--jobs N]
Environment: CLANG_TIDY (default clang-tidy), CLANG_TIDY_DIFF (default clang-tidy-diff).
"""
import argparse
import json
import os
import re
import subprocess
import sys

from gitdiff import CXX, GATED as PATHSPEC, changed_lines, git, merge_base

HERE = os.path.dirname(os.path.abspath(__file__))
GATE_CONFIG = os.path.join(HERE, 'clang-tidy-gate.yaml')
NEW_CONFIG = os.path.join(HERE, 'clang-tidy-new-files.yaml')
HEADER = ('.h', '.hpp')
DIAG = re.compile(r'^(.+?):(\d+):(\d+): (warning|error): (.*?) \[([^\]]+)\]$')


def parse(text, root):
    found = []
    for line in text.splitlines():
        m = DIAG.match(line.strip())
        if not m:
            continue
        path = os.path.relpath(os.path.realpath(m.group(1)), root)
        checks = [c for c in m.group(6).split(',') if c and not c.startswith('-warnings-as-errors')]
        found.append(dict(file=path, line=int(m.group(2)), col=int(m.group(3)), level=m.group(4),
                          msg=m.group(5), rule=checks[0] if checks else m.group(6)))
    return found


def enabled_checks(tidy, config):
    r = subprocess.run([tidy, '--list-checks', f'--config-file={config}'], capture_output=True, text=True, check=True)
    return [l.strip() for l in r.stdout.splitlines()[1:] if l.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n', 1)[0])
    ap.add_argument('--base', required=True)
    ap.add_argument('--build', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--jobs', type=int, default=os.cpu_count() or 2)
    a = ap.parse_args()
    tidy = os.environ.get('CLANG_TIDY', 'clang-tidy')
    tidy_diff = os.environ.get('CLANG_TIDY_DIFF', 'clang-tidy-diff')
    root = os.path.realpath(git('rev-parse', '--show-toplevel').strip())
    os.chdir(root)  # clang-tidy-diff takes the diff's relative paths from the working directory
    build = os.path.realpath(a.build)
    os.makedirs(a.out, exist_ok=True)
    mb = merge_base(a.base)
    changed = changed_lines(mb, PATHSPEC)
    added = [f for f in git('diff', '--name-only', '--diff-filter=A', '--no-renames', mb, 'HEAD', '--', *PATHSPEC).split()
             if re.match(CXX, f)]
    version = subprocess.run([tidy, '--version'], capture_output=True, text=True).stdout.strip().splitlines()
    log = []

    # 1. Changed lines (clang-tidy-diff, gate configuration).
    diff = git('diff', '-U0', '--no-color', mb, 'HEAD', '--', *PATHSPEC)
    gate_raw = ''
    if diff.strip():
        r = subprocess.run([tidy_diff, '-p1', '-path', build, '-config-file', GATE_CONFIG, '-j', str(a.jobs),
                            '-quiet', '-iregex', CXX, '-clang-tidy-binary', tidy, '-extra-arg=-Wno-error'],
                           input=diff, capture_output=True, text=True)
        gate_raw = r.stdout + r.stderr
        log.append(f'clang-tidy-diff exit status {r.returncode}')
    gate = [d for d in parse(gate_raw, root) if d['line'] in changed.get(d['file'], ())
            or d['rule'] == 'clang-diagnostic-error']

    # 2. Added files (whole file, new-files configuration).
    new_raw = ''
    if added:
        headers = [re.escape(os.path.join(root, f)) for f in added if f.endswith(HEADER)]
        hf = '^(' + '|'.join(headers) + ')$' if headers else '^$'
        r = subprocess.run([tidy, '-p', build, f'--config-file={NEW_CONFIG}', f'--header-filter={hf}', '-quiet',
                            '-extra-arg=-Wno-error', *added], capture_output=True, text=True)
        new_raw = r.stdout + r.stderr
        log.append(f'clang-tidy (added files) exit status {r.returncode}')
    new = [d for d in parse(new_raw, root) if d['file'] in added or d['rule'] == 'clang-diagnostic-error']

    with open(os.path.join(a.out, 'clang-tidy-raw.txt'), 'w', encoding='utf-8') as fh:
        fh.write(gate_raw + '\n' + new_raw)

    seen, failing, skipped = set(), [], []
    for kind, diags in (('changed line', gate), ('added file', new)):
        for d in diags:
            key = (d['file'], d['line'], d['col'], d['rule'])
            if key in seen:
                continue
            seen.add(key)
            d['kind'] = kind
            if d['rule'] == 'clang-diagnostic-error' and d['file'].endswith(HEADER):
                skipped.append(d)
            else:
                failing.append(d)

    rules = sorted(set(enabled_checks(tidy, GATE_CONFIG)) | set(enabled_checks(tidy, NEW_CONFIG))
                   | {d['rule'] for d in failing})
    sarif = {
        '$schema': 'https://json.schemastore.org/sarif-2.1.0.json',
        'version': '2.1.0',
        'runs': [{
            'tool': {'driver': {
                'name': 'clang-tidy', 'version': version[0] if version else 'unknown',
                'informationUri': 'https://clang.llvm.org/extra/clang-tidy/',
                'rules': [{'id': r, 'shortDescription': {'text': r},
                           'helpUri': 'https://clang.llvm.org/extra/clang-tidy/checks/list.html'} for r in rules],
            }},
            'results': [{
                'ruleId': d['rule'], 'level': 'error' if d['level'] == 'error' else 'warning',
                'message': {'text': d['msg']},
                'locations': [{'physicalLocation': {
                    'artifactLocation': {'uri': d['file']},
                    'region': {'startLine': d['line'], 'startColumn': d['col']}}}],
            } for d in failing],
        }],
    }
    with open(os.path.join(a.out, 'clang-tidy.sarif'), 'w', encoding='utf-8') as fh:
        json.dump(sarif, fh, indent=1)

    lines = ['### clang-tidy (changed lines: bugprone-, cert-, clang-analyzer-; added files: readability-, modernize-)\n',
             f"{version[0] if version else tidy}; merge base {mb[:9]}; {sum(map(len, changed.values()))} changed line(s) "
             f'in {len(changed)} gated file(s); {len(added)} added C++ file(s); {len(rules)} rule(s) in the SARIF.\n']
    if failing:
        lines += ['| File:line | Rule | Run | Message |', '|---|---|---|---|']
        lines += [f"| `{d['file']}:{d['line']}` | `{d['rule']}` | {d['kind']} | {d['msg'].replace('|', '/')} |"
                  for d in failing]
    if skipped:
        lines.append(f'\nNot analysed on their own (header not self-contained; {len(skipped)} compile error(s), '
                     'not a failure): ' + ', '.join(sorted({f"`{d['file']}`" for d in skipped})))
    lines.append(f"\n**clang-tidy: {'FAIL' if failing else 'PASS'}** ({len(failing)} finding(s))")
    report = '\n'.join(lines)
    with open(os.path.join(a.out, 'clang-tidy.md'), 'w', encoding='utf-8') as fh:
        fh.write(report + '\n')
    print(report)
    print('\n' + '; '.join(log), file=sys.stderr)
    return 1 if failing else 0


if __name__ == '__main__':
    sys.exit(main())
