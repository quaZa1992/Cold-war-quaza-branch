# IMPERIA CW — Cold War: jerusalem landmarks — placement.
"""Integrate the Jerusalem landmark and keep its local visual footprint clear.

The ordinary spawn edits affect presentation only. Building levels, supply-node
provinces, railways, ownership and the existing Dome of Rock remain unchanged.
"""
from functools import lru_cache
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import sys

sys.dont_write_bytecode = True
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'tools/berlin_landmarks'))
from pdx import read, meshes
_spec = importlib.util.spec_from_file_location('jerusalem_placement_clearance', HERE/'clear_city_corridor.py')
_clearance = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_clearance)
protected_assets = _clearance.protected_assets

BUILDING = 'landmark_jerusalem_western_wall'
SPAWN_ROW = '207;western_wall_spawn;3351.30;10.06;1174.70;0.00;0'
FOOTPRINT = np.array([[3350.3, 1173.9875], [3351.5, 1173.9875],
                      [3351.5, 1175.4125], [3350.3, 1175.4125]])
DOME = {'path': 'gfx/models/buildings/landmarks/domeofrock.mesh',
        'combined_scale': .2, 'anchor': [3353.58, 10.80, 1173.92], 'rotation': 1.31}
FACTORY = {'path': 'gfx/models/buildings/factory.mesh', 'combined_scale': 1.4}
AIRBASE = {'path': 'gfx/models/buildings/hangar_flight.mesh', 'combined_scale': 1.4}
# Preserve original visual rotations except the two factory orientations which
# otherwise cannot remain fully inside Jerusalem while clearing the landmarks.
MOVES = [
    ('207;industrial_complex;3351.00;9.90;1173.00;5.35;0', 3350.6, 1172.6, 0.),
    ('207;industrial_complex;3350.00;9.80;1173.00;4.40;0', 3350.5, 1172.5, 4.4),
    ('207;arms_factory;3351.00;9.90;1174.00;5.86;0', 3350.6, 1172.4, 5.86),
    ('207;arms_factory;3352.00;10.12;1173.00;2.24;0', 3350.6, 1172.6, 0.),
    ('207;arms_factory;3352.00;10.12;1173.00;4.91;0', 3350.6, 1172.6, 4.91),
    ('207;arms_factory;3351.00;9.90;1173.00;2.75;0', 3350.7, 1172.6, 2.75),
    ('207;arms_factory;3351.00;9.90;1173.00;2.85;0', 3350.8, 1172.7, 2.85),
    ('207;air_base;3352.50;10.30;1172.74;3.36;0', 3351.3, 1171.5, 3.36),
]
INSERTED_BLOCK = '''\t\t# Western Wall landmark in the 1970 setup.
\t\t1967.6.10 = {
\t\t\tbuildings = {
\t\t\t\t1086 = { landmark_jerusalem_western_wall = 1 }
\t\t\t}
\t\t}

'''
HISTORY_MARKER = '\t\t# MDCW1970 verified unchanged geography; native base/future history preserved.'


def sha(data):
    return hashlib.sha256(data).hexdigest()


@lru_cache(maxsize=None)
def native_model(path, scale):
    vertices, triangles = [], []
    count = 0
    for _, shape in meshes(read(ROOT/path)):
        try:
            p = shape.prop('p').value.reshape(-1, 3).astype(float)*scale
            t = shape.prop('tri').value.reshape(-1, 3)
        except StopIteration:
            continue
        vertices.append(p)
        triangles.append(t+count)
        count += len(p)
    return np.concatenate(vertices), np.concatenate(triangles)


def world_vertices(path, scale, anchor, rotation, sign=1):
    vertices, _ = native_model(path, scale)
    a = rotation*sign
    c, s = math.cos(a), math.sin(a)
    result = vertices.copy()
    result[:, [0, 2]] = np.column_stack((c*vertices[:, 0]+s*vertices[:, 2],
                                       -s*vertices[:, 0]+c*vertices[:, 2]))
    return result+np.asarray(anchor)


def hull(points):
    points = sorted(set(tuple(p) for p in points))
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lower, upper = [], []
    for point in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    for point in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return np.array(lower[:-1]+upper[:-1])


def projected_overlaps(vertices, triangles, polygon):
    """Count nonzero native triangle projections intersecting a convex polygon."""
    points = vertices[:, [0, 2]]
    projected = points[triangles]
    v, w = projected[:, 1]-projected[:, 0], projected[:, 2]-projected[:, 0]
    area = np.abs(v[:, 0]*w[:, 1]-v[:, 1]*w[:, 0])
    selected = area > 1e-10
    # Polygon edge normals are common to every candidate triangle.
    edges = np.roll(polygon, -1, axis=0)-polygon
    for edge in edges:
        axis = np.array([-edge[1], edge[0]])
        axis /= np.linalg.norm(axis)
        p = projected@axis
        q = polygon@axis
        selected &= (p.max(axis=1) >= q.min()-1e-9) & (p.min(axis=1) <= q.max()+1e-9)
    at = np.flatnonzero(selected)
    projected = projected[at]
    if not len(projected):
        return 0
    # Each triangle contributes its three additional SAT axes.
    edges = np.roll(projected, -1, axis=1)-projected
    axes = np.stack((-edges[:, :, 1], edges[:, :, 0]), axis=-1)
    for edge_no in range(3):
        axis = axes[:, edge_no]
        p = np.einsum('nvi,ni->nv', projected, axis)
        q = np.einsum('vi,ni->nv', polygon, axis)
        selected[at] &= ((p.max(axis=1) >= q.min(axis=1)-1e-9)
                         & (p.min(axis=1) <= q.max(axis=1)+1e-9))
    return int(selected.sum())


