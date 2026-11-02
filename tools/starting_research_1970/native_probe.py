# IMPERIA COLD WAR — Native January 1970 starting-research verification.
"""Use the existing hidden native runner with an isolated research/design fixture."""
import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
from build import outputs, FLAG
from catalog import catalogue
from variants import FLAG as VARIANT_FLAG, BEGIN as VARIANT_BEGIN, END as VARIANT_END, load_variants

RUNTIME_ROOT=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/starting_research_1970').resolve()
MARKER='# IMPERIA COLD WAR — Isolated starting-research verification.\n'


def fixture():
    _,countries=outputs();techs,_=catalogue()
    hook=MARKER+'''on_actions = {
 on_startup = { effect = {
  if = {
   limit = { NOT = { has_global_flag = ICW_RESEARCH_probe_queued } }
   set_global_flag = ICW_RESEARCH_probe_queued
   log = "ICW_RESEARCH STARTUP"
   USA = { country_event = { id = ICW_QUALITY.1 hours = 1 } }
  }
 } }
}
'''
    event=[MARKER.rstrip(),'add_namespace = ICW_QUALITY','country_event = { id = ICW_QUALITY.1 hidden = yes is_triggered_only = yes immediate = {','log = "ICW_RESEARCH FIRST_HOUR"']
    for dlc,label in [('No Step Back','NSB'),('By Blood Alone','BBA'),('Gotterdammerung','GOT')]:
        event+=['if = { limit = { has_dlc = "'+dlc+'" } log = "ICW_RESEARCH DLC '+label+' active" } else = { log = "ICW_RESEARCH DLC '+label+' inactive" }']
    forbidden=[key for key,row in techs.items() if row['year'] and row['year']>1969]
    for tag,row in sorted(countries.items()):
        event += [tag+' = {','if = { limit = { exists = yes }','set_temp_variable = { ICW_RESEARCH_failures = 0 }',
                  'if = { limit = { NOT = { has_country_flag = '+FLAG+' } } add_to_temp_variable = { ICW_RESEARCH_failures = 1 } log = "ICW_RESEARCH FAIL '+tag+' history_flag" }',
                  'if = { limit = { NOT = { has_country_flag = '+VARIANT_FLAG+' } } add_to_temp_variable = { ICW_RESEARCH_failures = 1 } log = "ICW_RESEARCH FAIL '+tag+' variant_history_flag" }']
        groups=row['technology_groups']
        def check(keys):
            return ['if = { limit = { NOT = { has_tech = '+key+' } } add_to_temp_variable = { ICW_RESEARCH_failures = 1 } log = "ICW_RESEARCH FAIL '+tag+' missing '+key+'" }' for key in keys]
        event+=check(groups['common'])
        for dlc,yes,no in [('No Step Back','nsb','legacy'),('By Blood Alone','bba','non_bba'),('Gotterdammerung','got','non_got')]:
            event+=['if = { limit = { has_dlc = "'+dlc+'" }']+check(groups[yes])+['} else = {']+check(groups[no])+['}']
        permitted=set().union(*(set(items) for items in groups.values()))
        absent=[key for key,entry in techs.items() if entry['year'] is not None and entry['year']<=1969 and key not in permitted]
        event+=['if = { limit = { has_tech = '+key+' } add_to_temp_variable = { ICW_RESEARCH_failures = 1 } log = "ICW_RESEARCH FAIL '+tag+' unassigned '+key+'" }' for key in absent]
        # Check every dated future technology, rather than a hand-picked sample.
        event+=['if = { limit = { has_tech = '+key+' } add_to_temp_variable = { ICW_RESEARCH_failures = 1 } log = "ICW_RESEARCH FAIL '+tag+' future '+key+'" }' for key in forbidden]
        event+=['if = { limit = { check_variable = { ICW_RESEARCH_failures = 0 } } log = "ICW_RESEARCH PASS '+tag+'" }','}','}']
    event+=['log = "ICW_RESEARCH COMPLETE"','log = "ICW_QUALITY COMPLETE"','} }','']
    return hook,'\n'.join(event)


