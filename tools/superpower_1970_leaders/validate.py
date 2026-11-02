# IMPERIA COLD WAR — Bounded validation of USA and Soviet candidate selections.
"""Parse current files and execute their selection logic in a bounded model, not HOI4."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from multiplayer_quality.audit import parse
from superpower_1970_leaders.build import P, TRIG, PROFILES, PEOPLE, ident
from superpower_1970_leaders.integration import adapt


def first(tree,key,default=None): return next((v for k,o,v in tree if k==key),default)
def walk(tree):
    for k,o,v in tree:
        yield k,o,v
        if isinstance(v,list): yield from walk(v)
def unquote(value): return value.strip('"')


class Model:
    def __init__(self,effects,triggers,tag='USA',party=1,year=1970):
        self.effects,self.triggers=effects,triggers
        self.tag,self.party,self.year=tag,party,year
        self.variables={'ruling_party':party}
        self.flags,self.globals=set(),set()
        self.leader='';self.portrait=''; self.creations=self.retirements=self.callbacks=0
        self.human=self.exists=self.scenario=True; self.dynamic=False
    def number(self,v):
        try:return float(v)
        except ValueError:return self.variables.get(v,0)
    def condition(self,tree):
        def check(k,o,v):
            if k=='OR':return any(check(*r) for r in v)
            if k in ('AND','hidden_trigger'):return self.condition(v)
            if k=='NOT':return not self.condition(v)
            if k=='original_tag':return v==self.tag
            if k=='exists':return self.exists==(v=='yes')
            if k=='is_dynamic_country':return self.dynamic==(v=='yes')
            if k=='IMP_is_1970_scenario':return self.scenario==(v=='yes')
            if k=='is_ai':return (not self.human)==(v=='yes')
            if k in self.triggers:return self.condition(self.triggers[k])==(v=='yes')
            if k in [t+'_are_in_power' for t in TRIG]:return k==TRIG[self.party]+'_are_in_power' and v=='yes'
            if k=='has_country_flag':return v in self.flags
            if k=='has_global_flag':return v in self.globals
            if k=='has_variable':return v in self.variables
            if k=='has_country_leader':return unquote(first(v,'name'))==self.leader
            if k=='check_variable':
                return all((self.number(a)>self.number(b) if op=='>' else self.number(a)<self.number(b) if op=='<' else self.number(a)==self.number(b)) for a,op,b in v)
            if k=='date':
                now=(self.year,1,1); other=tuple(map(int,v.split('.')))
                return now>other if o=='>' else now<other
            raise AssertionError('Uninterpreted trigger '+k)
        return all(check(*r) for r in tree)
    def run(self,tree,depth=0):
        assert depth<30
        chain=False
        for k,o,v in tree:
            if k in ('if','else_if','else'):
                if k=='if':chain=False
                if not chain and (k=='else' or self.condition(first(v,'limit',[]))):
                    self.run([r for r in v if r[0]!='limit'],depth+1);chain=True
            elif k in self.effects:self.run(self.effects[k],depth+1)
            elif k=='hidden_effect':self.run(v,depth+1)
            elif k in ('set_variable','add_to_variable'):
                for a,op,z in v:self.variables[a]=self.number(z)+(self.variables.get(a,0) if k=='add_to_variable' else 0)
            elif k=='set_country_flag':self.flags.add(v)
            elif k=='clr_country_flag':self.flags.discard(v)
            elif k=='set_global_flag':self.globals.add(v)
            elif k=='create_country_leader':self.leader=unquote(first(v,'name'));self.portrait=unquote(first(v,'picture',''));self.creations+=1
            elif k=='set_country_leader_portrait':self.portrait=unquote(first(v,'portrait'))
            elif k in ('retire_country_leader','kill_country_leader'):self.leader='';self.retirements+=1
            elif k in ('update_set_politics','set_correct_ideology_trait','force_update_dynamic_modifier','log'):pass
            elif k in ('COLDWAR_USA_legacy_reconcile_party_programmes','COLDWAR_SOV_clear_heirs','MDCW_HP_SOV_clear_manual_retirement_pending','COLDWAR_SOV_succession'):
                self.callbacks+=1  # Native boundary, not a reimplementation of those owners.
            elif k in ('name','trigger','ai_chance'):pass
            else:raise AssertionError('Uninterpreted effect '+k)
    def effect(self,key):self.run(self.effects[key])


def main():
    manifest=json.loads((HERE/'runtime_files.json').read_text(encoding='utf-8'))
    roster=json.loads((HERE/'runtime_roster.json').read_text(encoding='utf-8'))['people']
    data={r['id']:r for r in roster}; asts={}; hashes={}
    for rel in manifest['files']:
        p=ROOT/rel;raw=p.read_bytes();hashes[rel]=hashlib.sha256(raw).hexdigest()
        if p.suffix in ('.txt','.gfx'):
            assert not raw.startswith(b'\xef\xbb\xbf'),rel
            assert raw.decode('utf-8').startswith('# IMPERIA COLD WAR'),rel
            asts[rel]=parse(raw.decode('utf-8'))
            assert adapt(rel,raw.decode('utf-8'),data)==raw.decode('utf-8'),'Non-idempotent adapter: '+rel
        elif p.suffix=='.yml':
            assert raw.startswith(b'\xef\xbb\xbf'),rel
            assert raw.decode('utf-8-sig').splitlines()[1].startswith('# IMPERIA COLD WAR'),rel
        elif p.suffix=='.py':compile(raw,str(p),'exec')
    own='common/scripted_effects/COLDWAR_superpower_1970_leaders.txt'
    effects={k:v for k,o,v in asts[own]}
    triggers={k:v for k,o,v in asts['common/scripted_triggers/COLDWAR_superpower_1970_leaders.txt']}
    for target,path in [(effects,'common/scripted_effects/COLDWAR_lukashenko_1970.txt'),(triggers,'common/scripted_triggers/COLDWAR_lukashenko_1970.txt')]:
        target.update({k:v for k,o,v in parse((ROOT/path).read_text(encoding='utf8'))})
    native_triggers=(ROOT/'common/scripted_triggers/01_political_triggers.txt').read_text(encoding='utf-8-sig')
    for slot in {s for p in PEOPLE for s in p['slots']}:
        assert TRIG[slot]+'_are_in_power = {' in native_triggers,slot
    cases=0
    for p in PEOPLE:
        for slot in p['slots']:
            key=P+p['tag']+'_choose_'+str(slot)+'_'+p['key']+'_effect'
            for year in (1970,1999,2005):
                m=Model(effects,triggers,p['tag'],slot,year)
                m.flags={'COLDWAR_SOV_gensec_bre','earned_focus_receipt'}
                if p.get('available_from') and year<int(p['available_from'].split('.')[0]):
                    before=(m.creations,m.retirements,dict(m.variables),set(m.flags));m.effect(key)
                    assert before==(m.creations,m.retirements,m.variables,m.flags) and not m.leader,(key,year)
                    cases+=1;continue
                m.effect(key);assert m.leader==p['name'],(key,year,m.leader)
                before=(m.creations,m.retirements,dict(m.variables),set(m.flags))
                m.effect(key);assert before==(m.creations,m.retirements,m.variables,m.flags),key
                assert 'earned_focus_receipt' in m.flags
                if p['tag']=='SOV':
                    expected={'COLDWAR_SOV_gensec_'+p['profile']} if slot==4 and p.get('profile') else set()
                    assert {f for f in m.flags if f.startswith('COLDWAR_SOV_gensec_')}==expected,key
                if p['tag']=='USA':assert ('USA_1970_nixon_presidency' in m.flags)==(p['key']=='richard_nixon' and slot==1)
                cases+=1
            for field,value in [('party',8),('tag','CUB'),('human',False),('exists',False),('scenario',False),('dynamic',True)]:
                m=Model(effects,triggers,p['tag'],slot);setattr(m,field,value)
                if field=='party':m.variables['ruling_party']=value
                m.effect(key);assert m.creations==m.retirements==0 and not m.leader,(key,field)
                cases+=1
    for tag in ('USA','SOV'):
        slots=sorted({s for p in PEOPLE if p['tag']==tag for s in p['slots']})
        m=Model(effects,triggers,tag,slots[0]);selected={}
        for slot in slots:
            m.party=slot;m.variables['ruling_party']=slot
            p=[p for p in PEOPLE if p['tag']==tag and slot in p['slots'] and (not p.get('available_from') or int(p['available_from'].split('.')[0])<=1970)][-1]
            m.effect(P+tag+'_choose_'+str(slot)+'_'+p['key']+'_effect');selected[slot]=p['name']
        for slot in slots:
            m.party=slot;m.variables['ruling_party']=slot;m.effect(P+tag+'_set_leader')
            assert m.leader==selected[slot],(tag,slot,m.leader,selected[slot]);cases+=1
        m.variables['MDCW_HP_native_retirement']=1
        old=m.leader;m.effect(P+tag+'_set_leader')
        assert m.leader!=old or len([p for p in PEOPLE if p['tag']==tag and m.party in p['slots']])==1
        cases+=1
    # Calendar deaths, including already open event options, cannot depose a human selection.
    events=asts['events/COLDWAR_SOV_1970_events.txt']
    for k,o,event in events:
        if k!='country_event' or not re.fullmatch(r'COLDWAR_SOV\.9[0-7]',first(event,'id','')):continue
        m=Model(effects,triggers,'SOV',4,1999);m.flags={'COLDWAR_SOV_gensec_bre','COLDWAR_SOV_initialized'};m.leader='Leonid Brezhnev'
        assert not m.condition(first(event,'trigger'))
        m.run(first(event,'immediate',[]))
        for key,op,option in event:
            if key=='option':m.run(option)
        assert m.flags=={'COLDWAR_SOV_gensec_bre','COLDWAR_SOV_initialized'} and not m.globals and m.callbacks==0
        cases+=1
    sov_triggers=dict((k,v) for k,o,v in asts['common/scripted_triggers/COLDWAR_SOV_1970_scripted_triggers.txt'])
    for key in ('bre','kos','pod','sus','and','gre','ust','che'):
        m=Model(effects,{**triggers,**sov_triggers},'SOV',4,1999)
        primary=next(p for p in PEOPLE if p['tag']=='SOV' and p.get('profile')==key and not p['standin'])
        m.leader=primary['name'];m.globals.add('COLDWAR_SOV_dead_'+key)
        assert m.condition(sov_triggers['COLDWAR_SOV_alive_'+key]);cases+=1
    # Every actual named 1970 tree appointment resolves to a real, inspected portrait.
    names={n:r for r in roster for n in [r['name'],*r.get('aliases',[])]}
    named=0
    for rel,tree in asts.items():
        if not rel.startswith(('common/national_focus/','common/scripted_effects/')):continue
        for k,o,v in walk(tree):
            if k=='create_country_leader' and unquote(first(v,'name','')) in names:
                row=names[unquote(first(v,'name'))]
                assert unquote(first(v,'picture',''))==row['portrait'],(rel,row['name'])
                named+=1
    sprites=asts['interface/COLDWAR_superpower_1970_leaders.gfx']
    gfx={unquote(first(v,'name')):unquote(first(v,'texturefile')) for k,o,v in walk(sprites) if k=='spriteType'}
    assert len(gfx)==len(roster)==len(PEOPLE)
    for row in roster:
        assert (ROOT/row['portrait']).is_file(),row['id']
        assert Image.open(ROOT/row['icon']).size==(33,30)
        assert gfx['GFX_'+P+row['id']]==row['icon']
        if row['portrait'].startswith('gfx/leaders/COLDWAR_superpower_1970/'):
            assert Image.open(ROOT/row['portrait']).size==(156,210)
    # A second complete build must preserve every installed text file byte-for-byte.
    run=subprocess.run([sys.executable,str(HERE/'build.py')],cwd=ROOT,capture_output=True,text=True)
    assert run.returncode==0,run.stdout+run.stderr
    for rel,digest in hashes.items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest,'Regeneration changed '+rel
    report=dict(project='IMPERIA COLD WAR',result='PASS',people=len(roster),by_country={t:sum(p['tag']==t for p in roster) for t in ('USA','SOV')},
        choices=sum(len(p['slots']) for p in PEOPLE),model_cases=cases,parsed_files=len(asts),named_creation_references=named,
        portrait_methods={method:sum(r['method']==method for r in roster) for method in sorted({r['method'] for r in roster})},
        checks=['Current text parse','Encoding and markers','Execution guards','Undated legacy choices and explicitly dated Lukashenko exception','Repeat selection','Cross-party preference retention','Native retirement cycling','Personal Soviet programme flags','Queued calendar death options','Portrait and sprite closure','Owning adapter and full-build idempotence'],
        native_engine_tested=False,live_multiplayer_tested=False,native_boundary='The model stubs MD politics, traits, dynamic modifier refresh and existing programme reconciliation.',sha256=hashes,
        commands=['python tools/superpower_1970_leaders/catalogue.py','python tools/superpower_1970_leaders/build.py','python tools/superpower_1970_leaders/validate.py'])
    (HERE/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='sha256'},indent=2))


if __name__=='__main__':main()
