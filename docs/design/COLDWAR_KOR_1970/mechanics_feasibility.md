# South Korea 1970–1990 Focus Tree: Mechanics and Integration Feasibility

Read-only audit of the target MD Cold War checkout and the supplied Millennium Dawn workshop source. No loaded mod scripts were changed. This report identifies existing APIs and providers; it is not a balance proposal or approval to implement.

## Executive result

- Target is MD Cold War 2.0.2 for HOI4 1.19. The 1 January 1970 KOR history loads mdcw_1970_generic_focus; no dedicated KOR 1970 tree is loaded in target at audit time. Donor MD includes 05_south_korea.txt and legacy KOR focus material, but target's 1970 history replaces the campaign start and must remain the authority for new-tree integration.
- Runtime party registry base: 0 DRP, 1 NDP, 2 Forties Standard-Bearers (Kim Young-sam/Kim Dae-jung revolt combined), 3 Unification Socialist Party, 4 underground Revolutionary Party for Reunification, 5 June Third Generation, 7 KCIA, 13 Economic Planning Board coalition technocracy, 22 Army, and 23 Yi dynasty. This 1970 taxonomy does not encode later DRP successor factions, Chun/Roh party identity, or separate YS and DJ party slots.
- Existing native/MD national modifiers and Imperia-CW economy can support economic, military, domestic-security, labour and diplomatic trade-offs. Use modifier fields with actual consumers. Use native treasury (billions) for one-time spending and existing weekly expense-rate flow for recurring upkeep. Do not set debt directly or invent monthly money fields.
- Korean unification is already an NKO-owned offer/response system. NKO has Korean-channel and confederation-offer focuses, recipient-side events, and an armed reunification path. South Korean content should extend/use a bilateral contract only after reviewing both scopes; a unilateral KOR focus should not auto-accept an NKO proposal.
- Static evidence supports a Park/DRP 1970 start and opposition routes. Static source inspection does not prove parser acceptance, in-game tooltips, runtime scope resolution, campaign behavior, or save compatibility.

## Environment and evidence boundary

Target: C:\Users\sonyz\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar-main (descriptor version 2.0.2; supported HOI4 1.19.*). Donor MD: C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\2777392649.

Primary anchors inspected:
- history/countries/KOR - Korea.txt; history/states/604-Gyeonggi.txt through 608-Jeju.txt
- tools/party_registry_1970/data/KOR.json and generated historical party pools/effects/triggers under common/scripted_effects and common/scripted_triggers
- common/national_focus/COLDWAR_NKO_1970_focus.txt, common/scripted_effects/COLDWAR_NKO_1970_focus_effects.txt, events/COLDWAR_NKO_1970_foreign_events.txt
- common/dynamic_modifiers/99_KOR_dynamic_modifiers.txt, mdcw_1970_generic_party_programmes.txt, mdcw_imperia_development_dynamic_modifiers.txt
- common/scripted_effects/00_money_system.txt, IMP_1970_gdp_scripted_effects.txt, mdcw_imperia_development_effects.txt, mdcw_imperia_debt_effects.txt, COLDWAR_nuclear_power_effects.txt, COLDWAR_nuclear_development_budget.txt

The modifier-audit and national-tree skills, references, project contract and source map were read. This is not engine verification.

## 1970 setup and tree integration

The target's history/countries/KOR - Korea.txt has a 1970.1.1 snapshot. It sets the historical-politics scenario flag, initializes popularity and custom party arrays, sets ruling_party = 0, places coalition slot 13, and creates Park Chung Hee as incumbent through 1979-10-26. Before 1985 it loads mdcw_1970_generic_focus, sets GDP per capita/productivity and gives KOR mdcw_ni_overseas_employment_programme. The campaign also starts with empty land/naval/air OOBs as a temporary setup. Park's ruling-party route is playable from the start; no unlock focus for the already ruling DRP is justified.

Registry details from tools/party_registry_1970/data/KOR.json:

| Slot | Start representation | Integration note |
|---:|---|---|
| 0 | Democratic Republican Party (DRP) | Ruling party at start; Park's governing civilian vehicle. |
| 1 | New Democratic Party (NDP) | Main opposition; native pool includes Kim Young-sam. |
| 2 | Forties Standard-Bearers | Internal opposition generation; YS/DJ revolt is combined, not a separate party. |
| 3 | Unification Socialist Party (USP) | Small legal left opposition; Kim Dae-jung pool is associated with slot 3. |
| 4 | Revolutionary Party for Reunification (RPR) | Underground; do not treat as a normal cabinet route without resolving legality. |
| 5 | June Third Generation | Student pressure/base, not an incumbent party. |
| 7 | Korean Central Intelligence Agency | Regime power bloc; explicitly not the ruling party. |
| 13 | Economic Planning Board | Technocratic coalition member, distinct from incumbent party. |
| 22 | Army | Military power base and successor path; native pool includes Park and Chun Doo-hwan. |
| 23 | Yi dynasty | Monarchist fringe; not covered in this audit. |

The history clears/resizes arrays and sets slots explicitly. Do not assume party_pop_array indexes equal vanilla ideology identifiers, or that outlook alone identifies a subparty. Registry/coalition and generated pools provide the 1970 model, not the whole later party map.

### Later party and leader mapping

Confirmed in current source:
- Park is the 1970 incumbent and appears in KOR's slot-22 native pool.
- Slot 22 includes Chun Doo-hwan as a later military leader.
- No Roh Tae-woo declaration was found in KOR native pools or history in the searched source.
- Native pools include Kim Young-sam in slot 1 and Kim Dae-jung in slot 3. mdcw_historical_retirement_alternatives.txt checks YS with ruling_party = 1 and DJ with ruling_party = 3.
- The 1970 registry has one NDP slot and a combined slot 2; there is no later DRP/RDP/DJP mapping or YS-vs-DJ party split. Chun's presence in the Army leader pool does not prove a new governing party is installed.

The 1980–1990 office/party route needs an explicit integration decision. Existing incumbent test shape is has_country_leader = { name = "Kim Young-sam" ruling_only = yes }; this tests the installed incumbent, not a candidate pool. Future Chun/Roh/YS/DJ divergence needs proper historical pools and party/outlook/slot integration or a real existing succession route. Do not invent party tokens from names or equate a leader pool with an office holder.

## Existing API and effect signatures

### Ideas, modifiers, parties and leaders

Target patterns include:
- add_ideas = idea_id and remove_ideas = idea_id
- add_dynamic_modifier = { modifier = id }, remove_dynamic_modifier = { modifier = id }, force_update_dynamic_modifier = yes
- party_popularity_increase = value followed by change_relative_party_popularity = yes in generic political helpers
- set_variable = { ruling_party = slot } in historical start
- has_country_leader = { name = "..." ruling_only = yes } for incumbent checks

Called directly from a focus these are country-scope effects unless explicitly wrapped in another tag/state scope. Modifiers must be registered and use supported fields with consumers; names/localization do not prove behavior. Generic party programmes are dynamic modifiers with enable conditions and variable-backed values. A false enable can disable a retained programme; do not assume party change removes it. Trace refresh and ownership for each new KOR modifier.

KOR's united_korea_modifiers maps custom variables such as UKOR_army_defence_var, UKOR_org_factor_var, UKOR_conscription_var and command variables. This is unified-Korea-specific, not a general South Korean focus API.

### Supported modifier categories with relevant consumers

Exact keys appearing in target/MD provider and consumer code include:
- Industry/building: industrial_capacity_factory, production_speed_buildings_factor, production_factory_max_efficiency_factor, construction_speed_factor.
- Military: army_attack_factor, army_defence_factor, army_core_defence_factor, army_org_factor, army_morale_factor, army_speed_factor, breakthrough_factor, training_time_army_factor, conscription, command_power_gain.
- Political order: stability_factor, political_power_gain, political_power_factor, party_popularity_stability_factor, drift_defence_factor and ideology-specific drift fields.
- Labour/skills: generic programmes define Imperia custom keys including literacy_rate_education_modifier, buildings_worker_requirement_modifier, productivity_growth_modifier and selected spending modifiers. Use only with registered definitions and actual consumers.
- Trade/influence: trade_opinion_factor, foreign_influence_defense_modifier and foreign_influence_modifier have definitions/readers. They do not conclude alliances, open inter-Korean talks or execute an agreement.

The KOR modifier file's unified-Korea variables are not a South-only bonus source. Generic party programme mappings show consumer patterns, not suggested KOR values. Verify each numeric field's definition and consumer before describing scale or units. Do not infer meaning from suffixes: the interest_rate_multiplier_modifier is read in the money system's own pre-clamp interest calculation.

### State ids and buildings

