# IMPERIA COLD WAR — USA tax calibration source and save regression checks.
"""Exercise emitted guards and native-formula forecasts without launching HOI4."""
from __future__ import annotations

from decimal import Decimal as D
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import economy
from focus_prerequisite_ui import nodes

ROOT = economy.ROOT


class World:
    def __init__(self, rate=48, tag='USA', scenario=True, initialized=True):
        text = (ROOT / economy.EFFECT_PATH).read_text(encoding='utf-8')
        self.effects = {n.key: n.children() for n in nodes(text)}
        self.vars = dict(corporate_tax_rate=D(str(rate)))
        self.flags = {'USA_1970_systems_initialized'} if initialized else set()
        self.tag, self.scenario, self.refreshes = tag, scenario, []

    def valid(self, body):
        for node in body:
            if node.key == 'NOT':
                result = not self.valid(node.children())
            elif node.key == 'tag':
                result = self.tag == node.value
            elif node.key == 'IMP_is_1970_scenario':
                result = self.scenario
            elif node.key == 'has_country_flag':
                result = node.value in self.flags
            elif node.key == 'check_variable':
                check, = node.children()
                self.assert_native_comparison(check)
                result = self.vars.get(check.key, D(0)) == D(check.value)
            else:
                raise AssertionError(('unmodeled trigger', node.key))
            if not result:
                return False
        return True

    @staticmethod
    def assert_native_comparison(node):
        assert node.op == '=', (node.key, node.op)

    def run(self, name):
        self.execute(self.effects[name])

    def execute(self, body):
        previous_if = False
        for node in body:
            if node.key in ('if', 'else_if'):
                limit = next(n for n in node.children() if n.key == 'limit')
                take = self.valid(limit.children()) and (node.key == 'if' or not previous_if)
                if take:
                    self.execute([n for n in node.children() if n.key != 'limit'])
                previous_if = take or (previous_if if node.key == 'else_if' else False)
            elif node.key == 'set_country_flag':
                self.flags.add(node.value)
            elif node.key in ('set_variable', 'set_temp_variable'):
                var, = node.children()
                self.vars[var.key] = D(var.value)
            elif node.key in ('calculate_tax_rate', 'force_update_dynamic_modifier', 'ingame_update_setup'):
                self.refreshes.append(node.key)
            else:
                raise AssertionError(('unmodeled effect', node.key))


