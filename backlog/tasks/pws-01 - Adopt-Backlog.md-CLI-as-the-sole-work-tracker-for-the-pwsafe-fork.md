---
id: PWS-01
title: Adopt Backlog.md CLI as the sole work tracker for the pwsafe fork
status: In Progress
assignee:
  - '@fred-brooks'
created_date: '2026-10-08 11:40'
updated_date: '2026-10-08 13:40'
labels: []
dependencies: []
references:
  - 'https://github.com/rjbarbour/pwsafe'
type: chore
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Owner decision (Robert Barbour, 2026-10-08): adopt the MrLesk Backlog.md CLI as the sole delivery work tracker for the rjbarbour/pwsafe fork, under SOP: Adopt Backlog.md CLI in an Existing or New Project v1.4.

The fork tracks upstream pwsafe/pwsafe. Feature work must stay upstream-shaped, so backlog/, backlog.config.yml and any AGENTS.md routing must never appear in an upstream-bound feature branch diff.

Scope: initialise Backlog.md (project pwsafe, prefix PWS, backlog/ directory, root backlog.config.yml, CLI integration, no agent-instruction overwrite); record the Diceware Milestone 1 work as a task; declare the integration branch and routing.
Exclusions: no legacy PROJECT.md, PLAN.md, ROADMAP.md or handwritten backlog; no change to upstream source; no README edit that would diverge from upstream without an owner decision; no credentials in any file.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Fork `master` is declared the integration branch holding the tracker (owner decision: Robert Barbour, 2026-10-08), and no upstream-bound feature branch diff contains backlog/, backlog.config.yml or AGENTS.md
- [x] #2 `backlog/` and `backlog.config.yml` are version-controlled on fork `master` in their own commit
- [x] #3 AGENTS.md on fork `master` names Backlog.md as the sole work tracker, the PWS-NN identifier format, the installed `backlog instructions` guides, the one-task-ID-per-branch/commit/PR rule and the fork-only file rule
- [x] #4 `backlog task list --json` lists the adoption task and the Diceware Milestone 1 task with the intended IDs and statuses
- [x] #5 The adoption commit is integrated on the fork through one reviewed pull request, with GitHub authentication done without exposing a secret
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Decision (owner Robert Barbour, 2026-10-08 12:42 BST): option A. Fork `master` is the integration branch and holds the tracker (backlog/, backlog.config.yml, AGENTS.md). These files are fork-only and never go into an upstream pwsafe/pwsafe pull request. Upstream contributions come from feature branches based on upstream master; those branches skip the Tracked Work SOP GT-03A rebase onto fork `master` and synchronise against upstream master instead. Consequence: fork `master` permanently differs from upstream, so upstream changes arrive by merge, not fast-forward.
Rejected: B (separate fork tracker branch, keeping master a pure upstream mirror) and C (separate tracker repository).
2026-10-08: initialised Backlog.md CLI 1.50.1 (project pwsafe, prefix PWS, zero-padded 2, backlog/ directory, root config, CLI integration, no agent-instruction files). AGENTS.md written by hand, minimal and fork-specific. No README edit, to keep upstream files unchanged.
Capability gap: `backlog config set` cannot set statuses, so Shaping, Ready and Review from the SOP are not configured; defaults are To Do, In Progress, Done (Draft is native).
State: one local commit on fork `master`; local-only, not pushed.
Blocker for push and pull request: GitHub command line on the box is not signed in.
Remaining: GitHub sign-in under GH-01; push an adoption branch and open one reviewed pull request into fork `master`; after merge, synchronise local `master` and record evidence.

Evidence 2026-10-08 (Margaret Hamilton): PR #1 https://github.com/rjbarbour/pwsafe/pull/1 merged by rjbarbour at 12:54 BST, merge commit f24fd88. Adoption commit 48fbf4f adds AGENTS.md, backlog.config.yml and backlog/ only, no upstream source (AGENTS.md is in the same commit). PR #2 file list checked: no backlog/, backlog.config.yml or AGENTS.md. backlog task list shows PWS-01 and PWS-02. GitHub access used a repo-scoped token passed as GH_TOKEN; no secret written to any file. Accepted by Fred Brooks, 2026-10-08.

CI evidence 2026-10-08 (checked via the GitHub Actions API by Fred Brooks): both macOS workflows ran on fork `master` at merge commit f24fd88, event workflow_dispatch, conclusion success.
- Build pwsafe with CMake on macOS (.github/workflows/macos-cmake-latest.yml), run 37773748187, 12:59 to 13:19 BST: https://github.com/rjbarbour/pwsafe/actions/runs/37773748187
- mac-pwsafe (.github/workflows/macos-latest.yml), run 37773751736, 12:59 to 13:15 BST: https://github.com/rjbarbour/pwsafe/actions/runs/37773751736

Status correction 2026-10-08 (Fred Brooks): set back from Done to In Progress. The board rule for Done needs coordinator acceptance, the merged PR, and QA checks and CI recorded in the task; Edsger Dijkstra's QA check for PWS-01 is not recorded in this task or on PR #1. QA evidence pending; moves to Review when the Review status lands (PR #4).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Adopted Backlog.md CLI 1.50.1 as the fork's sole work tracker on fork master (fork-only AGENTS.md, backlog/, backlog.config.yml). Integrated through PR #1, reviewed and merged by Robert Barbour on 2026-10-08. Verified from the merged PR, the adoption commit's file list, PR #2's file list and backlog task list.
<!-- SECTION:FINAL_SUMMARY:END -->
