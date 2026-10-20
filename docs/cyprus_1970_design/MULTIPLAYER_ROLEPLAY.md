# Cyprus crisis: multiplayer roleplay concept

**Concept only.** No runtime, tree, event or generator changes are included. Future Greek and Turkish trees/events should connect to this contract; they are not being written now. Reviewed sources: `WAR_MECHANICS.md`, `cyprus_crisis.py`, `build_design.py`, native MD events, and the local Imperia Cold War hooks. All `COLDWAR_CYP_1970_rp_*` names below are **proposed new definitions**, not existing APIs.

Assume GRE, TUR and ENG are human seats. CYP can be a human seat or an explicitly dedicated historical AI seat. Historical CYP policy must never become a mechanism for selecting another country's policy.

## Three separate layers

| Layer | Meaning | Owner | Example | What it cannot establish |
|---|---|---|---|---|
| 1. Historical policy / intention | What the current Cypriot government wants and chooses to propose | CYP, with deterministic historical selection only in a dedicated CYP AI seat | Makarios seeks independent sovereignty, investigates armed opponents, requests an officer withdrawal and seeks mediation | Greek agreement, a successful withdrawal, a coup, Turkish intervention or a signed treaty |
| 2. Authorized foreign action | A substantive choice made by the relevant foreign player | GRE, TUR or ENG; separate Turkish Cypriot mandate for community decisions | Greece accepts/rejects withdrawal; Turkey issues an ultimatum or chooses continued diplomacy; Britain declines joint intervention | That troops have departed, a coup succeeded, a landing occurred, or every other party consented |
| 3. Actual result | A verified implemented agreement, failed/successful operation, engine war or negotiated outcome | One guarded outcome resolver observes/applies the specific result | Withdrawal implemented; coup defeated; TUR–CYP war actually begins; ceasefire terms accepted by its necessary parties | Universal historical inevitability, recognition of a territorial claim, or permission to replay rewards |

Keep separate fields for **policy chosen**, **offer sent**, **reply received**, **action authorized**, **implementation pending**, and **actual outcome**. A human player's adverse outcome can be imposed by a legitimate hostile action and its resolution; consent is required from the actor making that action, not from every opponent it affects. Payments, agreements and joint operations require the assent of their actual participants.

## Roles and ownership

| Role | Controls | Cannot control |
|---|---|---|
| CYP government | Its own security policy, command reforms, diplomacy, responses to live proposals, civilian protection and military defence | Ankara's intervention decision; Greek coup sponsorship; British participation; Turkish Cypriot assent |
| GRE government | Its officer policy, sponsorship/restraint of a plot, aid, withdrawal and any separately authorized military action | Guaranteed coup success or a Turkish response |
| TUR government | Consultation, actual ultimatum terms, diplomacy, readiness and explicit military decisions | Turkish Cypriot consent by substitution, guaranteed landing success, British participation or Greek withdrawal |
| ENG government | Mediation, invitations, base policy, requested aid/joint action, its own participation | Automatic sovereignty over an agreed Cyprus settlement, automatic permission from its allies, or a forced intervention |
| Turkish Cypriot representatives | Their own negotiating mandate, constitutional/security terms and community assent | The policy of all Turkey; automatic control of the whole CYP country |
| Session facilitator | Agreed RP scheduling and explicit player-seat reservation changes | Selecting a sovereign response, secretly ratifying a treaty, or changing military outcomes |
| Outcome coordinator | Validates records, executes a result once, updates the public crisis view and records milestones | Inventing foreign authorization to advance a historical script |

Before a later NCY country actually exists, the Turkish Cypriot role is an **internal counterpart**, not a country that is released to make messages possible. Use an independently resolved mandate with visible criteria. If the session appoints a human RP representative, record that delegation explicitly; it is not automatically the Turkish player. Otherwise use the documented counterpart policy and safeguards. Neither CYP AI nor a human CYP player simply chooses an obedient negotiator.

## Messages and decisions

Each proposed packet contains a crisis instance, actor, topic, request ID, revision, intended recipient, exact terms, stage, relevant deadlines and result status. These are a conceptual schema, not JavaScript-like objects available in HOI scripting. Later implementation can use country variables, flags and topic-specific bilateral slots in native MD style. Do not overwrite an unanswered ceasefire request with an unrelated aid offer merely because the recipient is the same country.

