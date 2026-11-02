# IMPERIA COLD WAR — Independent validation of emitted Chile 1970 runtime content.
"""Read emitted scripts, not compiler functions. No gameplay files are written."""
from pathlib import Path
from collections import Counter
import argparse, hashlib, json, re, sys
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
sys.path.insert(0,str(HERE))
from script_ast import parse,first,walk,values
from current_design import load_design
P='COLDWAR_CHL_'

def validate(base):
    d=load_design()
    errors=[];counts={};check=lambda ok,msg:errors.append(msg) if not ok else None
    manifest=json.loads((ROOT/'docs/CHILE_COLDWAR_CONCEPT_1970_1990/IMPLEMENTATION_MANIFEST.json').read_text(encoding='utf-8'))
    check(hashlib.sha256((HERE/'approved_design.json').read_bytes()).hexdigest()==manifest['approved_sha256'],'Approval snapshot changed')
    integration_count=0
    for record in manifest['outputs']:
        path=base/record['path']
        check(path.is_file(),'Missing manifested file '+record['path'])
        if not path.is_file():continue
        raw=path.read_bytes()
        check(hashlib.sha256(raw).hexdigest()==record['sha256'],'Manifest hash drift '+record['path'])
        if 'COLDWAR_CHL' not in record['path']:
            integration_count+=1
            check(not raw.startswith(b'\xef\xbb\xbf'),'Integration script BOM '+record['path'])
            check(raw.decode('utf-8').startswith('# IMPERIA COLD WAR —'),'Integration marker '+record['path'])
            try:parse(raw.decode('utf-8'))
            except Exception as ex:errors.append('Integration parse '+record['path']+': '+str(ex))
    paths=[base/r['path'] for r in manifest['outputs'] if r['path'].startswith(('common/','events/','localisation/','interface/')) and 'COLDWAR_CHL' in r['path']]
    trees={};texts={};loc={}
    for path in paths:
        check(path.exists(),'Missing output '+str(path))
        if not path.exists():continue
        raw=path.read_bytes();text=raw.decode('utf-8-sig');rel=path.relative_to(base).as_posix();texts[rel]=text
        if path.suffix=='.yml':
            check(raw.startswith(b'\xef\xbb\xbf'),'Localisation lacks BOM: '+rel)
            check(text.startswith('l_english:\n# IMPERIA COLD WAR —'),'Localisation marker: '+rel)
            for key,value in re.findall(r'^\s+([^ :]+):\d*\s*"((?:\\.|[^"\\])*)"',text,re.M):
                check(key not in loc,'Duplicate localisation '+key);loc[key]=value
                check(not any(c in value for c in '\u2013\u2014'),'Player text dash: '+key)
        else:
            check(not raw.startswith(b'\xef\xbb\xbf'),'Script BOM: '+rel)
            check(text.startswith('# IMPERIA COLD WAR —'),'Script marker: '+rel)
            check(not re.search(r'\b_(?:bare|list)\s*=',text),'Parser sentinel in '+rel)
            try:trees[rel]=parse(text)
            except Exception as ex:errors.append('Parse '+rel+': '+str(ex))
    for category in ('scripted_effects','scripted_triggers','dynamic_modifiers'):
        declarations=Counter(k for rel,t in trees.items() if '/'+category+'/' in rel for k,op,v in t)
        for key,count in declarations.items():check(count==1,'Duplicate '+category+' declaration '+key)
    def branch_chains(rows,rel):
        previous=None
        for k,op,v in rows:
            if k in ('else_if','else'):check(previous in ('if','else_if'),'Orphan '+k+' in '+rel)
            if isinstance(v,list):branch_chains(v,rel)
            previous=k
    for rel,t in trees.items():branch_chains(t,rel)
    effects={k:v for rel,t in trees.items() if '/scripted_effects/' in rel for k,op,v in t}
    triggers={k:v for rel,t in trees.items() if '/scripted_triggers/' in rel for k,op,v in t}
    dyn={k:v for rel,t in trees.items() if '/dynamic_modifiers/' in rel for k,op,v in t}
    idea_ids={k:v for rel,t in trees.items() if '/ideas/' in rel for root,op,cats in t if isinstance(cats,list) for cat,op,items in cats if isinstance(items,list) for k,op,v in items}
    event_ids={first(v,'id'):v for rel,t in trees.items() if rel.startswith('events/') for k,op,v in t if k in ('country_event','news_event')}
    sprite_names=set()
    for folder in (ROOT/'interface',Path('C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV/interface')):
        for source in folder.rglob('*.gfx'):
            sprite_names.update(re.findall(r'\bname\s*=\s*"([^"]+)"',source.read_text(encoding='utf-8-sig')))
    for rel,t in trees.items():
        for k,op,v in walk(t):
            if not isinstance(v,str):continue
            sprite=None
            if k=='picture' and '/ideas/' in rel:sprite='GFX_idea_'+v
            elif k=='picture' and rel.startswith('events/'):sprite=v
            elif k=='icon' and '/decisions/categories/' in rel:sprite='GFX_decision_category_'+v
            elif k=='icon' and '/decisions/' in rel:sprite='GFX_decision_'+v
            elif k=='icon' and v.startswith('GFX_'):sprite=v
            if sprite:check(sprite in sprite_names,'Unregistered sprite '+sprite+' in '+rel)
    supplied_flags=set()
    for t in trees.values():
        for k,op,v in walk(t):
            if k in ('set_country_flag','set_global_flag'):
                flag=first(v,'flag') if isinstance(v,list) else v
                if flag:supplied_flags.add(flag)
    for rel,t in trees.items():
        for k,op,v in walk(t):
            if k in ('has_country_flag','has_global_flag') and isinstance(v,str) and v.startswith(P):
                check(v in supplied_flags,'Missing flag provider '+v+' in '+rel)
    # Confirm the actual effect/trigger vocabulary against installed engine docs
    # and current MD scripted providers. Argument blocks are not effects.
    docs=Path('C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV/documentation')
    if docs.is_dir():
        vocabulary={}
        for kind,folder in [('effects','scripted_effects'),('triggers','scripted_triggers')]:
            native=set(re.findall(r'^## (\w+)\s*$',(docs/(kind+'_documentation.md')).read_text(encoding='utf-8-sig'),re.M))
            for source in (ROOT/'common'/folder).glob('*.txt'):
                native.update(re.findall(r'^(\w+)\s*=\s*\{',source.read_text(encoding='utf-8-sig'),re.M))
            native.update(effects if kind=='effects' else triggers)
            vocabulary[kind]=native
        def api_rows(rows,kind,where):
            for k,op,v in rows:
                if k in ('limit','trigger','enable'):
                    if isinstance(v,list):api_rows(v,'triggers',where)
                elif k in ('if','else_if','else','hidden_effect','effect_tooltip','every_country','every_other_country','every_state'):
                    if isinstance(v,list):api_rows(v,kind,where)
                elif k in ('AND','OR','NOT','hidden_trigger','custom_trigger_tooltip','custom_override_tooltip'):
                    if isinstance(v,list):api_rows([row for row in v if row[0] not in ('tooltip','not_tooltip')],'triggers',where)
                elif re.fullmatch(r'[A-Z]{3}|\d+|(?:ROOT|FROM|PREV|THIS)(?:\.(?:ROOT|FROM|PREV|THIS))*',k):
                    if isinstance(v,list):api_rows(v,kind,where)
                else:check(k in vocabulary[kind],'Unregistered '+kind+' API '+k+' in '+where)
        for rel,t in trees.items():
            if '/scripted_effects/' in rel or '/scripted_triggers/' in rel:
                kind='effects' if '/scripted_effects/' in rel else 'triggers'
                for k,op,v in t:
                    if isinstance(v,list):api_rows(v,kind,k)
    for rel,t in trees.items():
        for k,op,v in walk(t):
            if k.startswith(P) and v=='yes':check(k in effects or k in triggers,'Unknown Chile call '+k+' in '+rel)
            if k=='country_event' and isinstance(v,list):
                event=first(v,'id')
                if event and event.startswith('COLDWAR_CHL'):check(event in event_ids,'Unknown event '+event+' in '+rel)
            if k in ('add_ideas','remove_ideas','has_idea') and isinstance(v,str) and v.startswith(P):check(v in idea_ids,'Unknown idea '+v+' in '+rel)
            if k=='add_timed_idea' and isinstance(v,list):
                key=first(v,'idea');check(key in idea_ids,'Unknown timed idea '+str(key)+' in '+rel)
            if k in ('add_dynamic_modifier','remove_dynamic_modifier'):
                check(isinstance(v,list),'Scalar dynamic modifier '+rel)
                if isinstance(v,list):check(first(v,'modifier') in dyn,'Unknown dynamic modifier '+str(first(v,'modifier')))
            if k in ('tooltip','localization_key','unlock_decision_tooltip') and isinstance(v,str) and v.startswith(P):check(v in loc,'Unknown localisation '+v+' in '+rel)
            if k=='custom_effect_tooltip' and isinstance(v,str) and v.startswith(P):check(v in loc,'Unknown tooltip '+v+' in '+rel)
            if k=='set_politics' and isinstance(v,list):check(first(v,'ruling_party') in ('THIS','ROOT','democratic','communism','fascism','neutrality','nationalist'),'Invalid native set_politics '+str(v))
            if k=='option' and isinstance(v,list):check(first(v,'effect') is None,'Invalid effect wrapper in country-event option '+rel)
    # Reconstruct the full focus graph directly from emitted offsets.
    focus_rel='common/national_focus/COLDWAR_CHL_1970_focus.txt'
    froot=next((v for k,op,v in trees.get(focus_rel,[]) if k=='focus_tree'),[])
    foci={first(v,'id'):v for k,op,v in froot if k=='focus'}
    check(len(foci)==184,'Expected184 focuses, got '+str(len(foci)))
    expected={n['id']:n for n in d['nodes']};positions={}
    refresh=effects.get(P+'refresh_programmes',[])
    for k,op,v in walk(refresh):
        check(k not in ('modify_treasury_effect','add_building_construction','add_tech_bonus'),'One-time reward in programme refresh: '+k)
    def resolve(key,seen=frozenset()):
        if key in positions:return positions[key]
        if key in seen or key not in foci:raise ValueError('Missing/cyclic anchor '+key)
        f=foci[key];x,y=int(first(f,'x')),int(first(f,'y'));anchor=first(f,'relative_position_id')
        if anchor:
            ax,ay=resolve(anchor,seen|{key});x+=ax;y+=ay
        positions[key]=(x,y);return x,y
    for key,n in expected.items():
        check(key in foci,'Missing focus '+key)
        if key not in foci:continue
        f=foci[key]
        check(resolve(key)==(n['x'],n['y']),'Wrong coordinate '+key)
        check([[v for k,op,v in ps if k=='focus'] for ps in values(f,'prerequisite')]==n['prerequisites'],'Changed AND/OR groups '+key)
        check([v for ps in values(f,'mutually_exclusive') for k,op,v in ps if k=='focus']==n['excludes'],'Changed exclusions '+key)
        check(float(first(f,'cost'))==n['cost'],'Changed duration '+key)
        check(first(f,'allow_branch') is None,'Hidden party branch '+key)
        check(first(f,'cancel_if_invalid')=='yes','Missing focus cancellation '+key)
        completion=first(f,'completion_reward',[])
        check(first(completion,'effect_tooltip') is not None and first(completion,'hidden_effect') is not None,'Missing separated preview/execution '+key)
        apply=effects.get(P+'apply_'+n['key'],[]);preview=effects.get(P+'preview_focus_'+n['key'],[])
        check(bool(apply) and bool(preview),'Missing focus provider '+key)
        check(any(k=='has_country_flag' and v==key+'_applied' for k,op,v in walk(triggers.get(P+'can_complete_'+n['key'],[]))),'Missing receipt guard '+key)
        check(any(k=='set_country_flag' and v==key+'_applied' for k,op,v in walk(apply)),'Missing execution receipt '+key)
        if n['party_trigger']:check(any(k==n['party_trigger'] and v=='yes' for k,op,v in walk(triggers.get(P+'can_complete_'+n['key'],[]))),'Missing party guard '+key)
        if n.get('leader'):check(any(k=='has_country_leader' for k,op,v in walk(triggers.get(P+'can_complete_'+n['key'],[]))),'Missing leader guard '+key)
        earned=[v for k,op,v in walk(refresh) if k=='if' and isinstance(v,list) and any(ck=='has_country_flag' and cv==key+'_applied' for ck,co,cv in first(v,'limit',[]))]
        if n['modifiers'] or n['weekly']:
            check(bool(earned),'Missing retained programme rewards '+key)
            for mod,amount in n['modifiers'].items():
                changes=[float(cv) for branch in earned for ck,co,cv in walk(branch) if ck.endswith('_'+mod) and isinstance(cv,str)]
                check(changes==[amount],'Wrong programme modifier '+key+' / '+mod+': '+str(changes))
            if n['weekly']:
                changes=[float(first(v,P+'domestic_weekly')) for branch in earned for k,op,v in walk(branch) if k=='add_to_variable' and first(v,P+'domestic_weekly') is not None]
                check(changes==[n['weekly']],'Wrong active weekly expense '+key)
        for source,label in [(apply,'execution'),(preview,'preview')]:
            fees=[float(v) for k,op,v in walk(source) if k=='treasury_change' and isinstance(v,str)]
            check(fees==([-n['money']] if n['money'] else []),'Wrong '+label+' focus fee '+key+': '+str(fees))
            for b in n['buildings']:
                check(any(k==str(b['state']) and any(ck=='add_building_construction' and first(cv,'type')==b['type'] and first(cv,'level')==str(b['levels']) for ck,co,cv in walk(v)) for k,op,v in walk(source) if isinstance(v,list)),'Wrong '+label+' building '+key)
            for r in n['research']:check(any(k=='add_tech_bonus' and first(v,'category')==r['category'] and float(first(v,'bonus'))==r['bonus'] for k,op,v in walk(source) if isinstance(v,list)),'Missing '+label+' research '+key)
    cards=[]
    for key,(x,y) in positions.items():
        for ok,ox,oy in cards:check(not(abs(x-ox)*96<165 and abs(y-oy)*130<128),'Focus overlap '+key+' / '+ok)
        cards.append((key,x,y))
    # Every building in previews and actual effects receives same-state slots first.
    def slot_walk(rows,state=None):
        for i,(k,op,v) in enumerate(rows):
            if k=='add_building_construction':
                prev=rows[i-1] if i else None
                check(prev is not None and prev[0]=='add_extra_state_shared_building_slots' and int(prev[2])>=int(first(v,'level','1')),'Unpaired slot/building in state '+str(state))
                check(state is not None,'Unscoped building grant')
            if isinstance(v,list):slot_walk(v,k if k.isdigit() else state)
    for rel,t in trees.items():slot_walk(t)
    # Compare every starting liability and treaty spirit against the immutable approval.
    for spirit in d['spirits']+d['conditional_spirits']:
        definition=idea_ids.get(spirit['id'],[])
        actual={k:float(v) for k,op,v in first(definition,'modifier',[])}
        check(actual==spirit['modifiers'],'Changed spirit modifiers '+spirit['id'])
        check(loc.get(spirit['id'])==spirit['name'],'Changed spirit name '+spirit['id'])
    for agreement in d['agreements']:
        key=agreement['id'].removeprefix(P)
        sides=[('CHL',agreement['chile'])]+[(tag,agreement['recipient']) for tag in agreement.get('partners',[agreement['partner']])]
        for tag,side in sides:
            idea=P+'dip_'+key+'_'+tag.lower()
            actual={k:float(v) for k,op,v in first(idea_ids.get(idea,[]),'modifier',[])}
            check(actual==side['modifiers'],'Changed agreement spirit '+idea)
    # All country leader subideologies and portrait paths must resolve.
    ideologies=set()
    for path in (ROOT/'common/ideologies').glob('*.txt'):
        for k,op,v in walk(parse(path.read_text(encoding='utf-8-sig'))):
            if k=='types' and isinstance(v,list):ideologies.update(ik for ik,io,iv in v)
    for rel,t in trees.items():
        for k,op,v in walk(t):
            if k=='create_country_leader':
                check(first(v,'ideology') in ideologies,'Unknown leader subideology '+str(first(v,'ideology'))+' in '+rel)
                pic=first(v,'picture')
                if pic and ('/' in pic or '\\' in pic):check((ROOT/pic.strip('"')).is_file() or (Path('C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV')/pic.strip('"')).is_file(),'Missing leader picture '+pic)
    for rel,text in texts.items():
        if not rel.endswith('.yml'):
            check(not re.search(r'\btreasury\s*(?:>|>=)',text),'Cash affordability gate in '+rel)
            check(not re.search(r'workforce\w*\s*=\s*-',text),'Negative workforce in '+rel)
            check(not re.search(r'\b(?:treasury_change|[\w]*weekly\w*)\s*=\s*-?\d+\.\d{6}',text),'Overprecise money literal in '+rel)
    counts.update(files=len(paths),integration_files=integration_count,focuses=len(foci),prerequisite_links=sum(len(ps) for n in d['nodes'] for ps in n['prerequisites']),exclusion_pairs=sum(len(n['excludes']) for n in d['nodes'])//2,scripted_effects=len(effects),scripted_triggers=len(triggers),ideas=len(idea_ids),dynamic_modifiers=len(dyn),events=len(event_ids),localisation=len(loc))
    return {'project':'IMPERIA COLD WAR','counts':counts,'errors':errors,'passed':not errors,'engine_tested':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--installed',action='store_true');args=p.parse_args()
    report=validate(ROOT if args.installed else HERE/'stage')
    out=ROOT/'docs/CHILE_COLDWAR_CONCEPT_1970_1990/RUNTIME_STATIC_QA.json';out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));sys.exit(0 if report['passed'] else 1)
