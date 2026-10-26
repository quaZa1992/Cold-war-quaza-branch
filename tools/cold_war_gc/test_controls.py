# IMPERIA CW — Cold War: execute GC controls, shared formulas and crisis-stage effects.
"""Strict script-harness checks; native HOI4 rendering and MP are not simulated."""
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
spec = importlib.util.spec_from_file_location('cw_gc_build', HERE / 'build.py')
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)
P = B.P


def read(relative):
    return V.parse((ROOT / relative).read_text(encoding='utf-8-sig'))


EFFECTS = {key: value for relative in (B.WORLD,
           'common/scripted_effects/COLDWAR_gc_equilibrium_effects.txt',
           'common/scripted_effects/IMP_cold_war_military_industrial_complex_effects.txt',
           'common/scripted_effects/imp_oil_prices_scripted_effects.txt')
           for key, _, value in read(relative)}
TRIGGERS = {key: value for key, _, value in read('common/scripted_triggers/mdcw_cold_war_triggers.txt')}
DECISIONS = dict((key, value) for key, _, value in V.first(
    read('common/decisions/COLDWAR_gc_equilibrium_decisions.txt'), 'imp_gc_tools_decisions'))


class Machine(V.ScriptMachine):
    def __init__(self):
        super().__init__(EFFECTS, TRIGGERS)
        self.global_scope = V.Country('GLOBAL')
        self.country_scans = 0
        self.global_scope.flags['mdcw_cw_initialized'] = V.D(0)
        self.global_scope.variables.update(mdcw_cw_tension=V.D(45), mdcw_cw_tension_baseline=V.D(40),
            mdcw_cw_oil_level=V.D(1), imp_global_oil_price=V.D(75), imp_global_oil_price_equilibrium=V.D(75),
            imp_oil_price_base_unit=V.D('.024'), mdcw_cw_cpi=V.D(1), tot_dep=V.D(1))
        for country in self.countries.values():
            country.flags['mdcw_cw_initialized'] = V.D(0)
            country.variables.update(globalism_value=V.D(50), imp_oil_dependency=V.D(1))
            country.ideas.clear()
            country.enemies = []
        self.root.ideas.add('imp_gc_nation')

    def scope(self, name):
        if name.lower() == 'global':
            return self.global_scope
        return super().scope(name)

    def get(self, name):
        if name == 'modifier@mdcw_cw_market_exposure':
            return self.current.variables.get('test_market_exposure_bonus', V.D(0))
        return super().get(name)

    def test(self, body):
        for key, op, value in body:
            if key == 'has_global_flag':
                answer = value in self.global_scope.flags
            elif key == 'has_variable':
                target, name = self.resolve_variable(value)
                answer = name in target.variables or name in target.temporary
            elif key == 'any_enemy_country':
                answer = any(self.in_scope(self.countries[tag], lambda: self.test(value))
                             for tag in self.current.enemies)
            else:
                answer = super().test([(key, op, value)])
            if not answer:
                return False
        return True

    def execute(self, body):
        pending = []
        for key, op, value in body:
            if key != 'every_country':
                pending.append((key, op, value))
                continue
            if pending:
                super().execute(pending)
                pending = []
            self.country_scans += 1
            for country in self.countries.values():
                def visit():
                    if self.test(V.first(value, 'limit', [])):
                        self.execute([node for node in value if node[0] != 'limit'])
                self.in_scope(country, visit)
        if pending:
            super().execute(pending)

    def refresh(self):
        self.call(P + 'refresh')

    def decision(self, name):
        body = DECISIONS[P + name]
        assert self.test(V.first(body, 'visible'))
        assert self.test(V.first(body, 'available'))
        self.execute(V.first(body, 'complete_effect'))


