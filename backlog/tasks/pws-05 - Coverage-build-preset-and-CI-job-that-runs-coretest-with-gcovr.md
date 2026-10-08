---
id: PWS-05
title: Coverage build preset and CI job that runs coretest with gcovr
status: Shaping
assignee: []
created_date: '2026-10-08 12:49'
updated_date: '2026-10-08 12:55'
labels:
  - quality
dependencies: []
type: chore
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A CMake configure preset builds `coretest` with GCC coverage instrumentation, and a fork-only CI job runs Coretests with it and publishes gcovr line and function coverage for `src/core` and `src/os`, with the vendored `src/core/pugixml` and `src/core/crypto/external` excluded. It reports coverage and does not gate on it; the changed-line gate belongs to the fork quality gate task. Drafts: `tools/quality/coverage.sh` and the coverage build step in the draft `.github/workflows/fork-quality.yml` (Grace Hopper).

Code-quality stack agreed in the pwsafe platform room; requested by Fred Brooks, 2026-10-08.

Exclusions: the upstream workflows (`cmake-build.yml`, `codeql-analysis.yml`, `macos-latest.yml`, `macos-cmake-latest.yml`) stay untouched; fork-only, never part of an upstream pull request; any gate covers new or changed code only; no SonarQube Cloud or CodeRabbit; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given a clean checkout of fork `master` on `ubuntu-latest`, when the coverage preset named in the task notes is configured and `coretest` is built, then the configure output shows `CMAKE_BUILD_TYPE=Debug`, `CMAKE_EXPORT_COMPILE_COMMANDS=ON`, `USE_INTERPROCEDURAL_OPTIMIZATION=OFF` and `--coverage -O0` in both the C and C++ flags
- [ ] #2 Given a push to `master` or a pull request to `master` in rjbarbour/pwsafe, when the coverage job runs, then `ctest -R Coretests` passes and the run uploads `coverage.json`, `coverage.cobertura.xml` and a text summary produced by gcovr 8.6 as an artefact
- [ ] #3 Given that artefact, when QA reads the text summary, then it lists files under `src/core` and `src/os` only and no file under `src/core/pugixml` or `src/core/crypto/external`
- [ ] #4 Given the first job run on `master`, when QA reads the task notes, then they record its line and function coverage for `src/core` and `src/os/unix` next to Grace Hopper's baseline at f24fd88 (`src/core` lines 7659/19424 = 39.4%, functions 930/1495 = 62.2%; `src/os/unix` lines 430/1988 = 21.6%, functions 54/196 = 27.6%)
- [ ] #5 Given the same workflow runs in any repository other than rjbarbour/pwsafe, when it is triggered, then the coverage job is skipped and no coverage artefact is produced
<!-- AC:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 12:55
---
DoR check 2026-10-08 (Fred Brooks): fail. Decision to add: coverage flags (--coverage -O0 and the coverage linker flags) are set in the fork-only workflow's configure step; CMakePresets.json and other upstream files are not edited. The title, description and AC #1 still call for a coverage preset; reword AC #1 to the workflow's configure step. Also record where the drafts (coverage.sh, fork-quality.yml) are, as they are not in the repository.
---
<!-- COMMENTS:END -->
