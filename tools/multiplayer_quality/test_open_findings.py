# IMPERIA COLD WAR — Current integration regressions for the outstanding native findings.
"""Test loaded source and immutable currency lineage, without an MP/OOS claim."""
from collections import Counter
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/spain_1970_v2'))
sys.path.insert(0, str(ROOT / 'tools/frf_itl_currencies'))
from script_ast import parse, first, walk
from extension_manifest import reverse_extension


def source(name):
    return (ROOT / name).read_text(encoding='utf-8-sig')


def clean(rows):
    return [(k, o, clean(v) if isinstance(v, list) else v)
            for k, o, v in rows if not k.startswith('#')]


class OpenFindings(unittest.TestCase):
    def test_nuclear_safety_modifier_is_registered_for_synchronized_lookup(self):
        tokens = []
        for path in (ROOT / 'common/synchronized_dynamic_tokens').glob('*.txt'):
            tokens.extend(re.sub(r'#[^\n]*', '', path.read_text(encoding='utf-8-sig')).split())
        self.assertEqual(tokens.count('mdcw_nuclear_safety_target'), 1)
        self.assertTrue('modifier@mdcw_nuclear_safety_target' in source('common/scripted_effects/COLDWAR_nuclear_power_effects.txt'))

    def test_nuclear_budget_cap_is_declared_in_its_actual_loaded_file(self):
        rows = parse(source('common/scripted_effects/COLDWAR_nuclear_development_budget.txt'))
        self.assertEqual(first(rows, '@math_expressions_max'), '100000000')
        budget = first(rows, 'COLDWAR_price_nuclear_development_budget')
        used_constants = {v for _, _, v in walk(budget) if isinstance(v, str) and v.startswith('@')}
        declared = {k for k, _, v in rows if k.startswith('@') and isinstance(v, str)}
        self.assertFalse(used_constants - declared)

    def test_chinese_1985_opinion_rewards_have_registered_native_providers(self):
        providers = {k for path in (ROOT / 'common/opinion_modifiers').glob('*.txt')
                     for k, _, v in first(parse(path.read_text(encoding='utf-8-sig')), 'opinion_modifiers', [])
                     if isinstance(v, list)}
        rewards = [first(v, 'modifier') for k, _, v in walk(parse(source('common/national_focus/CHI_1985.txt')))
                   if k == 'add_opinion_modifier']
        self.assertTrue(rewards)
        self.assertEqual(set(rewards) - providers, set())
        self.assertEqual(rewards.count('economic_mission'), 11)

    def test_no_custom_country_calls_or_scenario_triggers_remain_at_startup_root(self):
        unsafe = []
        def visit(rows, scoped, path):
            for key, _, value in rows:
                if not scoped and re.match(r'(?:IMP_|ICW_|COLDWAR_|mdcw_|cw_sr_)', key):
                    unsafe.append((path, key))
                if isinstance(value, list):
                    enters_scope = bool(re.fullmatch(r'[A-Z0-9]{3}', key)) or key in {
                        'every_country', 'every_other_country', 'random_country', 'random_other_country',
                        'every_state', 'every_possible_country'}
                    visit(value, scoped or enters_scope, path)
        for path in (ROOT / 'common/on_actions').glob('*.txt'):
            actions = first(parse(path.read_text(encoding='utf-8-sig')), 'on_actions', [])
            for key, _, body in actions:
                if key == 'on_startup': visit(body, False, path.name)
        self.assertEqual(unsafe, [])

    def test_egyptian_land_doctrine_rewards_use_the_native_doctrine_provider(self):
        tree = first(parse(source('common/national_focus/COLDWAR_EGY_1970_focus.txt')), 'focus_tree')
        for name in ('soviet_deep_battle', 'western_training'):
            focus = next(v for k, _, v in tree if k == 'focus' and first(v, 'id') == 'COLDWAR_EGY_' + name)
            reward = first(focus, 'completion_reward')
            bonus = first(reward, 'add_doctrine_cost_reduction')
            self.assertIsNotNone(bonus)
            self.assertEqual(first(bonus, 'category'), 'land_doctrine')
            self.assertEqual(Decimal(first(bonus, 'cost_reduction')), Decimal('.75'))
            self.assertEqual(first(bonus, 'uses'), '1')
            self.assertFalse(any(k == 'add_tech_bonus' and first(v, 'category') == 'land_doctrine'
                                 for k, _, v in walk(reward)))

    def test_actual_startup_dispatches_have_country_scope_and_repeat_safely_on_reload(self):
        callbacks = {'COLDWAR_covert_action_1970_setup', 'COLDWAR_configure_research_slot_thresholds',
                     'ICW_pmc_cancel_pending_recruitment', 'international_systems_force_update',
                     'IMP_cold_war_initialize_military_industrial_complex',
                     'update_canal_blockage_flags', 'mdcw_suez_update_world'}
        paths = json.loads(source('docs/audits/open_findings_20261024/startup_scope_repairs.json'))['files']
        for order in (('USA', 'GER', 'DDR'), ('DDR', 'GER', 'USA')):
            flags = {'unrelated_saved_flag'}
            counts = Counter()
            def condition(rows, context):
                answers = []
                for key, _, value in rows:
                    if key == 'NOT': answer = not condition(value, context)
                    elif key == 'OR': answer = any(condition([row], context) for row in value)
                    elif key == 'has_global_flag': answer = value in flags
                    elif key == 'USA': answer = condition(value, 'USA')
                    elif key == 'ICW_pmc_system_active': answer = value == 'no'
                    elif key in ('IMP_is_1970_scenario', 'IMP_is_1985_scenario'):
                        answer = (key == 'IMP_is_1970_scenario') == (value == 'yes')
                    else: raise AssertionError(('Unmodelled startup trigger', key))
                    answers.append(answer)
                return all(answers)
            def execute(rows, context=None):
                for key, _, value in rows:
                    if key == 'clr_global_flag': flags.discard(value)
                    elif key == 'set_global_flag': flags.add(value)
                    elif key == 'set_variable':
                        self.assertTrue(all(k.lower().startswith('global.') for k, _, _ in value))
                    elif key == 'every_country':
                        for country in order:
                            if condition(first(value, 'limit', []), country):
                                execute([row for row in value if row[0] != 'limit'], country)
                    elif key == 'if':
                        if condition(first(value, 'limit', []), context):
                            execute([row for row in value if row[0] != 'limit'], context)
                    elif key in callbacks:
                        # The existing feature suites execute these providers.
                        # Here their boundary must receive a real country.
                        self.assertIn(context, order, key)
                        counts[key] += 1
                    else: raise AssertionError(('Unmodelled startup effect', key))
            for _ in range(2):
                for record in paths:
                    actions = first(parse(source(record['path'])), 'on_actions')
                    execute(first(first(actions, 'on_startup'), 'effect'))
                    self.assertEqual(flags, {'unrelated_saved_flag'})
            for callback in callbacks:
                self.assertEqual(counts[callback], 6 if callback == 'ICW_pmc_cancel_pending_recruitment' else 2, callback)

    def test_colonial_event_namespaces_are_registered_and_ids_are_unique(self):
        ids = set()
        for name in ('COLDWAR_colonial_affairs', 'COLDWAR_colonial_contacts'):
            rows = parse(source('events/' + name + '.txt'))
            self.assertEqual(first(rows, 'add_namespace'), name)
            self.assertIsNone(first(rows, 'namespace'))
            for key, _, event in rows:
                if key not in ('country_event', 'news_event'):
                    continue
                identifier = first(event, 'id')
                self.assertTrue(identifier.startswith(name + '.'))
                self.assertNotIn(identifier, ids)
                ids.add(identifier)
        self.assertEqual(len(ids), 8)

    def test_syrian_event_files_have_no_orphaned_effects(self):
        for kind in ('foreign', 'politics'):
            rows = clean(parse(source(f'events/COLDWAR_SYR_{kind}_events.txt')))
            self.assertTrue(rows)
            self.assertFalse([k for k, _, _ in rows
                              if k not in ('add_namespace', 'country_event', 'news_event')])
            for key, _, event in rows:
                if key == 'country_event':
                    self.assertIsNotNone(first(event, 'id'))

    def test_cypriot_yugoslav_contracts_route_to_registered_country_and_keep_receipts(self):
        tags = source('common/country_tags/00_countries.txt')
        self.assertRegex(tags, r'(?m)^SER\s*=')
        self.assertIn('set_cosmetic_tag = YUG_Coldwar_Communism', source('history/countries/SER - Serbia.txt'))
        decisions = parse(source('common/decisions/COLDWAR_CYP_1970_decisions.txt'))
        found = 0
        for _, _, category in decisions:
            if not isinstance(category, list):
                continue
            for key, _, body in category:
                if '_YUG_' not in key:
                    continue
                found += 1
                self.assertIn(('original_tag', '=', 'SER'), list(walk(body)), key)
        self.assertEqual(found, 4)
        for directory in ('common', 'events', 'localisation/english'):
            for path in (ROOT / directory).rglob('COLDWAR_CYP_1970*'):
                if path.is_file() and path.suffix in ('.txt', '.yml'):
                    self.assertNotRegex(path.read_text(encoding='utf-8-sig'), r'\bYUG\b', str(path))
        self.assertTrue('COLDWAR_CYP_1970_pending_YUG_p1_finance_a' in source('common/scripted_effects/COLDWAR_CYP_1970_effects.txt'))

    def test_custom_numeric_modifier_blocks_do_not_drop_duplicate_entries(self):
        checked = 0
        for directory in ('ideas', 'bop', 'dynamic_modifiers'):
            for path in (ROOT / 'common' / directory).glob('*.txt'):
                if not path.name.startswith(('COLDWAR', 'IMP', 'mdcw', 'ICW')):
                    continue
                for key, _, block in walk(parse(path.read_text(encoding='utf-8-sig'))):
                    if key != 'modifier' or not isinstance(block, list):
                        continue
                    counts = Counter(k for k, o, v in block if o == '=' and isinstance(v, str)
                                     and re.fullmatch(r'-?\d+(?:\.\d+)?', v))
                    self.assertFalse([k for k, n in counts.items() if n > 1], str(path))
                    checked += 1
        self.assertGreater(checked, 100)
        rows = parse(source('common/bop/COLDWAR_DDR_1970_inner_german_course.txt'))
        ranges = [v for k, _, v in walk(rows) if k == 'range'
                  and first(v, 'id') == 'COLDWAR_DDR_german_course_bop_total_demarcation']
        self.assertEqual(Decimal(first(first(ranges[0], 'modifier'), 'drift_defence_factor')), Decimal('.35'))

    def test_german_bop_matches_current_canonical_generator(self):
        sys.path.insert(0, str(ROOT / 'tools/west_germany_1970'))
        import systems
        current = clean(parse(source('common/bop/COLDWAR_GER_1970_bop.txt')))
        self.assertEqual(current, clean(parse(systems.bop())))

    def test_currency_law_history_is_exact_beneath_documented_later_changes(self):
        name = 'common/ideas/AA_law_expanded_economics.txt'
        # The existing realignment manifest proves every inserted hook before
        # reversal. Keep all original baseline hashes and approval files intact.
        period = reverse_extension(name, (ROOT / name).read_bytes()).decode('utf-8')
        old_gate = ('visible = { date < 1999.1.1 }\n'
                    '\t\t\tavailable = { date < 1999.1.1 check_variable = { global.dem_issuer > 0 } }')
        new_gate = ('visible = { always = yes }\n'
                    '\t\t\tavailable = { check_variable = { global.dem_issuer > 0 } }')
        self.assertEqual(period.count(new_gate), 1)
        original = re.sub(r'^[ \t]*# IMPERIA[^\n]*\n', '', period, flags=re.M).replace(new_gate, old_gate, 1).encode('utf-8')
        record = json.loads(source('tools/currency_balance/changes.json'))['files'][name]
        self.assertEqual(hashlib.sha256(original).hexdigest(), record['after_sha256'])
        for edit in reversed(record['edits']):
            at, after = edit['offset_after'], edit['after'].encode('utf-8')
            self.assertEqual(original[at:at + len(after)], after)
            original = original[:at] + edit['before'].encode('utf-8') + original[at + len(after):]
        self.assertEqual(hashlib.sha256(original).hexdigest(), record['before_sha256'])

    def test_current_currency_drawbacks_and_ddr_reader_match_numeric_policy(self):
        laws = first(first(parse(source('common/ideas/AA_law_expanded_economics.txt')), 'ideas'), 'reserve_currency')
        policy = json.loads(source('tools/currency_balance/policy.json'))
        self.assertEqual({k for k, _, v in laws if isinstance(v, list)}, set(policy['added']) | set(policy['retained']))
        for name, expected in (policy['added'] | policy['retained']).items():
            modifier = first(first(laws, name), 'modifier')
            for key, number in expected.items():
                values = [v for k, _, v in walk(modifier) if k == key]
                self.assertEqual([Decimal(v) for v in values], [Decimal(str(number))], (name, key))
        ddr = first(first(laws, 'ddr_mark'), 'modifier')
        self.assertEqual(Decimal(first(ddr, 'interest_rate_multiplier_modifier')), Decimal('-.5'))
        interest = first(parse(source('common/scripted_effects/00_money_system.txt')), 'calculate_interest_rate')
        self.assertIn(('add', '=', 'modifier@interest_rate_multiplier_modifier'), list(walk(interest)))


if __name__ == '__main__':
    unittest.main(verbosity=2)
