# NKO 1970 implementation: independent core audit

**Scope:** Read-only review of the approved v2 focus output, its core triggers/effects/modifiers, and NKO 1970 startup. Foreign Diplomacy, domestic programme outputs and Kim Jong Il succession are excluded while their implementation is in progress. The audit compares emitted output to `v2/COLDWAR_NKO_v2_design.json`; it does not certify HOI4 runtime behavior.

## Findings

No concrete defect found in the reviewed core scope.

- All 189 design focus IDs appear exactly once in the emitted tree. Parsing the tree and design found no mismatches in focus icon, emitted coordinate/anchor, cost, grouped prerequisite semantics or mutex list. Independently resolving all 189 design anchors found no missing or cyclic anchor, coordinate mismatch, missing prerequisite ID or nonreciprocal mutex.
- All 48 distinct focus icon IDs used by the design are registered in `interface/goals.gfx`, with existing texture files. This verifies registration and file presence, not artistic suitability in the live focus view.
- Every nonempty focus modifier dictionary matches the corresponding emitted dynamic modifier's field/value pairs. The 51 unique fields are backed by the active MD/Imperia source; specialized unit fields are registered in the MD unit modifier list, and `imp_sanction_resistance` is registered by this mod.
- Availability and execution share each focus's `COLDWAR_NKO_can_<key>` guard. Party-branch slot metadata matches the containing design section, and the 1970 WPK route uses ruling-party slot 4. Completion helpers require the same `can_` trigger and an unset `*_earned` receipt before setting the receipt and applying the payout. Thus focus refreshes do not replay the focus's one-time payment or other effects.
- Party-bound modifiers use their earned receipt and current ruling-party slot in their `enable` condition. The refresh helper adds valid modifiers and removes invalid ones. Government and ruling-party on-actions call it; earned receipts remain available so a returning party regains its earned programme.
- The 1970 start is supported by source: the NKO history block sets ruling-party slot 4, creates Kim Il Sung, and loads `COLDWAR_NKO_1970_focus` in the pre-1985 branch. The focus-tree country selector and init helper require original tag NKO and the 1970-scenario predicate. Startup and weekly hooks call initialization, which sets a one-time initialization flag and refreshes the starting modifiers.
- The reviewed script files are UTF-8 without BOM; the focus localization file starts with the required UTF-8 BOM.

## Follow-up: foreign agreements and succession

**Scope:** Independent static review of the current emitted foreign-agreement effects/triggers/dynamic modifiers, native weekly budget integration, and Kim Il Sung succession outputs. Domestic outputs and unfinished foreign UX/localization feedback were not re-audited. This remains a source review, not an in-game test.

No additional execution-path defect found in this scope. The foreign agreement helpers debit each saved quote once for each signatory after acceptance. Recipient decisions show an `effect_tooltip`, then invoke the hidden executor; acceptance triggers require the pending receipts positively, so they are not accidentally gated by `NOT pending`. The 90-day pending flags are symmetric. Refusal and expiry allow NKO to resubmit after the pair is eligible again. The public signed-active triggers remain true through an upgrade; base active is excluded during upgrade and upgrade modifiers carry base values plus the increment. Refresh removes each agreement's two modifiers when pair eligibility fails. Weekly expenses require both signatory acceptance receipts and a clear pair, and the native money system calls the fee helper once (`common/scripted_effects/00_money_system.txt:4540`). The pair-clear triggers check diplomatic, financial, economic and military sanction arrays in both directions; for example, the Soviet pair checks all eight array/target combinations in `common/scripted_triggers/COLDWAR_NKO_1970_foreign.txt:7-24`.

The Soviet industrial reward validates either NKO-owned and controlled state 602 or 1200 with fewer than 50 industrial complexes, then adds the extra slot and factory in the same selected state (`common/scripted_triggers/COLDWAR_NKO_1970_foreign.txt:508-512`; `common/scripted_effects/COLDWAR_NKO_1970_foreign.txt:37-40`). Succession uses the July 8, 1994 event date, while the historical Kim Il Sung definition expires July 9; the event only kills a ruling-party-slot-4 leader whose ruling-only name is Kim Il Sung. If NKO is absent, the world-scope fallback broadcasts the event and sets the shared once-only flag (`common/scripted_effects/COLDWAR_NKO_1970_succession_effects.txt:5-10,23-28`; `history/countries/NKO - North Korea.txt:31-36`).

### Confirmed unit presentation issue in current output

