---
id: PWS-20
title: 'Record the WIP limits, board flow and hand-edited docs exception in AGENTS.md'
status: To Do
assignee: []
created_date: '2026-10-08 16:13'
updated_date: '2026-10-08 16:38'
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
- [ ] #2 Given the pull request head, when QA reads the root `AGENTS.md`, then it states the board flow To Do, Shaping, Ready, In Progress, Review, Done, in that order, and that Fred Brooks moves tasks between statuses after To Do, Margaret Hamilton shapes tasks in Shaping, and any SDLC role may ask Fred Brooks to return a task to Shaping under Definition of Ready triggers RT-01 to RT-04
- [ ] #3 Given the pull request head, when QA reads the root `AGENTS.md`, then it records the one exception to changing docs only through the Backlog.md CLI: `backlog/docs/raid-log.md` and `backlog/docs/test-strategy.md` are edited by hand to keep their paths, because `backlog doc update` renames them (it renames the RAID log to `doc-01 - RAID-log.md`)
- [ ] #4 Given the pull request diff, when QA inspects it, then it changes only the root `AGENTS.md`
- [ ] #5 Given the pull request for this task, when it is merged, then Fred Brooks and Dennis Ritchie have each recorded a code review, and every automated-check finding on it (CI, CodeQL, the fork quality gate or any other check) has been addressed by disabling or tuning the rule, suppressing it in code within this task's limits, mitigating or fixing it, or recording the residual risk in `backlog/docs/raid-log.md`, and the pull request or task notes say which for each finding
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
DoR check 2026-10-08 (Fred Brooks, Definition of Ready v1.3): pass, with one proposed wording change before Ready; stays in To Do while Ready holds 3. RD-01: the outcome is explicit (the board rules agents work to are written down), for every agent and Robert. RD-02: scope and exclusions are explicit (root AGENTS.md only; no config or RAID log change). RD-03: AC 1-5 are concrete and checkable by reading AGENTS.md; AC 1's reason holds, because Backlog.md 1.50.1 has no WIP-limit setting. RD-04: sources are Dennis Ritchie's review (68d429b93) and Fred Brooks's (ef7ed8628). Rebase dependency: PWS-11 also edits the root AGENTS.md, so whichever merges second rebases on the other and keeps both changes. RD-05: low risk, reversible, Build commitment (project default). RD-06: one file; QA by Edsger Dijkstra; two code reviews (AC 5). RD-07: project defaults. Proposed for Margaret: AC 2's 'Fred Brooks owns every status after To Do' would contradict Definition of Ready v1.3, under which SDLC may return a task to Shaping. Reword it to: 'Fred Brooks moves tasks between statuses after To Do; Margaret Hamilton shapes tasks in Shaping; an SDLC role may ask Fred Brooks to return a task to Shaping under DoR v1.3 triggers RT-01 to RT-04.'

DoR re-check 2026-10-08 (Fred Brooks) after the AC 2 edit (70f5aee14): pass holds, and the proposed wording condition is now met. AC 2 now says who moves, shapes and can return tasks, consistent with Definition of Ready v1.3 RT-01 to RT-04. Stays in To Do while Ready holds 3.

DoR re-check 2026-10-08 (Fred Brooks, Definition of Ready v1.3) at e03ff6890: the pass stands. Under c07de4ff9, AC 3's hand-edit exception covers both backlog/docs/raid-log.md and backlog/docs/test-strategy.md. That matches PWS-22, which keeps the test-strategy.md path. The title now reads 'hand-edited docs exception' (e03ff6890), which resolves the title point. Non-blocking: AC 3 and the description still say 'the one exception' for an exception that now covers two files; 'the exception' would read better. Status unchanged (To Do).
<!-- SECTION:NOTES:END -->
