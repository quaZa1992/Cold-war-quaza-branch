# IMPERIA COLD WAR — Emitted strategy, statement and legacy-consent regression cases.
from collections import defaultdict
from decimal import Decimal as D
from pathlib import Path
import hashlib
import json
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from usa_kissinger_implementation.test_triangular_china import ChinaModel, T, P


class StrategyModel(ChinaModel):
    def __init__(self):
        self.globals=defaultdict(D)
        super().__init__()
        self.countries['SOV']['vars']['gdp_total']=D(400)

    def value(self,value,scope):
        if str(value).startswith('global.') and str(value)!='global.num_days':
            return self.globals[str(value)[7:]]
        return super().value(value,scope)

    def signed_programme(self,slot,pid,protocol):
        self.globals.update({f'icwt_{slot}_programme':D(pid),f'icwt_{slot}_revision':D(4),
          f'icwt_{slot}_programme_revision':D(5),f'icwt_{slot}_{protocol}':D(1)})
        for tag in ('USA','SOV'):
            self.countries[tag]['flags'].add(f'icwt_member_{slot}')
            self.countries[tag]['vars'][f'icwt_programme_{pid}_receipt']=D(5)


class StrategyTests(unittest.TestCase):
    def test_linkage_requires_real_statement_consent_not_only_the_focus_badge(self):
        m=StrategyModel();us=m.countries['USA']
        us['focuses'].add(P+'signal_moscow');us['flags'].add(P+'done_signal_moscow')
        self.assertFalse(m.trigger(P+'ready_linkage'))
        us['flags'].add(T+'signal_signed')
        self.assertTrue(m.trigger(P+'ready_linkage'))
        us['flags'].remove(T+'signal_signed');us['flags'].add(T+'sov_signal_completed')
        self.assertTrue(m.trigger(P+'ready_linkage'))

    def test_pacific_priority_is_paid_once_and_requires_the_live_exchange(self):
        m=StrategyModel();us=m.countries['USA'];chi=m.countries['CHI']
        us['flags'].add(T+'exchange_signed');chi['flags'].add(T+'exchange_signed')
        us['vars'][T+'exchange_end']=m.day+D(1460)
        before=us['vars']['treasury']
        m.call(P+'complete_china_priority');m.call(P+'complete_china_priority')
        self.assertEqual(us['vars']['treasury'],before-D('.005'))
        self.assertIn(T+'priority_china',us['ideas'])
        m.call(P+'calculate_streams');funded=us['vars'][P+'weekly_expense']
        m.day=us['vars'][T+'exchange_end']
        m.call(P+'calculate_streams')
        self.assertNotIn(T+'priority_china',us['ideas'])
        self.assertEqual(funded-us['vars'][P+'weekly_expense'],D('.0004'))
        self.assertEqual(us['vars']['treasury'],before-D('.005'))

    def test_detente_priority_needs_both_actual_signatories_and_restores_without_payment(self):
        m=StrategyModel();us=m.countries['USA'];sov=m.countries['SOV']
        us['flags'].add(P+'done_soviet_exchange')
        m.call(P+'complete_soviet_priority')
        self.assertNotIn(T+'priority_moscow',us['ideas'])
        m.signed_programme(9,1,'investment')
        before=us['vars']['treasury'];m.call(P+'complete_soviet_priority')
        self.assertIn(T+'priority_moscow',us['ideas'])
        self.assertEqual(us['vars']['treasury'],before-D('.005'))
        sov['flags'].remove('icwt_member_9');m.call(T+'reconcile_priorities')
        self.assertNotIn(T+'priority_moscow',us['ideas'])
        sov['flags'].add('icwt_member_9');m.call(T+'reconcile_priorities')
        self.assertIn(T+'priority_moscow',us['ideas'])
        self.assertEqual(us['vars']['treasury'],before-D('.005'))

    def test_cancelled_soviet_statement_clears_both_pending_flags_without_reward(self):
        m=StrategyModel();m.signed_programme(8,2,'trade');us=m.countries['USA'];sov=m.countries['SOV']
        us['flags'].add(P+'done_wider_settlement');before=us['vars']['treasury']
        m.call(T+'sov_signal_offer')
        self.assertIn(T+'sov_signal_pending',sov['flags'])
        m.call(T+'sov_signal_end')
        for country in (us,sov):self.assertNotIn(T+'sov_signal_pending',country['flags'])
        m.call(T+'sov_signal_accept','SOV')
        self.assertNotIn(T+'sov_signal_spirit',us['ideas'])
        self.assertEqual(us['vars']['treasury'],before)

    def test_soviet_statement_reprices_at_acceptance_and_cannot_replay(self):
        m=StrategyModel();m.signed_programme(8,2,'trade');us=m.countries['USA'];sov=m.countries['SOV']
        us['flags'].add(P+'done_wider_settlement');m.call(T+'sov_signal_offer')
        us['vars']['gdp_total']=D(2000);before=us['vars']['treasury']
        m.call(T+'sov_signal_accept','SOV');m.call(T+'sov_signal_accept','SOV')
        self.assertEqual(us['vars']['treasury'],before-D('.004'))
        self.assertIn(T+'sov_signal_spirit',us['ideas'])
        for country in (us,sov):self.assertNotIn(T+'sov_signal_pending',country['flags'])
        self.assertEqual(sov['events'].count('COLDWAR_USA_TDSP.2'),1)

    def test_soviet_statement_failure_keeps_pending_and_leaves_cash_and_spirits_intact(self):
        m=StrategyModel();m.signed_programme(8,2,'trade');us=m.countries['USA'];sov=m.countries['SOV']
        us['flags'].add(P+'done_wider_settlement');m.call(T+'sov_signal_offer')
        us['vars']['treasury']=D('.001');m.call(T+'sov_signal_accept','SOV')
        self.assertEqual(us['vars']['treasury'],D('.001'))
        self.assertNotIn(T+'sov_signal_spirit',us['ideas'])
        for country in (us,sov):self.assertIn(T+'sov_signal_pending',country['flags'])
        self.assertNotIn('COLDWAR_USA_TDSP.2',sov['events'])

    def test_moscow_migration_removes_only_the_old_receipts_without_granting_consent(self):
        m=StrategyModel();us=m.countries['USA'];sov=m.countries['SOV']
        for country,side in ((us,'usa'),(sov,'partner')):
            country['flags'].update({P+'deal_moscow_signed',P+'deal_moscow_pending','icwt_member_9'})
            country['ideas'].add(P+'deal_moscow_'+side)
        before=[country['vars']['treasury'] for country in (us,sov)]
        m.call(T+'migrate_moscow');m.call(T+'migrate_moscow')
        for country,side in ((us,'usa'),(sov,'partner')):
            self.assertNotIn(P+'deal_moscow_'+side,country['ideas'])
            self.assertNotIn(P+'deal_moscow_signed',country['flags'])
            self.assertIn('icwt_member_9',country['flags'])
            self.assertNotIn('icwt_member_7',country['flags'])
        self.assertEqual([country['vars']['treasury'] for country in (us,sov)],before)


if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(StrategyTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    sources=[ROOT/'common/scripted_effects/COLDWAR_USA_kissinger.txt',ROOT/'common/scripted_triggers/COLDWAR_USA_kissinger.txt',ROOT/'common/scripted_triggers/ICW_superpower_treaties.txt',Path(__file__)]
    report=dict(project='IMPERIA COLD WAR',scope='Installed emitted-AST strategy and legacy consent tests; no engine or MP execution',status='PASS' if result.wasSuccessful() else 'FAIL',tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),source_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})
    (ROOT/'docs/design/usa_triangular_20261029/strategy_tests.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(not result.wasSuccessful())
