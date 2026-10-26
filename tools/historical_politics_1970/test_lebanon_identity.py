# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""LEB-only modern-fallback regression using emitted history and native limits."""
from __future__ import annotations
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

from starting_identity import (ROOT, SNAPSHOT_BEGIN, SNAPSHOT_END, parse, emit,
    first, values, walk, history_output, normalise_native_seed, leb_array_input)
from test_starting_identity import later


def marker_seed(text):
    return parse(text.split(SNAPSHOT_BEGIN, 1)[1].split(SNAPSHOT_END, 1)[0])


def execute(seed, scenario, existing=None):
    state = {'variables': {}, 'arrays': {}, 'leaders': [], 'broad': {}, 'flags': set(), 'elections': False}
    if existing:
        state.update(deepcopy(existing))
    def rows(body):
        for key, _, value in body:
            if key == 'if':
                if first(first(value, 'limit', []), 'IMP_is_1970_scenario') == 'yes' and scenario:
                    rows([row for row in value if row[0] != 'limit'])
            elif key == 'set_country_flag':
                state['flags'].add(value)
            elif key == 'set_popularities':
                state['broad'] = {k: float(v) for k, _, v in value}
            elif key == 'set_politics':
                state['elections'] = first(value, 'elections_allowed') == 'yes'
            elif key == 'clear_array':
                state['arrays'][value] = []
            elif key == 'clear_variable':
                state['variables'].pop(value, None)
            elif key == 'resize_array':
                state['arrays'][first(value, 'array')] = [float(first(value, 'value', '0'))] * int(first(value, 'size'))
            elif key == 'set_variable':
                for name, _, number in value:
                    if '^' in name:
                        array, index = name.split('^')
                        target = state['arrays'].setdefault(array, [])
                        while len(target) <= int(index):
                            target.append(0.0)
                        target[int(index)] = float(number)
                    else:
                        state['variables'][name] = float(number)
            elif key == 'add_to_array':
                for array, _, number in value:
                    state['arrays'].setdefault(array, []).append(float(number))
            elif key == 'create_country_leader':
                state['leaders'].append(value)
            elif key != 'set_cosmetic_tag':
                raise AssertionError(('Unsupported emitted LEB leaf', key))
    rows(seed)
    return state


def native_limit(condition, state):
    def variable(name):
        if '^' in name:
            array, index = name.split('^'); entries = state['arrays'].get(array, [])
            return entries[int(index)] if int(index) < len(entries) else 0
        return state['variables'].get(name, 0)
    def leaf(key, op, value):
        if key == 'NOT':
            return not native_limit(value, state)
        if key == 'OR':
            return any(leaf(k, o, v) for k, o, v in value)
        if key == 'check_variable':
            return all(variable(k) > float(v) if o == '>' else variable(k) == float(v) for k, o, v in value)
        if key in state['broad']:
            return state['broad'][key] > float(value) if op == '>' else state['broad'][key] == float(value)
        raise AssertionError(('Unsupported native failsafe condition', key))
    return all(leaf(k, o, v) for k, o, v in condition)


