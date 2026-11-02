# IMPERIA COLD WAR — Native small-idea and Cold War focus art for the SSR programme.
"""Reference existing textures without changing approved mechanics or source images."""
from pathlib import Path
import hashlib
import json
import re
import shared

HERE = Path(__file__).resolve().parent
CATALOGUE = json.loads((HERE / 'art_catalogue.json').read_text(encoding='utf-8'))
NODES = {n['id']: n for n in shared.nodes()}
PARTY_ART = {shared.slug(n['group_key']): n['art_key'] for n in NODES.values()
             if n['phase'] == 'party' and n['key'].endswith('_root')}
ROLE = {'aircraft': 'air', 'armour': 'armour', 'artillery': 'artillery',
        'army': 'army', 'navy': 'navy', 'agriculture': 'agriculture',
        'industry': 'industry', 'resources': 'resources', 'electronics': 'electronics'}
PARTY_FOCUS = {'communist': 'socialism', 'liberal': 'market', 'social': 'workers',
               'national_social': 'workers', 'national': 'independence',
               'nationalist': 'independence', 'liberation': 'independence',
               'authoritarian': 'authoritarian', 'restoration': 'constitution',
               'conservative': 'constitution', 'faith_civic': 'constitution',
               'unionist': 'union'}
PARTY_SPIRIT = {'communist': 'socialism', 'liberal': 'liberal',
                'social': 'social_democrat', 'national_social': 'social_democrat',
                'conservative': 'conservative', 'authoritarian': 'discipline',
                'restoration': 'administration', 'faith_civic': 'administration',
                'unionist': 'diplomacy', 'national': 'national',
                'nationalist': 'national', 'liberation': 'national'}
REGIONAL = {'UKR': 'industry', 'BLR': 'trade', 'MLV': 'industry',
            'EST': 'energy', 'LAT': 'industry', 'LIT': 'agriculture',
            'GEO': 'patronage', 'ARM': 'trade', 'AZE': 'energy',
            'KAZ': 'resources', 'UZB': 'agriculture', 'TRK': 'agriculture',
            'KYR': 'water', 'TAJ': 'industry'}

COMMON = {}
for _theme, _keys in {
    'administration': 'secretariat local_cadres civil_registers public_authority executive_service regional_service',
    'cadres': 'moscow_cadres successor_training',
    'education': 'appointment_school technical_institutes vocational_schools officer_education local_officers',
    'audit': 'audit_staff discipline_campaign rights_commission',
    'constitution': 'controlled_debate unified_line republican_statute citizenship_civic citizenship_restoration',
    'negotiation': 'complaints_office plan_bargain social_compact',
    'union': 'union_delegate deepen_specialisation combined_exercises',
    'planning': 'economic_accounts plan_settlement',
    'industry': 'combine_priority dual_use_industry domestic_chains industrial_conversion regional_orders',
    'consumer': 'local_retention consumer_priority housing_repairs regional_diversify',
    'fiscal': 'enterprise_accounts revenue_service registered_accounts payment_register budget_consolidation transition_settlement',
    'efficiency': 'output_incentives quality_contracts energy_savings fuel_discipline commercial_standards',
    'transport': 'rail_depots strategic_transport',
    'food': 'rural_processing household_plots',
    'production': 'machine_tools military_components',
    'supplies': 'service_networks maintenance_stocks technical_reserves military_repairs ready_stocks supplier_contracts maintenance_command reserve_records',
    'energy': 'new_power energy_offer',
    'health': 'social_accounts public_health service_settlement budget_protection',
    'workers': 'republican_culture worker_ownership',
    'research': 'union_curriculum regional_standards',
    'agriculture': 'collective_farms',
    'water': 'water_accounts environmental_controls remediation_fund river_offer',
    'defence': 'defence_commission civil_shelters defence_records defence_authority defence_settlement prepared_defence',
    'army': 'specialist_training mass_training professional_force territorial_force mobile_defence training_offer',
    'local_authority': 'unitary_services local_guarantees regional_review',
    'rule_of_law': 'court_review',
    'market': 'rapid_conversion gradual_conversion open_tenders',
    'public_ownership': 'directed_reform',
    'trade': 'diversify_orders export_conversion old_market_offer',
    'diplomacy': 'foreign_service new_market_offer border_offer civil_neutrality',
}.items():
    COMMON.update({key: _theme for key in _keys.split()})


