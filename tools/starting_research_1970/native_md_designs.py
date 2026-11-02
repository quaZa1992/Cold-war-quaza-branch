# IMPERIA COLD WAR — Native MD designer types for historical starting equipment.
"""Repair the manifests against MD's actual production and designer contracts."""
import argparse
import hashlib
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from variants import FILES
from component_compat import span

MARK = '# IMPERIA COLD WAR — Native MD historical designer integration.'
TYPE_MAP = {
    'medium_tank_chassis_mdcw_1943': 'medium_tank_chassis_0',
    'medium_tank_chassis_mdcw_1955': 'medium_tank_chassis_0',
    'medium_tank_destroyer_chassis_mdcw_1955': 'medium_tank_destroyer_chassis_0',
    'medium_tank_amphibious_chassis_mdcw_1955': 'medium_tank_amphibious_chassis_0',
    'medium_tank_aa_chassis_mdcw_1955': 'medium_tank_aa_chassis_0',
    'mdcw_small_plane_airframe_gen1': 'small_plane_airframe_1',
    'mdcw_small_plane_airframe_gen2': 'small_plane_airframe_1',
    'mdcw_bba_early_small_airframe_1945': 'small_plane_airframe_1',
    'small_plane_cas_airframe_mdcw_1945': 'small_plane_cas_airframe_1',
    'small_plane_cas_airframe_mdcw_gen1': 'small_plane_cas_airframe_1',
    'small_plane_cas_airframe_mdcw_gen2': 'small_plane_cas_airframe_1',
    'medium_plane_cas_airframe_mdcw_gen1': 'medium_plane_cas_airframe_1',
    'medium_plane_cas_airframe_mdcw_gen2': 'medium_plane_cas_airframe_1',
    'medium_plane_fighter_airframe_mdcw_gen2': 'medium_plane_fighter_airframe_1',
    'cv_small_plane_cas_airframe_mdcw_gen1': 'cv_small_plane_cas_airframe_1',
    'mdcw_destroyer_hull_1955_model': 'destroyer_hull_1',
    'mdcw_diesel_submarine_hull_1959_model': 'attack_submarine_hull_1',
    'mdcw_attack_submarine_hull_1955_model': 'attack_submarine_hull_1',
    'mdcw_carrier_hull_1955_model': 'carrier_hull_1',
}
TRANSPORT_HELOS = {'mdcw_utility_helicopter_1955_modular', 'heavy_tank_amphibious_chassis_0'}
RETIRED_FRAMES = {
    'mdcw_early_piston_attack_1940_model', 'mdcw_early_jet_bomber_1950_model',
    'mdcw_early_carrier_attack_1950_model', 'mdcw_utility_helicopter_1955_modular',
}


