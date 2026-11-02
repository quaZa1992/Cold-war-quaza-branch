# IMPERIA COLD WAR

# France 1970 GDP reward redesign review

**Reviewed input:** `tools/france_1970_design/concept.json`, FRA2 concept 1.2, 152 focuses, SHA-256 `4f57a4c6e3d13eba6b7ec4129cb81fd8b9a2a645e9fac10c5ebf8d36588c18b5`. The review compares the current data with `GDP_REWARD_BASELINE.json`, `NATO_PRESERVATION.json`, the reward and asset references, and current local MD source. This is a static source and design-data review. No generator, builder, loaded game file, or concept data was changed. No game, parser, or browser checks were run by this reviewer.

## Review result

The new fiscal schema is internally consistent in the current focus and offer data. I checked 74 focus-level `treasury_gdp` effects, 19 offers on both signatory sides, and every recurring expense literal. There are no flat Treasury effect kinds. Every one-time charge uses the payer's own `gdp_total` at payment, is once-only, and has `percent / 100 == gdp_fraction`. Every recurring stream uses its payer's own `gdp_total`, annual share divided by 52, weekly recalculation, and no more than five fractional digits; the share and stored fraction agree. The policy matches MD's annual GDP base and weekly expense units described in `GDP_COST_REFERENCE.md`.

All 36 local focus construction effects and all offer construction effects specify `slots == amount`, slots before construction, and once-only execution. The current strict-JSON baseline comparison found all 152 focus keys still present, with no changes to group, prerequisite, exclusion, or coordinates. The reward revision is represented in effects and offer terms, not graph changes. No additional permanent research slot or advanced equipment stockpile was added.

This remains a concept contract, not active runtime. The focus and offer records name the intended transaction, payer, guard, and preview terms, but no implementation currently performs the GDP charge, weekly stream, recipient approval, or paired suspension/restoration. Native source evidence validates the keys and patterns; it does not prove that the unimplemented custom effects work in game.

## GDP pricing and affordability

The money-system source describes `gdp_total` in billions and rebuilds `additional_expenses_rate` as a weekly aggregate (`common/scripted_effects/00_money_system.txt:3697-3706, 4708-4717`; GDP description at `:4795`). Native French/UK/Iraqi focus examples calculate GDP-relative payments (`GDP_COST_REFERENCE.md`, source anchors there). The current proposal correctly separates payment and service budget:

- Setup: at acceptance, debit each signatory's own `gdp_total` multiplied by its signed `gdp_fraction` once. A partner's share is not computed from French GDP.
- Programme: store an annual GDP share and add `own gdp_total * gdp_fraction / 52` to that country's stream on each weekly rebuild while active. Suspension contributes zero. A restore restarts the stream without setup fees or finite awards.
- Construction: the native `add_building_construction` helper has no MD Treasury fee parameter; native France examples pair construction and a separate `modify_treasury_effect` (`GDP_COST_REFERENCE.md`, `common/national_focus/05_france.txt:1048-1064,1503-1527`). Thus the proposal's separate one-time GDP charge is not a duplicate MD-helper bill. It still needs a single transaction receipt so slots and levels cannot be granted twice.
- Availability: the concept explicitly adds no Treasury-balance gate. Keep an internal GDP-initialization guard from becoming a fixed-price fallback or a player-facing affordability requirement.

The highest one-focus fee is 0.8% of GDP (`public_combine`); other large one-off projects are 0.75% (`nuclear_scale`) and 0.6% each for TGV, motorways, regional industry, diverse energy, and champion model. The family-limited offer data has ten families. If one alternative in every family is signed, the sum of the largest French setup shares is 2.10% of French GDP and the French annual programme shares sum to 0.57% of French GDP per year. The equivalent recipient figures are 1.76% of the respective recipients' own GDP and 0.42% per year, but they span different countries and should not be presented as one country's total. Summing all 19 alternatives produces 0.99% French annual share and is not a reachable package. These are design maxima before testing family/focus path reachability, player choice, current GDP, and any concurrent native spending.

Keep the full shared-expense and party-path budget visible in implementation previews. The stream is an appropriation added to other native weekly expenses, not an automatic annual budget line in the treasury. The current fields are concise enough for this calculation, but offer preview rendering must calculate and display each signatory's actual current weekly MD amount without rounding a small amount to zero.

## Native modifier and research verification

The reward set uses real local provider/consumer keys and registered category tags. The current key inventory is recorded in `mechanics_reference.md`, `verified_effects.json`, `GDP_COST_REFERENCE.md`, and `NATO_MECHANICS.md`. Targeted source checks confirmed the revised categories and new energy/research rewards:

| Concept entry | Source check | Finding |
| --- | --- | --- |
| `CAT_electronics`, `CAT_industry`, `CAT_armor`, `CAT_aircraft`, `CAT_naval`, `CAT_nuclear_reactors` | Registered in `common/technology_tags/00_technology.txt:25-205`; examples and France bonus idioms in `mechanics_reference.md:25-29` | Valid, real tech categories. The concept's limited bonuses are finite by `uses`; they do not add research slots. |
| `CAT_energy` | Registered at `common/technology_tags/00_technology.txt:185`; many actual technologies in `common/technologies/industry.txt:1352+` | Valid research category for the ecology branch. |
| `CAT_infrastructure` | Registered at `common/technology_tags/00_technology.txt:194`; real technologies in `common/technologies/industry.txt:3821+`, `common/technologies/mdcw_early_railway.txt:27-74`, and `common/technologies/mdcw_industry_1968_1985.txt:21` | Valid limited research category for TGV. It does not require or grant the 1990 `rail_terminal`. |
| `production_speed_nuclear_reactor_factor` and `nuclear_energy_generation_modifier` | French native ideas at `common/ideas/05_france.txt:619-620`; energy formula and modifier definition at `common/scripted_effects/!_energy_effects.txt:474-499` and `common/modifier_definitions/energy_modifier_definitions.txt:122-127` | Exact separate effects: reactor build time versus output per active reactor. Neither grants a reactor, uranium, or fuel. |
| `energy_gain_multiplier`, `energy_use_modifier_civs` | The energy aggregator is in `common/scripted_effects/!_energy_effects.txt:254,319-368`; consumer formulas are summarized in `verified_effects.json` | Valid separate generation and civilian demand modifiers. Demand reduction is not free generation. |
| `offices_productivity` | Native modifier definition `common/modifier_definitions/money_modifier_definitions.txt:402`; France idea example `common/ideas/05_france.txt:411` | Valid offices-sector productivity. It is distinct from generic factory output or build speed. |
| `training_time_army_factor`, `army_org_factor`, `army_core_defence_factor`, `supply_consumption_factor`, `equipment_cost_multiplier_modifier`, `army_org_regain`, `max_planning` | Native providers and consumers are cited in `mechanics_reference.md:23-29` and `NATO_MECHANICS.md:26-39` | Valid narrow military/logistics keys. Use signs carefully: positive equipment, service, or supply multipliers increase recurring costs; negative values save costs. |

The revised focus nodes contain 45 distinct modifier keys. The category and modifier inventory had no unknown key or abstract research alias in the audited focus rewards. No broad attack, defence, morale, or organization reward was added in the new NATO branch; its effects stay on procurement, planning, logistics, accident risk, doctrine and finite research. Existing France examples show the keys are recognized, not that the concept's exact percentages are balanced in a live campaign.

## Buildings, providers, and one timing issue

The metropolitan targets and state names are consistent with the exact 1970 history inventory in `REWARD_ASSET_REFERENCE.md` and `mechanics_reference.md:11-15`: 54 Hauts-de-France, 55 Normandie, 56 Ile de France, 57 Alsace-Lorraine, 58 Bourgogne, 59 Loire, 60 Aquitaine, 61 Midi Pyrenees, 62 Rhone-Alpes, 63 Provence, 64 Bretagne, 65 Corsica. The two port upgrades use provinces 6449 (Normandie/55) and 6536 (Bretagne/64); the southern naval base is province 11834 in Provence/63. The reference confirms the state/province membership, 1970 ownership/control, current level, native cap, and base slot headroom. Future runtime must still re-check live ownership, control and capacity; current source data alone cannot establish the state remains available after play begins.

Offer assets are recorded for both sides, including France state 61 and German state 1080 for Airbus, France state 56 and German state 42 for Symphonie, and French state 57 plus German state 42 for Rhine. The records correctly carry one slot per level. The bilateral transaction note asks to validate both recipients' ownership/control and capacity before charging either side, which is essential for an atomic acceptance. The proposed Symphonie internet station is explicitly guarded by `internet_1` for France and Germany. `common/technologies/engineering.txt:1779-1790` gives that technology a 1975 start year and unlocks `internet_station`; the building definition and later levels are in `common/buildings/00_buildings.txt:93-107` and engineering technology progression. This is a meaningful post-1975 gate for the focus and offer, not an immediate 1970 building.

Other changed asset shapes stay within the described 1970 system: TGV grants infrastructure plus a finite `CAT_infrastructure` bonus rather than the 1990 rail terminal; the replacement naval assets are actual coastal port upgrades; fossil power uses `fossil_powerplant`; energy efficiency uses generation/research or existing hydro infrastructure rather than an early `renewable_energy_infra` building. These are concept-level target checks, not engine-tested construction transactions.

## Recipient offers and lifecycle contract

