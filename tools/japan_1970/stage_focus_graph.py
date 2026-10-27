# IMPERIA CW — Cold War: Japan 1970 approved focus graph staging.
"""Generate a non-loaded graph for structural review, not a playable tree."""
import json
from pathlib import Path
import re
from layout import apply_layout, CONTINUOUS_POSITION
from foreign_presentation import offer_tooltip

root = Path(__file__).resolve().parent
design = apply_layout(json.loads((root / 'approved_design.json').read_text(encoding='utf-8'))['design'])
out = root / 'staging' / 'graph'
out.mkdir(parents=True, exist_ok=True)
prefix = 'COLDWAR_JAP_1970_'
def focus_id(ident):
    return ident if ident.startswith(prefix) else prefix + ident
def loc_value(value):
    return value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

icons = {'defence': 'army_defence1', 'navy': 'naval_industry', 'air': 'goal_JAP_JASDF',
         'health': 'generic_healthcare', 'science': 'science', 'politics': 'goverment_building_sheep',
         'labour': 'labor_unions', 'agriculture': 'agriculture2', 'industry': 'focus_JAP_ministry_of_commerce_and_industry',
         'diplomacy': 'diplomacy'}
def focus_icon(node, section):
    """Reuse sprites sampled from the native Japanese and Russian focus trees."""
    # Specific institutions and construction programmes take precedence over
    # the broad branch classifier. All sprites are existing native MD assets.
    overrides = {
        'tohoku_technical_colleges': 'focus_generic_university_2',
        'national_7_technical_colleges': 'focus_generic_university_1',
        'national_10_engineering_faculties': 'focus_generic_university_2',
        'national_10_public_laboratory_grants': 'focus_JAP_expand_the_showa_research_association',
        'tohoku_supply_firms': 'focus_generic_industry_investment',
        'supplier_quality': 'focus_generic_industrialists',
        'brand_discipline': 'focus_generic_industry_investment',
        'tohoku_development': 'focus_JAP_the_five_great_cities',
        'regional_airports': 'generic_airport_icon',
        'hokkaido_ports': 'focus_generic_merchant_fleet',
        'regional_port_links': 'focus_generic_refit_civilian_ships',
        'hokkaido_processing': 'factory_complex',
        'coal_transition': 'focus_JAP_expand_coal_islands',
        'renewable_industry': 'focus_generic_hydroelectric_energy',
        'grid_storage': 'focus_generic_electrification',
        'fuel_reserves': 'focus_JAP_resource_security',
        'national_8_disaster_response': 'focus_generic_field_hostpital',
    }
    if node['id'] in overrides:
        return overrides[node['id']]
    name = (node['id'] + ' ' + node['name']).lower()
    article_icons = {
        'debate': 'examine_foreign_laws', 'commission': 'Focus_AUS_lawmaking_leniency',
        'coalition': 'tripartite_pact', 'campaign': 'focus_JAP_minshu_shugi',
        'party_talks': 'goverment_building_sheep', 'public_hearings': 'Election_graphics',
        'draft': 'constitution', 'civilian': 'goverment_building_sheep',
        'mission': 'army_defence1', 'diet': 'goverment_building_sheep',
        'referendum': 'Election_graphics', 'abolish': 'army_defence1', 'confirm': 'constitution',
    }
    article_prefix = 'COLDWAR_JAP_1970_article9_'
    if node['id'].startswith(article_prefix):
        return article_icons[node['id'][len(article_prefix):]]
    rules = [
        (('article9', 'article nine', 'constitutional', 'constitution'), 'constitution'),
        (('cabinet', 'parliament', 'diet', 'civilian control'), 'goverment_building_sheep'),
        (('civilian investment',), 'focus_JAP_further_urban_investments'),
        (('budget', 'appropriation', 'defence estimates'), 'goal_JAP_budget_check'),
        (('environmental compliance',), 'focus_generic_improve_the_administration'),
        (('alliance',), 'major_alliance3'),
        (('logistics',), 'construction_engineering'),
        (('rural', 'agricultur', 'farming', 'farmers'), 'agriculture2'),
        (('pollution', 'environment', 'environmental'), 'generic_healthcare'),
        (('wage', 'bargain', 'labour', 'labor', 'workers', 'union'), 'BRA_labor_laws'),
        (('public works', 'regional works'), 'construction_buldozer'),
        (('industrial', 'factory', 'factories', 'manufactur'), 'factory_complex'),
        (('market liberal', 'deregulation'), 'BRA_economic_liberalization'),
        (('export', 'trade'), 'trade'),
        (('administra', 'bureaucracy'), 'focus_generic_improve_the_administration'),
        (('nuclear', 'reactor'), 'focus_generic_nuclear_development'),
        (('shinkansen', 'rail', 'commuter'), 'focus_JAP_shinkansen'),
        (('oil', 'fuel', 'energy security'), 'focus_JAP_resource_security'),
        (('electric', 'grid'), 'focus_generic_electrification'),
        (('education', 'school', 'university'), 'education_reform'),
        (('research', 'scientific', 'science'), 'science'),
        (('health', 'medical', 'hospital'), 'generic_healthcare'),
        (('bank', 'credit', 'finance'), 'economic_banks'),
        (('taiwan', 'taipei'), 'align_to_taiwan'),
        (('beijing', 'china'), 'align_to_china'),
        (('seoul', 'south korea'), 'align_to_south_korea'),
        (('pyongyang', 'north korea'), 'align_to_north_korea'),
        (('asean',), 'align_to_asean'),
        (('aircraft', 'air force', 'aircraft'), 'goal_JAP_JASDF'),
        (('shipyard', 'dockyard', 'naval industry'), 'naval_industry'),
    ]
    return next((icon for words, icon in rules if any(word in name for word in words)), icons[section['icon']])
