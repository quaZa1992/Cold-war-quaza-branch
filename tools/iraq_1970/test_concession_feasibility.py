# IMPERIA CW — Cold War: iraq 1970 — test concession feasibility.
"""Regression for review bug4: capacity must precede concession payment.

Runs the fresh pure decision/event generator in memory. It does not compile or
install game outputs. Native state ownership/capacity and treasury APIs are
bounded harness models, not an engine or multiplayer certificate.
"""
from copy import deepcopy
import unittest

from common import P, ROOT, first, values, walk, parse
from test_decisions_module import DecisionWorld


class ConcessionFeasibilityTest(unittest.TestCase):
    def proposal(self):
        w=DecisionWorld()
        w.c['IRQ'].var['treasury']=1
        offered=w.open('oil_concession_offer')
        w.choose(offered,'ENG')
        reply=w.response()
        self.assertEqual(reply[1],'ENG')
        option=next(v for v in values(w.events[reply[0]],'option')
                    if 'Accept the stated agreement' in w.loc.get(first(v,'name'),''))
        return w,reply,option

    def assert_refused_without_mutation(self,change):
        w,reply,option=self.proposal()
        change(w)
        irq=w.c['IRQ'];eng=w.c['ENG']
        before=(irq.var['treasury'],eng.var['treasury'],deepcopy(irq.flags),deepcopy(eng.flags))
        # Native option visibility rejects it. Deliberately bypass that UI
        # check as well: execution must independently reject the callback.
        self.assertFalse(w.tests(first(option,'trigger'),eng))
        w.choose(reply,'Accept the stated agreement')
        self.assertEqual((irq.var['treasury'],eng.var['treasury'],irq.flags,eng.flags),before)
        self.assertNotIn(P+'oil_concession_accepted',irq.flags)
        self.assertNotIn(P+'accepted_oil_concession_offer_ENG',irq.flags)
        self.assertNotIn(P+'oil_concession_partner',eng.flags)

    def test_basra_ownership_lost_after_offer_blocks_both_treasuries_and_receipts(self):
        self.assert_refused_without_mutation(lambda w:setattr(w.s['171'],'owner','PER'))

    def test_basra_control_lost_after_offer_blocks_both_treasuries_and_receipts(self):
        self.assert_refused_without_mutation(lambda w:setattr(w.s['171'],'controller','PER'))

    def test_basra_full_infrastructure_after_offer_blocks_payment(self):
        self.assert_refused_without_mutation(lambda w:setattr(w.s['171'],'infrastructure',6))

    def test_exact_cash_frozen_one_percent_fee_last_slot_and_duplicate_callback(self):
        w,reply,option=self.proposal();irq=w.c['IRQ'];eng=w.c['ENG']
        self.assertAlmostEqual(irq.var[P+'D_oil_concession_offer_ENG_invoice'],.1)
        irq.var.update(gdp_total=100,treasury=.1)
        w.s['171'].infrastructure=5
        self.assertTrue(w.tests(first(option,'trigger'),eng))
        self.assertFalse(w.research)
        w.choose(reply,'Accept the stated agreement')
        self.assertAlmostEqual(irq.var['treasury'],0)
        self.assertAlmostEqual(eng.var['treasury'],10.1)
        self.assertIn(P+'oil_concession_accepted',irq.flags)
        self.assertIn(P+'accepted_oil_concession_offer_ENG',irq.flags)
        self.assertIn(P+'oil_concession_partner',eng.flags)
        self.assertEqual(w.s['171'].infrastructure,5)
        self.assertFalse(w.research)
        after=(irq.var['treasury'],eng.var['treasury'],deepcopy(irq.flags),deepcopy(eng.flags))
        self.assertFalse(w.tests(first(option,'trigger'),eng))
        w.choose(reply,'Accept the stated agreement')
        self.assertEqual((irq.var['treasury'],eng.var['treasury'],irq.flags,eng.flags),after)

    def test_blocked_capacity_can_recover_under_same_live_frozen_offer(self):
        w,reply,option=self.proposal();irq=w.c['IRQ'];eng=w.c['ENG']
        w.s['171'].infrastructure=6
        w.choose(reply,'Accept the stated agreement')
        self.assertEqual((irq.var['treasury'],eng.var['treasury']),(1,10))
        self.assertNotIn(P+'oil_concession_accepted',irq.flags)
        w.s['171'].infrastructure=5
        irq.var['gdp_total']=100
        self.assertTrue(w.tests(first(option,'trigger'),eng))
        w.choose(reply,'Accept the stated agreement')
        self.assertAlmostEqual(irq.var['treasury'],.9)
        self.assertAlmostEqual(eng.var['treasury'],10.1)
        self.assertIn(P+'oil_concession_accepted',irq.flags)

    def test_native_nonshared_capacity_syntax_in_visibility_and_execution(self):
        w,reply,option=self.proposal()
        visible=[v for k,o,v in walk(first(option,'trigger')) if k=='free_building_slots']
        executable=[v for k,o,v in walk([r for r in option if r[0] not in ['trigger','name','ai_chance']]) if k=='free_building_slots']
        self.assertTrue(visible)
        self.assertTrue(executable)
        for rows in visible+executable:
            self.assertEqual(first(rows,'building'),'infrastructure')
            self.assertIn(('size','>','0'),rows)
            self.assertIsNone(first(rows,'include_locked'))
        # The existing later delivery remains a separate guarded transaction.
        rewards=parse((ROOT/'common/scripted_effects/COLDWAR_IRQ_1970_rewards.txt').read_text(encoding='utf-8-sig'))
        later=first(rewards,P+'apply_oil_concession_delivery')
        self.assertIsNotNone(later)
        self.assertTrue(any(k=='free_building_slots' and first(v,'building')=='infrastructure' for k,o,v in walk(later)))
        self.assertTrue(any(k=='is_owned_and_controlled_by' and v=='IRQ' for k,o,v in walk(later)))


if __name__=='__main__':
    unittest.main(verbosity=2)
