IMPERIA COLD WAR

# Argentina 1970 runtime mechanics review

## Scope and evidence

Read-only audit of the approved design, generator sources, emitted COLDWAR_ARG runtime files, and the shared money-system integration. Evidence includes `tools/argentina_1970/approved_design.json`, `core.py`, `treaties.py`, `runtime_design.json`, and current emitted scripts under `common/`, `events/`, and `localisation/english/`. The emitted catalogue contains 299 focus nodes, 20 agreements, 16 events, 22 groups, and six starting spirits. Emitted counts match: 299 `focus` blocks, 20 treaty active triggers, and 16 country events. There is no top-level `starts` array in the approved/runtime JSON; the six starting spirits are the six `COLDWAR_ARG_start_*` ideas installed by the initializer.

This is a source audit. It does not prove that HOI4 parses every token, renders every tooltip as intended, evaluates every scope in a live campaign, or preserves behavior in a saved game. No game launch or native parser test was performed by this reviewer.

## Findings

| Finding | Evidence | Disposition |
|---|---|---|
| Recipient treaty spirits could have outlived Argentina in the first emitted version. | The current output resolves this: the daily global hook calls `COLDWAR_ARG_refresh_treaties` whenever the 1970 scenario is active, regardless of whether ARG exists (`common/on_actions/COLDWAR_ARG_1970_on_actions.txt:67-81`). The refreshed helper checks each treaty's active trigger and explicitly removes or restores ideas in both country scopes (`common/scripted_effects/COLDWAR_ARG_1970_treaties.txt:2467-2555` and subsequent generated pairs). The active triggers require both countries to exist. | Resolved in current emitted output; the same helper still needs in-game annexation testing. |
| Debt-crisis escalation used the wrong API for MD's high-interest state in an earlier source snapshot. | The current emitted check correctly uses `has_dynamic_modifier = { modifier = very_high_interest_country_modifiers }` at `common/scripted_effects/COLDWAR_ARG_1970_core.txt:10060`. MD defines it under `common/dynamic_modifiers/00_money_dynamic_modifiers.txt:2` and adds/removes it with `has_dynamic_modifier` at `common/scripted_effects/00_money_system.txt:2663-2668, 2715-2717`. | Resolved in current emitted output. The additional `interest_rate > 15` check is redundant with the dynamic-modifier branch but does not prevent detection. |

## Mechanics that passed static review

### Focus rewards, previews, and politics

- Focus completion separates display from execution: the focus tooltip calls `COLDWAR_ARG_preview_focus_*` under `effect_tooltip`, while the one-time guarded completion helper is in `hidden_effect` (for example `common/national_focus/COLDWAR_ARG_1970_focus.txt:4780-4783`; completion and preview helpers are in `common/scripted_effects/COLDWAR_ARG_1970_core.txt:8601-8608`). The preview helper itself is display-only. Material changes run once behind a completion receipt and a rechecked trigger.
- Party branches use native ruling-party triggers as availability requirements and have no party-gated `allow_branch`; there are no `allow_branch` statements in the emitted tree. Thus the content remains inspectable while the ruling party differs. Execution and active programme ownership are guarded separately.
- Programme refresh zeroes and recomputes modifiers from completed-focus receipts and current owner checks, then adds/removes the active dynamic modifier (`common/scripted_effects/COLDWAR_ARG_1970_core.txt:1-10` onward; definitions in `common/dynamic_modifiers/COLDWAR_ARG_1970_programmes.txt`). A party or leader leaving deactivates the matching programme modifier and weekly contribution. Returning recomputes from receipts, so construction, treasury changes, research, and other one-time rewards do not replay.
- The approved design's religious/political context is reflected in its party identities; no Salafi, Shia, or other invented Muslim pathway appears in the emitted modifiers, ideas, scripted effects, or events.

### Modifier support and economic units

- The emitted programme dynamic modifiers map catalogue variables to native MD or registered Imperia modifier keys. Current target evidence includes target modifier definitions and active readers for MD fiscal modifiers in `common/modifier_definitions/money_modifier_definitions.txt` and `common/scripted_effects/00_money_system.txt`; ordinary HOI country modifiers are also used by native ideas and dynamic modifiers. `imp_sanction_resistance` is registered in `common/modifier_definitions/mdcw_imperia_globalism_modifiers.txt` and read by `common/scripted_effects/imp_sanctions_effects.txt`.
- Semantic limits matter for player interpretation: `civilian_factories_productivity` feeds MD economic productivity/GDP calculations and does not itself change physical factory count or factory throughput; `resource_export_multiplier_modifier` changes export revenue, not resource output; the native MD key is spelled `agricolture_productivity_modifier`. `interest_rate_multiplier_modifier` is displayed as percentage points in the generator and is consumed by MD's interest-rate calculation.
- All recurrent programme, event, and treaty expenses enter MD's weekly aggregators in billion-dollar units. The Argentina helpers are called once in the current expense and income aggregation blocks (`common/scripted_effects/00_money_system.txt:2570, 4683`); the helpers add the resulting values to `additional_income_rate` and `additional_expenses_rate` (`common/scripted_effects/COLDWAR_ARG_1970_core.txt:10119-10138`, treaty transfer helpers in `common/scripted_effects/COLDWAR_ARG_1970_treaties.txt:3327+`). Setup payments use MD's `treasury_change` plus `modify_treasury_effect` in the guarded transaction.
- Treaty money direction and recurring arithmetic match the design: Argentina receives the $0.006 billion weekly Soviet grain transfer while paying its separately stated $0.001 billion weekly operating cost; Bolivia receives $0.002 billion weekly under the gas agreement while Argentina pays $0.003 billion and Bolivia pays $0.0005 billion weekly. The acceptance preview and recurring money helpers use these same values.

