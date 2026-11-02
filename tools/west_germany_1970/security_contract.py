# IMPERIA COLD WAR — Native trigger compatibility integration.
# IMPERIA CW — Cold War: authoritative German RAF lifecycle and programme contract.
"""Shared by the national tree, German cabinet and international contact file.

Legacy programme flag names remain valid for existing saves. The sole monthly
owner is COLDWAR_GER_1970_monthly; common contact updates never tick the RAF.
"""
import json
from pathlib import Path
from cw_lib import P, L

HERE=Path(__file__).resolve().parent
PROGRAMMES=json.loads((HERE.parent/'colonial_affairs/raf_programmes.json').read_text(encoding='utf-8'))
RAF_ACTIONS={'raster','reward','posters','kronzeuge','informant','forcefeed','dropout','kinkel','storm','safehouse','contactban','stall','givein'}
HEADER='# IMPERIA CW — Cold War: unified German RAF security contract.\n'


def block(name,body):return name+' = {\n'+body+'\n}\n'
def iff(gate,body):return block('if','limit = { '+gate+' }\n'+body)


def triggers():
    out=block(P+'_raf_case_active',f'''original_tag = GER
IMP_is_1970_scenario = yes
has_country_flag = {P}_initialized
date > 1970.5.13
NOT = {{ has_country_flag = {P}_raf_dissolved }}
NOT = {{ has_country_flag = COLDWAR_COL_raf_settlement }}
check_variable = {{ cwger_raf_gen > 0 }}
check_variable = {{ cwger_raf_gen < 4 }}''')
    for row in PROGRAMMES:
        key=row['id'];flag='COLDWAR_COL_measure_'+key
        gate=f'''{P}_raf_case_active = yes
has_country_flag = cwsec_initialized
OR = {{ has_country_flag = {row['unlock']} has_completed_focus = {P}_{row['focus']} }}
NOT = {{ has_country_flag = {flag}_cooldown }}
NOT = {{ has_political_power < {row['pp']} }}
NOT = {{ has_country_flag = MD_skip_treasury_cost }}
check_variable = {{ var = treasury value = {row['cash']} compare = greater_than_or_equals }}
{row['guard']}'''
        out+=block(P+'_sec_can_'+key,gate)
    return HEADER+out


def traces(amount):
    return '\n'.join(iff(f'check_variable = {{ cwsec_w{i}_st < 2 }}',f'add_to_variable = {{ cwsec_w{i}_ort = {amount} }}\nclamp_variable = {{ var = cwsec_w{i}_ort min = 0 max = 100 }}') for i in range(1,7))


