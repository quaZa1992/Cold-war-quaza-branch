# IMPERIA CW — Cold War: gulf 1970 — test abu musa.
"""Execute emitted Abu Musa scripts at native API boundaries; no HOI4 engine."""
from pathlib import Path
import copy
import datetime as dt
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'tools/vietnam_1970'))
from script_ast import parse, first, walk
import abu_musa

P = 'COLDWAR_PER_'
OUT = abu_musa.build()
E = {k:v for k,_,v in parse(OUT['common/scripted_effects/COLDWAR_PER_Abu_Musa_1970.txt'])}
T = {k:v for k,_,v in parse(OUT['common/scripted_triggers/COLDWAR_PER_Abu_Musa_1970.txt'])}
IDEA = first(first(first(parse(OUT['common/ideas/COLDWAR_PER_Abu_Musa_1970.txt']), 'ideas'), 'country'), P+'abu_musa_landing_preparations')


class World:
    def __init__(self, date='1970.1.1'):
        self.date = date
        self.exists, self.scenario, self.dynamic = {'PER','UAE','ENG'}, True, False
        self.subjects = {'PER':None,'UAE':'ENG'}
        self.v = {'PER':{}, 'UAE':{'COLDWAR_UAE_treaty_nonce':0}}
        self.f = {'PER':set(), 'UAE':{'COLDWAR_UAE_withdrawal_schedule_active','COLDWAR_UAE_historical_withdrawal_schedule'}}
        self.pp = {'PER':100., 'UAE':10.}
        self.owner = self.controller = 'UAE'
        self.ideas, self.wars, self.goals, self.opinions = {}, set(), [], []

    def day(self): return (dt.date(*map(int,self.date.split('.')))-dt.date(1970,1,1)).days

    def num(self, x, c):
        try: return float(x)
        except (ValueError, TypeError): pass
        if x == 'global.date': return self.day()*.024
        if '.' in x:
            tag,var=x.split('.',1); return self.v[tag].get(var,0)
        return self.v[c].get(x,0)

    def test(self, rows, c='PER', state=False):
        return all(self.condition(k,o,v,c,state) for k,o,v in rows)

    def condition(self,k,o,v,c,state):
        if k in {'AND','limit'}: return self.test(v,c,state)
        if k == 'OR': return any(self.condition(a,b,d,c,state) for a,b,d in v)
        if k == 'NOT': return not self.test(v,c,state)
        if k in T: return self.test(T[k],c,state) == (v=='yes')
        if k in self.exists: return self.test(v,k,state)
        if k == '1119': return self.test(v,c,True)
        if k in {'tag','original_tag'}: return c==v
        if k == 'is_dynamic_country': return self.dynamic == (v=='yes')
        if k == 'IMP_is_1970_scenario': return self.scenario == (v=='yes')
        if k == 'country_exists': return v in self.exists
        if k == 'is_subject': return bool(self.subjects[c]) == (v=='yes')
        if k == 'is_subject_of': return self.subjects[c]==v
        if k == 'has_country_flag': return v in self.f[c]
        if k == 'has_variable': return v in self.v[c]
        if k == 'has_idea': return self.ideas.get((c,v),-1)>self.day()
        if k == 'has_war_with': return (c,v) in self.wars or (v,c) in self.wars
        if k in {'is_owned_by','is_controlled_by'}: return (self.owner if k=='is_owned_by' else self.controller)==v
        if k == 'date':
            a,b=tuple(map(int,self.date.split('.'))),tuple(map(int,v.split('.')))
            return {'>':a>b,'<':a<b,'=':a==b}[o]
        if k == 'has_political_power': return {'>':self.pp[c]>float(v),'<':self.pp[c]<float(v)}[o]
        if k == 'check_variable':
            if first(v,'var'):
                a,b,op=self.num(first(v,'var'),c),self.num(first(v,'value'),c),first(v,'compare','equals')
            else:
                name,op,value=v[0]; a,b=self.num(name,c),self.num(value,c)
            return {'>':a>b,'<':a<b,'=':a==b,'equals':a==b,
                    'less_than_or_equals':a<=b,'greater_than_or_equals':a>=b}[op]
        raise AssertionError('Unmodelled trigger '+k)

    def execute(self,rows,c='PER'):
        branch=False
        for k,o,v in rows:
            if k=='if':
                branch=self.test(first(v,'limit',[]),c)
                if branch: self.execute([r for r in v if r[0]!='limit'],c)
                continue
            if k=='else_if':
                if not branch:
                    branch=self.test(first(v,'limit',[]),c)
                    if branch:self.execute([r for r in v if r[0]!='limit'],c)
                continue
            if k=='else':
                if not branch:self.execute(v,c)
                branch=False;continue
            branch=False
            if k in E:self.execute(E[k],c)
            elif k in self.exists:self.execute(v,k)
            elif k in {'set_variable','set_temp_variable'}:
                for a,_,b in v:self.v[c][a]=self.num(b,c)
            elif k=='subtract_from_temp_variable':
                a,_,b=v[0];self.v[c][a]-=self.num(b,c)
            elif k=='set_country_flag':self.f[c].add(v)
            elif k=='clr_country_flag':self.f[c].discard(v)
            elif k=='add_political_power':self.pp[c]+=float(v)
            elif k=='add_timed_idea':self.ideas[c,first(v,'idea')]=self.day()+int(first(v,'days'))
            elif k=='remove_ideas':self.ideas.pop((c,v),None)
            elif k=='create_wargoal':self.goals.append((c,first(v,'target'),first(v,'type'),tuple(int(x) for a,_,x in first(v,'generator') if a=='_bare')))
            elif k=='add_opinion_modifier':self.opinions.append((c,first(v,'target'),first(v,'modifier')))
            else:raise AssertionError('Unmodelled effect '+k)

    def call(self,key):self.execute(E[P+key])


