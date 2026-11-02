# IMPERIA COLD WAR — COMECON human authority, sealed terms and passive recipients
from build import *

def compile_triggers():
    out=[MARK+' human funding and sealed agreement authority']
    out.append(block('cc_member_country','exists = yes NOT = { COLDWAR_SOV_is_union_republic = yes } is_in_array = { array = global.cc_members value = THIS } OR = { has_idea = cc_member has_idea = COLDWAR_CUB_cmea_member }'))
    out.append(block('cc_human_member','is_ai = no cc_member_country = yes'))
    out.append(block('cc_access','OR = { cc_member_country = yes COLDWAR_SOV_is_union_republic = yes }'))
    out.append(block('cc_launcher_access','OR = { has_global_flag = cc_initialized country_exists = SOV }'))
    out.append(block('cc_secretariat','custom_trigger_tooltip = { tooltip = cc_secretariat_tt cc_human_member = yes check_variable = { THIS.id = global.cc_chair } }'))
    out.append(block('cc_clock_alive','NOT = { check_variable = { global.cc_clock = 0 } } var:global.cc_clock = { exists = yes }'))
    for s in range(1,5):
        out += [block(f'cc_{s}_editable',f'cc_secretariat = yes hidden_trigger = {{ check_variable = {{ global.cc_{s}_phase = 0 }} }}'),
            block(f'cc_{s}_participant',f'cc_human_member = yes check_variable = {{ cc_{s}_share > 0 }}'),
            block(f'cc_{s}_voter',f'''cc_human_member = yes OR = {{
AND = {{ check_variable = {{ global.cc_{s}_phase = 0 }} OR = {{ cc_{s}_participant = yes check_variable = {{ THIS.id = global.cc_{s}_host }} check_variable = {{ global.cc_{s}_founding = 1 }} }} }}
AND = {{ check_variable = {{ global.cc_{s}_phase > 0 }} is_in_array = {{ array = global.cc_{s}_signatories value = THIS }} }} }}'''),
            block(f'cc_{s}_receiving_country',f'is_in_array = {{ array = global.cc_{s}_receivers value = THIS }}'),
            block(f'cc_{s}_ai_consent','always = no'),
            block(f'cc_{s}_allocation_valid',f'OR = {{ NOT = {{ tag = SOV }} var:cc_{s}_recipient = {{ OR = {{ tag = SOV COLDWAR_SOV_is_union_republic = yes }} }} }}'),
            block(f'cc_{s}_signed',f'cc_{s}_voter = yes check_variable = {{ cc_{s}_vote_revision = global.cc_{s}_revision }}'),
            block(f'cc_{s}_receiver_consent',f'''OR = {{ is_ai = yes AND = {{ is_ai = no OR = {{ cc_{s}_signed = yes
AND = {{ NOT = {{ cc_{s}_voter = yes }} check_variable = {{ cc_{s}_local_revision = global.cc_{s}_revision }} }} }} }} }}'''),
            block(f'cc_{s}_seen_terms',f'custom_trigger_tooltip = {{ tooltip = cc_reviewed_terms_tt is_ai = no check_variable = {{ cc_{s}_seen_revision = global.cc_{s}_revision }} }}'),
            block(f'cc_{s}_can_review',f'''cc_{s}_editable = yes
custom_trigger_tooltip = {{ tooltip = cc_financing_covered_tt check_variable = {{ global.cc_{s}_coverage = 100 }} }}
custom_trigger_tooltip = {{ tooltip = cc_human_funder_tt check_variable = {{ global.cc_{s}_participants > 0 }} }}
custom_trigger_tooltip = {{ tooltip = cc_ready_sites_tt check_variable = {{ global.cc_{s}_asset_invalid = 0 }} }}'''),
            block(f'cc_{s}_can_ratify',f'''cc_secretariat = yes hidden_trigger = {{ check_variable = {{ global.cc_{s}_phase = 1 }} }}
custom_trigger_tooltip = {{ tooltip = cc_financing_covered_tt check_variable = {{ global.cc_{s}_coverage = 100 }} }}
custom_trigger_tooltip = {{ tooltip = cc_human_funder_tt check_variable = {{ global.cc_{s}_participants > 0 }} }}
custom_trigger_tooltip = {{ tooltip = cc_signed_sites_tt check_variable = {{ global.cc_{s}_invalid = 0 }} }}''')]
        for assetcheck in (True,False):
            cases=[]
            for i,(p,o) in enumerate(OFFERS,1):
                for t in range(3):
                    host=cv('THIS.id','=',f'global.cc_{s}_host')
                    ordinary=target_conditions(s,p,o,t,False,assetcheck);hosted=target_conditions(s,p,o,t,True,assetcheck)
                    cases.append(f'AND = {{ {cv(f"global.cc_{s}_offer","=",i)} {cv(f"global.cc_{s}_tier","=",t+1)} OR = {{ AND = {{ {host} {hosted} }} AND = {{ NOT = {{ {host} }} {ordinary} }} }} }}')
            out.append(block(f'cc_{s}_target_'+('valid' if assetcheck else 'operating'),'OR = { '+'\n'.join(cases)+' }'))
    from elections import compile_election_triggers
    out.append(compile_election_triggers())
    return '\n'.join(out)

