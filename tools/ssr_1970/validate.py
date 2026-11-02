# IMPERIA COLD WAR — validate installed SSR output against the approved design.
from pathlib import Path
import hashlib,json,re,sys
import shared
sys.path.insert(0,str(shared.ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,values,walk

ROOT=shared.ROOT
HERE=shared.HERE

def main():
    manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
    errors=[];warnings=[]
    outputs=[ROOT/path for path in manifest['outputs']]
    scripts={}
    for path in outputs:
        raw=path.read_bytes();text=raw.decode('utf-8-sig')
        if path.suffix=='.yml':
            if not raw.startswith(b'\xef\xbb\xbf'):errors.append('Localisation missing BOM: '+str(path))
        elif path.suffix=='.txt':
            if raw.startswith(b'\xef\xbb\xbf'):errors.append('Script BOM: '+str(path))
            try:scripts[path]=parse(text)
            except Exception as error:errors.append('Parse '+str(path)+': '+str(error))
        first_lines=text.splitlines()[:2]
        if not any('IMPERIA COLD WAR' in line for line in first_lines):errors.append('Missing file marker: '+str(path))
        if 'COLDWAR_SSR' in path.name:
            for match in re.finditer(r'(?<![\w.])-?\d+\.(\d+)(?![\w.])',text):
                if len(match[1])>5:errors.append('Overprecision '+str(path)+': '+match[0])

    tree_path=ROOT/'common/national_focus/COLDWAR_SSR_1970_focus.txt'
    tree=first(scripts.get(tree_path,[]),'focus_tree',[])
    focus_list=values(tree,'focus');actual={first(f,'id'):f for f in focus_list}
    expected={n['id']:n for n in shared.nodes()}
    if len(actual)!=len(focus_list):errors.append('Duplicate focus IDs')
    if set(actual)!=set(expected):errors.append('Focus coverage differs from approved model')
    coords={}
    party_triggers=shared.data()['party_triggers']
    for identifier,f in actual.items():
        n=expected[identifier];a=first(f,'relative_position_id')
        x=int(first(f,'x'));y=int(first(f,'y'))
        if a:
            if a not in coords:errors.append('Forward/missing anchor '+identifier)
            else:x+=coords[a][0];y+=coords[a][1]
        coords[identifier]=(x,y)
        if (x,y)!=(n['x'],n['y']):errors.append('Coordinate mismatch '+identifier)
        prereqs=[values(p,'focus') for p in values(f,'prerequisite')]
        if prereqs!=n['prerequisites']:errors.append('Prerequisite mismatch '+identifier)
        exclusions=values(first(f,'mutually_exclusive',[]),'focus')
        if exclusions!=n['exclusive']:errors.append('Mutual exclusion mismatch '+identifier)
        if float(first(f,'cost'))!=n['cost']:errors.append('Cost mismatch '+identifier)
        available=first(f,'available',[])
        needed='COLDWAR_SSR_is_ssr' if n['phase']=='ssr' else 'COLDWAR_SSR_is_independent'
        if not any(k==needed and v=='yes' for k,_,v in walk(available)):errors.append('Missing status gate '+identifier)
        if n['phase']=='party':
            trigger=party_triggers[n['gate'][4:]]
            if first(available,trigger)!='yes':errors.append('Wrong party gate '+identifier)
        visibility=first(f,'allow_branch',[])
        if n['scope_tag']:
            if visibility!=[('original_tag','=',n['scope_tag'])]:errors.append('Non-country visibility '+identifier)
        elif visibility:errors.append('Hidden universal branch '+identifier)

    effect_defs=set();trigger_defs=set();local_keys=set();categories=set();idea_defs=set();dynamic_defs=set()
    for path in (ROOT/'common/ideas').glob('COLDWAR_SSR*.txt'):
        rows=parse(path.read_text(encoding='utf-8-sig'))
        container=first(rows,'ideas',[])
        if not container:errors.append('Invalid native ideas container '+str(path))
        for category,_,body in container:
            if isinstance(body,list):idea_defs.update(k for k,_,v in body if isinstance(v,list))
    for path in (ROOT/'common/dynamic_modifiers').glob('COLDWAR_SSR*.txt'):
        dynamic_defs.update(k for k,_,v in parse(path.read_text(encoding='utf-8-sig')) if isinstance(v,list))
    for path in (ROOT/'common/scripted_effects').glob('*.txt'):
        effect_defs.update(re.findall(r'^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{',path.read_text(encoding='utf-8-sig',errors='replace'),re.M))
    for path in (ROOT/'common/scripted_triggers').glob('*.txt'):
        trigger_defs.update(re.findall(r'^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{',path.read_text(encoding='utf-8-sig',errors='replace'),re.M))
    for path in (ROOT/'localisation/english').glob('*.yml'):
        local_keys.update(re.findall(r'^\s*([^\s:#]+):',path.read_text(encoding='utf-8-sig',errors='replace'),re.M))
    for path in (ROOT/'common/decisions/categories').glob('*.txt'):
        categories.update(re.findall(r'^(\w+)\s*=\s*\{',path.read_text(encoding='utf-8-sig',errors='replace'),re.M))
    for path,rows in scripts.items():
        if path.parent.name=='decisions':
            for category,_,body in rows:
                if category not in categories:errors.append('Missing decision category '+category)
        for name,op,value in walk(rows):
            if name.startswith('COLDWAR_SSR_') and value in ('yes','no') and name not in effect_defs|trigger_defs:
                errors.append('Unresolved SSR callback '+name+' in '+str(path.relative_to(ROOT)))
            if name in ('custom_effect_tooltip','tooltip','localization_key','unlock_decision_tooltip') and isinstance(value,str) and value.startswith('COLDWAR_SSR_') and value not in local_keys:
                errors.append('Unresolved tooltip '+value)
            if name=='country_exists' and value in ('yes','no'):errors.append('Invalid country_exists boolean '+str(path))
            if name in ('add_ideas','remove_ideas') and isinstance(value,str) and value.startswith('COLDWAR_SSR_') and value not in idea_defs:
                errors.append('Unregistered idea '+value)
            if name=='add_timed_idea' and isinstance(value,list):
                target=first(value,'idea','')
                if target.startswith('COLDWAR_SSR_') and target not in idea_defs:errors.append('Unregistered timed idea '+target)
            if name in ('add_dynamic_modifier','remove_dynamic_modifier','has_dynamic_modifier') and isinstance(value,list):
                target=first(value,'modifier','')
                if target.startswith('COLDWAR_SSR_') and target not in dynamic_defs:errors.append('Unregistered dynamic modifier '+target)
    for identifier in expected:
        if identifier not in local_keys or identifier+'_desc' not in local_keys:errors.append('Missing focus localisation '+identifier)
    finance=(ROOT/'common/scripted_effects/00_money_system.txt').read_text(encoding='utf-8')
    if finance.count('COLDWAR_SSR_add_weekly_expenses = yes')!=1:errors.append('Weekly consumer is not exactly once')
    fallback=(ROOT/'common/scripted_effects/mdcw_1970_focus_tree_effects.txt').read_text(encoding='utf-8')
    if fallback.count('AND = { IMP_is_1970_scenario = yes has_focus_tree = COLDWAR_SSR_1970_focus }')!=1:
        errors.append('Authored SSR tree is not preserved by legacy fallback events')
    report=shared.baseline();report.update(errors=sorted(set(errors)),warnings=warnings,installed_focuses=len(actual),countries=len(shared.TAGS),
       outputs=len(outputs),scope='Static emitted-code, encoding, graph, condition and reference checks. Native game tests are reported separately.')
    (HERE/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
