# IMPERIA COLD WAR — Emitted-script regression tests for annual orders and controller changes.
import copy
import json
import hashlib
import sys
from pathlib import Path
import unittest
from catalogue import FAMILIES, IDS
from script_harness import Harness

P='COLDWAR_ORD_'


class OrderTests(unittest.TestCase):
    def setUp(self):self.h=Harness();self.sov=self.h.country('SOV');self.ukr=self.h.country('UKR')
    def val(self,key,tag='UKR'):return self.h.country(tag).values[P+key]
    def call(self,key,tag='UKR',root=None):self.h.call(P+key,tag,root)
    def review_proposals(self,tag='UKR'):
        self.sov.values[P+'review_target']=self.h.country(tag).id
        self.call('snapshot_proposals','SOV')
    def certify(self,key):
        self.ukr.flags.add(P+key+'_return_pending')
        self.sov.values.update({P+'return_target':self.ukr.id,P+'return_family':IDS[key],P+'return_serial':self.val(key+'_serial')})
        self.call('certify_'+key,root='SOV')

    def test_every_family_reserves_with_correct_fixed_window(self):
        for f in FAMILIES:
            with self.subTest(f=f.key):
                self.h=Harness();self.ukr=self.h.country('UKR')
                self.h.choose('SOV',f.key,2,3 if f.buildings else 1)
                self.assertEqual(self.val(f.key+'_state'),2)
                self.assertEqual(self.ukr.missions[P+'window_'+f.key],365)

    def test_direct_order_charges_once_and_cannot_be_overwritten(self):
        self.h.choose('SOV','mbt',300,fraction=.0005)
        self.assertEqual(self.val('mbt_state'),2)
        self.assertAlmostEqual(self.sov.values['treasury'],99.5)
        self.assertAlmostEqual(self.ukr.values['treasury'],100.5)
        self.h.choose('SOV','mbt',900,fraction=.002)
        self.assertEqual(self.val('mbt_quantity'),300)
        self.assertAlmostEqual(self.sov.values['treasury'],99.5)

    def test_proposal_reserves_without_payment_or_quota_clock(self):
        self.h.choose('UKR','mbt',400,fraction=.0005)
        self.assertEqual(self.val('mbt_state'),1)
        self.assertNotIn(P+'window_mbt',self.ukr.missions)
        self.assertEqual(self.sov.values['treasury'],100)
        self.h.choose('SOV','mbt',900)
        self.assertEqual(self.val('mbt_quantity'),400)
        self.h.advance(4)
        self.assertEqual(self.val('mbt_state'),1)
        self.review_proposals()
        self.call('approve_mbt',root='SOV')
        self.assertEqual(self.ukr.missions[P+'window_mbt'],365)
        self.assertAlmostEqual(self.sov.values['treasury'],99.5)
        self.call('approve_mbt',root='SOV')
        self.assertAlmostEqual(self.sov.values['treasury'],99.5)

    def test_proposal_lapses_without_failure(self):
        self.h.choose('UKR','mbt',300)
        self.h.advance(30)
        self.assertEqual(self.val('mbt_state'),0)
        self.assertNotIn(P+'shortfall',self.sov.ideas)
        self.assertEqual(self.h.globals['COLDWAR_UNI_members'],0)

    def test_insufficient_funds_never_partially_commits(self):
        self.sov.values['treasury']=0
        self.h.choose('SOV','mbt',300,fraction=.002)
        self.assertEqual(self.val('mbt_state'),0)
        self.assertFalse(self.ukr.missions)
        self.h.choose('UKR','mbt',300,fraction=.002)
        self.review_proposals()
        self.call('approve_mbt',root='SOV')
        self.assertEqual(self.val('mbt_state'),1)
        self.assertNotIn(P+'window_mbt',self.ukr.missions)

    def test_zero_assistance_remains_available_with_negative_soviet_treasury(self):
        self.sov.values['treasury']=-100
        self.h.choose('UKR','civilian',1,3)
        self.assertEqual(self.val('civilian_cost'),0)
        self.review_proposals()
        self.call('approve_civilian',root='SOV')
        self.assertEqual(self.val('civilian_state'),2)
        self.assertEqual(self.sov.values['treasury'],-100)

    def test_republic_cannot_submit_for_another_republic(self):
        self.h.choose('UKR','mbt',300,target='BLR')
        self.assertEqual(self.val('mbt_state','BLR'),0)

    def test_manual_returns_never_self_fulfil(self):
        self.h.choose('SOV','mbt',300)
        self.h.advance(3)
        self.assertEqual(self.val('mbt_state'),2)
        self.assertNotIn(P+'successful_mbt',self.sov.ideas)
        self.certify('mbt')
        self.assertEqual(self.val('mbt_state'),3)
        self.assertEqual(self.sov.ideas[P+'successful_mbt'],180)
        self.assertEqual(self.ukr.missions[P+'window_mbt'],362)

    def test_success_expires_after_180_without_releasing_annual_slot(self):
        self.h.choose('SOV','mbt',300);self.certify('mbt')
        self.h.advance(180)
        self.assertNotIn(P+'successful_mbt',self.sov.ideas)
        self.assertNotIn(P+'successful_mbt',self.ukr.ideas)
        self.assertEqual(self.val('mbt_state'),3)
        self.assertEqual(self.ukr.missions[P+'window_mbt'],185)

    def test_failure_and_cg_are_180_days(self):
        self.h.choose('SOV','mbt',300)
        self.h.advance(365)
        self.assertEqual(self.val('mbt_state'),0)
        self.assertEqual(self.sov.ideas[P+'unfulfilled_mbt'],180)
        self.assertEqual(self.sov.ideas[P+'shortfall'],180)
        self.h.advance(180)
        self.assertNotIn(P+'unfulfilled_mbt',self.sov.ideas)
        self.assertNotIn(P+'shortfall',self.sov.ideas)

    def test_ai_only_programme_never_awards_or_punishes(self):
        self.ukr.ai=True
        self.h.choose('SOV','mbt',300)
        self.assertEqual(self.val('mbt_state'),6)
        self.h.advance(365)
        self.assertEqual(self.val('mbt_state'),0)
        self.assertFalse(self.sov.ideas)
        self.assertNotIn('COLDWAR_UNI_year_won',self.h.global_flags)

    def test_ai_takeover_and_human_return_leave_neutral_reservation(self):
        self.h.choose('SOV','mbt',300,fraction=.0005)
        self.ukr.ai=True;self.call('daily')
        self.assertEqual(self.val('mbt_state'),5)
        self.ukr.ai=False;self.call('daily')
        self.h.choose('SOV','mbt',900,fraction=.002)
        self.assertEqual(self.val('mbt_quantity'),300)
        self.assertAlmostEqual(self.sov.values['treasury'],99.5)
        self.h.advance(365)
        self.assertFalse(self.sov.ideas)

    def test_timeout_rechecks_ai_without_waiting_for_daily_watcher(self):
        self.h.choose('SOV','mbt',300)
        self.ukr.ai=True
        self.call('close_mbt')
        self.assertFalse(self.sov.ideas)

    def test_building_scope_counts_recipient_not_soviet_assets(self):
        self.h.choose('SOV','civilian',1,3)
        state=next(s for s in self.h.states if s.owner is self.ukr)
        state.buildings['industrial_complex']+=1
        self.call('daily')
        self.assertEqual(self.val('civilian_state'),3)
        self.assertIn(P+'successful_civilian',self.sov.ideas)

    def test_cotton_accepts_civilian_processing(self):
        self.h.choose('SOV','cotton',1,3)
        state=next(s for s in self.h.states if s.owner is self.ukr)
        state.buildings['industrial_complex']=1
        self.call('daily')
        self.assertEqual(self.val('cotton_state'),3)

    def test_delivery_moves_actual_equipment_and_never_mints(self):
        self.h.choose('SOV','rifles',300,2)
        self.ukr.stock['infantry_weapons_type']=100
        self.call('deliver_rifles')
        self.assertEqual(self.val('rifles_delivered'),100)
        self.assertEqual(self.val('rifles_state'),2)
        self.ukr.stock['infantry_weapons_type']=200
        self.call('deliver_rifles')
        self.assertEqual(self.val('rifles_state'),3)
        self.assertEqual(self.sov.stock['infantry_weapons_type'],300)
        self.call('deliver_rifles')
        self.assertEqual(self.sov.stock['infantry_weapons_type'],300)

    def test_broad_counter_uses_opening_baseline_not_stock(self):
        self.ukr.values['total_equipment_produced_artillery']=500
        self.h.choose('SOV','artillery_class',100)
        self.ukr.stock['artillery_equipment']=1000
        self.call('daily');self.assertEqual(self.val('artillery_class_state'),2)
        self.ukr.values['total_equipment_produced_artillery']=600
        self.call('daily');self.assertEqual(self.val('artillery_class_state'),3)

    def test_overlapping_family_and_production_delivery_cannot_double_book(self):
        self.h.choose('SOV','artillery_class',300)
        self.h.choose('SOV','towed_artillery',300)
        self.assertEqual(self.val('towed_artillery_state'),0)
        self.h.choose('SOV','artillery_class',300,2)
        self.assertEqual(self.val('artillery_class_kind'),1)

    def test_independence_suspends_and_restores_only_remaining_reward(self):
        self.h.choose('SOV','mbt',300);self.certify('mbt');self.h.advance(20)
        balance=self.ukr.values['treasury'];self.ukr.subject=None;self.call('daily')
        self.assertNotIn(P+'successful_mbt',self.ukr.ideas)
        self.h.advance(10);self.ukr.subject='SOV';self.call('daily')
        self.assertEqual(self.ukr.ideas[P+'successful_mbt'],150)
        self.assertEqual(self.ukr.values['treasury'],balance)

    def test_consumer_goods_penalty_is_one_spirit_across_families(self):
        self.h.choose('SOV','mbt',300);self.h.choose('SOV','rifles',300)
        self.call('fail_mbt');self.call('fail_rifles')
        self.assertEqual(list(k for k in self.sov.ideas if k==P+'shortfall'),[P+'shortfall'])
        self.assertEqual(self.sov.ideas[P+'shortfall'],180)

    def test_empty_calendar_gives_no_collective_success(self):
        self.call('settle_calendar','SOV')
        self.assertNotIn('COLDWAR_UNI_last_won',self.h.global_flags)
        self.assertEqual(self.h.globals['COLDWAR_UNI_good_years_9'],0)

    def test_closed_human_result_survives_later_ai_control(self):
        self.h.choose('SOV','mbt',300);self.call('fail_mbt')
        self.ukr.ai=True;self.call('daily')
        self.assertEqual(self.val('mbt_state'),4)
        self.assertIn(P+'unfulfilled_mbt',self.sov.ideas)

    def test_shared_overlapping_artillery_targets_have_one_outcome_each(self):
        self.h.choose('SOV','artillery_class',100)
        self.ukr.values['total_equipment_produced_artillery']=100
        self.call('daily')
        self.assertIn(P+'successful_towed_artillery',self.sov.ideas)
        self.assertIn(P+'successful_sp_artillery',self.sov.ideas)
        self.h.choose('SOV','towed_artillery',100,target='BLR')
        self.call('fail_towed_artillery','BLR')
        self.assertNotIn(P+'successful_towed_artillery',self.sov.ideas)
        self.assertIn(P+'unfulfilled_towed_artillery',self.sov.ideas)
        self.assertIn(P+'successful_sp_artillery',self.sov.ideas)

    def test_shared_policy_restores_without_regrant_or_payment(self):
        self.ukr.flags.add('COLDWAR_UNI_counter_unlocked')
        self.call('sync_policies');self.assertIn(P+'policy_counter_plan',self.ukr.ideas)
        balance=self.ukr.values['treasury']
        self.ukr.subject=None;self.call('sync_policies')
        self.assertNotIn(P+'policy_counter_plan',self.ukr.ideas)
        self.ukr.subject='SOV';self.call('sync_policies')
        self.assertIn(P+'policy_counter_plan',self.ukr.ideas)
        self.assertEqual(self.ukr.values['treasury'],balance)

    def test_save_rehost_preserves_reservation_baseline_and_payment(self):
        self.call('bootstrap','SOV')
        self.h.choose('SOV','mbt',300,fraction=.0005)
        self.h.advance(20)
        clone=copy.deepcopy(self.h);self.h=clone;self.sov=clone.country('SOV');self.ukr=clone.country('UKR')
        self.call('bootstrap','SOV')
        self.h.choose('SOV','mbt',900,fraction=.002)
        self.assertEqual(self.val('mbt_quantity'),300)
        self.assertEqual(self.ukr.missions[P+'window_mbt'],345)
        self.assertAlmostEqual(self.sov.values['treasury'],99.5)

    def test_collective_summary_uses_closed_human_results_and_180_day_bonus(self):
        self.h.globals['COLDWAR_SOV_plan']=9
        self.h.choose('SOV','mbt',300);self.certify('mbt')
        self.h.country('BLR').ai=True
        self.h.choose('SOV','rifles',300,target='BLR')
        self.call('settle_calendar','SOV')
        self.assertEqual(self.h.globals['COLDWAR_UNI_last_members'],1)
        self.assertEqual(self.h.globals['COLDWAR_UNI_good_years_9'],1)
        self.assertEqual(self.sov.ideas['COLDWAR_UNI_plan_fulfilled'],180)

    def test_proposal_receipt_retains_original_window_if_native_timer_is_missing(self):
        self.h.choose('UKR','mbt',300)
        self.ukr.missions.pop(P+'proposal_mbt')
        self.call('daily')
        self.assertEqual(self.val('mbt_state'),1)
        self.h.advance(30)
        self.assertEqual(self.val('mbt_state'),0)

    def test_stale_soviet_review_cannot_accept_or_reject_a_replacement_proposal(self):
        self.h.choose('UKR','mbt',300,fraction=.0005);self.review_proposals()
        old_serial=self.val('mbt_serial')
        self.call('reject_mbt',root='UKR')
        self.h.choose('UKR','mbt',900,fraction=.002)
        self.assertNotEqual(self.val('mbt_serial'),old_serial)
        self.call('approve_mbt',root='SOV');self.assertEqual(self.val('mbt_state'),1)
        self.call('reject_mbt',root='SOV');self.assertEqual(self.val('mbt_state'),1)
        self.assertEqual(self.sov.values['treasury'],100)
        self.review_proposals();self.call('approve_mbt',root='SOV')
        self.assertEqual(self.val('mbt_state'),2)
        self.assertEqual(self.val('mbt_quantity'),900)
        self.assertEqual(self.sov.values['treasury'],98)

    def test_stale_production_review_cannot_certify_the_next_annual_order(self):
        self.h.choose('SOV','mbt',300)
        old_serial=self.val('mbt_serial')
        self.sov.values.update({P+'return_target':self.ukr.id,P+'return_family':IDS['mbt'],P+'return_serial':old_serial})
        self.call('close_mbt')
        self.h.choose('SOV','mbt',900)
        self.ukr.flags.add(P+'mbt_return_pending')
        self.call('certify_mbt',root='SOV')
        self.assertEqual(self.val('mbt_state'),2)
        self.certify('mbt');self.assertEqual(self.val('mbt_state'),3)

    def test_later_success_refreshes_shared_clock_without_stacking(self):
        self.h.choose('SOV','mbt',300);self.certify('mbt');self.h.advance(10)
        self.h.choose('SOV','mbt',300,target='BLR')
        other=self.h.country('BLR');other.flags.add(P+'mbt_return_pending')
        self.sov.values.update({P+'return_target':other.id,P+'return_family':IDS['mbt'],P+'return_serial':other.values[P+'mbt_serial']})
        self.call('certify_mbt','BLR',root='SOV')
        self.assertEqual(self.sov.missions[P+'success_clock_mbt'],180)
        self.assertEqual(self.sov.ideas[P+'successful_mbt'],180)


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(OrderTests))
    here=Path(__file__).resolve().parent
    manifest=json.loads((here/'manifest.json').read_text(encoding='utf-8'))
    report={'project':'IMPERIA COLD WAR','tests_run':result.testsRun,'failures':[{'test':str(t),'detail':detail} for t,detail in result.failures],'errors':[{'test':str(t),'detail':detail} for t,detail in result.errors],'success':result.wasSuccessful(),'scope':'Regression interpreter executes the actual emitted script subset. Save/rehost test copies that model, not a native save. Native and multiplayer evidence is separate.','source_hashes':manifest['outputs']}
    (here/'TEST_REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    sys.exit(not result.wasSuccessful())
