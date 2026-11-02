# IMPERIA COLD WAR — German leadership candidate and portrait integration checks.
"""Bounded script-model and asset closure checks. This does not launch HOI4."""
from pathlib import Path
import sys,json,re,hashlib
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from multiplayer_quality.audit import parse
from superpower_1970_leaders.validate import Model,first,walk
from europe_1970_leaders.build import P,PROFILES,PEOPLE,ident,preference,rows,render
from europe_1970_leaders.integration import adapt

class GermanModel(Model):
    def condition(self,tree):
        transformed=[('has_country_flag',o,'earned_'+v) if k=='has_completed_focus' else (k,o,v) for k,o,v in tree]
        return super().condition(transformed)
    def run(self,tree,depth=0):
        # Traits are independently checked for earned-focus guards below.
        return super().run([r for r in tree if r[0]!='add_country_leader_trait'],depth)

def main(code_only=False):
    if code_only:
        data=rows();render(data)
        from europe_1970_leaders.build import WRITTEN
        files=list(WRITTEN)
    else:
        files=json.loads((HERE/'runtime_files.json').read_text(encoding='utf8'))['files'];data={r['id']:r for r in json.loads((HERE/'runtime_roster.json').read_text(encoding='utf8'))['people']}
    asts={};hashes={}
    for relative in files:
        path=ROOT/relative;raw=path.read_bytes();hashes[relative]=hashlib.sha256(raw).hexdigest()
        if path.suffix in ('.txt','.gfx'):
            assert not raw.startswith(b'\xef\xbb\xbf'),relative
            assert raw.decode('utf8').startswith('# IMPERIA COLD WAR'),relative
            asts[relative]=parse(raw.decode('utf8'))
            assert adapt(relative,raw.decode('utf8'),data)==raw.decode('utf8'),relative
        if path.suffix=='.yml':
            assert raw.startswith(b'\xef\xbb\xbf'),relative
            assert raw.decode('utf-8-sig').splitlines()[1].startswith('# IMPERIA COLD WAR'),relative
        if path.suffix=='.py':compile(raw,str(path),'exec')
    effects={k:v for k,o,v in asts['common/scripted_effects/COLDWAR_europe_1970_leaders.txt']}
    triggers={k:v for k,o,v in asts['common/scripted_triggers/COLDWAR_europe_1970_leaders.txt']}
    native=parse((ROOT/'common/scripted_effects/COLDWAR_DDR_1970_scripted_effects.txt').read_text(encoding='utf8'))
    effects.update({k:v for k,o,v in native if k in ('COLDWAR_DDR_clear_first_sec','COLDWAR_DDR_clear_heirs')})
    cases=0
    for p in data.values():
        for slot in p['slots']:
            choose=P+p['tag']+'_choose_'+str(slot)+'_'+p['key']+'_effect'
            for year in (1970,1999,2005):
                m=GermanModel(effects,triggers,p['tag'],slot,year);m.flags={'COLDWAR_DDR_first_sec_ulb','earned_focus_receipt'}
                m.effect(choose);assert m.leader==p['name'],(choose,m.leader)
                state=m.creations,m.retirements,dict(m.variables),set(m.flags);m.effect(choose)
                assert state==(m.creations,m.retirements,m.variables,m.flags),choose
                assert 'earned_focus_receipt' in m.flags
                if p['tag']=='DDR':
                    expected={'COLDWAR_DDR_first_sec_'+p['profile']} if slot==4 and p.get('profile') else set()
                    assert {f for f in m.flags if f.startswith('COLDWAR_DDR_first_sec_')}==expected,choose
                    assert ('COLDWAR_DDR_kessler_leads' in m.flags)==(slot==4 and p['key']=='heinz_kessler')
                cases+=1
            for field,value in [('party',8),('tag','CUB'),('human',False),('exists',False),('scenario',False),('dynamic',True)]:
                m=GermanModel(effects,triggers,p['tag'],slot);setattr(m,field,value)
                if field=='party':m.variables['ruling_party']=value
                m.effect(choose);assert m.creations==m.retirements==0,(choose,field);cases+=1
            for alias in [p['name'],*p['aliases']]:
                m=GermanModel(effects,triggers,p['tag'],slot);m.leader=alias;m.effect(choose)
                assert m.creations==m.retirements==0,(choose,alias);cases+=1
    for tag in ('GER','DDR'):
        selected={};m=GermanModel(effects,triggers,tag,1)
        for slot in sorted({s for p in data.values() if p['tag']==tag for s in p['slots']}):
            candidates=[p for p in data.values() if p['tag']==tag and slot in p['slots']]
            p=candidates[-1];m.party=slot;m.variables['ruling_party']=slot;m.effect(P+tag+'_choose_'+str(slot)+'_'+p['key']+'_effect');selected[slot]=p['name']
        for slot,name in selected.items():
            m.party=slot;m.variables['ruling_party']=slot;m.effect(P+tag+'_set_leader')
            assert m.leader==name,(tag,slot,m.leader,name);cases+=1
    # Explicit appointments written by existing West German focus/event rewards win.
    for slot,var in ((1,'cwger_cdu_leader'),(2,'cwger_fdp_leader'),(3,'cwger_spd_leader')):
        people=[p for p in data.values() if p['tag']=='GER' and slot in p['slots']]
        for index,p in enumerate(people,1):
            m=GermanModel(effects,triggers,'GER',slot);m.leader=people[0]['name'];m.variables[var]=index
            m.effect(P+'GER_set_leader');assert m.leader==p['name'],(var,index,m.leader);cases+=1
    # Human calendar mortality and previously saved death flags cannot lock candidates.
    alive=parse((ROOT/'common/scripted_triggers/COLDWAR_DDR_1970_scripted_triggers.txt').read_text(encoding='utf8'))
    for k,o,v in alive:
        if k not in ('COLDWAR_DDR_alive_ulb','COLDWAR_DDR_alive_hof','COLDWAR_DDR_alive_lam'):continue
        v=parse(adapt('common/scripted_triggers/COLDWAR_DDR_1970_scripted_triggers.txt',(ROOT/'common/scripted_triggers/COLDWAR_DDR_1970_scripted_triggers.txt').read_text(encoding='utf8'),data))
        body=next(vv for kk,oo,vv in v if kk==k)
        m=GermanModel(effects,triggers,'DDR',4,1999);m.flags={'COLDWAR_DDR_dead_'+k.rsplit('_',1)[-1]};assert m.condition(body)
        m.human=False;assert not m.condition(body);cases+=2
    hooks=(ROOT/'common/on_actions/COLDWAR_europe_1970_leaders.txt').read_text(encoding='utf8')
    assert not re.search(r'on_(daily|weekly)|every_country|every_possible_country',hooks)
    assert hooks.count('on_monthly_')==2
    if not code_only:
        sprites={first(v,'name').strip('"'):first(v,'texturefile').strip('"') for k,o,v in walk(asts['interface/COLDWAR_europe_1970_leaders.gfx']) if k=='spriteType'}
        assert len(sprites)==len(data)
        for p in data.values():
            assert Image.open(ROOT/p['portrait']).size==(156,210),p['id']
            assert Image.open(ROOT/p['icon']).size==(33,30),p['id']
            assert sprites['GFX_'+P+p['id']]==p['icon'],p['id']
        for relative,tree in asts.items():
            for key,op,value in walk(tree):
                if key.startswith(P) and value in ('yes','no'):assert key in effects or key in triggers,(relative,key)
        manifest=json.loads((HERE/'ASSET_MANIFEST.json').read_text(encoding='utf8'))['assets']
        assert len(manifest)==len({a['id'] for a in manifest})==112
        for asset in manifest:
            for binding in asset['bindings']:
                path=ROOT/binding['path'];assert Image.open(path).size==(156,210)
                assert hashlib.sha256(path.read_bytes()).hexdigest()==binding['sha256'],path
        from europe_1970_leaders.art import approved
        assert set(approved())=={'willy_brandt','walter_ulbricht','SOV_leonid_brezhnev'}
        for key,record in approved().items():
            for path in [record['original_binding'],*record.get('compatibility_aliases',[])]:
                assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==record['sha256'],('Approved portrait changed',key,path)
        for path in HERE.glob('*.py'):compile(path.read_bytes(),str(path),'exec')
        # A replay of the canonical build must preserve the same bytes.
        from europe_1970_leaders.build import main as build
        build()
        changed=[f for f,h in hashes.items() if hashlib.sha256((ROOT/f).read_bytes()).hexdigest()!=h]
        assert not changed,('Build is not byte-idempotent',changed)
        for key,record in approved().items():
            for path in [record['original_binding'],*record.get('compatibility_aliases',[])]:
                assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==record['sha256'],('Rebuild replaced approved portrait',key,path)
    report=dict(project='IMPERIA COLD WAR',status='PASS',people=len(data),unique_people=len({p['key'] for p in data.values()}),choices=sum(len(p['slots']) for p in data.values()),bounded_model_cases=cases,calendar_locks=False,monthly_country_hooks=2,engine_tested=False,multiplayer_tested=False,code_only=code_only,files=hashes)
    (HERE/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8');print(json.dumps({k:v for k,v in report.items() if k!='files'}))
if __name__=='__main__':main('--code-only' in sys.argv)