def backup():
    destination = HERE / 'native_md_repair_before.json'
    if destination.exists():
        return
    files = list((ROOT / 'history/countries').glob('*.txt'))
    files += [p for p in HERE.iterdir() if p.is_file()]
    files += list((ROOT / 'common/technologies').glob('*'))
    files += list((ROOT / 'common/units/equipment').glob('*.txt'))
    files += [ROOT / 'common/script_enums.txt', ROOT / 'interface/COLDWAR_1970_historical_components.gfx']
    files += list((ROOT / 'localisation/english').glob('COLDWAR_1970_historical*.yml'))
    files += [ROOT / 'common/units/equipment/modules/COLDWAR_1970_historical_components.txt']
    base = Path('E:/MDColdWar_Backups/Codex_Test_Archives').resolve()
    target = (base / ('native_md_design_repair_' + datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S') + '.zip')).resolve()
    assert target.is_relative_to(base)
    base.mkdir(parents=True, exist_ok=True)
    hashes = {}
    with zipfile.ZipFile(target, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(set(files)):
            assert path.is_file() and not path.is_symlink() and not path.is_junction()
            relative = path.relative_to(ROOT).as_posix()
            raw = path.read_bytes()
            archive.writestr(relative, raw)
            hashes[relative] = hashlib.sha256(raw).hexdigest()
    destination.write_text(json.dumps({'project': 'IMPERIA COLD WAR', 'archive': str(target), 'before_sha256': hashes}, indent=2) + '\n', encoding='utf-8')
    print('Archived', len(hashes), 'specific files:', target)


def migrate():
    for filename in FILES:
        path = HERE / filename
        data = json.loads(path.read_text(encoding='utf-8-sig'))
        for key, model in data['models'].items():
            old = model['type']
            if 'native_md_original_type' not in model:
                model['native_md_original_type'] = old
            if old in TRANSPORT_HELOS:
                model.update(type='transport_helicopter_1', modules={}, upgrades={}, requires_dlc=[])
                model.pop('fallback', None)
                model['notes'] = [n for n in model.get('notes', []) if 'modular' not in n.lower() and '1955 utility' not in n.lower()]
                model['notes'].append('Native MD transport-helicopter family, following the fixed Mi-8/UH-1/Z-5 prefabs in the 2000 country histories. No invented gunship modules or unsupported engine-count upgrades. Payload and piston/turbine differences are beyond this fixed MD family.')
            elif old in TYPE_MAP:
                model['type'] = TYPE_MAP[old]
            elif 'airframe' in old and old.endswith('_0'):
                # MD's _0 aircraft are primitive bases. Its actual 2000 old-aircraft
                # prefabs use the first production _1, with equipment set by modules.
                model['type'] = old[:-1] + '1'
            if key in {'eur_an2', 'africa_an2'}:
                model.update(type='medium_plane_air_transport_airframe_1', requires_dlc=['By Blood Alone'],
                             modules={'fixed_main_weapon_slot': 'weap_buff_transport',
                                      'fixed_gun_slot': 'empty', 'engine_type_slot': 'engine_prop_single_1',
                                      'avionics_type_slot': 'avionics_manned_0', 'wingform_type_slot': 'wing_straight'},
                             fallback={'type': 'transport_plane1', 'upgrades': {}})
                model['notes'] = ['Native medium transport role with one propeller engine and cargo module. MD has no biplane wing or low-powered radial engine module; its transport capacity and propeller-engine performance remain coarse abstractions. No weapon, radar or countermeasure package.']
            if key == 'am_p3b':
                model.update(type='large_plane_maritime_patrol_airframe_1', requires_dlc=['By Blood Alone'],
                             modules={'fixed_main_weapon_slot': 'weap_as_hardpoint_1', 'fixed_gun_slot': 'empty',
                                      'engine_type_slot': 'engine_prop_quad_1', 'avionics_type_slot': 'avionics_manned_1',
                                      'wingform_type_slot': 'wing_straight', 'special_slot_type_2': 'spec_mad_1'},
                             fallback={'type': 'naval_plane1', 'upgrades': {}})
                model['notes'] = ['Native maritime patrol designer, first ASW payload tier and magnetic anomaly detector, with four propeller engines. The native payload module covers torpedoes/depth charges and patrol detection. No Harpoon, later P-3C sensors or nuclear payload.']
            if key in {'am_cavalier','am_gua_f51','am_els_corsair','am_hon_corsair','am_bol_f51','am_dom_f51'}:
                model['type']='small_plane_cas_airframe_1'
                model['role']='cas'
                model['modules'].pop('fixed_auxiliary_weapon_slot_1',None)
                model['modules']['fixed_main_weapon_slot']='module_mdcw_unguided_bombs_1945'
                model['notes'].append('Native small close-support role: unguided bombs in the primary slot and historical machine guns in the gun slot. Native small frames have no auxiliary weapon slot. The name is retained from the actual service aircraft.') if not any('Native small close-support role' in n for n in model.get('notes',[])) else None
            if key=='am_p3b':
                model.setdefault('module_exceptions',{})['spec_mad_1']='The original 1960s P-3B carried an AN/ASQ-10 magnetic anomaly detector. Native MD dates its first MAD research node to 1970; only this documented first-generation sensor is supplied as service knowledge, not the 1970 technology or any later upgrade.'
            if 'airframe' in model['type']:
                model['requires_dlc'] = ['By Blood Alone']
            model['native_md_contract'] = ('fixed_transport_helicopter' if model['type'] == 'transport_helicopter_1'
                                           else 'modular_aircraft' if 'airframe' in model['type']
                                           else 'modular_ground' if model.get('modules') and 'tank_' in model['type']
                                           else 'modular_ship' if model.get('modules') and 'hull' in model['type']
                                           else 'fixed_native_equipment')
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def repair_sources():
    # Retire the unregistered extra frames from their research enable lists.
    for filename in ['mdcw_historical_air_naval.txt', 'bombers.txt']:
        path = ROOT / 'common/technologies' / filename
        source = path.read_text(encoding='utf-8-sig')
        for name in RETIRED_FRAMES:
            source = re.sub(r'(?m)^[ \t]*' + re.escape(name) + r'[ \t]*(?:# IMPERIA COLD WAR[^\n]*)?\n', '', source)
        source=source.replace('enable_equipments = { mdcw_utility_helicopter_1955_model',
                              'enable_equipments = { transport_helicopter_1 # IMPERIA COLD WAR: native MD transport family.')
        path.write_bytes(source.encode('utf-8'))
    # Cargo is native MD's only plane_heavy_modules component. The medium
    # transport role exists, but its inherited primary slot omitted that category.
    path = ROOT / 'common/units/equipment/MD_plane_airframes.txt'
    source = path.read_text(encoding='utf-8-sig')
    a, b, c = span(source, 'medium_plane_airframe_1')
    body = source[b+1:c]
    d, e, f = span(body, 'fixed_main_weapon_slot')
    slot = body[e+1:f]
    if 'plane_heavy_modules' not in slot:
        g, h, i = span(slot, 'allowed_module_categories')
        slot = slot[:i] + '\n\t\t\t\t\tplane_heavy_modules # IMPERIA COLD WAR: native medium transport cargo bay.\n\t\t\t\t' + slot[i:]
        body = body[:e+1] + slot + body[f:]
        source = source[:b+1] + body + source[c:]
    if not source.startswith(MARK):
        source = MARK + '\n' + source
    path.write_bytes(source.encode('utf-8'))
    # Earlier Cold War research frames are bare technology rewards, not extra
    # armed prefabs. Historical operating fleets use the native designs above.
    for filename in ['mdcw_historical_air_naval_equipment.txt', 'mdcw_jet_generation_airframes.txt']:
        path = ROOT / 'common/units/equipment' / filename
        source = path.read_text(encoding='utf-8-sig')
        source = re.sub(r'(fixed_main_weapon_slot\s*=\s*)module_mdcw_early_fighter_guns', r'\1empty', source)
        # Do not modify the pre-existing static helicopter or naval definitions.
        path.write_bytes(source.encode('utf-8'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture', action='store_true')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    if args.capture:
        backup()
    if args.apply:
        assert (HERE / 'native_md_repair_before.json').is_file(), 'Capture the pre-repair source first'
        migrate()
        repair_sources()
        print('Native MD historical design manifests repaired')


if __name__ == '__main__':
    main()