parties = {'LDP governs': (1, 'LDP'), 'Democratic Socialist Party governs': (2, 'DSP'),
           'Japan Socialist Party governs': (3, 'JSP'), 'Japanese Communist Party governs': (4, 'JCP'),
           'Kōmeitō governs': (14, 'Komeito')}
article_rewards = {
    'debate': (-50, 0, 730, 15), 'commission': (-50, 0, 730, 10),
    'coalition': (0, 2, 730, 20), 'campaign': (30, 0, 730, 15),
    'party_talks': (0, 0, 730, 10), 'public_hearings': (0, 1, 730, 10),
    'draft': (0, 1, 730, 8), 'civilian': (0, 0, 730, 8), 'mission': (0, 0, 730, 10),
    'diet': (-75, 0, 365, None), 'referendum': (-75, 2, None, None),
    'abolish': (0, 0, None, None), 'confirm': (0, 0, None, None),
}
short_titles = {
    'national_0_review_the_security_settlement': 'Review Security Policy',
    'national_0_plan_the_self_defence_forces': 'Plan the Defence Forces',
    'national_0_parliamentary_oversight': 'Parliamentary Oversight',
    'national_0_administrative_continuity': 'Administrative Continuity',
    'national_0_a_restrained_defence_budget': 'A Restrained Budget',
    'national_0_expand_defence_appropriations': 'Defence Appropriations',
    'national_0_publish_defence_estimates': 'Publish Defence Estimates',
    'national_0_professional_procurement': 'Professional Procurement',
    'national_0_the_constitutional_settlement': 'The Postwar Constitution',
    prefix + 'article9_debate': 'Debate Article Nine',
    prefix + 'article9_commission': 'Revision Commission',
    prefix + 'article9_coalition': 'A Revision Coalition',
    prefix + 'article9_campaign': 'A Popular Campaign',
    prefix + 'article9_civilian': 'Civilian Control',
    prefix + 'article9_mission': 'A Broader Defence Mission',
    prefix + 'article9_diet': 'Diet Supermajority',
    prefix + 'article9_referendum': 'National Referendum',
    'ldp_industry': 'Asian Finance',
    'distributed_power': 'Local Power & Savings',
    'advanced_manufacturing': 'Manufacturing Edge',
    'china_technology_exchange': 'China Civilian Tech',
    'jcp_policy_1': 'Tenant and Land Laws',
}
curated_titles = root / 'short_titles.json'
if curated_titles.exists():
    short_titles.update(json.loads(curated_titles.read_text(encoding='utf-8')))
    short_titles.update({
        prefix + 'article9_debate': 'Debate Article Nine',
        'ldp_industry': 'Asian Finance',
        'distributed_power': 'Local Power & Savings',
        'advanced_manufacturing': 'Manufacturing Edge',
        'china_technology_exchange': 'China Civilian Tech',
        'jcp_policy_1': 'Tenant and Land Laws',
    })