def run():
    checks=[]
    def passed(x):checks.append(x)
    for text in OUT.values():
        if text.startswith(abu_musa.HEADER) and not text.startswith('l_english:'):parse(text)
    state=first(parse(OUT['history/states/1119-Abumusa.txt']),'state')
    history=first(state,'history'); start=first(history,'1970.1.1'); later=first(history,'2000.1.1')
    assert first(start,'owner')==first(start,'controller')=='UAE'
    assert first(start,'remove_core_of')==first(start,'add_claim_by')=='PER'
    assert first(later,'owner')==first(later,'controller')=='PER' and first(later,'add_core_of')=='PER'
    assert first(state,'provinces')==[('_bare','=','16219')]
    passed('History assigns Sharjah-representing UAE administration in1970, Iranian claim, and preserves native2000 ownership without changing provinces')

    w=World();w.call('prepare_abu_musa');assert w.pp['PER']==100 and not w.ideas
    for params in [('1971.9.1',False),('1971.9.2',True),('1971.11.29',True),('1971.11.30',True),('1971.12.1',False)]:
        w=World(params[0]);w.call('observe_abu_musa_withdrawal')
        assert w.test(T[P+'can_prepare_abu_musa'])==params[1]
    w=World('1971.11.29');w.call('prepare_abu_musa');assert w.pp['PER']==50
    w.call('assert_abu_musa');assert not w.goals and w.pp['PER']==50
    w.date='1971.11.30';w.call('assert_abu_musa');w.call('assert_abu_musa')
    assert w.goals==[('PER','UAE','take_state_focus',(1119,))] and w.pp['PER']==25
    assert w.ideas['PER',P+'abu_musa_landing_preparations']==w.day()+90
    assert w.owner==w.controller=='UAE' and not w.wars
    passed('Historical preparation opens90 days before withdrawal; coercive goal opens30November; goal is state1119 only and completion neither changes ownership nor declares war')

    w=World('1971.9.2');w.call('prepare_abu_musa');w.date='1971.11.30';w.call('assert_abu_musa')
    operational_end=w.ideas['PER',P+'abu_musa_landing_preparations']
    assert operational_end==w.day()+90
    w.date='1971.12.1';w.call('assert_abu_musa');assert w.ideas['PER',P+'abu_musa_landing_preparations']==operational_end
    passed('Early preparation does not exhaust the actual landing window; asserting the claim resets90 operational days once, and repeat clicks cannot extend it')

    w=World('1970.5.1');w.subjects['UAE']=None;w.pp['PER']=49.999;w.call('prepare_abu_musa');assert not w.ideas
    w.pp['PER']=50;w.call('prepare_abu_musa');w.call('prepare_abu_musa');assert w.pp['PER']==0 and len(w.ideas)==1
    w.pp['PER']=24.999;w.call('assert_abu_musa');assert not w.goals
    w.pp['PER']=25;w.call('assert_abu_musa');w.call('assert_abu_musa');assert w.pp['PER']==0 and len(w.goals)==1
    passed('Early actual independence opens the path; exact PP costs execute once and insufficient fractional funds never debit or grant')

    w=World('1975.1.1');w.f['UAE'].discard('COLDWAR_UAE_historical_withdrawal_schedule')
    w.v['UAE']['COLDWAR_UAE_contract_due']=w.day()*.024+2.17
    w.call('prepare_abu_musa');assert not w.ideas
    w.v['UAE']['COLDWAR_UAE_contract_due']=w.day()*.024+2.15
    w.call('prepare_abu_musa');assert w.ideas
    w.call('assert_abu_musa');assert not w.goals
    w.v['UAE']['COLDWAR_UAE_contract_due']=w.day()*.024+.023
    w.call('assert_abu_musa');assert len(w.goals)==1
    passed('Mutually revised handover dates use actual date-variable deadline, not a hardcoded1971 conquest opportunity')

    w=World('1971.11.30');w.call('observe_abu_musa_withdrawal');w.v['UAE']['COLDWAR_UAE_treaty_nonce']+=1
    assert not w.test(T[P+'can_prepare_abu_musa'])
    w.f['UAE'].discard('COLDWAR_UAE_historical_withdrawal_schedule');w.f['UAE'].discard('COLDWAR_UAE_withdrawal_schedule_active');w.f['UAE'].add('COLDWAR_UAE_protection_accepted')
    w.call('prepare_abu_musa');assert not w.ideas and w.pp['PER']==100
    passed('Changed treaty version invalidates old observer flags immediately; renewed protection closes the operation before any payment')

    for mutate in [lambda w:setattr(w,'scenario',False),lambda w:setattr(w,'dynamic',True),
                   lambda w:setattr(w,'owner','PER'),lambda w:setattr(w,'controller','ENG'),
                   lambda w:w.f['UAE'].add('COLDWAR_UAE_island_arbitration_agreed')]:
        w=World('1971.11.30');mutate(w);w.call('prepare_abu_musa');assert not w.ideas and w.pp['PER']==100
    w=World('1971.11.30');w.call('prepare_abu_musa');assert not w.test(first(IDEA,'cancel'))
    w.controller='PER';assert w.test(first(IDEA,'cancel'))
    w=World('1971.11.30');w.call('prepare_abu_musa');w.date='1972.3.1';assert not w.condition('has_idea','=',P+'abu_musa_landing_preparations','PER',False)
    passed('Later starts, dynamic tags, lost target control and accepted arbitration block grants; capture cancels bonuses and90-day expiry is finite')

    forbidden={'transfer_state','set_state_owner_to','annex_country','declare_war_on','create_unit','add_equipment_to_stockpile'}
    assert not forbidden.intersection(k for _,body in E.items() for k,_,_ in walk(body))
    mods=first(IDEA,'modifier')
    assert float(first(mods,'amphibious_invasion'))==.15 and float(first(mods,'invasion_preparation'))==-.25
    assert int(first(mods,'naval_invasion_capacity'))==5 and float(first(mods,'navy_personnel_cost_multiplier_modifier'))==.05
    for rel,text in OUT.items():
        if rel.endswith('.txt') or rel.endswith('.gfx'):parse(text)
    passed('Four real native modifiers, temporary cost, no invented forces/territorial shortcut; every emittedClausewitz file parses')
    result={'passed':len(checks),'checks':checks,'engine_tested':False,'limits':'AST and native-source checks; naval movement/combat, tooltips and multiplayer require HOI4.'}
    (HERE/'abu_musa_validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result))


if __name__=='__main__':run()
