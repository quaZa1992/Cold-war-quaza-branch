# IMPERIA CW — Cold War: jerusalem landmarks — validate.
"""Read-only validation of the Western Wall's Blender export and integration.

Only validation_report.json is written. Geometry, source files, history and
map assets are never repaired. Native mesh round trips, render attributes,
full DDS mip payloads and scoped placement evidence are checked independently.
"""
from pathlib import Path
import hashlib
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

BUILDING = 'landmark_jerusalem_western_wall'
SPAWN = 'western_wall_spawn'
MESH = 'mdcw_jerusalem_western_wall'
MODELS = [BUILDING+'.mesh', BUILDING+'_destroyed.mesh']
TEXTURES = {slot: MESH+'_'+suffix+'.dds'
            for slot, suffix in [('diff', 'diffuse'), ('n', 'normal'), ('spec', 'specular')]}
native.TEXTURES = TEXTURES.copy()
require = native.require


def sha(data):
    return hashlib.sha256(data).hexdigest()


def text(path):
    return path.read_text(encoding='utf-8-sig')


def code_mask(source):
    """Keep offsets and line boundaries while masking strings and comments."""
    return re.sub(r'"(?:\\.|[^"\\])*"|#[^\r\n]*',
                  lambda match: ''.join('\n' if c == '\n' else ' ' for c in match[0]), source)


def blocks(source, pattern):
    mask = code_mask(source)
    for found in re.finditer(pattern, mask, re.M):
        start = mask.index('{', found.start(), found.end())
        depth, end = 1, start+1
        while end < len(mask) and depth:
            depth += (mask[end] == '{')-(mask[end] == '}')
            end += 1
        require(depth == 0, 'Unclosed PDX block')
        yield source[found.start():end]


def named_block(source, key):
    found = list(blocks(source, r'^\s*'+re.escape(str(key))+r'\s*=\s*\{'))
    require(len(found) == 1, f'Expected exactly one {key} block, found {len(found)}')
    return found[0]


def named_entity(source, name, kind='entity'):
    found = [value for value in blocks(source, r'^\s*'+kind+r'\s*=\s*\{')
             if re.search(r'\bname\s*=\s*"'+re.escape(name)+'"', value)]
    require(len(found) == 1, f'Expected exactly one {kind} {name}')
    return found[0]


def balanced(source, name):
    depth = 0
    for c in code_mask(source):
        depth += (c == '{')-(c == '}')
        require(depth >= 0, f'{name}: unexpected closing brace')
    require(depth == 0, f'{name}: unclosed braces')


def check_sources(config):
    manifest = json.loads(text(HERE/'blender_export.json'))
    require(bool(manifest.get('blender_version')), 'Missing Blender version')
    require('io_pdx_mesh' in manifest.get('exporter', ''), 'Missing native exporter identity')
    source = HERE/manifest['source']
    require(source.resolve().parent == (HERE/'source').resolve() and source.suffix == '.blend',
            'Unexpected Blender source location')
    raw = source.read_bytes()
    require(raw.startswith(b'BLENDER') and len(raw) > 12, 'Invalid or compressed Blender source')
    require((source.name, sha(raw)) in list(native.source_hash_records(manifest)), 'Stale Blender source hash')
    for filename in MODELS:
        require(manifest['mesh_sha256'].get(filename) == sha((OUT/filename).read_bytes()),
                f'Stale native export hash: {filename}')
    require(np.isclose(manifest['height'], config['original_height'], atol=.001), 'Source height differs')
    require(np.isclose(manifest['scale'], config['scale'], atol=1e-9), 'Source map scale differs')
    require(np.isclose(manifest['display_height'], config['original_height']*config['scale'], atol=.001),
            'Source display height differs')
    return {'blender_version': manifest['blender_version'], 'exporter': manifest['exporter'],
            'source': str(source.relative_to(ROOT)), 'source_sha256': sha(raw), 'source_bytes': len(raw)}, manifest