### Agreements and consent

- Every treaty active trigger checks both countries' existence and peace, no native bilateral embargo, and all eight directional membership arrays covering the four mirrored Imperia sanction classes. Example UK trigger: `common/scripted_triggers/COLDWAR_ARG_1970_treaties.txt:1100-1180`; there are 20 generated active triggers.
- Every dependent treaty requires the parent agreement's Argentine spirit plus active trigger and the recipient's parent spirit; the Brazil nuclear trigger demonstrates this at `common/scripted_triggers/COLDWAR_ARG_1970_treaties.txt:77-114`. Acceptance rechecks the parent requirement and current relationship conditions.
- Offers originate from Argentina focus rewards and send the named recipient an event. The recipient has distinct accept and decline decisions (`common/decisions/COLDWAR_ARG_1970_treaties.txt`); the refusal branch clears pending flags without charging or granting assets. A signed contract has no expiry. Refresh removes/restores both sides' ideas without repeating setup payments, construction, or research.
- Focus and acceptance previews call the same complete display helper. For example, Argentina's Brazil offer focus uses the preview helper and queues the actual offer only in its hidden completion helper (`common/national_focus/COLDWAR_ARG_1970_focus.txt:4769-4783`; `common/scripted_effects/COLDWAR_ARG_1970_core.txt:8601-8608`). Treaty previews show both setup payments, each side's signed modifier values and weekly flows, named spirits, research bonuses, buildings and slots, and the UK sovereignty transfer where applicable. Acceptance runs the guarded real transaction. Previews do not run execution.
- Current signed assets and research are one-time acceptance effects. Both directions' setup charges are paid once; recurring payments run through the weekly aggregators. An agreement's add/remove idea refresh has no setup or construction path.

### Building capacity and uranium

- Every emitted construction reward grants one shared state building slot per level before adding construction. In the focus/decision pipeline this is in the same guarded payout; for example `core.py`'s `grant()` emits the two effects in order. The approved focus and decision data has no building whose slot count differs from its level count. Treaty buildings use the same slot-per-level order in preview and acceptance.
- Core construction requirements check state ownership and control, native state level limits, shared slots where the building type uses them, and special uranium deposit/level data. For example, `common/scripted_triggers/COLDWAR_ARG_1970_core.txt:169-180` checks Cordoba ownership/control, the uranium mine state cap of 3, deposit modifier, per-level data, the one-mine reserve and free mine slot. Treaty infrastructure checks actual owner/control and state limit separately; infrastructure does not require shared capacity to build.
- The $4.000 billion sponsored uranium mine is funded by its construction decision rather than pre-paid by the survey focus. The focus bypasses if a mine already exists; the decision rechecks deposit, capacity, ownership/control, and no existing or under-construction mine before charging. The existing native mine investment remains independently available. The design does not grant raw uranium production or seed another deposit.

### Rosario and scenario reachability

- `COLDWAR_ARG_rosario_plan` is an actual war-goal reward in both its display helper and guarded payout: `create_wargoal` has `type = take_state_focus`, `target = ENG`, `generator = { 26 }`, and `expire = 730` in `common/scripted_effects/COLDWAR_ARG_1970_core.txt:8926-8946`. It does not use `autowar`.
- The core scenario trigger requires Argentina, a non-dynamic country, and MD's 1970 scenario trigger (`common/scripted_triggers/COLDWAR_ARG_1970_core.txt:2`). The initializer loads the Argentina tree and installs the six starting spirits once (`common/scripted_effects/COLDWAR_ARG_1970_core.txt:10080-10105`). Scenario date, receipt and routing checks stay internal to the actual trigger; player-facing availability requirements show gameplay conditions.

## Final bounded recheck

After the integration refinements, no confirmed remaining source defect was found in the reviewed mechanics scope.

- Treaty offer presentation now wraps retry-window and pair-clear requirements in meaningful `custom_trigger_tooltip` blocks while keeping their real checks inside `hidden_trigger` (`common/scripted_triggers/COLDWAR_ARG_1970_treaties.txt:45-79`, with equivalent forms for the other agreements). The focus completion path and recipient decision still call the full execution-side availability and transaction guards.
- The party-specific authoritarian routes require the relevant party still to govern, alongside their earned route receipt (`common/scripted_triggers/COLDWAR_ARG_1970_core.txt:5-15`). Constitutional civilian government requires elections and excludes the project's authoritarian-government trigger (`:16-22`). Elected handover requires the recorded winner to match the actual ruling party and the civilian constitutional trigger (`:2744-2750`).
- Native election resolution waits until both the election and coalition-forming flags have cleared, then records the actual `ruling_party`; handover rechecks that same party value before transition (`common/scripted_effects/COLDWAR_ARG_1970_politics.txt:234-280`). Slot 18 requires its identity choice before handover. The added political events use the registered `COLDWAR_ARG_politics` namespace (`events/COLDWAR_ARG_1970_politics.txt:2-4,33-35`), and leader ideology identifiers resolve to current MD ideology definitions in `common/ideologies/00_ideologies.txt`.
- The Argentina treaty refresh is now called from the daily global hook even if Argentina no longer exists, so a signed recipient's ordinary treaty idea can be removed when the active trigger fails (`common/on_actions/COLDWAR_ARG_1970_on_actions.txt:67-81`; `common/scripted_effects/COLDWAR_ARG_1970_treaties.txt:2467+`). The earlier source issue is resolved statically.

## Remaining verification

The output was statically inspected and compared with its runtime design. Native HOI4 load, fresh January 1970 start, locked-focus hover/preview rendering, party changes and re-entry, treaty accept/refuse/war/embargo/sanction transitions, Argentina annexation cleanup, saves, and weekly cash posting still need engine validation. Static generation and text inspection do not establish those runtime results.
