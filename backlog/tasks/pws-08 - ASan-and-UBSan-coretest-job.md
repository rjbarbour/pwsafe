---
id: PWS-08
title: ASan and UBSan coretest job
status: To Do
assignee: []
created_date: '2026-10-08 12:50'
labels:
  - quality
dependencies: []
type: chore
ordinal: 8000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A fork-only CI job builds `coretest` with AddressSanitizer and UndefinedBehaviorSanitizer together and runs Coretests, so memory and undefined-behaviour errors reached by the tests fail the run. There is no draft for this job in Grace Hopper's material. On `master`, `CMakeLists.txt` reads `USE_ASAN` but not `USE_UBSAN`, so the existing `linux-ubsan-debug` preset does not by itself add `-fsanitize=undefined`.

Code-quality stack agreed in the pwsafe platform room; requested by Fred Brooks, 2026-10-08.

Exclusions: the upstream workflows (`cmake-build.yml`, `codeql-analysis.yml`, `macos-latest.yml`, `macos-cmake-latest.yml`) stay untouched; fork-only, never part of an upstream pull request; any gate covers new or changed code only; no SonarQube Cloud or CodeRabbit; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given a pull request to `master` in rjbarbour/pwsafe, when the sanitiser job builds `coretest`, then every `coretest` compile command in the job's `compile_commands.json` or build log contains both `-fsanitize=address` and `-fsanitize=undefined`
- [ ] #2 Given that build, when `ctest -R Coretests` runs and no sanitiser reports an error, then the job passes and its log contains no `ERROR: AddressSanitizer` line and no `runtime error:` line
- [ ] #3 Given a throwaway branch that adds one Coretests case with a heap buffer overflow and another with signed integer overflow, when the job runs on it, then the job fails, the log shows an AddressSanitizer report and a `runtime error:` report, and the branch is deleted unmerged with its run URL in the task notes
- [ ] #4 Given the same workflow in any repository other than rjbarbour/pwsafe, when it is triggered, then the sanitiser job is skipped
<!-- AC:END -->
