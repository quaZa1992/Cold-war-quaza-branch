# Independent focus-only UAE review — 19 October 2026

Final reviewed state: 114 national focuses, three authored UAE decisions,
1,920 UAE contract delivery IDs and 192 shared GCC admission delivery IDs.
This report distinguishes source evidence from live HOI4 behavior.

## Confirmed findings repaired during the revision

1. The Trucial cosmetic used the modern UAE flag pattern. Its former medium
   and small assets were pixel-identical to modern UAE flags. The final assets
   differ at all three sizes. The new large preview was visually inspected:
   red-white-red horizontal fields and a seven-point star, without the modern
   UAE green-white-black stripe arrangement.
2. The three Kuwait agreement providers initially required only completion of
   Gulf Diplomacy. The final `can_offer_kuwait_support`, `...transit` and
   `...deployment` triggers require their own new focus receipts. Their direct
   focus-dispatch helpers also require the corresponding receipt. Executing a
   helper with only Gulf Diplomacy complete now sends no proposal or payment.
3. The reused GCC offer originally accepted only nonmember recipients. That
   could leave the UAE focus unable to request admission from an existing
   Saudi GCC member. The common helper now permits a new member to petition a
   current member, retains actual recipient consent, charges only new members
   and rejects an offer between two existing members.
4. The UAE cooperation focus remains available to countries that already joined
   through another country's invitation. Its permanent national reward still
   applies once, without sending another petition. The petition preview now
   omits admission rows when UAE already belongs, matching actual delivery.

## Independent verification

`python tools/uae_1970/test_focus_only.py` passes nine installed-AST groups:

- All 114 nominal 70-day focuses have resolvable prerequisite/exclusion
  references, symmetric exclusions and an acyclic prerequisite graph.
- Exactly `oil_restraint`, `reserve_deposit` and `reserve_withdraw` remain in the
  authored UAE decision category. Existing focus unlock rows reference only
  these three. This does not assert that unrelated global MD decision systems
  contain no decisions.
- Native resource expansion is hidden for 1970 UAE only. The actual installed
  category predicate remains true for a later UAE start and another country.
- The historical federal council recognizes the association without enabling
  elections. The separate optional Constitutional Competition focus invokes
  actual electoral reform and wider party legalization once.
- Removed domestic courses do not add another temporary modifier, invoice or
  policy-menu event. Existing permanent focus programmes remain their source.
- The actual Arab Solidarity focus chooses Egypt, pays its existing domestic
  investment once, dispatches one real offer and applies the separate frozen
  agreement invoice/productivity only after recipient acceptance. Duplicate
  focus/helper/retry or accepted-option execution does not repeat delivery.
- Each Kuwait focus is complementary, requires an actual Kuwaiti war and its
  own receipt, dispatches once and grants only the accepted financial aid or
  military access. Neither aid nor access enters the UAE into war or creates
  troops. Without the actual new focus, the agreement helper grants nothing.
- The actual formation helper preserves the Trucial Council/name until the
  proclamation receipt; then Zayed is installed under Western Autocracy and
  the cosmetic is removed. Flag assets differ from modern UAE at every size.
- All 1,920 retained UAE contract IDs resolve in the audited installed UAE
  files. Sharjah, oil-downturn and Kuwait domestic policy-menu IDs are absent.

The separate shared GCC suite passes nine groups, including initial formation,
joining an existing Saudi member, refusal without charge, no second member fee,
duplicate and concurrent offers, cost previews and invalid contexts. The common
GCC charter decision is hidden only for UAE; the shared focus root still
requires the actual membership spirit.

## Native presentation comparison

Compared the emitted council/optional electoral reform, Arab Solidarity and
three Kuwait descriptions with their actual reward code. The descriptions
explain the institutions, invasion context, recipient consent and limits on
military commitment; they contain no implementation ledger or invoice catalogue.
Financial support previews the native UAE debit and Kuwaiti credit at 3% of UAE
GDP. Transit and contingent focuses show the correct directional native access
effect. These previews use `TT_IF_THEY_ACCEPT` instead of implying automatic
foreign agreement.

Reference grammar was checked against current installed main MD Russia:
`05_russia.txt:2295` (`SOV_CSTO_enlargement_with_ukr`) uses recipient event plus
`TT_IF_THEY_ACCEPT` and `effect_tooltip`; `05_russia.txt:15506`
(`SOV_lgbt_rights`) uses the named dynamic-modifier heading and signed native
numeric variable tooltips. This is a grammar comparison, not an assertion that
the UAE should share Russia's historical policy or superpower reward scale.

## Old “Reopen the Status Talks” display

The old decision ID and its English label are absent from currently loaded
workspace common/decision/localisation/event code. An inert pending-flag cleanup
remains intentionally. Read-only launcher evidence showed only
`mod/mdcoldwar.mod` enabled and pointed to this workspace; the active playset
likewise had only this directory enabled. No duplicate active mod path was found.
No HOI4 process was running when checked. A stale earlier process/save/UI is a
possible explanation for an old screenshot, not a proven cause.

## Limits

The interpreters execute installed authored guards, payments, receipts and
recipient options. Native economy recalculation, portraits, UI rendering,
save migration and live multiplayer delivery remain explicit boundaries. No
live HOI4 load or hover test was performed. No unresolved source blocker was
found in the final audited focus-only integration.

## Closure of the separate native GCC array defect

The previously reported P1 native membership-array defect is also repaired.
The bounded startup wrapper keeps the modern six-member seed unchanged and
uses actual sovereign membership in 1970. A founder-only refresh reconciles
membership loss, rejoining and native puppet/free hooks without clearing
legitimate nonfounder entries, resetting unity or replaying assets. The final
shared GCC suite passes ten groups, including actual native idea callbacks,
the installed native startup fragment and native joint-exercise dispatch to
real members only. The legacy adapter passes seventeen isolation/idempotence
checks. This closes the known source finding; engine tests remain unperformed.
