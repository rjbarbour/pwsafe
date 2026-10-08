#!/usr/bin/env python3
"""PWS-07: cppcheck gate (fork-only; never part of an upstream pull request).

Runs cppcheck once over the build's compile_commands.json for the gated paths (gitdiff.GATED), with a
cppcheck build directory, then a second time from that cache to write a text report:
  * <out>/cppcheck.sarif: cppcheck's native SARIF, with results kept only where a location is on a
    changed line and paths made repository-relative, for upload to code scanning (category cppcheck);
    every rule cppcheck reported stays in the rule list, but a rule with no result on a changed line
    keeps only its id as its description (cppcheck words it after a finding elsewhere in the tree);
  * <out>/cppcheck-gate.txt: findings of severity error or warning in diff-quality's cppcheck format;
    `diff-quality --violations=cppcheck --fail-under=100` fails the gate on any of them on a changed
    line. Other severities (style, performance, portability, information) never fail; those on changed
    lines are listed in the summary and the SARIF.

Usage: cppcheck_gate.py --base REF --build DIR --out DIR [--jobs N]
Environment: CPPCHECK (default cppcheck), DIFF_QUALITY (default diff-quality).
"""
import argparse
import json
import os
import re
import subprocess
import sys

from gitdiff import GATED, changed_lines, git, merge_base

