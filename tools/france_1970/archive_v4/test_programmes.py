# IMPERIA COLD WAR — Source-model regression checks for French programmes.
"""Exercise emitted script AST. This deliberately does not claim engine execution."""
from pathlib import Path
from collections import defaultdict
from decimal import Decimal
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse, first, values
D=json.loads((HERE/'approved_design.json').read_text(encoding='utf-8'))
def read(path):return parse((ROOT/path).read_text(encoding='utf-8-sig'))
E={k:v for k,o,v in read('common/scripted_effects/COLDWAR_FRA_1970_effects.txt')}
T={k:v for k,o,v in read('common/scripted_triggers/COLDWAR_FRA_1970_triggers.txt')}
def date(s):return tuple(map(int,s.split('.')))
def number(s):
    try:return Decimal(str(s))
    except Exception:return None

class Country:
    def __init__(self, group='gaullist', dlcs=()):
        self.flags=set();self.ideas=set();self.dynamic=set();self.variables=defaultdict(Decimal)
        self.tech=set();self.projects={'sp_armoured_vehicle_project','sp_aircraft_project','sp_naval_vessel_project'}
        self.dlcs=set(dlcs);self.day=date('1970.1.1');self.pp=Decimal(0);self.awards=[];self.xp=defaultdict(Decimal);self.stability=Decimal(0)
        self.switch(group)
    def switch(self, group):
        gate=next(n['party_gate'] for n in D['nodes'] if n['group']==group)
        self.variables['ruling_party']=Decimal(gate.get('ruling_party_equals',1))
        self.day=date('1973.1.1' if group=='national' else '1970.1.1')
    def value(self,s):
        n=number(s)
        return n if n is not None else self.variables[s]
    def condition(self, rows, any_=False):
        result=[]
        for k,o,v in rows:
            if k=='OR':r=self.condition(v,True)
            elif k in ('AND','hidden_trigger','limit','custom_trigger_tooltip'):r=self.condition(v)
            elif k=='NOT':r=not self.condition(v)
            elif k in T:r=self.condition(T[k]) == (v=='yes')
            elif k=='has_country_flag':r=v in self.flags
            elif k=='has_idea':r=v in self.ideas
            elif k=='has_dynamic_modifier':r=first(v,'modifier') in self.dynamic
            elif k=='has_tech':r=v in self.tech
            elif k=='has_dlc':r=v.strip('"') in self.dlcs
            elif k=='is_special_project_completed':r=v.removeprefix('sp:') in self.projects
            elif k=='date':r=(self.day<date(v)) if o=='<' else (self.day>date(v))
            elif k=='check_variable':
                if first(v,'var'):
                    a=self.value(first(v,'var'));b=self.value(first(v,'value'));op=first(v,'compare','equals')
                    r={'equals':a==b,'greater_than_or_equals':a>=b,'less_than':a<b}[op]
                else:
                    a,op,b=v[0];a=self.value(a);b=self.value(b)
                    r=(a==b) if op=='=' else ((a>b) if op=='>' else (a<b))
            elif k in ('tag','original_tag'):r=v=='FRA'
            elif k in ('exists','IMP_is_1970_scenario','always'):r=v=='yes'
            elif k=='tooltip':continue
            else:raise AssertionError('Unsupported model trigger '+str((k,o,v)))
            result.append(r)
        return any(result) if any_ else all(result)
    def execute(self,rows):
        previous=None
        for k,o,v in rows:
            if k=='if':
                previous=self.condition(first(v,'limit',[]))
                if previous:self.execute([r for r in v if r[0]!='limit'])
            elif k=='else':
                if previous is False:self.execute(v)
                previous=None
            elif k=='set_variable':
                a,o,b=v[0];self.variables[a]=self.value(b)
            elif k=='add_to_variable':
                a,o,b=v[0];self.variables[a]+=self.value(b)
            elif k=='set_country_flag':self.flags.add(v)
            elif k=='clr_country_flag':self.flags.discard(v)
            elif k=='add_ideas':self.ideas.add(v)
            elif k=='remove_ideas':self.ideas.discard(v)
            elif k=='swap_ideas':self.ideas.discard(first(v,'remove_idea'));self.ideas.add(first(v,'add_idea'))
            elif k=='add_dynamic_modifier':self.dynamic.add(first(v,'modifier'))
            elif k=='remove_dynamic_modifier':self.dynamic.discard(first(v,'modifier'))
            elif k=='add_political_power':self.pp+=self.value(v)
            elif k=='add_stability':self.stability+=self.value(v)
            elif k=='add_tech_bonus':self.awards.append(v)
            elif k in ('army_experience','navy_experience','air_experience'):self.xp[k]+=self.value(v)
            elif k=='COLDWAR_FRA_offer_maintenance':pass # Separate recipient/consent source review owns this helper.
            elif k in E:self.execute(E[k])
            elif k in ('force_update_dynamic_modifier','mark_focus_tree_layout_dirty'):pass
            else:raise AssertionError('Unsupported model effect '+str((k,o,v)))
    def call(self,k):self.execute(E[k])
    def snapshot(self):return (self.pp,list(self.awards),dict(self.xp),self.stability,set(self.ideas))

checks=0
def check(ok,message):
    global checks
    checks+=1
    assert ok,message

