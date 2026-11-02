IMPERIA COLD WAR

# Read-only 1970 nonshared-capacity audit: generic, Iraq, UAE, Cuba and Cyprus

27 October 2026. This audit changed no gameplay source, ran no compiler and launched no game. It follows focuses into their actual helpers and distinguishes native manual construction permission from a building's physical state maximum. The detailed inventory, including every listed focus ID, exact helper/check/grant line, quantities, receipts, party slots, caller money lines and source hashes, is `OTHER_COUNTRIES_READONLY.json`.

## Findings and evidence level

Source confirms the same **permission-coupled predicate pattern** in 37 generic focuses, 20 Iraqi main reward helpers and two Cuban contracts/programmes. These are logical sources, not counts of all duplicated previews or pending helpers. A native `free_building_slots` predicate can reflect a researched manual maximum lower than the physical `state_max`. For scripted gifts, replacing it requires an explicit policy choice and native proof that the actual instant grant succeeds before manual unlock. This audit supplies source evidence, not that proof. The separate USA A/B fixture remains unrun while the user's game is active.

The installed unlock definitions are concrete:

| Building | Physical state cap | Manual unlock provider | Relevant limit |
| --- | --- | --- | --- |
| Renewable energy infrastructure | 20 | `common/technologies/industry.txt:1322`, `fuel_silos`, starts1985 | Enables20 renewable levels. |
| Fuel silo | 5 | Same `fuel_silos` node, line1329 | Enables5 silo levels. |
| Nuclear reactor | 20 | `industry.txt:2694`, `reactor1`, historically reworked to1956 | Enables20 levels; a special-project technology, with historical precursor dependencies. |
| Infrastructure | 6 | `industry.txt:3802` onward, `railway_system_01` through `_06`; smart-grid special project for6 | First manual level starts1985, later levels1990 onward. Physical one-level gift needs current level<=5, independent of the chosen manual limit. |
| Radar station | 6 | `common/technologies/engineering.txt:1757`, `radar`, starts1945 | Enables6 radar levels. The tech is researchable in1970 but is not automatically supplied by the reviewed1970 country setup. |
| Anti-air building | 5 | `missile_defense.txt:50` or `non_got_missiles.txt:44` | First level from1945 `air_defense` or `air_defense_non_got`; subsequent SAM tech raises the manual maximum. |
| Air base | 10 | No matching `enable_building` found in the installed technology definitions | No source evidence of the same missing-tech permission problem. |
| Fossil powerplant | 20 | No matching `enable_building` found in the installed technology definitions | Do not classify its native free-space test as the same confirmed tech-lock merely because it is nonshared. |

Physical definitions are in `common/buildings/00_buildings.txt`. The1970 IRQ/CUB/UAE history invokes `mdcw_apply_1970_infantry_research`; its tag profiles grant infantry/support research, not fuel silos, railway-system infrastructure, radar stations or SAM building unlocks. The country's `fuel_silos`/`radar` assignments found later in its history belong to later scenario blocks. No corresponding `fuel_silos=1` or `railway_system_01=1` starter grant was found in runtime scripted effects/on-actions. This is source evidence of an implicit research prerequisite; a particular ongoing save may already have researched it.

## Generic1970: transitive native-helper coupling

The active file is `common/national_focus/mdcw_1970_generic_focus.txt`. It contains37 distinct focuses calling technology-limited nonshared instant-building helpers:24 infrastructure,4 renewable,2 radar,6 anti-air,1 fuel-silo and1 reactor roles, with overlap between roles. There are also4 airbase roles; airbase-only cases are excluded from the37. All40 focuses with one of these nonshared helper calls are inventoried in JSON.

The helper chain is real, not a direct-key-absence finding:

