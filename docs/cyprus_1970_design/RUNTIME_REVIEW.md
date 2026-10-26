# Cyprus 1970 runtime review

Read-only audit of runtime work authorized after the295-focus design. Only this report is edited by the review agent. The main implementation agent owns all generator/runtime fixes. Source findings below are verified locally; static checks are not an in-game compile or multiplayer test.

**Final review status:** source/static-output review complete for the295-focus implementation. All concrete findings recorded below are addressed in the final regenerated snapshot. Earlier sections preserve the audit history and are superseded by the final sign-off at the end. This is not an in-game or multiplayer certification.

## Initial source verification

At the first pass no `tools/cyprus_1970/compile.py` or `COLDWAR_CYP_1970_*` runtime files had yet appeared. The following contracts should constrain the generated implementation:

| Item | Verified source | Required implementation behaviour |
|---|---|---|
| State dynamic modifiers | `common/scripted_effects/00_internal_investment_automation_effects.txt:99`, `:118`; `common/dynamic_modifiers/00_money_dynamic_modifiers.txt:78` | Add/update145/146 modifiers in state scope. State-held values must be initialized in that state; country programme values cannot be silently read as state variables. Growth modifier scales positive growth, not current GDP. |
| Naval construction location | `events/05_australia_events.txt:128`; `common/decisions/05_ENG_decisions.txt:723` | In state146 scope, province7193, level1; check owner/control and `free_building_slots = { building = naval_base size > 0 province =7193 }` before queueing. Do not accidentally queue in country/province scope or grant a new state. |
| Queue rather than instant grant | `common/decisions/05_CHI_decisions.txt:4993` and following | `instant_build = no` is a real native usage. It queues construction; it does not pay construction/upkeep or guarantee the eventual project succeeds. |
| Money cost | `common/scripted_effects/00_budget_effects.txt:1487` | Set `treasury_change` to GDP multiplied by a negative fraction and call `modify_treasury_effect`. It updates treasury/dirty money state but performs no affordability check. Require initialized positive GDP, current funds and an atomic result/cost gate. |
| Debt | same`:1501` | Set `debt_change`, call `modify_debt_effect`; a loan also needs a real corresponding cash transfer and donor consent. An unimplemented foreign loan may remain unavailable; it must not silently become free cash. |
| Resource trigger | `common/scripted_triggers/00_scripted_triggers.txt:276`, `common/national_focus/00_generic.txt:1847` | Actual state trigger is `has_resources_amount = { resource = oil amount > 0 }`. Do not invent `has_resources` or confuse stockpile/strategic-resource values with map deposits. |
| One-time focus marker | `events/05_armenia.txt:10170`; block form `05_australia_events.txt:5354` | `complete_national_focus` is real. No verified `reward=no` option; no promise it ignores prerequisites/exclusions. Event milestone must have one payload owner, compatible topology and a guard against recursive rewards/dispatch. |
| Fallback tree | `common/scripted_effects/mdcw_1970_focus_tree_effects.txt` | Existing fallback excludes USA/SPR/LBA/EGY/ISR but initially notCYP. Add an era-scopedCYP exclusion so old events do not replace the authored tree or reset progress. |
| Native leader routing | `common/scripted_effects/00_leader_setup_scripted_effects.txt:9–26` | `set_leader` calls `kill_country_leader` **before** `set_leader_[TAG]`. A cached/no-op customCYP dispatcher called after that kill leaves no correct leader. InterceptCYP1970 before the central kill, or guarantee a native routing call recreates the correct era leader. A periodic refresh should not continuously retire/recreate leaders. |
| Later leader definitions | `common/scripted_effects/CYP_political_leaders.txt` | Native helper contains Praxoula Antoniadou, Marinos Sizopoulos, Andros Kyprianou and modern nationalist leaders. Guard the whole modern branch out of1970; do not let correct focus gates coexist with anachronistic political leaders. |
| Actual war observation | `common/on_actions/mdcw_cold_war_on_actions.txt:43` | ROOT attacker/FROM defender. Passive manualTUR→CYP observer records an existing action, not a new declaration, retrospective coup or forced territorial transfer. |
| Modern ambient content | `common/on_actions/CYP_on_actions.txt`; `common/decisions/categories/99_GRE_decision_categories.txt:47` | Quarantine incompatible modern/randomCYP content in1970. It must not supply foreign authorization or trigger war behind the MP callback system. |

## Priority findings before generated-file inspection

