---
id: PWS-02
title: >-
  Diceware passphrase generation as an app-scope Preferences setting (EFF long
  list)
status: Shaping
assignee:
  - '@dennis-ritchie'
created_date: '2026-10-08 11:40'
updated_date: '2026-10-08 16:37'
labels: []
dependencies: []
references:
  - 'https://github.com/rjbarbour/pwsafe'
modified_files:
  - src/core/Passphrase.h
  - src/core/Passphrase.cpp
  - src/core/EffLongWordlist.cpp
  - src/core/EffLongWordlist.inc
  - docs/EFF/EFF-LONG-WORDLIST-NOTICE.txt
  - install/macosx/Makefile
  - install/deb/copyright.debian
  - src/core/CMakeLists.txt
  - src/core/Makefile
  - src/core/core-15.vcxproj
  - src/core/core-15.vcxproj.filters
  - src/core/core-16.vcxproj
  - src/core/core_wx-15.vcxproj
  - src/core/core_wx-15.vcxproj.filters
  - Xcode/pwsafe-xcode6.xcodeproj/project.pbxproj
  - CodeBlocks/core/core.cbp
  - CodeLite/core.project
  - src/test/CMakeLists.txt
  - src/test/PassphraseTest.cpp
  - src/test/coretest-15.vcxproj
  - src/test/coretest-15.vcxproj.filters
  - src/test/coretest-16.vcxproj
  - src/ui/wxWidgets/AddEditPropSheetDlg.cpp
  - src/ui/wxWidgets/AddEditPropSheetDlg.h
  - src/core/PWSprefs.h
  - src/core/PWSprefs.cpp
  - src/ui/wxWidgets/OptionsPropertySheetDlg.h
  - src/ui/wxWidgets/OptionsPropertySheetDlg.cpp
type: feature
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Milestone 1 of Diceware passphrase generation in Password Safe (wxWidgets, macOS target). A small change shaped for upstream pwsafe/pwsafe.

Outcome: the user sets once, in Preferences, whether Generate Password uses the safe's password policy or this computer's policy (a Diceware passphrase from the EFF long word list, with a word count). The entry's Basic tab carries no passphrase controls.

Design: recorded in decision-03 "Passphrase policy is an app-scope preference (Option A)" (Barbara Liskov, accepted by Robert Barbour, 2026-10-08). In short:
- Two new `ptApplication` preferences in `PWSprefs.h/.cpp`: bool `UseLocalPassphrasePolicy` (default false) and int `PassphraseWordCount` (default `kDefaultPassphraseWords`, 6; min 1, max 99). Both are appended at the end of `BoolPrefs` and `IntPrefs` so no existing enum value moves (database preferences are written by enum index). They are saved by name in the local `pwsafe.cfg`, never in the safe.
- Preferences (`OptionsPropertySheetDlg`) gets a new "Password Generation" page, built by a new `OptionsPropertySheetDlg::CreatePasswordGenerationPanel`, placed straight after Password History and reusing Password History's icon (image index 3); no new artwork. It offers "Use the safe's password policy" or "Use this computer's policy". This computer's policy means Diceware, with the word count and a bits line showing count x log2(7776) (6 words = 77.5 bits).
- `AddEditPropSheetDlg::OnGenerateButtonClick` calls `MakePassphrase` with the `PWSrand` draw (DrawWithRangeRand) when `UseLocalPassphrasePolicy` is on, and otherwise keeps the existing `PWPolicy::MakeRandomPassword` path, subject to the precedence rule (AC 13). The passphrase goes through the existing Generate tail: clipboard copy with the existing clear-on-minimise and timeout handling, password and confirmation fields, strength meter. No new clipboard code. An empty result shows the existing "Couldn't generate password - invalid policy" message, with no new strings and nothing copied. The word list is compiled in, so an empty result needs impossible input (empty list, zero word count or failed draw).
- PR #2's Passphrase button, word-count spin and bits line come off the Basic tab.
- Carried over unchanged from PR #2: `MakePassphrase(list, count, draw)` (returns StringX, draws with replacement, does not call RangeRand itself, fails closed with an empty result), `Passphrase.*`, `EffLongWordlist.*` (`src/core/EffLongWordlist.inc` is the only copy of the list; its header gives EFF's source URL and the SHA-256 of EFF's file), the EFF notice `docs/EFF/EFF-LONG-WORDLIST-NOTICE.txt` (CC BY 4.0 International, shipped in the Mac dmg via `install/macosx/Makefile`, listed in `install/deb/copyright.debian`), the existing tests, and the unchanged About box.
- Rework on the same branch and PR #2 (Robert's ruling); Ken Thompson implements, Fred Brooks and Dennis Ritchie review.