* `one_random_infrastructure` / `two_random_infrastructure` / `three_random_infrastructure`: `common/scripted_effects/00_scripted_effects.txt:442`,493,544 -> `infrastructure_random_build_loc`, `common/scripted_triggers/00_scripted_triggers.txt:523`, native free-space checks525/531. These give one level in up to1/2/3 selected states, not two or three levels in a single state. Native default invoices are3.5/7/10.5; caller skip wrappers must be respected.
* `one_random_renewable_energy_infra`: effects1202 -> renewable selector triggers571, native free-space573/579. Selects one owned controlled state for one instantaneous level. The physical per-state threshold is<=19.
* `one_radar_station`: effects1467 -> radar selector triggers603/605. One instantaneous radar level; physical threshold<=5.
* `one_anti_air`: effects1575 -> anti-air selector triggers619/621. One instantaneous SAM level; physical threshold<=4. The generic capital variant also has an inline manual-capacity branch at tree25109 and falls back to this same helper at25126.

The exact renewable callers are:

| Focus | Focus line | Helper-call line | Actual caller cost |
| --- | --- | --- | --- |
| `GEN_1970_gr_a_nuclear_free_future` | 15126 | 15158 | 1.1%GDP; native8.50fee explicitly skipped |
| `GEN_1970_gr_small_is_beautiful` | 15273 | 15297 | 1.1%GDP; native8.50fee explicitly skipped |
| `GEN_1970_gr_the_soft_energy_path` | 15358 | 15382 | 1.1%GDP; native8.50fee explicitly skipped |
| `GEN_1970_gr_neither_growth_nor_bloc` | 15676 | 15704 | 1.1%GDP; native8.50fee explicitly skipped |

These four green-policy callers set `skip_payment=1`, call the helper, reset it to0 and apply their own1.1%GDP invoice. They also grant other real policy effects. The issue is an omitted promised physical asset if no eligible state is selected, while the policy's own invoice and other effects still execute. It is not four unconditional8.50charges or an entirely empty focus reward. Other generic callers differ: the JSON preserves each one's actual payment/skip lines. Ten of the37 do not contain a skip1 wrapper; inspect their exact branch before any fee correction.

Two further generic helper chains were added after the initial handpicked-family inventory missed them. Counts above include this correction:

* `GEN_1970_expand_the_strategic_reserves` (focus22565, call22581) -> `one_fuel_reserve` (effects1791) -> `fuel_reserve_random_build_loc` (triggers651/653). It promises one instant silo, physical cap5, with a3unit helper invoice outside state-selection success. The full predecessor chain contains no technology grant or tech requirement. `GEN_1970_national_fuel_depots` (22448) directly grants one capital silo plus slot and200000fuel for3units; that gift does not research `fuel_silos`.
* `GEN_1970_first_nuclear_power_station` (focus23553, call23571) -> `one_random_nuclear_reactor` (effects938) -> `nuclear_reactor_random_build_loc` (triggers539/541). It promises one instant reactor, physical cap20, with a9unit helper invoice outside state-selection success. Its visible extra condition is only `NOT GEN_1970_nuclear_free`. `GEN_1970_the_atomic_future` (23401) supplies the atoms-for-peace spirit and a50% one-use reactor research coupon, not `reactor1`; no other ancestor grants or requires that technology. The unlock is the current1956historical special-project tech, not an assumed1985default. Existing country-specific technology can make a particular save eligible, but the generic focus itself does not ensure it.

The emitted generic header names `tools/generate_1970_generic_focus_tree.py`, but that generator is absent from the current workspace search. Existing `tools/focus_quality_20261020/apply_generic.py` updates prose, and `tools/gcc_1970/compile.py` patches GCC integration; neither is evidence of a complete canonical mechanics generator. Canonical repair ownership is unresolved. Do not edit the shared MD helpers globally to change every normal construction or investment consumer.

## Iraq:20 technology-limited gifts and one unconfirmed fossil case

`tools/iraq_1970/compile.py:68` `capacity()` emits the native manual predicate for both shared and nonshared building components. `reward_overhaul.py:139` `_raw()` emits the actual instantaneous gift; `delivery()` keeps each component receipt and recovered credit. Structured amounts/prices come from `reward_overhaul_economy.json`, politics and streamlining overlays assembled by `audit_design.load_design()`. Main runtime helpers are in `common/scripted_effects/COLDWAR_IRQ_1970_rewards.txt`.

