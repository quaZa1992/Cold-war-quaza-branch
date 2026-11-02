# IMPERIA COLD WAR — Greece Enosis layout review

## Scope and source

Read-only geometry review of the pending Greece replacement concept. No concept or runtime file was changed. Source: `concept.json`, SHA-256 `51348163890E8BFC4EB1AE5AC67A8DD8076AB66E7657BEB31D0DA2FFD73DDDF9` (30 October 2026). The concept contains 100 focuses; its static check reports zero focus-window overlaps, valid graph references, and satisfiable focus prerequisites. The checked grid bounds are x=0–50 and y=0–16. The review treats concept x/y as resolved grid coordinates, not emitted offsets.

## Enosis and Cyprus geometry

| Focus | Position | Relevant link |
|---|---:|---|
| `operational_initiative` | (48,5) | prerequisite for both Enosis options |
| `enosis_full` | (46,6) | OR prerequisite for `cypriot_settlement` |
| `enosis_compromise` | (50,6) | OR prerequisite for `cypriot_settlement` |
| `cypriot_settlement` | (48,7) | one prerequisite block containing both Enosis choices, therefore OR |

This is a compact fork and reconvergence: the two options sit two grid columns apart, with their settlement one row below and centered between them. The prerequisite semantics are satisfiable and should remain one OR block. Do not convert it to two blocks, which would require both exclusive choices. The regional Cyprus extension spans x=40–50 and y=0–8; the Crown branch begins at y=11, leaving three clear grid rows vertically.

## Connector review

Static review found no focus-card collision in the supplied check. The one edge family to inspect in the refreshed branch render is the long `external_room` → `bulgarian_trade` route, from (34,0) to (38,5), alongside the left edge of the Cyprus cluster (x=40). The preview renderer has a dedicated short horizontal bus for the two long `external_room` links, then routes vertically at each destination; this keeps the connectors away from Aegean sibling cards and ends west of the Cyprus cards. The distance to the nearest Cyprus card is two grid columns. This is a routing watchpoint, not a confirmed defect.

The Enosis join itself has a clear vertical gap in the preview model: the fork cards end 18 px before the next row begins on the 96×130 grid, leaving the shared OR bus in that inter-row gap. Native engine connector routing remains unverified.

## Visual status

The requested refreshed `ENOSIS_BRANCH.png` was not present during this static pass. Visual checks of card artwork, titles, and actual connector paths therefore remain pending that render. Existing `CONCEPT_CHECKS.json` reports 165×128 item-window bounds and 96×130 pitch, but it is a static bounds result rather than a live native-renderer check. The preview itself labels its font and connectors approximate. No runtime test or engine validation was performed.

## Addendum: refreshed branch image inspected

Opened `ENOSIS_BRANCH.png` at 82%, showing all 17 Cyprus-section focuses. The two Enosis cards form a clear fork after `operational_initiative`; the dashed mutual-exclusion line stays between their cards. Their common `cypriot_settlement` connector runs beneath the alternatives and into the centered settlement card without crossing a card or title. The separate `gre_response` branch and its volunteer/escalation alternatives are also visible, with their dashed exclusion line clear of both labels. No visible card, icon, or title overlap was found. The standalone `reinforce_guard` root sits to the left with clear separation from the main spine.

This clears the visual questions in the earlier static pass for this preview. It remains an external-font, approximate-connector rendering at 82%; native font and engine routing still need verification after approval. No runtime test was performed.
