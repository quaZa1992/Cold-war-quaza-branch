# Cuba 1970 concept: independent graph and layout review

Review snapshot: 23 October 2026. Source: `docs/design/cuba_1970_concept/COLDWAR_CUB_1970_CONCEPT.json`, 115 focuses in 17 groups, rendered in the project's native-style browser preview. This review assesses graph geometry, connectors, labels, screenshots, and registry coverage; it does not approve gameplay balance or substitute for an in-game engine run.

## Native presentation and graph

The reference dimensions match the installed main-MD focus UI: 96 × 130 px grid, 165 × 128 px focus card, and 147 × 20 px title field. The JSON uses that grid. Every focus has a unique resolved `xy`; same-row centers are at least two cells (192 px) apart, leaving 27 px between cards and 45 px between title fields. Titles fit the title fields at the renderer's measured font width. For the map scale, the overview is intentionally a topology map rather than a reading view; the individual branches are comfortably legible at their captured 78–92% zooms.

The shared roots are now compacted to Economy (8,0), Society (20,0), Defence (30,0), and Foreign Affairs (42,0). Their node bounds are respectively x=0–14/y=0–6, x=18–22/y=0–4, x=28–32/y=0–4, and x=38–50/y=0–6. The remaining gaps preserve clear section separation without the earlier excessive spread. Shared policy ends at y=6; the first political programme row starts at y=10, leaving three empty grid rows. This is a good visual distinction between national policy and governing programmes; keep it.

Political roots form a clean two-tier array. At y=10: PCC/Fidel slot 4 at x=6, Orthodox Planning Cadres slot 6 at x=14, Guevarist slot 19 at x=22, FAR slot 22 at x=30, Auténtico slot 3 at x=38, OSPAAAL slot 5 at x=46, and JUCEPLAN slot 13 at x=54. At y=18: Ortodoxo slot 18 at x=6, Christian Democratic Movement slot 1 at x=14, Constitutional Liberal Republic slot 2 at x=22, RECE slot 0 at x=30, Alpha 66 slot 20 at x=38, and MININT slot 7 at x=46. The eight-cell pitch is ample for the widest local branch: a four-cell center span is 384 px, so ordinary programme clusters do not touch. The max x of 56 is still a modest overall extent. The second tier begins three rows below the first tier's programme roots and one row below their deepest local branches, so this vertical pitch is tighter than the shared-to-politics gap but remains readable in the previews.

## Connectors and prerequisite semantics

The native-style renderer uses orthogonal routes: a vertical stem leaves the parent, a horizontal rail runs above destination medallions, then a vertical drop reaches the child. Reviewing the actual `PREVIEW_*.png` captures clears the earlier static diagonal-line crossing suspicion around `rail_lorries`, `sugar_exports`, and `havana_ports`; do not move the sugar/mill pair for that reason. The visible economic routes do not cross node faces or make unrelated branches appear joined.

There are 112 prerequisite edges across the 115 nodes. All node positions are unique, all references resolve, and the measured edges advance downward. Solid prerequisite rails and dashed mutual-exclusion rails remain visually distinguishable. The paired alternatives make sensible local forks. Multi-parent prerequisite lists are OR alternatives in the preview model; there are no AND joins encoded as multiple prerequisite blocks. The First PCC Congress correctly accepts either Party over Ministry or JUCEPLAN's Mandate: these two preparations are mutually exclusive alternatives, so a conjunctive gate would make it unreachable. The graph's MEX pairs are symmetric, including the later compact OSPAAAL, MININT, and JUCEPLAN choices.

## Preview review

`PREVIEW_overview.png` has a coherent hierarchy: four shared sections form the upper band, seven programmes the next band, and six the lower band. Branch density is balanced and the empty lower-right area gives the long foreign tree some room. At 18%, individual title text is not a reading surface, as expected; labels and node silhouettes still communicate the full topology. The screenshot also has the negotiated-agreements panel open below the canvas, so it is a composite concept interface rather than a tree-only plate.

`PREVIEW_pcc.png`, `PREVIEW_defence.png`, and `PREVIEW_society.png` read cleanly at native-style branch scale. PCC's two OR parents converge on First Congress with clear dashed exclusions. The smaller `PREVIEW_ospaaal.png`, `PREVIEW_minint.png`, and `PREVIEW_juceplan.png` views make the three-node institutional currents legible without inflating them into full-length party trees. `PREVIEW_starting.png` uses distinct native imagery and its scrollable panel can accommodate the spirit list.

The regenerated `PREVIEW_economy.png`, `PREVIEW_foreign.png`, and `PREVIEW_liberal.png` resolve the prior crop problems. Economy now contains Havana Ports, Oil Shock Reserve, and Joint Ventures with comfortable margins. Foreign Affairs shows Playa RDA and Use and Handover fully above the caption, with Washington Talks clear of the right edge. The Liberal programme is isolated from adjacent branches. Branch inspection mode hides other groups for readability without changing focus coordinates or emitted focus code. The refreshed previews also use native-sized icon art and centre-positioned mutual-exclusion markers. These captures are now suitable for signoff.

Browser validation reports 51 views, 115 inspector states, 13 governing alternatives, zero missing images, and no browser errors. It explicitly checks that every visible card stays within the canvas at 320, 736, and 1024 px widths. This confirms browser-renderer state, image, and canvas bounds; it is not an HOI4 engine test.

## Party and institution coverage

The ten earlier party-only groups have been supplemented with three real registry slots. The current 13 choices map to ten historical or counterfactual political coalitions and three institution/current-led governing alignments: OSPAAAL (slot 5), MININT (slot 7), and JUCEPLAN (slot 13). The group descriptions explicitly note that OSPAAAL was a solidarity organization, and MININT and JUCEPLAN were state institutions rather than separate parties. This is a useful completeness improvement without pretending these are equivalent kinds of organization. Continue to call them governing programmes/alternatives, not thirteen parties.

No additional subbranches are needed for layout completeness at this scale. The concept already covers the significant internationalist and security currents, while small nationalist and monarchist registry entries can remain excluded from the national tree. Keep the institutional labels and historical-status caveats visible in the concept documentation.

## Recommendation

Approve the current graph geometry, native-style aesthetics, and regenerated branch captures. No crop or focus-coordinate changes remain. Do not increase political branch count for layout reasons.

