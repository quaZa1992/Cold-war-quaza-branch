# South Korea 1970–1990 expansion mechanics review

**Review scope:** current 298-focus concept JSON and `tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_expansion.py`, with the generated native recipes. This is a read-only mechanics audit; no loaded game files or concept data were changed. The report reflects the files read on 24 October 2026 and should be refreshed after the parent’s pending event/state/provider-ledger corrections.

## Findings requiring concept/provider closure

### 1. The constitutional referendum rejection path is still a dead end

`transition_system.ratification.reject` says the chosen model remains selected and a repeatable 50 PP redraft decision becomes available after 90 days (`COLDWAR_KOR_design.json`, `transition_system.ratification`; `COLDWAR_KOR_expansion.py:334–337`). However, the chosen model focus and `COLDWAR_KOR_constitution_referendum` are one-shot completed focuses. The models are focus-level mutually exclusive, the referendum focus is paid once, and the current action catalogue has no redraft action/decision ID, event, guard, or effects that reopen submission. A rejection therefore leaves no native focus route to choose a replacement model or resubmit. Specify a concrete repeatable decision/event that either reopens the same model for another ballot or allows selection of a new model and launches its ballot; include its cooldown, PP charge, model flag update, and no-replay rules. No focus reset should be needed.

### 2. Military command failure and the three transition-entry receipts lack setters

The exact focus gates require `COLDWAR_KOR_electoral_opening`, `COLDWAR_KOR_caretaker_installed`, or `COLDWAR_KOR_military_opening_authorized` (`COLDWAR_KOR_expansion.py:222–230`; generated exact recipes in `COLDWAR_KOR_native_recipes.md` around the transition entries). Current `transition_events` entries describe choices and consequences in prose, but do not give concrete event/decision option code mapping those outcomes to these receipts. The military challenge description also says failure permits a later authorized military opening, but that authorization has no setter or action provider in the current module. Add explicit outcome-to-flag recipes and define the lost-command route’s later authorization. Without them, the entry focuses are correctly guarded but unreachable from the described content.

### 3. Ratification electorate needs an executable participant definition and a denominator guard

The stated vote model is an abstraction over the unique current party/organization slots that support the charter, divided by legal participating shares, with a strict >50% threshold. `register_charter_participants` is only a named action; neither it nor `transition_system.ratification` enumerates which real slots count as supporters/participants, how slots are registered/removed when the legal coalition changes, or what happens if no legal participants remain. Define a stable slot table and update rules; make zero denominator an explicit non-pass that cannot produce NaN/divide-by-zero. The UI should display the exact current numerator, denominator, and result rule. The current design’s “no bonus popularity” constraint is sound.

### 4. Refusal bypass is semantically viable; generated native recipe should expose it explicitly

The two offer-dependent follow-ups (`cultural_visits`, `border_notice_protocol`) correctly keep signed-contract conditions in their availability and completion guards, while refusal/expiry is metadata for a native focus `bypass` block. A native bypass skips the focus without running `completion_reward`; it must not be merged into the reward guard. The builder currently records `node.bypass` with `native_pattern` in `COLDWAR_KOR_expansion.py:207–210`, but emitted JSON/Markdown recipes do not yet expose a `native_bypass_body`. Treat this as a missing emission detail, not an impossible route. Before implementation, emit the exact `OR = { refused expired }` bypass body and verify each provider sets exactly one terminal receipt, with no payment or agreement reward.

## Verified mechanics and remaining implementation boundaries

### Native modifier readers

- `civilian_factories_productivity` is a country-scoped percentage registered in `common/modifier_definitions/money_modifier_definitions.txt:381–386`. The readers at `common/scripted_effects/00_money_system.txt:469` and `:6027` change civilian-factory tax and its GDP contribution. The GDP factors are both 10, so +0.06 is +6% to those civilian-factory components, not +6% to total national GDP, HOI4 production-line output, or military production. The current label/caveat in the concept is accurate.
- `dockyard_productivity` is also supported, registered at `money_modifier_definitions.txt:395–400` and read at `00_money_system.txt:511` (dockyard tax) and `:6041` (dockyard GDP). The `commercial_shipyards` policy value +0.18 applies to the commercial dockyard tax/GDP contribution, not military shipyard output (`industrial_capacity_dockyard`). Its “commercial” framing is mechanically correct.
- The earlier modifier audit found no unsupported modifier among the prior 206-node set. Current expansion additions use the same validated native catalogue plus `dockyard_productivity`; verify the parent’s stacking/profile ledger against each exact policy-slot replacement after the final build. A present modifier token is not itself proof of the proposed new KOR dynamic modifier’s aggregation.
- The native focus leaf writes policy variables only. The concept explicitly states that the new `COLDWAR_KOR_refresh_programmes` provider must aggregate the latest earned policy for each qualified owner/slot and apply one dynamic modifier; this is new KOR code, not an existing MD API. The same applies to `COLDWAR_KOR_calculate_weekly_cost`, offer handlers, politics sync, transition event routes, rollbacks, ratification, and membership/legacy adapters.