1. **Leader pre-kill trap:** an era dispatcher can be correct internally yet still lose the leader if the native caller killed it first and the custom dispatcher returns early because its cached party/leader ID has not changed. Test elections, same-party transitions and periodic leader refresh separately.
2. **Fallback protection:** the initial generic fallback can replaceCYP unless the authored1970 guard is added. Startup protection alone is insufficient if a later old event invokes the fallback.
3. **Queue and affordability:** ordinary queued naval construction and GDP administration costs are separate. Recheck current ownership/control/province cap and cash at completion; do not charge for a no-op or grant the reward after a failed debit. Existing helper usage alone does not enforce that.

## Review status

Awaiting generated files for concrete runtime findings. This report does not certify a295-focus runtime merely because its source design passed static key checks. The next pass will inspect actual startup history/on-actions, tree selection, party enable/lifecycle, state modifier scope, focus cost/completion guards, safe historical leader routing and MP reservation/response hooks.

## First generator-policy inspection: `tools/cyprus_1970/rules.py`

The explicit FOREIGN/COMMUNITY/OBSERVED classifications and FLEXIBLE_PAIRS removal policy match the reviewed MP separation: a coup result/guarantor result is observed, and conference/defiance or talks/remobilisation are not permanently exclusive stances. These classifications still need corresponding generated code before they can be certified operational.

**Concrete semantic finding:** `EXTRA['war_junta_links']` initially checks `GRE = { has_government = nationalist }`. This accepts the entire nationalist outlook, including populist and monarchist parties; it is broader than the stated requirement that a military junta actually governs Greece. Prefer the existing exact `nationalist_military_junta_are_in_power = yes` trigger (index22), or a separately justified actual-junta flag. Any additional eligible regime should be explicit rather than inherited from the outlook label. Reported to implementation owner.

`IMP_is_1970_scenario` is based on the campaign **start date** (`common/scripted_triggers/IMP_cold_war_scenario_triggers.txt:1`), so remains true in later years of a1970 campaign. Date-gated successor selection and later community party foundation dates therefore still need live-date checks; the scenario trigger alone is not a1970-only date condition.

## Compiler inspection before runtime module generation

`tools/cyprus_1970/compile.py` now exists. Initial read-only checks:

- State modifiers are emitted as valid flat state-dynamic definitions rather than country-variable references accidentally evaluated in state scope.
- Six party programme definitions enable on the scenario, originalCYP tag and exact governing indices; the combined security route enables21OR22. Political and economic rewards share the same programme namespace.
- The controller gate distinguishes current human control from dedicated unreserved historicalCYP AI. Actual reservation setup remains to inspect in the runtime module.
- Current GDP cost is recomputed on a completion path by `recalc_cost`; `afford_current` and `pay_cost` are separate helpers. They must be called in that order inside the same successful outcome guard. Native treasury helpers do not supply the missing guard themselves.
- OBSERVED and REACTIVE focuses have marker-only completion payloads. OBSERVED prerequisites/exclusions are removed, while flexible stance exclusions are removed explicitly. This is consistent with event-owned results and avoids duplicate rewards from completion itself; actual engine completion behaviour still needs testing.
- Research examples use existing categories and standard native bonus syntax. `FOCUS_FILTER_ARMY` and ideas with `allowed = { always = no }` are used elsewhere locally; these are not unsupported names/patterns.

No additional concrete compiler defect was established in this first pass. Startup/fallback changes, money/outcome idempotency, real bilateral callbacks, historical government dispatch and reserved-seat response handling depend on the forthcoming runtime module/generated files and are not yet certified.

**Subsequent compiler finding: tooltip newline escaping.** The initial `effect_text` AST join separator is a two-character literal backslash+n, while the localisation writer subsequently serializes values through `json.dumps`. This emits doubled backslashes in the YAML string, unlike native single-backslash newline escapes. Prefer an actual newline character in the internal Python value so JSON serialization emits the intended single `\n` escape, or explicitly normalize it in the localisation serializer. Reported to the implementation owner; verify generated multiline tooltips rather than only checking that localisation keys exist.

