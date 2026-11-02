# IMPERIA COLD WAR — Civilian shelter construction pictogram.
"""Fit the generated shelter to its native tile and patch only building frame 39."""

import hashlib
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FRAME = 46
FRAME_INDEX = 38
STRIPS = ("building_icon_strip.dds", "building_icon_without_bg_strip.dds")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def outside_bytes(im):
    return im.crop((0, 0, 1748, 46)).tobytes() + im.crop((1794, 0, 1840, 46)).tobytes()


def make_frame():
    master = Image.open(HERE / "shelter_master.png").convert("RGBA")
    # Ignore the generator's nearly invisible alpha=1 fringe for bounds only.
    # Keep the original alpha inside the selected crop.
    bounds = master.getchannel("A").point(lambda v: 255 if v > 1 else 0).getbbox()
    assert bounds is not None
    motif = master.crop(bounds)
    motif.thumbnail((36, 31), Image.Resampling.LANCZOS)
    background = Image.open(HERE / "native_blank_frame.png").convert("RGBA")
    assert background.size == (FRAME, FRAME)
    # Centre the broad shelter vertically and retain the native blank MD bezel.
    xy = ((FRAME - motif.width) // 2, 8 + (31 - motif.height) // 2)
    background.alpha_composite(motif, xy)
    background.save(HERE / "frame_39.png")
    return background, {"master_alpha_bounds": list(bounds), "motif_size": list(motif.size), "position": list(xy)}


def patch_strip(path, frame):
    before = path.read_bytes()
    assert before[:4] == b"DDS " and len(before) == 128 + 1840 * 46 * 4
    header = struct.unpack("<31I", before[4:128])
    assert header[2:5] == (46, 1840, 7360), "Unexpected DDS dimensions or pitch"
    assert header[18:26] == (32, 65, 0, 32, 0xFF0000, 0xFF00, 0xFF, 0xFF000000), "Expected native BGRA DDS"
    original = Image.open(path).convert("RGBA")
    assert original.size == (1840, 46)
    raw = frame.tobytes("raw", "BGRA")
    updated = bytearray(before)
    for y in range(FRAME):
        start = 128 + y * 7360 + FRAME_INDEX * FRAME * 4
        updated[start:start + FRAME * 4] = raw[y * FRAME * 4:(y + 1) * FRAME * 4]
    path.write_bytes(updated)
    current = Image.open(path).convert("RGBA")
    assert before[:128] == updated[:128]
    assert outside_bytes(original) == outside_bytes(current), "Another building frame changed"
    assert current.crop((1748, 0, 1794, 46)).tobytes() == frame.tobytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "before_sha256": digest(before),
        "after_sha256": digest(bytes(updated)),
        "outside_frame_rgba_sha256": digest(outside_bytes(current)),
        "frames_1_to_38_unchanged": True,
        "uranium_frame_40_unchanged": True,
        "dds_header_unchanged": True,
        "frame_39_matches_export": True,
    }


def make_preview(frame):
    old = Image.open(HERE / "native_frame_source.png").convert("RGBA")
    preview = Image.new("RGB", (400, 256), (30, 32, 35))
    draw = ImageDraw.Draw(preview)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 17)
        small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)
    except OSError:
        font = small = ImageFont.load_default()
    for x, label, im in [(18, "Previous", old), (216, "Civilian Shelter", frame)]:
        draw.text((x, 10), label, fill=(230, 230, 230), font=font)
        preview.paste(im.resize((138, 138), Image.Resampling.NEAREST), (x + 15, 40), im.resize((138, 138), Image.Resampling.NEAREST))
        preview.paste(im, (x + 61, 190), im)
    draw.text((15, 240), "Asset preview: 3x above, native 46 px below", fill=(170, 176, 182), font=small)
    preview.save(HERE / "preview.png")


def main():
    frame, layout = make_frame()
    reports = [patch_strip(ROOT / "gfx/interface/buildings" / name, frame) for name in STRIPS]
    make_preview(frame)
    report = {
        "project": "IMPERIA COLD WAR",
        "feature": "Civilian shelter construction pictogram",
        "date": "2026-10-30",
        "generation": "OpenAI built-in ImageGen",
        "prompt": "PROMPT.txt",
        "source": "shelter_master.png",
        "source_sha256": digest((HERE / "shelter_master.png").read_bytes()),
        "native_blank_donor": "Frame 21 from gfx/interface/buildings/building_icon_strip.dds before this change",
        "original_frame_source": "native_frame_source.png",
        "frame": 39,
        "frame_rgba_sha256": digest(frame.tobytes()),
        "layout": layout,
        "strips": reports,
        "verification": "Decoded pixels, alpha, DDS header and all 39 other frames checked; no live-game screenshot or engine test.",
    }
    (HERE / "manifest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"project": report["project"], "frame": 39, "motif": layout, "other_frames_unchanged": True, "outputs": [item["path"] for item in reports]}))


if __name__ == "__main__":
    main()
