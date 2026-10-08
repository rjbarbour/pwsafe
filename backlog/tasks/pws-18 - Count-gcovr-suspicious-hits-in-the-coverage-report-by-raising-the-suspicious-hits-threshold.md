---
id: PWS-18
title: >-
  Count gcovr suspicious hits in the coverage report by raising the
  suspicious-hits threshold
status: To Do
assignee: []
created_date: '2026-10-08 15:57'
updated_date: '2026-10-08 15:59'
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

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
DoR check 2026-10-08 (Fred Brooks, Definition of Ready v1.3): pass, with one recommended tightening. RD-01: the outcome is explicit (the lines gcovr now treats as suspicious are counted), and the benefit is accurate coverage figures (RAID R-10). RD-02: scope and exclusions are explicit (coverage.sh only; no gate, flags, filters or src/ change). RD-03: AC 1-5 are concrete and deterministic. Recommended for AC 3: the before and after runs use the same runner image and compiler, as the job log shows. Otherwise the ubuntu-latest move to 26.04 on 19 October 2026 (RAID R-09) could change other lines and fail AC 3 for a reason unrelated to this task. RD-04: depends on PWS-05 (Done); no decision outstanding. RD-05: low risk, reversible, report-only job, Build commitment (project default). RD-06: one file changes; QA by Edsger Dijkstra; two code reviews (AC 5); the gate after is Done and closing RAID R-10. RD-07: project defaults; if the observed hit counts are close enough to a real counter overflow that no threshold separates them, stop and return to Fred Brooks. Stays in To Do while Ready holds 3 (PWS-06, PWS-07, PWS-13).
<!-- SECTION:NOTES:END -->