def focus_theme(node):
    key = node['key']
    if key in COMMON:
        return COMMON[key]
    if node.get('specialisation'):
        role = node['specialisation']
        if key.endswith('_schools'):
            return 'computing' if role == 'electronics' else 'education'
        if key.endswith('_efficiency'):
            return 'efficiency'
        if key.endswith('_office'):
            return 'administration'
        if key.endswith('_priority'):
            return 'planning'
        if key.endswith('_settlement'):
            return 'union'
        if key.endswith('_works'):
            return {'aircraft': 'air_industry', 'electronics': 'electronics',
                    'navy': 'navy', 'agriculture': 'agriculture'}.get(role, 'production')
        if 'Institute' in node['title'] or 'Laborator' in node['title']:
            return 'research'
        if role == 'artillery' and 'Volume' in node['title']:
            return 'production'
        return ROLE[role]
    art = node['art_key']
    if art.startswith('party_'):
        return PARTY_FOCUS[art[6:]]
    if node['phase'] == 'party':
        suffix = re.sub(r'^p\d+_', '', key)
        themes = {'civic': 'constitution', 'executive': 'authoritarian',
                  'institution': 'administration', 'archives': 'audit',
                  'public': 'public_ownership', 'market': 'market',
                  'production': 'industry', 'consumer': 'consumer',
                  'development': 'research', 'universal': 'health',
                  'targeted': 'food', 'civilian': 'consumer', 'cadres': 'cadres',
                  'enterprise_service': 'supplies', 'revenue_courts': 'rule_of_law',
                  'settlement': 'constitution'}
        if suffix in themes:
            return themes[suffix]
    return {'institution': 'constitution', 'industry': 'industry',
            'research': 'research', 'society': 'health', 'army': 'army',
            'agriculture': 'agriculture', 'diplomacy': 'diplomacy',
            'air': 'air', 'navy': 'navy'}[node['kind']]


def focus_icon(node):
    return 'GFX_COLDWAR_SSR_goal_' + focus_theme(node)


def spirit_theme(identifier):
    name = identifier.removeprefix('COLDWAR_SSR_')
    if name.startswith('lifecycle_'):
        name = name[10:]
        if name.startswith('special_'):
            return ROLE[name.split('_')[1]]
        if name.startswith('group_'):
            group = name[6:]
            if group.startswith('party_'):
                return PARTY_SPIRIT[PARTY_ART[group][6:]]
            if group.startswith('regional_'):
                return REGIONAL[group[-3:].upper()]
            return {'secretariat': 'civil_service', 'planning': 'planning',
                    'society': 'social', 'union_defence': 'army',
                    'statehood': 'administration', 'transition_economy': 'finance',
                    'national_defence': 'army', 'foreign': 'diplomacy'}[group]
        if name.startswith('transition_'):
            return {'broken_supply': 'trade', 'state_accounts': 'restructuring',
                    'command_gap': 'army'}[name[11:]]
        tag, _, stage = name.partition('_')
        if stage.startswith('regional_'):
            return REGIONAL[tag]
        return {'unconverted_orders': 'trade', 'plan': 'shortages',
                'plan_revised': 'planning', 'plan_republican': 'industry',
                'patronage': 'patronage', 'professional': 'civil_service',
                'discipline': 'discipline', 'social': 'social',
                'social_republican': 'social', 'technical': 'science'}[stage]
    if name.startswith('diplomacy_'):
        key = name[10:].rsplit('_', 1)[0]
        return {'clearing': 'trade', 'technical': 'science', 'border': 'diplomacy',
                'training': 'army', 'energy': 'energy', 'water': 'water',
                'romanian': 'diplomacy'}[key]
    if name.startswith('market_'):
        if 'method_preview_' in name:
            return {'auction': 'finance', 'workers': 'social',
                    'liquidate': 'fiscal_crisis', 'public': 'industry'}[name.rsplit('_', 1)[-1]]
        if 'fiscal' in name:
            return 'fiscal_crisis'
        if 'burden' in name or 'relief' in name:
            return 'restructuring'
        if 'settlements' in name:
            return 'industry'
        return 'finance'
    raise ValueError('Unmapped SSR national-spirit artwork: ' + identifier)


def picture_for_idea(identifier):
    return 'COLDWAR_SSR_' + spirit_theme(identifier)


def icon_for_idea(identifier):
    return 'GFX_idea_' + picture_for_idea(identifier)


