---
id: doc-01
title: RAID log
type: other
created_date: '2026-10-08 15:54'
---

# RAID log: rjbarbour/pwsafe fork

Risks, assumptions, issues and dependencies for the rjbarbour/pwsafe fork. Robert Barbour's rule (2026-10-08): every automated-check finding on a pull request, for feature and platform work alike, is addressed before merge, by disabling or tuning the rule, suppressing it in code, or mitigating it; any risk that remains is logged here. Every entry names an owner and a linked PWS task or pull request, and the detail stays in that task's notes. This file is fork-only (it lives under `backlog/`) and never enters an upstream pull request. The repository is public, so no security-vulnerability detail, CodeQL alert location or rule name, or secret goes in this file; such items are referred to by task ID only.

Status values: Open (action or decision outstanding), Monitoring (mitigated or accepted, watched for change), Closed (no longer applies; keep the row).

## Risks

| ID | Date | Description | Owner | Linked task/PR | Mitigation or next step | Status |
|---|---|---|---|---|---|---|
| R-01 | 2026-10-08 | An upstream sync from pwsafe/pwsafe can bring in new include edges between `src/core`, `src/os`, `src/ui` and `wx/` that the fork does not control. | Barbara Liskov | PWS-04 (decision-01, Consequences), PWS-07 | PWS-07's layering check fails on any edge not in decision-01; each new edge is reviewed as a design change and decision-01 is superseded with the new list. The sync is not blocked by default. | Open (mitigation lands with PWS-07) |
| R-02 | 2026-10-08 | `src/core/PWSversion.cpp` includes the generated `version.h`. `Makefile.macos` writes it into `src/ui/wxWidgets`, so resolving includes by file system would count a core-to-ui edge on that build. | Grace Hopper | PWS-04 (note ceeaa88), PWS-07 AC 10 | The layering check resolves includes against `git ls-files`, with one allow-list entry naming `src/core/PWSversion.cpp`; decision-01 is unchanged. | Open (mitigation lands with PWS-07) |
| R-03 | 2026-10-08 | The fork's macOS app keeps the bundle ID `org.pwsafe.pwsafe`. Only if Huvisoft's app has the same ID might macOS treat the two apps as one for preferences and "Open With". | Robert Barbour | PWS-12 | Robert checks Huvisoft's ID with `defaults read "/Applications/<Huvisoft app>.app/Contents/Info" CFBundleIdentifier` before the PWS-12 side-by-side install (AC 2). Changing the bundle ID is out of PWS-12's scope. | Open |
| R-04 | 2026-10-08 | On the `ubuntu-26.04` runner image, apt cannot find `dpkg-sig`, so cpack builds the `.deb` unsigned; the step still succeeds. | Grace Hopper | PWS-15 | The setup script already treats `dpkg-sig` as optional. Next step: decide whether to accept the unsigned `.deb` or raise a platform task before `ubuntu-latest` moves to 26.04 (from 19 October 2026). | Open |
| R-05 | 2026-10-08 | PWS-05's CI coverage figures differ slightly from Grace Hopper's f24fd88 baseline (`src/core` lines 7656/19423 v. 7659/19424, functions 927/1493 v. 930/1495; `src/os/unix` lines 431/1988 v. 430/1988, functions 54/196 both), all within 0.12 percentage points. No file under `src/` changed between f24fd88 and 35c62e7, and the differences sit in three files. Likely cause, not confirmed: the toolchain. The PR run's configure log (run 37787860322) shows "The CXX compiler identification is GNU 13.3.0"; the team box has GCC 14.2. | Grace Hopper | PWS-05 AC 4, PR #6 | The first `master` run (37804161642 on 35c62e7) gave the same figures as the PR run, so CI is stable from run to run (11a3386). Accepted for PWS-05's AC 4; later comparisons use the CI figures, and R-09 covers re-baselining after the Ubuntu 26 move. | Monitoring |
| R-06 | 2026-10-08 | Several later CodeQL analyses of `master` (27ad593, fba2350, 1f0128b, 390051d) show 0 rules and 0 results, so a listed analysis with 0 results does not prove a real scan. | Grace Hopper | PWS-03 (QA note), PWS-06, PWS-13 | PWS-06 and PWS-13 check the rules count of an analysis, not only its results count, before treating it as a clean scan. | Open |
| R-07 | 2026-10-08 | GitHub Actions in the fork-only `fork-quality.yml` are pinned by tag, not by commit SHA, and gcovr is pinned by version with no hash check (PR #6 review nit and Dennis Ritchie's retrospective review, 2449a589e). | Grace Hopper | PWS-05, PR #6 | Accepted as low risk: the job has a read-only token and no secrets, and the upstream workflows pin the same way. Revisit if the job gains write permissions or secrets. | Accepted |
| R-08 | 2026-10-08 | Pull request branches are based on upstream master and so do not contain the fork's `AGENTS.md`; the Codex reviewer may not apply the fork's review rules to them. | Barbara Liskov | PWS-11 | PWS-11's representative pull request shows whether Codex applies the rules to such a branch. | Open |
| R-09 | 2026-10-08 | `ubuntu-latest` moves to Ubuntu 26.04 on 19 October 2026. Its newer GCC can shift the coverage figures and gcovr's JSON format (Dennis Ritchie's retrospective review, 2449a589e). Kept apart from R-04, which is about `.deb` signing, not coverage. | Grace Hopper | PWS-05, PWS-15 | Pin the coverage job to `ubuntu-24.04`, or re-baseline coverage after the move. | Open |
| R-10 | 2026-10-08 | gcovr reports 4 "suspicious hits" that `tools/quality/coverage.sh` ignores, so a few `src/core` lines are under-counted in the coverage report (Dennis Ritchie's retrospective review, 2449a589e). | Grace Hopper | PWS-05, PWS-18 | PWS-18 raises `--gcov-suspicious-hits-threshold` above the observed count. | Open (mitigation in PWS-18) |

## Assumptions

| ID | Date | Description | Owner | Linked task/PR | Mitigation or next step | Status |
|---|---|---|---|---|---|---|
| A-01 | 2026-10-08 | The fork-only coverage job is skipped in any repository other than rjbarbour/pwsafe because of its job-level `github.repository == 'rjbarbour/pwsafe'` condition. QA passed this on inspection only; it has not been run in another repository. | Grace Hopper | PWS-05 AC 5, PR #6 | Confirm the skip if the workflow is ever run in another repository; the same guard pattern is reused by PWS-07. | Monitoring |
| A-02 | 2026-10-08 | The Ubuntu workflows stay green when GitHub moves `ubuntu-latest` to 26.04 (from 19 October 2026), based on the PWS-15 runs on image `ubuntu-26.04` 20260927.149.1. | Grace Hopper | PWS-15 | Check the first `master` runs after the switch. | Monitoring |

## Issues

| ID | Date | Description | Owner | Linked task/PR | Mitigation or next step | Status |
|---|---|---|---|---|---|---|
| I-01 | 2026-10-08 | PR #6 was merged (35c62e7) with one code review, Fred Brooks's, before Robert's rule of two code reviews per pull request (Fred Brooks and Dennis Ritchie). | Dennis Ritchie | PWS-05, PR #6 | Dennis's retrospective review of 35c62e7 passed with no blockers (PWS-05 note, 2449a589e). His findings are logged as R-07, R-09, R-10 and I-04. | Closed |
| I-02 | 2026-10-08 | PR #1 was merged (f24fd88) with no GitHub approving review: the owner's merge, the Codex bot's automated review with no findings, and Edsger Dijkstra's QA. | Fred Brooks | PWS-01, PR #1 | No waiver is sought. Under Robert's two-reviewer rule, Fred Brooks and Dennis Ritchie review f24fd88 retrospectively and record the result in PWS-01's notes. | Open (retrospective review pending) |
| I-03 | 2026-10-08 | gcovr "suspicious hits" on the coverage job (Dennis Ritchie's retrospective review, 2449a589e). | Grace Hopper | PWS-05, PR #6 | Recorded as a risk instead: see R-10. | Closed (moved to R-10) |
| I-04 | 2026-10-08 | The coverage workflow's concurrency comment does not hold: a newer push to `master` cancels a pending run (seen on run 37804187626 for 9b3e6a5), and every push to `master`, tracker-only ones included, runs the full coverage build (Dennis Ritchie's retrospective findings 1 and 2 on PR #6). | Grace Hopper | PWS-05, PWS-17, PR #6 | PWS-17 corrects the concurrency comment and skips coverage on tracker-only pushes. | Open (fix in PWS-17) |

## Dependencies

| ID | Date | Description | Owner | Linked task/PR | Mitigation or next step | Status |
|---|---|---|---|---|---|---|
| D-01 | 2026-10-08 | PWS-16 depends on PWS-02: both change the Basic tab of the Add/Edit Entry dialog. | Fred Brooks | PWS-16, PWS-02, PR #2 | PWS-16 is held in To Do until PWS-02 is Done, to avoid a merge clash. | Open |
| D-02 | 2026-10-08 | PWS-07 depends on PWS-04 and PWS-05. | Fred Brooks | PWS-07, PWS-05, PR #6 | Both are Done (PWS-05 on 2026-10-08), so PWS-07 is no longer blocked. | Closed |
| D-03 | 2026-10-08 | The PWS-02 rework depends on Robert's decision on where the passphrase setting is saved; the acceptance criteria are rewritten after it. | Robert Barbour | PWS-02, PR #2 | Robert picks where the setting is saved; Margaret Hamilton then rewrites the criteria. | Open |
