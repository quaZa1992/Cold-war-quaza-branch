# IMPERIA COLD WAR — Repair and validate the native agency repetition sprite declaration.
"""Run after a Millennium Dawn interface sync: --repair is idempotent; default checks only."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[2]
GFX = ROOT / "interface/countryintelligenceagencyview.gfx"
GUI = ROOT / "interface/countryintelligenceagencyview.gui"
PROJECT = "IMPERIA COLD WAR"
SPRITE = "GFX_agency_upgrade_repetition_icon"
TEXTURE = "gfx/interface/cont_focus_check_icon_small.dds"
FILE_MARK = "# IMPERIA COLD WAR — Agency repetition icon frame-count integration only."
LINE_MARK = "# IMPERIA COLD WAR — match the native three-state atlas."


def blocks(text: str, tag: str):
    for match in re.finditer(rf"\b{re.escape(tag)}\s*=\s*\{{", text):
        start = match.start()
        opening = text.find("{", start)
        depth = 0
        quoted = escaped = False
        for index in range(opening, len(text)):
            char = text[index]
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quoted = False
            elif char == '"':
                quoted = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    yield start, index + 1, text[start:index + 1]
                    break
        else:
            raise ValueError(f"Unclosed {tag} block")


def named_block(text: str, tag: str, name: str):
    for start, end, block in blocks(text, tag):
        found = re.search(r'^\s*name\s*=\s*"([^\"]+)"', block, re.M)
        if found and found.group(1) == name:
            return start, end, block
    raise ValueError(f"Expected one {tag} named {name}")


def preflight_gui() -> dict:
    text = GUI.read_text(encoding="utf-8")
    needle = f'spriteType = "{SPRITE}"'
    references = [(path, line_number) for path in (ROOT / "interface").rglob("*.gui")
                  for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1)
                  if needle in line]
    if len(references) != 1 or references[0][0] != GUI:
        raise ValueError(f"Expected one project GUI reference to {SPRITE}, found {[(str(p), n) for p, n in references]}")
    _, _, icon = named_block(text, "containerWindowType", "agency_upgrade_repetition_icon")
    if not re.search(r"size\s*=\s*\{\s*width\s*=\s*11\s+height\s*=\s*21\s*\}", icon):
        raise ValueError("Native 11x21 repetition icon container changed")
    if not re.search(r"scale\s*=\s*0\.7\b", icon) or not re.search(r"frame\s*=\s*1\b", icon):
        raise ValueError("Native repetition icon scale/frame changed")
    _, _, entry = named_block(text, "containerWindowType", "upgrade_entry")
    if not re.search(r"size\s*=\s*\{\s*width\s*=\s*200\s+height\s*=\s*115\s*\}", entry):
        raise ValueError("Native 200x115 upgrade card geometry changed")
    if not re.search(r"name\s*=\s*\"repetitions_icons\"", entry):
        raise ValueError("Upgrade card no longer contains repetitions_icons")
    if re.search(r"name\s*=\s*\"progressbar_content\"", entry):
        raise ValueError("Upgrade entry unexpectedly contains a progress bar")
    return {"gui_references": len(references), "reference": f"{GUI.relative_to(ROOT)}:{references[0][1]}",
            "icon_container_px": [11, 21], "icon_scale": 0.7,
            "icon_frame": 1, "upgrade_card_px": [200, 115], "card_progressbar": False}


def check_texture(game_root: Path) -> dict:
    override = ROOT / TEXTURE
    path = override if override.exists() else game_root / TEXTURE
    if not path.exists():
        raise ValueError(f"Cannot verify the atlas; provide the installed game root (checked {path})")
    raw = path.read_bytes()
    if raw[:4] != b"DDS ":
        raise ValueError(f"Texture override is not a DDS file: {path}")
    height, width = struct.unpack_from("<II", raw, 12)
    if (width, height) != (96, 32) or width % 3:
        raise ValueError(f"Expected a 96x32 three-frame atlas, got {width}x{height}")
    return {"project_override": override.exists(), "source": str(path), "dimensions_px": [width, height],
            "frame_count": 3, "frame_size_px": [width // 3, height]}


def repair_or_check(repair: bool, game_root: Path) -> dict:
    gui_report = preflight_gui()
    texture_report = check_texture(game_root)
    raw = GFX.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("GFX must remain UTF-8 without BOM")
    text = raw.decode("utf-8")
    start, end, block = named_block(text, "spriteType", SPRITE)
    if text.count(f'name = "{SPRITE}"') != 1:
        raise ValueError(f"Expected one declaration of {SPRITE}")
    texture_match = re.search(r'^\s*texturefile\s*=\s*"([^"]+)"', block, re.M | re.I)
    if not texture_match or texture_match.group(1) != TEXTURE:
        raise ValueError(f"Unexpected {SPRITE} texture path")
    frames = list(re.finditer(r"(?m)^(?P<indent>[ \t]*)noOfFrames[ \t]*=[ \t]*(?P<count>\d+)(?P<tail>[ \t]*(?:#[^\r\n]*)?)(?P<newline>\r?\n|$)", block))
    if len(frames) != 1:
        raise ValueError(f"Expected one noOfFrames in {SPRITE}, found {len(frames)}")
    value = int(frames[0].group("count"))
    if value not in (2, 3):
        raise ValueError(f"Refusing to overwrite unexpected noOfFrames={value}")
    if not repair and value != 3:
        raise ValueError(f"Incorrect noOfFrames={value}; run with --repair after the MD sync")
    if not repair and (not text.startswith(FILE_MARK) or LINE_MARK not in block):
        raise ValueError("The project integration markers are missing; run with --repair")
    changed = False
    if repair:
        if value == 2:
            line = frames[0]
            ending = line.group("newline")
            replacement = f'{line.group("indent")}noOfFrames = 3'
            if line.group("tail").strip():
                replacement += " " + line.group("tail").strip() + ending
                replacement += f'{line.group("indent")}{LINE_MARK}{ending}'
            else:
                replacement += f' {LINE_MARK}{ending}'
            block = block[:line.start()] + replacement + block[line.end():]
            text = text[:start] + block + text[end:]
            changed = True
        elif LINE_MARK not in block:
            line = frames[0]
            ending = line.group("newline")
            replacement = f'{line.group("indent")}noOfFrames = 3'
            if line.group("tail").strip():
                replacement += " " + line.group("tail").strip() + ending
                replacement += f'{line.group("indent")}{LINE_MARK}{ending}'
            else:
                replacement += f' {LINE_MARK}{ending}'
            block = block[:line.start()] + replacement + block[line.end():]
            text = text[:start] + block + text[end:]
            changed = True
        if not text.startswith(FILE_MARK):
            ending = "\r\n" if "\r\n" in text else "\n"
            text = FILE_MARK + ending + text
            changed = True
        if changed:
            temp = GFX.with_name(GFX.name + ".tmp")
            temp.write_bytes(text.encode("utf-8"))
            temp.replace(GFX)
    verified = repair_or_check(False, game_root) if repair else None
    return {"path": str(GFX.relative_to(ROOT)), "frames_before": value,
            "frames_after": 3 if repair else value, "changed": changed,
            "sha256": hashlib.sha256(GFX.read_bytes()).hexdigest(),
            "gui": gui_report, "texture": texture_report,
            "verified_after_repair": verified is not None}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repair", action="store_true", help="repair 2 to 3 frames and add scoped project markers")
    parser.add_argument("--check", action="store_true", help="validate only; this is the default")
    parser.add_argument("--game-root", type=Path,
                        default=Path(os.environ.get("HOI4_GAME_ROOT", "E:/SteamLibrary/steamapps/common/Hearts of Iron IV")),
                        help="installed game root, used only to verify the native DDS dimensions")
    args = parser.parse_args()
    if args.repair and args.check:
        parser.error("choose either --repair or --check")
    result = repair_or_check(args.repair, args.game_root)
    print(json.dumps({"project": PROJECT, "status": "PASS", **result}, indent=2))


if __name__ == "__main__":
    main()
