IMPERIA COLD WAR

# Cold War doctrine artwork provenance

The fourteen new doctrine icons were generated with the built-in OpenAI ImageGen tool at the user's request. Codex directed the prompts to match the existing Millennium Dawn doctrine pictogram family. There are no external photographs, national emblems, author signatures or visible project watermarks in the new artwork.

`imagegen_sources.json` preserves the exact prompts, built-in generation route, transparent-background setting, style-reference paths and original output paths. `masters/` contains copied original RGBA PNG outputs and 64-pixel review PNGs. `icon_manifest.json` records source and runtime texture hashes, dimensions, alpha bounds and format.

Style references are the existing Millennium Dawn textures `gfx/interface/technologies/0_generic/Land_Doctrines/overwhelming_firepower.dds` and `large_front_operations.dds`. Additional images in `native_references.png` are existing MD textures used solely for the local review of the style. Their individual artists, separate redistribution licences and permission are unknown in the supplied checkout. Reference PNGs are unchanged format conversions. Existing upstream rights remain separate; the project marker does not establish ownership of them.

The new masters are AI-generated assets, not claimed to be hand-drawn by an MD artist. Their applicable service terms govern their use; no separate public asset licence is assigned here. Export modifications are limited to removing empty transparent margins, proportional downscaling, centering and lossless DDS channel encoding. `export_icons.py` preserves the original masters and verifies exact decoded colour and alpha for every DDS.

Runtime output: `gfx/interface/doctrines/icons/land/mdcw_expansion/`. Companion record: `IMPERIA_COLD_WAR_NOTICE.md` in that directory. The review sheet is an asset composition, not a live game screenshot.
