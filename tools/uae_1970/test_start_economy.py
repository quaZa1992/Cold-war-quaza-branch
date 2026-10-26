# IMPERIA CW — Cold War: uae 1970 — test start economy.
"""Execute the bounded industrial bootstrap AST and inspect dated snapshots.

No game files are installed. --installed additionally compares all three live
outputs. This is source/AST evidence, not an emulation of HOI4 economy or UI.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'tools/vietnam_1970'))
from script_ast import parse, first, values, walk
import economy_start as start

P = 'COLDWAR_UAE_'


class World:
    def __init__(self):
        self.original, self.dynamic, self.start = 'UAE', False, (1970, 1, 1)
        self.date = (1970, 1, 1)
        self.flags, self.variables = set(), {}
        self.states = {179: {'owner': 'UAE', 'controller': 'UAE', 'aluminium': 19, 'steel': 0, 'oil': 1, 'composite_plant': 0},
                       180: {'owner': 'UAE', 'controller': 'UAE', 'aluminium': 22, 'steel': 5, 'oil': 3, 'composite_plant': 0}}
        self.removal_works = True
        self.removal_calls = {179: 0, 180: 0}

    def number(self, value, state):
        try:
            return float(value)
        except (TypeError, ValueError):
            return self.variables.get((state, value), 0)

    def test(self, rows, state=None):
        return all(self.condition(k, op, value, state) for k, op, value in rows)

    def condition(self, key, op, value, state):
        if key in {'AND', 'limit'}:
            return self.test(value, state)
        if key == 'OR':
            return any(self.condition(k, o, v, state) for k, o, v in value)
        if key == 'NOT':
            return not self.test(value, state)
        if key == 'original_tag':
            return self.original == value
        if key == 'is_dynamic_country':
            return self.dynamic == (value == 'yes')
        if key == 'IMP_is_1970_scenario':
            return ((1969, 12, 31) < self.start < (1970, 1, 2)) == (value == 'yes')
        if key == P+'1970_campaign':
            identity = self.original == 'UAE' and not self.dynamic and self.start == (1970, 1, 1)
            return identity == (value == 'yes')
        if key == 'date':
            other = tuple(map(int, value.split('.')))
            return self.date < other if op == '<' else self.date > other if op == '>' else self.date == other
        if key == 'has_country_flag':
            return value in self.flags
        if key in {'owns_state', 'controls_state'}:
            return self.states[int(value)]['owner' if key == 'owns_state' else 'controller'] == 'UAE'
        if key == 'composite_plant':
            return self.states[state][key] > int(value) if op == '>' else self.states[state][key] == int(value)
        if key == 'check_variable':
            a, b = self.number(first(value, 'var'), state), self.number(first(value, 'value'), state)
            return a < b if first(value, 'compare') == 'less_than' else a == b
        raise AssertionError('Unmodelled bootstrap trigger: '+key)

    def run(self, rows, state=None):
        for key, op, value in rows:
            if key == 'if':
                if self.test(first(value, 'limit', []), state):
                    self.run([row for row in value if row[0] != 'limit'], state)
            elif key.isdigit():
                self.run(value, int(key))
            elif key == 'while_loop_effect':
                turns = 0
                while self.test(first(value, 'limit'), state):
                    self.run([row for row in value if row[0] != 'limit'], state)
                    turns += 1
                    assert turns <= 5, 'Composite removal exceeded native state cap'
            elif key == 'add_resource':
                self.states[state][first(value, 'type')] += int(first(value, 'amount'))
            elif key == 'remove_building':
                self.removal_calls[state] += 1
                if self.removal_works:
                    building = first(value, 'type')
                    self.states[state][building] = max(0, self.states[state][building]-int(first(value, 'level')))
            elif key in {'set_temp_variable', 'add_to_temp_variable'}:
                variable, _, operand = value[0]
                self.variables[state, variable] = self.number(operand, state) + (self.number(variable, state) if key.startswith('add_') else 0)
            elif key == 'set_country_flag':
                self.flags.add(value)
            else:
                raise AssertionError('Unmodelled bootstrap effect: '+key)


def levels(text, date):
    history = first(first(parse(text), 'state'), 'history')
    result = {}
    def apply(rows):
        for building in values(rows, 'buildings'):
            for key, _, value in building:
                if isinstance(value, str):
                    result[key] = int(value)
    apply(history)
    dates = [(tuple(map(int, key.split('.'))), block) for key, _, block in history if re.fullmatch(r'\d{4}\.\d+\.\d+', key)]
    for stamp, block in sorted(dates):
        if stamp <= date:
            apply(block)
    return result


def run(installed=False):
    checks, cases = 0, []
    def check(value, label):
        nonlocal checks
        checks += 1
        assert value, label
    before = {relative: (ROOT/relative).read_bytes() for relative, _, _ in start.STATES.values()}
    outputs = start.build({})
    check(len(outputs) == 3 and start.EFFECT_PATH in outputs, 'Wrong owned output set')
    check(all((ROOT/path).read_bytes() == data for path, data in before.items()), 'Pure build wrote game files')
    body = first(parse(outputs[start.EFFECT_PATH]), P+'startup_industry')
    w = World(); w.run(body)
    check(all(state['aluminium'] == state['steel'] == state['composite_plant'] == 0 for state in w.states.values()), 'Baseline retains modern industry')
    check([w.states[s]['oil'] for s in (179, 180)] == [1, 3], 'Industry bootstrap changes oil')
    check(P+'industry_start_applied' in w.flags, 'One-time industry receipt missing')
    cases.append('Fresh historical UAE removes19+22 light metals and5 steel without touching oil')
    for first_level in range(6):
        for second_level in range(6):
            w = World(); w.states[179]['composite_plant'], w.states[180]['composite_plant'] = first_level, second_level
            w.run(body)
            check(w.states[179]['composite_plant'] == w.states[180]['composite_plant'] == 0, 'A valid native plant level survived')
            check(w.removal_calls == {179: first_level, 180: second_level}, 'Wrong bounded native removal count')
    w = World(); w.removal_works = False
    w.states[179]['composite_plant'] = 5; w.run(body)
    check(w.removal_calls[179] == 5, 'No-progress removal can hang startup')
    cases.append('Native remove_building clears every0..5 plant combination and stops after5 attempts even without progress')
    w = World(); w.run(body)
    w.states[179].update(aluminium=8, steel=2, composite_plant=1)
    w.states[180].update(aluminium=10, steel=7, composite_plant=2)
    funded = deepcopy(w.states); w.run(body)
    check(w.states == funded, 'Repeated initialization resets funded upgrades')
    w.date = (1990, 1, 1); w.run(body)
    check(w.states == funded, 'Later campaign resets funded upgrades')
    cases.append('Receipt and date guards preserve later paid resources/plants and make repeat calls inert')
    for invalid in ['modern', 'foreign', 'dynamic', 'late', 'gdp', 'receipt', 'owner179', 'controller179', 'owner180', 'controller180']:
        w = World()
        if invalid == 'modern': w.start = (2000, 1, 1)
        elif invalid == 'foreign': w.original = 'ENG'
        elif invalid == 'dynamic': w.dynamic = True
        elif invalid == 'late': w.date = (1970, 1, 3)
        elif invalid == 'gdp': w.flags.add('IMP_1970_gdp_profile_applied')
        elif invalid == 'receipt': w.flags.add(P+'industry_start_applied')
        else:
            state_id = int(invalid[-3:]); key = invalid[:-3]
            w.states[state_id][key] = 'PER'
        initial = deepcopy((w.states, w.flags)); w.run(body)
        check((w.states, w.flags) == initial, 'Invalid bootstrap scope executes: '+invalid)
    cases.append('Modern, foreign, dynamic, late, calibrated, repeated and either unowned/uncontrolled state cannot be altered')
    for state_id, (relative, _, modern) in start.STATES.items():
        source = before[relative].decode('utf-8')
        target = outputs[relative]
        baseline = start.strip_owned(source)
        check(start.strip_owned(target) == baseline, 'Unrelated state bytes changed')
        check(start.state_history(target, state_id) == target, 'Marked history patch is not idempotent')
        for year, expected in [(1970, 0), (1971, 0), (1990, 0), (2000, modern), (2017, modern)]:
            check(levels(target, (year, 1, 1)).get('composite_plant', 0) == expected, 'Dated plant level is wrong')
        for variant in (baseline.replace('\r\n', '\n').replace('\n', '\r\n'), '\ufeff'+baseline.lstrip('\ufeff')):
            patched = start.state_history(variant, state_id)
            check(start.strip_owned(patched) == variant, 'Newline/BOM or unrelated bytes changed')
        # Exercise an existing later date instead of creating a duplicate key.
        old = '\n\t\t2000.1.1 = {\n\t\t\tbuildings = { offices = 7 }\n\t\t}\n'
        history_end = baseline.index('\n\t}\n', baseline.index('history ='))
        fixture = baseline[:history_end]+old+baseline[history_end:]
        patched = start.state_history(fixture, state_id)
        check(start.strip_owned(patched) == fixture, 'Existing later-history bytes changed')
        check(patched.count('2000.1.1 = {') == 1, 'Duplicate later-date snapshot introduced')
        check(levels(patched, (2000, 1, 1))['offices'] == 7, 'Other later building overwritten')
        check(levels(patched, (2000, 1, 1))['composite_plant'] == modern, 'Later composite restoration missing')
    cases.append('1970/1971/1990 composites0;2000/2017 native1+0; owned patches are byte-reversible, idempotent and preserve existing later dates/BOM/CRLF')
    forbidden = {'ingame_update_setup', 'IMP_1970_apply_starting_gdp_profile', 'clear_variable', 'country_event',
                 'add_building_construction', 'set_building_level'}
    check(not forbidden & {key for key, _, _ in walk(body)}, 'Bootstrap recalibrates economy, grants money or schedules a reset')
    native = (ROOT/'common/buildings/00_buildings.txt').read_text(encoding='utf-8-sig')
    composite = first(first(parse(native), 'buildings'), 'composite_plant')
    check(first(first(composite, 'level_cap'), 'state_max') == '5', 'Native plant cap requires loop-bound review')
    cases.append('No GDP recalibration/economic grants/runtime history event; five-attempt bound matches actual native plant cap')
    hashes = {relative: hashlib.sha256(text.encode('utf-8')).hexdigest() for relative, text in outputs.items()}
    matches = {relative: (ROOT/relative).exists() and (ROOT/relative).read_bytes() == text.encode('utf-8') for relative, text in outputs.items()}
    if installed:
        check(all(matches.values()), 'Installed outputs differ from current pure build')
    report = {'checks': checks, 'passed': True, 'cases': cases, 'outputs': hashes,
              'installed_match': matches, 'installed_check_required': installed, 'engine_tested': False,
              'limit': 'Generated AST and dated-history interpretation only; HOI4 load/save/hover/economy are not emulated.'}
    (HERE/'START_ECONOMY_VALIDATION.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    run(installed='--installed' in sys.argv)
