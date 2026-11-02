IMPERIA COLD WAR

# Economic organisation: implemented compact interface

The economic organisation bar is an independent country variable from -100 to +100. It appears above the tax controls in the scrolling MD economy window. Its seven policy ranges provide alternative economic national spirits. Native national balance-of-power definitions, values, modifiers, decisions and focus content are not rewritten by this feature.

The compact bar opens an economic reform dialog. The same five reforms are also available in the Economic Organisation decision category. Both entry points call the same guarded request/start transaction. Orange left arrows mark planning reforms, while blue right arrows mark market reforms. Both bars render their position marker at 150% scale, with its centre aligned to the actual policy value. The dialog compares current modifiers with the selected reform's exact target and signed changes. Merely selecting a row or opening an effect preview cannot pay for or enact a reform.

The native decision category shows the current policy, reform status, 90-day implementation time and 180-day reform interval in a compact description. It uses MD's existing economic category icon and distinct factory, production agreement, enterprise agreement, investment and international banking icons for its five reforms. Reform descriptions show their direction and movement alongside the existing concrete effect previews. The custom political-power cost defines all three native localisation forms: the normal amount, the red `_blocked` amount and the `_tooltip` cost. This fixes the visible raw cost keys when political power is insufficient.

| Reform | Movement | Political power | Duration |
| --- | ---: | ---: | ---: |
| Expand State Ownership | -10 | 50 | 90 days |
| Introduce Production Targets | -5 | 35 | 90 days |
| Grant Enterprise Autonomy | +5 | 35 | 90 days |
| Privatise State Enterprises | +10 | 50 | 90 days |
| Open International Capital Markets | +15 | 75 | 90 days |

Only one reform or pending approval request may exist at a time. The common cooldown is 180 days from the start, leaving 90 days after a normally completed reform. Political power is charged once when implementation starts. The new position and corresponding policy spirit apply at completion. Repeated clicks or calls cannot restart an active reform or duplicate its effect. Insufficient political power, overshooting either endpoint and the shared cooldown block execution in the actual payment effect as well as in the interface.

## Overlord approval

Independent governments retain the existing direct reform start. Subject governments instead see Request Approval in the economic dialog. The decision-menu route uses the same approval workflow. Submitting a proposal records the selected reform, original economic position, applicant country and its current overlord, then queues a country event for that overlord exactly one day later. It does not charge political power, move the bar or start the reform/cooldown clocks.

The overlord's event previews the requesting country's concrete political-power cost, policy movement and prospective economic spirit. Authorisation rechecks the current subject relationship, original overlord, applicant identity, original economic position, political power, policy bounds, cooldown and Globalisation requirements. If valid, it starts the normal 90-day reform and 180-day start interval, charging the subject once. The authority flag exists only inside this guarded transaction and is cleared afterwards. Declining clears the proposal with no political or economic cost and no cooldown.

Daily reconciliation clears proposals invalidated by a change of overlord, independence, changed economic position or an invalid copied-country receipt. Events with invalid applicants or relationships do not deliver an actionable proposal. Each queued event carries its own local applicant target, allowing multiple subjects to request approval from the same overlord without sharing a global target. Repeated answers cannot charge or start an already resolved proposal again. Political power is not reserved while approval is pending: if the subject spends it meanwhile, approval becomes unavailable and the overlord can decline. Existing active reforms are not retroactively cancelled when diplomatic status changes.

All positive reforms that would enter the Laissez-Faire range require at least 80 current Globalisation. Open International Capital Markets requires 80 even below that range. The condition is checked when proposing and again at actual reform start; subsequent Globalisation changes do not cancel an active reform or force a policy downgrade.

## Policy contributions

Each range is a complete alternative spirit. Its effects add to existing laws, technologies, national content and other MD modifiers; they do not overwrite those contributions. In particular, existing Soviet and East German economic and market-exposure spirits remain additive. These interactions are deliberate and require campaign balance observation.

