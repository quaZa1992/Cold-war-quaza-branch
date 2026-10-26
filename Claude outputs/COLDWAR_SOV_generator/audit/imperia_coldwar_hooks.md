# Imperia / Cold War hooks for the Soviet 1970 tree (COLDWAR_SOV)

Audit 16.10.2026. Sources: staged mod files under `mdcoldwar/` (MD 2.0.2, HOI4 1.19), project docs `mdcw_cold_war_system_as_built.md`, `mdcw_coding_playbook.md`, `mdcw_1970_generic_focus_tree.md`, the generated tree `COLDWAR_SOV_1970_focus.txt` (836 foci) and `cw_effects.py`. Machine-readable twin: `imperia_coldwar_hooks.json`.

Rules applied: no focus forces war, alliance, bases, territory or a bloc on another country (offers only); oil stays a player system (no AI automatism); every gain has a price; no parallel systems.

## 1. Hook catalogue

| Hook | System | What it does | Scope | Guards / notes | Player-only | Sample |
| --- | --- | --- | --- | --- | --- | --- |
| `mdcw_cw_add_tension` | Cold War | Changes Cold War Tension (0-100, start 45, monthly drift to 40 + 0.1 per inter-bloc sanction, max +8). Tension drives Market Confidence (100 - 0.7 x tension ...), Arms Demand (0.8 x tension ...), the political-climate tiers (Brink 80/Confrontation 60/Elevated 40/Detente 20/Calm) and the Imperia oil risk premium (+0.3 model $ per point above 50). | any (writes globals); call inside completion_reward | Clamped 0-100 by the effect. Optional has_global_flag = mdcw_cw_initialized. Use the effect, never add_to_variable on global.mdcw_cw_tension (the generic tree's GEN_1970_change_tension does that and skips the tier/display/GUI update). | no | common/scripted_effects/mdcw_cold_war_effects.txt:13; COLDWAR_SOV_we_join_the_free_world |
| `cw_world_state_read` | Cold War | Read-only world state for available/bypass/ai_will_do/scaling: tension, Market Confidence, Arms Demand, tiers, bloc shares and scales, bloc member counts, oil price level and ratio, CPI. | any | Read-only. Values exist only after mdcw_cw_initialize (1970 game). | no | common/scripted_effects/mdcw_cold_war_effects.txt:4002 (update_world_situation); COLDWAR_SOV_the_end_of_detente (tension > 59) |
| `mdcw_cw_change_alignment` | Cold War | Moves the country to another bloc (0 Non-Aligned, 1 West, 2 Soviet, 3 Beijing). Charges 15 PP per bloc point (max 150; half to NA) and sets a 730-day lock unless mdcw_cw_t_free = 1. Leaving a bloc: 180 days mdcw_cw_diplomatic_realignment, opinion malus from the old leader, event mdcw_cw.3; tension + bloc_value x 0.2 (x0.1 from NA, x0.05 to NA). ALL subjects of the country follow their overlord. | country (the aligning country) | Guard with mdcw_cw_can_join_<west\|soviet\|beijing\|na> (ruling-party fit + lock). Team pattern for foci: mdcw_cw_t_free = 1 (EGY, SOV). MP: subjects (incl. human Warsaw Pact members under autonomy_warsaw) are moved too. For SOV leaving bloc 2 the effect gives SOV an opinion modifier towards itself and fires mdcw_cw.3 to SOV. | no | common/scripted_effects/mdcw_cold_war_effects.txt:3626; COLDWAR_EGY_1970_focus.txt:2323-2326 |
| `mdcw_cw_bloc_triggers` | Cold War | Scripted triggers (file common/scripted_triggers/mdcw_cold_war_triggers.txt, not staged; names from the generator index): mdcw_cw_can_join_west/_soviet/_beijing/_na, mdcw_cw_can_change_alignment, mdcw_cw_party_fits_west/_soviet/_beijing, mdcw_cw_party_core_*, mdcw_cw_fits_own_bloc, mdcw_cw_is_bloc_leader, mdcw_cw_is_active, mdcw_cw_same_bloc_as_prev, mdcw_cw_opposing_to_prev, mdcw_cw_has_link_with_prev, mdcw_cw_can_embargo_prev, mdcw_cw_is_opec_member, mdcw_cw_is_major_oil_exporter, mdcw_cw_is_oil_exporter. | country (PREV = other country for *_prev triggers) | Bloc leaders and subjects always fit their bloc (never estranged). | no | common/decisions/mdcw_cold_war_decisions.txt:258 (mdcw_cw_is_bloc_leader) |
| `mdcw_cw_assistance_capacity` | Cold War | Custom modifier (number). Adds programme capacity on top of the power-rank base (superpower 8) and the bloc-leader tier bonus (0-3). Read by mdcw_cw_recalculate_capacity via modifier@. | country modifier | Call mdcw_cw_recalculate_country after a change (the national ideas do this in on_add), otherwise the Programmes tab stays stale until the monthly tick. | no | common/ideas/mdcw_cold_war_national_ideas.txt (mdcw_ni_development_agency: +4); COLDWAR_SOV_economic_aid_programmes (+2) |
| `mdcw_cw_support_effectiveness` | Cold War | Custom modifier (%). Multiplies the popularity our Public Political Support campaigns (50 PP diplomatic action) give abroad (sponsor side). | country modifier (sponsor) | Per-receiver cap 0.002 popularity/month still applies. | no | mdcw_ni_broadcasting +0.25; generic GEN_1970_export_our_model +0.15 |
| `mdcw_cw_ideological_defence` | Cold War | Custom modifier (%). Reduces the popularity foreign Public Political Support campaigns give inside our country (1 - value, clamped 0-1). | country modifier (receiver) | Not listed in the as-built doc but defined in mdcw_cold_war_modifiers.txt. | no | mdcw_ni_loyalty_boards +0.3; COLDWAR_SOV_the_fifth_directorate +0.1 |
| `mdcw_cw_military_programme_cost` | Cold War | Custom modifier (%). Cost factor of our military assistance programmes (Military Training Mission, Arms Production Assistance). | country modifier (donor) | Clamped at 0 (cannot go negative). Recalc as for capacity. | no | mdcw_ni_military_advisers -0.25 |
| `mdcw_cw_assistance_limit` | Cold War | Custom modifier (%). Raises the per-effect caps of incoming programmes (receiver). | country modifier (receiver) | Only useful for countries that receive programmes (not the USSR). | no | mdcw_ni_open_door_aid +0.5; generic GEN_1970_balancing_act +0.25 |
| `mdcw_cw_assistance_effectiveness` | Cold War | Custom modifier (%). Incoming programme effect (receiver). | country modifier (receiver) | Receiver side; incoming effects also scale with Imperia development (Developing x1.25, Developed x0.6) and great-power competition (x1.1). | no | mdcw_ni_open_door_aid +0.25 |
| `mdcw_cw_market_exposure` | Cold War | Custom modifier (%), negative colour. Multiplies the Cold War world-market effects (exposure = globalism_value/50, x (1 + this), clamp 2.5). A typical 'price' for opening foci. | country modifier | Call mdcw_cw_update_world_market after a change. | no | mdcw_ni_export_led +0.25; generic GEN_1970_western_capital +0.1 |
| `mdcw_cw_programmes_and_pps` | Cold War | Player diplomatic actions on the target: Assistance Programme (25 PP; 8 types: Construction Assistance, Technical Mission, Industrial Equipment Program, Productivity Mission, Consumer Supply Credits, Military Training Mission, Arms Production Assistance, Administrative Assistance; sizes 1-3) and Public Political Support (50 PP). The receiver accepts or declines. | sender scope with PREV = target (internal effects) | Never call mdcw_cw_start_program_N / mdcw_cw_start_pps from a focus (bypasses the receiver's consent and capacity checks). | yes | common/scripted_effects/mdcw_cold_war_effects.txt:3225, 3476 |
| `mdcw_cw_bloc_leader_decisions` | Cold War | Player-only decisions (is_ai = no): mdcw_cw_dec_comecon (SOV leader, 75 PP, every 1095 d; 730 d: members efficiency growth +5 %, oil price resistance +10 %; SOV upkeep x1.5, oil export income -5 %), mdcw_cw_dec_detente (any bloc leader, 75 PP/365 d, tension -3, pairs within 90 d), mdcw_cw_dec_show_of_strength (any bloc leader, 50 PP/180 d, tension +3). Soviet Credits are for members only (not SOV). | country | Generated file; do not patch by hand (the SOV generator currently ships a patched copy for the Comprehensive Programme refund). | yes | common/decisions/mdcw_cold_war_decisions.txt:46 (comecon) |
| `mdcw_cw_detente_initiative` | Cold War | Effect behind the Detente decision: pairs with another bloc leader's initiative of the last 90 days (both get mdcw_cw_detente_agreement 365 d, tension -5, news to humans) or opens a 90-day offer flag. An offer, so MP-safe. | country (a bloc leader) | Guard: mdcw_cw_is_bloc_leader = yes and is_ai = no (the AI never takes CW decisions). Does not include the decision's own -3 tension. | yes | common/scripted_effects/mdcw_cold_war_effects.txt:4626 |
| `mdcw_cw_ideas` | Cold War | CW timed ideas that can be reused as rewards/prices: mdcw_cw_show_of_strength (war support +5 %, army XP +5 %), mdcw_cw_detente_hawks (war support -5 %), mdcw_cw_detente_agreement, mdcw_cw_diplomatic_realignment (automatic on leaving a bloc). Member-only: mdcw_cw_soviet_advisers, mdcw_cw_imf_conditions, mdcw_cw_self_reliance, mdcw_cw_nam_summit, mdcw_cw_competing_offers. | country | Ideas file not staged; names from decisions/loc. | no | common/decisions/mdcw_cold_war_decisions.txt:291 |
| `mdcw_cw_national_ideas` | Cold War | Ten CW national ideas in Imperia's pools (150 PP, 1440-day lock flag_ni_mdcw_*, on_add recalculates CW). For the USSR in 1970: available = Broadcasting (AI takes it as bloc leader), Border Regime (communist; AI takes it in the Soviet bloc), Development Agency, Open Door, Import Substitution, Export-Led, Military Advisers; not available: Loyalty Boards (needs a West-fitting party), Armed Neutrality (Non-Aligned only), Strategic Petroleum Reserve if SOV is an oil exporter. Oil Price Indexation from the as-built doc no longer exists. | country | AI weights live in the ideas themselves; a focus should discount, not grant (slot behaviour of add_ideas in a law category with 2 slots is unverified). | no | common/ideas/mdcw_cold_war_national_ideas.txt |
| `mdcw_cw_oil_system` | Cold War (oil) | OPEC price level global.mdcw_cw_oil_level (0.5-12) over the Imperia market; real ratio global.mdcw_cw_oil_ratio; CPI global.mdcw_cw_cpi. Player tools: OPEC ballots (mdcw_cw_dec_oil_price_agreement / _price_cut / _output_restraint; OPEC members, humans vote, AI abstains) and bilateral oil embargo / exemption diplomatic actions (MDCW_CW_OIL_EMBARGO_IMPOSE/LIFT, MDCW_CW_OIL_EXEMPTION_GRANT/REVOKE). Crisis tiers per country (mdcw_cw_oil_crisis_tier). The as-built 'Use the Oil Weapon' decision and 'Oil Price Indexation' were replaced by this. | global / country | Player-only by design (Vorgabe Enes): no AI automatism may move the oil price. | yes | common/decisions/mdcw_cold_war_decisions.txt:303; mdcw_cold_war_effects.txt:1488, 1631, 1781 |
| `mdcw_cw_sanction_hooks` | Cold War | mdcw_cw_on_sanction_imposed / _lifted: called by the 8 Imperia sanction diplomatic actions (temp mdcw_cw_t_sanc_type 1-4); inter-bloc sanctions raise tension; bloc leaders' sanctions call bloc embargoes. | target scope, ROOT = sanctioning country | Internal. | yes | common/scripted_effects/mdcw_cold_war_effects.txt:4301 |
| `IMP_is_1970_scenario` | Imperia | Scenario trigger (has_start_date). Country scope; in scope-less on_startup use USA = { IMP_is_1970_scenario = yes }. | country | Every 1970 mechanic is gated by tag + scenario. | no | common/on_actions/mdcw_cold_war_on_actions.txt:14 |
| `imp_national_ideas_pools` | Imperia | Government-screen pools imp_national_ideas_1 'Our Society' / _2 'Our Economy' / _3 'Our Military' (law = yes, 2 slots each per playbook, 150 PP, removal 150, 1440-day lock flag_ni_<n>, Imperia ideas have ai_will_do factor = -10). Many fit the USSR 1970: Patriotic Education, Mandatory Youth Service, Censorship Bureaus, Mass Surveillance, Natality Campaigns (1); National Labour Mobilization, Urbanization Efforts, Worker Co-operatives, Resource Extraction Mandate, Innovation Ecosystem (2); Military Parades, Civil Militia, Army Reserve Mobilization, Civil Defence Drills, Maritime Industry Hub, Nationalized Steel, Special Forces Prioritization, Military Logistics Reform (3). | country | Discount yes (cost factor). Unlock no (would need edits in Imperia files). Grant via add_ideas only after testing the slot behaviour; on_add sets the lock flag. | no | common/ideas/mdcw_imperia_national_ideas_1.txt:5 (imp_ni_3) |
| `imp_oil_market` | Imperia | Imperia oil market: global.imp_global_oil_price (model $, 75 = normal, clamp 15-200), equilibrium (30-135, set by exporters' asking-price ideas imp_oil_prices_ask_1..11 x export share x world dependency + CW premium), weekly 7.5 % adjustment; exporter ideas imp_major_oil_exporter (top 3) / imp_minor_oil_exporter (next 12) by net exports; wars/civil wars at exporters spike +22.5/+11.25. Player decisions d_imp_raise_oil_price / d_imp_lower_oil_price (is_ai = no, need interest group fossil_fuel_industry). Displays: global.imp_oil_price_display (dollars of the day). | global / country | AI exporters never get asking-price ideas (decisions invisible), so their exports do not push the price. Adding oil resources only changes the exporter ranking. | yes | common/scripted_effects/imp_oil_prices_scripted_effects.txt:134; common/decisions/imp_oil_price_decisions.txt |
| `imp_oil_price_resistance` | Imperia | Custom modifier. Lowers imp_oil_dependency (base 0.4 + 0.3 x fossil power share + 0.3 x non-electric fuel use, min 0.2), which scales every high/low-price effect (investment duration, tax, social cost, productivity, consumer goods) and the CW oil crisis tiers. non_electric_fuel_consumption_modifier and nuclear/renewable power work on the same formula. | country modifier | No guard needed. | no | common/ideas/mdcw_imperia_national_ideas_1.txt:582 (Free Public Transport) |
| `imp_trade_policy_oil_spike` | Imperia | imp_set_trade_policy: when a major/minor oil exporter changes its trade law, the oil price spikes +-0.10..0.40 x 75 (720-day cooldown). No caller in the staged files (trade laws call only ingame_update_setup). | country | Watch item. | yes | common/scripted_effects/imp_oil_prices_scripted_effects.txt:978 |
| `imp_sanctions` | Imperia | Four sanction kinds with arrays imp_<dip\|fin\|eco\|mil>_sanc_on_us / _by_us (country scopes), strengths imp_*_sanction_strength (GDP share, offices, factories), effects imp_*_sanctions_p through dynamic modifiers imp_sanctions_<kind>_dynamic_modifier. Modifiers imp_sanction_resistance (receiver) and imp_sanction_effectiveness (sender). Imposing/lifting only through Imperia's diplomatic actions (which carry the CW hook). Player decisions: d_imp_check_sanctions_on/_by (reports), d_imp_consolidate_power (corruption +1, +300 PP when a sanction kind > 10 %). | country | Never write the arrays from a focus (bypasses strengths and the CW hook). Globalism also sets resistance (80 % at 0) and effectiveness (-80 % at 0). | no | common/scripted_effects/imp_sanctions_effects.txt:113; generic GEN_1970_self_reliance (imp_sanction_resistance = 0.1) |
| `imp_military_industrial_complex` | Imperia + Cold War | IMP_military_industrial_complex_dynamic_modifier for countries with the interest group idea defense_industry: extra military-industry tax = 0.4 % x (Arms Demand - 25) (clamp -10 %..+30 %) + 0.5 % per country at war (max 10 %), total -10 %..+40 %. Recalculated monthly. AI countries get IMP_cold_war_ai_war_declaration_lock. | country | SOV has defense_industry from COLDWAR_SOV_initialize_1970, so the MIC is active. The as-built doc still says 2 % per point; the code uses 0.4 %. | no | common/scripted_effects/IMP_cold_war_military_industrial_complex_effects.txt:46 |
| `imp_globalism` | Imperia | globalism_value 0-100 drifts (0.2 x (1 + globalism_rate_multiplier) per tick) towards modifier@globalism_equilibrium. Trade laws set -40 (closed) / +25 / +50 / +70 (mixed) / +50 / +35; blocs: West +5, Soviet -10, Beijing -15. Effects (imp_globalism_modifier): war support +20 %..-20 %, sanction resistance 80 %..0, sanction effectiveness -80 %..0, productivity growth -1..+1, ROI -2..+2 %, interest +2.5 below 50, investment duration +50 %..0. CW market exposure = globalism/50. | country modifier | SOV starts at equilibrium about -50 (closed economy + Soviet bloc) = globalism 0; +5 changes nothing until the trade law opens. Changing globalism_value directly is a bypass - don't. | no | common/scripted_effects/mdcw_imperia_globalism_effects.txt:1; COLDWAR_EGY_1970_focus.txt:2258 |
| `imp_development` | Imperia | Development tiers imp_eco_1/2/3_dynamic_modifier (Developed/Emerging/Developing) from overall_productivity (IMP_developed/emerging_productivity_level triggers, not staged); news events imp_economy.1/2 on promotion. Effects on interest, corruption cost, upgrade cost, pop growth, workforce; visibility of many Imperia national ideas; incoming CW programme effect x1.25 (Developing) / x0.6 (Developed). SOV 1970: productivity 385.4. | country | Read-only; never add/remove these modifiers from a focus. | no | common/scripted_effects/mdcw_imperia_development_effects.txt:1 |
| `imp_debt` | Imperia / MD | MD debt via debt_change + modify_debt_effect; Imperia debt events fire by debt level (imp_eco_debt_high/_very_high/_low -> imp_economy.3-8) and bond events imp_economy.9-12 (Moody's, capital flight) after foreign bond sell-offs. | country | Use the MD helper; Imperia reacts automatically. | no | common/scripted_effects/mdcw_cold_war_effects.txt:4614 (mdcw_cw_take_loan) |
| `imp_gdp_balance` | Imperia | Startup calibration only: IMP_1970_apply_starting_gdp_profile, IMP_1970_restore_state_productivity_profile, mdcw_imperia_apply_own_gdp_curves, employment fractions. Variables gdp_total, gdp_per_capita, overall_productivity are readable. | country | Not for foci (would distort the calibration). | no | common/scripted_effects/mdcw_imperia_gdp_balance_effects.txt:60 |
| `imp_infrastructure_costs` | Imperia | update_infrastructure_rate: weekly upkeep per building level - roads 0.005, air base 0.005, radar 0.007, anti-air 0.007, fuel silo 0.002, civilian shelter 0.008 (0.02 damaged), rocket site 0.001, stronghold network 0.05 - times (1 + infra_cost_multiplier_modifier). Every infrastructure/air base/AA/fuel focus therefore has a built-in running price. | country modifier / automatic | Note: the GDP scaling temp gdp_infra_cost_modifier is computed but never applied in the staged version. | no | common/scripted_effects/mdcw_imperia_infrastructure_effects.txt:5 |
| `imp_nuclear` | Imperia | Strike consequences only: imp_tac_nuke_effects / imp_big_nuke_effects (state scope: contamination/devastation, casualties reduced by civilian_shelter 10 %/8 % per level, permanent building loss, news imp_nukes.1-4, global flags imp_first_tact_used / imp_first_nuke_used, global.total_nukes_explodes). No warhead-stockpile or test system in the staged files; MD law nuclear_status (nuclear_power_def/_off need reactor1 + sp_nuclear_warhead_program). | state / global | The staged SOV 1970 snapshot sets neither nuclear_status nor sp_nuclear_warhead_program (only the 2000 block does) - verify in game. | no | common/scripted_effects/mdcw_imperia_nuclear_effects.txt:82 |
| `imp_refugees` | Imperia | War refugees flow automatically to attractive neighbours (score from GDP, GDP/capita, imp_refugee_pull_modifier); costs via imp_refugees_dynamic_modifier, integration via imp_refugee_integration_rate; idea imp_refugee_block_costs; events imp_refugee_event.1-4. | country modifier | Mostly irrelevant for a closed USSR; CW Border Regime clamps immigration on adoption. | no | common/scripted_effects/imp_refugees_effects.txt:165 |
| `imp_corruption_events` | Imperia | corruption_event_1/2/3: random Imperia scandal events imp_corruption.1-12 (event_1 at corruption level 1-2 with 60 % nothing; event_2 at levels 1-5 with 40 % nothing; event_3 below level 8). MD helpers increase_corruption / decrease_corruption step the corruption_level_01..10 law. | country | Use as a hidden 'price' of foci that tolerate graft. | no | common/scripted_effects/imp_corruption_events_scripted_effects.txt:33 |
| `imp_minis` | Imperia | imp_set_investment_caps (outgoing/incoming investment slots by GDP + modifiers imp_investment_out_extra / imp_investment_in_extra), imp_calc_casualty_cost (imp_casualties_dynamic_modifier 'The Price of War', automatic in wars), diplomatic insult and volunteer actions. | country modifier | Investments themselves stay player actions. | no | common/scripted_effects/imp_minis_effects.txt:5 |
| `imp_money_transfer` | Imperia | Player diplomatic actions Transfer Funds, Grant Subsidies (weekly), Purchase/Buyback Bonds; variables active_subsidies@TAG, given_bonds@TAG; helpers calculate_subsidies_in/_out, calculate_bond_size, calculate_new_bonds_held/_owed. | country | Do not write given_bonds/active_subsidies from a focus. | yes | common/scripted_effects/imp_money_transfer_scripted_effects.txt:5 |
| `mdcw_infantry_research` | Cold War | mdcw_apply_1970_infantry_research (file common/scripted_effects/mdcw_1970_infantry_research_effects.txt, NOT staged) sets the 1940-1985 infantry/research profile with protection bonuses 25/75; called in the SOV history before the tree. | country | Not verifiable here. | no | history/countries/SOV - Russia.txt:8 |
| `mdcw_industry_1960s_70s_techs` | Cold War | Historical industry techs (from mdcw_industry_60s_70s_l_english.yml and mdcw_historical_industry_l_english.yml; tech files not staged): Carbon Fibre I/II (mdcw_pan_carbon_fibers_1961, mdcw_graphitic_fibers_1970: factory/dockyard output +3 %, efficiency cap +2.5 %), CAD / Solid Modelling (mdcw_computer_aided_drafting_1963, mdcw_solid_modelling_1975), Genetic Code / Gene Cloning / Sequencing (mdcw_genetic_code_1966, mdcw_recombinant_dna_1973, mdcw_dna_sequencing_1977), construction (mdcw_precast_construction_1960, mdcw_site_planning_1970, mdcw_resource_loaded_construction_1975, mdcw_preventive_industrial_maintenance_1975), machine tools (mdcw_numerical_control_1955, mdcw_industrial_robotics_1961, mdcw_factory_control_1970, mdcw_computer_controlled_machine_tools_1975, mdcw_flexible_manufacturing_1980), power (mdcw_regional_grid_1955, mdcw_grid_dispatch_1965, mdcw_grid_stability_1975, mdcw_supercritical_steam_1957, mdcw_large_hydro_turbines_1965, mdcw_combined_cycle_generation_1967). | country | Folders MDCW_EARLY_MATERIALS / _GENETICS / _POWER. Verify IDs and categories against the tech files. | no | localisation/english/mdcw_industry_60s_70s_l_english.yml |

### Call patterns

**mdcw_cw_add_tension**
```
set_temp_variable = { mdcw_cw_tension_delta = -3 }
mdcw_cw_add_tension = yes
```
**cw_world_state_read**
```
check_variable = { global.mdcw_cw_tension > 59 }
check_variable = { global.mdcw_cw_market < 40 }
check_variable = { global.mdcw_cw_arms > 60 }
check_variable = { global.mdcw_cw_share_2 > 0.299 }   # Soviet bloc >= 30 % of world power (Global tier)
check_variable = { global.mdcw_cw_oil_ratio > 2 }
```
**mdcw_cw_change_alignment**
```
if = { limit = { mdcw_cw_can_join_west = yes }
	set_temp_variable = { mdcw_cw_new_alignment = 1 }
	set_temp_variable = { mdcw_cw_t_free = 1 }
	mdcw_cw_change_alignment = yes
}
```
**mdcw_cw_bloc_triggers**
```
available = { mdcw_cw_is_bloc_leader = yes }
limit = { mdcw_cw_can_join_na = yes }
```
**mdcw_cw_assistance_capacity**
```
mdcw_cw_assistance_capacity = 1   # in an idea / dynamic modifier
hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_recalculate_country = yes } }
```
**mdcw_cw_support_effectiveness**
```
mdcw_cw_support_effectiveness = 0.1
```
**mdcw_cw_ideological_defence**
```
mdcw_cw_ideological_defence = 0.05
```
**mdcw_cw_military_programme_cost**
```
mdcw_cw_military_programme_cost = -0.1
```
**mdcw_cw_assistance_limit**
```
mdcw_cw_assistance_limit = 0.25
```
**mdcw_cw_assistance_effectiveness**
```
mdcw_cw_assistance_effectiveness = 0.15
```
**mdcw_cw_market_exposure**
```
mdcw_cw_market_exposure = 0.1
hidden_effect = { mdcw_cw_update_world_market = yes }
```
**mdcw_cw_programmes_and_pps**
```
# not callable from a focus: start via the diplomacy screen. Foci change capacity/cost/effectiveness modifiers only.
```
**mdcw_cw_bloc_leader_decisions**
```
set_variable = { mdcw_cw_refund_comecon = 25 }   # proposed CW-generator hook, see proposals
```
**mdcw_cw_detente_initiative**
```
if = {
	limit = { is_ai = no has_country_flag = mdcw_cw_initialized mdcw_cw_is_bloc_leader = yes }
	custom_effect_tooltip = COLDWAR_SOV_detente_offer_tt   # "We open a Detente initiative: if another bloc leader takes 'Detente Initiative' within 90 days, both get Detente and tension falls by 5."
	hidden_effect = { mdcw_cw_detente_initiative = yes }
	add_timed_idea = { idea = mdcw_cw_detente_hawks days = 180 }
}
```
**mdcw_cw_ideas**
```
add_timed_idea = { idea = mdcw_cw_show_of_strength days = 180 }
```
**mdcw_cw_national_ideas**
```
add_timed_idea = { idea = COLDWAR_SOV_ni_window_society days = 365 }   # imp_national_ideas_1_cost_factor = -0.5
```
**mdcw_cw_oil_system**
```
# allowed in a focus: read globals, change own oil_export_multiplier_modifier, imp_oil_price_resistance, add_resource oil
# forbidden in a focus: mdcw_cw_start_opec_vote, mdcw_cw_start_oil_embargo, mdcw_cw_end_oil_embargo, set/multiply global.mdcw_cw_oil_level, imp_spike_oil_price, imp_oil_price_demand_raise/_lower, add_ideas = imp_oil_prices_ask_N
```
**mdcw_cw_sanction_hooks**
```
# not for foci
```
**IMP_is_1970_scenario**
```
IMP_is_1970_scenario = yes
```
**imp_national_ideas_pools**
```
imp_national_ideas_2_cost_factor = -0.5   # engine '<idea category>_cost_factor' pattern (MD uses trade_laws_cost_factor, social_budget_cost_factor ...); first use for these categories -> verify in game and whitelist in validate_sov
```
**imp_oil_market**
```
custom_effect_tooltip = COLDWAR_SOV_oil_price_now_tt   # "Oil: $[?global.imp_oil_price_display|.2] per barrel"
```
**imp_oil_price_resistance**
```
imp_oil_price_resistance = 0.05
non_electric_fuel_consumption_modifier = -0.05
```
**imp_trade_policy_oil_spike**
```
# if this gets wired to trade-law on_add, AI-taken trade-law foci would move the oil price -> guard with is_ai = no
```
**imp_sanctions**
```
any_of_scopes = { array = imp_eco_sanc_on_us tag = USA }   # read-only trigger
imp_sanction_resistance = 0.05   # modifier
```
**imp_military_industrial_complex**
```
check_variable = { global.mdcw_cw_arms > 60 }
if = { limit = { has_idea = defense_industry } remove_ideas = defense_industry hidden_effect = { IMP_cold_war_update_military_industrial_complex_country = yes } }
```
**imp_globalism**
```
globalism_equilibrium = 5   # in a COLDWAR_SOV dynamic modifier (EGY pattern: COLDWAR_EGY_economy_globalism_equilibrium)
```
**imp_development**
```
has_dynamic_modifier = { modifier = imp_eco_1_dynamic_modifier }   # read-only
```
**imp_debt**
```
set_temp_variable = { debt_change = 5 }
modify_debt_effect = yes
```
**imp_gdp_balance**
```
check_variable = { gdp_per_capita > 2 }   # read-only
```
**imp_infrastructure_costs**
```
infra_cost_multiplier_modifier = -0.05
```
**imp_nuclear**
```
capital_scope = { add_building_construction = { type = civilian_shelter level = 2 instant_build = yes } }
has_global_flag = imp_first_nuke_used   # read-only
```
**imp_refugees**
```
imp_refugee_pull_modifier = -0.1
```
**imp_corruption_events**
```
hidden_effect = { corruption_event_2 = yes }
```
**imp_minis**
```
imp_investment_in_extra = 1
```
**imp_money_transfer**
```
# not for foci; the SOV offers use COLDWAR_SOV_transfer_gdp_share (accepted by the partner) - keep it one-off
```
**mdcw_infantry_research**
```
# foci: add_tech_bonus on CAT_small_arms etc. only; never set_technology infantry techs
```
**mdcw_industry_1960s_70s_techs**
```
add_tech_bonus = { name = COLDWAR_SOV_x bonus = 0.5 uses = 1 technology = mdcw_factory_control_1970 }
```

## 2. Already used in COLDWAR_SOV

| Hook | Usage in the generated tree |
| --- | --- |
| mdcw_cw_add_tension | 52 calls / 52 foci (sum +66, -44; largest: strike_at_dawn +10, cnr_the_revanche +5, the_surgical_strike_option +5, chr_disarmament -5) |
| global.mdcw_cw_tension (read) | 2 foci: ple_gre (available > 54), the_end_of_detente (available > 59); decisions and events too |
| mdcw_cw_change_alignment (+ mdcw_cw_t_free = 1) | 4 foci: we_join_the_free_world, nts_into_the_west, chr_join_the_free_world, na_join_the_movement |
| mdcw_cw_can_join_west | 3 foci (the same three West foci); na_join_the_movement checks the raw variable |
| global.mdcw_cw_oil_level (read) | 1 focus: petrodollars (available) |
| mdcw_cw_support_effectiveness | 12 foci via COLDWAR_SOV_commonwealth/_sus_programme + start value 0.1 + 1 idea |
| mdcw_cw_ideological_defence | 9 foci via party_state/cpsu/bre/sus/and/kv programmes + 1 idea |
| mdcw_cw_military_programme_cost | 3 foci: sus_the_liberation_movements, gre_arms_for_allies, military_advisers |
| mdcw_cw_assistance_capacity | 2 foci: the_commonwealth_of_socialist_nations (+1), economic_aid_programmes (+2) |
| Comecon Integration Programme (mdcw_cw_dec_comecon) | 1 focus: the_comprehensive_programme (flag + hand-patched copy of the generated decision file: 25 PP refund) |
| imp_sanction_resistance | 1 focus: ns_the_closed_economy (+0.1) |
| MD trade law -> Imperia globalism | 6 foci: mixed_economy (we_the_market_returns, nts_free_market_russia, chr_the_convergence_economy, smc_the_mixed_economy), md_closed_economy (ns_the_closed_economy, cnr_fortress_russia) |
| oil_export_multiplier_modifier (Imperia oil income) | 7 foci: bre_the_oil_bet, gt_the_resource_state, samotlor, urengoy, aliyev_in_baku, subsidised_oil, world_market_prices; + start -0.1 |
| add_resource oil (Imperia exporter ranking) | 2 foci: samotlor (+10), the_tyumen_complex (+8) |
| international_market_income / military_industry_tax (arms market, MIC) | 3 + 4 foci; defense_industry interest group from init keeps the Imperia MIC active; 22 foci move its opinion |
| MD debt (Imperia debt events) | 4 foci via COLDWAR_SOV_change_debt_gdp_share |
| MD corruption helpers | 23 calls in 21 foci (Imperia corruption_event_* not used) |
| IMP_is_1970_scenario | tree weight + 12 enables in ideas/dynamic modifiers |
| Buildings with Imperia upkeep | ~19 foci (roads, air bases, AA, fuel silo) - price is automatic but not shown |

Oil rule check: no call of `imp_spike_oil_price`, `imp_oil_price_demand_*`, `mdcw_cw_start_opec_vote`, `mdcw_cw_start_oil_embargo`, no write to `global.mdcw_cw_oil_level`, no `imp_oil_prices_ask_*` idea in focus, idea, decision, event or effect files of the tree. Compliant.

DSL kinds in `cw_effects.compile_effect`: pp, stab, ws, fac, party, outlook, dyn, prog, idea, rmidea, coh, tech, bop, build, tension, offer, op, rp, gdp, gdp_gain, debt, corr, heir, decision, event, space, sp, xp, cp, mastery, manpower, infl, elections, setlaw, law, cwjoin, trait, leader, flag, note/custom/gensec. Only `tension` and `cwjoin` touch CW effects; CW/Imperia modifiers enter through `dyn`/`prog` keys.

## 3. Missing

| Hook | State |
| --- | --- |
| mdcw_cw_detente_initiative / CW ideas (show_of_strength, detente_hawks) | not used; Detente foci use only raw tension |
| Bloc leader decisions (Detente, Show of Strength) | no link; Comecon via a patch that the CW generator will overwrite |
| mdcw_cw_market_exposure, mdcw_cw_assistance_limit/_effectiveness | not used (receiver modifiers irrelevant for SOV; market exposure is the natural price of opening) |
| CW recalculation after modifier changes | missing in all 26 foci that change CW modifiers |
| mdcw_cw_can_join_na, mdcw_cw_is_bloc_leader | not used |
| Subject handling on bloc change | missing - human Warsaw Pact partners would be moved |
| Cold War national ideas | no focus discounts/refers to Broadcasting, Border Regime, Development Agency, Military Advisers, Import Substitution, Armed Neutrality |
| Imperia national ideas (3 pools) | not used |
| Imperia globalism (globalism_equilibrium) | only indirectly through trade laws; no tooltip |
| Imperia sanction arrays / imp_sanction_effectiveness | not read/used |
| Imperia oil: fossil_fuel_industry, imp_oil_price_resistance, real price ratio | not used (petrodollars reads the OPEC level only) |
| Imperia investments (imp_investment_in/_out_extra) | not used |
| Imperia infrastructure costs (infra_cost_multiplier_modifier) | not used, upkeep not shown |
| Imperia nuclear (civilian_shelter) | not used; civil defence focus gives only modifiers |
| Imperia corruption events | not used |
| Imperia development tiers | not used (only relevant for read-only scaling) |
| Imperia refugees, money transfer, GDP balance | not used - correctly (no fitting focus / player tools / startup only) |
| 1960s-70s industry techs (mdcw_*) | not targeted; tree uses only category bonuses |

### Open checks and findings

- SOV 1970 snapshot (staged history) sets neither the nuclear_status law nor sp:sp_nuclear_warhead_program (only the 2000 block does). Verify in game; if missing, set it in COLDWAR_SOV_initialize_1970, not in a focus.
- As-built doc v3.3.2 is outdated: 'Use the Oil Weapon' and 'Oil Price Indexation' are gone; OPEC ballots (human-only voting) and bilateral embargo/exemption diplomatic actions replaced them; MIC is 0.4 %/point; modifiers mdcw_cw_ideological_defence and mdcw_cw_assistance_effectiveness and the Great Power Competition spirit exist.
- mdcw_cw_change_alignment with SOV leaving bloc 2: SOV = { add_opinion_modifier = { target = PREV ... } } targets SOV itself and mdcw_cw.3 is sent to SOV; members of the abandoned bloc get no notice. Fix in the CW generator.
- GEN_1970_change_tension (generic tree) writes global.mdcw_cw_tension directly: no tier/display/GUI update until the monthly tick. The SOV tree does it right (mdcw_cw_add_tension).
- imp_set_trade_policy (oil spike on exporters' trade-law change) has no caller in the staged files; if it is wired to trade-law on_add, the 6 trade-law foci need an is_ai = no guard to keep oil player-only.
- update_infrastructure_rate computes gdp_infra_cost_modifier but never applies it (staged version).
- imp_national_ideas_N_cost_factor is the engine's '<category>_cost_factor' pattern (as trade_laws_cost_factor) but has never been used for these categories - test once and whitelist it in validate_sov (modkeys).
- Not staged, so not verified: mdcw_cold_war_triggers.txt (can_join_* logic), mdcw_1970_infantry_research_effects.txt, the CW ideas file, Imperia sanction/money diplomatic actions, tech files for the mdcw_* industry techs.

## 4. Integration proposals per section

Priorities: **P1** correctness/MP (do first), **P2** core integration, **P3** flavour/optional. Codes go into `completion_reward` unless marked. `dsl` (JSON) gives the `dyn` form for the generator. New ideas needed: `COLDWAR_SOV_ni_window_society/_economy/_military` (365 days, `imp_national_ideas_<1|2|3>_cost_factor = -0.5`) and `COLDWAR_SOV_fraternal_oil` (`imp_oil_price_resistance = 0.15`, for partners); new events: Fraternal Oil offer, free-exit offer to bloc members.

Generator-level changes (cover many foci at once):
- `cw_effects.dyn_change`: if a key starts with `mdcw_cw_`, append `hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_recalculate_country = yes } }` (26 foci); for `globalism_equilibrium`/`mdcw_cw_market_exposure` also `mdcw_cw_update_world_market = yes`.
- `cw_effects.cw_join`: subject guard (below) or, better, `is_ai = yes` in the CW generator's 'Subjects follow their overlord' loop; reset `mdcw_cw_t_free = 0` after the call.
- New DSL kinds suggested: `cwdetente` (detente-initiative block), `cwidea` (CW timed idea), `niwindow` (pool discount), `cwrecalc`.
- Remove the patched copy `out/common/decisions/mdcw_cold_war_decisions.txt`; move the refund into the CW generator.

### pol

No proposal. Trunk foci are domestic (Politburo, cohesion, directions). Tension/alignment effects sit in the outlook and foreign sections; no Imperia hook needed.

### em

No proposal. Uses CW support effectiveness already (em_peace_and_socialism); the generator recalc fix covers it.

### we

**COLDWAR_SOV_we_join_the_free_world** (P1; hooks: mdcw_cw_change_alignment, mdcw_cw_bloc_triggers)

Multiplayer rule: mdcw_cw_change_alignment moves every subject with its overlord, so the Warsaw Pact partners (subjects via autonomy_warsaw, possibly human) would be dragged into the West/Non-Aligned by our focus. The guard restores human subjects' own bloc; AI subjects and the SSRs follow. Cleaner long-term fix: add `is_ai = yes` to the 'Subjects follow their overlord' limit in the CW generator (tools/_gen_effects.py) - then this guard can go. Price already built in: leaving bloc 2 gives 180 days Diplomatic Realignment.
```
# replaces the current alignment block
if = { limit = { mdcw_cw_can_join_west = yes }
	# COLDWAR | human partners keep their own bloc (mdcw_cw_change_alignment moves every subject with its overlord)
	every_subject_country = { limit = { is_ai = no has_country_flag = mdcw_cw_initialized } set_variable = { COLDWAR_SOV_keep_alignment = mdcw_cw_alignment } }
	set_temp_variable = { mdcw_cw_new_alignment = 1 }
	set_temp_variable = { mdcw_cw_t_free = 1 }
	mdcw_cw_change_alignment = yes
	set_temp_variable = { mdcw_cw_t_free = 0 }
	every_subject_country = {
		limit = { has_variable = COLDWAR_SOV_keep_alignment }
		set_variable = { mdcw_cw_alignment = COLDWAR_SOV_keep_alignment }
		clear_variable = COLDWAR_SOV_keep_alignment
		mdcw_cw_recalculate_country = yes
	}
	hidden_effect = { mdcw_cw_rebuild_blocs = yes mdcw_cw_refresh_all_bloc_effects = yes }
}
```

**COLDWAR_SOV_we_stop_the_jamming** (P2; hooks: mdcw_cw_ideological_defence)

Ending the jamming of Western radio is exactly what Ideological Defence measures; currently only drift defence falls.
```
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_party_state_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_party_state_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_party_state_modifier }
add_to_variable = { COLDWAR_SOV_party_state_mdcw_cw_ideological_defence = -0.1 tooltip = COLDWAR_SOV_mod_mdcw_cw_ideological_defence_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
```

**COLDWAR_SOV_we_the_market_returns** (P2; hooks: imp_globalism)

The trade-law change is the biggest Imperia effect in the tree (Globalism 0 -> ~60) but invisible in the tooltip. Same tooltip for smc_the_mixed_economy, chr_the_convergence_economy, nts_free_market_russia; the reverse text for ns_the_closed_economy / cnr_fortress_russia.
```
custom_effect_tooltip = COLDWAR_SOV_globalism_opening_tt   # "Mixed Economy raises our Globalism equilibrium by 110 (closed economy -40 -> +70): less war support and sanction resistance, more productivity and return on investment; world-market swings reach us (Cold War market exposure = Globalism / 50)."
```

### na

**COLDWAR_SOV_na_join_the_movement** (P1; hooks: mdcw_cw_change_alignment, mdcw_cw_bloc_triggers)

Multiplayer rule: mdcw_cw_change_alignment moves every subject with its overlord, so the Warsaw Pact partners (subjects via autonomy_warsaw, possibly human) would be dragged into the West/Non-Aligned by our focus. The guard restores human subjects' own bloc; AI subjects and the SSRs follow. Cleaner long-term fix: add `is_ai = yes` to the 'Subjects follow their overlord' limit in the CW generator (tools/_gen_effects.py) - then this guard can go. Also uses the existing mdcw_cw_can_join_na trigger instead of a raw alignment check. Price already built in: leaving bloc 2 gives 180 days Diplomatic Realignment.
```
# replaces the current alignment block
if = { limit = { mdcw_cw_can_join_na = yes }
	# COLDWAR | human partners keep their own bloc (mdcw_cw_change_alignment moves every subject with its overlord)
	every_subject_country = { limit = { is_ai = no has_country_flag = mdcw_cw_initialized } set_variable = { COLDWAR_SOV_keep_alignment = mdcw_cw_alignment } }
	set_temp_variable = { mdcw_cw_new_alignment = 0 }
	set_temp_variable = { mdcw_cw_t_free = 1 }
	mdcw_cw_change_alignment = yes
	set_temp_variable = { mdcw_cw_t_free = 0 }
	every_subject_country = {
		limit = { has_variable = COLDWAR_SOV_keep_alignment }
		set_variable = { mdcw_cw_alignment = COLDWAR_SOV_keep_alignment }
		clear_variable = COLDWAR_SOV_keep_alignment
		mdcw_cw_recalculate_country = yes
	}
	hidden_effect = { mdcw_cw_rebuild_blocs = yes mdcw_cw_refresh_all_bloc_effects = yes }
}
```

### nt

**COLDWAR_SOV_nt_the_victory_cult** (P3; hooks: imp_national_ideas_pools)

Imperia idea imp_ni_27 (war support +10 %; equipment cost +2.5 %) is the Imperia form of the Victory cult.
```
add_timed_idea = { idea = COLDWAR_SOV_ni_window_military days = 365 }   # new idea: imp_national_ideas_3_cost_factor = -0.5
custom_effect_tooltip = COLDWAR_SOV_ni_window_military_parades_tt   # "For a year, adopting §YMilitary Parades§! (Government screen) costs half."
```

### cpsu

No proposal. Ideological defence already used (cpsu_the_party_of_lenin); nothing further.

### ple

No proposal. Plenum gates already read Cold War tension (ple_gre); keep.

### bre

**COLDWAR_SOV_bre_the_oil_bet** (P3; hooks: imp_oil_market)

Same oil-lobby hook on Brezhnev's 'oil bet' path (choose one of the two foci, or both with the NOT has_idea guard).
```
if = { limit = { NOT = { has_idea = fossil_fuel_industry } }
	add_ideas = fossil_fuel_industry
	set_variable = { fossil_fuel_industry_opinion = 60 }
	hidden_effect = { initialize_internal_faction_dynamic_modifiers = yes }
}
custom_effect_tooltip = COLDWAR_SOV_oil_lobby_tt   # "The oil and gas ministries become an interest group. If we are one of Imperia's oil exporters, a player government may set our asking price (Oil Price decisions)."
```

**COLDWAR_SOV_bre_the_dnepropetrovsk_clan** (P3; hooks: imp_corruption_events)

Imperia scandal events as the hidden price of clan politics (40 % nothing, else one of imp_corruption.1-8).
```
hidden_effect = { corruption_event_2 = yes }
```

### kos

**COLDWAR_SOV_kos_joint_ventures** (P2; hooks: imp_minis, imp_sanctions)

Joint ventures = one more incoming investment slot in Imperia's investment caps (imp_set_investment_caps). Price: dependence on Western partners lowers sanction resistance (plus the existing debt).
```
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_gosplan_modifier }
add_to_variable = { COLDWAR_SOV_gosplan_imp_investment_in_extra = 1 tooltip = COLDWAR_SOV_mod_imp_investment_in_extra_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_party_state_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_party_state_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_party_state_modifier }
add_to_variable = { COLDWAR_SOV_party_state_imp_sanction_resistance = -0.05 tooltip = COLDWAR_SOV_mod_imp_sanction_resistance_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
```

**COLDWAR_SOV_kos_the_production_associations** (P3; hooks: mdcw_industry_1960s_70s_techs)

Production associations -> planned maintenance tech.
```
add_tech_bonus = { name = COLDWAR_SOV_kos_the_production_associations_mdcw bonus = 0.5 uses = 1 technology = mdcw_preventive_industrial_maintenance_1975 }   # tech IDs from mdcw_*_l_english.yml; verify the technology files
```

### pod

No proposal. Support effectiveness via pod_the_treaty_signer (recalc fix); no other hook.

### sus

No proposal. Support effectiveness, ideological defence and military programme cost already used; recalc fix only. Optional Broadcasting window if kgb_active_measures is not taken.

### she

**COLDWAR_SOV_she_confront_the_west** (P3; hooks: mdcw_cw_ideas)

Same reuse; avoids a permanent war-support gain for a demonstrative act.
```
# replaces add_war_support = 0.03
add_timed_idea = { idea = mdcw_cw_show_of_strength days = 180 }
```

### and

**COLDWAR_SOV_and_the_technology_gap** (P3; hooks: mdcw_industry_1960s_70s_techs)

Closing the technology gap -> digital design tech.
```
add_tech_bonus = { name = COLDWAR_SOV_and_the_technology_gap_mdcw bonus = 0.5 uses = 1 technology = mdcw_solid_modelling_1975 }   # tech IDs from mdcw_*_l_english.yml; verify the technology files
```

### gre

**COLDWAR_SOV_gre_arms_for_allies** (P1; hooks: mdcw_cw_military_programme_cost)

Military programme cost -10 %: refresh (same generator fix).
```
hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_recalculate_country = yes } }   # also recalculates capacity
```

### ust

**COLDWAR_SOV_ust_arms_not_soldiers** (P3; hooks: cw_world_state_read)

Same Arms Demand read for Ustinov's arms-export choice.
```
# ai_will_do
modifier = { add = 5 check_variable = { global.mdcw_cw_arms > 59 } }
```

### gro

**COLDWAR_SOV_gro_no_concessions** (P3; hooks: imp_sanctions)

Hard line = sanction-proofing through Imperia's own modifier (gain); the existing trade opinion -5 % and tension +2 are the price.
```
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_party_state_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_party_state_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_party_state_modifier }
add_to_variable = { COLDWAR_SOV_party_state_imp_sanction_resistance = 0.05 tooltip = COLDWAR_SOV_mod_imp_sanction_resistance_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
```

**COLDWAR_SOV_gro_automated_plants** (P3; hooks: mdcw_industry_1960s_70s_techs)

Romanov's automation -> our robotics/programmable-control techs.
```
add_tech_bonus = { name = COLDWAR_SOV_gro_automated_plants_mdcw bonus = 0.5 uses = 1 technology = mdcw_industrial_robotics_1961 technology = mdcw_factory_control_1970 }   # tech IDs from mdcw_*_l_english.yml; verify the technology files
```

### che

No proposal. Foreign line uses an offer; optionally the Detente-initiative block like save_detente (choose at most one of save_detente/gor_new_thinking/che_the_peace_offensive per playthrough - they are on different paths).

### gor

**COLDWAR_SOV_gor_new_thinking** (P2; hooks: mdcw_cw_detente_initiative)

Reykjavik/INF climate through the same CW offer; keeps the existing -3 tension.
```
if = {
	limit = { is_ai = no has_country_flag = mdcw_cw_initialized mdcw_cw_is_bloc_leader = yes }
	custom_effect_tooltip = COLDWAR_SOV_detente_offer_tt   # "We open a Detente initiative: if another bloc leader takes 'Detente Initiative' within 90 days, both get Detente and tension falls by 5."
	hidden_effect = { mdcw_cw_detente_initiative = yes }
	add_timed_idea = { idea = mdcw_cw_detente_hawks days = 180 }
}
```

**COLDWAR_SOV_gor_the_sinatra_doctrine** (P2; hooks: mdcw_cw_change_alignment)

Gorbachev path version of the same offer.
```
# same member offer as COLDWAR_SOV_let_them_go_their_way (shared event)
```

### wc

**COLDWAR_SOV_wc_leave_the_arms_race** (P3; hooks: imp_military_industrial_complex)

Same MIC hook for the council-communist path.
```
if = { limit = { has_idea = defense_industry } remove_ideas = defense_industry hidden_effect = { initialize_internal_faction_dynamic_modifiers = yes IMP_cold_war_update_military_industrial_complex_country = yes } }
custom_effect_tooltip = COLDWAR_SOV_mic_dissolved_tt   # "The Military-Industrial Complex loses its seat at the table: no more Export Compulsion tax bonus from Arms Demand."
```

### ns

**COLDWAR_SOV_ns_the_closed_economy** (P2; hooks: mdcw_cw_national_ideas, imp_globalism)

The Stalinist autarky path matches the CW idea Import Substitution (construction +10 %, sanction resistance +10 %; Globalism -10, productivity growth -5 %, consumer goods +2 %). Tooltip: closed economy pins Globalism at 0 (war support +20 %, sanction resistance 80 %, productivity -1, interest +2.5).
```
add_timed_idea = { idea = COLDWAR_SOV_ni_window_economy days = 365 }   # new idea: imp_national_ideas_2_cost_factor = -0.5
custom_effect_tooltip = COLDWAR_SOV_ni_window_import_substitution_tt   # "For a year, adopting §YImport Substitution Industrialisation§! (Government screen) costs half."
custom_effect_tooltip = COLDWAR_SOV_globalism_closing_tt
```

### kv

**COLDWAR_SOV_kv_construction_battalions** (P3; hooks: imp_infrastructure_costs)

Construction battalions maintain the roads they build: Imperia infrastructure upkeep -5 % (gain); the existing labour/stability effects remain the price.
```
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_gosplan_modifier }
add_to_variable = { COLDWAR_SOV_gosplan_infra_cost_multiplier_modifier = -0.05 tooltip = COLDWAR_SOV_mod_infra_cost_multiplier_modifier_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
```

### sd

**COLDWAR_SOV_sd_the_corporate_union** (P3; hooks: imp_minis)

The corporate path already lowers receiving-investment cost; the extra Imperia slot makes it usable. Price already present (debt 1 % GDP).
```
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_gosplan_modifier }
add_to_variable = { COLDWAR_SOV_gosplan_imp_investment_in_extra = 1 tooltip = COLDWAR_SOV_mod_imp_investment_in_extra_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
```

### nts

**COLDWAR_SOV_nts_into_the_west** (P1; hooks: mdcw_cw_change_alignment, mdcw_cw_bloc_triggers)

Multiplayer rule: mdcw_cw_change_alignment moves every subject with its overlord, so the Warsaw Pact partners (subjects via autonomy_warsaw, possibly human) would be dragged into the West/Non-Aligned by our focus. The guard restores human subjects' own bloc; AI subjects and the SSRs follow. Cleaner long-term fix: add `is_ai = yes` to the 'Subjects follow their overlord' limit in the CW generator (tools/_gen_effects.py) - then this guard can go. Price already built in: leaving bloc 2 gives 180 days Diplomatic Realignment.
```
# replaces the current alignment block
if = { limit = { mdcw_cw_can_join_west = yes }
	# COLDWAR | human partners keep their own bloc (mdcw_cw_change_alignment moves every subject with its overlord)
	every_subject_country = { limit = { is_ai = no has_country_flag = mdcw_cw_initialized } set_variable = { COLDWAR_SOV_keep_alignment = mdcw_cw_alignment } }
	set_temp_variable = { mdcw_cw_new_alignment = 1 }
	set_temp_variable = { mdcw_cw_t_free = 1 }
	mdcw_cw_change_alignment = yes
	set_temp_variable = { mdcw_cw_t_free = 0 }
	every_subject_country = {
		limit = { has_variable = COLDWAR_SOV_keep_alignment }
		set_variable = { mdcw_cw_alignment = COLDWAR_SOV_keep_alignment }
		clear_variable = COLDWAR_SOV_keep_alignment
		mdcw_cw_recalculate_country = yes
	}
	hidden_effect = { mdcw_cw_rebuild_blocs = yes mdcw_cw_refresh_all_bloc_effects = yes }
}
```

### chr

**COLDWAR_SOV_chr_join_the_free_world** (P1; hooks: mdcw_cw_change_alignment, mdcw_cw_bloc_triggers)

Multiplayer rule: mdcw_cw_change_alignment moves every subject with its overlord, so the Warsaw Pact partners (subjects via autonomy_warsaw, possibly human) would be dragged into the West/Non-Aligned by our focus. The guard restores human subjects' own bloc; AI subjects and the SSRs follow. Cleaner long-term fix: add `is_ai = yes` to the 'Subjects follow their overlord' limit in the CW generator (tools/_gen_effects.py) - then this guard can go. Price already built in: leaving bloc 2 gives 180 days Diplomatic Realignment.
```
# replaces the current alignment block
if = { limit = { mdcw_cw_can_join_west = yes }
	# COLDWAR | human partners keep their own bloc (mdcw_cw_change_alignment moves every subject with its overlord)
	every_subject_country = { limit = { is_ai = no has_country_flag = mdcw_cw_initialized } set_variable = { COLDWAR_SOV_keep_alignment = mdcw_cw_alignment } }
	set_temp_variable = { mdcw_cw_new_alignment = 1 }
	set_temp_variable = { mdcw_cw_t_free = 1 }
	mdcw_cw_change_alignment = yes
	set_temp_variable = { mdcw_cw_t_free = 0 }
	every_subject_country = {
		limit = { has_variable = COLDWAR_SOV_keep_alignment }
		set_variable = { mdcw_cw_alignment = COLDWAR_SOV_keep_alignment }
		clear_variable = COLDWAR_SOV_keep_alignment
		mdcw_cw_recalculate_country = yes
	}
	hidden_effect = { mdcw_cw_rebuild_blocs = yes mdcw_cw_refresh_all_bloc_effects = yes }
}
```

**COLDWAR_SOV_chr_disarmament** (P3; hooks: imp_military_industrial_complex)

Uses the Imperia MIC instead of a new malus: without the defense_industry interest group the MIC export bonus (0.4 % per Arms Demand point above 25) ends. Gain: the military-industrial lobby can no longer block us; price: lost arms-tax income.
```
if = { limit = { has_idea = defense_industry } remove_ideas = defense_industry hidden_effect = { initialize_internal_faction_dynamic_modifiers = yes IMP_cold_war_update_military_industrial_complex_country = yes } }
custom_effect_tooltip = COLDWAR_SOV_mic_dissolved_tt   # "The Military-Industrial Complex loses its seat at the table: no more Export Compulsion tax bonus from Arms Demand."
```

### uds

No proposal. Defence cut uses an MD law; optionally the MIC hook of chr_disarmament.

### gt

**COLDWAR_SOV_gt_trade_with_all** (P3; hooks: imp_globalism)

Trade with all blocs = more Globalism (effective only with an opened trade law); price stays the existing tension/trade trade-off.
```
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_gosplan_modifier }
add_to_variable = { COLDWAR_SOV_gosplan_globalism_equilibrium = 5 tooltip = COLDWAR_SOV_mod_globalism_equilibrium_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_recalculate_country = yes mdcw_cw_update_world_market = yes } }
```

**COLDWAR_SOV_gt_the_resource_state** (P2; hooks: imp_oil_market, mdcw_cw_oil_system)

Legitimate Imperia oil hook: Imperia's asking-price decisions need the fossil_fuel_industry interest group and are is_ai = no, so only a human Soviet player can use them - oil stays player-only. Price: a new interest group with its own demands (same pattern as the clergy/oligarch factions in cw_manual.py).
```
if = { limit = { NOT = { has_idea = fossil_fuel_industry } }
	add_ideas = fossil_fuel_industry
	set_variable = { fossil_fuel_industry_opinion = 60 }
	hidden_effect = { initialize_internal_faction_dynamic_modifiers = yes }
}
custom_effect_tooltip = COLDWAR_SOV_oil_lobby_tt   # "The oil and gas ministries become an interest group. If we are one of Imperia's oil exporters, a player government may set our asking price (Oil Price decisions)."
```

### lnl

**COLDWAR_SOV_lnl_end_the_foreign_adventures** (P3; hooks: mdcw_cw_assistance_capacity)

Ending foreign adventures should also shrink the CW aid apparatus (capacity -2) - consistent with its tax gain.
```
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_commonwealth_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_commonwealth_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_commonwealth_modifier }
add_to_variable = { COLDWAR_SOV_commonwealth_mdcw_cw_assistance_capacity = -2 tooltip = COLDWAR_SOV_mod_mdcw_cw_assistance_capacity_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_recalculate_country = yes } }   # also recalculates capacity
```

### rd

**COLDWAR_SOV_rd_western_accounts** (P3; hooks: imp_corruption_events, imp_sanctions)

Money in Western banks: Imperia scandal events and vulnerability to financial sanctions (Imperia resistance -5 %).
```
hidden_effect = { corruption_event_3 = yes }
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_party_state_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_party_state_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_party_state_modifier }
add_to_variable = { COLDWAR_SOV_party_state_imp_sanction_resistance = -0.05 tooltip = COLDWAR_SOV_mod_imp_sanction_resistance_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
```

### fel

**COLDWAR_SOV_fel_the_rouble_convertible** (P2; hooks: imp_globalism, mdcw_cw_market_exposure)

A convertible rouble integrates the economy (EGY pattern: liberal programmes +10/+15 Globalism); price: Cold War market swings hit 10 % harder.
```
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_gosplan_modifier }
add_to_variable = { COLDWAR_SOV_gosplan_globalism_equilibrium = 10 tooltip = COLDWAR_SOV_mod_globalism_equilibrium_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_gosplan_modifier }
add_to_variable = { COLDWAR_SOV_gosplan_mdcw_cw_market_exposure = 0.1 tooltip = COLDWAR_SOV_mod_mdcw_cw_market_exposure_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_recalculate_country = yes mdcw_cw_update_world_market = yes } }
```

**COLDWAR_SOV_fel_open_to_investment** (P2; hooks: imp_minis)

Same Imperia slot for the free-enterprise path; price: foreign influence defence -10 %.
```
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_gosplan_modifier }
add_to_variable = { COLDWAR_SOV_gosplan_imp_investment_in_extra = 1 tooltip = COLDWAR_SOV_mod_imp_investment_in_extra_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_party_state_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_party_state_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_party_state_modifier }
add_to_variable = { COLDWAR_SOV_party_state_foreign_influence_defense_modifier = -0.1 tooltip = COLDWAR_SOV_mod_foreign_influence_defense_modifier_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
```

### fob

**COLDWAR_SOV_fob_conservation_first** (P3; hooks: imp_oil_price_resistance)

Conservation lowers fuel use, an input of Imperia's oil dependency formula (less exposure to oil shocks).
```
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_gosplan_modifier }
add_to_variable = { COLDWAR_SOV_gosplan_non_electric_fuel_consumption_modifier = -0.05 tooltip = COLDWAR_SOV_mod_non_electric_fuel_consumption_modifier_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
```

### smc

**COLDWAR_SOV_smc_open_to_the_world** (P3; hooks: imp_globalism, mdcw_cw_market_exposure)

Same logic for the market-socialist path; the exposure is the price.
```
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_gosplan_modifier }
add_to_variable = { COLDWAR_SOV_gosplan_globalism_equilibrium = 5 tooltip = COLDWAR_SOV_mod_globalism_equilibrium_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_gosplan_modifier }
add_to_variable = { COLDWAR_SOV_gosplan_mdcw_cw_market_exposure = 0.05 tooltip = COLDWAR_SOV_mod_mdcw_cw_market_exposure_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_recalculate_country = yes mdcw_cw_update_world_market = yes } }
```

### usr

No proposal. Republic/Union mechanics only - no Imperia/CW system applies.

### rp

No proposal. Domestic nationalism - no hook needed.

### cnr

**COLDWAR_SOV_cnr_fortress_russia** (P3; hooks: mdcw_cw_national_ideas)

Same idea for the nationalist 'fortress' path (both foci set md_closed_economy).
```
add_timed_idea = { idea = COLDWAR_SOV_ni_window_economy days = 365 }   # new idea: imp_national_ideas_2_cost_factor = -0.5
custom_effect_tooltip = COLDWAR_SOV_ni_window_import_substitution_tt   # "For a year, adopting §YImport Substitution Industrialisation§! (Government screen) costs half."
```

### com

No proposal. Strategic deterrence already raises tension; optional window for Imperia 'Fear is the Weapon' (rocket-site construction +50 %).

### rom

No proposal. No hook needed.

### eco

**COLDWAR_SOV_plan_fulfilment_campaigns** (P3; hooks: imp_national_ideas_pools)

Imperia idea imp_ni_5 (construction +25 %, workforce +4 %; bureaucracy +10 %, productivity growth -20 %, stability -5 %) is the Imperia form of Soviet plan campaigns (requires has_elections = no).
```
add_timed_idea = { idea = COLDWAR_SOV_ni_window_economy days = 365 }   # new idea: imp_national_ideas_2_cost_factor = -0.5
custom_effect_tooltip = COLDWAR_SOV_ni_window_labour_mobilization_tt   # "For a year, adopting §YNational Labour Mobilization§! (Government screen) costs half."
```

**COLDWAR_SOV_legalise_the_cooperatives** (P3; hooks: imp_national_ideas_pools, imp_development)

Imperia idea imp_ni_14 (stability +5 %, social cost -10 %, communism drift; productivity growth -10 %, investment duration +35 %) - visible for Emerging/Developed economies.
```
add_timed_idea = { idea = COLDWAR_SOV_ni_window_economy days = 365 }   # new idea: imp_national_ideas_2_cost_factor = -0.5
custom_effect_tooltip = COLDWAR_SOV_ni_window_worker_cooperatives_tt   # "For a year, adopting §YWorker Co-operatives§! (Government screen) costs half."
```

**COLDWAR_SOV_the_tolkachi** (P3; hooks: imp_corruption_events)

Fixers and grey supply = small Imperia scandal chance.
```
hidden_effect = { corruption_event_1 = yes }
```

**COLDWAR_SOV_machine_building_first** (P3; hooks: mdcw_industry_1960s_70s_techs)

Point the bonus at our own 1960s/70s machine-tool techs (category bonuses may miss them).
```
add_tech_bonus = { name = COLDWAR_SOV_machine_building_first_mdcw bonus = 0.5 uses = 1 technology = mdcw_numerical_control_1955 technology = mdcw_factory_control_1970 }   # tech IDs from mdcw_*_l_english.yml; verify the technology files
```

**COLDWAR_SOV_cybernetic_planning** (P3; hooks: mdcw_industry_1960s_70s_techs)

OGAS/CAD techs from the 1960s-70s industry folder.
```
add_tech_bonus = { name = COLDWAR_SOV_cybernetic_planning_mdcw bonus = 0.5 uses = 1 technology = mdcw_computer_aided_drafting_1963 technology = mdcw_solid_modelling_1975 }   # tech IDs from mdcw_*_l_english.yml; verify the technology files
```

**COLDWAR_SOV_group_a_means_of_production** (P3; hooks: mdcw_industry_1960s_70s_techs)

Materials techs (factory/dockyard output +3 % each).
```
add_tech_bonus = { name = COLDWAR_SOV_group_a_means_of_production_mdcw bonus = 0.5 uses = 1 technology = mdcw_pan_carbon_fibers_1961 technology = mdcw_graphitic_fibers_1970 }   # tech IDs from mdcw_*_l_english.yml; verify the technology files
```

**COLDWAR_SOV_the_scientific_technical_revolution** (P3; hooks: mdcw_industry_1960s_70s_techs)

Capstone of the economy branch -> our late machine-tool techs.
```
add_tech_bonus = { name = COLDWAR_SOV_the_scientific_technical_revolution_mdcw bonus = 0.5 uses = 1 technology = mdcw_computer_controlled_machine_tools_1975 technology = mdcw_flexible_manufacturing_1980 }   # tech IDs from mdcw_*_l_english.yml; verify the technology files
```

### agr

**COLDWAR_SOV_buy_grain_abroad** (P2; hooks: imp_sanctions)

Reads Imperia's sanction array (read-only): if a US player imposed economic sanctions (1980 grain embargo), grain imports cost 50 % more. Nothing is forced on the USA.
```
# in decision COLDWAR_SOV_buy_grain_abroad (unlocked by this focus), complete_effect:
if = {
	limit = { any_of_scopes = { array = imp_eco_sanc_on_us tag = USA } }
	set_temp_variable = { COLDWAR_SOV_gdp_share = 0.0025 }
	COLDWAR_SOV_pay_gdp_share = yes
	custom_effect_tooltip = COLDWAR_SOV_grain_embargo_tt   # "The US grain embargo forces us to buy through Argentina and Canada: +50 % cost."
}
```

### en

**COLDWAR_SOV_petrodollars** (P1; hooks: mdcw_cw_oil_system, cw_world_state_read)

Oil stays a player system: the OPEC level only moves through human votes, so `global.mdcw_cw_oil_level > 1 OR date > 1973` hands the AI a windfall in a world without an oil shock. Reading the real price ratio (read-only, AI-safe) ties the reward to what players actually did with oil; the Oil Dependency idea stays as the price.
```
# replaces the flat 1 % GDP payment
if = { limit = { check_variable = { global.mdcw_cw_oil_ratio > 2 } }
	set_temp_variable = { COLDWAR_SOV_gdp_share = 0.015 }
	COLDWAR_SOV_receive_gdp_share = yes
}
else = {
	set_temp_variable = { COLDWAR_SOV_gdp_share = 0.005 }
	COLDWAR_SOV_receive_gdp_share = yes
}
custom_effect_tooltip = COLDWAR_SOV_petrodollars_price_tt   # "Oil now: $[?global.imp_oil_price_display|.2] per barrel ([?global.mdcw_cw_oil_ratio|.1] x January 1970)"
```

**COLDWAR_SOV_the_baikal_amur_mainline** (P3; hooks: imp_infrastructure_costs)

Makes the running Imperia price of the 5 BAM infrastructure levels visible (also for the_brezhnevka, gt_siberian_projects, lnl_the_north_east, she_the_komsomol_economy).
```
custom_effect_tooltip = COLDWAR_SOV_infra_upkeep_tt   # "Every new road level costs Imperia infrastructure upkeep (0.005 bn per week and level)."
```

**COLDWAR_SOV_the_unified_energy_system** (P3; hooks: mdcw_industry_1960s_70s_techs)

Grid techs of the Early Power Engineering folder.
```
add_tech_bonus = { name = COLDWAR_SOV_the_unified_energy_system_mdcw bonus = 0.5 uses = 1 technology = mdcw_grid_dispatch_1965 technology = mdcw_grid_stability_1975 }   # tech IDs from mdcw_*_l_english.yml; verify the technology files
```

**COLDWAR_SOV_the_great_siberian_dams** (P3; hooks: mdcw_industry_1960s_70s_techs)

Bratsk/Krasnoyarsk/Sayano-Shushenskaya -> hydro turbines tech.
```
add_tech_bonus = { name = COLDWAR_SOV_the_great_siberian_dams_mdcw bonus = 0.5 uses = 1 technology = mdcw_large_hydro_turbines_1965 }   # tech IDs from mdcw_*_l_english.yml; verify the technology files
```

**COLDWAR_SOV_kuzbass_and_ekibastuz** (P3; hooks: mdcw_industry_1960s_70s_techs)

Coal plants -> steam-cycle efficiency (fossil fuel use -5 %, which also lowers Imperia oil dependency via fossil share).
```
add_tech_bonus = { name = COLDWAR_SOV_kuzbass_and_ekibastuz_mdcw bonus = 0.5 uses = 1 technology = mdcw_supercritical_steam_1957 }   # tech IDs from mdcw_*_l_english.yml; verify the technology files
```

### sci

**COLDWAR_SOV_genetics_rehabilitated** (P3; hooks: mdcw_industry_1960s_70s_techs)

Lysenko's fall -> our Early Genetics folder (agriculture +3 %, productivity growth).
```
add_tech_bonus = { name = COLDWAR_SOV_genetics_rehabilitated_mdcw bonus = 0.5 uses = 1 technology = mdcw_genetic_code_1966 technology = mdcw_recombinant_dna_1973 }   # tech IDs from mdcw_*_l_english.yml; verify the technology files
```

### army

**COLDWAR_SOV_universal_military_duty** (P3; hooks: imp_national_ideas_pools)

Imperia idea imp_ni_29 (conscription +0.5 %; productivity growth -10 %, research -5 %) matches the 1967 Law on Universal Military Duty (needs bureau_03+, SOV has bureau_04).
```
add_timed_idea = { idea = COLDWAR_SOV_ni_window_society days = 365 }   # new idea: imp_national_ideas_1_cost_factor = -0.5
custom_effect_tooltip = COLDWAR_SOV_ni_window_youth_service_tt   # "For a year, adopting §YMandatory Youth Service§! (Government screen) costs half."
```

### str

**COLDWAR_SOV_civil_defence_of_the_ussr** (P2; hooks: imp_nuclear, imp_infrastructure_costs)

Civil defence through Imperia's own nuclear model: civilian_shelter levels reduce casualties in imp_tac/big_nuke_effects (10 %/8 % per level) and carry Imperia infrastructure upkeep (0.008/level/week) - gain and running price in one existing system. Optional: Civil Defence Drills (imp_ni_50) window.
```
capital_scope = { add_building_construction = { type = civilian_shelter level = 2 instant_build = yes } }
set_temp_variable = { COLDWAR_SOV_gdp_share = 0.003 }
COLDWAR_SOV_pay_gdp_share = yes
custom_effect_tooltip = COLDWAR_SOV_shelters_tt   # "Two levels of civil-defence shelters in Moscow: nuclear casualties there fall by 16 % (Imperia). Upkeep 0.016 bn per week."
```

### navy

**COLDWAR_SOV_the_shipyards_of_the_north** (P3; hooks: imp_national_ideas_pools)

Imperia idea imp_ni_36 (dockyard output +15 %, dockyard construction +40 %; bureaucracy +30 %, construction -20 %) fits Severodvinsk/Nikolaev; requires defence spending above defence_02 (SOV has defence_07).
```
add_timed_idea = { idea = COLDWAR_SOV_ni_window_military days = 365 }   # new idea: imp_national_ideas_3_cost_factor = -0.5
custom_effect_tooltip = COLDWAR_SOV_ni_window_maritime_hub_tt   # "For a year, adopting §YMaritime Industry Hub§! (Government screen) costs half."
```

### kgb

**COLDWAR_SOV_active_measures** (P2; hooks: mdcw_cw_national_ideas, imp_national_ideas_pools)

Radio Moscow / Radio Peace and Progress = CW idea International Broadcasting Service (campaigns +25 %, ideological defence +10 %; 0.2 bn/month, each campaign tension +0.1). Note: AI SOV already takes it as bloc leader.
```
add_timed_idea = { idea = COLDWAR_SOV_ni_window_society days = 365 }   # new idea: imp_national_ideas_1_cost_factor = -0.5
custom_effect_tooltip = COLDWAR_SOV_ni_window_broadcasting_tt   # "For a year, adopting §YInternational Broadcasting Service§! (Government screen) costs half."
```

**COLDWAR_SOV_kgb_border_troops** (P2; hooks: mdcw_cw_national_ideas)

KGB Border Troops = CW idea Border Regime and Exit Controls (research +3 %, ideological defence +15 %, drift defence +10 %; stability -3 %, trade opinion -10 %, Globalism -5).
```
add_timed_idea = { idea = COLDWAR_SOV_ni_window_society days = 365 }   # new idea: imp_national_ideas_1_cost_factor = -0.5
custom_effect_tooltip = COLDWAR_SOV_ni_window_border_regime_tt   # "For a year, adopting §YBorder Regime and Exit Controls§! (Government screen) costs half."
```

**COLDWAR_SOV_open_the_gates** (P3; hooks: mdcw_cw_national_ideas, imp_refugees)

Consistency with the CW national idea: Border Regime clamps emigration on adoption; opening the gates for Jewish emigration contradicts it. Respect its 1440-day lock flag.
```
available = { NOT = { has_idea = mdcw_ni_border_regime } }   # or remove it: if = { limit = { has_idea = mdcw_ni_border_regime NOT = { has_country_flag = flag_ni_mdcw_border_regime } } remove_ideas = mdcw_ni_border_regime }
```

### union

**COLDWAR_SOV_irrigate_the_desert** (P3; hooks: imp_corruption_events)

Cotton pripiski start here; Imperia scandal chance.
```
hidden_effect = { corruption_event_1 = yes }
```

### soc

**COLDWAR_SOV_the_demographic_gap** (P3; hooks: imp_national_ideas_pools)

1981 maternity measures = Imperia idea imp_ni_3 (population +0.15; population tax -4 %, social cost +10 %).
```
add_timed_idea = { idea = COLDWAR_SOV_ni_window_society days = 365 }   # new idea: imp_national_ideas_1_cost_factor = -0.5
custom_effect_tooltip = COLDWAR_SOV_ni_window_natality_tt   # "For a year, adopting §YNatality Campaigns§! (Government screen) costs half."
```

### det

**COLDWAR_SOV_save_detente** (P2; hooks: mdcw_cw_detente_initiative, mdcw_cw_ideas)

Uses the CW Detente mechanic instead of a parallel one: our focus opens the initiative; it only becomes a Detente agreement if the US (or Beijing) leader takes its own Detente decision within 90 days - an offer, never forced. Price: Hawks Oppose Detente (war support -5 %, 180 days) on top of the existing -50 PP. AI never triggers it (CW rule: AI starts nothing).
```
if = {
	limit = { is_ai = no has_country_flag = mdcw_cw_initialized mdcw_cw_is_bloc_leader = yes }
	custom_effect_tooltip = COLDWAR_SOV_detente_offer_tt   # "We open a Detente initiative: if another bloc leader takes 'Detente Initiative' within 90 days, both get Detente and tension falls by 5."
	hidden_effect = { mdcw_cw_detente_initiative = yes }
	add_timed_idea = { idea = mdcw_cw_detente_hawks days = 180 }
}
```

**COLDWAR_SOV_superiority_not_parity** (P2; hooks: mdcw_cw_ideas)

Reuse the CW 'Show of Strength' spirit (war support +5 %, army XP +5 %) instead of inventing a new one; the price (tension +3 -> lower Market Confidence and higher Arms Demand for everyone) is already in the focus.
```
add_timed_idea = { idea = mdcw_cw_show_of_strength days = 180 }
```

**COLDWAR_SOV_trade_and_credits** (P2; hooks: imp_globalism, imp_sanctions)

Western credits mean exposure: a small Globalism push (only matters once the trade law opens) and lower sanction resistance - a Western credit embargo would now hurt. Price for the existing technology/trade gains.
```
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_gosplan_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_gosplan_modifier }
add_to_variable = { COLDWAR_SOV_gosplan_globalism_equilibrium = 5 tooltip = COLDWAR_SOV_mod_globalism_equilibrium_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_party_state_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_party_state_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_party_state_modifier }
add_to_variable = { COLDWAR_SOV_party_state_imp_sanction_resistance = -0.05 tooltip = COLDWAR_SOV_mod_imp_sanction_resistance_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_recalculate_country = yes mdcw_cw_update_world_market = yes } }
```

**COLDWAR_SOV_the_helsinki_conference** (P2; hooks: mdcw_cw_ideological_defence)

Basket Three: human-rights monitoring makes foreign Public Political Support campaigns more effective inside the USSR - the CW price of the Helsinki gains.
```
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_party_state_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_party_state_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_party_state_modifier }
add_to_variable = { COLDWAR_SOV_party_state_mdcw_cw_ideological_defence = -0.05 tooltip = COLDWAR_SOV_mod_mdcw_cw_ideological_defence_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
```

### chi

No proposal. Tension already used on the strike path; plan_lop_nur only creates a wargoal (no war forced). If a nuclear option is ever added, Imperia's strike effects fire automatically. Beijing is a CW bloc leader - reconcile_with_beijing could read global.mdcw_cw_share_3 for AI weights.

### bloc

**COLDWAR_SOV_the_commonwealth_of_socialist_nations** (P1; hooks: mdcw_cw_assistance_capacity, mdcw_cw_bloc_triggers)

Capstone gives +1 assistance capacity: refresh like the NIs. Gate on still being in bloc 2 (after a West/NA path the 'socialist commonwealth' bonus makes no sense).
```
available = { check_variable = { mdcw_cw_alignment = 2 } }   # we still lead the Soviet bloc
hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_recalculate_country = yes } }   # also recalculates capacity
```

**COLDWAR_SOV_the_comprehensive_programme** (P1; hooks: mdcw_cw_bloc_leader_decisions)

The SOV generator ships a hand-patched copy of the generated common/decisions/mdcw_cold_war_decisions.txt; the next `generate_mdcw_cold_war.py` run overwrites it (and the validator flags hand edits). A generic refund variable in the CW generator keeps one system and lets other trees (Comecon members, other leaders) use the same hook.
```
set_variable = { mdcw_cw_refund_comecon = 25 }   # replaces set_country_flag = COLDWAR_SOV_comprehensive_programme
# CW generator (tools/_gen_decisions.py), mdcw_cw_dec_comecon complete_effect:
#   if = { limit = { check_variable = { mdcw_cw_refund_comecon > 0 } } add_political_power = mdcw_cw_refund_comecon }
```

**COLDWAR_SOV_the_brezhnev_doctrine** (P2; hooks: imp_sanctions)

Bloc discipline makes Moscow's Imperia sanctions bite harder (the CW bloc-embargo call then has weight); the price (tension +1, idea) is already there. With Globalism 0 our base effectiveness is -80 %, so this is modest.
```
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_SOV_commonwealth_modifier } } } hidden_effect = { add_dynamic_modifier = { modifier = COLDWAR_SOV_commonwealth_modifier } } }
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_SOV_commonwealth_modifier }
add_to_variable = { COLDWAR_SOV_commonwealth_imp_sanction_effectiveness = 0.05 tooltip = COLDWAR_SOV_mod_imp_sanction_effectiveness_tt }
hidden_effect = { force_update_dynamic_modifier = yes }
```

**COLDWAR_SOV_subsidised_oil** (P2; hooks: imp_oil_price_resistance)

Turns 'subsidised oil' into a real Imperia effect for the partners (their oil dependency falls) instead of opinion only - as an offer each Comecon member accepts or declines. Price for us stays: oil export income -5 %.
```
every_country = {
	limit = { has_country_flag = mdcw_cw_initialized check_variable = { mdcw_cw_alignment = 2 } NOT = { original_tag = SOV } }
	country_event = { id = COLDWAR_SOV.<new> days = 1 }   # 'Fraternal Oil': accept -> add_timed_idea = { idea = COLDWAR_SOV_fraternal_oil days = 1825 } (imp_oil_price_resistance = 0.15); decline -> nothing
}
```

**COLDWAR_SOV_world_market_prices** (P3; hooks: cw_world_state_read, mdcw_cw_oil_system)

Charging Comecon world prices is worth more after an oil shock: read-only scaling with the real oil price (AI-safe).
```
# replaces the flat 0.3 % GDP
set_temp_variable = { COLDWAR_SOV_gdp_share = 0.002 }
multiply_temp_variable = { COLDWAR_SOV_gdp_share = global.mdcw_cw_oil_ratio }
clamp_temp_variable = { var = COLDWAR_SOV_gdp_share min = 0.002 max = 0.01 }
COLDWAR_SOV_receive_gdp_share = yes
```

**COLDWAR_SOV_let_them_go_their_way** (P2; hooks: mdcw_cw_change_alignment, mdcw_cw_bloc_triggers)

Sinatra logic through the CW alignment system: every Soviet-bloc member may leave free of PP and lock - its own choice (offer). Check mdcw_cw_can_change_alignment for subjects (autonomy_warsaw) before showing option A. Price for us: bloc share/upkeep base shrinks if they go.
```
every_country = {
	limit = { has_country_flag = mdcw_cw_initialized check_variable = { mdcw_cw_alignment = 2 } NOT = { original_tag = SOV } }
	country_event = { id = COLDWAR_SOV.<new> days = 1 }   # option A (partner scope): set_temp_variable = { mdcw_cw_new_alignment = 0 } set_temp_variable = { mdcw_cw_t_free = 1 } mdcw_cw_change_alignment = yes; option B: stay
}
```

**COLDWAR_SOV_the_socialist_commonwealth** (P2; hooks: mdcw_cw_bloc_triggers)

The whole bloc branch assumes we lead bloc 2; after a West/NA switch it should close (alternatively mdcw_cw_is_bloc_leader = yes).
```
available = { check_variable = { mdcw_cw_alignment = 2 } }
```

### tw

**COLDWAR_SOV_economic_aid_programmes** (P1; hooks: mdcw_cw_assistance_capacity, mdcw_cw_national_ideas, imp_national_ideas_pools)

Capacity +2 only reaches the Programmes tab at the next monthly tick; the CW national ideas call mdcw_cw_recalculate_country on change - do the same. Generator-level: in cw_effects.dyn_change append the recalc line whenever a key starts with mdcw_cw_ (covers all 26 foci with CW modifiers). The NI window makes the Development Agency (+4 capacity, bureaucracy +10 %, PP -5 %, population tax -3 %) the natural next step; its own costs stay.
```
hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_recalculate_country = yes } }   # also recalculates capacity
add_timed_idea = { idea = COLDWAR_SOV_ni_window_economy days = 365 }   # new idea: imp_national_ideas_2_cost_factor = -0.5
custom_effect_tooltip = COLDWAR_SOV_ni_window_development_agency_tt   # "For a year, adopting §YInternational Development Agency§! (Government screen) costs half."
```

**COLDWAR_SOV_military_advisers** (P1; hooks: mdcw_cw_military_programme_cost, mdcw_cw_national_ideas)

Military programme cost -15 % needs the same refresh. Window towards the CW national idea Military Advisers Abroad (programmes -25 %, army XP +5 %; war support -3 %, army personnel cost +3 %).
```
hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_recalculate_country = yes } }   # also recalculates capacity
add_timed_idea = { idea = COLDWAR_SOV_ni_window_military days = 365 }   # new idea: imp_national_ideas_3_cost_factor = -0.5
custom_effect_tooltip = COLDWAR_SOV_ni_window_military_advisers_tt   # "For a year, adopting §YMilitary Advisers Abroad§! (Government screen) costs half."
```

**COLDWAR_SOV_arms_on_credit** (P3; hooks: cw_world_state_read, imp_military_industrial_complex)

Arms exports pay more in a high Arms Demand world (CW tiers 'High'/'Surge' give arms sales income +20/30 %); read-only world state.
```
# ai_will_do
modifier = { add = 5 check_variable = { global.mdcw_cw_arms > 59 } }
# completion_reward
if = { limit = { check_variable = { global.mdcw_cw_arms > 59 } } add_political_power = 25 }   # optional: cheap boost when the world arms market is hot
```

