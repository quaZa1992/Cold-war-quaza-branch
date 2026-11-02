# IMPERIA COLD WAR — Shared German dossier access and transactions
"""Bounded script model: transactions, ownership, refresh, consent and lifecycle."""
import copy
import json
from pathlib import Path
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/colonial_affairs'))
from test_runtime import Model,Scope,D,parse,first
from script_ast import walk
P='COLDWAR_GER_1970';E=P+'_east';R=P+'_rv'


def load(rel):return parse((ROOT/rel).read_text(encoding='utf-8-sig'))


class Relations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template=Model()
        for rel,kind in [('common/scripted_effects/'+P+'_windows_effects.txt','effects'),
                         ('common/scripted_triggers/'+P+'_windows_triggers.txt','triggers'),
                         ('common/scripted_triggers/'+P+'_sandbox.txt','triggers'),
                         ('common/scripted_effects/COLDWAR_DDR_1970_relations.txt','effects'),
                         ('common/scripted_triggers/COLDWAR_DDR_1970_relations.txt','triggers')]:
            getattr(cls.template,kind).update((k,v) for k,o,v in load(rel))
        political=load('common/scripted_triggers/01_political_triggers.txt')
        cls.template.triggers['emerging_communist_state_are_in_power']=first(political,'emerging_communist_state_are_in_power')
        native=load('common/scripted_triggers/COLDWAR_DDR_1970_scripted_triggers.txt')
        cls.template.triggers['COLDWAR_DDR_sed_governs']=first(native,'COLDWAR_DDR_sed_governs')
        cls.template.triggers['COLDWAR_DDR_ladder_border_active']=first(native,'COLDWAR_DDR_ladder_border_active')

    def setUp(self):
        self.m=copy.deepcopy(self.template)
        self.w=self.m.c['GER']=Scope('GER');self.d=self.m.c['DDR']=Scope('DDR')
        self.m.root=self.d;self.m.date='1973.1.1'
        self.w.flags.update((P+'_initialized','cwgg_initialized'))
        self.d.flags.update((P+'_ddr_initialized','COLDWAR_DDR_initialized'))
        self.w.pp=D(500);self.d.pp=D(500)
        self.w.vars.update(cwgg_init_ddr=D(6),cwgg_init_brd=D(6),cwgg_klima=D(20),cwgg_stufe=D(1),
                           cwgg_druck=D(10),cwgg_dhebel_transit=D(2),cwgg_dhebel_grenze=D(1),
                           cwgg_dhebel_zwang=D(1),cwger_ostpolitik=D(50))
        self.d.vars.update(cwddr_hard_currency=D(50),cwddr_exit_pressure=D(40),cwddr_sed_control=D(70),
                           cwddr_opposition=D(30),Granted_Recognition=D(19),
                           COLDWAR_DDR_course=D('-.25'),ruling_party=D(4))

    def run_action(self,key):self.m.run(E+'_act_'+key,self.d)

    def test_gui_and_native_pay_same_cost_once_and_share_lock(self):
        self.d.pp=D(25)
        self.run_action('raise_exchange')
        self.assertEqual((self.d.pp,self.w.pp,self.w.vars['cwgg_init_ddr']),(0,500,4))
        self.assertEqual((self.d.vars['cwddr_hard_currency'],self.d.vars['cwddr_exit_pressure']),(47,41))
        self.assertEqual(self.w.vars['cwgg_klima'],14)
        self.assertNotIn('cwgg_klima',self.d.vars)
        self.d.pp=D(25);before=self.d.vars['cwddr_hard_currency']
        # Simulate the engine's native 25-PP debit on a stale queued decision.
        self.d.pp-=25;self.m.run(E+'_native_raise_exchange',self.d)
        self.assertEqual(self.d.pp,25);self.assertEqual(self.d.vars['cwddr_hard_currency'],before)
        self.d.flags.remove('cwgg_east_cd_raise_exchange')
        self.d.pp-=25;self.m.run(E+'_native_raise_exchange',self.d)
        self.assertEqual(self.d.pp,25);self.assertEqual(self.w.vars['cwgg_init_ddr'],4)
        self.d.flags.remove('cwgg_balance_offensive_cd')
        self.d.pp-=25;self.m.run(E+'_native_raise_exchange',self.d)
        self.assertEqual(self.d.pp,0);self.assertEqual(self.w.vars['cwgg_init_ddr'],2)

    def test_no_funds_no_initiative_and_closed_country_cannot_pay(self):
        for change in ('money','initiative','unity','missing_ger'):
            with self.subTest(change=change):
                self.setUp()
                if change=='money':self.d.pp=D(24)
                if change=='initiative':self.w.vars['cwgg_init_ddr']=D(1)
                if change=='unity':self.m.g.flags.add(P+'_unity_achieved')
                if change=='missing_ger':del self.m.c['GER']
                before=(self.d.pp,copy.deepcopy(self.d.vars),copy.deepcopy(self.w.vars))
                self.run_action('raise_exchange')
                self.assertEqual(before,(self.d.pp,self.d.vars,self.w.vars))

    def test_native_exact_price_unity_request_preserves_bonn_consent(self):
        self.w.focuses.add(P+'_european_peace_order')
        self.w.vars.update(cwgg_klima=D(80),cwgg_stufe=D(0),cwgg_detente_m=D(36))
        for i in (3,5,6,7):self.w.vars['cwgg_vertrag_'+str(i)]=D(1)
        self.d.pp=D(100)
        self.assertTrue(self.m.condition(self.m.triggers[E+'_can_propose_unity'],self.d))
        self.d.pp-=100;self.m.run(E+'_native_propose_unity',self.d)
        self.assertEqual(self.d.pp,0)
        self.assertEqual(self.w.vars['cwgg_u_phase'],1)
        self.assertEqual(self.w.vars['cwgg_init_ddr'],3)
        self.assertEqual(self.m.events[-1][:2],('COLDWAR_GGU.2','GER'))
        self.assertNotIn('cwgg_u_rat_ddr',self.w.flags)

    def test_domestic_policy_has_native_tradeoff_and_one_time_receipt(self):
        self.run_action('intershop')
        self.assertEqual((self.d.pp,self.d.vars['cwddr_hard_currency'],self.d.vars['cwddr_opposition']),(460,46,31))
        self.assertEqual(self.d.vars['cwddr_west_media'],2)
        self.run_action('reform_course');value=self.d.vars['cwddr_exit_pressure'];paid=self.d.pp
        self.run_action('reform_course')
        self.assertEqual((self.d.pp,self.d.vars['cwddr_exit_pressure']),(paid,value))
        self.assertIn('cwgg_east_done_reform_course',self.d.flags)

    def test_sed_specific_actions_close_after_party_change(self):
        self.d.vars['ruling_party']=D(1)
        before=self.d.pp
        for key in ('border_regime','stasi_sweep','tighten_border','hva_offensive','reform_course'):
            self.run_action(key)
        self.assertEqual(self.d.pp,before)
        self.assertEqual(self.w.vars['cwgg_init_ddr'],6)

    def test_crisis_selection_locks_both_paths_and_charges_only_at_resolution(self):
        self.w.vars['cwgg_krise_typ']=D(1)
        self.run_action('answer_3')
        self.assertEqual(self.w.vars['cwgg_ddr_wahl'],3)
        self.assertEqual(self.w.vars['cwgg_init_ddr'],6)
        self.run_action('answer_1');self.assertEqual(self.w.vars['cwgg_ddr_wahl'],3)
        self.m.run(R+'_ddr_answer',self.w)
        self.assertEqual((self.w.vars['cwgg_a'],self.w.vars['cwgg_init_ddr'],self.w.vars['cwgg_ddr_wahl']),(3,5,0))
        self.assertFalse(self.m.condition(self.m.triggers[E+'_can_crisis_menu'],self.d))

    def test_moscow_choice_requires_existing_partner_without_trust_score(self):
        self.w.vars['cwgg_krise_typ']=D(1)
        self.m.c.pop('SOV',None)
        self.run_action('answer_4');self.assertNotIn('cwgg_ddr_wahl',self.w.vars)
        self.m.c['SOV']=Scope('SOV')
        self.run_action('answer_4');self.assertEqual(self.w.vars['cwgg_ddr_wahl'],4)
        self.assertFalse(any('trust' in key or 'moscow_backing' in key for key in self.d.vars))

    def test_unity_chapter_review_shares_native_cooldown_without_accepting(self):
        self.w.vars.update(cwgg_u_phase=D(2),cwgg_u_cur=D(3))
        self.run_action('unity_review')
        self.assertEqual(self.m.events[-1][:2],('COLDWAR_GGU.33','DDR'))
        self.assertNotIn('cwgg_u_dpos',self.w.vars)
        count=len(self.m.events)
        self.m.run(E+'_native_unity_position',self.d)
        self.assertEqual(len(self.m.events),count)
        self.w.vars['cwgg_u_phase']=D(4)
        self.assertFalse(self.m.condition(self.m.triggers[E+'_can_unity_review'],self.d))

    def test_refresh_changes_only_local_presentation_and_leaves_borders_as_snapshot(self):
        self.d.flags.add('cwgg_east_open');self.w.flags.add('cwgg_open')
        self.w.vars.update(cwgg_aufm_brd_div=D(17),cwgg_aufm_ddr_div=D(9))
        before=copy.deepcopy(self.w.vars);own=copy.deepcopy(self.d.vars);pp=(self.w.pp,self.d.pp)
        self.m.run(R+'_sync_views',self.w)
        for key,value in before.items():self.assertEqual(self.w.vars[key],value)
        for key,value in own.items():self.assertEqual(self.d.vars[key],value)
        self.assertEqual((self.w.pp,self.d.pp),pp)
        for key in set(self.d.vars)-set(own):self.assertTrue(key.startswith(('cwgg_g_','cwgg_east_gui_')),key)
        self.assertGreater(self.d.vars['cwgg_east_gui_dirty'],0)
        self.assertGreater(self.w.vars['cwgg_rv_gui_dirty'],0)

    def test_closed_and_ai_views_do_not_calculate_presentation(self):
        for ai in (True,False):
            self.d.ai=ai
            self.m.run(E+'_gui_refresh',self.d)
            self.assertFalse(any(k.startswith('cwgg_g_') for k in self.d.vars))

    def test_human_ddr_can_act_and_refresh_with_ai_bonn(self):
        self.w.ai=True;self.d.flags.add('cwgg_east_open')
        self.run_action('raise_exchange')
        self.assertEqual(self.w.vars['cwgg_klima'],14)
        self.assertEqual(self.d.pp,475)
        self.assertGreater(self.d.vars['cwgg_east_gui_dirty'],0)
        self.assertNotIn('cwgg_rv_gui_dirty',self.w.vars)

    def test_confederation_keeps_both_states_and_bilateral_actions_playable(self):
        self.d.flags.add('cwgg_east_open');self.m.g.flags.add(P+'_confederation')
        self.m.run(E+'_gui_refresh',self.d)
        self.assertIn('cwgg_east_open',self.d.flags)
        self.assertTrue(self.m.condition(self.m.triggers[E+'_can_raise_exchange'],self.d))
        self.run_action('intershop');self.assertEqual(self.d.pp,460)

    def test_actual_ddr_course_is_independent_of_bilateral_climate(self):
        for course in ('-1','1'):
            self.d.vars['COLDWAR_DDR_course']=D(course)
            self.w.vars.update(cwgg_klima=D(0),cwgg_druck=D(0))
            self.m.run(R+'_climate',self.w)
            if course=='-1':low=self.w.vars['cwgg_basis']
            else:self.assertEqual(self.w.vars['cwgg_basis'],low)
        self.assertEqual(self.d.vars['COLDWAR_DDR_course'],1)

    def test_both_ddr_launchers_route_to_their_tabs(self):
        for key,tab in (('relations',1),('domestic',5)):
            self.m.run(E+'_open_'+key,self.d)
            self.assertIn('cwgg_east_open',self.d.flags)
            self.assertEqual(self.d.vars['cwgg_east_tab'],tab)
        gui=first(load('common/scripted_guis/COLDWAR_DDR_1970_relations.txt'),'scripted_gui')
        for kind,target in (('relations','relations'),('security','domestic')):
            node=first(gui,'cwgg_east_'+kind+'_launcher')
            self.assertEqual(first(node,'parent_window_token'),'politics_tab')
            effects=first(node,'effects')
            click=first(effects,'cwgg_east_'+kind+'_launcher_button_click')
            self.assertEqual(first(click,E+'_open_'+target),'yes')

    def test_missing_bonn_leaves_domestic_file_and_policies_accessible(self):
        del self.m.c['GER']
        self.m.run(E+'_open_domestic',self.d)
        self.assertIn('cwgg_east_open',self.d.flags)
        self.run_action('intershop')
        self.assertEqual((self.d.pp,self.d.vars['cwddr_hard_currency']),(460,46))
        self.assertFalse(self.m.condition(self.m.triggers[E+'_can_raise_exchange'],self.d))

    def test_no_new_simulation_hook_or_current_bonn_stance_reader(self):
        hooks=load('common/on_actions/COLDWAR_DDR_1970_relations.txt')
        keys=[k for k,o,v in walk(hooks)]
        self.assertNotIn('on_monthly_DDR',keys);self.assertNotIn('on_monthly',keys)
        for effect in (E+'_gui_refresh',R+'_sync_views'):
            names=[];visited=set()
            def trace(name):
                if name in visited:return
                visited.add(name)
                for key,op,value in walk(self.m.effects[name]):
                    names.append(key)
                    if key in self.m.effects:trace(key)
            trace(effect)
            self.assertNotIn(R+'_border_count',names)
            self.assertNotIn(R+'_tick',names)
        gui=(ROOT/'interface/COLDWAR_DDR_1970_relations.gui').read_text()
        loc=(ROOT/'localisation/english/COLDWAR_DDR_1970_relations_l_english.yml').read_text(encoding='utf-8-sig')
        dt=(ROOT/'common/scripted_localisation/COLDWAR_DDR_1970_relations.txt').read_text()
        self.assertNotIn('cwgg_haltung',gui+loc+dt)
        self.assertNotIn('global.cwgg_east_gui_dirty',gui)


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Relations))
    report=dict(passed=result.wasSuccessful(),tests=result.testsRun,errors=len(result.errors),failures=len(result.failures),engine_tested=False)
    Path(__file__).with_name('ddr_relations_tests.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
