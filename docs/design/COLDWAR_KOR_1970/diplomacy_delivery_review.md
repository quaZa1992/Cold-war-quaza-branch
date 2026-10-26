# South Korea diplomacy delivery review

## Scope and confidence

This is a source audit of the installed `COLDWAR_KOR_1970` focus, event, scripted-effect, and English-localisation files, cross-checked against the compiler/runtime helpers and design record. It does not establish that the live game loaded these files or rendered the reported tooltip. No live-engine event, tooltip, or save test was available for this review.

Relevant installed files:

- `common/national_focus/COLDWAR_KOR_1970_focus.txt`
- `common/scripted_effects/COLDWAR_KOR_1970_focus.txt`
- `common/scripted_effects/COLDWAR_KOR_1970_foreign.txt`
- `common/scripted_triggers/COLDWAR_KOR_1970_foreign.txt`
- `events/COLDWAR_KOR_1970_foreign.txt`
- `common/dynamic_modifiers/COLDWAR_KOR_1970_foreign.txt`
- `localisation/english/COLDWAR_KOR_1970_l_english.yml`

## Findings

### 1. Working Contacts is an offer-only focus, and acceptance has no material payoff

`COLDWAR_KOR_reciprocal_contacts` displays only `COLDWAR_KOR_working_contacts_offer_tt` and calls `COLDWAR_KOR_complete_reciprocal_contacts` (`common/national_focus/COLDWAR_KOR_1970_focus.txt:5391-5408`). Completion records the focus as paid and sends an offer; it adds no modifier, treasury change, construction, or other direct reward (`common/scripted_effects/COLDWAR_KOR_1970_focus.txt:2735-2743`). The current offer tooltip says only that ratification “Establishes the agreed diplomatic framework” (`localisation/english/COLDWAR_KOR_1970_l_english.yml:3760`).

The recipient event is real: North Korea receives `COLDWAR_KOR_foreign.6`, with accept, decline, and ineligible-state options (`events/COLDWAR_KOR_1970_foreign.txt:251-272`). Acceptance only records mutual signed flags, clears pending state, refreshes Korea’s programmes, and sends Korea event `.106`; it does not charge either country or add an idea/modifier (`common/scripted_effects/COLDWAR_KOR_1970_foreign.txt:574-604`). The agreement is used as a prerequisite for later settlement focuses, so that unlock is its actual gameplay effect. It is not a passive military, industrial, or economic bonus.

The tooltip is therefore technically accurate but uninformative. Replace “agreed diplomatic framework” with the concrete terms and unlock: e.g. official working-level contact, no payment or passive modifier, and that ratification enables the subsequent Korean settlement route. That gives a substantive preview without inventing a payout.

### 2. “Peninsula Policy” and “Diplomatic Review” already have material, non-agreement rewards

These root focuses are paid national policies, not foreign offers. `COLDWAR_KOR_diplomatic_review` charges $1bn, sets trade opinion +0.05 and bureaucracy-cost modifier +0.03, and refreshes active programmes (`common/scripted_effects/COLDWAR_KOR_1970_focus.txt:2404-2417`). `COLDWAR_KOR_review_korean_policy` likewise charges $1bn, sets foreign-influence defence +0.04 and bureaucracy-cost modifier +0.03, then refreshes (`common/scripted_effects/COLDWAR_KOR_1970_focus.txt:2668-2682`). Both focus blocks display preview ideas, but the displayed reward is primarily idea flavour text; neither has an accept/decline event because neither proposes terms to another country (`common/national_focus/COLDWAR_KOR_1970_focus.txt:4770-4789`, around `4980-5000`).

If the desired feature is an offer to other countries, add a distinct follow-on action/focus or proposal. Do not convert these already-paid domestic reviews into recipient agreements without changing their ownership/intent. A dedicated U.S. garrison-and-exercises branch should likewise have its own recipient event and contract state, rather than presenting current policy-focus rewards as if they were bilateral terms.

### 3. Recipient decisions and proposer feedback exist; proposer feedback is too generic

For Working Contacts, the offer sends `.6` to NKO and schedules a 61-day expiry check for KOR (`common/scripted_effects/COLDWAR_KOR_1970_foreign.txt:552-572`). Acceptance sends KOR `.106`; refusal also clears state and sends `.106`; expiry uses `.206` (`same file:574-644`). KOR receives a response event in source, so the recipient-response path is not missing.

However, `.106` is the same event after acceptance and refusal. Its description says only that “The parties have recorded their decision” (`events/COLDWAR_KOR_1970_foreign.txt:276-281`; localisation lines 1071-1073). That is not false, but it does not tell the proposer whether the offer was accepted or declined. The `.206` expiry event is explicitly identified as expiration (localisation lines 1224-1226). Recommendation: route accept and refuse through distinct sender reply events or pass a signed/refused outcome that the reply event can display; retain the already-specific expiry reply. Apply this to the other recipient contracts if they use the same generic reply pattern.

