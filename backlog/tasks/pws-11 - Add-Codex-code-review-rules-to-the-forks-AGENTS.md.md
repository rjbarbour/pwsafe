---
id: PWS-11
title: Add Codex code review rules to the fork's AGENTS.md
status: Shaping
assignee:
  - '@barbara-liskov'
created_date: '2026-10-08 12:59'
updated_date: '2026-10-08 16:15'
labels:
  - quality
dependencies: []
references:
  - 'https://developers.openai.com/codex/integrations/github'
modified_files:
  - AGENTS.md
type: chore
ordinal: 11000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The fork's root `AGENTS.md` gains a `## Code Review Rules` section, so the Codex GitHub reviewer checks pull requests in rjbarbour/pwsafe against a few architecture and scope rules that reviewers would otherwise have to explain each time. Barbara Liskov drafts the rules. Start with two short rules, each saying what to flag, why it matters, and the safe path or exception:

- No file under `src/core` or `src/os` includes a header under `src/ui`, and no new `wx/` include is added under `src/core` or `src/os` (exceptions as in the PWS-04 decision record).
- Flag refactors or file changes that the pull request's PWS task does not need.

Further rules are added later as separate changes, once agreed.

Known risk: pull request branches are based on upstream master, so they do not contain `AGENTS.md`. Whether Codex applies the rules to such a branch is what the representative pull request has to show.

Requested by Robert Barbour in the pwsafe platform room (can the Codex reviewer be tuned for architecture checks?), relayed by Fred Brooks, 2026-10-08. Reference: Codex GitHub integration, "Customize what Codex reviews".

The same change also completes the fork-only file list in `AGENTS.md`, from Dennis Ritchie's retrospective review of PR #1 (finding 3, recorded on PWS-01 in 68d429b93): alongside `backlog/`, `backlog.config.yml` and `AGENTS.md`, it names `.github/workflows/fork-*.yml` and `tools/quality/`, as decision-02 does, so upstream-bound pull requests must not touch those paths either. This sits outside the `## Code Review Rules` section. The WIP limits and board flow from the same review are a separate task, so that this task stays limited to code-review scope.

Exclusions: fork `master` only, never part of an upstream pull request; root `AGENTS.md` only, with no nested `AGENTS.md` under `src/`; no `@codex security review`; no mechanical lint, formatting or include-count rules, which stay in CI (PWS-07); no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the change is on fork `master`, when QA reads the root `AGENTS.md`, then it has one `## Code Review Rules` section with the rules drafted by Barbara Liskov, each stating what to flag, why it matters, and the safe path or exception
- [ ] #2 Given that section, when QA reads it, then it contains exactly two rules: that `src/core` and `src/os` never include a header under `src/ui` and add no new `wx/` include, and that refactors or file changes the pull request's PWS task does not need are flagged
- [ ] #3 Given that section, when QA reads it, then it contains no formatting, lint or other mechanical check
- [ ] #4 Given the change, when QA runs `git ls-files '*AGENTS.md'` on fork `master`, then the root `AGENTS.md` is the only match, and the commit changes no file other than `AGENTS.md` and the PWS task file
- [ ] #5 Given Robert Barbour has agreed to an `@codex review` comment being posted under his name, and a representative pull request to fork `master` from a branch based on upstream master that breaks at least one rule, when Codex reviews it, then Grace Hopper records in the task notes the pull request URL, the review URL, and whether Codex flagged the break with reference to the rule
- [ ] #6 Given Codex does not apply the rules on that pull request, when Grace Hopper records the result, then the task notes say so and the task goes back to Fred Brooks for a decision rather than adding a nested or branch copy of `AGENTS.md`
- [ ] #7 Given the representative pull request, when the check is finished, then it is closed unmerged and its branch deleted
- [ ] #8 Given the pull request head, when QA reads the fork-only file list in the root `AGENTS.md`, then, outside the `## Code Review Rules` section, it names `backlog/`, `backlog.config.yml`, `AGENTS.md`, `.github/workflows/fork-*.yml` and `tools/quality/`, matching decision-02, and says that no upstream-bound pull request may touch any of them
- [ ] #9 Given the pull request for this task, when it is merged, then Fred Brooks and Dennis Ritchie have each recorded a code review, and every automated-check finding on it (CI, CodeQL, the fork quality gate or any other check) has been addressed by disabling or tuning the rule, suppressing it in code within this task's limits, mitigating or fixing it, or recording the residual risk in `backlog/docs/raid-log.md`, and the pull request or task notes say which for each finding
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
DoR re-check 2026-10-08 (Fred Brooks, Definition of Ready v1.3) after AC 8 (56493b180): pass; stays in Shaping (no status change while Ready holds 3). The earlier fail (13:06) is closed: the rules are now limited to layering and scope. RD-01: the outcome is explicit (Codex flags layering and scope breaks; the fork-only list is complete), for reviewers and Robert. RD-02: scope and exclusions are explicit, and AC 6 sends a failed Codex trial back to Fred Brooks. RD-03: AC 1-9 are concrete. AC 8 matches decision-02, which already names .github/workflows/fork-*.yml and tools/quality/. RD-04: the known risk is RAID R-08, and decision-02 is the source. Rebase dependency: PWS-20 also edits the root AGENTS.md, so whichever merges second rebases on the other and keeps both changes. RD-05: low risk, reversible, Build commitment (project default). RD-06: AGENTS.md only; Barbara Liskov drafts, Grace Hopper runs the Codex trial, QA by Edsger Dijkstra, two code reviews (AC 9). RD-07: Robert's agreement to an @codex review comment posted under his name is reserved to him and must be recorded before AC 5 starts. Proposed tidy for Margaret, non-blocking: AC 4 'the commit changes no file other than AGENTS.md and the PWS task file' becomes 'the pull request changes only the root AGENTS.md; task notes go to fork master as tracker-only commits (decision-02, point 5)', to match PWS-20 AC 4.
<!-- SECTION:NOTES:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 13:06
---
DoR re-check 2026-10-08 (Fred Brooks): fail. hold the crypto/randomness/clipboard rule until owner decision; start with layering and scope only.
---
<!-- COMMENTS:END -->
