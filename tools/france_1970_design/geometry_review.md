IMPERIA COLD WAR

# FRA2 concept geometry review

Reviewed the regenerated `tools\france_1970_design\concept.json` snapshot (`FRA2 concept 1`, SHA-256 `04a12f6f1d2a3f4e500e6f848cac5fb1eab3c083d664642a6e09a88cca3060c2`). This is an independent, read-only coordinate and logic review. I did not change the concept. The local browser preview was reviewed after this initial coordinate/logic pass. No native game render is claimed.

## Structural result

The parser resolved all 134 focus coordinates across 13 groups. There are no missing or forward anchors, anchor-offset mismatches, duplicate grid positions, unknown prerequisite keys or unknown exclusions. All 39 mutual-exclusion pairs are reciprocal. The 158 prerequisite edges stay within their declared group.

## Geometry against installed MD

The current concept spans x=4..134 and y=0..13. Party and shared-institution programmes occupy y=0..5. The three shared economy, defence and diplomacy roots start at y=8 and their lower branches reach y=13. The separated bands leave room between political programmes and shared policy sections.

At the requested native item size 165×128 px and grid stride 96×130 px, the centered-rectangle model finds 0 focus-box overlaps. Same-row nodes are at least two x-grid columns apart, leaving a 27 px gap between item boxes. The one-row progression step leaves a 2 px gap between same-column item boxes. That is close to the installed MD vertical rhythm, which commonly advances by one grid row, but the near-touching boundaries still need normal-scale visual review.

The overall span is panoramic: about 12,645 px wide by 1,818 px tall at the native grid stride, before viewport margins. The top party branches are spaced apart deliberately. The concept now specifies an opening focus and 13 section shortcuts; native-engine camera behavior remains unverified.

## Connector review

A straight centerline estimate had flagged possible card intersections before the HTML preview existed. That estimate is superseded by the current rendered preview route check. The current orthogonal SVG routes were sampled along their actual path geometry against all focus rectangles; no prerequisite connector path intersects an unrelated focus card. The routing changes place the line from the parent card's bottom edge to the child card's top edge, with the bus one pixel above the child. This matches the tree's 2 px vertical card gap. Preview paths are not proof of native HOI4 connector rendering.
## Title fit flags

The donor focus name region is 147 px wide and 20 px high (`nationalfocusview.gui:578-583`). The current preview now uses 147 px of title width at Arial 15 px. Fresh DOM measurement found 0 of 134 labels over 147 px. The latest short-title revisions fit this preview check. Native HOI4 font metrics and truncation remain unverified.
## Art map and review boundary

`concept_icon_map.json` maps the concept's 13 icon categories to actual installed MD sprite names and DDS paths. The concept currently reuses one icon across every focus in a given group. Several party marks are modern visual proxies, not claims about January 1970 party branding; the map identifies those limits. Overview-fit and normal-scale branch views were inspected; repeated-symbol fatigue and focus-specific scanability remain art-design review points.

`geometry_review.json` contains group bounds, anchor/prerequisite/exclusion diagnostics, title metrics, the approximate source-line report, and current rendered-route findings. Donor measurements and source references are in `md_layout_reference.md` and `donor_profile.json`. The browser preview uses orthogonal SVG connectors and was inspected at overview and branch scale. Native-engine connector routing, camera behavior and focus-state titlebars remain unverified.

## Current rendered browser-preview findings

The current `PREVIEW.html` title check loaded in local Chrome with no page errors and measured all 134 focus labels in Arial 15 px. The content width is now 147 px and no label exceeds it. Native-game font and truncation remain unverified.

The current orthogonal SVG routes have zero intersections with unrelated focus rectangles in the rendered DOM check. Paths connect the parent bottom (y+128), run through a horizontal bus at the child top minus one pixel, then terminate at the child top. The 2 px gap between cards leaves the route outside focus-card bounds. All 196 paths were matched to concept prerequisite edges; none were missing. Earlier direct-centerline flags are superseded by this current routed-path result.

The 134-node tree was reviewed in overview-fit and native-scale branch views. The full tree is panoramic, so overview fit shows overall structure while selected branch views are needed for legible labels and links. The concept specifies initial focus `COLDWAR_FRA2_progress` and 13 shortcuts. This is the local HTML preview, not a native HOI4 screenshot. Current concept hash: 04a12f6f1d2a3f4e500e6f848cac5fb1eab3c083d664642a6e09a88cca3060c2.



