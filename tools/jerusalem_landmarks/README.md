# Western Wall, Jerusalem, 1970

The landmark is authored in native Blender 4.2.23 LTS and exported with the
installed `io_pdx_mesh` 0.91 addon. `source/western_wall.blend` contains editable
parts and packed textures. The PDX reader checks the exported geometry; it does
not generate the model. No AI-generated bitmap assets are used.

The exposed prayer face is approximately 57 m long and 19 m high. Its large
lower ashlars have geometric boss relief, while the smaller upper stone courses
use the texture atlas. A rough masonry northern attachment, small doorways and
windows, sparse plants in joints, a simple timber prayer divider and the southern
earth-and-stone access bank provide period context. The northern attachment
reaches 22 m. The model omits the later wooden Mughrabi bridge and modern plaza
canopies and the modeled plaza floor. Only the masonry, period features and
buried footings are exported; the game's terrain supplies the ground. The flat
surface in Blender previews is presentation terrain and is never exported.

Primary photographs from 1969 and 1970 guide the appearance. Overall prayer-face
dimensions are documented, but individual stone sizes, the attachment, wall
thickness, buried footings, courtyard extent and terrain adaptation are estimates
for a readable map model rather than a surveyed reconstruction. This represents
the visible prayer section, not the entire 488 m western retaining wall.

## Game integration

The native building is `landmark_jerusalem_western_wall`, with its own
`western_wall_spawn` and placeholder entity. It appears in province 1086,
state 207, at 3351.3 / 10.06 / 1174.7. Entity scale 0.025 gives the main wall
an above-ground height of 0.475 map units, and the northern attachment 0.55.
The intact mesh supplies the required destroyed fallback because the landmark
has zero damage factor.

State history initializes the landmark on `1967.6.10` for the post-1967 plaza
representation. This is a scenario initialization date, not the wall's
construction date. Native `country_modifiers` grant the controlling country
`stability_factor = 0.02` and `monthly_population = 0.02`: +2 percentage points
of stability and a +2% population-growth modifier. The population bonus modifies
growth rather than adding 2% to the total population each month.
`show_modifier = yes` exposes both bonuses in the landmark tooltip. English and
German localization and two-frame building icons are included.

Decorative-house clearance is limited to cells that could overlap the site,
including a conservative allowance for house rotation and placement jitter.
The city-mask header, palette and unrelated pixels are preserved. Existing
Berlin, Warsaw and Bucharest landmarks, their owned city-mask cells and the
Dome of the Rock assets are protected by the clearance report and validator.

## Performance

The export uses a joined mesh shape, one material and a 1024-square atlas with
complete 11-level mip chains. Diffuse uses BC1; packed normal/specular use BC3.
The shipped floor-free model has 2,999 triangles and 8,073 exported vertices.
Stone glossiness is kept low in the native specular alpha channel; the Blender
preview converts that channel to roughness so both renderers show matte stone.
Geometric detail is reserved for the silhouette, prominent lower masonry,
entrances and a few plants. Small upper stones, irregular joints, limestone
grain, weathered flakes, pores and edge abrasion use the atlas and its packed
normal map. The neutral cream-grey palette avoids multicoloured stone variation. The target budget is fewer than 7,000 triangles. Final measured counts
and hashes belong to `blender_export.json` and `validation_report.json`; a
render alone is not an in-game performance measurement.

## Rebuild and verification

Requires Python with Pillow and NumPy, the Blender runtime configured in
`config.json`, and the installed PDX exporter used by the existing landmarks.
Override the runtime with `build.py --blender <path>` when necessary. Shared
helpers are reused, while all model and atlas output filenames are dedicated
to this Jerusalem landmark.

```powershell
python tools/jerusalem_landmarks/clear_city_corridor.py
python tools/jerusalem_landmarks/build.py
python tools/jerusalem_landmarks/validate.py
```

`build.py` generates the material atlas, runs Blender authoring and export,
creates the UI icons, reads the shipped PDX mesh back into Blender for a
verification render, then runs the read-only validator. Blender preferences
are redirected to ignored `runtime/`; background processes do not open a
Windows window. Blender may require execution outside the restricted shell
sandbox.

- `previews/western_wall.png`: native source render.
- `previews/western_wall_detail.png`: closer view of the masonry and prayer face.
- `previews/western_wall_icon.png`: transparent native source render for the UI.
- `previews/western_wall_export.png`: shipped PDX geometry read back into Blender.
- `blender_export.json`: native source/export hashes and measured mesh counts.
- `validation_report.json`: geometry, textures, integration and preservation checks.
- `city_clearance_report.json`: exact local city-mask changes and protected hashes.

These previews are Blender renders, not HOI4 screenshots. Direct in-game visual
confirmation remains necessary. Restart HOI4 and start a fresh 1970 campaign to
initialize the historical building; loading an existing save does not add it.

## References

- [Western Wall Heritage Foundation: measurements and masonry](https://thekotel.org/en/wailing-wall-western-wall/).
- [Israel Antiquities Authority: Western Wall Plaza excavations, 2005–2009](https://hadashot.iaa.org.il/report_detail_eng.aspx?id=1219&mag_id=115).
- [Historical photographs, source links and CC BY 4.0 attribution](references/SOURCES.md).

The reference photographs are retained for visual research and are not used as
in-game textures. The Foundation gives slightly inconsistent course counts
(28 and 29 exposed layers); the model follows the documented appearance rather
than presenting a precise course-by-course archaeological survey.
