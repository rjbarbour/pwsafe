---
id: PWS-15
title: Check the Ubuntu workflows on the Ubuntu 26.04 runner image before 19 October
status: To Do
assignee: []
created_date: '2026-10-08 13:11'
labels: []
dependencies: []
type: chore
ordinal: 15000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
GitHub's `ubuntu-latest` runner image is due to move to Ubuntu 26.04 on 19 October 2026, according to Grace Hopper. Before then, `cmake-build.yml` and `codeql-analysis.yml`, the fork's workflows that run on `ubuntu-latest`, are run once on the Ubuntu 26.04 image, and the results are recorded. If either fails, the task records the failure and goes back to Fred Brooks for a decision, for example pinning the image or fixing the build. Making that change is a separate task.

Requested by Grace Hopper, relayed by Fred Brooks, 2026-10-08.

Exclusions: no workflow change lands on `master` under this task; the test runs use a throwaway branch that is deleted unmerged; fork-only; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given a throwaway branch in rjbarbour/pwsafe that sets the Ubuntu jobs of `cmake-build.yml` and `codeql-analysis.yml` to the Ubuntu 26.04 image, when both workflows run on it before 19 October 2026, then the task notes record each run's URL and result
- [ ] #2 Given either run fails, when QA reads the task notes, then they name the failing step and its first error, and record that the task went back to Fred Brooks for a decision
- [ ] #3 Given the check is finished, when QA lists the branches of rjbarbour/pwsafe, then the throwaway branch is gone, and no workflow file on `master` has changed for this task
<!-- AC:END -->
