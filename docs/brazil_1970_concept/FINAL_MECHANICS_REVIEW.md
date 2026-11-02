# IMPERIA COLD WAR — Brazil 1970 final mechanics review

## Scope

Static mechanics review of `tools/brazil_1970_concept/content.py`, the exporter `tools/brazil_1970_concept/build.py`, and the generated `docs/brazil_1970_concept/concept.json`, checked against the local MD source and France 1970 fiscal precedent. No runtime code was changed and no game or parser test was run. This report separates verified native support from generation and integration requirements.

## Compiled concept snapshot

The reviewed JSON SHA-256 is `b776255f3eb24ddd132c5c713cdb6b412ac17a7a40bfc6b7a3c413e6225c8a1e`. It contains 224 focuses across 18 groups, 45 exclusive pairs, 14 recipient-approved offers, 8 starting spirits and 8 events. The generated static report records zero missing focus references, zero anchor mismatches and zero card collisions. These are concept/exporter checks, not HOI4 load or runtime validation.

The earlier state-map error is fixed in the compiled snapshot: Paraguay is state 895, and the display map names state 893 `Uruguay (Rio de la Plata)`. The concept now uses `foreign_influence_defense_modifier` rather than claiming that positive `foreign_influence_modifier` represents dependence. The 14 recipient tags are registered in the current country-tag file, including Angola as AGL. All building targets were checked against current state history: Brazilian targets are BRA-owned, Itaipu's Paraguay target 895 is PAR-owned, and the Uruguay office target 893 is URG-owned. Ownership at the current start is evidence only; runtime must recheck ownership and control.

The modifier keys in the JSON do not include `foreign_influence_modifier`. All 8 research categories are present in the installed technology files or are used by native `add_tech_bonus` examples. Every authored numeric budget/share literal is within the five-decimal project limit. Itaipu has a paired RP financial-support stream: `BRA` to `PAR`, annual share 0.08%, direction `expense` on Brazil and `income` on Paraguay. Preview rendering uses Brazil current GDP for both sides of that paired payment and each country's own GDP for its separate annual programme appropriation. The JSON contains setup costs, weekly appropriations, slot counts, building targets, research uses, modifier changes, XP and faction changes for both signatories; `PREVIEW.html` renders both complete prospective sides under “If they accept.” This verifies displayed data and preview code, not a native execution path.

The generated JSON now attaches an `execution_contract` to each focus. All 45 building rewards have a matching scope and state record with ownership, full-control, native building-type capacity and shared-capacity-after-slot checks. The transaction order records one receipt, setup debit, extra slots and construction in one guarded transaction. This resolves the earlier omission from the design data. The contract is still declarative and does not implement native HOI4 checks or effects.

## Reachable balance stacking

The four `BRA_idea_*` modifiers previously discussed are not in the 1970 start. In `history/countries/BRA - Brazil.txt`, the 1970 country-identity block ends around line 422; the four ideas are added in the dated `2000.1.1` block around lines 1243-1246. No 1970 activation of those four ideas was found in the inspected history or common scripts. Do not include their modifiers in the 1970 balance sum unless another scenario integration explicitly adds them.

Among the eight proposed concept starting spirits, the five stability effects sum to `stability_factor = -0.225`: AI-5 `-0.07`, wage squeeze `-0.05`, land inequality `-0.04`, urban pressure `-0.035`, and Amazon pressure `-0.03`. This is the direct sum of proposed modifier inputs, not an engine-measured stability result. It is a meaningful starting penalty and should be considered alongside any other approved 1970 starting modifiers when balancing.

A reachable military route is `military_0` -> either `military_1` or `military_2` -> `military_3` -> `military_4` -> `military_6` -> `military_7` -> `military_9`. `military_7` adds `+0.07` factory output and `+0.5` interest points. Before a remedy removes the proposed `miracle` spirit, the concept-only overlap is `+0.11` factory output (`+0.04` starting spirit plus `+0.07` focus) and `+1.0` interest points (`+0.5` spirit plus `+0.5` focus). The modern BRA ideas must not be added to this 1970 sum. Taking the economy `refinance` branch removes `miracle` and contributes `-0.4` interest points, so it changes that overlap; it is a real cross-branch alternative, not a separate free modifier.

