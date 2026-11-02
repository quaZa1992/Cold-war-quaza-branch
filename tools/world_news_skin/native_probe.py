# IMPERIA COLD WAR — Isolated World Ledger native UI probe.
"""Explicit E: profile only. Never modifies saves, playsets or an existing game."""
from pathlib import Path
import argparse
import datetime
import hashlib
import importlib.util
import json
import re
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
BASE=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/world_ledger')
PRIOR=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/israel_v2/20261029_182301_643193/probe_manifest.json')
MARK='# IMPERIA COLD WAR — Private World Ledger UI fixture.\n'

def write(base,relative,raw):
    p=base/relative;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(raw if isinstance(raw,bytes) else raw.encode('utf-8'));return p
def dump(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
def hidden():
    s=subprocess.STARTUPINFO();s.dwFlags|=subprocess.STARTF_USESHOWWINDOW;s.wShowWindow=0;return s
def private(path):
    p=path.resolve();assert p!=BASE.resolve() and p.is_relative_to(BASE.resolve());return p
def active():
    r=subprocess.run(['powershell','-NoProfile','-Command','Get-Process hoi4 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True,startupinfo=hidden(),creationflags=subprocess.CREATE_NO_WINDOW)
    return [int(v) for v in r.stdout.split() if v.isdigit()]

def prepare():
    spec=importlib.util.spec_from_file_location('news_skin',HERE/'build.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    payload,report=m.build()
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    run=private(BASE/stamp);run.mkdir(parents=True,exist_ok=False);profile=run/'profile';fixture=profile/'fixture'
    parent=json.loads(PRIOR.read_text(encoding='utf-8'));snapshot=Path(parent['snapshot']);assert snapshot.is_dir()
    descriptor=(snapshot/'descriptor.mod').read_text(encoding='utf-8-sig')
    name=re.search(r'(?m)^name\s*=\s*"([^"]+)"',descriptor)[1]
    descriptor=re.sub(r'(?m)^path\s*=.*\n?','',descriptor)
    write(profile,'mod/base.mod',descriptor+'\npath="'+snapshot.as_posix()+'"\n')
    addon=MARK+'name="IMPERIA World Ledger UI Probe"\ndependencies={ "'+name+'" }\npath="'+fixture.as_posix()+'"\n'
    write(profile,'mod/probe.mod',addon);write(fixture,'descriptor.mod',addon)
    for relative,raw in payload.items():write(fixture,relative,raw)
    for relative in ['interface/ISR2_news_art.gfx','gfx/event_pictures/ISR2/news_settlers_1970s.dds']:
        write(fixture,relative,(ROOT/relative).read_bytes())
    lead=('Israeli settlers have attacked Palestinian residents in the West Bank, causing civilian casualties. '
          'The incident has deepened tensions around the settlements and placed the conduct of armed civilian groups under scrutiny. '
          'The military administration faces pressure to protect residents, enforce public order and maintain security for the settlements.')
    events=[MARK+'add_namespace = ICW_NEWS_UI\n']
    for i in (1,2,3):
        options=[]
        count=4 if i==3 else 1
        for n in range(1,count+1):
            follow='country_event = { id = ICW_NEWS_UI.4 }' if i==3 else 'news_event = { id = ICW_NEWS_UI.'+str(i+1)+' }'
            options.append('option = { name = ICW_NEWS_UI.'+str(i)+'.'+str(n)+' hidden_effect = { log = "ICW_NEWS_UI CHOICE '+str(i)+'.'+str(n)+'" '+follow+' } }')
        events.append('news_event = { id = ICW_NEWS_UI.'+str(i)+' title = ICW_NEWS_UI.'+str(i)+'.t desc = ICW_NEWS_UI.'+str(i)+'.d picture = GFX_ISR2_news_settlers_1970s is_triggered_only = yes major = yes immediate = { log = "ICW_NEWS_UI SHOWN_'+str(i)+'" }\n'+'\n'.join(options)+'\n}\n')
    events.append('country_event = { id = ICW_NEWS_UI.4 title = ICW_NEWS_UI.4.t desc = ICW_NEWS_UI.4.d picture = GFX_israeli_government_event is_triggered_only = yes immediate = { log = "ICW_NEWS_UI COUNTRY_REFERENCE" } option = { name = ICW_NEWS_UI.4.1 log = "ICW_NEWS_UI COMPLETE" } }')
    write(fixture,'events/ICW_NEWS_UI.txt','\n'.join(events))
    write(fixture,'common/on_actions/zzzz_ICW_NEWS_UI.txt',MARK+'on_actions = { on_startup = { effect = { log = "ICW_NEWS_UI STARTUP" ENG = { news_event = { id = ICW_NEWS_UI.1 days = 1 } } } } }\n')
    loc=['l_english:',MARK.strip(),
         ' ICW_NEWS_UI.1.t: "Settler Violence in the West Bank"',
         ' ICW_NEWS_UI.1.d: "'+lead+'"',
         ' ICW_NEWS_UI.1.1: "Read the next report."',
         ' ICW_NEWS_UI.2.t: "A Prolonged Political Dispute over the Administration and Security of the Occupied Territories Raises Further Questions about Policy"',
         ' ICW_NEWS_UI.2.d: "'+('\\n\\n'.join([lead]*8))+'\\n\\nFINAL DISPATCH PARAGRAPH. The complete report remains available through the native text scrollbar."',
         ' ICW_NEWS_UI.2.1: "Proceed to the response list."',
         ' ICW_NEWS_UI.3.t: "Four Native Response Options"',
         ' ICW_NEWS_UI.3.d: "The private layout check presents four native options. The final entry must remain reachable. No actual country programme or agreement is changed by this private fixture."',
         ' ICW_NEWS_UI.4.t: "Ordinary Country Event Reference"',
         ' ICW_NEWS_UI.4.d: "This ordinary country-event frame and its native options are retained unchanged by the world-news skin. This is an isolated interface fixture."',
         ' ICW_NEWS_UI.4.1: "Complete the interface check."']
    for n in range(1,5):loc.append(' ICW_NEWS_UI.3.'+str(n)+': "'+('First response.','Second response.','Third response.','Fourth response: final visible entry.')[n-1]+'"')
    write(fixture,'localisation/english/ICW_NEWS_UI_l_english.yml',b'\xef\xbb\xbf'+('\n'.join(loc)+'\n').encode('utf-8'))
    write(profile,'dlc_load.json',json.dumps(dict(enabled_mods=['mod/base.mod','mod/probe.mod'],disabled_dlcs=[])))
    write(profile,'settings.txt',MARK+'language="l_english"\ngraphics={size={x=1440 y=1080} min_gui={x=1280 y=720} gui_scale=1.000000 fullScreen=no borderless=no}\nmaster_volume=0\n')
    manifest=dict(project='IMPERIA COLD WAR',status='PREPARED',profile=str(profile),fixture=str(fixture),snapshot=str(snapshot),
                  source_gui_sha256=report['source_gui_sha256'],payload=report['files'],native_ui_tested=False,
                  checks=['short news','long title','long scrollable description','four options including final entry','minimize and reopen','ordinary country-event reference'])
    dump(run/'manifest.json',manifest)
    print(json.dumps(dict(project='IMPERIA COLD WAR',status='PREPARED',run=str(run),files=len(payload))),flush=True)
    return run

def launch(run):
    run=private(run);m=json.loads((run/'manifest.json').read_text());assert m['status']=='PREPARED'
    # A separate userdir keeps user settings, playsets and saves isolated.
    # Existing games are recorded and never stopped, paused or controlled.
    existing=active()
    p=subprocess.Popen([str(GAME/'hoi4.exe'),'-debug','-noasserts','-assertsdialog=no','-userdir='+m['profile'],'-start_tag=ENG','-start_speed=2','-hands_off'],cwd=GAME,startupinfo=hidden(),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    assert p.pid not in existing
    m.update(status='RUNNING',pid=p.pid,untouched_existing_processes=existing);dump(run/'manifest.json',m)
    print(json.dumps(dict(project='IMPERIA COLD WAR',status='RUNNING',pid=p.pid,run=str(run))),flush=True)
    # Keep the owning exec job alive while the interactive private process runs.
    # Returning immediately can let the host clean up the launched child.
    try:
        p.wait(timeout=1200)
    except subprocess.TimeoutExpired:
        p.terminate();p.wait(timeout=15)
    m['status']='EXITED';m['exit_code']=p.returncode;dump(run/'manifest.json',m)
    print(json.dumps(dict(project='IMPERIA COLD WAR',status='EXITED',exit_code=p.returncode,run=str(run))),flush=True)

def stop(run):
    run=private(run);m=json.loads((run/'manifest.json').read_text());assert m.get('pid')
    # Stop only the exact private process created above, never another game.
    query='(Get-CimInstance Win32_Process -Filter "ProcessId = '+str(int(m['pid']))+'").CommandLine'
    r=subprocess.run(['powershell','-NoProfile','-Command',query],capture_output=True,text=True,startupinfo=hidden(),creationflags=subprocess.CREATE_NO_WINDOW)
    if r.stdout.strip():
        assert m['profile'].lower() in r.stdout.lower(),'Process identity changed'
        subprocess.run(['taskkill','/PID',str(m['pid']),'/F'],check=True,capture_output=True,startupinfo=hidden(),creationflags=subprocess.CREATE_NO_WINDOW)
    m['status']='STOPPED';dump(run/'manifest.json',m)
    print(json.dumps(dict(project='IMPERIA COLD WAR',status='STOPPED',run=str(run))))

def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--prepare',action='store_true');g.add_argument('--launch',type=Path);g.add_argument('--stop',type=Path)
    a=p.parse_args()
    if a.prepare:prepare()
    elif a.launch:launch(a.launch)
    else:stop(a.stop)
if __name__=='__main__':main()
