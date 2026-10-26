# IMPERIA CW — Cold War: execute native research initialization with the revised GDP ladder.
"""Regression checks for real script ASTs; not an HOI4 runtime simulation."""
from copy import deepcopy
from pathlib import Path
import importlib.util
import json
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools/guest_workers'))
import validate as V
import build


def read(relative):
    return V.parse((ROOT / relative).read_text(encoding='utf-8-sig'))


EFFECTS = {k: v for rel in ('common/scripted_effects/00_research_slots_effects.txt', build.EFFECT_PATH)
           for k, _, v in read(rel)}
TRIGGERS = {k: v for k, _, v in read('common/scripted_triggers/IMP_cold_war_scenario_triggers.txt')}
GLOBALS = V.first(read(build.STARTUP_PATH), 'setup_global_arrays')
DEFAULTS = [node for node in GLOBALS if node[0] == 'set_variable'
            and any(k.startswith(('GLOBAL.gdp_slot^', 'GLOBAL.gdp_c_slot^')) for k, _, _ in node[2])]
GUI = V.first(read('common/scripted_guis/01_research_scripted_gui.txt'), 'scripted_gui')
CLICKS = dict((k, v) for k, _, v in V.first(V.first(GUI, 'MD_research_slot_gui'), 'triggers'))
SNAPSHOT = json.loads((HERE / 'start_snapshot.json').read_text(encoding='utf-8'))
COUNTRIES = {row['tag']: row for row in SNAPSHOT['countries']}


class Machine(V.ScriptMachine):
    def __init__(self, row=None, start=(1970, 1, 1)):
        super().__init__(EFFECTS, TRIGGERS)
        self.global_scope = V.Country('GLOBAL')
        self.start = start
        self.current.research_slots = 0
        self.current.decisions = set()
        self.current.civs = V.D((row or {}).get('civilian_factories', '100'))
        self.current.variables.update(gdp_total=V.D((row or COUNTRIES['USA'])['gdp_internal']),
                                      gdp_per_capita=V.D((row or COUNTRIES['USA'])['gdpc_internal']))
        self.execute(DEFAULTS)

    def scope(self, name):
        if name.lower() == 'global':
            return self.global_scope
        return super().scope(name)

    def test(self, body):
        for key, op, value in body:
            if key == 'has_start_date':
                result = self.compare(self.start, op, tuple(map(int, value.split('.'))))
            elif key == 'num_of_civilian_factories':
                result = self.compare(self.current.civs, op, self.expression(value))
            elif key == 'has_decision':
                result = value in self.current.decisions
            elif key == 'if':
                condition = V.first(value, 'limit')
                result = not self.test(condition) or self.test([n for n in value if n[0] != 'limit'])
            else:
                result = super().test([(key, op, value)])
            if not result:
                return False
        return True

    def execute(self, body):
        if not any(k in {'set_research_slots', 'add_research_slot'} for k, _, v in body):
            return super().execute(body)
        # Native initialization consists of independent if blocks, not an else chain.
        assert not any(k in {'else', 'else_if'} for k, _, v in body)
        for key, op, value in body:
            if key == 'set_research_slots':
                self.current.research_slots = int(self.expression(value))
            elif key == 'add_research_slot':
                self.current.research_slots += int(self.expression(value))
            else:
                super().execute([(key, op, value)])

    def initialize(self):
        self.call(build.EFFECT)
        self.call('research_slot_init_for_country')


