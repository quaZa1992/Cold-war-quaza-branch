# DPRK 1970 concept layout review

Reviewed the canonical concept snapshot in `COLDWAR_NKO_1970_design.json`, its structural validation output, the eight party/institution visibility states, and the rendered overview plus all twelve branch PNGs dated 23 October 2026. This is an independent static and visual layout review; no canonical design or build source was edited for this report.

## Checked structure and geometry

- The design contains 167 positioned focuses across 12 groups. The checked absolute bounds are x=2..56 and y=0..25.
- All 12 group roots are unanchored roots at local offset (0,0): WPK (6,0), economy (16,0), defence (30,0), diplomacy (44,0), atomic (54,0), KDP (4,17), Chondoist (12,17), cabinet (20,17), KPA (28,17), Yan’an (36,17), labour (44,17), and Christian (52,17). Every anchored focus resolves from its named root using its `dx`/`dy` relative offsets, with no mismatches in the rerun. These offsets must be emitted as relative positions in the game tree; copying resolved absolute x/y values into child offsets would double-count nonzero root positions.
- The graph has 189 prerequisite edges and 30 reciprocal mutual-exclusion pairs. The structural checker reports no unresolved IDs, non-reciprocal exclusions, or forward-edge cycles. It also checked AND/OR prerequisite and choice-history reachability.
- Eight government variants were checked at slots 2, 3, 4, 5, 7, 13, 14, and 22. The checker applied the conditional visibility rules to each state and found zero overlaps between full 165×128 px focus cards on a 96×130 px grid. The focus-only geometry remained distinct from the alternate-programme band in each state.
- The shared/WPK area occupies y=0..14 and the eight conditional programme blocks occupy y=17..25, leaving three grid rows between the bands. The upper roots are at x=6, 16, 30, 44, and 54; the lower roots are at x=4, 12, 20, 28, 36, 44, and 52. Native-style two-way forks use child offsets ±2 (four columns between branch centres); the economy three-way fan uses −4/0/+4; the defence four-way row uses −6/−2/+2/+6. The overview shows the two bands clearly.
- I reran the current preview connector geometry against all eight states. Prerequisite lines run from the source card bottom (`top + 128`) to the child card top, with the orthogonal bend at their midpoint; this places adjacent-row joins in the 2 px gap of the 130 px row pitch. The checker found zero prerequisite-line intersections with unrelated focus cards and zero crossings between unrelated prerequisite edges in all eight states. Mutual-exclusion data contains 30 reciprocal pairs in 28 choice groups. The preview draws only adjacent connectors within a same-row mutually exclusive cluster, while retaining every pairwise exclusion in the data; these connector lines also have zero intersections with unrelated card boxes in all states. The refreshed defence crop confirms that the tightened fan remains legible, and its four-choice row has no card or route collision in this model. The exact native engine route was not exercised.

The machine-readable counts and checks are recorded in `COLDWAR_NKO_1970_design.json` under `validation` and in `structural_validation.json`. The current structural report records 167 nodes, 28 choice groups, 30 exclusions, and 189 edges with zero errors; it explicitly marks `engine_tested: false`.

## Title fit

`short_titles.json` contains 88 manually shortened labels corresponding to the source titles wider than the 147 px native focus-name field. I measured the strings against the installed game's `hoi_16mbs.fnt` glyph advances. All mapped strings are supported by the font and measure at most 140 px, leaving at least 7 px against the nominal field width; the maximum is “Responsible Secretariat” at 140 px. This measurement establishes native glyph-advance fit for those strings, not the exact rendered result for every language or display scale.

## Visual review

After the coordinate refinement, I rechecked the overview and the WPK, economy, KDP, and defence crops. I also checked the refreshed defence crop after the connector update. They show the shared and conditional bands clearly, with readable focus cards and no visible card collisions. The new four-column two-way rhythm and the economy and defence fans read cleanly. The branch layouts preserve the intended native MD node rhythm and the selected icons fit their subject matter in the main economy, military, and diplomacy branches. The industrial-labour programme keeps worker imagery; the Christian programme uses the cross emblem, and the Chondoist programme remains visually distinct as its own conditional branch. Remaining deliberate icon repetition is most noticeable in the Chondoist agriculture/cornfield branch, the cabinet plan-accountability branch, and the KPA medallion branch; these are icon-variety considerations rather than geometry defects.

Rendered artifacts reviewed:

- [Full-tree overview](COLDWAR_NKO_1970_overview.png)
- [WPK branch](branch_wpk.png)
- [Economy branch](branch_economy.png)
- [Defence branch](branch_defence.png)
- [Diplomacy branch](branch_diplomacy.png)
- [Atomic branch](branch_atomic.png)
- [KDP programme](branch_kdp.png)
- [Chondoist programme](branch_chondo.png)
- [Cabinet programme](branch_cabinet.png)
- [KPA programme](branch_kpa.png)
- [Yan'an programme](branch_yanan.png)
- [Labour programme](branch_union.png)
- [Christian programme](branch_christian.png)

## Limits of the preview

The local HTML/PNG preview approximates the native MD focus-card geometry and connector appearance. Its browser-rendered labels use the preview's available Arial-like font rather than the game renderer, so the image is not an exact native-font capture; the separate glyph-advance check above covers the mapped labels. The local Chromium executable was unavailable and the in-app browser cannot reach the local preview server, so no browser-runtime or in-game test is claimed. The current PNGs are visual review aids only. Final acceptance of exact native card text and connector placement still depends on the in-game tree view.
