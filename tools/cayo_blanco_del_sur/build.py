# IMPERIA COLD WAR — reproducible Cayo Blanco del Sur map installation.
"""Stage from the verified pre-install backup; --apply installs guarded outputs."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import shutil
import struct

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = ROOT / "docs/design/cuba_1970_island"
BACKUP = ROOT / "rollback_backups/cayo_blanco_del_sur_20261023_before_install"
STAGE = HERE / "runtime/stage"
DONOR = Path("E:/SteamLibrary/steamapps/workshop/content/394360/2777392649")
STATE_ID, PROVINCE_ID, SEA_ID = 1252, 16537, 5735
RGB = (214, 173, 62)
HEIGHT = 100
# Nine orthogonally connected pixels: the native Kharg province also has nine.
# A complete sea row (y=821) separates this footprint from the existing coast.
PIXELS = [(1535, 822), (1536, 822),
          (1534, 823), (1535, 823), (1536, 823), (1537, 823),
          (1536, 824), (1537, 824), (1538, 824)]
MARK = "# IMPERIA COLD WAR — Cayo Blanco del Sur island state."
STATE_PATH = "history/states/1252-Cayo Blanco del Sur.txt"
LOC_PATH = "localisation/english/mdcw_cayo_blanco_del_sur_l_english.yml"


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def original(rel):
    return (BACKUP / rel).read_bytes()


def text_original(rel):
    return original(rel).decode("utf-8-sig")


def stage(rel, blob):
    path = STAGE / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(blob)


def text_bytes(text, bom=False):
    return text.encode("utf-8-sig" if bom else "utf-8")


def bmp_patch(blob, changes):
    """Patch pixel bytes only; preserve every header, palette and padding byte."""
    assert blob[:2] == b"BM"
    offset = struct.unpack_from("<I", blob, 10)[0]
    width, signed_height = struct.unpack_from("<ii", blob, 18)
    bpp = struct.unpack_from("<H", blob, 28)[0]
    assert bpp in (8, 24) and struct.unpack_from("<I", blob, 30)[0] == 0
    height = abs(signed_height)
    stride = ((width * bpp + 31) // 32) * 4
    result = bytearray(blob)
    for (x, y), value in changes.items():
        assert 0 <= x < width and 0 <= y < height
        row = height - 1 - y if signed_height > 0 else y
        pos = offset + row * stride + x * (bpp // 8)
        if bpp == 8:
            result[pos] = int(value)
        else:
            result[pos:pos + 3] = bytes(reversed(tuple(map(int, value))))
    return bytes(result)


def dds_patch(blob, changes):
    """Native MD colormap is uncompressed BGRA8, one level, fixed DDS header."""
    assert blob[:4] == b"DDS "
    height, width = struct.unpack_from("<II", blob, 12)
    assert struct.unpack_from("<I", blob, 28)[0] in (0, 1)
    assert struct.unpack_from("<I", blob, 88)[0] == 32
    assert struct.unpack_from("<IIII", blob, 92) == (0xff0000, 0xff00, 0xff, 0xff000000)
    assert len(blob) == 128 + width * height * 4
    result = bytearray(blob)
    for (x, y), rgba in changes.items():
        assert 0 <= x < width and 0 <= y < height
        r, g, b, alpha = map(int, rgba)
        pos = 128 + (y * width + x) * 4
        result[pos:pos + 4] = bytes((b, g, r, alpha))
    return bytes(result)


def append_records(rel, records):
    blob = original(rel)
    newline = b"\r\n" if b"\r\n" in blob else b"\n"
    return blob.rstrip(b"\r\n") + newline + newline.join(r.encode("ascii") for r in records) + newline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    options = parser.parse_args()
    manifest = json.loads((BACKUP / "manifest.json").read_text(encoding="utf-8"))
    for rel, entry in manifest["files"].items():
        assert digest(original(rel)) == entry["sha256"], f"Damaged backup: {rel}"
    HERE.joinpath("runtime").mkdir(exist_ok=True)
    HERE.joinpath("runtime/.gitignore").write_text("*\n", encoding="utf-8")
    AUDIT.mkdir(parents=True, exist_ok=True)

    rows = list(csv.reader(text_original("map/definition.csv").splitlines(), delimiter=";"))
    definitions = {int(r[0]): r for r in rows if r and r[0].isdigit()}
    assert max(definitions) + 1 == PROVINCE_ID
    assert RGB not in {tuple(map(int, r[1:4])) for r in definitions.values()}
    sea_rgb = tuple(map(int, definitions[SEA_ID][1:4]))
    province = np.asarray(Image.open(BACKUP / "map/provinces.bmp"))
    assert all(tuple(province[y, x]) == sea_rgb for x, y in PIXELS)
    stage("map/provinces.bmp", bmp_patch(original("map/provinces.bmp"), {p: RGB for p in PIXELS}))
    stage("map/definition.csv", append_records("map/definition.csv", [f"{PROVINCE_ID};{RGB[0]};{RGB[1]};{RGB[2]};land;true;plains;3"]))

    # A low shore, above WATER_HEIGHT=9.5, with a submerged one-pixel apron.
    heights = np.asarray(Image.open(BACKUP / "map/heightmap.bmp"))
    height_changes = {p: HEIGHT for p in PIXELS}
    footprint = set(PIXELS)
    for x, y in PIXELS:
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                p = (x + dx, y + dy)
                if p not in footprint and tuple(province[p[1], p[0]]) == sea_rgb:
                    height_changes[p] = max(int(heights[p[1], p[0]]), 92)
    stage("map/heightmap.bmp", bmp_patch(original("map/heightmap.bmp"), height_changes))
    stage("map/terrain.bmp", bmp_patch(original("map/terrain.bmp"), {p: 0 for p in PIXELS}))
    stage("map/rivers.bmp", bmp_patch(original("map/rivers.bmp"), {p: 255 for p in PIXELS}))
    # Native MD's unassigned city index 3, already used for Berlin clearance,
    # suppresses decorative house generation. This does not add a city.
    stage("map/cities.bmp", bmp_patch(original("map/cities.bmp"), {p: 3 for p in PIXELS}))

    # Add the island's slope contribution to the existing native normal field.
    # The original field and all pixels outside this local 8x7 window survive.
    delta = np.zeros_like(heights, dtype=np.float64)
    for (x, y), value in height_changes.items():
        delta[y, x] = value - int(heights[y, x])
    small = delta.reshape(1024, 2, 2816, 2).mean(axis=(1, 3))
    small = gaussian_filter(small, sigma=0.65, truncate=2)
    gy, gx = np.gradient(small)
    normals = np.asarray(Image.open(BACKUP / "map/world_normal.bmp"))
    normal_changes = {}
    for y, x in zip(*np.where((np.abs(gx) + np.abs(gy)) > 0.00001)):
        v = normals[y, x].astype(float) / 127.5 - 1
        v[0] -= gx[y, x] * 0.10
        v[1] += gy[y, x] * 0.10
        v /= np.linalg.norm(v)
        value = tuple(np.clip(np.rint((v + 1) * 127.5), 0, 255).astype(int))
        if value != tuple(normals[y, x]):
            normal_changes[(int(x), int(y))] = value
    stage("map/world_normal.bmp", bmp_patch(original("map/world_normal.bmp"), normal_changes))

    # Paint only the four half-resolution texels intersecting the new island.
    # Sample existing Cuban land colour, preserving alpha=0 (no night lights).
    rel = "map/terrain/colormap_rgb_cityemissivemask_a.dds"
    colormap = np.asarray(Image.open(BACKUP / rel))
    land_colour = (*map(int, colormap[407, 768, :3]), 0)
    colour_pixels = {(x // 2, y // 2): land_colour for x, y in PIXELS}
    stage(rel, dds_patch(original(rel), colour_pixels))

    rel = "map/strategicregions/212-Cuba.txt"
    text = text_original(rel)
    old = "14488 14489 14490"
    assert text.count(old) == 1
    text = text.replace(old, old + f"\n\t\t{MARK}\n\t\t{PROVINCE_ID}")
    stage(rel, text_bytes(text))

    donor_units = [l.split(";") for l in text_original("map/unitstacks.txt").splitlines() if l.startswith("16398;")]
    assert sorted(int(r[1]) for r in donor_units) == [0, 1, 2, 9, 10, 21, 22, 23, 38]
    anchors = [(1535.5, 822.5), (1536.5, 823.5), (1536.5, 824.5)]
    records = []
    for n, r in enumerate(donor_units):
        x, bitmap_y = anchors[n % len(anchors)]
        records.append(f"{PROVINCE_ID};{r[1]};{x:.2f};10.00;{2048 - bitmap_y:.2f};{r[5]};{r[6]}")
    stage("map/unitstacks.txt", append_records("map/unitstacks.txt", records))

    donor_buildings = [l.split(";") for l in text_original("map/buildings.txt").splitlines() if l.startswith("1241;")]
    assert len(donor_buildings) == 32
    records = []
    for n, r in enumerate(donor_buildings):
        x, bitmap_y = anchors[n % len(anchors)]
        rotation, extra = r[5], "0"
        if r[1] == "naval_base_spawn":
            x, bitmap_y, rotation, extra = 1537.5, 824.5, "-1.57", str(SEA_ID)
        elif r[1] == "floating_harbor":
            x, bitmap_y, rotation, extra = 1538.5, 825.5, "-1.57", str(PROVINCE_ID)
        elif r[1] in ("dockyard", "coastal_bunker", "naval_supply_hub"):
            x, bitmap_y, rotation = 1537.5, 824.5, "-1.57"
        records.append(f"{STATE_ID};{r[1]};{x:.2f};{'9.50' if r[1] == 'floating_harbor' else '10.00'};{2048 - bitmap_y:.2f};{rotation};{extra}")
    stage("map/buildings.txt", append_records("map/buildings.txt", records))

    state = f'''{MARK}
# Native MD micro-island population floor; one tiny-state investment slot, no starting buildings.
state = {{
\tid = {STATE_ID}
\tname = "STATE_{STATE_ID}"
\tmanpower = 1
\tstate_category = state_00
\tbuildings_max_level_factor = 1.000
\thistory = {{
\t\towner = CUB
\t\tcontroller = CUB
\t\tadd_core_of = CUB
\t\tset_state_flag = COLDWAR_CUB_cayo_blanco_del_sur
\t\tset_variable = {{ state_renewable_capacity_factor_modifier_var = 1.185 }}
\t\tset_variable = {{ productivity_state_var = 254.534 }}
\t\tbuildings = {{ infrastructure = 0 }}
\t}}
\tprovinces = {{ {PROVINCE_ID} }}
}}
'''
    stage(STATE_PATH, text_bytes(state))
    loc = f'''l_english:
 {MARK}
 STATE_{STATE_ID}:0 "Cayo Blanco del Sur"
 VICTORY_POINTS_{PROVINCE_ID}:0 "Cayo Blanco del Sur"
 COLDWAR_CUB_ernst_thaelmann_island_name:0 "Ernst Thälmann Island"
'''
    stage(LOC_PATH, text_bytes(loc, bom=True))

    rel = "common/scripted_effects/IMP_1970_gdp_scripted_effects.txt"
    text = text_original(rel)
    old = "\t\t1251 = { set_variable = { productivity_state_var = 734 } }"
    assert text.count(old) == 1
    text = text.replace(old, old + f"\n\t\t{MARK}\n\t\t{STATE_ID} = {{ set_variable = {{ productivity_state_var = 254.534 }} }}")
    stage(rel, text_bytes(text))

    outputs = {p.relative_to(STAGE).as_posix(): digest(p.read_bytes()) for p in STAGE.rglob("*") if p.is_file()}
    new_paths = [STATE_PATH, LOC_PATH]
    manifest["new_runtime_paths"] = new_paths
    manifest["installed_outputs_sha256"] = outputs
    (BACKUP / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    # Full donor blocks are recorded, including every ancillary spawn locator.
    donor_state = next((DONOR / "history/states").glob("1241-*"))
    native = {
        "feature": "IMPERIA COLD WAR — native MD Kharg reference",
        "source": str(DONOR), "state_file": donor_state.name,
        "state_text": donor_state.read_text(encoding="utf-8-sig"),
        "definition": definitions[16398],
        "unitstacks": donor_units, "building_locators": donor_buildings,
        "note": "All 9 unit entries and all 32 building entries reviewed; locator rows do not grant built facilities. Water colormap and tree layer need no island-specific edit.",
    }
    (AUDIT / "kharg_reference.json").write_text(json.dumps(native, indent=2) + "\n", encoding="utf-8")
    plan = {
        "feature": "IMPERIA COLD WAR — Cayo Blanco del Sur installation",
        "state_id": STATE_ID, "province_id": PROVINCE_ID, "rgb": RGB,
        "pixels_top_left_origin": PIXELS, "height_changes": len(height_changes),
        "normal_changes": len(normal_changes), "colour_changes": len(colour_pixels),
        "land_colour_rgba": land_colour, "backup": str(BACKUP),
        "runtime_outputs_sha256": outputs, "applied": options.apply,
    }
    if options.apply:
        # Check every target before writing any target. Preserve concurrent work.
        for rel, expected in outputs.items():
            current = ROOT / rel
            if rel in new_paths:
                assert not current.exists() or digest(current.read_bytes()) == expected, f"New file collision: {rel}"
            else:
                assert digest(current.read_bytes()) in (manifest["files"][rel]["sha256"], expected), f"File changed since backup: {rel}"
        for rel in outputs:
            target = ROOT / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(STAGE / rel, target)
    (AUDIT / "install_manifest.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in plan.items() if k != "runtime_outputs_sha256"}, indent=2), flush=True)


if __name__ == "__main__":
    main()
