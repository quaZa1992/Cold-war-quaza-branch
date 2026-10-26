# IMPERIA CW — Cold War: israel 1970 — validate policy.
"""Validate the Israel 1970 policy compiler output and key policy invariants.

This is a static/compiler-output and small state-transition simulation. It does
not claim to emulate the HOI4 engine. Run after the policy compiler has emitted
english_design.json['policy_expansion'] and the ISR70_policy_* script files.
"""
from pathlib import Path
import argparse
import itertools
import json
import re
import sys

from script_format import read

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DESIGN_PATH = HERE / 'policy_design.json'
EXPORT_PATH = HERE / 'english_design.json'
EFFECT_PATH = ROOT / 'common/scripted_effects/ISR70_policy_effects.txt'
TRIGGER_PATH = ROOT / 'common/scripted_triggers/ISR70_policy_triggers.txt'
DYNAMIC_PATH = ROOT / 'common/dynamic_modifiers/ISR70_policy_dynamic_modifiers.txt'
DECISION_PATH = ROOT / 'common/decisions/ISR70_policy_decisions.txt'
EVENT_PATH = ROOT / 'events/ISR70_policy_events.txt'
IDEA_PATH = ROOT / 'common/ideas/ISR70_ideas.txt'

ALIASES = {'citizen_review': 'arab_citizens', 'equal_services': 'equal_local_services',
           'municipal_self': 'local_autonomy'}
ERRORS = []
CHECKS = []


def check(condition, message):
    CHECKS.append(message)
    if not condition:
        ERRORS.append(message)


def focus_id(key):
    return 'ISR70_' + ALIASES.get(key, key)


def direct(block, key):
    return [value for name, op, value in block if name == key and op == '=']


def walk(block):
    for name, op, value in block:
        yield name, op, value
        if isinstance(value, list):
            yield from walk(value)


def descendants(block, key):
    for name, op, value in block:
        if name == key and isinstance(value, list):
            yield value
        if isinstance(value, list):
            yield from descendants(value, key)


def scalar(block, key, default=None):
    return next((v for v in direct(block, key) if not isinstance(v, list)), default)


def block_map(ast):
    return {name: value for name, op, value in walk(ast)
            if op == '=' and isinstance(value, list)}


def normalized(text):
    return re.sub(r'\s+', ' ', text).strip()


def named_block_text(source, key, *, event_id=None):
    needle = 'id = ' + event_id if event_id else key + ' = {'
    marker = source.find(needle)
    if marker < 0:
        return ''
    start = source.rfind('country_event = {', 0, marker) if event_id else marker
    if start < 0:
        return ''
    opening = source.find('{', start)
    depth = 0
    quoted = False
    escaped = False
    for i in range(opening, len(source)):
        char = source[i]
        if quoted:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                return source[start:i + 1]
    return ''


def focus_reachable(nodes, excluded=frozenset()):
    """Evaluate focus prerequisites using HOI's OR-of-AND rows."""
    completed = set()
    while True:
        added = set()
        for node in nodes:
            key = node['id']
            if key in completed or key in excluded:
                continue
            prerequisites = node.get('prerequisites', [])
            if all(any(parent in completed for parent in row) for row in prerequisites):
                added.add(key)
        if not added:
            return completed
        completed.update(added)


def reserve_budget(gdp, share, treasury):
    amount = gdp * share
    if treasury < amount:
        return None, treasury
    return amount, treasury - amount


def finish_project(reserved, treasury, still_valid):
    """Model compiler callback: commit on valid completion, exact refund otherwise."""
    return treasury if still_valid else treasury + reserved


def simulate_transfer(source_population, target_population, cap, years):
    """Monthly capped migration with equal source loss and target gain."""
    remaining = min(cap, source_population)
    initial_total = source_population + target_population
    monthly = cap / (years * 12)
    moved = 0
    for _ in range(years * 12):
        amount = min(monthly, remaining, source_population)
        source_population -= amount
        target_population += amount
        remaining -= amount
        moved += amount
    assert abs(source_population + target_population - initial_total) < 1e-7
    assert moved <= cap + 1e-7 and source_population >= -1e-7
    return source_population, target_population, moved


