# COLDWAR UAE — British subject / independence path mechanics

2026-10-19. Concept audit only. No generator or loaded game file was edited. This report verifies existing APIs and proposes an explicit recipient-controlled diplomatic flow.

Final emitted concept review: **107 focuses / 40 decisions; passed the bounded British-path review.** The revised generator, JSON and both preview data models are consistent. All 97 unrelated focus records match the preservation baseline. Agreement handlers, mirrored spirits and date/nonce consumers remain explicitly proposed integration, not an installed or engine-tested system.

## Exact native starting relation and keys

The January 1970 setup executes:

```text
ENG = {
    set_autonomy = { target = UAE autonomy_state = autonomy_puppet_state }
}
```

Source: CW `common/scripted_effects/IMP_1970_world_politics_effects.txt:1226–1232`.

`autonomy_puppet_state` is an installed MD autonomy ID, not a guessed vanilla key. Its definition at CW `common/autonomous_states/MD_default_autonomies.txt:87–124` includes:

- Puppet status and blocked independent war declarations.
- No ability to decline the overlord's call to war.
- 50% civilian and military factory capacity to the overlord.
- Existing manpower, preferential-trade and research-sharing consequences.
- Ability for the overlord to build for the subject.

These are real existing trade-offs of the loyal option. Do not add a duplicate “50% factories lost” spirit on top.

The actual subject and sovereignty tests are:

| Meaning | Native country trigger | Evidence |
|---|---|---|
| UAE currently belongs to the British overlord | `is_subject_of = ENG` | Installed game `documentation/triggers_documentation.md:6285–6293` |
| UAE is actually independent of every overlord | `is_subject = no` | Same document:6276–6284; many native MD focus uses |
| ENG exists as the intended recipient | `country_exists = ENG` or `ENG = { exists = yes }` | Existing country scripts and native trigger |
| UAE still exists at reply time | `country_exists = UAE` | Existing project diplomatic guards |

**Not being a British subject is not proof of independence.** A UAE transferred to another overlord satisfies `NOT = { is_subject_of = ENG }` while still being a subject. The withdrawal/formation route must use `is_subject = no`.

## Narrow native release leaf and correct scope

Recommended native contract-execution effect, used immediately on acceptance or once at an already accepted future maturity:

```text
# Inside UK scope, where ROOT is ENG:
end_puppet = UAE
```

Or explicitly scoped from a UAE helper:

```text
ENG = { end_puppet = UAE }
```

Both forms require a live recheck that UAE is still a subject of ENG. The effect acts on the **current country's puppet**; it must run in the overlord's scope.

Proof:

- Installed game `documentation/effects_documentation.md:3662–3670`: `end_puppet` stops the specified country being a puppet of the current country.
- Main MD `events/Russia.txt:6734,6801`: `SOV = { end_puppet = ROOT }`.
- Main MD `events/05_armenia.txt:9405`: `SOV = { end_puppet = SOO }`.
- Existing Cold War `events/COLDWAR_DDR_1970_events.txt:1441–1463`: an accepting overlord option uses `end_puppet = DDR`.
- Existing Cold War `events/COLDWAR_SOV_1970_events.txt:539–547`: `end_puppet = FROM`.

Native MD also uses `set_autonomy = { target = ... autonomy_state = autonomy_free }`, for example CW `common/scripted_effects/99_SOV_scripted_effects.txt:2074–2079`. The narrower `end_puppet` is preferable here. Installed `set_autonomy` documentation at 6586–6604 lists default war-ending behavior; a simple independence request does not justify extra war/faction outcomes.

Do not use an invented `autonomy_independent`, `free_country`, `release_from_subject` or `set_overlord = none` key.

## Required player-visible flow

The requested structure is:

1. A meaningful mutually exclusive choice between continued British protection and requesting independence.
2. The independence-request focus sends an actual event/offer to ENG.
3. The British player accepts or refuses.
4. Valid acceptance either executes immediate release or binds a stated future independence date. A future-date agreement leaves the UAE a British subject until that date, then executes release once without asking Britain again.
5. Both countries receive linked national spirits displaying the accepted terms and date. The existing “British withdrawal” / formation continuation becomes available **after actual independence**, with the other founder/constitutional conditions still intact.

The request focus is an action to send a request, not independence itself. Its completion must not set a flag whose mere presence bypasses the actual subject check.

