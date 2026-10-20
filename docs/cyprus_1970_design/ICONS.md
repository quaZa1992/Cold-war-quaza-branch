# Cyprus 1970 icon map

`runtime_icon_map.json` supplies an icon assignment for all 295 focus IDs and all 11 starting spirit IDs in `coldwar_cyprus_1970_design.json`. Each entry records the registered sprite, its texture path, and a short rationale. The map deliberately reuses the existing Millennium Dawn Cold War goal artwork: 25 distinct registered sprites cover the 306 entries.

The sprites are registered in `interface/COLDWAR_EGY_1970_goals.gfx`; the selected texture files exist under `gfx/interface/goals/coldwar/`. The icon artwork was visually sampled from a Pillow contact sheet, including the constitution, civilian oversight, council, parliament, election, Mediterranean, investment, roads, ports, irrigation, factory, worker, army, negotiation, ceasefire, and reconstruction motifs. Cyprus- or Eastern Mediterranean-specific artwork is only used where the image remains geographically appropriate; Egypt-specific political imagery was avoided.

No new icon textures or sprite registrations were needed, so this task adds no `interface/COLDWAR_CYP_1970_goals.gfx`. Existing sprite identifiers are used directly. Assignment is intentionally thematic rather than one-icon-per-focus; related project and political-route focuses share motifs.
