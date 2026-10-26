# COLDWAR UAE / Trucial States — mechanics audit

Scope: concept and approval preview only. No loaded gameplay files were edited. Audit performed against the supplied MD install and the current Cold War workspace on 2026-10-19. This is source verification, not an HOI4 runtime test.

Source roots:

- `MD`: `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`
- `CW`: `C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar`

## Critical conclusions

1. Use the existing `UAE` tag and `UAE_TRUCIAL_1970` cosmetic identity. The 1970 government is nationalist outlook / Monarchist subparty, array index **23**, not the native 2000 Western Autocracy index 0.
2. The historical start already loads `mdcw_1970_generic_focus`, recruits the Trucial States Council and defers all starting armies. Replace the focus assignment only after concept approval. Do not spawn a modern army through the concept.
3. The authored 1970 GDP target is **0.686 billion** and productivity is **582.8**. Gulf 2000 costs of 9.375–50 billion are useful examples of syntax and reward composition, not acceptable unchanged UAE 1970 prices.
4. Native Gulf spirits are mechanically useful references but several have 2000-specific cleanup and modern values. Write `COLDWAR_UAE_...` spirits; do not simply add the 2000 list.
5. Permanent national gains, active-government programmes and temporary reform burdens need separate ownership. Party-bound programmes can deactivate and return while earned variables remain; one-time buildings, money and research grants must never run during resynchronization.
6. Imperia oil prices, sanctions and investment caps are active systems. Extend their supported modifiers and decisions rather than creating parallel oil-price or sanction systems.
7. A tooltip or named proposed helper is not an executable reward. New helpers in the concept must be labelled proposed wrappers around the verified leaf APIs below.

## Actual January 1970 setup and scenario caveats

| Fact | Current source |
|---|---|
| Country tag UAE; capital state 180; generic Cold War focus; GDP/capita 2.394; productivity 582.800; Monarchist profile; cosmetic tag; council character | CW `history/countries/UAE - United Arab Emirates.txt:1–21` |
| Empty land/naval/air OOBs explicitly deferred by user decision | Same file, lines 23–26 |
| Monarchist profile = nationalist 60%, ruling subparty 23; subparty shares initialized; no elections | CW `common/scripted_effects/IMP_1970_world_politics_effects.txt:237–256` |
| Startup council leader, Monarchist, expiry 1971.12.2 | Same file, lines 588–592; CW `common/characters/mdcw_gulf_1970.txt:58–69` |
| British puppet relation configured at world setup | CW `common/scripted_effects/IMP_1970_world_politics_effects.txt:1226–1232` |
| GDP target 0.686 | CW `common/scripted_effects/IMP_1970_gdp_scripted_effects.txt:1812` |
| Two UAE states: Dubai 179 and Abu Dhabi 180 | CW `history/states/179-Dubai.txt:2,11,42–67`; `history/states/180-Abu Dhabi.txt:2,11,49–68` |
| 1970 state productivity: Dubai 589.477, Abu Dhabi 564.093 | Same state files, lines 46 and 53 |
| Authored buildings: Dubai 1 office, 0 arms/airbase, 0 new sectors; Abu Dhabi 1 arms, 0 civilian, fossil reset for rebuild | Same state files |
| Base resources are still present (Dubai oil 7; Abu Dhabi oil 40) | Same state files, resources blocks |
| Native 2000 economy, GCC, WTO, League, rentier and expatriate spirits are inside 2000.1.1, not 1970 | Country history from line 29 onward |

The state files also retain inherited base infrastructure, bases and other fields. World initialization subsequently recalculates sectors. Do not claim an exact final treasury, debt, electrical surplus or full building inventory from country history alone. Confirm those in a fresh campaign when implementation is approved.

The map represents the seven emirates through only two states. “Northern emirate” projects can target Dubai state 179, but independent northern-emirate annexations or state transfers would require additional map/tag design. Do not advertise those as existing leaf mechanics.

The council's expiry is data, not a complete demonstrated federal formation/succession chain. A new focus/event needs to install the chosen post-formation leader explicitly through the project’s political system. The existing native political leader pool already contains Council → Rashid → Zayed under `Monarchist_leader` 0/1/2 in CW `common/scripted_effects/mdcw_historical_native_pools.txt:12628–12711`; it must not be invoked blindly for a focus that promises a specific ruler.

## Exact party gates and slots

