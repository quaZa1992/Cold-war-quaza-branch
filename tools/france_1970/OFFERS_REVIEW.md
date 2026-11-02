IMPERIA COLD WAR — French bilateral offers review

Reviewed 2026-10-23 against approved_design.json, SHA256 f90e6193464ffce880d3a6ba049568f779ccb0ab8111acb252c34118cdbdc780.

Scope and results

- All 24 approved offers are emitted: 16 reciprocal 365-day compacts and eight finite research exchanges. A direct emitted-block audit checked every modifier, treasury/Political Power charge, research category, bonus and use count against the approved source. Both governments have identical approved timed modifiers; both receive their separately named approved research award.
- Targeted decisions use ROOT France and FROM recipient, following the existing Soviet targeted-decision grammar. The invitation saves FROM as the global quoted recipient, snapshots both governments and dispatches a recipient-owned event. Recipient event ROOT receives only an invitation. Acceptance runs in recipient scope, rechecks both governments and financial requirements before either side is charged, then applies recipient effects and FRA-scoped French effects within one synchronous guarded block.
- Actual acceptance is an event option owned by the recipient. AI weights allow acceptance or refusal. No focus completion or proposal dispatch grants treaty effects to another country.
- One shared pending lock prevents concurrent invitations. At acceptance, the current recipient global reference and the 90-day age guard reject stale events. A stale refusal clears its own offer flag but cannot clear a newer quote to another recipient.
- Every timed acceptance rechecks that France has no active compact, then sets the shared active lock. Finite research exchanges do not grant temporary compacts, so completing an exchange alongside a compact does not evade the one-timed-compact limit.
- Research receipts have two independent durable gates: one France flag per offer focus, and one recipient flag for its research relationship with France. They survive party changes, withdrawal, expiry and timed-compact cleanup. Research-category eligibility derives from actual technology category membership and requires at least one unresearched category technology on each side.
- Timed ideas use native add_timed_idea, with the same 365-day duration on both countries. Daily maintenance detects missing ideas, war, lost sovereignty, failed French governing-party/date eligibility or changed government epochs/ruling slots and removes both halves. Separate active snapshots prevent a subsequent research proposal from rewriting compact government identity.
- Review fixed deleted-partner cleanup: every_country excludes removed countries, so maintenance now checks the stored recipient/partner existence separately in France scope and clears the pending lock or ends the surviving compact. Timed ideas and receipts on an annexed country have no active country consumer; restored countries are checked again by maintenance.
- Withdrawal is available to France and its active partner and executes the same bilateral removal helper. A renewed timed agreement requires a new proposal and consent and pays the approved acceptance charges again. Completed research grants are never replayed.
- Monetary setup costs call the native modify_treasury_effect with treasury_change. The approved recurring expenditure modifiers affect existing MD weekly education/administration bases; there are no invented fixed weekly transfers or annual runtime literals.

Integration checked

compile.py provides COLDWAR_FRA_<group>_government triggers, COLDWAR_FRA_government_epoch updates and France's daily COLDWAR_FRA_offer_maintenance call. For immediate cancellation on a recipient government callback, root integration should invoke FRA = { COLDWAR_FRA_offer_maintenance = yes } after the recipient epoch increment as well. Daily maintenance otherwise cancels within the next daily tick. Native government callbacks may not cover every same-party character replacement; no unverified leader-snapshot API was invented.

The offer preview API is COLDWAR_FRA_offer_<focuskey>_preview = yes. It contains a numeric tooltip only and never executes awards or charges. Core focus integration must call it in the visible reward preview.

Validation

The isolated builder was rerun against the in-repository approved design. The 24-event count, all numeric source contracts, guard and receipt presence, balanced script delimiters, UTF-8 without BOM scripts and UTF-8 BOM localisation passed. Python compilation passed. Decision, idea and event artwork references were checked against interface declarations (generic political discourse, generic diplomatic treaty and GFX_message_signing). Decision target eligibility uses existing sovereign countries and no bilateral war; HOI4 does not expose a separate ordinary diplomatic-contact acquisition mechanic in the inspected native patterns.

This is a static source and integration review. HOI4 engine execution, actual event option tooltips, save/reload and multiplayer timing were not run. The historical proposal source, authorship and provenance remain those recorded by the approved design and project notice; this review creates no new historical claims or third-party ownership assertions.

Final native-script formatting review

All five script outputs now pass through the existing Vietnam script_ast formatter. The builder compares the parsed Clausewitz AST before and after formatting and fails if semantics differ. It restores every generated custom-block marker at its matching declaration and retains the exact first-file project marker. Event acceptance exposes the actual scripted helper effects (native treasury/Political Power charges, timed ideas and research bonuses); the duplicate numeric custom terms were removed from that option. Numeric agreement terms remain in the nonexecuting focus preview. Rebuilding and Python compilation passed after the change.

Transitive localisation correction

The final localisation audit found sixteen missing add_tech_bonus.name keys. The compiler now emits both governments' approved research-award identifiers using their institutional offer title. A mandatory transitive audit checks every own custom_effect_tooltip, event title/description, event-option name, research-bonus name, decision/category name and treaty name/description before writing outputs. All references resolve after regeneration. Python compilation and semantic formatting assertions passed again.