For immediate acceptance, verify `UAE = { is_subject = no }` after executing release before marking execution complete. For future-date acceptance, mark the agreement binding but unexecuted, keep actual subject status, and let the date observer execute the same release helper once at maturity. Acceptance and execution are distinct states. The main formation focus must not contain a second release effect.

A suitable formation condition remains conceptually:

```text
is_subject = no
has_country_flag = COLDWAR_UAE_founders_consented
# Plus the actual selected institutional prerequisites.
```

If the concept requires this specific British agreement rather than independence achieved by other normal game mechanics, add the accepted-agreement flag **as well as** `is_subject = no`. If the intention is to accept any genuinely independent UAE, do not require a redundant British flag. Pick one policy explicitly in the design; never substitute the flag for actual freedom.

The previous catalogue's withdrawal decision and “The Union Proclaimed ends the British relation” reward must be revised together. There must be one authoritative release helper: invoked by valid immediate acceptance or by the due-date observer for a previously accepted binding contract.

## Proposed request lifecycle

All new `COLDWAR_UAE_...` request flags, events and handlers below are design work; they do not exist merely because their names appear here.

### Send

Check UAE exists and is the requesting country, ENG exists, UAE is currently `is_subject_of = ENG`, no UAE–ENG war or capitulation invalidates negotiation, no current request is pending, and the request is not already resolved.

Record a current request instance and pending status before dispatching the UK event. The event identifies UAE as the requester and lists the real terms. No foreign transfer, bases, troops or guarantee is assumed.

A finite pending window and retry cooldown should be stated. A reasonable proposed policy is a 60-day response window and a 180-day retry cooldown after refusal/expiry; these are gameplay choices, not native mandates.

### Accept in UK scope

Recheck the current request instance, pending state, both countries' existence, actual British subject relation and relevant peace/capitulation conditions.

Then consume that request once, freeze its accepted terms and either execute immediate release or record the agreed future due date. Clear negotiation-pending state, install both role-specific agreement spirits, notify the UAE player and recompute affected programme modifiers. Future acceptance must not execute `end_puppet` early. The execution helper later confirms actual independence and marks release executed. Do not rerun the initial world-alignment setup.

Acceptance is not acceptance of a base treaty, troop deployment, faction membership, oil equity or a treasury payment. Such terms need explicit separate agreement.

If the actual relation changed while the popup was open, the acceptance must become stale/cancelled and perform no release from another overlord.

### Refuse, expire or cancel

Refusal keeps the current native British subject relation, clears pending status, records the cooldown/result and sends a UAE reply. It grants no cash, automatic war goal, civil war or independence.

Expiry or cancellation must also clear pending state. A human's silence is not consent.

Cancel stale requests if ENG or UAE disappears, the actual overlord changes, UAE becomes independent by another route, or the offer's defined peace/subject conditions no longer hold.

Because focus completion is normally one-time, a refusal must leave a named retry decision unlocked from the completed request focus. Otherwise the path could become permanently inert after one British refusal.

A serial/request-identity check prevents an old popup from accepting a different later request after a retry. The concept should identify the intended current request; implementation must test duplicate clicks and stale replies.

## Loyal protectorate path: meaningful supported rewards

The loyal choice should remain playable economically and politically while retaining the native costs of puppet status. It should not be a hidden automatic independence route.

Use `is_subject_of = ENG` and any genuine accepted-programme flag as active conditions for ongoing British cooperation. On release or a change of overlord, these programmes deactivate; earned progress can remain for a later negotiated return. Permanent funded buildings or productivity-point grants do not disappear.

Useful supported packages, proposed for calibration:

| Programme | Concrete native benefit | Credible cost / condition |
|---|---|---|
| British technical mission | One paid +15 or +20 productivity-point grant; possibly +3–5% research for 730 days | UAE pays a frozen numerical mission fee; +5% education spending while active; ENG accepts providing experts |
| Adviser compact | +15 Army experience; −10% training time for 730 days | +10% personnel spending for the same duration; numerical UAE fee; ENG consent; no free British divisions |
| Commercial administration | +8–10% offices productivity or −5% bureaucracy costs | Administrative fee and an explicit continuing supervision/education burden; accepted technical contract where British participation is promised |
| Protectorate works | Queue a named office or infrastructure project in an owned/controlled UAE state | Full native construction/labor/energy remains; identify payer; UK contributes only after choosing acceptance |
| Rulers' continuity settlement | Modest stability/PP programme linked to ongoing British protection | Actual subject status and local ruler agreement; preserve existing war/trade/factory constraints |

