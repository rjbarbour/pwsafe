---
id: doc-02
title: Test strategy
type: other
created_date: '2026-10-08'
---

# Test strategy: rjbarbour/pwsafe fork

**Status: draft.** Awaiting Robert Barbour's approval (PWS-22 AC 14). Open points: Grace Hopper owns the coverage runner and compiler (AC 3); Robert Barbour owns the macOS coverage choice (AC 9).

This is the fork's test policy for implementers, reviewers and QA. New code under the measured tree must meet 100% line, branch and condition coverage, with parameter and boundary tests, unit tests, automated UAT, and light integration tests only around key interfaces. There is no obligation to raise coverage of existing code. Gates that enforce the bar are implemented elsewhere (PWS-07, PWS-18 or a new task); this document defines the policy only.

## 1. Test pyramid

```mermaid
flowchart TB
  mac["Robert's Mac run<br/>manual UAT on the dmg"]
  gui["GUI checks<br/>Linux/GTK AT-SPI harness"]
  integ["Light integration tests<br/>inside coretest"]
  unit["coretest unit tests<br/>GoogleTest in src/test"]
  mac --> gui --> integ --> unit
```

| Level | What belongs here | Who / what runs it | Platforms |
|---|---|---|---|
| Unit (coretest) | Pure logic, policies, prefs behaviour, fail-closed paths, parameter and boundary cases | `coretest` (GoogleTest under `src/test`), via `ctest -R Coretests` or the `coretest` binary | Linux (CMake in `cmake-build.yml`; coverage in fork-only `fork-quality.yml`); macOS (`macos-latest.yml`, `macos-cmake-latest.yml`) |
| Light integration | Wiring across a small number of already-tested units (see §7) | Same `coretest` run as unit tests | Same as unit |
| GUI checks | Dialog behaviour traced to a task's acceptance criteria | QA harness at `/workspace/qa-dialog-check` (off-repo; AT-SPI / pyatspi under Xvfb; scratch `HOME` so `pwsafe.cfg` starts at first run) | Linux/GTK only |
| Robert's Mac run | User-visible UI and platform-native behaviour before merge | Robert Barbour, from the `.dmg` built by the macOS workflow | macOS only |

Most new behaviour is proved at the bottom. GUI checks confirm the dialogs wire to that behaviour. The Mac run covers what Linux cannot see.

## 2. New-code coverage bar

**Bar:** 100% line, branch and condition coverage of new code.

**New code:** the lines a pull request adds or changes against its merge base (whole new files, plus changed lines in existing files).

**Measured tree:** code that coretest instruments — `src/core` and `src/os` as filtered by `tools/quality/coverage.sh` (vendored `src/core/pugixml` and `src/core/crypto/external` excluded). See §5 for files that are not measured.

### How each metric is measured