There are 19 offer records, each linked to a distinct French focus. Every offer has separate `france` and `recipient` spirit/effect lists and now explicitly contains `acceptance_conditions`, `acceptance_transaction`, `payment_contract`, and `asset_execution`. The acceptance conditions across all 19 require named-recipient consent, both countries to exist, bilateral peace, no mutual native embargo or any of the four mirrored Imperia sanctions, an unapplied valid proposal, and full ownership/control plus native construction and slot capacity for promised assets. Each also adds its specific gate where relevant, such as `internet_1`, an active parent agreement, or NATO membership. The transaction text requires acceptance-time rechecks, each payer's current GDP, both-side atomic once-only charges and rewards, slots before construction, and no balance gate or restoration replay. Both parties' setup and annual weekly shares are separately scoped to their own GDP. The schema check found no missing offer field among these four records.

These are complete concept-level transaction contracts, not active runtime. Implementation still has to enforce the acceptance rechecks, mutual embargo/sanction predicates, GDP initialization, full-control and capacity checks, atomic idempotence, and one-time receipts. The preview must show both complete prospective effect lists, setup charges, recurring charges and construction slots while locked, unsigned or suspended, while preview code remains non-executing.

`additional_expenses_rate` is a rebuilt aggregate, not durable agreement state. Its active weekly consumer must read a persistent treaty/programme variable and include each share once (`GDP_COST_REFERENCE.md`, native precedent `common/scripted_effects/00_money_system.txt:3697-3706,4431-4435`). No custom France stream, response decision, cross-country payment, or suspension reconciler is active yet.

## Reachable balance and unresolved runtime evidence

Because the reward rewrite changes many numerical values, the previous 134-focus modifier ceilings are not current ceilings. I recomputed focus-only bounds using the concept's nested prerequisite representation as OR alternatives within each prerequisite group, while separate groups and exclusions still constrain reachability. For each ruling-party route I combine the compatible shared groups, that party's programme, and the NATO sub-branch only for UDR, because both occupy the same slot and the NATO branch itself requires UDR. External parent-group availability is treated as obtainable. Values exclude starting spirits and all bilateral spirits, and each modifier is maximized independently. These are static upper bounds, not one coherent package or a campaign simulation.

| Modifier | Maximum route | Static concept upper bound | Balance interpretation |
| --- | --- | ---: | --- |
| `political_power_factor` | PS | +0.25 | Policy multiplier assembled from the PS route and compatible shared choices. |
| `bureaucracy_cost_multiplier_modifier` | PS | +0.28 | A 28% increase to the relevant recurring bureaucracy bill, not a direct Treasury charge. |
| `education_cost_multiplier_modifier` | Radical | +0.26 | A 26% increase to the education bill. |
| `social_cost_multiplier_modifier` | PS | +0.37 | A 37% increase to the social-spending bill; scrutinize the full route cost. |
| `production_factory_efficiency_gain_factor` | UDR + NATO branch | +0.30 | Efficiency growth rate, not output or construction speed. Includes same-slot UDR/NATO-compatible programme choices. |
| `civilian_factories_productivity` | UDR | +0.16 | GDP/productivity contribution from civilian factories. |
| `production_speed_infrastructure_factor` | Centre | +0.16 | Build time for infrastructure. |
| `equipment_cost_multiplier_modifier` | UDR + NATO branch | +0.27 | Increase to the existing equipment bill; an expensive but selectable UDR/NATO path. |
| `army_org_factor` | Any party route | +0.09 | Compatible defence choices: Balanced Forces (+0.05) and Professional Intervention Core (+0.04). |
| `army_core_defence_factor` | National Right | +0.14 | Focus-only static ceiling, before any external spirits. |
| `training_time_army_factor` | PSU | +0.13 | Training-time factor from the PSU plus compatible shared defence choices. |
| `supply_consumption_factor` | UDR | -0.07 | Lower supply consumption from compatible UDR and shared choices. |

These values should be checked with starting spirits and signed agreements before release. In particular, historical `After the 1969 Devaluation` adds temporary output and construction penalties; the starting stability total is negative. The new choices also include actual budget trade-offs rather than uniformly beneficial cost reductions. Treaty modifiers are outside the table and can add to route totals: for example, Atlantic Training adds +0.04 `army_org_regain`, while the chosen NATO agreement may add organization regain, supply, personnel cost, or accident-rate effects. The current agreement fee/weekly schema changed, so use current offer percentages here, not older fixed MD-dollar totals in `NATO_REVIEW.md`.

One compatibility note: `Symphonie` and the local `telecoms` focus both need `internet_1`. The French tech gate is valid, but it means the tree cannot deliver the telecom asset before the player researches a 1975-base-year tech. Symphonie also requires Germany to have it before the focus is available. Keep that explicit in previews and acceptance checks; do not imply the satellite agreement is immediately available at the January 1970 start.

## Scope boundary

The review verifies current source definitions and concept arithmetic. The custom France runtime still needs implementation of focus transactions, dual-country consent, dynamic weekly expenses, full preview effects, asset validation, party activation, and all suspension/restoration rules. None of those design strings establishes game-load or multiplayer correctness. The parent-reported browser QA is not attributed to this review.