Target 1970 state IDs are 604 Gyeonggi (Seoul/capital), 605 Yeongnam, 606 Chungcheong, 607 Honam and 608 Jeju, present in target history/states. Before fixed-state construction verify owner, current level, slots and access/coast. Standard legal building types in installed MD/HOI4 include industrial_complex, infrastructure, arms_factory, air_base, anti_air_building, radar_station and dockyard where geography/slots allow. These IDs are anchors, not proof of capacity or building suitability. The donor 05_south_korea.txt uses the standard add_building_construction effect with a type and level. Direct state construction can represent regional investment; don't add unconsumed state-development variables.

## Economy, costs, development and debt

### One-time costs

The Imperia economy stores country variables including treasury, debt, treasury_rate, additional_expenses_rate and additional_income_rate. Monetary effect arguments are in billions of dollars. Use the supported treasury/accounting path already used in target and show the same amount in the focus tooltip. The project contract's paid-action calibration is $1–10bn scaled by importance and benefit; it is not a fee mandate for every focus. Native borrowing may let spending overdraw treasury. Do not manipulate debt directly as a focus-price shortcut.

Scripted budget literals must have no more than five fractional digits.

### Recurring costs

00_money_system.txt documents the active weekly economy. calculate_additional_expense_rate resets and rebuilds additional_expenses_rate, then passes the total into weekly treasury accounting. Existing examples add total_subsidies_out, named weekly costs, lease costs and COLDWAR_nuclear_development_weekly_cost. Recurring police, military, education or industrial programme costs should contribute to this consumed weekly rate and be described in weekly MD units. Convert source budgets before integration. For conditional programmes document owner and termination/refresh behavior.

### Development and debt

mdcw_imperia_development_effects.txt runs imp_eco_progress_calc. It classifies countries via IMP_developed_productivity_level / IMP_emerging_productivity_level, assigns imp_eco_1/2/3_dynamic_modifier and calculates variables for economy/workforce readers. mdcw_imperia_development_dynamic_modifiers.txt binds those modifiers to calculated variables. This is shared progression, not a direct KOR policy reward. Raising overall_productivity or forcing a tier via focus may interfere with progression or trigger nonlinear recalculation; do not use without auditing all readers and refresh paths.

IMP_1970_gdp_scripted_effects.txt is a scenario economy initializer, not a recurring focus reward. Do not replay start initialization from a focus. mdcw_imperia_debt_effects.txt contains event dispatch helpers; debt, interest, rates and restructuring are handled by 00_money_system.txt. No KOR-specific reusable debt-grant helper was identified. Avoid direct debt assignment because it bypasses accounting/interest behavior.

## Choice families

| Concept | Existing route | Cost/trade-off route | Limit |
|---|---|---|---|
| Export-led growth / heavy-chemical industry | State construction, industrial capacity/construction and supported productivity-programme fields | One-time treasury spend; supported worker/stability or debt/interest consequences | No free “chaebol” key unless registered and consumed. |
| ROK-US readiness / reserve forces | Native army, training, command and conscription modifiers; actual defence spending system | Recurring defence cost in weekly MD units; manpower/industry opportunity cost | Modifiers do not spawn units. |
| Yushin/emergency rule/KCIA | Supported stability/war support/police law, party/outlook shift, or custom modifier with proven reader | Opposition legitimacy, stability/PP/popularity or weekly police cost if consumed | No universal existing repression helper; slot 7 remains a power bloc, not ruler. |
| Labour discipline / overseas employment | KOR starts with mdcw_ni_overseas_employment_programme; target has guest-worker/remittance integrations and worker/productivity/spending fields | Weekly labour/administrative cost or consent contract; social/regional trade-off | Trace existing idea and finance consumer; do not add a parallel remittance system. |
| Labour rights / rural modernization | Political, education, literacy/productivity and construction systems | Treasury cost; opposition trade-off through supported party model | Elections, ruling party and popularity are separate state. |
| Inter-Korean diplomacy | NKO Korean-channel/confederation contract with recipient events | Recipient consent and response-specific effects | No symmetric KOR helper was confirmed here; do not auto-accept. |

KCIA is slot 7 power bloc. An idea labelled KCIA without a consumed modifier is cosmetic. Relation modifiers do not replace an event consent contract. Nuclear content should use existing eligibility, safeguards, technology and project budget.

## North Korean diplomatic hooks

COLDWAR_NKO_1970_focus.txt contains a Korean-channel route and COLDWAR_NKO_confederation_offer focus. The offer checks channel status and independent KOR, displays a preview separately from hidden completion, and calls COLDWAR_NKO_complete_confederation_offer in COLDWAR_NKO_1970_focus_effects.txt. events/COLDWAR_NKO_1970_foreign_events.txt has recipient events/terms. A separate NKO armed-reunification focus creates a KOR wargoal under its guards.

