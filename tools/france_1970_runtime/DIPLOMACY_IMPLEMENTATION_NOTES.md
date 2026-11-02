IMPERIA COLD WAR

# France 1970 bilateral runtime notes

## Generator boundary

`diplomacy.py` is a pure generator. `build_diplomacy(design)` returns five repo-relative UTF-8 script files and English localisation key/value pairs. It does not write into the loaded mod. The root integration owns installation and the native game validation.

The output is bounded to the nineteen fixed-recipient offers and eight partner tags in the approved France 1970 design. It creates a recipient-side accept/decline decision for each pending offer and a France-side reissue decision for the original partner. No event, image, or country-wide recipient menu is emitted. MD's available decision is the recipient notification surface.

## Runtime behavior

- The focus completion helper only opens the named proposal. Both countries receive 90-day pending flags; France also receives the family-pending flag. A 180-day sender cooldown controls reissue. A refusal clears pending state and starts the same cooldown. Reissue eligibility keys off the completed source focus, so a proposal blocked by temporary partner or relation conditions can be sent later without replaying its focus rewards.
- Acceptance rechecks the fixed recipient, pair status, both GDP values, France's source-focus and party gate, all source technology and activation gates, and both sides' building ownership, full control, and physical building cap before any setup debit or award. Current design assets are unique per side/state/building; the generator rejects repeated assets that would need combined capacity math.
- Each signatory pays its own `gdp_total` share once at acceptance. The stream helper contributes its own annual-GDP share divided by 52 to `additional_expenses_rate` while the paired signed flags and activation conditions remain valid. It calls the France domestic expense helper only in France scope and exits immediately for countries outside France and the eight named partners.
- Treaty sync is France-scope guarded and runs daily before domestic programme synchronization. It keeps the two offer-specific spirits present together while both signatures, peace, no mutual native embargo, no mirrored diplomatic/financial/economic/military sanctions, and any actual parent/membership ideas remain valid. Suspension removes both spirits but leaves signed flags intact; restoration re-adds spirits without repeating fees, buildings, research, doctrine or experience.
- A bounded daily cleanup checks only the eight named partner tags. If France no longer exists, it removes this feature's recipient-side bilateral spirits while retaining signed flags and other country state.
- Preview helpers use `TT_IF_THEY_ACCEPT`, country-name headings, native spirit/research/doctrine/building/slot/experience/opinion effects, and short numeric setup-share and weekly-expense lines. They are intended to be called inside the caller's non-executing `effect_tooltip` block.

## Native source evidence and custom additions

Native behavior referenced by the generator:

- `common/scripted_effects/00_money_system.txt:3701-3726` resets and accumulates weekly `additional_expenses_rate`; the output contributes via the same accumulator.
- `common/scripted_triggers/COLDWAR_CUB_1970_bilateral.txt:1-10` demonstrates bilateral war, embargo and mirrored sanction checks. The France helper expands the same native arrays across all four sanction classes and both directions.
- `tools/building_grants/grants.py:134` emits the native shared-slot grant immediately before `add_building_construction` with `instant_build = yes`. `tools/building_grants/README.md` records the physical-level capacity policy used by the acceptance preflight.
- Native `gdp_total`, `modify_treasury_effect`, `add_tech_bonus`, `add_doctrine_cost_reduction`, and `add_to_variable` are used with the approved design's source keys and values.

The custom elements are the `COLDWAR_FRA2_*` offer IDs, flags, fixed-recipient decisions, quote loc keys, offer ideas, pair-lifecycle reconciliation, and GDP-share transaction math. They are compiled into the installed mod. `NATIVE_RESULT.json` records the current native result; browser checks, human decision UI, save/reload and live multiplayer are separate evidence levels.

France starts with the native CoCom military restriction against the Soviet Union. The user's rule excludes cooperation under any bilateral sanction class, so the Soviet offer remains blocked until that restriction is lifted through the existing system. The focus can be completed and its proposal renewed after relations qualify. The runtime never clears the restriction itself.

## Handoff validation bounds

The generator's bounded smoke check should confirm nineteen offers, all five marked output files, no BOM, and the expected loc set. Root integration should then validate decision visibility in each named recipient, refusal/reissue timing, preflight failure with changed ownership/capacity, paired suspension/restoration, all eight partner sanctions in both directions, current-GDP weekly arithmetic, and that no setup or one-use award repeats after reload or suspension. The generator agent did not run the game or install these outputs.
