# IMPERIA CW — Cold War: jerusalem landmarks — clear city corridor.
"""Clear only decorative house cells that can overlap the Western Wall site.

Patch original indexed BMP bytes and preserve the V4 header and palette. The
conservative buffer includes the largest native Western house, arbitrary house
rotation, and jitter within its map pixel. Adjacent urban province cells are
included when their houses could reach the forecourt; no terrain is repainted.
"""
from pathlib import Path
import hashlib
import json
import math
import re
import struct

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CITY_MAP = ROOT/'map/cities.bmp'
EMPTY_INDEX = 3
SOURCE_INDEX = 15
HOUSE_RADIUS = 1.309592
PIXEL_RADIUS = math.sqrt(.5)
EXTRA_MARGIN = .08
ENVELOPE = [-40., 8., -28.5, 28.5]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def protected_assets():
    paths = []
    for city in ('berlin', 'warsaw', 'bucharest'):
        paths += list((ROOT/'gfx/models/buildings/landmarks').glob(f'landmark_{city}_*.mesh'))
        paths += list((ROOT/'gfx/models/buildings/landmarks').glob(f'mdcw_{city}_*.dds'))
        paths += list((ROOT/'gfx/entities').glob(f'mdcw_{city}*'))
        paths += list((ROOT/f'tools/{city}_landmarks/source').glob('*.blend'))
    paths += list((ROOT/'gfx/models/buildings/landmarks').glob('domeofrock*'))
    paths += [ROOT/name for name in (
        'map/provinces.bmp', 'map/terrain.bmp', 'map/heightmap.bmp',
        'map/ambient_object.txt', 'map/cities.txt', 'gfx/entities/landmarks.asset',
        'gfx/entities/landmarks.gfx')]
    return {str(path.relative_to(ROOT)): sha(path.read_bytes()) for path in sorted(set(paths))}


def previous_city_cells():
    """Snapshot approved Berlin, Warsaw and Bucharest city-mask ownership."""
    result = []
    with Image.open(CITY_MAP) as image:
        pixels = np.asarray(image)
        for city, report_name in (
            ('berlin', 'city_clearance_report.json'),
            ('warsaw', 'city_style_report.json'),
            ('bucharest', 'city_clearance_report.json')):
            report = json.loads((ROOT/f'tools/{city}_landmarks'/report_name).read_text())
            if city == 'warsaw':
                # All Warsaw province pixels, including houses restored there.
                provinces = np.asarray(Image.open(ROOT/'map/provinces.bmp').convert('RGB'))
                yy, xx = np.where(np.all(provinces == [44, 159, 148], axis=2))
                cells = [{'x': int(x), 'y': int(y)} for x, y in zip(xx, yy)]
            else:
                cells = report['changes']
            result.append({'city': city, 'cells': [
                {'x': int(c['x']), 'y': int(c['y']),
                 'value': int(pixels[c['y'], c['x']])} for c in cells]})
    return result


def selected_cells(config, width, height):
    assert config['state'] == 207 and config['province'] == 1086
    assert np.isclose(config['scale'], .025)
    assert np.allclose(config['anchor'], [3351.3, 10.06, 1174.7])
    bounds = config.get('footprint_source', ENVELOPE)
    assert np.allclose(bounds, ENVELOPE)
    anchor = np.asarray(config['anchor'])[[0, 2]]
    lower = anchor+np.asarray(bounds)[[0, 2]]*config['scale']
    upper = anchor+np.asarray(bounds)[[1, 3]]*config['scale']
    clearance = HOUSE_RADIUS+PIXEL_RADIUS+EXTRA_MARGIN
    xs = np.arange(max(0, math.floor(lower[0]-clearance)-1),
                   min(width, math.ceil(upper[0]+clearance)+1))
    ys = np.arange(max(0, math.floor(height-upper[1]-clearance)-1),
                   min(height, math.ceil(height-lower[1]+clearance)+1))
    yy, xx = np.meshgrid(ys, xs, indexing='ij')
    centers = np.c_[xx.ravel()+.5, height-yy.ravel()-.5]
    distance = np.linalg.norm(np.maximum(np.maximum(lower-centers, centers-upper), 0), axis=1)
    close = distance <= clearance
    terrain = np.asarray(Image.open(ROOT/'map/terrain.bmp'))
    urban = terrain[yy.ravel(), xx.ravel()] == 13
    selected = close & urban
    x, y = xx.ravel()[selected], yy.ravel()[selected]
    provinces = np.asarray(Image.open(ROOT/'map/provinces.bmp').convert('RGB'))
    outside = [{'x': int(cx), 'y': int(cy)} for cx, cy in zip(x, y)
               if not np.array_equal(provinces[cy, cx], [5, 81, 210])]
    return x, y, {
        'world_bounds_xz': [lower.tolist(), upper.tolist()],
        'envelope_source_xz': bounds,
        'house_maximum_horizontal_radius': HOUSE_RADIUS,
        'pixel_half_diagonal': PIXEL_RADIUS, 'additional_margin': EXTRA_MARGIN,
        'clearance_from_envelope': clearance,
        'urban_pixels_selected': int(selected.sum()),
        'nonurban_pixels_ignored': int((close & ~urban).sum()),
        'selected_cells_outside_jerusalem_province': outside,
    }