The table below lists every nonshared main helper found. Each grant is one level in the named state. Infrastructure has physical cap6, silo5, fossil20. Slot annotations are outside this capacity-only audit; do not duplicate existing component deliveries when later correcting them.

| Focus suffix after `COLDWAR_IRQ_` | State/type | Check line | Grant line | Actual party slot |
| --- | --- | --- | --- | --- |
| `autonomy_guarantees` | 166 / infrastructure | 599 | 628 | Common national path |
| `bakr_development` | 557 / infrastructure | 1818 | 1847 | 21 |
| `royal_public_works` | 171 / infrastructure | 7035 | 7064 | 23 |
| `foreign_border_delivery` | 1124 / infrastructure | 7460 | 7489 | Common national path |
| `kdp_mountain_routes` | 164 / infrastructure | 8282 | 8311 | 6 |
| `puk_trade_routes` | 630 / infrastructure | 9198 | 9227 | 19 |
| `sciri_water_services` | 1124 / infrastructure | 10710 | 10739 | 9 |
| `oil_concession_delivery` | 171 / infrastructure | 11745 | 11767 | Common national path |
| `oil_revenue_state` | 171 / infrastructure | 11891 | 11920 | Common national path |
| `oil_baiji` | 167 / fuel_silo | 12161 | 12190 | Common national path |
| `oil_reserve_policy` | 171 / fuel_silo | 12235 | 12264 | Common national path |
| `industry_power_grid` | 557 / infrastructure | 12618 | 12647 | Common national path |
| `industry_power` | 171 / fossil_powerplant | 12907 | 12936 | Common national path |
| `agri_large_irrigation` | 1141 / infrastructure | 13405 | 13434 | Common national path |
| `agri_grain_storage` | 1142 / infrastructure | 13664 | 13693 | Common national path |
| `society_primary_care` | 1124 / infrastructure | 14360 | 14389 | Common national path |
| `society_priority_districts` | 166 / infrastructure | 14433 | 14462 | Common national path |
| `society_housing` | 557 / infrastructure | 14609 | 14638 | Common national path |
| `defence_logistics` | 167 / infrastructure | 15501 | 15530 | Common national path |
| `iran_forward_depots` | 167 / infrastructure | 17289 | 17318 | Common national path |
| `iran_oil_rehabilitation` | 399 / infrastructure | 17720 | 17749 | Common national path |

Twenty rows are source-confirmed technology-dependent capacity coupling:18 infrastructure and2 silo gifts. `industry_power` is the separate fossil case, not proven to share a missing-unlock problem. Baiji and reserve policy require the implemented oil-revenue ledger, their own frozen GDP invoice, treasury coverage and no `MD_skip_treasury_cost`. Their prices are3.5% and2.5%GDP. A failed capacity check leaves the main programme pending before payment; it does not charge the invoice and then silently skip the silo. Descendants requiring `_implemented` can then remain blocked.

Do not flatten migration logic: `COLDWAR_IRQ_reward_v3_<key>_0` or sufficient prior component credit bypasses a building already delivered. The native capacity check applies to the outstanding remainder. Matching checks also occur in `COLDWAR_IRQ_1970_direct_rewards_v3.txt`, `_audit_migration.txt` and pending decisions. They are additional execution/recovery paths for the same logical programme, not additional independent focus grants. Party restrictions remain real: Bakr21 plus office holder, monarchy23, KDP6, PUK19 plus `puk_formed`, SCIRI9 plus `sciri_formed`. Wartime/captured-state cases retain their Iran-war and actual ownership requirements. These are not all immediateJanuary1970 choices.

## Cuba: Havana silo and recipient-approved radar

`COLDWAR_CUB_havana_ports` -> `COLDWAR_CUB_can_havana_ports`, `common/scripted_triggers/COLDWAR_CUB_1970_triggers.txt:102`, tests Havana naval-base province7622 separately and then state854 `fuel_silo` manual free capacity at115. `COLDWAR_CUB_apply_havana_ports`, effects164, grants port+slot for0.55 and, unless `COLDWAR_CUB_oil_reserve_applied` already exists, silo+slot for another0.35. Both are instantaneous. `havana_ports_applied` prevents repeat completion. The fuel unlock is the same1985technology; physical silo threshold for one level is<=4. The correctly province-scoped port predicate is not the same issue.

