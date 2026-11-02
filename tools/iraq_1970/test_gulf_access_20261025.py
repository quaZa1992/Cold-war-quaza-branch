# IMPERIA COLD WAR — Live Kuwait-war and Gulf subtree integration regressions.
"""Read-only bounded AST checks. No game, external compiler or save is started."""
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from usa_module import generate, P
from test_usa_module import World
from script_ast import parse, first, values


class GulfAccessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = generate(ROOT)
        cls.focuses = {first(n, 'id'): n for n in values(parse(cls.out['tools/iraq_1970/staged/USA_GULF_FOCUS_FRAGMENT.txt']), 'focus')}

    def world(self):
        w = World(self.out)
        for sid in ('172', '488'):
            w.s[sid].owner = w.s[sid].controller = 'KUW'
        return w

    def check(self, w, key, country='USA'):
        return w.tests(w.triggers[P + key], w.c[country])

    def test_peacetime_1970_does_not_create_gulf_crisis(self):
        w = self.world()
        self.assertFalse(self.check(w, 'kuwait_unresolved'))
        self.assertFalse(self.check(w, 'military_opening'))

    def test_real_kuwait_war_needs_no_special_focus_or_aggression_receipt(self):
        w = self.world(); w.c['IRQ'].wars.add('KUW')
        self.assertEqual(w.global_flags, set())
        self.assertTrue(self.check(w, 'kuwait_unresolved'))
        self.assertTrue(self.check(w, 'military_opening'))
        self.assertNotIn('IRQ', w.c['USA'].wars)

    def test_occupation_and_annexation_remain_a_crisis_after_war_ends(self):
        for owner, controller, exists in [('IRQ', 'IRQ', True), ('KUW', 'IRQ', True), ('IRQ', 'IRQ', False)]:
            w = self.world(); w.s['172'].owner = owner; w.s['172'].controller = controller; w.c['KUW'].exists = exists
            self.assertTrue(self.check(w, 'kuwait_unresolved'))

    def test_puppet_kuwait_is_not_restored_independence(self):
        w = self.world(); w.c['KUW'].subject = 'IRQ'
        self.assertTrue(self.check(w, 'kuwait_unresolved'))

    def test_restored_kuwait_closes_crisis_despite_historical_aggression_flag(self):
        w = self.world(); w.global_flags.add('COLDWAR_IRQ_gulf_iraq_attacked_kuwait')
        self.assertFalse(self.check(w, 'kuwait_unresolved'))

    def test_real_withdrawal_opens_finite_postwar_window_once(self):
        w = self.world(); w.c['IRQ'].wars.add('KUW')
        w.s['172'].owner = w.s['172'].controller = 'IRQ'
        w.call(P + 'observe_kuwait_crisis', 'IRQ')
        self.assertTrue(w.flag(w.c['USA'], P + 'kuwait_crisis_recorded'))
        w.c['IRQ'].wars.clear(); w.s['172'].owner = w.s['172'].controller = 'KUW'; w.call(P + 'observe_kuwait_crisis', 'IRQ')
        original = w.c['IRQ'].flags[P + 'recent_defeat']
        self.assertTrue(self.check(w, 'military_opening'))
        w.day += 10; w.call(P + 'observe_kuwait_crisis', 'IRQ')
        self.assertEqual(w.c['IRQ'].flags[P + 'recent_defeat'], original)
        w.day = original + 1
        self.assertFalse(self.check(w, 'military_opening'))

    def test_unoccupied_diplomatic_settlement_does_not_invent_military_defeat(self):
        w = self.world(); w.c['IRQ'].wars.add('KUW')
        w.call(P + 'observe_kuwait_crisis', 'IRQ')
        w.c['IRQ'].wars.clear(); w.call(P + 'observe_kuwait_crisis', 'IRQ')
        self.assertFalse(self.check(w, 'military_opening'))
        self.assertFalse(w.flag(w.c['IRQ'], P + 'recent_defeat'))

    def test_already_belligerent_usa_bypasses_redundant_wargoal_focus(self):
        focus = self.focuses[P + 'desert_storm']
        w = self.world()
        self.assertFalse(w.tests(first(focus, 'bypass'), w.c['USA']))
        w.c['USA'].wars.add('IRQ')
        self.assertTrue(w.tests(first(focus, 'bypass'), w.c['USA']))

    def test_northern_channels_have_three_real_alternative_entry_roots(self):
        focus = self.focuses[P + 'appeal']
        self.assertEqual([values(p, 'focus') for p in values(focus, 'prerequisite')], [[P + n for n in ('desert_shield', 'desert_storm', 'coalition')]])
        w = self.world(); w.c['IRQ'].wars.add('KUW')
        self.assertTrue(w.tests(first(focus, 'available'), w.c['USA']))

    def test_retired_contact_card_stays_hidden_and_relief_stays_independent(self):
        self.assertEqual(first(first(self.focuses[P + 'contacts'], 'allow_branch'), 'always'), 'no')
        for key in ('comfort', 'northern_access'):
            self.assertEqual(values(self.focuses[P + key], 'prerequisite'), [])

    def test_distant_basing_does_not_supply_a_clandestine_border_network(self):
        w = self.world(); w.c['TUR'].flags.clear(); w.c['USA'].access.clear()
        w.c['FRA'].flags[P + 'host_north'] = None; w.c['USA'].access.add('FRA')
        self.assertTrue(self.check(w, 'route_open'))
        self.assertFalse(self.check(w, 'clandestine_route_open'))
        before = w.c['USA'].var['treasury'], w.c['USA'].stock
        w.call(P + 'initial_underground')
        self.assertEqual((w.c['USA'].var['treasury'], w.c['USA'].stock), before)

    def test_iran_decides_and_host_fee_is_charged_once_without_host_cash_grant(self):
        w = self.world(); w.c['TUR'].flags.clear(); w.c['USA'].access.clear()
        self.assertFalse(self.check(w, 'clandestine_route_open'))
        w.c['USA'].flags[P + 'pending_north_PER'] = None
        host_cash = w.c['PER'].var['treasury']
        w.accept(14, 'PER', option=1)
        self.assertTrue(self.check(w, 'clandestine_route_open'))
        self.assertEqual(w.c['USA'].var['treasury'], 9.5)
        self.assertEqual(w.c['PER'].var['treasury'], host_cash)
        w.c['USA'].flags[P + 'pending_north_PER'] = None
        w.accept(14, 'PER', option=1)
        self.assertEqual(w.c['USA'].var['treasury'], 9.5)

    def test_border_route_loss_stops_subsidy_without_erasing_committed_weapons(self):
        w = self.world(); w.call(P + 'initial_underground')
        self.assertEqual(w.c['USA'].var[P + 'cache'], 1000)
        w.c['TUR'].flags.clear(); w.c['USA'].access.clear()
        cash = w.c['USA'].var['treasury']
        w.tick('USA')
        self.assertEqual(w.c['USA'].var[P + 'support_days'], 0)
        self.assertEqual(w.c['USA'].var[P + 'cache'], 1000)
        self.assertEqual(w.c['USA'].var['treasury'], cash)

    def test_every_host_rechecks_full_first_fee_at_acceptance(self):
        for host, event in [('TUR',10),('SAU',11),('ENG',12),('FRA',13),('PER',14)]:
            for kind, option, invoice in [('staging',0,2),('north',1,.5)]:
                for cash, skip in [(invoice-.001,False),(10,True)]:
                    w = self.world(); w.c['USA'].var['treasury'] = cash
                    w.c[host].flags.clear(); w.c['USA'].access.clear()
                    w.c['USA'].flags[P + 'pending_' + kind + '_' + host] = None
                    if skip: w.c['USA'].flags['MD_skip_treasury_cost'] = None
                    w.accept(event, host, option=option)
                    self.assertEqual(w.c['USA'].var['treasury'], cash, (host,kind,cash,skip))
                    self.assertFalse(w.flag(w.c[host],P + 'host_' + kind), (host,kind,cash,skip))
                    self.assertNotIn(host,w.c['USA'].access)

    def rising_world(self):
        w = self.world(); w.call(P + 'initial_underground'); w.c['IRQ'].wars.add('KUW')
        w.s['164'].resistance = w.s['633'].resistance = 80
        return w

    def test_existing_peaceful_kurdish_actor_cannot_be_forced_into_a_rising(self):
        w = self.rising_world(); w.c['KUR'].exists = True
        w.s['630'].owner = w.s['630'].controller = 'KUR'
        w.call(P + 'bounded_uprising', 'IRQ')
        self.assertNotIn('IRQ',w.c['KUR'].wars)
        self.assertEqual(w.s['164'].owner,'IRQ'); self.assertEqual(w.s['633'].owner,'IRQ')
        self.assertFalse(w.flag(w.c['KUR'],P + 'local_columns_created'))
        self.assertFalse(w.flag(w.c['IRQ'],P + 'uprising_fired'))

    def test_existing_independent_actor_can_explicitly_join_the_rising(self):
        w = self.rising_world(); w.c['KUR'].exists = True
        w.s['630'].owner = w.s['630'].controller = 'KUR'
        w.c['KUR'].flags[P + 'organized_opposition'] = None
        w.call(P + 'bounded_uprising', 'IRQ')
        self.assertIn('IRQ',w.c['KUR'].wars)
        self.assertEqual(w.s['164'].owner,'KUR'); self.assertEqual(w.s['633'].owner,'KUR')

    def test_new_rebel_actor_can_receive_both_prepared_states_once(self):
        w = self.rising_world(); w.call(P + 'bounded_uprising','IRQ')
        self.assertEqual(w.s['164'].owner,'KUR'); self.assertEqual(w.s['633'].owner,'KUR')
        self.assertIn('IRQ',w.c['KUR'].wars)
        count = len(w.units); w.call(P + 'bounded_uprising','IRQ')
        self.assertEqual(len(w.units),count)

    def test_canonical_overlay_preserves_every_other_focus(self):
        sys.path.insert(0, str(ROOT / 'tools/usa_1970_expansion'))
        import gulf_revision
        from focus_prerequisite_ui import nodes, field
        source = (ROOT / 'common/national_focus/USA_1970.txt').read_text(encoding='utf-8-sig')
        patched = gulf_revision.patch_tree(source)
        def other(text):
            tree = next(n for n in nodes(text) if n.key == 'focus_tree')
            return {field(n.children(), 'id'): text[n.start:n.end] for n in tree.children() if n.key == 'focus' and not str(field(n.children(), 'id')).startswith(P)}
        self.assertEqual(other(source), other(patched))
        self.assertEqual(len(other(source)), 286)


if __name__ == '__main__':
    unittest.main(verbosity=2)
