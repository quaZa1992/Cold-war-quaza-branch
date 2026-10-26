# IMPERIA CW — Cold War: execute authored readiness scripts against multiplayer scenarios.
"""Strict AST interpreter. Native graphics, notifications and economy refresh are boundaries."""
from pathlib import Path
import copy
import json
import math
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools/vietnam_1970'))
from script_ast import parse, first, walk
from build import MACROS

P='COLDWAR_nr_'
def read(rel):return (ROOT/rel).read_text(encoding='utf-8-sig')
E={k:v for k,_,v in parse(read('common/scripted_effects/COLDWAR_nuclear_readiness.txt'))}
T={k:v for k,_,v in parse(read('common/scripted_triggers/COLDWAR_nuclear_readiness.txt'))}
# IMPERIA CW — Cold War: execute the target-bound release procedure and native war boundary.
E.update({k:v for k,_,v in parse(read('common/scripted_effects/COLDWAR_nuclear_escalation.txt'))})
T.update({k:v for k,_,v in parse(read('common/scripted_triggers/COLDWAR_nuclear_escalation.txt'))})
T.update({k:v for k,_,v in parse(read('common/scripted_triggers/01_raids_triggers.txt')) if k in ['is_able_to_use_nuclear_strikes','is_able_to_use_nuclear_strikes_tac']})
A={k:v for k,_,v in parse(read('common/scripted_diplomatic_actions/COLDWAR_nuclear_readiness.txt'))[0][2]}

