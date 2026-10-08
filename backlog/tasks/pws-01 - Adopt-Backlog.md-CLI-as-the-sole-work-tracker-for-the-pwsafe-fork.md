---
id: PWS-01
title: Adopt Backlog.md CLI as the sole work tracker for the pwsafe fork
status: Done
assignee:
  - '@fred-brooks'
created_date: '2026-10-08 11:40'
updated_date: '2026-10-08 15:55'
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
Superseded 2026-10-08: the earlier local-only state, the GitHub sign-in blocker and the remaining-steps list no longer apply. The adoption branch was pushed and integrated through PR #1 (merge f24fd88); see the evidence below.

Evidence 2026-10-08 (Margaret Hamilton): PR #1 https://github.com/rjbarbour/pwsafe/pull/1 merged by rjbarbour at 12:54 BST, merge commit f24fd88. Adoption commit 48fbf4f adds AGENTS.md, backlog.config.yml and backlog/ only, no upstream source (AGENTS.md is in the same commit). PR #2 file list checked: no backlog/, backlog.config.yml or AGENTS.md. backlog task list shows PWS-01 and PWS-02. GitHub access used a repo-scoped token passed as GH_TOKEN; no secret written to any file. Accepted by Fred Brooks, 2026-10-08.

CI evidence 2026-10-08 (checked via the GitHub Actions API by Fred Brooks): both macOS workflows ran on fork `master` at merge commit f24fd88, event workflow_dispatch, conclusion success.
- Build pwsafe with CMake on macOS (.github/workflows/macos-cmake-latest.yml), run 37773748187, 12:59 to 13:19 BST: https://github.com/rjbarbour/pwsafe/actions/runs/37773748187
- mac-pwsafe (.github/workflows/macos-latest.yml), run 37773751736, 12:59 to 13:15 BST: https://github.com/rjbarbour/pwsafe/actions/runs/37773751736

QA evidence 2026-10-08 (Edsger Dijkstra), checked against fork `master` f24fd88: all 5 acceptance criteria pass.
- AC1 fork-only: diff 3996b15..f24fd88 adds only AGENTS.md, backlog.config.yml and the two task files. Upstream-bound branch codex/PWS-02-diceware-passphrase (db9dab1) has merge-base 3996b15 and contains no backlog/, backlog.config.yml or AGENTS.md. No PRs by rjbarbour on pwsafe/pwsafe.
- AC2: 48fbf4f (parent 3996b15) is a single tracker-only commit with the four files (AGENTS.md included; no source files).
- AC3: AGENTS.md names Backlog.md as the sole tracker, PWS-NN IDs, the backlog instructions guides, the one-task-one-branch-one-PR rule and the fork-only rule.
- AC4: Backlog.md 1.50.1 in a clean worktree of f24fd88: `backlog task list` (json and plain), `backlog board export` and `backlog browser` (GET / returns 200; /api/tasks lists PWS-01 and PWS-02) all work.
- Secrets: no *.psafe3 in the tree; a secret-pattern search of added lines found only AGENTS.md's policy text.
- AC5 caveat: PR #1 has no GitHub approving review. Review consisted of the owner's merge by rjbarbour at 12:54 BST (merge f24fd88) plus the Codex bot's automated review of 48fbf4f, which had no findings.

Status 2026-10-08 (Fred Brooks): QA and CI are now recorded in this task. With acceptance by Fred Brooks and PR #1 merged, PWS-01 meets the board rule for Done.

DoD v1.1 check 2026-10-08 (Fred Brooks): DD-01 pass for AC 1-4 (Edsger Dijkstra's QA of f24fd88); AC 5 is ticked, but its 'reviewed pull request' rests on the owner's merge and the Codex bot's automated review, so it stands only with the DD-03 waiver below; DD-02 pass: PR #1 merged as f24fd88 on fork master, and macOS runs 37773748187 and 37773751736 succeeded on f24fd88; DD-03 gap: independent QA by Edsger Dijkstra, but no human technical review of PR #1 and no explicit waiver (RAID I-02); DD-04 gaps: (a) the owner decision on the integration branch (option A, with options B and C rejected and fork master permanently differing from upstream) is recorded only in these notes, not as a Backlog.md decision record; (b) the 'Capability gap' line saying Shaping, Ready and Review are not configured is stale, because 8f7c8c4 added them to backlog.config.yml; DD-05 partial: the operational constraint (upstream changes arrive by merge, not fast-forward) is recorded, but no residual risk or next gate is stated; overlay DO-05 (documentation and configuration only, so no application build is needed; authority is Robert Barbour's 2026-10-08 decision, and QA checked the rendered board). Result: gaps: DD-03 waiver or retrospective review (I-02); DD-04 decision record and stale status line; DD-05 next gate.
Proposed wording, not yet agreed: DD-03 'Waiver (Robert Barbour, <date>): PR #1 is tracker-only (AGENTS.md, backlog.config.yml, backlog/); the owner's merge, the Codex automated review with no findings and Edsger Dijkstra's QA of f24fd88 stand in place of a technical review.' Otherwise Fred Brooks and Dennis Ritchie review f24fd88 retrospectively. DD-04 (a): Barbara Liskov records decision-02 'Fork master is the integration branch and holds the fork-only tracker' from the 12:42 BST owner decision, or Robert rules that these notes are the record. DD-04 (b): 'Superseded 2026-10-08: Shaping, Ready and Review were added to backlog.config.yml in 8f7c8c4.' DD-05: 'Next gate: none for adoption. Fork-only files are kept out of upstream pull requests by checking each pull request's file list, as on PR #2. Fork risks are logged in backlog/docs/raid-log.md.'
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Adopted Backlog.md CLI 1.50.1 as the fork's sole work tracker on fork master (fork-only AGENTS.md, backlog/, backlog.config.yml). Integrated through PR #1, merged by Robert Barbour on 2026-10-08 (merge f24fd88); PR #1 had no GitHub approving review, only the owner's merge and the Codex bot's automated review of 48fbf4f with no findings. CI: macOS runs 37773748187 and 37773751736 on f24fd88 succeeded. QA: Edsger Dijkstra checked all 5 acceptance criteria against f24fd88 and they pass.
<!-- SECTION:FINAL_SUMMARY:END -->