def article_preview(ident):
    name = ident[len(prefix + 'article9_'):]
    pp, cost, days, support = article_rewards[name]
    preview = ['effect_tooltip = {']
    if pp:
        preview.append(f'add_political_power = {pp}')
    if cost:
        preview.extend([f'set_temp_variable = {{ treasury_change = -{cost} }}', 'modify_treasury_effect = yes'])
    if days:
        preview.append(f'add_timed_idea = {{ idea = {prefix}article9_{name}_climate days = {days} }}')
    if name == 'abolish':
        preview.extend(['remove_ideas = COLDWAR_JAP_1970_article9_self_defence',
                        'add_ideas = COLDWAR_JAP_1970_revised_defence_constitution',
                        'custom_effect_tooltip = COLDWAR_JAP_1970_article9_foreign_reactions_tt'])
    if name == 'confirm':
        preview.extend(['add_political_power = 50',
                        'add_timed_idea = { idea = COLDWAR_JAP_1970_article9_retained_mandate days = 730 }'])
    if support is not None:
        preview.append(f'custom_effect_tooltip = COLDWAR_JAP_1970_article9_support_{support}_tt')
    if name == 'debate':
        preview.append('custom_effect_tooltip = COLDWAR_JAP_1970_article9_campaign_unlocked_tt')
    if name == 'referendum':
        preview.append('custom_effect_tooltip = COLDWAR_JAP_1970_article9_referendum_tt')
    preview.append('}')
    return preview
general = json.loads((root / 'effect_inventory.json').read_text(encoding='utf-8'))
general_ids = {x['id'] for x in general}
general_previews = {x['focus']: x['effect_tooltip'] for x in json.loads(
    (root / 'staging' / 'national_economy_focus_effect_previews.json').read_text(encoding='utf-8'))}
party = json.loads((root / 'party_map.json').read_text(encoding='utf-8'))['focus_helpers']
party_preview_file = root / 'party_effect_tooltip_previews.txt'
party_previews = {}
if party_preview_file.exists():
    source = party_preview_file.read_text(encoding='utf-8')
    for ident in party:
        marker = 'COLDWAR_JAP_1970_party_preview_' + ident
        match = re.search(r'(?m)^' + re.escape(marker) + r'\s*=\s*\{', source)
        if not match:
            continue
        start = match.end()
        depth = 1
        end = start
        while depth and end < len(source):
            depth += (source[end] == '{') - (source[end] == '}')
            end += 1
        if depth:
            raise ValueError('Unbalanced preview for ' + ident)
        party_previews[ident] = source[start:end-1].strip()
