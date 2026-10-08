---
id: PWS-08
title: ASan and UBSan coretest job
status: Shaping
assignee: []
created_date: '2026-10-08 12:50'
updated_date: '2026-10-08 13:06'
labels:
  - quality
dependencies: []
type: chore
ordinal: 8000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A fork-only CI job in its own workflow file, `.github/workflows/fork-sanitizers.yml`, builds `coretest` with AddressSanitizer and UndefinedBehaviorSanitizer together and runs Coretests, so memory and undefined-behaviour errors reached by the tests fail the run. The sanitiser flags (`-fsanitize=address,undefined`) are passed in that workflow's configure step; `CMakePresets.json` and `CMakeLists.txt` are not edited. On `master`, `CMakeLists.txt` reads `USE_ASAN` but not `USE_UBSAN`, so the existing `linux-ubsan-debug` preset does not by itself add `-fsanitize=undefined`; fixing that preset is out of scope. There is no draft for this job in Grace Hopper's material. A separate workflow file keeps this task independent of PWS-07.

First run off GitHub: Actions logs on rjbarbour/pwsafe are public, so the first sanitiser run of Coretests on `master` happens on Grace Hopper's machine with the workflow's flags, not in GitHub Actions. The workflow is pushed to a branch in rjbarbour/pwsafe only once that run is clean.

Stop condition: fixing anything under `src/` is out of scope. If that first run shows an AddressSanitizer or UBSan error in Coretests, the implementer stops, changes no file under `src/`, and escalates to Fred Brooks. The full report goes to Fred outside the repository. The task notes say only that a sanitiser error already on `master` stopped the work, with no file, line, test name or stack details, until Fred and Robert Barbour decide how to proceed.

Code-quality stack agreed in the pwsafe platform room; requested by Fred Brooks, 2026-10-08. Flags in the workflow and the stop condition: Fred Brooks, 2026-10-08.

Exclusions: the upstream workflows (`cmake-build.yml`, `codeql-analysis.yml`, `macos-latest.yml`, `macos-cmake-latest.yml`) stay untouched; fork-only, never part of an upstream pull request; any gate covers new or changed code only; no SonarQube Cloud or CodeRabbit; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given a pull request to `master` in rjbarbour/pwsafe, when the sanitiser job in `.github/workflows/fork-sanitizers.yml` builds `coretest`, then every `coretest` compile command in the job's `compile_commands.json` or build log contains both `-fsanitize=address` and `-fsanitize=undefined`
- [ ] #2 Given that build, when `ctest -R Coretests` runs and no sanitiser reports an error, then the job passes and its log contains no `ERROR: AddressSanitizer` line and no `runtime error:` line
- [ ] #3 Given a throwaway branch that adds one Coretests case with a heap buffer overflow and another with signed integer overflow, when the job runs on it, then the job fails, the log shows an AddressSanitizer report and a `runtime error:` report, and the branch is deleted unmerged with its run URL in the task notes
- [ ] #4 Given the same workflow in any repository other than rjbarbour/pwsafe, when it is triggered, then the sanitiser job is skipped
- [ ] #5 Given the pull request that adds the job, when QA reads its diff, then the only changed file is `.github/workflows/fork-sanitizers.yml`, and `CMakePresets.json`, `CMakeLists.txt` and every file under `src/` are unchanged
- [ ] #6 Given the first sanitiser run of Coretests on `master`, made on Grace Hopper's machine with the workflow's flags before the workflow is pushed anywhere in rjbarbour/pwsafe, when it reports an AddressSanitizer or UBSan error, then the workflow is not pushed, no file under `src/` is changed for this task, and the task notes say only that a sanitiser error already on `master` stopped the work and that it was escalated to Fred Brooks, with no file, line, test name or stack details
- [ ] #7 Given that first run on Grace Hopper's machine is clean, when QA reads the task notes, then they record the `master` commit it ran on, the sanitiser flags and the clean result, dated before the workflow's first GitHub Actions run
<!-- AC:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @fred-brooks
created: 2026-10-08 12:55
---
DoR check 2026-10-08 (Fred Brooks): fail. Decision supplied: sanitiser flags (-fsanitize=address,undefined) are set in the fork-only workflow; CMakePresets.json and CMakeLists.txt are not edited, and the linux-ubsan-debug preset gap is out of scope. Gap: state what happens if Coretests on master already reports an AddressSanitizer or UBSan error (escalation and stop condition, given src/ fixes are not in scope), and name the workflow file the job goes in.
---

author: @fred-brooks
created: 2026-10-08 13:06
---
Awaiting content: first sanitiser run happens locally on the platform engineer's machine; the workflow lands on master only once master is clean, because Actions logs are public.
---
<!-- COMMENTS:END -->