TEMPLATE = '[{file}:{line}]: ({severity}) {message} [{id}]'
LINE = re.compile(r'^\[(.+?):(\d+)\]: \((\w+)\) (.*) \[(\w+)\]$')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n', 1)[0])
    ap.add_argument('--base', required=True)
    ap.add_argument('--build', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--jobs', type=int, default=os.cpu_count() or 2)
    a = ap.parse_args()
    cppcheck = os.environ.get('CPPCHECK', 'cppcheck')
    diff_quality = os.environ.get('DIFF_QUALITY', 'diff-quality')
    root = os.path.realpath(git('rev-parse', '--show-toplevel').strip())
    os.chdir(root)
    build = os.path.realpath(a.build)
    out = os.path.realpath(a.out)
    os.makedirs(os.path.join(out, 'cppcheck-build'), exist_ok=True)
    mb = merge_base(a.base)
    changed = changed_lines(mb, GATED)

    common = [
        cppcheck, f'--project={build}/compile_commands.json',
        '--file-filter=*/src/core/*', '--file-filter=*/src/os/unix/*', '--file-filter=*/src/ui/wxWidgets/*',
        '--file-filter=*/src/ui/cli/*', '--file-filter=*/src/test/*',
        f'-i{root}/src/core/pugixml', f'-i{root}/src/core/crypto/external',
        '--suppress=*:*/src/core/pugixml/*', '--suppress=*:*/src/core/crypto/external/*',
        f'--suppress=*:{build}/*', '--suppress=*:/usr/include/*', '--suppress=missingIncludeSystem',
        '--platform=unix64', '-D__linux__=1', '-D__BYTE_ORDER__=1234', '-D__ORDER_LITTLE_ENDIAN__=1234',
        '-D__ORDER_BIG_ENDIAN__=4321', '--library=wxwidgets', '--enable=warning,style,performance,portability',
        '--inline-suppr', f'--cppcheck-build-dir={out}/cppcheck-build', f'-j{a.jobs}', '--quiet',
    ]
    version = subprocess.run([cppcheck, '--version'], capture_output=True, text=True).stdout.strip()
    subprocess.run([*common, '--output-format=sarif', f'--output-file={out}/cppcheck-full.sarif'], check=True)
    subprocess.run([*common, f'--template={TEMPLATE}', f'--output-file={out}/cppcheck-full.txt'], check=True)

    def rel(path):
        path = re.sub(r'^file://', '', path)
        return os.path.relpath(os.path.realpath(path), root) if os.path.isabs(path) else os.path.normpath(path)

    def on_changed(path, line):
        return int(line) in changed.get(path, ())

    # SARIF: keep native rules; keep results with any location on a changed line.
    with open(f'{out}/cppcheck-full.sarif', encoding='utf-8') as fh:
        sarif = json.load(fh)
    total = kept = rules = 0
    for run in sarif.get('runs', []):
        results = []
        for res in run.get('results', []):
            total += 1
            hit = False
            for loc in res.get('locations', []):
                art = loc.get('physicalLocation', {}).get('artifactLocation', {})
                if 'uri' in art:
                    art['uri'] = rel(art['uri'])
                    hit |= on_changed(art['uri'], loc['physicalLocation'].get('region', {}).get('startLine', 0))
            if hit:
                results.append(res)
        kept += len(results)
        run['results'] = results
        # cppcheck words each rule's description after the first finding it met anywhere in the tree;
        # for rules with no finding on a changed line, keep only the rule id.
        hit_rules = {res.get('ruleId') for res in results}
        driver_rules = run.get('tool', {}).get('driver', {}).get('rules', [])
        for rule in driver_rules:
            # Code scanning requires security-severity as a string; cppcheck writes a number.
            props = rule.get('properties', {})
            if isinstance(props.get('security-severity'), (int, float)):
                props['security-severity'] = f"{props['security-severity']:.1f}"
            if rule.get('id') not in hit_rules:
                for key in ('shortDescription', 'fullDescription', 'help'):
                    if key in rule:
                        rule[key] = {'text': rule['id']}
        rules = len(driver_rules)
    with open(f'{out}/cppcheck.sarif', 'w', encoding='utf-8') as fh:
        json.dump(sarif, fh, indent=1)

    # Text report: error and warning severities for diff-quality; the rest is report only.
    gate, other = [], []
    with open(f'{out}/cppcheck-full.txt', encoding='utf-8', errors='replace') as fh:
        for line in fh:
            m = LINE.match(line.strip())
            if not m:
                continue
            path, lineno, sev, msg, rule = rel(m.group(1)), m.group(2), m.group(3), m.group(4), m.group(5)
            if sev in ('error', 'warning'):
                gate.append(f'[{path}:{lineno}]: ({sev}) {msg} [{rule}]')
            if on_changed(path, lineno):
                other.append((path, lineno, sev, rule, msg))
    with open(f'{out}/cppcheck-gate.txt', 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(gate) + ('\n' if gate else ''))
    dq = subprocess.run([diff_quality, '--violations=cppcheck', f'--compare-branch={mb}', '--fail-under=100',
                         f'--format=markdown:{out}/cppcheck-diff-quality.md', f'{out}/cppcheck-gate.txt'],
                        capture_output=True, text=True)

    lines = ['### cppcheck (changed lines; error and warning severities fail)\n',
             f'{version}; merge base {mb[:9]}; {total} finding(s) in the gated paths, {kept} on changed lines '
             f'(uploaded); {rules} rule(s) in the SARIF; {len(gate)} error/warning finding(s) passed to diff-quality.\n']
    if other:
        lines += ['| File:line | Severity | Rule | Message | Fails |', '|---|---|---|---|---|']
        lines += [f"| `{p}:{n}` | {s} | `{r}` | {m.replace('|', '/')} | {'yes' if s in ('error', 'warning') else 'no'} |"
                  for p, n, s, r, m in other]
    lines += [f'\ndiff-quality (exit status {dq.returncode}):\n', '```', dq.stdout.strip() or '(no output)', '```']
    failed = dq.returncode != 0
    lines.append(f"\n**cppcheck: {'FAIL' if failed else 'PASS'}**")
    report = '\n'.join(lines)
    with open(f'{out}/cppcheck.md', 'w', encoding='utf-8') as fh:
        fh.write(report + '\n')
    print(report)
    if dq.stderr.strip():
        print(dq.stderr.strip(), file=sys.stderr)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