class World:
    def __init__(self):
        self.tags=['USA','SOV','FRA','CHI','GER','RAID']
        self.ids={tag:i+1 for i,tag in enumerate(self.tags)}
        self.c={t:{'v':{'gdp_per_capita':36,'gdp_total':1000,'inflation_multiplier':1},'flags':{},'stock':{'nuclear_missile_equipment':1000,'nuclear_ballistic_missile_equipment':500},'ideas':{'nuclear_power_off','full_first_use'},'dynamic':set(),'pp':500,'ai':False,'cap':False,'subject':False,'exists':True,'faction':t,'intel':{}} for t in self.tags}
        self.g={P+'serial':0,'mdcw_cw_tension':20}
        self.day=1;self.targets={};self.events=[];self.threat=0
        self.enabled=True;self.wars=set();self.naps=set();self.declarations=[];self.queue=[]
        for c in self.c.values():c.update(stability=.8,opinion={},overlord=None)
        for tag in self.tags[:-1]:self.call('init',tag)
    def scope(self,name,stack,root,fr):
        if name=='THIS':return stack[-1]
        if name=='ROOT':return root
        if name=='PREV':return stack[-2] if len(stack)>1 else None
        if name=='FROM':return fr
        if name.startswith('event_target:'):return self.targets.get(name.split(':',1)[1])
        if name.startswith('var:'):
            ident=self.num(name[4:],stack,root,fr)
            return next((k for k,v in self.ids.items() if v==ident),None)
        return name if name in self.c else None
    def address(self,name,stack,root,fr):
        name=str(name)
        if '@' in name and not name.startswith(('num_equipment@',)):
            key,target=name.split('@',1)
            name=key+'@'+str(self.scope(target,stack,root,fr) or target)
        if name.startswith('global.'):return self.g,name[7:]
        if '.' in name:
            scope,key=name.rsplit('.',1)
            tag=self.scope(scope,stack,root,fr)
            if tag is None:raise AssertionError(('invalid variable scope',name,stack))
            if key=='id':return None,self.ids[tag]
            return self.c[tag]['v'],key
        return self.c[stack[-1]]['v'],name
    def num(self,value,stack,root,fr):
        if isinstance(value,list):
            result=0
            for k,_,v in value:
                if k=='value':result=self.num(v,stack,root,fr)
                elif k=='add':result+=self.num(v,stack,root,fr)
                elif k=='subtract':result-=self.num(v,stack,root,fr)
                elif k=='multiply':result*=self.num(v,stack,root,fr)
                elif k=='divide':result/=self.num(v,stack,root,fr)
                elif k=='round':result=math.floor(result+.5)
                elif k=='clamp':result=max(self.num(first(v,'min',-1e30),stack,root,fr),min(self.num(first(v,'max',1e30),stack,root,fr),result))
                else:raise AssertionError(('math',k))
            return result
        try:return float(value)
        except (TypeError,ValueError):pass
        if value=='global.num_days':return self.day
        if str(value).startswith('num_equipment@'):return self.c[stack[-1]]['stock'].get(value.split('@',1)[1],0)
        if str(value)=='THIS.id':return self.ids[stack[-1]]
        store,key=self.address(value,stack,root,fr)
        return key if store is None else store.get(key,0)
    def cond(self,rows,stack,root,fr=None):
        chain=False;answers=[]
        c=self.c[stack[-1]]
        for k,op,v in rows:
            if k in ['tooltip']:continue
            if k in ['if','else_if','else']:
                if k=='if':chain=False
                if not chain and (k=='else' or self.cond(first(v,'limit',[]),stack,root,fr)):
                    chain=True;answers.append(self.cond([r for r in v if r[0]!='limit'],stack,root,fr))
                continue
            if k in ['custom_trigger_tooltip','custom_override_tooltip','hidden_trigger','AND']:answer=self.cond(v,stack,root,fr)
            elif k=='NOT':answer=not self.cond(v,stack,root,fr)
            elif k=='OR':answer=any(self.cond([r],stack,root,fr) for r in v)
            elif k in T:answer=self.cond(T[k],stack,root,fr)
            elif k=='always':answer=v=='yes'
            elif k=='IMP_is_1970_scenario':answer=self.enabled
            elif k=='has_dlc':answer=True
            elif k=='is_ai':answer=c['ai']==(v=='yes')
            elif k=='has_capitulated':answer=c['cap']==(v=='yes')
            elif k=='is_subject':answer=c['subject']==(v=='yes')
            elif k=='exists':answer=c['exists']==(v=='yes')
            elif k=='has_political_power':answer=c['pp']>self.num(v,stack,root,fr)
            elif k=='has_idea':answer=v in c['ideas']
            elif k=='has_variable':
                store,key=self.address(v,stack,root,fr);answer=key in store
            elif k=='has_country_flag':answer=v in c['flags'] and (c['flags'][v] is None or c['flags'][v]>self.day)
            elif k=='has_global_flag':answer=v=='mdcw_cw_initialized'
            elif k=='has_dynamic_modifier':answer=first(v,'modifier') in c['dynamic']
            elif k=='has_equipment':
                eq,cmp,n=v[0];answer=c['stock'].get(eq,0)>float(n) if cmp=='>' else c['stock'].get(eq,0)==float(n)
            elif k=='check_variable':
                a,cmp,b=v[0];a=self.num(a,stack,root,fr);b=self.num(b,stack,root,fr)
                answer={'=':a==b,'>':a>b,'<':a<b,'>=':a>=b,'<=':a<=b,'!=':a!=b}[cmp]
            elif k=='tag':answer=stack[-1]==self.scope(v,stack,root,fr)
            elif k=='is_in_faction_with':answer=c['faction']==self.c[self.scope(v,stack,root,fr)]['faction']
            elif k=='has_war_with':answer=frozenset([stack[-1],self.scope(v,stack,root,fr)]) in self.wars
            elif k=='has_non_aggression_pact_with':answer=frozenset([stack[-1],self.scope(v,stack,root,fr)]) in self.naps
            elif k=='is_subject_of':answer=c['overlord']==self.scope(v,stack,root,fr)
            elif k=='is_in_array':answer=self.num(first(v,'value'),stack,root,fr) in c['v'].get(first(v,'array'),[])
            elif k=='intel_level_over':
                target=self.scope(first(v,'target'),stack,root,fr)
                amount=float(next(x for a,_,x in v if a=='airforce_intel'))
                answer=c['intel'].get(target,0)>amount
            elif k=='set_temp_variable':self.run([(k,op,v)],stack,root,fr);answer=True
            else:
                target=self.scope(k,stack,root,fr)
                if target is None:raise AssertionError(('trigger',k,stack))
                answer=self.cond(v,stack+[target],root,fr)
            answers.append(answer)
        return all(answers)
    def run(self,rows,stack,root,fr=None):
        chain=False
        for k,op,v in rows:
            c=self.c[stack[-1]]
            if k in ['if','else_if','else']:
                if k=='if':chain=False
                if not chain and (k=='else' or self.cond(first(v,'limit',[]),stack,root,fr)):
                    chain=True;self.run([r for r in v if r[0]!='limit'],stack,root,fr)
            elif k in E:
                body=E[k]
                if isinstance(v,list):
                    params={a:b for a,_,b in v}
                    def subst(x):
                        if isinstance(x,list):return [(subst(a),b,subst(c)) for a,b,c in x]
                        for a,b in params.items():x=x.replace('$'+a+'$',str(b))
                        return x
                    body=subst(body)
                self.run(body,stack,root,fr)
            elif k in ['set_variable','set_temp_variable','add_to_variable','subtract_from_variable','multiply_variable','add_to_temp_variable','multiply_temp_variable']:
                name,_,amount=v[0];amount=self.num(amount,stack,root,fr);store,key=self.address(name,stack,root,fr)
                if k.startswith('set_'):store[key]=amount
                elif k.startswith('add_'):store[key]=store.get(key,0)+amount
                elif k.startswith('subtract_'):store[key]=store.get(key,0)-amount
                else:store[key]=store.get(key,0)*amount
            elif k=='clamp_variable':
                store,key=self.address(first(v,'var'),stack,root,fr)
                store[key]=max(float(first(v,'min',-1e30)),min(float(first(v,'max',1e30)),store.get(key,0)))
            elif k=='clear_variable':
                store,key=self.address(v,stack,root,fr);store.pop(key,None)
            elif k=='set_country_flag':
                if isinstance(v,list):c['flags'][first(v,'flag')]=self.day+float(first(v,'days'))
                else:c['flags'][v]=None
            elif k=='clr_country_flag':c['flags'].pop(v,None)
            elif k=='add_dynamic_modifier':c['dynamic'].add(first(v,'modifier'))
            elif k=='remove_dynamic_modifier':c['dynamic'].discard(first(v,'modifier'))
            elif k=='add_political_power':c['pp']+=float(v)
            elif k=='save_event_target_as':self.targets[v]=stack[-1]
            elif k=='country_event':
                event=first(v,'id')
                if event=='cw_nuclear.90':
                    # Native 1.19 processes the scheduling hour inclusively.
                    delay=max(0,float(first(v,'hours',0))-1)+24*float(first(v,'days',0))
                    self.queue.append((round(self.day*24+delay,8),stack[-1]))
                else:self.events.append((stack[-1],event))
            elif k=='declare_war_on':
                target=self.scope(first(v,'target'),stack,root,fr)
                self.wars.add(frozenset([stack[-1],target]));self.declarations.append((stack[-1],target))
            elif k=='add_stability':c['stability']+=float(v)
            elif k=='add_opinion_modifier':c['opinion'][self.scope(first(v,'target'),stack,root,fr)]=first(v,'modifier')
            elif k=='every_country':
                for tag in self.tags[:-1]:
                    if self.cond(first(v,'limit',[]),stack+[tag],root,fr):self.run([r for r in v if r[0]!='limit'],stack+[tag],root,fr)
            elif k=='add_named_threat':self.threat+=float(first(v,'threat'))
            elif k=='mdcw_cw_add_tension':self.g['mdcw_cw_tension']=max(0,min(100,self.g['mdcw_cw_tension']+c['v']['mdcw_cw_tension_delta']))
            elif k=='add_to_array':
                key=first(v,'array');c['v'].setdefault(key,[]).append(self.num(first(v,'value'),stack,root,fr))
            elif k=='add_equipment_to_stockpile':
                eq=first(v,'type');c['stock'][eq]=max(0,c['stock'].get(eq,0)+self.num(first(v,'amount'),stack,root,fr))
            elif k=='force_update_dynamic_modifier':pass
            else:
                target=self.scope(k,stack,root,fr)
                if target is None:raise AssertionError(('effect',k,stack))
                self.run(v,stack+[target],root,fr)
    def call(self,name,tag='USA',prev=None,params=None,fr=None):
        stack=([prev] if prev else [])+[tag]
        if 'nr_'+name in MACROS:
            param,choices=MACROS['nr_'+name]
            value=next(v for k,_,v in params if k==param)
            name+='_'+choices[str(value)]
        self.run([(P+name,'=','yes')],stack,tag,fr)
    def check(self,name,tag='USA',prev=None,fr=None):
        return self.cond(T[P+name],([prev] if prev else [])+[tag],tag,fr)
    def var(self,name,tag='USA'):return self.c[tag]['v'].get(P+name,0)
    def set(self,name,value,tag='USA'):self.c[tag]['v'][P+name]=value
    def advance_hours(self,hours):
        until=round(self.day*24+hours,8)
        while self.queue and min(self.queue)[0]<=until:
            when,tag=min(self.queue);self.queue.remove((when,tag));self.day=when/24
            self.call('first_use_tick',tag)
        self.day=until/24
    def level(self,n,tag='USA'):self.set('level',n,tag);self.set('order',n,tag);self.call('refresh',tag)
    def warn(self,a='USA',b='SOV'):self.call('begin_crisis',a,b)
    def offer(self,kind=1,a='USA',b='SOV'):
        self.call('send_offer',a,b,[('KIND','=',str(kind))])
    def accept(self,kind=1,a='USA',b='SOV'):
        self.set('accept_kind',kind,a);self.call('finish_offer',a,b,[('KIND','=',str(kind))])

