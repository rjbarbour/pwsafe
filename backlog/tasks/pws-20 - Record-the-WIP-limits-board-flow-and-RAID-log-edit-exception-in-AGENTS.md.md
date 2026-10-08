---
id: PWS-20
title: 'Record the WIP limits, board flow and RAID-log edit exception in AGENTS.md'
status: To Do
assignee: []
created_date: '2026-10-08 16:13'
updated_date: '2026-10-08 16:13'
labels:
  - tracker
dependencies: []
modified_files:
  - AGENTS.md
type: chore
ordinal: 20000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The root `AGENTS.md` states the board rules the team already works to but which are not written down: the WIP limits, the board flow and who moves tasks, and the one exception to editing docs only through the Backlog.md CLI. From Dennis Ritchie's retrospective review of PR #1 (finding 2, recorded on PWS-01 in 68d429b93) and Fred Brooks's follow-up (ef7ed8628 on PWS-01).

Kept separate from PWS-11 so that PWS-11 stays limited to code-review scope (b92316333). PWS-11 carries the fork-only file list change.

Exclusions: the only file the pull request changes is the root `AGENTS.md`; fork `master` only, never part of an upstream pull request; no change to `backlog.config.yml` or the RAID log; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the pull request head, when QA reads the root `AGENTS.md`, then it states the WIP limits of at most one task In Progress and at most three Ready, and that Fred Brooks enforces them by hand because Backlog.md has no WIP-limit setting
- [ ] #2 Given the pull request head, when QA reads the root `AGENTS.md`, then it states the board flow To Do, Shaping, Ready, In Progress, Review, Done, in that order, and that Fred Brooks owns every status after To Do
- [ ] #3 Given the pull request head, when QA reads the root `AGENTS.md`, then it records the one exception to changing docs only through the Backlog.md CLI: `backlog/docs/raid-log.md` is edited by hand to keep its path, because `backlog doc update` renames it to `doc-01 - RAID-log.md`
- [ ] #4 Given the pull request diff, when QA inspects it, then it changes only the root `AGENTS.md`
- [ ] #5 Given the pull request for this task, when it is merged, then Fred Brooks and Dennis Ritchie have each recorded a code review, and every automated-check finding on it (CI, CodeQL, the fork quality gate or any other check) has been addressed by disabling or tuning the rule, suppressing it in code within this task's limits, mitigating or fixing it, or recording the residual risk in `backlog/docs/raid-log.md`, and the pull request or task notes say which for each finding
<!-- AC:END -->
