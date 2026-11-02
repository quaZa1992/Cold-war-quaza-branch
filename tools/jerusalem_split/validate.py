# IMPERIA COLD WAR — Structural, geometry and preservation checks for Jerusalem.
"""Validate proposed outputs, or --live after installation. No runtime writes."""
from collections import Counter
from pathlib import Path
import argparse
import io
import json
import re
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import label, binary_dilation

from integrate import ROOT, OUT, TARGET, RGB, STATE, PROVINCE, build, git_blob, sha

sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'tools/spain_1970_v2'))
from script_ast import parse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--live', action='store_true')
    options = parser.parse_args()
    proposed = build()
    data = {k: (ROOT / k).read_bytes() if options.live else v for k, v in proposed.items()}
    report = {'project': 'IMPERIA COLD WAR', 'mode': 'installed' if options.live else 'proposed', 'checks': []}

    def passed(name, **details):
        report['checks'].append({'name': name, 'passed': True, **details})

    def read(relative):
        return data[relative] if relative in data else (ROOT / relative).read_bytes()

    def text(relative):
        return read(relative).decode('utf-8-sig')

    def rows(relative, prefix):
        return [r.split(';') for r in text(relative).splitlines() if r.startswith(str(prefix) + ';')]

    assert all(data[k] == v for k, v in proposed.items()), 'Installed generated outputs differ'
    for relative, blob in data.items():
        if relative.endswith('.bmp'):
            continue
        if relative.endswith('.yml'):
            assert blob.startswith(b'\xef\xbb\xbfl_english:\n# IMPERIA COLD WAR')
        else:
            assert not blob.startswith(b'\xef\xbb\xbf'), relative
            blob.decode('utf-8')
            if relative.startswith(('common/', 'events/', 'history/')) or relative.startswith('map/strategicregions/'):
                parse(blob.decode('utf-8'))
                assert blob.startswith('# IMPERIA COLD WAR —'.encode()), relative
    passed('generated_parity_script_syntax_markers_and_encoding', files=len(data))

    definitions = [r.split(';') for r in text('map/definition.csv').splitlines() if r and r[0].isdigit()]
    assert [int(r[0]) for r in definitions] == list(range(PROVINCE + 1))
    colours = [tuple(map(int, r[1:4])) for r in definitions]
    # Native definition 16257 shares the reserved black colour with province zero.
    inherited = [tuple(map(int, r.split(';')[1:4])) for r in git_blob(TARGET, 'map/definition.csv').decode().splitlines() if r and r[0].isdigit()]
    assert Counter(colours) - Counter(inherited) == Counter({RGB: 1})
    assert colours.count(RGB) == 1
    assert definitions[PROVINCE][1:] == ['221', '101', '178', 'land', 'false', 'urban', '7']
    assert definitions[16537] == ['16537', '214', '173', '62', 'land', 'true', 'plains', '3']
    old_blob = git_blob(TARGET, 'map/provinces.bmp')
    old, new = np.asarray(Image.open(io.BytesIO(old_blob))), np.asarray(Image.open(io.BytesIO(read('map/provinces.bmp'))))
    assert old.shape == new.shape == (2048, 5632, 3)
    changed = np.any(old != new, axis=2)
    yy, xx = np.where(changed)
    assert len(xx) == 9 and xx.min() >= 3349 and xx.max() <= 3351 and yy.min() >= 873 and yy.max() <= 877
    assert read('map/provinces.bmp')[:54] == old_blob[:54]
    old_rgb = colours[1086]
    masks = {1086: np.all(new == old_rgb, axis=2), PROVINCE: np.all(new == RGB, axis=2)}
    assert np.array_equal(masks[1086] | masks[PROVINCE], np.all(old == old_rgb, axis=2)), 'Outer city boundary changed'
    adjacency = {}
    for province, mask in masks.items():
        assert label(mask)[1] == 1
        assert int(mask.sum()) > 8, 'Native engine warns for provinces of eight pixels or fewer'
        near = binary_dilation(mask) & ~mask
        neighbours = set(map(tuple, new[near]))
        assert all(c in colours for c in neighbours)
        adjacency[province] = sorted(colours.index(c) for c in neighbours)
    assert PROVINCE in adjacency[1086] and 1086 in adjacency[PROVINCE]
    for y in range(868, 880):
        for x in range(3347, 3357):
            assert len(set(map(tuple, new[y:y+2, x:x+2].reshape(-1, 3)))) <= 3, (x, y)
    # No new sea/land painting, unknown colours, or changes to other map regions.
    changed_colours = set(map(tuple, new[changed]))
    assert changed_colours.isdisjoint(c for c, row in zip(colours, definitions) if row[4] != 'land')
    passed('unique_contiguous_ids_connected_land_no_four_way_intersections', changed_pixels=len(xx),
           east_pixels=int(masks[1086].sum()), west_pixels=int(masks[PROVINCE].sum()), adjacent=adjacency)

    state_ids, membership, region_membership = [], {}, {}
    state_paths = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'history/states').glob('*.txt')}
    state_paths.update(k for k in data if k.startswith('history/states/'))
    for relative in sorted(state_paths):
        source = re.sub(r'#[^\n]*', '', text(relative))
        state_id = int(re.search(r'\bid\s*=\s*(\d+)', source)[1])
        state_ids.append(state_id)
        for block in re.findall(r'\bprovinces\s*=\s*\{([^}]+)\}', source):
            for province in map(int, block.split()):
                membership.setdefault(province, []).append(state_id)
    assert len(state_ids) == len(set(state_ids))
    assert membership[PROVINCE] == [STATE] and membership[16537] == [1252] and membership[1086] == [207]
    assert all(len(membership.get(int(r[0]), [])) == 1 for r in definitions if r[4] == 'land' and r[0] != '0'), 'Duplicate or missing land-state assignment'
    for path in (ROOT / 'map/strategicregions').glob('*.txt'):
        source = re.sub(r'#[^\n]*', '', text(path.relative_to(ROOT).as_posix()))
        for block in re.findall(r'\bprovinces\s*=\s*\{([^}]+)\}', source):
            for province in map(int, block.split()):
                region_membership.setdefault(province, []).append(path.name)
    assert region_membership[PROVINCE] == ['174-Levant.txt']
    assert region_membership[16537] == ['212-Cuba.txt']
    passed('unique_state_and_strategic_region_membership', state_count=len(state_ids))

    for relative, prefixes in [('map/buildings.txt', [207, STATE]), ('map/unitstacks.txt', [1086, PROVINCE])]:
        for prefix in prefixes:
            records = rows(relative, prefix)
            expected = old_rgb if prefix in (207, 1086) else RGB
            for record in records:
                x, y = int(float(record[2])), 2047 - int(float(record[4]))
                assert tuple(new[y, x]) == expected, (relative, prefix, record)
            types = Counter(r[1] for r in records)
            if relative.endswith('unitstacks.txt'):
                assert set(types) == {'0', '1', '2', '3', '4', '5', '9', '10', '21', '22', '23', '24', '25', '26', '38'}
                assert all(v == 1 for v in types.values())
            else:
                assert types['industrial_complex'] == types['arms_factory'] == 6
                assert types['special_project_facility_spawn'] == types['supply_node'] == 1
                assert types['landmark_spawn'] == types['western_wall_spawn'] == (1 if prefix == 207 else 0)
        old_records = git_blob(TARGET, relative).decode('utf-8-sig').splitlines()
        ignored = {'207'} if relative.endswith('buildings.txt') else {'1086'}
        extra = str(STATE if relative.endswith('buildings.txt') else PROVINCE)
        existing = [s for s in old_records if s and not s.startswith('#') and s.split(';')[0] not in ignored]
        current = [s for s in text(relative).splitlines() if s and not s.startswith('#') and s.split(';')[0] not in ignored | {extra}]
        assert current == existing, f'Unrelated locators changed: {relative}'
    passed('complete_inland_building_and_unit_locators_inside_their_provinces_and_other_rows_preserved')

    # Use the actual approved mesh envelope, not just its anchor.
    config = json.loads((ROOT / 'tools/jerusalem_landmarks/config.json').read_text())
    x0, x1, z0, z1 = config['footprint_source']
    xx, zz = np.meshgrid(np.linspace(x0, x1, 101), np.linspace(z0, z1, 101))
    px = np.floor(xx * config['scale'] + config['anchor'][0]).astype(int)
    py = np.floor(2048 - (zz * config['scale'] + config['anchor'][2])).astype(int)
    assert np.all(new[py, px] == old_rgb)
    landmarks = ['landmark_spawn', 'western_wall_spawn']
    for kind in landmarks:
        before = [r for r in git_blob(TARGET, 'map/buildings.txt').decode().splitlines() if r.startswith('207;' + kind + ';')]
        after = [';'.join(r) for r in rows('map/buildings.txt', 207) if r[1] == kind]
        assert before == after and len(after) == 1
    east, west = text('history/states/207-Jerusalem.txt'), text('history/states/1253-West Jerusalem.txt')
    assert 'landmark_domeofrock' not in west and 'landmark_jerusalem_western_wall' not in west
    assert east.count('landmark_domeofrock') == east.count('landmark_jerusalem_western_wall') == 1
    passed('dome_and_western_wall_preserved_once_in_east_with_complete_wall_envelope')

    populations = [int(re.search(r'\bmanpower\s*=\s*(\d+)', s)[1]) for s in (east, west)]
    deltas = [int(re.search(r'\badd_manpower\s*=\s*(-?\d+)', s)[1]) for s in (east, west)]
    assert sum(populations) == 829543 and sum(populations) + sum(deltas) == 392282
    assert sum(map(int, re.findall(r'anti_air_building\s*=\s*(\d+)', east + west))) == 4
    assert sum(map(int, re.findall(r'victory_points\s*=\s*\{\s*\d+\s+(\d+)', east + west))) == 8
    categories = text('common/state_category/ICW_jerusalem_split.txt')
    assert sum(map(int, re.findall(r'local_building_slots\s*=\s*(\d+)', categories))) == 8
    assert 'internet_station' not in east + west and 'arms_factory' not in east + west and 'offices' not in east + west
    assert 'capital = 1253' in text('history/countries/ISR - Israel.txt')
    assert '1253 = { set_variable = { productivity_state_var = 655.667 } }' in text('common/scripted_effects/IMP_1970_gdp_scripted_effects.txt')
    assert re.search(r'^1 2 1086 16538$', text('map/railways.txt'), re.M)
    assert 4206 in adjacency[1086] and 4088 in adjacency[1086]
    assert '1 1086' in text('map/supply_nodes.txt')
    for relative in ['common/scripted_triggers/ICW_COMECON_hubs.txt', 'common/scripted_effects/ICW_COMECON_hubs.txt']:
        source = text(relative)
        assert 'state = 1253' in source and 'path = { 16538 1086 }' in source and 'path = { 1086 16538 }' in source
        def first(body, key):
            return next((v for k, op, v in body if k == key), [])
        def without_city(body):
            kept = []
            for key, op, value in body:
                if isinstance(value, list):
                    state = first(value, 'state') if key == 'AND' else first(first(first(value, 'limit'), 'hidden_trigger'), 'state') if key == 'if' else []
                    if state in ('207', '1253'):
                        continue
                    value = without_city(value)
                kept.append((key, op, value))
            return kept
        assert without_city(parse(source)) == without_city(parse(git_blob(TARGET, relative).decode())), 'Unrelated COMECON catalogue entries changed'
    passed('population_building_capacity_victory_points_productivity_and_existing_supply_preserved',
           population_1970={'east': populations[0] + deltas[0], 'west': populations[1] + deltas[1], 'total': 392282})

    for relative in ['history/states/1252-Cayo Blanco del Sur.txt', 'history/states/1251-West Berlin.txt',
                     'history/states/45-Berlin.txt', 'history/states/1241-Kharg.txt', 'map/supply_nodes.txt',
                     'map/heightmap.bmp', 'map/terrain.bmp', 'map/rivers.bmp', 'map/cities.bmp']:
        assert read(relative) == git_blob(TARGET, relative), f'Protected feature changed: {relative}'
    protected = ~changed
    assert np.array_equal(new[protected], old[protected])
    passed('berlin_cayo_kharg_and_all_pixels_outside_jerusalem_preserved')
    report['success'] = True
    report['runtime_hashes'] = {k: sha(v) for k, v in data.items()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / ('validation_installed.json' if options.live else 'validation_proposed.json')).write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'success': True, 'checks': len(report['checks']), 'mode': report['mode']}, indent=2))


if __name__ == '__main__':
    main()
