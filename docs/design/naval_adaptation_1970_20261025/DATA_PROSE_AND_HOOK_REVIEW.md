IMPERIA COLD WAR

# Independent data, prose, owner-hook and coastal-view review

25 October 2026. The bounded review passes. Native game, multiplayer and actual engine connector routing remain untested. Exact current hashes and structured results are recorded in [DATA_PROSE_AND_HOOK_REVIEW.json](DATA_PROSE_AND_HOOK_REVIEW.json).

The independent editorial scope is USA, IRQ and UAE. This reviewer originally authored the SOV/DDR profiles and does not claim independent editorial signoff of those two. Technical ID, caption, integration and provider checks cover all five countries.

## Data and prose

All 85 new focus IDs and their parent/exclusion routes resolve: 20 each for USA/SOV and 15 each for DDR/IRQ/UAE. The active local generic source has a different whole-file hash from upstream MD 2.0.2, but all twenty naval donor focuses were independently compared and have identical parsed semantics.

Current native bitmap title maxima are USA 119, IRQ 144, UAE 143, SOV 143 and DDR 142 pixels, against the 147-pixel limit. Five overlong IRQ/UAE captions were corrected through the authorised profile edits. Existing long legacy captions elsewhere in the older trees are outside this new-caption claim.

Three USA descriptions now use positive institutional prose about materials laboratories, Fleet Marine Force integration and sensor trials. They no longer explain the adaptation's avoidance of future technologies or pretend that establishing an existing Marine Corps is the player's task. IRQ/UAE sensor captions and descriptions now match the actual electronics coupons; they no longer promise direct mine-system research from `CAT_naval_electronics`. The narrow changes are fully listed in the JSON. No ID, prerequisite, effect, cost or country-generator code was changed by these prose edits.

The country identities remain appropriate: the United States develops its established oceanic fleet; Iraq expands coastal institutions serving Basrah/Umm Qasr; the UAE profile names the existing Abu Dhabi Sea Wing and voluntary cooperation between separate emirate establishments. It does not assume a unified federal navy in January 1970. The content adds no leadership changes, automatic foreign access, ship formations or future special-project completions.

## Prices and the inherited UAE deficit rule

The emitted blue-water invoice is $0.5 billion per port level and $7.5 billion per yard level; the two-yard package costs $15 billion. Coastal invoices are 0.2% of annual GDP per port level and 0.8% per yard. The combined-industry focus retains the donor's capacity-guarded free arms factory. The repair idea lasts 365 days; conversion and concentrated vessel production last 730 days. The reviewed descriptions do not claim contradictory prices or permanent versions of those temporary programmes.

The pre-existing UAE focus policy explicitly permits deficit financing. The final adapter therefore removes Treasury coverage only when `country == UAE` and `allow_deficit` is the actual boolean `true`. It still requires a positive quotation/GDP, rejects `MD_skip_treasury_cost`, checks actual ownership/control and port-province control, checks native capacity, and charges the whole invoice once. Other twelve paid projects in USA, SOV, DDR and IRQ retain their funding guards.

The final emitted asset and lifecycle suites passed independently: 16 asset tests and 14 actual-runtime lifecycle tests, with writes blocked. Three additional actual UAE helper cases began at Treasury -3, waited without charging while control was lost, and completed after control returned and GDP rose from 100 to 200. The port charged 0.400 and ended at -3.400; each yard project charged 1.600 and ended at -4.600. Repeated completion and pending retries made no further delivery. All fifteen new UAE availability and real ready helpers were independently checked for direct and transitive Treasury vetoes: none remain. No free cash or waived invoice was introduced.

## Reproducible owner retention

[test_owner_hooks.py](../../../tools/naval_adaptation_1970/test_owner_hooks.py) passes five checks. Run `python -B tools/naval_adaptation_1970/test_owner_hooks.py` from the repository root.

The SOV and DDR tests use fresh isolated processes, block filesystem mutation APIs and execute only `cw_focus.focus_file()` or `dg_focus.focus_file()`. Neither broad build module is imported. An observer captures each emitter's original string before the naval hook. Every original focus block remains byte-identical; removing exactly one marked naval block restores the complete original parsed tree semantics. The hook adds twenty/fifteen focuses and remains idempotent.

The tests also verify the real IRQ/UAE focus-emission calls, the `parents[2] / tools` paths and the final runtime dictionary update in all four legacy owners. SOV's runtime package is inserted after its variable-hiding/name pass; DDR's follows its quality runtime package; IRQ's follows decision streamlining; UAE's follows its constituent modules. Later normal writes cannot replace the naval runtime with an earlier transformed copy. Seven owner Python files parse, all five current trees reintegrate byte-identically, and all five runtime outputs equal fresh canonical text. The native compatibility normalizer leaves those outputs unchanged. No broad country builder was run for this review.

## IRQ/UAE source-composite inspection

The four inspected files are the IRQ/UAE `*_NAVAL.png` and `*_NAVAL_WITH_NEIGHBOURS.png` views under [installed](installed/NOTICE.md). Each shows fifteen visible new cards with readable titles and registered artwork. No new card, title or icon overlap was observed. Iraq attaches to the existing maintenance institution, displayed as The Coastal Fleet. The UAE attaches to A Defence Staff and retains its existing political and military branch choices.

The compositor has known routing ambiguities. The UAE attachment from (15,22) to (22,26) uses a midpoint route through the goal of A Sustainable Force at (15,24). Its approximate pixel path is (1520,2924), (1520,3152), (2192,3152), (2192,3380). Both coastal views also route Surface Ships to Vessel Production at midpoint y3672 through the doctrine-innovation goal at row 28. These are visible source-preview ambiguities, not demonstrated native-engine geometry defects. They do not justify introducing another gameplay prerequisite or changing approved coordinates on their own.

Current IRQ/UAE title, icon, resolved coordinate, parent, exclusion and anchor metadata was independently compared with the rendered evidence. Final `LAYOUT_EVIDENCE.json` now matches all five current tree hashes. The latest eligibility and deficit changes did not alter that visual data. The images use installed assets and bitmap fonts, while locked-state styling and connector bends remain approximations.

In total, this reviewer executed 38 bounded cases: five owner-hook tests, sixteen asset tests, fourteen runtime lifecycle tests and three additional UAE pending/GDP/replay cases. Coordinator validation totals are not included in that number. These checks do not emulate battles, the native economy's debt tick, live GUI clipping, save loading or multiplayer synchronisation.
