IMPERIA COLD WAR

# Soviet and East German naval adaptation: source profile and integration advice

Read-only audit, 25 October 2026. No gameplay, generator, history, leader, approval snapshot or localisation was edited. Counts and hashes below describe the inspected baseline before the new adaptation is installed. They are not validation of a subsequent build.

## Active 1970 providers

| Country | Authoritative history route | Active tree and inspected baseline |
| --- | --- | --- |
| Soviet Union | `history/countries/SOV - Russia.txt:39`, inside the 1970 snapshot's `date < 1985.1.1` selection | `common/national_focus/COLDWAR_SOV_1970_focus.txt`, tree ID `COLDWAR_SOV_1970_focus`, 836 direct focuses; SHA-256 `2b0beb6dfd49ee5910d5bb35f963b5adcdeadcf29c145e7e87d85caba86b1c69` |
| German Democratic Republic | `history/countries/DDR - East Germany.txt:44`, inside the equivalent 1970 snapshot selection | `common/national_focus/COLDWAR_DDR_1970_focus.txt`, tree ID `COLDWAR_DDR_1970_focus`, 821 direct focuses; SHA-256 `58397c0c0f1f047e1cd804da58a16d70920bfbd6528295f68fb43c40792221d9` |

Both trees also select the real original tag and `IMP_is_1970_scenario`. `common/scripted_effects/mdcw_1970_focus_tree_effects.txt:39` and `:40` exempt these countries from the generic replacement route. `SOV_1985.txt`, `ddr.txt` and modern Russia are not the target providers. The history's scenario selection is not a proposal for a dated naval focus restriction.

## Actual current main-MD donor

The inspected donor is Steam Workshop item 2777392649, Millennium Dawn 2.0.2, supported HOI4 1.19.*, at `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/00_generic.txt`. SHA-256: `c3f2e55df976b712e423fa906afd18b9e638c838d1cb34a13fb80bfa2ea82ac5`. Its generic naval chapter starts at line 4298. Original individual authorship and applicable licence/permission were not established in this small source audit; retain upstream attribution and resolve that provenance in the copying implementation. No binary art was copied for this report.

There are 20 focuses descended from `GENERIC_naval_reform`. Its root resolves to (31,0), and its complete footprint is x26..35, y0..5: relative x-5..+4, y0..5. Most costs are 10; vessel production and two industrial follow-ups cost 5; nuclear submarines and submarine expansion cost 7.1. The entry uses icon `navy`, requires control of a coastal state, and grants 75 navy XP, 30 naval mastery if a naval grand doctrine is selected, 15% progress toward an unfinished naval-vessel special project, and +10 Maritime Industry opinion. These are the current donor's effects, not a guessed older generic branch.

Copying the chapter also requires tracing its buildings, ideas, research categories, special projects and grand-doctrine effects. Retain native icon classes, numeric previews and meaningful coastal requirements. Give every adapted ID a country-specific namespace so completing one country's programme cannot satisfy another country's receipts.

## Existing country content and reward scale

**Soviet Union.** The existing naval chapter has 15 focuses. `COLDWAR_SOV_gorshkovs_navy` starts at (315,0), line 29214. Okean-70 is at (312,1); The Navy Question at (318,1). Its second row contains the Fifth Eskadra (312,2), northern shipyards (314,2), naval missile aviation (316,2), carriers/cruisers (318,2) and submarines (322,2). The submarine and carrier/cruiser priorities are mutually exclusive. The third row has overseas access, Kiev, Kirov, bastion protection and Lira projects. The Typhoon programme is at (321,4), and the blue-water capstone at (322,5).

Representative actual rewards:

| Existing focus | Cost | Native reward bundle and invoice |
| --- | --- | --- |
| Gorshkov's Navy | 3 | 25 navy XP; range +5%; organisation +3% |
| The Submarine Fleet | 5 | One dockyard; 0.8% GDP invoice; 25 navy XP; two 50% coupons across attack/missile submarine categories |
| Carriers and Cruisers | 5 | One dockyard; 1% GDP invoice; 25 navy XP; two 50% coupons across carrier/cruiser categories |
| The Bastion Strategy | 5 | Submarine attack +5%; organisation +3%; two 50% sonar coupons; 25 navy XP; 0.3% GDP invoice |
| The Kiev Class | 7 | Two 75% carrier coupons; dockyard output +5%; range +5%; 50 navy XP; 0.8% GDP invoice |

The capstone adds `COLDWAR_SOV_blue_water_navy`: range +10%, naval damage +3%, organisation +3%. Existing dynamic modifier providers are in `common/dynamic_modifiers/COLDWAR_SOV_1970_dynamic_modifiers.txt`. Audit new compatible-route totals against these existing rewards instead of counting the generic chapter in isolation. Preserve the old priority exclusion and its follow-through; the new chapter must not accidentally make the excluded country's old receipt payable through a renamed generic focus.

