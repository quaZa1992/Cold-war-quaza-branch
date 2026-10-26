"""Targeted execution tests of the emitted script AST, not an HOI4 emulator.

Exercises transactional money/queue effects, exact actor responses, programme
lifecycle and crisis transitions. Engine UI, political roster and economy
formulas are outside this interpreter's scope and are reported separately.
"""
from pathlib import Path
from dataclasses import dataclass,field
import json,copy
from script_ast import parse,first,values
from runtime_design import load_design

ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
P='COLDWAR_VIE_';D=load_design()
def read(rel):return parse((ROOT/rel).read_text(encoding='utf-8-sig'))
E={k:v for k,o,v in read('common/scripted_effects/COLDWAR_VIE_1970_effects.txt')}
budget={k:v for k,o,v in read('common/scripted_effects/00_budget_effects.txt')}
E.update({k:budget[k] for k in ('modify_treasury_effect','modify_debt_effect')})
T={k:v for k,o,v in read('common/scripted_triggers/COLDWAR_VIE_1970_triggers.txt')}
political={k:v for k,o,v in read('common/scripted_triggers/01_political_triggers.txt')}
for g in D['groups']:
    if g['party'] is not None:
        name=g['gate'].splitlines()[-1].split(' = ')[0];T[name]=political[name]
IDEAS={k:v for k,o,v in first(first(read('common/ideas/COLDWAR_VIE_1970_ideas.txt'),'ideas'),'country')}
DYN={k:v for k,o,v in read('common/dynamic_modifiers/COLDWAR_VIE_1970_dynamic_modifiers.txt')}
EVENTS={first(b,'id'):b for b in values(read('events/COLDWAR_VIE_1970_events.txt'),'country_event')}
N={n['id']:n for n in D['nodes']};Q={q['id']:q for q in D['decisions']}

@dataclass
class Country:
    tag:str='VIE';gov:str='communism';leader:str='Le Duan';exists:bool=True;scenario:bool=True
    variables:dict=field(default_factory=lambda:{'treasury':1.,'ruling_party':4.})
    flags:dict=field(default_factory=dict);ideas:dict=field(default_factory=dict);dynamic:set=field(default_factory=set)
    wars:set=field(default_factory=set);xp:float=0;tree:str='COLDWAR_VIE_1970_focus'
@dataclass
class State:
    id:int;owner:str='VIE';controller:str='VIE';slots:dict=field(default_factory=dict)

