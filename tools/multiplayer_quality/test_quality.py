# IMPERIA COLD WAR — Native compatibility and multiplayer scheduler regressions.
"""Execute emitted ASTs at repaired boundaries; no network/OOS claim."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tools/space_race_1970'))
import validate as V
from multiplayer_quality.repair_native_syntax import repair
from multiplayer_quality.native_compat import normalize, blocks
from multiplayer_quality.audit import parse


def source(relative):
    return (ROOT / relative).read_text(encoding='utf-8-sig')


class Quality(unittest.TestCase):
    def test_native_stat_triggers_preserve_dynamic_variable_operands(self):
        original = '# stability < 0.5\nif = { limit = { political_power > 25 stability < 0.5 check_variable = { stability < 0.2 } } add_political_power = -25 }'
        fixed = repair(original)
        self.assertIn('has_political_power > 25', fixed)
        self.assertIn('has_stability < 0.5', fixed)
        self.assertIn('check_variable = { stability < 0.2 }', fixed)
        self.assertTrue(fixed.startswith('# stability < 0.5'))
        self.assertEqual(repair(fixed), fixed)

    def test_inclusive_comparisons_use_documented_native_form(self):
        for operator, name in [('>=', 'greater_than_or_equals'), ('<=', 'less_than_or_equals'), ('!=', 'not_equals')]:
            fixed = repair('check_variable = { preparedness ' + operator + ' 80 }')
            rows = V.first(parse(fixed), 'check_variable')
            self.assertEqual(V.first(rows, 'compare'), name)
            self.assertEqual(V.first(rows, 'var'), 'preparedness')
            self.assertEqual(V.first(rows, 'value'), '80')

    def test_repaired_historical_setters_are_complete_native_blocks(self):
        report = json.loads(source('docs/audits/multiplayer_quality_20261023/leader_delimiter_repairs.json'))
        self.assertEqual(report['repaired_count'], 129)
        for relative in report['files']:
            with self.subTest(file=relative):
                text = source(relative)
                parse(text)
                self.assertNotRegex(text, r'(?m)^# MDCW HISTORICAL NATIVE POOL END [A-Z0-9]{3}\}')

    def test_historical_generator_keeps_original_outer_brace_on_a_new_line(self):
        spec = importlib.util.spec_from_file_location('icw_historical_dispatch', ROOT / 'tools/historical_politics_1970/dispatch.py')
        dispatch = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dispatch)
        fixtures = ROOT / 'tools/multiplayer_quality/.fixtures'
        fixtures.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=fixtures) as directory:
            root = Path(directory)
            self.assertTrue(root.resolve().is_relative_to(fixtures.resolve()))
            target = root / 'common/scripted_effects/TST_political_leaders.txt'
            target.parent.mkdir(parents=True)
            target.write_text('# IMPERIA COLD WAR — Historical wrapper fixture.\nset_leader_TST = {\nadd_political_power = 5\n}\n', encoding='utf-8')
            first = dispatch._wrap_native_setter(root, 'TST', {1: []})
            parse(first)
            self.assertIn('# MDCW HISTORICAL NATIVE POOL END TST\n}', first)
            target.write_text(first, encoding='utf-8')
            self.assertEqual(dispatch._wrap_native_setter(root, 'TST', {1: []}), first)

    def test_live_decision_requirements_survive_static_allowed_repair(self):
        original = 'category = { decision = { allowed = { original_tag = GRE exists = yes IMP_is_1970_scenario = yes } visible = { has_country_flag = pending } complete_effect = { add_political_power = 5 } } }'
        fixed = normalize(original, 'common/decisions/fixture.txt')
        decision = V.first(V.first(parse(fixed), 'category'), 'decision')
        self.assertEqual(V.first(decision, 'allowed'), [('original_tag', '=', 'GRE')])
        visible = V.first(decision, 'visible')
        self.assertIn(('exists', '=', 'yes'), visible)
        self.assertIn(('IMP_is_1970_scenario', '=', 'yes'), visible)
        self.assertIn(('has_country_flag', '=', 'pending'), visible)
        self.assertEqual(normalize(fixed, 'common/decisions/fixture.txt'), fixed)

    def test_scalar_modifier_removal_is_a_native_block(self):
        fixed = normalize('cleanup = { 213 = { remove_dynamic_modifier = local_programme } }', 'common/scripted_effects/fixture.txt')
        body = V.first(V.first(parse(fixed), 'cleanup'), '213')
        self.assertEqual(V.first(body, 'remove_dynamic_modifier'), [('modifier', '=', 'local_programme')])

    def test_scheduled_world_ranking_is_once_per_day_across_country_order_and_reload(self):
        for order in [('SOV', 'USA', 'DDR'), ('DDR', 'USA', 'SOV')]:
            m = V.Machine(order)
            calls = []
            original = m.call
            def counted(key):
                if key == 'cw_sr_rank':
                    calls.append(key)
                original(key)
            m.call = counted
            m.g['num_days'] = V.D(500)
            for _ in range(4):
                for tag in order:
                    m.c = m.countries[tag]
                    m.call('cw_sr_calendar_tick')
            self.assertEqual(len(calls), 1)
            m.g, m.gf = deepcopy((m.g, m.gf))
            m.call('cw_sr_calendar_tick')
            self.assertEqual(len(calls), 1)
            m.g['num_days'] += 1
            m.call('cw_sr_calendar_tick')
            self.assertEqual(len(calls), 2)
            m.gf.add('cw_sr_emergency_disabled')
            m.g['num_days'] += 1
            m.call('cw_sr_calendar_tick')
            self.assertEqual(len(calls), 2)

    def test_existing_ddr_rewards_migrate_once_and_add_to_new_rewards(self):
        effect = V.first(parse(source('common/scripted_effects/ICW_native_compatibility.txt')), 'ICW_migrate_ddr_ideological_defence')
        spec = importlib.util.spec_from_file_location('icw_native_contract_machine', ROOT / 'tools/guest_workers/validate.py')
        machine = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = machine
        spec.loader.exec_module(machine)
        m = machine.ScriptMachine({'migrate': effect}, {})
        m.root.variables['COLDWAR_DDR_party_state_mdcw_cw_ideological_defence'] = V.D('.03')
        m.root.variables['COLDWAR_DDR_party_state_drift_defence_factor'] = V.D('.05')
        m.call('migrate')
        m.call('migrate')
        self.assertEqual(m.root.variables['COLDWAR_DDR_party_state_drift_defence_factor'], V.D('.08'))
        self.assertNotIn('COLDWAR_DDR_party_state_mdcw_cw_ideological_defence', m.root.variables)

    def test_zero_energy_oil_dependency_does_not_divide_by_zero(self):
        effect = V.first(parse(source('common/scripted_effects/imp_oil_prices_scripted_effects.txt')), 'imp_calculate_oil_dependency')
        m = V.Machine(('USA', 'SOV'))
        for tag, generation, total in [('USA', 0, 0), ('SOV', 20, 40)]:
            m.c = m.countries[tag]
            m.put('energy_sum', total)
            m.put('fossil_pp_energy_generation', generation)
        m.run(effect)
        self.assertEqual(m.countries['USA'].variables['imp_oil_dependency'], V.D('.7'))
        self.assertEqual(m.countries['SOV'].variables['imp_oil_dependency'], V.D('.85'))

    def test_oil_trade_aggregation_stays_in_the_pulse_country_scope(self):
        hooks = V.first(parse(source('common/on_actions/zzzzzz_imp_minis_on_actions.txt')), 'on_actions')
        pulse = V.values(hooks, 'on_monthly_LUX')[1]
        loop = next(body for key, _, body in V.walk(pulse) if key == 'every_country')
        class OilMachine(V.Machine):
            def run(self, rows):
                if not any(key == 'PREV' for key, _, _ in rows):
                    return super().run(rows)
                for key, operator, body in rows:
                    if key == 'PREV':
                        assert self.parents, 'PREV needs an enclosing country scope'
                        self.enter(self.parents[-1], body)
                    else:
                        super().run([(key, operator, body)])
        m = OilMachine(('LUX', 'USA', 'SOV'))
        for tag, exports, imports in [('LUX', 0, 0), ('USA', 1200, 100), ('SOV', 100, 20)]:
            m.c = m.countries[tag]
            m.put('resource_exported@oil', exports)
            m.put('resource_imported@oil', imports)
        m.c = m.countries['LUX']
        m.run(parse('set_temp_variable = { oil_exp_t = 0 } set_temp_variable = { oil_imp_t = 0 }'))
        m.run([('every_country', '=', loop)])
        self.assertEqual(m.get('oil_exp_t') - m.get('oil_imp_t'), V.D(1180))
        for tag in ['USA', 'SOV']:
            self.assertNotIn('oil_exp_t', m.countries[tag].variables)

    def test_gc_seat_effects_have_no_runtime_template_parameters(self):
        effects = parse(source('common/scripted_effects/COLDWAR_gc_unsc.txt'))
        text = source('common/scripted_effects/COLDWAR_gc_unsc.txt')
        self.assertNotIn('$seat$', text)
        for seat in ['europe', 'americas', 'africa', 'middle_east', 'asia']:
            self.assertIsInstance(V.first(effects, 'COLDWAR_gc_un_assign_' + seat), list)
            self.assertIsInstance(V.first(effects, 'COLDWAR_gc_un_clear_' + seat), list)


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Quality))
    out = ROOT / 'docs/audits/multiplayer_quality_20261023/quality_tests.json'
    out.write_text(json.dumps({'project': 'IMPERIA COLD WAR', 'tests': result.testsRun,
                              'passed': result.wasSuccessful(), 'failures': len(result.failures),
                              'errors': len(result.errors), 'live_multiplayer_tested': False}, indent=2) + '\n', encoding='utf-8')
    sys.exit(0 if result.wasSuccessful() else 1)