def read_row(row):
    fields = row.split(';')
    return fields[1], list(map(float, fields[2:5])), float(fields[5])


def model_for(kind):
    return AIRBASE if kind == 'air_base' else FACTORY


def geometry_record(row, model, province_mask, dome_polygon):
    kind, anchor, rotation = read_row(row)
    _, triangles = native_model(model['path'], model['combined_scale'])
    results = []
    for sign in (1, -1):
        vertices = world_vertices(model['path'], model['combined_scale'], anchor, rotation, sign)
        xx = np.floor(vertices[:, 0]).astype(int)
        yy = np.floor(province_mask.shape[0]-vertices[:, 2]).astype(int)
        anchor_x, anchor_y = math.floor(anchor[0]), math.floor(province_mask.shape[0]-anchor[2])
        results.append({
            'rotation_sign': sign,
            'wall_projected_triangle_overlaps': projected_overlaps(vertices, triangles, FOOTPRINT),
            'dome_convex_footprint_triangle_overlaps': projected_overlaps(vertices, triangles, dome_polygon),
            'anchor_inside_province_1086': bool(province_mask[anchor_y, anchor_x]),
            'native_vertices_inside_province_1086': bool(province_mask[yy, xx].all()),
            'world_bounds_xz': [vertices[:, [0, 2]].min(0).tolist(), vertices[:, [0, 2]].max(0).tolist()],
        })
    return results


def ground_height(x, z, heightmap):
    y = heightmap.shape[0]-z
    i, j = math.floor(x), math.floor(y)
    u, v = x-i, y-j
    return float((1-u)*(1-v)*heightmap[j, i]+u*(1-v)*heightmap[j, i+1]
                 +(1-u)*v*heightmap[j+1, i]+u*v*heightmap[j+1, i+1])/10


