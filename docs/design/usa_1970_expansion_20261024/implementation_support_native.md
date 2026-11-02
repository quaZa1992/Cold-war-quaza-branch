IMPERIA COLD WAR: Isolated native probe and event-frame inspection

24 October 2026. Read-only feasibility inspection. No game process was launched or stopped, no profile was changed and no previous snapshot was reused.

## Available native test path

The executable exists at `E:/SteamLibrary/steamapps/common/Hearts of Iron IV/hoi4.exe`. The Windows file-version fields both say `1.0`, so they are not evidence of the actual game patch. At inspection, `Get-Process -Name hoi4` returned no process. CIM command-line inspection was unavailable under the current process permissions; this does not justify changing system permissions. Approximately 52.9 GB was free on C and 1.45 TB on E.

`tools/multiplayer_quality/native_probe.py` provides a useful hidden-window launch pattern with these arguments:

```text
hoi4.exe -noasserts -assertsdialog=no -userdir=<isolated profile> -start_tag=USA -start_speed=5 -hands_off
```

Its `STARTUPINFO` sets `STARTF_USESHOWWINDOW` and `wShowWindow = 0`. The default 1970 bookmark is `common/bookmarks/the_gathering_storm.txt`, dated `1970.1.1.12`, `default = yes`, default country USA. A prior recorded run reached startup, first hour, first day, a weekly checkpoint and 9 January 1970. That proves the old driver could start this scenario; it is not a test result for the current US implementation.

The existing driver cannot be used unmodified for this task without sharing mutable state:

- `PROFILE` is fixed to `tools/multiplayer_quality/runtime`.
- `--snapshot` is constrained to a descendant of `tools/multiplayer_quality`.
- `--out-dir` is constrained to `docs/audits`.
- Running without `--snapshot` copies a broad script snapshot and returns before launching; asset junctions must be prepared separately.
- Running with `--snapshot` rewrites the shared profile, fixture, mod descriptors, settings and enabled-mod list, and archives shared logs.

For an isolated US test, adapt the driver in the USA task-owned tools directory with distinct profile, fixture, snapshot and report paths. Do not write the existing multiplayer-quality runtime or old snapshots. Freeze the scripts under test rather than referencing mutable live scripts, record hashes, and isolate assets through read-only references/junctions with verified targets. The driver should terminate only the process handle it created, never all `hoi4.exe` processes.

The old calendar probe stops on an exact per-run completion marker or duration. Its report truthfully separates first-hour/startup, weekly/monthly progression, unperformed save/reload and multiplayer testing. Preserve that distinction. A prior native report has `calendar_complete = false` and thousands of inherited diagnostic lines; do not reuse it as a passing baseline for a new US test.

## Country-event geometry

The current `interface/eventwindow.gui` is byte-identical to the installed original MD donor. SHA256: `c9d314401c37d35c86533b0102e199df277c4913c5768349d4a0d76845bed220`.

The inspected complete ordinary country-event window is 581 x 427. Its title section is at (0, 0), 581 x 121; description section at (0, 121), 580 x 100, with a 512-pixel text width and 230-pixel text maximum height. Its bottom section begins at (0, 221), 581 x 206, with clipping disabled.

Within that bottom section:

- `event_picture` is at (5, 5).
- `event_pic_clip` is at (-3, 35).
- `options_grid` is at (215, -1), nominal size 300 x 30.
- The option slots are 300 x 47, one horizontal slot.
- `event_option_entry` is 300 x 47, clipping disabled.
- Its label begins at (5, 0), uses `hoi_20bs`, max width 340 and max height 40.

Thus a broad news picture can cover the adjacent option area. A sprite being registered does not establish compatibility with this window.

The existing Cuba generator and frame verification use the same donor `gfx/event_pictures/generic/elections/political_deal.dds`, exact frame 217 x 163 and photo inset (19, 6, 180, 150). The current donor hash equals the original MD donor hash, so reusing the unmodified entire texture preserves its exact frame and alpha pixels. This review did not generate a donor-composed or live-game screenshot.

## Texture classes and targeted issue

| Sprite | Actual dimensions | SHA256 | Result |
|---|---|---|---|
| `GFX_political_deal` | 217 x 163 RGBA | `ad09f566f836ec2f5fae2906818fbca58df1dfe723ca5233ec7aa5d858f8f62c` | Native country-event class |
| `GFX_handshake_black` | 217 x 163 RGBA | `294b12317e64c653a5eeef043527ec12596ae1537fc8fcb2851d7463ebe1ee53` | Native country-event class |
| `GFX_handgun` | 217 x 163 RGBA | `f65d89d4874854784d3738d65e60d79e97bed33af3322551095aaafcef745d7d` | Native country-event class |
| `GFX_declined_offer_no` | 217 x 163 RGBA | `71cb3ca9a75245b7b0d012651800e1ef449ae940ab47cb2d92c5d1ffe4051f7b` | Native country-event class |
| `GFX_news_usa_nsa_bahrain` | 397 x 153 RGBA | `2b95c8ef92684b571ef7aa3373a8c49a5c5706820cdf8e34fb641c079351e6de` | Broad news class |

All five source texture hashes match the original MD donor. The broad Bahrain picture is used in ordinary country events at `events/COLDWAR_USA_bahrain_base_events.txt:9` and `:95`. These are the confirmed targeted image-class defects. Reusing an appropriate unchanged framed country picture resolves the geometry without changing global GUI or frame pixels. The generic pictures in the ordinary US, Nixon and Gulf modules are already correctly dimensioned and should not be replaced just because their sprite names are generic.

Original imagery and GUI remain credited to Millennium Dawn contributors and their original sources. Individual photographers/art authors and separate redistribution permissions are unknown in this inspection. The analysis does not assign ownership or create a licence.
