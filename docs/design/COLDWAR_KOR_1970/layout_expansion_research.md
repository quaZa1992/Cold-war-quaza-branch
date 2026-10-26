# South Korea 1970 focus-tree expansion: layout research

Read-only spatial proposal for expanding the current 206-focus concept toward the 300-focus ceiling. This report does not edit the design or its generator. The current `COLDWAR_KOR_design.json` remains the position source for previews; the builder’s `enrich → refine → declare` pipeline intentionally resolves authored positions through review fixes.

## Measured native grid and navigation limits

The donor is Millennium Dawn Workshop `2777392649`, version `2.0.2`, `supported_version = "1.19.*"` (`descriptor.mod:1-17`). Its South Korea tree has 219 focus cards; Russia has 806 and Generic 158. The relevant measurements and native examples are recorded with file:line evidence in [`md_reference_layout.md`](md_reference_layout.md).

| Native rule | Measurement / example | Evidence |
|---|---|---|
| Focus card | 165×128 px | Donor and target `interface/nationalfocusview.gui:446-449` |
| Grid pitch | 96×130 px; one column is too close for two cards | `nationalfocusview.gui:573-585` |
| Safe two-way fork | sibling centers two grid columns apart; 192 px apart, about 27 px card-edge clearance | KOR aircraft alternatives at relative x=-10/-8, y=2, with join at x=-9,y=3; `05_south_korea.txt:68-80,140-152,200-212` |
| Safe three-way row | alternatives at x=-1,+1,+3 (two-column intervals), for a four-column total span | Russia economic alternatives resolve to `(74,8),(76,8),(78,8)`; `05_russia.txt:552-694` |
| Prerequisite grouping | repeated `prerequisite` blocks are AND; `focus` entries inside one block are OR | KOR aircraft join at `05_south_korea.txt:201-212`; Russia's three outcomes have two shared prerequisite blocks at `05_russia.txt:552-678` |
| Navigation | eight vertical shortcut slots maximum | Target/donor `nationalfocusview.gui:370-384`; current JSON has exactly 8 shortcuts |

The KOR tree uses independent political and national roots: armed forces `(0,0)`, state/politics `(27,0)`, diplomacy `(61,0)` (`05_south_korea.txt:19-38,1541-58,4972-89`). Its political entry fans to outlook alternatives at root-relative `(-4,+1)` and `(+4,+1)` (`05_south_korea.txt:1560-79,3533-59`). Russia’s much larger tree similarly reserves a distinct band for Putin’s route, rooted at `(75,1)` (`05_russia.txt:51-79,107-153`). These examples support separate, navigable programme bands rather than making every continuation a single narrow trunk.

## Current concept footprint

The current design JSON has 206 nodes in 13 groups. Its resolved bounds are x=3..73, y=0..25. The eight shortcuts target DRP, NDP, Two Kims, Army/DJP, national development, defence, foreign policy, and the Korean question (`COLDWAR_KOR_design.json:15138-15195`). The initial view targets the Developmental State. Current group bounds:

| Group | Anchor | Nodes | Current x / y bounds |
|---|---:|---:|---:|
| DRP | (4,0) | 18 | 3..5 / 0..10 |
| NDP | (12,0) | 14 | 11..13 / 0..8 |
| Two Kims / reform | (23,0) | 18 | 18..28 / 0..8 |
| Army / DJP | (34,0) | 18 | 33..35 / 0..10 |
| USP | (4,14) | 14 | 3..5 / 14..22 |
| Minjung / student and independent left | (13,14) | 14 | 9..17 / 14..18 |
| RPR | (23,14) | 12 | 22..24 / 14..21 |
| Security directorate | (34,14) | 12 | 33..35 / 14..21 |
| Economy | (45,0) | 24 | 44..46 / 0..14 |
| Defence | (54,0) | 20 | 53..55 / 0..11 |
| Foreign policy | (63,0) | 14 | 62..64 / 0..8 |
| Korean question | (72,0) | 16 | 71..73 / 0..9 |
| KJP | (45,18) | 12 | 44..46 / 18..25 |

These columns leave a usable next band below y=25. The current continuous-focus panel is positioned at pixel `(5500,3500)` (`COLDWAR_KOR_review_fixes.py:157-161`); that position falls over the planned extension row at x≈57,y≈27 and should be moved below/right of the expanded card bounds.

## Compact expansion proposal: 92 additional cards

Target 298 cards (206 + 92), reserving two slots below the hard 300-focus cap. Add 60 cards that continue every existing party and national sector, then a distinct 32-card transition programme to the right. The coordinates below are proposed absolute grid cells; builder-authored offsets can resolve them through the existing refinement pipeline.

### Sector continuations: 60 cards

