# IMPERIA CW — Cold War: ddr currency — build icon.
"""Package an approved transparent DDR currency master as a native MD icon.

Image generation performs the creative edit. This script only preserves that
master, fits its alpha-bounded subject to the existing currency icon footprint,
and writes one uncompressed A8R8G8B8 DDS frame. It does not remove backgrounds,
repaint the emblem, recolour pixels, or change the generated alpha deliberately.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct

from PIL import Image, ImageDraw


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MASTER = HERE / "source/ddr_mark_generated.png"
TARGET = ROOT / "gfx/interface/ideas/laws/currency_ddr_mark.dds"
PREVIEWS = HERE / "previews"
CANVAS_SIZE = (72, 64)
# Matches the rouble icon's observed alpha bounds: (9, 4, 67, 64).
SUBJECT_BOX = (9, 4, 67, 64)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_native_dds(image: Image.Image, destination: Path) -> None:
    """Write the same legacy 32-bit BGRA header/payload as currency siblings."""
    if image.mode != "RGBA" or image.size != CANVAS_SIZE:
        raise ValueError("Native currency frame must be 72x64 RGBA")
    width, height = image.size
    header = (
        b"DDS "
        + struct.pack("<7I", 124, 0x2100F, height, width, width * 4, 1, 1)
        + struct.pack("<11I", *([0] * 11))
        + struct.pack(
            "<8I", 32, 0x41, 0, 32,
            0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000,
        )
        + struct.pack("<5I", 0x1000, 0, 0, 0, 0)
    )
    assert len(header) == 128
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(header + image.tobytes("raw", "BGRA"))


def create_preview(frame: Image.Image) -> None:
    """Show the shipped DDS beside unchanged existing currency textures."""
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    frame.save(PREVIEWS / "ddr_mark.png")
    frame.resize((432, 384), Image.Resampling.BILINEAR).save(
        PREVIEWS / "ddr_mark_large.png"
    )
    names = [
        ("DDR-Mark", TARGET),
        ("Rubel", TARGET.with_name("russia_rouble.dds")),
        ("Yuan", TARGET.with_name("chinese_yuan.dds")),
        ("Euro", TARGET.with_name("euro.dds")),
        ("Dollar", TARGET.with_name("us_dollar.dds")),
    ]
    cell_width, cell_height = 240, 284
    sheet = Image.new("RGB", (cell_width * len(names), cell_height), (37, 40, 36))
    draw = ImageDraw.Draw(sheet)
    for index, (label, path) in enumerate(names):
        with Image.open(path) as icon:
            icon = icon.convert("RGBA")
        enlarged = icon.resize((216, 192), Image.Resampling.BILINEAR)
        sheet.paste(enlarged, (index * cell_width + 12, 8), enlarged)
        sheet.paste(icon, (index * cell_width + 84, 202), icon)
        draw.text((index * cell_width + 8, 270), label, fill=(235, 235, 230))
    sheet.save(PREVIEWS / "currency_comparison.png")


def build(source: Path) -> dict:
    source = source.resolve(strict=True)
    with Image.open(source) as original:
        if original.format != "PNG":
            raise ValueError("Expected the approved PNG image generation master")
        if "A" not in original.getbands():
            raise ValueError("Approved master must already have a transparent background")
        master = original.convert("RGBA")
    alpha = master.getchannel("A")
    if alpha.getextrema()[0] != 0:
        raise ValueError("Master has no fully transparent background pixels")
    subject_bounds = alpha.getbbox()
    if subject_bounds is None:
        raise ValueError("Master contains no visible subject")

    MASTER.parent.mkdir(parents=True, exist_ok=True)
    if source != MASTER.resolve():
        shutil.copy2(source, MASTER)
    subject = master.crop(subject_bounds)
    left, top, right, bottom = SUBJECT_BOX
    subject.thumbnail((right - left, bottom - top), Image.Resampling.LANCZOS)
    position = (
        left + (right - left - subject.width) // 2,
        top + (bottom - top - subject.height) // 2,
    )
    frame = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    # No mask here: directly copy RGBA, preserving the antialiased source alpha.
    frame.paste(subject, position)
    write_native_dds(frame, TARGET)
    with Image.open(TARGET) as decoded:
        decoded = decoded.convert("RGBA")
        if decoded.size != frame.size or decoded.tobytes() != frame.tobytes():
            raise ValueError("DDS round trip altered the native RGBA frame")
    create_preview(decoded)

    manifest = {
        "creative_tool": "built-in image_gen",
        "packaging": "alpha-bounded fit and native BGRA DDS encoding only",
        "master": MASTER.relative_to(ROOT).as_posix(),
        "master_sha256": sha256(MASTER),
        "master_size": list(master.size),
        "master_alpha_bbox": list(subject_bounds),
        "texture": TARGET.relative_to(ROOT).as_posix(),
        "texture_sha256": sha256(TARGET),
        "dimensions": list(CANVAS_SIZE),
        "alpha_bbox": list(frame.getchannel("A").getbbox()),
        "format": "legacy uncompressed A8R8G8B8 (BGRA payload)",
        "frames": 1,
        "mip_levels": 1,
        "comparison_preview": (PREVIEWS / "currency_comparison.png").relative_to(ROOT).as_posix(),
    }
    (HERE / "asset_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Approved transparent image_gen PNG")
    args = parser.parse_args()
    print(json.dumps(build(args.source), indent=2))


if __name__ == "__main__":
    main()
