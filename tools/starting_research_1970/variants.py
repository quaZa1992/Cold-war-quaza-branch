# IMPERIA COLD WAR — January 1970 native historical equipment variants.
"""Compile evidenced designs after their bare hulls and exact service components."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
from catalog import catalogue, first, bare

PROJECT='IMPERIA COLD WAR'
FEATURE='# IMPERIA COLD WAR — January 1970 historical equipment variants.'
BEGIN=FEATURE+' BEGIN'
END=FEATURE+' END'
FLAG='COLDWAR_1970_historical_variants_assigned'
FILES=('europe_variants.json','asia_variants.json','africa_variants.json','americas_oceania_variants.json','usa_variants.json')
SUPPORT_PATH=ROOT/'common/technologies/COLDWAR_1970_service_components.txt'


def load_variants():
    models={};countries={}
    for filename in FILES:
        data=json.loads((HERE/filename).read_text(encoding='utf-8-sig'))
        assert data['project']==PROJECT and data['cutoff']=='1970-01-01',filename
        for key,row in data['models'].items():
            assert key not in models,key
            models[key]=dict(row,source_manifest=filename)
        for tag,assigned in data['countries'].items():
            assert tag not in countries,tag
            countries[tag]=assigned
    expected={p.stem[:3] for p in (ROOT/'history/countries').glob('*.txt')}
    assert set(countries)==expected,sorted(expected-set(countries))
    assert all(key in models for assigned in countries.values() for key in assigned)
    return models,countries


def bundle_name(modules,hulls,group='common'):
    signature=json.dumps({'modules':sorted(modules),'hulls':sorted(hulls),'group':group},sort_keys=True)
    return 'COLDWAR_1970_service_components_'+hashlib.sha256(signature.encode()).hexdigest()[:16]


def minimum_enablers(key,equipment,techs,seen=()):
    if key not in equipment or key in seen:return []
    row=equipment[key]
    year=int(float(row['year'])) if row.get('year') is not None else 9999
    choices=[x for x in row['enable_techs'] if x in techs and not x.startswith('COLDWAR_1970_service_components_') and (techs[x]['year']<=1969 if techs[x]['year'] is not None else year<=1969)]
    if choices:return sorted(choices,key=lambda x:(techs[x]['year'] if techs[x]['year'] is not None else year,x))
    origin=row.get('generated_from')
    # The transport helicopter derivative must not acquire the parent's
    # attack-helicopter programme merely to expose its unarmed bare frame.
    if origin and key.startswith('heavy_tank_amphibious_chassis_'):
        return []
    if origin:return minimum_enablers(origin,equipment,techs,seen+(key,))
    return []


def service_hulls(key,equipment):
    result={key}
    origin=equipment[key].get('generated_from')
    # These prefix-correct historical copies have no broad research node.
    # Enable both the exact native role and its own bare physical frame before
    # create_equipment_variant. Do not expose an attack-helicopter parent.
    if origin and Path(equipment[origin]['file']).name=='MD_w_COLDWAR_1970_historical_role_frames.txt':
        result.add(origin)
    return result


def primary_module_roles(key,modules,seen=()):
    if key not in modules or key in seen:return set()
    row=modules[key]
    value=first(row['direct_rows'],'add_equipment_type')
    if value is None:
        return primary_module_roles(row.get('parent'),modules,seen+(key,))
    return set(bare(value) if isinstance(value,list) else [value])


def plan(profiles,techs,base_groups):
    import build
    models,countries=load_variants()
    equipment=json.loads((HERE/'equipment_catalog.json').read_text(encoding='utf-8'))['equipment']
    modules=json.loads((HERE/'module_catalog.json').read_text(encoding='utf-8'))['modules']
    # A static design can be used beside either designer. Its native enabling
    # node may exist only in the other DLC tree, so a union of all branches is
    # insufficient evidence that the current design's bare type is available.
    routing={key:{group for group,items in build.selections({'name':key,'domains':{},'add_techs':[key]},techs).items() if key in items} for key,row in techs.items() if row['year'] is None or row['year']<=1969}
    bundles={};support={};synthetic={}
    for tag,assigned in countries.items():
        known=set().union(*(set(items) for items in base_groups[tag].values()))
        additions=set();components=set();hulls=set();reasons=[]
        branch_components={group:set() for group in ('common','nsb','legacy','bba','non_bba')}
        branch_hulls={group:set() for group in branch_components}
        for key in assigned:
            model=models[key]
            assert model['service_by']<='1969-12-31',(tag,key)
            required=model.get('requires_dlc',[])
            assert len(required)<=1,(tag,key,'Unsupported combined DLC design')
            primary={'No Step Back':'nsb','By Blood Alone':'bba'}.get(required[0],'common') if required else 'common'
            alternatives=[(model,primary)]
            if model.get('fallback'):alternatives.append((model['fallback'],{'nsb':'legacy','bba':'non_bba'}[primary]))
            for design,group in alternatives:
                eq=design['type'];assert eq in equipment,(tag,key,eq)
                main=design.get('modules',{}).get('fixed_main_weapon_slot')
                if main and main!='empty':
                    roles=primary_module_roles(main,modules)
                    assert not roles or roles&set(equipment[eq]['type']),(tag,key,eq,main,'Primary aircraft module role must match the actual native equipment type',sorted(roles),equipment[eq]['type'])
                candidates=minimum_enablers(eq,equipment,techs)
                enablers=[tech for tech in candidates if routing[tech]&{'common',group}]
                required_enablers=[]
                if enablers:
                    required_enablers=[next((tech for tech in enablers if tech in known|additions),enablers[0])]
                elif group=='common':
                    # A native mirrored pair can expose the same static gun
                    # in every configuration without a duplicate bare frame.
                    for yes,no in [('nsb','legacy'),('bba','non_bba'),('got','non_got')]:
                        left=[tech for tech in candidates if yes in routing[tech]]
                        right=[tech for tech in candidates if no in routing[tech]]
                        if left and right:
                            required_enablers=[left[0],right[0]]
                            break
                # An imported old design must not promote its operator's
                # national research to the later date of MD's generic chassis.
                # Reuse an already researched native family, otherwise expose
                # only the exact operated bare type through service knowledge.
                if eq==model['type'] and model.get('native_md_contract') in {'modular_aircraft','modular_ground','modular_ship','fixed_transport_helicopter'} and required_enablers and not any(tech in known for tech in required_enablers):
                    required_enablers=[]
                if not required_enablers:
                    physical_year=int(float(equipment[eq].get('year') or 9999))
                    assert physical_year<=1969 or model.get('type_year_exception'),f'No evidenced pre1970 bare-equipment unlock for {tag}/{key}/{eq}'
                    exact_hulls=service_hulls(eq,equipment)
                    hulls.update(exact_hulls)
                    branch_hulls[group].update(exact_hulls)
                    reasons.append({'model':key,'equipment':eq,'technology':None,'group':group,'reason':'Exact documented service frame has no pre1970 enabling research node in every DLC configuration where this design is created; grant its bare frame through the matching narrow service-knowledge bundle before the design.'})
                else:
                    for selected in required_enablers:
                        if selected in known|additions:continue
                        additions.add(selected)
                        reasons.append({'model':key,'equipment':eq,'technology':selected,'reason':'Minimum existing active or mirrored native family required before the documented service design is created.'})
                for slot,module in design.get('modules',{}).items():
                    if module=='empty':continue
                    assert module in modules,(tag,key,module)
                    components.add(module)
                    branch_components[group].add(module)
        # Hard technology dependencies are satisfied without filling every
        # optional incoming research path or unrelated design specialisation.
        while True:
            new={dep for technology in additions for dep in techs[technology].get('dependencies',[]) if dep not in known|additions}
            if not new:break
            assert all((techs[x]['year'] or 9999)<=1969 for x in new),new
            additions.update(new)
        selected_bundles={}
        for group in branch_components:
            group_modules=branch_components[group];group_hulls=branch_hulls[group]
            if not(group_modules or group_hulls):continue
            bundle=bundle_name(group_modules,group_hulls,group)
            selected_bundles[group]=bundle
            branch=[]
            if group!='common':
                dlc='No Step Back' if group in ('nsb','legacy') else 'By Blood Alone'
                branch=[['has_dlc','=','"'+dlc+'"']]
                if group in ('legacy','non_bba'):branch=[['NOT','=',branch]]
            bundles[bundle]={'modules':sorted(group_modules),'hulls':sorted(group_hulls),'group':group,'allow_branch':branch}
            synthetic[bundle]={'file':SUPPORT_PATH.relative_to(ROOT).as_posix(),'year':1969,'folders':[],'categories':[],'paths':[],'xor':[],'dependencies':[],'allow':[['always','=','no']],'allow_branch':branch,'doctrine':None,'enable_equipments':sorted(group_hulls),'enable_equipment_modules':sorted(group_modules),'special_projects':[]}
        support[tag]={'research_additions':sorted(additions),'component_bundle':selected_bundles.get('common'),'component_bundles':selected_bundles,'modules':sorted(components),'bare_equipment':sorted(hulls),'reasons':reasons,'models':assigned}
    return models,countries,support,bundles,synthetic


def render_support(bundles):
    rows=[FEATURE,'# Generated by tools/starting_research_1970/variants.py. Exact historical service components only.','technologies = {']
    for name,entry in sorted(bundles.items()):
        rows+=['\t'+name+' = {','\t\tallow = { always = no }','\t\tresearch_cost = 1','\t\tstart_year = 1969']
        group=entry.get('group','common')
        if group!='common':
            dlc='No Step Back' if group in ('nsb','legacy') else 'By Blood Alone'
            condition='has_dlc = "'+dlc+'"'
            if group in ('legacy','non_bba'):condition='NOT = { '+condition+' }'
            rows+=['\t\tallow_branch = { '+condition+' }']
        for field,items in [('enable_equipments',entry['hulls']),('enable_equipment_modules',entry['modules'])]:
            if items:rows+=['\t\t'+field+' = {']+['\t\t\t'+item for item in items]+['\t\t}']
        rows+=['\t\tai_will_do = { factor = 0 }','\t}']
    return '\n'.join(rows+['}',''])


def native_design(model,depth=2,fallback=False):
    design=model['fallback'] if fallback else model
    tab='\t'*depth
    name=model['name'];assert not any(x in name for x in ['"','\n','\r','\u2013','\u2014']),name
    lines=[tab+'create_equipment_variant = {',tab+'\tname = "'+name+'"',tab+'\ttype = '+design['type']]
    if design.get('modules'):
        lines += [tab+'\tmodules = {']+[tab+'\t\t'+slot+' = '+module for slot,module in design['modules'].items()]+[tab+'\t}']
    if design.get('upgrades'):
        lines += [tab+'\tupgrades = {']+[tab+'\t\t'+key+' = '+str(value) for key,value in design['upgrades'].items()]+[tab+'\t}']
    # Historical designs start active. No future MIO, designer, XP, obsolete
    # flag or implicit stockpile is copied from a later scenario.
    if model.get('icon') and not fallback:lines.append(tab+'\ticon = "'+model['icon']+'"')
    return lines+[tab+'}']


def render_country(tag,models,countries):
    lines=['\t'+BEGIN,'\tif = {','\t\tlimit = { IMP_is_1970_scenario = yes NOT = { has_country_flag = '+FLAG+' } }','\t\tset_country_flag = '+FLAG]
    for key in countries[tag]:
        model=models[key];dlcs=model.get('requires_dlc',[])
        if dlcs:
            trigger=' '.join('has_dlc = "'+dlc+'"' for dlc in dlcs)
            lines+=['\t\tif = {','\t\t\tlimit = { '+trigger+' }']+native_design(model,3)+['\t\t}']
            if model.get('fallback'):lines+=['\t\telse = {']+native_design(model,3,True)+['\t\t}']
        else:lines+=native_design(model,2)
    return '\n'.join(lines+['\t}','\t'+END])+'\n'


def strip_block(source):
    return re.sub(r'(?m)^\t'+re.escape(BEGIN)+r'\n.*?^\t'+re.escape(END)+r'\n','',source,flags=re.S)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--apply-support',action='store_true');args=parser.parse_args()
    import build
    profiles=build.profiles();techs,_=catalogue()
    groups={tag:build.full_selections(row,techs) for tag,row in profiles.items()}
    models,countries,support,bundles,synthetic=plan(profiles,techs,groups)
    if args.apply_support:SUPPORT_PATH.write_bytes(render_support(bundles).encode('utf-8'))
    (HERE/'variant_support.json').write_text(json.dumps({'project':PROJECT,'countries':support,'bundles':bundles},indent=2)+'\n',encoding='utf-8')
    (HERE/'variant_manifest.json').write_text(json.dumps({'project':PROJECT,'cutoff':'1970-01-01','models':models,'countries':countries},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'project':PROJECT,'models':len(models),'assignments':sum(map(len,countries.values())),'bundles':len(bundles),'countries':len(countries)}))


if __name__=='__main__':main()