For five-card groups, place an entry at `(C,26)`, two mutually exclusive choices at `(C−1,27)` and `(C+1,27)`, an OR join at `(C,28)`, then a two-focus continuation at `(C,29)` and `(C,30)`. This is a 3-column-wide cluster with native 192 px choice separation. The entry should follow the existing group’s actual terminal policy by a deliberate prerequisite; if the group has alternative endings, use one OR prerequisite group rather than requiring both sides of an exclusive fork.

For four-card groups, use an entry at `(C,34)`, alternatives at `(C−1,35)` and `(C+1,35)`, and an OR join at `(C,36)`. This preserves one choice and an explicit common continuation within a small footprint. Each lower band is separated from the upper continuations by four empty rows; this also prevents cards that share a column (DRP/USP, reform/RPR, Army/security, economy/KJP) from colliding.

| Existing sector | Added | Proposed center / rows | Spatial purpose |
|---|---:|---|---|
| DRP | 5 | C=4, y=26..30 | Continue state-led growth through institutional succession and a policy fork |
| NDP | 5 | C=12, y=26..30 | Extend parliamentary and civil-service settlement into regional/social policy |
| Two Kims / reform | 5 | C=23, y=26..30 | Extend civilian reform with a distinct coalition or electoral branch |
| Army / DJP | 5 | C=34, y=26..30 | Continue controlled government into either managed opening or security consolidation |
| Economy | 5 | C=45, y=26..30 | Add a second investment/productivity choice beyond the existing export/energy spine |
| Defence | 5 | C=54, y=26..30 | Add a doctrinal choice followed by readiness/logistics continuation |
| Foreign policy | 5 | C=63, y=26..30 | Extend alliance/autonomy choices into parallel diplomacy and trade outcomes |
| Korean question | 5 | C=72, y=26..30 | Continue contacts and settlement into alternative security/peace institutions |
| USP | 4 | C=4, y=34..36 | Add social-democratic civic and economic continuation |
| Minjung / independent left | 4 | C=13, y=34..36 | Add a non-revolutionary versus independent-left policy resolution |
| RPR | 4 | C=23, y=34..36 | Add a state-planning or southern-settlement choice |
| Security directorate | 4 | C=34, y=34..36 | Extend protected planning versus civilian handover |
| KJP | 4 | C=45, y=34..36 | Extend conservative coalition and succession arrangements |
| **Total** | **60** | **x=3..73, y=26..36** | All thirteen existing groups receive meaningful new focus cards |

The y=26..30 and 34..36 rows use only already-established columns, so the existing left/right section balance is retained. A two-way fork in each group follows donor KOR geometry; do not squeeze a three-way choice into adjacent grid columns. If a group’s alternative policy paths need their own continuation before joining, reserve another two grid rows or use a four-column-wide fork.

### Dictatorship-to-democracy transition: 32 cards

Place a cross-party constitutional transition band in the open space to the right of the Korean-question group. Let C=82; use the footprint x=80..84, y=0..21. The current rightmost focus center is x=73, leaving a seven-column gap from the existing edge to the new branch. The branch adds eleven columns to the total tree width and uses existing horizontal space more efficiently than stacking 32 cards beneath every group.

| Stage | Coordinates | Cards | Suggested function |
|---|---|---:|---|
| Transition entry | `(82,0)` | 1 | Available when a real succession/constitutional transition is open |
| Three settlement routes | `(80,1),(82,1),(84,1)` | 3 | Officer-negotiated transition; caretaker compact; opposition-led negotiated transition |
| Route-specific follow-through | each route’s x at y=2 and y=3 | 6 | Two costs/guarantees per route; keep routes mutually exclusive where they truly are alternatives |
| First shared join | `(82,4)` | 1 | One OR prerequisite block over those three route outcomes |
| Constitutional process spine | `(82,5..9)` | 5 | Party legalization, election administration, civilian command, judicial/legislative checks, implementation |
| Institutional settlement choice | `(80,10),(82,10),(84,10)` | 3 | Three constitutionally distinct settlement models, reciprocal exclusions |
| Model-specific continuation | each choice’s x at y=11 | 3 | One immediate institutional consequence per model |
| Second shared join | `(82,12)` | 1 | OR join, not AND across mutually exclusive settlements |
| Democratic consolidation | `(82,13..21)` | 9 | Shared civil liberties, local representation, accountable security, labour mediation, party competition and peaceful transfer |
| **Total** | **x=80..84, y=0..21** | **32** | A substantial but compact path with two consequential choices |

This gives the overall concept 298 focuses, x=3..84, y=0..36. A new transition shortcut would be a ninth destination and would overflow the native vertical shortcut grid. Retain the eight current shortcuts; the transition cluster can be reached from its cross-party prerequisite lines and an overview pan. If later playtests show it is too difficult to locate, replace a shortcut only after choosing which existing destination is less important; do not silently exceed eight.

