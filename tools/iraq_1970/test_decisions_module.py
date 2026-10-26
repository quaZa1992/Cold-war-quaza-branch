# IMPERIA CW — Cold War: iraq 1970 — test decisions module.
"""Execute generated decision/event AST at authority and transaction boundaries.

Native politics/economy/combat are recorded API boundaries, not simulated HOI4.
The harness bypasses native option visibility deliberately to test execution guards.
"""
from pathlib import Path
from datetime import date
import json,math,re
from common import ROOT,P,parse,first,values
import decisions_module,gulf_module
from audit_design import load_design
from test_usa_module import World,Scope


class DecisionWorld(World):
    def __init__(self):
        super().__init__({'common/scripted_effects/COLDWAR_USA_gulf_effects.txt':'','common/scripted_triggers/COLDWAR_USA_gulf_triggers.txt':'','events/COLDWAR_USA_gulf_events.txt':''})
        self.out=decisions_module.generate(ROOT);self.calls=[];self.since={};self.date=date(1970,1,1);self.scenario=True
        for tag in ['PER','SOV','SYR','EGY','PAL','JOR','UAE']:self.c[tag]=Scope(tag)
        self.c['IRQ'].leader='Ahmed Hassan al-Bakr';self.c['IRQ'].var.update(ruling_party=21,debt=0)
        self.s['554']=Scope('554',owner='SYR',controller='SYR')
        self.s['171']=Scope('171',owner='IRQ',controller='IRQ')
        self.arrays={key:{} for key in self.c}
        self.research=[]
        for output in [gulf_module.generate(ROOT),self.out]:
            for path,text in output.items():
                if path.startswith('common/scripted_effects/'):
                    self.effects.update({k:v for k,_,v in parse(text)})
                elif path.startswith('common/scripted_triggers/'):
                    self.triggers.update({k:v for k,_,v in parse(text)})
                elif path.startswith('events/'):
                    self.events.update({first(v,'id'):v for v in values(parse(text),'country_event')})
        self.loc={k:v for k,v in re.findall(r'^ ([^:]+):0 "(.*)"$',self.out['localisation/english/COLDWAR_IRQ_1970_decisions_l_english.yml'],re.M)}
        self.effects[P+'reconcile_programmes']=[] # separately tested root API
        self.effects[P+'set_leader']=[]            # separately tested root API
        self.effects[P+'refresh_situations']=[]
        self.design=load_design()
        assert len(self.design['nodes'])==426
        assert len({n['id'] for n in self.design['nodes']})==426
    def ready(self,key):
        d=next(d for d in self.design['decisions'] if d['id']==P+'decision_'+key)
        if d['unlock']!='START':
            self.c['IRQ'].flags[d['id']+'_unlocked']=None
            providers=d.get('audit_providers',[d['unlock']])
            self.c['IRQ'].flags[providers[0]+'_implemented']=None
    def test(self,k,o,v,c,root,prev,source):
        if k=='custom_trigger_tooltip':return self.tests([r for r in v if r[0]!='tooltip'],c,root,prev,source)
        if k=='is_in_array':return self.num(first(v,'value'),c) in self.arrays.get(c.key,{}).get(first(v,'array'),set())
        if k=='COLDWAR_IRQ_campaign_active':return self.scenario and c.key=='IRQ' and v=='yes'
        if k=='COLDWAR_IRQ_northern_settlement_active':return self.flag(c,P+'autonomy_fulfilled') and not(c.wars&{'KUR','PUK'})
        if k=='country_exists':return v in self.c and self.c[v].exists
        if k=='date':
            rhs=date(*map(int,str(v).strip('"').split('.')))
            return {'>':self.date>rhs,'<':self.date<rhs,'=':self.date==rhs}[o]
        if k=='has_country_flag' and isinstance(v,list):
            f=first(v,'flag');r=next(r for r in v if r[0]=='days')
            return self.flag(c,f) and self.compare(self.day-self.since.get((c.key,f),0),r[1],float(r[2]))
        if k=='has_country_leader':return getattr(c,'leader','')==first(v,'name').strip('"')
        if k in ['COLDWAR_IRQ_leader_bakr_in_office','COLDWAR_IRQ_leader_saddam_in_office','COLDWAR_IRQ_leader_aziz_muhammad_in_office']:
            return getattr(c,'leader','')==dict(zip(['COLDWAR_IRQ_leader_bakr_in_office','COLDWAR_IRQ_leader_saddam_in_office','COLDWAR_IRQ_leader_aziz_muhammad_in_office'],['Ahmed Hassan al-Bakr','Saddam Hussein','Aziz Muhammad']))[k]
        if k=='has_variable':return v in c.var
        if k=='has_war':return bool(c.wars)==(v=='yes')
        if k=='has_completed_focus':return v+'_implemented' in c.flags
        if k=='is_in_faction_with':return v in getattr(c,'faction',set())
        if k=='is_claimed_by':return v in getattr(c,'claims',set())
        if k=='free_building_slots':
            assert first(v,'building')=='infrastructure',('Unsupported state-capacity model',v)
            definitions=first(parse((ROOT/'common/buildings/00_buildings.txt').read_text(encoding='utf-8-sig')),'buildings')
            maximum=int(first(first(first(definitions,'infrastructure'),'level_cap'),'state_max'))
            _,op,count=next(r for r in v if r[0]=='size')
            return self.compare(maximum-c.infrastructure,op,float(count))
        return super().test(k,o,v,c,root,prev,source)
    def run(self,rows,c,root=None,prev=None,source=None):
        root=root or c;taken=False
        for k,o,v in rows:
            if k=='if':
                taken=self.tests(first(v,'limit',[]),c,root,prev,source)
                if taken:self.run([r for r in v if r[0]!='limit'],c,root,prev,source)
                continue
            if k=='else_if':
                if not taken and self.tests(first(v,'limit',[]),c,root,prev,source):taken=True;self.run([r for r in v if r[0]!='limit'],c,root,prev,source)
                continue
            if k=='else':
                if not taken:self.run(v,c,root,prev,source)
                taken=True;continue
            taken=False
            if k in ['effect_tooltip','custom_effect_tooltip']:continue
            if k=='add_tech_bonus':self.research.append(dict((a,d) for a,b,d in v));continue
            if k in ['add_to_array','remove_from_array']:
                name=first(v,'array')
                if name is None:name,_,raw=v[0]
                else:raw=first(v,'value')
                arr=self.arrays.setdefault(c.key,{}).setdefault(name,set())
                value=self.num(raw,c)
                if k=='add_to_array':arr.add(value)
                else:arr.discard(value)
                continue
            if k=='set_country_flag':self.since[(c.key,first(v,'flag') if isinstance(v,list) else v)]=self.day
            if k=='clear_variable':c.var.pop(v,None);continue
            if k=='subtract_from_temp_variable':
                name,_,value=v[0];c.var[name]=c.var.get(name,0)-self.num(value,c);continue
            if k=='clamp_variable':
                n=first(v,'var');c.var[n]=max(self.num(first(v,'min',-1e30),c),min(self.num(first(v,'max',1e30),c),c.var.get(n,0)));continue
            if k=='modify_debt_effect':c.var['debt']=c.var.get('debt',0)+c.var['debt_change'];continue
            if k=='add_political_power':
                c.var['political_power']=c.var.get('political_power',0)+self.num(v,c)
                continue
            if k=='add_stability':
                c.var['stability']=c.var.get('stability',0)+self.num(v,c)
                continue
            if k=='swap_ideas':
                c.ideas.pop(first(v,'remove_idea'),None)
                c.ideas[first(v,'add_idea')]=None
                continue
            if k in ['add_opinion_modifier','remove_opinion_modifier','set_correct_ideology_trait','update_dirty_politicsview_expanded','unban_party_scripted_call','update_government_coalition_strength']:
                self.calls.append((c.key,k,v));continue
            if k in ['change_relative_party_popularity','create_wargoal','white_peace']:
                self.calls.append((c.key,k,dict(c.var) if k=='change_relative_party_popularity' else v));continue
            super().run([(k,o,v)],c,root,prev,source)
    def show(self,eid,country):
        self.run(first(self.events[eid],'immediate',[]),self.c[country]);return eid,country
    def open(self,key):
        # Prison review's native complete_effect records the paid30PP session.
        if key=='prison_review':self.c['IRQ'].flags[P+'prison_review_pending']=None
        self.ready(key);self.call(P+'do_'+key,'IRQ');return self.show(*reversed(self.event_queue.pop()))
    def choose(self,shown,words):
        eid,country=shown
        option=next(v for v in values(self.events[eid],'option') if words in self.loc.get(first(v,'name'),'!'))
        self.run([r for r in option if r[0] not in ['name','trigger','ai_chance']],self.c[country])
        return option
    def response(self):return self.show(*reversed(self.event_queue.pop()))