The concept's event options and decisions use the same checked modifier, money, research, XP, building and faction-opinion kinds. Brazil's inspected 1970 initialization adds `the_military`, `industrial_conglomerates` and `landowners`; it does not add `farmers` or `labour_unions`, which appear only in the later dated history. The revised concept maps rural `farmers` DSL requests to the active `landowners` faction. Every faction effect records its `if_idea` condition; the preview says “If [faction] are active” before its numeric opinion change. This keeps absent-union changes conditional without changing the three installed 1970 factions. Native lowering still must honor the idea guard. Call the helper in the target country scope with signed `temp_opinion` immediately before it. `autocrats_opinion_change` copies this to `temp_opinion_change` and doubles positive values under recognized autocratic checks, including slot 22. The concept's `native_input_policy` records the requested final signed delta: halve a positive native input only inside an autocratic branch where the helper would double it; do not halve values for other governments or negative changes. The helper then clamps to modifier-adjusted faction bounds and refreshes its dynamic modifier. Brazil's military faction can therefore scale differently by ruling identity. The study decision gives only its stated fee and a finite nuclear-research bonus. It does not grant uranium resource production or a mine; the prospective `Surveyed deposit` and paid native mine-development conditions must remain real conditions in any implementation.

## Native lowering and execution guard proposal

The JSON effect names remain DSL records. Their concrete lowerings need an approved generator/runtime adapter. Minimum transaction contract:

```yaml
focus:
  availability: prerequisite focus checks + native broad party trigger + registered exact party identity where required
  visibility: keep all party groups visible; never use party-dependent allow_branch
  execution: repeat availability checks and a unique completion receipt before one-time rewards
  preview: render effects without calling any effect or changing variables
building_transaction:
  scope: recipient country scope for recipient buildings; Brazil scope for Brazil buildings
  state_checks: [state exists, state owner is current country, state controller is current country, free native capacity for amount]
  once_guard: same transaction receipt wraps slots and building construction
  effects_in_order: [add_extra_state_shared_building_slots equal to amount, add_building_construction for the named state and amount]
offer_acceptance:
  initiator: completing Brazilian focus only creates the offer
  recipient: named partner receives accept or decline decision
  acceptance_checks: [both tags exist, no bilateral war, no native embargo either direction, no mirrored Imperia diplomatic financial economic or military sanctions]
  once_guard: sign flag and acceptance receipt wrap both signatories' setup payments, buildings, finite awards and spirits
  recheck: ownership controller and native construction capacity for every state build at acceptance
  rejection_or_invalid_offer: no charges, buildings, spirits or finite awards
agreement_reconcile:
  active: valid signed agreement and all bilateral conditions remain true
  inactive: remove or suspend both named spirits and set both recurring streams to zero
  restore: reapply the same spirits and streams only; never replay setup fees, buildings, research, XP or other finite rewards
  dependent_offer: actual parent agreement spirit must be active in both offer availability and acceptance execution
weekly_transfer:
  source_scope: recalculate source current gdp_total * 0.0008 / 52 in each weekly refresh
  expense: add that exact value once to source additional_expenses_rate
  income: add that exact value once to target additional_income_rate
  reconciliation: same share, source, target and active receipt on both mirrored records
  preview: compute prospectively from current source GDP in both sides' effects
party_identity:
  required: exact installed subparty identity or explicitly approved formation identity, plus its real native outlook-slot trigger
  unresolved: later PDS PMDB PFL PT PDT later PTB PSDB PRN identities require registration; do not infer them from a shared slot
```

The building types and modifiers can lower to native effects, but there are no native effects literally named `building`, `treasury_gdp`, `weekly_gdp_expense`, `weekly_transfer`, `faction_opinion`, `remove_spirit`, `experience`, `event`, `unlock_decision` or `suspend_agreement`. Use native `modify_treasury_effect`, state slot and `add_building_construction` effects, `add_tech_bonus`, service XP effects, faction opinion helpers, spirit add/remove or swap logic, and the project event/decision/standing-agreement handlers. `weekly_transfer` in particular needs the matched Brazil expense and Paraguay income hooks; a preview row by itself does not implement the transfer.

## Resolved findings and remaining integration requirements

