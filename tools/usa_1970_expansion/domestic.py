# IMPERIA COLD WAR — USA national and party programme implementation.
"""Emit only the owned USA domestic programme files and focus integration specs.

The approved design is the source of narrative, amounts and reward counts. Static
idea tiers replace programme modifiers instead of accumulating new copies. The
completion receipt owns setup assets; lifecycle reconciliation never calls setup.
"""
from __future__ import annotations

from collections import OrderedDict
from decimal import Decimal
import ast
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from usa_building_capacity import capacity_trigger
from focus_dates import patch_ready_triggers, strip_condition_dates

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DESIGN = ROOT / 'docs/design/usa_1970_expansion_20261024'
PREFIX = 'COLDWAR_USA_dom_'
MARKER = '# IMPERIA COLD WAR — USA national and party programmes.\n'

MODIFIERS = {
    'factory output': 'industrial_capacity_factory',
    'production efficiency growth': 'production_factory_efficiency_gain_factor',
    'consumer goods factor': 'consumer_goods_factor',
    'construction speed': 'production_speed_buildings_factor',
    'maximum production efficiency': 'production_factory_max_efficiency_factor',
    'tax collection efficiency': 'tax_gain_multiplier_modifier',
    'production efficiency retention': 'line_change_production_efficiency_factor',
    'education cost': 'education_cost_multiplier_modifier',
    'stability': 'stability_factor',
    'research speed': 'research_speed_factor',
    'nuclear energy generation': 'nuclear_energy_generation_modifier',
    'nuclear-reactor construction speed': 'production_speed_nuclear_reactor_factor',
    'energy consumption': 'energy_use_multiplier',
    'division organisation': 'army_org_factor',
    'army experience gain': 'experience_gain_army_factor',
    'training time': 'training_time_army_factor',
    'recruitable population factor': 'conscription_factor',
    'organisation regain': 'army_morale_factor',
    'mobilisation speed': 'mobilization_speed',
    'equipment cost': 'equipment_cost_multiplier_modifier',
    'encryption': 'encryption_factor',
    'intelligence agency upgrade time': 'agency_upgrade_time',
    'civilian intelligence': 'civilian_intel_factor',
    'supply consumption': 'supply_consumption_factor',
    'planning speed': 'planning_speed',
    'army fuel consumption': 'army_fuel_consumption_factor',
    'naval organisation': 'navy_org_factor',
    'naval experience gain': 'experience_gain_navy_factor',
    'naval personnel cost': 'navy_personnel_cost_multiplier_modifier',
    'convoy escort efficiency': 'convoy_escort_efficiency',
    'submarine detection': 'navy_submarine_detection_factor',
    'political power gain': 'political_power_factor',
    'drift defence': 'drift_defence_factor',
    'bureaucracy cost': 'bureaucracy_cost_multiplier_modifier',
    'war support': 'war_support_factor',
    'personnel cost': 'personnel_cost_multiplier_modifier',
}
PARTIES = {
    'Democratic Party is in power': 'western_liberals_are_in_power',
    'Republican Party is in power': 'western_conservatism_are_in_power',
}
PICTURES = {
    'Industry': 'USA_interiori', 'Civil priorities': 'research_bonus',
    'Energy': 'USA_energyi', 'Force structure': 'USA_armyi',
    'Intelligence': 'department_of_defense', 'Army doctrine': 'USA_armyi',
    'Naval priorities': 'USA_navyi', 'Civil rights': 'USA_capitol_building',
    'Foreign doctrine': 'USA_capitol_building',
}
FOCUS_ICONS = {
    'Industry': 'factory_planning', 'Civil priorities': 'economic_internet',
    'Energy': 'oil_green', 'Force structure': 'Generic_American_Soldier2',
    'Intelligence': 'examine_foreign_laws', 'Army doctrine': 'army_mobilisation',
    'Naval priorities': 'naval_doctrine', 'Civil rights': 'pass_legislation',
    'Foreign doctrine': 'diplomatic_treaty',
}


def number(value):
    return format(Decimal(str(value)).normalize(), 'f')


def key(focus_id):
    return focus_id.removeprefix('USA_1970_').removeprefix('USA_X_')


def done(focus_id):
    return PREFIX + 'done_' + key(focus_id)


def queued(focus_id):
    return PREFIX + 'pending_' + key(focus_id)


