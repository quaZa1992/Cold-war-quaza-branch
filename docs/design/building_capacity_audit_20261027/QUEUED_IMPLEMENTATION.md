IMPERIA COLD WAR: Five reviewed queued-construction corrections

Implemented 2026-10-28 as direct building awards within the requested capacity repair. Each focus keeps its existing duration, price, rewards and receipt. The additional civilian-factory construction wait is removed. No construction-permission or later MD technology is installed.

| Focus | State | Direct award | Fee, unchanged | Focus duration, unchanged |
|---|---:|---|---|---:|
| COLDWAR_GRE_1970_economy_18 | 139 | infrastructure +1, slot +1 | 1.5% current GDP | 56 days |
| COLDWAR_VIE_kiet_transport | 523 | infrastructure +1, slot +1 | 0.06 billion | 70 days |
| COLDWAR_VIE_industry_roads | 524 | infrastructure +1, slot +1 | 0.06 billion | 70 days |
| COLDWAR_VIE_farm_dykes | 522 | infrastructure +1, slot +1 | 0.05 billion | 70 days |
| COLDWAR_VIE_army_airdefence | 522 | anti_air_building +1, slot +1 | 0.06 billion | 70 days |

All five transactions require real state ownership/control and room under the loaded physical building ceiling. Every original party, leader, predecessor, funding and once-only check remains. Each adds its same-state slot before the building. Failed implementation remains unpaid and can use the existing country retry. Both focus and retry contain complete nonexecuting native costs, programme changes, XP where applicable, slots and buildings while locked. Other focuses, shared-slot projects, province construction and immutable approvals were not rebuilt.

Native choice: private retry04 ran591.23seconds with33 component checks,28 positives, zero fixture errors and no crash. Its five counterexamples rejected two instant_build=no API assumptions and three reservation-safety assumptions. set_building_level ignored the non-instant request. include_locked did not bypass missing nonshared permission. Private minimal permissions enabled genuine queued infra/AA completion, but free_building_slots ignored queued reservations and allowed a fee despite the second order being capped at level6. The permission route was therefore rejected. The original33-check result remains native_pass=false; this report does not relabel it as an entirely passing suite.

The diagnostic queue_permissions.py now contains only the private provider functions needed to reproduce that rejected candidate. No production module imports it and neither candidate technology/localisation provider exists in the loaded mod. Full frozen fixtures and native logs remain on E:, not in this repository.

Validation:11 focused emitted transaction, locked-preview, canonical-parity and CAS-race cases pass. ISR10, GRE radar5 and quality6, VIE transactions21 and campaigns21 also pass. A bounded dry run reports no further changes. The updater snapshots every source before writing, stages changed files, then atomically replaces individual files after a second complete preflight. Existing source notices are retained when adding required project markers. Replacement-block indentation is normalised; unrelated focus blocks stay byte-identical.

The canonical sources are tools/greece_1970/compile.py and tools/vietnam_1970/compile.py plus reward_rework.py. Only these actual loaded paths were updated for the five contracts:

- common/national_focus/COLDWAR_GRE_1970_focus.txt
- common/scripted_effects/COLDWAR_GRE_1970_tree_effects.txt
- common/decisions/COLDWAR_GRE_1970_tree_decisions.txt
- common/national_focus/COLDWAR_VIE_1970_focus.txt
- common/scripted_effects/COLDWAR_VIE_1970_effects.txt
- common/decisions/COLDWAR_VIE_1970_decisions.txt
- localisation/english/COLDWAR_GRE_1970_tree_l_english.yml: existing project marker preserved.
- localisation/english/COLDWAR_VIE_1970_l_english.yml: exact project marker and one national-programmes category description corrected.

The JSON records exact current hashes for all eight runtime files and the canonical/test providers. Two broader existing validator limits remain separate: the old Greek validator expects removed Cyprus focus COLDWAR_GRE_1970_cyprus_0; root independently reported an Egyptian KeyError:18. Neither is claimed green or repaired by this work. No additional broad validation or country build was run.

Scope of proof: emitted source and focused transaction models, plus isolated native effect observations. This is not a live playthrough of all five focuses, a native hover screenshot, save migration test or multiplayer stability claim.