The full original compact-concept effect package was restored at the user's explicit request. Later construction, office productivity, incoming investment, Globalisation and world-market-exposure contributions are retained. Where an original value and its first implementation differed for the same modifier, the original value takes precedence; these are alternatives, not duplicate bonuses.

| Policy | Restored original effects |
| --- | --- |
| Command Economy | Available Workforce +5%; Production Efficiency Cap +10%; Productivity Growth -20% |
| Central Planning | Available Workforce +3%; Production Efficiency Cap +5%; Productivity Growth -12% |
| State-Led Development | Domestic Investment Money Cost -5%; Civilian Industry Construction Speed +8%; Administration Cost +5% |
| Mixed Economy | Domestic Investment Money Cost -2%; Production Efficiency Growth +3% |
| Regulated Market Economy | Productivity Growth +5%; Office Construction Speed +5%; Administration Cost +5% |
| Liberal Market Economy | Productivity Growth +10%; Incoming Investment Duration -10%; Domestic Investment Money Cost +10% |
| Laissez-Faire Economy | Productivity Growth +15%; Annual Investment Return +1%; Domestic Investment Money Cost +20% |

The frozen numeric acceptance contract is `original_compact_effects.json`, extracted from the original selected compact concept. `pre_restoration_balance.json` preserves the first implementation's numbers. The validator checks every original effect and every retained later enhancement against those independent records.

| Policy and position | Civilian / infrastructure construction | Office construction / productivity | Efficiency cap / growth | Incoming investment cost / duration | Domestic investment money cost | Globalisation equilibrium | World-market exposure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Command Economy, -100 to below -70 | +10% / +15% | -15% / -10% | +10% / -20% | +15% / +15% | -10% | -15 | -25% |
| Central Planning, -70 to below -40 | +7% / +10% | -10% / -7% | +5% / -12% | +10% / +10% | -7% | -10 | -15% |
| State-Led Development, -40 to below -15 | +8% / +5% | -5% / -3% | +2% / -5% | +5% / +5% | -5% | -5 | -5% |
| Mixed Economy, -15 to below +15 | 0 / 0 | 0 / 0 | 0 / +3% | 0 / 0 | -2% | 0 | 0 |
| Regulated Market Economy, +15 to below +40 | 0 / 0 | +5% / +3% | 0 / 0 | -3% / -5% | +4% | +5 | +5% |
| Liberal Market Economy, +40 to below +70 | 0 / 0 | +10% / +7% | 0 / 0 | -7% / -10% | +10% | +10 | +15% |
| Laissez-Faire Economy, +70 to +100 | 0 / 0 | +15% / +10% | 0 / 0 | -10% / -15% | +20% | +15 | +25% |

Globalisation equilibrium is added to the existing modifier sum before its 0 to 100 clamp. The current Globalisation value is preserved when a reform completes. Existing weekly convergence and its growth and investment-return readers continue to operate. The restored direct growth and ROI contributions now also apply, as explicitly requested.

Available Workforce uses the existing `total_workforce_modifier` reader: population times the MD workforce base of 0.6, multiplied by the clamped sum of participation modifiers. With no other modifiers, +5% means 63% of the population in the workforce, and +3% means 61.8%; it does not create population or add five percentage points of total population. Existing participation caps remain in force. Leaving a planning tier removes its contribution through the normal policy-spirit replacement.

Relative Productivity Growth uses `country_productivity_growth_modifier`, distinct from the later production efficiency growth modifiers retained on the planning side. It scales MD's existing productivity-growth calculation rather than adding a flat monthly growth amount. Annual Investment Return uses `return_on_investment_modifier = 0.01`, adding one percentage point before the existing ROI cap. Administration Cost uses `bureaucracy_cost_multiplier_modifier`. The prototype's State Programme Cost is implemented through the existing domestic investment money-cost reader, not as a multiplier on every government expense.

All percentage modifiers use the native `%` notation in the economic panel and bar tooltips. Production Efficiency Cap therefore displays +10%, +5% or +2%, and Annual Investment Return displays +1%, matching native effect presentation. The former `pp` display suffix was removed at the user's request to avoid confusion with political power. Only the display unit changed; the underlying additive modifier values and calculations remain as recorded above.

