# Cyprus January 1970 Focus Tree Layout Review

## Scope

This is a layout recommendation for a sizeable Cyprus tree with shared economy, military, and diplomacy sections plus party-gated ideological routes. It covers positions and dependency presentation only; it does not prescribe or revise historical events, party identities, effects, or code.

## What the reference trees show

The current main-MD generic tree uses a plain `x`/`y` position for the root focus and then positions descendants with `relative_position_id` and local `x`/`y` offsets. For example, `GENERIC_political_reform` is at `x=-7, y=0`, while its cabinet and government children use offsets relative to it (`00_generic.txt:55-59, 80-120`). This lets a subtree be designed as a compact local grid and then moved by moving its anchor.

The generic tree typically uses two-column offsets for neighboring focuses, widening to three or more columns where paths need more room. It puts AND requirements in separate `prerequisite` blocks and alternatives within one block: `GENERIC_political_games` requires both cabinet reform and a stronger government (`00_generic.txt:139-150`), and `GENERIC_the_state` joins two completed policy paths (`00_generic.txt:223-234`). Its mutually exclusive choices are declared on the sibling focuses themselves (`00_generic.txt:692-700` and following branch heads). Treat those as separate from visual spacing: the visual row should make the decision legible, and the exclusion declarations should describe the actual game rule.

Russia is a useful unique-tree comparison. Its main root is an absolute `x=62, y=0`; branch starters use local offsets from the root or from a second anchor. Putin's branch starts at `x=13, y=1` relative to the root, and then its children are positioned relative to `SOV_putin` (`05_russia.txt:52-57, 109-119, 157-166`). Russia's shortcuts point to recognizable branch entry focuses, rather than encoding any position (`05_russia.txt:14-45`).

The local 1970 generic tree applies the same approach at larger scale. Its fourteen shortcuts are declared near the top (`mdcw_1970_generic_focus.txt:18-83`). The tree anchors government at x=6; ideological entry focuses at x=21, 44, 63, 86, and 113; foreign policy at x=129; economy and development at x=146 and 161; and industry, social policy, and armed services from x=172 through x=220 (`mdcw_1970_generic_focus.txt:91-94, 618-626, 1660, 3090, 3679, 5475, 6475, 7321, 8047, 8735, 9332, 9900, 10597, 11038`). Those are independent roots, not offsets from the government focus. The wide spans keep a large tree legible and give the player direct shortcut access to distant sections.

Within each local ideological subtree, the common lead-in is a short, centered funnel, then the route spreads into distinct policy tracks. The Western branch has paired civic focuses at row 1, a join at row 2, a government focus at row 3, and four political subroutes at row 4 (`mdcw_1970_generic_focus.txt:659-771, 797-918`). Its row 5-6 options use consistent two-column spacing. The emerging-aligned branch reserves a wider field for six distinct political models, using four-column spacing between model heads and two-column spacing between sub-options (`mdcw_1970_generic_focus.txt:1660-1700, 1814-1860`). This is the strongest precedent for giving Cyprus routes different widths according to their actual number of internal tracks.

## Recommended Cyprus canvas

Use one absolute root for each major region, then position its descendants relative to that section anchor. The current design uses these anchors:

| Region | Anchor | Current role |
| --- | ---: | --- |
| Republic / government | (6, 0) | Constitution, communal crisis, and institutions |
| Shared economy | (26, 0) | Development and investment choices |
| Shared military | (46, 0) | Defensive force, procurement, and civilian authority |
| Shared diplomacy | (66, 0) | Guarantors, blocs, and Enosis question |
| Conditional aftermath | (26, 20) | Crisis, ceasefire, and recovery |
| Turkish Cypriot community | (86, 0) | Community mandate, postwar administration, constitutional consent, and community outcomes |
| Makarios / AKEL / EDEK / Eniaion / Progressive Front / Enosis milieu | (114, 0), (136, 0), (158, 0), (180, 0), (202, 0), (224, 0) | Six party-gated, bespoke 24-focus ideological and economic routes |
| Road to war | (6, 14) | Conditional 1970-74 escalation, coup, intervention, and ceasefire pathway |

The six party roots are spaced 22 columns apart. Each route occupies local x=-8..+8 and y=0..14, so its 17-column footprint leaves five clear columns before the next route; all six share a common top row and depth instead of being stacked into banks. The Turkish Cypriot section occupies x=80..92 and y=0..25, while party routes begin at x=106, leaving a 13-column gap. Shared diplomacy ends at x=72, leaving seven columns before the community section. Shared economy ends at y=15 and aftermath begins at y=20. The total design spans x=0..232 and y=0..31. These bounds come from the current design JSON, with global coordinates recomputed as section anchor plus local offset (`build_design.py:20-25, 296`; each focus record stores both forms).

The six routes share a 24-focus structure but have bespoke political and economic content. Each makes a visible political-settlement-to-economy handoff at local y=6 to y=8, leaving a clear row between those phases. This common vertical rhythm aids comparison while the ±8 local width accommodates distinct economic branches and joins. Keep the Turkish Cypriot community route visually independent: its constitutional-consent focus is an outcome of that section, not a prerequisite gate on CYP party routes.

