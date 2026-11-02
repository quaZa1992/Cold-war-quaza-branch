# IMPERIA COLD WAR — Independent emitted-AST tests for Kissinger statecraft.
"""Bounded source interpreter. This does not run HOI4 or prove native delivery.

Read the installed effects and triggers; never run a content generator. Unknown
effects and conditions fail closed in an exercised path instead of being treated
as successes. Native startup, unit creation and war execution remain outside
this interpreter and require separate engine evidence.
"""
from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from decimal import Decimal as D, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from focus_prerequisite_ui import nodes,field

P='COLDWAR_USA_KS_'
STEM='COLDWAR_USA_kissinger'
REPORT=ROOT/'docs/design/usa_kissinger_20261028/IMPLEMENTATION_VALIDATION_MODEL.json'


def children(items,key,default=None):
    found=next((n for n in items if n.key==key),None)
    return found.children() if found else ([] if default is None else default)


def descendants(items):
    for node in items:
        yield node
        yield from descendants(node.children())


class Model:
    """Only the native constructs exercised by the bounded transaction tests."""
    def __init__(self):
        self.effects={n.key:n.children() for n in nodes((ROOT/f'common/scripted_effects/{STEM}.txt').read_text(encoding='utf-8-sig'))}
        self.triggers={n.key:n.children() for n in nodes((ROOT/f'common/scripted_triggers/{STEM}.txt').read_text(encoding='utf-8-sig'))}
        donor=ROOT/'common/scripted_triggers/COLDWAR_USA_gulf_triggers.txt'
        self.triggers.update({n.key:n.children() for n in nodes(donor.read_text(encoding='utf-8-sig'))})
        donor=ROOT/'common/scripted_triggers/COLDWAR_IRQ_1970_triggers.txt'
        self.triggers.update({n.key:n.children() for n in nodes(donor.read_text(encoding='utf-8-sig'))})
        # IMPERIA COLD WAR — Real treaty predicates are now cross-feature dependencies.
        for donor in (ROOT/'common/scripted_triggers').glob('ICW_superpower*.txt'):
            self.triggers.update({n.key:n.children() for n in nodes(donor.read_text(encoding='utf-8-sig'))})
        self.countries={}
        for tag in ('USA','IRQ','PER','TUR','SYR','KUR','PUK','KPI','KPT','KPS','CHI','SOV','UNI','CHL'):
            self.countries[tag]=dict(tag=tag,alive=tag not in ('KUR','PUK','KPI','KPT','KPS'),
                vars=defaultdict(D,treasury=D(100),gdp_total=D(100)),temp=defaultdict(D),
                flags=set(),ideas=set(),wars=set(),embargo=set(),focuses=set(),arrays={},dynamic=False,missions=set(),
                equipment=defaultdict(D,infantry_weapons_1=D(10000)),divisions={},opinions={},events=[],dirty=0,subject=False,timed_ideas={},opinion_modifiers=[])
        self.states={}
        for tag,states in {'IRQ':[164,633,630,1078],'PER':[408],'TUR':[162],'SYR':[193]}.items():
            for sid in states:self.states[sid]=dict(id=sid,owner=tag,controller=tag,fully_controlled=True,population=D(1000000),cores={tag},flags=set(),vars=defaultdict(D),temp=defaultdict(D),resistance=D(0),resistance_targets=set())
        self.neighbours={frozenset((a,b)) for a,b in [('IRQ','PER'),('IRQ','TUR'),('IRQ','SYR'),('PER','TUR'),('SYR','TUR')]}
        self.stack=[];self.root=None;self.scenario=True
        # Fixture setup invokes the emitted fiscal provider. Rates are never
        # injected into model defaults or imported from the content generator.
        for tag in self.countries:self.call(P+'refresh_fiscal',tag)

    def target(self,name):
        if name in ('THIS','SELF'):return self.stack[-1] if self.stack else self.root
        if name=='ROOT':return self.root
        if name=='PREV':return self.stack[-2] if len(self.stack)>1 else None
        if name in self.countries:return self.countries[name]
        if str(name).isdigit():return self.states.get(int(name))
        return None

    def value(self,value,scope):
        value=str(value)
        try:return D(value)
        except Exception:pass
        if '.' in value:
            tag,name=value.split('.',1)
            target=self.target(tag)
            if target is not None:return self.value(name,target)
        if value in scope['temp']:return scope['temp'][value]
        return scope['vars'].get(value,D(0))

    def cmp(self,left,op,right):
        return {'>':left>right,'<':left<right,'=':left==right,'>=':left>=right,'<=':left<=right,'!=':left!=right}[op]

    def cond(self,items,scope):
        push=not self.stack or self.stack[-1] is not scope
        if push:self.stack.append(scope)
        try:
            for n in items:
                key,op,value=n.key,n.op,n.value;body=n.children()
                if key in ('tooltip','log'):continue
                if key in self.triggers:ok=self.cond(self.triggers[key],scope)==(value=='yes')
                elif key=='OR':ok=any(self.cond([x],scope) for x in body)
                elif key=='NOT':ok=not self.cond(body,scope)
                elif key in ('AND','hidden_trigger','custom_trigger_tooltip'):ok=self.cond(body,scope)
                elif key=='always':ok=value=='yes'
                elif key=='IMP_is_1970_scenario':ok=self.scenario==(value=='yes')
                elif key in ('tag','original_tag'):ok=scope.get('tag')==value
                elif key=='is_dynamic_country':ok=scope['dynamic']==(value=='yes')
                elif key=='exists':ok=scope.get('alive',False)==(value=='yes')
                elif key=='country_exists':ok=bool(self.countries[value]['alive'])
                elif key=='has_country_flag':ok=value in scope['flags']
                elif key=='has_active_mission':ok=value in scope['missions']
                elif key=='has_state_flag':ok=value in scope['flags']
                elif key=='has_resistance':ok=(scope['resistance']>0)==(value=='yes')
                elif key=='resistance':ok=self.cmp(scope['resistance'],op,D(value))
                elif key=='has_idea':ok=value in scope['ideas']
                elif key=='has_completed_focus':ok=value in scope['focuses']
                elif key=='has_war_with':ok=value in scope['wars']
                elif key=='has_war':ok=bool(scope['wars'])==(value=='yes')
                elif key=='is_subject':ok=scope['subject']==(value=='yes')
                elif key=='is_embargoing':ok=value in scope['embargo']
                elif key=='has_equipment':ok=all(self.cmp(scope['equipment'][x.key],x.op,D(x.value)) for x in body)
                elif key=='is_in_array':
                    array=field(body,'array');target=field(body,'value')
                    if array is None:array,target=body[0].key,body[0].value
                    target=self.target(target)['tag'] if self.target(target) else target
                    ok=target in scope['arrays'].get(array,set())
                elif key=='check_variable':
                    if field(body,'var') is not None:
                        ident=field(body,'var');right=field(body,'value');sign=field(body,'compare')
                        signs={'greater_than':'>','less_than':'<','greater_than_or_equals':'>=','less_than_or_equals':'<=','equals':'=','not_equals':'!='}
                        ok=self.cmp(self.value(ident,scope),signs[sign],self.value(right,scope))
                    else:
                        x=next(x for x in body if x.key!='tooltip')
                        assert x.op in ('=','>','<'),('Native check_variable shorthand is unsupported',x.op)
                        ok=self.cmp(self.value(x.key,scope),x.op,self.value(x.value,scope))
                elif key=='num_divisions_in_states':
                    states=[int(x.value) for x in children(body,'states')]
                    count=sum(scope['divisions'].get(s,0) for s in states)
                    x=next(x for x in body if x.key=='count');ok=self.cmp(D(count),x.op,D(x.value))
                elif key in ('any_owned_state','any_controlled_state'):
                    owner='owner' if key=='any_owned_state' else 'controller'
                    ok=any(s[owner]==scope['tag'] and self.cond(body,s) for s in self.states.values())
                elif key=='is_owned_and_controlled_by':ok=scope['owner']==value and scope['controller']==value
                elif key=='is_fully_controlled_by':ok=scope['controller']==value and scope['fully_controlled']
                elif key=='is_controlled_by':ok=scope['controller']==self.target(value)['tag'] if self.target(value) else False
                elif key=='is_owned_by':ok=scope['owner']==value
                elif key=='state':ok=scope['id']==int(value)
                elif key=='state_population':ok=self.cmp(scope['population'],op,D(value))
                elif key=='is_neighbor_of':ok=frozenset((scope['tag'],value)) in self.neighbours
                elif key=='has_opinion':
                    x=next(x for x in body if x.key=='value')
                    ok=self.cmp(D(scope['opinions'].get(field(body,'target'),0)),x.op,D(x.value))
                elif self.target(key) is not None:ok=self.cond(body,self.target(key))
                else:raise AssertionError(('Unmodelled condition',key,op,value))
                if not ok:return False
            return True
        finally:
            if push:self.stack.pop()

    def run(self,items,scope):
        push=not self.stack or self.stack[-1] is not scope
        if push:self.stack.append(scope)
        try:
            branch=False
            for n in items:
                key,value=n.key,n.value;body=n.children()
                if key=='if':
                    branch=self.cond(children(body,'limit'),scope)
                    if branch:self.run([x for x in body if x.key!='limit'],scope)
                    continue
                if key=='else_if':
                    if not branch and self.cond(children(body,'limit'),scope):
                        self.run([x for x in body if x.key!='limit'],scope);branch=True
                    continue
                if key=='else':
                    if not branch:self.run(body,scope)
                    branch=True;continue
                branch=False
                if key in ('effect_tooltip','custom_effect_tooltip','unlock_decision_tooltip','log'):continue
                if key=='hidden_effect':self.run(body,scope)
                elif key in self.effects:self.run(self.effects[key],scope)
                elif key in ('set_variable','set_temp_variable','add_to_variable','add_to_temp_variable','subtract_from_variable','subtract_from_temp_variable','multiply_variable','multiply_temp_variable','divide_variable','divide_temp_variable'):
                    values=scope['temp'] if 'temp_variable' in key else scope['vars']
                    x=next(x for x in body if x.key!='tooltip');right=self.value(x.value,scope)
                    if key.startswith('set_'):values[x.key]=right
                    elif key.startswith('add_'):values[x.key]+=right
                    elif key.startswith('subtract_'):values[x.key]-=right
                    elif key.startswith('multiply_'):values[x.key]*=right
                    else:values[x.key]/=right
                elif key=='clamp_variable':
                    ident=field(body,'var');left=self.value(ident,scope)
                    if field(body,'min') is not None:left=max(left,D(field(body,'min')))
                    if field(body,'max') is not None:left=min(left,D(field(body,'max')))
                    scope['vars'][ident]=left
                elif key=='round_variable':
                    # Installed effects_documentation.md documents the scalar
                    # form. Exercised UI values avoid ties; this test makes no
                    # claim about native half-integer rounding edge cases.
                    self.assert_ui_round_only(value)
                    scope['vars'][value]=self.value(value,scope).quantize(D(1),rounding=ROUND_HALF_UP)
                elif key=='set_country_flag':scope['flags'].add(field(body,'flag') if body else value)
                elif key=='clr_country_flag':scope['flags'].discard(value)
                elif key=='add_ideas':scope['ideas'].add(value)
                elif key=='add_stability':scope['vars']['stability']+=D(value)
                elif key=='add_manpower':
                    if 'id' in scope:scope['population']+=self.value(value,scope)
                    else:scope['vars']['manpower']+=self.value(value,scope)
                elif key=='add_timed_idea':
                    ident=field(body,'idea');scope['ideas'].add(ident);scope['timed_ideas'][ident]=int(field(body,'days'))
                elif key=='remove_ideas':scope['ideas'].discard(value)
                elif key=='add_opinion_modifier':scope['opinion_modifiers'].append((field(body,'target'),field(body,'modifier')))
                elif key in ('add_to_array','remove_from_array'):
                    array=field(body,'array');target=field(body,'value')
                    if array is None:array,target=body[0].key,body[0].value
                    target=self.target(target)['tag'] if self.target(target) else target
                    collection=scope['arrays'].setdefault(array,set())
                    collection.add(target) if key=='add_to_array' else collection.discard(target)
                elif key=='clear_array':scope['arrays'][value]=set()
                elif key=='add_political_power':scope['vars']['political_power']+=self.value(value,scope)
                elif key=='add_equipment_to_stockpile':scope['equipment'][field(body,'type')]+=self.value(field(body,'amount'),scope)
                elif key=='modify_treasury_effect':
                    # The installed native provider is separately checked by
                    # validate.py: guard MD_skip_treasury_cost, add treasury_change.
                    if 'MD_skip_treasury_cost' not in scope['flags']:
                        scope['vars']['treasury']+=self.value('treasury_change',scope);scope['dirty']+=1
                elif key=='update_money_dirty_variable':scope['dirty']+=1
                elif key=='country_event':scope['events'].append(field(body,'id'))
                elif key=='remove_resistance_target':scope['resistance_targets'].discard(int(value))
                elif key=='every_country':
                    # Only the one-off international incident dispatch is
                    # exercised here; this is not a world-tick performance test.
                    for country in self.countries.values():
                        if country['alive'] and self.cond(children(body,'limit'),country):
                            self.run([x for x in body if x.key!='limit'],country)
                elif key=='for_each_scope_loop':raise AssertionError('Scoped array loop not modelled in bounded country test')
                elif self.target(key) is not None:self.run(body,self.target(key))
                else:raise AssertionError(('Unmodelled effect',key,value))
        finally:
            if push:self.stack.pop()

    def call(self,key,tag='USA'):
        self.root=self.countries[tag]
        self.run(self.effects[key],self.root)
        assert not self.stack

    def trigger(self,key,tag='USA'):
        self.root=self.countries[tag]
        result=self.cond(self.triggers[key],self.root)
        assert not self.stack
        return result

    def authorise_route(self):
        self.countries['USA']['flags'].update({P+'deal_irq_anatolia_signed',P+'deal_irq_transit_signed'})

    @staticmethod
    def assert_ui_round_only(value):
        assert value==P+'ui_unrest',('Unreviewed rounding field',value)

    def decide(self,key,tag):
        self.root=self.countries[tag]
        self.run(children(decision_node(P+key).children(),'complete_effect'),self.root)
        assert not self.stack

    def decision_ai_weight(self,key,tag):
        body=children(decision_node(P+key).children(),'ai_will_do')
        weight=D(field(body,'factor','1'));self.root=self.countries[tag]
        for node in body:
            if node.key=='modifier' and self.cond([x for x in node.children() if x.key!='factor'],self.root):
                weight*=D(field(node.children(),'factor','1'))
        assert not self.stack
        return weight

    def state_snapshot(self):return deepcopy(self.countries)


