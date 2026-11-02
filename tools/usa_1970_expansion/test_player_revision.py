# IMPERIA COLD WAR — Integrated USA player-revision regression checks.
"""Exercise old-save modifier migration and inspect real integration boundaries.

These tests read emitted production source. They do not start HOI4, mutate a
campaign, or establish live tooltip, save-load or multiplayer behavior.
"""
from collections import defaultdict
from decimal import Decimal as D
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from focus_prerequisite_ui import nodes, field


def read(path):
    return nodes((ROOT / path).read_text(encoding='utf-8-sig'))


def walk(items):
    for n in items:
        yield n
        yield from walk(n.children())


class Migration:
    def __init__(self, completed=(), flags=(), tag='USA', scenario=True):
        self.completed, self.flags = set(completed), set(flags)
        self.tag, self.scenario = tag, scenario
        self.variables, self.refreshes = defaultdict(D), 0

    def valid(self, items):
        def check(n):
            if n.key == 'OR': return any(check(c) for c in n.children())
            if n.key == 'NOT': return not all(check(c) for c in n.children())
            if n.key == 'has_country_flag': return n.value in self.flags
            if n.key == 'has_completed_focus': return n.value in self.completed
            if n.key == 'tag': return self.tag == n.value
            if n.key == 'IMP_is_1970_scenario': return self.scenario == (n.value == 'yes')
            raise AssertionError(('Unmodeled migration condition', n.key))
        return all(check(n) for n in items)

    def run(self, items):
        for n in items:
            if n.key == 'if':
                if self.valid(next(c for c in n.children() if c.key == 'limit').children()):
                    self.run([c for c in n.children() if c.key != 'limit'])
            elif n.key == 'add_to_variable':
                c, = n.children()
                self.variables[c.key] += D(c.value)
            elif n.key == 'set_country_flag': self.flags.add(n.value)
            elif n.key == 'clr_country_flag': self.flags.discard(n.value)
            elif n.key == 'force_update_dynamic_modifier': self.refreshes += 1
            else: raise AssertionError(('Unmodeled migration effect', n.key))


class PlayerRevisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.effects = {n.key: n for n in read('common/scripted_effects/COLDWAR_USA_1970_expansion.txt')}
        cls.migration = cls.effects['COLDWAR_USA_early_legacy_bundle_migrate'].children()
        cls.roots = ('USA_1970_F7', 'USA_1970_E9', 'USA_1970_NIX_F3')

    def test_pre_revision_save_reverses_exact_seven_old_deltas_once(self):
        m = Migration(self.roots)
        m.run(self.migration)
        expected = {'federal_budget_bureaucracy_cost': D('-.06'),
                    'domestic_foreign_influence_defense': D('-.02'),
                    'federal_budget_export_money_return': D('-.01'),
                    'federal_budget_personnel_cost': D('-.02'),
                    'domestic_offensive_foreign_influence': D('.01')}
        self.assertEqual(dict(m.variables), expected)
        m.run(self.migration)
        self.assertEqual(dict(m.variables), expected)
        self.assertEqual(m.refreshes, 1)

    def test_unpaid_pending_roots_have_no_historic_deltas_to_reverse(self):
        flags = ['COLDWAR_USA_legacy_pending_' + f.removeprefix('USA_1970_') for f in self.roots]
        m = Migration(self.roots, flags)
        m.run(self.migration)
        self.assertEqual(dict(m.variables), {})
        self.assertFalse(set(flags) & m.flags)

    def test_paid_receipt_wins_over_stale_pending_marker(self):
        m = Migration(['USA_1970_F7'], ['COLDWAR_USA_legacy_pending_F7', 'COLDWAR_USA_legacy_done_F7'])
        m.run(self.migration)
        self.assertEqual(dict(m.variables), {'federal_budget_bureaucracy_cost': D('-.01')})

    def test_current_revision_root_authorisations_never_reverse_new_rewards(self):
        flags = ['COLDWAR_USA_early_root_israel_authorised', 'COLDWAR_USA_early_root_trade_authorised', 'COLDWAR_USA_early_alliances_authorised']
        m = Migration(self.roots, flags)
        m.run(self.migration)
        self.assertEqual(dict(m.variables), {})

    def test_new_start_receipt_prevents_later_focus_reversal(self):
        m = Migration()
        m.run(self.migration)
        m.completed.update(self.roots)
        m.run(self.migration)
        self.assertEqual(dict(m.variables), {})

    def test_other_country_and_scenario_untouched(self):
        for m in (Migration(self.roots, tag='CAN'), Migration(self.roots, scenario=False)):
            m.run(self.migration)
            self.assertEqual(dict(m.variables), {})
            self.assertEqual(m.flags, set())

    def test_migration_precedes_new_early_initialization(self):
        calls = [n.key for n in walk(self.effects['COLDWAR_USA_expansion_initialize'].children())]
        self.assertLess(calls.index('COLDWAR_USA_early_legacy_bundle_migrate'), calls.index('COLDWAR_USA_early_initialize'))

    def test_all_four_native_membership_boundaries_have_one_callback(self):
        effects = {n.key: n for n in read('common/scripted_effects/01_NATO_effects.txt')}
        for key in ('NATO_join', 'NATO_leave', 'NATO_major_non_nato_ally_join', 'NATO_major_non_nato_ally_leave'):
            calls = [n.key for n in walk(effects[key].children())]
            for helper in ('COLDWAR_USA_early_membership_changed', 'COLDWAR_USA_early_reconcile_all', 'COLDWAR_USA_agreements_reconcile_all'):
                self.assertEqual(calls.count(helper), 1, (key, helper))

    def test_direct_native_membership_grants_also_reach_offer_dispatch(self):
        for path, idea in [('common/ideas/Factions.txt', 'NATO_member'), ('common/ideas/united_states.txt', 'Major_Non_NATO_Ally')]:
            target = next(n for n in walk(read(path)) if n.key == idea)
            callback, = [n for n in target.children() if n.key == 'on_add']
            calls = [n.key for n in walk(callback.children())]
            self.assertEqual(calls.count('COLDWAR_USA_early_membership_changed'), 1)
            self.assertTrue(any(n.key == 'has_country_flag' and n.value == 'COLDWAR_USA_expansion_initialized' for n in walk(callback.children())))

    def test_surviving_nixon_retains_office_but_ford_succession_clears_it(self):
        ev = next(n for n in read('events/USA_1970_events.txt') if n.key == 'country_event' and field(n.children(), 'id') == 'USA_1970.10')
        for suffix, required, forbidden in [('a', 'clr_country_flag', 'set_country_flag'), ('b', 'set_country_flag', 'clr_country_flag')]:
            option = next(n for n in ev.children() if n.key == 'option' and field(n.children(), 'name') == 'USA_1970.10.' + suffix)
            flags = {(n.key, n.value) for n in option.children() if not isinstance(n.value, list)}
            self.assertIn((required, 'USA_1970_nixon_presidency'), flags)
            self.assertNotIn((forbidden, 'USA_1970_nixon_presidency'), flags)

    def test_israeli_funding_accepts_real_new_parent_without_faking_legacy_receipt(self):
        decisions = read('common/decisions/USA_1970_policy_decisions.txt')
        decision = next(n for n in walk(decisions) if n.key == 'USA_1970_decision_middle_east_security_primacy')
        available = next(n for n in decision.children() if n.key == 'available')
        alternatives = next(n for n in available.children() if n.key == 'OR' and any(c.key == 'has_country_flag' and c.value == 'USA_1970_israel_package_completed' for c in n.children()))
        self.assertIn('COLDWAR_USA_early_israel_usa', [n.value for n in alternatives.children() if n.key == 'has_idea'])
        for path in ('common/decisions/USA_1970_policy_decisions.txt', 'common/decisions/categories/USA_1970_policy_decision_categories.txt'):
            self.assertTrue(any(n.key == 'has_completed_focus' and n.value == 'USA_1970_F7' for n in walk(read(path))))


if __name__ == '__main__':
    unittest.main()