| Type | What the sender does | Substantive reply examples | What receipt means |
|---|---|---|---|
| Notice | Reports a coup, threat or other observed development | A subsequent independently chosen policy, if any | Delivered information only |
| Request | Asks for officer withdrawal, mediation, access or aid | Accept, refuse, or provide a specific counterproposal | No acceptance and no implementation |
| Invitation | Offers attendance at a defined conference | Accept attendance, decline attendance, propose a different time/format with concrete terms | No conference attendance and no agreement on its substance |
| Ultimatum | A sovereign actor issues specific demands and a deadline | Comply, reject, give a substantive counterproposal, or explicitly decline to decide | No compliance; expiry does not declare war |
| Terms / agreement | Circulates a versioned package | Each necessary actor signs, rejects or proposes a new revision | No treaty or signature |
| Operation decision | The actor decides its own coup support, intervention or renewed attack | This is an actor authorization, followed by a separate result | A policy statement is not a successful operation |

“Received”, “we will consider it”, opening a popup, requesting more RP time, acknowledging a notification and a delivery receipt are **procedural**. They are not a substantive guarantor response or agreement. “We will not participate in the proposed joint intervention” is a substantive refusal; “we acknowledge the invitation” is not. “We propose a conference on these stated terms” can be substantive, but it does not bind its invitees.

Silence produces **unanswered/expired**, not acceptance, rejection attributed to the player, a signature, a payment, a coup or war. A refused proposal and an unanswered proposal remain distinct in tooltips and AI reasoning. A sender can react to silence by making a new decision; the system does not make that decision for a human sender.

### Packet state and result matrix

| Current state | Valid next states | Trigger | Forbidden inference |
|---|---|---|---|
| Draft | Submitted / cancelled | Actual sender choice | Drafted terms were communicated |
| Submitted | Delivered / unavailable-recipient / cancelled | Routing validates current actors and instance | Delivery equals response |
| Delivered | Acknowledged / deferred / substantive reply / expired-unanswered | Receiver action or deadline | Acknowledgement equals agreement |
| Acknowledged / deferred | Substantive reply / extended / expired-unanswered | Explicit response or timing rule | A request for more time counts as war authorization |
| Substantive reply | Counterproposal / declined / accepted-in-principle / action-authorized | Valid actor, topic, instance and current revision | Acceptance in principle equals troop movement or full treaty implementation |
| Accepted-in-principle | Implementation-pending / terms-revised / agreement-lapsed | Required signatures and live prerequisites | A third party's absent signature is implied |
| Action-authorized / implementation-pending | Implemented / failed / suspended-for-human / cancelled-if-revocable | Sole result resolver and actual prerequisites | A coup order means a successful coup |
| Implemented / failed | Archived; new packet if needed | Result recorded once | Reopening a menu repeats rewards or costs |
| Expired-unanswered / declined / lapsed | Archived; revised or new packet if desired | Explicit new sender choice | Silence retrospectively becomes the historical decision |

Changing terms increments the revision and invalidates signatures for the old **changed** package. Do not silently transplant an actor's signature onto different demands. Distinguish a nonbinding exchange, a signed package and the verified implementation of its terms.

## `The Guarantors Respond`: one substantive response is enough

For `COLDWAR_CYP_1970_war_guarantors`, use the following threshold:

**The first valid, relevant, substantive GRE, TUR or ENG policy response in a live Cyprus crisis records the milestone.**

This is a **one-of-three** threshold, not unanimity. The title says that the guarantors have begun responding; it does not say that all three have replied, agreed, intervened or settled the crisis. This makes the threshold factually defensible and avoids one silent player holding every other channel hostage. A qualifying first response may be an actual Turkish ultimatum, a concrete British mediation initiative/refusal of requested joint action, or a Greek decision on the relevant coup/officer crisis. A proactive relevant action can qualify without waiting for CYP to send an invitation first.

The adapter checks:

1. The crisis exists and the response pertains to its current instance/topic, or a real external action creates and classifies a new relevant crisis.
2. The actor is an eligible GRE/TUR/ENG participant and its own event/decision or an observed actual action supplies the record.
3. The choice is substantive and authorized. Delivery, acknowledgement, RP hold, disconnected-seat standby and a stale reply do not count.
4. The reply is not duplicated, superseded or for another request revision.
5. The coordinator records the current response, then records the permanent focus marker if it has never been recorded.

After the first response:

