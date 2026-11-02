IMPERIA COLD WAR

# Land doctrine expansion implementation tools

User-approved source: `docs/doctrine_expansion_20261028.md`. The implementation adds two grand doctrines and twelve subdoctrines with their exact approved bases and progression values. Historical countries guide the English descriptions and soft AI preferences; they do not restrict player access.

The user's subsequent stronger-trade-off request is implemented in `balance_revision.py` and documented in `docs/doctrine_tradeoffs_20261028.md`. It supersedes the affected activation penalties for six expansion and six legacy choices while preserving positive rewards. The original concept and initial reports remain historical records, not the current penalty specification.

The 29 October follow-up is owned by `coverage_revision.py` and documented in `docs/doctrine_coverage_20261029.md`. It extends foot/SF coverage, replaces general artillery attack with a native category modifier covering MLRS as well, adds immediate missing grand/school trade-offs, grants early Mission Rehearsal planning, and corrects forced-green unit-stat formatting. `validate_coverage.py` compares all 71 installed land entries against the immutable pre-revision semantic input and checks every mastery stage. `coverage_validation.json` is its complete result; earlier evidence files remain historical.

`coverage_revision_evidence.json` records the successful corrected native run, all eighteen runtime hashes, fourteen grand-penalty observations and twenty-seven mastery slot checks. The first attempt and its missing-token diagnostic remain recorded separately. A new token can be loaded from a separately hashed fixture overlay when reusing an immutable snapshot. The user's Escape ended Computer Use during loading; no further UI actions or live colour-verification claim followed.

`design.py` owns the packages, native unit scopes, sixty mastery rewards, English text and AI preferences. `build.py` emits the two doctrine files, English localisation and sprite registrations. It also adds the reciprocal Key Zone Defence exclusion to the existing Territorial Defence trigger without replacing unrelated trigger definitions. `build.py --check` compares installed output without rewriting it.

`imagegen_sources.json`, `masters/`, `icon_manifest.json` and `NOTICE.md` preserve the original generated artwork, prompts, source credits, unknown reference permissions, export details and hashes. `export_icons.py` performs transparent crop, proportional downscale and native BGRA32 DDS export. It does not repaint the generated artwork. `icon_review.png` shows native and enlarged assets, not an in-game screenshot.

`validate.py` checks the installed AST against independently transcribed approved end states, the explicit later penalty revision, unchanged legacy rewards, complete progression, scopes, costs, identity guards, native text-field geometry, duplicate references, encoding and DDS storage. `validation.json` contains every current check and source hash. `text_layout.json` preserves native font line measurements.

Commands from the repository root:

```text
python tools/doctrine_expansion_1970/build.py
python tools/doctrine_expansion_1970/export_icons.py
python tools/doctrine_expansion_1970/build.py --check
python tools/doctrine_expansion_1970/validate.py
python tools/doctrine_expansion_1970/validate_coverage.py
```

Native tests use `native_probe.py --prepare`, followed by `native_probe.py --run --duration 300`. Preparation creates a new private frozen script snapshot and profile under `E:/HOI4_Mod_Tools/mdcoldwar/runtime/doctrine_expansion_1970/`. It creates asset junctions without traversing them. It does not copy archives into the mod, reuse a previous test result, alter the normal HOI4 profile, or terminate another process. Native effect and trigger syntax is taken from the installed game's documentation.

The initial native run completed on 2 January 1970: four tested grand assignments, twenty-four completed slot instances covering all twelve new subdoctrines, a blocked Territorial Defence conflict and removal of the +20% grand artillery modifier on a switch. Its result is retained in `native_result_initial_20261028.json`. The revised probe also covers all six revised legacy choices and checks removal of the new supply-gap penalty. Full private logs and snapshot manifests remain on E:. `native_run_location.json` and `native_result.json` contain the current compact pointers and results.

The initial run's gameplay scripts, trigger and graphics registration matched its installed source hashes. Afterwards only the initial English descriptions were shortened to fit the existing four-line description field. The current revision validates all affected descriptions again. Native probe preparation can reuse an immutable snapshot only after matching all ten affected runtime-file hashes, while always creating a fresh profile and fixture. An attempted read-only UI capture during the initial implementation returned an unrelated occluding window, so it is not retained or counted as a visual inspection of the game. Live hover rendering, rehost/save behaviour and multiplayer balance are not certified by these tests.

See `docs/doctrine_expansion_implementation_20261028.md` for the delivered content and evidence boundaries. The approved concept remains unchanged as the design record.
