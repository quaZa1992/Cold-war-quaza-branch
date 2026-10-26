# IMPERIA CW — Cold War: uae 1970 — test focus runtime.
"""Exercise emitted focus/programme AST, not the HOI4 engine or native economy."""
from pathlib import Path
import copy
import json
import sys
from revision import current_design

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first

P = 'COLDWAR_UAE_'
def read(rel):
    return parse((ROOT / rel).read_text(encoding='utf-8-sig'))

E = {}
for name in ['focus_effects', 'programmes']:
    E.update({k: v for k, _, v in read('common/scripted_effects/COLDWAR_UAE_1970_' + name + '.txt')})
T = {k: v for k, _, v in read('common/scripted_triggers/COLDWAR_UAE_1970_focus_triggers.txt')}
T.update({k: v for k, _, v in read('common/scripted_triggers/COLDWAR_UAE_1970_politics_triggers.txt')})
D = current_design()


class World:
    def __init__(self):
        self.variables = {'treasury': 10.0, 'ruling_party': 0}
        self.flags = {}
        self.day = 0
        self.subject = 'ENG'
        self.governments = {'western_autocrats_are_in_power'}
        self.states = {179: {'owner': 'UAE', 'controller': 'UAE', 'slots': 3, 'oil': 1, 'productivity': 100, 'aluminium': 0, 'steel': 0, 'industrial_complex': 0},
                       180: {'owner': 'UAE', 'controller': 'UAE', 'slots': 3, 'oil': 3, 'productivity': 100, 'aluminium': 0, 'steel': 0, 'industrial_complex': 0}}
        self.dynamic = set()
        self.xp = {}
        self.queue = []
        self.province_queue = []
        self.province_buildings = {3725: {'naval_base': 0}}
        self.scenario = True

    def num(self, value, state=None):
        if value == 'building_level@industrial_complex':
            return self.states[state]['industrial_complex']
        try:
            return float(value)
        except (ValueError, TypeError):
            return self.variables.get(value, 0)

    def has_flag(self, key):
        return key in self.flags and (self.flags[key] is None or self.flags[key] > self.day)

    def test(self, rows, state=None):
        return all(self.condition(k, o, v, state) for k, o, v in rows)

    def condition(self, key, op, value, state):
        if key in {'AND', 'hidden_trigger', 'limit'}:
            return self.test(value, state)
        if key == 'OR':
            return any(self.condition(k, o, v, state) for k, o, v in value)
        if key == 'NOT':
            return not self.test(value, state)
        if key == 'custom_trigger_tooltip':
            return self.test([r for r in value if r[0] != 'tooltip'], state)
        if key.isdigit():
            return self.test(value, int(key))
        if key == P + '1970_campaign':
            return self.scenario
        if key in T:
            return self.test(T[key], state) == (value == 'yes')
        if key.endswith('_are_in_power'):
            return (key in self.governments) == (value == 'yes')
        if key == 'always':
            return value == 'yes'
        if key == 'has_country_flag':
            return self.has_flag(value)
        if key == 'has_dynamic_modifier':
            return first(value, 'modifier') in self.dynamic
        if key == 'is_subject_of':
            return self.subject == value
        if key == 'is_subject':
            return bool(self.subject) == (value == 'yes')
        if key in {'is_owned_by', 'is_controlled_by'}:
            return self.states[state]['owner' if key == 'is_owned_by' else 'controller'] == ('UAE' if value == 'ROOT' else value)
        if key in {'owns_state', 'controls_state'}:
            return self.states[int(value)]['owner' if key == 'owns_state' else 'controller'] == 'UAE'
        if key == 'controls_province':
            assert value == '3725'
            return self.states[179]['controller'] == 'UAE'
        if key == 'any_province_building_level':
            province = int(first(first(value, 'province'), 'id'))
            level = self.province_buildings.get(province, {}).get(first(value, 'building'), 0)
            _, comparison, amount = next(row for row in value if row[0] == 'level')
            return {'>': level > int(amount), '<': level < int(amount), '=': level == int(amount)}[comparison]
        if key == 'free_building_slots':
            if first(value, 'building') == 'air_base':
                return self.states[state].get('air_base', 0) < 10
            return self.states[state]['slots'] > 0
        if key == 'check_variable':
            if first(value, 'var'):
                a, b, compare = self.num(first(value, 'var'), state), self.num(first(value, 'value'), state), first(value, 'compare', 'equals')
            else:
                variable, compare, operand = value[0]
                a, b = self.num(variable, state), self.num(operand, state)
            return {'greater_than_or_equals': a >= b, 'less_than_or_equals': a <= b,
                    'greater_than': a > b, 'less_than': a < b, 'equals': a == b,
                    '>': a > b, '<': a < b, '=': a == b}[compare]
        raise AssertionError('Unmodelled trigger: ' + key)

    def execute(self, rows, state=None):
        branch = False
        for key, op, value in rows:
            if key == 'if':
                branch = self.test(first(value, 'limit', []), state)
                if branch:
                    self.execute([r for r in value if r[0] != 'limit'], state)
            elif key == 'else':
                if not branch:
                    self.execute(value, state)
                branch = False
            elif key == 'hidden_effect':
                self.execute(value, state)
            elif key.isdigit():
                self.execute(value, int(key))
            elif key in E:
                self.execute(E[key], state)
            elif key in {'set_variable', 'set_temp_variable', 'add_to_variable', 'subtract_from_variable',
                         'add_to_temp_variable', 'subtract_from_temp_variable', 'multiply_variable',
                         'multiply_temp_variable', 'divide_variable', 'divide_temp_variable'}:
                variable, _, operand = value[0]
                if key in {'set_variable', 'set_temp_variable'}:
                    self.variables[variable] = self.num(operand)
                elif key.startswith('multiply_'):
                    self.variables[variable] = self.num(variable) * self.num(operand)
                elif key.startswith('divide_'):
                    self.variables[variable] = self.num(variable) / self.num(operand)
                else:
                    self.variables[variable] = self.num(variable) + self.num(operand) * (-1 if key.startswith('subtract_') else 1)
            elif key in {'clamp_variable', 'clamp_temp_variable'}:
                var = first(value, 'var')
                self.variables[var] = max(self.num(first(value, 'min', '-inf')), min(self.num(first(value, 'max', 'inf')), self.num(var)))
            elif key == 'set_country_flag':
                flag = first(value, 'flag') if isinstance(value, list) else value
                self.flags[flag] = self.day + int(first(value, 'days')) if isinstance(value, list) else None
            elif key == 'clr_country_flag':
                self.flags.pop(value, None)
            elif key == 'modify_treasury_effect':
                self.variables['treasury'] += self.variables['treasury_change']
            elif key == 'add_dynamic_modifier':
                self.dynamic.add(first(value, 'modifier'))
            elif key == 'remove_dynamic_modifier':
                self.dynamic.discard(first(value, 'modifier'))
            elif key == 'add_resource':
                self.states[state][first(value, 'type')] += int(first(value, 'amount'))
            elif key == 'add_extra_state_shared_building_slots':
                self.states[state]['slots'] += int(value)
            elif key == 'add_building_construction':
                building, level = first(value, 'type'), int(first(value, 'level'))
                if first(value, 'instant_build') == 'yes':
                    self.states[state][building] = self.states[state].get(building, 0) + level
                else:
                    self.queue.append((state, building, level))
                    if first(value, 'province'):
                        self.province_queue.append((state, int(first(value, 'province')), building, level))
            elif key == 'state_flat_productivity_change_effect':
                self.states[state]['productivity'] += self.variables['temp_productivity_change']
            elif key == 'flat_productivity_change_effect':
                for s in self.states.values():
                    if s['controller'] == 'UAE':
                        s['productivity'] += self.variables['temp_productivity_change']
            elif key.endswith('_experience'):
                self.xp[key] = self.xp.get(key, 0) + float(value)
            elif key in {'custom_effect_tooltip', 'unlock_decision_tooltip', 'ingame_update_setup', 'force_update_dynamic_modifier'}:
                pass  # Native presentation/economic recalculation are deliberately outside this test.
            else:
                raise AssertionError('Unmodelled effect: ' + key)

    def call(self, name):
        self.execute(E[P + name])