def block(name, lines, tabs=0):
    pad = '\t' * tabs
    return pad + name + ' = {\n' + ''.join(pad + '\t' + x + '\n' for x in lines) + pad + '}\n'


def ast_rows(nodes):
    """Preserve frozen native predicates, including operators and OR grouping."""
    return [k + ' ' + op + ' ' + ('{ ' + ' '.join(ast_rows(v)) + ' }' if isinstance(v, list) else str(v)) for k, op, v in nodes]


def parser():
    path = ROOT / 'tools/israel_1970/validate_content.py'
    module = ast.parse(path.read_text(encoding='utf-8-sig'))
    ns = {'re': re}
    names = {'tokens', 'parse', 'first', 'values', 'walk'}
    exec(compile(ast.Module(body=[n for n in module.body if isinstance(n, ast.FunctionDef) and n.name in names], type_ignores=[]), str(path), 'exec'), ns)
    return ns['parse'], ns['first']


def write(relative, text, localisation=False):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if not localisation:
        depth, formatted = 0, []
        for line in text.splitlines():
            clean = line.strip()
            indentation = depth - (1 if clean.startswith('}') else 0)
            formatted.append('\t' * max(indentation, 0) + clean if clean else '')
            if not clean.startswith('#'):
                depth += clean.count('{') - clean.count('}')
            assert depth >= 0, (relative, clean)
        assert depth == 0, relative
        text = '\n'.join(formatted) + '\n'
    path.write_text(text, encoding='utf-8-sig' if localisation else 'utf-8', newline='\n')


def modifier_rows(raw):
    result = OrderedDict()
    for term in raw.split(';'):
        match = re.fullmatch(r'\s*(.*?)\s+([+-]\d+(?:\.\d+)?)%\s*', term)
        if not match:
            raise ValueError(('unmapped programme row', term))
        label, amount = match.groups()
        result[MODIFIERS[label.lower()]] = Decimal(amount) / 100
    return result


def programme_row(node):
    for row in node['effects']:
        match = re.match(r'(Add|Modify) (.*?): (.*)', row)
        if match and not match[2].startswith('Retrofit Adjustment'):
            return match[1], match[2], modifier_rows(match[3])
    return None


