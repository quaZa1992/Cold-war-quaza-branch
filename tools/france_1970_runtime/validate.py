# IMPERIA COLD WAR — Installed France 1970 source and contract validation.
"""Check emitted files and the immutable approval, without executing retired tools."""
from __future__ import annotations
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from focus_prerequisite_ui import nodes, field


def walk(rows):
    for row in rows:
        yield row
        yield from walk(row.children())


def walk_context(rows, parent=None):
    for row in rows:
        yield row, parent
        yield from walk_context(row.children(), row.key)


def main():
    issues = []
    def require(ok, msg):
        if not ok:
            issues.append(msg)
    from balance_revision import apply_balance_revision
    from starting_spirit_revision import apply_starting_spirit_revision
    from asset_reward_revision import apply_asset_reward_revision
    from expansion_revision import apply_expansion_revision
    approved = apply_asset_reward_revision(apply_starting_spirit_revision(apply_balance_revision(json.loads((HERE / 'approved_party_revision.json').read_text(encoding='utf-8')))))
    approved['status'] = 'IMPLEMENTED. Compiled from the approved France 1970 party revision.'
    approved['approved_source_sha256'] = '4f57a4c6e3d13eba6b7ec4129cb81fd8b9a2a645e9fac10c5ebf8d36588c18b5'
    approved['approved_party_revision_sha256'] = '5159aaad0f0b13bbf3ef38e2d374be05fcb907a5df6386c8b2e933520b278419'
    approved['revision'] = 'FRA2 runtime 1.2: persistent recovery and funded investment'
    approved = apply_expansion_revision(approved)
    approved['status'] = 'IMPLEMENTED. Compiled from the approved France 1970 party and expansion revisions.'
    approved['approved_expansion_sha256'] = 'c8e6ab3933bf72a14b043c3a92d846826f3d1937f902efc7cc3d0dd64364c055'
    approved['revision'] = 'FRA2 runtime 1.3: approved 20-focus party expansion'
    from foreign_policy_revision import apply_foreign_policy_revision, APPROVED_SHA256 as FOREIGN_POLICY_HASH
    approved = apply_foreign_policy_revision(approved)
    approved['status'] = 'IMPLEMENTED. Compiled from approved French national and foreign-policy programmes.'
    approved['approved_foreign_policy_sha256'] = FOREIGN_POLICY_HASH
    approved['revision'] = 'FRA2 runtime 1.4: negotiated foreign policy'
    from deal_balance_revision import apply_deal_balance_revision
    approved = apply_deal_balance_revision(approved)
    approved['revision'] = 'FRA2 runtime 1.5: asymmetric agreements and restrained doctrine rewards'
    approved['pressure_revision'] = json.loads((HERE / 'pressure_contracts.json').read_text(encoding='utf-8'))
    from ec_membership_revision import apply_ec_membership_revision
    approved = apply_ec_membership_revision(approved)
    design = json.loads((HERE / 'runtime_design.json').read_text(encoding='utf-8'))
    manifest = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))
    require(hashlib.sha256((HERE / 'approved_design.json').read_bytes()).hexdigest() == manifest['approved_sha256'], 'Approval hash')
    require(hashlib.sha256((HERE / 'approved_party_revision.json').read_bytes()).hexdigest() == manifest['approved_party_revision_sha256'], 'Party revision approval hash')
    require(hashlib.sha256((HERE / 'approved_expansion.json').read_bytes()).hexdigest() == manifest['approved_expansion_sha256'], 'Expansion approval hash')
    require(hashlib.sha256((HERE / 'EXPANSION_APPROVAL.json').read_bytes()).hexdigest() == manifest['expansion_approval_sha256'], 'Expansion approval record hash')
    require(hashlib.sha256((HERE / 'balance_revision.py').read_bytes()).hexdigest() == manifest['balance_revision_source_sha256'], 'Tangible trade-off source hash')
    require(hashlib.sha256((HERE / 'expansion_revision.py').read_bytes()).hexdigest() == manifest['expansion_revision_source_sha256'], 'Expansion overlay source hash')
    require(hashlib.sha256((HERE / 'approved_foreign_policy.json').read_bytes()).hexdigest() == manifest['approved_foreign_policy_sha256'], 'Foreign-policy approval input hash')
    require(hashlib.sha256((HERE / 'foreign_policy_revision.py').read_bytes()).hexdigest() == manifest['foreign_policy_revision_source_sha256'], 'Foreign-policy overlay source hash')
    require(hashlib.sha256((HERE / 'deal_balance_revision.py').read_bytes()).hexdigest() == manifest['deal_balance_revision_source_sha256'], 'Agreement balance source hash')
    require(hashlib.sha256((HERE / 'pressure.py').read_bytes()).hexdigest() == manifest['pressure_source_sha256'], 'Pressure source hash')
    require(hashlib.sha256((HERE / 'pressure_contracts.json').read_bytes()).hexdigest() == manifest['pressure_contracts_sha256'], 'Pressure contract source hash')
    require(design.get('pressure_revision') == approved['pressure_revision'], 'Pressure contract compiled design')
    require(manifest.get('pressure_partner_count') == 6, 'Six pressure partners')
    require(len(design['deal_balance_revision']['removed_negative_agreement_tax_modifiers']) == 22, 'Twenty-two agreement tax penalties removed')
    for node in design['nodes']:
        for side in ('france', 'recipient'):
            require(not any(e.get('key') == 'corporate_tax_income_multiplier_modifier' and e.get('value', 0) < 0
                            for e in node.get('offer', {}).get(side, {}).get('effects', [])), 'Negative bilateral corporate-tax penalty: ' + node['key'])
        for effect in node.get('effects', []) + node.get('offer', {}).get('france', {}).get('effects', []):
            if effect.get('kind') == 'doctrine' and effect.get('category') == 'land_doctrine':
                require(effect['reduction'] <= .25 and effect['uses'] == 1, 'French land-doctrine ceiling: ' + node['key'])
    require(hashlib.sha256((HERE / 'FOREIGN_POLICY_APPROVAL.json').read_bytes()).hexdigest() == manifest['foreign_policy_approval_sha256'], 'Foreign-policy authorization record hash')
    expansion_approval = json.loads((HERE / 'EXPANSION_APPROVAL.json').read_text(encoding='utf-8'))
    expansion_snapshot = json.loads((HERE / 'approved_expansion.json').read_text(encoding='utf-8'))
    require(expansion_approval.get('project') == 'IMPERIA COLD WAR', 'Expansion approval project marker')
    require(expansion_approval.get('approval_date') == '2026-10-30', 'Expansion approval date')
    require(expansion_approval.get('user_quote') == 'gerne alles dann reincoden, die visualisierten neuerungen auch', 'Expansion approval quote')
    require(expansion_approval.get('approved_input_sha256') == manifest['approved_expansion_sha256'], 'Expansion approval snapshot hash binding')
    require(hashlib.sha256((HERE / 'approved_expansion.json').read_bytes()).hexdigest() == 'c8e6ab3933bf72a14b043c3a92d846826f3d1937f902efc7cc3d0dd64364c055', 'Frozen expansion source hash')
    for module in ('starting_spirit_revision', 'asset_reward_revision', 'ec_membership_revision'):
        require(hashlib.sha256((HERE / (module + '.py')).read_bytes()).hexdigest() == manifest[module + '_source_sha256'], module + ' source hash')
    parsed = {}
    generated_scripts = {}
    for rel, record in manifest['files'].items():
        path = ROOT / rel
        raw = path.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == record['sha256'], 'Manifest drift: ' + rel)
        if rel.endswith(('.txt', '.gfx', '.gui', '.yml')):
            isloc = rel.endswith('.yml')
            require(raw.startswith(b'\xef\xbb\xbf') == isloc, 'Encoding: ' + rel)
            text = raw.decode('utf-8-sig')
            line = text.splitlines()[1 if isloc else 0]
            require(line.startswith('# IMPERIA COLD WAR — '), 'File-start project marker: ' + rel)
            if not isloc:
                try:
                    parsed[rel] = nodes(text)
                except Exception as exc:
                    issues.append(f'Parse {rel}: {exc}')
                if record['ownership'] == 'generated_runtime':
                    generated_scripts[rel] = text

    tree_rel = 'common/national_focus/COLDWAR_FRA2_1970_focus.txt'
    tree = next(n for n in parsed[tree_rel] if n.key == 'focus_tree')
    focuses = {field(n.children(), 'id'): n for n in tree.children() if n.key == 'focus'}
    expected = {n['id']: n for n in design['nodes']}
    require(set(focuses) == set(expected), 'Installed focus roster differs')
    require(len(focuses) == 213, 'Expected 213 focuses')
    added_keys = {n['key'] for n in design['nodes'] if n.get('expansion_change') == 'new'}
    require(len(added_keys) == 20, 'Expected the approved 20 expansion focuses')
    require(added_keys == set(expansion_approval.get('added_focus_keys', [])), 'Expansion approval focus key set')
    require({n['key'] for n in expansion_snapshot['nodes'] if n.get('expansion_change') == 'new'} == added_keys, 'Frozen proposal focus key set')
    require(set(design.get('expansion_revision', {}).get('added_focus_keys', [])) == added_keys, 'Expansion receipt key set differs')
    require(sum('offer' in n for n in design['nodes']) == 67, 'Expected 67 reciprocal offers')
    foreign_keys = {n['key'] for n in design['nodes'] if n.get('foreign_policy_change') == 'new'}
    require(len(foreign_keys) == 37, 'Expected 37 new foreign-policy focuses')
    require(foreign_keys == set(design.get('foreign_policy_revision', {}).get('added_focus_keys', [])), 'Foreign-policy receipt key set')
    require(design.get('decisions') == approved.get('decisions'), 'Domestic decision payload differs from approval')
    require(len(design.get('decisions', [])) == 5, 'Expected five domestic decisions')
    require('allow_branch' not in generated_scripts[tree_rel], 'Hidden political branches')
    resolved = {}
    resolving = set()
    emitted_order = list(focuses)
    def position(nid):
        if nid in resolved:
            return resolved[nid]
        assert nid not in resolving, ('Anchor cycle', nid)
        resolving.add(nid)
        row = focuses[nid].children()
        x, y = float(field(row, 'x')), float(field(row, 'y'))
        parent = field(row, 'relative_position_id')
        if parent:
            require(emitted_order.index(parent) < emitted_order.index(nid), 'Anchor declared too late: ' + nid)
            px, py = position(parent)
            x += px
            y += py
        resolving.remove(nid)
        resolved[nid] = (x, y)
        return x, y
    original = {n['id']: n for n in approved['nodes']}
    groups = {g['id']: g for g in design['groups']}
    for nid, spec in expected.items():
        rows = focuses[nid].children()
        require(position(nid) == (spec['x'], spec['y']), 'Coordinates: ' + nid)
        prereqs = [[field([e], 'focus') for e in n.children() if e.key == 'focus'] for n in rows if n.key == 'prerequisite']
        excl = [e.value for n in rows if n.key == 'mutually_exclusive' for e in n.children() if e.key == 'focus']
        require(prereqs == [['COLDWAR_FRA2_' + p for p in group] for group in spec['prerequisites']], 'Prerequisites: ' + nid)
        require(set(excl) == {'COLDWAR_FRA2_' + p for p in spec['exclusions']}, 'Exclusions: ' + nid)
        require(float(field(rows, 'cost')) == spec['cost'], 'Focus cost: ' + nid)
        for key in ('effects', 'cost', 'days', 'prerequisites', 'exclusions', 'group', 'lifetime', 'conditions', 'reward_guards', 'activation_conditions', 'title', 'description', 'icon', 'icon_source', 'spirit', 'spirit_name', 'modifier_pool', 'programme_activation_conditions'):
            require(spec.get(key) == original[nid].get(key), 'Unapproved gameplay change: ' + nid + '/' + key)
        if spec.get('offer'):
            from copy import deepcopy
            def offer_payload(value):
                value = deepcopy(value)
                for side in ('france', 'recipient'):
                    value[side].pop('name', None)
                    value[side].pop('picture', None)
                return value
            require(offer_payload(spec['offer']) == offer_payload(original[nid]['offer']), 'Unapproved offer gameplay change: ' + nid)
        available = next(n for n in rows if n.key == 'available')
        text = generated_scripts[tree_rel][available.start:available.end]
        group = groups[spec['group']]
        if group.get('trigger'):
            require(group['trigger'] + ' = yes' in text, 'Visible native party check: ' + nid)
        if spec['group'] == 'udr_nato':
            require('has_idea = NATO_member' in text, 'NATO availability: ' + nid)
        reward = next(n for n in rows if n.key == 'completion_reward')
        rtext = generated_scripts[tree_rel][reward.start:reward.end]
        require('effect_tooltip' in rtext and 'hidden_effect' in rtext, 'Preview/execution separation: ' + nid)
        for effect in spec['effects']:
            if effect['kind'] == 'faction_opinion':
                require(effect['provider'] + ' = yes' in rtext, 'Native MD opinion preview: ' + nid)
                require('temp_opinion = ' + str(effect['value']) in rtext, 'Opinion point value: ' + nid)
        if spec.get('offer'):
            require('COLDWAR_FRA2_offer_preview_' + spec['key'] + ' = yes' in rtext, 'Bilateral focus preview: ' + nid)

    loc_rel = 'localisation/english/COLDWAR_FRA2_1970_l_english.yml'
    loc = (ROOT / loc_rel).read_text(encoding='utf-8-sig')
    pairs = re.findall(r'^ ([^\s:]+):\d*\s+"(.*)"\s*$', loc, re.M)
    keys = [k for k, _ in pairs]
    require(len(keys) == len(set(keys)), 'Duplicate English localisation')
    require(len(keys) == manifest['english_localisation_keys'], 'Localisation parse/count mismatch')
    require('\u2013' not in '\n'.join(v for _, v in pairs) and '\u2014' not in '\n'.join(v for _, v in pairs), 'Player-facing dash punctuation')
    require(not any(k.startswith('COLDWAR_FRA2_faction_') and k.endswith('_opinion_tt') for k in keys), 'Retired percentage opinion preview must not be emitted')
    for nid in expected:
        require(nid in keys and nid + '_desc' in keys, 'Missing focus localisation: ' + nid)

    # A call-like custom key must resolve to a declared scripted provider. Flags,
    # numeric backing variables and dynamic modifier arguments are not calls.
    providers = {n.key for rel, rows in parsed.items() if '/scripted_effects/' in rel or '/scripted_triggers/' in rel for n in rows}
    defined_ideas = {n.key for rel, rows in parsed.items() if '/ideas/' in rel
                     for n, parent in walk_context(rows) if parent == 'country' and n.key.startswith('COLDWAR_FRA2_')}
    custom_provider_list = [n.key for rel, rows in parsed.items() if '/scripted_effects/' in rel or '/scripted_triggers/' in rel for n in rows if n.key.startswith('COLDWAR_FRA2_')]
    for key, count in Counter(custom_provider_list).items():
        require(count == 1, f'Duplicate scripted provider: {key} ({count})')
    variable_blocks = {'set_variable', 'set_temp_variable', 'add_to_variable', 'subtract_from_variable', 'multiply_variable', 'divide_variable', 'multiply_temp_variable', 'add_to_temp_variable', 'check_variable', 'clamp_variable', 'round_variable', 'set_array', 'add_to_array'}
    def calls(rows, parent=''):
        for row in rows:
            if row.key.startswith('COLDWAR_FRA2_') and row.value in ('yes', 'no') and parent not in variable_blocks:
                yield row.key
            yield from calls(row.children(), row.key)
    for rel, text in generated_scripts.items():
        for child, parent_key in walk_context(parsed[rel]):
            if child.key == '_bare':
                require(isinstance(child.value, str) and (child.value.startswith('FOCUS_FILTER_') or
                    parent_key == 'resources' and child.value == 'uranium'), f'Unassigned script token {child.value} in {rel}')
            if child.key == 'has_completed_focus' and str(child.value).startswith('COLDWAR_FRA2_'):
                require(child.value in expected, f'Unresolved focus requirement {child.value} in {rel}')
            if (child.key in ('has_idea', 'add_ideas', 'remove_ideas')
                    or child.key == 'idea' and parent_key == 'add_timed_idea') and str(child.value).startswith('COLDWAR_FRA2_'):
                require(child.value in defined_ideas, f'Unresolved custom idea {child.value} in {rel}')
            if child.key in ('custom_effect_tooltip', 'custom_cost_text', 'tooltip') and str(child.value).startswith('COLDWAR_FRA2_'):
                require(child.value in keys, f'Unresolved English tooltip {child.value} in {rel}')
            if child.key == 'set_country_flag' and child.children() and field(child.children(), 'days') is not None:
                require(float(field(child.children(), 'value', 0)) > 0, f'Timed flag requires a positive explicit value in {rel}')
            require(child.key not in ('add_timed_ideas', 'add_army_experience', 'add_navy_experience', 'add_air_experience', 'initial_focus'), f'Unsupported native API {child.key} in {rel}')
        if '/scripted_effects/' in rel or '/scripted_triggers/' in rel or '/national_focus/' in rel or '/on_actions/' in rel or '/decisions/' in rel:
            for key in calls(parsed[rel]):
                require(key in providers, f'Unresolved custom provider {key} in {rel}')
        forbidden_in_trigger = {'set_variable', 'set_temp_variable', 'add_to_variable', 'multiply_variable',
                                'add_ideas', 'add_timed_idea', 'remove_ideas', 'set_country_flag', 'clr_country_flag',
                                'add_building_construction', 'add_extra_state_shared_building_slots', 'add_tech_bonus',
                                'add_political_power', 'force_update_dynamic_modifier', 'modify_treasury_effect'}
        for block in walk(parsed[rel]):
            if block.key in ('limit', 'available', 'visible'):
                for child in walk(block.children()):
                    require(child.key not in forbidden_in_trigger, f'Effect {child.key} inside trigger {block.key} in {rel}')
    money = (ROOT / 'common/scripted_effects/00_money_system.txt').read_text(encoding='utf-8')
    require(money.count('COLDWAR_FRA2_add_weekly_expenses = yes') == 1, 'Single native expense integration')
    aggregator = next(n for n in nodes(money) if n.key == 'calculate_additional_expense_rate')
    require(any(n.key == 'COLDWAR_FRA2_add_weekly_expenses' for n in aggregator.children()), 'Expense hook must run in every payer country')
    for rel, text in generated_scripts.items():
        require(not re.search(r'\btreasury\s*[<>]=?\s*|\btreasury\s*=\s*\d', text), 'Unapproved treasury balance gate: ' + rel)
    counts = Counter(e['kind'] for n in design['nodes'] for e in n['effects'])
    slot_effects = [e for n in design['nodes'] for e in n['effects'] if e['kind'] == 'state_slots']
    require(len(slot_effects) == 2 and sum(int(e['amount']) for e in slot_effects) == 5, 'Standalone state slots should total five')
    require(sum(int(e['amount']) for n in design['nodes'] for e in n['effects'] if e['kind'] == 'building' and n.get('expansion_change') == 'new') == 32, 'Expansion building level count should be 32')
    require(sum(int(e.get('slots', 0)) for n in design['nodes'] for e in n['effects'] if e['kind'] == 'building' and n.get('expansion_change') == 'new') == 32, 'Every expansion building level should receive a shared slot')
    cid_keys = {'cid_tax', 'cid_cooperatives', 'cid_wholesale_cooperatives', 'cid_rural_networks'}
    cid_nodes = {n['key']: n for n in design['nodes'] if n['key'] in cid_keys}
    require(set(cid_nodes) == cid_keys, 'All four dated CID focuses are present')
    for key, node in cid_nodes.items():
        require(node.get('group') == 'right', 'CID focus remains in visible Right branch: ' + key)
        require(node.get('modifier_pool') == 'CID', 'CID focus uses isolated dated pool: ' + key)
        require(node.get('programme_activation_conditions') == [
            'nationalist_right_wing_populists_are_in_power = yes', 'date < 1972.10.5'],
            'CID party/date activation contract: ' + key)
        focus_text = generated_scripts[tree_rel]
        focus_node = focuses[node['id']]
        availability = next(n for n in focus_node.children() if n.key == 'available')
        available_text = focus_text[availability.start:availability.end]
        require('nationalist_right_wing_populists_are_in_power = yes' in available_text, 'Visible CID ruling-party gate: ' + key)
        require('date < 1972.10.5' in available_text, 'CID date gate: ' + key)
    effects_rel = 'common/scripted_effects/COLDWAR_FRA2_1970_effects.txt'
    effect_rows = parsed.get(effects_rel, [])
    cid_migration = next((n for n in effect_rows if n.key == 'COLDWAR_FRA2_migrate_CID_pool'), None)
    require(cid_migration is not None, 'CID pool save migration provider')
    if cid_migration is not None:
        cid_migration_text = generated_scripts[effects_rel][cid_migration.start:cid_migration.end]
        require('COLDWAR_FRA2_right_programme' in cid_migration_text and 'remove_dynamic_modifier' in cid_migration_text,
                'CID migration detaches stale Right pool before normal resync')
        forbidden_migration_effects = {'modify_treasury_effect', 'add_building_construction', 'add_extra_state_shared_building_slots',
            'add_tech_bonus', 'add_doctrine_cost_reduction', 'add_political_power', 'army_experience', 'navy_experience', 'air_experience',
            'add_ideas', 'add_idea', 'add_timed_idea', 'add_to_faction_opinion'}
        # Pool reconstruction may add earned modifier deltas; it must not replay any finite award.
        require(not any(n.key in forbidden_migration_effects for n in walk(cid_migration.children())),
                'CID migration must not replay finite focus rewards')
        rebuilt_vars = [n for n in walk(cid_migration.children()) if n.key == 'add_to_variable']
        require(all(n.children() and n.children()[0].key.startswith(('COLDWAR_FRA2_right_', 'COLDWAR_FRA2_CID_')) for n in rebuilt_vars),
                'CID migration variable additions must stay inside the rebuilt Right/CID pools')
    for node in design['nodes']:
        if node.get('expansion_change') != 'new':
            continue
        slot_effects_for_node = [e for e in node.get('effects', []) if e['kind'] == 'state_slots']
        for effect in slot_effects_for_node:
            require(effect.get('native_effect') == 'add_extra_state_shared_building_slots', 'Native state-slot effect: ' + node['key'])
            available = next(n for n in focuses[node['id']].children() if n.key == 'available')
            available_text = generated_scripts[tree_rel][available.start:available.end]
            for guard in (f"owns_state = {effect['state']}", f"controls_state = {effect['state']}", f"has_full_control_of_state = {effect['state']}"):
                require(guard in available_text, 'Standalone state-slot ownership/control gate: ' + node['key'] + '/' + guard)
            reward = next(n for n in focuses[node['id']].children() if n.key == 'completion_reward')
            reward_text = generated_scripts[tree_rel][reward.start:reward.end]
            require('add_extra_state_shared_building_slots = ' + str(effect['amount']) in reward_text,
                    'Standalone native state-slot reward and preview: ' + node['key'])
    fund_id = 'COLDWAR_FRA2P_regional_conversion'
    fund = next((d for d in design['decisions'] if d['id'] == fund_id), None)
    require(fund is not None, 'Regional Conversion Fund decision remains')
    if fund is not None:
        approved_fund = next(d for d in expansion_snapshot['decisions'] if d['id'] == fund_id)
        require(fund.get('effects') == approved_fund.get('effects'), 'Regional Conversion Fund cost/assets/research remain unchanged')
        expected_or = 'OR = { has_completed_focus = COLDWAR_FRA2_public_banks has_completed_focus = COLDWAR_FRA2_ps_conversion_boards }'
        require(expected_or in fund.get('runtime_guards', []), 'Regional Conversion Fund has exact alternate prerequisite')
        decisions_rel = 'common/decisions/COLDWAR_FRA2_1970_decisions.txt'
        decision_nodes = parsed.get(decisions_rel, [])
        emitted_fund = next((d for d in walk(decision_nodes) if d.key == fund_id), None)
        require(emitted_fund is not None, 'Regional Conversion Fund source block')
        if emitted_fund is not None:
            source_text = generated_scripts[decisions_rel][emitted_fund.start:emitted_fund.end]
            require('has_completed_focus = COLDWAR_FRA2_public_banks' in source_text and 'has_completed_focus = COLDWAR_FRA2_ps_conversion_boards' in source_text,
                    'Regional Conversion Fund availability and completion include both qualifying paths')
    for n in design['nodes']:
        for side in ('france', 'recipient') if n.get('offer') else ():
            counts.update(e['kind'] for e in n['offer'][side]['effects'])
    for decision in design.get('decisions', []):
        counts.update(e['kind'] for e in decision['effects'])
    payloads = [n['effects'] for n in design['nodes']]
    payloads += [n['offer'][side]['effects'] for n in design['nodes'] if n.get('offer') for side in ('france', 'recipient')]
    payloads += [d['effects'] for d in design.get('decisions', [])]
    for effects in payloads:
        for effect in effects:
            if effect['kind'] == 'modifier' and 'influence' in effect['key']:
                require(effect['value'] >= 0, 'Uncorrected negative influence trade-off: ' + effect['key'])
            if effect['kind'] == 'building':
                require(effect['slots'] == effect['amount'] and effect['slots_before_construction'], 'Building slot contract: ' + str(effect))
            if effect['kind'] in ('treasury_gdp', 'weekly_gdp_expense'):
                require(effect['base'] == 'gdp_total' and effect['payer'] == 'own_country', 'Own-GDP payment contract: ' + str(effect))
                if effect['kind'] == 'weekly_gdp_expense':
                    require(effect['divisor'] == 52, 'Weekly budget divisor: ' + str(effect))
    report = {'project': 'IMPERIA COLD WAR', 'scope': 'Installed source, approval, graph, references, encoding and generator contracts. Native tests recorded separately.',
              'focuses': len(focuses), 'offers': sum('offer' in n for n in design['nodes']),
              'approved_expansion_focuses': len(added_keys), 'expansion_building_levels': 32, 'expansion_building_slots': 32,
              'standalone_state_slots': 5, 'cid_pool_migration': 'one-time earned modifier rebuild; stale Right container detached before sync',
              'programmes': len(groups), 'localisation_keys': len(keys), 'effect_counts': dict(counts),
              'approved_sha256': manifest['approved_sha256'], 'approved_expansion_sha256': manifest['approved_expansion_sha256'], 'files_checked': len(manifest['files']),
              'approved_party_revision_sha256': manifest['approved_party_revision_sha256'],
              'issues': issues, 'passed': not issues}
    (HERE / 'VALIDATION.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return bool(issues)


if __name__ == '__main__':
    sys.exit(main())
