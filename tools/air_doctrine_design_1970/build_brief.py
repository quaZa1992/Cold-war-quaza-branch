# IMPERIA COLD WAR — Air Command concept inventory and arithmetic review.
"""Write a design brief and model evidence. Never write runtime mod content."""
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
import hashlib
import json
import re
import sys
from design import *

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools/multiplayer_quality'))
from audit import parse

INPUTS = ('common/doctrines/grand_doctrines/air_doctrine.txt', 'common/doctrines/subdoctrines/air/air.txt',
          'common/doctrines/tracks/air.txt', 'common/doctrines/folders/doctrine_folders.txt',
          'common/units/MD_air_units.txt', 'common/units/equipment/MD_plane_airframes.txt',
          'common/scripted_effects/00_money_system.txt', 'common/defines/MD_defines.lua')
META = {'folder','track','name','description','icon','xp_cost','xp_type','available','visible','ai_will_do','tracks','milestones','rewards','mastery','effect','enable_tactic','instant'}
BAD_HIGH = {'airforce_personnel_cost_multiplier_modifier','air_fuel_consumption_factor','air_accidents_factor','air_night_penalty','air_weather_penalty','build_cost_ic','air_wing_xp_loss_when_killed_factor'}
BAD_LOW = {'air_range_factor','air_strategic_bomber_bombing_factor','air_home_defence_factor','air_intercept_efficiency',
           'air_superiority_efficiency','air_escort_efficiency','air_training_xp_gain_factor','air_mission_xp_gain_factor',
           'air_cas_efficiency','air_attack_factor','air_mission_efficiency','air_ace_generation_chance_factor',
           'air_agility','air_defence','maximum_speed','air_range','air_ground_attack','air_bombing','air_attack','naval_strike_attack'}
