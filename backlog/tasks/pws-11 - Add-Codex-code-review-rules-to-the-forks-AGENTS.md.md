---
id: PWS-11
title: Add Codex code review rules to the fork's AGENTS.md
status: Shaping
assignee: []
created_date: '2026-10-08 12:59'
updated_date: '2026-10-08 13:06'
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
The fork's root `AGENTS.md` gains a `## Code Review Rules` section, so the Codex GitHub reviewer checks pull requests in rjbarbour/pwsafe against a few architecture and scope rules that reviewers would otherwise have to explain each time. Barbara Liskov drafts the rules. Start with two or three short rules, each saying what to flag, why it matters, and the safe path or exception:

- No file under `src/core` or `src/os` includes a header under `src/ui`, and no new `wx/` include is added under `src/core` or `src/os` (exceptions as in the PWS-04 decision record).
- Flag refactors or file changes that the pull request's PWS task does not need.
- Flag new cryptographic or random-number sources that bypass Password Safe's existing facilities, and generated secrets written to logs or to the clipboard. The clipboard rule names Password Safe's existing user-initiated copy as the expected path, so Codex does not flag it. The wording stays general.

Known risk: pull request branches are based on upstream master, so they do not contain `AGENTS.md`. Whether Codex applies the rules to such a branch is what the representative pull request has to show.

Requested by Robert Barbour in the pwsafe platform room (can the Codex reviewer be tuned for architecture checks?), relayed by Fred Brooks, 2026-10-08. Reference: Codex GitHub integration, "Customize what Codex reviews".

Exclusions: fork `master` only, never part of an upstream pull request; root `AGENTS.md` only, with no nested `AGENTS.md` under `src/`; no `@codex security review`; no mechanical lint, formatting or include-count rules, which stay in CI (PWS-07); no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the change is on fork `master`, when QA reads the root `AGENTS.md`, then it has one `## Code Review Rules` section with two or three rules drafted by Barbara Liskov, each stating what to flag, why it matters, and the safe path or exception
- [ ] #2 Given that section, when QA reads it, then it contains a rule that `src/core` and `src/os` never include a header under `src/ui` and add no new `wx/` include, a rule to flag refactors or file changes the pull request's PWS task does not need, and a rule to flag new cryptographic or random-number sources that bypass Password Safe's existing facilities and generated secrets written to logs or the clipboard, with Password Safe's existing user-initiated copy named as the expected path
- [ ] #3 Given that section, when QA reads it, then it contains no formatting, lint or other mechanical check, and its random-source rule is written in general terms, naming no specific platform or implementation detail
- [ ] #4 Given the change, when QA runs `git ls-files '*AGENTS.md'` on fork `master`, then the root `AGENTS.md` is the only match, and the commit changes no file other than `AGENTS.md` and the PWS task file
- [ ] #5 Given Robert Barbour has agreed to an `@codex review` comment being posted under his name, and a representative pull request to fork `master` from a branch based on upstream master that breaks at least one rule, when Codex reviews it, then Grace Hopper records in the task notes the pull request URL, the review URL, and whether Codex flagged the break with reference to the rule
- [ ] #6 Given Codex does not apply the rules on that pull request, when Grace Hopper records the result, then the task notes say so and the task goes back to Fred Brooks for a decision rather than adding a nested or branch copy of `AGENTS.md`
- [ ] #7 Given the representative pull request, when the check is finished, then it is closed unmerged and its branch deleted
<!-- AC:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 13:06
---
DoR re-check 2026-10-08 (Fred Brooks): fail. hold the crypto/randomness/clipboard rule until owner decision; start with layering and scope only.
---
<!-- COMMENTS:END -->
