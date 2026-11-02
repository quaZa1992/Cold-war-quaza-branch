IMPERIA COLD WAR

# Land doctrine expansion implementation

This is the initial implementation report. The later user-authorised penalty revision is recorded in `docs/doctrine_tradeoffs_20261028.md`; that revision supersedes the affected numeric drawbacks and has its own current validation evidence. The initial concept, native result and value record remain preserved.

Implemented on 28 October 2026 following the user's approval of `docs/doctrine_expansion_20261028.md`. The two grand doctrines, twelve subdoctrines, fourteen original icons and all sixty mastery rewards are installed. Numeric bases and cumulative end states match the approved concept, including the strengthened Key Zone Defence package. Existing doctrine balance was not changed beyond the approved reciprocal identity exclusion.

## Delivered doctrines

| Native category | New choices |
| --- | --- |
| Grand doctrine | Deliberate Firepower; Mobile Raiding Warfare |
| Structure | Cohesive Unit Rotation; Integrated Support Commands |
| Operational Theory | Forest Envelopment; Heliborne Reaction Forces |
| Dedicated Doctrine | Assault Breaching; Key Zone Defence; Coastal Denial |
| Training | Opposing Force Exercises; Mission Rehearsal |
| Leadership | Institutional Combat Learning |
| Technology | Guided Anti Armour Integration; Counterfire Coordination |

Grand doctrines cost 100 Army XP and provide six native slots with six corresponding milestones. Deliberate Firepower has one of each land track. Mobile Raiding Warfare has two Operational Theory slots and no Dedicated slot. Each subdoctrine costs 75 Army XP and has five native mastery rewards. No custom polling, extra economic transaction, permanent character trait or equipment grant is added.

All choices use native numeric effects and the existing MD budget components. Aircraft, anti-tank weapons, engineers and coastal forts are not granted by selecting a doctrine. Bonuses target the approved infantry, special-forces, artillery, AT-company and support-company scopes. New country examples and AI weights do not lock player selection behind country tags, governments or historical dates.

Key Zone Defence excludes both Operational and Dedicated Territorial Defence variants. The existing Territorial Defence trigger now excludes Key Zone Defence in return, while retaining its original Total Defence parent requirement. No additional broad family exclusions were introduced.

## English descriptions and historical basis

Descriptions name the Finnish motti experience, Swedish coastal-defence planning, Austrian Raumverteidigung, South African mobile battle groups, Rhodesian Fireforce and Egyptian assault/anti-armour experience where applicable. British unit rotation, Korean logistical commands and later American training and lessons institutions provide organisational examples. Post-1970 examples are dated rather than presented as organisations already operating at the January start.

The detailed historical research and direct source links are retained in the approved concept. Its sources include Tuunainen's motti research, the Austrian defence ministry and military journal, Lagerberg's contemporary 1959 report, Scientia Militaria, U.S. Army histories, contemporary artillery publications and the GAO's 1984 training evaluation. Numerical benefits and penalties are game-balance choices rather than measured historical effectiveness.

All fourteen selection names fit the native 140 x 50 name field at `hoi_20bs`. All fourteen descriptions fit four 18-pixel lines within the existing 460 x 80 field at `hoi_18mbs`. Measurement uses the actual inherited BMFont advances, not a generic character count. Full results are in `tools/doctrine_expansion_1970/text_layout.json`. The shared GUI geometry is unchanged.

## Icons and provenance

Fourteen new transparent icons follow the existing black/silver/orange MD doctrine pictograms. The runtime textures are 64 x 64 uncompressed BGRA32 DDS, with decoded colour and alpha verified against the prepared PNGs. Native scale and enlarged versions are shown in `tools/doctrine_expansion_1970/icon_review.png`.

The built-in OpenAI ImageGen tool generated the original masters under Codex's direction. Existing MD doctrine textures were supplied as style references. Individual reference artists and separate redistribution permissions are unknown. Exact prompts, source paths, copied original masters, reference records and content hashes are retained in `tools/doctrine_expansion_1970/`. See its `NOTICE.md` and the runtime directory's companion notice. The project marker does not assign third-party rights.

## Files and regeneration

- `common/doctrines/grand_doctrines/mdcw_land_doctrine_expansion.txt`
- `common/doctrines/subdoctrines/land/mdcw_land_doctrine_expansion.txt`
- `common/scripted_triggers/00_doctrines_scripted_triggers.txt`: file-start integration notice and one reciprocal exclusion only.
- `interface/mdcw_land_doctrine_expansion.gfx`
- `localisation/english/mdcw_land_doctrine_expansion_l_english.yml`
- `gfx/interface/doctrines/icons/land/mdcw_expansion/`: fourteen textures and a companion notice.
- `tools/doctrine_expansion_1970/`: source model, generator, exporter, verification and compact evidence.

Every new code file starts with the exact IMPERIA COLD WAR project marker. Scripts and graphics registration use UTF-8 without BOM. English localisation uses UTF-8 with BOM, with its marker immediately after `l_english:`. No translations, changelog rewrite, branch change or commit are included.

## Source verification

`python tools/doctrine_expansion_1970/validate.py` completed successfully with **214 of 214 checks passing**. The report contains every check, actual cumulative values and source hashes.

Coverage includes exact approved end values for all fourteen packages, six milestones per grand, five rewards per subdoctrine, costs, six-category distribution, native unit scopes, self-duplicate guards, reciprocal Territorial/Key Zone conflicts, preservation of unrelated MD triggers, complete English keys, no collisions with existing English keys or registered sprites, native text-field fit, DDS headers/transparency and generator parity. Final output uses no negative workforce modifiers or unsupported one-time reward substitutes.

## Native engine verification

The isolated hidden HOI4 run used a frozen script snapshot at:

`E:/HOI4_Mod_Tools/mdcoldwar/runtime/doctrine_expansion_1970/20261028_182046/`

It reached its completion marker on **2 January 1970 at 15:00** after 207.5 seconds of wall time. Fixtures were confined to the private profile and did not alter the user's normal game or live mod scripts.

Observed results:

- The two new grand doctrines loaded and were assigned successfully. Total Defence also accepted the new options in its existing slots.
- Twenty-four slot checks across USA, Egypt, Austria and South Africa passed, covering **all twelve new subdoctrines at complete mastery**.
- The actual Territorial Defence scripted trigger rejected the conflict while Austria held Key Zone Defence.
- Switching the test USA from fully mastered Deliberate Firepower to Mobile Raiding Warfare changed its observed artillery modifier from 0.2 to 0.0. The old grand's +20% artillery bonus was removed.
- No error-log lines referencing the new doctrine files or IDs were found. Existing unrelated mod diagnostics remain in the full private log; this is not a claim of a warning-free repository.
- Only the test process created by this run was stopped after completion.

The tested doctrine scripts, trigger and graphics registration exactly match the installed hashes. The subsequent English-description shortening affects text only and passed the final source/font checks. The native run used live asset junctions; texture hashes are recorded in the separate icon manifest.

An attempted screenshot of the hidden test window captured an unrelated occluding window. It is not retained or offered as game evidence. The icon review is a composed asset preview, and bitmap-font measurement is source-level UI evidence. Live tooltip appearance, save/reload, rehost and multi-client balance remain unverified.

Compact native evidence is in `tools/doctrine_expansion_1970/native_result.json`; the full logs and immutable snapshot hashes remain on E:. The test uses direct fixture effects to populate doctrine slots. It verifies native assignment and mastery execution, not a complete player click-through of every XP purchase.
