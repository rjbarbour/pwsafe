---
id: PWS-04
title: 'Decision record: include layering between core, os and ui'
status: Done
assignee:
  - '@barbara-liskov'
created_date: '2026-10-08 12:49'
updated_date: '2026-10-08 15:55'
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
- [x] #1 Given the decision record created with `backlog decision create`, when QA reads it, then it states that no file under `src/core` or `src/os` includes a header under `src/ui`
- [x] #2 Given the decision record, when QA reads it, then it lists inline all 39 include edges found at fork master `f24fd88`, each as source file, included header and classification, with counts of 30 `src/os` to `src/core`, 7 `src/core` to `wx/`, 1 `src/os` to `wx/` and 1 `src/core` to `src/ui`; and given any listed edge, when QA runs `git grep -n '#include' f24fd88 -- <source file>`, then the include is present
- [x] #3 Given the decision record, when QA reads it, then it states that the existing include cycle between `src/core` and `src/os` is accepted, names the 30 `src/os`-to-`src/core` edges in its list as the accepted set, and states whether a new `src/os`-to-`src/core` edge fails the layering check
- [x] #4 Given the decision record, when QA reads it, then it names the Windows-only include of `../ui/Windows/stdafx.h` from `src/core/PwsPlatform.h` as the only exception to the no-`src/ui` rule, and it classifies each of the 8 listed edges from `src/core` (7) and `src/os` (1) to `wx/` headers as allowed or forbidden, leaving no listed edge unclassified
- [x] #5 Given the decision record, when QA reads it, then it lists the conditions under which the decision would be reversed
- [x] #6 Given the decision record, when QA reads it, then it states that the edge-list file used by the PWS-07 layering check must list exactly the edges in the record, and that any change to either list is reviewed as a design change by the architect or Fred Brooks before it merges
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-10-08 14:30 BST: Decision record decision-01 landed in 1f90a0b. Moved to Review by Fred Brooks; QA (Edsger Dijkstra) checks AC 1-6 against the record and fork master f24fd88.

2026-10-08 14:32 BST: QA (Edsger Dijkstra) passed AC 1-6 against decision-01 (1f90a0b) and f24fd88: all 39 edges checked and regenerated with an exact match, counts 30/7/1/1. Non-blocking for PWS-07: src/core/PWSversion.cpp includes generated "version.h" (from src/ui/*/version.in, resolved in the build directory); the layering check's path resolution must handle it. Accepted and moved to Done by Fred Brooks (tracker-only task, no PR).
2026-10-08 16:55 BST (Barbara Liskov), DoD v1.1 DD-05, residual risk and next step: (1) An upstream sync can bring in new include edges; the PWS-07 layering check fails on any edge not in decision-01, and each such edge is reviewed as a design change, per decision-01's consequences. (2) Generated header: src/core/PWSversion.cpp includes "version.h", generated from src/ui/*/version.in. CMake and Xcode write it to the build directory, but Makefile.macos writes it into src/ui/wxWidgets, so resolution by filesystem would count a core-to-ui edge. Agreed handling in PWS-07: resolve includes against git ls-files, with one allow-list entry for PWSversion.cpp; decision-01 unchanged (Fred Brooks, 2026-10-08). Next step: PWS-07 adopts the edge-list file, which must equal decision-01's 39 edges.

DoD v1.1 check 2026-10-08 (Fred Brooks): DD-01 pass: AC 1-6 are ticked after Edsger Dijkstra's QA, which regenerated all 39 edges at f24fd88 with an exact match (counts 30/7/1/1); DD-02 pass: decision-01 is on fork master in 1f90a0b, the commit QA checked; no code change; DD-03 pass: Edsger Dijkstra's independent QA plus Fred Brooks's acceptance review of the record, proportionate for a tracker-only decision record with no pull request; DD-04 pass: decision-01 is the deliverable, status accepted, with alternatives, consequences and reversal conditions, and later changes go by supersession; DD-05 pass: Barbara Liskov's note (ceeaa88) records the residual risks, logged as RAID R-01 (an upstream sync brings new edges) and R-02 (generated version.h under Makefile.macos), and the next gate is PWS-07, whose edge-list file must equal decision-01's 39 edges (PWS-07 AC 8 and AC 10); overlay DO-05 (decision record: authority, terminology and edge references checked by QA, no build needed), and DO-03's 'record any new boundary rule' is met by decision-01. Result: meets DoD.
<!-- SECTION:NOTES:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 12:55
---
DoR check 2026-10-08 (Fred Brooks): fail. Source material cannot be found from the task: tools/quality/layering_baseline.txt and layering.py are not in the repository. They exist only as Grace Hopper's drafts on the team box (/workspace/grace-quality/out/layering_baseline.txt, /workspace/grace-quality/scripts/layering.py). Record where they are, or how to regenerate the 39 edges at f24fd88, so QA can check AC #2 and #3. Counts checked against that file: 30 os-to-core, 7 core-to-wx, 1 os-to-wx, 1 core-to-ui.
---

author: @fred-brooks
created: 2026-10-08 13:06
---
DoR re-check 2026-10-08 (Fred Brooks): pass. Prior gap closed: the 39 edges are listed inline; QA checks against f24fd88 with no draft needed. Assigned to Barbara Liskov. Build commitment (project default).
---
<!-- COMMENTS:END -->
