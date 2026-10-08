---
id: decision-02
title: Fork master is the integration branch and holds the fork-only tracker
date: '2026-10-08 12:42'
status: accepted
---
## Context

PWS-01. Robert Barbour adopted the Backlog.md CLI as the sole work tracker for the rjbarbour/pwsafe fork. The fork tracks upstream pwsafe/pwsafe and contributes features back to it, so feature work must stay upstream-shaped. The tracker (`backlog/`, `backlog.config.yml`) and the fork's agent routing (`AGENTS.md`) have no place upstream. They need a home in the fork that every agent reads from, without leaking into an upstream pull request. Owner decision: Robert Barbour, 2026-10-08 12:42 BST, option A, recorded in PWS-01's notes. This record restates that decision; it does not change it.

## Decision

1. **Fork `master` is the integration branch.** It holds `backlog/`, `backlog.config.yml` and `AGENTS.md`, and it receives upstream changes by merge.
2. **These files are fork-only.** They never appear in a pull request to pwsafe/pwsafe.
3. **Upstream-bound work comes from feature branches based on upstream master**, not on fork `master`. Such a branch skips the Tracked Work SOP GT-03A rebase onto fork `master` and is synchronised against upstream master instead; the task records that.
4. **Each pull request's file list is checked before it is opened or merged**, and any `backlog/`, `backlog.config.yml` or `AGENTS.md` path in an upstream-bound diff blocks it. PR #2's file list was checked this way (PWS-01 evidence).
5. **Tracker-only changes go straight to fork `master`**, one task ID per commit, with no feature branch.

## Alternatives considered

- **B: a separate fork tracker branch**, keeping fork `master` a pure mirror of upstream. Rejected: every agent would read the tracker from a non-default branch, and tracker commits would need their own integration path.
- **C: a separate tracker repository.** Rejected: it splits the tracker from the code it tracks, so task IDs, branches and pull requests would no longer live in one place.

## Consequences

- Fork `master` permanently differs from upstream master. Upstream changes arrive by merge, never by fast-forward.
- A feature branch based on upstream master does not contain `AGENTS.md`, so tools that read it from the branch under review may not see the fork's rules (RAID R-08, PWS-11).
- Keeping fork-only files out of upstream pull requests depends on the file-list check in point 4. Today that check is manual; a missed check would put fork-only files in front of upstream reviewers.
- Fork-only platform files (`.github/workflows/fork-*.yml`, `tools/quality/`) also live only on fork `master` and are kept out of upstream pull requests by the same file-list check.
- Fork risks are logged in `backlog/docs/raid-log.md`.

## What would reverse this decision

- Upstream adopting Backlog.md or an equivalent tracker in its own repository.
- The fork stopping upstream contributions, so a pure upstream mirror no longer matters, or needing one, so `master` must fast-forward to upstream.
- Repeated leaks of fork-only files into upstream-bound branches despite the file-list check, which would favour option B or C.
- Robert Barbour deciding otherwise. A reversal supersedes this record; it is not edited.
