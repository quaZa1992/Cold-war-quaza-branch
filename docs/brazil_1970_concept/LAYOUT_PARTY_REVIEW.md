IMPERIA COLD WAR

# Brazil 1970 layout and party integration review

**Reviewer:** `/root/md_structure`  
**Scope:** Read-only audit of the approved concept against emitted focus, scripted trigger, scripted localisation, party decision, leader, and native integration sources. The one authorised generator edit described under Leader callback diagnosis is recorded separately; no shared integration file was changed.

## Focus layout and reward graph

The approved source is `concept.json` (SHA-256 `0b14031fbad84b84ad72a1599e47cf444a3b52523bcc26070c8f7fd94bc55875`). I parsed every top-level focus in `common/national_focus/COLDWAR_BRA_1970_focus.txt`, resolved each `relative_position_id` recursively, and compared absolute coordinates, prerequisite groups, and mutually exclusive references with the approved nodes.

| Measure | Approved | Emitted | Result |
|---|---:|---:|---|
| Focuses | 224 | 224 | Exact ID match |
| Focus groups | 18 | 18 | All roots present |
| Absolute node coordinates | 224 | 224 | 0 differences |
| Prerequisite groups and references | 224 | 224 | 0 differences |
| Exclusion pairs | 45 | 45 | 0 differences |
| Extra or missing concept focuses | 0 | 0 | None |

Forty-six nodes use a prerequisite group with OR alternatives; fifteen have multiple prerequisite groups joined by AND. The emitted blocks preserve these groupings and edges. The native shortcut list contains eight entries. Existing static checks report no unreachable focus, title overflow, or connector crossing a third-party card.

I visually inspected `PREVIEW_OVERVIEW.png`, `PREVIEW_POLITICAL_NEIGHBOURS.png`, `PREVIEW_military.png`, and `PREVIEW_prn.png`. The overview reads as a single compact tree with clearly separated political, domestic, security, and diplomatic programmes. Political branches retain the intended shared outlook identities while following their own coordinates and reward routes. The military and PRN examples show legible card spacing and native-style connector routing. These files are static reconstructions, not in-game screenshots.

## Party identity and requirements

The emitted triggers in `common/scripted_triggers/COLDWAR_BRA_1970_politics.txt` check the native ruling slot plus the exact registered identity for ARENA/PDS, MDB/PMDB, historic PTB, later PTB, PDT, PT, PFL, PSDB, and PRN. PCB and PCdoB require their own legalisation or explicit alternate-accession flag; the Lacerdist branch requires the active movement and, after Lacerda's death, congressional successor authorization. The military branch checks native slot 22. All thirteen political in-power trigger tooltips resolve to English localisation.

The ARENA/PDS and MDB/PMDB tooltip names are selected from the current identity variable, so a PFL or PSDB identity cannot appear as the required predecessor. The remaining tooltips use the specific registered party keys: historic PTB `party_3_1`, later PTB `party_3_2`, PDT `party_3_3`, PT `party_3_4`, PFL `party_1_3`, and PSDB `party_2_3`. PCB and PCdoB use their full English party names. No tooltip uses the current slot label as a substitute for a different future organisation.

`common/decisions/COLDWAR_BRA_1970_politics.txt` contains 24 valid category decisions: 11 formation decisions, 12 congress nomination decisions, and the separate Lacerdist continuity authorization. Congress decisions change only the registered identity variable and displayed party name; they do not assign the ruling slot. The focus branches stay visible, with the exact party trigger used for availability and rewards.

The shared native registry slots remain distinct: 22 is the Armed Forces; 1 contains ARENA, PDS, and PFL identities; 2 contains MDB, PMDB, and PSDB; 3 distinguishes historic PTB, later PTB, PDT, and PT; slots 4 and 19 are PCB and PCdoB; and slot 20 distinguishes the Lacerdist movement and PRN. No replacement of the existing 24 native slots was found in the Brazil party helpers. Formation gates require the authorised constitutional/party opening and real predecessors for the PFL and PSDB splits. Early alternative party reorganisation under a meaningful reform is intentional and is not treated as a historical-date defect.

## Leader callback diagnosis

The initial isolated native run recorded 59 of 81 assertions passing, with `mdb_real_leader` and `pt_real_leader` failing. The fixture switches parties through `change_ruling_party_effect`, which invokes the global `set_leader` effect. Its Brazil early branch created the correct named candidates, but returned before the generic `update_set_politics` call. The engine's numeric `ruling_party` slot therefore changed while its native ideology group could remain on the previous government; `has_country_leader { ruling_only = yes }` correctly rejected the new candidate. The saved error log recorded creation of Ulysses Guimarães, confirming that registration and callback reachability were not the problem.

I added a scoped native `update_set_politics = yes` call to the generated Brazil leader helper, before candidate selection. It temporarily sets the native `no_leader_change` guard and preserves an already-set guard. This maps the actual numeric party slot to the engine's corresponding ideology group before the helper creates the elected party's named leader, without retiring or killing Médici. The regenerated native fixture then passed all 114 of 114 assertions, including both leader assertions, with no feature diagnostics.

## Shared marker ownership

The compiled Brazil early-leader clause now sits outside Chile's `COLDWAR_CHL_EARLY_LEADER_BEGIN` / `COLDWAR_CHL_EARLY_LEADER_END` region, immediately before the generic fallback in `common/scripted_effects/00_leader_setup_scripted_effects.txt`. Chile's region contains only its own route. This removes the overlapping marker ownership that could have let a future Chile regeneration overwrite the Brazil clause.

## Verification boundary

The final native fixture is isolated under `D:/HOI4_Mod_Tools/mdcoldwar/runtime/brazil_1970/20261102_124504_878168`. The package report verifies all 29 frozen runtime files against the sources used by the native run, with no runtime drift or package errors. I also ran `compile.py --check`; it reported `changed: []`. The leader portrait callback uses the neutral portrait fallback when no exact local portrait exists and applies the Trial of Allegiance Prestes portrait only when that DLC is available. No DLC image was copied into the mod. No in-game focus hover or multiplayer claim is made here.
