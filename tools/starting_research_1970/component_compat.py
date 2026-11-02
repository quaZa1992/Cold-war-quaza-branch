# IMPERIA COLD WAR — Historically compatible early aircraft, tank and frigate modules.
"""Add narrow native module equivalents instead of fitting later hardware to old names."""
import argparse
import copy
import hashlib
import json
import os
import re
import sys
import zipfile
import uuid
from datetime import datetime,timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(ROOT/'tools/spain_1970_v2'))
from catalog import parse,first
from script_ast import emit

MARK='# IMPERIA COLD WAR — Historical January 1970 equipment component compatibility.'
CHANGES={
 'common/technologies/mdcw_historical_air_naval.txt':{'mdcw_early_airframes_1945':['module_mdcw_unguided_bombs_1945','module_mdcw_aircraft_machine_guns_1940','module_mdcw_aircraft_cannon_20mm','module_mdcw_aircraft_cannon_30mm','module_mdcw_mixed_aircraft_cannons_1945']},
 'common/technologies/naval_modules.txt':{'tech_naval_systems_engineering':['module_mdcw_light_steam_power_1945']},
 'common/technologies/mdcw_historical_land.txt':{'mdcw_postwar_medium_tank_1955_nsb':['module_mdcw_90mm_tank_gun_1945']},
 'common/technologies/NSB_artillery.txt':{'nsb_gun_technology_1':['module_mdcw_sp_gun_175mm','module_mdcw_sp_howitzer_203mm']},
}
FRAME_UNLOCKS={}

