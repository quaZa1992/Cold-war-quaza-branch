# IMPERIA COLD WAR — Strict interpreter for emitted annual-order transaction regression tests.
"""Executes the emitted subset. Unsupported operations fail rather than pass silently.

This is a source harness, not a replacement for native parser or multiplayer tests.
"""
from collections import defaultdict
from pathlib import Path
import copy
import operator
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first
from catalogue import TAGS


class Country:
    def __init__(self,tag,identifier):
        self.tag=tag;self.id=identifier;self.ai=False;self.exists=True
        self.subject=None if tag=='SOV' else 'SOV'
        self.values=defaultdict(float,treasury=100,gdp_total=1000,naval_factory_total=1)
        self.flags=set();self.flag_days={};self.missions={};self.ideas={};self.stock=defaultdict(float)


class State:
    def __init__(self,owner):
        self.owner=owner;self.controller=owner;self.cores={owner};self.coastal=True
        self.buildings=defaultdict(float)


class Context:
    def __init__(self,current,root,previous=None):self.current=current;self.root=root;self.previous=previous
    def enter(self,current):return Context(current,self.root,self.current)


class Harness:
    def __init__(self):
        self.countries={t:Country(t,i+1) for i,t in enumerate(('SOV',)+TAGS)}
        self.states=[State(c) for t,c in self.countries.items() if t!='SOV']
        self.globals=defaultdict(float);self.global_flags={'COLDWAR_ORD_enabled'}
        self.effects=dict((k,v) for k,o,v in parse((ROOT/'common/scripted_effects/COLDWAR_UNION_orders.txt').read_text(encoding='utf-8')))
        legacy=parse((ROOT/'common/scripted_effects/COLDWAR_UNI_1970_scripted_effects.txt').read_text(encoding='utf-8'))
        self.effects['COLDWAR_UNI_add_union_buff']=first(legacy,'COLDWAR_UNI_add_union_buff')
        self.triggers=dict((k,v) for k,o,v in parse((ROOT/'common/scripted_triggers/COLDWAR_UNION_orders.txt').read_text(encoding='utf-8')))
        self.decisions={k:v for name in ('prepare','submissions','register') for _,_,cat in parse((ROOT/f'common/decisions/COLDWAR_UNION_orders_{name}.txt').read_text(encoding='utf-8')) for k,o,v in cat}
        self.native_days=0
        for c in self.countries.values():self.call('COLDWAR_ORD_initialise_country',c.tag)
    def country(self,t):return self.countries[t]
    def resolve(self,name,ctx):
        if name=='THIS':return ctx.current
        if name=='ROOT':return ctx.root
        if name=='PREV':return ctx.previous
        if name=='FROM':return getattr(self,'from_country',None)
        if name.startswith('var:'):
            identifier=self.value(name[4:],ctx)
            return next((c for c in self.countries.values() if c.id==identifier),None)
        return self.countries.get(name)
    def target(self,name,ctx):
        if name.startswith('global.'):return self.globals,name[7:]
        if '.' in name:
            scope,key=name.split('.',1);obj=self.resolve(scope,ctx)
            if obj is None:raise AssertionError('Invalid variable scope: '+name)
            return obj.values,key
        return ctx.current.values,name
    def value(self,name,ctx):
        if isinstance(name,list):
            result=self.value(first(name,'value',0),ctx)
            for k,o,v in name:
                if k=='multiply':result*=self.value(v,ctx)
                elif k=='add':result+=self.value(v,ctx)
                elif k=='subtract':result-=self.value(v,ctx)
                elif k=='divide':result/=self.value(v,ctx)
            return result
        try:return float(name)
        except (ValueError,TypeError):pass
        if '.' in name:
            scope,key=name.split('.',1)
            if scope=='global':return self.globals[key]
            obj=self.resolve(scope,ctx)
            if obj is None:raise AssertionError('Invalid read scope: '+name)
            return self.value(key,ctx.enter(obj))
        if name=='id':return ctx.current.id
        if name.startswith('days_mission_timeout@'):return ctx.current.missions.get(name.split('@',1)[1],0)
        if name.startswith('num_equipment@'):return ctx.current.stock[name.split('@',1)[1]]
        if name.startswith('building_level@'):return ctx.current.buildings[name.split('@',1)[1]]
        return ctx.current.values[name]
    def test(self,rows,ctx,mode='and'):
        found=[]
        for k,o,v in rows:
            if k=='OR':answer=self.test(v,ctx,'or')
            elif k=='AND':answer=self.test(v,ctx)
            elif k=='NOT':answer=not self.test(v,ctx)
            elif k=='hidden_trigger':answer=self.test(v,ctx)
            elif k=='custom_trigger_tooltip':answer=self.test([r for r in v if r[0]!='tooltip'],ctx)
            elif k=='always':answer=v=='yes'
            elif k=='IMP_is_1970_scenario':answer=v=='yes'
            elif k=='is_ai':answer=ctx.current.ai==(v=='yes')
            elif k=='exists':answer=ctx.current.exists==(v=='yes')
            elif k in {'tag','original_tag'}:answer=ctx.current.tag==v
            elif k=='is_subject_of':answer=ctx.current.subject==v
            elif k=='has_country_flag':answer=v in ctx.current.flags
            elif k=='has_global_flag':answer=v in self.global_flags
            elif k=='has_variable':answer=v in ctx.current.values
            elif k=='has_active_mission':answer=v in ctx.current.missions
            elif k=='has_idea':answer=v in ctx.current.ideas
            elif k=='check_variable':
                if first(v,'var') is not None:
                    left=self.value(first(v,'var'),ctx);right=self.value(first(v,'value'),ctx)
                    comparison=first(v,'compare','equals')
                else:
                    a,b,c=v[0];left=self.value(a,ctx);right=self.value(c,ctx);comparison=b
                ops={'=':operator.eq,'>':operator.gt,'<':operator.lt,'>=':operator.ge,'<=':operator.le,'equals':operator.eq,'greater_than_or_equals':operator.ge,'greater_than':operator.gt,'less_than':operator.lt,'not_equals':operator.ne}
                answer=ops[comparison](left,right)
            elif k in self.triggers:answer=self.test(self.triggers[k],ctx)==(v=='yes')
            elif k=='any_owned_state':answer=any(self.test(v,ctx.enter(s)) for s in self.states if s.owner is ctx.current)
            elif k=='is_coastal':answer=ctx.current.coastal==(v=='yes')
            elif k=='is_owned_and_controlled_by':answer=ctx.current.owner is self.resolve(v,ctx) and ctx.current.controller is self.resolve(v,ctx)
            elif k=='is_core_of':answer=self.resolve(v,ctx) in ctx.current.cores
            elif isinstance(v,list):
                obj=self.resolve(k,ctx);answer=obj is not None and self.test(v,ctx.enter(obj))
            else:raise AssertionError('Unsupported trigger '+str((k,o,v)))
            found.append(answer)
        return any(found) if mode=='or' else all(found)
    def run(self,rows,ctx):
        branch=None
        for k,o,v in rows:
            if k=='if':
                branch=self.test(first(v,'limit'),ctx)
                if branch:self.run([r for r in v if r[0]!='limit'],ctx)
            elif k=='else_if':
                if branch is False:
                    branch=self.test(first(v,'limit'),ctx)
                    if branch:self.run([r for r in v if r[0]!='limit'],ctx)
            elif k=='else':
                if branch is False:self.run(v,ctx)
                branch=None
            elif k=='hidden_effect':self.run(v,ctx)
            elif k=='effect_tooltip':continue
            elif k in self.effects:self.run(self.effects[k],ctx)
            elif k in {'set_variable','set_temp_variable','add_to_variable','add_to_temp_variable','subtract_from_variable','subtract_from_temp_variable','multiply_variable','divide_variable'}:
                name,_,value=v[0];store,key=self.target(name,ctx);amount=self.value(value,ctx)
                if k.startswith('set_'):store[key]=amount
                elif k.startswith('add_'):store[key]+=amount
                elif k.startswith('subtract_'):store[key]-=amount
                elif k=='multiply_variable':store[key]*=amount
                elif k=='divide_variable':store[key]/=amount
            elif k in {'clamp_variable','clamp_temp_variable'}:
                store,key=self.target(first(v,'var'),ctx)
                store[key]=max(self.value(first(v,'min','-1000000000'),ctx),min(self.value(first(v,'max','1000000000'),ctx),store[key]))
            elif k=='round_variable':
                store,key=self.target(v,ctx);store[key]=int(store[key]+.5)
            elif k=='set_country_flag':
                flag=first(v,'flag') if isinstance(v,list) else v
                ctx.current.flags.add(flag)
                if isinstance(v,list):ctx.current.flag_days[flag]=self.value(first(v,'days'),ctx)
            elif k=='clr_country_flag':ctx.current.flags.discard(v);ctx.current.flag_days.pop(v,None)
            elif k=='set_global_flag':self.global_flags.add(v)
            elif k=='clr_global_flag':self.global_flags.discard(v)
            elif k=='activate_mission':ctx.current.missions[v]=self.value(first(self.decisions[v],'days_mission_timeout'),ctx)
            elif k=='remove_mission':ctx.current.missions.pop(v,None)
            elif k=='add_timed_idea':ctx.current.ideas[first(v,'idea')]=self.value(first(v,'days'),ctx)
            elif k=='add_ideas':ctx.current.ideas[v]=None
            elif k=='remove_ideas':ctx.current.ideas.pop(v,None)
            elif k=='modify_treasury_effect':ctx.current.values['treasury']+=ctx.current.values['treasury_change']
            elif k=='send_equipment':
                typ=first(v,'type');amount=min(ctx.current.stock[typ],self.value(first(v,'amount'),ctx));target=self.resolve(first(v,'target'),ctx)
                ctx.current.stock[typ]-=amount;target.stock[typ]+=amount
            elif k=='every_owned_state':
                for s in self.states:
                    child=ctx.enter(s)
                    if s.owner is ctx.current and self.test(first(v,'limit',[]),child):self.run([r for r in v if r[0]!='limit'],child)
            elif isinstance(v,list):
                obj=self.resolve(k,ctx)
                if obj is None:raise AssertionError('Invalid effect scope '+k)
                self.run(v,ctx.enter(obj))
            else:raise AssertionError('Unsupported effect '+str((k,o,v)))
    def call(self,name,tag,root=None):
        c=self.country(tag);self.run(self.effects[name],Context(c,self.country(root or tag)))
    def choose(self,actor,family,quantity=300,kind=1,fraction=0,target='UKR'):
        from catalogue import IDS
        c=self.country(actor)
        c.values.update(COLDWAR_ORD_draft_target=self.country(target).id,COLDWAR_ORD_draft_family=IDS[family],COLDWAR_ORD_draft_quantity=quantity,COLDWAR_ORD_draft_kind=kind,COLDWAR_ORD_draft_fraction=fraction)
        self.call('COLDWAR_ORD_commit_draft',actor)
    def advance(self,days):
        for _ in range(days):
            self.native_days+=1
            for c in self.countries.values():
                for flag in list(c.flag_days):
                    c.flag_days[flag]-=1
                    if c.flag_days[flag]<=0:c.flag_days.pop(flag);c.flags.discard(flag)
                for idea in list(c.ideas):
                    if c.ideas[idea] is None:continue
                    c.ideas[idea]-=1
                    if c.ideas[idea]<=0:del c.ideas[idea]
            for c in self.countries.values():
                for m in list(c.missions):
                    if m not in c.missions:continue
                    c.missions[m]-=1
                    if c.missions[m]<=0:
                        del c.missions[m]
                        self.run(first(self.decisions[m],'timeout_effect',[]),Context(c,c))
            for c in self.countries.values():self.call('COLDWAR_ORD_daily',c.tag)
