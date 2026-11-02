# IMPERIA COLD WAR — COMECON file-bound review and contribution controls
from native_ui import *

def compile_controls(gui,scripts,local):
    def footer_button(name,x,y,*args,**kwargs):
        return btn(name,x-240,y-541,*args,**kwargs)
    for s in range(1,5):
        prefix=f'cc_{s}_ui_';guard=f'is_ai = no check_variable = {{ cc_view_slot = {s} }}'
        loc(prefix+'review','Review Terms');loc(prefix+'reopen','Reopen Draft');loc(prefix+'balance','Balance')
        loc(prefix+'own',f'Your offer: [?cc_{s}_share|0]% · $[?cc_{s}_weekly|3]B/week')
        loc(prefix+'balance_tt','Offer the unfunded balance from your own national budget.')
        for key,action in [('review','review'),('approve','approve'),('finalize','finalize')]:
            loc(prefix+key+'_tt',f'§HRequirements:§!\n[!{prefix+action}_click_enabled]\n\n§HEffects:§!\n[!{prefix+action}_click]')
        local.append(defined(prefix+'finalize_label',[(cv(f'global.cc_{s}_phase','=',0),loc(prefix+'submit','Submit for Review')),(cv(f'global.cc_{s}_phase','=',1),'cc_ui_ratify')],loc(prefix+'active','Agreement Active')))
        body=[footer_button(prefix+'review',240,541,prefix+'review','GFX_cc_action_140',tip=prefix+'review_tt'),
            footer_button(prefix+'reset',390,541,'cc_ui_reset','GFX_cc_action_120'),footer_button(prefix+'reopen',390,541,prefix+'reopen','GFX_cc_action_120'),footer_button(prefix+'resume',525,541,'cc_ui_resume','GFX_cc_action_150'),
            footer_button(prefix+'finalize',716,541,'['+prefix+'finalize_label]','GFX_cc_primary_156','cc_primary',tip=prefix+'finalize_tt'),
            footer_button(prefix+'minus',240,541,'cc_minus','GFX_cc_action_60'),footer_button(prefix+'plus',307,541,'cc_plus','GFX_cc_action_60'),
            footer_button(prefix+'balance',376,541,prefix+'balance','GFX_cc_action_80','cc_registertab',tip=prefix+'balance_tt'),txt(prefix+'own',226,8,prefix+'own',240,20,'cc_small'),
            footer_button(prefix+'approve',240,541,'cc_ui_approve','GFX_cc_action_120',tip=prefix+'approve_tt'),footer_button(prefix+'decline',374,541,'cc_ui_decline','GFX_cc_action_120'),footer_button(prefix+'local',240,541,'cc_ui_local','GFX_cc_action_240')]
        name=prefix+'controls';gui.append(window(name,'\n'.join(body),640,35,240,541))
        actions=[f'{prefix}review_click = {{ cc_{s}_preview_all = yes hidden_effect = {{ if = {{ limit = {{ {guard} }} cc_{s}_acknowledge = yes cc_ui_refresh = yes }} }} }}',
            f'{prefix}finalize_click = {{ cc_{s}_preview_all = yes hidden_effect = {{ if = {{ limit = {{ {guard} }} if = {{ limit = {{ check_variable = {{ global.cc_{s}_phase = 0 }} }} cc_{s}_open_review = yes }} else_if = {{ limit = {{ check_variable = {{ global.cc_{s}_phase = 1 }} }} cc_{s}_ratify = yes }} }} }} }}']
        for button,fn in [('minus','decrease_share'),('plus','increase_share'),('balance','fund_remainder'),('approve','approve'),('decline','decline'),('local','confirm_local'),('reset','reset'),('reopen','reopen'),('resume','resume')]:
            preview=f'cc_{s}_preview_all = yes ' if button in ('approve','local') else ''
            actions.append(f'{prefix}{button}_click = {{ {preview}hidden_effect = {{ if = {{ limit = {{ {guard} }} cc_{s}_{fn} = yes }} }} }}')
        tr=[f'{prefix}finalize_visible = {{ check_variable = {{ cc_view_tab < 3 }} }}',f'{prefix}review_visible = {{ check_variable = {{ cc_view_tab = 0 }} }}',
            f'{prefix}review_click_enabled = {{ {guard} }}',
            f'{prefix}finalize_click_enabled = {{ OR = {{ cc_{s}_can_review = yes cc_{s}_can_ratify = yes }} }}',
            f'{prefix}reset_visible = {{ check_variable = {{ cc_view_tab = 0 }} cc_secretariat = yes check_variable = {{ global.cc_{s}_phase = 4 }} }}',
            f'{prefix}reopen_visible = {{ check_variable = {{ cc_view_tab = 0 }} cc_secretariat = yes check_variable = {{ global.cc_{s}_phase = 1 }} }}',
            f'{prefix}resume_visible = {{ check_variable = {{ cc_view_tab = 0 }} cc_secretariat = yes check_variable = {{ global.cc_{s}_phase = 2 }} check_variable = {{ global.cc_{s}_period_left = 0 }} }}',
            f'{prefix}own_visible = {{ check_variable = {{ cc_view_tab = 1 }} }}']
        for button in ['minus','plus','balance']:
            tr += [f'{prefix}{button}_visible = {{ check_variable = {{ cc_view_tab = 1 }} }}',f'{prefix}{button}_click_enabled = {{ cc_human_member = yes check_variable = {{ global.cc_{s}_phase = 0 }} }}']
        for button in ['approve','decline']:
            phase=f'OR = {{ check_variable = {{ global.cc_{s}_phase = 1 }} AND = {{ check_variable = {{ global.cc_{s}_phase = 2 }} is_in_array = {{ array = global.cc_{s}_payers value = THIS }} NOT = {{ cc_{s}_signed = yes }} }} }}' if button=='approve' else f'check_variable = {{ global.cc_{s}_phase = 1 }}'
            tr += [f'{prefix}{button}_visible = {{ check_variable = {{ cc_view_tab = 2 }} cc_{s}_voter = yes }}',f'{prefix}{button}_click_enabled = {{ cc_{s}_seen_terms = yes {phase} }}']
        tr += [f'{prefix}local_visible = {{ check_variable = {{ cc_view_tab = 2 }} is_ai = no cc_{s}_receiving_country = yes NOT = {{ cc_{s}_voter = yes }} }}',
            f'{prefix}local_click_enabled = {{ cc_{s}_seen_terms = yes check_variable = {{ global.cc_{s}_phase > 0 }} check_variable = {{ global.cc_{s}_phase < 4 }} }}']
        scripts.append(sg(name,name,visible=cv('cc_view_slot','=',s),effects='\n'.join(actions),triggers='\n'.join(tr)))

