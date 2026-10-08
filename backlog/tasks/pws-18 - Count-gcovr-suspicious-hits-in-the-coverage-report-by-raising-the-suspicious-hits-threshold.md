---
id: PWS-18
title: >-
  Count gcovr suspicious hits in the coverage report by raising the
  suspicious-hits threshold
status: To Do
assignee: []
created_date: '2026-10-08 15:57'
labels:
  - quality
dependencies:
  - PWS-05
modified_files:
  - tools/quality/coverage.sh
type: chore
ordinal: 18000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
gcovr currently treats 4 line hit counts in the coretest coverage run as "suspicious" (for example `src/core/crypto/bitops.h:285`) and, because `tools/quality/coverage.sh` passes `--gcov-ignore-parse-errors=suspicious_hits.warn_once_per_file`, leaves those lines out of the report, so a few in-scope crypto lines are under-reported. `coverage.sh` sets `--gcov-suspicious-hits-threshold` just above the highest hit count observed on those lines, so they are counted, while a genuinely overflowed counter, far above that, is still caught. From Dennis Ritchie's retrospective review of PR #6 (PWS-05 notes, finding 3).

Requested by Fred Brooks from Dennis Ritchie's review, 2026-10-08.

Exclusions: fork-only, never part of an upstream pull request; no change to the workflow, the filters or exclusions, or the coverage flags; no file under `src/` changes; no coverage gate is added; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the change, when QA reads `tools/quality/coverage.sh`, then it passes `--gcov-suspicious-hits-threshold` set to the smallest power of ten above the highest hit count observed on the currently suspicious lines, and the task notes record that highest count and the threshold chosen
- [ ] #2 Given a Fork quality coverage run after the change, when QA reads the gcovr output in its log, then there is no suspicious hits warning
- [ ] #3 Given the gcovr JSON from the last coverage run before the change and from the first run after it, both on the same commit of `src/`, when QA compares them line by line, then the only lines that differ are the ones gcovr reported as suspicious before the change, and the task notes list those lines and the before and after totals for `src/core` and `src/os`
- [ ] #4 Given the pull request, when QA reads its diff, then it changes only `tools/quality/coverage.sh`
- [ ] #5 Given the pull request for this task, when it is merged, then Fred Brooks and Dennis Ritchie have each recorded a code review, and every automated-check finding on it (CI, CodeQL, the fork quality gate or any other check) has been addressed by disabling or tuning the rule, suppressing it in code within this task's limits, mitigating or fixing it, or recording the residual risk in `backlog/docs/raid-log.md`, and the pull request or task notes say which for each finding
<!-- AC:END -->