**Important runtime timing defect:** the compiler initially copies `n['focus_cost']`, which the design builder calculates as `days / 10`. The installed base game's `E:/SteamLibrary/steamapps/common/Hearts of Iron IV/common/defines/00_defines.lua:3599` sets **`FOCUS_POINT_DAYS = 7`** (“Each point takes a week”), and no local-mod or supplied-MD override was found. Thus nominal35/50/60day designs compile to approximately24.5/35/42days. To retain their stated durations, calculate runtime cost from `n['days'] / 7` (35→5,50→7.142857,60→8.571429), or explicitly adopt shorter durations and update all claims. The genericMD `cost =8.6` consequently corresponds to roughly60days, not86. Reported directly to the implementation owner; this corrects an earlier design-stage assumption rather than validating it.

## First generated-runtime inspection

Generated snapshot now exists:295 focuses,890 scripted effects,61 events and58 decisions. These findings refer to the first inspected output and may be superseded by subsequent owner fixes. No generated file was edited by this reviewer.

### Priority findings reported to implementation owner

1. **Daily tick scope:** `common/on_actions/COLDWAR_CYP_1970_on_actions.txt` initially enters `CYP = { daily_tick }` unconditionally inside the country-scoped `on_daily`. Native `00_on_actions.txt:86` processes each country's energy/resources, confirming this is a country pulse. The generated form reruns Cyprus's entire tick once per existing country each day. Gate current scope to originalCYP or add a reliable once-per-day coordinator guard.
2. **Dedicated AI inferred from temporary control:** `COLDWAR_CYP_1970_initialize` initially assigns dedicated historicalAI whenever `is_ai = yes`, rather than requiring an explicit session choice and checking a human reservation. A reserved humanCYP slot that begins unoccupied/temporarilyAI can be misclassified. Default-safe reservation or an explicit session/lobby seat mode is needed; `is_ai` alone is not a disconnect/slot-ownership detector.
3. **State modifier removal shape:** relief/reconstruction emits scalar `remove_dynamic_modifier = ID` (e.g.effects`:343`). All verified MD/local/base examples use `remove_dynamic_modifier = { modifier = ID }`; no native scalar example was found. Switch to the verified block shape so relief does not fail to remove its baseline and stack the replacement malus. This is a strong source-compatibility finding, not a claim of an observed engine error log.
4. **Reactive actions are globally once-only:** `respond_war_conference`, `respond_war_geneva` and other reactive decisions require `NOT registered_*`; the grant effects require `NOT applied_*`, with global lifetime flags. That correctly deduplicates a campaign programme but prevents a new crisis from receiving a fresh Cypriot conference/ultimatum/remobilisation choice. Use a crisis-instance action/result ledger for REACTIVE actions while preserving permanent focus badges and ordinary economic one-time grants.
5. **Stale phase state survives new crisis:** `begin_crisis` resets reply count and some flags, but initially leaves first-intervention, ultimatum, remobilisation and opened-talks flags from earlier episodes. A later crisis can therefore inherit the wrong phase. Reset current-case phase/authorization state, retain historical badge state, and require current-instance evidence.
6. **Old foreign offers can execute in a new crisis:** offer-instance equality is initially tested only when counting the guarantor reply, not in the actual acceptance validity/grant path. Crisis-sensitive stale offers may set current talk/command results or pay a loan despite belonging to another episode. Validate instance/revision before the whole result; durable ordinary programmes may have separately explicit cross-case persistence rules.
7. **Acceptance/payment execution guard:** loan donor debit and the accepted payload initially live directly inside an option whose `trigger` contains validity/funds checks. Do not assume an open popup's option-trigger cache is an atomic execution-time check. Recheck live packet, current actor/funds/party/territory and not-applied status inside the effect before debit and grant. Repeated queued events must not transfer a loan twice even if a bonus grant is independently idempotent.
8. **Response relevance:** every accepted/declined GRE/TUR/ENG foreign offer initially counts as a guarantor response if offered in the active crisis instance, including ordinary trade/training offers. Restrict qualifying topics to real relevant crisis responses or explicitly labelled crisis policy; routine commercial cooperation must not falsely complete “The Guarantors Respond”. Deferral/receipt correctly does not count.
9. **Enosis terminal action absent:** the first inspected `grant_enosis_agreement` has no corresponding implemented transfer/terminal outcome in `extras`. It can mark a successful accepted union applied without carrying out the promised outcome. Either implement the fully consented guarded terminal result, or keep the incomplete terminal offer explicitly unavailable with an honest explanation. Do not charge/mark applied for a silent no-op.
10. **Historical AI context after real regime change:** `historical(n)` only permits politicalparty1 forAI, and reactive decisions use fixed weights independent of current government. That constrains Makarios's path but does not yet implement the required response table for a genuinely changed living government after an actual successful coup/restoration. A small explicit regime/context mapping is needed; it must not letAI choose a coup to reach the map or force a foreign response.

