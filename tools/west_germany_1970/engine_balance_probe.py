# IMPERIA COLD WAR — Isolated native German balance transaction probe.
"""Private profile only. Does not alter the user's playset, saves or active game."""
from pathlib import Path
import json
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
PROFILE = HERE / 'balance_audit/engine_profile'
EXPECTED = []
PREFIX = 'COLDWAR_GER_BALANCE_ENGINE'


def write(rel, text):
    path = PROFILE / rel; path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')


def check(name, gate):
    EXPECTED.append(name)
    return f'if = {{ limit = {{ {gate} }} log = "{PREFIX} PASS {name}" }} else = {{ log = "{PREFIX} FAIL {name}" }}\n'


def fixture():
    p = 'COLDWAR_GER_1970'
    s = p + '_settlement'
    text = '# IMPERIA COLD WAR — Private native fixtures with a real GER event ROOT.\n'
    text += 'add_namespace = COLDWAR_GER_BALANCE_ENGINE\ncountry_event = { id = COLDWAR_GER_BALANCE_ENGINE.1 hidden = yes is_triggered_only = yes immediate = {\n'
    text += f'log = "{PREFIX} START"\n'
    text += check('1970_loaded', 'IMP_is_1970_scenario = yes country_exists = DDR has_country_flag = cwgg_initialized')
    text += '''set_variable = { cwgg_klima = 0 }
add_political_power = 1000
set_variable = { cwgg_init_brd = 6 }
set_variable = { cwgg_krise_typ = 0 }
set_variable = { ruling_party = 1 }
set_variable = { gdp_total = 500 }
set_variable = { treasury = 10 }
clr_country_flag = cwgg_done_credit
DDR = { set_variable = { cwddr_hard_currency = 60 } set_variable = { cwddr_west_dependency = 10 } }
'''
    text += p + '_rv_act_credit = yes\n'
    text += check('credit_proposal_no_concessions', 'has_country_flag = COLDWAR_GER_1970_balance_credit_pending check_variable = { cwgg_klima = 0 } check_variable = { treasury = 10 } DDR = { check_variable = { cwddr_hard_currency = 60 } }')
    text += 'DDR = { ' + p + '_balance_refuse_credit = yes }\n'
    text += check('credit_refusal_clears_sender', 'NOT = { has_country_flag = COLDWAR_GER_1970_balance_credit_pending } check_variable = { cwgg_klima = 0 }')
    text += 'clr_country_flag = cwgg_done_credit\nset_variable = { cwgg_init_brd = 6 }\n' + p + '_rv_act_credit = yes\nDDR = { ' + p + '_balance_accept_credit = yes }\n'
    text += check('credit_accepts_real_cost', 'check_variable = { treasury = 9.5 } check_variable = { cwgg_klima = 10 } DDR = { check_variable = { cwddr_hard_currency = 45 } }')
    text += 'DDR = { ' + p + '_balance_accept_credit = yes }\n'
    text += check('credit_no_repeat_cost', 'check_variable = { treasury = 9.5 } check_variable = { cwgg_klima = 10 }')
    text += '''set_variable = { cwgg_init_brd = 6 }
set_variable = { cwger_stasi_penetration = 50 }
set_variable = { cwger_counterintel = 35 }
clr_country_flag = cwgg_cd_raid
clr_country_flag = cwger_intel_operation_cd
'''
    text += p + '_rv_act_raid = yes\n'
    text += check('raid_rebalanced', 'check_variable = { cwger_stasi_penetration = 40 } check_variable = { cwger_counterintel = 38 } has_country_flag = cwger_intel_operation_cd')
    text += p + '_sec_act_counterspy = yes\n'
    text += check('second_intel_operation_blocked', 'check_variable = { cwger_stasi_penetration = 40 } check_variable = { cwger_counterintel = 38 }')
    text += '''set_variable = { cwgg_krise_typ = 9 }
set_variable = { cwgg_krise_monat = 0 }
set_variable = { cwgg_krise_runde = 0 }
set_variable = { cwgg_krise_max = 4 }
set_variable = { cwgg_krise_int = 60 }
set_variable = { cwgg_countdown = 0 }
set_variable = { cwgg_brd_order_ready = 1 }
set_variable = { cwgg_ddr_order_ready = 1 }
set_variable = { cwgg_haltung = 1 }
set_variable = { cwgg_ddr_wahl = 2 }
'''
    text += p + '_rv_crisis_clock = yes\n'
    text += check('first_month_no_resolution', 'check_variable = { cwgg_krise_monat = 1 } check_variable = { cwgg_krise_runde = 0 }')
    text += p + '_rv_crisis_clock = yes\n'
    text += check('second_month_resolves', 'check_variable = { cwgg_krise_monat = 0 } check_variable = { cwgg_krise_runde = 1 }')
    text += '''set_variable = { cwgg_krise_typ = 0 }
set_variable = { cwgg_special_used = 0 }
set_variable = { cwgg_countdown = 0 }
set_variable = { cwgg_vertrag_3 = 0 }
set_variable = { cwgg_hebel_recht = 2 }
clr_country_flag = cwgg_crisis_cd
add_ideas = COLDWAR_GER_1970_idea_hallstein_legacy
SWI = { if = { limit = { is_in_array = { recognised_countries = DDR } } remove_from_array = { recognised_countries = DDR } } add_ideas = non_power }
DDR = { COLDWAR_Germany_recount_recognition = yes COLDWAR_Germany_seed_recognition_pp = yes set_temp_variable = { cwgg_engine_pp_before = political_power } }
SWI = { COLDWAR_Germany_recognise_DDR = yes }
'''
    text += check('recogniser_frozen_on_real_crisis', 'check_variable = { cwgg_krise_typ = 5 } is_in_array = { cwgg_recognition_country = SWI }')
    text += p + '_rv_special_5 = yes\n'
    text += check('targeted_sanction_mirrors', 'is_in_array = { array = imp_dip_sanc_by_us value = SWI } SWI = { is_in_array = { array = imp_dip_sanc_on_us value = GER } }')
    text += '''DDR = { set_temp_variable = { cwgg_engine_pp_after = political_power } }
SWI = { remove_from_array = { recognised_countries = DDR } }
DDR = { COLDWAR_Germany_recount_recognition = yes }
SWI = { COLDWAR_Germany_recognise_DDR = yes }
'''
    text += check('recognition_pp_regrant_blocked', 'DDR = { check_variable = { political_power = cwgg_engine_pp_after } }')
    text += '''set_variable = { cwgg_krise_typ = 0 }
set_variable = { cwgg_countdown = 0 }
clr_country_flag = cwgg_settlement_proposal_cd
DDR = { clr_country_flag = cwgg_settlement_proposal_cd }
declare_war_on = { target = DDR type = annex_everything }
SOV = { if = { limit = { NOT = { has_war_with = GER } } declare_war_on = { target = GER type = annex_everything } } }
set_global_flag = cwgg_german_war
'''
    text += s + '_propose_1 = yes\n'
    text += '''for_each_scope_loop = {
 array = cwgg_settlement_participants
 if = { limit = { NOT = { tag = SOV } } COLDWAR_GER_1970_settlement_accept = yes }
}
'''
    text += check('soviet_signature_blocks_peace', 'has_war_with = DDR has_war_with = SOV has_country_flag = cwgg_settlement_pending')
    text += 'SOV = { ' + s + '_accept = yes }\n'
    text += check('unanimous_native_peace', 'NOT = { has_war_with = DDR } NOT = { has_war_with = SOV } NOT = { has_country_flag = cwgg_settlement_pending } country_exists = DDR')
    text += f'log = "{PREFIX} COMPLETE"\n}} }}\n'
    return text


