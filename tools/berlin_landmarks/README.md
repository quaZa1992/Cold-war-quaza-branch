# Berlin landmarks — Blender sources and game export

Both landmarks are authored and saved in Blender 4.2.23 LTS. The installed
`io_pdx_mesh` 0.91 Blender exporter generates the four native HOI4 meshes.
No vanilla installation file is modified. The Reichstag remains reverted.

## Editable sources and previews

- `source/tv_tower.blend`: separately editable shaft, sphere, window trims,
  catching platform, railings, aerials and red-white antenna. DDS materials packed.
- `source/berlin_wall.blend`: editable concrete walls, round crowns, patrol lane,
  lights, control strip, fence and watchtowers; Blender bevel modifiers retained.
- `previews/blender_tower.png`, `blender_tower_detail.png`, `blender_wall.png`:
  actual Cycles renders from those sources.
- `previews/blender_map_scale.png`: Blender composition using the real game
  entity scale and map anchors. This is not an in-game screenshot.
- `previews/blender_export_verification.png`: final PDX files read back into
  Blender and rendered at the configured game scale, including exported UVs
  and custom normals. This verifies the shipped meshes as well as the sources.
- `previews/border_placement.png`: route against the actual province bitmap.

## Current design

The TV tower uses the original 365 m height and a 32 m sphere centered at 213.78 m.
The concrete shaft has a curved foot, tapers to 9 m diameter at 190 m and continues
cylindrically to the platform at 248.7 m. The antenna has a roughly 4 m base
and tapers to the original 1.8 m tip. The silver shell has subtle pyramidal normal
detail rather than alternating gray plates; two lower window rows and restrained
antenna equipment remain readable in the silhouette. The 1972 entrance pavilion
is omitted for the 1970 setting.

Game scale is now **.014** (5.11 map units tall), one third of the previous .042.
The northern anchor remains **3013.20 / 1572.70**, clear of the radar installation.
The required custom spawn entity alias remains present. State 45 / province 6521
receives the tower from 3 October 1969.

The wall follows **four long runs** instead of eleven right-angle pixel steps.
Its five control points retain both endpoints of the real shared Berlin border;
the centerline differs from the raster staircase by at most **0.5 map units**.
The province bitmap is unchanged. This deliberately smooths the boundary's tiny
steps rather than tracing them again. The compact border strip is 0.50 units wide;
front and rear walls remain 0.56 and 0.44 units high, plus their round coping.

The normal map's blue channel is zero on exterior surfaces: HOI4 uses this channel
as an emissive mask. This avoids making the entire tower and wall glow at night.

## Rebuild

Requires Python with NumPy/Pillow/Matplotlib, installed Blender and `io_pdx_mesh`.
Paths and dimensions live in `config.json`.

```powershell
python tools/berlin_landmarks/build.py
python tools/berlin_landmarks/preview.py
python tools/berlin_landmarks/validate_blender.py
```

## Decorative house clearance

`clear_city_corridor.py` patches only local city-style pixels along the approved
wall in `map/cities.bmp`. The existing unassigned index 3 suppresses decorative
house groups there; terrain, province borders, state history, the city name and
the approved landmark models stay unchanged. The buffer includes the largest
western house radius (1.3096 map units), half a pixel diagonal and a small margin,
so houses with centers next to the wall do not project their roofs into it.

The initial patch cleared 61 map pixels. The subsequent small density adjustment
restores three outer pixels, leaving 58 clear; the extra margin is reduced from
0.10 to 0.02 while retaining the full house radius and half-pixel safety distance.
Original BMP V4 header/palette bytes are
preserved verbatim; the ignored `runtime/cities_before_wall_clearance.bmp` backup
and `city_clearance_report.json` retain the original data and exact pixel list.
This is a local house-generation mask, not a change to city density worldwide.
Use the game console command `cityreload` or restart HOI4 to reload the decoration;
a new campaign is unnecessary for this visual map asset. In-game confirmation
is still required after reloading.

`build.py` launches the actual installed Blender. Its `--game` argument is retained
for compatibility but unnecessary for geometry creation. `blender_landmarks.py`
authors the native Blender objects, saves the `.blend` projects, prepares applied
modifiers/triangles/UV tangents on export copies, and invokes the unmodified
installed PDX exporter. Source objects stay editable. `blender_reexport.py` can
re-export those saved projects without rerendering; run it with Blender's
`--background --factory-startup --python-exit-code 1 --python` flags.
The export preparation removes collapsed microfaces with Blender's BMesh tools;
the long wall panels keep plain vertical faces and separate rounded coping,
avoiding unstable bottom bevels below the map terrain.

The full build redirects Blender preferences into ignored `runtime/`; it does not
register the exporter UI or modify the user's Blender preferences. `pdx.py` is used
only for reading/validation, not for generating the current model geometry.

`blender_export.json` records source and export hashes. `validation_report_blender.json`
checks Blender headers/hashes, the four mesh structures, normals/tangents, winding,
bounds, material references, smoothed boundary deviation, tower proportions and
placement, spawn alias, and absence of a Reichstag override. In-game visual
verification still requires restarting HOI4 and loading a new 1970 game.

## References

- [Original 1970 elevation and engineering description](https://hidden-structures.info/wp-content/uploads/2023/11/03_Fernsehturm_Auszug_Ingenieurbaufuehrer_Berlin.pdf)
- [Berlin monument database](https://denkmaldatenbank.berlin.de/daobj.php?obj_dok_nr=09065023)
- [Official Berlin monument photograph](https://www.berlin.de/ost-west-ost-kulturbahnhoefe/history-walk/artikel.1558558.php)
