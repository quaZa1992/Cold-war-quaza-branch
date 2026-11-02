IMPERIA COLD WAR

# COLDWAR_KOR — approval-stage national focus concept

This directory is the canonical source for the January 1970 South Korean focus concept. It does not install or overwrite any game file. The owner requested a complete visual design and effects first, followed by an approval stop.

Revision 2 contains 298 focuses (+92; 44.7% growth), 55 mutually exclusive choice groups (61 pair links, including three three-way choices), 14 programme clusters, nine starting spirits (eight proposed plus the existing overseas-employment spirit), 29 diplomatic contracts and 17 historical event stages. Every original programme grows; 36 new focuses form a shared military-to-democratic transition. English text only. Prefix all eventual content with `COLDWAR_KOR_` and preserve the shared project contracts.

## Sources and outputs

- `COLDWAR_KOR_build_concept.py`: authored programme graph, effects and starting-spirit data.
- `COLDWAR_KOR_contracts.py`: concrete bilateral terms, ownership and refusal rules.
- `COLDWAR_KOR_review_fixes.py`: historical/geometry/semantic corrections from independent review.
- `COLDWAR_KOR_expansion.py`: researched92-focus expansion and resolved layout.
- `COLDWAR_KOR_alliance_revision.py`: effective 300-focus alliance and diplomacy revision.
- `COLDWAR_KOR_reward_revision.py`: derived reward overlay applied after the alliance revision; it leaves the approval-stage design JSON unchanged.
- `COLDWAR_KOR_transition_plan.py`: transition receipts, concrete ballot arithmetic, repeatable ratification, command outcomes and court implementation.
- `COLDWAR_KOR_native_plan.py`: proposed new provider contracts and existing MD primitive recipes. These are specifications, not loaded APIs.
- `COLDWAR_KOR_tree_fragment.html`: interactive preview template.
- `COLDWAR_KOR_render.py`: native-art previews and English catalogue.
- `COLDWAR_KOR_validate.py`: independent graph, geometry, title-width, modifier-reader and lifecycle checks.
- `COLDWAR_KOR_preview_smoke.js`: minimal DOM wiring test for every focus, programme, institutional stage and camera control; no browser-layout claim.

Outputs stay under `docs/design/COLDWAR_KOR_1970`, except the inline preview in this chat’s explicitly writable visualization directory. The approved design JSON remains the immutable baseline. The effective loader adds the alliance and reward overlays in memory before preview and native emission. Preview fonts, symbol placement and connector routing are approximations; engine tests follow implementation.

The 68-policy reward overlay, 21-project package layer, and domestic GDP cost scale, with before/after manifest and research record, live in `docs/reward_rework_20261027/KOR_reward_revision.json`, `KOR_reward_change_manifest.json`, and `KOR_REWARD_RESEARCH.md`. The effective loader applies this overlay after building the alliance revision. The overlay covers 80 unique existing focus IDs. It adds 18 paid levels across 17 packages and finite weapon-family, research, and doctrine rewards. Positive domestic focus setup charges convert to 0.25% of GDP per legacy $1bn, capped at 2% for the base fraction; project increments combine into one GDP-based Treasury charge. Native previews show that total charge and every building slot. Bilateral contract terms remain separate and unchanged. Do not copy computed values into the approved base JSON.

## Rebuild

Run with the bundled Python runtime, in this order:

```text
python tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_build_concept.py
python tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_render.py
python tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_validate.py
node tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_preview_smoke.js <absolute-inline-fragment-path>
```

No broad generator or installer is called. Preserve script UTF-8 without BOM and English-localisation UTF-8 with BOM in the later implementation phase.

## Approval boundary and next phase

Wait for explicit approval of this concept before writing `common`, `events`, `history`, `interface` or `localisation`. After approval, implement from the approved JSON rather than an old image. Reconcile the country’s1970 party registry with legacy leader pools and retirement routing, create the declared KOR providers, integrate the existing NKO ledger without duplicate rewards, then stage and independently parse the emitted code. Verify start/hover/rewards, refusal/expiry, government change/return, save/reload, construction capacity and actual MD routing in HOI4.

Do not interpret the static PASS as an engine test or the new `COLDWAR_KOR_*` provider specifications as existing runtime helpers. Balance numbers are proposals awaiting multiplayer review.

