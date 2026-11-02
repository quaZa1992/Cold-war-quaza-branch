# Cuba 1970–1990 concept: effect/API audit

Scope: concept-stage mechanics inventory only; no runtime edits. Evidence checked against this checkout and installed MD 2777392649. Static source establishes API/provider/consumer presence, not in-game scope, balance, tooltip rendering or multiplayer synchronization.

## Political gates and reactivation

The January 1970 CUB setup in history/countries/CUB - Cuba.txt sets ruling_party = 4 (PCC), while set_politics uses the broad ideology communism. tools/party_registry_1970/data/CUB.json is authoritative for live subparty slots. Important slots: PCC 4; Microfracción 6; MININT 7; El Hombre Nuevo/Guevarism 19; FAR 22; JUCEPLAN 13; OSPAAAL 5; exile Christian Democrats 1, constitutional liberals 2, Auténtico social democrats 3, RECE 0. Other actual slots are Vergüenza contra Dinero 18, Catholic Church 14, Cuban Academy 17, exile landowners 15, CAMACOL 16, Alpha 66 20, Cuban Nationalist Movement 21, and Hispanist monarchists 23. Slots 8–12 are diaspora/student religious groups; do not elevate them to national governing branches without separate design evidence.

Use check_variable = { ruling_party = N } for the exact subparty, never ideology alone. change_ruling_party_effect in common/scripted_effects/00_MD_politicsview_scripted_effects.txt sets the subparty, then updates leadership, coalition and IP_idea_configuration; it already contains country refresh hooks for Syria, Vietnam, Iraq and UAE. Cuba requires a custom refresh hook and a registered dynamic modifier or idea gated by exact party slot. Gate both availability and reward application. Durable outcomes (buildings, one-time grants, enacted policy) must be separated from active party programmes. On returning to a party, reactivate its programme without replaying one-time rewards. This is custom glue.

## Supported effect families and likely applications

