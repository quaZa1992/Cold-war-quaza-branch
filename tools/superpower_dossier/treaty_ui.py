# IMPERIA COLD WAR — Native approved briefing layout and configurable treaty editor
from treaties import TREATIES, FIELDS, OPTIONS


def build(write,loc,defined,mark):
    from presentation import txt,icon,btn,SIDES
    gui=[mark,'guiTypes = {','containerWindowType = { name = "icsd_launcher_window" position = { x=-333 y=88 } orientation = upper_right size = { width=46 height=46 }']
    for side in SIDES:gui.append(btn('icsd_launcher_'+side,0,0,'','launcher_'+side,tip='icsd_open_tt',shortcut='"shift+i"'))
    gui+=['}','containerWindowType = { name = "icsd_main_window" position = { x=0 y=0 } size = { width=790 height=794 } orientation = center origo = center moveable = yes']
    tests=[];clicks=[]
    def visible(name,cond):tests.append(name+'_visible = { '+cond+' }')
    def text(name,x,y,label,w,h=20,font='icsd_body',cond=None):
        gui.append(txt(name,x,y,label,w,h,font))
        if cond:visible(name,cond)
    def button(name,x,y,label,eff,cond=None,enabled='icwt_core = yes',sprite='action',tip=None,primary=False):
        if primary:
            for side,p in SIDES.items():
                button(name+'_'+side,x,y,label,eff,(cond+' ' if cond else '')+'tag = '+p['tag'],enabled,'primary_'+side,tip)
            return
        gui.append(btn(name,x,y,label,sprite,typeface='icsd_primary' if sprite.startswith('primary_') else 'icsd_button',tip=tip,shortcut='ESCAPE' if name=='icsd_close' else None));clicks.append(name+'_click = { '+eff+' }')
        if cond:visible(name,cond)
        tests.append(name+'_click_enabled = { '+enabled+' }')
    report='OR = { check_variable = { icsd_tab = 1 } AND = { check_variable = { icsd_tab = 3 } check_variable = { icwt_register = 0 } } }'
    treaty='OR = { check_variable = { icsd_tab = 2 } AND = { check_variable = { icsd_tab = 3 } check_variable = { icwt_register = 1 } } }'
    cat='check_variable = { icsd_tab = 2 } check_variable = { icwt_screen = 0 }'
    terms='check_variable = { icsd_tab = 2 } check_variable = { icwt_screen = 1 }'
    parties='check_variable = { icsd_tab = 2 } check_variable = { icwt_screen = 2 }'
    editing='OR = { AND = { '+terms+' } AND = { '+parties+' } }'
    review='check_variable = { icsd_tab = 2 } check_variable = { icwt_screen = 3 }'
    register='check_variable = { icsd_tab = 3 } check_variable = { icwt_register = 1 }'
    for side,p in SIDES.items():
        gui.append(icon('icsd_paper_'+side,0,0,'dossier_'+side));visible('icsd_paper_'+side,'tag = '+p['tag'])
    button('icsd_close',749,77,'','clr_country_flag = icsd_open icsd_touch = yes',enabled='icsd_view_access = yes',sprite='close')
    for i in range(1,4):
        x=41+(i-1)*209
        button(f'icsd_tab_{i}',x,224,'',f'''if = {{ limit = {{ icwt_core = yes }} set_variable = {{ icsd_tab = {i} }} clear_variable = icsd_offset clear_variable = icsd_selected_kind set_variable = {{ icwt_screen = 0 }}'''+(' set_variable = { icwt_register = 1 }' if i==3 else '')+' icsd_build_view = yes if = { limit = { check_variable = { icsd_row_count > 0 } } icsd_select_0 = yes } icwt_display = yes icsd_touch = yes }')
        for side,p in SIDES.items():gui.append(icon(f'icsd_tab_active_{i}_{side}',x,224,'tab_active_'+side));visible(f'icsd_tab_active_{i}_{side}',f'tag = {p["tag"]} check_variable = {{ icsd_tab = {i} }}')
        text(f'icsd_tab_label_{i}',x+8,236,'[icwt_tab_'+str(i)+']',194,18,'icsd_small')
    text('icsd_index',41,281,'[icwt_index_title]',174,18,'icsd_label')
    # Existing observations. Their cache is already filtered for the observer.
    for i in range(5):
        y=310+i*72;test=report+f' check_variable = {{ icsd_r{i}_kind > 0 }}'
        button(f'icsd_row_{i}',41,y,'',f'icsd_select_{i} = yes icsd_touch = yes',test,'icsd_view_access = yes',sprite='row')
        for side,p in SIDES.items():
            name=f'icsd_selected_{i}_{side}';gui.append(icon(name,41,y,'selected_'+side));visible(name,test+f' tag = {p["tag"]} '+' '.join(f'check_variable = {{ icsd_selected_{c} = icsd_r{i}_{c} }}' for c in ('actor','target','kind','key')))
        text(f'icsd_row_{i}_mark',48,y+5,'[icwt_report_mark]',160,17,'icsd_kicker',test)
        text(f'icsd_row_{i}_country',48,y+22,f'[?icsd_r{i}_target.GetName]',160,32,'icsd_body',test)
        text(f'icsd_row_{i}_type',48,y+54,f'[icsd_row_{i}_kind]',160,17,'icsd_small',test)
    text('icsd_page',41,682,'icsd_page',174,18,'icsd_small',report)
    button('icsd_prev',270,751,'<','if = { limit = { check_variable = { icsd_offset > 0 } } subtract_from_variable = { icsd_offset = 5 } icsd_build_view = yes icsd_select_0 = yes }',report,'check_variable = { icsd_offset > 0 }',sprite='page')
    button('icsd_next',322,751,'>','if = { limit = { check_variable = { icsd_view_count > icsd_next_offset } } add_to_variable = { icsd_offset = 5 } icsd_build_view = yes icsd_select_0 = yes }',report,'check_variable = { icsd_view_count > icsd_next_offset }',sprite='page')
    button('icwt_own_toggle',41,710,'[icwt_ledger_toggle]','if = { limit = { check_variable = { icwt_register = 1 } } clear_variable = icwt_register } else = { set_variable = { icwt_register = 1 } } clear_variable = icsd_offset icsd_build_view = yes icsd_select_0 = yes icwt_display = yes icsd_touch = yes','check_variable = { icsd_tab = 3 }',sprite='index_button')
    button('icwt_history',41,710,'[icwt_history_label]','if = { limit = { check_variable = { icsd_history = 1 } } clear_variable = icsd_history } else = { set_variable = { icsd_history = 1 } } clear_variable = icsd_offset icsd_build_view = yes icsd_select_0 = yes','check_variable = { icsd_tab = 1 }',sprite='index_button')
    selection=report+' icsd_has_selection = yes'
    text('icsd_doc_kicker',244,282,'[icsd_selected_kind_L]',508,18,'icsd_label',selection)
    text('icsd_detail_title',244,303,'[?icsd_selected_target.GetName]',508,35,'icsd_heading',selection)
    text('icwt_salutation',244,372,'[icwt_salutation]',508,18,'icsd_kicker',selection)
    for side,p in SIDES.items():
        for status in range(6):name=f'icsd_status_{side}_{status}';gui.append(icon(name,244,341,f'status_{side}_{status}'));visible(name,selection+f' tag = {p["tag"]} check_variable = {{ icsd_selected_state = {status} }}')
    text('icsd_summary',244,395,'[icwt_briefing]',508,72,'icsd_prose',selection)
    text('icsd_description',244,474,'[icsd_extra]',508,68,'icsd_small',selection)
    text('icwt_assessment_label',244,548,'icwt_assessment_label',508,18,'icsd_label',selection)
    text('icwt_assessment',244,571,'[icwt_assessment]',508,55,'icsd_prose',selection)
    text('icsd_response_header',244,632,'icsd_response_options',408,18,'icsd_label',selection)
    button('icsd_pick',244,626,'','set_country_flag = icsd_picking clr_country_flag = icsd_open clear_variable = icwt_pick_role icsd_touch = yes',selection,'icsd_view_access = yes',sprite='response',tip='icsd_pick_tt')
    button('icsd_more',662,628,'[icsd_more_label]','add_to_variable = { icsd_actions_page = 1 } if = { limit = { check_variable = { icsd_actions_page > 2 } } clear_variable = icsd_actions_page } icsd_touch = yes',selection,sprite='more')
    keys=('lend','volunteers','attache','money','sanctions','trade','invest','assist','party_action','politics','aid','subsidy')
    for i,key in enumerate(keys,1):
        k=(i-1)%4;x=244+(k%2)*258;y=656+(k//2)*43
        name=f'icsd_action_{i}'
        button(name,x,y,'icsd_'+key,'if = { limit = { icsd_view_access = yes icsd_has_selection = yes icsd_can_locate = yes } icsd_locate = yes }',selection+f' check_variable = {{ icsd_actions_page = {(i-1)//4} }}','icsd_can_locate = yes',tip=f'icsd_action_tip_{i}',primary=(i==1))
    text('icsd_empty_list',244,310,'icsd_no_records',508,72,'icsd_prose',report+' NOT = { icsd_has_selection = yes }')
    # Treaty categories and bounded static catalogue. No world or inventory query in a property.
    for c,label,x in ((1,'icwt_arms',41),(2,'icwt_economic',101),(3,'icwt_regional',161)):
        button(f'icwt_category_{c}',x,305,label,f'set_variable = {{ icwt_category = {c} }} clear_variable = icwt_page set_variable = {{ icwt_template = {1 if c==1 else 8 if c==2 else 10} }} set_variable = {{ icwt_screen = 0 }} icwt_display = yes icsd_touch = yes',treaty+' NOT = { check_variable = { icsd_tab = 3 } }',sprite='category')
    for n,(slug,title,caption,desc,c) in enumerate(TREATIES,1):
        index=[k for k,t in enumerate(TREATIES,1) if t[4]==c].index(n);page=index//4;y=345+(index%4)*72
        cond=f'check_variable = {{ icsd_tab = 2 }} check_variable = {{ icwt_category = {c} }} check_variable = {{ icwt_page = {page} }}'
        button(f'icwt_catalog_{n}',41,y,'',f'icwt_select_{n} = yes icwt_display = yes',cond,sprite='row',tip=f'icwt_history_{n}')
        for side,p in SIDES.items():
            name=f'icwt_catalog_selected_{n}_{side}';gui.append(icon(name,41,y,'selected_'+side));visible(name,cond+f' check_variable = {{ icwt_template = {n} }} tag = '+p['tag'])
        text(f'icwt_catalog_title_{n}',48,y+12,f'icwt_title_{n}',160,34,'icsd_body',cond)
        text(f'icwt_catalog_caption_{n}',48,y+49,f'icwt_caption_{n}',160,18,'icsd_small',cond)
    button('icwt_catalog_prev',41,635,'<','clear_variable = icwt_page icsd_touch = yes',treaty+' check_variable = { icsd_tab = 2 } check_variable = { icwt_category = 1 }','check_variable = { icwt_page > 0 }',sprite='page')
    button('icwt_catalog_next',93,635,'>','set_variable = { icwt_page = 1 } icsd_touch = yes',treaty+' check_variable = { icsd_tab = 2 } check_variable = { icwt_category = 1 }','check_variable = { icwt_page = 0 }',sprite='page')
    text('icwt_document_title',244,303,'[icwt_selected_title]',508,35,'icsd_heading',treaty)
    text('icwt_document_kicker',244,282,'[icwt_document_kicker]',508,18,'icsd_label',treaty)
    text('icwt_catalog_desc',244,356,'[icwt_selected_desc]',508,52,'icsd_prose',cat)
    gui.append(icon('icwt_catalog_spirit',244,418,'treaty_spirit'));visible('icwt_catalog_spirit',cat)
    text('icwt_catalog_spirit_name',316,432,'[icwt_selected_spirit]',436,48,'icsd_heading',cat)
    text('icwt_catalog_effects',244,490,'icwt_terms_summary',508,178,'icsd_body',cat)
    for n in range(1,len(TREATIES)+1):
        cond=cat+f' check_variable = {{ icwt_template = {n} }} check_variable = {{ icsd_tab = 2 }}'
        label='icwt_create' if n<=6 else 'icwt_create_custom' if n==12 else 'icwt_suggest'
        button(f'icwt_create_{n}',244,672,label,f'icwt_edit_{n} = yes icwt_display = yes',cond,f'icwt_core = yes NOT = {{ icwt_pending = yes }} check_variable = {{ global.icwt_{n}_members^num < 1 }}',tip=f'icwt_history_{n}')
        button(f'icwt_pending_{n}',41,680,'icwt_pending_short',f'icwt_review_{n} = yes icwt_display = yes',cat+f' check_variable = {{ global.icwt_pending = {n} }}',f'check_variable = {{ global.icwt_pending = {n} }}',sprite='index_button',tip='icwt_help_pending')
    button('icwt_custom_draft',502,672,'icwt_custom','icwt_open_custom = yes',cat+' NOT = { check_variable = { icwt_template = 12 } }','icwt_core = yes NOT = { icwt_pending = yes } check_variable = { global.icwt_12_members^num < 1 }',tip='icwt_history_12')
    # Two compact editor pages followed by a complete-effect review page.
    for screen,label,x in ((1,'icwt_terms',244),(2,'icwt_parties',502)):
        button(f'icwt_editor_{screen}',x,348,label,f'set_variable = {{ icwt_screen = {screen} }} icwt_display = yes icsd_touch = yes',editing)
    positions={'scope':(244,401),'reduction':(244,455),'reserve_limit':(502,455),'sanctions':(244,509),'trade':(502,509),'investment':(244,563),'duration':(502,563),'regional':(244,617),'programme':(502,617)}
    for f,(x,y) in positions.items():
        text(f'icwt_label_{f}',x,y,'icwt_label_'+f,244,18,'icsd_small',terms)
        amendment_guard=' NOT = { check_variable = { icwt_edit_addendum = 1 } }' if f!='programme' else ''
        if f=='programme':amendment_guard+=' OR = { check_variable = { icwt_template = 1 } check_variable = { icwt_template = 8 } check_variable = { icwt_template = 9 } check_variable = { icwt_template = 10 } }'
        button(f'icwt_value_{f}',x,y+18,'[icwt_value_'+f+']',f'icwt_cycle_{f} = yes icwt_display = yes',terms,'icwt_core = yes NOT = { icwt_pending = yes }'+amendment_guard,tip='icwt_help_'+f)
    text('icwt_participant_names',244,405,'icwt_participant_names',508,160,'icsd_body',parties)
    for role,label,y in ((1,'icwt_pick_usa',577),(2,'icwt_pick_sov',620),(3,'icwt_invite',663)):
        button(f'icwt_choose_{role}',244,y,label,f'set_variable = {{ icwt_pick_role = {role} }} set_country_flag = icsd_picking clr_country_flag = icsd_open icsd_touch = yes',parties,'icwt_core = yes NOT = { icwt_pending = yes } NOT = { check_variable = { icwt_edit_addendum = 1 } }',tip='icwt_help_'+('usa_target' if role==1 else 'sov_target' if role==2 else 'invites'))
    text('icwt_participant_note',502,577,'icwt_optional_note',244,116,'icsd_prose',parties)
    button('icwt_review_edit',502,704,'icwt_review_full','set_variable = { icwt_screen = 3 } icwt_display = yes icsd_touch = yes',editing,'icwt_core = yes',tip='icwt_workflow_help')
    text('icwt_review_terms',244,358,'icwt_terms_summary',508,160,'icsd_body',review)
    gui.append(icon('icwt_review_spirit',244,526,'treaty_spirit'));visible('icwt_review_spirit',review)
    text('icwt_review_spirit_name',316,540,'[icwt_selected_spirit]',436,48,'icsd_heading',review)
    text('icwt_review_reciprocity',244,602,'icwt_reciprocity',508,36,'icsd_prose',review)
    button('icwt_effect_preview',244,638,'icwt_effect_preview','icwt_preview_selected = yes',review,'icwt_core = yes',tip='icwt_effect_preview_tip')
    button('icwt_participants_preview',502,638,'icwt_participants_preview','',review,'icwt_core = yes',sprite='more',tip='icwt_participants_tip')
    for n in range(1,len(TREATIES)+1):
        cond=review+f' check_variable = {{ icwt_template = {n} }}'
        button(f'icwt_submit_{n}',244,688,'icwt_submit',f'icwt_send_{n} = yes icwt_display = yes',cond+' NOT = { icwt_pending = yes }','icwt_core = yes icwt_edit_valid = yes',primary=True)
        button(f'icwt_sign_{n}',244,688,'icwt_sign',f'icwt_sign_{n} = yes icwt_display = yes',cond+' icwt_pending = yes',f'icwt_core = yes check_variable = {{ global.icwt_pending = {n} }} icwt_reviewed_{n} = yes check_variable = {{ icwt_review_revision = global.icwt_p_revision }} NOT = {{ check_variable = {{ global.icwt_p_author = THIS.id }} }}',primary=True,tip='icwt_help_signature')
    button('icwt_decline',663,638,'icwt_decline_short','icwt_cancel_pending = yes icwt_display = yes',review+' icwt_pending = yes','icwt_core = yes',sprite='more')
    button('icwt_counter',502,688,'icwt_counter','icwt_counteroffer = yes icwt_display = yes',review+' icwt_pending = yes','icwt_core = yes icwt_pending = yes')
    button('icwt_amend',502,688,'icwt_amend','set_variable = { icwt_screen = 1 } icsd_touch = yes',review+' NOT = { icwt_pending = yes }')
    # Register: four cached membership IDs per page, with no per-frame traversal.
    for i in range(4):
        y=310+i*72
        button(f'icwt_register_row_{i}',41,y,'',f'set_variable = {{ icwt_template = icwt_rows^{i} }} clear_variable = icwt_exit_review icwt_display = yes icsd_touch = yes',register+f' check_variable = {{ icwt_rows^num > {i} }}',sprite='row')
        for side,p in SIDES.items():
            name=f'icwt_register_selected_{i}_{side}';gui.append(icon(name,41,y,'selected_'+side));visible(name,register+f' tag = {p["tag"]} check_variable = {{ icwt_rows^num > {i} }} check_variable = {{ icwt_template = icwt_rows^{i} }}')
        text(f'icwt_register_text_{i}',48,y+12,f'[icwt_register_name_{i}]',160,45,'icsd_body',register+f' check_variable = {{ icwt_rows^num > {i} }}')
    button('icwt_register_prev',41,635,'<','subtract_from_variable = { icwt_register_offset = 4 } icwt_display = yes',register,'check_variable = { icwt_register_offset > 0 }',sprite='page')
    button('icwt_register_next',93,635,'>','add_to_variable = { icwt_register_offset = 4 } icwt_display = yes',register,'check_variable = { icwt_list^num > icwt_register_next }',sprite='page')
    text('icwt_register_status',244,356,'[icwt_register_status]',508,52,'icsd_body',register)
    button('icwt_register_participants',662,394,'icwt_participants_preview','',register,'icwt_core = yes',sprite='more',tip='icwt_members_tip')
    current=register+' check_variable = { icwt_show_member = 1 }'
    gui.append(icon('icwt_register_spirit',244,418,'treaty_spirit'));visible('icwt_register_spirit',current)
    text('icwt_register_spirit_name',316,432,'[icwt_selected_spirit]',436,48,'icsd_heading',current)
    text('icwt_register_terms',244,490,'icwt_terms_summary',508,172,'icsd_body',register)
    text('icwt_register_note',244,664,'icwt_register_note',508,18,'icsd_small',register)
    for n in range(1,len(TREATIES)+1):
        cond=register+f' check_variable = {{ icwt_template = {n} }}'
        button(f'icwt_exit_review_{n}',244,684,'icwt_exit_review',f'set_variable = {{ icwt_exit_review = {n} }} icsd_touch = yes',cond+' check_variable = { icwt_exit_review = 0 }',f'has_country_flag = icwt_member_{n}')
        button(f'icwt_exit_{n}',244,684,'icwt_exit_confirm',f'icwt_leave_{n} = yes clear_variable = icwt_exit_review icwt_display = yes',cond+f' check_variable = {{ icwt_exit_review = {n} }}',f'has_country_flag = icwt_member_{n}')
    button('icwt_active_invite',41,666,'icwt_invite_active','set_variable = { icwt_pick_role = 4 } set_variable = { icwt_picking_template = icwt_template } set_country_flag = icsd_picking clr_country_flag = icsd_open icsd_touch = yes',register,'icwt_core = yes check_variable = { icwt_show_member = 1 }',sprite='index_button')
    button('icwt_consult',502,684,'icwt_consult','icwt_consult = yes',register,'icwt_core = yes')
    for n in (1,8,9,10):
        button(f'icwt_amend_programme_{n}',41,708,'icwt_amend_programme',f'icwt_edit_addendum_{n} = yes',register+f' check_variable = {{ icwt_template = {n} }}',f'icwt_core = yes NOT = {{ icwt_pending = yes }} USA = {{ has_country_flag = icwt_member_{n} }} SOV = {{ has_country_flag = icwt_member_{n} }}',sprite='index_button')
    button('icsd_sources',580,751,'?','',report,enabled='icsd_view_access = yes',sprite='page',tip='icsd_sources_tt')
    button('icwt_sources',580,751,'?','',treaty,enabled='icsd_view_access = yes',sprite='page',tip='icwt_workflow_help')
    gui+=['}','containerWindowType = { name = "icsd_picker_window" position = { x=20 y=200 } size = { width=430 height=85 }',btn('icsd_pick_use',0,0,'[icwt_picker_label]','modal_button'),btn('icsd_pick_cancel',0,42,'icsd_picker_cancel','modal_button'),'}','}']
    write('interface/ICW_superpower_dossier.gui','\n'.join(gui)+'\n')
    launch=['icsd_launcher = { context_type = player_context window_name = "icsd_launcher_window" dirty = icsd_dirty ai_enabled = { always = no } visible = { icsd_view_access = yes } triggers = {']
    for side,p in SIDES.items():launch.append(f'icsd_launcher_{side}_visible = {{ tag = {p["tag"]} }}')
    launch+=['} effects = {']
    for side in SIDES:launch.append(f'icsd_launcher_{side}_click = {{ if = {{ limit = {{ icsd_view_access = yes }} if = {{ limit = {{ has_country_flag = icsd_open }} clr_country_flag = icsd_open icsd_touch = yes }} else = {{ icsd_open = yes icwt_display = yes }} }} }}')
    launch+=['} }']
    picker='''icsd_picker = { context_type = selected_country_context parent_window_token = selected_country_view window_name = "icsd_picker_window" ai_enabled = { always = no }
visible = { ROOT = { icsd_view_access = yes has_country_flag = icsd_picking } exists = yes NOT = { tag = ROOT } }
effects = {
icsd_pick_use_click = { if = { limit = { exists = yes NOT = { tag = ROOT } ROOT = { icsd_view_access = yes has_country_flag = icsd_picking } }
ROOT = {
if = { limit = { check_variable = { icwt_pick_role = 1 } } set_variable = { icwt_edit_usa_target = PREV.id } }
else_if = { limit = { check_variable = { icwt_pick_role = 2 } } set_variable = { icwt_edit_sov_target = PREV.id } }
else_if = { limit = { check_variable = { icwt_pick_role = 3 } check_variable = { icwt_edit_invites^num < 6 } NOT = { is_in_array = { array = icwt_edit_invites value = PREV } } PREV = { NOT = { tag = USA } NOT = { tag = SOV } } } add_to_array = { icwt_edit_invites = PREV.id } }
else_if = { limit = { check_variable = { icwt_pick_role = 4 } } ACTIVE_INVITE_DISPATCH }
else_if = { limit = { check_variable = { icwt_pick_role = 0 } } set_variable = { icsd_response_target = PREV.id } }
clear_variable = icwt_pick_role clr_country_flag = icsd_picking set_country_flag = icsd_open icwt_display = yes icsd_touch = yes } } }
icsd_pick_cancel_click = { ROOT = { clear_variable = icwt_pick_role clr_country_flag = icsd_picking set_country_flag = icsd_open icsd_touch = yes } }
} }'''
    invite_dispatch=' '.join(f'if = {{ limit = {{ check_variable = {{ icwt_picking_template = {n} }} }} icwt_invite_active_{n} = yes }}' for n in range(1,len(TREATIES)+1))
    picker=picker.replace('ACTIVE_INVITE_DISPATCH',invite_dispatch)
    write('common/scripted_guis/ICW_superpower_dossier.txt',mark+'scripted_gui = {\n'+'\n'.join(launch)+'\nicsd_main = { context_type = player_context window_name = "icsd_main_window" dirty = icsd_dirty ai_enabled = { always = no } visible = { icsd_view_access = yes has_country_flag = icsd_open } triggers = {\n'+'\n'.join(tests)+'\n} effects = {\n'+'\n'.join(clicks)+'\n} }\n'+picker+'\n}\n')