The exact keys already traced in `MECHANICS_AUDIT.md` include `research_speed_factor`, `education_cost_multiplier_modifier`, `offices_productivity`, `bureaucracy_cost_multiplier_modifier`, `training_time_factor`, `army_personnel_cost_multiplier_modifier`, `army_experience`, the flat productivity helpers and native construction.

These are suggestions, not a requirement to add five more branches. The point is to offer a real economic/security programme with a price and the native dependence costs.

Any bilateral option must show costs and benefits numerically in the actual event options. The description should explain the political choice briefly, following the user's native-MD preference. Do not bury the invoice in a long diplomatic story.

Do not force ENG to pay treasury, supply equipment, provide an army, accept bases or guarantee UAE merely because the UAE completes a focus. An existing overlord's ability to build is not proof it has funded a particular project.

## Identity, succession and save behavior

### Tags and cosmetic names

- UK is tag `ENG` in the 1970 setup. Its Harold Wilson government comes from `history/countries/ENG - United Kingdom.txt:4–18` and `IMP_1970_world_politics_effects.txt:379–383`.
- UAE remains tag `UAE`; `UAE_TRUCIAL_1970` is a cosmetic identity, not a new country.
- Government, leader and displayed-country-name changes do not by themselves change the actual subject trigger.
- A British civil-war successor with a different current tag must not be treated as ENG merely because it has British history or controls London. Either cancel the ENG contract when the actual relation changes or design a separate explicit successor negotiation. Do not guess a successor from state ownership.

### Startup must not re-puppet a released UAE

CW `common/scripted_effects/IMP_1970_world_politics_effects.txt:1348–1356` wraps the global alignment setup in `NOT = { has_global_flag = IMP_1970_global_alignment_initialized }` and sets that flag after setup. Preserve this existing one-time guard.

Do not call `IMP_1970_setup_global_alignment_internal` on acceptance, party refresh or save load. It includes the initial ENG→UAE subject grant and much unrelated world setup. A normal reload should retain the global initialization flag.

Keep the independence request/result flags separate from the low-oil starting flag, paid extraction flags, frozen GDP profile and permanent national reforms. Release is not a reason to reset any of those.

### Loyal-route leadership beyond 1971

CW `common/characters/mdcw_gulf_1970.txt:58–69` gives the starting Council character an expiry of 1971.12.2. A continuing protectorate needs a deliberate representative/council continuity outcome rather than relying on that expiry to define the alternate constitution.

CW `common/scripted_effects/mdcw_historical_native_pools.txt:12628–12711` cycles Council → Rashid → Zayed through `Monarchist_leader`. Calling that helper blindly does not guarantee the representative promised by the loyal focus. Preserve the existing party system and select any new office explicitly.

The native expiry date is not proof that the engine will release the country or form a federation. Do not use it as the independence mechanism.

## Bounded review checklist for the forthcoming concept

- Request focus and loyal focus mutually exclude each other symmetrically.
- Independence request is available only under the actual British subject relationship.
- The authoritative release helper contains `end_puppet = UAE` in ENG scope and is invoked only by valid immediate acceptance or a due, previously accepted binding contract.
- Withdrawal/formation requires `is_subject = no` plus its real remaining conditions.
- A successful flag alone cannot bypass subject status; transfer to another master does not unlock formation.
- Refusal/expiry is retryable without repeating one-off focus rewards.
- Pending/accepted/cancelled results are mutually consistent and stale responses cannot release an unrelated later subject relationship.
- Loyal bonuses require actual British subject status and any promised British acceptance.
- All paid support offers are numerically explicit and recipient-controlled.
- No automatic UK troops, treasury or equipment; no repeated release at federation formation.
- Starting Council continuity is addressed if long protectorate play is supported.
- Existing oil grants, baseline, GDP calibration, programme progress and global alignment initialization survive the transition and save/load.
- Source consistency and a browser preview do not replace a fresh 1970 game and two-player acceptance/refusal/save test.

Final emitted review can be appended once the revised generator and JSON are available. No gameplay implementation or HOI4 runtime verification has been performed by this auditor.

## Revision: bilateral national spirits and contractual independence date

This section incorporates the newer requirement and supersedes the earlier immediate-only release description. Britain may accept immediate independence or bind a future date. The accepted future contract is already consent: maturity does not request another British veto.

### Native bilateral agreement presentation patterns

There is direct main-MD precedent for agreement spirits on both sides:

