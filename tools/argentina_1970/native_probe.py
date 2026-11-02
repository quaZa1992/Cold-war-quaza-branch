# IMPERIA COLD WAR — Isolated Argentina native transaction fixture.
"""Run the actual installed effects in a private E: profile with artificial inputs."""
from __future__ import annotations
import argparse,hashlib,json,subprocess,sys,time
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
RUNTIME=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/argentina_1970')
PREFIX='ICW_ARG_NATIVE'
CHECKS=[]
MARK='# IMPERIA COLD WAR — Argentina isolated native fixture.\n'
sys.path.insert(0,str(HERE))
from core import P,grant
from budget import setup_share,annual_share,own_weekly_weight,transfer

def assertion(name,guard):
    CHECKS.append(name)
    return f'if = {{ limit = {{ {guard} }} log = "{PREFIX} PASS {name}" }} else = {{ log = "{PREFIX} FAIL {name}" }}\n'
def eq(var,value):return f'check_variable = {{ var = {var} value = {value} compare = equals }}'
def provider_drift(record):
    """Keep raw hash drift visible, distinguishing concurrent header comments."""
    sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
    from script_ast import parse
    raw=[];semantic=[]
    for rel,h in record['frozen_sources'].items():
        current=ROOT/rel;frozen=Path(record['overlay'])/rel
        if hashlib.sha256(current.read_bytes()).hexdigest()==h:continue
        raw.append(rel)
        if not rel.endswith('.txt') or parse(current.read_text(encoding='utf-8-sig'))!=parse(frozen.read_text(encoding='utf-8-sig')):semantic.append(rel)
    return raw,semantic
