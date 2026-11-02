# IMPERIA COLD WAR — Selector icon provenance and native colour storage

Source masters: the 31 retained PNG files in `tools/selector_icons/masters/`. Their original built-in OpenAI Imagegen generation prompts, reference-image assignments and receipts are recorded in `tools/selector_icons/manifest.json` and `tools/selector_icons/generation_receipts.json`.

Original generated images: OpenAI Imagegen, commissioned for this project. Original numbered Imperia reference-icon author or credit: unknown. Applicable licence or redistribution permission for the reference artwork: unknown. This project notice does not claim ownership of that material or supply a replacement licence.

Modification for the current correction: Codex changed the native DDS exporter to store BGRA bytes with A8R8G8B8 channel masks, matching the existing numbered Imperia badges. All 31 generated selector DDS textures were re-exported from their retained masters. Source PNGs, pictograms and alpha were preserved. No new image generation or artistic recolouring was performed; the military backgrounds retain their intended burgundy tone.

Affected files: all `.dds` assets in this directory registered by `interface/COLDWAR_IMPERIA_selector_icons.gfx`. The PNG companions and `tools/selector_icons/preview.png` and `overview.png` are export and comparison previews of the same generated artwork. The exporter and output hashes are recorded in `tools/selector_icons/build.py` and `validation.json`.