class Readiness(unittest.TestCase):
    # IMPERIA CW — Cold War: arsenal ownership enables nuclear diplomacy for every country.
    def test_warning_access_follows_weapons_without_status_laws_or_country_restrictions(self):
        for tag in World().tags[:-1]:
            for equipment in ['nuclear_missile_equipment','nuclear_ballistic_missile_equipment']:
                with self.subTest(country=tag,equipment=equipment):
                    w=World();target='SOV' if tag!='SOV' else 'USA'
                    w.c[tag]['ideas'].clear()
                    w.c[tag]['stock']={equipment:1}
                    w.c[tag]['subject']=tag=='GER'
                    w.call('refresh',tag)
                    self.assertTrue(w.check('nuclear_power',tag))
                    self.assertTrue(w.cond(first(A[P+'warning'],'visible'),[target],tag))
                    self.assertFalse(w.cond(first(A[P+'warning'],'selectable'),[target],tag))
                    w.call('order_level',tag,params=[('LEVEL','=','3')])
                    for _ in range(4):w.call('daily',tag)
                    for field in ['selectable','can_be_sent']:
                        self.assertTrue(w.cond(first(A[P+'warning'],field),[target],tag),field)
                    w.warn(tag,target)
                    self.assertEqual(w.var('opponent',tag),w.ids[target])
                    self.assertEqual(w.var('opponent',target),w.ids[tag])
    def test_nuclear_status_without_weapons_does_not_enable_warning(self):
        w=World();w.c['USA']['stock']={};w.level(3)
        self.assertFalse(w.check('nuclear_power'))
        self.assertFalse(w.cond(first(A[P+'warning'],'visible'),['SOV'],'USA'))
        self.assertFalse(w.check('can_warn_prev',prev='SOV'))
        w.warn();self.assertFalse(w.var('opponent'))
    def test_orders_have_real_lead_time_and_old_posture_remains(self):
        w=World();w.call('order_level',params=[('LEVEL','=','3')])
        self.assertEqual((w.var('level'),w.var('build_days')),(5,4))
        self.assertFalse(w.check('tactical_ready'))
        for _ in range(4):w.call('daily')
        self.assertEqual(w.var('level'),3);self.assertTrue(w.check('tactical_ready'))
        self.assertFalse(w.check('state_ready'))
        self.assertEqual(w.c['USA']['pp'],475)
    def test_standdown_blocks_rearm_but_a_nuclear_attack_releases_it(self):
        w=World();w.c['USA']['flags'][P+'standdown']=31
        w.call('order_level',params=[('LEVEL','=','1')])
        self.assertEqual(w.var('level'),5)
        self.raid(w,'SOV','USA')
        self.assertNotIn(P+'standdown',w.c['USA']['flags'])
        self.assertEqual(w.var('build_days'),1)
        w.call('daily');self.assertEqual(w.var('level'),1)
        self.assertTrue(w.check('retaliation_allowed',fr='SOV'))
        self.assertFalse(w.check('retaliation_allowed',fr='FRA'))
    def test_simultaneous_crossed_and_third_party_warnings(self):
        w=World();w.level(3);w.level(3,'SOV');w.level(3,'FRA')
        w.warn();serial=w.var('serial')
        w.warn('SOV','USA');w.warn('FRA','SOV')
        self.assertEqual(w.var('serial'),serial)
        self.assertEqual(w.var('opponent'),w.ids['SOV'])
        self.assertFalse(w.var('opponent','FRA'))
        self.assertEqual(w.g['mdcw_cw_tension'],25)
    def test_two_independent_crises_and_mutual_resolution(self):
        w=World()
        for t in ['USA','SOV','FRA','CHI']:w.level(3,t)
        w.warn();w.warn('FRA','CHI');w.call('counter_signal','SOV','USA')
        self.assertEqual(w.g['mdcw_cw_tension'],33)
        w.offer();w.accept();self.assertIn(P+'hotline',w.c['SOV']['flags'])
        w.day+=22;w.offer(2);w.accept(2)
        self.assertEqual(w.g['mdcw_cw_tension'],25)
        self.assertEqual((w.var('level'),w.var('level','SOV')),(5,5))
        self.assertFalse(w.var('opponent'));self.assertTrue(w.check('pair_valid','FRA'))
        self.assertFalse(w.check('can_warn_prev',prev='SOV'))
    def test_expired_offer_cannot_execute(self):
        w=World();w.level(3);w.warn();w.offer();w.day+=15;w.accept()
        self.assertNotIn(P+'hotline',w.c['USA']['flags'])
    def test_nuclear_use_invalidates_outstanding_offer(self):
        w=World();w.level(3);w.warn();w.offer();self.raid(w,'USA','SOV')
        self.assertFalse(w.check('offer_intact_prev',prev='SOV'))
        w.accept();self.assertNotIn(P+'hotline',w.c['USA']['flags'])
        self.assertIn(('USA','cw_nuclear.13'),w.events)
    def test_routine_and_high_alert_protect_different_reserves(self):
        a=World();a.level(5,'SOV');self.raid(a,'USA','SOV',.4)
        b=World();b.level(1,'SOV');self.raid(b,'USA','SOV',.4)
        self.assertEqual(a.c['SOV']['stock']['nuclear_missile_equipment'],640)
        self.assertEqual(b.c['SOV']['stock']['nuclear_missile_equipment'],800)
        self.assertEqual(len(b.c['SOV']['v'][P+'aggressors']),1)
    def test_fatigue_recovers_and_refresh_never_spends(self):
        w=World();w.level(1)
        for _ in range(50):w.call('daily')
        self.assertEqual(w.var('fatigue'),100)
        self.assertAlmostEqual(w.var('fatigue_stability'),-.05)
        expected=(.002+1500*.00001)*2.5*1.5
        self.assertAlmostEqual(w.var('forces_weekly'),expected)
        pp=w.c['USA']['pp']
        for _ in range(5):w.call('init')
        self.assertAlmostEqual(w.var('forces_weekly'),expected);self.assertEqual(w.c['USA']['pp'],pp)
        w.call('stand_down')
        for _ in range(50):w.call('daily')
        self.assertEqual(w.var('fatigue'),0)
    def test_civil_defence_preparation_costs_and_release(self):
        w=World();w.call('start_civil')
        self.assertEqual(w.var('civil_days'),3)
        self.assertAlmostEqual(w.var('civil_weekly'),.022)
        self.assertNotIn(P+'civil_active',w.c['USA']['flags'])
        for _ in range(3):w.call('daily')
        self.assertIn(P+'civil_active',w.c['USA']['flags'])
        w.call('end_civil');self.assertEqual(w.var('civil_weekly'),0)
        self.assertNotIn(P+'civil_defence',w.c['USA']['dynamic'])
    def test_stock_loss_cancels_empty_arsenal_and_stale_launch_cache(self):
        w=World();w.level(1);w.c['USA']['stock']={}
        self.assertFalse(w.check('strategic_ready'))
        w.call('daily');self.assertEqual(w.var('level'),5)
        self.assertEqual(w.var('forces_weekly'),0)
    def test_intelligence_access_does_not_reveal_exact_low_intel(self):
        w=World();w.level(2,'SOV')
        w.call('assess_prev',prev='SOV');self.assertEqual(w.var('assessment'),0)
        w.c['USA']['intel']['SOV']=.5;w.call('assess_prev',prev='SOV')
        self.assertEqual((w.var('assessment'),w.var('assessed_level')),(1,3))
        w.c['USA']['intel']['SOV']=.8;w.call('assess_prev',prev='SOV')
        self.assertEqual((w.var('assessment'),w.var('assessed_level')),(2,2))
        self.assertEqual(w.g['mdcw_cw_tension'],21)
        w.call('assess_prev',prev='SOV');self.assertEqual(w.g['mdcw_cw_tension'],21)
    def test_collapse_or_orphan_cleanup_does_not_clear_another_crisis(self):
        w=World();w.level(3);w.warn();w.set('serial',999,'SOV')
        w.call('daily');self.assertFalse(w.var('opponent'))
        self.assertEqual(w.var('serial','SOV'),999)
    def test_no_duplicate_counter_alert(self):
        w=World();w.level(3);w.level(3,'SOV');w.warn()
        w.call('counter_signal',prev='SOV');self.assertEqual(w.g['mdcw_cw_tension'],25)
        w.call('counter_signal','SOV','USA');w.call('counter_signal','SOV','USA')
        self.assertEqual(w.g['mdcw_cw_tension'],28)
    def test_capped_tension_cannot_be_farmed_by_mutual_standdown(self):
        w=World();w.g['mdcw_cw_tension']=99;w.level(3);w.level(3,'SOV')
        w.warn();w.call('counter_signal','SOV','USA')
        self.assertEqual(w.var('pressure'),1)
        w.offer();w.accept();w.day+=22;w.offer(2);w.accept(2)
        self.assertEqual(w.g['mdcw_cw_tension'],99)
    def test_recipient_cannot_withdraw_the_issuers_warning(self):
        w=World();w.level(3);w.level(3,'SOV');w.warn()
        w.call('withdraw','SOV','USA')
        self.assertTrue(w.check('pair_valid'))
        self.assertEqual(w.g['mdcw_cw_tension'],25)
        w.call('withdraw',prev='SOV')
        self.assertFalse(w.check('pair_valid'))
        self.assertEqual(w.g['mdcw_cw_tension'],23)
    def test_capped_tension_cannot_be_farmed_by_unilateral_withdrawal(self):
        for initial in [99,99.5,100]:
            w=World();w.g['mdcw_cw_tension']=initial;w.level(3);w.warn()
            w.call('withdraw',prev='SOV')
            self.assertEqual(w.g['mdcw_cw_tension'],initial)
    @staticmethod
    def raid(w,attacker,victim,loss=.15):
        w.wars.add(frozenset([attacker,victim]))
        w.c['RAID']['v'].update(actor_country=w.ids[attacker],victim_country=w.ids[victim])
        w.call('record_raid','RAID',params=[('LOSS','=',str(loss))])

