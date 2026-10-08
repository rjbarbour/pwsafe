---
id: PWS-04
title: 'Decision record: include layering between core, os and ui'
status: Shaping
assignee:
  - '@barbara-liskov'
created_date: '2026-10-08 12:49'
updated_date: '2026-10-08 12:57'
labels:
  - quality
dependencies: []
type: task
ordinal: 4000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A Backlog.md decision record fixes which include edges between `src/core`, `src/os` and `src/ui` are allowed, so that the layering check in the fork quality gate (PWS-07) enforces an agreed design rule rather than a script default. The record is self-contained: it lists inline every include edge found at fork master `f24fd88` (39 edges), each with its source file, the included header and its classification, so QA can check it by reading the record and the source at `f24fd88`, without any draft. The edge-list file and the layering check are adopted in PWS-07 and must match this list; any difference is a design change for the architect or Fred Brooks to review. The deliverable is the decision record; no source file changes.

Source material: Grace Hopper's drafts on the team box, not in the repository: `/workspace/grace-quality/out/layering_baseline.txt` (the 39 edges), `/workspace/grace-quality/out/layering_report.txt` (the same edges with line numbers and rule) and `/workspace/grace-quality/scripts/layering.py`. Counts at `f24fd88`: 30 `src/os` to `src/core`, 7 `src/core` to `wx/`, 1 `src/os` to `wx/`, 1 `src/core` to `src/ui`.

Code-quality stack agreed in the pwsafe platform room; requested by Fred Brooks, 2026-10-08. Inline listing of the edges requested by Barbara Liskov, 2026-10-08.

Exclusions: the upstream workflows (`cmake-build.yml`, `codeql-analysis.yml`, `macos-latest.yml`, `macos-cmake-latest.yml`) stay untouched; fork-only, never part of an upstream pull request; any gate covers new or changed code only; no SonarQube Cloud or CodeRabbit; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the decision record created with `backlog decision create`, when QA reads it, then it states that no file under `src/core` or `src/os` includes a header under `src/ui`
- [ ] #2 Given the decision record, when QA reads it, then it lists inline all 39 include edges found at fork master `f24fd88`, each as source file, included header and classification, with counts of 30 `src/os` to `src/core`, 7 `src/core` to `wx/`, 1 `src/os` to `wx/` and 1 `src/core` to `src/ui`; and given any listed edge, when QA runs `git grep -n '#include' f24fd88 -- <source file>`, then the include is present
- [ ] #3 Given the decision record, when QA reads it, then it states that the existing include cycle between `src/core` and `src/os` is accepted, names the 30 `src/os`-to-`src/core` edges in its list as the accepted set, and states whether a new `src/os`-to-`src/core` edge fails the layering check
- [ ] #4 Given the decision record, when QA reads it, then it names the Windows-only include of `../ui/Windows/stdafx.h` from `src/core/PwsPlatform.h` as the only exception to the no-`src/ui` rule, and it classifies each of the 8 listed edges from `src/core` (7) and `src/os` (1) to `wx/` headers as allowed or forbidden, leaving no listed edge unclassified
- [ ] #5 Given the decision record, when QA reads it, then it lists the conditions under which the decision would be reversed
- [ ] #6 Given the decision record, when QA reads it, then it states that the edge-list file used by the PWS-07 layering check must list exactly the edges in the record, and that any change to either list is reviewed as a design change by the architect or Fred Brooks before it merges
<!-- AC:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 12:55
---
DoR check 2026-10-08 (Fred Brooks): fail. Source material cannot be found from the task: tools/quality/layering_baseline.txt and layering.py are not in the repository. They exist only as Grace Hopper's drafts on the team box (/workspace/grace-quality/out/layering_baseline.txt, /workspace/grace-quality/scripts/layering.py). Record where they are, or how to regenerate the 39 edges at f24fd88, so QA can check AC #2 and #3. Counts checked against that file: 30 os-to-core, 7 core-to-wx, 1 os-to-wx, 1 core-to-ui.
---
<!-- COMMENTS:END -->
