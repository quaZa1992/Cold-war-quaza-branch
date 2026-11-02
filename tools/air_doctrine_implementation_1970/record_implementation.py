# IMPERIA COLD WAR — Installed Air Command values and bounded implementation evidence.
from pathlib import Path
from collections import defaultdict
import json,hashlib
import build
build.sys.path.insert(0,str(build.HERE))
from validate import flat,total

ROOT,HERE=build.ROOT,build.HERE

def main():
    inventory=[]
    for path in [build.OLD_GRAND,build.NEW_GRAND,build.OLD_SUB,build.NEW_SUB]:
        for ident,_,body in build.parse((ROOT/path).read_text(encoding='utf-8')):
            progression=build.get(body,'rewards',build.get(body,'milestones',[]))
            inventory.append({'id':ident,'source':path,'track':build.get(body,'track','grand'),
                'activation':{k:str(v) for k,v in flat(body).items()},
                'progression':[{'id':key,'effects':{k:str(v) for k,v in flat(stage).items()}} for key,_,stage in progression],
                'final':{k:str(v) for k,v in total(body).items()}})
    record={'project':'IMPERIA COLD WAR','installed_doctrines':inventory,
            'runtime_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in build.outputs()},
            'basis':'Approved design plus documented native role, owned-legacy-reward and capability integrations.'}
    (HERE/'installed_values.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    validation=json.loads((HERE/'validation.json').read_text(encoding='utf-8'))
    native=json.loads((HERE/'native_result.json').read_text(encoding='utf-8')) if (HERE/'native_result.json').exists() else {}
    location=json.loads((HERE/'native_run_location.json').read_text(encoding='utf-8')) if (HERE/'native_run_location.json').exists() else {}
    native_matches=native.get('profile')==location.get('profile')
    native_pass=native_matches and native.get('completed') and not native.get('failed_markers') and not native.get('air_related_errors')
    overlay=location.get('fixture_runtime_sha256',{})
    changed=[p for p,digest in record['runtime_sha256'].items() if overlay.get(p)!=digest]
    result={
      'project':'IMPERIA COLD WAR','new_grands':5,'new_subdoctrines':14,'inherited_choices_rebalanced':45,
      'installed_grands':12,'installed_subdoctrines':52,'new_grand_milestones':30,'new_sub_rewards':70,
      'original_icons':19,'static_checks_passed':validation['passed'],'static_failures':validation['failed'],
      'native_pass':bool(native_pass and not changed and not validation['failed']),'native_profile':location.get('profile'),'native_runtime_mismatches':changed,
      'native_unique_completed_masteries':len({line.split('MASTERY_',1)[1].rsplit('_PASS',1)[0] for line in native.get('markers',[]) if 'ICW_AIR MASTERY_' in line and '_PASS' in line}) if native_matches else 0,
      'engine_full_error_log':native.get('full_error_log') if native_matches else None,
      'multiplayer_test':False,'live_ui_verified':False,
      'verification_limits':['Native completion is distinct from adversarial multiplayer balance.','Live UI and DLC-disabled paths require separate inspection.','Migration is exercised by injecting old ideas into a new test game; loading an actual pre-change save is not certified.']}
    (HERE/'implementation_result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
