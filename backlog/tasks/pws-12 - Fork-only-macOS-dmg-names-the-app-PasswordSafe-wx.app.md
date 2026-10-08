---
id: PWS-12
title: Fork-only macOS dmg names the app PasswordSafe-wx.app
status: To Do
assignee:
  - '@grace-hopper'
created_date: '2026-10-08 13:11'
updated_date: '2026-10-08 15:58'
labels: []
dependencies:
  - PWS-03
modified_files:
  - install/macosx/Makefile
  - .github/workflows/macos-latest.yml
type: chore
ordinal: 12000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The macOS dmg built by the fork's CI contains the app as `PasswordSafe-wx.app`, so Robert Barbour can install it beside Huvisoft's `pwsafe.app` in `/Applications`. Only the staged `.app` folder in the dmg is renamed. `install/macosx/Makefile` gains a variable `DMG_APP ?= pwsafe.app`, used for the `cp -R` destination, the ad hoc re-sign, and the `--volicon` and `--icon` lines of `create-dmg`. `RESOURCES` and the `.xcent` entitlements path keep pointing at Xcode's `pwsafe.app`. The fork's dmg workflow (`.github/workflows/macos-latest.yml`, step "Install language files and create dmg") passes `DMG_APP=PasswordSafe-wx.app`. With no override, the Makefile still produces `pwsafe.app`.

Low priority: no rebuild is needed now; it ships with the next fork-only CI change.

Requested by Robert Barbour in the pwsafe platform room, relayed and narrowed by Fred Brooks, 2026-10-08.

Out of scope: changing `PRODUCT_NAME`, the executable name or the bundle ID; signing or notarisation (the dmg stays ad hoc signed, so macOS still asks before first opening it). Residual risk: our bundle ID stays `org.pwsafe.pwsafe` (from the Xcode project's `org.pwsafe.${PRODUCT_NAME:rfc1034identifier}`). Only if Huvisoft's app has that same ID might macOS treat the two apps as one for preferences and "Open With"; Robert can check with `defaults read "/Applications/<Huvisoft app>.app/Contents/Info" CFBundleIdentifier`.

Exclusions: fork-only, never part of an upstream pull request; no file under `src/` changes; no secrets; no `*.psafe3` file is committed.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given a fork CI run of `.github/workflows/macos-latest.yml` on rjbarbour/pwsafe, when QA mounts the dmg artefact, then it contains `PasswordSafe-wx.app` and no `pwsafe.app`, and the `Yubico` folder is present as before
- [ ] #2 Given that dmg, when Robert Barbour copies `PasswordSafe-wx.app` into `/Applications` beside Huvisoft's `pwsafe.app` and allows the ad hoc signed app on first open, then it opens a test safe, and Huvisoft's `pwsafe.app` is still present
- [ ] #3 Given `install/macosx/Makefile` on fork `master`, when `make` runs in `install/macosx` without `DMG_APP` set, then the staged app and the dmg's app icon are named `pwsafe.app`
- [ ] #4 Given the change, when QA reads its diff, then it touches only `install/macosx/Makefile` and the fork's dmg workflow; `RESOURCES` and the `.xcent` path still name `pwsafe.app`; and `PRODUCT_NAME`, the executable name and the bundle ID are unchanged
- [ ] #5 Given the same fork CI run, when QA reads its log, then the coretest step passes
- [ ] #6 Given the pull request for this task, when it is merged, then Fred Brooks and Dennis Ritchie have each recorded a code review, and every automated-check finding on it (CI, CodeQL, the fork quality gate or any other check) has been addressed by disabling or tuning the rule, suppressing it in code within this task's limits, mitigating or fixing it, or recording the residual risk in `backlog/docs/raid-log.md`, and the pull request or task notes say which for each finding
<!-- AC:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 13:43
---
DoR check 2026-10-08 (Fred Brooks): fail. AC #1 requires the EFF word-list notice in the dmg "as before", but master does not ship it (the install/macosx/Makefile DOCS list has only the Yubico notice; the EFF notice is on PR #2 / PWS-02). Drop the EFF notice from AC #1, or depend on PWS-02 and say the notice is present only after that merge.
---

author: @fred-brooks
created: 2026-10-08 13:43
---
DoR re-check 2026-10-08 (Fred Brooks): pass. EFF notice removed from AC 1. Held in To Do while Ready is at its limit of 3.
---
<!-- COMMENTS:END -->
