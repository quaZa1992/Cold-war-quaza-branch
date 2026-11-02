# IMPERIA COLD WAR — Permanent agreement emitted-source lifecycle tests.
"""Bounded AST evaluator; not native HOI4 execution or a performance benchmark."""
import json
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,values,walk
def read(path):return parse((ROOT/path).read_text(encoding='utf-8-sig'))
D=json.loads((HERE/'approved_design.json').read_text(encoding='utf-8'))
E={k:v for k,o,v in read('common/scripted_effects/COLDWAR_FRA_1970_offers.txt')}
T={k:v for k,o,v in read('common/scripted_triggers/COLDWAR_FRA_1970_offer_triggers.txt')}
I={k:v for k,o,v in first(first(read('common/ideas/COLDWAR_FRA_1970_treaties.txt'),'ideas'),'country')}
DEC=first(read('common/decisions/COLDWAR_FRA_1970_offers.txt'),'COLDWAR_FRA_offers')

class Country:
    def __init__(self,tag):
        self.tag=tag;self.exists=True;self.subject=False;self.flags={};self.vars=defaultdict(Decimal)
        self.ideas=set();self.timed=set();self.wars=set();self.arrays=defaultdict(set);self.completed=set()
        self.government='gaullist';self.pp=Decimal(1000);self.vars['treasury']=Decimal(1000);self.awards=[]

class World:
    def __init__(self):
        self.countries={t:Country(t) for t in ('FRA','GER','USA')};self.targets={};self.day=0;self.temp={};self.checks=0
    def scope(self,key):
        return self.countries.get(self.targets.get(key.removeprefix('event_target:'))) if key.startswith('event_target:') else self.countries.get(key)
    def val(self,c,s):
        try:return Decimal(str(s))
        except Exception:return c.vars[s]
    def compare(self,a,op,b):
        return {'=':a==b,'<':a<b,'>':a>b,'equals':a==b,'greater_than_or_equals':a>=b}[op]
    def condition(self,c,rows,any_=False):
        out=[]
        for k,op,v in rows:
            self.checks+=1
            if k in ('AND','hidden_trigger','custom_trigger_tooltip'):r=self.condition(c,v)
            elif k=='OR':r=self.condition(c,v,True)
            elif k=='NOT':r=not self.condition(c,v)
            elif k in T:r=self.condition(c,T[k]) == (v=='yes')
            elif k.startswith('event_target:') or k in self.countries:
                other=self.scope(k);r=other is not None and self.condition(other,v)
            elif k=='tag':
                other=self.scope(v);r=c.tag==(other.tag if other else v)
            elif k=='exists':r=c.exists==(v=='yes')
            elif k=='is_subject':r=c.subject==(v=='yes')
            elif k=='IMP_is_1970_scenario':r=v=='yes'
            elif k=='has_war_with':r=v in c.wars
            elif k=='is_in_array':r=first(v,'value') in c.arrays[first(v,'array')]
            elif k=='has_country_flag':
                if isinstance(v,list):
                    name=first(v,'flag');age=next((o,int(x)) for key,o,x in v if key=='days')
                    r=name in c.flags and self.compare(self.day-c.flags[name],age[0],age[1])
                else:r=v in c.flags
            elif k=='has_idea':r=v in c.ideas
            elif k=='has_completed_focus':r=v in c.completed
            elif k.endswith('_government') and k.startswith('COLDWAR_FRA_'):r=c.government==k.removeprefix('COLDWAR_FRA_').removesuffix('_government')
            elif k=='check_variable':
                if first(v,'var'):
                    r=self.compare(self.val(c,first(v,'var')),first(v,'compare','equals'),self.val(c,first(v,'value')))
                else:
                    key,operation,value=v[0];r=self.compare(self.val(c,key),operation,self.val(c,value))
            elif k=='has_political_power':r=self.compare(c.pp,op,Decimal(v))
            elif k=='has_tech':r=False
            elif k in ('tooltip','always'):continue
            else:raise AssertionError('Unsupported trigger '+str((k,op,v)))
            out.append(r)
        return any(out) if any_ else all(out)
    def effect(self,c,rows):
        previous=None
        for k,op,v in rows:
            if k=='if':
                previous=self.condition(c,first(v,'limit',[]))
                if previous:self.effect(c,[r for r in v if r[0]!='limit'])
            elif k=='else':
                if previous is False:self.effect(c,v)
                previous=None
            elif k.startswith('event_target:') or k in self.countries:
                target=self.scope(k)
                if target is not None:self.effect(target,v)
            elif k in E:self.effect(c,E[k])
            elif k=='set_country_flag':c.flags[v]=self.day
            elif k=='clr_country_flag':c.flags.pop(v,None)
            elif k=='save_global_event_target_as':self.targets[v]=c.tag
            elif k=='clear_global_event_target':self.targets.pop(v,None)
            elif k=='add_ideas':c.ideas.add(v)
            elif k=='remove_ideas':c.ideas.discard(v);c.timed.discard(v)
            elif k=='set_variable':
                name,operation,value=v[0];c.vars[name]=self.val(c,value)
            elif k=='set_temp_variable':
                name,operation,value=v[0];self.temp[name]=self.val(c,value)
            elif k=='modify_treasury_effect':c.vars['treasury']+=self.temp['treasury_change']
            elif k=='add_political_power':c.pp+=Decimal(v)
            elif k=='add_tech_bonus':c.awards.append(v)
            elif k=='effect_tooltip':pass # Native non-executing prospective effects.
            elif k in ('custom_effect_tooltip','hidden_effect'):
                if isinstance(v,list):self.effect(c,v)
            else:raise AssertionError('Unsupported effect '+str((k,op,v)))
    def call(self,tag,effect):self.effect(self.countries[tag],E[effect])
    def maintain(self):self.call('FRA','COLDWAR_FRA_offer_maintenance')
    def quote(self,o,tag='GER'):
        f=self.countries['FRA'];p=self.countries[tag]
        f.government=o['group'];f.completed.add('COLDWAR_FRA_'+o['focus'])
        f.flags['COLDWAR_FRA_'+o['focus']+'_earned']=self.day
        self.targets['COLDWAR_FRA_offer_recipient']=tag
        f.flags['COLDWAR_FRA_offer_pending']=self.day;p.flags[o['id']+'_pending']=self.day
        for c in (f,p):c.vars['COLDWAR_FRA_quote_party']=c.vars['ruling_party'];c.vars['COLDWAR_FRA_quote_epoch']=c.vars['COLDWAR_FRA_government_epoch']
    def accept(self,o,tag='GER'):self.call(tag,o['id']+'_accept')
    def balances(self):return {t:(c.pp,c.vars['treasury'],len(c.awards)) for t,c in self.countries.items()}

