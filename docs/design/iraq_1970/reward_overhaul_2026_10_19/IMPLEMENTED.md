# Iraqi direct focus rewards — installed revision

19 October 2026. Installed `direct_rewards_2026_10_19_v3`, manifest SHA256 `9849fa40ed152295a6d84016ed8e2335fdf72112d63fe4037aeec68779bae1af`. This supersedes the previous reward-diversity proposal as the actual implementation. All410 playable focuses are covered. The16 hidden compatibility entries retain their IDs. All410 focus coordinates, grouped prerequisites and exclusions remain unchanged.

## Material changes

The source comparison used original main MD `05_iraq.txt`, `05_russia.txt` and `05_iran.txt`, with called ideas/effects and period-appropriate technology consumers. The independent benchmark catalogue and final installed review are in `MD_REFERENCE_REVIEW.md`. The actual names, prices, durations and final reward operands for every focus are in `ALL_FOCUS_REWARDS.md`.

| Reward coverage | Before | Installed |
|---|---:|---:|
| Active focuses |410|410|
| Focuses with a positive bureaucracy-cost contribution |140|48|
| Focuses with any bureaucracy contribution |150|62|
| Focuses with any stability contribution |122|18|
| Focuses with physical building deliveries |23|36|
| Limited research/doctrine instruction pools |11|35|

All active focuses have a direct reward. Permanent construction, finite research/doctrine, service-specific training, literacy, a real corruption-law step, sector productivity/tax channels, operating costs, resource income and military capabilities replace much of the former administrative repetition. All410 English descriptions were rewritten as Iraqi country narrative. Normal focus completion shows native numeric effects, costs and actual spirit changes. Flat daily political power and equipment-design XP costs have correctly typed country-local tooltip formatters; false treaty conditions no longer hide all prospective numbers.

The choice between Professional Core and Mass Reserve Army remains substantive: professional organisation+8%/25XP with personnel expense+6%, versus recruitable-population factor+15%/recovery+8%/25XP with organisation−3%. Heavy Industry delivers a civilian factory, production-efficiency cap+10%, military output+5% and one35% industry instruction, with consumer-goods factor+2%; Consumer Expansion delivers its own civilian factory, construction+8% and civilian productivity+8%. Political programmes use different sector and institutional outcomes, with route sums in `POLITICAL_ROUTE_TOTALS.json`.

No new focus-reward decision menu was added. The existing78 focuses with84 decision-unlock entries are retained for actual offers, political settlements, optional policy revisions and operational choices. Their completion now carries a direct reward; this implementation does **not** claim that those existing decisions were deleted or that their unlock count fell. Recipient consent, elections, succession, Gulf borrowing and the Iran/Kuwait/US intervention contracts remain real. The existing seven starting burdens and their reform/cleanup rules remain.

## Save and funding integration

The new source files are `tools/iraq_1970/reward_overhaul_economy.json`, `reward_overhaul_politics.json` and `reward_overhaul.py`; compiler, runtime initialization and presentation integrate them. The immutable approved concept is unchanged. The old v2 migration is deliberately emitted from the old design, with a distinct v3 entitlement/receipt layer. Old unfunded work must finish before a later expansion; actual deliveries are credited, and only a positive GDP-price increment creates a supplementary quote. The old programme remains until that outstanding expansion is financed. A research course is credited by category/use count instead of being recreated because its name/percentage changed. Old quotes retain their historical basis. Reconciliation does not deliver buildings, money, courses or law steps.

Every physical component checks actual Iraqi ownership/control and remaining native building capacity before payment. No secretly priced random-building/office helper is wrapped inside a second invoice. Durable assets remain after government change; political programmes deactivate and return with their real government/leader/selected-policy/contract gates. The90-day oil-nationalisation marketing cost is retained and does not restart for an old completed nationalisation.

## Verification

- Static installed validation:104 generated files, all original USA focuses preserved,410 resolved Iraqi positions,13,437 scripted calls resolved, zero missing package references. The independent reviewer additionally matched all104 generated files and9 scoped adapters against the final manifest and all410 emitted descriptions against final source.
- Current direct-reward AST checks:12 cases plus a separate native corruption-law transaction. This includes all36 building-bearing nodes under lost ownership/control/capacity, price freeze, old receipts, no replay, one-time research/XP and party/leader cleanup. These execute emitted logic at explicit native boundaries, rather than simulating warfare or the economy.
- Existing contracts:22 legacy migration cases,13 graph checks,8 installed core checks,18 political transaction cases,9 starting-spirit cases,6 concession-feasibility cases and35 USA intervention/regression cases pass. The15 earlier reward-data tests continue to check their explicit legacy revision.
- Presentation:9 installed tests pass, including820 focus/queue availability views, all modifier operands/formatters,14 actual starting-spirit preview families, treaty-false numeric previews and English localization.
- The updated installed-source viewer passes17 Chromium interaction checks, including all638 Iraqi/US inspectors, left/middle/right dragging, wheel panning, zoom, minimap and widths320/736/1024. It contains the current emitted source, not the superseded proposal.

The final isolated native HOI4 asset test passed all five expected checkpoints against the unchanged final manifest: one actual civilian factory (state557 level1→2), one actual fossil power plant in state171, exact respective0.5-billion payments at fixture GDP10, and no second payment or construction when the helpers were repeated. No IRQ/USA-package error lines appeared. This deliberately uses synthetic fixture GDP10/treasury1000 before ordinary world simulation; it proves targeted native delivery and charging, not the natural Iraqi starting economy. The process was terminated by its own successful bounded probe. See `tools/iraq_1970/ENGINE_ASSET_REPORT.json` (`success=true`, `manifest_unchanged=true`, elapsed210.6s). The earlier attempt is retained in its attempts history; it passed the asset checkpoints but was invalidated as an exact snapshot by the subsequent tooltip-only recompile.

These checks do not establish complete native focus-hover rendering, research consumption, long-term economic balance, an old-save reload or multiplayer gameplay. Compatible programme totals are reviewed balance choices, not a measured GDP or war forecast.