def main():
    checks=[]
    def done(s):checks.append(s)
    out=decisions_module.generate(ROOT)
    for path,text in out.items():
        if path.endswith(('.txt','.gfx')):parse(text)
    done(f'All {len(out)} generated decision/effect/event/trigger/art files parse; no runtime writes from generate')
    w=DecisionWorld();w.c['IRQ'].var['gdp_total']=0;w.c['IRQ'].var['treasury']=1
    e=w.open('political_opening');w.c['IRQ'].var['gdp_total']=10;w.choose(e,'Accept legal rights')
    assert w.c['IRQ'].var['treasury']==1 and not w.flag(w.c['IRQ'],P+'legalization_accepted')
    done('GDP-zero menu cannot later accept an unset/free invoice after GDP recovers')
    w=DecisionWorld();e=w.open('political_opening');assert w.c['IRQ'].var[P+'D_legalization_invoice']==.1
    w.c['IRQ'].var.update(gdp_total=100,treasury=.1);w.choose(e,'Accept legal rights')
    assert math.isclose(w.c['IRQ'].var['treasury'],0,abs_tol=1e-9) and w.flag(w.c['IRQ'],P+'legalization_accepted')
    done('Event immediate freezes positive GDP invoice before display; later GDP change does not requote')
    w=DecisionWorld();e=w.open('front_offer');w.c['IRQ'].var['ruling_party']=22;cash=w.c['IRQ'].var['treasury'];w.choose(e,'Accept the charter')
    assert w.c['IRQ'].var['treasury']==cash and not w.flag(w.c['IRQ'],P+'front_accepted')
    done('Open domestic menu repeats exact current governing-party/provider authority at execution')
    w=DecisionWorld();e=w.open('prison_review');w.c['IRQ'].var['treasury']=0;w.choose(e,'Release and rehabilitate')
    assert not w.flag(w.c['IRQ'],P+'rikabi_rehabilitated') and not w.flag(w.c['IRQ'],P+'dawa_cadres_protected')
    done('Unaffordable prisoner review cannot grant historical candidate protection')
    for invalid in ['war','skip','expired']:
        w=DecisionWorld();e=w.open('oil_concession_offer');w.choose(e,'ENG');r=w.response();cash=w.c['IRQ'].var['treasury'];other=w.c['ENG'].var['treasury']
        if invalid=='war':w.c['IRQ'].wars.add('ENG')
        if invalid=='skip':w.c['ENG'].flags['MD_skip_treasury_cost']=None
        if invalid=='expired':w.day=61
        w.choose(r,'Accept the stated agreement')
        assert (w.c['IRQ'].var['treasury'],w.c['ENG'].var['treasury'])==(cash,other)
        assert not w.flag(w.c['IRQ'],P+'oil_concession_accepted')
    done('Foreign concession callback rejects stale war, recipient skip and expired pending consent without transfer')
    w=DecisionWorld();e=w.open('oil_concession_offer');w.choose(e,'ENG');r=w.response();w.choose(r,'Accept the stated agreement');w.choose(r,'Accept the stated agreement')
    assert math.isclose(w.c['IRQ'].var['treasury'],9.9) and math.isclose(w.c['ENG'].var['treasury'],10.1)
    assert w.tests(parse('COLDWAR_IRQ_oil_concession_active = yes'),w.c['IRQ'])
    w.c['ENG'].exists=False;assert not w.tests(parse('COLDWAR_IRQ_oil_concession_active = yes'),w.c['IRQ'])
    done('Accepted concession transfers exact once; active contract stops when counterpart disappears')
    w=DecisionWorld();w.c['IRQ'].var.update(ruling_party=2,debt=1,COLDWAR_IRQ_gulf_debt_snapshot=1,COLDWAR_IRQ_gulf_other_debt=0,COLDWAR_IRQ_gulf_principal_KUW=1);w.c['IRQ'].flags[P+'gulf_initialized']=None
    e=w.open('civic_credit_offer');w.choose(e,'SOV');r=w.response();w.choose(r,'Accept the stated agreement')
    assert math.isclose(w.c['IRQ'].var['debt'],1.5) and math.isclose(w.c['SOV'].var['treasury'],9.5)
    w.c['IRQ'].var['ruling_party']=21;w.c['IRQ'].leader='Saddam Hussein';e=w.open('saddam_repay');w.choose(e,'SOV civic_credit_offer')
    assert math.isclose(w.c['IRQ'].var['debt'],1.3) and math.isclose(w.c['SOV'].var['treasury'],9.7)
    assert math.isclose(w.c['IRQ'].var[P+'gulf_principal_KUW'],1)
    done('Actual emitted signed-debt API conserves named cash/native debt and preserves unrelated Gulf principal')
    w=DecisionWorld();c=w.c['IRQ'];c.var.update(ruling_party=2,debt=1,COLDWAR_IRQ_gulf_debt_snapshot=1,COLDWAR_IRQ_gulf_other_debt=1);c.flags[P+'gulf_initialized']=None
    e=w.open('civic_credit_offer');w.choose(e,'SOV');r=w.response();w.choose(r,'Accept the stated agreement')
    principal=P+'principal_civic_credit_offer_SOV';assert math.isclose(c.var[principal],.5)
    lender_cash=w.c['SOV'].var['treasury'];c.var['debt']=0;w.call(P+'reconcile_contract_credit','IRQ')
    assert c.var[principal]==0 and math.isclose(c.var[P+'gulf_other_retirement_total'],1.5) and math.isclose(c.var[P+'credit_retirement_seen'],1.5)
    assert w.c['SOV'].var['treasury']==lender_cash
    e=w.open('industry_credit');w.choose(e,'ENG');r=w.response();w.choose(r,'Accept the stated agreement');w.call(P+'reconcile_contract_credit','IRQ')
    assert c.var[principal]==0 and math.isclose(c.var[P+'principal_industry_credit_ENG'],.5) and math.isclose(c.var['debt'],.5)
    w.call(P+'reconcile_contract_credit','IRQ');assert math.isclose(c.var[P+'principal_industry_credit_ENG'],.5)
    done('Unknown native debt retirement is consumed once; later borrowing cannot revive an old creditor claim or fabricate creditor cash')
    w=DecisionWorld();w.date=date(1972,1,1);w.call(P+'reconcile_historical_roster','IRQ');assert w.flag(w.c['IRQ'],P+'dukhayl_unavailable') and not w.flag(w.c['IRQ'],P+'dukhayl_dead')
    w.date=date(1974,1,1);w.call(P+'reconcile_historical_roster','IRQ');assert w.flag(w.c['IRQ'],P+'dukhayl_dead')
    w.c['IRQ'].flags[P+'dawa_cadres_protected']=None;w.call(P+'reconcile_historical_roster','IRQ');assert w.flag(w.c['IRQ'],P+'dukhayl_dead')
    done('Dukhayl detention and year-precision death are distinct; late protection cannot clear recorded death')
    w=DecisionWorld();w.c['IRQ'].var['ruling_party']=8;w.call(P+'reconcile_historical_roster','IRQ');w.date=date(1989,1,1);w.call(P+'reconcile_historical_roster','IRQ')
    assert not w.flag(w.c['IRQ'],P+'dukhayl_dead') and not w.flag(w.c['IRQ'],P+'subayti_dead')
    w=DecisionWorld();w.date=date(1988,11,8);w.call(P+'reconcile_historical_roster','IRQ');assert not w.flag(w.c['IRQ'],P+'subayti_dead')
    w.date=date(1988,11,9);w.call(P+'reconcile_historical_roster','IRQ');assert w.flag(w.c['IRQ'],P+'subayti_dead')
    done('Earlier governing Dawa averts contingent repression; unprotected Subayti cutoff is9November1988')
    w=DecisionWorld();e=w.open('organize_western');w.choose(e,'National Progressive Party');w.day=89;w.call(P+'decision_tick','IRQ');assert not [x for x in w.calls if x[1]=='change_relative_party_popularity']
    w.day=90;w.call(P+'decision_tick','IRQ');w.call(P+'decision_tick','IRQ');calls=[x for x in w.calls if x[1]=='change_relative_party_popularity'];assert len(calls)==1 and calls[0][2]['party_index']==2 and calls[0][2]['party_popularity_increase']==.03
    done('Political organization delivers native normalized inputs only after90days and cannot replay on later ticks')
    w=DecisionWorld();w.ready('iran_opening');c=w.c['IRQ'];c.wars.add('PER');c.flags[P+'iran_campaign_window_open']=30;c.flags[P+'iran_short_war_implemented']=None;w.call(P+'refresh_decision_quotes','IRQ');w.call(P+'do_iran_opening','IRQ');cash=c.var['treasury'];w.call(P+'do_iran_opening','IRQ')
    assert math.isclose(cash,9.8) and c.var['treasury']==cash and w.idea(c,P+'iran_mobilization_bill')
    done('First-war paid opening consumes permanent entitlement once and installs its independent personnel bill')
    w=DecisionWorld();w.ready('iran_followup');c=w.c['IRQ'];c.wars.add('PER');c.flags[P+'iran_current_war_start']=None;w.day=89;w.call(P+'refresh_decision_quotes','IRQ');w.call(P+'do_iran_followup','IRQ');assert c.var['treasury']==10
    w.day=90;w.call(P+'refresh_decision_quotes','IRQ');w.call(P+'do_iran_followup','IRQ');assert math.isclose(c.var['treasury'],9.7)
    w.day=180;w.call(P+'do_iran_followup','IRQ');assert math.isclose(c.var['treasury'],9.7)
    done('Follow-up uses authoritative continuous-war clock,90day threshold,positive quote and180day cooldown')
    w=DecisionWorld();e=w.open('oil_contract_review');w.choose(e,'ENG');r=w.response();w.choose(r,'Accept the stated agreement');assert w.flag(w.c['IRQ'],P+'oil_export_contract_ENG')
    e=w.open('oil_contract_review');w.choose(e,'USA');r=w.response();w.choose(r,'Accept the stated agreement')
    assert w.flag(w.c['IRQ'],P+'oil_export_contract_USA') and not w.flag(w.c['IRQ'],P+'oil_export_contract_ENG') and len([i for i in w.c['IRQ'].ideas if i==P+'current_export_contract'])==1
    done('New accepted oil agreement replaces the previous sole contract; its programme never stacks')
    report={'scope':'Executed freshly generated decision/event/Gulf API AST; native engines are explicit boundaries, not HOI4 simulation','passed':len(checks),'checks':checks}
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