### 4. Offers mostly show costs and duration, not the benefit purchased

The English offer summaries frequently list only the South Korean/each-government contribution, weekly upkeep, and duration. Examples include American Alliance Assurances, Military Staff Cooperation, Japanese Technical Cooperation, and Allied Procurement (`localisation/english/COLDWAR_KOR_1970_l_english.yml:144, 1552, 3374, 3685`). Framework offers—Working Contacts, Red Cross Liaison, Nonaggression Compact, Reciprocal Recognition, and several dialogue/notification offers—say only “Establishes the agreed diplomatic framework” (`same file: 1856, 1937, 2129, 3760`, with related keys noted below).

The event-side acceptance previews also tend to show only the commitment and duration. For example, `.6.accepted_tt` repeats the framework wording (`localisation/english/COLDWAR_KOR_1970_l_english.yml:1388-1393`). When a contract grants a measurable modifier, include its actual numeric effect in the proposer preview and recipient accept-option tooltip, alongside who pays, weekly cost, and duration. For a deliberately non-material diplomatic framework, state the concrete flag-based consequence/unlock and explicitly say “No passive modifier or payment” rather than promising a material benefit. Keep display and executed helper values in sync.

### 5. Existing U.S.-related defence content is procurement and staff cooperation, not garrison or drills

The documented defence group contains 28 nodes; its U.S.-specific bilateral offer is `COLDWAR_KOR_allied_procurement` (American procurement offer) and the follow-up `COLDWAR_KOR_licensed_maintenance` requires the accepted contract. The foreign group separately contains `COLDWAR_KOR_alliance_bargain` (U.S. alliance assurance) and `COLDWAR_KOR_diverse_partners` (security staff cooperation can target USA or Japan). Their offer strings describe contributions/upkeep and three-year terms, but do not define U.S. troop stationing or joint exercises. The current installed USA-targetable security offer should not be described as a garrison/drill agreement.

For a dedicated U.S. garrison/drills branch, the source-backed implementation shape is an explicit KOR proposal → U.S. accept/decline event → accepted-only, revalidated bilateral effect → distinct proposer outcome reply → expiry/cleanup. Define whether this means a temporary bilateral modifier, a real U.S. division transfer, or both before choosing an effect. Do not imply a real garrison through a modifier alone. Show the Korean and American costs, duration, and the numerical benefit in both proposal and recipient-option tooltips. Static source cannot establish whether U.S. AI accepts, whether a new division transfer is valid in all relevant scopes, or whether the tooltip/event fires in a live campaign.

## Agreement-only inventory

The design record’s `contracts` entries explicitly identify zero-cost, zero-upkeep frameworks with empty policy and recipient-effect payloads. The matching installed focus/action paths should be treated as diplomatic unlocks, not as material rewards, unless the accepted helper actually adds a modifier or other effect:

- Korea group: `COLDWAR_KOR_red_cross_channel`, `COLDWAR_KOR_reciprocal_contacts` (Working Contacts), `COLDWAR_KOR_two_governments` (Parallel Recognition), `COLDWAR_KOR_civilian_exchange_priority` (Cultural Exchange Framework), `COLDWAR_KOR_verification_priority` (Military Notification Talks), `COLDWAR_KOR_community_dialogue`.
- Foreign group: `COLDWAR_KOR_claims_first` (Historical Claims Talks), `COLDWAR_KOR_nordpolitik` (recognition offer; proposal is bilateral/stateful, not immediate material reward), and the neutrality-guarantees route where present in the wider policy path.

This inventory is about the agreement proposal itself, not the focus’ prerequisite/history value. Several focus completions also create a receipt flag that makes later focuses available. The Nonaggression Compact is a special case: its acceptance applies a native bilateral non-aggression relation, so it has a concrete diplomatic effect even though it has no passive modifier or cost. Conversely, where an accepted agreement applies paid bonuses, those are separate from the offer-only focus reward and should be stated explicitly.

## Requested group inventory

For cross-checking against the installed focus IDs, the design record lists these complete groups:

- **Foreign (21):** diplomatic_review; alliance_bargain; strategic_autonomy; burden_sharing; diverse_partners; vietnam_legacy; japan_pragmatism; claims_first; joint_technical_training; alternative_capital; overseas_workers; nordpolitik; pacific_exports; middle_power; overseas_commercial_service; middle_east_bids; pacific_standards; contract_worker_protection; international_quality; professional_trade_missions; public_treaty_process.
- **Korea (23):** korean_question; red_cross_channel; armed_vigilance; family_reunions; incident_hotline; review_korean_policy; peaceful_coexistence; competitive_legitimacy; verified_restraint; defector_protection; reciprocal_contacts; sovereign_confederation; two_governments; confederal_secretariat; limited_trade; korean_settlement; korean_implementation_review; civilian_exchange_priority; verification_priority; cultural_visits; border_notice_protocol; peninsula_liaison_office; community_dialogue.
- **Defence (28):** defence_review; dmz_deterrence; mobile_deterrence; counter_infiltration_units; combined_arms_training; defence_logistics; allied_procurement; domestic_defence_industry; licensed_maintenance; changwon_production; defence_quality; reserve_army; professional_core; civil_defence_training; career_ncos; joint_staff; coastal_defence; air_defence; coastal_logistics; air_command; yulgok_readiness_review; air_cover_priority; aircrew_training; escort_priority; escort_staff; counterbattery_priority; fire_direction; joint_readiness_audits.

