# IMPERIA CW — Cold War: warsaw landmarks — city style.
"""Apply and validate a strictly local 1970 Warsaw decorative-building style.

Uses existing masonry city meshes, removes hand-placed modern Warsaw towers,
and preserves the original indexed BMP header/palette and every non-Warsaw
pixel. The palace plaza uses an unassigned style, as the Berlin wall does.
No province, terrain, history, Berlin asset, or landmark mesh is written.
"""
from pathlib import Path
import hashlib
import json
import math
import re
import struct
import sys

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'tools/berlin_landmarks'))
from pdx import read, meshes

PROVINCE_ID = 3544
CITY_INDEX = 4
EMPTY_INDEX = 3
PLAZA = [3129.9, 3133.1, 1561.6, 1565.4]  # xmin, xmax, zmin, zmax
PIXEL_RADIUS = math.sqrt(.5)
EXTRA_MARGIN = .08
# Entity scale multiplied by the scale of the referenced pdxmesh definition.
STYLES = {
    'mdcw_warsaw_low_houses': ('Western/western_buildings_4_01.mesh', 1.30),
    'mdcw_warsaw_oldtown': ('french_city_4_02.mesh', .85*.36),
    'mdcw_warsaw_perimeter': ('city_4_03.mesh', 1.35),
    'mdcw_warsaw_apartments': ('city_4_04.mesh', 1.35),
}
START = '# IMPERIA CW — Cold War: warsaw landmarks generated content.\n# MDCW Warsaw 1970 local city style'
CITY_GROUP = '# IMPERIA CW — Cold War: warsaw landmarks generated content.\n# MDCW Warsaw 1970 local city style\n# Palette index 4 is used only in province 3544; index 3 clears the palace plaza.\ncity_group = {\n    color_index = 4\n    density = 0.9\n    building = {\n        distance = 1\n        mesh = {\n            "mdcw_warsaw_low_houses"\n            "mdcw_warsaw_oldtown"\n            "mdcw_warsaw_perimeter"\n        }\n    }\n    building = {\n        distance = 2\n        mesh = {\n            "mdcw_warsaw_oldtown"\n            "mdcw_warsaw_perimeter"\n            "mdcw_warsaw_apartments"\n        }\n    }\n    building = {\n        distance = 3\n        mesh = {\n            "mdcw_warsaw_perimeter"\n            "mdcw_warsaw_apartments"\n        }\n    }\n    building = {\n        distance = 4\n        mesh = {\n            "mdcw_warsaw_perimeter"\n            "mdcw_warsaw_apartments"\n        }\n    }\n}\n'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blocks(text, expression, start=0, end=None):
    """Find balanced sibling blocks, retaining source byte ranges."""
    limit = len(text) if end is None else end
    at = start
    while found := re.search(expression, text[at:limit], re.M):
        begin = at+found.start()
        cursor = at+found.end()
        depth = 1
        while depth:
            if text[cursor] == '{':
                depth += 1
            elif text[cursor] == '}':
                depth -= 1
            cursor += 1
            assert cursor <= limit
        yield begin, cursor, text[begin:cursor]
        at = cursor


def ambient_objects(text):
    result = []
    for _, _, group in blocks(text, r'^type\s*=\s*\{'):
        kind = re.search(r'type\s*=\s*"([^"]+)"', group).group(1)
        group_at = text.index(group)
        for begin, end, source in blocks(group, r'^\tobject\s*=\s*\{'):
            pos = re.search(r'position\s*=\s*\{\s*([\d.-]+)\s+([\d.-]+)\s+([\d.-]+)', source)
            if pos:
                result.append((kind, tuple(map(float, pos.groups())), group_at+begin, group_at+end, source))
    return result


