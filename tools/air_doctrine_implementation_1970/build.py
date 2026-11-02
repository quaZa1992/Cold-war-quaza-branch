# IMPERIA COLD WAR — Approved Air Command expansion and native MD integration.
"""Emit the approved content from immutable design and pre-integration sources."""
from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools/air_doctrine_design_1970'))
sys.path.insert(0, str(ROOT / 'tools/multiplayer_quality'))
from design import GRANDS, SUBS, OLD_DEBUFF_DELTAS, POSITIVE_FINAL_TARGETS, FIGHTERS, STRIKERS
from audit import parse
from texts import NEW, OLD, REWARD_DESCRIPTIONS, STAGES

MARKER = '# IMPERIA COLD WAR — Air Command doctrine expansion and balance.'
OLD_GRAND = 'common/doctrines/grand_doctrines/air_doctrine.txt'
OLD_SUB = 'common/doctrines/subdoctrines/air/air.txt'
TRACK = 'common/doctrines/tracks/air.txt'
NEW_GRAND = 'common/doctrines/grand_doctrines/mdcw_air_doctrines.txt'
NEW_SUB = 'common/doctrines/subdoctrines/air/mdcw_air_doctrines.txt'
LOC = 'localisation/english/replace/mdcw_air_doctrines_l_english.yml'
GFX = 'interface/mdcw_air_doctrines.gfx'
TECH = 'common/technologies/mdcw_air_reconnaissance_rpvs.txt'
EQUIPMENT = 'common/units/equipment/mdcw_air_reconnaissance_rpvs.txt'
MIGRATION = 'common/scripted_effects/mdcw_air_doctrine_migration.txt'
ON_ACTION = 'common/on_actions/mdcw_air_doctrine_migration.txt'
ENUM = 'common/script_enums.txt'
GUI = 'interface/countrytechtreeview.gui'
UNITS = 'common/units/MD_air_units.txt'
META = {'folder','track','name','description','icon','xp_cost','xp_type','available','visible','ai_will_do','tracks','milestones','rewards','mastery','effect','instant'}


def get(rows, key, default=None):
    return next((v for k, _, v in rows if k == key), default)


def set_value(rows, key, value):
    for i, (k, op, old) in enumerate(rows):
        if k == key:
            rows[i] = (key, op, value)
            return
    rows.append((key, '=', value))


def effects(body):
    return [body, *[v for _, _, v in get(body, 'rewards', get(body, 'milestones', []))]]


def number(value):
    if isinstance(value,str) and re.fullmatch(r'[+-]?\.\d+',value):
        value=Decimal(value)
    if isinstance(value, (Decimal, float)):
        return format(Decimal(str(value)), 'f').rstrip('0').rstrip('.') if '.' in format(Decimal(str(value)), 'f') else str(value)
    return str(value)


def emit(rows, depth=0):
    output=[]
    prefix='\t'*depth
    for key, op, value in rows:
        if isinstance(value, list):
            opening='{' if key=='_anonymous' else key+' '+op+' {'
            output.extend([prefix+opening,*emit(value,depth+1),prefix+'}'])
        elif key in {'_bare','_anonymous'}:
            output.append(prefix+number(value))
        else:
            output.append(prefix+key+' '+op+' '+number(value))
    return output


def script(rows, notice=''):
    return MARKER+'\n'+notice+'\n'.join(emit(rows))+'\n'


def from_flat(values):
    result=[]
    for path,value in values.items():
        put(result,path,value)
    return result


def put(rows, path, value, additive=False):
    keys=path.split('.')
    current=rows
    for key in keys[:-1]:
        nested=get(current,key)
        if nested is None:
            nested=[]
            current.append((key,'=',nested))
        assert isinstance(nested,list), path
        current=nested
    key=keys[-1]
    if additive:
        value=Decimal(str(get(current,key,'0')))+Decimal(str(value))
    set_value(current,key,value)
    if keys[0]=='equipment_bonus':
        gear=get(get(rows,'equipment_bonus'),keys[1])
        set_value(gear,'instant','yes')


def remove_key(rows, wanted):
    for i in reversed(range(len(rows))):
        key,op,value=rows[i]
        if key==wanted:
            rows.pop(i)
        elif isinstance(value,list):
            remove_key(value,wanted)


