---
id: PWS-10
title: >-
  Seed pwsafe's random generator from the operating system's random source on
  every platform
status: To Do
assignee: []
created_date: '2026-10-08 12:50'
labels: []
dependencies: []
type: enhancement
ordinal: 10000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A general Password Safe improvement, separate from Diceware (Robert Barbour ruling, 2026-10-08). One central random source, which Generate, Passphrase and every other existing caller already share, is seeded from the best operating-system random source on macOS and Linux (Intel, AMD and Apple silicon), and on other platforms where that is cheap. It is a likely upstream contribution, so its branch is based on upstream master and contains no fork-only files. It does not block PWS-02. Design: a decision record by Barbara Liskov.

Exclusions: no new cryptographic algorithm; no file-format change; existing caller interfaces unchanged; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given macOS or Linux, when the central random generator initialises, then it is seeded from the operating-system random source that the decision record names for that platform
- [ ] #2 Given the operating-system random source is unavailable or reports an error, when the generator initialises, then nothing that depends on the generator goes ahead with any other seed, and the failure is reported as the decision record specifies
- [ ] #3 Given the change, when Generate, Passphrase and the other existing callers are built, then their call sites and interfaces are unchanged, and coretest passes on Linux and on macOS CI
- [ ] #4 Given the change, when `src/` is searched for operating-system random-source calls, then they appear only in the central random source's per-platform code
- [ ] #5 Given coretest, when it runs, then it includes a case that injects an operating-system source and shows the seed is taken from it, and a case where the injected source fails and the generator fails closed
- [ ] #6 Given the pull request, when QA inspects it, then it is based on upstream master and its diff contains none of the fork-only files (`AGENTS.md`, `backlog/`, `backlog.config.yml`)
<!-- AC:END -->