for n in D['nodes']:
    for dlcs in [(),('No Step Back','By Blood Alone')]:
        c=Country(n['group'],dlcs)
        c.ideas={s['id'] for s in D['spirits']}
        for parents in n['parents']:c.flags.add('COLDWAR_FRA_'+parents[0]+'_earned')
        c.call('COLDWAR_FRA_apply_'+n['key'])
        check(n['id']+'_earned' in c.flags,'Valid completion rejected: '+n['key'])
        check(c.pp==n['pp'],'Wrong charged PP: '+n['key'])
        check(len(c.awards)==sum(e['kind']=='tech_bonus' for e in n['one_time_effects']),'DLC research award count: '+n['key'])
        for t in n['transitions']:
            check(t['source'] not in c.ideas,'Original spirit retained: '+n['key'])
            if t['target']:check(t['target'] in c.ideas,'Residual spirit missing: '+n['key'])
        before=c.snapshot();c.call('COLDWAR_FRA_apply_'+n['key'])
        check(c.snapshot()==before,'Replayed one-time award: '+n['key'])
        c.call('COLDWAR_FRA_refresh_programmes');check(c.snapshot()==before,'Refresh replayed grant: '+n['key'])
        if n['group']!='institutions':
            c=Country(n['group'],dlcs)
            for parents in n['parents']:c.flags.add('COLDWAR_FRA_'+parents[0]+'_earned')
            c.variables['ruling_party']=Decimal(999)
            c.call('COLDWAR_FRA_apply_'+n['key'])
            check(n['id']+'_earned' not in c.flags and c.pp==0 and not c.awards,'Wrong government earned rewards: '+n['key'])
        for excluded in n['exclusive']:
            c=Country(n['group'],dlcs)
            for parents in n['parents']:c.flags.add('COLDWAR_FRA_'+parents[0]+'_earned')
            c.flags.add('COLDWAR_FRA_'+excluded+'_earned')
            c.call('COLDWAR_FRA_apply_'+n['key'])
            check(n['id']+'_earned' not in c.flags and c.pp==0,'Excluded completion executed: '+n['key'])
        for research in [e for e in n['one_time_effects'] if e.get('target_variants')]:
            active=next(v for v in research['target_variants'] if all((value in dlcs) if key=='has_dlc' else (value not in dlcs) for key,value in v.get('when',{}).items()))
            c=Country(n['group'],dlcs)
            for parents in n['parents']:c.flags.add('COLDWAR_FRA_'+parents[0]+'_earned')
            c.tech.update(active['technologies']);c.call('COLDWAR_FRA_apply_'+n['key'])
            check(n['id']+'_earned' not in c.flags and c.pp==0 and not c.awards,'Exhausted research charged or granted: '+n['key'])
            if active.get('required_projects'):
                c=Country(n['group'],dlcs)
                for parents in n['parents']:c.flags.add('COLDWAR_FRA_'+parents[0]+'_earned')
                c.projects.clear();c.call('COLDWAR_FRA_apply_'+n['key'])
                check(n['id']+'_earned' not in c.flags and c.pp==0 and not c.awards,'Missing project research granted: '+n['key'])

for g in D['groups']:
    gid=g['id']; programme='COLDWAR_FRA_'+gid+'_programme'
    for route in g['variants']:
        c=Country(gid)
        c.flags.update('COLDWAR_FRA_'+k+'_earned' for k in route['focuses'])
        c.call('COLDWAR_FRA_refresh_programmes')
        for m,v in route['mods'].items():
            check(abs(c.variables['COLDWAR_FRA_'+gid+'_'+m]-Decimal(str(v)))<Decimal('0.000001'),'Wrong active sum: '+gid)
        check(programme in c.dynamic,'Programme not attached: '+gid)
        before=dict(c.variables);c.variables['ruling_party']=Decimal(999);c.call('COLDWAR_FRA_refresh_programmes')
        check((programme in c.dynamic)==(gid=='institutions'),'Programme ownership failed: '+gid)
        c.switch(gid);c.call('COLDWAR_FRA_refresh_programmes')
        check(programme in c.dynamic,'Programme did not return: '+gid)
        check(all(c.variables['COLDWAR_FRA_'+gid+'_'+m]==before['COLDWAR_FRA_'+gid+'_'+m] for m in route['mods']),'Return stacked programme: '+gid)
        check(c.pp==0 and not c.awards and not c.xp,'Return replayed finite award: '+gid)

# Start spirits initialize once; a resolved spirit is never re-created by daily init.
c=Country();c.call('COLDWAR_FRA_1970_initialize')
check(c.ideas=={s['id'] for s in D['spirits']},'Wrong initial ideas')
c.ideas.remove('COLDWAR_FRA_unsettled_social_compromise');c.call('COLDWAR_FRA_1970_initialize')
check('COLDWAR_FRA_unsettled_social_compromise' not in c.ideas,'Initializer revived resolved starting malus')
# Dated CID/FN are separate earned ledgers despite sharing native slot 20.
c=Country('cid');c.flags.add('COLDWAR_FRA_shopkeepers_voice_earned');c.call('COLDWAR_FRA_refresh_programmes')
check('COLDWAR_FRA_cid_programme' in c.dynamic,'CID unavailable before FN foundation')
c.day=date('1972.10.5');c.call('COLDWAR_FRA_refresh_programmes')
check('COLDWAR_FRA_cid_programme' not in c.dynamic and 'COLDWAR_FRA_national_programme' not in c.dynamic,'Dated identity leaked CID rewards to FN')

report={'project':'IMPERIA COLD WAR','kind':'Emitted AST source-model tests; not HOI4','checks':checks,'focuses':234,'dlc_configurations':2,'compatible_routes':sum(len(g['variants']) for g in D['groups']),'result':'pass'}
(HERE/'PROGRAMME_TESTS.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
