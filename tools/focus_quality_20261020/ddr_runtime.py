# IMPERIA CW — Cold War: focus quality 20261020 — ddr runtime.
"""Emit bounded, consent-based DDR repayment and tank transactions.

No periodic on_action is installed. Work happens on focus completion, a manual
retry, or a recipient-owned response. Native send_equipment moves real stock;
licence creation is checked before any invoice or factory delivery.
"""
from pathlib import Path
from source_edit import ROOT, write

BASE = ROOT / 'Claude outputs/COLDWAR_DDR_generator/quality_runtime'
P = 'COLDWAR_DDR_Q_'


def install(relative, text):
    text = text.strip() + '\n'
    write(BASE / relative, text)
    write(ROOT / relative, text)


def build():
    effects = '''
# Approved focus quality pass: native transactions, no daily/weekly callbacks.
COLDWAR_DDR_Q_prepare_repayment = {
    set_variable = { COLDWAR_DDR_Q_repayment_cost = { value = gdp_total multiply = 0.03 min = debt max = 0 } }
}
COLDWAR_DDR_Q_finish_repayment = {
    if = {
        limit = {
            has_country_flag = COLDWAR_DDR_Q_repayment_open
            NOT = { has_country_flag = COLDWAR_DDR_Q_repayment_done }
            NOT = { has_country_flag = MD_skip_treasury_cost }
            check_variable = { COLDWAR_DDR_Q_repayment_cost > 0 }
            check_variable = { var = debt value = COLDWAR_DDR_Q_repayment_cost compare = greater_than_or_equals }
            check_variable = { var = treasury value = COLDWAR_DDR_Q_repayment_cost compare = greater_than_or_equals }
        }
        set_temp_variable = { treasury_change = { value = COLDWAR_DDR_Q_repayment_cost multiply = -1 } }
        modify_treasury_effect = yes
        set_temp_variable = { debt_change = { value = COLDWAR_DDR_Q_repayment_cost multiply = -1 } }
        modify_debt_effect = yes
        add_timed_idea = { idea = COLDWAR_DDR_Q_creditworthiness days = 730 }
        add_to_variable = { COLDWAR_DDR_planned_economy_imp_sanction_resistance = 0.08 tooltip = COLDWAR_imp_sanction_resistance_tt }
        set_temp_variable = { COLDWAR_DDR_trust_delta = 5 }
        COLDWAR_DDR_change_trust = yes
        set_temp_variable = { temp_opinion = 5 }
        change_communist_cadres_opinion = yes
        add_power_balance_value = { id = COLDWAR_DDR_german_course_bop value = -0.05 tooltip_side = COLDWAR_DDR_german_course_bop_left_side }
        add_to_variable = { COLDWAR_DDR_course = -0.05 }
        clamp_variable = { var = COLDWAR_DDR_course min = -1 max = 1 }
        set_country_flag = COLDWAR_DDR_Q_repayment_done
        clr_country_flag = COLDWAR_DDR_Q_repayment_open
        clr_country_flag = COLDWAR_DDR_Q_repayment_dialog
        force_update_dynamic_modifier = yes
    }
}
COLDWAR_DDR_Q_open_repayment = {
    custom_effect_tooltip = COLDWAR_DDR_Q_repayment_terms_tt
    effect_tooltip = { add_timed_idea = { idea = COLDWAR_DDR_Q_creditworthiness days = 730 } }
    hidden_effect = {
        if = {
            limit = { NOT = { has_country_flag = COLDWAR_DDR_Q_repayment_done } }
            set_country_flag = COLDWAR_DDR_Q_repayment_open
            COLDWAR_DDR_Q_prepare_repayment = yes
            COLDWAR_DDR_Q_finish_repayment = yes
        }
    }
}
COLDWAR_DDR_Q_start_import = {
    custom_effect_tooltip = COLDWAR_DDR_Q_import_terms_tt
    effect_tooltip = { army_experience = 25 }
    hidden_effect = {
        if = {
            limit = { NOT = { has_country_flag = COLDWAR_DDR_Q_import_started } }
            army_experience = 25
            set_country_flag = COLDWAR_DDR_Q_import_started
            set_country_flag = COLDWAR_DDR_Q_import_open
            COLDWAR_DDR_Q_request_import = yes
        }
    }
}
COLDWAR_DDR_Q_start_licence = {
    custom_effect_tooltip = COLDWAR_DDR_Q_licence_terms_tt
    effect_tooltip = {
        add_to_variable = { COLDWAR_DDR_planned_economy_military_factories_productivity = 0.03 tooltip = military_factories_productivity_tt }
    }
    hidden_effect = {
        if = {
            limit = { NOT = { has_country_flag = COLDWAR_DDR_Q_licence_started } }
            set_country_flag = COLDWAR_DDR_Q_licence_started
            set_country_flag = COLDWAR_DDR_Q_licence_open
            COLDWAR_DDR_Q_request_licence = yes
        }
    }
}
COLDWAR_DDR_Q_request_import = {
    if = {
        limit = {
            tag = DDR
            has_country_flag = COLDWAR_DDR_Q_import_open
            NOT = { has_country_flag = COLDWAR_DDR_Q_import_done }
            NOT = { has_country_flag = COLDWAR_DDR_Q_trade_pending }
            NOT = { has_country_flag = COLDWAR_DDR_Q_trade_retry }
            country_exists = SOV
            NOT = { has_war_with = SOV }
        }
        set_variable = { COLDWAR_DDR_Q_import_price = { value = gdp_total multiply = 0.01 max = 0 } }
        set_country_flag = { flag = COLDWAR_DDR_Q_trade_pending days = 14 value = 1 }
        set_country_flag = { flag = COLDWAR_DDR_Q_trade_retry days = 30 value = 1 }
        SOV = { country_event = { id = COLDWAR_DDR_Q.1 days = 1 } }
    }
}
COLDWAR_DDR_Q_request_licence = {
    if = {
        limit = {
            tag = DDR
            has_country_flag = COLDWAR_DDR_Q_licence_open
            NOT = { has_country_flag = COLDWAR_DDR_Q_licence_done }
            NOT = { has_country_flag = COLDWAR_DDR_Q_trade_pending }
            NOT = { has_country_flag = COLDWAR_DDR_Q_trade_retry }
            country_exists = SOV
            NOT = { has_war_with = SOV }
        }
        set_variable = { COLDWAR_DDR_Q_licence_price = { value = gdp_total multiply = 0.016 max = 0 } }
        set_country_flag = { flag = COLDWAR_DDR_Q_trade_pending days = 14 value = 1 }
        set_country_flag = { flag = COLDWAR_DDR_Q_trade_retry days = 30 value = 1 }
        SOV = { country_event = { id = COLDWAR_DDR_Q.2 days = 1 } }
    }
}
COLDWAR_DDR_Q_accept_import = {
    if = {
        limit = { COLDWAR_DDR_Q_can_sell_tanks = yes }
        send_equipment = { type = medium_tank_chassis amount = 90 target = DDR }
        set_temp_variable = { treasury_change = DDR.COLDWAR_DDR_Q_import_price }
        modify_treasury_effect = yes
        DDR = {
            set_temp_variable = { treasury_change = { value = COLDWAR_DDR_Q_import_price multiply = -1 } }
            modify_treasury_effect = yes
            set_country_flag = COLDWAR_DDR_Q_import_done
            clr_country_flag = COLDWAR_DDR_Q_import_open
            clr_country_flag = COLDWAR_DDR_Q_trade_pending
            set_temp_variable = { COLDWAR_DDR_trust_delta = 3 }
            COLDWAR_DDR_change_trust = yes
            set_temp_variable = { temp_opinion = -5 }
            change_industrial_conglomerates_opinion = yes
            set_temp_variable = { temp_opinion = 10 }
            change_the_military_opinion = yes
            country_event = { id = COLDWAR_DDR_Q.3 hours = 1 }
        }
    }
}
'''
    # Prefer the newest eligible, period-correct family. Successful native
    # licensing is verified afterward: knowing a technology alone does not prove
    # that the seller has created a licensable design.
    candidates = [
        ('has_dlc = "No Step Back" date > 1974.12.31 has_tech = mbt_tech_1', 'medium_tank_chassis_1'),
        ('has_dlc = "No Step Back" has_tech = mbt_tech', 'medium_tank_chassis_0'),
        ('has_dlc = "No Step Back" has_tech = mdcw_postwar_medium_tank_1955_nsb', 'medium_tank_chassis_mdcw_1955'),
        ('NOT = { has_dlc = "No Step Back" } date > 1974.12.31 has_tech = MBT_2', 'MBT_2'),
        ('NOT = { has_dlc = "No Step Back" } has_tech = MBT_1', 'MBT_1'),
    ]
    effects += '\nCOLDWAR_DDR_Q_accept_licence = {\n    if = {\n        limit = { COLDWAR_DDR_Q_can_offer_licence = yes }\n'
    for guard, model in candidates:
        effects += f'''        if = {{
            limit = {{ {guard} DDR = {{ NOT = {{ has_license = {{ from = SOV archetype = medium_tank_chassis }} }} }} }}
            create_production_license = {{ target = DDR cost_factor = 1 equipment = {{ type = {model} }} }}
        }}
'''
    effects += '''
        if = {
            limit = { DDR = { has_license = { from = SOV archetype = medium_tank_chassis } } }
            set_temp_variable = { treasury_change = DDR.COLDWAR_DDR_Q_licence_price }
            modify_treasury_effect = yes
            DDR = {
                set_temp_variable = { treasury_change = { value = COLDWAR_DDR_Q_licence_price multiply = -1 } }
                modify_treasury_effect = yes
                random_owned_controlled_state = {
                    limit = { free_building_slots = { building = arms_factory size > 1 include_locked = no } }
                    add_extra_state_shared_building_slots = 2
                    add_building_construction = { type = arms_factory level = 2 instant_build = yes }
                }
                add_to_variable = { COLDWAR_DDR_planned_economy_military_factories_productivity = 0.03 tooltip = military_factories_productivity_tt }
                force_update_dynamic_modifier = yes
                set_temp_variable = { temp_opinion = 10 }
                change_industrial_conglomerates_opinion = yes
                set_temp_variable = { COLDWAR_DDR_trust_delta = -3 }
                COLDWAR_DDR_change_trust = yes
                set_country_flag = COLDWAR_DDR_Q_licence_done
                clr_country_flag = COLDWAR_DDR_Q_licence_open
                clr_country_flag = COLDWAR_DDR_Q_trade_pending
                country_event = { id = COLDWAR_DDR_Q.4 hours = 1 }
            }
        }
        else = {
            DDR = {
                clr_country_flag = COLDWAR_DDR_Q_trade_pending
                country_event = { id = COLDWAR_DDR_Q.5 hours = 1 }
            }
        }
    }
}
'''
    triggers = '''
COLDWAR_DDR_Q_can_sell_tanks = {
    tag = SOV
    NOT = { has_country_flag = MD_skip_treasury_cost }
    country_exists = DDR
    has_equipment = { medium_tank_chassis > 89 }
    NOT = { has_war_with = DDR }
    DDR = {
        has_country_flag = COLDWAR_DDR_Q_trade_pending
        has_country_flag = COLDWAR_DDR_Q_import_open
        NOT = { has_country_flag = COLDWAR_DDR_Q_import_done }
        NOT = { has_country_flag = MD_skip_treasury_cost }
        check_variable = { COLDWAR_DDR_Q_import_price > 0 }
        check_variable = { var = treasury value = COLDWAR_DDR_Q_import_price compare = greater_than_or_equals }
    }
}
COLDWAR_DDR_Q_can_offer_licence = {
    tag = SOV
    NOT = { has_country_flag = MD_skip_treasury_cost }
    country_exists = DDR
    NOT = { has_war_with = DDR }
    DDR = {
        has_country_flag = COLDWAR_DDR_Q_trade_pending
        has_country_flag = COLDWAR_DDR_Q_licence_open
        NOT = { has_country_flag = COLDWAR_DDR_Q_licence_done }
        NOT = { has_country_flag = MD_skip_treasury_cost }
        check_variable = { COLDWAR_DDR_Q_licence_price > 0 }
        check_variable = { var = treasury value = COLDWAR_DDR_Q_licence_price compare = greater_than_or_equals }
        any_owned_state = {
            is_controlled_by = DDR
            free_building_slots = { building = arms_factory size > 1 include_locked = no }
        }
    }
    OR = {
        DDR = { has_license = { from = SOV archetype = medium_tank_chassis } }
        AND = { has_dlc = "No Step Back" OR = { has_tech = mbt_tech has_tech = mdcw_postwar_medium_tank_1955_nsb AND = { date > 1974.12.31 has_tech = mbt_tech_1 } } }
        AND = { NOT = { has_dlc = "No Step Back" } OR = { has_tech = MBT_1 AND = { date > 1974.12.31 has_tech = MBT_2 } } }
    }
}
'''
    events = 'add_namespace = COLDWAR_DDR_Q\n'
    for n, kind in [(1, 'import'), (2, 'licence')]:
        valid = 'can_sell_tanks' if kind == 'import' else 'can_offer_licence'
        # Numeric option effects use native providers; acceptance is rechecked
        # by the authoritative helper in case the political/economic state moved.
        preview = '''send_equipment = { type = medium_tank_chassis amount = 90 target = DDR }
            custom_effect_tooltip = COLDWAR_DDR_Q_import_payment_tt''' if kind == 'import' else '''custom_effect_tooltip = COLDWAR_DDR_Q_licence_payment_tt
            custom_effect_tooltip = COLDWAR_DDR_Q_licence_native_tt'''
        events += f'''
country_event = {{
    id = COLDWAR_DDR_Q.{n}
    title = COLDWAR_DDR_Q.{n}.t
    desc = COLDWAR_DDR_Q.{n}.d
    picture = GFX_politics_negotiations
    is_triggered_only = yes
    timeout_days = 7
    option = {{
        name = COLDWAR_DDR_Q.accept
        trigger = {{ COLDWAR_DDR_Q_{valid} = yes }}
        ai_chance = {{ base = 70 modifier = {{ factor = 0.3 NOT = {{ has_government = communism }} }} }}
        effect_tooltip = {{ {preview} }}
        hidden_effect = {{ COLDWAR_DDR_Q_accept_{kind} = yes }}
    }}
    option = {{
        name = COLDWAR_DDR_Q.refuse
        ai_chance = {{ base = 30 }}
        hidden_effect = {{
            if = {{ limit = {{ country_exists = DDR DDR = {{ has_country_flag = COLDWAR_DDR_Q_trade_pending }} }} DDR = {{ clr_country_flag = COLDWAR_DDR_Q_trade_pending country_event = {{ id = COLDWAR_DDR_Q.7 hours = 1 }} }} }}
        }}
    }}
}}
'''
    for n in [3, 4, 5, 7]:
        receipt = 'custom_effect_tooltip = COLDWAR_DDR_Q_import_receipt_tt' if n == 3 else 'custom_effect_tooltip = COLDWAR_DDR_Q_licence_receipt_tt' if n == 4 else ''
        events += f'''
country_event = {{
    id = COLDWAR_DDR_Q.{n}
    title = COLDWAR_DDR_Q.{n}.t
    desc = COLDWAR_DDR_Q.{n}.d
    picture = GFX_politics_negotiations
    is_triggered_only = yes
    option = {{ name = COLDWAR_DDR_Q.ack {receipt} }}
}}
'''
    events += '''
country_event = {
    id = COLDWAR_DDR_Q.6
    title = COLDWAR_DDR_Q.6.t
    desc = COLDWAR_DDR_Q.6.d
    picture = GFX_politics_negotiations
    is_triggered_only = yes
    timeout_days = 7
    immediate = { COLDWAR_DDR_Q_prepare_repayment = yes }
    option = {
        name = COLDWAR_DDR_Q.repay
        trigger = {
            has_country_flag = COLDWAR_DDR_Q_repayment_dialog
            has_country_flag = COLDWAR_DDR_Q_repayment_open
            NOT = { has_country_flag = COLDWAR_DDR_Q_repayment_done }
            NOT = { has_country_flag = MD_skip_treasury_cost }
            check_variable = { COLDWAR_DDR_Q_repayment_cost > 0 }
            check_variable = { var = debt value = COLDWAR_DDR_Q_repayment_cost compare = greater_than_or_equals }
            check_variable = { var = treasury value = COLDWAR_DDR_Q_repayment_cost compare = greater_than_or_equals }
        }
        ai_chance = { base = 100 }
        effect_tooltip = {
            custom_effect_tooltip = COLDWAR_DDR_Q_repayment_payment_tt
            add_timed_idea = { idea = COLDWAR_DDR_Q_creditworthiness days = 730 }
        }
        hidden_effect = {
            if = { limit = { has_country_flag = COLDWAR_DDR_Q_repayment_dialog } COLDWAR_DDR_Q_finish_repayment = yes }
            clr_country_flag = COLDWAR_DDR_Q_repayment_dialog
        }
    }
    option = { name = COLDWAR_DDR_Q.cancel ai_chance = { base = 0 } clr_country_flag = COLDWAR_DDR_Q_repayment_dialog }
}
'''
    decisions = '''
COLDWAR_DDR_Q_programmes = {
    COLDWAR_DDR_Q_repayment = {
        icon = GFX_decision_generic_construction
        cost = 0
        days_re_enable = 7
        visible = { has_country_flag = COLDWAR_DDR_Q_repayment_open NOT = { has_country_flag = COLDWAR_DDR_Q_repayment_done } }
        available = { check_variable = { debt > 0 } NOT = { has_country_flag = COLDWAR_DDR_Q_repayment_dialog } }
        complete_effect = { set_country_flag = { flag = COLDWAR_DDR_Q_repayment_dialog days = 8 value = 1 } country_event = { id = COLDWAR_DDR_Q.6 hours = 1 } }
        ai_will_do = { base = 1 }
    }
'''
    for kind in ['import', 'licence']:
        decisions += f'''
    COLDWAR_DDR_Q_retry_{kind} = {{
        icon = GFX_decision_generic_military
        cost = 0
        days_re_enable = 30
        visible = {{ has_country_flag = COLDWAR_DDR_Q_{kind}_open NOT = {{ has_country_flag = COLDWAR_DDR_Q_{kind}_done }} }}
        available = {{ country_exists = SOV NOT = {{ has_war_with = SOV }} NOT = {{ has_country_flag = COLDWAR_DDR_Q_trade_pending }} NOT = {{ has_country_flag = COLDWAR_DDR_Q_trade_retry }} }}
        complete_effect = {{ COLDWAR_DDR_Q_request_{kind} = yes }}
        ai_will_do = {{ base = 1 }}
    }}
'''
    decisions += '}\n'
    category = '''
COLDWAR_DDR_Q_programmes = {
    icon = GFX_decision_category_generic_economy
    priority = 180
    allowed = { tag = DDR }
    visible = { OR = { has_country_flag = COLDWAR_DDR_Q_repayment_open has_country_flag = COLDWAR_DDR_Q_import_open has_country_flag = COLDWAR_DDR_Q_licence_open } }
}
'''
    ideas = '''
ideas = {
    country = {
        COLDWAR_DDR_Q_creditworthiness = {
            picture = export_economy
            allowed_civil_war = { always = yes }
            modifier = { interest_rate_multiplier_modifier = -0.25 }
        }
    }
}
'''
    loc = '''
l_english:
 COLDWAR_DDR_Q_programmes:0 "State Finance and Procurement"
 COLDWAR_DDR_Q_import_payment_tt:0 "Soviet treasury: §G+$[?DDR.COLDWAR_DDR_Q_import_price|2] billion§!\\nGerman treasury: §R-$[?DDR.COLDWAR_DDR_Q_import_price|2] billion§!"
 COLDWAR_DDR_Q_import_receipt_tt:0 "Completed transfer from Soviet reserves: §G90 tanks§!\\nPayment completed: §Y$[?COLDWAR_DDR_Q_import_price|2] billion§! to the Soviet treasury."
 COLDWAR_DDR_Q_licence_receipt_tt:0 "Soviet tank-production licence: §Gactive§!\\nMilitary factories delivered: §G2§!\\nMilitary-factory productivity: §G+3%§!\\nPayment completed: §Y$[?COLDWAR_DDR_Q_licence_price|2] billion§! to the Soviet treasury."
 COLDWAR_DDR_Q_licence_payment_tt:0 "Soviet treasury on successful implementation: §G+$[?DDR.COLDWAR_DDR_Q_licence_price|2] billion§!\\nGerman treasury on successful implementation: §R-$[?DDR.COLDWAR_DDR_Q_licence_price|2] billion§!"
 COLDWAR_DDR_Q_repayment_payment_tt:0 "Treasury: §R-$[?COLDWAR_DDR_Q_repayment_cost|2] billion§!\\nOutstanding debt: §G-$[?COLDWAR_DDR_Q_repayment_cost|2] billion§!\\nSanction resistance: §G+8%§!\\nMoscow's Trust: §G+5§!"
 COLDWAR_DDR_Q_creditworthiness:0 "Restored Creditworthiness"
 COLDWAR_DDR_Q_creditworthiness_desc:0 "A funded reduction in outstanding debt has strengthened confidence in the republic's finances. The interest-rate reduction is measured in percentage points."
 COLDWAR_DDR_Q_repayment_terms_tt:0 "Fund a debt repayment of up to §Y3% of current GDP§!, capped at outstanding principal. The same amount is deducted from the treasury and debt; no new borrowing finances this transaction. If funds are insufficient, the repayment remains available under §YState Finance and Procurement§!. Successful repayment also grants §G+8%§! sanction resistance, §G+5§! Moscow's Trust and moves the Inner-German course §Y0.05§! towards demarcation."
 COLDWAR_DDR_Q_import_terms_tt:0 "Request a paid transfer of §Y90 tanks§! from existing Soviet stock. The Soviet government must accept. Price: §Y1% of GDP§!, frozen when the request is sent and paid entirely to the Soviet treasury. No tanks or money change hands on refusal or failed validation. Unfinished requests can be renewed under §YState Finance and Procurement§!."
 COLDWAR_DDR_Q_licence_terms_tt:0 "Request a Soviet tank-production licence and a domestic assembly project: §Y2 military factories§!, §G+3%§! military-factory productivity. Implementation costs §Y1.6% of GDP§!, frozen when requested and paid to the Soviet treasury. Payment and factories require a successfully created licence and an eligible construction site. No future model is unlocked."
 COLDWAR_DDR_Q_licence_native_tt:0 "German Democratic Republic receives an active Soviet tank-production licence, §Y2 military factories§! and §G+3%§! military-factory productivity only after successful implementation."
 COLDWAR_DDR_Q_repayment:0 "Fund the Debt Repayment"
 COLDWAR_DDR_Q_repayment_desc:0 "Settle up to 3% of current GDP in outstanding principal from available cash. The confirmation shows the exact treasury and debt deductions. An unfunded repayment cannot create a new loan."
 COLDWAR_DDR_Q_retry_import:0 "Renew the Soviet Tank Order"
 COLDWAR_DDR_Q_retry_import_desc:0 "Request ninety tanks from Soviet reserves. Payment requires acceptance, sufficient funds and an available Soviet stockpile."
 COLDWAR_DDR_Q_retry_licence:0 "Renew the Soviet Tank Licence Request"
 COLDWAR_DDR_Q_retry_licence_desc:0 "Seek a production licence for an available Soviet design and the domestic assembly project. Failed design selection or missing construction capacity causes no charge."
 COLDWAR_DDR_Q.accept:0 "Accept the agreement."
 COLDWAR_DDR_Q.refuse:0 "Decline the request."
 COLDWAR_DDR_Q.cancel:0 "Leave the programme unfunded."
 COLDWAR_DDR_Q.repay:0 "Settle the principal."
 COLDWAR_DDR_Q.ack:0 "Acknowledged."
 COLDWAR_DDR_Q.1.t:0 "A German Tank Order"
 COLDWAR_DDR_Q.1.d:0 "The German Democratic Republic requests ninety tanks from our reserves under a paid procurement agreement."
 COLDWAR_DDR_Q.2.t:0 "A German Tank Assembly Proposal"
 COLDWAR_DDR_Q.2.d:0 "The German Democratic Republic seeks a licence for an available Soviet tank design and technical assistance for domestic assembly."
 COLDWAR_DDR_Q.3.t:0 "Soviet Tanks Delivered"
 COLDWAR_DDR_Q.3.d:0 "Ninety tanks have been transferred from Soviet reserves. The agreed payment has reached the Soviet treasury."
 COLDWAR_DDR_Q.4.t:0 "Tank Assembly Agreement Implemented"
 COLDWAR_DDR_Q.4.d:0 "The Soviet production licence is active and the two-factory assembly project has been delivered. The agreed payment is complete."
 COLDWAR_DDR_Q.5.t:0 "Tank Assembly Agreement Deferred"
 COLDWAR_DDR_Q.5.d:0 "An eligible Soviet design could not be licensed. No payment was taken and no factory was granted. The request can be renewed after the negotiation interval."
 COLDWAR_DDR_Q.6.t:0 "A Funded Debt Repayment"
 COLDWAR_DDR_Q.6.d:0 "Settle outstanding principal from the republic's available cash and restore confidence in its finances."
 COLDWAR_DDR_Q.7.t:0 "The Soviet Procurement Request Was Declined"
 COLDWAR_DDR_Q.7.d:0 "The agreement was not concluded. No payment was taken and no equipment, licence or assembly works were delivered. The request may be renewed after the negotiation interval."
'''
    install('common/scripted_effects/COLDWAR_DDR_1970_quality.txt', effects)
    install('common/scripted_triggers/COLDWAR_DDR_1970_quality.txt', triggers)
    install('events/COLDWAR_DDR_1970_quality.txt', events)
    install('common/ideas/COLDWAR_DDR_1970_quality.txt', ideas)
    install('common/decisions/COLDWAR_DDR_1970_quality.txt', decisions)
    install('common/decisions/categories/COLDWAR_DDR_1970_quality.txt', category)
    install('localisation/english/COLDWAR_DDR_1970_quality_l_english.yml', loc)


if __name__ == '__main__':
    build()
