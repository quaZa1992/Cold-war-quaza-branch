# IMPERIA COLD WAR — Worldwide January 1970 starting research in country history.
"""Compile researched country capabilities into bounded, scenario-only history blocks."""
import argparse
import hashlib
import itertools
import json
import os
import re
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from catalog import catalogue, first, parse

PROJECT = 'IMPERIA COLD WAR'
FEATURE = '# IMPERIA COLD WAR — January 1970 researched national technology baseline.'
BEGIN = FEATURE + ' BEGIN'
END = FEATURE + ' END'
FLAG = 'COLDWAR_1970_world_research_assigned'
PROFILE_FILES = ('europe_profiles.json','asia_profiles.json','africa_profiles.json','americas_oceania_profiles.json')

# Each chain is deliberately independent. Owning an imported jet does not
# imply integrated circuits, robotic factories or an indigenous engine design.
CHAINS = {
    'construction': [(1940,'mdcw_engineering_basics_1940'),(1949,'mdcw_tower_cranes_1949'),(1950,'mdcw_ready_mixed_concrete_1950'),(1954,'mdcw_hydraulic_earthmoving_1954'),(1960,'mdcw_precast_construction_1960')],
    'machinery': [(1940,'mdcw_precision_machine_tools_1940'),(1950,'mdcw_powered_machinery_1950'),(1955,'mdcw_numerical_control_1955'),(1961,'mdcw_industrial_robotics_1961')],
    'grid': [(1955,'mdcw_regional_grid_1955'),(1965,'mdcw_grid_dispatch_1965')],
    'computing': [(1945,'basic_computing'),(1955,'integrated_circuit'),(1965,'computing_1')],
    'infantry': [(1940,'mdcw_infantry_weapons_1940'),(1950,'mdcw_infantry_weapons_1950'),(1955,'mdcw_infantry_weapons_1955'),(1965,'infantry_weapons_1')],
    'support': [(1940,'mdcw_support_weapons_1940'),(1955,'mdcw_support_weapons_1955'),(1957,'mdcw_gpmg_support_1957'),(1965,'support_weapons')],
    'communications': [(1940,'mdcw_cnc_equipment_1940'),(1943,'mdcw_portable_radios_1943'),(1950,'mdcw_cnc_equipment_1950'),(1960,'mdcw_cnc_equipment_1960')],
    'vehicles': [(1940,'mdcw_util_vehicle_1940'),(1941,'mdcw_light_4x4_vehicles_1941'),(1950,'mdcw_util_vehicle_1950'),(1960,'mdcw_util_vehicle_1960'),(1965,'util_vehicle_1')],
    'camouflage': [(1940,'mdcw_camouflage_1940'),(1950,'mdcw_camouflage_1950')],
    'special_forces': [(1940,'mdcw_special_forces_1940'),(1950,'mdcw_special_forces_1950'),(1965,'special_forces_tech_1')],
    'night_vision': [(1950,'mdcw_night_vision_1950'),(1965,'night_vision_1')],
    'body_armor': [(1945,'mdcw_body_armor_1945'),(1960,'mdcw_body_armor_1960')],
    'anti_tank': [(1940,'mdcw_anti_tank_1940'),(1950,'mdcw_anti_tank_1950'),(1965,'Anti_tank_1')],
    'anti_air': [(1940,'mdcw_nsb_anti_air_1940'),(1950,'mdcw_nsb_anti_air_1950'),(1965,'nsb_Anti_Air_0')],
    'artillery': [(1940,'mdcw_m101_model_1940_nsb'),(1955,'mdcw_m101_service_model_1955_nsb'),(1965,'nsb_artillery_1')],
    'armor': [(1940,'mdcw_ww2_tank_chassis_1940_nsb'),(1943,'mdcw_ww2_tank_chassis_1943_nsb'),(1945,'mbt_tech_ops'),(1955,'mdcw_postwar_medium_tank_1955_nsb'),(1965,'mbt_tech')],
    'jet_light': [(1940,'mdcw_early_airframes_1945'),(1950,'mdcw_gen_1_light'),(1955,'mdcw_gen_2_light'),(1960,'gen_3_light')],
    'jet_medium': [(1950,'mdcw_early_airframes_1945'),(1950,'mdcw_gen_1_medium'),(1955,'mdcw_gen_2_medium'),(1960,'gen_3_medium')],
    'aircraft_modules': [(1945,'mdcw_early_airframes_1945'),(1955,'early_airframe_designs'),(1955,'early_weapons')],
    'helicopter': [(1945,'helo_ops_tech'),(1955,'mdcw_utility_helicopter_1955'),(1965,'nsb_transport_helicopter_1')],
    'naval_surface': [(1945,'tech_naval_systems_engineering'),(1945,'tech_early_naval_weapon_systems'),(1965,'corvette_hull_1'),(1965,'frigate_hull_1'),(1965,'tech_diesel_power_systems_1')],
    'naval_submarine': [(1945,'tech_submarine_engineering_1'),(1959,'mdcw_diesel_submarine_hull_1959'),(1965,'mdcw_submarine_reactor_1955'),(1965,'mdcw_attack_submarine_hull_1955'),(1965,'tech_submarine_engineering_2'),(1965,'attack_submarine_hull_1')],
}