1. **Itaipu state mapping is resolved.** Paraguay is state `895-Paraguay.txt`, tag `PAR`; state 878 is Suriname, tag `SUR`. The display map uses 895 for Paraguay. State 893 is the Rio de la Plata state owned by `URG` and is displayed as Uruguay (Rio de la Plata). Brazil's construction target remains state 880, Paraná.
2. **Party identity data is declarative, not a native trigger.** The JSON records a real broad MD outlook trigger and a proposed exact party identity. Strings such as `ARENA; PDS after its real reorganisation` are not runnable trigger syntax. The identities for later PDS, PMDB, PFL, PT, PDT, later PTB, PSDB and PRN require approved existing-registry integration and reward-time checks. Do not infer a party from its broad slot or create additional slots without approval.
3. **Building guards are described in the JSON but still need implementation.** `execution_contract` now records owner, controller, native building-type capacity and shared capacity after the extra slot grant for all 45 building effects. It also records the one-time receipt, setup debit, extra slot and construction order. These are design guards; native execution must implement and recheck them at focus completion or recipient acceptance.
4. **Foreign influence and Itaipu wording are corrected.** The compiled content contains no `foreign_influence_modifier`; the Itaipu focus describes RP financial support and disclaims historical royalty pricing and physical electricity delivery. Negative `foreign_influence_defense_modifier` still means political vulnerability, not general technology or financial dependence. Some other descriptions use broad “dependence” language for licensing or market access; keep it tied to explicit costs and access rewards.
5. **Faction opinion availability is represented conditionally in this snapshot.** Rural farmer DSL entries map to the present 1970 `landowners` faction. Union opinion entries carry `if_idea = labour_unions` and the prospective preview labels them conditional. Runtime must implement these through native `has_idea` checks and opinion helpers. Do not add either faction to the 1970 start merely to make the preview unconditional.
6. **Standalone modification types still need native lowering.** `treasury_gdp`, `weekly_gdp_expense`, `building`, `research`, `faction_opinion`, `remove_spirit`, `experience`, `event`, `unlock_decision`, `weekly_transfer` and `suspend_agreement` are concept DSL kinds, not literal native effects. Use the corresponding native money, state construction, research, faction, spirit, XP and project agreement mechanisms.

## Verified economic contract

`gdp_total` is annual GDP in billions of MD's internal dollars. The economy UI labels GDP in billions; `calculate_gdp` writes the value in native `common/scripted_effects/00_money_system.txt`. The 1970 historical-display adjustment is separate. Focus charges use the payer's current `gdp_total` at execution, multiplied by the negative percentage share and passed once through `modify_treasury_effect`. The exporter represents a 0.15% cost as `percent = -0.15`, and shows it as a one-time percent of current payer GDP. The eventual compiler must divide percentage points by 100 in its arithmetic and must not also add the setup charge to weekly expenses.

Recurring appropriation uses each country's current GDP on each weekly refresh: `gdp_total * annual_share / 52`. The France integration at `tools/france_1970_runtime/integration.py` and native `COLDWAR_FRA2_add_weekly_expenses` / `COLDWAR_FRA2_add_weekly_income` show the existing aggregator pattern. Expense goes to `additional_expenses_rate`; an approved bilateral transfer can pair the same amount as recipient `additional_income_rate`. The France sample cache stores a quote for seven days. Because this concept calls for current weekly GDP, Brazil must recalculate the same payer-GDP share at each weekly refresh rather than reuse a frozen or cached quote. This is budget accounting, not a direct Treasury deposit or physical commodity delivery. The stream must enter each side's aggregator only once, reset before rebuilding, and be zero whenever the agreement is inactive. The current GDP-priced recurring contract takes precedence over older flat-cost rules.

For Itaipu, the compiled concept has the paired 0.08% annual Brazil-GDP payment as `BRA.gdp_total * 0.0008 / 52`, counted once as Brazil's weekly expense and once as Paraguay's weekly income under the signed active agreement. Each country also has a separate own-GDP programme appropriation (`0.18%` Brazil, `0.12%` Paraguay). Verify both runtime aggregation paths use one identical current Brazil-GDP quote per weekly refresh. Do not call the payment a price for electricity unless a separate tariff model is added.

MD's `calculate_energy_load_sharing` in native `common/scripted_effects/!_energy_effects.txt` can transfer energy supply to a deficit recipient subject to the provider having enough energy. Its own comment says it is one-way. It is a physical energy-load mechanic, not a priced, reciprocal electricity trade contract. No native electricity-price modifier or income consumer was found in the inspected energy system. A bilateral Itaipu concept can use the energy sharing API only if the native relationship can express the actual Brazil/Paraguay provider and recipient needs; otherwise describe capacity development, building rewards and budgets without promising a delivered quantity or royalty.

