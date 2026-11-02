# IMPERIA COLD WAR — Cayo Blanco del Sur

State **1252**, province **16537**, RGB **214 / 173 / 62**. Starts Cuban, with a
Cuban core and the pre-1972 name. The Cuba 1970 tree separately negotiates
symbolic renaming or an actual transfer with explicit DDR consent.

Native MD **Kharg** (state 1241 / province 16398) is the reference: a nine-pixel
island, one state/province, nine unit locator records, and 32 building locator
records. Every donor locator type is carried over, including coastal spawns and
the floating-harbour sea anchor. Locator records do not grant built facilities.
The island has no initial port, factories, resources, or victory points. It uses
MD's existing `state_00` category with one local building slot and a one-person
population floor. The former `state_inhospitable` category prevented both native
investment menus from appearing. Cuba's daily update repairs that old category
in existing 1970 saves, including if the island is now DDR-owned; see
`../cuba_1970/ISLAND_INVESTMENT_FIX.md`.

The backup is under
`rollback_backups/cayo_blanco_del_sur_20261023_before_install/`, with original
file hashes and the two feature-created runtime paths recorded in its manifest.
It was created and verified before any runtime edit. Backups and runtime probe
files are ignored by Git. No vanilla or installed workshop files are modified.

```powershell
python tools/cayo_blanco_del_sur/build.py          # stage only
python tools/cayo_blanco_del_sur/validate.py --staged
python tools/cayo_blanco_del_sur/build.py --apply
python tools/cayo_blanco_del_sur/validate.py
python tools/cayo_blanco_del_sur/preview.py
python tools/cayo_blanco_del_sur/engine_probe.py --hold
python tools/cayo_blanco_del_sur/restore.py        # inspect rollback only
```

`restore.py --apply` restores only this feature. It refuses to overwrite later
unrelated edits. `build.py --apply` similarly requires every existing target to
match either the verified backup or its exact generated output.

The image writers patch existing pixel bytes, preserving original BMP headers,
palettes, padding, and DDS headers. Only nine province pixels change; the local
height apron stays below sea level. Land colour has no city emissivity; city
index 3 suppresses decorative houses, following the established Berlin mask.
Trees and water colour remain unchanged. The GDP startup restore list includes
the new state with the same productivity as its Cuban coastal neighbour.

CSV map files have no injected script comments: those records are positional
data. Their custom additions are identified in `install_manifest.json` and the
Kharg audit. Script and localisation blocks carry the project's feature marker.
Scripts are UTF-8 without BOM; English localisation has a BOM.

The native probe uses a separate user directory and an ignored temporary addon.
It checks starting ownership/core/economy, transfers just the island to the GDR,
exercises the future rename key, and returns it to Cuba. The normal launcher
playset and normal saves are not changed. See `docs/design/cuba_1970_island/` for
the actual validation and engine results; a static pass alone is not an engine
or visual pass.
