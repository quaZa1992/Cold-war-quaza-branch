IMPERIA COLD WAR

# Independent reward review: BRD and DDR

## Scope and review basis

Read-only review of the bounded West German reward renderer and the current DDR reward overlay, including their loaded focus outputs, package manifests, helper guards, route costs, installed MD equipment and research identifiers. This review checks reward semantics, focus lifecycle, visible effects, and economic scale. It does not claim a live HOI4 session or multiplayer test.

The historical facts and main-MD scale examples are documented in [HISTORICAL_AND_MD_REFERENCES.md](HISTORICAL_AND_MD_REFERENCES.md). The detailed country manifests and implementation notes are [GER_CHANGES.json](GER_CHANGES.json), [GER_REVIEW.md](GER_REVIEW.md), and the canonical DDR overlay at `Claude outputs/COLDWAR_DDR_generator/design/ddr_reward_overlay_20261027.json`.

## West Germany

The renderer expands 54 existing focus rewards and corrects the existing Energy Mix percentage mapping. It preserves the old focus rewards and wraps the old and new effects in a single execution guard with original focus availability, GER and 1970 routing, positive GDP, full building and technology capacity checks, and a permanent focus receipt. Preview shows the original and added native effects together. Every original or added fixed-state building level now receives a shared slot before construction, including the repaired original grants for Patriot radar and anti-air in states 39 and 41, and AWACS radar and air-base levels in state 39.

Current examples have plausible game-scale investment costs and substantial choices: the SPD stimulus and technology route adds 3.2% GDP in overlay charges, versus 3.0% for austerity; energy examples range from 0.7% for coal and century contracts to 1.6% for moratorium and renewables; the army modernization and air route costs 4.0% in overlay charges. The manifest separates previous Treasury effects and debt from the new charges. These are point-in-time GDP comparisons, not fixed nominal runtime prices.

The Energy Mix dynamic modifier now maps `cwfo_energie_fossil` to `fossil_pp_fuel_consumption_modifier` and `cwfo_energie_nuclear` to `nuclear_energy_generation_modifier`, matching the percentage tooltips. Renewable-infrastructure gates use the installed `fuel_silos` unlock, which actually enables that building tier. Tornado production discounts target the supported `medium_plane_airframe` family; installed equipment data assigns that archetype to legacy `Strike_fighter` equipment, and the BBA Tornado record uses medium-plane CAS equipment. Research uses the real `CAT_aircraft` category. F122 and Type 209 use installed frigate and submarine families and categories.

The cumulative routes combine named-state industrial, research, energy, and military assets with limited-use research support, equipment-family cost reductions, and signed programme-core modifiers. Costs, branch exclusivity, equipment roles, and plant technology gates are explicit in the manifest. No free reactor, renewable plant, or microchip plant is created.

## East Germany

The bounded DDR revision adds 31 static finite or modifier rewards and 18 paid asset programmes across 49 existing focus rewards. The loaded tree retains its 836 focus IDs and its previous graph, timing, and party/branch rules, as confirmed by the parent verifier. Each paid focus previews its complete old residual reward plus the current-GDP fee, new assets, slots, and modifiers. Execution repeats the focus availability, GDP, ownership, control, building-cap, and specialist-technology checks under one receipt guard. The old random building helpers and project fees are folded into the same transaction, preventing a second charge or separate project payout. Ordinary industrial, office, infrastructure, power, agricultural, microchip, and arms construction is included.

Representative route totals, verified from the transaction manifest at DDR's $32 billion scenario-start GDP:

| Route | Total fee | Start-GDP amount |
|---|---:|---:|
| Ulbricht NÖS: structure, Kombinat, cybernetics | 8.64% | $2.7648B |
| Honecker: pay, housing, main task | 9.30% | $2.9760B |
| Green League renewable package | 2.71% | $0.8672B |
| CDU social-market package | 3.20% | $1.0240B |
| UCT guild-economy package | 3.20% | $1.0240B |
| DBD villages plus village programme | 2.34% | $0.7488B |

The 46.16% sum across all 18 DDR transactions includes mutually exclusive choices and is not a single path. On a focus-by-focus basis, benefits now distinguish industrial investment and enterprise autonomy, household spending, computing and microelectronics, energy sources, rural development, and military production. Fees provide a consistent capital trade-off; costs and negative modifiers vary by focus. There are no workforce-size penalties, free equipment, or automatic uranium production.

