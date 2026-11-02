IMPERIA COLD WAR

# North Korea 1970 reward revision

Date: 27 October 2026  
Scope: canonical 360-focus DPRK model, NKO bilateral offers and source compiler. South Korea and Japan remain outside this source-only handoff.

## Change summary

The deliberate overlay in `tools/north_korea_1970/reward_revision.py` applies after the existing expansions. It preserves the 360 focus IDs, coordinates, prerequisite graph, exclusions, party visibility and execution gates, 1994 succession, historical starting leader, portraits, and existing bilateral consent, setup-price and weekly-fee rules. The overlay touches 39 focus records and adds a mechanical reward or cost change to 35 of 360 focuses (9.7%). It adds 15 domestic building levels with matching shared slots, 8 single-use research grants, and 12 focused equipment cost targets across relevant factory families. The mutually exclusive heavy, consumer and balanced priorities now each add a distinct asset or equipment-saving package.

The overlay uses separate building-specific ownership, control, capacity and coastal checks. Each added building level receives one shared slot in the same state before construction; original construction effects are preserved. No workforce-size penalty, uranium production, uranium mine, nuclear weapon, or readiness-stock reward is introduced.

## Internal focus inventory

Costs are one-time shares of current GDP. Existing signed modifiers are shown as script API keys and values from the pre-overlay design. “Overlay and after” gives additions or revised values and the new one-time cost. Bonus numbers are native MD API values, not guessed percentage conversions. All 39 affected IDs are listed, including four description-only clarifications.

