# IMPERIA CW — Cold War: final ultimatums and deliberate nuclear first use.
"""Author the peacetime release procedure; launches remain native nuclear raids."""

TRIGGERS = '''
nr_first_use_policy = {
    nr_nuclear_power = yes is_ai = no is_subject = no
    has_idea = nuclear_power_off
    OR = { has_idea = full_first_use has_idea = tac_first_use_strat_retaliation }
}
nr_first_use_posture = {
    nr_first_use_policy = yes
    check_variable = { nr_level = 1 }
    check_variable = { nr_build_days = 0 }
    NOT = { has_country_flag = nr_standdown }
}
nr_can_ultimatum_prev = {
    nr_is_opponent_prev = yes nr_first_use_posture = yes
    NOT = { has_variable = nr_fu_partner }
    NOT = { has_country_flag = nr_fu_cooldown }
    NOT = { has_war_with = PREV }
    PREV = {
        exists = yes has_capitulated = no is_subject = no
        NOT = { is_in_faction_with = ROOT }
        NOT = { has_non_aggression_pact_with = ROOT }
    }
}
nr_first_use_context = {
  if = { limit = { has_variable = nr_fu_partner }
    nr_first_use_posture = yes nr_pair_valid = yes
    check_variable = { nr_fu_partner = nr_opponent }
    check_variable = { nr_fu_serial = nr_serial }
    check_variable = { nr_fu_own_use = nr_strike_revision }
    var:nr_fu_partner = {
        exists = yes has_capitulated = no is_subject = no
        check_variable = { nr_strike_revision = PREV.nr_fu_peer_use }
        NOT = { has_war_with = PREV }
        NOT = { is_in_faction_with = PREV }
        NOT = { has_non_aggression_pact_with = PREV }
    }
  }
  else = { always = no }
}
nr_can_revoke_prev = {
    nr_is_opponent_prev = yes
    check_variable = { nr_fu_partner = PREV.id }
    check_variable = { nr_fu_serial = nr_serial }
    OR = { has_country_flag = nr_fu_waiting has_country_flag = nr_fu_authorised }
}
nr_release_for_from = {
    nr_first_use_context = yes
    check_variable = { nr_fu_partner = FROM.id }
    has_country_flag = nr_fu_authorised
    check_variable = { nr_fu_hours > 0 }
}
nr_ultimatum_for_from = {
    nr_first_use_context = yes
    check_variable = { nr_fu_partner = FROM.id }
    OR = { has_country_flag = nr_fu_waiting has_country_flag = nr_fu_authorised }
    check_variable = { nr_fu_hours > 0 }
}
nr_raid_target_from = {
    FROM = {
        exists = yes has_capitulated = no
        NOT = { tag = ROOT }
        NOT = { is_subject_of = ROOT }
        NOT = { has_non_aggression_pact_with = ROOT }
        NOT = { is_in_faction_with = ROOT }
    }
}
nr_can_prepare_nuclear_operation = {
    if = { limit = { nr_enabled = yes }
        custom_trigger_tooltip = { tooltip = nr_tt_prepare_first_use
            nr_raid_target_from = yes
            OR = { has_war_with = FROM nr_ultimatum_for_from = yes }
        }
    }
    else = { has_war_with = FROM }
}
nr_can_prepare_tactical_operation = {
    if = { limit = { nr_enabled = yes } nr_can_prepare_nuclear_operation = yes }
}
nr_can_launch_nuclear_operation = {
    if = { limit = { nr_enabled = yes }
        custom_trigger_tooltip = { tooltip = nr_tt_launch_first_use
            nr_raid_target_from = yes
            OR = { has_war_with = FROM nr_release_for_from = yes }
        }
    }
    else = { has_war_with = FROM }
}
nr_foreign_ultimatum = {
  if = { limit = { nr_pair_valid = yes }
    var:nr_opponent = {
        check_variable = { nr_fu_partner = PREV.id }
        check_variable = { nr_fu_serial = PREV.nr_serial }
        OR = { has_country_flag = nr_fu_waiting has_country_flag = nr_fu_authorised }
    }
  }
  else = { always = no }
}
nr_foreign_release = {
  if = { limit = { nr_pair_valid = yes }
    var:nr_opponent = {
        check_variable = { nr_fu_partner = PREV.id }
        check_variable = { nr_fu_serial = PREV.nr_serial }
        has_country_flag = nr_fu_authorised
    }
  }
  else = { always = no }
}
'''