class RuntimeTests(unittest.TestCase):
    def model(self):return Model()

    def test_underground_funding_and_pressure_work_before_any_kurdish_country_exists(self):
        for region,tag,fund in [('irq','IRQ','irq_fund'),('per','PER','irn_fund'),('tur','TUR','tur_networks'),('syr','SYR','syr_voice')]:
            with self.subTest(region=region):
                m=self.model();m.authorise_route();us=m.countries['USA'];host=m.countries[tag]
                us['flags'].update({P+'contact_'+region,P+'breach_'+region})
                m.call(P+'complete_'+fund);self.assertEqual(us['vars'][P+'stage_'+region],2)
                before=host['vars'][P+'unrest'];organisation=host['vars'][P+'organisation'];money=us['vars']['treasury']
                m.decide(region+'_finance_networks','USA')
                self.assertEqual(host['vars'][P+'organisation'],organisation+15)
                self.assertEqual(host['vars'][P+'unrest'],before+5)
                self.assertEqual(us['vars']['treasury'],money-D('.0005'))
                self.assertIn(P+'underground_'+region+'_2',us['ideas'])
                us['vars'][P+'weekly_expense']=D(0);m.call(P+'regional_streams');self.assertEqual(us['vars'][P+'weekly_expense'],D('.00002'))
                m.call(P+'tick_'+region,tag);self.assertGreater(host['vars'][P+'unrest'],before+5)
                self.assertFalse(any(m.countries[t]['alive'] for t in ('KUR','PUK','KPI','KPT','KPS')))
                self.assertFalse(any(m.countries[t]['vars'][P+'weekly_income'] for t in ('KUR','PUK','KPI','KPT','KPS')))

    def test_network_operation_rechecks_price_and_has_a_real_cooldown(self):
        m,us,host=self.regional_compact();host['flags'].discard(P+'domestic_rights_signed');m.call(P+'reconcile_domestic','PER')
        host['vars']['treasury']=D(100);us['vars']['gdp_total']=D(200);us['vars']['treasury']=D('.00075')
        before=host['vars'][P+'organisation'];m.call(P+'per_finance_networks')
        self.assertEqual(host['vars'][P+'organisation'],before);self.assertEqual(us['vars']['treasury'],D('.00075'))
        us['vars']['treasury']=D(1);m.call(P+'per_finance_networks');self.assertEqual(host['vars'][P+'organisation'],before+15)
        after=m.state_snapshot();m.call(P+'per_finance_networks');self.assertEqual(m.countries,after)
        for _ in range(13):m.call(P+'tick_per','PER')
        self.assertEqual(host['vars'][P+'network_cooldown'],0)
        before=host['vars'][P+'organisation'];m.call(P+'per_finance_networks');self.assertEqual(host['vars'][P+'organisation'],before+15)

    def test_arming_cells_strengthens_the_host_region_without_minting_a_country(self):
        for region,tag,state,actor in [('irq','IRQ',164,'KUR'),('per','PER',408,'KPI'),('tur','TUR',162,'KPT'),('syr','SYR',193,'KPS')]:
            with self.subTest(region=region):
                m,us,host=self.regional_compact(region,tag,(state,));host['flags'].discard(P+'domestic_rights_signed');m.call(P+'reconcile_domestic',tag)
                before=host['vars'][P+'organisation'];unrest=host['vars'][P+'unrest'];equipment=us['equipment']['infantry_weapons_1']
                others={t:deepcopy(m.countries[t]) for t in ('IRQ','PER','TUR','SYR') if t!=tag}
                m.decide(region+'_resupply','USA')
                self.assertEqual(host['vars'][P+'organisation'],before+5);self.assertEqual(host['vars'][P+'unrest'],unrest+3)
                self.assertEqual(us['equipment']['infantry_weapons_1'],equipment-1000);self.assertEqual(us['vars'][P+'cache_'+region],1000)
                self.assertFalse(m.countries[actor]['alive']);self.assertNotIn(P+'partner_'+region,m.countries[actor]['flags'])
                for t,snapshot in others.items():self.assertEqual(m.countries[t],snapshot,t)

    def test_funded_deployment_can_contain_a_prestate_armed_campaign(self):
        m,us,host=self.regional_compact();host['flags'].discard(P+'domestic_rights_signed');m.call(P+'reconcile_domestic','PER')
        host['vars'][P+'unrest']=D(75);host['vars'][P+'stabilisation']=D(70)
        m.decide('per_security','PER')
        for _ in range(20):m.call(P+'tick_per','PER')
        self.assertLess(host['vars'][P+'unrest'],75);self.assertNotIn(P+'warning',host['flags']);self.assertFalse(m.countries['KPI']['alive'])

    def test_international_report_reaches_every_existing_country_once(self):
        m,us,host=self.regional_compact('irq','IRQ',(164,633,630,1078))
        m.countries['KUR']['alive']=True;host['divisions'][164]=4;host['vars'][P+'unrest']=D(100)
        # The first state is ineligible. Report the actual second-state loss.
        m.states[164]['fully_controlled']=False
        m.decide('irq_repression','IRQ')
        self.assertEqual(host['vars'][P+'incident_state'],633)
        for tag,country in m.countries.items():
            expected='COLDWAR_USA_KS.'+str(210 if tag=='IRQ' else 220 if tag=='USA' else 230 if tag in ('KUR','PUK') else 240)
            if country['alive']:self.assertEqual(country['events'].count(expected),1,tag)
            else:self.assertFalse(country['events'],tag)
        before=m.state_snapshot();m.decide('irq_repression','IRQ');self.assertEqual(m.countries,before)

    def test_failed_crackdown_has_no_population_loss_or_world_report(self):
        m,us,host=self.regional_compact();host['divisions'][408]=4;host['vars'][P+'unrest']=D(100);host['vars']['treasury']=D('3.99')
        before=m.state_snapshot();population=deepcopy(m.states);m.decide('per_repression','PER')
        self.assertEqual(m.countries,before);self.assertEqual(m.states,population)

    def test_absent_former_payee_restores_the_underground_budget_display(self):
        m=self.model();m.authorise_route();us=m.countries['USA'];kur=m.countries['KUR']
        us['vars'][P+'stage_irq']=D(2);us['arrays'][P+'payees_irq']={'KUR'};kur['alive']=True;kur['flags'].add(P+'partner_irq')
        m.call(P+'reconcile_aid');self.assertIn(P+'aid_irq_kur_2_usa',us['ideas']);self.assertNotIn(P+'underground_irq_2',us['ideas'])
        kur['alive']=False;m.call(P+'reconcile_aid')
        self.assertNotIn(P+'aid_irq_kur_2_usa',us['ideas']);self.assertIn(P+'underground_irq_2',us['ideas'])

    def regional_compact(self,region='per',tag='PER',states=(408,)):
        m=self.model();m.authorise_route();us=m.countries['USA'];host=m.countries[tag]
        us['flags'].update({P+'contact_'+region,P+'breach_'+region})
        us['vars'][P+'stage_'+region]=D(3);us['vars'][P+'max_stage_'+region]=D(3)
        m.call(P+'init_'+region);host['vars'][P+'unrest']=D(0);host['vars'][P+'stabilisation']=D(80)
        host['divisions'][states[0]]=2;m.call(P+'refresh_host',tag)
        m.decide(region+'_autonomy',tag);m.decide(region+'_investment',tag)
        return m,us,host

    def test_all_hosts_can_see_their_localised_regional_decisions(self):
        loc=(ROOT/f'localisation/english/{STEM}_l_english.yml').read_text(encoding='utf-8-sig')
        categories=nodes((ROOT/f'common/decisions/categories/{STEM}.txt').read_text(encoding='utf-8-sig'))
        for region,tag,states in [('irq','IRQ',(164,633,630,1078)),('per','PER',(408,)),('tur','TUR',(162,)),('syr','SYR',(193,))]:
            m,us,host=self.regional_compact(region,tag,states)
            category=next(n for n in categories if n.key==P+'region_'+region)
            m.root=host;self.assertTrue(m.cond(children(category.children(),'visible'),host))
            for suffix in ('security','investment','autonomy','consolidate'):
                key=P+region+'_'+suffix;choice=decision_node(key)
                m.root=host;self.assertTrue(m.cond(children(choice.children(),'visible'),host))
                self.assertIn(' '+key+':',loc);self.assertIn(' '+key+'_desc:',loc)

    def test_compact_requires_full_ten_year_progress_and_cannot_repeat_payment(self):
        for region,tag,states in [('irq','IRQ',(164,633,630,1078)),('per','PER',(408,)),('tur','TUR',(162,)),('syr','SYR',(193,))]:
            with self.subTest(region=region):
                m,us,host=self.regional_compact(region,tag,states)
                for _ in range(519):m.call(P+'tick_'+region,tag)
                before=host['vars']['treasury'];m.decide(region+'_consolidate',tag)
                self.assertNotIn(P+'pacified',host['flags']);self.assertEqual(host['vars']['treasury'],before)
                m.call(P+'tick_'+region,tag);self.assertEqual(host['vars'][P+'reconciliation_weeks'],520)
                m.decide(region+'_consolidate',tag)
                self.assertIn(P+'pacified',host['flags']);self.assertIn(P+'consolidated_compact',host['ideas'])
                self.assertEqual(host['vars']['treasury'],before-10)
                m.decide(region+'_consolidate',tag);self.assertEqual(host['vars']['treasury'],before-10)
                host['divisions'].clear();host['flags'].discard(P+'investment')
                for _ in range(52):m.call(P+'tick_'+region,tag)
                self.assertEqual(host['vars'][P+'unrest'],0);self.assertIn(P+'pacified',host['flags'])

    def test_compact_progress_loses_ground_when_each_required_policy_is_abandoned(self):
        for failure in ('troops','investment','rights','unrest','stabilisation','territory','war'):
            with self.subTest(failure=failure):
                m,us,host=self.regional_compact();host['vars'][P+'qualifying_weeks']=D(100);m.call(P+'reconciliation_total','PER')
                if failure=='troops':host['divisions'][408]=1
                elif failure=='investment':host['flags'].discard(P+'investment')
                elif failure=='rights':m.decide('per_end_rights','PER')
                elif failure=='unrest':host['vars'][P+'unrest']=D(100)
                elif failure=='stabilisation':host['vars'][P+'stabilisation']=D(0)
                elif failure=='territory':m.states[408]['fully_controlled']=False
                else:host['wars'].add('USA')
                m.call(P+'peace_tick_per','PER');self.assertEqual(host['vars'][P+'reconciliation_weeks'],98)

    def test_foreign_pressure_is_paid_once_and_invalid_transactions_are_inert(self):
        for failure in ('cash','weapons','paused','route','wrong_actor','guarantee'):
            m,us,host=self.regional_compact()
            if failure=='cash':us['vars']['treasury']=D('.00249')
            elif failure=='weapons':us['equipment']['infantry_weapons_1']=D(999)
            elif failure=='paused':us['vars'][P+'stage_per']=D(0)
            elif failure=='route':us['flags'].difference_update({P+'deal_irq_anatolia_signed',P+'deal_irq_transit_signed'})
            elif failure=='guarantee':us['flags'].add(P+'deal_irn_rights_signed')
            before=m.state_snapshot();m.call(P+'per_intensify','PER' if failure=='wrong_actor' else 'USA')
            self.assertEqual(m.countries,before,failure)
        m,us,host=self.regional_compact();us['vars']['treasury']=D('.0025')
        m.call(P+'calculate_streams');baseline=us['vars'][P+'weekly_expense']
        weapons=us['equipment']['infantry_weapons_1'];m.call(P+'per_intensify')
        self.assertEqual(us['vars']['treasury'],0);self.assertEqual(us['equipment']['infantry_weapons_1'],weapons-1000)
        self.assertEqual(us['vars'][P+'cache_per'],1000);self.assertEqual(host['vars'][P+'pressure_weeks'],26)
        before=m.state_snapshot();m.call(P+'per_intensify');self.assertEqual(m.countries,before)
        self.assertFalse(m.trigger(P+'settlement_protects_per'));m.call(P+'calculate_streams')
        self.assertEqual(us['vars'][P+'weekly_expense']-baseline,D('.00025'))
        for _ in range(26):m.call(P+'tick_per','PER')
        self.assertEqual(host['vars'][P+'pressure_weeks'],0);self.assertTrue(m.trigger(P+'settlement_protects_per'))

    def test_deployment_controls_pressure_but_neglect_can_reopen_a_consolidated_region(self):
        m,us,host=self.regional_compact();host['vars'][P+'qualifying_weeks']=D(520);m.call(P+'reconciliation_total','PER')
        host['vars'][P+'stabilisation']=D(100);m.decide('per_consolidate','PER')
        m.call(P+'per_intensify')
        for _ in range(26):m.call(P+'tick_per','PER')
        self.assertEqual(host['vars'][P+'unrest'],0);self.assertIn(P+'pacified',host['flags'])
        self.assertFalse(m.countries['KPI']['alive'])
        host['divisions'].clear();m.decide('per_end_programme','PER')
        for _ in range(2):
            m.call(P+'per_intensify')
            for _ in range(26):m.call(P+'tick_per','PER')
        self.assertNotIn(P+'pacified',host['flags']);self.assertGreater(host['vars'][P+'unrest'],79)
        self.assertFalse(m.countries['KPI']['alive'])
        host['divisions'][408]=2;m.decide('per_security','PER')
        for _ in range(26):m.call(P+'tick_per','PER')
        self.assertEqual(host['vars'][P+'unrest'],0);self.assertNotIn(P+'mobilisation_ready',host['flags'])

    def test_progress_and_surge_stay_in_their_own_country_and_keep_local_consent(self):
        m,us,host=self.regional_compact();host['vars'][P+'qualifying_weeks']=D(100);m.call(P+'reconciliation_total','PER')
        other=deepcopy(m.countries['TUR']);m.call(P+'per_intensify');m.call(P+'tick_per','PER')
        self.assertEqual(host['vars'][P+'reconciliation_weeks'],98);self.assertEqual(m.countries['TUR'],other)
        self.assertNotIn(P+'participate_per',m.countries['KPI']['flags'])
        self.assertNotIn(P+'partner_per',m.countries['KPI']['flags'])

    def test_four_costly_reforms_reduce_ten_year_route_to_six_but_never_below_it(self):
        m,us,host=self.regional_compact();initial=host['vars']['treasury']
        steps={52:'rights_charter',104:'revenue',156:'integration',208:'reconstruction'}
        for week in range(1,313):
            m.call(P+'tick_per','PER')
            if week in steps:
                key='per_reform_'+steps[week];m.decide(key,'PER')
                before=host['vars']['treasury'];m.decide(key,'PER');self.assertEqual(host['vars']['treasury'],before)
            if week==311:
                self.assertEqual(host['vars'][P+'reconciliation_weeks'],519)
                before=host['vars']['treasury'];m.decide('per_consolidate','PER')
                self.assertNotIn(P+'pacified',host['flags']);self.assertEqual(host['vars']['treasury'],before)
        self.assertEqual(host['vars'][P+'reform_credit'],208)
        self.assertEqual(host['vars']['treasury'],initial-55)
        m.decide('per_consolidate','PER');self.assertIn(P+'pacified',host['flags'])
        self.assertEqual(host['vars']['treasury'],initial-65)

    def test_reform_guard_rejects_wrong_sequence_insufficient_funds_and_a_surge(self):
        m,us,host=self.regional_compact();host['vars'][P+'qualifying_weeks']=D(208)
        before=m.state_snapshot();m.decide('per_reform_revenue','PER');self.assertEqual(m.countries,before)
        host['vars']['treasury']=D('9.999');before=m.state_snapshot()
        m.decide('per_reform_rights_charter','PER');self.assertEqual(m.countries,before)
        host['vars']['treasury']=D(100);m.call(P+'per_intensify');before=m.state_snapshot()
        m.decide('per_reform_rights_charter','PER');self.assertEqual(m.countries,before)

    def test_repression_removes_population_once_breaks_rights_and_notifies_the_right_players(self):
        for region,tag,state,local in [('irq','IRQ',164,'KUR'),('per','PER',408,'KPI'),('tur','TUR',162,'KPT'),('syr','SYR',193,'KPS')]:
            for policy,loss in [('emergency',1000),('repression',10000)]:
                with self.subTest(region=region,policy=policy):
                    m,us,host=self.regional_compact(region,tag,(state,));m.countries[local]['alive']=True
                    host['divisions'][state]=4;host['vars'][P+'unrest']=D(100)
                    host['vars'][P+'qualifying_weeks']=D(200);m.call(P+'reconciliation_total',tag)
                    original=sum(s['population'] for s in m.states.values());before=host['vars']['treasury']
                    m.decide(region+'_'+policy,tag)
                    self.assertEqual(sum(s['population'] for s in m.states.values()),original-loss)
                    self.assertEqual(host['vars'][P+'civilian_losses'],loss)
                    self.assertEqual(host['vars']['treasury'],before-(2 if policy=='emergency' else 4))
                    self.assertFalse(m.trigger(P+'rights_'+region,tag));self.assertNotIn(P+'pacified',host['flags'])
                    self.assertIn(P+'repression_legacy',host['ideas']);self.assertFalse(m.trigger(P+'reconciliation_conditions_'+region,tag))
                    index=('irq','per','tur','syr').index(region)
                    self.assertIn('COLDWAR_USA_KS.'+str(210+index),host['events'])
                    self.assertIn('COLDWAR_USA_KS.'+str(220+index),us['events'])
                    self.assertIn('COLDWAR_USA_KS.'+str(230+index),m.countries[local]['events'])
                    before=m.state_snapshot();population=deepcopy(m.states)
                    m.decide(region+'_'+policy,tag);self.assertEqual(m.countries,before);self.assertEqual(m.states,population)
                    for _ in range(156):m.call(P+'repression_tick',tag)
                    self.assertEqual(host['vars'][P+'trauma_weeks'],0);self.assertNotIn(P+'repression_legacy',host['ideas'])

    def test_repression_requires_real_troops_territory_population_and_payment(self):
        for failure in ('troops','territory','population','cash','wrong_actor'):
            m,us,host=self.regional_compact();host['divisions'][408]=4;host['vars'][P+'unrest']=D(100)
            if failure=='troops':host['divisions'][408]=3
            elif failure=='territory':m.states[408]['fully_controlled']=False
            elif failure=='population':m.states[408]['population']=D(10000)
            elif failure=='cash':host['vars']['treasury']=D('3.99')
            before=m.state_snapshot();population=deepcopy(m.states)
            m.call(P+'per_repression','USA' if failure=='wrong_actor' else 'PER')
            self.assertEqual(m.countries,before,failure);self.assertEqual(m.states,population,failure)

    def test_host_setup_uses_current_gdp_at_payment_even_after_the_quote_changes(self):
        m=self.model();host=m.countries['PER'];host['flags'].add(P+'tracked');host['divisions'][408]=2
        m.call(P+'refresh_host','PER');host['vars']['gdp_total']=D(200);host['vars']['treasury']=D(3)
        m.call(P+'per_security','PER')
        self.assertEqual(host['vars']['treasury'],3);self.assertNotIn(P+'security',host['flags'])
        host['vars']['treasury']=D(4);m.call(P+'per_security','PER')
        self.assertEqual(host['vars']['treasury'],0);self.assertIn(P+'security',host['flags'])

    def test_us_escalation_rechecks_live_gdp_without_charging_or_minting_assets(self):
        m,us,host=self.regional_compact();us['vars']['treasury']=D('.003')
        us['vars']['gdp_total']=D(200)  # old quote 0.0025, current price 0.005
        equipment=us['equipment']['infantry_weapons_1'];m.call(P+'per_intensify')
        self.assertEqual(us['vars']['treasury'],D('.003'));self.assertEqual(us['equipment']['infantry_weapons_1'],equipment)
        self.assertEqual(us['vars'][P+'cache_per'],0);self.assertEqual(host['vars'][P+'pressure_weeks'],0)

    def test_host_weekly_costs_scale_with_gdp_and_recalculation_does_not_compound(self):
        m=self.model();host=m.countries['PER'];host['flags'].update({P+'tracked',P+'security'})
        host['vars']['gdp_total']=D(40);m.call(P+'calculate_streams','PER')
        self.assertEqual(host['vars'][P+'weekly_expense'],D('.0016'))
        m.call(P+'calculate_streams','PER');self.assertEqual(host['vars'][P+'weekly_expense'],D('.0016'))
        host['vars']['gdp_total']=D(80);m.call(P+'calculate_streams','PER')
        self.assertEqual(host['vars'][P+'weekly_expense'],D('.0032'))
        host['flags'].discard(P+'security');host['flags'].update({P+'investment',P+'domestic_rights_signed'})
        m.call(P+'calculate_streams','PER');self.assertEqual(host['vars'][P+'weekly_expense'],D('.0024'))
        host['vars']['gdp_total']=D(1);m.call(P+'calculate_streams','PER')
        self.assertEqual(host['vars'][P+'weekly_expense'],D('.00003'))

    def test_assistance_uses_donor_gdp_for_both_countries_and_tracks_growth(self):
        m=self.model();m.authorise_route();us=m.countries['USA'];kur=m.countries['KUR']
        kur['alive']=True;kur['flags'].add(P+'partner_irq');kur['vars']['gdp_total']=D(1)
        m.states[164]['owner']=m.states[164]['controller']='KUR'
        us['vars']['gdp_total']=D(1000);us['vars'][P+'stage_irq']=D(2);us['arrays'][P+'payees_irq']={'KUR'}
        m.call(P+'calculate_streams');m.call(P+'calculate_streams','KUR')
        self.assertEqual(kur['vars'][P+'weekly_income'],D('.0002'))
        self.assertEqual(us['vars'][P+'week_us_funded'],kur['vars'][P+'weekly_income'])
        us['vars']['gdp_total']=D(2000);kur['vars']['gdp_total']=D(300)
        m.call(P+'calculate_streams');m.call(P+'calculate_streams','KUR')
        self.assertEqual(kur['vars'][P+'weekly_income'],D('.0004'))
        self.assertEqual(us['vars'][P+'week_us_funded'],kur['vars'][P+'weekly_income'])
        m.call(P+'calculate_streams','KUR');self.assertEqual(kur['vars'][P+'weekly_income'],D('.0004'))

    def test_transit_transfer_uses_us_gdp_and_legacy_moscow_receipts_do_not_charge(self):
        m=self.model();us=m.countries['USA'];per=m.countries['PER'];sov=m.countries['SOV']
        us['vars']['gdp_total']=D(1000);per['vars']['gdp_total']=D(10);sov['vars']['gdp_total']=D(400)
        m.call(P+'deal_irq_transit_offer');m.call(P+'deal_irq_transit_accept','PER')
        # The old consultation receipt is not consent to a new treaty programme.
        us['flags'].add(P+'deal_moscow_signed');sov['flags'].add(P+'deal_moscow_signed')
        m.call(P+'calculate_streams');m.call(P+'calculate_streams','PER');m.call(P+'calculate_streams','SOV')
        self.assertEqual(us['vars'][P+'weekly_expense'],D('.0002'))
        self.assertEqual(per['vars'][P+'weekly_income'],D('.0002'))
        self.assertEqual(sov['vars'][P+'weekly_expense'],D('0'))

    def test_committed_cash_keeps_authorisation_value_while_weekly_aid_tracks_current_gdp(self):
        m=self.model();m.authorise_route();us=m.countries['USA'];kur=m.countries['KUR']
        kur['alive']=True;kur['flags'].add(P+'partner_irq');us['flags'].add('COLDWAR_USA_gulf_programme_arm_front')
        m.states[164]['owner']=m.states[164]['controller']='KUR'
        m.call(P+'legacy_irq_start');self.assertEqual(us['vars'][P+'legacy_irq_cash'],D('.025'))
        us['vars']['gdp_total']=D(200);m.decide('irq_cache_kur','KUR')
        self.assertEqual(kur['vars']['treasury'],D('100.025'))
        m.call(P+'calculate_streams');m.call(P+'calculate_streams','KUR')
        self.assertEqual(kur['vars'][P+'weekly_income'],D('.01'))
        self.assertEqual(us['vars'][P+'week_us_legacy'],kur['vars'][P+'weekly_income'])
        before=us['vars']['treasury'];m.call(P+'legacy_irq_start');self.assertEqual(us['vars']['treasury'],before)

    def test_gdp_cost_previews_are_inert_even_when_unfunded_and_locked(self):
        m=self.model();m.countries['USA']['vars']['treasury']=D(0);m.countries['USA']['vars']['gdp_total']=D(0)
        before=m.state_snapshot()
        for key in ('preview_covert','preview_irq_fund','preview_irq_front','deal_irq_transit_preview','legacy_irq_preview'):
            m.call(P+key);self.assertEqual(m.countries,before)

    def test_runtime_has_no_fixed_nonzero_treasury_or_weekly_programme_amounts(self):
        rows=list(descendants([node for value in Model().effects.values() for node in value]))
        for node in rows:
            if node.key not in ('set_temp_variable','add_to_variable'):continue
            for pair in node.children():
                if pair.key not in ('treasury_change',P+'weekly_expense',P+'weekly_income'):continue
                try:amount=D(pair.value)
                except Exception:continue
                self.assertEqual(amount,0,(node.key,pair.key,pair.value))

    def test_offer_is_recipient_owned_and_has_no_prospective_reward_side_effect(self):
        m=self.model();m.call(P+'deal_beijing_offer')
        us=m.countries['USA'];them=m.countries['CHI']
        self.assertIn(P+'deal_beijing_pending',us['flags']);self.assertIn(P+'deal_beijing_pending',them['flags'])
        self.assertFalse(us['ideas']);self.assertFalse(them['ideas'])
        self.assertEqual(them['events'],['COLDWAR_USA_KS.1'])
        before=m.state_snapshot();m.call(P+'deal_beijing_preview');self.assertEqual(m.countries,before)

    def test_focus_treasury_cost_preserves_the_approved_negative_sign(self):
        m=self.model();m.call(P+'execute_covert')
        self.assertEqual(m.countries['USA']['vars']['treasury'],D('99.9995'))
        before=m.state_snapshot();m.call(P+'execute_covert');self.assertEqual(m.countries,before)

    def test_funding_focus_debits_real_equipment_and_money_exactly_once(self):
        m=self.model();m.authorise_route();m.countries['IRQ']['opinions']['USA']=-25
        m.call(P+'execute_irq_fund');us=m.countries['USA']
        self.assertEqual(us['vars']['treasury'],D('99.9995'))
        self.assertEqual(us['equipment']['infantry_weapons_1'],9000)
        self.assertEqual(us['vars'][P+'cache_irq'],1000)
        before=m.state_snapshot();m.call(P+'execute_irq_fund');self.assertEqual(m.countries,before)
        m=self.model();m.authorise_route();m.countries['IRQ']['opinions']['USA']=-25
        m.countries['USA']['equipment']['infantry_weapons_1']=D(999)
        m.call(P+'execute_irq_fund')
        self.assertEqual(m.countries['USA']['vars']['treasury'],100)
        self.assertEqual(m.countries['USA']['vars'].get(P+'cache_irq',0),0)

    def test_acceptance_revalidates_recipient_and_pending_before_granting(self):
        m=self.model();m.call(P+'deal_beijing_accept','CHI');self.assertFalse(m.countries['CHI']['ideas'])
        m.call(P+'deal_beijing_offer');m.call(P+'deal_beijing_accept','TUR')
        self.assertFalse(m.countries['USA']['ideas']);self.assertFalse(m.countries['TUR']['ideas'])
        m.call(P+'deal_beijing_accept','CHI')
        self.assertIn(P+'deal_beijing_usa',m.countries['USA']['ideas'])
        self.assertIn(P+'deal_beijing_partner',m.countries['CHI']['ideas'])
        before=m.state_snapshot();m.call(P+'deal_beijing_accept','CHI');self.assertEqual(m.countries,before)

    def test_refusal_leaves_no_spirit_or_charge(self):
        m=self.model();m.call(P+'deal_beijing_offer');m.call(P+'deal_beijing_end','CHI')
        for tag in ('USA','CHI'):
            self.assertNotIn(P+'deal_beijing_pending',m.countries[tag]['flags'])
            self.assertNotIn(P+'deal_beijing_signed',m.countries[tag]['flags'])
            self.assertFalse(m.countries[tag]['ideas']);self.assertEqual(m.countries[tag]['vars']['treasury'],100)

    def test_war_embargo_and_each_mirrored_sanction_block_consent(self):
        for kind in ('war','embargo',*[f'{k}_{d}' for k in ('dip','fin','eco','mil') for d in ('on','by')]):
            for side in ('USA','CHI'):
                with self.subTest(kind=kind,side=side):
                    m=self.model();m.call(P+'deal_beijing_offer');c=m.countries[side];other='CHI' if side=='USA' else 'USA'
                    if kind=='war':c['wars'].add(other)
                    elif kind=='embargo':c['embargo'].add(other)
                    else:
                        family,direction=kind.split('_')
                        c['arrays'][f'imp_{family}_sanc_{direction}_us']={other}
                    self.assertFalse(m.trigger(P+'deal_beijing_accept_valid','CHI'))
                    m.call(P+'deal_beijing_accept','CHI');self.assertFalse(m.countries['USA']['ideas'])

    def test_suspension_and_restoration_do_not_repeat_setup_assets(self):
        m=self.model();m.call(P+'deal_beijing_offer');m.call(P+'deal_beijing_accept','CHI')
        us=m.countries['USA'];us['wars'].add('CHI');m.call(P+'reconcile_deals')
        self.assertNotIn(P+'deal_beijing_usa',us['ideas']);self.assertNotIn(P+'deal_beijing_partner',m.countries['CHI']['ideas'])
        us['wars'].clear();m.call(P+'reconcile_deals');m.call(P+'reconcile_deals')
        self.assertIn(P+'deal_beijing_usa',us['ideas']);self.assertEqual(us['vars']['treasury'],100)
        self.assertEqual(us['equipment']['infantry_weapons_1'],10000)

    def test_existing_regional_actor_has_real_settlement_consent(self):
        m=self.model();actor=m.countries['KPI'];actor['alive']=True
        m.states[408]['owner']=m.states[408]['controller']='KPI'
        m.call(P+'deal_irn_rights_offer');m.call(P+'deal_irn_rights_accept','PER')
        self.assertIn(P+'rights_per_pending',actor['flags'])
        self.assertNotIn(P+'deal_irn_rights_usa',m.countries['USA']['ideas'])
        self.assertNotIn(P+'deal_irn_rights_partner',m.countries['PER']['ideas'])
        choice=decision_node(P+'rights_per_local_kpi');m.root=actor;m.run(children(choice.children(),'complete_effect'),actor)
        self.assertIn(P+'deal_irn_rights_usa',m.countries['USA']['ideas'])
        self.assertIn(P+'deal_irn_rights_partner',m.countries['PER']['ideas'])

    def test_local_refusal_closes_the_unsigned_settlement_for_renegotiation(self):
        m=self.model();actor=m.countries['KPI'];actor['alive']=True
        m.states[408]['owner']=m.states[408]['controller']='KPI'
        m.call(P+'deal_irn_rights_offer');m.call(P+'deal_irn_rights_accept','PER')
        choice=decision_node(P+'rights_per_local_kpi_decline');m.root=actor;m.run(children(choice.children(),'complete_effect'),actor)
        for tag in ('USA','PER'):
            self.assertNotIn(P+'deal_irn_rights_signed',m.countries[tag]['flags'])
            self.assertFalse(m.countries[tag]['ideas'])
        self.assertNotIn(P+'rights_per_pending',actor['flags'])
        m.countries['USA']['flags'].discard(P+'deal_irn_rights_cooldown')
        self.assertTrue(m.trigger(P+'deal_irn_rights_can_offer'))

    def test_weekly_streams_reset_do_not_compound_and_stop_when_suspended(self):
        m=self.model();m.call(P+'deal_beijing_offer');m.call(P+'deal_beijing_accept','CHI')
        m.call(P+'calculate_streams');expense=m.countries['USA']['vars'][P+'weekly_expense']
        self.assertEqual(expense,D('.00002'));m.call(P+'calculate_streams')
        self.assertEqual(m.countries['USA']['vars'][P+'weekly_expense'],expense)
        m.countries['USA']['wars'].add('CHI');m.call(P+'calculate_streams')
        self.assertEqual(m.countries['USA']['vars'][P+'weekly_expense'],0)

    def test_real_material_cache_can_only_be_delivered_once(self):
        m=self.model();m.authorise_route();us=m.countries['USA'];kur=m.countries['KUR'];kur['alive']=True
        m.states[164]['owner']=m.states[164]['controller']='KUR'
        us['vars'][P+'cache_irq']=D(1000);us['vars'][P+'stage_irq']=D(2)
        # Execute the actual decision complete_effect from installed source.
        decision=decision_node(P+'irq_cache_kur');m.root=kur;m.run(children(decision.children(),'complete_effect'),kur)
        self.assertEqual(us['vars'][P+'cache_irq'],0);self.assertEqual(kur['equipment']['infantry_weapons_1'],11000)
        m.run(children(decision.children(),'complete_effect'),kur)
        self.assertEqual(kur['equipment']['infantry_weapons_1'],11000)
        puk=m.countries['PUK'];puk['alive']=True;m.states[1078]['owner']=m.states[1078]['controller']='PUK'
        stale_choice=decision_node(P+'irq_cache_puk');m.root=puk;m.run(children(stale_choice.children(),'complete_effect'),puk)
        self.assertEqual(puk['equipment']['infantry_weapons_1'],10000)
        self.assertEqual(us['vars'][P+'cache_irq'],0)

    def test_accepted_material_grants_paired_budget_spirits_without_war_consent(self):
        m=self.model();m.authorise_route();us=m.countries['USA'];actor=m.countries['KPI'];actor['alive']=True
        m.states[408]['owner']=m.states[408]['controller']='KPI'
        us['vars'][P+'cache_per']=D(1000);us['vars'][P+'stage_per']=D(2);us['flags'].add(P+'contact_per')
        m.decide('per_cache_kpi','KPI')
        self.assertEqual(actor['equipment']['infantry_weapons_1'],10000)
        self.assertEqual(us['vars'][P+'cache_per'],1000)
        m.decide('per_liaison_kpi','KPI')
        self.assertIn(P+'partner_per',actor['flags']);self.assertNotIn(P+'participate_per',actor['flags'])
        m.decide('per_cache_kpi','KPI')
        self.assertIn(P+'aid_per_kpi_2_usa',us['ideas']);self.assertIn(P+'aid_per_kpi_2_partner',actor['ideas'])
        self.assertEqual(actor['equipment']['infantry_weapons_1'],11000)
        self.assertNotIn(P+'participate_per',actor['flags'])
        m.decide('per_participate_kpi','KPI');self.assertIn(P+'participate_per',actor['flags'])
        m.decide('per_stand_down_kpi','KPI')
        self.assertIn(P+'partner_per',actor['flags']);self.assertNotIn(P+'participate_per',actor['flags'])
        m.decide('per_end_liaison_kpi','KPI')
        self.assertNotIn(P+'aid_per_kpi_2_usa',us['ideas']);self.assertNotIn(P+'aid_per_kpi_2_partner',actor['ideas'])
        self.assertEqual(actor['equipment']['infantry_weapons_1'],11000)

    def test_suspended_material_acceptance_keeps_its_finite_cache(self):
        m=self.model();m.authorise_route();us=m.countries['USA'];actor=m.countries['KPI'];actor['alive']=True
        m.states[408]['owner']=m.states[408]['controller']='KPI'
        us['vars'][P+'cache_per']=D(1000);us['vars'][P+'stage_per']=D(2);us['flags'].add(P+'contact_per')
        m.decide('per_liaison_kpi','KPI');us['vars'][P+'stage_per']=D(0)
        m.decide('per_cache_kpi','KPI')
        self.assertEqual(actor['equipment']['infantry_weapons_1'],10000);self.assertEqual(us['vars'][P+'cache_per'],1000)
        self.assertNotIn(P+'aid_per_kpi_2_partner',actor['ideas'])

    def test_host_autonomy_remains_available_after_arms_and_requires_local_consent(self):
        for local in (False,True):
            with self.subTest(existing_local_actor=local):
                m=self.model();m.authorise_route();us=m.countries['USA'];host=m.countries['PER'];actor=m.countries['KPI']
                us['vars'][P+'stage_per']=D(3);us['focuses'].add(P+'irn_front');m.call(P+'init_per')
                if local:
                    actor['alive']=True;m.states[408]['owner']=m.states[408]['controller']='KPI'
                m.decide('per_autonomy','PER')
                self.assertEqual(host['vars']['treasury'],99)
                self.assertNotIn(P+'deal_irn_rights_signed',us['flags'])
                self.assertEqual(m.trigger(P+'rights_per','PER'),not local)
                if local:
                    self.assertIn(P+'rights_per_pending',actor['flags'])
                    self.assertNotIn(P+'domestic_rights',host['ideas'])
                    m.decide('rights_per_local_kpi','KPI')
                self.assertTrue(m.trigger(P+'rights_per','PER'))
                self.assertIn(P+'domestic_rights',host['ideas'])
                m.call(P+'calculate_streams','PER');self.assertEqual(host['vars'][P+'weekly_expense'],D('.001'))
                before=host['vars']['treasury'];m.decide('per_autonomy','PER');self.assertEqual(host['vars']['treasury'],before)
                m.decide('per_end_rights','PER');self.assertFalse(m.trigger(P+'rights_per','PER'))

    def test_campaign_cap_is_recounted_at_real_completion_before_payment(self):
        m=self.model();m.authorise_route();us=m.countries['USA']
        us['vars'][P+'stage_irq']=D(2);us['vars'][P+'stage_per']=D(2)
        us['vars'][P+'campaign_count']=D(0)
        m.call(P+'complete_tur_networks')
        self.assertEqual(us['vars'][P+'campaign_count'],2)
        self.assertEqual(us['vars'].get(P+'stage_tur',0),0)
        self.assertEqual(us['vars']['treasury'],100)
        us['focuses'].add(P+'expanded');m.call(P+'complete_tur_networks')
        self.assertEqual(us['vars'][P+'campaign_count'],3)
        self.assertEqual(us['vars'][P+'stage_tur'],2)
        self.assertEqual(us['vars']['treasury'],D('99.9998'))
        before=m.state_snapshot();m.call(P+'complete_tur_networks');self.assertEqual(m.countries,before)

    def test_legacy_gulf_setup_scales_with_donor_gdp_and_cash_cache_pays_once(self):
        m=self.model();m.authorise_route();us=m.countries['USA'];kur=m.countries['KUR'];kur['alive']=True
        m.states[164]['owner']=m.states[164]['controller']='KUR';us['flags'].add('COLDWAR_USA_gulf_programme_arm_front')
        m.call(P+'calculate_streams');baseline=us['vars'][P+'weekly_expense']
        m.call(P+'legacy_irq_start');self.assertEqual(us['vars']['treasury'],D('99.975'))
        self.assertEqual(us['vars'][P+'legacy_irq_cash'],D('.025'));self.assertEqual(us['equipment']['infantry_weapons_1'],9000)
        m.call(P+'legacy_irq_start');self.assertEqual(us['vars']['treasury'],D('99.975'))
        m.decide('irq_cache_kur','KUR');self.assertEqual(kur['vars']['treasury'],D('100.025'))
        self.assertEqual(kur['equipment']['infantry_weapons_1'],11000);self.assertNotIn(P+'participate_irq',kur['flags'])
        m.decide('irq_cache_kur','KUR');self.assertEqual(kur['vars']['treasury'],D('100.025'))
        m.call(P+'calculate_streams');m.call(P+'calculate_streams','KUR')
        self.assertEqual(us['vars'][P+'weekly_expense']-baseline,D('.005'));self.assertEqual(kur['vars'][P+'weekly_income'],D('.005'))

    def test_legacy_migration_moves_receipts_once_without_recharging_or_forcing_new_consent(self):
        m=self.model();m.authorise_route();us=m.countries['USA'];host=m.countries['IRQ'];kur=m.countries['KUR'];kur['alive']=True
        m.states[164]['owner']=m.states[164]['controller']='KUR'
        us['vars']['COLDWAR_USA_gulf_cache']=D(400);us['vars']['COLDWAR_USA_gulf_support_days']=D(300)
        us['flags'].add('COLDWAR_USA_gulf_support_kur');kur['flags'].add('COLDWAR_USA_gulf_initial_aid_received')
        host['ideas'].add('COLDWAR_USA_gulf_security_major')
        m.call(P+'migrate_irq')
        self.assertEqual(us['vars'][P+'cache_irq'],400);self.assertEqual(us['vars']['COLDWAR_USA_gulf_cache'],0)
        self.assertEqual(us['vars'][P+'delivered_irq_kur'],1000);self.assertEqual(us['vars']['COLDWAR_USA_gulf_support_days'],0)
        self.assertEqual(us['vars'][P+'legacy_irq_rate'],D(1));self.assertIn('KUR',us['arrays'][P+'payees_irq'])
        self.assertIn(P+'partner_irq',kur['flags']);self.assertNotIn(P+'participate_irq',kur['flags'])
        self.assertIn(P+'security',host['flags']);self.assertIn(P+'security_programme',host['ideas'])
        self.assertNotIn('COLDWAR_USA_gulf_security_major',host['ideas'])
        self.assertEqual(us['vars']['treasury'],100);self.assertEqual(host['vars']['treasury'],100)
        m.call(P+'migrate_irq');self.assertEqual(us['vars'][P+'cache_irq'],400)
        m.decide('irq_end_liaison_kur','KUR');m.call(P+'migrate_irq')
        self.assertNotIn(P+'partner_irq',kur['flags']);self.assertNotIn('KUR',us['arrays'][P+'payees_irq'])

    def test_legacy_gulf_recounts_campaign_cap_but_can_upgrade_an_existing_iraqi_programme(self):
        m=self.model();m.authorise_route();us=m.countries['USA'];us['flags'].add('COLDWAR_USA_gulf_programme_arm_front')
        us['vars'][P+'stage_per']=D(2);us['vars'][P+'stage_tur']=D(2);us['vars'][P+'campaign_count']=D(0)
        m.call(P+'legacy_irq_start')
        self.assertEqual(us['vars'][P+'campaign_count'],2);self.assertEqual(us['vars'].get(P+'stage_irq',0),0)
        self.assertEqual(us['vars']['treasury'],100);self.assertEqual(us['equipment']['infantry_weapons_1'],10000)
        us['vars'][P+'stage_tur']=D(0);us['vars'][P+'stage_irq']=D(2)
        m.call(P+'legacy_irq_start')
        self.assertEqual(us['vars'][P+'campaign_count'],2);self.assertEqual(us['vars'][P+'stage_irq'],3)
        self.assertEqual(us['vars']['treasury'],D('99.975'));self.assertEqual(us['equipment']['infantry_weapons_1'],9000)

    def test_accepted_regional_payee_receives_one_flow_and_hostility_suspends_it(self):
        m=self.model();m.authorise_route();us=m.countries['USA'];kur=m.countries['KUR'];kur['alive']=True
        m.states[164]['owner']=m.states[164]['controller']='KUR'
        us['vars'][P+'cache_irq']=D(1000);us['vars'][P+'stage_irq']=D(2)
        decision=decision_node(P+'irq_cache_kur');m.root=kur;m.run(children(decision.children(),'complete_effect'),kur)
        m.call(P+'calculate_streams','KUR');self.assertEqual(kur['vars'][P+'weekly_income'],D('.00002'))
        m.call(P+'calculate_streams','KUR');self.assertEqual(kur['vars'][P+'weekly_income'],D('.00002'))
        kur['wars'].add('USA');us['wars'].add('KUR')
        m.call(P+'calculate_streams','KUR');self.assertEqual(kur['vars'][P+'weekly_income'],0)

    def test_regional_recipient_can_see_its_acceptance_category(self):
        categories={n.key:n for n in nodes((ROOT/f'common/decisions/categories/{STEM}.txt').read_text(encoding='utf-8-sig'))}
        for host,central,recipients in [('irq','IRQ',['KUR','PUK']),('per','PER',['KPI']),('tur','TUR',['KPT']),('syr','SYR',['KPS'])]:
            for tag in recipients:
                with self.subTest(host=host,recipient=tag):
                    m=self.model();m.countries[central]['flags'].add(P+'tracked');m.countries[tag]['alive']=True;m.root=m.countries[tag]
                    self.assertTrue(m.cond(children(categories[P+'region_'+host].children(),'visible'),m.root))

    def test_ai_does_not_randomly_end_signed_or_pending_standing_deals(self):
        m=self.model()
        for key,tag in [('deal_irq_anatolia_terminate','TUR'),('deal_irq_anatolia_cancel','USA'),('per_end_programme','PER'),('per_pause','USA'),('per_end_liaison_kpi','KPI'),('per_stand_down_kpi','KPI'),('per_withdraw_rights_kpi','KPI'),('per_end_rights','PER')]:
            with self.subTest(decision=key):self.assertEqual(m.decision_ai_weight(key,tag),0)
        self.assertGreater(m.decision_ai_weight('per_resume','USA'),0)

    def test_ai_preserves_paid_host_plan_and_avoids_bankruptcy_without_blocking_human_switches(self):
        for region,tag,state in [('irq','IRQ',164),('per','PER',408),('tur','TUR',162),('syr','SYR',193)]:
            with self.subTest(host=tag):
                m=self.model();m.call(P+'init_'+region);host=m.countries[tag];host['divisions'][state]=2
                self.assertGreater(m.decision_ai_weight(region+'_security',tag),0)
                self.assertGreater(m.decision_ai_weight(region+'_investment',tag),0)
                host['flags'].add(P+'investment')
                self.assertEqual(m.decision_ai_weight(region+'_security',tag),0)
                m.root=host;self.assertTrue(m.cond(children(decision_node(P+region+'_security').children(),'available'),host))
                m.call(P+region+'_security',tag)
                self.assertIn(P+'security',host['flags']);self.assertNotIn(P+'investment',host['flags'])
                self.assertEqual(host['vars']['treasury'],98)
                self.assertEqual(m.decision_ai_weight(region+'_investment',tag),0)
                host['flags'].clear();host['missions'].add('bankruptcy_incoming_collapse')
                self.assertEqual(m.decision_ai_weight(region+'_security',tag),0)
                self.assertEqual(m.decision_ai_weight(region+'_investment',tag),0)

    def test_six_month_security_gains_survive_withdrawal_and_eventually_fade(self):
        m=self.model();m.authorise_route();us=m.countries['USA'];host=m.countries['PER']
        us['vars'][P+'stage_per']=D(2);us['flags'].add(P+'contact_per');m.call(P+'init_per')
        host['divisions'][408]=2;host['flags'].add(P+'security')
        for _ in range(26):m.call(P+'tick_per','PER')
        self.assertEqual(host['vars'][P+'unrest'],0);self.assertEqual(host['vars'][P+'stabilisation'],91)
        host['divisions'].clear();host['flags'].discard(P+'security')
        for _ in range(52):m.call(P+'tick_per','PER')
        self.assertEqual(host['vars'][P+'unrest'],0);self.assertGreater(host['vars'][P+'stabilisation'],50)
        for _ in range(52):m.call(P+'tick_per','PER')
        self.assertGreater(host['vars'][P+'unrest'],40);self.assertLess(host['vars'][P+'stabilisation'],25)
        for _ in range(52):m.call(P+'tick_per','PER')
        self.assertEqual(host['vars'][P+'unrest'],100);self.assertEqual(host['vars'][P+'stabilisation'],0)

    def test_invalid_security_payment_does_not_grant_programme_or_charge(self):
        for amount in (D(0),D('1.99')):
            m=self.model();host=m.countries['PER'];host['flags'].add(P+'tracked');host['divisions'][408]=2
            m.call(P+'refresh_host','PER')
            host['vars']['treasury']=amount;m.call(P+'per_security','PER')
            self.assertNotIn(P+'security',host['flags']);self.assertEqual(host['vars']['treasury'],amount)
        m=self.model();host=m.countries['PER'];host['flags'].add(P+'tracked');host['divisions'][408]=2
        m.call(P+'refresh_host','PER')
        m.call(P+'per_security','PER');self.assertIn(P+'security',host['flags']);self.assertEqual(host['vars']['treasury'],98)
        m.call(P+'per_security','PER');self.assertEqual(host['vars']['treasury'],98)
        m=self.model();host=m.countries['PER'];host['flags'].add(P+'tracked');host['divisions'][408]=2
        m.call(P+'refresh_host','PER');host['vars']['treasury']=D(2)
        m.call(P+'per_security','PER');self.assertIn(P+'security',host['flags']);self.assertEqual(host['vars']['treasury'],0)

    def test_completed_warning_is_a_manual_opportunity_and_counterplay_can_close_it(self):
        m=self.model();m.authorise_route();us=m.countries['USA'];host=m.countries['PER']
        us['vars'][P+'stage_per']=D(3);us['vars'][P+'cache_per']=D(1000);m.call(P+'init_per')
        host['vars'][P+'unrest']=D(100)
        for _ in range(14):m.call(P+'tick_per','PER')
        self.assertIn(P+'mobilisation_ready',host['flags'])
        self.assertFalse(m.countries['KPI']['alive']);self.assertEqual(m.states[408]['owner'],'PER')
        provoke=decision_node(P+'per_provoke');m.root=us
        self.assertTrue(m.cond(children(provoke.children(),'available'),us))
        m.decide('per_autonomy','PER')
        m.root=us;self.assertFalse(m.cond(children(provoke.children(),'available'),us))
        before=deepcopy(m.states);m.call(P+'uprising_per','PER');self.assertEqual(m.states,before)

    def test_country_ledgers_and_wrong_actor_are_isolated(self):
        m=self.model();m.authorise_route();m.call(P+'init_per');m.call(P+'init_tur')
        before=deepcopy(m.countries['TUR']);m.call(P+'tick_per','PER');self.assertEqual(m.countries['TUR'],before)
        before=m.state_snapshot();m.call(P+'tick_per','USA');self.assertEqual(m.countries,before)

    def test_recognition_needs_actual_regional_control_and_local_request(self):
        m=self.model();actor=m.countries['KPI'];actor['alive']=True
        actor['flags'].add(P+'recognition_requested')
        self.assertFalse(m.trigger(P+'ready_irn_claim'))
        m.states[408]['owner']=m.states[408]['controller']='KPI'
        actor['flags'].discard(P+'recognition_requested');self.assertFalse(m.trigger(P+'ready_irn_claim'))
        actor['flags'].add(P+'recognition_requested');self.assertTrue(m.trigger(P+'ready_irn_claim'))
        before=deepcopy(m.states);m.call(P+'execute_irn_claim')
        self.assertEqual(m.states,before)
        self.assertIn('KPI',m.countries['USA']['arrays']['recognised_countries'])
        self.assertIn(P+'recognised_by_usa',actor['flags'])
        self.assertEqual(m.countries['USA']['timed_ideas'][P+'recognition_cost'],180)

    def test_uprising_rechecks_warning_material_rights_and_ownership_at_execution(self):
        for host,tag,state in [('per','PER',408),('tur','TUR',162),('syr','SYR',193)]:
            with self.subTest(host=host):
                m=self.model();m.authorise_route();c=m.countries[tag];us=m.countries['USA']
                c['flags'].add(P+'tracked');c['vars'][P+'unrest']=D(100)
                c['vars'][P+'qualifying_days']=D(30);c['vars'][P+'warning_days']=D(44)
                us['vars'][P+'stage_'+host]=D(3);us['vars'][P+'cache_'+host]=D(1000)
                top=next(n for n in m.effects[P+'uprising_'+host] if n.key=='if')
                limit=children(top.children(),'limit');m.root=c
                self.assertFalse(m.cond(limit,c))
                c['vars'][P+'warning_days']=D(45);self.assertTrue(m.cond(limit,c))
                us['vars'][P+'cache_'+host]=D(999);self.assertFalse(m.cond(limit,c))
                us['vars'][P+'cache_'+host]=D(1000)
                m.states[state]['controller']='USA';self.assertFalse(m.cond(limit,c))
                m.states[state]['controller']=tag
                m.states[state]['fully_controlled']=False;self.assertFalse(m.cond(limit,c))
                m.states[state]['fully_controlled']=True;self.assertTrue(m.cond(limit,c))
                deal={'per':'irn_rights','tur':'tur_rights','syr':'syr_rights'}[host]
                us['flags'].add(P+'deal_'+deal+'_signed');self.assertFalse(m.cond(limit,c))

    def test_iraqi_provocation_requires_two_fully_controlled_main_states(self):
        m=self.model();m.authorise_route();us=m.countries['USA'];host=m.countries['IRQ']
        host['flags'].add(P+'tracked');host['vars'][P+'unrest']=D(100)
        host['vars'][P+'qualifying_days']=D(30);host['vars'][P+'warning_days']=D(45)
        us['vars'][P+'stage_irq']=D(3);us['vars'][P+'cache_irq']=D(1000)
        m.states[633]['controller']='USA';m.states[630]['controller']='USA'
        decision=decision_node(P+'irq_provoke');m.root=us
        self.assertFalse(m.cond(children(decision.children(),'available'),us))
        before=deepcopy(m.states);m.call(P+'uprising_irq','IRQ');self.assertEqual(m.states,before)
        self.assertFalse(m.countries['KUR']['alive']);self.assertEqual(us['vars'][P+'cache_irq'],1000)
        m.states[633]['controller']='IRQ';m.root=us
        self.assertTrue(m.cond(children(decision.children(),'available'),us))
        m.states[633]['fully_controlled']=False
        self.assertFalse(m.cond(children(decision.children(),'available'),us))

    def test_newborn_equipment_cleanup_cannot_touch_existing_regional_actors(self):
        for region,tag,actor in [('per','PER','KPI'),('tur','TUR','KPT'),('syr','SYR','KPS')]:
            with self.subTest(actor=actor):
                m=self.model();m.authorise_route();m.countries[actor]['alive']=True
                host=m.countries[tag];host['flags'].add(P+'tracked');host['vars'][P+'unrest']=D(100)
                host['vars'][P+'qualifying_days']=D(30);host['vars'][P+'warning_days']=D(45)
                us=m.countries['USA'];us['vars'][P+'stage_'+region]=D(3);us['vars'][P+'cache_'+region]=D(1000)
                before=m.state_snapshot();m.call(P+'uprising_'+region,tag);self.assertEqual(m.countries,before)
        for actor in ('KUR','PUK'):
            with self.subTest(actor=actor):
                m=self.model();m.countries[actor]['alive']=True;m.root=m.countries[actor]
                guards=[n for n in descendants(m.effects[P+'uprising_irq']) if n.key=='if' and any(x.key=='has_country_flag' and x.value==P+'new_'+actor.lower() for x in descendants(children(n.children(),'limit')))]
                self.assertTrue(guards)
                before=m.state_snapshot()
                for guard in guards:m.run([guard],m.countries[actor])
                self.assertEqual(m.countries,before)


