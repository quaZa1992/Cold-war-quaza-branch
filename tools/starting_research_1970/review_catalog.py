# IMPERIA COLD WAR — Review index for researched January 1970 equipment designs.
"""Render authoritative variant inputs as a compact human-readable review index."""
import collections
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
FILES=('europe','asia','africa','americas_oceania','usa')


def cell(value):
    return str(value).replace('|','/').replace('\n',' ')


def main():
    models={};operators=collections.defaultdict(list)
    for region in FILES:
        data=json.loads((HERE/(region+'_variants.json')).read_text(encoding='utf-8'))
        for key,row in data['models'].items():models[key]=dict(row,region=region)
        for tag,ids in data['countries'].items():
            for key in ids:operators[key].append(tag)
    lines=['IMPERIA COLD WAR','','# January 1970 historical design review index','',
           'Generated from the five authoritative regional variant inputs by `review_catalog.py`. This index describes named service designs, not deployed quantities or a complete historical order of battle. Country research covers all 400 history tags separately. Empty release or uncertain country packages retain their conservative researched native equipment families.','',
           'Physical measurements below are historical evidence. Native MD module values and upgrade levels remain game abstractions. A native armor level is not a literal millimetre measurement, and an engine upgrade is not a horsepower field. Original service fits exclude later improvements. Full specifications, evidence, exceptions and module slots remain in the linked JSON inputs and companion source registers.','',
           f'{len(models)} design records; {sum(map(len,operators.values()))} country-design assignments.','',
           '| Model | Native equipment family | Service by | Designer | Operators | Native upgrades | Evidence |',
           '|---|---|---|---|---|---|---|']
    for key,row in sorted(models.items(),key=lambda item:(item[1]['name'].lower(),item[0])):
        levels=', '.join(f'{name}={value}' for name,value in row.get('upgrades',{}).items()) or 'Baseline'
        source=row['sources'][0] if row.get('sources') else None
        evidence=f'[Source]({source})' if source else 'See country rationale'
        values=[f"{row['name']} (`{key}`)",f"`{row['type']}`",row['service_by'],', '.join(row.get('requires_dlc',[])) or 'Native static/ship',', '.join(sorted(operators[key])),levels,evidence]
        lines.append('| '+' | '.join(cell(value) for value in values)+' |')
    lines+=['','# Sourced land-vehicle calibration','',
            'These measurements and relative native upgrade choices can be reviewed independently. An omitted measurement is unknown in this record; it is not inferred from another model. Module selections, original fuel/material, native costs and reliability effects also contribute to the resulting equipment.','',
            '| Model | Main gun mm | Engine power | Road speed km/h | Maximum stated armor mm | Native armor/engine levels |',
            '|---|---:|---|---:|---:|---|']
    for key,row in sorted(models.items(),key=lambda item:(item[1]['name'].lower(),item[0])):
        upgrades=row.get('upgrades',{});specs=row.get('historical_specs',{})
        if not any(name.startswith('tank_nsb_') for name in upgrades):continue
        power=[]
        for name,unit in [('engine_power_ps','PS'),('engine_power_hp','hp'),('engine_power_kw','kW')]:
            if name in specs:power.append(f'{specs[name]} {unit}')
        values=[row['name'],specs.get('gun_mm',''),', '.join(power),specs.get('road_speed_kmh',''),specs.get('armor_max_mm',''),f"{upgrades.get('tank_nsb_armor_upgrade',0)} / {upgrades.get('tank_nsb_engine_upgrade',0)}"]
        lines.append('| '+' | '.join(cell(value) for value in values)+' |')
    lines+=['','# Full source manifests','']
    for region in FILES:
        lines.append(f'- [{region} model data]({region}_variants.json), [historical sources and mapping rationale]({region}_variants_sources.md).')
    (HERE/'MODEL_INDEX.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'project':'IMPERIA COLD WAR','models':len(models),'output':'MODEL_INDEX.md'}))


if __name__=='__main__':main()
