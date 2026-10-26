# IMPERIA CW — Cold War: Guest Worker Administration
"""Native HOI4 UI and English presentation for the approved Ministry dossier."""
from pathlib import Path
import json
import re
from ministry_art import build as art
from ministry_runtime import HEADER, adapter, runtime
from ministry_overseas import runtime as overseas_runtime
from policy_content import build as build_policy_content
from ministry_policy import add as add_policy_page

ROOT=Path(__file__).resolve().parents[2]


def write(path,text):
    (ROOT/path).write_text(text,encoding='utf-8-sig' if path.endswith('.yml') else 'utf-8')


def main():
    build_policy_content(ROOT)
    art(ROOT/'gfx/interface/guest_workers')
    gfx=['spriteTypes = {']
    for name,frames in [('dashboard',1),('wide',3),('medium',3),('small',3),('page',3),
                        ('tab',3),('country',3),('danger',3),('coverage',11),('progress',5),
                        ('selection',1),('tab_selection',1),('muted',3),('wide_muted',3),('nav',3),('nav_selection',1)]:
        sprite='GFX_mdcw_gw_'+('button_'+name if name in ('wide','medium','small','page','tab','country','danger','muted','wide_muted','nav') else name)
        gfx.append(f' spriteType = {{ name = "{sprite}" texturefile = "gfx/interface/guest_workers/{name}.dds"'+(f' noOfFrames = {frames}' if frames>1 else '')+' }')
    write('interface/mdcw_diaspora.gfx',HEADER+'\n'.join(gfx)+'\n}\n')
    gui=['guiTypes = {',' containerWindowType = { name = "mdcw_gw_dashboard_window" position = { x = 4 y = 0 } size = { width = 510 height = 740 }']
    properties=[];triggers=[];effects=[];loc={};defined=[]
    def local(key,value):loc[key]=value;return key
    def show(name,condition='',tab=None):
        parts=([f'check_variable = {{ gw_ui_tab = {tab} }}'] if tab is not None else [])+([condition] if condition else [])
        if parts:triggers.append(f'{name}_visible = {{ '+ ' '.join(parts)+' }')
    def label(name,text,x,y,width=460,height=20,font='hoi4_typewriter16',align='left',tip=None,tab=None,condition=''):
        local(name,text);extra=f' pdx_tooltip = "{tip}"' if tip else ''
        gui.append(f' instantTextBoxType = {{ name = "{name}" position = {{ x = {x} y = {y} }} font = "{font}" text = "{name}" maxWidth = {width} maxHeight = {height} fixedsize = yes format = {align}{extra} }}')
        show(name,condition,tab)
    def icon(name,sprite,x,y,tab=None,condition='',prop=None):
        gui.append(f' iconType = {{ name = "{name}" spriteType = "{sprite}" position = {{ x = {x} y = {y} }} }}')
        show(name,condition,tab)
        if prop:properties.append(f'{name} = {{ {prop} }}')
    def button(name,text,x,y,style='medium',tab=None,condition='',enabled=None,effect=None,tip=None,font='hoi_16mbs'):
        local(name,text);extra=f' pdx_tooltip = "{tip}"' if tip else ''
        gui.append(f' buttonType = {{ name = "{name}" position = {{ x = {x} y = {y} }} quadTextureSprite = "GFX_mdcw_gw_button_{style}" buttonFont = "{font}" buttonText = "{name}"{extra} }}')
        show(name,condition,tab)
        if enabled is not None:triggers.append(f'{name}_click_enabled = {{ {enabled} }}')
        if effect:effects.append(f'{name}_click = {{ {effect} }}')
    def flag(name,var,x,y,tab,condition,click):
        gui.append(f' buttonType = {{ name = "{name}" position = {{ x = {x} y = {y} }} quadTextureSprite = "GFX_flag_small2" text = "" }}')
        properties.append(f'{name} = {{ image = "[?{var}.GetFlag]" }}')
        show(name,condition,tab)
        if click:effects.append(f'{name}_click = {{ {click} }}')
    def dt(name,entries,fallback):
        defined.append('defined_text = {\n name = '+name+'\n'+''.join(' text = { trigger = { '+c+' } localization_key = '+k+' }\n' for c,k in entries)+' text = { localization_key = '+fallback+' }\n}\n')
    def number(name,stock,people,millions):
        local(name+'_full',f'[?{people}|0]');local(name+'_million',f'[?{millions}|2] million')
        dt(name,[(f'check_variable = {{ {stock} > 2000 }}',name+'_million')],name+'_full')
    number('gw_ui_residents','mdcw_gw_guest_workers_k','gw_ui_population','gw_ui_population_m')
    number('gw_ui_abroad_count','gw_abroad_k','gw_ui_abroad','gw_ui_abroad_m')
    number('gw_ui_selected_count','gw_selected_stock_k','gw_ui_selected_people','gw_ui_selected_m')
    number('gw_ui_host_count','gw_ui_host_stock_k','gw_ui_host_people','gw_ui_host_m')
    dt('gw_ui_community_name',[('has_country_flag = gw_ui_show_abroad',local('gw_ui_host_name','[?gw_ui_host.GetName]'))],local('gw_ui_home_name','[?gw_selected_origin.GetName]'))
    dt('gw_ui_community_count',[('has_country_flag = gw_ui_show_abroad',local('gw_ui_host_count_line','[gw_ui_host_count] residents'))],local('gw_ui_home_count_line','[gw_ui_selected_count] residents'))
    dt('mdcw_gw_ministry_partner_name',[('check_variable = { gw_ui_partner > -1 }',local('gw_ui_partner_name','[?gw_ui_partner.GetName]'))],local('gw_ui_no_partner_name','an overseas employment partner'))
    icon('gw_dossier','GFX_mdcw_gw_dashboard',0,0)
    label('gw_department','MINISTRY OF LABOUR',24,17,font='hoi_16mbs')
    label('gw_dashboard_title','OVERSEAS LABOUR',24,37,font='hoi_24header',height=30)
    label('gw_dashboard_subtitle','Agreements | Communities | Public Services',24,73,font='hoi_16mbs',height=18)
    label('gw_file_heading','National Labour Office',24,105,width=330)
    label('gw_file_stamp','BRIEFING',368,105,width=110,align='right')
    sender='NOT = { check_variable = { mdcw_gw_guest_workers_k > 0 } } OR = { check_variable = { gw_abroad_k > 0 } check_variable = { mdcw_gw_remittance_pool_m > 0 } AND = { has_idea = mdcw_ni_overseas_employment_programme NOT = { has_idea = mdcw_ni_guest_worker_recruitment_programme } } }'
    domestic='NOT = { AND = { '+sender+' } }'
    for x,key,text,value,tip in [(24,'residents','Residents','[gw_ui_residents]',None),
                               (193,'share','Population share','[?gw_population_share|%1]',None),
                               (343,'cost','Weekly cost','$[?gw_total_m|2]m','gw_costs_tt')]:
        width=142 if x<300 else 137
        label('gw_metric_'+key+'_label',text,x,131,width=width,condition=domestic)
        label('gw_metric_'+key,value,x,153,width=width,font='hoi4_typewriter22',height=26,tip=tip,condition=domestic)
    for x,key,text,value in [(24,'abroad','Workers abroad','[gw_ui_abroad_count]'),(193,'remittance','Weekly remittances','$[?gw_dp_total_income_m|2]m'),(343,'partners','Overseas partners','[?gw_hosts^num|0]')]:
        # IMPERIA CW — Cold War: Explain the shared remittance limit on hover.
        remittance_tip='mdcw_gw_remittance_status_tt' if key=='remittance' else None
        label('gw_sender_metric_'+key+'_label',text,x,131,width=142,condition=sender,tip=remittance_tip)
        label('gw_sender_metric_'+key,value,x,153,width=142,font='hoi4_typewriter22',height=26,condition=sender,tip=remittance_tip)
    for n,(key,text,x) in enumerate([('overview','Overview',22),('communities','Communities',140),('recruitment','Recruitment',258),('policies','Policies',376)]):
        body=f'mdcw_gw_ledger_initialize = yes set_variable = {{ gw_ui_tab = {n} }} clr_country_flag = gw_ui_return_open '
        body+=('mdcw_gw_ministry_list_partners = yes' if n==2 else 'mdcw_gw_ministry_host_page = yes mdcw_dp_prepare_selected = yes' if n==3 else 'mdcw_gw_refresh_dashboard = yes')
        if n==1:
            body+=' if = { limit = { NOT = { check_variable = { mdcw_gw_guest_workers_k > 0 } } check_variable = { gw_abroad_k > 0 } } set_country_flag = gw_ui_show_abroad } if = { limit = { has_country_flag = gw_ui_show_abroad } mdcw_gw_ministry_host_page = yes }'
        button('gw_tab_'+key,text,x,194,'nav',effect=body)
        icon('gw_tab_'+key+'_selected','GFX_mdcw_gw_nav_selection',x,228,tab=n)
    # OVERVIEW: budget and ongoing policy, rather than every management button.
    label('gw_budget_heading','WEEKLY PUBLIC SPENDING',24,252,tab=0,font='hoi4_typewriter22',height=28,condition=domestic)
    for y,name,title,value in [(295,'health','Healthcare','gw_health_m'),(328,'welfare','Welfare','gw_welfare_m'),
                              (361,'bureaucracy','Administration','gw_administration_m'),(394,'integration','Integration & settlement','gw_ui_project_m')]:
        label('gw_budget_'+name,title,24,y,width=310,tab=0,tip='gw_costs_tt',condition=domestic)
        label('gw_budget_'+name+'_amount',f'$[?{value}|2]m',345,y,width=134,tab=0,align='right',tip='gw_costs_tt',condition=domestic)
    label('gw_budget_total','TOTAL / WEEK',24,438,width=310,tab=0,condition=domestic)
    label('gw_budget_total_amount','$[?gw_total_m|2]m',345,438,width=134,tab=0,align='right',tip='gw_costs_tt',condition=domestic)
    label('gw_project_heading','CURRENT PROGRAMME',24,484,tab=0,condition=domestic)
    label('gw_dashboard_project','[mdcw_gw_project_status]',24,512,height=40,tab=0,condition=domestic)
    label('gw_sender_heading','OVERSEAS EMPLOYMENT',24,252,tab=0,font='hoi4_typewriter22',height=28,condition=sender)
    for y,key,title,value in [(295,'abroad','Workers abroad','[gw_ui_abroad_count]'),(328,'income','Weekly remittances','$[?gw_dp_total_income_m|2]m'),(361,'cap','Weekly income limit','$3.00bn'),(394,'decline','Base weekly decline','0.01%')]:
        # IMPERIA CW — Cold War: Income and cap rows share the same explanation.
        remittance_tip='mdcw_gw_remittance_status_tt' if key in ('income','cap','decline') else None
        label('gw_sender_'+key+'_label',title,24,y,width=310,tab=0,condition=sender,tip=remittance_tip)
        label('gw_sender_'+key+'_value',value,345,y,width=134,align='right',tab=0,condition=sender,tip=remittance_tip)
    label('gw_sender_income_note','Remittances continue after recruitment closes.',24,438,tab=0,condition=sender)
    label('gw_consular_heading','CONSULAR AFFAIRS',24,484,tab=0,condition=sender)
    label('gw_consular_intro','Our embassies maintain ties with workers abroad.\nReview their access to public services and\narrange consular support under Communities.',24,512,height=64,tab=0,condition=sender)
    icon('gw_progress','GFX_mdcw_gw_progress',24,555,tab=0,condition='OR = { has_country_flag = gw_project_active has_country_flag = gw_return_active }',prop='frame = gw_progress_frame')
    label('gw_overview_backlash','Immigration Backlash: nationalist agitation',24,575,tab=0,condition='has_idea = mdcw_gw_immigration_backlash NOT = { check_variable = { gw_unrecorded_k > 0 } }',tip='mdcw_gw_immigration_backlash_desc')
    label('gw_overview_abroad','Workers abroad: [gw_ui_abroad_count]',24,605,tab=0,condition=domestic+' NOT = { check_variable = { gw_unrecorded_k > 0 } }')
    label('gw_overview_remittances','Remittances: $[?gw_dp_total_income_m|2]m/week',24,630,tab=0,condition=domestic,tip='mdcw_gw_remittance_status_tt')
    button('gw_manage','Manage Communities',24,654,'wide',tab=0,effect='set_variable = { gw_ui_tab = 1 } mdcw_gw_refresh_dashboard = yes if = { limit = { '+sender+' } set_country_flag = gw_ui_show_abroad } if = { limit = { has_country_flag = gw_ui_show_abroad } mdcw_gw_ministry_host_page = yes }')
    # COMMUNITIES: exactly four rows, plus detail for the selected origin.
    button('gw_home_mode','At Home',24,240,tab=1,effect='clr_country_flag = gw_ui_show_abroad clr_country_flag = gw_ui_return_open mdcw_gw_refresh_dashboard = yes')
    button('gw_abroad_mode','Abroad',182,240,tab=1,effect='set_country_flag = gw_ui_show_abroad clr_country_flag = gw_ui_return_open mdcw_gw_ministry_host_page = yes')
    icon('gw_home_mode_selected','GFX_mdcw_gw_tab_selection',24,271,tab=1,condition='NOT = { has_country_flag = gw_ui_show_abroad }')
    icon('gw_abroad_mode_selected','GFX_mdcw_gw_tab_selection',182,271,tab=1,condition='has_country_flag = gw_ui_show_abroad')
    label('gw_dashboard_column_count','RESIDENTS',360,247,width=114,align='right',tab=1)
    for row in range(1,5):
        y=276+(row-1)*40;condition=f'NOT = {{ has_country_flag = gw_ui_show_abroad }} check_variable = {{ gw_row{row}_k > 0 }}'
        effect=f'set_variable = {{ gw_selected_origin = gw_row{row}_origin }} clr_country_flag = gw_ui_return_open mdcw_gw_select_origin = yes'
        number(f'gw_ui_row{row}_count',f'gw_row{row}_k',f'gw_row{row}_people',f'gw_row{row}_m')
        button(f'gw_row{row}_select','',24,y,'country',tab=1,condition=condition,effect=effect)
        flag(f'gw_row{row}_flag',f'gw_row{row}_origin',31,y+5,1,condition,effect)
        label(f'gw_row{row}_name',f'[?gw_row{row}_origin.GetName]',81,y+10,width=264,tab=1,condition=condition)
        label(f'gw_row{row}_amount',f'[gw_ui_row{row}_count]',351,y+10,width=125,align='right',tab=1,condition=condition)
        icon(f'gw_row{row}_selected','GFX_mdcw_gw_selection',24,y,tab=1,condition=condition+f' check_variable = {{ gw_selected_origin = gw_row{row}_origin }}')
    for row in range(1,5):
        y=276+(row-1)*40;condition=f'has_country_flag = gw_ui_show_abroad check_variable = {{ gw_host{row}_k > 0 }}'
        click=f'set_variable = {{ gw_ui_host = gw_host{row}_origin }} mdcw_gw_ministry_host_selection = yes'
        number(f'gw_ui_host{row}_count',f'gw_host{row}_k',f'gw_host{row}_people',f'gw_host{row}_m')
        button(f'gw_host{row}_select','',24,y,'country',tab=1,condition=condition,effect=click)
        flag(f'gw_host{row}_flag',f'gw_host{row}_origin',31,y+5,1,condition,click)
        label(f'gw_host{row}_name',f'[?gw_host{row}_origin.GetName]',81,y+10,width=264,tab=1,condition=condition)
        label(f'gw_host{row}_amount',f'[gw_ui_host{row}_count]',351,y+10,width=125,align='right',tab=1,condition=condition)
        icon(f'gw_host{row}_selected','GFX_mdcw_gw_selection',24,y,tab=1,condition=condition+f' check_variable = {{ gw_ui_host = gw_host{row}_origin }}')
    label('gw_dashboard_empty','No guest-worker communities live here.',24,294,tab=1,condition='NOT = { has_country_flag = gw_ui_show_abroad } check_variable = { gw_ui_indices^num = 0 }')
    label('gw_overseas_empty','No active overseas communities on this page.',24,294,tab=1,condition='has_country_flag = gw_ui_show_abroad '+ ' '.join(f'NOT = {{ check_variable = {{ gw_host{r}_k > 0 }} }}' for r in range(1,5)))
    label('gw_dashboard_page','Communities: [?gw_ui_indices^num|0] | Page [?gw_page_display|0]',24,441,width=360,tab=1,condition='NOT = { has_country_flag = gw_ui_show_abroad }')
    label('gw_host_page','Overseas partners: [?gw_hosts^num|0] | Page [?gw_ui_host_page_display|0]',24,441,width=360,tab=1,condition='has_country_flag = gw_ui_show_abroad')
    button('gw_previous','<',404,436,'page',tab=1,condition='NOT = { has_country_flag = gw_ui_show_abroad }',enabled='check_variable = { gw_page > 0 }',effect='subtract_from_variable = { gw_page = 1 } mdcw_gw_refresh_dashboard = yes')
    button('gw_next','>',449,436,'page',tab=1,condition='NOT = { has_country_flag = gw_ui_show_abroad }',enabled='check_variable = { gw_next_offset < gw_ui_indices^num }',effect='if = { limit = { check_variable = { gw_next_offset < gw_ui_indices^num } } add_to_variable = { gw_page = 1 } mdcw_gw_refresh_dashboard = yes }')
    button('gw_host_previous','<',404,436,'page',tab=1,condition='has_country_flag = gw_ui_show_abroad',enabled='check_variable = { gw_ui_host_page > 0 }',effect='subtract_from_variable = { gw_ui_host_page = 1 } mdcw_gw_ministry_host_page = yes')
    button('gw_host_next','>',449,436,'page',tab=1,condition='has_country_flag = gw_ui_show_abroad',enabled='check_variable = { gw_ui_host_next < gw_hosts^num }',effect='if = { limit = { check_variable = { gw_ui_host_next < gw_hosts^num } } add_to_variable = { gw_ui_host_page = 1 } mdcw_gw_ministry_host_page = yes }')
    selected='NOT = { has_country_flag = gw_ui_show_abroad } check_variable = { gw_selected_stock_k > 0 }';normal=selected+' NOT = { has_country_flag = gw_ui_return_open }'
    abroad='has_country_flag = gw_ui_show_abroad check_variable = { gw_ui_host_stock_k > 0 }'
    either='OR = { AND = { '+normal+' } AND = { '+abroad+' } }'
    label('gw_selected_title','[gw_ui_community_name]',24,477,width=460,tab=1,condition='OR = { AND = { '+selected+' } AND = { '+abroad+' } }',font='hoi4_typewriter22',height=27)
    label('gw_selected_count','[gw_ui_community_count]',24,505,tab=1,condition='OR = { AND = { '+selected+' } AND = { '+abroad+' } }',tip='gw_dp_migration_tt')
    label('gw_dashboard_select_hint','Select a country flag to review its community.',24,477,height=40,tab=1,condition='NOT = { OR = { AND = { '+selected+' } AND = { '+abroad+' } } }')
    for source,title,y in [('registered','Language support',539),('housed','Housing & services',567),('protected','Labour protection',595)]:
        label('gw_selected_'+source,title,24,y,width=165,tab=1,condition=either)
        icon('gw_bar_'+source,'GFX_mdcw_gw_coverage',193,y+12,tab=1,condition=either,prop=f'frame = gw_ui_{source}_frame')
        label('gw_selected_'+source+'_percent',f'[?gw_ui_{source}_ratio|%0]',398,y-4,width=79,align='right',tab=1,condition=either)
    for choice,(name,text,x) in enumerate([('gw_register','Language Support',24),('gw_housing','Housing & Services',182),('gw_protect','Labour Protection',340)],1):
        # Coverage is revalidated in the confirmation too. Fully covered groups
        # cannot open a misleading funding dialog.
        field=('registered','housed','protected')[choice-1]
        enabled=f'mdcw_gw_can_plan_integration = yes NOT = {{ has_country_flag = gw_dialog_window }} check_variable = {{ gw_selected_{field}_k < gw_selected_stock_k }}'
        click=f'if = {{ limit = {{ {enabled} }} set_variable = {{ gw_dialog_origin = gw_selected_origin }} set_country_flag = gw_dialog_window set_country_flag = {{ flag = gw_dialog_valid value = 1 days = 13 }} set_variable = {{ gw_project_choice = {choice} }} mdcw_gw_prepare_project = yes country_event = {{ id = mdcw_diaspora.{10+choice} }} }}'
        button(name,text,x,620,tab=1,condition=normal,enabled=enabled,effect=click,tip=name+'_tt')
    button('gw_return_menu','Repatriation...',24,656,'danger',tab=1,condition=normal,enabled='mdcw_gw_can_plan_return = yes NOT = { has_country_flag = gw_dialog_window }',effect='set_country_flag = gw_ui_return_open add_to_variable = { gw_ui_dirty = 1 }',tip='gw_return_tt')
    label('gw_selected_status','[mdcw_gw_management_status]',264,660,width=214,tab=1,condition=normal)
    outreach='NOT = { has_country_flag = gw_dialog_window } NOT = { check_variable = { political_power < 75 } } NOT = { check_variable = { treasury < 0.5 } } var:gw_ui_host = { mdcw_gw_outreach_target_valid = yes }'
    button('gw_outreach','Consular Outreach',24,620,'wide',tab=1,condition=abroad,enabled=outreach,effect='if = { limit = { '+outreach+' } set_variable = { gw_dialog_host = gw_ui_host } set_country_flag = gw_dialog_window set_country_flag = { flag = gw_dialog_valid days = 13 } country_event = { id = mdcw_diaspora.86 } }',tip='gw_outreach_tt')
    local('gw_outreach_tt','Strengthen consular and cultural links with our community.\n\n75 Political Power | $$500 million | 180 days\nInfluence action effectiveness: up to +10%.\nRequires 25,000 residents and 0.25% of the host population. Labour integration reduces its effectiveness.')
    button('gw_resume_host','Resume Agreements',264,620,'wide',tab=1,condition=abroad+' is_in_array = { gw_suspended_hosts = gw_ui_host }',effect='remove_from_array = { gw_suspended_hosts = gw_ui_host } add_to_variable = { gw_ui_dirty = 1 }')
    label('gw_overseas_note','Support abroad strengthens diplomatic ties;\ninfluence still requires diplomatic action.',24,651,height=32,tab=1,condition=abroad)
    for amount,x in [(25,24),(50,142),(100,260),(0,378)]:
        enabled='mdcw_gw_can_plan_return = yes NOT = { has_country_flag = gw_dialog_window } '+(f'NOT = {{ check_variable = {{ gw_selected_stock_k < {amount} }} }}' if amount else 'check_variable = { gw_selected_stock_k < 25 }')
        selection=str(amount) if amount else 'gw_selected_stock_k'
        extra='clamp_variable = { var = gw_return_choice_k min = 0 max = 24.999 }' if not amount else ''
        click=f'if = {{ limit = {{ {enabled} }} set_variable = {{ gw_dialog_origin = gw_selected_origin }} set_country_flag = gw_dialog_window set_country_flag = {{ flag = gw_dialog_valid days = 7 }} set_variable = {{ gw_return_choice_k = {selection} }} {extra} mdcw_gw_prepare_return = yes country_event = {{ id = mdcw_diaspora.30 }} clr_country_flag = gw_ui_return_open }}'
        button('gw_return_'+str(amount),f'{amount},000' if amount else 'Final Group',x,555,'small',tab=1,condition=selected+' has_country_flag = gw_ui_return_open',enabled=enabled,effect=click,tip='gw_return_tt')
    label('gw_return_explanation','Forced return | 90-day preparation\nCosts and diplomatic consequences are shown\nbefore authorisation.',24,600,height=60,tab=1,condition=selected+' has_country_flag = gw_ui_return_open')
    button('gw_return_back','Back to Community',24,656,'wide',tab=1,condition='has_country_flag = gw_ui_return_open',effect='clr_country_flag = gw_ui_return_open add_to_variable = { gw_ui_dirty = 1 }')
    # RECRUITMENT: a bounded country page is populated only on tab entry/reload.
    label('gw_partner_heading','CHOOSE A PARTNER',24,247,width=300,tab=2)
    button('gw_partner_refresh','Refresh List',340,241,tab=2,enabled='NOT = { has_country_flag = gw_ui_partner_report_requested }',effect='mdcw_gw_ministry_refresh_partners = yes',tip='gw_partner_refresh_tt')
    local('gw_partner_refresh_tt','Request updated details from our overseas employment offices. A new report can be requested once per day. Agreement terms are checked again when we negotiate.')
    for row in range(1,5):
        y=282+(row-1)*40;cond=f'check_variable = {{ gw_ui_partner_{row} > -1 }}';var=f'gw_ui_partner_{row}'
        click=f'set_variable = {{ gw_ui_partner = {var} }} mdcw_gw_ministry_counters = yes add_to_variable = {{ gw_ui_dirty = 1 }}'
        button('gw_partner_'+str(row)+'_select','',24,y,'country',tab=2,condition=cond,effect=click)
        flag('gw_partner_'+str(row)+'_flag',var,31,y+5,2,cond,click)
        label('gw_partner_'+str(row)+'_name',f'[?{var}.GetName]',81,y+10,width=393,tab=2,condition=cond)
        icon('gw_partner_'+str(row)+'_selected','GFX_mdcw_gw_selection',24,y,tab=2,condition=cond+f' check_variable = {{ gw_ui_partner = {var} }}')
    label('gw_partner_empty','No overseas employment partners are available.',24,294,height=40,tab=2,condition='check_variable = { gw_ui_candidates^num = 0 }')
    label('gw_partner_page','Partners: [?gw_ui_candidates^num|0] | Page [?gw_ui_partner_page_display|0]',24,451,width=360,tab=2)
    button('gw_partner_previous','<',404,446,'page',tab=2,enabled='check_variable = { gw_ui_partner_page > 0 }',effect='subtract_from_variable = { gw_ui_partner_page = 1 } mdcw_gw_ministry_partner_page = yes')
    button('gw_partner_next','>',449,446,'page',tab=2,enabled='check_variable = { gw_ui_partner_next < gw_ui_candidates^num }',effect='if = { limit = { check_variable = { gw_ui_partner_next < gw_ui_candidates^num } } add_to_variable = { gw_ui_partner_page = 1 } mdcw_gw_ministry_partner_page = yes }')
    label('gw_partner_selected','[?gw_ui_partner.GetName]',24,490,tab=2,condition='check_variable = { gw_ui_partner > -1 }',font='hoi4_typewriter22',height=27)
    label('gw_recruitment_readiness','[mdcw_gw_ministry_readiness]',24,522,height=44,tab=2)
    for size,pp,cash,x in [(25000,75,10,24),(50000,125,15,182),(100000,200,25,340)]:
        # IMPERIA CW — Cold War: One actionable control or its inert grey twin.
        # Both read the same live guard, refreshed by the pending-state transition.
        ready=f'mdcw_gw_ui_can_recruit_{size} = yes'
        button('gw_recruit_'+str(size),f'{size:,} Workers',x,579,tab=2,condition=ready,enabled=ready,effect=f'mdcw_gw_ui_recruit_{size} = yes',tip='gw_recruit_'+str(size)+'_tt')
        button('gw_recruit_'+str(size)+'_unavailable',f'{size:,} Workers',x,579,'muted',tab=2,condition='NOT = { '+ready+' }',enabled='always = no',tip='gw_recruit_'+str(size)+'_tt')
        label('gw_recruit_'+str(size)+'_price',f'{pp} PP | ${cash}bn',x,615,width=148,tab=2,align='center')
        local('gw_recruit_'+str(size)+'_tt',f'Recruit {size:,} workers from [mdcw_gw_ministry_partner_name].\n\nPolitical Power: §R{pp}§!\nPayment on approval: §R$${cash} billion§!\n\n[mdcw_gw_ministry_readiness_{size}]\nGovernment approval is required. Unsuccessful negotiations refund Political Power.')
    label('gw_recruitment_note','Partner government approval is required.\nNext recruitment: 60 days after approval.',24,643,height=36,tab=2)
    label('gw_legacy_notice','Origin unknown: [?gw_unrecorded_k|1] thousand.\nUpdate residency records in the decisions below.',24,575,height=48,tab=0,condition='check_variable = { gw_unrecorded_k > 0 }')
    # IMPERIA CW — Cold War: Dedicated programme page, separate from community services.
    add_policy_page(label,button,local,dt,flag)
    # Footer: closure is not offered while residents/operations remain.
    button('gw_suspend','[mdcw_gw_recruitment_button]',24,700,'wide',condition='has_idea = mdcw_ni_guest_worker_recruitment_programme',enabled='has_idea = mdcw_ni_guest_worker_recruitment_programme NOT = { has_country_flag = mdcw_gw_request_pending } NOT = { has_country_flag = mdcw_gw_offer_pending }',effect='if = { limit = { has_country_flag = gw_recruitment_suspended } clr_country_flag = gw_recruitment_suspended } else = { set_country_flag = gw_recruitment_suspended } add_to_variable = { gw_ui_dirty = 1 }',tip='gw_suspend_tt')
    close='has_idea = mdcw_ni_guest_worker_recruitment_programme NOT = { check_variable = { mdcw_gw_guest_workers_k > 0 } } NOT = { has_country_flag = gw_project_active } NOT = { has_country_flag = gw_return_active } NOT = { has_country_flag = mdcw_gw_request_pending } NOT = { has_country_flag = mdcw_gw_offer_pending } NOT = { has_country_flag = mdcw_gw_offer_window_open }'
    button('gw_close','Close Programme | 150 PP',264,700,'wide',condition=close,enabled='mdcw_gw_can_close_programme = yes',effect='if = { limit = { mdcw_gw_can_close_programme = yes } add_political_power = -150 remove_ideas = mdcw_ni_guest_worker_recruitment_programme clr_country_flag = gw_recruitment_suspended ingame_update_setup = yes }',tip='gw_close_tt')
    label('gw_footer_residents','Responsibilities remain\nwhile guest workers live here.',264,697,width=215,height=36,condition='check_variable = { mdcw_gw_guest_workers_k > 0 }')
    gui+=[' }','}'];write('interface/mdcw_diaspora.gui',HEADER+'\n'.join(gui)+'\n')
    write('common/scripted_guis/mdcw_diaspora_gui.txt',HEADER+'scripted_gui = {\n mdcw_gw_dashboard = {\n context_type = decision_category\n window_name = "mdcw_gw_dashboard_window"\n dirty = gw_ui_dirty\n ai_enabled = { always = no }\n properties = {\n'+'\n'.join(properties)+'\n }\n triggers = {\n'+'\n'.join(triggers)+'\n }\n effects = {\n'+'\n'.join(effects)+'\n }\n }\n}\n')
    extra_triggers,extra_effects,tt=adapter(ROOT)
    write('common/scripted_triggers/mdcw_diaspora_dashboard_triggers.txt',extra_triggers)
    write('common/scripted_effects/mdcw_diaspora_dashboard_effects.txt',runtime()+overseas_runtime())
    write('common/scripted_effects/mdcw_diaspora_recruitment_effects.txt',extra_effects)
    # FROM text is adapted with the same country-local selection as the scripts.
    source={}
    for name in ('mdcw_guest_workers_l_english.yml','mdcw_diaspora_l_english.yml'):
        source.update({k:json.loads(v) for k,v in re.findall(r'^ (\S+):\d+ (".*")$',(ROOT/'localisation/english'/name).read_text(encoding='utf-8-sig'),re.M)})
    for key in sorted(tt):
        loc['gw_ui_'+key]=source[key].replace('[FROM.GetName]','[?gw_ui_partner.GetName]').replace('[?FROM.gdp_per_capita|2]','[?gw_ui_partner_gdpc|2]')
    reasons=[('NOT = { has_idea = mdcw_ni_guest_worker_recruitment_programme }','Establish the Guest Worker Recruitment Programme.'),
             ('has_country_flag = gw_recruitment_suspended','Recruitment is suspended.'),
             ('has_country_flag = gw_return_active','Complete the ongoing repatriation first.'),
             ('has_country_flag = mdcw_gw_request_pending','Awaiting a reply from [?mdcw_gw_partner.GetName].'),
             ('OR = { has_country_flag = mdcw_gw_request_pending has_country_flag = mdcw_gw_offer_pending has_country_flag = mdcw_gw_offer_window_open has_country_flag = gw_dp_request has_country_flag = gw_dp_offer has_country_flag = gw_dp_offer_window }','Conclude our current labour negotiations first.'),
             ('has_country_flag = mdcw_gw_receiving_cooldown','We must wait 60 days after our last agreement.'),
             ('NOT = { check_variable = { gw_ui_partner > -1 } }','Select an overseas employment partner.'),
             ('var:gw_ui_partner = { NOT = { exists = yes } }','The selected partner is no longer available.'),
             ('NOT = { mdcw_gw_ui_pair_not_suspended = yes }','This government has suspended agreements with us.'),
             ('var:gw_ui_partner = { OR = { has_country_flag = mdcw_gw_request_pending has_country_flag = mdcw_gw_offer_pending has_country_flag = mdcw_gw_offer_window_open has_country_flag = gw_dp_request has_country_flag = gw_dp_offer has_country_flag = gw_dp_offer_window } }','This government is negotiating another agreement.'),
             ('NOT = { mdcw_gw_ui_income_advantage = yes }','Our GDP per capita must be at least 25% higher.'),
             ('check_variable = { treasury < 10 }','At least $10 billion is required for an agreement.'),
             ('has_political_power < 75','At least 75 Political Power is required.'),
             ('NOT = { mdcw_gw_ui_request_available_25000 = yes }','The selected partner cannot fulfil an agreement now.')]
    dt('mdcw_gw_ministry_readiness',[(c,local('gw_ministry_reason_'+str(i),v)) for i,(c,v) in enumerate(reasons)],local('gw_ministry_ready','Ready to negotiate. Choose an agreement below.'))
    for size,pp,cash in [(25000,75,10),(50000,125,15),(100000,200,25)]:
        # Keep the general status brief; show the selected tier's precise blocker
        # in its own tooltip, rather than saying "Ready" on a disabled button.
        entries=[(c,'gw_ministry_reason_'+str(i)) for i,(c,v) in enumerate(reasons[:-3])]
        entries += [(f'check_variable = {{ treasury < {cash} }}',local(f'gw_tier_cash_{size}',f'This agreement requires $${cash} billion.')),
                    (f'check_variable = {{ political_power < {pp} }}',local(f'gw_tier_pp_{size}',f'This agreement requires {pp} Political Power.')),
                    (f'NOT = {{ var:gw_ui_partner = {{ mdcw_gw_ui_has_sending_state_{size} = yes }} }}',local(f'gw_tier_population_{size}',
                      'This agreement needs two regions, each with more than 50,000 residents.' if size==100000 else f'The partner needs a region with more than {size:,} residents.')),
                    (f'NOT = {{ mdcw_gw_ui_request_available_{size} = yes }}',local(f'gw_tier_unavailable_{size}','The agreement cannot proceed under the present conditions.'))]
        dt(f'mdcw_gw_ministry_readiness_{size}',entries,'gw_ministry_ready')
    write('common/scripted_localisation/mdcw_diaspora_dashboard_localisation.txt',HEADER+'\n'.join(defined))
    write('localisation/english/mdcw_diaspora_ui_l_english.yml','l_english:\n'+HEADER+''.join(f' {key}:0 {json.dumps(value,ensure_ascii=False)}\n' for key,value in loc.items()))
    print('Built IMPERIA CW Ministry dossier: 510x740, four tabs, bounded diaspora policies and guarded native transactions.')