### Weekly and agreement money

- The current JSON has 29 contracts and all 29 specify `KOR_cost_bn`, `KOR_weekly_bn`, and `duration_days`; recurring amounts are expressed in weekly billions and literals observed are within five decimal places. Examples: `family_reunions` costs $1bn once and $0.001bn/week for 1,095 days; `limited_trade` costs $1bn once and $0.002bn/week for 1,095 days. Where a recipient pays too, its own once/weekly terms are represented separately in `recipient_effects`.
- The native money API is weekly: `calculate_additional_expense_rate` reconstructs `additional_expenses_rate` in `common/scripted_effects/00_money_system.txt:3663–3681`; treasury mutations use the native billion-dollar `modify_treasury_effect` interface. The named new KOR aggregator is necessary to charge active policy commitments and bilateral agreements once per weekly accounting cycle and to stop charges at expiry/termination. Avoid monthly direct treasury deductions or treating the recipient event’s `ROOT` as KOR.
- Current domestic commitment records use one owner-qualified expense slot per focus record; repeated `slot` values across alternatives are intentional replacement groups, not additive charges. The implementation must choose exactly one latest active value for each owner/slot and clear a slot when a selected zero-cost policy replaces it. The only modifiers/costs should be active for the proper owner and active settlement; one-time focus effects remain behind once-only paid receipts.

### Transition semantics checked

- Exact native gates separate route receipts from ordinary focus prerequisites. `authorize_talks` requires `negotiating_commitment`; the mandate requires one electoral-ticket option and one accountability option; a model endpoint precedes the referendum; `impartial_election_board` requires the ratification-pass receipt; constitutional institutions require `constitutional_order`; orderly handover additionally requires `lawful_election_completed`. No current declaration directly sets democratic government or installs a predetermined winner.
- `defend_civil_command` is an action node whose outcome must be resolved by its proposed event provider. `transition_system.military_failure` correctly forbids automatic Chun accession and calls for a later authorized route, but concrete successful/failed outcome flag recipes remain the gap listed above.
- The current `impartial_election_board` body repeats `has_country_flag = COLDWAR_KOR_constitutional_ratification_passed` twice (`COLDWAR_KOR_expansion.py:285` and `:364`). This duplicate is harmless but should be deduplicated in the emitter.
- The transition root’s text gate says “actual crisis, mandate and constitutional states,” while its exact generated gate only checks KOR, 1970 scenario, and independence. Since this focus is a paid dossier/review opener, this can be intentional; align the group/root gate wording so it does not suggest the crisis is an engine-enforced prerequisite.
- `emergency_decrees` and `dynastic_presidency` exact generated gates include `constitution_yushin`; `press_consolidation` includes `constitution_controlled_fifth`. These latest correction guards now agree with their proposed receipt semantics.

### Nuclear gate and buildings

- `civil_nuclear` now checks `COLDWAR_nuc_economy_allows = yes`, `has_tech = reactor1`, and `country_can_build_nuclear_reactors = yes` in both its exact start and completion gate (`COLDWAR_KOR_expansion.py:365–367`). The nuclear trigger/effects and funded weekly development budget exist in the MD nuclear subsystem. The concept still relies on new action adapters to reveal only existing paid civil projects; it grants no reactor, weapon, uranium production, mine, or deposit.
- Construction targets use real KOR state IDs 604–608, all found in `history/states/604-Gyeonggi.txt` through `608-Jeju.txt`; these state files identify KOR ownership. The generated construction gate checks state ownership/control and free building slots (`COLDWAR_KOR_native_plan.py:124–128`). Exact post-1970 state building-slot/capacity legality still depends on the parent’s provider ledger; the gate is preferable to assuming a construction reward always fits. `commercial_shipyards` and `coastal_logistics` use state 605 dockyards; there is one starting dockyard in its state history, so the dynamic slot check is material.

## Approval-stage classification

All content beginning `COLDWAR_KOR_` in the recipes (dynamic modifiers, weekly aggregator, political router, transition actions/events, voter registration, rollback/court/press/civilian-command readers, legacy treaty adapter, membership idea and atomic offer handling) is proposed new KOR content. Existing MD APIs include the cited money readers, modifier definitions, nuclear gates/budget, state-scope construction, and `change_ruling_party_effect`; proposed wrappers/hooks are not installed code. No game files were modified by this review.

## Revision review: `COLDWAR_KOR_transition_plan.py`