`COLDWAR_CUB_air_defence` (tree1143) requires `COLDWAR_CUB_far_reorganisation_applied`, an existing Soviet Union and peace with it (`triggers:192`). It has no additional ruling-party check. It calls `COLDWAR_CUB_offer_air_defence`, diplomacy effects32/34. The offer itself needs Havana radar manual free capacity, as do Soviet acceptance availability and execution at `common/decisions/COLDWAR_CUB_1970_diplomacy.txt:133`,138,143 and retry486. Acceptance grants Havana one radar+one slot, a25% one-use `radar` research bonus and the delivery receipt; Soviet fee0.15 and Cuban fee0.45. Thus the manual permission can block dispatch/acceptance of the very agreement that promises the radar installation. Researchable1945radar is an implicit prerequisite, and if already researched its same-tech coupon has reduced/no value. Preserve actual Soviet consent, peace, ownership, open/pending flags and `air_defence_receipt` in any later repair.

Canonical sites: `tools/cuba_1970/compile.py:81` `economic_guard()` special-cases infrastructure to physical `<6` but applies native free-space checks to every other building at94. `direct()`202 emits the construction. Current data are assembled by `cuba_runtime_design.py` over the immutable approval and revision; do not mutate either approval snapshot. The bilateral source is `tools/cuba_1970/diplomacy.py:51`,495-502 and674.

`COLDWAR_CUB_moa_refinery` also has a state1121 fossil-power free-capacity condition (`triggers:73`) guarding its grid component (`effects:112` onward). It is nonshared but not proven to be limited by an unresearched unlock. Existing Cuban infrastructure focus guards already use explicit physical `<6`; those are not this defect.

## UAE and Cyprus: keep distinct checks

UAE's only state-nonshared manual predicate in its core focus triggers is `COLDWAR_UAE_can_apply_aviation_hub`, `common/scripted_triggers/COLDWAR_UAE_1970_focus_triggers.txt:752`, airbase check763. Actual helper `_apply_aviation_hub`, effects1733, guards its receipt, costs2.5, and adds one slot then one instant airbase in state179. Its commercial-courts predecessor and industrial-port exclusion must remain. Physical airbase cap10, but no installed technology was found lowering the manual permission. This is a review candidate, not a confirmed instance of the1970fuel-silos problem. Canonical sources: UAE `compile.py:106` project mapping,200 guard, `development.py:57`, `focus_only.py:24`. Existing Dubai harbour level/capacity work and the naval graft use province/shared checks and are outside this state-unlock finding.

The authored CYP tree does not contain a comparable state-nonshared instant grant gate. Its Famagusta harbour path uses actual province7193 capacity (`tree:1848`, `effects:2403`, `tools/cyprus_1970/rules.py:55`) and queues construction with `instant_build=no` (`effects:2380`). Keep it separate. Northern Cyprus currently loads `mdcw_1970_generic_focus` (`history/countries/NCY - Northern Cyprus.txt:43`), so it inherits the generic helper cases; there is no separate installed NCY national tree to declare clean.

## Repair boundaries

No blanket replacement is justified. Shared-state slots, provincial naval bases/forts, construction queues and foreign-investment APIs have their own capacity semantics. A future bounded fix for an intended instantaneous nonshared gift must preserve ownership/control, exact quantity, party/institution/war gates, component credits, funding, genuine recipient consent and once-only slots/assets. It must recheck the complete transaction at execution and show the actual physical requirement in native numeric form. The isolated engine A/B is still needed to establish how instant construction behaves before the manual technology unlock.

All historical and game/provider authors retain their existing credits. This audit creates only compact original reports, copies no asset and makes no separate ownership claim. Source hashes identify the inspected revision; they are not a gameplay or multiplayer certificate.