Market exposure uses the existing `mdcw_cw_market_exposure` reader in the Cold War world-market system. It affects favourable and unfavourable world-market conditions, not the probability of recession. Office productivity uses `offices_productivity`, which already contributes to office tax receipts and office GDP with different formulas. It is not a national GDP percentage.

The shared incoming-investment duration reader previously treated both signs as a construction-speed increase. The bounded integration changes it to multiply calculated days by `clamp(1 + combined duration modifier, 0.1, 10)`, with a minimum of one day. Positive duration now slows completion and negative duration accelerates it. This correction also affects pre-existing duration modifiers, including bilateral reductions; it is the only non-GUI shared runtime calculation changed here.

## Initialization and persistence

Every existing country initializes once on startup. The weekly country hook also initializes newly created countries or an older save whose startup hook was not rerun. The initialized flag prevents a saved position or active reform from resetting. Reinitialization refreshes only the cached needle coordinate, preserving position and reform clocks when an older save still contains the smaller marker offset. Positions, pending position, remaining days and cooldown use normal saved country variables and flags.

Before 1992, the initial institutional profiles in `tools/economic_organisation/catalogue.py` assign representative Cold War positions. China uses a distinct profile from 1979. Countries without a listed profile, newly released tags and later scenarios start at Mixed Economy. These positions are campaign calibration, not measured historical indices or a complete classification of every country's institutions. Profiles do not force a government or party. The two outer planning tiers now add +0.01/+0.02 Daily Emerging Support, and the outer market tiers add +0.01/+0.02 Daily Western Support. Intermediate tiers have no added outlook contribution. AI countries retain their initial profile because autonomous reform selection is deliberately disabled for this RP feature.

Privatisation now pays at completion for a newly reached market range, up to 0.5% of native MD GDP for ten points. The amount is frozen at actual reform start and cannot be claimed again by reversing and repeating the same range. This is a one-time asset-sale receipt through MD's treasury helper. See `docs/audits/economic_reforms_ui_20261027/REPORT.md` for the exact policy, migration, historical sources and verification.

## Files and reproducibility

The policy catalogue and compiler live in `tools/economic_organisation/`. Run `python tools/economic_organisation/compile.py --scripts-only` from the repository root to regenerate the twelve dedicated runtime files while preserving artwork, or omit the flag when intentionally rebuilding the native interface assets. The compiler preserves unrelated source text and applies the two bounded shared-file integrations idempotently. `implementation_manifest.json` records generated paths and hashes. `economy_layout_moves.json` records all four adjacent content windows moved together and the new scrolling content height.

Shared integration touches `interface/MD_countryeconomyview.gui` and `common/scripted_effects/99_investment_scripted_effects.txt`. All feature IDs use the `icw_econ_` prefix; the investment helper uses `icw_investment_duration_factor`. Script files use UTF-8 without BOM, while the English localisation uses UTF-8 with BOM.

The additional funded decision families in the earlier concept remain future design options. The planning spirits now include their original workforce participation contribution. The implementation does not create population, buildings or state slots and does not change inflation or national focus rewards.

## Validation and remaining limits

The current decision-presentation revision passes 448 static and transaction-model checks, including the native cost-localisation contract and decision icon registration and dimensions. Native-font layout renders cover both normal and blocked costs and show no text overlaps or overflows. Only the decision category, individual decision icons and English localisation changed in the runtime files for this revision; payment, approval, policy values, clocks, GUI bars and shared integrations retain their previous bytes. Regeneration reproduces all 21 compared runtime, shared integration and texture files byte for byte.

The earlier native engine probe passed 42 checkpoints with no errors naming this feature. It predates this presentation revision and the saved-marker cache migration described above, and was not repeated for the text and icon changes. The broader working checkout still reports unrelated errors; this is not a clean bill of health for the entire mod. See `verification_summary.json`, `validation_report.json`, `engine_report.json` and `native_review/layout_report.json` for scope and evidence.

