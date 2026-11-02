# IMPERIA COLD WAR — Independent strict-AST national-grant transaction model.
"""Exercise emitted script, not a reimplementation of grant selection.

This is a bounded source/model test, not a native-engine or multiplayer test.
The interpreter rejects unsupported statements. It executes installed alias
providers and actual EGY capacity triggers. Lifecycle fixtures are compiled by
the real programme API under a temporary in-memory scope, with no file writes.
Money projects only the native treasury-change ledger; debt is out of scope.
Random selection uses the first legal distinct sample, not a model of HOI4 RNG.
Collection comparisons are strict, matching the observed engine correction.
"""
from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from focus_prerequisite_ui import nodes, field
from building_grants import grants


class UnsupportedScript(AssertionError):
    pass


def number(value):
    try:
        return Decimal(str(value))
    except Exception as exc:
        raise UnsupportedScript(('Not a number', value)) from exc


class World:
    def __init__(self, effects, triggers=None, actions=None):
        self.effects = effects; self.triggers = triggers or {}; self.actions = actions or {}
        self.tag = 'EGY'; self.tree = 'TEST_GRANT_TREE'; self.scenario = True
        self.variables = {'treasury': Decimal(100), 'ruling_party': Decimal(2)}
        self.flags = set(); self.completed = {'TEST_PARENT'}; self.states = {}; self.events = []

    def state(self, sid, level=0, building='infrastructure', owner='EGY', controller=None, home=True):
        self.states[sid] = {'owner': owner, 'controller': owner if controller is None else controller,
                            'home': home, 'levels': {building: level}, 'variables': {},
                            'flags': set(), 'slots': 0}
        return self

    def variables_at(self, scope):
        return self.variables if scope is None else self.states[scope]['variables']

    def value(self, name, scope):
        if str(name).startswith('building_level@'):
            if scope is None: raise UnsupportedScript('Building level read in country scope')
            return number(self.states[scope]['levels'].get(name.split('@')[1], 0))
        try: return Decimal(str(name))
        except Exception: return number(self.variables_at(scope).get(str(name), 0))

    def owned(self):
        return sorted(sid for sid, state in self.states.items() if state['owner'] == self.tag)

    def condition(self, row, scope=None):
        key, value, children = row.key, row.value, row.children()
        if key in ('AND', 'limit', 'custom_trigger_tooltip'):
            return all(self.condition(c, scope) for c in children if c.key != 'tooltip')
        if key == 'OR': return any(self.condition(c, scope) for c in children)
        if key == 'NOT': return not all(self.condition(c, scope) for c in children)
        if key == 'ROOT': return all(self.condition(c, None) for c in children)
        if key.isdigit(): return all(self.condition(c, int(key)) for c in children)
        if key == 'always': return value == 'yes'
        if key == 'tag': return self.tag == value
        if key == 'exists': return value == 'yes'
        if key == 'has_focus_tree': return self.tree == value
        if key == 'IMP_is_1970_scenario': return self.scenario == (value == 'yes')
        if key == 'has_completed_focus': return value in self.completed
        if key == 'has_country_flag': return value in self.flags
        if key == 'has_state_flag':
            if scope is None: raise UnsupportedScript('State flag in country scope')
            return value in self.states[scope]['flags']
        if key == 'is_owned_and_controlled_by':
            if scope is None or value != 'ROOT': raise UnsupportedScript((key, value, scope))
            state = self.states[scope]
            return state['owner'] == state['controller'] == self.tag
        if key == 'is_in_home_area': return self.states[scope]['home'] == (value == 'yes')
        if key == 'any_owned_state':
            return any(all(self.condition(c, sid) for c in children) for sid in self.owned())
        if key == 'check_variable':
            variable = field(children, 'var')
            if variable is not None:
                left = self.value(variable, scope); right = self.value(field(children, 'value'), scope)
                compare = field(children, 'compare', 'equals')
            else:
                if len(children) != 1: raise UnsupportedScript(('Ambiguous check', children))
                check = children[0]; left = self.value(check.key, scope); right = self.value(check.value, scope)
                compare = check.op
            comparisons = {'=': left == right, 'equals': left == right, '>': left > right,
                           '<': left < right, '>=': left >= right, '<=': left <= right,
                           'less_than_or_equals': left <= right, 'greater_than_or_equals': left >= right}
            if compare not in comparisons: raise UnsupportedScript(('Comparison', compare))
            return comparisons[compare]
        if key == 'collection_size':
            # Deliberately strict native AST shape. A malformed/flattened input
            # cannot be accepted by this model as though it selected states.
            if scope is not None: raise UnsupportedScript('Collection root is not country')
            inp = next(c for c in children if c.key == 'input')
            if field(inp.children(), 'input') != 'game:scope': raise UnsupportedScript('Collection source')
            operators = next(c for c in inp.children() if c.key == 'operators')
            bare = [c.value for c in operators.children() if c.key == '_bare']
            if bare != ['owned_states']: raise UnsupportedScript(('Collection operator', bare))
            limit = next(c for c in operators.children() if c.key == 'limit')
            size = sum(self.condition(limit, sid) for sid in self.owned())
            comparison = next(c for c in children if c.key == 'value')
            if comparison.op != '>': raise UnsupportedScript(('Collection comparison', comparison.op))
            return size > int(comparison.value)
        if key in self.triggers and value == 'yes':
            return all(self.condition(c, scope) for c in self.triggers[key].children())
        raise UnsupportedScript(('Trigger', key, row.op, value, scope))

    def execute(self, rows, scope=None, depth=0):
        if depth > 60: raise UnsupportedScript('Effect recursion')
        index = 0
        while index < len(rows):
            row = rows[index]; index += 1
            key, value, children = row.key, row.value, row.children()
            if key == 'if':
                chain = [row]
                while index < len(rows) and rows[index].key in ('else_if', 'else'):
                    chain.append(rows[index]); index += 1
                for branch in chain:
                    limits = [c for c in branch.children() if c.key == 'limit']
                    if branch.key == 'else' or all(self.condition(c, scope) for c in limits):
                        self.execute([c for c in branch.children() if c.key != 'limit'], scope, depth + 1)
                        break
            elif key in ('else', 'else_if'):
                raise UnsupportedScript('Unpaired conditional branch')
            elif key == 'effect_tooltip':
                continue
            elif key in ('hidden_effect', 'effect'):
                self.execute(children, scope, depth + 1)
            elif key == 'ROOT':
                self.execute(children, None, depth + 1)
            elif key.isdigit():
                self.execute(children, int(key), depth + 1)
            elif key == 'every_owned_state':
                limits = [c for c in children if c.key == 'limit']
                eligible = [sid for sid in self.owned() if all(self.condition(c, sid) for c in limits)]
                amount = field(children, 'random_select_amount')
                chosen = eligible if amount is None else eligible[:int(amount)]
                for sid in chosen:
                    self.execute([c for c in children if c.key not in ('limit', 'random_select_amount')], sid, depth + 1)
            elif key in ('set_temp_variable', 'set_variable', 'subtract_from_temp_variable'):
                if len(children) != 1: raise UnsupportedScript(('Variable mutation', key))
                change = children[0]; variables = self.variables_at(scope)
                operand = self.value(change.value, scope)
                variables[change.key] = variables.get(change.key, Decimal(0)) - operand if key.startswith('subtract') else operand
            elif key in ('set_country_flag', 'clr_country_flag'):
                if scope is not None: raise UnsupportedScript('Country receipt in state scope')
                self.flags.add(value) if key == 'set_country_flag' else self.flags.discard(value)
            elif key in ('set_state_flag', 'clr_state_flag'):
                if scope is None: raise UnsupportedScript('State receipt in country scope')
                flags = self.states[scope]['flags']
                flags.add(value) if key == 'set_state_flag' else flags.discard(value)
            elif key == 'add_extra_state_shared_building_slots':
                if scope is None: raise UnsupportedScript('Slot without state')
                self.states[scope]['slots'] += int(value); self.events.append(('slot', scope, int(value)))
            elif key == 'add_building_construction':
                if scope is None or field(children, 'instant_build') != 'yes': raise UnsupportedScript('Unmodelled construction')
                kind = field(children, 'type'); quantity = int(field(children, 'level'))
                target = self.states[scope]['levels'].get(kind, 0) + quantity
                if target > int(grants.building_definitions()[kind]['state_max']): raise UnsupportedScript('Physical overgrant')
                self.states[scope]['levels'][kind] = target; self.events.append(('building', scope, quantity))
            elif key == 'modify_treasury_effect':
                if scope is not None: raise UnsupportedScript('Treasury charged on state')
                self.variables['treasury'] += self.variables.get('treasury_change', Decimal(0))
            elif key in self.effects and value == 'yes':
                self.execute(self.effects[key].children(), scope, depth + 1)
            else:
                raise UnsupportedScript(('Effect', key, row.op, value, scope))

    def call(self, name, scope=None):
        self.execute(self.effects[name].children(), scope)

    def tick(self):
        self.execute(self.actions['on_daily_EGY'].children())


class NativeGrantModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        native = (ROOT / 'common/scripted_effects/COLDWAR_GRANT_native.txt').read_text(encoding='utf-8')
        cls.native = {n.key: n for n in nodes(native)}
        actual = (ROOT / 'common/scripted_triggers/COLDWAR_GRANT_programmes.txt').read_text(encoding='utf-8')
        cls.actual_triggers = {n.key: n for n in nodes(actual)}
        fixture = '''focus_tree = { id = TEST_GRANT_TREE
 focus = { id = TEST_PARENT x = 0 y = 0 }
 focus = { id = TEST_FOCUS x = 0 y = 1 cost = 1
  prerequisite = { focus = TEST_PARENT focus = TEST_ALTERNATIVE }
  mutually_exclusive = { focus = TEST_EXCLUDED }
  available = { check_variable = { ruling_party = 2 } }
  completion_reward = { one_random_infrastructure = yes }
 } }'''
        spec = {'EGY': {'tree': 'unused_fixture.txt', 'focuses': ['TEST_FOCUS']}}
        with patch.object(grants, 'scope', return_value=spec), patch.object(grants, '_TREES', {'EGY': fixture}), patch.object(grants, '_RECORDS', {}):
            effects, triggers, actions, _ = grants._programme_outputs()
        cls.programmes = {n.key: n for n in nodes('\n'.join(effects))}
        cls.triggers = {n.key: n for n in nodes('\n'.join(triggers))}
        cls.actions = {n.key: n for n in nodes('\n'.join(actions))}

    def world(self, programme=False):
        return World({**self.native, **(self.programmes if programme else {})},
                     self.triggers if programme else {}, self.actions if programme else {})

    def alias(self, name): return grants.alias(name)
    def complete(self): return grants.PREFIX + 'complete_TEST_FOCUS'

    def test_01_preview_does_not_mutate(self):
        w = self.world().state(1)
        snapshot = deepcopy((w.variables, w.states, w.flags))
        preview = next(c for c in self.native[self.alias('one_random_infrastructure')].children() if c.key == 'effect_tooltip')
        w.execute([preview])
        self.assertEqual((w.variables, w.states, w.flags), snapshot)

    def test_02_one_charge_and_slots_precede_actual_building(self):
        w = self.world().state(1); w.call(self.alias('one_random_infrastructure'))
        self.assertEqual(w.variables['treasury'], Decimal('96.5'))
        self.assertEqual(w.events, [('slot', 1, 1), ('building', 1, 1)])

    def test_03_native_deficit_is_allowed(self):
        w = self.world().state(1); w.variables['treasury'] = Decimal(0)
        w.call(self.alias('one_random_infrastructure'))
        self.assertEqual(w.variables['treasury'], Decimal('-3.5'))

    def test_04_country_skip_preserves_asset_without_extra_fee(self):
        w = self.world().state(1); w.variables['skip_payment'] = Decimal(1)
        w.call(self.alias('one_random_infrastructure'))
        self.assertEqual(w.variables['treasury'], Decimal(100)); self.assertEqual(w.states[1]['slots'], 1)

    def test_05_state_helper_reads_skip_from_country_root(self):
        w = self.world().state(1); w.variables['skip_payment'] = Decimal(1)
        w.call(self.alias('one_state_infrastructure'), 1)
        self.assertEqual(w.variables['treasury'], Decimal(100)); self.assertEqual(w.states[1]['slots'], 1)

    def test_06_state_helper_charges_country_not_state(self):
        w = self.world().state(1); w.states[1]['variables']['treasury'] = Decimal(999)
        w.call(self.alias('one_state_infrastructure'), 1)
        self.assertEqual(w.variables['treasury'], Decimal('96.5'))
        self.assertEqual(w.states[1]['variables']['treasury'], Decimal(999))

    def test_07_foreign_fixed_state_falls_back_to_own_controlled_state(self):
        w = self.world().state(1, owner='OTHER').state(2)
        w.call(self.alias('one_state_infrastructure'), 1)
        self.assertEqual(w.states[1]['slots'], 0); self.assertEqual(w.states[2]['slots'], 1)

    def test_08_at_cap_produces_no_asset_or_charge(self):
        w = self.world().state(1, level=6); w.call(self.alias('one_random_infrastructure'))
        self.assertEqual(w.variables['treasury'], Decimal(100)); self.assertEqual(w.events, [])

    def test_09_enemy_control_is_excluded(self):
        w = self.world().state(1, controller='OTHER'); w.call(self.alias('one_random_infrastructure'))
        self.assertEqual(w.variables['treasury'], Decimal(100)); self.assertEqual(w.events, [])

    def test_10_two_distinct_state_batch_rejects_one_wide_state(self):
        w = self.world().state(1); w.call(self.alias('two_random_infrastructure'))
        self.assertEqual(w.variables['treasury'], Decimal(100)); self.assertEqual(w.events, [])

    def test_11_exactly_two_distinct_states_are_sufficient(self):
        w = self.world().state(1, level=5).state(2, level=5)
        w.call(self.alias('two_random_infrastructure'))
        self.assertEqual([w.states[i]['levels']['infrastructure'] for i in [1, 2]], [6, 6])
        self.assertEqual(w.variables['treasury'], Decimal(93)); self.assertTrue(all(not s['flags'] for s in w.states.values()))

    def test_12_home_states_are_preferred(self):
        w = self.world().state(1, home=False).state(2).state(3)
        w.call(self.alias('two_random_infrastructure'))
        self.assertEqual([w.states[i]['slots'] for i in [1, 2, 3]], [0, 1, 1])

    def test_13_home_shortfall_uses_distinct_nonhome_fallback(self):
        w = self.world().state(1).state(2, home=False).state(3, home=False)
        w.call(self.alias('three_random_infrastructure'))
        self.assertEqual([w.states[i]['slots'] for i in [1, 2, 3]], [1, 1, 1])
        self.assertEqual(w.variables['treasury'], Decimal('89.5')); self.assertTrue(all(not s['flags'] for s in w.states.values()))

    def test_14_collection_comparison_is_strict_at_zero_one_two(self):
        row = nodes(grants._count_states('infrastructure', 2))[0]
        for count in [0, 1, 2]:
            with self.subTest(count=count):
                w = self.world()
                for sid in range(count): w.state(sid)
                self.assertEqual(w.condition(row), count >= 2)

    def test_15_actual_egy_two_plant_preflight_checks_total_physical_room(self):
        trigger = self.actual_triggers['COLDWAR_GRANT_capacity_COLDWAR_EGY_fn_shumans_legacy']
        worlds = [(self.world().state(218, level=20, building='renewable_energy_infra'), False),
                  (self.world().state(218, level=19, building='renewable_energy_infra'), False),
                  (self.world().state(218, level=18, building='renewable_energy_infra'), True),
                  (self.world().state(218, level=19, building='renewable_energy_infra').state(219, level=19, building='renewable_energy_infra'), True)]
        for w, expected in worlds:
            with self.subTest(states=w.states): self.assertEqual(all(w.condition(c) for c in trigger.children()), expected)

    def test_16_pending_resume_delivers_complete_package_once(self):
        w = self.world(True).state(1, level=6); w.call(self.complete())
        self.assertIn('COLDWAR_GRANT_pending_TEST_FOCUS', w.flags); self.assertEqual(w.variables['treasury'], Decimal(100))
        w.states[1]['levels']['infrastructure'] = 5; w.completed.add('TEST_FOCUS'); w.tick()
        self.assertEqual(w.variables['treasury'], Decimal('96.5'))
        self.assertIn('COLDWAR_GRANT_done_TEST_FOCUS', w.flags)
        self.assertNotIn('COLDWAR_GRANT_pending_TEST_FOCUS', w.flags)
        self.assertNotIn('COLDWAR_GRANT_any_pending', w.flags)

    def test_17_repeated_completion_and_daily_tick_are_inert(self):
        w = self.world(True).state(1); w.call(self.complete()); snapshot = deepcopy((w.variables['treasury'], w.events, w.states))
        w.call(self.complete()); w.completed.add('TEST_FOCUS'); w.tick(); w.tick()
        self.assertEqual((w.variables['treasury'], w.events, w.states), snapshot)

    def test_18_party_predecessor_exclusion_and_scenario_are_rechecked(self):
        for fail in ['party', 'predecessor', 'exclusion', 'scenario']:
            with self.subTest(fail=fail):
                w = self.world(True).state(1)
                if fail == 'party': w.variables['ruling_party'] = Decimal(1)
                if fail == 'predecessor': w.completed.clear()
                if fail == 'exclusion': w.completed.add('TEST_EXCLUDED')
                if fail == 'scenario': w.scenario = False
                w.call(self.complete()); self.assertEqual(w.events, []); self.assertEqual(w.variables['treasury'], Decimal(100))
        w = self.world(True).state(1); w.completed = {'TEST_ALTERNATIVE'}; w.call(self.complete())
        self.assertEqual(w.states[1]['slots'], 1)

    def test_19_already_completed_save_migrates_without_replay(self):
        w = self.world(True).state(1); w.completed.add('TEST_FOCUS'); w.tick()
        self.assertIn('COLDWAR_GRANT_done_TEST_FOCUS', w.flags)
        self.assertEqual(w.events, []); self.assertEqual(w.variables['treasury'], Decimal(100))
        w.call(self.complete()); self.assertEqual(w.events, [])

    def test_20_unknown_authored_statements_fail_closed(self):
        w = self.world()
        with self.assertRaises(UnsupportedScript): w.execute(nodes('unexpected_effect = yes'))
        with self.assertRaises(UnsupportedScript): w.condition(nodes('unexpected_trigger = yes')[0])


if __name__ == '__main__':
    unittest.main()
