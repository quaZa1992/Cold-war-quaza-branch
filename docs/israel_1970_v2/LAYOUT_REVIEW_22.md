# IMPERIA COLD WAR: Israel Version 2.2 focus-only layout review

Revision: `2.2-focus-only-20261028`. Result: **PASS** for the external design preview containing 213 focuses, nineteen programmes and 244 prerequisite edges. This review supersedes the 192-focus Version 2.1 geometry review for the current proposal. No loaded national-focus, GUI, script, history or localisation file was edited by this layout task.

## Coordinate-only arrangement

`tools/israel_v2/focus_layout.py` provides `arrange(nodes, groups)`. The function changes only focus `xy` coordinates and group `origin` coordinates. It checks semantic equality before and after arrangement, preserves the supplied prerequisites and exclusive alternatives, and performs no file I/O. Reapplying it to the final data produces identical coordinates.

The major parties keep their deep downward programmes. Mafdal occupies a fifth column beside Territories because the settlement-reopening focus has a real cross-branch OR prerequisite: `Cap New Settlement Projects` or Mafdal's restraint policy. This gate remains visible and runs downward. The Negev, West Bank and Gaza alternatives share one row beside each other, and the common Mafdal service bargain remains below them. The controlled-development, foreign-foothold and ending-foreign-funding rows are separated within Territories. The reserve actions and Gahal appropriation alternatives have their own clear rows.

The independent arrangement checks found:

- No intersecting focus-card rectangles or complete programme footprints, including header clearance.
- Every prerequisite points downward, including the real Territories/Mafdal cross-branch gate.
- Every pair of exclusive alternatives shares a row.
- No semantic change, missing ID or duplicate ID.

The exact final coordinates, origins and equality evidence are recorded in `layout_verification_22.json`. Its semantic SHA256, excluding focus coordinates and group origins, is unchanged before and after arrangement: `2d5da7a2d9c042b91cf440dae9ad36101420ab7386731d576e0226204c5159d6`.

## Final source identity

The browser runner compared these source hashes before and after its complete run. No input changed during verification. The inline visualization is 689,338 bytes.

| Input | SHA256 |
|---|---|
| `tools/israel_v2/design.json` | `aa480fcaf2c1609d7d8531164978a3d2dc0023728331775261f26eae09962706` |
| `tools/israel_v2/fragment.html` | `a7becbbde921207387d613780833fb42ab63b63b5c9a3acb09cbe393cb64f354` |
| Standalone `docs/israel_1970_v2/preview.html` | `5bc26d32886688fcd864471c76303e8b636b7e8aadfa8db4d0b0be1f28855d4c` |
| Inline `israel-1970-v2.html` | `8c9184cf8064ec513dfb099ac116d264511e78441c536061647a06e81a52829e` |
| `tools/israel_v2/focus_layout.py` | `04b7844fde9603ce30f37a1204ee9086e8fc615f7235e83d37b8b5f7301a1e42` |

## Complete browser verification

The final `node tools/israel_v2/verify_preview.cjs` run passed. Detailed results are in `browser_validation.json`.

- 57 responsive programme views: all nineteen programmes at widths 320, 736 and 1024 pixels.
- 213 actual pointer focus inspections, each showing the correct title and the complete supplied Effects rows.
- Zero visible Decision unlocks in those 213 Effects inspections. Zero normal Programme-details sections exposing implementation notes.
- All 213 native focus cards and 244 edges retained across programme navigation. Every image loaded and all party programmes remained inspectable.
- Zero card collisions, routed-connector/card intersections, off-row exclusive alternatives or overflowing titles. Twelve gutter or row-gap detours preserve the real prerequisite logic.
- Actual pointer dragging and the actual zoom buttons worked.
- Every programme reached a fully visible final row through real downward-navigation controls at every tested width. Return to the opening row passed whenever continuation was required.
- All three overview sizes passed with zero overlapping or clipped group labels. Starting conditions and the complete programme index remained available.
- Initial selection correctly opened Mafdal's Negev survey focus at 74% scale, labelled Version 2.2 and Design proposal / Not installed.

The first complete 213-focus run exposed only overlapping Arsenal and Diplomacy overview labels at 736 and 1024 pixels. Moving the Diplomacy overlay eight pixels horizontally resolved that display issue without changing focus data, coordinates or logic. The entire browser suite was rerun after rendering that correction and passed with the hashes above.

## Visual inspection

Current browser screenshots include `preview-default.png`, `preview-mafdal-choice.png`, `preview-settlements.png`, `preview-territories-foreign.png`, `preview-territories-close.png`, `preview-alignment-deep.png`, `preview-gahal-deep.png`, `preview-mafdal-deep.png` and `preview-overview.png`.

The Mafdal opening presents the three land-policy alternatives together with native focus medallions and gold titlebars. The selected Negev focus shows concrete benefits, costs and requirements in the right-hand inspector. The Territories continuation shows all four foreign-foothold focuses together and the corresponding four ending-funding focuses below them. The West Bank inspector exposes Israel's numbers, the actual host's numbers, state penalties and the Palestinian consequences directly. The ending-funding view shows the removed advantages, recurring savings and mirrored relief numerically, while retaining the final reopening focus lower in the canvas. No technical Programme-details section appears.

The overview was also visually checked by the main reviewer after the targeted overlay correction. The older `preview-gahal.png` is a Version 2.1 historical image and is not the current initial view.

## Native presentation and evidence limits

The supplied MD 2.0.3 national-focus GUI was inspected directly in the preceding layout review: native container 165 x 128 pixels, grid 96 x 130 pixels, title field 147 x 20 pixels and font `hoi_16mbs`. The external proposal retains native artwork but uses 147 x 142 focus bounds, 82 x 178 preview units and a Georgia font approximation. All cards remain in a single pannable canvas; programme selection changes the camera rather than hiding content. A readable 74% minimum scale and downward continuation expose the deep branches without reducing the full tree to unreadable miniature titles.

This evidence establishes preview geometry, navigation, complete supplied-effect visibility and the absence of Decision unlocks in the rendered Effects. These are browser-rendered design previews, not HOI4 screenshots. The review does not execute rewards or establish native modifier validity, gameplay balance, multiplayer stability, save/reload behaviour or rehost stability. It does not address an existing game crash.

Provenance: the coordinate arrangement, renderer changes, checks and review were authored for IMPERIA COLD WAR with Codex. Existing native images were reused from project, MD and Imperia assets. Individual original authors, separate licences or permissions remain unknown where inherited records do not identify them. Existing credits and licences continue to apply; see `IMPERIA_COLD_WAR_NOTICE.md` and the current design provenance. No raster artwork was generated or retouched by this task.