### Positive checks in the generated snapshot

- No forced war declaration, free modern division spawn or automatic northern-state release appears in the generated crisis framework. The Turkish-war observer records an actual TUR→CYP relation and synchronizes markers; it does not issue a new declaration.
- Foreign reply options require current human control; temporaryAI has the neutral deferral option. All foreign partners appearing in the explicit proposal map are assigned human-seat reservation flags. Loan principal is2% of submission GDP and the intended donor debit/CYP credit/CYP debt signs and units are correct; execution-time validation/idempotency still needs the fix above.
- The political/economic programme variables are initialized and share exact current-party enable conditions, including21OR22. Later elections need not reset programme variables or completed focuses.
- State relief uses monotonic stage comparisons and checks both CYP state ownership/control before transition; eventual removal syntax needs the source-compatible correction above.
- Port construction uses state146, province7193, level1 and `instant_build = no`, with owner/control/peace/cap conditions declared in the policy table. It does not invoke the $7.5–12billion factory helpers.
- Marker rewards contain no second gameplay payload; pending-funding paths withhold the outcome until completion conditions are met. Ordinary programme and grant registrations are idempotent in the intended single-event path.

Fallback/history/modern-leader hooks still appeared unpatched during this snapshot. Owner integration work may resolve them; a final review must re-read actual files rather than infer their status from the new helper definitions.

**Additional concrete payload finding:** the first `extras('reconstruction')` unconditionally adds `reconstruction_damage` (-7.5% construction/growth) to every CYP-owned/controlled145/146 after removing `shattered_communities`. If a state never had shattered-community damage (for example an undamaged southern state during an actual northern partition), reconstruction introduces a new permanent malus. Require the original damage modifier before replacing it, otherwise leave that state unchanged.

Read-only structural scan of the first generated snapshot: nineCOLDWAR text files have balanced braces after ignoring comments/quoted strings, and no unresolved `COLDWAR_CYP_1970_* = yes` call was found against the generated definitions. This is a narrow static check, not an engine parser or proof that every trigger/effect is evaluated in the correct scope.

Source fixes are now visible for focus duration (`days/7`), tooltip newline values, state-modifier block removal, exact Greek-junta gating, current-CYP daily pulse, explicit seat rule, current-phase/reactive reset, offer-instance validity, inner acceptance/refusal guards and crisis-topic filtering. Generated files had not yet been regenerated during that observation; final closure requires checking the regenerated output and the separate legacy integration files.

## Regenerated runtime and integration review

The subsequent generated snapshot contains **295 focuses, 891 scripted effects, 106 events and 59 decisions**. The manifest explicitly reports `engine_tested: false`; this review agrees with that limitation. Earlier counts in this report describe superseded snapshots.

Confirmed in actual generated output, rather than inferred from generator intentions:

- Country-scoped daily processing now gates the current original-CYP scope before calling the daily tick.
- The explicit lobby seat rule exists in `common/game_rules/COLDWAR_CYP_1970_rules.txt`. Human CYP and a reserved-human lobby choice preserve the human reservation; dedicated historical AI requires the historical-AI choice. No engine disconnect detector is invented.
- Focus costs now use native seven-day points. A35-day design emits `cost = 5.000000`; a50-day design emits `7.142857`. Multiline localisation now emits native single-backslash newline escapes.
- State dynamic-modifier removals now use the verified block form. Reconstruction replaces shattered-community damage only when that particular owned/controlled state actually has the old damage, so it no longer damages an untouched state.
- A new crisis resets current reply/phase state and REACTIVE action registration/application state while retaining completed focus badges. Foreign acceptance and refusal recheck live proposal, current instance and current conditions inside the execution effect. Loan debit also rechecks donor funds there.
- Guarantor milestone counting is restricted to the explicit crisis-topic set; ordinary trade/training offers do not count. One substantive relevant reply suffices, with other reply channels remaining open.
- Peaceful enosis now has a separate final human-CYP ratification event with an explicit loss-of-independent-play notice. It runs the actual guarded Greek annexation only on ratification, rather than marking a nonexistent terminal outcome. Annexation and final ownership effects require an engine test before claiming this terminal route safe.
- History actually loads the new tree and initializes its starting modifiers. The generic1970 fallback actually excludes scenario CYP. The central native `set_leader` now intercepts1970 CYP before its original kill/modern dispatcher. Modern CYP weekly EU/Green-Line content and modern `CYP_decisions.txt` decisions are actually quarantined from this campaign.