def load_runner(runroot,ui_hold=False):
    spec=importlib.util.spec_from_file_location('icw_existing_native_runner',ROOT/'tools/multiplayer_quality/native_probe.py')
    module=importlib.util.module_from_spec(spec)
    if ui_hold:
        # Apply UI-only launch/hold changes in memory. Keep the shared runner
        # unchanged and terminate only the private process it creates.
        source=Path(spec.origin).read_text(encoding='utf-8')
        old="if 'ICW_QUALITY COMPLETE' in observed:"
        assert source.count(old)==1
        source=source.replace(old,"if 'ICW_QUALITY COMPLETE' in observed and (PROFILE / 'ui_finished').exists():")
        old="'-start_tag=USA', '-start_speed=5', '-hands_off'"
        assert source.count(old)==1
        source=source.replace(old,"'-start_tag=SOV', '-start_speed=1'")
        source=source.replace('x=1024 y=720','x=1280 y=900')
        exec(compile(source,spec.origin,'exec'),module.__dict__)
    else:spec.loader.exec_module(module)
    module.RUNTIME=runroot
    module.PROFILE=runroot/'profile'
    module.OUT=runroot/'diagnostics'
    return module


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare',action='store_true')
    parser.add_argument('--run',action='store_true')
    parser.add_argument('--collect',action='store_true',help='Collect an existing private run without launching HOI4.')
    parser.add_argument('--duration',type=int,default=480)
    parser.add_argument('--ui-hold',action='store_true',help='Hold the isolated test for designer inspection until its ui_finished sentinel or timeout.')
    args=parser.parse_args()
    assert sum((args.prepare,args.run,args.collect))==1
    planpath=HERE/'native_plan.json'
    if args.prepare:
        runroot=(RUNTIME_ROOT/datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')).resolve()
        assert runroot.is_relative_to(RUNTIME_ROOT) and not runroot.exists()
        runroot.mkdir(parents=True)
        snapshot=runroot/'engine_snapshot'
        snapshot.mkdir()
        # An explicit live-game folder list excludes reports, tools, archives
        # and old scenario-test directories. No asset tree is enumerated here.
        for name in ('common','events','history','interface','localisation','portraits','descriptions','tutorial'):
            source=ROOT/name
            if source.is_dir():
                assert not source.is_junction() and not source.is_symlink()
                shutil.copytree(source,snapshot/name)
        for source in ROOT.iterdir():
            if source.is_file() and source.suffix in {'.mod','.txt','.lua'}:
                shutil.copy2(source,snapshot/source.name)
        # Link native assets without copying or enumerating the contents of any
        # asset junction. Only scripts/history are frozen by the existing runner.
        for name in ('gfx','map','sound','music'):
            target=(snapshot/name).resolve();source=ROOT/name
            assert target.is_relative_to(runroot)
            quote=lambda p:"'"+str(p).replace("'","''")+"'"
            subprocess.run(['powershell','-NoProfile','-Command','New-Item -ItemType Junction -Path '+quote(target)+' -Target '+quote(source)+' | Out-Null'],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
        plan={'project':'IMPERIA COLD WAR','runtime':str(runroot),'snapshot':str(snapshot),'duration':args.duration}
        planpath.write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(plan))
        return
    plan=json.loads(planpath.read_text(encoding='utf-8'));runroot=Path(plan['runtime']).resolve()
    assert args.collect or not plan.get('stale_after_repair'),'Prepare a fresh final-source snapshot before running HOI4'
    assert runroot.is_relative_to(RUNTIME_ROOT)
    # Never interfere with a game session the user started independently.
    active=subprocess.run(['powershell','-NoProfile','-Command',"[System.Diagnostics.Process]::GetProcessesByName('hoi4').Length"],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW)
    assert active.returncode==0,'Unable to establish whether an existing HOI4 session is active'
    if not args.collect and active.stdout.strip()!='0':
        blocked={'project':'IMPERIA COLD WAR','status':'not_run_existing_game',
                 'checked_utc':datetime.now(timezone.utc).isoformat(),'snapshot':plan['snapshot'],
                 'existing_game_processes':int(active.stdout.strip()),'test_process_launched':False,
                 'note':'An existing HOI4 process prevents the isolated test. No existing process was changed or stopped. Static source checks are recorded separately; native startup, design inventory, save/reload and multiplayer remain unverified.'}
        (HERE/'native_validation.json').write_text(json.dumps(blocked,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(blocked))
        return
    runner=load_runner(runroot,args.ui_hold);hook,event=fixture();original_write=runner.write
    def write(relative,source):
        if relative=='fixture/common/on_actions/zzzzzzzzzz_IMPERIA_quality_probe.txt':source=hook
        elif relative=='fixture/common/on_actions/000_IMPERIA_quality_probe.txt':source=MARKER+'on_actions = {}\n'
        elif relative=='fixture/events/ICW_quality_probe.txt':source=event
        original_write(relative,source)
    runner.write=write
    sys.argv=[str(Path(__file__)),'--snapshot',plan['snapshot'],'--duration',str(args.duration)]
    if not args.collect:runner.main()
    native=json.loads((runner.OUT/'native_result.json').read_text(encoding='utf-8'))
    log=(runner.OUT/'native_game.log').read_text(encoding='utf-8')
    errors=(runner.OUT/'native_error.log').read_text(encoding='utf-8')
    import re
    passed=sorted(set(re.findall(r'ICW_RESEARCH PASS ([A-Z0-9]{3})',log)))
    failures=[line for line in log.splitlines() if 'ICW_RESEARCH FAIL' in line]
    models,_=load_variants()
    fitted={value for model in models.values() for value in model.get('modules',{}).values() if value!='empty'}
    equipment_types={model['type'] for model in models.values()}
    equipment_pattern=re.compile(r'\b(?:'+'|'.join(re.escape(word) for word in sorted(fitted|equipment_types))+r')\b')
    relevant=[line for line in errors.splitlines() if any(word in line for word in ('world_research','starting_research','COLDWAR_1970','researched national technology','set_technology','create_equipment_variant','mdcw_1970_air_research_effects','mdcw_1970_infantry_research_effects')) or equipment_pattern.search(line)]
    spans={}
    for path in (Path(plan['snapshot'])/'history/countries').glob('*.txt'):
        source=path.read_text(encoding='utf-8-sig')
        if VARIANT_BEGIN in source:
            spans[path.name]=(source[:source.index(VARIANT_BEGIN)].count('\n')+1,
                              source[:source.index(VARIANT_END)].count('\n')+1)
    component_record=json.loads((HERE/'component_manifest.json').read_text(encoding='utf-8'))
    custom_ids=set(component_record['modules'])|set(component_record['frames'])
    # Extra historical role frames are retired. Native types are in the
    # equipment_types set; do not depend on the removed role-frame generator API.
    custom_pattern=re.compile(r'\b(?:'+'|'.join(re.escape(word) for word in sorted(custom_ids))+r')\b')
    feature_diagnostics=[]
    for line in relevant:
        match=re.search(r'history/countries/([^:]+\.txt):(\d+):',line)
        in_variants=bool(match and match[1] in spans and spans[match[1]][0]<=int(match[2])<=spans[match[1]][1])
        if in_variants or custom_pattern.search(line) or 'COLDWAR_1970_service_components' in line or 'COLDWAR_1970_historical' in line:
            feature_diagnostics.append(line)
    finished='ICW_RESEARCH COMPLETE' in log
    report={
        'project':'IMPERIA COLD WAR','snapshot':plan['snapshot'],'full_diagnostics':str(runner.OUT),
        'source_snapshot_unchanged':native['source_snapshot_unchanged'],'elapsed_seconds':native['elapsed_seconds'],
        'startup_observed':'ICW_RESEARCH STARTUP' in log,'first_hour_observed':'ICW_RESEARCH FIRST_HOUR' in log,
        'observed_dlc_branches':dict(re.findall(r'ICW_RESEARCH DLC (NSB|BBA|GOT) (active|inactive)',log)),
        'status':'passed_feature_checks' if finished and passed and not failures and not feature_diagnostics else 'failed_or_incomplete',
        'complete':finished,'countries_checked':passed,'country_count':len(passed),
        'failures':failures,'relevant_engine_diagnostics':relevant,'total_engine_diagnostic_lines':native['error_lines'],
        'feature_engine_diagnostics':feature_diagnostics,
        'other_equipment_related_engine_diagnostics':[line for line in relevant if line not in feature_diagnostics],
        'last_observed_game_date':native['last_observed_game_date'],'live_multiplayer_tested':False,'save_reload_tested':False,
        'variant_history_receipts_checked':True,'variant_inventory_inspected':False,
        'note':'Native all-installed-DLC positive-grant, unassigned-pre1970, all-dated-future-tech and design-history receipt checks for actually existing countries. Engine diagnostics include fitted component and equipment IDs. Receipt flags do not prove every design inventory entry; alternate DLC combinations and hypothetical releases are verified by the independent source model.',
    }
    stopfile=runner.PROFILE/'ui_finished'
    interrupted=stopfile.is_file() and 'Computer Use stopped' in stopfile.read_text(encoding='utf-8-sig')
    if interrupted:
        report.update(status='interrupted_before_designer_inspection',user_stopped_computer_use=True,
                      designer_ui_verified=False,variant_history_receipts_checked=finished,
                      note='Physical Escape stopped Computer Use. No further app input was issued. The private test was deliberately stopped; partial logs do not establish startup or designer acceptance.')
    if plan.get('stale_after_repair'):
        report['source_revision']='Earlier frozen snapshot; final source correction not rerun'
    (HERE/'native_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:report[key] for key in ('project','status','complete','country_count','first_hour_observed','observed_dlc_branches','source_snapshot_unchanged','elapsed_seconds','full_diagnostics')}|{'failures':len(failures),'feature_engine_diagnostics':len(feature_diagnostics),'other_equipment_related_engine_diagnostics':len(relevant)-len(feature_diagnostics)}))


if __name__=='__main__':main()