def simulate_status_switch(current, chosen, known, persistent):
    """Apply replace semantics while retaining explicitly persistent harm."""
    assert chosen in known
    return {chosen} | (set(current) & set(persistent))


def check_source_design(design, metadata):
    branches = design['branches']
    policy_nodes = [n for b in branches for n in b.get('common', [])]
    policy_nodes += [n for b in branches for p in b.get('paths', []) for n in p.get('nodes', [])]
    ids = [n['id'] for n in policy_nodes]
    check(len(ids) == len(set(ids)), 'policy design contains duplicate focus keys')
    check(len(ids) == 77, f'expected 77 design keys, found {len(ids)}')

    metadata_nodes = {n['id']: n for n in metadata['nodes']}
    missing = {focus_id(k) for k in ids} - metadata_nodes.keys()
    check(not missing, f'focus metadata missing policy nodes: {sorted(missing)}')
    if missing:
        return

    for key in ids:
        n = metadata_nodes[focus_id(key)]
        check(n.get('policy_extension') is True and n.get('policy_key') == key,
              f'policy node marker/key mismatch: {key}')
        check(bool(n.get('policy_effect')) and n.get('reward') == n.get('policy_effect') + ' = yes',
              f'focus completion effect is not wired: {key}')

    reachable = focus_reachable(metadata['nodes'])
    check(reachable == set(metadata_nodes),
          f'focus graph has unreachable or cyclic nodes: {sorted(set(metadata_nodes)-reachable)[:12]}')
    # Enumerate mutually exclusive selections per choice_group. This validates
    # each option survives its real prerequisite graph when competing siblings
    # are removed, instead of only checking that the unfiltered graph is acyclic.
    for branch in branches:
        lanes = branch.get('paths', [])
        for lane in lanes:
            lane_keys = {focus_id(n['id']) for n in lane.get('nodes', [])}
            siblings = {focus_id(n['id']) for other in lanes if other is not lane
                        for n in other.get('nodes', [])}
            selected_reach = focus_reachable(metadata['nodes'], frozenset(siblings))
            check(lane_keys <= selected_reach,
                  f'focus OR-route is not reachable: {branch["id"]}/{lane["id"]}')

    expected_aliases = metadata.get('policy_expansion', {}).get('focus_aliases', ALIASES)
    check(expected_aliases == ALIASES, 'compiler focus aliases changed unexpectedly')


def check_domestic_values():
    source = (HERE / 'policy_domestic.py').read_text(encoding='utf-8')
    expected = {
        'office worker deltas': ['offices_worker_requirement_modifier": -.02',
                                 'offices_worker_requirement_modifier": -.03',
                                 'offices_worker_requirement_modifier": -.03',
                                 'offices_worker_requirement_modifier": -.02',
                                 'offices_worker_requirement_modifier": -.04'],
        'office productivity': ['"offices_productivity": .03', '"offices_productivity": .05'],
        'building speed': ['"production_speed_offices_factor": .05', '"production_speed_offices_factor": .10'],
        'credit outcomes': ['"receiving_investment_cost_modifier": -.05',
                            '"mdcw_cw_market_exposure": .05'],
    }
    for label, tokens in expected.items():
        check(all(token in source for token in tokens), f'approved finance values changed: {label}')
    check('NOT = { has_country_flag = ISR70_us_military_agreement }' not in source,
          'civilian export credit was incorrectly blocked by military cooperation')
    check('repeatable=True, cooldown=360' in source and 'cost=50' in source,
          'declined export-credit request lacks repeatable 50 PP / 360 day retry')
    check('has_country_flag = ISR70_policy_export_credit_accepted' in source,
          'dependent international credit effects lack an acceptance gate')
    check(r'set_temp_variable = { temp_opinion = 10 }\nchange_industrial_conglomerates_opinion = yes' in source,
          'industrial-conglomerate opinion does not follow the MD temp_opinion API')
    check(all(token in source for token in ('api.money(.003)', 'api.money(.002)',
                                             'api.money(.004)', 'api.money(.006)',
                                             'api.money(.005)')),
          'one-time GDP expenses do not use the compiler affordability/payment helper')
    project_budget = {'equal_services': '.006', 'equal_access': '.012',
                      'municipal_pacts': '.01', 'preferential_allocations': '.005',
                      'restricted_employment': '.012', 'development_offices': '.012',
                      'industrial_credit': '.012', 'export_services': '.012'}
    for key, value in project_budget.items():
        pattern = r'api\.project\(\s*["\']' + re.escape(key) + r'["\'].*?,\s*' + re.escape(value) + r'(?:\s|,)'
        check(re.search(pattern, source, re.S) is not None,
              f'approved project reservation changed: {key} expected {float(value)*100:.3f}% GDP')
    check(abs((.004 + .006 + .012) - .022) < 1e-12,
          'domestic-bond finance route cash-spend sum changed')
    check(abs((.004 + .006 + .005 + .012) - .027) < 1e-12,
          'bank finance route cash-spend sum changed')
    check(abs((.004 + .006 + .006 + .012) - .028) < 1e-12,
          'international finance route cash-spend sum changed')


