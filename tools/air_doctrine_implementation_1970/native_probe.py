# IMPERIA COLD WAR — Isolated native Air Command selection and mastery checks.
from datetime import datetime,timezone
from pathlib import Path
from collections import defaultdict
import argparse,hashlib,json,os,shutil,subprocess,time
import build
build.sys.path.insert(0,str(build.HERE))
from validate import flat

ROOT,HERE=build.ROOT,build.HERE
BASE=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/air_doctrine_1970')
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
MARKER='# IMPERIA COLD WAR — Private Air Command native test.\n'
PREFIX='ICW_AIR '

def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8',newline='\n')

def trees():
    out=build.outputs()
    grands=dict((k,v) for f in [build.OLD_GRAND,build.NEW_GRAND] for k,_,v in build.parse(out[f]))
    subs=dict((k,v) for f in [build.OLD_SUB,build.NEW_SUB] for k,_,v in build.parse(out[f]))
    return grands,subs

def configs():
    grands,subs=trees(); pending=defaultdict(list); allsubs=defaultdict(list)
    for ident,body in subs.items():
        track=build.get(body,'track'); pending[track].append(ident); allsubs[track].append(ident)
    config=[]
    def add(ident):
        selected=[]
        for _,_,track in build.get(grands[ident],'tracks'):
            candidates=[s for s in pending[track] if s not in selected]
            chosen=candidates[0] if candidates else next(s for s in allsubs[track] if s not in selected)
            selected.append(chosen)
            if chosen in pending[track]: pending[track].remove(chosen)
        config.append((ident,selected))
    for ident in grands: add(ident)
    while any(pending.values()):
        best=max(grands,key=lambda ident:sum(min([v for _,_,v in build.get(grands[ident],'tracks')].count(t),len(s)) for t,s in pending.items()))
        add(best)
    tags=['USA','EGY','AUS','SAF','ENG','FRA','SOV','FIN','SWE','NRY','ARG','POR','ISR','VIE','RAJ','KOR']
    assert len(config)<=len(tags)
    return dict(zip(tags,config))

def passed(name,trigger):
    return ['if = { limit = { '+trigger+' } log = "'+PREFIX+name+'_PASS" }','else = { log = "'+PREFIX+'FAIL '+name+'" }']