def decision_node(key):
    for category in nodes((ROOT/f'common/decisions/{STEM}.txt').read_text(encoding='utf-8-sig')):
        for decision in category.children():
            if decision.key==key:return decision
    raise KeyError(key)


if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(RuntimeTests)
    names=[str(test) for test in suite]
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    inputs=[ROOT/f'common/{kind}/{STEM}.txt' for kind in ('scripted_effects','scripted_triggers','decisions')]
    inputs.extend([ROOT/f'common/decisions/categories/{STEM}.txt',ROOT/'common/scripted_triggers/COLDWAR_USA_gulf_triggers.txt',ROOT/'common/scripted_triggers/COLDWAR_IRQ_1970_triggers.txt',Path(__file__)])
    report=dict(project='IMPERIA COLD WAR',scope='Independent bounded interpreter of emitted scripts',
        tests=result.testsRun,failures=[str(t)+': '+s for t,s in result.failures],errors=[str(t)+': '+s for t,s in result.errors],
        cases=names,source_sha256={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in inputs},
        status='PASS' if result.wasSuccessful() else 'FAIL',
        limitations=['No native HOI4 execution, event delivery, unit reinforcement, UI hover or network/save/rehost test.','Country birth and war effects are statically checked separately, not simulated here.'])
    REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