class EconomyTests(unittest.TestCase):
    def test_legacy_default_48_is_calibrated(self):
        w = World(48)
        w.run('COLDWAR_USA_1970_economy_migrate')
        self.assertEqual(w.vars['corporate_tax_rate'], 20)
        self.assertEqual(w.refreshes, ['calculate_tax_rate', 'force_update_dynamic_modifier', 'ingame_update_setup'])

    def test_observed_save_42_preserves_relative_reduction(self):
        w = World(42)
        w.run('COLDWAR_USA_1970_economy_migrate')
        self.assertEqual(w.vars['corporate_tax_rate'], D('17.5'))
        self.assertEqual(D(42) / 48, w.vars['corporate_tax_rate'] / 20)

    def test_existing_manual_20_and_25_are_preserved(self):
        for rate in (0, 15, 20, 25, D('42.5'), 47, 50):
            with self.subTest(rate=rate):
                w = World(rate)
                w.run('COLDWAR_USA_1970_economy_migrate')
                self.assertEqual(w.vars['corporate_tax_rate'], rate)
                self.assertFalse(w.refreshes)
                self.assertIn(economy.FLAG, w.flags)

    def test_migration_never_reapplies_after_player_adjustment(self):
        w = World(42)
        w.run('COLDWAR_USA_1970_economy_migrate')
        w.vars['corporate_tax_rate'] = D(48)
        w.run('COLDWAR_USA_1970_economy_migrate')
        self.assertEqual(w.vars['corporate_tax_rate'], 48)
        self.assertEqual(len(w.refreshes), 3)

    def test_country_scenario_and_initialization_guards(self):
        for kwargs in (dict(tag='D01'), dict(tag='CAN'), dict(scenario=False), dict(initialized=False)):
            for name in ('initialize', 'migrate'):
                with self.subTest(kwargs=kwargs, hook=name):
                    w = World(48, **kwargs)
                    w.run('COLDWAR_USA_1970_economy_' + name)
                    self.assertEqual(w.vars['corporate_tax_rate'], 48)
                    self.assertNotIn(economy.FLAG, w.flags)

    def test_new_start_and_reload_do_not_reset_policy(self):
        w = World(48)
        w.run('COLDWAR_USA_1970_economy_initialize')
        self.assertEqual(w.vars['corporate_tax_rate'], 20)
        self.assertFalse(w.refreshes, 'Fresh-start fiscal pass remains owned by native startup')
        w.vars['corporate_tax_rate'] = D(25)
        w.run('COLDWAR_USA_1970_economy_initialize')
        w.run('COLDWAR_USA_1970_economy_migrate')
        self.assertEqual(w.vars['corporate_tax_rate'], 25)

    def test_screenshot_and_initial_defaults_have_zero_construction(self):
        for rate in (42, 48):
            self.assertEqual(economy.consumer_goods(rate, '1.62')['usable_lower_bound'], 0)
        self.assertEqual(economy.consumer_goods(42, '1.62')['share'], D('1.0206'))

    def test_new_start_with_full_pressure_has_construction(self):
        r = economy.consumer_goods(20, '1.62')
        self.assertEqual(r['required'], D('78.73200'))
        self.assertGreaterEqual(r['usable_lower_bound'], 21)

    def test_observed_save_migration_has_construction(self):
        r = economy.consumer_goods('17.5', '1.62')
        self.assertEqual(r['required'], D('68.890500'))
        self.assertGreaterEqual(r['usable_lower_bound'], 31)

    def test_all_positive_authored_domestic_cg_deltas_still_leave_capacity(self):
        # Conservative superset: E1, E11, legal aid and Democratic public works.
        # Cumulative idea tiers are replacements, not additional duplicate copies.
        base = economy.compound_factors(['.99', '1.05', '1.04', '1.10', '1.355', '1.01'])
        continuation = economy.compound_factors(['1.01', '1.01', '1.005', '1.01'])
        r = economy.consumer_goods(20, base * continuation)
        self.assertGreaterEqual(r['usable_lower_bound'], 18)
        self.assertLess(r['required'], 82)

    def test_native_factors_compound_instead_of_adding_percentages(self):
        base = economy.compound_factors(['.99', '1.05', '1.04', '1.10', '1.355', '1.01'])
        self.assertEqual(base, D('1.6274632374'))
        self.assertNotEqual(base, D('1.545'))
        self.assertGreaterEqual(economy.consumer_goods(20, base)['usable_lower_bound'], 20)

    def test_tax_formula_matches_installed_provider(self):
        text = (ROOT / 'common/scripted_effects/00_money_system.txt').read_text(encoding='utf-8-sig')
        body = next(n for n in nodes(text) if n.key == 'calculate_tax_rate')
        raw = text[body.start:body.end]
        self.assertRegex(raw, r'consumer_goods_from_corporate_tax\s*=\s*\{\s*value\s*=\s*corporate_tax_rate\s*multiply\s*=\s*0\.015')
        for name in ('calculate_tax_rate', 'ingame_update_setup'):
            self.assertIn(name, {n.key for n in nodes(text)})

    def test_fiscal_cost_is_not_hidden_by_income_compensation(self):
        old_income, old_corp, expenses = D('69.25320'), D('49.76320'), D('54.85895')
        projected = old_income - old_corp + old_corp * 20 / 48
        self.assertLess(projected - expenses, 0)
        self.assertAlmostEqual(projected - expenses, D('-14.63428333333333333333333333'))
        text, _ = economy.build()
        for forbidden in ('modify_treasury_effect =', 'modify_debt_effect =', 'add_to_array =', 'consumer_goods_factor =', 'tax_gain_multiplier_modifier ='):
            self.assertNotIn(forbidden, text)

    def test_native_weekly_deficit_and_automatic_borrowing_are_retained(self):
        weekly = (ROOT / 'common/on_actions/MD_on_actions.txt').read_text(encoding='utf-8-sig')
        self.assertIn('add_to_variable = { treasury = treasury_rate_gain }', weekly)
        self.assertIn('automated_debt_taker = yes', weekly)
        utilities = (ROOT / 'common/scripted_effects/00_economic_system_utilities.txt').read_text(encoding='utf-8-sig')
        effect = next(n for n in nodes(utilities) if n.key == 'automated_debt_taker')
        raw = utilities[effect.start:effect.end]
        for native_row in ('check_variable = { treasury < 0 }',
                           'multiply_temp_variable = { treasury_temp = -1.25 }',
                           'multiply_temp_variable = { gdp_adder = 0.01 }',
                           'multiply_temp_variable = { debt_temp = 1.01 }',
                           'add_to_variable = { treasury = treasury_temp }',
                           'add_to_variable = { debt = debt_temp }'):
            self.assertIn(native_row, raw)
        # The existing provider finances a deficit with principal plus a fee.
        treasury, debt, gdp = D(-10), D(371), D('3941.76292')
        advance = treasury * D('-1.25') + gdp * D('.01')
        self.assertGreater(treasury + advance, 0)
        self.assertGreater(debt + advance * D('1.01'), debt)

    def test_output_is_exact_utf8_no_bom_and_idempotent(self):
        expected, _ = economy.build()
        self.assertEqual((ROOT / economy.EFFECT_PATH).read_bytes(), expected.encode('utf-8'))
        self.assertFalse((ROOT / economy.EFFECT_PATH).read_bytes().startswith(b'\xef\xbb\xbf'))
        self.assertEqual(economy.generate()['changed'], [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