foreign_path = root / 'staging' / 'foreign'
domestic = json.loads((foreign_path / 'manifest.json').read_text(encoding='utf-8'))
bilateral = [json.loads(line) for line in (foreign_path / 'bilateral_manifest.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
foreign_registry = json.loads((foreign_path / 'foreign_helper_registry.json').read_text(encoding='utf-8'))
domestic_by_id = {x['focus']: x for x in domestic}
foreign_by_id = {x['focus']: x for x in foreign_registry}
foreign_helpers = {x['focus']: x['effect'] for x in domestic}
foreign_helpers.update({x['focus']: x['helper'] for x in bilateral})
foreign_offer_records = {x['focus']: x for x in bilateral}
nodes = [n for section in design['sections'] for n in section['nodes']]
lines = ['# IMPERIA CW — Cold War: Japan 1970 national focus tree.', 'focus_tree = {',
         '\tid = COLDWAR_JAP_1970_focus', '\tcountry = { factor = 0 }', '\tdefault = no',
         '\tinitial_show_position = { focus = COLDWAR_JAP_1970_national_0_the_civilian_cabinet }',
         f'\tcontinuous_focus_position = {{ x = {CONTINUOUS_POSITION[0]} y = {CONTINUOUS_POSITION[1]} }}']
loc = ['l_english:']
shortcuts = [(0, 'constitution', 'Constitution'), (1, 'defence', 'Self-Defence Forces'),
             (5, 'society', 'Society'), (11, 'economy', 'Economy'), (19, 'alliance', 'The US Alliance'),
             (20, 'east_asia', 'East Asia'), (27, 'ldp', 'LDP'), (28, 'dsp', 'DSP'),
             (29, 'jsp', 'JSP'), (30, 'jcp', 'JCP'), (31, 'komeito', 'Komeito')]
for section_index, key, title in shortcuts:
    shortcut = prefix + 'shortcut_' + key
    target = focus_id(design['sections'][section_index]['nodes'][0]['id'])
    lines.append(f'\tshortcut = {{ name = {shortcut} target = {target} scroll_wheel_factor = 0.8 }}')
    loc.append(f' {shortcut}: "{title}"')
unmapped = []
for section in design['sections']:
    lines.append(f'\t# {section["name"]}')
    anchor = section['nodes'][0]
    for node in section['nodes']:
        ident, fid = node['id'], focus_id(node['id'])
        x = node['globalX'] if node is anchor else node['globalX'] - anchor['globalX']
        y = node['globalY'] if node is anchor else node['globalY'] - anchor['globalY']
        lines += ['\tfocus = {', f'\t\tid = {fid}', f'\t\ticon = {focus_icon(node, section)}',
                  f'\t\tx = {x}', f'\t\ty = {y}',
                  f'\t\tcost = {node["duration"] // 7}']
        if node is not anchor:
            lines.append(f'\t\trelative_position_id = {focus_id(anchor["id"])}')
        search_filter = {'National life':'FOCUS_FILTER_POLITICAL', 'Economy':'FOCUS_FILTER_ECONOMY',
                         'Foreign affairs':'FOCUS_FILTER_FOREIGN_POLICY', 'Political parties':'FOCUS_FILTER_POLITICAL'}[section['category']]
        lines.append(f'\t\tsearch_filters = {{ {search_filter} }}')
        if node['parents']:
            if node['parent_mode'] == 'OR':
                lines.append('\t\tprerequisite = { ' + ' '.join('focus = ' + focus_id(p) for p in node['parents']) + ' }')
            else:
                lines.extend('\t\tprerequisite = { focus = ' + focus_id(p) + ' }' for p in node['parents'])
        if node['exclusive']:
            lines.append('\t\tmutually_exclusive = { ' + ' '.join('focus = ' + focus_id(p) for p in node['exclusive']) + ' }')
        lines += ['\t\tavailable = {', '\t\t\thidden_trigger = { original_tag = JAP IMP_is_1970_scenario = yes }']
        if node['gate'] in parties:
            number, label = parties[node['gate']]
            lines.append(f'\t\t\tcustom_trigger_tooltip = {{ tooltip = {prefix}governing_{label} check_variable = {{ ruling_party = {number} }} }}')
        if ident in foreign_offer_records:
            offer = foreign_offer_records[ident]
            if offer.get('recipient'):
                lines.append(f'\t\t\tcountry_exists = {offer["recipient"]}')
            elif offer.get('recipients'):
                lines.append('\t\t\tOR = { ' + ' '.join('country_exists = ' + target for target in offer['recipients']) + ' }')
        if ident in general_ids:
            from generate_staged_effects import INVENTORY, FOCUS_GUARDS, state_building_guard
            rec = INVENTORY[ident]
            lines.extend('\t\t\t' + guard for guard in FOCUS_GUARDS.get(ident, []))
            lines.extend('\t\t\t' + state_building_guard(*building) for building in rec['buildings'])
        if ident in (prefix + 'article9_debate', prefix + 'article9_commission', prefix + 'article9_abolish', prefix + 'article9_confirm'):
            lines.append('\t\t\thas_idea = COLDWAR_JAP_1970_article9_self_defence')
        if ident == prefix + 'article9_diet':
            lines.append('\t\t\tcustom_trigger_tooltip = { tooltip = COLDWAR_JAP_1970_article9_support_requirement check_variable = { var = COLDWAR_JAP_1970_article9_support value = 67 compare = greater_than_or_equals } }')
        if ident == prefix + 'article9_abolish':
            lines.append('\t\t\thas_stability > 0.54999')
        lines.append('\t\t}')
        helper = None
        if ident in general_ids:
            helper = fid + '_apply'
        elif ident in party:
            helper = party[ident]['effect']
        elif ident.startswith(prefix + 'article9_'):
            helper = prefix + 'article9_reward_' + ident[len(prefix + 'article9_'):]
        elif ident in foreign_helpers:
            helper = foreign_helpers[ident]
        else:
            unmapped.append(ident)
        if helper:
            lines += ['\t\tcompletion_reward = {']
            if ident in general_ids:
                lines.append('\t\t\teffect_tooltip = {')
                lines.extend('\t\t\t\t' + line for line in general_previews[ident].splitlines())
                lines.append('\t\t\t}')
            elif ident in party_previews:
                lines.extend('\t\t\t' + line.strip() for line in party_previews[ident].splitlines())
                lines.append('\t\t\tcustom_effect_tooltip = COLDWAR_JAP_1970_governing_programme_tt')
            elif ident.startswith(prefix + 'article9_'):
                lines.extend('\t\t\t' + line for line in article_preview(ident))
            elif ident in domestic_by_id:
                record = domestic_by_id[ident]
                lines.extend(['\t\t\teffect_tooltip = {',
                              f'\t\t\t\tset_temp_variable = {{ treasury_change = -{record["cost_billions"]:g} }}',
                              '\t\t\t\tmodify_treasury_effect = yes'])
                if record['status'] == 'persistent_dynamic_condition':
                    lines.append('\t\t\t\tcustom_effect_tooltip = COLDWAR_JAP_1970_oil_contingency_tt')
                elif record['status'] == 'staged':
                    idea = f'COLDWAR_JAP70_FOREIGN_{ident}_idea'
                    if record['duration_days']:
                        lines.append(f'\t\t\t\tadd_timed_idea = {{ idea = {idea} days = {record["duration_days"]} }}')
                    else:
                        lines.append(f'\t\t\t\tadd_ideas = {idea}')
                lines.append('\t\t\t}')
            elif ident in foreign_by_id:
                lines.append(f'\t\t\tcustom_effect_tooltip = {fid}_agreement_tt')
                body = offer_tooltip(foreign_by_id[ident], foreign_offer_records[ident])
                loc.append(f' {fid}_agreement_tt: "{loc_value(body)}"')
            lines += [f'\t\t\thidden_effect = {{ {helper} = yes }}', '\t\t}']
        lines += ['\t\tai_will_do = { base = 1 }', '\t}']
        loc.append(f' {fid}: "{loc_value(short_titles.get(ident, node["name"]))}"')
        description = ('The electorate decides whether the approved amendment takes effect.'
                       if ident == prefix + 'article9_referendum' else node['description'])
        loc.append(f' {fid}_desc: "{loc_value(description)}"')
for _, label in parties.values():
    names = {'LDP':'Liberal Democratic Party', 'DSP':'Democratic Socialist Party', 'JSP':'Japan Socialist Party',
             'JCP':'Japanese Communist Party', 'Komeito':'Komeito'}
    loc.append(f' {prefix}governing_{label}: "The {names[label]} leads the government"')
    loc.append(f' {prefix}governing_{label}_NOT: "The {names[label]} does not lead the government"')
loc.append(' COLDWAR_JAP_1970_governing_programme_tt: "Programme modifiers apply while this party leads the government."')
loc.append(' COLDWAR_JAP_1970_article9_support_requirement: "Constitutional reform support is at least 67"')
loc.append(' COLDWAR_JAP_1970_article9_support_requirement_NOT: "Constitutional reform support is below 67"')
for amount in (8, 10, 15, 20):
    loc.append(f' COLDWAR_JAP_1970_article9_support_{amount}_tt: "Constitutional reform support: §G+{amount}§!"')
loc.append(' COLDWAR_JAP_1970_article9_campaign_unlocked_tt: "Unlock public revision campaigns"')
loc.append(' COLDWAR_JAP_1970_article9_referendum_tt: "The electorate will decide the constitutional settlement"')
loc.append(' COLDWAR_JAP_1970_article9_foreign_reactions_tt: "American opinion of Japan: §R−15§! for §Y730 days§!\\nSoviet opinion of Japan: §R−30§! for §Y730 days§!\\nBoth governments may take further diplomatic action."')
loc.append(' COLDWAR_JAP_1970_oil_contingency_tt: "While the §YOil Shock§! is active:\\n  Stability: §G+5%§!\\n  Tax income multiplier: §G+5%§!"')
lines.append('}')
(out / 'focus_tree.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
(out / 'focus_l_english.yml').write_text('\n'.join(loc) + '\n', encoding='utf-8-sig')
(out / 'unmapped.json').write_text(json.dumps(unmapped, indent=2) + '\n', encoding='utf-8')
print(f'Staged {len(nodes)} graph nodes. {len(unmapped)} have no mapped reward; in-game behaviour remains unverified.')