def main():
    checks = 0
    def check(ok, message):
        nonlocal checks
        checks += 1
        assert ok, message
    path = next((ROOT / 'history/countries').glob('LEB - *.txt'))
    profiles = parse((ROOT / 'common/scripted_effects/IMP_1970_world_politics_effects.txt').read_text(encoding='utf-8-sig'))
    raw = path.read_bytes()
    output, _ = history_output(path, profiles)
    installed = marker_seed(output.decode('utf-8-sig'))
    check(later(raw) == later(output), 'LEB native2000tail changed')
    guards = [row for row in installed if row[0] == 'if' and any(leb_array_input(child) for child in row[2])]
    check(len(guards) == 1, 'Missing/duplicated LEB array guard')
    check(first(first(guards[0][2], 'limit'), 'IMP_is_1970_scenario') == 'yes', 'LEB array guard widened')
    check(not any(leb_array_input(row) for row in installed), 'New array leaves remain unconditional')
    check([first(value, 'ruling_party') for value in values(installed, 'set_variable')] == ['1'], 'Raw preview ruling party lost/duplicated')
    check(installed.index(guards[0]) < next(i for i, row in enumerate(installed) if row[0] == 'set_variable'), 'Clear-ruling guard follows raw ruling-party assignment')
    for key in ('set_politics', 'set_popularities', 'create_country_leader'):
        check(len(values(installed, key)) == 1, ('Preview identity became conditional', key))
    before = marker_seed(raw.decode('utf-8-sig'))
    # Recover the previously unconditional1970 seed to compare actual values.
    original = []
    for key, op, value in before:
        if key == 'if' and any(leb_array_input(row) for row in value):
            original += [row for row in value if row[0] != 'limit']
        else:
            original.append((key, op, value))
    historic = execute(installed, True)
    baseline = execute(original, True)
    check(historic == baseline, '1970 arrays/support/coalition changed')
    check(len(historic['arrays']['party_pop_array']) == 24 and historic['arrays']['party_pop_array'][1] == 0.48,
          '1970 native party array not initialized')
    check(historic['arrays']['gov_coalition_array'] == [2.0] and historic['variables']['ruling_party'] == 1,
          '1970 coalition/ruling party changed')
    modern = execute(installed, False)
    check(modern['arrays'] == {} and modern['variables'] == {'ruling_party': 1.0}, 'New arrays leak into later start')
    check(len(modern['leaders']) == 1 and first(modern['leaders'][0], 'name') == '"Charles Helou"', 'Direct authored preview leader lost')
    check(first(modern['leaders'][0], 'expire') == '"1970.9.22"', 'Existing historical expiry changed')
    sentinel = {'arrays': {'party_pop_array': [0.27], 'gov_coalition_array': [9], 'party_banned_array': [1]}}
    check(execute(installed, False, sentinel)['arrays'] == sentinel['arrays'], 'Later preexisting arrays cleared or replaced')
    # Native set_failsafe_values should still see absent arrays in a modern
    # start, while it must retain the complete authored1970 distribution.
    native = first(parse((ROOT / 'common/scripted_effects/00_leader_setup_scripted_effects.txt').read_text(encoding='utf-8-sig')), 'set_failsafe_values')
    native_guards = [first(body, 'limit') for body in values(native, 'if')]
    check(len(native_guards) == 5, 'Native failsafe families changed; review evaluator')
    for condition in native_guards:
        check(native_limit(condition, modern), ('Modern native fallback suppressed', condition))
        check(not native_limit(condition, historic), ('1970 authored distribution lost', condition))
    # A fresh pre-repair source has the same behavior as marker migration.
    fresh = b'''capital = 202
1970.1.1 = {
 if = { limit = { date < 1985.1.1 } IMP_1970_profile_democratic_conservative = yes }
 set_popularities = { democratic = 72 communism = 5 fascism = 2 neutrality = 15 nationalist = 6 }
 set_politics = { ruling_party = democratic last_election = "1968.1.1" election_frequency = 48 elections_allowed = yes }
 set_variable = { ruling_party = 1 }
 create_country_leader = { name = "Charles Helou" picture = "gfx/Leaders/LEB/LEB_Coldwar_Charles_Helou.dds" expire = "1970.9.22" ideology = conservatism }
}
2000.1.1 = { set_country_flag = existing_modern_sentinel }
'''
    with patch.object(Path, 'read_bytes', return_value=fresh):
        transformed, _ = history_output(path, profiles)
    fresh_seed = marker_seed(transformed.decode('utf-8-sig'))
    check(execute(fresh_seed, False)['arrays'] == {}, 'Fresh source leaks arrays into modern start')
    check(execute(fresh_seed, True) == historic, 'Fresh and migrated1970 identities differ')
    check(later(fresh) == later(transformed), 'Fresh native modern tail changed')
    check(normalise_native_seed(installed, 'LEB') == installed, 'LEB guard migration is not idempotent')
    for other in ('FRA', 'USA', 'SOV'):
        other_path = next((ROOT / 'history/countries').glob(other + ' - *.txt'))
        seed = marker_seed(other_path.read_text(encoding='utf-8-sig'))
        check(normalise_native_seed(seed, other) == seed and any(leb_array_input(row) for row in seed),
              (other, 'Other direct native arrays changed'))
    print(json.dumps({'ok': True, 'checks': checks, 'scope': 'LEB only',
                      'history_sha256': hashlib.sha256(output).hexdigest(),
                      'later_sha256': hashlib.sha256(later(output)).hexdigest(), 'engine_tested': False}))


if __name__ == '__main__':
    main()
