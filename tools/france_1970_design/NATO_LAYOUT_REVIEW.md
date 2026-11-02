IMPERIA COLD WAR

# Gaullist NATO subtree: geometry review

## Scope and freshness

Reviewed current FRA2 concept revision `FRA2 concept 1.1: Gaullist NATO` with 152 focuses and 14 groups. Concept SHA-256: `bbe435370fbff890169652ba0a25a0e4244236e803b7761062a7fb5c014efb22`. This report is read-only. The earlier 134-focus `geometry_review.md/json` remain as historical baseline; this separate report describes the current NATO extension.

## Placement and footprint

The 18-focus `udr_nato` subgroup uses UDR slot 1 and is governed by UDR. Its root `nato_review` is at `(20,7)` and requires `gaullist_success` at `(20,5)`. The branch spans x=15..25 and y=7..11. The entry connector crosses the 132 px card-to-card vertical gap between those rows.

The NATO focus-card footprint is 1,125 × 648 px at the measured 96 × 130 grid and 165 × 128 focus size. The six-card leaf/offer rows have two grid columns between adjacent centers, leaving 27 px between cards. Shared economy content starts at x=30, leaving 315 px from the NATO subtree’s rightmost card edge. This reserves the extension while keeping the party branch and shared economy legible.

## Rendered visual review

Inspected the current full-tree fit at 18% and the NATO section at 73% in a 2,400 × 1,550 local Chrome viewport. The normal-scale view shows the Gaullist Majority prerequisite, NATO entry, three mutually exclusive strategic directions and their leaves. The section camera now includes the external parent gate. The subgroup is visually distinct beneath UDR; the economy branch remains visible to its right without entering the NATO card footprint.

The rendered tree has 152 focus cards across 14 sections, with 46 full-tree mutual-exclusion pairs. It renders 223 SVG paths. All 178 prerequisite edges have matching paths. Analytic intersection checks found no prerequisite route passing through an unrelated focus-card rectangle. This checks the current preview router only; native HOI4 routing remains unverified.

Focus icons and frames read clearly at normal scale. NATO and nuclear medallions distinguish the entry and nuclear choice; French land/naval marks distinguish the six subordinate leaf cards. The full-tree overview is useful for hierarchy, while normal-scale views are needed to read labels.

## Title fit and offers

All 18 NATO titles fit the current 147 px title width using Arial 15 px measurement; the widest is `Selective Cooperation` at 146.76 px. Font metrics are a preview approximation; the installed game has not been rendered.

All four NATO bilateral offer inspectors show an `If they accept` section with both partner-specific Add sections visible. Their effect rows are listed in `NATO_LAYOUT_REVIEW.json`; this review checks presentation only.

| Focus | Short title | France rows | Recipient rows |
|---|---|---:|---:|
| `nato_rhine` | Rhine Field Exercises | 3 | 3 |
| `nato_atlantic_fleet` | Atlantic Exercises | 4 | 4 |
| `nato_europe_land` | Land Standardisation | 4 | 4 |
| `nato_europe_sea` | Naval Industry Pact | 4 | 4 |

## Limits

The layout report does not validate gameplay balance or the historical basis for each effect. External preview routing, title font, camera behavior, and icon display are not proof of the native HOI4 engine render.
