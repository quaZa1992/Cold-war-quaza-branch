IMPERIA COLD WAR: economic reform UI, sale proceeds and outlook support

The user's screenshot showed a literal `$icw_econ_move_autonomy_tt$` placeholder and gave no useful comparison of reform results. The generated descriptions now include their movement directly and resolve target names and signed modifier differences through scripted localisation. The reform dialog shows current modifiers on the left and the selected reform's target policy, target position, treasury receipt and modifier changes on the right. A reform within the same tier explicitly shows that its policy modifiers do not change yet. Political-power costs, 90-day implementation and the 180-day reform interval are retained.

The dialog remains 680 pixels wide. Its height increases from 640 to 710, while its own host anchor moves from y=205 to y=135, preserving the original bottom edge at y=845. Adjacent native economy controls retain their existing positions and scrolling geometry. Existing artwork, fonts and sprite registrations are preserved; `compile.py --scripts-only` regenerates the twelve dedicated script/UI/localisation outputs without rebuilding textures. Selection effects are hidden from native effect previews and still perform no payment or reform activation.

Privatisation pays a one-time treasury receipt at completion, using the native MD `modify_treasury_effect` helper. The maximum for a full ten-point newly reached market range is 0.5% of the country's native MD GDP. Only the portion above the country's previously reached maximum market position qualifies. A five-point new range therefore pays 0.25%; a fully repeated range pays zero. Other market reforms advance that maximum without paying sale proceeds. Nationalising and selling the same range again cannot create another receipt. This conservative range model approximates newly saleable public holdings; it does not transfer or delete factory buildings.

The receipt is quoted and saved when implementation actually starts. An overlord approval request pays nothing and reserves no proceeds; a valid authorisation starts the applicant's normal transaction. GDP changes during the following 90 days do not revalue an existing receipt. Completion clears the active reform and pending payment, so retries and reloads cannot pay twice. A one-time migration initializes older countries from their current position without resetting an active reform, political-power cost or timer. This is not recurring budget income.

Only the two outer tiers on each side gain native daily outlook support:

| Policy | Native contribution |
| --- | --- |
| Command Economy | Daily Emerging Support +0.02 |
| Central Planning | Daily Emerging Support +0.01 |
| State-Led Development / Mixed / Regulated Market | No added outlook support |
| Liberal Market Economy | Daily Western Support +0.01 |
| Laissez-Faire Economy | Daily Western Support +0.02 |

These are `communism_drift` and `democratic_drift`, respectively, using MD's Emerging and Western outlook mapping. Replacing the economic spirit removes the old contribution; tiers do not stack. No ruling party, election result or government is directly changed. Existing economic modifiers and positive workforce contributions remain as previously approved.

Historical basis and balance choices

[The Bundestag's account of 1957-1961](https://www.bundestag.de/dokumente/textarchiv/wahlperioden-03-199868) records the 1960 decision to privatise Volkswagen and the sale of 60% to private investors, following Preussag's public share issue. [Volkswagen's 1961 annual report](https://www.volkswagen-group.com/en/publications/corporate/annual-report-1961-2279/download?disposition=attachment) records the actual share sale. These precedents make a sale programme available within the Cold War setting rather than tying it to a compulsory later date.

[IMF Occasional Paper 194](https://www.imf.org/external/pubs/nft/op/194/index.htm) treats privatisation as an exchange of assets with uncertain, non-recurring receipts and distinguishes gross sale proceeds from net budget receipts. This supports a finite, one-time settlement rather than a permanent income multiplier. The 0.5% coefficient and the saved range approximation are explicit gameplay choices, not historical estimates.

[The IMF's account of Hungary's New Economic Mechanism](https://www.elibrary.imf.org/display/book/9781557752161/Ch02.xml) describes enterprise autonomy and market-based incentives within continuing socialist ownership and institutions after 1968. This is why intermediate economic arrangements carry no compulsory outlook drift. The modest outer-tier support values are the user's requested RP/balance connection, not a claim that ownership policy automatically determines political allegiance.

Validation

- The existing parser, original-value preservation, native decision costs, transaction/approval, profile, boundary and investment-reader suite passes all 448 checks.
- Eleven new behavioral tests cover every integer position and additional fractional boundaries for all five reforms, exact target/delta selection, localisation closure, delayed and frozen sale receipts, replay, partial ranges, sale reversal, unavailable/concurrent starts, older-save state preservation, applicant-scoped approval and native outlook values.
- Generated-interface compositions use the emitted GUI, native textures and actual bitmap fonts. Representative same-tier, threshold-crossing, planning and market views fit without text overflow. They are QA compositions rather than live screenshots or pointer-hover evidence. The renderer now caches fonts instead of eagerly reloading them for every element.
- `engine_report.json`: all 45 core native checkpoints pass in 168.7 seconds, with no feature diagnostics. They include the original modifier packages, unaffected national balance-of-power systems, payment/replay guards, fixed sale quotes and all four native outlook contributions. The emitted selected-target getter resolves to `Liberal Market Economy` in an actual native log. The core run is paused at startup and uses forced daily-effect calls for the 90/180-day assertions; it is not evidence of natural 90-day calendar progression.
- The first, extended native attempt passed the new cash/outlook checks but crashed at game time `1970.01.01.13`, before its forced new-Soviet-subject approval scenario could finish. `engine_attempt_1.json` and `fresh_crash.json` retain this failure. The private crash records HOI4 1.19.4.0.48d6 and `C0000005`; no economic-feature diagnostic or failed economic assertion preceded it. The last generic messages mention a missing enabled target template. Neither those messages nor unsymbolicated PHYSFS export names establish the cause. The bounded rerun does not resolve, conceal or certify this longer-run failure.
- Native source hashes, the unchanged shared-host GUI hash and final generator/source checks are recorded in `summary.json`. Four trailing spaces in one emitted file were removed after the core test. Its parsed syntax tree is identical to the frozen native source; all other native output hashes remain exact. The scoped Git whitespace check passes.
- Both test runs used frozen script/map snapshots and separate profiles on E:. The user's active game was left untouched, and the user closed it before the probes. The completed core probe was stopped by its own runner. Native pointer interaction, a real save/reload, natural calendar approval delivery in the current build and live multiplayer remain unverified. The wider native log's unrelated diagnostics are not certified by this scoped review.

Provenance

The requested UI and balance changes were authored for IMPERIA COLD WAR. Existing native frames, textures, glyphs and MD currency helpers retain their Paradox Interactive/Millennium Dawn contributor credits; individual original artists and separate redistribution permissions remain unknown where not previously supplied. No artwork is regenerated by this revision. QA image provenance remains in `docs/design/economic_organisation/native_review/NOTICE.md` and `gfx/interface/ICW_economic_organisation/NOTICE.md`. The project marker makes no ownership or licence claim over those assets.
