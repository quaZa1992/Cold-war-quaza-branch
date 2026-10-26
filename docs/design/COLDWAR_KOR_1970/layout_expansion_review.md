# KOR 1970 expansion — independent layout review

Read-only review of the resolved 298-focus concept and its regenerated PNG previews. No design, generator, or game files were changed. Review focuses on native-grid card spacing, lower-party/top-extension clearance, three-way connectors, the economy/KJP boundary, and tree navigation.

## Reviewed snapshot

The current resolved JSON contains 298 focus cards in 14 groups, with bounds x=3..86 and y=0..27. It declares eight shortcuts, including the new transition branch. JSON SHA-256: `C94210A3DD3580AD5CECBCD62E35F53CC0EBF8CFFDAF49A1D7F4ABED5C2DC598`.

All preview images below were regenerated on 2026-10-24 at 19:42. SHA-256 values identify the exact files reviewed:

| Preview | Bytes | SHA-256 |
|---|---:|---|
| `COLDWAR_KOR_entire_tree.png` | 964,329 | `3773262229E1B4956640F699CB846707602642B3CB7B12899AB5BEA1A96C54C7` |
| `COLDWAR_KOR_Democratic_Transition_detail.png` | 475,636 | `4A8D1392347733F15D612E2E6F5938ABDCB393F31A7A6E50814A1946061091BE` |
| `COLDWAR_KOR_Economy_detail.png` | 418,470 | `DA17921984AB35618394F0DC8FE5F8B68ECE7E5506A4244E84387AC3A9D6E7E7` |
| `COLDWAR_KOR_Defence_detail.png` | 346,546 | `4379E3F4570B1C3F0DFED9ABA79B438844B4959767B79718D5B2D1D9787D81E9` |
| `COLDWAR_KOR_Kim_Jong_pil_detail.png` | 169,705 | `BC9218325912E31A7FBF8EC2079E8E9891BCC4281D27E8061845E36A3DA846EC` |
| `COLDWAR_KOR_DRP_detail.png` | 301,581 | `2901BF4B98EE6939242F307B5BD44B38E12DA7B1E97A89B122E571ECA51FF7B0` |

Previews state that font, symbol placement, connector routing, and states approximate engine presentation. Native comparison remains the measured 165×128 px item, 96×130 px pitch, and 147×20 px title field in `interface/nationalfocusview.gui:446-493,573-585`; the donor KOR and Russian spacing evidence is in [`md_reference_layout.md`](md_reference_layout.md).

## Geometry and graph checks

| Check | Result |
|---|---|
| Node count / groups | 298 / 14 |
| Unique grid cells | 298; no duplicate coordinates |
| Card-box intersections | None using native 165×128 px boxes on the 96×130 px grid |
| Missing prerequisite/exclusion references | 0 |
| Reciprocal exclusion declarations | 0 asymmetric pairs |
| Structurally reachable focus cards | 298 of 298 under OR-within-prerequisite-block / AND-across-block semantics |
| Cross-group prerequisite edges | 0; each programme is self-contained in its visual band |
| Shortcut capacity | 8/8, including “From military rule to democracy” |

### Lower party roots and top extensions

The upper-party additions end at y=10..12. The lower-party roots begin at y=14, so the nearest same-column pair is two grid rows apart: 260 px center-to-center against a 128 px card height, leaving 132 px edge clearance. The DRP/USP pair and Army/Security pair are the tightest vertical alignments; the preview shows no card, icon, or title overlap. The remaining NDP/Minjung and Reform/RPR pairs have at least three to four rows of separation. No cross-group prerequisite connectors traverse these shared x-columns, so the new local extensions do not route through lower-party roots.

The entire-tree preview shows 14 clear bands and a well-separated transition section at the right. At whole-tree fit, labels are too small to read, as expected for this canvas size; the normal-scale detail views make the branches legible. The initial view remains DRP. The eight shortcut list retains four main political/navigation targets (DRP, transition, Two Kims, Army/DJP) plus economy, defence, foreign policy, and Korean question; NDP and the five lower/alternate party groups remain reachable by panning from nearby roots, subject to the native eight-slot cap.

### Three-way exclusion and connector routing

The three-way choices use safe native-sized gaps: economics at x=43/45/47,y=16; defence at x=52/54/56,y=13; and constitutional models at x=80/82/84,y=8. Adjacent outcomes are two grid columns apart, yielding 192 px center separation and about 27 px between 165 px item bounds. Card rectangles do not collide.

There is a connector-routing hazard in each three-way row. The JSON correctly declares every alternative mutually exclusive with both others, but the preview draws all three pairwise orange lines. The outer line runs from the left card to the right card through the middle choice: `electronics_priority`↔`shipbuilding_priority` crosses `machinery_priority`; `air_cover_priority`↔`counterbattery_priority` crosses `escort_priority`; and `presidential_democracy`↔`consensus_presidency` crosses `parliamentary_democracy`. In the inspected PNGs, the middle card artwork/title masks most of the outer segment and the visible adjacent exclusion markers remain understandable. This is a renderer approximation, not proof that Clausewitz routes the native connectors the same way. Keep all six reciprocal declarations in the data; for a clearer preview, draw only the two adjacent links for a complete three-way exclusion set, or route the outer link around the row.