def main():
    write('.gitignore', '# IMPERIA COLD WAR: private native test profile\n*\n')
    write('mod/mdcoldwar.mod', '# IMPERIA COLD WAR — Private profile reference to the live mod.\n' + (ROOT / 'descriptor.mod').read_text(encoding='utf-8-sig') + '\npath="' + ROOT.as_posix() + '"\n')
    addon = '# IMPERIA COLD WAR — Isolated native balance fixtures.\nname="German balance native probe"\ndependencies={ "MD Cold War" }\npath="' + (PROFILE / 'fixture').as_posix() + '"\n'
    write('mod/balance_probe.mod', addon); write('fixture/descriptor.mod', addon)
    write('dlc_load.json', json.dumps(dict(enabled_mods=['mod/mdcoldwar.mod', 'mod/balance_probe.mod'], disabled_dlcs=[])))
    write('settings.txt', '# IMPERIA COLD WAR — Private muted test window.\nlanguage="l_english"\ngraphics={size={x=1280 y=900} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n')
    write('fixture/events/COLDWAR_GER_BALANCE_ENGINE.txt', fixture())
    write('fixture/common/on_actions/zzzzzz_COLDWAR_GER_BALANCE_ENGINE.txt', '# IMPERIA COLD WAR — Private post-startup probe.\non_actions = { on_startup = { effect = { GER = { country_event = { id = COLDWAR_GER_BALANCE_ENGINE.1 days = 1 } } } } }\n')
    for name in ('game.log', 'error.log'): write('logs/' + name, '')
    args = [str(GAME / 'hoi4.exe'), '-debug', '-noasserts', '-assertsdialog=no', '-userdir=' + str(PROFILE), '-start_tag=GER', '-start_speed=2', '-hands_off']
    startup = subprocess.STARTUPINFO(); startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW; startup.wShowWindow = 0
    started = time.monotonic(); process = subprocess.Popen(args, cwd=GAME, startupinfo=startup)
    print(json.dumps(dict(pid=process.pid, private_profile=str(PROFILE))), flush=True)
    try:
        while process.poll() is None and time.monotonic() - started < 420:
            time.sleep(1)
            path = PROFILE / 'logs/game.log'
            text = path.read_text(encoding='utf-8-sig', errors='replace') if path.exists() else ''
            if PREFIX + ' COMPLETE' in text: break
    finally:
        if process.poll() is None: process.terminate()
        try: process.wait(timeout=10)
        except subprocess.TimeoutExpired: process.kill(); process.wait()
    game_log = (PROFILE / 'logs/game.log').read_text(encoding='utf-8-sig', errors='replace')
    errors = (PROFILE / 'logs/error.log').read_text(encoding='utf-8-sig', errors='replace')
    passed = [key for key in EXPECTED if PREFIX + ' PASS ' + key in game_log]
    failed = [key for key in EXPECTED if key not in passed]
    # IMPERIA COLD WAR — Native errors can concatenate multiple records without newlines.
    records = re.split(r'(?=\[\d{2}:\d{2}:\d{2}\]\[)', errors)
    relevant = [record.strip() for record in records if any(key in record for key in ('COLDWAR_GER_1970_balance', 'cwgg_settlement_', 'recognition_pp_', 'COLDWAR_GER_BALANCE', 'COLDWAR_diplomacy_1970')) and 'Reloading Events:' not in record]
    assertions = [record.strip() for record in records if 'assertion failed:' in record]
    report = dict(project='IMPERIA COLD WAR', passed=passed, failed=failed, relevant_errors=relevant,
                  completed=PREFIX + ' COMPLETE' in game_log, elapsed_seconds=round(time.monotonic() - started, 1),
                  general_assertions=assertions,
                  scope='Actual native 1970 profile, GER event ROOT, direct installed transactions. No manual tooltip, real save/reload or multiplayer claim.')
    report['success'] = report['completed'] and not failed and not relevant
    (HERE / 'balance_audit/engine_report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__': main()