checks=0
def check(ok,message):
    global checks
    checks+=1
    assert ok,message
compacts=[o for o in D['offers'] if o['duration_days']]
for o in compacts:
    oid=o['id'];idea=oid+'_treaty'
    w=World();w.quote(o);w.accept(o)
    check(all(idea in w.countries[t].ideas for t in ('FRA','GER')),'Not granted to both: '+oid)
    check(all(not w.condition(w.countries[t],first(I[idea],'cancel')) for t in ('FRA','GER')),'Native orphan guard rejects valid pair: '+oid)
    balances=w.balances();w.accept(o);w.maintain()
    check(w.balances()==balances,'Repeated acceptance/maintenance charged again: '+oid)
    w.day=2000;w.countries['FRA'].government='other';w.countries['FRA'].vars['COLDWAR_FRA_government_epoch']+=1;w.countries['GER'].vars['ruling_party']=99;w.maintain()
    check(all(idea in w.countries[t].ideas for t in ('FRA','GER')),'Duration or government change ended compact: '+oid)
    w.countries['GER'].wars.add('FRA');w.maintain()
    check(all(idea not in w.countries[t].ideas for t in ('FRA','GER')),'War did not remove both halves: '+oid)
    w.countries['GER'].wars.clear();w.maintain()
    check(all(idea not in w.countries[t].ideas for t in ('FRA','GER')),'Peace automatically regranted compact: '+oid)
    for kind in ('dip','fin','eco','mil'):
        for direction in ('on_us','by_us'):
            array='imp_'+kind+'_sanc_'+direction
            w=World();w.quote(o);w.accept(o);w.countries['GER'].arrays[array].add('FRA');w.maintain()
            check(all(idea not in w.countries[t].ideas for t in ('FRA','GER')),'Sanction missed: '+oid+' '+array)
            w.countries['GER'].arrays[array].clear();w.maintain()
            check(all(idea not in w.countries[t].ideas for t in ('FRA','GER')),'Sanction lifting regranted compact: '+oid)
            w=World();w.quote(o);w.countries['GER'].arrays[array].add('FRA');before=w.balances();w.accept(o)
            check(w.balances()==before and not w.countries['FRA'].ideas,'Acceptance ignored sanctions: '+oid+' '+array)
    # Unrelated third-country sanctions are irrelevant.
    w=World();w.quote(o);w.accept(o);w.countries['GER'].arrays['imp_eco_sanc_by_us'].add('USA');w.maintain()
    check(idea in w.countries['FRA'].ideas,'Third-party sanctions cancelled compact: '+oid)
    # Deleted partner, sovereignty loss and unilateral idea loss clean both sides.
    for change in ('deleted_partner','subject','missing_idea'):
        w=World();w.quote(o);w.accept(o)
        if change=='deleted_partner':w.countries['GER'].exists=False
        elif change=='subject':w.countries['GER'].subject=True
        else:w.countries['GER'].ideas.remove(idea)
        w.maintain();check(idea not in w.countries['FRA'].ideas,'Broken pair not cleaned: '+oid+' '+change)
    # Both signatories can withdraw, while a stale third-country flag cannot.
    for tag in ('FRA','GER','USA'):
        w=World();w.quote(o);w.accept(o);w.countries['USA'].flags['COLDWAR_FRA_compact_partner']=0
        w.effect(w.countries[tag],first(first(DEC,'COLDWAR_FRA_offer_withdraw'),'complete_effect'))
        check((idea in w.countries['FRA'].ideas)==(tag=='USA'),'Withdrawal identity guard failed: '+oid+' '+tag)
    # Upgrade an old saved 365-day idea without changing charges or receipts.
    w=World();w.quote(o);w.accept(o);w.countries['FRA'].flags.pop('COLDWAR_FRA_compact_permanent')
    for tag in ('FRA','GER'):w.countries[tag].timed.add(idea)
    balances=w.balances();w.maintain();w.maintain()
    check(w.balances()==balances and all(idea in w.countries[t].ideas and idea not in w.countries[t].timed for t in ('FRA','GER')),'Migration failed or charged again: '+oid)
    # Only the pair is touched; no global country or array iteration is emitted.
    check(not any(k in ('every_country','every_other_country','for_each_scope_loop') for k,op,v in walk(E['COLDWAR_FRA_offer_maintenance'])),'World scan in maintenance')

