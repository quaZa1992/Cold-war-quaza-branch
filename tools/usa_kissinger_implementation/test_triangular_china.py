# IMPERIA COLD WAR — Emitted-AST checks for paid Chinese bilateral programmes.
"""Run installed effects with explicit native semantics. This does not run HOI4."""
from decimal import Decimal as D
from pathlib import Path
import json
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from usa_kissinger_implementation.test_runtime import Model, children
from focus_prerequisite_ui import nodes,field

P='COLDWAR_USA_KS_'
T=P+'td_'


class ChinaModel(Model):
    def __init__(self):
        self.day=D(10000);self.source=None;self.recall_allowed=True;self.global_vars={}
        super().__init__()
        self.ids={tag:D(index+1) for index,tag in enumerate(self.countries)}
        for country in self.countries.values():
            country['attaches']=set();country['volunteers']={}
            country['vars']['political_power']=D(100);country['vars']['command_power']=D(100)
        for path in (ROOT/'common/scripted_triggers').glob('ICW_superpower*.txt'):
            self.triggers.update({n.key:n.children() for n in nodes(path.read_text(encoding='utf-8-sig'))})
        for path in (ROOT/'common/scripted_effects').glob('ICW_superpower*.txt'):
            self.effects.update({n.key:n.children() for n in nodes(path.read_text(encoding='utf-8-sig'))})
        self.countries['USA']['vars']['gdp_total']=D(1000)
        self.countries['CHI']['vars']['gdp_total']=D(100)
        self.countries['USA']['flags'].add(P+'deal_beijing_signed')
        self.countries['CHI']['flags'].add(P+'deal_beijing_signed')

    def target(self,name):
        if name=='FROM':return self.source
        if name.startswith('var:') and self.stack:
            value=self.value(name[4:],self.stack[-1])
            return next((self.countries[tag] for tag,ident in self.ids.items() if ident==value),None)
        return super().target(name)

    def value(self,value,scope):
        if str(value)=='global.num_days':return self.day
        if str(value).startswith('global.'):return self.global_vars.get(str(value)[7:],D(0))
        if str(value)=='id':return self.ids[scope['tag']]
        return super().value(value,scope)

    def cond(self,items,scope):
        push=not self.stack or self.stack[-1] is not scope
        if push:self.stack.append(scope)
        try:
            for n in items:
                if n.key=='has_attache_from':
                    target=self.target(n.value);tag=target['tag'] if target else n.value
                    ok=tag in scope['attaches']
                elif n.key=='has_volunteers_amount_from':
                    tag=field(n.children(),'tag');target=self.target(tag)
                    tag=target['tag'] if target else tag
                    count=next(x for x in n.children() if x.key=='count')
                    ok=self.cmp(D(scope['volunteers'].get(tag,0)),count.op,D(count.value))
                elif n.key=='has_game_rule':ok=self.recall_allowed and field(n.children(),'rule')=='allow_recall_intervention_forces'
                elif n.key in ('has_political_power','command_power'):
                    ok=self.cmp(self.value('political_power' if n.key=='has_political_power' else 'command_power',scope),n.op,D(n.value))
                else:ok=super().cond([n],scope)
                if not ok:return False
            return True
        finally:
            if push:self.stack.pop()

    def run(self,items,scope):
        # Native effects cannot enter an annexed country's named scope. This
        # matters for local cleanup by the surviving bilateral partner.
        if scope.get('tag') and not scope.get('alive',False):return
        ordinary=[]
        def flush():
            if ordinary:super(ChinaModel,self).run(ordinary[:],scope);ordinary.clear()
        for n in items:
            if n.key in ('clear_variable','recall_attache','recall_volunteers_from','add_command_power','news_event'):
                flush()
                if n.key=='clear_variable':scope['vars'].pop(n.value,None)
                elif n.key=='add_command_power':scope['vars']['command_power']+=self.value(n.value,scope)
                elif n.key=='news_event':scope['events'].append(field(n.children(),'id'))
                else:
                    target=self.target(n.value)
                    assert target is not None,('Missing native recall target',n.value)
                    if n.key=='recall_attache':target['attaches'].discard(scope['tag'])
                    else:target['volunteers'][scope['tag']]=0
            else:ordinary.append(n)
        flush()

    def authorise(self,key):
        focus={'exchange':'china_exchange','industry':'china_industry','security':'china_security','regional':'linkage','signal':'signal_moscow'}[key]
        self.countries['USA']['flags'].add(P+'done_'+focus)

    def sign(self,key):
        self.authorise(key);self.call(T+key+'_offer');self.call(T+key+'_review','CHI');self.call(T+key+'_accept','CHI')

    def recalc_streams(self,tag):
        self.countries[tag]['vars'][P+'weekly_income']=D(0)
        self.countries[tag]['vars'][P+'weekly_expense']=D(0)
        self.call(T+'streams',tag)

    def select_region(self,tag='IRQ'):
        source=(ROOT/'common/decisions/COLDWAR_USA_kissinger.txt').read_text(encoding='utf-8-sig')
        decision=next(n for cat in nodes(source) for n in cat.children() if n.key==T+'regional_select')
        self.root=self.countries['CHI'];self.source=self.countries[tag]
        self.run(children(decision.children(),'complete_effect'),self.root)
        assert not self.stack
        self.source=None

    def decision_available(self,key,tag='CHI'):
        source=(ROOT/'common/decisions/COLDWAR_USA_kissinger.txt').read_text(encoding='utf-8-sig')
        decision=next(n for cat in nodes(source) for n in cat.children() if n.key==T+key)
        self.root=self.countries[tag]
        result=self.cond(children(decision.children(),'available'),self.root)
        assert not self.stack
        return result