- **Other GRE/TUR/ENG channels stay open.** No pending invitation, counterproposal or bilateral request is cancelled merely because the focus marker completed.
- Necessary signatures for an actual deal remain necessary; one response cannot implement a three-party treaty.
- Further responses update the current ledger and UI, without completing/rewarding the focus again.
- A player can act independently of whether the badge is visible. The event network must not require completion of this focus to recognize an actual war, send a response or hold a conference.
- If all three remain silent, the milestone remains unrecorded. CYP's own economy, command policy and ordinary diplomacy continue. The case can become unanswered/dormant; it is not labelled a peace settlement, and a later external action can reactivate or create a crisis.

**The focus badge is permanent and once-only across the campaign. It is never reset for a new crisis.** Each later crisis gets a fresh response/result ledger. `has_completed_focus = ...war_guarantors` may be used only to avoid repeating the historical badge; it must never answer “has the current crisis received a response?” or “is the current crisis peaceful?”

Example public UI:

> Historical milestone: **The Guarantors Respond — reached previously.**
>
> Current crisis **#4**: **1 of 3 substantive responses**. Greece: pending. Turkey: ultimatum issued. Britain: extension requested, no policy response yet. No ceasefire or settlement implemented.

If an actor no longer exists or is outside the relevant scenario, display it as unavailable rather than pretending it has replied. Show the actual eligible denominator. An unavailable actor cannot approve a guarantee or contribute a fake signature; the proposed terms may need revision.

## Historical CYP AI: deterministic policy, contingent world

The user's requirement is **always historical choices for a genuine CYP AI seat**, not a weighted preference among alternate political routes. It applies to CYP's offered political/response choices, not to foreign sovereign decisions or predetermined military success.

Every Cypriot event should declare a historical policy key for the **living/current government and actual context**, with a source-backed policy table. The proposed resolver selects that valid historical option deterministically and gives incompatible alternate choices zero AI weight. If no historical-context option is valid, it uses an explicit “await response / seek revised terms / continue own policy” fallback, rather than inventing a foreign agreement or choosing a random alternate regime. A missing mapping is an authoring issue, not permission to choose whichever option advances the calendar.

| Actual CYP context | Historical AI intention / offered choice | Foreign action it cannot choose | Possible actual divergence |
|---|---|---|---|
| Makarios government, 1970 | Continue the independent republic, investigate armed opposition, maintain talks and ordinary civil administration | Greek sponsorship, a successful assassination or Turkish intervention | Human GRE restrains networks; no later coup occurs |
| Makarios faces mainland-command confrontation | Pursue the historically grounded demand for civilian authority/officer withdrawal and defend his government | GRE's refusal, support for a putsch or a successful coup | GRE accepts withdrawal: CYP AI accepts an implemented result consistent with its own requested policy; it does not sabotage compliance to recreate history |
| An externally authorized putsch is attempted | Defend the presidency/constitutional authority through the actual resistance mechanics | Guarantee that the putsch succeeds or that Makarios dies | Attempt fails; Makarios remains and no Sampson branch is manufactured |
| Coup actually succeeds and Sampson's regime exists | Use that actual regime's mapped historical policies and responses, while retaining consequences and eventual succession/restoration conditions | Automatic Turkish war or British participation | TUR chooses diplomacy or no intervention; the regime's history continues under a different external situation |
| Constitutional/acting authority is actually restored | Use the current lawful government's mapped policies, mediation/ceasefire and constitutional positions | A universal signature on any package merely labelled “peace” | Negotiations succeed, fail or remain unanswered according to actual other players |
| Foreign intervention actually occurs | Defend, seek the historically grounded diplomatic/UN channel and select the documented offered responses | Forced enemy defeat, a guaranteed landing, a foreign ceasefire signature or fixed partition | War follows real/selected abstract results; no scripted final territorial reward |
| Negotiations have different terms from historical negotiations | Maintain the current government's sourced objectives through an explicit context mapping | Assume every new foreign demand was historically accepted | Revise, reject or seek time as mapped; do not manufacture a second offensive to match a date |

This table defines policy directions; future event authors must attach an exact eligible historical choice to each concrete event and government. It does not claim that every conceivable new RP offer has a known historical yes/no answer. Never translate “historical CYP AI” into “CYP organizes the coup against itself”, “Ankara must invade” or “all actors receive their historical regime even if the prerequisites were removed.”

Native `ai_chance` / `ai_will_do` shapes are reusable, but are not enough if several random alternatives remain eligible. A future deterministic CYP policy adapter is **new**. Earlier design text describing only “historical AI biases” needs reconciliation by the main designer for this dedicated seat mode. Human CYP retains its full policy choice.

## Player-seat reservation, disconnect and hotjoin

`is_ai = yes` describes present AI control. It does **not** prove that the country is an intentionally AI-owned slot, and it does not tell us whether a human disconnected. No automatic engine disconnect/hotjoin detector is asserted here.

