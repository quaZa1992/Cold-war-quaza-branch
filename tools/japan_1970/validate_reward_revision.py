# IMPERIA COLD WAR — Japan 1970 reward overlay validation.
"""Validate reward-overlay coverage without writing staged or loaded output."""
from collections import Counter
import json
import re
from pathlib import Path

from reward_revision import effective_design, effective_inventory, effective_party_map, load_overlay, party_preview_overrides

ROOT = Path(__file__).resolve().parent
DESIGN_PATH = ROOT / 'approved_design.json'
DESIGN = json.loads(DESIGN_PATH.read_text(encoding='utf-8'))['design']
EFFECTIVE = effective_design(DESIGN)
OVERLAY = load_overlay()
errors = []


def node_map(design):
    return {node['id']: (section, node) for section in design['sections'] for node in section['nodes']}


baseline_nodes, effective_nodes = node_map(DESIGN), node_map(EFFECTIVE)
if set(baseline_nodes) != set(effective_nodes):
    errors.append('Focus ID set changed under the reward overlay')
for ident in baseline_nodes.keys() & effective_nodes.keys():
    old_section, old = baseline_nodes[ident]
    new_section, new = effective_nodes[ident]
    if old_section['name'] != new_section['name']:
        errors.append(f'{ident}: section changed')
    for key in ('name', 'description', 'duration', 'x', 'y', 'globalX', 'globalY', 'parents',
                'parent_mode', 'exclusive', 'gate', 'sectionGate', 'sectionIndex'):
        if old.get(key) != new.get(key):
            errors.append(f'{ident}: protected field {key} changed')

general_snapshot = json.loads((ROOT / 'effect_inventory.json').read_text(encoding='utf-8'))
general = effective_inventory(general_snapshot)
party_source = json.loads((ROOT / 'party_map.json').read_text(encoding='utf-8'))
party = effective_party_map(party_source)['focus_helpers']
if not set(OVERLAY.get('inventory', {})) <= set(general):
    errors.append('General inventory overlay contains a missing focus')
if not set(OVERLAY.get('party', {})) <= set(party):
    errors.append('Party overlay contains a missing focus')
if not set(OVERLAY.get('effect_text', {})) <= set(effective_nodes):
    errors.append('Effect-text overlay contains a missing focus')

for ident, record in general.items():
    share = record.get('cost_gdp_share', 0)
    if share:
        if record.get('treasury_cost', 0) != 0 or share <= 0 or share > 0.25:
            errors.append(f'{ident}: GDP-price record has an invalid share or still includes a fixed treasury charge')
        if len(str(share).partition('.')[2]) > 5:
            errors.append(f'{ident}: GDP share literal exceeds five fractional digits')
        focus_text = OVERLAY.get('effect_text', {}).get(ident, '')
        if 'treasury cost:' not in focus_text.lower() or 'current gdp' not in focus_text.lower():
            errors.append(f'{ident}: GDP-priced focus text does not identify the budget basis')
    for key, value in record.get('modifiers', {}).items():
        if key in {'available_workforce_factor', 'available_workforce_size_factor', 'population_factor'} and value < 0:
            errors.append(f'{ident}: prohibited negative workforce/population-size reward')
    for bonus in record.get('bonuses', []):
        if bonus.get('category') not in {'CAT_industry', 'CAT_agriculture'}:
            errors.append(f'{ident}: unverified technology category {bonus.get("category")}')
    for bonus in record.get('doctrine_bonuses', []):
        if bonus.get('category') not in {'land_doctrine', 'naval_doctrine', 'air_doctrine', 'equipment_doctrine'}:
            errors.append(f'{ident}: invalid doctrine category {bonus.get("category")}')
    for equipment in record.get('equipment_bonuses', []):
        if not equipment.get('types'):
            errors.append(f'{ident}: equipment cost bonus has no equipment family')
        for equipment_type, modifiers in equipment.get('types', {}).items():
            if not modifiers or any(key != 'build_cost_ic' for key in modifiers):
                errors.append(f'{ident}: unsupported equipment bonus fields for {equipment_type}')

