IMPERIA COLD WAR

# Chile 1970 event-art review

## Decision

Reuse existing, registered Millennium Dawn country-event sprites without copying or modifying their image files. The installed MD donor has appropriate generic photographs for the 14 Chilean event subjects. No Chile-, Allende- or Pinochet-specific 1970s event photograph was found in the donor or project `gfx/event_pictures` folders. Reuse keeps the native event-image viewport and alpha treatment intact, avoids new uncredited binaries, and requires no extra sprite registry.

## Native event window measurements

Donor source: `C:/Program Files (x86)/Steam/steamapps/workshop/content/394360/3374271790/interface/eventwindow.gui`.

- `EventWindow` begins at line 3, size 581 x 427.
- The bottom window begins at line 74, size 581 x 206.
- The event image uses `GFX_report_event_001` at bottom-window x=5, y=5 (lines 86-91).
- The clipping frame uses `GFX_event_pic_clip` at x=-3, y=35 (lines 93-98).
- The option grid begins at x=215, y=-1; size 300 x 30; slots are 300 x 47; one option column (lines 103-108).
- The MD country-event pictures checked below are 217 x 163 DDS textures. Reusing them unchanged preserves their source alpha pixels; the native clip sprite and event-window geometry remain responsible for the displayed frame.

The game registry maps `GFX_report_event_001` to `gfx/event_pictures/report_event_001.dds` in base-game `interface/eventpictures.gfx` (line 324). The donor `interface/MD_eventpictures.gfx` contains the named sprites and their file paths.

## Reusable art by event subject

All listed pictures were visually inspected in their 217 x 163 event-window shape and measured at that size. `GFX_*` keys and filenames are case-sensitive.

| Chile event subject | Suggested MD sprite | Donor image path | Notes |
| --- | --- | --- | --- |
| 1970 presidential succession; 1988 plebiscite | `GFX_election_day` or `GFX_election_rally` | `gfx/event_pictures/generic/elections/GFX_election_day.dds`; `.../GFX_election_rally.dds` | Ballot-day motif or public rally. |
| Congress, constitutional settlement, civilian handover | `GFX_political_deal` or `GFX_politics_talks` | `gfx/event_pictures/generic/elections/political_deal.dds`; `gfx/event_pictures/generic/politics/politics_talks.dds` | Parliamentary table or political discussion. |
| Copper compensation; Andean regional agreement | `GFX_treaty` | `gfx/event_pictures/generic/events/treaty.dds` | Signing document; generic diplomacy image. |
| Transport stoppage | `GFX_generic_train_event` | `gfx/event_pictures/generic/events/generic_train_event.dds` | Broad rail transport image; it does not depict the Chilean trucker strike. |
| Constitutional rupture; repression; military government | `GFX_internal_conflict` or `GFX_Military_Reform` | `gfx/event_pictures/generic/events/internal_conflict.dds`; `gfx/event_pictures/generic/events/Military_Reform.dds` | Generic political conflict or soldiers. Neither is Chile-specific. Avoid using donor Ecuador junta art as if it showed Chile. |
| Adjustment and external credit | `GFX_banking_crisis` | `gfx/event_pictures/generic/events/banking_crisis.dds` | Financial image. |
| Copper industry | `GFX_mining` | `gfx/event_pictures/generic/events/mining.dds` | Industrial mine machinery. |
| Truth, justice, reparations | `GFX_court` | `gfx/event_pictures/generic/events/court.dds` | Courtroom gavel. |

The 14 events reuse pictures where the composition fits both. The exact mapping is recorded in `tools/chile_1970/event_art.py`; its `build()` intentionally emits no files because all selected IDs already resolve in the installed MD registry. The event title and description provide the Chile-specific context; the image is illustrative.

The source alpha channel is intrinsic to each existing picture and is preserved by direct reuse. In the left/right 19-pixel margins and top/bottom 6/7-pixel margins around the central 180 x 150 photo area, selected photographs show both transparent and opaque frame pixels. Measured outer-band alpha extrema are 0-255 for election rally, political deal, mining, train, internal conflict, military reform, banking crisis, court and treaty. (Three assets considered during selection, `GFX_economy_crisis`, `GFX_politics_talks` and `GFX_election_day`, have icon-style compositions and were rejected for these event popups.) This is why the selection reuses original files as-is instead of reconstructing a frame from a single donor image. The separate `GFX_event_pic_clip` overlay is registered by base-game `interface/eventwindow.gfx` (line 14) and referenced by MD's event window at lines 93-98; it is not baked by this integration.

## Preview status

The emitted concept preview is `COLDWAR_CHL_preview.html` and the rendered focus-tree overview is `preview-overview.png` in this directory. Those show the focus-tree prototype; they do not render Chile's event popup. This mapping is therefore tied to the 14 event records in `COLDWAR_CHL_design.json`, not presented as an event-window screenshot. The native event UI geometry and donor art were inspected independently. No live HOI4 launch, event popup, or engine validation is claimed here.

## Provenance and limits

Source: the installed Millennium Dawn donor at `C:/Program Files (x86)/Steam/steamapps/workshop/content/394360/3374271790`. The underlying photographers/authors and separate redistribution permissions for these pictures are unknown from local metadata; MD and game credits/licensing remain authoritative. No art was copied, edited, generated, or exported for this review. No ownership or reuse permission is asserted here. The only files written for the initial image inventory were a temporary contact sheet, which was deleted after visual inspection.

This is an asset/UI inspection, not a live HOI4 event-window screenshot or engine validation.
