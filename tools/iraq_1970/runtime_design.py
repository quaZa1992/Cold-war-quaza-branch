# IMPERIA CW — Cold War: iraq 1970 — runtime design.
"""Scenario initialization, observed campaign clocks and replaceable situations."""
import json
from pathlib import Path
from common import *

def generate(root=ROOT):
    from audit_design import load_design
    d=load_design()
    loc={};triggers=[];effects=[];ideas=[]
    def L(k,v,desc=None):
        loc[k]=v
        if desc is not None:loc[k+'_desc']=desc
    def E(k,v):effects.append(block(P+k,v))
    def T(k,v):triggers.append(block(P+k,v))
    T('campaign_active',block('hidden_trigger','tag = IRQ\noriginal_tag = IRQ\nis_dynamic_country = no\nexists = yes\nIMP_is_1970_scenario = yes'))
    T('northern_settlement_active','COLDWAR_IRQ_campaign_active = yes\nCOLDWAR_USA_gulf_settlement_respected = yes')
    for key,name in [('bakr','Ahmed Hassan al-Bakr'),('saddam','Saddam Hussein'),('aziz_muhammad','Aziz Muhammad')]:
        T('leader_'+key+'_in_office',f'has_country_leader = {{ name = "{name}" ruling_only = yes }}')
    sync=''
    for s in d['starting_spirits']:
        sid=s['id'];mods=s['modifiers']
        for key,val in mods.items():sync+=f'set_variable = {{ {sid}_{key} = {val:g} }}\n'
    # Each original burden component has one authoritative replacement value.
    north=P+'spirit_unsettled_north'
    sync+=block('if',block('limit','COLDWAR_IRQ_northern_settlement_active = yes')+f'set_variable = {{ {north}_stability_factor = -0.08 }}\n'+block('if',block('limit','NOT = { has_idea = COLDWAR_IRQ_autonomy_guarantee_cost }')+'add_ideas = COLDWAR_IRQ_autonomy_guarantee_cost'))
    sync+=block('else','remove_ideas = COLDWAR_IRQ_autonomy_guarantee_cost')
    sync+=block('if',block('limit','has_country_flag = COLDWAR_IRQ_federal_settlement\nCOLDWAR_IRQ_northern_settlement_active = yes')+f'set_variable = {{ {north}_stability_factor = -0.03 }}\nset_variable = {{ {north}_army_personnel_cost_multiplier_modifier = 0.04 }}\nset_variable = {{ {north}_supply_consumption_factor = 0.01 }}')
    patron=P+'spirit_patronage'
    sync+=block('if',block('limit',flag(P+'ministerial_audit_implemented'))+f'set_variable = {{ {patron}_bureaucracy_cost_multiplier_modifier = 0.07 }}')
    sync+=block('if',block('limit',flag(P+'professional_command_implemented'))+f'set_variable = {{ {patron}_army_org_factor = 0 }}')
    ipc=P+'spirit_ipc_oil_export_multiplier_modifier'
    sync+=block('if',block('limit',flag(P+'oil_state_company_implemented'))+f'set_variable = {{ {ipc} = -0.06 }}\n'+block('if',block('limit',flag(P+'oil_field_maintenance_implemented'))+f'set_variable = {{ {ipc} = 0 }}'))
    sync+=block('else_if',block('limit',flag(P+'oil_concession_delivery_implemented')+'\nCOLDWAR_IRQ_oil_concession_active = yes')+f'set_variable = {{ {ipc} = -0.09 }}')
    rural=P+'spirit_rural'
    sync+=block('if',block('limit','OR = { '+flag(P+'agri_cooperative_credit_implemented')+' '+flag(P+'agri_smallholder_credit_implemented')+' }')+f'set_variable = {{ {rural}_agricolture_productivity_modifier = -0.08 }}')
    sync+=block('if',block('limit',flag(P+'agri_extension_implemented'))+f'set_variable = {{ {rural}_agricolture_productivity_modifier = -0.04 }}')
    sync+=block('if',block('limit',flag(P+'agri_distribution_implemented'))+f'set_variable = {{ {rural}_consumer_goods_factor = 0.01 }}')
    sync+=block('if',block('limit',flag(P+'agri_reform_delivery_implemented'))+f'set_variable = {{ {rural}_agricolture_productivity_modifier = 0 }}\nset_variable = {{ {rural}_consumer_goods_factor = 0 }}')
    sync+='COLDWAR_IRQ_refresh_starting_spirit_cards = yes\nforce_update_dynamic_modifier = yes'
    E('reconcile_situations',block('if',block('limit','COLDWAR_IRQ_campaign_active = yes')+sync))
    for key,s in d['iran_war_ideas'].items():
        body=f'picture = {key}\nallowed = {{ tag = IRQ }}\nremoval_cost = -1\n'
        if s.get('cancel_peace'):body+=block('cancel','NOT = { has_war_with = PER }')
        body+=block('modifier','\n'.join(k+' = '+str(v) for k,v in s['modifier'].items()))
        if s.get('targeted_modifier'):body+=block('targeted_modifier','\n'.join(k+' = '+str(v) for k,v in s['targeted_modifier'].items()))
        ideas.append(block(key,body));L(key,s['label'],s['description'])
    init='COLDWAR_IRQ_seed_starting_spirits = yes\n'+block('if',block('limit','NOT = { has_country_flag = COLDWAR_IRQ_initialized }')+'''set_country_flag = COLDWAR_IRQ_initialized
if = { limit = { NOT = { has_variable = literacy_rate } }
 set_variable = { literacy_rate = 0.35 }
 set_temp_variable = { LR_change = 0 }
 update_literacy_rate = yes
EDU_learn_your_ABCs_with_dread = yes
}
COLDWAR_IRQ_record_incumbent = yes
''')
    init+='''if = { limit = { NOT = { is_in_array = { array = global.literacy_rate_nation value = THIS } } }
 add_to_array = { global.literacy_rate_nation = THIS }
}
if = { limit = { has_variable = literacy_rate NOT = { has_country_flag = education_mechanic } NOT = { has_country_flag = EDU_cleared_previously } }
 EDU_learn_your_ABCs_with_dread = yes
}
'''
    init+=block('if',block('limit','NOT = { has_focus_tree = COLDWAR_IRQ_1970_focus }')+'load_focus_tree = COLDWAR_IRQ_1970_focus')
    init+='COLDWAR_IRQ_repair_completed_focus_metadata = yes\nCOLDWAR_IRQ_migrate_audit_revision = yes\nCOLDWAR_IRQ_migrate_direct_rewards_v3 = yes\nCOLDWAR_IRQ_refresh_audit_upgrade_quotes = yes\nCOLDWAR_IRQ_refresh_direct_reward_quotes_v3 = yes\nCOLDWAR_IRQ_reconcile_situations = yes\nCOLDWAR_IRQ_reconcile_programmes = yes'
    E('initialize',block('if',block('limit','COLDWAR_IRQ_campaign_active = yes')+init))
    # Clocks refer to actual war/ownership, never a fixed historical calendar.
    daily='COLDWAR_IRQ_initialize = yes\nCOLDWAR_IRQ_political_tick = yes\nCOLDWAR_IRQ_decision_tick = yes\n'
    daily+='''set_temp_variable = { COLDWAR_IRQ_current_civilian_capacity = num_of_civilian_factories }
if = { limit = { NOT = { has_variable = COLDWAR_IRQ_civilian_capacity_peak } } set_variable = { COLDWAR_IRQ_civilian_capacity_peak = COLDWAR_IRQ_current_civilian_capacity } }
if = { limit = { check_variable = { var = COLDWAR_IRQ_current_civilian_capacity value = COLDWAR_IRQ_civilian_capacity_peak compare = greater_than } } set_variable = { COLDWAR_IRQ_civilian_capacity_peak = COLDWAR_IRQ_current_civilian_capacity } }
if = {
 limit = { has_war = yes }
 set_country_flag = COLDWAR_IRQ_war_participation
 if = { limit = { OR = { has_damaged_buildings = yes check_variable = { var = COLDWAR_IRQ_current_civilian_capacity value = COLDWAR_IRQ_civilian_capacity_peak compare = less_than } } } set_country_flag = COLDWAR_IRQ_reconstruction_need }
}
if = {
 limit = { has_war_with = PER }
 if = { limit = { NOT = { has_country_flag = COLDWAR_IRQ_iran_first_war_seen } }
  set_country_flag = COLDWAR_IRQ_iran_first_war_seen
  set_country_flag = { flag = COLDWAR_IRQ_iran_campaign_window_open days = 30 value = 1 }
 }
 if = { limit = { NOT = { has_country_flag = COLDWAR_IRQ_iran_current_war_start } } set_country_flag = COLDWAR_IRQ_iran_current_war_start }
 if = { limit = { has_country_flag = { flag = COLDWAR_IRQ_iran_current_war_start days > 179 } NOT = { has_idea = COLDWAR_IRQ_iran_attrition_bill } } add_ideas = COLDWAR_IRQ_iran_attrition_bill }
}
else = {
 clr_country_flag = COLDWAR_IRQ_iran_current_war_start
 clr_country_flag = COLDWAR_IRQ_iran_campaign_window_open
 remove_ideas = COLDWAR_IRQ_iran_attrition_bill
 remove_ideas = COLDWAR_IRQ_iran_opening_offensive
 remove_ideas = COLDWAR_IRQ_iran_sustained_offensive
 remove_ideas = COLDWAR_IRQ_iran_followup_offensive
}
if = { limit = { 399 = { is_owned_and_controlled_by = IRQ } }
 if = { limit = { NOT = { has_country_flag = COLDWAR_IRQ_khuzestan_hold_since } } set_country_flag = COLDWAR_IRQ_khuzestan_hold_since }
}
else = { clr_country_flag = COLDWAR_IRQ_khuzestan_hold_since }
COLDWAR_IRQ_reconcile_situations = yes
COLDWAR_IRQ_reconcile_programmes = yes
'''
    E('daily',block('if',block('limit','COLDWAR_IRQ_campaign_active = yes')+daily))
    hooks=block('on_startup',block('effect','IRQ = { COLDWAR_IRQ_initialize = yes }'))
    hooks+=block('on_daily',block('effect','COLDWAR_IRQ_daily = yes'))
    for hook in ['on_government_change','on_ruling_party_change']:
        hooks+=block(hook,block('effect','COLDWAR_IRQ_reconcile_programmes = yes\nCOLDWAR_IRQ_reconcile_situations = yes'))
    return {
     'common/scripted_triggers/COLDWAR_IRQ_1970_triggers.txt':'\n'.join(triggers),
     'common/scripted_effects/COLDWAR_IRQ_1970_situations.txt':'\n'.join(effects),
     'common/ideas/COLDWAR_IRQ_1970_ideas.txt':block('ideas',block('country','\n'.join(ideas))),
     'common/on_actions/COLDWAR_IRQ_1970_on_actions.txt':block('on_actions',hooks),
     'localisation/english/COLDWAR_IRQ_1970_situations_l_english.yml':'l_english:\n# IMPERIA CW — Cold War: iraq 1970 English localisation.\n'+'\n'.join(locline(k,v) for k,v in loc.items())+'\n',
    }
