IMPERIA COLD WAR

# West Germany and East Germany reward revision

The revision improves 103 existing focus programmes: 54 in West Germany and 49 in East Germany. Important policy choices now award concrete industrial, research, energy and military packages with current-GDP costs, sector-specific benefits and relevant disadvantages. The 417-focus GER tree and 836-focus DDR tree retain their IDs, positions, durations, prerequisites and mutual exclusions.

The complete numerical packages are recorded in [GER_CHANGES.json](GER_CHANGES.json) and [CHANGES.json](CHANGES.json). [Historical and MD references](HISTORICAL_AND_MD_REFERENCES.md) distinguish historical precedents, installed mechanic examples and balance proposals. Values are game balance choices rather than estimates of historical policy effects.

## West Germany

The [GER review](GER_REVIEW.md) lists all 54 packages and compatible route totals. Examples include:

- The social-market programme adds two civilian factories, industrial research support and improvements to the existing economic programme for 0.2% of current GDP. Social and institutional programmes add offices, industrial capacity and finite research support appropriate to their purposes.
- Stimulus and austerity retain their mutually exclusive fiscal policies. Stimulus funds a larger demand and investment package with its existing debt burden; austerity offers a smaller investment package, fiscal relief and the original growth trade-off.
- Nuclear expansion creates two reactors for 0.5% of current GDP. Fast-breeder investment and a nuclear moratorium lead to different reactor or renewable assets and energy trade-offs. Coal support expands generation while increasing fuel consumption. The existing nuclear opposition and political consequences remain.
- Microelectronics adds an actual microchip plant with finite electronics, computing and chip research support. The programme requires the installed chip technology and sufficient researched state capacity.
- Military programmes combine arms factories, dockyards, radar or air-base projects with finite research and actual equipment-family production-cost reductions. Tornado uses the active medium-plane airframe family; submarines, frigates, armour, artillery and air defence use their corresponding native families. Existing output and readiness benefits remain. W15 and W18 retain their exclusive service models.

The Energy Mix core now connects its percentage previews to MD's percentage fossil-fuel consumption and nuclear-generation modifiers. Previously those variables were connected to flat consumption and generation values. Original Patriot and NATO AWACS construction rewards also receive the required shared slots before their radar, air-defence and air-base levels.

## East Germany

The [DDR review](DDR_REVIEW.md) lists 31 policy, military, research or doctrine improvements and 18 paid asset programmes. The 18 prices include both retained project fees and new investment, avoiding a separate legacy charge.

- The Kombinat programme delivers four civilian factories in Saxony for 3.2% of GDP, with an additional 5% civilian productivity and 3% maximum production efficiency. Its additional 3% corruption cost represents greater managerial discretion.
- The housing programme delivers two civilian factories and four infrastructure levels distributed across four regions, for 3.1% of GDP. It reduces consumer-goods pressure by 2 percentage points while raising social spending costs by 3%, alongside retained infrastructure and stability rewards.
- The microelectronics resolution delivers two chip plants in Saxony, additional limited research support and research-speed improvement for 2.22% of GDP. Retained chip productivity and consumer-goods pressure remain. Both plants must fit the actual researched technology tier.
- Lignite expansion delivers two fossil plants for 1.35% of GDP. Greifswald offers two reactors for 2.96%, gated by reactor technology. The Green League alternative offers two renewable levels for 2.71%, health-cost relief and retained conservation benefits, with slower production-efficiency growth.
- Agricultural, Christian-social, guild-economy and defence-first programmes offer distinct farm, civilian or military capacity rather than identical generic bonuses. The Suhl arsenal delivers four arms factories. Specialised military research and production discounts cover the relevant equipment families.

Honecker's compatible housing and infrastructure programmes distribute their upgrades across six states. Berlin's starting infrastructure and the native cap no longer make a later programme impossible. The Ulbricht and Schkopau refinery allocations likewise account for cumulative state capacity and researched refinery tiers.

