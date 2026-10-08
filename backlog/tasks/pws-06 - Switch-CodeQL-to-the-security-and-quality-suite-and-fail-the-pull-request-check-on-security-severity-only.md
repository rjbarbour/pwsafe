---
id: PWS-06
title: >-
  Switch CodeQL to the security-and-quality suite and fail the pull request
  check on security severity only
status: Shaping
assignee: []
created_date: '2026-10-08 12:50'
updated_date: '2026-10-08 12:58'
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
- [ ] #1 Given the change is on fork `master`, when `git diff 3996b15 HEAD -- .github/workflows/cmake-build.yml .github/workflows/codeql-analysis.yml .github/workflows/macos-latest.yml .github/workflows/macos-cmake-latest.yml` is run, then the only difference is the added `queries: security-and-quality` line in `.github/workflows/codeql-analysis.yml`
- [ ] #2 Given the first CodeQL run on `master` after the change, when QA reads the Initialize CodeQL step of its log, then it shows the `security-and-quality` suite, and the number of queries run is greater than in the PWS-03 baseline run
- [ ] #3 Given that run, when QA reads the task notes, then they record the open alert total for `refs/heads/master` and its breakdown in the same form as PWS-03, next to the PWS-03 figures
- [ ] #4 Given a test pull request to `master` that introduces only an alert with no security severity, when CodeQL runs, then the CodeQL check passes and the alert is listed on the pull request
- [ ] #5 Given a test pull request to `master` that introduces an alert with security severity high or critical, when CodeQL runs, then the CodeQL check fails
- [ ] #6 Given both test pull requests, when the task is finished, then they are closed unmerged and their run URLs are in the task notes
- [ ] #7 Given Robert Barbour has changed the code-scanning check-failure setting on rjbarbour/pwsafe, when QA reads the task notes, then they record that security alerts fail the check at high or above and that quality-only alerts never fail it, with the date Robert confirmed it
<!-- AC:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 12:55
---
DoR check 2026-10-08 (Fred Brooks): fail. Decision to add: the pull request check fails on security severity high and above; quality-only alerts are reported but do not block. AC #5 should name that level rather than a level recorded in the task notes. Also name who changes the repository's code-scanning check-failure setting, which needs admin rights on rjbarbour/pwsafe.
---
<!-- COMMENTS:END -->
