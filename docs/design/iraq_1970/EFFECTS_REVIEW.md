# COLDWAR | Independent Iraq concept effects review

Independent source review, 18 October 2026. The JSON catalogue and both emitted specimens have been inspected across all 396 focuses. The reviewer edits only the review/research documents, not the authoring sources. No HOI4 engine, government-transition or multiplayer test has been performed.

## Scope and status boundary

Reviewed authoring sources: `tools/iraq_1970_concept/build_concept.py` and `tools/iraq_1970_concept/content.py`. This is an approval-stage design under `docs/design/iraq_1970`, not an installable tree. New `COLDWAR_IRQ_*` triggers, reconciliation helpers, decisions and response contracts are intentionally proposed interfaces; their names are not existing MD API evidence.

The final scope follows the user's correction: historically significant parties and principal leaders. The communist content is the ICP and Aziz Muhammad. The four previously drafted alternative communist-leader groups are excluded from the emitted catalogue; their internal historical debates do not establish additional governing secretaries.

All29 keys in the modifier-label inventory have real providers:28 in the installed main MD country ideas, one in the target Cold War system with a demonstrated consumer. Twenty-eight keys are actually used by focus packages; the registered interest-rate key remains an unused inventory entry. The emitted transactional specimen now contains native affordability, ownership/control and one-time guards. New Iraqi reconciliation helpers, condition-flag providers and playable decision files remain unimplemented approval-stage contracts.

| Coverage in the reviewed JSON | Count / result |
|---|---|
| Focuses / sections / starting cards |396 /22 /7 |
| Decision designs at this review snapshot |72; separate `COLDWAR_IRQ_decision_` namespace prevents localization collisions. Includes one START pending-delivery retry and four START outlook campaigns. |
| Focuses with a GDP-share invoice |189; each has one `modify_treasury_effect` debit and a treasury≥frozen-invoice check |
| Physical building deliveries |20;7 civilian factories,7 infrastructure levels,2 agriculture districts,1 power plant,1 office,1 dockyard,1 arms factory |
| Additional native instant-effect packages |11;10 bounded literacy cohorts and1 finite+4-oil grant in state165 |
| Army-XP packages |3; ordinary native `army_experience`, no generated OOB or equipment |
| Explicit additional availability requirements |24; every requirement's proposed code appears in the corresponding `available` condition |
| Situation replacement contracts |12; separate from permanent programme contributions |
| ID and connector checks | No duplicate focus/decision IDs, missing prerequisite IDs or asymmetric exclusions |
| Specimen syntax sanity | Both specimens have balanced braces after removing quoted strings and comments; not an engine load test |

## Every current modifier key: independent provider check

Main MD root: `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`.
The source in this table is relative to its `common/ideas` directory unless otherwise specified.