def effects():
    reconcile=''
    # Focus receipts are reconciled without replaying any PP, buildings or bonuses.
    for row in PROGRAMMES:
        reconcile+=iff(f'has_completed_focus = {P}_{row["focus"]}',f'set_country_flag = {row["unlock"]}')
    cleanup='\n'.join('clr_country_flag = COLDWAR_COL_measure_'+r['id']+'_live' for r in PROGRAMMES)
    cleanup+='\nset_variable = { COLDWAR_COL_raf_aid = 0 }\nset_variable = { cwsec_program_weekly_cost = 0 }\n'
    cleanup+='\n'.join(f'set_variable = {{ cwsec_plan_{key} = 0 }}' for key in ('justice','business','usforces','politics','infra','embassy'))
    cleanup+=f'\nclr_country_flag = {P}_hostage_ultimatum\nclr_country_flag = {P}_hostage_crisis_active\nset_variable = {{ cwsec_ult_days = 0 }}'
    reconcile+=iff(P+'_raf_case_active = no',cleanup)
    out=block(P+'_security_reconcile',iff(f'original_tag = GER IMP_is_1970_scenario = yes has_country_flag = {P}_initialized',reconcile+f'\n{P}_sec_reconcile_custody = yes'))
    # Aggregate prisoner counts include earlier generations outside the six
    # current cards. Only remove excess custody cards; never invent prisoners.
    custody='set_temp_variable = { cwsec_tracked_custody = 0 }\n'
    for i in range(1,7):custody+=iff(f'check_variable = {{ cwsec_w{i}_st = 2 }}','add_to_temp_variable = { cwsec_tracked_custody = 1 }')
    for i in range(1,7):
        custody+=iff(f'check_variable = {{ cwsec_w{i}_st = 2 }} check_variable = {{ var = cwsec_tracked_custody value = cwger_raf_prisoners compare = greater_than }}',f'set_variable = {{ cwsec_w{i}_st = 5 }}\nsubtract_from_temp_variable = {{ cwsec_tracked_custody = 1 }}')
    out+=block(P+'_sec_reconcile_custody',custody)
    cost='set_variable = { cwsec_program_weekly_cost = 0 }\n'
    cost+=iff(P+'_raf_case_active = yes','\n'.join(iff('has_country_flag = COLDWAR_COL_measure_'+r['id']+'_live',f'add_to_variable = {{ cwsec_program_weekly_cost = {r["weekly"]} }}') for r in PROGRAMMES))
    out+=block(P+'_security_weekly_budget',cost)
    monthly='''COLDWAR_COL_refresh_raf_aid = yes
set_temp_variable = { COLDWAR_COL_raf_reinforcement = COLDWAR_COL_raf_aid }
multiply_temp_variable = { COLDWAR_COL_raf_reinforcement = 0.05 }
add_to_variable = { cwger_raf_cadre = COLDWAR_COL_raf_reinforcement }
clamp_variable = { var = cwger_raf_cadre min = 0 max = 120 }
'''
    monthly+=iff('has_country_flag = COLDWAR_COL_measure_coordination_live',traces(1))
    monthly+=iff('has_country_flag = COLDWAR_COL_measure_judicial_live','add_to_variable = { cwger_raf_milieu = -0.25 }\nclamp_variable = { var = cwger_raf_milieu min = 0 max = 100 }')
    out+=block(P+'_security_external_monthly',iff(P+'_raf_case_active = yes',monthly))
    # A read-only derived threat can be refreshed after a focus/action/payment
    # without executing recruitment, arrests, attacks or programme ticks again.
    threat='set_variable = { cwger_terror_left = 0 }\n'
    threat+=iff(P+'_raf_case_active = yes','''set_variable = { cwger_terror_left = cwger_raf_cadre }
multiply_variable = { cwger_terror_left = 0.9 }
set_temp_variable = { cwsec_threat_milieu = cwger_raf_milieu }
multiply_temp_variable = { cwsec_threat_milieu = 0.35 }
add_to_variable = { cwger_terror_left = cwsec_threat_milieu }''')
    threat+=f'''if = {{ limit = {{ NOT = {{ has_country_flag = {P}_j2m_dissolved }} date < 1980.6.2 }} add_to_variable = {{ cwger_terror_left = 5 }} }}
if = {{ limit = {{ NOT = {{ has_country_flag = {P}_rz_dissolved }} date > 1973.1.1 date < 1995.1.1 }} add_to_variable = {{ cwger_terror_left = 4 }} }}
clamp_variable = {{ var = cwger_terror_left min = 0 max = 100 }}'''
    out+=block(P+'_security_refresh_threat',threat)
    for row in PROGRAMMES:
        key=row['id'];flag='COLDWAR_COL_measure_'+key
        code=f'''add_political_power = -{row['pp']}
set_temp_variable = {{ treasury_change = -{row['cash']} }}
modify_treasury_effect = yes
set_country_flag = {{ flag = {flag}_cooldown days = {row['cd']} }}
set_country_flag = {{ flag = {flag}_live days = {row['days']} }}
{row['result']}
'''
        if key=='coordination':code+=traces(8)
        code+='\n'+'\n'.join(f'clamp_variable = {{ var = {v} min = 0 max = 100 }}' for v in ('cwger_raf_milieu','cwger_rechtsstaat','cwger_security','cwsec_hunger'))
        code+=f'\n{P}_security_weekly_budget = yes\n{P}_sec_gui_refresh = yes'
        out+=block(P+'_sec_act_'+key,f'{P}_security_reconcile = yes\n'+iff(P+'_sec_can_'+key+' = yes',code))
    return HEADER+out


def localise():
    L(P+'_security_programmes','Security Programmes')
    L(P+'_security_programme_cost','Additional programmes: §Y$[?cwsec_program_weekly_cost|3]bn/week§!')
    for row in PROGRAMMES:
        name=P+'_security_programme_'+row['id']
        focus_label={'bka_expansion':'BKA Expansion','data_protection':'Data Protection','stammheim_trial':'The Stammheim Trial'}[row['focus']]
        L(name,{'coordination':'Case Coordination','judicial':'Judicial Review','medical':'Medical Review'}[row['id']])
        L(name+'_tt',row['name']+'\n'+row['terms']+'\n'+row['detail']+'\nRequires §Y'+focus_label+'§!.')
        L(name+'_terms',f"{row['pp']} PP / ${float(row['cash']):.3f}bn\n${float(row['weekly']):.3f}bn/week / {row['days']} days")
    L('cwgg_sec_raf_inactive','The RAF case is not active. Formation: 14 May 1970; closed cases do not recruit or plan attacks.')


def files():
    localise()
    # Refresh owns reconciliation, derived values and the guarded open-window
    # calculation. This also updates date/expiry gates and a closed hostage bar.
    daily=f'on_actions = {{ on_daily = {{ effect = {{ if = {{ limit = {{ original_tag = GER IMP_is_1970_scenario = yes has_country_flag = {P}_initialized }} {P}_sec_gui_refresh = yes }} }} }} }}\n'
    return {f'common/scripted_effects/{P}_security_contract.txt':effects(),f'common/scripted_triggers/{P}_security_contract.txt':triggers(),f'common/on_actions/{P}_security_contract.txt':HEADER+daily}