def fixture():
    grands,subs=trees(); configuration=configs()
    configure=['log = "ICW_AIR CONFIGURE"']
    # Migrate a deliberately reintroduced legacy hidden spirit twice.
    configure+=['clr_global_flag = mdcw_air_doctrine_migration_v1','FIN = { add_ideas = { '+' '.join(build.integration_baseline()['native_ideas'])+' } }',
                'mdcw_air_doctrine_migrate = yes','mdcw_air_doctrine_migrate = yes']
    configure+=passed('MIGRATION','FIN = { NOT = { '+' '.join('has_idea = '+s for s in build.integration_baseline()['native_ideas'])+' } } has_global_flag = mdcw_air_doctrine_migration_v1')
    # Test actual feature availability with and without an enabled historical RPV.
    configure+=['USA = {']
    # Inspect both gates before granting the technology. The native grant effect
    # does not provide a reliable same-event reversal of a completed technology.
    for sub in ['mdcw_reconnaissance_rpv_operations','mdcw_decoy_rpv_operations']:
        availability=build.emit(build.get(subs[sub],'available'))
        configure+=passed('RPV_GATE_CLOSED_'+sub,'NOT = { AND = { '+' '.join(availability)+' } }')
    configure+=['set_technology = { mdcw_rpv_1964 = 1 popup = no }']
    for sub in ['mdcw_reconnaissance_rpv_operations','mdcw_decoy_rpv_operations']:
        availability=build.emit(build.get(subs[sub],'available'))
        configure+=passed('RPV_GATE_OPEN_'+sub,' '.join(availability))
    configure+=['}']
    for tag,(grand,selected) in configuration.items():
        configure += [tag+' = {','set_technology = { mdcw_rpv_1964 = 1 mdcw_rpv_1978 = 1 drone_1 = 1 drone_2 = 1 suicide_drone_1 = 1 suicide_drone_2 = 1 stealth_tech_1 = 1 }',
                      'set_variable = { num_ships_with_type@carrier = 1 }','set_grand_doctrine = '+grand]
        for index,sub in enumerate(selected): configure+=['set_sub_doctrine = { sub_doctrine = '+sub+' folder = air track = '+str(index)+' }']
        configure+=['add_mastery = { amount = 500 folder = air }','}']
    configure+=['USA = {','add_equipment_to_stockpile = { type = mdcw_recon_rpv_1964_model amount = 11 producer = USA }',
                'add_equipment_to_stockpile = { type = mdcw_recon_rpv_1978_model amount = 13 producer = USA }']
    configure+=passed('RPV_1964_STOCKPILE','has_equipment = { mdcw_recon_rpv_1964_model > 10 }')
    configure+=passed('RPV_1978_STOCKPILE','has_equipment = { mdcw_recon_rpv_1978_model > 12 }')+['}']
    for year in (1964,1978):
        configure+=['USA = { add_equipment_production = { equipment = { type = mdcw_recon_rpv_'+str(year)+'_model creator = USA } requested_factories = 1 progress = 0.99 efficiency = 1 } }']
    configure+=['country_event = { id = ICW_AIR.2 hours = 26 }']
    verify=['log = "ICW_AIR VERIFY"']
    for tag,(grand,selected) in configuration.items():
        verify+=[tag+' = {']+passed('GRAND_'+grand,'has_doctrine = '+grand)
        for sub in selected: verify+=passed('MASTERY_'+sub,'has_completed_subdoctrine = '+sub)
        verify+=passed('NO_HIDDEN_IDEAS_'+tag,'NOT = { '+' '.join('has_idea = '+s for s in build.integration_baseline()['native_ideas'])+' }')
        verify+=['}']
    # Observe each grand's own activation penalty using a grand with no immediate
    # contribution to that field as reference. Native replacement resets tracks.
    for grand,body in grands.items():
        activation=flat(body)
        penalties=build.OLD_DEBUFF_DELTAS.get(grand) or next(i['activation'] for i in build.GRANDS if i['id']==grand)
        field=next(k for k,v in penalties.items() if '.' not in k and (float(v)<0 and not any(s in k for s in ['accident','cost','fuel'])) or ('.' not in k and float(v)>0 and 'cost' in k))
        expected=activation[field]
        reference=next(k for k,v in grands.items() if k!=grand and field not in flat(v))
        verify+=['SAF = {','set_grand_doctrine = '+reference,'set_temp_variable = { ICW_air_before = modifier@'+field+' }',
                 'set_grand_doctrine = '+grand,'set_temp_variable = { ICW_air_delta = modifier@'+field+' }',
                 'subtract_from_temp_variable = { ICW_air_delta = ICW_air_before }']
        verify+=passed('GRAND_PENALTY_'+grand,'check_variable = { ICW_air_delta = '+str(expected)+' }')+['}']
    verify+=['SAF = {','set_grand_doctrine = mdcw_dispersed_air_defence',
             'set_sub_doctrine = { sub_doctrine = mdcw_dispersed_servicing_teams folder = air track = 0 }',
             'set_temp_variable = { ICW_air_before = modifier@airforce_personnel_cost_multiplier_modifier }',
             'set_grand_doctrine = local_airspace_defense',
             'set_temp_variable = { ICW_air_removed = ICW_air_before }',
             'subtract_from_temp_variable = { ICW_air_removed = modifier@airforce_personnel_cost_multiplier_modifier }']
    verify+=passed('SWITCH_CLEANUP','check_variable = { ICW_air_removed = 0.22 }')+['}']
    verify+=['log = "ICW_AIR RUN_COMPLETE"']
    return MARKER+'add_namespace = ICW_AIR\n'+''.join('country_event = { id = ICW_AIR.'+str(i)+' hidden = yes is_triggered_only = yes immediate = {\n'+'\n'.join(rows)+'\n} }\n' for i,rows in [(1,configure),(2,verify)])

