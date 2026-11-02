IMPERIA COLD WAR

# Argentina 1970 runtime layout review

## Scope and evidence

Independent layout and presentation review of the approved Argentina 1970 tree after compilation. Compared `tools/argentina_1970/runtime_design.json` against `common/national_focus/COLDWAR_ARG_1970_focus.txt` and checked the immutable approval source `tools/argentina_1970/approved_design.json` (SHA-256 `bbfa7337ba2677c7f3939a09e1aa3b456caad8966dbf8d03369d262483006012`). Inspected the full-tree overview and native-scale chapter views in `docs/design/COLDWAR_ARG_1970/preview-overview.png`, `preview-pj.png`, `preview-military.png`, and `preview-falklands.png`; independently rendered the current concept HTML in Playwright. The concept HTML is a browser preview, not an HOI4 screenshot.

The browser preview's node presentation and geometry fields (IDs, English titles, icons, groups, absolute positions, prerequisites and exclusions) match all 299 runtime-design entries. It therefore remains a faithful layout view of the emitted tree for those fields. I did not modify the generator, game code, design input, or preview.

## Structural comparison

| Check | Result |
|---|---:|
| Approved, runtime-design, and emitted focus count | 299 each |
| Missing or extra emitted focus IDs | 0 |
| Relative anchor/offset mismatches | 0 |
| Recursively resolved absolute-position mismatches | 0 |
| Prerequisite-group mismatches | 0 |
| Exclusion-relation mismatches | 0 |
| Missing/cyclic anchors | 0 |
| Party-dependent `allow_branch` entries | 0 |
| Shortcuts | 8, each targeting an existing section root |

Resolved bounds are x=2..222 and y=0..36 across 22 sections. The compiled file retains the approved relative anchors and offsets, including all OR/AND prerequisite grouping. Party programmes remain in the visible tree regardless of government; the absence of `allow_branch` agrees with the project requirement. The eight shortcuts target military, PJ, UCR, MID, institutions, economy, defence, and diplomacy roots.

## Geometry and visual findings

The target `interface/nationalfocusview.gui` uses a 96 by 130 focus grid, a 165 by 128 focus item, and a 147 by 20 title field in `hoi_16mbs`. The preview labels its grid at 96 by 130. Its full overview keeps all 22 sections distinguishable while compressing the full 221-column canvas to fit; it is useful for structure, not title inspection. The PJ and military views show connected neighboring cards at readable scale. In the inspected alternatives, exclusion rails pass through open gaps between the focus cards rather than through icons or title bars. The root-to-choice connectors and short branch continuations are legible. The Falklands concept image shows the upper branch only, so the lower section extent was checked from resolved coordinates and the full-tree image rather than inferred from that crop.

The preview's reported geometry record (`BROWSER_QA.json`) covers 342 prerequisite links, 299 focus inspectors, 16 government variants, and reports no card overlaps, exclusion-art collisions, title overflows, or missing art. That record belongs to the browser concept preview, not the HOI4 engine. The current emitted coordinates and visible titles/icons match its design data, but the report is not evidence of native connector routing or in-game GUI behavior.

No concrete focus-ID collision or card/title clipping issue was found in the inspected preview. The 8-column navigation set is useful for opening major sections in a tree this wide. Initial focus is `COLDWAR_ARG_army_directives`; opening viewport and shortcut scrolling have not been checked in game.

## Source, preview, and engine boundary

- **Source:** the approved design is hash-pinned above. Runtime design preserves the approved IDs, positions, titles, icons, prerequisite groups, and exclusion relations. Static parsing of emitted focus blocks confirms the same positions and logic.
- **Preview:** the supplied full overview and chapter views are composed in the browser with native-style focus art and titlebars. The page itself labels font and connector routing as approximations. Event art's `native-window-donor-composed.png` is a donor-composed QA preview, not a live game screenshot; its notice says the selected images are illustrative stock art and makes no claim that they document specific Argentine events.
- **Engine:** no HOI4 screenshot or in-game hover/navigation test was part of this review. Native rendering, focus-link routing, shortcut behavior, clipping and gameplay remain engine checks.

## Reference and verdict

The geometry reference is the installed Millennium Dawn focus UI and the measured profile in `docs/design/COLDWAR_ARG_1970/md_reference_profile.md`, sampled 2026-11-01 from Generic, France, Russia, and Germany trees. The measured 96 by 130 spacing, 165 by 128 item, and 147 by 20 title bounds are recorded in the profile. They are local UI measurements, not claims about universal engine limits.

**Layout verdict:** the emitted positions, prerequisite groups, exclusions, and party-branch visibility match the approved design. The card-level browser preview shows no layout issue requiring a geometry change. Treat this as a static and visual-preview review only; engine rendering remains unverified.