Propose explicit session rules and persistent country-seat flags:

- `..._human_seat_reserved`: this country belongs to a human seat even when temporarily controlled by AI.
- `..._dedicated_historical_cyp_ai`: the session deliberately assigned CYP to historical AI.
- A session-declared facilitator and an agreed manual seat-claim/release procedure. These are new lobby/session rules, not an existing MD host-authority API.

GRE/TUR/ENG are reserved human seats by default in this MP concept. CYP is explicitly configured as either reserved human or dedicated historical AI. Historical automation requires **all** of: CYP is AI-controlled now, dedicated historical-AI mode is assigned, and no human reservation exists. A temporary AI takeover of a reserved CYP never satisfies that contract.

| Seat situation | Pending crisis behaviour |
|---|---|
| Human currently controls country | Present normal choices; only its own explicit choices authorize its actions |
| Reserved human seat temporarily AI-controlled | Hold pending sovereign choices; neutral standby only. No AI acceptance, refusal attributed to the human, coup sponsorship, war, payment or treaty decision |
| Dedicated historical CYP AI | Select the valid historical CYP policy deterministically; external action remains unchosen until its own actor acts |
| Human hotjoins a dedicated-AI country | Stop AI selection as soon as current human control is observed; claim/reserve the seat before resuming play. Show existing decisions/results, without undoing already valid history |
| Reserved human returns | Revalidate current requests/revisions and restore the human choice surface. Do not treat their earlier silence as a decision |
| Session deliberately releases a human slot to AI | Explicit facilitator/session change, recorded visibly; only then apply the selected AI policy, never inferred from elapsed disconnect time |

The facilitator should pause the actual game during a disconnect/seat change when possible. A custom RP-clock hold is not an engine-wide pause and cannot guarantee that unrelated native AI/combat stops. The new scenario's action wrappers can and must block pending sovereign choices for reserved AI seats. Complete protection from **other** pre-existing AI war systems would require those future integration paths to respect the same reservation policy, or an actual host pause. Do not promise otherwise.

At event creation and again at action execution, check reservation/current-control status. A neutral standby option should be safe if the engine auto-selects or dismisses a popup. It records a hold only; it does not qualify as a substantive guarantor response. Avoid handing a reserved AI a dangling new war goal and assuming it will await the custom decision: the final human authorization should create/execute the intended action atomically through the guarded actor path when possible. Already initiated combat does not rewind on disconnect, and a recorded completed payment is not repeated on reconnect.

All seat reservations, pending choices, instances, response revisions and outcome-applied ledgers must survive save/reload. A daily observer can read existing `is_ai` state; it is not an undocumented disconnect event and cannot retroactively close a race before it observed a newly joined player. Seat changes should therefore be confirmed before unpausing.

## Crisis clock and RP clock

Preparatory focuses retain their normal durations. Reactive choices use events/short decisions, with a **game-time crisis clock** independent of displayed focus duration. Suggested RP windows are balancing proposals, not historical timestamps:

- Ordinary diplomatic invitations: several game days, with an explicit request to extend or move the conference.
- A declared acute ultimatum: roughly 24–72 game hours as agreed by session rules; the issuer states the terms and can later choose what to do after expiry.
- Conference terms: a negotiated deadline, revision history and visible requests for extra time.

An RP hold freezes **that case's custom deadline counters** while the session discusses or waits for a reserved seat. Actual host pause freezes simulation normally. A custom hold must not claim to stop engine war, military movements, civilian damage already generated by the engine or all other countries' clocks. Never use a timed flag's automatic expiry as the sole proof that a human agreed, refused or authorized war.

Store remaining custom time or adjust the recorded deadline when a hold ends. Display who requested the hold, whether it was agreed under session rules and which deadlines are affected. A facilitator schedules; a facilitator does not sign foreign terms. A default unanswered deadline closes that revision as unanswered, informs the issuer once, and leaves a new **actor choice** to renew, revise, withdraw or explicitly escalate. No deadline callback launches a war merely because a human target or issuer stayed silent.

Do not block every other response behind one paused channel. A frozen aid request does not prevent a Turkish diplomatic response or a Greek officer decision; an acute hostage to a missing third signature means that particular joint package is incomplete, not that all diplomacy must stop.

## State and milestone matrix

Focus markers are **once-only campaign history**. Current policy and crisis results live in **instance-specific records**. Focus completion never substitutes for the records in the second column.

