# IMPERIA COLD WAR - Final foreign-policy concept review

## Resolved review findings

`Protected Enterprises` and `Joint Ventures` now both require `Moa's Refinery`, restoring the route that previously passed through Light Industry. Their exclusive choice is intact, and their combined duration still carries the Light Industry cost. This resolves the missing-prerequisite issue recorded in the previous review.

The preview connector now starts at `parent.y + 129` and ends at `child.y - 1`, with a flat initial segment. I re-ran the orthogonal path check against all 118 prerequisite edges and found no connector segments crossing unrelated focus cards. The earlier intersections came from ending at `child.y - 8`, which placed the horizontal path inside the preceding row's card bounds. The new foreign, trade, and context images show complete routes without clipping.

The node budget is consistent. `VALIDATION.json` lists 11 merge records; the relocation record accounts for two old military focuses moving into the foreign section. The 11 actions release 12 old section slots, producing the approved 120 total with 25 foreign focuses. This is consistent with the revised protocol wording.

## Checks that passed

The concept contains 120 focuses with 25 in foreign policy and preserves the 13-focus PCC branch. Its Mexico offers are symmetric in structure: both Mexican focuses target MEX, grant separate paired spirits and charge only on acceptance. They are mutually exclusive with each other as competing project-credit priorities. Their exclusivity does not block Soviet, Spanish, Canadian, Caribbean, or other-country agreements.

The COMECON application and Division of Labour remain separate. The latter requires actual COMECON membership. The Soviet commodity and industrial credit alternatives, Mexico's competing projects, Spain's projects, Canada's projects, symbolic island cooperation versus cession, limited trade versus claims settlement, and advisers versus expeditionary forces are represented as local forks rather than one global foreign-policy mutex.

All prerequisite references resolve, the graph has no prerequisite cycle, and every prerequisite edge points down the tree. The cross-section Territorial Defence versus Expeditionary Brigades mutex is reciprocal; Advisory Missions remain compatible with Territorial Defence. A 165 by 128 pixel card check on the 96 by 130 grid found no overlapping focus bounds. Browser QA passes all 120 focus clicks across 15 view/viewport combinations at widths 320, 736, and 1024, with pan, zoom, and drag checks passing. The full context preview shows all focus cards without clipping or overlap. The foreign preview uses the available Cuba icons and keeps the partner offers visually separate.

## Evidence files

- Current graph and merge declarations: `FOREIGN_POLICY_CONCEPT.json`.
- Count and build metadata: `VALIDATION.json`.
- Approved source prerequisites and focus IDs: `tools/cuba_1970/approved_design.json`.
- Builder prerequisite replacement logic: `tools/cuba_1970/foreign_concept/build.py`.
- Orthogonal preview connector routing: `tools/cuba_1970/foreign_concept/fragment.html`.
- Visual review: `PREVIEW_foreign.png`, `PREVIEW_trade.png`, and `PREVIEW_context.png`.

This review covers the concept graph and rendered proposal only. It does not validate runtime focus scripting or engine behavior.
