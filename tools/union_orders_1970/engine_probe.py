# IMPERIA COLD WAR — Isolated native order, stock-transfer and timer probe on E:.
"""Private addon only. Never edits user saves, playsets, or source controller rules."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
PROFILE=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/union_orders_1970')/time.strftime('%Y%m%d_%H%M%S')
P='COLDWAR_ORD_'
NS=P+'ENGINE'
EXPECTED=[]
MARK='# IMPERIA COLD WAR — Private annual-order engine fixture.'


def check(name,condition):
    EXPECTED.append(name)
    return 'if = { limit = { '+condition+' } log = "'+NS+' PASS '+name+'" } else = { log = "'+NS+' FAIL '+name+'" }\n'


def event(number,body):
    return 'country_event = { id = '+NS+'.'+str(number)+' hidden = yes is_triggered_only = yes immediate = {\n'+body+'\n} }\n'


def choose(family,amount=300,kind=1,fraction=0):
    from catalogue import IDS
    return f'''set_variable = {{ {P}draft_target = UKR.id }}
set_variable = {{ {P}draft_family = {IDS[family]} }}
set_variable = {{ {P}draft_quantity = {amount} }}
set_variable = {{ {P}draft_kind = {kind} }}
set_variable = {{ {P}draft_fraction = {fraction:.5f} }}
{P}commit_draft = yes
'''


def fixture():
    from catalogue import IDS
    first=f'''{P}bootstrap = yes
set_country_flag = {NS}_human
UKR = {{ set_country_flag = {NS}_human set_variable = {{ treasury = 100 }} }}
set_variable = {{ treasury = 100 }}
set_variable = {{ gdp_total = 1000 }}
'''
    first+=check('ukraine_actual_ssr','UKR = { '+P+'republic = yes }')
    first+=choose('mbt',300,1,.0005)
    first+=check('direct_order_native_year','UKR = { check_variable = { '+P+'mbt_state = 2 } has_country_flag = '+P+'window_mbt }')
    first+=check('native_year_length','UKR = { check_variable = { days_mission_timeout@'+P+'window_mbt > 364 } }')
    first+=check('soviet_support_paid_once','check_variable = { var = treasury value = 99.5 compare = equals }')
    first+=check('republic_support_received','UKR = { check_variable = { var = treasury value = 100.5 compare = equals } }')
    first+='UKR = { '+P+'succeed_mbt = yes }\n'
    first+=check('uncertified_order_not_fulfilled','UKR = { check_variable = { '+P+'mbt_state = 2 } } NOT = { has_idea = '+P+'successful_mbt }')
    first+=f'set_variable = {{ {P}return_target = UKR.id }}\nset_variable = {{ {P}return_family = {IDS["mbt"]} }}\nset_variable = {{ {P}return_serial = UKR.{P}mbt_serial }}\nadd_to_variable = {{ {P}return_serial = 1 }}\n'
    first+='UKR = { set_country_flag = '+P+'mbt_return_pending '+P+'certify_mbt = yes }\n'
    first+=check('stale_native_production_review_blocked','UKR = { check_variable = { '+P+'mbt_state = 2 } } NOT = { has_idea = '+P+'successful_mbt }')
    first+=f'set_variable = {{ {P}return_serial = UKR.{P}mbt_serial }}\n'
    first+='UKR = { set_country_flag = '+P+'mbt_return_pending '+P+'certify_mbt = yes }\n'
    first+=check('native_certified_programme','has_idea = '+P+'successful_mbt UKR = { has_idea = '+P+'successful_mbt check_variable = { '+P+'mbt_state = 3 } }')
    first+=check('native_success_clock_180','check_variable = { days_mission_timeout@'+P+'success_clock_mbt > 179 }')
    first+=choose('mbt',900,1,.002)
    first+=check('duplicate_does_not_pay','check_variable = { var = treasury value = 99.5 compare = equals } UKR = { check_variable = { '+P+'mbt_quantity = 300 } }')
    first+=choose('rifles',100,2)
    first+='UKR = { add_equipment_to_stockpile = { type = infantry_weapons_type amount = 100 producer = UKR } set_variable = { '+NS+'_stock_before = num_equipment@infantry_weapons_type } }\n'
    first+='set_variable = { '+NS+'_stock_before = num_equipment@infantry_weapons_type }\n'
    first+='UKR = { '+P+'deliver_rifles = yes }\n'
    first+='set_variable = { '+NS+'_stock_delta = num_equipment@infantry_weapons_type } subtract_from_variable = { '+NS+'_stock_delta = '+NS+'_stock_before }\n'
    first+=check('real_equipment_arrives','check_variable = { var = '+NS+'_stock_delta value = 100 compare = equals }')
    first+=check('delivery_record_matches_native_transfer','UKR = { check_variable = { '+P+'rifles_delivered = 100 } check_variable = { '+P+'rifles_state = 3 } }')
    first+='UKR = { '+P+'deliver_rifles = yes }\n'
    first+='set_variable = { '+NS+'_stock_delta = num_equipment@infantry_weapons_type } subtract_from_variable = { '+NS+'_stock_delta = '+NS+'_stock_before }\n'
    first+=check('delivery_cannot_repeat','check_variable = { var = '+NS+'_stock_delta value = 100 compare = equals }')
    # Actual AI control remains true in hands-off mode. Fixture flags only allow
    # exercising human-authority transactions without a second network client.
    first+='UKR = { clr_country_flag = '+NS+'_human }\n'+choose('towed_artillery')
    first+=check('native_ai_advisory','UKR = { is_ai = yes check_variable = { '+P+'towed_artillery_state = 6 } }')
    first+='UKR = { '+P+'close_towed_artillery = yes }\n'
    first+=check('native_ai_closes_harmlessly','NOT = { has_idea = '+P+'unfulfilled_towed_artillery } NOT = { has_idea = '+P+'shortfall }')
    first+='UKR = { set_country_flag = '+NS+'_human }\n'+choose('apc')
    first+='UKR = { clr_country_flag = '+NS+'_human '+P+'daily = yes }\n'
    first+=check('native_ai_takeover_neutral','UKR = { check_variable = { '+P+'apc_state = 5 } }')
    first+='UKR = { set_country_flag = '+NS+'_human '+P+'daily = yes '+P+'close_apc = yes }\n'
    first+=check('native_human_return_does_not_inherit_penalty','NOT = { has_idea = '+P+'unfulfilled_apc } NOT = { has_idea = '+P+'shortfall }')
    first+=choose('light_at')
    first+='UKR = { add_days_mission_timeout = { mission = '+P+'window_light_at days = -364 } add_days_mission_timeout = { mission = '+P+'objective_light_at days = -364 } country_event = { id = '+NS+'.10 } }\n'
    first+='add_days_mission_timeout = { mission = '+P+'success_clock_mbt days = -179 }\n'
    first+='country_event = { id = '+NS+'.2 days = 2 }\n'
    proposal=choose('civilian',1,3)
    proposal+=check('native_republic_proposal','check_variable = { '+P+'civilian_state = 1 } NOT = { has_active_mission = '+P+'window_civilian }')
    proposal+=f'SOV = {{ set_variable = {{ {P}review_target = UKR.id }} {P}snapshot_proposals = yes }}\n'
    proposal+=check('native_proposal_review_copies_serial','SOV = { check_variable = { '+P+'review_serial_civilian = PREV.'+P+'civilian_serial } }')
    proposal+=P+'reject_civilian = yes\n'+choose('civilian',1,3)
    proposal+=check('native_replacement_has_new_serial','check_variable = { var = '+P+'civilian_serial value = SOV.'+P+'review_serial_civilian compare = greater_than }')
    second=check('native_background_clocks_advance','UKR = { check_variable = { days_mission_timeout@'+P+'window_mbt < 365 } check_variable = { days_mission_timeout@'+P+'window_mbt > 360 } } check_variable = { days_mission_timeout@'+P+'success_clock_rifles < 180 } check_variable = { days_mission_timeout@'+P+'success_clock_rifles > 175 }')
    second+=check('native_failure_programme','has_idea = '+P+'unfulfilled_light_at has_idea = '+P+'shortfall')
    second+=check('native_failure_clock_180','check_variable = { days_mission_timeout@'+P+'failure_clock_light_at > 177 }')
    second+=check('success_clock_expiry_removes_both_spirits','NOT = { has_idea = '+P+'successful_mbt } UKR = { NOT = { has_idea = '+P+'successful_mbt } }')
    second+=check('pending_survives_daily','UKR = { check_variable = { '+P+'civilian_state = 1 } }')
    second+='UKR = { '+P+'approve_civilian = yes '+P+'reject_civilian = yes }\n'
    second+=check('stale_native_proposal_review_blocked','UKR = { check_variable = { '+P+'civilian_state = 1 } }')
    second+=f'set_variable = {{ {P}review_target = UKR.id }}\n{P}snapshot_proposals = yes\n'
    second+='UKR = { '+P+'approve_civilian = yes capital_scope = { add_extra_state_shared_building_slots = 1 add_building_construction = { type = industrial_complex level = 1 instant_build = yes } } '+P+'daily = yes }\n'
    second+=check('native_processing_building_counts_recipient','UKR = { check_variable = { '+P+'civilian_state = 3 } } has_idea = '+P+'successful_civilian')
    second+='log = "'+NS+' DIAG sov_treasury=[?treasury] civilian_state=[?UKR.'+P+'civilian_state] baseline=[?UKR.'+P+'civilian_baseline0] target=[?UKR.'+P+'civilian_target0] current=[?UKR.'+P+'civilian_current0] mbt_days=[?UKR.days_mission_timeout@'+P+'window_mbt] rifles_clock=[?days_mission_timeout@'+P+'success_clock_rifles]"\n'
    second+='UKR = { set_variable = { '+NS+'_old_shortfall = COLDWAR_UNI_sf_pts } COLDWAR_UNI_target_failed = yes }\n'
    second+=check('legacy_failure_blocked','UKR = { check_variable = { var = COLDWAR_UNI_sf_pts value = '+NS+'_old_shortfall compare = equals } }')
    second+='add_days_mission_timeout = { mission = '+P+'failure_clock_light_at days = -179 }\nadd_days_mission_timeout = { mission = '+P+'shortfall_clock days = -179 }\ncountry_event = { id = '+NS+'.3 days = 2 }\n'
    third=check('failure_and_consumer_goods_expire','NOT = { has_idea = '+P+'unfulfilled_light_at } NOT = { has_idea = '+P+'shortfall } UKR = { NOT = { has_idea = '+P+'shortfall } }')
    third+='log = "'+NS+' COMPLETE"\n'
    return MARK+'\nadd_namespace = '+NS+'\n'+event(1,first)+event(10,proposal)+event(2,second)+event(3,third)


def write(relative,body):
    path=PROFILE/relative;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(body,encoding='utf-8')


def main():
    manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
    inputs={p:d for p,d in manifest['outputs'].items() if Path(p).suffix in {'.txt','.yml'}}
    private={}
    for relative,digest in inputs.items():
        source=ROOT/relative;destination=PROFILE/'fixture'/relative
        destination.parent.mkdir(parents=True,exist_ok=True);raw=source.read_bytes()
        if relative=='common/scripted_triggers/COLDWAR_UNION_orders.txt':
            text=raw.decode('utf-8')
            text,n=re.subn(r'COLDWAR_ORD_human_country\s*=\s*\{\s*is_ai = no\s*\}',P+'human_country = { OR = { is_ai = no has_country_flag = '+NS+'_human } }',text)
            assert n==1
            raw=text.encode('utf-8')
        destination.write_bytes(raw);private[relative]=hashlib.sha256(raw).hexdigest()
    write('.gitignore',MARK+'\n*\n')
    write('mod/mdcoldwar.mod',MARK+'\n'+(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig')+'\npath="'+ROOT.as_posix()+'"\n')
    addon=MARK+'\nname="Annual Union orders native probe"\ndependencies={ "MD Cold War" }\npath="'+(PROFILE/'fixture').as_posix()+'"\n'
    write('mod/orders_probe.mod',addon);write('fixture/descriptor.mod',addon)
    write('dlc_load.json',json.dumps({'enabled_mods':['mod/mdcoldwar.mod','mod/orders_probe.mod'],'disabled_dlcs':[]}))
    write('settings.txt',MARK+'\nlanguage="l_english"\ngraphics={size={x=1280 y=900} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n')
    write('fixture/events/'+NS+'.txt',fixture())
    write('fixture/common/on_actions/zzzz_'+NS+'.txt',MARK+'\non_actions = { on_startup = { effect = { SOV = { country_event = { id = '+NS+'.1 } } } } }')
    for name in ('game.log','error.log'):write('logs/'+name,'')
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
    args=[str(GAME/'hoi4.exe'),'-debug','-noasserts','-assertsdialog=no','-userdir='+str(PROFILE),'-start_tag=SOV','-start_speed=5','-hands_off']
    started=time.monotonic();process=subprocess.Popen(args,cwd=GAME,startupinfo=startup)
    print(json.dumps({'project':'IMPERIA COLD WAR','pid':process.pid,'profile':str(PROFILE)}),flush=True)
    try:
        while process.poll() is None and time.monotonic()-started<700:
            time.sleep(1)
            log=PROFILE/'logs/game.log'
            if log.exists() and NS+' COMPLETE' in log.read_text(encoding='utf-8-sig',errors='replace'):break
    finally:
        if process.poll() is None:process.terminate()
        try:process.wait(timeout=10)
        except subprocess.TimeoutExpired:process.kill();process.wait()
    game=(PROFILE/'logs/game.log').read_text(encoding='utf-8-sig',errors='replace')
    errors=(PROFILE/'logs/error.log').read_text(encoding='utf-8-sig',errors='replace')
    records=re.split(r'(?=\[\d{2}:\d{2}:\d{2}\]\[)',errors)
    own=[r.strip() for r in records if ('COLDWAR_ORD' in r or 'COLDWAR_UNION_orders' in r) and 'Reloading Events:' not in r]
    passed=[n for n in EXPECTED if NS+' PASS '+n in game];failed=[n for n in EXPECTED if NS+' FAIL '+n in game]
    unrun=[n for n in EXPECTED if n not in passed+failed]
    report={'project':'IMPERIA COLD WAR','profile':str(PROFILE),'passed':passed,'failed':failed,'unrun':unrun,'order_errors':own,'completed':NS+' COMPLETE' in game,'elapsed_seconds':round(time.monotonic()-started,1),'source_hashes':inputs,'private_snapshot_hashes':private,'source_changed':[p for p,d in inputs.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=d],
      'limitations':['Private authority trigger admits explicitly marked AI countries to exercise human transaction paths without a second client. Actual AI neutralisation removes that private flag. Production controller switching is not a real multiplayer hotjoin.','Private fixture shortens selected already-activated clocks to exercise native expiry; shipped quota/outcome definitions remain 365/180.','No live multiplayer, manual tooltip, cost-stat inspector or save/rehost rehearsal.']}
    report['success']=report['completed'] and not failed and not unrun and not own and not report['source_changed']
    (HERE/'ENGINE_REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'success':report['success'],'passed':len(passed),'failed':failed,'unrun':unrun,'elapsed_seconds':report['elapsed_seconds'],'order_error_count':len(own),'order_error_sample':own[:3],'profile':str(PROFILE),'report':str(HERE/'ENGINE_REPORT.json')}),flush=True)


if __name__=='__main__':main()
