---
id: PWS-03
title: Confirm the CodeQL alert baseline on fork master under the default query suite
status: Ready
assignee: []
created_date: '2026-10-08 12:49'
updated_date: '2026-10-08 12:55'
labels:
  - quality
dependencies: []
type: task
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Record how many CodeQL alerts are open on fork `master` and how they break down by rule, for one named commit analysed by the unchanged upstream `.github/workflows/codeql-analysis.yml` (default query suite), so that the suite change can be measured against it. Grace Hopper's baseline (lizard, CRAP, coverage, CPD, clang-tidy, cppcheck, layering) holds no CodeQL figures, and the code-scanning alert list for `refs/heads/master` was empty when read on 2026-10-08, which does not show whether `master` has been analysed.

Code-quality stack agreed in the pwsafe platform room; requested by Fred Brooks, 2026-10-08.

Exclusions: the upstream workflows (`cmake-build.yml`, `codeql-analysis.yml`, `macos-latest.yml`, `macos-cmake-latest.yml`) stay untouched; fork-only, never part of an upstream pull request; any gate covers new or changed code only; no SonarQube Cloud or CodeRabbit; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given `.github/workflows/codeql-analysis.yml` on fork `master` is unchanged from upstream (`git diff 3996b15 <analysed commit> -- .github/workflows/codeql-analysis.yml` is empty), when its Analyze-Linux job completes on a push to `master`, then the task notes record the run URL, the full SHA of the analysed commit and the CodeQL version shown in the run log
- [ ] #2 Given that completed run, when the open code-scanning alerts for `refs/heads/master` are listed, then the task notes record the total number of open alerts, the number per rule ID for alerts without a security severity, and the number per security-severity level (no rule ID, file or line) for alerts with one, and these numbers add up to the total
- [ ] #3 Given the recorded total is zero, when QA opens the code-scanning analyses for `refs/heads/master`, then an analysis of the recorded commit by the CodeQL tool is listed, so zero means analysed with no alerts and not never analysed
- [ ] #4 Given the recorded figures, when QA lists the open alerts for `refs/heads/master` at the recorded commit, then the numbers match the task notes
<!-- AC:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 12:55
---
DoR check 2026-10-08 (Fred Brooks): pass. Outcome, scope, acceptance evidence and QA route are explicit; no dependencies or open decisions; task notes only, no file changes; Build commitment (project default).
---
<!-- COMMENTS:END -->