class ChinaContracts(unittest.TestCase):
    def setUp(self):self.m=ChinaModel()

    def test_no_effects_before_consent_and_repeat_accept_is_harmless(self):
        m=self.m;m.authorise('exchange');m.call(T+'exchange_offer')
        self.assertEqual(m.countries['USA']['vars']['treasury'],D(100))
        self.assertNotIn(T+'exchange_usa',m.countries['USA']['ideas'])
        m.call(T+'exchange_accept','CHI')
        self.assertNotIn(T+'exchange_usa',m.countries['USA']['ideas'])
        m.call(T+'exchange_review','CHI');m.call(T+'exchange_accept','CHI')
        self.assertEqual(m.countries['USA']['vars']['treasury'],D('99.997'))
        self.assertIn(T+'exchange_usa',m.countries['USA']['ideas'])
        self.assertIn(T+'exchange_china',m.countries['CHI']['ideas'])
        m.call(T+'exchange_accept','CHI');m.call(T+'reconcile')
        self.assertEqual(m.countries['USA']['vars']['treasury'],D('99.997'))

    def test_current_gdp_is_repriced_atomically_at_signature(self):
        m=self.m;m.authorise('exchange');m.call(T+'exchange_offer');m.call(T+'exchange_review','CHI')
        m.countries['USA']['vars']['gdp_total']=D(2000)
        m.countries['USA']['vars']['treasury']=D('.004')
        m.call(T+'exchange_accept','CHI')
        self.assertEqual(m.countries['USA']['vars']['treasury'],D('.004'))
        self.assertIn(T+'exchange_pending',m.countries['USA']['flags'])
        self.assertNotIn(T+'exchange_signed',m.countries['CHI']['flags'])
        m.countries['USA']['vars']['treasury']=D('.01');m.call(T+'exchange_accept','CHI')
        self.assertEqual(m.countries['USA']['vars']['treasury'],D('.004'))

    def test_accept_decision_disables_without_funding_and_restores_with_funding(self):
        m=self.m;m.authorise('exchange');m.call(T+'exchange_offer');m.call(T+'exchange_review','CHI')
        m.countries['USA']['vars']['treasury']=D('.002')
        self.assertFalse(m.decision_available('exchange_accept_decision'))
        m.call(T+'exchange_accept','CHI')
        self.assertEqual(m.countries['USA']['vars']['treasury'],D('.002'))
        self.assertNotIn(T+'exchange_signed',m.countries['USA']['flags'])
        m.countries['USA']['vars']['treasury']=D('.004')
        self.assertTrue(m.decision_available('exchange_accept_decision'))
        m.call(T+'exchange_accept','CHI')
        self.assertEqual(m.countries['USA']['vars']['treasury'],D('.001'))

    def test_joint_statement_accept_decision_uses_the_same_funding_guard(self):
        m=self.m;m.sign('exchange');m.countries['USA']['flags'].add(P+'done_china_priority');m.sign('industry')
        m.authorise('signal');m.call(T+'signal_offer')
        m.countries['USA']['vars']['treasury']=D('.001')
        self.assertFalse(m.decision_available('signal_accept_decision'))
        m.call(T+'signal_accept','CHI')
        self.assertEqual(m.countries['USA']['vars']['treasury'],D('.001'))
        self.assertNotIn(T+'signal_signed',m.countries['USA']['flags'])
        m.countries['USA']['vars']['treasury']=D('.003')
        self.assertTrue(m.decision_available('signal_accept_decision'))
        m.call(T+'signal_accept','CHI')
        self.assertEqual(m.countries['USA']['vars']['treasury'],D('.001'))

    def test_sanctions_pause_both_sides_and_restoration_does_not_restart_term(self):
        m=self.m;m.sign('exchange');deadline=m.countries['USA']['vars'][T+'exchange_end']
        m.day+=D(200);m.countries['USA']['arrays']['imp_fin_sanc_by_us']={'CHI'}
        m.call(T+'reconcile');m.recalc_streams('USA');m.recalc_streams('CHI')
        self.assertNotIn(T+'exchange_usa',m.countries['USA']['ideas'])
        self.assertNotIn(T+'exchange_china',m.countries['CHI']['ideas'])
        self.assertEqual(m.countries['CHI']['vars'][P+'weekly_expense'],0)
        m.countries['USA']['arrays']['imp_fin_sanc_by_us']=set();m.call(T+'reconcile')
        self.assertEqual(m.countries['USA']['vars'][T+'exchange_end'],deadline)
        self.assertEqual(m.countries['USA']['vars']['treasury'],D('99.997'))
        self.assertIn(T+'exchange_usa',m.countries['USA']['ideas'])

    def test_expiry_during_war_does_not_return_benefits_after_peace(self):
        m=self.m;m.sign('exchange');m.countries['USA']['wars'].add('CHI')
        m.day=D(11460);m.call(T+'exchange_expire');m.call(T+'reconcile')
        m.countries['USA']['wars'].clear();m.call(T+'reconcile')
        self.assertNotIn(T+'exchange_signed',m.countries['USA']['flags'])
        self.assertNotIn(T+'exchange_signed',m.countries['CHI']['flags'])
        self.assertNotIn(T+'exchange_usa',m.countries['USA']['ideas'])

    def test_missing_usa_is_cleaned_by_surviving_china_and_restores_without_payment(self):
        m=self.m;m.sign('exchange');m.countries['USA']['flags'].add(P+'done_china_priority');m.sign('industry')
        before=m.countries['USA']['vars']['treasury'];deadline=m.countries['USA']['vars'][T+'exchange_end']
        m.countries['USA']['alive']=False;m.day+=D(100)
        # Only China's provider runs, exactly as when USA is annexed. No test
        # call enters the dead USA scope to remove China's benefits for it.
        m.recalc_streams('CHI')
        self.assertNotIn(T+'exchange_china',m.countries['CHI']['ideas'])
        self.assertNotIn(T+'industry_china',m.countries['CHI']['ideas'])
        self.assertEqual(m.countries['CHI']['vars'][P+'weekly_income'],0)
        self.assertEqual(m.countries['CHI']['vars'][P+'weekly_expense'],0)
        self.assertIn(T+'exchange_signed',m.countries['CHI']['flags'])
        m.countries['USA']['alive']=True;m.recalc_streams('CHI')
        self.assertIn(T+'exchange_china',m.countries['CHI']['ideas'])
        self.assertIn(T+'industry_china',m.countries['CHI']['ideas'])
        self.assertEqual(m.countries['USA']['vars'][T+'exchange_end'],deadline)
        self.assertEqual(m.countries['USA']['vars']['treasury'],before)

    def test_cancellation_and_new_offer_require_fresh_review(self):
        m=self.m;m.authorise('exchange');m.call(T+'exchange_offer');m.call(T+'exchange_review','CHI')
        m.call(T+'exchange_end');m.countries['USA']['flags'].discard(T+'exchange_cooldown')
        m.call(T+'exchange_offer');m.call(T+'exchange_accept','CHI')
        self.assertNotIn(T+'exchange_signed',m.countries['USA']['flags'])
        m.call(T+'exchange_review','CHI');m.call(T+'exchange_accept','CHI')
        self.assertIn(T+'exchange_signed',m.countries['USA']['flags'])

    def test_industry_transfer_is_mirrored_and_parent_expiry_stops_it(self):
        m=self.m;m.sign('exchange');m.countries['USA']['flags'].add(P+'done_china_priority');m.sign('industry')
        m.recalc_streams('USA');m.recalc_streams('CHI')
        self.assertEqual(m.countries['USA']['vars'][P+'weekly_expense'],D('.0007'))
        self.assertEqual(m.countries['CHI']['vars'][P+'weekly_income'],D('.0005'))
        self.assertEqual(m.countries['CHI']['vars'][P+'weekly_expense'],D('.0002'))
        m.day=D(11460);m.recalc_streams('USA');m.recalc_streams('CHI')
        self.assertEqual(m.countries['USA']['vars'][P+'weekly_expense'],0)
        self.assertEqual(m.countries['CHI']['vars'][P+'weekly_income'],0)
        self.assertNotIn(T+'industry_china',m.countries['CHI']['ideas'])

    def test_preview_calls_do_not_change_treasury_or_membership(self):
        m=self.m
        before={tag:(dict(c['vars']),set(c['flags']),set(c['ideas'])) for tag,c in m.countries.items()}
        for key in ('exchange','industry','security','regional','signal'):m.call(T+key+'_preview')
        after={tag:(dict(c['vars']),set(c['flags']),set(c['ideas'])) for tag,c in m.countries.items()}
        self.assertEqual(before,after)

    def test_four_year_term_is_visible_in_both_native_previews(self):
        preview=children(self.m.effects[T+'exchange_preview'],'effect_tooltip')
        for tag,side in [('USA','usa'),('CHI','china')]:
            shown=children(children(preview,tag),'add_timed_idea')
            self.assertEqual(field(shown,'idea'),T+'exchange_'+side)
            self.assertEqual(field(shown,'days'),'1460')

    def test_regional_requires_both_consents_and_real_recall(self):
        m=self.m;m.authorise('regional');m.countries['IRQ']['attaches'].add('CHI');m.countries['IRQ']['volunteers']['CHI']=2
        m.call(T+'regional_offer');m.select_region();m.call(T+'regional_review','CHI');m.call(T+'regional_accept','CHI')
        self.assertNotIn(T+'regional_signed',m.countries['CHI']['flags'])
        m.call(T+'regional_approve');m.call(T+'regional_review','CHI');m.call(T+'regional_accept','CHI')
        self.assertIn(T+'regional_signed',m.countries['CHI']['flags'])
        self.assertNotIn('CHI',m.countries['IRQ']['attaches'])
        self.assertEqual(m.countries['IRQ']['volunteers']['CHI'],0)
        self.assertEqual(m.countries['CHI']['vars']['political_power'],D(50))
        self.assertEqual(m.countries['CHI']['vars']['command_power'],D(85))
        self.assertEqual(m.countries['USA']['vars']['treasury'],D('99.995'))

    def test_regional_forbidden_recall_leaves_assets_and_cash_intact(self):
        m=self.m;m.authorise('regional');m.countries['IRQ']['volunteers']['CHI']=2
        m.call(T+'regional_offer');m.select_region();m.call(T+'regional_approve');m.call(T+'regional_review','CHI')
        m.recall_allowed=False;m.call(T+'regional_accept','CHI')
        self.assertEqual(m.countries['IRQ']['volunteers']['CHI'],2)
        self.assertEqual(m.countries['USA']['vars']['treasury'],D(100))
        self.assertNotIn(T+'regional_signed',m.countries['CHI']['flags'])

    def test_shared_regional_spirit_survives_missing_soviet_peer_only_with_chinese_contract(self):
        m=self.m;m.authorise('regional');m.countries['IRQ']['attaches'].add('CHI')
        m.call(T+'regional_offer');m.select_region();m.call(T+'regional_approve');m.call(T+'regional_review','CHI');m.call(T+'regional_accept','CHI')
        self.assertTrue(m.trigger(T+'regional_active'))
        m.global_vars.update(icwt_10_programme=D(4),icwt_10_regional=D(3),icwt_10_revision=D(1),icwt_10_programme_revision=D(1),
            icwt_10_usa_target=m.ids['IRQ'],icwt_10_sov_target=m.ids['PER'])
        for tag in ('USA','SOV'):
            m.countries[tag]['flags'].add('icwt_member_10')
            m.countries[tag]['vars']['icwt_programme_4_receipt']=D(1)
        self.assertTrue(m.trigger('icwt_programme_4_active'))
        m.call('icwt_programmes_refresh');before=m.countries['USA']['vars']['treasury']
        m.countries['SOV']['alive']=False;m.call('icwt_programmes_refresh')
        self.assertFalse(m.trigger('icwt_programme_4_active'))
        self.assertIn('icwt_programme_4_usa',m.countries['USA']['ideas'])
        m.call(T+'regional_end','CHI')
        self.assertNotIn('icwt_programme_4_usa',m.countries['USA']['ideas'])
        m.countries['SOV']['alive']=True;m.call('icwt_programmes_refresh')
        self.assertIn('icwt_programme_4_usa',m.countries['USA']['ideas'])
        self.assertEqual(m.countries['USA']['vars']['treasury'],before)


if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ChinaContracts)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    report={'project':'IMPERIA COLD WAR','scope':'Installed emitted-AST contract tests, not native engine or multiplayer execution','tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'passed':result.wasSuccessful()}
    (ROOT/'docs/design/USA_TRIANGULAR_CHINA_TESTS.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
