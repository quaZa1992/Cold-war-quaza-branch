# COLDWAR UAE: installed focus layout and presentation review

> Historical review of the original 107-focus installation. Current geometry, artwork and reward presentation are covered by [the maritime and visible-reward review](MARITIME_REWARD_REVIEW.md); [the industrial-development review](INDUSTRY_DEVELOPMENT_REVIEW.md) and [the intermediate 108-focus independence revision](USER_REVISION_LAYOUT_AND_PRESENTATION_REVIEW.md) are also retained. The original evidence below is historical; current source hashes and proof sheets are in `LAYOUT_REVIEW.json`.

Reviewed 19 October 2026. This review reads the emitted focus, GFX, English localisation and programme files from the loaded mod. It does not import or run the compiler to obtain focus coordinates. The immutable approved catalogue has SHA-256 `23e89bc7f0a02f4df337248bcfa67d139ec8fc910c414978a3f5ef5913158272`.

**Result: installed focus geometry, English titles, durations, grouped prerequisites, exclusions and native artwork match all 107 approved focuses. The three completion-presentation findings identified during staging have been corrected.** Diplomacy and political integration were still being completed in parallel and are not certified by this report.

## Reproducible evidence

Run `python tools/uae_1970/audit_layout.py`. The independent parser reconstructs the emitted Clausewitz blocks, recursively resolves relative anchors and reads the actual English/GFX registrations. It writes only this evidence directory:

- `LAYOUT_REVIEW.json`: current source hashes and machine-readable findings.
- `FOCUS_MANIFEST.json`: actual source line, anchor, offsets, resolved position, title, description, duration, logical prerequisites, exclusions and texture hash for every focus.
- Twelve `BRANCH_*.png` files: native-scale card proofs reconstructed from emitted source, native DDS pixels, inherited titlebars and the actual Ubuntu Bold 16 bitmap atlas. Connector paths and unavailable shading are external approximations.

At this review the machine report contains zero errors, zero warnings and zero unrelated visible-card intersections. There are 107 focuses, 95 relative anchors, 12 programme roots and 24 reciprocal exclusive pairs. The maximum title advance is 142 pixels inside the 147-pixel field.

## Geometry and visual result

Every emitted absolute position agrees with the approved catalogue. Every OR group remains one prerequisite block; multiple blocks retain their AND relationship. Exclusions and nominal durations agree independently with the approval data. No relative anchor is missing or cyclic. The source opening camera targets `COLDWAR_UAE_treaty_coast`, and there is a shortcut for each of the 12 programme areas.

The independent reconstructions were compared with the approved proof sheets below their annotation headers. All twelve card/connection bodies are pixel-identical. The reconstructed British, oil and compact constitutional sheets were also opened and visually inspected. Negative-x cards remain visible, the offshore investment extension fits, compact two-unit choices retain readable titles, and no header/card clipping or unrelated card crossing was observed. The existing whole-tree footprint and all neighbouring programmes are preserved.

The continuous-focus panel has a deliberately separate source position, outside the card tree. Exact engine panel bounds, scroll limits, native connector routing, hover cards, current/completed shading and initial-camera behaviour remain in-game checks. These source reconstructions are not screenshots of a running HOI4 session.

## Art closure

The emitted `GFX_COLDWAR_UAE_<focus suffix>` aliases point to the same approved native MD textures, without a bitmap conversion or global GUI change. Every focus has its matching `_shine` registration, using the same base texture as its mask and the native `gfx/FX/buttonstate.lua` logical effect alias plus `shine_overlay.dds`. That effect alias follows main MD `interface/goals_shine.gfx`; a literal `.lua` file is not required to duplicate the native engine provider.

Starting spirits, twelve programme modifiers and accepted UK/UAE treaty spirits have separate `GFX_idea_` aliases. The two prime-minister office ideas use the approved civil-administration art. Source aliases are verified; their exact in-game national-spirit sizes and shader animation remain engine checks.

## English narrative and effect presentation

The 107 emitted focus descriptions equal `flavour.FOCUS_DESCRIPTIONS`. The six non-treaty starting-spirit descriptions equal `SPIRIT_DESCRIPTIONS`; diplomacy owns the starting treaty spirit's text. English localisation files have their expected UTF-8 BOM and English header. Titles and numeric rewards remain approved; flavour edits describe Emirati institutions, constituencies and policy costs instead of discussing invoice bookkeeping or authoring instructions.

Representative political, public-service, oil, commercial, defence and treaty descriptions were read beside their resulting effects. The wording names the actual institution or sector and leaves numeric effects to the effect panel. The Ras Al Khaimah description no longer mentions an “invisible territorial reward,” and public-industry/offshore descriptions explain capital, labour and operating obligations in ordinary game narrative.

For the native reference, main MD Russia uses a named `modifies_dynamic_modifier_tt` heading with numeric modifier formatter rows at `05_russia.txt:410–413` and `:31904–31906`. The UAE completion preview now follows that grammar. `effect_tooltip` supplies a non-executing named programme/numeric preview; the real one-time application runs through the hidden guarded helper. Native treasury, productivity, resource, building, experience and decision-unlock effects remain visible in the preview where applicable.

The independent checker compares every displayed programme contribution and treasury debit with the approved numeric data. It confirms the native treasury provider in each costed preview and a separate hidden application call. The four oil grants remain native resource effects, and factory/office rewards remain construction queues rather than completed free buildings.

Three staging findings were corrected:

1. Interest-rate reductions initially appeared red. The current `RIGHT|-=2` formatter follows the native bad-type interest-rate definition, so a reduction is beneficial.
2. Positive political stability contributions initially omitted their approved ceiling. Relevant previews now show the common +15 percentage-point cap, with negative contributions retained.
3. Programme effects initially used a hand-built numeric catalogue. They now use named modifier headings and signed native RIGHT formatters in the non-executing preview. This preserves the real guarded application and its receipts rather than executing a payment merely to show it.

The current static source separates programme refresh from permanent capital and structural remedies: it rebuilds variable-backed active contributions from earned flags, retains the approved political stability cap and suspends government/status-bound programmes through their active conditions. Dynamic starting-spirit components have real variable consumers and their declared remedy floors. This is a source-level confirmation; live party transitions and all diplomatic contract states require the separate integration review and an eventual engine check.

## Scope limits

This report closes the focus layout, card art, title/description coverage and native numerical preview surfaces. It does not certify final startup history, the broader decision catalogue, UK event delivery, accepted-date maturity, leader succession or runtime save recovery. Those modules were being reviewed by their owners in parallel. Final source hashes are recorded in `LAYOUT_REVIEW.json`; rerun the bounded checker after the final compile if any referenced output changes.
