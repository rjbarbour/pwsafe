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
  --json-summary "$OUT/coverage_files_summary.json" \
  --cobertura "$OUT/coverage.cobertura.xml" \
  --txt "$OUT/coverage_files.txt" \
  --txt-summary > "$OUT/coverage_totals.txt"

# Per-directory totals.
# Lines: from coverage.json, counted as in the f24fd88 baseline (each line once per file, at its
#   highest hit count). gcovr's own totals count repeated line entries, so they read slightly higher.
# Functions: gcovr's per-file function counts from its JSON summary. The function records inside
#   coverage.json differ between gcov versions; these counts match the baseline's method locally.
python3 - "$OUT/coverage.json" "$OUT/coverage_files_summary.json" > "$OUT/coverage_dirs.txt" <<'PY'
import collections, json, sys
cov = json.load(open(sys.argv[1]))
summary = {f['filename']: f for f in json.load(open(sys.argv[2]))['files']}
lines = collections.defaultdict(dict)
for f in cov['files']:
    for l in f['lines']:
        n = l['line_number']
        lines[f['file']][n] = max(lines[f['file']].get(n, 0), l.get('count', 0))
def pct(c, t):
    return f'{c}/{t} = {c / t:.1%}' if t else f'{c}/{t} = n/a'
names = set(lines) | set(summary)
print('Per-directory coverage (coretest, gcovr; vendored code excluded, see tools/quality/coverage.sh)')
print(f"{'Directory':<14}{'Files':>6}  {'Lines':<24}{'Functions':<24}")
for d in ('src/core', 'src/os/unix', 'src/os'):
    fs = sorted(n for n in names if n.startswith(d + '/'))
    lt = sum(len(lines[n]) for n in fs)
    lc = sum(1 for n in fs for c in lines[n].values() if c > 0)
    ft = sum(summary[n]['function_total'] for n in fs if n in summary)
    fc = sum(summary[n]['function_covered'] for n in fs if n in summary)
    print(f'{d:<14}{len(fs):>6}  {pct(lc, lt):<24}{pct(fc, ft):<24}')
other = sorted(n for n in names if not n.startswith(('src/core/', 'src/os/')))
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
rm -f "$OUT/coverage_dirs.txt" "$OUT/coverage_totals.txt" "$OUT/coverage_files.txt" \
  "$OUT/coverage_files_summary.json"

sed -n '1,/^branches:/p' "$OUT/coverage_summary.txt"
