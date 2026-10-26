"""Validate installed VIE content against the immutable approved design."""
from pathlib import Path
import hashlib,json,re
from collections import Counter
from PIL import Image
from script_ast import parse,first,values,walk
from presentation import clean_ui
from runtime_design import load_design,load_campaign_design

ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
D=load_design()
C=load_campaign_design()
M=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
P='COLDWAR_VIE_';errors=[];checks=0
def check(ok,msg):
    global checks
    checks+=1
    if not ok:errors.append(msg)
asts={};hashes={}
for rel in M['generated']:
    path=ROOT/rel;check(path.exists(),'Missing generated output: '+rel)
    if not path.exists():continue
    hashes[rel]=hashlib.sha256(path.read_bytes()).hexdigest()
    if path.suffix in ('.txt','.gfx'):
        try:
            asts[rel]=parse(path.read_text(encoding='utf-8-sig'))
            check(not any(o in ('>=','<=','!=') for k,o,v in walk(asts[rel])),'Unsupported comparison syntax: '+rel)
        except ValueError as e:errors.append(rel+': '+str(e))
    if path.suffix=='.dds':
        im=Image.open(path);check(im.width>0 and im.height>0,'Invalid DDS: '+rel)

tree=first(asts['common/national_focus/COLDWAR_VIE_1970_focus.txt'],'focus_tree')
focuses=values(tree,'focus');all_by={first(f,'id'):f for f in focuses};approved={n['id']:n for n in D['nodes']}
check(set(all_by)==set(approved)|{n['id'] for n in C['nodes']} and len(focuses)==len(all_by)==307,'Focus IDs/count differ from the two approvals')
by={key:all_by[key] for key in approved if key in all_by}
check(first(tree,'id')==M['tree'],'Wrong tree id')
check(first(tree,'reset_on_civilwar')=='no','Civil-war progress protection missing')
check(first(first(tree,'initial_show_position'),'focus')==D['layout']['initial_focus'],'Initial camera differs')
resolved={}
def xy(key,seen=frozenset()):
    if key in resolved:return resolved[key]
    check(key not in seen,'Cyclic relative anchor: '+key)
    f=by[key];x,y=float(first(f,'x')),float(first(f,'y'));anchor=first(f,'relative_position_id')
    if anchor:
        check(anchor in by,'Missing relative anchor: '+str(anchor));ax,ay=xy(anchor,seen|{key});x+=ax;y+=ay
    resolved[key]=(x,y);return x,y
for key,f in by.items():
    n=approved[key];check(xy(key)==(n['x'],n['y']),'Coordinates differ: '+key)
    check(float(first(f,'cost'))*7==n['days'],'Duration differs: '+key)
    check([values(p,'focus') for p in values(f,'prerequisite')]==n['prerequisites'],'AND/OR prerequisites differ: '+key)
    ex=[q for e in values(f,'mutually_exclusive') for q in values(e,'focus')]
    check(ex==n['exclusive'],'Exclusions differ: '+key)
    available=first(f,'available',[])
    for clause in n['prerequisites']:
        want=[('custom_trigger_tooltip','=',[('tooltip','=',p+'_reward_applied'),('has_country_flag','=',p+'_reward_applied')]) for p in clause]
        expected=('OR','=',want)
        check(expected in available or ('hidden_trigger','=',[expected]) in available,'Unfunded parent can unlock child: '+key)
    reward=first(f,'completion_reward',[])
    check(first(reward,'effect_tooltip')==parse(n['raw_reward_code']),'Visible reward differs from approved effects: '+key)
    check(first(reward,'hidden_effect')==parse(n['completion_reward_code']),'Actual completion no longer calls guarded reward: '+key)
    check([k for k,o,v in reward]==['log','effect_tooltip','hidden_effect'],'Reward is executed or shown twice: '+key)
    for k,o,v in walk(first(f,'completion_reward',[])):
        check(not(k=='load_focus_tree'),'A reward reloads the tree: '+key)
check(len(set(resolved.values()))==239,'Focus positions overlap')

effects=asts['common/scripted_effects/COLDWAR_VIE_1970_effects.txt'];effectmap={k:v for k,o,v in effects}
triggers=asts['common/scripted_triggers/COLDWAR_VIE_1970_triggers.txt'];triggermap={k:v for k,o,v in triggers}
check([k for k,o,v in triggermap[P+'is_1970']]==['hidden_trigger'],'Internal country/scenario checks exposed in tooltips')
for key,n in approved.items():
    name=P+'apply_'+key.removeprefix(P);check(name in effectmap,'Missing reward helper: '+key)
    raw=parse(n['raw_reward_code']);body=effectmap.get(name,[])
    outer=first(body,'if',[]);inner=first(outer,'if',[])
    # All approved rewards remain as a semantic subsequence; guards/stamps are integration additions.
    check(inner[1:1+len(raw)]==raw,'Executable approved reward changed: '+key)
    check(('set_country_flag','=',key+'_reward_applied') in inner,'One-time stamp missing: '+key)
    check(('clr_country_flag','=',key+'_pending') in inner,'Pending cleanup missing: '+key)
    check(first(first(outer,'limit',[]),'NOT')==[('has_country_flag','=',key+'_reward_applied')],'Replay protection missing: '+key)