def compile_pickers(gui,scripts):
    for s in range(1,5):
        for kind,target in [(1,'host'),(2,'union')]:
            prefix=f'cc_{s}_pick_{kind}_';name=prefix+'window'
            body=[txt(prefix+'heading',12,9,'[cc_ui_picker_heading]',350,22,'cc_registertab'),grid(prefix+'choices',12,38,350,192,32,350),
                btn(prefix+'previous',12,233,'<','GFX_cc_tiny_button'),txt(prefix+'page',70,239,'cc_ui_choice_page',200,18,'cc_label'),btn(prefix+'next',340,233,'>','GFX_cc_tiny_button')]
            gui.append(window(name,'\n'.join(body),380,270,242,252,'background = { name = "cc_picker_paper" quadTextureSprite = GFX_cc_picker }'))
            entry=prefix+'entry';gui.append(window(entry,btn(prefix+'country',0,0,'cc_ui_popup_row','GFX_cc_choice_row','cc_country')+country_flag(prefix+'flag',4,6),350,32))
            valid='var:v = { cc_access = yes }' if kind==1 else 'OR = { check_variable = { v = SOV.id } var:v = { COLDWAR_SOV_is_union_republic = yes } }'
            guard=f'cc_{s}_editable = yes check_variable = {{ cc_view_slot = {s} }} check_variable = {{ cc_ui_popup = {kind} }}'
            fx=[f'{prefix}country_click = {{ if = {{ limit = {{ {guard} {valid} }} set_variable = {{ global.cc_{s}_{target} = v }} set_variable = {{ cc_ui_popup = 0 }} cc_{s}_revise = yes }} }}']
            for action,delta in [('previous',-1),('next',1)]:fx.append(f'{prefix}{action}_click = {{ if = {{ limit = {{ {guard} }} add_to_variable = {{ cc_ui_choice_page = {delta} }} cc_ui_refresh = yes cc_touch = yes }} }}')
            scripts.append(sg(name,name,visible=f'cc_secretariat = yes check_variable = {{ cc_view_slot = {s} }} check_variable = {{ cc_ui_popup = {kind} }}',effects=' '.join(fx),triggers=f'{prefix}previous_click_enabled = {{ check_variable = {{ cc_ui_choice_page > 0 }} }} {prefix}next_click_enabled = {{ check_variable = {{ cc_ui_choice_page < cc_ui_choice_max }} }}',properties=f'{prefix}flag = {{ image = "[?v.GetFlag]" }}',lists=f'{prefix}choices = {{ array = cc_ui_choice_rows entry_container = {entry} change_scope = no }}'))
        name=f'cc_{s}_scale_picker';body=[];fx=[]
        for tier,key in [(1,'cc_limited'),(2,'cc_standard'),(3,'cc_major')]:
            button=f'cc_{s}_scale_{tier}';body.append(btn(button,8,8+(tier-1)*36,key,'GFX_cc_scale_row','cc_country'))
            fx.append(f'{button}_click = {{ if = {{ limit = {{ cc_{s}_editable = yes check_variable = {{ cc_view_slot = {s} }} check_variable = {{ cc_ui_popup = 3 }} }} set_variable = {{ global.cc_{s}_tier = {tier} }} set_variable = {{ cc_ui_popup = 0 }} cc_{s}_revise = yes }} }}')
        gui.append(window(name,'\n'.join(body),342,124,538,291,'background = { name = "cc_picker_paper" quadTextureSprite = GFX_cc_scale_picker }'))
        scripts.append(sg(name,name,visible=f'cc_secretariat = yes check_variable = {{ cc_view_slot = {s} }} check_variable = {{ cc_ui_popup = 3 }}',effects=' '.join(fx)))