# Alternatives expose the same evidence-backed family in each native DLC tree.
PAIRS = {
    'mdcw_nsb_anti_air_1940':'mdcw_anti_air_1940',
    'mdcw_nsb_anti_air_1950':'mdcw_anti_air_1950',
    'nsb_Anti_Air_0':'Anti_Air_0',
    'mdcw_m101_model_1940_nsb':'mdcw_m101_model_1940_legacy',
    'mdcw_m101_service_model_1955_nsb':'mdcw_m101_service_model_1955_legacy',
    'nsb_artillery_1':'tech_arty_0',
    'mdcw_155mm_m114_option_nsb':'mdcw_155mm_m114_option_legacy',
    'mdcw_ww2_tank_chassis_1940_nsb':'mdcw_ww2_tank_chassis_1940_legacy',
    'mdcw_ww2_tank_chassis_1943_nsb':'mdcw_ww2_tank_chassis_1943_legacy',
    'mdcw_postwar_medium_tank_1955_nsb':'mdcw_postwar_medium_tank_1955_legacy',
    'mbt_tech':'MBT_1',
    'nsb_transport_helicopter_1':'transport_helicopter_1',
    'nsb_attack_helicopter_tech_1':'attack_helicopter_1',
}
LEGACY_AIR = [(1940,'mdcw_piston_fighter_1940'),(1945,'early_fighter'),(1950,'mdcw_early_jet_fighter_1950'),(1955,'mdcw_early_supersonic_fighter_1955'),(1960,'MR_Fighter1')]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def profiles():
    countries = {}
    for name in PROFILE_FILES:
        data = json.loads((HERE/name).read_text(encoding='utf-8-sig'))
        assert data['project'] == PROJECT and data['cutoff'] == '1970-01-01', name
        for tag, row in data['countries'].items():
            assert tag not in countries, f'Duplicate profile: {tag}'
            countries[tag] = dict(row, profile_source=name)
    return countries


def selections(row, techs):
    groups = {key:set() for key in ('common','nsb','legacy','bba','non_bba','got','non_got')}
    domains = row['domains']
    requested = {tech for domain, chain in CHAINS.items() for year,tech in chain if domains.get(domain,0) >= year}
    requested.update(row.get('add_techs',[]))
    requested.difference_update(row.get('remove_techs',[]))
    # Provide older equipment components, not every 1965 composite/computer/ATGM module.
    if domains.get('armor',0) >= 1940:
        requested.add('mdcw_ww2_tank_ammunition_1940')
    if domains.get('armor',0) >= 1943:
        requested.add('mdcw_ww2_tank_ammunition_1943')
    if domains.get('armor',0) >= 1965:
        requested.update(('diesel_engine_tech','medium_gun_tech','small_medium_gun_tech'))
    if domains.get('naval_submarine',0):
        requested.update(('tech_naval_systems_engineering','tech_early_naval_weapon_systems'))
    for key in sorted(requested):
        assert key in techs, f"Unknown technology {key} in {row['name']}"
        record = techs[key]
        assert record['year'] is None or record['year'] <= 1969 or key in row.get('dated_exceptions',{}), f"Post-cutoff technology {key} in {row['name']}"
        folders = record['folders']
        if key in PAIRS:
            groups['nsb'].add(key); groups['legacy'].add(PAIRS[key])
        elif key + '_non_got' in techs:
            groups['got'].add(key); groups['non_got'].add(key+'_non_got')
        elif 'cruise_missiles_folder' in folders:
            groups['got'].add(key)
        elif 'missile_non_got_folder' in folders:
            groups['non_got'].add(key)
        elif folders == ['nsb_armour_folder'] or 'No Step Back' in json.dumps(record['allow_branch']):
            # Explicit NOT NoStepBack records without a mirrored ID are legacy-only.
            groups['legacy' if any(x[0]=='NOT' for x in record['allow_branch']) else 'nsb'].add(key)
        elif folders == ['armour_folder']:
            groups['legacy'].add(key)
        elif folders == ['bba_aircraft_folder']:
            groups['bba'].add(key)
        elif 'By Blood Alone' in json.dumps(record['allow_branch']):
            groups['non_bba' if any(x[0]=='NOT' for x in record['allow_branch']) else 'bba'].add(key)
        elif folders == ['fixed_wing_folder'] or folders == ['bomber_folder']:
            groups['non_bba'].add(key)
        else:
            groups['common'].add(key)
    # The NSB post-war APC hull is included in the tank hull node. Legacy APCs
    # need their separate equipment family; IFVs require an explicit country grant.
    if domains.get('armor',0)>=1965:groups['legacy'].add('APC_1')
    elif domains.get('armor',0)>=1960:groups['legacy'].update(('Early_APC','mdcw_tracked_apc_1960_legacy'))
    elif domains.get('armor',0)>=1945:groups['legacy'].add('Early_APC')
    # BBA airframe sizes do not exist in the legacy tree. Map only the evidenced
    # light combat family; strike/strategic/carrier roles remain explicit grants.
    light = domains.get('jet_light',0)
    for year,key in LEGACY_AIR:
        if light>=year:groups['non_bba'].add(key)
    if domains.get('jet_medium',0)>=1950:
        groups['non_bba'].add('early_bomber')
    if domains.get('jet_medium',0)>=1960:
        groups['non_bba'].add('MR_Fighter1')
    if 'gen_3_large' in requested:groups['non_bba'].add('strategic_bomber1')
    return {key:sorted(value - set(row.get('remove_techs',[]))) for key,value in groups.items()}