| Exact key | Actual provider | Mechanical meaning / unit check |
|---|---|---|
| `stability_factor` | `!_energy_ideas.txt:9` | Fractional active stability modifier; .03 is3 stability points. |
| `political_power_factor` | `!_energy_ideas.txt:17` | .03 is+3% PP-gain multiplier. |
| `drift_defence_factor` | `05_armenia.txt:1220` | Ideological drift defence; does not mean coup immunity or Cold War PPS resistance. |
| `production_speed_buildings_factor` | `!_energy_ideas.txt:16` | Country construction-speed modifier. |
| `industrial_capacity_factory` | `05_armenia.txt:336` | Military factory output, not civilian construction. |
| `production_factory_max_efficiency_factor` | `03_CHI_NKO_joint.txt:28` | Native production-efficiency-cap modifier. |
| `production_factory_efficiency_gain_factor` | `05_armenia.txt:1187` | Native efficiency-growth multiplier. |
| `consumer_goods_factor` | `!_special_project_ideas.txt:165` | Native consumer-goods requirement factor. Preserve native wording; not a promised fixed count of spare factories. |
| `tax_gain_multiplier_modifier` | `!_energy_ideas.txt:7` | Tax-revenue multiplier, not an increase to the statutory tax rate. Target consumer `00_money_system.txt:425,729,778`. |
| `oil_export_multiplier_modifier` | `05_Australia.txt:1368` | Multiplier to actual exported-oil revenue; target consumer `00_money_system.txt:4506–4529`. No oil exports means no fictional extra sale. |
| `bureaucracy_cost_multiplier_modifier` | `05_armenia.txt:456` | Fractional bureaucracy spending multiplier; consumer `00_money_system.txt:3307`. |
| `social_cost_multiplier_modifier` | `!_special_project_ideas.txt:132` | Fractional welfare/social spending multiplier; consumer `00_money_system.txt:3501`. It does not independently raise health/education spending laws. |
| `army_personnel_cost_multiplier_modifier` | `05_armenia.txt:443` | Army personnel expenditure, not the entirety of the military budget; consumer `00_money_system.txt:3180`. |
| `interest_rate_multiplier_modifier` | `05_armenia.txt:123` | A number of interest percentage points; consumer `00_money_system.txt:2556`. Not a fractional percentage reduction despite its name. |
| `agricolture_productivity_modifier` | `!_special_project_ideas.txt:62` | Exact MD misspelling. Registered as percentage in target `modifier_definitions/money_modifier_definitions.txt:353`; .04 is+4% agriculture-productivity input. Not generic numerical productivity-growth units. |
| `research_speed_factor` | `00_gpu_development.txt:8` | Country research-speed factor. It does not directly award a technology. |
| `conscription_factor` | `05_armenia.txt:401` | Recruitable-population factor, not an unconditional manpower grant. |
| `army_org_factor` | `05_armenia.txt:442` | Country land-unit organization factor; not restricted to a named guard formation. |
| `army_morale_factor` | `05_armenia.txt:1904` | Native recovery-rate factor. |
| `army_attack_factor` | `05_armenia.txt:439` | Native land-unit attack factor. |
| `army_defence_factor` | `05_armenia.txt:441` | Native land-unit defence factor. |
| `training_time_army_factor` | `05_armenia.txt:865` | Positive lengthens training; negative shortens it. |
| `supply_consumption_factor` | `05_armenia.txt:1477` | Positive raises supply consumption. |
| `army_fuel_consumption_factor` | `05_armenia.txt:3008` | Positive raises army fuel consumption; not fuel gain or export revenue. |
| `fuel_gain_factor` | `!_special_project_ideas.txt:204` | Fuel gain from oil; does not create map oil. |
| `industrial_capacity_dockyard` | `05_Australia.txt:962` | Native dockyard output. A country modifier is not itself a new shipyard. |
| `opinion_gain_monthly_same_ideology_factor` | `05_china.txt:2477` | Factor to monthly opinion gain with the same outlook. Does not automatically create a treaty or ally. |
| `foreign_influence_modifier` | `03_CHI_SOV_joint.txt:19` | Outward foreign-influence modifier. Target consumer `00_influence_scripted_effects.txt:1106–1122` combines attacker strength and defender resistance. |
| `mdcw_cw_support_effectiveness` | **Target** `common/modifier_definitions/mdcw_cold_war_modifiers.txt:35` | Cold War foreign party-support/broadcasting campaign effectiveness, consumed at `mdcw_cold_war_effects.txt:3601`. Not military aid, proxy combat strength or friendly-division attack. |

Engine-native entries are established by real MD country-idea usage; the HOI4 executable applies them. For scripted custom entries, the target calculation was followed. Source consistency is not an engine test.

## Findings and their disposition

The following issues were sent to the author while the concept was being written and then checked against emitted data. They are recorded to explain the final contracts, not as a list of outstanding bugs.

