# IMPERIA CW — Cold War: isolated native Japan mechanics probe.
"""Run an addon in a separate user directory; never alter the user's playset."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time
import ctypes

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
GAME=Path('C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV')
MARKER='COLDWAR_JAP70_ENGINE_PROBE'


def prepare(phase):
    profile=HERE/'runtime_probe'/phase
    addon=profile/'fixture'
    for folder in ('mod','fixture/common/on_actions','fixture/events','fixture/common/scripted_effects'):
        (profile/folder).mkdir(parents=True,exist_ok=True)
    (HERE/'runtime_probe/.gitignore').write_text('*\n',encoding='utf-8')
    # Preserve all replace_path directives; otherwise vanilla states and
    # scripted databases merge with MD and fail before any test can run.
    base=(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig')+'\npath="'+ROOT.as_posix()+'"\n'
    overlay='name="COLDWAR Japan isolated probe"\ndependencies={"MD Cold War"}\npath="'+addon.as_posix()+'"\n'
    (profile/'mod/base.mod').write_text(base,encoding='utf-8')
    (profile/'mod/probe.mod').write_text(overlay,encoding='utf-8')
    (addon/'descriptor.mod').write_text(overlay,encoding='utf-8')
    (profile/'dlc_load.json').write_text(json.dumps({'enabled_mods':['mod/base.mod','mod/probe.mod'],'disabled_dlcs':[]}),encoding='utf-8')
    (profile/'settings.txt').write_text('language="l_english"\ngraphics={size={x=1280 y=720} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n',encoding='utf-8')
    # Preserve the exact tested donor helpers/events for this run while work on
    # later repairs continues. Instrumentation changes logging only.
    helpers=ROOT/'common/scripted_effects/COLDWAR_JAP70_bilateral_effects.txt'
    (addon/'common/scripted_effects'/helpers.name).write_bytes(helpers.read_bytes())
    events=(ROOT/'events/COLDWAR_JAP70_bilateral_events.txt').read_text(encoding='utf-8')
    events=events.replace('id = COLDWAR_JAP70_BILATERAL.7117\n','id = COLDWAR_JAP70_BILATERAL.7117\n immediate = { log = "'+MARKER+' DELIVERED claims country=[ROOT.GetTag]" }\n')
    for outcome in ('accept','refuse'):
        events=events.replace('name = COLDWAR_JAP70_BIL_korea_claims_commission_'+outcome,
            'log = "'+MARKER+' RESPONSE claims '+outcome+' country=[ROOT.GetTag]"\n  name = COLDWAR_JAP70_BIL_korea_claims_commission_'+outcome)
    (addon/'events/COLDWAR_JAP70_bilateral_events.txt').write_text(events,encoding='utf-8')
    if (ROOT/'events/COLDWAR_JAP70_diplomatic_reports.txt').exists():
        import re
        reports=(ROOT/'events/COLDWAR_JAP70_diplomatic_reports.txt').read_text(encoding='utf-8')
        report_map={r['event']:r for r in json.loads((HERE/'staging/foreign/diplomatic_reports_manifest.json').read_text(encoding='utf-8'))}
        def instrument_report(match):
            data=report_map[match.group(1)]
            return match.group()+f'\timmediate = {{ log = "COLDWAR_JAP70_ENGINE_PROBE REPORT {data["focus"]} {data["outcome"]} country=[ROOT.GetTag] sender=[FROM.GetTag]" }}\n'
        reports=re.sub(r'\bid = (COLDWAR_JAP70_REPORT\.\d+)\n',instrument_report,reports)
        (addon/'events/COLDWAR_JAP70_diplomatic_reports.txt').write_text(reports,encoding='utf-8')
    hook='''# IMPERIA CW — Cold War: isolated Japan engine assertions.
on_actions = { on_startup = { effect = {
 log = "COLDWAR_JAP70_ENGINE_PROBE START"
 JAP = {
  if = { limit = { IMP_is_1970_scenario = yes } log = "COLDWAR_JAP70_ENGINE_PROBE PASS campaign" }
  else = { log = "COLDWAR_JAP70_ENGINE_PROBE FAIL campaign" }
  clr_country_flag = MD_skip_treasury_cost
  set_variable = { treasury = 1000 }
  set_variable = { gdp_total = 10 }
  complete_national_focus = COLDWAR_JAP_1970_korea_policy_review
  complete_national_focus = COLDWAR_JAP_1970_seoul_relations
  complete_national_focus = COLDWAR_JAP_1970_korea_claims_commission
  if = { limit = { has_country_flag = COLDWAR_JAP70_FOREIGN_korea_claims_commission_offer_receipt }
   log = "COLDWAR_JAP70_ENGINE_PROBE PASS focus_dispatched_claims" }
  else = { log = "COLDWAR_JAP70_ENGINE_PROBE FAIL focus_dispatched_claims" }
  if = { limit = { KOR = { has_country_flag = COLDWAR_JAP70_BIL_korea_claims_commission_pending } }
   log = "COLDWAR_JAP70_ENGINE_PROBE PASS recipient_pending_claims" }
  else = { log = "COLDWAR_JAP70_ENGINE_PROBE FAIL recipient_pending_claims" }
  log = "COLDWAR_JAP70_ENGINE_PROBE treasury_after_dispatch=[?treasury]"
 }
 log = "COLDWAR_JAP70_ENGINE_PROBE INITIAL_CHECKS_DONE"
} } }
'''
    if phase=='verified':
        extra='''JAP = {
 set_variable = { treasury = 0 }
 617 = { set_variable = { COLDWAR_JAP70_probe_before = building_level@industrial_complex } }
 complete_national_focus = COLDWAR_JAP_1970_hokkaido_processing
 if = { limit = { check_variable = { treasury = -8.5 } }
  log = "COLDWAR_JAP70_ENGINE_PROBE PASS negative_treasury_payment" }
 else = { log = "COLDWAR_JAP70_ENGINE_PROBE FAIL negative_treasury_payment treasury=[?treasury]" }
 617 = {
  set_variable = { COLDWAR_JAP70_probe_increase = building_level@industrial_complex }
  subtract_from_variable = { COLDWAR_JAP70_probe_increase = COLDWAR_JAP70_probe_before }
  if = { limit = { check_variable = { COLDWAR_JAP70_probe_increase = 1 } }
   log = "COLDWAR_JAP70_ENGINE_PROBE PASS actual_hokkaido_factory" }
  else = { log = "COLDWAR_JAP70_ENGINE_PROBE FAIL actual_hokkaido_factory" }
 }
 COLDWAR_JAP_1970_hokkaido_processing_apply = yes
 if = { limit = { check_variable = { treasury = -8.5 } }
  log = "COLDWAR_JAP70_ENGINE_PROBE PASS no_repeated_payment" }
 else = { log = "COLDWAR_JAP70_ENGINE_PROBE FAIL no_repeated_payment" }
 complete_national_focus = COLDWAR_JAP_1970_ldp_policy_0
 if = { limit = { check_variable = { COLDWAR_JAP_1970_LDP_agricolture_productivity_modifier = 0.04 } }
  log = "COLDWAR_JAP70_ENGINE_PROBE PASS party_programme_variable" }
 else = { log = "COLDWAR_JAP70_ENGINE_PROBE FAIL party_programme_variable" }
 complete_national_focus = COLDWAR_JAP_1970_article9_debate
 if = { limit = { has_variable = COLDWAR_JAP_1970_article9_support has_country_flag = COLDWAR_JAP_1970_article9_debate_open }
  log = "COLDWAR_JAP70_ENGINE_PROBE PASS constitutional_campaign_open" }
 else = { log = "COLDWAR_JAP70_ENGINE_PROBE FAIL constitutional_campaign_open" }
 set_country_flag = COLDWAR_JAP70_FOREIGN_china_technology_exchange_offer_receipt
 complete_national_focus = COLDWAR_JAP_1970_china_technology_exchange
 COLDWAR_JAP70_restore_unanswered_offers = yes
 if = { limit = { has_country_flag = COLDWAR_JAP70_response_recovery_v1 CHI = { has_country_flag = COLDWAR_JAP70_BIL_china_technology_exchange_pending } }
  log = "COLDWAR_JAP70_ENGINE_PROBE PASS orphaned_completed_offer_recovered" }
 else = { log = "COLDWAR_JAP70_ENGINE_PROBE FAIL orphaned_completed_offer_recovered" }
 set_variable = { COLDWAR_JAP70_probe_before_recovery = treasury }
 COLDWAR_JAP70_restore_unanswered_offers = yes
 if = { limit = { check_variable = { var = treasury value = COLDWAR_JAP70_probe_before_recovery compare = equals } }
  log = "COLDWAR_JAP70_ENGINE_PROBE PASS recovery_has_no_payment" }
 else = { log = "COLDWAR_JAP70_ENGINE_PROBE FAIL recovery_has_no_payment" }
}
'''
        hook=hook.replace(' log = "COLDWAR_JAP70_ENGINE_PROBE INITIAL_CHECKS_DONE"',extra+' log = "COLDWAR_JAP70_ENGINE_PROBE INITIAL_CHECKS_DONE"')
    from check_script_grammar import parse
    from presentation import field
    for p in (addon/'events').glob('*.txt'):
        for item in parse(p.read_text(encoding='utf-8')):
            if item.key not in ('add_namespace','country_event','news_event'):raise ValueError('Invalid snapshot top-level '+str(p))
            if item.key=='country_event' and field(item.value,'hidden')!='yes' and not any(e.key=='option' for e in item.value):raise ValueError('Snapshot event lacks options '+str(p))
    (addon/'common/on_actions/000_COLDWAR_JAP70_engine_probe.txt').write_text(hook,encoding='utf-8')
    return profile


def run(profile,phase):
    log=profile/'logs/game.log'
    errors=profile/'logs/error.log'
    for p in (log,errors):
        if p.exists():p.write_text('',encoding='utf-8')
    startup=subprocess.STARTUPINFO()
    startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow=0
    # The engine's Windows profile switch does not tolerate this long path's
    # spaces reliably. Use the existing filesystem short path and verify that
    # its own log directory appears before allowing the test to continue.
    short=ctypes.create_unicode_buffer(32768)
    if not ctypes.windll.kernel32.GetShortPathNameW(str(profile),short,len(short)) or ' ' in short.value:
        raise RuntimeError('A space-free isolated profile path is unavailable')
    args=[str(GAME/'hoi4.exe'),'-debug','-noasserts','-assertsdialog=no',
          '-userdir='+short.value,'-start_tag=JAP','-start_speed=1','-hands_off']
    start=time.time()
    process=subprocess.Popen(args,cwd=GAME,startupinfo=startup)
    print(json.dumps({'phase':phase,'pid':process.pid,'profile':str(profile)}),flush=True)
    reached=None
    stopped_by_probe=False
    try:
        while process.poll() is None and time.time()-start<360:
            time.sleep(1)
            if time.time()-start>30 and not log.exists():
                print('Isolated profile was not selected; stopping this attempt.',flush=True)
                break
            text=log.read_text(encoding='utf-8-sig',errors='replace') if log.exists() else ''
            if MARKER+' INITIAL_CHECKS_DONE' in text and reached is None:reached=time.time()
            if MARKER+' REPORT korea_claims_commission accepted country=JAP sender=KOR' in text or reached and time.time()-reached>45:break
    finally:
        if process.poll() is None:
            stopped_by_probe=True
            process.terminate()
        try:process.wait(timeout=10)
        except subprocess.TimeoutExpired:process.kill();process.wait()
    text=log.read_text(encoding='utf-8-sig',errors='replace') if log.exists() else ''
    err=errors.read_text(encoding='utf-8-sig',errors='replace') if errors.exists() else ''
    report={'phase':phase,'elapsed_seconds':round(time.time()-start,1),
            'checkpoints':[l for l in text.splitlines() if MARKER in l],
            'module_errors':[l for l in err.splitlines() if 'COLDWAR_JAP' in l],
            'returncode':process.returncode,'stopped_by_probe':stopped_by_probe,
            'scope':'Isolated engine startup/effect probe; not a UI or multiplayer session'}
    expected=['campaign','focus_dispatched_claims','recipient_pending_claims']
    if phase=='verified':expected+=['negative_treasury_payment','actual_hokkaido_factory','no_repeated_payment','party_programme_variable','constitutional_campaign_open','orphaned_completed_offer_recovered','recovery_has_no_payment']
    report['all_expected_checks_pass']=all(MARKER+' PASS '+name in text for name in expected) and MARKER+' FAIL ' not in text
    report['claims_response_received_in_Japan']=MARKER+' REPORT korea_claims_commission accepted country=JAP sender=KOR' in text
    report['success']=report['all_expected_checks_pass'] and report['claims_response_received_in_Japan'] and not report['module_errors']
    (HERE/f'ENGINE_{phase.upper()}_REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--phase',default='baseline')
    parser.add_argument('--run',action='store_true')
    args=parser.parse_args()
    profile=prepare(args.phase)
    if args.run:run(profile,args.phase)
    else:print(profile)