All gates below are native scripted triggers in CW `common/scripted_triggers/01_political_triggers.txt`. They check the actual `ruling_party` variable; outlook alone is insufficient.

| Intended programme | Exact gate | Slot | Source line |
|---|---|---:|---:|
| Western autocratic modernization | `western_autocrats_are_in_power` | 0 | 58 |
| Western conservative parliamentary route | `western_conservatism_are_in_power` | 1 | 176 |
| Communist state | `emerging_communist_state_are_in_power` | 4 | 197 |
| Emerging autocratic / Arab authoritarian | `emerging_autocracy_are_in_power` | 7 | 218 |
| Moderate Shia | `emerging_moderate_shiite_are_in_power` | 8 | 225 |
| Salafist kingdom | `salafist_kingdom_are_in_power` | 10 | 239 |
| Salafist caliphate | `salafist_caliphate_are_in_power` | 11 | 246 |
| Muslim Brotherhood / Islah | `neutrality_neutral_muslim_brotherhood_are_in_power` | 12 | 253 |
| Neutral autocratic | `neutrality_neutral_autocracy_are_in_power` | 13 | 260 |
| Neutral conservative | `neutrality_neutral_conservatism_are_in_power` | 14 | 267 |
| Neutral oligarchic merchant politics | `neutrality_neutral_oligarch_are_in_power` | 15 | 274 |
| Neutral social / Arab socialist | `neutrality_neutral_social_are_in_power` | 18 | 295 |
| Neutral communist | `neutrality_neutral_communism_are_in_power` | 19 | 302 |
| Nationalist junta | `nationalist_military_junta_are_in_power` | 22 | 323 |
| Historical dynastic federation | `nationalist_monarchists_are_in_power` | 23 | 330 |

The existence of a slot does not establish a historically meaningful UAE movement or named leader for that slot. Historical research must decide which branches deserve content. Do not invent a party array index for an unrepresented movement.

## Supported executable reward leaves

| Leaf API | Required input / scope | Actual result / caveat | Evidence |
|---|---|---|---|
| `modify_treasury_effect = yes` | country; `set_temp_variable = { treasury_change = ... }` | Adds the signed value to treasury, marks money dirty; native tooltip. Amounts use MD billions, including small decimals. Does not establish affordability by itself. | CW `common/scripted_effects/00_budget_effects.txt:1482–1497` |
| `modify_debt_effect = yes` | country; `debt_change` | Adds signed debt; clamps debt to zero; native tooltip. Treasury transfer is separate. | Same file, 1495–1505 |
| `flat_productivity_change_effect = yes` | country; `temp_productivity_change` | Adds productivity points to **every controlled state**, clamps minimum 100, recalculates economy. It is not a percentage. | CW `common/scripted_effects/00_economic_system_utilities.txt:2–9` |
| `state_flat_productivity_change_effect = yes` | state; `temp_productivity_change` | Adds productivity points to that state and recalculates controller. | Same file, 11–21 |
| `add_building_construction` | owned, controlled state; `type`, `level`; optional `instant_build = yes` | Native construction. With no instant flag it joins construction. Match narrative to queued/completed status. Check free levels/slots first. | MD `common/national_focus/00_generic.txt:3079–3093`; MD Russia 3983–4024 |
| `add_extra_state_shared_building_slots` | state | Extra shared slots; not free labor, energy or infrastructure. | MD Generic 3082 |
| `add_resource = { type = oil amount = N }` | state | Adds map resource units, not money or barrels/day. Owned-state selection should be deterministic for UAE. | MD `common/national_focus/gulf.txt:70–84` |
| `add_tech_bonus` | country; name, bonus, uses, actual technology category | One or more discounted research uses. A 0.25 bonus is a native +25% research bonus; does not grant the technology. | MD Russia `SOV_aero_improvements`, 13301–13306 |
| `add_doctrine_cost_reduction` | country; name, cost_reduction, uses, category | Doctrine-cost reduction, distinct from tech research. | CW `common/national_focus/turkey.txt:3189–3194` |
| `add_stability`, `add_war_support`, army/navy/air XP | country | Native one-time effects; use as secondary thematic effects, not the sole industrial payoff. | MD Russia `SOV_npp_again`, 3934; native country trees throughout |
| `add_opinion_modifier` | target country + existing opinion modifier | Opinion; not permission or acceptance of an agreement. Bilateral material rewards require recipient choice. | MD Gulf and Russia; existing project Gulf agreements |