**DDR.** The common coast/air entry is at (94,12). The Volksmarine root is (90,13), line 27113. Coastal Navy (88,14) and Blue-Water Ambitions (90,14) are mutually exclusive. The 6th Flotilla and Peene Shipyard are at (88,15) and (90,15); the coastal missile regiment at (88,16). United Baltic Fleets is (92,14). This is eight naval/common cards within an 18-card naval/air chapter. Air/space follow-ups occupy x93..98 through y17.

The Volksmarine grants 35 navy XP and one 50% patrol-boat coupon. Coastal Navy grants organisation +5%, equipment upkeep -2%, 25 navy XP and Maritime Industry opinion -5. Blue-Water Ambitions costs 0.8% GDP, adds one dockyard, range +10% and Maritime Industry opinion +5. Peene costs another 0.8% GDP, adds one dockyard, output +4%, one 50% corvette coupon and Maritime Industry opinion +5. These are existing country-specific opportunity costs, not empty flavour choices. The real NVA dynamic modifier maps naval coordination, organisation, range and dockyard output in `common/dynamic_modifiers/COLDWAR_DDR_1970_dynamic_modifiers.txt:97`.

The current `one_random_dockyard` helper in `common/scripted_effects/00_scripted_effects.txt:595` already grants a shared slot before construction. Its selector checks ownership, controlled-state iteration, coast and native slots through `dockyard_random_build_loc` at `common/scripted_triggers/00_scripted_triggers.txt:505`. It nevertheless bills a flat $7.5 billion unless `skip_payment = 1`. Existing SOV/DDR focuses deliberately use the skip wrapper and pay their own GDP share. Do not silently add the helper's flat invoice on top of the adapted country invoice, or assume its scale is appropriate to the DDR. Recheck asset capacity at execution and do not charge a promised asset that cannot be delivered.

## Canonical generator and safe integration points

SOV's source is `Claude outputs/COLDWAR_SOV_design/sov_dsl.py` and `d_mil_state.py`, registered through `build_all.py`. `Claude outputs/COLDWAR_SOV_generator/cw_layout.py` resolves layout and applies `overrides/g7_military_foreign.json`; English descriptions/icons come from `desc/out_2.json` and related registries. `cw_focus.py:243` builds the focus file and returns it at line 264. `cw_build.py:9` captures that file before building the remaining registries, then writes mirrored output under its `out/` directory.

DDR's source is `Claude outputs/COLDWAR_DDR_generator/design/ddr_tree.json` and `page_data.json`, loaded by `dg_load.py`. `dg_focus.py:197` constructs the focus file and returns it at line 222. `dg_build.py:9` captures it; later it includes `dg_quality.py` runtime outputs. Existing quality, trust-removal and native-modifier fixes must remain intact.

A narrow pure transformation at each focus emitter's returned string, or a coordinator-owned bounded overlay after existing corrections, can install new IDs without regenerating unrelated history and mechanics. Register the adaptation's localisation and runtime files through the same canonical build route so a later ordinary build cannot erase it. Do not import or run either broad build script merely to inspect it: both perform top-level output-directory removal and build much more than the naval chapter. This audit ran neither generator.

Placement candidates for the actual 20-node donor footprint:

| Country | New root candidate | Resulting new footprint | Existing neighbours and cautions |
| --- | --- | --- | --- |
| SOV | (315,7) | x310..319, y7..12 | No existing focus in x300..335 at y7 or lower. Existing navy ends at y5. The continuous panel starts at pixel (31200,1040), equivalent x325,y8, outside this footprint. An attachment to an existing root still needs connector inspection. |
| DDR | (90,19) | x85..94, y19..24 | Naval/air cards end at y17. The footprint is below the existing local branch, not within its border-policy, party or air branches. Continuous panel at pixel (31488,1560) is far away at x328,y12. |

These are source-coordinate candidates, not approved or rendered final geometry. Reuse a meaningful existing naval root where appropriate. Do not require the SOV blue-water capstone merely to access basic generic naval development: that would also import its overseas-access dependency. Keep new development inspectable without party or arbitrary date gates. No new leader or head-of-state work is needed.

## Historical source profile and country fit

**Strategic submarines were a real Soviet programme before 1970.** Helms's 4 August 1969 memorandum discusses an August 1970 projection of 560 submarine ballistic-missile launchers, including 272 on 17 Y-class boats still at different construction stages. This supports SSBN construction, propulsion, patrol preparation and survivability research; projected launchers under construction must not become a free commissioned fleet at scenario start. [FRUS SALT I, document 32](https://history.state.gov/historicaldocuments/frus1969-76v32/d32)