The first snapshot findings on daily scope, scalar dynamic removal, explicit seat setup, cost duration, newline escaping, instance guards, atomic acceptance, response-topic filtering, reconstruction and absent enosis terminal handling are therefore **closed at source/static-output level**. This does not close engine-behaviour tests for event-option caching, dynamic modifier refresh, focus milestone synchronization or multiplayer country selection.

### Remaining concrete review findings reported to the owner

1. **Successful-coup classification is too broad.** The generated `on_coup_succeeded` hook classifies every successful CYP coup as the specific `coup_regime_active` and the daily AI then restores party2 after eight days of war. A real communist or other coup would inherit the Sampson withdrawal policy. The generic observed coup-attempt marker may be broad; the specific nationalist coup regime and its policy must require actual indices20/21/22 or an explicit authorized regime contract. A foreign sponsored coup is observed independently of CYP focus prerequisites.
2. **Makarios return needs a living-government context.** The acting-Clerides AI return currently checks the absolute December1974 date but not `makarios_deceased`. A later acting presidency after1977 can consequently be redirected to party1/Kyprianou by a rule intended to model Makarios's1974 return. Require the live historical leader and appropriate return context; do not apply a1974 succession template to every later crisis.
3. **Renewal within the same crisis has no packet revision.** `offer_instance` identifies a crisis, not a particular renewal. A previously opened popup may become eligible again when the same proposal's pending/live flags are renewed. For a loan, recomputing principal on renewal could silently change the amount associated with the old popup. Preserve the original submitted principal and label offers as the current proposal, or implement a tested per-packet revision/snapshot mechanism. This is an explicit multiplayer caching test case, not a claim that a particular engine popup was experimentally reproduced.
4. **A second legacy CYP decision family remains.** `common/decisions/05_GRE_decisions.txt:790` contains `CYP_seek_greek_union`, `CYP_appeal_to_un`, and `CYP_economic_incentive_north`, with AI weights and native influence changes. Their category `CYP_NCY_diplomatic_category` remains eligible for CYP/NCY through `common/decisions/categories/99_GRE_decision_categories.txt:47`. They become visible if NCY later exists, bypassing the new dossier and historical-AI policy despite the quarantine in the separate CYP decision file. Era-gate that category or the relevant decisions; no Greek tree redesign is needed.
5. **Withheld final ratification needs an explicit terminal meaning or a recovery entry.** After all foreign enosis consents, the applied grant schedules event4000 once. Its `Withhold final ratification` option currently has no follow-up, while ordinary renewal is hidden once the grant is applied. Either state clearly that withholding permanently rejects this settlement, or provide a human-CYP review decision that reopens the final ratification with the same live consent/peace/territory guards. Do not auto-ratify merely because earlier consents exist.

A second narrow structural scan found balanced braces in16 generated/integrated text files and no undefined `COLDWAR_CYP_1970_* = yes` effect calls. The focus file contains295 focus IDs plus its tree ID. This is not an engine syntax validator.

### Essential engine validation still outstanding

Check a fresh1970 lobby with human CYP, dedicated AI CYP, and explicitly reserved/unoccupied CYP; hotjoin after reservation; modern-date CYP; genuine current-government change and same-party leader refresh; all nine initial spirits/state modifiers; GDP-funded focus completion and delayed funding; insufficient donor funds and duplicate/deferred/renewed loan popups; one then multiple guarantor replies; new crisis after an earlier completed badge; direct manual TUR-to-CYP war without custom prerequisite flags; externally successful coup; and dynamic programme disabling/re-enabling after an election. No result in this document substitutes for those actual engine/session tests.

## Final targeted regeneration review

The owner regenerated **295 focuses,891 effects,106 events,142 decisions and1648 English localisation keys**. The owner validator reports295 unique focus IDs, zero coordinate collisions,289 guarded grants and37 locally evidenced native modifier keys. The reviewer inspected actual generated code; the validator was read, not rerun, because its normal execution writes a separate validation artifact outside this reviewer's edit allocation.

The five remaining findings above are now addressed at source/output level:

- Coup observation remains general, but the particular nationalist coup-regime flag and historical-AI resignation require actual governing indices20/21/22. A communist coup no longer inherits that resignation rule.
- Makarios's return requires the live leader, a recorded1974 return context, a narrow December1974 window, current party2, dedicated AI and no human reservation. Later acting presidencies are not automatically converted to this1974 return.
- Foreign event notices contain only a name and AI acknowledgement chance. They cannot accept, decline, transfer money or move territory. Binding accept/decline decisions live in the responding country's current dossier and repeat actor tag, human control, pending/live, instance, current-party and relevant territorial/funding conditions inside their execution guard. The loan principal is initialized once; renewal preserves the submitted principal. Thus an old foreign popup cannot sign a renewed loan or agreement.
- The additional legacy CYP/NCY diplomatic category is now excluded from1970, alongside the separately guarded modern Cyprus decisions.
- The human-CYP final-ratification review decision reopens the terminal notice without applying union automatically. Final ratification still requires an explicit guarded human choice; withholding leaves the review route available.

The reviewed loan acceptance in `common/decisions/COLDWAR_CYP_1970_decisions.txt` debits the lender only after checking current cash against the frozen CYP principal, then adds matching CYP cash and debt and consumes pending/live flags. Its sign and GDP-money units are correct. No foreign AI acceptance fallback was introduced.

Two final guard refinements were reported during this pass and are now **confirmed fixed**: final enosis ratification rechecks all three recorded foreign consents, no recorded refusal, no unresolved reprisals and the current crisis instance; inner foreign-decision validity requires CYP still exists. The enosis renewal route explicitly permits resubmission after an instance change without resetting the once-only applied grant. Fresh foreign replies then reopen final review, rather than reusing old consent or repeating the payload.

## Final sign-off and limits

Final inspected output: **295 focuses,896 scripted effects,106 events,142 decisions and1648 English localisation keys**. The reviewer independently confirmed that the structural validator's recorded hashes match every current generated artifact,18 generated/integrated text or graphics-definition files have balanced braces, and no custom `COLDWAR_CYP_1970_* = yes` effect call is undefined.

All concrete issues raised in this review are closed at source/static-output level. In particular:

- Ordinary children now require their parent result to have been applied, in addition to its historical focus badge, except explicit observed milestones. A submitted but unaccepted loan does not unlock its follow-up reward.
- Renewed civilian harm revokes current communal and constitutional consents. The communal pending resolver can reconsider a renewed proposal, while the once-only grant guard still prevents duplicate political power, research bonuses, reform credit and programme values. Reaffirmed extras restore agreement flags or advance monotonic relief; they do not replay the base reward.
- Enosis final review checks current foreign and communal consent, current crisis, peace, relevant territorial conditions and absence of unresolved reprisals. Renewal after a new crisis remains possible without a second grant. No old foreign notification can authorize money, territory or union.
- A later final settlement can complete displacement recovery after earlier reconstruction/restitution; the emergency is not stuck solely because those stages occurred in the opposite order. Accepted guarantee revision removes the corresponding guarantor-pressure spirit.
- Thin human-actor-owned callbacks record the Turkish renewed-hostilities decision and withdrawal from a currently accepted negotiation. Current withdrawal flags reset with the crisis. Optional Greek/British withdrawal does not create a veto; Turkish withdrawal from these defined negotiations closes that required channel. None of these callbacks declares war, fabricates a battle result or sets `second_phase_combat`.

The owner's nine focused transaction tests passed against emitted ASTs: affordable/deferred payment, duplicate loan acceptance, insufficient funds/AI/stale/wrong-actor rejection, frozen renewal principal, monotonic relief, intact-state reconstruction, unaccepted-finance follow-up blocking, exclusive current-party programme enable/idempotency, and later settlement completing displacement recovery. The reviewer inspected the tests and recorded result. These deliberately limited transaction models are **not** an HOI4 engine emulator, an engine parser or a multiplayer synchronization test.

The remaining limits are implementation boundaries, not unresolved claims of completed features: Greek/Turkish national trees and their full event chains remain future work; later foreign content must invoke the actor-owned callbacks after real authorized choices; actual second-phase combat and a combat-stopping, ownership-preserving ceasefire require a tested military adapter. No first-phase combat flag alone establishes an engine ceasefire. Existing deferred armies/navies/air forces remain deferred, so this review does not certify a playable historical invasion. Native focus auto-completion, state/country dynamic modifier refresh, queued naval construction, country history/leader dispatch, hotjoin/reserved-seat behaviour and authoritative multiplayer ordering still need direct HOI4 validation.

No runtime or generator file was edited by this review agent. Only this report was changed.
