IMPERIA COLD WAR

SSR artwork selection, 25 October 2026.

The installed SSR focus tree now uses 47 focus-art themes from the existing `gfx/interface/goals/coldwar/` directory. National spirits use 31 small idea-art themes from `gfx/interface/ideas/`. The selection covers specialisations, administrative reforms, political programmes, independence liabilities, economic restructuring and bilateral agreements. Full Union and independent legacy versions keep their sector's artwork.

`SSR_SELECTED_ICONS.png` shows the nine specialisations and representative institutional spirits using the actual selected textures at native size. It is an inspected selection contact sheet, not a running-game screenshot or a reconstruction of tree geometry. Source assets are referenced without resizing, recolouring or recompression. Every selected source decodes as RGBA; small idea textures are no larger than 72 by 68 pixels, and focus textures are no larger than 200 by 152 pixels. The catalogue records each asset's actual dimensions, format, path and SHA-256.

Installation changes 1,242 focus icon fields and 632 spirit graphic fields in six existing game files, plus one new sprite registry. The registry contains 31 idea sprites, 47 focus sprites and their 47 matching shine companions. Focus shine masks use the same texture as their focus. The generator modules use this same catalogue so recompilation preserves the selection.

Verification passed:

- All six generated art-bearing files match the installed script semantics, including their new graphic references.
- Comparing these files with Git HEAD after excluding graphic fields found no other semantic changes. Positions, prerequisites, costs, modifiers and activation behaviour are preserved.
- All 78 source images match their recorded hashes, dimensions, image formats and transparency. All focus references have registered shine companions, and idea references resolve to the proper small texture class.
- The existing SSR static validator reports no errors or warnings across 43 outputs. Python syntax checks passed for the five changed generator modules.

`tools/ssr_1970/ART_VALIDATION.json`, `ART_INSTALLATION.json` and `VALIDATION.json` retain the compact evidence. The original native engine report is historical evidence from before this art change and has not been presented as a new graphics test. Live game rendering was not tested for this change.

The associated Union expansion remains a design proposal. The user's corrected quota period is a full 365 days from issue for every building or production target, including targets issued midyear. No new quota runtime was installed by this artwork change.

Provenance: the source material is inherited HOI4, Millennium Dawn and Cold War artwork already present in this checkout. Original individual authors and the applicable licence or permission are unknown where inherited donor records do not identify them. No ownership is asserted. Selection, reference registration and the review composition are the modifications recorded here; source images are unchanged. See `tools/ssr_1970/art_catalogue.json` and `IMPERIA_COLD_WAR_NOTICE.md`.

Exploratory candidate contact sheets are private review intermediates retained on E:, outside the mod directory, under `E:/HOI4_Mod_Tools/mdcoldwar/runtime/ssr_icon_review_20261025/`. The final compact selection sheet and this report remain in the repository.
