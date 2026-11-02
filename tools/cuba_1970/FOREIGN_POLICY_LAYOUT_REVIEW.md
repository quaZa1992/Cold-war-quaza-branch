# IMPERIA COLD WAR - Cuba foreign policy layout review

## Recommendation

The revised 25-node plan is viable with separate COMECON admission and member-only follow-up focuses. It drops the standalone Havana Conference and carries the non-aligned theme through the Caribbean cooperation offer. Keep the COMECON admission offer reachable before membership, and require the actual membership spirit at availability and reward on the Division of Labour focus.

Do not turn the Soviet, Mexican, Spanish, Canadian, Jamaican, or American trade arrangements into a single mutually exclusive alignment choice. These can coexist. Keep visible exclusivity for the genuine institutional alternatives: Moscow alignment versus independent diplomacy, symbolic naming versus territorial cession, and advisers versus an expeditionary commitment. The Soviet commodity arrangement and Soviet industrial cooperation should also be independently completable if they represent distinct contracts.

## Current tree and fit

The approved design contains 120 focuses. Its shared sections hold 43 nodes: economy 15, society 7, defence 8, and foreign policy 13. The political programmes account for the remaining 77, including the 13-focus PCC/Fidel branch. Keep that approved political branch intact.

The current foreign group is rooted at grid coordinate (42,0), spans approximately x=38 to 50 and y=0 to 6, and covers diplomacy, COMECON, the Caribbean, the United States, the DDR, and the Thälmann island agreements. The armed forces branch is rooted at (30,0) and the political roots begin at y=10. The 96 by 130 native grid and 165 by 128 focus cards favor two-cell minimum horizontal separation; four cells is more comfortable for parallel labelled tracks. A 25-node foreign section can fit above the political roots if it extends down to about y=8 and stays roughly within x=34 to 54. Use short parallel country tracks rather than adding wide, tangled cross-branch connectors. The complete tree currently reaches x=56, so avoid pushing new content far beyond that edge.

The revised foreign list counts 25: Island Diplomacy (1), Soviet Assistance (1), Soviet Commodity and Soviet Industry (2), COMECON admission and member follow-up (2), Mexico (2), Spain (2), Canada (2), Berlin/Havana (1), symbolic Thälmann cooperation and cession (2), Interests Sections (1), Limited Trade and Full Claims Settlement (2), Caribbean Cooperation with a non-aligned theme (1), Overseas Institution (1), Advisers and Expeditionary Forces (2), Angola (1), Ethiopia (1), and Algeria medical cooperation (1). The medics' national medical policy stays in the Society section; the Algeria offer should require that policy rather than creating a generic medical-mission chooser.

## Concrete 12-node consolidation

The following set reaches the 25-node version while retaining the current high-level choices. It moves exact rewards and their full costs/duration onto the surviving node or both surviving alternatives. Combined rewards must not reduce aggregate focus days, treasury deductions, or investments.

| Section | Merge | Nodes removed | Preservation condition |
|---|---|---:|---|
| Economy | Put Rail and Lorries' shared reward on both Finish the Zafra / Restore the Sectors choices | 1 | Preserve State 854 infrastructure, the infrastructure research bonus, cost, and duration on either strategy; retain both strategy effects as a real fork. Reparent downstream focuses to the alternatives as an OR requirement. |
| Economy | Sugar for Export + Mill Mechanisation | 1 | Keep the export-policy modifier and the existing State 854 agriculture-district investment and treasury cost on the same route. |
| Economy | Food before Sugar + ANAP Cooperatives | 1 | Keep the food-priority effect and the existing State 1121 agriculture-district investment and cost. |
| Economy | Moa's Refinery + Repair the Grid + Light Industry | 2 | Retain the State 855 industrial complex, State 1121 fossil powerplant, second State 1121 industrial complex, and all three treasury deductions; use the combined original duration. |
| Economy | Havana's Ports + Oil Shock Reserve | 1 | Retain the State 854 naval base at province 7622 and the State 854 fuel silo with both costs and aggregate duration. |
| Defence | Move Expeditionary Forces and Mission Schools into the foreign expeditionary/doctrine route | 2 | Retain both posture modifiers and the land-doctrine reward; preserve their combined duration and connect the overseas offer to the actual expeditionary route. |
| Defence | Territorial Defence + Militia Logistics | 1 | Carry both current modifiers and the small-arms research reward; preserve combined focus time. |
| Society | Fold The Social Promise into both Rural Clinics / Teaching Hospitals choices | 1 | Preserve the education law and modifier on either choice, with the original entry-plus-choice duration. |
| Society | Science Schools + Health Workforce | 1 | Preserve the health-budget law, treasury deductions, both electronics research bonuses, and the intended conditional caps; use the combined duration and make the research preview match its actual gates. |
| OSPAAAL | Fold Tricontinental Secretariat into the two exclusive programme choices | 1 | Keep Diplomatic Solidarity versus Foreign Cadres as two visible, mutually exclusive alternatives; retain each full modifier set and aggregate duration. |