| Focus ID | Before | Overlay and after | One-time cost |
|---|---|---|---:|
| `COLDWAR_NKO_heavy_priority` | production_speed_arms_factory_factor +0.12; production_factory_max_efficiency_factor +0.08; agricolture_productivity_modifier -0.06; energy_use_multiplier +0.08 | artillery_equipment build_cost_ic -0.05; medium_tank_chassis build_cost_ic -0.04 | 0.5% -> 0.5% |
| `COLDWAR_NKO_light_priority` | agricolture_productivity_modifier +0.12; production_speed_industrial_complex_factor +0.1; production_speed_arms_factory_factor -0.08; social_cost_multiplier_modifier +0.05 | +1 agriculture_district level, +1 shared slot (states 603, 602) | 0.5% -> 0.625% |
| `COLDWAR_NKO_balanced_priority` | productivity_growth_modifier +0.08; production_factory_efficiency_gain_factor +0.06; production_speed_buildings_factor -0.04; bureaucracy_cost_multiplier_modifier +0.05 | +1 industrial_complex level, +1 shared slot (states 602, 1200) | 0.5% -> 0.625% |
| `COLDWAR_NKO_steelworks` | 1 arms_factory level(s), 1 slot(s) | +1 arms_factory level, +1 shared slot (states 602, 601) | 1.88% -> 2.25% |
| `COLDWAR_NKO_food_district` | 1 agriculture_district level(s), 1 slot(s) | +1 agriculture_district level, +1 shared slot (states 603, 602) | 1.25% -> 1.5% |
| `COLDWAR_NKO_machine_tools` | production_factory_max_efficiency_factor +0.06; education_cost_multiplier_modifier +0.04 | one-use CAT_industry bonus 0.5 (1 use) | 0.5% -> 0.5% |
| `COLDWAR_NKO_power_grid` | energy_use_multiplier -0.08 | one-use CAT_renewable_energy bonus 0.5 (1 use) | 0.5% -> 0.5% |
| `COLDWAR_NKO_fertilizer` | agricolture_productivity_modifier +0.08; energy_use_multiplier +0.04 | +1 agriculture_district level, +1 shared slot (states 603, 602) | 0.5% -> 0.625% |
| `COLDWAR_NKO_technical_schools` | research_speed_factor +0.04; education_cost_multiplier_modifier +0.06 | one-use CAT_electronics bonus 0.5 (1 use) | 0.25% -> 0.25% |
| `COLDWAR_NKO_lessons_1969` | experience_gain_army +0.06; army_personnel_cost_multiplier_modifier +0.03 | Description clarifies the existing route and its trade-off | 0% -> 0% |
| `COLDWAR_NKO_munitions_directorate` | army_artillery_attack_factor +0.05; production_speed_arms_factory_factor +0.04; social_cost_multiplier_modifier +0.03 | artillery_equipment build_cost_ic -0.05 | 0.875% -> 0.875% |
| `COLDWAR_NKO_artillery_works` | 1 arms_factory level(s), 1 slot(s); production_speed_arms_factory_factor +0.06; equipment_cost_multiplier_modifier +0.04; energy_use_multiplier +0.04 | +1 arms_factory level, +1 shared slot (states 602, 601) | 1.4% -> 1.65% |
| `COLDWAR_NKO_kpa_engineer_corps` | army_core_defence_factor +0.06; supply_consumption_factor -0.04; bureaucracy_cost_multiplier_modifier +0.04 | Description clarifies the existing route and its trade-off | 1% -> 1% |
| `COLDWAR_NKO_kpa_command_schools` | experience_gain_army +0.06; army_org_factor +0.04; education_cost_multiplier_modifier +0.05 | Description clarifies the existing route and its trade-off | 1% -> 1% |
| `COLDWAR_NKO_soviet_machine_standards` | production_factory_efficiency_gain_factor +0.05; research_speed_factor +0.025; foreign_influence_defense_modifier -0.03 | one-use CAT_industry bonus 0.5 (1 use) | 0.875% -> 0.875% |
| `COLDWAR_NKO_three_revolutions` | production_factory_efficiency_gain_factor +0.08; bureaucracy_cost_multiplier_modifier +0.06 | one-use CAT_electronics bonus 0.5 (1 use) | 0% -> 0% |
| `COLDWAR_NKO_engineer_commissions` | production_factory_max_efficiency_factor +0.06; bureaucracy_cost_multiplier_modifier +0.04 | Description clarifies the existing route and its trade-off | 0% -> 0% |
| `COLDWAR_NKO_cabinet_engineering_colleges` | research_speed_factor +0.05; productivity_growth_modifier +0.04; education_cost_multiplier_modifier +0.06 | one-use CAT_electronics bonus 0.5 (1 use) | 1% -> 1% |
| `COLDWAR_NKO_yanan_machine_repair` | production_factory_efficiency_gain_factor +0.06; production_factory_max_efficiency_factor +0.04; bureaucracy_cost_multiplier_modifier +0.04 | +1 industrial_complex level, +1 shared slot (states 602, 1200) | 0.875% -> 1% |
| `COLDWAR_NKO_jongil_industrial_repair` | industrial_capacity_factory +0.06; production_factory_efficiency_gain_factor +0.05; non_electric_fuel_consumption_modifier +0.06 | +1 industrial_complex level, +1 shared slot (states 602, 1200) | 1% -> 1.12% |
| `COLDWAR_NKO_jongil_distribution` | agricolture_productivity_modifier +0.06; stability_factor +0.04; social_cost_multiplier_modifier +0.06; tax_gain_multiplier_modifier -0.03 | +1 agriculture_district level, +1 shared slot (states 603, 602) | 0.75% -> 1% |
| `COLDWAR_NKO_kdp_industrial_standards` | production_factory_efficiency_gain_factor +0.07; research_speed_factor +0.025; bureaucracy_cost_multiplier_modifier +0.05 | one-use CAT_industry bonus 0.5 (1 use) | 0.875% -> 0.875% |
| `COLDWAR_NKO_chondo_cooperative_irrigation` | agricolture_productivity_modifier +0.1; bureaucracy_cost_multiplier_modifier +0.07; social_cost_multiplier_modifier +0.04 | +1 agriculture_district level, +1 shared slot (states 603, 602) | 1% -> 1.12% |
| `COLDWAR_NKO_chondo_granary` | agricolture_productivity_modifier +0.05; social_cost_multiplier_modifier +0.05 | +1 agriculture_district level, +1 shared slot (states 603, 602) | 0.5% -> 0.625% |
| `COLDWAR_NKO_mobile_army` | army_org_factor +0.08; max_planning_factor +0.08; equipment_cost_multiplier_modifier +0.12; army_fuel_consumption_factor +0.08; modifier_army_sub_unit_Mot_Inf_Bat_attack_factor +0.06; modifier_army_sub_unit_Mech_Inf_Bat_attack_factor +0.06 | medium_tank_chassis build_cost_ic -0.07 | 0% -> 0% |
| `COLDWAR_NKO_mass_artillery` | supply_consumption_factor +0.08; equipment_cost_multiplier_modifier +0.05; army_artillery_attack_factor +0.06; modifier_army_sub_unit_SP_R_arty_Bat_attack_factor +0.06 | artillery_equipment build_cost_ic -0.05 | 0.5% -> 0.5% |
| `COLDWAR_NKO_ammunition_standards` | production_factory_max_efficiency_factor +0.06; production_factory_efficiency_gain_factor -0.04; army_artillery_attack_factor +0.04; modifier_army_sub_unit_SP_R_arty_Bat_attack_factor +0.04 | artillery_equipment build_cost_ic -0.04 | 0.25% -> 0.25% |
| `COLDWAR_NKO_fighter_conversion` | air_accidents_factor -0.05; air_superiority_efficiency +0.06; education_cost_multiplier_modifier +0.04 | fighter build_cost_ic -0.07 | 1% -> 1% |
| `COLDWAR_NKO_dispersed_airfields` | air_interception_detect_factor +0.05; air_accidents_factor -0.04; production_speed_industrial_complex_factor -0.03 | fighter build_cost_ic -0.05 | 1% -> 1% |
| `COLDWAR_NKO_naval_workshops` | 1 dockyard level(s), 1 slot(s) | +1 dockyard level, +1 shared slot (states 601, 1199); naval_bomber build_cost_ic -0.06 | 1.88% -> 2% |
| `COLDWAR_NKO_armour_mobility_drills` | army_org_factor +0.05; modifier_army_sub_unit_Mot_Inf_Bat_attack_factor +0.04; army_fuel_consumption_factor +0.04 | medium_tank_chassis build_cost_ic -0.05 | 0.875% -> 0.875% |
| `COLDWAR_NKO_air_warning_network` | air_interception_detect_factor +0.08; static_anti_air_damage_factor +0.04; energy_use_multiplier +0.03 | +1 radar_station level, +1 shared slot (states 601, 1200) | 0.875% -> 1% |
| `COLDWAR_NKO_cabinet_imported_generators` | productivity_growth_modifier +0.06; trade_opinion_factor +0.08; foreign_influence_defense_modifier -0.07 | +1 fossil_powerplant level, +1 shared slot (states 602, 601) | 1.5% -> 1.75% |
| `COLDWAR_NKO_christian_clinic_service` | health_cost_multiplier_modifier +0.06; productivity_growth_modifier +0.04; bureaucracy_cost_multiplier_modifier +0.04 | health_cost_multiplier_modifier -0.02 (revised value) | 0.875% -> 0.875% |
| `COLDWAR_NKO_christian_welfare` | productivity_growth_modifier +0.05; health_cost_multiplier_modifier +0.08; social_cost_multiplier_modifier +0.06 | health_cost_multiplier_modifier +0.04 (revised value) | 0.25% -> 0.25% |
| `COLDWAR_NKO_union_apprenticeships` | research_speed_factor +0.04; productivity_growth_modifier +0.04; education_cost_multiplier_modifier +0.05 | one-use CAT_industry bonus 0.5 (1 use) | 1% -> 1% |
| `COLDWAR_NKO_yanan_experts` | research_speed_factor +0.07; productivity_growth_modifier +0.06; foreign_influence_defense_modifier -0.1 | infantry_weapons_type build_cost_ic -0.05 | 0.5% -> 0.5% |
| `COLDWAR_NKO_kpa_maintenance_battalions` | equipment_cost_multiplier_modifier -0.04; production_factory_efficiency_gain_factor +0.04; army_personnel_cost_multiplier_modifier +0.05 | infantry_weapons_type build_cost_ic -0.04 | 1% -> 1% |
| `COLDWAR_NKO_jongil_supply_commission` | supply_consumption_factor -0.04; social_cost_multiplier_modifier +0.04 | +1 agriculture_district level, +1 shared slot (states 603, 602) | 0.5% -> 0.625% |

