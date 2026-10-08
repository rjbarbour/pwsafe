---
id: PWS-21
title: 'Fail a pull request that adds a *.psafe3 file, with a fork-only check'
status: To Do
assignee: []
created_date: '2026-10-08 16:13'
labels:
  - quality
dependencies: []
type: chore
ordinal: 21000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Longer-term mitigation for RAID R-11 (`backlog/docs/raid-log.md`): nothing in the repository stops a `*.psafe3` password database being committed. A fork-only check under `tools/quality/`, run from a `.github/workflows/fork-*.yml` workflow, fails a pull request to fork `master` that adds such a file or renames a file to such a name. The local `.git/info/exclude` entry stays as it is.

From Dennis Ritchie's retrospective review of PR #1 (finding 4, recorded on PWS-01 in 68d429b93) and RAID R-11.

Exclusions: upstream `.gitignore` and upstream workflows are not edited; no file under `src/` changes; fork-only, never part of an upstream pull request; the RAID log is not edited by this task; no real safe data in any test file; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given a pull request to fork `master` that adds a file whose name ends in `.psafe3` (in any directory and in any letter case), or renames a file to such a name, when the fork-only check runs, then it fails and its log names each such file
- [ ] #2 Given a pull request to fork `master` that adds or renames no such file, when the fork-only check runs, then it passes
- [ ] #3 Given the evidence for AC 1 and AC 2, when QA reads the task notes, then they link one failing and one passing run, the failing run used an empty placeholder file with no safe data, and that file was never merged
- [ ] #4 Given the pull request diff, when it is inspected, then it touches only `tools/quality/` and `.github/workflows/fork-*.yml`, and `.gitignore`, the upstream workflows and `src/` are unchanged
- [ ] #5 Given the pull request for this task, when it is merged, then Fred Brooks and Dennis Ritchie have each recorded a code review, and every automated-check finding on it (CI, CodeQL, the fork quality gate or any other check) has been addressed by disabling or tuning the rule, suppressing it in code within this task's limits, mitigating or fixing it, or recording the residual risk in `backlog/docs/raid-log.md`, and the pull request or task notes say which for each finding
<!-- AC:END -->