| Marker / proposed current fact | Required current evidence | Actor / payload owner | Badge meaning and limits |
|---|---|---|---|
| `war_guarantors` | First relevant substantive GRE/TUR/ENG decision in a live case | Actor publishes its own choice; CYP coordinator records once | Some guarantor response happened; not all three replies, an ultimatum acceptance or a war |
| `war_conference` | CYP/actual convenor formally submits the conference initiative | Actual convenor owns invitation | A conference was sought. Separate flags record invitations accepted, conference opened and terms signed |
| `war_defy` | A real, currently valid ultimatum exists and CYP actually rejects that revision | CYP response owner | An ultimatum was rejected at least once; does not forbid earlier/later talks |
| `war_putsch` | An actual attempted coup is resolved and classified success/failure, with recorded sponsor/actors | Coup result resolver or actual coup observer | Coup episode occurred/resolved; not CYP ordering its own fall. Success and failure have distinct current outcomes |
| `war_restore` | Real constitutional restoration/succession completed | Restoration resolver | Restoration happened; a later new coup is still possible under its own evidence |
| `war_prepare_intervention` | CYP performs its chosen defensive preparation, while foreign intent remains separate | CYP preparedness owner | Defence prepared; does not order Ankara to intervene |
| `war_july_ceasefire` / neutral label “Ceasefire Appeal” | Real first-hostilities phase or explicitly selected abstract phase; actual appeal/response recorded | Relevant actor/phase resolver | Appeal milestone; separate necessary replies and tested adapter establish an effective ceasefire |
| `war_geneva` / neutral label “Settlement Talks” | A real round of talks is opened/entered by its necessary participants | Conference coordinator records actual participants | Talks occurred, not that every term was accepted or that later remobilisation is impossible |
| `war_remobilise` | Actual sovereign remobilisation policy/implementation after the relevant context | Country choosing remobilisation | Historical remobilisation marker, not authorization of a foreign attack |
| `war_august` / neutral label “Renewed Hostilities Decision” | Prior actual/abstract phase plus unresolved or failed negotiations and a new actor decision | Sovereign actor / phase coordinator | Later decision occurred; not a calendar-triggered second offensive |
| `war_military_settlement` | Actual renewed combat / resulting military outcome in the selected phase model | Combat/outcome resolver | A military phase/result, not eternal hostility or a free future authorization |
| `war_monitored_settlement` | Required consent plus verified implementation of a specific package | Sole agreement resolver | A settlement occurred. A new later breach/crisis has fresh records and counterplay |

An existing badge remains complete in crisis #2, #3 and beyond. None is reset. New records identify which action belongs to which episode and whether the current situation differs. Do not use a once-completed settlement focus to make all later ceasefires permanent, to presume a later negotiation succeeded, or to suppress new opposition forever.

### Proposed graph corrections, for later work only

1. Remove permanent political-stance exclusions between **`war_conference` / `war_defy`**. Asking for talks can precede rejection of a specific later ultimatum, and rejection can precede renewed talks. The stance belongs to the current packet/revision; each focus records a historical action once.
2. Remove permanent exclusions between **`war_geneva` / `war_remobilise`**. Negotiation followed by failure and remobilisation is a normal causal sequence, not a forbidden ideological reversal. Later negotiation remains possible after renewed military preparation.
3. Decouple an observed **`war_putsch`** outcome from a permanent **`war_officer_agreement` / `war_plot`** exclusion and from CYP's optional plotting path. A Greek-sponsored coup attempt must remain visible after CYP sought an officer agreement. Make coup preparation an actor-owned path; make the coup result an independent, properly gated milestone. A defensive Makarios government should not need to select “organise my overthrow” to expose a foreign attempt.
4. Treat final settlement/combat badges as prior outcomes; do not let permanent terminal-focus exclusions disable future crisis rounds. Keep truly incompatible **durable implemented programmes** or one-time constitutional packages in separate explicit policy slots with replacement/repeal rules.
5. Keep independent event entry points for actual foreign actions. A missing/incompatible focus prerequisite or a legacy exclusion cannot make a real coup/war invisible. Do not assume `complete_national_focus` safely bypasses every prerequisite/exclusion until tested. For later implementation, make milestone topology compatible first and keep the event result authoritative even if the marker cannot yet be painted.

These are changes proposed for future graph design. This document does not alter `cyprus_crisis.py`, `build_design.py`, JSON or any runtime tree.

## Source-backed hooks and illustrative adapter sketches

### Reusable existing language / hooks

