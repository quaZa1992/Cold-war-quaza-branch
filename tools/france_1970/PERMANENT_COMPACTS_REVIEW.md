IMPERIA COLD WAR — Permanent bilateral compacts: sanctions and performance review

Source review, 2026-10-23

The current diplomatic UI writes the Imperia sanctions arrays directly in common/scripted_diplomatic_actions/imp_sanctions_diplomatic_actions.txt. Diplomatic imposition (lines 34–49), financial imposition (126–141), economic imposition (226–241), and military imposition (326–341) all execute in recipient THIS scope. They add the sanctioner ROOT to the recipient's imp_<type>_sanc_on_us array, then enter ROOT and add PREV (the recipient) to imp_<type>_sanc_by_us. The corresponding lifting blocks remove the same two memberships (79–94, 179–194, 279–294, 371–386). The UI's eligibility checks consult these same arrays, so the runtime compact condition should use them rather than opinions, modifier names or a separately maintained sanctions flag.

Historical 1970 initialization uses IMP_sanctions_add_<type>_from_prev in common/scripted_effects/IMP_sanctions_support_effects.txt, lines 6–51. Its documented scope is recipient THIS, sanctioner PREV. Each helper writes the same incoming/outgoing mirrored arrays with duplicate guards. Thus the pair-local test covers both player UI sanctions and scenario sanctions.

Recommended condition, evaluated only in the stored compact partner's scope:

OR = {
    is_in_array = { array = imp_dip_sanc_on_us value = FRA }
    is_in_array = { array = imp_dip_sanc_by_us value = FRA }
    is_in_array = { array = imp_fin_sanc_on_us value = FRA }
    is_in_array = { array = imp_fin_sanc_by_us value = FRA }
    is_in_array = { array = imp_eco_sanc_on_us value = FRA }
    is_in_array = { array = imp_eco_sanc_by_us value = FRA }
    is_in_array = { array = imp_mil_sanc_on_us value = FRA }
    is_in_array = { array = imp_mil_sanc_by_us value = FRA }
}

The on_us memberships mean France sanctions the partner; the by_us memberships mean the partner sanctions France. Explicit value = FRA avoids ROOT/PREV interpretation changing when maintenance is reached from on-actions, an event, or a scripted effect. Eight partner-local membership tests are sufficient for the supported runtime array contract. Testing the France mirrors as well would duplicate work and should only be considered for unsupported corrupted or manually edited save states.

Performance recommendation

Gate maintenance on France's pending or active lock before entering stored event targets. Scope directly to event_target:COLDWAR_FRA_offer_recipient for proposals and event_target:COLDWAR_FRA_compact_partner for an accepted compact. No every_country or every_other_country loop is needed. A compact cannot change its counterpart after acceptance without a fresh proposal, so its stored partner is the authoritative scope. A fixed offer discriminator or partner-specific active flag can select the idea pair for removal without a worldwide search. Native add_ideas provides unlimited duration; no native timed idea expiration, party trigger, quoted government epoch or ruling-slot comparison should remain in accepted-compact maintenance. Proposal quotes may still reject changed governments before acceptance under the approved consent rules.

The new authorized behavior replaces the former annual term/government-bound model. Accepted bilateral modifiers should persist through either government's change and should terminate for bilateral war or any listed bilateral sanction. Existing one-use research receipts must remain durable. Lifting sanctions must not automatically regrant a removed compact. A new compact requires the normal new-consent path and any approved setup charges.

This record is a local runtime source review; it adds no historical claims or third-party assets. Source credit is the original Moveably notices retained in the referenced sanctions files; other authorship/licence information is unknown here and remains subject to IMPERIA_COLD_WAR_NOTICE.md. Engine execution and multiplayer timing are not yet tested. Generated-offer review completed below.

Generated implementation review

Reviewed the actual regenerated build_offers.py, offer_policy.json and runtime scripts after the lifecycle override. No blocking defect found in the requested permanent-compact lifecycle.

- The policy override preserves the immutable approved-design hash and changes lifecycle without changing approved modifier amounts or research bundles. An independent parsed-output audit confirmed all sixteen modifier dictionaries exactly match the approved source and all eight finite exchanges still emit both research awards and their durable receipts.
- All compact grants now use add_ideas, with no add_timed_idea anywhere in the offers effects. Accepted maintenance and native idea cancellation contain no ruling-party, government-epoch or quoted-government requirements. Pending invitations retain their original quote and 90-day checks.
- The actual relationship trigger has exactly the eight recommended local sanctions memberships, all explicitly value = FRA, plus bilateral war and the pre-existing existence/sovereignty requirements. Both government changes can therefore preserve an accepted compact. Loss of sovereignty and signatory disappearance still terminate it under the existing eligibility contract.
- The parsed emitted effects contain no every_country or every_other_country loops. France first checks its pending/active locks, then inspects only the saved corresponding target. Compact removal cleans France and the saved partner directly. Fixed checks over the sixteen known offer flags do not scan the world's countries.
- Native idea orphan cancellation checks the specific accepted offer flag and saved partner identity. Accepted flags and the saved counterpart are established before either permanent idea is granted. Neither idea's cancel block references government eligibility.
- Existing accepted timed ideas migrate by remove_ideas plus add_ideas only when the permanent migration receipt is absent and both old idea halves remain present. No treasury, Political Power or research award is emitted by this migration. The migration receipt is then stored on France. Fresh acceptance stores it immediately, avoiding redundant migration.
- Withdrawal's visibility and execution both require France's current active lock or the actual saved partner identity with its partner flag. A restored former partner carrying a stale flag cannot withdraw from a different country's current compact.
- War or any supported bilateral Imperia sanction fails the active relationship check and executes bilateral cleanup. Lifting the sanction contains no regrant route; reinstatement requires a new proposal and acceptance. Detection runs through the existing daily maintenance path, so sanction termination can occur on the next daily tick; no unsupported immediate global sanctions callback was introduced.

Static AST assertions passed for the no-country-loop/no-timed-grant contract, all eight exact sanctions memberships, absence of government quotes from accepted maintenance, sixteen approved modifier dictionaries and eight dual research grants. This independent review did not mutate the builder, policy or generated runtime files. HOI4 engine/save-migration and multiplayer execution remain unperformed.
