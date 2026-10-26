# UAE fishing, pearling and visible focus rewards

Historical review snapshot: the subsequent user-authorized revision removes all focus Treasury prerequisites, adds social-cost relief and scales coastal benefits with delivered oil expansion. Current behavior is recorded in [the maritime/oil revision review](../../../audits/COLDWAR_UAE_MARITIME_OIL_REVIEW.md) and `tools/uae_1970/README.md`. The earlier affordability and unscaled-positive-benefit conclusions below are superseded.

Independently reviewed on 19 October 2026. **No material open finding.** The current build retains 110 focuses, 98 relative anchors and twelve groups; it adds the eighth starting spirit and repurposes two existing commerce nodes without moving any card.

## Historical framing

The starting description presents inherited seafaring skills, fishing households and maritime trade after the decline of large-scale pearling. It does not present January 1970 as a continuing pearl-export boom. Abu Dhabi's Department of Culture and Tourism describes the industry's flourishing period as lasting until the 1930s in its [2019 Marawah pearl discovery release](https://dct.gov.ae/en/media.centre/news/abu.dhabi.pearl.the.worlds.oldest.known.natural.pearl.discovered.on.marawah.island..aspx). That page's indexed official text was available; direct fetching timed out during review.

The UAE Ministry of Culture's [Museums Guidebook, PDF page 37](https://moc.gov.ae/wp-content/uploads/2026/05/UAEMuseums_ENG-low.pdf) documents Sharjah Maritime Museum's wooden dhows, pearl-diving and fishing tools, navigation and coastal craftsmanship. The [official Sharjah tourism museum page](https://www.visitsharjah.com/activities/family/sharjah-maritime-museum/) also identifies fishing, pearling and trading as distinct parts of the coast's heritage. These institutional descriptions support the qualitative setting, rather than a numerical estimate of the 1970 economy.

A contemporary [Trucial States development fisheries report held by Exeter's Digital Archive of the Middle East](https://humanities-collections.exeter.ac.uk/dame/files/original/f0f7b43183694bfdadba9407357026ed9ad32213.pdf) discusses 1969–70 fisheries investigations, ice factories, cold stores and insulated transport. Its indexed text supports the harbour-and-storage policy theme; the scanned PDF did not expose extractable text through the review tool. No fish-stock or output estimate from it is used as a game balance claim. The [British Library's archival account of the pearl trade](https://www.qdl.qa/en/pearl-diving-inside-trade-shaped-gulf) separately documents the earlier hazardous work, merchant finance and debt relationships; these are historical background, not a claim that every 1970 fishing household retained the old diving contract system.

## Starting spirit and two existing focuses

| Content | Current numeric effect |
|---|---|
| Pearls, Fishing and Dhows, starting spirit | Agriculture productivity +10%; office productivity +3%; country productivity growth modifier −5% |
| Pearls and Fishing, existing `trading_coast` at (35,9) | $0.10 billion; agriculture productivity +10%; existing office productivity +6% |
| Fishing Harbours, existing `port_planning` at (35,10) | $0.15 billion; agriculture productivity +10%; energy use +2%; existing naval-base construction +15% and bureaucracy cost +3%; clears the starting spirit's −5% growth component |

The harbour remedy changes only that spirit's negative component to zero. Its useful agriculture/office contributions remain, so the whole spirit is not falsely advertised as removed. Other programmes' productivity penalties are independent. The registered native `agricolture_productivity_modifier` represents the primary-sector benefit within MD's available economy model; the numerical amounts are roleplay balance, not historical fishing statistics.

The emitted dynamic modifier has all three real variable consumers and a real installation provider. Its label and English narrative equal the current revision. The original seven starting-spirit payloads remain unchanged.

## Native artwork and layout

The exact native source is `GFX_idea_maritime_industry`, registered at `interface/MD_ideas.gfx:6050`, pointing to `gfx/interface/ideas/internal_factions/maritime_industry.dds`. The emitted `GFX_idea_COLDWAR_UAE_maritime_livelihoods` alias and dynamic-modifier icon resolve to that same 72×64 national-spirit DDS. Its SHA-256 is `6d8f3d27734c1a89f1f1ad9c7c960d89d22660699bbb48df4dd49e8b33aca0de`.

The image was visually inspected: it is a neutral civilian ship on a blue roundel. It is generic maritime artwork, not a claimed picture of pearl divers or a dhow. No dedicated fish/pearl national-spirit sprite was found; country-branded shipping badges, warship art and a crowded migrant-boat icon were rejected. The proof `MARITIME_SPIRIT_ART.png` displays the original native pixels and a labelled enlargement. No focus icon was substituted for the national-spirit artwork.

The reviewer opened the final commerce branch, full overview and spirit proof. Both renamed focus titles fit the unchanged native 147-pixel field. All 110 positions, prerequisites, exclusions, durations, focus textures and neighbours match the current revision; zero unrelated card/connector intersections are found. The external proofs use native icon/titlebar/font pixels, while lines and unavailable shading remain labelled approximations.

## Prospective reward tooltips

The previous outer `if` made programme numbers disappear when a player hovered a currently unavailable government or status route. Advertised numeric programme rewards now remain visible regardless of the current qualifying government/status. This changes presentation, while the actual live activation and transaction conditions remain in the guarded providers and programme descriptions.

Genuinely future agreement rewards use the existing native `TT_IF_THEY_ACCEPT` heading. The checker requires this heading for the relevant agreement contributions rather than treating them as unconditional grants. Current earned spirit relief and political/population caps still display marginal amounts instead of an overstated nominal benefit.

The independent emitted-preview arithmetic passes **1,980 contexts**, including false government/status predicates, accepted and unaccepted terms, earned relief, capped contributions and changed state control. Every expected numeric row and treasury debit is present and matches the current design. The existing 36 opening-gate and 60 office-preview checks remain clean. Current population contributions are +160% on the citizen-housing route and +200% on the workforce-housing route, with a +200% tree cap; these modify growth rate, not population by that percentage each month.

Current focus source SHA-256: `7fabc035c60384bcc1b9a051729153b473a2a7e2665aa500ee5bc9c0aa2a412a`. Current presentation source SHA-256: `5a049675ef38352f927f37cd255e5291489aeec46497ae84b45faa3e9436de44`. `LAYOUT_REVIEW.json` and `FOCUS_MANIFEST.json` contain the complete current hashes, emitted source lines and geometry. The original approval snapshot remains unchanged.

## Limits

This review establishes source, arithmetic, native-art and externally rendered card consistency. It does not establish actual HOI4 hover rendering, startup GDP, live fishing-output simulation, growth over time, multiplayer behaviour or progressed-save compatibility. No game code or native texture was edited by the independent reviewer during this task.
