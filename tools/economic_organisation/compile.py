# IMPERIA COLD WAR — Economic organisation compiler and bounded integration
import ast
import argparse
import hashlib
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw
from catalogue import ROOT, HERE, MARKER, TIERS, LABELS, DESCRIPTIONS, REFORMS, STARTS, SALE_GDP_PER_POINT

OUT = ROOT / 'docs/design/economic_organisation'
OUT.mkdir(parents=True, exist_ok=True)
GENERATED = []
# IMPERIA COLD WAR — Economic reform decision presentation
DECISION_ICONS = {
    'ownership': 'GFX_decision_generic_factory',
    'targets': 'GFX_decision_eng_trade_unions_support',
    'autonomy': 'GFX_decision_attract_foreign_investor',
    'privatisation': 'GFX_decision_gre_investment_decisions',
    'capital': 'GFX_decision_international_bankers',
}

def write(rel, source):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source.rstrip()+'\n', encoding='utf-8-sig' if rel.endswith('.yml') else 'utf-8')
    GENERATED.append(rel)

def number(value):
    return f'{value:.5f}'.rstrip('0').rstrip('.') if isinstance(value, float) else str(value)

def idea(slug): return 'icw_econ_'+slug

# IMPERIA COLD WAR — Native percentage notation for economic modifiers
def tier_effects(mods):
    lines=[]
    for key,value in mods.items():
        label,positive,percentage=LABELS[key]
        good=(value>0)==positive
        printed=f'{value:+.2f}' if percentage=='daily' else f'{value*100:+.0f}%' if percentage else f'{value:+.0f}'
        lines.append(f'{label}: §{"G" if good else "R"}{printed}§!')
    return '\\n'.join(lines)

def preview(delta):
    result=[]
    for index,(slug,name,lo,hi,mods) in enumerate(TIERS):
        condition=f'check_variable = {{ icw_econ_position < {hi-delta} }}' if index<6 else 'always = yes'
        swaps=[]
        for old,*_ in TIERS:
            if old!=slug:
                swaps.append(f'if = {{ limit = {{ hidden_trigger = {{ has_idea = {idea(old)} }} }} swap_ideas = {{ remove_idea = {idea(old)} add_idea = {idea(slug)} }} }}')
        result.append(f'{"if" if index==0 else "else_if"} = {{ limit = {{ hidden_trigger = {{ {condition} }} }} '+ ' '.join(swaps)+' }')
    return '\n'.join(result)

def delta_effects(current, target):
    return tier_effects({key:round(target.get(key,0)-current.get(key,0),5) for key in LABELS
                         if abs(target.get(key,0)-current.get(key,0))>.000001})


