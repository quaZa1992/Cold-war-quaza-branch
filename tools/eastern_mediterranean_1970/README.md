# Eastern Mediterranean 1970 portrait build

Completed:41 new photo-based restorations (TUR20, GRE16, CYP5). The complete
Cyprus review sheet also includes the five previously approved restorations,
for10 unique people. Source photographs and full imagegen prompts are documented
in `SOURCES.md` and `generation.json`. These are restored interpretations of
historical photographs, not untouched archival originals.

Backgrounds follow each source: outdoor settings, offices, curtains, press rooms
and plain archival backdrops all remain possible. The base prompt is
“Kolorisiere es und mache das wie ein handyfoto”.

The regional runtime contains39 named characters:20 Turkish,16 Greek and3
Cypriot military figures. Makarios and Clerides use the existing Cyprus political
dispatcher. President/regent advisors are distinct from prime ministers and
party leaders. Dates expose candidates without scheduling coups, elections,
invasions or forced changes to human incumbents. Unknown political collectives
use their country's flag; named people never receive an unrelated generic face.

The CYP research roster still records commanders for whom no unambiguous still
photograph has been secured. They are not synthesized from guessed faces.

Rebuild and verify from the mod root, in this order:

```powershell
python tools/eastern_mediterranean_1970/build_assets.py
python tools/cyprus_1970/compile.py
python tools/eastern_mediterranean_1970/compile.py
python tools/eastern_mediterranean_1970/CYP/preview.py
python tools/eastern_mediterranean_1970/validate_runtime.py
python tools/eastern_mediterranean_1970/check_fixture.py
python tools/cyprus_1970/validate.py
python tools/cyprus_1970/test_transactions.py
python tools/cyprus_1970/test_north.py
```

Validation covers native script structure, actual DDS files, all48 Turkish/Greek
party slots,59 interpreted behavior cases,17 existing Cyprus/Northern Cyprus
tests, idempotence and unchanged2000 history sections. No HOI4 engine session or
multiplayer synchronization test has been performed.

`recover_outputs.py` is a one-time export-recovery aid, not a generation tool.
The selected revision records take priority over first-pass output mappings.

`build_assets.py` converts only completed, locally available portrait masters
into HOI4 leader DDS files. A supplied master may already be a source-photo AI
restoration; this script only makes a restrained 156×210 technical crop and a
38×51 small crop. It retains the master photo and its background, writes an
`assets.json` and a labeled contact sheet for each represented country, and
records the source URLs and master path. It does not generate, restore, repair,
or substitute a portrait.

For incremental work, place each completed record atomically as
`tools/eastern_mediterranean_1970/generated/TAG_key.json`. Each record contains
`country`, `key`, `name`, `master`, and may contain `source_urls` and `prompt`.
An optional `crop_box` can frame a subject that is too small in a full-scene
master. It is `[left, top, right, bottom]` in normalized source-image
coordinates, with each value from 0 to 1. This changes only the technical crop;
the master remains untouched and both DDS sizes use the same crop window.
`master` may be an absolute workspace path or a path relative to that individual
JSON's directory. An optional aggregate `generation.json` may contain a list of
the same records; relative masters there resolve against the manifest's
directory. The incremental records take precedence over duplicate entries in
the aggregate manifest. Existing prompts are preserved as metadata and are
never rewritten by the builder.

When a matching person key exists in `TAG/roster_research.json`, the researched
name is used on the contact sheet and roster source URLs are merged with any
URLs in the generation record. The builder does not invent missing source URLs.

Run from the mod workspace with:

```powershell
python tools/eastern_mediterranean_1970/build_assets.py
```

Entries with absent or empty masters are skipped and reported; no placeholder
is emitted. The output paths are `gfx/leaders/TAG/1970/COLDWAR_TAG_1970_key.dds`
and `gfx/leaders/TAG/1970/small/COLDWAR_TAG_1970_key_small.dds`. Per-country
metadata and review sheets are written under `tools/eastern_mediterranean_1970/TAG/`.

The metadata status is `source_photo_ai_restoration_technical_conversion`,
describing the master provenance and this builder's technical output. The script
reopens both DDS files and checks the expected dimensions. Review the contact
sheet before using any portrait in the game. The crop uses a modest upward bias
suited to frontal and profile source photos; it does not detect, reconstruct, or
alter facial features. To test in an isolated directory, pass `--generation`,
`--generated-dir`, and `--output-root` explicitly.
