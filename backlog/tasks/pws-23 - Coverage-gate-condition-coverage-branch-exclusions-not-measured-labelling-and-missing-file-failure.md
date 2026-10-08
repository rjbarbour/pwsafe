---
id: PWS-23
title: >-
  Coverage gate: condition coverage, branch exclusions, not-measured labelling
  and missing-file failure
status: To Do
assignee:
  - '@grace-hopper'
created_date: '2026-10-08 16:58'
labels:
  - quality
dependencies:
  - PWS-07
  - PWS-18
type: chore
ordinal: 23000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Fred Brooks decided on 2026-10-08 that this one platform task owns gates 2, 4, 5 and 6 in §11 of `backlog/docs/test-strategy.md` (PWS-22). PWS-07's scope is unchanged. PWS-18 only sets the suspicious-hits threshold and may only touch `coverage.sh`, so it cannot take these gates. This task extends `tools/quality/gate_changed.py` (from PWS-07) and `tools/quality/coverage.sh` (from PWS-18) once those have merged.

It is a fork-only change limited to `.github/workflows/fork-*.yml` and `tools/quality/`, with no upstream workflow or `src/` change. It does not set the coverage percentage limit: raising PWS-07 AC 2's limit is a separate tracker change after Robert Barbour approves PWS-22. Once PWS-22 is approved, `backlog/docs/test-strategy.md` defines how these measures work.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given Grace Hopper's confirmation of the runner (recommended `ubuntu-26.04` with GCC 15.2), when the coverage job runs on a pull request, then it uses a compiler that supports condition coverage (GCC 14 or later), and the task notes record the runner, the compiler version and the one coverage re-baseline
- [ ] #2 Given a pull request that changes a measured file, when the coverage job runs, then the coverage report includes condition coverage for that file alongside line and branch coverage
- [ ] #3 Given the coverage job, when it runs gcovr, then it passes `--exclude-throw-branches` and `--exclude-unreachable-branches`, and no exclusion beyond the vendored-directory filters already in place
- [ ] #4 Given gcovr does not report how many branches it excluded, when the coverage job runs, then it computes that count and prints it in the job log and in the coverage summary
- [ ] #5 Given a pull request that changes a file under `src/ui`, `src/os/mac` or `src/os/windows`, when the gate runs, then the report lists the file as not measured with its reason (GUI wiring reviewed by hand for `src/ui`, macOS-only for `src/os/mac`, and "not built in fork CI" for `src/os/windows`), and the gate does not fail on it
- [ ] #6 Given a pull request that changes a file under `src/core` or `src/os/unix`, or directly under `src/os`, and the file is missing from the coverage report and has executable lines, when the gate runs, then the gate fails and names the file
- [ ] #7 Given such a missing file that has no executable lines, when the gate runs, then the report lists it as "not in coverage report: no executable code, confirm in review" and the gate does not fail on it
- [ ] #8 Given the new or changed gate logic in `tools/quality/`, when its tests run, then each case in AC 4 to AC 7 has a unit test with a fixture coverage report, and every branch of the new code is covered
- [ ] #9 Given the pull request diff, when it is read, then it touches only `.github/workflows/fork-*.yml` and `tools/quality/`, with no upstream workflow and no `src/` file
- [ ] #10 Given the pull request for this task, when it is merged, then Fred Brooks and Dennis Ritchie have each recorded a code review, and every automated-check finding on it (CI, CodeQL, the fork quality gate or any other check) has been addressed by disabling or tuning the rule, suppressing it in code within this task's limits, mitigating or fixing it, or recording the residual risk in `backlog/docs/raid-log.md`, and the pull request or task notes say which for each finding
<!-- AC:END -->