class World:
    def __init__(self):
        self.countries={t:Country(tag=t) for t in ('VIE','SOV','CHI','SVN','USA','RAJ','LAO','CAM','CBD','JAP')}
        self.states={s:State(s,slots={b:3 for b in ('industrial_complex','arms_factory','dockyard','offices','infrastructure','agriculture_district','fossil_powerplant','anti_air_building')}) for s in (519,520,521,522,523,524)}
        self.day=0;self.date='1970.1.1';self.events=[];self.queue=[];self.calls=[]
        self.call(P+'initialize')
    @property
    def vie(self):return self.countries['VIE']
    def number(self,v,c):
        try:return float(v)
        except (ValueError,TypeError):return c.variables.get(v,0.)
    def flag(self,c,k):return k in c.flags and (c.flags[k] is None or c.flags[k]>self.day)
    def idea(self,c,k):return k in c.ideas and (c.ideas[k] is None or c.ideas[k]>self.day)
    def datevalue(self,s):
        y,m,d=map(int,s.split('.'));return y*372+m*31+d
    def scope(self,key):
        if key in self.countries:return self.countries[key]
        if key.isdigit() and int(key) in self.states:return self.states[int(key)]
    def test(self,rows,c=None,root=None):
        c=c or self.vie;root=root or c
        return all(self.condition(k,o,v,c,root) for k,o,v in rows)
    def condition(self,k,o,v,c,root):
        if k in ('AND','limit','hidden_trigger'):return self.test(v,c,root)
        if k=='OR':return any(self.condition(a,b,d,c,root) for a,b,d in v)
        if k=='NOT':return not self.test(v,c,root)
        if k=='custom_trigger_tooltip':return self.test([r for r in v if r[0]!='tooltip'],c,root)
        scoped=self.scope(k)
        if scoped is not None:return self.test(v,scoped,root)
        if k in T:return self.test(T[k],c,root)==(v=='yes')
        if k=='IMP_is_1970_scenario':return c.scenario==(v=='yes')
        if k in ('original_tag','tag'):return c.tag==v
        if k=='exists':return c.exists==(v=='yes')
        if k=='has_government':return c.gov==v
        if k=='has_country_leader':return c.leader==json.loads(first(v,'name'))
        if k=='has_country_flag':return self.flag(c,v)
        if k=='has_idea':return self.idea(c,v)
        if k=='has_dynamic_modifier':return first(v,'modifier') in c.dynamic
        if k=='has_focus_tree':return c.tree==v
        if k=='has_war':return bool(c.wars)==(v=='yes')
        if k=='has_war_with':return v in c.wars
        if k=='owns_state':return self.states[int(v)].owner==c.tag
        if k=='is_owned_and_controlled_by':
            tag=root.tag if v=='ROOT' else v
            return c.owner==tag and c.controller==tag
        if k=='free_building_slots':return c.slots.get(first(v,'building'),0)>0
        if k=='has_variable':return v in c.variables
        if k=='date':return self.datevalue(self.date)>self.datevalue(v) if o=='>' else self.datevalue(self.date)<self.datevalue(v)
        if k=='check_variable':
            if first(v,'var'):
                a=self.number(first(v,'var'),c);b=self.number(first(v,'value'),c);op=first(v,'compare','equals')
                return {'greater_than_or_equals':a>=b,'less_than_or_equals':a<=b,'greater_than':a>b,'less_than':a<b,'equals':a==b}[op]
            key,op,val=v[0];a=self.number(key,c);b=self.number(val,c)
            return a>b if op=='>' else a<b if op=='<' else a==b
        raise AssertionError('Unhandled trigger '+str((k,o,v)))
    def call(self,key,c=None,root=None):self.run(E[key],c or self.vie,root or c or self.vie)
    def run(self,rows,c=None,root=None):
        c=c or self.vie;root=root or c;chain=False
        for k,o,v in rows:
            if k=='if':
                chain=self.test(first(v,'limit',[]),c,root)
                if chain:self.run([r for r in v if r[0]!='limit'],c,root)
                continue
            if k=='else_if':
                if not chain and self.test(first(v,'limit',[]),c,root):self.run([r for r in v if r[0]!='limit'],c,root);chain=True
                continue
            if k=='else':
                if not chain:self.run(v,c,root)
                chain=False;continue
            chain=False
            scoped=self.scope(k)
            if scoped is not None:self.run(v,scoped,root);continue
            if k in ('COLDWAR_VIE_1970_initialize_politics','COLDWAR_VIE_1970_update_politics'):
                self.calls.append(k);continue # Political provider has separate independent checks.
            if k in E:self.call(k,c,root);continue
            if k in ('hidden_effect','immediate'):self.run(v,c,root);continue
            if k in ('effect_tooltip','custom_effect_tooltip','force_update_dynamic_modifier','update_money_dirty_variable','log','name','trigger','ai_chance'):continue
            if k in ('set_variable','set_temp_variable','add_to_variable'):
                key,op,val=next(r for r in v if r[0] not in ('tooltip',))
                c.variables[key]=(c.variables.get(key,0) if k=='add_to_variable' else 0)+self.number(val,c);continue
            if k=='set_country_flag':
                if isinstance(v,list):c.flags[first(v,'flag')]=self.day+int(first(v,'days'))
                else:c.flags[v]=None
                continue
            if k=='clr_country_flag':c.flags.pop(v,None);continue
            if k=='add_ideas':c.ideas[v]=None;continue
            if k=='remove_ideas':c.ideas.pop(v,None);continue
            if k=='add_timed_idea':c.ideas[first(v,'idea')]=self.day+int(first(v,'days'));continue
            if k=='add_dynamic_modifier':c.dynamic.add(first(v,'modifier'));continue
            if k=='remove_dynamic_modifier':c.dynamic.discard(first(v,'modifier'));continue
            if k=='army_experience':c.xp+=float(v);continue
            if k=='country_event':self.events.append((c.tag,first(v,'id')));continue
            if k=='add_building_construction':
                b=first(v,'type');c.slots[b]-=1;self.queue.append((c.id,b,first(v,'instant_build')));continue
            if k=='load_focus_tree':c.tree=v;continue
            raise AssertionError('Unhandled effect '+str((k,o,v)))
    def ready(self,focus):
        for group in N[focus]['prerequisites']:self.vie.flags[group[0]+'_reward_applied']=None
    def grant(self,focus):self.call(P+'apply_'+focus.removeprefix(P))
    def earn(self,focus):self.vie.flags[focus+'_reward_applied']=None;self.vie.flags[P+'unlock_'+N[focus]['unlock']]=None
    def response(self,qid,accept=True,actor=None):
        q=Q[qid];i=D['decisions'].index(q)+1;event=EVENTS['COLDWAR_VIE_DIP.'+str(i)]
        self.run(values(event,'option')[0 if accept else 1],self.countries[actor or q['target']])
    def advance(self,days):
        self.day+=days
        for c in self.countries.values():
            for key in list(c.ideas):
                if not self.idea(c,key) or ('cancel' in [k for k,o,v in IDEAS.get(key,[])] and self.test(first(IDEAS[key],'cancel'),c,c)):c.ideas.pop(key,None)

