---
id: PWS-05
title: >-
  Fork-only CI job that builds coretest with coverage flags and publishes gcovr
  coverage
status: Done
assignee:
  - '@grace-hopper'
created_date: '2026-10-08 12:49'
updated_date: '2026-10-08 16:08'
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
- [x] #1 Given a clean checkout of fork `master` on `ubuntu-latest`, when the coverage job's configure step runs and `coretest` is built, then the step's log shows `CMAKE_BUILD_TYPE=Debug`, `CMAKE_EXPORT_COMPILE_COMMANDS=ON`, `USE_INTERPROCEDURAL_OPTIMIZATION=OFF`, `--coverage -O0` in both `CMAKE_C_FLAGS` and `CMAKE_CXX_FLAGS`, and `--coverage` in `CMAKE_EXE_LINKER_FLAGS`; and given the pull request that adds the job, when QA reads its diff, then `CMakePresets.json` and `CMakeLists.txt` are unchanged
- [x] #2 Given a push to `master` or a pull request to `master` in rjbarbour/pwsafe, when the coverage job runs, then `ctest -R Coretests` passes and the run uploads `coverage.json`, `coverage.cobertura.xml` and a text summary produced by gcovr 8.6 as an artefact
- [x] #3 Given that artefact, when QA reads the text summary, then it lists files under `src/core` and `src/os` only and no file under `src/core/pugixml` or `src/core/crypto/external`
- [x] #4 Given the first job run on `master`, when QA reads the task notes, then they record its line and function coverage for `src/core` and `src/os/unix` next to Grace Hopper's baseline at f24fd88 (`src/core` lines 7659/19424 = 39.4%, functions 930/1495 = 62.2%; `src/os/unix` lines 430/1988 = 21.6%, functions 54/196 = 27.6%)
- [x] #5 Given the same workflow runs in any repository other than rjbarbour/pwsafe, when it is triggered, then the coverage job is skipped and no coverage artefact is produced
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

AC #4 - first master run 2026-10-08 (Grace Hopper):
Run https://github.com/rjbarbour/pwsafe/actions/runs/37804161642 (job 113403925079, "Coverage (coretest, gcovr)"), event push, master commit 35c62e7 (the PR #6 squash merge), conclusion success, finished 16:54 BST. Coretests passed (1/1); gcovr 8.6; artefact coverage-35c62e7bad1502db631b3c86effdd1da0066de3d. Figures from its coverage_summary.txt (per-directory table, same counting as the baseline):
- src/core lines: 7656/19423 = 39.4% (baseline f24fd88 7659/19424 = 39.4%; delta -3 covered, -1 total, -0.01 pp)
- src/core functions: 927/1493 = 62.1% (baseline 930/1495 = 62.2%; delta -3 covered, -2 total, -0.12 pp)
- src/os/unix lines: 431/1988 = 21.7% (baseline 430/1988 = 21.6%; delta +1 covered, 0 total, +0.05 pp)
- src/os/unix functions: 54/196 = 27.6% (baseline 54/196 = 27.6%; no change)
Same figures as the PR #6 run 37787860322 that Edsger read, so CI is stable run to run. No file under src/ changed between f24fd88 and 35c62e7 (git diff --stat f24fd88 35c62e7 -- src is empty). Comparing per-file lines in the two coverage.json files, the differences sit in three files only: src/core/Command.cpp (baseline 349/760, CI 348/759), src/core/PWSprefs.cpp (261/979 vs 259/979) and src/os/unix/utf8conv.cpp (33/48 vs 34/48). Likely cause is the toolchain and environment: baseline built on the team box (Debian 13, GCC 14.2), CI on ubuntu-24.04 (g++ 13.2). Not a code change. AC 4 checkbox left for QA and Fred; status unchanged.

Retrospective code review 2026-10-08 16:56 BST (Dennis Ritchie): second review of PR #6 under Robert's two-review rule of 16:52 (PR #6 was merged at 16:51 on Fred's review alone).

Verdict: pass with findings. No blockers.

Scope: squash commit 35c62e7 (parent 7cc6b1fa4) adds exactly two files, `.github/workflows/fork-quality.yml` and `tools/quality/coverage.sh`. Both blobs are identical at PR head 83cf89f, at 35c62e7 and on master. No change under `src/`, to `CMakeLists.txt` or `CMakePresets.json`, or to any upstream workflow.

What was checked: both files read in full; shellcheck reports nothing on `coverage.sh`; actionlint reports nothing on `fork-quality.yml`; check-run annotations on 83cf89f read. `coverage.sh` has `set -euo pipefail`, quotes every expansion and writes only to the output directory it is given. The workflow uses `pull_request` (not `pull_request_target`), `permissions: contents: read`, `persist-credentials: false`, references no secrets, guards the job on `github.repository`, and writes only to `build/`, `coverage/` and `$RUNNER_TEMP`.

