# IMPERIA CW — Cold War: cyprus 1970 — validate.
"""Validate generated native references and important Cyprus integration invariants."""
from pathlib import Path
import json
import re
import hashlib

ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
P='COLDWAR_CYP_1970_'
errors=[]
def check(ok,msg):
    if not ok:errors.append(msg)

def parse(text):
    ts=[m[0] for m in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|>=|<=|!=|=|<|>|[^\s{}<>=!#"]+',text) if not m[0].startswith('#')]
    pos=0
    def read(nested=False):
        nonlocal pos
        result=[]
        while pos<len(ts):
            key=ts[pos];pos+=1
            if key=='}':
                assert nested,'unexpected closing brace'
                return result
            if key=='{':result.append(('_list','=',read(True)));continue
            if pos<len(ts) and ts[pos] in ('=','<','>','>=','<=','!='):
                op=ts[pos];pos+=1
                assert op not in ('>=','<=','!='),'unsupported native comparison '+op
                assert pos<len(ts),'missing value'
                value=ts[pos];pos+=1
                if value=='{':value=read(True)
                elif value=='}':raise AssertionError('missing value')
                result.append((key,op,value))
            else:result.append(('_bare','=',key))
        assert not nested,'unclosed block'
        return result
    return read()

def vals(tree,key):return [v for k,op,v in tree if k==key]
def first(tree,key,default=None):return next(iter(vals(tree,key)),default)
def walk(tree):
    for k,op,v in tree:
        yield k,op,v
        if isinstance(v,list):yield from walk(v)

def main():
    manifest=json.loads((HERE/'manifest.json').read_text());asts={}
    integration=json.loads((HERE/'integration.json').read_text())
    for rel in manifest['generated']+integration:
        path=ROOT/rel;check(path.exists(),'Missing '+rel)
        if path.suffix in ('.txt','.gfx'):
            try:asts[rel]=parse(path.read_text(encoding='utf-8-sig'))
            except AssertionError as e:errors.append(rel+': '+str(e))
    locpath=ROOT/'localisation/english/COLDWAR_CYP_1970_l_english.yml';raw=locpath.read_bytes()
    check(raw.startswith(b'\xef\xbb\xbf'),'English localisation lacks BOM')
    pairs=re.findall(r'^ (\S+):0 (".*")\r?$',raw.decode('utf-8-sig'),re.M)
    local={}
    for key,encoded in pairs:
        try:local[key]=json.loads(encoded)
        except ValueError:errors.append('Invalid localisation '+key)
    check(len(local)==len(pairs),'Duplicate English localisation keys')
    check(not any('\\n' in v for v in local.values()),'Double-escaped newline in localisation')
    check(not list((ROOT/'localisation/german').glob('COLDWAR_CYP_1970*')),'Unexpected German localisation')
    focus=first(asts.get('common/national_focus/COLDWAR_CYP_1970_focus.txt',[]),'focus_tree',[])
    ns=vals(focus,'focus');ids={first(n,'id'):n for n in ns}
    check(len(ns)==295 and len(ids)==295,'Expected295 unique focus IDs')
    check(first(focus,'reset_on_civilwar')=='no','Civil war resets progress')
    check(first(focus,'id')==P+'focus','Wrong tree id')
    design=json.loads((ROOT/'docs/cyprus_1970_design/coldwar_cyprus_1970_design.json').read_text(encoding='utf-8'))
    design_by={n['id']:n for n in design['focuses']}
    coords={}
    def xy(fid):
        n=ids[fid];x=float(first(n,'x'));y=float(first(n,'y'));parent=first(n,'relative_position_id')
        if parent:rx,ry=xy(parent);x+=rx;y+=ry
        return x,y
    for fid,n in ids.items():
        position=xy(fid);check(position not in coords,'Duplicate focus position '+str(position));coords[position]=fid
        check(position==(design_by[fid]['x'],design_by[fid]['y']),'Moved design coordinates '+fid)
        check(abs(float(first(n,'cost'))*7-design_by[fid]['days'])<.00001,'Wrong native focus duration '+fid)
        check(fid in local and fid+'_desc' in local,'Missing focus localisation '+fid)
        for group in vals(n,'prerequisite'):
            for parent in vals(group,'focus'):
                check(parent in ids,'Missing prerequisite '+parent)
                if parent in ids:check(xy(parent)[1]<position[1],'Non-descending prerequisite '+fid)
        for group in vals(n,'mutually_exclusive'):
            for other in vals(group,'focus'):
                check(other in ids,'Missing exclusion '+other)
                if other in ids:check(any(fid in vals(g,'focus') for g in vals(ids[other],'mutually_exclusive')),'Non-reciprocal exclusion '+fid)
        if design_by[fid]['party'] is not None:
            av=first(n,'available',[]);txt=str(av)
            for index in design_by[fid]['party_indices']:
                check(('ruling_party', '=', str(index)) in list(walk(av)),'Missing exact party gate '+fid)
        if design_by[fid].get('execution_mode')=='event_milestone':
            reward=first(n,'completion_reward',[])
            check(all(k=='custom_effect_tooltip' for k,op,v in reward),'Milestone owns gameplay payload '+fid)
    sprite_text='\n'.join(p.read_text(encoding='utf-8-sig') for p in (ROOT/'interface').rglob('*.gfx'))
    sprites=set(re.findall(r'name\s*=\s*"([^"]+)"',sprite_text))
    for fid,n in ids.items():check(first(n,'icon') in sprites,'Missing focus sprite '+fid)
    for rel,ast in asts.items():
        if rel.startswith('interface/'):
            for k,op,v in walk(ast):
                if k=='texturefile':check((ROOT/v.strip('"')).exists(),'Missing texture '+v)
    effects=asts.get('common/scripted_effects/COLDWAR_CYP_1970_effects.txt',[])
    defs={k for k,op,v in effects};em={k:v for k,op,v in effects}
    for rel,ast in asts.items():
        for k,op,v in walk(ast):
            if k.startswith(P) and v=='yes':check(k in defs,'Missing scripted effect '+k+' in '+rel)
            if k=='remove_dynamic_modifier':check(isinstance(v,list) and first(v,'modifier') is not None,'Unsafe scalar dynamic removal '+rel)
            if k in ('custom_effect_tooltip','tooltip','name','title','desc') and isinstance(v,str) and v.startswith(P):
                check(v in local or v in defs,'Missing localisation '+v)
    # Every gameplay grant has a persistent guard. Popup execution revalidates
    # the live proposal before any lender money or territory can move.
    grants=[(k,v) for k,v in em.items() if k.startswith(P+'grant_')]
    for key,body in grants:
        check('has_country_flag' in str(body) and P+'applied_' in str(body),'Unguarded grant '+key)
    event_ast=asts.get('events/COLDWAR_CYP_1970_events.txt',[])
    eventids=[]
    for ev in vals(event_ast,'country_event'):
        eventids.append(first(ev,'id'))
        for opt in vals(ev,'option'):
            if first(opt,'name') and 'Accept these terms' in local.get(first(opt,'name'),''):
                check(bool(vals(opt,'if')),'Acceptance relies only on popup availability '+str(first(ev,'id')))
    check(len(eventids)==len(set(eventids)),'Duplicate event IDs')
    decision_ast=asts.get('common/decisions/COLDWAR_CYP_1970_decisions.txt',[])
    foreign=first(decision_ast,P+'foreign_dossier',[])
    for key,op,decision in foreign:
        complete=first(decision,'complete_effect',[])
        guard=first(first(complete,'if',[]),'limit',[])
        check('is_ai' in str(guard) and 'pending_' in str(guard) and 'offer_instance_' in str(guard),'Foreign decision lacks atomic live-state guard '+key)
    for ev in vals(event_ast,'country_event'):
        number=int(first(ev,'id').split('.')[-1])
        if 1000<=number<3000:
            for opt in vals(ev,'option'):
                check(set(k for k,op,v in opt)<= {'name','ai_chance'},'Foreign notice contains binding gameplay '+first(ev,'id'))
    on=asts.get('common/on_actions/COLDWAR_CYP_1970_on_actions.txt',[])
    daily=first(first(on,'on_actions',[]),'on_daily',[])
    check('original_tag' in str(daily) and 'CYP' in str(daily),'Daily tick lacks current-country guard')
    script=(ROOT/'common/scripted_effects/COLDWAR_CYP_1970_effects.txt').read_text()
    check('declare_war_on' not in script,'CYP framework declares a foreign war')
    check('release = NCY' not in script,'Unsafe blanket NCY release')
    decision_script=(ROOT/'common/decisions/COLDWAR_CYP_1970_decisions.txt').read_text()
    check('modify_debt_effect = yes' in decision_script,'Loans do not record debt')
    check('COLDWAR_CYP_1970_seat_policy' in script,'No explicit lobby seat policy')
    hist=(ROOT/'history/countries/CYP - Cyprus.txt').read_text();early=hist.split('2000.1.1 = {')[0]
    check('load_focus_tree = '+P+'focus' in early,'History does not load Cyprus tree')
    check(P+'initialize = yes' in early,'Starting spirits not connected to history')
    for channel in ('land','naval','air'):check('mdcw_1970_empty_'+channel in early,'Deferred OOB changed '+channel)
    fallback=(ROOT/'common/scripted_effects/mdcw_1970_focus_tree_effects.txt').read_text()
    check('AND = { original_tag = CYP IMP_is_1970_scenario = yes }' in fallback,'Generic fallback overwrites Cyprus')
    leader=(ROOT/'common/scripted_effects/00_leader_setup_scripted_effects.txt').read_text()
    check(leader.index(P+'set_leader = yes')<leader.index('kill_country_leader = yes'),'1970 leader interception happens after modern leader kill')
    for name in ('Makarios III','Glafkos Clerides','Vassos Lyssarides','Ezekias Papaioannou','Nikos Sampson','Georgios Grivas','Spyros Kyprianou'):
        check(name in script,'Historical leader omitted '+name)
    from PIL import Image
    portrait_registry=json.loads((HERE/'leader_assets.json').read_text(encoding='utf-8'))
    portrait_variants=0
    for k,op,v in walk(effects):
        if k=='create_country_leader' and isinstance(v,list):
            name=first(v,'name','').strip('"')
            if name not in portrait_registry['portraits']:continue
            path=first(v,'picture','').strip('"');expected=portrait_registry['portraits'][name]
            check(path==expected,'Wrong portrait assigned to '+name)
            check((ROOT/path).exists(),'Missing leader portrait '+path)
            if (ROOT/path).exists():
                with Image.open(ROOT/path) as img:
                    check(img.format=='DDS' and img.size==(156,210),'Wrong leader portrait format '+name)
            portrait_variants+=1
    check(portrait_variants==9,'Missing named leader or succession portrait variant')
    check('COLDWAR_CYP_1970_portraits_v1' in script,'Existing games do not receive the portrait refresh')
    check('COLDWAR_CYP_1970_portraits_v2' in script,'Existing games do not receive the regional photo refresh')
    check(portrait_registry['generic_portrait']=='gfx/leaders/NCY/1970/COLDWAR_NCY_1970_generic.dds','Unnamed administration uses an unrelated face')
    for name,key in (('Makarios III','makarios'),('Glafkos Clerides','clerides')):
        check(portrait_registry['portraits'].get(name)=='gfx/leaders/CYP/1970/COLDWAR_CYP_1970_'+key+'.dds','Unrestored native portrait retained for '+name)
    ideas=first(first(asts.get('common/ideas/COLDWAR_CYP_1970_ideas.txt',[]),'ideas',[]),'country',[])
    for k,op,idea in ideas:
        if isinstance(idea,list):check('GFX_idea_'+first(idea,'picture','') in sprites,'Missing idea icon '+k)
    native_mods='\n'.join(p.read_text(encoding='utf-8-sig') for folder in ('common/ideas','common/dynamic_modifiers','common/modifiers') for p in (ROOT/folder).glob('*.txt') if not p.name.startswith('COLDWAR_CYP'))
    used={k for n in design['focuses'] for k in n['modifiers']}|{k for s in design['starting_spirits'] for k in s['modifiers']}
    for key in used:check(bool(re.search(r'\b'+key+r'\s*=',native_mods)),'Modifier has no existing mod evidence '+key)
    result={'passed':not errors,'errors':errors,'focuses':len(ns),'coordinate_collisions':295-len(coords),'events':len(eventids),
            'decisions':manifest['decisions'],'guarded_grants':len(grants),'native_modifier_keys':len(used),'icon_sources':manifest['icon_sources'],
            'english_localisation_keys':len(local),'native_focus_point_days':7,'named_leader_portrait_variants':portrait_variants,'in_game_test_performed':False,
            'generated_hashes':{r:hashlib.sha256((ROOT/r).read_bytes()).hexdigest() for r in manifest['generated'] if (ROOT/r).exists()}}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='generated_hashes'},indent=2))
    raise SystemExit(1 if errors else 0)

if __name__=='__main__':main()
