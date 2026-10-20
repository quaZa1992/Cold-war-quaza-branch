# Full MD-style layout preview

All 295 focuses share one navigable coordinate space. Section shortcuts move the camera without hiding or rearranging other branches. English names, exact coordinates, prerequisites, exclusive choices and proposed effects remain inspectable.

- Six major political routes contain 24 focuses each: ten political and fourteen bespoke economic focuses. Roots: x114, 136, 158, 180, 202 and 224, all y0.
- The Turkish Cypriot community has 39 focuses, rooted at (86,0), independent of the CYP ruling party.
- The researched Road to War contains 22 focuses, rooted at (6,14), with its own coup-pressure track and conditional intervention/negotiation phases.
- Nine starting spirits/state modifiers are visible above the tree. Two additional displacement/destruction burdens activate only after actual crisis harm.

The default preview opens on Road to War. **All 295** shows the full arrangement; **Opening**, **Turkish Cypriots**, **Road to war** and the section/focus picker move to exact positions. **1:1** restores native-size labels. Drag, wheel, +/- and minimap navigate the same canvas. Selecting a focus shows its effects, local/absolute positions, costs and exclusions.

World coordinates use `pixel_x=190+90*x`, `pixel_y=200+130*y`. The 90x130 preview pitch is explicit, not an assertion about engine grid constants. The inspected MD `interface/nationalfocusview.gui` defines a 165x128 focus item, textured symbols, title background, zoom controls and drag scrolling. This preview uses existing MD art; final per-focus icons remain provisional. Current full-world dimensions are 21260x4560.

Interactive fragments `coldwar-cyprus-md-layout.html` and `coldwar-cyprus-preview.html` are identical current aliases. `coldwar-cyprus-full-layout.svg` preserves every node and English label at full vector resolution. Rebuild using `build_design.py`, then `build_md_view.py`; render the fragment with the visualization render helper before running `qa_md_view.cjs`.

`MD_VIEW_ASSETS.json` records source textures and dimensions. `VALIDATION.json` checks IDs, coordinates and reciprocal exclusions. `GRAPH_REACHABILITY.json` independently checks all 295 nodes against prerequisites/exclusions with OR-within-group and AND-across-group semantics. `MD_VIEW_QA.json` records browser interactions at desktop and mobile widths. None of these checks substitutes for engine validation of future runtime definitions.

The chosen current-map campaign design explicitly abstracts the small July foothold and conference phase. Reactive milestones run through actor events/short decisions and are recorded once in the focus tree; their displayed focus duration does not delay the crisis. Actual engine warfare still requires the deliberately deferred 1970 forces/readiness setup. See `WAR_HISTORY.md` and `WAR_MECHANICS.md`. No runtime game files were changed.
