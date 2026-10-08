# Fork quality tooling (rjbarbour/pwsafe only)

Fork-only. Nothing under `tools/quality/` or `.github/workflows/fork-*.yml` goes into an upstream
pull request; upstream-bound branches are cut from upstream `master`.

## Coverage (PWS-05)

`coverage.sh` writes the gcovr report for coretest (`src/core` and `src/os`, vendored code excluded).
The `coverage` job of `.github/workflows/fork-quality.yml` runs it on every pull request and push to
`master` and uploads the report as an artefact.

## Quality gate (PWS-07)

The `quality` job of `fork-quality.yml` runs on pull requests to `master`, after the `coverage` job,
and judges only what the pull request adds or changes against its merge base with `master`. Legacy
code it does not touch never fails it. Every step runs even if an earlier one fails, and each writes
its section of the job summary.

| Check | Script | Fails the job when |
|---|---|---|
| Include layering | `layering.py`, `layering-edges.txt`, `layering-allow.txt` | an include edge from `src/core` or `src/os` breaks decision-01 and is not in the edge list (NEW) |
| Complexity, CRAP | `gate_changed.py` (lizard 1.24.1) | a new function has CCN > 10, cognitive complexity > 15, or (under `src/core`, `src/os`) CRAP > 30; an existing function's modified CCN or cognitive complexity rises above the limit (ratchet failure) |
| Changed-line coverage | `gate_changed.py`, `coverage-gate.toml` (gcovr JSON from the `coverage` job) | line coverage of the changed lines in `src/core`, `src/os/unix` and the top-level `src/os` headers is below the threshold in `coverage-gate.toml` (80% today); or a changed or new source file there is missing from the coverage report. Changed lines inside a function with no instrumented line in the report (an unused inline or template function in a header, say) count as uncovered; declaration-only header changes are listed and have nothing to cover. Branch and condition figures are reported when gcovr has them and enforced only once given a threshold. Changes under `src/ui`, `src/os/mac` and `src/os/windows` are listed as "not measured: reviewed by hand" |
| Coverage listing | diff-cover 10.6.0 (workflow step) | never: report only (annotated uncovered changed lines) |
| Duplication | `gate_changed.py` (lizard `-Eduplicate`) | never: report only |
| clang-tidy | `clang_tidy_gate.py`, `clang-tidy-gate.yaml`, `clang-tidy-new-files.yaml` | any finding on a changed line (bugprone-, cert-, clang-analyzer-), or any finding in a file the pull request adds (readability-, modernize-) |
| cppcheck | `cppcheck_gate.py` (cppcheck 2.17.1, built from source in the job) | a finding of severity error or warning on a changed line (diff-quality) |

`gitdiff.py` holds the shared changed-line helper and the list of paths the static analysers cover
(what the Linux build compiles). macOS- and Windows-only code is not compiled on the Linux runner, so
clang-tidy, cppcheck and coverage do not reach it; the summary lists such files as not measured.

clang-tidy and cppcheck results on changed lines (and in added files) are uploaded to code scanning
as SARIF, in the `clang-tidy` and `cppcheck` categories. A false positive is dismissed there with a
reason; the dismissal is the audit trail.

### Tuning rules

A noisy or false-positive rule is disabled in the YAML files here, with a comment giving the reason,
never in an upstream file. A `readability-` or `modernize-` finding is never suppressed with an
inline comment; an inline suppression comment (clang-tidy's or cppcheck's) is a last resort for a
single genuine false positive, because it would travel into an upstream pull request.

### Changing the edge list

`layering-edges.txt` lists exactly the 39 edges of `backlog/decisions/decision-01`. Any change to it
is a design change: the architect or Fred Brooks reviews it before merge, and decision-01 is
superseded with the new list.

### Running the gate locally

From the root of a clone, on the branch to check, with a coverage build of coretest in `build/`
(`ctest -R Coretests` run, then `tools/quality/coverage.sh . build coverage`):

    BASE=origin/master
    python3 tools/quality/layering.py
    LIZARD=lizard python3 tools/quality/gate_changed.py --base $BASE --coverage coverage/coverage.json
    diff-cover coverage/coverage.cobertura.xml --compare-branch=$BASE --include 'src/core/*' 'src/os/*'
    CLANG_TIDY=clang-tidy CLANG_TIDY_DIFF=clang-tidy-diff.py python3 tools/quality/clang_tidy_gate.py --base $BASE --build build --out q
    CPPCHECK=cppcheck DIFF_QUALITY=diff-quality python3 tools/quality/cppcheck_gate.py --base $BASE --build build --out q

clang-tidy-diff takes the diff's relative paths from the working directory, so the scripts change to
the repository root first.