Exclusions: no `PWPolicy`, `PWCharPool` or `CPasswordCharPool` change; no database-scope preference; no file-format change (no policy flag, no field type, no change to `HDR_PSWDPOLICIES` or the preferences header); no existing preference enum value moves; entry Policy tab and Manage Password Policies unchanged; no new clipboard code, no new user-visible error string, no new artwork; other Preferences pages and their order unchanged apart from the new page; no new dialog or toolkit; no new crypto or RNG; no change to `Passphrase.*` or `EffLongWordlist.*`. Option B is out of scope (PWS-19).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the core characterisation tests of existing policy behaviour, added as the first commit on the pull request branch, before any rework commit, when coretest runs on that commit, on the pull request head and on upstream `3996b15`, then they pass at all three points, the task notes name both commits, and they cover: (a) `PWPolicy::MakeRandomPassword` for a normal character-class policy that uses all four classes (lowercase, uppercase, digits, symbols) with non-trivial minimum counts, asserting the length and that each class meets its minimum; the bare default policy; Pronounceable; Easy Vision; hex digits only; and a policy with a custom symbol set, asserting that only that set's symbols appear; and (b) save and reload through V3 for four carriers, an inline per-entry policy (field 0x10), an entry that references a named policy (field 0x18), a named policy in the header, and the safe's default policy, asserting for each that the flags, the length and every minimum count are unchanged after reload
- [ ] #2 Given the reserved-bit characterisation tests, which pin current behaviour as at 3b7afd068 (`PWPolicy.cpp` lines 79 to 91) and do not describe desired behaviour, when coretest runs on the commit that adds them, which is the first commit on the pull request branch, before any rework commit, and on the pull request head and on upstream `3996b15`, then they pass at all three points and show that a reserved or unknown flag bit set alongside character classes round-trips untouched, and that a reserved bit set alongside UseHexDigits parses to an empty policy
- [ ] #3 Given the new preferences `UseLocalPassphrasePolicy` (bool, default false) and `PassphraseWordCount` (int, default `kDefaultPassphraseWords` = 6, min 1, max 99), when QA reads their definitions in `PWSprefs.cpp` and runs the core test that checks them, then both are `ptApplication`, neither is `ptDatabase`, their defaults and limits are as stated, and the test passes
- [ ] #4 Given `PWSprefs.h` on the pull request head and on upstream master (3996b15), when QA compares the `BoolPrefs` and `IntPrefs` enums (by a core test or a diff check recorded in the task notes), then `UseLocalPassphrasePolicy` is the last value before `NumBoolPrefs`, `PassphraseWordCount` is the last value before `NumIntPrefs`, and every existing value in both enums keeps its position
- [ ] #5 Given a safe saved once with `UseLocalPassphrasePolicy` on and once with it off, with the same entries and policies, when the core test compares the two saved files after reloading them through V3, then the preferences header and the named and default password policies are identical
- [ ] #6 Given Preferences is open, when QA looks at its pages, then a "Password Generation" page sits straight after Password History, shows Password History's icon, and every other page is present in its existing order
- [ ] #7 Given the "Password Generation" page on first run, when QA looks at it, then it offers exactly "Use the safe's password policy" and "Use this computer's policy", "Use the safe's password policy" is selected, and the word-count control and bits line are disabled until "Use this computer's policy" is selected
- [ ] #8 Given "Use this computer's policy" is selected, when the user sets the word count, then it accepts 1 to 99, defaults to 6, and the bits line shows count x log2(7776) to one decimal place (6 words shows 77.5 bits), not a larger figure that assumes the word list is secret; typing a number without the arrows updates the bits line to agree with the count
- [ ] #9 Given the user has selected "Use this computer's policy" and a word count of 4, clicked OK and quit Password Safe, when Password Safe is restarted and a different safe is opened, then the page still shows "Use this computer's policy" with 4 words, `pwsafe.cfg` holds `UseLocalPassphrasePolicy` and `PassphraseWordCount` by name with those values, and neither safe file has changed
- [ ] #10 Given "Use this computer's policy" with 6 words, and an entry whose Policy tab uses the safe's default policy, when the user clicks Generate Password, then the password field (and the confirmation field when the password is hidden) holds six lowercase words from the EFF long list joined by single hyphens (counted as entries of the EFF long list, not by splitting on hyphens, since four list words, `drop-down`, `felt-tip`, `t-shirt` and `yo-yo`, contain a hyphen themselves), the strength meter updates, and the clipboard holds the same passphrase, cleared on minimise and after the timeout exactly as for the existing Generate; the diff adds no clipboard code
- [ ] #11 Given `MakePassphrase` is called with an empty word list, a word count of zero, or a draw that fails, when the core test runs, then each call returns an empty result; and given the Generate handler receives an empty passphrase, when QA reads the diff (the word list is compiled in, so this cannot be triggered from the GUI), then it shows the existing "Couldn't generate password - invalid policy" message, adds no new user-visible string, and writes nothing to the clipboard or the password fields
- [ ] #12 Given "Use the safe's password policy" is selected, when the user clicks Generate Password with each of the default, Pronounceable and Easy Vision policies, then the existing generator runs for that policy, unaffected by this change
- [ ] #13 Given "Use this computer's policy" is selected, when the user clicks Generate Password on an entry whose Policy tab uses the safe's default policy, then a Diceware passphrase of the configured word count from the EFF long list is generated; and when the user clicks Generate Password on an entry whose Policy tab uses the entry's own policy or a named policy, then the existing generator runs with that entry or named policy and no passphrase is generated (an entry's own policy or a named policy wins; this computer's policy replaces only the safe's default policy, as decision-03 point 5 proposed and Robert Barbour confirmed on 2026-10-08)
- [ ] #14 Given the add/edit dialog is open for a new or an existing entry, when QA looks at the Basic tab, then there is no Passphrase button, no word-count spin and no bits line; Generate, the password field and its row are where they were before PR #2
- [ ] #15 Given the add/edit dialog is open for an entry, when QA looks at the Policy tab and edits the entry's own and named policy there, then its controls and behaviour are the same as on upstream master (3996b15)
- [ ] #16 Given the pull request head, when coretest runs on Linux CMake and in the macOS workflow, then it passes with no test skipped or removed, and the existing Passphrase tests are unchanged
- [ ] #17 Given the pull request, when its coverage report is read, then new code it adds under `src/core` has 100% line coverage, 100% branch coverage and 100% condition coverage, as Robert Barbour set on 2026-10-08, whether or not `backlog/docs/test-strategy.md` (PWS-22) has been approved by then (once approved, it defines how these are measured); and new code under `src/ui` is listed as not measured (GUI wiring, reviewed by hand) rather than left out
- [ ] #18 Given the pull request diff, when it is inspected, then the passphrase bits figure and its one-decimal formatting, and the generate decision (a function taking plain values for whether "Use this computer's policy" is selected and whether the entry is on the safe's default policy, and returning whether to generate a passphrase), are functions in `src/core/Passphrase.h` and `src/core/Passphrase.cpp` with no wx types, each with its cases in `src/test/PassphraseTest.cpp`; and the dialog code calls these functions and contains no branching of its own beyond wiring
- [ ] #19 Given the GUI checks for this task, when each run starts, then it uses a scratch home directory, so `pwsafe.cfg` starts in its first-run state and the tester's own configuration is not read or changed; and the task notes record, for each run, the scratch path used and that `pwsafe.cfg` did not exist at its start
- [ ] #20 Given the pull request for this task, when it is merged, then Fred Brooks and Dennis Ritchie have each recorded a code review, and every automated-check finding on it (CI, CodeQL, the fork quality gate or any other check) has been addressed by disabling or tuning the rule, suppressing it in code within this task's limits, mitigating or fixing it, or recording the residual risk in `backlog/docs/raid-log.md`, and the pull request or task notes say which for each finding
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
State 2026-10-08: pull request #2 on branch codex/PWS-02-diceware-passphrase. The evidence below was taken on db9dab1. The head has since moved to 5beca97: ea519ea (lint fixes) and 5beca97 (one-line fix to the EFF notice text). No evidence is claimed for ea519ea or 5beca97 yet.
Evidence on db9dab1:
- Linux CMake coretest 129/129 (Dennis Ritchie and Edsger Dijkstra).
- Linux/GTK dialog check 27/27 in Add Entry and Edit Entry (Edsger Dijkstra).
- AC 4 and 5 (Pronounceable and Easy Vision) from Edsger Dijkstra's 3902dfe run, carried forward by Fred Brooks because nothing under src/ui changed after 3902dfe apart from the spin size.
- Barbara Liskov's design review of db9dab1 found nothing blocking (below).
Pending on 5beca97: macOS workflow runs and CodeQL (Grace Hopper), and the Linux/GTK dialog check. Then Robert's run on his Mac.
Open points:
- Three tracked files under Misc/wxWidgets_VS_Updates/build/msw/ show deleted in the working tree, unexplained; not part of this task and must not be committed.
- Word list: one copy since db9dab1, `EffLongWordlist.inc`; `eff-long-wordlist.txt` removed (Barbara Liskov ruling, 2026-10-08).
- V3test.psafe3 in the repo root stays untracked.

