# COLDWAR Egypt 1970 generator

Source of the Egypt 1970 focus tree (`COLDWAR_EGY_1970_focus`). The mod files are generated, do not edit them by hand.

- `egy_tree.json` – approved design (805 foci, German design text)
- `desc/out_*.json` – English focus descriptions, `desc/icons_*.json` – icon picks (+2 alternatives)
- `cw_effects.py` / `cw_events.py` / `cw_avail.py` – translation of the design lines into Clausewitz, events and offers
- `cw_compile.py` – focus file and layout, `cw_build.py` – all other files, `validate_cw.py` – static checks

Run `python3 cw_build.py && python3 validate_cw.py`. The scripts read the mod's localisation, gfx and modifier files from
`/mnt/user-data/uploads/mdcoldwar/...` (staged copies); adjust those paths to your mod folder when running locally.
Output goes to `out/` with the same relative paths as the mod.

Naming convention: everything new carries **COLDWAR** (like Imperia's IMP): IDs `COLDWAR_EGY_*`, events `COLDWAR_EGY.N`,
files `COLDWAR_EGY_1970_*`, sprites `GFX_COLDWAR_goal_*`, comments `# COLDWAR |`.
