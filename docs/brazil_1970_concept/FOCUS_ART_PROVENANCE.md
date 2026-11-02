IMPERIA COLD WAR

# Brazil 1970 focus art polish and provenance

## Scope and result

This pass changes focus icon selections only. The approved 224 focus IDs, English titles, coordinates, prerequisite groups, exclusions, availability, costs, durations and rewards remain untouched. The canonical art selection is `tools/brazil_1970_runtime/focus_art_polish.json`; it maps 185 focus IDs to existing native Millennium Dawn sprite keys, texture paths and short subject rationales. The other 39 focuses keep their approved icon keys.

The original tree uses 23 distinct native icon keys. Applying the map gives 83 distinct symbols in the focus tree, a gain of 60 symbols. The runtime alias set contains 87 keys: all 23 original aliases remain available for the archived approval render, and 64 additional native sources support the polish map. The most reused selected icon is `generic_bank` on eight finance or credit focuses; the next highest frequency is seven. Party identity emblems remain on defining entry focuses while policy cards use relevant institutional, economic and social symbols.

## Native sources and footprint review

The donor registry is the current Millennium Dawn Workshop source `394360/3374271790`, `interface/goals.gfx`, SHA-256 `0c837b6d765252b41ea5de791366afc43658d7706f7b04f4184773d46bc8d341`. Every chosen sprite key and texture path was confirmed in that registry. All selected textures also exist in the target checkout, and each selected DDS compares byte-for-byte with the Workshop source.

The chosen native textures are transparent RGBA focus artwork. Across the retained and selected alias set, source dimensions range from 80 x 72 to 111 x 111 pixels. No selected texture exceeds 120 pixels in either dimension, and no unusually wide source remains in the mapping. `art.py` registers aliases that point to the existing texture paths; it does not resample, crop, recolour or copy the focus textures. The existing shine alias behaviour is retained.

The source-derived contact sheet and the branch review were visually inspected. The contact sheet shows each retained or selected source once at aspect-preserving review scale. The branch review checks the Brazil military programme, PT programme and economic development programme with the chosen icons beside their English focus titles. It groups cards for art review only; it does not reproduce focus-tree positions, connector routing, titlebar states or the live game viewport.

## Files

- `tools/brazil_1970_runtime/focus_art_polish.json`: focus-to-native-icon map with exact source texture and semantic rationale.
- `tools/brazil_1970_runtime/art.py`: validation of mapped IDs and native registry paths; alias registration retains the original icon set and adds only mapped native sources.
- `docs/brazil_1970_concept/FOCUS_ART_CONTACT_SHEET.png`: source texture contact sheet.
- `docs/brazil_1970_concept/FOCUS_ART_BRANCH_REVIEW.png`: static military, PT and economy art composition review.

The mapping does not modify `approved_design.json` or focus gameplay. The core compiler now consumes `focus_icon_overrides` and writes `COLDWAR_BRA_focus_<native_icon>` on each mapped focus.

## Emitted integration verification

I parsed the current emitted focus file and GFX aliases read-only. All 224 focuses use their expected mapped or retained icon. The emitted IDs, English titles, absolute coordinates, prerequisite groups, mutually exclusive links and focus costs match the approved design for all 224 nodes. There are exactly 87 expected native focus sprite aliases and 87 matching shine aliases. Each alias resolves to its declared texture, and every shine uses the same source mask with the native MD shine overlay. All 72 newly selected sprite keys and their DDS bytes match the installed Workshop source.

The final tree contains 83 distinct focus symbols. `compile.py --check` reports `changed: []`, and the approved design hash remains unchanged. These are emitted-source checks, not a live focus-tree screenshot or an icon-hover inspection. The parent-owned 117-assertion native run was still in progress at the time of this record, so this art review does not claim its result.

## Credits and rights

The source is the user's installed Millennium Dawn Workshop content, Workshop item `394360/3374271790`. Existing national-focus icon files were reused through sprite references. The original individual artists or asset authors for the selected textures, and any separate permission or redistribution terms for those individual assets, are unknown in the source records inspected. Existing Millennium Dawn and Paradox rights remain with their respective holders. This project marker does not establish ownership or replace any applicable licence. The PNG inspection sheets are derived review images assembled from the source textures and do not assert ownership of their components.