## Suggested shared section shapes

- **Government and opening:** a short common spine (three to five focuses) that establishes the crisis/cabinet context and opens the other shared sections. Keep its ending in a central position so connector lines to diplomacy, economy, defense, and the party decision do not cross through the detailed branches.
- **Diplomacy:** a compact review focus, then a three-way alignment/neutrality decision in one row. Put each route's follow-up directly below its own choice. If an agreement or regional outcome requires more than one shared policy route, join those prerequisite lines on a centered capstone, as MD does for AND joins.
- **Economy:** start with a shared diagnostic, split into two or three clearly labeled policy priorities, and rejoin at a national program only when the game logic truly requires all selected tracks. Keep the main investment/capstone nodes close to the center of the economic anchor.
- **Military and security:** start with the shared defense review, then divide by function (for example, army, air, navy/coastal defense, or internal security as supported by the intended scope). Do not use a naval subtree as a large equal-weight branch just to fill space; Cyprus's actual planned content should determine its width.
- **Party-gated ideological routes:** give every route its own absolute anchor, one entry focus at local `(0,0)`, and the same broad visual grammar: a short institutional lead-in, a government/program commitment, then one or two internal tracks. Keep the separate routes structurally parallel enough that players can compare their depth, while allowing routes with more planned content a wider field. Use names/icons and search filters to communicate the political distinction; coordinates should communicate only the route structure.

## Party gates and branch legibility

Place the six ideological route heads in a single horizontal row, keeping each route's internal layout consistent in its own local frame. In each route, keep the exact-party gate on or immediately before the entry focus so a player can see why a branch is unavailable before scrolling deep into it. Where a player should commit to exactly one route, declare route heads mutually exclusive with one another, consistently across all heads. Where the intended political system allows later transitions or multiple coalition partners, do not imply exclusivity through layout alone; express that in the focus requirements and conditions instead. Route visibility, party-index availability, and any persistent reveal behavior are gameplay rules; do not rely on their visual position to implement them. The Turkish Cypriot community route should remain independent of the currently ruling CYP party; community consent can inform shared constitutional outcomes without gating party-route access.

Use separate prerequisite blocks for genuinely cumulative requirements and a single block containing several focus names for alternatives. This distinction is visible in both MD and the local generic tree (`00_generic.txt:139-150`; `mdcw_1970_generic_focus.txt:591-601`). Avoid connector lines that travel across the whole tree from every common focus into every party branch. Prefer one shared handoff/capstone near the center, with the selected ideological route requiring that handoff. This keeps both the diagram and its rule set understandable.

## Shortcuts and first view

Provide shortcuts for the high-level sections and each ideological route entry, as the local 1970 tree does for government, foreign policy, economy, development, and each service (`mdcw_1970_generic_focus.txt:18-83`). Point each shortcut at its section anchor or a meaningful first focus. Set `initial_show_position` on the common opening or the first political decision so Cyprus loads at the start of the story (`mdcw_1970_generic_focus.txt:15-16`). Shortcuts should supplement the first view, which should still show the opening focus and the nearby direction of the major branches.

## Practical coordinate checks for the draft

1. Write a small position inventory before implementation: focus ID, anchor focus, local x/y, prerequisites, and whether the node is a route head or capstone.
2. For each subtree, calculate its full local min/max x footprint, including all descendants. Shift anchor roots until those footprints have a clear gap; root positions alone do not reveal collisions.
3. Keep sibling rows aligned. Prefer x gaps of 2 for ordinary paired choices; use 4 or more for multiple ideological models or for tracks whose connectors would otherwise cross.
4. Make joins visually central to their inputs and put them below the input row. Avoid joining across distant sections when a single common handoff can express the dependency.
5. Check reciprocal mutual exclusions and separate AND/OR prerequisite semantics against the intended political design. These are rule checks, not cosmetic choices.
6. Review the opening viewport and each shortcut destination in game. A syntactically valid coordinate map can still scroll poorly or produce visually tangled connectors.

## Audit of the current design

The current JSON contains 295 unique focuses: six party routes with 24 focuses each, a 39-focus Turkish Cypriot community section, a 22-focus Road to War section, and the shared constitution, economy, military, diplomacy, and aftermath sections. The six route anchors are x=114, 136, 158, 180, 202, and 224; the community anchor is `(86,0)`, and Road to War begins at `(6,14)`. The coordinate audit recomputed each global position from its section anchor and local offset (`build_design.py:20-25, 296`). All positions are unique; references resolve; there are no dependency cycles. All 55 mutual-exclusion pairs are reciprocal. The graph has 347 prerequisite edges, all descending in y. There are no cross-section prerequisite edges. The 295-focus reachability audit reports every focus structurally reachable (`GRAPH_REACHABILITY.json`).

