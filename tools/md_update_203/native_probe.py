# IMPERIA COLD WAR — Isolated native MD 2.0.3 loading and preservation smoke test.
"""Freeze loaded scripts/map on E:, use a private unsaved 1970 game, then exit.

Only this probe's process may be terminated. User saves, launcher playsets and
the installed mod sources are not modified by the native test.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import time

from audit import ROOT,OUT,PROJECT,emit

GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
RUNTIME=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/md_update_203')
MARK='# IMPERIA COLD WAR — Private MD 2.0.3 native smoke test.\n'
PREFIX='ICW_MD203'
CHECKS={
 'scenario_1970':'date > 1969.12.31 date < 1970.2.1',
 'israel_scenario':'ISR = { ISR70_is_scenario = yes }',
 'israel_focus_tree':'ISR = { has_focus_tree = ISR70_focus }',
 'israel_gdp_positive':'ISR = { has_variable = gdp_total check_variable = { gdp_total > 0 } }',
 'usa_gdp_positive':'USA = { has_variable = gdp_total check_variable = { gdp_total > 0 } }',
 'west_bank_occupation_budget':'ISR = { has_dynamic_modifier = { modifier = ISR70_policy_occupation_208_budget } }',
 'jerusalem_split':'207 = { is_owned_by = ISR is_controlled_by = ISR } 1253 = { is_owned_by = ISR is_controlled_by = ISR }',
 'ssr_agency_rule':'UKR = { has_autonomy_state = autonomy_soviet_republic_1985 COLDWAR_can_create_intelligence_agency = no }'}


def copy_tree(source,destination,hashes):
    destination.mkdir(parents=True,exist_ok=True)
    for entry in os.scandir(source):
        p=Path(entry.path);m=entry.stat(follow_symlinks=False)
        assert not m.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT,'Refusing to traverse junction: '+str(p)
        target=destination/entry.name
        if entry.is_dir(follow_symlinks=False):copy_tree(p,target,hashes)
        elif entry.is_file(follow_symlinks=False):
            shutil.copy2(p,target)
            raw=target.read_bytes();assert hashlib.sha256(raw).digest()==hashlib.sha256(p.read_bytes()).digest(),str(p)
            hashes[p.relative_to(ROOT).as_posix()]=hashlib.sha256(raw).hexdigest()


def main():
    active=subprocess.run(['powershell','-NoProfile','-Command','Get-Process hoi4 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
    if active.stdout.strip():
        report=dict(project=PROJECT,status='NOT_RUN_EXISTING_HOI4',native_test=False,
            active_process_ids=[int(s) for s in active.stdout.split() if s.isdigit()],
            reason='An existing HOI4 session is active. It was not stopped, modified or used for test fixtures.')
        emit(OUT/'native_report.json',report);print(json.dumps(report),flush=True)
        raise SystemExit(2)
    implementation=json.loads((OUT/'implementation.json').read_text(encoding='utf-8'))
    assert implementation['status']=='PASS','Complete the source-preservation check first'
    run=RUNTIME/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    snapshot,profile=run/'snapshot',run/'profile'
    assert run.resolve().is_relative_to(RUNTIME.resolve())
    hashes={}
    for name in ('common','events','history','interface','localisation','map','portraits'):
        copy_tree(ROOT/name,snapshot/name,hashes)
    for name in ('gfx','music','sound'):
        target=snapshot/name;assert not target.exists()
        subprocess.run(['cmd.exe','/c','mklink','/J',str(target),str(ROOT/name)],check=True,capture_output=True)
    shutil.copy2(ROOT/'descriptor.mod',snapshot/'descriptor.mod')

    def write(relative,value):
        p=profile/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(value,encoding='utf-8',newline='\n')

    write('mod/mdcoldwar.mod',(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig')+'\npath="'+snapshot.as_posix()+'"\n')
    addon=MARK+'name="IMPERIA MD203 Verification"\ndependencies={ "MD Cold War" }\npath="'+(profile/'fixture').as_posix()+'"\n'
    write('mod/probe.mod',addon);write('fixture/descriptor.mod',addon)
    write('dlc_load.json',json.dumps({'enabled_mods':['mod/mdcoldwar.mod','mod/probe.mod'],'disabled_dlcs':[]}))
    write('settings.txt',MARK+'language="l_english"\ngraphics={size={x=1024 y=720} fullScreen=no borderless=no}\nmaster_volume=0\n')
    write('fixture/common/on_actions/zzzzzzzz_ICW_MD203.txt',MARK+'on_actions = { on_startup = { effect = { log = "ICW_MD203 STARTUP" ISR = { country_event = { id = ICW_MD203.1 days = 2 } } } } }\n')
    assertions='\n'.join('if = { limit = { '+trigger+' } log = "'+PREFIX+' PASS '+name+'" } else = { log = "'+PREFIX+' FAIL '+name+'" }' for name,trigger in CHECKS.items())
    event=MARK+'add_namespace = ICW_MD203\ncountry_event = { id = ICW_MD203.1 hidden = yes is_triggered_only = yes immediate = {\n'+assertions+'\nlog = "ICW_MD203 COMPLETE"\n} }\n'
    write('fixture/events/ICW_MD203.txt',event)
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
    args=[str(GAME/'hoi4.exe'),'-debug','-noasserts','-assertsdialog=no','-userdir='+str(profile),'-start_tag=ISR','-start_speed=3','-hands_off']
    started=time.monotonic();process=subprocess.Popen(args,cwd=GAME,startupinfo=startup,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    print(json.dumps(dict(project=PROJECT,pid=process.pid,profile=str(profile),frozen_files=len(hashes))),flush=True)
    log='';last_progress=0
    try:
        while process.poll() is None and time.monotonic()-started<600:
            time.sleep(1)
            p=profile/'logs/game.log';log=p.read_text(encoding='utf-8-sig',errors='replace') if p.exists() else ''
            if PREFIX+' COMPLETE' in log:break
            elapsed=int(time.monotonic()-started)
            if elapsed-last_progress>=30:
                last_progress=elapsed;print(json.dumps(dict(phase='native',elapsed_seconds=elapsed,startup_seen=PREFIX+' STARTUP' in log)),flush=True)
    finally:
        stopped=process.poll() is None
        if stopped:process.terminate()
        try:process.wait(timeout=10)
        except subprocess.TimeoutExpired:process.kill();process.wait()
    errors_path=profile/'logs/error.log';errors=errors_path.read_text(encoding='utf-8-sig',errors='replace') if errors_path.exists() else ''
    passed=[name for name in CHECKS if PREFIX+' PASS '+name in log]
    failed=[name for name in CHECKS if PREFIX+' FAIL '+name in log]
    unrun=[name for name in CHECKS if name not in passed+failed]
    snapshot_drift=[relative for relative,digest in hashes.items() if hashlib.sha256((snapshot/relative).read_bytes()).hexdigest()!=digest]
    source_drift=[relative for relative,digest in hashes.items() if hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()!=digest]
    relevant=[line for line in errors.splitlines() if 'ICW_MD203' in line]
    success=not(failed or unrun or snapshot_drift or source_drift or relevant)
    crashes=sorted((profile/'crashes').glob('*/exception.txt')) if (profile/'crashes').exists() else []
    report=dict(project=PROJECT,status='PASS' if success else ('FAIL_ENGINE_CRASH' if crashes else 'FAIL_INCOMPLETE'),
        native_test_executed=True,native_test=success,success=success,
        engine_version=json.loads((GAME/'launcher-settings.json').read_text(encoding='utf-8-sig'))['rawVersion'],
        profile=str(profile),snapshot=str(snapshot),passed=passed,failed=failed,unrun=unrun,
        frozen_files=len(hashes),snapshot_drift=snapshot_drift,source_drift=source_drift,relevant_fixture_errors=relevant,
        total_error_log_lines=len(errors.splitlines()),full_error_log=str(errors_path),
        crash_exceptions=[str(path) for path in crashes],
        game_log=str(profile/'logs/game.log'),checkpoints=[line for line in log.splitlines() if PREFIX in line],
        elapsed_seconds=round(time.monotonic()-started,1),returncode=process.returncode,stopped_own_probe=stopped,
        scope='Frozen scripts and map, separate unsaved 1970 Israel campaign, day-three startup/economy/feature-preservation smoke checks.',
        limitations=['No manual UI hover, save/reload, first-month, or live multiplayer test.',
            'All engine diagnostics are retained at full_error_log; a successful checkpoint run is not a zero-warning certification.'])
    emit(OUT/'native_report.json',report)
    print(json.dumps({k:report[k] for k in ('success','passed','failed','unrun','frozen_files','elapsed_seconds','total_error_log_lines')}),flush=True)
    raise SystemExit(0 if report['success'] else 1)


if __name__=='__main__':main()
