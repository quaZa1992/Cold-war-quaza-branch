# IMPERIA CW — Cold War: iraq 1970 — engine check.
"""Isolated, bounded engine loader check; never alters the user's playset."""
from pathlib import Path
import subprocess,time,json,re,os,hashlib

ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
def main():
    folder=HERE/'engine_run';(folder/'mod').mkdir(parents=True,exist_ok=True)
    (folder/'.gitignore').write_text('*\n',encoding='utf-8')
    descriptor=(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig')+'\npath="'+ROOT.as_posix()+'"\n'
    (folder/'mod/mdcoldwar.mod').write_text(descriptor,encoding='utf-8')
    (folder/'dlc_load.json').write_text(json.dumps({'enabled_mods':['mod/mdcoldwar.mod'],'disabled_dlcs':[]}),encoding='utf-8')
    (folder/'settings.txt').write_text('language="l_english"\ngraphics={ size={x=1280 y=720} fullScreen=no borderless=no }\nmaster_volume=0\n',encoding='utf-8')
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
    manifest_hash=hashlib.sha256((HERE/'manifest.json').read_bytes()).hexdigest()
    started=time.time();p=subprocess.Popen([str(GAME/'hoi4.exe'),'-debug','-userdir='+str(folder)],cwd=GAME,startupinfo=startup)
    print(json.dumps({'pid':p.pid,'isolated_userdir':str(folder)}),flush=True)
    stopped=False
    while p.poll() is None and time.time()-started<240:
        time.sleep(1)
        setup=folder/'logs/setup.log';errorfile=folder/'logs/error.log'
        # Reaching the main menu is enough for a content loader check. Actual
        # 1970 gameplay/hover/save/network behavior still requires a live test.
        errors=errorfile.read_text(encoding='utf-8-sig',errors='replace') if errorfile.exists() else ''
        parsed_scripts='gameitemdatabase.h' in errors and 'scripted_effects/' in errors
        if parsed_scripts and setup.exists() and time.time()-setup.stat().st_mtime>15 and time.time()-started>100:
            p.terminate();stopped=True;break
    if p.poll() is None:p.terminate();stopped=True
    try:p.wait(timeout=10)
    except subprocess.TimeoutExpired:p.kill();p.wait()
    logs=folder/'logs';errors=(logs/'error.log').read_text(encoding='utf-8-sig',errors='replace') if (logs/'error.log').exists() else ''
    lines=errors.splitlines();relevant=[]
    for i,line in enumerate(lines):
        if any(k in line for k in ['COLDWAR_IRQ_','COLDWAR_USA_gulf_']):relevant.extend(lines[max(0,i-1):min(len(lines),i+3)])
    relevant=list(dict.fromkeys(relevant))
    report={'scope':'Isolated engine content-loader attempt; no live 1970, hover, save/reload or multiplayer test','manifest_sha256_at_start':manifest_hash,'manifest_unchanged':hashlib.sha256((HERE/'manifest.json').read_bytes()).hexdigest()==manifest_hash,'returncode':p.returncode,'stopped_after_loader_window':stopped,'elapsed_seconds':round(time.time()-started,1),'logs_created':logs.exists(),'script_database_reached':'scripted_effects/' in errors,'relevant_error_lines':relevant,'total_error_lines':len(lines)}
    (HERE/'ENGINE_REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
