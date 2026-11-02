IMPERIA COLD WAR — German politics launcher placement audit

The launcher anchors to the native `politics_tab` token. Coordinates below are local to that token.

In `interface/countrypoliticsview.gui`, the faction row begins inside `ruling_party_info` at
(88, 300), then `faction` is offset by (95, -46), giving row origin (183, 254). The faction
member label begins at x=45 and has maxWidth=143 (outer x=228..371); the no-faction label
is x=236..379. The original_in_faction label occupies x=195..390. Its dismantle_faction
control starts at (392,254); the installed base-game GFX_dismantle_faction_button texture
is 31x31 (interface/countrypoliticsview.gfx -> gfx/interface/dismantle_faction_button.dds),
so that full native hitbox ends at (423,285). The faction open/create button uses
gfx/interface/factions/ui/factions_button.dds, 573x57 in 3 frames: 191x57 per frame,
occupying x=183..374. These controls are checked even for the engine-selected branches.
The native `view_factions_button` starts at faction-local x=285, giving x=468. Its 32 px hitbox
spans x=468..500; its y offset is -8 from the row, giving y=246..278. The native membership
controls leave a 45 px gap between x=423 and x=468 when dismantle is present.

Relations launcher bounds: (424,248)..(444,268). Security launcher bounds: (446,248)..(466,268).
Both 20x20 hitboxes clear the native dismantle button by 1 px, each other by 2 px,
and the native faction-view button by 2 px. They clear all faction-label boxes and the
national-spirit scroll area ending at y=242. The same placement is used for the DDR-only pair.

The placement preview is a coordinate diagram, not a screenshot of Hearts of Iron IV. It is rendered
by `tools/west_germany_1970/entry_ui.py --preview`.
