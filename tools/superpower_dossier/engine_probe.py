# IMPERIA COLD WAR — Isolated native dossier integration and metadata assertions
import hashlib
import json
import re
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
MARK='# IMPERIA COLD WAR — Superpower dossier native probe\n'


def main():
    profile=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/superpower_dossier')/('native_'+str(time.time_ns()))
    snapshot=profile/'snapshot'
    snapshot.mkdir(parents=True)
    def put(rel,source):
        p=profile/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(source,encoding='utf-8',newline='\n')
    assets=HERE/'asset_provider'
    assert all((assets/name).is_dir() for name in ('gfx','map','sound','music')), 'Current asset-only junction provider is required.'
    assert all(not (assets/name).exists() for name in ('common','events','history','interface','localisation')), 'Asset cache contains runtime code.'
    put('IMPERIA_COLD_WAR_NOTICE.md','IMPERIA COLD WAR: disposable isolated native dossier test. Runtime code and private dossier art/fonts are copied into a snapshot. A task-owned assets-only provider reads current workspace assets through four directory junctions. No writes to those junctions, normal profiles, user saves or source assets occur.\n')
    # Freeze code to avoid another chat's live edits triggering debug database reloads.
    runtime=('common','events','history','interface','localisation','portraits','descriptions','tutorial','scenario_tests')
    for folder in runtime:
        shutil.copytree(ROOT/folder,snapshot/folder)
    shutil.copytree(ROOT/'gfx/interface/superpower_dossier',snapshot/'gfx/interface/superpower_dossier')
    shutil.copytree(ROOT/'gfx/fonts/superpower_dossier',snapshot/'gfx/fonts/superpower_dossier')
    for item in ROOT.iterdir():
        if item.is_file() and item.suffix in ('.mod','.txt','.json'):
            shutil.copyfile(item,snapshot/item.name)
    masks=re.findall(r'^\s*replace_path\s*=\s*"([^"]+)"',(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig'),re.M)
    provider=MARK+'name="IMPERIA dossier current asset provider"\nsupported_version="1.19.*"\n'+''.join('replace_path="'+p+'"\n' for p in masks if p.strip('/').split('/')[0] in ('gfx','map','sound','music'))+'path="'+assets.as_posix()+'"\n'
    put('mod/assets.mod',provider)
    overlay=MARK+'name="IMPERIA COLD WAR dossier native snapshot"\ndependencies={ "IMPERIA dossier current asset provider" }\n'
    overlay+=''.join('replace_path="'+p+'"\n' for p in masks if p.strip('/').split('/')[0] in runtime)
    overlay+='path="'+snapshot.as_posix()+'"\n'
    put('mod/dossier.mod',overlay)
    (snapshot/'descriptor.mod').write_text(overlay,encoding='utf-8')
    put('dlc_load.json',json.dumps({'enabled_mods':['mod/assets.mod','mod/dossier.mod'],'disabled_dlcs':[]}))
    put('settings.txt','language="l_english"\ngraphics={size={x=1280 y=900} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n')
    if '--treaties' in sys.argv:
        from treaty_native_fixture import source
    else:
        from native_fixture import source
    (snapshot/'common/scripted_effects/zzzz_ICSD_probe.txt').write_text(MARK+source(),encoding='utf-8')
    (snapshot/'events/ICSD_probe.txt').write_text(MARK+'add_namespace = icsd_probe\ncountry_event = { id = icsd_probe.1 hidden = yes is_triggered_only = yes immediate = { icsd_probe_run = yes } }\n',encoding='utf-8')
    (snapshot/'common/on_actions/zzzzzzzzzzzz_ICSD_probe.txt').write_text(MARK+'on_actions = { on_startup = { effect = { USA = { country_event = { id = icsd_probe.1 } } } } }\n',encoding='utf-8')
    manifest=json.loads((HERE/'generated.json').read_text())
    frozen={rel:hashlib.sha256((snapshot/rel).read_bytes()).hexdigest() for rel in manifest['generated']+manifest['integrations']}
    put('source-snapshot.json',json.dumps({'project':'IMPERIA COLD WAR','sha256':frozen},indent=2))
    args=[str(GAME/'hoi4.exe'),'-crash_data_log','-noasserts','-assertsdialog=no','-userdir='+str(profile),'-start_tag=USA','-start_speed=1']
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
    process=subprocess.Popen(args,cwd=GAME,startupinfo=startup)
    put('process.json',json.dumps({'project':'IMPERIA COLD WAR','pid':process.pid,'args':args},indent=2))
    print(json.dumps({'pid':process.pid,'profile':str(profile),'snapshot':str(snapshot)}),flush=True)
    started=time.time();logs='';complete=False
    try:
        while process.poll() is None and time.time()-started<900:
            time.sleep(1)
            logfile=profile/'logs/game.log'
            if logfile.exists():logs=logfile.read_text(encoding='utf-8-sig',errors='replace')
            if 'ICSD_NATIVE COMPLETE' in logs:
                complete=True
                if '--keep-open' not in sys.argv:break
            if (profile/'STOP').exists():break
    finally:
        if process.poll() is None:process.terminate()
        try:process.wait(timeout=10)
        except subprocess.TimeoutExpired:process.kill();process.wait()
    p=profile/'logs/error.log';errors=p.read_text(encoding='utf-8-sig',errors='replace') if p.exists() else ''
    selected=[line for line in errors.splitlines() if re.search(r'\b(?:icsd|icwt)_\w+|ICW_superpower|[/\\]superpower_dossier[/\\]|Token (?:nuclear_missile_equipment|nuclear_ballistic_missile_equipment|ballistic_missile_equipment|guided_missile_equipment)_\d+ is a dynamic token',line,re.I)]
    report={'project':'IMPERIA COLD WAR','completed':complete,'profile':str(profile.relative_to(ROOT)),'elapsed_seconds':round(time.time()-started,2),'checks':[l for l in logs.splitlines() if 'ICSD_NATIVE' in l],'feature_errors':selected,'all_error_lines':len(errors.splitlines()),'snapshot_unchanged':all(hashlib.sha256((snapshot/rel).read_bytes()).hexdigest()==h for rel,h in frozen.items()),'multiplayer_tested':False,'scope':'Isolated native scenario startup and synchronous observer/UI-state assertions. No real network or pointer test.'}
    report['success']=complete and 'ICSD_NATIVE FAIL' not in logs and not selected
    report['process_returncode']=process.returncode
    report['named_checks']=[{'status':status,'name':name} for status,name in re.findall(r'ICSD_NATIVE (PASS|FAIL|INFO)\s+(\w+)',logs)]
    if (profile/'ui-reload.json').exists():
        report['ui_reload_stage']=json.loads((profile/'ui-reload.json').read_text(encoding='utf-8'))
        report['scope']='Original frozen backend native assertions, followed by preserved GUI-only source changes. Final UI activation must be recorded separately; not multiplayer.'
    (HERE/'native_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