def check_atlas(path, slot):
    data = path.read_bytes()
    require(len(data) >= 128 and data[:4] == b'DDS ', f'{slot}: invalid DDS header')
    require(struct.unpack_from('<I', data, 4)[0] == 124, f'{slot}: invalid DDS header size')
    flags, height, width = struct.unpack_from('<III', data, 8)
    mips = struct.unpack_from('<I', data, 28)[0]
    pf_size, pf_flags = struct.unpack_from('<II', data, 76)
    fourcc = data[84:88]
    require((width, height) == (1024, 1024), f'{slot}: atlas must be 1024 square')
    require(pf_size == 32 and pf_flags & 4, f'{slot}: DDS must be block compressed')
    require(fourcc == (b'DXT1' if slot == 'diff' else b'DXT5'), f'{slot}: wrong block compression')
    require(flags & 0x20000 and mips == 11, f'{slot}: complete mip chain missing')
    require(struct.unpack_from('<I', data, 108)[0] & 0x400008 == 0x400008,
            f'{slot}: mipmap/complex DDS flags missing')
    offset, levels = 128, []
    for level in range(mips):
        w, h = max(1, width >> level), max(1, height >> level)
        size = max(1, (w+3)//4)*max(1, (h+3)//4)*(8 if fourcc == b'DXT1' else 16)
        require(offset+size <= len(data), f'{slot}: mip {level} is truncated')
        levels.append({'level': level, 'size': [w, h], 'offset': offset, 'bytes': size})
        offset += size
    require(offset == len(data), f'{slot}: DDS size differs from mip payload')
    require(struct.unpack_from('<I', data, 20)[0] == levels[0]['bytes'], f'{slot}: incorrect linear size')
    with Image.open(path) as image:
        require(image.size == (1024, 1024), f'{slot}: decoder dimensions differ')
        image.verify()
    return {'size': [width, height], 'compression': fourcc.decode(), 'mips': mips,
            'levels': levels, 'file_bytes': len(data), 'sha256': sha(data)}


def check_models(config, manifest):
    result, attrs, geometry = {}, [], []
    for filename in MODELS:
        points, record = native.check_mesh(OUT/filename, BUILDING)
        require(record['triangles'] < 7000, f'{filename}: triangle budget exceeded')
        require(record['vertices'] < 16000, f'{filename}: vertex budget exceeded')
        node = next(meshes(read(OUT/filename)))[1]
        attr = {key: node.prop(key).value for key in ('p', 'tri', 'n', 'u0', 'ta')}
        triangle = points[attr['tri'].reshape(-1, 3)]
        extent = np.ptp(triangle, axis=1)
        floor_panel = ((triangle[:, :, 0].min(axis=1) < -8.5)
                       & (extent[:, 0] > 3) & (extent[:, 2] > 3) & (extent[:, 1] < 3))
        require(not floor_panel.any(), f'{filename}: removed forecourt paving is still exported')
        uv, normal, tangent = attr['u0'].reshape(-1, 2), attr['n'].reshape(-1, 3), attr['ta'].reshape(-1, 4)
        require(((uv >= 0) & (uv <= 1)).all(), f'{filename}: UVs leave atlas')
        dot = float(np.abs(np.einsum('ij,ij->i', normal, tangent[:, :3])).max())
        require(dot <= .015, f'{filename}: tangent basis is not orthogonal')
        require(np.isclose(points[:, 1].max(), config['original_height'], atol=.001),
                f'{filename}: unexpected architectural height')
        require(np.isclose(points[:, 1].min(), -config['foundation_depth'], atol=.001),
                f'{filename}: buried footings differ')
        bounds = np.asarray(config['footprint_source'])
        require((points[:, 0] >= bounds[0]-.001).all() and (points[:, 0] <= bounds[1]+.001).all()
                and (points[:, 2] >= bounds[2]-.001).all() and (points[:, 2] <= bounds[3]+.001).all(),
                f'{filename}: geometry exceeds clearance envelope')
        record.update({'materials': 1, 'maximum_normal_tangent_dot': dot,
                       'triangle_limit_exclusive': 7000, 'vertex_limit_exclusive': 16000,
                       'forecourt_ground_surface_removed': True})
        result[filename], attrs = record, attrs+[attr]
        geometry.append(points)
    for key in ('p', 'tri', 'n', 'u0'):
        require(np.array_equal(attrs[0][key], attrs[1][key]), f'Destroyed fallback differs in {key}')
    require(np.allclose(attrs[0]['ta'], attrs[1]['ta'], rtol=0, atol=2e-6), 'Fallback tangent basis differs')
    for slot, filename in TEXTURES.items():
        result[filename] = check_atlas(OUT/filename, slot)
    normal_map = np.asarray(Image.open(OUT/TEXTURES['n']).convert('RGBA'))
    require(normal_map[:, :, 2].max() <= 18, 'Normal map has unwanted emissive lighting')
    properties = np.asarray(Image.open(OUT/TEXTURES['spec']).convert('RGBA'))
    require(properties[:, :, 3].max() <= 60, 'Limestone glossiness is too high for the native shader')
    performance = manifest.get('performance', {})
    actual = result[MODELS[0]]
    for key in ('triangles', 'vertices', 'materials'):
        require(performance.get(key) == actual[key], f'Stale performance manifest: {key}')
    require(performance.get('atlas_size') == 1024 and performance.get('mip_levels') == 11,
            'Stale texture performance manifest')
    result['destroyed_fallback_geometry_identical'] = True
    return geometry[0], result


def world_xz(points, config):
    angle = config.get('rotation', 0)
    rotation = np.asarray([[math.cos(angle), math.sin(angle)], [-math.sin(angle), math.cos(angle)]])
    return points@rotation.T*config['scale']+np.asarray(config['anchor'])[[0, 2]]


def check_integration(points, config):
    require(config['state'] == 207 and config['province'] == 1086, 'Unexpected Jerusalem province/state')
    require(np.isclose(config['scale'], .025, atol=1e-9), 'Unexpected wall display scale')
    common = text(ROOT/'common/buildings/mdcw_jerusalem_landmarks.txt')
    building = named_block(common, BUILDING)
    require(re.search(r'\bspawn_point\s*=\s*'+SPAWN+r'\b', building), 'Independent wall spawn missing')
    require(re.search(r'\bis_buildable\s*=\s*no\b', building), 'Landmark should not be buildable')
    require(re.search(r'\bshow_modifier\s*=\s*yes\b', building), 'Bonuses are hidden in tooltip')
    country = named_block(building, 'country_modifiers')
    require('enable_for_controllers' not in country, 'Unexpected country restriction on requested bonuses')
    modifiers = named_block(country, 'modifiers')
    effects = dict((k, float(v)) for k, v in re.findall(r'^\s*(\w+)\s*=\s*([-.\d]+)\s*$', modifiers, re.M))
    require(effects == {'stability_factor': .02, 'monthly_population': .02}, 'Requested native bonuses differ')
    spawn = named_block(common, SPAWN)
    for pattern in (r'\btype\s*=\s*province\b', r'\bmax\s*=\s*1\b', r'\bdisable_auto_nudging\s*=\s*yes\b'):
        require(re.search(pattern, spawn), 'Spawn needs province/max1/protected-position settings')
    asset = text(ROOT/'gfx/entities/mdcw_jerusalem_landmarks.asset')
    gfx = text(ROOT/'gfx/entities/mdcw_jerusalem_landmarks.gfx')
    icon_gfx = text(ROOT/'interface/mdcw_jerusalem_landmarks.gfx')
    for label, source in [('building', common), ('entities', asset), ('meshes', gfx), ('icons', icon_gfx)]:
        balanced(source, label)
    for suffix in ('', '_destroyed'):
        entity = named_entity(asset, 'building_'+BUILDING+suffix)
        require(re.search(r'\bpdxmesh\s*=\s*"'+MESH+suffix+'_mesh"', entity), 'Wrong entity mesh reference')
        scales = re.findall(r'\bscale\s*=\s*([\d.]+)', entity)
        require(len(scales) == 1 and np.isclose(float(scales[0]), config['scale']), 'Wrong entity scale')
        definition = named_entity(gfx, MESH+suffix+'_mesh', 'pdxmesh')
        require('gfx/models/buildings/landmarks/'+BUILDING+suffix+'.mesh' in definition, 'Wrong mesh file')
        setting = named_block(definition, 'meshsettings')
        require('name = "'+BUILDING+'"' in setting, 'Wrong exported shape override')
        require(all(filename in setting for filename in TEXTURES.values()), 'Atlas slot missing')
        require('PdxMeshAdvancedSnow' in setting, 'Snow shader missing')
    require('clone = "building_landmark_spawn"' in named_entity(asset, 'building_'+SPAWN), 'Spawn placeholder alias missing')
    rows = re.findall(r'^207;'+SPAWN+r';([^;]+);([^;]+);([^;]+);([^;]+);', text(ROOT/'map/buildings.txt'), re.M)
    require(len(rows) == 1, 'Expected exactly one Jerusalem wall map row')
    row = np.asarray(list(map(float, rows[0])))
    require(np.allclose(row[:3], config['anchor'], atol=1e-6)
            and np.isclose(row[3], config.get('rotation', 0)), 'Map placement differs from config')
    history_files = list((ROOT/'history/states').glob(str(config['state'])+'-*.txt'))
    require(len(history_files) == 1, 'State history missing or duplicated')
    dated = named_block(text(history_files[0]), config['opening_date'])
    province = named_block(named_block(dated, 'buildings'), config['province'])
    require(re.search(r'\b'+BUILDING+r'\s*=\s*1\b', province), 'Wall missing from scenario history')
    rgb_rows = [line.split(';') for line in text(ROOT/'map/definition.csv').splitlines()
                if line.startswith(str(config['province'])+';')]
    require(len(rgb_rows) == 1, 'Province definition missing or duplicated')
    rgb = np.asarray(list(map(int, rgb_rows[0][1:4])))
    province_map = np.asarray(Image.open(ROOT/'map/provinces.bmp').convert('RGB'))
    bound = config['footprint_source']
    xx, zz = np.meshgrid(np.linspace(bound[0], bound[1], 101), np.linspace(bound[2], bound[3], 101))
    samples = np.vstack((points[:, [0, 2]], np.c_[xx.ravel(), zz.ravel()]))
    world = world_xz(samples, config)
    px, py = np.floor(world[:, 0]).astype(int), np.floor(province_map.shape[0]-world[:, 1]).astype(int)
    require(((px >= 0) & (px < province_map.shape[1]) & (py >= 0) & (py < province_map.shape[0])).all(), 'Model leaves map')
    require(np.all(province_map[py, px] == rgb), 'Model envelope leaves Jerusalem province')
    special = re.search(r'\bspecial_icon\s*=\s*(\w+)', building)
    require(special and special[1] in icon_gfx, 'Building icon definition missing')
    for size, suffix in [('large', ''), ('small', '_small')]:
        sprite = named_entity(icon_gfx, 'GFX_western_wall_icon'+suffix, 'spriteType')
        require(re.search(r'\bnoOfFrames\s*=\s*2\b', sprite), 'Icon needs two frames')
        match = re.search(r'\btexturefile\s*=\s*"([^"]+)"', sprite)
        require(match is not None, 'Icon texture reference missing')
        path = ROOT/match[1]
        require('/'+size+'/' in match[1], 'Wrong icon size directory')
        with Image.open(path) as image:
            side = 64 if size == 'large' else 32
            require(image.size == (side*2, side), 'Icon dimensions differ')
            rgba = np.asarray(image.convert('RGBA'))
            for frame in range(2):
                alpha = rgba[:, frame*side:(frame+1)*side, 3]
                require(alpha.max() > 0 and alpha.min() == 0, 'Icon is empty or lacks transparent background')
    for language in ('english', 'german'):
        path = ROOT/'localisation'/language/f'mdcw_jerusalem_landmarks_l_{language}.yml'
        raw = path.read_bytes()
        require(raw.startswith(b'\xef\xbb\xbf'), f'{language}: missing UTF8 BOM')
        source = raw.decode('utf-8-sig')
        require(source.startswith('l_'+language+':'), f'{language}: wrong localization language')
        for key in (BUILDING, BUILDING+'_plural', BUILDING+'_desc'):
            require(len(re.findall(r'^\s*'+key+r':', source, re.M)) == 1, f'{language}: missing/duplicate {key}')
    native_docs = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV/documentation/modifiers_documentation.md')
    if native_docs.is_file():
        for key in effects:
            require('## '+key+'\n' in text(native_docs), f'{key}: missing native modifier documentation')
    return {'state': config['state'], 'province': config['province'], 'anchor': row[:3].tolist(),
            'rotation': row[3], 'scale': config['scale'], 'history_initialization': config['opening_date'],
            'native_vertices_and_conservative_envelope_inside_Jerusalem': True,
            'world_bounds_xz': [world.min(0).tolist(), world.max(0).tolist()], 'country_modifiers': effects,
            'monthly_population_semantics': 'Native +2% growth factor, additive with other growth modifiers; not 2% of total population per month.'}


def check_city_clearance(config):
    report = json.loads(text(HERE/'city_clearance_report.json'))
    require(report['status'] == 'PASS', 'City clearance report did not pass')
    current = (ROOT/'map/cities.bmp').read_bytes()
    require(sha(current) == report['after_sha256'], 'Current city mask differs from clearance report')
    require(current[:2] == b'BM', 'Invalid city BMP signature')
    offset = struct.unpack_from('<I', current, 10)[0]
    width, height = struct.unpack_from('<ii', current, 18)
    require(width > 0 and height > 0 and struct.unpack_from('<HI', current, 28) == (8, 0),
            'City mask is not bottom-up uncompressed indexed 8bit')
    stride = (width+3)//4*4
    require(len(current) >= offset+stride*height, 'Truncated city BMP')
    require(sha(current[:offset]) == report['unchanged_header_palette_sha256'], 'City BMP header/palette changed')
    source = np.asarray(config['footprint_source'])
    lower = world_xz(np.asarray([[source[0], source[2]]]), config)[0]
    upper = world_xz(np.asarray([[source[1], source[3]]]), config)[0]
    require(np.allclose(report['scope']['world_bounds_xz'], [lower, upper]), 'Clearance envelope differs from model')
    radius = report['scope']['house_maximum_horizontal_radius']
    jitter = report['scope']['pixel_half_diagonal']
    margin = report['scope']['additional_margin']
    require(radius >= 1.309591 and np.isclose(jitter, math.sqrt(.5)) and margin >= .08,
            'House clearance fails arbitrary rotation and pixel jitter allowance')
    clearance = radius+jitter+margin
    terrain = np.asarray(Image.open(ROOT/'map/terrain.bmp'))
    require(terrain.shape == (height, width), 'City/terrain dimensions differ')
    cells = set()
    for cy in range(max(0, int(math.floor(height-upper[1]-clearance))-1),
                    min(height, int(math.ceil(height-lower[1]+clearance))+1)):
        for cx in range(max(0, int(math.floor(lower[0]-clearance))-1),
                        min(width, int(math.ceil(upper[0]+clearance))+1)):
            point = np.asarray([cx+.5, height-cy-.5])
            distance = np.linalg.norm(np.maximum(np.maximum(lower-point, point-upper), 0))
            if distance <= clearance and terrain[cy, cx] == 13:
                cells.add((cx, cy))
    for cx, cy in cells:
        require(current[offset+(height-1-cy)*stride+cx] == 3, 'A decorative house may enter the wall site')
    changed = {(entry['x'], entry['y']) for entry in report['changes']}
    require(len(changed) == len(report['changes']) == report['changed_pixel_count'], 'Duplicate or incorrect edit count')
    require(changed <= cells, 'City patch includes a distant or nonurban cell')
    reconstructed = bytearray(current)
    for entry in report['changes']:
        require(entry['from'] == 15 and entry['to'] == 3, 'Unexpected city style replacement')
        at = offset+(height-1-entry['y'])*stride+entry['x']
        require(current[at] == entry['to'], 'Changed city cell was overwritten')
        reconstructed[at] = entry['from']
    require(sha(reconstructed) == report['baseline_before_sha256'], 'Unrelated city bytes changed')
    backup = HERE/report['backup']
    require(backup.resolve().parent == (HERE/'runtime').resolve(), 'Unexpected city backup location')
    if backup.exists():
        require(bytes(reconstructed) == backup.read_bytes(), 'Reversing wall clearance does not recreate original city mask')
    assigned = {int(value) for value in re.findall(r'color_index\s*=\s*(\d+)', text(ROOT/'map/cities.txt'))}
    require(15 in assigned and 3 not in assigned, 'Empty city index now spawns houses')
    for previous in report['approved_previous_city_cells_unchanged']:
        for cell in previous['cells']:
            at = offset+(height-1-cell['y'])*stride+cell['x']
            require(current[at] == cell['value'], f"Approved {previous['city']} city cell changed")
    require({item['city'] for item in report['approved_previous_city_cells_unchanged']}
            == {'berlin', 'warsaw', 'bucharest'}, 'Previous city mask snapshots missing')
    expected = set()
    for city in ('berlin', 'warsaw', 'bucharest'):
        expected.update(OUT.glob('landmark_'+city+'_*.mesh'))
        expected.update(OUT.glob('mdcw_'+city+'_*.dds'))
        expected.update((ROOT/'gfx/entities').glob('mdcw_'+city+'*'))
        expected.update((ROOT/f'tools/{city}_landmarks/source').glob('*.blend'))
    expected.update(OUT.glob('domeofrock*'))
    expected.update(ROOT/name for name in ('map/provinces.bmp', 'map/terrain.bmp', 'map/heightmap.bmp',
                                          'map/ambient_object.txt', 'map/cities.txt',
                                          'gfx/entities/landmarks.asset', 'gfx/entities/landmarks.gfx'))
    preserved = report['approved_assets_unchanged']
    require({str(path.relative_to(ROOT)) for path in expected} == set(preserved), 'Protected asset list is incomplete')
    for name, digest in preserved.items():
        require(sha((ROOT/name).read_bytes()) == digest, f'Previously approved asset changed: {name}')
    return {'selected_urban_pixels': len(cells), 'changed_urban_pixels': len(changed),
            'all_other_city_bytes_unchanged': True, 'header_palette_unchanged': True,
            'previous_Berlin_Warsaw_Bucharest_city_cells_unchanged': True,
            'previous_landmarks_and_Dome_of_the_Rock_preserved': True,
            'protected_asset_count': len(preserved)}


def check_scoped_placement(config):
    report = json.loads(text(HERE/'placement_report.json'))
    require(report['status'] == 'PASS', 'Placement report did not pass')
    current = (ROOT/'map/buildings.txt').read_bytes()
    require(sha(current) == report['map_buildings_after_sha256'], 'Map rows differ from placement report')
    newline = b'\r\n' if b'\r\n' in current else b'\n'
    row = report['spawn_row'].encode()
    require(current.count(row+newline) == 1, 'Independent wall row missing or duplicated')
    reconstructed = current.replace(row+newline, b'', 1)
    history = ROOT/report['history_path']
    history_raw = history.read_bytes()
    require(sha(history_raw) == report['history_after_sha256'], 'State history differs from placement report')
    history_newline = b'\r\n' if b'\r\n' in history_raw else b'\n'
    inserted = report['inserted_history_block'].encode().replace(b'\n', history_newline)
    require(history_raw.count(inserted) == 1, 'Dated landmark block missing or duplicated')
    reversed_history = history_raw.replace(inserted, b'', 1)
    history_backup = HERE/report['history_backup']
    require(history_backup.resolve().parent == (HERE/'runtime').resolve(), 'Unexpected history backup path')
    require(sha(reversed_history) == report['history_baseline_sha256'], 'Unrelated state history changed')
    if history_backup.exists():
        require(reversed_history == history_backup.read_bytes(), 'State history differs from local original backup')
    definition = next(line.split(';') for line in text(ROOT/'map/definition.csv').splitlines()
                      if line.startswith(str(config['province'])+';'))
    rgb = np.asarray(list(map(int, definition[1:4])))
    provinces = np.asarray(Image.open(ROOT/'map/provinces.bmp').convert('RGB'))
    envelope = np.asarray(config['footprint_source'])
    polygon = world_xz(np.asarray([[envelope[0], envelope[2]], [envelope[1], envelope[2]],
                                  [envelope[1], envelope[3]], [envelope[0], envelope[3]]]), config)
    wall = polygon[np.asarray([[0, 1, 2], [0, 2, 3]])]
    dome = report['dome']
    require(dome['changed'] is False and sha((ROOT/dome['path']).read_bytes()) == dome['sha256'],
            'Existing Dome model changed')
    dome_rows = re.findall(r'^207;landmark_spawn;([^;]+);([^;]+);([^;]+);([^;]+);', current.decode('utf-8-sig'), re.M)
    require(len(dome_rows) == 1, 'Existing Dome map spawn missing or duplicated')
    dome_row = np.asarray(list(map(float, dome_rows[0])))
    require(np.allclose(dome_row[:3], dome['anchor']) and np.isclose(dome_row[3], dome['rotation']),
            'Existing Dome position changed')
    cloud = np.concatenate([projected_mesh(dome['path'], dome['combined_scale'],
                                         np.asarray(dome['anchor'])[[0, 2]], dome['rotation']*sign)[1]
                            for sign in (1, -1)])
    dome_hull = convex_hull(cloud)
    require(np.allclose(dome_hull, dome['both_rotation_convex_footprint']), 'Dome clearance hull differs from native vertices')
    dome_triangles = dome_hull[np.asarray([[0, i, i+1] for i in range(1, len(dome_hull)-1)])]
    require(projected_overlap_count(wall, dome_triangles) == 0, 'Western Wall envelope intersects existing Dome')

    def geometry(row, model, require_inside, require_dome=True):
        fields = row.split(';')
        anchor = np.asarray(list(map(float, fields[2:5])))
        angle = float(fields[5])
        path = ROOT/model['path']
        require(sha(path.read_bytes()) == model['sha256'], f'Ordinary model changed: {model["path"]}')
        records = []
        for sign in (1, -1):
            triangle, vertex = projected_mesh(model['path'], model['combined_scale'], anchor[[0, 2]], angle*sign)
            wall_count = projected_overlap_count(wall, triangle)
            dome_count = projected_overlap_count(dome_triangles, triangle)
            require(wall_count == 0 and (dome_count == 0 or not require_dome),
                    'An ordinary visual model intersects a landmark')
            px, py = np.floor(vertex[:, 0]).astype(int), np.floor(provinces.shape[0]-vertex[:, 1]).astype(int)
            require(((px >= 0) & (px < provinces.shape[1]) & (py >= 0) & (py < provinces.shape[0])).all(), 'Ordinary model leaves map')
            inside = bool(np.all(provinces[py, px] == rgb))
            ax, ay = math.floor(anchor[0]), math.floor(provinces.shape[0]-anchor[2])
            require(np.array_equal(provinces[ay, ax], rgb), 'Ordinary visual anchor leaves province')
            require(inside or not require_inside, 'Relocated factory footprint leaves province')
            records.append({'rotation_sign': sign, 'wall_triangle_overlap_pairs': wall_count,
                            'Dome_convex_hull_triangle_overlap_pairs': dome_count,
                            'native_vertices_inside_Jerusalem': inside})
        return records

    records, seen = [], set()
    for edit in report['visual_spawn_edits']:
        old, new = edit['old_row'].encode(), edit['new_row'].encode()
        require(new not in seen and current.count(new) == 1 and current.count(old) == 0,
                'Relocated ordinary row missing or duplicated')
        seen.add(new)
        reconstructed = reconstructed.replace(new, old, 1)
        before, after = edit['old_row'].split(';'), edit['new_row'].split(';')
        require(all(before[i] == after[i] for i in (0, 1, 6)), 'Visual move changed ordinary state/type/metadata')
        require(before[1] in ('industrial_complex', 'arms_factory', 'air_base'), 'Unexpected ordinary spawn edit')
        require_inside = before[1] != 'air_base'
        if not require_inside:
            require(before[5] == after[5] and bool(report['airbase_footprint_exception']), 'Airbase rotation or exception differs')
        checks = geometry(edit['new_row'], edit['model'], require_inside)
        for evidence in edit['after']:
            require(evidence['wall_projected_triangle_overlaps'] == 0
                    and evidence['dome_convex_footprint_triangle_overlaps'] == 0,
                    'Placement collision evidence did not pass')
        records.append({'type': after[1], 'anchor': list(map(float, after[2:5])), 'geometry': checks})
    building_backup = HERE/report['buildings_backup']
    require(building_backup.resolve().parent == (HERE/'runtime').resolve(), 'Unexpected buildings backup path')
    require(sha(reconstructed) == report['map_buildings_baseline_sha256'], 'Unrelated map rows changed')
    if building_backup.exists():
        require(reconstructed == building_backup.read_bytes(), 'Map rows differ from local original backup')
    active = []
    for check in report['unchanged_active_visual_checks']:
        require(check['changed'] is False and current.count(check['row'].encode()) == 1, 'Unchanged active row differs')
        # Existing active meshes are not relocated; only landmark clearance is required.
        records_active = geometry(check['row'], check['model'], False, False)
        active.append({'row': check['row'], 'geometry': records_active})
    for filename, digest in report['gameplay_files_unchanged'].items():
        require(sha((ROOT/filename).read_bytes()) == digest, f'Gameplay asset changed: {filename}')
    require(set(report['gameplay_files_unchanged']) == {'map/supply_nodes.txt', 'map/railways.txt'}, 'Gameplay preservation evidence missing')
    for filename, digest in report['approved_assets_unchanged'].items():
        require(sha((ROOT/filename).read_bytes()) == digest, f'Protected placement asset changed: {filename}')
    return {'ordinary_visual_rows_adjusted': records, 'unchanged_active_visual_models': active,
            'all_other_map_building_bytes_unchanged': True, 'all_other_state_history_bytes_unchanged': True,
            'supply_nodes_and_railways_unchanged': True, 'Dome_source_and_spawn_unchanged': True,
            'airbase_footprint_exception': report['airbase_footprint_exception']}


def convex_hull(points):
    points = sorted(set(map(tuple, points)))
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
    return np.asarray(lower[:-1]+upper[:-1])


def projected_mesh(filename, scale, anchor, rotation=0):
    """Read the actual native architectural triangles in map coordinates."""
    path = Path(filename)
    if not path.is_absolute():
        path = ROOT/path
    rotate = np.asarray([[math.cos(rotation), math.sin(rotation)],
                         [-math.sin(rotation), math.cos(rotation)]])
    triangles, vertices = [], []
    for _, node in meshes(read(path)):
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
    require(bool(vertices), f'Native model has no vertices: {filename}')
    return np.concatenate(triangles), np.concatenate(vertices)


def projected_overlap_count(first, second):
    """Triangle SAT; touching footprints also count as architectural collisions."""
    total = 0
    lower, upper = second.min(axis=1), second.max(axis=1)
    for triangle in first:
        candidate = second[np.all(upper >= triangle.min(0), axis=1)
                           & np.all(lower <= triangle.max(0), axis=1)]
        if not len(candidate):
            continue
        edges_a = np.roll(triangle, -1, axis=0)-triangle
        edges_b = np.roll(candidate, -1, axis=1)-candidate
        axes = np.concatenate([np.tile(edges_a[None], (len(candidate), 1, 1)), edges_b], axis=1)
        axes = axes[:, :, [1, 0]]*np.asarray([-1, 1])
        projection_a = np.einsum('ij,nkj->nki', triangle, axes)
        projection_b = np.einsum('nij,nkj->nki', candidate, axes)
        separated = ((projection_a.max(2) < projection_b.min(2)-1e-9)
                     | (projection_b.max(2) < projection_a.min(2)-1e-9))
        total += int((~separated.any(axis=1)).sum())
    return total


def main():
    report = {'status': 'FAIL', 'scope': 'Read-only; only validation_report.json is written'}
    try:
        config = json.loads(text(HERE/'config.json'))
        report['Blender_source'], manifest = check_sources(config)
        points, report['native_models'] = check_models(config, manifest)
        report['integration'] = check_integration(points, config)
        report['city_clearance'] = check_city_clearance(config)
        report['scoped_placement'] = check_scoped_placement(config)
        report['status'] = 'PASS'
    except (OSError, ValueError, KeyError, IndexError, AssertionError, StopIteration) as error:
        report['error'] = str(error) or type(error).__name__
    (HERE/'validation_report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(f"{report['status']}: {report.get('error', 'Native Blender meshes, materials, effects, scenario integration and scoped placement verified.')}")
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