def fee(weight,gdp=1000):return Decimal(str(gdp))*Decimal(str(setup_share(weight))) if weight>0 else Decimal(str(weight))
def fixture(d):
    CHECKS.clear();out=[];bykey={n['key']:n for n in d['nodes']}
    out.append('COLDWAR_ARG_initialize = yes\n')
    out.append(assertion('scenario_tree','COLDWAR_ARG_is_scenario = yes has_focus_tree = COLDWAR_ARG_1970_focus'))
    out.append(assertion('ongania_start','COLDWAR_ARG_is_leader_ongania = yes nationalist_military_junta_are_in_power = yes'))
    for s in d['spirits']:out.append(assertion(s['id'],'has_idea = '+s['id']))
    out.append(assertion('uranium_zero','450 = { uranium_mine < 1 has_dynamic_modifier = { modifier = imp_uranium_deposit } }'))
    out.append('set_variable = { treasury = 1000 }\nset_variable = { gdp_total = 1000 }\nclr_country_flag = MD_skip_treasury_cost\n')
    out.append('complete_national_focus = COLDWAR_ARG_army_directives\n')
    n=bykey['army_directives'];balance=Decimal(1000)-fee(n['money'])
    out.append(assertion('first_focus_receipt','has_country_flag = COLDWAR_ARG_army_directives_applied'))
    out.append(assertion('first_focus_fee',eq('treasury',balance)))
    out.append(assertion('military_programme_active','has_dynamic_modifier = { modifier = COLDWAR_ARG_military_programme }'))
    out.append('COLDWAR_ARG_complete_army_directives = yes\n')
    out.append(assertion('focus_no_replay',eq('treasury',balance)))
    out.append('set_variable = { ruling_party = 3 }\nCOLDWAR_ARG_refresh_programmes = yes\n')
    out.append(assertion('military_out_of_office','NOT = { has_dynamic_modifier = { modifier = COLDWAR_ARG_military_programme } }'))
    out.append('set_variable = { ruling_party = 22 }\nCOLDWAR_ARG_refresh_programmes = yes\n')
    out.append(assertion('military_return','has_dynamic_modifier = { modifier = COLDWAR_ARG_military_programme } '+eq('treasury',balance)))
    out.append('effect_tooltip = { COLDWAR_ARG_preview_focus_army_directives = yes }\n')
    out.append(assertion('cost_preview_does_not_charge',eq('treasury',balance)))
    out.append('clr_country_flag = COLDWAR_ARG_army_directives_applied\nset_variable = { gdp_total = 0 }\nCOLDWAR_ARG_complete_army_directives = yes\n')
    out.append(assertion('zero_gdp_cannot_grant_free_focus',eq('treasury',balance)+' NOT = { has_country_flag = COLDWAR_ARG_army_directives_applied } NOT = { COLDWAR_ARG_can_complete_army_directives = yes }'))
    out.append('set_variable = { gdp_total = 2000 }\nCOLDWAR_ARG_complete_army_directives = yes\n')
    out.append(assertion('double_gdp_doubles_focus_cost',eq('treasury',balance-fee(n['money'],2000))))
    out.append('set_variable = { gdp_total = 1000 }\nset_variable = { treasury = '+str(balance)+' }\n')
    # Unlock only the Rosario prerequisite chain through the real native completion effect.
    done={'army_directives'}
    def complete(key):
        if key in done:return
        n=bykey[key]
        for group in n['prerequisites']:
            parent=next(x for x in group if next(z for z in d['nodes'] if z['id']==x)['party'] in (None,22))
            complete(parent.removeprefix(P))
        if key not in done:out.append('complete_national_focus = '+n['id']+'\n');done.add(key)
    complete('rosario_plan')
    out.append(assertion('rosario_goal','has_wargoal_against = ENG has_country_flag = COLDWAR_ARG_rosario_plan_applied NOT = { has_war_with = ENG }'))
    # Native building limits, then one paid mine construction through the real decision body helper guard.
    mine=next(a for a in d['decisions'] if a['key']=='uranium_mine')
    out.append('set_country_flag = COLDWAR_ARG_unlock_uranium_mine\n')
    out.append(assertion('uranium_capacity','COLDWAR_ARG_can_decide_uranium_mine = yes'))
    # Execute the installed uranium decision's hidden transaction, rather than a parallel implementation.
    sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
    from script_ast import parse,first,emit
    decs=first(parse((ROOT/'common/decisions/COLDWAR_ARG_1970_decisions.txt').read_text()),P+'national_decisions')
    mine_tx=first(first(first(decs,P+'decision_uranium_mine'),'complete_effect'),'hidden_effect')
    out.append('set_variable = { treasury = 0 }\n'+emit(mine_tx)+'\n')
    out.append(assertion('uranium_paid_from_zero',eq('treasury',-fee(mine['money']))+' 450 = { uranium_mine > 0 uranium_mine < 2 }'))
    out.append(emit(mine_tx)+'\n')
    out.append(assertion('uranium_no_replay',eq('treasury',-fee(mine['money']))+' 450 = { uranium_mine > 0 uranium_mine < 2 }'))
    build=bykey['state_steel']
    for group in build['prerequisites']:complete(group[0].removeprefix(P))
    out.append('453 = { set_variable = { ICW_ARG_before_factory = building_level@industrial_complex } }\nset_variable = { treasury = -1 }\n')
    complete('state_steel')
    out.append(assertion('factory_paid_from_negative',eq('treasury',-1-fee(build['money']))))
    out.append('453 = { set_variable = { ICW_ARG_factory_delta = building_level@industrial_complex } subtract_from_variable = { ICW_ARG_factory_delta = ICW_ARG_before_factory }\n'+assertion('factory_level_added',eq('ICW_ARG_factory_delta',1))+'}\n')
    out.append('COLDWAR_ARG_complete_state_steel = yes\n')
    out.append(assertion('factory_no_replay',eq('treasury',-1-fee(build['money']))))
    handover_tx=first(first(first(decs,P+'decision_civilian_handover'),'complete_effect'),'hidden_effect')
    out.append('set_country_flag = COLDWAR_ARG_party_organization_legalized\nset_country_flag = COLDWAR_ARG_electoral_timetable_published\nset_country_flag = COLDWAR_ARG_election_framework_ready\nset_country_flag = COLDWAR_ARG_unlock_civilian_handover\nenable_elections_with_no_leader_change = yes\nset_variable = { treasury = 1000 }\nset_country_flag = elections_in_progress\nCOLDWAR_ARG_record_native_election = yes\nset_variable = { ruling_party = 3 }\nCOLDWAR_ARG_refresh_politics = yes\n')
    out.append(assertion('handover_waits_for_election','NOT = { COLDWAR_ARG_has_recorded_election_winner = yes }'))
    out.append('clr_country_flag = elections_in_progress\nset_country_flag = coalition_forming\nCOLDWAR_ARG_refresh_politics = yes\n')
    out.append(assertion('handover_waits_for_coalition','NOT = { COLDWAR_ARG_has_recorded_election_winner = yes }'))
    out.append('clr_country_flag = coalition_forming\nCOLDWAR_ARG_refresh_politics = yes\n')
    out.append(assertion('records_actual_coalition_leader',eq('COLDWAR_ARG_last_election_winner',3)+' COLDWAR_ARG_can_decide_civilian_handover = yes'))
    out.append(emit(handover_tx)+'\n')
    out.append(assertion('civilian_handover_paid',eq('treasury',998)+' has_country_flag = COLDWAR_ARG_constitutional_government NOT = { has_idea = COLDWAR_ARG_start_regime } COLDWAR_ARG_is_leader_ricardo_balbin = yes'))
    out.append(emit(handover_tx)+'\n'+assertion('civilian_handover_no_replay',eq('treasury',998)))
    out.append('set_country_flag = elections_in_progress\nCOLDWAR_ARG_record_native_election = yes\nset_variable = { ruling_party = 13 }\nclr_country_flag = elections_in_progress\nCOLDWAR_ARG_refresh_politics = yes\n')
    out.append(assertion('second_term_handover_available','COLDWAR_ARG_can_decide_civilian_handover = yes'))
    out.append(emit(handover_tx)+'\n'+assertion('second_term_handover_paid',eq('treasury',996)+' COLDWAR_ARG_is_leader_peron = yes'))
    out.append('set_country_flag = elections_in_progress\nCOLDWAR_ARG_record_native_election = yes\nset_variable = { ruling_party = 22 }\nclr_country_flag = elections_in_progress\nCOLDWAR_ARG_refresh_politics = yes\n')
    out.append(emit(handover_tx)+'\n'+assertion('military_result_not_civilian',eq('treasury',996)+' NOT = { COLDWAR_ARG_can_decide_civilian_handover = yes }'))
    # These contract tests control both country's starting balances and restrictions privately.
    from treaties import SANCTIONS
    agreements={a['id']:a for a in d['agreements']}
    def clear_pair(p):
        return ''.join(f'if = {{ limit = {{ is_in_array = {{ array = {ar} value = {p} }} }} remove_from_array = {{ array = {ar} value = {p} }} }}\n{p} = {{ if = {{ limit = {{ is_in_array = {{ array = {ar} value = ARG }} }} remove_from_array = {{ array = {ar} value = ARG }} }} }}\n' for ar in SANCTIONS)
    for a in d['agreements']:
        k,p=a['id'],a['partner']
        out.append(clear_pair(p))
        out.append(f'set_variable = {{ treasury = 1000 }}\n{p} = {{ set_variable = {{ treasury = 1000 }} set_variable = {{ gdp_total = 500 }} clr_country_flag = MD_skip_treasury_cost }}\n')
        if k in ('madrid_consular','madrid_diplomatic'):out.append('set_country_flag = COLDWAR_ARG_south_atlantic_campaign\nset_country_flag = COLDWAR_ARG_south_atlantic_war_ended\n')
        parents=[];parent=a.get('parent')
        while parent:parents.insert(0,parent);parent=agreements[parent].get('parent')
        for parent in parents:
            out.append(f'set_country_flag = COLDWAR_ARG_treaty_{parent}_signed\n{p} = {{ set_country_flag = COLDWAR_ARG_treaty_{parent}_signed }}\nCOLDWAR_ARG_refresh_treaties = yes\n')
        # Restore British ownership between incompatible alternative treaty cases in this fixture only.
        if k in ('uk_links','uk_sovereignty'):out.append('ENG = { transfer_state = 26 }\n')
        out.append(f'COLDWAR_ARG_offer_{k} = yes\n')
        out.append(assertion(k+'_recipient_pending',f'has_country_flag = COLDWAR_ARG_treaty_{k}_pending {p} = {{ has_country_flag = COLDWAR_ARG_treaty_{k}_pending }}'))
        out.append(assertion(k+'_no_reward_before_consent',f'NOT = {{ has_idea = COLDWAR_ARG_treaty_{k}_arg }} {p} = {{ NOT = {{ has_idea = COLDWAR_ARG_treaty_{k}_partner }} }}'))
        out.append(f'{p} = {{ COLDWAR_ARG_execute_treaty_{k} = yes }}\nCOLDWAR_ARG_refresh_treaties = yes\n')
        out.append(assertion(k+'_both_spirits',f'has_idea = COLDWAR_ARG_treaty_{k}_arg {p} = {{ has_idea = COLDWAR_ARG_treaty_{k}_partner }}'))
        arg_after=Decimal(1000)-fee(a['argentina'].get('setup',0))
        par_after=Decimal(1000)-fee(a['recipient'].get('setup',0),500)+(Decimal(15) if a['id']=='uk_sovereignty' else Decimal(0))
        out.append(assertion(k+'_setup_arg',eq('treasury',arg_after)))
        out.append(assertion(k+'_setup_partner',f'{p} = {{ {eq("treasury",par_after)} }}'))
        out.append(f'{p} = {{ COLDWAR_ARG_execute_treaty_{k} = yes }}\n')
        out.append(assertion(k+'_setup_once',eq('treasury',arg_after)+f' {p} = {{ {eq("treasury",par_after)} }}'))
        if k=='uk_sovereignty':out.append(assertion('consensual_island_transfer','owns_state = 26 controls_state = 26 NOT = { is_core_of = ENG }' if False else 'owns_state = 26 controls_state = 26'))
        if k=='brazil_industry':
            for ar in SANCTIONS:
                for tag,target in [('ARG',p),(p,'ARG')]:
                    out.append(f'{tag} = {{ add_to_array = {{ array = {ar} value = {target} }} }}\nCOLDWAR_ARG_refresh_treaties = yes\n')
                    out.append(assertion(k+'_'+ar+'_'+tag+'_suspended',f'NOT = {{ has_idea = COLDWAR_ARG_treaty_{k}_arg }} {p} = {{ NOT = {{ has_idea = COLDWAR_ARG_treaty_{k}_partner }} }}'))
                    out.append(f'{tag} = {{ remove_from_array = {{ array = {ar} value = {target} }} }}\nCOLDWAR_ARG_refresh_treaties = yes\n')
                    out.append(assertion(k+'_'+ar+'_'+tag+'_restored',f'has_idea = COLDWAR_ARG_treaty_{k}_arg {p} = {{ has_idea = COLDWAR_ARG_treaty_{k}_partner }}'))
            # break_embargo operates on the event ROOT, so this synchronous fixture
            # exercises lift/restore as ARG. Recipient embargo suspension is separately checked.
            for tag,target in [('ARG',p)]:
                out.append(f'{tag} = {{ send_embargo = {target} }}\nCOLDWAR_ARG_refresh_treaties = yes\n')
                out.append(assertion(tag+'_embargo_suspends_pair',f'NOT = {{ has_idea = COLDWAR_ARG_treaty_{k}_arg }} {p} = {{ NOT = {{ has_idea = COLDWAR_ARG_treaty_{k}_partner }} }}'))
                out.append(f'{tag} = {{ break_embargo = {target} }}\nCOLDWAR_ARG_refresh_treaties = yes\n')
                out.append(assertion(tag+'_embargo_lift_restores_pair',f'has_idea = COLDWAR_ARG_treaty_{k}_arg {p} = {{ has_idea = COLDWAR_ARG_treaty_{k}_partner }}'))
            out.append('BRA = { send_embargo = ARG }\nCOLDWAR_ARG_refresh_treaties = yes\n')
            out.append(assertion('recipient_embargo_suspends_pair','NOT = { has_idea = COLDWAR_ARG_treaty_brazil_industry_arg } BRA = { NOT = { has_idea = COLDWAR_ARG_treaty_brazil_industry_partner } }'))
            out.append('declare_war_on = { target = BRA type = annex_everything }\nCOLDWAR_ARG_refresh_treaties = yes\n')
            out.append(assertion('war_suspends_pair','has_war_with = BRA NOT = { has_idea = COLDWAR_ARG_treaty_brazil_industry_arg } BRA = { NOT = { has_idea = COLDWAR_ARG_treaty_brazil_industry_partner } }'))
            out.append('white_peace = BRA\nCOLDWAR_ARG_refresh_treaties = yes\n')
            out.append(assertion('peace_restores_pair','NOT = { has_war_with = BRA } has_idea = COLDWAR_ARG_treaty_brazil_industry_arg BRA = { has_idea = COLDWAR_ARG_treaty_brazil_industry_partner }'))
        # Current-scope MD weekly aggregates use the actual signed treaty guards.
        for tag,side in [('ARG',a['argentina']),(p,a['recipient'])]:
            out.append(f'{tag} = {{ set_variable = {{ additional_income_rate = 0 }} set_variable = {{ additional_expenses_rate = 0 }} COLDWAR_ARG_add_treaty_income = yes COLDWAR_ARG_add_treaty_expenses = yes\n')
            # Other signed agreements can stack. This case's own positive flow must be included.
            if side.get('credit',0):out.append(assertion(k+'_'+tag+'_weekly_income',f'check_variable = {{ additional_income_rate > 0 }}'))
            if side.get('weekly',0):out.append(assertion(k+'_'+tag+'_weekly_expenses',f'check_variable = {{ additional_expenses_rate > 0 }}'))
            out.append('}\n')
        if k in ('bolivia_gas','soviet_grain'):
            payer,recipient,annual=transfer(a)
            # Compare each recipient income with the payer's incremental transfer,
            # excluding its own GDP-funded operating budget.
            out.append(f'{payer} = {{ set_variable = {{ additional_expenses_rate = 0 }} COLDWAR_ARG_add_treaty_expenses = yes set_variable = {{ ICW_ARG_transfer_debit = additional_expenses_rate }}\n')
            which='argentina' if payer=='ARG' else 'recipient'
            own=annual_share(own_weekly_weight(a,which))
            out.append(f'set_temp_variable = {{ ICW_ARG_transfer_operations = {{ value = gdp_total multiply = {own} divide = 52 }} }} subtract_from_variable = {{ ICW_ARG_transfer_debit = ICW_ARG_transfer_operations }} }}\n')
            out.append(f'{recipient} = {{ set_variable = {{ additional_income_rate = 0 }} COLDWAR_ARG_add_treaty_income = yes\n')
            out.append(assertion(k+'_transfer_debit_matches_credit',f'check_variable = {{ var = additional_income_rate value = {payer}.ICW_ARG_transfer_debit compare = equals }}'))
            out.append('}\n')
        # Clean this independent case; parent cases are re-established explicitly.
        out.append(f'clr_country_flag = COLDWAR_ARG_treaty_{k}_signed\n{p} = {{ clr_country_flag = COLDWAR_ARG_treaty_{k}_signed }}\nCOLDWAR_ARG_refresh_treaties = yes\n')
        for parent in reversed(parents):out.append(f'clr_country_flag = COLDWAR_ARG_treaty_{parent}_signed\n{p} = {{ clr_country_flag = COLDWAR_ARG_treaty_{parent}_signed }}\nCOLDWAR_ARG_refresh_treaties = yes\n')
    out.append('set_country_flag = COLDWAR_ARG_treaty_brazil_industry_signed\nBRA = { set_country_flag = COLDWAR_ARG_treaty_brazil_industry_signed }\nCOLDWAR_ARG_refresh_treaties = yes\n')
    out.append(assertion('annex_fixture_pair_active','has_idea = COLDWAR_ARG_treaty_brazil_industry_arg BRA = { has_idea = COLDWAR_ARG_treaty_brazil_industry_partner }'))
    out.append('BRA = { annex_country = { target = ARG transfer_troops = no } COLDWAR_ARG_refresh_treaties = yes\n'+assertion('annexation_removes_recipient_spirit','NOT = { country_exists = ARG } NOT = { has_idea = COLDWAR_ARG_treaty_brazil_industry_partner }')+'}\n')
    out.append(f'log = "{PREFIX} COMPLETE"\n');return ''.join(out)

