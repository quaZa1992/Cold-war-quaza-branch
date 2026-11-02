IMPERIA COLD WAR

# Chile 1970 compact layout report

## Scope

This overlay changes coordinates only for the 184-focus approved Chile design. It leaves `approved_design.json`, focus IDs, rewards, costs, requirements, prerequisites, exclusions, availability, and AI data untouched. The original concept files and installed outputs were not changed.

## Reference profile

Inspected the current checkout's `common/national_focus/00_generic.txt`, `common/national_focus/05_france.txt`, and `common/national_focus/05_russia.txt`, alongside the target design's declared 96 by 130 grid and 165 by 128 focus item. Generic and France demonstrate relative-positioned focus cards and deliberate native grid spacing; Russia was inspected as an additional current national-tree reference. The project geometry was measured from every node's stored absolute design coordinate and actual section membership.

The overlay retains each section's internal shape and focus anchor IDs. Section rectangles are translated as units, with two grid units between section bounds and between bands. All focus-card rectangles were independently checked using the declared native dimensions.

## Layout change

Sections are arranged into three bands:

| Band | Sections | Vertical span |
|---|---|---:|
| 1 | Republic, Development, Defence, PDC, PN | 0 to 6 |
| 2 | PR, PS, PCCh, MAPU, Diplomacy | 9 to 15 |
| 3 | DR, PADENA, Gremial, MIR, Military | 18 to 26 |

| Measure | Before | Overlay |
|---|---:|---:|
| Focus columns | 157 (x 4 to 160) | 77 (x 0 to 76) |
| Focus rows | 18 (y 0 to 17) | 27 (y 0 to 26) |
| Focuses | 184 | 184 |
| Card overlaps at 165 by 128 px | Not re-audited in original placement | 0 |

The continuous-focus panel proposal keeps its horizontal origin and moves to y=3640, two grid rows below the last focus row, based on the design's 130 px grid height.

## Integrity checks

- All 184 focus IDs match the frozen approved design.
- Full non-geometric design content compares equal after excluding only focus/group positions and the derived layout span/revision/panel position metadata.
- Prerequisite groups and mutual exclusions compare equal by focus ID.
- All 184 focus anchors exist; the overlay preserves the anchor ID of every focus and each group's anchor ID.
- Pairwise axis-aligned card collision check found no overlaps at the declared 165 by 128 px card bounds on the 96 by 130 px grid.
- No prerequisite crosses section boundaries in the approved design, so translating sections does not create cross-section links.

## Verification limits

This report covers geometry and structural data only. It does not claim a rendered browser preview, live-game navigation, native connector routing, or HOI4 engine verification. Parent task will review the actual generated preview separately.
