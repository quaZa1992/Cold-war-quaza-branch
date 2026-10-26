# Warsaw 1970 landmark and city style

The Palace of Culture and Science is authored in native Blender 4.2.23 LTS and
exported with the installed, unmodified `io_pdx_mesh` 0.91 addon. The editable
`source/warsaw_palace.blend` contains separate wings, tower, terrace, ornamental
attics, entrance portico, west Congress Hall and original spire. Textures are
packed. The PDX reader is used for verification, never geometry generation.

The model represents the pre-1994, 230.68 m silhouette and omits the later clock
dials. At entity scale .014 it is 3.22952 map units tall, using the same scale per
metre as the approved Berlin TV tower. Position is province 3544 in state 114,
3131.50 / 9.80 / 1563.50, facing east. A custom spawn slot and its placeholder
entity prevent conflicts with other buildings. State history adds it on
22 July 1955, before the 1970 scenario. The indestructible landmark uses its
intact model for the required destroyed fallback.

This is a stylized map model based on documented massing, dimensions and period
features; intermediate wing and ornament dimensions are approximations.

## Visual refinement and performance

The revised model uses compact tower setbacks, a close-fitting observation
gallery at 114 m, a solid clockless upper field, a steep pavilion roof and a
continuous needle. Carved attic bands and sparse finials replace the detached
roof beads. Five monumental porticoes, recessed dark roofs, rusticated ground
floors and the visible round, domed Congress Hall differentiate the lower wings.
The built 1955 aerial and street photographs guide this version.

Facade panels carry windows, frames, stone joints and small relief details in
one 1024-square atlas. BC1 diffuse and BC3 packed normal/specular DDS textures
have complete 11-level mip chains to reduce texture aliasing at map distance.
The shipped model has **6,380 triangles and 13,753 exported vertices**, down from
16,144 / 33,545 (60.5% fewer triangles). One joined shape and one material keep
the same draw-call count. The native spire is only 12-sided; broad silhouette
elements retain the geometry budget. There is no unverified LOD mechanism.

The broad rectangular forecourt slab has been removed. Existing ground-level
walls, the lowest entrance steps and southern columns extend to terrain level;
their upper edges and the palace silhouette retain the approved proportions.

The validator enforces fewer than 8,000 triangles and 16,000 vertices, one
material, and correct block-compressed DDS headers and mip payloads.

## Gameplay

Native landmark `country_modifiers` grant the province controller
`education_cost_multiplier_modifier = -0.03` and `research_speed_factor = 0.02`.
The former is the real country modifier consumed by `update_education_rate` in
`common/scripted_effects/00_money_system.txt`; it subtracts three percentage
points from the additive education cost multiplier. The research bonus is +2%.
`show_modifier = yes` exposes both in the ordinary landmark tooltip. No periodic
scripts, polling, extra ideas, or global changes are required.

## Local city style

Eleven hand-placed modern skyscrapers in Warsaw have been removed. Four historic
blocks remain, with one moved clear of the palace. Index 4 in `map/cities.bmp`
is used only inside province 3544 and selects low houses, old-town masonry and
midrise courtyard blocks. Fifty-nine pixels generate houses; 45 clear the palace
plaza. The clearance includes the largest house radius plus the half-pixel
diagonal and a small margin. The original BMP header and palette are preserved,
as are all pixels outside Warsaw, including Berlin's approved wall clearance.

`city_style.py` applies these scoped edits idempotently; `city_style_report.json`
records exact pixels, removed objects, moved block, bounds and checks. It does
not regenerate any province boundary or change global city styles.

## Rebuild and verification

Requires Python with Pillow/NumPy, the configured Blender runtime, and the same
PDX exporter used by the Berlin sources. Paths live in `config.json`.

```powershell
python tools/warsaw_landmarks/city_style.py
python tools/warsaw_landmarks/build.py
python tools/warsaw_landmarks/validate.py
```

The Blender runtime may require execution outside the restricted shell sandbox.
User preferences are redirected into ignored `runtime/`.

- `previews/palace_blender.png`: native source render.
- `previews/palace_west.png`: rear view of the circular Congress Hall and roofs.
- `previews/city_style.png`: actual selected game house meshes.
- `previews/palace_export_scale.png`: shipped PDX geometry read back into Blender,
  with exported UVs and normals; surrounding house meshes use their real game
  scale. House positions in this studio comparison are illustrative.
- `blender_export.json`: source/export hashes and Blender version.
- `validation_report.json`: numerical geometry and integration checks.

These previews are Blender renders, not screenshots of HOI4. In-game visual
confirmation remains necessary. Restart HOI4 and start a fresh 1970 game to load
the new building from state history. `cityreload` alone reloads city decorations,
but does not add a new historical landmark to an existing save.

## Primary references

- [PKiN operator: height, 1994 mast extension and later clocks](https://pkin.pl/en/trivia/)
- [PKiN operator: history and 1955 opening](https://pkin.pl/en/history/)
- [National heritage register: tower, wings and Congress Hall](https://zabytek.pl/en/obiekty/palac-kultury-i-nauki-warszawa)
- [Period construction models and 1955 aerial views](https://visitpkin.pl/en/history/)

The Berlin wall, tower, Reichstag state and their approved source models are not
modified by this Warsaw build.
