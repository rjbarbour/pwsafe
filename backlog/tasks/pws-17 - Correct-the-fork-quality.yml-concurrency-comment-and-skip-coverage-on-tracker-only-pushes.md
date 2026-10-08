---
id: PWS-17
title: >-
  Correct the fork-quality.yml concurrency comment and skip coverage on
  tracker-only pushes
status: To Do
assignee: []
created_date: '2026-10-08 15:57'
updated_date: '2026-10-08 15:59'
labels:
  - quality
dependencies:
  - PWS-05
modified_files:
  - .github/workflows/fork-quality.yml
type: chore
ordinal: 17000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Two housekeeping changes to `.github/workflows/fork-quality.yml`, from Dennis Ritchie's retrospective review of PR #6 (PWS-05 notes, findings 1 and 2).

First, the concurrency comment is corrected. It says every push to `master` keeps its own run, but GitHub keeps at most one running and one pending run per concurrency group, so a newer push cancels the older pending run whatever `cancel-in-progress` says (seen on run 37804187626). The comment is reworded to say that; the `concurrency` settings themselves are unchanged.

Second, the coverage job no longer runs on pushes to `master` that change only tracker files: the `push` trigger gets `paths-ignore` for `backlog/**` and `backlog.config.yml`. A push that changes any other file still runs it. The `pull_request` trigger gets no path filter, because a skipped required check stays pending: if the coverage job is ever made a required check, no path filter may apply to it, and a comment next to the filter says so.

Requested by Fred Brooks from Dennis Ritchie's review, 2026-10-08.

Exclusions: fork-only, never part of an upstream pull request; no change to the job's steps, `tools/quality/coverage.sh` or any upstream workflow; no file under `src/` changes; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the change, when QA reads `.github/workflows/fork-quality.yml`, then the concurrency comment says that a newer push to `master` cancels an older run still pending in the same group, it no longer says every push keeps its own run, and the `concurrency` group and `cancel-in-progress` values are unchanged
- [ ] #2 Given the change, when QA reads the workflow triggers, then `push` has `paths-ignore` listing exactly `backlog/**` and `backlog.config.yml`, `pull_request` and `workflow_dispatch` have no path filter, and a comment next to the filter says it must be removed if the coverage job becomes a required status check, because a skipped required check stays pending
- [ ] #3 Given a push to `master` that changes only files under `backlog/` or `backlog.config.yml`, when it lands, then no Fork quality run starts for it; and given a push that also changes any other file, then the coverage job runs as before; the task notes give the commit SHAs or run URLs for both
- [ ] #4 Given the pull request, when QA reads its diff, then it changes only `.github/workflows/fork-quality.yml`, and only its comment and `on.push` block
- [ ] #5 Given the pull request for this task, when it is merged, then Fred Brooks and Dennis Ritchie have each recorded a code review, and every automated-check finding on it (CI, CodeQL, the fork quality gate or any other check) has been addressed by disabling or tuning the rule, suppressing it in code within this task's limits, mitigating or fixing it, or recording the residual risk in `backlog/docs/raid-log.md`, and the pull request or task notes say which for each finding
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
DoR check 2026-10-08 (Fred Brooks, Definition of Ready v1.3): pass. RD-01: the outcome is explicit (an accurate concurrency comment, and no coverage run on tracker-only pushes), and the benefit is to platform operations (master coverage runs are not cancelled by tracker commits; RAID I-04). RD-02: scope, exclusions and the required-check escalation are explicit. RD-03: AC 1-5 are concrete and deterministic, with run URLs or SHAs for AC 3. RD-04: depends on PWS-05 (Done). PWS-07 edits the same fork-quality.yml, so whichever merges second rebases on the other; this does not block either. RD-05: low risk, reversible, Build commitment (project default). RD-06: one file changes; QA by Edsger Dijkstra; two code reviews (AC 5); the gate after is Done and closing RAID I-04. RD-07: project defaults; making the coverage job a required check is Robert's decision and is covered by AC 2's comment. Observation, not a gap: PWS-13 ignores backlog/** only for CodeQL, while this task also ignores backlog.config.yml. Stays in To Do while Ready holds 3 (PWS-06, PWS-07, PWS-13).
<!-- SECTION:NOTES:END -->
