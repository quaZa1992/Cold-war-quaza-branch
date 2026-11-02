IMPERIA COLD WAR

# France 1970 bilateral party revision: emitted mechanics review

## Scope and source set

Read-only review of the compiled France runtime outputs produced from the approved 156-focus, 35-offer party revision and tangible balance revision. Source design hash: `5159aaad0f0b13bbf3ef38e2d374be05fcb907a5df6386c8b2e933520b278419`. Reviewed compiled design, scripted effects and triggers, recipient decisions, treaty ideas, focus previews, on-actions, and modifier consumers. No generated or live files were edited for this review.

## Emitted agreement surface

The compiled output contains 35 send, accept and active scripted triggers; 35 offer preview helpers; 35 acceptance effects; 35 recipient acceptance decisions; 35 decline decisions; and 35 reissue decisions. The reissue file also contains its shared category. The idea output carries two signatory ideas for each deal: 38 legacy-format idea IDs and 32 party-revision IDs. The complete fixed-recipient tag set is GER, ENG, USA, SOV, ALG, PER, SEN, ITA, SER, AUS and ARG.

Both send and acceptance guards check bilateral existence, peace, embargo and each of the four mirrored sanction arrays in both directions. Acceptance also rechecks the current proposer-party trigger, current GDP positivity, parent or organisation membership ideas, and all asset state checks before either country is charged. Recipient choice is confined to the named recipient's decision. The reissue path goes through the same current send guard.

The PCF Soviet parent and its Energy Engineering and Commercial Shipping continuations require both parent ideas where applicable. The two specialisations share the same pending and signed family flags and cannot both be accepted. Their signed effects depend on the parent agreement remaining active. Signed agreement activation does not depend on the proposer still holding the original party office, so existing agreements survive elections. The treaty synchronizer adds or removes the paired ideas and weekly shares based on bilateral status; it does not replay fees or finite awards. Daily orphan cleanup is bounded to the 11 named partners.

## Preview and reward APIs

Every focus completion reward calls its offer preview outside the execution guard. The generated preview itself has no eligibility or signed-state conditional and renders both the French and recipient scope, current-GDP setup charge, weekly GDP/52 amount, signatory idea, and any asset, finite research, doctrine, experience or faction-opinion effect. The idea definitions carry each signatory's complete signed modifier payload. This is source-level evidence; native rendering of those idea modifiers within the focus Effects hover still needs confirmation in game, because the preview uses `add_ideas` for the modifier payload.

The 35 deals use 25 building effects, six doctrine-cost reductions across `land_doctrine` and `naval_doctrine`, five service-experience awards, one internal-faction opinion adjustment, 45 finite research bonuses, 109 idea modifiers, 70 setup debits and 70 weekly expense shares. The native source has matching focus examples for doctrine costs and service experience, and the current internal-faction helpers support the registered opinion providers. Setup and weekly expenses use each side's own `gdp_total`; weekly annual shares divide by 52. There are no fixed-price substitutions or available-treasury gates.

Bilateral construction checks include state ownership, control, full control and the current physical building headroom before transaction effects. The emitted effects grant one extra shared slot per construction level before adding each building, including infrastructure. Construction checks for both signatories are part of the acceptance preflight before either setup debit.

## Save migration and date-gate finding

The existing 19 offer IDs, signed flags and spirit IDs are retained. The core migration clears and reconstructs the non-offer programme modifier pools from their existing `COLDWAR_FRA2_earned_*` receipts; it changes modifier values without repeating one-time GDP charges, research, experience, opinion or buildings. The two pre-existing signed offers `atlantic_training` and `iran_energy` also reuse their idea IDs, so existing accepted agreements receive the newly approved France-side cost modifiers when their existing ideas are refreshed or reloaded, with no repeated setup fee or one-time award. This is the effective save migration for those continuing agreements.

The first compiled output omitted the FN date predicate from `fn_export`'s send and acceptance triggers, although the focus itself requires the FN identity date. I corrected the generator's condition mapping so `FN identity` emits `date > 1972.10.4` in both transaction guards. The signed-active trigger remains date-independent. The compiled output examined here predates that source correction; recompile and native fixture verification are still required before treating the transaction guard as final.

## Source anchors

- Pair, transaction and preview output: `common/scripted_triggers/COLDWAR_FRA2_diplomacy_triggers.txt`, `common/scripted_effects/COLDWAR_FRA2_diplomacy_effects.txt`, and `common/decisions/COLDWAR_FRA2_diplomacy_decisions.txt`.
- Paired idea modifiers: `common/ideas/COLDWAR_FRA2_diplomacy_ideas.txt`.
- Daily and weekly sync, plus recipient cleanup: `common/on_actions/COLDWAR_FRA2_1970_on_actions.txt`.
- Native cost readers: `common/scripted_effects/00_money_system.txt:3240` for personnel costs, `:3440` for education costs, and `:442`/`:755` for corporate tax income.
- Native faction-opinion helpers: `common/scripted_effects/00_internal_faction_effects.txt:1001` and `:1055`.
- Party migration and current-party pools: `tools/france_1970_runtime/core.py:104` and `:650`.

## Evidence boundary

This is a source and emitted-file review. The root agent owns native fixture work. No live-game screenshot, all-build native load result, or multiplayer stability result is claimed here.