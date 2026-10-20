# Israel 1970 focus tree layout review

This review records layout-only adjustments in `tools/israel_1970/layout.py`.
Focus prerequisites and gameplay dependencies were not changed. Coordinates below
show resolved COMMON positions as `(x, y)`; positions described as relative are
the values stored under the relevant COMMON block or ORIGINS entry.

## Changes

| Focus IDs | Before | After | Reason |
| --- | --- | --- | --- |
| `ISR70_civil_defense` | (98,4) | (95,3) | Keeps it on the immediate row below `reserve_system` and moves its connector out of the `defensive_depth`/`maneuver` boxes. COMMON local position changes from (-12,3) to (-15,2). |
| `ISR70_preparedness` | (100,5) | (100,6) | Creates a clear connector corridor from its deep-defense and air-defense prerequisites. COMMON local position changes from (-10,4) to (-10,5). |
| `ISR70_intelligence` | (128,2) | (110,6) | Starts an independent intelligence branch in the open center column below `staff`. COMMON local position changes from (18,1) to (0,5). |
| `ISR70_intelligence_analysis` | (127,3) | (108,7) | Forms the left child of the intelligence root. COMMON local position changes from (17,2) to (-2,6). |
| `ISR70_intelligence_operations` | (129,3) | (112,7) | Forms the right child of the intelligence root. COMMON local position changes from (19,2) to (2,6). |
| `ISR70_import_substitution` | (11,4) | (11,3) | Places the child on the immediate row below `haifa_industry`; its connector now stays in the row gap. COMMON local position changes from (-2,3) to (-2,2). |
| `ISR70_export_specialization` | (15,4) | (15,3) | Symmetric to import substitution, on the immediate row below `haifa_industry`. COMMON local position changes from (2,3) to (2,2). |
| `ISR70_territorial_maximalism` | (110,13) | (108,14) | Clears the center vertical corridor below `territorial_policy`, which is used by the Golan and Gaza connectors. COMMON local position changes from (0,5) to (-2,5), with the territories origin moving down one row. |
| `ISR70_golan_review` | (113,14) | (113,16) | Adds two resolved rows beneath its Revision-4 position so its connector enters through the gap below the territorial choice row. COMMON local y changes from 6 to 7, with the territories origin moving down one row. |
| `ISR70_gaza_services` | (116,14) | (116,16) | Same connector clearance as Golan review. COMMON local y changes from 6 to 7, with the territories origin moving down one row. |

The `territories` group origin moves from (110,8) to (110,9). This shifts the
whole block down one row, leaves a full row between the intelligence children at
y=7 and Suez at y=9, and gives the preview group heading more room above Suez.
The layout metadata revision is now 5.

## Geometry review

The in-memory preview simulation used the current 315-node `english_design.json`
prerequisite graph, `x_unit=80`, `y_unit=190`, and 148×160 focus boxes. It modeled
the preview's orthogonal route from each parent bottom-center to the vertical
midpoint between parent and child, then horizontally to the child's vertical
center, then down to the child top. With these proposed positions, the simulation
found no intersecting focus boxes, no child at or above a prerequisite, and no
connector segment crossing an unrelated focus box. The previously identified
Haifa and territorial connectors also clear the intervening focus boxes.

This is an exact check of the preview's modeled geometry, not a Hearts of Iron IV
game-engine render. The game may route focus connectors differently, and this
review does not claim that the in-game lines will be pixel-identical. No build or
game launch was run as part of this review.
