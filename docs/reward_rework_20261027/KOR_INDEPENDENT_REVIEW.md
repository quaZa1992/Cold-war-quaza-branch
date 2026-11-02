IMPERIA COLD WAR

# South Korea reward emission review

Date: 27 October 2026  
Scope: read-only inspection of the installed KOR focus tree, focus completion helpers, scripted triggers, 1970 history, the canonical KOR reward overlay, native MD building definitions, and the three-country frozen graph snapshot. The native probe was still running during this review.

## Finding

**P2: native focus previews omit finite equipment, research, and doctrine bonuses.** The KOR compiler's `Compiler.preview()` renders treasury and project GDP charges, building and slot grants, policy ideas and weekly costs, but does not render `equipment_bonuses`, `tech_bonuses`, or `doctrine_bonuses` from the effective focus record. The completion helper does emit those effects behind the same `can_*` and `*_paid` one-time guard. Therefore the new bonuses are granted in play but are not visible in the focus Effects preview before taking them.

The mismatch is visible in the installed sources:

- The source preview builder handles cost, building effects and policy ideas at [COLDWAR_KOR_runtime.py](../../tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_runtime.py#L258). The completion path appends `native_leaf_effects` at [COLDWAR_KOR_runtime.py](../../tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_runtime.py#L343), which includes the direct finite bonuses.
- The installed `air_cover_priority` focus tooltip shows the charge, policy idea and weekly cost, while its completion helper grants fighter build cost -0.04 and one `CAT_aircraft` bonus of 0.5 with one use. Compare [COLDWAR_KOR_1970_focus.txt](../../common/national_focus/COLDWAR_KOR_1970_focus.txt#L6283) with [COLDWAR_KOR_1970_focus.txt effects](../../common/scripted_effects/COLDWAR_KOR_1970_focus.txt#L3736).
- The same omission affects the overlay bonuses for `technical_colleges`, `industrial_laboratories`, `joint_staff`, `changwon_production`, `escort_priority`, `mobile_deterrence`, and `counterbattery_priority`. Actual helper records are at [COLDWAR_KOR_1970_focus.txt effects](../../common/scripted_effects/COLDWAR_KOR_1970_focus.txt#L2061), [#L2078](../../common/scripted_effects/COLDWAR_KOR_1970_focus.txt#L2078), [#L2481](../../common/scripted_effects/COLDWAR_KOR_1970_focus.txt#L2481), [#L4682](../../common/scripted_effects/COLDWAR_KOR_1970_focus.txt#L4682), [#L3775](../../common/scripted_effects/COLDWAR_KOR_1970_focus.txt#L3775), [#L2353](../../common/scripted_effects/COLDWAR_KOR_1970_focus.txt#L2353), and [#L3814](../../common/scripted_effects/COLDWAR_KOR_1970_focus.txt#L3814).
- The emitted KOR helper file contains five `add_equipment_bonus` records, eight `add_tech_bonus` records, and one `add_doctrine_cost_reduction` record. The affected native previews show no corresponding bonus line. The base Changwon military-production focus has the same omission for its two finite research grants and equipment savings.

This is a presentation defect, not evidence that the guarded completion transaction fails. The source-only remedy is to mirror each finite bonus in `Compiler.preview()` using the same structured focus payload as completion. No generation or native-probe result is claimed here.

## Checks with no source-level issue found

- The overlay has 68 policy entries and 21 project records affecting 80 unique focus IDs. Seventeen project records add 18 building levels; four remaining project records add bounded military bonuses without buildings. All 17 construction packages add 0.5% to 1.5% GDP and have a positive-GDP availability guard. The four bonus-only packages preserve their existing focus and recurring-policy charges; `mobile_deterrence` has no setup Treasury charge but retains its $0.005 billion weekly cost.
- Static comparison of the installed completion helpers against the project records found all 18 added building levels. Each level has one shared building slot in that same state, and every slot grant is emitted before any construction in the one-time completion helper. All project states have separate ROOT ownership and control checks. Building caps match the emitted aggregate state bundle, including shared-cap groups. No state/cap/slot mismatch was found in this source comparison.
- GDP increments are added to the focus's existing fixed Treasury charge inside the paid completion guard. The `can_*` trigger blocks nonpositive GDP for every GDP-share project; the preview also displays the project fraction. The existing runtime contract has no Treasury-affordability requirement, so this review does not treat a negative cash balance as a defect.
- The five equipment bonus grants use installed family keys: `infantry_weapons_type`, `artillery_equipment`, `fighter`, `frigate`, and `medium_tank_chassis`. All cost values are negative `build_cost_ic` changes, from -0.04 to -0.06. The eight finite research grants use the project's documented MD categories at 0.5 bonus and one use; the doctrine grant uses `add_doctrine_cost_reduction` with `land_doctrine`, 0.25 reduction and one use. Equipment and technology rewards are each emitted once in the paid helper; this review found no duplicate KOR bonus call.
- Party and leader programmes retain their native ownership checks. Programme activation also requires the focus paid receipt and the latest slot sequence value; refresh removes an inactive programme when its party or leader condition changes and can restore the earned programme if the condition returns. The paid flag keeps construction, Treasury charges, and one-time bonuses from replaying.
- The history source starts KOR with Park Chung Hee and ruling-party value 0. The reward overlay changes no focus IDs, conditions, party slots, transition receipts, or historical leader records.

## Evidence limits

This is a static source review. It does not establish how HOI4 formats the hidden native bonuses in a live tooltip, whether a displayed tooltip wraps within the game UI, or whether the native save/rehost probe passes. Those checks were pending at review time.

## Final integration resolution

The finite-bonus preview omission is resolved in Compiler.preview(). Exact structured equipment, research and doctrine payloads now appear once in both native focus previews and guarded helpers. All 300 records are checked for payload parity. A later affordability correction also supersedes the fixed-price observations above: all 111 positive domestic setup prices now use GDP fractions. Pohang costs 1.75% of current GDP in total, rather than a fixed $3B plus the project share. Existing negotiated foreign-contract fees remain unchanged. The final native probe confirms both levels and slots, the 1.75% debit, aggregate native-capacity rejection, zero-GDP rejection and replay protection. The 26 modeled scenarios pass. Manual tooltip readability and multi-client behavior remain unverified.