EFFECTS = '''
nr_update_release_display = {
    if = { limit = { has_variable = nr_fu_partner }
        var:nr_fu_partner = {
            if = { limit = { check_variable = { nr_opponent = PREV.id } }
                set_variable = { nr_fu_incoming_hours = PREV.nr_fu_hours }
                nr_touch = yes
            }
        }
    }
    nr_touch = yes
}
nr_clear_first_use = {
    if = { limit = { has_variable = nr_fu_partner }
        var:nr_fu_partner = {
            if = { limit = { check_variable = { nr_opponent = PREV.id } }
                set_variable = { nr_fu_incoming_hours = 0 }
                nr_touch = yes
            }
        }
    }
    clr_country_flag = nr_fu_waiting
    clr_country_flag = nr_fu_authorised
    clear_variable = nr_fu_partner
    clear_variable = nr_fu_serial
    clear_variable = nr_fu_own_use
    clear_variable = nr_fu_peer_use
    set_variable = { nr_fu_hours = 0 }
    nr_touch = yes
}
nr_first_use_notice = {
    save_event_target_as = nr_sender
    if = { limit = { has_variable = nr_fu_partner }
        var:nr_fu_partner = { save_event_target_as = nr_recipient }
        if = { limit = { is_ai = no } country_event = { id = cw_nuclear.19 } }
        var:nr_fu_partner = {
            if = { limit = { exists = yes is_ai = no } country_event = { id = cw_nuclear.19 } }
        }
    }
}
nr_validate_first_use = {
    if = { limit = { has_variable = nr_fu_partner NOT = { nr_first_use_context = yes } }
        nr_first_use_notice = yes
        nr_clear_first_use = yes
    }
}
nr_issue_ultimatum = {
    if = { limit = { nr_can_ultimatum_prev = yes }
        save_event_target_as = nr_sender
        PREV = { save_event_target_as = nr_recipient }
        set_variable = { nr_fu_partner = PREV.id }
        set_variable = { nr_fu_serial = nr_serial }
        set_variable = { nr_fu_own_use = nr_strike_revision }
        set_variable = { nr_fu_peer_use = PREV.nr_strike_revision }
        set_variable = { nr_fu_hours = 72 }
        set_country_flag = nr_fu_waiting
        clr_country_flag = nr_fu_authorised
        set_country_flag = { flag = nr_fu_cooldown days = 90 }
        set_country_flag = { flag = nr_public days = 90 }
        nr_tension = { DELTA = 5 }
        set_temp_variable = { nr_fu_pressure = nr_tension_applied }
        add_to_variable = { nr_pressure = nr_fu_pressure }
        var:nr_fu_partner = { add_to_variable = { nr_pressure = PREV.nr_fu_pressure } }
        add_named_threat = { threat = 2 name = nr_ultimatum_threat }
        var:nr_fu_partner = {
            if = { limit = { is_ai = no } country_event = { id = cw_nuclear.15 } }
        }
        every_country = {
            limit = { is_ai = no NOT = { tag = event_target:nr_sender } NOT = { tag = event_target:nr_recipient } }
            country_event = { id = cw_nuclear.18 }
        }
        nr_update_release_display = yes
        country_event = { id = cw_nuclear.90 hours = 2 }
    }
}
nr_revoke_first_use = {
    if = { limit = { nr_can_revoke_prev = yes }
        nr_first_use_notice = yes
        nr_clear_first_use = yes
    }
}
nr_first_use_tick = {
    nr_advance_first_use = yes
    if = { limit = { has_variable = nr_fu_partner }
        country_event = { id = cw_nuclear.90 hours = 2 }
    }
}
nr_advance_first_use = {
    nr_validate_first_use = yes
    if = { limit = { has_variable = nr_fu_partner }
        subtract_from_variable = { nr_fu_hours = 1 }
        if = { limit = { check_variable = { nr_fu_hours < 1 } }
            if = { limit = { has_country_flag = nr_fu_waiting }
                clr_country_flag = nr_fu_waiting
                set_country_flag = nr_fu_authorised
                set_variable = { nr_fu_hours = 168 }
                save_event_target_as = nr_sender
                var:nr_fu_partner = { save_event_target_as = nr_recipient }
                if = { limit = { is_ai = no } country_event = { id = cw_nuclear.16 } }
                var:nr_fu_partner = {
                    if = { limit = { is_ai = no } country_event = { id = cw_nuclear.17 } }
                }
            }
            else = {
                save_event_target_as = nr_sender
                var:nr_fu_partner = {
                    save_event_target_as = nr_recipient
                    if = { limit = { is_ai = no } country_event = { id = cw_nuclear.20 } }
                }
                if = { limit = { is_ai = no } country_event = { id = cw_nuclear.20 } }
                nr_clear_first_use = yes
            }
        }
        nr_update_release_display = yes
    }
}
nr_resolve_peacetime_operation = {
    var:actor_country = { save_event_target_as = nr_operation_attacker }
    var:victim_country = { save_event_target_as = nr_operation_victim }
    event_target:nr_operation_attacker = {
        if = { limit = {
            nr_enabled = yes
            NOT = { has_war_with = event_target:nr_operation_victim }
            event_target:nr_operation_victim = { exists = yes }
        }
            declare_war_on = { target = event_target:nr_operation_victim type = annex_everything }
            if = { limit = { has_war_with = event_target:nr_operation_victim }
                save_event_target_as = nr_sender
                event_target:nr_operation_victim = { save_event_target_as = nr_recipient }
                set_country_flag = { flag = nr_nuclear_aggressor days = 365 }
                set_country_flag = { flag = nr_public days = 90 }
                add_to_variable = { nr_strike_revision = 1 }
                nr_clear_first_use = yes
                add_stability = -0.05
                if = { limit = { has_global_flag = mdcw_cw_initialized }
                    set_temp_variable = { mdcw_cw_tension_delta = 20 }
                    mdcw_cw_add_tension = yes
                }
                add_named_threat = { threat = 10 name = nr_first_use_threat }
                event_target:nr_operation_victim = {
                    nr_clear_first_use = yes
                    nr_init = yes
                    add_to_variable = { nr_strike_revision = 1 }
                    if = { limit = { NOT = { is_in_array = { array = nr_aggressors value = event_target:nr_operation_attacker.id } } }
                        add_to_array = { array = nr_aggressors value = event_target:nr_operation_attacker.id }
                    }
                    set_variable = { nr_last_aggressor = event_target:nr_operation_attacker.id }
                    clr_country_flag = nr_standdown
                    if = { limit = { nr_nuclear_power = yes NOT = { check_variable = { nr_level = 1 } } }
                        set_variable = { nr_order = 1 }
                        set_variable = { nr_build_days = 1 }
                    }
                    nr_touch = yes
                }
                every_country = {
                    limit = { exists = yes NOT = { tag = event_target:nr_operation_attacker } }
                    add_opinion_modifier = { target = event_target:nr_operation_attacker modifier = nr_first_use_condemnation }
                }
                every_country = { limit = { is_ai = no } country_event = { id = cw_nuclear.21 } }
                nr_touch = yes
            }
        }
    }
}
'''

