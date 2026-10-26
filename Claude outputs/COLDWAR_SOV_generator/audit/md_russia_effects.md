# Millennium Dawn 2000 Russia: how the foci reward the player

Audit of `common/national_focus/05_russia.txt` (806 foci) as the benchmark for the COLDWAR_SOV 1970 tree. Read-only; parsed with a Clausewitz parser (comments stripped, brace-matched). An effect counts as *visible* when it is not inside `hidden_effect`, not AI-only (`limit = { is_ai = yes }`) and not inside `effect_tooltip` (shown but not executed). Themes come from `search_filters`, names and effects; about 5 % of the theme assignments are judgement calls.

**Key findings**

- MD foci are small: median **3 visible lines and 2 effect kinds**; 37 % give a single kind. PP appears in only 9 % of foci (median **100**), stability in 7 % (median **+5 %**).
- The main reward currency is the **country's own dynamic modifiers**: 28 % of foci change them, usually **2 lines of 0.02-0.05** on one modifier.
- **Buildings are always paid**: 76 of 79 building foci pay, at 1.0-1.15x the helper's flat price (7.5 bn per factory).
- **Cost barely changes reward size**: cost 3 and cost 7 both have a median of 3 lines. Only building counts, money and stability grow with cost. Our rulebook therefore adds a stricter reward budget.
- **33 % of foci carry a visible downside.** The usual cost is money (15 %), a cost line on the modifier (9 %) or an idea with trade-offs (7 %). Flat stability or PP losses are rare (2 %).
- In foreign policy **57 foci use the offer pattern** (event to the partner, `TT_IF_THEY_ACCEPT`, `effect_tooltip`). But 48 foci change the other country's opinion directly and about 10 impose treaties or territory. That breaks our multiplayer rule.

## 1. Effect catalogue (counts and value ranges)
Uses = number of calls; foci = foci with at least one call (out of 806). Values are visible, executed calls. MD money is in billions of model dollars.

| Effect (MD code) | Uses | Foci | % | Typical value | Range / quartiles | Notes |
|---|---|---|---|---|---|---|
| dynamic-modifier variable `add_to_variable = { SOV_x_y = v tooltip = y_tt }` | 614 | 227 | 28.2 | +0.03 (mode +0.05) | pos p25-p75 0.02-0.05, max 0.12; neg -0.02..-0.10 | 1 modifier per focus, median 2 lines; 32 % of these foci include a cost line |
| header `custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = X }` | 287 | 220 | 27.3 | 1 per modifier touched |  | always precedes the variable lines; no `force_update_dynamic_modifier` in foci |
| `country_event` / `news_event` | 288 | 161 | 20.0 |  |  | visible: 138 to other countries, 70 to self; 29 news events hidden |
| `custom_effect_tooltip` (text) | 244 | 167 | 20.7 |  |  | `TT_IF_THEY_ACCEPT` 57, `TT_IF_THEY_REJECT` 23, decision-unlock texts 47, separatism 14 |
| scripted helpers `x = yes` | 271 | 216 | 26.8 |  |  | AI popularity helper 88 (hidden), economy meter 47, company capitalisation 30, separatism 19, trade agreement 14 |
| treasury `set_temp_variable = { treasury_change = v }` + `modify_treasury_effect = yes` | 154 | 139 | 17.2 | -7.5 | costs p25 -15 / med -7.5 / p75 -4, min -155; gains 10-110 (7 foci) | building foci med -10; other costs med -7 |
| `add_opinion_modifier` / `reverse_add_opinion_modifier` | 148 | 63 | 7.8 | has_expressed_loyalty |  | 69 executed in the other country's scope |
| `unlock_decision_tooltip` | 120 | 66 | 8.2 | 1-4 per focus |  | 110 distinct decisions; 24 foci give nothing else |
| `add_ideas` | 94 | 88 | 10.9 |  |  | 258 ideas in Russian.txt; most carry a trade-off |
| `add_political_power` | 79 | 74 | 9.2 | 100 | 25-250, quartiles 50 / 100 / 145 | negatives -25..-100 (6) |
| `add_building_construction` (direct) | 78 | 47 | 5.8 | 1 level | infrastructure 24, IC 15, arms 8, dockyards 5 (level 2-3) | paired with treasury in 44 of 47 foci |
| party popularity `party_index` + `party_popularity_increase` (+ `temp_outlook_increase`) + `change_relative_party_popularity` | 77 | 66 | 8.2 | +0.02 (mode) | 0.001-0.15; entry +0.10 with outlook +0.10; AI-only ±0.75 | 18 hidden |
| influence `percent_change` + `influence_target` (+ `tag_index`) + `change_influence_percentage` | 73 | 54 | 6.7 | +3 (mode) | 2-5 (25 once) | 20 calls give *foreign* countries influence in Russia (car brands, Western investors) as the cost |
| faction `temp_opinion` + `change_<faction>_opinion` | 72 | 53 | 6.6 | +5 (mode) | +1..+15; neg -5..-40 (mode -10) | oligarchs 29, intelligence community 17, fossil-fuel industry 13, defence industry 6 |
| `add_stability` | 66 | 59 | 7.3 | +0.05 | +0.01..+0.30, quartiles 0.02 / 0.05 / 0.05; neg -0.02..-0.25 |  |
| building helpers (`one_random_industrial_complex` ...) | 58 | 41 | 5.1 | 1-3 buildings | offices 12+2+2, IC 9+2+2, arms 9+1+2, renewables 6 | built-in price; never `skip_payment` in MD |
| `swap_ideas` | 53 | 47 | 5.8 |  |  | 3-5-tier ladders (section 4) |
| `add_power_balance_value` (SOV_west_east_bop) | 52 | 52 | 6.5 | ±0.20 | always 0.20 (one 0.05) |  |
| `add_popularity` (ideology) | 47 | 45 | 5.6 | +0.10 | +0.02..+0.15; neg -0.03..-0.20 |  |
| budget/law helpers (`increase_policing_budget` ...) | 44 | 43 | 5.3 | +1 step |  | centralisation 12, policing 9, economic growth 8, military 6, social 4 |
| `create_wargoal` / `add_threat_from_wargoal_effect` | 68 | 35 | 4.3 |  |  | 24 of 44 wargoals hidden (inside event outcomes) |
| `add_tech_bonus` | 39 | 29 | 3.6 | bonus 0.5, uses 1 | bonus 0.15-1.0; uses 1 (74 %), 2 (23 %), 3 (1) | CAT_internet 6, armoured vehicles 5, tanks 3 |
| `add_resource` | 37 | 20 | 2.5 | +3 | +1..+12 per state (oil 8 ×5, oil 3 ×5, rubber 3 ×5) |  |
| `add_extra_state_shared_building_slots` | 37 | 33 | 4.1 | +1 | 1-5 | always with a building |
| `add_timed_idea` | 37 | 34 | 4.2 | 365 d | 21-2000 d; modes 365, 100, 1095 |  |
| `remove_ideas` | 33 | 26 | 3.2 |  |  | removes a negative start spirit |
| `add_equipment_to_stockpile` | 30 | 11 | 1.4 |  | 8 MLRS; 100-1100 vehicles; 150-500 UAV; 6000 inf. weapons | negative amounts = gifts to others |
| `modify_europeanism` | 29 | 29 | 3.6 | +0.03 | 0.03-0.07 | liberal paths |
| `create_unit` / `division_template` | 35 | 17 | 2.1 |  |  | mostly hidden (annexations, PMC); Rosgvardia template |
| `add_war_support` | 20 | 20 | 2.5 | +0.03 | +0.01..+0.09 |  |
| domestic influence `change_domestic_influence_percentage` | 19 | 19 | 2.4 | +3.5 | -5..+15 |  |
| corruption `increase_corruption` / `decrease_corruption` | 17 | 17 | 2.1 | decrease ×1 |  | 14 decrease, 3 increase |
| `add_dynamic_modifier` | 16 | 14 | 1.7 |  |  | party modifiers switched on by the path's entry focus |
| leaders (`create_country_leader`, traits) | 18 | 18 | 2.2 |  |  |  |
| elections (`modify_election_threshold`, bans) | 17 | 16 | 2.0 |  |  |  |
| `modify_international_investment_effect` | 14 | 14 | 1.7 | +1 | always +1 | the 14 'Friendship with X' foci |
| `army_experience` / `navy_experience` / `air_experience` | 12 | 7 | 0.9 | 25 | army 15-50, navy 10-50, air 15-25 |  |
| `add_equipment_bonus` (build_cost_ic) | 11 | 11 | 1.4 | -0.07 per type | -0.07..-0.13, `instant = yes` | arms companies, all cost 5 |
| `change_ruling_party_effect` (`rul_party_temp`) | 8 | 8 | 1.0 |  |  | 7 of 8 hidden behind a tooltip |
| tax-rate helpers (`modify_corporate/population_tax_rate_effect`) | 8 | 8 | 1.0 | corp +5, pop -5 |  |  |
| `add_breakthrough_progress` | 3 | 3 | 0.4 | sp_breakthrough_progress.medium |  |  |
| `set_technology`, `add_doctrine_cost_reduction` (0.5 ×2), MIO unlock | 4 | 4 | 0.5 |  |  | one each |
| `modify_debt_effect` | 1 | 1 | 0.1 | -450 |  | Kasyanov's Government repays debt |
| research slots, special projects, `add_mastery`, `add_command_power`, `add_manpower` (positive) | 0 | 0 | 0 | - |  | not used in MD Russia foci |

**MD building prices** (flat, built into `00_scripted_effects.txt` helpers, charged unless `skip_payment = 1`): industrial complex, arms factory and dockyard 7.5 · office + fossil power plant 12 · nuclear reactor 9 · enrichment facility 15.5 · microchip plant 10.5 · renewable 8.5 · energy/industrial infrastructure 6.5 · synthetic refinery 6 · agriculture district 3.75 · infrastructure 3.5 · fossil power plant 3.25 · anti-air 3.25 · internet station / fuel silo 3 · air base / rail terminal 2.5 · radar 1.75. `two_`/`three_` helpers cost 2x/3x.

**Russian dynamic modifiers changed by foci** (lines): `SOV_economy_modifier` 122 · `SOV_landforce_modifier` 109 · `SOV_intelligence_modifier` 102 · `SOV_just_inner_modifier` 47 · `SUB_russian_economy_modifier` (mirror for sphere members, hidden) 43 · `SOV_navalny_inner_modifier` 41 · `SOV_koba_politic_modifier` 33 · `SOV_navy_modifier` 32 · `SOV_revived_politburo_modifier` 24 · `SOV_russian_oligarchs_modifier` 18 · `SOV_western_sanctions_modifier` 18 · `SOV_airforce_modifier` 13 · `SOV_npp_modifier` 7 · `SOV_putin_politic_modifier` 5.

**Most common modifier keys and values:** stability_factor 52× (+0.02, ±0.01-0.10) · war_support_factor 37× (+0.02) · corporate_tax_income 30× (+0.01, up to 0.12) · political_power_factor 21× (+0.05, up to 0.10) · conscription_factor 21× (+0.02) · bureaucracy_cost 15× (+0.085 as a cost) · research_speed_factor 14× (+0.02, up to 0.10) · foreign_influence_defense 13× (+0.05) · police_cost 13× (±0.02-0.04) · drift_defence 13× (+0.05) · root_out_resistance 10× (0.05-0.25) · oil_export 10× (+0.02) · production_speed_buildings 9× (+0.03, up to 0.10). Combat stats make up 16 of 109 landforce lines (15 %), median 0.03: army_core_defence 7× (0.01-0.10), army_org 3× (0.03), army_defence and infantry_attack 2× each (0.02-0.05), artillery and core attack 1× each (0.05). They always come bundled with other lines, never as the whole reward.

## 2. Effects per focus and costs

**Size of a focus.** Visible reward lines per focus (each modifier line counts): 0: 8 · 1: 154 · 2: 186 · 3: 157 · 4: 121 · 5: 74 · 6: 47 · 7+: 59. Distinct effect kinds: 1: 300 (37 %) · 2: 214 · 3: 147 · 4: 89 · 5+: 33 · 0: 23.

**Foci without a real reward:** 85 give only an event (+tooltip), 24 only a decision unlock, 16 only a scripted helper, 15 only a tooltip, 8 nothing visible. Together with 3 event+decision-only foci that is 151 foci (19 %), mostly referendum, annexation and CIS steps in the LDPR/CPRF/liberal foreign branches.

**Downsides.** 262 foci (33 %) carry a visible downside; 223 (28 %) without counting the building price. By type (foci): pure money cost 75 · cost line on a dynamic modifier 73 · idea with trade-off 57 · building payment 45 · foreign influence in Russia 14 · flat stability loss 9 · faction loss 9 · corruption up 3 · war support 2. MD rarely uses flat stability or PP penalties; costs live in money and modifier lines.

**Cost and reward size** (all foci, visible effects; % = share of foci with that effect, value = median where present):

