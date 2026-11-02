# IMPERIA COLD WAR — Isolated Brazil native transaction and government test.
"""Uses the user-approved D: test location; never changes a player profile/save."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import argparse,hashlib,json,os,subprocess,sys,time
from common import *
RUNTIME=Path('D:/HOI4_Mod_Tools/mdcoldwar/runtime/brazil_1970')
GAME=Path('C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV')
PREFIX='ICW_BRA_NATIVE';CHECKS=[]
def assertion(name,condition):
    CHECKS.append(name)
    return iff(condition,'log = "'+PREFIX+' PASS '+name+'"')+'\n'+block('else','log = "'+PREFIX+' FAIL '+name+'"')+'\n'
def eq(variable,v):return 'check_variable = { var = '+variable+' value = '+num(v)+' compare = equals }'
def approx(variable,v,tolerance='.0002'):
    x=Decimal(str(v));t=Decimal(tolerance)
    return f'check_variable = {{ {variable} > {num(x-t)} }}\ncheck_variable = {{ {variable} < {num(x+t)} }}'
def swap(slot):return 'set_temp_variable = { rul_party_temp = '+str(slot)+' }\nset_temp_variable = { disable_elections = 0 }\nchange_ruling_party_effect = yes\n'
def fixture(d):
    CHECKS.clear();out=[]
    out += [assertion('scenario_tree','tag = BRA\nIMP_is_1970_scenario = yes\nhas_focus_tree = '+TREE),assertion('medici_start','has_country_leader = { name = "Emilio Garrastazu Medici" ruling_only = yes }'),assertion('military_start','COLDWAR_BRA_military_in_power = yes')]
    for s in d['starting_spirits']:out.append(assertion('start_'+s['id'],'has_idea = '+s['id']))
    out += ['set_variable = { gdp_total = 1000 }\nset_variable = { treasury = 0 }\nclr_country_flag = MD_skip_treasury_cost\n',P+'complete_constitutional = yes\n',assertion('zero_balance_paid',eq('treasury',-2.5)),assertion('ai5_removed','NOT = { has_idea = COLDWAR_BRA_ai5 }'),P+'complete_constitutional = yes\n',assertion('no_duplicate_fee',eq('treasury',-2.5)),
            'set_variable = { treasury = -10 }\n'+P+'complete_development_bank = yes\n',assertion('negative_balance_paid',eq('treasury',-13)),P+'complete_military_0 = yes\n',assertion('military_policy_active','has_idea = '+idea_id('military_0')),P+'complete_arena_0 = yes\n',assertion('wrong_party_no_reward','NOT = { '+earned('arena_0')+' }'),
            'set_variable = { ICW_BRA_saved_cash = treasury }\n',swap(2),assertion('military_policy_suspended','NOT = { has_idea = '+idea_id('military_0')+' }'),assertion('national_policy_retained','has_idea = '+idea_id('constitutional')),assertion('mdb_real_leader','has_country_leader = { name = "Ulysses Guimarães" ruling_only = yes }'),swap(22),assertion('military_policy_restored','has_idea = '+idea_id('military_0')),assertion('party_return_no_fee',eq('treasury','ICW_BRA_saved_cash') if False else 'check_variable = { var = treasury value = ICW_BRA_saved_cash compare = equals }')]
    # Native historical programme rewards normalize the positive autocrat opinion input.
    out += ['set_variable = { the_military_opinion = 50 }\ncomplete_national_focus = '+P+'military_0\ncomplete_national_focus = '+P+'military_1\n'+P+'complete_military_1 = yes\n',assertion('faction_exact_signed_delta',eq('the_military_opinion',58))]
    for sid in (882,888):
        out.append(assertion('infra_preflight_'+str(sid),asset_checks(dict(state=sid,building='infrastructure',amount=1))))
        out.append(country(str(sid),'set_variable = { ICW_BRA_infra_before = building_level@infrastructure }')+'\n')
    out += ['set_variable = { treasury = 1000 }\n'+P+'complete_municipal = yes\n',assertion('municipal_paid_once',eq('treasury',994))]
    for sid in (882,888):
        delta=country(str(sid),'set_temp_variable = { ICW_BRA_delta = { value = building_level@infrastructure subtract = ICW_BRA_infra_before } }\n'+assertion('infra_'+str(sid),eq('ICW_BRA_delta',1)))
        out.append(delta+'\n')
    out += [P+'complete_municipal = yes\n',assertion('municipal_replay_blocked',eq('treasury',994))]
    # A shared-slot-consuming industrial grant exercises the other capacity path.
    for sid in (882,884):out.append(country(str(sid),'set_variable = { ICW_BRA_civ_before = building_level@industrial_complex }')+'\n')
    out += ['complete_national_focus = '+P+'development_bank\n'+P+'complete_industrial_triangle = yes\n',assertion('industrial_paid_once',eq('treasury',985))]
    for sid in (882,884):
        out.append(country(str(sid),'set_temp_variable = { ICW_BRA_delta = { value = building_level@industrial_complex subtract = ICW_BRA_civ_before } }\n'+assertion('civ_'+str(sid),eq('ICW_BRA_delta',1)))+'\n')
    out += [P+'complete_industrial_triangle = yes\n',assertion('industrial_replay_blocked',eq('treasury',985))]
    # Material preview helpers must never grant support or register an organization.
    out += ['set_variable = { ICW_BRA_preview_party_before = party_pop_array^3 }\nset_variable = { ICW_BRA_preview_outlook_before = party_popularity@democratic }\n',block('effect_tooltip',P+'1970_preview_register_pt = yes')+'\n',assertion('registration_preview_no_party_reward','check_variable = { var = party_pop_array^3 value = ICW_BRA_preview_party_before compare = equals }'),assertion('registration_preview_no_outlook_reward','check_variable = { var = party_popularity@democratic value = ICW_BRA_preview_outlook_before compare = equals }'),assertion('registration_preview_no_registration','NOT = { '+flag('1970_party_pt_registered')+' }')]
    # Exercise real reform -> registration -> native outlook election -> exact programme.
    out += [P+'event_apply_party_reform_option_0 = yes\n',assertion('reform_preserves_medici','has_country_leader = { name = "Emilio Garrastazu Medici" ruling_only = yes }'),assertion('elections_enabled','has_elections = yes'),assertion('labour_stage_open',flag('1970_labourist_reorganization_open')),P+'1970_form_pt = yes\n'+P+'1970_nominate_pt = yes\n',assertion('pt_registered',flag('1970_party_pt_registered')),swap(3),assertion('pt_exact_government',P+'pt_in_power = yes\nNOT = { '+P+'pdt_in_power = yes }'),assertion('pt_real_leader','has_country_leader = { name = "Luiz Inácio Lula da Silva" ruling_only = yes }'),P+'complete_pt_0 = yes\n',assertion('pt_programme_active','has_idea = '+idea_id('pt_0')),P+'complete_pdt_0 = yes\n',assertion('same_slot_other_party_blocked','NOT = { '+earned('pdt_0')+' }'),swap(22),assertion('pt_programme_suspended','NOT = { has_idea = '+idea_id('pt_0')+' }'),swap(3),assertion('pt_programme_restored','has_idea = '+idea_id('pt_0')),swap(22)]
    # Native election mapping across outlooks and distinct parties within one outlook.
    out += [P+'1970_form_pds = yes\n'+P+'1970_form_pmdb = yes\n'+P+'open_organisation_stages = yes\n']
    for org,group,slot,leader in [('pds','arena',1,'Paulo Salim Maluf'),('pfl','pfl',1,'Jorge Bornhausen'),('pmdb','mdb',2,'Tancredo Neves'),('psdb','psdb',2,'Fernando Henrique Cardoso'),('historic_ptb','ptb',3,'João Goulart'),('ptb_late','ptb_late',3,'Ivete Vargas'),('pdt','pdt',3,'Leonel Brizola'),('pcb','pcb',4,'Luís Carlos Prestes'),('pcdob','pcdob',19,'João Amazonas')]:
        out += [P+'1970_form_'+org+' = yes\n']
        if org not in ('pcb','pcdob'):out.append(P+'1970_nominate_'+org+' = yes\n')
        out += [swap(slot),assertion(org+'_identity',P+group+'_in_power = yes'),assertion(org+'_leader','has_country_leader = { name = "'+leader+'" ruling_only = yes }'),swap(22)]
    # One full standing agreement: focus sends, recipient consents, both sides pay their own GDP.
    n=next(n for n in d['nodes'] if n['key']=='itaipu');o=n['offer'];tag=o['partner']
    for side in ('BRA',tag):
        other=tag if side=='BRA' else 'BRA'
        out.append(country(side,'\n'.join(iff('is_in_array = { array = imp_'+cls+'_sanc_'+di+' value = '+other+' }','remove_from_array = { array = imp_'+cls+'_sanc_'+di+' value = '+other+' }') for cls in ('dip','fin','eco','mil') for di in ('on_us','by_us')))+'\n')
    out += ['complete_national_focus = '+P+'itamaraty\n'+P+'complete_itamaraty = yes\ncomplete_national_focus = '+P+'regional\n'+P+'complete_regional = yes\nset_variable = { gdp_total = 1000 }\nset_variable = { treasury = 1000 }\nPAR = { set_variable = { gdp_total = 500 } set_variable = { treasury = 1000 } clr_country_flag = MD_skip_treasury_cost }\n',P+'propose_itaipu = yes\n',assertion('proposal_no_brazil_fee',eq('treasury',1000)),assertion('proposal_no_spirits','NOT = { has_idea = '+o['brazil']['spirit']+' }'),assertion('recipient_pending','PAR = { '+flag('pending_itaipu')+' }'),assertion('acceptance_ready',P+'can_accept_itaipu = yes'),country('PAR',P+'accept_itaipu = yes')+'\n',assertion('brazil_own_gdp_setup',eq('treasury',985)),assertion('paraguay_own_gdp_setup',country('PAR',eq('treasury',996.75))),assertion('both_standing_spirits','has_idea = '+o['brazil']['spirit']+'\nPAR = { has_idea = '+o['recipient']['spirit']+' }'),country('PAR',P+'accept_itaipu = yes')+'\n',assertion('acceptance_replay_blocked',eq('treasury',985))]
    out += ['set_variable = { additional_expenses_rate = 0 }\n'+P+'add_weekly_expenses = yes\n',assertion('brazil_gdp_weekly_budget',approx(P+'cooperation_weekly_expense',Decimal(1000)*Decimal('.0026')/52)),country('PAR','set_variable = { additional_income_rate = 0 }\n'+P+'add_weekly_income = yes\n'+assertion('paraguay_same_quote_income',approx(P+'cooperation_weekly_income',Decimal(1000)*Decimal('.0008')/52)))+'\n',
            'set_variable = { gdp_total = 2000 }\nset_variable = { additional_expenses_rate = 0 }\n'+P+'add_weekly_expenses = yes\n',assertion('current_gdp_reprices',approx(P+'cooperation_weekly_expense',Decimal(2000)*Decimal('.0026')/52)),country('PAR',P+'add_weekly_income = yes\n'+assertion('same_repriced_transfer',approx(P+'cooperation_weekly_income',Decimal(2000)*Decimal('.0008')/52)))+'\n','set_variable = { ICW_BRA_contract_cash = treasury }\nPAR = { set_variable = { ICW_BRA_contract_cash = treasury } }\n']
    for cls in ('dip','fin','eco','mil'):
        for di in ('on_us','by_us'):
            arr='imp_'+cls+'_sanc_'+di;k=cls+'_'+di
            out += ['add_to_array = { array = '+arr+' value = PAR }\n'+P+'sync_agreements = yes\n',assertion('suspend_'+k,'NOT = { has_idea = '+o['brazil']['spirit']+' }\nPAR = { NOT = { has_idea = '+o['recipient']['spirit']+' } }'),P+'add_weekly_expenses = yes\n',assertion('no_expense_'+k,eq(P+'cooperation_weekly_expense',0)),'remove_from_array = { array = '+arr+' value = PAR }\n'+P+'sync_agreements = yes\n',assertion('restore_'+k,'has_idea = '+o['brazil']['spirit']+'\nPAR = { has_idea = '+o['recipient']['spirit']+' }'),assertion('no_setup_replay_'+k,'check_variable = { var = treasury value = ICW_BRA_contract_cash compare = equals }\nPAR = { check_variable = { var = treasury value = ICW_BRA_contract_cash compare = equals } }')]
    for side,other in [('BRA','PAR')]:
        out += [country(side,'send_embargo = '+other)+'\n'+P+'sync_agreements = yes\n',assertion('embargo_suspends_'+side,'NOT = { has_idea = '+o['brazil']['spirit']+' }\nPAR = { NOT = { has_idea = '+o['recipient']['spirit']+' } }'),country(side,'break_embargo = '+other)+'\n'+P+'sync_agreements = yes\n',assertion('embargo_restore_'+side,P+'itaipu_active = yes')]
    out += ['declare_war_on = { target = PAR type = annex_everything }\n'+P+'sync_agreements = yes\n',assertion('war_suspends','has_war_with = PAR\nNOT = { has_idea = '+o['brazil']['spirit']+' }\nPAR = { NOT = { has_idea = '+o['recipient']['spirit']+' } }'),'white_peace = { tag = PAR }\n'+P+'sync_agreements = yes\n',assertion('peace_restores',P+'itaipu_active = yes'),assertion('peace_no_setup_replay','check_variable = { var = treasury value = ICW_BRA_contract_cash compare = equals }')]
    # break_embargo explicitly uses ROOT as sender. A separate recipient event is
    # necessary to test Paraguay's side; nesting PAR in this BRA event is not enough.
    out += ['PAR = { country_event = { id = ICW_BRA_NATIVE.2 hours = 1 } }\n']
    return ''.join(out)

def recipient_fixture(d):
    o=next(n['offer'] for n in d['nodes'] if n['key']=='itaipu')
    return ''.join([
        assertion('recipient_event_scope','tag = PAR'),
        'send_embargo = BRA\nBRA = { '+P+'sync_agreements = yes }\n',
        assertion('embargo_suspends_PAR','NOT = { has_idea = '+o['recipient']['spirit']+' }\nBRA = { NOT = { has_idea = '+o['brazil']['spirit']+' } }'),
        'break_embargo = BRA\nBRA = { '+P+'sync_agreements = yes }\n',
        assertion('embargo_restore_PAR','BRA = { '+P+'itaipu_active = yes }'),
        assertion('recipient_restore_no_fee','check_variable = { var = treasury value = ICW_BRA_contract_cash compare = equals }'),
        'log = "'+PREFIX+' COMPLETE"\n',
    ])
def prepare():
    validation=json.loads((HERE/'VALIDATION.json').read_text());assert not validation['errors']
    run=RUNTIME/datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f');assert run.resolve().is_relative_to(RUNTIME.resolve());run.mkdir(parents=True)
    profile=run/'profile';overlay=run/'fixture'
    def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
    manifest=json.loads((HERE/'manifest.json').read_text());frozen={}
    for rel in manifest['files']:
        if rel.startswith(('common/','history/','events/','localisation/','interface/')):
            p=ROOT/rel;q=overlay/rel;q.parent.mkdir(parents=True,exist_ok=True);raw=p.read_bytes();q.write_bytes(raw);frozen[rel]=hashlib.sha256(raw).hexdigest()
    # No asset traversal or junction copy: ordinary base-mod assets remain read-only.
    rel='interface/COLDWAR_BRA_1970.gfx';q=overlay/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((ROOT/rel).read_bytes());frozen[rel]=hashlib.sha256(q.read_bytes()).hexdigest()
    art=json.loads((HERE/'art_manifest.json').read_text());assets={}
    for family in ('focus_icons','event_pictures','idea_icons','group_idea_icons'):
        for row in art[family].values():
            path=row.get('source_texture',row.get('asset'));assets[path]=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
    design=json.loads((HERE/'approved_design.json').read_text());body=fixture(design);recipient=recipient_fixture(design)
    write(overlay/'common/on_actions/zzzz_ICW_BRA_native.txt',MARK+'on_actions = { on_startup = { effect = { BRA = { country_event = { id = ICW_BRA_NATIVE.1 hours = 1 } } } } }\n')
    write(overlay/'events/zzzz_ICW_BRA_native.txt',MARK+'add_namespace = ICW_BRA_NATIVE\ncountry_event = { id = ICW_BRA_NATIVE.1 hidden = yes is_triggered_only = yes immediate = {\n'+body+'} }\ncountry_event = { id = ICW_BRA_NATIVE.2 hidden = yes is_triggered_only = yes immediate = {\n'+recipient+'} }\n')
    write(profile/'mod/base.mod',MARK+(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig')+'\npath="'+ROOT.as_posix()+'"\n')
    addon=MARK+'name="IMPERIA Brazil native fixture"\ndependencies={"MD Cold War"}\npath="'+overlay.as_posix()+'"\n'
    write(profile/'mod/fixture.mod',addon);write(overlay/'descriptor.mod',addon)
    write(profile/'dlc_load.json',json.dumps(dict(enabled_mods=['mod/base.mod','mod/fixture.mod'],disabled_dlcs=[])))
    write(profile/'settings.txt','language="l_english"\ngraphics={size={x=1280 y=720} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n')
    record=dict(project='IMPERIA COLD WAR',profile=str(profile),overlay=str(overlay),frozen_sources=frozen,referenced_art_sha256=assets,checks=CHECKS,boundary='Isolated artificial GDP/treasury and party states, one hidden owned process. No player profile/save/playset changes; no MP or visual hover claim.')
    write(run/'manifest.json',json.dumps(record,indent=2));(HERE/'NATIVE_PREPARE.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',run=str(run),checks=len(CHECKS)),indent=2),encoding='utf-8')
    return run
def execute(run,duration,inspect_seconds=0):
    r=json.loads((run/'manifest.json').read_text());profile=Path(r['profile'])
    existing=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command','Get-Process -Name hoi4 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
    assert not existing.stdout.strip(),'An existing HOI4 process is running; leave it untouched.'
    startinfo=subprocess.STARTUPINFO();startinfo.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startinfo.wShowWindow=0
    env=dict(os.environ);env['SteamAppId']='394360'
    args=[str(GAME/'hoi4.exe'),'-debug','-noasserts','-assertsdialog=no','-userdir='+str(profile),'-start_tag=BRA','-start_speed=5','-hands_off']
    process=subprocess.Popen(args,cwd=GAME,env=env,startupinfo=startinfo,creationflags=subprocess.CREATE_NO_WINDOW)
    print(json.dumps(dict(pid=process.pid,profile=str(profile),expected=len(r['checks']))),flush=True)
    started=time.monotonic();logpath=profile/'logs/game.log';errorpath=profile/'logs/error.log';status='timeout';tick=0
    try:
        while process.poll() is None and time.monotonic()-started<duration:
            time.sleep(1);log=logpath.read_text(encoding='utf-8-sig',errors='replace') if logpath.exists() else ''
            if PREFIX+' COMPLETE' in log:
                status='fixture_complete'
                if inspect_seconds:
                    print(json.dumps(dict(inspection_ready=True,pid=process.pid,hold_seconds=inspect_seconds)),flush=True)
                    hold=time.monotonic()
                    while process.poll() is None and time.monotonic()-hold<inspect_seconds:
                        if (run/'END_INSPECTION').exists():break
                        time.sleep(1)
                break
            if time.monotonic()-tick>30:tick=time.monotonic();print(json.dumps(dict(elapsed=round(time.monotonic()-started),log=logpath.exists())),flush=True)
        if process.poll() is not None:status='exited'
    finally:
        if process.poll() is None:process.terminate()
        try:process.wait(timeout=10)
        except subprocess.TimeoutExpired:process.kill();process.wait()
    log=logpath.read_text(encoding='utf-8-sig',errors='replace') if logpath.exists() else '';err=errorpath.read_text(encoding='utf-8-sig',errors='replace') if errorpath.exists() else ''
    passed=[n for n in r['checks'] if PREFIX+' PASS '+n in log];failed=[n for n in r['checks'] if PREFIX+' FAIL '+n in log];missing=[n for n in r['checks'] if n not in passed+failed]
    diagnostics=[s for s in err.splitlines() if any(k in s for k in ('COLDWAR_BRA','ICW_BRA','zzzz_ICW_BRA'))]
    result=dict(project='IMPERIA COLD WAR',run=str(run),status=status,exit_code=process.returncode,seconds=round(time.monotonic()-started,2),expected=len(r['checks']),passed=len(passed),failed=failed,missing=missing,feature_diagnostics=diagnostics,total_error_lines=len(err.splitlines()),boundary=r['boundary'])
    result['native_pass']=status=='fixture_complete' and not(failed or missing or diagnostics)
    (run/'NATIVE_RESULT.json').write_text(json.dumps(result,indent=2),encoding='utf-8');(HERE/'NATIVE_RESULT.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (HERE/'NATIVE_CHECKPOINTS.txt').write_text('IMPERIA COLD WAR\n\n'+'\n'.join(s for s in log.splitlines() if PREFIX in s)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)
    return int(not result['native_pass'])
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--duration',type=int,default=300);parser.add_argument('--prepare-only',action='store_true');parser.add_argument('--inspect-seconds',type=int,default=0);parser.add_argument('--release',action='store_true');a=parser.parse_args()
    if a.release:
        run=Path(json.loads((HERE/'NATIVE_PREPARE.json').read_text())['run']);assert run.resolve().is_relative_to(RUNTIME.resolve())
        (run/'END_INSPECTION').write_text('IMPERIA COLD WAR\n',encoding='utf-8');sys.exit(0)
    run=prepare();print(str(run),flush=True)
    sys.exit(0 if a.prepare_only else execute(run,a.duration,a.inspect_seconds))