- `events/05_netherlands.txt:6266`: accepting SUR adds `HOL_suriname_trade_agreement_idea1`; its Dutch reply at 6291 adds the same idea to HOL.
- Its definition at `common/ideas/05_netherlands.txt:2795–2811` includes existence cleanup and targeted trade effects.
- Role-specific precedent: `events/Belarus.txt:884` adds `BLR_mzkt_contract` to the buyer; the reply at 930 adds `BLR_mzkt_contract_blr` to Belarus. Definitions at `common/ideas/Belarusian.txt:1594–1627,1660–1674` differ by role.

These examples prove bilateral/role-specific idea grants are native patterns; their equipment bonuses and balance are not UAE recommendations.

Proposed UAE–UK presentation should use **two role-specific spirit definitions** for each active agreement kind, for example:

- `COLDWAR_UAE_british_protection_terms_uae` and `..._eng`.
- `COLDWAR_UAE_british_withdrawal_terms_uae` and `..._eng`.

They must share one frozen contract identity and the same accepted term/date; the numerical modifiers may differ by role. A shared agreement name alone does not synchronize anything.

Native `add_dynamic_modifier` is supported in country scope, including a variable duration (`documentation/effects_documentation.md:1153–1173`). Existing Cold War programme modifiers use `enable` conditions. Alternatively, native `add_ideas` can install role-specific ideas with explicit removal. `add_timed_idea` accepts positive integer or variable year/month/day durations (same documentation:2244–2268). The chosen architecture must keep the agreement's state independently of whether a visual spirit happens to expire.

### Display contract terms on both countries

Each spirit should state:

- Counterparty and contract identifier/version.
- Agreement kind: continued protection, immediate independence, or binding withdrawal timetable.
- Status: proposed / accepted and awaiting date / executed / lapsed or cancelled.
- The precise independence date for withdrawal, or the next terms-review date for continued protection.
- The country's own concrete costs, responsibilities and benefits.
- Whether support benefits end at independence or continue under a separate accepted post-independence agreement.

A loyal spirit should say **no independence date has been agreed** if that is the actual bargain; a review date is not a disguised automatic release date.

Descriptions should explain the political bargain briefly. Named numeric effects remain native numeric modifier/effect tooltips. Reuse the user's English-only localization rule.

### Verified date variable and display APIs

Installed `documentation/dynamic_variables_documentation.md:975–978` documents `global.date` as a date value comparable to other date values and renderable by `GetDateString`, `GetDateStringShortMonth`, `GetDateStringNoHour` and `GetDateStringNoHourLong`.

Direct native MD provider/consumer pair:

- CW `common/scripted_effects/99_investment_scripted_effects.txt:699–721` copies `global.date` into `soi_expiry_date`, adds **2.88 for 120 days** or **8.64 for 360 days**, stores it in an expiry array, and sets a timed flag for the same duration.
- CW `localisation/english/MD_investments_l_english.yml:226–231` displays the stored value with `[?soi_slot_expiry^1.GetDateStringNoHourLong]`.

This supports copying a current/accepted date into a persistent variable and rendering it, rather than showing the ever-changing current date as if it were the contractual date. The existing MD conversion is 0.024 date units per day; that unit relationship is source evidence from the investment provider, not an invented new API.

For a relative **360-day** agreement, a concept outline can use:

```text
set_variable = { COLDWAR_UAE_british_due_date = global.date }
add_to_variable = { COLDWAR_UAE_british_due_date = 8.64 }
```

and display:

```text
[?COLDWAR_UAE_british_due_date.GetDateStringNoHourLong]
```

A documented date-value comparison can check current `global.date` against that stored due value with the ordinary `check_variable` comparison form. Exact daily boundary alignment should still be verified in the engine.

For the specified **1 December 1971** option, the simplest robust concept uses a stored fixed-date choice flag and the native calendar trigger:

```text
NOT = { date < 1971.12.1 }
```

Its English spirit text can explicitly show “1 December 1971.” This avoids guessing a serialized numeric date or inventing an unsupported `set_date_variable` effect. A fixed calendar option need not use an arbitrary numeric date conversion merely to display its known date.

If a generic date provider is later added for arbitrary selected calendar dates, trace it before claiming support. A literal string `"1971.12.1"` should not be assigned to an ordinary numeric variable and assumed to become an engine date value without evidence.

The historical-date option should only be offered as a future timetable before that date. After the date has passed, valid acceptance should use immediate execution or a newly agreed future date, not store an already elapsed schedule and call it a future promise.

