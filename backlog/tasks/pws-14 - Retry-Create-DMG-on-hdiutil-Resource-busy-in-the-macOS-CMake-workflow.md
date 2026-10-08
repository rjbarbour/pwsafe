---
id: PWS-14
title: Retry Create DMG on hdiutil Resource busy in the macOS CMake workflow
status: To Do
assignee:
  - '@grace-hopper'
created_date: '2026-10-08 13:11'
updated_date: '2026-10-08 15:58'
labels: []
dependencies: []
modified_files:
  - .github/workflows/macos-cmake-latest.yml
type: chore
ordinal: 14000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The "Create DMG" step in `.github/workflows/macos-cmake-latest.yml` (`cpack -G DragNDrop`) sometimes fails with `hdiutil: Resource busy`. The step retries that command up to 3 times on that failure, so a runner flake no longer fails the job. A failure with any other error still fails the job at once.

Requested by Grace Hopper, relayed by Fred Brooks, 2026-10-08.

Exclusions: fork-only, never part of an upstream pull request; no other step or workflow changes; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the change, when QA reads the "Create DMG" step of `.github/workflows/macos-cmake-latest.yml`, then it retries `cpack -G DragNDrop` up to 3 times, only when the output contains `hdiutil: Resource busy`, and no other step changes
- [ ] #2 Given a run where the first attempt fails with `hdiutil: Resource busy` and a later attempt succeeds, when the job finishes, then it passes and the log shows the retry; the task notes give that run's URL, or say a simulated failure on a throwaway branch was used instead
- [ ] #3 Given a run where the step fails with any other error, when the job finishes, then it fails without retrying
- [ ] #4 Given the pull request for this task, when it is merged, then Fred Brooks and Dennis Ritchie have each recorded a code review, and every automated-check finding on it (CI, CodeQL, the fork quality gate or any other check) has been addressed by disabling or tuning the rule, suppressing it in code within this task's limits, mitigating or fixing it, or recording the residual risk in `backlog/docs/raid-log.md`, and the pull request or task notes say which for each finding
<!-- AC:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 13:43
---
DoR check 2026-10-08 (Fred Brooks): fail. Name the retry count in the description and AC #1 (for example 3 attempts), rather than leaving it to be stated later in the task notes.
---

author: @fred-brooks
created: 2026-10-08 13:43
---
DoR re-check 2026-10-08 (Fred Brooks): pass. Retry count named. Held in To Do while Ready is at its limit of 3.
---
<!-- COMMENTS:END -->
