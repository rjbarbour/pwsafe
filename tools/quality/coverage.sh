#!/usr/bin/env bash
# PWS-05: gcovr coverage report for coretest (fork-only; never part of an upstream pull request).
#
# Usage: tools/quality/coverage.sh <repo-root> <build-dir> <out-dir>
# Run after a --coverage build of coretest and `ctest -R Coretests`.
# GCOVR may point at a specific gcovr binary (default: gcovr on PATH). Written for gcovr 8.6.
#
# Writes to <out-dir>:
#   coverage.json            gcovr JSON (per-file lines and functions)
#   coverage.cobertura.xml   Cobertura XML
#   coverage_summary.txt     per-directory totals, gcovr totals, then the per-file line table
#
# Scope: src/core and src/os only; the vendored src/core/pugixml and src/core/crypto/external
# are excluded, as is everything else (tests, gtest, the build directory).
# Report only: this script never fails on a coverage figure.
set -euo pipefail

REPO=$(cd "${1:?usage: coverage.sh <repo-root> <build-dir> <out-dir>}" && pwd)
BUILD=$(cd "${2:?usage: coverage.sh <repo-root> <build-dir> <out-dir>}" && pwd)
mkdir -p "${3:?usage: coverage.sh <repo-root> <build-dir> <out-dir>}"
OUT=$(cd "$3" && pwd)
GCOVR=${GCOVR:-gcovr}

# Relative filters are matched against paths relative to the working directory.
cd "$REPO"
"$GCOVR" --root "$REPO" "$BUILD" -j 4 \
  --gcov-ignore-parse-errors=negative_hits.warn_once_per_file \
  --gcov-ignore-parse-errors=suspicious_hits.warn_once_per_file \
  --filter 'src/core/' --filter 'src/os/' \
  --exclude 'src/core/pugixml/' --exclude 'src/core/crypto/external/' \
  --json "$OUT/coverage.json" \
  --cobertura "$OUT/coverage.cobertura.xml" \
  --txt "$OUT/coverage_files.txt" \
  --txt-summary > "$OUT/coverage_totals.txt"

# Per-directory totals from coverage.json. Same method as the f24fd88 baseline: a line counts once per
# file (highest hit count), a function once per (name, line).
python3 - "$OUT/coverage.json" > "$OUT/coverage_dirs.txt" <<'PY'
import collections, json, sys
cov = json.load(open(sys.argv[1]))
lines = collections.defaultdict(dict)
funcs = collections.defaultdict(dict)
for f in cov['files']:
    for l in f['lines']:
        n = l['line_number']
        lines[f['file']][n] = max(lines[f['file']].get(n, 0), l['count'])
    for fn in f['functions']:
        # gcovr omits the mangled 'name' when gcov gives only demangled names (seen with the runner's GCC).
        k = (fn.get('name') or fn.get('demangled_name'), fn.get('lineno'))
        funcs[f['file']][k] = max(funcs[f['file']].get(k, 0), fn['execution_count'])
def pct(c, t):
    return f'{c}/{t} = {c / t:.1%}' if t else f'{c}/{t} = n/a'
print('Per-directory coverage (coretest, gcovr; vendored code excluded, see tools/quality/coverage.sh)')
print(f"{'Directory':<14}{'Files':>6}  {'Lines':<24}{'Functions':<24}")
for d in ('src/core', 'src/os/unix', 'src/os'):
    fs = [n for n in lines if n.startswith(d + '/')]
    lt = sum(len(lines[n]) for n in fs); lc = sum(1 for n in fs for c in lines[n].values() if c > 0)
    ft = sum(len(funcs[n]) for n in fs); fc = sum(1 for n in fs for c in funcs[n].values() if c > 0)
    print(f'{d:<14}{len(fs):>6}  {pct(lc, lt):<24}{pct(fc, ft):<24}')
other = sorted(n for n in lines if not n.startswith(('src/core/', 'src/os/')))
if other:
    print('UNEXPECTED files outside src/core and src/os:', *other, sep='\n  ')
PY

{
  cat "$OUT/coverage_dirs.txt"
  echo
  echo 'gcovr totals (src/core + src/os)'
  cat "$OUT/coverage_totals.txt"
  echo
  cat "$OUT/coverage_files.txt"
} > "$OUT/coverage_summary.txt"
rm -f "$OUT/coverage_dirs.txt" "$OUT/coverage_totals.txt" "$OUT/coverage_files.txt"

sed -n '1,/^branches:/p' "$OUT/coverage_summary.txt"
