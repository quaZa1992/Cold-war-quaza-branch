# IMPERIA COLD WAR — Guarded integration of Viltsu's Jerusalem map split.
"""Build a narrow, replay-safe overlay; --apply backs up and installs it on E:."""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import io
import json
import re
import struct
import subprocess

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/audits/jerusalem_split_20261027'
BASE = 'a019ff912cf5064cf7dea860ac1f2be300a735b4'
SOURCE = '972ca21aba34849ad8543654c11546b6c1aa2d4f'
TARGET = '2d08dc687d26b9258921870f81d9107446665da0'
STATE, PROVINCE = 1253, 16538
RGB = (221, 101, 178)
MARK = '# IMPERIA COLD WAR — Jerusalem split integration.\n'
BACKUP = Path('E:/MDColdWar_Backups/Codex_Test_Archives/jerusalem_split_20261027')


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def git_blob(revision, relative):
    blob = subprocess.check_output(['git', 'show', revision + ':' + relative], cwd=ROOT, stderr=subprocess.DEVNULL)
    if blob.startswith(b'version https://git-lfs.github.com/spec/v1'):
        oid = blob.decode().split('oid sha256:')[1].splitlines()[0]
        gitdir = Path(subprocess.check_output(['git', 'rev-parse', '--git-common-dir'], cwd=ROOT, text=True).strip())
        blob = (gitdir / 'lfs/objects' / oid[:2] / oid[2:4] / oid).read_bytes()
        assert sha(blob) == oid
    return blob


def text(revision, relative):
    return git_blob(revision, relative).decode('utf-8-sig').replace('\r\n', '\n')


def marked(value):
    return MARK + value


