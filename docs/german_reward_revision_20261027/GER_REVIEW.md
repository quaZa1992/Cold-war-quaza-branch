IMPERIA COLD WAR

# West German reward revision review

## Scope and ownership

This is a GER-only reward overlay for 54 existing focus IDs, plus a correction to the existing GER Energy Mix modifier mapping. The source tree remains the owner of the focus nodes. The bounded installer renders canonical GER content in memory and patches only these runtime outputs:

- `common/national_focus/COLDWAR_GER_1970_focus.txt`
- `localisation/english/COLDWAR_GER_1970_l_english.yml`
- `common/dynamic_modifiers/COLDWAR_GER_1970_dynamic_modifiers.txt`, only `COLDWAR_GER_1970_core_energie`
- `common/scripted_effects/COLDWAR_GER_1970_trust_cleanup.txt`, only the retired-trust cleanup effect

The bounded installer wrote the approved GER outputs. The final dry-run reports no pending writes. Its last focus update changed only BAföG, Works Constitution and Barzel social-market requirements to native MD party triggers, and retained the corrected Mannheim-before-LaFontaine anchor order. The trust cleanup regression passes 6/6. The parent native rerun passed all 37 targeted assertions; see ENGINE_REPORT.json for exact coverage. An AST pass also added missing shared slots to the selected original Patriot and NATO AWACS construction rewards before each grant. Focus IDs, positions, times, prerequisites, exclusions, historical leaders, security mechanics, sandbox and DDR rivalry remain unchanged.

The canonical reward source is [reward_overlay.py](../../tools/west_germany_1970/reward_overlay.py). The bounded writer is [install_reward_overlay.py](../../tools/west_germany_1970/install_reward_overlay.py). The complete per-focus package, original building map, gates, costs, receipts and modifier values are recorded in [GER_CHANGES.json](GER_CHANGES.json).

## What changed in play

The old rewards stay in place. Each revised focus now previews its complete old reward and its added package under a native effect tooltip. The completed-focus payout runs both together under one receipt-guarded transaction.

The additions give players paid, named-state assets, finite one-use research bonuses, production-cost changes for equipment families, and signed changes to existing GER programme cores. They emphasize the decisions already represented by the tree:

- Economic choices add industrial capacity and research support. The 1975 stimulus package costs 0.3% of current GDP, while austerity costs 0.1%. The focus already selects between debt-financed demand and treasury revenue, respectively.
- Coal support, Soviet gas, nuclear construction and energy conservation have different Energy Mix effects. Nuclear expansion costs capital and can add protest and consumption pressure. Renewables cost capital and improve renewable output while shifting the nuclear or fossil mix. The nuclear moratorium and fast-breeder focus remain mutually exclusive.
- Research policy and microelectronics use limited-use research bonuses. The microchip plant requires its real installed unlock and enough researched tier capacity. Renewable and reactor construction require their real enabling technologies.
- Military choices add factories and limited equipment bonuses for the relevant research or production family. W15 and W18 remain mutually exclusive. The overlay adds no conscription-factor increase, avoiding an implausible jump in recruitable population.
- SPD programmes at BAföG and the Works Constitution use the native western_social_democrats_are_in_power requirement; Barzel's CDU social-market programme uses western_conservatism_are_in_power. The existing CDU grand-coalition condition and Green-government environmental programmes retain their party or coalition requirements. These are one-time investment packages. Their permanent receipt prevents a former government from replaying their cash and assets after returning to office.

All new cost examples use the scenario's 1970 GER starting GDP of 216.629 billion. A 0.1% package is 0.216629 billion; 0.2% is 0.433258 billion; 0.3% is 0.649887 billion; 0.5% is 1.083145 billion; and 0.6% is 1.299774 billion. Each preview calculates the charge from current GDP, not the starting value. Package costs are one-time; no new weekly expense or treasury cash affordability gate was added.

Summing all 54 incremental packages gives 13.0% of starting GDP, or 28.162 billion. That sum is an unreachable upper bound, not a route: it includes separate party branches, disconnected programmes, and mutually exclusive stimulus/austerity, fast-breeder/moratorium and W15/W18 decisions. Coherent example routes include their existing GDP-scaled charges and are calculated at frozen starting GDP for scale. Runtime charges recalculate at each focus completion.

| Route example | Overlay packages | Existing treasury cost or revenue | Gross or net cash at frozen starting GDP |
|---|---:|---:|---:|
| SPD stimulus and high technology | 3.2% GDP | 1.0% cost, plus 0.6% GDP debt | 4.2% gross cash, about 9.098 billion, plus about 1.300 billion debt |
| SPD austerity and high technology | 3.0% GDP | 1.0% cost, 0.4% revenue | 3.6% net cash, about 7.799 billion |
| Coal and century contracts | 0.7% GDP | 0.2% cost | 0.9% cash, about 1.950 billion |
| Nuclear expansion through fast breeder | 1.3% GDP | None | 2.816 billion |
| Moratorium and renewable transition | 1.6% GDP | 0.2% cost | 1.8% cash, about 3.899 billion |
| Army modernization with air defence and Tornado route | 4.0% GDP | 0.3% cost | 4.3% cash, about 9.315 billion |
| Type 209 and F122 procurement | 0.6% GDP | None | 1.300 billion |