| Cost | Foci | Lines | Kinds | PP | Stability | Dyn. lines | Buildings | Treasury cost | Tech | Ideas | Downside |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-2 | 93 | 2 | 1 | 17 % · 87.5 | 4 % · +0.025 | 16 % · 2 | 0 % | 2 % · -4 | 2 % | 5 % | 8 % |
| 3 | 314 | 3 | 2 | 7 % · 75 | 3 % · +0.03 | 32 % · 2 | 2 % · 1 | 12 % · -5 | 4 % · 0.5 | 25 % | 29 % |
| 4-5 | 224 | 3 | 2 | 7 % · 100 | 6 % · +0.05 | 28 % · 2 | 21 % · 2 | 25 % · -10 | 4 % · 0.5 | 19 % | 44 % |
| 6-7 | 174 | 3 | 2 | 7 % · 100 | 9 % · +0.05 | 28 % · 2 | 14 % · 2 | 13 % · -10 | 3 % · 0.5 | 10 % | 37 % |

Substantive foci only (at least one visible reward other than event, decision, helper or tooltip): lines 2 → 3 → 3.5 → 4 and kinds 2 → 2 → 3 → 3 for cost 1-2 → 3 → 5 → 7.

**What a big focus gives compared to a small one.** In the economy branch cost really buys something: buildings 10 % → 41 % → 51 % of foci, treasury cost -3.5 → -10 → -13.5, stability 0 % → 3 % → 14 %. Examples:
- cost 3 `SOV_economic_rjd_north_latitudinal`: 1 infrastructure for -3.5
- cost 5 `SOV_economic_rjd_baikal_amure`: 4 infrastructure for -14 plus the economy meter
- cost 7 `SOV_economic_rjd_transsib`: 13 infrastructure levels for -42 plus the economy meter
- cost 3 `SOV_economic_russian` (tree root): 4 industrial complexes for -34
- cost 7 `SOV_revitalize_russian_industrial_sector`: `three_random_industrial_complex` plus the economy meter

Political and party branches do not scale. 23 of the 29 Yabloko-only foci cost 7, yet their median is 3 lines: typically 1-3 modifier lines plus Europeanism +0.03. `SOV_kill_revanchism` (cost 7) gives stability factor +1 % and costs war support -6 %, conscription -1 % and nationalist drift -5 %. Comparable cost-3 CPRF foci give the same or more (`SOV_honor_gorbachevs_legacy`: PP 75, democratic +5 %, 2 lines).
Conclusion: MD uses cost mostly as *time*, not as reward size. Our rulebook keeps MD's effect vocabulary and value sizes but ties the number of reward points to cost.

## 3. Theme templates with MD examples

