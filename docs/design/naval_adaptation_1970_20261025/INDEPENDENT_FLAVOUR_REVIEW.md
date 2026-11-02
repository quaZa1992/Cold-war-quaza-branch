IMPERIA COLD WAR

# Independent naval flavour and presentation review

25 October 2026. Scope: the 20 USA, 20 Soviet and 15 DDR additions, their actual installed focuses, native idea modifiers and English localisation. This reviewer did not author those profiles. The IRQ/UAE profiles are excluded from the independent prose judgement because this reviewer authored them.

Two text findings were corrected and emitted:

* Soviet `weapon_conversion_packages` originally promised shipboard missile refits, and DDR's equivalent promised fast-boat weapons improvements. Their actual native spirit gives equipment conversion speed +15% and factory output +15% for 730 days. The profiles now use **Arsenal Conversion** and **Military Supply Refits**, with descriptions of wider defence supply, equipment reuse and factory production. No reward was changed. Sources: `tools/naval_adaptation_1970/profiles/SOV.json:24`, `:46`; `profiles/DDR.json:20`, `:37`; native ideas `common/ideas/COLDWAR_NAVY_1970.txt:14` and `:104`.
* The USA Fleet Marine Force description contained an editorial contrast about pretending a Marine Corps still needed founding. Its owner replaced that with normal institutional prose while retaining the existing force's identity.

The corrected profiles preserve national institutions: the Soviet fleet's industrial ministries and naval infantry, the Volksmarine's coastal service and shipbuilding enterprises, and the United States' established Marine force and competing aviation-ship priorities. The descriptions do not promise automatic commissioned ships, allies' access, foreign consent or completed future stealth/composite projects. The donor material-research and sensor rewards are described as technical development rather than as an already completed modern industry.

All 55 installed focus names and descriptions match the current UTF-8 profiles. All 55 titles fit the native 147-pixel caption: maximum USA 119px, SOV 143px, DDR 142px. Measurements use the installed `hoi_16mbs.fnt` advance widths and kerning. All title and description characters, including the DDR place-name umlauts, exist in both installed `hoi_16mbs` and `hoi_18mbs` glyph tables. The localisation uses UTF-8 BOM. The new branches have no party-dependent `allow_branch` hiding their cards. Exact metrics and source hashes are in `INDEPENDENT_FLAVOUR_REVIEW.json`.

## Inspected source reconstructions

The reviewer opened all six installed PNGs: `installed/USA_NAVAL.png`, `USA_NAVAL_WITH_NEIGHBOURS.png`, `SOV_NAVAL.png`, `SOV_NAVAL_WITH_NEIGHBOURS.png`, `DDR_NAVAL.png` and `DDR_NAVAL_WITH_NEIGHBOURS.png`. They use actual installed coordinates, existing art, native titlebars and bitmap fonts. They are **source reconstructions, not live screenshots**; connector routing is approximate.

At full card scale the new captions, titlebars and icons are readable, with no new card or caption overlap visible. The USA continuation from the two existing strategy alternatives remains legible. DDR's two existing predecessors merge below their cards, leaving nearby air content clear. The Soviet root's long parent trunk occupies an empty column between existing naval cards. Existing neighbouring captions that are already truncated are outside this new-profile review.

One presentation limitation remains: in the approximate renderer, the long `surface_ships` connection to `combined_military_defense_industries`, and the coastal connection to `vessel_production`, pass behind icons on the intermediate doctrine/nuclear row. Native engine routing may differ. This is recorded as a live link/hover check or a renderer-routing improvement, not reported as a proven native gameplay defect. No new gameplay or coordinates were changed to correct an unverified rendering approximation.

## Boundaries and provenance

No game was launched and no live hover or multiplayer behaviour was tested for this review. Native effect counts, modifier support, guards, cumulative balance and full-tree collision tests are separate parent-coordinated checks. The two corrected profile title/description pairs are the only additional runtime-source edits made during this prose review; their emitted localisation was installed by the central owner.

The existing HOI4/MD textures and fonts belong to their original providers. This review copied no assets, changed no font and makes no separate ownership or redistribution claim. Historical research and source-access limits remain in `SOV_DDR_RESEARCH.md`, `IRQ_UAE_RESEARCH.md` and the USA profile's source references.