def check_design_mechanics(design):
    occupation = next(b for b in design['branches'] if b['id'] == 'occupation')
    rules = occupation.get('status_rules', {})
    regimes = set(rules.get('exclusive_regimes', []))
    check(regimes == {'equal_civil', 'occupation_special', 'kach_special'},
          'occupation status packages are not an exclusive three-way choice')
    check('Preserve' in ' '.join(rules.get('preserve', [])) or bool(rules.get('preserve')),
          'status replacement does not preserve non-status history')
    check(rules.get('factory_access_cap') == 1.0, 'status switch lacks a bounded factory-access cap')

    transfers = [n['population_transfer'] for b in design['branches']
                 for n in b.get('common', []) + [x for p in b.get('paths', []) for x in p.get('nodes', [])]
                 if n.get('population_transfer')]
    check(bool(transfers), 'no capped population transfers are described')
    for transfer in transfers:
        check(transfer.get('voluntary') is True and transfer.get('cap', 0) > 0 and transfer.get('years', 0) > 0,
              f'population movement is not bounded and voluntary: {transfer}')
        check(transfer.get('source') == 'ISR_core_states' and transfer.get('target') not in ('ISR_core_states', None),
              f'population source/target is not distinct: {transfer}')

    # Boundary simulations cover full cap, exhausted source, treasury just below
    # affordability, successful completion and cancellation after reservation.
    for source, target, cap, years in ((50000, 100, 20000, 5), (5000, 300, 20000, 5), (20000, 0, 15000, 5)):
        _, _, moved = simulate_transfer(source, target, cap, years)
        check(moved == min(source, cap), f'migration cap/source boundary failed: {source}/{cap}')
    frontier = next(b for b in design['branches'] if b['id'] == 'greater')
    growth_focus = next(n for n in frontier['common'] + [x for p in frontier['paths'] for x in p['nodes']]
                        if n['id'] == 'gi_frontier_families')
    check(growth_focus.get('mods', {}).get('monthly_population') == .05 and
          growth_focus.get('mods', {}).get('health_cost_multiplier_modifier') == .02,
          'frontier population growth is not paired with its stated service cost')
    amount, after = reserve_budget(1_000_000, .012, 12_000)
    check(amount == 12_000 and after == 0, 'GDP reservation affordability boundary failed')
    reservation, unchanged = reserve_budget(1_000_000, .012, 11_999)
    check(reservation is None and unchanged == 11_999, 'underfunded project was not rejected')
    check(finish_project(amount, after, True) == after, 'successful project changed the reserved budget twice')
    check(finish_project(amount, after, False) == 12_000, 'failed project refund was not exact')
    status = simulate_status_switch({'equal_civil', 'equal_civil_project', 'displaced_claims'},
                                    'kach_special', regimes,
                                    {'equal_civil_project', 'displaced_claims'})
    check(status == {'kach_special', 'equal_civil_project', 'displaced_claims'},
          'status replacement erased persistent project/claims or stacked status effects')