For funded decisions, proposed design wrapper should: freeze amount from current GDP at offer/start; verify treasury and actual construction feasibility; pay exactly once on recipient acceptance or project start; mark paid/consumed state; grant exactly once; define failure/retry behavior; show native numeric amounts. A focus unlocking an offer is not acceptance.

At GDP 0.686, 1% = 0.00686 billion, 3% = 0.02058 billion, 5% = 0.03430 billion, 10% = 0.06860 billion. These are arithmetic examples, not historical estimates. A whole free factory for 1–3% of that initial GDP would be grossly underpriced compared with the native factory scale; use construction bonuses/slots/productivity for small projects or substantial staged funding for major physical buildings.

## Verified modifier palette and units

Values below are illustrative **design ranges**, not approved balance. They are intentionally smaller than a superpower's whole-programme rewards. Persistent rewards belong in an idea or registered dynamic modifier; changing an unbound variable alone gives no benefit.

| Exact key | Correct interpretation | Plausible concept magnitude / counterweight | Registration and consuming evidence |
|---|---|---|---|
| `productivity_growth_modifier` | Flat productivity growth input, not percent. CW country display multiplies by 0.5 then applies country growth multiplier; state catch-up further changes result. Do not promise an invariant realized monthly increase. | +0.10 to +0.40 per substantial education/management programme; budget burden | CW `common/modifier_definitions/money_modifier_definitions.txt:409–415`; `common/scripted_effects/00_productivity_effects.txt:61–86` |
| `country_productivity_growth_modifier` | Percentage multiplier on positive growth input; clamped nonnegative in CW reader | +0.05 to +0.15; workforce or spending cost | Same definitions:515; productivity reader:79 |
| `civilian_factories_productivity` | Percentage increase to civilian-sector productivity/tax and GDP components; not simply vanilla construction speed | +0.05 to +0.15; energy/labor demand | Definitions:381; money reader:452–469 and 5915 |
| `military_factories_productivity` | Percentage military-sector productivity/tax and GDP components; use actual output modifier separately if promising weapon production | +0.05 to +0.10; procurement cost | Definitions:388; money reader:476–490 and 5922 |
| `offices_productivity` | Percentage office-sector productivity in office tax and GDP components | +0.05 to +0.15 for trade/services; exposure/cost | Definitions:402; money reader:525 and 5936 |
| `buildings_worker_requirement_modifier` | Multiplies building labor requirements by 1+modifier, floor 0.10; negative saves workers | -0.05 to -0.10; education cost | Definitions:466; money reader:5283 and other sectors |
| `total_workforce_modifier` | Workforce is population ×0.6×clamp(1+modifier,0,1.5). +0.05 increases modeled workforce by 5%, not five population-share points. | +0.05 to +0.15 immigration/participation; housing/social burden | Definitions:473; money reader:5138–5153 |
| `oil_export_multiplier_modifier` | Additive oil-export revenue multiplier. Base includes general resource modifier; revenue = exported units × price × multiplier × weekly conversion | +0.05 to +0.15 contracts/processing; rentier cost or foreign leverage | Definitions:121; money reader:4505–4530 |
| `office_park_income_tax_modifier` | Modifier to the office-sector tax calculation, not a universal corporate tax rate | +0.05 to +0.10; infrastructure cost | Definitions:268; money reader:522 |
| `education_cost_multiplier_modifier` | Additive percentage to education spending multiplier; 1+modifier+research slot modifier, then common money scaling | +0.05 to +0.15 as recurring programme burden; do not label as annual GDP cost | Definitions:65; money reader:3373–3376 |
| `bureaucracy_cost_multiplier_modifier` | Percentage spending multiplier | +0.05 to +0.15 federal ministry cost or -0.05 administrative reform | Definitions:51; money reader:3310 |
| `army_personnel_cost_multiplier_modifier` | Percentage to personnel cost multiplier | +0.05 to +0.15 professional-force cost, paired with org/training | Definitions:23; money reader:3183 |
| `equipment_cost_multiplier_modifier` | Percentage military equipment expense multiplier | +0.05 to +0.15 imported sophisticated arms; -0.05 standardization | Definitions:44; money reader:3187 |
| `interest_rate_multiplier_modifier` | **Additive percentage points** to annual interest rate before clamp 0.8–50, despite key name. Zero debt bypasses interest. | -0.25 to -0.50 percentage points credit reform, with fiscal tradeoff | Definitions:9; money reader:2524–2582, especially 2559 |
| `energy_use_multiplier` | Percentage aggregate energy-use multiplier, 1+value | -0.05 to -0.10 conservation; investment cost | CW `common/modifier_definitions/energy_modifier_definitions.txt:58`; `common/scripted_effects/!_energy_effects.txt:188` |
| `fossil_pp_energy_generation_modifier` | Percentage fossil power output multiplier | +0.10 to +0.20 gas plants; fuel dependency/expense | energy definitions; energy effects:366 |
| `energy_gain_multiplier` | Percentage overall energy generation multiplier | +0.05 to +0.10 grid modernization | energy effects:312 |
| `imp_oil_price_resistance` | Subtracts from modeled consumer oil dependency, which is clamped 0.2–1. Does **not** eliminate exposure of oil export income | +0.025 to +0.10 conservation/diversification; capital cost | CW `common/modifier_definitions/imp_oil_prices_modifiers.txt:1`; `common/scripted_effects/imp_oil_prices_scripted_effects.txt:99–121` |
| `imp_sanction_resistance` | Multiplies relevant sanction severity by 1−modifier before severity clamp; not diplomatic immunity | +0.05 to +0.15 diversification; weaker access to patron support | CW `common/modifier_definitions/mdcw_imperia_globalism_modifiers.txt:21`; `common/scripted_effects/imp_sanctions_effects.txt:130–148` |
| `imp_investment_in_extra` | Flat extra concurrent inward investment capacity. Base is 3 for UAE GDP band. A +1 is substantial | +1 late trade hub; oversight/corporate tax cost | Same definitions:15; CW `common/scripted_effects/imp_minis_effects.txt:6–49` |
| `production_speed_buildings_factor` | Native percentage construction modifier; employment/productivity overlays still apply | +0.05 to +0.10; capacity/labor/debt burden | Native Gulf ideas `arab_spirits.txt:228–263`; productivity output reader `00_productivity_effects.txt:89+` |
| `research_speed_factor` | Native percentage research speed | +0.03 to +0.08 programme; education cost | MD Russia `SOV_npp_again`:3941 via mapped modifier |
| `army_org_factor`, `training_time_factor`, `supply_consumption_factor` | Native percentage military modifiers | +0.05 organization; -0.05 training time; realistic higher personnel cost | CW Soviet dynamic modifiers:92–110; native MD military ideas |
| `foreign_influence_modifier` | Used by native influence and political manipulation calculations; consumer-specific clamps and branch logic exist. Do not promise a universal +N% influence on all actions | +0.05 to +0.10 diplomacy if exact action trace confirms its effect | Definitions `influence_modifier_definitions.txt:8`; influence effects:255,264,1106 |

