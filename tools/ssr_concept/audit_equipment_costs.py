# IMPERIA COLD WAR — equipment-target and retained-production regression audit.
"""Static source and compatible-route checks. Does not test the game engine."""
from pathlib import Path
import hashlib,json,re

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/design/ssr_1970_concept'
source=OUT/'DESIGN.json'
design=json.loads(source.read_text(encoding='utf-8'))
errors=[]
expected={
 'aircraft':{'small_plane_airframe','small_plane_strike_airframe','small_plane_cas_airframe',
             'medium_plane_fighter_airframe','medium_plane_airframe','medium_plane_cas_airframe',
             'large_plane_air_transport_airframe'},
 'armour':{'medium_tank_chassis'},
 'artillery':{'artillery_equipment','medium_tank_artillery_chassis','medium_tank_rocket_chassis'},
 'army':{'infantry_weapons_type','util_vehicle_type'},
 'navy':{'patrol_boat','corvette','frigate'},'electronics':{'cnc_equipment_type'},
}
retained={
 'special_aircraft_mandate':{'industrial_capacity_factory':.05},
 'special_aircraft_left':{'industrial_capacity_factory':.05},
 'special_armour_mandate':{'industrial_capacity_factory':.05,'production_factory_max_efficiency_factor':.05},
 'special_armour_left':{'production_factory_max_efficiency_factor':.08},
 'special_armour_right':{'industrial_capacity_factory':.08},
 'special_armour_right_follow':{'production_factory_max_efficiency_factor':.04},
 'special_armour_office':{'industrial_capacity_factory':.04},
 'special_armour_settlement':{'production_factory_max_efficiency_factor':.04},
 'special_artillery_mandate':{'industrial_capacity_factory':.05},
 'special_artillery_right':{'industrial_capacity_factory':.06},
 'special_artillery_office':{'production_factory_max_efficiency_factor':.06},
 'special_artillery_settlement':{'industrial_capacity_factory':.04},
 'special_navy_mandate':{'industrial_capacity_dockyard':.08},
 'special_navy_left':{'industrial_capacity_dockyard':.12},
 'special_navy_right':{'industrial_capacity_dockyard':.04},
 'special_navy_office':{'industrial_capacity_dockyard':.05},
 'special_electronics_left':{'production_factory_max_efficiency_factor':.08},
 'special_electronics_right':{'production_factory_max_efficiency_factor':-.03},
}
targets=set().union(*expected.values())
providers={}
for path in sorted((ROOT/'common/units/equipment').glob('*.txt')):
    for line,text in enumerate(path.read_text(encoding='utf-8-sig').splitlines(),1):
        match=re.match(r'\s*(\w+)\s*=\s*\{',text)
        if match and match[1] in targets:
            providers.setdefault(match[1],dict(path=str(path.relative_to(ROOT)),line=line))
for key in targets:
    if key not in providers:errors.append('Missing equipment declaration: '+key)
    if key not in design['equipment_labels']:errors.append('Missing native equipment name: '+key)

routes=[]
for tag,model in design['models'].items():
    by={node['key']:node for node in model['nodes']}
    for key,modifiers in retained.items():
        for name,value in modifiers.items():
            if abs(by[key]['modifiers'].get(name,0)-value)>1e-9:
                errors.append(f'{tag}: original production modifier changed: {key} {name}')
    for role,types in expected.items():
        prefix='special_'+role+'_'
        nodes=[n for n in model['nodes'] if n.get('specialisation')==role]
        for n in nodes:
            names=[e['target'] for e in n.get('equipment_bonuses',[])]
            if len(names)!=len(set(names)):errors.append('Duplicate target in '+n['id'])
        for direction in ['left','right']:
            for administration in ['priority','efficiency']:
                opposite='right' if direction=='left' else 'left'
                excluded={opposite,opposite+'_follow','efficiency' if administration=='priority' else 'priority'}
                chosen=[n for n in nodes if n['key'].removeprefix(prefix) not in excluded]
                full={};legacy={}
                for n in chosen:
                    for field,dest in [('equipment_bonuses',full),('legacy_equipment_bonuses',legacy)]:
                        for equipment in n.get(field,[]):
                            key=equipment['target']
                            dest[key]=dest.get(key,0)+equipment['modifiers'].get('build_cost_ic',0)
                if not types.issubset(full):errors.append(f'{tag}: incomplete {role} cost coverage')
                for key in types:
                    if full.get(key,0)>=0:errors.append(f'{tag}: no net SSR cost saving: {role} {direction} {key}')
                if tag=='UKR':
                    routes.append(dict(role=role,direction=direction,administration=administration,
                        production_cost_percent={k:round(v*100,5) for k,v in full.items()},
                        legacy_cost_percent={k:round(v*100,5) for k,v in legacy.items()}))
report=dict(project='IMPERIA COLD WAR',status='Static concept checks only; native engine and DLC behavior untested.',
 design_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),errors=errors,countries=len(design['models']),
 weapon_related_programmes=len(expected),compatible_routes_checked=len(design['models'])*6*4,
 retained_production_sources_per_country=len(retained),equipment_providers=providers,representative_routes=routes)
(OUT/'EQUIPMENT_COST_CHECKS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in {'equipment_providers','representative_routes'}}))
if errors:raise SystemExit(1)