def bmp_patch(blob, array, mask):
    assert blob[:2] == b'BM' and struct.unpack_from('<H', blob, 28)[0] == 24
    assert struct.unpack_from('<I', blob, 30)[0] == 0
    offset = struct.unpack_from('<I', blob, 10)[0]
    width, height = struct.unpack_from('<ii', blob, 18)
    stride = ((width * 24 + 31) // 32) * 4
    result = bytearray(blob)
    for y, x in zip(*np.where(mask)):
        row = height - 1 - int(y) if height > 0 else int(y)
        pos = offset + row * stride + int(x) * 3
        result[pos:pos + 3] = bytes(map(int, array[y, x, ::-1]))
    return bytes(result)


def state_history(west):
    # Retain the project's calibrated city-wide population and productivity.
    # The approximate 74/26 allocation follows the documented 1967 sector ratio.
    state = STATE if west else 207
    province = PROVINCE if west else 1086
    population, delta = (613862, -323573) if west else (215681, -113688)
    name = 'west' if west else 'east'
    landmark = '' if west else '''
            1086 = {
                landmark_domeofrock = { level = 1 }
            }
'''
    wall = '' if west else '''
        1967.6.10 = {
            buildings = {
                1086 = {
                    landmark_jerusalem_western_wall = 1
                }
            }
        }
'''
    return marked(f'''# Adapted from Viltsu's Split-Jerusalem branch; see the audit provenance.
state = {{
    id = {state}
    name = "STATE_{state}"
    manpower = {population}
    state_category = state_icw_jerusalem_{name}
    history = {{
        owner = ISR
        controller = ISR
        add_core_of = ISR
        add_core_of = PAL
        set_variable = {{ state_renewable_capacity_factor_modifier_var = 0.933 }}
        set_variable = {{ productivity_state_var = 1219 }}
        victory_points = {{ {province} 4 }}
        buildings = {{
            infrastructure = 3
            anti_air_building = 2
            fossil_powerplant = {1 if west else 0}
{landmark}        }}
        add_province_modifier = {{
            static_modifiers = {{ terrain_jerusalem }}
            province = {{ id = {province} }}
        }}
{wall}
        1970.1.1 = {{
            owner = ISR
            controller = ISR
            add_manpower = {delta}
            set_variable = {{ productivity_state_var = 655.667 }}
            buildings = {{ fossil_powerplant = 0 }}
        }}
    }}
    provinces = {{ {province} }}
}}
''')


def locator_rows(relative, prefix):
    return [line.split(';') for line in text(SOURCE, relative).splitlines() if line.startswith(str(prefix) + ';')]


def centre_z(fields):
    # Native lookup uses bottom-up raster rows: H - 1 - floor(world_z).
    # Avoid integer-edge ambiguity in the donor's nudge coordinates.
    if float(fields[4]).is_integer():
        fields[4] = f'{float(fields[4]) - .5:.2f}'


def closing_brace(source, opening):
    masked = re.sub(r'"(?:\\.|[^"\\])*"|#[^\n]*', lambda m: ' ' * len(m[0]), source)
    depth = 1
    for index in range(opening + 1, len(source)):
        depth += (masked[index] == '{') - (masked[index] == '}')
        if not depth:
            return index
    raise AssertionError('Unclosed generated helper')


def hub_catalogue(relative):
    source = text(TARGET, relative)
    trigger = relative.startswith('common/scripted_triggers/')
    pattern = r'(?m)^AND = \{ state = 207 OR' if trigger else r'(?m)^if = \{ limit = \{ hidden_trigger = \{ state = 207 \}'
    found = list(re.finditer(pattern, source))
    assert len(found) == (1 if trigger else 2)
    # Replace only the city's old catalogue entries. Every other state stays exact.
    for match in reversed(found):
        opening = source.index('{', match.start())
        end = closing_brace(source, opening) + 1
        source = source[:match.start()] + source[end + (source[end:end+1] == '\n'):]
    for helper in (['cc_hub_site_valid'] if trigger else ['cc_build_hub', 'cc_preview_hub']):
        start = re.search(r'(?m)^' + helper + r'\s*=\s*\{', source)
        assert start
        opening = source.index('{', start.start())
        if trigger:
            opening = source.index('{', source.index('OR', opening))
        end = closing_brace(source, opening)
        additions = [MARK.rstrip()]
        for state, province, neighbours in [(207, 1086, [4088, 4206, PROVINCE]), (STATE, PROVINCE, [1086])]:
            links = 'OR = { ' + ' '.join(f'AND = {{ PREV = {{ controls_province = {other} }} has_railway_connection = {{ path = {{ {province} {other} }} }} }}' for other in neighbours) + ' }'
            guard = f'PREV = {{ controls_province = {province} }} free_building_slots = {{ building = supply_node size > 0 include_locked = no province = {province} }} {links}'
            if trigger:
                additions.append(f'AND = {{ state = {state} OR = {{ AND = {{ {guard} }} }} }}')
            else:
                reward = f'add_building_construction = {{ type = supply_node level = 1 instant_build = yes province = {province} }}'
                branch = f'if = {{ limit = {{ hidden_trigger = {{ state = {state} }} }}\nif = {{ limit = {{ hidden_trigger = {{ {guard} }} }} {reward} }}\n'
                if helper == 'cc_preview_hub':
                    branch += f'else = {{ {reward} }}\n'
                additions.append(branch + '}')
        source = source[:end] + '\n'.join(additions) + '\n' + source[end:]
    return '# IMPERIA COLD WAR — COMECON Jerusalem split integration.\n' + source


def build():
    outputs = {}

    def emit(relative, value, bom=False):
        outputs[relative] = value if isinstance(value, bytes) else value.encode('utf-8-sig' if bom else 'utf-8')

    baseline = git_blob(TARGET, 'map/provinces.bmp')
    ancestor = np.asarray(Image.open(io.BytesIO(git_blob(BASE, 'map/provinces.bmp'))))
    donor = np.array(Image.open(io.BytesIO(git_blob(SOURCE, 'map/provinces.bmp'))))
    current = np.asarray(Image.open(io.BytesIO(baseline)))
    mask = np.any(ancestor != donor, axis=2)
    assert mask.sum() == 16 and np.array_equal(current[mask], ancestor[mask])
    old_rgb = tuple(map(int, text(TARGET, 'map/definition.csv').splitlines()[1086].split(';')[1:4]))
    # Keep the complete already-approved Western Wall mesh envelope in East Jerusalem.
    for x, y in [(3350, 873), (3351, 873), (3350, 874), (3351, 874)]:
        assert tuple(donor[y, x]) == RGB
        donor[y, x] = old_rgb
    # The native engine warns at exactly eight pixels. Match the nine-pixel
    # floor already used by Kharg and Cayo without touching either landmark.
    assert tuple(donor[877, 3350]) == old_rgb
    donor[877, 3350] = RGB
    # Import only the new western province. The donor's outer-border edits
    # touch existing Judean Plain/West Bank locators and are not needed here.
    mask = np.all(donor == RGB, axis=2)
    assert np.all(ancestor[mask] == old_rgb)
    result = current.copy()
    result[mask] = RGB
    emit('map/provinces.bmp', bmp_patch(baseline, result, mask))

    definitions = text(TARGET, 'map/definition.csv')
    assert definitions.splitlines()[-1].startswith('16537;214;173;62;')
    emit('map/definition.csv', definitions.rstrip('\n') + f'\n{PROVINCE};221;101;178;land;false;urban;7\n')
    region = text(TARGET, 'map/strategicregions/174-Levant.txt')
    region, count = re.subn(r'(\bprovinces\s*=\s*\{)([^}]+)', lambda m: m[1] + m[2].rstrip() + f' {PROVINCE}\n\t', region, count=1)
    assert count == 1
    emit('map/strategicregions/174-Levant.txt', marked(region))

    emit('history/states/207-Jerusalem.txt', state_history(False))
    emit('history/states/1253-West Jerusalem.txt', state_history(True))
    emit('common/state_category/ICW_jerusalem_split.txt', marked('''state_categories = {
    state_icw_jerusalem_east = { local_building_slots = 2 color = { 255 231 173 } }
    state_icw_jerusalem_west = { local_building_slots = 6 color = { 255 216 132 } }
}
'''))
    country = text(TARGET, 'history/countries/ISR - Israel.txt')
    assert country.startswith('capital = 207\n')
    country = country.replace('capital = 207', 'capital = 1253', 1)
    # The inherited infrastructure issue applies to both halves. The Waqf remains east.
    needle = '\t207 = { add_dynamic_modifier = { modifier = ISR_infrastruc_problems } }'
    assert country.count(needle) == 1
    country = country.replace(needle, needle + '\n\t# IMPERIA COLD WAR — Inherited city infrastructure modifier on the western sector.\n\t1253 = { add_dynamic_modifier = { modifier = ISR_infrastruc_problems } }')
    emit('history/countries/ISR - Israel.txt', marked(country))
    productivity = text(TARGET, 'common/scripted_effects/IMP_1970_gdp_scripted_effects.txt')
    needle = '\t\t1252 = { set_variable = { productivity_state_var = 254.534 } }'
    assert productivity.count(needle) == 1
    productivity = productivity.replace(needle, needle + '\n\t\t# IMPERIA COLD WAR — West Jerusalem retains the existing city productivity.\n\t\t1253 = { set_variable = { productivity_state_var = 655.667 } }')
    emit('common/scripted_effects/IMP_1970_gdp_scripted_effects.txt', marked(productivity))
    emit('localisation/english/replace/ICW_jerusalem_split_l_english.yml', '''l_english:
# IMPERIA COLD WAR — Jerusalem split integration.
 STATE_207:0 "East Jerusalem"
 STATE_1253:0 "West Jerusalem"
 VICTORY_POINTS_1086:0 "East Jerusalem"
 VICTORY_POINTS_16538:0 "West Jerusalem"
''', bom=True)

    buildings = text(TARGET, 'map/buildings.txt')
    old_rows = [line for line in buildings.splitlines() if line.startswith('207;')]
    landmark_rows = [r for r in old_rows if r.split(';')[1] in ('western_wall_spawn', 'landmark_spawn')]
    assert len(landmark_rows) == 2
    rows = []
    for prefix in [207, 1252]:
        for fields in locator_rows('map/buildings.txt', prefix):
            if fields[1] == 'landmark_spawn':
                continue
            fields[0] = str(STATE if prefix == 1252 else 207)
            centre_z(fields)
            expected = RGB if prefix == 1252 else old_rgb
            x, y = int(float(fields[2])), 2047 - int(float(fields[4]))
            if tuple(result[y, x]) != expected:
                fields[2:5] = ['3351.50', '9.90', '1171.50']
            rows.append(';'.join(fields))
    rows.extend(landmark_rows)
    # Omit donor changes to states 204/208, and retain every existing Cayo locator.
    kept = [line for line in buildings.splitlines() if not line.startswith('207;')]
    emit('map/buildings.txt', marked('\n'.join(kept) + '\n' + MARK + '\n'.join(rows) + '\n'))

    stacks = text(TARGET, 'map/unitstacks.txt')
    rows = []
    for prefix in [1086, 16537]:
        candidates = {r[1]: r for r in locator_rows('map/unitstacks.txt', prefix)}
        # Complete the same inland locator kinds as native West Berlin, including forts.
        for kind in ['0', '1', '2', '3', '4', '5', '9', '10', '21', '22', '23', '24', '25', '26', '38']:
            fields = candidates.get(kind, candidates['0']).copy()
            fields[0], fields[1] = str(PROVINCE if prefix == 16537 else 1086), kind
            centre_z(fields)
            expected = RGB if prefix == 16537 else old_rgb
            x, y = int(float(fields[2])), 2047 - int(float(fields[4]))
            if tuple(result[y, x]) != expected or kind not in candidates:
                fields[2:5] = ['3349.50', '9.80', '1172.50'] if prefix == 16537 else ['3352.50', '10.20', '1174.50']
            rows.append(';'.join(fields))
    kept = [line for line in stacks.splitlines() if not line.startswith('1086;')]
    emit('map/unitstacks.txt', marked('\n'.join(kept) + '\n' + MARK + '\n'.join(rows) + '\n'))
    railways = text(TARGET, 'map/railways.txt')
    emit('map/railways.txt', marked(railways.rstrip('\n') + f'\n# IMPERIA COLD WAR — Connect the western capital to the retained eastern supply hub.\n1 2 1086 {PROVINCE}\n'))

    # Preserve native peace-plan behaviour for the whole city where it is intended.
    # Palestinian-capital terms already refer specifically to East Jerusalem.
    relative = 'events/Middle East Peace Plan.txt'
    peace = text(TARGET, relative)
    needle = '207 = { remove_core_of = PAL }'
    assert peace.count(needle) == 2
    peace = peace.replace(needle, needle + '\n\t\t\t\t# IMPERIA COLD WAR — Whole-city Israeli settlement.\n\t\t\t\t1253 = { remove_core_of = PAL }')
    peace, count = re.subn(r'(207\s*=\s*\{\s*set_demilitarized_zone\s*=\s*yes\s*\})', r'\1\n\t\t\t\t# IMPERIA COLD WAR — Whole-city internationalisation.\n\t\t\t\t1253 = { set_demilitarized_zone = yes }', peace)
    assert count == 2
    emit(relative, marked(peace))
    relative = 'common/scripted_triggers/00_peace_deal_triggers.txt'
    triggers = text(TARGET, relative)
    needle = '\t\t\t\tstate = 207\n'
    assert triggers.count(needle) == 1
    triggers = triggers.replace(needle, needle + '\t\t\t\t# IMPERIA COLD WAR — Western sector remains in the inherited Palestinian-state catalogue.\n\t\t\t\tstate = 1253\n')
    emit(relative, marked(triggers))
    # These native COMECON catalogues are generated from map/railways and states.
    # Extend their installed outputs without rebuilding unrelated dossier artwork.
    for relative in ['common/scripted_triggers/ICW_COMECON_hubs.txt', 'common/scripted_effects/ICW_COMECON_hubs.txt']:
        emit(relative, hub_catalogue(relative))
    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    options = parser.parse_args()
    outputs = build()
    OUT.mkdir(parents=True, exist_ok=True)
    prior_path = OUT / 'installation.json'
    prior = json.loads(prior_path.read_text(encoding='utf-8')) if prior_path.exists() else None
    report = {'project': 'IMPERIA COLD WAR', 'source_commit': SOURCE, 'base_commit': BASE, 'integration_base': TARGET,
              'new_state': STATE, 'new_province': PROVINCE, 'outputs': {k: sha(v) for k, v in outputs.items()}, 'inputs': {}}
    for relative, blob in outputs.items():
        path = ROOT / relative
        before = path.read_bytes() if path.exists() else None
        report['inputs'][relative] = prior['inputs'][relative] if prior and relative in prior['inputs'] else (sha(before) if before is not None else None)
        if before is not None and sha(before) == sha(blob):
            continue
        if prior and relative in prior['outputs'] and before is not None and sha(before) == prior['outputs'][relative]:
            continue
        try:
            expected = git_blob(TARGET, relative)
        except subprocess.CalledProcessError:
            assert before is None, f'Unrelated new file exists: {relative}'
        else:
            assert before is not None and before.replace(b'\r\n', b'\n') == expected.replace(b'\r\n', b'\n'), f'Uncommitted input changed: {relative}'
    if options.apply:
        for relative, blob in outputs.items():
            path = ROOT / relative
            if path.exists() and path.read_bytes() == blob:
                continue
            if path.exists() and report['inputs'][relative] is not None:
                backup = BACKUP / relative
                backup.parent.mkdir(parents=True, exist_ok=True)
                if backup.exists():
                    assert sha(backup.read_bytes()) == report['inputs'][relative], f'Original backup differs: {relative}'
                else:
                    backup.write_bytes(path.read_bytes())
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(blob)
        report['applied'] = True
    (OUT / ('installation.json' if options.apply else 'plan.json')).write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'outputs': len(outputs), 'applied': options.apply, 'report': str(OUT)}, indent=2))


if __name__ == '__main__':
    main()