party_asset_specs = {
    'ldp_deep_fork1_a_follow': (0.0075, 2, [('industrial_complex', 1, 615)], True),
    'ldp_deep_fork1_b_follow': (0.01, 0, [('offices', 2, 612)], False),
    'dsp_programme': (0.01, 2, [('industrial_complex', 1, 614)], True),
    'jsp_programme': (0.01, 0, [('industrial_complex', 1, 612), ('offices', 1, 616)], False),
    'jcp_industry': (0.01, 1, [('industrial_complex', 1, 611), ('offices', 1, 612)], False),
    'komeito_programme': (0.01, 3, [('offices', 1, 612), ('industrial_complex', 1, 616)], False),
}
party_previews = party_preview_overrides()
party_effects = (ROOT / 'staging' / 'party' / 'COLDWAR_JAP_1970_party_effects.txt').read_text(encoding='utf-8')
party_focus_tree = (ROOT / 'staging' / 'graph' / 'focus_tree.txt').read_text(encoding='utf-8')
for ident, (share, fixed_cost, buildings, has_industry_research) in party_asset_specs.items():
    record = party.get(ident)
    if record is None:
        errors.append(f'{ident}: party asset milestone is missing from the effective party map')
        continue
    one_time = record.get('one_time_effects', [])
    share_rewards = [reward for reward in one_time if reward.get('type') == 'treasury_gdp_share']
    if len(share_rewards) != 1 or abs(share_rewards[0].get('share', 0) - share) > 1e-9:
        errors.append(f'{ident}: GDP-priced party milestone share is missing or differs from {share}')
    actual_fixed = sum(-reward.get('amount', 0) for reward in one_time if reward.get('type') == 'treasury')
    if abs(actual_fixed - fixed_cost) > 1e-9:
        errors.append(f'{ident}: original fixed treasury fee {fixed_cost} is not preserved')
    actual_buildings = sorted((reward.get('building'), int(reward.get('level', 0)), int(reward.get('state_id', -1)))
                              for reward in one_time if reward.get('type') == 'building')
    if actual_buildings != sorted(buildings):
        errors.append(f'{ident}: party asset package does not match its approved state/building plan')
    helper_id = record['effect']
    helper_start = party_effects.find(helper_id + ' = {')
    helper_end = party_effects.find('\n}\n', helper_start)
    helper = party_effects[helper_start:helper_end + 3] if helper_start >= 0 and helper_end >= 0 else ''
    preview = party_previews.get(ident, '')
    if 'check_variable = { gdp_total > 0 }' not in helper:
        errors.append(f'{ident}: executor lacks its positive-GDP guard')
    if 'check_variable = { gdp_total > 0 }' not in party_focus_tree[party_focus_tree.find('id = COLDWAR_JAP_1970_' + ident):party_focus_tree.find('\n\tfocus = {', party_focus_tree.find('id = COLDWAR_JAP_1970_' + ident) + 1)]:
        errors.append(f'{ident}: focus availability lacks its positive-GDP guard')
    if f'value = gdp_total multiply = -{share:.5f}' not in helper or f'value = gdp_total multiply = -{share:.5f}' not in preview:
        errors.append(f'{ident}: native numeric GDP price differs between execution and preview')
    for building, level, state_id in buildings:
        grant = f'type = {building} level = {level} instant_build = yes'
        if grant not in helper or grant not in preview:
            errors.append(f'{ident}: {building} x{level} in state {state_id} is missing from executor or preview')
        if f'{state_id} = {{' not in helper or f'{state_id} = {{' not in preview:
            errors.append(f'{ident}: state {state_id} slot/grant scope is missing from executor or preview')
        if f'add_extra_state_shared_building_slots = {level}' not in helper or f'add_extra_state_shared_building_slots = {level}' not in preview:
            errors.append(f'{ident}: one shared state slot per {building} level is missing')
        if 'is_owned_by = ROOT' not in helper or 'is_controlled_by = ROOT' not in helper:
            errors.append(f'{ident}: state {state_id} ownership/control guard is missing')
        if f'building_level@{building} <' not in helper:
            errors.append(f'{ident}: native {building} state-cap headroom guard is missing')
    if 'free_building_slots' in helper:
        errors.append(f'{ident}: party asset transaction incorrectly requires a pre-existing shared slot')
    if has_industry_research and not any(reward.get('type') == 'research_bonus' and
                                         reward.get('category') == 'CAT_industry' and
                                         reward.get('bonus') == 0.5 and reward.get('uses') == 1
                                         for reward in one_time):
        errors.append(f'{ident}: one-use 50% industry research grant is missing')

generator_text = (ROOT / 'generate_staged_effects.py').read_text(encoding='utf-8')
for required in ('check_variable = { gdp_total > 0 }',
                 'value = gdp_total multiply = -',
                 '"modify_treasury_effect = yes"'):
    if required not in generator_text:
        errors.append(f'GDP-price implementation is missing source support: {required}')
if 'custom_effect_tooltip = {fid(node[\'id\'])}_gdp_cost_tt' in generator_text or 'scripted_localisation.txt' in generator_text:
    errors.append('GDP cost preview should use the native treasury effect formatter, not custom scripted localization')
if "'add_political_power = 50'" in (ROOT / 'stage_focus_graph.py').read_text(encoding='utf-8'):
    errors.append('Article 9 confirmation preview still adds the terminal helper political-power reward twice')
if 'terminal_ideas' not in OVERLAY or len(OVERLAY['terminal_ideas']) != 3:
    errors.append('Article 9 terminal idea overlay is incomplete')

effect_text = OVERLAY.get('effect_text', {})
for ident, text in effect_text.items():
    if 'consumer-goods demand' in text.lower():
        errors.append(f'{ident}: consumer_goods_factor is inaccurately described as consumer demand')
    if 'electricity generation +' in text.lower():
        errors.append(f'{ident}: energy_gain_multiplier must be described as an electrical power-generation factor')
generator_text = (ROOT / 'generate_staged_effects.py').read_text(encoding='utf-8')
for required in ('"consumer_goods_factor": "Tax Cost Factor"',
                 '"energy_gain_multiplier": "electrical power generation factor"',
                 '"renewable_energy_gain_multiplier": "renewable power generation factor"'):
    if required not in generator_text:
        errors.append(f'Native modifier label missing or inaccurate: {required}')
