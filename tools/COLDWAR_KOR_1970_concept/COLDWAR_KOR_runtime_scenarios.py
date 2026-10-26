# IMPERIA CW — Cold War: bounded scenarios executing emitted Korean scripts.
"""A fail-closed source interpreter, not the game engine or network simulator."""
from pathlib import Path
from copy import deepcopy
import argparse,json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];DOC=ROOT/'docs/design/COLDWAR_KOR_1970'
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,values,walk
P='COLDWAR_KOR_'

class World:
    def __init__(self,base):
        self.e={};self.t={};self.dm={};self.events={};self.decisions={};self.day=0;self.wars=set();self.queue=[];self.scopes=[]
        self.c={tag:{'v':{'ruling_party':0 if tag=='KOR' else 1,'treasury':0,'current_term':0},'tmp':{},'flags':{},'ideas':set(),'idea_until':{},'access':set(),'dm':set(),'leader':'Park Chung Hee' if tag=='KOR' else tag,'elections':False,'subject':False} for tag in ('KOR','NKO','USA','JAP','SOV','CHI','SVN','GER','SAU','IRQ')}
        self.c['KOR']['flags'][P+'initialized']=None
        for folder,target in [('scripted_effects',self.e),('scripted_triggers',self.t),('dynamic_modifiers',self.dm)]:
            for path in (base/'common'/folder).glob('COLDWAR_KOR_1970*.txt'):
                for k,o,v in parse(path.read_text(encoding='utf-8')):target[k]=v
        for path in (base/'events').glob('COLDWAR_KOR_1970*.txt'):
            for b in values(parse(path.read_text(encoding='utf-8')),'country_event'):self.events[first(b,'id')]=b
        for path in (base/'common/decisions').glob('COLDWAR_KOR_1970*.txt'):
            for cat,o,b in parse(path.read_text(encoding='utf-8')):
                for key,o,v in b:
                    if isinstance(v,list):self.decisions[key]=v
    def flag(self,tag,name):return name in self.c[tag]['flags'] and (self.c[tag]['flags'][name] is None or self.c[tag]['flags'][name]>self.day)
    def addflag(self,tag,name,days=None):self.c[tag]['flags'][name]=self.day+days if days else None
    def value(self,x,tag):
        if isinstance(x,list):
            val=self.value(first(x,'value','0'),tag)
            for k,o,v in x:
                if k=='add':val+=self.value(v,tag)
                elif k=='subtract':val-=self.value(v,tag)
                elif k=='multiply':val*=self.value(v,tag)
                elif k=='divide':val/=self.value(v,tag)
                elif k=='clamp':val=max(float(first(v,'min','-1e20')),min(float(first(v,'max','1e20')),val))
                elif k in ('min','max'):val=min(val,self.value(v,tag)) if k=='min' else max(val,self.value(v,tag))
            return val
        try:return float(x)
        except (ValueError,TypeError):
            if x in self.c:return x
            if '.' in str(x):
                scope,name=x.split('.',1)
                if scope in self.c:return self.value(name,scope)
            return self.c[tag]['tmp'].get(x,self.c[tag]['v'].get(x,0))
    def trigger(self,rows,tag='KOR'):
        for k,op,v in rows:
            c=self.c[tag]
            if k in self.t:r=self.trigger(self.t[k],tag)==(v=='yes')
            elif k in self.c:r=self.trigger(v,k)
            elif k=='AND' or k=='hidden_trigger':r=self.trigger(v,tag)
            elif k=='OR':r=any(self.trigger([a],tag) for a in v)
            elif k=='NOT':r=not self.trigger(v,tag)
            elif k in ('tag','original_tag'):r=tag==v
            elif k=='IMP_is_1970_scenario':r=v=='yes'
            elif k=='exists':r=v=='yes'
            elif k=='country_exists':r=v in self.c
            elif k=='is_subject':r=c['subject']==(v=='yes')
            elif k=='has_war_with':r=frozenset((tag,v)) in self.wars
            elif k=='has_country_flag':r=self.flag(tag,v)
            elif k=='has_idea':r=v in c['ideas'] and c['idea_until'].get(v,1e20)>self.day
            elif k=='has_military_access_to':r=v in c['access']
            elif k=='has_variable':r=v in c['v']
            elif k=='has_dynamic_modifier':r=first(v,'modifier') in c['dm']
            elif k=='has_country_leader':r=c['leader']==first(v,'name').strip('"')
            elif k=='has_elections':r=c['elections']==(v=='yes')
            elif k=='has_army_size':
                a,compare,b=v[0];count=c['v'].get('num_divisions',0)
                r=count>float(b) if compare=='>' else count<float(b)
            elif k=='has_stability':r=c['v'].get('stability',.5)<float(v) if op=='<' else c['v'].get('stability',.5)>float(v)
            elif k=='always':r=v=='yes'
            elif k=='check_variable':
                if first(v,'var') is not None:
                    lhs=self.value(first(v,'var'),tag);rhs=self.value(first(v,'value'),tag);cmp=first(v,'compare','equals')
                    cmp={'equals':'=','not_equals':'!=','greater_than':'>','less_than':'<','greater_than_or_equals':'>=','less_than_or_equals':'<='}.get(cmp,cmp)
                else:
                    a,cmp,b=v[0];lhs=self.value(a,tag);rhs=self.value(b,tag)
                r={'=':lhs==rhs,'!=':lhs!=rhs,'>':lhs>rhs,'<':lhs<rhs,'>=':lhs>=rhs,'<=':lhs<=rhs}[cmp]
            elif k=='custom_trigger_tooltip':r=self.trigger([a for a in v if a[0] not in ('tooltip','not_tooltip')],tag)
            elif k=='is_special_project_completed':r=False
            elif k=='date':r=False
            else:raise ValueError('Unmodelled trigger '+k+' in '+tag)
            if not r:return False
        return True
    def execute(self,rows,tag='KOR'):
        prior=False
        for k,op,v in rows:
            c=self.c[tag]
            if k=='if':
                prior=self.trigger(first(v,'limit',[]),tag)
                if prior:self.execute([a for a in v if a[0]!='limit'],tag)
            elif k=='else_if':
                if not prior:
                    prior=self.trigger(first(v,'limit',[]),tag)
                    if prior:self.execute([a for a in v if a[0]!='limit'],tag)
            elif k=='else':
                if not prior:self.execute(v,tag)
                prior=False
            elif k in self.e:self.execute(self.e[k],tag)
            elif k in self.c:self.execute(v,k)
            elif k=='hidden_effect':self.execute(v,tag)
            elif k in ('effect_tooltip','custom_effect_tooltip','log','title','desc','picture','is_triggered_only','fire_only_once','ai_chance'):continue
            elif k=='set_country_flag':
                self.addflag(tag,v if isinstance(v,str) else first(v,'flag'),None if isinstance(v,str) else int(first(v,'days','0')))
            elif k=='clr_country_flag':c['flags'].pop(v,None)
            elif k in ('set_variable','set_temp_variable','add_to_variable','add_to_temp_variable','subtract_from_variable','multiply_variable','divide_variable'):
                a,o,b=v[0];target=c['tmp'] if 'temp' in k else c['v'];val=self.value(b,tag)
                target[a]=target.get(a,0)+val if k.startswith('add_') else target.get(a,0)-val if k.startswith('subtract_') else target.get(a,0)*val if k.startswith('multiply_') else target.get(a,0)/val if k.startswith('divide_') else val
            elif k=='modify_treasury_effect':c['v']['treasury']+=self.value('treasury_change',tag)
            elif k=='add_dynamic_modifier':c['dm'].add(first(v,'modifier'))
            elif k=='remove_dynamic_modifier':c['dm'].discard(first(v,'modifier'))
            elif k=='add_ideas':
                c['ideas'].add(v)
                if v=='labour_unions':c['v']['labour_unions_opinion']=60
            elif k=='remove_ideas':c['ideas'].discard(v);c['idea_until'].pop(v,None)
            elif k=='add_timed_idea':
                id=first(v,'idea');c['ideas'].add(id);c['idea_until'][id]=self.day+int(first(v,'days','0'))
            elif k=='country_event':self.queue.append((tag,first(v,'id'),self.day+int(first(v,'days','0'))))
            elif k=='give_military_access':self.c[v]['access'].add(tag)
            elif k=='diplomatic_relation':
                if first(v,'relation')=='military_access':
                    target=first(v,'country')
                    if first(v,'active')=='yes':c['access'].add(target)
                    else:c['access'].discard(target)
            elif k=='army_experience':c['v']['army_experience']=c['v'].get('army_experience',0)+float(v)
            elif k in ('add_political_power','add_stability','add_war_support'):
                c['v'][k]=c['v'].get(k,0)+self.value(v,tag)
            elif k=='change_labour_unions_opinion':c['v']['labour_unions_opinion']=min(100,c['v']['labour_unions_opinion']+self.value('temp_opinion',tag))
            elif k in ('initialize_internal_faction_dynamic_modifiers','force_update_dynamic_modifier','update_set_politics','set_correct_ideology_trait'):continue
            elif k=='set_elections_60_months':c['elections']=True;c['v']['election_frequency']=60
            elif k=='create_country_leader':c['leader']=first(v,'name').strip('"')
            elif k=='kill_country_leader':c['leader']='New party incumbent';c['v']['retirements']=c['v'].get('retirements',0)+1
            elif k=='change_ruling_party_effect':
                # Native stand-in: actual helper sets party and election
                # permissions and dispatches set_leader without adding votes.
                c['v']['ruling_party']=self.value('rul_party_temp',tag)
                c['elections']=self.value('disable_elections',tag)==0
                self.call('1970_set_leader',tag)
            else:raise ValueError('Unmodelled effect '+k+' in '+tag)
    def call(self,name,tag='KOR'):self.execute(self.e[P+name],tag)
    def event_immediate(self,id,tag='KOR'):self.execute(first(self.events[id],'immediate',[]),tag)
    def option(self,id,index=0,tag='KOR'):
        b=values(self.events[id],'option')[index]
        assert self.trigger(first(b,'trigger',[]),tag),(id,index,'option unavailable')
        self.execute([a for a in b if a[0] not in ('name','trigger')],tag)
    def snapshot_cash(self):return {tag:c['v']['treasury'] for tag,c in self.c.items()}
    def can_decide(self,key):return self.trigger(first(self.decisions[P+key],'available',[]))
    def decide(self,key):
        assert self.can_decide(key),key
        b=self.decisions[P+key];self.c['KOR']['v']['add_political_power']=self.c['KOR']['v'].get('add_political_power',0)-float(first(b,'cost','0'))
        self.execute(first(b,'complete_effect',[]))
    def weekly(self,tag):
        self.c[tag]['v']['additional_expenses_rate']=0;self.c[tag]['v']['additional_income_rate']=0
        self.call('contract_expenses',tag);self.call('contract_income',tag)
        return (self.c[tag]['v']['additional_expenses_rate'],self.c[tag]['v']['additional_income_rate'])