Branch base (per PWS-01 decision, Robert Barbour, 2026-10-08): this branch is upstream-bound and is based on upstream master (3996b15), not on fork `master`. It skips the Tracked Work SOP GT-03A rebase onto fork `master`; synchronise it against upstream master before review or pull request. Its diff must contain no backlog/, backlog.config.yml or AGENTS.md.

Design review of PR #2 at db9dab1 (Barbara Liskov, architect, 2026-10-08). Covers the design only, not Fred's code review or Edsger's QA. Read from the PR diff; nothing built or run.
Conforms to the rulings:
- The draw is the seam. `Passphrase.h` declares `PassphraseDraw` and does not include `PWSrand`. Only the dialog adapts `PWSrand::RangeRand`, which has the same signature. `MakePassphrase` checks `nWords == 0` before it draws, so "n is never zero" holds. It fails closed: an out-of-range draw or a null or empty word returns empty and keeps nothing partial.
- No `CPasswordCharPool` inheritance. `PWPolicy`, `PWCharPool`, `PWSrand` and the file format are untouched, and no preference is added.
- The handler is thin. It uses Generate's guard (Validate, TransferDataFromWindow, not an alias), writes `m_Password` (a StringX) and the confirmation when hidden, then updates the meter. It doesn't touch the clipboard, logging or the policy. OnUpdateUI disables the spin and the button exactly as it disables Generate.
- No class was extracted. The dialog diff is the new controls, two handlers and rows moved down two (growable row 18 to 20).
- `EffLongWordlist.inc` is the only copy, with EFF's URL and SHA-256 in its header. `static_assert`s pin the count at 7776. All five build systems list the new files, and Xcode lists the .inc as text that isn't compiled.
- The EFF credit follows the Yubico pattern: `docs/EFF` is on the dmg DOCS line, the Debian file has a `Files:` stanza for CC-BY-4.0, and the About box is unchanged.
Findings (none block the design):
1. The notice is stale. Its last line, `docs/EFF/EFF-LONG-WORDLIST-NOTICE.txt`, still describes the deleted .txt ("One lowercase word per line"). Suggested wording: "Dice prefixes are not included; the list is compiled into Password Safe from src/core/EffLongWordlist.inc." This is a one-line doc fix, but it changes what the dmg ships, so Fred decides whether it goes in with any fix from the evidence or as the only post-evidence commit.
2. The PR text should name two deliberate differences from Generate so the maintainer doesn't read them as oversights. Passphrase doesn't copy to the clipboard, and it shows no error box because an empty result is only possible for impossible input.
3. Mac check for Robert's run: type a number into the spin, without the arrows, then click Passphrase. The word count and the entropy line should agree. Only EVT_SPINCTRL updates the entropy line, and when a native spin control sends that event while someone is typing varies between platforms.
4. For the maintainer's judgement, not a change now: `PassphraseEntropyLine` builds UI text, including "bits", in core, so it can't be translated through _(). It's acceptable for milestone 1. If upstream asks, the formatting moves to the dialog and core keeps `PassphraseEntropyBits`.
Verdict: db9dab1 implements the agreed design. No ADR is needed and nothing here changes a contract.

