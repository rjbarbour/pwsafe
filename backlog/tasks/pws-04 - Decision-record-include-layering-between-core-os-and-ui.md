---
id: PWS-04
title: 'Decision record: include layering between core, os and ui'
status: To Do
assignee:
  - '@barbara-liskov'
created_date: '2026-10-08 12:49'
labels:
  - quality
dependencies: []
type: task
ordinal: 4000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A Backlog.md decision record fixes which include edges between `src/core`, `src/os` and `src/ui` are allowed, so that the layering check in the fork quality gate enforces an agreed design rule rather than a script default. It comes before the layering script in `tools/quality/layering.py` and its edge list `tools/quality/layering_baseline.txt` (39 edges, taken on fork master f24fd88) are adopted. The deliverable is the decision record; no source file changes.

Code-quality stack agreed in the pwsafe platform room; requested by Fred Brooks, 2026-10-08.

Exclusions: the upstream workflows (`cmake-build.yml`, `codeql-analysis.yml`, `macos-latest.yml`, `macos-cmake-latest.yml`) stay untouched; fork-only, never part of an upstream pull request; any gate covers new or changed code only; no SonarQube Cloud or CodeRabbit; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the decision record created with `backlog decision create`, when QA reads it, then it states that no file under `src/core` or `src/os` includes a header under `src/ui`
- [ ] #2 Given the decision record, when QA reads it, then it states that the existing include cycle between `src/core` and `src/os` is accepted, names the 30 `src/os`-to-`src/core` edges in `tools/quality/layering_baseline.txt` as the accepted set, and states whether a new `src/os`-to-`src/core` edge fails the layering check
- [ ] #3 Given the decision record, when QA reads it, then it names the Windows-only include of `../ui/Windows/stdafx.h` from `src/core/PwsPlatform.h` as the only exception to the no-`src/ui` rule, and it classifies each of the 8 baseline edges from `src/core` (7) and `src/os` (1) to `wx/` headers as allowed or forbidden, leaving no baseline edge unclassified
- [ ] #4 Given the decision record, when QA reads it, then it lists the conditions under which the decision would be reversed
- [ ] #5 Given the decision record, when QA reads it, then it states that any change to `tools/quality/layering_baseline.txt` is reviewed as a design change by the architect before it merges
<!-- AC:END -->
