# IMPERIA CW — Cold War: execute cartel startup and defeat eligibility against native history.
"""Regression checks use real emitted scripts; they do not replace an engine test."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/guest_workers'))
import validate as V


def read(relative):
    return V.parse((ROOT / relative).read_text(encoding='utf-8-sig'))


TRIGGERS = {k: v for k, _, v in read('common/scripted_triggers/01_cartels_scripted_triggers.txt')}
EFFECTS = {k: v for rel in ('common/scripted_effects/01_cartels_terror_scripted_effects.txt',
                          'common/scripted_effects/IMPERIA_CW_1970_cartel_effects.txt')
           for k, _, v in read(rel)}
TAGS = [v for k, _, v in V.walk(TRIGGERS['set_cartel_nation']) if k == 'original_tag' and v != 'HOL']
STARTUP = [('if', '=', next(v for k, _, v in V.walk(read('common/on_actions/00_on_actions.txt'))
                           if k == 'if' and ('IMP_1970_initialize_cartel_variables', '=', 'yes') in v))]
DEFEAT = next(v for k, _, v in read('events/cartel_events.txt')
              if k == 'country_event' and V.first(v, 'id') == 'cartel_event.52')
STOCKS = ('strength_of_cartels', 'cartel_political_influence')


class Machine(V.ScriptMachine):
    is_1970 = True

    def execute(self, body):
        # Record engine UI cleanup/broadcasts; all variable arithmetic stays in the emitted AST.
        if not any(k in {'remove_decision', 'news_event'} for k, _, v in body):
            return super().execute(body)
        assert not any(k in {'if', 'else_if', 'else'} for k, _, v in body)
        for key, op, value in body:
            if key == 'remove_decision':
                self.removed_decisions.append(value)
            elif key == 'news_event':
                self.queue.append(('news', V.first(value, 'id')))
            else:
                super().execute([(key, op, value)])

    def test(self, body):
        answers = []
        for key, op, value in body:
            if key == 'original_tag':
                answer = self.current.tag == value
            elif key == 'IMP_is_1970_scenario':
                answer = self.is_1970 == (value == 'yes')
            else:
                answer = super().test([(key, op, value)])
            answers.append(answer)
        return all(answers)


def fixture(tag='MEX', modern=False):
    m = Machine(EFFECTS, TRIGGERS)
    c = V.Country(tag)
    m.countries = {tag: c}
    m.current = m.root = m.origin = m.previous = c
    m.removed_decisions = []
    m.is_1970 = not modern
    return m


def history_profile(tag, date):
    path = next((ROOT / 'history/countries').glob(tag + ' - *.txt'))
    history = V.first(V.parse(path.read_text(encoding='utf-8-sig')), date, [])
    result = {}
    for key, _, body in V.walk(history):
        if key == 'set_variable' and isinstance(body, list):
            for name, _, value in body:
                if name in STOCKS:
                    result[name] = V.D(value)
    return result


class CartelStartupTests(unittest.TestCase):
    def test_all_enabled_countries_start_with_native_profiles_and_cannot_claim_victory(self):
        self.assertEqual(len(set(TAGS)), 28)
        for tag in TAGS:
            with self.subTest(tag=tag):
                m = fixture(tag)
                m.root.variables.update(history_profile(tag, '1970.1.1'))
                m.execute(STARTUP)
                self.assertEqual({k: m.root.variables[k] for k in STOCKS}, history_profile(tag, '2000.1.1'))
                self.assertIn('is_cartel_nation', m.root.flags)
                self.assertIn('cartel_penalties', m.root.dynamic_modifiers)
                self.assertLess(m.root.variables['CAR_stability_factor'], 0)
                self.assertFalse(m.test(V.first(DEFEAT, 'trigger')))

    def test_native_startup_defect_is_reproduced_before_initialisation(self):
        m = fixture()
        self.assertEqual(history_profile('MEX', '1970.1.1'), {})
        self.assertTrue(m.test(V.parse('check_variable = { strength_of_cartels < 5 } check_variable = { cartel_political_influence < 5 }')))

    def test_existing_stocks_including_zero_are_not_reset(self):
        for strength, influence in ((0, 0), (3, 0), (70, 88)):
            with self.subTest(strength=strength, influence=influence):
                m = fixture()
                m.root.variables.update(dict(zip(STOCKS, map(V.D, (strength, influence)))))
                before = deepcopy(m.root.variables)
                m.call('IMP_1970_initialize_cartel_variables')
                m.call('IMP_1970_initialize_cartel_variables')
                self.assertEqual(m.root.variables, before)

    def test_partial_history_only_seeds_the_missing_stock(self):
        for present in STOCKS:
            with self.subTest(present=present):
                m = fixture('BRM')
                m.root.variables[present] = V.D(0)
                m.call('IMP_1970_initialize_cartel_variables')
                self.assertEqual(m.root.variables[present], 0)
                missing = next(k for k in STOCKS if k != present)
                self.assertEqual(m.root.variables[missing], history_profile('BRM', '2000.1.1')[missing])

    def test_modern_history_remains_authoritative(self):
        m = fixture('MEX', modern=True)
        m.root.variables.update(history_profile('MEX', '2000.1.1'))
        before = deepcopy(m.root.variables)
        m.execute(STARTUP)
        for k, value in before.items():
            self.assertEqual(m.root.variables[k], value)

    def test_modern_missing_data_is_not_seeded_by_cold_war_fallback(self):
        m = fixture(modern=True)
        m.call('IMP_1970_initialize_cartel_variables')
        self.assertFalse(any(k in m.root.variables for k in STOCKS))

    def test_holland_and_non_cartel_tags_are_not_activated(self):
        for tag in ('HOL', 'USA'):
            with self.subTest(tag=tag):
                m = fixture(tag)
                m.execute(STARTUP)
                self.assertNotIn('is_cartel_nation', m.root.flags)
                self.assertFalse(any(k in m.root.variables for k in STOCKS))

    def test_already_defeated_country_is_not_reseeded(self):
        m = fixture()
        m.root.flags['CARTEL_defeated_the_cartels'] = True
        m.call('IMP_1970_initialize_cartel_variables')
        self.assertFalse(any(k in m.root.variables for k in STOCKS))

    def test_defeat_requires_both_initialized_stocks(self):
        for seeded in ({}, {STOCKS[0]: V.D(0)}, {STOCKS[1]: V.D(0)}):
            with self.subTest(seeded=seeded):
                m = fixture()
                m.root.variables.update(seeded)
                m.root.flags['is_cartel_nation'] = True
                m.root.dynamic_modifiers.add('cartel_penalties')
                self.assertFalse(m.test(V.first(DEFEAT, 'trigger')))

    def test_actual_defeat_after_campaign_remains_possible(self):
        m = fixture()
        m.execute(STARTUP)
        m.root.variables.update({k: V.D(0) for k in STOCKS})
        self.assertTrue(m.test(V.first(DEFEAT, 'trigger')))
        m.execute([node for node in V.first(DEFEAT, 'option') if node[0] != 'name'])
        self.assertIn('CARTEL_defeated_the_cartels', m.root.flags)
        self.assertNotIn('cartel_penalties', m.root.dynamic_modifiers)
        self.assertFalse(any(k in m.root.variables for k in STOCKS))

    def test_scripts_have_no_bom_and_parse(self):
        for rel in ('common/scripted_effects/IMPERIA_CW_1970_cartel_effects.txt',
                    'common/on_actions/00_on_actions.txt', 'events/cartel_events.txt'):
            with self.subTest(path=rel):
                self.assertFalse((ROOT / rel).read_bytes().startswith(b'\xef\xbb\xbf'))
                read(rel)


if __name__ == '__main__':
    unittest.main()
