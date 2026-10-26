# IMPERIA CW — Cold War: bucharest landmarks — validate.
"""Read-only checks for the native Casa Scinteii landmark and local house mask.

Only validation_report.json is written; neither sources nor game files are
repaired. Berlin/Warsaw geometry, materials and their exact mask cells are
checked against the snapshot made before the Bucharest house clearance.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import re
import struct
import sys

sys.dont_write_bytecode = True
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT/'gfx/models/buildings/landmarks'
sys.path.insert(0, str(ROOT/'tools/berlin_landmarks'))
import validate_blender as native
from pdx import meshes, read
sys.path.insert(0, str(ROOT/'tools/warsaw_landmarks'))
from city_style import blocks
spec = importlib.util.spec_from_file_location('warsaw_validation_reuse', ROOT/'tools/warsaw_landmarks/validate.py')
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)
# Warsaw's validator changes this shared helper's slot names on import. Set
# this namespace only after all imports, so no Casa check can use its atlas.
TEXTURES = {slot: f'mdcw_bucharest_scinteii_{suffix}.dds'
            for slot, suffix in [('diff', 'diffuse'), ('n', 'normal'), ('spec', 'specular')]}
native.TEXTURES = TEXTURES.copy()
require = native.require
MODELS = ['landmark_bucharest_scinteii.mesh', 'landmark_bucharest_scinteii_destroyed.mesh']
BUILDING = 'landmark_bucharest_scinteii'
SPAWN = 'bucharest_scinteii_spawn'
SHAPE = 'mdcw_bucharest_scinteii'

spec = importlib.util.spec_from_file_location('bucharest_clearance_reuse', HERE/'clear_city_corridor.py')
clearance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(clearance)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def text(path):
    return path.read_text(encoding='utf-8-sig')


def named_block(source, key):
    found = list(blocks(source, r'^\s*'+re.escape(key)+r'\s*=\s*\{'))
    require(len(found) == 1, f'Expected exactly one {key} block')
    return found[0][2]


def named_entity(source, key):
    found = [value for _, _, value in blocks(source, r'^\s*entity\s*=\s*\{')
             if re.search(r'\bname\s*=\s*"'+re.escape(key)+'"', value)]
    require(len(found) == 1, f'Expected exactly one entity {key}')
    return found[0]


def check_sources(config):
    manifest = json.loads(text(HERE/'blender_export.json'))
    require(bool(manifest.get('blender_version')), 'Missing Blender version')
    require('io_pdx_mesh' in manifest.get('exporter', ''), 'Missing native Blender exporter identity')
    source = HERE/manifest['source']
    require(source.resolve() == (HERE/'source/casa_scinteii.blend').resolve(), 'Unexpected Blender source path')
    raw = source.read_bytes()
    require(raw.startswith(b'BLENDER') and len(raw) > 12, 'Invalid or compressed Blender source')
    require((source.name, sha(raw)) in list(native.source_hash_records(manifest)), 'Stale Blender source hash')
    for name in MODELS:
        require(manifest['mesh_sha256'].get(name) == sha((OUT/name).read_bytes()), f'Stale native export hash: {name}')
    require(np.isclose(manifest['height'], 104, atol=.001), 'Unexpected documented building height')
    require(np.isclose(manifest['scale'], config['scale'], atol=1e-9), 'Manifest scale differs from config')
    require(np.isclose(manifest['display_height'], 104*config['scale'], atol=.001), 'Unexpected display height')
    return {'blender_version': manifest['blender_version'], 'exporter': manifest['exporter'],
            'source': str(source.relative_to(ROOT)), 'source_sha256': sha(raw), 'source_bytes': len(raw)}


def check_models(config):
    result, attributes = {}, []
    for name in MODELS:
        points, record = native.check_mesh(OUT/name, SHAPE)
        require(record['triangles'] < 8000, f'{name}: triangle budget exceeded')
        require(record['vertices'] < 16000, f'{name}: vertex budget exceeded')
        node = next(meshes(read(OUT/name)))[1]
        attrs = {key: node.prop(key).value for key in ('p', 'tri', 'n', 'u0', 'ta')}
        uv, normals, tangent = attrs['u0'].reshape(-1, 2), attrs['n'].reshape(-1, 3), attrs['ta'].reshape(-1, 4)
        require(((uv >= 0) & (uv <= 1)).all(), f'{name}: UVs outside atlas')
        dot = float(np.abs(np.einsum('ij,ij->i', normals, tangent[:, :3])).max())
        require(dot <= .015, f'{name}: nonorthogonal tangent basis')
        require(np.isclose(points[:, 1].min(), -8, atol=.001), f'{name}: expected buried wall footings down to -8m')
        require(np.isclose(points[:, 1].max(), 104, atol=.001), f'{name}: expected 104m historic tower height')
        require(230 < np.ptp(points[:, 0]) <= 280.01 and 200 < np.ptp(points[:, 2]) <= 260.01,
                f'{name}: unexpected architectural footprint proportions')
        bounds = np.asarray(config['footprint_source'])
        require((points[:, 0] >= bounds[0]-.001).all() and (points[:, 0] <= bounds[1]+.001).all()
                and (points[:, 2] >= bounds[2]-.001).all() and (points[:, 2] <= bounds[3]+.001).all(),
                f'{name}: geometry exceeds approved clearance envelope')
        record['maximum_normal_tangent_dot'] = dot
        record['materials'] = 1
        record['triangle_limit_exclusive'] = 8000
        record['vertex_limit_exclusive'] = 16000
        result[name] = record
        attributes.append(attrs)
    for key in ('p', 'tri', 'n', 'u0'):
        require(np.array_equal(attributes[0][key], attributes[1][key]), f'Destroyed fallback differs in {key}')
    require(np.allclose(attributes[0]['ta'], attributes[1]['ta'], rtol=0, atol=2e-6), 'Fallback tangent basis differs')
    normal = np.asarray(Image.open(OUT/TEXTURES['n']).convert('RGBA'))
    require(normal[:, :, 2].max() <= 18, 'Normal map has excessive unintended emissive lighting')
    for slot, name in TEXTURES.items():
        result[name] = previous.check_atlas(OUT/name, slot)
    result['destroyed_fallback_geometry_identical'] = True
    return attributes[0]['p'].reshape(-1, 3), result


def check_city_clearance(config):
    report = json.loads(text(HERE/'city_clearance_report.json'))
    raw = (ROOT/'map/cities.bmp').read_bytes()
    require(sha(raw) == report['after_sha256'], 'City mask differs from Bucharest clearance report')
    offset = struct.unpack_from('<I', raw, 10)[0]
    width, height = struct.unpack_from('<ii', raw, 18)
    require(struct.unpack_from('<HI', raw, 28) == (8, 0), 'City bitmap is not indexed uncompressed 8bit')
    require(sha(raw[:offset]) == report['unchanged_header_palette_sha256'], 'City BMP header/palette changed')
    stride = (width+3)//4*4
    x, y, selected = clearance.selected_cells(config, width, height)
    positions = {(int(cx), int(cy)) for cx, cy in zip(x, y)}
    changed = {(entry['x'], entry['y']) for entry in report['changes']}
    require(len(changed) == len(report['changes']), 'Duplicate city-mask edit records')
    require(changed <= positions, 'City-mask patch includes a nonurban or distant cell')
    reconstructed = bytearray(raw)
    for cx, cy in positions:
        require(raw[offset+(height-1-cy)*stride+cx] == 3, 'A decorative house can overlap the landmark')
    for entry in report['changes']:
        require(entry['from'] == 15 and entry['to'] == 3, 'Unexpected source/destination city style')
        reconstructed[offset+(height-1-entry['y'])*stride+entry['x']] = entry['from']
    require(sha(reconstructed) == report['baseline_before_sha256'], 'Unrelated city bytes changed after Bucharest baseline')
    backup = (HERE/report['backup']).read_bytes()
    require(bytes(reconstructed) == backup, 'Reversing only Casa edits does not recreate the saved original bitmap')
    warsaw = json.loads(text(ROOT/'tools/warsaw_landmarks/city_style_report.json'))
    require(sha(reconstructed) == warsaw['cities_bmp_after_sha256'], 'Bucharest baseline does not retain approved Warsaw/Berlin city mask')
    for entry in warsaw['warsaw_pixel_edits']:
        at = offset+(height-1-entry['y'])*stride+entry['x']
        require(raw[at] == entry['new_index'], 'An approved Warsaw city cell changed')
    berlin = json.loads(text(ROOT/'tools/berlin_landmarks/city_clearance_report.json'))
    for entry in berlin['changes']:
        at = offset+(height-1-entry['y'])*stride+entry['x']
        require(raw[at] == entry['to'], 'An approved Berlin city cell changed')
    for name, digest in report['approved_assets_unchanged'].items():
        require(sha((ROOT/name).read_bytes()) == digest, f'Previously approved source/map asset changed: {name}')
    require(clearance.protected_assets() == report['approved_assets_unchanged'], 'Protected asset snapshot differs')
    return {'cleared_urban_pixels': len(changed), 'selected_urban_pixels': len(positions),
            'all_other_bitmap_bytes_unchanged': True, 'header_palette_unchanged': True,
            'Warsaw_and_Berlin_exact_city_cells_unchanged': True,
            'Berlin_Warsaw_sources_meshes_textures_entities_unchanged': True,
            'scope': selected}


def check_integration(points, config):
    require(config['state'] == 150 and config['province'] == 9617, 'Unexpected landmark state/province')
    require(np.allclose(config['anchor'], [3214.2, 9.8, 1410.1], atol=1e-6), 'Unexpected landmark anchor')
    require(np.isclose(config['scale'], .014, atol=1e-9), 'Unexpected map scale')
    common = text(ROOT/'common/buildings/mdcw_bucharest_landmarks.txt')
    building = named_block(common, BUILDING)
    require(re.search(r'\bspawn_point\s*=\s*'+SPAWN+r'\b', building), 'Building has no independent Casa spawn')
    require(re.search(r'\bis_buildable\s*=\s*no\b', building), 'Historical landmark should not be normally buildable')
    require(re.search(r'\bshow_modifier\s*=\s*yes\b', building), 'Administration bonus is not visible in the landmark tooltip')
    modifiers = named_block(named_block(building, 'country_modifiers'), 'modifiers')
    cost = re.findall(r'\bbureaucracy_cost_multiplier_modifier\s*=\s*([-.\d]+)', modifiers)
    require(len(cost) == 1 and np.isclose(float(cost[0]), -.03), 'Unexpected administration cost bonus')
    spawn = named_block(common, SPAWN)
    for pattern in (r'\btype\s*=\s*province\b', r'\bmax\s*=\s*1\b', r'\bdisable_auto_nudging\s*=\s*yes\b'):
        require(re.search(pattern, spawn), 'Spawn is missing province/max1/protected-position settings')
    asset = text(ROOT/'gfx/entities/mdcw_bucharest_landmarks.asset')
    gfx = text(ROOT/'gfx/entities/mdcw_bucharest_landmarks.gfx')
    for suffix in ('', '_destroyed'):
        entity = named_entity(asset, 'building_'+BUILDING+suffix)
        require(re.search(r'\bpdxmesh\s*=\s*"'+SHAPE+suffix+'_mesh"', entity), 'Entity references the wrong native mesh')
        scale = re.findall(r'\bscale\s*=\s*([\d.]+)', entity)
        require(len(scale) == 1 and np.isclose(float(scale[0]), config['scale']), 'Entity map scale differs')
        definitions = [value for _, _, value in blocks(gfx, r'^\s*pdxmesh\s*=\s*\{')
                       if re.search(r'\bname\s*=\s*"'+SHAPE+suffix+'_mesh"', value)]
        require(len(definitions) == 1, 'Missing unique pdxmesh definition')
        require('gfx/models/buildings/landmarks/'+BUILDING+suffix+'.mesh' in definitions[0], 'Wrong native model path')
        require(all(name in definitions[0] for name in TEXTURES.values()), 'Gfx definition misses atlas slots')
        require('PdxMeshAdvancedSnow' in definitions[0], 'Missing snow-capable shader')
    require('clone = "building_landmark_spawn"' in named_entity(asset, 'building_'+SPAWN), 'Spawn placeholder alias missing')
    rows = re.findall(r'^150;'+SPAWN+r';([^;]+);([^;]+);([^;]+);([^;]+);', text(ROOT/'map/buildings.txt'), re.M)
    require(len(rows) == 1, 'Casa needs exactly one independent map row')
    row = np.asarray(list(map(float, rows[0])))
    require(np.allclose(row[:3], config['anchor'], atol=1e-6) and np.isclose(row[3], 0), 'Map anchor or rotation differs')
    history = text(ROOT/'history/states/150-Wallachia.txt')
    dated = named_block(history, '1957.1.1')
    province = named_block(named_block(dated, 'buildings'), '9617')
    require(re.search(r'\b'+BUILDING+r'\s*=\s*1\b', province), 'Casa is not initialized in Bucharest before 1970')
    province_map = np.asarray(Image.open(ROOT/'map/provinces.bmp'))
    world = points[:, [0, 2]]*config['scale']+np.asarray(config['anchor'])[[0, 2]]
    source = np.asarray(config['footprint_source'])
    xx, zz = np.meshgrid(np.linspace(source[0], source[1], 101), np.linspace(source[2], source[3], 101))
    envelope = np.c_[xx.ravel(), zz.ravel()]*config['scale']+np.asarray(config['anchor'])[[0, 2]]
    for label, sample in [('native vertices', world), ('full conservative envelope', envelope)]:
        px, py = np.floor(sample[:, 0]).astype(int), np.floor(province_map.shape[0]-sample[:, 1]).astype(int)
        require(((px >= 0) & (px < province_map.shape[1]) & (py >= 0) & (py < province_map.shape[0])).all(), f'{label} leave map')
        require(np.all(province_map[py, px] == [129, 45, 89]), f'{label} extend outside Bucharest province')
    icon_gfx = text(ROOT/'interface/mdcw_bucharest_landmarks.gfx')
    icon = re.search(r'\bspecial_icon\s*=\s*(\w+)', building)
    require(icon and icon[1] in icon_gfx, 'Building icon has no interface definition')
    textures = re.findall(r'\btexturefile\s*=\s*"([^"]+)"', icon_gfx, re.I)
    require(len(textures) == 2, 'Expected normal and small landmark icons')
    for filename in textures:
        with Image.open(ROOT/filename) as image:
            require(image.size in [(128, 64), (64, 32)], f'Unexpected landmark icon dimensions: {filename}')
            image.verify()
    for language in ('english', 'german'):
        files = list((ROOT/'localisation'/language).glob('*bucharest*.yml'))
        require(len(files) == 1, f'Expected one {language} Casa localization')
        raw = files[0].read_bytes()
        require(raw.startswith(b'\xef\xbb\xbf'), f'{language} localization needs UTF8 BOM')
        for key in (BUILDING, BUILDING+'_plural', BUILDING+'_desc'):
            require(re.search(r'^\s*'+key+r':', raw.decode('utf-8-sig'), re.M), f'{language} localization misses {key}')
    return {'anchor': row[:3].tolist(), 'rotation': float(row[3]), 'scale': config['scale'],
            'documented_height_metres': 104, 'display_height_above_ground': 104*config['scale'],
            'buried_wall_footings_metres': -8, 'province': 9617,
            'native_vertices_and_full_envelope_inside_Bucharest': True,
            'world_bounds_xz': [world.min(0).tolist(), world.max(0).tolist()],
            'history_initialization': '1957.1.1',
            'country_modifiers': {'bureaucracy_cost_multiplier_modifier': -.03},
            'show_modifier': True}


def projected_mesh(filename, scale, anchor, rotation=0):
    """Conservative architectural footprint from actual native triangles."""
    rotate = np.asarray([[math.cos(rotation), math.sin(rotation)],
                         [-math.sin(rotation), math.cos(rotation)]])
    triangles, vertices = [], []
    for _, node in meshes(read(ROOT/filename)):
        try:
            points = node.prop('p').value.reshape(-1, 3)*scale
            indices = node.prop('tri').value.reshape(-1, 3)
        except StopIteration:
            continue
        world = points[:, [0, 2]]@rotate.T+np.asarray(anchor)
        candidate = world[indices]
        a, b = candidate[:, 1]-candidate[:, 0], candidate[:, 2]-candidate[:, 0]
        nonzero = np.abs(a[:, 0]*b[:, 1]-a[:, 1]*b[:, 0]) > 1e-10
        triangles.append(candidate[nonzero])
        vertices.append(world)
    return np.concatenate(triangles), np.concatenate(vertices)


def projected_overlap_count(first, second):
    """Triangle SAT includes touching roofs and footings as a collision."""
    total = 0
    lower, upper = second.min(axis=1), second.max(axis=1)
    for triangle in first:
        candidates = second[np.all(upper >= triangle.min(0), axis=1)
                            & np.all(lower <= triangle.max(0), axis=1)]
        if not len(candidates):
            continue
        edge_a = np.roll(triangle, -1, axis=0)-triangle
        edge_b = np.roll(candidates, -1, axis=1)-candidates
        axes = np.concatenate([np.tile(edge_a[None], (len(candidates), 1, 1)), edge_b], axis=1)
        axes = axes[:, :, [1, 0]]*np.asarray([-1, 1])
        first_projected = np.einsum('ij,nkj->nki', triangle, axes)
        second_projected = np.einsum('nij,nkj->nki', candidates, axes)
        separated = ((first_projected.max(2) < second_projected.min(2)-1e-9)
                     | (second_projected.max(2) < first_projected.min(2)-1e-9))
        total += int((~separated.any(axis=1)).sum())
    return total


def check_ordinary_placement(config):
    report = json.loads(text(HERE/'placement_report.json'))
    current = (ROOT/'map/buildings.txt').read_bytes()
    require(sha(current) == report['map_buildings_after_sha256'], 'Visual map rows differ from scoped placement audit')
    reconstructed = current
    casa, _ = projected_mesh('gfx/models/buildings/landmarks/'+MODELS[0], config['scale'],
                             np.asarray(config['anchor'])[[0, 2]])
    provinces = np.asarray(Image.open(ROOT/'map/provinces.bmp'))
    result = []
    for edit in report['visual_spawn_edits']:
        old, new = edit['old_row'].encode(), edit['new_row'].encode()
        require(current.count(new) == 1 and current.count(old) == 0, 'A nudged ordinary spawn is missing or duplicated')
        reconstructed = reconstructed.replace(new, old, 1)
        before, after = edit['old_row'].split(';'), edit['new_row'].split(';')
        require(all(before[i] == after[i] for i in [0, 1, 3, 5, 6]), 'Visual nudge changed state, type, elevation, rotation or metadata')
        anchor = [float(after[2]), float(after[4])]
        counts = []
        for sign in (1, -1):
            triangle, vertex = projected_mesh(edit['mesh'], edit['combined_scale'], anchor, float(after[5])*sign)
            counts.append(projected_overlap_count(casa, triangle))
            px = np.floor(vertex[:, 0]).astype(int)
            py = np.floor(provinces.shape[0]-vertex[:, 1]).astype(int)
            require(np.all(provinces[py, px] == [129, 45, 89]), 'Nudged native building footprint leaves Bucharest province')
        require(counts == [0, 0], 'An ordinary visual spawn still intersects the landmark footprint')
        result.append({'type': after[1], 'anchor': anchor, 'native_projected_triangle_overlaps_both_rotations': counts,
                       'native_vertices_inside_province_9617': True})
    require(sha(reconstructed) == report['map_buildings_before_sha256'], 'Unrelated map-building bytes changed during visual nudges')
    for name, digest in report['gameplay_files_unchanged'].items():
        require(sha((ROOT/name).read_bytes()) == digest, f'Ordinary placement adjustment changed gameplay file: {name}')
    return {'visual_rows_adjusted': result, 'all_other_building_rows_byte_identical': True,
            'supply_node_province_railways_and_ordinary_history_levels_unchanged': True}


def main():
    report = {'status': 'FAIL', 'scope': 'Read-only; only validation_report.json is written'}
    try:
        config = json.loads(text(HERE/'config.json'))
        report['Blender_source'] = check_sources(config)
        points, report['native_models'] = check_models(config)
        report['city_clearance_and_preservation'] = check_city_clearance(config)
        report['integration'] = check_integration(points, config)
        report['ordinary_object_clearance'] = check_ordinary_placement(config)
        report['status'] = 'PASS'
    except (OSError, ValueError, KeyError, IndexError, AssertionError, StopIteration) as error:
        report['error'] = str(error) or type(error).__name__
    (HERE/'validation_report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(f"{report['status']}: {report.get('error', 'Native Blender model, material, integration, local house clearance and protected landmarks verified.')}")
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
