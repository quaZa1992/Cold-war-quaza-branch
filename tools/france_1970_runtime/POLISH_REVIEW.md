IMPERIA COLD WAR

# France 1970 polish overlay smoke review

## Frozen input and semantic preservation

- Approved design SHA-256: `4f57a4c6e3d13eba6b7ec4129cb81fd8b9a2a645e9fac10c5ebf8d36588c18b5`.
- Approved gameplay fingerprint before and after `polish_design`: `05dd62c197cae8e2ace7942fe74f115e0f3552ef91a9e40268385f3db5a36c20` (identical).
- Tree remains 152 focuses, 14 programme groups, and 19 offers. No focus is deleted and the gameplay projection confirms rewards, GDP terms, acceptance conditions, prerequisites, exclusions and party activation fields are preserved.

## Native map geometry

- Focus footprint changes from x=4..134, y=0..13 to x=4..103, y=0..13. The 14 section positions are explicit in `polish.py`; UDR and its NATO extension move as one branch, and each group's internal spacing is preserved.
- At the inspected MD card and grid dimensions (165 x 128 px cards, 96 x 130 px stride), a pairwise card-bounds check finds zero focus card overlaps.
- All focus offsets resolve to their intended absolute positions. A root without an anchor now emits its own absolute `[x, y]`; anchored focuses emit their position relative to the anchor.
- This is a coordinate and card-bounds check. Connector routing still needs review against the freshly compiled native preview and ultimately the game renderer.

## Player-facing text and artwork

- The overlay revises 28 short titles and 145 focus descriptions, and supplies programme and bilateral idea descriptions. Existing focus IDs and approved reward data remain unchanged.
- Measured all 152 rendered names in Chrome Canvas at Arial 15 px against the 147 px title width: zero overflow. This is a font-width approximation, not an in-game screenshot measurement.
- The GFX pack registers 81 aliases: 36 native focus textures, 9 small native idea textures and 36 selected/available shine sprites. All referenced DDS files exist in the installed Workshop item. No binary texture assets are copied or modified.
- Long-term programme labels use “Gaullist Government” and “Liberal Republicans”; dated party names in shortcuts remain delegated to the native party registry. The UDR programme uses the French Republic emblem; the overlay avoids later RPR/UMP branding. Idea sprites resolve to small `gfx/interface/ideas` textures rather than focus medallions.
- Credit and licence/permission limitations are recorded in `ART_PROVENANCE.md`.

## Build handoff

`polish_design(design)` returns a polished deep copy. `build_art(design)` returns `design`, UTF-8 `files`, English key/value `loc`, `art_copies` (currently empty), and an `art_notice` provenance record. Files are limited to the generator output map; this module does not write live game files.

## Emitted-file confirmation

The generated files were then read back from the mod tree and checked against the polished design:

- The installed focus script contains 152 focus blocks. Every ID, icon name and resolved position matches the polished design; all root and anchored coordinates resolve with zero mismatches.
- The English YAML contains all 705 expected merged localisation keys with no missing or differing values. It starts with `l_english:` and has the required UTF-8 BOM. The focus script and GFX file are UTF-8 without BOM and begin with the project marker.
- The emitted GFX has 45 basic alias declarations, every focus icon resolves to an alias, and every referenced DDS path exists in the installed MD Workshop checkout.
- Emitted runtime design SHA-256: `907d39b72fd9c17e07a16012317ecfee80aec8e33ac27f8f321581ba9616b5e2`.

The visual viewport, connector routing and in-game tooltip rendering still require the native preview/game checks.


## Native focus shine aliases

The final polish builder copies all 36 matching MD `spriteType` blocks from `interface/goals_shine.gfx` and changes only each registered name to `<project focus icon>_shine`. A block-by-block comparison against the current Workshop source found no other differences. These pairs supply the native selected/available focus button animation. The emitted mod still needs recompilation after this addition; the prior emitted-file hashes above describe the pre-shine build.

The two programme-title refinements do not change the approved gameplay fingerprint; programme idea names become “Gaullist Government Programme” and “Liberal Republicans Programme.”


## Final emitted preview after parent integration

- Final emitted runtime design SHA-256: `28d443626810b606d185f3a094a6bfaf7f5b7ed8b1a3c20f10cd0a1ddeedb7b1`.
- Final installed output is 152 focuses, 14 groups, 19 recipient-approved offers, 739 English localisation keys and 81 GFX sprites (36 basic focus icons, 36 native shine animations and 9 small idea textures).
- The rebuilt interactive fragment embeds 36 current focus DDS textures and both native 164 x 50 titlebars as lossless PNG, without resizing. Its size is 991,393 bytes, below 1 MB.
- Browser QA passed all 152 focus inspections, all 19 bilateral term panels, 42 section-fit views at 320/736/1024 px, party shading, pan/zoom and 147 px Arial title measurement. It found zero broken images, title overflows or runtime failures.
- The preview is a browser rendering of emitted data and native art, not an HOI4 engine screenshot. Screenshots and the machine-readable QA report are under `tools/france_1970_runtime/screenshots` and `PREVIEW_QA.json`.
