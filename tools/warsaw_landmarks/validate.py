# IMPERIA CW — Cold War: warsaw landmarks — validate.
"""Read-only validation of the Warsaw landmark, placement and local city changes.

Only validation_report.json is written. No source, game asset, mask, history,
or Blender manifest is repaired or changed by this validator.
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
BERLIN = ROOT/'tools/berlin_landmarks'
OUT = ROOT/'gfx/models/buildings/landmarks'
sys.path.insert(0, str(BERLIN))
import validate_blender as native
from pdx import meshes, read
from city_style import STYLES, ambient_objects, blocks

native.TEXTURES = {
    'diff': 'mdcw_warsaw_palace_diffuse.dds',
    'n': 'mdcw_warsaw_palace_normal.dds',
    'spec': 'mdcw_warsaw_palace_specular.dds',
}
require = native.require
MODELS = ['landmark_warsaw_palace.mesh', 'landmark_warsaw_palace_destroyed.mesh']
PREVIOUS_VERTICES = 33545
PREVIOUS_TRIANGLES = 16144


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_text(path):
    return path.read_text(encoding='utf-8-sig')


def named_block(text, key):
    found = list(blocks(text, r'^\s*'+re.escape(key)+r'\s*=\s*\{'))
    require(len(found) == 1, f'Expected exactly one {key} block, found {len(found)}')
    return found[0][2]


def entity_block(text, name):
    found = [block for _, _, block in blocks(text, r'^\s*entity\s*=\s*\{')
             if re.search(r'\bname\s*=\s*"'+re.escape(name)+r'"', block)]
    require(len(found) == 1, f'Expected exactly one entity {name}')
    return found[0]


def check_sources(config):
    manifest = json.loads(read_text(HERE/'blender_export.json'))
    require(bool(manifest.get('blender_version')), 'Blender version missing from export manifest')
    require('io_pdx_mesh' in manifest.get('exporter', ''), 'Native Blender exporter identity missing')
    path = HERE/manifest['source']
    require(path.resolve().parent == (HERE/'source').resolve(), 'Blender source path escapes source folder')
    source = path.read_bytes()
    require(source.startswith(b'BLENDER') and len(source) > 12, 'Invalid or compressed Blender source header')
    require((path.name, sha(source)) in list(native.source_hash_records(manifest)),
            'Blender source hash missing or stale in export manifest')
    for name in MODELS:
        require(manifest['mesh_sha256'].get(name) == sha((OUT/name).read_bytes()),
                f'{name}: native export manifest hash is stale')
    require(np.isclose(manifest['height'], config['original_height'], atol=.001), 'Manifest height differs from config')
    require(np.isclose(manifest['scale'], config['scale'], atol=1e-9), 'Manifest scale differs from config')
    require(np.isclose(manifest['display_height'], config['original_height']*config['scale'], atol=.001),
            'Manifest display height differs from configured geometry and scale')
    return {'blender_version': manifest['blender_version'], 'exporter': manifest['exporter'],
            'source': str(path.relative_to(ROOT)), 'source_sha256': sha(source),
            'source_bytes': len(source), 'exported_mesh_hashes_current': True}


def check_atlas(path, slot):
    """Validate compression and every mip's storage, not just the decoded top."""
    data = path.read_bytes()
    require(len(data) >= 128 and data[:4] == b'DDS ', f'{slot}: invalid DDS header')
    require(struct.unpack_from('<I', data, 4)[0] == 124, f'{slot}: invalid DDS header size')
    flags, height, width = struct.unpack_from('<III', data, 8)
    mip_count = struct.unpack_from('<I', data, 28)[0]
    pf_size, pf_flags = struct.unpack_from('<II', data, 76)
    fourcc = data[84:88]
    expected_codec = b'DXT1' if slot == 'diff' else b'DXT5'
    require((width, height) == (1024, 1024), f'{slot}: incorrect atlas dimensions')
    require(pf_size == 32 and pf_flags & 4, f'{slot}: DDS is not FourCC block compressed')
    require(fourcc == expected_codec, f'{slot}: expected {expected_codec.decode()} compression')
    require(flags & 0x20000 and mip_count == 11, f'{slot}: missing complete 11-level mip chain')
    caps = struct.unpack_from('<I', data, 108)[0]
    require(caps & 0x400008 == 0x400008, f'{slot}: mipmap/complex DDS caps missing')
    block_bytes = 8 if fourcc == b'DXT1' else 16
    levels = []
    offset = 128
    for level in range(mip_count):
        w, h = max(1, width >> level), max(1, height >> level)
        size = max(1, (w+3)//4)*max(1, (h+3)//4)*block_bytes
        require(offset+size <= len(data), f'{slot}: mip {level} payload is truncated')
        levels.append({'level': level, 'size': [w, h], 'offset': offset, 'bytes': size})
        offset += size
    require(offset == len(data), f'{slot}: DDS payload size differs from its complete mip chain')
    require(struct.unpack_from('<I', data, 20)[0] == levels[0]['bytes'],
            f'{slot}: compressed top-level linear size is incorrect')
    with Image.open(path) as image:
        require(image.size == (width, height), f'{slot}: decoder/header dimensions disagree')
        mode = image.mode
        image.verify()
    return {'size': [width, height], 'mode': mode, 'sha256': sha(data),
            'compression': 'BC1' if fourcc == b'DXT1' else 'BC3',
            'mip_count': mip_count, 'mip_levels': levels,
            'payload_bytes': len(data)-128, 'file_bytes': len(data)}


def check_models(config):
    geometry = {}
    report = {}
    attributes = {}
    for name in MODELS:
        p, record = native.check_mesh(OUT/name, 'mdcw_warsaw_palace')
        require(record['triangles'] < 8000, f'{name}: triangle count exceeds the performance budget')
        require(record['vertices'] < 16000, f'{name}: exported vertex count exceeds the performance budget')
        record['performance'] = {
            'joined_shapes': 1, 'materials': 1,
            'triangle_limit_exclusive': 8000, 'vertex_limit_exclusive': 16000,
            'previous_triangles': PREVIOUS_TRIANGLES, 'previous_vertices': PREVIOUS_VERTICES,
            'triangle_reduction_percent': 100*(1-record['triangles']/PREVIOUS_TRIANGLES),
            'vertex_reduction_percent': 100*(1-record['vertices']/PREVIOUS_VERTICES),
        }
        mesh = next(meshes(read(OUT/name)))[1]
        uv = mesh.prop('u0').value.reshape(-1, 2)
        normals = mesh.prop('n').value.reshape(-1, 3)
        tangents = mesh.prop('ta').value.reshape(-1, 4)
        require(((uv >= 0) & (uv <= 1)).all(), f'{name}: UVs outside the native atlas')
        require(np.abs(np.einsum('ij,ij->i', normals, tangents[:, :3])).max() <= .015,
                f'{name}: tangents are not perpendicular to the normals')
        require(np.isclose(p[:, 1].min(), 0, atol=.001), f'{name}: ground plane is not at zero')
        require(np.isclose(p[:, 1].max(), config['original_height'], atol=.001),
                f'{name}: height differs from the original 230.68 metre silhouette')
        require(180 < np.ptp(p[:, 0]) < 240 and 240 < np.ptp(p[:, 2]) < 280,
                f'{name}: palace footprint proportions or orientation are unexpected')
        geometry[name] = p
        attributes[name] = {key: mesh.prop(key).value for key in ['p', 'tri', 'n', 'u0', 'ta']}
        record['uv_range'] = [float(uv.min()), float(uv.max())]
        record['maximum_normal_tangent_dot'] = float(np.abs(np.einsum('ij,ij->i', normals, tangents[:, :3])).max())
        report[name] = record
    a, b = [attributes[name] for name in MODELS]
    for key in ['p', 'tri', 'n', 'u0']:
        require(np.array_equal(a[key], b[key]), f'Destroyed fallback differs in {key} geometry')
    # The native exporter recalculates the same tangent basis independently.
    require(np.allclose(a['ta'], b['ta'], rtol=0, atol=2e-6), 'Destroyed fallback tangent basis differs')
    normal = np.asarray(Image.open(OUT/native.TEXTURES['n']).convert('RGBA'))
    require(int(normal[:, :, 2].max()) <= 18, 'Normal map has unintended strong building emission')
    for slot, name in native.TEXTURES.items():
        report[name] = check_atlas(OUT/name, slot)
    report['destroyed_fallback_geometry_identical'] = True
    return geometry[MODELS[0]], report


def check_integration(points, config):
    require(config['state'] == 114 and config['province'] == 3544, 'Unexpected Warsaw state or province')
    require(config['opening_date'] == '1955.7.22', 'Unexpected palace opening date')
    require(np.isclose(config['scale'], .014, atol=1e-9), 'Unexpected palace map scale')
    require(np.allclose(config['anchor'], [3131.5, 9.8, 1563.5], atol=1e-6), 'Unexpected palace anchor')
    common = read_text(ROOT/'common/buildings/mdcw_warsaw_landmarks.txt')
    building = named_block(common, 'landmark_warsaw_palace')
    require(re.search(r'\bspawn_point\s*=\s*warsaw_palace_spawn\b', building), 'Building does not use its independent Warsaw spawn')
    require(re.search(r'\bis_buildable\s*=\s*no\b', building), 'Historical landmark should not be normally buildable')
    require(re.search(r'\bshow_modifier\s*=\s*yes\b', building), 'Palace effects are not shown in the building tooltip')
    country_modifiers = named_block(building, 'country_modifiers')
    modifiers = named_block(country_modifiers, 'modifiers')
    effects = {'education_cost_multiplier_modifier': -.03, 'research_speed_factor': .02}
    for key, expected in effects.items():
        values = re.findall(r'\b'+re.escape(key)+r'\s*=\s*([-+\d.]+)', modifiers)
        require(len(values) == 1 and np.isclose(float(values[0]), expected, atol=1e-9),
                f'Palace country modifier {key} differs from {expected}')
    spawn = named_block(common, 'warsaw_palace_spawn')
    require(re.search(r'\btype\s*=\s*province\b', spawn), 'Palace spawn is not province scoped')
    require(re.search(r'\bmax\s*=\s*1\b', spawn), 'Palace spawn must have max 1')
    require(re.search(r'\bdisable_auto_nudging\s*=\s*yes\b', spawn), 'Palace anchor is not protected from automatic nudging')
    asset = read_text(ROOT/'gfx/entities/mdcw_warsaw_landmarks.asset')
    for suffix in ['', '_destroyed']:
        entity = entity_block(asset, 'building_landmark_warsaw_palace'+suffix)
        require(re.search(r'\bpdxmesh\s*=\s*"mdcw_warsaw_palace'+suffix+r'_mesh"', entity),
                f'Palace{suffix} entity references the wrong pdxmesh')
        scales = re.findall(r'\bscale\s*=\s*([\d.]+)', entity)
        require(len(scales) == 1 and np.isclose(float(scales[0]), config['scale'], atol=1e-9),
                f'Palace{suffix} entity scale differs from config')
    alias = entity_block(asset, 'building_warsaw_palace_spawn')
    require(re.search(r'\bclone\s*=\s*"building_landmark_spawn"', alias), 'Palace spawn placeholder alias missing')
    gfx = read_text(ROOT/'gfx/entities/mdcw_warsaw_landmarks.gfx')
    for suffix in ['', '_destroyed']:
        candidates = [block for _, _, block in blocks(gfx, r'^\s*pdxmesh\s*=\s*\{')
                      if re.search(r'\bname\s*=\s*"mdcw_warsaw_palace'+suffix+r'_mesh"', block)]
        require(len(candidates) == 1, f'Missing unique palace{suffix} pdxmesh definition')
        definition = candidates[0]
        require('gfx/models/buildings/landmarks/landmark_warsaw_palace'+suffix+'.mesh' in definition,
                f'Palace{suffix} pdxmesh references the wrong native file')
        for name in native.TEXTURES.values():
            require(name in definition, f'Palace{suffix} gfx definition misses atlas {name}')
        require(re.search(r'\bshader\s*=\s*"PdxMeshAdvancedSnow"', definition), 'Palace shader must support snow')
    map_rows = re.findall(r'^114;warsaw_palace_spawn;([^;]+);([^;]+);([^;]+);([^;]+);',
                          read_text(ROOT/'map/buildings.txt'), re.M)
    require(len(map_rows) == 1, 'Palace needs exactly one independent map spawn row')
    row = list(map(float, map_rows[0]))
    require(np.allclose(row[:3], config['anchor'], atol=1e-6), 'Map row anchor differs from config')
    require(np.isclose(row[3], 0, atol=1e-8), 'Palace map row has unexpected rotation')
    state = read_text(ROOT/'history/states/114-Masovia.txt')
    opening = named_block(state, config['opening_date'])
    history_buildings = named_block(opening, 'buildings')
    province = named_block(history_buildings, '3544')
    require(re.search(r'\blandmark_warsaw_palace\s*=\s*1\b', province), 'Palace is not added at Warsaw in July 1955')
    provinces = np.asarray(Image.open(ROOT/'map/provinces.bmp').convert('RGB'))
    scale = config['scale']
    world = points[:, [0, 2]]*scale+np.asarray(config['anchor'])[[0, 2]]
    xs = np.floor(world[:, 0]).astype(int)
    ys = np.floor(provinces.shape[0]-world[:, 1]).astype(int)
    require(((xs >= 0) & (xs < provinces.shape[1]) & (ys >= 0) & (ys < provinces.shape[0])).all(), 'Palace footprint leaves bitmap')
    require((provinces[ys, xs] == [44, 159, 148]).all(), 'Palace footprint extends outside Warsaw province 3544')
    return {'anchor': row[:3], 'rotation': row[3], 'scale': scale,
            'display_height': float(points[:, 1].max()*scale), 'opening_date': config['opening_date'],
            'province': 3544, 'projected_footprint_within_province': True,
            'country_modifiers': effects, 'show_modifier': True,
            'world_bounds_xz': [world.min(axis=0).tolist(), world.max(axis=0).tolist()]}


def check_city_style():
    report = json.loads(read_text(HERE/'city_style_report.json'))
    raw = (ROOT/'map/cities.bmp').read_bytes()
    require(sha(raw) == report['cities_bmp_after_sha256'], 'Current city BMP differs from validated Warsaw patch')
    offset = struct.unpack_from('<I', raw, 10)[0]
    width, height = struct.unpack_from('<ii', raw, 18)
    require(struct.unpack_from('<HI', raw, 28) == (8, 0), 'City BMP is not uncompressed indexed 8-bit data')
    stride = (width+3)//4*4
    require(sha(raw[:offset]) == report['bmp_header_palette_sha256'], 'City BMP header or palette changed')
    reconstructed = bytearray(raw)
    edits = report['warsaw_pixel_edits']
    provinces = np.asarray(Image.open(ROOT/'map/provinces.bmp'))
    mask = np.all(provinces == [44, 159, 148], axis=2)
    require(len(edits) == int(mask.sum()) == 104, 'Warsaw pixel patch does not cover exactly province 3544')
    positions = set()
    for item in edits:
        x, y = item['x'], item['y']
        require(mask[y, x], 'City patch includes a pixel outside Warsaw province')
        positions.add((x, y))
        at = offset+(height-1-y)*stride+x
        require(raw[at] == item['new_index'], f'Warsaw city pixel {x}/{y} differs from audit report')
        reconstructed[at] = item['old_index']
    require(len(positions) == 104, 'Warsaw pixel patch contains duplicates')
    require(sha(reconstructed) == report['cities_bmp_before_sha256'],
            'Reversing only Warsaw edits does not recreate the original city BMP: unrelated pixels changed')
    berlin_report = json.loads(read_text(BERLIN/'city_clearance_report.json'))
    require(sha(reconstructed) == berlin_report['after_sha256'], 'Berlin city mask changed before Warsaw patch')
    berlin_backup = (BERLIN/berlin_report['backup']).read_bytes()
    # That report's before_sha256 describes a clearance run, whereas its runtime
    # backup predates every clearance run. Reapplying the approved 58 edits is
    # the exact byte-level proof that this older backup is the right baseline.
    require(len(berlin_backup) == len(raw) and berlin_backup[:offset] == raw[:offset],
            'Berlin runtime city backup dimensions, header or palette mismatch')
    expected_before_warsaw = bytearray(berlin_backup)
    for item in berlin_report['changes']:
        at = offset+(height-1-item['y'])*stride+item['x']
        expected_before_warsaw[at] = item['to']
    require(expected_before_warsaw == reconstructed, 'Warsaw original mask does not match Berlin runtime backup plus its approved 58 edits')
    groups = list(blocks(read_text(ROOT/'map/cities.txt'), r'^\s*city_group\s*=\s*\{'))
    groups_by_index = {}
    for _, _, group in groups:
        index = int(re.search(r'color_index\s*=\s*(\d+)', group).group(1))
        require(index not in groups_by_index, f'Duplicate city style group {index}')
        groups_by_index[index] = group
    require(3 not in groups_by_index and 4 in groups_by_index, 'Warsaw style or house-free plaza assignment is wrong')
    require(re.search(r'\bdensity\s*=\s*0\.9\b', groups_by_index[4]), 'Warsaw city density changed')
    asset = read_text(ROOT/'gfx/entities/mdcw_warsaw_city_style.asset')
    definitions = read_text(ROOT/'gfx/entities/buildings.gfx')+'\n'+read_text(ROOT/'gfx/entities/mapitems.gfx')
    for name, (filename, combined_scale) in STYLES.items():
        require('"'+name+'"' in groups_by_index[4], f'Warsaw city group misses house alias {name}')
        entity = entity_block(asset, name)
        pdxmesh = re.search(r'\bpdxmesh\s*=\s*"([^"]+)"', entity).group(1)
        entity_scale = float(re.search(r'\bscale\s*=\s*([\d.]+)', entity).group(1))
        pdx = [block for _, _, block in blocks(definitions, r'^\s*pdxmesh\s*=\s*\{')
               if re.search(r'\bname\s*=\s*"'+re.escape(pdxmesh)+'"', block)]
        require(len(pdx) == 1, f'City alias {name} has missing or ambiguous native pdxmesh')
        require('gfx/models/buildings/'+filename in pdx[0], f'City alias {name} references the wrong house model')
        scale_match = re.search(r'\bscale\s*=\s*([\d.]+)', pdx[0])
        native_scale = float(scale_match[1]) if scale_match else 1.
        require(np.isclose(entity_scale*native_scale, combined_scale, atol=1e-8), f'City alias {name} has changed map scale')
        p = np.concatenate([mesh.prop('p').value.reshape(-1, 3)
                            for _, mesh in meshes(read(ROOT/'gfx/models/buildings'/filename))])*combined_scale
        require(p[:, 1].max() <= .60, f'City alias {name} is too tall for the approved Warsaw style')
    ambient_bytes = (ROOT/'map/ambient_object.txt').read_bytes()
    require(sha(ambient_bytes) == report['ambient_after_sha256'], 'Ambient source differs from the scoped Warsaw mutation audit')
    objects = ambient_objects(ambient_bytes.decode('utf-8'))
    historic = []
    modern = []
    for kind, (x, y, z), _, _, _ in objects:
        px, py = math.floor(x), math.floor(height-z)
        if 0 <= px < width and 0 <= py < height and mask[py, px]:
            if kind.startswith('skyscraper'):
                modern.append((kind, x, z))
            if kind in {'cityblock_entity', 'cityblock2_entity'}:
                historic.append((kind, x, z))
    require(not modern, 'Modern ambient skyscrapers remain in Warsaw')
    require(len(historic) == 4, 'The four historical Warsaw perimeter blocks were not retained')
    moved = report['moved_historic_block']
    require(any(kind == moved['type'] and np.allclose([x, z], np.asarray(moved['new_position'])[[0, 2]], atol=.001)
                for kind, x, z in historic), 'Palace entrance block was not moved clear of the plaza')
    require(len(report['removed_modern_instances']) == 11, 'Scoped tower-removal audit does not contain 11 objects')
    return {'house_pixels': report['house_pixels'], 'plaza_pixels': report['palace_clearance_pixels'],
            'all_non_Warsaw_pixels_and_header_palette_unchanged': True,
            'Berlin_mask_matches_runtime_backup_plus_58_approved_edits': True,
            'Berlin_runtime_backup_sha256': sha(berlin_backup),
            'modern_ambient_instances_removed': 11, 'modern_ambient_instances_remaining': 0,
            'historical_ambient_blocks_retained': len(historic),
            'ambient_hash_matches_original_scoped_mutation_audit': True,
            'ambient_scope_evidence': 'city_style.py audited every unrelated source block during mutation; no pre-edit ambient backup exists'}


def check_berlin_preserved():
    manifest = json.loads(read_text(BERLIN/'blender_export.json'))
    source_result = {}
    for entry in manifest['sources']:
        path = BERLIN/entry['path']
        require(sha(path.read_bytes()) == entry['sha256'], f'Berlin source changed: {path.name}')
        source_result[path.name] = entry['sha256']
    for name, digest in manifest['exported_files'].items():
        require(sha((OUT/name).read_bytes()) == digest, f'Berlin native landmark changed: {name}')
    report = json.loads(read_text(BERLIN/'city_clearance_report.json'))
    for name, digest in report['approved_assets_unchanged'].items():
        path = ROOT/name
        if path == ROOT/'map/buildings.txt':
            continue  # The independent Warsaw spawn is intentionally added here.
        require(sha(path.read_bytes()) == digest, f'Previously approved Berlin asset or map changed: {name}')
    return {'native_meshes_match_manifest': True, 'Blender_sources_match_manifest': source_result,
            'Berlin_textures_entities_provinces_terrain_match_previous_hashes': True}


def main():
    report = {'status': 'FAIL', 'validator': 'validate.py', 'scope': 'Read-only; only this report is written'}
    try:
        config = json.loads(read_text(HERE/'config.json'))
        report['sources'] = check_sources(config)
        points, report['native_models'] = check_models(config)
        report['city_style'] = check_city_style()
        report['Berlin_preservation'] = check_berlin_preserved()
        report['integration'] = check_integration(points, config)
        report['status'] = 'PASS'
    except (ValueError, AssertionError, OSError, KeyError, IndexError, StopIteration) as error:
        report['error'] = str(error) or type(error).__name__
    (HERE/'validation_report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(f"{report['status']}: {report.get('error', 'Native meshes, Blender sources, materials, placement, city style and unchanged Berlin verified.')}")
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
