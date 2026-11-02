# IMPERIA COLD WAR — COMECON annual accredited-delegation ballot
from build import *

ORDER=('BUL','HUN','DDR','CUB','MON','POL','ROM','SOV','CZE')


def compile_election_triggers():
    return '\n'.join([
        block('cc_chair_alive','NOT = { check_variable = { global.cc_chair = 0 } } var:global.cc_chair = { cc_human_member = yes }'),
        block('cc_ballot_can_vote','cc_human_member = yes check_variable = { global.cc_ballot_open = 1 } check_variable = { global.cc_ballot_days_left > 0 } is_in_array = { array = global.cc_ballot_register value = THIS } NOT = { check_variable = { cc_ballot_receipt = global.cc_ballot_round } }'),
        block('cc_ballot_target_valid','var:cc_ballot_target = { cc_human_member = yes is_in_array = { array = global.cc_ballot_candidates value = THIS } }'),
        block('cc_ballot_proposal_valid','var:cc_ballot_proposed = { cc_human_member = yes is_in_array = { array = global.cc_ballot_candidates value = THIS } }'),
        block('cc_agenda_selection_valid','NOT = { check_variable = { cc_agenda_selected = 0 } } var:cc_agenda_selected = { cc_human_member = yes check_variable = { cc_agenda_pending = 1 } check_variable = { cc_agenda_revision = PREV.cc_agenda_selected_revision } }'),
    ])