Per theme: size, costs, how often each effect appears (share of the theme's foci), median magnitudes, typical downside and 3-4 MD foci quoted verbatim (log line and AI-only helper removed).

### Industry / construction (59 foci; cost 1: 1, 3: 19, 5: 18, 7: 21)

- Effects: treasury 34 %, scripted helper 31 %, building helper 27 %, direct building 25 %, dyn-modifier change 19 %, building slots 17 %, add idea 15 %, influence 14 %.
- Medians where present: PP 75, stability +0.035, treasury -8.5, buildings 2, dyn lines 2; 3 visible lines.
- Downside in 47 % of foci.
- Pattern: Paid buildings are the reward. Either a helper with a built-in price (`one_random_industrial_complex`, `one_office_construction`, `three_random_industrial_complex`) or `add_building_construction` with slots and an explicit `treasury_change` at about the helper price (IC 7.5-8.5, infrastructure 3.5). Usually one economy-meter tick (`SOV_modify_economic = 1`) is added, sometimes 1-2 economy lines. Downside: the price; for foreign car brands also foreign influence in Russia (+4 per brand).

`SOV_economic_russian` (The Russian Economy, cost 3)
```
every_owned_state = {
	random_select_amount = 4
	add_building_construction = {
		type = industrial_complex
		level = 1
		instant_build = yes
	}
	add_extra_state_shared_building_slots = 1
}
newline = yes
set_temp_variable = { treasury_change = -34 }
modify_treasury_effect = yes
```
`SOV_economic_cars_europe` (European Car Brands, cost 5)
```
SOV_economy_cars_script = yes
652 = {
	add_extra_state_shared_building_slots = 2
	add_building_construction = {
		type = industrial_complex
		level = 2
		instant_build = yes
	}
}
set_temp_variable = { treasury_change = -17 }
modify_treasury_effect = yes
set_temp_variable = { percent_change = 4 }
set_temp_variable = { tag_index = GER }
set_temp_variable = { influence_target = SOV }
change_influence_percentage = yes
set_temp_variable = { percent_change = 4 }
set_temp_variable = { tag_index = FRA }
set_temp_variable = { influence_target = SOV }
change_influence_percentage = yes
```
`SOV_may_decrees` (May Decrees, cost 7)
```
add_political_power = 100
one_random_industrial_complex = yes
one_office_construction = yes
```
`SOV_economic_rjd_transsib` (Trans-Siberian Railway, cost 7)
```
set_temp_variable = { SOV_modify_economic = 1 }
SOV_modify_economic_support = yes
newline = yes
651 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
660 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
661 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
658 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
676 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
677 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
680 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
682 = { add_building_construction = { type = infrastructure level = 2 instant_build = yes } }
685 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
687 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
686 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
692 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
newline = yes
set_temp_variable = { treasury_change = -42 }
modify_treasury_effect = yes
```

### Economy / finance (53 foci; cost 1: 2, 2: 5, 3: 12, 5: 18, 7: 16)

- Effects: dyn-modifier change 36 %, treasury 23 %, add idea 21 %, faction opinion 17 %, budget/law helper 13 %, idea swap 13 %, PP 11 %, decision unlock 9 %.
- Medians where present: PP 100, stability +0.05, treasury -17.5, dyn lines 2; 3 visible lines.
- Downside in 55 % of foci.
- Pattern: Economy-modifier lines (corporate tax, tax gain, office tax, ROI through the sanctions modifier), treasury both ways, negative start spirits eased step by step (`SOV_ruble_collapse` → `_1` → `_2`), tax-rate helpers, faction shifts (oligarchs, bankers). The money is the downside in crisis foci (-10 to -40, Stabilisation Fund -155). The rare gains (+50 to +60) come from seizures with oligarchs -25.

`SOV_prevent_panic_on_currency_exchange` (Stop the Panic in the Stock Markets, cost 3)
```
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_western_sanctions_modifier }
add_to_variable = { SOV_sanctions_office_tax_gain = 0.02 tooltip = office_park_income_tax_modifier_tt }
add_to_variable = { SOV_sanctions_research_speed = 0.01 tooltip = research_speed_factor_tt }
newline = yes
set_temp_variable = { treasury_change = -10 }
modify_treasury_effect = yes
```
`SOV_progressive_taxation` (Progressive Taxation, cost 3)
```
decrease_corruption = yes
set_temp_variable = { pop_change = -5 }
modify_population_tax_rate_effect = yes
set_temp_variable = { corp_change = 5 }
modify_corporate_tax_rate_effect = yes
```
`SOV_fnb_destroyed` (Destroy the National Welfare Fund, cost 5)
```
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_western_sanctions_modifier }
add_to_variable = { SOV_sanctions_roi = 0.02 tooltip = return_on_investment_modifier_tt }
newline = yes
swap_ideas = {
	remove_idea = SOV_ruble_collapse
	add_idea = SOV_ruble_collapse_1
}
newline = yes
set_temp_variable = { treasury_change = -40 }
modify_treasury_effect = yes
```
`SOV_move_oligarchic_entites_back_to_russia` (Move Oligarchic Entities Back, cost 7)
```
set_temp_variable = { treasury_change = 60 }
modify_treasury_effect = yes
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_russian_oligarchs_modifier }
add_to_variable = { SOV_oligarchs_corruption_cost_factor = 0.07 tooltip = corruption_cost_factor_tt }
add_to_variable = { SOV_oligarchs_office_income_factor = 0.05 tooltip = office_park_income_tax_modifier_tt }
```

### Agriculture (9 foci; cost 3: 3, 5: 5, 7: 1)

- Effects: dyn-modifier change 56 %, direct building 33 %, treasury 33 %, decision unlock 33 %, scripted helper 33 %, building slots 33 %, building helper 22 %, domestic influence 11 %.
- Medians where present: treasury -12.5, buildings 3, dyn lines 2; 3 visible lines.
- Downside in 67 % of foci.
- Pattern: Agriculture districts (helper 3.75 each, or 4 placed for -16), agriculture tax/productivity lines (0.01-0.03; party modifiers up to 0.12/0.20), economy meter, decision unlock. Downside: price, bureaucracy cost +0.21 on the big party version, stability -0.05 for collectivisation.

`SOV_recollectivization` (Recollectivization, cost 3)
```
set_temp_variable = { percent_change = 2 }
change_domestic_influence_percentage = yes
add_stability = -0.05
one_random_industrial_complex = yes
```
`SOV_economic_rusagro` (RusAgro, cost 5)
```
unlock_decision_tooltip = SOV_economic_rusagro_expanded
newline = yes
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_economy_modifier }
add_to_variable = { SOV_econ_agriculture_district_income_tax_modifier = 0.01 tooltip = agriculture_district_income_tax_modifier_tt }
add_to_variable = { SOV_econ_agriculture_tax_modifier = 0.01 tooltip = agriculture_tax_modifier_tt }
newline = yes
set_temp_variable = { SOV_modify_economic = 1 }
SOV_modify_economic_support = yes
newline = yes
every_owned_state = {
	random_select_amount = 4
	add_building_construction = {
		type = agriculture_district
		level = 1
		instant_build = yes
	}
	add_extra_state_shared_building_slots = 1
}
newline = yes
set_temp_variable = { treasury_change = -16 }
modify_treasury_effect = yes
hidden_effect = {
	add_to_variable = { SOV_econsub_agriculture_district_income_tax_modifier = 0.01 }
	add_to_variable = { SOV_econsub_agriculture_tax_modifier = 0.01 }
	add_to_variable = { SOV_econ_sphere_company_count = 1 }
}
```
`SOV_land_socialisation` (The Land Socialisation, cost 7)
```
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_just_inner_modifier }
add_to_variable = { SOV_just_inner_agricolture_productivity_modifier = 0.12 tooltip = agricolture_productivity_modifier_tt }
add_to_variable = { SOV_just_inner_bureaucracy_cost_multiplier_modifier = 0.21 tooltip = bureaucracy_cost_multiplier_modifier_tt }
add_to_variable = { SOV_just_inner_agriculture_tax_modifier = 0.20 tooltip = agriculture_tax_modifier_tt }
```

### Energy / resources (49 foci; cost 1: 1, 2: 3, 3: 22, 5: 15, 7: 8)

- Effects: scripted helper 73 %, treasury 47 %, dyn-modifier change 39 %, resource 37 %, direct building 22 %, decision unlock 20 %, faction opinion 14 %, building slots 12 %.
- Medians where present: treasury -7.5, buildings 1, dyn lines 2; 4 visible lines.
- Downside in 49 % of foci.
- Pattern: `add_resource` +2..+8 in named states (median 3), a small paid building (IC, fuel silo, reactor), treasury -2..-20, export-multiplier lines 0.02-0.03, company capitalisation helper (`SOV_modify_capitalisation_gazprom`), decision unlock. Pipelines give modifier lines only; renewables cost the fossil-fuel faction -5.

`SOV_economic_oil_khmao` (Oil and Gas Project in [KHM.GetName], cost 3)
```
678 = { add_resource = { type = oil amount = 3 } }
newline = yes
set_temp_variable = { SOV_modify_capitalisation_gazprom = -1.8 }
SOV_modify_capitalisation_gazprom_support = yes
newline = yes
set_temp_variable = { treasury_change = -1.8 }
modify_treasury_effect = yes
```
`SOV_found_rosatom` (Found Rosatom, cost 3)
```
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_economy_modifier }
add_to_variable = { SOV_econ_nuclear_energy_generation_modifier = 0.01 tooltip = nuclear_energy_generation_modifier_tt }
add_to_variable = { SOV_econ_nuclear_fuel_consumption_modifier = -0.01 tooltip = nuclear_fuel_consumption_modifier_tt }
add_to_variable = { SOV_econ_repair_speed_nuclear_reactor_factor = 0.10 tooltip = repair_speed_nuclear_reactor_factor_tt }
add_to_variable = { SOV_econ_production_speed_nuclear_reactor_factor = 0.20 tooltip = production_speed_nuclear_reactor_factor_tt }
newline = yes
set_temp_variable = { SOV_modify_economic = 2 }
SOV_modify_economic_support = yes
newline = yes
set_temp_variable = { treasury_change = -20 }
modify_treasury_effect = yes
```
`SOV_economic_alrosa` (ALROSA, cost 5)
```
unlock_decision_tooltip = SOV_economic_nakynskoe
newline = yes
688 = {
	add_resource = { type = chromium amount = 2 }
	add_extra_state_shared_building_slots = 1
	add_building_construction = {
		type = industrial_complex
		level = 1
		instant_build = yes
	}
}
647 = { add_resource = { type = chromium amount = 2 } }
newline = yes
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_economy_modifier }
add_to_variable = { SOV_econ_gdp_from_resource_sector_modifier = 0.01 tooltip = gdp_from_resource_sector_modifier_tt }
add_to_variable = { SOV_econ_chromium_export_multiplier_modifier = 0.02 tooltip = chromium_export_multiplier_modifier_tt }
add_to_variable = { SOV_econ_corporate_tax_income_multiplier_modifier = 0.02 tooltip = corporate_tax_income_multiplier_modifier_tt }
newline = yes
set_temp_variable = { SOV_modify_capitalisation_alrosa = 0.190 }
SOV_modify_capitalisation_alrosa_support = yes
newline = yes
set_temp_variable = { SOV_modify_economic = 1 }
SOV_modify_economic_support = yes
newline = yes
set_temp_variable = { treasury_change = -12.1 }
modify_treasury_effect = yes
```
`SOV_renewable_energy_investments` (Renewable Energy Investments, cost 7)
```
add_ideas = SOV_renewables_idea
set_temp_variable = { temp_opinion = -5 }
change_fossil_fuel_industry_opinion = yes
one_random_renewable_energy_infra = yes
one_random_renewable_energy_infra = yes
```

### Research / science / space (29 foci; cost 2: 2, 3: 11, 5: 12, 7: 4)

- Effects: dyn-modifier change 41 %, tech bonus 31 %, scripted helper 28 %, treasury 21 %, party popularity 14 %, building helper 14 %, decision unlock 10 %, budget/law helper 7 %.
- Medians where present: treasury -10, buildings 2.5, dyn lines 2; 3 visible lines.
- Downside in 38 % of foci.
- Pattern: `add_tech_bonus` (CAT_internet 1.0 ×2, satellites 0.5 ×3, IT 0.3 ×1), research-speed lines 0.01-0.05, paid offices/internet stations, economy meter. Space foci pay 10-20 (Vostochny -15 for 7 buildings).

`SOV_economic_rostelekom` (Rostelecom, cost 3)
```
add_tech_bonus = {
	name = SOV_economic_rostelekom
	bonus = 1.0
	uses = 2
	category = CAT_internet
}
newline = yes
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_economy_modifier }
add_to_variable = { SOV_econ_research_speed_factor = 0.01 tooltip = research_speed_factor_tt }
add_to_variable = { SOV_econ_foreign_influence_defense_modifier = 0.04 tooltip = foreign_influence_defense_modifier_tt }
add_to_variable = { SOV_econ_production_speed_internet_station_factor = 0.05 tooltip = production_speed_internet_station_factor_tt }
newline = yes
set_temp_variable = { SOV_modify_economic = 1 }
SOV_modify_economic_support = yes
hidden_effect = {
	add_to_variable = { SOV_econsub_research_speed_factor = 0.01 }
	add_to_variable = { SOV_econsub_foreign_influence_defense_modifier = 0.04 }
	add_to_variable = { SOV_econsub_production_speed_internet_station_factor = 0.05 }
	add_to_variable = { SOV_econ_sphere_company_count = 1 }
}
```
`SOV_outer_space_sateelites` (Investing in Satellites, cost 3)
```
add_tech_bonus = {
	name = SOV_outer_space_sateelites
	bonus = 0.5
	uses = 3
	category = CAT_satellites
}
```
`SOV_economic_it_sphere` (Russian IT Sector, cost 5)
```
add_tech_bonus = {
	name = SOV_economic_it_sphere
	bonus = 0.30
	uses = 1
	category = CAT_internet
}
newline = yes
set_temp_variable = { SOV_modify_economic = 1 }
SOV_modify_economic_support = yes
newline = yes
one_office_construction = yes
```
`SOV_soviet_academy_of_sciences` (Soviet Academy of Sciences, cost 7)
```
one_office_construction = yes
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_revived_politburo_modifier }
add_to_variable = { SOV_revived_politburo_research_speed = 0.05 tooltip = research_speed_factor_tt }
```

### Army (79 foci; cost 1: 3, 2: 8, 3: 47, 4: 1, 5: 17, 7: 3)

- Effects: dyn-modifier change 39 %, treasury 27 %, party popularity 24 %, equipment cost bonus 13 %, custom tooltip 13 %, decision unlock 10 %, building slots 10 %, direct building 10 %.
- Medians where present: PP 25, treasury -7.5, buildings 1, dyn lines 2; 3 visible lines.
- Downside in 37 % of foci.
- Pattern: Two landforce lines of 0.02-0.05 (conscription, planning, special forces, supply, acclimatisation; combat stats in 15 % of lines, median 0.03, always bundled). Party 22 +0.02, defence industry or military +1..+5, treasury -3..-10. Kit foci give tech bonus 0.35-0.75 ×1-2; reform foci give XP 15-50 and climb the 'Outdated Army' ladder. Arms companies (cost 5): equipment cost -7 % on 12 types + 1 arms factory for -7.5..-20.

`SOV_form_yunarmiya` (Form Yunarmiya, cost 3)
```
set_temp_variable = { temp_opinion = 5 }
change_the_military_opinion = yes
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_landforce_modifier }
add_to_variable = { SOV_land_conscription_factor = 0.02 tooltip = conscription_factor_tt }
if = {
	limit = { NOT = { has_country_flag = SOV_wagner_parties } }
	newline = yes
	set_temp_variable = { party_index = 22 }
	set_temp_variable = { party_popularity_increase = 0.02 }
	change_relative_party_popularity = yes
}
```
`SOV_ratnik_program` (The Ratnik Program, cost 3)
```
add_tech_bonus = {
	name = SOV_ratnik_program
	bonus = 0.15
	uses = 1
	category = CAT_infantry
}
set_temp_variable = { temp_opinion = 1 }
change_defense_industry_opinion = yes
if = {
	limit = { NOT = { has_country_flag = SOV_wagner_parties } }
	set_temp_variable = { party_index = 22 }
	set_temp_variable = { party_popularity_increase = 0.02 }
	change_relative_party_popularity = yes
	newline = yes
}
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_landforce_modifier }
add_to_variable = { SOV_land_army_defence_factor = 0.05 tooltip = army_defence_factor_tt }
add_to_variable = { SOV_land_army_infantry_attack_factor = 0.05 tooltip = army_infantry_attack_factor_tt }
add_to_variable = { SOV_land_army_org_factor = 0.03 tooltip = army_org_factor_tt }
add_to_variable = { SOV_land_acclimatization_cold_climate_gain_factor = 0.20 tooltip = acclimatization_cold_climate_gain_factor_tt }
add_to_variable = { SOV_land_acclimatization_hot_climate_gain_factor = 0.20 tooltip = acclimatization_hot_climate_gain_factor_tt }
add_to_variable = { SOV_land_personnel_cost_multiplier_modifier = 0.09 tooltip = personnel_cost_multiplier_modifier_tt }
```
`SOV_2008_military_reforms` (Continue Military Reforms, cost 5)
```
swap_ideas = {
	remove_idea = SOV_outdated_army_idea_2
	add_idea = SOV_outdated_army_idea_3
}
if = {
	limit = { NOT = { has_country_flag = SOV_wagner_parties } }
	set_temp_variable = { party_index = 22 }
	set_temp_variable = { party_popularity_increase = 0.02 }
	change_relative_party_popularity = yes
	newline = yes
}
show_unit_leaders_tooltip = SOV_sergey_shoygu
army_experience = 15
air_experience = 15
newline = yes
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_landforce_modifier }
add_to_variable = { SOV_land_expected_mil_modifier = 0.5 tooltip = expected_mil_modifier_tt }
newline = yes
set_temp_variable = { treasury_change = -7 }
modify_treasury_effect = yes
```
`SOV_mechanized_infantry_renovations` (Use "Armata" for APCs and IFVs, cost 5)
```
set_temp_variable = { temp_opinion = 3 }
change_defense_industry_opinion = yes
if = {
	limit = { NOT = { has_country_flag = SOV_wagner_parties } }
	set_temp_variable = { party_index = 22 }
	set_temp_variable = { party_popularity_increase = 0.02 }
	change_relative_party_popularity = yes
	newline = yes
}
add_tech_bonus = {
	name = SOV_mechanized_infantry_renovations
	bonus = 0.35
	uses = 2
	category = CAT_armored_fighting_vehicles
}
newline = yes
add_tech_bonus = {
	name = SOV_mechanized_infantry_renovations
	bonus = 0.35
	uses = 2
	category = CAT_armored_personnel_carriers
}
newline = yes
add_tech_bonus = {
	name = SOV_mechanized_infantry_renovations
	bonus = 0.75
# ... 6 more lines
```

### Navy (9 foci; cost 3: 4, 5: 4, 7: 1)

- Effects: treasury 67 %, building slots 44 %, direct building 44 %, dyn-modifier change 33 %, event 22 %, idea swap 22 %, decision unlock 11 %, wargoal 11 %.
- Medians where present: PP 50, treasury -21.25, buildings 3, dyn lines 8; 5 visible lines.
- Downside in 67 % of foci.
- Pattern: The richest foci in MD: navy modifier up to 8 lines (0.01-0.08), dockyards level 2-3 placed and paid (-15..-25), navy XP 50 + PP 50, the 'Plundered Navy' ladder, doctrine cost -50 % ×2, MIO unlock.

`SOV_fleet` (Glorious Soviet Navy, cost 3)
```
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_navy_modifier }
add_to_variable = { SOV_navy_naval_accidents_chance = -0.03 tooltip = naval_accidents_chance_tt }
add_to_variable = { SOV_navy_naval_mine_hit_chance = -0.03 tooltip = naval_mine_hit_chance_tt }
add_to_variable = { SOV_navy_positioning = 0.02 tooltip = positioning_tt }
add_to_variable = { SOV_navy_industrial_capacity_dockyard = 0.04 tooltip = industrial_capacity_dockyard_tt }
add_to_variable = { SOV_navy_naval_speed_factor = 0.04 tooltip = naval_speed_factor_tt }
add_to_variable = { SOV_navy_navy_max_range_factor = 0.04 tooltip = navy_max_range_factor_tt }
add_to_variable = { SOV_navy_navy_anti_air_attack_factor = 0.03 tooltip = navy_anti_air_attack_factor_tt }
add_to_variable = { SOV_navy_amphibious_invasion = 0.03 tooltip = amphibious_invasion_tt }
```
`SOV_start_fleet_reforms` (Reforms of the Russian Navy, cost 3)
```
swap_ideas = {
	remove_idea = SOV_the_plundered_russian_navy1
	add_idea = SOV_the_plundered_russian_navy2
}
navy_experience = 50
add_political_power = 50
newline = yes
country_event = russia.118
newline = yes
set_temp_variable = { treasury_change = -10 }
modify_treasury_effect = yes
```
`SOV_The_high_seas_fleet` (The High Seas Fleet, cost 5)
```
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_navy_modifier }
add_to_variable = { SOV_navy_naval_accidents_chance = -0.01 tooltip = naval_accidents_chance_tt }
add_to_variable = { SOV_navy_naval_mine_hit_chance = -0.01 tooltip = naval_mine_hit_chance_tt }
add_to_variable = { SOV_navy_positioning = 0.03 tooltip = positioning_tt }
add_to_variable = { SOV_navy_industrial_capacity_dockyard = 0.04 tooltip = industrial_capacity_dockyard_tt }
add_to_variable = { SOV_navy_naval_speed_factor = 0.04 tooltip = naval_speed_factor_tt }
add_to_variable = { SOV_navy_navy_max_range_factor = 0.04 tooltip = navy_max_range_factor_tt }
add_to_variable = { SOV_navy_navy_anti_air_attack_factor = 0.05 tooltip = navy_anti_air_attack_factor_tt }
add_to_variable = { SOV_navy_amphibious_invasion = 0.05 tooltip = amphibious_invasion_tt }
newline = yes
668 = {
	add_extra_state_shared_building_slots = 2
	add_building_construction = {
		type = dockyard
		level = 2
	}
}
1140 = {
	add_extra_state_shared_building_slots = 2
	add_building_construction = {
		type = dockyard
		level = 2
	}
}
set_temp_variable = { treasury_change = -25 }
modify_treasury_effect = yes
newline = yes
unlock_military_industrial_organization_tooltip = mio:SOV_nevskoye_design_bureau_naval_manufacturer
```

### Air force (14 foci; cost 3: 8, 5: 6)

- Effects: dyn-modifier change 57 %, treasury 43 %, tech bonus 29 %, party popularity 29 %, building helper 21 %, scripted helper 21 %, experience 7 %, direct building 7 %.
- Medians where present: treasury -5, buildings 2, dyn lines 1.5; 3 visible lines.
- Downside in 43 % of foci.
- Pattern: Tech bonus on one airframe (0.55 ×1 for 5th-gen fighters, 0.25 aircraft), air-defence 0.10, XP 20, air bases via helper, treasury -3..-10, party 22 +0.02.

`SOV_pakfa` (PAKFA, cost 3)
```
if = {
	limit = { has_dlc = "By Blood Alone" }
	add_tech_bonus = {
		name = SOV_pakfa
		bonus = 0.55
		uses = 1
		technology = gen_5_medium
	}
}
else = {
	add_tech_bonus = {
		name = SOV_pakfa
		bonus = 0.55
		uses = 1
		technology = MR_Fighter5
	}
}
newline = yes
set_temp_variable = { treasury_change = -7 }
modify_treasury_effect = yes
```
`SOV_aero_improvements` (Aircraft Improvements, cost 3)
```
set_temp_variable = { treasury_change = -3 }
modify_treasury_effect = yes
if = {
	limit = { NOT = { has_country_flag = SOV_wagner_parties } }
	set_temp_variable = { party_index = 22 }
	set_temp_variable = { party_popularity_increase = 0.02 }
	change_relative_party_popularity = yes
	newline = yes
}
add_tech_bonus = {
	name = SOV_aero_improvements
	bonus = 0.25
	uses = 1
	category = CAT_aircraft
}
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_revived_politburo_modifier }
add_to_variable = { SOV_revived_politburo_air_accidents = -0.10 tooltip = air_accidents_tt }
```
`SOV_reorganize_airforce` (Reorganize the Air Force, cost 5)
```
air_experience = 20
newline = yes
SOV_aviation_script = yes
set_temp_variable = { treasury_change = -10 }
modify_treasury_effect = yes
```
`SOV_air_rocket_defence` (Air and Missile Defense Forces, cost 5)
```
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_airforce_modifier }
add_to_variable = { SOV_air_air_defence_factor = 0.10 tooltip = air_defence_factor_tt }
newline = yes
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_landforce_modifier }
add_to_variable = { SOV_land_rocket_attack_factor = 0.05 tooltip = rocket_attack_factor_tt }
```

### Strategic / nuclear / space-military (13 foci; cost 3: 6, 5: 4, 7: 2, 10: 1)

- Effects: treasury 62 %, dyn-modifier change 62 %, tech bonus 15 %, direct building 15 %, building helper 8 %, remove idea 8 %, event 8 %, set_technology 8 %.
- Medians where present: treasury -9.25, buildings 3, dyn lines 3; 3 visible lines.
- Downside in 62 % of foci.
- Pattern: Always paid (13 of 13 carry money or a cost line): 3 rocket sites for -6, rocket attack +0.05..+0.10, missile tech 0.75 ×1, ICBM technology + 25 missiles for -4, space militarisation -20..-100.

`SOV_rocketi` (Strengthen the Strategic Missile Forces, cost 3)
```
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_landforce_modifier }
add_to_variable = { SOV_land_rocket_attack_factor = 0.10 tooltip = rocket_attack_factor_tt }
```
`SOV_missile_development` (Strategic Rocket Forces, cost 5)
```
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_landforce_modifier }
add_to_variable = { SOV_land_rocket_attack_factor = 0.10 tooltip = rocket_attack_factor_tt }
newline = yes
642 = {
	add_building_construction = {
		type = rocket_site
		level = 1
		instant_build = yes
	}
}
668 = {
	add_building_construction = {
		type = rocket_site
		level = 1
		instant_build = yes
	}
}
1140 = {
	add_building_construction = {
		type = rocket_site
		level = 1
		instant_build = yes
	}
}
newline = yes
set_temp_variable = { treasury_change = -6 }
modify_treasury_effect = yes
```
`SOV_modernize_soviet_missile_stockpiles` (Improvement of Launch Shafts, cost 5)
```
if = {
	limit = { nuclear_grant_allowed = yes }
	if = { limit = { NOT = { has_tech = ICBM5 } } set_technology = { ICBM5 = 1 } }
	add_equipment_to_stockpile = {
		type = nuclear_missile_equipment_5
		amount = 25
	}
}
newline = yes
set_temp_variable = { treasury_change = -4 }
modify_treasury_effect = yes
```
`SOV_hypersonic_missiles` (Hypersonic Missiles, cost 7)
```
if = {
	limit = { has_dlc = "Gotterdammerung" }
	add_tech_bonus = {
		name = SOV_hypersonic_missiles
		bonus = 0.75
		uses = 1
		category = CAT_ballistic_missiles
	}
}
add_tech_bonus = {
	name = SOV_hypersonic_missiles
	bonus = 0.75
	uses = 1
	category = CAT_cruise_missiles
}
newline = yes
set_temp_variable = { treasury_change = -8 }
modify_treasury_effect = yes
```

### Intelligence / internal security (38 foci; cost 2: 2, 3: 27, 5: 4, 7: 5)

- Effects: dyn-modifier change 79 %, faction opinion 32 %, custom tooltip 24 %, treasury 16 %, division template 11 %, stability 8 %, budget/law helper 8 %, event 5 %.
- Medians where present: PP 77.5, stability +0.05, treasury -4.5, dyn lines 3; 3 visible lines.
- Downside in 47 % of foci.
- Pattern: Intelligence modifier 2-5 lines (encryption 0.05-0.15, agency defence 0.10-0.20, influence defence 0.05-0.10, subversive activities 0.15) + intelligence community +4..+10 + separatism -1. Costs: police cost +0.04, root-out -0.15, treasury -4. Rosgvardia unlocks a template.

`SOV_gru` (GRU, cost 3)
```
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_intelligence_modifier }
add_to_variable = { SOV_intel_decryption_factor = 0.05 tooltip = decryption_factor_tt }
add_to_variable = { SOV_intel_police_cost_multiplier_modifier = 0.04 tooltip = police_cost_multiplier_modifier_tt }
newline = yes
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_landforce_modifier }
add_to_variable = { SOV_land_send_volunteers_tension = -0.05 tooltip = send_volunteers_tension_tt }
newline = yes
set_temp_variable = { temp_opinion = 4 }
change_intelligence_community_opinion = yes
```
`SOV_FSB_expansion` (Expand FSB, cost 3)
```
set_temp_variable = { temp_opinion = 7 }
change_intelligence_community_opinion = yes
custom_effect_tooltip = SOV_subjectsepar_minus_tt
hidden_effect = {
	SUB_separatism_minus_subject = yes
}
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_intelligence_modifier }
add_to_variable = { SOV_intel_intelligence_agency_defense = 0.20 tooltip = intelligence_agency_defense_tt }
add_to_variable = { SOV_intel_encryption_factor = 0.15 tooltip = encryption_factor_tt }
add_to_variable = { SOV_intel_foreign_influence_defense_modifier = 0.10 tooltip = foreign_influence_defense_modifier_tt }
```
`SOV_rosgvardia` (Form the Rosgvardia, cost 5)
```
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_intelligence_modifier }
add_to_variable = { SOV_intel_root_out_resistance_effectiveness_factor = -0.15 tooltip = root_out_resistance_effectiveness_factor_tt }
add_to_variable = { SOV_intel_foreign_subversive_activites = 0.15 tooltip = foreign_subversive_activites_tt }
add_to_variable = { SOV_intel_police_cost_multiplier_modifier = -0.02 tooltip = police_cost_multiplier_modifier_tt }
newline = yes
set_temp_variable = { treasury_change = -4 }
modify_treasury_effect = yes
custom_effect_tooltip = SOV_create_rosgvardia_unlock_tt
division_template = {
	name = "Rosgvardia"
	is_locked = yes
	regiments = {
		Militia_Bat = { x = 0 y = 0 }
		Militia_Bat = { x = 0 y = 1 }
		Militia_Bat = { x = 0 y = 2 }
		Militia_Bat = { x = 1 y = 0 }
		Militia_Bat = { x = 1 y = 1 }
		Militia_Bat = { x = 1 y = 2 }
		Arty_Bat = { x = 2 y = 0 }
		Arty_Bat = { x = 2 y = 1 }
		Arty_Bat = { x = 2 y = 2 }
	}
	support = {
		Mot_Recce_Comp = { x = 0 y = 0 }
		L_Engi_Comp = { x = 0 y = 1 }
	}
# ... 5 more lines
```
`SOV_secure_the_FSB` (Secure the FSB, cost 7)
```
add_stability = 0.05
add_timed_idea = {
	idea = SOV_FSB_renewed
	days = 730
}
```

### Political / party (158 foci; cost 1: 6, 2: 21, 3: 60, 5: 41, 7: 30)

- Effects: dyn-modifier change 27 %, balance of power 20 %, PP 18 %, event 17 %, add idea 16 %, ideology popularity 13 %, idea swap 13 %, stability 12 %.
- Medians where present: PP 100, stability +0.03, dyn lines 2; 2 visible lines.
- Downside in 29 % of foci.
- Pattern: Entry foci switch on the path's own dynamic modifier with 2 starting lines, change the ruling party, add +0.10 popularity (outlook +0.10) and a leader. Later foci add 1-3 lines to that modifier, BoP ±0.20, PP 50-100, party +0.02, and climb 3-5-tier idea ladders. Downside: cost lines (bureaucracy +0.10, stability factor -0.04), ideas with drawbacks, rival party -0.05.

`SOV_putin` (Vladimir Putin, cost 2)
```
country_event = { id = russia.104 days = 10 }
add_to_variable = { SOV_putin_politic_political_power_factor = 0.05 tooltip = political_power_factor_tt }
add_to_variable = { SOV_putin_politic_communism_drift = 0.05 tooltip = communism_drift_tt }
add_dynamic_modifier = { modifier = SOV_putin_politic_modifier }
set_country_flag = sov_putin_econ
if = {
	limit = { has_country_flag = sov_putin_econ }
	clr_country_flag = sov_zug_econ
	clr_country_flag = sov_zir_econ
}
if = {
	limit = { NOT = { check_variable = { ruling_party = 6 } } }
	set_temp_variable = { rul_party_temp = 6 }
	change_ruling_party_effect = yes
}
set_temp_variable = { party_index = 6 }
set_temp_variable = { party_popularity_increase = 0.10 }
set_temp_variable = { temp_outlook_increase = 0.10 }
change_relative_party_popularity = yes
```
`SOV_restalinization` (Restalinization, cost 3)
```
add_political_power = 75
add_ideas = SOV_idea_restalinization
add_power_balance_value = {
	id = SOV_west_east_bop
	value = 0.20
	tooltip_side = SOV_west_east_bop_right_side
}
country_event = { id = sov_communists.6 days = 1 }
```
`SOV_putinism` (Putinism, cost 5)
```
add_political_power = 50
add_stability = 0.02
add_ideas = SOV_idea_putinism
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_putin_politic_modifier }
add_to_variable = { SOV_putin_politic_communism_drift = 0.03 tooltip = communism_drift_tt }
add_to_variable = { SOV_putin_politic_political_power_factor = 0.07 tooltip = political_power_factor_tt }
add_to_variable = { SOV_putin_politic_stability_factor = 0.03 tooltip = stability_factor_tt }
set_temp_variable = { threshold_change = 0.07 }
modify_election_threshold = yes
add_power_balance_value = {
	id = SOV_west_east_bop
	value = 0.20
	tooltip_side = SOV_west_east_bop_right_side
}
```
`SOV_third_way` (The Third Way, cost 7)
```
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_just_inner_modifier }
add_to_variable = { SOV_just_inner_corporate_tax_income_multiplier_modifier = 0.12 tooltip = corporate_tax_income_multiplier_modifier_tt }
add_to_variable = { SOV_just_inner_bureaucracy_cost_multiplier_modifier = 0.10 tooltip = bureaucracy_cost_multiplier_modifier_tt }
add_to_variable = { SOV_just_inner_production_speed_buildings_factor_modifier = 0.06 tooltip = production_speed_buildings_factor_tt }
```

### Internal factions (10 foci; cost 2: 3, 3: 3, 5: 3, 7: 1)

- Effects: faction opinion 50 %, event 50 %, idea swap 30 %, custom tooltip 30 %, stability 20 %, corruption 20 %, dyn-modifier change 10 %, treasury 10 %.
- Medians where present: stability +0.05, dyn lines 4; 4 visible lines.
- Downside in 30 % of foci.
- Pattern: Winner +5..+10, loser -10..-40, stability +0.05, corruption -1, seizures +50 treasury. Verdict foci show both outcomes in `effect_tooltip` and resolve by event.

`SOV_purge_disloyal_oligarchs` (Purge Disloyal Oligarchs, cost 3)
```
decrease_corruption = yes
add_war_support = 0.03
set_temp_variable = { temp_opinion = -25 }
change_oligarchs_opinion = yes
set_temp_variable = { treasury_change = 50.5 }
modify_treasury_effect = yes
country_event = { id = sov_economic.26 days = 1 }
if = {
	limit = { has_idea = SOV_corrupt_oligarchy }
	remove_ideas = SOV_corrupt_oligarchy
}
```
`SOV_the_grand_bargain` (The Grand Bargain, cost 5)
```
add_stability = 0.05
set_temp_variable = { temp_opinion = 7 }
change_oligarchs_opinion = yes
```
`SOV_end_lawsuits_against_oligarchs` (End Lawsuits Against Oligarchs, cost 5)
```
add_stability = 0.05
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_russian_oligarchs_modifier }
add_to_variable = { SOV_oligarchs_corruption_cost_factor = 0.10 tooltip = corruption_cost_factor_tt }
add_to_variable = { SOV_oligarchs_political_power_factor = 0.05 tooltip = political_power_factor_tt }
add_to_variable = { SOV_oligarchs_tax_cost_factor = -0.02 tooltip = consumer_goods_factor_tt }
add_to_variable = { SOV_oligarchs_neutrality_drift_factor = 0.03 tooltip = neutrality_drift_tt }
set_temp_variable = { temp_opinion = 10 }
change_oligarchs_opinion = yes
```

### Foreign policy / influence / alliances (198 foci; cost 1: 4, 2: 28, 3: 59, 5: 44, 6: 6, 7: 57)

- Effects: event 35 %, custom tooltip 26 %, opinion modifier 23 %, influence 18 %, scripted helper 16 %, decision unlock 12 %, wargoal 8 %, threat 8 %.
- Medians where present: PP 150, stability +0.05, treasury -4.5, buildings 3, dyn lines 2; 3 visible lines.
- Downside in 11 % of foci.
- Pattern: Own opinion + their opinion (`has_expressed_loyalty`) + influence +2..+5 + trade agreement + international investment +1. Partnerships use the offer pattern: event to the partner, `TT_IF_THEY_ACCEPT` and `effect_tooltip` with both outcomes, rejection = their opinion -medium. 20 foci create wargoals. Few have a cost: 11 % carry a downside.

`SOV_befriend_india` (Befriend India, cost 5)
```
RAJ = { add_opinion_modifier = { target = SOV modifier = has_expressed_loyalty } }
add_opinion_modifier = { target = RAJ modifier = has_expressed_loyalty }
set_temp_variable = { percent_change = 2 }
set_temp_variable = { influence_target = RAJ.id }
change_influence_percentage = yes
```
`SOV_freind_kaz` (Friendship with Kazakhstan, cost 7)
```
KAZ = { add_opinion_modifier = { target = SOV modifier = has_expressed_loyalty } }
add_opinion_modifier = { target = KAZ modifier = has_expressed_loyalty }
set_temp_variable = { percent_change = 3 }
set_temp_variable = { influence_target = KAZ }
change_influence_percentage = yes
set_temp_variable = { receiver_nation = KAZ.id }
set_temp_variable = { sender_nation = SOV }
set_improved_trade_agreement = yes
set_temp_variable = { int_investment_change = 1 }
modify_international_investment_effect = yes
```
`SOV_volkswagen` (Volkswagen, cost 7)
```
GER = { country_event = { id = russia.32 days = 1 } }
custom_effect_tooltip = TT_IF_THEY_ACCEPT
effect_tooltip = {
	GER = { one_random_arms_factory = yes }
	one_random_arms_factory = yes
}
custom_effect_tooltip = TT_IF_THEY_REJECT
effect_tooltip = {
	GER = { add_opinion_modifier = { target = SOV modifier = medium_decrease } }
}
```
*Counter-example (do not copy): sets a guarantee in CHI scope without CHI agreeing.*

`SOV_alliance_with_china` (Shanghai Conference, cost 7)
```
CHI = {
	add_opinion_modifier = { target = ROOT modifier = has_expressed_loyalty }
	reverse_add_opinion_modifier = { target = ROOT modifier = has_expressed_loyalty }
	diplomatic_relation = {
		country = SOV
		relation = guarantee
	}
}
diplomatic_relation = {
	country = CHI
	relation = guarantee
}
```

### Society / stability / propaganda (57 foci; cost 2: 1, 3: 19, 5: 19, 7: 18)

- Effects: dyn-modifier change 40 %, ideology popularity 18 %, add idea 12 %, stability 12 %, balance of power 12 %, PP 12 %, idea swap 12 %, budget/law helper 11 %.
- Medians where present: PP 70, stability +0.04, treasury -10.5, dyn lines 2; 2 visible lines.
- Downside in 39 % of foci.
- Pattern: Stability +0.03..+0.05, PP 70-75, timed idea 365 d, ideology popularity +0.05..+0.10, a budget-law step (social, health, education), stability or war-support factor 0.01-0.02, Europeanism +0.03. Costs: bureaucracy +0.07, stability -0.05 for repression.

`SOV_social_conservatism` (Social Conservatism, cost 3)
```
add_political_power = 70
add_timed_idea = { idea = SOV_idea_social_conservatism days = 365 }
```
`SOV_honor_gorbachevs_legacy` (Honor Gorbachev's Legacy, cost 3)
```
add_political_power = 75
add_popularity = {
	ideology = democratic
	popularity = 0.05
}
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_revived_politburo_modifier }
add_to_variable = { SOV_revived_politburo_democratic_support = 0.05 tooltip = democratic_drift_tt }
add_to_variable = { SOV_revived_politburo_drift_defence_factor = 0.05 tooltip = drift_defence_factor_tt }
hidden_effect = {
	country_event = russia.102
}
```
`SOV_2011_healthcare_reforms` (2011 Healthcare Reforms, cost 5)
```
add_stability = 0.03
set_temp_variable = { party_index = 6 }
set_temp_variable = { party_popularity_increase = 0.025 }
change_relative_party_popularity = yes
increase_healthcare_budget = yes
```
`SOV_real_welfare` (A Real Social Welfare, cost 7)
```
increase_social_spending = yes
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_just_inner_modifier }
add_to_variable = { SOV_just_inner_bureaucracy_cost_multiplier_modifier = 0.07 tooltip = bureaucracy_cost_multiplier_modifier_tt }
if = {
	limit = { NOT = { has_global_flag = GAME_RULE_eu_disabled } }
	set_temp_variable = { modify_europeanism = 0.03 }
	set_temp_variable = { modify_europeanism_target = ROOT }
	europeanism_change = yes
}
```

### Regions / subjects (31 foci; cost 2: 3, 3: 14, 4: 7, 5: 6, 7: 1)

- Effects: custom tooltip 65 %, event 26 %, scripted helper 19 %, PP 10 %, budget/law helper 10 %, decision unlock 10 %, stability 6 %, set capital 6 %.
- Medians where present: PP 90, stability +0.035, dyn lines 2.5; 2 visible lines.
- Downside in 13 % of foci.
- Pattern: Separatism -1/-2 per focus (`SUB_separatism_minus_subject` behind a custom tooltip) + stability +0.02. Referendum foci send one event to the subject, which decides. Capital move = `set_capital` + decentralisation + PP 80. 65 % of the theme rely on custom tooltips; `SOV_usr` hides stability -25 %.

`SOV_subjects` (Subjects of the Federation, cost 2)
```
add_stability = 0.02
custom_effect_tooltip = SOV_subjectsepar_minus_tt
hidden_effect = {
	SUB_separatism_minus_subject = yes
}
```
`SOV_referendum_in_tatarstan` (Status of [TAT.GetNameWithFlag], cost 4)
```
country_event = { id = subject_rus.91 days = 1 }
custom_effect_tooltip = SOV_subject_referendum_tt
```
`SOV_nazbols_ekb` (Move the Capital to Yekaterinburg, cost 3)
```
unlock_decision_tooltip = SOV_ekb_build
decrease_centralization = yes
set_capital = { state = 676 }
add_political_power = 80
set_country_flag = SOV_moscow_no_more
MSC_abolish_mayor_office = yes
```
*Counter-example (do not copy): stability -25 % hidden inside `hidden_effect`.*

`SOV_usr` (United States of Russia, cost 5)
```
custom_effect_tooltip = SOV_usr_check_tt
custom_effect_tooltip = SOV_subjectsepar_minus_tt
add_power_balance_value = {
	id = SOV_west_east_bop
	value = -0.20
	tooltip_side = SOV_west_east_bop_left_side
}
hidden_effect = {
	SUB_separatism_minus_subject = yes
	increase_centralization = yes
	russian_remove_national_core = yes
	russian_new_states = yes
	add_stability = -0.25
	set_cosmetic_tag = SOV_USA
	clr_country_flag = dynamic_flag
	news_event = {
		hours = 6
		id = sov_liberals_news.1
	}
}
if = {
	limit = { NOT = { has_global_flag = GAME_RULE_eu_disabled } }
	set_temp_variable = { modify_europeanism = 0.03 }
	set_temp_variable = { modify_europeanism_target = ROOT }
	europeanism_change = yes
}
```

## 4. Special patterns

### 4.1 Russia's own dynamic modifiers

- **Six base modifiers** are switched on in the 2000 history file and stay for the whole game: `SOV_economy_modifier`, `SOV_capitalisation_modifier`, `SOV_landforce_modifier`, `SOV_airforce_modifier`, `SOV_navy_modifier` and `SOV_intelligence_modifier`. Each modifier key reads one variable, e.g. `research_speed_factor = SOV_econ_research_speed_factor`. Prefixes: `SOV_econ_`, `SOV_land_`, `SOV_air_`, `SOV_navy_`, `SOV_intel_`, `SOV_cap_`.
- **Party/leader modifiers** are switched on by the path's entry focus: `SOV_putin_politic_`, `SOV_just_inner_`, `SOV_navalny_inner_` (Yavlinsky, Navalny and Nemtsov share it), `SOV_koba_politic_` and `SOV_revived_politburo_` (CPRF). The entry focus first sets 2-3 starting values, then adds the modifier. Example:
```
add_to_variable = { SOV_navalny_inner_political_power_factor = 0.05 tooltip = political_power_factor_tt }
add_to_variable = { SOV_navalny_inner_stability_factor = 0.10 tooltip = stability_factor_tt }
add_dynamic_modifier = { modifier = SOV_navalny_inner_modifier }
```
- **How a focus changes a modifier:** one header line, then 1-n variable lines. The header is `custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = SOV_economy_modifier }`; each line is `add_to_variable = { SOV_econ_x = v tooltip = x_tt }`, so the tooltip uses the modifier's own loc key. MD never calls `force_update_dynamic_modifier` in foci; the modifier refreshes on its own. Our DSL adds it, which is fine.
  - Median 2 lines; 180 of 227 such foci touch one modifier only.
  - 32 % mix a cost line (bureaucracy, police or education cost, consumer goods) into the same block.
  - The largest single blocks are 8 navy lines (`SOV_The_high_seas_fleet`, `SOV_fleet`) and 9 landforce lines (`SOV_til_vs`).
- **Sphere mirror:** economy foci also add the same or smaller values (e.g. +0.03 at home, +0.01 for the sphere) to `SOV_econsub_*` inside `hidden_effect`. These feed `SUB_russian_economy_modifier` for Russian sphere members. Equivalent for us: the `commonwealth`/`union` groups.
- **Penalty-offset modifier:** Sanctions events push the variables of `SOV_western_sanctions_modifier` negative (`SOV_sanctions_roi` -0.04, `office_tax_gain` -0.04, ...) and crisis foci add positive amounts back (+0.01..+0.05). A crisis is solved by refilling a modifier, not by deleting an idea.
- **Progress meters:** `SOV_modify_economic = 1/2` + `SOV_modify_economic_support = yes` moves the national economy meter `SOV_economic` (0-30, 47 foci). `SOV_modify_capitalisation_<company>` (±0.2..8.5, 30 calls) moves company value; a monthly effect turns that into the `SOV_cap_*` modifier lines.
- **Complex effects behind a tooltip:** `SOV_npp` hides `add_dynamic_modifier` and shows its own `custom_effect_tooltip`. Separatism helpers and the sphere mirror work the same way: the effect is hidden, the tooltip states it.

### 4.2 How ideas evolve (swap ladders)

| Ladder | Steps (foci) | What changes |
|---|---|---|
| Kasyanov reform | `SOV_kasyanov_political` → 1 → 2 → 3 → 4 (`ease_administrative_pressure`, `kasyanov_economic_reform`, `kasyanov_human_capital`, `reduce_taxes_on_small_businesses`) | each tier keeps the daily PP malus (-0.03 → -0.07) and adds a new bonus (bureaucracy -25 %, cycles -10 %, factory output +15-20 %, population tax +10 %) |
| Zhirinovsky party (loyal / disloyal) | idea → 1 → 2 → 3 (3 foci each) | loyal: drift defence 0.10 → 0.25, PP 0.02 → 0.05, corruption -0.05 → -0.15; disloyal: PP 0.04 → 0.15, corruption cost +0.05 → +0.15 |
| Outdated Army (start spirit) | 0 → 1 → 2 → 3 (`finish_1998_reforms`, `2001_military_reforms`, `2008_military_reforms`) | attack/defence -20 % → -5 %, org -15 % → 0, personnel cost +7 % → 0 |
| Plundered Navy (start spirit) | 1 → 2 → 3 (`start_fleet_reforms`, `Updated_naval_doctrine`) | every naval malus shrinks by ~1/3 per step |
| Ruble Collapse (crisis spirit) | 0 → 1 → 2 (`fnb_destroyed`, `prevent_ruble_collapse`) | construction/factory/stability malus shrinks; personnel cost stays |
| Media control / independent media | idea → 1 → 2 → 3 | cost or benefit grows per step |
| Form of government | semi-presidential → presidential / parliamentary | exclusive swaps |

Rules seen: (1) a ladder lets the player *remove a start malus step by step* or *grow one idea instead of adding new ones*; (2) every step is guarded `if = { limit = { has_idea = old } swap_ideas = {...} } else_if = { add_ideas = new }`; (3) good tiers keep a trade-off, e.g. Kasyanov's PP malus grows with the bonus.

### 4.3 How party paths are rewarded

- **Entry focus (cost 1-2), e.g. `SOV_putin`, `SOV_zyuganov`, `SOV_zhirinovsky`, `SOV_yavlinskiy`, `SOV_navalny`, `SOV_a_just_russia`:**
  - change the ruling party if needed (`rul_party_temp`, mostly hidden)
  - party +0.10 with outlook +0.10 (AI-only ±0.75 swing inside `is_ai = yes`)
  - new leader via `create_country_leader` with ideology and traits
  - switch on the path's dynamic modifier with 2 starting lines: PP factor +0.03..+0.05 plus stability (-0.04..+0.10) or drift
  - a path flag (`sov_putin_econ`) that clears the rivals' flags
  - a narrative event, sometimes a news event
  - PP only in a few (A Just Russia: 75)
- **Later foci:** 1-3 lines on the path modifier (party_state-like: PP factor, stability, drift, bureaucracy cost), BoP ±0.20, PP 50-100, small party popularity (+0.02; party index 22 gets +0.02 in 17 army foci unless the PMC parties exist), ideology popularity +0.05..+0.10, idea ladders, election rules. The path's economy foci reuse the same building/treasury bundles as the main economy tree.
- **Path ends:** cosmetic tag, new leader trait, idea capstone. Little extra size: cost-7 liberal foci are the same size as cost-3 ones.

### 4.4 How the economy branch pays for buildings

- **Two ways, both paid.**
  - **Helpers** with built-in price: `one_random_industrial_complex` charges 7.5 via `treasury_change`. MD never sets `skip_payment` in foci.
  - **Direct placement** in named states: `add_building_construction` + `add_extra_state_shared_building_slots` + an explicit `treasury_change`. The price is close to the helper price: IC 8.5, infrastructure 3.5, agriculture district 4, dockyard 5-7.5 per level, rocket site 2, radar 1.75. Arms factories with an equipment bonus cost 10-20.
- **Payment rate:** 76 of 79 building foci pay. The 3 exceptions are `SOV_economic_mechel`, `SOV_rosatom_predmet_zoloto` and `SOV_rosatom_fuel_division2`.
- **Extra money effects:** the economy meter tick and a capitalisation change usually come with the building. Big programmes are paid as one sum: Trans-Siberian -42, Stabilisation Fund -155, Space Marines -100.
- **For us:** MD pays 7.5 per factory at a Russian GDP of roughly 1.5-2 trillion model dollars (estimated from MD 2.0 `gdp_per_capita` 14.57 × ~146 M; not verified in game), i.e. about 0.4-0.5 % of GDP per factory. The COLDWAR design charges 0.6-1.5 % per building via `skip_payment` + `COLDWAR_SOV_pay_gdp_share`, about twice MD's relative price but proportional to the same price list. Section 5 keeps the design scale (1 factory = 0.8 % GDP).

### 4.5 How the military branch gives XP, equipment and tech

- **XP:** only 7 foci. Army 15-50, navy 10-50, air 15-25, always in "reform" foci, often with PP 50 and an idea-ladder step.
- **Tech:** 29 foci, `add_tech_bonus` mostly 0.5 ×1. Kit foci stack categories, e.g. Armata: AFV 0.35 ×2 + APC 0.35 ×2 + light tanks 0.75 ×1. DLC-dependent bonuses are wrapped in `if = { limit = { has_dlc = ... } }`.
- **Equipment:** 11 foci, small and specific: 8 TOS-1, 150-500 drones, 100-1100 armoured vehicles, 25 ICBMs with `set_technology`.
- **Equipment cost:** `add_equipment_bonus` -7 % (artillery -13 %) with `instant = yes` on 12 equipment types, in 7 arms-company foci (cost 5), each with 1 arms factory.
- **Modifiers:** the landforce modifier is the default army reward. Combat stats are 15 % of its lines (median 0.03, core defence up to 0.10) and always sit next to other lines; Ratnik gives defence +5 %, infantry attack +5 %, org +3 % and pays personnel cost +9 %. Specialised lines (planning, initiative, supply, special forces, acclimatisation) are the norm.
- **Not used in foci:** command power, mastery, special projects, research slots. There is one doctrine cost reduction (navy) and one MIO unlock.

### 4.6 How foreign policy treats other countries

- **Offer pattern (57 foci):** `TAG = { country_event = ... }` + `custom_effect_tooltip = TT_IF_THEY_ACCEPT` + `effect_tooltip = { ...both sides... }` + `TT_IF_THEY_REJECT` + `effect_tooltip = { their opinion -medium }`. The partner decides in the event; nothing is executed before. This is the model for our `offer(key)`. Examples: `SOV_volkswagen`, `SOV_us_russia_defence_pact`, `SOV_praise_china`.
- **Unilateral but soft (most common):**
  - our opinion of them: `add_opinion_modifier = { target = KAZ ... }`
  - their opinion of us: `KAZ = { add_opinion_modifier = { target = SOV ... } }`, in 48 foci
  - influence +2..+5 (`change_influence_percentage`), trade agreement, international investment +1
- **Imposing (about 10 foci):** guarantees and NAPs set in the partner's scope (`SOV_alliance_with_china`, `SOV_alliance_with_india`, `SOV_unite_with_asia`), annexation of puppets, hidden `transfer_state`/`set_autonomy`, `start_civil_war` in Belarus, and 20 wargoal foci.
- **Our multiplayer rule** keeps only our own side: our opinion, our influence and our modifiers, plus `offer(key)` for anything the partner gets or gives. Their opinion of us, their diplomatic relations, faction entry, territory and puppet status only change inside the accepted offer event.

### 4.7 Hidden and AI-only effects

- `ai_russian_popularity_assistant` (88 foci, hidden, `is_ai = yes`) pushes the AI's path party by +0.15; entry foci also swing the AI's parties by ±0.75. Acceptable for AI steering, never for players.
- Hidden *negative* effects exist in 4 foci (`SOV_usr` stability -0.25, `SOV_regional_control` oligarchs -40, `SOV_new_cosmic_warfare` -20, `SOV_vstavai_strana` -7 in five parts). We do not copy that.

## 5. Rulebook for COLDWAR_SOV (DSL)

The DSL kinds are those compiled by `/home/claude/sovgen/cw_effects.py` `compile_effect`. Values follow MD's sizes; the *amount per cost* is stricter than MD (see 5.1). Machine-readable version: `/home/claude/audit/md_effect_norms.json`.

### 5.1 Reward budget per cost

Reward points (our rule): one typical MD reward line = 1 point, so the MD cost-3 median focus (3 lines) ≈ 3 points.

| Effect | Points |
|---|---|
| `pp` | v / 50 |
| `stab` | v / 0.02 |
| `ws` | v / 0.03 |
| `dyn`/`prog` line in the good direction | abs(v) / MD-typical size of that modifier, max 3 (default 0.03; e.g. research 0.02, stability 0.02, PP factor 0.05, planning 0.05, subversive activities 0.15, rocket attack 0.10; full table in the JSON) |
| `dyn`/`prog` line in the cost direction | -1 |
| ideology drift line | 0.5 |
| `tech` | 3 × b × n (extra categories in the same bonus add nothing) |
| `build`, net of price, per building | IC / arms / dockyard 1 · office 1.5 · microchip 1.4 · reactor 1.2 · infrastructure / agriculture 0.5 · air base 0.4 |
| `fac` | v / 10 |
| `party` | v / 0.04 |
| `outlook` | v / 0.06 |
| `xp` | v / 25 |
| `infl` | v / 3 per tag |
| `coh` | v / 2 |
| `gdp_gain` | v / 0.005 |
| `gdp` | -v / 0.005 |
| `decision` (real) | 1 |
| `idea` (permanent or ladder step) | 2 |
| timed `idea` | 1.5 |
| `corr` | ±1 |
| `law` | 0.5 |
| `sp` | v / 0.1 |
| `mastery` | v / 25 |
| resource (custom) | 1 |
| `offer` | 1.5 (expected value, no advance reward) |
| `bop`, `tension`, `rp`, `flag`, `event`, `op` | 0 (direction, not reward) |

| Cost | Points | Effect kinds | Lines | Typical values | Downside |
|---|---|---|---|---|---|
| 2 (entry/hub) | 2-3.5 | 1-2 | 2-3 | pp 50-100 **or** party 0.10/o 0.10 (path entry) **or** 1-2 dyn lines 0.02-0.05; stab ≤ 0.03; no buildings | optional (≈10 %) |
| 3 | 3-4 | 2-3 | 3-4 | pp 50-75; stab 0.02-0.03; 2 dyn lines 0.02-0.05; fac +5; party +0.02; tech 0.5 ×1; xp 25; infl 3; coh 1-2; bop 0.03-0.05; max 1 paid building; gdp 0.003-0.006 | ≈30 % |
| 5 | 5-6 | 3-4 | 4-5 | pp 75-100; stab 0.03-0.05; 2-4 dyn lines 0.03-0.07; fac +5..+10; tech 0.5-0.75 ×1-2; 1-2 paid buildings; xp 25-35; infl 3-5; coh 2-3; bop 0.05-0.10; gdp 0.006-0.012 | ≈45 % |
| 7 | 7-9 | 3-5 | 5-7 | pp 100-150; stab 0.04-0.06; 3-4 dyn lines incl. one 0.07-0.10; 2-4 paid buildings; tech 0.75 ×1 or 0.5 ×2; xp 50 (or mastery 50); fac +10; coh 3-5; idea-ladder step; gdp 0.01-0.025 or gdp_gain 0.01-0.03 with a political cost | ≈45 % |
| 10 (capstone) | 10-13 | 4-6 | 6-9 | as 7 plus a spirit/idea capstone, sp 0.25, tech 0.75-1.0 ×2 | ≈60 % |

A downside refunds points; one visible cost per focus is normal from cost 5 up. In order of MD frequency: money (`gdp`/building price), a cost line on the same modifier, an idea trade-off, a faction loss, a stability loss.

### 5.2 Money (GDP share)

- **Buildings:** always `{"k":"build","helper":...,"cost":share}`. Shares (1 factory = 0.008, scaled by MD's price list):
  - IC / arms factory / dockyard 0.008
  - office 0.013 · nuclear reactor 0.0095 · microchip plant 0.011 · renewable 0.009
  - energy/industrial infrastructure 0.007
  - infrastructure / agriculture district 0.004
  - anti-air 0.0035 · air base / fuel silo / internet station 0.003 · radar 0.002
  - `two_`/`three_` helpers ×2/×3
- **Pure costs** (`gdp`): programmes without buildings 0.003-0.006 at cost 3, 0.006-0.012 at cost 5-7, up to 0.025 for flagship programmes (MD's median -7.5 / -10, large -20..-40).
- **Income** (`gdp_gain`): only with a political price (faction -10..-25, corruption +1, tension, idea trade-off), 0.01-0.03. All 7 MD treasury gains are seizures or repatriations.
- **Debt** (`debt`): rare (MD 1 focus), for big credit-financed deals: debt 0.005-0.01.

### 5.3 Theme bundles

Bundles per cost tier, scored with 5.1; `<...>` are placeholders. Every non-placeholder line compiles with `compile_effect` (203 effects tested). Downsides are the usual alternatives, pick one; each refunds about 0.5-1.5 points. The MD source of each bundle is in section 3.

**Industry / construction**. MD: paid buildings (helper with built-in price or add_building_construction + treasury_change ~= helper price) + economy-meter tick + 0-2 economy modifier lines; 47 % of industry foci have no other reward.

cost 3 (3 points):
```python
{"k": "build", "helper": "one_random_industrial_complex", "cost": 0.008},
{"k": "dyn", "g": "gosplan", "mods": {"production_speed_buildings_factor": 0.03, "production_factory_max_efficiency_factor": 0.03}}
```
cost 5 (5.33 points):
```python
{"k": "build", "helper": "two_random_industrial_complex", "cost": 0.016},
{"k": "dyn", "g": "gosplan", "mods": {"production_speed_buildings_factor": 0.05, "productivity_growth_modifier": 0.02}},
{"k": "stab", "v": 0.02}
```
cost 7 (7.67 points):
```python
{"k": "build", "helper": "three_random_industrial_complex", "cost": 0.024},
{"k": "build", "helper": "two_random_infrastructure", "cost": 0.008},
{"k": "dyn", "g": "gosplan", "mods": {"production_speed_buildings_factor": 0.05, "productivity_growth_modifier": 0.03}},
{"k": "stab", "v": 0.02}
```
downside options:
```python
{"k": "dyn", "g": "gosplan", "mods": {"consumer_goods_factor": 0.02}},
{"k": "fac", "f": "labour_unions", "v": -5}
```

**Economy / finance**. MD: economy-modifier lines (corporate tax/tax gain/ROI +0.01..+0.05), treasury +/- (crisis foci pay 10-40 bn), negative-spirit swap ladders (Ruble Collapse 3 tiers), tax-rate helpers (+5 corporate / -5 population), oligarch/banker faction shifts.

cost 3 (3 points):
```python
{"k": "dyn", "g": "gosplan", "mods": {"tax_gain_multiplier_modifier": 0.045, "productivity_growth_modifier": 0.03}},
{"k": "pp", "v": 50}
```
cost 5 (5.44 points):
```python
{"k": "dyn", "g": "gosplan", "mods": {"tax_gain_multiplier_modifier": 0.05, "productivity_growth_modifier": 0.04}},
{"k": "pp", "v": 75},
{"k": "stab", "v": 0.03}
```
cost 7 (7.67 points):
```python
{"k": "idea", "id": "COLDWAR_SOV_<reform_tier_n+1>", "swap": "<Reform Tier n display name>"},
{"k": "gdp_gain", "v": 0.02},
{"k": "dyn", "g": "gosplan", "mods": {"productivity_growth_modifier": 0.05}},
{"k": "fac", "f": "communist_cadres", "v": -10},
{"k": "pp", "v": 50}
```
downside options:
```python
{"k": "gdp", "v": 0.005},
{"k": "fac", "f": "industrial_conglomerates", "v": -5},
{"k": "corr", "helper": "increase_corruption", "v": 1},
{"k": "dyn", "g": "gosplan", "mods": {"consumer_goods_factor": 0.02}}
```

**Agriculture**. MD: agriculture districts (4 for 16 bn) + agriculture tax/productivity lines (0.01-0.12) + economy meter; collectivisation-type foci pay with stability -0.05.

cost 3 (3.33 points):
```python
{"k": "dyn", "g": "gosplan", "mods": {"agricolture_productivity_modifier": 0.04, "agriculture_tax_modifier": 0.01}},
{"k": "fac", "f": "farmers", "v": 5},
{"k": "pp", "v": 25}
```
cost 5 (5.17 points):
```python
{"k": "build", "helper": "two_random_agriculture_district", "cost": 0.008},
{"k": "dyn", "g": "gosplan", "mods": {"agricolture_productivity_modifier": 0.05, "agriculture_tax_modifier": 0.01}},
{"k": "fac", "f": "farmers", "v": 5},
{"k": "stab", "v": 0.02}
```
cost 7 (8.67 points):
```python
{"k": "build", "helper": "two_random_agriculture_district", "cost": 0.008},
{"k": "build", "helper": "one_random_agriculture_district", "cost": 0.004},
{"k": "dyn", "g": "gosplan", "mods": {"agricolture_productivity_modifier": 0.08, "agriculture_tax_modifier": 0.02}},
{"k": "stab", "v": 0.03},
{"k": "fac", "f": "farmers", "v": 10}
```
downside options:
```python
{"k": "dyn", "g": "gosplan", "mods": {"social_cost_multiplier_modifier": 0.03}},
{"k": "stab", "v": -0.03},
{"k": "dyn", "g": "gosplan", "mods": {"bureaucracy_cost_multiplier_modifier": 0.07}}
```

**Energy / resources**. MD: add_resource +2..+8 per state (median 3) + small paid building (IC, fuel silo) + treasury -2..-15 + export-multiplier lines + company capitalisation + unlock 1 decision; 73 % of energy foci call a helper (economy meter/capitalisation).

cost 3 (3 points):
```python
{"k": "custom", "t": "add_resource +3 oil/gas/steel in one owned state (random_owned_controlled_state)"},
{"k": "dyn", "g": "gosplan", "mods": {"oil_export_multiplier_modifier": 0.02, "energy_gain_multiplier": 0.03}}
```
cost 5 (5.23 points):
```python
{"k": "custom", "t": "add_resource +4..+6"},
{"k": "build", "helper": "one_random_energy_infrastructure", "cost": 0.007},
{"k": "dyn", "g": "gosplan", "mods": {"energy_gain_multiplier": 0.03, "resource_export_multiplier_modifier": 0.04}},
{"k": "decision", "key": "COLDWAR_SOV_<field_expansion>"}
```
cost 7 (7.37 points):
```python
{"k": "custom", "t": "add_resource +8..+10"},
{"k": "build", "helper": "one_random_nuclear_reactor", "cost": 0.0095},
{"k": "dyn", "g": "gosplan", "mods": {"energy_gain_multiplier": 0.05, "oil_export_multiplier_modifier": 0.04}},
{"k": "tech", "cats": ["CAT_nuclear_reactors"], "b": 0.5, "n": 1}
```
downside options:
```python
{"k": "gdp", "v": 0.003},
{"k": "fac", "f": "<energy lobby or farmers>", "v": -5},
{"k": "dyn", "g": "gosplan", "mods": {"energy_use_multiplier": 0.03}}
```

**Research / science / space**. MD: add_tech_bonus (internet 1.0 x2, satellites 0.5 x3, IT 0.3 x1) + economy research/internet-build lines 0.01-0.05 + paid office/internet buildings; space foci pay 10-20 bn.

cost 3 (3 points):
```python
{"k": "tech", "cats": ["CAT_computing"], "b": 0.5, "n": 1},
{"k": "dyn", "g": "party_state", "mods": {"research_speed_factor": 0.02}},
{"k": "pp", "v": 25}
```
cost 5 (5 points):
```python
{"k": "tech", "cats": ["CAT_computing"], "b": 0.5, "n": 2},
{"k": "dyn", "g": "party_state", "mods": {"research_speed_factor": 0.02}},
{"k": "sp", "project": "sp_space_program", "v": 0.1}
```
cost 7 (7.15 points):
```python
{"k": "build", "helper": "one_random_microchip_plant", "cost": 0.011},
{"k": "tech", "cats": ["CAT_microchips"], "b": 0.75, "n": 1},
{"k": "dyn", "g": "party_state", "mods": {"research_speed_factor": 0.04}},
{"k": "sp", "project": "sp_space_program", "v": 0.15}
```
downside options:
```python
{"k": "gdp", "v": 0.005},
{"k": "dyn", "g": "gosplan", "mods": {"education_cost_multiplier_modifier": 0.03}}
```

**Army**. MD: landforce modifier 2 lines of 0.02-0.05 (conscription, planning, special forces, supply) + party-22 popularity +0.02 + faction +3..+5 + treasury -3..-10; tech bonus 0.35-0.75 x1-2 for kit foci; XP 15-50 in reform foci; 'Outdated Army' 4-tier spirit ladder.

cost 3 (3.5 points):
```python
{"k": "dyn", "g": "armed_forces", "mods": {"planning_speed": 0.05, "conscription_factor": 0.02}},
{"k": "fac", "f": "the_military", "v": 5},
{"k": "xp", "kind": "army", "v": 25}
```
cost 5 (5.87 points):
```python
{"k": "tech", "cats": ["CAT_main_battle_tanks"], "b": 0.5, "n": 2},
{"k": "dyn", "g": "armed_forces", "mods": {"army_org_factor": 0.03, "training_time_factor": -0.05}},
{"k": "xp", "kind": "army", "v": 25},
{"k": "gdp", "v": 0.004}
```
cost 7 (7.73 points):
```python
{"k": "idea", "id": "COLDWAR_SOV_<army_spirit_tier_n+1>", "swap": "<Army Spirit Tier n display name>"},
{"k": "xp", "kind": "army", "v": 50},
{"k": "mastery", "folder": "land", "v": 50},
{"k": "dyn", "g": "armed_forces", "mods": {"army_morale_factor": 0.05, "breakthrough_factor": 0.05}},
{"k": "gdp", "v": 0.008}
```
downside options:
```python
{"k": "gdp", "v": 0.004},
{"k": "dyn", "g": "armed_forces", "mods": {"army_personnel_cost_multiplier_modifier": 0.05}},
{"k": "fac", "f": "communist_cadres", "v": -5}
```

**Navy**. MD: navy modifier up to 8 lines of 0.01-0.08, dockyards level 2-3 placed directly and paid 15-25 bn, navy XP 50, PP 50, 'Plundered Navy' 3-tier swap ladder, doctrine cost reduction 0.5 x2, MIO unlock.

cost 3 (3 points):
```python
{"k": "dyn", "g": "armed_forces", "mods": {"naval_speed_factor": 0.04, "positioning": 0.04}},
{"k": "xp", "kind": "navy", "v": 25}
```
cost 5 (5 points):
```python
{"k": "build", "helper": "two_random_dockyards", "cost": 0.016},
{"k": "dyn", "g": "armed_forces", "mods": {"naval_speed_factor": 0.04, "navy_max_range_factor": 0.04}},
{"k": "sp", "project": "sp_naval_vessel_project", "v": 0.1}
```
cost 7 (7.5 points):
```python
{"k": "build", "helper": "two_random_dockyards", "cost": 0.016},
{"k": "xp", "kind": "navy", "v": 50},
{"k": "dyn", "g": "armed_forces", "mods": {"naval_speed_factor": 0.05, "positioning": 0.05}},
{"k": "sp", "project": "sp_naval_vessel_project", "v": 0.1}
```
downside options:
```python
{"k": "gdp", "v": 0.004},
{"k": "dyn", "g": "armed_forces", "mods": {"equipment_cost_multiplier_modifier": 0.02}}
```

**Air force**. MD: tech bonus (5th-gen fighter 0.55 x1, aircraft 0.25 x1) + air modifier (air defence 0.10-0.15, XP gain 0.02-0.03) + air bases via helper + air XP 15-25 + treasury -3..-10 + party 22 +0.02.

cost 3 (3.37 points):
```python
{"k": "tech", "cats": ["CAT_medium_aircraft"], "b": 0.5, "n": 1},
{"k": "dyn", "g": "armed_forces", "mods": {"air_defence_factor": 0.05}},
{"k": "xp", "kind": "air", "v": 25},
{"k": "gdp", "v": 0.004}
```
cost 5 (5.13 points):
```python
{"k": "build", "helper": "two_air_base", "cost": 0.006},
{"k": "dyn", "g": "armed_forces", "mods": {"air_defence_factor": 0.05, "air_accidents_factor": -0.05}},
{"k": "xp", "kind": "air", "v": 25}
```
cost 7 (7.65 points):
```python
{"k": "tech", "cats": ["CAT_medium_aircraft"], "b": 0.75, "n": 1},
{"k": "sp", "project": "sp_aircraft_project", "v": 0.2},
{"k": "xp", "kind": "air", "v": 50},
{"k": "mastery", "folder": "air", "v": 50},
{"k": "dyn", "g": "armed_forces", "mods": {"air_defence_factor": 0.03}},
{"k": "gdp", "v": 0.008}
```
downside options:
```python
{"k": "gdp", "v": 0.004}
```

**Strategic / nuclear / space-military**. MD: always paid (treasury -4..-20): rocket sites 3 for 6 bn, rocket attack 0.05-0.10, missile tech 0.75 x1, ICBM set_technology + 25 missiles; never free.

cost 3 (3.12 points):
```python
{"k": "dyn", "g": "armed_forces", "mods": {"rocket_attack_factor": 0.1}},
{"k": "tech", "cats": ["CAT_missiles"], "b": 0.75, "n": 1},
{"k": "ws", "v": 0.02},
{"k": "gdp", "v": 0.004}
```
cost 5 (4.97 points):
```python
{"k": "tech", "cats": ["CAT_intercontinental_ballistic_missiles"], "b": 0.5, "n": 2},
{"k": "sp", "project": "<missile/nuclear project>", "v": 0.15},
{"k": "dyn", "g": "armed_forces", "mods": {"rocket_attack_factor": 0.1}},
{"k": "ws", "v": 0.02},
{"k": "gdp", "v": 0.006},
{"k": "tension", "v": 1}
```
cost 7 (7.27 points):
```python
{"k": "tech", "cats": ["CAT_nuclear"], "b": 0.75, "n": 2},
{"k": "sp", "project": "<missile/nuclear project>", "v": 0.25},
{"k": "dyn", "g": "armed_forces", "mods": {"rocket_attack_factor": 0.1}},
{"k": "ws", "v": 0.05},
{"k": "gdp", "v": 0.012},
{"k": "tension", "v": 2},
{"k": "bop", "v": 0.05}
```
downside options:
```python
{"k": "gdp", "v": 0.004, "note": "strategic foci are always paid"},
{"k": "tension", "v": 1}
```

**Intelligence / internal security**. MD: intelligence modifier 2-5 lines (encryption 0.05-0.15, agency defence 0.10-0.20, influence defence 0.05-0.10) + intelligence community +4..+10 + separatism -1; costs: police cost +0.04, treasury -4; Rosgvardia template.

cost 3 (3.17 points):
```python
{"k": "dyn", "g": "party_state", "mods": {"foreign_subversive_activites": 0.15, "decryption_factor": 0.05, "encryption_factor": 0.1, "police_cost_multiplier_modifier": 0.02}},
{"k": "fac", "f": "intelligence_community", "v": 5}
```
cost 5 (5.37 points):
```python
{"k": "dyn", "g": "party_state", "mods": {"intel_network_gain_factor": 0.05, "foreign_subversive_activites": 0.15, "encryption_factor": 0.1, "intelligence_agency_defense": 0.1, "police_cost_multiplier_modifier": 0.03}},
{"k": "fac", "f": "intelligence_community", "v": 7},
{"k": "coh", "v": 2}
```
cost 7 (7.17 points):
```python
{"k": "idea", "id": "COLDWAR_SOV_<security_spirit>", "days": 730},
{"k": "stab", "v": 0.04},
{"k": "decision", "key": "COLDWAR_SOV_<operation>"},
{"k": "fac", "f": "intelligence_community", "v": 10},
{"k": "dyn", "g": "party_state", "mods": {"decryption_factor": 0.05}}
```
downside options:
```python
{"k": "dyn", "g": "party_state", "mods": {"police_cost_multiplier_modifier": 0.03}},
{"k": "fac", "f": "communist_cadres", "v": -5},
{"k": "gdp", "v": 0.004}
```

**Political / party**. MD: entry focus: ruling-party change + party +0.10 (outlook +0.10) + new leader + own dynamic modifier switched on with 2 starting lines (PP factor +0.03..+0.05, stability -0.04..+0.10); later foci: 1-3 lines on that modifier, BoP 0.20, PP 50-100, party +0.02, 3-5-tier idea ladders.

cost 2 (3.6 points):
```python
{"k": "rp", "i": "<party index>", "leader": "<leader name>"},
{"k": "party", "i": "<idx>", "v": 0.1, "o": 0.1},
{"k": "prog", "g": "<party/leader>", "mods": {"political_power_factor": 0.03, "stability_factor": 0.01}}
```
cost 3 (3 points):
```python
{"k": "prog", "g": "<party/leader>", "mods": {"political_power_factor": 0.05, "drift_defence_factor": 0.05}},
{"k": "party", "i": "<idx>", "v": 0.02, "o": 0.0},
{"k": "bop", "v": 0.05},
{"k": "pp", "v": 25}
```
cost 5 (5 points):
```python
{"k": "pp", "v": 100},
{"k": "stab", "v": 0.02},
{"k": "prog", "g": "<party/leader>", "mods": {"political_power_factor": 0.05, "stability_factor": 0.02}},
{"k": "bop", "v": 0.05}
```
cost 7 (7.75 points):
```python
{"k": "idea", "id": "COLDWAR_SOV_<party_idea_tier_n+1>", "swap": "<Tier n display name>"},
{"k": "pp", "v": 100},
{"k": "party", "i": "<idx>", "v": 0.03, "o": 0.0},
{"k": "prog", "g": "<party/leader>", "mods": {"political_power_factor": 0.05, "stability_factor": 0.02}},
{"k": "stab", "v": 0.02},
{"k": "bop", "v": 0.1}
```
downside options:
```python
{"k": "prog", "g": "<party/leader>", "mods": {"stability_factor": -0.03}},
{"k": "fac", "f": "<rival faction>", "v": -10},
{"k": "party", "i": "<rival idx>", "v": -0.03, "o": 0.0}
```

**Internal factions**. MD: faction opinion +5..+10 for the winner and -10..-40 for the loser, stability +0.05, corruption -1, asset seizure +50 bn treasury with oligarchs -25; 'which verdict' foci show both outcomes with effect_tooltip and resolve by event.

cost 3 (3 points):
```python
{"k": "fac", "f": "<winner>", "v": 10},
{"k": "fac", "f": "<loser>", "v": -5},
{"k": "pp", "v": 50},
{"k": "stab", "v": 0.03}
```
cost 5 (5 points):
```python
{"k": "fac", "f": "<winner>", "v": 10},
{"k": "fac", "f": "<loser>", "v": -10},
{"k": "stab", "v": 0.04},
{"k": "corr", "helper": "decrease_corruption", "v": -1},
{"k": "pp", "v": 50},
{"k": "dyn", "g": "party_state", "mods": {"drift_defence_factor": 0.05}}
```
cost 7 (7.2 points):
```python
{"k": "fac", "f": "<winner>", "v": 12},
{"k": "fac", "f": "<loser>", "v": -25},
{"k": "gdp_gain", "v": 0.02},
{"k": "stab", "v": 0.03},
{"k": "idea", "id": "COLDWAR_SOV_<settlement>", "days": 730},
{"k": "pp", "v": 75}
```
downside options:
```python
{"k": "fac", "f": "<loser>", "v": -15}
```

**Foreign policy / influence / alliances**. MD: own opinion + their opinion (has_expressed_loyalty) + influence +3 (2-5) + trade agreement + international investment +1 (14 'Friendship with X' foci, all cost 7); 57 foci use the offer pattern (country_event to the partner + TT_IF_THEY_ACCEPT + effect_tooltip of both outcomes); 20 create wargoals.

cost 3 (3.17 points):
```python
{"k": "op", "tag": "<TAG>", "key": "COLDWAR_SOV_<partner>", "v": 10},
{"k": "infl", "tags": ["<TAG>"], "v": 3},
{"k": "dyn", "g": "commonwealth", "mods": {"trade_opinion_factor": 0.05}},
{"k": "pp", "v": 25}
```
cost 5 (5.5 points):
```python
{"k": "offer", "key": "COLDWAR_SOV_offer_<deal>"},
{"k": "infl", "tags": ["<TAG>"], "v": 4},
{"k": "dyn", "g": "commonwealth", "mods": {"trade_opinion_factor": 0.05}},
{"k": "pp", "v": 50}
```
cost 7 (8.17 points):
```python
{"k": "offer", "key": "COLDWAR_SOV_offer_<treaty>"},
{"k": "infl", "tags": ["<TAG1>", "<TAG2>"], "v": 4},
{"k": "dyn", "g": "commonwealth", "mods": {"mdcw_cw_support_effectiveness": 0.1}},
{"k": "pp", "v": 50},
{"k": "tension", "v": -1}
```
downside options:
```python
{"k": "gdp", "v": 0.005},
{"k": "tension", "v": 2},
{"k": "op", "tag": "<rival>", "key": "COLDWAR_SOV_<rival_angered>", "v": -10}
```

**Society / stability / propaganda**. MD: stability +0.03..+0.05, PP 70-75, timed idea 365 d, ideology popularity +0.05..+0.10, budget-law helper +1 step (social/health/education), stability/war-support factor lines 0.01-0.02; costs: bureaucracy +0.07..+0.21, stability -0.05 for repressive choices.

cost 3 (3 points):
```python
{"k": "pp", "v": 50},
{"k": "idea", "id": "COLDWAR_SOV_<campaign>", "days": 365},
{"k": "stab", "v": 0.01}
```
cost 5 (5.33 points):
```python
{"k": "stab", "v": 0.04},
{"k": "law", "helper": "increase_social_spending"},
{"k": "dyn", "g": "party_state", "mods": {"stability_factor": 0.02}},
{"k": "outlook", "o": "<outlook 0-4>", "v": 0.05},
{"k": "pp", "v": 50}
```
cost 7 (7.33 points):
```python
{"k": "stab", "v": 0.05},
{"k": "prog", "g": "<leader>", "mods": {"stability_factor": 0.02, "political_power_factor": 0.05}},
{"k": "coh", "v": 2},
{"k": "pp", "v": 50},
{"k": "outlook", "o": "<outlook 0-4>", "v": 0.05}
```
downside options:
```python
{"k": "dyn", "g": "gosplan", "mods": {"social_cost_multiplier_modifier": 0.03}},
{"k": "stab", "v": -0.03},
{"k": "fac", "f": "communist_cadres", "v": -5}
```

**Regions / subjects**. MD: separatism -1/-2 per focus (SUB_separatism_minus_subject behind a custom tooltip) + stability +0.02; referendum foci fire one event to the subject (it decides); capital move = set_capital + decentralisation + PP 80.

cost 3 (3 points):
```python
{"k": "coh", "v": 3},
{"k": "stab", "v": 0.02},
{"k": "pp", "v": 25}
```
cost 5 (5 points):
```python
{"k": "coh", "v": 4},
{"k": "dyn", "g": "union", "mods": {"stability_factor": 0.02, "drift_defence_factor": 0.05}},
{"k": "pp", "v": 50}
```
cost 7 (7 points):
```python
{"k": "custom", "t": "republic_offer: each republic decides (cw_manual.republic_offer)"},
{"k": "coh", "v": 5},
{"k": "decision", "key": "COLDWAR_SOV_<republic_programme>"},
{"k": "dyn", "g": "union", "mods": {"stability_factor": 0.02}},
{"k": "bop", "v": -0.05},
{"k": "pp", "v": 75}
```
downside options:
```python
{"k": "coh", "v": -3},
{"k": "stab", "v": -0.03},
{"k": "dyn", "g": "union", "mods": {"nationalist_drift": 0.01}}
```

### 5.4 MD element → our DSL

| MD | Our DSL |
|---|---|
| `SOV_economy_modifier` lines | `dyn` g=`gosplan` |
| `SOV_landforce/airforce/navy_modifier` | `dyn` g=`armed_forces` |
| `SOV_intelligence_modifier` | `dyn` g=`party_state` (KGB lines: subversive activities, decryption, police cost) |
| party modifiers (`SOV_putin_politic`, `SOV_just_inner`, ...) | `prog` g=leader/party key |
| `SOV_econsub_*` mirror for sphere members | `dyn` g=`commonwealth` / `union` |
| `SOV_west_east_bop` ±0.20 | `bop` ±0.05 (±0.10 at cost 7, ±0.15 for path-deciding foci). We have ~3x more BoP foci, so this keeps MD's pace of 5-10 foci to win. |
| `change_<faction>_opinion` | `fac` (exact helper) |
| `change_relative_party_popularity` | `party` (i, v, o) |
| `add_popularity` | `outlook` |
| `change_ruling_party_effect` + `create_country_leader` | `rp` / `leader` |
| `SUB_separatism_minus_subject` | `coh` +1..+3 |
| `treasury_change` | `gdp` / `gdp_gain` / build `cost` |
| `change_influence_percentage` | `infl` (tags in `INFL_TAGS_OK`, ≤ 5 per focus) |
| offer pattern (`TT_IF_THEY_ACCEPT`) | `offer` |
| our `add_opinion_modifier` | `op` |
| `unlock_decision_tooltip` | `decision` |
| `swap_ideas` ladder | `idea` with `swap` = *display name* of the old idea (compile looks it up by name) |
| budget helpers | `law` (helper) / `setlaw` |
| `decrease_corruption` | `corr` v=-1 |

### 5.5 Never do
1. A focus whose only visible reward is a custom tooltip or design note (MD: 15 tooltip-only foci = 2 %; our design: 90 cost-3 'question' foci with only a note). A choice hub gives at least 25-50 PP, one dyn/prog line or a short timed idea.
2. Buildings without payment: every build helper runs with skip_payment and a GDP share; add_building_construction needs gdp() in the same focus (MD pays in 76 of 79 building foci, 1.0-1.15x the helper price).
3. Stand-alone combat buffs of +2-4 % (army attack/defence/breakthrough as the focus's only reward). MD uses combat stats in 15 % of its landforce lines (median 0.03), but always bundled with other lines. COLDWAR rule, stricter than MD: a combat line is >= 5 %, sits in a bundle and is paid for (gdp or a cost line); otherwise use XP, tech bonus, equipment, planning/org/supply lines, mastery or special projects.
4. Hidden downsides (MD SOV_usr hides stability -25 %, SOV_regional_control hides oligarchs -40). Every negative value is visible.
5. Anything executed in another country's scope: their opinion of us, guarantees/diplomatic_relation, add_to_faction, annex/puppet/transfer_state, set_autonomy, cores on their states, civil war, wargoal-driven transfers. Use offer(key) (event, partner decides, no advance reward) - multiplayer rule. MD breaks this in ~10 foci and imposes opinion in 48.
6. Only an event or decision with no own reward on a cost >= 5 focus (MD: 85 event-only + 24 decision-only foci). Pair it with a real bundle or make the focus cost 2-3.
7. Free money: gdp_gain without a political, faction, corruption or tension cost (all 7 MD treasury gains are seizures/repatriations with oligarchs -25 or similar).
8. More than 6 dyn/prog lines in one focus or more than two modifiers touched (MD median 2 lines, 1 modifier; max 10 lines once).
9. Player party-popularity swings above +-0.10 (MD uses +-0.75 only inside is_ai = yes).
10. Stability above +0.06 or PP above 150 in a normal focus (MD outliers 0.16 / 0.30 and 250 exist only on capstones).
11. Tech bonus above 1.0 or more than 3 uses; more than two tech categories per focus.
12. Cost 7 foci that give no more than a cost-3 focus (MD has many, e.g. 'Destroy Revanchist Thoughts' at cost 7: stability factor +1 % against three cost lines). Use the reward-point budget.
13. Opinion/BoP/tension-only foci: these are directional, not rewards; they ride along with a real bundle.
14. Swapping an idea without checking it is present (always compile through idea(swap=...) which falls back to add_ideas).

### 5.6 Where the current design (`/home/claude/sov`, 836 foci) differs from these norms

| Point | Design now | Norm |
|---|---|---|
| Note-only foci | 90 cost-3 "question" foci (mutually exclusive hubs) have only a note → tooltip-only focus | give each a 2-3-point reward: pp 25-50, one dyn line, or a timed idea |
| Cost distribution | 585 of 836 foci (70 %) cost 5 with median 2 effects and 2 kinds; MD's cost 5 median is 3-3.5 lines | cost 5 needs 5-6 points, i.e. one more line or a paid building |
| PP | in 4 % of foci (median 50) vs 9 % in MD (median 100) | PP is a cheap way to give hubs and entry foci a reward |
| Building prices | 0.6-1.5 % per building, always paid | consistent; keep |
| Faction values | +5 / -10 | same as MD |
| BoP | 0.05 per focus | good for the tree size |
| Tech | 0.5 ×1 | same as MD |