def run(base):
    tests=[]
    def test(name,fn):fn();tests.append(name)
    def assurance():
        w=World(base);start=w.snapshot_cash();w.call('send_us_alliance_assurance');assert w.snapshot_cash()==start
        w.call('accept_us_alliance_assurance','USA')
        assert w.c['KOR']['v']['treasury']==-1 and w.c['USA']['v']['treasury']==1,w.snapshot_cash()
        assert w.weekly('KOR')==(.002,0) and w.weekly('USA')==(0,.002)
        signed=w.snapshot_cash();w.call('accept_us_alliance_assurance','USA');w.call('refuse_us_alliance_assurance','USA');assert w.snapshot_cash()==signed
        assert w.flag('KOR',P+'us_alliance_assurance_signed')
    test('accepted agreement: negative Korean treasury, directed partner income, weekly rates, no repeated or stale-option payment',assurance)
    def refusal():
        w=World(base);start=w.snapshot_cash();w.call('send_family_reunions');w.call('refuse_family_reunions','NKO');assert w.snapshot_cash()==start
        assert not w.flag('KOR',P+'family_reunions_signed') and w.flag('KOR',P+'family_reunions_cooldown')
        assert not w.trigger(w.t[P+'can_send_family_reunions']);w.day=181;assert w.trigger(w.t[P+'can_send_family_reunions'])
    test('refusal charges neither party and blocks resubmission for180days',refusal)
    def deadline():
        w=World(base);w.call('send_family_reunions');w.day=60;before=w.snapshot_cash();w.call('contract_maintenance')
        assert not w.flag('KOR',P+'family_reunions_pending') and w.flag('KOR',P+'family_reunions_cooldown')
        w.call('accept_family_reunions','NKO');assert w.snapshot_cash()==before
        w.option(P+'foreign.2',2,'NKO');assert w.snapshot_cash()==before
    test('60-day live window closes acceptance and maintenance guarantees automatic cooldown/cleanup',deadline)
    def office():
        w=World(base);w.c['KOR']['v'][P+'office_epoch']=1;w.call('send_us_alliance_assurance');before=w.snapshot_cash();w.c['KOR']['v'][P+'office_epoch']=2
        w.call('accept_us_alliance_assurance','USA');assert w.snapshot_cash()==before and not w.flag('KOR',P+'us_alliance_assurance_signed')
    test('same-party change of incumbent invalidates the old office offer without payment',office)
    def selected():
        w=World(base);w.call('send_alternative_finance_contacts_to_GER');assert w.flag('GER',P+'alternative_finance_contacts_pending') and not w.flag('USA',P+'alternative_finance_contacts_pending')
        before=w.snapshot_cash();w.call('accept_alternative_finance_contacts','USA');assert w.snapshot_cash()==before
        w.call('accept_alternative_finance_contacts','GER');assert w.c['KOR']['v']['treasury']==-1 and w.c['GER']['v']['treasury']==1
        w.call('foreign_refresh');assert w.flag('KOR',P+'alternative_finance_contacts_GER_signed')
        assert any('alternative_finance_contacts' in x for x in w.c['KOR']['dm'])
        w.wars.add(frozenset(('KOR','GER')));assert w.weekly('GER')==(0,0)
        w.call('foreign_refresh');assert not any('alternative_finance_contacts' in x for x in w.c['KOR']['dm'])
    test('selected second partner, unauthorized actor, maintenance and war cleanup',selected)
    def nordpolitik():
        w=World(base)
        for tag in ('SOV','CHI'):
            w.call('send_nordpolitik_recognition_to_'+tag);w.call('accept_nordpolitik_recognition',tag)
        w.call('foreign_refresh')
        mods=[x for x in w.c['KOR']['dm'] if 'nordpolitik_recognition' in x]
        assert len(mods)==2,mods
        total=sum(float(first(w.dm[x],'trade_opinion_factor','0')) for x in mods)
        assert abs(total-.06)<1e-8,total
    test('two independent Soviet/Chinese signatures retain two separate Korean reward records',nordpolitik)
    def stale_deadline():
        w=World(base);w.call('send_nordpolitik_recognition_to_SOV');w.call('accept_nordpolitik_recognition','SOV');w.day=10;w.call('send_nordpolitik_recognition_to_CHI')
        w.day=60;w.call('expire_nordpolitik_recognition');assert w.flag('KOR',P+'nordpolitik_recognition_pending')
        w.day=70;w.call('contract_maintenance');assert not w.flag('KOR',P+'nordpolitik_recognition_pending') and w.flag('KOR',P+'nordpolitik_recognition_cooldown')
    test('an old offer timeout cannot cancel a newer still-open transaction',stale_deadline)
    def multilateral():
        w=World(base);w.call('send_neutrality_guarantees');before=w.snapshot_cash()
        for tag in ('USA','NKO','SOV'):w.call('accept_neutrality_guarantees',tag)
        assert w.snapshot_cash()==before and not w.flag('KOR',P+'neutrality_guarantees_signed')
        w.call('accept_neutrality_guarantees','CHI');assert w.flag('KOR',P+'neutrality_guarantees_signed')
        for tag in ('USA','NKO','SOV','CHI'):assert not w.flag(tag,P+'neutrality_guarantees_assent_'+tag)
    test('multilateral agreement requires every current signatory and clears all assent receipts',multilateral)
    def partial_retry():
        w=World(base);w.call('send_neutrality_guarantees')
        for tag in ('USA','NKO','SOV'):w.call('accept_neutrality_guarantees',tag)
        w.day=60;w.call('contract_maintenance');w.day=241;w.call('send_neutrality_guarantees');w.call('accept_neutrality_guarantees','CHI')
        assert not w.flag('KOR',P+'neutrality_guarantees_signed')
    test('partial multilateral assent from an expired offer never supplies the new offer',partial_retry)
    def expiry():
        w=World(base);w.call('send_family_reunions');w.call('accept_family_reunions','NKO');assert w.weekly('KOR')[0]>.0
        w.day=1100;w.call('foreign_refresh');assert w.weekly('KOR')==(0,0) and w.weekly('NKO')==(0,0)
        assert not any('family_reunions' in x for x in w.c['KOR']['dm']|w.c['NKO']['dm'])
        before=w.snapshot_cash();w.call('foreign_refresh');assert w.snapshot_cash()==before
    test('term expiry removes both modifiers and weekly costs; refresh never replays capital charges',expiry)
    def legacy():
        w=World(base);before=w.snapshot_cash();w.addflag('KOR','COLDWAR_NKO_korean_channel_confederation_offer_accepted');w.call('foreign_initialize');assert P+'confederal_member' not in w.c['KOR']['ideas']
        w.addflag('NKO','COLDWAR_NKO_korean_channel_confederation_offer_accepted');w.call('foreign_initialize');assert P+'confederal_member' in w.c['KOR']['ideas'] and P+'confederal_member' in w.c['NKO']['ideas'];assert w.snapshot_cash()==before
        fresh=World(base);fresh.call('send_sovereign_confederation');fresh.call('accept_sovereign_confederation','NKO');assert P+'confederal_member' in fresh.c['KOR']['ideas']
        assert not fresh.flag('KOR','COLDWAR_NKO_korean_channel_confederation_offer_accepted')
    test('membership requires both legacy signatures; new consent never manufactures old paid acceptance',legacy)
    def ballot():
        w=World(base);v=w.c['KOR']['v'];v.update({'party_pop_array^0':49,'party_pop_array^1':51,P+'charter_model':1})
        for f in ('talks_authorized','charter_mandate','ballot_pending'):w.addflag('KOR',P+f)
        w.addflag('KOR',P+'charter_supporter_1');w.event_immediate(P+'transition.30')
        assert w.flag('KOR',P+'constitutional_ratification_passed') and not w.flag('KOR',P+'constitutional_order') and not w.c['KOR']['elections']
        reject=World(base);reject.c['KOR']['v'].update({'party_pop_array^0':50,'party_pop_array^1':50,P+'charter_model':1})
        for f in ('talks_authorized','charter_mandate','ballot_pending','charter_supporter_1'):reject.addflag('KOR',P+f)
        reject.event_immediate(P+'transition.30');assert reject.flag('KOR',P+'charter_rejected') and not reject.flag('KOR',P+'constitutional_ratification_passed')
        empty=World(base);empty.call('calculate_charter_vote');assert empty.c['KOR']['v'][P+'charter_support_share']==0
    test('actual emitted charter ballot: majority succeeds, tie rejects, zero electorate safe, no elections before implementation',ballot)
    def opposition():
        w=World(base);w.c['KOR']['v']['party_pop_array^1']=.4;w.addflag('KOR',P+'talks_authorized');w.option(P+'transition.201',0)
        assert w.flag('KOR',P+'charter_supporter_1') and w.c['KOR']['v']['ruling_party']==0
    test('a legal opposition party can accept charter terms without first taking government',opposition)
    def court():
        w=World(base)
        for name in ('judicial_review','constitutional_order','court_appointments_implemented','court_implementation_pending'):w.addflag('KOR',P+name)
        w.addflag('KOR',P+'court_commissioning_delay',90);w.call('politics_sync');assert not any(x[1]==P+'transition.88' for x in w.queue)
        w.day=90;w.call('politics_sync');w.call('politics_sync');assert sum(x[1]==P+'transition.88' for x in w.queue)==1
        w.option(P+'transition.88',0);w.call('politics_sync');assert w.flag('KOR',P+'judicial_review_operational') and not w.flag('KOR',P+'court_implementation_pending')
    test('court requires funded appointments and elapsed commissioning; only one event is queued',court)
    def actual_winner():
        w=World(base);c=w.c['KOR'];c['v']['ruling_party']=22;c['leader']='Chun Doo-hwan';c['elections']=True;c['v'][P+'charter_model']=1
        for name in ('constitutional_order','election_resolution_pending','roh_nominated'):w.addflag('KOR',P+name)
        w.call('1970_set_leader');assert c['leader']=='Chun Doo-hwan'
        w.addflag('KOR',P+'install_elected_incumbent');w.call('on_native_election_resolved')
        assert c['leader']=='Roh Tae-woo' and w.flag('KOR',P+'lawful_election_completed') and not w.flag('KOR',P+'election_resolution_pending')
    test('Roh nomination preserves the incumbent until an actual winning-party result authorizes installation',actual_winner)
    def term_limit():
        w=World(base);c=w.c['KOR'];c['elections']=True;c['v'].update({'ruling_party':22,P+'charter_model':1,'current_term':1});c['leader']='Roh Tae-woo'
        for f in ('constitutional_order','election_resolution_pending','install_elected_incumbent'):w.addflag('KOR',P+f)
        w.call('on_native_election_resolved');assert c['leader']=='Roh Tae-woo' and w.flag('KOR',P+'presidential_term_served_roh')
        w.addflag('KOR',P+'election_resolution_pending');c['v']['current_term']=2;before=c['v'].get('retirements',0);w.call('on_native_election_resolved')
        assert c['leader']!='Roh Tae-woo' and c['v']['retirements']==before+1 and c['v']['current_term']==1
        w.call('1970_set_leader');assert c['leader']=='New party incumbent' and c['v']['retirements']==before+1
        c['v']['party_pop_array^2']=.2;w.addflag('KOR',P+'constitution_presidential');w.addflag('KOR',P+'presidential_term_served_ys')
        assert not w.can_decide('nominate_ys') and w.can_decide('nominate_dj')
        w.decide('nominate_dj');c['v']['ruling_party']=2;w.addflag('KOR',P+'election_resolution_pending');w.call('on_native_election_resolved')
        assert c['leader']=='Kim Dae-jung' and w.flag('KOR',P+'presidential_term_served_dj')
    test('one-term president retires at the next resolved election; an unserved same-party rival remains eligible',term_limit)
    def formation():
        w=World(base);v=w.c['KOR']['v'];v.update({'ruling_party':22,'party_pop_array^22':.2});w.addflag('KOR',P+'constitution_controlled_fifth')
        assert not w.flag('KOR',P+'lawful_election_completed');w.decide('form_democratic_justice_party');assert w.flag('KOR',P+'djp_formed') and v['party_pop_array^22']==.2
    test('DJP electoral organization forms before its first election without free votes or a new incumbent',formation)
    def revolutionary():
        w=World(base);assert not w.can_decide('ratify_revolutionary_settlement');w.addflag('KOR',P+'left_pluralism');assert not w.can_decide('ratify_revolutionary_settlement')
        c=w.c['KOR'];c['v']['ruling_party']=4;c['elections']=True;w.addflag('KOR',P+'constitutional_order');w.decide('ratify_revolutionary_settlement')
        assert c['leader']=='Revolutionary Cabinet' and c['elections'] and P+'revolutionary_settlement_burden' in c['ideas']
    test('revolutionary cabinet requires actual party accession and preserves an existing lawful electoral settlement',revolutionary)
    def security():
        w=World(base);v=w.c['KOR']['v'];v['stability']=.2;w.addflag('KOR',P+'park_succession_unresolved');assert not w.can_decide('authorize_security_directorate')
        w.addflag('KOR',P+'officer_council_contest');w.decide('authorize_security_directorate');assert v['ruling_party']==7 and w.c['KOR']['leader']=='Security Directorate' and not w.c['KOR']['elections']
        assert P+'security_directorate_burden' in w.c['KOR']['ideas'] and v['add_political_power']==-100
    test('security takeover requires an actual command crisis and instability; startup succession marker is insufficient',security)
    def kjp():
        w=World(base);c=w.c['KOR'];c['elections']=True;c['v']['party_pop_array^0']=.48;w.addflag('KOR',P+'constitutional_order');w.decide('nominate_kjp');w.call('1970_set_leader');assert c['leader']=='Park Chung Hee'
        for f in ('install_elected_incumbent','election_resolution_pending'):w.addflag('KOR',P+f)
        w.call('on_native_election_resolved');assert c['leader']=='Kim Jong-pil' and w.flag('KOR',P+'kjp_successor')
    test('Kim Jong-pil nomination preserves Park until the actual winning DRP election result',kjp)
    def legalization():
        w=World(base);w.addflag('KOR',P+'negotiating_commitment');w.c['KOR']['v']['party_banned_array^5']=1;w.decide('legalize_civic_parties')
        assert w.flag('KOR',P+'civic_legal_5') and w.flag('KOR',P+'civic_legal_19') and w.c['KOR']['v']['party_banned_array^5']==0 and w.c['KOR']['v']['ruling_party']==0
    test('civic legalization opens lawful participation without appointing a government or adding votes',legalization)
    def labour():
        w=World(base);w.c['KOR']['v']['labour_unions_opinion']=23;w.addflag('KOR',P+'lawful_labour_bargaining');w.call('ensure_labour_representation');assert w.c['KOR']['v']['labour_unions_opinion']==33
        w.call('ensure_labour_representation');assert w.c['KOR']['v']['labour_unions_opinion']==33
    test('native labour representation preserves prior opinion and applies the recognition change once',labour)
    return tests

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--installed',action='store_true');a=ap.parse_args();base=ROOT if a.installed else HERE/'runtime_staged'
    tests=run(base);report={'status':'PASS','target':'installed' if a.installed else 'staged','tests':tests,'scope':'Executes emitted effects/triggers through a bounded source model with explicit native helper stand-ins; not an HOI4 engine, multiplayer transport or save test'}
    (DOC/'COLDWAR_KOR_runtime_scenarios.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))

if __name__=='__main__':main()
