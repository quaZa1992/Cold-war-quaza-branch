# IMPERIA COLD WAR — Isolated native East Asia, succession and readiness verification.
"""Private E: profile, unchanged user playsets/saves, no live combat or MP claim."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from source import ROOT,REPORT,SNAPSHOT

GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
PROFILE=SNAPSHOT.parent/'native'/time.strftime('%Y%m%d_%H%M%S')
MARK='# IMPERIA COLD WAR — Private East Asia integration engine fixture.\n'
CHECKS=[]


def check(name,condition):
    CHECKS.append(name)
    return f'if = {{ limit = {{ {condition} }} log = "READINESS_PROBE PASS {name}" }} else = {{ log = "READINESS_PROBE FAIL {name}" }}\n'


def fixture():
    # Literal fixture data only, not execution of the donor's process/file writer.
    source=ast.parse((ROOT/'tools/nuclear_readiness/engine_probe.py').read_text(encoding='utf-8'))
    launch=next(n for n in source.body if isinstance(n,ast.FunctionDef) and n.name=='launch')
    assignment=next(n for n in launch.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='fixture' for t in n.targets) and isinstance(n.value,ast.Constant))
    body=ast.literal_eval(assignment.value)
    CHECKS.extend(re.findall(r'READINESS_PROBE PASS ([a-z_]+)',body))
    extra=''
    for tag,leader in (('NKO','Kim Il Sung'),('KOR','Park Chung Hee'),('JAP','Eisaku Sato')):
        extra+=check(tag.lower()+'_authored_tree',f'{tag} = {{ has_focus_tree = COLDWAR_{tag}_1970_focus }}')
        extra+=check(tag.lower()+'_historical_leader',f'{tag} = {{ has_country_leader = {{ name = "{leader}" ruling_only = yes }} }}')
    extra+='NKO = { COLDWAR_NKO_initialize = yes set_country_flag = COLDWAR_EA_ENGINE_death_date COLDWAR_NKO_succession_daily = yes }\n'
    extra+=check('nko_actual_death_and_mourning','NKO = { has_country_flag = COLDWAR_NKO_kim_il_sung_death_recorded has_country_flag = COLDWAR_NKO_succession_pending has_country_leader = { name = "Funeral Committee" ruling_only = yes } NOT = { has_country_leader = { name = "Kim Il Sung" ruling_only = yes } } NOT = { has_country_leader = { name = "Kim Jong-il" ruling_only = yes } } }')
    extra+='NKO = { COLDWAR_NKO_succession_daily = yes set_leader = yes }\n'
    extra+=check('nko_native_router_preserves_mourning','NKO = { has_country_leader = { name = "Funeral Committee" ruling_only = yes } has_country_flag = COLDWAR_NKO_succession_pending }')
    extra+='NKO = { COLDWAR_NKO_install_kim_jong_il = yes }\n'
    extra+=check('nko_successor_selectable','NKO = { has_country_leader = { name = "Kim Jong-il" ruling_only = yes } has_country_flag = COLDWAR_NKO_kim_jong_il_succeeded NOT = { has_country_flag = COLDWAR_NKO_succession_pending } }')
    extra+='NKO = { COLDWAR_NKO_install_kim_jong_il = yes COLDWAR_NKO_succession_daily = yes set_leader = yes }\n'
    extra+=check('nko_successor_cannot_revert','NKO = { has_country_leader = { name = "Kim Jong-il" ruling_only = yes } NOT = { has_country_flag = COLDWAR_NKO_succession_pending } }')
    body=body.replace('log = "READINESS_PROBE START"','log = "READINESS_PROBE START"\n'+extra,1)
    sys.path.insert(0,str(ROOT/'tools/nuclear_readiness'))
    from build import expand
    return MARK+expand(body.replace('COLDWAR_nr_','nr_')).replace('nr_','COLDWAR_nr_').replace('COLDWAR_nr_probe','nr_probe')


def write(relative,text):
    path=PROFILE/relative;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8')


def main():
    integration=json.loads((REPORT/'INTEGRATION.json').read_text(encoding='utf-8'))
    imported=json.loads((REPORT/'INITIAL_IMPORT.json').read_text(encoding='utf-8'))
    inputs={p for p in set(integration['installed'])|set(imported['files']) if p.startswith(('common/','events/','interface/','history/','localisation/english/'))}
    inputs.update(p.relative_to(ROOT).as_posix() for folder in ('common','events','interface','localisation/english') for p in (ROOT/folder).rglob('COLDWAR_NKO_1970_succession*'))
    inputs.update(('gfx/Leaders/NKO/NKO_Coldwar_Kim_Il_Sung.dds','gfx/Leaders/NKO/COLDWAR_NKO_Kim_Il_Sung_memorial.dds','gfx/event_pictures/COLDWAR_NKO_1994_funeral.dds'))
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(inputs)}
    write('mod/base.mod',MARK+(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig')+'\npath="'+ROOT.as_posix()+'"\n')
    addon=MARK+'name="East Asia native verification"\ndependencies={ "MD Cold War" }\npath="'+(PROFILE/'fixture').as_posix()+'"\n'
    write('mod/probe.mod',addon);write('fixture/descriptor.mod',addon)
    write('dlc_load.json',json.dumps({'enabled_mods':['mod/base.mod','mod/probe.mod'],'disabled_dlcs':[]}))
    write('settings.txt',MARK+'language="l_english"\ngraphics={size={x=1280 y=900} fullScreen=no borderless=no}\nmaster_volume=0\n')
    write('fixture/common/on_actions/zz_COLDWAR_EA_ENGINE.txt',MARK+'on_actions = { on_startup = { effect = { USA = { country_event = { id = nr_probe.1 hours = 1 } } } } }')
    write('fixture/events/COLDWAR_EA_ENGINE.txt',fixture())
    # Exercise actual death/leader-routing effects at the 1970 start, rather
    # than waiting 24 campaign years or changing the campaign's real date.
    relative='common/scripted_effects/COLDWAR_NKO_1970_succession_effects.txt'
    text=(ROOT/relative).read_text(encoding='utf-8')
    text=text.replace('NOT = { date < 1994.7.8 }','OR = { NOT = { date < 1994.7.8 } has_country_flag = COLDWAR_EA_ENGINE_death_date }')
    write('fixture/'+relative,text)
    for name in ('game.log','error.log'):write('logs/'+name,'')
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
    started=time.monotonic()
    process=subprocess.Popen([str(GAME/'hoi4.exe'),'-debug','-noasserts','-assertsdialog=no','-userdir='+str(PROFILE),'-start_tag=USA','-start_speed=5'],cwd=GAME,startupinfo=startup)
    print(json.dumps({'project':'IMPERIA COLD WAR','pid':process.pid,'profile':str(PROFILE)}),flush=True)
    try:
        while process.poll() is None and time.monotonic()-started<700:
            time.sleep(1)
            if 'READINESS_PROBE COMPLETE' in (PROFILE/'logs/game.log').read_text(encoding='utf-8-sig',errors='replace'):break
    finally:
        if process.poll() is None:process.terminate()
        try:process.wait(timeout=10)
        except subprocess.TimeoutExpired:process.kill();process.wait()
    game=(PROFILE/'logs/game.log').read_text(encoding='utf-8-sig',errors='replace')
    errors=(PROFILE/'logs/error.log').read_text(encoding='utf-8-sig',errors='replace')
    records=re.split(r'(?=\[\d{2}:\d{2}:\d{2}\]\[)',errors)
    relevant=[r.strip() for r in records if any(x in r for x in ('COLDWAR_NKO','COLDWAR_KOR','COLDWAR_JAP','COLDWAR_nr_','COLDWAR_nuclear_readiness','COLDWAR_nuclear_escalation','COLDWAR_EA_ENGINE','nr_probe.')) and 'Reloading Events:' not in r]
    passed=[n for n in CHECKS if 'READINESS_PROBE PASS '+n in game]
    failed=[n for n in CHECKS if 'READINESS_PROBE FAIL '+n in game]
    result={'project':'IMPERIA COLD WAR','profile':str(PROFILE),'passed':passed,'failed':failed,'unrun':[n for n in CHECKS if n not in passed+failed],
            'relevant_errors':relevant,'completed':'READINESS_PROBE COMPLETE' in game,'source_sha256':hashes,
            'changed_during_run':[p for p,h in hashes.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h],
            'scope':'Native single-client private fixture. Country startup identity/tree loading, death/caretaker/successor routing, readiness transactions and scheduled hourly callback. Private date-authority override tests 1994 succession at a 1970 start. Subsequent ultimatum hours advanced with the actual native helper; nuclear outcome helper invoked directly, no live raid combat, MP transport/OOS, save/rehost or manual hover proof.',
            'elapsed_seconds':round(time.monotonic()-started,1),'process_exit_code':process.returncode,
            'crash_directories':[p.name for p in (PROFILE/'crashes').glob('*') if p.is_dir()]}
    result['success']=result['completed'] and not failed and not result['unrun'] and not relevant and not result['changed_during_run']
    (REPORT/'ENGINE_REPORT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'success':result['success'],'passed':len(passed),'failed':failed,'unrun':result['unrun'],'relevant_error_count':len(relevant),'sample':relevant[:8],'profile':str(PROFILE)}),flush=True)


if __name__=='__main__':main()