| Metric | Tool and command | Report field / note |
|---|---|---|
| Line | gcovr 8.6 via `tools/quality/coverage.sh` (`--json`, Cobertura, text summary); changed-line line hits may also be checked with diff-cover | gcovr JSON per-line `count` |
| Branch | same gcovr run, with `--exclude-throw-branches` and `--exclude-unreachable-branches` (see §4) | gcovr JSON per-line `branches` |
| Condition | same gcovr run after a GCC 14+ build with `-fcondition-coverage` | gcovr JSON per-line `conditions` (`conditionno`, `count`, `covered`, `not_covered_false`, `not_covered_true`); gcovr passes `gcov --conditions` when the gcov tool supports it ([gcovr 8.6 JSON output](https://gcovr.com/en/8.6/output/json.html); [gcovr FAQ — gcov options](https://gcovr.com/en/stable/faq.html)) |

diff-cover can enforce changed-line **line** coverage only. Branch and condition coverage on changed lines is enforced by the gate script reading gcovr JSON (Grace Hopper's plan: extend `gate_changed.py` in PWS-07).

### Runner and compiler (open point — Grace Hopper)

Condition coverage needs **GCC 14 or later** (`-fcondition-coverage`). The current coverage job in `.github/workflows/fork-quality.yml` runs on `ubuntu-latest` (today ubuntu-24.04) with **GCC 13** (configure log of run 37787860322 shows GNU 13.3.0).

Grace Hopper's recommendation (2026-10-08): move the coverage job to the **`ubuntu-26.04`** runner (GCC 15.2), add `-fcondition-coverage` in `coverage.sh`, use a gcovr that reports conditions, and re-take the coverage baseline once after the move. Until she confirms the runner and compiler, this remains an **open point owned by Grace Hopper**.

## 3. Boundary and parameter policy

Every new function with a numeric or enumerated input is tested at each boundary and just outside it, and with a parameterised test over each equivalence class.

**Worked example — PWS-02 `PassphraseWordCount` (allowed range 1..99):**

- Boundaries and just outside: 0, 1, 2, 98, 99, 100
- Parameterised equivalence classes: below range, in range, above range

For an enumerated input: every defined value, plus one invalid value.

## 4. Branch exclusions in the coverage report

The branch (and, once available, condition) measure uses gcovr's:

- `--exclude-throw-branches`
- `--exclude-unreachable-branches`

**Why:** those are compiler-generated exception and unreachable branches that cannot be exercised meaningfully from tests. Without them the 100% branch figure is noise.

The coverage summary reports the excluded count so every report means the same thing. **No other coverage exclusions** are used. Any exemption is a reasoned entry in a reviewed file under `tools/quality/`, only for judgement calls in modified `src/core` or `src/os/unix` files — never a standing list of UI files.

## 5. What the coverage bar does and does not measure

The 100% bar applies only to code coretest instruments. New `src/ui` and `src/os/mac` files are **not measured**. The coverage report lists them as:

> not measured (GUI or platform wiring, reviewed by hand)

They must not be left out silently, and the strategy must not be read as if GUI or platform code meets the 100% bar.

A changed file under `src/core` or `src/os/unix` that the coverage job is meant to measure but which is **missing from the coverage report fails the coverage gate**. It is not treated as covered or skipped. That catches a new file coretest never builds or links.

## 6. Layering policy (testability)

New decision logic lives in `src/core`, or in `src/os` code that the Linux coretest build compiles (`src/os/unix`). `src/ui` and `src/os/mac` hold thin wiring only. That is what makes the 100% bar reachable without driving the GUI.

**Allowed:** the dialog makes the existing Default Policy comparison and passes the result to `GenerateMakesPassphrase(useLocalPolicy, entryOnSafeDefault)` in `Passphrase.h`, then acts on the answer.

**Disallowed:** the dialog itself branching on the switch and the policy to decide whether to make a passphrase. The same rule applies in `src/os/mac`: no decision logic that belongs in core.

GUI checks and Robert's Mac run exercise the wiring; they do not substitute for coretest coverage of the decision.

## 7. Light integration tests

Integration tests are warranted **only around key interfaces, to confirm wiring**. They are not used to reach coverage of logic that belongs in unit tests.

Interfaces that qualify in this codebase:

- V3 save/reload carriers (for example `FileV3Test`)
- `PWSprefs` ↔ `pwsafe.cfg`
- Passphrase generation ↔ the injected `PWSrand` draw (and injected word list where used)
- Dialog → core decision function (the dialog supplies inputs; the decision stays in core and is unit-tested)

## 8. Automated UAT and Robert's Mac run

**Automated UAT** for this fork means the Linux/GTK GUI checks. They live off-repo under `/workspace/qa-dialog-check`, are driven with AT-SPI (pyatspi) under Xvfb on their own display and D-Bus session, and use a scratch home directory (`HOME=/tmp/qa-dialog-home` and matching XDG paths) so `pwsafe.cfg` starts at first run. QA runs them per task; each check is traced to that task's acceptance criteria. Screenshots may be taken for layout. The harness does not modify the git tree.

**Robert Barbour's Mac run** is required for any user-visible UI change before he decides on the merge, and specifically for platform-native behaviour:

- native spin-control events (typed value without arrows)
- macOS location of `pwsafe.cfg` (the run names the file it checked)
- clipboard clearing on minimise
- a cheap screenshot for layout

It is run from the `.dmg` built by the macOS workflow (`PasswordSafe-macOS*.dmg`). The result is recorded in the task notes with date, build/commit, what was checked, and the result.

## 9. macOS-only code coverage (open point — Robert Barbour)

The macOS workflows run coretest but measure no coverage today.

Two options:

| Option | What it does |
|---|---|
| **(a)** Fork-only macOS coverage job | Runs only when a pull request changes `src/os/mac`; uses Apple clang / llvm-cov |
| **(b)** Not measured | Listed in the report as not measured; reviewed by hand by both code reviewers (Fred Brooks and Dennis Ritchie) plus Robert's Mac run |

**Recommendation (Edsger Dijkstra): (b).** The layering rule keeps decision logic out of `src/os/mac`, so there is little to measure; the Mac workflows already run the full coretest; and (a) adds a second toolchain for a job that would rarely trigger. If a pull request ever needs real logic in `src/os/mac`, that is a design exception and the trigger to add (a).

Until Robert chooses, this is an **open point owned by Robert Barbour**. His answer is recorded in the PWS-22 task notes.

## 10. Existing code

Existing code carries **no obligation** to raise coverage. When a pull request changes existing lines, its notes state which changed lines are covered and why any are not, and both code reviewers (Fred Brooks and Dennis Ritchie) accept that.

## 11. Gate map

Policy → check → blocks or advises → workflow → implementing task.

| Policy | Check | Blocks / advises | Workflow | Implementing task |
|---|---|---|---|---|
| 100% line / branch / condition on new code (changed lines) | `gate_changed.py` reads gcovr JSON (and may use diff-cover for line); raise PWS-07 AC 2 from 80% changed lines to 100% line, branch and condition | Blocks | `.github/workflows/fork-quality.yml` | **PWS-07** (extend `gate_changed.py`; raise AC 2) |
| Condition coverage enabled in the report | Build with `-fcondition-coverage`; gcovr JSON `conditions` populated | Blocks once the bar is live (report must carry the data the gate reads) | `fork-quality.yml` + `tools/quality/coverage.sh` | **PWS-18 or a new task** (PWS-18 today only raises the suspicious-hits threshold; condition-coverage flags need an AC extension or a new task) |
| Coverage accuracy (suspicious hits counted) | `--gcov-suspicious-hits-threshold` in `coverage.sh` | Advises accuracy of the report the gate reads | `fork-quality.yml` + `coverage.sh` | **PWS-18** |
| Throw / unreachable branch exclusions | `--exclude-throw-branches`, `--exclude-unreachable-branches`; excluded count in summary | Blocks (defines what 100% branch means) | `coverage.sh` | **PWS-18 or a new task** (same coverage.sh change set) |
| Not-measured labelling for `src/ui` / `src/os/mac` | Report lists those changed files as not measured (reviewed by hand) | Blocks if omitted silently | `fork-quality.yml` / gate script | **PWS-07 or a new task** |
| Missing measured file fails | Changed file under `src/core` or `src/os/unix` absent from the coverage report → fail | Blocks | `fork-quality.yml` / gate script | **PWS-07 or a new task** |
| Judgement exemptions | Reasoned entry in a reviewed file under `tools/quality/`, modified `src/core` / `src/os/unix` only | Blocks misuse (no standing UI exclude list) | `tools/quality/` | **PWS-07** (exemption file owned with the gate) |
| Mac coverage if Robert picks (a) | Fork-only macOS coverage job on `src/os/mac` changes | Blocks when that job is required | new `fork-*.yml` | **New task** |
| Mac coverage if Robert picks (b) | Hand review + Mac run; not-measured label | Advises (review and Mac run recorded in notes) | none (process) | No gate task; recorded under AC 9 / task notes |
| Automated UAT (GUI checks) | QA harness run traced to ACs | Advises (evidence in task notes); does not replace coretest | off-repo harness | Per feature task (no separate gate workflow) |
| Robert's Mac run | Notes: date, build/commit, checks, result | Advises merge decision | macOS workflow artefact | Per feature task |

This document does not implement any of those gates.
