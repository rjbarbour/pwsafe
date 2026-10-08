---
id: PWS-02
title: Diceware passphrase button on add/edit dialog (EFF long list)
status: Shaping
assignee:
  - '@dennis-ritchie'
created_date: '2026-10-08 11:40'
updated_date: '2026-10-08 13:27'
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
type: feature
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Milestone 1 of Diceware passphrase generation in Password Safe (wxWidgets, macOS target). A small change shaped for upstream pwsafe/pwsafe.

Outcome: in the add/edit entry dialog, a Passphrase button beside Generate fills the password and confirmation fields with a Diceware passphrase drawn from the EFF long word list.

Agreed design:
- `MakePassphrase(list, count, draw)` returns StringX and draws with replacement; it does not call RangeRand itself.
- The button on AddEditPropSheetDlg uses DrawWithRangeRand on the EFF long list (7776 words) and writes the password and confirmation fields, never the clipboard. `src/core/EffLongWordlist.inc` is the only copy of the list; its header gives EFF's source URL and the SHA-256 of EFF's file. The list is CC BY 4.0 International (EFF copyright policy, https://www.eff.org/copyright): the notice is `docs/EFF/EFF-LONG-WORDLIST-NOTICE.txt`, shipped in the Mac dmg via `install/macosx/Makefile`, and listed in `install/deb/copyright.debian`. The About box is unchanged (Barbara Liskov, 2026-10-08).
- The word-count spin and the entropy line sit on their own row in the existing add/edit dialog, aligned like the other fields, not on the password row (Robert Barbour, 2026-10-04). Spin default 6, range 1 to 99.
- An entropy line shows count x log2(7776) (6 words = 77.5 bits).

Exclusions: Generate, the password field, CPasswordCharPool and PWPolicy unchanged; no new dialog or toolkit; no file-format change; no new crypto or RNG; no clipboard write; no dialog test on the branch.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the add/edit dialog is open with an empty password and the word-count spin at 6, when the user clicks Passphrase, then the password field holds six lowercase words joined by single hyphens
- [ ] #2 Given the word-count spin is set to 4, when the user clicks Passphrase, then the password field holds four lowercase words joined by single hyphens
- [ ] #3 Given the spin is at 6, then the entropy line shows 6 x log2(7776), not a larger figure that assumes the word list is secret
- [ ] #4 Given Pronounceable is selected, when the user clicks Generate Password, then the existing pronounceable generator runs, unaffected by this change
- [ ] #5 Given Easy Vision is selected, when the user clicks Generate Password, then the existing easy-vision generator runs, unaffected by this change
- [ ] #6 Given the add/edit dialog is open, then the word-count spin and the entropy line sit on their own row, aligned like the other fields in that dialog, and not on the password row; Generate, the password field and the policy controls are where they were; no new dialog is opened
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
<!-- SECTION:NOTES:END -->
