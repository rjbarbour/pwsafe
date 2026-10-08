---
id: PWS-03
title: Confirm the CodeQL alert baseline on fork master under the default query suite
status: In Progress
assignee:
  - '@grace-hopper'
created_date: '2026-10-08 12:49'
updated_date: '2026-10-08 13:27'
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

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-10-08 14:27 BST: CodeQL baseline on master 293d1bf completed (analysis uploaded 14:18 BST); Grace started. Moved to In Progress by Fred Brooks.

Baseline 2026-10-08 (Grace Hopper).

Workflow: `.github/workflows/codeql-analysis.yml` unchanged from upstream 3996b15 (`git diff` empty against the analysed commit). Init inputs are `languages: cpp` only, with no `queries:`, `packs:` or `config-file:` input, so the default query suite. Code scanning default setup state: not-configured (no clash with the advanced workflow).

Run: https://github.com/rjbarbour/pwsafe/actions/runs/37781946022 (push to master, Analyze-Linux success). Analysed commit: 293d1bf0a61912cb3922e3616236e969d4423f39. CodeQL CLI 2.27.1 (job log). Analysis id 1915953522, uploaded 14:18 BST; category `.github/workflows/codeql-analysis.yml:analyzeL`; tool CodeQL 2.27.1; rules_count 58; results_count 2; error empty.

Open alerts on refs/heads/master: total 2. Without a security severity: 0. With a security severity: critical 2. Sum 2. Both are pre-existing upstream code: the source tree at 293d1bf is identical to upstream 3996b15 (only AGENTS.md, backlog.config.yml and backlog/ differ), and neither alert is in a file PR #2 (PWS-02) changes. Triage is PWS-09, with alert detail kept out of the repository; dismissal awaits Robert Barbour.
<!-- SECTION:NOTES:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 12:55
---
DoR check 2026-10-08 (Fred Brooks): pass. Outcome, scope, acceptance evidence and QA route are explicit; no dependencies or open decisions; task notes only, no file changes; Build commitment (project default).
---
<!-- COMMENTS:END -->