def main():
    config = json.loads((HERE/'config.json').read_text(encoding='utf-8-sig'))
    protected = protected_assets()
    prior_cities = previous_city_cells()
    original = CITY_MAP.read_bytes()
    assert original[:2] == b'BM'
    offset = struct.unpack_from('<I', original, 10)[0]
    width, height = struct.unpack_from('<ii', original, 18)
    assert width > 0 and height > 0 and struct.unpack_from('<HI', original, 28) == (8, 0)
    stride = (width+3)//4*4
    assert len(original) >= offset+stride*height
    assigned = {int(v) for v in re.findall(r'color_index\s*=\s*(\d+)',
                (ROOT/'map/cities.txt').read_text(encoding='utf-8-sig'))}
    assert SOURCE_INDEX in assigned and EMPTY_INDEX not in assigned
    x, y, scope = selected_cells(config, width, height)
    indices = offset+(height-1-y)*stride+x
    selected = set(map(int, indices))
    report_path = HERE/'city_clearance_report.json'
    prior = json.loads(report_path.read_text()) if report_path.exists() else {}
    result = bytearray(original)
    values = np.frombuffer(result, dtype=np.uint8)
    retained, restored = [], []
    for c in prior.get('changes', []):
        at = offset+(height-1-c['y'])*stride+c['x']
        if values[at] != EMPTY_INDEX:
            assert at not in selected, 'A selected city cell was independently changed'
            continue
        assert c['from'] == SOURCE_INDEX and c['to'] == EMPTY_INDEX
        if at in selected:
            retained.append(c)
        else:
            values[at] = SOURCE_INDEX
            restored.append(c)
    previous = values[indices].copy()
    assert set(previous) <= {SOURCE_INDEX, EMPTY_INDEX}
    changed = previous == SOURCE_INDEX
    values[indices[changed]] = EMPTY_INDEX
    changes = retained+[
        {'x': int(cx), 'y': int(cy), 'from': SOURCE_INDEX, 'to': EMPTY_INDEX}
        for cx, cy in zip(x[changed], y[changed])]
    actual = set(map(int, np.flatnonzero(values != np.frombuffer(original, dtype=np.uint8))))
    restored_at = {offset+(height-1-c['y'])*stride+c['x'] for c in restored}
    assert actual == set(map(int, indices[changed])) | restored_at
    assert result[:offset] == original[:offset]
    assert (values[indices] == EMPTY_INDEX).all()
    backup = HERE/'runtime/cities_before_western_wall_clearance.bmp'
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        backup.write_bytes(original)
    # HOI4 may memory-map the file while running. Patch only the changed bytes
    # in place: opening with wb would first truncate that mapped file and fail.
    with CITY_MAP.open('r+b') as handle:
        for at in sorted(actual):
            handle.seek(at)
            handle.write(result[at:at+1])
        handle.flush()
    assert CITY_MAP.read_bytes() == result
    with Image.open(CITY_MAP) as image:
        assert image.mode == 'P' and image.size == (width, height)
        image.verify()
    assert protected_assets() == protected
    assert previous_city_cells() == prior_cities
    report = {
        'status': 'PASS', 'source': 'map/cities.bmp', 'width': width,
        'height': height, 'pixel_offset': offset,
        'unchanged_header_palette_sha256': sha(original[:offset]),
        'baseline_before_sha256': prior.get('baseline_before_sha256', sha(original)),
        'before_sha256': sha(original), 'after_sha256': sha(result),
        'empty_city_style_index': EMPTY_INDEX, 'scope': scope,
        'changed_pixel_count': len(changes), 'newly_cleared_this_run': int(changed.sum()),
        'restored_this_run': len(restored), 'modified_this_run': len(actual),
        'changes': changes, 'restored_pixels': restored,
        'approved_assets_unchanged': protected,
        'approved_previous_city_cells_unchanged': prior_cities,
        'backup': str(backup.relative_to(HERE)),
        'reload': 'cityreload or restart HOI4; new landmark history requires a new game',
        'scope_note': 'Only the listed local urban city-mask bytes; all other file bytes identical.',
    }
    report_path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(f'PASS: {len(changes)} local urban house cells clear; {len(actual)} bytes changed; all other bytes and approved landmarks preserved.')


if __name__ == '__main__':
    main()