def compile_governance(out):
    from mechanics import each,participants,recipients,refresh
    election='''set_variable = { global.cc_clock = 0 }
SOV = { if = { limit = { exists = yes } set_variable = { global.cc_clock = THIS.id } } }
for_each_scope_loop = { array = global.cc_members if = { limit = { exists = yes check_variable = { global.cc_clock = 0 } } set_variable = { global.cc_clock = THIS.id } } }
if = { limit = { NOT = { check_variable = { global.cc_ballot_winner = 0 } } var:global.cc_ballot_winner = { cc_human_member = yes } } set_variable = { global.cc_chair = global.cc_ballot_winner } }
if = { limit = { NOT = { cc_chair_alive = yes } }
set_variable = { global.cc_chair = 0 }
SOV = { if = { limit = { cc_human_member = yes } set_variable = { global.cc_chair = THIS.id } } }
for_each_scope_loop = { array = global.cc_members if = { limit = { cc_human_member = yes check_variable = { global.cc_chair = 0 } } set_variable = { global.cc_chair = THIS.id } } } }'''
    out.append(block('cc_update_authority',election))
    migrate=['if = { limit = { NOT = { has_global_flag = cc_safety_v2 } } cc_update_authority = yes']
    for s in range(1,5):
        migrate += [f'if = {{ limit = {{ check_variable = {{ global.cc_{s}_phase < 2 }} }} '+each(s,f'if = {{ limit = {{ is_ai = yes }} set_variable = {{ cc_{s}_share = 0 }} }}')+f' set_variable = {{ global.cc_{s}_phase = 0 }} add_to_variable = {{ global.cc_{s}_revision = 1 }} }} else = {{',
            f'clear_array = global.cc_{s}_receivers clear_array = global.cc_{s}_parties clear_array = global.cc_{s}_signatories',
            participants(s,f'''add_to_array = {{ global.cc_{s}_parties = THIS }} add_to_array = {{ global.cc_{s}_signatories = THIS }}
if = {{ limit = {{ is_ai = yes }} set_variable = {{ cc_{s}_vote_revision = -1 }} }}
var:cc_{s}_recipient = {{ if = {{ limit = {{ NOT = {{ is_in_array = {{ array = global.cc_{s}_receivers value = THIS }} }} }} add_to_array = {{ global.cc_{s}_receivers = THIS }} }} }}'''),
            recipients(s,f'if = {{ limit = {{ NOT = {{ is_in_array = {{ array = global.cc_{s}_parties value = THIS }} }} }} add_to_array = {{ global.cc_{s}_parties = THIS }} }}'),
            f'cc_{s}_check_operating = yes }}']
    migrate += ['set_global_flag = cc_safety_v2 }']
    out.append(block('cc_migrate_safety','\n'.join(migrate)))
    for s in range(1,5):
        ready=[var(f'global.cc_{s}_asset_invalid',0),var(f'global.cc_{s}_invalid',0),
            f'var:global.cc_{s}_host = {{ if = {{ limit = {{ NOT = {{ cc_access = yes }} }} add_to_variable = {{ global.cc_{s}_asset_invalid = 1 }} }} }}',
            recipients(s,f'if = {{ limit = {{ NOT = {{ cc_access = yes cc_{s}_target_valid = yes }} }} add_to_variable = {{ global.cc_{s}_asset_invalid = 1 }} }}'),
            each(s,f'if = {{ limit = {{ cc_{s}_voter = yes NOT = {{ cc_{s}_signed = yes }} }} add_to_variable = {{ global.cc_{s}_invalid = 1 }} }}'),
            recipients(s,f'if = {{ limit = {{ NOT = {{ cc_{s}_receiver_consent = yes }} }} add_to_variable = {{ global.cc_{s}_invalid = 1 }} }}'),
            participants(s,f'if = {{ limit = {{ NOT = {{ cc_human_member = yes cc_{s}_allocation_valid = yes }} }} add_to_variable = {{ global.cc_{s}_invalid = 1 }} }}'),
            f'add_to_variable = {{ global.cc_{s}_invalid = global.cc_{s}_asset_invalid }}']
        out.append(block(f'cc_{s}_check_readiness','\n'.join(ready)))
        seal=f'''if = {{ limit = {{ cc_human_member = yes }} cc_update_authority = yes cc_{s}_rebuild = yes
if = {{ limit = {{ cc_{s}_can_review = yes }} cc_{s}_validate_partners = yes
if = {{ limit = {{ check_variable = {{ global.cc_{s}_valid = 1 }} }}
clear_array = global.cc_{s}_payers clear_array = global.cc_{s}_signatories
{each(s,f'if = {{ limit = {{ cc_{s}_participant = yes }} add_to_array = {{ global.cc_{s}_payers = THIS }} }} if = {{ limit = {{ cc_{s}_voter = yes }} add_to_array = {{ global.cc_{s}_signatories = THIS }} }}')}
set_variable = {{ global.cc_{s}_phase = 1 }} add_to_variable = {{ global.cc_{s}_revision = 1 }} cc_{s}_rebuild = yes }} }} }}'''
        out.append(block(f'cc_{s}_open_review',seal))
        out.append(block(f'cc_{s}_reopen',f'cc_update_authority = yes if = {{ limit = {{ cc_secretariat = yes check_variable = {{ global.cc_{s}_phase = 1 }} }} set_variable = {{ global.cc_{s}_phase = 0 }} cc_{s}_revise = yes }}'))
        out.append(block(f'cc_{s}_acknowledge',f'if = {{ limit = {{ is_ai = no OR = {{ cc_{s}_voter = yes cc_{s}_receiving_country = yes }} check_variable = {{ global.cc_{s}_phase > 0 }} }} set_variable = {{ cc_{s}_seen_revision = global.cc_{s}_revision }} cc_touch = yes }}'))
        for name,value in [('approve',f'global.cc_{s}_revision'),('decline','-1')]:
            phases=f'OR = {{ check_variable = {{ global.cc_{s}_phase = 1 }} AND = {{ check_variable = {{ global.cc_{s}_phase = 2 }} is_in_array = {{ array = global.cc_{s}_payers value = THIS }} NOT = {{ cc_{s}_signed = yes }} }} }}' if name=='approve' else f'check_variable = {{ global.cc_{s}_phase = 1 }}'
            out.append(block(f'cc_{s}_{name}',f'if = {{ limit = {{ cc_{s}_voter = yes cc_{s}_seen_terms = yes {phases} }} set_variable = {{ cc_{s}_vote_revision = {value} }} cc_{s}_rebuild = yes }}'))
        out.append(block(f'cc_{s}_confirm_local',f'''if = {{ limit = {{ is_ai = no cc_{s}_receiving_country = yes NOT = {{ cc_{s}_voter = yes }} cc_{s}_seen_terms = yes
check_variable = {{ global.cc_{s}_phase > 0 }} check_variable = {{ global.cc_{s}_phase < 4 }} }} set_variable = {{ cc_{s}_local_revision = global.cc_{s}_revision }} cc_{s}_rebuild = yes cc_{s}_check_operating = yes }}'''))
        for name,delta in [('increase',5),('decrease',-5)]:
            out.append(block(f'cc_{s}_{name}_share',f'if = {{ limit = {{ cc_human_member = yes check_variable = {{ global.cc_{s}_phase = 0 }} check_variable = {{ cc_view_slot = {s} }} }} set_temp_variable = {{ cc_previous_share = cc_{s}_share }} add_to_variable = {{ cc_{s}_share = {delta} }} clamp_variable = {{ var = cc_{s}_share min = 0 max = 100 }} if = {{ limit = {{ NOT = {{ check_variable = {{ cc_{s}_share = cc_previous_share }} }} }} cc_{s}_revise = yes }} }}'))
        out.append(block(f'cc_{s}_fund_remainder',f'''if = {{ limit = {{ cc_human_member = yes check_variable = {{ global.cc_{s}_phase = 0 }} check_variable = {{ cc_view_slot = {s} }} }} cc_{s}_rebuild = yes
set_temp_variable = {{ cc_previous_share = cc_{s}_share }} set_variable = {{ cc_{s}_share = 100 }} subtract_from_variable = {{ cc_{s}_share = global.cc_{s}_coverage }} add_to_variable = {{ cc_{s}_share = cc_previous_share }} clamp_variable = {{ var = cc_{s}_share min = 0 max = 100 }}
if = {{ limit = {{ NOT = {{ check_variable = {{ cc_{s}_share = cc_previous_share }} }} }} cc_{s}_revise = yes }} }}'''))
        # Losing a human financier stops progress immediately. No remaining share moves to another payer.
        guard=f'''if = {{ limit = {{ check_variable = {{ global.cc_{s}_phase > 1 }} check_variable = {{ global.cc_{s}_phase < 4 }} check_variable = {{ global.cc_{s}_valid = 1 }} }}
{participants(s,f'if = {{ limit = {{ check_variable = {{ global.cc_{s}_phase = 2 }} NOT = {{ cc_human_member = yes cc_{s}_signed = yes }} }} set_variable = {{ global.cc_{s}_valid = 0 }} }}')}
{recipients(s,f'if = {{ limit = {{ NOT = {{ cc_{s}_receiver_consent = yes }} }} set_variable = {{ global.cc_{s}_valid = 0 }} }}')}
if = {{ limit = {{ check_variable = {{ global.cc_{s}_valid = 0 }} }} set_variable = {{ global.cc_{s}_operating = 0 }} {refresh(s)} cc_touch = yes }} }}'''
        out.append(block(f'cc_{s}_guard_controllers',guard))

    from elections import compile_elections
    compile_elections(out)
