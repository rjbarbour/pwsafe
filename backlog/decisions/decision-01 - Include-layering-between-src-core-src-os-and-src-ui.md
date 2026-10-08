---
id: decision-01
title: 'Include layering between src/core, src/os and src/ui'
date: '2026-10-08 13:09'
status: accepted
---
## Context

PWS-04. The fork quality gate (PWS-07) adds a layering check on `#include` edges. That check needs an agreed rule, not a script default. Upstream pwsafe has three source layers that matter here: `src/core` (the model, file formats and crypto), `src/os` (platform services) and `src/ui` (the Windows MFC and wxWidgets front ends). The intended direction is `ui` over `core` over `os`, but upstream already departs from it in a small, stable set of places, listed below. This fork adds features for upstream contribution and does not restructure upstream code.

An edge is a pair: the including file under `src/core` or `src/os`, and the header it includes, written as it appears in the source. The set was taken at fork `master` `f24fd88` by listing every `#include` in `src/core` and `src/os` and keeping those that reach `src/ui`, a `wx/` header, or (from `src/os`) a `src/core` header. That gives 39 edges. The set was checked against Grace Hopper's draft baseline and is identical. No unqualified include in `src/core` or `src/os` resolves to a header in another layer at `f24fd88`; `src/os/windows/yubi/YkLib.cpp`'s `"StdAfx.h"` resolves to its own directory's `stdafx.h`.

## Decision

1. **No file under `src/core` or `src/os` includes a header under `src/ui`.** The single exception is edge E1 below, the Windows MFC-only include of `../ui/Windows/stdafx.h` from `src/core/PwsPlatform.h`, guarded by `(_WIN32 || _WIN64) && !__WX__`. The check resolves include paths, so an unqualified include that would compile only because `src/ui/wxWidgets` is on the include path counts as an include of `src/ui`.
2. **The existing include cycle between `src/core` and `src/os` is accepted.** The 30 `src/os`-to-`src/core` edges E9 to E38 are the accepted set. **A new `src/os`-to-`src/core` edge fails the layering check.** `src/core` including `src/os` is the intended direction and is not checked.
3. **`src/core` and `src/os` take no new dependency on wxWidgets.** The 8 existing `wx/` edges are classified **allowed**: they are upstream code, guarded to non-Windows or wxWidgets builds (or unix-only for E39), and used only for string translation, precompiled headers, the MSVC debug CRT, and `wxExecute`. Any other `wx/` include under `src/core` or `src/os` fails the check.
4. **The check covers changes only.** Every listed edge is accepted as it stands. Nothing in this decision asks for upstream code to be refactored, and the fork does not remove any listed edge unless a tracked task needs it.
5. **The list is the authority.** The edge-list file used by the PWS-07 layering check must list exactly the edges in this record. Any change to either list, including an addition, removal, or a move caused by renaming a file, is a design change. The architect or Fred Brooks reviews it before it merges. A change to the list is recorded by superseding this decision, not by editing it.

### Edges at `f24fd88`

Counts: 1 `src/core` to `src/ui`, 7 `src/core` to `wx/`, 30 `src/os` to `src/core`, 1 `src/os` to `wx/`. Total 39. Line numbers are at `f24fd88` and are for checking only; the edge is the file and header pair.