class GCEquilibriumTests(unittest.TestCase):
    def ready(self):
        m = Machine()
        m.refresh()
        m.decision('expand')
        return m

    def test_decisions_are_gc_only_and_collapsible(self):
        self.assertEqual(len(DECISIONS), 22)
        m = Machine()
        self.assertTrue(m.test(V.first(DECISIONS[P + 'expand'], 'visible')))
        m.decision('expand')
        self.assertFalse(m.test(V.first(DECISIONS[P + 'expand'], 'visible')))
        self.assertTrue(m.test(V.first(DECISIONS[P + 'market_raise_5'], 'visible')))
        m.decision('collapse')
        self.assertFalse(m.test(V.first(DECISIONS[P + 'market_raise_5'], 'visible')))
        for ai, gc in ((True, True), (False, False), (True, False)):
            m.root.is_ai = ai
            m.root.ideas = {'imp_gc_nation'} if gc else set()
            for body in DECISIONS.values():
                self.assertFalse(m.test(V.first(body, 'visible')))
                self.assertFalse(m.test(V.first(body, 'available')))
            before = deepcopy(m.global_scope.variables)
            m.root.temporary['COLDWAR_gc_cw_delta'] = V.D(20)
            for track in ('tension', 'market', 'arms', 'oil'):
                m.call(P + 'change_' + track)
                m.call(P + 'reset_' + track)
            self.assertEqual(m.global_scope.variables, before)

    def test_tension_adjustments_and_baseline_reset_refresh_every_country(self):
        m = self.ready()
        m.decision('tension_raise_20')
        self.assertEqual(m.get('global.mdcw_cw_tension'), 65)
        self.assertEqual(m.root.variables['mdcw_cw_wm_trade'], V.D('-.12'))
        self.assertEqual(m.origin.variables['mdcw_cw_wm_trade'], V.D('-.12'))
        m.decision('tension_lower_5')
        self.assertEqual(m.get('global.mdcw_cw_tension'), 60)
        m.decision('tension_reset')
        self.assertEqual(m.get('global.mdcw_cw_tension'), 40)
        self.assertTrue(all(c.dynamic_refreshes > 0 for c in m.countries.values()))

    def test_market_and_arms_assessments_survive_normal_recalculation(self):
        for track in ('market', 'arms'):
            with self.subTest(track=track):
                m = self.ready()
                before = m.get('global.mdcw_cw_' + track)
                m.decision(track + '_raise_5')
                expected = min(before + 5, 100)
                self.assertEqual(m.get('global.mdcw_cw_' + track), expected)
                for _ in range(4):
                    m.call('mdcw_cw_update_world_situation')
                    self.assertEqual(m.get('global.mdcw_cw_' + track), expected)
                m.decision(track + '_reset')
                self.assertEqual(m.get('global.mdcw_cw_' + track), before)

    def test_repeated_steps_clamp_without_hidden_excess(self):
        for track, floor in (('market', 5), ('arms', 0)):
            with self.subTest(track=track):
                m = self.ready()
                while m.test(V.first(DECISIONS[P + track + '_raise_20'], 'available')):
                    m.decision(track + '_raise_20')
                self.assertEqual(m.get('global.mdcw_cw_' + track), 100)
                m.decision(track + '_lower_5')
                self.assertEqual(m.get('global.mdcw_cw_' + track), 95)
                while m.test(V.first(DECISIONS[P + track + '_lower_20'], 'available')):
                    m.decision(track + '_lower_20')
                self.assertEqual(m.get('global.mdcw_cw_' + track), floor)
                m.decision(track + '_raise_5')
                self.assertEqual(m.get('global.mdcw_cw_' + track), floor + 5)

    def test_old_save_without_gc_caches_can_be_adjusted_downwards(self):
        m = self.ready()
        m.global_scope.variables.pop(P + 'market_base')
        before = m.get('global.mdcw_cw_market')
        m.decision('market_lower_5')
        self.assertEqual(m.get('global.mdcw_cw_market'), before - 5)

    def test_oil_buttons_apply_real_prices_and_reset_crisis_burdens(self):
        m = self.ready()
        for _ in range(5):
            m.decision('oil_raise_1')
        self.assertEqual(m.get('global.mdcw_cw_oil_level'), 6)
        self.assertEqual(m.root.variables['mdcw_cw_oil_crisis_tier'], 4)
        self.assertEqual(m.root.variables['mdcw_cw_oil_crisis_output'], V.D('-.2'))
        self.assertEqual(m.get('global.imp_oil_price_real_display'), V.D('10.8'))
        first = {k: v for k, v in m.root.variables.items() if k.startswith(('imp_oil_', 'mdcw_cw_oil_crisis_'))}
        m.refresh()
        self.assertEqual({k: v for k, v in m.root.variables.items() if k in first}, first)
        m.decision('oil_reset')
        self.assertEqual(m.get('global.mdcw_cw_oil_level'), 1)
        self.assertEqual(m.root.variables['mdcw_cw_oil_crisis_output'], 0)
        self.assertEqual(m.root.variables['mdcw_cw_oil_crisis_tier'], 0)

    def test_every_market_stage_uses_stronger_costs(self):
        # Office, ROI, productivity, civilian income, stability, interest, consumer goods.
        expected = {80: ('.08', '.005', '.02', '.03', '0', '.75', '.05'),
                    60: ('.03', '.002', '0', '0', '0', '.2', '0'),
                    40: ('-.06', '-.005', '-.02', '0', '0', '-.1', '0'),
                    20: ('-.18', '-.015', '-.06', '-.06', '-.04', '0', '0'),
                     5: ('-.3', '-.03', '-.12', '-.12', '-.08', '2', '0')}
        keys = ('office', 'roi', 'prod_growth', 'civ_tax', 'stab', 'interest', 'consumer')
        for score, values in expected.items():
            m = Machine()
            m.global_scope.variables.update(mdcw_cw_tension=V.D(20), mdcw_cw_arms=V.D(30), mdcw_cw_market=V.D(score))
            m.call('mdcw_cw_update_world_market')
            self.assertEqual(tuple(m.get('mdcw_cw_wm_' + k) for k in keys), tuple(map(V.D, values)))

    def test_every_tension_stage_and_arms_stage(self):
        for score, values in {80: ('-.08', '-.25', '.08', '.06'), 60: ('-.03', '-.12', '.03', '.03'),
                              40: ('-.01', '-.04', '.01', '0'), 20: ('0', '.05', '0', '-.04'),
                               0: ('.01', '.1', '0', '-.08')}.items():
            m = Machine()
            m.global_scope.variables.update(mdcw_cw_tension=V.D(score), mdcw_cw_arms=V.D(30), mdcw_cw_market=V.D(60))
            m.call('mdcw_cw_update_world_market')
            self.assertEqual(tuple(m.get('mdcw_cw_wm_' + k) for k in ('stab', 'trade', 'consumer', 'war_sup')),
                             tuple(map(V.D, values)))
        for score, upkeep, sales, income in ((80, '.2', '.12', '.12'), (60, '.12', '.08', '.08'),
                                             (30, '.06', '.04', '.04'), (0, '-.02', '-.1', '-.06')):
            m = Machine()
            m.global_scope.variables.update(mdcw_cw_tension=V.D(40), mdcw_cw_arms=V.D(score), mdcw_cw_market=V.D(60))
            m.call('mdcw_cw_update_world_market')
            self.assertEqual(tuple(m.get('mdcw_cw_wm_' + k) for k in ('equip', 'arms_sales', 'mil_income')),
                             tuple(map(V.D, (upkeep, sales, income))))

    def test_exposure_scales_stronger_market_penalties_and_caps(self):
        for globalism, bonus, exposure in ((0, 0, '.25'), (25, 0, '.625'), (50, 0, '1'),
                                           (75, 0, '1.5'), (100, 0, '2'), (100, 1, '2.5')):
            m = Machine()
            m.root.variables.update(globalism_value=V.D(globalism), test_market_exposure_bonus=V.D(bonus))
            m.global_scope.variables.update(mdcw_cw_tension=V.D(20), mdcw_cw_arms=V.D(30), mdcw_cw_market=V.D(5))
            m.call('mdcw_cw_update_world_market')
            self.assertEqual(m.get('mdcw_cw_wm_exposure'), V.D(exposure))
            self.assertEqual(m.get('mdcw_cw_wm_office'), V.D('-.3') * V.D(exposure))
            self.assertEqual(m.get('mdcw_cw_wm_interest'), V.D(2) * V.D(exposure))

    def test_oil_stages_and_dependency_are_graded_and_reset(self):
        expected = {1: ('0', '0', '0', '0'), 1.5: ('.04', '-.02', '-.02', '-.005'),
                    2.5: ('.08', '-.06', '-.06', '-.015'), 4: ('.14', '-.12', '-.12', '-.04'),
                    6: ('.2', '-.2', '-.2', '-.08')}
        for dependency in ('.2', '.5', '1'):
            for ratio, values in expected.items():
                m = Machine()
                m.root.variables.update(mdcw_cw_oil_crisis_ratio=V.D(str(ratio)), imp_oil_dependency=V.D(dependency))
                m.call('mdcw_cw_update_oil_crisis_tier')
                self.assertEqual(tuple(m.get('mdcw_cw_oil_crisis_' + k) for k in ('consumer', 'tax', 'output', 'stability')),
                                 tuple(V.D(x) * V.D(dependency) for x in values))

    def test_manual_refresh_does_not_advance_monthly_or_weekly_simulation(self):
        m = self.ready()
        m.country_scans = 0
        m.decision('market_raise_5')
        self.assertEqual(m.country_scans, 3)  # Two existing war counts and one modifier pass.
        called = {k for k, _, v in V.walk(EFFECTS[P + 'refresh'])}
        self.assertFalse(called & {'mdcw_cw_global_monthly', 'mdcw_cw_update_oil_level',
                                   'imp_weekly_oil_price_change', 'mdcw_cw_rebuild_blocs'})
        hook = V.first(read('common/on_actions/COLDWAR_gc_equilibrium_on_actions.txt'), 'on_actions')
        self.assertEqual([key for key, _, value in hook], ['on_startup'])
        self.assertIn((P + 'refresh', '=', 'yes'), list(V.walk(hook)))

    def test_arms_controls_refresh_mic_income_without_changing_ai_war_rules(self):
        m = self.ready()
        m.root.ideas.add('defense_industry')
        m.origin.ideas.add('defense_industry')
        m.origin.is_ai = True
        m.refresh()
        before = m.root.variables['IMP_military_industrial_complex_tax_bonus']
        m.decision('arms_raise_5')
        for country in m.countries.values():
            self.assertEqual(country.variables['IMP_military_industrial_complex_tax_bonus'], before + V.D('.02'))
            self.assertNotIn('IMP_cold_war_ai_war_declaration_lock', country.ideas)

    def test_localisation_and_canonical_outputs_are_complete(self):
        for relative, text in B.render().items():
            raw = (ROOT / relative).read_bytes()
            self.assertEqual(raw, text.encode('utf-8-sig' if relative.endswith('.yml') else 'utf-8'))
            self.assertEqual(raw.startswith(b'\xef\xbb\xbf'), relative.endswith('.yml'))
            if not relative.endswith('.yml'):
                V.parse(text)
        loc = (ROOT / 'localisation/english/COLDWAR_gc_equilibrium_l_english.yml').read_text(encoding='utf-8-sig')
        keys = re.findall(r'^ ([\w.]+):', loc, re.M)
        self.assertEqual(len(keys), len(set(keys)))
        for name in DECISIONS:
            self.assertIn(name, keys)
            self.assertIn(name + '_desc', keys)
            if not name.endswith(('expand', 'collapse')):
                self.assertIn(name + '_tt', keys)


if __name__ == '__main__':
    unittest.main()
