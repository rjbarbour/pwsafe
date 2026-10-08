---
id: PWS-15
title: Check the Ubuntu workflows on the Ubuntu 26.04 runner image before 19 October
status: Ready
assignee:
  - '@grace-hopper'
created_date: '2026-10-08 13:11'
updated_date: '2026-10-08 13:43'
labels: []
dependencies: []
type: chore
ordinal: 15000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
GitHub's `ubuntu-latest` runner image is due to move to Ubuntu 26.04 on 19 October 2026, according to Grace Hopper. Before then, the fork's workflows that use `ubuntu-latest` are run once on the Ubuntu 26.04 image label `ubuntu-26.04`, and the results are recorded. The check uses a throwaway branch that replaces only `ubuntu-latest`: the `ubuntu-latest` cell of the `cmake-build.yml` matrix, and the `runs-on: ubuntu-latest` line of `codeql-analysis.yml`. The `ubuntu-22.04` and `windows-latest` matrix cells stay unchanged. If either run fails, the task records the failure and goes back to Fred Brooks for a decision, for example pinning the image or fixing the build. Making that change is a separate task.

Requested by Grace Hopper, relayed by Fred Brooks, 2026-10-08.

Exclusions: no workflow change lands on `master` under this task; the test runs use a throwaway branch that is deleted unmerged; fork-only; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given a throwaway branch in rjbarbour/pwsafe that sets only the `ubuntu-latest` jobs to the image label `ubuntu-26.04` (the `ubuntu-latest` cell of the `cmake-build.yml` matrix and the `runs-on` of `codeql-analysis.yml`, leaving `ubuntu-22.04` and `windows-latest` unchanged), when both workflows run on it before 19 October 2026, then the task notes record each run's URL and result
- [ ] #2 Given either run fails, when QA reads the task notes, then they name the failing step and its first error, and record that the task went back to Fred Brooks for a decision
- [ ] #3 Given the check is finished, when QA lists the branches of rjbarbour/pwsafe, then the throwaway branch is gone, and no workflow file on `master` has changed for this task
<!-- AC:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 13:43
---
DoR check 2026-10-08 (Fred Brooks): fail. Name the image label ubuntu-26.04 in the description and AC #1, and say the throwaway branch replaces only ubuntu-latest (the cmake-build matrix cell and CodeQL runs-on), leaving ubuntu-22.04 and windows-latest unchanged. Will move to Ready as soon as that edit lands (19 October deadline).
---

author: @fred-brooks
created: 2026-10-08 13:43
---
DoR re-check 2026-10-08 (Fred Brooks): pass. Image label and retargeting scope now explicit.
---
<!-- COMMENTS:END -->