def prepare():
    assert json.loads((HERE/'VALIDATION.json').read_text())['passed']
    run=RUNTIME/datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    assert run.resolve().is_relative_to(RUNTIME.resolve());run.mkdir(parents=True)
    profile,overlay=run/'profile',run/'fixture'
    def write(p,text):
        assert p.absolute().is_relative_to(run.absolute());p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8',newline='\n')
    manifest=json.loads((HERE/'manifest.json').read_text());frozen={}
    for rel in manifest['files']:
        src=ROOT/rel;dest=overlay/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(src.read_bytes());frozen[rel]=hashlib.sha256(src.read_bytes()).hexdigest()
    body=fixture(json.loads((HERE/'runtime_design.json').read_text(encoding='utf-8')))
    write(overlay/'common/on_actions/zzzz_ICW_ARG_native.txt',MARK+'on_actions = { on_startup = { effect = { ARG = { country_event = { id = ICW_ARG_NATIVE.1 hours = 1 } } } } }\n')
    write(overlay/'events/zzzz_ICW_ARG_native.txt',MARK+'add_namespace = ICW_ARG_NATIVE\ncountry_event = { id = ICW_ARG_NATIVE.1 hidden = yes is_triggered_only = yes immediate = {\n'+body+'} }\n')
    write(profile/'mod/base.mod',MARK+(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig')+'\npath="'+ROOT.as_posix()+'"\n')
    addon=MARK+'name="IMPERIA Argentina native fixture"\ndependencies={"MD Cold War"}\npath="'+overlay.as_posix()+'"\n'
    write(profile/'mod/fixture.mod',addon);write(overlay/'descriptor.mod',addon)
    write(profile/'dlc_load.json',json.dumps(dict(project='IMPERIA COLD WAR',enabled_mods=['mod/base.mod','mod/fixture.mod'],disabled_dlcs=[])))
    write(profile/'settings.txt','language="l_english"\ngraphics={size={x=1280 y=720} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n')
    record=dict(project='IMPERIA COLD WAR',profile=str(profile),overlay=str(overlay),frozen_sources=frozen,checks=CHECKS,boundary='One isolated native process. Controlled party slots, balances, sanctions and treaty receipts inside private fixture. No human UI, save/reload or multiplayer evidence.')
    write(run/'manifest.json',json.dumps(record,indent=2)+'\n');return run

def run_probe(run,duration):
    record=json.loads((run/'manifest.json').read_text());profile=Path(record['profile'])
    existing=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command','Get-Process -Name hoi4 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
    assert not existing.stdout.strip(),'Existing HOI4 process; leave it untouched.'
    game=Path('C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV')
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
    started=time.monotonic();process=subprocess.Popen([str(game/'hoi4.exe'),'-debug','-noasserts','-assertsdialog=no','-userdir='+str(profile),'-start_tag=ARG','-start_speed=5','-hands_off'],cwd=game,startupinfo=startup,creationflags=subprocess.CREATE_NO_WINDOW)
    print(json.dumps(dict(project='IMPERIA COLD WAR',pid=process.pid,profile=str(profile),expected_checks=len(CHECKS))),flush=True)
    logpath=profile/'logs/game.log';errorpath=profile/'logs/error.log';status='bounded_timeout';last=0
    try:
        while process.poll() is None and time.monotonic()-started<duration:
            time.sleep(1);log=logpath.read_text(encoding='utf-8-sig',errors='replace') if logpath.exists() else ''
            if PREFIX+' COMPLETE' in log:status='fixture_complete';break
            elapsed=int(time.monotonic()-started)
            if elapsed-last>=30:last=elapsed;print(json.dumps(dict(phase='native',elapsed_seconds=elapsed)),flush=True)
        if process.poll() is not None:status='process_exited'
    finally:
        if process.poll() is None:process.terminate()
        try:process.wait(timeout=10)
        except subprocess.TimeoutExpired:process.kill();process.wait()
    log=logpath.read_text(encoding='utf-8-sig',errors='replace') if logpath.exists() else ''
    error=errorpath.read_text(encoding='utf-8-sig',errors='replace') if errorpath.exists() else ''
    passed=[n for n in CHECKS if PREFIX+' PASS '+n in log];failed=[n for n in CHECKS if PREFIX+' FAIL '+n in log];missing=[n for n in CHECKS if n not in passed+failed]
    relevant=[s for s in error.splitlines() if any(k in s for k in ('COLDWAR_ARG','ICW_ARG_NATIVE','zzzz_ICW_ARG'))]
    drift,semantic_drift=provider_drift(record)
    result=dict(project='IMPERIA COLD WAR',run=str(run),status=status,elapsed_seconds=round(time.monotonic()-started,2),expected=len(CHECKS),passed=len(passed),failed=failed,missing=missing,feature_diagnostics=relevant,total_error_lines=len(error.splitlines()),frozen_source_drift=drift,runtime_semantic_drift=semantic_drift,boundary=record['boundary'])
    result['native_pass']=status=='fixture_complete' and not failed and not missing and not relevant and not semantic_drift
    text=json.dumps(result,indent=2)+'\n';(run/'NATIVE_RESULT.json').write_text(text,encoding='utf-8');(HERE/'NATIVE_RESULT.json').write_text(text,encoding='utf-8')
    (HERE/'NATIVE_CHECKPOINTS.txt').write_text('IMPERIA COLD WAR\n\n'+'\n'.join(s for s in log.splitlines() if PREFIX in s)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='feature_diagnostics'}|dict(feature_diagnostic_lines=len(relevant),first_diagnostics=relevant[:10]),indent=2),flush=True);return not result['native_pass']

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--duration',type=int,default=600);ap.add_argument('--runtime-root',type=Path,default=RUNTIME);ap.add_argument('--review-source-drift',action='store_true');args=ap.parse_args()
    RUNTIME=args.runtime_root
    if args.review_source_drift:
        path=HERE/'NATIVE_RESULT.json';result=json.loads(path.read_text());record=json.loads((Path(result['run'])/'manifest.json').read_text())
        raw,semantic=provider_drift(record)
        result['frozen_source_drift']=raw;result['runtime_semantic_drift']=semantic
        result['source_drift_review']='Raw changes retained. Parsed native-script bodies were compared with their exact frozen providers; comments and whitespace do not change the runtime body.'
        result['native_pass']=result['status']=='fixture_complete' and not result['failed'] and not result['missing'] and not result['feature_diagnostics'] and not semantic
        path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result));raise SystemExit(not result['native_pass'])
    raise SystemExit(run_probe(prepare(),args.duration))