class ResearchBalanceTests(unittest.TestCase):
    def test_observed_usa_start_changes_only_its_gdp_slots(self):
        old = Machine(COUNTRIES['USA'])
        old.call('research_slot_init_for_country')
        new = Machine(COUNTRIES['USA'])
        new.initialize()
        self.assertEqual((old.current.research_slots, new.current.research_slots), (6, 4))
        self.assertEqual((old.get('research_slots_from_gdp'), new.get('research_slots_from_gdp')), (4, 2))
        self.assertEqual((old.get('research_slots_from_gdp_c'), new.get('research_slots_from_gdp_c')), (2, 2))

    def test_all_observed_countries_keep_their_development_slots(self):
        self.assertEqual(len(COUNTRIES), 163)
        for tag, row in COUNTRIES.items():
            with self.subTest(country=tag):
                old, new = Machine(row), Machine(row)
                old.call('research_slot_init_for_country')
                new.initialize()
                self.assertEqual(old.get('research_slots_from_gdp_c'), new.get('research_slots_from_gdp_c'))
                self.assertGreaterEqual(new.current.research_slots, 2)
                self.assertLessEqual(new.current.research_slots, 4)

    def test_development_thresholds_are_unchanged_even_on_reload(self):
        m = Machine()
        before = {k: v for k, v in m.global_scope.variables.items() if k.startswith('gdp_c_slot^')}
        m.initialize()
        hook = V.first(V.first(V.first(read(build.HOOK_PATH), 'on_actions'), 'on_startup'), 'effect')
        m.execute(hook)
        after = {k: v for k, v in m.global_scope.variables.items() if k.startswith('gdp_c_slot^')}
        self.assertEqual(before, after)
        self.assertEqual([after[f'gdp_c_slot^{i}'] for i in range(1, 7)],
                         list(map(V.D, SNAPSHOT['original_development_thresholds'])))

    def test_modern_campaign_keeps_its_native_economic_thresholds(self):
        m = Machine(start=(2000, 1, 1))
        before = deepcopy(m.global_scope.variables)
        m.call('research_slot_init_for_country')
        original_slots = m.current.research_slots
        m.initialize()
        for key, value in before.items():
            self.assertEqual(m.global_scope.variables[key], value)
        self.assertEqual(m.current.research_slots, original_slots)

    def test_loading_only_refreshes_thresholds_not_country_research(self):
        m = Machine()
        m.initialize()
        m.current.variables['active_research_progress'] = V.D('0.65')
        before = deepcopy(m.current.variables)
        m.call(build.EFFECT)
        m.call(build.EFFECT)
        self.assertEqual(m.current.variables, before)
        self.assertEqual(m.current.research_slots, 4)
        self.assertNotIn('research_slot_init_for_country',
                         [k for k, _, v in V.walk(read(build.HOOK_PATH))])

    def test_next_gdp_slot_has_real_boundary_and_keeps_existing_cooldown(self):
        m = Machine()
        m.initialize()
        trigger = CLICKS['gdp_slot_gain_industry_size_click_enabled']
        self.assertFalse(m.test(trigger))
        m.current.variables['gdp_total'] = V.D(6800)
        self.assertFalse(m.test(trigger))  # Native comparisons use strict greater-than.
        m.current.variables['gdp_total'] += V.D('0.01')
        self.assertTrue(m.test(trigger))
        m.current.flags['gdp_gain_industry_slot_flag'] = V.D(240)
        self.assertFalse(m.test(trigger))
        m.current.flags.clear()
        m.current.decisions.add('gdp_gain_slot')
        self.assertFalse(m.test(trigger))

    def test_existing_rich_small_country_factory_requirement_still_applies(self):
        m = Machine()
        m.current.variables.update(gdp_total=V.D(1), gdp_per_capita=V.D(50))
        m.current.civs = V.D(0)
        m.initialize()
        self.assertEqual(m.current.research_slots, 2)
        self.assertEqual(m.get('research_slots_from_gdp_c'), 1)

    def test_ui_gdp_thresholds_match_internal_comparisons(self):
        data = json.loads((HERE / 'balance.json').read_text(encoding='utf-8'))
        m = Machine()
        m.initialize()
        for i, nominal in enumerate(data['gdp_billions_1970'], 1):
            self.assertEqual(m.get(f'GLOBAL.cw_research_gdp_display^{i}'), V.D(nominal))
            self.assertEqual(m.get(f'GLOBAL.gdp_slot^{i}'), V.D(nominal) * V.D('3.4'))
        text = (ROOT / build.LOC_PATH).read_text(encoding='utf-8-sig')
        self.assertNotIn('GLOBAL.gdp_slot^', text)
        self.assertIn('GLOBAL.cw_research_gdp_display^next_slot_from_gdp', text)
        actual = dict(re.findall(r'^ ([\w.]+):\s*(.*)$', text, re.M))
        for key, before in SNAPSHOT['protected_development_localisation'].items():
            self.assertEqual(actual[key], before)

    def test_global_thresholds_are_ready_before_native_country_initialization(self):
        index = next(i for i, row in enumerate(GLOBALS) if row == (build.EFFECT, '=', 'yes'))
        defaults = [i for i, row in enumerate(GLOBALS) if row in DEFAULTS]
        self.assertGreater(index, max(defaults))
        actions = (ROOT / 'common/on_actions/00_on_actions.txt').read_text(encoding='utf-8')
        start = actions[actions.index('\ton_startup = {'):]
        self.assertLess(start.index('setup_global_arrays = yes'),
                        start.index('research_slot_init_for_country = yes'))

    def test_canonical_outputs_and_encoding(self):
        for relative, expected in build.render().items():
            raw = (ROOT / relative).read_bytes()
            self.assertEqual(raw, expected.encode('utf-8-sig' if relative.endswith('.yml') else 'utf-8'))
            self.assertEqual(raw.startswith(b'\xef\xbb\xbf'), relative.endswith('.yml'))
            self.assertIn('IMPERIA CW', raw.decode('utf-8-sig'))
            if not relative.endswith('.yml'):
                V.parse(raw.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