`corruption_cost_factor` is used by native Gulf spirits and Soviet programmes but its exact current consumer/formula was not established in this bounded pass. It may be included as a native known modifier only with explicit final formula verification; do not describe a value as a guaranteed income loss without that trace.

## Native MD numerical and presentation references

| Reference focus | Duration field | Bundle | Gate / caution |
|---|---:|---|---|
| Generic `GENERIC_productivity_measures` | cost 7.86 (~55 nominal days at 7 days/cost) | +25 productivity points to controlled states; treasury −3% current GDP | Productivity-targeted autarky branch; MD `00_generic.txt:2135–2154` |
| Generic `GENERIC_improved_worker_productivity` | 7.86 | Spirit: −10% building worker requirements; +0.50 flat productivity-growth input | Mutually exclusive with manpower solution; focus 2171–2187, CW matching idea `generic_ideas.txt:219–226` |
| Generic `GENERIC_energy_sector` | 10 (~70 days) | −10.5 treasury; extra capital slot; fossil and renewable construction | Parent working-class branch; MD Generic:3063–3093 |
| Generic `GENERIC_fossil_powerplant` | 10 | −2 treasury; extra slot and fossil construction; +5 fossil industry opinion | Exclusive renewable alternative; MD Generic:3106–3137 |
| Generic `GENERIC_debt_refactoring` | Read current block before copying | +5% current debt (max 100); timed interest −1 percentage point and PP factor −5% | Debt/GDP >50 gate; focus 2412–2436; idea 284–291 |
| Russia `SOV_npp_again` | 7 (~49 days) | +16 stability; −20 treasury; +3% bureau costs; +5% arms factory construction; +7% education cost; +10% research; +5% offices construction; +5% health cost; +0.03 population growth input | Requires npp and one of actual party gates; MD Russia:3908–3946 |
| Russia `SOV_aero_improvements` | 3 (~21 days) | −3 treasury; one 25% aircraft research bonus; −10% air accidents; party side effect conditional | Communist/neutral communist + UAC gate; MD Russia:13268–13310 |
| Gulf `GCC_expand_oil_extraction` | 8.58 (~60 days) | Non-SAU −9.375 treasury, +10 oil in random owned state; SAU twice reward/cost | MD Gulf:55–87. Use deterministic UAE state, substantially rescale cost. |
| Gulf `GCC_empower_the_mutaween` vs `GCC_weaken_the_mutaween` | 6.45 (~45 days) | ±10 government social conservatism; ±5 religious faction opinions; different decisions | MD Gulf:2080–2144. UAE historical route must not copy Saudi institutional narrative. |
| Turkey `TUR_the_soldiers` | 7.15 (~50 days) | one 100% infantry research bonus + one 50% land doctrine-cost reduction | CW Turkey:3168–3194. Small professional military programme need not copy both at full magnitude. |