LABELS = {
 'airforce_personnel_cost_multiplier_modifier': 'Air force personnel cost', 'air_fuel_consumption_factor':'Air fuel consumption',
 'air_accidents_factor':'Air accident chance', 'air_range_factor':'Air range', 'air_home_defence_factor':'Home air defence',
 'air_intercept_efficiency':'Interception mission efficiency', 'air_interception_detect_factor':'Interception detection',
 'air_superiority_efficiency':'Air-superiority mission efficiency', 'air_superiority_detect_factor':'Air-superiority detection',
 'air_escort_efficiency':'Escort mission efficiency', 'air_mission_efficiency':'Air mission efficiency',
 'air_training_xp_gain_factor':'Training XP gain', 'air_mission_xp_gain_factor':'Mission XP gain',
 'air_wing_xp_loss_when_killed_factor':'Wing XP loss when aircraft are lost', 'air_untrained_pilots_penalty_factor':'Untrained-pilot penalty',
 'air_ace_generation_chance_factor':'Ace generation chance', 'ace_effectiveness_factor':'Ace effectiveness',
 'repair_speed_air_base_factor':'Air-base repair speed', 'air_cas_efficiency':'CAS mission efficiency',
 'air_cas_present_factor':'Ground-support combat modifier', 'air_close_air_support_org_damage_factor':'CAS organisation damage',
 'ground_attack_factor':'CAS ground-attack modifier', 'air_bombing_targetting':'Bombing targeting',
 'air_strategic_bomber_bombing_factor':'Strategic bombing', 'air_attack_factor':'Air attack',
 'air_nav_efficiency':'Naval mission efficiency', 'naval_strike_targetting_factor':'Naval strike targeting',
 'naval_strike_attack_factor':'Naval strike attack', 'port_strike':'Port strike', 'air_weather_penalty':'Bad-weather penalty',
 'paradrop_organization_factor':'Organisation after paradropping',
 'air_agility':'Agility', 'air_defence':'Air defence', 'maximum_speed':'Maximum speed', 'air_range':'Range',
 'air_ground_attack':'Ground attack', 'air_bombing':'Strategic-bombing stat', 'air_attack':'Air attack',
 'naval_strike_attack':'Naval strike attack', 'surface_detection':'Surface detection', 'sub_detection':'Sub detection',
 'fuel_consumption':'Fuel consumption', 'build_cost_ic':'Production IC cost',
}
TRACK_LABELS = {T:'Training and Operations',D:'Aircraft Design',H:'Heavy Aircraft',M:'Multirole Aircraft',S:'Strike Aircraft',F:'Fighter Aircraft',U:'Drone Warfare'}
OLD_REASON = {
 'local_airspace_defense':'Home-oriented basing and control sacrifice distant operations.',
 'strategic_destruction':'Long bomber campaigns consume fuel and divert interception resources.',
 'air_battlefield_support':'Tactical support commitments consume fuel and reduce air-superiority emphasis.',
 'air_supremacy':'Standing fighter effort uses fuel and diverts close-support capacity.',
 'autonomous_air_operations':'Specialist remote crews and qualification burden; modern content must be identified honestly.',
 'mixed_role_air_force':'Broad qualifications take longer and require more specialist staff.',
 'integrated_air_warfare':'Coordination, support crews and simultaneous missions consume resources.',
 'centralized_air_command':'Central control slows local learning and needs coordinating staff.',
 'detached_air_commands':'Independent commands duplicate fuel/support effort and coordinate escorts less efficiently.',
 'naval_air_command':'Maritime qualifications and flying priorities reduce close-support emphasis.',
 'multirole_aircraft_designs':'Compromise layouts and role equipment reduce peak agility.',
 'dedicated_aircraft_designs':'Different specialised fleets need separate personnel skills.',
 'heavy_aircraft_designs':'Large designs cost more to produce and manoeuvre less readily.',
 'drone_designs':'Cheap unmanned designs accept lower protection.',
 'stealth_aircraft_designs':'Low-observable manufacturing and configurations consume production resources and range.',
 'electronic_warfare_designs':'Specialist crews and equipment compete with offensive weapon carriage.',
 'modular_airframe_designs':'Common interfaces and adaptable configurations sacrifice peak attack performance.',
 'strategic_bomber_command':'Heavy loads and long missions impose fuel demand and manoeuvre limits.',
 'naval_bombers':'Patrol equipment and endurance configurations reduce agility.',
 'heavy_gunships':'Slow gunships remain vulnerable in contested airspace, even with crew training.',
 'airborne_early_warning':'Large support aircraft and specialist controllers consume fuel and personnel.',
 'strategic_airlift':'Transport schedules require fuel and a substantial support establishment.',
 'aerial_refueling_operations':'Tanker sorties extend reach but require extra fuel and support crews.',
 'mixed_multirole_aircraft':'Multiple role qualifications require staff and slower training progression.',
 'strike_multirole_aircraft':'Attack loads reduce manoeuvring performance.',
 'multirole_air_operations':'Complex role packages trade range and staff effort for flexibility.',
 'air_dominance_multirole':'Air-combat priority reduces ground-attack and bombing emphasis.',
 'carrier_multirole_operations':'Deck and mission qualifications slow training and cost more.',
 'cas_aircraft_operations':'Ground-attack configurations trade air combat and reach for close support.',
 'naval_strike_operations':'Maritime navigation/weapon commitments cost specialist staff and agility.',
 'munitions_and_support':'Specialist arming and support arrangements cost staff and slow mission preparation.',
 'sead_dead_operations':'Threat-focused loads divert ground firepower and need specialist staff. The old static-AA modifier needs separate correction.',
 'deep_interdiction_doctrine':'Deep targets consume fuel and divert aircraft from immediate close support.',
 'air_interdiction_campaign':'Sustained sorties consume fuel and planning staff.',
 'light_fighters':'Lightweight designs accept limited reach and protection.',
 'air_superiority_fighters':'Specialised fighter airframes cost more to produce.',
 'bvr_combat_doctrine':'Missile/radar-centred configurations and qualifications trade agility and staff expense.',
 'wvr_dogfighting_doctrine':'Close-combat preparation costs qualification time and favours shorter-range profiles.',
 'stealth_fighter_doctrine':'Concealed configurations prioritise survival over weapon employment and require specialist staff.',
 'dedicated_interceptor_doctrine':'Short defensive commitments sacrifice escort and continuous superiority patrols.',
 'male_ucav_operations':'Long-endurance unmanned systems remain vulnerable and require control teams. This is a later capability.',
 'ucas_carrier_strike':'Carrier UAV qualification and control impose training and staffing demands. This is post-Cold-War content.',
 'loitering_munitions_doctrine':'Compact expendable systems trade range and control staff for the chosen strike role.',
 'counter_drone_operations':'Point-defence staffing and local coverage divert effort from distant escort. Existing benefits are not drone-exclusive.',
 'drone_swarm_integration':'Large formations accept vulnerable platforms and more difficult mission coordination. This is post-Cold-War content.',
}