TOK=re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|[^\s{}#"]+')


def span(source,name,start=0):
    match=re.search(r'(?m)^\s*'+re.escape(name)+r'\s*=\s*\{',source[start:])
    assert match,name
    opening=source.index('{',start+match.start());depth=0
    for tok in TOK.finditer(source,opening):
        if tok[0]=='{':depth+=1
        elif tok[0]=='}':
            depth-=1
            if depth==0:return start+match.start(),opening,tok.start()
    raise AssertionError(name)


def modules():
    records={}
    for path in (ROOT/'common/units/equipment/modules').glob('*.txt'):
        for k,o,rows in parse(path.read_text(encoding='utf-8-sig')):
            if k=='equipment_modules':records.update({name:block for name,op,block in rows if isinstance(block,list)})
    bombs=copy.deepcopy(records['weap_ag_cas_hardpoint_1'])
    bombs=[item for item in bombs if item[0] not in {'can_convert_from'}]
    bombs=[(k,o,'"cwbm"' if k=='abbreviation' else v) for k,o,v in bombs]
    steam=copy.deepcopy(records['module_surface_oil_power'])
    steam=[(k,o,'module_light_surface_power_source_category' if k=='category' else v) for k,o,v in steam]
    gun=copy.deepcopy(records['tank_small_cannon'])
    gun=[item for item in gun if item[0]!='forbid_equipment_type_exact_match']
    gun=[(k,o,[('_bare','=','armor'),('_bare','=','anti_tank')] if k=='allow_equipment_type' else '"cw90"' if k=='abbreviation' else v) for k,o,v in gun]
    result=[('module_mdcw_unguided_bombs_1945','=',bombs),('module_mdcw_light_steam_power_1945','=',steam),('module_mdcw_90mm_tank_gun_1945','=',gun)]
    # Neutral historical names avoid inherited country aliases such as the
    # post1970 BK27 on an otherwise correctly fitted 1960s F104.
    for name,donor in [('module_mdcw_aircraft_machine_guns_1940','weap_multi_gun_1'),('module_mdcw_aircraft_cannon_20mm','weap_multi_gun_2'),('module_mdcw_aircraft_cannon_30mm','weap_multi_gun_2'),('module_mdcw_mixed_aircraft_cannons_1945','weap_multi_gun_2')]:
        result.append((name,'=',copy.deepcopy(records[donor])))
    for name in ('module_mdcw_sp_gun_175mm','module_mdcw_sp_howitzer_203mm'):
        result.append((name,'=',copy.deepcopy(records['art_med_gun_gen1'])))
    # The early eight-round trainable ASROC box launcher predates vertical
    # launchers. Reuse the native first ASW support category and balance tier,
    # with the correct weapon identity rather than a fictional mortar fit.
    result.append(('module_naval_mdcw_mk112_asroc','=',copy.deepcopy(records['module_anti_submarine_mortar'])))
    return result


def frames():
    existing=first(parse((ROOT/'common/units/equipment/mdcw_historical_air_naval_equipment.txt').read_text(encoding='utf-8-sig')),'equipments')
    records={k:v for k,o,v in existing}
    def fixed(original,changes):
        rows=[item for item in copy.deepcopy(records[original]) if item[0] not in changes]
        combined=rows+[(k,'=',v) for k,v in changes.items()]
        # Native equipment parsing needs its archetype/parent established
        # before interpreting mission lists and equipment-specific stats.
        first_keys=('year','archetype','parent','priority','allow_mission_type')
        return [item for key in first_keys for item in combined if item[0]==key]+[item for item in combined if item[0] not in first_keys]
    piston=fixed('mdcw_piston_fighter_1940_model',{
        'archetype':'medium_plane_cas_airframe','allow_mission_type':[('_bare','=','cas'),('_bare','=','attack_logistics')],
        'maximum_speed':'450','air_agility':'40','air_attack':'8','air_defence':'50','air_ground_attack':'6','air_bombing':'1','build_cost_ic':'150',
    })
    bomber=fixed('mdcw_early_jet_fighter_1950_model',{
        'archetype':'medium_plane_cas_airframe','allow_mission_type':[('_bare','=','cas'),('_bare','=','strategic_bomber'),('_bare','=','attack_logistics')],
        'maximum_speed':'900','air_range':'1500','air_agility':'25','air_attack':'8','air_defence':'65','air_ground_attack':'14','air_bombing':'12','build_cost_ic':'300','fuel_consumption':'6',
    })
    utility=[('year','=','1955'),('archetype','=','heavy_tank_amphibious_chassis'),('parent','=','heavy_tank_amphibious_chassis_0'),('module_slots','=','inherit'),('priority','=','4'),('abbreviation','=','"cu55"'),('derived_variant_name','=','mdcw_utility_helicopter_1955_modular')]
    carrier=[(k,o,'cv_medium_plane_cas_airframe' if k=='archetype' else '1200' if k=='air_range' else v) for k,o,v in copy.deepcopy(bomber)]
    return [('mdcw_early_piston_attack_1940_model','=',piston),('mdcw_early_jet_bomber_1950_model','=',bomber),('mdcw_early_carrier_attack_1950_model','=',carrier)]


def outputs():
    result={ROOT/'common/units/equipment/modules/COLDWAR_1970_historical_components.txt':MARK+'\n'+emit([('equipment_modules','=',modules())])+'\n'}
    # Load after MD archetypes and the mdcw_historical donor equipment.
    result[ROOT/'common/units/equipment/zz_COLDWAR_1970_historical_design_frames.txt']=MARK+'\n'+emit([('equipments','=',frames())])+'\n'
    combined={}
    for relative,techs in CHANGES.items():
        for name,added in techs.items():combined.setdefault(relative,[]).append((name,'enable_equipment_modules',added))
    for relative,techs in FRAME_UNLOCKS.items():
        for name,added in techs.items():combined.setdefault(relative,[]).append((name,'enable_equipments',added))
    for relative,patches in combined.items():
        path=ROOT/relative;source=path.read_text(encoding='utf-8-sig').replace('\r\n','\n')
        for name,field,added in patches:
            begin,opening,end=span(source,name)
            body=source[opening+1:end]
            for module in added:
                if re.search(r'\b'+re.escape(module)+r'\b',body):continue
                if re.search(r'\b'+field+r'\s*=\s*\{',body):
                    a,b,c=span(body,field)
                    body=body[:c]+'\n\t\t\t'+module+'\n\t\t'+body[c:]
                else:body+='\n\t\t'+field+' = {\n\t\t\t'+module+'\n\t\t}\n\t'
            # Shared MD sources retain attribution and identify the precise
            # integration entries as well as carrying the file-start notice.
            for module in added:
                body=re.sub(r'\s*\b'+re.escape(module)+r'\b[ \t]*(?:# IMPERIA COLD WAR[^\n]*)?\s*',
                            '\n\t\t\t'+module+' # IMPERIA COLD WAR — Historical January 1970 component integration.\n\t\t',body)
            source=source[:opening+1]+body+source[end:]
        if not source.startswith(MARK+'\n'):source=MARK+'\n'+source
        result[path]=source
    result[ROOT/'localisation/english/COLDWAR_1970_historical_components_l_english.yml']='''l_english:
 # IMPERIA COLD WAR — Historical January 1970 equipment component compatibility.
 module_mdcw_unguided_bombs_1945: "Unguided Bomb Load"
 module_mdcw_unguided_bombs_1945_desc: "Conventional free-fall bombs carried on racks or in a bomb bay for tactical bombing and close air support."
 module_mdcw_light_steam_power_1945: "Light Steam Propulsion"
 module_mdcw_light_steam_power_1945_desc: "Oil-fired boilers and steam machinery for conventional frigates and escort vessels."
 module_mdcw_90mm_tank_gun_1945: "90 mm Tank Cannon"
 module_mdcw_90mm_tank_gun_1945_desc: "A conventional 90 mm cannon for late-war and early Cold War tanks, using manual loading and optical sights."
 module_mdcw_aircraft_machine_guns_1940: "Aircraft Machine Guns"
 module_mdcw_aircraft_machine_guns_1940_desc: "Fixed machine-gun armament for conventional piston and early jet aircraft."
 module_mdcw_aircraft_cannon_20mm: "20 mm Aircraft Cannon"
 module_mdcw_aircraft_cannon_20mm_desc: "Fixed 20 mm cannon armament for Cold War combat aircraft."
 module_mdcw_aircraft_cannon_30mm: "30 mm Aircraft Cannon"
 module_mdcw_aircraft_cannon_30mm_desc: "Fixed 30 mm cannon armament for Cold War combat aircraft."
 module_mdcw_mixed_aircraft_cannons_1945: "Mixed Aircraft Cannons"
 module_mdcw_mixed_aircraft_cannons_1945_desc: "A mixed-calibre cannon battery for early jet fighters."
 module_mdcw_sp_gun_175mm: "175 mm Heavy Gun"
 module_mdcw_sp_gun_175mm_desc: "A conventional long-barrelled heavy gun on a self-propelled carriage, using optical fire direction and standard artillery ammunition."
 module_mdcw_sp_howitzer_203mm: "203 mm Heavy Howitzer"
 module_mdcw_sp_howitzer_203mm_desc: "A conventional heavy howitzer on a self-propelled carriage, with manual ammunition handling and an open gun position."
 module_naval_mdcw_mk112_asroc: "Mk 112 ASROC Box Launcher"
 module_naval_mdcw_mk112_asroc_desc: "An eight-round trainable launcher for rocket-delivered anti-submarine torpedoes."
 mdcw_early_piston_attack_1940_model: "Early Piston Attack Aircraft"
 mdcw_early_piston_attack_1940_model_short: "Piston Attack Aircraft"
 mdcw_early_jet_bomber_1950_model: "Early Jet Bomber"
 mdcw_early_jet_bomber_1950_model_short: "Early Jet Bomber"
 mdcw_early_carrier_attack_1950_model: "Early Carrier Attack Aircraft"
 mdcw_early_carrier_attack_1950_model_short: "Early Carrier Attack Aircraft"
'''
    sprites=[('GFX_EMI_module_mdcw_unguided_bombs_1945','gfx/interface/technologies/0_modules/plane_builder/weapons/weapon_ag_gb_12.dds'),('GFX_SMI_module_mdcw_light_steam_power_1945','gfx/interface/technologies/0_modules/ship_builder/E1.dds'),('GFX_EMI_module_mdcw_90mm_tank_gun_1945','gfx/interface/technologies/0_modules/tank_builder/armament/tank_small_medium_cannon.dds')]
    for name in ('module_mdcw_aircraft_machine_guns_1940','module_mdcw_aircraft_cannon_20mm','module_mdcw_aircraft_cannon_30mm','module_mdcw_mixed_aircraft_cannons_1945'):
        texture='weapon_multi_hmg.dds' if name=='module_mdcw_aircraft_machine_guns_1940' else 'weapon_multi_cannon_1.dds'
        sprites.append(('GFX_EMI_'+name,'gfx/interface/technologies/0_modules/plane_builder/weapons/'+texture))
    for name in ('module_mdcw_sp_gun_175mm','module_mdcw_sp_howitzer_203mm'):
        sprites.append(('GFX_EMI_'+name,'gfx/interface/technologies/0_modules/arty_builder/120mm_cannons/120mm_cannon.dds'))
    sprites.append(('GFX_SMI_module_naval_mdcw_mk112_asroc','gfx/interface/technologies/0_modules/ship_builder/ASWMORTAR.dds'))
    gfx=MARK+'\nspriteTypes = {\n'+''.join('\tspriteType = { name = "'+key+'" textureFile = "'+texture+'" }\n' for key,texture in sprites)+'}\n'
    assert all((ROOT/texture).is_file() for key,texture in sprites)
    result[ROOT/'interface/COLDWAR_1970_historical_components.gfx']=gfx
    enum=ROOT/'common/script_enums.txt'
    enum_source=enum.read_text(encoding='utf-8-sig').replace('\r\n','\n')
    enum_marker='# IMPERIA COLD WAR — January 1970 equipment enum integration; existing MD registrations retained.'
    enum_source=re.sub(r'(?m)^[ \t]*mdcw_utility_helicopter_1955_modular[ \t]*\n','',enum_source)
    missing=[name for name,operator,rows in frames() if not re.search(r'(?m)^\s*'+re.escape(name)+r'\s*(?:#.*)?$',enum_source)]
    if missing:
        opening=re.search(r'script_enum_equipment_bonus_type\s*=\s*\{',enum_source).end()
        enum_source=enum_source[:opening]+'\n\t# IMPERIA COLD WAR — Historical January 1970 design frames.\n'+''.join('\t'+name+'\n' for name in missing)+enum_source[opening:]
    if not enum_source.startswith(enum_marker+'\n'):enum_source=enum_marker+'\n'+enum_source
    result[enum]=enum_source
    return result


def capture():
    record=HERE/'component_before_hashes.json'
    recorded=set()
    for previous in HERE.glob('component_before_hashes*.json'):
        recorded.update(json.loads(previous.read_text(encoding='utf-8'))['before_sha256'])
    pending=sorted((set(CHANGES)|set(FRAME_UNLOCKS)|{'common/script_enums.txt'})-recorded)
    if not pending:return
    if record.exists():record=HERE/('component_before_hashes_extra_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')+'.json')
    directory=Path('E:/MDColdWar_Backups/Codex_Test_Archives').resolve()
    directory.mkdir(parents=True,exist_ok=True)
    target=(directory/('starting_research_components_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')+'.zip')).resolve()
    assert target.is_relative_to(directory)
    hashes={}
    with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for relative in pending:
            raw=(ROOT/relative).read_bytes();z.writestr(relative,raw);hashes[relative]=hashlib.sha256(raw).hexdigest()
    record.write_text(json.dumps({'project':'IMPERIA COLD WAR','archive':str(target),'before_sha256':hashes},indent=2)+'\n',encoding='utf-8')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--apply',action='store_true');parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.apply:capture()
    retired=ROOT/'common/units/equipment/COLDWAR_1970_historical_design_frames.txt'
    if args.apply and retired.exists():
        previous=json.loads((HERE/'component_manifest.json').read_text(encoding='utf-8'))
        relative=retired.relative_to(ROOT).as_posix()
        assert retired.resolve().is_relative_to(ROOT.resolve()) and not retired.is_symlink() and not retired.is_junction()
        assert hashlib.sha256(retired.read_bytes()).hexdigest()==previous['outputs_sha256'][relative],'Retired generated frame was edited outside its generator'
        retired.unlink()
    elif args.check:assert not retired.exists(),'Retired early-loading frame file remains'
    result=outputs()
    for p,source in result.items():
        raw=source.encode('utf-8-sig' if p.suffix=='.yml' else 'utf-8')
        if args.apply:
            temporary=p.with_name(p.name+'.'+uuid.uuid4().hex+'.icw-tmp')
            assert temporary.resolve().is_relative_to(ROOT.resolve())
            temporary.write_bytes(raw)
            os.replace(temporary,p)
        elif args.check:assert p.read_bytes()==raw,p
        if p.suffix!='.yml':parse(source)
    if args.apply:
        donors=['common/units/equipment/modules/MD_plane_modules.txt','common/units/equipment/modules/MD_ship_modules.txt','common/units/equipment/modules/MD_tank_modules.txt','common/units/equipment/modules/MD_arty_modules.txt','common/units/equipment/mdcw_historical_air_naval_equipment.txt']
        report={'project':'IMPERIA COLD WAR','feature':'Historical equipment component compatibility','source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in donors},'outputs_sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in result},'modules':[name for name,op,body in modules()],'frames':[name for name,op,body in frames()]}
        (HERE/'component_manifest.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'project':'IMPERIA COLD WAR','outputs':len(result),'modules':len(modules()),'frames':len(frames()),'mode':'apply' if args.apply else 'check' if args.check else 'preview'}))


if __name__=='__main__':main()
