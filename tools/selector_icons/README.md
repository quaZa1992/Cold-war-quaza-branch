# IMPERIA CW — Cold War: Selector policy artwork

Thirty-one individual badges were generated with the built-in `image_gen` tool.
The complete prompts, subjects, category assignments and reference images are in
`manifest.json`; source receipts are in `generation_receipts.json`. Every selected
generated image is retained under `masters/` inside this workspace.

The original numbered Imperia badges provide the visual reference: political
institutions use blue, economic policies green, and military policies burgundy.
The eight era policies, ten Cold War Equilibrium policies, both guest-worker
programmes, the joint training command, eight policies previously reusing another
policy's artwork, the licensed-armaments programme and directed urbanisation now have distinct icons.
The guest-worker country backlash and dynamic cost displays use the corresponding
new recruitment/employment icons as well.

## Licensed Armaments Programme

Military selector; 250 PP base adoption cost, 150 PP base removal cost and the
selector's existing 1,440-day commitment convention. Native modifiers grant
`license_production_speed = 0.40` and `industrial_capacity_factory = -0.10`.
The factory output penalty affects all military factories, including licensed
lines; it does not penalise only domestic designs. Standard licence agreements,
foreign approval, technology penalties and payments remain the engine's concern.
The policy does not add polling, on-actions, events or country/state scans.

## Export and verification

Run `python tools/selector_icons/build.py` from the repository root.
`--register-only` updates picture assignments and sprite registration without
re-exporting textures. Registration is idempotent.

FFmpeg only downsizes the generated artwork, using premultiplied filtering to
preserve the alpha edge. Native textures are 64×64 uncompressed RGBA32 DDS, without
lossy block compression or mipmaps. PNG companions match the decoded DDS exactly.
Runtime textures are in `gfx/interface/ideas/COLDWAR_selector/` and registered in
`interface/COLDWAR_IMPERIA_selector_icons.gfx`.

`preview.png` shows every native icon beside a nearest-neighbour enlargement for
pixel inspection. `overview.png` is the presentation overview. `validation.json`
records source/output hashes, formats and alpha checks; `integration_audit.json`
records sprite uniqueness, actual selector categories, colour validation,
localisation, encoding, supported engine modifiers and unchanged existing gameplay
tokens. Script/GFX files use UTF-8 without BOM; localisation uses UTF-8 with BOM.
Static integration and visual export checks passed. No running-game or multiplayer
session was used for validation.