# IMPERIA CW — Cold War: multiplayer first-use lifecycle and adversarial state changes.
class FirstUse(unittest.TestCase):
    def prepared(self,tag='USA',target='SOV'):
        w=World();w.level(1,tag);w.warn(tag,target)
        self.assertTrue(w.check('can_ultimatum_prev',tag,prev=target))
        w.call('issue_ultimatum',tag,prev=target)
        return w
    def operation(self,w,attacker='USA',victim='SOV'):
        w.c['RAID']['v'].update(actor_country=w.ids[attacker],victim_country=w.ids[victim])
        w.call('resolve_peacetime_operation','RAID')
    def test_exact_72_hour_ultimatum_and_seven_day_window_without_automatic_war(self):
        w=self.prepared()
        self.assertTrue(w.check('can_prepare_nuclear_operation',fr='SOV'))
        self.assertFalse(w.check('can_launch_nuclear_operation',fr='SOV'))
        w.advance_hours(71)
        self.assertEqual(w.var('fu_hours'),1)
        self.assertFalse(w.check('can_launch_nuclear_operation',fr='SOV'))
        w.advance_hours(1)
        self.assertEqual(w.var('fu_hours'),168)
        self.assertTrue(w.check('can_launch_nuclear_operation',fr='SOV'))
        self.assertIn(('USA','cw_nuclear.16'),w.events)
        self.assertIn(('SOV','cw_nuclear.17'),w.events)
        w.advance_hours(167);self.assertTrue(w.check('can_launch_nuclear_operation',fr='SOV'))
        w.advance_hours(1);self.assertFalse(w.check('can_launch_nuclear_operation',fr='SOV'))
        self.assertFalse(w.var('fu_partner'));self.assertFalse(w.wars)
        self.assertIn(('SOV','cw_nuclear.20'),w.events)
    def test_authority_is_bound_to_the_warned_country(self):
        w=self.prepared();w.advance_hours(72)
        self.assertTrue(w.check('release_for_from',fr='SOV'))
        self.assertFalse(w.check('release_for_from',fr='FRA'))
        self.assertFalse(w.check('can_prepare_nuclear_operation',fr='FRA'))
        self.assertFalse(w.check('can_launch_nuclear_operation',fr='FRA'))
    def test_new_nuclear_countries_receive_the_same_procedure(self):
        for tag in ['USA','SOV','FRA','CHI','GER']:
            with self.subTest(country=tag):
                target='SOV' if tag!='SOV' else 'USA'
                w=self.prepared(tag,target);w.advance_hours(72)
                self.assertTrue(w.check('can_launch_nuclear_operation',tag,fr=target))
    def test_retaliation_only_and_defensive_policies_cannot_issue_first_use_orders(self):
        for ideas in [{'nuclear_power_off','strategic_retaliation_only'}, {'nuclear_power_off','tac_and_strat_retaliation'}, {'nuclear_power_def','full_first_use'}]:
            with self.subTest(ideas=ideas):
                w=World();w.level(1);w.warn();w.c['USA']['ideas']=ideas
                self.assertFalse(w.check('can_ultimatum_prev',prev='SOV'))
                w.call('issue_ultimatum',prev='SOV');self.assertFalse(w.var('fu_partner'))
    def test_tactical_first_use_does_not_unlock_strategic_first_use(self):
        w=World();w.level(1);w.warn();w.c['USA']['ideas']={'nuclear_power_off','tac_first_use_strat_retaliation'}
        w.call('issue_ultimatum',prev='SOV');w.advance_hours(72)
        self.assertTrue(w.check('release_for_from',fr='SOV'))
        self.assertTrue(w.cond([('is_able_to_use_nuclear_strikes_tac','=','yes')],['USA'],'USA',fr='SOV'))
        self.assertFalse(w.cond([('is_able_to_use_nuclear_strikes','=','yes')],['USA'],'USA',fr='SOV'))
    def test_lowering_readiness_immediately_revokes_release(self):
        w=self.prepared();w.advance_hours(72);w.level(2)
        self.assertFalse(w.var('fu_partner'));self.assertFalse(w.check('can_launch_nuclear_operation',fr='SOV'))
        w.advance_hours(240);self.assertFalse(w.wars)
    def test_lost_weapons_or_changed_doctrine_revoke_the_procedure(self):
        for change in ['arsenal','doctrine','subject','capitulation']:
            with self.subTest(change=change):
                w=self.prepared()
                if change=='arsenal':w.c['USA']['stock']={}
                elif change=='doctrine':w.c['USA']['ideas']={'nuclear_power_off','strategic_retaliation_only'}
                elif change=='subject':w.c['USA']['subject']=True
                else:w.c['USA']['cap']=True
                w.advance_hours(1)
                self.assertFalse(w.var('fu_partner'));self.assertFalse(w.check('can_launch_nuclear_operation',fr='SOV'))
    def test_alliance_pact_or_target_collapse_blocks_prepared_launches(self):
        for change in ['faction','pact','subject','capitulation','removed']:
            with self.subTest(change=change):
                w=self.prepared();w.advance_hours(72)
                if change=='faction':w.c['SOV']['faction']='USA'
                elif change=='pact':w.naps.add(frozenset(['USA','SOV']))
                elif change=='subject':w.c['SOV']['subject']=True
                elif change=='capitulation':w.c['SOV']['cap']=True
                else:w.c['SOV']['exists']=False
                self.assertFalse(w.check('release_for_from',fr='SOV'))
                w.advance_hours(1);self.assertFalse(w.var('fu_partner'))
    def test_pair_serial_and_nuclear_use_snapshots_cannot_be_reused(self):
        for change in ['pair','own_use','peer_use']:
            with self.subTest(change=change):
                w=self.prepared();w.advance_hours(72)
                if change=='pair':w.set('serial',w.var('serial')+1)
                elif change=='own_use':w.set('strike_revision',w.var('strike_revision')+1)
                else:w.set('strike_revision',w.var('strike_revision','SOV')+1,'SOV')
                self.assertFalse(w.check('release_for_from',fr='SOV'))
                w.advance_hours(1);self.assertFalse(w.var('fu_partner'))
    def test_revocation_stops_the_timer_without_refunding_or_rearming(self):
        w=self.prepared();pressure=w.g['mdcw_cw_tension']
        w.call('revoke_first_use',prev='SOV')
        self.assertFalse(w.var('fu_partner'));self.assertEqual(w.var('level'),1)
        w.advance_hours(240)
        self.assertNotIn(('USA','cw_nuclear.16'),w.events)
        self.assertFalse(w.check('can_ultimatum_prev',prev='SOV'))
        self.assertEqual(w.g['mdcw_cw_tension'],pressure)
    def test_only_one_ultimatum_can_be_issued_during_the_cooling_off_period(self):
        w=self.prepared();w.call('issue_ultimatum',prev='SOV')
        self.assertEqual(w.g['mdcw_cw_tension'],30)
        self.assertEqual(len(w.queue),1)
        w.call('withdraw',prev='SOV');w.warn('USA','FRA')
        self.assertFalse(w.check('can_ultimatum_prev',prev='FRA'))
    def test_hotline_allows_immediate_standdown_before_the_ultimatum_expires(self):
        w=self.prepared();w.offer();w.accept()
        self.assertTrue(w.check('can_offer_prev',prev='SOV'))
        w.offer(2);w.accept(2)
        self.assertFalse(w.var('fu_partner'));self.assertEqual(w.var('level'),5)
        w.advance_hours(240);self.assertFalse(w.wars)
        self.assertNotIn(('USA','cw_nuclear.16'),w.events)
    def test_mutual_standdown_cancels_both_governments_release_orders(self):
        w=self.prepared();w.level(1,'SOV');w.call('issue_ultimatum','SOV',prev='USA')
        w.advance_hours(72)
        self.assertTrue(w.check('release_for_from','SOV',fr='USA'))
        w.offer();w.accept();w.offer(2);w.accept(2)
        self.assertFalse(w.var('fu_partner'));self.assertFalse(w.var('fu_partner','SOV'))
        self.assertEqual(w.g['mdcw_cw_tension'],20)
        w.advance_hours(200);self.assertFalse(w.wars)
    def test_capped_ultimatum_pressure_cannot_create_a_tension_refund(self):
        for initial in [99,99.5,100]:
            with self.subTest(initial=initial):
                w=World();w.g['mdcw_cw_tension']=initial;w.level(1);w.warn();w.call('issue_ultimatum',prev='SOV')
                w.offer();w.accept();w.offer(2);w.accept(2)
                self.assertEqual(w.g['mdcw_cw_tension'],initial)
    def test_first_operation_opens_war_once_and_attributes_retaliation_to_the_attacker(self):
        w=self.prepared();w.advance_hours(72);w.offer()
        self.operation(w)
        self.assertEqual(w.declarations,[('USA','SOV')])
        self.assertAlmostEqual(w.c['USA']['stability'],.75)
        self.assertEqual(w.g['mdcw_cw_tension'],50)
        self.assertTrue(w.check('retaliation_allowed','SOV',fr='USA'))
        self.assertFalse(w.check('retaliation_allowed','SOV',fr='FRA'))
        self.assertFalse(w.check('offer_intact_prev',prev='SOV'))
        self.assertEqual(w.c['FRA']['opinion']['USA'],P+'first_use_condemnation')
        self.assertFalse(w.var('fu_partner'))
        snapshot=(w.g['mdcw_cw_tension'],w.threat,w.c['USA']['stability'],len(w.events))
        self.operation(w)
        self.assertEqual((w.g['mdcw_cw_tension'],w.threat,w.c['USA']['stability'],len(w.events)),snapshot)
        self.assertEqual(len(w.declarations),1)
    def test_committed_operations_still_open_war_after_release_is_revoked(self):
        w=self.prepared();w.advance_hours(72);w.call('revoke_first_use',prev='SOV')
        self.assertFalse(w.check('can_launch_nuclear_operation',fr='SOV'))
        self.operation(w);self.assertEqual(w.declarations,[('USA','SOV')])
    def test_wartime_operations_do_not_receive_peacetime_first_use_penalties(self):
        w=World();w.wars.add(frozenset(['USA','SOV']))
        self.assertTrue(w.check('can_launch_nuclear_operation',fr='SOV'))
        self.operation(w)
        self.assertFalse(w.declarations);self.assertEqual(w.g['mdcw_cw_tension'],20)
        self.assertEqual(w.c['USA']['stability'],.8)
    def test_existing_war_and_ai_rules_remain_in_force_outside_the_scenario(self):
        w=World();w.enabled=False
        self.assertTrue(w.check('can_prepare_tactical_operation',fr='SOV'))
        self.assertFalse(w.check('can_launch_nuclear_operation',fr='SOV'))
        w.wars.add(frozenset(['USA','SOV']));self.assertTrue(w.check('can_launch_nuclear_operation',fr='SOV'))
        w=self.prepared();w.call('revoke_first_use',prev='SOV');w.c['USA']['flags'].pop(P+'fu_cooldown');w.c['USA']['ai']=True
        self.assertFalse(w.check('can_ultimatum_prev',prev='SOV'))

