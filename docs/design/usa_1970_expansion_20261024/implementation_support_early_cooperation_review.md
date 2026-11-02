IMPERIA COLD WAR: Independent early US cooperation review

24 October 2026. Reviewed `early_cooperation.py`, its emitted scripts, ideas, events, decisions, English text, focus specs and research record. This is a provider review before parent-owned integration. No shared compiler, loaded runtime, generator or test was edited by this reviewer, and no game process was launched.

## Result

No remaining confirmed provider defect was found in the final reviewed version. Five source issues raised during the review were corrected by the author:

1. The actual Nixon-root completion checked the presidency but omitted the USA's NATO membership. `common/scripted_effects/COLDWAR_USA_1970_early_cooperation.txt:719` now rechecks both conditions, matching the root's visible availability.
2. The initializer repeatedly authorized any completed root without an authorization flag. This could bypass a rejected fresh completion on the next tick. Its historical migration is now enclosed by the once-only `COLDWAR_USA_early_initialized` receipt at `:725`. It can migrate an old completed mandate once while leaving a new invalid completion rejected.
3. The capped USA alliance spirit showed its personnel modifier but omitted its actual separate weekly expense. It now has a numeric custom modifier tooltip at `common/ideas/COLDWAR_USA_1970_early_cooperation.txt:184`, using the alliance-only `COLDWAR_USA_early_alliance_weekly_expense` variable. Reconciliation updates the value immediately; the pure fiscal aggregator recalculates it independently. ISR/trade costs are excluded from this particular spirit's amount.
4. The generic root preview placed all partner terms and costs inside a membership-filtered world scope. It now contains an unconditional recipient template and a separate per-accepted-partner USA cost at the effects provider's `:476`. A world with no currently eligible partner still has the complete prospective terms in the source preview.
5. A current member blocked by war, sanctions or embargo during initial dispatch could never receive its first offer after relations improved. Eligible country scopes are now recorded before delivery, and a bounded candidate-array pass retries only the first undelivered offer. The three fixed parents similarly retry their first authorized delivery. Declined or expired delivered offers do not produce repeated unsolicited events.

A sixth finding concerned the test model rather than runtime: inherited war/embargo evaluation compared literal `PREV`, so it failed to exercise the USA-side relationship. The author corrected operand resolution and added bilateral acceptance/suspension/restoration cases. Installed native trigger documentation explicitly supports `PREV` for both `has_war_with` and `is_embargoing`; the emitted scopes themselves already used the correct supported target.

## Consent, terms and real costs

The three roots create offers only. They do not grant either side's spirit, doctrine reduction, money, buildings, equipment, territorial control or membership at completion. Canada and Mexico receive independent offers and consent separately. Israel receives its own security-assistance offer.

The fixed pairs' signed national-spirit terms are:

| Pair | USA | Recipient |
| --- | --- | --- |
| Israel | Army experience gain +5%, production efficiency retention +3%, equipment cost +1%, weekly expense 0.01 | Division organisation +4%, organisation regain +4%, equipment cost -2%, personnel cost +2% |
| Canada | Factory output +2%, production efficiency retention +3%, tax collection efficiency -1%, weekly expense 0.005 | Factory output +3%, production efficiency growth +3%, tax collection efficiency -1% |
| Mexico | Factory output +2%, production efficiency growth +3%, tax collection efficiency -1%, weekly expense 0.005 | Factory output +3%, production efficiency growth +3%, education cost +2% |

Actual allied-readiness eligibility requires the USA's `NATO_member` spirit and the recipient's real `NATO_member` or `Major_Non_NATO_Ally` spirit. There is no static recipient-tag whitelist, automatic membership grant or forced war entry. The author publishes a native membership-change hook for later admissions or returning members.

Each accepting readiness partner receives organisation +3%, supply consumption -3%, personnel cost +2% and one 50% land-doctrine reduction. The USA receives one shared coordination spirit with organisation +2%, army experience gain +5% and personnel cost +2%. Its modifiers remain one static copy regardless of partner count. The USA receives one doctrine reduction in total; each recipient has its own persistent grant receipt.

Every actually active accepted readiness partner adds 0.005 MD billion to the USA's weekly expense. Thus the early module's total USA expense, with all three fixed pairs and N active readiness partners, is 0.02 + 0.005N. The coordination spirit shows only 0.005N, distinct from the personnel-cost percentage and the fixed-pair expenses. There are no setup fees or one-time assets in these early contracts. Existing advanced Israeli, Canadian and Mexican grants and fees remain separate negotiations.

## Lifecycle and replay checks

The readiness acceptance guard rechecks a current authorized pending offer, correct non-USA recipient, actual membership, both countries' existence, bilateral peace, both native embargo directions and all 16 mirrored sanction-array combinations. The fixed pairs use explicit named recipients and the same four-class bilateral policy. No party or alliance change can make a stale pending acceptance grant a package.

Signed receipts survive temporary suspension. Daily reconciliation restores paired spirits only when their actual conditions return, without calling setup or doctrine grants. If another partner remains active, the USA's shared institution remains; the suspended partner loses its own spirit and contributes no weekly expense. Repeated consent, suspension and recipient termination/reacceptance do not farm doctrine reductions. Acceptance-array insertion is guarded against duplicate countries.