The previous exact same-focus duplicate modifiers have been removed. I compared each overlay's dynamic modifier keys against the frozen base reward: the current DDR JSON has no same-focus overlap in its static or paid transaction entries. This catches the earlier repeated energy, housing, consumer-goods, microchip, population, reactor-speed, and NVA modifiers.

The Honecker infrastructure was redistributed after a route-capacity audit. Berlin (45) begins at infrastructure 3, and the other five program states begin at 2, with a native cap of 6. Across pay, housing, and the main task, the route reaches Berlin 5, Saxony (44) 4, Mecklenburg (539) 4, Thuringia (545) 5, Saxony-Anhalt (972) 4, and Brandenburg (1079) 4. Adding the DBD village package brings Mecklenburg to 6 exactly. The Ulbricht trio plus Schkopau puts synthetic refineries at Saxony 1 and Saxony-Anhalt 2, within the amount-aware tier-2 gate. These are source-level calculations against the parent's January 1970 start levels. They are arithmetic checks of the transaction manifest, not an engine fixture result.

## Final semantic assessment

The root's final semantic corrections are in the current canonical overlay and emitted DDR focus/runtime outputs. The MiG-23 reward now uses NVA `air_defence_factor +3%` instead of static ground anti-air damage, while its description identifies the `air_accidents_factor +2%` penalty as conversion-accident risk. Border troops add party-state police costs +2%, and the 40th Parachute Battalion adds NVA personnel costs +1%, giving both descriptions mechanical trade-offs. The conservation and Greifswald descriptions no longer promise absent upkeep, the housing programme describes construction and infrastructure support rather than delivered housing, and the microelectronics prose no longer counts implementation-level research uses. The UCT, price-control, Coast and Skies, MiG-21, NVA, Soviet-equipment, and Thousand Small Things descriptions were also aligned to their effects. These edits are itemised in `final_semantic_corrections` in [CHANGES.json](CHANGES.json).

The DDR emitter now gives new limited-use research and doctrine bonuses distinct names from retained legacy bonuses. The previous NVA equipment cost reduction is removed before the family-specific bonus is added.

`consumer_goods_factor` in this mod affects the consumer-goods factory allocation and tax-cost burden; it is not a measurement of delivered household goods. The remaining Ulbricht description about household consumption losing priority is a political-economy interpretation of the investment-first package and its factory-allocation burden, not a direct consumer-goods output statistic. Likewise, the review's descriptions of historical scarcity or import dependence are narrative context unless a matching modifier or fee is listed.

## Findings and verification boundary

- Corrected the focus-point conversion in the research note: installed `NFocus.FOCUS_POINT_DAYS = 7`, so costs 4.3, 6, 6.5, 7, and 10 correspond to 30.1, 42, 45.5, 49, and 70 theoretical days. Fractional-day rounding remains unresolved.
- Corrected the Works Constitution Act chronology: the Bundestag passed the reform in November 1971, the Act is dated January 1972, and the law is from 1972. The 1951 Montan co-determination precedent and 1976 codetermination law are distinguished.
- Source-level review covered current package descriptions, frozen old rewards, added modifiers, buildings, fees, and current emitted focus/tooltips. The DDR graph, state capacity totals, and representative fees above were checked from the current project sources and the parent's January 1970 starting-level inputs.
- I did not run the root parser, source verification suite, native assertion fixture, or HOI4 engine. The root owns those checks and had started a final native run on frozen inputs when this note was updated. No native pass or multiplayer result is claimed by this independent review.

Both revisions make the important economic and defense programmes more concrete and materially larger. Their strongest balance safeguards are named-site investments, one-time GDP fees, finite research uses, meaningful route alternatives, actual MD equipment families, and whole-transaction guards. Full live-game balance, cost pressure, and effect presentation still depend on the root's native results.

## Parent verification addendum

After this independent content review, the parent recorded a passing combined source check, 37/37 targeted native assertions and 49/49 existing source-model regressions. The two bounded rebuilds are byte-identical to the native-tested files. An intermediate pre-assertion game-start crash is retained in ENGINE_ATTEMPT_2.json; no cause is established. These are parent results rather than additional tests run by the independent reviewer. Coverage boundaries and exact hashes are in FINAL_CHECKS.json and ENGINE_REPORT.json.
