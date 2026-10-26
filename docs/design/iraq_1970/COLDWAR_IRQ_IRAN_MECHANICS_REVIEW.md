# COLDWAR_IRQ — Iran escalation mechanics review

18 October 2026. Static concept review by the separate `iran_war_mechanics` agent, transcribed by the author after its final response. No live installation or HOI4 test. The subsequent final changes selected four already-used native icons and normalized new English prose spacing; mechanics were unchanged.

**PASS for the corrected source concept, with integration still proposed.** Both exclusive preparation plans reach the state399 claim, its conquest war goal and the offensive activation decision. Gulf credit and supplier responses are optional and cannot veto the attack. Each doctrine has22 structurally reachable focuses out of26; the unselected doctrine and its three dependent focuses are excluded.

The native claim is `add_state_claim = 399`. The180day goal uses `take_state_focus`, PER and `generator = { 399 }`, with the existing native threat helper. Neither effect grants an Iraqi core, transfers ownership, or forces peace. Current1970 Khuzestan contains11base oil, with actual occupation, infrastructure, export and market limits.

PER-targeted attack, planning speed, supply, fuel, personnel cost and timed-idea syntax were checked against native MD sources, recorded in `COLDWAR_IRQ_IRAN_ROAD_TO_WAR.md`. The short opening gives90days of+8%attack; the sustained opening gives120days of+5%. Attack targets PER forces anywhere, while the other stated effects are country-wide. A permanent consumed flag prevents a second opening. Follow-up attacks are paid, cannot overlap opening/follow-up benefits or their own previous bill, and may coexist with remaining initial mobilization costs.

The new observer distinguishes lifetime first-war history from each continuous war. It closes the first30day window, applies attrition after180continuous days, removes only present operational bonuses at peace, and preserves fixed-duration bills. Start and peace transitions execute programme reconciliation. Earned territorial packages request guarded daily reevaluation. Each observer call requests at most one reconciliation, which must not replay any one-time delivery.

The review found and the author corrected two concrete blockers before finalization:

- **Quick-victory continuation:** Campaign Ledger originally required an ongoing war. Its gate now reads the persistent observed-war record, so winning before completing that focus does not block later administration.
- **Programme eligibility:** Arabistan Secured originally inherited its completion-time peace requirement. Explicit live conditions are now distinct from delivery gates; its earned regional programme continues while Iraq owns and controls399, including during a later war.

Oilworks funds one actual infrastructure level. The+10%national oil-export multiplier/+6%bureaucracy package remains dormant until Iraq owns and controls399 and its infrastructure exceeds2. It is neither a provincial output bonus nor a guaranteed total-income increase. `399 = { add_compliance = 5 }` gives five percentage points once; the state remains non-core.

The final source review found no remaining blocking mechanic issue. The author subsequently compared every embedded preview field with the rebuilt422-record catalogue, checked localization/ID closure and the two corrected gates, and reran browser QA. The final catalogue, focus specimen, idea specimen, campaign observer specimen, English localization and preview have the fingerprints recorded in `DESIGN_VALIDATION.json` and the independent layout review.

Remaining work after approval: implement the new observer hooks, first-war initialization, frozen-invoice decision wrappers, selected/earned programme reconciliation, actual settlement-provider synchronization, offer/response pipelines and truthful native tooltips. Test the1970start, combat timing, money, ownership/control/infrastructure changes, party changes, peace, save/load and multiplayer. Source-supported templates and a faithful browser are not engine verification.

## Superseding core continuation review

The same independent mechanics reviewer subsequently checked the four-focus core continuation requested by the user. **PASS**, with no blocking finding in the emitted426-focus concept. Settlement(92,28), civic/central alternatives(90/94,29) and the OR-joined core(92,30) match the catalogue. The final once-only transaction rechecks state399ownership/control, non-core status, infrastructure>=3, compliance>=60, resistance<15, peace withPER,730continuous holding days and the frozen6%GDP invoice. Debit precedes `399 = { add_core_of = IRQ }`. No other cores are removed and no extra population, resources or buildings are granted.

The new observer starts the holding clock on actual ownership/control, independently of focuses, party or war, and resets it only on losing ownership or control. Native control-change and authoritative peace/transfer hooks remain implementation requirements. Civic/central compliance grants are12/6points once; their earned administrative/social/political costs depend on current holding only and therefore continue after core delivery. Neither ongoing non-core status nor occupation metrics are required to retain the core or its programmes. These are alternate-history balance conditions, not historical Iraqi core claims. Exact native references appear in the current Road to War design document.

The author separately verified all422preceding focus records are unchanged by reconstructing the prior catalogue fingerprint. Final preview, English-key closure, navigation and native card geometry are checked in their own current reports. Runtime coring, tooltip and multiplayer behavior remain untested pending implementation approval.
