# IMPERIA CW — Cold War: shared RAF lifecycle, tree and cabinet integration checks.
"""Execute installed effects with the strict common-system transaction model.

This checks scripted state transitions and ownership, not HOI4 UI or netcode.
"""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools/colonial_affairs'))
from test_runtime import Model, Scope, D, parse, first

P = 'COLDWAR_GER_1970'
PROGRAMMES = json.loads((ROOT/'tools/colonial_affairs/raf_programmes.json').read_text())


def script(path):return parse((ROOT/path).read_text(encoding='utf-8'))


def walk(rows):
    for key, op, value in rows:
        yield key, op, value
        if isinstance(value, list):yield from walk(value)


class SecurityContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = Model()
        cls.native = script('common/scripted_effects/'+P+'_effects.txt')
        cls.windows = script('common/scripted_effects/'+P+'_windows_effects.txt')
        cls.template.effects.update((k,v) for k,o,v in cls.windows if k.startswith(P+'_sec_'))
        cls.template.effects.update((k,v) for k,o,v in cls.native if k==P+'_terror_tick')
        cls.template.triggers.update((k,v) for k,o,v in script('common/scripted_triggers/'+P+'_windows_triggers.txt') if k.startswith(P+'_sec_'))

    def setUp(self):
        self.m = copy.deepcopy(self.template)
        self.g = self.m.c['GER'] = Scope('GER')
        self.m.root = self.g
        self.m.date = '1977.10.1'
        self.g.flags.update((P+'_initialized','cwsec_initialized','cwgg_initialized'))
        self.g.pp = D(300)
        self.g.vars.update(treasury=D(1),cwger_raf_gen=D(2),cwger_raf_cadre=D(20),
                           cwger_raf_milieu=D(40),cwger_security=D(50),cwger_rechtsstaat=D(55),
                           cwger_raf_prisoners=D(2),cwger_bka_level=D(3),cwsec_hunger=D(30),
                           cwsec_used=D(0),cwsec_slots=D(2),cwsec_haft=D(1))
        ni=self.m.s['17']=Scope('17','state')
        ni.owner=ni.controller=self.m.c['ENG']
        for state in ('41','42','1080','1251'):
            region=self.m.s[state]=Scope(state,'state')
            region.owner=region.controller=self.g;region.cores={'GER'}

    def run_effect(self,name):self.m.run(P+'_'+name,self.g)

    def active(self):return self.m.condition(self.m.triggers[P+'_raf_case_active'],self.g)

    def test_formation_and_closure_have_one_gate(self):
        for date,expected in [('1970.1.1',False),('1970.5.13',False),('1970.5.14',True)]:
            self.m.date=date
            self.assertEqual(self.active(),expected)
        self.g.flags.add(P+'_raf_dissolved');self.assertFalse(self.active())
        self.g.flags.remove(P+'_raf_dissolved')
        self.g.flags.add('COLDWAR_COL_raf_settlement');self.assertFalse(self.active())
        self.g.flags.remove('COLDWAR_COL_raf_settlement')
        self.g.vars['cwger_raf_gen']=D(4);self.assertFalse(self.active())

    def test_january_and_closed_case_do_not_tick_raf(self):
        # No US country avoids an unrelated divisions-in-state model dependency.
        del self.m.c['USA']
        for date,closed in [('1970.1.1',False),('1977.10.1',True)]:
            self.m.date=date
            if closed:self.g.flags.add(P+'_raf_dissolved')
            self.g.vars.update(cwsec_w1_ort=D(25),cwsec_plan_justice=D(45))
            self.run_effect('security_reconcile')
            baseline=tuple(self.g.vars[v] for v in ('cwger_raf_cadre','cwger_raf_milieu','cwsec_w1_ort','cwsec_plan_justice'))
            self.run_effect('terror_tick');self.run_effect('sec_tick')
            self.assertEqual(baseline,tuple(self.g.vars[v] for v in ('cwger_raf_cadre','cwger_raf_milieu','cwsec_w1_ort','cwsec_plan_justice')))

    def test_focus_receipts_migrate_without_replaying_rewards(self):
        for row in PROGRAMMES:self.g.focuses.add(P+'_'+row['focus'])
        original=copy.deepcopy(self.g.vars)
        self.run_effect('security_reconcile');self.run_effect('security_reconcile')
        for row in PROGRAMMES:self.assertIn(row['unlock'],self.g.flags)
        self.assertEqual(self.g.pp,300)
        for key,value in original.items():self.assertEqual(self.g.vars[key],value)

    def test_programmes_require_focus_and_share_payment_and_cooldown(self):
        for row in PROGRAMMES:
            with self.subTest(programme=row['id']):
                before=(self.g.pp,self.g.vars['treasury'])
                self.m.run('COLDWAR_COL_measure_'+row['id'],self.g)
                self.assertEqual(before,(self.g.pp,self.g.vars['treasury']))
                self.g.focuses.add(P+'_'+row['focus'])
                self.m.run('COLDWAR_COL_measure_'+row['id'],self.g)
                self.assertEqual((self.g.pp,self.g.vars['treasury']),(before[0]-D(row['pp']),before[1]-D(row['cash'])))
                paid=(self.g.pp,self.g.vars['treasury'])
                self.run_effect('sec_act_'+row['id'])
                self.assertEqual(paid,(self.g.pp,self.g.vars['treasury']))
                self.assertIn('COLDWAR_COL_measure_'+row['id']+'_cooldown',self.g.flags)

    def test_weekly_account_counts_programmes_once_independently_of_menu(self):
        for row in PROGRAMMES:self.g.flags.add('COLDWAR_COL_measure_'+row['id']+'_live')
        self.run_effect('security_weekly_budget')
        self.assertEqual(self.g.vars['cwsec_program_weekly_cost'],D('.008'))
        for ignored in range(3):
            self.m.run('COLDWAR_COL_domestic_budget',self.g)
            self.assertEqual(self.g.vars['COLDWAR_COL_domestic_weekly_cost'],D('.008'))
        self.g.flags.discard('COLDWAR_COL_measure_medical_live')
        self.m.run('COLDWAR_COL_domestic_budget',self.g)
        self.assertEqual(self.g.vars['COLDWAR_COL_domestic_weekly_cost'],D('.005'))

    def test_only_german_monthly_owns_aid_and_programme_ticks(self):
        sponsor=self.m.c['ALG']
        sponsor.flags.add('COLDWAR_COL_local_funding_live')
        sponsor.vars.update(COLDWAR_COL_local_funding_state=D(41),COLDWAR_COL_local_funding_power=self.g)
        region=self.m.s['41']=Scope('41','state');region.owner=region.controller=self.g;region.cores={'GER'}
        self.g.flags.update(('COLDWAR_COL_measure_coordination_live','COLDWAR_COL_measure_judicial_live'))
        self.g.vars['cwsec_w1_ort']=D(20)
        self.m.run('COLDWAR_COL_contacts_monthly',self.g)
        self.assertEqual((self.g.vars['cwger_raf_cadre'],self.g.vars['cwsec_w1_ort']),(20,20))
        self.run_effect('security_external_monthly')
        self.assertEqual((self.g.vars['cwger_raf_cadre'],self.g.vars['cwsec_w1_ort'],self.g.vars['cwger_raf_milieu']),(D('20.25'),21,D('39.75')))
        monthly=list(walk(first(self.native,P+'_monthly')))
        calls=[k for k,o,v in monthly]
        self.assertEqual(calls.count(P+'_security_external_monthly'),1)
        self.assertLess(calls.index(P+'_security_external_monthly'),calls.index(P+'_terror_tick'))
        self.assertLess(calls.index(P+'_terror_tick'),calls.index(P+'_sec_tick'))
        contacts=list(walk(self.m.effects['COLDWAR_COL_contacts_monthly']))
        self.assertNotIn(P+'_security_external_monthly',[k for k,o,v in contacts])

    def test_closure_cleans_commitments_plans_and_hostage_deadline(self):
        self.g.flags.update((P+'_raf_dissolved',P+'_hostage_ultimatum',P+'_hostage_crisis_active'))
        for row in PROGRAMMES:self.g.flags.update(('COLDWAR_COL_measure_'+row['id']+'_live','COLDWAR_COL_measure_'+row['id']+'_cooldown'))
        self.g.vars.update(cwsec_plan_justice=D(90),cwsec_ult_days=D(12),COLDWAR_COL_raf_aid=D(15))
        self.run_effect('security_reconcile');self.run_effect('security_external_monthly')
        self.m.run('COLDWAR_COL_domestic_budget',self.g)
        for row in PROGRAMMES:
            self.assertNotIn('COLDWAR_COL_measure_'+row['id']+'_live',self.g.flags)
            self.assertIn('COLDWAR_COL_measure_'+row['id']+'_cooldown',self.g.flags)
        for key in ('cwsec_plan_justice','cwsec_ult_days','COLDWAR_COL_raf_aid','COLDWAR_COL_domestic_weekly_cost'):self.assertEqual(self.g.vars[key],0)
        self.assertNotIn(P+'_hostage_ultimatum',self.g.flags)
        self.assertEqual(self.g.vars['cwger_raf_cadre'],20)

    def test_custody_cards_follow_releases_without_inventing_prisoners(self):
        for i in range(1,5):self.g.vars['cwsec_w'+str(i)+'_st']=D(2)
        self.run_effect('sec_reconcile_custody')
        self.assertEqual(sum(self.g.vars.get('cwsec_w'+str(i)+'_st')==2 for i in range(1,7)),2)
        self.assertEqual(self.g.vars['cwger_raf_prisoners'],2)
        self.assertEqual(self.g.vars['cwsec_w1_st'],5)
        self.g.vars['cwger_raf_prisoners']=D(8)
        self.run_effect('sec_reconcile_custody')
        self.assertEqual(self.g.vars['cwger_raf_prisoners'],8)
        self.assertEqual(self.g.vars['cwsec_w1_st'],5)

    def test_stale_manual_actions_cannot_spend_or_run_after_closure(self):
        self.g.flags.add(P+'_raf_dissolved')
        self.g.vars['cwsec_w1_st']=D(1)
        before=copy.deepcopy(self.g)
        for action in ('access_1','protect_justice','regime_normal','act_raster'):
            self.run_effect('sec_'+action)
        self.assertEqual(self.g.pp,before.pp)
        self.assertEqual(self.g.vars,before.vars)
        self.assertEqual(self.g.flags,before.flags)

    def test_stale_manual_actions_recheck_funds_cooldowns_and_doctrine(self):
        self.g.vars['cwsec_w1_st']=D(1)
        for action,cost,flag in [('access_1',35,'cwsec_access_cd'),('protect_justice',10,None),('regime_normal',25,'cwsec_regime_cd')]:
            self.g.pp=D(cost-1);before=copy.deepcopy(self.g)
            self.run_effect('sec_'+action)
            self.assertEqual((self.g.pp,self.g.vars,self.g.flags),(before.pp,before.vars,before.flags))
            if flag:
                self.g.pp=D(300);self.g.flags.add(flag);before=copy.deepcopy(self.g)
                self.run_effect('sec_'+action)
                self.assertEqual((self.g.pp,self.g.vars,self.g.flags),(before.pp,before.vars,before.flags))
                self.g.flags.remove(flag)
        self.g.pp=D(300)
        self.assertFalse(self.m.condition(self.m.triggers[P+'_sec_can_raster'],self.g))
        self.g.flags.add('cwsec_dragnet_doctrine')
        self.assertTrue(self.m.condition(self.m.triggers[P+'_sec_can_raster'],self.g))

    def test_focus_unlocks_and_rewards_refresh_same_native_case(self):
        tree=first(script('common/national_focus/'+P+'_focus.txt'),'focus_tree')
        focuses={first(v,'id'):v for k,o,v in tree if k=='focus'}
        for row in PROGRAMMES:
            body=list(walk(first(focuses[P+'_'+row['focus']],'completion_reward')))
            self.assertIn(('set_country_flag','=',row['unlock']),body)
            self.assertIn((P+'_sec_gui_refresh','=','yes'),body)
        requirements=[v for k,o,v in focuses[P+'_reconciliation_offer'] if k=='prerequisite']
        self.assertEqual(len(requirements),1)
        self.assertEqual({v for k,o,v in requirements[0] if k=='focus'},
                         {P+'_crown_witness',P+'_exit_programme',P+'_data_protection'})

    def test_daily_observer_refreshes_expiry_without_monthly_ticks_or_payments(self):
        callback=first(first(first(script('common/on_actions/'+P+'_security_contract.txt'),'on_actions'),'on_daily'),'effect')
        self.g.flags.add('COLDWAR_COL_measure_coordination_live')
        before=(self.g.pp,self.g.vars['treasury'],self.g.vars['cwger_raf_cadre'],self.g.vars['cwger_raf_milieu'])
        self.m.execute(callback,self.g,self.g,None)
        self.assertEqual(before,(self.g.pp,self.g.vars['treasury'],self.g.vars['cwger_raf_cadre'],self.g.vars['cwger_raf_milieu']))
        self.assertEqual(self.g.vars['cwsec_program_weekly_cost'],D('.003'))
        self.assertNotIn('cwgg_g_cwgg_sec_r_cadre',self.g.vars)
        self.g.flags.remove('COLDWAR_COL_measure_coordination_live')
        self.m.execute(callback,self.g,self.g,None)
        self.assertEqual(self.g.vars['cwsec_program_weekly_cost'],0)


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(SecurityContract))
    report=dict(passed=result.wasSuccessful(),tests=result.testsRun,errors=len(result.errors),failures=len(result.failures),engine_tested=False)
    Path(__file__).with_name('security_contract_tests.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