dynmap={k:v for k,o,v in asts['common/dynamic_modifiers/COLDWAR_VIE_1970_dynamic_modifiers.txt']}
for g in D['groups']:
    key=P+g['id']+'_programme';body=dynmap[key]
    keys={k for n in D['nodes'] if n['group']==g['id'] for k in n['modifiers']}
    for k in keys:check(first(body,k)==P+g['id']+'_'+k,'Unmapped dynamic value: '+key+'/'+k)
    if g['party'] is not None:check((g['gate'].splitlines()[-1].split(' = ')[0],'=','yes') in first(body,'enable',[]),'Exact party gate missing: '+key)
    if g['leader']:check(first(first(body,'enable',[]),'has_country_leader')==[('name','=','"'+g['leader']+'"'),('ruling_only','=','yes')],'Leader gate missing: '+key)
sync=effectmap[P+'sync_programmes']
check(not any(k in ('modify_treasury_effect','add_building_construction','add_timed_idea','army_experience','add_to_variable') for k,o,v in walk(sync)),'Programme sync replays rewards')

idea_body=first(first(asts['common/ideas/COLDWAR_VIE_1970_ideas.txt'],'ideas'),'country');ideas={k:v for k,o,v in idea_body}
for s in D['spirits']:
    for i,stage in enumerate(s['stages']):
        key=s['id']+'_'+str(i);actual={k:float(v) for k,o,v in first(ideas[key],'modifier')}
        check(actual==stage,'Starting/recovery spirit values differ: '+key)
for q in D['decisions']:
    key=q['id']+'_idea';actual={k:float(v) for k,o,v in first(ideas[key],'modifier')}
    check(actual==q['modifiers'],'Decision modifiers differ: '+key)
    check(first(first(ideas[key],'cancel'),'NOT')==[(q['id']+'_eligible','=','yes')],'Timed idea regime cancellation missing: '+key)
    eligible=triggermap[q['id']+'_eligible'];ors=first(eligible,'OR')
    check(len(values(ors,'AND'))==len(q['provider_focuses']),'Wrong decision provider count: '+key)
    for f,clause in zip(q['provider_focuses'],values(ors,'AND')):check(('has_country_flag','=',f+'_reward_applied') in list(walk(clause)),'Decision enabled by unearned focus: '+key)
for c in D['crises']:check({k:float(v) for k,o,v in first(ideas[c['id']],'modifier')}==c['modifiers'],'Crisis values differ: '+c['id'])

decs=asts['common/decisions/COLDWAR_VIE_1970_decisions.txt'];main=first(decs,P+'programmes');retry=first(decs,P+'deferred_projects')
check(len(main)==48 and len(retry)==239,'Decision counts differ')
for q in D['decisions']:
    node=first(main,q['id']);available=first(node,'available')
    for other in D['decisions']:
        if other['family']==q['family']:check(('NOT','=',[('has_idea','=',other['id']+'_idea')]) in available,'Family stacking guard missing: '+q['id'])

all_ideas=dict(ideas)
for rel,ast in asts.items():
    if rel.startswith('common/ideas/'):
        all_ideas.update({k:v for k,o,v in first(first(ast,'ideas',[]),'country',[])})
events=[e for rel,ast in asts.items() if rel.startswith('events/') for e in values(ast,'country_event')];eventmap={first(e,'id'):e for e in events}
check(len(eventmap)==len(events),'Duplicate event IDs')
for rel,ast in asts.items():
    for k,o,v in walk(ast):
        if k=='country_event' and isinstance(v,list):check(first(v,'id') in eventmap,'Missing event: '+str(first(v,'id')))
        if k=='add_timed_idea':check(first(v,'idea') in all_ideas,'Missing timed idea: '+str(first(v,'idea')))
        if k=='add_ideas' and isinstance(v,str):check(v in all_ideas,'Missing idea: '+v)

sprite_roots=[asts['interface/COLDWAR_VIE_1970_goals.gfx'],asts['interface/COLDWAR_VIE_1970_goals_shine.gfx']]
sprites={}
for ast in sprite_roots:
    for b in values(first(ast,'spriteTypes'),'spriteType'):
        name=first(b,'name').strip('"');check(name not in sprites,'Duplicate sprite '+name);sprites[name]=b
        tex=first(b,'texturefile').strip('"');check((ROOT/tex).exists(),'Missing sprite texture: '+tex)