| Existing facility | Local evidence | Reuse / boundary |
|---|---|---|
| `country_event = { id = ... days = ... }` | `events/Greece.txt` near4235 | Route a real actor invitation; recipient event ID/content is new |
| Event delay in hours | `events/05_armenia.txt:12581` | Short crisis routing is supported; a delay is not consent |
| `complete_national_focus = ID` | `events/05_armenia.txt:10170` | Record a milestone with valid topology and once-only guard; reward/prerequisite behaviour needs engine testing |
| Block-form completion | `events/05_australia_events.txt:5354` | Existing `focus`, `use_side_message`, `originator_name`; no invented `reward = no` parameter |
| `on_war_relation_added` | `common/on_actions/mdcw_cold_war_on_actions.txt:43` | ROOT attacker, FROM defender; detects actual regular war, not only custom-tree choices |
| `on_coup_succeeded` | Same file near65 | ROOT changed government, FROM sponsor; actual engine coup observation. A manually changed government may require a separate explicit custom result callback |
| `on_daily` | `common/on_actions/00_on_actions.txt:86` | A future CYP-scoped coordinator can update custom queues/deadlines; no engine disconnect detection implied |
| Pending offer records / validation | `common/scripted_effects/mdcw_cold_war_effects.txt:3217–3225` | Native bilateral type/size/deadline fields, clearing, donor-capacity revalidation; reuse pattern, not unrelated assistance slots for crisis data |
| Tension / GUI refresh | Same file`:13`, `mdcw_cw_add_tension` | Adds/clamps Cold War tension and updates display; distinguish local communal/coup tracks |
| Exact subparty and coalition handling | `00_MD_politicsview_scripted_effects.txt:1979` | Real `change_ruling_party_effect`; a response ledger must not use it to force another player's politics |

### A. Future TUR event publishes its own response

Illustrative Clausewitz-shaped sketch. **The receiving event, flags and `record_external_reply` effect are NEW.** The actual Turkish event/decision owns its choice. CYP does not choose a numeric response on Ankara's behalf.

```text
# In the future TUR-owned option/decision, AFTER validating the live packet,
# human-seat policy and the actor's actual selected response:
CYP = {
    set_temp_variable = { COLDWAR_CYP_1970_rp_reply_actor = PREV.id }
    set_temp_variable = {
        COLDWAR_CYP_1970_rp_reply_request = PREV.COLDWAR_CYP_1970_rp_pending_request
    }
    set_temp_variable = { COLDWAR_CYP_1970_rp_reply_kind = 2 }
    COLDWAR_CYP_1970_rp_record_external_reply = yes # NEW, not defined yet
}
```

Here2 is a **new documented reply enum**, not an existing MD constant; for example it could mean a substantive diplomatic counterproposal. The new adapter must validate packet identity, topic, revision, expected actor and authorization provenance. It updates records and sends notifications; it must not contain a hidden fallback “Turkey declares war” action. A separate Turkish authorized operation owner executes war/payment/mission effects, then reports the result once.

The native Cold War system already relies on sender/PREV scoping, but the new wrapper's exact scope chain must be tested. A user-selected actor tag or a mutable “reply_actor=TUR” value is not sufficient evidence of Turkish authorization. The code entry point and actual actor option/hook supply that evidence; Cyprus must not call an actor's result as a shortcut to its desired history.

### B. Coordinator records the permanent badge once

Illustrative NEW CYP-scoped recorder; `current_substantive_replies` is rebuilt from the **current instance**. The real completion effect is existing; every variable/flag here is new.

```text
if = {
    limit = {
        check_variable = { COLDWAR_CYP_1970_rp_current_substantive_replies > 0 }
        NOT = { has_country_flag = COLDWAR_CYP_1970_rp_guarantors_ever_recorded }
    }
    set_country_flag = COLDWAR_CYP_1970_rp_guarantors_ever_recorded
    if = {
        limit = {
            NOT = { has_completed_focus = COLDWAR_CYP_1970_war_guarantors }
        }
        complete_national_focus = COLDWAR_CYP_1970_war_guarantors
    }
}
```

Set the once-only guard before completion so reward callbacks cannot recursively redispatch or reapply payloads. The focus reward for this milestone must be a no-payload record/tooltip; it must not charge cash, grant an idea, issue a request or resolve a war. The present `build_design.py` annotates `execution_mode = event_milestone`, but still emits proposed payload text for some reactive nodes. That annotation is a design contract, not an implemented reward suppressor. Later runtime work must move effects to the guarded outcome owner and make marker completion record-only explicitly.