def build():
    proposal = json.loads((DESIGN / 'proposal.json').read_text(encoding='utf-8'))
    titles_path = HERE / 'focus_titles.json'
    titles = json.loads(titles_path.read_text(encoding='utf-8'))['titles'] if titles_path.exists() else {}
    inventory = json.loads((DESIGN / 'current_inventory.json').read_text(encoding='utf-8'))
    original = {n['id']: n for n in inventory['focuses']}
    nodes = [n for n in proposal['nodes'] if 'offer' not in n]
    assert len(nodes) == 49, len(nodes)
    by_id = {n['id']: n for n in nodes}
    groups = OrderedDict()
    membership = {}
    for n in nodes:
        row = programme_row(n)
        if row and row[0] == 'Add':
            groups[row[1]] = dict(root=n, nodes=[n], deltas=[row[2]])
            membership[n['id']] = row[1]
        elif row:
            assert row[1] in groups, row
            groups[row[1]]['nodes'].append(n)
            groups[row[1]]['deltas'].append(row[2])
            membership[n['id']] = row[1]
    for name, group in groups.items():
        group['ideas'] = [PREFIX + key(group['root']['id']) + '_s' + str(i) for i in range(len(group['nodes']))]
        group['party'] = next((PARTIES[r] for r in group['root']['requirements'] if r in PARTIES), None)
        group['law'] = {'USA_1970_D1': 'volunteer_army', 'USA_1970_D2': 'draft_army'}.get(group['root']['id'])

    # Each continuation has exactly one linear ownership chain in the approved
    # catalogue. Its spirit tier includes every earned previous delta.
    for n in nodes:
        n['_party'] = next((PARTIES[r] for r in n['requirements'] if r in PARTIES), None)
        n['_cost'] = next((Decimal(re.search(r'-\$(\d+(?:\.\d+)?)', s)[1]) for s in n['effects'] if s.startswith('Treasury:')), Decimal(0))
        n['_build'] = None
        for row in n['effects']:
            match = re.search(r'(\d+) (civilian factor(?:y|ies)|office levels?|infrastructure levels?)', row)
            if match:
                quantity, kind = match.groups()
                building = 'industrial_complex' if kind.startswith('civilian') else 'offices' if kind.startswith('office') else 'infrastructure'
                n['_build'] = (building, int(quantity))
        n['_parent'] = None
        if n['id'] in membership:
            g = groups[membership[n['id']]]
            index = g['nodes'].index(n)
            n['_group'] = g
            n['_stage'] = index
            if index:
                n['_parent'] = g['nodes'][index - 1]['id']
        elif n['id'] == 'USA_X_test_ranges':
            n['_parent'] = 'USA_X_army_precision'

    def state_limit(n):
        building, quantity = n['_build']
        maximum = 6 if building == 'infrastructure' else 50
        result = ['is_core_of = USA', 'is_owned_and_controlled_by = ROOT']
        if n['id'] == 'USA_1970_E1':
            result.append('OR = { state = 771 state = 775 state = 777 state = 778 }')
        elif n['id'] == 'USA_1970_E2':
            result.append('OR = { state = 769 state = 770 state = 778 state = 800 state = 809 state = 811 }')
        # Native state dynamic variable, documented in installed HOI4
        # dynamic_variables_documentation.md. Capacity is amount-aware and
        # independent of the additional shared slots granted by the transaction.
        result += [f'check_variable = {{ var = building_level@{building} value = {maximum - quantity} compare = less_than_or_equals }}',
                   capacity_trigger(building,quantity)]
        return result

    def active_parent(n):
        parent = n['_parent']
        if not parent:
            return []
        g = groups[membership[parent]]
        return ['OR = { ' + ' '.join('has_idea = ' + idea for idea in g['ideas']) + ' }']

    localisation = OrderedDict()
    def loc(k, v):
        assert '\u2013' not in v and '\u2014' not in v, (k, v)
        assert k not in localisation, k
        localisation[k] = v

    ideas = []
    for name, g in groups.items():
        totals = OrderedDict()
        for stage, idea in enumerate(g['ideas']):
            for modifier, amount in g['deltas'][stage].items():
                totals[modifier] = totals.get(modifier, Decimal(0)) + amount
            picture = PICTURES.get(g['root']['module'], 'USA_capitol_building')
            rows = [f'picture = {picture}', 'allowed = { original_tag = USA tag = USA }', 'allowed_civil_war = { always = no }', 'cancel = { NOT = { tag = USA } }', 'removal_cost = -1']
            mods = [f'{k} = {number(v)}' for k, v in totals.items()]
            if g['root']['id'] == 'USA_X_nuclear_priority':
                mods.append('custom_modifier_tooltip = COLDWAR_USA_dom_nuclear_weekly_tt')
            rows.append(block('modifier', mods).rstrip())
            ideas.append(block(idea, rows))
            loc(idea, name)
            loc(idea + '_desc', g['root']['description'])
    ideas += [block(PREFIX + 'retrofit_adjustment', ['picture = USA_energyi', 'allowed = { original_tag = USA tag = USA }', 'allowed_civil_war = { always = no }', 'cancel = { NOT = { tag = USA } }', 'modifier = { production_speed_buildings_factor = -0.02 }']),
              block(PREFIX + 'export_guarantees', ['picture = USA_interiori', 'allowed = { original_tag = USA tag = USA }', 'allowed_civil_war = { always = no }', 'cancel = { NOT = { tag = USA } }', 'modifier = { resource_export_multiplier_modifier = 0.05 tax_gain_multiplier_modifier = -0.01 }'])]
    loc(PREFIX + 'retrofit_adjustment', 'Retrofit Adjustment')
    loc(PREFIX + 'retrofit_adjustment_desc', 'Industrial retrofits divert construction teams toward existing plants while the first energy-saving installations are completed.')
    loc(PREFIX + 'export_guarantees', 'Export Credit Guarantees')
    loc(PREFIX + 'export_guarantees_desc', 'Federal credit guarantees support overseas contracts while placing part of the commercial risk on the public balance sheet.')
    loc('COLDWAR_USA_dom_nuclear_weekly_tt', 'Weekly programme expense: §R-$0.03 billion§!')

    def benefits(n, preview=False):
        result = []
        if n['_cost']:
            result += [f'set_temp_variable = {{ treasury_change = -{number(n["_cost"])} }}', 'modify_treasury_effect = yes']
        if n['id'] == 'USA_1970_D1':
            result += ['set_volunteer_army_effect = yes']
        elif n['id'] == 'USA_1970_D2':
            result += ['set_draft_army_effect = yes']
        if n['id'] in membership:
            g, index = n['_group'], n['_stage']
            idea = g['ideas'][index]
            if preview:
                result.append(f'swap_ideas = {{ remove_idea = {g["ideas"][index-1]} add_idea = {idea} }}' if index else 'add_ideas = ' + idea)
            else:
                # Reconcile chooses the final tier from earned receipts. No
                # source-specific modifier is added through native US variables.
                pass
        if n['id'] == 'USA_X_efficiency_priority':
            result.append('add_timed_idea = { idea = ' + PREFIX + 'retrofit_adjustment days = 730 }')
        if n['_build']:
            building, quantity = n['_build']
            state = state_limit(n)
            result.append(block('random_owned_state', [block('limit', state).rstrip(), f'add_extra_state_shared_building_slots = {quantity}', f'add_building_construction = {{ type = {building} level = {quantity} instant_build = yes }}']).rstrip())
        bonus_index = 0
        for row in n['effects']:
            if 'research bonus' in row:
                count = int(re.search(r'(\d+) x', row)[1])
                if 'destroyer' in row:
                    categories = [('CAT_destroyers', 1), ('CAT_submarines', 1)]
                elif 'aircraft' in row:
                    categories = [('CAT_aircraft', 1), ('CAT_electronics', 1)]
                elif 'nuclear' in row:
                    categories = [('CAT_nuclear_reactors', count)]
                elif 'electronics' in row:
                    categories = [('CAT_electronics', count)]
                else:
                    assert 'industry' in row, row
                    categories = [('CAT_industry', count)]
                for category, uses in categories:
                    bonus_index += 1
                    bonus_name = PREFIX + key(n['id']) + '_research_' + str(bonus_index)
                    result.append(f'add_tech_bonus = {{ name = {bonus_name} bonus = 0.5 uses = {uses} category = {category} }}')
                    if bonus_name not in localisation:
                        loc(bonus_name, n['name'])
            if 'doctrine cost reduction' in row:
                match = re.search(r'(\d+) x 50% (land|air|naval) doctrine', row)
                assert match, row
                uses, category = match.groups()
                bonus_name = PREFIX + key(n['id']) + '_' + category + '_doctrine'
                result.append(f'add_doctrine_cost_reduction = {{ name = {bonus_name} cost_reduction = 0.5 uses = {uses} category = {category}_doctrine }}')
                if bonus_name not in localisation:
                    loc(bonus_name, n['name'])
            if re.match(r'(Army|Air) experience:', row):
                kind, value = row.split(':')
                result.append(('army_experience' if kind == 'Army experience' else 'air_experience') + ' = ' + str(int(value)))
            if row.startswith('Unlock decision:'):
                result.append('unlock_decision_tooltip = ' + PREFIX + 'export_credit_guarantees')
        return result

    triggers = []
    effects = []
    specs = []
    pending_decisions = []
    for n in nodes:
        suffix = key(n['id'])
        ready = PREFIX + 'ready_' + suffix
        capacity = PREFIX + 'capacity_' + suffix
        apply = PREFIX + 'apply_' + suffix
        complete = PREFIX + 'complete_' + suffix
        preview = PREFIX + 'preview_' + suffix
        available = []
        if n['_party']:
            available.append(n['_party'] + ' = yes')
        if n['id'] == 'USA_1970_D2':
            available.append('NOT = { has_doctrine = mdcw_all_volunteer_force }')
        available += active_parent(n)
        if n['_build']:
            triggers.append(block(capacity, [block('any_owned_state', state_limit(n)).rstrip()]))
            tooltip = PREFIX + 'capacity_' + suffix + '_tt'
            kind, qty = n['_build']
            noun = {'industrial_complex': 'civilian factory', 'offices': 'office', 'infrastructure': 'infrastructure'}[kind]
            loc(tooltip, f'An eligible US core state is owned and controlled by the United States and has space for {qty} {noun} level' + ('s.' if qty != 1 else '.'))
            available.append(f'custom_trigger_tooltip = {{ tooltip = {tooltip} {capacity} = yes }}')
        ready_conditions = ['original_tag = USA', 'tag = USA', 'IMP_is_1970_scenario = yes',
                            f'has_country_flag = {queued(n["id"])}',
                            f'NOT = {{ has_country_flag = {done(n["id"])} }}']
        if n['_party']:
            ready_conditions.append(n['_party'] + ' = yes')
        if n['id'] == 'USA_1970_D2':
            ready_conditions.append('NOT = { has_doctrine = mdcw_all_volunteer_force }')
        ready_conditions += active_parent(n)
        if n['_parent']:
            ready_conditions.append('has_country_flag = ' + done(n['_parent']))
        for excluded in n['mutually_exclusive']:
            if excluded in by_id:
                ready_conditions.append('NOT = { has_country_flag = ' + done(excluded) + ' }')
        for parents in n['prerequisites']:
            ready_conditions.append('OR = { ' + ' '.join('has_completed_focus = ' + p for p in parents) + ' }')
        if n['status'] == 'Rework':
            ready_conditions += ast_rows(original[n['id']]['available'])
        if n['_build']:
            ready_conditions.append(capacity + ' = yes')
        triggers.append(block(ready, ready_conditions))
        display = benefits(n, preview=True)
        effects.append(block(preview, display))
        institutional = []
        if n['id'] == 'USA_1970_D1':
            institutional = ['set_country_flag = USA_1970_force_model_volunteer']
        elif n['id'] == 'USA_1970_D2':
            institutional = ['set_country_flag = USA_1970_force_model_selective_service']
        elif n['id'] == 'USA_1970_D3':
            institutional = ['set_country_flag = USA_1970_covert_oversight']
        elif n['id'] == 'USA_1970_D4':
            institutional = ['set_country_flag = USA_1970_covert_freedom']
        execution = benefits(n) + [f'set_country_flag = {done(n["id"])}', f'clr_country_flag = {queued(n["id"])}'] + institutional + [PREFIX + 'reconcile = yes']
        effects.append(block(apply, [block('if', ['limit = { ' + ready + ' = yes }'] + execution).rstrip()]))
        effects.append(block(complete, [block('if', ['limit = { original_tag = USA tag = USA IMP_is_1970_scenario = yes NOT = { has_country_flag = ' + done(n['id']) + ' } }', f'set_country_flag = {queued(n["id"])}', apply + ' = yes']).rstrip()]))
        completion = f'effect_tooltip = {{ {preview} = yes }}\nhidden_effect = {{ {complete} = yes }}'
        specs.append(dict(id=n['id'], available='\n'.join(available), completion_reward=completion,
                          icon=FOCUS_ICONS.get(n['module'], 'pass_legislation'), cost=number(Decimal(str(n['days'])) / 7),
                          name=titles.get(n['id'], n['name']), description=n['description'], apply_effect=apply, preview_effect=preview,
                          completion_effect=complete, done_flag=done(n['id']), pending_flag=queued(n['id']),
                          exclusive=n['mutually_exclusive'], prerequisites=n['prerequisites'],
                          programme_ideas=n['_group']['ideas'] if '_group' in n else [], party_trigger=n['_party']))
        decision = PREFIX + 'enact_' + suffix
        pending_decisions.append(block(decision, ['icon = GFX_decision_generic_political_discourse', 'cost = 0',
            f'visible = {{ has_country_flag = {queued(n["id"])} NOT = {{ has_country_flag = {done(n["id"])} }} }}',
            f'available = {{ {ready} = yes }}', f'complete_effect = {{ effect_tooltip = {{ {preview} = yes }} hidden_effect = {{ {apply} = yes }} }}', 'ai_will_do = { factor = 5 }']))
        loc(decision, 'Enact ' + n['name'])
        loc(decision + '_desc', n['description'])
        if n['status'] != 'Rework':
            loc(n['id'], titles.get(n['id'], n['name']))
            loc(n['id'] + '_desc', n['description'])

    # Apply only the highest earned tier. Off-party programmes are removed, but
    # their earned receipts survive so returning governments recover modifiers.
    reconcile = []
    for name, g in groups.items():
        branches = []
        for stage in reversed(range(len(g['nodes']))):
            n, idea = g['nodes'][stage], g['ideas'][stage]
            terms = [f'has_country_flag = {done(n["id"])}']
            if stage:
                terms += [f'has_country_flag = {done(previous["id"])}' for previous in g['nodes'][:stage]]
            if g['party']:
                terms.append(g['party'] + ' = yes')
            if g['law']:
                terms.append('has_idea = ' + g['law'])
            if g['root']['id'] == 'USA_1970_D2':
                terms.append('NOT = { has_doctrine = mdcw_all_volunteer_force }')
            grant = [f'if = {{ limit = {{ has_idea = {other} }} remove_ideas = {other} }}' for other in g['ideas'] if other != idea]
            grant += [f'if = {{ limit = {{ NOT = {{ has_idea = {idea} }} }} add_ideas = {idea} }}']
            branches.append(block('if' if not branches else 'else_if', ['limit = { ' + ' '.join(terms) + ' }'] + grant).rstrip())
        branches.append(block('else', [f'if = {{ limit = {{ has_idea = {idea} }} remove_ideas = {idea} }}' for idea in g['ideas']]).rstrip())
        reconcile.extend(branches)
    reconcile += [PREFIX + 'recalculate_weekly_expense = yes']
    effects.append(block(PREFIX + 'reconcile', [block('if', ['limit = { original_tag = USA tag = USA IMP_is_1970_scenario = yes }'] + reconcile).rstrip()]))
    nuclear_ideas = groups['Standard Reactor Programme']['ideas']
    effects.append(block(PREFIX + 'recalculate_weekly_expense', ['set_variable = { COLDWAR_USA_domestic_weekly_expense = 0 }',
        'if = { limit = { original_tag = USA tag = USA IMP_is_1970_scenario = yes OR = { ' + ' '.join('has_idea = ' + i for i in nuclear_ideas) + ' } } set_variable = { COLDWAR_USA_domestic_weekly_expense = 0.03 } }']))
    effects.append(block(PREFIX + 'add_expense_rate', [PREFIX + 'recalculate_weekly_expense = yes', 'add_to_variable = { additional_expenses_rate = COLDWAR_USA_domestic_weekly_expense }']))

    # Migrate only the unbounded persistent US policy-variable contributions.
    # Historic one-time money, PP, stability, assets and random/capped faction or
    # Congress outcomes cannot be reconstructed exactly and are not replayed.
    parse, first = parser()
    bridge = {k: v for k, _, v in parse((ROOT / 'common/scripted_effects/mdcw_1970_USA_native_api_bridge.txt').read_text(encoding='utf-8-sig'))}
    migrate = []
    migration_rows = []
    for n in nodes:
        if n['status'] != 'Rework':
            continue
        reverse = []
        temp = None
        for command, _, value in original[n['id']]['completion_reward']:
            if command == 'set_temp_variable' and value[0][0] == 'temp_change':
                temp = Decimal(value[0][2])
            elif command.startswith('USA_change_'):
                assert command in bridge, command
                add = first(bridge[command], 'add_to_variable')
                assert add and add[0][2] == 'temp_change', command
                reverse.append(f'add_to_variable = {{ {add[0][0]} = {number(-temp)} }}')
                migration_rows.append(dict(focus=n['id'], variable=add[0][0], removed_delta=number(temp)))
        reverse += [f'set_country_flag = {done(n["id"])}']
        migrate.append(block('if', [f'limit = {{ has_completed_focus = {n["id"]} NOT = {{ has_country_flag = {done(n["id"])} }} }}'] + reverse).rstrip())
    effects.append(block(PREFIX + 'initialize', [block('if', ['limit = { original_tag = USA tag = USA IMP_is_1970_scenario = yes NOT = { has_country_flag = COLDWAR_USA_domestic_v1_initialized } }'] + migrate + ['set_country_flag = COLDWAR_USA_domestic_v1_initialized', 'force_update_dynamic_modifier = yes']).rstrip(), PREFIX + 'reconcile = yes']))

    loc(PREFIX + 'pending_category', 'National Programme Enactment')
    loc(PREFIX + 'pending_category_desc', 'Congressional measures and national programmes can be enacted when their political and territorial requirements are met.')
    loc(PREFIX + 'credit_category', 'Export Credit Policy')
    loc(PREFIX + 'credit_category_desc', 'Federal guarantees help American firms finance overseas contracts. Public credit support must be weighed against its fiscal cost.')
    loc(PREFIX + 'export_credit_guarantees', 'Export Credit Guarantees')
    loc(PREFIX + 'export_credit_guarantees_desc', 'Guarantees can improve the return on American exports while reducing immediate tax receipts. Each authorisation covers a limited period of commercial support.')
    export_active = 'OR = { ' + ' '.join('has_idea = ' + i for i in groups['Competitive Investment Zones']['ideas']) + ' }'
    export_ready = ['original_tag = USA', 'tag = USA', 'IMP_is_1970_scenario = yes', 'has_country_flag = ' + done('USA_X_export_credit'), export_active,
                    'NOT = { has_idea = ' + PREFIX + 'export_guarantees }', 'check_variable = { var = treasury value = 5 compare = greater_than_or_equals }']
    triggers.append(block(PREFIX + 'export_credit_ready', export_ready))
    export_terms = ['set_temp_variable = { treasury_change = -5 }', 'modify_treasury_effect = yes', 'add_timed_idea = { idea = ' + PREFIX + 'export_guarantees days = 180 }']
    export_runtime = block('if', ['limit = { ' + PREFIX + 'export_credit_ready = yes }'] + export_terms).rstrip() + '\nelse = { add_political_power = 75 }'
    export_decision = block(PREFIX + 'export_credit_guarantees', ['icon = GFX_decision_generic_factory', 'cost = 75', 'days_re_enable = 365',
        'visible = { has_country_flag = ' + done('USA_X_export_credit') + ' }',
        'available = { ' + export_active + ' NOT = { has_idea = ' + PREFIX + 'export_guarantees } check_variable = { var = treasury value = 5 compare = greater_than_or_equals } }',
        block('complete_effect', [block('effect_tooltip', export_terms).rstrip(), block('hidden_effect', [export_runtime]).rstrip()]).rstrip(), 'ai_will_do = { factor = 1 }'])
    categories = [block(PREFIX + 'pending_category', ['icon = GFX_decision_category_usa_congress', 'allowed = { original_tag = USA }', 'visible = { IMP_is_1970_scenario = yes OR = { ' + ' '.join('has_country_flag = ' + queued(n['id']) for n in nodes) + ' } }']),
                  block(PREFIX + 'credit_category', ['icon = GFX_decision_category_economic', 'allowed = { original_tag = USA }', 'visible = { IMP_is_1970_scenario = yes has_country_flag = ' + done('USA_X_export_credit') + ' }'])]

    write('common/ideas/COLDWAR_USA_1970_programmes.txt', MARKER + block('ideas', [block('country', [x.rstrip() for x in ideas]).rstrip()]))
    write('common/scripted_effects/COLDWAR_USA_1970_programmes.txt', MARKER + '\n'.join(effects))
    write('common/scripted_triggers/COLDWAR_USA_1970_programmes.txt', patch_ready_triggers(MARKER + '\n'.join(triggers)))
    write('common/decisions/COLDWAR_USA_1970_programmes.txt', MARKER + block(PREFIX + 'pending_category', [x.rstrip() for x in pending_decisions]) + block(PREFIX + 'credit_category', [export_decision.rstrip()]))
    write('common/decisions/categories/COLDWAR_USA_1970_programmes.txt', MARKER + '\n'.join(categories))
    text = 'l_english:\n' + MARKER + ''.join(' ' + k + ':0 ' + json.dumps(v, ensure_ascii=False) + '\n' for k, v in localisation.items())
    write('localisation/english/COLDWAR_USA_1970_programmes_l_english.yml', text, localisation=True)
    for spec in specs:
        spec['available'] = strip_condition_dates(spec['available'])
    (HERE / 'domestic_focus_specs.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR', focuses=specs, hooks=dict(initialize=PREFIX + 'initialize', reconcile=PREFIX + 'reconcile', calculate_expense=PREFIX + 'recalculate_weekly_expense', append_expense=PREFIX + 'add_expense_rate', weekly_expense_variable='COLDWAR_USA_domestic_weekly_expense'), migration_removed_deltas=migration_rows), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {'focuses': len(nodes), 'programme_families': len(groups), 'idea_tiers': sum(len(g['ideas']) for g in groups.values()), 'localisation_keys': len(localisation), 'migration_deltas': len(migration_rows)}


if __name__ == '__main__':
    print(json.dumps(build()))
