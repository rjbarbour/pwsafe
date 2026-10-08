# Agent routing for the rjbarbour/pwsafe fork

This file is fork-only. It is not part of upstream Password Safe (pwsafe/pwsafe).

## Fork-only files and upstream contributions

- `AGENTS.md`, `backlog/` and `backlog.config.yml` exist only on this fork's `master`.
  They must never appear in a pull request to upstream pwsafe/pwsafe.
- Fork `master` is the integration branch. It holds the work tracker and receives
  upstream changes by merge.
- Upstream-bound feature branches are based on upstream master, not on fork `master`.
  They skip the Tracked Work SOP GT-03A rebase onto fork `master`; synchronise them
  against upstream master instead, and record that in the task.
- Before opening any pull request, check that its diff contains none of the fork-only files.

## Work tracker

- [Backlog.md](https://github.com/MrLesk/Backlog.md) CLI is the sole live delivery work
  tracker. `backlog/` and `backlog.config.yml` are its data store.
- Task IDs use the form `PWS-NN`. One task ID binds the branch, commits, pull request and
  evidence for one piece of substantive work. One branch and one pull request per task.
- Default branch form: `codex/PWS-NN-short-goal`.
- Begin task work with `backlog instructions overview`.
- Before creating, executing or finalising a task, read the matching guide:
  `backlog instructions task-creation`, `backlog instructions task-execution`,
  `backlog instructions task-finalization`.
- Change task, draft, decision, document and milestone records only through the
  `backlog` CLI. Do not edit generated `backlog/` files by hand.
- Serve the board (`backlog board`, `backlog browser`) only from a clean checkout of fork
  `master`, never from a task worktree.
- Terminology: task, status, Definition of Ready, acceptance criteria, Definition of Done,
  implementation plan, implementation notes, final summary, decision, milestone, document,
  board and browser.
- Do not create `PROJECT.md`, `PLAN.md`, `ROADMAP.md`, `ITEM-BACKLOG.md` or a handwritten
  backlog file. None existed before adoption.

## GitHub and secrets

- Authenticate GitHub operations under the owner's GH-01 credential policy. Do not use
  `gh auth login`, `gh auth logout` or `gh auth switch` as a fallback.
- Never commit secrets, tokens, credential labels, Keychain paths or password database
  files (for example `*.psafe3` test databases) to this repository.
