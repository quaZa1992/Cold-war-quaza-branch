# IMPERIA CW — Cold War: greece 1970 — test quality.
"""Execute the emitted air-project transaction, not a mirrored implementation."""
import unittest
from validate import World, P

class QualityTests(unittest.TestCase):
    def world(self,money):
        w=World();w.countries['GRE']['variables'].update(gdp_total=100,treasury=money)
        w.call('complete_air_0');return w

    def builds(self,w):return sum(len(s['builds']) for s in w.states.values())

    def test_readiness_is_experience_not_repeated_pp(self):
        w=self.world(1);w.call('complete_air_0')
        self.assertEqual(w.countries['GRE']['xp'],25)
        self.assertEqual(w.countries['GRE']['pp'],0)

    def test_exact_funds_pay_for_one_radar_once(self):
        w=self.world(.25);w.call('complete_air_1');w.call('complete_air_1')
        self.assertAlmostEqual(w.countries['GRE']['variables']['treasury'],0)
        self.assertEqual(self.builds(w),1)
        self.assertIn(P+'air_1_granted',w.countries['GRE']['flags'])

    def test_insufficient_funds_retains_retry_without_partial_reward(self):
        w=self.world(.249);w.call('complete_air_1')
        self.assertEqual(self.builds(w),0)
        self.assertAlmostEqual(w.countries['GRE']['variables']['treasury'],.249)
        self.assertIn(P+'air_1_awaiting_funding',w.countries['GRE']['flags'])
        w.countries['GRE']['variables']['treasury']=.25;w.call('complete_air_1')
        self.assertEqual(self.builds(w),1)

    def test_no_eligible_state_never_charges(self):
        for reason in ('occupation','capacity'):
            w=self.world(1)
            for state in w.states.values():
                if reason=='occupation':state['controller']='TUR'
                else:state['slots']=False
            w.call('complete_air_1')
            self.assertEqual(self.builds(w),0)
            self.assertEqual(w.countries['GRE']['variables']['treasury'],1)
            self.assertNotIn(P+'air_1_granted',w.countries['GRE']['flags'])

    def test_retry_rechecks_control_and_capacity(self):
        w=self.world(0);w.call('complete_air_1');w.countries['GRE']['variables']['treasury']=1
        for state in w.states.values():state['slots']=False
        w.call('complete_air_1');self.assertEqual(self.builds(w),0)
        self.assertEqual(w.countries['GRE']['variables']['treasury'],1)
        w.states['139']['slots']=True;w.call('complete_air_1')
        self.assertEqual(self.builds(w),1)
        self.assertAlmostEqual(w.countries['GRE']['variables']['treasury'],.75)

    def test_native_history_fee_skip_cannot_grant_free_radar(self):
        w=self.world(1);w.countries['GRE']['flags'].add('MD_skip_treasury_cost')
        w.call('complete_air_1')
        self.assertEqual(self.builds(w),0)
        self.assertEqual(w.countries['GRE']['variables']['treasury'],1)
        w.countries['GRE']['flags'].remove('MD_skip_treasury_cost');w.call('complete_air_1')
        self.assertEqual(self.builds(w),1)
        self.assertAlmostEqual(w.countries['GRE']['variables']['treasury'],.75)

if __name__=='__main__':unittest.main(verbosity=2)
