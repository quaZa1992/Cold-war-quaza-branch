# South Korea 1970 presentation repair: independent review

Review scope: read-only review of the current generated decisions/events and the KOR runtime generators. No game or generator source was changed during this review. Review criteria follow `mdcw-national-trees/references/runtime-presentation.md` and `mdcw-modifier-audit/references/modifier-effect-audit.md`.

## Confirmed presentation defects in the current source

1. **Decision availability leaks internal trigger IDs and raw flag names.** The installed [politics decisions](../../../common/decisions/COLDWAR_KOR_1970_politics.txt) expose `COLDWAR_KOR_political_scenario = yes`, direct `has_country_flag = COLDWAR_KOR_*` checks and negated flag checks in `available` (for example, lines 6–14 and 22–32). `reopen_constitutional_talks` directly requires `COLDWAR_KOR_military_reconsolidation` and `COLDWAR_KOR_opposition_constitutional_demand`, then exposes five `NOT` flags; this matches the screenshot’s raw `COLDWAR_KOR_military_reconsolidation` and `Not:COLDWAR_KOR_...` report. The KOR `Compiler.visible_trigger` in [runtime generator](../../../tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_runtime.py:117) wraps localized flags, but its only call in this generator is focus-gate emission at line 237; it does not process the decision module output. `hide_routing_checks` is applied to generated scripted triggers and dynamic-modifier enable blocks, not decision availability. Repair should keep the scenario/original-tag/initialization guards executable but hidden, while localizing substantive political requirements and accurate inverse descriptions. Do not blanket-hide the whole decision gate: e.g. governing-party, opposition-demand, martial-law, constitutional-order, retry cooldown, pending-ballot and legally represented party checks are real requirements.

2. **The weekly commitment tooltip is implementation-facing and awkward.** [The generator](../../../tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_runtime.py:187) emits `Active programme commitment: §R$…bn/week§!; replaces the previous commitment in this programme.` The emitted localization repeats this for all ongoing policies; the incident hotline example is in the loaded [English localisation](../../../localisation/english/COLDWAR_KOR_1970_l_english.yml:1214). Besides the screenshot’s “replaces previous commitment” phrasing, this describes replacement mechanics rather than the practical fiscal choice. Preserve the weekly number and explain it as a weekly public cost, with any replacement behavior phrased in player terms only if needed to understand selecting a new option.

3. **Agreement acceptance summary duplicates and fragments the numeric preview.** In [foreign event generation](../../../tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_runtime_foreign.py:432), an acceptance option contains an `effect_tooltip` with numeric deductions/modifier effects, then adds `custom_effect_tooltip = COLDWAR_KOR_foreign.<n>.accepted_tt` at line 449. The loaded [English loc](../../../localisation/english/COLDWAR_KOR_1970_l_english.yml:1541) has `COLDWAR_KOR_military_hotline_offer_tt` and many accepted summaries with repeated clauses such as “Korea pays …; Korea pays … weekly; … Terms last 1095 days.” The screenshot’s “On acceptance only; … Terms last1095days” is therefore backed by both a redundant sentence summary and the engine effect preview; it also fails the project preference to show concrete numeric agreement costs/rewards in native option effects. Review each summary against the actual option and avoid making a second charge or effect-preview copy while improving readability. Keep cancellation/no-change truthful.

## Checks to retain during the repair

- The decision predicates are not all flags. `COLDWAR_KOR_political_scenario` is a real scripted trigger (`common/scripted_triggers/COLDWAR_KOR_1970_politics.txt`); it includes original-tag/scenario/non-subject checks. Conceal technical routing only at presentation, without deleting the execution predicate.
- The foreign offer event IDs currently use distinct `.t`, `.d`, `.option_a`, `.accepted_tt` suffixes in generated event script (`COLDWAR_KOR_runtime_foreign.py`, event emitter near lines 428–450), which avoids the known `.d`/letter-option namespace collision. Recheck this property after regeneration.
- Foreign accepted summaries may describe counterpart payments and multiple counterpart signatures. Verify each against the matching `effect_tooltip` and acceptance helper. Do not state that an offer has been accepted merely because an offer is pending, or describe a refusal/expiry as an agreement.
- `effect_tooltip` is display-only; the actual charge is in the acceptance helper. Any edit to event previews must preserve this separation and must not duplicate execution.

## Follow-up status

Initial-source review is complete. I have not yet reviewed the parent’s updated staged or installed output; a post-edit check is still required for emitted decision predicates, inverse strings, event localization namespaces, accepted-option previews and the agreement wording.

## Revised prose JSON review

The second editorial pass removes the repeated boilerplate: a sentence-level scan of the current `COLDWAR_KOR_prose_politics.json` and `COLDWAR_KOR_prose_national.json` found no repeated long description sentences. The current prose is substantially more policy-specific. I found these remaining concrete source/prose mismatches in the politics JSON, which should be resolved or supported by additional implementation evidence before installation:

- `COLDWAR_KOR_industrial_rationalization_desc` says overextended lines “would close or merge,” but the emitted completion body in `common/scripted_effects/COLDWAR_KOR_1970_focus.txt` only assigns the interest-rate and civilian-factory productivity modifiers. It does not close or merge production lines.
- `COLDWAR_KOR_competitive_credit_desc` says banks would assess smaller exporters and broaden capital access. Its completion body only grants production-speed, interest-rate and productivity modifiers; no lending/allocation mechanism is called.
- `COLDWAR_KOR_export_recovery_desc` promises export finance and wage discipline; the current node payout is macro modifiers and a weekly public commitment, with no export-credit or wage-setting action.
- `COLDWAR_KOR_retire_political_networks_desc` explicitly describes the pre-1993 Hanahoe dismantling as an alternate outcome. Full completion helper review confirms the implementation sets `COLDWAR_KOR_officer_networks_retired`, charges $2bn, and applies a 180-day disruption idea; the focus has a modeled retirement outcome, so this is not a confirmed mismatch.
- `COLDWAR_KOR_olympic_republic_desc` refers to international hosting. I found no Olympic hosting/event implementation in the focus effect checked; the focus currently models a trade-opinion effect and administrative cost. Keep the text to international engagement unless a separate hosting outcome is confirmed.

The closure/merger language is a concrete operation the current source does not perform; the credit and wage language may be read as policy framing, but should not imply a transaction or wage-setting effect. These are presentation accuracy findings, not a request to redesign the mechanics. The parent is handling the decision presenter and foreign agreement terms. Their staged/install output still needs the promised post-edit recheck.


## Staged presentation recheck

The staged global presenter now wraps decision flag and variable predicates with a native positive/inverse tooltip pair; substantive availability checks remain executable. Representative `reopen_constitutional_talks` output preserves the party, military reconsolidation, opposition demand, constitutional-order and cooldown guards with localized wording. Foreign event acceptance calls are hidden inside `hidden_effect`, while `effect_tooltip` remains display-only and accepted summaries now use payer-aware weekly amounts, terms and durations. No evidence of doubled execution was found in the reviewed staged sample; this is a source-level check, not an engine tooltip test.

Two concrete defects remain in the staged output:

- `COLDWAR_KOR_political_scenario = yes` remains directly in every political decision's `available` block (e.g. `runtime_staged/common/decisions/COLDWAR_KOR_1970_politics.txt`, lines 7, 56, 120). The provider body hides its scenario checks, but this caller itself has not been hidden or replaced with `hidden_trigger`; this can still expose the internal scenario-routing helper.
- The generated inverse strings for two shared North Korean proposal flags are ungrammatical in `runtime_staged/localisation/english/COLDWAR_KOR_1970_l_english.yml`: lines 2243 and 2245 read “There is no a Northern…” and “There is no an inter-Korean…”. Use “No Northern … proposal is awaiting resolution” and “No inter-Korean … proposal is awaiting resolution.”

The staged foreign decision file still calls `COLDWAR_KOR_can_send_*` provider helpers directly. The screenshot evidence indicates native tooltips expand these provider bodies rather than exposing the helper name, so this is not a confirmed leak. The parent plans to inline those existing predicates at decision/category call sites to make presentation coverage explicit while preserving their guards. The installed/live game presentation was not available in this review.


## Final staged check

The next staged revision closes both previously reported issues: decision and category call sites now inline the KOR scenario/provider predicates while retaining their routing and independence requirements, and the two NKO inverse strings now state that no proposal is awaiting resolution. Final source review found decision trigger labels paired to positive and inverse predicates; the original guards for constitutional status, party legality/support, agreement signatures, pending offers and cooldowns remain present. Foreign accept helpers are under `hidden_effect`, while effect previews and separate structured summaries present the costs/weekly upkeep/duration. No duplicated executed payment was observed in the source-level review.

I found no remaining confirmed source-level blocker. Ten accepted foreign options with no material numerical rewards retain an empty `effect_tooltip` body containing only `KOR = {}` and `ROOT = {}`. It is likely inert; filter it for cleaner emitted script if desired. This review did not render a live HOI4 tooltip, so no engine-display claim is made.

### Installed closure — implementer

The remaining empty numerical previews were filtered from the final output. Installation and all three installed validators pass: structural checks, 22 bounded behavioral scenarios, and the independent presentation audit (64 decisions, 418 positive/inverse labels, 298 distinct focus descriptions). Canonical executable predicates and effects still match the pre-polish installed baseline. This closure adds source verification, not a live-engine rendering claim.