These counts/IDs are from `docs/design/COLDWAR_KOR_1970/COLDWAR_KOR_design.json`. That document labels itself a concept awaiting owner approval, so it is an inventory aid; the installed scripts and localisation above are the runtime-source evidence.

## Recommended implementation order

1. Rewrite Working Contacts’ proposal and recipient acceptance preview to explain the real consequence (official contacts + later-focus unlock) and explicitly state that it has no payment or passive modifier.
2. Make sender outcome messages distinguish accepted, declined, and expired proposals. Preserve refusal/expiry flags and existing cooldown behavior.
3. Add measurable benefit lines to every numeric agreement preview and recipient acceptance option by copying values from the accepted helper and modifier definition; where no benefit exists, say so and identify the unlocked route.
4. Build the requested U.S. garrison/exercises branch as a separate bilateral contract, with concrete scope, costs, benefits, duration, refusal, expiry, and cleanup. Verify U.S. recipient behavior and any unit-transfer effect in a live game before describing it as actual stationing.
5. Run a live campaign check for the 1970 start to confirm loaded focus tooltips, NKO/USA event arrival, accepted/refused/expired replies, and that no agreement payment or effect fires before acceptance.

## Final emitted-source revision audit (2026-10-25)

This follow-up reviews the emitted files in `tools/COLDWAR_KOR_1970_concept/runtime_staged`, including the new agreement, term-review, preview, and USFK exercise modules. It is a static source audit; it does not confirm that the live game loaded the staged output or rendered its tooltips. The earlier findings above describe the pre-revision installed source and should not be read as findings against this staged revision.

### Result

I found no source-level blocker in the requested checks:

- **Old-save agreements:** `COLDWAR_KOR_upgrade_agreement_terms` runs from daily contract maintenance. For each revised offer/agreement, it recognizes signed or pending legacy terms without the current `*_terms_v3` / `*_offer_v3` marker, clears both countries' old state, and queues sender notice `.700`. Changed bonuses and recurring charges are gated on the current term markers for both parties. The existing legacy Working Contacts flag is preserved for its compatibility handling, but no new charge is imposed until a fresh offer is accepted. The generator's `COLDWAR_KOR_delivery_validate.py` exercises this old-save path for Working Contacts; this audit also checked the term-review and guards present for the other revised agreement families.
- **USFK permissions and membership:** the live cooperation trigger requires sovereign KOR and USA, both membership ideas, no KOR-USA war, and a mutually signed garrison or drawdown agreement. The first garrison acceptance grants USA military access only when absent and records that this feature granted it; expiry/end cleanup removes only feature-granted access. Drawdown ratification aborts any exercise, ends the stationing agreement, and retains bilateral membership while drawdown cooperation is live. Reconciliation removes stale membership when neither agreement remains live.
- **Focus gates:** the initial stationing proposal is reachable before membership exists. The later alliance, burden-sharing, and combined-exercises focuses require the member idea in both availability and runtime completion guards. The domestic Korean-led defence policy remains separate from the bilateral drawdown acceptance, consistent with the intended design.
- **Preview versus execution:** acceptance-event and focus previews use static native ideas with the same coefficients as the emitted dynamic modifiers. Offer strings show payer and weekly amount, term length, and the proposal's concrete purpose. The staged delivery validator additionally compares preview coefficients against modifier data. I found no numeric preview mismatch in the inspected USFK proposal values.
- **Exercises:** USA assent alone does not charge or grant training outcomes. Korean launch remains separately guarded by live bilateral cooperation, current sender/office state, both-country assent, and training feasibility. Costs accrue only during an active training window; field outcomes require both armies, temporary access is tracked and removed only when the exercise granted it, and expiry/war/feasibility loss routes through cleanup.
- **Outcome messages:** the new agreement accept, decline, and expiry routes use distinct sender replies. Exercise assent, refusal, cancellation, and expiry are also separately reported.

One small localization polish remains: `COLDWAR_KOR_us_garrison_offer_tt` says “Each counterpart’s upkeep” for the USA's $4 million/week share. “United States upkeep” would name the payer more directly. This is wording only and does not affect the script scopes or amounts.

The above conclusions are based on generated source and the validator's source-model scenarios. A live-engine check is still needed to verify actual dynamic modifier loading, event delivery, native idea tooltip rendering, and weekly account changes in the installed 1970 campaign.