def leaf_refs(rows, path):
    keys=path.split('.')
    current=rows
    for key in keys[:-1]:
        current=get(current,key)
        if not isinstance(current,list): return []
    return [(current,i) for i,(k,_,v) in enumerate(current) if k==keys[-1] and not isinstance(v,list)]


def retune(body, path, target):
    refs=[ref for stage in effects(body) for ref in leaf_refs(stage,path)]
    assert refs, 'No contribution for '+path
    total=sum((Decimal(str(rows[i][2])) for rows,i in refs),Decimal(0))
    assert total != 0, path
    target=Decimal(str(target))
    assigned=Decimal(0)
    for index,(rows,i) in enumerate(refs):
        key,op,value=rows[i]
        amount=(Decimal(str(value))*target/total).quantize(Decimal('.00001'),rounding=ROUND_HALF_UP) if index<len(refs)-1 else target-assigned
        assigned+=amount
        rows[i]=(key,op,amount)


def role_coverage(body, ident):
    for stage in effects(body):
        if ident in {'bvr_combat_doctrine','wvr_dogfighting_doctrine'}:
            exemplar=get(stage,'category_light_fighter')
            if exemplar is not None:
                for scope in FIGHTERS:
                    if get(stage,scope) is None:
                        stage.append((scope,'=',deepcopy(exemplar)))
        broad=get(stage,'category_fighter')
        if broad is not None:
            remove_key(stage,'category_fighter')
            for scope in FIGHTERS:
                assert get(stage,scope) is None
                stage.append((scope,'=',deepcopy(broad)))
        if ident in {'air_battlefield_support','integrated_air_warfare','cas_aircraft_operations'}:
            cas=get(stage,'category_CAS')
            if cas is not None and get(stage,'gunship') is None:
                stage.append(('gunship','=',deepcopy(cas)))


def gates(ident):
    if ident in {'mdcw_reconnaissance_rpv_operations','mdcw_decoy_rpv_operations'}:
        return [('OR','=',[('has_tech','=','mdcw_rpv_1964'),('has_tech','=','mdcw_rpv_1978'),('has_tech','=','drone_1'),('has_tech','=','drone_2')])]
    if ident in {'autonomous_air_operations','male_ucav_operations','ucas_carrier_strike'}:
        result=[('has_tech','=','drone_2')]
        if ident=='ucas_carrier_strike':
            result.append(('check_variable','=',[('num_ships_with_type@carrier','>','0')]))
        return result
    if ident=='drone_designs': return [('has_tech','=','drone_1')]
    if ident=='loitering_munitions_doctrine': return [('has_tech','=','suicide_drone_1')]
    if ident=='drone_swarm_integration': return [('has_tech','=','drone_2'),('has_tech','=','suicide_drone_2')]
    if ident in {'stealth_aircraft_designs','stealth_fighter_doctrine'}:
        return [('OR','=',[('has_tech','=','stealth_tech_1'),('is_special_project_completed','=','sp:sp_stealth_technology')])]
    return []


def integration_baseline():
    return json.loads((HERE/'integration_baselines.json').read_text(encoding='utf-8'))


def actual_fighter_roles(rows):
    """MD also tags a future mothership as Strike Fighter. Use actual units."""
    result=[]
    for key,op,value in rows:
        if key=='category_Strike_fighter':
            result.extend((unit,op,deepcopy(value)) for unit in ('light_strike','cv_light_strike'))
        else:
            result.append((key,op,actual_fighter_roles(value) if isinstance(value,list) else value))
    return result


def uav_category_integration():
    source=(ROOT/UNITS).read_text(encoding='utf-8-sig')
    header='# IMPERIA COLD WAR — Complete UAV doctrine category integration; native MD units retained.\n'
    source=source.removeprefix(header)
    source=re.sub(r'\n\s*# IMPERIA COLD WAR — Expendable UAVs share actual UAV doctrine effects and mastery\.\n', '\n',source)
    source=source.replace('categories = { category_cas category_Air_UAV }','categories = { category_cas }')
    start=source.index('kamikaze_drone = {')
    tail=source[start:]
    assert tail.count('categories = { category_cas }')==1
    tail=tail.replace('categories = { category_cas }', '# IMPERIA COLD WAR — Expendable UAVs share actual UAV doctrine effects and mastery.\n\t\tcategories = { category_cas category_Air_UAV }',1)
    return header+source[:start]+tail


