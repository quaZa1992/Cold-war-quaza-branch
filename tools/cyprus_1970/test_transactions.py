# IMPERIA CW — Cold War: cyprus 1970 — test transactions.
"""Focused transaction tests against emitted ASTs, not an HOI4 engine emulator.

Models only the documented native commands reached by these scenarios. Unknown
commands fail loudly. Engine parsing, event ordering and MP sync require HOI4.
"""
import json
import unittest
from collections import defaultdict
from validate import ROOT, HERE, P, parse, first


class Transactions:
    def __init__(self):
        self.effects=dict((k,v) for k,op,v in parse((ROOT/'common/scripted_effects/COLDWAR_CYP_1970_effects.txt').read_text()))
        ast=parse((ROOT/'common/decisions/COLDWAR_CYP_1970_decisions.txt').read_text())
        self.decisions=dict((k,v) for category,op,children in ast for k,op,v in children)
        self.data=defaultdict(lambda:{'v':defaultdict(float),'f':set(),'ideas':set(),'dm':set(),'ai':False})
        self.temp={};self.notices=[]
        self.data['CYP']['v'].update(gdp_total=1,treasury=1,debt=0,ruling_party=1)

    def ready(self,key):
        design=json.loads((ROOT/'docs/cyprus_1970_design/coldwar_cyprus_1970_design.json').read_text(encoding='utf-8'))
        nodes={n['id']:n for n in design['focuses']}
        def parent(node):
            for group in node['prerequisite_groups']:
                for identifier in group:
                    self.data['CYP']['f'].add(P+'applied_'+identifier[len(P):]);parent(nodes[identifier])
        parent(nodes[P+key])

    def num(self,x,s):
        try:return float(x)
        except ValueError:
            if '.' in x:s,x=x.split('.',1)
            return self.temp.get(x,self.data[s]['v'][x])

    def test(self,tree,s='CYP'):
        return all(self.term(k,op,v,s) for k,op,v in tree)

    def term(self,k,op,v,s):
        if k in self.data or k in ('CYP','GRE','TUR','ENG','YUG','SOV','145','146'):return self.test(v,k)
        if k in ('AND','OR','NOT','hidden_trigger'):
            checks=[self.term(a,b,c,s) for a,b,c in v]
            return all(checks) if k in ('AND','hidden_trigger') else any(checks) if k=='OR' else not any(checks)
        if k in ('IMP_is_1970_scenario','always','exists'):return v=='yes'
        if k=='original_tag':return s==v
        if k=='country_exists':return True
        if k=='is_ai':return self.data[s]['ai']==(v=='yes')
        if k=='has_country_flag':return v in self.data[s]['f']
        if k=='has_variable':return v in self.data[s]['v']
        if k=='has_completed_focus':return True # Explicit fixture: all parent badges exist.
        if k in ('owns_state','controls_state'):return s=='CYP' and v in ('145','146')
        if k in ('is_owned_by','is_controlled_by'):return v=='CYP' and s in ('145','146')
        if k=='has_war':return v=='no'
        if k=='has_dynamic_modifier':return first(v,'modifier') in self.data[s]['dm']
        if k=='check_variable':
            if first(v,'var'):
                left=self.num(first(v,'var'),s);right=self.num(first(v,'value'),s)
                return left>=right if first(v,'compare')=='greater_than_or_equals' else left==right
            name,cmp,value=v[0];left=self.num(name,s);right=self.num(value,s)
            return left==right if cmp=='=' else left>right if cmp=='>' else left<right
        raise AssertionError('Unmodelled trigger '+k)

    def run(self,tree,s='CYP'):
        matched=False
        for k,op,v in tree:
            d=self.data[s]
            if k=='if':
                matched=self.test(first(v,'limit',[]),s)
                if matched:self.run([x for x in v if x[0]!='limit'],s)
            elif k=='else':
                if not matched:self.run(v,s)
            elif k in self.effects:self.run(self.effects[k],s)
            elif k in ('CYP','GRE','TUR','ENG','YUG','SOV','145','146'):self.run(v,k)
            elif k in ('set_country_flag','clr_country_flag'):
                name=first(v,'flag') if isinstance(v,list) else v
                (d['f'].add if k=='set_country_flag' else d['f'].discard)(name)
            elif k in ('set_variable','set_temp_variable','add_to_variable','multiply_variable','multiply_temp_variable','subtract_from_temp_variable'):
                name,_,value=v[0];target=self.temp if 'temp_variable' in k else d['v'];value=self.num(value,s)
                if k.startswith('set_'):target[name]=value
                elif k.startswith('add_'):target[name]+=value
                elif k.startswith('multiply_'):target[name]*=value
                else:target[name]-=value
            elif k=='clamp_variable':
                name=first(v,'var');d['v'][name]=min(float(first(v,'max')),max(float(first(v,'min')),d['v'][name]))
            elif k=='modify_treasury_effect':d['v']['treasury']+=self.temp['treasury_change']
            elif k=='modify_debt_effect':d['v']['debt']+=self.temp['debt_change']
            elif k in ('add_ideas','remove_ideas'):(d['ideas'].add if k=='add_ideas' else d['ideas'].discard)(v)
            elif k in ('add_dynamic_modifier','remove_dynamic_modifier'):(d['dm'].add if k=='add_dynamic_modifier' else d['dm'].discard)(first(v,'modifier'))
            elif k=='force_update_dynamic_modifier':pass # No engine refresh is claimed.
            elif k=='country_event':self.notices.append(first(v,'id'))
            else:raise AssertionError('Unmodelled effect '+k)

    def call(self,key):self.run(self.effects[P+key])
    def decision(self,key,s):self.run(first(self.decisions[P+key],'complete_effect'),s)