Every authored budget literal has at most five fractional digits in the examined source. Preserve this at compile time. Tooltip calculations must remain prospective and must never execute charges or grant assets.

## Native keys and reward meanings

The current `M()` palette is supported by native definitions or consumers, with important semantic limits:

| Exact key | Verified effect meaning |
| --- | --- |
| `industrial_capacity_factory`, `industrial_capacity_dockyard` | Sector output capacity, not construction speed. |
| `production_speed_buildings_factor`, `production_speed_nuclear_reactor_factor` | Construction duration. Does not grant a completed building. |
| `production_factory_efficiency_gain_factor`, `production_factory_max_efficiency_factor` | Efficiency growth and cap respectively. |
| `research_speed_factor`, `literacy_rate_education_modifier`, `education_cost_multiplier_modifier` | Research speed, literacy growth and education bill are distinct. |
| `agricolture_productivity_modifier` | MD spelling is intentional; it contributes to the agriculture productivity calculation. |
| `bureaucracy_cost_multiplier_modifier`, `social_cost_multiplier_modifier`, `consumer_goods_factor` | Different recurring costs and consumer-goods factory allocation. |
| `country_productivity_growth_modifier` | Growth contribution, not an instant GDP bonus. |
| `resource_export_multiplier_modifier`, `steel_export_multiplier_modifier` | Sale revenue multiplier for resources actually exported; do not promise export volume or oil production. |
| `fuel_gain_factor` | Fuel-system modifier, separate from oil export revenue or reserves. |
| `inflation_cost_multiplier_modifier`, `inflation_gain_multiplier_modifier` | Inflation-related cost and inflation growth calculation. |
| `interest_rate_multiplier_modifier` | Additive percentage points to interest, followed by native 0.8 to 50 percent clamp; not a relative rate percentage. |
| `foreign_influence_modifier` | Influencer action strength, so a positive value strengthens Brazil's ability to exert influence. It does not mean foreign dependence. |
| `foreign_influence_defense_modifier` | Modifies defense against influence. A negative value is vulnerability, not broad economic dependence. |
| `army_org_factor`, `navy_org_factor`, `army_infantry_attack_factor`, `air_mission_efficiency`, `air_accidents_factor` | Organization, attack, air effectiveness and accident chance. These do not grant equipment, units or trained personnel. |
| `army_personnel_cost_multiplier_modifier`, `navy_personnel_cost_multiplier_modifier`, `airforce_personnel_cost_multiplier_modifier`, `equipment_cost_multiplier_modifier`, `military_spending_cost_multiplier_modifier` | Separate native cost consumers. Cost changes are not combat bonuses. |
| `political_power_factor`, `stability_factor`, `corporate_tax_income_multiplier_modifier` | Supported political power, stability and corporate-tax income consumers. Tax income multiplier does not change the statutory rate. |

Research categories in `CAT` are present in the installed technology tree. `add_tech_bonus` must be emitted with category, bonus, uses and a unique bonus name. The source reward palette does not include unsupported generic literacy, fuel-production, energy-export or workforce-size aliases. No negative workforce-size modifier appears in the inspected catalogue.

The four Brazil-specific ideas `BRA_idea_brazilian_knack`, `BRA_idea_oncoming_debt_crisis`, `BRA_idea_enraged_natives` and `BRA_idea_crippled_currency_one` are in the 2000.1.1 dated history block at lines 1243-1246, not the inspected 1970 scenario block; no separate 1970 provider was found in the inspected common scripts. Exclude them from 1970 stacking estimates unless another scenario integration explicitly adds them. Within the concept spirits, `miracle` contributes +0.04 factory output and +0.5 interest points; the reachable `military_7` focus adds +0.07 factory output and +0.5 interest points. Before the `refinance` or `export_discipline` remedy removes `miracle`, those concept-only values total +0.11 factory output and +1.0 interest points. The five proposed starting-spirit stability changes total -0.225 modifier input. Treat that as a balance target, not a measured engine outcome. Every `COLDWAR_BRA_*` spirit still needs a real provider, exact effect list, starting availability, lifecycle and localization. `remove_spirit` must lower to `remove_ideas` or safe swap/cleanup logic, not a literal native effect named `remove_spirit`.