## Bilateral offers

Terms remain subject to the named recipient's decision. The offers retain their current recipient identity, prospective “If they accept” effects for both countries, acceptance guard, one-time receipts, pair-peace and mirrored embargo/sanction authority. Setup prices and weekly recurring formulas are unchanged.

| Offer | NKO package if accepted | Partner package if accepted | Setup fee; weekly commitment |
|---|---|---|---|
| `soviet_industry` | +1 civilian factory and slot in state 602 or 1200; productivity +0.06; production efficiency cap +0.06; fossil power generation +0.08; foreign influence defense -0.04; factory output +0.04 | SOV corporate tax income +0.015; foreign influence +0.05; education costs +0.02 | NKO pays 1.25% GDP + USSR pays 0.025% GDP once; weekly NKO GDP x 0.0015 / 52 and USSR GDP x 0.0002 / 52 |
| `china_farm_supply` | +1 agriculture district and slot in state 603 or 602; agriculture productivity +0.06; supply use -0.03; tax gain -0.02; foreign influence defense -0.03 | CHI trade opinion +0.04; resource export multiplier +0.02; bureaucracy costs +0.015 | NKO pays 0.875% GDP + China pays 0.05% GDP once; weekly NKO GDP x 0.001 / 52 and China GDP x 0.00025 / 52 |
| `soviet_energy_projects` | +1 civilian factory and +1 fossil power plant, with 2 slots in one eligible state (602 or 1200); fossil power generation +0.06; production efficiency cap +0.05; productivity +0.04; foreign influence defense -0.04 | SOV corporate tax income +0.02; foreign influence +0.03; education costs +0.02 | NKO pays 1.5% GDP + USSR pays 0.1% GDP once; weekly NKO GDP x 0.0015 / 52 and USSR GDP x 0.0004 / 52 |
| `japan_fisheries` | +1 dockyard and slot in coastal state 601 or 1199; agriculture productivity +0.06; corporate tax income +0.02; police costs +0.02 | JAP agriculture productivity +0.02; trade opinion +0.03; bureaucracy costs +0.01 | NKO pays 0.125% GDP + Japan pays 0.025% GDP once; weekly NKO GDP x 0.0003 / 52 and Japan GDP x 0.0001 / 52 |

