IMPERIA COLD WAR

# Argentina 1970 concept: layout review

## Scope and evidence

Read-only review of the complete concept snapshot on 2026-11-01. Inspected `preview-overview.png`, `preview-military.png`, `preview-pj.png`, `preview-falklands.png`, `preview-agreement.png`, and `preview-mobile.png`. Independently resolved all 299 entries in `proposal_graph_fixture.txt` and compared them with the current `COLDWAR_ARG_design.json`: 299 parsed, 299 matched, zero coordinate mismatches, and zero duplicate focus IDs. No builder was run or edited. No game engine is installed, so this review covers the concept preview only.

The geometry audit records 299 focuses in 22 clusters, 20 bilateral agreement previews, and world bounds x=2..222, y=0..36. Native basis is 96 by 130 per grid unit. The preview says its font and connector routing are approximations. BROWSER_QA.json records 342 prerequisite links with no detected card collisions or overlaps across 16 government variants, one title overflow (`Fund the Los Gigantes Mine`), no missing art, and no engine test. Confirm the final title after its planned shortening and refresh QA output before approval.

## Full layout and boundaries

All 22 chapter roots have consistent section positions and the overview keeps the political programmes, shared institutions, economy, defence, science, partner agreements, and Falklands visually distinct. The two political rows occupy y=0..16 and y=18..30. Their cluster edges leave clear channels at the overview scale. Shared institutions span x=130..140 and y=0..18. Economy spans x=148..160 and y=0..24. Defence spans x=168..180 and y=0..16. Science sits below defence at x=170..178, y=20..36, with a four-row vertical gap from the defence bottom. Diplomacy spans x=188..200 and y=0..20. Falklands spans x=210..222 and y=0..24. These footprints do not overlap, and the overview shows the intended chapter grouping without one sector intruding into its neighbours.

No prerequisite or exclusion edges cross between clusters in the current JSON. That keeps the full tree's major sector gaps open. Shared requirements such as membership, active agreements, and scenario rules appear in the inspectors rather than long cross-tree links. Keep this boundary pattern if later edits add cross-sector gates. If an approved gameplay dependency must be drawn across sections, inspect it in the full overview and at normal scale with all party routes visible.

Section counts and resolved extents:

| Cluster | Count | x range | y range | Root |
|---|---:|---:|---:|---|
| Institutions | 17 | 130..140 | 0..18 | Governability Crisis |
| FFAA | 18 | 2..12 | 0..10 | Command Directives |
| PJ | 20 | 20..30 | 0..16 | Negotiate the Social Pact |
| UCR | 16 | 34..46 | 0..16 | Restore the Committees |
| MID | 12 | 52..60 | 0..14 | The Development Agenda |
| PCI | 12 | 68..76 | 0..14 | Publish the Real Budget |
| PD | 10 | 84..92 | 0..12 | A Cabinet from Cuyo |
| PDC | 10 | 100..108 | 0..12 | A Christian Social Cabinet |
| PCA | 12 | 116..124 | 0..14 | A Workers' Front |
| Montoneros | 10 | 4..12 | 18..30 | Neighborhood Committees |
| PRT | 10 | 20..28 | 18..30 | A Workers' Congress |
| CGTA | 10 | 36..44 | 18..30 | A Shop-Floor Mandate |
| 62 Organizations | 10 | 52..60 | 18..30 | The Union Mandate |
| Ateneo | 8 | 68..76 | 18..28 | The Athenaeum Cabinet |
| UDELPA | 8 | 84..92 | 18..28 | Order and the Republic |
| SRA | 8 | 100..108 | 18..26 | The Exporting Countryside |
| PSD | 10 | 116..124 | 18..30 | A Socialist Coalition |
| Economy | 23 | 148..160 | 0..24 | National Economic Survey |
| Defence | 19 | 168..180 | 0..16 | A Joint Readiness Review |
| Science | 13 | 170..178 | 20..36 | The CNEA Mandate |
| Partners | 20 | 188..200 | 0..20 | San Martin Palace Desk |
| Falklands | 23 | 210..222 | 0..24 | A Sovereignty Dossier |

The roots are consistently readable in the overview. The FFAA, PJ and Falklands chapter views show a centered root, short vertical spine, and evenly spaced choices. No focus box overlap is visible in the requested views. The overview is intentionally too zoomed out for title inspection, so the normal-scale chapter screenshots remain necessary.

