# Casa Scînteii, Bucharest, 1970

The landmark is authored in native Blender 4.2.23 LTS and exported with the
installed `io_pdx_mesh` 0.91 addon. `source/casa_scinteii.blend` contains editable
building parts and packed textures. The PDX reader verifies the exported mesh;
it does not generate the building geometry.

The model follows the broad, stepped composition of Casa Scînteii, now called
Casa Presei Libere: a central tower, low connecting ranges, four outer towers,
three open courtyards, arcaded entrances and restrained roof ornaments. The
period television antenna reaches 104 m, with the building body at 91.6 m.
The small Lenin monument represents the statue present from 1960 to 1990.
Later advertisements and the Aripi memorial are omitted. There is no broad
ground slab under the complex; footings extend below the terrain to conceal
small terrain variations.

Documented overall dimensions and historical photographs guide this stylized
map model. Intermediate heights, wall thicknesses, ornaments and sculpture
details are estimates, rather than surveyed measurements. The 280 by 260 m
envelope and courtyard arrangement are adapted to remain readable in HOI4.

At the user's request the rear printing ranges are slimmer than the surveyed
plan: outer width 124 m, side-range thickness 22 m, and rear depth 110 m.
The rear roofs occupy about half their previous area. This keeps the courts
and connections while making the back of the model less bulky on the map.

## Game integration

The native building is `landmark_bucharest_scinteii`, with its own
`bucharest_scinteii_spawn` and placeholder entity. It appears in province 9617,
state 150, at 3214.2 / 9.8 / 1410.1. Entity scale 0.014 gives the documented
104 m tower a height of 1.456 map units above ground, matching the scale per
metre used by the Berlin and Warsaw landmarks. The intact mesh also supplies
the required destroyed fallback, since the landmark has zero damage factor.

State history initializes the landmark on `1957.1.1`, after construction was
completed by 1956. This is a game initialization date, not a claimed historical
opening day. Native `country_modifiers` grant the controlling country
`bureaucracy_cost_multiplier_modifier = -0.03`. This subtracts three percentage
points from the additive bureaucracy cost multiplier used by the money system;
it is not a fixed percentage cut to final spending. `show_modifier = yes` exposes
the bonus in the landmark tooltip. English and German localization and
two-frame building icons are included; no polling or extra ideas are needed.

House clearance is limited to the landmark's immediate area. The city mask's
header, palette and unrelated pixels are preserved. Its report and validator
also check the approved Berlin and Warsaw geometry and city-mask cells.

## Performance

The export uses one joined mesh shape, one material and one 1024-square texture
atlas. Diffuse uses BC1; packed normal/specular use BC3. All three DDS files
contain the complete 11-level mip chain. Window groups, relief and surface
variation use texture detail, reserving geometry for the silhouette, courts
and entrance arches.

The validator enforces fewer than 8,000 triangles and 16,000 exported vertices.
The exact final counts and hashes are recorded in `blender_export.json` and
`validation_report.json`. No unverified LOD mechanism is used.

## Rebuild and verification

Requires Python with Pillow and NumPy, the configured Blender runtime and the
installed PDX exporter used by the Berlin sources. The runtime path is in
`config.json`; override it with `build.py --blender <path>` when necessary.
The authoring reuses existing Warsaw primitive helpers and Berlin's native
export helper; material generation reuses Warsaw's DDS mip writer. Each output
has a dedicated Bucharest filename, so these helpers leave the existing
landmarks and their atlases intact.

```powershell
python tools/bucharest_landmarks/clear_city_corridor.py
python tools/bucharest_landmarks/build.py
python tools/bucharest_landmarks/validate.py
```

`build.py` creates the material atlas, runs the native Blender authoring and
export, creates the icons, reads the shipped PDX geometry back into Blender for
a verification render, then runs the read-only validator. Blender preferences
are redirected to ignored `runtime/`; background processes do not open a window
on Windows. Blender may require execution outside the restricted shell sandbox.

- `previews/casa_scinteii.png`: native source render, principal facade.
- `previews/casa_scinteii_rear.png`: reverse view showing the courts and rear wings.
- `previews/casa_scinteii_icon.png`: transparent native source render used for UI.
- `previews/casa_scinteii_export.png`: shipped PDX geometry read back into Blender.
- `blender_export.json`: native source/export hashes and performance counts.
- `validation_report.json`: geometry, textures, integration and preservation checks.
- `city_clearance_report.json`: exact local city-mask changes.
- `placement_report.json`: two nearby visual spawn positions moved clear of
  the native landmark footprint; ordinary building levels, supply-node province
  and railway data are preserved.

The images are Blender renders, not HOI4 screenshots. In-game visual
confirmation remains necessary. Restart HOI4 and start a fresh 1970 game to
initialize the landmark from state history; loading an existing save does not
apply new historical buildings.

## References and map attribution

- [CNI Coresi, building operator: history, dimensions and height](https://www.cni-coresi.ro/despre-2/despre-noi/istorie/).
- [AGERPRES: historical and current views, 24 March 2023](https://agerpres.ro/documentare/2023/03/24/atunci-si-acum-casa-presei-libere--1079520).
- [ICOMOS: architectural analysis and illustrations](https://journals.ub.uni-heidelberg.de/index.php/icomoshefte/article/view/20095/13886).
- [cIMeC / National Heritage Institute: historical postcard](https://cartipostale.cimec.ro/Detaliu.php?id=11838).
- [OpenStreetMap relation 15922160](https://www.openstreetmap.org/relation/15922160),
  used as a reference for the footprint and courtyard arrangement. Map data
  © OpenStreetMap contributors, available under the
  [Open Database Licence](https://www.openstreetmap.org/copyright).

The model's rectangular masses are a stylized interpretation of the referenced
footprint, not a copy of its individual vertices. Period photographs guide the
facades and historical features; they are not used as game textures.