Reviewed the new approval-stage provider plan, including its wiring into the builder between `expand` and `declare`. This addendum reflects the transition-plan source itself; the generated JSON/preview may still be rebuilding.

### Prior issues resolved at plan level

- **Referendum rejection retry:** resolved in concept. The new repeatable `COLDWAR_KOR_reopen_charter_ballot` decision requires `charter_rejected`, no pending ballot, no retry cooldown, and a selected model; it charges 50 PP, sets pending and schedules the existing ballot event. Rejection preserves the selected model and begins a 90-day cooldown. This is a coherent same-model resubmission without focus reset or reward replay. It intentionally does not permit switching model after rejection.
- **Entry receipts:** the 1971 competitive choice now maps to `electoral_opening`, the 1979 caretaker outcome uses a named Choi installation provider, and the 1987 concession maps to `military_opening_authorized`. These close the previous missing-setter gap in the plan. The Choi and political authorization providers still need exact executable guard bodies as noted below.
- **Electorate table and zero denominator:** the ballot model now enumerates ordinary slots 0–3, conditional slots 4/5/19/22, excludes KCIA/EPB/non-party associations, counts each eligible party once, and treats zero legal electorate as non-passing. `party_pop_array^s`, `party_banned_array^s`, `add_to_temp_variable`, `value = … divide = … clamp = { min = 0 max = 1 }`, and `check_variable` forms have current MD usage/pattern support (examples include `common/scripted_effects/IMP_1970_fossil_starting_capacity.txt:12`, `common/scripted_effects/00_MD_politicsview_scripted_effects.txt:2115–2173`, and the existing national decision/effect array readers). This resolves the prior prose-only denominator issue at concept level.
- **Judicial review timing:** the plan correctly distinguishes the 1987 constitutional legal basis from 1988 operational review and adds `judicial_review_operational` to the court modifier’s active trigger. This is the right two-stage lifecycle, but the event/focus wiring currently bypasses the stated implementation requirement (see below).

### Remaining concrete issues

1. **`reopen_constitutional_talks` still has an underspecified executable guard.** Its `available` block checks KOR/1970, `military_reconsolidation`, and the cooldown; the “current government authorizes talks” and “legal opposition has issued the registered constitutional demand” constraints exist only in `additional_guard` prose. As emitted, any KOR government retaining the reconsolidation receipt can take it. Add explicit office/party or authorization and opposition-demand receipt checks to `available`; do not rely on tooltip text or an uncompiled prose guard.

2. **The command event trigger has no exact pending-receipt setter.** `COLDWAR_KOR_transition.12` requires `command_settlement_pending`, and the focus schedules it one day after `defend_civil_command`. The plan describes `resolve_command_challenge` as the action and gives success/failure narratives, but does not specify the exact effect that sets `command_settlement_pending` and makes a selected outcome available before the event fires. Add a concrete pre-event state/effect or make the action itself create and resolve an explicit event with pending outcome receipts. Otherwise the scheduled event may fail its trigger and be lost.

3. **Transition event outcomes remain partly prose, not executable recipes.** `.12` success/failure and `.30` pass/reject fields are strings such as “Set…; clear…” rather than explicit native effect bodies. The ballot formula is substantially better specified, but an implementation recipe still needs the actual `immediate` placement, outcome option guards/effects, cooldown flag syntax, and the selector mapping from `charter_model` 1/2/3 to exactly one constitution receipt. The new Choi provider also gives a native effect body, but its `guard` remains prose and its office/pool dispatcher is explicitly new code. Keep these separated as proposed new providers rather than claiming they are current MD callbacks.

4. **Court focus schedules automatic activation after 90 days.** `independent_constitutional_court` appends `country_event = { id = COLDWAR_KOR_transition.88 days = 90 }`; event `.88` only checks `judicial_review` and `constitutional_order`, then unconditionally sets `judicial_review_operational`. That does not require appointments or implementation and makes the 1988 operational stage automatic 90 days after a focus, including alternate early transitions. The separate `court_1988` history-event description says appointments/implementation must be complete but is not wired as the actual provider. Remove the automatic scheduled grant or gate `.88` on a distinct appointment/implementation receipt set by the real implementation choice/event.

5. **Transition event IDs vs native event callback details:** The plan assigns `.12`, `.30`, `.88`, and many historical event IDs as new content. Check event-ID uniqueness before emission and ensure each event has actual trigger/option script. This is an implementation checklist rather than evidence of an existing MD event API.

### Status update

The prior dead-end referendum retry, missing entry receipt mapping, and missing electorate/zero-denominator specification are now resolved at concept level by `COLDWAR_KOR_transition_plan.py`. The refusal-bypass point remains a generator output detail until `native_bypass_body` is emitted. Outstanding blockers are the overly broad talks decision guard, command pending-receipt setup, executable ballot/command outcome bodies, and court auto-activation without appointments/implementation.

