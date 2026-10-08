---
id: PWS-19
title: >-
  Record Option B (Diceware policy flag stored in the safe file) as a decision,
  no code
status: To Do
assignee: []
created_date: '2026-10-08 16:06'
labels:
  - decision
dependencies:
  - PWS-02
type: chore
ordinal: 19000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Robert chose Option A for PWS-02 on 2026-10-08 (an app-scope Preferences setting, no file-format change). Option B, a Diceware policy flag stored in the safe file, is recorded as a Backlog.md decision record only: no code, no branch other than fork master, no pull request. It becomes a pwsafe/pwsafe issue only with Robert's approval, if Option A gets traction. Barbara Liskov writes it once assigned.

Exclusions: no change under `src/`, no workflow or build file change, nothing raised on pwsafe/pwsafe without Robert's approval; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the decision record on fork master under `backlog/decisions/`, when it is read, then it describes the policy flag bit in the safe file, where the word count is stored, and why Option A was chosen for now
- [ ] #2 Given the decision record on fork master under `backlog/decisions/`, when it is read, then it describes how older Password Safe builds behave with a safe carrying the flag: release builds fail to generate a password ("Couldn't generate password - invalid policy"), and the older wxWidgets policy dialogs drop unknown bits when an entry or named policy is edited, citing `PasswordPolicyDlg.cpp` and `AddEditPropSheetDlg.cpp`
- [ ] #3 Given the decision record on fork master under `backlog/decisions/`, when it is read, then it lists the tests Option B would need: core save-and-reload tests at entry, named-policy and default-policy level, an older-build fallback test, and a dropped-bit test
- [ ] #4 Given the decision record on fork master under `backlog/decisions/`, when it is read, then it states that Option B is raised on pwsafe/pwsafe only with Robert's approval
- [ ] #5 Given the commit that adds the record, when its diff is inspected, then it touches only files under `backlog/` and no file under `src/`, no workflow file and no build file
<!-- AC:END -->