def generate():
    lines = ['spriteTypes = {']
    for theme, asset in CATALOGUE['spirit'].items():
        lines.extend(['\tspriteType = {', '\t\tname = "GFX_idea_COLDWAR_SSR_' + theme + '"',
                      '\t\ttexturefile = "' + asset['texture'] + '"', '\t}'])
    for theme, asset in CATALOGUE['focus'].items():
        sprite = 'GFX_COLDWAR_SSR_goal_' + theme
        texture = asset['texture']
        lines.extend(['\tspriteType = {', '\t\tname = "' + sprite + '"',
                      '\t\ttexturefile = "' + texture + '"', '\t}'])
        lines.extend(['\tspriteType = {', '\t\tname = "' + sprite + '_shine"',
                      '\t\ttexturefile = "' + texture + '"',
                      '\t\teffectFile = "gfx/FX/buttonstate.lua"'])
        for rotation in (-90.0, 90.0):
            lines.extend(['\t\tanimation = {', '\t\t\tanimationmaskfile = "' + texture + '"',
                          '\t\t\tanimationtexturefile = "gfx/interface/goals/shine_overlay.dds"',
                          '\t\t\tanimationrotation = ' + str(rotation),
                          '\t\t\tanimationlooping = no', '\t\t\tanimationtime = 0.75',
                          '\t\t\tanimationdelay = 0', '\t\t\tanimationblendmode = "add"',
                          '\t\t\tanimationtype = "scrolling"',
                          '\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }',
                          '\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 }', '\t\t}'])
        lines.extend(['\t\tlegacy_lazy_load = no', '\t}'])
    lines.append('}')
    return [shared.write('interface/COLDWAR_SSR_icons.gfx', '\n'.join(lines) + '\n')]


def install_art_only():
    """Narrow installation: replace graphic fields, prove all other script semantics identical."""
    import sys
    sys.path.insert(0, str(shared.ROOT / 'tools/vietnam_1970'))
    from script_ast import parse
    def without_art(rows):
        return [(k, op, without_art(v) if isinstance(v, list) else v)
                for k, op, v in rows if k not in {'icon', 'picture'}]
    paths = ['common/national_focus/COLDWAR_SSR_1970_focus.txt',
             'common/ideas/COLDWAR_SSR_lifecycle_ideas.txt',
             'common/dynamic_modifiers/COLDWAR_SSR_lifecycle_dynamic_modifiers.txt',
             'common/ideas/COLDWAR_SSR_market_preview.txt',
             'common/dynamic_modifiers/COLDWAR_SSR_market.txt',
             'common/ideas/COLDWAR_SSR_diplomacy.txt']
    changed = []
    counts = {}
    for rel in paths:
        path = shared.ROOT / rel
        old = path.read_text(encoding='utf-8')
        if '/national_focus/' in rel:
            pattern = r'(\bid\s*=\s*(COLDWAR_SSR_\w+)\s*\n\s*icon\s*=\s*)\S+'
            new, count = re.subn(pattern, lambda m: m[1] + focus_icon(NODES[m[2]]), old)
            assert count == len(NODES)
        else:
            pattern = r'(^[ \t]*)(COLDWAR_SSR_\w+)(\s*=\s*\{\n[ \t]*)(picture|icon)\s*=\s*"?\w+"?'
            def replace(m):
                value = picture_for_idea(m[2]) if m[4] == 'picture' else icon_for_idea(m[2])
                return m[1] + m[2] + m[3] + m[4] + ' = ' + value
            new, count = re.subn(pattern, replace, old, flags=re.M)
            assert count > 0, rel
        assert without_art(parse(old)) == without_art(parse(new)), 'Non-art change: ' + rel
        if new != old:
            path.write_text(new, encoding='utf-8')
            changed.append(rel)
        counts[rel] = count
    gfx = generate()
    manifest_path = HERE / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    for rel in paths + gfx:
        key = next((p for p in manifest['outputs'] if Path(p).as_posix() == Path(rel).as_posix()), str(Path(rel)))
        manifest['outputs'][key] = hashlib.sha256((shared.ROOT / rel).read_bytes()).hexdigest()
    manifest['art_catalogue_sha256'] = hashlib.sha256((HERE / 'art_catalogue.json').read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return {'project': 'IMPERIA COLD WAR', 'changed': changed, 'graphic_fields': counts,
            'non_graphic_script_semantics_unchanged': True, 'source_images_modified': False,
            'new_interface': gfx, 'live_game_inspection': False}


if __name__ == '__main__':
    report = install_art_only()
    (HERE / 'ART_INSTALLATION.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))