These totals add package GDP fractions, then report pre-existing treasury charges and revenue separately. They exclude focus point time and cannot predict later nominal GDP. The exact focus sets and receipts are in the manifest. Parent review should assess stacking against the native focus graph before installation.

## Whole-package gates and receipts

The original visible focus requirements remain visible. The overlay adds visible named-state ownership, control, real state capacity, and relevant specialty building technology requirements. It uses the current installed MD building caps and technology tiers through [programme_assets.py](../../tools/german_reward_revision_20261027/programme_assets.py). Dockyards require coastal states. Original fixed-state construction and added construction are coalesced by state and building type before capacity checks, so the gate covers the complete building payout rather than only the new package.

Every added building level receives one extra shared state slot before construction. An AST pass also adds missing slots to original construction in the selected focus rewards, including Patriot radar and anti-air buildings and NATO AWACS radar/air-base construction. Specialty unlocks are amount-aware: adding more levels requires a technology that actually unlocks the requested total. No focus grants uranium output or free nuclear, renewable or microchip assets.

Only GER identity, scenario routing, GDP validity and the replay receipt are hidden. The same execution guard also checks the focus's original availability, positive GDP and the full site/capacity/technology bundle. The receipt is set before both the original reward and the added package run, preventing partial payment and replay after party changes. A focus cannot grant a partial package when state control, building cap or technology changes between availability and completion.

## Energy Mix unit correction

The existing focus prose presents `cwfo_energie_fossil` and `cwfo_energie_nuclear` as percentage changes. The old GER dynamic modifier connected them to flat `fossil_fuel_consumption` and flat `nuclear_energy_gain`. The 0.05 value therefore did not mean a 5% change. The source now maps those variables to the installed percentage modifiers `fossil_pp_fuel_consumption_modifier` and `nuclear_energy_generation_modifier`. This is a GER-only correction to the Energy Mix block; the shared main MD files are untouched. It makes existing and new focus percentages use the scale shown to players.

## Historical basis and installed MD references

The reward themes follow the documented sources and historical caveats in [HISTORICAL_AND_MD_REFERENCES.md](HISTORICAL_AND_MD_REFERENCES.md). Selected source focus IDs are `COLDWAR_GER_1970_bafoeg`, `..._works_constitution`, `..._codetermination`, `..._social_market`, `..._concerted_action`, `..._stimulus_1975`, `..._austerity_1975`, `..._energy_programme`, `..._kohlepfennig`, `..._nuclear_buildout`, `..._fast_breeder`, `..._nuclear_moratorium`, `..._renewable_research`, `..._feed_in_law`, `..._microelectronics`, `..._army_structure_3`, `..._leber_modernisation`, `..._leopard_2`, `..._conscription_w15`, `..._conscription_w18`, `..._tornado`, `..._type_209` and `..._f122_frigates`.

The installed main MD references include `common/buildings/00_buildings.txt` for native state caps, `common/technologies/industry.txt` for reactor and power unlocks, `common/technologies/engineering.txt` for microchip unlocks, `common/technologies/nuclear.txt` for nuclear research categories, `common/technologies/fixed_wing.txt` for aircraft research, `common/units/equipment/MD_x_plane_airframes.txt` for the legacy `Strike_fighter` equipment and its `medium_plane_airframe` archetype, and `history/units/GER_2000_bba.txt` for the BBA Tornado `medium_plane_cas_airframe_1` variant. The Tornado package therefore uses the actual medium-plane family cost modifier and verified `CAT_aircraft` research category; it does not apply a generic fighter-only discount.

Main MD focus examples used as scale references are recorded with exact IDs and costs in the shared research note: `GER_expand_mainstream_industry`, `GER_education_investments`, `GER_army_defence_exercise`, `GER_Armored_Delay`, `GER_economic_growth`, `GER_bundeswehr_reforms`, `SOV_gen_3_nuclear_plants` and `GENERIC_self_propelled_artillery`. The note treats them as mechanic examples, not historical evidence.

## Review boundary

The bounded render checked generator composition, snapshot compatibility, native script parsing, output markers, focus IDs and changed-file footprint. The trust cleanup regression passes 6/6. No broad project generator was run. The parent agent owns the final native fixture rerun, independent review and validation of the latest requirement update.

## Parent final verification

The final combined source check passed. All 37 targeted native assertions and all 49 existing source-model regression tests passed. Both bounded canonical rebuilds produced byte-identical runtime files to the successful native fixture. One intermediate game launch crashed before fixture execution; its crash profile and report are retained separately. No crash cause or full multiplayer result is claimed. See [FINAL_CHECKS.json](FINAL_CHECKS.json) and [IMPLEMENTATION.md](IMPLEMENTATION.md).
