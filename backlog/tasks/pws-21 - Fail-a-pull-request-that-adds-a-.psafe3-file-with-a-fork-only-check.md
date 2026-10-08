---
id: PWS-21
title: 'Fail a pull request that adds a *.psafe3 file, with a fork-only check'
status: To Do
assignee: []
created_date: '2026-10-08 16:13'
updated_date: '2026-10-08 16:20'
labels:
  - quality
dependencies: []
modified_files:
  - .github/workflows/fork-hygiene.yml
  - tools/quality/check-no-psafe3.sh
type: chore
ordinal: 21000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Longer-term mitigation for RAID R-11 (`backlog/docs/raid-log.md`): nothing in the repository stops a `*.psafe3` password database being committed. A new fork-only workflow, `.github/workflows/fork-hygiene.yml`, with the fork repository guard (`github.repository == 'rjbarbour/pwsafe'`), calls a new script, `tools/quality/check-no-psafe3.sh`. On a pull request to fork `master` it fails the pull request if a file whose name ends in `.psafe3` is added or a file is renamed to such a name. On a push to fork `master`, where tracker-only commits land directly with no pull request (decision-02), it fails the run and names the file: it detects such a file but cannot prevent it, so RAID R-11 keeps that residual risk. Whether the check becomes a required status check is Robert Barbour's decision (AC 5). The local `.git/info/exclude` entry stays as it is.

The check is kept separate from `fork-quality.yml` and `tools/quality/coverage.sh` so that it does not collide with PWS-07, PWS-17 or PWS-18.

From Dennis Ritchie's retrospective review of PR #1 (finding 4, recorded on PWS-01 in 68d429b93) and RAID R-11.

