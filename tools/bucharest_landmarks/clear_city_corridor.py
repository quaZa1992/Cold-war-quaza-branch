# IMPERIA CW — Cold War: bucharest landmarks — clear city corridor.
"""Clear only urban decorative houses within Casa Scinteii's local envelope.

The indexed BMP is patched byte-for-byte. This tool never repaints terrain,
changes a city style, removes forest, or writes Berlin/Warsaw source assets.
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
URBAN_TERRAIN = 13
HOUSE_RADIUS = 1.309592
PIXEL_RADIUS = math.sqrt(.5)
EXTRA_MARGIN = .08
ENVELOPE_METRES = [280., 260.]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def protected_assets():
    paths = []
    for city in ('berlin', 'warsaw'):
        paths += list((ROOT/'gfx/models/buildings/landmarks').glob(f'landmark_{city}_*.mesh'))
        paths += list((ROOT/'gfx/models/buildings/landmarks').glob(f'mdcw_{city}_*.dds'))
        paths += list((ROOT/'gfx/entities').glob(f'mdcw_{city}*'))
        paths += list((ROOT/f'tools/{city}_landmarks/source').glob('*.blend'))
    paths += [ROOT/name for name in ('map/provinces.bmp', 'map/terrain.bmp',
              'map/heightmap.bmp', 'map/ambient_object.txt', 'map/cities.txt')]
    return {str(path.relative_to(ROOT)): sha(path.read_bytes()) for path in sorted(set(paths))}


def selected_cells(config, width, height):
    """Use pixel centres and a rotation/jitter-safe distance from the rectangle."""
    anchor = np.asarray(config['anchor'], dtype=float)[[0, 2]]
    bounds = config.get('footprint_source', [-140., 140., -130., 130.])
    lower = anchor+np.asarray(bounds)[[0, 2]]*float(config['scale'])
    upper = anchor+np.asarray(bounds)[[1, 3]]*float(config['scale'])
    clearance = HOUSE_RADIUS+PIXEL_RADIUS+EXTRA_MARGIN
    xs = np.arange(max(0, int(math.floor(lower[0]-clearance))-1),
                   min(width, int(math.ceil(upper[0]+clearance))+1))
    ys = np.arange(max(0, int(math.floor(height-upper[1]-clearance))-1),
                   min(height, int(math.ceil(height-lower[1]+clearance))+1))
    yy, xx = np.meshgrid(ys, xs, indexing='ij')
    centers = np.c_[xx.ravel()+.5, height-yy.ravel()-.5]
    delta = np.maximum(np.maximum(lower-centers, centers-upper), 0)
    close = np.linalg.norm(delta, axis=1) <= clearance
    terrain = np.asarray(Image.open(ROOT/'map/terrain.bmp'))
    urban = terrain[yy.ravel(), xx.ravel()] == URBAN_TERRAIN
    selected = close & urban
    return xx.ravel()[selected], yy.ravel()[selected], {
        'world_bounds_xz': [lower.tolist(), upper.tolist()],
        'envelope_source_xz': bounds,
        'house_maximum_horizontal_radius': HOUSE_RADIUS,
        'pixel_half_diagonal': PIXEL_RADIUS,
        'additional_margin': EXTRA_MARGIN,
        'clearance_from_envelope': clearance,
        'urban_pixels_selected': int(selected.sum()),
        'nonurban_pixels_ignored': int((close & ~urban).sum()),
    }


def main():
    config = json.loads((HERE/'config.json').read_text(encoding='utf-8-sig'))
    assert config['province'] == 9617 and config['state'] == 150
    before_protected = protected_assets()
    original = CITY_MAP.read_bytes()
    assert original[:2] == b'BM'
    offset = struct.unpack_from('<I', original, 10)[0]
    width, height = struct.unpack_from('<ii', original, 18)
    assert width > 0 and height > 0 and struct.unpack_from('<HI', original, 28) == (8, 0)
    stride = (width+3)//4*4
    assert offset+stride*height <= len(original)
    assigned = {int(value) for value in re.findall(r'color_index\s*=\s*(\d+)',
                (ROOT/'map/cities.txt').read_text(encoding='utf-8-sig'))}
    assert SOURCE_INDEX in assigned and EMPTY_INDEX not in assigned
    x, y, scope = selected_cells(config, width, height)
    indices = offset+(height-1-y)*stride+x
    selected = set(map(int, indices))
    prior_path = HERE/'city_clearance_report.json'
    prior = json.loads(prior_path.read_text()) if prior_path.exists() else {}
    result = bytearray(original)
    values = np.frombuffer(result, dtype=np.uint8)
    retained, restored = [], []
    for change in prior.get('changes', []):
        at = offset+(height-1-change['y'])*stride+change['x']
        # A changed value belongs to another edit, so never overwrite it.
        if values[at] != EMPTY_INDEX:
            assert at not in selected, 'A selected city cell was independently edited'
            continue
        assert change['from'] == SOURCE_INDEX and change['to'] == EMPTY_INDEX
        if at in selected:
            retained.append(change)
        else:
            values[at] = SOURCE_INDEX
            restored.append(change)
    old = values[indices].copy()
    assert set(old) <= {SOURCE_INDEX, EMPTY_INDEX}, 'Selected cells contain an independently edited city style'
    changed = old == SOURCE_INDEX
    values[indices[changed]] = EMPTY_INDEX
    new = [{'x': int(cx), 'y': int(cy), 'from': SOURCE_INDEX, 'to': EMPTY_INDEX}
           for cx, cy in zip(x[changed], y[changed])]
    changes = retained+new
    actual = set(map(int, np.flatnonzero(values != np.frombuffer(original, dtype=np.uint8))))
    restored_at = {offset+(height-1-e['y'])*stride+e['x'] for e in restored}
    assert actual == set(map(int, indices[changed])) | restored_at
    assert result[:offset] == original[:offset], 'BMP header/palette changed'
    assert (values[indices] == EMPTY_INDEX).all()
    provinces = np.asarray(Image.open(ROOT/'map/provinces.bmp'))
    rgb = np.asarray([129, 45, 89])
    outside = [(int(cx), int(cy)) for cx, cy in zip(x, y) if not np.array_equal(provinces[cy, cx], rgb)]
    backup = HERE/'runtime/cities_before_scinteii_clearance.bmp'
    backup.parent.mkdir(exist_ok=True)
    if not backup.exists():
        backup.write_bytes(original)
    CITY_MAP.write_bytes(result)
    with Image.open(CITY_MAP) as image:
        assert image.mode == 'P' and image.size == (width, height)
        image.verify()
    assert before_protected == protected_assets(), 'Previously approved model or map assets changed'
    report = {
        'status': 'PASS', 'source': 'map/cities.bmp',
        'width': width, 'height': height, 'pixel_offset': offset,
        'unchanged_header_palette_sha256': sha(original[:offset]),
        'baseline_before_sha256': prior.get('baseline_before_sha256', sha(original)),
        'before_sha256': sha(original), 'after_sha256': sha(result),
        'empty_city_style_index': EMPTY_INDEX,
        'scope': scope, 'changed_pixel_count': len(changes),
        'newly_cleared_this_run': int(changed.sum()),
        'restored_this_run': len(restored), 'modified_this_run': len(actual),
        'changes': changes, 'restored_pixels': restored,
        'selected_cells_outside_bucharest_province': outside,
        'approved_assets_unchanged': before_protected,
        'backup': str(backup.relative_to(HERE)),
        'reload': 'cityreload or restart HOI4',
    }
    prior_path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(f'PASS: {len(changes)} urban house cells clear; {len(actual)} bytes changed this run; all other bytes and approved landmarks preserved.')


if __name__ == '__main__':
    main()
