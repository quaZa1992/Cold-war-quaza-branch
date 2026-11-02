# IMPERIA COLD WAR — Read-only USA expansion source and lifecycle audit.
"""Read the approved baseline and current providers; write audit records only.

This helper never edits loaded game files. Focus spans are relative to each
immutable raw focus stored in current_inventory.json, not a moving live file.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
from usa_building_capacity import capacity_trigger

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/design/usa_1970_expansion_20261024'
BASELINE_SHA256 = '479D4979B1B7574AC8F58E2943505DDC432DE1E563429C837E276D0E585C8DA8'


@dataclass
class Statement:
    key: str
    op: str
    value: str | list
    start: int
    end: int
    value_start: int
    value_end: int


def parse(source):
    tokens = [(m[0], m.start(), m.end()) for m in re.finditer(
        r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|>=|<=|!=|=|<|>|[^\s{}<>=!#"]+', source)
        if not m[0].startswith('#')]
    position = 0

    def block(nested=False):
        nonlocal position
        rows = []
        while position < len(tokens):
            key, start, end = tokens[position]
            position += 1
            if key == '}':
                if not nested:
                    raise ValueError('Unexpected closing brace')
                return rows, end
            if key == '{':
                value, finish = block(True)
                rows.append(Statement('_list', '=', value, start, finish, start, finish))
                continue
            if position < len(tokens) and tokens[position][0] in ('=', '<', '>', '>=', '<=', '!='):
                op = tokens[position][0]
                position += 1
                value, value_start, finish = tokens[position]
                position += 1
                if value == '{':
                    value, finish = block(True)
                rows.append(Statement(key, op, value, start, finish, value_start, finish))
            else:
                rows.append(Statement('_bare', '=', key, start, end, start, end))
        if nested:
            raise ValueError('Unclosed block')
        return rows, len(source)

    return block()[0]


def first(rows, key, default=None):
    return next((r.value for r in rows if r.key == key), default)


def walk(rows, ancestors=()):
    for row in rows:
        yield row, ancestors
        if isinstance(row.value, list):
            yield from walk(row.value, ancestors + (row,))


def read(relative):
    return (ROOT / relative).read_text(encoding='utf-8-sig')


def raw(source, row):
    return source[row.start:row.end]


def line(source, offset):
    return source.count('\n', 0, offset) + 1


def serialize(rows):
    return [[r.key, r.op, serialize(r.value) if isinstance(r.value, list) else r.value] for r in rows]


def write(name, data):
    (OUT / name).write_text(json.dumps({'project': 'IMPERIA COLD WAR', **data}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def providers():
    source = read('common/scripted_effects/mdcw_1970_USA_native_api_bridge.txt')
    result = {}
    for row in parse(source):
        if not isinstance(row.value, list):
            continue
        additions = [r for r, _ in walk(row.value) if r.key == 'add_to_variable']
        if row.key.startswith('USA_change_') and len(additions) == 1:
            variable = additions[0].value[0].key
            result[row.key] = {'variable': variable, 'line': line(source, row.start), 'source': 'common/scripted_effects/mdcw_1970_USA_native_api_bridge.txt', 'implicit_treasury_fee': False, 'body': raw(source, row)}
    return result


def deltas(rows, bridge, source):
    result = []

    def scan(block, ancestor_keys=()):
        current = None
        for row in block:
            if row.key == 'set_temp_variable' and isinstance(row.value, list):
                value = first(row.value, 'temp_change')
                if value is not None:
                    current = value
            if row.key in bridge:
                result.append({'helper': row.key, 'variable': bridge[row.key]['variable'], 'amount': current, 'conditional_scope': list(ancestor_keys), 'statement_span': [row.start, row.end], 'raw': raw(source, row), 'provider_line': bridge[row.key]['line']})
            if isinstance(row.value, list):
                scan(row.value, ancestor_keys + (row.key,))
    scan(rows)
    return result


def building_records(focuses, bridge):
    buildings_source = read('common/buildings/00_buildings.txt')
    definitions = first(parse(buildings_source), 'buildings')
    caps = {}
    for row in definitions:
        if isinstance(row.value, list):
            cap = first(row.value, 'level_cap', [])
            if cap:
                caps[row.key] = {'state_max': first(cap, 'state_max'), 'province_max': first(cap, 'province_max'), 'shares_slots': first(cap, 'shares_slots', 'no'), 'group_by': first(cap, 'group_by'), 'only_coastal': first(row.value, 'only_costal', 'no'), 'definition_line': line(buildings_source, row.start)}
    records = []
    for focus in focuses:
        source = focus['raw']
        body = first(parse(source), 'focus')
        reward_node = next(r for r in body if r.key == 'completion_reward')
        grants = []
        for row, ancestors in walk(reward_node.value):
            if row.key != 'add_building_construction':
                continue
            state_node = next((a for a in reversed(ancestors) if a.key.isdecimal()), None)
            if state_node is None:
                raise ValueError('No fixed state container: ' + focus['id'])
            kind, level = first(row.value, 'type'), int(first(row.value, 'level'))
            grants.append({'state': int(state_node.key), 'building': kind, 'level': level, 'province': first(row.value, 'province'), 'building_span_in_raw_focus': [row.start, row.end], 'building_raw': raw(source, row), 'state_container_span_in_raw_focus': [state_node.start, state_node.end], 'state_container_raw': raw(source, state_node), 'slot_insert_before_offset': row.start, 'slot_statement': 'add_extra_state_shared_building_slots = ' + str(level), 'native_cap': caps[kind], 'capacity_trigger': capacity_trigger(kind,level), 'owner_control_trigger': 'is_owned_and_controlled_by = USA', 'province_owner_control_check': 'Not applicable: this is a state building with no province field.'})
        if not grants:
            continue
        grouped = defaultdict(Counter)
        for grant in grants:
            grouped[grant['state']][grant['building']] += grant['level']
        per_state = []
        for state, kinds in grouped.items():
            paths = list((ROOT / 'history/states').glob(str(state) + '-*.txt'))
            history = {}
            history_path = None
            if len(paths) == 1:
                history_path = str(paths[0].relative_to(ROOT))
                state_ast = first(parse(paths[0].read_text(encoding='utf-8-sig')), 'state')
                hist = first(state_ast, 'history', [])
                at_1970 = first(hist, '1970.1.1', [])
                history = {'owner': first(at_1970, 'owner', first(hist, 'owner')), 'controller': first(at_1970, 'controller', first(hist, 'controller')), 'building_history_base': serialize(first(hist, 'buildings', [])), 'building_history_1970_override': serialize(first(at_1970, 'buildings', [])), 'runtime_capacity_not_proven_by_history': True}
            per_state.append({'state': state, 'levels_by_type': dict(kinds), 'total_slots_required': sum(kinds.values()), 'state_history_source': history_path, 'state_history_1970': history, 'aggregate_owner_control': f'{state} = {{ is_owned_and_controlled_by = USA }}', 'aggregate_capacity': [f'{state} = {{ {capacity_trigger(kind,amount)} }}' for kind, amount in kinds.items()]})
        slot_nodes = [r for r, _ in walk(reward_node.value) if r.key == 'add_extra_state_shared_building_slots']
        cash = [first(r.value, 'treasury_change') for r, _ in walk(reward_node.value) if r.key == 'set_temp_variable' and isinstance(r.value, list) and first(r.value, 'treasury_change') is not None]
        records.append({'id': focus['id'], 'name': focus['name'], 'baseline_line': focus['line'], 'raw_focus_sha256': sha256(source.encode('utf-8')).hexdigest(), 'raw_focus': source, 'completion_reward_span_in_raw_focus': [reward_node.start, reward_node.end], 'missing_slots': not slot_nodes, 'existing_slot_commands': [raw(source, r) for r in slot_nodes], 'declared_treasury_changes': cash, 'fees': {'native_instant_build_has_no_explicit_treasury_helper': True, 'treasury_changes_already_in_completion': cash, 'bridge_helpers_have_no_implicit_fee': True, 'slot_price_should_not_be_added_without_approved_balance_change': True}, 'state_groups': per_state, 'grants': grants, 'patch_recipe': ['Verify this immutable raw-focus hash against the block selected for modification; do not use stale absolute file offsets.', 'Keep new reward replacements authoritative. Do not reinsert assets removed by one of the 13 approved focus reworks.', 'Add actual USA ownership/control and native capacity for every grouped asset to availability and real execution. Preserve the approved domestic native deficit/deduction pattern; do not introduce a new Treasury prerequisite by default.', 'Use one transaction receipt around setup cost and the entire package. Revalidate all state groups before any payment, slot or building. Preserve any existing explicitly approved funding contract.', 'Inside each state, add one shared slot per building level before each construction. Aggregate repeated types when testing capacity.', 'Keep ownership/capacity checks independent of shared-slot grants. Existing N2/N3/N6 also require these checks.', 'Do not charge a new slot fee merely because 00_buildings.txt contains a suggested slot price comment.', 'Keep native prospective effects visible independently of the hidden real transaction guard.']})
    missing = [r for r in records if r['missing_slots']]
    write('building_slot_repairs.json', {'baseline_source': 'common/national_focus/USA_1970.txt', 'baseline_sha256': BASELINE_SHA256, 'span_units': 'Zero-based Python Unicode code-point offsets in each record raw_focus; end-exclusive.', 'counts': {'baseline_focuses': len(focuses), 'building_focuses': len(records), 'missing_slot_focuses': len(missing), 'construction_commands': sum(len(r['grants']) for r in records), 'missing_slot_construction_commands': sum(len(r['grants']) for r in missing)}, 'native_max_shared_slots': 80, 'capacity_policy': 'The supplied free_building_slots triggers conservatively require current native capacity before the extra slots. They may reject a full shared-slot state even if a new slot would otherwise make room. They do not prove eligibility against every engine state or override a type/group cap.', 'missing_slot_focuses': missing, 'existing_slot_focuses_also_requiring_transaction_review': [r for r in records if not r['missing_slots']], 'building_definitions': caps})


# Explicit semantic classification of the actual baseline names, not a blanket
# subtraction rule. Ambiguous bundles remain national until separately decided.
DURABLE = {
    '1972_dem_1', '1972_dem_4', '1972_dem_5', '1972_dem_6', '1972_dem_7', '1972_rep_7',
    '1976_dem_4', '1976_dem_5', '1976_dem_6', '1976_dem_7', '1976_rep_6',
    '1980_dem_4', '1980_dem_6', '1980_rep_5', '1980_rep_7',
    '1984_dem_3', '1984_dem_4', '1984_dem_5', '1984_dem_6', '1984_dem_7', '1984_rep_6', '1984_rep_7',
    '1988_dem_2', '1988_dem_3', '1988_dem_4', '1988_dem_6', '1988_rep_1', '1988_rep_6', '1988_rep_7',
    '1992_dem_3', '1992_dem_5', '1992_dem_7', '1992_rep_1', '1992_rep_4', '1992_rep_5', '1992_rep_6', '1992_rep_7',
    '1996_dem_3', '1996_rep_1', '1996_rep_3', '1996_rep_4',
}
ACTIVE = {
    '1972_dem_2', '1972_dem_3', '1972_rep_1', '1972_rep_2', '1972_rep_3', '1972_rep_4', '1972_rep_6',
    '1976_dem_1', '1976_dem_2', '1976_rep_1', '1976_rep_2', '1976_rep_3', '1976_rep_4', '1976_rep_5',
    '1980_dem_1', '1980_dem_3', '1980_dem_5', '1980_dem_7', '1980_rep_1', '1980_rep_2', '1980_rep_3', '1980_rep_4', '1980_rep_6',
    '1984_dem_1', '1984_dem_2', '1984_rep_1', '1984_rep_2', '1984_rep_3', '1984_rep_4', '1984_rep_5',
    '1988_dem_1', '1988_dem_5', '1988_dem_7', '1988_rep_2', '1988_rep_3', '1988_rep_4',
    '1992_dem_1', '1992_dem_2', '1992_dem_4', '1992_dem_6', '1992_rep_2',
    '1996_dem_1', '1996_dem_2', '1996_rep_2',
}


def election_records(focuses, bridge):
    nodes = []
    for focus in focuses:
        if not re.match(r'USA_1970_19\d\d_', focus['id']):
            continue
        source = focus['raw']; body = first(parse(source), 'focus')
        reward = first(body, 'completion_reward', [])
        match = re.match(r'USA_1970_(19\d\d)_(dem|rep)_(\d+)_', focus['id'])
        if match:
            year, party, number = match.groups()
            key = f'{year}_{party}_{number}'
            gate = 'western_liberals_are_in_power' if party == 'dem' else 'western_conservatism_are_in_power'
            if key in DURABLE:
                category, suspend = 'durable_national_institution_or_enacted_measure', False
                reason = 'The named measure establishes legislation, an official institution, lasting reorganisation, completed industrial conversion or a resolved financial intervention. Keep its baseline helper bundle national unless an explicit repeal mechanic is approved.'
            elif key in ACTIVE:
                category, suspend = 'ongoing_administration_programme', True
                reason = 'The named focus represents a continuing appropriation priority, discretionary economic stance, diplomatic posture or strategic programme. Its signed helper-stat bundle can follow the exact governing party; one-time and legal receipts remain national.'
            else:
                category, suspend = 'ambiguous_preserve_pending_explicit_classification', False
                reason = 'The title and reward mix do not distinguish the lasting institutional outcome from ongoing funding sufficiently. Do not invent a broad reversal. Flag for an explicit split; conservative default preserves the baseline bundle.'
            kind = 'partisan_programme'
        elif '_common_' in focus['id']:
            year, party, gate, category, suspend, kind = focus['id'][9:13], None, None, 'durable_common_national_measure', False, 'common_measure'
            reason = 'Shared national act reached after either election result. Do not make the institution disappear on a later party change.'
        else:
            year, party, gate, category, suspend, kind = focus['id'][9:13], ('dem' if 'democratic_victory' in focus['id'] else 'rep'), None, 'persistent_election_receipt', False, 'election_marker'
            reason = 'Zero-cost election bypass marker. It records the actual past result and must persist independently of the current government.'
        changes = deltas(reward, bridge, source)
        flags = [r.value for r, _ in walk(reward) if r.key == 'set_country_flag']
        once = [{'command': r.key, 'raw': raw(source, r)} for r, _ in walk(reward) if r.key in {'add_building_construction', 'army_experience', 'navy_experience', 'air_experience', 'add_political_power', 'add_stability', 'add_war_support', 'modify_treasury_effect', 'modify_debt_effect', 'change_relative_party_popularity', 'USA_congress_small_support', 'USA_congress_medium_support', 'USA_congress_small_opposition', 'USA_congress_medium_opposition', 'change_wall_street_opinion', 'change_defense_industry_opinion', 'USA_modify_economic_regulation', 'add_tech_bonus', 'add_doctrine_cost_reduction', 'set_idea_to_volunteer_army', 'set_idea_to_draft_army'}]
        nodes.append({'id': focus['id'], 'name': focus['name'], 'baseline_line': focus['line'], 'kind': kind, 'party': party, 'year': year, 'execution_gate': gate, 'classification': category, 'suspend_helper_bundle_on_party_loss': suspend, 'classification_reason': reason, 'classification_evidence_boundary': 'Implementation design classification based on actual title and reward scope, not a newly researched historical repeal claim.', 'receipt': 'has_completed_focus = ' + focus['id'], 'country_flags_to_preserve': flags, 'helper_deltas': changes, 'persistent_helper_deltas': [] if suspend else changes, 'party_bound_helper_deltas': changes if suspend else [], 'one_time_effects_to_preserve': once, 'keep_allow_branch_visible': True, 'raw_focus_sha256': sha256(source.encode('utf-8')).hexdigest()})
    counts = Counter(n['classification'] for n in nodes)
    write('implementation_support_elections.json', {'baseline_sha256': BASELINE_SHA256, 'counts': dict(counts), 'node_count': len(nodes), 'native_party_triggers': {'dem': {'trigger': 'western_liberals_are_in_power', 'slot': 2, 'provider': 'common/scripted_triggers/01_political_triggers.txt:183'}, 'rep': {'trigger': 'western_conservatism_are_in_power', 'slot': 1, 'provider': 'common/scripted_triggers/01_political_triggers.txt:176'}}, 'nodes': nodes, 'providers': bridge, 'hook_recommendation': {'generic_dispatch': 'common/scripted_effects/00_leader_setup_scripted_effects.txt:set_leader updates outlook and calls set_leader_[TAG] by original_tag.', 'narrow_immediate_hook': 'Call the idempotent USA programme sync once at the END of top-level set_leader_USA, outside its special-successor if/else chain, guarded by real USA/1970/initialisation. This covers special successors and third-party governments.', 'avoid_incomplete_hook': 'Hooking only USA_1970_set_scenario_leader misses the special-successor branch and non-Dem/Rep governments.', 'fallback': 'Add an idempotent call to the existing on_weekly_USA effect block in common/on_actions/mdcw_1970_USA_on_actions.txt; this catches direct ruling_party edits that bypass leader recreation.', 'do_not_replay': 'Sync only signed helper contributions. Never rerun completion_reward or repeat setup costs, buildings, PP, XP, factions, native law swaps or treaty dispatch.'}, 'migration_recipe': ['Execution gates go on 92 partisan programme focuses in availability AND the real completion guard. They do not replace historical election receipts.', 'Keep 14 election markers and 7 shared laws persistent. Remove date-dependent allow_branch hiding without deleting actual bypass/availability date guards.', 'For each explicitly active helper bundle, track its last applied signed contribution per variable. Desired contribution is the sum of earned compatible bundles whose exact party currently governs.', 'Adjust each native consumed variable by desired minus previously applied contribution, then store the new applied value. Repeated sync is a no-op. Do not reset the whole USA variable to a party sum.', 'Initialize the old-save applied ledger from completed explicitly active focuses because their old additive deltas are already embedded in USA totals; only then reconcile against the current party. Do not add those historical deltas again.', 'Preserve all one-time assets and earned receipts. Preserve enacted-law and official-institution helper bundles. Ambiguous nodes are listed explicitly and preserved by default.', 'Do not use reverse faction/opinion/Congress/regulation helpers for cleanup: those mutate clamped or random national systems and are not mathematically reversible.']})


def legacy_records():
    records = []
    for relative, prefix in [('events/USA_1970_events.txt', 'USA_1970.'), ('events/USA_1970_nixon_diplomacy_events.txt', 'USA_1970_nixon_dip.')]:
        source = read(relative)
        for row in parse(source):
            if row.key != 'country_event' or not isinstance(row.value, list):
                continue
            event_id = first(row.value, 'id')
            if relative.endswith('USA_1970_events.txt') and event_id not in {f'USA_1970.{n}' for n in [100,101,110,111,120,121,130,131,140,141,150,151,170,171]}:
                continue
            flags = sorted({r.value for r, _ in walk(row.value) if r.key in {'set_country_flag', 'has_country_flag', 'clr_country_flag'} and isinstance(r.value,str)})
            options = []
            for option in (r for r in row.value if r.key == 'option'):
                options.append({'name': first(option.value,'name'), 'raw': raw(source,option), 'line': line(source,option.start), 'helper_deltas': deltas(option.value, providers(), source)})
            records.append({'id': event_id, 'source': relative, 'line': line(source,row.start), 'flags': flags, 'options': options, 'raw': raw(source,row)})
    write('implementation_support_diplomacy.json', {'scope': 'Legacy offer/event source snapshot before expansion consolidation. No runtime files changed.', 'events': records, 'critical_fee_helpers': [{'helper': 'enbo_usa_send_monetary_package_to_israel_effect', 'source': 'common/scripted_effects/mdcw_1970_aipac_consumed_helpers.txt:32', 'debit_USA': 5, 'credit_ISR': 5, 'other_effects': 'Wall Street opinion and influence mutation; event dispatch'}, {'helper': 'USA_1970_register_arab_compact_acceptance', 'source': 'common/scripted_effects/USA_1970_scripted_effects.txt:384', 'debit_USA': 15, 'receipt': 'USA_1970_arab_compact_applied'}, {'event_option': 'USA_1970.101.a', 'debit_USA': 5, 'scope': 'Atlantic renegotiation'}, {'event_option': 'USA_1970.141.a', 'debit_USA': 10, 'scope': 'Maritime renegotiation'}], 'migration_rules': ['An accepted old partner flag proves only the old package. It is not consent to new stronger spirits or new payments.', 'Do not initialize new signed/setup receipts solely because the sending focus is complete. Missing/refused/pending offers are distinct.', 'Preserve past one-time cash, XP, PP, access, borders, old native trade agreements and historical acceptance receipts; never replay them from a new treaty sync.', 'For new distinct follow-up programmes use new explicit recipient consent and the approved new costs once. State in the implementation that these are new terms, not automatic grandfathered acceptance.', 'If a legacy treaty is genuinely upgraded without new assets/costs, migrate a scoped receipt only for the exact named accepted partner and exact old package; never infer all signatories from an aggregate count.', 'Retire or redirect old senders F4-F9/D6/E9 and later globalization channels consistently, including queued old accept and renegotiation event options.', 'Preserve registration flags consumed by later decisions/F10 or migrate their consumers to active new receipts; do not leave unreachable decisions referencing abandoned partner flags.', 'Do not subtract aggregate old treaty deltas once per partner: Atlantic rewards trigger at two registrations; commercial and Arab rewards are guarded once per whole package; Israeli registration originally is per accepted package. Any reconciliation needs exact application flags.', 'Nixon accepted channels are historical contacts, not standing paired spirits. Preserve their acknowledgement and material receipts; new Japan/China/Moscow/SVN programmes must not replay old summit or assistance effects.']})


def main():
    focuses = json.loads((OUT / 'current_inventory.json').read_text(encoding='utf-8'))['focuses']
    bridge = providers()
    building_records(focuses, bridge)
    election_records(focuses, bridge)
    legacy_records()
    print('Wrote audit-only building, election and diplomacy records for', len(focuses), 'baseline focuses.')


if __name__ == '__main__':
    main()