def main():
    report_path = HERE/'city_style_report.json'
    prior = json.loads(report_path.read_text()) if report_path.exists() else {}
    bmp_path = ROOT/'map/cities.bmp'
    original = bmp_path.read_bytes()
    offset = struct.unpack_from('<I', original, 10)[0]
    width, height = struct.unpack_from('<ii', original, 18)
    assert original[:2] == b'BM' and width > 0 and height > 0
    assert struct.unpack_from('<HI', original, 28) == (8, 0)
    stride = (width+3)//4*4
    pixels = np.ndarray((height, width), dtype=np.uint8, buffer=original,
                        offset=offset, strides=(stride, 1))[::-1]
    provinces = np.asarray(Image.open(ROOT/'map/provinces.bmp'))
    line = next(line for line in (ROOT/'map/definition.csv').read_text().splitlines()
                if line.startswith(f'{PROVINCE_ID};'))
    rgb = list(map(int, line.split(';')[1:4]))
    warsaw = np.all(provinces == rgb, axis=2)
    assert warsaw.sum() == 104
    yy, xx = np.where(warsaw)
    zz = height-yy
    assert set(np.unique(pixels[warsaw])) <= {15, CITY_INDEX, EMPTY_INDEX}
    assert not np.any((pixels == CITY_INDEX) & ~warsaw), 'Index 4 already used elsewhere'

    bounds = {}
    for name, (filename, scale) in STYLES.items():
        vertices = np.concatenate([shape.prop('p').value.reshape(-1, 3)
                                   for _, shape in meshes(read(ROOT/'gfx/models/buildings'/filename))])*scale
        radius = float(np.linalg.norm(vertices[:, [0, 2]], axis=1).max())
        bounds[name] = {'mesh': filename, 'combined_scale': scale,
                       'min': vertices.min(axis=0).tolist(), 'max': vertices.max(axis=0).tolist(),
                       'horizontal_radius': radius}
        assert vertices[:, 1].max() <= .60 and radius <= .95
    radius = max(value['horizontal_radius'] for value in bounds.values())
    buffer = radius+PIXEL_RADIUS+EXTRA_MARGIN
    x0, x1, z0, z1 = PLAZA
    clear = ((xx >= x0-buffer) & (xx <= x1+buffer) &
             (zz >= z0-buffer) & (zz <= z1+buffer))
    desired = np.full(len(xx), CITY_INDEX, dtype=np.uint8)
    desired[clear] = EMPTY_INDEX
    assert int(clear.sum()) == 45 and len(desired)-int(clear.sum()) == 59
    patched = bytearray(original)
    for x, y, value in zip(xx, yy, desired):
        patched[offset+(height-1-int(y))*stride+int(x)] = int(value)
    result = bytes(patched)
    updated = np.ndarray((height, width), dtype=np.uint8, buffer=result,
                         offset=offset, strides=(stride, 1))[::-1]
    assert original[:offset] == result[:offset], 'BMP header/palette changed'
    assert np.array_equal(updated[~warsaw], pixels[~warsaw]), 'Changed pixels outside Warsaw'
    assert np.array_equal(updated[warsaw], desired), 'Wrong Warsaw style bytes'

    cities_path = ROOT/'map/cities.txt'
    city_original = cities_path.read_bytes()
    city_text = city_original.decode('utf-8-sig')
    base_city_text = city_text[:city_text.index(START)] if START in city_text else city_text
    assert CITY_INDEX not in {int(n) for n in re.findall(r'color_index\s*=\s*(\d+)', base_city_text)}
    assert EMPTY_INDEX not in {int(n) for n in re.findall(r'color_index\s*=\s*(\d+)', base_city_text)}
    ambient_path = ROOT/'map/ambient_object.txt'
    ambient_original = ambient_path.read_bytes()
    ambient_text = ambient_original.decode('utf-8')
    before = ambient_objects(ambient_text)
    removed = []
    edits = []
    move = None
    for kind, (x, y, z), begin, end, source in before:
        px, py = math.floor(x), height-math.floor(z)
        inside = 0 <= px < width and 0 <= py < height and warsaw[py, px]
        if kind.startswith('skyscraper') and inside:
            removed.append({'type': kind, 'position': [x, y, z], 'source': source})
            # Also remove the trailing newline, retaining all other bytes exactly.
            if ambient_text[end:end+2] == '\r\n':
                end += 2
            elif ambient_text[end:end+1] == '\n':
                end += 1
            edits.append((begin, end, ''))
        if kind == 'cityblock_entity' and abs(x-3133.11) < .001 and abs(z-1562.62) < .001:
            moved = re.sub(r'(position\s*=\s*\{\s*)([\d.-]+)(\s+)([\d.-]+)(\s+)([\d.-]+)',
                           lambda m: m[1]+'3135.000'+m[3]+m[4]+m[5]+'1563.800', source, count=1)
            edits.append((begin, end, moved))
            move = {'type': kind, 'old_position': [x, y, z], 'new_position': [3135., y, 1563.8]}
    assert len(removed) == 11 or (not removed and len(prior.get('removed_modern_instances', [])) == 11)
    assert move or prior.get('moved_historic_block')
    for begin, end, replacement in sorted(edits, reverse=True):
        ambient_text = ambient_text[:begin]+replacement+ambient_text[end:]
    after = ambient_objects(ambient_text)
    historic_count = 0
    for kind, (x, y, z), _, _, _ in after:
        px, py = math.floor(x), height-math.floor(z)
        inside = 0 <= px < width and 0 <= py < height and warsaw[py, px]
        assert not (kind.startswith('skyscraper') and inside), (kind, x, z)
        historic_count += int(inside and kind in {'cityblock_entity', 'cityblock2_entity'})
    assert historic_count == 4
    # Every object other than the 11 towers and the single moved perimeter block
    # must remain byte-for-byte identical, including all Berlin ambient objects.
    affected_sources = {item['source'] for item in removed}
    if move:
        affected_sources |= {item[4] for item in before if item[0] == move['type'] and
                             item[1] == tuple(move['old_position'])}
    unaffected = [(kind, pos, source) for kind, pos, _, _, source in before if source not in affected_sources]
    after_sources = {(kind, pos, source) for kind, pos, _, _, source in after}
    assert all(item in after_sources for item in unaffected), 'Unrelated ambient object changed'

    # Validate everything before making the three strictly scoped mutations.
    if result != original:
        bmp_path.write_bytes(result)
    # Normalize only our appended block; retain the original city groups verbatim.
    if START.encode() not in city_original:
        city_bytes = city_original.rstrip(b'\r\n')+b'\r\n\r\n'+CITY_GROUP.replace('\n', '\r\n').encode()
    else:
        at = city_original.index(START.encode())
        city_bytes = city_original[:at]+CITY_GROUP.replace('\n', '\r\n').encode()
    if city_bytes != city_original:
        cities_path.write_bytes(city_bytes)
    ambient_result = ambient_text.encode('utf-8')
    if ambient_result != ambient_original:
        ambient_path.write_bytes(ambient_result)
    report = {
        'province_id': PROVINCE_ID, 'state_id': 114,
        'province_bounds_image': [int(xx.min()), int(yy.min()), int(xx.max()), int(yy.max())],
        'province_rgb': rgb, 'city_style_index': CITY_INDEX, 'empty_style_index': EMPTY_INDEX,
        'urban_pixels': len(desired), 'house_pixels': int((desired == CITY_INDEX).sum()),
        'palace_clearance_pixels': int(clear.sum()), 'palace_world_rectangle': PLAZA,
        'maximum_house_radius': radius, 'clearance_radius_including_pixel_and_margin': buffer,
        'chosen_meshes': bounds,
        'removed_modern_instances': removed or prior['removed_modern_instances'],
        'moved_historic_block': move or prior['moved_historic_block'],
        'untouched_ambient_object_count': len(unaffected),
        'cities_bmp_before_sha256': prior.get('cities_bmp_before_sha256', sha(original)),
        'cities_bmp_after_sha256': sha(result),
        'bmp_header_palette_sha256': sha(result[:offset]),
        'ambient_before_sha256': prior.get('ambient_before_sha256', sha(ambient_original)),
        'ambient_after_sha256': sha(ambient_result),
        'warsaw_pixel_edits': [{'x': int(x), 'y': int(y), 'world_z': int(height-y),
                               'old_index': 15, 'new_index': int(value)}
                              for x, y, value in zip(xx, yy, desired)],
        'checks': {'original_bmp_header_and_palette_preserved': True,
                   'all_pixels_outside_province_3544_preserved': True,
                   'berlin_house_mask_preserved': True,
                   'unrelated_ambient_objects_byte_identical': True,
                   'warsaw_ambient_modern_skyscrapers_remaining': 0,
                   'historic_ambient_blocks_retained': historic_count,
                   'tallest_new_decorative_house_below_point_60': True},
    }
    report_path.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: report[key] for key in ['urban_pixels', 'house_pixels',
          'palace_clearance_pixels', 'maximum_house_radius', 'checks']}, indent=2))


if __name__ == '__main__':
    main()
