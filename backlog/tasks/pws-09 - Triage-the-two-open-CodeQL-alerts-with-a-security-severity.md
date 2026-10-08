---
id: PWS-09
title: Triage the two open CodeQL alerts with a security severity
status: In Progress
assignee:
  - '@dennis-ritchie'
created_date: '2026-10-08 12:50'
updated_date: '2026-10-08 13:12'
labels:
  - quality
dependencies: []
type: task
ordinal: 9000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Each of the two open CodeQL alerts with a security severity, first reported on the analysis of codex/PWS-02-diceware-passphrase at db9dab1 (see the repository's code-scanning page) gets a recorded verdict: false positive, dismissed in CodeQL as False positive; no defect reachable from current callers, dismissed in CodeQL as Won't fix; or true positive, with the follow-up raised privately with Robert Barbour. Verdicts in the task notes use code-scanning alert numbers only, with no file, line or rule. Triage also records whether each alert comes from code that PR #2 changed or from existing upstream code. No code fix is in scope.

Code-quality stack agreed in the pwsafe platform room; requested by Fred Brooks, 2026-10-08.

Exclusions: the upstream workflows (`cmake-build.yml`, `codeql-analysis.yml`, `macos-latest.yml`, `macos-cmake-latest.yml`) stay untouched; fork-only, never part of an upstream pull request; any gate covers new or changed code only; no SonarQube Cloud or CodeRabbit; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the two open CodeQL alerts with a security severity, first reported on the analysis of codex/PWS-02-diceware-passphrase at db9dab1 (see the repository's code-scanning page), when triage is finished, then the task notes hold exactly two verdicts, one per alert, identified by code-scanning alert number only, each one of "false positive, dismissed in CodeQL as False positive", "no defect reachable from current callers, dismissed in CodeQL as Won't fix" or "true positive, follow-up raised privately with Robert Barbour", with no file path, line number or rule name
- [ ] #2 Given each verdict, when QA reads the task notes, then they state whether that alert comes from code that PR #2 changed or from existing upstream code, and QA can confirm it against the PR #2 diff from 3996b15 to db9dab1
- [ ] #3 Given a verdict of false positive or of no defect reachable from current callers, when QA opens that alert on the repository's code-scanning page, then it is dismissed with the reason "False positive" or "Won't fix" to match the verdict, and a dismissal comment that states why; dismissals are made only after Robert Barbour agrees, as they are recorded under his name
- [ ] #4 Given a true-positive verdict, when QA opens that alert on the repository's code-scanning page, then it is still open, and the task, its commits and any pull request contain no file path, line number, rule name or other detail of it
- [ ] #5 Given the task's commits, when QA lists the files they change, then no file under `src/` is changed
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Triage by Dennis Ritchie, reviewed by Barbara Liskov, against codex/PWS-02-diceware-passphrase at 5beca97 (the flagged code is identical at db9dab1).

- Alert #2: false positive. Comes from existing upstream code; the PR #2 diff from 3996b15 to db9dab1 does not change the file it is in. To be dismissed in CodeQL as False positive once Robert Barbour agrees.
- Alert #1: no defect reachable from current callers. Comes from existing upstream code; the PR #2 diff from 3996b15 to db9dab1 does not change the file it is in. To be dismissed in CodeQL as Won't fix, reason "upstream code, not reachable from current callers, out of scope for this fork", once Robert Barbour agrees.

Both alerts are in existing upstream code that PR #2 doesn't change. Review found no defect reachable from current callers. No file under src/ changed.
<!-- SECTION:NOTES:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 12:55
---
DoR check 2026-10-08 (Fred Brooks): pass. Outcome, scope (no code fix), acceptance evidence and QA route are explicit; true-positive handling keeps detail out of the repository; no dependencies or open decisions; Build commitment (project default).
---

author: @fred-brooks
created: 2026-10-08 13:06
---
Claimed In Progress; assignee Dennis Ritchie.
---
<!-- COMMENTS:END -->
