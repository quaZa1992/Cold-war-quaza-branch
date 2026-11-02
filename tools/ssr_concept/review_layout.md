IMPERIA COLD WAR — SSR 1970 concept layout review

# Independent final geometry review

Reviewed `docs/design/ssr_1970_concept/DESIGN.json` at SHA-256 `13783991d91c880ccef75ab9fe1c9842e599305e6c7e41cb163fe7a9bb9a4edd`.

## Findings

- The 14 country models use one consistent chapter map: SSR chapters at x=8, 20, 32, and 44; regional priorities at x=56; the shared Union Plan at x=70. Independence chapters begin at y=14. Party chapter centres advance by 12 grid units from x=6, with party programmes beginning at y=25.
- Resolved focus coordinates across each country plus the 17 shared Union Plan focuses fit within x=4..80 and y=0..33. The country-specific regional branch occupies x=54..58 and y=0..2. The rehosted Union Plan occupies x=61..80 and y=0..3, leaving visible card clearance between the two branches.
- The shared Union Plan no longer collides with the regional branch. The secretary's earlier x=90/91 collision is cleared by the final rehost. The final `DESIGN_AUDIT.json` reports zero errors for all 14 model routes, combined card bounds, and continuous-panel bounds.
- The continuous-focus panel is specified at (6100,650), sized 770x380. The audit reports no focus-card overlap with this panel.
- Party columns use 12-unit spacing, so adjacent 165px cards have substantial horizontal separation at the 96px grid pitch. The longest party branches reach y=33, leaving the map bounded and legible for chapter navigation.
- The JSON defines the Union Plan's native focus prerequisites independently of the SSR regional branch. Its geography rule also says a focus without an eligible counterpart remains unavailable without blocking unrelated regional diplomacy. No structural prerequisite route was found that makes the foreign border offer a prerequisite for the training, energy, or water routes.

## Limits

This is a static coordinate and prerequisite review of the concept data. `DESIGN_AUDIT.json` also explicitly limits its scope to concept data; neither it nor this review establishes native-game connector rendering, live tree navigation, or save behavior. The final design records long-edge routing through empty adjacent columns; those connectors still need visual confirmation in the native focus tree before implementation is approved.