def technology_order(keys,techs):
    selected=set(keys);parents={key:set(techs[key].get('dependencies',[]))&selected for key in selected}
    for parent in selected:
        for child in techs[parent].get('paths',[]):
            if child in selected:parents[child].add(parent)
    ordered=[]
    while parents:
        ready=sorted((key for key,needed in parents.items() if not needed),key=lambda key:(techs[key]['year'] or 0,key))
        assert ready,('Cyclic starting technology predecessors',sorted(parents))
        ordered.extend(ready)
        for key in ready:del parents[key]
        for needed in parents.values():needed.difference_update(ready)
    return ordered


def technology_block(keys, depth,techs):
    if not keys:return []
    tab='\t'*depth
    return [tab+'set_technology = {',tab+'\tpopup = no',*[tab+'\t'+key+' = 1' for key in technology_order(keys,techs)],tab+'}']


def full_selections(row,techs):
    from prerequisites import complete
    return complete(selections(row,techs),techs,lambda key:selections({'name':row['name'],'domains':{},'add_techs':[key]},techs))


def history_block(row,techs):
    groups=full_selections(row,techs)
    lines=['\t'+BEGIN,'\tif = {','\t\tlimit = { IMP_is_1970_scenario = yes }','\t\tset_country_flag = '+FLAG,
           '\t\tset_country_flag = mdcw_1970_infantry_research_applied','\t\tset_country_flag = mdcw_1970_air_research_applied']
    owners={key:group for group,ids in groups.items() for key in ids}
    assert len(owners)==sum(map(len,groups.values())),'Duplicate technology across active routing groups'
    branches={'nsb':('No Step Back',True),'legacy':('No Step Back',False),
              'bba':('By Blood Alone',True),'non_bba':('By Blood Alone',False),
              'got':('Gotterdammerung',True),'non_got':('Gotterdammerung',False)}
    # Order the complete native graph, not each DLC branch in isolation:
    # a common static family can have a predecessor in a legacy-only branch.
    for group,sequence in itertools.groupby(technology_order(owners,techs),key=owners.get):
        ids=list(sequence)
        if group=='common':lines+=technology_block(ids,2,techs)
        else:
            dlc,positive=branches[group];condition='has_dlc = "'+dlc+'"'
            if not positive:condition='NOT = { '+condition+' }'
            lines+=['\t\tif = {','\t\t\tlimit = { '+condition+' }']+technology_block(ids,3,techs)+['\t\t}']
    lines+=['\t}','\t'+END]
    return '\n'.join(lines)+'\n',groups


