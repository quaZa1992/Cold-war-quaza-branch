IMPERIA COLD WAR

# Chile, Brazil and Argentina event photographs

33 selected photo restorations cover 91 country events: Chile 31, Brazil 22 and Argentina 38. Political events use researched country photographs. Agreements use subject-specific industry, grain, naval, aviation, nuclear, medical or signing photographs. Existing focus rewards, decisions, consent and event options are unchanged.

The built-in `image_gen` tool restored and colorized the selected sources with natural colors, neutral white balance and clean detail resembling modern smartphone photography. Historical subjects and period equipment were retained. AI colors and restored detail are interpretations. `generations.json` contains the exact prompt set, including the Mirage canvas extension. Selected final PNG masters are retained in `masters/`; `originals/` contains the acquired source images. `sources.json` preserves the Commons metadata, source pages and credit/licence fields. [ASSET_NOTICE.md](ASSET_NOTICE.md) records credits, licence links, unknown permissions, date limitations and individual modifications.

`inspection/` contains reduced JPEG viewing copies of the original sources with the same filename keys and attribution. `local_sources/treaty.png` is the 180 x 150 photo inset from the existing MD treaty image, retained as the restoration input; its photographer and separate permission are unknown. These source copies do not change the original source licences.

The native MD donor was rechecked against the complete `EventWindow`, `bottom_Window`, `options_grid` and `event_option_entry` blocks in `interface/eventwindow.gui`. Textures are 217 x 163 pixels with an opaque 180 x 150 photo at (19,6). Every outer frame and alpha pixel is unchanged. Native BGRA8 DDS storage is verified against PNG previews. The 581 x 427 window, adjacent 300 x 47 option slots and native 340-pixel option-text width were retained. No GUI changes are installed.

`sa_photo_catalogue.py` is the shared mapping. The Chile compiler, Brazil core/diplomacy/art generators and Argentina core/politics/treaty/art generators consume it or preserve its selected references. Compatibility aliases retain old Argentina/Brazil sprite names with the new photos. Frozen approval/design files are not changed. Historical seven-image Argentina and generic Chile art reviews are superseded by the current report.

Rebuild the selected texture set and registry with:

```powershell
& 'C:/Users/sonyz/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' tools/south_america_event_art/sa_photo_export.py
```

Add `--install` only to reapply the 91 event picture references. This bounded installer checks that only picture values change. It does not rebuild or install any gameplay output. To verify the assets and future generator output without installing gameplay:

```powershell
& 'C:/Users/sonyz/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' tools/south_america_event_art/validate.py
```

Current evidence is in `docs/event_art_review/south_america_1970/`: source/output hashes, per-event bindings, integration checks, native-size contact sheets and a donor-composed event window. These previews are not live HOI4 screenshots. No live engine run, save/reload or multiplayer test is claimed. Private native test profiles and archives were not created.
