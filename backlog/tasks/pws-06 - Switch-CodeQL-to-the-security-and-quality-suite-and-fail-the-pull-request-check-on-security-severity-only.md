---
id: PWS-06
title: >-
  Switch CodeQL to the security-and-quality suite and fail the pull request
  check on security severity only
status: To Do
assignee: []
created_date: '2026-10-08 12:50'
updated_date: '2026-10-08 16:41'
labels:
  - quality
dependencies:
  - PWS-03
type: chore
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
CodeQL on the fork runs the `security-and-quality` query suite. The CodeQL check on a pull request fails only for new alerts with security severity high or above; quality-only alerts are reported on the pull request but do not block. This task changes exactly two things. First, one line, `queries: security-and-quality`, is added under `with:` in the `github/codeql-action/init@v4.38.2` step of `.github/workflows/codeql-analysis.yml`; nothing else in that file changes. Second, the fork repository's code-scanning check-failure setting is changed so that security alerts fail the check at high or above and quality-only alerts never fail it. That setting needs admin rights on rjbarbour/pwsafe, so Robert Barbour changes it; the implementer makes the workflow change and records the setting in the task notes once Robert confirms it.

Code-quality stack agreed in the pwsafe platform room; requested by Fred Brooks, 2026-10-08. Failing level (high and above) decided by Fred Brooks, 2026-10-08.

Exclusions: `cmake-build.yml`, `macos-latest.yml` and `macos-cmake-latest.yml` stay untouched, and `codeql-analysis.yml` changes only by the line above; fork-only, never part of an upstream pull request; the check fails on alerts new to the pull request only; no SonarQube Cloud or CodeRabbit; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the change is on fork `master`, when QA diffs `.github/workflows/cmake-build.yml`, `.github/workflows/codeql-analysis.yml`, `.github/workflows/macos-latest.yml` and `.github/workflows/macos-cmake-latest.yml` against the commit immediately before this task's change, then the only difference is the added `queries: security-and-quality` line under the `github/codeql-action/init@v4.38.2` step of `codeql-analysis.yml`
- [ ] #2 Given the first CodeQL run on `master` after the change, when QA reads the Initialize CodeQL step of its log and the uploaded analysis, then it shows the `security-and-quality` suite, the analysis lists a non-zero rule count (an analysis with 0 rules and 0 results is not a real scan), and the number of queries run is greater than in the PWS-03 baseline run
- [ ] #3 Given that run, when QA reads the task notes, then they record the open alert total for `refs/heads/master` and its breakdown in the same form as PWS-03, next to the PWS-03 figures, and those figures come from an analysis with a non-zero rule count
- [ ] #4 Given a test pull request to `master` that introduces only an alert with no security severity, when CodeQL runs, then the CodeQL check passes and the alert is listed on the pull request
- [ ] #5 Given a test pull request to `master` that introduces an alert with security severity high or critical, when CodeQL runs, then the CodeQL check fails
- [ ] #6 Given both test pull requests, when the task is finished, then they are closed unmerged and their run URLs are in the task notes
- [ ] #7 Given Robert Barbour has changed the code-scanning check-failure setting on rjbarbour/pwsafe, when QA reads the task notes, then they record that security alerts fail the check at high or above and that quality-only alerts never fail it, with the date Robert confirmed it
- [ ] #8 Given the pull request for this task, when it is merged, then Fred Brooks and Dennis Ritchie have each recorded a code review, and every automated-check finding on it (CI, CodeQL, the fork quality gate or any other check) has been addressed by disabling or tuning the rule, suppressing it in code within this task's limits, mitigating or fixing it, or recording the residual risk in `backlog/docs/raid-log.md`, and the pull request or task notes say which for each finding
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-10-08 14:32 BST: Dependency PWS-03 is Done; moved from To Do to Ready by Fred Brooks (DoR passed earlier).

2026-10-08 14:35 BST: DoR re-check after AC edit b7f3de5 (Fred Brooks): pass, stays Ready. Non-blocking: AC 1 diffs the other three workflows against 3996b15, which would fail if PWS-12 (macos-latest.yml) or PWS-14 (macos-cmake-latest.yml) lands first; diffing all four against the commit before this task's change avoids the ordering dependency.

DoR re-check after standard merge AC: pass. AC 8 is testable (two recorded code reviews, and a stated disposition for each automated-check finding), and it doesn't conflict with AC 4-6, because the test pull requests are closed unmerged and AC 8 covers only this task's pull request. Note for execution: the suite switch may show alerts on existing code as new on this pull request; each still needs a disposition, and in public notes alerts are referred to by code-scanning alert number only, with no file, line or rule name. Stays in Ready.

2026-10-08 (Fred Brooks): returned from Ready to To Do to keep Ready within the limit of 1 to 3 when PWS-02 became Ready. Its DoR pass still stands.
<!-- SECTION:NOTES:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 12:55
---
DoR check 2026-10-08 (Fred Brooks): fail. Decision to add: the pull request check fails on security severity high and above; quality-only alerts are reported but do not block. AC #5 should name that level rather than a level recorded in the task notes. Also name who changes the repository's code-scanning check-failure setting, which needs admin rights on rjbarbour/pwsafe.
---

author: @fred-brooks
created: 2026-10-08 13:06
---
DoR re-check 2026-10-08 (Fred Brooks): pass. Prior gaps closed: PR check fails on security severity high and above; Robert Barbour changes the admin check-failure setting; AC #5 and #7 name that. Depends on PWS-03 (Ready). Build commitment (project default).
---

author: @fred-brooks
created: 2026-10-08 13:07
---
Passed DoR 2026-10-08; held in To Do under the 1–3 Ready limit until its dependency (PWS-03) is Done. No content gap.
---

author: @fred-brooks
created: 2026-10-08 13:43
---
DoR re-check 2026-10-08 (Fred Brooks): AC 1 now compares all four workflows against the parent of this task's change; still passes.
---
<!-- COMMENTS:END -->