def main():
    config = json.loads((HERE/'config.json').read_text(encoding='utf-8-sig'))
    assert config['province'] == 1086 and config['state'] == 207
    assert np.allclose(config['anchor'], [3351.3, 10.06, 1174.7])
    protected = protected_assets()
    gameplay_files = ['map/supply_nodes.txt', 'map/railways.txt']
    gameplay_before = {name: sha((ROOT/name).read_bytes()) for name in gameplay_files}
    provinces = np.asarray(Image.open(ROOT/'map/provinces.bmp').convert('RGB'))
    province_mask = np.all(provinces == [5, 81, 210], axis=2)
    heightmap = np.asarray(Image.open(ROOT/'map/heightmap.bmp'))
    dome_polygon = hull(np.concatenate([
        world_vertices(DOME['path'], DOME['combined_scale'], DOME['anchor'], DOME['rotation'], sign)[:, [0, 2]]
        for sign in (1, -1)]))
    runtime = HERE/'runtime'
    runtime.mkdir(parents=True, exist_ok=True)
    buildings_path = ROOT/'map/buildings.txt'
    history_path = ROOT/'history/states/207-Jerusalem.txt'
    original_buildings = buildings_path.read_bytes()
    original_history = history_path.read_bytes()
    backup_buildings = runtime/'buildings_before_western_wall.txt'
    backup_history = runtime/'history_before_western_wall.txt'
    if not backup_buildings.exists():
        backup_buildings.write_bytes(original_buildings)
    if not backup_history.exists():
        backup_history.write_bytes(original_history)
    result_buildings = original_buildings
    visual_edits = []
    for old_row, x, z, rotation in MOVES:
        fields = old_row.split(';')
        new_row = ';'.join([fields[0], fields[1], f'{x:.2f}',
                            f'{ground_height(x, z, heightmap):.2f}', f'{z:.2f}',
                            f'{rotation:.2f}', fields[6]])
        old, new = old_row.encode(), new_row.encode()
        if old in result_buildings:
            assert result_buildings.count(old) == 1
            result_buildings = result_buildings.replace(old, new, 1)
        else:
            assert result_buildings.count(new) == 1
        model = model_for(fields[1]).copy()
        model['sha256'] = sha((ROOT/model['path']).read_bytes())
        before = geometry_record(old_row, model, province_mask, dome_polygon)
        after = geometry_record(new_row, model, province_mask, dome_polygon)
        assert any(g['wall_projected_triangle_overlaps'] for g in before)
        assert all(g['wall_projected_triangle_overlaps'] == 0 for g in after)
        assert all(g['dome_convex_footprint_triangle_overlaps'] == 0 for g in after)
        assert all(g['anchor_inside_province_1086'] for g in after)
        if fields[1] != 'air_base':
            assert all(g['native_vertices_inside_province_1086'] for g in after)
        visual_edits.append({'old_row': old_row, 'new_row': new_row, 'model': model,
                             'before': before, 'after': after})
    newline = b'\r\n' if b'\r\n' in original_buildings else b'\n'
    if SPAWN_ROW.encode() not in result_buildings:
        assert result_buildings.endswith(newline)
        result_buildings += SPAWN_ROW.encode()+newline
    assert result_buildings.count(SPAWN_ROW.encode()) == 1
    reversed_buildings = result_buildings.replace(SPAWN_ROW.encode()+newline, b'', 1)
    for edit in visual_edits:
        reversed_buildings = reversed_buildings.replace(edit['new_row'].encode(), edit['old_row'].encode(), 1)
    assert reversed_buildings == backup_buildings.read_bytes(), 'Unrelated map/buildings bytes changed'
    history_newline = b'\r\n' if b'\r\n' in original_history else b'\n'
    inserted = INSERTED_BLOCK.encode().replace(b'\n', history_newline)
    result_history = original_history
    if inserted not in result_history:
        assert BUILDING.encode() not in result_history
        marker = HISTORY_MARKER.encode()
        assert result_history.count(marker) == 1
        result_history = result_history.replace(marker, inserted+marker, 1)
    assert result_history.count(inserted) == 1
    assert result_history.replace(inserted, b'', 1) == backup_history.read_bytes(), 'Unrelated state history changed'
    buildings_path.write_bytes(result_buildings)
    history_path.write_bytes(result_history)
    assert protected_assets() == protected
    assert {name: sha((ROOT/name).read_bytes()) for name in gameplay_files} == gameplay_before
    active_rows = {
        '207;internet_station;3350.00;9.80;1173.00;0.69;0': {'path': 'gfx/models/buildings/celltower.mesh', 'combined_scale': .1},
        '207;anti_air_building;3350.00;9.82;1172.00;1.30;0': {'path': 'gfx/models/buildings/88aagun.mesh', 'combined_scale': .12},
        '207;supply_node;3351.00;9.95;1172.00;0.63;0': {'path': 'gfx/models/buildings/supply_station.mesh', 'combined_scale': 2.},
    }
    active_checks = []
    for row, model in active_rows.items():
        assert row.encode() in result_buildings
        model = model | {'sha256': sha((ROOT/model['path']).read_bytes())}
        record = geometry_record(row, model, province_mask, dome_polygon)
        assert all(g['wall_projected_triangle_overlaps'] == 0 for g in record)
        active_checks.append({'row': row, 'model': model, 'geometry': record, 'changed': False})
    report = {
        'status': 'PASS', 'scope': 'One independent landmark spawn, dated initialization, and eight future ordinary visual spawn relocations only',
        'spawn_row': SPAWN_ROW, 'inserted_history_block': INSERTED_BLOCK,
        'history_date': '1967.6.10', 'history_path': str(history_path.relative_to(ROOT)),
        'map_buildings_baseline_sha256': sha(backup_buildings.read_bytes()),
        'map_buildings_after_sha256': sha(result_buildings),
        'history_baseline_sha256': sha(backup_history.read_bytes()),
        'history_after_sha256': sha(result_history),
        'map_buildings_all_other_bytes_identical_when_reversing_listed_edits': True,
        'history_all_other_bytes_identical_when_reversing_inserted_block': True,
        'visual_spawn_edits': visual_edits,
        'unchanged_active_visual_checks': active_checks,
        'landmark_world_envelope': FOOTPRINT.tolist(),
        'dome': DOME | {'sha256': sha((ROOT/DOME['path']).read_bytes()),
                        'both_rotation_convex_footprint': dome_polygon.tolist(), 'changed': False},
        'airbase_footprint_exception': 'Existing airbase mesh is too wide for the tiny Jerusalem province. Its original footprint already spans the border. Its moved anchor remains inside province1086, size and rotation are unchanged, and both landmarks are now clear.',
        'ordinary_1970_levels': {'arms_factory': 0, 'industrial_complex': 0, 'air_base': 0, 'internet_station': 2, 'anti_air_building': 4},
        'collision_method': 'Native nonzero-area mesh triangle projections against the full wall envelope and a conservative Dome convex footprint; SAT checked under both Y rotation sign conventions.',
        'gameplay_files_unchanged': gameplay_before,
        'approved_assets_unchanged': protected,
        'buildings_backup': str(backup_buildings.relative_to(HERE)),
        'history_backup': str(backup_history.relative_to(HERE)),
    }
    (HERE/'placement_report.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('PASS: Western Wall spawn and dated history integrated; eight future visual spawns clear both landmarks; all unrelated map/history bytes preserved.')


if __name__ == '__main__':
    main()