def bind_legacy_rewards(body,ident):
    """Inline legacy idea rewards so native doctrine replacement cleans them up."""
    ideas=integration_baseline()['native_ideas']
    for stage in effects(body):
        effect=get(stage,'effect')
        if effect is None: continue
        idea=get(effect,'add_ideas')
        assert idea in ideas, (ident,idea)
        remove_key(stage,'effect')
        for key,op,value in ideas[idea]:
            if key=='equipment_bonus': stage.append((key,op,deepcopy(value)))
            if key=='modifier': stage.extend(deepcopy(value))
        if idea=='stealth_aircraft_design_hidden_spirit':
            for frame,_,bonus in get(ideas[idea],'equipment_bonus'):
                # Preserve the original production reward while retaining the
                # approved +15% net cost at full mastery on these six frames.
                put(body,'equipment_bonus.'+frame+'.build_cost_ic','.15',True)
    # Removing the misleading static-AA stat must not leave paid empty rewards.
    rewards=get(body,'rewards',[])
    if ident=='stealth_aircraft_designs':
        for frame,_,bonus in get(ideas['stealth_aircraft_design_hidden_spirit'],'equipment_bonus'):
            path='equipment_bonus.'+frame+'.air_defence'
            put(body,path,'-.0125',True)
            put(get(rewards,'reduced_rcs_design'),path,'.0125')
    if ident=='electronic_warfare_designs':
        donor=get(rewards,'electronic_countermeasures')
        for frame,_,_ in get(donor,'equipment_bonus'):
            path='equipment_bonus.'+frame+'.air_defence'
            put(donor,path,'-.01',True)
            put(get(rewards,'sead_mission_integration'),path,'.01')
    if ident=='heavy_gunships':
        put(get(rewards,'high_intensity_gunship_ops'),'gunship.air_defence','-.10',True)
        put(get(rewards,'enhanced_defensive_measures'),'gunship.air_defence','.10')
    if ident=='cas_aircraft_operations':
        for scope in ('category_CAS','gunship'):
            path=scope+'.air_defence'
            put(get(rewards,'expanded_combat_tactics'),path,'-.02',True)
            put(get(rewards,'jsead'),path,'.02')


def legacy_trees(baseline):
    grand=parse(baseline['sources'][OLD_GRAND]['text'])
    subs=parse(baseline['sources'][OLD_SUB]['text'])
    for ident,_,body in [*grand,*subs]:
        remove_key(body,'tech_air_damage_factor')
        role_coverage(body,ident)
        if ident=='local_airspace_defense':
            stages=get(body,'milestones')
            stages[0]=('_anonymous','=',[('air_interception_detect_factor','=',Decimal('.10'))])
        if ident=='sead_dead_operations':
            for stage in (body,get(get(body,'rewards'),'anti_radiation_missiles')):
                for key,value in {scope+'.air_defence':'.05' for scope in STRIKERS}.items():
                    put(stage,key,value,True)
        for path,value in POSITIVE_FINAL_TARGETS.get(ident,{}).items():
            retune(body,path,value)
        for path,value in OLD_DEBUFF_DELTAS[ident].items():
            put(body,path,value,True)
            if ident=='cas_aircraft_operations' and path.startswith('category_CAS.'):
                put(body,path.replace('category_CAS.','gunship.'),value,True)
        bind_legacy_rewards(body,ident)
        availability=get(body,'available')
        for key,_,value in availability:
            if key=='if':
                # The actual 1970 Japan tree replaces the modern Article 9 committee.
                # Constitutional national modifiers remain in their owning country system.
                limit=get(value,'limit')
                limit.append(('NOT','=',[('IMP_is_1970_scenario','=','yes')]))
        availability.extend(gates(ident))
        if get(body,'track') is not None:
            set_value(get(body,'mastery'),'multiplier','6')
        # Activation modifiers precede progression in native MD presentation.
        body.sort(key=lambda row: row[0] in {'rewards','milestones','mastery'})
    return grand,subs