`faction_opinion` lowers through native helpers such as `change_the_military_opinion`, `change_landowners_opinion`, `change_farmers_opinion` and `change_labour_unions_opinion`. Each helper only acts if its corresponding faction idea is present, clamps opinion to native bounds and refreshes faction modifiers. Set signed `temp_opinion` just before the helper. `autocrats_opinion_change` copies it into `temp_opinion_change` and doubles positive changes under recognized autocratic checks, including ruling slot 22. The farmer helper has an additional positive-change doubling under the specific Syria subsidy idea; this concept maps farmer rewards to landowners, so that exceptional farmer scaling does not apply. The concept's `if_idea` field is declarative and must lower to the native `has_idea` guard. Its `native_input_policy` means halve only positive helper inputs inside autocratic checks; keep the displayed target opinion delta exact under other governments and for negative changes.

## Parties and scenario gates

The verified 1970 government is Medici with `ruling_party = 22`. The exact native broad outlook triggers are `western_conservatism_are_in_power` for slot 1, `western_liberals_are_in_power` for slot 2, `western_social_democrats_are_in_power` for slot 3, `emerging_communist_state_are_in_power` for slot 4, `neutrality_neutral_communism_are_in_power` for slot 19, `nationalist_right_wing_populists_are_in_power` for slot 20, and `nationalist_military_junta_are_in_power` for slot 22. Brazil's current mapping is ARENA 1, MDB 2, old PTB 3, PCB 4, PCdoB 19, Lacerdists 20 and FFAA 22. Keep FFAA22 distinct from civilian ARENA1.

PDS/ARENA and PMDB/MDB can share their existing broad identities when their real continuity/renaming is represented. PFL, PT, PDT, later PTB, PSDB and PRN require separately registered identities or real formation flags before same-slot programmes can be distinguished. Do not create them or take additional party slots without approval. `conditions` text that names a party is not itself an availability or reward gate. Keep all party branches visible, and check the approved exact identity in both focus availability and execution.

## State and native building audit

The building names used in the catalogue are present in native `common/buildings/00_buildings.txt`, including `offices`, `agriculture_district`, `renewable_energy_infra`, `fuel_silo`, `nuclear_reactor`, `synthetic_refinery`, factories, dockyards, infrastructure and air bases. The exporter maps each building reward to `slots = amount`, which follows the project rule. Verify each current-history owner and controller, whether the building occupies shared or specialized capacity, and native capacity immediately before execution. Paraguay is 895; Uruguay state 893 is owned by URG and has a clear display name in this compiled version.

## Bilateral lifecycle and regional system

The standing-offer contract records separate Brazilian and recipient spirits and prospective effects, real recipient consent, no expiry, bilateral peace, both-country existence, native embargo and all four mirrored Imperia sanction classes. Retain all these checks in actual availability, acceptance, active-stream calculation and spirit reconcile. Every offer that depends on another offer needs the actual parent active-membership/signed spirit in both preview requirements and runtime reward guards. Each one-time setup payment and asset must happen once at acceptance; suspending and restoring must only remove/reapply the two spirits and active budget streams.

ALALC is the appropriate 1970 regional framework; ALADI succeeds it in 1980. The installed MD Mercosur system is real (`common/scripted_effects/05_MERCOSUR_effects.txt`, `common/national_focus/06_MERCOSUR_shared.txt`, `common/decisions/mercosur_decisions.txt`) and gates membership benefits on its membership spirit. It is a separate later organisation; do not copy Brazil's modern history seed into a 1970 start or auto-enrol countries. The concept's `regional_secretariat` is a nationally built office and programme, not Mercosur membership.

## Sources checked

- `tools/france_1970_design/GDP_COST_REFERENCE.md` and `tools/france_1970_runtime/integration.py` for current-GDP prices and the paired weekly finance aggregator.
- Native `common/scripted_effects/00_money_system.txt`, `00_budget_effects.txt`, `COLDWAR_FRA2_diplomacy_effects.txt`, `00_influence_scripted_effects.txt`, `!_energy_effects.txt`, `00_internal_faction_effects.txt`.
- Native `common/modifier_definitions/money_modifier_definitions.txt`, `influence_modifier_definitions.txt`, `common/buildings/00_buildings.txt`, Brazilian ideas, political triggers and state history files for 878, 880, 893 and 895.
- [ALADI treaty history](https://www.aladi.org/preguntas-frecuentes/) and [Brazil Siscomex ALALC/ALADI overview](https://www.gov.br/siscomex/pt-br/informacoes/acordos-comerciais/aladi).
