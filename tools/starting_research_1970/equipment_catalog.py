# IMPERIA COLD WAR — Native equipment, designer slots and module research catalogue.
"""Index live MD equipment plus inherited vanilla IDs for historical design fitting."""
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
from catalog import catalogue, parse, first, values, bare

GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')


def index(folder,container):
    result={}
    for base in (GAME,ROOT):
        for p in sorted((base/folder).glob('*.txt')):
            for name,operator,rows in parse(p.read_text(encoding='utf-8-sig')):
                if name!=container or not isinstance(rows,list):continue
                for key,operator,block in rows:
                    if not isinstance(block,list) or key.startswith('@') or key=='limit':continue
                    result[key]={'file':str(p),'rows':block}
    return result


def merged_block(key,definitions,stack=()):
    if key not in definitions or key in stack:return []
    rows=definitions[key]['rows']
    parent=first(rows,'parent')
    if not parent:parent=first(rows,'archetype')
    inherited=merged_block(parent,definitions,stack+(key,)) if parent and parent!=key else []
    direct={k for k,o,v in rows if v!='inherit'}
    return [item for item in inherited if item[0] not in direct]+[item for item in rows if item[2]!='inherit']


def members(value):
    return bare(value) if isinstance(value,list) else [value] if value else []


def main():
    techs,_=catalogue()
    equipment=index('common/units/equipment','equipments')
    modules=index('common/units/equipment/modules','equipment_modules')
    duplicates=index('common/units/equipment','duplicate_archetypes')
    originals=dict(equipment)
    for name,record in duplicates.items():
        base=first(record['rows'],'archetype')
        if not base:continue
        if name not in equipment:
            equipment[name]={'file':record['file'],'rows':[('parent','=',base)]+record['rows'],'generated_from':base}
        for key,row in originals.items():
            if first(row['rows'],'archetype')!=base or not key.startswith(base):continue
            generated=name+key[len(base):]
            if generated not in equipment:
                role=first(record['rows'],'type')
                rows=[('parent','=',key),('archetype','=',name)]+([('type','=',role)] if role is not None else [])+[item for item in row['rows'] if item[0] not in {'parent','archetype','type'}]
                equipment[generated]={'file':record['file'],'rows':rows,'generated_from':key}
    enabling_modules={};enabling_equipment={}
    for key,row in techs.items():
        for module in row['enable_equipment_modules']:enabling_modules.setdefault(module,[]).append(key)
        for item in row['enable_equipments']:enabling_equipment.setdefault(item,[]).append(key)
    result_e={};result_m={}
    for key,row in equipment.items():
        rows=merged_block(key,equipment)
        slots=first(rows,'module_slots',[])
        if not isinstance(slots,list):slots=[]
        result_e[key]={
            'file':row['file'],'parent':first(row['rows'],'parent'),'archetype':first(rows,'archetype'),
            'generated_from':row.get('generated_from'),
            'year':first(rows,'year'),'type':members(first(rows,'type',[])),
            'module_slots':{name:{'categories':members(first(block,'allowed_module_categories',[])), 'required':first(block,'required'),'default_module':first(block,'default_module')} for name,op,block in slots if isinstance(block,list)},
            'enable_techs':enabling_equipment.get(key,[]),
            'direct_rows':row['rows'],
        }
    for key,row in modules.items():
        rows=merged_block(key,modules)
        result_m[key]={
            'file':row['file'],'parent':first(row['rows'],'parent'),
            'category':first(rows,'category'),'categories':members(first(rows,'categories',[])),
            'enable_techs':enabling_modules.get(key,[]),
            'tech_years':{t:techs[t]['year'] for t in enabling_modules.get(key,[])},
            'add_stats':first(rows,'add_stats',[]),'multiply_stats':first(rows,'multiply_stats',[]),
            'allowed_module_categories':{slot:members(cats) for slot,op,cats in first(rows,'allowed_module_categories',[])},
            'allow_equipment_type':first(rows,'allow_equipment_type',[]),
            'forbid_equipment_type':first(rows,'forbid_equipment_type',[]),
            'forbid_equipment_type_exact_match':first(rows,'forbid_equipment_type_exact_match'),
            'direct_rows':row['rows'],
        }
    (HERE/'equipment_catalog.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','equipment':result_e},indent=2)+'\n',encoding='utf-8')
    (HERE/'module_catalog.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','modules':result_m},indent=2)+'\n',encoding='utf-8')
    lines=['IMPERIA COLD WAR: modules with a pre1970 enabling technology or no direct tech lock','ID\tCATEGORY\tENABLING_TECHS\tYEARS']
    for key,row in result_m.items():
        years=list(row['tech_years'].values())
        if not years or any(y is None or y<=1969 for y in years):lines.append(key+'\t'+str(row['category'])+'\t'+','.join(row['enable_techs'])+'\t'+','.join(str(y) for y in years))
    (HERE/'early_modules.tsv').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'equipment':len(equipment),'modules':len(modules),'early_or_unlocked_modules':len(lines)-2}))


if __name__=='__main__':main()