| Policy intent | Supported API and proven reader | Scope, units and caps | Cuba concept and boundary |
|---|---|---|---|
| Sugar diversification / food security | Imperia agrarian economy: AGRI_allocation_change_effect, AGRI_shift_crop_allocation, AGRI_price_change_effect, AGRI_update_math_variables in common/scripted_effects/00_agrarian_economy_effects.txt. agri_crop_allocation^0 (basic) and ^1 (cash) each clamp 0..1. Reader computes workers × share × price, combined crop value and weekly harvest income. | Country economy variables; yearly harvest is converted to weekly income by 0.00019 (annual / 52 / 100). Allocation bounded 0..1. | Existing model has basic/cash crop shares and harvest income, but no sugar identity, tonnage, ration queue or import substitution. Diversification can use a transparent basic-vs-cash proxy. Literal sugar output or rations require custom category/reader and must not be claimed from the proxy. |
| Health and education | Native increase_healthcare_budget[_2..4] and increase_education_budget[_2..4] in common/scripted_effects/00_budget_effects.txt swap existing law-tier ideas. EDU_update_education_idea_DYNMOD, annual pulse and literacy update in 00_education_effects.txt drive literacy (clamped 0.01..1) and related research, productivity and workforce modifiers. Imperia health_cost_multiplier_modifier and education_cost_multiplier_modifier have consumers. | Country-wide spending tier; literacy changes through yearly simulation. Cost multipliers must be traced to cost formula before selecting values. | Reuse the existing tier transitions, after verifying CUB has literacy initialization. Do not describe a tier step as an immediate flat literacy grant. Above tier cap, helper fallback can grant PP rather than more service. |
| Soviet dependence / US normalization | Native effects set_improved_trade_agreement, add_opinion_modifier, reverse_add_opinion_modifier. CUB history initializes bilateral economic relations with USA/SOV. Imperia trade_opinion_factor and international_market_income_modifier have readers. | Bilateral relations or country modifier. International-market income is not literal bilateral volume. | Use relation/trade agreement plus explicit foreign-policy terms. Soviet oil, arms or credit dependence and embargo relief need bilateral accounting/custom effects. A globalism variable without a reader is not an effect. |
| Public service / scarcity / limited private activity | Native ideas/dynamic modifiers support consumer_goods_factor, civilian_industry_tax_modifier, agriculture_tax_modifier, corporate_tax_income_multiplier_modifier, total_workforce_modifier, factory productivity and building speed. One-time money cost uses treasury_change and modify_treasury_effect. | National modifier units are determined by the actual consumer. Treasury uses current MD money units. Any recurring expense must be weekly and displayed weekly; convert source periods before writing. | Planned/private compromise can be represented by an idea with real production/tax effects. There is no base ownership or workplace-governance simulation. Worker councils and private-sector share require custom institution variables and a reconciler/decision; do not label generic output as ownership. |
| Repression / migration | Reuse police spending tiers, intelligence modifiers, foreign_influence_defense_modifier, drift_defence_factor, resistance-effectiveness, and monthly_population. | Law tiers/intelligence are national. monthly_population changes population growth; it is not a politically motivated refugee count. | Show surveillance/censorship through actual law/intelligence systems. Exile/migration totals, return and amnesty policies need custom counters/effects. |
| Defense vs revolutionary missions abroad | Native modifiers support army_core_defence_factor, army_defence_factor, attack/org, training, special-forces cap and naval/air/intelligence effects. DDR/SOV dynamic modifier files demonstrate party and office programme ownership. | Effects feed HOI4 combat or MD intelligence readers. Generic attack does not distinguish home defense from overseas deployment. | Territorial defense can use core defense, training or doctrine. Internationalist missions need custom expeditionary commitment/cost/readiness if the mechanic itself must change. |
| DDR island agreement | Native country events/options, country scopes, opinion/relation effects and recipient-owned proposal/acceptance patterns exist elsewhere in project. Joint focus examples show member-specific rewards. | Revalidate payer, recipient, pending state, eligibility and cost at acceptance. Sending an offer is not executing an agreed project. | Custom bilateral event/flag lifecycle needed for offer, acceptance, price, delivery, refusal/expiry and duplicate prevention. No live Cuba-DDR treaty effect found. |

## Costs, scale, references and suitable research

Normal MD focuses commonly use cost = 10 (70 days at 7 days per point). Syntax/value examples: installed MD GENERIC_expand_the_secret_service in common/national_focus/00_generic.txt costs 10, gives one 25% CAT_night_vision research use, opinion changes and an idea. GENERIC_build_intelligence_stations (near line 320) deducts 3.5 Treasury once and instant-builds two radar stations if each has a valid slot. These are API references, not Cuba balance targets. Installed MD CHI_NKO_defense_consultations in 03_china_north_korea_joint.txt grants 25 army XP and a 50% land-doctrine cost reduction for two uses to originator and one to member, guarded by selected-doctrine logic. APIs: add_tech_bonus = { name = ... category = ... uses = N bonus = 0.25 }; add_doctrine_cost_reduction = { name = ... category = land_doctrine cost_reduction = 0.50 uses = N }; add_equipment_bonus = { name = ... bonus = { infantry_weapons_type = { build_cost_ic = -0.04 } } }.

CUB 1970 history starts empty land, naval and air OOBs. Use the mod's 1940–1970 equipment and research definitions, not 2000-era stock. Examples present in the 1970 tech set include mdcw_infantry_weapons_1950/1955, mdcw_cnc_equipment_1950/1960, mdcw_support_weapons_1955, mdcw_util_vehicle_1950/1960, early anti-air/anti-tank, 1960 body armor, 1950 special forces, and 1968 engineer vehicles. 1980 rifle, 1972 night vision, thermal, drone, digital and other post-2000 options are future or inappropriate. Verify each actual research category contains valid technologies. Doctrine bonuses use doctrine API, not tech categories. CUB history currently applies mdcw_apply_1970_infantry_research; ensure any proposed research use remains available after scenario initialization.

