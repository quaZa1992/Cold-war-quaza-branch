"""Build a view-only contact sheet from approved CYP portrait DDS manifests."""
from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OLD_MANIFEST = ROOT / "tools" / "cyprus_1970" / "portraits" / "assets.json"
REGIONAL_MANIFEST = HERE / "assets.json"
OUTPUT = HERE / "portrait_contact_sheet_full.png"

# Fixed display order; any one person appears at most once even if both
# manifests eventually contain a restored/regional version.
PEOPLE = [
    ("makarios", "Makarios III"),
    ("clerides", "Glafkos Clerides"),
    ("lyssarides", "Vassos Lyssarides"),
    ("papaioannou", "Ezekias Papaioannou"),
    ("kyprianou", "Spyros Kyprianou"),
    ("grivas", "Georgios Grivas"),
    ("sampson", "Nikos Sampson"),
    ("charalambopoulos", "Charalambos Charalambopoulos"),
    ("denisis", "Georgios Denisis"),
    ("georgitsis", "Michael Georgitsis"),
]


def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def load_entries(path: Path, old: bool) -> list[dict]:
    if not path.is_file():
        print(f"MISSING manifest: {path}")
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    mapping = data.get("portraits", {}) if old else data.get("assets", {})
    entries = []
    for key, record in mapping.items():
        name = str(record.get("name", ""))
        portrait = record.get("portrait")
        if not portrait:
            print(f"SKIP {key}: no portrait path")
            continue
        entries.append({
            "key": key,
            "name": name,
            "path": (ROOT / portrait).resolve(),
            "origin": "approved legacy" if old else "regional",
        })
    return entries


def main() -> None:
    all_entries = load_entries(OLD_MANIFEST, old=True) + load_entries(REGIONAL_MANIFEST, old=False)
    selected: list[dict] = []
    claimed: set[str] = set()
    for wanted_key, wanted_name in PEOPLE:
        candidates = [entry for entry in all_entries
                      if norm(entry["key"]).endswith(norm(wanted_key))
                      or norm(entry["name"]) == norm(wanted_name)]
        # Prefer a regional replacement when available; otherwise use the
        # already approved legacy portrait. This never edits either DDS.
        candidates.sort(key=lambda item: item["origin"] != "regional")
        chosen = next((entry for entry in candidates
                       if norm(entry["name"]) not in claimed), None)
        if chosen is None:
            print(f"WAITING: {wanted_name} ({wanted_key}) has no manifest record yet")
            continue
        if not chosen["path"].is_file():
            print(f"WAITING: {wanted_name}: DDS not present at {chosen['path']}")
            continue
        chosen["display_name"] = wanted_name
        chosen["wanted_key"] = wanted_key
        selected.append(chosen)
        claimed.add(norm(chosen["name"]))

    if not selected:
        print("No available CYP portraits; no contact sheet written.")
        return

    cell_w, cell_h, portrait_w, portrait_h = 210, 280, 156, 210
    columns = min(5, len(selected))
    rows = (len(selected) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * cell_w, rows * cell_h), (32, 36, 42))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
        small_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11)
    except OSError:
        font = small_font = ImageFont.load_default()

    for index, entry in enumerate(selected):
        x, y = (index % columns) * cell_w, (index // columns) * cell_h
        with Image.open(entry["path"]) as opened:
            portrait = opened.convert("RGBA")
            if portrait.size != (portrait_w, portrait_h):
                print(f"NOTE: {entry['path'].name} is {portrait.size}, displayed at source size")
            tile = Image.new("RGBA", portrait.size, (72, 76, 82, 255))
            tile.alpha_composite(portrait)
            sheet.paste(tile.convert("RGB"), (x + (cell_w - portrait.width) // 2, y + 8))
        draw.text((x + cell_w // 2, y + 232), entry["display_name"],
                  font=font, fill="white", anchor="mm")
        draw.text((x + cell_w // 2, y + 254), "Restored historical photo",
                  font=small_font, fill="#bac4d0", anchor="mm")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUTPUT)
    print(f"WROTE {OUTPUT} ({len(selected)}/{len(PEOPLE)} unique portraits)")


if __name__ == "__main__":
    main()
