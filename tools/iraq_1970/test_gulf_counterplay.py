# IMPERIA COLD WAR — Local Iraqi counterplay generated-source regressions.
"""Exercise the emitted AST. No file writes or native engine claims."""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from usa_module import generate
from gulf_counterplay import P, NORTH, OP, AGE, RECEIPT, MIGRATED
from test_usa_module import World, ROOT, parse, first, values


class Model(World):
    def run(self, rows, c, root=None, prev=None, source=None):
        # Only nonexecuting native preview boundaries are added to the model.
        # Hidden effects run the same real helper as the generated decision.
        flattened = []
        for row in rows:
            if row[0] in ('effect_tooltip', 'custom_effect_tooltip'):
                continue
            if row[0] == 'hidden_effect':
                flattened.extend(row[2])
            else:
                flattened.append(row)
        return super().run(flattened, c, root, prev, source)

    def days(self, count):
        for _ in range(count):
            self.day += 1
            self.call(P + 'irq_daily', 'IRQ')


class LocalCounterplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = generate(ROOT)
        cls.decisions = dict((k, v) for k, _, v in first(parse(cls.out['common/decisions/COLDWAR_USA_gulf_decisions.txt']), P + 'category'))

    def world(self, troops=None, underground=True):
        w = Model(self.out)
        w.c['IRQ'].troops = troops if troops is not None else {'164': 2, '633': 2}
        if underground:
            w.call(P + 'initial_underground')
        return w

    def test_native_state_list_counts_only_actual_local_divisions(self):
        w = self.world({'164': 2, '633': 0, '165': 100})
        for state, expected in [('164', True), ('633', False)]:
            predicate = parse(f'num_divisions_in_states = {{ count > 1 states = {{ {state} }} }}')
            self.assertEqual(w.tests(predicate, w.c['IRQ']), expected)
        w.c['IRQ'].troops = {'165': 100}
        cash = w.c['IRQ'].var['treasury'];w.call(P + 'start_security', 'IRQ')
        self.assertEqual(w.c['IRQ'].var['treasury'], cash)
        self.assertFalse(w.idea(w.c['IRQ'], P + 'security_small'))

    def test_local_delivery_needs_thirty_days_and_never_reaches_remote_state(self):
        w = self.world({'164': 2});w.call(P + 'start_security', 'IRQ');w.days(29)
        self.assertEqual(w.s['164'].resistance, 60)
        w.days(1)
        self.assertEqual(w.s['164'].resistance, 45)
        self.assertEqual(w.s['633'].resistance, 60)
        self.assertEqual(w.s['164'].targets['19709102'][0], -20)
        self.assertNotIn('19709102', w.s['633'].targets)

    def test_departure_resets_local_preparation_and_preserves_paid_overhead(self):
        w = self.world({'164': 2});w.call(P + 'start_security', 'IRQ');w.days(20)
        w.c['IRQ'].troops = {};w.days(1)
        self.assertEqual(w.s['164'].var[AGE], 0)
        self.assertTrue(w.idea(w.c['IRQ'], P + 'security_small'))
        w.c['IRQ'].troops = {'164': 2};w.days(29)
        self.assertEqual(w.s['164'].resistance, 60)
        w.days(1);self.assertEqual(w.s['164'].resistance, 45)

    def test_delivered_reduction_cannot_replay_when_troops_return(self):
        w = self.world({'164': 2});w.call(P + 'start_security', 'IRQ');w.days(30)
        receipt = w.s['164'].var[RECEIPT];w.c['IRQ'].troops = {};w.call(P + 'security_reconcile_local', 'IRQ')
        self.assertEqual(w.s['164'].var[AGE], 0);self.assertNotIn('19709102', w.s['164'].targets)
        w.c['IRQ'].troops = {'164': 2};w.days(30)
        self.assertEqual(w.s['164'].resistance, 45);self.assertEqual(w.s['164'].var[RECEIPT], receipt)
        self.assertIn('19709102', w.s['164'].targets)

    def test_foreign_pulse_is_local_and_resumes_with_no_troops(self):
        w = self.world({'164': 2});w.call(P + 'start_security', 'IRQ');w.days(30)
        w.s['164'].resistance = w.s['633'].resistance = 65
        w.c['USA'].var[P + 'pulse_age'] = 29;w.call(P + 'usa_daily')
        self.assertEqual(w.s['164'].resistance, 65);self.assertEqual(w.s['633'].resistance, 75)
        w.day += 1;w.c['IRQ'].troops = {};w.c['USA'].var[P + 'pulse_age'] = 29;w.call(P + 'usa_daily')
        self.assertEqual(w.s['164'].resistance, 75)
        self.assertTrue(w.idea(w.c['IRQ'], P + 'security_small'))
        w.call(P + 'irq_daily', 'IRQ');self.assertNotIn('19709102', w.s['164'].targets)

    def test_major_requires_three_in_each_secured_state(self):
        w = self.world({'164': 2, '633': 2});cash = w.c['IRQ'].var['treasury'];w.call(P + 'start_major_operation', 'IRQ')
        self.assertEqual(w.c['IRQ'].var['treasury'], cash)
        w.c['IRQ'].troops['164'] = 3;w.call(P + 'start_major_operation', 'IRQ');w.days(30)
        self.assertAlmostEqual(w.c['IRQ'].var['treasury'], cash - .4)
        self.assertEqual(w.s['164'].resistance, 35);self.assertEqual(w.s['633'].resistance, 60)
        self.assertEqual(w.s['164'].targets['19709102'][0], -35)

    def test_invoice_repeat_and_withdrawal_cannot_evade_cooldown(self):
        w = self.world();cash = w.c['IRQ'].var['treasury'];w.call(P + 'start_security', 'IRQ');w.call(P + 'start_security', 'IRQ')
        self.assertAlmostEqual(w.c['IRQ'].var['treasury'], cash - .2);self.assertEqual(w.c['IRQ'].var[OP], 1)
        w.call(P + 'end_security', 'IRQ');w.day = 89;w.call(P + 'start_major_operation', 'IRQ')
        self.assertAlmostEqual(w.c['IRQ'].var['treasury'], cash - .2)
        w.day = 90;w.call(P + 'start_security', 'IRQ')
        self.assertAlmostEqual(w.c['IRQ'].var['treasury'], cash - .4);self.assertEqual(w.c['IRQ'].var[OP], 2)

    def test_preemptive_operation_requires_actual_war_and_can_prepare_before_seeds(self):
        w = self.world({'164': 2}, underground=False);w.call(P + 'start_security', 'IRQ')
        self.assertFalse(w.idea(w.c['IRQ'], P + 'security_small'))
        w.c['IRQ'].wars.add('KUW');w.c['KUW'].wars.add('IRQ');w.call(P + 'start_security', 'IRQ');w.days(30)
        self.assertTrue(w.idea(w.c['IRQ'], P + 'security_small'));self.assertIsNone(w.s['164'].resistance)
        self.assertEqual(w.s['164'].var[AGE], 30)
        self.assertTrue(w.flag(w.c['IRQ'], P + 'kuwait_crisis_seen'))
        self.assertTrue(w.flag(w.c['USA'], P + 'kuwait_crisis_recorded'))
        w.call(P + 'initial_underground');w.call(P + 'irq_daily', 'IRQ')
        self.assertEqual(w.s['164'].resistance, 45);self.assertEqual(w.s['633'].resistance, 60)

    def test_insufficient_funds_zero_gdp_and_wrong_country_fail_closed(self):
        for cash, gdp, caller in [(.199, 10, 'IRQ'), (10, 0, 'IRQ'), (10, 10, 'USA')]:
            with self.subTest(cash=cash, gdp=gdp, caller=caller):
                w = self.world();w.c['IRQ'].var.update(treasury=cash, gdp_total=gdp)
                w.call(P + 'start_security', caller)
                self.assertEqual(w.c['IRQ'].var['treasury'], cash)
                self.assertFalse(w.idea(w.c['IRQ'], P + 'security_small'))
                self.assertNotIn(OP, w.c['IRQ'].var)

    def test_old_completed_paid_operation_preserves_all_reduction_receipts(self):
        w = self.world({'164': 2});irq = w.c['IRQ'];irq.ideas[P + 'security_small'] = 90;irq.var[P + 'security_target'] = -20
        w.s['164'].resistance = w.s['633'].resistance = 45;cash = irq.var['treasury'];w.call(P + 'irq_daily', 'IRQ')
        self.assertEqual(irq.var[OP], 1);self.assertTrue(w.flag(irq, MIGRATED))
        self.assertEqual(w.s['164'].resistance, 45);self.assertEqual(w.s['164'].var[RECEIPT], 1)
        self.assertEqual(w.s['633'].var[RECEIPT], 1)
        irq.troops['633'] = 2;w.days(30)
        self.assertEqual(w.s['633'].resistance, 45);self.assertEqual(irq.var['treasury'], cash)

    def test_old_undelivered_operation_does_not_charge_or_deliver_twice(self):
        w = self.world({'164': 2});irq = w.c['IRQ'];irq.ideas[P + 'security_small'] = 90;irq.flags[P + 'security_delivery'] = 90;irq.var[P + 'security_target'] = -20
        irq.var[P + 'security_age'] = 20;cash = irq.var['treasury'];w.days(29)
        self.assertEqual(w.s['164'].resistance, 60)
        w.days(1);self.assertEqual(w.s['164'].resistance, 45)
        for _ in range(40):w.call(P + 'security_reduce', 'IRQ')
        self.assertEqual(w.s['164'].resistance, 45);self.assertEqual(irq.var['treasury'], cash)

    def test_repeated_observers_do_not_accelerate_calendar_readiness(self):
        w = self.world({'164': 2});w.call(P + 'start_security', 'IRQ');w.days(1)
        for _ in range(50):w.call(P + 'security_reconcile_local', 'IRQ')
        self.assertEqual(w.s['164'].var[AGE], 1);self.assertEqual(w.s['164'].resistance, 60)

    def test_forty_five_day_warning_can_be_averted_with_stationed_forces(self):
        w = self.world();w.c['USA'].wars.add('IRQ');w.c['IRQ'].wars.add('USA');w.s['164'].resistance = w.s['633'].resistance = 80
        w.days(30);self.assertTrue(w.flag(w.c['IRQ'], P + 'uprising_warning'))
        w.call(P + 'start_security', 'IRQ');w.days(30)
        self.assertEqual(w.s['164'].resistance, 65);self.assertEqual(w.s['633'].resistance, 65)
        w.days(14);self.assertFalse(w.flag(w.c['IRQ'], P + 'uprising_warning'))
        self.assertFalse(w.flag(w.c['IRQ'], P + 'uprising_fired'));self.assertEqual(w.s['164'].owner, 'IRQ')

    def test_decisions_keep_exact_native_numeric_previews_without_execution(self):
        for did, quote, idea, minimum in [('COLDWAR_IRQ_northern_security', 'security_quote', 'security_small', 2), ('COLDWAR_IRQ_northern_major_operation', 'major_quote', 'security_major', 3)]:
            w = self.world({'164': minimum});w.call(P + 'irq_daily', 'IRQ')
            body = self.decisions[did];preview = first(first(body, 'complete_effect'), 'effect_tooltip')
            self.assertIn(P + quote, str(preview));self.assertIn(P + idea, str(preview))
            before = copy.deepcopy((w.c, w.s));w.run([('effect_tooltip', '=', preview)], w.c['IRQ']);self.assertEqual(before, (w.c, w.s))
            w.run(first(body, 'complete_effect'), w.c['IRQ'])
            self.assertAlmostEqual(w.c['IRQ'].var['treasury'], 10 - (.2 if minimum == 2 else .4))

    def test_reconstruction_uses_native_capacity_and_adds_its_slot_once(self):
        w = self.world(underground=False);local = w.c['KUR'];local.exists = True
        local.flags[P + 'reconstruction_received'] = None
        state = w.s['164'];state.owner = state.controller = 'KUR'
        body = self.decisions[P + 'local_rebuild']
        self.assertTrue(w.tests(first(body, 'available'), local))
        cash = local.var['treasury'];w.run(first(body, 'complete_effect'), local)
        self.assertEqual(state.infrastructure, 3);self.assertEqual(state.shared_slots, 1)
        self.assertAlmostEqual(local.var['treasury'], cash - .2)
        w.run(first(body, 'complete_effect'), local)
        self.assertEqual(state.infrastructure, 3);self.assertEqual(state.shared_slots, 1)
        self.assertAlmostEqual(local.var['treasury'], cash - .2)
        capped = self.world(underground=False);local = capped.c['KUR'];local.exists = True
        capped.s['164'].owner = capped.s['164'].controller = 'KUR'
        capped.s['164'].infrastructure = capped.infrastructure_cap
        before = copy.deepcopy((capped.c, capped.s));capped.run(first(body, 'complete_effect'), local)
        self.assertEqual(before, (capped.c, capped.s))


if __name__ == '__main__':
    unittest.main(verbosity=2)
