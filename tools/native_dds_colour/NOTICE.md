# IMPERIA COLD WAR — Native DDS colour-storage audit and provenance

The initial read-only scan examined 58,551 valid DDS headers under `gfx/`. Nine additional uncompressed 32-bit textures used RGBA masks and byte order instead of the established native MD BGRA layout. The scan is recorded in `scan.json`. Compressed textures, DX10 textures, RGB565 and single-channel formats were left unchanged. This audit identifies the channel-order defect, not every possible artistic colour difference.

`repair.py` changes only storage order and the matching channel masks in the nine explicitly listed files. Every pixel, including all mip levels and alpha, is retained. The decoded top-level image and file length are verified. Original bytes are retained under `before/`; `repair_report.json` records hashes. The Soviet and DDR generator staging copies are updated as well, and four custom exporters now produce the corrected format directly. `python tools/native_dds_colour/repair.py --check` verifies the installed assets without rewriting them.

Sources and credits:

- DDR introduction: the retained MD photograph `gfx/event_pictures/europe/russia - SOV/warsaw1_gdr.dds` and native country-event frame. Original photographer and specific redistribution permission: unknown. Existing export record: `tools/event_art/source/COLDWAR_DDR_intro_export.json`.
- Soviet Politburo: the retained photograph and built-in Imagegen restoration recorded in `docs/event_art_review/politburo_export.json`. Original photographer and specific permission: unknown.
- UAE rulers: user-supplied monochrome photograph and built-in Imagegen colourisation recorded in `tools/uae_1970/art/README.md`. Original photographer and redistribution permission: unknown.
- Joint training and guest-worker badges: existing built-in Imagegen masters; see `tools/joint_training_icon/validation.json` and `tools/guest_workers/art/IMAGEGEN_ICONS.md`. Original reference-icon author and applicable permission: unknown.
- Iranian balance-of-power image, Maersk company badge and Turkish party icon: pre-existing project/MD assets at the paths in `repair.py`. Original authors, credits and applicable asset licences or permissions: unknown. Existing notices and source records remain applicable.

Modification author for this correction: Codex, at the user's request. No new image generation, repainting, visible watermark or ownership claim is involved in the format repair. Original source artwork and its existing rights remain separate from the project marker.
