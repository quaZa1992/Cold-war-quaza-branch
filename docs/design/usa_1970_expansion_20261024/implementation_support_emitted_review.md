IMPERIA COLD WAR: Independent emitted USA expansion review

24 October 2026. Reviewed the canonical compilers and their emitted domestic, treaty, focus, decision, idea, trigger, event and money-hook code. This is a separate source review from the authors' model tests. No loaded runtime files were edited by this reviewer and no game process was launched.

## Approved catalogue and live graph

The approved catalogue has 65 authored nodes: 49 domestic/non-offer nodes and 16 recipient-approved offers. Thirteen existing focuses are reworked and 52 are added, retaining all 229 baseline IDs for 281 installed focus definitions.

An independent parse of the emitted complete `common/national_focus/USA_1970.txt` found 281 unique IDs, no missing prerequisite or exclusion references, no exact coordinate collisions, and exact coordinate agreement with all 65 approved nodes. No `allow_branch` remained, so party branches are inspectable. The earlier independent graph review also established acyclic AND/OR prerequisites and structurally feasible routes; that is not an engine availability test.

## Domestic programme review

Reviewed `tools/usa_1970_expansion/domestic.py`, `domestic_focus_specs.json`, emitted `COLDWAR_USA_1970_programmes` files and the native providers called by those files.

- The 49 focus specs match the 49 approved non-offer nodes. The compiler maps signed modifier rows, setup amounts, asset counts, experience, finite research bonuses and doctrine coupons from the approved catalogue.
- `CAT_industry`, `CAT_electronics`, `CAT_nuclear_reactors`, `CAT_aircraft`, `CAT_destroyers` and `CAT_submarines` are registered categories with actual technology consumers. Aircraft/electronics and destroyer/submarine packages split the two uses across their specified sectors.
- The installed native effect documentation declares `add_tech_bonus` and `add_doctrine_cost_reduction` in country scope. The latter's 50%, uses and doctrine-category structure matches the existing native Russia example at `common/national_focus/05_russia.txt:26229`.
- `state_limit` checks a US core, actual ownership and control, type maximum and native available capacity. E1/E2 additionally restrict their intended regional state pools. Real assets and their matching shared slots are inside one guarded completion effect; preview effects are kept separate.
- Native volunteer/draft effects remain the law-change authority. They are not replaced by the smaller new programme spirit. D1/D2 spirit activation is tied to the actual respective law; D2 also checks the incompatible all-volunteer doctrine.
- Reconciliation selects the highest earned tier and removes lower tiers. Party-bound tiers suspend off-party while their earned receipts survive. Setup benefits are absent from reconciliation.
- The old-save migration reverses only recorded unbounded USA bridge-variable deltas of the 13 reworks, marks their completed receipts, and grants the new programme tier without replaying money, assets, PP, XP, Congress, factions or laws. The bridge provider itself uses direct addition and no clamp, making those identified numerical reversals distinct from unsafe opinion/regulation reversals.
- The nuclear programme resets its weekly expense contribution to zero before conditionally assigning 0.03. It does not add another copy on repeated reconciliation.

Findings raised and corrected by the author:

1. The original prepared ready triggers did not retain D2/D3 congressional gates and D1/D2 force-model checks. Final ready conditions append the frozen original availability AST as real execution conditions. Pending enactment therefore rechecks those requirements too.
2. A capacity requirement contained the implementation phrase "native capacity". It now uses plain player-facing wording about available space.
3. `generic_research` looked like an idea identifier but resolved to the base-game focus medallion `goal_generic_scientific_exchange.dds`, 89 x 79. The author replaced it with `research_bonus`, an actual 60 x 68 idea texture. The other USA department icons resolve to actual 60 x 68 idea artwork.

A provisional concern about missing domestic Treasury prerequisites was withdrawn after checking the explicit national-tree project contract and the parent's instruction. Native domestic focus deductions may create a deficit. This is intentional, not an unresolved defect. The separately funded export-credit decision received its own explicit funding/recheck contract.

The domestic author reports 13 model tests passing, including 49 once-only completions, wrong-party completion, lost control and native caps, tier restoration, law changes, congressional races, old-save migration and weekly reset. The reviewer did not rerun that test entry point because its setup calls the compiler and the assigned review was read-only. Native engine behaviour remains separate.

