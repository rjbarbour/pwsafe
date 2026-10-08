---
id: PWS-15
title: Check the Ubuntu workflows on the Ubuntu 26.04 runner image before 19 October
status: Ready
assignee:
  - '@grace-hopper'
created_date: '2026-10-08 13:11'
updated_date: '2026-10-08 14:09'
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

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
ubuntu-26.04 check, 2026-10-08 (Grace Hopper). Result: both workflows pass on ubuntu-26.04. No failure, so nothing goes back to Fred Brooks.

Throwaway branch `pws-15-ubuntu-2604-check`, cut from master ceaa038, one commit c2162e2 "PWS-15: throwaway - run Ubuntu jobs on ubuntu-26.04". It changed only the `ubuntu-latest` matrix cell in cmake-build.yml to `ubuntu-26.04` and CodeQL `runs-on: ubuntu-latest` to `ubuntu-26.04`. The `windows-latest` and `ubuntu-22.04` cells were unchanged. No step condition keys off the label (steps use `runner.os`). Misc/setup-linux-dev-env.sh picks packages from the distro release, so 26.04 gets libwxgtk3.2-dev, as 24.04 does. The only label-derived value is the artifact name, PasswordSafe-ubuntu-26.04.<sha>.

Pushed 14:58 BST. The ubuntu-26.04 jobs got a runner within seconds, with no queueing.
- CMake Build, run https://github.com/rjbarbour/pwsafe/actions/runs/37788601781 : success (finished 15:08 BST)
  - build (ubuntu-26.04): success. Configure, Build, Test (2 of 2 passed), cpack DEB (passwordsafe-ubuntu26-1.25-amd64.deb), dpkg -i and artifact upload all passed.
  - build (ubuntu-22.04): success (context)
  - build (windows-latest): success (context; image windows-2025-vs2026 20260925.250.1)
- CodeQL, run https://github.com/rjbarbour/pwsafe/actions/runs/37788601678 : success (finished 15:06 BST)
  - Analyze-Linux on ubuntu-26.04: success. C++ analysed ("Running queries for cpp"). Branch analysis 1916308919 used CodeQL 2.27.1 with 58 rules and 2 results, the same as master ceaa038's analysis (58 rules, 2 results).

Image: ubuntu-26.04, Version 20260927.149.1 (runner-images release ubuntu26/20260927.149). Toolchain: GCC 15.2.0, cmake 4.2.3 from apt, wxWidgets 3.2.9. The 22.04 job used GCC 11.4.0, cmake 3.22.1 and wxWidgets 3.0.
Observation, not a failure: on 26.04, apt cannot find dpkg-sig ("E: Unable to locate package dpkg-sig"). The setup script already treats it as optional, and cpack logs "Couldn't find dpkg-sig or debsigs". The .deb is built unsigned, and the step still succeeds.

The macOS run the push triggered (mac-pwsafe 37788601663) was cancelled on the throwaway branch only, because it is out of scope.
The throwaway branch was deleted unmerged at 15:09 BST. The branches API returns 404 for it. No workflow file on master was changed by this task.
<!-- SECTION:NOTES:END -->

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
