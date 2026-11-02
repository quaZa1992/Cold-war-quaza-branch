# IMPERIA COLD WAR — Independent Korea/Japan reward revision source checks.
"""Compare the actual emitted graphs and effects with the private pre-revision copy."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'docs/reward_rework_20261027'
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,values,walk


def live_paths():
    result=set()
    for directory in ('common','events','interface','localisation/english'):
        result.update(p.relative_to(ROOT).as_posix() for p in (ROOT/directory).rglob('*')
            if p.is_file() and re.match(r'COLDWAR_(?:NKO|KOR|JAP)',p.name) and p.suffix in {'.txt','.gfx','.gui','.yml'})
    before=json.loads((REPORT/'BEFORE.json').read_text(encoding='utf-8'))
    result.update(p for p in before['runtime_sha256'] if not re.search(r'COLDWAR_(?:NKO|KOR|JAP)',p))
    return sorted(result)


def main():
    before=json.loads((REPORT/'BEFORE.json').read_text(encoding='utf-8'))
    backup=Path(before['runtime_backup'])
    paths=live_paths()
    # Reuse the integration's bounded API/reference checker against the NEW
    # feature inventory and output directory, preserving previous evidence.
    (REPORT/'INITIAL_IMPORT.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','files':paths},indent=2)+'\n',encoding='utf-8')
    (REPORT/'INTEGRATION.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','installed':paths},indent=2)+'\n',encoding='utf-8')
    sys.path.insert(0,str(ROOT/'tools/quaza_eastasia_integration'))
    spec=importlib.util.spec_from_file_location('reward_revision_api_audit',ROOT/'tools/quaza_eastasia_integration/validate.py')
    audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
    audit.REPORT=REPORT
    api_failed=audit.main()
    errors=[];graphs={};research=[];equipment=[]
    tech_categories=set()
    equipment_types=set()
    for p in (ROOT/'common/technologies').glob('*.txt'):
        for key,op,body in walk(parse(p.read_text(encoding='utf-8-sig'))):
            if key=='categories' and isinstance(body,list):
                tech_categories.update(v for k,o,v in body if k=='_bare')
    for p in (ROOT/'common/units/equipment').glob('*.txt'):
        rows=first(parse(p.read_text(encoding='utf-8-sig')),'equipments',[])
        equipment_types.update(k for k,o,v in rows)
        # Native bonuses also accept actual equipment categories/types. MD's
        # modular aircraft derive fighter/naval_bomber from their fitted modules.
        for name,op,body in rows:
            if not isinstance(body,list):continue
            for field in ('type','allowed_types','categories'):
                for entry in values(body,field):
                    if isinstance(entry,str):equipment_types.add(entry)
                    elif isinstance(entry,list):equipment_types.update(v for k,o,v in entry if k=='_bare')
    for tag in ('NKO','KOR','JAP'):
        relative=f'common/national_focus/COLDWAR_{tag}_1970_focus.txt'
        def foci(base):
            return {first(f,'id'):f for f in values(first(parse((base/relative).read_text(encoding='utf-8')),'focus_tree'),'focus')}
        old=foci(backup);new=foci(ROOT)
        if old.keys()!=new.keys():errors.append('Changed focus ID set: '+tag)
        for identifier,node in new.items():
            previous=old.get(identifier,[])
            for field in ('x','y','relative_position_id','cost','prerequisite','mutually_exclusive'):
                if values(node,field)!=values(previous,field):errors.append('Changed graph/time: '+identifier+' '+field)
        graphs[tag]={'focuses':len(new),'graph_and_days_unchanged':not any(tag in e for e in errors)}
    for relative in paths:
        if not relative.endswith(('.txt','.gfx','.gui')):continue
        raw=(ROOT/relative).read_bytes();rows=parse(raw.decode('utf-8-sig'))
        if re.search(r'(?<![\w.])-?\d+\.\d{6,}(?![\w.])',raw.decode('utf-8-sig')) and re.search(r'COLDWAR_(?:NKO|KOR|JAP)',Path(relative).name):
            errors.append('Unsafe fixed-point precision: '+relative)
        for key,op,body in walk(rows):
            if key=='add_tech_bonus' and isinstance(body,list):
                for category in values(body,'category'):
                    research.append({'file':relative,'category':category,'uses':first(body,'uses'),'bonus':first(body,'bonus')})
                    if category not in tech_categories:errors.append('Research category has no current technologies: '+str(category)+' '+relative)
            if key=='add_equipment_bonus' and isinstance(body,list):
                for target,o,bonus in first(body,'bonus',[]):
                    equipment.append({'file':relative,'name':first(body,'name'),'target':target,'modifiers':bonus})
                    if target not in equipment_types:errors.append('Missing actual equipment type: '+target+' '+relative)
    result={'project':'IMPERIA COLD WAR','graphs':graphs,'errors':errors,'api_audit_failed':bool(api_failed),'research_bonus_occurrences':research,'equipment_bonus_occurrences':equipment,'runtime_files':len(paths),'runtime_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},'scope':'Actual emitted graph/time preservation, live category/equipment resolution and bounded API/reference audit. Not a native UI, campaign, save/rehost or multiplayer test.'}
    result['success']=not errors and not api_failed
    (REPORT/'SOURCE_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'success':result['success'],'graphs':graphs,'errors':errors,'research_bonus_occurrences':len(research),'equipment_bonus_occurrences':len(equipment)}))
    return not result['success']


if __name__=='__main__':raise SystemExit(main())
