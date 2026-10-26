# IMPERIA CW — Cold War: suez 1970 — test lifecycle.
"""Source-driven lifecycle checks; these do not substitute for a HOI4 test."""
from pathlib import Path
import ast
import importlib
import json
import sys
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/israel_1970'))
from script_format import read


def source(relative):
    return (ROOT / relative).read_text(encoding='utf-8-sig')


def value(items, key):
    return next(v for k, op, v in items if k == key)


def extract_block(text, start):
    opening = text.index('{', start)
    depth = 1
    end = opening + 1
    while depth:
        depth += (text[end] == '{') - (text[end] == '}')
        end += 1
    return text[start:end]


def named_block(relative, kind, identity):
    text = source(relative)
    at = text.index('id = ' + identity)
    return value(read(extract_block(text, text.rfind(kind + ' = {', 0, at))), kind)


EFFECTS = dict((k, v) for k, op, v in read(source('common/scripted_effects/mdcw_suez_canal_effects.txt')) if op)
TRIGGERS = dict((k, v) for k, op, v in read(source('common/scripted_triggers/mdcw_suez_canal_triggers.txt')) if op)
FOCUS = value(named_block('common/national_focus/COLDWAR_EGY_1970_focus.txt', 'focus', 'COLDWAR_EGY_reopen_the_suez_canal'), 'completion_reward')
CALLBACK = value(named_block('events/ISR70_policy_events.txt', 'country_event', 'ISR70P.1160'), 'immediate')


class Model:
    """Evaluate only the real Suez snippets' trigger/effect subset, fail closed."""
    def __init__(self, scenario=True):
        self.scenario = scenario
        self.global_flags = set()
        self.countries = {tag: {'flags': set(), 'ideas': set(), 'vars': {'treasury': 1000}} for tag in ('EGY', 'ISR', 'USA')}
        self.controls = {'214': 'EGY', '213': 'ISR'}
        self.damaged = False
        self.wars = set()
        self.temp = {}
        self.broadcasts = []
        self.root = 'EGY'

    def test(self, items, scope='EGY'):
        return all(self.condition(k, v, scope) for k, op, v in items if op)

    def condition(self, key, argument, scope):
        country = self.countries.get(scope, {'flags': set(), 'ideas': set(), 'vars': {}})
        if key == 'AND': return self.test(argument, scope)
        if key == 'OR': return any(self.condition(k, v, scope) for k, op, v in argument if op)
        if key == 'NOT': return not self.test(argument, scope)
        if key == 'IMP_is_1970_scenario': return self.scenario
        if key in TRIGGERS: return self.test(TRIGGERS[key], scope)
        if key in ('EGY', 'ISR', '214', '213'): return self.test(argument, key)
        if key == 'has_global_flag': return argument in self.global_flags
        if key == 'has_country_flag': return argument in country['flags']
        if key == 'has_idea': return argument in country['ideas']
        if key == 'country_exists': return argument in self.countries
        if key == 'has_dynamic_modifier': return scope == '214' and self.damaged
        if key == 'is_controlled_by': return self.controls.get(scope) == (self.root if argument == 'ROOT' else argument)
        if key == 'controls_state': return self.controls.get(argument) == scope
        if key == 'original_tag': return scope == argument
        if key == 'has_war_with': return frozenset((scope, argument)) in self.wars
        raise AssertionError('Unsupported Suez trigger: ' + key)

    def number(self, token, scope):
        try: return float(token)
        except ValueError: return self.countries[scope]['vars'].get(token, self.temp.get(token, 0))

    def run(self, items, scope='EGY'):
        previous = False
        for key, op, argument in items:
            if not op: continue
            if key in ('if', 'else_if', 'else'):
                eligible = key == 'if' or not previous
                passed = eligible and (key == 'else' or self.test(value(argument, 'limit'), scope))
                if key == 'if': previous = passed
                else: previous = previous or passed
                if passed: self.run([item for item in argument if item[0] != 'limit'], scope)
                continue
            previous = False
            if key in EFFECTS: self.run(EFFECTS[key], scope)
            elif key == 'mdcw_suez_update_world': self.broadcasts.append('SUEZ_CANAL_BLOCKED' in self.global_flags)
            elif key in ('EGY', 'ISR'): self.run(argument, key)
            elif key == 'hidden_effect': self.run(argument, scope)
            elif key == 'set_global_flag': self.global_flags.add(argument)
            elif key == 'clr_global_flag': self.global_flags.discard(argument)
            elif key == 'set_country_flag': self.countries[scope]['flags'].add(argument)
            elif key == 'clr_country_flag': self.countries[scope]['flags'].discard(argument)
            elif key == 'remove_ideas': self.countries[scope]['ideas'].discard(argument)
            elif key == 'add_ideas': self.countries[scope]['ideas'].add(argument)
            elif key == 'clear_variable': self.countries[scope]['vars'].pop(argument, None)
            elif key == 'set_temp_variable':
                name, _, token = argument[0]
                self.temp[name] = self.number(token, scope)
            elif key == 'modify_treasury_effect': self.countries[scope]['vars']['treasury'] += self.temp['treasury_change']
            elif key == 'COLDWAR_EGY_pay_gdp_share': self.countries[scope]['vars']['treasury'] -= 1000 * self.temp['COLDWAR_EGY_gdp_share']
            elif key != 'log': raise AssertionError('Unsupported Suez effect: ' + key)

    def refresh(self):
        self.run(EFFECTS['mdcw_suez_refresh_canal_blockage'])

    def start_project(self):
        self.countries['EGY']['flags'].add('ISR70_policy_egypt_canal_project')
        self.countries['EGY']['vars'].update(ISR70_policy_egypt_canal_paid=8, treasury=992)


