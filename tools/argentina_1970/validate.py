# IMPERIA COLD WAR — Argentina installed-source validation.
"""Check the installed programme and immutable approval, separately from engine QA."""
from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,values,walk

def main():
    checks=[]
    def ck(ok,name):
        checks.append(dict(name=name,passed=bool(ok)))
        if not ok:print('FAIL '+name)
    record=json.loads((HERE/'APPROVAL_RECORD.json').read_text())
    ck(hashlib.sha256((HERE/'approved_design.json').read_bytes()).hexdigest()==record['approved_sha256'],'immutable approval hash')
    d=json.loads((HERE/'runtime_design.json').read_text(encoding='utf-8'))
    manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
    parsed={};loc={};owned=[]
    for rel,h in manifest['files'].items():
        raw=(ROOT/rel).read_bytes();ck(hashlib.sha256(raw).hexdigest()==h,'installed manifest '+rel)
        text=raw.decode('utf-8-sig');custom='COLDWAR_ARG' in Path(rel).name
        if rel.endswith('.txt'):
            ck(not raw.startswith(b'\xef\xbb\xbf'),'script has no BOM '+rel)
            parsed[rel]=parse(text)
        if rel.endswith('.yml'):
            ck(raw.startswith(b'\xef\xbb\xbf'),'localisation has BOM '+rel)
            ck(text.startswith('l_english:\n# IMPERIA COLD WAR'),'localisation marker '+rel)
            for k,v in re.findall(r'^\s+([\w.\-]+):\d+\s+"(.*)"\s*$',text,re.M):
                ck(k not in loc,'unique localisation '+k);loc[k]=v
            ck(not re.search('[\u2013\u2014]', '\n'.join(loc.values())),'English prose punctuation '+rel)
        else:ck(text.startswith('# IMPERIA COLD WAR'),'file marker '+rel)
        if custom:owned.append(rel)
    tree=first(parsed['common/national_focus/COLDWAR_ARG_1970_focus.txt'],'focus_tree')
    focuses={first(n,'id'):n for n in values(tree,'focus')};byid={n['id']:n for n in d['nodes']}
    ck(set(focuses)==set(byid) and len(focuses)==299,'299 approved focus IDs')
    ck(len(values(tree,'shortcut'))==8,'native shortcut grid maximum eight')
    resolved={}
    def pos(fid,stack=()):
        if fid in resolved:return resolved[fid]
        assert fid not in stack,('cyclic anchor',fid)
        f=focuses[fid];p=first(f,'relative_position_id');x=int(first(f,'x'));y=int(first(f,'y'))
        if p:
            a,b=pos(p,stack+(fid,));x+=a;y+=b
        resolved[fid]=(x,y);return x,y
    effects={};triggers={};static=set();dynamic=set();events=set();sprites=set()
    for rel,rows in parsed.items():
        if 'scripted_effects/COLDWAR_ARG' in rel:effects.update({k:v for k,o,v in rows})
        if 'scripted_triggers/COLDWAR_ARG' in rel:triggers.update({k:v for k,o,v in rows})
        if 'dynamic_modifiers/COLDWAR_ARG' in rel:dynamic.update(k for k,o,v in rows)
        if 'ideas/COLDWAR_ARG' in rel:
            static.update(k for k,o,v in first(first(rows,'ideas'),'country'))
        if rel.startswith('events/COLDWAR_ARG'):
            events.update(first(v,'id') for k,o,v in rows if k=='country_event')
    for fid,n in byid.items():
        f=focuses[fid]
        ck(pos(fid)==(n['x'],n['y']),fid+' resolved coordinates')
        ck([values(p,'focus') for p in values(f,'prerequisite')]==n['prerequisites'],fid+' prerequisite grouping')
        ck(values(first(f,'mutually_exclusive',[]),'focus')==n['excludes'],fid+' exclusions')
        ck(first(f,'allow_branch') is None,fid+' party branch remains inspectable')
        reward=first(f,'completion_reward');ck(bool(first(reward,'effect_tooltip')) and bool(first(reward,'hidden_effect')),fid+' independent preview and guarded execution')
        ck(fid in loc and fid+'_desc' in loc,fid+' English localisation')
        ck('COLDWAR_ARG_complete_'+n['key'] in effects and 'COLDWAR_ARG_can_complete_'+n['key'] in triggers,fid+' execution providers')
    ck(len(set(resolved.values()))==299,'no overlapping focus centers')
    ck(len(d['spirits'])==6 and all(s['id'] in static for s in d['spirits']),'six registered starting spirits')
    ck(len(d['agreements'])==20,'twenty bilateral agreements')
    # Custom calls, event IDs, spirits and custom tooltip references must resolve.
    providers=set(effects)|set(triggers)
    for rel in owned:
        if rel not in parsed:continue
        for k,o,v in walk(parsed[rel]):
            if k.startswith('COLDWAR_ARG_') and v in ('yes','no') if isinstance(v,str) else False:
                ck(k in providers,rel+' provider '+k)
            if k in ('custom_effect_tooltip','tooltip','localization_key') and isinstance(v,str) and v.startswith('COLDWAR_ARG'):
                ck(v in loc,rel+' tooltip '+v)
            if k in ('add_ideas','remove_ideas','idea','modifier') and isinstance(v,str) and v.startswith('COLDWAR_ARG'):
                ck(v in static|dynamic,rel+' spirit '+v)
            if k=='id' and isinstance(v,str) and v.startswith(('COLDWAR_ARG.','COLDWAR_ARG_TREATY.','COLDWAR_ARG_politics.')):
                ck(v in events,rel+' event '+v)
    for path in (ROOT/'interface').glob('*.gfx'):
        text=path.read_text(encoding='utf-8-sig',errors='replace')
        sprites.update(re.findall(r'\bname\s*=\s*"?([\w.]+)',text))
    for f in focuses.values():ck(first(f,'icon') in sprites,'focus sprite '+first(f,'id'))
    ideology_rows=parse((ROOT/'common/ideologies/00_ideologies.txt').read_text(encoding='utf-8-sig'))
    ideologies=set()
    for k,o,v in first(ideology_rows,'ideologies'):
        ideologies.update(t for t,op,body in first(v,'types',[]))
    for rel,rows in parsed.items():
        if not rel.startswith('events/COLDWAR_ARG'):continue
        namespaces=set(values(rows,'add_namespace'))
        for k,o,v in rows:
            if k!='country_event':continue
            ck(first(v,'id').rsplit('.',1)[0] in namespaces,first(v,'id')+' registered namespace')
            for key in ('title','desc'):
                val=first(v,key);ck(val in loc,first(v,'id')+' '+key)
            ck(first(v,'picture') in sprites,first(v,'id')+' photo sprite')
            for opt in values(v,'option'):ck(first(opt,'name') in loc,first(v,'id')+' option localisation')
    for rel,rows in parsed.items():
        if 'scripted_effects/COLDWAR_ARG' not in rel:continue
        for k,o,v in walk(rows):
            if k=='create_country_leader':
                ck(first(v,'ideology') in ideologies,rel+' registered leader ideology '+first(v,'ideology'))
                pic=first(v,'picture')
                if pic:ck((ROOT/pic.strip('"')).is_file(),rel+' portrait '+pic)
    goal=effects['COLDWAR_ARG_complete_rosario_plan']
    goals=[v for k,o,v in walk(goal) if k=='create_wargoal']
    ck(len(goals)==1 and first(goals[0],'type')=='take_state_focus' and first(goals[0],'target')=='ENG' and first(goals[0],'expire')=='730' and first(first(goals[0],'generator'),'_bare')=='26','Rosario real native Falklands war goal')
    result=dict(project='IMPERIA COLD WAR',passed=all(c['passed'] for c in checks),checks=len(checks),failed=[c['name'] for c in checks if not c['passed']],focuses=299,agreements=20,events=len(events),source_only=True,boundary='Source, reference and geometry checks. Engine behavior and UI require native testing.')
    (HERE/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False));return not result['passed']
if __name__=='__main__':raise SystemExit(main())
