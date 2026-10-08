---
id: PWS-02
title: Diceware passphrase button on add/edit dialog (EFF long list)
status: In Progress
assignee:
  - '@dennis-ritchie'
created_date: '2026-10-08 11:40'
updated_date: '2026-10-08 11:42'
labels: []
dependencies: []
references:
  - 'https://github.com/rjbarbour/pwsafe'
modified_files:
  - src/core/Passphrase.h
  - src/core/Passphrase.cpp
  - src/core/EffLongWordlist.cpp
  - src/core/EffLongWordlist.inc
  - src/core/eff-long-wordlist.txt
  - src/core/EFF-LONG-WORDLIST-NOTICE.txt
  - src/core/CMakeLists.txt
  - src/test/CMakeLists.txt
  - src/test/PassphraseTest.cpp
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
- The button on AddEditPropSheetDlg uses DrawWithRangeRand on the EFF long list (7776 words, CC BY notice in src/core) and writes the password and confirmation fields, never the clipboard.
- A word-count spin sits beside Generate, default 6, range 1 to 99.
- An entropy line shows count x log2(7776) (6 words = 77.5 bits).

Exclusions: Generate, CPasswordCharPool and PWPolicy untouched; no file-format change; no new crypto or RNG; no clipboard write.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given the add/edit dialog is open with an empty password and the word-count spin at 6, when the user clicks Passphrase, then the password field holds six lowercase words joined by single hyphens
- [ ] #2 Given the word-count spin is set to 4, when the user clicks Passphrase, then the password field holds four lowercase words joined by single hyphens
- [ ] #3 Given the spin is at 6, then the entropy line shows 6 x log2(7776), not a larger figure that assumes the word list is secret
- [ ] #4 Given Pronounceable is selected, when the user clicks Generate Password, then the existing pronounceable generator runs, unaffected by this change
- [ ] #5 Given Easy Vision is selected, when the user clicks Generate Password, then the existing easy-vision generator runs, unaffected by this change
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
State 2026-10-08: implementation commit 4cbd3bb "[wx] Add an EFF long-list passphrase beside Generate" on local branch `passphrase`, based on master 3996b15. Local-only: not pushed, no pull request.
Intended branch per Tracked Work SOP GT-03: codex/PWS-02-diceware-passphrase (existing branch `passphrase` not yet renamed).
Evidence so far: three PassphraseTest cases reported passing in the Linux coretest on 2026-10-04 (not rerun on 4cbd3bb). Linux add/edit dialog check on 2026-10-04: six lowercase hyphenated words in password and confirmation, new phrase per click, 77.5 bits at 6 and 51.7 at 4, clipboard empty. Not accepted.
Open points:
- Spin cap: code creates range 1 to 99; the Linux dialog run reported 1 to 100. Confirm before PR.
- Three tracked files under Misc/wxWidgets_VS_Updates/build/msw/ show deleted in the working tree, unexplained; not part of this task and must not be committed.
- Word list is committed twice (eff-long-wordlist.txt and EffLongWordlist.inc); for review.
- Pronounceable and Easy Vision scenarios (AC 4 and 5) not yet checked.
- Dialog run on Robert's Mac pending.
- Push, pull request on the fork and CI (build, CodeQL) pending; GitHub command line on the box is not signed in.
- V3test.psafe3 in the repo root stays untracked.
Next action: Dennis confirms the spin cap and resolves the deleted Misc files, then pushes once GitHub sign-in works.

Branch base (per PWS-01 decision, Robert Barbour, 2026-10-08): this branch is upstream-bound and is based on upstream master (3996b15), not on fork `master`. It skips the Tracked Work SOP GT-03A rebase onto fork `master`; synchronise it against upstream master before review or pull request. Its diff must contain no backlog/, backlog.config.yml or AGENTS.md.
<!-- SECTION:NOTES:END -->