Other fan/join paths are visually clean at normal scale. In the transition view, the first three policy tracks (x=78/82/86) intentionally all feed `Constitutional Talks`; they are not a mutually exclusive choice. Their four-column spacing provides breathing room, while the single OR choice later uses the narrower x=80/82/84 row. The `Parliamentary Audits` join collects either officer-retirement option plus the Constitutional Review milestone; the long path from the court focus is visible but crosses no unrelated card. These are approximated browser routes and still need an engine view during implementation.

### Economy row 17 and KJP/sector edges

`Industrial Standards` at `(45,18)` has one OR prerequisite block containing all three production outcomes at `(43,17),(45,17),(47,17)`. It therefore unlocks from any one specialization, matching the three-way choice; the join is centered and visually balanced. Its continuations at `(44,19)` and `(46,19)` stay inside the economy band. The moved KJP root is `(54,19)`: it is at least eight grid columns from the nearest economy continuation (768 px center-to-center), with roughly 603 px between card edges. The KJP tree remains internally connected through `(53..55,20..27)` and does not collide with economic cards or their connectors. No prerequisite links cross from economy to KJP.

The Defence three-way row follows the same readable pattern and its three follow-ups join at the central readiness audit. The preview shows no connector crossing a different focus card beyond the outer-pair exclusion links called out above.

## Presentation and navigation notes

- Continuous-focus panel position `(7100,3300)` is clear of nodes in the new bounds: the transition band ends above it, while KJP ends far to the left. The full overview places it in open lower-right canvas area.
- `Constitutional Authority`, `Defend Civilian Command`, `An Independent Inquiry`, `A Consensus Presidency`, `Submit the Constitution`, and `Accountable Intelligence` visibly truncate in the 147 px title field in the transition detail. Shorten titles if the final native focus cards should show the full names without relying on hover text.
- The title field and connector routing remain renderer approximations; actual HOI4 font clipping, focus-link routing, shortcut behavior, and panel placement have not been verified in-game.

## Recommended follow-up

The current layout passes card geometry, coordinate uniqueness, reference integrity, structural reachability, and shortcut-capacity checks. The only visible structural presentation issue is the outer exclusion connector crossing the center card in each three-way choice. Retain the native exclusion data and make the preview route easier to read; confirm the true connectors in-game when the design is implemented. The transition root is a separate, shortcut-addressable section with no cross-group prerequisite links; that keeps the tree clean and compact, while its actual scenario/crisis eligibility must be enforced by the focus availability guards rather than inferred from its position.

## Final preview pass — shortened transition titles and exclusion links

This final pass supersedes the initial-pass findings above about transition title truncation and visible outer exclusion links. Coordinates are unchanged; the current JSON is 298 nodes, 14 groups, bounds x=3..86/y=0..27, and exactly 8 shortcuts. Current JSON SHA-256 is `E1802C486E497E15EB0C27D1BAD9D4602C68AB06C33F81CE3255AC7BE584B633`.

The latest captures were generated at 19:54 on 2026-10-24 and visually inspected at native-detail scale:

| Latest preview | Bytes | SHA-256 |
|---|---:|---|
| `COLDWAR_KOR_entire_tree.png` | 964,179 | `7AA591B649365414604C83E7D898DEB9D546FE7BC327AE160822142155593114` |
| `COLDWAR_KOR_Democratic_Transition_detail.png` | 474,589 | `A757083EB385D4A475ACD844C608F3848D864B2C87A8C895C8B9656A1B92A42D` |
| `COLDWAR_KOR_Economy_detail.png` | 418,470 | `DA17921984AB35618394F0DC8FE5F8B68ECE7E5506A4244E84387AC3A9D6E7E7` |
| `COLDWAR_KOR_Defence_detail.png` | 346,546 | `4379E3F4570B1C3F0DFED9ABA79B438844B4959767B79718D5B2D1D9787D81E9` |

The shortened transition labels now fit the 147 px name field in the detail preview: examples include “Constitutional Review,” “Uphold Civil Command,” “Independent Inquiry,” “Consensus Presidency,” “Submit the Charter,” “Security Accountability,” “Phased Retirement,” and “Labour Bargaining.” I saw no remaining ellipsized labels in the transition capture. The full overview shows the same distinct political, national, lower-party, KJP, and transition bands with no visible card collisions; full-tree labels remain too small to read at overview scale, so normal detail views are still needed for content review.

The updated renderer suppresses the outer pairwise line for complete three-way exclusion sets. In the newest economy, defence, and transition captures, only adjacent orange exclusion links are visible, and they no longer cut through the center choice. I rechecked that the resolved JSON still declares every alternative mutually exclusive with both other choices in each set; only the preview routing changed. The focused details show the new presentation clearly. Native Clausewitz connector behavior remains unverified, as indicated in the image captions.

No new overlap or clearance issue appeared. The lower-party/top-extension spacing and economy-to-KJP clearance remain as recorded above; the continuous-focus panel remains in an open lower-right area of the full overview.
