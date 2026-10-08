---
id: PWS-07
title: Fork-only quality gate workflow for new and changed code (fork-quality.yml)
status: Review
assignee:
  - '@grace-hopper'
created_date: '2026-10-08 12:50'
updated_date: '2026-10-08 19:43'
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

Clean-code style rules for new files only: clang-tidy also runs the `readability-` and `modernize-` groups, from `tools/quality/clang-tidy-new-files.yaml`, on the whole of each C++ source or header file the pull request adds (the files `git diff --diff-filter=A` lists against the pull request's base), and any finding there fails the job. Files the pull request modifies get no `readability-` or `modernize-` checks; they keep the gate above (`bugprone-`, `cert-` and `clang-analyzer-` on changed lines only). Changes to existing files should follow the surrounding file's existing style, which matters more there than a clean-code rule.

Rule tuning: a noisy or false-positive rule is disabled in fork-only configuration under `tools/quality/`, never in an upstream file. That includes the `readability-` and `modernize-` rules for new files, and each rule disabled there carries a comment giving the reason; a `readability-` or `modernize-` finding is never suppressed inline with `NOLINT`. An inline suppression (`NOLINT`, `cppcheck-suppress`) is a last resort for a single genuine false positive, because it would end up in upstream pull requests.

Scope: the gate covers new or changed lines only, plus the whole of files the pull request adds for the `readability-` and `modernize-` rules. There is no refactoring of existing code beyond what a feature needs; broader clean-up is a separate project.

Layering check: it may use an existing GitHub Action if Grace Hopper finds a suitable one, otherwise `tools/quality/layering.py`. Either way it reads an edge-list file that lists exactly the 39 edges in the PWS-04 decision record; any difference is a design change for the architect or Fred Brooks to review.

Drafts by Grace Hopper, on the team box and not in the repository: `/workspace/grace-quality/proposed/fork-quality.yml`, `/workspace/grace-quality/proposed/clang-tidy-gate.yaml`, `/workspace/grace-quality/scripts/gate_changed.py`, `/workspace/grace-quality/scripts/layering.py` and `/workspace/grace-quality/out/layering_baseline.txt`, with destinations under `tools/quality/`. The PMD CPD draft (`cpd.sh`) is dropped.

Code-quality stack agreed in the pwsafe platform room; requested by Fred Brooks, 2026-10-08. Tooling rulings (PMD and CPD dropped, lizard duplication report-only, fork-only rule tuning, SARIF upload to code scanning, new or changed lines only, layering action left open) by Robert Barbour in the platform room, relayed by Fred Brooks, 2026-10-08. Clean-code style rules for added files only, not modified files, by Robert Barbour in his 1:1 with Fred Brooks, 16:45, relayed by Fred Brooks, 2026-10-08.

Exclusions: the upstream workflows (`cmake-build.yml`, `codeql-analysis.yml`, `macos-latest.yml`, `macos-cmake-latest.yml`) stay untouched; fork-only, never part of an upstream pull request; any gate covers new or changed code only; no SonarQube Cloud or CodeRabbit; no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given a pull request to `master` in rjbarbour/pwsafe, when it is opened, then the `quality` job of `.github/workflows/fork-quality.yml` runs and its configure step log shows `CMAKE_EXPORT_COMPILE_COMMANDS=ON`; and given the same workflow in any other repository, when it is triggered, then the job is skipped by its `github.repository == 'rjbarbour/pwsafe'` condition
- [ ] #2 Given a pull request that adds a function with CCN above 10 or lizard cognitive complexity above 15, or adds a function under `src/core` or `src/os` with CRAP above 30, or leaves less than 80% of its changed lines under `src/core` and `src/os` covered by Coretests, when the gate runs, then the job fails and the job summary names each function or file and the limit it breaks
- [ ] #3 Given a pull request that edits an existing function already above CCN 10 or cognitive complexity 15 without raising its modified CCN or cognitive complexity, or that leaves such legacy functions untouched, when the gate runs, then those functions do not fail the job; and given an edit that raises either figure, then the job fails and the summary marks the function as a ratchet failure
- [ ] #4 Given `tools/quality/clang-tidy-gate.yaml` enables checks only from the `bugprone-`, `cert-` and `clang-analyzer-` groups, when a pull request has a clang-tidy finding on a changed line, then `clang-tidy-diff` fails the job; when it has a cppcheck finding of severity `error` or `warning` on a changed line, then `diff-quality` fails the job; and a finding only on unchanged lines, or a cppcheck finding of any other severity, does not fail the job; and no `readability-` or `modernize-` check runs on any file the pull request modifies
- [ ] #5 Given a gate run on a pull request, when QA opens the repository's code-scanning alerts, then the clang-tidy and cppcheck findings are there under the `clang-tidy` and `cppcheck` categories, uploaded as SARIF with `github/codeql-action/upload-sarif`, and the alerts new to the pull request are listed on it
- [ ] #6 Given a pull request whose changed lines add a block that duplicates code elsewhere under `src/`, when the gate runs, then the job summary shows the lizard `-Eduplicate` report naming both locations, and that duplication alone does not fail the job
- [ ] #7 Given a pull request that adds an include edge not in the layering check's edge-list file, when the gate runs, then the job fails and lists the edge as NEW; and given a pull request that edits the edge-list file, then its review records the design-change approval of the architect or Fred Brooks required by the PWS-04 decision record
- [ ] #8 Given the edge-list file the layering check reads, when QA compares it with the PWS-04 decision record, then both list the same 39 edges
- [ ] #9 Given the pull request that adds the gate, when QA reads its diff, then every changed file is `.github/workflows/fork-quality.yml` or under `tools/quality/`, no file under `src/` changes, no `NOLINT` or `cppcheck-suppress` comment is added, and the workflow neither installs nor runs PMD, CPD, include-what-you-use, CodeChecker or SonarQube
- [ ] #10 Given `src/core/PWSversion.cpp` includes the generated `"version.h"`, which is built from the `src/ui/*/version.in` templates into the build directory by CMake and Xcode but into `src/ui/wxWidgets` by `Makefile.macos`, when the layering check runs, then it resolves includes against `git ls-files` rather than the filesystem, so that include is never counted as a `src/core` to `src/ui` edge on any build; the check's allow list has exactly one entry for it, naming `src/core/PWSversion.cpp`; it is not reported as a NEW edge; and the edge-list file still lists exactly the 39 edges of the PWS-04 decision record
- [ ] #11 Given `tools/quality/clang-tidy-new-files.yaml` enables the `readability-` and `modernize-` groups, with each rule it disables carrying a comment that gives the reason, when a pull request adds a C++ source or header file, then clang-tidy runs that configuration on the whole of each file `git diff --diff-filter=A` lists against the pull request's base, any finding fails the job, and the job summary names the file, line and rule
- [ ] #12 Given a pull request that adds a new file with a `readability-` finding, when the gate runs, then the job fails; and given a pull request whose only `readability-` finding is the same finding on a changed line of an existing file, when the gate runs, then that finding does not fail the job
- [ ] #13 Given the pull request for this task, when it is merged, then Fred Brooks and Dennis Ritchie have each recorded a code review, and every automated-check finding on it (CI, CodeQL, the fork quality gate or any other check) has been addressed by disabling or tuning the rule, suppressing it in code within this task's limits, mitigating or fixing it, or recording the residual risk in `backlog/docs/raid-log.md`, and the pull request or task notes say which for each finding
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
DoR re-check 2026-10-08 (Fred Brooks): pass. 65fd69c (readability/modernize on added files only, AC 11-12, AC 4 negative) and 7cc6b1f (AC 10 git ls-files resolution, one allow-list entry) match Robert's ruling and the agreed version.h handling. Moves to Ready once PWS-05 is Done (PR #6 merged as 35c62e7; AC 4 pending).

2026-10-08 (Fred Brooks): moved to Ready and assigned to Grace Hopper. The DoR re-check passed in 43e1401, and its dependencies PWS-04 and PWS-05 are Done. Ready now holds PWS-06, PWS-13 and PWS-07 (limit 3).

Robert's 2026-10-08 rule applies: two code reviews (Fred Brooks, Dennis Ritchie); every automated-check finding addressed before merge or logged in backlog/docs/raid-log.md.

2026-10-08 (Fred Brooks, board sync): moved Ready to In Progress. Grace Hopper opened PR #7 (branch pws-07-quality-gate, head 89f1783) at 17:46 BST; CI still queued and the PR body says evidence follows, so not yet Review. In Progress now holds PWS-02, PWS-09 and PWS-07, above the one-task limit proposed in PWS-20; flagged to Robert.

2026-10-08 (Grace Hopper, verification resume): Independent check of PR #7 head 03e9a4e16 against the ACs. No rebuild; no AC boxes ticked; status unchanged.

CI on head: Fork quality run 37816745452 (Coverage and Quality gate passed; configure log shows CMAKE_EXPORT_COMPILE_COMMANDS:UNINITIALIZED=ON); CMake Build 37816745480 (ubuntu-22.04, ubuntu-latest, windows-latest) passed; CodeQL 37816745961 Analyze-Linux passed; Socket passed. macOS runs 37816745424 (macos-latest) and 37816745594 (macos-cmake) still queued at verification time (~40+ minutes), never started.

Code scanning for refs/pull/7/merge: clang-tidy analysis 1917858718 (312 rules, 0 results); cppcheck analysis 1917859503 (58 rules, 0 results); CodeQL analysis 1917833477 (58 rules, 0 results). Open alerts on the PR merge ref: 0. The two open CodeQL alerts on master/branch head are the existing baseline (PWS-09), not new to this PR.

Gate behaviour (local dry runs on local-only branches, never pushed): (1) earlier final1 run under /workspace/pws07-scratch fails layering (NEW os->core edge), ratchet, CCN/cognitive/CRAP, diff-cover ~2%, clang-tidy on changed lines plus readability on an added header, and one cppcheck warning via diff-quality; untouched upstream findings are not gated. (2) wx-only and src/os/mac-only changes PASS and are listed as "Not measured: reviewed by hand". (3) a new src/core .cpp missing from the coverage report FAILs and names the file. (4) an unused inline in a new src/core header counts as uncovered (0/6 < 80%, FAIL); a declaration-only header is listed and PASSes.

Fred's coverage-gate points in gate_changed.py / coverage-gate.toml: single threshold line=80; per-metric hooks for branch and condition (commented); not_measured lists src/ui/, src/os/mac/, src/os/windows/; missing measured source fails; no exemption file (none of the ACs needs one).

Finding dispositions (also in the PR body): Codex P1 (diff-cover include did not recurse) fixed in 03e9a4e16; Codex P2 (uninstrumented header skipped) fixed in 03e9a4e16; first-run CI: core_st generation (868a89294) and SARIF security-severity string (8678778d7). clang-tidy, cppcheck, CodeQL and Socket: no new findings on this PR. AC 13 reviews by Fred Brooks and Dennis Ritchie are still outstanding; proposed residual risks remain in the PR body for Fred to log.

Recorded on master rather than the PR branch: first committed on the PR branch as aa542afb7, reverted there in fd4129b9c so PR #7 touches only .github/workflows/fork-*.yml and tools/quality/ (PR head content equals 03e9a4e16).
2026-10-08 (Fred Brooks, board sync): moved In Progress to Review. PR #7 is open at head fd4129b9c, every check on that head has passed (fork quality gate, coverage, clang-tidy, cppcheck, CodeQL, CMake builds on Ubuntu and Windows, both macOS builds, Socket), and Grace Hopper's verification evidence and finding dispositions are recorded above (1ed0a28). Still open before merge: AC 13 code reviews by Fred Brooks and Dennis Ritchie, residual risks from the PR body into backlog/docs/raid-log.md, then Edsger Dijkstra's QA.

2026-10-08 19:42 BST, Fred Brooks: code review of PR #7 at fd4129b9c - pass, with no blocking findings. The PR's net change against master (three-dot diff from merge base 07ee21502) is `.github/workflows/fork-quality.yml` plus 12 new files under `tools/quality/`. No `src/`, upstream workflow, `coverage.sh` or `backlog/` file changes; no inline suppression comment is added; nothing installs PMD, CPD, include-what-you-use, CodeChecker or SonarQube; and GitHub reports the PR merges cleanly. All 18 checks on fd4129b9c passed, and the merge ref has no open code-scanning alerts. Both Codex findings and the two first-run CI failures are fixed. The edge list matches decision-01's 39 edges, and `layering.py` passes with the single `PWSversion.cpp` allow entry. I checked the gate locally. Only line coverage is enforced, at 80%; branch and condition stay with PWS-23. `src/ui`, `src/os/mac` and `src/os/windows` are listed as not measured. A neutral edit to an existing function over the limit passes, and an edit that raises its complexity fails as a ratchet failure. Required before merge (sent to Grace): (1) pin the quality job's actions to commit SHAs, because it now holds `security-events: write` and that meets R-07's revisit condition; (2) make the gate scripts fail when clang-tidy, clang-tidy-diff or lizard exits non-zero and no findings were parsed; (3) drop the leading `./` from the duplication scan's vendored-code exclusions; (4) use the recursive `src/core/**` and `src/os/**` patterns in the README's local diff-cover command. Follow-up, not blocking: split the larger gate-script functions before PWS-23 extends `gate_changed.py`. RAID: R-07 and R-09 updated, and three new risks logged (macOS/Windows-only code unchecked on Linux; non-self-contained headers; platform-#ifdef code in measured core files). Still needed before merge: Dennis Ritchie's code review, Grace's four fixes with my re-check, and Edsger Dijkstra's QA.

PWS-07 code review (Dennis Ritchie) on fd4129b9c — 2026-10-08

Result: well-scoped and clean on security, layering and secrets; two fail-open defects in the gate scripts to address before merge, plus residual risks for the RAID log. Per Robert's rule each finding is fix-or-RAID, so this is a review with blockers, not a clean pass yet.

What holds:
- Scope (AC 9): confined to .github/workflows/fork-quality.yml and tools/quality/; no src/ change, no other workflow, no NOLINT/cppcheck-suppress added. 13 files, +1192/-1.
- Security: no pull_request_target, no secrets.*/token use; security-events: write (quality job only) is the one broad scope, needed for upload-sarif; checkout uses persist-credentials: false; cppcheck is tag-pinned and SHA-256-checked (checksum reproduced), not piped to a shell. Secret scan over all added lines clean.
- Layering: layering-edges.txt matches decision-01's 39 edges E1-E39 exactly; allow-list is the single PWSversion.cpp -> version.h. Local run at head passes.
- CI: all 18 checks green on fd4129b9c; code scanning 0 alerts across clang-tidy, cppcheck and CodeQL.

Address before merge (fix, or log in RAID with explicit acceptance):
1. Fail-open on tool crash. clang_tidy_gate.py never checks the exit codes of clang-tidy-diff/clang-tidy (only parses stdout); gate_changed.py never checks lizard's exit code. A crash or unparseable output yields no findings and the gate goes green. Should fail closed: check return codes and fail on non-zero.

RAID (residual risks to record, acceptable if logged):
2. CI has not exercised the failure paths — this PR changes no C/C++, so clang-tidy-diff, the added-file run, the coverage threshold, CRAP and the ratchet never ran with real input in CI; only evidence is local runs on unpushed branches. Capture that evidence or a canary in notes/RAID.
3. Coverage scope vs AC 2: AC 2 says src/core and src/os; the gate measures src/core, src/os/unix and top-level src/os/*.h, with src/os/mac and src/os/windows hand-reviewed (not compiled on Linux). Reconcile AC 2 wording or record the deviation.
4. Outside-fork PRs get a read-only token, so upload-sarif would fail and redden the job for outside contributors. Known limitation for a personal fork.
5. Dependency pinning: clang-tidy-18 via apt unpinned, pip exact versions without hashes, actions tag-pinned not SHA-pinned (matches the rest of the repo). Note as accepted.

Nits:
6. cppcheck_gate.py: if a SARIF file has no runs, rules is unset and the step NameErrors — fails closed (job red) so benign, but worth a guard.
7. README line 58 local example uses 'src/core/*' 'src/os/*' (non-recursive); the workflow uses **. Align the doc.
8. Squash-merge recommended: aa542afb7 (notes) + fd4129b9c (its revert) otherwise linger in history.

Still ahead: Fred's review, the RAID entries, and Edsger's QA.

2026-10-08 20:00 BST, Fred Brooks: delta re-check of PR #7 fd4129b9c..a40131b56 - pass, no blockers. The four quality-job actions are pinned to commit SHAs that each match their tag (codeql-action upload-sarif v4.38.2's annotated tag peeled to its commit); the coverage job's tag pins remain under R-07. clang_tidy_gate.py and gate_changed.py now fail with tool name, exit code and stderr when clang-tidy-diff, clang-tidy or lizard exits non-zero with no findings parsed. I reproduced this locally with fake tools for each call site, and controls behaved normally. The vendored exclusions now take effect (8817 to 8062 functions). README line 58 uses the recursive patterns, and the nits are in. The net diff still touches only fork-quality.yml and tools/quality/, all 18 check runs on a40131b56 succeeded, the PR is mergeable, and the merge ref has no open code-scanning alerts. Non-blocking follow-up: the gate_changed.py docstring and README tool table still say duplication "never fails", though a lizard crash now fails the job. Remaining before merge: Dennis's sign-off on the delta and Edsger's QA.

2026-10-08 20:02 BST, Grace Hopper: failure-path evidence for RAID (Dennis's review item 2). CI on PR #7 exercises no C/C++ change, so the failure paths have local evidence only. Local dry-runs (never pushed): (1) final1 under /workspace/pws07-scratch — layering FAIL (NEW os→core edge), complexity/CRAP FAIL (ratchet plus new-function limits), diff-cover FAIL, clang-tidy FAIL (changed-line findings plus readability on an added header), cppcheck FAIL via diff-quality; each EXIT non-zero as expected. (2) wx-only and src/os/mac-only changes PASS as not-measured. (3) a new src/core .cpp missing from the coverage report FAILs and names the file. (4) an unused inline in a new src/core header fails coverage (<80%); a declaration-only header PASSes. Crash-path negative tests at a40131b56: fake clang-tidy, clang-tidy-diff and lizard each exiting 1 with no output make the gate fail with tool name and exit code; a non-zero exit with parsed findings still takes the findings path. Lizard duplication scan: 8817 functions before exclusions, 8062 after (755 vendored excluded: pugixml 751, crypto/external 4).

2026-10-08 20:02 BST, Grace Hopper (housekeeping, at Dennis's request): Dennis's 19:46 review entry (cc944ff41) closes with a 'still ahead' line that predates Fred's review and RAID entries in cad23dcfa; those have landed. Dennis's item-1 blocker (fail-open on tool crash) was fixed in code at a40131b56. Follow-up for the next tools/quality change (likely PWS-23): update the gate_changed.py docstring and README tool table, which still say duplication 'never fails'.

PWS-07 code review follow-up (Dennis Ritchie) on a40131b56 — 2026-10-08

Result: item-1 blocker cleared; no blockers from me on a40131b56. (Supersedes the closing "still ahead" line of my fd4129b9c entry, which predated Fred's review and the RAID entries.)
- clang_tidy_gate.py now checks the exit codes of both clang-tidy-diff and clang-tidy; gate_changed.py checks every lizard call and uses zip(strict=True). A tool that crashes producing nothing parseable now fails the job instead of passing.
- Scope confined: delta fd4129b9c..a40131b56 is 5 files (fork-quality.yml SHA-pinning of the quality job's actions + the four tools/quality/ fixes); no src/, no other workflow, no new files; AC 9 holds. Secret scan clean (five action SHAs match their tags). All 18 checks green, mergeable.
- Also folded in: nit 6 (README diff-cover example now recurses), the cppcheck no-runs guard, and vendored-code exclusion from the duplication report.
- Residual for RAID (not blockers): the fail-closed check only fires when nothing was parsed, so a partial tool crash is still masked; and CI on this head did not exercise the new checks (no C/C++ changed), so fail-closed is evidenced by reading, not a run.

Remaining gate: Edsger's QA.

2026-10-08 20:45 BST, Edsger Dijkstra (QA): QA verdict on PR #7 at a40131b56 - the gate passes AC 1 to AC 12 (some with notes); AC 13 is still open, so not yet mergeable.

Result: every check I could run failed on an injected violation, named the function, file, line or rule and the limit, and passed again once the violation was removed. Legacy findings on unchanged lines did not fail it. I found no defect in the gate. AC 13 remains open on records only: three residual risks from Dennis's reviews have no disposition in the RAID log or these notes (see Blocker).

How I tested: PR head a40131b56 (matches GitHub), merge base with master 07ee21502. Work was done in my own worktree /workspace/edsger-pwsafe-qa7 and a scratch clone /workspace/edsger-pws07-neg with no remote, on local-only branches. Nothing was pushed and nothing was posted on GitHub. Tools: lizard 1.24.1, diff-cover 10.6.0 and gcovr 8.6 (the workflow's pins), cppcheck 2.17.1, and clang-tidy 19.1.7 (CI uses 18.1.3, which is not on the box). Each local run follows the workflow's steps with base a40131b56: a coverage build of coretest, Coretests, coverage.sh, then layering.py, gate_changed.py, diff-cover, clang_tidy_gate.py and cppcheck_gate.py. States: P2, a passing change (a neutral legacy edit, a readability pattern and a cppcheck style finding on changed lines, and a duplicated test); N, which is P2 plus the violations below; P3, P2 re-run after N. For CI, I read fork quality run 37826866671 (pull_request on a40131b56, 19:46 to 19:56 BST): both job logs, both artefacts, and the code-scanning analyses for refs/pull/7/merge.

| AC | Verdict | What I exercised |
|---|---|---|
| 1 | Pass with note | Run 37826866671 is a pull_request run on a40131b56, and its quality job ran. The configure log shows `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` and `CMAKE_EXPORT_COMPILE_COMMANDS:UNINITIALIZED=ON`. Both jobs carry `github.repository == 'rjbarbour/pwsafe'`. The skip in another repository was checked by reading only, as RAID A-01 already records. |
| 2 | Pass with note | A new function in src/core/Util.cpp FAILED with "CCN 12 > 10; cognitive complexity 21 > 15; CRAP 156.0 > 30". A separate uncovered function with CCN 6 and cognitive complexity 5 FAILED on "CRAP 42.0 > 30" alone. Changed-line coverage of 3/23 = 13.0% FAILED "below 80%", and 1/1 = 100% passed. Note: src/os/mac and src/os/windows are listed as "not measured: reviewed by hand" rather than measured (RAID R-13). |
| 3 | Pass | A neutral edit to legacy PWSprefs::SetMRUList (CCN 16, cognitive 12) was listed as changed, result "ok". A nested if FAILED it with "ratchet failure: modified CCN 16 -> 18" and "ratchet failure: cognitive complexity 12 -> 17". Untouched legacy functions over the limits in the same file were not listed. |
| 4 | Pass | `--list-checks` on the gate config gives 79 bugprone-, 35 cert- and 125 clang-analyzer- checks, and nothing else. rand() on a changed line FAILED via clang-tidy-diff (cert-msc30-c). An out-of-bounds write on a changed line FAILED via diff-quality (cppcheck error, "Quality is below 100"). Style and performance findings on changed lines were listed with "Fails: no", and P2, which contains one, passed. These did not fail: a pre-existing cppcheck error on an unchanged line of the modified Util.cpp, and 14 pre-existing gate-config clang-tidy findings on unchanged lines of the modified Util.cpp and PWSprefs.cpp. No readability- or modernize- check ran on modified files. A changed line in PWSprefs.cpp has a readability-implicit-bool-conversion finding (confirmed by running the new-files config on it directly), and the gate passed. |
| 5 | Pass with note | refs/pull/7/merge (d69310abb) has clang-tidy (312 rules) and cppcheck (58 rules) analyses from this run, uploaded by upload-sarif pinned to v4.38.2's commit. There are 0 results and 0 open alerts on the PR. Locally, state N's SARIF held its 5 clang-tidy and 4 cppcheck results with repository-relative paths and string security-severity. Not seen: an alert actually listed on a PR, because no PR has had a finding yet. |
| 6 | Pass with note | A duplicated test in src/test/UtilTest.cpp gave "changed src/test/UtilTest.cpp:37-47 duplicates src/test/UtilTest.cpp:24-34", and the run passed. Note: a second verbatim 18-line copy, in MRUListTest.cpp, was not reported. lizard's heuristic skips a block whose original already has repeated snippets. Duplication is report-only, so this can only under-report. The vendored exclusions now work: with the old `./` prefix lizard still scanned pugixml, and without it no vendored file appears. |
| 7 | Pass with note | A new `#include "../../core/UTF8Conv.h"` in src/os/unix/dir.cpp FAILED: "NEW edge (os to core) ... not in the edge list, so a design change for the architect or Fred Brooks". The second half (an edit to the edge list gets a design-change review) is a review rule. This PR creates the file, and Fred's review records that it matches decision-01. |
| 8 | Pass | I parsed decision-01's table and layering-edges.txt: 39 edges each, the same E-numbers, and the same pair for each number. layering.py at head finds 39 edges against 39 listed and passes. |
| 9 | Pass | See the scope check below. No NOLINT or cppcheck-suppress comment is added. Nothing installs or runs PMD, CPD, include-what-you-use, CodeChecker or SonarQube. |
| 10 | Pass | The allow list has exactly one entry, `src/core/PWSversion.cpp -> version.h`. An untracked, generated src/ui/wxWidgets/version.h (the Makefile.macos case) passed with 39 edges, and still passed with the allow list emptied. With version.h tracked under src/ui/wxWidgets, it is "allowed" with the entry and a NEW core-to-ui edge without it. So includes resolve against git ls-files, and the one entry is what keeps that include out. |
| 11 | Pass | The new-files config enables 50 readability- and 40 modernize- checks, and disables three, each with a reason. An added src/core/QaNewFile.cpp and QaNewHelper.h FAILED with four findings, each naming file, line and rule. An added .cpp that is in no CMakeLists, so not in compile_commands.json, was still analysed and FAILED. |
| 12 | Pass | An added file with readability-implicit-bool-conversion FAILED. The same rule on a changed line of the existing PWSprefs.cpp was not reported, and P2 passed. |
| 13 | Fail (open) | Code reviews by Fred and Dennis are recorded, as are Fred's delta re-check (20:00) and Dennis's follow-up on a40131b56. I confirmed Fred's four required fixes at a40131b56: the four action SHAs match their tags, crashes fail closed (below), the `./` prefix is gone, and the README patterns are recursive. All 18 checks on a40131b56 passed, with 0 code-scanning alerts on the PR. Missing: the three dispositions under Blocker. |

Scope check (Robert's merge authority for platform PRs): pass. The net diff from merge base 07ee21502 to a40131b56 has 13 files: M .github/workflows/fork-quality.yml, plus A tools/quality/.gitignore, README.md, clang-tidy-gate.yaml, clang-tidy-new-files.yaml, clang_tidy_gate.py, coverage-gate.toml, cppcheck_gate.py, gate_changed.py, gitdiff.py, layering-allow.txt, layering-edges.txt and layering.py. There is no src/ change and no upstream workflow change. Two commits outside the net diff: aa542afb7 touched this task file and fd4129b9c reverted it, so a squash merge keeps them out of master's history (Dennis's item 8).

Fail-closed and exit codes: a fake clang-tidy-diff, lizard, cppcheck or diff-quality that exits non-zero with no output each makes its step exit 1. The first two give "exited 3 with no findings parsed"; cppcheck fails with an exception, and diff-quality makes the step report "cppcheck: FAIL". layering.py exits 1 when git fails. In CI, the steps run under `bash -e -o pipefail` (from the job log), so the `| tee` keeps the exit status. Tools did run and analyse files in CI: layering scanned 250 files, cppcheck reported 1006 tree findings with 0 on changed lines, and the SARIF lists 312 and 58 rules. The judged diff was empty, because the PR changes no C/C++.

Blocker (AC 13; Fred to record before merge): give each of these a disposition in backlog/docs/raid-log.md or these notes:
(1) Dennis's fd4129b9c item 4: pull requests from other forks get a read-only token, so the SARIF upload step fails and turns the job red. The README mentions it, but there is no disposition.
(2) Dennis's item 5: R-07 covers the action pins, the clang-tidy-18 apt install and gcovr, but not lizard and diff-cover being pip-pinned without hashes.
(3) Dennis's a40131b56 residual: fail-closed only fires when nothing was parsed, so a partial crash is still masked.
Dennis's item 2 (CI never runs the failure paths) now has local evidence from Grace and from this QA. Fred decides whether it also needs a RAID line.

Other observations, none blocking: lizard can miss a duplicate (AC 6 note). The README's local commands write q/ and coverage/ into the repository root, and neither is ignored, so `git add -A` would pick them up; it nearly did in my scratch clone.

Not checked: the skip in another repository (read only); an alert listed on a PR; any macOS- or Windows-only code; clang-tidy 18 locally (I used 19); CodeQL, Socket and the build jobs beyond their check status.

/workspace/pwsafe was not touched: HEAD 19a7302f4 on codex/PWS-02-diceware-passphrase with a clean tree, both before and after.

Edsger Dijkstra (QA)

2026-10-08 20:45 BST, Fred Brooks: AC 13 decisions on Edsger's three residual risks from his QA at cd8a88143. (1) Outside-fork PRs get a read-only token, so the SARIF upload fails: logged as a new risk, accepted, low, because this fork takes no outside PRs. (2) lizard and diff-cover are version-pinned without hashes: folded into R-07 and accepted on the same basis as gcovr. (3) A partial tool crash can be hidden by the no-findings crash check: logged as a new risk, accepted, with a follow-up for PWS-23. Non-blocking follow-ups for PWS-23, so they don't change PR #7: lizard's duplicate report can miss some copies (it is report-only under AC 6); add a .gitignore rule for the README local run's `q/` and `coverage/` output; and fix the docstring and README wording that says duplication 'never fails'. PR #7 is to be squash-merged, so the add-then-revert notes commits don't reach master history. Remaining before merge: Dennis Ritchie's confirmation on a40131b56.
<!-- SECTION:NOTES:END -->

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
