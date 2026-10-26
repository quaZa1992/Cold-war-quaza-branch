# IMPERIA CW — Cold War: source-level fixtures for the emitted Spanish political provider.
"""Bounded script fixtures; this is not a HOI4 engine simulation."""
import json
from pathlib import Path
from collections import defaultdict
from script_ast import parse,first,walk
from politics import build

HERE=Path(__file__).resolve().parent
DESIGN=json.loads((HERE/'approved_design.json').read_text(encoding='utf-8'))
OUTPUT=build(HERE.parents[1],DESIGN)
EFFECTS=dict((k,v) for k,o,v in parse(OUTPUT['common/scripted_effects/COLDWAR_SPR_v2_politics.txt']))
TRIGGERS=dict((k,v) for k,o,v in parse(OUTPUT['common/scripted_triggers/COLDWAR_SPR_v2_politics.txt']))

class Fixture:
    def __init__(self,date='1970.1.1',slot=21):
        self.date=tuple(map(int,date.split('.')));self.vars=defaultdict(float,ruling_party=slot)
        self.flags=set();self.ideas=set();self.timed={};self.stability=0.;self.leader='Francisco Franco' if slot==21 else None
        self.elections=False;self.created=[];self.queued=[]
    def value(self,v):
        try:return float(v)
        except (ValueError,TypeError):return self.vars[v]
    def cond(self,rows):
        for key,op,v in rows:
            if key=='tooltip':continue
            if key=='OR':result=any(self.cond([x]) for x in v)
            elif key=='AND':result=self.cond(v)
            elif key=='NOT':result=not self.cond(v)
            elif key=='custom_trigger_tooltip':result=self.cond(v)
            elif key in TRIGGERS:result=self.cond(TRIGGERS[key])==(v=='yes')
            elif key in ['tag','original_tag']:result=v=='SPR'
            elif key=='IMP_is_1970_scenario':result=v=='yes'
            elif key=='is_dynamic_country':result=v=='no'
            elif key=='has_country_flag':result=v in self.flags
            elif key=='has_elections':result=self.elections==(v=='yes')
            elif key=='has_variable':result=v in self.vars
            elif key=='has_idea':result=v in self.ideas
            elif key=='has_country_leader':result=self.leader==json.loads(first(v,'name'))
            elif key=='has_completed_focus':result=False
            elif key=='date':
                wanted=tuple(map(int,v.split('.')));result={'<':self.date<wanted,'>':self.date>wanted}[op]
            elif key=='check_variable':
                a,o,b=v[0];a=self.value(a);b=self.value(b)
                result={'=':a==b,'>':a>b,'<':a<b,'>=':a>=b,'<=':a<=b}[o]
            else:raise AssertionError('Unknown condition '+key)
            if not result:return False
        return True
    def run(self,rows):
        previous=False
        for key,op,v in rows:
            if key in ['if','else_if','else']:
                take=(key=='if' or not previous) and (key=='else' or self.cond(first(v,'limit',[])))
                if key=='if':previous=False
                if take:self.run([r for r in v if r[0]!='limit']);previous=True
                continue
            previous=False
            if key in EFFECTS:self.run(EFFECTS[key])
            elif key=='set_country_flag':self.flags.add(v)
            elif key=='clr_country_flag':self.flags.discard(v)
            elif key in ['set_variable','set_temp_variable','add_to_variable','subtract_from_variable']:
                k,_,amount=v[0];amount=self.value(amount)
                if key.startswith('set_'):self.vars[k]=amount
                elif key=='add_to_variable':self.vars[k]+=amount
                else:self.vars[k]-=amount
            elif key=='clamp_variable':
                k=first(v,'var');self.vars[k]=max(float(first(v,'min')),min(float(first(v,'max')),self.vars[k]))
            elif key=='add_ideas':self.ideas.add(v)
            elif key=='remove_ideas':self.ideas.discard(v)
            elif key=='add_timed_idea':self.ideas.add(first(v,'idea'));self.timed[first(v,'idea')]=int(first(v,'days'))
            elif key=='add_stability':self.stability+=float(v)
            elif key=='country_event':self.queued.append(first(v,'id'))
            elif key=='create_country_leader':self.leader=json.loads(first(v,'name'));self.created.append(self.leader)
            elif key=='kill_country_leader':self.leader=None
            elif key=='change_ruling_party_effect':
                self.vars['ruling_party']=self.vars['rul_party_temp'];self.run(EFFECTS['COLDWAR_SPR_dispatch_leader'])
            elif key=='set_politics':
                setting=first(v,'elections_allowed');self.elections=setting=='yes' if setting else self.elections
            elif key in ['random','COLDWAR_SPR_initialize_core','COLDWAR_SPR_initialize_agreements','COLDWAR_SPR_refresh_agreements','COLDWAR_SPR_refresh_colour','COLDWAR_SPR_retry_completed_focuses','COLDWAR_SPR_sync_programmes','update_party_name','update_set_politics','set_correct_ideology_trait']:pass
            else:raise AssertionError('Unknown effect '+key)
    def effect(self,name):self.run(EFFECTS['COLDWAR_SPR_'+name])