Recurring money values must be weekly MD units with no more than five fractional digits in scripted literals. Trace each expense's source period and actual consumer. Distinguish one-time, timed and tick-maintained effect. For construction, validate ownership, available slots, caps and instant/queued behavior before promising a building.

## Unsupported or custom-glue list

- Dedicated sugar output, sugar export tonnage, food stocks and ration fulfilment: not in current agrarian model; only basic/cash allocation and price are proven.
- Cuba-specific Soviet fuel/arms exposure or credit dependency: generic relations/trade exist, exact bilateral commodity flow needs a custom reader.
- The IMPERIA refugee system is live: imp_refugee_pull_modifier changes a nation's share of globally available refugees, while imp_refugee_integration_rate controls integration conversion. The mdcw_diaspora/guest-worker system records bilateral guest-worker and voluntary return agreements, migration stocks by origin and weekly settlement costs. It is not a gross net-emigration counter or a Cuba-specific exile register. Cuba can reuse it if the relevant guest-worker policy idea/UI is unlocked; politically attributed exile, asylum and amnesty still need explicit Cuban policy/event glue.
- Worker-council authority, cooperative/private ownership ratio and expeditionary manpower: no existing Cuba reader found; require custom state and effects.
- DDR agreement lifecycle: custom event/decision glue; other-country transaction patterns are architecture, not an existing Cuba offer.
- Cuba party programme lifecycle: custom exact-slot refresh hook/modifiers; verify reactivation and avoid replaying one-time grants.

## Source anchors

Project: tools/party_registry_1970/data/CUB.json; history/countries/CUB - Cuba.txt; common/scripted_effects/00_MD_politicsview_scripted_effects.txt (change_ruling_party_effect); common/scripted_effects/00_agrarian_economy_effects.txt; common/scripted_effects/00_education_effects.txt; common/scripted_effects/00_budget_effects.txt; common/dynamic_modifiers/COLDWAR_DDR_1970_dynamic_modifiers.txt and COLDWAR_SOV_1970_dynamic_modifiers.txt; common/technologies/mdcw_early_infantry.txt, mdcw_early_railway.txt, armor.txt, infantry.txt. Installed MD: common/national_focus/00_generic.txt and 03_china_north_korea_joint.txt.


## Exact key whitelist and machine-usable primitives

The keys below have traceable providers and consumers in this project. For dynamic modifiers, register the native key in the modifier block and map it to a Cuba variable; declaring a dynamic idea alone does not provide behavior.

