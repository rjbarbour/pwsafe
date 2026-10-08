---
id: PWS-05
title: >-
  Fork-only CI job that builds coretest with coverage flags and publishes gcovr
  coverage
status: Review
assignee:
  - '@grace-hopper'
created_date: '2026-10-08 12:49'
updated_date: '2026-10-08 15:51'
labels:
  - quality
dependencies: []
type: chore
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A fork-only CI job configures and builds `coretest` with GCC coverage instrumentation, runs Coretests and publishes gcovr line and function coverage for `src/core` and `src/os`, with the vendored `src/core/pugixml` and `src/core/crypto/external` excluded. The coverage flags (`--coverage -O0` for C and C++, and `--coverage` for the linker) are passed in the fork-only workflow's own configure step; `CMakePresets.json`, `CMakeLists.txt` and other upstream files are not edited. The job reports coverage and does not gate on it; the changed-line gate belongs to PWS-07.

Drafts by Grace Hopper, on the team box and not in the repository: `/workspace/grace-quality/scripts/coverage.sh` (destination `tools/quality/coverage.sh`) and the "Coverage build + coretest" step in `/workspace/grace-quality/proposed/fork-quality.yml`.

Code-quality stack agreed in the pwsafe platform room; requested by Fred Brooks, 2026-10-08. Flags in the workflow rather than a preset: Fred Brooks, 2026-10-08.

Exclusions: the upstream workflows (`cmake-build.yml`, `codeql-analysis.yml`, `macos-latest.yml`, `macos-cmake-latest.yml`) stay untouched; fork-only, never part of an upstream pull request; any gate covers new or changed code only; no SonarQube Cloud or CodeRabbit; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given a clean checkout of fork `master` on `ubuntu-latest`, when the coverage job's configure step runs and `coretest` is built, then the step's log shows `CMAKE_BUILD_TYPE=Debug`, `CMAKE_EXPORT_COMPILE_COMMANDS=ON`, `USE_INTERPROCEDURAL_OPTIMIZATION=OFF`, `--coverage -O0` in both `CMAKE_C_FLAGS` and `CMAKE_CXX_FLAGS`, and `--coverage` in `CMAKE_EXE_LINKER_FLAGS`; and given the pull request that adds the job, when QA reads its diff, then `CMakePresets.json` and `CMakeLists.txt` are unchanged
- [ ] #2 Given a push to `master` or a pull request to `master` in rjbarbour/pwsafe, when the coverage job runs, then `ctest -R Coretests` passes and the run uploads `coverage.json`, `coverage.cobertura.xml` and a text summary produced by gcovr 8.6 as an artefact
- [ ] #3 Given that artefact, when QA reads the text summary, then it lists files under `src/core` and `src/os` only and no file under `src/core/pugixml` or `src/core/crypto/external`
- [ ] #4 Given the first job run on `master`, when QA reads the task notes, then they record its line and function coverage for `src/core` and `src/os/unix` next to Grace Hopper's baseline at f24fd88 (`src/core` lines 7659/19424 = 39.4%, functions 930/1495 = 62.2%; `src/os/unix` lines 430/1988 = 21.6%, functions 54/196 = 27.6%)
- [ ] #5 Given the same workflow runs in any repository other than rjbarbour/pwsafe, when it is triggered, then the coverage job is skipped and no coverage artefact is produced
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-10-08 14:35 BST: Grace started. Moved to In Progress by Fred Brooks.

Review 2026-10-08 (Fred Brooks): PR #6 head 83cf89f read in full. Two new files only (.github/workflows/fork-quality.yml, tools/quality/coverage.sh); job guarded by github.repository; contents: read; persist-credentials false; gcovr pinned 8.6; vendored pugixml and crypto/external excluded; all checks green. No blockers. Nits: branch name is pws-05-coverage-job rather than codex/PWS-05-...; actions pinned by tag, not SHA. Next: QA (Edsger) on AC 1-3 and 5; AC 4 after merge.

QA 2026-10-08 16:50 BST (Edsger Dijkstra):

Verdicts (AC checkboxes left unticked; status unchanged):
- AC 1 PASS. Job https://github.com/rjbarbour/pwsafe/actions/runs/37787860322/job/113347166782 (run 37787860322, head 83cf89f, event pull_request). Configure step log shows CMAKE_BUILD_TYPE:STRING=Debug, CMAKE_EXPORT_COMPILE_COMMANDS:UNINITIALIZED=ON, USE_INTERPROCEDURAL_OPTIMIZATION:BOOL=OFF, CMAKE_C_FLAGS:STRING=--coverage -O0, CMAKE_CXX_FLAGS:STRING=--coverage -O0, CMAKE_EXE_LINKER_FLAGS:STRING=--coverage. PR #6 diff names only .github/workflows/fork-quality.yml and tools/quality/coverage.sh; CMakePresets.json and CMakeLists.txt are not in the diff (gh pr diff 6 --name-only; compare master...83cf89f).
- AC 2 PASS. Same run: step "Run Coretests" ran `ctest --test-dir build -R Coretests --output-on-failure`; Coretests Passed 74.38s; "100% tests passed, 0 tests failed out of 1". pip installed gcovr==8.6; `gcovr --version` printed "gcovr 8.6". Artefact coverage-83cf89fb0c9d9d7c69ecca4535f4d766ed43468d (id 11555745328) downloaded with gh run download 37787860322; contains coverage.json, coverage.cobertura.xml, coverage_summary.txt.
- AC 3 PASS. coverage_summary.txt per-directory header lists src/core, src/os/unix, src/os only. Parsed 131 file rows: all under src/core/ or src/os/; zero matches for pugixml or crypto/external in the summary text and in coverage.json file list.
- AC 4 NOT CHECKED. Requires the first job run on master after merge; not available yet.
- AC 5 PASS (by workflow inspection). fork-quality.yml at 83cf89f has `if: github.repository == 'rjbarbour/pwsafe'` on the coverage job; comment states other repositories skip and upload nothing. Could not trigger the workflow in another repository from this check; the skip is the job-level `if`, which GitHub evaluates before steps run.

Non-blocking: CMAKE_EXPORT_COMPILE_COMMANDS appears as UNINITIALIZED=ON in CMakeCache (still ON). PR coverage figures (src/core 7656/19423 lines, 927/1493 functions; src/os/unix 431/1988, 54/196) differ slightly from the f24fd88 baseline cited in AC 4; re-check on the first master run. Fred's nits (branch name; actions pinned by tag not SHA) stand.

PR #6 squash-merged 2026-10-08 as 35c62e7 by Fred Brooks under Robert's standing rule for fork-only platform PRs (CI green, Fred review, Edsger QA 6ce79a0 AC 1-3 and 5). Stays in Review until Grace records AC 4 from the first master run.
<!-- SECTION:NOTES:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 12:55
---
DoR check 2026-10-08 (Fred Brooks): fail. Decision to add: coverage flags (--coverage -O0 and the coverage linker flags) are set in the fork-only workflow's configure step; CMakePresets.json and other upstream files are not edited. The title, description and AC #1 still call for a coverage preset; reword AC #1 to the workflow's configure step. Also record where the drafts (coverage.sh, fork-quality.yml) are, as they are not in the repository.
---

author: @fred-brooks
created: 2026-10-08 13:06
---
DoR re-check 2026-10-08 (Fred Brooks): pass. Prior gaps closed: coverage flags live in the fork-only workflow's configure step; CMakePresets.json and CMakeLists.txt stay untouched; draft locations recorded. Build commitment (project default).
---
<!-- COMMENTS:END -->
