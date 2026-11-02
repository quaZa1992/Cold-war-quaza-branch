# IMPERIA COLD WAR — Cayo Blanco del Sur state-category validation.
from pathlib import Path
from collections import Counter
import argparse
import csv
import json
import re
import struct

import numpy as np
from PIL import Image
from scipy.ndimage import label, binary_dilation

from build import ROOT, HERE, AUDIT, BACKUP, STAGE, STATE_ID, PROVINCE_ID, SEA_ID, RGB, PIXELS, STATE_PATH, LOC_PATH, digest


def codes(array):
    a = array.astype(np.uint32)
    return (a[..., 0] << 16) | (a[..., 1] << 8) | a[..., 2]


def balance(text):
    text = re.sub(r'"(?:[^"\\]|\\.)*"', '""', text)
    text = re.sub(r"#[^\n]*", "", text)
    depth = 0
    for c in text:
        depth += (c == "{") - (c == "}")
        assert depth >= 0, "Closing brace without opening brace"
    assert depth == 0, "Unbalanced script"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged", action="store_true")
    options = parser.parse_args()
    target = STAGE if options.staged else ROOT
    report = {"feature": "IMPERIA COLD WAR — Cayo Blanco del Sur island validation", "staged": options.staged, "checks": []}

    def passed(name, **details):
        report["checks"].append({"check": name, "pass": True, **details})

    manifest = json.loads((AUDIT / "install_manifest.json").read_text())
    for rel, expected in manifest["runtime_outputs_sha256"].items():
        assert digest((target / rel).read_bytes()) == expected, f"Output drift: {rel}"
    passed("all_runtime_output_hashes")
    rows = {int(r[0]): r for r in csv.reader((target / "map/definition.csv").read_text().splitlines(), delimiter=";") if r and r[0].isdigit()}
    assert len(rows) == PROVINCE_ID + 1 and list(rows) == list(range(PROVINCE_ID + 1))
    colour_counts = Counter(tuple(map(int, r[1:4])) for r in rows.values())
    assert colour_counts[RGB] == 1 and rows[PROVINCE_ID][4:] == ["land", "true", "plains", "3"]
    passed("province_ids_contiguous_and_new_rgb_unique", rgb=RGB)
    before = np.asarray(Image.open(BACKUP / "map/provinces.bmp"))
    after = np.asarray(Image.open(target / "map/provinces.bmp"))
    assert after.shape == before.shape == (2048, 5632, 3)
    changed = np.any(before != after, axis=2)
    expected_mask = np.zeros((2048, 5632), bool)
    for x, y in PIXELS:
        expected_mask[y, x] = True
    assert np.array_equal(changed, expected_mask)
    assert np.array_equal(np.all(after == RGB, axis=2), expected_mask)
    assert label(expected_mask)[1] == 1
    neighbouring = binary_dilation(expected_mask, structure=np.ones((3, 3))) & ~expected_mask
    sea_rgb = tuple(map(int, rows[SEA_ID][1:4]))
    assert np.all(after[neighbouring] == sea_rgb), "Island touches another land province"
    assert label(np.all(before == sea_rgb, axis=2))[1] == label(np.all(after == sea_rgb, axis=2))[1]
    # No diagonal-only connections or new four-province intersections.
    for y in range(820, 826):
        for x in range(1532, 1540):
            assert len(np.unique(after[y:y+2, x:x+2].reshape(-1, 3), axis=0)) <= 3
    passed("exactly_nine_connected_pixels_and_complete_sea_gap", changed_pixels=int(changed.sum()))

    valid_codes = {(r << 16) | (g << 8) | b for r, g, b in colour_counts}
    old_unknown = set(map(int, np.unique(codes(before)))) - valid_codes
    new_unknown = set(map(int, np.unique(codes(after)))) - valid_codes
    assert new_unknown <= old_unknown
    passed("no_new_unregistered_colours", existing_unregistered_colours=len(old_unknown))

    bitmap_changes = {}
    for stem in ["provinces", "heightmap", "terrain", "rivers", "cities", "world_normal"]:
        rel = f"map/{stem}.bmp"
        old_blob, new_blob = (BACKUP / rel).read_bytes(), (target / rel).read_bytes()
        offset = struct.unpack_from("<I", old_blob, 10)[0]
        assert old_blob[:offset] == new_blob[:offset], f"BMP metadata/palette changed: {stem}"
        old, new = np.asarray(Image.open(BACKUP / rel)), np.asarray(Image.open(target / rel))
        diff = np.any(old != new, axis=2) if new.ndim == 3 else old != new
        ys, xs = np.where(diff)
        bounds = (764, 408, 771, 414) if stem == "world_normal" else (1533, 821, 1539, 825)
        assert np.all((xs >= bounds[0]) & (xs <= bounds[2]) & (ys >= bounds[1]) & (ys <= bounds[3]))
        bitmap_changes[stem] = int(diff.sum())
        if stem == "heightmap":
            assert np.all(new[expected_mask] > 95)
            assert np.all(new[neighbouring] < 95)
        if stem == "rivers":
            assert np.all(new[expected_mask] == 255)
        if stem == "cities":
            assert np.all(new[expected_mask] == 3)
        if stem == "terrain":
            assert np.all(new[expected_mask] == 0)
    passed("bitmap_headers_palettes_and_outside_pixels_preserved", pixel_changes=bitmap_changes)
    rel = "map/terrain/colormap_rgb_cityemissivemask_a.dds"
    old_blob, new_blob = (BACKUP / rel).read_bytes(), (target / rel).read_bytes()
    assert old_blob[:128] == new_blob[:128] and len(old_blob) == len(new_blob)
    old, new = np.asarray(Image.open(BACKUP / rel)), np.asarray(Image.open(target / rel))
    changed_colours = set((int(x), int(y)) for y, x in zip(*np.where(np.any(old != new, axis=2))))
    assert changed_colours == {(x // 2, y // 2) for x, y in PIXELS}
    assert all(new[y, x, 3] == 0 for x, y in changed_colours)
    for rel in ["map/trees.bmp", "map/terrain/colormap_water_0.dds"]:
        assert digest((ROOT / rel).read_bytes()) == digest((BACKUP / rel).read_bytes())
    passed("local_land_colour_without_city_lights_and_unchanged_water_trees")

    state_text = (target / STATE_PATH).read_text(encoding="utf-8")
    balance(state_text)
    assert "owner = CUB" in state_text and "controller = CUB" in state_text and "add_core_of = CUB" in state_text
    assert "manpower = 1" in state_text and "state_category = state_00" in state_text
    assert "naval_base" not in state_text and "victory_points" not in state_text and "resources" not in state_text
    category = (ROOT / "common/state_category/state_00.txt").read_text()
    assert "local_building_slots = 1" in category
    province_membership, state_ids = [], []
    paths = list((ROOT / "history/states").glob("*.txt"))
    if options.staged:
        paths = [p for p in paths if p.name != Path(STATE_PATH).name] + [target / STATE_PATH]
    for p in paths:
        text = re.sub(r"#[^\n]*", "", p.read_text(encoding="utf-8-sig"))
        match = re.search(r"\bid\s*=\s*(\d+)", text)
        if match:
            state_ids.append(int(match[1]))
        for match in re.finditer(r"\bprovinces\s*=\s*\{([^}]+)\}", text):
            if str(PROVINCE_ID) in match[1].split():
                province_membership.append(p.name)
    assert state_ids.count(STATE_ID) == 1 and len(state_ids) == len(set(state_ids))
    assert province_membership == [Path(STATE_PATH).name]
    regions = []
    for p in (ROOT / "map/strategicregions").glob("*.txt"):
        text = (target / "map/strategicregions" / p.name).read_text(encoding="utf-8-sig") if p.name == "212-Cuba.txt" else p.read_text(encoding="utf-8-sig")
        for match in re.finditer(r"\bprovinces\s*=\s*\{([^}]+)\}", re.sub(r"#[^\n]*", "", text)):
            if str(PROVINCE_ID) in match[1].split():
                regions.append(p.name)
    assert regions == ["212-Cuba.txt"]
    passed("unique_state_membership_and_land_air_region_no_free_industry")

    locator_counts = {}
    for rel, prefix, donor_prefix in [("map/unitstacks.txt", f"{PROVINCE_ID};", "16398;"), ("map/buildings.txt", f"{STATE_ID};", "1241;")]:
        text = (target / rel).read_text()
        records = [l.split(";") for l in text.splitlines() if l.startswith(prefix)]
        donor = [l.split(";") for l in (BACKUP / rel).read_text().splitlines() if l.startswith(donor_prefix)]
        assert Counter(r[1] for r in records) == Counter(r[1] for r in donor)
        for r in records:
            x, y = int(float(r[2])), int(2048 - float(r[4]))
            assert 0 <= x < 5632 and 0 <= y < 2048
            is_floating = r[1] == "floating_harbor"
            assert tuple(after[y, x]) == (sea_rgb if is_floating else RGB), f"Invalid locator: {r}"
            assert float(r[3]) == (9.5 if is_floating else 10)
            if r[1] == "naval_base_spawn":
                assert int(r[6]) == SEA_ID
            elif is_floating:
                assert int(r[6]) == PROVINCE_ID
        locator_counts[rel] = len(records)
        old = (BACKUP / rel).read_bytes().rstrip(b"\r\n")
        assert (target / rel).read_bytes().startswith(old), "Existing locator records were rewritten"
    passed("complete_native_kharg_locator_types_and_valid_land_sea_positions", counts=locator_counts)
    for rel in [STATE_PATH, "common/scripted_effects/IMP_1970_gdp_scripted_effects.txt", "map/strategicregions/212-Cuba.txt"]:
        blob = (target / rel).read_bytes()
        assert not blob.startswith(b"\xef\xbb\xbf")
        balance(blob.decode("utf-8"))
    loc = (target / LOC_PATH).read_bytes()
    assert loc.startswith(b"\xef\xbb\xbf") and loc.decode("utf-8-sig").startswith("l_english:\n")
    assert f'STATE_{STATE_ID}:0 "Cayo Blanco del Sur"' in loc.decode("utf-8-sig")
    gdp = (target / "common/scripted_effects/IMP_1970_gdp_scripted_effects.txt").read_text()
    assert f"{STATE_ID} = {{ set_variable = {{ productivity_state_var = 254.534 }} }}" in gdp
    passed("script_localisation_encodings_and_startup_productivity_profile")
    report["success"] = True
    destination = AUDIT / ("validation_stage.json" if options.staged else "validation.json")
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
    main()
