# IMPERIA CW — Cold War: israel 1970 — audit md patterns.
"""Audit the whole Israel module against actual MD definitions and reward forms."""
from pathlib import Path
import json
import re
from script_format import read,format_script

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
MD=Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
data=json.loads((HERE/'english_design.json').read_text(encoding='utf-8'))
manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
errors=[]
def check(ok,message):
    if not ok:errors.append(message)
def fields(ast,key):return [v for k,o,v in ast if k==key]
def one(ast,key,default=None):return next(iter(fields(ast,key)),default)
def walk(ast):
    for k,o,v in ast:
        yield k,o,v
        if isinstance(v,list):yield from walk(v)
def blocks(source,key):
    clean=re.sub(r'"(?:\\.|[^"\\])*"|#[^\n]*',lambda m:' '*len(m[0]),source)
    for match in re.finditer(r'\b'+key+r'\s*=\s*\{',clean):
        start=match.end();end=start;depth=1
        while depth:
            depth+=(clean[end]=='{')-(clean[end]=='}');end+=1
        yield source[start:end-1],source.count('\n',0,start)+1

# A key in an equipment bonus is not evidence for a country modifier. Only
# direct modifier fields from MD ideas or native dynamic-modifier roots count.
used={m for n in data['nodes'] for m in n['modifiers']}
used|={m for s in data['idea_definitions'].values() for m in s['modifiers']}
evidence={}
for p in sorted((MD/'common/ideas').glob('*.txt')):
    source=p.read_text(encoding='utf-8-sig')
    for body,line in blocks(source,'modifier'):
        for k,o,v in read(body):
            if k in used and not isinstance(v,list):evidence.setdefault(k,{'source':'MD/'+p.relative_to(MD).as_posix(),'line':line,'context':'country idea modifier'})
for p in sorted((MD/'common/dynamic_modifiers').glob('*.txt')):
    try:ast=read(p.read_text(encoding='utf-8-sig'))
    except AssertionError:continue
    for name,o,body in ast:
        if not isinstance(body,list):continue
        for k,o,v in body:
            if k in used and not isinstance(v,list):evidence.setdefault(k,{'source':'MD/'+p.relative_to(MD).as_posix(),'context':'dynamic modifier'})
for p in sorted((ROOT/'common/modifier_definitions').glob('*.txt')):
    for name,o,body in read(p.read_text(encoding='utf-8-sig')):
        if name in used:
            check(one(body,'category')=='country','Custom modifier has wrong scope: '+name)
            evidence.setdefault(name,{'source':p.relative_to(ROOT).as_posix(),'context':'registered Imperia/Cold War country modifier'})
check(used<=evidence.keys(),'Unverified country modifiers: '+', '.join(sorted(used-evidence.keys())))

references={};native_sources=[]
for name,file in [('generic','00_generic.txt'),('russia','05_russia.txt'),('israel','05_israel.txt')]:
    source=(MD/'common/national_focus'/file).read_text(encoding='utf-8-sig');native_sources.append(source)
    references[name]={'file':'MD/common/national_focus/'+file,'focuses':len(list(blocks(source,'focus')))}
for p in (MD/'common/scripted_effects').glob('*.txt'):native_sources.append(p.read_text(encoding='utf-8-sig'))
native_sources.append((MD/'events/Egypt.txt').read_text(encoding='utf-8-sig'))
native='\n'.join(native_sources)
native_commands=set(re.findall(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*=',native))
engine_docs=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV/documentation/effects_documentation.md')
if engine_docs.exists():native_commands.update(re.findall(r'^## ([a-z_]\w*)$',engine_docs.read_text(encoding='utf-8-sig'),re.M))
defined=set()
for p in (ROOT/'common/scripted_effects').glob('*.txt'):
    defined.update(re.findall(r'(?m)^([A-Za-z_]\w*)\s*=\s*\{',p.read_text(encoding='utf-8-sig')))

calls=set()
def effects(ast,scope='country'):
    for k,o,v in ast:
        if k.startswith('#') or k in ('limit','name','trigger','ai_chance'):continue
        if k in ('if','else_if','else','hidden_effect'):
            effects(v,scope);continue
        if k.isdigit():effects(v,'state');continue
        if k in ('every_country','random_country','every_other_country'):effects(v,'country');continue
        if k in ('every_state','every_owned_state','every_controlled_state','random_owned_state'):effects(v,'state');continue
        if k in ('ROOT','FROM','PREV','THIS','CONTROLLER') or re.fullmatch('[A-Z]{3}',k):
            effects(v,'country');continue
        calls.add(k)
        check(k in native_commands or k in defined,'Unknown effect command: '+k)
        if k in ('add_building_construction','add_extra_state_shared_building_slots','state_flat_productivity_change_effect','add_resistance_target','remove_resistance_target'):
            check(scope=='state','State effect in country scope: '+k)
        if k in ('set_politics','add_political_power','add_tech_bonus','modify_treasury_effect','modify_debt_effect','set_state_controller'):
            check(scope=='country','Country effect in state scope: '+k)
        if k=='set_politics':check(one(v,'ruling_party') in ('democratic','communism','neutrality','nationalist'),'Unsafe visible politics tooltip')

generated=[]
for rel in manifest['generated']:
    if not rel.endswith('.txt'):continue
    source=(ROOT/rel).read_text(encoding='utf-8-sig');ast=read(source);generated.append(rel)
    check(read(format_script(source))==ast,'Formatting changes script structure: '+rel)
    if rel in ('common/scripted_effects/ISR70_effects.txt','common/scripted_effects/ISR70_policy_effects.txt'):
        for name,o,body in ast:
            if isinstance(body,list):effects(body)
    else:
        for k,o,v in walk(ast):
            if k in ('completion_reward','complete_effect','remove_effect','option','immediate'):effects(v)
    for k,o,v in walk(ast):
        if k in ('add_ideas','idea') and isinstance(v,str) and v.startswith('ISR70_'):
            spirit=data['idea_definitions'].get(v.removeprefix('ISR70_'))
            check(not spirit or bool(spirit['modifiers']),'Empty legacy spirit is still granted: '+v)
loc=(ROOT/'localisation/english/ISR70_l_english.yml').read_text(encoding='utf-8-sig')
for n in data['nodes']:
    check(bool(n['description'].strip()),'Missing narrative: '+n['id'])
    check(not re.search(r'\b(?:MD|Imperia|completion_reward|research bonuses|automatic cores|national focus tree)\b',n['description']),'Technical implementation text in focus narrative: '+n['id'])
    check(n['id']+'_desc:0 '+json.dumps(n['description'],ensure_ascii=False) in loc,'Narrative differs from localisation: '+n['id'])
    if n['modifiers'] and not n['group'].startswith('party_'):
        check(data['idea_definitions'][n['id'].removeprefix('ISR70_')+'_idea']['treatment']==n['description'],'Spirit and focus descriptions disagree: '+n['id'])
check('GEN_1970_change_tension' not in '\n'.join(n['reward'] for n in data['nodes']),'Israel still depends on the broken generic helper file')
report={'status':'FAIL' if errors else 'PASS','errors':errors,'reference_trees':references,'verified_country_modifiers':len(evidence),'modifier_evidence':evidence,'effects_checked':sorted(calls),'generated_scripts_checked':generated,'narratives_checked':len(data['nodes']),'runtime_test':False}
(ROOT/'docs/israel_1970_design/md_pattern_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('modifier_evidence','effects_checked','generated_scripts_checked')},indent=2))
raise SystemExit(bool(errors))