This does not claim the completion call overrides incompatible prerequisites/exclusions. The future topology must make the record legal; if completion fails during testing, leave the actual reply/result intact, log the marker problem and fix topology. Never reverse a valid response or invent missing actions to satisfy a focus prerequisite. The persistent-ever flag and an already-completed badge must also be reconciled on save migration without replaying any payload.

### C. Actual manual Turkish war is an independent entry point

Use the verified `on_war_relation_added` hook to observe **ROOT=TUR, FROM=CYP**. The future observer creates/finds the correct current case, records an actual sovereign war and classifies its timing/context. It must work even when no custom tree/ultimatum flag was set.

```text
# Additional future on_war_relation_added observer; NEW callback only.
# Native hook: ROOT attacker, FROM defender.
if = {
    limit = {
        ROOT = { original_tag = TUR }
        FROM = { original_tag = CYP IMP_is_1970_scenario = yes }
    }
    CYP = {
        COLDWAR_CYP_1970_rp_observe_turkish_war = yes # NEW implementation
    }
}
```

The callback observes an **already existing war**. It must not declare it again, demand retroactive approval, fabricate a preceding coup, or rewrite an early/alternate war as the historical20July1974 operation. Record `actual_war_started`, observed participants/date and whether the historical causal context exists. A premature/otherwise divergent Turkish war is an alternate course. It is also a substantive relevant guarantor action for the first-response milestone, with its own result record.

Use neutral display labels such as **First Intervention**, **Ceasefire Appeal**, **Settlement Talks** and **Renewed Hostilities** when dates diverge; stable existing IDs may remain. Do not generate a historical coup simply to make the actor's already-declared war fit a timeline. Other actual wars/participants also remain engine facts even if their custom political authorization record is absent; classify and display them rather than silently deny they occurred.

Native Imperia `mdcw_cw_on_war_relation` already handles its own interbloc shock and assistance suspension. The new observer must not repeat that entire effect and double-charge global tension. `on_coup_succeeded` can similarly feed an actual-coup result record; it is not a license for CYP to claim an unperformed Greek action. Deduplicate custom resolution versus engine observation with a shared action/result ID.

## One payload owner per action/result

The response recorder owns records; the specific action resolver owns side effects. A treaty/payment/operation has a stable ID and an outcome-applied ledger. One possible flow:

1. Actor selects and authorizes a validated choice.
2. Actor's operation owner checks current funds/readiness/terms and applies the action **once**, or records pending/failed without pretending success.
3. Outcome recorder stores implemented/failed status and the true participants.
4. Milestone coordinator records applicable once-only focus markers.
5. Notification handlers display the result, with no gameplay payload.

If an ordinary engine war already applied the action, the observer is record-only; it does not become another declaration owner. If a custom operation resolves a coup, the callback is not another coup. If `complete_national_focus` triggers a reward path, that reward path must see the result already applied and remain record-only. No invented “reward=no” completion parameter is assumed. All retries, save/reload, reissued popups, hotjoin and repeated hooks must be idempotent.

The actual military constraints recorded in WAR_MECHANICS.md remain: the existing two-province map, deferred OOBs and unsafe generic CPD July-ceasefire semantics. Recording “ceasefire appeal” or a historical badge is not an engine stop-combat adapter. Keep proposed agreements, actual hostilities and verified military outcomes distinct.

## Visible counterplay

Every crisis panel should show what each participant can still do, without exposing imagined secret authorizations as facts:

- CYP: maintain talks, protect civilians, secure arms/command, request withdrawal, prepare defence, propose guarantees, reply to actual demands and restore constitutional authority if appropriate.
- GRE: retain/reassign/withdraw officers, refuse sponsorship, restrain a plot, offer aid, or explicitly authorize a hostile operation with visible consequences/counterplay.
- TUR: propose consultations, mediate, formulate an actual ultimatum, choose restraint, prepare/choose its own operation, accept/reject terms and decide on renewed hostilities.
- ENG: offer/refuse mediation or joint action, define base/humanitarian policy and respond without silently being added to a war.
- TC counterpart: accept/reject/revise security and constitutional terms through its own mandate; civilian access and property safeguards remain substantive.

No single missing reply should disable all these choices. Display “unanswered” as uncertainty, not as the human government's secret hostility. Preserve previous political choices as history while allowing a legitimate later change of stance.

## Example MP sequences

### 1. Dedicated historical CYP AI, democratic/restraint-minded Greece