def compile_elections(out):
    order=['clear_array = global.cc_ballot_register']
    for tag in ORDER:
        order.append(f'{tag} = {{ if = {{ limit = {{ cc_human_member = yes }} add_to_array = {{ global.cc_ballot_register = THIS }} }} }}')
    order.append('for_each_scope_loop = { array = global.cc_members if = { limit = { cc_human_member = yes NOT = { is_in_array = { array = global.cc_ballot_register value = THIS } } } add_to_array = { global.cc_ballot_register = THIS } } }')
    out.append(block('cc_ballot_build_register','\n'.join(order)))
    out.append(block('cc_election_initialize','''if = { limit = { NOT = { has_global_flag = cc_elections_v1 } }
set_global_flag = cc_elections_v1 set_variable = { global.cc_ballot_year = -1 } }
if = { limit = { check_variable = { global.cc_ballot_open = 0 } NOT = { check_variable = { global.cc_ballot_year = global.year } } } cc_ballot_begin = yes }'''))
    out.append(block('cc_ballot_begin','''if = { limit = { check_variable = { global.cc_ballot_open = 0 } NOT = { check_variable = { global.cc_ballot_year = global.year } } }
cc_ballot_build_register = yes
if = { limit = { check_variable = { global.cc_ballot_register^num > 0 } }
set_variable = { global.cc_ballot_year = global.year } add_to_variable = { global.cc_ballot_round = 1 }
set_variable = { global.cc_ballot_open = 1 } set_variable = { global.cc_ballot_days_left = 15 }
set_variable = { global.cc_ballot_start_day = global.num_days } set_variable = { global.cc_ballot_outgoing = global.cc_chair }
clear_array = global.cc_ballot_candidates set_variable = { global.cc_ballot_chair_index = -1 } set_variable = { global.cc_ballot_index = 0 }
for_each_scope_loop = { array = global.cc_ballot_register if = { limit = { check_variable = { THIS.id = global.cc_ballot_outgoing } } set_variable = { global.cc_ballot_chair_index = global.cc_ballot_index } } add_to_variable = { global.cc_ballot_index = 1 } }
set_variable = { global.cc_ballot_index = 0 }
for_each_scope_loop = { array = global.cc_ballot_register if = { limit = { check_variable = { global.cc_ballot_index > global.cc_ballot_chair_index } } add_to_array = { global.cc_ballot_candidates = THIS } } add_to_variable = { global.cc_ballot_index = 1 } }
set_variable = { global.cc_ballot_index = 0 }
for_each_scope_loop = { array = global.cc_ballot_register if = { limit = { NOT = { check_variable = { global.cc_ballot_index > global.cc_ballot_chair_index } } } add_to_array = { global.cc_ballot_candidates = THIS } } add_to_variable = { global.cc_ballot_index = 1 } }
cc_ballot_count = yes cc_touch = yes } }'''))
    out.append(block('cc_ballot_count','''for_each_scope_loop = { array = global.cc_ballot_candidates set_variable = { cc_ballot_tally = 0 } }
set_variable = { global.cc_ballots_received = 0 }
for_each_scope_loop = { array = global.cc_ballot_register
if = { limit = { cc_human_member = yes check_variable = { cc_ballot_receipt = global.cc_ballot_round } cc_ballot_target_valid = yes }
var:cc_ballot_target = { add_to_variable = { cc_ballot_tally = 1 } } add_to_variable = { global.cc_ballots_received = 1 } } }'''))
    out.append(block('cc_ballot_cast','''if = { limit = { cc_ballot_can_vote = yes check_variable = { cc_ballot_view_round = global.cc_ballot_round } cc_ballot_proposal_valid = yes }
set_variable = { cc_ballot_target = cc_ballot_proposed } set_variable = { cc_ballot_receipt = global.cc_ballot_round } cc_ballot_count = yes cc_touch = yes }'''))
    out.append(block('cc_ballot_resolve','''if = { limit = { check_variable = { global.cc_ballot_open = 1 } NOT = { check_variable = { global.cc_ballot_days_left > 0 } } }
cc_ballot_count = yes set_variable = { global.cc_ballot_winner = 0 } set_variable = { global.cc_ballot_best = -1 }
for_each_scope_loop = { array = global.cc_ballot_candidates
if = { limit = { cc_human_member = yes check_variable = { cc_ballot_tally > global.cc_ballot_best } }
set_variable = { global.cc_ballot_winner = THIS.id } set_variable = { global.cc_ballot_best = cc_ballot_tally } } }
if = { limit = { NOT = { check_variable = { global.cc_ballot_winner = 0 } } } set_variable = { global.cc_chair = global.cc_ballot_winner } }
set_variable = { global.cc_ballot_open = 0 } set_variable = { global.cc_ballot_days_left = 0 }
set_variable = { global.cc_ballot_closed_round = global.cc_ballot_round } cc_update_authority = yes cc_touch = yes }'''))
    out.append(block('cc_election_tick','''cc_election_initialize = yes
if = { limit = { check_variable = { global.cc_ballot_open = 1 } }
set_variable = { global.cc_ballot_days_left = global.num_days } subtract_from_variable = { global.cc_ballot_days_left = global.cc_ballot_start_day }
multiply_variable = { global.cc_ballot_days_left = -1 } add_to_variable = { global.cc_ballot_days_left = 15 }
clamp_variable = { var = global.cc_ballot_days_left min = 0 max = 15 }
set_variable = { global.cc_ballot_roster_changed = 0 }
for_each_scope_loop = { array = global.cc_ballot_register
if = { limit = { cc_human_member = yes NOT = { check_variable = { cc_ballot_accredited = 1 } } } set_variable = { cc_ballot_accredited = 1 } set_variable = { global.cc_ballot_roster_changed = 1 } }
else_if = { limit = { NOT = { cc_human_member = yes } check_variable = { cc_ballot_accredited = 1 } } set_variable = { cc_ballot_accredited = 0 } set_variable = { global.cc_ballot_roster_changed = 1 } } }
if = { limit = { check_variable = { global.cc_ballot_roster_changed = 1 } } cc_ballot_count = yes cc_touch = yes }
cc_ballot_resolve = yes }
if = { limit = { NOT = { cc_chair_alive = yes } } cc_update_authority = yes cc_touch = yes }'''))

    valid_offer='check_variable = { cc_catalog_offer > 0 } check_variable = { cc_catalog_offer < 45 } check_variable = { cc_catalog_tier > 0 } check_variable = { cc_catalog_tier < 4 }'
    out.append(block('cc_agenda_submit','if = { limit = { cc_human_member = yes '+valid_offer+' } set_variable = { cc_agenda_offer = cc_catalog_offer } set_variable = { cc_agenda_tier = cc_catalog_tier } set_variable = { cc_agenda_pending = 1 } add_to_variable = { cc_agenda_revision = 1 } cc_touch = yes }'))
    for s in range(1,5):
        guard=f'cc_{s}_editable = yes check_variable = {{ cc_view_slot = {s} }}'
        out.append(block(f'cc_{s}_prepare_catalogue',f'''if = {{ limit = {{ {guard} check_variable = {{ cc_view_tab = 4 }} {valid_offer} }}
set_variable = {{ global.cc_{s}_offer = cc_catalog_offer }} set_variable = {{ global.cc_{s}_tier = cc_catalog_tier }}
set_variable = {{ cc_view_tab = 0 }} set_variable = {{ cc_sheet = 0 }} cc_{s}_revise = yes cc_ui_refresh = yes cc_touch = yes }}'''))
        out.append(block(f'cc_{s}_prepare_agenda',f'''if = {{ limit = {{ {guard} check_variable = {{ cc_view_tab = 3 }}
var:cc_agenda_selected = {{ cc_human_member = yes check_variable = {{ cc_agenda_pending = 1 }} check_variable = {{ cc_agenda_revision = PREV.cc_agenda_selected_revision }} check_variable = {{ cc_agenda_offer > 0 }} check_variable = {{ cc_agenda_offer < 45 }} check_variable = {{ cc_agenda_tier > 0 }} check_variable = {{ cc_agenda_tier < 4 }} }} }}
var:cc_agenda_selected = {{ set_variable = {{ PREV.cc_prepare_offer = cc_agenda_offer }} set_variable = {{ PREV.cc_prepare_tier = cc_agenda_tier }} set_variable = {{ cc_agenda_pending = 0 }} add_to_variable = {{ cc_agenda_revision = 1 }} }}
set_variable = {{ global.cc_{s}_offer = cc_prepare_offer }} set_variable = {{ global.cc_{s}_tier = cc_prepare_tier }}
set_variable = {{ cc_view_tab = 0 }} set_variable = {{ cc_sheet = 0 }} cc_{s}_revise = yes cc_ui_refresh = yes cc_touch = yes }}'''))
