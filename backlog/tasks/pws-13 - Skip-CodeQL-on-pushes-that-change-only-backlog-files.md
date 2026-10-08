---
id: PWS-13
title: Skip CodeQL on pushes that change only backlog files
status: Ready
assignee:
  - '@grace-hopper'
created_date: '2026-10-08 13:11'
updated_date: '2026-10-08 15:58'
labels: []
dependencies:
  - PWS-03
modified_files:
  - .github/workflows/codeql-analysis.yml
type: chore
ordinal: 13000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Pushes to fork `master` that change only files under `backlog/` no longer start a CodeQL analysis, so tracker-only commits stop cancelling the analysis already running for the previous code change. `.github/workflows/codeql-analysis.yml` gets a `paths-ignore: ['backlog/**']` filter on its `push` trigger. A push that also changes any file outside `backlog/` still runs CodeQL. This waits until PWS-03 has confirmed the CodeQL baseline on `master`.

Requested by Grace Hopper, relayed by Fred Brooks, 2026-10-08.

Exclusions: fork-only, never part of an upstream pull request; the `pull_request` and `schedule` triggers and the analysis steps are unchanged; no other workflow changes; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the change on fork `master`, when QA reads `.github/workflows/codeql-analysis.yml`, then the `push` trigger has `paths-ignore` with `backlog/**`, and the `pull_request` and `schedule` triggers and every job step are unchanged
- [ ] #2 Given a push to `master` that changes only files under `backlog/`, when it lands, then no CodeQL run starts for it and a CodeQL run already in progress on `master` is not cancelled
- [ ] #3 Given a push to `master` that changes a file outside `backlog/`, when it lands, then a CodeQL run starts as before and its uploaded analysis lists a non-zero rule count (an analysis with 0 rules and 0 results is not a real scan)
- [ ] #4 Given the task notes, when QA reads them, then they give the run URLs or commit SHAs for both checks above
- [ ] #5 Given the pull request for this task, when it is merged, then Fred Brooks and Dennis Ritchie have each recorded a code review, and every automated-check finding on it (CI, CodeQL, the fork quality gate or any other check) has been addressed by disabling or tuning the rule, suppressing it in code within this task's limits, mitigating or fixing it, or recording the residual risk in `backlog/docs/raid-log.md`, and the pull request or task notes say which for each finding
<!-- AC:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 13:43
---
DoR check 2026-10-08 (Fred Brooks): pass. Outcome, paths-ignore scope, acceptance evidence (including a non-zero rule count on a real scan) and QA route are explicit; PWS-03 is Done; Build commitment (project default).
---
<!-- COMMENTS:END -->