These are reference bundles, not UAE reward budgets. Source cost values are exact; calendar durations are nominal approximations and can be affected by the scenario.

Native presentation pattern: named programme heading, numeric variable delta with correct tooltip, actual construction/research leaf, visible treasury debit, and short national narrative. Avoid replacing effects with a prose list.

## Imperia / Cold War integration details

- **Oil prices are active in 1970.** CW `common/on_actions/zzzzzz_imp_oil_prices_on_actions.txt:6–43` initializes internal price 75, displayed 1970 conversion 0.024 (= $1.80), installs country oil dynamic modifiers, and recalculates dependency monthly. Weekly price changes use the existing world equilibrium.
- **Two different oil exposures:** `imp_oil_price_resistance` protects modeled consumer costs; oil export receipts still depend on actual exported oil and price. A non-oil development branch should improve offices/civilian economy and reform the rentier spirit instead of calling consumer protection “the end of oil dependence.”
- **Existing OPEC restraint debit:** CW `00_money_system.txt:4517–4521` subtracts 0.1 from oil export multiplier under `mdcw_cw_opec_supply_restraint`. Do not add a duplicate identical debit in a new spirit.
- **Investment capacity:** `imp_set_investment_caps` gives base 3 inward/outward slots below GDP 1000, then adds extra modifiers. The focus may unlock a decision to use native investment; a flag/tooltip alone does not create an actual foreign project.
- **Sanctions:** source proves resistance modifier arithmetic. Counterparties must retain refusal in multiplayer diplomatic agreements. Do not grant a bilateral factory or cash transfer merely because UAE completes “Offer Partnership.”
- **Recipient-controlled agreement example:** CW `common/scripted_effects/COLDWAR_IRQ_gulf_effects.txt:413–480` and matching triggers explicitly reserve UAE offer state, check payer treasury, apply one-time acceptance and repayment. This is a project integration example, not automatic approval to reuse its exact 4% Iraqi GDP price or political assumptions.

## Starting spirits that can be built using verified keys

Proposed values require aggregate balance review. Each should clearly show both sides; total starting load must remain playable alongside existing weak productivity, workforce and subject status.

| Proposed COLDWAR spirit | Appropriate supported effects | Removal / evolution |
|---|---|---|
| `COLDWAR_UAE_seven_rulers_one_coast` | −10% PP factor, −5% construction; +5% ideological defense if verified; avoid permanent duplicate puppet penalties | Union compromise focus replaces with council/federal settlement version |
| `COLDWAR_UAE_uneven_oil_prosperity` | +10% oil-export revenue multiplier; −10% country productivity growth multiplier; optional budget/federal sharing burden | ADNOC/revenue sharing/merchant diversification each changes a different component |
| `COLDWAR_UAE_scarce_citizen_workforce` | −10% total workforce; +5% personnel cost | Immigration or citizen training paths reduce different parts; never use 2000 millions of migrant removals |
| `COLDWAR_UAE_imported_expertise` | +5% construction; +10% equipment/administrative or education cost chosen by programme | Technical institutes/emiratization change modifier rather than delete productive benefits blindly |
| `COLDWAR_UAE_scattered_administration` | +10% bureaucracy cost; −5% research or construction | Common ministries/loose union choose more integration vs more local autonomy |
| `COLDWAR_UAE_water_and_power_constraints` | +10% energy use (demand burden) and −5% construction; no fictional water-resource modifier | Desalination represented by actual energy cost, plant/grid construction and productivity relief |
| `COLDWAR_UAE_british_security_umbrella` | Reuse actual subject relation; optional personnel/procurement trade-off only if not double-counting subject mechanics | Independence agreement changes relation and temporary transition burden; no automatic modern divisions |