This preserves the core policy forks and the development outcomes, but it makes some cards denser. If the renderer cannot present those bundled rewards clearly, keep the extra node and reduce elsewhere only after comparing the historical and gameplay value. Do not delete a branch's substantive choice to meet an arbitrary count.

The list above makes economy 15 to 9, defence 8 to 5, society 7 to 5, and OSPAAAL 3 to 2, releasing exactly 12 focuses. The two military nodes moved to the foreign doctrine route are counted in the revised 25-node foreign total, not as deleted content. This funds the foreign section's net increase from 13 to 25 while preserving the political alternatives. The OSPAAAL reduction is only one node because compressing its solidarity-versus-cadres alternatives into one focus would erase a meaningful political choice.

## Foreign-policy structure and routes

Keep a compact top-level Island Diplomacy root, then arrange three readable horizontal clusters: partner trade and industrial agreements; Caribbean/United States and Berlin/Havana diplomacy; and overseas missions. Mexico, Spain, and Canada should be parallel two-focus tracks with their own partner acceptance decisions and independent spirits. Their agreement terms should remain separately completable from Soviet assistance and Soviet commodity or industrial contracts.

For the Thälmann island, retain the two distinct terminal routes. Symbolic cooperation can name the island and unlock the Playa RDA arrangement. Cession should remain a separate partner decision with its own later development protocol. Do not present symbolism as if it transfers sovereignty, or imply that cession is merely another trade preference.

Make the overseas institution an enabling focus, with Angola and Ethiopia as distinct recipient-specific mission focuses. Keep the Algerian medical route distinct from military deployment. The Advisers versus Expeditionary fork should carry a genuine posture trade-off and feed the mission focuses with a short, legible join. Do not grant volunteers or intervention access merely from a diplomacy bonus; recipient consent and a valid theatre remain separate runtime gates. The Angola branch should describe an operational readiness or offer path at a 1970 start, not assert that the later Angolan war is already underway.

Keep Limited Trade and Full Claims Settlement as alternative terms only if the second is explicitly a final settlement that supersedes the first. Otherwise make them a sequence or independent American arrangements. The American Interests Sections should be an additional, compatible diplomatic track where its terms allow; they should not silently cancel an unrelated Canadian or Mexican deal.

## Native presentation references

The current native Cuba tree demonstrates a visible bilateral posture fork in `CUB_coop_china` and `CUB_coop_usa` at `05_cuba.txt` lines 197 and 255. They are adjacent one-cell children of `CUB_reforms_of_army`, have native prerequisites and costs, and are mutually exclusive because they are alignment alternatives. The later `CUB_revolutionary_army` focus at line 318 joins the routes through one prerequisite block containing either predecessor. This OR join is an appropriate pattern for compatible later policy. It is not a reason to make every trading partner exclusive.

The current Russian tree's `SOV_aggressive_foreign_policy` around line 2976 uses exact prerequisites, a native dynamic-modifier reward, and a targeted decision unlock. `SOV_neoliberal_foreign_policy` around line 15816 shows a foreign-policy root with visible institutional and party requirements. `SOV_expand_trade_with_taiwan` around line 20577 is a partner-specific trade focus with reciprocal relations/influence and a targeted decision category. These examples support discrete bilateral tracks with local gates and numeric reward previews, not one generic world-trade focus.

For Cuba's compact sibling layout, keep parallel deal roots at least two grid cells apart, and preferably four where long native labels need room. Use a single explicit OR join only where either branch genuinely enables the same next step. Preserve separate AND requirements as separate prerequisite blocks. Keep the long overseas mission connection routed through a nearby institution node rather than drawing a long connector across the full foreign section.

## Source evidence

- Current counts, grid roots, coordinates, and focus rewards: `tools/cuba_1970/approved_design.json`, groups and nodes `economy`, `society`, `defence`, and `foreign`.
- Current COMECON, Thälmann island, Caribbean, and overseas focus IDs: `COLDWAR_CUB_cmea_application`, `COLDWAR_CUB_division_labour`, `COLDWAR_CUB_thaelmann_name`, `COLDWAR_CUB_caribbean_treaty`, `COLDWAR_CUB_playa_rda`, and `COLDWAR_CUB_development_protocol` in the same snapshot.
- Partner trade precedents and timing caveats: `tools/cuba_1970/BILATERAL_HISTORICAL_PRECEDENTS.md`.
- Native source file: `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_cuba.txt` and `05_russia.txt`.