for o in D['offers']:
    w=World();before=w.balances();w.call('FRA',o['id']+'_preview')
    check(w.balances()==before and not any(c.ideas or c.flags for c in w.countries.values()),'Native preview executed an agreement reward: '+o['id'])
    w=World();w.quote(o);w.day=90;w.maintain()
    check('COLDWAR_FRA_offer_pending' not in w.countries['FRA'].flags,'Proposal timeout stuck: '+o['id'])
    w=World();w.quote(o);w.countries['GER'].vars['COLDWAR_FRA_government_epoch']+=1;w.maintain()
    check('COLDWAR_FRA_offer_pending' not in w.countries['FRA'].flags,'Changed proposal government accepted: '+o['id'])
    w=World();w.quote(o);w.countries['GER'].exists=False;w.maintain()
    check('COLDWAR_FRA_offer_pending' not in w.countries['FRA'].flags,'Deleted pending recipient stuck: '+o['id'])
    if not o['duration_days']:
        w=World();w.quote(o);w.accept(o);check(len(w.countries['FRA'].awards)==len(w.countries['GER'].awards)==1,'Finite research award lost')
        before=w.balances();w.quote(o);w.accept(o);check(w.balances()==before,'Finite research replayed')
        w=World();w.quote(o);cost=next(-e['amount'] for e in o['france']['completion_effects'] if e['kind']=='political_power')
        w.countries['FRA'].pp=Decimal(cost)-Decimal('0.5');before=w.balances();w.accept(o)
        check(w.balances()==before,'Fractional insufficient PP charged')

report={'project':'IMPERIA COLD WAR','kind':'Emitted AST model; no engine timing or FPS claim','checks':checks,'compacts':len(compacts),'sanction_directions_per_compact':8,'world_country_loops':0,'result':'pass'}
(HERE/'OFFER_TESTS.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