results=[]
def case(name,fn):fn();results.append(name)
def money(w):return w.vie.variables['treasury']
def eq(a,b):assert abs(a-b)<1e-9,(a,b)

def paid():
    w=World();f=P+'industry_machine';w.ready(f);w.vie.variables['treasury']=.01
    w.grant(f);eq(money(w),.01);assert not w.queue and w.flag(w.vie,f+'_pending')
    w.vie.variables['treasury']=.12;w.grant(f);eq(money(w),0);assert w.queue==[(524,'industrial_complex','no')]
    w.grant(f);eq(money(w),0);assert len(w.queue)==1 and not w.flag(w.vie,f+'_pending')
case('Insufficient funding, exact funding, later retry and no replay',paid)
def state_guards():
    for mode in ('foreign_owner','occupation','full'):
        w=World();f=P+'industry_machine';w.ready(f);s=w.states[524]
        if mode=='foreign_owner':s.owner='CHI'
        if mode=='occupation':s.controller='CHI'
        if mode=='full':s.slots['industrial_complex']=0
        w.grant(f);eq(money(w),1);assert not w.queue
case('Ownership, control and capacity guard both queue and payment',state_guards)
def parent():
    w=World();f=P+'industry_machine';w.grant(f);assert not w.queue
    w.ready(f);w.grant(f);assert len(w.queue)==1
case('Unimplemented parent badges cannot release child rewards',parent)
def lifecycle():
    w=World();w.grant(P+'duan_root');w.grant(P+'industry_root');v=copy.deepcopy(w.vie.variables)
    w.vie.leader='Nguyen Van Linh';w.call(P+'sync_programmes');assert P+'duan_programme' not in w.vie.dynamic
    assert P+'industry_programme' in w.vie.dynamic
    w.grant(P+'linh_root');w.vie.leader='Le Duan';w.call(P+'sync_programmes')
    assert P+'duan_programme' in w.vie.dynamic and P+'linh_programme' not in w.vie.dynamic
    eq(w.vie.variables[P+'duan_war_support_factor'],v[P+'duan_war_support_factor'])
    before=copy.deepcopy(w.vie.variables);w.call(P+'sync_programmes');assert w.vie.variables==before
    w.vie.variables['ruling_party']=2;w.vie.gov='democratic';w.call(P+'sync_programmes')
    assert P+'duan_programme' not in w.vie.dynamic and P+'industry_programme' in w.vie.dynamic