2026-10-08 14:27 BST: Robert tested the 5beca97 dmg on his Mac; the feature works, but he wants the passphrase controls off the Basic tab and set once as a policy-level setting. PR #2 stays open and unmerged for rework on the same branch; the core (MakePassphrase, word list, notice, tests) carries over. Criteria to be rewritten once Robert picks where the setting is saved. Moved back to Shaping by Fred Brooks.

2026-10-08 (Fred Brooks): The State, evidence, pending and open-point notes above, about db9dab1 and 5beca97, the Basic-tab Passphrase design and Barbara Liskov's design review of PR #2, are superseded by the Option A rewrite in e21da4bd1, and so are their references to old AC 4 and AC 5 (Pronounceable and Easy Vision, now covered by AC 12). They stay as history. Precedence (decision-03 point 5: an entry's own or named policy wins, and this computer's policy replaces only the safe's default) was confirmed by Robert Barbour on 2026-10-08; it is AC 13, and the confirmation is recorded on decision-03 in ad3d2c165. Still current: the branch-base rule (upstream master 3996b15, no fork-only files in the diff); the three deleted Misc/wxWidgets_VS_Updates files must not be committed; and V3test.psafe3 stays untracked (now locally ignored, RAID R-11).

DoR check 2026-10-08 (Fred Brooks, Definition of Ready v1.3) on the Option A rewrite (e21da4bd1): fail on four blocking gaps; status unchanged (Shaping). Inputs: decision-03 (274487c8e, with the confirmation in ad3d2c165), the design in the description, Robert Barbour's new-code coverage bar (100% line, branch and condition coverage, 2026-10-08) and Barbara Liskov's ruling that new decision logic goes in small pure functions in src/core, covered by coretest, with only thin glue in the dialogs.
Checked and met: AC 13 matches decision-03 point 5 in substance. The ACs cover characterisation tests before any behaviour change (AC 1), reserved-bit characterisation (AC 2), the ptApplication test (AC 3), enum positions (AC 4), an unchanged saved file with the switch on (AC 5 in core, and AC 9's 'neither safe file has changed'), the empty-result message with nothing copied (AC 11), first-run defaults (AC 7), removal of PR #2's Basic-tab UI (AC 14), and the Policy tab unchanged (AC 15). The standard merge AC is last (AC 17). RD-01, RD-02, RD-04 and RD-07 are explicit. No vulnerability detail, CodeQL specifics or generator internals beyond the design seam appear.
Gap 1, blocking (RD-03, coverage evidence): there is no AC for Robert's bar. Proposed new AC, placed before the merge AC: 'Given the pull request head, when coretest is built with GCC 14 or later using --coverage and -fcondition-coverage and gcovr reports on the lines this pull request adds or changes under src/core, then line, branch and condition coverage of those lines are each 100%; the task notes record the three figures, the compiler and gcovr versions and the report; no coverage-exclusion marker is added; and any line that cannot be covered goes to Fred Brooks for Robert Barbour's decision rather than being excluded.' Dependency: condition coverage needs GCC 14 or later, but the PWS-05 job compiles with GCC 13.3.0 on ubuntu-latest. Either measure on the team box (GCC 14.2) and record that, or raise a platform task with Grace Hopper to add condition coverage to the coverage job. That also bears on PWS-07, whose AC 2 sets 80% of changed lines.
Gap 2, blocking (RD-02 and RD-06, design boundary): Barbara's ruling is not in the ACs. The bits-line figure and text already exist as pure core functions (PassphraseEntropyBits and PassphraseEntropyLine in Passphrase.*, carried over unchanged). The generate decision (which generator runs, given the switch and whether the entry uses its own, a named or the safe's default policy) does not. Proposed new AC: 'Given the pull request diff, when QA reads it, then the generate decision for AC 13 is a pure function in a new src/core file with no wx dependency, covered by a coretest case for each combination of the switch and the policy source; the bits line on the Password Generation page comes from PassphraseEntropyLine; and OnGenerateButtonClick and the Password Generation page only call these functions and act on their results.'
Gap 3, blocking (RD-06, file list): modified_files lacks the new src/core files for the generate decision (names for the implementer and Barbara, for example src/core/PassphrasePolicy.h and src/core/PassphrasePolicy.cpp) and the new core test files for AC 1 to 5 and gap 2 (for example src/test/PWPolicyTest.cpp, src/test/PWSprefsTest.cpp and src/test/PassphrasePolicyTest.cpp). They also need adding to every build list already named (src/core CMakeLists.txt, Makefile, core-15/16 and core_wx-15 vcxproj(.filters), the Xcode project, CodeBlocks and CodeLite), and to src/test/CMakeLists.txt and coretest-15/16.vcxproj(.filters).
Gap 4, blocking (RD-03, starting conditions): no AC sets up a scratch pwsafe.cfg for Edsger Dijkstra's GUI checks. Without one, 'first run' in AC 7 cannot be set up reliably, AC 9 reads whichever real config the tester has, and the checks would overwrite a real user's preferences. Proposed new AC: 'Given Edsger Dijkstra's GUI checks for AC 6 to AC 10 and AC 12 to AC 15, when he runs Password Safe, then he starts it with -g <scratch path> (--config_file), where the file does not exist before AC 7, reuses the same scratch file across the restart in AC 9, never uses a real user's pwsafe.cfg, and records the scratch path in the task notes.'
Non-blocking: (1) 3b7afd068 exists only on the local branch passphrase in /workspace/pwsafe (5beca97 plus one commit) and not on PR #2's branch, which is at 5beca97. It should be pushed to codex/PWS-02-diceware-passphrase before handover. AC 2 could read 'as at upstream 3996b15 (src/core/PWPolicy.cpp is unchanged at 3b7afd068)'. (2) Reaching 100% condition coverage of Passphrase.* may need new tests; AC 16 keeps the existing Passphrase tests unchanged, so new tests go in a new test file. (3) RD-06: add 'After Edsger's QA, a fresh CI dmg goes to Robert Barbour for a run on his Mac, and merging PR #2 is his decision.' (4) The label is 'Use this computer's policy', while decision-03 says 'this Mac's'; the neutral wording suits upstream, so note it as deliberate. (5) RD-05: name the commitment; Build is the project default, and this work is security-sensitive and upstream-bound.
<!-- SECTION:NOTES:END -->