Makarios AI follows the historical independent-government policy and requests civilian command/officer withdrawal. Human GRE accepts and actually implements reassignment. The withdrawal result reduces command capture; no sponsored coup is created. If that response belongs to a live relevant guarantor crisis, it can record `war_guarantors`; if this is ordinary earlier diplomacy, it remains that diplomacy and does not manufacture a crisis merely to award a badge. TUR/ENG remain free to answer separately. CYP AI does not choose an alternate ideology or sabotage the requested success to force1974.

### 2. Greek-backed putsch is attempted but fails

GRE explicitly authorizes a prepared attempt. Makarios AI chooses constitutional resistance. The actual resolver finds the coup defeated. The coup milestone records a failed attempt independently of CYP's earlier officer-agreement choice. No Sampson government, automatic Turkish invasion or automaticNCY appears. TUR may demand inspections or remain diplomatic; those are Turkish choices. Countermeasures and civilian consequences follow the actual attempt.

### 3. Coup succeeds, Turkey answers first, Britain is silent

An actual successful coup installs the relevant regime and opens a guarantor case. Human TUR issues a concrete ultimatum. That first substantive response permanently records **The Guarantors Respond**. Current UI reads1/3; GRE andENG channels remain open. Britain merely received the invitation and contributes no response yet. The actual CYP regime answers the ultimatum according to its policy/controller. Expiry does not launch an attack; TUR must explicitly choose its next action. No joint British intervention is presumed.

### 4. Coup succeeds but Turkey chooses no intervention

TUR explicitly decides continued diplomacy/no military intervention. This is a substantive response, not a landing. The guarantor badge may record it, but no first-intervention or July-ceasefire result is created. The actual Cypriot government follows its historical policy for that living regime under the altered external situation. Political restoration, mediation or continued crisis can follow; the calendar cannot supply a Turkish war that its player refused.

### 5. Talks, then rejection, then renewed talks

CYP seeks a conference. Participants attend, but an actual later ultimatum contains unacceptable terms. CYP rejects that revision while keeping talks open; both historical-action markers can be recorded. Negotiations later fail, a sovereign actor remobilizes, then a revised package is discussed. None of this is blocked by permanent conference/defiance or talks/remobilisation exclusions. Actual renewed hostilities require the relevant actor's choice and readiness. Necessary agreement signatures still cannot be substituted by a focus badge.

### 6. Reserved Turkey disconnects during an ultimatum window

TUR is a reserved human seat. The facilitator pauses the game or applies an agreed custom RP hold. Temporary AI does not select war, acceptance or withdrawal. A neutral hold is procedural and earns no substantive response. When the player returns/hotjoins, the current packet and remaining agreed deadline are revalidated. If the request expired unanswered, the issuer sees that fact and may revise/reissue; no historic response is retroactively assigned. A reserved human CYP receives the same protection and is not silently converted to deterministic historical AI.

### 7. Ordinary manual TUR→CYP war declaration

Human TUR declares through regular game controls without the future custom tree. `on_war_relation_added` observes it. The coordinator records the actual action, creates/classifies the case and updates the guarantor milestone if applicable. An early war is labelled alternate chronology, with no invented coup or forged ultimatum. Military outcomes remain real/selected-model results; unrelated assumptions about1983 recognition or complete territorial transfer are not injected.

### 8. New crisis after an earlier settlement

The guarantor and settlement focus badges remain complete from crisis #1. A new breach in crisis #2 opens new messages, replies, authorization and outcome records. UI separately shows historical badges and current0/3 or1/3. An old `has_completed_focus` cannot make the new case automatically answered, peaceful, hostile or settled. Replies to crisis #1 are rejected as stale for #2, and the new result never replays old costs/rewards.

## Future integration boundaries

Later Greek and Turkish content needs only documented entry points: publish own policy/response, authorize own action, report actual result, observe regular engine actions and query current packet/instance. Its event IDs need not match CYP's internal tree IDs. Keep the interface stable even while foreign trees are added later.

Quarantine incompatible modern/random Cyprus content in1970. `common/on_actions/CYP_on_actions.txt` currently fires EU integration `cyprus.3` and a Green Line incident `cyprus.4` with later division/NCY conditions. Those events and modern gas/EU decisions must not silently create guarantor authorization, justify war or supply a human's missing reply. An ambient incident can be information for a separate new choice; it is not itself a foreign choice.

This concept needs future adapters, event definitions, deterministic CYP policy mappings, session-seat configuration, UI and engine/MP testing. It does not claim an existing disconnect detector, a host-control API, auto-skipping of focus prerequisites, a safe ceasefire implementation or completed foreign trees. No code outside this document has been changed.