case('Party/leader departure and return preserve values without replay',lifecycle)
def initialization():
    w=World();w.grant(P+'duan_root');before=copy.deepcopy(w.vie.variables);w.call(P+'initialize');assert w.vie.variables==before
    for s in D['spirits']:assert s['id']+'_0' in w.vie.ideas
    w.vie.scenario=False;before=copy.deepcopy(w.vie);w.call(P+'daily_update');assert w.vie==before
case('One-time initialization and non1970 exclusion',initialization)
def temporary():
    w=World();w.earn(P+'farm_root');w.call(P+'decision_rice_import_implement');eq(money(w),.965)
    w.earn(P+'farm_reserves');w.call(P+'decision_ration_implement');eq(money(w),.965);assert P+'decision_ration_idea' not in w.vie.ideas
    w.advance(181);w.call(P+'decision_ration_implement');eq(money(w),.945)
    w.earn(P+'linh_root');w.vie.leader='Nguyen Van Linh';w.advance(180);w.call(P+'decision_renovation_implement');assert P+'decision_renovation_idea' in w.vie.ideas
    w.vie.leader='Le Duan';w.advance(0);assert P+'decision_renovation_idea' not in w.vie.ideas
    w.vie.leader='Nguyen Van Linh';w.call(P+'sync_programmes');assert P+'decision_renovation_idea' not in w.vie.ideas
case('Family cap, real expiry, regime cancellation and no free restoration',temporary)
def unearned_common():
    w=World();w.earn(P+'chinh_field');w.vie.leader='Truong Chinh';assert w.test(T[P+'decision_local_pilot_eligible'])
    w.vie.leader='Le Duan';assert not w.test(T[P+'decision_local_pilot_eligible'])
    w.earn(P+'state_provincial');assert w.test(T[P+'decision_local_pilot_eligible'])
case('Shared decision access requires the exact earned provider',unearned_common)
def offer(accept=True):
    w=World();w.earn(P+'diplomacy_moscow');q=P+'decision_soviet_aid';w.call(q+'_send');eq(money(w),1);assert w.flag(w.vie,q+'_offer_pending')
    w.response(q,accept,actor='USA');eq(money(w),1);assert w.flag(w.vie,q+'_offer_pending')
    w.response(q,accept);eq(money(w),.96 if accept else 1);assert not w.flag(w.vie,q+'_offer_pending')
    w.response(q,accept);eq(money(w),.96 if accept else 1)
    return w
case('Foreign acceptance is actor-owned and paid exactly once',lambda:offer(True))
case('Foreign refusal costs nothing and stale responses do nothing',lambda:offer(False))
def expired_or_unfunded():
    for mode in ('expired','unfunded','ineligible','family_full'):
        w=World();w.earn(P+'diplomacy_moscow');q=P+'decision_soviet_aid';w.call(q+'_send')
        if mode=='expired':w.advance(91)
        if mode=='unfunded':w.vie.variables['treasury']=.01
        if mode=='ineligible':w.vie.flags.pop(P+'diplomacy_moscow_reward_applied')
        if mode=='family_full':w.vie.ideas[P+'decision_chinese_trade_idea']=w.day+180
        amount=money(w);w.response(q);eq(money(w),amount);assert q+'_idea' not in w.vie.ideas
case('Delayed acceptance rechecks expiry, funds, earned access and family cap',expired_or_unfunded)
def patron():
    w=World();w.earn(P+'diplomacy_moscow');q=P+'decision_soviet_aid';w.countries['SOV'].gov='democratic';w.call(q+'_send');w.response(q);w.call(P+'daily_update');assert P+'crisis_patron' not in w.vie.ideas
    w=offer(True);w.countries['SOV'].gov='democratic';w.call(P+'daily_update');assert P+'crisis_patron' in w.vie.ideas
    expires=w.vie.ideas[P+'crisis_patron'];w.advance(1);w.call(P+'daily_update');assert w.vie.ideas[P+'crisis_patron']==expires