1. **Corrected:** all emitted invoice assignments now read `gdp_total`, the actual MD economy variable.
2. **Corrected:** agriculture displays percentage input; it is not confused with number-valued productivity growth.
3. **Corrected:** inline comments were removed from gate strings. The final specimens' brace structure is balanced.
4. **Corrected:** the `proxy` alias displays “Foreign party support campaign effectiveness”; it does not claim stronger armed proxies.
5. **Intent clarified:** the frontier spirit lowers Iraq's outward influence by5%. It does not use the different defender-resistance modifier. Treat this as the selected diplomatic-cost abstraction.
6. **Corrected and clarified:** the payroll audit removes only3 bureaucracy points through its situation ledger and has no duplicate−.03 package. Professional command removes the original−.05 organization component and separately contributes+.03, explicitly an8-point improvement from that component's initial state. Agricultural and oil programme contributions are explicitly separate from structural-spirit changes. The rural distribution package includes an additional−.01 consumer-goods contribution while its situation component falls from+.03 to+.01; combined effect from those two entries is zero relative to an otherwise zero baseline.
7. **Scope corrected:** the separate Zaki, Amir, Nuri and Central Command governing programmes are absent from the final emitted design. Aziz Muhammad is the principal historical ICP leader; factional debate is not treated as evidence of a different incumbent secretaryship.
8. **Corrected:** decision IDs use a separate prefix, eliminating global localization-key collisions.
9. **Graph corrected:** the final convergence is one OR prerequisite group. Peaceful completion is reachable through the civic/service side and the sanctions-response dossier; war-only rewards retain separate requirements. The dossier can be opened without sanctions, while its actual sanctions-review decision requires an observed sanctions situation.
10. **Contract corrected:** `war_economy` and `war_procurement_cycle` include `has_war = yes` in their live `active_condition`; programme caches must evaluate that condition after peace. Every package's active condition now also includes its complete availability conditions. Actual detach/restore behaviour still needs the new reconciler and an engine test.
11. **Concern resolved by native evidence:** `free_building_slots` with `building = infrastructure` is a real building-specific MD capacity check (`MD:99_AFG_scripted_effects.txt:165,190`; `MD:99_AI_investment_scripted_effects.txt:136`). The current infrastructure building definition has `state_max = 6`; do not replace the native check with an assumed legacy level5 cap. The phrase “shared slots” in generic comments should read “native building capacity”.
12. **Corrected:** renegotiating the IPC contract no longer grants an oil-revenue package before foreign acceptance. The accepted-delivery node grants the consolidated+.06 oil contribution and the−.03 outward-influence cost.
13. **Corrected:** programme reconciliation is emitted after the node's `_implemented` flag. Its eligibility scan can therefore see the just-delivered package without waiting for another focus or periodic resync.
14. **Corrected:** every descendant requires actual `_implemented` predecessor flags using the same AND/OR grouping as its focus prerequisites. Completing an unfunded focus therefore cannot grant its descendants. The early physical factory, oil and agricultural projects are optional funded spurs, avoiding a universal bottleneck behind an undelivered building.
15. **Price calibration clarified:** native 2000-era construction-helper prices are retained only as comparison metadata. The final specimens apply no native-price floor. Their separate Iraqi 1970 GDP-share quotes are explicit new balance proposals, with no claimed existing historical-discount API.
16. **Negotiation reachability checked:** Baath, ICP and KDP first-fork contract deliveries are side spurs; PUK and civic second-fork contract deliveries are side spurs; both oil forks use this structure. Their main domestic continuations require the selected policy focus rather than a refused or pending contract-delivery focus. Contract benefits retain their acceptance flags. Delivered-parent checks remain on actual descendants of each spur, so bypassing a foreign/domestic counterparty veto does not bypass payment or acceptance for that spur's reward.

### Financial transaction and retry contract

The emitted specimen now freezes a persistent per-focus invoice at the first completion attempt, rechecks exact party/leader/extra availability and treasury, and for physical projects rechecks native capacity and current Iraqi ownership/control. Only the passing branch debits treasury, executes every reward and marks the focus `_implemented`; the failing branch sets a pending flag and executes no reward. The outer once guard prevents a retry or reconciliation from replaying money, factories, resource increments, literacy or XP.

This is **pay on delivery**, with no deposit: no refund is owed on a failed attempt. The final 72-decision catalogue explicitly includes `COLDWAR_IRQ_decision_retry_pending` from START, at 0 PP: select one pending item, preserve its frozen invoice, recheck original eligibility, and execute the same one-time transaction. The proposed provider is honestly named `COLDWAR_IRQ_retry_selected_pending_programme`; its actual playable decision/helper is to be authored after approval, together with the other new decision files. Four additional START campaigns use the native `change_relative_party_popularity` API with +.03 party/outlook inputs and clear the optional outlook input afterward; registered-party selection remains a proposed bridge. Their final wording correctly states that native MD normalization determines final gains, rather than promising a fixed resulting party-array increase. These additions were checked for distinct IDs, START access and declared cost/cooldown.

The existing native `modify_treasury_effect` only adjusts the account and marks money dirty; it supplies no affordability protection itself. The new guards are therefore material and were checked in all 189 invoice nodes. Quoted shares range from .5% to 5% of MD GDP; they are proposed game costs, not historical Iraqi expenditure measurements or promises of full native construction-price equivalence.

The seven native domestic-helper reference charges, in MD billions, are: civilian factory 7.5, arms factory 7.5, dockyard 7.5, infrastructure 3.5, office project 12, fossil power plant 3.25 and agriculture district 3.75. Providers are main MD `00_scripted_effects.txt:235,16,607,454,724,1911,2083` respectively. The office helper also grants a power plant; the concept deliberately proposes an office-only delivery and cannot call that helper unchanged. The native units are explicit at target `MD_money_l_english.yml:11,16,25`.

The target sets Iraq's 1970 GDP target to 3.281 (`IMP_1970_gdp_scripted_effects.txt:1729`) and applies its base adjustment at :1829–1830, consumed in `00_money_system.txt:6150` onward. Therefore a literal 7.5-billion helper charge would equal approximately 229% of that starting GDP. No universal 1970 construction-price factor was established in the examined helper/treasury path; scaling of ongoing spending or oil display is not such a factor. The concept's GDP-share project prices resolve this conflict openly as new balancing proposals. They still need a native budget/capacity playtest before implementation; this review verifies APIs and accounting rather than claiming a realistic capital-price model.

### Programme totals and stability