The section bounds are constitution x=0..16/y=0..9, economy x=20..32/y=0..15, military x=40..52/y=0..14, diplomacy x=60..76/y=0..10, aftermath x=22..30/y=20..31, Turkish Cypriot community x=80..92/y=0..25, party routes x=106..122, 128..144, 150..166, 172..188, 194..210, and 216..232 (each y=0..15), and Road to War x=2..10/y=14..32. Their focus coordinates do not overlap. The six broad party islands have consistent pitch and generous clear gaps; the added escalation section sits below the opening constitution area without colliding with it or the aftermath section.

The party routes have a clear internal progression: political settlement at local y=6 hands off to the bespoke economic mandate at y=8. The Turkish Cypriot constitutional-consent focus is not a party gate, and none of its focuses requires a party index. Community assent is instead reflected as an outcome input to shared constitutional settlement. Starting spirits are presented as preview-only metadata; the game-facing spirits belong in the native country-spirit UI.

The preview uses orthogonal connectors from the parent focus's lower edge to the child's upper edge, with a horizontal jog at the midpoint (`build_md_view.py:90-107`). The final static reroute adopts section-local positions in `build_design.py`'s reposition block. In the constitution section, `foreign_officers` / `emergency_powers` are `(10,2)` / `(10,4)` (global `(16,2)` / `(16,4)`), and `crisis_conference` is `(0,9)` (global `(6,9)`). In diplomacy, `british_bases` / `base_sovereignty` are `(6,3)` / `(10,4)` (global `(72,3)` / `(76,4)); `athens_relationship`, `ankara_channel`, and `soviet_trade` are `(-4,5)`, `(0,4)`, and `(-2,2)` (global `(62,5)`, `(66,4)`, `(64,2)`). The economy route places `limassol_port` at `(0,7)`, `credit_question` at `(0,9)`, `foreign_capital` / `cooperative_credit` at `(-4,10)` / `(4,10)`, and `transparent_accounts` / `village_banks` at `(-4,11)` / `(4,11)`, all relative to the economy anchor. Military `air_ambulance` is at `(0,9)` relative to its anchor.

The Turkish Cypriot unilateral-resolution focus is now an independent conditional focus, with its graphical prerequisite edge removed. Its availability requires the recorded `tc_terms_rejected` outcome and no implemented final settlement; its design requirement states that the community rejects negotiated terms and the CYP government then chooses unilateral pressure. This preserves the separate community and government decisions.

A static pass using the preview's orthogonal wire route, with focus tile bounds of 165×128 px at 90×130 px coordinate pitch, now finds zero proper connector crossings and zero unrelated focus-tile intersections across all 347 prerequisite edges. Coordinates remain unique and all edges descend in y. The expanded constitution and diplomacy boxes end at x=16 and x=76 respectively, leaving three empty grid columns before the economy at x=20 and Turkish Cypriot section at x=80. The preview and browser QA were regenerated after the final position changes.

The builder's prerequisite semantics are AND across groups and OR among focus names in one group: `focus(..., parents=[a,b])` creates `[[a],[b]]`, while `either(node,a,b)` creates `[[a,b]]` (`build_design.py:20-38`). Thus `war_command_dispute` and `war_august` are not unsatisfiable on account of mutually exclusive alternatives; both are authored through `either`, and the independent reachability audit confirms all 295 focuses reachable. `war_august`'s OR choice is consistent with either Geneva or remobilisation supplying the prerequisite path, while its availability carries the failed-Geneva and no-final-settlement conditions.

The preview builder writes both aliases from the current full-tree MD-style fragment and scales the layout from all world coordinates (`build_md_view.py:58-74, 84-107`). After the final coordinate reflow, the regenerated preview passed browser QA at 1024, 736 and 360 pixels: 295 focuses, 13 sections, nine starting spirits, zoom/pan, effects and both community/war shortcuts. Starting-spirit information remains preview-only, while in-game spirits belong in the native country-spirit UI.

## Priorities for the next revision

1. Preserve the adopted global coordinates when authoring the runtime tree; the current preview and browser QA use this arrangement.
2. Review the separate TC rejection outcome and CYP unilateral-pressure choice in event flow; availability already gates on `tc_terms_rejected` and blocks after final settlement.
3. Review the focus tree in game when runtime focus definitions exist; preview geometry cannot confirm engine scrolling or rendered tile sizes.

The current design has 295 unique focus IDs and positions, 55 reciprocal mutual-exclusion pairs, and 347 prerequisite edges. All references resolve, every edge descends in y, the graph has no dependency cycles, and the reachability audit passes all 295 focuses using the builder's OR/AND semantics. The 22-focus Road to War section expands the canvas to y=32; the six party routes and Turkish Cypriot community section retain their prior spacing and political-to-economic structure. The adopted positions and conditional gate produce zero orthogonal prerequisite-wire crossings and zero unrelated focus-tile hits in the static geometry audit. Preview regeneration and browser checks are complete; in-game rendering remains to verify after runtime definitions are authored. Only the reposition/graph-override block in the design builder was edited; its generated JSON/dossier and this report were refreshed. Runtime focus definitions were not changed.
