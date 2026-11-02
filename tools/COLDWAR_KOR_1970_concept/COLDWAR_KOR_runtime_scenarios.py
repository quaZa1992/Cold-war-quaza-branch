# IMPERIA COLD WAR — Cold War: bounded scenarios executing emitted Korean scripts.
"""A fail-closed source interpreter, not the game engine or network simulator."""
from pathlib import Path
from copy import deepcopy
from datetime import date
import argparse,json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];DOC=ROOT/'docs/design/COLDWAR_KOR_1970'
STAGE=Path(r'E:\HOI4_Mod_Tools\mdcoldwar\runtime\quaza_eastasia_20261027\kor_stage')
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,values,walk
from COLDWAR_KOR_alliance_revision import load_design
from COLDWAR_KOR_runtime_politics import build as build_politics
from COLDWAR_KOR_reward_revision import BUILDING_METADATA
P='COLDWAR_KOR_'

class World:
    def __init__(self,base):
        self.e={};self.t={};self.dm={};self.events={};self.decisions={};self.day=0;self.current_date='1970.1.1';self.wars=set();self.queue=[];self.scopes=[]
        self.c={tag:{'v':{'ruling_party':0 if tag=='KOR' else 1,'treasury':0,'current_term':0},'tmp':{},'flags':{},'ideas':set(),'idea_until':{},'access':set(),'dm':set(),'leader':'Park Chung Hee' if tag=='KOR' else tag,'elections':False,'subject':False,'slot_grants':{},'pending_slots':{},'buildings':{},'state_buildings':{},'equipment_bonuses':[],'tech_bonuses':[],'doctrine_bonuses':[]} for tag in ('KOR','NKO','USA','JAP','SOV','CHI','SVN','GER','SAU','IRQ')}
        # GDP-backed national focus charges use a round 100B scenario fixture;
        # tests for missing GDP explicitly remove this variable.
        self.c['KOR']['v']['gdp_total']=100
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
    def trigger(self,rows,tag='KOR',state=None):
        for k,op,v in rows:
            c=self.c[tag]
            if k in self.t:r=self.trigger(self.t[k],tag,state)==(v=='yes')
            elif k in self.c:r=self.trigger(v,k,None)
            elif k=='AND' or k=='hidden_trigger':r=self.trigger(v,tag,state)
            elif k=='OR':r=any(self.trigger([a],tag,state) for a in v)
            elif k=='NOT':r=not self.trigger(v,tag,state)
            elif k in ('tag','original_tag'):r=tag==v
            elif k=='IMP_is_1970_scenario':r=v=='yes'
            elif k=='exists':r=v=='yes'
            elif k=='country_exists':r=v in self.c
            elif k=='is_subject':r=c['subject']==(v=='yes')
            elif k in ('is_owned_by','is_controlled_by'):r=v=='ROOT'
            elif k=='free_building_slots':r=True
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
            elif k.isdigit():r=self.trigger(v,tag,k)
            elif k in BUILDING_METADATA and state is not None:
                spec=BUILDING_METADATA[k]
                current=c['state_buildings'].get((state,k),0)+c['buildings'].get((state,k),0)
                group=spec['group_by']
                if group:
                    current=sum(amount for (building_state,building),amount in c['state_buildings'].items()
                                if building_state==state and BUILDING_METADATA.get(building,{}).get('group_by')==group)
                    current+=sum(amount for (building_state,building),amount in c['buildings'].items()
                                 if building_state==state and BUILDING_METADATA.get(building,{}).get('group_by')==group)
                r=current>float(v) if op=='>' else current<float(v)
            elif k=='check_variable':
                if first(v,'var') is not None:
                    lhs=self.value(first(v,'var'),tag);rhs=self.value(first(v,'value'),tag);cmp=first(v,'compare','equals')
                    cmp={'equals':'=','not_equals':'!=','greater_than':'>','less_than':'<','greater_than_or_equals':'>=','less_than_or_equals':'<='}.get(cmp,cmp)
                else:
                    a,cmp,b=v[0];lhs=self.value(a,tag);rhs=self.value(b,tag)
                r={'=':lhs==rhs,'!=':lhs!=rhs,'>':lhs>rhs,'<':lhs<rhs,'>=':lhs>=rhs,'<=':lhs<=rhs}[cmp]
            elif k=='custom_trigger_tooltip':r=self.trigger([a for a in v if a[0] not in ('tooltip','not_tooltip')],tag,state)
            elif k=='is_special_project_completed':r=False
            elif k=='date':
                lhs=date(*map(int,self.current_date.split('.')));rhs=date(*map(int,v.split('.')))
                r={'>':lhs>rhs,'<':lhs<rhs,'=':lhs==rhs,'>=':lhs>=rhs,'<=':lhs<=rhs}.get(op,False)
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
            elif k in ('set_variable','set_temp_variable','add_to_variable','add_to_temp_variable','subtract_from_variable','subtract_from_temp_variable','multiply_variable','divide_variable'):
                a,o,b=v[0];target=c['tmp'] if 'temp' in k else c['v'];val=self.value(b,tag)
                target[a]=target.get(a,0)+val if k.startswith('add_') else target.get(a,0)-val if k.startswith(('subtract_','subtract_from_')) else target.get(a,0)*val if k.startswith('multiply_') else target.get(a,0)/val if k.startswith('divide_') else val
            elif k=='modify_treasury_effect':c['v']['treasury']+=self.value('treasury_change',tag)
            elif k=='add_dynamic_modifier':c['dm'].add(first(v,'modifier'))
            elif k=='remove_dynamic_modifier':c['dm'].discard(first(v,'modifier'))
            elif k=='add_ideas':
                c['ideas'].add(v)
                if v=='labour_unions':c['v']['labour_unions_opinion']=60
            elif k=='remove_ideas':c['ideas'].discard(v);c['idea_until'].pop(v,None)
            elif k=='add_timed_idea':
                id=first(v,'idea');c['ideas'].add(id);c['idea_until'][id]=self.day+int(first(v,'days','0'))
            elif k=='add_equipment_bonus':
                c['equipment_bonuses'].append((first(v,'name'),deepcopy(first(v,'bonus',[]))))
            elif k=='add_tech_bonus':
                c['tech_bonuses'].append({key:value for key,_,value in v})
            elif k=='add_doctrine_cost_reduction':
                c['doctrine_bonuses'].append({key:value for key,_,value in v})
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
            elif k.isdigit():
                for effect,_,body in v:
                    if effect=='add_extra_state_shared_building_slots':
                        level=int(body);assert level>0,(tag,k,effect,body)
                        c['slot_grants'][k]=c['slot_grants'].get(k,0)+level
                        c['pending_slots'][k]=c['pending_slots'].get(k,0)+level
                    elif effect=='add_building_construction':
                        level=int(first(body,'level','1'))
                        assert c['pending_slots'].get(k,0)>=level,(tag,k,first(body,'type'),level,c['pending_slots'])
                        c['pending_slots'][k]-=level
                        key=(k,first(body,'type'))
                        c['buildings'][key]=c['buildings'].get(key,0)+level
                    else:raise ValueError('Unmodelled state effect '+effect+' in '+tag)
            else:raise ValueError('Unmodelled effect '+k+' in '+tag)
    def call(self,name,tag='KOR'):self.execute(self.e[P+name],tag)
    def event_immediate(self,id,tag='KOR'):self.execute(first(self.events[id],'immediate',[]),tag)
    def deliver_due_events(self):
        fired=[];pending=[]
        for tag,event_id,due in self.queue:
            if due>self.day:
                pending.append((tag,event_id,due));continue
            event=self.events.get(event_id)
            if event and self.trigger(first(event,'trigger',[]),tag):
                self.execute(first(event,'immediate',[]),tag);fired.append(event_id)
        self.queue=pending
        return fired
    def option(self,id,index=0,tag='KOR'):
        b=values(self.events[id],'option')[index]
        assert self.trigger(first(b,'trigger',[]),tag),(id,index,'option unavailable')
        self.execute([a for a in b if a[0] not in ('name','trigger')],tag)
        self.queue=[item for item in self.queue if not (item[0]==tag and item[1]==id)]
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
    def use_generated_politics(self):
        files,_=build_politics(load_design())
        effect_path='common/scripted_effects/COLDWAR_KOR_1970_politics.txt'
        for key,_,body in parse(files[effect_path]):self.e[key]=body
        event_path='events/COLDWAR_KOR_1970_politics.txt'
        for event in values(parse(files[event_path]),'country_event'):
            self.events[first(event,'id')]=event

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
    def building_slots():
        w=World(base);c=w.c['KOR'];c['v']['gdp_total']=100
        w.call('complete_balanced_provinces')
        assert c['v']['treasury']==-.5,c['v']['treasury']
        assert c['slot_grants']=={'606':1,'607':1},c['slot_grants']
        assert c['pending_slots']=={'606':0,'607':0},c['pending_slots']
        assert c['buildings']=={('606','infrastructure'):1,('607','infrastructure'):1},c['buildings']
        paid=(c['v']['treasury'],deepcopy(c['slot_grants']),deepcopy(c['pending_slots']),deepcopy(c['buildings']))
        w.call('complete_balanced_provinces')
        assert paid==(c['v']['treasury'],c['slot_grants'],c['pending_slots'],c['buildings'])
    test('balanced provinces charges 0.5B at GDP 100; per-level state slots precede each construction and replay grants nothing twice',building_slots)
    def project_gdp_transaction():
        w=World(base);c=w.c['KOR'];c['v']['gdp_total']=100
        c['state_buildings'][('605','industrial_complex')]=48
        assert w.trigger(w.t[P+'can_pohang_foundry'])
        w.call('complete_pohang_foundry')
        assert abs(c['v']['treasury']+1.75)<1e-8,c['v']['treasury']
        assert c['slot_grants']=={'605':2},c['slot_grants']
        assert c['pending_slots']=={'605':0},c['pending_slots']
        assert c['buildings']=={('605','industrial_complex'):2},c['buildings']
        assert c['state_buildings'][('605','industrial_complex')]+c['buildings'][('605','industrial_complex')]==50
        paid=(c['v']['treasury'],deepcopy(c['slot_grants']),deepcopy(c['buildings']))
        w.call('complete_pohang_foundry')
        assert paid==(c['v']['treasury'],c['slot_grants'],c['buildings'])
        capped=World(base);crowded=capped.c['KOR'];crowded['v']['gdp_total']=100
        crowded['state_buildings'][('605','industrial_complex')]=49
        assert not capped.trigger(capped.t[P+'can_pohang_foundry'])
        capped.call('complete_pohang_foundry')
        assert crowded['v']['treasury']==0 and not capped.flag('KOR',P+'pohang_foundry_paid')
        assert crowded['slot_grants']=={} and crowded['buildings']=={}
        no_gdp=World(base);empty=no_gdp.c['KOR'];empty['v'].pop('gdp_total')
        no_gdp.call('complete_pohang_foundry')
        assert empty['v']['treasury']==0,empty['v']['treasury']
        assert not no_gdp.flag('KOR',P+'pohang_foundry_paid')
        assert empty['slot_grants']=={} and empty['pending_slots']=={} and empty['buildings']=={}
        assert empty['equipment_bonuses']==[] and empty['tech_bonuses']==[] and empty['doctrine_bonuses']==[]
        base_only=World(base);base_country=base_only.c['KOR'];base_country['v'].pop('gdp_total')
        assert not base_only.trigger(base_only.t[P+'can_third_plan'])
        base_only.call('complete_third_plan')
        assert base_country['v']['treasury']==0 and not base_only.flag('KOR',P+'third_plan_paid')
        assert not any(k.startswith(P+'third_plan_') for k in base_country['v'])
    test('emitted Pohang trigger accepts 48/50 and rejects 49/50 before its 1.75B GDP-based charge, two factory levels, and two slots; zero GDP withholds the entire transaction',project_gdp_transaction)
    def equipment_bonus_party_cycle():
        w=World(base);c=w.c['KOR']
        c['v']['gdp_total']=100
        w.call('complete_changwon_production')
        assert len(c['equipment_bonuses'])==1 and c['equipment_bonuses'][0][0]==P+'changwon_production',c['equipment_bonuses']
        equipment=c['equipment_bonuses'][0][1]
        families={key:value for key,_,value in equipment}
        assert first(families['infantry_weapons_type'],'build_cost_ic')=='-0.06'
        assert first(families['artillery_equipment'],'build_cost_ic')=='-0.04'
        assert [b['name'] for b in c['tech_bonuses']]==[P+'changwon_small_arms',P+'changwon_artillery']
        assert all(b.get('uses')=='1' and b.get('bonus')=='0.5' for b in c['tech_bonuses'])
        w.call('complete_changwon_production')
        assert len(c['equipment_bonuses'])==1 and len(c['tech_bonuses'])==2
        w.call('complete_chaebol_compact');assert P+'chaebol_compact_programme' in c['dm']
        paid=(c['v']['treasury'],deepcopy(c['slot_grants']),deepcopy(c['buildings']),deepcopy(c['equipment_bonuses']),deepcopy(c['tech_bonuses']))
        c['v']['ruling_party']=1;w.call('refresh_programmes')
        assert P+'chaebol_compact_programme' not in c['dm']
        assert len(c['equipment_bonuses'])==1 and len(c['tech_bonuses'])==2
        c['v']['ruling_party']=0;w.call('refresh_programmes')
        assert P+'chaebol_compact_programme' in c['dm']
        w.call('complete_changwon_production')
        assert paid==(c['v']['treasury'],c['slot_grants'],c['buildings'],c['equipment_bonuses'],c['tech_bonuses'])
    test('emitted Changwon cost and finite research bonuses persist once across replay and a party programme departure/return',equipment_bonus_party_cycle)
    def generated_political_dispatch():
        generated_files,_=build_politics(load_design())
        political_events={first(event,'id'):event for event in values(parse(generated_files['events/COLDWAR_KOR_1970_politics.txt']),'country_event')}
        political_effects={key:body for key,_,body in parse(generated_files['common/scripted_effects/COLDWAR_KOR_1970_politics.txt'])}
        daily=political_effects[P+'politics_daily'];dispatch_rows=[]
        def find_dispatch(rows):
            for key,_,body in rows:
                if key=='if':
                    limit=first(body,'limit',[]);actions=[row for row in body if row[0]!='limit']
                    ids=[first(effect,'id') for action,_,effect in actions if action=='country_event' and isinstance(effect,list)]
                    for event_id in ids:dispatch_rows.append((event_id,limit,actions))
                    find_dispatch(actions)
                elif isinstance(body,list):find_dispatch(body)
        find_dispatch(daily)
        auto_ids=['COLDWAR_KOR_transition.100']+[f'COLDWAR_KOR_transition.{i}' for i in range(101,115)]
        for event_id in auto_ids:
            event=political_events[event_id];number=event_id.rsplit('.',1)[1]
            queue=f'COLDWAR_KOR_transition_{number}_dispatch_queued';delivered=f'COLDWAR_KOR_transition_{number}_delivered'
            assert first(event,'is_triggered_only')=='yes' and first(event,'mean_time_to_happen') is None,event_id
            scheduled=[(limit,actions) for eid,limit,actions in dispatch_rows if eid==event_id]
            assert len(scheduled)==1,(event_id,len(scheduled))
            limit,actions=scheduled[0]
            limit_without_receipts=[row for row in limit if not (row[0]=='NOT' and first(row[2],'has_country_flag') in (queue,delivered))]
            assert limit_without_receipts==first(event,'trigger',[]),event_id
            assert any(key=='set_country_flag' and first(body,'flag')==queue and first(body,'days')=='2' for key,_,body in actions),event_id
            call=next(body for key,_,body in actions if key=='country_event' and first(body,'id')==event_id)
            assert first(call,'days')=='1',event_id
            options=values(event,'option')
            assert first(first(event,'immediate',[]),'set_country_flag')==delivered,event_id
            assert len(options)==2 and all(all(any(key=='clr_country_flag' and body==flag for key,_,body in walk(option)) for flag in (queue,delivered)) for option in options),event_id
        assert not [event_id for event_id,event in political_events.items() if first(event,'mean_time_to_happen') is not None]
        def ready(date_value='1971.4.28'):
            w=World(base);w.use_generated_politics();w.current_date=date_value
            w.c['KOR']['leader']='Park Chung Hee';w.c['KOR']['v']['stability']=.5
            return w
        def queued(w,eid):return [item for item in w.queue if item[1]==eid]
        empty=ready('1971.4.27');empty.call('politics_daily')
        assert not queued(empty,'COLDWAR_KOR_transition.102')
        human=ready();before=(human.c['KOR']['v'].get('add_political_power',0),human.c['KOR']['v']['stability'])
        human.call('politics_daily');first_queue=queued(human,'COLDWAR_KOR_transition.102')
        assert len(first_queue)==1 and first_queue[0][2]==1 and human.flag('KOR','COLDWAR_KOR_transition_102_dispatch_queued')
        assert not human.flag('KOR','COLDWAR_KOR_transition_1971_recorded')
        assert before==(human.c['KOR']['v'].get('add_political_power',0),human.c['KOR']['v']['stability'])
        human.call('politics_daily');assert len(queued(human,'COLDWAR_KOR_transition.102'))==1
        human.day=1;human.current_date='1971.4.29';assert human.deliver_due_events()==['COLDWAR_KOR_transition.102']
        assert human.flag('KOR','COLDWAR_KOR_transition_102_delivered')
        human.day=4;human.current_date='1971.5.2';human.call('politics_daily')
        assert not queued(human,'COLDWAR_KOR_transition.102')
        assert not human.flag('KOR','COLDWAR_KOR_transition_1971_recorded')
        human.option('COLDWAR_KOR_transition.102',0)
        assert human.flag('KOR','COLDWAR_KOR_transition_1971_recorded')
        assert human.flag('KOR','COLDWAR_KOR_electoral_opening') and human.c['KOR']['v']['add_stability']==.03
        assert not human.flag('KOR','COLDWAR_KOR_transition_102_dispatch_queued') and not human.flag('KOR','COLDWAR_KOR_transition_102_delivered')
        human.call('politics_daily');assert not queued(human,'COLDWAR_KOR_transition.102')
        ai=ready();ai.call('politics_daily');assert len(queued(ai,'COLDWAR_KOR_transition.102'))==1
        ai.day=1;ai.current_date='1971.4.29';assert ai.deliver_due_events()==['COLDWAR_KOR_transition.102'];ai.option('COLDWAR_KOR_transition.102',1)
        assert ai.flag('KOR','COLDWAR_KOR_transition_1971_recorded') and ai.flag('KOR','COLDWAR_KOR_executive_emergency_proposed')
        assert ai.c['KOR']['v']['add_stability']==-.05 and not ai.flag('KOR','COLDWAR_KOR_transition_102_dispatch_queued') and not ai.flag('KOR','COLDWAR_KOR_transition_102_delivered')
        dropped=ready();dropped.call('politics_daily');assert len(queued(dropped,'COLDWAR_KOR_transition.102'))==1
        dropped.day=1;dropped.current_date='1971.4.29';dropped.c['KOR']['flags'].pop('COLDWAR_KOR_1971_contest_pending')
        assert dropped.deliver_due_events()==[] and not dropped.flag('KOR','COLDWAR_KOR_transition_102_delivered')
        dropped.day=2;dropped.c['KOR']['flags']['COLDWAR_KOR_1971_contest_pending']=None;dropped.call('politics_daily')
        assert len(queued(dropped,'COLDWAR_KOR_transition.102'))==1 and dropped.flag('KOR','COLDWAR_KOR_transition_102_dispatch_queued')
        replay=ready('1979.10.26');replay.addflag('KOR','COLDWAR_KOR_park_succession_unresolved');replay.call('politics_daily')
        first100=queued(replay,'COLDWAR_KOR_transition.100');assert len(first100)==1 and first100[0][2]==1
        replay.call('politics_daily');assert len(queued(replay,'COLDWAR_KOR_transition.100'))==1
        assert replay.flag('KOR','COLDWAR_KOR_park_succession_unresolved')
        replay.day=1;replay.current_date='1979.10.27';assert replay.deliver_due_events()==['COLDWAR_KOR_transition.100'];replay.option('COLDWAR_KOR_transition.100',1)
        assert not replay.flag('KOR','COLDWAR_KOR_park_succession_unresolved')
        assert replay.flag('KOR','COLDWAR_KOR_officer_council_contest') and not replay.flag('KOR','COLDWAR_KOR_transition_100_dispatch_queued') and not replay.flag('KOR','COLDWAR_KOR_transition_100_delivered')
    test('generated dated politics dispatch: exact trigger, next-day queue, empty and replay safety, human choice and AI option outcomes',generated_political_dispatch)
    return tests

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--installed',action='store_true');a=ap.parse_args();base=ROOT if a.installed else STAGE
    tests=run(base);report={'project':'IMPERIA COLD WAR','status':'PASS','target':'installed' if a.installed else 'staged','tests':tests,'scope':'Executes emitted effects/triggers through a bounded source model with explicit native helper stand-ins; not an HOI4 engine, multiplayer transport or save test'}
    (DOC/'COLDWAR_KOR_runtime_scenarios.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))

if __name__=='__main__':main()