foreign = ROOT / 'staging' / 'foreign'
transactions = {row['focus']: row for row in
                (json.loads(line) for line in (foreign / 'bilateral_manifest.jsonl').read_text(encoding='utf-8').splitlines() if line.strip())}
decision_text = (foreign / 'COLDWAR_JAP70_foreign_project_decisions.txt').read_text(encoding='utf-8')
idea_text = (foreign / 'COLDWAR_JAP70_bilateral_ideas.txt').read_text(encoding='utf-8')
event_text = (foreign / 'COLDWAR_JAP70_bilateral_events.txt').read_text(encoding='utf-8')
loc_text = (foreign / 'COLDWAR_JAP70_bilateral_l_english.yml').read_text(encoding='utf-8-sig')
registry_text = (foreign / 'foreign_helper_registry.json').read_text(encoding='utf-8')
if 'consumer-goods demand' in registry_text.lower() or 'consumer-goods demand' in loc_text.lower():
    errors.append('China trade preview still calls consumer_goods_factor consumer-goods demand')
if 'Tax Cost Factor +1%' not in loc_text or 'Tax Cost Factor' not in registry_text:
    errors.append('China trade preview does not display the native Tax Cost Factor label')
project_specs = {
    'seoul_industrial_cooperation': (8.0, [('industrial_complex', 2), ('rail_terminal', 1)], 3),
    'asean_infrastructure': (4.0, [('infrastructure', 2)], 2),
    'mekong_development': (5.0, [('infrastructure', 2), ('rail_terminal', 1)], 3),
    'indochina_reconstruction': (10.0, [('industrial_complex', 2), ('rail_terminal', 1)], 3),
}
for focus, (cost, buildings, slots) in project_specs.items():
    row = transactions.get(focus)
    if not row or abs(row.get('cost_billions', 0) - cost) > .00001:
        errors.append(f'{focus}: foreign transaction cost does not match the authorized offer record')
    if f'treasury_change = -{cost:.3f}' not in decision_text:
        errors.append(f'{focus}: completion payment does not match the offer record')
    block_match = re.search(rf'(?s)COLDWAR_JAP70_{re.escape(focus)}_site\s*=\s*\{{(.*?)\n \}}', decision_text)
    block = block_match.group(1) if block_match else ''
    for building, level in buildings:
        construction = f'type = {building} level = {level} instant_build = yes'
        if block.count(construction) < 2:
            errors.append(f'{focus}: preview and guarded transaction do not both grant {building} x{level}')
    if block.count(f'add_extra_state_shared_building_slots = {slots}') < 2:
        errors.append(f'{focus}: missing slots in preview and guarded transaction')
    if 'is_owned_and_controlled_by = ROOT' not in block or 'COLDWAR_JAP70_' + focus + '_completed' not in block and 'COLDWAR_JAP70_BIL_' + focus + '_completed' not in block:
        errors.append(f'{focus}: missing recipient-site ownership/control or replay receipt gate')
    if focus in {'seoul_industrial_cooperation', 'mekong_development', 'indochina_reconstruction'}:
        if block.count('building_level@rail_terminal < 5') < 2:
            errors.append(f'{focus}: missing native rail-terminal capacity guard')
if 'COLDWAR_JAP70_asean_infrastructure_offices = 0.03' not in decision_text:
    errors.append('ASEAN recurring productivity addition does not match the 3% offer')
if 'COLDWAR_JAP70_asean_infrastructure_offices = -0.03' not in event_text:
    errors.append('ASEAN project expiry does not remove the full 3% productivity grant')
if 'COLDWAR_JAP70_mekong_industry_cooperation:' not in loc_text:
    errors.append('Mekong finite research bonus lacks matching English localization')
key = 'COLDWAR_JAP70_BIL_indochina_reconstruction_idea'
if key not in idea_text or f'{key}:' not in loc_text:
    errors.append(f'{key}: idea or matching English localization missing')
for key in ('COLDWAR_JAP70_BIL_china_technology_exchange_recipient', 'COLDWAR_JAP70_BIL_china_technology_exchange_JAP'):
    if key not in event_text or f'{key}:' not in loc_text:
        errors.append(f'{key}: acceptance effect or matching English localization missing')

money_literals = re.findall(r'treasury_change\s*=\s*-?([0-9]+(?:\.[0-9]+)?)', decision_text)
if any(len(value.partition('.')[2]) > 5 for value in money_literals):
    errors.append('Foreign project budget literal exceeds the five-fractional-digit project limit')

print(f'{len(baseline_nodes)} focus IDs; {len(OVERLAY.get("inventory", {}))} general rewards; '
      f'{len(OVERLAY.get("party", {}))} party rewards; {len(OVERLAY.get("article9", {}))} Article 9 rewards; '
      f'{len(project_specs)} revised regional project offers')
for error in errors:
    print('ERROR:', error)
print(f'{len(errors)} reward revision findings')
raise SystemExit(bool(errors))
