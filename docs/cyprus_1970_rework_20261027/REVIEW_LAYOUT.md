IMPERIA COLD WAR: Compact Cyprus concept layout review

Scope: read-only review of `concept.json`, `full-tree.svg`, `tools/cyprus_1970_concept/build.py` and `preview.html`. Concept only. No loaded game files or concept source files were changed.

## Final regeneration review

The four connector intersections from the preceding draft are resolved in the regenerated coordinates: `recovery` `(49,5)`, `resilience` `(67,5)`, `civilian_rule` `(37,7)` and `geneva` `(43,7)`. Rechecking the current CYP focus graph with 165 by 128 pixel card bounds and the approximate 85 by 130 pixel pitch finds no overlapping card rectangles or connector paths through unrelated cards.

The prior EEC preview omission is resolved. The `association` focus preview names West Germany, France, Italy, Belgium, Netherlands and Luxembourg separately, and shows each partner's spirit, numeric modifiers, setup and recurring amounts. Its receiver-side terms now use direct per-country values rather than an unnamed pooled result.

The preview now uses the native 147-pixel by 20-pixel single-line title box. The final alias is `reserve_service`, “Reserve Standards”; the previously measured one-pixel overflow is resolved in the current generated JSON. The exact native font is still an approximation, so final fit needs an in-game check.

The 12 supporting guarantor focuses are now represented in `concept.json` and the interactive preview as separate mini-modules: six for Greece, three for Turkey and three for Britain. The three local graphs have distinct positions, no simulated card overlap or connector collision, and reciprocal exclusions. Their attachment points and camera positions inside the complete national trees remain unverified; `full-tree.svg` shows the 100-focus Cyprus tree, while the interactive preview holds the supporting modules separately.

## Checks that passed

- `concept.json` contains 100 focuses, 100 unique keys and positions, and the declared nine group counts match the actual counts.
- Regenerated compact positions retain the six shared upper sections at `y=0..8` or less, with the three party programmes beginning at `y=11` and ending at `y=18`.
- Every relative anchor refers to an earlier focus and resolves to the recorded absolute coordinate. The proposed 85 by 130 pixel grid has no overlapping 165 by 128 pixel focus-card rectangles. These measurements are preview approximations, not engine-exact spacing.
- All 15 exclusion pairs are reciprocal. The focus prerequisite groups are satisfiable under the encoded AND/OR rules; no missing key or prerequisite cycle was found. There are no cross-group prerequisite edges.
- All three party programmes have consistent exact party triggers on every focus: `western_conservatism_are_in_power` for Presidential Centre, `western_liberals_are_in_power` for Eniaion and `emerging_communist_state_are_in_power` for AKEL. They remain represented in the concept independently of which party is currently in power.
- No native focus `unlock` effects remain. The seven offer focuses include sender and recipient effects, setup and recurring amounts, named spirits, modifiers and other listed rewards. The focus inspector renders prospective offer effects without an eligibility filter, including named EEC recipients.
- The supporting actor modules contain 12 focus records across GRE, TUR and ENG. All prerequisite references resolve and their exclusion pairs are reciprocal.
- Reconciliation is described as monthly with targeted transition hooks. I found no weekly relationship polling in the concept builder or preview; weekly entries refer to monetary agreement streams.

## Limits

The SVG and browser preview use an approximate 85 by 130 pixel grid, Arial text and simulated orthogonal connectors. They do not prove native connector routing, actual font fit, scroll behavior, actor-tree integration or in-game card clearance. No HOI4 render was available in this review.
