---
id: PWS-16
title: >-
  Widen the password field on the Add/Edit Entry Basic tab to match the Username
  field
status: To Do
assignee: []
created_date: '2026-10-08 13:19'
updated_date: '2026-10-08 13:43'
labels: []
dependencies:
  - PWS-02
modified_files:
  - src/ui/wxWidgets/AddEditPropSheetDlg.cpp
type: chore
ordinal: 16000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
On the Basic tab of the Add Entry and Edit Entry dialogs, the Password field is widened to match the Username field above it, about 50% wider than now, so longer passwords such as six-word passphrases can be read in full when shown. The buttons beside the Password field are rearranged as needed to make room. The change doesn't depend on passphrases, but longer passphrases make it more useful.

Requested by Robert Barbour in the pwsafe diceware room, 2026-10-08, after trying the PWS-02 build on his Mac; split out from PWS-02 by Fred Brooks.

It touches the same dialog as the PWS-02 rework, so it is best sequenced after that rework to avoid a merge clash. The Confirm field's width is not part of the request, and the implementer should raise it if leaving it unchanged looks wrong.

Exclusions: layout only, with no change to what any control does; no change to `PWPolicy`, the file format or the generator; no other tab or dialog changes; the same branch and upstream rules as PWS-02 apply; no secrets; no `*.psafe3` file is committed.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the Add Entry or Edit Entry dialog open on the Basic tab at its default size, on macOS and on Linux/GTK, when QA compares the fields, then the Password field's left and right edges line up with the Username field's, and the task notes record both widths before and after the change
- [ ] #2 Given Show Password and a password of up to 50 characters in the field, when QA looks at the field at the dialog's default size, then the whole password is visible without scrolling
- [ ] #3 Given the controls that sat beside the Password field before the change, when QA uses each one after the change, then every control is still present, visible and does what it did before
- [ ] #4 Given the change, when QA compares the Basic tab with the build before it, then no field other than Password, and no control other than those rearranged beside it, has moved or changed size, and `coretest` passes
<!-- AC:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 13:43
---
DoR check 2026-10-08 (Fred Brooks): fail. Add PWS-02 as a dependency; it edits the same Basic tab and is back in Shaping pending Robert's storage choice. Re-check after that dependency is recorded.
---

author: @fred-brooks
created: 2026-10-08 13:43
---
DoR re-check 2026-10-08 (Fred Brooks): dependency on PWS-02 recorded. Held in To Do until PWS-02 is Done.
---
<!-- COMMENTS:END -->