def main(scripts_only=False):
    # One named national spirit per country. Existing country spirits and native BoPs are untouched.
    ideas=[MARKER+' policy spirits', 'ideas = { country = {']
    for slug,name,lo,hi,mods in TIERS:
        ideas.append(f'{idea(slug)} = {{ picture = {"sov_planned_economy_idea" if lo< -15 else "market_dynamics"} allowed = {{ always = yes }} allowed_civil_war = {{ always = yes }} removal_cost = -1 modifier = {{')
        ideas.extend(f'{key} = {number(value)}' for key,value in mods.items())
        ideas.append('} }')
    ideas.append('} }')
    write('common/ideas/ICW_economic_organisation.txt', '\n'.join(ideas))

    triggers=[MARKER+' shared reform requirements', 'icw_econ_execution_ready = { hidden_trigger = { has_country_flag = icw_econ_initialized } custom_trigger_tooltip = { tooltip = icw_econ_no_active_reform_tt NOT = { has_country_flag = icw_econ_reform_active } } check_variable = { icw_econ_cooldown_days < 1 } }',
        'icw_econ_ready = { icw_econ_execution_ready = yes custom_trigger_tooltip = { tooltip = icw_econ_no_pending_request_tt NOT = { has_country_flag = icw_econ_approval_pending } } }',
        '''icw_econ_request_valid = { exists = yes has_country_flag = icw_econ_approval_pending is_subject = yes NOT = { has_country_flag = icw_econ_reform_active } check_variable = { icw_econ_requested_country = THIS.id } check_variable = { icw_econ_position = icw_econ_requested_origin } overlord = { exists = yes check_variable = { PREV.icw_econ_requested_overlord = THIS.id } } }''']
    for slug,name,delta,cost,description in REFORMS:
        bound=f'NOT = {{ check_variable = {{ icw_econ_position < {-100-delta} }} }}' if delta<0 else f'NOT = {{ check_variable = {{ icw_econ_position > {100-delta} }} }}'
        gate=(f' OR = {{ check_variable = {{ icw_econ_position < {70-delta} }} NOT = {{ check_variable = {{ globalism_value < 80 }} }} }}' if delta>0 else '')
        triggers.append(f'icw_econ_conditions_{slug} = {{ icw_econ_execution_ready = yes NOT = {{ has_political_power < {cost} }} {bound}'+gate+(' NOT = { check_variable = { globalism_value < 80 } }' if slug=='capital' else '')+' }')
        triggers.append(f'icw_econ_can_{slug} = {{ icw_econ_ready = yes icw_econ_conditions_{slug} = yes }}')
    write('common/scripted_triggers/ICW_economic_organisation.txt', '\n'.join(triggers))

    effects=[MARKER+' country state and transactions', '''icw_econ_sale_initialize = {
 if = { limit = { NOT = { has_country_flag = icw_econ_sale_initialized } }
  set_country_flag = icw_econ_sale_initialized
  set_variable = { icw_econ_market_high_water = icw_econ_position }
 }
}
icw_econ_update_preview = {
 set_temp_variable = { icw_econ_sale_reference = icw_econ_position }
 if = { limit = { has_country_flag = icw_econ_sale_initialized }
  set_temp_variable = { icw_econ_sale_reference = icw_econ_market_high_water }
 }
''']
    effects.append(f'''set_variable = {{ icw_econ_sale_quote = {{ value = icw_econ_position add = 10 clamp = {{ min = -100 max = 100 }} subtract = icw_econ_sale_reference clamp = {{ min = 0 max = 10 }} multiply = gdp_total multiply = {number(SALE_GDP_PER_POINT)} clamp = {{ min = 0 max = 1000000000 }} }} }}''')
    effects.extend(f'set_variable = {{ icw_econ_target_{slug} = {{ value = icw_econ_position add = {delta} clamp = {{ min = -100 max = 100 }} }} }}' for slug,name,delta,cost,description in REFORMS)
    effects.append('''}
icw_econ_touch = { add_to_variable = { icw_econ_gui_dirty = 1 } icw_econ_update_preview = yes }
icw_econ_update_marker = {
 set_variable = { icw_econ_needle_x = { value = icw_econ_position add = 100 multiply = 2.7 add = 59 round = yes } }
 icw_econ_touch = yes
}
icw_econ_refresh_tier = {
 clamp_variable = { var = icw_econ_position min = -100 max = 100 }
''')
    all_ideas=' '.join(idea(t[0]) for t in TIERS)
    for index,(slug,name,lo,hi,mods) in enumerate(TIERS):
        condition=f'check_variable = {{ icw_econ_position < {hi} }}' if index<6 else 'always = yes'
        effects.append(f'{"if" if index==0 else "else_if"} = {{ limit = {{ {condition} }} set_variable = {{ icw_econ_tier = {index+1} }} if = {{ limit = {{ NOT = {{ has_idea = {idea(slug)} }} }} remove_ideas = {{ {all_ideas} }} add_ideas = {idea(slug)} }} }}')
    effects.append('icw_econ_update_marker = yes\n}')
    effects.append('icw_econ_initialize = { if = { limit = { NOT = { has_country_flag = icw_econ_initialized } } set_country_flag = icw_econ_initialized set_variable = { icw_econ_position = 0 } set_variable = { icw_econ_selected_reform = 3 } set_variable = { icw_econ_cooldown_days = 0 } set_variable = { icw_econ_days_remaining = 0 }')
    effects.extend(f'set_variable = {{ icw_econ_button_{i} = {2 if i==3 else 1} }}' for i in range(1,6))
    effects.append('if = { limit = { date < 1992.1.1 }')
    for position,tags in STARTS.items():
        effects.append(f'if = {{ limit = {{ OR = {{ {" ".join("original_tag = "+tag for tag in tags)} }} }} set_variable = {{ icw_econ_position = {position} }} }}')
    effects.append('if = { limit = { original_tag = CHI } set_variable = { icw_econ_position = -80 } if = { limit = { date > 1978.12.31 } set_variable = { icw_econ_position = -35 } } }\n}')
    effects.append('icw_econ_refresh_tier = yes\nset_variable = { globalism_value_eq = modifier@globalism_equilibrium }\nclamp_variable = { var = globalism_value_eq min = 0 max = 100 }\n}\nicw_econ_sale_initialize = yes\nicw_econ_update_preview = yes\nset_variable = { icw_econ_needle_x = { value = icw_econ_position add = 100 multiply = 2.7 add = 59 round = yes } }\n}')
    effects.append('''icw_econ_clear_request = { clr_country_flag = icw_econ_approval_pending clear_variable = icw_econ_requested_reform clear_variable = icw_econ_requested_origin clear_variable = icw_econ_requested_overlord clear_variable = icw_econ_requested_country icw_econ_touch = yes }
''')
    for index,(slug,name,delta,cost,description) in enumerate(REFORMS,1):
        frames=' '.join(f'set_variable = {{ icw_econ_button_{j} = {2 if j==index else 1} }}' for j in range(1,6))
        sale='icw_econ_update_preview = yes set_variable = { icw_econ_pending_sale = icw_econ_sale_quote }' if slug=='privatisation' else 'clear_variable = icw_econ_pending_sale'
        effects.append(f'''icw_econ_apply_{slug} = {{ if = {{ limit = {{ icw_econ_can_{slug} = yes OR = {{ is_subject = no has_country_flag = icw_econ_overlord_authorised }} }} add_political_power = -{cost} hidden_effect = {{ icw_econ_sale_initialize = yes {sale} clr_country_flag = icw_econ_overlord_authorised set_country_flag = icw_econ_reform_active set_variable = {{ icw_econ_pending_position = {{ value = icw_econ_position add = {delta} }} }} set_variable = {{ icw_econ_days_remaining = 90 }} set_variable = {{ icw_econ_cooldown_days = 180 }} set_variable = {{ icw_econ_selected_reform = {index} }} {frames} icw_econ_touch = yes }} }} }}
icw_econ_start_{slug} = {{ if = {{ limit = {{ icw_econ_can_{slug} = yes }} if = {{ limit = {{ is_subject = yes }} set_country_flag = icw_econ_approval_pending set_variable = {{ icw_econ_requested_reform = {index} }} set_variable = {{ icw_econ_requested_origin = icw_econ_position }} set_variable = {{ icw_econ_requested_country = THIS.id }} save_event_target_as = icw_econ_applicant overlord = {{ set_variable = {{ PREV.icw_econ_requested_overlord = THIS.id }} country_event = {{ id = ICW_ECON_APPROVAL.{index} days = 1 }} }} icw_econ_touch = yes }} else = {{ icw_econ_apply_{slug} = yes }} }} }}
icw_econ_approve_{slug} = {{ if = {{ limit = {{ icw_econ_request_valid = yes is_subject_of = ROOT check_variable = {{ icw_econ_requested_overlord = ROOT.id }} check_variable = {{ icw_econ_requested_reform = {index} }} icw_econ_conditions_{slug} = yes }} icw_econ_clear_request = yes set_country_flag = icw_econ_overlord_authorised icw_econ_apply_{slug} = yes clr_country_flag = icw_econ_overlord_authorised }} }}
icw_econ_decline_{slug} = {{ if = {{ limit = {{ has_country_flag = icw_econ_approval_pending check_variable = {{ icw_econ_requested_overlord = ROOT.id }} check_variable = {{ icw_econ_requested_reform = {index} }} }} icw_econ_clear_request = yes }} }}''')
        sale_preview='custom_effect_tooltip = icw_econ_sale_preview_tt' if slug=='privatisation' else ''
        header=f'icw_econ_preview_{slug} = {{ add_political_power = -{cost} custom_effect_tooltip = icw_econ_move_{slug}_tt {sale_preview}'.rstrip()
        effects.append(header+f'\n{preview(delta)}\n}}')
    effects.append('''icw_econ_complete_reform = {
 if = { limit = { has_country_flag = icw_econ_reform_active }
  clr_country_flag = icw_econ_reform_active
  set_variable = { icw_econ_position = icw_econ_pending_position }
  clear_variable = icw_econ_pending_position
  set_variable = { icw_econ_days_remaining = 0 }
  icw_econ_sale_initialize = yes
  if = { limit = { check_variable = { icw_econ_pending_sale > 0 } }
   set_temp_variable = { treasury_change = icw_econ_pending_sale }
   modify_treasury_effect = yes
  }
  clear_variable = icw_econ_pending_sale
  if = { limit = { check_variable = { icw_econ_position > icw_econ_market_high_water } }
   set_variable = { icw_econ_market_high_water = icw_econ_position }
  }
  icw_econ_refresh_tier = yes
  set_variable = { globalism_value_eq = modifier@globalism_equilibrium }
  clamp_variable = { var = globalism_value_eq min = 0 max = 100 }
  if = { limit = { has_dynamic_modifier = { modifier = imp_globalism_modifier } } imp_eco_globalism_modifier = yes }
  if = { limit = { IMP_is_1970_scenario = yes } mdcw_cw_update_world_market = yes }
  ingame_update_setup = yes
 }
}
icw_econ_daily = {
 if = { limit = { has_country_flag = icw_econ_initialized }
  if = { limit = { is_ai = no } icw_econ_update_preview = yes }
  if = { limit = { has_country_flag = icw_econ_approval_pending NOT = { icw_econ_request_valid = yes } } icw_econ_clear_request = yes }
  if = { limit = { check_variable = { icw_econ_cooldown_days > 0 } } subtract_from_variable = { icw_econ_cooldown_days = 1 } icw_econ_touch = yes }
  if = { limit = { has_country_flag = icw_econ_reform_active }
   subtract_from_variable = { icw_econ_days_remaining = 1 }
   if = { limit = { check_variable = { icw_econ_days_remaining < 1 } } icw_econ_complete_reform = yes }
   icw_econ_touch = yes
  }
 }
}
''')
    write('common/scripted_effects/ICW_economic_organisation.txt', '\n'.join(effects))
    events=[MARKER+' subject reform approval events', 'add_namespace = ICW_ECON_APPROVAL']
    for index,(slug,name,delta,cost,description) in enumerate(REFORMS,1):
        valid=f'icw_econ_request_valid = yes is_subject_of = ROOT check_variable = {{ icw_econ_requested_overlord = ROOT.id }} check_variable = {{ icw_econ_requested_reform = {index} }}'
        events.append(f'''country_event = {{ id = ICW_ECON_APPROVAL.{index} title = icw_econ_approval_{slug}_title desc = icw_econ_approval_{slug}_desc is_triggered_only = yes
 trigger = {{ event_target:icw_econ_applicant = {{ {valid} }} }}
 option = {{ name = icw_econ_approve_option trigger = {{ event_target:icw_econ_applicant = {{ {valid} icw_econ_conditions_{slug} = yes }} }} ai_chance = {{ base = 100 }} event_target:icw_econ_applicant = {{ effect_tooltip = {{ icw_econ_preview_{slug} = yes }} hidden_effect = {{ icw_econ_approve_{slug} = yes }} }} }}
 option = {{ name = icw_econ_decline_option ai_chance = {{ base = 0 }} hidden_effect = {{ event_target:icw_econ_applicant = {{ icw_econ_decline_{slug} = yes }} }} }}
}}''')
    write('events/ICW_economic_organisation.txt','\n'.join(events))
    write('common/on_actions/zzzzzzzz_ICW_economic_organisation.txt', MARKER+''' startup and saved reform clocks
on_actions = {
 on_startup = { effect = { every_country = { icw_econ_initialize = yes } } }
 on_daily = { effect = { icw_econ_daily = yes } }
 on_weekly = { effect = { if = { limit = { OR = { NOT = { has_country_flag = icw_econ_initialized } NOT = { has_country_flag = icw_econ_sale_initialized } } } icw_econ_initialize = yes } } }
}
''')

    # IMPERIA COLD WAR — Native economic reform decisions
    # Native decisions and the GUI both call the guarded payment transaction.
    write('common/decisions/categories/ICW_economic_organisation.txt', MARKER+''' decision category
icw_econ_category = { icon = GFX_decision_economy allowed = { always = yes } visible = { has_country_flag = icw_econ_initialized } }
''')
    decisions=[MARKER+' reform decisions', 'icw_econ_category = {']
    for slug,name,delta,cost,description in REFORMS:
        decisions.append(f'icw_econ_decision_{slug} = {{ icon = {DECISION_ICONS[slug]} cost = 0 fire_only_once = no custom_cost_trigger = {{ NOT = {{ has_political_power < {cost} }} }} custom_cost_text = icw_econ_cost_{cost} available = {{ icw_econ_can_{slug} = yes }} complete_effect = {{ effect_tooltip = {{ icw_econ_preview_{slug} = yes }} hidden_effect = {{ icw_econ_start_{slug} = yes }} }} ai_will_do = {{ base = 0 }} }}')
    decisions.append('}')
    write('common/decisions/ICW_economic_organisation.txt', '\n'.join(decisions))

    # IMPERIA COLD WAR — Economic organisation English localisation
    # English names, descriptions, native effect rows and signed previews share the same catalogue.
    loc={
        'icw_econ_title':'Economic Organisation', 'icw_econ_axis_planning':'State Planning', 'icw_econ_market':'Market Economy',
        'icw_econ_open':'Economic Reforms', 'icw_econ_close':'Close', 'icw_econ_enact':'Enact Reform', 'icw_econ_current_policy':'Current Policy',
        'icw_econ_position':'Economic Organisation', 'icw_econ_cooldown_days':'Economic Reform Cooldown',
        'icw_econ_category':'Economic Organisation',
        'icw_econ_category_desc':'Current policy: §Y[icw_econ_current_name]§!\\n[icw_econ_status]\\n\\nImplementation: §Y90 days§!  |  Reform interval: §Y180 days§!',
        'icw_econ_status_ready':'Institutional reforms are available.',
        'icw_econ_status_active':'Reform in progress: §Y[?icw_econ_days_remaining|0] days§!',
        'icw_econ_status_cooldown':'Next reform available in §Y[?icw_econ_cooldown_days|0] days§!',
        'icw_econ_panel_tooltip':'§Y[icw_econ_current_name]§!\\n\\n[icw_econ_current_modifiers]',
        'icw_econ_reform_active':'Institutional reform in progress',
        'icw_econ_no_active_reform_tt':'No institutional reform is in progress.',
        'icw_econ_no_pending_request_tt':'No economic reform proposal is awaiting overlord approval.',
        'icw_econ_status_approval':'Awaiting overlord approval.',
        'icw_econ_request_approval':'Request Approval',
        'icw_econ_approve_option':'Authorise the reform.',
        'icw_econ_decline_option':'Decline the proposal.',
        'icw_econ_changes_heading':'Current modifiers',
        'icw_econ_current_position':'Current position: §Y[?icw_econ_position|+0]§!\\n[icw_econ_next_threshold]',
        'icw_econ_no_modifier_change':'No modifier changes at this position.',
        'icw_econ_sale_preview_tt':'Treasury after 90 days: $$[?icw_econ_sale_quote|+5] Billion',
        'icw_econ_selected_name':'After 90 days:\\n[icw_econ_selected_target_name]',
    }
    # The native decision list appends _blocked and _tooltip to custom_cost_text.
    for cost in sorted({r[3] for r in REFORMS}):
        loc[f'icw_econ_cost_{cost}']=f'£pol_power §Y{cost}§!'
        loc[f'icw_econ_cost_{cost}_blocked']=f'£pol_power §R{cost}§!'
        loc[f'icw_econ_cost_{cost}_tooltip']=f'Political Power: §Y{cost}§!'
    for slug,name,lo,hi,mods in TIERS:
        loc[idea(slug)]=name;loc[idea(slug)+'_desc']=DESCRIPTIONS[slug]
        loc[f'icw_econ_effects_{slug}']=tier_effects(mods) or ''
        loc[f'icw_econ_hover_{slug}']=f'§Y{name}§!'+('\\n\\n'+tier_effects(mods) if mods else '')
    for slug,name,delta,cost,description in REFORMS:
        loc[f'icw_econ_decision_{slug}']=name
        movement=f'{"State Planning" if delta<0 else "Market Economy"}: §Y+{abs(delta)}§!'
        sale_line='\\nTreasury: $$[?icw_econ_sale_quote|+5] Billion' if slug=='privatisation' else ''
        loc[f'icw_econ_summary_{slug}']=movement+f' (to [?icw_econ_target_{slug}|+0])'+sale_line
        loc[f'icw_econ_result_{slug}']='[icw_econ_delta_'+slug+']'
        sale_desc=' Proceeds are limited to newly privatised holdings; reversing an earlier reform does not restore them.' if slug=='privatisation' else ''
        loc[f'icw_econ_decision_{slug}_desc']=description+sale_desc+f'\\n\\n{movement}\\nPolitical Power: §R-{cost}§!\\nImplementation: §Y90 days§!\\nReform interval: §Y180 days§!\\n\\nAfter 90 days: §Y[icw_econ_target_name_{slug}]§!{sale_line}\\n[icw_econ_delta_{slug}]\\n\\nSubject governments require overlord approval.'
        loc[f'icw_econ_approval_{slug}_title']='Economic Reform: '+name
        loc[f'icw_econ_approval_{slug}_desc']='The government of [event_target:icw_econ_applicant.GetName] requests permission to '+name.lower()+'. Approval authorises a 90-day institutional reform, with its political cost paid by the requesting government.'
        loc[f'icw_econ_row_{slug}']=f'{name}   |   {cost} £pol_power   |   90 days'
        loc[f'icw_econ_move_{slug}_tt']=movement
    for current in TIERS:
        for target in TIERS:
            loc[f'icw_econ_delta_{current[0]}_{target[0]}']=delta_effects(current[4],target[4]) or loc['icw_econ_no_modifier_change']
    for index,(slug,name,lo,hi,mods) in enumerate(TIERS):
        loc[f'icw_econ_threshold_{slug}']=f'Next market tier: §Y+{hi}§!' if hi>0 and index<6 else f'Next market tier: §Y{hi}§!' if index<6 else 'Market limit: §Y+100§!'
    localisation=[MARKER+' policy names and status']
    for name,suffix in [('icw_econ_current_name',''),('icw_econ_current_modifiers','effects')]:
        localisation.append(f'defined_text = {{ name = {name}')
        for index,(slug,*_) in enumerate(TIERS,1):localisation.append(f'text = {{ trigger = {{ check_variable = {{ icw_econ_tier = {index} }} }} localization_key = {idea(slug) if not suffix else "icw_econ_effects_"+slug} }}')
        localisation.append('}')
    localisation.append('defined_text = { name = icw_econ_status text = { trigger = { has_country_flag = icw_econ_approval_pending } localization_key = icw_econ_status_approval } text = { trigger = { has_country_flag = icw_econ_reform_active } localization_key = icw_econ_status_active } text = { trigger = { check_variable = { icw_econ_cooldown_days > 0 } } localization_key = icw_econ_status_cooldown } text = { localization_key = icw_econ_status_ready } }')
    localisation.append('defined_text = { name = icw_econ_enact_label text = { trigger = { is_subject = yes } localization_key = icw_econ_request_approval } text = { localization_key = icw_econ_enact } }')
    for slug,name,delta,cost,description in REFORMS:
        localisation.append(f'defined_text = {{ name = icw_econ_target_name_{slug}')
        for index,(target,title,lo,hi,mods) in enumerate(TIERS):
            condition=f'check_variable = {{ icw_econ_position < {hi-delta} }}' if index<6 else 'always = yes'
            localisation.append(f'text = {{ trigger = {{ {condition} }} localization_key = {idea(target)} }}')
        localisation.append('}')
        localisation.append(f'defined_text = {{ name = icw_econ_delta_{slug}')
        for current_index,current in enumerate(TIERS,1):
            for target_index,target in enumerate(TIERS):
                low=-10000 if target_index==0 else target[2]-delta
                high=10000 if target_index==6 else target[3]-delta
                if max(current[2],low)>=min(current[3],high):continue
                condition=f'check_variable = {{ icw_econ_tier = {current_index} }} NOT = {{ check_variable = {{ icw_econ_position < {low} }} }} check_variable = {{ icw_econ_position < {high} }}'
                localisation.append(f'text = {{ trigger = {{ {condition} }} localization_key = icw_econ_delta_{current[0]}_{target[0]} }}')
        localisation.append('}')
    for function,template in [('icw_econ_selected_target_name','icw_econ_name_'),('icw_econ_selected_summary','icw_econ_summary_'),('icw_econ_selected_changes','icw_econ_result_')]:
        localisation.append(f'defined_text = {{ name = {function}')
        for index,(slug,*_) in enumerate(REFORMS,1):
            if template=='icw_econ_name_':loc_key='icw_econ_selected_target_'+slug
            else:loc_key=template+slug
            localisation.append(f'text = {{ trigger = {{ check_variable = {{ icw_econ_selected_reform = {index} }} }} localization_key = {loc_key} }}')
        localisation.append('}')
    localisation.append('defined_text = { name = icw_econ_next_threshold '+' '.join(f'text = {{ trigger = {{ check_variable = {{ icw_econ_tier = {i} }} }} localization_key = icw_econ_threshold_{tier[0]} }}' for i,tier in enumerate(TIERS,1))+' }')
    # Add the final selected-name wrappers without $-substitutions in runtime text.
    for slug,*_ in REFORMS:loc[f'icw_econ_selected_target_{slug}']='[icw_econ_target_name_'+slug+']'
    write('localisation/english/ICW_economic_organisation_l_english.yml', 'l_english:\n'+MARKER+' English localisation\n'+'\n'.join(' '+key+': "'+value.replace('"','\\"')+'"' for key,value in loc.items()))
    write('common/scripted_localisation/ICW_economic_organisation.txt', '\n'.join(localisation))

    if scripts_only:
        assert (ROOT/'interface/ICW_economic_organisation.gfx').exists()
        GENERATED.append('interface/ICW_economic_organisation.gfx')
    else:assets()
    gui()
    integrate()
    manifest={'project':'IMPERIA COLD WAR','generated':GENERATED,'tier_count':7,'reform_days':90,'start_interval_days':180,'ai_reforms':'Disabled; AI retains its initialized institutions.','profiles':STARTS,'fallback_position':0,'files_sha256':{rel:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() for rel in GENERATED}}
    (OUT/'implementation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'generated':len(GENERATED),'tiers':len(TIERS),'reforms':len(REFORMS)}))

def assets():
    game=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
    folder=ROOT/'gfx/interface/ICW_economic_organisation';folder.mkdir(parents=True,exist_ok=True)
    bar=Image.new('RGBA',(360,16))
    for side,name in [(0,'orange'),(180,'blue')]:
        src=Image.open(game/f'gfx/interface/bop/bop_bar_{name}_dark.dds').convert('RGBA')
        bar.paste(src.resize((180,16)),(side,0))
    bar.save(folder/'bar.dds')
    for width,height in [(160,28),(640,38)]:
        strip=Image.new('RGBA',(width*3,height))
        for frame,(base,edge) in enumerate([('#303b32','#68715b'),('#46513d','#b6ab7d'),('#202d23','#9b936c')]):
            tile=Image.new('RGBA',(width,height),base);draw=ImageDraw.Draw(tile);draw.rectangle((0,0,width-1,height-1),outline=edge);draw.line((1,1,width-2,1),fill='#899078');strip.paste(tile,(width*frame,0))
        strip.save(folder/f'button_{width}_{height}.dds')
    for width in [68,81]:Image.new('RGBA',(width,36)).save(folder/f'hover_{width}.dds')
    for direction,color in [('left','#c78852'),('right','#6dabb6')]:
        arrow=Image.new('RGBA',(28,20));draw=ImageDraw.Draw(arrow)
        points=[(2,10),(12,1),(12,6),(25,6),(25,14),(12,14),(12,19)]
        if direction=='right':points=[(27-x,y) for x,y in points]
        draw.polygon(points,fill=color,outline='#e1d9ba');arrow.save(folder/f'arrow_{direction}.dds')
    gfx=[MARKER+' sprites','spriteTypes = {','spriteType = { name = GFX_icw_econ_bar texturefile = "gfx/interface/ICW_economic_organisation/bar.dds" }']
    for width,height in [(160,28),(640,38)]:gfx.append(f'spriteType = {{ name = GFX_icw_econ_button_{width} texturefile = "gfx/interface/ICW_economic_organisation/button_{width}_{height}.dds" noOfFrames = 3 }}')
    for width in [68,81]:gfx.append(f'spriteType = {{ name = GFX_icw_econ_hover_{width} texturefile = "gfx/interface/ICW_economic_organisation/hover_{width}.dds" }}')
    for direction in ['left','right']:gfx.append(f'spriteType = {{ name = GFX_icw_econ_arrow_{direction} texturefile = "gfx/interface/ICW_economic_organisation/arrow_{direction}.dds" }}')
    gfx.extend(['spriteType = { name = GFX_icw_econ_frame texturefile = "gfx/interface/bop/bop_bar_frame.dds" }','spriteType = { name = GFX_icw_econ_needle texturefile = "gfx/interface/bop/bop_needle.dds" }','spriteType = { name = GFX_icw_econ_splitter texturefile = "gfx/interface/bop/bop_splitter.dds" }','}'])
    write('interface/ICW_economic_organisation.gfx','\n'.join(gfx))
    notice='IMPERIA COLD WAR — Economic organisation interface asset provenance\n\nThe bar combines the original Hearts of Iron IV orange and blue balance-of-power textures, resized to half-width. Source: installed Hearts of Iron IV gfx/interface/bop/bop_bar_orange_dark.dds and bop_bar_blue_dark.dds. Credit: Paradox Interactive; individual artists unknown. Separate redistribution permission is unknown. Frame, needle and splitter registrations reuse installed original textures without copying or editing their binaries. Upstream rights remain separate.\n\nThe rectangular controls and transparent hover images are procedural interface assets authored by OpenAI Codex for Enes. No third-party source pixels are used in those controls. No project-wide licence is established by this notice.\n'
    notice+='\nThe directional arrows are original procedural polygons authored by OpenAI Codex for Enes. The native position needle is rendered at 150% scale in both policy bars; its texture is not edited.\n'
    (folder/'NOTICE.md').write_text(notice,encoding='utf-8')

def textbox(name,text,x,y,w,h=22,font='hoi_16mbs'):
    return f'instantTextboxType = {{ name = "{name}" position = {{ x={x} y={y} }} font = "{font}" text = "{text}" maxWidth = {w} maxHeight = {h} format = left fixedsize = yes alwaystransparent = yes }}'

def bar(prefix,y):
    body=[f'iconType = {{ name = "{prefix}_bar" position = {{ x=74 y={y+6} }} spriteType = GFX_icw_econ_bar scale = 1.5 alwaystransparent = yes }}',f'iconType = {{ name = "{prefix}_frame" position = {{ x=68 y={y} }} spriteType = GFX_icw_econ_frame scale = 1.5 alwaystransparent = yes }}']
    for index,bound in enumerate([-70,-40,-15,15,40,70]):body.append(f'iconType = {{ name = "{prefix}_split_{index}" position = {{ x={round(74+(bound+100)*2.7)-6} y={y-3} }} spriteType = GFX_icw_econ_splitter scale = 1.5 alwaystransparent = yes }}')
    body.append(f'iconType = {{ name = "{prefix}_needle" position = {{ x=329 y={y-6} }} spriteType = GFX_icw_econ_needle scale = 1.5 alwaystransparent = yes }}')
    for slug,name,lo,hi,mods in TIERS:
        width=81 if hi-lo>=30 else 68
        body.append(f'iconType = {{ name = "{prefix}_hover_{slug}" position = {{ x={round(74+(lo+100)*2.7)} y={y} }} spriteType = GFX_icw_econ_hover_{width} pdx_tooltip = icw_econ_hover_{slug} }}')
    return '\n'.join(body)

def gui():
    compact=[MARKER+' compact economy bar and reform dialog','guiTypes = {','containerWindowType = { name = "icw_econ_compact_window" position = { x=0 y=0 } size = { width=680 height=126 } background = { name = "background" quadTextureSprite = GFX_MD_tiled_window1 }',textbox('icw_econ_left','icw_econ_axis_planning',10,7,250),textbox('icw_econ_right','icw_econ_market',500,7,170),bar('icw_econ_compact',29),textbox('icw_econ_name','[icw_econ_current_name]',12,73,500),textbox('icw_econ_value','[?icw_econ_position|+0]',600,73,65),textbox('icw_econ_status','[icw_econ_status]',12,101,470), 'buttonType = { name = "icw_econ_open" position = { x=508 y=94 } quadTextureSprite = GFX_icw_econ_button_160 buttonFont = hoi_16mbs text = icw_econ_open pdx_tooltip = icw_econ_panel_tooltip }','}',
        'containerWindowType = { name = "icw_econ_reforms_window" position = { x=0 y=0 } size = { width=680 height=710 } background = { name = "background" quadTextureSprite = GFX_MD_tiled_window1 }',textbox('icw_econ_header','icw_econ_title',15,10,560,30,'hoi_24header'),'buttonType = { name = "icw_econ_close" position = { x=620 y=7 } quadTextureSprite = GFX_closebutton shortcut = ESCAPE pdx_tooltip = CLOSE }',textbox('icw_econ_policy_name','[icw_econ_current_name]',16,48,640,26,'hoi_20b'),bar('icw_econ_dialog',77),textbox('icw_econ_current_heading','icw_econ_changes_heading',18,122,310),textbox('icw_econ_modifiers','[icw_econ_current_modifiers]',18,145,310,224),textbox('icw_econ_current_progress','icw_econ_current_position',18,382,310,36),textbox('icw_econ_preview_heading','icw_econ_selected_name',348,122,312,36),textbox('icw_econ_preview_summary','[icw_econ_selected_summary]',348,160,312,40),textbox('icw_econ_preview_changes','[icw_econ_selected_changes]',348,202,312,224)]
    for index,(slug,name,delta,cost,desc) in enumerate(REFORMS,1):
        y=437+(index-1)*43
        compact.append(f'buttonType = {{ name = "icw_econ_select_{slug}" position = {{ x=20 y={y} }} quadTextureSprite = GFX_icw_econ_button_640 buttonFont = hoi_16mbs text = icw_econ_row_{slug} pdx_tooltip = icw_econ_decision_{slug}_desc }}')
        compact.append(f'iconType = {{ name = "icw_econ_direction_{slug}" position = {{ x={32 if delta<0 else 620} y={y+9} }} spriteType = GFX_icw_econ_arrow_{"left" if delta<0 else "right"} alwaystransparent = yes }}')
    compact.extend([textbox('icw_econ_dialog_status','[icw_econ_status]',20,664,450,36),'buttonType = { name = "icw_econ_enact" position = { x=500 y=664 } quadTextureSprite = GFX_icw_econ_button_160 buttonFont = hoi_16mbs text = "[icw_econ_enact_label]" }','}','}'])
    write('interface/ICW_economic_organisation.gui','\n'.join(compact))
    sg=[MARKER+' economic interface bindings','scripted_gui = {', '''icw_econ_compact = { context_type = player_context window_name = "icw_econ_compact_window" parent_window_name = icw_econ_anchor ai_enabled = { always = no } visible = { is_ai = no has_country_flag = icw_econ_initialized } properties = { icw_econ_compact_needle = { x = icw_econ_needle_x } } effects = { icw_econ_open_click = { set_country_flag = icw_econ_dialog_open icw_econ_touch = yes } } }''',
        '''icw_econ_reforms = { context_type = player_context window_name = "icw_econ_reforms_window" parent_window_name = icw_econ_dialog_anchor ai_enabled = { always = no } visible = { is_ai = no has_country_flag = icw_econ_initialized has_country_flag = icw_econ_dialog_open check_variable = { MD_tradeview_tab_economy_state = 1 } } properties = { icw_econ_dialog_needle = { x = icw_econ_needle_x }''']
    for index,(slug,*_) in enumerate(REFORMS,1):sg.append(f'icw_econ_select_{slug} = {{ frame = icw_econ_button_{index} }}')
    sg.append('} triggers = { icw_econ_enact_click_enabled = {')
    sg.append('OR = { '+' '.join(f'AND = {{ check_variable = {{ icw_econ_selected_reform = {i} }} icw_econ_can_{r[0]} = yes }}' for i,r in enumerate(REFORMS,1))+' } } }')
    sg.append('effects = { icw_econ_close_click = { clr_country_flag = icw_econ_dialog_open icw_econ_touch = yes }')
    for index,(slug,*_) in enumerate(REFORMS,1):
        assignments=' '.join(f'set_variable = {{ icw_econ_button_{j} = {2 if j==index else 1} }}' for j in range(1,6))
        sg.append(f'icw_econ_select_{slug}_click = {{ hidden_effect = {{ set_variable = {{ icw_econ_selected_reform = {index} }} {assignments} icw_econ_touch = yes }} }}')
    sg.append('icw_econ_enact_click = {')
    for index,(slug,*_) in enumerate(REFORMS,1):sg.append(f'if = {{ limit = {{ hidden_trigger = {{ check_variable = {{ icw_econ_selected_reform = {index} }} }} }} effect_tooltip = {{ icw_econ_preview_{slug} = yes }} hidden_effect = {{ icw_econ_start_{slug} = yes }} }}')
    sg.append('} } } }')
    write('common/scripted_guis/ICW_economic_organisation.txt','\n'.join(sg))

def integrate():
    # Match and move the complete immediate children of the inner scrolling economy container.
    path=ROOT/'interface/MD_countryeconomyview.gui'
    source=path.read_text(encoding='utf-8')
    old_anchor='name = "icw_econ_dialog_anchor" position = { x=20 y=205 } size = { width=680 height=640 }'
    new_anchor='name = "icw_econ_dialog_anchor" position = { x=20 y=135 } size = { width=680 height=710 }'
    if old_anchor in source:
        source=source.replace(old_anchor,new_anchor,1)
        if not source.startswith('# IMPERIA COLD WAR —'):
            source=MARKER+' reform-preview integration\n'+source
        path.write_text(source,encoding='utf-8')
    tag='# IMPERIA COLD WAR — Economic organisation compact bar'
    if tag not in source:
        match=re.search(r'containerWindowType\s*=\s*\{\s*name\s*=\s*"economyview_container"\s*position\s*=\s*\{\s*x=0 y=0\s*\}\s*size\s*=\s*\{\s*width = 722 height = 920\s*\}',source)
        assert match,'Economy content layout changed; inspect before integrating.'
        start=source.index('{',match.start());depth=1;i=start+1
        while depth:
            if source[i]=='{':depth+=1
            elif source[i]=='}':depth-=1
            i+=1
        body=source[start+1:i-1]
        # Direct nested windows only. All neighbours move together, not keyword-selected fields.
        tokens=list(re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]',body));depth=0;spans=[]
        for token in tokens:
            if token[0]=='{':
                if depth==0:opening=token.start()
                depth+=1
            elif token[0]=='}':
                depth-=1
                if depth==0:
                    preceding=body[max(0,opening-40):opening]
                    if re.search(r'containerWindowType\s*=\s*$',preceding):spans.append((opening,token.end()))
        moves=[]
        for a,b in reversed(spans):
            block=body[a:b]
            name=re.search(r'name\s*=\s*"([^"]+)"',block)[1]
            p=re.search(r'position\s*=\s*\{\s*x\s*=\s*(-?\d+)\s+y\s*=\s*(-?\d+)\s*\}',block)
            assert p, name
            old=int(p[2]);block=block[:p.start(2)]+str(old+138)+block[p.end(2):]
            body=body[:a]+block+body[b:];moves.append({'name':name,'before_y':old,'after_y':old+138})
        assert len(moves)>=3, moves
        body=body.replace('height = 920','height = 1058',1)
        body='\n                '+tag+'\n                containerWindowType = { name = "icw_econ_anchor" position = { x=0 y=0 } size = { width=680 height=126 } }\n'+body
        source=source[:start+1]+body+source[i-1:]
        path.write_text(source,encoding='utf-8')
        (OUT/'economy_layout_moves.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','moves':moves,'content_height':1058},indent=2),encoding='utf-8')
    # A named child anchor avoids relying on the generated instance name of a scripted root window.
    source=path.read_text(encoding='utf-8')
    tag='# IMPERIA COLD WAR — Economic organisation reform dialog anchor'
    if tag not in source:
        match=re.search(r'containerWindowType\s*=\s*\{\s*name\s*=\s*"MD_countryeconomyview"',source)
        assert match,'Economy root window missing'
        opening=source.index('{',match.start());depth=0;end=None
        for token in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]',source[opening:]):
            if token[0]=='{':depth+=1
            elif token[0]=='}':
                depth-=1
                if depth==0:end=opening+token.start();break
        assert end is not None
        source=source[:end].rstrip()+'\n\n        '+tag+'\n        containerWindowType = { name = "icw_econ_dialog_anchor" position = { x=20 y=205 } size = { width=680 height=640 } }\n    '+source[end:]
        path.write_text(source,encoding='utf-8')
    # Correct duration semantics: duration modifiers multiply days, not construction speed.
    path=ROOT/'common/scripted_effects/99_investment_scripted_effects.txt'
    source=path.read_text(encoding='utf-8')
    tag='# IMPERIA COLD WAR — Economic organisation investment duration semantics'
    if tag not in source:
        old='''\tclamp_temp_variable = { var = receiving_investment_duration_temp min = -1 }
\tif = { limit = { check_variable = { receiving_investment_duration_temp > 0 } }
\t\tadd_to_temp_variable = { construction_speed = receiving_investment_duration_temp }
\t}
\telse = {
\t\tsubtract_from_temp_variable = { construction_speed = receiving_investment_duration_temp }
\t}'''
        assert source.count(old)==1,'Investment duration reader changed; inspect before integrating.'
        source=source.replace(old,tag+'''\n\tset_temp_variable = { icw_investment_duration_factor = { value = 1 add = receiving_investment_duration_temp clamp = { min = 0.1 max = 10 } } }''')
        old='\t\tdivide_temp_variable = { building_cost = construction_speed }'
        assert source.count(old)==1
        source=source.replace(old,old+'\n\t\t'+tag+'\n\t\tmultiply_temp_variable = { building_cost = icw_investment_duration_factor }\n\t\tclamp_temp_variable = { var = building_cost min = 1 }')
        path.write_text(source,encoding='utf-8')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--scripts-only',action='store_true',help='Preserve the existing native artwork and sprite registration.')
    main(scripts_only=parser.parse_args().scripts_only)