EVENT_COPY = {
    15: ('A Final Nuclear Ultimatum', '[nr_sender.GetNameDefCap] has issued a final nuclear ultimatum to our government. Its cabinet will be able to authorise nuclear operations after 72 hours. Direct communications and a mutual stand-down remain available.'),
    16: ('Nuclear Release Authority Granted', 'The 72-hour ultimatum has expired. The cabinet has granted seven days of nuclear release authority against [nr_recipient.GetNameDef]. A separate military order is required to carry out an operation. The first operation will open a state of war.'),
    17: ('A Foreign Nuclear Release Order', '[nr_sender.GetNameDefCap] has completed its ultimatum and authorised nuclear operations against our government for seven days. The danger of an attack is immediate. Direct negotiations can still secure a mutual stand-down.'),
    18: ('An Ultimatum Threatens Nuclear Use', '[nr_sender.GetNameDefCap] has delivered a 72-hour nuclear ultimatum to [nr_recipient.GetNameDef]. Diplomatic missions are seeking a negotiated reduction of readiness before nuclear operations can be authorised.'),
    19: ('Nuclear Release Authority Withdrawn', '[nr_sender.GetNameDefCap] has withdrawn its final ultimatum and any associated nuclear release authority. National readiness orders remain in force. Operations already underway remain committed.'),
    20: ('Nuclear Release Authority Expires', 'The nuclear release authority held by [nr_sender.GetNameDef] against [nr_recipient.GetNameDef] has expired. Further operations outside an existing war require a new authorisation. National readiness remains under government control.'),
    21: ('A Nuclear Operation Opens Hostilities', '[nr_sender.GetNameDefCap] has carried out a nuclear operation against [nr_recipient.GetNameDef] before a declaration of war. A state of war now exists between the two governments, irrespective of the operation\'s outcome. Foreign governments have condemned the attack.'),
}