def flat(rows, prefix=''):
    out = defaultdict(Decimal)
    for key, _, value in rows:
        if key in META:
            continue
        if isinstance(value,list):
            for name, amount in flat(value,prefix+key+'.').items():
                out[name] += amount
        else:
            try: out[prefix+key] += Decimal(value)
            except Exception: pass
    return dict(out)


def add(left, right):
    result=left.copy()
    for k,v in right.items(): result[k]=result.get(k,Decimal(0))+Decimal(str(v))
    return result


def bad(key, value):
    leaf=key.rsplit('.',1)[-1]
    return (leaf in BAD_HIGH and value>0) or (leaf in BAD_LOW and value<0)


def render(values):
    groups=defaultdict(list)
    for key,value in values.items():
        parts=key.split('.')
        label=LABELS.get(parts[-1],parts[-1])
        amount=Decimal(str(value))*100
        number=f'{amount:+f}'.rstrip('0').rstrip('.') if '.' in f'{amount:+f}' else f'{amount:+f}'
        groups[(label,number)].append('.'.join(parts[:-1]))
    lines=[]
    for (label,number), scopes in groups.items():
        if scopes==['']: prefix=''
        elif set(scopes)==set(FIGHTERS): prefix='Eligible fighter roles: '
        elif set(scopes)==set(STRIKERS): prefix='Multirole and strike roles: '
        elif set(scopes)==set(ATTACK): prefix='CAS and gunships: '
        elif all(s.startswith('equipment_bonus.') for s in scopes): prefix=f'{len(scopes)} specified airframe families: '
        else: prefix=', '.join(scopes)+': '
        lines.append(prefix+label+' '+number+'%')
    return '; '.join(lines) or 'None'