Recipients can decline, reconsider after the consultation interval or terminate. The USA's targeted termination removes only the selected accepted country and blocks it from reopening against the sponsor's withdrawn authorization. Other partners continue. A recipient can terminate after the USA disappears. Partner ideas also have native cancellation conditions for a missing USA; billing requires the live sponsor. The model does not simulate the engine's automatic idea-cancel scheduler, so that specific cleanup is source evidence, not an observed native tick.

Recurring fiscal calculation resets its own amounts and sums actual active terms. It grants no spirit, doctrine, cash, event or receipt and performs no reconciliation. Initial dispatch is the focus-time world pass. Recurring reconciliation visits stored candidates/accepted scopes and three fixed contracts, rather than scanning every country daily. Work therefore follows the stored membership/offer footprint; this is a source workload description, not a native timing measurement.

## Preview, native presentation and research

All three roots directly call nonexecuting `effect_tooltip` previews. Fixed pairs show both named countries, exact spirits, every signed modifier and weekly expense without acceptance or active-state guards around their initial terms. The readiness root now shows the complete USA institution, generic recipient spirit/modifiers/doctrine and per-partner USA expense unconditionally, independent of current member count, eligibility, signatures or suspension. Recipient acceptance options show the actual incremental doctrine grants, omitting a coupon already received. No preview executes a transaction.

The installed effect documentation at `E:/SteamLibrary/steamapps/common/Hearts of Iron IV/documentation/effects_documentation.md:3644` defines `effect_tooltip` as displaying effects only. Its `for_each_scope_loop` definition at `:4296` supports stored scope arrays. The native MD NATO effects also use these country-scope loops, while the actual membership providers are `common/ideas/Factions.txt:5` and `common/ideas/united_states.txt:276`.

The native MD `USA_focus_gold_star_program` at the donor `common/national_focus/05_usa.txt:5421` costs 8.6 and combines army experience, leader experience, army attack/defence and construction benefits with personnel, education and training costs. This supports mixed institutional readiness bundles with real trade-offs, rather than an unqualified gain per allied country. New numeric values and weekly budgets are authored balance choices.

The primary historical sources were checked independently: [Nixon's March 1970 security commitment](https://history.state.gov/historicaldocuments/frus1969-76v23/d103) and the [August 1970 costed assistance review](https://history.state.gov/historicaldocuments/frus1969-76v23/d153) support security assistance and consultation. [NATO's December 1970 defence programme](https://www.nato.int/en/about-us/official-texts-and-resources/official-texts/1970/12/03/alliance-defence-for-the-seventies) supports funded readiness and shared burdens. The [Canadian treaty record](https://www.treaty-accord.gc.ca/details.aspx?id=100604) confirms the 1965 automotive agreement; Mexico's [official maquiladora history](https://www.economia-snci.gob.mx/sic_php/pages/importa/abc_maquiladora.php) dates its border-industrial policy to May 1965. These support distinct bilateral institutions, not a 1970 NAFTA or a claim that modern MNNA law already applied. Native MD status is used for RP eligibility, as the research record explicitly distinguishes.

All new event definitions use unchanged `GFX_political_deal`, the previously verified native 217 x 163 frame. Idea art resolves to real 60 x 68 NATO, trade and Defense Department textures. The new readiness focus uses the existing 100 x 88 NATO cooperation goal artwork. The three captions measure 113, 130 and 133 pixels in the actual native bitmap font and fit the 147-pixel title area. No new binary asset or global GUI/font edit is required.

## Independent validation and integration boundary

Fourteen final emitted-AST model tests passed independently with regeneration skipped and both file-write methods blocked. The reviewer also exercised 29 extra adversarial cases: 16 mirrored sanctions before acceptance, both war/embargo directions before and after consent, lost USA/recipient membership, unrelated-country sanctions, terminate/reaccept replay, and blocked Canada while Mexico proceeds. The additional runs initially exposed the model-only `PREV` limitation; the completed model now resolves those targets and explicitly tests those directions.

Exact reviewed hashes for the generator, final tests, seven emitted providers, research, specs and author validation are in `implementation_support_early_cooperation_review.json`. The generator SHA256 is `eef835813622c59207f554cce90e8d0006687f84b28182b61c84c923e62710c3`; the effects provider is `e086654829c99c314ec8f10ae9fea60d71b9d729fa8678b54efbcbfed6a23460`.

The parent still owns replacement of the three roots and their old execution/retry bundles, safe removal of recorded old recurring helper contributions, once-only money-hook integration, native admission/removal callbacks and all three advanced agreements' parent checks in offer availability, final acceptance and ongoing readiness. Hooking actual idea addition/removal is the most complete way to cover native admissions through different effect/focus paths; the module itself does not mutate those shared definitions.

This signoff covers the stable provider and source/model cases above. It does not assert installed full-tree integration, a post-change native event delivery, zero-member hover rendering, idea-tooltip display, native scope-array persistence after reload, automatic cancellation ticks or multiplayer synchronization. Those remain distinct checks. No current game process was controlled.