The agreement generator computes valid shared states across all contracted buildings. Preview and acceptance use the same ordered site predicates for NKO ownership, control, each building's level cap, and coastal status for dockyards. When an eligible site exists, the preview selects the same first site the acceptance transaction will use; while locked with no eligible site, it keeps the full prospective package visible at the first listed alternative and labels the eligible-state alternatives. The complete numeric effects, buildings, slots, setup fee and weekly fee are in native prospective acceptance previews for both countries. These previews execute inside `effect_tooltip`; only acceptance applies effects or charges.

## Route and stacking review

- The mutually exclusive light priority adds one agricultural district and slot for 0.625% GDP, while balanced priority adds one civilian factory and slot for 0.625% GDP; heavy priority retains a direct equipment-specialization reward. Their prior persistent output bonuses and trade-offs remain in place.
- Heavy priority grants artillery build cost -0.05 and medium tank chassis cost -0.04. Together with munitions and the artillery branch, artillery equipment reductions total -0.19 across heavy priority, munitions directorate, mass artillery and ammunition standards; no output modifier is removed. That compatible sequence costs 2.125% GDP across its four focuses. Medium tank chassis reductions from heavy priority, mobile army and mobility drills total -0.16 across compatible focuses, at 1.375% GDP. These bonuses apply to production cost only.
- The fighter alternatives are mutually exclusive: conversion gives fighter build cost -0.07, while dispersed airfields gives -0.05 and preserves its own interception and construction trade-offs. Yan'an technical cadres give infantry-weapons build cost -0.05; the KPA maintenance branch independently gives -0.04. Naval bomber build cost falls by -0.06. `naval_workshops` adds one dockyard and slot alongside the naval aviation savings. The specified equipment targets follow MD family identifiers; they do not add ships, divisions, uranium or weapons.
- Agricultural assets are directed at the food-district, fertilizer, Chondo cooperative and post-1994 distribution programmes. The alternative market route preserves its different tax and local-control benefits. The extra construction outlays are visible in one-time GDP shares and focus completion checks.
- The major KDP, Chondo, Christian, Yan'an, cabinet, union, KPA and successor choices remain visible through existing party gates. Their new rewards are distinct: quality-control research, irrigated agriculture, health-cost relief, repair capacity, generation, engineering/electronics bonuses, officer and technical training, or sector-specific production costs. Their existing institutional costs and political trade-offs remain attached.
- 8 one-use research grants remain across industry, renewable energy and electronics. They use native MD categories and do not create permanent research-speed modifiers. Equipment savings are focused to hardware families and do not stack as country-wide army attack or defense modifiers.