`python tools/economic_organisation/validate.py` checks the emitted scripts, transaction guards, duplicate calls, 89/90/180-day boundaries, policy boundaries, initialization profiles, preview non-mutation, encoding, complete host-container positions and texture decoding. Its interrupted-state continuation check is a model of persisted state, not a real game save/reload.

`python tools/economic_organisation/render_preview.py` renders the emitted GUI and the native decision category with installed native fonts and textures and checks text fit. Decision review images use PP in place of the inline political-power glyph. Outputs in `native_review/` are layout renders, not game screenshots.

`python tools/economic_organisation/engine_probe.py` launches an isolated native game profile and temporary startup assertions. The user's launcher profile, saves and playset are not used. It tests actual reform transactions, policy boundaries, duration signs, positive GDP, every original compact effect package, workforce increases and removal, relative productivity growth, annual ROI and the active Soviet, West German and East German BoP before and after policy changes. The subject test additionally runs the real game clock: a request at 12:00 on 1 January reaches its overlord at 12:00 on 2 January, starts the approved reform with one subject payment, and passes a decline/repeated-answer check on 3 January. A fixture copy adds only diagnostic observations to the shipped approval events; its triggers, option effects and one-day dispatch use the production implementation. See `engine_report.json` for the actual result. Pointer interaction and a real save/reload remain outside this automated probe's coverage.

The duration probe supplies a controlled positive local construction modifier. The original Cuban base construction reader otherwise reached its existing nonpositive-speed, one-day fallback, making duration differences unobservable. With positive construction, baseline duration was 1,153 days, a +0.2 duration contribution produced 1,280 days and -0.2 produced 1,026 days. These are controlled probe values with Cuba's other modifiers included, not advertised universal project durations. The native test process is terminated by its own helper after the COMPLETE marker; the recorded process return code is not a normal player-session exit status.

## Historical rationale and provenance

The precedents and primary historical sources are recorded in `ECONOMIC_POLICY_BALANCE_2026_10_23.md`: Soviet extensive mobilization and later efficiency limits, Korean directed industrial credit and infrastructure alongside financing costs, Chinese enterprise incentives and opening, and Hungarian decentralization within socialist ownership. These support institutional trade-offs. The signed modifier percentages, tier boundaries, reform costs and initial positions are original game-balance choices rather than figures derived from those sources.

Implementation reference: the installed Paradox engine effect, trigger, modifier and variable documentation in `E:/SteamLibrary/steamapps/common/Hearts of Iron IV/documentation/`, plus the existing MD economy, investment, Globalisation and Cold War world-market readers in this checkout. Underlying engine and MD authorship remains with Paradox Interactive and Millennium Dawn contributors. Individual upstream authors and separate redistribution permissions are unknown here.

The economic organisation code, policy catalogue, procedural controls and QA tools were authored by OpenAI Codex for Enes. Native bar textures are resized derivatives of installed Paradox BoP textures. Frame, needle and splitter registrations reuse installed game assets. Detailed asset credits, modifications and unknown permissions are recorded in `gfx/interface/ICW_economic_organisation/NOTICE.md`; native review images have their own companion notice. No new project-wide licence is asserted.

Decision icons reuse the existing sprites in `interface/MD_decisions.gfx`: `GFX_decision_economy`, `GFX_decision_generic_factory`, `GFX_decision_eng_trade_unions_support`, `GFX_decision_attract_foreign_investor`, `GFX_decision_gre_investment_decisions` and `GFX_decision_international_bankers`. Their original source is the existing MD decision artwork in this checkout. Original credit belongs to Millennium Dawn contributors and any underlying Paradox artwork; individual artists, applicable separate licences and redistribution permissions are unknown here. No icon texture is copied or modified. The category and row layout is reused from the complete `interface/countrydecisionview.gui` donor, including the name, cost, tracking and selection fields. The `_blocked` and `_tooltip` contract follows the existing native MD `cost_0_01` definitions in `localisation/english/MD_decisions_l_english.yml`.