The `productivity_growth_modifier` field is defined as `value_type = number`, not percentage, and the native productivity consumer scales that raw number by 0.5 (`common/modifier_definitions/money_modifier_definitions.txt:410-415`; `common/scripted_effects/00_productivity_effects.txt:84-93`). Therefore foreign agreement prose must not label values such as `0.06` or `0.03` as percentages. Other checked foreign agreement fields use fractional values for percentage modifiers; the interest-rate modifier is a numeric rate-point amount added directly during calculation (`common/scripted_effects/00_money_system.txt:2575-2583`).

No live HOI4 game check was run. In particular, dynamic modifier presentation, in-game agreement interaction and the exact fee behavior in a running campaign remain unverified.

## Evidence anchors

- `common/national_focus/COLDWAR_NKO_1970_focus.txt:3` defines the tree and 1970 country selector; lines 28–49 define the reachable Fifth Congress entry and its display/execution split.
- `common/scripted_triggers/COLDWAR_NKO_1970_focus_triggers.txt:3` defines the first focus guard.
- `common/scripted_effects/COLDWAR_NKO_1970_focus_effects.txt:3` shows the receipt-protected completion pattern; line 2486 begins programme refresh; line 6063 begins guarded initialization.
- `common/dynamic_modifiers/COLDWAR_NKO_1970_programmes.txt:135` begins the Fifth Congress modifier; party-bound entries include the receipt and party-slot condition.
- `common/on_actions/COLDWAR_NKO_1970_on_actions.txt:4` starts startup initialization; lines 20–35 provide weekly and government/party refresh hooks.
- `history/countries/NKO - North Korea.txt:13` sets historical 1970 politics, line 30 sets ruling-party slot 4, line 32 creates Kim Il Sung, and line 44 loads the 1970 focus tree.
- `common/modifier_definitions/mdcw_imperia_globalism_modifiers.txt:22` registers `imp_sanction_resistance`; installed MD `common/units/unit_modifiers/unit_modifiers.txt:25-112` registers the specialized unit modifiers used by the tree.

## Limits

No game parser, tooltip, campaign-start, party-transition, save/reload or multiplayer test was run. The above confirms static source correspondence and guarded reachability inputs only. The design JSON still has its original concept-status metadata even though the implementation task treats v2 as approved; this did not affect the emitted comparison.

## Final audit: latest foreign feedback and domestic outputs

**Scope:** Read-only review of the latest foreign feedback event set and refresh behavior, domestic advanced-funding decisions and account/safeguards/disruption effects, and succession date/event syntax. The review does not claim native engine parsing or live campaign behavior.

No concrete defect found in this update. The foreign output contains 72 unique event IDs and each has localized title, description and option text. The 18 closure notification receipts are unique by agreement and stage; they reset on a new submission, while the daily refresh notifies once after offer expiry or invalidation. The event calls target a country scope and use the established `country_event = { id = ... }` form. Recipient decisions and domestic decisions use standard `visible`, `available`, `complete_effect`, `effect_tooltip`, and `hidden_effect` structures.

Domestic advanced-funding decisions invoke the same one-time focus completion helper as the focus reward. The helper's `*_earned` receipt prevents duplicate funding/buildings; focus availability remains independent of that receipt, so using the advance decision does not block subsequently completing the focus. Credit settlement caps principal at outstanding debt and clears the account and credit modifiers once debt reaches zero; early review still requires an open account with positive recorded principal. Safeguard withdrawal clears the validity flag and refreshes both NKO programmes and bilateral modifiers. Patron-disruption mitigation charges 0.40% of GDP and removes the modifier in the guarded executor.

The succession helper still uses `date = 1994.7.8`, a positive exact-date predicate recognized by the local source-model tests. The installed MD and vanilla script samples I checked demonstrate relational `date <`/`date >` triggers but do not establish that exact equality is accepted by the native engine; no game parser was available for this audit. Therefore exact-date native trigger parsing remains an engine-only verification item, not a confirmed source defect. The surrounding event IDs, namespace, `is_triggered_only`, country/news event calls, event option triggers, and country-scope on-action calls follow forms used elsewhere in the installed scripts.

### Confirmed native army-experience tooltip unit correction

The installed MD localization currently formats `experience_gain_army_tt` as `$RIGHT|+=%1$` (`MD_dm_modifiers_l_english.yml:86`), but vanilla formats the same flat `MODIFIER_XP_GAIN_ARMY` as `$RIGHT|+=2$` (`modifiers_l_english.yml:252-255`). Vanilla uses the percentage format for the separate `experience_gain_army_factor_tt` key. NKO foreign modifiers use `experience_gain_army = 0.04` / `0.08`, so the flat numeric formatter is correct; the existing percentage formatter would mislabel the native dynamic-modifier tooltip. Both source localization files have UTF-8 BOMs.
