---
id: PWS-09
title: Triage the two open CodeQL alerts with a security severity
status: To Do
assignee: []
created_date: '2026-10-08 12:50'
updated_date: '2026-10-08 12:52'
labels:
  - quality
dependencies: []
type: task
ordinal: 9000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Each of the two open CodeQL alerts with a security severity, first reported on the analysis of codex/PWS-02-diceware-passphrase at db9dab1 (see the repository's code-scanning page) gets a recorded verdict: false positive, dismissed in CodeQL with the reason given there, or true positive, with the follow-up raised privately with Robert Barbour. Triage also records whether each alert comes from code that PR #2 changed or from existing upstream code. No code fix is in scope.

Code-quality stack agreed in the pwsafe platform room; requested by Fred Brooks, 2026-10-08.

Exclusions: the upstream workflows (`cmake-build.yml`, `codeql-analysis.yml`, `macos-latest.yml`, `macos-cmake-latest.yml`) stay untouched; fork-only, never part of an upstream pull request; any gate covers new or changed code only; no SonarQube Cloud or CodeRabbit; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the two open CodeQL alerts with a security severity, first reported on the analysis of codex/PWS-02-diceware-passphrase at db9dab1 (see the repository's code-scanning page), when triage is finished, then the task notes hold exactly two verdicts, one per alert, each either "false positive, dismissed in CodeQL" or "true positive, follow-up raised privately with Robert Barbour"
- [ ] #2 Given each verdict, when QA reads the task notes, then they state whether that alert comes from code that PR #2 changed or from existing upstream code, and QA can confirm it against the PR #2 diff from 3996b15 to db9dab1
- [ ] #3 Given a false-positive verdict, when QA opens that alert on the repository's code-scanning page, then it is dismissed with the reason "False positive" and a dismissal comment that states why
- [ ] #4 Given a true-positive verdict, when QA opens that alert on the repository's code-scanning page, then it is still open, and the task, its commits and any pull request contain no file path, line number, rule name or other detail of it
- [ ] #5 Given the task's commits, when QA lists the files they change, then no file under `src/` is changed
<!-- AC:END -->