## Integration and safeguards

Paid packages show their prospective concrete effects even when locked. At execution, the complete package rechecks country/scenario routing, original political requirements, positive GDP, ownership, control, native capacity and relevant technology. Each building level receives a shared slot first. A permanent receipt prevents a second asset grant or payment. Cash balance is not an additional availability requirement; MD financing remains available.

New static supplements have their own country, original policy-requirement and receipt guards. Capital investments and established institutions are durable outcomes. Existing party-programme activation, leadership, security, diplomacy and succession systems remain responsible for their own lifecycles. No new workforce-size penalty, automatic uranium production, nuclear stockpile, recurring monetary stream or recurring country scan is introduced by the reward overlay.

Canonical sources are `tools/west_germany_1970/reward_overlay.py` and `Claude outputs/COLDWAR_DDR_generator/design/ddr_reward_overlay_20261027.json`. The bounded writers are `tools/west_germany_1970/install_reward_overlay.py` and `tools/focus_quality_20261020/apply_ddr_reward_overlay.py`. They avoid rebuilding the legacy DDR generator, which contains only 821 focuses and would omit the current naval extension.

Final loading repairs emit the existing Mannheim anchor before its LaFontaine dependent, write the DDR naval shortcut factor as `0.8` instead of the native-parser-invalid `.8`, and remove five unresolved retired-modifier removal calls while preserving the one-time retired-score cleanup. New DDR research and doctrine awards use distinct localised names so that they do not replace retained research pools.

A concurrent building-grant integration also changes 29 other DDR reward nodes and emits five shared `COLDWAR_GRANT` dependencies. Those changes are separate from the 103 programme improvements. Their current emitted files are included in source hashes and the native fixture because the DDR writer uses that integration. They are preserved rather than attributed to this reward revision.

## Review evidence

The final checks passed: 37 targeted native assertions, 49 existing source-model regressions, source/reference/encoding checks, and byte-identical bounded rebuilds. All 1,253 existing focus IDs and their graphs remain intact. [REGRESSIONS.json](REGRESSIONS.json) contains the complete four regression-suite outputs.

[INDEPENDENT_REVIEW.md](INDEPENDENT_REVIEW.md) records the content review and its resolved findings. [SOURCE_CHECKS.json](SOURCE_CHECKS.json), [ENGINE_REPORT.json](ENGINE_REPORT.json), [REBUILD.json](REBUILD.json) and [FINAL_CHECKS.json](FINAL_CHECKS.json) record the final verification results. The first engine attempt is retained in [ENGINE_ATTEMPT_1.json](ENGINE_ATTEMPT_1.json), including the load errors that prompted the final corrections. [ENGINE_ATTEMPT_2.json](ENGINE_ATTEMPT_2.json) records an intermediate access-violation crash before test execution; the subsequent run used the same runtime hashes and passed all 37 assertions. The crash cause is unestablished.

Native coverage uses four representative complete emitted focus payouts: GER social-market and nuclear construction, DDR lignite and microelectronics. It exercises costs, assets, real missing technologies, researched-tier limits, zero GDP, lost capacity and repeated execution in a private 1970 single-client fixture. Its temporary history, state and party setup is confined to the private test profile. It is not a full campaign, mouse-hover, save/rehost or multiplayer/OOS test.

Source-derived [BRD energy](GER_energy.png), [BRD economy](GER_economy.png), [DDR economic reform](DDR_economic_reform.png) and [DDR energy](DDR_energy.png) views show current focus geometry and native artwork. Full overviews are also included. [PREVIEWS.json](PREVIEWS.json) and [PREVIEW_NOTICE.md](PREVIEW_NOTICE.md) describe rendering approximations and provenance. The source-derived views are not engine screenshots.

Private backups, game profiles and raw native logs are stored under `E:/HOI4_Mod_Tools/mdcoldwar/runtime/german_reward_revision_20261027`, outside the mod. No commit or push is performed by this task.