| # | Source file | Line | Included header | Classification |
|---|---|---|---|---|
| E1 | `src/core/PwsPlatform.h` | 47 | `../ui/Windows/stdafx.h` | core to ui: allowed, the only exception (Windows MFC build only) |
| E2 | `src/core/StringX.cpp` | 19 | `wx/intl.h` | core to wx: allowed (existing) |
| E3 | `src/core/XML/Pugi/PFileXMLProcessor.cpp` | 20 | `wx/wxprec.h` | core to wx: allowed (existing) |
| E4 | `src/core/XML/Pugi/PFileXMLProcessor.cpp` | 23 | `wx/wx.h` | core to wx: allowed (existing) |
| E5 | `src/core/XML/Pugi/PFileXMLProcessor.cpp` | 27 | `wx/msw/msvcrt.h` | core to wx: allowed (existing) |
| E6 | `src/core/XML/Pugi/PFilterXMLProcessor.cpp` | 21 | `wx/wxprec.h` | core to wx: allowed (existing) |
| E7 | `src/core/XML/Pugi/PFilterXMLProcessor.cpp` | 24 | `wx/wx.h` | core to wx: allowed (existing) |
| E8 | `src/core/XML/Pugi/PFilterXMLProcessor.cpp` | 28 | `wx/msw/msvcrt.h` | core to wx: allowed (existing) |
| E9 | `src/os/KeySend.h` | 21 | `../core/StringX.h` | os to core: accepted cycle |
| E10 | `src/os/UUID.h` | 30 | `../core/StringX.h` | os to core: accepted cycle |
| E11 | `src/os/file.h` | 13 | `../core/StringX.h` | os to core: accepted cycle |
| E12 | `src/os/mac/KeySend.cpp` | 11 | `../../core/UTF8Conv.h` | os to core: accepted cycle |
| E13 | `src/os/mac/UUID.cpp` | 17 | `../../core/Util.h` | os to core: accepted cycle |
| E14 | `src/os/mac/UUID.cpp` | 18 | `../../core/StringXStream.h` | os to core: accepted cycle |
| E15 | `src/os/mac/debug.cpp` | 131 | `../../core/StringX.h` | os to core: accepted cycle |
| E16 | `src/os/mac/file.cpp` | 30 | `../../core/core.h` | os to core: accepted cycle |
| E17 | `src/os/mac/file.cpp` | 31 | `../../core/Util.h` | os to core: accepted cycle |
| E18 | `src/os/mac/file.cpp` | 32 | `../../core/StringXStream.h` | os to core: accepted cycle |
| E19 | `src/os/mac/file.cpp` | 33 | `../../core/PwsPlatform.h` | os to core: accepted cycle |
| E20 | `src/os/mac/macsendstring.cpp` | 18 | `../../core/PwsPlatform.h` | os to core: accepted cycle |
| E21 | `src/os/run.h` | 21 | `../core/StringX.h` | os to core: accepted cycle |
| E22 | `src/os/typedefs.h` | 31 | `../core/PwsPlatform.h` | os to core: accepted cycle |
| E23 | `src/os/unix/KeySend.cpp` | 15 | `../../core/Util.h` | os to core: accepted cycle |
| E24 | `src/os/unix/KeySend.cpp` | 16 | `../../core/PWSprefs.h` | os to core: accepted cycle |
| E25 | `src/os/unix/UUID.cpp` | 17 | `../../core/Util.h` | os to core: accepted cycle |
| E26 | `src/os/unix/UUID.cpp` | 18 | `../../core/StringXStream.h` | os to core: accepted cycle |
| E27 | `src/os/unix/debug.cpp` | 72 | `../../core/StringX.h` | os to core: accepted cycle |
| E28 | `src/os/unix/file.cpp` | 36 | `core/core.h` | os to core: accepted cycle |
| E29 | `src/os/unix/file.cpp` | 37 | `core/StringXStream.h` | os to core: accepted cycle |
| E30 | `src/os/unix/file.cpp` | 38 | `core/Util.h` | os to core: accepted cycle |
| E31 | `src/os/unix/xsendstring.cpp` | 44 | `../../core/PwsPlatform.h` | os to core: accepted cycle |
| E32 | `src/os/unix/xsendstring.cpp` | 45 | `../../core/StringX.h` | os to core: accepted cycle |
| E33 | `src/os/unix/xsendstring.h` | 17 | `../../core/StringX.h` | os to core: accepted cycle |
| E34 | `src/os/windows/UUID.cpp` | 17 | `../../core/Util.h` | os to core: accepted cycle |
| E35 | `src/os/windows/UUID.cpp` | 18 | `../../core/StringXStream.h` | os to core: accepted cycle |
| E36 | `src/os/windows/debug.cpp` | 15 | `../../core/util.h` | os to core: accepted cycle (resolves to `Util.h` on case-insensitive file systems) |
| E37 | `src/os/windows/debug.cpp` | 85 | `../../core/StringX.h` | os to core: accepted cycle |
| E38 | `src/os/windows/file.cpp` | 32 | `../../core/core.h` | os to core: accepted cycle |
| E39 | `src/os/unix/run.cpp` | 14 | `wx/process.h` | os to wx: allowed (existing, unix only) |

To check any edge: `git grep -n '#include' f24fd88 -- <source file>`.

## Alternatives considered

- **No layering check; rely on review.** Rejected. Review catches design drift but not a stray include, and the cost of a script is small.
- **Directory-level rules with no edge list** (for example "os may include core"). Rejected. It would accept every new `src/os`-to-`src/core` include and so grow the cycle silently.
- **Remove the existing edges first.** Rejected. It is refactoring upstream code that no fork task needs, and it would make upstream contributions harder to review.
- **An off-the-shelf action** (archcheck, cpp-include-insight, cpp-dependencies, link-what-you-include, Archie). Not adopted at `f24fd88`: each was either immature, without enforced layer rules, diagnostic only, or needed changes to upstream's build. PWS-07 may revisit this if the tool can enforce exactly this record.

## Consequences

- A fork change that adds an include from `src/os` into `src/core`, from `src/core` or `src/os` into `src/ui`, or from `src/core` or `src/os` into `wx/`, fails the gate. The author either restructures the change or asks for a design change to this record.
- Renaming or moving a listed source file changes its edges and so needs the same review. That is rare in a fork that tracks upstream, and the review is cheap.
- Upstream code merged from `pwsafe/pwsafe` can add edges outside the fork's control. When a sync brings new edges, they are reviewed as a design change and the record is superseded with the new list; the sync is not blocked by default.
- The record and the edge-list file are fork-only (`backlog/` and the PWS-07 tooling) and never enter an upstream pull request.

## What would reverse this decision

- Upstream restructures the layers (for example, moves `StringX` and its relatives below `src/os`, or drops the MFC build that needs E1), so that the listed edges no longer describe the code.
- Upstream adopts its own layering rule or check. The fork then follows upstream's rule instead of this one.
- The edge list changes often enough that its reviews block legitimate work. A coarser rule would then replace the pair-level list.
- A maintained tool can enforce exactly these rules from a committed configuration without changes to upstream's build. The tool would replace the script, not the rules.
- The fork stops tracking upstream, at which point a deliberate restructuring would replace accepting the existing edges.