class Integration(unittest.TestCase):
    def test_live_script_encoding_references_and_precision(self):
        files=list((ROOT/'common').glob('*/COLDWAR_nuclear_readiness.txt'))+list((ROOT/'common').glob('*/COLDWAR_nuclear_escalation.txt'))+list((ROOT/'interface').glob('COLDWAR_nuclear_readiness.*'))+list((ROOT/'events').glob('COLDWAR_nuclear_readiness.txt'))
        for path in files:
            self.assertFalse(path.read_bytes().startswith(b'\xef\xbb\xbf'),path)
            s=path.read_text(encoding='utf-8');parse(s)
            self.assertNotRegex(s,r'\b\d+\.\d{6,}\b')
            self.assertTrue(s.startswith('# IMPERIA CW'))
        loc=ROOT/'localisation/english/COLDWAR_nuclear_readiness_l_english.yml'
        self.assertTrue(loc.read_bytes().startswith(b'\xef\xbb\xbf'))
        keys=re.findall(r'^ ([\w.]+):',loc.read_text(encoding='utf-8-sig'),re.M)
        self.assertEqual(len(keys),len(set(keys)))
        self.assertNotIn('[event_target:',loc.read_text(encoding='utf-8-sig'))
        # IMPERIA CW — Cold War: native diplomacy derives these keys from each action ID.
        for action_id in A:
            for suffix in ['_TITLE','_ACTION_DESC']:
                self.assertIn(action_id.upper()+suffix,keys)
        for path in files:
            for k,_,v in walk(parse(path.read_text(encoding='utf-8'))):
                if k in ['tooltip','pdx_tooltip','localization_key','send_description','receive_description','accept_title','accept_description','reject_title','reject_description'] and str(v).startswith(P):self.assertIn(v,keys,(path,k,v))
    def test_all_raid_phases_recheck_and_each_hit_records_once(self):
        raids=parse(read('common/raids/nuclear_raids.txt'))[0][2]
        for (_,_,body),kind,count in zip(raids,['tactical','state','strategic'],[2,4,4]):
            for field in ['available','launchable']:
                phase=first(body,field)
                self.assertEqual(phase[0],('is_ai','=','no'))
                self.assertIn((P+kind+'_ready','=','yes'),phase)
            self.assertEqual(sum(k.startswith(P+'record_raid_') for k,_,_ in walk(body)),count)
            self.assertEqual(sum(k==P+'resolve_peacetime_operation' for k,_,_ in walk(body)),4)
            self.assertIn((P+'can_launch_nuclear_operation','=','yes'),first(body,'launchable'))
            self.assertFalse(any(k=='has_war_with' for k,_,_ in walk(first(body,'available'))))
    def test_budget_is_aggregated_once_and_civil_protection_in_both_callbacks(self):
        money=read('common/scripted_effects/00_money_system.txt')
        self.assertEqual(money.count('add = '+P+'weekly_cost'),1)
        self.assertEqual(money.count(P+'calculate_budget = yes'),1)
        damage=read('common/scripted_effects/mdcw_imperia_nuclear_effects.txt')
        self.assertEqual(damage.count(P+'civilian_protection = yes'),2)
        doctrine=read('common/scripted_triggers/01_raids_triggers.txt')
        self.assertEqual(doctrine.count(P+'retaliation_allowed = yes'),4)
    def test_generation_is_deterministic(self):
        import build
        build.artwork()
        for rel,expected in build.FILES.items():self.assertEqual(read(rel),expected,rel)
    def test_timed_commitments_have_an_explicit_nonzero_flag_value(self):
        for file in ['COLDWAR_nuclear_readiness.txt','COLDWAR_nuclear_escalation.txt']:
            for k,_,v in walk(parse(read('common/scripted_effects/'+file))):
                if k=='set_country_flag' and isinstance(v,list) and first(v,'days'):
                    self.assertEqual(first(v,'value'),'1')

if __name__=='__main__':unittest.main(verbosity=2)
