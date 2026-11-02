# IMPERIA COLD WAR — Isolated native Cyprus runtime verification.
"""Uses a private E: userdir. Never changes the user's normal playset or saves."""
from pathlib import Path
import argparse, datetime, json, subprocess, sys, time

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
PROFILE=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/cyprus_r2_20261027')
EXPECTED=[]
P='COLDWAR_CYP_R2_'

def check(name,condition):
 EXPECTED.append(name)
 return 'if = { limit = { '+condition+' } log = "CYP_R2_ENGINE PASS '+name+'" } else = { log = "CYP_R2_ENGINE FAIL '+name+'" }\n'

def fixture():
 s='# IMPERIA COLD WAR — Fixture-only transactions, no campaign overrides.\nCYP_R2_ENGINE_run = {\n'
 s+=check('1970_start','IMP_is_1970_scenario = yes has_country_flag = '+P+'initialized western_conservatism_are_in_power = yes')
 for key in ['broken_constitutional_partnership','separate_communal_administrations','divided_national_guard_command','enosis_underground_networks','limited_technical_capacity','makarios_presidential_authority','unficyp_presence','1960_treaty_of_guarantee']:
  s+=check('start_'+key,'has_idea = '+P+'idea_'+key)
 for tag in ['GRE','TUR','ENG']:
  s+=check('treaty_'+tag,tag+' = { has_idea = '+P+'idea_1960_treaty_of_guarantee }')
 s+=P+'republic_apply = yes\n'+check('republic_paid','has_country_flag = '+P+'republic_enacted')
 s+=P+'cabinet_apply = yes\n'+check('cabinet_paid','has_country_flag = '+P+'cabinet_enacted')
 from engine_domestic_fixture import build
 s+=build(check)
 s+='set_variable = { treasury = 1000 } set_variable = { gdp_total = 10 }\n'
 s+=P+'offer_greek_training = yes\nGRE = { '+P+'accept_greek_training = yes }\n'
 s+=check('agreement_paired','has_idea = '+P+'greek_training_cyp GRE = { has_idea = '+P+'greek_training_gre }')
 s+='set_variable = { CYP_R2_ENGINE_treasury = treasury } set_variable = { CYP_R2_ENGINE_pen = '+P+'officer_penetration }\nGRE = { '+P+'accept_greek_training = yes }\n'
 s+=check('accept_once','check_variable = { var = treasury value = CYP_R2_ENGINE_treasury compare = equals } check_variable = { var = '+P+'officer_penetration value = CYP_R2_ENGINE_pen compare = equals }')
 for cls in ['dip','fin','eco','mil']:
  s+='add_to_array = { imp_'+cls+'_sanc_by_us = GRE }\n'+P+'agreements_reconcile = yes\n'
  s+=check('sanction_suspend_'+cls,'NOT = { has_idea = '+P+'greek_training_cyp } GRE = { NOT = { has_idea = '+P+'greek_training_gre } }')
  s+='remove_from_array = { imp_'+cls+'_sanc_by_us = GRE }\n'+P+'agreements_reconcile = yes\n'
  s+=check('sanction_restore_'+cls,'has_idea = '+P+'greek_training_cyp GRE = { has_idea = '+P+'greek_training_gre } check_variable = { var = treasury value = CYP_R2_ENGINE_treasury compare = equals }')
 s+='GRE = { add_to_array = { imp_dip_sanc_by_us = CYP } }\n'+P+'agreements_reconcile = yes\n'
 s+=check('reverse_sanction_suspend','NOT = { has_idea = '+P+'greek_training_cyp } GRE = { NOT = { has_idea = '+P+'greek_training_gre } }')
 s+='GRE = { remove_from_array = { imp_dip_sanc_by_us = CYP } }\n'+P+'agreements_reconcile = yes\n'
 s+='TUR = { set_variable = { treasury = 1000 } set_variable = { gdp_total = 100 } add_political_power = 1000 }\nset_country_flag = '+P+'crisis_active set_country_flag = '+P+'consultation_failed set_country_flag = '+P+'coup_government\n'
 s+='TUR = { '+P+'ACT_tur_operation_apply = yes }\n'
 s+=check('turkish_war','has_war_with = TUR TUR = { has_idea = '+P+'cyprus_intervention_forces has_country_flag = '+P+'intervention_receipt_used }')
 s+='GRE = { set_variable = { treasury = 1000 } set_variable = { gdp_total = 100 } add_political_power = 1000 }\n'
 s+=check('prior_nato_members','GRE = { has_idea = NATO_member } TUR = { has_idea = NATO_member }')
 s+='GRE = { '+P+'ACT_gre_response_apply = yes '+P+'ACT_gre_escalate_apply = yes }\n'
 s+=check('greek_war','GRE = { has_war_with = TUR }')
 s+=check('both_out_nato','GRE = { NOT = { has_idea = NATO_member } has_country_flag = '+P+'nato_separated } TUR = { NOT = { has_idea = NATO_member } has_country_flag = '+P+'nato_separated }')
 s+='GRE = { NATO_join = yes } TUR = { NATO_join_via_event = yes }\n'
 s+=check('premature_join_blocked','GRE = { NOT = { has_idea = NATO_member } } TUR = { NOT = { has_idea = NATO_member } }')
 s+='GRE = { white_peace = TUR }\n'+P+'crisis_reconcile = yes\n'
 s+=check('cyprus_war_still_blocks_return','has_war_with = TUR GRE = { NOT = { has_idea = NATO_member } } TUR = { NOT = { has_idea = NATO_member } }')
 s+='white_peace = TUR\n'+P+'crisis_reconcile = yes\n'
 s+=check('both_return_nato','GRE = { has_idea = NATO_member NOT = { has_country_flag = '+P+'nato_separated } } TUR = { has_idea = NATO_member NOT = { has_country_flag = '+P+'nato_separated } }')
 s+=check('operation_cleaned','TUR = { NOT = { has_idea = '+P+'cyprus_intervention_forces } NOT = { has_country_flag = '+P+'intervention_expense_cached } }')
 s+='log = "CYP_R2_ENGINE COMPLETE"\n}\n'
 return s

