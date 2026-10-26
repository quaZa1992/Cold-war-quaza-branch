# Emitted Iraq/US audit revision: final review

19 October 2026. Read the installed focus trees, English localization, changed reward providers, retirement/migration paths and native main-MD reference examples. This is an independent read of the Iraqi implementation; the same reviewer authored the US-policy source, so the US portion is a follow-up source review rather than an independent author review.

## Result

No new blocking reward, territorial-scope or duplicate-payment defect was found in the sampled emitted implementation. At the initial read, all103 generated file hashes matched manifest.json. Iraq registers426 IDs/410 active focuses, with16 hidden unavailable compatibility stubs and empty rewards; the two sampled retired apply helpers only clear stale pending flags. USA preserves214 original focuses and registers15 added IDs/14 active cards.

Representative changes were read with their actual completion effects:

| Installed content | Verified native presentation and reward |
|---|---|
| Basic Industries First / Consumer Expansion | Iraq/Baghdad and Mosul-specific industrial descriptions;49days each; native named programme deltas, one state-scoped civilian factory each and5%/4%GDP respectively. One35% industrial research use on the basic-industry route. |
| A Professional Core / A Mass Reserve Army | Distinct professional/reserve policy stakes; native+8%organisation/+6%personnel versus+15%relative conscription/+8%recovery/-3%organisation;25XP and1%GDP each. |
| Fund Staff Training | Iraqi staff coordination narrative;35XP and one25%land-doctrine-cost reduction;2%GDP and+4%training time. The old additional organisation bonus is absent. |
| Mass Literacy / Train Teachers First | Immediate adult instruction versus teaching capacity; native literacy provider+0.06 versus+5%research and one25%industry bonus. Both2.5%GDP/+3%social expenditure. |
| An Oil Revenue State / Beyond Oil | Basra exports versus Baghdad civilian investment; actual1infrastructure in171 or1civilian factory in557, plus distinct programme deltas and3.5%/4%GDP. |

Compared with the actual normal main-MD source/localization: Russia SOV_stabilisation_fund uses an institutional narrative, native idea/decision unlock and treasury effect; SOV_military_education gives35XP in21days. Israel ISR_deliver_computers gives one25%IT bonus at3bn; Germany GER_modernise_mining_equipment one40%construction bonus at10bn; Turkey TUR_industrial_research two50%industry uses. Iraq uses the same native outcome grammar while retaining its own1970 prices and political circumstances. These examples validate the API/presentation pattern, not historical percentage values or complete campaign balance.

Native treasury calls in sampled Iraqi focus previews sit inside non-executing effect_tooltip. Their guarded apply helpers contain one real debit and once-only building/research/XP receipts; previews do not pay a second bill. Oil concession delivery intentionally has no second focus invoice: its recipient agreement quotes1%GDP once. The two treasury calls in acceptance event372 are the matching ENG credit and IRQ debit, not two Iraqi charges. Revenue-priority review10003 changes only current revenue/diversification flags, charges its review price, and contains no factory grant or ownership/concession reset. Saddam's finale now has+8%PP/-3%bureaucracy/-2%tax and no old stability filler.

The English focus/custom-tooltip references checked across the emitted new trees resolve. Actual UTF-8 contains valid smart apostrophes in a few descriptions, not replacement characters. Office construction uses generic_office_construct; power dispatch uses national_grid; selected Saddam policy cards now use appropriate staff/intelligence art. Basra171, Nineveh166 and Baghdad557 match their intended grants; no new foreign-territory building error was observed.

## Presentation finding and correction

Three US focus availability conditions still exposed raw budget/current-policy variables: relief funding on Safe Haven, the selected recognised-autonomy stance on Northern Air Shield, and protection funding on Recovery. At the parent's explicit request, only these three predicates were wrapped in English custom_trigger_tooltip labels in usa_module.py. Removing the presentation wrappers reproduces the exact previous Boolean AST for all three. No condition was hidden or loosened. The parent owns final regeneration/manifest refresh after this source correction.

Final US source SHA256: `41c56a4c27e30a7b668c36bba6adb464c662ede5220aaec8bd9708409aa1bc5b`.

Twenty-one new US emitted-AST scenarios and all seventeen previous US transaction scenarios pass after that correction. New native event/decision references resolve. The current stance remains reversible through paid accepted offers, with no automatic war, forced unconsenting autonomy, geographic air ban or repeated initial assets.

## Boundaries

This pass did not observe native game hovers, the final camera/connector view, loading an old save in HOI4, combat or multiplayer synchronization. The parent is separately handling fresh rendered geometry, browser interaction and the final native engine probe. Those results must be reported separately; parser/source checks and old engine observations do not establish the newly revised tooltip or multiplayer behavior.