def prepare(reuse_snapshot=None):
    run=BASE/datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    assert run.resolve().is_relative_to(BASE.resolve()) and not run.exists()
    snapshot,profile,addon=run/'snapshot',run/'profile',run/'fixture'
    hashes={};overlays={}
    if reuse_snapshot:
        snapshot=Path(reuse_snapshot).resolve()
        assert snapshot.is_relative_to(BASE.resolve()) and snapshot.is_dir()
        hashes=json.loads((snapshot.parent/'snapshot_manifest.json').read_text(encoding='utf-8'))['script_sha256']
        for relative in build.outputs():
            raw=(ROOT/relative).read_bytes()
            target=addon/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
            overlays[relative]=hashlib.sha256(raw).hexdigest()
    for name in ([] if reuse_snapshot else ['common','events','history','interface','localisation','portraits','tutorial','descriptions']):
        source=ROOT/name
        if not source.is_dir() or source.is_junction() or source.is_symlink(): continue
        for current,dirs,files in os.walk(source,followlinks=False):
            dirs[:]=[d for d in dirs if not (Path(current)/d).is_junction() and not (Path(current)/d).is_symlink()]
            relative=Path(current).relative_to(ROOT)
            (snapshot/relative).mkdir(parents=True,exist_ok=True)
            for file in files:
                p=Path(current)/file
                if p.is_symlink(): continue
                shutil.copy2(p,snapshot/relative/file)
                hashes[(relative/file).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
        print('Frozen '+name,flush=True)
    for p in ([] if reuse_snapshot else ROOT.iterdir()):
        if p.is_file() and p.suffix in {'.txt','.mod','.lua'}: shutil.copy2(p,snapshot/p.name)
    for name in ([] if reuse_snapshot else ['gfx','map','sound','music']):
        result=subprocess.run(['cmd.exe','/c','mklink','/J',str(snapshot/name),str(ROOT/name)],capture_output=True,text=True)
        assert result.returncode==0,result.stdout+result.stderr
    descriptor=(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig')
    write(profile/'mod/mdcoldwar.mod',MARKER+descriptor+'\npath="'+snapshot.as_posix()+'"\n')
    desc=MARKER+'name="IMPERIA Air Command probe"\ndependencies={ "MD Cold War" }\npath="'+addon.as_posix()+'"\n'
    write(profile/'mod/probe.mod',desc);write(addon/'descriptor.mod',desc)
    write(profile/'dlc_load.json',json.dumps({'enabled_mods':['mod/mdcoldwar.mod','mod/probe.mod'],'disabled_dlcs':[]}))
    write(profile/'settings.txt',MARKER+'language="l_english"\ngraphics={size={x=1280 y=800} fullScreen=no borderless=no}\nmaster_volume=0\n')
    write(addon/'events/IMPERIA_air_probe.txt',fixture())
    write(addon/'common/on_actions/zzzzzz_IMPERIA_air_probe.txt',MARKER+'on_actions = { on_startup = { effect = { log = "ICW_AIR STARTUP" USA = { country_event = { id = ICW_AIR.1 hours = 2 } } } } }\n')
    record={'project':'IMPERIA COLD WAR','run':str(run),'snapshot':str(snapshot),'profile':str(profile),'script_sha256':hashes,'fixture_runtime_sha256':overlays,'configurations':configs(),'asset_junctions_not_traversed':['gfx','map','sound','music']}
    write(run/'snapshot_manifest.json',json.dumps(record,indent=2)+'\n')
    write(HERE/'native_run_location.json',json.dumps({k:v for k,v in record.items() if k!='script_sha256'},indent=2)+'\n')
    print(json.dumps({'prepared':str(run)}),flush=True)

def run_probe(duration):
    record=json.loads((HERE/'native_run_location.json').read_text(encoding='utf-8'))
    run,profile=Path(record['run']),Path(record['profile'])
    assert run.resolve().is_relative_to(BASE.resolve()) and not (run/'native_result.json').exists()
    startup=subprocess.STARTUPINFO(); startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW; startup.wShowWindow=0
    started=time.monotonic()
    process=subprocess.Popen([str(GAME/'hoi4.exe'),'-noasserts','-assertsdialog=no','-userdir='+str(profile),'-start_tag=USA','-start_speed=5','-hands_off'],cwd=GAME,startupinfo=startup)
    print(json.dumps({'pid':process.pid,'profile':str(profile)}),flush=True)
    observed=[];source=''
    try:
        while process.poll() is None and time.monotonic()-started<duration:
            time.sleep(2)
            path=profile/'logs/game.log';source=path.read_text(encoding='utf-8-sig',errors='replace') if path.exists() else ''
            markers=[line for line in source.splitlines() if PREFIX in line]
            for line in markers[len(observed):]: print(line,flush=True)
            observed=markers
            if PREFIX+'RUN_COMPLETE' in source: break
    finally:
        running=process.poll() is None;exitcode=process.poll()
        if running:
            process.terminate()
            try: process.wait(timeout=15)
            except subprocess.TimeoutExpired: process.kill();process.wait(timeout=10)
    errorpath=profile/'logs/error.log';errors=errorpath.read_text(encoding='utf-8-sig',errors='replace') if errorpath.exists() else ''
    grands,subs=trees()
    needles=['mdcw_air','mdcw_rpv','mdcw_recon_rpv','air_doctrine.txt','subdoctrines/air/air.txt','MD_air_units.txt','ICW_AIR','IMPERIA_air_probe',*grands,*subs]
    relevant=[line for line in errors.splitlines() if any(n in line for n in needles)]
    result={'project':'IMPERIA COLD WAR','pid':process.pid,'profile':str(profile),'elapsed_seconds':round(time.monotonic()-started,1),
            'engine_exit_before_termination':exitcode,'stopped_own_test_process':running,'completed':PREFIX+'RUN_COMPLETE' in source,
            'markers':observed,'failed_markers':[m for m in observed if PREFIX+'FAIL ' in m],'air_related_errors':relevant,'full_error_log':str(errorpath),
            'tested_grands':list(grands),'tested_subdoctrines':list(subs),'multiplayer_test':False,'live_ui_inspected':False}
    write(run/'native_result.json',json.dumps(result,indent=2)+'\n');write(HERE/'native_result.json',json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='markers'},indent=2),flush=True)
    raise SystemExit(not result['completed'] or bool(result['failed_markers']) or bool(relevant))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--prepare',action='store_true');parser.add_argument('--run',action='store_true');parser.add_argument('--duration',type=int,default=420);parser.add_argument('--snapshot')
    args=parser.parse_args()
    if args.prepare: prepare(args.snapshot)
    if args.run: run_probe(args.duration)