def new_tree(item):
    grand=item['track']=='grand'
    prefix='GRAND_DOCTRINE_' if grand else 'SUBDOCTRINE_'
    loc=prefix+item['id'].upper()
    body=[('folder' if grand else 'track','=','air' if grand else item['track']),
          ('name','=',loc),('description','=',loc+'_DESC'),('icon','=','GFX_doctrine_'+item['id']),
          ('xp_cost','=','100' if grand else '75'),('xp_type','=','air')]
    available=[('always','=','yes')] if grand else [('NOT','=',[('has_doctrine','=',item['id'])])]
    available.extend(gates(item['id']))
    body.append(('available','=',available))
    countries={'mdcw_dispersed_air_defence':['SWE','FIN','NRY'], 'mdcw_selective_air_denial':['FIN','VIE'],
               'mdcw_offensive_counter_air':['ISR'], 'mdcw_maritime_air_denial':['ARG','NRY'],
               'mdcw_counterinsurgency_air_support':['POR','ZIM']} .get(item['id'],[])
    ai=[('base','=','1')]
    if countries:
        ai.append(('modifier','=',[('add','=','15'),('OR','=',[('original_tag','=',tag) for tag in countries])]))
    body.append(('ai_will_do','=',ai))
    if grand: body.append(('tracks','=',[('_bare','=',t) for t in item['tracks']]))
    body.extend(from_flat(item['activation']))
    rewards=[]
    for index,stage in enumerate(item['progression'],1):
        rewards.append(('_anonymous' if grand else 'stage_'+str(index),'=',from_flat(stage['effects'])))
    body.append(('milestones' if grand else 'rewards','=',rewards))
    if not grand: body.append(('mastery','=',[('multiplier','=','6')]))
    return item['id'],'=',body


def loc_line(key,text):
    return ' '+key+':0 '+json.dumps(text,ensure_ascii=False)


