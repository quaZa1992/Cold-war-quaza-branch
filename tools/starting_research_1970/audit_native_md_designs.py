# IMPERIA COLD WAR — Independent native MD equipment designer routing audit.
"""Check actual GUI registrations and MD 2000 precedent, not just module presence."""
import hashlib
import json
import re
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
from variants import load_variants

def audit():
    models,countries=load_variants()
    equipment=json.loads((HERE/'equipment_catalog.json').read_text(encoding='utf-8'))['equipment']
    reference=json.loads((HERE/'MD_2000_variant_reference.json').read_text(encoding='utf-8'))['variants']
    guis=list((ROOT/'interface/equipmentdesigner').rglob('*.gui'))
    registrations={}
    for path in guis:
        for name in re.findall(r'\bname\s*=\s*"(equipment_designer_[^"]+)"',path.read_text(encoding='utf-8-sig')):
            registrations.setdefault(name,[]).append(path.relative_to(ROOT).as_posix())
    records={};errors=[]
    def require(ok,model,detail):
        if not ok:errors.append({'model':model,'detail':detail})
    for key,model in models.items():
        typ=model['type'];contract=model['native_md_contract'];row=equipment[typ]
        donor=next((r for r in reference if r['type']==typ),None)
        entry={'name':model['name'],'type':typ,'contract':contract,
               'native_2000_example':{'country':donor['country'],'name':donor['name'],'file':donor['file']} if donor else None}
        if contract=='modular_aircraft':
            gui='equipment_designer_'+typ
            require(bool(registrations.get(gui)),key,'Aircraft has no exact native designer GUI registration: '+gui)
            require(Path(row['file']).name in {'MD_plane_airframes.txt','MD_x_plane_airframes.txt'},key,'Aircraft type is not a native MD production frame')
            require(bool(model.get('modules')) and model.get('requires_dlc')==['By Blood Alone'],key,'BBA aircraft must have a modular primary design')
            require(typ.endswith('_1'),key,'Historical aircraft must use the first native MD production tier')
            entry['designer_gui']=registrations.get(gui,[])
            if not donor:entry['precedent_note']='Native role registered in MD designer GUI, unused by retained 2000 prefabs. Historical service fit selects this role.'
        elif contract=='fixed_transport_helicopter':
            require(typ=='transport_helicopter_1' and not model.get('modules') and not model.get('requires_dlc'),key,'Transport helicopter must follow the fixed native MD transport prefab')
            require(any(r['type']==typ and not r['modules'] for r in reference),key,'Missing fixed native transport-helicopter precedent')
        elif contract=='modular_ground':
            require(Path(row['file']).name in {'MD_tank_chassis.txt','MD_x_tank_chassis.txt'},key,'Ground design uses an extra custom chassis')
            gui='equipment_designer_'+row['archetype']
            require(bool(registrations.get(gui)),key,'Ground design has no native archetype designer GUI: '+gui)
            require(model.get('requires_dlc')==['No Step Back'],key,'Ground designer requires NSB')
            entry['designer_gui']=registrations.get(gui,[])
        elif contract=='modular_ship':
            require(bool(donor),key,'Historical ship hull has no native MD 2000 prefab precedent')
            require(Path(row['file']).name.startswith('MD_'),key,'Ship uses an extra custom hull')
        require(not (typ in {'transport_plane1','naval_plane1'}),key,'Fixed aircraft primary bypasses BBA designer')
        records[key]=entry
    # The old erroneous MiG frame must fail the exact-registration test.
    require('equipment_designer_mdcw_small_plane_airframe_gen2' not in registrations,'negative_control','Unregistered old aircraft frame unexpectedly passes the designer contract')
    report={'project':'IMPERIA COLD WAR','evidence_level':'Independent source routing and retained native MD 2000 prefab comparison; live UI recorded separately',
            'status':'passed' if not errors else 'failed','error_count':len(errors),'errors':errors,
            'model_count':len(models),'assignments':sum(map(len,countries.values())),
            'native_2000_variants':len(reference),'models':records,
            'source_sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in guis}}
    (HERE/'native_md_design_audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['project','status','model_count','assignments','native_2000_variants','error_count']}))
    if errors:print(json.dumps(errors[:8]));return 1
    return 0

if __name__=='__main__':raise SystemExit(audit())