This is an NKO-side framework, not proof of a symmetric KOR-initiated offer or fully symmetric response. Before implementation, trace current event IDs/options, acceptance/refusal, payer/recipient, pending/cleanup flags and retry behavior. KOR needs a reachable consent path; proposal is not acceptance.

## Nuclear integration

COLDWAR_nuclear_power_effects.txt has generic initialization and player-programme helpers. COLDWAR_nuclear_development_budget.txt prices active nuclear special projects and enrichment upkeep into a weekly rate consumed by the economy. KOR should use existing technology, safeguards and project guards. This does not justify a free weapon or a KOR-specific exception without reviewing diplomacy, AI and eligibility.

## New KOR helpers versus shared APIs

New South Korean content would include COLDWAR_KOR_1970_complete_* helpers, their once-only flags, KOR-only programme modifiers, a dated 1970–1990 election/succession dispatcher, a KOR response contract for NKO's offer, or new modifiers for Yushin/KCIA/chaebol/labour policy.

Existing shared APIs include standard ideas/dynamic modifiers, force_update_dynamic_modifier, variable/array effects, state construction, incumbent triggers, supported national modifier fields, economy rate accounting and NKO foreign offer/events. Each new modifier needs a registered definition, proven consumer, ownership/cleanup or enable condition, truthful tooltip and once-only guard as appropriate. Custom script follows project marker convention and UTF-8 without BOM.

## Feasibility recommendations

1. Route the target's 1970 setup to the new KOR tree while preserving Jan 1970 ruling_party = 0 reachability and any required non-1970 donor routing.
2. Organize politics around actual roles: Park/DRP, NDP opposition, Forties challenge, USP/left and military succession. Do not make KCIA/Army/EPB/student blocs ordinary governing parties without registry support.
3. Resolve 1980s party/leader representation before leader-locked rewards. Chun exists in the military pool; Roh was not found; later party mapping is absent.
4. Use treasury in billions for one-time spending and weekly rates for recurring programmes; keep script literals to at most five fractional digits and show numeric effects.
5. Use confirmed state construction or modifiers with identified readers. Separate permanent gains from active-party programmes.
6. Preserve KOR/NKO consent and nuclear eligibility/safeguards/project rules.

## Runtime validation still required

- Start a new 1 January 1970 campaign; verify loaded KOR tree, Park, party/ruling slot, coalition and programme state.
- Parser/load-check new scripts/localization; verify scopes and real modifier consumers.
- Hover available/unavailable focuses; compare preview, guards, payout and weekly costs. Check treasury after an economy tick.
- Exercise Park-to-Chun and intended opposition routes, programme shutdown/reactivation, and separately resolved Roh/YS/DJ successors.
- Send/accept/refuse KOR/NKO proposals as both tags; check payment, effects, reply, retry and cleanup in multiplayer.
- Test state capacity/ownership and nuclear safeguards/budget in a fresh game process. Static inspection cannot prove tooltip rendering, scope behavior, engine loading or save behavior.

## Key source anchors

Line numbers are from the audited checkout and should be rechecked if source is regenerated.

- Target KOR 1970 start: history/countries/KOR - Korea.txt:5 (snapshot), :32 (ruling slot 0), :33 (coalition slot 13), :35–39 (Park incumbent), :45 (generic focus tree), :46–47 (starting economic variables), :54 (overseas-employment idea).
- Registry taxonomy: tools/party_registry_1970/data/KOR.json (slot records and owner notes); KOR generated leader routing is common/scripted_effects/KOR_political_leaders.txt:1–15; KOR leader pools are common/scripted_effects/mdcw_historical_native_pools.txt:6904 onward; current YS/DJ incumbent alternatives are common/scripted_triggers/mdcw_historical_retirement_alternatives.txt:92–93; Park/Chun incumbent alternatives appear in native pools near :16287–16297.
- KOR custom modifier ownership: common/dynamic_modifiers/99_KOR_dynamic_modifiers.txt:1–29 for unified_korea_modifiers and its UKOR_* variable mapping. Generic 1970 party programme field examples and enable conditions are common/dynamic_modifiers/mdcw_1970_generic_party_programmes.txt.
- Economy weekly cost accumulation: common/scripted_effects/00_money_system.txt:3664–3681 defines calculate_additional_expense_rate, resets additional_expenses_rate at :3666 and then accumulates named costs; the weekly income/expense balance is written into treasury_rate around :4710. Nuclear project weekly costing is common/scripted_effects/COLDWAR_nuclear_development_budget.txt:6 onward.
- Development lifecycle: common/scripted_effects/mdcw_imperia_development_effects.txt:2 onward; debt event dispatch: common/scripted_effects/mdcw_imperia_debt_effects.txt:2 onward.
- NKO confederation offer: common/national_focus/COLDWAR_NKO_1970_focus.txt:2116–2141 (guards, recipient independent check, preview and hidden helper); common/scripted_effects/COLDWAR_NKO_1970_focus_effects.txt:1155–1163 (once-only offer helper); recipient-side contract is in events/COLDWAR_NKO_1970_foreign_events.txt.
- Target KOR state geography: history/states/604-Gyeonggi.txt through 608-Jeju.txt; installed donor building-effect examples are in workshop common/national_focus/05_south_korea.txt around the industrial-complex focuses.