## Recipient-approved agreement review

Reviewed `tools/usa_1970_expansion/agreements.py`, its 16 focus specs and all generated treaty functions. Key generation points are `preview_body`, `emit_triggers`, `emit_effects`, `emit_ideas` and `emit_decisions`.

Every original focus preview uses a nonexecuting `effect_tooltip` and directly lists every signatory, exact spirit, each signed modifier, setup payment, weekly income/expense and one-time asset or coupon. The original focus previews have no eligibility, signature, funding, sanction or party conditions around those prospective terms. Renewal controls separately omit already paid fees and received one-time assets. This distinction preserves complete original terms while showing the actual incremental renewal transaction.

Real transaction guards require the correct recipient, the USA's still-open offer, current final eligibility, all signatories' funds under the explicit bilateral contract and native asset capacity. Rogers obtains separate Egyptian and Israeli responses and ratifies only after both consents. One response alone charges and grants nothing. Egypt and Israel need not already be at peace with each other; the USA must remain clear with both.

Standing signatures and one-time receipts survive suspension. The active trigger requires both/all paired spirits, signatories and actual parent/membership conditions. All four mirrored sanction classes and native embargoes are checked in both directions, using only the counterpart's tag. The weekly accumulator resets both contributions before summing active terms, contains no payments/events/reconciliation and is scoped to the current country.

The German forward agreement separately adds USA income 0.02, USA gross expense 0.04 and German expense 0.02. Bahrain adds USA expense 0.02 and Bahraini income 0.02. Saudi terms add USA income 0.02 and Saudi expense 0.02. The real money integration appends treaty income and expense once to their native totals. It additionally appends the separate nuclear programme expense once. Setup remains distinct from recurring weekly values.

Temporary programmes use persistent calendar deadline flags, rather than restarting the clock when an idea is restored. Daily reconciliation removes both spirits and clears signatures when a term expires. Restoration calls no setup function. Family receipts also prevent German variant changes or repeated treaty cycles from farming factory, research or doctrine grants. Ordinary expiry/reoffer still requires new recipient consent.

All seven promised construction packages add the same number of shared slots before construction in the same state/transaction. Acceptance checks actual state ownership/control and native capacity. The Bahraini port also checks province 11181 control and province-specific capacity. State 624 has BHR ownership/controller in 1970, and its existing port level is 5 against the native level cap 10, so the proposed additional level is viable at the historical start. Its sovereignty remains Bahraini under this new agreement.

The agreement's `army_org_regain` mapping is valid native code. The installed `documentation/modifiers_documentation.md:1957` lists it, base-game `common/ideas/british_raj_goe.txt:1250` uses it in a country idea, and the native MD USA department also consumes it. `army_morale_factor` is another valid native recovery modifier, not proof that `army_org_regain` is invalid. Their labels should reflect the intended native effect.

The emitted agreement national spirits use real idea-art textures. All recipient and notification events reuse unchanged `GFX_political_deal`, the verified 217 x 163 country-event frame. The matching donor texture and complete adjacent option geometry were independently inspected in `implementation_support_native.md`.

One presentation finding was raised and corrected: a focus's direct call to `can_offer_*` expanded internal tag/scenario, signature, pending and cooldown receipt checks. The final focus spec hides the authoritative guard, then exposes native NATO and actual paired parent-spirit requirements plus meaningful yes/no labels for bilateral relations, pending offers, ratification and consultation intervals. The reviewer verified that corrected spec structure; the author reports all 16 visible wrappers modelled equivalent to their authoritative guards. The main compiler must install the refreshed specs. Native visual tooltip rendering remains a separate check.

## Legacy consolidation findings

Two integration findings were sent to the main author and the source corrections were verified:

1. Retiring original sending events while leaving queued renegotiation events 111, 121, 131, 151 and 171 executable allowed obsolete material registration and Israeli money transfers after consolidation. `compile.py` now includes these IDs in the retired event set.
2. Three Middle East policy decisions would otherwise require flags whose only new-game providers were the retired generic offers. Their requirements now accept either the historical receipt or the corresponding actual active new Israeli, Rogers or Saudi spirit. This preserves content without inventing a paid legacy receipt or calling old material helpers.

The main integration also replaced the two broad Bahrain news-picture assignments with the unchanged framed political-deal photograph. No global event GUI or frame pixels were altered.

