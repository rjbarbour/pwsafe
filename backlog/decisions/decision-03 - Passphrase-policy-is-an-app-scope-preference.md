---
id: decision-03
title: Passphrase policy is an app-scope preference (Option A)
date: '2026-10-08 17:04'
status: accepted
---
## Context

PWS-02. Robert Barbour tested PR #2 (head `5beca97`) on his Mac and asked for the passphrase choice, word count and strength line to move off the entry's Basic tab, to be set once rather than per entry, and asked whether passphrase generation could be a policy alongside the existing password policies, and at which level.

Password Safe stores password policies in the safe file at three levels: per entry (the `POLICY` field, or `POLICYNAME` for a named policy), as named policies (the `HDR_PSWDPOLICIES` header) and as the database default (database-scope preferences in the file's preferences header). There is no group-level policy. A `PWPolicy` is a set of character-class flags plus lengths in a fixed 19-character encoding, and the unused flag bits belong to upstream pwsafe/pwsafe's file format. Application-scope preferences (`ptApplication`) are stored by name in the local `pwsafe.cfg`, not in the safe.

Two options were set out:
- **A:** passphrase generation is an application preference on this Mac. No change to `PWPolicy` or the file format.
- **B:** passphrase is a new policy type stored in the safe, using an unused `PWPolicy` flag bit, at entry, named and default level.

Owner decision: Robert Barbour, 2026-10-08 17:04 BST, Option A now; B designed but not built.

## Decision

1. **The passphrase setting is application scope.** Two `ptApplication` preferences are added to `PWSprefs`: a switch and a word count. Names, default and range are set in PWS-02's acceptance criteria. They are stored in the local configuration file, never in the safe.
2. **No change to the safe file.** No `PWPolicy` flag, no new field type, no new database-scope preference, no change to `HDR_PSWDPOLICIES` or the preferences header. A safe saved with the switch on is the same as one saved with it off.
3. **The setting lives in Preferences.** `OptionsPropertySheetDlg` gets a password-generation section with the choice "Use the safe's password policy" or "Use this Mac's policy" (Diceware with a word count and its strength in bits). The passphrase controls are removed from the entry's Basic tab.
4. **Generate follows the switch.** `AddEditPropSheetDlg::OnGenerateButtonClick` calls `MakePassphrase` when the switch selects this Mac's policy, and otherwise keeps the existing `PWPolicy::MakeRandomPassword` path. `Passphrase.h/.cpp` and the word list are unchanged.
5. **Precedence: pending Robert Barbour's confirmation.** Proposed: an entry's own policy or a named policy wins; this Mac's policy replaces only the safe's default policy. Until Robert confirms it in PWS-02's acceptance criteria, this point is not decided. If he chooses otherwise, this record is superseded, not edited.

## Alternatives considered

- **B: passphrase as a policy type stored in the safe.** Deferred, not rejected. It gives per-entry, per-named-policy and per-safe passphrase policy that travels with the file, but it claims a flag bit in upstream's file format. Older and other Password Safe builds would not understand it, and an older wx build would drop the bit when the policy is edited. It needs upstream's agreement on the bit before it is built. Its full design is a separate decision record under its own task, with no code.
- **Leave the controls on the entry's Basic tab (PR #2 at `5beca97`).** Rejected by the owner after testing: the choice must be set once, not per entry.

## Consequences

- No file-format change, so safes stay readable and editable as before in the Windows build, upstream builds and other Password Safe apps such as Huvisoft's pwSafe.
- No upstream agreement is needed, and syncing with upstream stays cheap.
- The setting is per Mac. It does not travel with the safe, and other machines and apps do not generate passphrases from it.
- It is not on the Password Policy page. Manage Password Policies edits the safe's own policies, and a per-Mac switch there would mislead.
- Tests: a core test that saving a safe with the switch on writes the same preferences header and policies as with it off; a test that both preferences are `ptApplication`; characterisation tests of existing policy generation first; GUI checks that Generate follows the switch and the precedence rule.
- Easy to reverse: removing the two preferences and the Preferences section leaves no trace in any safe.

## What would reverse this decision

- Upstream pwsafe/pwsafe agreeing a passphrase policy type and flag bit, at which point B supersedes this record.
- Robert Barbour needing the passphrase choice to travel with the safe or to differ per entry or per safe.
- Robert Barbour choosing a different precedence rule (supersedes point 5 only).