def write(rel,s):
 p=PROFILE/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8')

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--timeout',type=int,default=420);args=parser.parse_args()
 descriptor=(ROOT/'descriptor.mod').read_text('utf-8-sig')+'\npath="'+ROOT.as_posix()+'"\n'
 write('mod/mdcoldwar.mod',descriptor)
 addon='name="Cyprus R2 private native fixture"\ndependencies={ "MD Cold War" }\npath="'+(PROFILE/'fixture').as_posix()+'"\n'
 write('mod/cyprus_probe.mod',addon);write('fixture/descriptor.mod',addon)
 write('dlc_load.json',json.dumps({'enabled_mods':['mod/mdcoldwar.mod','mod/cyprus_probe.mod'],'disabled_dlcs':[]}))
 write('settings.txt','language="l_english"\ngraphics={size={x=1280 y=900} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n')
 write('fixture/common/scripted_effects/CYP_R2_ENGINE.txt',fixture())
 write('fixture/common/on_actions/zzzzzzz_CYP_R2_ENGINE.txt','# IMPERIA COLD WAR — Private probe after country initialisation.\non_actions = { on_startup = { effect = { log = "CYP_R2_ENGINE STARTUP" CYP = { CYP_R2_ENGINE_run = yes } } } }\n')
 stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
 for name in ['game.log','error.log']:
  old=PROFILE/'logs'/name
  if old.exists():old.rename(old.with_name(stamp+'_previous_'+name))
  write('logs/'+name,'')
 cmd=[str(GAME/'hoi4.exe'),'-noasserts','-assertsdialog=no','-userdir='+str(PROFILE),'-start_tag=CYP','-start_speed=2','-hands_off']
 startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
 process=subprocess.Popen(cmd,cwd=GAME,startupinfo=startup)
 write('process.json',json.dumps({'pid':process.pid,'args':cmd},indent=2))
 print(json.dumps({'pid':process.pid,'profile':str(PROFILE)}),flush=True)
 start=time.monotonic();complete=None;stopped_by_probe=False
 try:
  while process.poll() is None and time.monotonic()-start<args.timeout:
   time.sleep(1)
   p=PROFILE/'logs/game.log';log=p.read_text('utf-8-sig',errors='replace')if p.exists()else''
   if 'CYP_R2_ENGINE COMPLETE'in log:
    if complete is None:complete=time.monotonic()
    if time.monotonic()-complete>6:break
 finally:
  if process.poll()is None:stopped_by_probe=True;process.terminate()
  try:process.wait(timeout=10)
  except subprocess.TimeoutExpired:process.kill();process.wait()
 p=PROFILE/'logs/game.log';log=p.read_text('utf-8-sig',errors='replace')if p.exists()else''
 p=PROFILE/'logs/error.log';errors=p.read_text('utf-8-sig',errors='replace')if p.exists()else''
 passed=[n for n in EXPECTED if 'CYP_R2_ENGINE PASS '+n in log]
 report={'project':'IMPERIA COLD WAR','scope':'Private native 1970 startup and synchronous installed transaction checks. No manual UI, save/reload or multiplayer claim. Fixture seeds budget and crisis conditions.',
 'profile':str(PROFILE),'elapsed_seconds':round(time.monotonic()-start,1),'returncode':process.returncode,'stopped_by_probe':stopped_by_probe,'completed':'CYP_R2_ENGINE COMPLETE'in log,'expected':EXPECTED,'passed':passed,'failed':[n for n in EXPECTED if n not in passed],
 'checkpoints':[line for line in log.splitlines()if'CYP_R2_ENGINE'in line],
 'relevant_errors':[line for line in errors.splitlines()if any(k in line for k in ['COLDWAR_CYP_R2','CYP_R2_ENGINE','COLDWAR_CYP_1970_focus','COLDWAR_CYP_R2_guarantor'])]}
 report['success']=report['completed']and not report['failed']and not report['relevant_errors']
 old=HERE/'ENGINE_REPORT.json'
 if old.exists():old.rename(HERE/('ENGINE_REPORT_'+stamp+'.json'))
 old.write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
 print(json.dumps({k:report[k]for k in ['success','completed','elapsed_seconds','failed']}|{'passed':len(passed),'relevant_errors':len(report['relevant_errors'])},indent=2),flush=True)

if __name__=='__main__':main()
