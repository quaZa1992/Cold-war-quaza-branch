# IMPERIA COLD WAR — Independent validation of emitted Brazil 1970 game scripts.
from pathlib import Path
from collections import Counter
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from focus_prerequisite_ui import nodes,field
P='COLDWAR_BRA_';errors=[];checks=0
def check(ok,label):
    global checks
    checks+=1
    if not ok:errors.append(label)
def walk(ns):
    for n in ns:
        yield n
        if isinstance(n.value,list):yield from walk(n.children())
def value(n,k,default=None):return field(n.children(),k,default)
def expr(ns,k):return [n.value for n in walk(ns) if n.key==k]
def main():
    d=json.loads((HERE/'approved_design.json').read_text(encoding='utf-8'));manifest=json.loads((HERE/'manifest.json').read_text())
    check(hashlib.sha256((HERE/'approved_design.json').read_bytes()).hexdigest()==manifest['approved_sha256'],'Immutable approval changed')
    paths=[ROOT/p for p in manifest['files'] if p.endswith(('.txt','.yml','.gfx'))]
    ast={};texts={};loc={}
    for p in paths:
        rel=p.relative_to(ROOT).as_posix();raw=p.read_bytes();s=raw.decode('utf-8-sig');texts[rel]=s
        check(hashlib.sha256(raw).hexdigest()==manifest['files'][rel]['sha256'],'Manifest drift '+rel)
        if p.suffix=='.yml':
            check(raw.startswith(b'\xef\xbb\xbf'),'Localisation BOM '+rel)
            check(s.startswith('l_english:\n# IMPERIA COLD WAR'),'Localisation marker '+rel)
            if 'COLDWAR_BRA' in rel:
                for key,v in re.findall(r'^\s*([^\s:]+):\d*\s*"((?:\\.|[^"\\])*)"',s,re.M):
                    check(key not in loc,'Duplicate English key '+key);loc[key]=v
                    check(not any(c in v for c in '\u2013\u2014'),'Player text dash '+key)
            continue
        check(not raw.startswith(b'\xef\xbb\xbf'),'Forbidden script BOM '+rel)
        check(s.startswith('# IMPERIA COLD WAR'),'Script marker '+rel)
        try:ast[rel]=nodes(s)
        except Exception as ex:errors.append('Parser '+rel+': '+str(ex))
        check(not re.search(r'\b_(?:bare|list)\s*=',s),'Parser sentinel '+rel)
        if 'COLDWAR_BRA' in rel:check(not re.search(r'(?<![\w.])-?\d+\.\d{6,}',s),'Fixed-point literal precision '+rel)
        def branches(ns):
            previous=None
            for n in ns:
                if n.key in ('else','else_if'):check(previous in ('if','else_if'),'Orphan branch '+rel)
                if isinstance(n.value,list):branches(n.children())
                previous=n.key
        if rel in ast and 'COLDWAR_BRA' in rel:branches(ast[rel])
    fx={n.key:n for rel,t in ast.items() if '/scripted_effects/' in rel and 'COLDWAR_BRA' in rel for n in t}
    tr={n.key:n for rel,t in ast.items() if '/scripted_triggers/' in rel and 'COLDWAR_BRA' in rel for n in t}
    declarations=Counter(n.key for rel,t in ast.items() if '/scripted_effects/' in rel and 'COLDWAR_BRA' in rel for n in t)
    for k,c in declarations.items():check(c==1,'Duplicate effect '+k)
    decision_ids={n.key for rel,t in ast.items() if rel.startswith('common/decisions/') and '/categories/' not in rel and 'COLDWAR_BRA' in rel for root in t for n in root.children()}
    for rel,t in ast.items():
        if 'COLDWAR_BRA' not in rel:continue
        for n in walk(t):
            if n.key=='unlock_decision_tooltip' and isinstance(n.value,str) and n.value.startswith(P):check(n.value in decision_ids,'Unknown decision unlock '+n.value)
    # Party organization previews include both actual support deltas, independently
    # of their hidden registration transaction. Existing effects remain unchanged.
    from politics_presentation import FORMS,CP
    for org,(_,outlook,_,_) in FORMS.items():
        form=fx[CP+'form_'+org];preview=fx[CP+'preview_register_'+org]
        check(expr(form.children(),'party_popularity_increase')==['0.01'],'Formation party support changed '+org)
        check(expr(form.children(),'temp_outlook_increase')==['0.01'],'Formation outlook support changed '+org)
        check(expr(preview.children(),'party_popularity_increase')==['0.01'],'Missing party support preview '+org)
        check(expr(preview.children(),'popularity')==['0.01'],'Missing outlook support preview '+org)
        check(expr(preview.children(),'ideology')==[outlook],'Wrong outlook preview '+org)
        check(not any(n.key in ('set_country_flag','set_variable','create_country_leader') for n in walk(preview.children())),'Preview performs party registration '+org)
    event_ast=ast['events/COLDWAR_BRA_1970_events.txt']
    split=next(n for n in event_ast if n.key=='country_event' and value(n,'id')=='COLDWAR_BRA.7')
    preview_calls=[n.key for n in walk(split.children()) if n.value=='yes']
    for org in ('ptb_late','pdt'):check(CP+'preview_register_'+org in preview_calls,'Party split omitted formation preview '+org)
    # A source use is insufficient: require an engine-documented or registered key.
    game=Path('C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV')
    documented=set(re.findall(r'^## ([a-zA-Z0-9_]+)$',(game/'documentation/modifiers_documentation.md').read_text(encoding='utf-8-sig'),re.M))
    registered={n.key for p in (ROOT/'common/modifier_definitions').glob('*.txt') for n in nodes(p.read_text(encoding='utf-8-sig'))}
    buildings={n.key for p in (ROOT/'common/buildings').glob('*.txt') for root in nodes(p.read_text(encoding='utf-8-sig')) if root.key=='buildings' for n in root.children()}
    documented.update('production_speed_'+name+'_factor' for name in buildings)
    for rel,t in ast.items():
        if '/ideas/' not in rel or 'COLDWAR_BRA' not in rel:continue
        for parent in walk(t):
            if parent.key=='modifier':
                for n in parent.children():check(n.key in documented|registered,'Unsupported idea modifier '+n.key+' in '+rel)
    # All country-specific yes/no calls must resolve in the actual loaded output.
    for rel,t in ast.items():
        if 'COLDWAR_BRA' not in rel:continue
        for n in walk(t):
            if n.key.startswith(P) and n.value in ('yes','no'):
                check(n.key in fx or n.key in tr,'Undefined helper '+n.key+' in '+rel)
    tree=next(n for n in ast['common/national_focus/COLDWAR_BRA_1970_focus.txt'] if n.key=='focus_tree')
    focuses={value(n,'id'):n for n in tree.children() if n.key=='focus'}
    check(len(focuses)==224,'Focus count')
    resolved={}
    def xy(i):
        if i in resolved:return resolved[i]
        n=focuses[i];x=int(value(n,'x'));y=int(value(n,'y'));a=value(n,'relative_position_id')
        if a:ax,ay=xy(a);x+=ax;y+=ay
        resolved[i]=(x,y);return x,y
    for n in d['nodes']:
        f=focuses[n['id']]
        check(xy(n['id'])==(n['x'],n['y']),'Coordinate changed '+n['key'])
        groups=[expr(p.children(),'focus') for p in f.children() if p.key=='prerequisite']
        check(groups==[[P+k for k in ps] for ps in n['prerequisites']],'Prerequisite grouping changed '+n['key'])
        exclusions=expr([v for v in f.children() if v.key=='mutually_exclusive'],'focus')
        check(set(exclusions)=={P+k for k in n['exclusions']},'Exclusions changed '+n['key'])
        check(float(value(f,'cost'))==float(n['cost']),'Duration changed '+n['key'])
        check(not any(v.key=='allow_branch' for v in walk(f.children())),'Party path hidden '+n['key'])
        helper=fx[P+'complete_'+n['key']];render=texts['common/scripted_effects/COLDWAR_BRA_1970_effects.txt'][helper.start:helper.end]
        check(P+'earned_'+n['key'] in render,'Missing once receipt '+n['key'])
        g=next(g for g in d['groups'] if g['id']==n['group'])
        if g['slot'] is not None:check(P+g['id']+'_in_power = yes' in render,'Wrong party reward guard '+n['key'])
        check('effect_tooltip' in expr(f.children(),'completion_reward')[0] if False else any(v.key=='effect_tooltip' for v in walk(f.children())),'Missing native preview '+n['key'])
        for e in n['effects']:
            if e['kind']=='treasury_gdp':
                expected=f'{e["percent"]/100:.5f}'.rstrip('0').rstrip('.')
                check('multiply = '+expected in render,'GDP fee changed '+n['key'])
    check(len([n for n in tree.children() if n.key=='shortcut'])==8,'Native shortcut count')
    model=json.loads((HERE/'runtime_design.json').read_text(encoding='utf-8'))
    canonical=[{k:n.get(k) for k in ('id','group','x','y','anchor','offset','prerequisites','exclusions','conditions','cost','effects','offer')} for n in model['nodes']]
    baseline=json.loads((HERE/'POLISH_BASELINE.json').read_text(encoding='utf-8'))
    check(hashlib.sha256(json.dumps(canonical,sort_keys=True).encode()).hexdigest()==baseline['gameplay_sha256'],'Polish changed approved gameplay')
    # Reconcile has spirit changes only; no finite grants or setup charges.
    for name in ('sync_programmes','sync_agreements'):
        n=fx[P+name];forbidden={'modify_treasury_effect','add_building_construction','add_extra_state_shared_building_slots','add_tech_bonus','army_experience','navy_experience','air_experience'}
        check(not any(k.key in forbidden for k in walk(n.children())),'Reconcile replays finite rewards '+name)
    for n in d['nodes']:
        if not n.get('offer'):continue
        k=n['key'];o=n['offer'];a=fx[P+'accept_initiator_'+k]
        s=texts['common/scripted_effects/COLDWAR_BRA_1970_diplomacy_effects.txt'][a.start:a.end]
        check(P+'can_accept_'+k in s,'Acceptance guard '+k)
        check(P+'signed_'+k in s,'Signed receipt '+k)
        check('days =' not in s,'Treaty expiry '+k)
        send=fx[P+'propose_'+k]
        check(not any(v.key in ('modify_treasury_effect','add_ideas','add_tech_bonus','add_building_construction') for v in walk(send.children())),'Premature agreement award '+k)
        prev=fx[P+'offer_preview_'+k];ps=texts['common/scripted_effects/COLDWAR_BRA_1970_diplomacy_effects.txt'][prev.start:prev.end]
        check(o['brazil']['spirit'] in ps and o['recipient']['spirit'] in ps,'Incomplete prospective spirits '+k)
        for side in ('brazil','recipient'):
            for e in o[side]['effects']:
                if e['kind']=='building':check('add_extra_state_shared_building_slots = '+str(e['amount']) in s,'Missing treaty slot '+k)
        for tag in [o['partner']]:
            pair=tr[P+'pair_'+tag+'_clear'];v=str(pair.value)
            for cls in ('dip','fin','eco','mil'):
                for direction in ('on_us','by_us'):check('imp_'+cls+'_sanc_'+direction in v,'Missing sanction '+tag+cls+direction)
    check('check_variable = { treasury' not in '\n'.join(s for rel,s in texts.items() if 'COLDWAR_BRA' in rel),'Own spending treasury gate')
    # Engine registry evidence, not an engine run, for built-in effects and triggers.
    script_loc=set()
    sprite_names=set()
    for p in (ROOT/'interface').glob('*.gfx'):
        sprite_names.update(re.findall(r'\bname\s*=\s*"([^"\n]+)"',p.read_text(encoding='utf-8-sig',errors='replace')))
    for rel,t in ast.items():
        if 'COLDWAR_BRA' not in rel:continue
        for n in walk(t):
            if n.key=='picture' and isinstance(n.value,str) and ('/ideas/' in rel or rel.startswith('events/')):
                sprite=n.value if rel.startswith('events/') else 'GFX_idea_'+n.value
                check(sprite in sprite_names,'Missing picture '+sprite+' in '+rel)
            if n.key=='icon' and isinstance(n.value,str) and n.value.startswith('COLDWAR_BRA_focus_'):check(n.value in sprite_names,'Missing focus sprite '+n.value)
    for rel,t in ast.items():
        if 'COLDWAR_BRA' not in rel:continue
        for n in walk(t):
            if n.key in ('tooltip','title','desc','name','localization_key') and isinstance(n.value,str) and n.value.startswith(('COLDWAR_BRA_','COLDWAR_BRA.','COLDWAR_BRA_AGREEMENTS.')):
                if n.key=='name' and n.value in sprite_names:continue
                if '/scripted_localisation/' in rel and n.key=='name':continue
                check(n.value in loc,'Missing localised key '+n.value+' in '+rel)
    report=dict(project='IMPERIA COLD WAR',kind='Independent emitted-source checks. Not HOI4 engine verification.',approved_sha256=manifest['approved_sha256'],assertions=checks,focuses=len(focuses),scripted_effects=len(fx),scripted_triggers=len(tr),english_keys=len(loc),errors=errors)
    (HERE/'VALIDATION.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2));return int(bool(errors))
if __name__=='__main__':sys.dont_write_bytecode=True;sys.exit(main())