TOKEN=re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|[^\s{}#"]+')


def date_span(source):
    match=re.search(r'(?m)^1970\.1\.1\s*=\s*\{',source)
    if not match:return None
    opening=source.index('{',match.start());depth=0
    for token in TOKEN.finditer(source,opening):
        if token[0]=='{':depth+=1
        elif token[0]=='}':
            depth-=1
            if depth==0:return opening,token.start()
    raise AssertionError('Unclosed1970history')


def strip_our_block(source):
    return re.sub(r'(?m)^\t'+re.escape(BEGIN)+r'\n.*?^\t'+re.escape(END)+r'\n','',source,flags=re.S)


def render_history(source,block,variant_block=''):
    import variants
    source=variants.strip_block(strip_our_block(source.replace('\r\n','\n')))
    if not source.startswith('# IMPERIA COLD WAR — '):
        source=FEATURE+'\n'+source
    span=date_span(source)
    if span:
        opening,closing=span
        # First within the dated block: old compatibility initializers see the
        # per-country applied flags and cannot add their former global packages.
        return source[:opening+1]+'\n'+block+variant_block+source[opening+1:].lstrip('\n')
    # Three regional release tags have only undated initialization. A dedicated
    # dated block adds research without rewriting their political setup.
    return source.rstrip()+'\n\n1970.1.1 = {\n'+block+variant_block+'}\n'


def compatibility_effects():
    output={}
    for name,effect,oldflag in [
        ('mdcw_1970_air_research_effects.txt','mdcw_apply_1970_air_research','mdcw_1970_air_research_applied'),
        ('mdcw_1970_infantry_research_effects.txt','mdcw_apply_1970_infantry_research','mdcw_1970_infantry_research_applied')]:
        p=ROOT/'common/scripted_effects'/name
        s=p.read_text(encoding='utf-8-sig').replace('\r\n','\n')
        start=s.index(effect+' = {');end=s.find('\n}\n',start)+3
        assert end>start
        section=s[start:end]
        guard='NOT = { has_country_flag = '+FLAG+' }'
        if guard not in section:
            anchor='NOT = { has_country_flag = '+oldflag+' }'
            assert section.count(anchor)==1
            section=section.replace(anchor,anchor+' '+guard,1)
            s=s[:start]+section+s[end:]
        marker='# IMPERIA COLD WAR — January 1970 research compatibility and retained later-start inheritance.'
        if not s.startswith(marker+'\n'):s=marker+'\n'+s
        output[p]=s
    return output


def outputs():
    import variants
    data=profiles();techs,duplicates=catalogue();assert not duplicates
    files={p.stem[:3]:p for p in (ROOT/'history/countries').glob('*.txt')}
    assert set(data)==set(files),f"Country coverage mismatch missing={sorted(set(files)-set(data))} extra={sorted(set(data)-set(files))}"
    base_groups={tag:full_selections(row,techs) for tag,row in data.items()}
    designs,assignments,support,bundles,synthetic=variants.plan(data,techs,base_groups)
    techs.update(synthetic)
    result={};manifest={}
    for tag,p in sorted(files.items()):
        source=p.read_text(encoding='utf-8-sig')
        row=dict(data[tag]);row['add_techs']=sorted(set(row.get('add_techs',[]))|set(support[tag]['research_additions'])|set(support[tag]['component_bundles'].values()))
        block,groups=history_block(row,techs)
        text=render_history(source,block,variants.render_country(tag,designs,assignments))
        parse(text)
        result[p]=text
        requested=selections(row,techs)
        completed={group:sorted(set(ids)-set(requested[group])) for group,ids in groups.items()}
        manifest[tag]={**data[tag],'history_file':p.relative_to(ROOT).as_posix(),'technology_groups':groups,'prerequisite_completion':completed,'variant_support':support[tag],'output_sha256':sha(text.encode('utf-8'))}
    result.update(compatibility_effects())
    result[variants.SUPPORT_PATH]=variants.render_support(bundles)
    return result,manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    result,manifest=outputs()
    if args.apply:
        baseline=json.loads((HERE/'before_hashes.json').read_text(encoding='utf-8'))
        assert Path(baseline['archive']).is_file(),'Pre-change archive missing'
        for p,text in result.items():
            raw=text.encode('utf-8')
            if p.exists() and p.read_bytes()==raw:continue
            temporary=p.with_name(p.name+'.'+uuid.uuid4().hex+'.icw-tmp')
            assert temporary.resolve().is_relative_to(ROOT.resolve())
            temporary.write_bytes(raw)
            os.replace(temporary,p)
    elif args.check:
        assert all(p.read_bytes()==s.encode('utf-8') for p,s in result.items()),'Generated history differs'
    (HERE/'country_manifest.json').write_text(json.dumps({'project':PROJECT,'cutoff':'1970-01-01','countries':manifest},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'project':PROJECT,'countries':len(manifest),'outputs':len(result),'mode':'apply' if args.apply else 'check' if args.check else 'preview'}))


if __name__=='__main__':main()