class SuezLifecycleTests(unittest.TestCase):
    def test_historical_closure_survives_egypt_annexation(self):
        game = Model()
        del game.countries['EGY']
        game.refresh()
        game.refresh()
        self.assertIn('SUEZ_CANAL_BLOCKED', game.global_flags)
        self.assertEqual(game.broadcasts, [True])

    def test_later_scenario_has_no_historical_closure(self):
        game = Model(scenario=False)
        game.refresh()
        self.assertNotIn('SUEZ_CANAL_BLOCKED', game.global_flags)
        self.assertEqual(game.broadcasts, [])

    def test_reopening_does_not_clear_other_closure_causes(self):
        for damage, ship in ((True, False), (False, True), (True, True)):
            with self.subTest(damage=damage, ship=ship):
                game = Model()
                game.refresh()
                game.damaged = damage
                if ship: game.countries['EGY']['ideas'].add('suez_canal_blocked')
                game.run(EFFECTS['mdcw_suez_reopen_historical_canal'])
                self.assertIn('SUEZ_CANAL_BLOCKED', game.global_flags)
                self.assertEqual(game.broadcasts, [True])
                game.damaged = False
                game.countries['EGY']['ideas'].discard('suez_canal_blocked')
                game.refresh()
                self.assertEqual(game.broadcasts, [True, False])

    def test_old_focus_receipt_migrates_without_replaying_rewards(self):
        game = Model()
        game.countries['EGY']['flags'].add('COLDWAR_EGY_canal_reopened')
        game.countries['EGY']['ideas'].add('COLDWAR_EGY_the_closed_canal')
        game.refresh()
        self.assertIn('ISR70_policy_canal_open', game.global_flags)
        self.assertNotIn('COLDWAR_EGY_the_closed_canal', game.countries['EGY']['ideas'])
        self.assertEqual(game.countries['EGY']['vars']['treasury'], 1000)
        self.assertNotIn('COLDWAR_EGY_suez_canal_authority', game.countries['EGY']['ideas'])

    def test_decision_reopens_once_without_focus_authority_reward(self):
        game = Model()
        game.countries['EGY']['ideas'].add('COLDWAR_EGY_the_closed_canal')
        game.refresh()
        game.start_project()
        game.run(CALLBACK)
        game.run(CALLBACK)
        self.assertIn('ISR70_policy_canal_open', game.global_flags)
        self.assertIn('COLDWAR_EGY_canal_reopened', game.countries['EGY']['flags'])
        self.assertEqual(game.countries['EGY']['vars']['treasury'], 992)
        self.assertNotIn('COLDWAR_EGY_suez_canal_authority', game.countries['EGY']['ideas'])
        self.assertNotIn('COLDWAR_EGY_the_closed_canal', game.countries['EGY']['ideas'])
        self.assertEqual(game.broadcasts, [True, False])

    def test_focus_refunds_pending_decision_and_late_callback_is_inert(self):
        game = Model()
        game.refresh()
        game.start_project()
        game.run(FOCUS)
        game.run(CALLBACK)
        game.run(CALLBACK)
        self.assertEqual(game.countries['EGY']['vars']['treasury'], 990)
        self.assertIn('COLDWAR_EGY_suez_canal_authority', game.countries['EGY']['ideas'])
        self.assertNotIn('ISR70_policy_egypt_canal_project', game.countries['EGY']['flags'])
        self.assertEqual(game.broadcasts, [True, False])

    def test_lost_control_blocks_focus_reward_and_refunds_decision(self):
        game = Model()
        game.start_project()
        game.controls['214'] = 'ISR'
        game.run(FOCUS)
        self.assertNotIn('ISR70_policy_canal_open', game.global_flags)
        self.assertNotIn('COLDWAR_EGY_suez_canal_authority', game.countries['EGY']['ideas'])
        game.run(CALLBACK)
        self.assertEqual(game.countries['EGY']['vars']['treasury'], 1000)

    def test_focus_and_decision_keep_their_distinct_wartime_guards(self):
        game = Model()
        game.wars.add(frozenset(('EGY', 'ISR')))
        game.controls['213'] = 'EGY'
        game.run(FOCUS)
        self.assertIn('ISR70_policy_canal_open', game.global_flags)
        decision = Model()
        decision.wars = game.wars
        decision.controls['213'] = 'EGY'
        decision.start_project()
        decision.run(CALLBACK)
        self.assertNotIn('ISR70_policy_canal_open', decision.global_flags)
        self.assertEqual(decision.countries['EGY']['vars']['treasury'], 1000)

    def test_already_open_decision_reservation_is_refunded_once(self):
        game = Model()
        game.global_flags.add('ISR70_policy_canal_open')
        game.start_project()
        game.run(CALLBACK)
        game.run(CALLBACK)
        self.assertEqual(game.countries['EGY']['vars']['treasury'], 1000)

    def test_income_requires_navigation_for_both_control_spirits(self):
        money = source('common/scripted_effects/00_money_system.txt')
        for spirit in ('full_control_of_suez', 'partial_control_of_suez'):
            at = money.index('has_idea = ' + spirit)
            clause = value(read(extract_block(money, money.rfind('if = {', 0, at))), 'if')
            gate = value(clause, 'limit')
            for scenario in (True, False):
                with self.subTest(spirit=spirit, scenario=scenario):
                    game = Model(scenario=scenario)
                    game.countries['EGY']['ideas'].add(spirit)
                    game.global_flags.add('ISR70_policy_canal_open')
                    self.assertTrue(game.test(gate))
                    game.global_flags.add('SUEZ_CANAL_BLOCKED')
                    self.assertFalse(game.test(gate))

    def test_israel_generator_matches_callback_and_preserves_income_gates(self):
        compiler = importlib.import_module('policy_world')
        callbacks = []
        def event(number, title, description, options, **kwargs):
            callbacks.append(options[0][1])
            return 'ISR70P.' + str(number)
        api = SimpleNamespace(root=ROOT, tick=[], money=lambda share: 'ISR70_policy_pay_0_0080 = yes', event=event, loc=lambda *args: None)
        compiler.register(api)
        self.assertEqual(read(callbacks[0]), CALLBACK)
        emitted = {}
        compiler.patch(api, lambda name, text, **kwargs: emitted.update({name: text}))
        self.assertEqual(emitted['common/scripted_effects/00_money_system.txt'], source('common/scripted_effects/00_money_system.txt'))

    def test_egypt_compiler_matches_installed_focus_reward(self):
        directory = ROOT / 'Claude outputs/COLDWAR_EGY_generator'
        sys.path.insert(0, str(directory))
        compiler = ast.parse(source('Claude outputs/COLDWAR_EGY_generator/cw_compile.py'))
        definition = next(node for node in compiler.body if isinstance(node, ast.FunctionDef) and node.name == 'focus_effects')
        effects = importlib.import_module('cw_effects')
        namespace = {'E': effects, 'R': effects.R, 'MAN': effects.MAN, 'EVLINES': effects.EVLINES, 'cid': importlib.import_module('cw_common').cid}
        exec(compile(ast.Module(body=[definition], type_ignores=[]), '<focus_effects only>', 'exec'), namespace)
        design = json.loads(source('Claude outputs/COLDWAR_EGY_generator/egy_tree.json'))
        focus = next(item for item in design['foci'] if item['id'] == 'EGY_1970_reopen_the_suez_canal')
        self.assertEqual(read('\n'.join(namespace['focus_effects'](focus))), FOCUS)


if __name__ == '__main__':
    unittest.main()