Findings (all non-blocking):
1. The concurrency comment ("every push to master keeps its own run") does not hold. GitHub keeps at most one running and one pending run per group, so a newer master push cancels the pending one whatever `cancel-in-progress` says. Seen on run 37804187626 (9b3e6a5ad): cancelled before any job started. Proposed: follow-up task (with 2): per-commit group for push events, or correct the comment.
2. Every push to master, including tracker-only commits, runs the full Debug coverage build. Proposed: same follow-up task: `paths-ignore: ['backlog/**']` on push; on `pull_request` only if the job is never made a required check, as a path-filtered required check stays pending.
3. The coverage job's own automated findings: gcovr "suspicious hits" warnings (4 hits, for example `src/core/crypto/bitops.h:285`). With `suspicious_hits` ignored, gcovr leaves those lines out of the report, so a few in-scope crypto lines are under-reported. Proposed: follow-up task to set `--gcov-suspicious-hits-threshold` in `coverage.sh` above the observed count (about 1.0e10) so the lines are counted and the check still catches real counter overflow; or a RAID entry if we accept the gap.
4. Runner notice on the same job: the `ubuntu-latest` label moves to Ubuntu 26 from 19 October 2026. A GCC/gcov change can shift the figures and the gcovr JSON shape (it already did once during PR #6). Proposed: RAID risk, linked to PWS-15 (ubuntu-26.04 spike); re-baseline after the migration, or pin `ubuntu-24.04`.
5. Actions are pinned by tag rather than SHA, and gcovr by version without hashes (extends Fred's nit). Mitigated by the read-only token, no secrets and `persist-credentials: false`; matches the upstream workflows. Proposed: RAID risk.
6. Observation, no action: the "UNEXPECTED files" check prints but does not fail. That is consistent with report-only and with AC 3.

DoD v1.1 check 2026-10-08 (Fred Brooks): DD-01 pass: AC 1, 2, 3 and 5 are ticked on Edsger Dijkstra's QA verdicts (6ce79a0: run 37787860322 and its coverage artefact; 131 files, all under src/core and src/os; the job-level github.repository guard). AC 5 was checked by reading the workflow, not by running it in another repository (RAID A-01). AC 4 is ticked on Grace Hopper's record (11a338604): master run 37804161642 on 35c62e7, with all four figures within 0.12 points of the f24fd88 baseline. Fred Brooks checked those figures against that run's coverage_summary.txt artefact (src/core 7656/19423 lines, 927/1493 functions; src/os/unix 431/1988 lines, 54/196 functions); Edsger has not separately QA'd AC 4. DD-02 pass: PR #6 was squash-merged as 35c62e7 on fork master, and the first master run 37804161642 (Fork quality, push) succeeded, with Coretests passing and the coverage artefact uploaded. DD-03 pass: two code reviews, Fred Brooks (848e07d) and Dennis Ritchie's retrospective review (2449a58, pass with findings, no blockers), plus Edsger Dijkstra's independent QA (6ce79a0). DD-04 pass: .github/workflows/fork-quality.yml and tools/quality/coverage.sh are the documentation, no upstream file changed, and residual risks are in backlog/docs/raid-log.md. DD-05 pass: residual risk and follow-up are logged as RAID R-05 (baseline difference, accepted), R-07 (pinned by tag and version, accepted), R-09 (Ubuntu 26 move), R-10 (gcovr suspicious hits; I-03 moved there) and I-04 (concurrency and coverage runs on tracker-only pushes); the next gate is Margaret Hamilton's follow-up platform tasks, PWS-18 for R-10 and PWS-17 for I-04. Overlay DO-04 (CI operations): the deployment evidence is the merge plus the first master run; the job reports coverage on every run as an artefact and a job summary; rollback is reverting the two fork-only files, with no upstream file involved. Result: meets DoD. Moved to Done by Fred Brooks.

QA 2026-10-08 (Edsger Dijkstra): AC 4

PASS. Independently checked against the first Fork quality push on master after the merge, not against Grace's or Fred's notes alone.

- Run https://github.com/rjbarbour/pwsafe/actions/runs/37804161642 (job 113403925079), event push, head 35c62e7 (PR #6 squash merge), conclusion success. Among fork-quality.yml runs with id ≤ 37804161642, this is the only successful push to master; earlier runs are pull_request only on pws-05-coverage-job. So it is the first master coverage job.
- Job log: Coretests Passed 66.29s (100%); gcovr 8.6; Image ubuntu-24.04; CXX GNU 13.3.0. Upload step produced artefact coverage-35c62e7bad1502db631b3c86effdd1da0066de3d (id 11561609532).
- Downloaded artefact with `gh run download 37804161642` into /workspace/qa-pws05/master-run/. coverage_summary.txt per-directory table: src/core lines 7656/19423 = 39.4%, functions 927/1493 = 62.1%; src/os/unix lines 431/1988 = 21.7%, functions 54/196 = 27.6%. Same four figures appear in the job log summary.
- Task notes (Grace, 11a338604) already record those figures next to the f24fd88 baseline stated in AC 4 (core 7659/19424 = 39.4%, 930/1495 = 62.2%; os/unix 430/1988 = 21.6%, 54/196 = 27.6%). That is what AC 4 requires.
- Versus the PR run 37787860322 artefact I read earlier: identical per-directory header (core 7656/19423, 927/1493; os/unix 431/1988, 54/196). CI is stable PR-to-master.
- Versus f24fd88 baseline: core lines −3 covered / −1 total (−0.01 pp), core functions −3 / −2 (−0.12 pp), os/unix lines +1 covered / 0 total (+0.05 pp), os/unix functions unchanged. `git diff --stat f24fd88 35c62e7 -- src` is empty, so the shift is not a source change under src/. Consistent with toolchain difference (CI ubuntu-24.04 / GCC 13.3 vs the local baseline environment). Accepted residual risk already in RAID R-05.

Status and AC checkboxes left unchanged.
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