## Final disposition: latest rebuilt concept

Rechecked the latest rebuilt `COLDWAR_KOR_design.json`, `COLDWAR_KOR_native_recipes.md`, `COLDWAR_KOR_transition_plan.py`, and `COLDWAR_KOR_native_plan.py`; this section supersedes the outstanding-item status in the prior revision review.

### Previous findings now closed

- `reopen_constitutional_talks` now has executable checks for KOR/1970, ruling party 22, military reconsolidation, registered opposition constitutional demand, no active constitutional order, and no cooldown. It now gates the specified actors and state rather than relying on `additional_guard` prose alone.
- `defend_civil_command` explicitly sets `command_settlement_pending` before scheduling event `.12`.
- The ballot has a concrete support-share calculation, bounded model check (1–3), pass/reject native effect bodies and guarded resubmission. It preserves the same chosen model, charges 50 PP on each retry, and does not replay the one-shot focus reward.
- The court focus now only records the legal basis. Operational review requires the once-only implementation decision, paid $1bn/50 PP, appointment and pending receipts, a 90-day commissioning delay, constitutional order, and a delayed event; the focus no longer schedules automatic activation. The declared monthly/restoration maintenance hook resumes an already paid, matured installation after interruption without another payment.
- The generated JSON/native recipe now carries a separate `native_bypass_body` for treaty-only follow-ups, so refusal/expiry can bypass without entering completion rewards.

### Remaining concept defect in the inspected snapshot

1. **Talks reopening can be purchased repeatedly.** The decision is repeatable and its effect sets `military_opening_authorized` plus a 90-day cooldown, but availability does not require that authorization to be absent or the transition to be not already open/completed. The effect also leaves `military_reconsolidation` and the opposition-demand receipt in place. Once its cooldown expires, the same government can pay another 75 PP and reapply the same authorization while the negotiated opening is already active. Add a one-use lock while `military_opening_authorized`/`transition_open` is active, or clear/consume the reconsolidation authorization in the opening transition and specify the later reauthorization rule.

2. **Command outcome is an intentional player-facing RP abstraction.** The parent clarified that event `.12` is the command-resolution choice itself, not a result roll following an external command statistic. Under this contract, the success option guard (caretaker installed and no nationwide martial law) appropriately restricts “Reorganize and Uphold Civil Command”; “Yield the Command” is the explicit alternative-history outcome and does not require a separate success receipt. The success option’s 75 PP/$1bn/90-day disruption and no-leader-appointment safeguards are coherent. This is not a blocker provided the emitted event presents those as mutually understandable player choices and its choice tooltips state the costs/outcomes.

### Verified syntax and lifecycle notes

- Timed `set_country_flag = { flag = … days = … }` is used in current MD source. The variable-array and temp-variable calculation forms also match existing MD practice; the generated vote computes only over enumerated eligible, non-banned slots and explicitly avoids division when the electorate is zero.
- The court decision’s event is scheduled for the same 90-day duration as its timed commissioning-delay flag. The event requires the delay flag to have expired; if engine tick ordering defers it, the declared monthly/restoration maintenance recipe is the recovery path. Keep that hook in the actual future implementation and ensure it is idempotent.
- The remaining `COLDWAR_KOR_*` event/decision actions, router, maintenance, and readers are proposed new KOR providers. The review verifies their concept guards and separation of effects, not runtime behavior in installed game files.


## Final check: reopening replay fix verified

Rechecked the rebuilt concept JSON against SHA-256 `bccc89cc0124842ed5db421e7c1920c9046b458fdd31b4851db5a693bb19c3dd`. This is the final snapshot named for this check.

`COLDWAR_KOR_reopen_constitutional_talks` now has executable `NOT` guards for `military_opening_authorized`, `transition_open`, and `talks_authorized`, in addition to the prior government, reconsolidation, opposition-demand, order, and cooldown conditions. Its effect clears `military_reconsolidation` when it sets the authorization and cooldown. The `.12` failure body clears both `transition_open` and `military_opening_authorized`, leaving reconsolidation as the new state receipt. Thus the 75 PP authorization cannot be repurchased while its opening is active or already authorized, and a future route must first return to the failed/reconsolidated state. The final repeated-purchase issue is closed in this JSON.

The command event also carries the explicit `resolution_mode` contract: the player-facing “Reorganize and Uphold Civil Command” vs “Yield the Command” options resolve the command challenge itself. Under that declared RP abstraction, no external random-success result or invented command meter is required; the success option remains guarded by the installed caretaker and absence of nationwide martial law.