**Ocean operations and naval aviation need logistics.** Moorer's 1970 paper records the large April exercise operating in three oceans and increasing Mediterranean activity. A later 23 December 1974 intelligence estimate identifies deterrent patrols and coordinated air, submarine and surface attacks on carriers, while stressing ASW shortcomings and limited replenishment. These are contemporaneous US assessments, not neutral proof of every Soviet intention. Design implication: preserve useful surface and submarine investment while making support ships, maintenance, sensors and actual access meaningful. Do not grant universal carrier immunity or a global ASW solution. [FRUS document 211](https://history.state.gov/historicaldocuments/frus1969-76v12/d211), [NIE 11-15-74](https://history.state.gov/historicaldocuments/frus1969-76v35/d150)

**Helicopter ships and strike carriers are different institutions.** The Royal Navy minister's 9 March 1970 presentation describes the Soviet emphasis on nuclear submarines and primarily ASW surface ships, alongside the absence of a carrier force in the contemporary strike-carrier sense. The 1967 defence secretary had already distinguished Soviet helicopter carriers from strike carriers. Thus Soviet helicopter/ASW ship research fits the baseline, while a larger aircraft-carrying cruiser programme is a prospective development choice. Do not describe Kiev, Kirov or Typhoon as an already completed January 1970 fleet. [9 March 1970 Hansard](https://hansard.parliament.uk/Commons/1970-03-09/debates/fd1a94c3-0913-4ce1-a13f-95fa9cbc1f72/OrderOfTheDay), [8 November 1967 ministerial answers](https://api.parliament.uk/historic-hansard/commons/1967/nov/08/aircraft-carriers)

**Warsaw Pact coastal cooperation did not erase national decisions.** The archival record of Gorshkov's 21 May 1970 report identifies East German, Polish, Bulgarian and Romanian modernisation needs and a proposed united naval command. The record of Hoffmann's 23 May report says the command proposal was abandoned following Romanian objections. Both are Bundesarchiv Military Archive documents catalogued by the Parallel History Project: DVW 1/71026 and DVW 1/71025. This supports coastal modernisation and joint exercises; it does not support automatically asserting a new unified command or real allied operational consent. [Gorshkov record](https://phpisn.ethz.ch/lory1.ethz.ch/collections/colltopic59bd.html?id=21367&lng=en&navinfo=14565), [Hoffmann record](https://phpisn.ethz.ch/lory1.ethz.ch/collections/colltopic0ba4.html?id=21362&lng=en&navinfo=14565)

**Mine clearance and local maritime services have direct East German precedent.** The DEFA archive describes its 1957 film *Achtung, Minen*: drifting wartime mines, fishermen's warnings, Rügen radio, Rostock maritime authorities, tugs, clearance boats and divers. The film is a period source, with the synopsis supplied by its present archival custodian. This provides a specific institutional basis for minesweeping, hydrography, radio coordination, rescue, repair and safe coastal traffic. The 1970 Warsaw Pact record supplies the later modernisation context. [DEFA film record](https://www.defa-stiftung.de/en/films/film-search/achtung-minen/)

For DDR, adapt the donor's submarine and nuclear-submarine slots to underwater detection, ASW and mine countermeasures; carrier-related slots to landing/support vessels and shore-based naval aviation; stealth development to practical signature control, sensors and ship protection. Use patrol boats, corvettes, escorts, mines, coastal missiles, repair and convoy handling as its historical centre. Registered existing categories include `CAT_patrol_boats`, `CAT_corvettes`, `CAT_frigates`, `CAT_landing_craft`, `CAT_naval_sonar` and `CAT_naval_anti_ship_missiles` in `common/technology_tags/00_technology.txt`. Verify the exact mine, repair and doctrine effects before emission. This packet supplies no evidence for an operational DDR nuclear-submarine, SSBN or carrier programme in 1970. Keep any continued blue-water ambition explicitly prospective and consistent with the existing alternative; it need not be the historical default.

## Evidence boundaries and later review

The primary FRUS and Hansard text was retrieved. The Gorshkov catalogue page was retrieved, but its 14-page scan failed to load; the Hoffmann document was available through indexed archival metadata. The DEFA record was available through its indexed custodian synopsis; the film was not viewed. NATO MCM-0039-1970 was found, but its PDF returned 403, so no OCR table count from that source is treated as independently inspected evidence. Exact source-access limits prevent an archival catalogue description being presented as a full document reading.

After implementation, independently review emitted scope/effect names, research-use/category support, cumulative existing-plus-new rewards, shared modifiers and one-time migration. Render both complete neighbouring trees and normal-scale naval branches, then inspect captions, actual icon classes, connectors and the continuous panel. A source preview and parser/model pass do not establish native or multiplayer behaviour. No native launch or multiplayer test was performed for this audit.
