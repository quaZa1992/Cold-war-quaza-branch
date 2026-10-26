# IMPERIA CW — Cold War: strategic readiness and bilateral nuclear diplomacy.
"""Author the independent readiness module; shared integrations are applied separately."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import format_code, parse, emit
from event_art import EVENT_ART, registry_source
import escalation
import command_ui

MARK = '# IMPERIA CW — Cold War: nuclear readiness and crisis diplomacy.\n'
FILES = {}
LOC = {}
MACROS = {
    'nr_order_level': ('LEVEL', {str(n):str(n) for n in range(1,6)}),
    'nr_tension': ('DELTA', {'5':'5','3':'3','1':'1','-2':'minus2','nr_relief':'relief'}),
    'nr_close_pair': ('RELIEF', {'-2':'minus2'}),
    'nr_send_offer': ('KIND', {'1':'1','2':'2'}),
    'nr_finish_offer': ('KIND', {'1':'1','2':'2'}),
    'nr_record_raid': ('LOSS', {'0.05':'tactical','0.15':'state','0.4':'strategic'}),
}

def expand(body):
    """Expand authoring parameters to fixed native scripted effects."""
    def substitute(rows, key, value):
        return [(k.replace('$'+key+'$',value),op,
                 substitute(v,key,value) if isinstance(v,list) else v.replace('$'+key+'$',value)) for k,op,v in rows]
    def visit(rows):
        output=[]
        for k,op,v in rows:
            if k in ['set_country_flag','set_global_flag'] and isinstance(v,list) and any(name=='days' for name,_,_ in v) and not any(name=='value' for name,_,_ in v):
                v=v+[('value','=','1')]
            if k in MACROS:
                param,choices=MACROS[k]
                if isinstance(v,list) and any('$'+param+'$' in str(x) for x in v):
                    for value,suffix in choices.items():
                        output.append((k+'_'+suffix,op,visit(substitute(v,param,value))))
                    continue
                if isinstance(v,list):
                    value=next((x for name,_,x in v if name==param),None)
                    if value is not None:
                        output.append((k+'_'+choices[value],op,'yes'))
                        continue
            output.append((k,op,visit(v) if isinstance(v,list) else v))
        return output
    return emit(visit(parse(body)))+'\n'

def source(path, body, formatted=True):
    if formatted:body = expand(body)
    body = body.replace('nr_', 'COLDWAR_nr_')
    FILES[path] = MARK + body

def loc(key, value):
    value = value.replace('•', '|').replace('−', '-').replace('’', "'")
    LOC[key.replace('nr_', 'COLDWAR_nr_')] = value.replace('nr_', 'COLDWAR_nr_')

LEVELS = {
    5: ('Routine Deterrence', .15, .10, 1.0),
    4: ('Increased Vigilance', .30, .15, 1.15),
    3: ('Reinforced Readiness', .50, .25, 1.4),
    2: ('Strategic Alert', .75, .40, 1.8),
    1: ('Maximum Readiness', 1.0, .50, 2.5),
}

source('common/scripted_triggers/COLDWAR_nuclear_readiness.txt', '''
nr_enabled = { IMP_is_1970_scenario = yes has_dlc = "Gotterdammerung" }
nr_nuclear_power = {
    nr_enabled = yes has_capitulated = no
    OR = {
        has_equipment = { nuclear_missile_equipment > 0 }
        has_equipment = { nuclear_ballistic_missile_equipment > 0 }
    }
}
nr_can_change = {
    custom_trigger_tooltip = { tooltip = nr_tt_arsenal nr_nuclear_power = yes }
    custom_trigger_tooltip = { tooltip = nr_tt_transition check_variable = { nr_build_days = 0 } }
    custom_trigger_tooltip = { tooltip = nr_tt_standdown NOT = { has_country_flag = nr_standdown } }
    has_political_power > 24
}
nr_pair_valid = {
    if = { limit = { has_variable = nr_opponent has_capitulated = no }
        var:nr_opponent = {
            exists = yes has_capitulated = no
            check_variable = { nr_opponent = PREV.id }
            check_variable = { nr_serial = PREV.nr_serial }
        }
    }
    else = { always = no }
}
nr_can_warn_prev = {
    is_ai = no nr_nuclear_power = yes
    check_variable = { nr_level < 4 }
    check_variable = { nr_build_days = 0 }
    NOT = { has_variable = nr_opponent }
    NOT = { has_country_flag = nr_standdown }
    NOT = { check_variable = { nr_cooldown@PREV > global.num_days } }
    PREV = {
        exists = yes has_capitulated = no is_subject = no
        NOT = { tag = ROOT }
        NOT = { is_in_faction_with = ROOT }
        NOT = { has_variable = nr_opponent }
        NOT = { check_variable = { nr_cooldown@ROOT > global.num_days } }
    }
}
nr_is_opponent_prev = {
    nr_pair_valid = yes
    check_variable = { nr_opponent = PREV.id }
}
nr_can_withdraw_prev = {
    nr_is_opponent_prev = yes
    check_variable = { nr_initiator = THIS.id }
}
nr_pending_prev = {
    nr_is_opponent_prev = yes
    check_variable = { nr_offer_serial@PREV = nr_serial }
    check_variable = { nr_offer_until@PREV > global.num_days }
}
nr_offer_intact_prev = {
    check_variable = { nr_offer_own_use@PREV = nr_strike_revision }
    check_variable = { nr_offer_peer_use@PREV = PREV.nr_strike_revision }
}
nr_can_offer_prev = {
    nr_is_opponent_prev = yes
    NOT = { check_variable = { nr_offer_until@PREV > global.num_days } }
    NOT = { check_variable = { PREV.nr_offer_until@THIS > global.num_days } }
    NOT = { check_variable = { nr_offer_cd@PREV > global.num_days } }
}
nr_retaliation_allowed = {
    if = { limit = { nr_enabled = yes }
        is_in_array = { array = nr_aggressors value = FROM.id }
    }
    else = { has_country_flag = has_been_nuked }
}
nr_tactical_ready = {
  custom_override_tooltip = { tooltip = nr_tt_tactical_ready
    if = { limit = { nr_enabled = yes }
        set_temp_variable = { nr_launch_allocation = { value = num_equipment@nuclear_missile_equipment add = num_equipment@nuclear_ballistic_missile_equipment multiply = nr_ready_share round = yes } }
        custom_trigger_tooltip = { tooltip = nr_tt_tactical_ready
            nr_nuclear_power = yes has_country_flag = nr_initialized
            check_variable = { nr_level < 4 }
            check_variable = { nr_launch_allocation > 0 }
        }
        custom_trigger_tooltip = { tooltip = nr_tt_standdown NOT = { has_country_flag = nr_standdown } }
    }
  }
}
nr_state_ready = {
  custom_override_tooltip = { tooltip = nr_tt_state_ready
    if = { limit = { nr_enabled = yes }
        set_temp_variable = { nr_launch_allocation = { value = num_equipment@nuclear_missile_equipment add = num_equipment@nuclear_ballistic_missile_equipment multiply = nr_ready_share round = yes } }
        custom_trigger_tooltip = { tooltip = nr_tt_state_ready
            nr_nuclear_power = yes has_country_flag = nr_initialized
            check_variable = { nr_level < 3 }
            check_variable = { nr_launch_allocation > 19 }
        }
        custom_trigger_tooltip = { tooltip = nr_tt_standdown NOT = { has_country_flag = nr_standdown } }
    }
  }
}
nr_strategic_ready = {
  custom_override_tooltip = { tooltip = nr_tt_strategic_ready
    if = { limit = { nr_enabled = yes }
        set_temp_variable = { nr_launch_allocation = { value = num_equipment@nuclear_missile_equipment add = num_equipment@nuclear_ballistic_missile_equipment multiply = nr_ready_share round = yes } }
        custom_trigger_tooltip = { tooltip = nr_tt_strategic_ready
            nr_nuclear_power = yes has_country_flag = nr_initialized
            check_variable = { nr_level = 1 }
            check_variable = { nr_launch_allocation > 199 }
        }
        custom_trigger_tooltip = { tooltip = nr_tt_standdown NOT = { has_country_flag = nr_standdown } }
    }
  }
}
''')

# IMPERIA CW — Cold War: peacetime nuclear release is a separate, target-bound procedure.
source('common/scripted_triggers/COLDWAR_nuclear_escalation.txt', escalation.TRIGGERS)
source('common/scripted_effects/COLDWAR_nuclear_escalation.txt', escalation.EFFECTS)
source('common/opinion_modifiers/COLDWAR_nuclear_escalation.txt', '''
opinion_modifiers = {
    nr_first_use_condemnation = { value = -100 days = 365 }
}
''')

effects = '''
nr_touch = { add_to_variable = { nr_dirty = 1 } }
nr_init = {
    if = { limit = { NOT = { has_country_flag = nr_initialized } }
        set_country_flag = nr_initialized
        set_variable = { nr_level = 5 }
        set_variable = { nr_order = 5 }
        set_variable = { nr_build_days = 0 }
        set_variable = { nr_fatigue = 0 }
        set_variable = { nr_civil_days = 0 }
    }
    nr_refresh = yes
}
nr_refresh = {
    set_variable = { nr_arsenal = { value = num_equipment@nuclear_missile_equipment add = num_equipment@nuclear_ballistic_missile_equipment clamp = { min = 0 max = 1000000 } } }
    set_variable = { nr_ready_share = 0 }
    set_variable = { nr_reserve_share = 0 }
    set_variable = { nr_cost_factor = 0 }
'''
for level, (_, ready, reserve, factor) in LEVELS.items():
    effects += f'''if = {{ limit = {{ check_variable = {{ nr_level = {level} }} }}
        set_variable = {{ nr_ready_share = {ready} }}
        set_variable = {{ nr_reserve_share = {reserve} }}
        set_variable = {{ nr_cost_factor = {factor} }}
    }}\n'''
effects += '''
    set_variable = { nr_ready_count = { value = nr_arsenal multiply = nr_ready_share round = yes } }
    set_variable = { nr_protected_count = { value = nr_arsenal multiply = nr_reserve_share round = yes } }
    set_variable = { nr_fatigue_stability = { value = nr_fatigue multiply = -0.0005 } }
    if = { limit = { nr_nuclear_power = yes }
        if = { limit = { NOT = { has_dynamic_modifier = { modifier = nr_strategic_forces } } }
            add_dynamic_modifier = { modifier = nr_strategic_forces }
        }
    }
    else = {
        set_variable = { nr_level = 5 }
        set_variable = { nr_order = 5 }
        set_variable = { nr_build_days = 0 }
        set_variable = { nr_ready_count = 0 }
        set_variable = { nr_protected_count = 0 }
        set_variable = { nr_ready_share = 0 }
        set_variable = { nr_reserve_share = 0 }
        if = { limit = { has_dynamic_modifier = { modifier = nr_strategic_forces } }
            remove_dynamic_modifier = { modifier = nr_strategic_forces }
        }
    }
    nr_calculate_budget = yes
    nr_validate_first_use = yes
    force_update_dynamic_modifier = yes
    nr_touch = yes
}
nr_calculate_budget = {
    set_variable = { nr_forces_weekly = 0 }
    set_variable = { nr_civil_weekly = 0 }
    set_variable = { nr_weekly_cost = 0 }
    if = { limit = { nr_nuclear_power = yes has_country_flag = nr_initialized }
        set_variable = { nr_forces_weekly = {
            value = num_equipment@nuclear_missile_equipment
            add = num_equipment@nuclear_ballistic_missile_equipment
            multiply = 0.00001 add = 0.002
            multiply = nr_cost_factor
            multiply = { value = 1 add = { value = nr_fatigue multiply = 0.005 } }
            multiply = { value = gdp_per_capita divide = 36 clamp = { min = 0.4 max = 1.2 } }
            multiply = { value = inflation_multiplier clamp = { min = 0.01 max = 100 } }
        } }
    }
    if = { limit = { OR = { has_country_flag = nr_civil_active check_variable = { nr_civil_days > 0 } } }
        set_variable = { nr_civil_weekly = {
            value = gdp_total multiply = 0.00002 add = 0.002
            multiply = { value = inflation_multiplier clamp = { min = 0.01 max = 100 } }
        } }
    }
    set_variable = { nr_weekly_cost = { value = nr_forces_weekly add = nr_civil_weekly } }
}
nr_order_level = {
    if = { limit = { nr_can_change = yes NOT = { check_variable = { nr_level = $LEVEL$ } } }
        add_political_power = -25
        set_variable = { nr_order = $LEVEL$ }
        if = { limit = { check_variable = { nr_level > $LEVEL$ } }
            set_variable = { nr_build_days = nr_level }
            subtract_from_variable = { nr_build_days = $LEVEL$ }
            multiply_variable = { nr_build_days = 2 }
        }
        else = {
            set_variable = { nr_level = $LEVEL$ }
            set_variable = { nr_build_days = 0 }
        }
        nr_refresh = yes
    }
}
nr_stand_down = {
    set_variable = { nr_level = 5 }
    set_variable = { nr_order = 5 }
    set_variable = { nr_build_days = 0 }
    nr_refresh = yes
}
nr_start_civil = {
    if = { limit = { nr_enabled = yes is_ai = no has_capitulated = no
        has_political_power > 24 NOT = { has_country_flag = nr_civil_active }
        check_variable = { nr_civil_days = 0 }
    }
        nr_init = yes
        add_political_power = -25
        set_variable = { nr_civil_days = 3 }
        add_dynamic_modifier = { modifier = nr_civil_defence }
        nr_refresh = yes
    }
}
nr_end_civil = {
    clr_country_flag = nr_civil_active
    set_variable = { nr_civil_days = 0 }
    remove_dynamic_modifier = { modifier = nr_civil_defence }
    nr_refresh = yes
}
nr_daily = {
    if = { limit = { NOT = { has_country_flag = nr_initialized } } nr_init = yes }
    if = { limit = { check_variable = { nr_build_days > 0 } }
        if = { limit = { nr_nuclear_power = yes NOT = { has_country_flag = nr_standdown } }
            subtract_from_variable = { nr_build_days = 1 }
            if = { limit = { check_variable = { nr_build_days = 0 } }
                set_variable = { nr_level = nr_order }
                if = { limit = { is_ai = no } country_event = { id = cw_nuclear.1 } }
            }
        }
        else = { set_variable = { nr_build_days = 0 } set_variable = { nr_order = nr_level } }
    }
    if = { limit = { check_variable = { nr_civil_days > 0 } }
        subtract_from_variable = { nr_civil_days = 1 }
        if = { limit = { check_variable = { nr_civil_days = 0 } }
            set_country_flag = nr_civil_active
            if = { limit = { is_ai = no } country_event = { id = cw_nuclear.2 } }
        }
    }
    if = { limit = { nr_nuclear_power = yes check_variable = { nr_level = 1 } }
        add_to_variable = { nr_fatigue = 2 }
    }
    else_if = { limit = { nr_nuclear_power = yes check_variable = { nr_level = 2 } }
        add_to_variable = { nr_fatigue = 1 }
    }
    else_if = { limit = { nr_nuclear_power = yes check_variable = { nr_level = 3 } }
        add_to_variable = { nr_fatigue = 0.25 }
    }
    else = { subtract_from_variable = { nr_fatigue = 2 } }
    clamp_variable = { var = nr_fatigue min = 0 max = 100 }
    if = { limit = { has_capitulated = yes }
        nr_stand_down = yes
        nr_end_civil = yes
    }
    if = { limit = { has_variable = nr_opponent }
        if = { limit = { NOT = { nr_pair_valid = yes } }
            nr_clear_local_crisis = yes
        }
        else_if = { limit = { check_variable = { nr_until < global.num_days } }
            save_event_target_as = nr_sender
            var:nr_opponent = { save_event_target_as = nr_recipient }
            nr_close_pair = { RELIEF = -2 }
            if = { limit = { is_ai = no } country_event = { id = cw_nuclear.9 } }
            event_target:nr_recipient = { if = { limit = { is_ai = no } country_event = { id = cw_nuclear.9 } } }
        }
    }
    nr_refresh = yes
}
nr_tension = {
    set_temp_variable = { nr_tension_applied = 0 }
    if = { limit = { has_global_flag = mdcw_cw_initialized }
        set_temp_variable = { nr_tension_before = global.mdcw_cw_tension }
        set_temp_variable = { mdcw_cw_tension_delta = $DELTA$ }
        mdcw_cw_add_tension = yes
        set_temp_variable = { nr_tension_applied = { value = global.mdcw_cw_tension subtract = nr_tension_before } }
    }
}
nr_begin_crisis = {
    if = { limit = { nr_can_warn_prev = yes }
        save_event_target_as = nr_sender
        PREV = { save_event_target_as = nr_recipient }
        nr_tension = { DELTA = 5 }
        add_to_variable = { global.nr_serial = 1 }
        set_variable = { nr_serial = global.nr_serial }
        set_variable = { nr_opponent = event_target:nr_recipient.id }
        set_variable = { nr_initiator = THIS.id }
        set_variable = { nr_until = { value = global.num_days add = 90 } }
        set_variable = { nr_pressure = nr_tension_applied }
        set_country_flag = { flag = nr_public days = 90 }
        clr_country_flag = nr_countered
        clr_country_flag = nr_hotline
        event_target:nr_recipient = {
            nr_init = yes
            set_variable = { nr_opponent = event_target:nr_sender.id }
            set_variable = { nr_initiator = event_target:nr_sender.id }
            set_variable = { nr_serial = global.nr_serial }
            set_variable = { nr_until = { value = global.num_days add = 90 } }
            set_variable = { nr_pressure = event_target:nr_sender.nr_pressure }
            clr_country_flag = nr_countered
            clr_country_flag = nr_hotline
            nr_refresh = yes
            country_event = { id = cw_nuclear.3 }
        }
        add_named_threat = { threat = 2 name = nr_warning_threat }
        every_country = {
            limit = { is_ai = no NOT = { tag = event_target:nr_sender } NOT = { tag = event_target:nr_recipient } }
            country_event = { id = cw_nuclear.10 }
        }
        nr_refresh = yes
    }
}
nr_counter_signal = {
    if = { limit = { nr_is_opponent_prev = yes nr_nuclear_power = yes
        check_variable = { nr_level < 4 } NOT = { has_country_flag = nr_countered }
        NOT = { check_variable = { nr_initiator = THIS.id } }
    }
        set_country_flag = nr_countered
        set_country_flag = { flag = nr_public days = 90 }
        nr_tension = { DELTA = 3 }
        set_variable = { nr_pressure_delta = nr_tension_applied }
        add_to_variable = { nr_pressure = nr_pressure_delta }
        var:nr_opponent = { add_to_variable = { nr_pressure = PREV.nr_pressure_delta } }
        add_named_threat = { threat = 1 name = nr_counter_threat }
        save_event_target_as = nr_sender
        var:nr_opponent = { save_event_target_as = nr_recipient country_event = { id = cw_nuclear.4 } }
        nr_touch = yes
    }
}
nr_send_offer = {
    if = { limit = { nr_can_offer_prev = yes }
        set_variable = { nr_offer_kind@PREV = $KIND$ }
        set_variable = { nr_offer_serial@PREV = nr_serial }
        set_variable = { nr_offer_until@PREV = { value = global.num_days add = 14 } }
        set_variable = { nr_offer_cd@PREV = { value = global.num_days add = 21 } }
        set_variable = { nr_offer_own_use@PREV = nr_strike_revision }
        set_variable = { nr_offer_peer_use@PREV = PREV.nr_strike_revision }
        nr_touch = yes
    }
}
nr_finish_offer = {
    if = { limit = { nr_pending_prev = yes check_variable = { nr_offer_kind@PREV = $KIND$ } }
        save_event_target_as = nr_sender
        PREV = { save_event_target_as = nr_recipient }
        clear_variable = nr_offer_until@PREV
        clear_variable = nr_offer_kind@PREV
        clear_variable = nr_offer_serial@PREV
        if = { limit = { nr_offer_intact_prev = yes }
            if = { limit = { check_variable = { nr_accept_kind = 1 } } nr_accept_offer_1 = yes }
            else = { nr_accept_offer_2 = yes }
        }
        else = { country_event = { id = cw_nuclear.13 } }
    }
}
nr_accept_offer_1 = {
    clear_variable = nr_offer_cd@event_target:nr_recipient
    set_country_flag = nr_hotline
    var:nr_opponent = { clear_variable = nr_offer_cd@PREV set_country_flag = nr_hotline nr_touch = yes }
    country_event = { id = cw_nuclear.5 }
    var:nr_opponent = { country_event = { id = cw_nuclear.5 } }
    nr_touch = yes
}
nr_accept_offer_2 = {
    nr_clear_first_use = yes
    var:nr_opponent = { nr_clear_first_use = yes }
    set_temp_variable = { nr_relief = nr_pressure }
    multiply_temp_variable = { nr_relief = -1 }
    nr_tension = { DELTA = nr_relief }
    var:nr_opponent = {
        nr_stand_down = yes
        set_country_flag = { flag = nr_standdown days = 30 }
        nr_clear_local_crisis = yes
    }
    nr_stand_down = yes
    set_country_flag = { flag = nr_standdown days = 30 }
    nr_clear_local_crisis = yes
    country_event = { id = cw_nuclear.6 }
    event_target:nr_recipient = { country_event = { id = cw_nuclear.6 } }
}
nr_reject_offer = {
    if = { limit = { nr_pending_prev = yes }
        save_event_target_as = nr_sender
        PREV = { save_event_target_as = nr_recipient }
        clear_variable = nr_offer_until@PREV
        clear_variable = nr_offer_kind@PREV
        clear_variable = nr_offer_serial@PREV
        country_event = { id = cw_nuclear.7 }
        nr_touch = yes
    }
}
nr_clear_local_crisis = {
    nr_clear_first_use = yes
    if = { limit = { has_variable = nr_opponent }
        var:nr_opponent = { save_event_target_as = nr_cleanup_partner }
        set_variable = { nr_cooldown@event_target:nr_cleanup_partner = { value = global.num_days add = 90 } }
        clear_variable = nr_offer_until@event_target:nr_cleanup_partner
        clear_variable = nr_offer_kind@event_target:nr_cleanup_partner
        clear_variable = nr_offer_serial@event_target:nr_cleanup_partner
    }
    clear_variable = nr_opponent
    clear_variable = nr_initiator
    clear_variable = nr_until
    clear_variable = nr_pressure
    clr_country_flag = nr_hotline
    clr_country_flag = nr_countered
    nr_touch = yes
}
nr_close_pair = {
    set_temp_variable = { nr_relief = { value = $RELIEF$ multiply = -1 clamp = { min = 0 max = nr_pressure } multiply = -1 } }
    if = { limit = { nr_pair_valid = yes }
        var:nr_opponent = { nr_clear_local_crisis = yes }
    }
    nr_clear_local_crisis = yes
    nr_tension = { DELTA = nr_relief }
}
nr_withdraw = {
    if = { limit = { nr_can_withdraw_prev = yes }
        nr_clear_first_use = yes
        var:nr_opponent = { nr_clear_first_use = yes }
        save_event_target_as = nr_sender
        PREV = { save_event_target_as = nr_recipient }
        nr_stand_down = yes
        set_country_flag = { flag = nr_standdown days = 14 }
        nr_close_pair = { RELIEF = -2 }
        event_target:nr_recipient = { country_event = { id = cw_nuclear.8 } }
    }
}
nr_consult_allies = {
    if = { limit = { nr_pair_valid = yes NOT = { has_country_flag = nr_consulted } }
        save_event_target_as = nr_sender
        var:nr_opponent = { save_event_target_as = nr_recipient }
        set_country_flag = { flag = nr_consulted days = 30 }
        every_allied_country = {
            limit = { is_ai = no NOT = { tag = event_target:nr_recipient } }
            country_event = { id = cw_nuclear.11 }
        }
    }
}
nr_assess_prev = {
    PREV = { save_event_target_as = nr_subject }
    set_variable = { nr_assessment = 0 }
    set_variable = { nr_assessed_level = 0 }
    if = { limit = { intel_level_over = { target = PREV airforce_intel > 0.65 } }
        set_variable = { nr_assessment = 2 }
        set_variable = { nr_assessed_level = PREV.nr_level }
        if = { limit = { check_variable = { nr_assessed_level = 0 } } set_variable = { nr_assessed_level = 5 } }
        if = { limit = { PREV = { check_variable = { nr_level < 3 } NOT = { has_country_flag = nr_public } NOT = { has_country_flag = nr_exposed_cd } } }
            nr_tension = { DELTA = 1 }
            PREV = { set_country_flag = { flag = nr_exposed_cd days = 30 } }
        }
    }
    else_if = { limit = {
        OR = { is_in_faction_with = PREV nr_is_opponent_prev = yes
            PREV = { has_country_flag = nr_public }
            intel_level_over = { target = PREV airforce_intel > 0.35 }
        }
    }
        set_variable = { nr_assessment = 1 }
        if = { limit = { PREV = { check_variable = { nr_level > 3 } } } set_variable = { nr_assessed_level = 5 } }
        else_if = { limit = { PREV = { check_variable = { nr_level > 1 } } } set_variable = { nr_assessed_level = 3 } }
        else_if = { limit = { PREV = { check_variable = { nr_level = 1 } } } set_variable = { nr_assessed_level = 1 } }
    }
    country_event = { id = cw_nuclear.14 }
}
nr_record_raid = {
    nr_resolve_peacetime_operation = yes
    var:actor_country = {
        save_event_target_as = nr_attacker
        if = { limit = { nr_enabled = yes }
            set_variable = { nr_last_use_serial = nr_serial }
            add_to_variable = { nr_strike_revision = 1 }
            set_country_flag = { flag = nr_public days = 90 }
        }
    }
    var:victim_country = {
        if = { limit = { nr_enabled = yes }
            nr_init = yes
            add_to_variable = { nr_strike_revision = 1 }
            if = { limit = { NOT = { is_in_array = { array = nr_aggressors value = event_target:nr_attacker.id } } }
                add_to_array = { array = nr_aggressors value = event_target:nr_attacker.id }
            }
            set_variable = { nr_last_aggressor = event_target:nr_attacker.id }
            clr_country_flag = nr_standdown
            set_temp_variable = { nr_counterforce_fraction = $LOSS$ }
            nr_counterforce_loss = yes
            if = { limit = { nr_nuclear_power = yes NOT = { check_variable = { nr_level = 1 } } }
                set_variable = { nr_order = 1 }
                set_variable = { nr_build_days = 1 }
                nr_touch = yes
            }
            if = { limit = { is_ai = no } country_event = { id = cw_nuclear.12 } }
        }
    }
}
nr_counterforce_loss = {
    set_temp_variable = { nr_exposed_fraction = { value = 1 subtract = nr_reserve_share multiply = nr_counterforce_fraction } }
    set_temp_variable = { nr_icbm_loss = { value = num_equipment@nuclear_missile_equipment multiply = nr_exposed_fraction round = yes multiply = -1 } }
    set_temp_variable = { nr_irbm_loss = { value = num_equipment@nuclear_ballistic_missile_equipment multiply = nr_exposed_fraction round = yes multiply = -1 } }
    if = { limit = { check_variable = { nr_icbm_loss < 0 } }
        add_equipment_to_stockpile = { type = nuclear_missile_equipment amount = nr_icbm_loss }
    }
    if = { limit = { check_variable = { nr_irbm_loss < 0 } }
        add_equipment_to_stockpile = { type = nuclear_ballistic_missile_equipment amount = nr_irbm_loss }
    }
    nr_refresh = yes
}
nr_civilian_protection = {
    if = { limit = { CONTROLLER = { has_country_flag = nr_civil_active } }
        multiply_temp_variable = { casualty_rate = 0.8 }
    }
}
'''
source('common/scripted_effects/COLDWAR_nuclear_readiness.txt', effects)

source('common/dynamic_modifiers/COLDWAR_nuclear_readiness.txt', '''
nr_strategic_forces = {
    enable = { nr_nuclear_power = yes }
    icon = GFX_idea_nuclear_power_def
    stability_factor = nr_fatigue_stability
}
nr_civil_defence = {
    enable = { always = yes }
    icon = GFX_idea_nuclear_power_def
    production_speed_buildings_factor = -0.03
    industrial_capacity_factory = -0.03
}
''')
source('common/on_actions/COLDWAR_nuclear_readiness.txt', '''
on_actions = {
    on_daily = { effect = {
        if = { limit = { nr_enabled = yes
            OR = { has_country_flag = nr_initialized nr_nuclear_power = yes }
        } nr_daily = yes }
    } }
}
''')

def write_all():
    for rel, content in FILES.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8', newline='\n')
    write_localisation()
    print(f'Wrote {len(FILES)} scripts and {len(LOC)} English strings.')

# IMPERIA CW — Cold War: allow localisation repairs without rewriting gameplay scripts.
def write_localisation():
    path = ROOT / 'localisation/english/COLDWAR_nuclear_readiness_l_english.yml'
    lines = ['l_english:', MARK.rstrip()]
    for key, value in LOC.items():
        lines.append(' ' + key + ':0 ' + json.dumps(value.replace('\\n', '\n'), ensure_ascii=False))
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8-sig', newline='\n')

def action(name, condition, effect, cost=0, acceptance=False, kind=None):
    visibility = {
        'warning': 'ROOT = { nr_nuclear_power = yes }',
        'counter': 'ROOT = { nr_pair_valid = yes check_variable = { nr_opponent = PREV.id } NOT = { check_variable = { nr_initiator = THIS.id } } }',
        'hotline': 'ROOT = { nr_is_opponent_prev = yes NOT = { has_country_flag = nr_hotline } }',
        'standdown': 'ROOT = { nr_is_opponent_prev = yes has_country_flag = nr_hotline }',
        'withdraw': 'ROOT = { nr_can_withdraw_prev = yes }',
        'assess': '',
        'ultimatum': 'ROOT = { nr_is_opponent_prev = yes NOT = { has_war_with = PREV } }',
        'revoke': 'ROOT = { nr_can_revoke_prev = yes }',
    }[name]
    pending = ''
    if acceptance:
        pending = f'''
        on_sent_effect = {{ ROOT = {{ nr_send_offer = {{ KIND = {kind} }} }} }}
        can_be_accepted = {{ ROOT = {{ nr_pending_prev = yes nr_offer_intact_prev = yes check_variable = {{ nr_offer_kind@PREV = {kind} }} }} }}
        reject_effect = {{ ROOT = {{ nr_reject_offer = yes }} }}
        ai_acceptance = {{ nr_ai_reason = {{ base = 50 modifier = {{ add = -100 ROOT = {{ has_war_with = PREV }} }} }} }}
        '''
    return f'''
    nr_{name} = {{
        allowed = {{ always = yes }}
        visible = {{ NOT = {{ tag = ROOT }} ROOT = {{ is_ai = no nr_enabled = yes }} {visibility} }}
        selectable = {{ ROOT = {{ {condition} }} }}
        can_be_sent = {{ ROOT = {{ {condition} }} }}
        cost = {cost}
        requires_acceptance = {'yes' if acceptance else 'no'}
        show_acceptance_on_action_button = {'yes' if acceptance else 'no'}
        icon = 22
        send_description = nr_{name}_send
        receive_description = nr_{name}_receive
        accept_title = nr_{name}_accept_title
        accept_description = nr_{name}_accept
        reject_title = nr_offer_reject_title
        reject_description = nr_offer_reject
        {pending}
        complete_effect = {{ ROOT = {{ {effect} }} }}
        ai_desire = {{ base = -1000 }}
    }}
    '''

actions = action('warning', '''
    custom_trigger_tooltip = { tooltip = nr_tt_warning nr_can_warn_prev = yes }
''', 'nr_begin_crisis = yes', 50)
actions += action('counter', '''
    custom_trigger_tooltip = { tooltip = nr_tt_counter
        nr_is_opponent_prev = yes nr_nuclear_power = yes
        check_variable = { nr_level < 4 }
        NOT = { check_variable = { nr_initiator = THIS.id } }
        NOT = { has_country_flag = nr_countered }
    }
''', 'nr_counter_signal = yes', 25)
for name, kind in [('hotline', 1), ('standdown', 2)]:
    extra = ('NOT = { has_country_flag = nr_hotline }' if kind == 1 else 'has_country_flag = nr_hotline')
    actions += action(name, f'''
        custom_trigger_tooltip = {{ tooltip = nr_tt_{'standdown_offer' if kind == 2 else name} nr_can_offer_prev = yes {extra} }}
    ''', f'set_variable = {{ nr_accept_kind = {kind} }} nr_finish_offer = {{ KIND = {kind} }}', 15, True, kind)
actions += action('withdraw', '''
    custom_trigger_tooltip = { tooltip = nr_tt_withdraw nr_can_withdraw_prev = yes }
''', 'nr_withdraw = yes')
actions += action('assess', '''
    custom_trigger_tooltip = { tooltip = nr_tt_assess
        PREV = { exists = yes }
        NOT = { check_variable = { nr_assess_cd@PREV > global.num_days } }
    }
''', '''
    set_variable = { nr_assess_cd@PREV = { value = global.num_days add = 14 } }
    nr_assess_prev = yes
''', 10)
# IMPERIA CW — Cold War: public final ultimatums and unilateral revocation.
actions += action('ultimatum', '''
    custom_trigger_tooltip = { tooltip = nr_tt_ultimatum nr_can_ultimatum_prev = yes }
''', 'nr_issue_ultimatum = yes', 100)
actions += action('revoke', '''
    custom_trigger_tooltip = { tooltip = nr_tt_revoke nr_can_revoke_prev = yes }
''', 'nr_revoke_first_use = yes')
source('common/scripted_diplomatic_actions/COLDWAR_nuclear_readiness.txt', 'scripted_diplomatic_actions = {\n' + actions + '\n}')

source('common/decisions/categories/COLDWAR_nuclear_readiness.txt', '''
nr_category = {
    icon = GFX_decision_missile_nuclear_button
    priority = 1350 visible_when_empty = yes
    visible = { is_ai = no nr_enabled = yes }
}
''')
source('common/decisions/COLDWAR_nuclear_readiness.txt', '''
nr_category = {
    nr_open_command = {
        icon = GFX_decision_generic_nuclear cost = 0
        complete_effect = { nr_init = yes set_country_flag = nr_open nr_touch = yes }
        ai_will_do = { factor = 0 }
    }
}
''')

events = 'add_namespace = cw_nuclear\n'
EVENT_COPY = {
    1: ('Readiness Orders Completed', 'The strategic forces have completed their preparations. The current posture is now [nr_level_L].'),
    2: ('Civil Defence Stations Ready', 'Emergency services and shelter authorities have completed their preparations. Civil defence arrangements are now in force.'),
    3: ('A Nuclear Warning', '[nr_sender.GetNameDefCap] has issued a formal nuclear warning to our government. Its strategic forces are at heightened readiness. The cabinet must decide how to respond.'),
    4: ('A Counter-Alert', '[nr_sender.GetNameDefCap] has announced a nuclear counter-alert. Both governments now face a confrontation in which each military move carries political consequences.'),
    5: ('Direct Communications Established', 'Our governments have agreed to keep a direct channel open throughout the confrontation. A mutual reduction of nuclear readiness can now be negotiated.'),
    6: ('Mutual Stand-Down Agreed', 'Both governments have accepted a coordinated return to routine nuclear readiness. The direct confrontation has ended.'),
    7: ('Proposal Declined', '[nr_recipient.GetNameDefCap] has declined our proposal. The existing military postures remain in place.'),
    8: ('Nuclear Warning Withdrawn', '[nr_sender.GetNameDefCap] has withdrawn its nuclear warning and returned its strategic forces to routine readiness. Our government retains control of its own posture.'),
    9: ('Confrontation Lapses', 'The period of formal nuclear confrontation has expired. Each government retains responsibility for its military posture and any further diplomatic action.'),
    10: ('A Nuclear Confrontation', '[nr_sender.GetNameDefCap] has issued a formal nuclear warning to [nr_recipient.GetNameDef]. Diplomatic missions are seeking clarification as governments assess the risk of escalation.'),
    11: ('An Ally Requests Consultation', '[nr_sender.GetNameDefCap] requests urgent consultations concerning its nuclear confrontation with [nr_recipient.GetNameDef]. Allied governments must coordinate their diplomatic and civil defence responses.'),
    12: ('Nuclear Attack Confirmed', '[nr_attacker.GetNameDefCap] has used nuclear weapons against us. Emergency services are assessing the consequences as the cabinet reviews its response.'),
    13: ('Negotiations Overtaken by Events', 'Nuclear weapons have been used during this confrontation. The proposed agreement can no longer be concluded on its previous terms.'),
    14: ('Strategic Intelligence Assessment', 'Our assessment of [nr_subject.GetNameDef]:\\n\\n[nr_assessment_L]'),
}
EVENT_COPY.update(escalation.EVENT_COPY)
for ident, (title, desc) in EVENT_COPY.items():
    # IMPERIA CW — Cold War: event localisation promotes saved targets by name.
    loc(f'cw_nuclear.{ident}.t', title)
    loc(f'cw_nuclear.{ident}.d', desc)
    events += f'''
    country_event = {{
        id = cw_nuclear.{ident} title = cw_nuclear.{ident}.t desc = cw_nuclear.{ident}.d
        picture = GFX_COLDWAR_nuclear_readiness_{EVENT_ART[ident]}
        is_triggered_only = yes
        option = {{ name = nr_review_command
            trigger = {{ is_ai = no nr_enabled = yes }}
            hidden_effect = {{ nr_init = yes set_country_flag = nr_open nr_touch = yes }}
        }}
        option = {{ name = nr_acknowledge ai_chance = {{ base = 100 }} }}
    }}
    '''
# IMPERIA CW — Cold War: one country-scoped hourly callback while a release procedure is active.
events += '''country_event = {
    id = cw_nuclear.90 hidden = yes is_triggered_only = yes
    immediate = { nr_first_use_tick = yes }
}\n'''
source('events/COLDWAR_nuclear_readiness.txt', events)
source('interface/COLDWAR_nuclear_readiness_eventpictures.gfx', registry_source())

loc('nr_category', 'Strategic Readiness')
loc('nr_category_desc', 'The government directs nuclear readiness, civil defence and crisis communications. Formal warnings and proposals are delivered through diplomatic channels.')
loc('nr_open_command', 'Convene the National Security Council')
loc('nr_open_command_desc', 'Review the posture of the strategic forces, the readiness of civil defence authorities and the state of any nuclear confrontation.')
loc('nr_title', 'STRATEGIC COMMAND')
loc('nr_subtitle', 'NATIONAL SECURITY COUNCIL  |  STRATEGIC FORCES DIRECTORATE')
loc('nr_review_command', 'Convene the National Security Council.')
loc('nr_acknowledge', 'Acknowledged.')
# IMPERIA CW — Cold War: readable label for the native event debug overlay.
loc('debug_event_scopes', 'Event context')
loc('nr_strategic_forces', 'Strategic Forces')
loc('nr_strategic_forces_desc', 'Maintaining nuclear forces at elevated readiness places sustained demands on personnel, equipment and the national budget.')
loc('nr_civil_defence', 'Civil Defence Mobilisation')
loc('nr_civil_defence_desc', 'Emergency services, shelter authorities and local administrations are assigned to civil defence duties.')
loc('nr_tt_arsenal', 'At least 1 nuclear missile in storage is required.')
loc('nr_tt_transition', 'The previous readiness order has been completed.')
loc('nr_tt_standdown', 'No agreed stand-down is in force.')
loc('nr_tt_tactical_ready', 'Requires Reinforced Readiness or higher, 1 operational nuclear missile and no agreed stand-down in force.')
loc('nr_tt_state_ready', 'Requires Strategic Alert or higher, 20 operational nuclear missiles and no agreed stand-down in force.')
loc('nr_tt_strategic_ready', 'Requires Maximum Readiness, 200 operational nuclear missiles and no agreed stand-down in force.')
loc('nr_tt_warning', 'Requires Reinforced Readiness or higher, completed preparations, an available nuclear arsenal and a sovereign government outside our faction. Neither government may be engaged in another nuclear confrontation or a 90-day cooling-off period.')
loc('nr_tt_counter', 'We are the recipient of an active nuclear warning, have reached Reinforced Readiness or higher and have not yet issued a counter-alert.')
loc('nr_tt_crisis', 'This government is our counterpart in an active nuclear confrontation.')
loc('nr_tt_withdraw', 'We issued the original warning to this government and the confrontation is still active.')
loc('nr_tt_hotline', 'An active nuclear confrontation has no direct communications channel or unanswered proposal. Proposals may be sent once every 21 days.')
loc('nr_tt_standdown', 'No agreed stand-down is in force.')
loc('nr_tt_standdown_offer', 'A direct communications channel is open. No proposal is pending. Proposals may be sent once every 21 days.')
loc('nr_tt_assess', 'A strategic assessment of this government has not been requested in the last 14 days.')
loc('nr_warning', 'Issue a Nuclear Warning')
# IMPERIA CW — Cold War: scope-independent diplomatic descriptions.
loc('nr_warning_send', 'Issue a formal nuclear warning to this government.\\n\\n§YCold War tension:§! §R+5§!\\n§YWorld tension:§! §R+2§!\\n§YDuration:§! 90 days\\n§YCooling-off period after closure:§! 90 days')
loc('nr_warning_receive', '[Root.GetNameDefCap] has issued a formal nuclear warning to our government.')
loc('nr_warning_accept_title', 'Nuclear Warning Delivered')
loc('nr_warning_accept', 'Our warning has been delivered to [This.GetNameDef].')
loc('nr_counter', 'Announce a Nuclear Counter-Alert')
loc('nr_counter_send', 'Announce a nuclear counter-alert to this government.\\n\\n§YCold War tension:§! §R+3§!\\n§YWorld tension:§! §R+1§!\\nOur readiness posture becomes publicly known.')
loc('nr_counter_receive', '[Root.GetNameDefCap] has announced a nuclear counter-alert.')
loc('nr_counter_accept_title', 'Counter-Alert Delivered')
loc('nr_counter_accept', 'Our counter-alert has been communicated to [This.GetNameDef].')
loc('nr_hotline', 'Propose Direct Crisis Communications')
loc('nr_hotline_send', 'Propose a direct communications channel between our governments.\\n\\n§YOn acceptance:§! Opens negotiations for a mutual stand-down.\\n§YOffer valid for:§! 14 days')
loc('nr_hotline_receive', '[Root.GetNameDefCap] proposes a direct channel between our governments.\\n\\n§YOn acceptance:§! Opens negotiations for a mutual stand-down.')
loc('nr_hotline_accept_title', 'Direct Communications Agreed')
loc('nr_hotline_accept', 'Both governments have agreed to maintain direct crisis communications.')
loc('nr_standdown', 'Propose a Mutual Nuclear Stand-Down')
loc('nr_standdown_send', 'Propose a coordinated nuclear stand-down.\\n\\n§YBoth governments on acceptance:§!\\nReturn to §YRoutine Deterrence§!.\\nCancel outstanding readiness orders.\\nObserve a §Y30-day§! stand-down.\\n§YCold War tension:§! §G−[?Root.nr_pressure|2]§!\\n§YCooling-off period:§! 90 days\\n§YOffer valid for:§! 14 days')
loc('nr_standdown_receive', '[Root.GetNameDefCap] proposes a coordinated stand-down.\\n\\n§YBoth governments on acceptance:§!\\nReturn to §YRoutine Deterrence§!.\\nCancel outstanding readiness orders.\\nObserve a §Y30-day§! stand-down.\\n§YCold War tension:§! §G−[?Root.nr_pressure|2]§!\\n§YCooling-off period:§! 90 days')
loc('nr_standdown_accept_title', 'Mutual Stand-Down Agreed')
loc('nr_standdown_accept', 'Both governments have agreed to return to routine nuclear readiness for 30 days.')
loc('nr_offer_reject_title', 'Proposal Declined')
loc('nr_offer_reject', '[This.GetNameDefCap] has declined our proposal. Existing military postures remain in place.')
loc('nr_withdraw', 'Withdraw the Nuclear Warning')
# IMPERIA CW — Cold War: bounded withdrawal effects without scoped placeholders.
loc('nr_withdraw_send', 'Withdraw our nuclear warning and return our forces to routine readiness.\\n\\n§YOur stand-down:§! 14 days\\n§YCold War tension reduction:§! §GUp to 2§!\\n§YCooling-off period:§! 90 days\\nThe reduction cannot exceed the tension added by this confrontation. The other government retains control of its readiness posture.')
loc('nr_withdraw_receive', '[Root.GetNameDefCap] has ended the nuclear confrontation.')
loc('nr_withdraw_accept_title', 'Warning Withdrawn')
loc('nr_withdraw_accept', 'Our government has returned its strategic forces to routine readiness.')
loc('nr_assess', 'Request a Strategic Intelligence Assessment')
# IMPERIA CW — Cold War: concise strategic assessment wording.
loc('nr_assess_send', 'Request a strategic intelligence assessment.\\n\\n§YBelow 35% air intelligence:§! Unconfirmed.\\n§Y35% air intelligence, allied liaison or a public warning:§! General posture.\\n§Y65% air intelligence:§! Confirmed readiness level.\\n§YDiscovery of a concealed strategic or maximum alert:§! §R+1 Cold War tension§!, once per government every 30 days.\\n§YNew assessment available in:§! 14 days')
loc('nr_assess_receive', 'A strategic intelligence assessment has been requested.')
loc('nr_assess_accept_title', 'Assessment Requested')
loc('nr_assess_accept', 'The intelligence directorate has delivered its assessment.')
loc('nr_warning_threat', 'Formal Nuclear Warning')
loc('nr_counter_threat', 'Nuclear Counter-Alert')
for level, (name, ready, reserve, factor) in LEVELS.items():
    loc(f'nr_level_{level}', name)
    loc(f'nr_order_{level}', f'{level}  {name}')
    permission = {5:'Additional preparation is required before nuclear operations.',4:'Additional preparation is required before nuclear operations.',3:'Tactical nuclear operations may be prepared.',2:'Tactical and state nuclear operations may be prepared.',1:'All nuclear operations may be prepared.'}[level]
    loc(f'nr_level_{level}_tt', f'§Y{name}§!\\n\\nOperational share: §Y{ready:.0%}§!\\nDispersed reserve: §Y{reserve:.0%}§!\\nWeekly readiness budget: §Y×{factor:g}§!\\n\\n{permission} Employment remains subject to national doctrine.\\n\\n§YOrder cost:§! 25 political power\\n§YPreparation:§! 2 days per level raised; reductions take effect immediately.')
loc('nr_assessment_unknown', '§YConfidence: Low§!\\nThe available evidence does not support a reliable assessment of the government’s nuclear readiness.')
loc('nr_assessment_routine', '§YConfidence: Assessed§!\\nThe strategic forces appear to be at routine readiness or increased vigilance.')
loc('nr_assessment_elevated', '§YConfidence: Assessed§!\\nThe strategic forces appear to be at reinforced readiness or strategic alert.')
loc('nr_assessment_maximum', '§YConfidence: Assessed§!\\nThe strategic forces appear to be at maximum readiness.')
for level,(name,*_) in LEVELS.items():
    loc(f'nr_assessment_exact_{level}', f'§YConfidence: Confirmed§!\\nCurrent readiness: §Y{name}§!.')

texts = 'defined_text = { name = nr_level_L\n'
for level in LEVELS:
    texts += f'text = {{ trigger = {{ check_variable = {{ nr_level = {level} }} }} localization_key = nr_level_{level} }}\n'
texts += 'text = { localization_key = nr_level_5 } }\n'
texts += 'defined_text = { name = nr_assessment_L\n'
for level in LEVELS:
    texts += f'text = {{ trigger = {{ check_variable = {{ nr_assessment = 2 }} check_variable = {{ nr_assessed_level = {level} }} }} localization_key = nr_assessment_exact_{level} }}\n'
for level,name in [(5,'routine'),(3,'elevated'),(1,'maximum')]:
    texts += f'text = {{ trigger = {{ check_variable = {{ nr_assessment = 1 }} check_variable = {{ nr_assessed_level = {level} }} }} localization_key = nr_assessment_{name} }}\n'
texts += 'text = { localization_key = nr_assessment_unknown } }\n'
texts += '''defined_text = { name = nr_withdraw_relief_L
    text = { trigger = { check_variable = { nr_pressure > 1.99999 } } localization_key = nr_relief_2 }
    text = { localization_key = nr_relief_current }
}\n'''
loc('nr_relief_2','2')
loc('nr_relief_current','[?Root.nr_pressure|2]')
source('common/scripted_localisation/COLDWAR_nuclear_readiness.txt', texts)

loc('nr_launcher_tt', '§YStrategic Command§!\\nCurrent posture: §Y[nr_level_L]§!\\n\\nReview strategic readiness, civil defence and nuclear crisis communications.')
loc('nr_launcher_value', '[nr_digit_L]')
loc('nr_current', '[nr_level_L]')
# IMPERIA CW — Cold War: institutional instrument-panel labels and state annunciators.
loc('nr_posture_label', '01 / READINESS POSTURE')
loc('nr_arsenal_title', '02 / ARSENAL & SUSTAINMENT')
loc('nr_in_force', 'IN FORCE')
loc('nr_preparing', 'PREPARING')
loc('nr_notice_standdown', '§YSTAND-DOWN IN FORCE§!')
loc('nr_notice_orders', '§YPREPARATIONS UNDERWAY§!')
loc('nr_notice_ready', 'POSTURE IN FORCE')
loc('nr_fatigue_high', '§R[?nr_fatigue|0] / 100§!')
loc('nr_fatigue_elevated', '§Y[?nr_fatigue|0] / 100§!')
loc('nr_stock_label', 'MISSILES IN STORAGE')
loc('nr_stock_value', '[?nr_arsenal|0]')
loc('nr_ready_label', 'OPERATIONAL ALLOCATION')
loc('nr_ready_value', '[?nr_ready_count|0]  §g/ [?nr_ready_share|%0]§!')
loc('nr_reserve_label', 'DISPERSED RESERVE')
loc('nr_reserve_value', '[?nr_protected_count|0]  §g/ [?nr_reserve_share|%0]§!')
loc('nr_stock_tt', '§YMissiles in storage§!\\nNuclear ballistic missiles and intercontinental missiles held in the national stockpile. Deployed weapons remain under their assigned commands.')
loc('nr_ready_tt', '§YOperational allocation§!\\nThe share of stored missiles assigned to immediate operations at the current readiness level. Required allocations: §Y1§! for a tactical raid, §Y20§! for a state raid and §Y200§! for a strategic raid. National doctrine and suitable delivery forces are also required.')
loc('nr_reserve_tt', '§YDispersed reserve§!\\nThis share of the stored arsenal is protected from counterforce losses. An incoming tactical, state or strategic raid destroys respectively §Y5%§!, §Y15%§! or §Y40%§! of the remaining exposed stockpile.')
loc('nr_forces_label', 'STRATEGIC FORCES / WEEK')
loc('nr_forces_value', '$[?nr_forces_weekly|3]B')
loc('nr_civil_label', 'CIVIL DEFENCE / WEEK')
loc('nr_civil_value', '$[?nr_civil_weekly|3]B')
loc('nr_fatigue_label', 'ALERT FATIGUE')
loc('nr_fatigue_value', '[?nr_fatigue|0] / 100')
loc('nr_budget_tt', '§YWeekly strategic forces budget§!\\nBase: §Y$0.002B§! plus §Y$0.00001B§! per stored missile, multiplied by readiness, fatigue, national wage levels and inflation.\\nReadiness multipliers: §Y1 / 1.15 / 1.4 / 1.8 / 2.5§!.\\nAlert fatigue adds up to §Y50%§! to this budget.\\n\\nCivil defence costs §Y$0.002B§! plus §Y0.002% of GDP§! per week, adjusted for inflation. Both expenses are included in the Defence Budget.')
loc('nr_fatigue_tt', '§YAlert fatigue§!\\nDaily change:\\nMaximum Readiness: §R+2§!\\nStrategic Alert: §R+1§!\\nReinforced Readiness: §R+0.25§!\\nRoutine Deterrence / Increased Vigilance: §G−2§!\\n\\nAt 100 fatigue: §R−5 percentage points§! stability and §R+50%§! readiness costs. Fatigue recovers as forces stand down.')
loc('nr_civil_title', '03 / CIVIL DEFENCE')
loc('nr_civil_inactive', 'Emergency services at routine readiness.')
loc('nr_civil_preparing', 'Shelter and emergency preparations: §Y[?nr_civil_days|0] days§!.')
loc('nr_civil_active_text', '§GProtection active§!  |  Nuclear population losses §Y-20%§!.')
loc('nr_civil_start', 'Mobilise  £pol_power  25')
loc('nr_civil_stop', 'Release Civil Defence')
loc('nr_civil_tt', '§YCivil defence mobilisation§!\\nCost: §Y25 political power§!\\nPreparation: §Y3 days§!\\nConstruction speed: §R−3%§!\\nFactory output: §R−3%§!\\n\\nOnce preparations are complete, population losses from nuclear attacks are reduced by §G20%§! after existing shelter protection. Weekly funding begins when mobilisation is ordered.')
loc('nr_crisis_title', '04 / CRISIS COMMUNICATIONS')
loc('nr_crisis_none', 'No formal nuclear confrontation.')
loc('nr_crisis_partner', 'Counterpart: §Y[?nr_opponent.GetNameDef]§!')
loc('nr_crisis_hotline', '§GDirect channel established§!  |  Mutual stand-down available.')
loc('nr_crisis_no_hotline', 'Direct communications have not been agreed.')
loc('nr_crisis_hint', 'Warnings, intelligence assessments and negotiations are available through diplomacy.')
loc('nr_consult', 'Consult Allies  £pol_power  20')
loc('nr_consult_tt', '§YUrgent allied consultations§!\\nCost: §Y20 political power§!\\nBrief allied player governments on the current confrontation.\\nAvailable once every §Y30 days§!.')
loc('nr_order_pending', 'Readiness order in progress: §Y[?nr_build_days|0] days§!.')
loc('nr_order_none', 'Readiness orders: 25 political power  |  2 days per level raised.')
loc('nr_cancel_order', 'Cancel Preparations')
loc('nr_cancel_tt', 'Cancel the outstanding readiness order. The current posture remains in force. Political power is not refunded.')
loc('nr_footer', 'READINESS  •  DETERRENCE  •  DIRECT COMMUNICATIONS')
loc('nr_ai_reason', 'Crisis communications')
for key, value in escalation.LOCALISATION.items():
    loc(key, value)
for name, branches, fallback in [
    ('nr_civil_status_L', [('has_country_flag = nr_civil_active','nr_civil_active_text'),('check_variable = { nr_civil_days > 0 }','nr_civil_preparing')], 'nr_civil_inactive'),
    ('nr_crisis_status_L', [('nr_pair_valid = yes','nr_crisis_partner')], 'nr_crisis_none'),
    ('nr_hotline_status_L', [('has_country_flag = nr_hotline','nr_crisis_hotline')], 'nr_crisis_no_hotline'),
    ('nr_order_status_L', [('check_variable = { nr_build_days > 0 }','nr_order_pending')], 'nr_order_none'),
]:
    texts += f'defined_text = {{ name = {name}\n'
    for condition,key in branches:
        texts += f'text = {{ trigger = {{ {condition} }} localization_key = {key} }}\n'
    texts += f'text = {{ localization_key = {fallback} }} }}\n'
source('common/scripted_localisation/COLDWAR_nuclear_readiness.txt', texts)
texts += 'defined_text = { name = nr_digit_L\n'
for level in LEVELS:
    texts += f'text = {{ trigger = {{ check_variable = {{ nr_level = {level} }} }} localization_key = nr_digit_{level} }}\n'
texts += 'text = { localization_key = nr_digit_5 } }\n'
texts += escalation.SCRIPTED_TEXT
texts += command_ui.SCRIPTED_TEXT
source('common/scripted_localisation/COLDWAR_nuclear_readiness.txt', texts)

# IMPERIA CW — Cold War: the command panel uses native, localised instrument widgets.
source('interface/COLDWAR_nuclear_readiness.gui', command_ui.gui_source(loc, LEVELS))

controller = '''scripted_gui = {
nr_launcher_gui = {
    context_type = player_context window_name = "nr_launcher" dirty = nr_dirty
    ai_enabled = { always = no }
    visible = { is_ai = no nr_enabled = yes NOT = { has_country_flag = hide_money } }
    effects = { nr_launch_click = {
        nr_init = yes
        if = { limit = { has_country_flag = nr_open } clr_country_flag = nr_open }
        else = { set_country_flag = nr_open }
        nr_touch = yes
    } }
}
nr_command_gui = {
    context_type = player_context window_name = "nr_window" dirty = nr_dirty
    ai_enabled = { always = no }
    visible = { is_ai = no nr_enabled = yes has_country_flag = nr_open }
    triggers = {
        nr_cancel_visible = { check_variable = { nr_build_days > 0 } }
        nr_civil_start_click_enabled = { has_political_power > 24 has_capitulated = no NOT = { has_country_flag = nr_civil_active } check_variable = { nr_civil_days = 0 } }
        nr_civil_stop_click_enabled = { OR = { has_country_flag = nr_civil_active check_variable = { nr_civil_days > 0 } } }
        nr_consult_visible = { nr_pair_valid = yes }
        nr_consult_click_enabled = { nr_pair_valid = yes is_in_faction = yes has_political_power > 19 NOT = { has_country_flag = nr_consulted } }
        nr_hotline_status_visible = { nr_pair_valid = yes }
'''
for level in LEVELS:
    controller += f'''
        nr_level_{level}_click_enabled = {{ nr_can_change = yes NOT = {{ check_variable = {{ nr_level = {level} }} }} }}
        nr_active_{level}_visible = {{ check_variable = {{ nr_level = {level} }} }}
    '''
controller += command_ui.visibility_triggers()
controller += '''
    }
    effects = {
        nr_close_click = { clr_country_flag = nr_open nr_touch = yes }
        nr_cancel_click = { set_variable = { nr_build_days = 0 } set_variable = { nr_order = nr_level } nr_touch = yes }
        nr_civil_start_click = { nr_start_civil = yes }
        nr_civil_stop_click = { nr_end_civil = yes }
        nr_consult_click = {
            if = { limit = { nr_pair_valid = yes is_in_faction = yes has_political_power > 19 NOT = { has_country_flag = nr_consulted } }
                add_political_power = -20 nr_consult_allies = yes
            }
        }
'''
for level in LEVELS:
    controller += f'nr_level_{level}_click = {{ nr_order_level = {{ LEVEL = {level} }} }}\n'
controller += '} } }'
source('common/scripted_guis/COLDWAR_nuclear_readiness.txt', controller)

# IMPERIA CW — Cold War: export the command insignia, instruments and typography.
def artwork():
    source('interface/COLDWAR_nuclear_readiness.gfx', command_ui.artwork(ROOT))

# IMPERIA CW — Cold War: native diplomatic-action titles and hover descriptions.
for action_name, title in {
    'warning': 'Issue a Nuclear Warning',
    'counter': 'Announce a Nuclear Counter-Alert',
    'hotline': 'Propose Crisis Communications',
    'standdown': 'Propose a Mutual Stand-Down',
    'withdraw': 'Withdraw Nuclear Warning',
    'assess': 'Request Strategic Assessment',
    'ultimatum': 'Issue Nuclear Ultimatum',
    'revoke': 'Withdraw Nuclear Ultimatum',
}.items():
    native_key = f'COLDWAR_NR_{action_name.upper()}'
    LOC[native_key + '_TITLE'] = title
    # IMPERIA CW — Cold War: diplomacy hover text has no event/country text context.
    hover = LOC[f'COLDWAR_nr_{action_name}_send']
    if action_name == 'standdown':
        hover = hover.replace(
            '§YCold War tension:§! §G-[?Root.COLDWAR_nr_pressure|2]§!',
            '§YCold War tension reduction:§! §GUp to 18§!')
        hover += '\\nThe reduction cannot exceed the tension added by this confrontation.'
    assert '[' not in hover and ']' not in hover, native_key
    LOC[native_key + '_ACTION_DESC'] = hover

if __name__ == '__main__':
    artwork()
    write_all()
