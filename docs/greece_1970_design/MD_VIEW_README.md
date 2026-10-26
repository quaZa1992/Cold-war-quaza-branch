# Greece 1970 focus-tree preview

Runtime implementation now lives in `tools/greece_1970/compile.py` and
`common/national_focus/COLDWAR_GRE_1970_focus.txt`. The 313-focus snapshot and
this preview remain the original design reference. See
`tools/greece_1970/README.md` and `tools/greece_1970/validation.json` for installed
behaviour and script validation. The historical design-only statements below
describe what the preview builder itself writes; the runtime is built separately.

`coldwar-greece-md-layout.html` is a self-contained interactive design view generated from `coldwar_greece_1970_design.json`. It preserves all focus coordinates, embeds 24 existing mod textures as WebP data URLs, and does not load external resources.

Run `python docs/greece_1970_design/build_md_view.py` to rebuild it. Run `node docs/greece_1970_design/qa_md_view.cjs` for Chrome checks at 1024, 736, and 360 px. `MD_VIEW_QA.json` records the latest result.

The Opening, Regime Paths, Economy, and Cyprus shortcuts and every section jump land on a readable focus entry at 85% zoom. Pan to inspect the remaining rows; Whole Tree shows every node together. The jump list includes all 17 sections and 313 focuses. Blue dotted edges are observed outcomes, gold dashed edges are revisable postures, and copper dashed edges are permanent exclusions. The opening camera starts at the Greece root at 85%.

The regime section has three pairwise-exclusive entry paths: retain the junta, negotiate a supervised opening, or hand executive power to civilians. These are paths in the focus tree. A later negotiated military exit or removal of the opening's veto feeds the same civilian obligations without requiring the initially excluded civilian entry focus. The military regime is a lasting alternate outcome. A supervised civilian cabinet retains military reserve powers; a free election and ratified parliamentary constitution are separate milestones.

Every regime focus exposes benefits, costs, retained legacies and replacement effects. The civilian route splits between independent investigations and a limited officer retirement settlement, then industrial credit and regional reconstruction. Trials can continue after the election; neither settlement erases serious abuse, evidence or victim claims. Government change does not cure regional inequality, clientelism, politicised command or foreign censure automatically.

Native prerequisite semantics are OR within one `prerequisite` block, AND between blocks. `REGIME_MD_STRUCTURE_REVIEW.json` and `REGIME_MD_EFFECTS_REVIEW.json` record the main Workshop MD comparisons. `REGIME_HISTORY_REVIEW.json` records the historical review.

`proposed_scripted_effects.txt` is a documentation-only draft of NEW Greek cleanup and reconciliation wrappers. It preserves one-time paid/granted flags, removes incompatible ideas, and re-enables only eligible previously funded permanent programmes after a legitimate government return. It never repeats treasury, stability, PP or XP rewards and never resurrects expired timed programmes. Later revisable policies need a current-selection key; the current permanent policy forks use native exclusions. New domestic outcome adapters and Greek idea definitions still require runtime implementation and engine tests. No file here installs a Greek runtime tree.

![Opening view](md-opening.png)

![Regime paths](md-regime-paths.png)

![Civilian settlement and economic alternatives](md-civilian-bottom.png)

![Cyprus section](md-cyprus.png)

![Full-tree overview](md-full-overview.png)

![Complete interface with starting spirits and selected focus details](md-full-ui-opening.png)