Exclusions: upstream `.gitignore` and upstream workflows are not edited; `fork-quality.yml` and `coverage.sh` are not edited; no file under `src/` changes; fork-only, never part of an upstream pull request; the RAID log is not edited by this task; no branch protection or ruleset change without Robert Barbour's decision; no `*.psafe3` file ever reaches fork `master`, and no real safe data in any test file; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given a pull request to fork `master` that adds a file whose name ends in `.psafe3` (in any directory and in any letter case), or renames a file to such a name, when the fork-only check runs, then it fails and its log names each such file
- [ ] #2 Given a push to fork `master` (where tracker commits land directly with no pull request) that adds a file whose name ends in `.psafe3` (in any directory and in any letter case), or renames a file to such a name, when the fork-only check runs, then it fails and its log names each such file; and the task notes state that on push the check detects the file but does not prevent it, so RAID R-11 keeps that residual risk
- [ ] #3 Given a pull request to fork `master`, or a push to fork `master`, that adds or renames no such file, when the fork-only check runs, then it passes
- [ ] #4 Given the evidence for AC 1 to AC 3, when QA reads the task notes, then they link one failing and one passing pull-request run and one passing push run on fork `master`; the failing push case is shown by running `tools/quality/check-no-psafe3.sh` on the box against the failing test branch's commit range, with its output in the notes, so that no `*.psafe3` file ever reaches fork `master`; the failing cases use an empty placeholder file with no safe data; and the test pull request is closed unmerged and its branch deleted; and running `tools/quality/check-no-psafe3.sh` on the box with an all-zero `before` and an empty placeholder `*.psafe3` file in the tree fails, and its log says it fell back to checking the whole tree, with the output in the task notes
- [ ] #5 Given the check is working, when Grace Hopper puts it to Robert Barbour, then Robert decides whether it becomes a required status check on fork `master`; Grace gives him the exact branch-protection or ruleset setting, including how tracker-only direct pushes to `master` stay possible (the owner's admin bypass with "include administrators" off, or a ruleset bypass), and states that blocking direct pushes would reverse decision-02 and need a superseding decision record; and the task notes record his answer
- [ ] #6 Given the pull request diff, when it is inspected, then it adds only `.github/workflows/fork-hygiene.yml` and `tools/quality/check-no-psafe3.sh`, the workflow has the repository guard `github.repository == 'rjbarbour/pwsafe'`, and `fork-quality.yml`, `tools/quality/coverage.sh`, `.gitignore`, the upstream workflows and `src/` are unchanged, and neither its push nor its pull_request trigger has a path filter, and the passing push run's log shows the commit range it checked, and when the push event's `before` is all zeros (a new branch) or is not an ancestor of the pushed head (a force-push), the script checks every file in the tree instead of an empty range
- [ ] #7 Given the pull request for this task, when it is merged, then Fred Brooks and Dennis Ritchie have each recorded a code review, and every automated-check finding on it (CI, CodeQL, the fork quality gate or any other check) has been addressed by disabling or tuning the rule, suppressing it in code within this task's limits, mitigating or fixing it, or recording the residual risk in `backlog/docs/raid-log.md`, and the pull request or task notes say which for each finding
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
DoR check 2026-10-08 (Fred Brooks, Definition of Ready v1.3): fail on two gaps; stays in To Do. RD-01: the outcome is explicit (RAID R-11's longer-term mitigation). RD-03: AC 1-5 are concrete. RD-05: low risk, reversible, Build commitment (project default). Gap 1 (RD-02, boundary): the check runs only on pull requests, but tracker-only changes go straight to fork master with no pull request (decision-02, point 5), so the most common write path stays unguarded. Proposed for Margaret, as a new AC: 'Given a push to fork master that adds or renames a file to a name ending in .psafe3, when the fork-only check runs on that push, then it fails and names the file; the task notes record that this detects the file after the push and does not prevent it, and RAID R-11 records that residual.' Or state the exclusion explicitly and keep R-11 open for direct pushes. Gap 2 (RD-07, owner decision): a failing check does not block a merge unless it is a required status check, which only Robert can set. Proposed: 'Whether the check becomes a required status check on master is Robert Barbour's decision; Grace Hopper gives him the exact branch-protection setting, and the task notes record his answer.' RD-04 and RD-06, overlap and sequencing: AC 4 allows tools/quality/ and any .github/workflows/fork-*.yml, which overlaps PWS-07 (fork-quality.yml and tools/quality/), PWS-17 (fork-quality.yml triggers) and PWS-18 (tools/quality/coverage.sh). Proposed: 'The check is a new job in a new workflow file, .github/workflows/fork-hygiene.yml, with its script under tools/quality/; it does not edit fork-quality.yml or coverage.sh, and the job is guarded by github.repository == rjbarbour/pwsafe.' If it must go in fork-quality.yml instead, it rebases after PWS-07 and PWS-17. Minor: add AGENTS.md-style modified_files metadata, and say the test branch is deleted after AC 3.

DoR re-check 2026-10-08 (Fred Brooks, Definition of Ready v1.3) after 1013b89ec: pass, with one proposed addition; stays in To Do. Gap 1 is closed: AC 2 adds the push trigger on fork master, its notes must say the check detects but does not prevent, and RAID R-11 keeps that residual. AC 4 proves the failing push case by running the script on the box against the test branch's commit range, so no *.psafe3 file reaches master. Gap 2 is closed: AC 5 puts the required-check decision to Robert, with the exact setting, how tracker-only direct pushes stay possible (admin or ruleset bypass), and the statement that blocking them would reverse decision-02 and need a superseding record. Also checked: AC 6 scopes the change to a new .github/workflows/fork-hygiene.yml and tools/quality/check-no-psafe3.sh, with the repository guard, and leaves fork-quality.yml and coverage.sh untouched, so it no longer collides with PWS-07, PWS-17 or PWS-18. modified_files names both files, and AC 4 closes the test pull request unmerged and deletes its branch. RD-01 to RD-07: outcome, boundaries, evidence, dependencies (none open; RAID R-11), risk (low, reversible, Build commitment by project default), delivery path (Grace Hopper, QA by Edsger Dijkstra, two code reviews, AC 7) and owner decisions (AC 5) are explicit. Proposed addition for Margaret, before Ready: the failing push case runs the script locally, not the workflow, so a path filter on the workflow's push trigger, such as PWS-17's backlog/** ignore, would go unnoticed and miss a file under backlog/. Add to AC 6: 'and neither its push nor its pull_request trigger has a path filter, and the passing push run's log shows the commit range it checked.'
<!-- SECTION:NOTES:END -->
