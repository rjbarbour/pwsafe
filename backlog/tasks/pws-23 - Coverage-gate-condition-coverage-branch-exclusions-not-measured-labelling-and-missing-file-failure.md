---
id: PWS-23
title: >-
  Coverage gate: condition coverage, branch exclusions, not-measured labelling
  and missing-file failure
status: To Do
assignee:
  - '@grace-hopper'
created_date: '2026-10-08 16:58'
updated_date: '2026-10-08 17:03'
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

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
DoR check 2026-10-08 (Fred Brooks, Definition of Ready v1.3) at 68cc03346, against §11 of backlog/docs/test-strategy.md at 054c0ab29: fail on two blocking gaps; status unchanged (To Do).
Met:
- RD-01: it owns §11 rows 2, 4, 5 and 6, under Fred Brooks's decision of 2026-10-08.
- RD-02: fork-only, limited to .github/workflows/fork-*.yml and tools/quality/, with no src/ or upstream workflow change and no coverage percentage limit.
- RD-05: platform work, owned by Grace Hopper.
- RD-06: delivered by pull request, with Fred Brooks and Dennis Ritchie reviewing, and the standard merge AC is last (AC 10).
- RD-07: AC 1 waits on Grace's runner confirmation.
- Consistency with §11: AC 1 and AC 2 match row 2, AC 3 and AC 4 match row 4 and §4 (branches only, count computed and printed), AC 5 matches row 5, and AC 6 and AC 7 match row 6 and §5.
Gap 1, blocking (RD-03, testability of AC 6 and AC 7): the gate must decide whether a missing file 'has executable lines', but §5 itself says the gate cannot prove that, and no AC says how it decides. Proposed rule, for both AC 6/7 and §5: 'A changed source file (.c, .cpp) under src/core, src/os/unix or directly under src/os that is missing from the coverage report fails the gate and is named. A changed header (.h) missing from the report is listed as "not in coverage report: no executable code, confirm in review", and both code reviewers confirm it.' Every file directly under src/os is a header today.
Gap 2, blocking (RD-04, open scope decision): two gates in §11 name PWS-07 as owner, but PWS-07's ACs don't cover them:
- Row 1 asks for 100% line and branch on changed lines, then condition. PWS-07 AC 2 checks 80% of changed lines covered, with no branch or condition check.
- Row 7 puts the reviewed exemption file under tools/quality/ with PWS-07, which has no AC for it.
With PWS-07's scope unchanged, both fall to this task or to another new task. If this task takes them, it needs ACs for (a) branch and condition checks on changed lines in gate_changed.py, and (b) reading the exemption file (path, lines, reason; measured files only). AC 3's 'no exclusion beyond the vendored-directory filters' also needs to allow that file. Fred Brooks decides.
Non-blocking:
(1) AC 5's reasons ('GUI wiring reviewed by hand' for src/ui, 'macOS-only' for src/os/mac) differ from the §5 label 'not measured (GUI or platform wiring, reviewed by hand)'. Use the §5 labels word for word.
(2) AC 8 should name the coverage tool for the Python gate logic, for example coverage.py with branch measurement, and say where those tests run.
(3) RAID R-09 (ubuntu-latest moves to 26.04 on 19 October 2026) and R-05 bear on AC 1's runner and re-baseline. Link them in the notes.
(4) The dependencies field could add PWS-22, because the description relies on its approval.
(5) Name a QA owner.
No vulnerability or CodeQL specifics appear.
<!-- SECTION:NOTES:END -->