The transition entry should depend on a single compatible political milestone or one OR prerequisite group containing route-specific predecessor foci. Do not put mutually exclusive party outcomes into separate prerequisite blocks, which would require all of them. Keep actual incumbent, ruling-party and active-constitution gates in `available`/reward guards; drawing connectors alone is not an eligibility test. Current transition-event concepts already distinguish the 1971 contest, 1979 succession, December officer challenge, Gwangju crisis, 1985 opposition reorganization, 1987 direct-election settlement and 1990 coalition talks (`COLDWAR_KOR_review_fixes.py:11-54`). Those event/decision stages can provide the historical receipts for the new focus chain; the tree should not make historical crises automatic or turn coercion into a beneficial shortcut.

## Parallel branches and visual hierarchy

Use the new spatial bands to give society, economy and security genuine parallel continuations. The current graph has strong vertical industrial/economic routes and parallel branches in the political trees, but the 32-card transition band can create a common institutional route while party-specific groups preserve alternatives. A transition focus may open a social, economic or military continuation through prerequisites and availability, but avoid visually wiring every group into one central knot. A few deliberate long links are easier to read than a dense fan of many-to-many lines.

The three-way structures should follow Russia’s measured economics example: outcomes at two-column intervals, all three alternatives mutually exclusive, and a one-block OR join below. Use multiple prerequisite blocks only when multiple independent milestones must all be complete. For the transition choice, select three materially different institutional settlements (e.g. controlled/gradual opening, negotiated presidential democracy, parliamentary coalition settlement) and let the following shared spine carry common constitutional duties. Do not make the named historical outcome inevitable merely because the player has selected one focus.

The proposed transition’s three-wide rows need only 4-column span, not 8: alternatives x=80,82,84 have center intervals of 192 px and card-edge clearance of about 27 px. Its branches continue vertically in their own columns and converge at x=82. Exclusion connectors should be drawn between the endpoint cards through their horizontal gap; actual native routing still needs an in-game check.

## Viewport and preview payload

The expanded x=3..84 bounds put the right edge of the last focus around `84×96 + 165 = 8,229 px` from the grid origin. Move the continuous-focus panel outside that footprint; a preview-safe candidate is pixel position `(8,500,5,200)` (verify actual game placement because the target panel is a GUI coordinate, not a focus-grid cell). This keeps the panel from covering the new political transition or the y=26..30 national extensions. The 8 native shortcuts remain the practical navigation ceiling. Preserve the current starting camera at the Developmental State; a later usability review may choose a transition-oriented starting view for a scenario that actually begins after succession.

`COLDWAR_KOR_preview_data.json` is 1,030,786 bytes: 1.03 MB decimal, under 1 MiB. `COLDWAR_KOR_render.py:228-235` currently embeds the entire compact design object—including policies and consent contracts—into the standalone HTML, then also writes a full pretty JSON copy. Keep the full resolved JSON as the source of truth. Generate the inline preview payload as a small projection containing only what the UI uses (focus ID/title/group/position, visual prerequisites/exclusions, icon family, shortcuts, and display availability); leave reward mechanics, audit evidence, consent contracts and policy descriptions in the full JSON. This reduces duplicated audit payload while retaining complete data for review and regeneration. Keep the HTML standalone if that is required by its delivery surface.

## Validation checklist for the expanded draft

Before approving the next graph, check resolved absolute coordinates (not authored relative offsets alone), unique grid cells, 165×128 card-box intersections, and connector intersections. Verify every new node has an intended prerequisite path; keep three-way choice edges 2 grid units apart and joins in one OR block. Check reciprocal exclusivity on all alternatives, no AND join across exclusive branches, no accidental cross-group gating, and whether each political route has a real successor. Recompute total cards (target 298), tree bounds, continuous-focus-panel bounds, and eight-shortcut capacity. Rebuild every normal-scale detail preview after edits; whole-tree screenshots are navigation aids, not proof of legible labels or engine-native link routing.

### Source references

- Current design and geometry: `docs/design/COLDWAR_KOR_1970/COLDWAR_KOR_design.json:15138-15195` and group/focus records throughout; `tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_review_fixes.py:136-161`.
- Current transition stages: `tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_review_fixes.py:11-54`.
- Donor geometry and GUI: see [`md_reference_layout.md`](md_reference_layout.md), particularly `05_south_korea.txt:68-80,140-152,200-212`, `05_russia.txt:552-694`, and `nationalfocusview.gui:370-384,446-493,573-585`.
- Preview serialization: `tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_render.py:185-235`; template `tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_tree_fragment.html`.
