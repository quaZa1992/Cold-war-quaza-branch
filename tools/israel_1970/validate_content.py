# IMPERIA CW — Cold War: israel 1970 — validate content.
"""Validate compiled scripts, localisation, assets and scenario integration."""
from pathlib import Path
import hashlib
import json
import re
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
data=json.loads((HERE/'english_design.json').read_text(encoding='utf-8'))
issues=[]
def check(condition,message):
    if not condition:issues.append(message)

def tokens(source):
    return [m[0] for m in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|>=|<=|!=|=|<|>|[^\s{}<>=!#"]+',source) if not m[0].startswith('#')]
def parse(source):
    ts=tokens(source);position=0
    # HOI4 does not accept these compound operators. In particular, size >= 1
    # aborts focus parsing and makes subsequent focus blocks disappear in game.
    assert not any(t in ('>=','<=','!=') for t in ts),'unsupported HOI4 comparison operator (use compare or NOT)'
    def block(nested=False):
        nonlocal position
        values=[]
        while position<len(ts):
            key=ts[position];position+=1
            if key=='}':
                assert nested,'unexpected closing brace'
                return values
            if key=='{':values.append(('_list','=',block(True)));continue
            if position<len(ts) and ts[position] in ('=','>','<','>=','<=','!='):
                op=ts[position];position+=1;assert position<len(ts),'missing value'
                value=ts[position];position+=1
                if value=='{':value=block(True)
                elif value=='}':raise AssertionError('missing value before closing brace')
                values.append((key,op,value))
            else:values.append(('_bare','=',key))
        assert not nested,'unclosed block'
        return values
    return block()
def values(block,key):return [v for k,op,v in block if k==key]
def first(block,key,default=None):return next(iter(values(block,key)),default)
def walk(block):
    for key,op,value in block:
        yield key,op,value
        if isinstance(value,list):yield from walk(value)

asts={}
for rel in manifest['generated']:
    p=ROOT/rel;check(p.exists(),'Missing file: '+rel)
    if p.suffix in ('.txt','.gfx'):
        try:asts[rel]=parse(p.read_text(encoding='utf-8-sig'))
        except AssertionError as e:issues.append(rel+': '+str(e))
locpath=ROOT/'localisation/english/ISR70_l_english.yml'
raw=locpath.read_bytes();check(raw.startswith(b'\xef\xbb\xbf'),'Localisation must use UTF-8 BOM')
check(raw.decode('utf-8-sig').startswith('l_english:\n'),'English header missing')
locpairs=re.findall(r'^ (\S+):0 (".*")$',raw.decode('utf-8-sig'),re.M)
localisation={}
for key,encoded in locpairs:
    try:localisation[key]=json.loads(encoded)
    except json.JSONDecodeError:issues.append('Invalid localisation quoting: '+key)
check(len(localisation)==len(locpairs),'Duplicate localisation keys')
check(not any(re.search(r'\b(?:Fokus|Führung|Regierung|Entscheidungen|Voraussetzung|Wirtschaft|Entwurf|gründen|Zweig|Gesellschaft)\b',v,re.I) for v in localisation.values()),'German content in new localisation')
check(not list((ROOT/'localisation/german').glob('ISR70*')),'German localisation was generated')
tree=first(asts['common/national_focus/ISR70_focus.txt'],'focus_tree')
focuses=values(tree,'focus');focusmap={first(n,'id'):n for n in focuses}
check(len(focuses)==manifest['focuses'] and len(focusmap)==manifest['focuses'],'Focus count or unique IDs incorrect')
check(first(tree,'id')=='ISR70_focus','Wrong tree id')
check(first(tree,'reset_on_civilwar')=='no','Civil war must not reset progress')
coords=[]
resolved={}
def resolve_position(key,visiting=frozenset()):
    if key in resolved:return resolved[key]
    check(key not in visiting,'Cyclic relative position: '+key)
    if key in visiting:return (0,0)
    item=focusmap[key]
    x,y=float(first(item,'x')),float(first(item,'y'))
    anchor=first(item,'relative_position_id')
    if anchor:
        check(anchor in focusmap,'Unknown position anchor: '+str(anchor))
        ax,ay=resolve_position(anchor,visiting|{key});x+=ax;y+=ay
    resolved[key]=(x,y)
    return resolved[key]
metadata={n['id']:n for n in data['nodes']}
for key,n in focusmap.items():
    coords.append(resolve_position(key))
    check(list(coords[-1])==metadata[key]['xy'],'Script coordinates differ from layout: '+key)
    check(key in localisation and key+'_desc' in localisation,'Missing focus localisation: '+key)
    check(first(n,'cancel_if_invalid')=='yes','Party focus cancellation missing: '+key)
    for row in values(n,'prerequisite'):
        for parent in values(row,'focus'):check(parent in focusmap,'Unknown prerequisite: '+str(parent))
    drawn=[values(row,'focus') for row in values(n,'prerequisite')]
    check(drawn==metadata[key]['visual_prerequisites'],'Incorrect visible prerequisites: '+key)
    for row in metadata[key]['availability_prerequisites']:
        expected=[('has_completed_focus','=',parent) for parent in row]
        clause=expected[0] if len(row)==1 else ('OR','=',expected)
        check(clause in first(n,'available',[]),'Lost cross-branch prerequisite: '+key)
    for row in values(n,'mutually_exclusive'):
        for other in values(row,'focus'):check(other in focusmap and any(key in values(r,'focus') for r in values(focusmap.get(other,[]),'mutually_exclusive')),'Asymmetric exclusion: '+key+' / '+str(other))
    if re.match(r'ISR70_p\d+_',key):
        slot=int(re.match(r'ISR70_p(\d+)_',key)[1]);trigger=next(g['trigger'] for g in data['groups'] if g['party']==slot)
        check(any(k==trigger and v=='yes' for k,op,v in walk(values(n,'available')[0])),'Missing exact governing-party check: '+key)
        expected_outlook='democratic' if slot<4 else 'communism' if slot<10 else 'neutrality' if slot<20 else 'nationalist'
        for effect,op,body in walk(first(n,'completion_reward',[])):
            if effect=='set_politics':
                check(first(body,'ruling_party')==expected_outlook,'Election tooltip has no matching ideology group: '+key)
check(len(set(coords))==manifest['focuses'],'Focus coordinates overlap')
removed=set(data['removed_unlock_focuses'])
check(len(removed)==32 and not removed.intersection(focusmap),'Political unlock focuses remain')
for group in (g for g in data['groups'] if g['party'] is not None):
    entry=focusmap[f'ISR70_p{group["party"]}_institution']
    check(not values(entry,'prerequisite'),'Party entry still requires another focus: '+group['id'])
    check(first(entry,'available')==[(group['trigger'],'=','yes')],'Party entry has redundant unlock requirements: '+group['id'])
    for node in (n for n in data['nodes'] if n['group']==group['id']):
        check(not re.search(r'ISR70_(?:party_\d+_founded|mapam_independent)',node['available']),'A governing party is blocked by a foundation flag: '+node['id'])
for rel,ast in asts.items():
    for key,op,value in walk(ast):
        if key in ('focus','has_completed_focus','relative_position_id','target') and isinstance(value,str):
            check(value not in removed,'Reference to deleted unlock focus: '+rel+'/'+value)
            if value.startswith('ISR70_'):check(value in focusmap,'Reference to nonexistent Israel focus: '+rel+'/'+value)

# Each party has two independent policy choices. Every combination must allow
# its government-programme finale; OR prerequisites stay OR, not accidental AND.
from itertools import product
choice_checks=0
for group in (g for g in data['groups'] if g['party'] is not None):
    idx=group['party'];entry=f'ISR70_p{idx}_institution';finish=f'ISR70_p{idx}_finish'
    for economy,civic in product(('ea','eb'),('ca','cb')):
        excluded={f'ISR70_p{idx}_{x}{tail}' for x in ({'ea','eb'}-{economy})|({'ca','cb'}-{civic}) for tail in ('','_deepen')}
        reachable={key for key in focusmap if not key.startswith(f'ISR70_p{idx}_')}
        previous=None
        while previous!=reachable:
            previous=set(reachable)
            for key,item in focusmap.items():
                if not key.startswith(f'ISR70_p{idx}_') or key in excluded:continue
                if all(any(parent in reachable for parent in values(row,'focus')) for row in values(item,'prerequisite')):reachable.add(key)
        check(entry in reachable and finish in reachable,f'Unreachable party policy combination: {idx}/{economy}/{civic}')
        choice_checks+=1

definitions=set()
script_sources={}
for directory in ('common/scripted_effects','common/scripted_triggers'):
    for p in (ROOT/directory).glob('*.txt'):
        s=p.read_text(encoding='utf-8-sig');script_sources[str(p.relative_to(ROOT))]=s
        definitions|=set(re.findall(r'(?m)^\w+\s*=\s*\{',s))
definitions={x.split('=')[0].strip() for x in definitions}
for rel,ast in asts.items():
    for key,op,value in walk(ast):
        if key.startswith('ISR70_') and value=='yes':check(key in definitions,'Undefined helper or trigger: '+key+' in '+rel)

effects=asts['common/scripted_effects/ISR70_effects.txt']
effect_names={k for k,op,v in effects}
dynamic_names={k for rel,ast in asts.items() if rel.startswith('common/dynamic_modifiers/') for k,op,v in ast}
opinion_names={k for rel,ast in asts.items() if rel.startswith('common/opinion_modifiers/') for k,op,v in first(ast,'opinion_modifiers',[])}
idea_root=first(asts['common/ideas/ISR70_ideas.txt'],'ideas');idea_defs={k for k,op,v in first(idea_root,'country')}
event_defs={first(e,'id') for rel,ast in asts.items() if rel.startswith('events/') for e in values(ast,'country_event')}
check(len(event_defs)==manifest['events'],'Implemented event count differs from manifest')
flags_read=set();flags_written=set()
for rel,ast in asts.items():
    for key,op,value in walk(ast):
        if key=='has_country_flag' and isinstance(value,str) and value.startswith('ISR70_'):flags_read.add(value)
        if key=='set_country_flag':
            flag=value if isinstance(value,str) else first(value,'flag','')
            if flag.startswith('ISR70_'):flags_written.add(flag)
        if key in ('add_ideas','remove_ideas','idea') and isinstance(value,str) and value.startswith('ISR70_'):check(value in idea_defs,'Unknown idea: '+value)
        if key=='modifier' and isinstance(value,str) and value.startswith('ISR70_'):check(value in dynamic_names|opinion_names,'Unknown dynamic/opinion modifier: '+value)
        if key=='country_event' and isinstance(value,list):
            ident=first(value,'id','')
            if ident.startswith(('ISR70.','ISR70P.')):check(ident in event_defs,'Unknown event: '+ident)
        if key in ('name','title','desc','custom_effect_tooltip') and isinstance(value,str) and value.startswith('ISR70_'):
            check(value in localisation,'Missing text: '+value)
        if key in ('title','desc','name') and isinstance(value,str) and value.startswith(('ISR70.','ISR70P.')):
            check(value in localisation,'Missing event text: '+value)
check(flags_read<=flags_written,'Unreachable flags: '+', '.join(sorted(flags_read-flags_written)))

# Graphics, text icons, actual asset files and small-image dimensions.
sprite_sources='\n'.join(p.read_text(encoding='utf-8-sig') for p in (ROOT/'interface').glob('*.gfx'))
sprites=set(re.findall(r'name\s*=\s*"([^\"]+)"',sprite_sources))
for key,text in localisation.items():
    for icon in re.findall(r'£([A-Za-z0-9_]+)',text):check('GFX_'+icon in sprites,'Unknown text icon: '+icon)
for rel,ast in asts.items():
    for key,op,value in walk(ast):
        if key in ('icon','picture') and isinstance(value,str):
            clean=value.strip('"')
            if clean.startswith('gfx/'):check((ROOT/clean).exists(),'Missing image: '+clean)
            elif clean.startswith('GFX_'):check(clean in sprites,'Missing sprite: '+clean)
            elif key=='picture' and clean.startswith('ISR70_spirit_'):check('GFX_idea_'+clean in sprites,'Missing national spirit artwork: '+clean)
            elif key=='icon' and rel.endswith('focus.txt'):check(clean in sprites,'Missing focus sprite: '+clean)
for key,rel in manifest['party_icons'].items():
    check((ROOT/rel).is_file(),'Missing party icon: '+key)
    try:
        im=Image.open(ROOT/rel);check(im.size==(22,22),'Incorrect party icon dimensions: '+key)
    except OSError:issues.append('Unreadable party DDS: '+key)

# Preserve the native later-history block and route all 1970 leader changes.
history=(ROOT/'history/countries/ISR - Israel.txt').read_text(encoding='utf-8-sig')
check('ISR70_initialize = yes' in history[:history.index('2000.1.1')],'1970 history integration missing')
leader=(ROOT/'common/scripted_effects/ISR_political_leaders.txt').read_text(encoding='utf-8-sig')
check('ISR70_set_party_leader = yes' in leader and '\telse = {' in leader,'Leader dispatch missing')
fallback=(ROOT/'common/scripted_effects/mdcw_1970_focus_tree_effects.txt').read_text(encoding='utf-8-sig')
check('AND = { original_tag = ISR IMP_is_1970_scenario = yes }' in fallback,'Scenario-scoped fallback protection missing')
getter=(ROOT/'common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt').read_text(encoding='utf-8-sig')
for idx in range(24):
    for suffix in ('','_desc','_icon'):check('localization_key = ISR70_party_'+str(idx)+suffix+' }' in getter,'Missing party getter: '+str(idx)+suffix)
decision_ast=[item for rel,ast in asts.items() if rel.startswith('common/decisions/') and '/categories/' not in rel for item in ast]
decision_count=sum(len(value) for key,op,value in decision_ast)
check(decision_count==manifest['total_decisions'],'Decision count mismatch')
all_decisions={key:value for cat,op,items in decision_ast for key,op,value in items}

# Regression checks for the engine errors that discarded most of the tree.
# These are supported MD forms, rather than C-style >= tokens.
for index in manifest['excluded_slots']:
    check(f'ISR70_seek_mandate_{index}' not in all_decisions,'Excluded mandate remains')
for index in sorted(set(range(24))-set(manifest['excluded_slots'])):
    available=first(all_decisions[f'ISR70_seek_mandate_{index}'],'available',[])
    checks=values(available,'check_variable')
    check(any(first(c,'var')==f'party_pop_array^{index}' and first(c,'value')=='0.5' and first(c,'compare')=='greater_than_or_equals' for c in checks),'Invalid mandate threshold: '+str(index))
for rel,ast in asts.items():
    for key,op,body in walk(ast):
        if key=='free_building_slots' and isinstance(body,list):
            size=[(operator,value) for name,operator,value in body if name=='size']
            check(len(size)==1 and size[0][0]=='>' and int(size[0][1])>=0,'Invalid building-capacity comparison: '+rel)
        if key=='reliability_factor':
            check(False,'Unsupported country reliability modifier: '+rel)
        if key=='set_politics' and isinstance(body,list):
            check(first(body,'ruling_party') in ('democratic','communism','neutrality','nationalist'),'Missing/invalid ideology group in politics tooltip: '+rel)
for rejected in ('check_variable = { treasury >= cost }','free_building_slots = { building = infrastructure size >= 1 }'):
    try:
        parse(rejected)
    except AssertionError:pass
    else:check(False,'Validator accepted an engine-breaking compound comparison')
debt_dec=all_decisions['ISR70_decision_debt_repayment']
check(not any(k=='ISR70_can_afford_1_0000' for k,op,v in walk(debt_dec)),'Debt repayment incorrectly requires a full year of GDP')
check('ISR70_can_repay_debt' in {k for k,op,v in walk(debt_dec)},'Capped debt affordability guard missing')
for key in ('ISR70_decision_civil_industry','ISR70_decision_office_project','ISR70_decision_armi_project'):
    item=all_decisions[key]
    upfront=values(item,'complete_effect');completion=values(item,'remove_effect')
    check(bool(upfront) and bool(completion),'Project must reserve its budget and deliver later: '+key)
    check(any(k.startswith('ISR70_pay_') for k,op,v in walk(upfront[0])),'Project budget missing: '+key)
    check(not any(k.startswith('ISR70_pay_') for k,op,v in walk(completion[0])),'Project charges its budget twice: '+key)
    check(any(k=='else' for k,op,v in walk(completion[0])),'Failed project cannot refund: '+key)
for key in ('ISR70_decision_talks_us','ISR70_decision_talks_egypt','ISR70_decision_talks_pal'):
    item=all_decisions[key];check(first(item,'fire_only_once')=='no','Rejected negotiations cannot be retried: '+key)
    check(not any(isinstance(v,str) and v==key+'_completed' for k,op,v in walk(item)),'Diplomacy disabled after first attempt: '+key)
check(manifest['party_slots']==20 and manifest['excluded_slots']==[8,9,10,11],'Excluded party families remain active')
check(not any(g['outlook']=='salafist' or g['party'] in (8,9,10,11) for g in data['groups']),'Excluded outlook or party branch remains')
for i in (8,9,10,11):
    check(not any(k.startswith(f'ISR70_p{i}_') for k in set(focusmap)|dynamic_names),'Excluded government programme remains: '+str(i))
    check(not any(k in all_decisions for k in (f'ISR70_seek_mandate_{i}',f'ISR70_decision_found_{i}',f'ISR70_decision_campaign_{i}')),'Excluded party decision remains: '+str(i))
    check(f'party_{i}' not in manifest['party_icons'],'Excluded party icon remains: '+str(i))
    check(f'set_variable = {{ party_banned_array^{i} = 1 }}' in (ROOT/'common/scripted_effects/ISR70_effects.txt').read_text(encoding='utf-8'),'Missing disabled native slot: '+str(i))
# Disabled native slots may still have historical registry descriptions. They
# must not reappear as authored programme/focus content or live paths.
focus_text=[localisation.get(fid+suffix,'') for fid in focusmap for suffix in ('','_desc')]
check(not any(re.search(r'\b(?:Shiite|Shia|Salafist|Salafism)\b',v,re.I) for v in focus_text),'Excluded ideology appears in authored focus content')
result={'status':'PASS' if not issues else 'FAIL','issues':issues,'focuses':len(focusmap),'decisions':decision_count,'events':len(event_defs),'party_slots':manifest['party_slots'],'party_variants':manifest['party_variants'],'party_icons':len(manifest['party_icons']),'policy_combinations_checked':choice_checks,'localisation_keys':len(localisation),'language':'English only','validation':'Static parsing, references, assets and integration. No running HOI4 session was used.'}
(ROOT/'docs/israel_1970_design/implementation_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(bool(issues))