### Authoritative state and shared contract identity

Keep a dedicated record with at least:

- Frozen contract ID / serial.
- UAE and ENG participant identities.
- Accepted type and terms version.
- Accepted date, and either fixed-date choice or stored due-date value.
- Binding-accepted flag.
- Release-executed flag.
- Current negotiation instance and resolved/cancelled state.
- Role-specific programme values and any actual payment-consumed flag.

Copy the same ID and terms to both participants. Country dynamic modifiers can enable only when their counterpart exists, both sides hold the same live contract ID/version and the appropriate active relationship still holds. Variables and flags must be real provider/consumer records; a spirit's description is not a contract state machine.

An old popup or delayed event must not activate a new contract after the agreement was superseded. Repeating a sync step must only ensure current spirits are present; it must not add the same payment, productivity, XP or resource reward again.

### Daily maturity and save/reload behavior

Native daily observers already exist:

- `common/on_actions/99_ENG_on_actions.txt:2–13` uses `on_daily_ENG`.
- `common/on_actions/COLDWAR_CYP_1970_on_actions.txt:16–28` uses a scoped daily country check and a country helper.
- `common/on_actions/COLDWAR_IRQ_gulf_on_actions.txt:3–21` pairs startup synchronization with a daily handler.

A proposed UAE contract observer should run from a correctly scoped daily callback and on startup/load reconciliation. It must check:

1. A binding accepted withdrawal contract exists.
2. Its current IDs/versions match the participant records.
3. It is not already executed.
4. The agreed date is due.
5. ENG and UAE still exist, and UAE is actually a subject of ENG.

Then invoke the one authoritative ENG-scoped release helper, confirm UAE is independent, mark that contract executed, and remove/replace the withdrawal spirits on **both** countries. Recompute relevant programme modifiers and give the agreed notifications. There is no new acceptance popup at maturity.

A daily handler can execute at the first tick on/after the date. A startup check catches a loaded save already past due. Both paths use the same executed guard so a reload or two observers cannot release twice or replay rewards.

Do not rely solely on a delayed `country_event` or an expiring timed idea. A delayed event can be a reminder/wakeup, but its effects must recheck the current contract identity. Losing a visible spirit or timer must not erase an otherwise binding accepted independence promise.

Do not refresh a timed idea with its original full duration on every load: that would push an agreed date into the future. The persisted due date remains authoritative.

### No second veto and materially changed world state

Once ENG accepts a future release, later British government, ruling-party, leader, opinion or focus changes do not create a new veto. An expired “offer pending” flag is irrelevant after the agreement has become binding.

At maturity:

- If UAE is still a British subject, execute release under the accepted terms.
- If UAE is already independent, mark the contract fulfilled and clean both pending spirits without a second `end_puppet` or repeated grants.
- If UAE is now a subject of a different overlord, do not release it from that other power and do not pretend it is independent. Mark the original bilateral obligation unable to execute under the changed relationship and report that state explicitly.
- If a participant no longer exists, handle the contract as interrupted/unfulfillable; do not guess that whoever owns London inherits the contract automatically.
- If the date is not yet due, preserve subject status and the matching agreed-date spirits.

A later war or change of opinion must not silently become a second veto unless a specific termination clause was part of the accepted contract. Such a clause must be visible to both players at acceptance. Do not invent broad cancellation powers in a housekeeping helper.

### Different numerical terms for the two countries

The spirits can carry asymmetric effects, using existing keys. For example:

- UAE: advisory training/research advantages and explicit education, administration or personnel costs while protection continues.
- ENG: a small explicit administrative/personnel commitment or a political effect representing an orderly scheduled withdrawal; no automatic resource grant.
- If the bargain transfers money, debit the named payer and credit the named recipient by the exact same frozen amount, once, only on the agreed payment trigger.
- If the bargain promises equipment or troops, it needs a separate exact consented delivery contract. A British flag or national spirit does not create the contribution.

Global percentage spending modifiers affect the country's whole spending category. A +1% UK personnel-cost modifier may be substantial; do not copy a UAE percentage onto the UK and assume equal absolute cost. The two roles need independent numerical calibration.

A status-only withdrawal commitment spirit is mechanically legitimate if its purpose is to expose the binding date and terms; do not claim an economic bonus it does not have. Meaningful support programmes can supply numeric effects separately.

### Updated final concept audit requirements

The forthcoming emitted concept should prove:

- Both role-specific spirits are granted on the same accepted contract identity.
- Both display the agreed date or clearly state that protection has only a review date.
- Future acceptance leaves the actual subject relation intact until due.
- Immediate acceptance and future maturity call the same guarded one-time release helper.
- Maturity has no second UK approval gate.
- The formation/withdrawal focus still checks actual `is_subject = no`.
- Refused negotiations, accepted binding contracts and executed releases are distinct states.
- Save/reload does not extend the agreed date or replay payments/rewards.
- Existing low-oil normalization, four paid oil grants and frozen GDP/initial world setup remain untouched.

This remains a source/design audit. Date formatting examples are native and source-backed; actual date-boundary execution, both spirit tooltips and save/reload behavior need an HOI4 test after implementation is approved.

## Final emitted British-path review

The 107-focus / 40-decision generator and emitted JSON were inspected after the co-financing guard and domestic-liaison ownership clarification. No unresolved concept mechanics blocker remains in this bounded revision.

Verified points:

- Nine new British focuses form a subject-status branch with a symmetric initial protection/independence exclusion.
- Renewed protection programmes require both `is_subject_of = ENG` and accepted protection; the root's domestic liaison explicitly depends only on the existing British relationship.
- The independent handover/friendship continuation uses actual `is_subject = no`. Friendship contributions additionally require accepted friendship.
- The main renamed **British Withdrawal** focus requires actual freedom plus founder consent and has no `end_puppet` effect. Formation is no longer the release trigger.
- Treaty Dependence is explicitly subject-status-bound and deactivates on actual British release, including before federal formation.
- Request focuses dispatch new consent-aware offers without releasing the country or moving UK money.
- Five bilateral presentation variants provide distinct UK/UAE spirit IDs and matching status/date/terms: initial protection, scheduled withdrawal, renewed protection review, fulfilled release notice and independent friendship.
- Immediate, fixed 1 December 1971 and native 360-day date options remain distinct. Future acceptance preserves subject status until due; the accepted deadline has no second UK vote.
- The one authoritative UK-scoped release outline checks the current/due accepted contract, actual British subject relation and active contract. Its proposed sync stops subject-only benefits and mirrors the fulfilled result. Already-free and materially changed-overlord cases are handled in the delivery contract.
- Refusal/timeout has a 180-day retry route; reopening talks after loyalty does not reset mutually exclusive focus progress. Amendments need both parties and cannot silently postpone the old binding date.
- The collective/interim leadership continuity contract explicitly covers continuing protection and the interval between independence and federation.
- UK co-financing now has a real proposed guarded wrapper: sufficient UK treasury, current request/nonce, UAE existence, actual British subjection, accepted protection, the relevant completed focus and absence of the paid grant flag. It debits UK 0.25bn and credits UAE 0.25bn once. Refusal/expiry does neither.
- The handover modifier has a stated 365-day contribution and does not renew on a government change; final implementation must supply its expiry consumer as specified by the generic programme architecture.
- Existing four paid oil projects, low-oil bootstrap, GDP calibration and other focus records are preserved.

Independent preservation check: all **97 unrelated focus records** equal `BRITISH_PRESERVATION_BASELINE.json` for its audited fields. The structural validator reports zero errors, 24 exclusion pairs, six passing remedy cases, the unchanged 4→47 oil programme and five bilateral treaty variants.

Final JSON SHA-256: `adfed639db46226ba8ade823af9474fb31bce4ffaea48c1a68c4d78cf9686f3d`.

Bounded final metadata refresh: the initial UAE-side bilateral spirit now reuses `COLDWAR_UAE_treaty_dependence`, avoiding a duplicate starting spirit. Nodes, effects and gates did not change. Both embedded preview models were checked again and match this final JSON.

| Preview | SHA-256 | Embedded model |
|---|---|---|
| `PREVIEW.html` | `de86df1149479819f67eaab7fd366c625d16599dc66b863d325f8799ed6448b1` | Exactly equals final JSON after removing embedded assets |
| Inline `uae-1970-focus-concept.html` | `ada21f137cc6c8e3b0d92743361fe217bf5fe6cdf57e089dca6d718be0fa1fcc` | Exactly equals final JSON after removing embedded assets |

This closes source/preview-data review only. The new `COLDWAR_UAE` dispatchers, current-contract/due trigger, mirrored idea providers, daily/load observer and expiry handling still require implementation after approval. The audit does not claim the game currently loads those helpers or that a multiplayer save has executed the contract.