Do not stack all illustrative penalties without a full start budget. This section establishes achievable mechanical representation, not a requirement for seven separate spirits.

Native `rentier_state` is a warning against direct reuse: `arab_spirits.txt:72–97` has a `date > 2000.1.2` cancellation condition and duplicate construction modifier declarations. Native `uae_expat` at 254–264 is calibrated to the modern UAE, with −2.2 percentage-point conscription and +1.1 population growth input. Its 2000 population assumptions are not a 1970 recommendation.

## Government programme lifecycle

Use native `available` party triggers on each programme focus, plus `cancel_if_invalid = yes` / `continue_if_invalid = no` as verified against actual native focus defaults when emitted. Do not add a ceremony focus before the already-ruling monarchy may use its own programme.

Recommended state ownership:

1. **Permanent state/national capital:** completed focuses, buildings, resource units, research bonus uses and one-time cash are executed once in completion/accepted-event code. They survive government turnover.
2. **Earned programme values:** keep separate `COLDWAR_UAE_<programme>_<modifier>` variables. Focuses increase these once.
3. **Active programme:** attach a dynamic modifier whose `enable` checks `original_tag = UAE`, actual ruling-party trigger and any real leader flag. Its modifier fields map earned variables. False enable deactivates it while progress stays stored; returning government can restore the same earned programme.
4. **Temporary burden:** timed idea with explicit duration, or a project-running flag and matching cleanup. A party change must not erase already-owed public debt or refund a completed national project.
5. **Synchronization:** ensure the applicable dynamic modifier is present; do not execute completion_reward again. Existing government-change lifecycle should call only this idempotent synchronization. Periodic fallback is acceptable only if needed; no global world-economy refresh after every tiny focus.

Working architecture reference: CW `common/dynamic_modifiers/COLDWAR_SOV_1970_dynamic_modifiers.txt:183–265` uses exact ruling-party and office gates, with mapped earned variables. This is an existing source pattern, not a demonstrated UAE engine test.

Do not assume mutually exclusive focuses automatically erase old spirits or that switching outlook cleans variables. Explicit ownership prevents accumulating the benefits of every former government. Simultaneously completed programmes from the same party can stack only within the approved aggregate cap.

## Unsupported or still-unverified promises

- Fictional modifier names such as water_security, federal_cohesion, oil_dependency_reduction or tourism_income have no demonstrated reader. They may be visible scenario variables/decisions only after implementation of a real consumer.
- A proposed `COLDWAR_UAE_fund_project` helper is not currently installed. Its executable output must use the verified native leaves and transaction controls above.
- Universal “foreign influence +10%” wording is too broad: current native influence consumers have different formulas and clamps.
- “Increase employment +X%” is ambiguous. Use workforce participation, worker requirements, sector staffing or actual buildings with appropriate native modifier wording.
- Don't mix productivity points, growth input and growth percentages.
- Don't call interest_rate_multiplier_modifier −0.5 “−50% interest”; it is −0.5 annual percentage points before limits.
- Don't call oil map units barrels/day or money.
- Don't reuse 2000 mass-deportation manpower numbers in 1970.
- Don't grant research in an empty technology category. Final category-to-technology cross-check remains required for every emitted category.
- Foreign alliance/recognition/guarantee agreements require their actual country scopes and consent logic; an opinion modifier is not consent.
- Subject independence must use actual autonomy/diplomatic effects and fit the British world start; a cosmetic tag change does not release UAE.
- A spirit definition or custom modifier registration alone is insufficient proof; final selected keys without a traced reader remain provisional.

## Remaining checks at implementation

Exact catalogue leaf syntax/scopes, all definitions/consumers and subparty names; valid research categories and doctrines; building feasibility; total rewards along each playable route; no impossible AND joins of exclusive branches; true one-time and accepted-event transaction behavior; native tooltip hovers; current-government exit/return; save/reload; both multiplayer participants; fresh January 1970 initialization.

No gameplay implementation or HOI4 runtime verification has occurred in this audit.

