---
id: PWS-07
title: Fork-only quality gate workflow for new and changed code (fork-quality.yml)
status: Shaping
assignee: []
created_date: '2026-10-08 12:50'
updated_date: '2026-10-08 12:55'
labels:
  - quality
dependencies:
  - PWS-04
  - PWS-05
type: chore
ordinal: 7000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
`.github/workflows/fork-quality.yml` runs on pull requests to `master` in rjbarbour/pwsafe and fails only when new or changed code breaks the agreed limits: CRAP, changed-line coverage, lizard complexity, clang-tidy, cppcheck, duplication and include layering. Drafts by Grace Hopper, by repository destination: `.github/workflows/fork-quality.yml`, `tools/quality/gate_changed.py`, `tools/quality/layering.py`, `tools/quality/layering_baseline.txt`, `tools/quality/clang-tidy-gate.yaml`, `tools/quality/coverage.sh` and `tools/quality/cpd.sh`. The layering rules come from the PWS-04 decision record; coverage comes from the PWS-05 build.

Code-quality stack agreed in the pwsafe platform room; requested by Fred Brooks, 2026-10-08.

Exclusions: the upstream workflows (`cmake-build.yml`, `codeql-analysis.yml`, `macos-latest.yml`, `macos-cmake-latest.yml`) stay untouched; fork-only, never part of an upstream pull request; any gate covers new or changed code only; no SonarQube Cloud or CodeRabbit; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given a pull request to `master` in rjbarbour/pwsafe, when it is opened, then the `quality` job of `.github/workflows/fork-quality.yml` runs; and given the same workflow in any other repository, when it is triggered, then the job is skipped by its `github.repository == 'rjbarbour/pwsafe'` condition
- [ ] #2 Given a pull request that adds a function with CCN above 10 or lizard cognitive complexity above 15, or adds a function under `src/core` or `src/os` with CRAP above 30, or leaves less than 80% of its changed lines under `src/core` and `src/os` covered by Coretests, when the gate runs, then the job fails and the job summary names each function or file and the limit it breaks
- [ ] #3 Given a pull request that edits an existing function already above CCN 10 or cognitive complexity 15 without raising its modified CCN or cognitive complexity, or that leaves such legacy functions untouched, when the gate runs, then those functions do not fail the job; and given an edit that raises either figure, then the job fails and the summary marks the function as a ratchet failure
- [ ] #4 Given `tools/quality/clang-tidy-gate.yaml` enables checks only from the `bugprone-`, `cert-` and `clang-analyzer-` groups, when a pull request has a clang-tidy finding on a changed line, then the job fails; when it has a cppcheck finding on a changed line, then the finding is listed as a code-scanning alert new to the pull request under the `cppcheck` category; and a finding only on unchanged lines does neither
- [ ] #5 Given a pull request whose changed lines overlap a block that PMD CPD reports as duplicated at the 100-token minimum, when the gate runs, then the job fails and the summary names both locations
- [ ] #6 Given a pull request that adds an include edge not listed in `tools/quality/layering_baseline.txt` (39 edges), when the gate runs, then the job fails and lists the edge as NEW; and given a pull request that edits `tools/quality/layering_baseline.txt`, then its review records the architect's design-change approval required by the PWS-04 decision record
<!-- AC:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 12:55
---
DoR check 2026-10-08 (Fred Brooks): fail. Awaiting content update for owner's tooling ruling (PMD dropped); re-check after.
---
<!-- COMMENTS:END -->
