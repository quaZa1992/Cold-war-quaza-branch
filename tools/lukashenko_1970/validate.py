# IMPERIA COLD WAR — Lukashenko year boundary, wardrobe and native route validation.
"""Execute current scripts in a bounded model. Does not launch the game."""
from pathlib import Path
import json,sys,hashlib,re
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from multiplayer_quality.audit import parse
from superpower_1970_leaders.validate import Model,first,walk
from lukashenko_1970.build import P,NAME,CONFIG,YOUNG,NINETIES,main as build
from lukashenko_1970.integration import adapt

def snapshot(m):return m.leader,m.portrait,m.creations,m.retirements,dict(m.variables),set(m.flags),m.callbacks

def main():
    effects={};triggers={};decisions={};categories={};cases=0
    files=json.loads((HERE/'runtime_files.json').read_text(encoding='utf8'))['files']
    files+=['common/scripted_effects/COLDWAR_superpower_1970_leaders.txt','common/scripted_triggers/COLDWAR_superpower_1970_leaders.txt','common/decisions/COLDWAR_superpower_1970_leaders.txt','common/decisions/categories/COLDWAR_superpower_1970_leaders.txt']
    hashes={};trees={}
    for relative in files:
        path=ROOT/relative;raw=path.read_bytes();hashes[relative]=hashlib.sha256(raw).hexdigest()
        if path.suffix in ('.txt','.gfx'):
            assert not raw.startswith(b'\xef\xbb\xbf'),relative
            assert raw.decode('utf8').startswith('# IMPERIA COLD WAR — '),relative
            trees[relative]=parse(raw.decode('utf8'))
            assert adapt(relative,raw.decode('utf8'))==raw.decode('utf8'),relative
        if path.suffix=='.yml':assert raw.startswith(b'\xef\xbb\xbf') and raw.decode('utf-8-sig').splitlines()[1].startswith('# IMPERIA COLD WAR — ')
        if path.suffix=='.py':compile(raw,str(path),'exec')
    for relative,tree in trees.items():
        if relative.startswith('common/scripted_effects/'):effects.update({k:v for k,o,v in tree if k.startswith((P,'COLDWAR_SP_1970_')) or k=='MDCW_HP_native_pool_BLR_6'})
        if relative.startswith('common/scripted_triggers/'):triggers.update({k:v for k,o,v in tree})
        if relative.startswith('common/decisions/categories/'):categories.update({k:v for k,o,v in tree})
        elif relative.startswith('common/decisions/'):
            for cat,op,items in tree:
                for key,op,value in items:
                    assert key not in decisions,('Duplicate decision',key)
                    decisions[key]=(cat,value)
    boundary=int(CONFIG['available_from'].split('.')[0]);years=sorted({1970,boundary-1,boundary,1990,1999,2005})
    for tag in ('BLR','SOV'):
        for slot in (4,6):
            choose=(P+'BLR_choose_'+str(slot)+'_lukashenko') if tag=='BLR' else 'COLDWAR_SP_1970_SOV_choose_'+str(slot)+'_alexander_lukashenko_effect'
            decision=choose if tag=='BLR' else choose.removesuffix('_effect')
            cat,definition=decisions[decision]
            for year in years:
                m=Model(effects,triggers,tag,slot,year);m.leader='Pyotr Masherov' if tag=='BLR' else 'Leonid Brezhnev';m.flags={'earned_focus_receipt'}
                assert m.condition(first(categories[cat],'visible')) and m.condition(first(definition,'visible')),(tag,slot,year,'Hidden before year')
                assert m.condition(first(definition,'available'))==(year>=boundary),(tag,slot,year)
                before=snapshot(m);m.effect(choose)
                if year<boundary:assert snapshot(m)==before,(tag,slot,year,'Early execution');cases+=1;continue
                assert m.leader==NAME and m.portrait=='GFX_'+P+'young_portrait'
                after=snapshot(m);m.effect(choose);assert after==snapshot(m),'Repeat selection recreates leader'
                creations=m.creations;retirements=m.retirements;variables=dict(m.variables)
                m.effect(P+'set_portrait_90s')
                if year<int(CONFIG['portrait_90s_from'].split('.')[0]):assert P+'portrait_90s' not in m.flags
                else:
                    assert m.portrait=='GFX_'+P+'90s_portrait' and P+'portrait_90s' in m.flags
                    again=snapshot(m);m.effect(P+'set_portrait_90s');assert again==snapshot(m),'Repeated appearance mutates government'
                assert m.leader==NAME and (m.creations,m.retirements)==(creations,retirements) and m.variables==variables
                m.effect(P+'set_portrait_young');assert m.portrait=='GFX_'+P+'young_portrait' and P+'portrait_90s' not in m.flags
                assert 'earned_focus_receipt' in m.flags
                cases+=5
            for field,value in [('party',8),('tag','CUB'),('human',False),('exists',False),('scenario',False),('dynamic',True)]:
                m=Model(effects,triggers,tag,slot,max(boundary,1990));m.leader='Existing incumbent';setattr(m,field,value)
                if field=='party':m.variables['ruling_party']=value
                before=snapshot(m);m.effect(choose);assert snapshot(m)==before,(tag,slot,field);cases+=1
            # Remember a changed portrait through an actual other leader and party return.
            m=Model(effects,triggers,tag,slot,max(boundary,1990));m.effect(choose);m.effect(P+'set_portrait_90s')
            if tag=='BLR':
                other_slot=6 if slot==4 else 4;m.party=other_slot;m.variables['ruling_party']=other_slot
                m.effect(P+'BLR_choose_'+str(other_slot)+'_masherov')
                m.party=slot;m.variables['ruling_party']=slot;m.effect(P+'BLR_set_leader')
            else:
                m.party=13;m.variables['ruling_party']=13;m.effect('COLDWAR_SP_1970_SOV_set_leader')
                m.party=slot;m.variables['ruling_party']=slot;m.effect('COLDWAR_SP_1970_SOV_set_leader')
            assert m.leader==NAME and m.portrait=='GFX_'+P+'90s_portrait',(tag,slot,'Lost wardrobe on party return');cases+=1
            for key in ('young','90s'):
                wardrobe=P+tag+'_'+str(slot)+'_portrait_'+key
                assert wardrobe in decisions
                m=Model(effects,triggers,tag,slot,max(boundary,1990));m.leader='Other leader';before=snapshot(m);m.effect(P+'set_portrait_'+key)
                assert snapshot(m)==before,'Wardrobe changes another leader';cases+=1
    # Both AI and old human saves cannot bypass the early Belarusian pool gate.
    for human in (True,False):
        m=Model(effects,triggers,'BLR',6,boundary-1);m.human=human;m.leader=NAME;m.effect('MDCW_HP_native_pool_BLR_6')
        assert m.leader=='Pyotr Masherov';cases+=1
    for effect in ('apply_portrait','set_portrait_young','set_portrait_90s'):
        assert not any(k in ('create_country_leader','retire_country_leader','kill_country_leader','set_politics','add_country_leader_trait','remove_country_leader_trait') for k,o,v in walk(effects[P+effect])),effect
    pulse=(ROOT/'common/on_actions/COLDWAR_lukashenko_1970.txt').read_text(encoding='utf8')
    assert pulse.count('on_monthly_BLR')==1 and not re.search(r'on_(daily|weekly)|every_country|every_possible_country',pulse)
    own_sprites={first(v,'name').strip('"'):first(v,'texturefile').strip('"') for k,o,v in walk(trees['interface/COLDWAR_lukashenko_1970.gfx']) if k=='spriteType'}
    assert len(own_sprites)==5
    for key,path in own_sprites.items():assert Image.open(ROOT/path).size==((156,210) if key.endswith('_portrait') else (33,30)),key
    for path in HERE.glob('*.py'):compile(path.read_bytes(),str(path),'exec')
    build()
    changed=[f for f,h in hashes.items() if hashlib.sha256((ROOT/f).read_bytes()).hexdigest()!=h];assert not changed,('Regeneration changed files',changed)
    report=dict(project='IMPERIA COLD WAR',result='PASS',model_cases=cases,available_from=CONFIG['available_from'],countries=['BLR','SOV'],slots=[4,6],portrait_variants=2,year_locked_choice_visible=True,monthly_hooks_added=1,new_weekly_or_daily_pulses=False,portrait_changes_recreate_leader=False,engine_tested=False,multiplayer_tested=False,sha256=hashes)
    (HERE/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:v for k,v in report.items() if k!='sha256'},indent=2))

if __name__=='__main__':main()