## Visual findings by requested view

- **Overview:** The major branches fit in a single wide canvas, with recognizable section labels and no apparent overlap between the 22 chapter footprints. The political tiers use generous horizontal breathing room. Keep the overview as a structural map, with chapter views carrying title and icon detail.
- **Military:** The root and three-way alternative row are centered and well spaced. The dashed red exclusion rail visibly passes through the central `National Industrial Capital` icon and the two flanking icon areas. It does not collide with prerequisite rails, but the art intersection is distracting. Route exclusion links in the empty strip below or above the icon art, or use a non-crossing alternative marker in the preview. Check native engine routing when available because the current renderer labels this routing approximate.
- **PJ:** The root and three programme choices are symmetric. The six links from the three-way OR group lead into the two leadership arrangements; they appear readable in the current normal-scale view. The red exclusion dashes again cross focus art at icon height. Move the exclusion path away from the artwork. This visual finding applies to other same-row exclusive choices, including the Falklands view.
- **Falklands:** The sovereignty root is centered above the reservation and coercion alternatives, and the alternatives are far enough apart for their artwork and titles. The red exclusion path crosses both icons. Move it to a clear horizontal connector channel. The rest of the branch continues below the current viewport, so this image does not verify the complete 23-focus cluster's lower edge.
- **Agreement:** The inspector clearly shows the event, both countries' full prospective setup and recurring costs, recurring income, named spirits, signed modifier values, and bilateral conditions. The selected `Overseas Trade Missions` root is clipped at the top of the tree viewport: the upper part of its icon falls behind the viewport edge. Add top camera padding or shift the initial tree view down enough to show the full root art and state bar. This does not obscure the agreement effects panel.
- **Mobile:** The controls, tree, legend, and inspector stack vertically without page-width overflow. The focus title and effect details remain readable. The selected root and child path are visible. As in desktop, the horizontal red exclusion rail passes through focus art. The tree itself remains wider than the handset and should remain a pannable canvas; do not compress native focus spacing to fit the full tree at once.

## Prerequisites and mutually exclusive choices

The current generated preview resolves the previously reviewed multi-parent areas cleanly. `peron_arbitration` and `cabinet_rules` have a symmetric three-way fan-in and separate, well-spaced child positions in the PJ view. The UCR four-way alternative at `republican_school` does not produce a visible line-through-card collision in the current preview. The institutions choices are centered around their OR joins. The normal-scale images support the grouping and spacing; an engine session is still needed to confirm real connector routing.

The earlier duplicate-ID report was incorrect. The current builder and design snapshot have one `rural_cabinet` focus in SRA; the PDC root is `christian_social`. Independent fixture comparison found zero duplicate focus IDs. No duplicate-ID issue remains in this snapshot.

## Review status

Layout looks clear across all current clusters and all six requested screenshots, subject to the two visible presentation fixes: route red mutual-exclusion lines outside focus art, and add top margin to the selected agreement root. Check the final shortened title and refresh the QA record. No gameplay or prerequisite change is recommended by this geometry review. Native rendering, engine-scale connector routing, and in-game navigation remain unverified until the project can be opened in HOI4.

## Final visual recheck

The regenerated military, PJ, and agreement screenshots were visually rechecked after the layout adjustments. The mutual-exclusion rails now stop in the gaps between cards and no longer cross focus art or title bars in the sampled military and PJ branches. The selected `Overseas Trade Missions` focus is fully visible with clear top margin in the agreement view. Its two-country acceptance effects remain fully readable in the inspector.

The latest `BROWSER_QA.json` reports 342 prerequisite links, no card collisions, no exclusion-art collisions, no title overflow, no missing art, no fixture errors, and no responsive page overflow at 1180, 736, or 360 px. It inspected all 299 focus inspectors, 16 event inspectors, and 20 agreement inspectors across 16 government variants. The mine title was shortened to `Fund the Uranium Mine` and the latest title-overflow result is empty. The 299-focus, 22-group model check also reports no prerequisite-history errors and world bounds x=2..222, y=0..36.

**Final layout verdict:** the reviewed concept preview has no remaining geometry or card-level visual issue requiring adjustment. The overview, chapter boundaries, choice spacing, agreement inspector, selected-focus framing, and mobile presentation are clear at the inspected scales. The preview remains an approximation of native fonts and connector routing. HOI4 engine rendering and gameplay are still unverified because the engine is unavailable.