## Party-bound programme lifecycle precedents

These country analogues illustrate three different ownership models; choose one deliberately for KOR rather than copying their keys wholesale.

- Vietnam (common/dynamic_modifiers/COLDWAR_VIE_1970_dynamic_modifiers.txt:26 onward) binds personal programmes to the actual incumbent via enable = { ... has_country_leader = { name = "Le Duan" ruling_only = yes } } (and equivalents for Truong Chinh, Nguyen Van Linh and Vo Van Kiet). Party programmes separately gate on the real outlook/subparty triggers. common/on_actions/COLDWAR_VIE_1970_on_actions.txt calls COLDWAR_VIE_sync_programmes from recurring update paths. This pattern leaves modifier ownership explicit and changes active effects when the actual leader/government changes.
- Soviet Union (common/scripted_effects/COLDWAR_SOV_1970_scripted_effects.txt:382 onward) has COLDWAR_SOV_clear_gensec and installer effects for each leadership choice. Installers clear previous leadership choices before granting the next, and generated monthly/transition handling calls the installer. This is explicit replacement, useful when only one programme may be active; permanent accumulated sector gains are managed separately and should not be wiped with office changes.
- West Germany's 1970 dynamic modifiers include persistent state/route modifiers and programme/assistance helpers; its scripted effects calculate government/parliament state and dated succession through real party and coalition arrays. It is not a generic rule that every modifier is party-bound. Keep once-earned permanent history separate from current leadership bonuses; party switching alone should not erase permanent outcomes.
- The target's generic party programmes and Vietnam demonstrate dynamic modifier enable-gating, while Soviet clear/install demonstrates explicit replacement. For KOR, decide whether a reward is permanent (retain it) or an active-party programme (disable/remove/replace it). Verify its grant, refresh and reverse-transition paths; no automatic cleanup can be inferred merely from the party changing.


### Custom modifier definition units (verified)

The target's custom definitions establish these display units and scopes exactly:

| Modifier key | Definition | Scope / tooltip value | Source |
|---|---|---|---|
| foreign_influence_defense_modifier | percentage, 2 precision | country | common/modifier_definitions/influence_modifier_definitions.txt:1–6 |
| foreign_influence_modifier | percentage, 2 precision | country | common/modifier_definitions/influence_modifier_definitions.txt:8–13 |
| literacy_rate_education_modifier | percentage, 2 precision | country | common/modifier_definitions/modifier_definitions.txt:72–77 |
| productivity_growth_modifier | number, 3 precision; definition comment says monthly overall-productivity growth and warns to keep it small | country | common/modifier_definitions/money_modifier_definitions.txt:410–416 |
| buildings_worker_requirement_modifier | percentage, 2 precision | country | common/modifier_definitions/money_modifier_definitions.txt:466–472 |
| investment_cost_modifier / receiving_investment_cost_modifier | percentage, 2 precision | country | common/modifier_definitions/money_modifier_definitions.txt around :50–70 |

These values describe modifier-definition/tool-tip presentation, not an independently verified numeric benefit for KOR. `modifier@key` reads a country modifier token; definition registration alone still does not prove the field is consumed. The referenced economy/influence readers and the generic programme definitions supply that second half. For state construction, donor focus patterns use `add_building_construction = { type = industrial_complex level = N }` within state scope; the country tree must explicitly enter the intended state or select a valid state before invoking it. Numeric level is building levels, not money.