## Evidence boundary

This review supports source consistency, declared scope, signed amounts, graph references and identified replay guards. It does not prove native visual tooltip rendering in every locked/nonexistent-country state, actual modifier impact, hard-cap behaviour at extreme state-slot limits, old-save execution, native calendar progression or live multiplayer synchronization. The original inventories, approved proposal and emitted runtime are different evidence layers and are labelled accordingly.

## Final installed-source visual review

Independently inspected the final `installed/USA_FOREIGN.png`, `USA_ENERGY_INDUSTRY.png`, `USA_DEFENCE.png` and `USA_FULL_INSTALLED.png`. The reviewed loaded tree is `common/national_focus/USA_1970.txt`, SHA256 `cde668bd4b711a14a7cfe07f63c8fbe6c492d50b313ec3f0034430a29783d380`. It contains 281 focuses and no conditional position offsets. The matching `installed/layout_evidence.json` SHA256 is `4a65539382c39ea090b83bec7f393e4ba45482f50f3ee7c7581dd89b340607e0`.

The branch composites use the loaded coordinates, registered source textures, actual titlebar and `hoi_16mbs` bitmap glyphs at the native 96 x 130 grid. They are source reconstructions, not native game screenshots. The full overview alone is reduced from 7056 x 7795 to 2600 x 2872; its purpose is branch footprint inspection, not small-text verification.

- Foreign policy: no target card, caption or icon collision was visible. The regional offers and follow-on programmes remain distinct and readable. Partial neighbouring cards at the crop edges are contextual content outside the selected branch, not missing focuses.
- Energy and industry: the two clusters remain separated and their new choices fit their allocated footprint. The branch image shows no missing artwork, card overlap or caption obscuring another focus.
- Defence: the recruitment, intelligence, joint technology, land-force and naval alternatives remain visually distinguishable. No target icon or caption collision was visible.
- Whole tree: the 281-node footprint retains the dated election modules and separates the expanded domestic, foreign and defence areas. No confirmed structural visual defect was found in the inspected source reconstruction.

An independent re-read resolved all 281 captions, with zero missing localisation keys. All advance widths agree with the evidence record and are at most 147 pixels. The final caption check found no missing font glyphs. Twelve captions at the edge of the permitted width have 1 or 2 pixels of outer glyph outline extending beyond the preview's fixed 147-pixel bitmap canvas: General Revenue Sharing, the seven Democratic victory markers, Negotiate from Strength, Telecommunications Act, Federal Industrial Grants and State Revenue Compacts. Their letters remain readable. This is a small static raster limitation: the actual engine may allow glyph overhang inside its wider focus container. It is not evidence that the game clips those captions, and no approved title was changed during this frozen review.

Some long prerequisite lines pass behind intermediate cards in these composites. The renderer deliberately uses a simple orthogonal midpoint route; it does not reproduce native link routing. Those lines support a suggestion to inspect long paths in game, rather than a confirmed engine overlap finding.

The continuous-focus rectangle is now at (-3200, 1800), with dimensions 770 x 380. The overview renderer does not draw that panel, so the image alone cannot verify its clearance. An independent rectangle check against all 281 focus footprints, conservatively expanded to each grid position plus (-35, -115, +205, +140), found zero intersections with the panel. Its source placement is therefore clear even under that wider static margin. Native camera, panel visibility and interactive navigation remain in-game checks.

Reviewed image SHA256 values:

| Image | SHA256 |
| --- | --- |
| `USA_FOREIGN.png` | `6a73c2ecd2f45f0c68c9d889456f0d8a8c7d003c8a21e5cdcfdf3fd67429a03d` |
| `USA_ENERGY_INDUSTRY.png` | `b973e9620db658276b6c42310c8d235b39a83d06297d49baee6c62214791d1ea` |
| `USA_DEFENCE.png` | `33aade8bfd2b006e45de06c673abef9f0bc4e8d276c580fae43b91ece3f211a2` |
| `USA_FULL_INSTALLED.png` | `7b201f6052c08c10d55b298241bd8992495d121ceea269a7682635be8ad0a49f` |

No loaded runtime file, generator, caption, image or approval record was changed by this final visual review. The separate native process launched by the parent is outside this review's evidence; this report makes no claim about its outcome.