## Historical basis

Kim Il Sung's 1964 *Theses on the Socialist Agrarian Question in Our Country* identifies irrigation, mechanization, electrification and chemicalization as rural technical-revolution priorities. This supports distinct irrigation, fertilizer, and farm-equipment programmes; exact grant quantities and costs are balance choices. [Kim Il Sung, Works, Vol. 18, English edition](https://kkfonline.com/wp-content/uploads/2020/04/Kim-Il-Sung-Works-18.pdf).

A 1970 People's Daily/Xinhua report records North Korean production of a 6,000-ton hydraulic press after work begun in 1968, providing a contemporary example for machine-tool and heavy-plant investment. It does not establish the overlay's exact balance values. [People's Daily, 7 June 1970, p. 6](https://cn.govopendata.com/renminribao/1970/06/07/6/).

A declassified CIA assessment describes power shortages, imported technical assistance and emphasis on heavy machinery and metallurgy in the period. It is a contemporary U.S. intelligence assessment, not a neutral DPRK national account. [CIA, North Korea: The Economy](https://www.cia.gov/readingroom/docs/CIA-RDP85T00875R001700030082-7.pdf).

The ROK Ministry of Unification describes the DPRK military's 1962 four-line military policy as including modernization, training and fortification. This informs the separate engineer, command-school, artillery, mobility and air-warning programmes rather than a single flat combat bonus. [ROK Ministry of Unification, Military Policy](https://nkinfo.unikorea.go.kr/nkp/pge/view.do?menuId=MENU_17).

## Native MD API calibration

Inspected installed Millennium Dawn reference at `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649` on 27 October 2026. The focus IDs, values and conditions below are direct donor checks for scale and API shape:

| Source | Observed reward | Conditions and cost |
|---|---|---|
| `SOV_UVZ_expanding`, `common/national_focus/05_russia.txt:32602` | `industrial_capacity_factory +0.10`, maximum production efficiency +0.10, one-use `CAT_tanks` bonus 1, medium tank chassis `build_cost_ic -0.08` | Focus cost 5, western-sanctions focus and no bankruptcy mission; treasury -10 |
| `SOV_economic_efko`, `05_russia.txt:32890` | 3 agriculture districts, agriculture productivity +0.02, decision access | Focus cost 5, no bankruptcy; treasury -12.5 |
| `SOV_economic_interrao`, `05_russia.txt:33164` | Energy use -0.03, energy gain +0.03 and one-use `CAT_renewable_energy` bonus 0.5 | Focus cost 5, no bankruptcy and an owned infrastructure/sphere context |
| `SOV_increased_arms_exports`, `05_russia.txt:5919` | 3 arms factories; artillery, anti-tank, anti-air and tank equipment build costs -0.02 | Focus cost 5 with donor route conditions |
| `SOV_rostech`, `05_russia.txt:24873` | One arms factory and equipment cost reductions including artillery, fighter, tactical bomber and naval bomber | Focus cost 5 and donor research gates |
| `SOV_uav_arms`, `05_russia.txt:21724` | `medium_plane_suicide_airframe` build cost -0.21 | Focus cost 5 with donor route conditions |
| `GENERIC_expand_the_secret_service`, `00_generic.txt:267` | One-use `CAT_night_vision` bonus 0.25 | Generic political-focus predecessor and native spy-system context |

The source compiler now emits native `add_equipment_bonus` records from the exact MD family keys and mirrors them in focus Effects previews. Building and research effects remain supported. The exact source focus IDs and values above are recorded to make the balance comparison auditable.

## Scope and evidence limits

This is a canonical-source-only implementation. Immutable approved snapshots and runtime exports are unchanged; the root integration pipeline must regenerate exports and run transaction, preview, preservation, equipment and building-slot checks before treating it as integrated. No NKO compiler or tests were run in this source-only handoff. Historical sources justify policy themes; balance values are game design decisions, not claims about historical programme amounts.

