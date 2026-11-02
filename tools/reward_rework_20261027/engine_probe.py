# IMPERIA COLD WAR — Native Korea/Japan capital, finance and programme checks.
"""Isolated E: fixture. Actual guards/helpers, no live multiplayer claim."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'docs/reward_rework_20261027'
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
PROFILE=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/reward_rework_20261027/native')/time.strftime('%Y%m%d_%H%M%S')
MARK='# IMPERIA COLD WAR — Private reward revision engine fixture.\n'
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,values,walk,emit
CHECKS=[]


def check(name,condition):
    CHECKS.append(name)
    return f'if = {{ limit = {{ {condition} }} log = "COLDWAR_RW_PROBE PASS {name}" }} else = {{ log = "COLDWAR_RW_PROBE FAIL {name}" }}\n'


def amount_is(variable,expected):
    return f'check_variable = {{ {variable} > {expected-.0001:.5f} }} check_variable = {{ {variable} < {expected+.0001:.5f} }}'


def parents(tag,target):
    tree=first(parse((ROOT/f'common/national_focus/COLDWAR_{tag}_1970_focus.txt').read_text(encoding='utf-8')),'focus_tree')
    by={first(f,'id'):f for f in values(tree,'focus')};seen=set();ordered=[]
    def visit(key):
        for group in values(by[key],'prerequisite'):
            parent=values(group,'focus')[0]
            if parent not in seen:
                visit(parent);seen.add(parent);ordered.append(parent)
    visit(target)
    return '\n'.join('complete_national_focus = '+key for key in ordered)


def helper(path,name):
    body=first(parse((ROOT/path).read_text(encoding='utf-8')),name)
    assert body is not None,name
    flag=next(v for k,o,v in walk(body) if k=='set_country_flag' and isinstance(v,str))
    return body,flag


def fixture():
    events=[MARK+'add_namespace = COLDWAR_RW_probe\n'];triggers=[]
    for idx,(tag,leader,target,call,path,state,building,levels,expected,cap) in enumerate([
        ('NKO','Kim Il Sung','COLDWAR_NKO_steelworks','COLDWAR_NKO_complete_steelworks','common/scripted_effects/COLDWAR_NKO_1970_focus_effects.txt',602,'arms_factory',2,2.25,None),
        ('KOR','Park Chung Hee','COLDWAR_KOR_pohang_foundry','COLDWAR_KOR_complete_pohang_foundry','common/scripted_effects/COLDWAR_KOR_1970_focus.txt',605,'industrial_complex',2,1.75,50),
        ('JAP','Eisaku Sato','COLDWAR_JAP_1970_microelectronics_capacity','COLDWAR_JAP_1970_microelectronics_capacity_apply','common/scripted_effects/COLDWAR_JAP_1970_national_economy.txt',615,'microchip_plant',2,2.5,5),
    ],1):
        body,receipt=helper(path,call)
        guard=first(first(body,'if'),'limit')
        can='COLDWAR_RW_can_'+tag
        triggers.append(can+' = {\n'+emit(guard)+'\n}')
        code=check(tag+'_authored_tree','has_focus_tree = COLDWAR_'+tag+'_1970_focus')
        code+=check(tag+'_historical_leader',f'has_country_leader = {{ name = "{leader}" ruling_only = yes }}')
        code+='set_variable = { gdp_total = 100 }\n'
        if tag=='JAP':code+='set_technology = { microchip_production_1 = 1 }\n'
        code+=parents(tag,target)+'\nset_variable = { gdp_total = 100 }\nset_variable = { treasury = 0 }\n'
        code+=f'{state} = {{ set_variable = {{ COLDWAR_RW_before_zero_gdp = building_level@{building} }} }}\nset_variable = {{ gdp_total = 0 }}\n'
        code+=check(tag+'_zero_gdp_blocks_project','NOT = { '+can+' = yes }')
        code+=call+' = yes\n'
        code+=check(tag+'_zero_gdp_has_no_assets_charge_or_receipt',amount_is('treasury',0)+f' NOT = {{ has_country_flag = {receipt} }} {state} = {{ check_variable = {{ building_level@{building} = COLDWAR_RW_before_zero_gdp }} }}')
        code+='set_variable = { gdp_total = 100 }\n'
        if cap:
            code+=f'{state} = {{ add_extra_state_shared_building_slots = 80 set_building_level = {{ type = {building} level = {cap-levels+1} }} }}\n'
            code+=check(tag+'_capacity_fixture',f'{state} = {{ check_variable = {{ building_level@{building} = {cap-levels+1} }} }}')
            code+=check(tag+'_aggregate_cap_guard','NOT = { '+can+' = yes }')
            code+=call+' = yes\n'
            code+=check(tag+'_blocked_project_has_no_charge_or_receipt',amount_is('treasury',0)+' NOT = { has_country_flag = '+receipt+' }')
            code+=f'{state} = {{ set_building_level = {{ type = {building} level = {cap-levels} }} }}\n'
        code+=check(tag+'_eligible',can+' = yes')
        code+=f'{state} = {{ set_variable = {{ COLDWAR_RW_expected_building = building_level@{building} }} add_to_variable = {{ COLDWAR_RW_expected_building = {levels} }} }}\n'
        code+=call+' = yes\n'
        conditions=f'has_country_flag = {receipt} {state} = {{ check_variable = {{ building_level@{building} = COLDWAR_RW_expected_building }} }} '+amount_is('treasury',-expected)
        code+=check(tag+'_capital_and_gdp_charge',conditions)
        code+=call+' = yes\n'+check(tag+'_replay_grants_and_charges_nothing',conditions)
        if tag=='JAP':
            code+=check('JAP_industry_research_bonus','has_tech_bonus = { category = CAT_industry }')
            party='COLDWAR_JAP_1970_party_reward_ldp_deep_fork1_a_follow'
            _,pflag=helper('common/scripted_effects/COLDWAR_JAP_1970_party_effects.txt',party)
            code+=parents(tag,'COLDWAR_JAP_1970_ldp_deep_fork1_a_follow')+'\nset_variable = { gdp_total = 100 }\nset_variable = { treasury = 0 }\n'
            code+='615 = { set_variable = { COLDWAR_RW_expected_party_civ = building_level@industrial_complex } add_to_variable = { COLDWAR_RW_expected_party_civ = 1 } }\n'
            code+=party+' = yes\n'
            code+='log = "COLDWAR_RW_VALUES party_grant ruling=[?ruling_party] civ=[?modifier@civilian_factories_productivity] ldp=[?COLDWAR_JAP_1970_LDP_civilian_factories_productivity] treasury=[?treasury]"\n'
            code+='if = { limit = { has_dynamic_modifier = { modifier = COLDWAR_JAP_1970_LDP_programme } } log = "COLDWAR_RW_VALUES party_grant LDP_present" } else = { log = "COLDWAR_RW_VALUES party_grant LDP_absent" }\n'
            pconditions=f'has_country_flag = {pflag} 615 = {{ check_variable = {{ building_level@industrial_complex = COLDWAR_RW_expected_party_civ }} }} '+amount_is('treasury',-2.75)
            code+=check('JAP_party_project_capital_and_gdp',pconditions)
            code+='set_variable = { COLDWAR_RW_active_civ = modifier@civilian_factories_productivity }\nset_variable = { COLDWAR_RW_inactive_civ = COLDWAR_RW_active_civ }\nsubtract_from_variable = { COLDWAR_RW_inactive_civ = COLDWAR_JAP_1970_LDP_civilian_factories_productivity }\nset_variable = { ruling_party = 2 }\nforce_update_dynamic_modifier = yes\n'
            code+='set_temp_variable = { COLDWAR_RW_delta = modifier@civilian_factories_productivity }\nsubtract_from_temp_variable = { COLDWAR_RW_delta = COLDWAR_RW_inactive_civ }\n'
            code+='log = "COLDWAR_RW_VALUES party_off ruling=[?ruling_party] civ=[?modifier@civilian_factories_productivity] expected=[?COLDWAR_RW_inactive_civ] delta=[?COLDWAR_RW_delta] treasury=[?treasury]"\n'
            code+='if = { limit = { has_dynamic_modifier = { modifier = COLDWAR_JAP_1970_LDP_programme } } log = "COLDWAR_RW_VALUES party_off LDP_present" } else = { log = "COLDWAR_RW_VALUES party_off LDP_absent" }\n'
            code+=check('JAP_party_programme_deactivates',amount_is('COLDWAR_RW_delta',0))
            code+='set_variable = { ruling_party = 1 }\nforce_update_dynamic_modifier = yes\n'+party+' = yes\n'
            code+='set_temp_variable = { COLDWAR_RW_delta = modifier@civilian_factories_productivity }\nsubtract_from_temp_variable = { COLDWAR_RW_delta = COLDWAR_RW_active_civ }\n'
            code+='log = "COLDWAR_RW_VALUES party_return ruling=[?ruling_party] civ=[?modifier@civilian_factories_productivity] expected=[?COLDWAR_RW_active_civ] delta=[?COLDWAR_RW_delta] treasury=[?treasury]"\n'
            code+='if = { limit = { has_dynamic_modifier = { modifier = COLDWAR_JAP_1970_LDP_programme } } log = "COLDWAR_RW_VALUES party_return LDP_present" } else = { log = "COLDWAR_RW_VALUES party_return LDP_absent" }\n'
            code+=check('JAP_party_return_restores_without_replay',pconditions+' '+amount_is('COLDWAR_RW_delta',0))
        code+='log = "COLDWAR_RW_PROBE DONE_'+tag+'"\n'
        events.append(f'country_event = {{ id = COLDWAR_RW_probe.{idx} hidden = yes is_triggered_only = yes immediate = {{\n'+code+'\n} }')
    return '\n'.join(events),MARK+'\n'.join(triggers)


def write(relative,text):
    p=PROFILE/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')


def main():
    hashes=json.loads((REPORT/'SOURCE_CHECKS.json').read_text(encoding='utf-8'))['runtime_sha256']
    for p,h in hashes.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
    write('mod/base.mod',MARK+(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig')+'\npath="'+ROOT.as_posix()+'"\n')
    addon=MARK+'name="Reward revision native verification"\ndependencies={ "MD Cold War" }\npath="'+(PROFILE/'fixture').as_posix()+'"\n'
    write('mod/probe.mod',addon);write('fixture/descriptor.mod',addon)
    write('dlc_load.json',json.dumps({'enabled_mods':['mod/base.mod','mod/probe.mod'],'disabled_dlcs':[]}))
    write('settings.txt',MARK+'language="l_english"\ngraphics={size={x=1280 y=900} fullScreen=no borderless=no}\nmaster_volume=0\n')
    dispatch=' '.join(tag+' = { country_event = { id = COLDWAR_RW_probe.'+str(i)+' hours = 1 } }' for i,tag in enumerate(('NKO','KOR','JAP'),1))
    write('fixture/common/on_actions/zz_COLDWAR_RW_probe.txt',MARK+'on_actions = { on_startup = { effect = { '+dispatch+' } } }')
    events,triggers=fixture();write('fixture/events/COLDWAR_RW_probe.txt',events);write('fixture/common/scripted_triggers/COLDWAR_RW_probe.txt',triggers)
    for name in ('game.log','error.log'):write('logs/'+name,'')
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
    started=time.monotonic()
    process=subprocess.Popen([str(GAME/'hoi4.exe'),'-debug','-noasserts','-assertsdialog=no','-userdir='+str(PROFILE),'-start_tag=NKO','-start_speed=5'],cwd=GAME,startupinfo=startup)
    print(json.dumps({'project':'IMPERIA COLD WAR','pid':process.pid,'profile':str(PROFILE)}),flush=True)
    try:
        while process.poll() is None and time.monotonic()-started<700:
            time.sleep(1)
            game=(PROFILE/'logs/game.log').read_text(encoding='utf-8-sig',errors='replace')
            if all('COLDWAR_RW_PROBE DONE_'+tag in game for tag in ('NKO','KOR','JAP')):break
    finally:
        if process.poll() is None:process.terminate()
        try:process.wait(timeout=10)
        except subprocess.TimeoutExpired:process.kill();process.wait()
    game=(PROFILE/'logs/game.log').read_text(encoding='utf-8-sig',errors='replace')
    errors=(PROFILE/'logs/error.log').read_text(encoding='utf-8-sig',errors='replace')
    records=re.split(r'(?=\[\d{2}:\d{2}:\d{2}\]\[)',errors)
    relevant=[r.strip() for r in records if any(token in r for token in ('COLDWAR_NKO','COLDWAR_KOR','COLDWAR_JAP','COLDWAR_RW_')) and 'Reloading Events:' not in r]
    passed=[n for n in CHECKS if 'COLDWAR_RW_PROBE PASS '+n in game];failed=[n for n in CHECKS if 'COLDWAR_RW_PROBE FAIL '+n in game]
    unrun=[n for n in CHECKS if n not in passed+failed]
    changed=[p for p,h in hashes.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    result={'project':'IMPERIA COLD WAR','profile':str(PROFILE),'passed':passed,'failed':failed,'unrun':unrun,'relevant_errors':relevant,'source_sha256':hashes,'changed_during_run':changed,'elapsed_seconds':round(time.monotonic()-started,1),'crashes':[p.name for p in (PROFILE/'crashes').glob('*') if p.is_dir()],'scope':'Native single-client reward fixture. Real country-scoped events prepare real predecessor focuses, GDP=100 and the stated technology. Extra private state slots and temporary levels exercise native cap boundaries. Actual country helpers run with their full guards, asset/treasury receipts, replay and Japanese party-variable deactivation/restoration. No real campaign balance, manual hover, save/rehost, live combat or multi-client/OOS claim.'}
    result['success']=not failed and not unrun and not relevant and not changed and not result['crashes']
    (REPORT/'ENGINE_REPORT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'success':result['success'],'passed':len(passed),'failed':failed,'unrun':unrun,'relevant_error_count':len(relevant),'sample':relevant[:6]}),flush=True)


if __name__=='__main__':main()