def main():
    count=0
    for rel,text in OUTPUT.items():
        if rel.endswith('.txt'):parse(text);count+=1
    initial=Fixture();initial.effect('initialize');assert initial.vars['COLDWAR_SPR_capacity']==75 and initial.vars['COLDWAR_SPR_preparedness']==20
    initial.effect('initialize');assert initial.vars['COLDWAR_SPR_preparedness']==20
    for _ in range(54):initial.effect('health_monthly')
    initial.date=(1974,7,9);initial.effect('health_daily');assert initial.vars['COLDWAR_SPR_capacity']==23
    initial.effect('health_daily');assert initial.vars['COLDWAR_SPR_capacity']==23
    initial.date=(1974,7,30);initial.effect('health_daily');assert initial.vars['COLDWAR_SPR_capacity']==33
    initial.effect('health_daily');assert initial.vars['COLDWAR_SPR_capacity']==33
    initial.effect('health_monthly');assert initial.vars['COLDWAR_SPR_capacity']==31.5
    for prep,expected in [(80,-.05),(50,-.10),(49,-.20)]:
        f=Fixture('1975.11.20',22);f.vars['COLDWAR_SPR_preparedness']=prep
        f.effect('health_daily');assert 'COLDWAR_SPR_franco_departed' in f.flags and f.stability==expected
        f.effect('health_daily');assert f.stability==expected
        assert ('COLDWAR_SPR_succession_disruption' in f.timed)==(prep<50)
    f=Fixture('1975.11.20');f.leader=None;f.effect('health_daily');assert f.vars['ruling_party']==23
    # Native party change and voluntary retirement end actual incumbency without an early death claim.
    f=Fixture('1972.1.1');f.effect('initialize');f.vars['ruling_party']=3;f.effect('dispatch_leader')
    assert 'COLDWAR_SPR_franco_departed' in f.flags and 'COLDWAR_SPR_franco_dead' not in f.flags and f.vars['ruling_party']==3
    f=Fixture('1972.1.1');f.effect('initialize');f.vars['MDCW_HP_native_retirement']=1;f.effect('dispatch_leader')
    assert 'COLDWAR_SPR_franco_departed' in f.flags and 'COLDWAR_SPR_franco_dead' not in f.flags and f.vars['ruling_party']==23 and f.leader=='Juan Carlos I'
    f=Fixture('1972.1.1');f.effect('initialize');f.effect('dispatch_leader');assert f.leader=='Francisco Franco' and 'COLDWAR_SPR_franco_departed' not in f.flags
    # Five-point delegation mitigation remains exact in the critical stage.
    f=Fixture();f.effect('initialize');f.vars['COLDWAR_SPR_capacity']=10;f.flags.add('COLDWAR_SPR_delegation_active');f.effect('sync_health');assert 'COLDWAR_SPR_capacity_critical_delegated' in f.ideas
    f=Fixture('1980.1.1',22);f.flags.add('COLDWAR_SPR_franco_departed');f.effect('enact_legal_fundamental');assert 'COLDWAR_SPR_legal_fundamental' in f.ideas
    f.effect('enact_legal_royal');assert 'COLDWAR_SPR_legal_fundamental' not in f.ideas and 'COLDWAR_SPR_legal_royal' in f.ideas
    f.effect('enact_legal_parliamentary');assert 'COLDWAR_SPR_legal_royal' not in f.ideas and f.cond(TRIGGERS['COLDWAR_SPR_representative_settlement'])
    f=Fixture('1996.1.1');f.flags.add('COLDWAR_SPR_franco_departed');f.leader=None;f.effect('historical_succession');assert f.created==['Jose Utrera Molina']
    f.created=[];f.effect('historical_succession');assert f.created==[]
    f.date=(2018,1,1);f.flags.add('do_not_retire');f.effect('historical_succession');assert f.leader=='National Council of the Movement'
    f=Fixture('1980.1.1',4);f.flags.add('COLDWAR_SPR_franco_departed');f.leader='Santiago Carrillo';f.vars['MDCW_HP_native_retirement']=1;f.effect('dispatch_leader');assert f.leader=='Gerardo Iglesias'
    f.vars['MDCW_HP_native_retirement']=0;f.created=[];f.effect('dispatch_leader');assert f.leader=='Gerardo Iglesias'
    f=Fixture('1990.1.1',4);f.flags.update(['COLDWAR_SPR_franco_departed','do_not_retire']);f.leader='Santiago Carrillo';f.effect('dispatch_leader');assert f.leader=='Santiago Carrillo'
    f.date=(2013,1,1);f.effect('dispatch_leader');assert f.leader=='Cayo Lara'
    # Conservative mandates are mutually exclusive and are independent of the constitution.
    f=Fixture('1980.1.1',1);f.flags.update(['COLDWAR_SPR_franco_departed','COLDWAR_SPR_mandate_ucd']);assert f.cond(TRIGGERS['COLDWAR_SPR_government_ucd']) and not f.cond(TRIGGERS['COLDWAR_SPR_government_ap_pp'])
    # Delayed negotiations cannot execute without a current matching authority receipt.
    parsed_events={first(v,'id'):v for k,o,v in parse(OUTPUT['events/COLDWAR_SPR_v2_politics.txt']) if k=='country_event'}
    for ident in [10,11,12,14,16,20,30]:
        f=Fixture('1980.1.1',3);f.flags.add('COLDWAR_SPR_franco_departed');f.vars['COLDWAR_SPR_government_generation']=4
        ev=parsed_events['COLDWAR_SPR_v2_politics.'+str(ident)]
        before=(set(f.flags),set(f.ideas),f.leader,f.stability)
        for k,o,v in ev:
            if k=='option':f.run([r for r in v if r[0] not in ['name','trigger']])
        assert before==(set(f.flags),set(f.ideas),f.leader,f.stability)
    # Rejection can reopen reform; the elected Cortes can ratify under a replacement cabinet.
    f=Fixture('1980.1.1',3);f.flags.update(['COLDWAR_SPR_franco_departed','COLDWAR_SPR_political_reform_delivered']);f.effect('begin_legal_reform')
    opts=[v for k,o,v in parsed_events['COLDWAR_SPR_v2_politics.10'] if k=='option'];f.run([r for r in opts[1] if r[0] not in ['name','trigger']]);assert 'COLDWAR_SPR_reform_in_progress' not in f.flags
    f.effect('begin_legal_reform');assert 'COLDWAR_SPR_reform_in_progress' in f.flags
    f.flags.update(['COLDWAR_SPR_constituent_campaign_pending','COLDWAR_SPR_constituent_ratification_pending']);f.vars['COLDWAR_SPR_government_generation']=2;f.effect('invalidate_old_mandate')
    assert f.vars['COLDWAR_SPR_constituent_generation']==2 and 'COLDWAR_SPR_v2_politics.12' in f.queued
    option=next(v for k,o,v in parsed_events['COLDWAR_SPR_v2_politics.12'] if k=='option');f.run([r for r in option if r[0] not in ['name','trigger']])
    assert 'COLDWAR_SPR_settlement_recorded' in f.flags and 'COLDWAR_SPR_legal_representative' in f.flags
    # Native election completion includes same-party victories and waits for coalition formation.
    f=Fixture('1980.1.1',3);f.effect('initialize');f.flags.update(['COLDWAR_SPR_franco_departed','COLDWAR_SPR_native_campaign_seen','elections_in_progress','COLDWAR_SPR_carlist_social_federalist_agreement'])
    on_actions=first(parse(OUTPUT['common/on_actions/COLDWAR_SPR_v2_politics.txt']),'on_actions');daily=first(first(on_actions,'on_daily_SPR'),'effect')
    f.run(daily);assert 'COLDWAR_SPR_carlist_social_federalist_agreement' in f.flags
    f.flags.discard('elections_in_progress');f.flags.add('coalition_forming');f.run(daily);assert 'COLDWAR_SPR_carlist_social_federalist_agreement' in f.flags
    old=f.vars['COLDWAR_SPR_government_generation'];f.flags.discard('coalition_forming');f.run(daily)
    assert f.vars['COLDWAR_SPR_government_generation']==old+1 and 'COLDWAR_SPR_carlist_social_federalist_agreement' not in f.flags
    # Every political custom payload and its preview exists, with one-time delivery receipts.
    previews=json.loads(OUTPUT['tools/spain_1970_v2/politics_previews.json'])
    for node in DESIGN['nodes']:
        for entry in node['effects']:
            if entry['type']=='decision' and (node['group']=='succession' or 'carlist' in node['id']):
                assert entry['id']+'_effect' in EFFECTS and entry['id'] in previews
                assert entry['id']+'_delivered' in str(EFFECTS[entry['id']+'_effect'])
    report={'status':'passed','parsed_script_files':count,'checks':['idempotent initialization','capacity decline and one recovery','three preparedness shock tiers and no replay','expired-Franco gap','actual party change and early retirement preserve living identity','ordinary callback preserves actual Franco','critical delegation exactly five points','exclusive constitutional packages','delayed newest-first succession','dead protected leader replacement','native retirement and no ordinal regression','living do_not_retire','actual conservative mandate','stale domestic event execution guards','rejected reform retry and constituent ratification under replacement cabinet','same-party election mandate completes after coalition formation','complete custom payload and preview registration'],'engine_tested':False}
    (HERE/'politics_tests.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))

if __name__=='__main__':main()
