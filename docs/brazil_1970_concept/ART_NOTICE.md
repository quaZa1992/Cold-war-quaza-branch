IMPERIA COLD WAR

# Brazil 1970 art assets and provenance

This art integration is for the approved Brazil 1970 national programme. Its focus aliases and idea artwork derive from assets already present in this mod. Country-event artwork reuses existing MD framed images without modifying their pixels. The images are illustrative and are not presented as photographs of the specific historical events described by the event titles.

## Focus and idea icons

Focus icons alias the existing textures registered by `interface/goals.gfx`. Their native `*_shine` aliases use the same source texture and the two-scroll animation convention in `interface/goals_shine.gfx`. The exact source texture and generated alias names are in `tools/brazil_1970_runtime/art_manifest.json`.

Starting spirit and focus-group idea icons use source images already in this mod, proportionally fitted and centered on transparent 128 x 128 DDS canvases. Standard native sprite aliases are registered as `GFX_idea_COLDWAR_BRA_<starting-spirit-id>` and `GFX_idea_COLDWAR_BRA_group_<group-id>`; use the matching suffix as the idea `picture` key. Source assets are listed in `tools/brazil_1970_runtime/art.py`. The image pixels belong to their existing upstream/mod sources; original artists, attribution terms, and specific licence permissions were not established by this integration and remain unknown.

## Country-event pictures

Nine full 217 x 163 DDS images are copied byte-for-byte to `gfx/event_pictures/COLDWAR_BRA_1970/`. Eight map to the approved Brazil events and one generic treaty image is available for recipient agreement notices. Source files are specified in `tools/brazil_1970_runtime/art.py`; sprite registrations and event keys are in `interface/COLDWAR_BRA_1970.gfx` and `art_manifest.json`.

The source images were visually reviewed as complete country-event pictures, including their outer frame and photo aperture. The native MD frame is 217 x 163 with a 180 x 150 image inset at x=19, y=6. Since the source pictures are copied unchanged, frame and alpha pixels remain identical. Credit and licensing for the source photographs and composited frames are unknown. Reuse does not establish ownership or replace any applicable upstream licence.

The full donor layout was inspected in `interface/eventwindow.gui`: the event window is 581 x 427; the bottom container begins at y=221; the country-event picture is at window x=5, y=226 and displays at 217 x 163; its clipping window starts at bottom-container x=-3, y=35. The option grid begins at window x=215, y=220, is 300 x 30, and has 300 x 47 option slots. No shared GUI was changed.

Any visual inspection sheets made during this work are temporary donor-composed previews, not live game screenshots. The installed DDS files are the actual registered assets.