| Key | Provider and consumer | Valid interpretation |
|---|---|---|
| bureaucracy_cost_multiplier_modifier | money_modifier_definitions.txt registers percentage/country; 00_money_system.txt:3333 multiplies bureaucracy expense by 1 + key | A recurring bureaucracy cost multiplier. Negative reduces expense; positive raises it. |
| health_cost_multiplier_modifier | money_modifier_definitions.txt; 00_money_system.txt:3498 multiplies per-capita health-law costs by 1 + key | Changes ongoing health-budget cost, not service outcomes directly. |
| education_cost_multiplier_modifier | money_modifier_definitions.txt; 00_money_system.txt:3396 adds key into education cost multiplier before calculating level costs | Changes education-law expenditure, not literacy directly. |
| total_workforce_modifier | money_modifier_definitions.txt:473; 00_money_system.txt:5238 adds key in workforce calculation | Workforce adjustment; usable for labor mobilization/constraint with a political cost. |
| agricolture_productivity_modifier | money_modifier_definitions.txt:353; 00_money_system.txt:417, 5342 and 6053 read it in farm/district productivity and GDP formulas | Exact legacy spelling is agricolture. Productivity for the existing agriculture system; no sugar identity. |
| agriculture_district_income_tax_modifier | money_modifier_definitions.txt:275; 00_money_system.txt:550 reads it into district tax income | Changes agriculture tax receipts. Pair higher tax with productivity/investment if desired. |
| civilian_factories_productivity | money_modifier_definitions.txt:381; 00_money_system.txt:469 and 6025 apply it to industrial output/GDP | Existing civilian industry output key. |
| industrial_capacity_factory | Native country modifier; 00_productivity_effects.txt:171 and 00_ledger_scripted_effects.txt:99 read it for factory output/productivity accounting | Broad factory output, not an extra factory. Avoid stacking with a duplicate factory-output reward. |
| production_speed_buildings_factor | Native registered modifier; 00_productivity_effects.txt:141, 01_international_systems_effects.txt:2088 and 99_investment_scripted_effects.txt:311 read construction speed | Speeds legal builds; does not create a building. |
| international_market_income_modifier | money_modifier_definitions.txt:529; 00_money_system.txt:2425 adds it in international-market income calculation | Market income modifier, not bilateral Cuban-US/Soviet import volume. |
| migration_rate_value_factor | migration_modifier_definitions.txt:18; 00_money_system.txt:6708 and 6715 add it to migration calculations | Native migration-rate adjustment, subject to law and wider migration calculations. |
| imp_refugee_pull_modifier | mdcw_imperia_idea_dependency_modifiers.txt registers percentage; imp_refugees_effects.txt:204 adds it to base 1 then clamps final pull factor 0..2 in refugee share | Refugee attraction/pull, separate from emigration. |
| imp_refugee_integration_rate | Same modifier definition file; imp_refugees_effects.txt:279 adds it to base 1 and clamps 0..2 before converting costly refugees into manpower | Refugee integration rate. |
| imp_sanction_effectiveness | mdcw_imperia_globalism_modifiers.txt registers; imp_sanctions_effects.txt:17–18 adds to a base 1.5 multiplier used in sanction-strength calculations | Scales outgoing sanctions; does not grant Cuba immunity from a US embargo. |
| imp_sanction_resistance | Same modifier definitions; imp_sanctions_effects.txt:131–132 subtracts from base 1 incoming-sanction multiplier; downstream rates clamp to 0..1 | Resistance to Imperia sanction impacts, distinct from trade normalization. |
| political_power_factor | Native HOI4/MD modifier, supplied in ideas/dynamic modifiers and consumed by the game's daily PP calculation | Real modifier; supplement a substantive programme rather than using it as the only result. |
| stability_factor | Native modifier; 00_money_system.txt:6752 reads into weekly stability economy component, plus game stability system | Factor on stability; check combined national sources/caps. |
| army_core_defence_factor | Native combat modifier used by HOI4 combat; registered in COLDWAR DDR/SOV party and army dynamic modifiers | Core defense specialization; does not distinguish overseas deployment. |
| intelligence_agency_defense | Native MD intelligence modifier used by agency/counterintelligence system | Defensive counterintelligence; agency/DLC setup must exist before promising agency actions. |

Machine-usable snippets, all concept-only until balance, scope and visible reward checks are complete:

One-time Treasury cost:
set_temp_variable = { treasury_change = -3.5 }
modify_treasury_effect = yes

Provider: common/scripted_effects/00_budget_effects.txt:1487–1498. It adds treasury_change to treasury unless MD_skip_treasury_cost is set. It can make the balance negative. Do not add a Treasury affordability gate unless the design explicitly needs one.

Debt change:
set_temp_variable = { debt_change = 2.0 }
modify_debt_effect = yes

Provider: common/scripted_effects/00_budget_effects.txt:1501–1507. To reduce debt use debt_change = -2.0. It clamps debt at zero. It does not itself increase Treasury; a loan needs a separate disbursement and explicit repayment/interest contract.

Custom weekly revenue stream:
add_to_variable = { additional_income_rate = 0.05 }

Provider/consumer: common/scripted_effects/00_money_system.txt:807 onward resets and aggregates additional_income_rate in the weekly economy. Values are MD billions per week. A recurring expense needs integration into calculate_additional_expense_rate or an existing weekly expense reader, plus a visible weekly amount. A one-time Treasury subtraction is not a recurring expense.