LOCALISATION = {
    'nr_tt_ultimatum': 'Requires an active nuclear confrontation, Maximum Readiness with preparations complete, offensive nuclear policy and a doctrine permitting first use. Both governments must be independent, at peace with each other and outside the same faction, with no non-aggression pact. No agreed stand-down or 90-day ultimatum cooling-off period may be in force.',
    'nr_tt_revoke': 'Our final ultimatum or nuclear release authority against this government is still in force.',
    'nr_tt_prepare_first_use': 'Requires war with this government or a final nuclear ultimatum at Maximum Readiness. The target must be outside our faction, outside our own subjects and not protected by a non-aggression pact.',
    'nr_tt_launch_first_use': 'Requires war with this government or valid nuclear release authority after the 72-hour ultimatum. Operations outside an existing war require Maximum Readiness and an eligible crisis counterpart. National employment doctrine still applies.',
    'nr_ultimatum_send': 'Deliver a final nuclear ultimatum to this government.\n\n§YCost:§! 100 political power\n§YUltimatum:§! 72 hours\n§YNuclear release authority after expiry:§! 7 days\n§YCold War tension:§! §R+5§!\n§YWorld tension:§! §R+2§!\n§YFurther ultimatums:§! 90-day cooling-off period\n\nNuclear operations require a separate military order. The first operation opens war, including an intercepted or unsuccessful attack.\n§YAdditional consequences on execution:§!\n§R+20§! Cold War tension; §R+10§! world tension.\n§R-5%§! stability.\nForeign opinion: §R-100§! for §Y365 days§!.\nA mutual stand-down cancels release authority. Withdrawing authority prevents further launches; operations already underway remain committed.',
    'nr_ultimatum_receive': 'Our government has received a final nuclear ultimatum.\n\n§YUltimatum:§! 72 hours\n§YRelease authority after expiry:§! 7 days\nNuclear operations can open war without a prior declaration. Direct communications and a mutual stand-down remain available.',
    'nr_ultimatum_accept_title': 'Final Ultimatum Delivered',
    'nr_ultimatum_accept': 'The final ultimatum has been delivered. The cabinet will review nuclear release authority after 72 hours.',
    'nr_revoke_send': 'Withdraw our final ultimatum and nuclear release authority.\n\n§YFurther launches outside an existing war:§! Cancelled\nCurrent national readiness remains in force.\nOperations already underway remain committed.\nThe 90-day ultimatum cooling-off period remains in force. Political power and tension already incurred are not refunded.',
    'nr_revoke_receive': 'The final nuclear ultimatum and associated release authority have been withdrawn. Current readiness remains under national control.',
    'nr_revoke_accept_title': 'Release Authority Withdrawn',
    'nr_revoke_accept': 'The cabinet has withdrawn its final ultimatum and nuclear release authority. Existing readiness orders remain in force.',
    'nr_ultimatum_threat': 'Final Nuclear Ultimatum',
    'nr_first_use_threat': 'Nuclear First Use Opens Hostilities',
    'nr_first_use_condemnation': 'Nuclear First Use',
    'nr_fu_waiting_text': '§RFinal ultimatum: [?nr_fu_hours|0] hours remaining§!',
    'nr_fu_authorised_text': '§RNuclear release authority: [?nr_fu_hours|0] hours remaining§!',
    'nr_fu_incoming_text': '§RForeign final ultimatum: [?nr_fu_incoming_hours|0] hours remaining§!',
    'nr_fu_foreign_release_text': '§RForeign nuclear release authority: [?nr_fu_incoming_hours|0] hours remaining§!',
    'nr_fu_both_text': '§RBoth governments have issued nuclear ultimatums or release orders.§!',
    'nr_fu_none_text': 'No final nuclear ultimatum or release authority is in force.',
    'nr_escalation_tt': '§YNuclear escalation§!\n\n§YOur government:§! [nr_fu_own_status_L]\n§YOur counterpart:§! [nr_fu_peer_status_L]\n\nUltimatums last §Y72 hours§!, followed by §Y7 days§! of release authority. A separate military order is required. A mutual stand-down cancels both governments\' release authority. Operations already underway remain committed.',
}

SCRIPTED_TEXT = '''
defined_text = { name = nr_fu_own_status_L
    text = { trigger = { has_country_flag = nr_fu_authorised } localization_key = nr_fu_authorised_text }
    text = { trigger = { has_country_flag = nr_fu_waiting } localization_key = nr_fu_waiting_text }
    text = { localization_key = nr_fu_none_text }
}
defined_text = { name = nr_fu_peer_status_L
    text = { trigger = { nr_foreign_release = yes } localization_key = nr_fu_foreign_release_text }
    text = { trigger = { nr_foreign_ultimatum = yes } localization_key = nr_fu_incoming_text }
    text = { localization_key = nr_fu_none_text }
}
defined_text = { name = nr_escalation_status_L
    text = { trigger = { nr_foreign_ultimatum = yes OR = { has_country_flag = nr_fu_waiting has_country_flag = nr_fu_authorised } } localization_key = nr_fu_both_text }
    text = { trigger = { nr_foreign_release = yes } localization_key = nr_fu_foreign_release_text }
    text = { trigger = { has_country_flag = nr_fu_authorised } localization_key = nr_fu_authorised_text }
    text = { trigger = { nr_foreign_ultimatum = yes } localization_key = nr_fu_incoming_text }
    text = { trigger = { has_country_flag = nr_fu_waiting } localization_key = nr_fu_waiting_text }
    text = { localization_key = nr_crisis_hint }
}
'''