def outputs():
    baseline=json.loads((HERE/'baseline.json').read_text(encoding='utf-8'))
    for relative,digest in baseline['approval_sha256'].items():
        assert hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()==digest, 'Approved input changed: '+relative
    grands,subs=legacy_trees(baseline)
    grands,subs=actual_fighter_roles(grands),actual_fighter_roles(subs)
    track=parse(baseline['sources'][TRACK]['text'])
    drone=get(get(track,'drone_warfare'),'mastery')
    remove_key(drone,'equipment')
    drone.append(('categories','=',[('_bare','=','category_Air_UAV')]))
    result={
      OLD_GRAND:script(grands,'# Native MD doctrine identities retained; all activation trade-offs and marked integrations are project changes.\n'),
      OLD_SUB:script(subs,'# Native MD subdoctrine identities retained; approved balance and role integrations are project changes.\n# Original MD source contained Air Operations, Aircraft Design and role-section comments.\n'),
      TRACK:script(track,'# Native MD track geometry retained. Drone mastery now follows actual UAV categories.\n'),
      NEW_GRAND:script(actual_fighter_roles([new_tree(item) for item in GRANDS])),
      NEW_SUB:script(actual_fighter_roles([new_tree(item) for item in SUBS])),
    }
    loc=['l_english:',MARKER]
    for ident,_,body in [*grands,*subs]: loc.append(loc_line(get(body,'description'),OLD[ident]))
    for item in [*GRANDS,*SUBS]:
        key=('GRAND_DOCTRINE_' if item['track']=='grand' else 'SUBDOCTRINE_')+item['id'].upper()
        loc.extend([loc_line(key,item['name']),loc_line(key+'_DESC',NEW[item['id']])])
        if item['track']!='grand':
            for index,stage in enumerate(item['progression'],1):
                reward=item['id']+'_stage_'+str(index)
                loc.extend([loc_line(reward,stage['name']),
                            loc_line(reward+'_desc',STAGES[item['id']][index-1])])
    for key,text in REWARD_DESCRIPTIONS.items(): loc.append(loc_line(key,text))
    for year,name,desc in [
       (1964,'Early Reconnaissance RPVs','Ryan reconnaissance drones used in the 1960s provide a precedent for unarmed remotely piloted observation. This programme enables a reusable reconnaissance model; aircraft must still be produced and deployed.'),
       (1978,'Tactical Reconnaissance RPVs','Israeli developments in the late 1970s provide a precedent for small remotely piloted observation aircraft. Specialist control teams support reconnaissance without turning the aircraft into armed strike platforms.')]:
        loc.extend([loc_line('mdcw_rpv_'+str(year),name.replace('Reconnaissance','Recon')),loc_line('mdcw_rpv_'+str(year)+'_desc',desc),
                    loc_line('mdcw_recon_rpv_'+str(year)+'_model',name),loc_line('mdcw_recon_rpv_'+str(year)+'_model_desc',desc)])
    result[LOC]='\n'.join(loc)+'\n'
    gfx=[MARKER,'spriteTypes = {']
    for item in [*GRANDS,*SUBS]:
        gfx.extend(['\tSpriteType = {','\t\tname = "GFX_doctrine_'+item['id']+'"',
                    '\t\ttexturefile = "gfx/interface/doctrines/icons/air/mdcw_expansion/'+item['id']+'.dds"',
                    '\t\talwaystransparent = yes','\t}'])
    for year in (1964,1978):
        gfx.extend(['\tSpriteType = {',f'\t\tname = "GFX_mdcw_rpv_{year}_medium"',
                    '\t\ttexturefile = "gfx/interface/technologies/0_modules/plane_builder/support/tech_drone_1.dds"','\t}',
                    '\tSpriteType = {',f'\t\tname = "GFX_mdcw_recon_rpv_{year}_model_medium"',
                    '\t\ttexturefile = "gfx/interface/technologies/USA/AIR/UAV1.dds"','\t}'])
    gfx.append('}')
    result[GFX]='\n'.join(gfx)+'\n'
    result[TECH]=rpv_technology()
    result[EQUIPMENT]=rpv_equipment()
    enum=(ROOT/ENUM).read_text(encoding='utf-8-sig')
    header='# IMPERIA COLD WAR — Air Command equipment enum integration; native MD entries retained.\n'
    enum=enum.removeprefix(header)
    block='\t# IMPERIA COLD WAR — Historical reconnaissance RPV models.\n\tmdcw_recon_rpv_1964_model\n\tmdcw_recon_rpv_1978_model\n'
    enum=enum.replace(block,'')
    result[ENUM]=header+enum.replace('script_enum_equipment_bonus_type = {\n','script_enum_equipment_bonus_type = {\n'+block,1)
    result[GUI]=rpv_gui()
    result[UNITS]=uav_category_integration()
    result[MIGRATION]=MARKER+'''
mdcw_air_doctrine_migrate = {
 if = {
  limit = { NOT = { has_global_flag = mdcw_air_doctrine_migration_v1 } }
  every_country = {
'''+''.join('   if = { limit = { has_idea = '+idea+' } remove_ideas = '+idea+' }\n' for idea in integration_baseline()['native_ideas'])+'''
  }
  set_global_flag = mdcw_air_doctrine_migration_v1
 }
}
'''
    result[ON_ACTION]=MARKER+'''
on_actions = {
 on_startup = { effect = { if = { limit = { NOT = { has_global_flag = mdcw_air_doctrine_migration_v1 } } random_country = { mdcw_air_doctrine_migrate = yes } } } }
 on_daily = { effect = { if = { limit = { NOT = { has_global_flag = mdcw_air_doctrine_migration_v1 } } random_country = { mdcw_air_doctrine_migrate = yes } } } }
}
'''
    return result