The final programme rule is `min(sum positive active policy contributions, .15) + sum negative active policy contributions`; original situation spirits are separate. This retains negative political trade-offs when the positive stability cap binds. Clamping only the net sum would partly conceal negative choices and is not the stated design. A listed positive focus stability value is a package contribution; once the cap binds it is not necessarily the realized stability increase. The preview and eventual native tooltip must disclose that limit.

Earned packages must be summed into derived caches from the selected policy slots and current party/leader eligibility. This is not another one-time payout. A party or leader change deactivates the old programme, while paid construction, literacy and durable national development persist. Existing MD Russia and target Soviet patterns in `MECHANICS_AND_HISTORY.md` establish viable architecture; the newly named Iraqi helpers are still designs rather than verified providers.

### Exact native education consequences of the proposed baseline

For the explicitly provisional `literacy_rate = .35`, the existing education formula gives a base of−60 literacy points relative to its95% baseline. `common/scripted_effects/00_education_effects.txt:118–131` and `common/dynamic_modifiers/00_MD_dynamic_modifiers.txt:166–173` then map it to research speed−30%, education expenditure+60%, numerical productivity-growth input−1.20, offices productivity−30%, and agriculture productivity input+30%. The last field is literally `agricolture_productivity_modifier`, not a generic uneducated-worker variable with a different effect.

That agriculture input offsets part of the separately proposed rural impairment; it cannot be omitted from a supposedly complete starting-effects summary. The negative growth input is processed through the existing productivity/catch-up formulas and other active modifiers, so it is not a guaranteed−1.20 state productivity change per month. A paid+2-point literacy cohort correspondingly changes these inputs by research+1 point, education cost−2 points, growth input+.04, office productivity+1 point and agriculture input−1 point. These are source-formula consequences, not a full initialized-country total or an engine test.

## Contracts to verify in final stage data

- Every condition in a focus's extra requirements must appear as a proposed executable requirement in its specimen and be visible in the inspector; narrative requirements alone do not gate a focus.
- Exact governing subparty and actual office-holder must control their programmes. Coalition membership is not governing-party authority. Same-outlook subparty switches need the existing party-change helper integration as well as a fallback resync.
- Accumulated programme variables survive departure, active programme modifiers detach/deactivate, and a returning eligible government restores earned modifiers. Schools, paid buildings, resource additions, literacy, money and army XP must never replay during reconciliation.
- Building and resource grants need current state ownership/control, capacity and one-time-grant checks. Proposed comments are a contract, not actual safeguards.
- Quoted GDP-share costs use a frozen invoice and pay on successful delivery; no deposits or refunds. The pending-project retry must preserve that quote and reuse the original transaction guards. Native `modify_treasury_effect` itself permits negative treasury; the explicit affordability check remains necessary.
- Foreign proposals require recipient accept/refuse/expiry, payer and beneficiary accounting, delayed-state rechecks, and a signature guard against duplicate delivery. A decision-unlock flag is not a completed negotiation.
- Starting literacy.35 is explicitly provisional; native education will provide its own research/workforce/cost consequences. No extra duplicate “low skills” research penalty should be added.
- Normal engine rewards must show actual native tooltips. Adding a backing variable without a stat tooltip and later dynamic refresh is not yet the finished native MD reward presentation.

The checked native APIs, units, scopes and transaction structure are suitable foundations for an approval concept. Outstanding implementation work is explicitly the new condition/leadership bridges, situation and programme reconcilers, pending retry and usable decision/event providers, truthful native reward tooltips and HOI4 transition/save/multiplayer checks. No claim is made that this concept can be copied into the loaded mod as finished gameplay.

## Reviewed snapshot hashes

SHA-256 hashes recorded for the 396-focus / 72-decision approval snapshot; later source changes require re-emission and renewed checks where affected.

| File | SHA-256 |
|---|---|
| `tools/iraq_1970_concept/build_concept.py` | `5ebb0229c7aa5247983776869933d9d52c6de543f7343bd18b555c98612ce723` |
| `tools/iraq_1970_concept/content.py` | `a725723f777eba48bf27d6d54a4873ddc6a2de2db19aeccff1abc987ca650fe1` |
| `COLDWAR_IRQ_1970_CONCEPT.json` | `9e50677eb90d2a8e827ae19e30b30b0d0037813c079dadce28da7d5780226913` |
| `COLDWAR_IRQ_FOCUS_SPECIMEN.txt` | `eee89e45c8d71156d445636c7a6fc8ea3d4f1cde223bc5d7f440a4acbe36aafe` |
| `COLDWAR_IRQ_MODIFIER_SPECIMEN.txt` | `50071ab5e3a3196e9b693615f278a29e01fd78b5e6be8374f7d307f8409ceaad` |
