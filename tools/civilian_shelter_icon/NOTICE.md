IMPERIA COLD WAR

# Civilian shelter construction icon

Created on 30 October 2026 at the user's request to improve the civilian shelter icon shown in their construction-menu screenshot.

`shelter_master.png` is the original output from OpenAI's built-in ImageGen tool, generated with Codex for this project. The exact prompt and transparent-background setting are recorded in `PROMPT.txt`. Original saved output: `C:/Users/Enes/.codex/generated_images/01a18d47-f011-7c32-ac51-1e02adcd9e8c/exec-038c6a37-0ad1-4966-8581-8bbcb39e6e26.png`. A separate asset-specific licence or human illustrator credit is unknown; use of the generated output remains subject to the applicable OpenAI terms.

The native MD building strips supplied the style reference. The generated pictogram depicts a gold-orange reinforced shelter with a thick curved roof, a dark entrance and broad steps. It contains no visible text, watermark or third-party logo. No source photograph is used.

`native_blank_frame.png` is unchanged frame 21 from the pre-change `gfx/interface/buildings/building_icon_strip.dds`. `native_frame_source.png` is unchanged pre-change civilian shelter frame 39, retained as the small source for the comparison preview. These inherited MD/Paradox assets retain their existing rights and notices. Their individual original artists and separate redistribution permissions are unknown in the available files. The project marker does not establish ownership or replace their licence.

`build.py` performs alpha-bounds cropping, aspect-preserving downscaling, transparent compositing onto the native blank tile, and direct BGRA byte replacement of frame 39 in both building strips. It preserves all other frame bytes and the original DDS headers. `frame_39.png` is the resulting 46 x 46 source consumed by the existing uranium integration generator as well as the regression check. The source master retains its original alpha; only the almost invisible alpha=1 fringe is excluded from the crop bounds.

`manifest.json` records source/output hashes and the pixel-preservation checks. `preview.png` is an asset comparison composed locally, not a live game screenshot. Its labels use the Windows Arial font for review only; the font is not bundled or painted into runtime assets. Font rights remain with their respective owners. No gameplay, building cost, bonus or icon-frame assignment is changed.

Validation passed: the existing `Integration.test_icon_frames_keep_shelter_and_add_uranium` regression confirms both exported shelter frames, unchanged frames 1 to 38 against the immutable historical source, unchanged uranium frame 40 against its original donor, and the existing building frame assignments. Python syntax and UTF-8 without BOM checks passed for the changed tools. No live engine test was performed.

To rebuild: `python tools/civilian_shelter_icon/build.py`.
