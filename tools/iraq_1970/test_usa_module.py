# IMPERIA CW — Cold War: iraq 1970 — test usa module.
"""Bounded execution of emitted Gulf AST; not an HOI4 emulator.

The interpreter fails closed on unsupported authored statements. It exercises
cash/equipment ledgers, native effect inputs, daily payments and warning/counter
timers. It does not simulate native resistance growth, battle, cancellation tick
ordering, economy formulas or the graphical/diplomatic engine.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import sys
import math
import json

ROOT = Path(__file__).resolve().parents[2]
# Use Vietnam's AST helper without shadowing the Iraqi compiler when this
# harness is imported by discovery alongside the other Iraqi test modules.
sys.path.append(str(ROOT / "tools/vietnam_1970"))
from script_ast import parse, first, values
from usa_module import generate, P


@dataclass
class Scope:
    key: str
    exists: bool = True
    var: dict = field(default_factory=lambda: {"treasury": 10., "gdp_total": 10.})
    flags: dict = field(default_factory=dict)
    ideas: dict = field(default_factory=dict)
    stock: float = 1000
    wars: set = field(default_factory=set)
    access: set = field(default_factory=set)
    subject: str | None = None
    troops: int = 2
    owner: str = "IRQ"
    controller: str = "IRQ"
    cores: set = field(default_factory=lambda: {"IRQ", "KUR"})
    resistance: float | None = None
    occupied: str = "KUR"
    targets: dict = field(default_factory=dict)
    forced: bool = False
    infrastructure: int = 2
    air_base: int = 1
    units: int = 0


class World:
    def __init__(self, outputs):
        self.out = outputs
        self.effects = dict((k,v) for k,_,v in parse(outputs['common/scripted_effects/COLDWAR_USA_gulf_effects.txt']))
        self.triggers = dict((k,v) for k,_,v in parse(outputs['common/scripted_triggers/COLDWAR_USA_gulf_triggers.txt']))
        self.events = dict((first(v,'id'),v) for v in values(parse(outputs['events/COLDWAR_USA_gulf_events.txt']),'country_event'))
        self.c = {s:Scope(s) for s in ('USA','IRQ','KUR','PUK','TUR','SAU','ENG','FRA','KUW')}
        self.c['KUR'].exists = self.c['PUK'].exists = False
        self.s = {str(s):Scope(str(s)) for s in (164,633,630,1078,165,172,488,399)}
        self.s['1078'].cores = {'IRQ','PUK'}
        self.s['1078'].occupied = 'PUK'
        self.s['100']=Scope('100',owner='TUR',controller='TUR')
        self.global_flags = set()
        self.day = 0
        self.event_queue = []
        self.units = []
        self.c['TUR'].flags[P+'host_north'] = None
        self.c['USA'].access.add('TUR')
    def lookup(self, key, c, root, prev, source):
        return {'ROOT':root,'PREV':prev,'THIS':c,'FROM':source}.get(key) or self.c.get(key) or self.s.get(key)
    def num(self, value, c):
        try: return float(value)
        except (ValueError,TypeError):
            if '.' in str(value):
                tag,key=str(value).split('.',1)
                if tag in self.c:return self.c[tag].var.get(key,0.)
            return c.var.get(value,0.)
    def flag(self,c,key):return key in c.flags and (c.flags[key] is None or c.flags[key]>self.day)
    def idea(self,c,key):return key in c.ideas and (c.ideas[key] is None or c.ideas[key]>self.day)
    def compare(self,a,op,b):
        return {'=':lambda:math.isclose(a,b,abs_tol=1e-9),'>':lambda:a>b,'<':lambda:a<b,'>=':lambda:a>=b,'<=':lambda:a<=b}[op]()
    def tests(self,rows,c,root=None,prev=None,source=None):
        root=root or c
        return all(self.test(k,o,v,c,root,prev,source) for k,o,v in rows)
    def test(self,k,o,v,c,root,prev,source):
        if k=='custom_trigger_tooltip':return self.tests([row for row in v if row[0]!='tooltip'],c,root,prev,source)
        if k in ('AND','limit','hidden_trigger'):return self.tests(v,c,root,prev,source)
        if k=='OR':return any(self.test(a,b,d,c,root,prev,source) for a,b,d in v)
        if k=='NOT':return not self.tests(v,c,root,prev,source)
        if k in self.triggers:return self.tests(self.triggers[k],c,root,prev,source)==(v=='yes')
        if k=='COLDWAR_IRQ_campaign_active':return c.key=='IRQ' and v=='yes'
        target=self.lookup(k,c,root,prev,source)
        if target:return self.tests(v,target,root,c,source)
        if k=='tag':return c.key==(self.lookup(v,c,root,prev,source) or Scope(v)).key
        if k=='exists':return c.exists==(v=='yes')
        if k=='always':return v=='yes'
        if k in ('has_country_flag','has_state_flag'):return self.flag(c,v)
        if k=='has_global_flag':return v in self.global_flags
        if k=='has_idea':return self.idea(c,v)
        if k=='has_war_with':return (self.lookup(v,c,root,prev,source) or Scope(v)).key in c.wars
        if k=='is_subject_of':return c.subject==(self.lookup(v,c,root,prev,source) or Scope(v)).key
        if k=='is_subject':return bool(c.subject)==(v=='yes')
        if k=='has_military_access_to':return (self.lookup(v,c,root,prev,source) or Scope(v)).key in c.access
        if k in ('is_owned_by','is_controlled_by','is_owned_and_controlled_by'):
            tag=(self.lookup(v,c,root,prev,source) or Scope(v)).key
            return {'is_owned_by':c.owner==tag,'is_controlled_by':c.controller==tag,'is_owned_and_controlled_by':c.owner==tag and c.controller==tag}[k]
        if k=='is_core_of':return (self.lookup(v,c,root,prev,source) or Scope(v)).key in c.cores
        if k=='occupied_country_tag':return c.occupied==(self.lookup(v,c,root,prev,source) or Scope(v)).key
        if k=='has_resistance':return (c.resistance is not None)==(v=='yes')
        if k=='resistance':return self.compare(c.resistance or 0,o,self.num(v,c))
        if k=='state':return c.key==v
        if k=='infrastructure':return self.compare(c.infrastructure,o,self.num(v,c))
        if k=='air_base':return self.compare(c.air_base,o,self.num(v,c))
        if k=='check_variable':
            if first(v,'var') is not None:
                a=self.num(first(v,'var'),c);b=self.num(first(v,'value'),c)
                op={'greater_than_or_equals':'>=','less_than_or_equals':'<=','greater_than':'>','less_than':'<','equals':'='}[first(v,'compare')]
            else:
                key,op,value=v[0];a=self.num(key,c);b=self.num(value,c)
            return self.compare(a,op,b)
        if k=='has_equipment':return all(self.compare(c.stock,op,self.num(amount,c)) for typ,op,amount in v)
        if k=='num_divisions_in_states':
            _,op,n=next(r for r in v if r[0]=='count');return self.compare(c.troops,op,float(n))
        if k=='any_country':return any(self.tests(v,x,root,c,source) for x in self.c.values() if x.exists)
        if k in ('any_owned_state','any_controlled_state'):
            selected=[s for s in self.s.values() if (s.owner if k=='any_owned_state' else s.controller)==c.key]
            return any(self.tests(v,s,root,c,source) for s in selected)
        raise AssertionError(('unsupported trigger',k,o,v,c.key))
    def call(self,key,c='USA',source=None):self.run(self.effects[key],self.c[c],self.c[c],None,self.c.get(source))
    def run(self,rows,c,root=None,prev=None,source=None):
        root=root or c
        taken=False
        for k,o,v in rows:
            if k=='if':
                taken=self.tests(first(v,'limit') or [],c,root,prev,source)
                if taken:self.run([r for r in v if r[0]!='limit'],c,root,prev,source)
                continue
            if k=='else_if':
                if not taken and self.tests(first(v,'limit') or [],c,root,prev,source):
                    taken=True;self.run([r for r in v if r[0]!='limit'],c,root,prev,source)
                continue
            if k=='else':
                if not taken:self.run(v,c,root,prev,source)
                taken=True;continue
            if k in self.effects:self.run(self.effects[k],c,root,prev,source);continue
            target=self.lookup(k,c,root,prev,source)
            if target:self.run(v,target,root,c,source);continue
            if k in ('set_variable','set_temp_variable','add_to_variable','add_to_temp_variable','subtract_from_variable','multiply_temp_variable','multiply_variable'):
                name,_,amount=v[0];amount=self.num(amount,c)
                if k.startswith('set_'):c.var[name]=amount
                elif k.startswith('add_'):c.var[name]=c.var.get(name,0)+amount
                elif k.startswith('subtract_'):c.var[name]=c.var.get(name,0)-amount
                else:c.var[name]=c.var.get(name,0)*amount
                continue
            if k=='modify_treasury_effect':c.var['treasury']+=c.var['treasury_change'];continue
            if k in ('set_country_flag','set_state_flag'):
                if isinstance(v,list):c.flags[first(v,'flag')]=self.day+self.num(first(v,'days'),c)
                else:c.flags[v]=None
                continue
            if k in ('clr_country_flag','clr_state_flag'):c.flags.pop(v,None);continue
            if k=='remove_ideas':c.ideas.pop(v,None);continue
            if k=='add_ideas':c.ideas[v]=None;continue
            if k=='add_timed_idea':c.ideas[first(v,'idea')]=self.day+self.num(first(v,'days'),c);continue
            if k=='add_equipment_to_stockpile':c.stock+=self.num(first(v,'amount'),c);continue
            if k=='send_equipment':
                amount=self.num(first(v,'amount'),c);target=self.lookup(first(v,'target'),c,root,prev,source)
                assert target is not None and target.exists and c.stock>=amount
                c.stock-=amount;target.stock+=amount;continue
            if k=='force_enable_resistance':c.forced=not isinstance(v,list) or first(v,'clear')!='yes';continue
            if k=='start_resistance':c.resistance=0;c.occupied=v;continue
            if k=='cancel_resistance':c.resistance=None;continue
            if k=='set_resistance':c.resistance=self.num(v,c);continue
            if k=='add_resistance':c.resistance=max(0,min(100,(c.resistance or 0)+self.num(v,c)));continue
            if k=='remove_resistance_target':c.targets.pop(v,None);continue
            if k=='add_resistance_target':c.targets[first(v,'id')]=(self.num(first(v,'amount'),c),self.day+self.num(first(v,'days'),c));continue
            if k=='country_event':self.event_queue.append((c.key,first(v,'id')));continue
            if k=='transfer_state':s=self.s[v];s.owner=s.controller=c.key;c.exists=True;continue
            if k=='division_template':continue
            if k=='create_unit':
                assert 'start_equipment_factor = 0' in first(v,'division')
                self.units.append((first(v,'owner'),c.key));continue
            if k=='declare_war_on':
                tag=first(v,'target');c.wars.add(tag);self.c[tag].wars.add(c.key);continue
            if k=='set_autonomy':self.c[first(v,'target')].subject=c.key;continue
            if k in ('every_country','random_owned_controlled_state'):
                selected=list(self.c.values()) if k=='every_country' else [s for s in self.s.values() if s.owner==c.key and s.controller==c.key]
                selected=[s for s in selected if self.tests(first(v,'limit') or [],s,root,c,source)]
                if k.startswith('random_'):selected=selected[:1]
                for s in selected:self.run([r for r in v if r[0]!='limit'],s,root,c,source)
                continue
            if k in ('add_dynamic_modifier','add_building_construction','diplomatic_relation'):continue
            raise AssertionError(('unsupported effect',k,o,v,c.key))
    def accept(self,event,c='KUR',option=0):
        row=values(self.events[P+'events.'+str(event)],'option')[option]
        self.run([r for r in row if r[0] not in ('trigger','name')],self.c[c])
    def tick(self,c='USA'):
        self.day+=1
        for obj in self.c.values():
            for idea in list(obj.ideas):
                if not self.idea(obj,idea):obj.ideas.pop(idea)
        self.call(P+('usa_daily' if c=='USA' else 'irq_daily'),c)


def main():
    out=generate(ROOT)
    for path,body in out.items():
        if path.endswith('.txt'):parse(body)
    checks=[]
    def done(label):checks.append(label)
    for cash,stock in [(.249,1000),(.25,999)]:
        w=World(out);w.c['USA'].var['treasury']=cash;w.c['USA'].stock=stock
        w.call(P+'initial_underground')
        assert w.c['USA'].stock==stock and w.c['USA'].var['treasury']==cash
        assert not w.flag(w.c['USA'],P+'initial_package_used')
    done('insufficient donor money or stock rejects entire underground transaction')
    w=World(out);w.c['USA'].var['treasury']=.25;w.s['164'].resistance=85
    w.call(P+'initial_underground')
    assert w.c['USA'].var['treasury']==0 and w.c['USA'].stock==0 and w.c['USA'].var[P+'cache']==1000
    assert sum(w.flag(s,P+'seeded') for s in w.s.values())==2
    assert w.s['164'].resistance==85 and w.s['633'].resistance==60
    w.call(P+'initial_underground');assert w.c['USA'].stock==0 and w.c['USA'].var[P+'cache']==1000
    done('exact funding succeeds once; at most two seeds; higher native resistance retained')
    w=World(out);w.call(P+'initial_underground');cash=w.c['USA'].var['treasury']
    for _ in range(90):w.tick()
    assert math.isclose(w.c['USA'].var['treasury'],cash-90*.05/7,abs_tol=1e-9)
    assert w.c['USA'].var[P+'support_days']==0 and not w.s['164'].targets
    done('90 actual funded days debit exactly the prorated budget; expiry removes owned targets')
    w=World(out);w.call(P+'initial_underground');w.c['USA'].var['treasury']=.001;w.tick()
    assert w.c['USA'].var['treasury']==.001 and w.c['USA'].var[P+'support_days']==0 and w.c['USA'].var[P+'cache']==1000
    done('unfunded recurring contract terminates without negative cash or cache recreation')
    w=World(out);w.call(P+'initial_underground');w.s['164'].resistance=79;w.s['633'].resistance=84
    for _ in range(30):w.tick()
    assert w.s['164'].resistance==80 and w.s['633'].resistance==84
    done('one monthly scripted pulse stops at80 without clamping native values above80')
    w=World(out);w.call(P+'initial_underground');w.c['IRQ'].var['treasury']=.199
    w.call(P+'start_security','IRQ');assert not w.idea(w.c['IRQ'],P+'security_small')
    w.c['IRQ'].var['treasury']=.2;w.call(P+'start_security','IRQ')
    assert w.idea(w.c['IRQ'],P+'security_small') and math.isclose(w.c['IRQ'].var['treasury'],0,abs_tol=1e-9)
    for _ in range(29):w.tick('IRQ')
    assert w.s['164'].resistance==60
    w.tick('IRQ');assert w.s['164'].resistance==45 and w.s['164'].targets['19709102'][0]==-20
    w.tick('IRQ');assert w.s['164'].resistance==45
    w.call(P+'end_security','IRQ');w.call(P+'start_major_operation','IRQ')
    assert not w.idea(w.c['IRQ'],P+'security_major') and w.flag(w.c['IRQ'],P+'security_cooldown')
    done('GDP invoice exact boundary,30-day delivery once, withdrawal keeps sunk invoice/cooldown')
    w=World(out);w.call(P+'initial_underground');w.call(P+'start_security','IRQ')
    for _ in range(20):w.tick('IRQ')
    w.c['IRQ'].troops=0;w.tick('IRQ');w.c['IRQ'].troops=2
    for _ in range(29):w.tick('IRQ')
    assert w.s['164'].resistance==60
    w.tick('IRQ');assert w.s['164'].resistance==45
    done('counterinsurgency reduction needs30 consecutive days of actual force presence')
    w=World(out);w.call(P+'initial_underground');w.c['IRQ'].wars.add('USA');w.c['USA'].wars.add('IRQ')
    w.s['164'].resistance=w.s['633'].resistance=80
    for _ in range(29):w.tick('IRQ')
    w.s['633'].resistance=79;w.tick('IRQ')
    assert w.c['IRQ'].var[P+'qualifying_days']==0
    w.s['633'].resistance=80
    for _ in range(30):w.tick('IRQ')
    assert w.flag(w.c['IRQ'],P+'uprising_warning')
    w.s['633'].resistance=79
    for _ in range(14):w.tick('IRQ')
    assert w.flag(w.c['IRQ'],P+'uprising_warning') and w.c['IRQ'].var[P+'warning_days']==0
    w.tick('IRQ');assert not w.flag(w.c['IRQ'],P+'uprising_warning')
    done('qualifying30days are consecutive; warning pauses and resets after15 invalid days')
    w=World(out);w.call(P+'initial_underground');w.c['IRQ'].wars.add('USA');w.c['USA'].wars.add('IRQ');w.s['164'].resistance=w.s['633'].resistance=80
    for _ in range(75):w.tick('IRQ')
    assert w.s['164'].owner==w.s['633'].owner=='KUR' and w.s['165'].owner=='IRQ' and w.s['630'].owner=='IRQ'
    assert all('IRQ' in w.s[s].cores for s in ('164','633')) and w.c['KUR'].wars=={'IRQ'}
    assert len(w.units)==1 and w.units[0][1] in ('164','633')
    assert not any(s.forced for s in w.s.values())
    assert not w.tests(w.triggers[P+'native_revolt_guard'],w.c['IRQ'],source=w.c['KUR'])
    w.c['KUR'].stock=0;w.accept(23)
    assert w.c['KUR'].stock==1000 and w.c['USA'].var[P+'cache']==0 and w.c['USA'].stock==0
    w.accept(23);assert w.c['KUR'].stock==1000
    assert w.c['USA'].var[P+'support_days']==90 and w.flag(w.c['USA'],P+'support_kur')
    done('bounded strongholds/core preservation, finite unequipped local force, cache delivered once without second debit')
    w=World(out);w.c['KUR'].exists=True;w.s['164'].owner=w.s['164'].controller='KUR';w.c['KUR'].stock=0
    w.c['KUR'].flags[P+'arms_offer']=None;w.accept(21)
    assert w.c['KUR'].stock==1000 and w.c['USA'].stock==0
    assert math.isclose(w.c['USA'].var['treasury'],9.75) and math.isclose(w.c['KUR'].var['treasury'],10.25)
    w.c['KUR'].flags[P+'arms_offer']=None;w.accept(21);assert w.c['KUR'].stock==1000
    done('recipient-owned direct transfer uses actual ROOT recipient and common once-only marker')
    w=World(out);w.call(P+'initial_underground');w.c['IRQ'].flags['COLDWAR_IRQ_autonomy_accepted']=None
    assert w.tests(w.triggers[P+'northern_grievance'],w.c['USA'])
    w.c['IRQ'].flags['COLDWAR_IRQ_autonomy_fulfilled']=None;w.call(P+'irq_daily','IRQ')
    assert w.s['164'].resistance is None and w.c['USA'].var[P+'support_days']==0
    assert w.c['USA'].var[P+'cache']==1000
    done('accepted offer alone leaves grievance; implemented settlement cleans owned override and preserves cache ledger')
    w=World(out);w.c['KUR'].exists=w.c['PUK'].exists=True
    w.s['164'].owner=w.s['164'].controller='KUR';w.s['1078'].owner=w.s['1078'].controller='PUK'
    w.c['IRQ'].flags.update({'COLDWAR_IRQ_autonomy_accepted':None,'COLDWAR_IRQ_autonomy_fulfilled':None})
    w.c['KUR'].flags[P+'accord_consent']=None;w.call(P+'recognize_kurdish_autonomy','IRQ')
    assert w.c['KUR'].subject=='IRQ' and w.c['PUK'].subject is None
    done('formal autonomy never subjects the other unconsenting local party')
    w=World(out);w.c['USA'].ideas[P+'northern_air_readiness']=3
    w.c['KUR'].ideas['COLDWAR_KUR_coalition_air_cover']=4;w.c['PUK'].ideas['COLDWAR_KUR_coalition_air_cover']=4
    w.call(P+'withdraw_air');assert not any(x.ideas for x in w.c.values())
    done('explicit USA air withdrawal immediately removes all owned recipient cover ideas')
    w=World(out);w.call(P+'initial_underground');w.call(P+'stop_support');w.c['USA'].wars.add('IRQ');w.s['164'].resistance=w.s['633'].resistance=80
    for _ in range(75):w.tick('IRQ')
    assert w.c['KUR'].exists and w.s['164'].owner=='KUR'
    done('withdrawal cannot freeze a supplied local movement or delete its committed cache')
    w=World(out);w.c['FRA'].flags.update({P+'host_north':None,P+'fresh_north_consent':None});w.c['FRA'].wars.add('USA')
    option=values(w.events[P+'events.42'],'option')[0]
    w.c['IRQ'].flags[P+'northern_emergency']=None
    assert not w.tests(first(option,'trigger'),w.c['USA'])
    w.c['TUR'].flags[P+'fresh_north_consent']=None
    assert w.tests(first(option,'trigger'),w.c['USA'])
    w.accept(42,'USA');assert w.c['USA'].ideas[P+'northern_air_readiness']==90
    assert not w.flag(w.c['TUR'],P+'fresh_north_consent')
    done('same current consenting host must supply access and an airbase; one consent cannot renew twice')
    w=World(out);w.c['KUR'].exists=w.c['PUK'].exists=True;w.s['164'].owner=w.s['164'].controller='KUR';w.s['1078'].owner=w.s['1078'].controller='PUK'
    w.c['IRQ'].flags.update({'COLDWAR_IRQ_autonomy_accepted':None,'COLDWAR_IRQ_autonomy_fulfilled':None});w.c['KUR'].flags[P+'accord_consent']=None;w.c['KUR'].subject='IRQ';w.c['IRQ'].wars.add('PUK')
    assert not w.tests(w.triggers[P+'settlement_respected'],w.c['USA'])
    assert w.tests(w.triggers[P+'northern_grievance'],w.c['USA'])
    done('one local party settlement cannot suppress an unconsenting other party at war')
    w=World(out);w.c['USA'].flags['MD_skip_treasury_cost']=None;w.call(P+'initial_underground')
    assert w.c['USA'].stock==1000 and P+'cache' not in w.c['USA'].var
    done('native treasury-skip setup cannot generate unpaid cash or equipment grants')
    report={'scope':'Static parsing and bounded emitted-AST execution; no HOI4 engine test','checks':checks,'passed':len(checks),'outputs':sorted(out)}
    path=ROOT/'tools/iraq_1970/staged/USA_GULF_TEST_REPORT.json';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