class TransactionTests(unittest.TestCase):
    def test_incumbent_administration_has_no_empty_mandate_gate(self):
        tree=parse((ROOT/'common/national_focus/COLDWAR_CYP_1970_focus.txt').read_text(encoding='utf-8'))
        focus_tree=first(tree,'focus_tree')
        focus=next(v for k,op,v in focus_tree if k=='focus' and first(v,'id')==P+'p1_organisation')
        self.assertFalse(any(k=='prerequisite' for k,op,v in focus))
        self.assertAlmostEqual(float(first(focus,'cost'))*7,35)

    def test_incumbent_administration_exact_funding_and_once_only(self):
        r=self.r;r.data['CYP']['v'].update(gdp_total=100,treasury=.25)
        r.call('complete_p1_organisation');r.call('complete_p1_organisation')
        self.assertAlmostEqual(r.data['CYP']['v']['treasury'],0)
        self.assertAlmostEqual(r.data['CYP']['v'][P+'p1_stability_factor'],.03)
        self.assertAlmostEqual(r.data['CYP']['v'][P+'p1_bureaucracy_cost_multiplier_modifier'],-.05)

    def test_incumbent_administration_insufficient_funding_is_atomic(self):
        r=self.r;r.data['CYP']['v'].update(gdp_total=100,treasury=.249)
        r.call('complete_p1_organisation')
        self.assertAlmostEqual(r.data['CYP']['v']['treasury'],.249)
        self.assertEqual(r.data['CYP']['v'][P+'p1_stability_factor'],0)
        self.assertEqual(r.data['CYP']['v'][P+'p1_bureaucracy_cost_multiplier_modifier'],0)

    def test_incumbent_administration_cannot_use_native_history_fee_skip(self):
        r=self.r;r.data['CYP']['v'].update(gdp_total=100,treasury=1)
        r.data['CYP']['f'].add('MD_skip_treasury_cost')
        r.call('complete_p1_organisation')
        self.assertEqual(r.data['CYP']['v']['treasury'],1)
        self.assertNotIn(P+'applied_p1_organisation',r.data['CYP']['f'])
        r.data['CYP']['f'].remove('MD_skip_treasury_cost');r.call('complete_p1_organisation')
        self.assertAlmostEqual(r.data['CYP']['v']['treasury'],.75)
        self.assertAlmostEqual(r.data['CYP']['v'][P+'p1_bureaucracy_cost_multiplier_modifier'],-.05)

    def setUp(self):self.r=Transactions()

    def test_insufficient_then_funded_project_pays_once(self):
        r=self.r;r.ready('development_budget');r.data['CYP']['v']['treasury']=0
        r.call('complete_development_budget')
        self.assertIn(P+'pending_completion_development_budget',r.data['CYP']['f'])
        self.assertNotIn(P+'development_budget_idea',r.data['CYP']['ideas'])
        r.data['CYP']['v']['treasury']=1
        r.call('complete_development_budget');r.call('complete_development_budget')
        self.assertAlmostEqual(r.data['CYP']['v']['treasury'],.99)
        self.assertIn(P+'development_budget_idea',r.data['CYP']['ideas'])

    def offer_loan(self):
        r=self.r;r.ready('p1_finance_a');r.data['CYP']['v'][P+'crisis_instance']=4;r.call('send_p1_finance_a')
        return r

    def test_duplicate_loan_acceptance_never_duplicates_cash_or_debt(self):
        r=self.offer_loan();r.data['YUG']['v']['treasury']=1
        r.decision('accept_YUG_p1_finance_a','YUG');r.decision('accept_YUG_p1_finance_a','YUG')
        self.assertAlmostEqual(r.data['YUG']['v']['treasury'],.98)
        self.assertAlmostEqual(r.data['CYP']['v']['treasury'],1.02)
        self.assertAlmostEqual(r.data['CYP']['v']['debt'],.02)

    def test_loan_unaffordable_or_ai_or_stale_cannot_pay(self):
        for reason in ('funds','ai','stale','wrong_actor'):
            with self.subTest(reason=reason):
                self.r=Transactions();r=self.offer_loan();r.data['YUG']['v']['treasury']=1
                if reason=='funds':r.data['YUG']['v']['treasury']=.001
                if reason=='ai':r.data['YUG']['ai']=True
                if reason=='stale':r.data['CYP']['v'][P+'crisis_instance']=5
                before=r.data['YUG']['v']['treasury']
                r.decision('accept_YUG_p1_finance_a','GRE' if reason=='wrong_actor' else 'YUG')
                self.assertEqual(r.data['YUG']['v']['treasury'],before)
                self.assertEqual(r.data['CYP']['v']['debt'],0)

    def test_renewal_freezes_original_principal(self):
        r=self.offer_loan();r.data['CYP']['v']['gdp_total']=10;r.call('send_p1_finance_a')
        self.assertAlmostEqual(r.data['CYP']['v'][P+'principal_p1_finance_a'],.02)

    def test_relief_never_reintroduces_an_earlier_penalty(self):
        r=self.r;r.call('relief_3');r.call('relief_1');r.call('relief_2')
        self.assertEqual(r.data['CYP']['v'][P+'relief_stage'],3)
        self.assertEqual(r.data['146']['dm'],set())
        self.assertNotIn(P+'admin_stage_1',r.data['CYP']['ideas'])

    def test_reconstruction_does_not_damage_an_intact_state(self):
        r=self.r;r.data['146']['dm'].add(P+'shattered_communities')
        # Run actual extras portion after grant's one-time flag and base payload.
        body=first(r.effects[P+'grant_reconstruction'],'if')
        state_effects=[x for x in body if x[0] in ('145','146')]
        r.run(state_effects)
        self.assertEqual(r.data['145']['dm'],set())
        self.assertEqual(r.data['146']['dm'],{P+'reconstruction_damage'})

    def test_unaccepted_finance_cannot_unlock_followup_benefits(self):
        r=self.r;r.ready('p1_finance_a_follow');r.data['CYP']['f'].discard(P+'applied_p1_finance_a')
        r.call('complete_p1_finance_a_follow')
        self.assertIn(P+'pending_completion_p1_finance_a_follow',r.data['CYP']['f'])
        self.assertNotIn(P+'applied_p1_finance_a_follow',r.data['CYP']['f'])

    def test_only_current_party_programme_enables_and_rewards_do_not_repeat(self):
        r=self.r;r.call('grant_p1_organisation');r.call('grant_p1_organisation');r.call('grant_p2_organisation')
        self.assertAlmostEqual(r.data['CYP']['v'][P+'p1_stability_factor'],.03)
        modifiers=parse((ROOT/'common/dynamic_modifiers/COLDWAR_CYP_1970_modifiers.txt').read_text())
        enable={k:first(v,'enable',[]) for k,op,v in modifiers if first(v,'enable')}
        r.data['CYP']['v']['ruling_party']=2
        self.assertFalse(r.test(enable[P+'p1_programme']))
        self.assertTrue(r.test(enable[P+'p2_programme']))
        self.assertEqual(sum(r.test(v) for v in enable.values()),1)

    def test_later_settlement_can_finish_displacement_recovery(self):
        r=self.r;r.data['CYP']['f'].update({P+'applied_reconstruction',P+'restitution_implemented',P+'displacement_active'})
        r.data['CYP']['ideas'].add(P+'displacement_emergency')
        r.call('update_displacement_recovery')
        self.assertIn(P+'displacement_emergency',r.data['CYP']['ideas'])
        r.data['CYP']['f'].add(P+'final_settlement_implemented');r.call('update_displacement_recovery')
        self.assertNotIn(P+'displacement_emergency',r.data['CYP']['ideas'])


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TransactionTests))
    (HERE/'transaction_tests.json').write_text(json.dumps({'passed':result.wasSuccessful(),'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'engine_emulation':False},indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