Corruption tier change:
increase_corruption = yes
decrease_corruption = yes

Providers: common/scripted_effects/00_budget_effects.txt:675 onward and paired corruption_level_01..10 ideas in common/ideas/AA_corruption_laws.txt. These switch the existing law level. Do not assume the similarly named corruption_cost_factor is a generic audited money expense key without tracing the applicable law consumer.

Health and education:
increase_education_budget = yes
increase_healthcare_budget = yes

These advance an existing idea tier by one and preserve tier caps/fallback behavior.

Basic/cash crop shift:
set_temp_variable = { allocation_change = 0.05 }
AGRI_shift_crop_allocation = yes

The helper moves share between basic and cash crops, clamping both. allocation_change is a share delta, not a production percentage.

Conditional instant construction:
random_owned_state = {
  limit = { free_building_slots = { building = industrial_complex size > 0 include_locked = no } }
  add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}

Use a separate valid Treasury transaction. This chooses one legal owned state; guarantee multiple levels with explicit slot checks or safe queue logic.

Technology, doctrine and military:
army_experience = 25
add_tech_bonus = { name = CUB_example category = CAT_small_arms uses = 1 bonus = 0.25 }
add_doctrine_cost_reduction = { name = CUB_example category = land_doctrine cost_reduction = 0.50 uses = 1 }

Confirm the technology category contains the intended technologies available from the 1970 start. Keep doctrine API separate.

Diplomacy:
add_opinion_modifier = { target = USA modifier = recent_actions_positive }
break_embargo = USA

The reverse direction is USA = { send_embargo = CUB }. USA 1970 history adds its opinion modifier toward CUB but no send_embargo = CUB command was found in that history block. Check is_embargoing/is_embargoed_by in the live campaign before claiming a formal embargo has been lifted; distinguish opinion dispute from engine embargo state.

Party refresh integration point:
Inside change_ruling_party_effect in common/scripted_effects/00_MD_politicsview_scripted_effects.txt, after set_leader = yes / IP_idea_configuration = yes and beside existing original_tag scenario-specific refresh conditionals. If later authorized, the Cuba branch can be:
if = { limit = { original_tag = CUB IMP_is_1970_scenario = yes } COLDWAR_CUB_refresh_programmes = yes }

Cuba helper must be idempotent and only reconcile currently active dynamic programmes; do not place cash, factories or other once-only outcomes in it. This hook is a recommendation, not an implemented change.

## Related existing features

- Colonial Affairs cannot be reused as a generic Cuban foreign-support system. Its contact triggers route Iraq and RAF cases; foreign contacts require an intelligence agency and network strength above 50 in an eligible registered or occupied state. It is scoped around compiled imperial/occupation cases and has no generic African or Latin American revolutionary target map.
- A compatible diplomatic pattern is COLDWAR_SPR_v2_iberoamerican_credit in common/decisions/COLDWAR_SPR_v2_agreements.txt. Its explicit target list includes CUB and its proposal is recipient-owned. It represents Spanish Ibero-American credit; a DDR-Cuba settlement needs its own history-appropriate contract.
- U.S.-Cuba embargo sources: history/countries/USA - USA.txt adds opinion modifier embargo toward CUB; common/opinion_modifiers/Cuban-American Relations.txt defines CUB_USA_Embargo = -40 for Cuban diplomacy. No active send_embargo = CUB was found in the USA 1970 history block. Engine commands send_embargo and break_embargo occur in other focus/event systems. Guard the prospective terms against live is_embargoing/is_embargoed_by state.
- Imperia globalism has a real weekly reader in common/on_actions/zzzzzz_mdcw_imperia_globalism_on_actions.txt and dynamic modifier imp_globalism_modifier feeds sanction effectiveness/resistance, productivity growth, returns, investment duration and foreign-influence defense. Do not present globalism as a generic trade-open slider; connect effects to those registered fields and their consumers.
