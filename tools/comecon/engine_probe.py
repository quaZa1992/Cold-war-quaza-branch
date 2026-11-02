# IMPERIA COLD WAR — COMECON isolated native-engine transaction checks
import json
import subprocess
import shutil
import hashlib
import sys
import re
import time
from pathlib import Path
from build import ROOT,HERE,MARK

RUNTIME=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/comecon')

def assertion(condition,name):
    return f'if = {{ limit = {{ {condition} }} log = "CC_NATIVE PASS {name}" }} else = {{ log = "CC_NATIVE FAIL {name}" }}'

def main():
    controller=next((a.split('=',1)[1] for a in sys.argv if a.startswith('--controller=')),'SOV')
    assert controller in ('SOV','HUN')
    keep_open='--keep-open' in sys.argv
    minimal_startup='--minimal-startup' in sys.argv
    fast_content='--fast-content' in sys.argv
    game=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
    profile=RUNTIME/('native_'+str(time.time_ns()))
    def put(rel,source):
        p=profile/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(source,encoding='utf-8')
    put('IMPERIA_COLD_WAR_NOTICE.md','IMPERIA COLD WAR: isolated native COMECON checks. Test fixture only. No existing user profile or saves are used.\n')
    # Freeze all script databases, including unrelated work edited in parallel in the workspace.
    # Large art/map directories are read-only asset junctions; COMECON assets are copied below.
    reuse=next((a.split('=',1)[1] for a in sys.argv if a.startswith('--base-snapshot=')),None)
    if reuse:
        assert re.fullmatch(r'native_\d+',reuse)
        frozen=(RUNTIME/reuse/'frozen-main').resolve()
        assert frozen.is_relative_to(RUNTIME.resolve()) and (frozen/'common').is_dir()
    else:
        frozen=profile/'frozen-main';frozen.mkdir(parents=True)
        for name in ('common','events','interface','history','localisation'):
            shutil.copytree(ROOT/name,frozen/name)
    junctions=[]
    for name in (() if reuse else ('gfx','map','music','portraits','sound','tutorial','scenario_tests','descriptions')):
        source=ROOT/name;destination=frozen/name
        if source.is_dir():
            quote=lambda p:"'"+str(p).replace("'","''")+"'"
            command='New-Item -ItemType Junction -Path '+quote(destination)+' -Target '+quote(source)+' | Out-Null'
            subprocess.run(['powershell','-NoProfile','-Command',command],check=True,capture_output=True)
            junctions.append(name)
    for p in (() if reuse else ROOT.iterdir()):
        if p.is_file() and p.suffix in ('.mod','.txt','.lua','.yml','.png'):
            shutil.copyfile(p,frozen/p.name)
    if not reuse:put('frozen-main/IMPERIA_COLD_WAR_NOTICE.md','IMPERIA COLD WAR: frozen script database for an isolated native check. Original notices and credits in copied sources are preserved. Large asset directories are read-only junctions to the existing mod.\n')
    put('mod/mdcoldwar.mod',MARK+' isolated test profile\n'+(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig')+'\npath="'+frozen.as_posix()+'"\n')
    addon=MARK+' native test fixture\nname="IMPERIA COLD WAR COMECON checks"\ndependencies={ "MD Cold War" }\npath="'+(profile/'fixture').as_posix()+'"\n'
    if minimal_startup:addon+='replace_path="common/on_actions"\n'
    if fast_content:addon+='replace_path="common/national_focus"\nreplace_path="common/decisions"\n'
    put('mod/comecon_probe.mod',addon);put('fixture/descriptor.mod',addon)
    put('dlc_load.json',json.dumps({'enabled_mods':['mod/mdcoldwar.mod','mod/comecon_probe.mod'],'disabled_dlcs':[]}))
    put('settings.txt','language="l_english"\ngraphics={size={x=1280 y=900} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n')
    # The engine reads databases in several passes. Freeze this feature before launching.
    manifest=json.loads((HERE/'generated.json').read_text())
    paths=manifest['generated']+manifest['integrations']+[str(p.relative_to(ROOT)).replace('\\','/') for p in (ROOT/'gfx/interface/comecon').glob('*.dds')]+[str(p.relative_to(ROOT)).replace('\\','/') for p in (ROOT/'gfx/fonts/COMECON').glob('*') if p.suffix in ('.fnt','.dds')]
    hashes={}
    for rel in paths:
        if rel.startswith('tools/'):continue
        src=ROOT/rel;dst=profile/'fixture'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
        hashes[rel]=hashlib.sha256(src.read_bytes()).hexdigest()
    put('source-snapshot.json',json.dumps({'project':'IMPERIA COLD WAR','sha256':hashes,'frozen_script_directories':['common','events','interface','history','localisation'],'read_only_asset_junctions':junctions,'reused_baseline':reuse},indent=2))
    put('fixture/common/on_actions/zzzzzzzzzzzz_ICW_COMECON_probe.txt',MARK+' isolated startup assertions\non_actions = { on_startup = { effect = { if = { limit = { NOT = { has_dlc = "La Resistance" } } set_variable = { global.var_missiles_button_x = -57 } } '+controller+' = { cc_probe_run = yes } } } }\n')
    put('fixture/events/ICW_COMECON_probe.txt',MARK+' isolated manual and delayed test entry\nadd_namespace = CC_NATIVE\ncountry_event = { id = CC_NATIVE.1 hidden = yes is_triggered_only = yes immediate = { cc_probe_run = yes } }\n')
    from native_safety_cases import compile_checks
    checks=compile_checks(controller,assertion)
    if '--council' in sys.argv:
        from native_council_cases import compile_cases
        checks=checks.replace('log = "CC_NATIVE COMPLETE"','')+'\n'+compile_cases(controller,assertion)+'\nlog = "CC_NATIVE COMPLETE"'
    if '--council-ui' in sys.argv:
        checks=checks.replace('log = "CC_NATIVE COMPLETE"','')+'\nset_country_flag = cc_open set_variable = { cc_view_tab = 3 } set_variable = { cc_office_page = 0 } set_variable = { cc_ballot_view_round = global.cc_ballot_round } set_variable = { cc_ballot_proposed = THIS.id } set_variable = { global.cc_ballot_open = 1 } set_variable = { global.cc_ballot_days_left = 15 } set_variable = { global.cc_ballot_start_day = global.num_days } '+('DDR' if controller=='HUN' else 'HUN')+' = { add_to_array = { global.cc_ballot_candidates = THIS } } cc_ui_refresh = yes cc_touch = yes log = "CC_NATIVE COMPLETE"'
    ui_effect=''
    if '--council-ui' in sys.argv:
        ai='DDR' if controller=='HUN' else 'HUN'
        ui_effect=MARK+' fixture-only ballot reset for visual interaction\ncc_probe_ui_ballot = { set_variable = { global.cc_ballot_open = 0 } set_variable = { global.cc_ballot_year = global.year } subtract_from_variable = { global.cc_ballot_year = 1 } cc_ballot_begin = yes '+ai+' = { add_to_array = { global.cc_ballot_candidates = THIS } } set_country_flag = cc_open set_variable = { cc_view_tab = 3 } set_variable = { cc_office_page = 0 } set_variable = { cc_office_help = 0 } set_variable = { cc_ballot_view_round = global.cc_ballot_round } cc_ui_refresh = yes cc_touch = yes log = "CC_NATIVE UI_BALLOT_RESET" }\n'
        put('fixture/events/ICW_COMECON_probe.txt',MARK+' isolated test entry\nadd_namespace = CC_NATIVE\ncountry_event = { id = CC_NATIVE.1 hidden = yes is_triggered_only = yes immediate = { cc_probe_run = yes } }\ncountry_event = { id = CC_NATIVE.2 hidden = yes is_triggered_only = yes immediate = { cc_probe_ui_ballot = yes } }\n')
    put('fixture/common/scripted_effects/ICW_COMECON_probe.txt',MARK+' isolated native assertions\ncc_probe_run = { if = { limit = { NOT = { has_country_flag = cc_probe_ran } } set_country_flag = cc_probe_ran\n'+checks+'\n} }\n'+ui_effect)
    args=[str(game/'hoi4.exe'),'-debug','-noasserts','-assertsdialog=no','-userdir='+str(profile),'-start_tag='+controller,'-start_speed=1']
    # Native player control is required by the safety fixture. Never use -hands_off here.
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=1 if keep_open or '--show' in sys.argv else 0
    process=subprocess.Popen(args,cwd=game,startupinfo=startup)
    put('process.json',json.dumps({'project':'IMPERIA COLD WAR','pid':process.pid,'args':args},indent=2))
    print(json.dumps({'pid':process.pid,'profile':str(profile)}),flush=True)
    started=time.time();logs='';ready=False
    try:
        while process.poll() is None and time.time()-started<(1800 if keep_open else 900):
            time.sleep(1)
            p=profile/'logs/game.log'
            if p.exists():logs=p.read_text(encoding='utf-8-sig',errors='replace')
            if 'CC_NATIVE COMPLETE' in logs:
                if not keep_open:break
                if not ready:print('CC_NATIVE READY_FOR_UI',flush=True);ready=True
            if (profile/'STOP').exists():break
    finally:
        if process.poll() is None:process.terminate()
        try:process.wait(timeout=10)
        except subprocess.TimeoutExpired:process.kill();process.wait()
    p=profile/'logs/error.log';errors=p.read_text(encoding='utf-8-sig',errors='replace') if p.exists() else ''
    selected=[line for line in errors.splitlines() if re.search(r'ICW_COMECON|CC_NATIVE|(?<![A-Za-z0-9_])cc_[A-Za-z0-9_]',line,re.I)]
    report={'project':'IMPERIA COLD WAR','profile':str(profile.relative_to(ROOT)),'controller':controller,'process_exit_code':process.returncode,'completed':'CC_NATIVE COMPLETE' in logs,'checks':[l for l in logs.splitlines() if 'CC_NATIVE' in l],'feature_errors':selected,'all_error_lines':len(errors.splitlines()),'elapsed_seconds':round(time.time()-started,1),'minimal_startup':minimal_startup,'fast_content':fast_content,'frozen_script_databases':True,'source_sha256':hashes,'reused_baseline':reuse,'scope':'Isolated native engine and synchronous transaction effects. Minimal startup replaces other on_actions in the fixture only; fast content omits national focus trees and unrelated decisions. Does not prove real calendar, pointer interaction, rehost or live multiplayer.'}
    report['success']=report['completed'] and 'CC_NATIVE FAIL' not in logs and not selected
    out=ROOT/('docs/design/comecon/native-'+('council-' if '--council' in sys.argv else 'safety-')+controller+'.json');out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
