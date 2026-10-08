---
id: PWS-07
title: Fork-only quality gate workflow for new and changed code (fork-quality.yml)
status: To Do
assignee: []
created_date: '2026-10-08 12:50'
updated_date: '2026-10-08 13:33'
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
`.github/workflows/fork-quality.yml` runs on pull requests to `master` in rjbarbour/pwsafe. It configures with `CMAKE_EXPORT_COMPILE_COMMANDS=ON` and fails only when new or changed lines break the agreed limits: CRAP, changed-line coverage, lizard complexity, clang-tidy, cppcheck and include layering. Duplication is reported with lizard `-Eduplicate` but never fails the job. The layering rules come from the PWS-04 decision record; coverage comes from the PWS-05 build.

Static analysis: clang-tidy and cppcheck write SARIF, which is uploaded to GitHub code scanning with `github/codeql-action/upload-sarif` so the findings sit alongside CodeQL. A false positive is dismissed in code scanning with a reason, and that dismissal is the audit trail. The gate itself fails the job on new findings on changed lines, using `clang-tidy-diff` for clang-tidy and `diff-quality` for cppcheck. There is no self-hosted dashboard (no CodeChecker server, no SonarQube), no include-what-you-use, and no PMD or CPD.

Rule tuning: a noisy or false-positive rule is disabled in fork-only configuration under `tools/quality/`, never in an upstream file. An inline suppression (`NOLINT`, `cppcheck-suppress`) is a last resort for a single genuine false positive, because it would end up in upstream pull requests.

Scope: the gate covers new or changed lines only. There is no refactoring of existing code beyond what a feature needs; broader clean-up is a separate project.

Layering check: it may use an existing GitHub Action if Grace Hopper finds a suitable one, otherwise `tools/quality/layering.py`. Either way it reads an edge-list file that lists exactly the 39 edges in the PWS-04 decision record; any difference is a design change for the architect or Fred Brooks to review.

Drafts by Grace Hopper, on the team box and not in the repository: `/workspace/grace-quality/proposed/fork-quality.yml`, `/workspace/grace-quality/proposed/clang-tidy-gate.yaml`, `/workspace/grace-quality/scripts/gate_changed.py`, `/workspace/grace-quality/scripts/layering.py` and `/workspace/grace-quality/out/layering_baseline.txt`, with destinations under `tools/quality/`. The PMD CPD draft (`cpd.sh`) is dropped.

Code-quality stack agreed in the pwsafe platform room; requested by Fred Brooks, 2026-10-08. Tooling rulings (PMD and CPD dropped, lizard duplication report-only, fork-only rule tuning, SARIF upload to code scanning, new or changed lines only, layering action left open) by Robert Barbour in the platform room, relayed by Fred Brooks, 2026-10-08.

Exclusions: the upstream workflows (`cmake-build.yml`, `codeql-analysis.yml`, `macos-latest.yml`, `macos-cmake-latest.yml`) stay untouched; fork-only, never part of an upstream pull request; any gate covers new or changed code only; no SonarQube Cloud or CodeRabbit; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given a pull request to `master` in rjbarbour/pwsafe, when it is opened, then the `quality` job of `.github/workflows/fork-quality.yml` runs and its configure step log shows `CMAKE_EXPORT_COMPILE_COMMANDS=ON`; and given the same workflow in any other repository, when it is triggered, then the job is skipped by its `github.repository == 'rjbarbour/pwsafe'` condition
- [ ] #2 Given a pull request that adds a function with CCN above 10 or lizard cognitive complexity above 15, or adds a function under `src/core` or `src/os` with CRAP above 30, or leaves less than 80% of its changed lines under `src/core` and `src/os` covered by Coretests, when the gate runs, then the job fails and the job summary names each function or file and the limit it breaks
- [ ] #3 Given a pull request that edits an existing function already above CCN 10 or cognitive complexity 15 without raising its modified CCN or cognitive complexity, or that leaves such legacy functions untouched, when the gate runs, then those functions do not fail the job; and given an edit that raises either figure, then the job fails and the summary marks the function as a ratchet failure
- [ ] #4 Given `tools/quality/clang-tidy-gate.yaml` enables checks only from the `bugprone-`, `cert-` and `clang-analyzer-` groups, when a pull request has a clang-tidy finding on a changed line, then `clang-tidy-diff` fails the job; when it has a cppcheck finding of severity `error` or `warning` on a changed line, then `diff-quality` fails the job; and a finding only on unchanged lines, or a cppcheck finding of any other severity, does not fail the job
- [ ] #5 Given a gate run on a pull request, when QA opens the repository's code-scanning alerts, then the clang-tidy and cppcheck findings are there under the `clang-tidy` and `cppcheck` categories, uploaded as SARIF with `github/codeql-action/upload-sarif`, and the alerts new to the pull request are listed on it
- [ ] #6 Given a pull request whose changed lines add a block that duplicates code elsewhere under `src/`, when the gate runs, then the job summary shows the lizard `-Eduplicate` report naming both locations, and that duplication alone does not fail the job
- [ ] #7 Given a pull request that adds an include edge not in the layering check's edge-list file, when the gate runs, then the job fails and lists the edge as NEW; and given a pull request that edits the edge-list file, then its review records the design-change approval of the architect or Fred Brooks required by the PWS-04 decision record
- [ ] #8 Given the edge-list file the layering check reads, when QA compares it with the PWS-04 decision record, then both list the same 39 edges
- [ ] #9 Given the pull request that adds the gate, when QA reads its diff, then every changed file is `.github/workflows/fork-quality.yml` or under `tools/quality/`, no file under `src/` changes, no `NOLINT` or `cppcheck-suppress` comment is added, and the workflow neither installs nor runs PMD, CPD, include-what-you-use, CodeChecker or SonarQube
- [ ] #10 Given `src/core/PWSversion.cpp` includes the generated `"version.h"`, which is produced in the build directory from the `src/ui/*/version.in` templates, when the layering check runs, then it resolves that include to the build directory rather than to `src/ui`, does not report it as a `src/ui` include or a NEW edge, and the edge-list file still lists exactly the 39 edges of the PWS-04 decision record
<!-- AC:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 12:55
---
DoR check 2026-10-08 (Fred Brooks): fail. Awaiting content update for owner's tooling ruling (PMD dropped); re-check after.
---

author: @fred-brooks
created: 2026-10-08 13:06
---
DoR re-check 2026-10-08 (Fred Brooks): pass. Owner tooling ruling applied: PMD/CPD dropped; lizard duplication report-only; cppcheck error/warning fails on changed lines; clang-tidy bugprone/cert/clang-analyzer; drafts located. Depends on PWS-04 and PWS-05 (now Ready). Build commitment (project default).
---

author: @fred-brooks
created: 2026-10-08 13:07
---
Passed DoR 2026-10-08; held in To Do under the 1–3 Ready limit until its dependencies (PWS-04, PWS-05) are Done. No content gap.
---
<!-- COMMENTS:END -->