def rpv_technology():
    entries=[]
    for year,cost,bba_y,fixed_y,successor in [(1964,'2',4,0,'mdcw_rpv_1978'),(1978,'2.5',9,3,None)]:
        body=[('enable_equipments','=',[('_bare','=',f'mdcw_recon_rpv_{year}_model')]),
              ('research_cost','=',cost),('start_year','=',str(year)),
              ('folder','=',[('name','=','bba_aircraft_folder'),('position','=',[('x','=','0'),('y','=',str(bba_y))])]),
              ('folder','=',[('name','=','fixed_wing_folder'),('position','=',[('x','=','0'),('y','=',str(fixed_y))])]),
              ('categories','=',[('_bare','=',x) for x in ['CAT_military','CAT_aircraft','CAT_air_drones','CAT_drones']]),
              ('ai_will_do','=',[('factor','=','1')])]
        if year==1964: body.append(('allow','=',[('OR','=',[('has_tech','=','early_airframe_designs'),('has_tech','=','early_fighter')])]))
        else: body.append(('allow','=',[('has_tech','=','mdcw_rpv_1964')]))
        if successor: body.append(('path','=',[('research_cost_coeff','=','1'),('leads_to_tech','=',successor)]))
        entries.append((f'mdcw_rpv_{year}','=',body))
    return script([('technologies','=',entries)])


def rpv_gui():
    source=(ROOT/GUI).read_text(encoding='utf-8-sig')
    header='# IMPERIA COLD WAR — Historical RPV research rows; native MD GUI retained.\n'
    source=source.removeprefix(header)
    source=re.sub(r'\n\s*# IMPERIA COLD WAR RPV ROW BEGIN\n.*?# IMPERIA COLD WAR RPV ROW END\n','\n',source,flags=re.S)
    for folder,x,y in [('bba_aircraft_folder',570,2120),('fixed_wing_folder',910,1400)]:
        needle='name = "'+folder+'"'
        start=source.index(needle)
        opening=source.rfind('{',0,start)
        depth=1;closing=opening+1
        # Native donor folder contains no braces in its quoted names/comments.
        while depth:
            if source[closing]=='{': depth+=1
            elif source[closing]=='}': depth-=1
            closing+=1
        block='\n\t\t\t# IMPERIA COLD WAR RPV ROW BEGIN\n'
        block+='\t\t\t# IMPERIA COLD WAR — Historical reconnaissance RPVs, separate native research row.\n'
        for year in (1964,1978):
            block+='\t\t\tgridboxtype = {\n\t\t\t\tname = "mdcw_rpv_'+str(year)+'_tree"\n'
            block+=f'\t\t\t\tposition = {{ x = {x} y = {y} }}\n'
            block+='\t\t\t\tsize = { width = 400 height = 1000 }\n\t\t\t\tslotsize = { width = 70 height = 70 }\n\t\t\t\tformat = "LEFT"\n\t\t\t}\n'
        block+='\t\t\t# IMPERIA COLD WAR RPV ROW END\n'
        source=source[:closing-1]+block+source[closing-1:]
    return header+source


def rpv_equipment():
    entries=[]
    for year,speed,radius,cost,fuel,defence in [(1964,600,900,80,1,15),(1978,180,600,60,.5,20)]:
        body=[('year','=',str(year)),('archetype','=','small_plane_suicide_airframe'),('priority','=','5' if year==1964 else '6'),
              ('allow_mission_type','=',[('_bare','=','recon'),('_bare','=','training')])]
        body.extend(from_flat(dict(maximum_speed=speed,air_range=radius,build_cost_ic=cost,fuel_consumption=fuel,
                                   air_defence=defence,air_agility=10,air_superiority=0,air_attack=0,air_ground_attack=0,
                                   air_bombing=0,naval_strike_attack=0,naval_strike_targetting=0,manpower=4,reliability=.8)))
        body.append(('resources','=',[('aluminium','=','1'),('rubber','=','1')]))
        entries.append((f'mdcw_recon_rpv_{year}_model','=',body))
    return script([('equipments','=',entries)])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    result=outputs()
    drift=[]
    for relative,text in result.items():
        path=ROOT/relative
        raw=text.encode('utf-8-sig' if path.suffix=='.yml' else 'utf-8')
        if args.check:
            if not path.is_file() or path.read_bytes()!=raw: drift.append(relative)
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(raw)
    print(json.dumps({'project':'IMPERIA COLD WAR','generator_drift':drift} if args.check else
                     {'project':'IMPERIA COLD WAR','written':list(result),'new_grands':5,'new_subdoctrines':14,'legacy_choices':45},indent=2))
    raise SystemExit(bool(drift))


if __name__=='__main__': main()
