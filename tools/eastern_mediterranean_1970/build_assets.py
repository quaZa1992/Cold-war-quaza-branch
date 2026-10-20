"""Build HOI4 leader DDS files from completed, existing portrait masters.

This script performs only a restrained aspect-ratio crop and format/size
conversion. It never generates, repairs, or substitutes a portrait.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LARGE_SIZE = (156, 210)
SMALL_SIZE = (38, 51)
SAFE = re.compile(r"^[A-Za-z0-9_-]+$")


def read_records(path: Path, generated_dir: Path) -> list[dict]:
    records: list[dict] = []
    if path.is_file():
        value = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(value, list):
            records.extend({**item, "__record_dir": path.parent} for item in value)
        elif isinstance(value, dict) and isinstance(value.get("assets"), list):
            records.extend({**item, "__record_dir": path.parent} for item in value["assets"])
        else:
            raise ValueError("generation.json must contain a list of portrait records")
    if generated_dir.is_dir():
        for record_file in sorted(generated_dir.glob("*.json")):
            value = json.loads(record_file.read_text(encoding="utf-8"))
            if isinstance(value, dict) and {"country", "key", "name", "master"} <= value.keys():
                records.append({**value, "__record_dir": record_file.parent})
    # Per-portrait result JSON is the latest atomic record and takes precedence
    # over an earlier aggregate generation manifest.
    deduplicated: dict[tuple[str, str], dict] = {}
    for item in records:
        deduplicated[(str(item.get("country", "")).upper(), str(item.get("key", "")))] = item
    return list(deduplicated.values())


def resolve_master(value: str, record_dir: Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = (record_dir / path).resolve()
    return path


def make_portrait(source: Path, destination: Path, size: tuple[int, int],
                  crop_box: list[float] | None = None) -> None:
    with Image.open(source) as opened:
        im = ImageOps.exif_transpose(opened).convert("RGB")
        if crop_box is not None:
            if (len(crop_box) != 4 or any(not isinstance(v, (int, float)) for v in crop_box)
                    or any(v < 0 or v > 1 for v in crop_box)):
                raise ValueError(f"crop_box must contain four normalized values in [0,1]: {crop_box!r}")
            left, top, right, bottom = crop_box
            if left >= right or top >= bottom:
                raise ValueError(f"crop_box must have positive area: {crop_box!r}")
            width, height = im.size
            bounds = (round(left * width), round(top * height),
                      round(right * width), round(bottom * height))
            im = im.crop(bounds)
        # HOI4's narrow portrait frame needs head and upper torso. This modest
        # upward bias preserves more of the face while retaining the source
        # background; profile direction does not trigger a mirroring/edit.
        frame = ImageOps.fit(
            im, LARGE_SIZE, method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.40),
        ).convert("RGBA")
        if size == SMALL_SIZE:
            frame = frame.resize(SMALL_SIZE, Image.Resampling.LANCZOS)
        elif size != LARGE_SIZE:
            raise ValueError(f"Unsupported portrait frame size: {size}")
        frame.save(destination, format="DDS")


def dds_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.size


def build(records: list[dict], output_root: Path, generation_file: Path) -> dict:
    ready: list[dict] = []
    seen: set[tuple[str, str]] = set()
    rosters: dict[str, dict[str, dict]] = {}
    for item in records:
        required = {"country", "key", "name", "master"}
        missing = required - item.keys()
        if missing:
            raise ValueError(f"Portrait record misses {sorted(missing)}: {item!r}")
        country, key = str(item["country"]).upper(), str(item["key"])
        if not SAFE.fullmatch(country) or not SAFE.fullmatch(key):
            raise ValueError(f"Unsafe country/key: {country}/{key}")
        pair = (country, key)
        if pair in seen:
            raise ValueError(f"Duplicate portrait record: {country}/{key}")
        seen.add(pair)
        master = resolve_master(str(item["master"]), Path(item.get("__record_dir", generation_file.parent)))
        # A master that is absent or zero bytes denotes incomplete work; skip
        # it and never construct a fallback or placeholder.
        if not master.is_file() or master.stat().st_size == 0:
            print(f"SKIP incomplete master: {country}/{key} ({master})")
            continue
        roster_map = rosters.get(country)
        if roster_map is None:
            roster_path = HERE / country / "roster_research.json"
            roster_map = {}
            if roster_path.is_file():
                roster_data = json.loads(roster_path.read_text(encoding="utf-8"))
                roster_entries = roster_data if isinstance(roster_data, list) else roster_data.get("roster", [])
                for roster_item in roster_entries:
                    roster_key = str(roster_item.get("key", ""))
                    roster_map[roster_key] = roster_item
                    if roster_key.startswith(country + "_"):
                        roster_map[roster_key[len(country) + 1:]] = roster_item
            rosters[country] = roster_map
        roster_item = roster_map.get(key)
        urls = list(item.get("source_urls") or [])
        if roster_item:
            for url in roster_item.get("source_urls", []):
                if url not in urls:
                    urls.append(url)
        enriched = {**item, "country": country, "key": key, "master_path": master,
                    "source_urls": urls}
        if roster_item and roster_item.get("name"):
            enriched["name"] = roster_item["name"]
        ready.append(enriched)

    by_country: dict[str, list[dict]] = {}
    for item in ready:
        by_country.setdefault(item["country"], []).append(item)

    for country, country_items in by_country.items():
        folder = output_root / "gfx" / "leaders" / country / "1970"
        small_folder = folder / "small"
        small_folder.mkdir(parents=True, exist_ok=True)
        tool_folder = output_root / "tools" / "eastern_mediterranean_1970" / country
        tool_folder.mkdir(parents=True, exist_ok=True)
        assets: dict[str, dict] = {}
        for item in country_items:
            key, master = item["key"], item["master_path"]
            basename = f"COLDWAR_{country}_1970_{key}"
            large, small = folder / f"{basename}.dds", small_folder / f"{basename}_small.dds"
            crop_box = item.get("crop_box")
            make_portrait(master, large, LARGE_SIZE, crop_box)
            make_portrait(master, small, SMALL_SIZE, crop_box)
            if dds_size(large) != LARGE_SIZE or dds_size(small) != SMALL_SIZE:
                raise RuntimeError(f"Unexpected DDS dimensions for {country}/{key}")
            source_label = master
            try:
                source_label = master.relative_to(output_root)
            except ValueError:
                pass
            provenance = list(item["source_urls"])
            assets[f"{country}_{key}"] = {
                "name": item["name"],
                "portrait": large.relative_to(output_root).as_posix(),
                "small": small.relative_to(output_root).as_posix(),
                "status": "source_photo_ai_restoration_technical_conversion",
                "source": str(source_label).replace("\\", "/"),
                "provenance": provenance,
                "prompt": item.get("prompt", ""),
                "crop_box": item.get("crop_box"),
                "crop": "normalized source window then centered, upward-biased fit; original background retained",
                "sha256": hashlib.sha256(large.read_bytes()).hexdigest(),
            }
        (tool_folder / "assets.json").write_text(
            json.dumps({"assets": assets}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        save_contact_sheet(country_items, assets, output_root, tool_folder / "portrait_contact_sheet.png")
        print(f"{country}: built {len(country_items)} portraits")
    return {"built": len(ready), "skipped": len(records) - len(ready), "countries": sorted(by_country)}


def save_contact_sheet(items: list[dict], assets: dict, root: Path, path: Path) -> None:
    cell_w, cell_h = 205, 270
    columns = min(6, max(1, len(items)))
    rows = (len(items) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * cell_w, rows * cell_h), (32, 36, 42))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
    for index, item in enumerate(items):
        record = assets[f"{item['country']}_{item['key']}"]
        x, y = (index % columns) * cell_w, (index // columns) * cell_h
        with Image.open(root / record["portrait"]) as portrait:
            sheet.paste(portrait.convert("RGB"), (x + 24, y + 8))
        draw.text((x + cell_w // 2, y + 230), record["name"], font=font, fill="white", anchor="mm")
        draw.text((x + cell_w // 2, y + 252), item["key"], font=font, fill="#bac4d0", anchor="mm")
    sheet.save(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generation", type=Path, default=HERE / "generation.json")
    parser.add_argument("--generated-dir", type=Path, default=HERE / "generated")
    parser.add_argument("--output-root", type=Path, default=ROOT,
                        help="Mod root; override for isolated tests")
    args = parser.parse_args()
    result = build(read_records(args.generation, args.generated_dir), args.output_root.resolve(), args.generation.resolve())
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