for n in D['nodes']+C['nodes']:check('GFX_'+n['id'] in sprites and 'GFX_'+n['id']+'_shine' in sprites,'Focus sprite/shine missing: '+n['id'])
for key,idea in all_ideas.items():check('GFX_idea_'+first(idea,'picture') in sprites,'Idea picture unresolved: '+key)
spirit_sprites={'GFX_idea_'+first(idea,'picture') for idea in all_ideas.values()}
for key,body in dynmap.items():
    icon=first(body,'icon');check(icon in sprites,'Dynamic programme icon unresolved: '+key)
    spirit_sprites.add(icon)
for name in sorted(spirit_sprites):
    texture=first(sprites[name],'texturefile').strip('"')
    check(texture.startswith('gfx/interface/ideas/'),'National spirit uses oversized focus art: '+name)
    with Image.open(ROOT/texture) as im:
        check(im.width<=68 and im.height<=68,'National spirit exceeds selected native MD icon bounds: '+name)

locpath=ROOT/'localisation/english/COLDWAR_VIE_1970_l_english.yml';raw=locpath.read_bytes();check(raw.startswith(b'\xef\xbb\xbf'),'English localisation missing BOM')
texts=re.findall(r'^ ([^ :]+):0 (".*")$',raw.decode('utf-8-sig'),re.M);localisation={}
for key,text in texts:
    try:localisation[key]=json.loads(text)
    except json.JSONDecodeError:errors.append('Invalid localisation quoting '+key)
check(len(texts)==len(localisation),'Duplicate localisation key')
for key in all_by:check(key in localisation and key+'_desc' in localisation,'Missing focus text '+key)
for key in all_ideas:check(key in localisation and key+'_desc' in localisation,'Missing spirit text '+key)
for ast in asts.values():
    for k,o,v in walk(ast):
        if k in ('title','desc','name','tooltip') and isinstance(v,str) and v.startswith(P):check(v in localisation,'Missing English reference '+v)
check(not any(re.search(r'\b(?:Führung|Regierung|Voraussetzung|Entwurf|Entscheidungen|Gesellschaft)\b',v) for v in localisation.values()),'German text in English localisation')
for key,text in localisation.items():
    visible=re.sub(r'\$[^$]+\$','',text)
    check(not re.search(r'[-\u2010-\u2014\u2212]',visible),'Dash punctuation remains in '+key)
    check(not re.search(r'\b(?:19|20)\d{2}\b',visible),'Visible year remains in '+key)
    check(text==clean_ui(text),'Unnormalized text in '+key)
for ast in asts.values():
    for k,o,v in walk(ast):
        if k=='has_country_flag' and v.startswith(P):check(v in localisation,'Raw internal flag can leak into tooltip: '+v)

for rel in M['integration']:
    text=(ROOT/rel).read_text(encoding='utf-8-sig')
    try:parse(text)
    except ValueError as e:errors.append('Integrated file parser error '+rel+': '+str(e))
history=(ROOT/'history/countries/VIE - Vietnam.txt').read_text(encoding='utf-8-sig')
check('load_focus_tree = '+M['tree'] in history.split('2000.1.1')[0],'1970 history not routed to VIE tree')
check('COLDWAR_VIE_1970_focus' not in history.split('2000.1.1')[1],'Later history changed tree')
fallback=(ROOT/'common/scripted_effects/mdcw_1970_focus_tree_effects.txt').read_text(encoding='utf-8-sig')
check('AND = { original_tag = VIE IMP_is_1970_scenario = yes } # COLDWAR_VIE_1970_focus' in fallback,'Generic fallback can overwrite progress')
campaign_decisions=asts['common/decisions/COLDWAR_VIE_campaign_decisions.txt']
campaign_main=first(campaign_decisions,P+'campaign_programmes',[])
campaign_retry=first(campaign_decisions,P+'campaign_deferred',[])
check(len(campaign_main)==len(C['decisions']),'Campaign decision count differs')
check(len(campaign_retry)==len(C['nodes']),'Campaign deferred-project count differs')
report=dict(status='pass' if not errors else 'fail',checks=checks,errors=errors,focuses=len(all_by),original_focuses_checked=len(by),decision_programmes=len(main)+len(campaign_main),original_decision_programmes=len(main),campaign_decision_programmes=len(campaign_main),deferred_projects=len(retry)+len(campaign_retry),events=len(eventmap),sprites=len(sprites),english_strings=len(localisation),hashes=hashes,engine_tested=False)
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='hashes'},indent=2))
raise SystemExit(bool(errors))
