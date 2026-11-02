IMPERIA COLD WAR — Native bare effects presentation review

Reviewed 2026-10-23 against regenerated France focus, offer decision, event and scripted-effect outputs. This review did not change runtime files or generators.

Native reference comparison

The upstream common/national_focus/05_france.txt Greece/eurozone reward around line 791 uses the stock TT_IF_THEY_ACCEPT heading immediately followed by effect_tooltip containing prospective effects. The NEPAD reward around line 19288 uses unlock_decision_tooltip for each newly available decision. The new French offers use these same native constructs: focuses unlock their targeted decision; its completion tooltip uses TT_IF_THEY_ACCEPT followed by native prospective effects; the actual invitation is hidden. This avoids explaining or executing a foreign award at focus completion.

Whole-tree review

An independent parsed-output check covered all 234 completion_reward blocks. Their visible previews contain no proposal flags, earned receipts or event-target bookkeeping. The only custom_effect_tooltip entries are stock modifies_dynamic_modifier_tt headers with their named programme; numeric variable-effect rows remain native effect rows with explicit modifier tooltip keys. Exactly 24 foreign focuses use unlock_decision_tooltip. No consent or programme-ownership explanatory paragraphs remain in these focus reward previews.

Offer review

All 24 recipient events contain one native effect_tooltip preview and a separate hidden acceptance transaction. The preview runs in recipient ROOT and enters FRA for France's effects. Targeted decision previews run in France ROOT and enter FROM for the selected recipient. Native add_ideas, add_tech_bonus, add_political_power and modify_treasury_effect paths expose named spirits, research numbers and actual financial amounts. The native treasury helper itself provides its standard monetary tooltip. No raw pending/active flags, research receipts, snapshots or government eligibility branches are exposed as acceptance effects. Decline bookkeeping is hidden. The previous custom terms and pending explanatory tooltip paragraphs have been removed.

The stock conditional-acceptance heading is appropriate to prospective decision effects; it is not duplicated on the recipient's acceptance option, which directly shows its native results. The actual transaction remains hidden and guarded, so preview rendering cannot pay out a grant or charge a country. Existing daily/permanent lifecycle semantics are retained by this presentation change.

Decision label correction resolved in source

The compiler now emits loc[id] = o['title'], using the plain approved offer title for every targeted decision. This removes the recipient-dependent [From.GetName] suffix from names reused by focus unlock tooltips. Selected-recipient references remain appropriately confined to targeted decision descriptions. The generated localisation is refreshed by root's next regeneration.

Prospective previews and runtime guards

The visible preview is a separate effect_tooltip block constructed from the native numeric reward operations. It exists in source independently of the real transaction's eligibility gate; a false runtime gate therefore does not suppress the prospective award listing as it did when visibility depended on a guarded execution helper. The actual transaction runs only through the separately hidden, guarded apply/accept helper. This preserves informative prospective native rows while preventing a tooltip from executing them. Standard MD headings and numeric effect formatting supply the visible structure; authored explanatory effect paragraphs are absent. The whole-tree coverage and source-model results are recorded separately in FULL_TREE_COVERAGE.md.

Validation and limits

Static AST assertions passed for all 234 reward previews, exactly 24 native decision unlocks and all 24 native event-option previews with hidden transactions. Root's numeric-preview/actual-effect comparison is complementary validation of amounts. This review checked source presentation and scope, not HOI4-rendered tooltip appearance; engine hover rendering and multiplayer execution remain unperformed.


Final emitted-source refresh: the builder was regenerated after the decision-name correction. All 24 decision labels now equal their plain approved titles; native acceptance previews and hidden execution match for both countries. The final validator and programme/offer models pass. All 234 interactive preview selections and 288 prerequisite links pass browser checks, with zero explanatory paragraphs inside effect fields. Native HOI4 hovers remain untested.
