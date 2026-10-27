# Staged effects implementation review

Generated from 212 National life/Economy records.

These fragments are staging only; they are not game-loaded.

Emitted 212 per-focus helpers and native display previews.

## Implemented

- Every focus preview is an unconditional native `effect_tooltip` sibling to the independently guarded `hidden_effect` payout. Preview bodies contain the same treasury changes, modifier-variable deltas, research bonuses, shared slots, and buildings as the payout without receipt or availability guards.
- `national_economy_focus_effect_previews.json` is the machine-readable mapping for root focus-graph integration; its `effect_tooltip` value is the inner body keyed by design focus ID.
- Treasury deductions use MD's `treasury_change` temporary variable and `modify_treasury_effect`; there is no cash-on-hand gate or direct debt manipulation.
- Research bonuses use Japan's native `add_tech_bonus` shape for one `CAT_industry` or `CAT_agriculture` technology.
- Four pollution focus improvements adjust the initialized persistent pollution modifier, which starts at stability −5% and health spending +8%.
- The initialized energy modifier starts at civilian factory energy use +10% and civilian productivity −3%. The `efficient_factories` focus's −5% energy-use special modifies this same modifier variable.
- Building caps and `shares_slots` behavior are transcribed from `common/buildings/00_buildings.txt`. All 14 inventory building types are state-level and use `state_max`; none use `province_max`.
- Every building helper and availability fragment requires current state ownership/control. `building_level@type` checks the building's current level against remaining `state_max`; the installed `free_building_slots` trigger checks available construction levels. Shared-slot buildings use `include_locked = no` only when a slot is still needed; non-shared buildings omit this option. A focus-awarded shared slot supplies its own required capacity.
- The `fuel_silo` grant of two levels requires `building_level@fuel_silo < 4` and `free_building_slots = { building = fuel_silo size > 1 }` (max 5). Energy and industrial grid buildings both enforce their shared `infrastructure_keystone` group limit of one.
- Licensed Production requires `has_idea = COLDWAR_ni_licensed_armaments_programme`; Expand Microelectronics Capacity requires `has_tech = microchip_production_1`. Both requirements appear in availability and helper reward guards.
- Technical `original_tag = JAP` and `IMP_is_1970_scenario = yes` checks are hidden in focus availability and retained in reward guards. Receipt flags are set after all scenario, focus-specific, ownership/control, and capacity guards pass.
- Source audits reconciled all 353 percent tokens against 350 mapped modifiers and 3 tech bonuses; the four percentage-point pollution specials are mapped separately. All 37 building entries match their state names and quantities in the effect text.
- Five `air_detection` rewards and three `planning_speed` rewards use percentage-valued native modifiers. `documentation/modifiers_documentation.md` lists these values, and `localisation/english/MD_dm_modifiers_l_english.yml` displays each with percent formatting.
- Explicit building quantities are sourced from `common/buildings/00_buildings.txt`: fossil plants 2 GW / 3,360 fuel per week; fuel silos 200,000 fuel and 500 storage per level; reactors 4 GW / 40 nuclear fuel per week; renewable plants 0.5 GW.
- Section modifiers and two starting modifiers have existing MD icons and English name keys.

## Unsupported or unverified
- Inventory `matched = 0` (no ordinary modifier phrase matched) for: `national_4_escort_yard_modernisation`, `national_4_factory_modernisation`, `national_5_the_pollution_diet`, `national_5_compensate_affected_communities`, `national_5_medical_certification`, `national_9_agricultural_research`, `national_10_collaborative_industrial_research`, `national_10_specialist_research_teams`, `kansai_redevelopment`, `tohoku_development`, `hokkaido_development`. Each is emitted through its inventory cost, building, pollution special, or research bonus entry.

- No unsupported special effects or research categories remain. Static emission does not establish engine validity.

## Source audit references

- Installed HOI4 `documentation/triggers_documentation.md` says `free_building_slots` checks available construction levels and that `include_locked` is an optional parameter for buildings using shared slots.
- Installed HOI4 `documentation/effects_documentation.md` defines `add_extra_state_shared_building_slots` as a STATE effect that adds shared slots. Native focus examples in `common/national_focus/05_japan.txt`, `05_china.txt`, and `05_belarus.txt` add slots before construction.
- Installed HOI4 `documentation/dynamic_variables_documentation.md` defines `building_level@<building>` as the current level of that building in a state. `common/scripted_triggers/00_investment_scripted_triggers.txt` also uses this dynamic variable in `check_variable`.

## Limits

- Article 9 amendment focuses are outside the 212-record `effect_inventory.json`; their timed 365/730-day effects are not generated here.
- The scripts pass source-level checks but were not parsed or exercised in a live HOI4 run.
- The pollution/energy starting initializer must be called at country setup to show the starting spirits at game start. Each generated focus helper also calls it idempotently as a fallback.
- Outputs remain staging fragments; no game-loaded file was changed.