def run():
    cases = []
    def passed(name): cases.append(name)
    w = World(); w.variables['treasury'] = -1
    # The oil entry's dependency must be earned before any payment.
    oil = next(n for n in D['nodes'] if n['id'] == P + 'oil_accounts')
    for row in oil['prerequisites']:
        w.flags[P + 'done_' + row[0].removeprefix(P)] = None
    w.call('apply_oil_accounts'); w.call('apply_oil_accounts')
    assert abs(w.variables['treasury'] + 1.75) < 1e-10 and w.states[180]['oil'] == 11
    passed('Negative treasury does not veto an eligible oil focus; its full0.75bn debit and resources apply once')
    w = World(); w.variables['treasury'] = 16.25
    phases = [n for n in D['nodes'] if any(c['resource'] == 'oil' for c in n.get('resource_changes', []))]
    for phase in phases:
        for row in phase['prerequisites']:
            w.flags[P + 'done_' + row[0].removeprefix(P)] = None
        w.call('apply_' + phase['id'].removeprefix(P))
    assert abs(w.variables['treasury']) < 1e-9 and w.states[180]['oil'] == 40 and w.states[179]['oil'] == 7
    for phase in phases:
        w.call('apply_' + phase['id'].removeprefix(P))
    assert abs(w.variables['treasury']) < 1e-9 and sum(s['oil'] for s in w.states.values()) == 47
    passed('All four funded oil phases cost 16.25bn and add exactly 43 base oil, without replay')
    before = copy.deepcopy((w.variables['treasury'], w.states, w.queue, w.xp))
    w.call('refresh_programmes'); w.call('refresh_programmes')
    assert before == (w.variables['treasury'], w.states, w.queue, w.xp)
    passed('Programme refresh replays no money, oil, productivity, queue or experience')
    w = World(); w.states[180]['controller'] = 'ENG'
    w.call('apply_oil_accounts')
    assert w.variables['treasury'] == 10 and w.states[180]['oil'] == 3
    passed('Loss of recipient-state control prevents oil expenditure')
    w = World(); w.call('apply_majlis')
    assert w.variables[P + 'monarchy_stability_factor'] == 0.05
    before = copy.deepcopy((w.variables['treasury'], w.states, w.queue, w.xp))
    w.governments = {'western_liberals_are_in_power'}; w.variables['ruling_party'] = 2; w.call('refresh_programmes')
    assert w.variables[P + 'monarchy_stability_factor'] == 0
    w.governments = {'western_autocrats_are_in_power'}; w.variables['ruling_party'] = 0; w.call('refresh_programmes')
    assert w.variables[P + 'monarchy_stability_factor'] == 0.05 and before == (w.variables['treasury'], w.states, w.queue, w.xp)
    passed('Party departure and return restore only earned ongoing contributions')
    for order in [('dual_veto', 'zayed_compact'), ('zayed_compact', 'dual_veto')]:
        w = World()
        for key in order:
            w.flags[P + 'done_' + key] = None
            w.call('refresh_programmes')
        assert w.variables[P + 'unequal_development_production_speed_buildings_factor'] == 0
    passed('Permanent construction remedies are order independent and clamp at zero')
    w = World()
    for key in ['dual_veto', 'emirate_commands']:
        w.flags[P + 'done_' + key] = None
    w.call('refresh_programmes')
    assert abs(w.variables[P + 'fragmented_authority_army_org_factor'] + 0.03) < 1e-9
    passed('Army integration uses strongest family credit rather than stacking')
    w = World(); w.subject = None
    for key in ['renew_protection', 'orderly_handover']:
        w.flags[P + 'done_' + key] = None
    w.flags[P + 'temporary_orderly_handover'] = 365
    w.call('refresh_programmes')
    assert w.variables[P + 'british_equipment_cost_multiplier_modifier'] == -0.08
    w.day = 365; w.call('refresh_programmes')
    assert w.variables[P + 'british_equipment_cost_multiplier_modifier'] == 0
    passed('Handover contribution expires without being renewed by refresh')
    w = World(); w.flags[P + 'done_nine_states'] = None; w.call('refresh_programmes')
    assert w.variables[P + 'union_imp_investment_in_extra'] == 0
    w.flags[P + 'broad_charter_accepted'] = None; w.call('refresh_programmes')
    assert w.variables[P + 'union_imp_investment_in_extra'] == 1
    passed('Broad federation investment capacity needs the accepted agreement')
    for occupied, full in [(False, False), (True, False), (False, True)]:
        w = World(); w.variables['treasury'] = -1
        w.flags[P+'done_trading_coast'] = None
        w.states[180]['naval_base'] = 10
        if occupied:
            w.states[179]['controller'] = 'ENG'
        if full:
            w.province_buildings[3725]['naval_base'] = 10
        w.call('apply_port_planning'); w.call('apply_port_planning')
        assert w.province_queue == ([] if occupied or full else [(179,3725,'naval_base',1)])
        assert abs(w.variables['treasury'] + 1.15) < 1e-9
    passed('Fishing Harbours queues one Dubai province3725 port at the single0.15bn focus cost; occupation/full target prevents construction and an unrelated level10 port does not block it')
    report = {'passed': len(cases), 'cases': cases, 'errors': [],
              'limits': 'Emitted AST subset only. Native UI, economic formulas, game loading and multiplayer are not emulated.'}
    (HERE / 'focus_runtime_validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    run()