case('Patron fall is a transition from accepted communist support, once only',patron)
def border():
    w=World();w.call(P+'daily_update');assert P+'crisis_border' not in w.vie.ideas
    w.vie.wars.add('CHI');w.call(P+'daily_update');assert P+'crisis_border' in w.vie.ideas
    w.vie.wars.clear();w.call(P+'daily_update');assert P+'crisis_border' not in w.vie.ideas
case('Border crisis requires actual China war and ends with peace',border)
def flood():
    w=World();w.call(P+'daily_update');assert not any(e[1]=='COLDWAR_VIE_CRISIS.1' for e in w.events)
    w.date='1971.8.20';w.call(P+'daily_update');w.call(P+'daily_update');assert w.events.count(('VIE','COLDWAR_VIE_CRISIS.1'))==1
    event=EVENTS['COLDWAR_VIE_CRISIS.1'];w.run(first(event,'immediate'));assert w.idea(w.vie,P+'crisis_flood')
    w=World();w.date='1972.1.1';w.call(P+'daily_update');assert not any(e[1]=='COLDWAR_VIE_CRISIS.1' for e in w.events)
case('1971 flood is neither a starting burden nor a retroactive late-save event',flood)
def southern():
    w=World();f=P+'unity_united';w.ready(f);w.states[520].controller='SVN';w.grant(f);assert P+'crisis_integration' not in w.vie.ideas
    w.states[520].controller='VIE';w.grant(f);assert w.idea(w.vie,P+'crisis_integration')
case('Actual southern ownership/control is needed for integration and its burden',southern)
def stages():
    w=World();f=P+'industry_recovery';w.ready(f);w.grant(f);assert w.vie.variables[P+'war_damage_stage']==3
    w.grant(P+'industry_root');assert w.vie.variables[P+'war_damage_stage']==3 and P+'war_damage_3' in w.vie.ideas and P+'war_damage_1' not in w.vie.ideas
case('Recovery stages are monotonic and cannot restack an earlier burden',stages)

def focus_preview_execution():
    focuses={first(f,'id'):f for f in values(first(read('common/national_focus/COLDWAR_VIE_1970_focus.txt'),'focus_tree'),'focus')}
    w=World();f=P+'industry_machine';completion=first(focuses[f],'completion_reward')
    # Native effect_tooltip is presentation only, including before prerequisites.
    before=copy.deepcopy(w.vie);w.run([('effect_tooltip','=',first(completion,'effect_tooltip'))])
    assert w.vie==before and not w.queue
    # Execute the actual completion block, not merely the helper, to catch a
    # preview accidentally paying or granting a second time.
    w.ready(f);w.vie.variables['treasury']=.12;w.run(completion)
    eq(money(w),0);assert w.queue==[(524,'industrial_complex','no')]
    w.run(completion);eq(money(w),0);assert len(w.queue)==1
case('Focus preview is inert while actual completion executes the guarded reward exactly once',focus_preview_execution)

def cambodia_recipient():
    for suffix in ('cambodia','withdrawal'):
        w=World();qid=P+'decision_'+suffix;q=Q[qid]
        w.earn(q['provider_focuses'][0]);w.call(qid+'_send')
        assert w.events[-1][0]=='CBD' and w.flag(w.vie,qid+'_offer_pending')
        w.response(qid,actor='CAM');eq(money(w),1)
        assert w.flag(w.vie,qid+'_offer_pending')
        w.response(qid,actor='CBD');eq(money(w),1-q['cash'])
        assert w.idea(w.vie,qid+'_idea') and not w.flag(w.vie,qid+'_offer_pending')
case('Both legacy Cambodian invitations reach CBD and reject Cameroon responses',cambodia_recipient)

report=dict(status='pass',tests=results,count=len(results),limits='A focused AST interpreter, not an engine emulator. Native UI, queue timing, economic formulas and political roster execution are not simulated. Independent provider and asset checks accompany this test.',engine_tested=False)
(HERE/'transaction_tests.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
