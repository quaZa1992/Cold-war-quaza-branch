IMPERIA COLD WAR

# Air Command implementation

Implements the user's approved Air Command expansion in the existing MD doctrine system: five new grand doctrines, fourteen new subdoctrines, thirty grand milestones, seventy mastery rewards, and permanent trade-offs for all seven inherited grands and thirty-eight inherited subs.

The immutable design package remains at `tools/air_doctrine_design_1970`. Its four approved source hashes are pinned in `baseline.json`, alongside the three complete pre-integration MD doctrine files. Do not regenerate that baseline from the installed output. All unrelated project changes must remain untouched.

- `build.py`: deterministic runtime generator. Reads the frozen baseline and approved values, applies documented native role/capability adapters, and writes fourteen runtime files (including shared research GUI, UAV-category and equipment-enum integrations). `--check` is read-only.
- `integration_baselines.json`: original shared GUI/enum/air-unit sources and the nine native legacy-idea definitions, used to preserve unrelated content and record side-effect corrections.
- `record_implementation.py`: emits installed values and current evidence summaries.
- `texts.py`: concise English historical descriptions, measured against the native text fields.
- `validate.py`: independent installed-value comparison, persistent penalty checks at every progression stage, native text measurements, references, icons, encoding and generator drift. Writes `validation.json` and `text_layout.json`.
- `export_icons.py`: copies the nineteen original transparent ImageGen masters, then crops transparent bounds, scales and converts them to native 64 x 64 BGRA DDS. It does not repaint source artwork.
- `imagegen_sources.json`, `icon_manifest.json`, `masters/`, `icon_review.png`: exact prompts, original generation paths, style donors, original masters, file hashes and native-size asset review.
- `native_probe.py`: freezes scripts into a new private profile under `E:/HOI4_Mod_Tools/mdcoldwar/runtime/air_doctrine_1970`. It never follows asset junctions. It launches and terminates only its own hidden game process. Full engine logs remain on E:.
- `native_run_location.json`, `native_result.json`: latest bounded native test evidence. Prior runs remain intact on E:.

Commands from the repository root:

```powershell
python tools/air_doctrine_implementation_1970/build.py
python tools/air_doctrine_implementation_1970/build.py --check
python tools/air_doctrine_implementation_1970/validate.py
python tools/air_doctrine_implementation_1970/export_icons.py
python tools/air_doctrine_implementation_1970/native_probe.py --prepare --run --duration 420
```

The native probe checks every grand, every subdoctrine's completed mastery, each grand's immediate cost, doctrine-switch cleanup, legacy hidden-spirit removal, historical RPV availability and equipment recognition. Forced doctrine selection is distinct from the separately tested availability conditions. These checks do not establish live UI appearance, save-file replay across versions, multiplayer synchronisation or competitive balance. See the implementation record for current results and limits.

Historical sources and balance rationale are recorded in `docs/air_doctrine_concepts_20261029.md` and `docs/air_doctrine_values_20261029.md`. Artwork and upstream rights are recorded in `NOTICE.md`.
