# IMPERIA COLD WAR: Israel Version 2.0 independent layout review (historical)

Current expanded-design verification: see [LAYOUT_REVIEW_21.md](LAYOUT_REVIEW_21.md). The record below concerns the earlier 138-focus draft and is retained as historical evidence, not the current 192-focus result.

Scope: the proposed 138-focus, 19-programme design, including eleven party programmes. No loaded focus, GUI, script, localisation or game-history file was changed by this layout work. The preview is a design proposal, not a screenshot from HOI4.

## Source and representation

The supplied MD 2.0.3 `interface/nationalfocusview.gui` was inspected directly. Its native focus container is 165 x 128 pixels, focus spacing is 96 x 130 pixels, and the title field is 147 x 20 pixels using `hoi_16mbs`.

The external inspector uses native focus artwork with 147 x 142 pixel focus bounds, a 147 pixel multiline title, 82 x 178 preview grid units and Georgia as a font approximation. This deliberately preserves readable titles in the external view. It does not certify final engine coordinates, native link routing or HOI4 typography. Party availability is displayed as a requirement; all parties remain inspectable in the proposed map.

Reviewed data SHA256: `c46b48eb7e5ae34512407482a53715f5309ca00b055fd8041caec80dfce75a3a`.

Final fragment SHA256: `bbb6406fd91f5331e01ea8aa55e7ec0694b9bf09a747213f2eb8734e86b13b83`.

Final rendered inline source SHA256: `696c4710c32ec94364a4f3de6a21db122f87358dd6262bee27881ea8d03087c8`.

## Confirmed findings and corrections

The initial automatic midpoint routing crossed unrelated cards at nine connections. Clear row-gap and vertical-gutter routes now preserve the exact prerequisite graph and avoid those intersections. The final 156 prerequisite edges include two gutter detours. The main author also put the civilian-spillover and defence-priority alternatives on the same row, allowing the exclusive-choice indicator to remain visible.

Initial 128 pixel labels clipped fourteen long titles. Widening the title field to the native title-field width of 147 pixels resolved every measured title overflow without reducing the font. Increasing the desktop map viewport to 760 pixels keeps the Alignment finale visible above the map footer. Overview programme titles use short, readable labels with complete names in accessible tooltips and the programme index. Removing repeated subtitles keeps the overview compact.

## Verification

`node tools/israel_v2/verify_preview.cjs` passed on the current 138-focus data:

- 57 responsive branch views: every programme at widths 320, 736 and 1024 pixels.
- 138 actual pointer inspections, with each focus centred by camera movement before the click. Every inspector showed its exact title and complete supplied effects.
- All 138 focus cards and all 156 prerequisite edges retained in every branch view. No party-dependent hiding was introduced.
- Every native focus image loaded.
- Zero focus-card collisions, zero routed connector/card intersections, zero off-row exclusive pairs and zero measured title overflows.
- Starting conditions and complete overview navigation checked at all three widths.

The final redundant historical-basis caption was removed after the full pass. A bounded `--refresh` check then passed unchanged geometry, title bounds and screenshot rendering; its evidence is `display_refresh.json`. The full prior click/responsive evidence remains separately preserved in `browser_validation.json`.

The reviewer visually inspected the updated `preview-alignment.png`, `preview-overview.png` and `preview-settlements.png`. The complete Alignment programme and finale are visible, overview labels no longer cover the focus clusters, and controlled development and unilateral foreign footholds remain separate paths. The larger army-industrial branch can require normal pan navigation when a readable scale is retained. This is intentional navigation, not removal of its outer nodes.

## Limits and provenance

These checks establish external preview geometry, interaction, label readability and supplied-effect visibility. They do not execute rewards, validate modifier scopes in HOI4, repair the existing native crash or establish multiplayer, save/reload or rehost stability.

The renderer, browser checks and this review were authored for IMPERIA COLD WAR with Codex. Native icon images were reused from the existing project preview, ultimately sourced from MD, Imperia and inherited assets. Individual original authors or separate permissions are unknown where the source records do not identify them. Existing credits and licence notices remain applicable; see the project root `IMPERIA_COLD_WAR_NOTICE.md` and the Version 2.0 source/provenance records. No raster artwork was generated or retouched by this layout task.

## Final author integration check

The final expanded-design browser pass reports 57 responsive branch views, 213 actual pointer inspections and 244 prerequisite edges. No card or routed-connector intersections, off-row exclusions or measured title overflows remain. Deep-branch navigation is checked separately in the browser report. The composed views and the independent layout review remain distinct from native gameplay evidence.

Final data SHA256: `aa480fcaf2c1609d7d8531164978a3d2dc0023728331775261f26eae09962706`.

Final fragment template SHA256: `a7becbbde921207387d613780833fb42ab63b63b5c9a3acb09cbe393cb64f354`.

Final inline preview SHA256: `8c9184cf8064ec513dfb099ac116d264511e78441c536061647a06e81a52829e`.