def main():
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in INPUTS}
    loc={}
    for path in (ROOT/'localisation/english').rglob('*.yml'):
        for key,value in re.findall(r'^\s*([A-Za-z0-9_]+):\d*\s+"((?:\\.|[^"\\])*)"',path.read_text(encoding='utf-8-sig',errors='replace'),re.M):
            loc[key]=value
    inventory=[]
    checks=[]
    def check(name,condition): checks.append({'check':name,'passed':bool(condition)})
    for relative in INPUTS[:2]:
        for ident,_,body in parse((ROOT/relative).read_text(encoding='utf-8-sig')):
            base=flat(body)
            rewards=next(v for k,_,v in body if k in {'milestones','rewards'})
            final=base.copy()
            for _,_,effects in rewards: final=add(final,flat(effects))
            delta=OLD_DEBUFF_DELTAS[ident]
            balanced=final.copy()
            balanced.update({k:Decimal(str(v)) for k,v in POSITIVE_FINAL_TARGETS.get(ident,{}).items()})
            if 'tech_air_damage_factor' in balanced:
                balanced['tech_air_damage_factor']=Decimal(0)
            if ident=='sead_dead_operations':
                balanced=add(balanced,scoped(STRIKERS,air_defence=.10))
            draft_final=add(balanced,delta)
            proposed=add(base,delta)
            stages=[proposed]
            for _,_,effects in rewards: stages.append(add(stages[-1],flat(effects)))
            for index,values in enumerate(stages):
                check('old_persistent_proposed_penalty:'+ident+':'+str(index), any(bad(k,values[k]) for k in delta))
            name=next(v for k,_,v in body if k=='name')
            track=next((v for k,_,v in body if k=='track'),'grand')
            inventory.append(dict(id=ident,name=loc.get(name,name),track=track,base=base,final=final,
                                  xp_cost=next(v for k,_,v in body if k=='xp_cost'),
                                  availability=next(v for k,_,v in body if k=='available'),
                                  tracks=next((v for k,_,v in body if k=='tracks'),[]),
                                  activation_deltas=delta,proposed_activation={k:proposed[k] for k in delta},
                                  proposed_final={k:stages[-1][k] for k in delta},stage_penalties=[{k:v for k,v in x.items() if k in delta and bad(k,v)} for x in stages],
                                  draft_final=draft_final,positive_final_targets=POSITIVE_FINAL_TARGETS.get(ident,{}),
                                  mastery=next((v for k,_,v in body if k=='mastery'),[]),
                                  side_effects=next((v for k,_,v in body if k=='effect'),[])))
    check('all_45_existing_choices_covered', {x['id'] for x in inventory}==set(OLD_DEBUFF_DELTAS) and len(inventory)==45)
    check('all_old_rationales_recorded',set(OLD_REASON)==set(OLD_DEBUFF_DELTAS))
    check('existing_costs_match_native_design',all(x['xp_cost']==('100' if x['track']=='grand' else '75') for x in inventory))
    proposed=[]
    for item in [*GRANDS,*SUBS]:
        current={k:Decimal(str(v)) for k,v in item['activation'].items()}
        stages=[current]
        for reward in item['progression']: stages.append(add(stages[-1],reward['effects']))
        check('progression_length:'+item['id'],len(item['progression'])==(6 if item['track']=='grand' else 5))
        check('sources:'+item['id'],all(s in SOURCES for s in item['sources']))
        check('english_punctuation:'+item['id'],not any(c in item['description'] for c in ('\u2013','\u2014')))
        for index,values in enumerate(stages): check('new_persistent_penalty:'+item['id']+':'+str(index),any(bad(k,v) for k,v in values.items()))
        proposed.append({**item,'final':stages[-1]})
    check('all_seven_new_sub_tracks',Counter(x['track'] for x in SUBS)==Counter({key:2 for key in TRACK_LABELS}))
    check('all_new_grands_have_six_tracks',all(len(x['tracks'])==6 for x in GRANDS))
    indexed={x['id']:x for x in proposed}
    old_indexed={x['id']:x for x in inventory}
    builds={}
    for name,(grand,subs) in EXAMPLE_BUILDS.items():
        check('legal_build_tracks:'+name, [indexed[s]['track'] if s in indexed else old_indexed[s]['track'] for s in subs]==list(indexed[grand]['tracks']))
        check('unique_subs:'+name,len(set(subs))==6)
        total=indexed[grand]['final']
        for sub in subs:
            total=add(total,indexed[sub]['final'] if sub in indexed else old_indexed[sub]['draft_final'])
        builds[name]={'grand':grand,'subdoctrines':subs,'combined_native_contributions':total}
    # This is a static model, not an engine or competitive-balance certification.
    definitions=(Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV/documentation/modifiers_documentation.md')).read_text(encoding='utf-8-sig')
    native=set(re.findall(r'^## ([a-zA-Z0-9_]+)\s*$',definitions,re.M))
    md=set()
    for p in (ROOT/'common/modifier_definitions').glob('*.txt'):
        md.update(re.findall(r'^([a-zA-Z0-9_]+)\s*=\s*\{',p.read_text(encoding='utf-8-sig'),re.M))
    for item in proposed:
        for key in item['final']:
            if '.' not in key:
                check('known_modifier:'+item['id']+':'+key,key in native or key in md or key=='repair_speed_air_base_factor')
    records={'project':'IMPERIA COLD WAR','status':'DESIGN ONLY. No runtime doctrine has been changed.',
             'existing_inventory':inventory,'new_concepts':proposed,'example_builds':builds,'sources':SOURCES,
             'source_sha256':hashes,'checks':checks,'failed':[c['check'] for c in checks if not c['passed']],
             'limits':['No engine run','No native UI test','No multiplayer balance proof','Old positive reward/coverage repairs are specified in the brief, not applied to runtime source.']}
    (HERE/'concept_values.json').write_text(json.dumps(records,indent=2,default=str)+'\n',encoding='utf-8')
    overview=['IMPERIA COLD WAR','','# Air Command: numerical concept catalogue','',
              'Design only, 29 October 2026. All proposed numbers are balance abstractions, not measured historical effects.',
              'Read [the main brief](air_doctrine_concepts_20261029.md) for scope, historical rationale, native limits and required corrections.',
              '', 'Grand doctrines cost 100 Air XP; subdoctrines cost 75 Air XP. Each new sub has five 100-mastery rewards. Grand milestones follow the six listed track slots.',
              'Activation values below remain active during mastery. Final values are cumulative contributions from that choice alone. Country, equipment and unit layers remain separate.',
              'All displayed numbers are percentage modifiers. Percentage changes to accident or XP-loss modifiers are not percentage-point changes in actual losses.',
              'Air force personnel cost uses the current MD weekly budget channel. Production IC cost changes aircraft manufacturing cost, not the treasury.', '']
    for item in proposed:
        overview += ['## '+item['name'],'',
                     '**Track:** '+TRACK_LABELS.get(item['track'],'Grand doctrine')+'. '+('**Slots:** '+', '.join(TRACK_LABELS[t] for t in item['tracks'])+'.' if item['track']=='grand' else ''),
                     '',item['description'],'','**On selection:** '+render(item['activation'])+'.','',
                     '| Stage | Name | Additional native modifiers |','| --- | --- | --- |']
        for index,reward in enumerate(item['progression'],1): overview.append(f'| {index} | {reward["name"]} | {render(reward["effects"])} |')
        overview += ['', '**Fully mastered:** '+render(item['final'])+'.','',
                     '**Historical basis:** '+', '.join('['+SOURCES[s][0]+']('+SOURCES[s][1]+')' for s in item['sources'])+'.','']
    overview += ['# Existing choices: complete proposed drawback schedule','',
                 'Every row is a proposed activation change. The final column already includes all of the choice\'s existing rewards on those same native fields. Unrelated positive rewards are preserved in this arithmetic model. Necessary scope and misleading-reward repairs are described separately in the main brief.','']
    for track in ['grand',*TRACK_LABELS]:
        overview += ['## '+TRACK_LABELS.get(track,'Existing Grand Doctrines'),'',
                     '| Existing choice | Proposed on-selection values | Values after its own mastery | Rationale |',
                     '| --- | --- | --- | --- |']
        for item in inventory:
            if item['track']==track: overview.append('| '+item['name']+' | '+render(item['proposed_activation'])+' | '+render(item['proposed_final'])+' | '+OLD_REASON[item['id']]+' |')
        overview.append('')
    overview += ['# Positive end-state adjustments for inherited outliers','',
                 'These are proposed cumulative targets BEFORE adding the new drawback deltas. They replace the corresponding current positive totals. Unlisted positive fields remain. Existing reward stages need redistribution in an implementation.', '',
                 '| Existing choice | Current values on the changed fields | Proposed positive end-state targets |',
                 '| --- | --- | --- |']
    for ident, targets in POSITIVE_FINAL_TARGETS.items():
        item=old_indexed[ident]
        overview.append('| '+item['name']+' | '+render({k:item['final'].get(k,0) for k in targets})+' | '+render(targets)+' |')
    overview += ['','BVR and WVR positive targets deliberately cover all four eligible fighter roles. The selected-role mapping must be repaired alongside the penalties. The present table is a design target, not evidence that the runtime scopes have changed.',
                 '', '# Legal example builds and their combined costs','',
                 'The complete native-field sums are in the JSON record. These are additive contributions by exact field; they are not a simulation of final damage, kills, sortie throughput or money paid. Country and aircraft/equipment layers are kept separate.','']
    for name,record in builds.items():
        values=record['combined_native_contributions']
        overview += ['## '+name,'', '**Grand:** '+indexed[record['grand']]['name']+'.',
                     '**Slots:** '+', '.join(indexed[s]['name'] if s in indexed else old_indexed[s]['name'] for s in record['subdoctrines'])+'.',
                     '', '**Budget and fuel:** '+render({k:values[k] for k in ('airforce_personnel_cost_multiplier_modifier','air_fuel_consumption_factor') if k in values})+'.','']
    overview += ['# Source register','']
    for ident,(title,url,scope) in SOURCES.items(): overview += ['- **'+ident+'**: ['+title+']('+url+'). '+scope]
    overview += ['', '# Exact technical values','',
                 '`tools/air_doctrine_design_1970/concept_values.json` retains every native field, exact scope, activation delta and cumulative stage calculation. It also records source hashes and every check result.',
                 'Existing MD/Paradox content retains upstream authorship. Historical texts remain their authors\' works. Individual upstream asset permissions are unknown where not recorded. No third-party images or document copies are redistributed.','']
    (ROOT/'docs/air_doctrine_values_20261029.md').write_text('\n'.join(overview),encoding='utf-8')
    assert hashes=={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in INPUTS}, 'Runtime inputs changed during the model build'
    print(json.dumps({'old_grands':sum(x['track']=='grand' for x in inventory),'old_subdoctrines':sum(x['track']!='grand' for x in inventory),
                      'new_grands':len(GRANDS),'new_subdoctrines':len(SUBS),'checks':len(checks),
                      'failed':records['failed'],'runtime_files_unchanged':True},indent=2))
    raise SystemExit(bool(records['failed']))


if __name__=='__main__': main()
