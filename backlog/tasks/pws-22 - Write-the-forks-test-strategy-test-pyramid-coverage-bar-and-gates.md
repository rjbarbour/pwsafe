---
id: PWS-22
title: 'Write the fork''s test strategy (test pyramid, coverage bar and gates)'
status: To Do
assignee:
  - '@edsger-dijkstra'
created_date: '2026-10-08 16:32'
labels:
  - docs
  - test
dependencies: []
type: chore
ordinal: 22000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Robert Barbour set the fork's test policy on 2026-10-08. New code needs 100% line, branch and condition coverage, with parameter and boundary tests, unit tests and automated UAT, and light integration tests only around key interfaces to confirm wiring. There is no obligation to raise coverage of existing code, and judgement applies in modified files. Edsger Dijkstra writes it up as `backlog/docs/test-strategy.md`, a tracker-only change committed straight to fork `master` with no pull request, and Robert approves it. Out of scope: implementing gates (PWS-18 or a new task does that), changing any workflow, `src/` or `tools/` file, and raising coverage of existing code.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given `backlog/docs/test-strategy.md` on fork `master`, when it is read, then it defines the fork's test levels as a pyramid (at least coretest unit tests, light integration tests, GUI checks on the dialogs, and Robert Barbour's Mac run), and for each level states what belongs there, what runs it and on which platforms
- [ ] #2 Given the document, when it is read, then it states the new-code coverage bar as 100% line, branch and condition coverage, defines new code as the lines a pull request adds or changes against its merge base, and names the tool and command that measure each of the three
- [ ] #3 Given the document, when it is read, then it states that condition coverage needs GCC 14 or later while CI uses GCC 13, and it records the measurement option Grace Hopper confirms; until she confirms, it names that as an open point with Grace as owner
- [ ] #4 Given the document, when it is read, then it states the boundary and parameter policy: every new function with a numeric or enumerated input is tested at each boundary and just outside it, with a parameterised test over each equivalence class, using PWS-02's word count of 1 to 99 as a worked example
- [ ] #5 Given the document, when it is read, then it states the layering policy: new decision logic lives in `src/core`, where coretest can reach it, and GUI code may contain only wiring that the GUI checks and Robert Barbour's Mac run exercise; it gives one allowed and one disallowed example, so a reviewer can tell whether a given branch in a dialog is allowed
- [ ] #6 Given the document, when it is read, then it defines automated UAT for this fork (GUI checks on Linux/GTK traced to a task's acceptance criteria) and Robert Barbour's Mac run, saying when the Mac run is required, naming the platform-native behaviours that need it (at least native spin-control events, the macOS location of `pwsafe.cfg` and clipboard clearing on minimise), and saying how its result is recorded in task notes
- [ ] #7 Given the document, when it is read, then it states when integration tests are warranted (only around key interfaces, to confirm wiring), names the interfaces that qualify in this codebase, and states that integration tests are not used to reach coverage of logic
- [ ] #8 Given the document, when it is read, then it states that existing code carries no obligation to raise coverage, and that when a pull request changes existing lines, its notes state which changed lines are covered and why any are not, and both code reviewers accept that
- [ ] #9 Given the document, when it is read, then it maps each policy to a gate (the check, whether it blocks or advises, and the workflow it belongs in) and names whether PWS-18 or a new task implements each gate
- [ ] #10 Given the document, when Robert Barbour has read it, then the task notes record his approval, or the changes he asked for and the commit that made them, with the date and the commit he approved
- [ ] #11 Given the commits for this task, when they are inspected, then they change only `backlog/docs/test-strategy.md` and this task's file, each carries the PWS-22 ID, and no `src/`, `.github/` or `tools/` file changes
<!-- AC:END -->
