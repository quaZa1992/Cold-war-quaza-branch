# COLDWAR guest-worker programme icons

Both replacements were edited with the built-in `image_gen` tool on19 October2026, using the previous icons as edit targets. They are project assets, not previews awaiting approval.

## Files and export

- Master: `source/COLDWAR_gw_overseas_employment_master.png` (1254×1254 RGBA). Loaded sprite: `gfx/interface/ideas/nat_ideas/mdcw_gw_overseas_employment.dds`; matching PNG beside it.
- Master: `source/COLDWAR_gw_recruitment_master.png` (1254×1254 RGBA). Loaded sprite: `gfx/interface/ideas/nat_ideas/mdcw_gw_recruitment.dds`; matching PNG beside it.
- Existing sprite IDs and idea bindings remain in `interface/mdcw_guest_workers.gfx` and `common/ideas/mdcw_guest_workers_ideas.txt`.
- Rebuild only these two textures with `tools/guest_workers/export_programme_icons.ps1`. FFmpeg resamples the generated masters using Lanczos and premultiplied-alpha filtering, then exports straight-alpha64×64 PNG and uncompressed32-bit RGBA DDS. The exporter does not procedurally draw workers, arrows or borders.
- Previous DDS files used DXT5. The replacement uses lossless RGBA, avoiding DXT block quantisation. Keep the generated high-resolution source; do not repeatedly upscale or re-compress the64px game texture.

## Verification

Both64px exports were visually inspected. PNG and decoded DDS pixels match exactly; corner alpha is0 and opaque alpha is255; intermediate alpha values are preserved. See `icon_validation.json`. No mechanics, localisation or UI layout was changed. Native game loading/rendering remains untested; restart HOI4 to reload the textures.

## Final prompts

### Overseas Employment

Use case: precise-object-edit. Asset type: a single Hearts of Iron IV Millennium Dawn national-idea icon, a transparent game UI sprite. The supplied image is the edit target, NOT a pixel-art style reference. Reconstruct and refine this exact emblem as clean high-resolution artwork at 1024x1024: one circular dark forest-green enamel badge with a restrained silver metal rim, a white/light-silver relief silhouette of a civilian construction worker in a hard hat and work overalls on the LEFT, with one clearly legible broad white arrow on the RIGHT pointing RIGHT, representing overseas employment and outward worker movement. Preserve the subject, green/silver palette, circular composition and right-pointing arrow. Replace the coarse pixel-drawn worker and staircase contours with fluid, smooth, precisely antialiased, tasteful engraved/illustrated contours; simplified coherent anatomy and clean folds in work clothes, no tiny facial details. Match the sober lightly worn metal-and-enamel style of native Millennium Dawn idea icons; crisp high contrast that survives reduction to64x64. Make the worker larger and readable; limit detail and keep the arrow separate from the figure. Keep the entire circle within the square with about4% transparent padding on each side. Outside the badge must be genuine transparent alpha, including clean edge antialiasing. One icon only, centered, front-facing, no scene, no UI panel, no wording, no numbers, no letters, no flags, no watermark, no pixel art, no checkerboard painted into the image, no white square, no blur, no glow.

### Guest Worker Recruitment

Use case: precise-object-edit. Asset type: a single Hearts of Iron IV Millennium Dawn national-idea icon, a transparent game UI sprite. The supplied image is the edit target, NOT a pixel-art style reference. Reconstruct and refine this exact emblem as clean high-resolution artwork at 1024x1024: one circular dark forest-green enamel badge with a restrained silver metal rim, a white/light-silver relief silhouette of a civilian construction worker in a hard hat and work overalls on the LEFT, with one clearly legible broad white arrow on the RIGHT pointing LEFT TOWARDS THE WORKER, representing guest-worker recruitment and inward worker movement. Preserve the subject, green/silver palette, circular composition and LEFT-pointing arrow. Replace the coarse pixel-drawn worker and staircase contours with fluid, smooth, precisely antialiased, tasteful engraved/illustrated contours; simplified coherent anatomy and clean folds in work clothes, no tiny facial details. Match the sober lightly worn metal-and-enamel style of native Millennium Dawn idea icons; crisp high contrast that survives reduction to64x64. Make the worker larger and readable; limit detail and keep the arrow separate from the figure. Keep the entire circle within the square with about4% transparent padding on each side. Outside the badge must be genuine transparent alpha, including clean edge antialiasing. One icon only, centered, front-facing, no scene, no UI panel, no wording, no numbers, no letters, no flags, no watermark, no pixel art, no checkerboard painted into the image, no white square, no blur, no glow.

