# Native MD European Union restored

> Historical rollback record. The subsequent adaptation was also removed. The [main MD EU restoration record](../main_md_eu_restore/README.md) describes the current active state.

Status: restored on 18 October 2026 at the user's request. This supersedes the CWEC implementation and design documents in this directory.

The active game uses the original Millennium Dawn European Union interface, Council and Parliament proceedings, elections, offices, reform decisions, budget allocation and membership effects. The custom seven-tab CWEC interface, human-only political docket, historical proposal catalogue, programme financing, EIB extensions and custom membership modifiers have been removed from the game directories. Native MD political voting and AI behaviour apply again.

Nine modified files were returned to their pre-CWEC repository versions. The five CWEC hook sites in `MD_on_actions.txt` were removed selectively, preserving the unrelated Cold War civil-war and yearly-event safeguards. Existing national currency support and the preexisting historical euro date restriction were retained. Other countries' work was preserved.

This restores the native MD ruleset, including its modern membership, institutional defaults and progression. It does not retain the custom historical 1970 institutions or finances.

## Verification

- No CWEC files or references remain under the active `common`, `events`, `interface` or `localisation` directories.
- The original GUI, voting handlers, triggers, decisions, events, membership idea and interface localisation were checked against the Workshop reference: 15 files match byte for byte.
- The restored script and interface files pass the structural parser.
- All 73 unrelated tracked local changes present during the rollback retained their previous file hashes.
- All 21 reviewed original Workshop files retained their previous hashes; no Workshop files were written.
- The newest restored interface has not been visually tested in a running game.

The machine-readable inventory is [native_restore_report.json](native_restore_report.json). The old implementation, generators, validators and affected files before restoration are preserved in the ZIP named in that report. The remaining `tools/europe_1970/check_original_md_reference.py` is a read-only reference checker; it cannot reinstall CWEC.

## Starting the restored system

Fully exit and restart Hearts of Iron IV, then start a **new campaign**. Existing CWEC saves contain altered membership, proposal arrays and the `EU_initialized` flag, which prevents the original startup from rebuilding its initial state. No save migration was performed.