def check_compiled(metadata, args):
    policy = metadata.get('policy_expansion', {})
    status_rules = metadata.get('policy_status_rules', {})
    check(status_rules.get('state') == 213,
          'equal/special/Kach legal-status rules still target a non-Sinai state')
    projects = policy.get('projects', [])
    check(len(projects) >= 8, f'compiled project export missing/short: {len(projects)}')
    seen = set()
    for project in projects:
        key = project.get('key')
        check(key not in seen, f'duplicate project metadata key: {key}')
        seen.add(key)
        check(project.get('share', 0) > 0 and project.get('days', 0) > 0,
              f'project lacks a positive reservation or delivery timer: {key}')
        check(project.get('paid') and project.get('done') and project.get('callback'),
              f'project metadata missing reservation/callback IDs: {key}')
        guard = project.get('guard', '')
        states = project.get('states', [])
        check(all(f'{state} = {{ is_controlled_by = ISR }}' in guard for state in states),
              f'project does not recheck control at delivery: {key}')
        if any(state in (204, 205, 206, 207) for state in states):
            check(all(f'{state} = {{ is_owned_by = ISR }}' in guard for state in states if state in (204,205,206,207)),
                  f'domestic project does not recheck ownership: {key}')

    required = (EFFECT_PATH, TRIGGER_PATH, DYNAMIC_PATH, DECISION_PATH, EVENT_PATH, IDEA_PATH)
    absent = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    check(not absent, f'compiled policy helper files are missing: {absent}')
    if absent:
        return
    parsed = {p: read(p.read_text(encoding='utf-8-sig')) for p in required}
    effects = parsed[EFFECT_PATH]
    effect_ids = {name for name, op, value in effects if op == '=' and isinstance(value, list)}
    for node in metadata['nodes']:
        if node.get('policy_extension'):
            check(node.get('policy_effect') in effect_ids,
                  f'focus effect helper is not emitted: {node["policy_key"]}')

    effect_text = EFFECT_PATH.read_text(encoding='utf-8-sig')
    event_text = EVENT_PATH.read_text(encoding='utf-8-sig')
    effect_blocks = block_map(effects)
    event_blocks = block_map(parsed[EVENT_PATH])

    # Population callbacks are recurring hidden events, not player-facing
    # decisions. Their namespace IDs must be unique because each migration
    # schedules itself again by ID every month.
    migrations = metadata.get('policy_migrations', [])
    top_events = [value for name, op, value in parsed[EVENT_PATH]
                  if name == 'country_event' and op == '=' and isinstance(value, list)]
    expected_migration_ids = {f'ISR70P.{1100 + i}' for i in range(len(migrations))}
    migration_events = [b for b in top_events if scalar(b, 'id') in expected_migration_ids]
    migration_ids = [scalar(b, 'id') for b in migration_events]
    all_event_ids = [scalar(b, 'id') for b in top_events]
    check(len(all_event_ids) == len(set(all_event_ids)),
          'generated country_event IDs are not globally unique')
    check(len(migration_ids) == len(migrations),
          f'expected one compiled callback per migration, found {len(migration_ids)} for {len(migrations)} migrations')
    check(len(migration_ids) == len(set(migration_ids)),
          f'migration callbacks reuse event IDs: {migration_ids}')
    for event in migration_events:
        check(scalar(event, 'hidden') == 'yes' and bool(direct(event, 'immediate')) and
              not direct(event, 'option'),
              f'migration callback {scalar(event, "id")} is not a hidden immediate event')
    for index, migration in enumerate(migrations):
        expected_id = f'ISR70P.{1100 + index}'
        check(expected_id in migration_ids,
              f'migration callback ID does not match unique allocation: {migration.get("key")}')
        event = next((b for b in migration_events if scalar(b, 'id') == expected_id), None)
        if event:
            code = normalized(named_block_text(event_text, '', event_id=expected_id))
            key = migration.get('key', '')
            source, target = str(migration.get('source')), str(migration.get('target'))
            active_flag = 'ISR70_policy_' + key + '_migration_active'
            check(active_flag in code and f'{source} = {{ add_manpower = -' in code and
                  f'{target} = {{ add_manpower =' in code,
                  f'migration callback does not implement the metadata route: {key}')
            check(migration.get('installments', 0) > 0 and migration.get('chunk', 0) > 0 and
                  migration.get('last', 0) > 0 and
                  migration.get('chunk', 0) * (migration.get('installments', 0) - 1) +
                  migration.get('last', 0) == migration.get('total'),
                  f'migration installments do not sum to the bounded population cap: {key}')

    # Sinai's general, canal-relabelled coastal, and Mafdal settlement
    # programmes are separate additive cohorts, each bounded independently.
    by_key = {m.get('key'): m for m in migrations}
    sinai_keys = ('gi_sinai_families', 'gi_canal_settlers', 'rad_mafdal_settlers')
    if all(key in by_key for key in sinai_keys):
        check(all(by_key[key].get('source') == 204 and by_key[key].get('target') == 213
                  for key in sinai_keys),
              'Sinai migration routes do not share the intended 204-to-213 corridor')
        check(sum(by_key[key].get('total', 0) for key in sinai_keys) == 45000 and
              by_key[sinai_keys[0]].get('total') == 20000 and
              by_key[sinai_keys[1]].get('total') == 15000 and
              by_key[sinai_keys[2]].get('total') == 10000,
              'the three independent Sinai cohorts no longer total 45,000 (20,000 + 15,000 + 10,000)')

    territory_dynamic = block_map(parsed[DYNAMIC_PATH])
    for key in ('special_status_access', 'kach_status_access', 'occupation_roads'):
        modifier = territory_dynamic.get('ISR70_policy_' + key)
        check(modifier is not None, f'territorial state modifier is missing: {key}')
        if modifier is None:
            continue
        enable = next(iter(direct(modifier, 'enable')), [])
        enables = {(k, v) for k, op, v in enable if op == '=' and not isinstance(v, list)}
        check(('is_controlled_by', 'ISR') in enables,
              f'territorial state modifier survives loss of Israeli control: {key}')
        values = {k: float(v) for k, op, v in modifier if op == '=' and not isinstance(v, list)
                  and k in ('local_factories', 'local_factories_factor',
                            'state_production_speed_buildings_factor')}
        check(not any(k != 'local_factories' for k in values),
              f'territorial access bonus uses a production modifier instead of local_factories: {key}')

    # Government packages reconcile in both directions each day. A completed
    # Herut/Mafdal programme should only carry its national idea while its
    # matching party is in office, and should regain it if that party returns.
    daily_text = named_block_text(effect_text, 'ISR70_policy_daily')
    for focus, idea, party in (
        ('rad_herut_authority', 'ISR70_policy_rad_herut_authority_idea', 'western_conservatism_are_in_power'),
        ('rad_herut_preparation', 'ISR70_policy_rad_herut_preparation_idea', 'western_conservatism_are_in_power'),
        ('rad_mafdal_review', 'ISR70_policy_rad_mafdal_review_idea', 'western_autocrats_are_in_power'),
    ):
        match = re.search(r'if = \{\s*limit = \{[^}]*has_completed_focus = ' + re.escape('ISR70_' + focus) +
                          r'[^}]*' + re.escape(party) + r'[^}]*\}.*?else = \{\s*remove_ideas = ' +
                          re.escape(idea) + r'\s*\}', daily_text, re.S)
        check(bool(match) and 'add_ideas = ' + idea in (match.group(0) if match else ''),
              f'government programme is not added on return and removed on exit: {focus}')

    # One aggregate dynamic modifier tracks only the marginal room below the
    # total 100% factory-access ceiling. The existing local_factories bonus is
    # subtracted, then the previously applied amount is restored before clamp.
    access = metadata.get('policy_factory_access', {})
    check(access.get('state') == 213 and access.get('modifier') == 'ISR70_policy_factory_access' and
          access.get('variable') == 'ISR70_policy_access_applied' and access.get('max_total') == 1.0,
          'Sinai factory-access cap metadata is absent or inconsistent')
    access_block = territory_dynamic.get('ISR70_policy_factory_access')
    check(access_block is not None, 'aggregate factory-access dynamic modifier is missing')
    if access_block is not None:
        access_values = {k for k, op, _ in access_block if op == '=' and k == 'local_factories'}
        check(access_values == {'local_factories'},
              'aggregate factory-access modifier does not apply the tracked local_factories value')
    update = named_block_text(effect_text, 'ISR70_policy_update_factory_access')
    for token in ('subtract_from_variable = { ISR70_policy_access_room = modifier@local_factories }',
                  'add_to_variable = { ISR70_policy_access_room = ISR70_policy_access_applied }',
                  'clamp_variable = { var = ISR70_policy_access_room min = 0 max = ISR70_policy_access_wanted }',
                  'set_variable = { ISR70_policy_access_applied = ISR70_policy_access_room }',
                  'remove_dynamic_modifier = ISR70_policy_factory_access',
                  'clear_variable = ISR70_policy_access_applied'):
        check(token in update, f'factory-access clamp/reconciliation is missing: {token}')
    for requested in (0.10, 0.15, 0.12):
        check(requested <= access.get('max_total', 0),
              f'factory-access request exceeds the aggregate ceiling: {requested}')

    for project in projects:
        callback = project['callback']
        check(callback in event_text, f'project completion callback is not emitted: {project["key"]}')
        # event entries are repeated, so select the block by its concrete id.
        callback_ast = next((b for b in descendants(parsed[EVENT_PATH], 'country_event')
                             if scalar(b, 'id') == callback), None)
        check(callback_ast is not None, f'project callback has no parseable country_event block: {project["key"]}')
        if callback_ast:
            code = normalized(named_block_text(event_text, '', event_id=callback))
            guard = normalized(project.get('guard', ''))
            check(bool(code) and guard in code, f'callback guard differs from project metadata: {project["key"]}')
        code = named_block_text(event_text, '', event_id=callback)
        check(re.search(r'treasury_change\s*=\s*' + re.escape(project['paid']) + r'.{0,100}?modify_treasury_effect\s*=\s*yes',
                        code, re.S) is not None,
              f'project does not refund its original reservation: {project["key"]}')
        check(project['done'] in code and 'clear_variable = ' + project['paid'] in code,
              f'project callback lacks completion/payment cleanup: {project["key"]}')
        start_id = 'ISR70_policy_start_' + project['key']
        start_code = effect_blocks.get(start_id, [])
        start_text = named_block_text(effect_text, start_id)
        token = 'ISR70_policy_cost_' + f'{project["share"]:.4f}'.replace('.', '_')
        days = project['days']
        check(project['paid'] in start_text and token in start_text,
              f'project reservation does not use its exact GDP share: {project["key"]}')
        check(f'country_event = {{ id = {callback} days = {days} }}' in start_text,
              f'project timer/callback differs from metadata: {project["key"]}')
        check('ISR70_policy_pay_' + token.removeprefix('ISR70_policy_cost_') + ' = yes' in start_text,
              f'project start does not debit the reserved share: {project["key"]}')
        check(bool(start_code), f'project start helper is missing from the parsed effects file: {project["key"]}')

    # Verify actual generated country-idea modifiers against the exported source
    # metadata, including the office percentages and both borrowing/debt effects.
    idea_blocks = block_map(parsed[IDEA_PATH])
    for short, spec in metadata.get('idea_definitions', {}).items():
        if not short.startswith('policy_'):
            continue
        actual = idea_blocks.get('ISR70_' + short)
        check(actual is not None, f'policy idea is absent from generated ideas: {short}')
        if actual is None:
            continue
        modifier = next(iter(direct(actual, 'modifier')), [])
        observed = {k: float(v) for k, op, v in modifier if op == '=' and not isinstance(v, list)}
        expected_mods = spec.get('modifiers', {})
        check(observed == {k: float(v) for k, v in expected_mods.items()},
              f'generated idea modifiers differ from metadata: {short}')

    # The standalone territory-state modifier must remain in state scope and
    # expire by its ownership/controller enable condition.
    dynamic_blocks = block_map(parsed[DYNAMIC_PATH])
    muni = dynamic_blocks.get('ISR70_policy_municipal_representation')
    check(muni is not None, 'municipal development modifier is missing')
    if muni is not None:
        enable = next(iter(direct(muni, 'enable')), [])
        enables = {(k, v) for k, op, v in enable if op == '=' and not isinstance(v, list)}
        actual = {k: float(v) for k, op, v in muni if op == '=' and
                  k == 'state_production_speed_infrastructure_factor' and not isinstance(v, list)}
        check(('is_owned_by', 'ISR') in enables and ('is_controlled_by', 'ISR') in enables,
              'municipal infrastructure modifier outlives Israeli ownership/control')
        check(actual == {'state_production_speed_infrastructure_factor': .15},
              'municipal infrastructure modifier has wrong state-scoped value')
    muni_text = named_block_text(effect_text, 'ISR70_policy_complete_municipal_representation')
    check(muni_text.count('add_dynamic_modifier = { modifier = ISR70_policy_municipal_representation }') == 2,
          'municipal state modifier is not applied to exactly states 205 and 206')

    decisions_ast = parsed[DECISION_PATH]
    bond = next((b for b in descendants(decisions_ast, 'ISR70_policy_decision_development_bond_draw')), None)
    check(bond is not None, 'development bond decision is missing')
    if bond:
        bond_text = normalized(named_block_text(DECISION_PATH.read_text(encoding='utf-8-sig'),
                                                'ISR70_policy_decision_development_bond_draw'))
        for fragment in ('treasury_change = gdp_total', 'multiply_temp_variable = { treasury_change = 0.01 }',
                         'modify_treasury_effect = yes', 'debt_change = gdp_total',
                         'multiply_temp_variable = { debt_change = 0.01 }', 'modify_debt_effect = yes'):
            check(fragment in bond_text[bond_text.find('ISR70_policy_decision_development_bond_draw ='):],
                  f'bond draw is not exactly matched treasury/debt: missing {fragment}')
        check('NOT = { has_country_flag = ISR70_policy_development_bond_draw_done }' in bond_text and
              'set_country_flag = ISR70_policy_development_bond_draw_done' in bond_text,
              'bond facility can be drawn more than once')

    domestic = (HERE / 'policy_domestic.py').read_text(encoding='utf-8')
    chain_requirements = {
        'equal_employment': 'ISR70_policy_project_equal_services_done',
        'equal_access': 'ISR70_policy_project_equal_services_done',
        'restricted_employment': 'ISR70_policy_project_preferential_allocations_done',
        'separate_development': 'ISR70_policy_project_restricted_employment_done',
    }
    for focus, flag in chain_requirements.items():
        check(flag in domestic, f'citizen route is gated on focus completion instead of delivery: {focus}')
    for focus, flag in {
        'municipal_representation': 'ISR70_policy_project_municipal_pacts_done',
        'restricted_employment': 'ISR70_policy_project_preferential_allocations_done',
        'separate_development': 'ISR70_policy_project_restricted_employment_done',
    }.items():
        match = re.search(r'api\.focus\("' + re.escape(focus) + r'".*?(?=\n\s*api\.|\Z)', domestic, re.S)
        check(bool(match and flag in match.group(0)),
              f'focus reward can complete before prior project delivery: {focus}')
    check(domestic.count('clr_country_flag = ISR70_policy_export_credit_pending') >= 2,
          'accepted and declined credit responses do not both clear pending')

    # Requests may be renewed after a refusal; pending is cleared on both
    # responses. A military agreement is allowed alongside accepted civilian aid.
    check('clr_country_flag = ISR70_policy_export_credit_pending' in event_text,
          'foreign credit response does not clear pending status')
    decision_text = DECISION_PATH.read_text(encoding='utf-8-sig')
    check('days_re_enable = 360' in decision_text and
          'ISR70_policy_export_credit_request_done' not in decision_text,
          'foreign request is not repeatable with the 360-day cooldown')
    check('ISR70_policy_export_credit_accepted' in event_text,
          'acceptance event does not grant the accepted-credit flag/idea')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-only', action='store_true',
                        help='run source and simulation checks before compiled metadata exists')
    args = parser.parse_args()
    design = json.loads(DESIGN_PATH.read_text(encoding='utf-8'))
    metadata = json.loads(EXPORT_PATH.read_text(encoding='utf-8'))
    check_design_mechanics(design)
    check_domestic_values()
    if args.source_only:
        print(json.dumps({'status': 'PASS' if not ERRORS else 'FAIL',
                          'mode': 'source-only; compiled Clausewitz checks skipped',
                          'checks': len(CHECKS), 'errors': ERRORS}, ensure_ascii=False, indent=2))
        return bool(ERRORS)
    if not metadata.get('policy_expansion'):
        ERRORS.append('compiler metadata export english_design.json[policy_expansion] is not present; build policy expansion before full validation')
    else:
        check_source_design(design, metadata)
        check_compiled(metadata, args)
    print(json.dumps({'status': 'PASS' if not ERRORS else 'FAIL', 'checks': len(CHECKS),
                      'errors': ERRORS}, ensure_ascii=False, indent=2))
    return bool(ERRORS)


if __name__ == '__main__':
    sys.exit(main())
