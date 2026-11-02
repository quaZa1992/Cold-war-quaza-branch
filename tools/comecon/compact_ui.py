# IMPERIA COLD WAR — COMECON compact paged native investment dossier
import textwrap
from native_ui import *
from pagination import turn_page

W,H=900,580
PX,PY,PW,PH=222,156,658,340
INNER=622

def heading(s,description=True):
    body=[icon('cc_page_mark',18,12,'GFX_cc_project_symbols'),
        txt('cc_page_file',78,9,'[cc_ui_file_heading]',562,16,'cc_label'),
        txt('cc_page_title',78,29,f'[cc_{s}_programme_name]',562,26,'cc_number')]
    if description:body += [txt('cc_page_description',18,58,f'[cc_{s}_description]',INNER,40,'cc_small'),icon('cc_heading_rule',18,101,'GFX_cc_line_622')]
    return '\n'.join(body)

def page(name,body):
    return window(name,body,PW,PH,PX,PY,'clipping = yes background = { name = "cc_page_hit_area" quadTextureSprite = GFX_tiled_window_transparent }')

def compile_compact_ui():
    local=register_text()
    labels={'cc_title':'Council for Mutual Economic Assistance','cc_caption_projects':'PROJECTS · 90 DAYS','cc_caption_joint':'PROGRAMMES · 180 DAYS',
        'cc_ui_file_selector':'FILE [?cc_view_slot|0] / 4','cc_ui_register_page':'[?cc_ui_register_number|0] / 2',
        'cc_ui_page':'PAGE [?cc_ui_leaf|0] / [?cc_ui_leaves|0] · [cc_ui_sheet_name]',
        'cc_sheet_overview':'OVERVIEW','cc_sheet_terms':'AGREEMENT TERMS','cc_sheet_effects':'COUNTRY EFFECTS',
        'cc_sheet_contributions':'CONTRIBUTIONS','cc_sheet_signatures':'SIGNATURES',
        'cc_ui_member_count':'[?cc_ui_delegate_count|0] delegations',
        'cc_ui_choice_page':'[?cc_ui_choice_number|0] / [?cc_ui_choice_pages|0]',
        'cc_ui_empty':'No countries are currently participating.',
        'cc_ui_turn_previous':'Previous page','cc_ui_turn_next':'Next page',
        'cc_ui_sidebar_previous':'Previous register page','cc_ui_sidebar_next':'Next register page',
        'cc_effects_country':'COUNTRY','cc_effects_benefits':'AGREED BENEFITS','cc_effects_costs':'SERVICES/WEEK',
        'cc_effects_timing':'Permanent assets · [?cc_ui_days|0] active days · CIV=civilian factory · INFRA=infrastructure · AGRI=agriculture',
        'cc_ui_popup_row':'[?v.GetName]'}
    for key,value in labels.items():loc(key,value)
    local.append(defined('cc_ui_sheet_name',[(cv('cc_view_tab','=',3),loc('cc_ui_office_sheet_route','[cc_ui_office_sheet]')),(cv('cc_view_tab','=',4),'cc_tab_catalogue'),(cv('cc_view_tab','=',1),'cc_sheet_contributions'),(cv('cc_view_tab','=',2),'cc_sheet_signatures'),(cv('cc_sheet','=',0),'cc_sheet_overview'),(cv('cc_sheet','=',3),'cc_sheet_effects')],'cc_sheet_terms'))
    local += [defined('cc_ui_picker_heading',[(cv('cc_ui_popup','=',2),'cc_union_label')],'cc_host_label'),
        defined('cc_ui_cycle',[(cv('cc_ui_days','=',180),loc('cc_cycle_180','180 funded days. Benefits run during the programme, beginning on ratification.'))],loc('cc_cycle_90','90 funded days until completion, followed by 90 active days of research or services.'))]
    gui=[MARK+' compact bounded pages, 900 x 580','guiTypes = {'];scripts=[MARK+' private page controls and authoritative agreement actions','scripted_gui = {']
    gui.append(window('cc_toolbar_window','buttonType = { name = "cc_open" position = { x=0 y=0 } spriteType = GFX_cc_toolbar scale = 0.9 shortcut = "shift+c" pdx_tooltip = cc_open_tt }',46,46,788,38))
    opening='cc_initialize = yes if = { limit = { has_global_flag = cc_initialized } if = { limit = { has_country_flag = cc_open } clr_country_flag = cc_open if = { limit = { is_in_array = { array = global.cc_observers value = THIS } } remove_from_array = { global.cc_observers = THIS } } } else = { set_country_flag = cc_open if = { limit = { NOT = { cc_access = yes } NOT = { is_in_array = { array = global.cc_observers value = THIS } } } add_to_array = { global.cc_observers = THIS } } if = { limit = { check_variable = { cc_view_slot < 1 } } set_variable = { cc_view_slot = 1 } } } set_variable = { cc_ui_popup = 0 } cc_ui_refresh = yes cc_touch = yes }'
    scripts.append(sg('cc_toolbar','cc_toolbar_window',parent=None,visible='is_ai = no cc_launcher_access = yes',effects='cc_open_click = { '+opening+' }',properties='cc_open = { x = global.var_missiles_button_x }'))
    root=[icon('cc_logo',24,27,'GFX_cc_header_logo',.65),txt('cc_kicker',85,14,'cc_kicker',590,17,'cc_kicker'),
        txt('cc_title',85,32,'cc_title',610,26,'cc_number'),txt('cc_subtitle',85,57,'cc_subtitle',600,18,'cc_small'),
        grid('cc_header_flags',85,79,450,26,26,45).replace('max_slots_horizontal = 1','max_slots_horizontal = 13'),
        txt('cc_delegation_count',540,14,'cc_ui_member_count',170,18,'cc_tiny'),txt('cc_chair_label',540,58,'cc_chair_label',175,16,'cc_label'),country_flag('cc_chair_flag',540,79),txt('cc_chair_name',588,74,'[cc_chair_current]',127,34,'cc_tiny'),icon('cc_stamp',724,23,'GFX_cc_stamp',.72),
        'buttonType = { name = "cc_close" position = { x=862 y=12 } quadTextureSprite = GFX_cc_close shortcut = ESCAPE }',
        btn('cc_register_projects',20,126,'','GFX_cc_register_tab'),btn('cc_register_joint',110,126,'','GFX_cc_register_tab'),
        txt('cc_projects_label',20,128,'cc_register_projects',84,34,'cc_registertab').replace('format = left','format = center'),
        txt('cc_joint_label',110,128,'cc_register_joint',84,34,'cc_registertab').replace('format = left','format = center'),
        txt('cc_register_caption',24,173,'cc_register_caption',178,18,'cc_registertab'),
        btn('cc_tab_0',230,126,'cc_tab_programme','GFX_cc_tab_104'),btn('cc_tab_1',338,126,'cc_tab_contributions','GFX_cc_tab_135'),btn('cc_tab_2',477,126,'cc_tab_signatures','GFX_cc_tab_112'),btn('cc_tab_3',593,126,'[cc_tab_office_label]','GFX_cc_tab_112',tip='cc_office_tip'),btn('cc_tab_4',709,126,'cc_tab_catalogue','GFX_cc_tab_135'),
        btn('cc_register_previous',20,504,'<','GFX_cc_tiny_button',tip='cc_ui_sidebar_previous'),txt('cc_register_page_label',67,510,'cc_ui_register_page',85,18,'cc_label'),btn('cc_register_next',168,504,'>','GFX_cc_tiny_button',tip='cc_ui_sidebar_next'),
        btn('cc_page_previous',240,501,'<','GFX_cc_tiny_button',tip='cc_ui_turn_previous'),txt('cc_page_label',282,507,'cc_ui_page',536,18,'cc_label'),btn('cc_page_next',838,501,'>','GFX_cc_tiny_button',tip='cc_ui_turn_next'),
        btn('cc_file_previous',20,543,'<','GFX_cc_tiny_button'),btn('cc_file_next',51,543,'>','GFX_cc_tiny_button'),txt('cc_file_selector',86,549,'cc_ui_file_selector',118,18,'cc_label')]
    gui.append(window('cc_main_window','\n'.join(root),W,H,extra='orientation = center origo = center moveable = yes background = { name = "cc_board" quadTextureSprite = GFX_cc_dossier }'))
    gui.append(window('cc_flag_entry',country_flag('cc_flag',0,0),45,26))
    fx=['cc_close_click = { clr_country_flag = cc_open if = { limit = { is_in_array = { array = global.cc_observers value = THIS } } remove_from_array = { global.cc_observers = THIS } } set_variable = { cc_ui_popup = 0 } cc_touch = yes }']
    for name,delta in [('previous',-1),('next',1)]:
        fx.append(f'cc_file_{name}_click = {{ add_to_variable = {{ cc_view_slot = {delta} }} if = {{ limit = {{ check_variable = {{ cc_view_slot < 1 }} }} set_variable = {{ cc_view_slot = 4 }} }} if = {{ limit = {{ check_variable = {{ cc_view_slot > 4 }} }} set_variable = {{ cc_view_slot = 1 }} }} set_variable = {{ cc_sheet = 0 }} set_variable = {{ cc_recipient_page = 0 }} set_variable = {{ cc_delegate_page = 0 }} set_variable = {{ cc_ui_popup = 0 }} cc_ui_refresh = yes cc_touch = yes }}')
        fx.append(f'cc_page_{name}_click = {{ if = {{ limit = {{ check_variable = {{ cc_view_tab = 3 }} }} add_to_variable = {{ cc_office_page = {delta} }} cc_ui_refresh = yes cc_touch = yes }} else_if = {{ limit = {{ check_variable = {{ cc_view_tab = 4 }} }} cc_catalogue_{name} = yes }} else = {{ {turn_page(delta)} }} }}')
        fx.append(f'cc_register_{name}_click = {{ add_to_variable = {{ cc_register_page = {delta} }} clamp_variable = {{ var = cc_register_page min = 0 max = 1 }} cc_ui_refresh = yes cc_touch = yes }}')
    for tab in range(5):fx.append(f'cc_tab_{tab}_click = {{ set_variable = {{ cc_view_tab = {tab} }} set_variable = {{ cc_ballot_view_round = global.cc_ballot_round }} set_variable = {{ cc_office_page = 0 }} set_variable = {{ cc_office_help = 0 }} set_variable = {{ cc_sheet = 0 }} set_variable = {{ cc_recipient_page = 0 }} set_variable = {{ cc_delegate_page = 0 }} set_variable = {{ cc_ui_popup = 0 }} cc_ui_refresh = yes cc_touch = yes }}')
    for register,name in [(0,'projects'),(1,'joint')]:fx.append(f'cc_register_{name}_click = {{ set_variable = {{ cc_register = {register} }} set_variable = {{ cc_register_page = 0 }} cc_ui_refresh = yes cc_touch = yes }}')
    tr=['cc_chair_flag_visible = { cc_chair_alive = yes }','cc_stamp_visible = { check_variable = { cc_view_tab < 3 } }','cc_page_previous_click_enabled = { check_variable = { cc_ui_leaf > 1 } }','cc_page_next_click_enabled = { check_variable = { cc_ui_leaf < cc_ui_leaves } }',
        'cc_register_previous_click_enabled = { check_variable = { cc_register_page > 0 } }','cc_register_next_click_enabled = { check_variable = { cc_register_page < 1 } }']
    props='cc_chair_flag = { image = "[?cc_ui_chair.GetFlag]" } cc_flag = { image = "[THIS.GetFlag]" } cc_stamp = { frame = cc_ui_stamp } '+' '.join(f'cc_tab_{j} = {{ frame = cc_ui_tab_frame_{j} }}' for j in range(5))+' cc_register_projects = { frame = cc_ui_register_frame_0 } cc_register_joint = { frame = cc_ui_register_frame_1 }'
    scripts.append(sg('cc_main','cc_main_window',parent=None,visible='is_ai = no has_global_flag = cc_initialized has_country_flag = cc_open',effects='\n'.join(fx),triggers='\n'.join(tr),properties=props,lists='cc_header_flags = { array = cc_ui_header_flags entry_container = cc_flag_entry change_scope = yes }'))
    short=['INTERMETAL','AGROMASH','INTERKHIM','WAGON POOL','POWER GRID','IKARUS','SCIENTIFIC INFO.','INTERATOMENERGO','BEARINGS','TEXTILE MACH.','RECOVERY','MATERIALS SUPPLY','RESOURCE RECOVERY','PRODUCTION PLANNING','STANDARDISATION','LABOUR PRODUCTIVITY','QUALITY CONTROL','POWER MAINTENANCE','FUEL ECONOMY','AGRICULTURAL EXTENSION','INFRASTRUCTURE TEAMS','SCIENTIFIC EXCHANGE']
    subs=['Metallurgy','Agricultural machinery','Chemical industry','Railway co-operation','Power interconnection','Vehicle production','Computing services','Civil nuclear support','Precision engineering','Textile machinery','Industrial reclamation','Resource allocation','Developed deposits','Production planning','Equipment standards','Technical training','Testing and inspection','Power maintenance','Fuel conservation','Agricultural advice','Shared engineering','Computing research']
    for s in range(1,5):
        for group in range(2):
            for leaf in range(2):
                body=[];actions=[];enables=[];properties=[]
                for offset in range(6):
                    idx=group*11+leaf*6+offset
                    if idx>=group*11+11:break
                    p=PROJECTS[idx];i=idx+1;y=offset*50;first=next(j for j,(q,o) in enumerate(OFFERS,1) if p==q)
                    title=textwrap.fill(short[idx],18,break_long_words=False);loc('cc_register_name_'+p,title);loc('cc_register_sub_'+p,subs[idx]);loc('cc_register_tip_'+p,DATA['catalogue'][p]['title']+'\n'+DATA['catalogue'][p]['description'])
                    body += [btn(f'cc_{s}_choose_'+p,0,y,'','GFX_cc_register_row',tip='cc_register_tip_'+p),icon('cc_mark_'+p,5,y+9,'GFX_cc_project_symbols',.667,frame=i),txt('cc_name_'+p,44,y+5,'cc_register_name_'+p,133,36 if '\n' in title else 20,'cc_registertab')]
                    if '\n' not in title:body.append(txt('cc_sub_'+p,44,y+25,'cc_register_sub_'+p,133,18,'cc_tiny'))
                    actions.append(f'cc_{s}_choose_'+p+'_click = { '+f'set_variable = {{ cc_catalog_offer = {first} }} set_variable = {{ cc_ui_popup = 0 }} set_variable = {{ cc_view_tab = 4 }} cc_ui_refresh = yes cc_touch = yes'+' }')
                    properties.append(f'cc_{s}_choose_{p} = {{ frame = cc_ui_project_frame_{i} }}')
                name=f'cc_{s}_register_{group}_{leaf}';gui.append(window(name,'\n'.join(body),182,300,20,194,'clipping = yes'))
                scripts.append(sg(name,name,visible=cv('cc_view_slot','=',s)+' '+cv('cc_register','=',group)+' '+cv('cc_register_page','=',leaf),effects=' '.join(actions),triggers=' '.join(enables),properties=' '.join(properties)))
    for s in range(1,5):
        body=[heading(s),txt('cc_host_label',18,108,'cc_host_label',300,16,'cc_label'),txt('cc_scale_label',340,108,'cc_scale_label',300,16,'cc_label'),
            btn('cc_host',18,120,'','GFX_cc_field_300'),country_flag('cc_host_flag',20,126),txt('cc_host_value',70,125,'cc_ui_host',231,22,'cc_country'),
            btn('cc_scale',340,120,'','GFX_cc_field_300'),txt('cc_scale_value',342,125,'[cc_ui_scale]',280,22,'cc_country'),
            txt('cc_union_label',18,158,'cc_union_label',INNER,16,'cc_label'),btn('cc_union',18,170,'','GFX_cc_field_622'),country_flag('cc_union_flag',20,176),txt('cc_union_value',70,175,'cc_ui_union',550,22,'cc_country'),
            icon('cc_totals_rule',18,211,'GFX_cc_line_622'),txt('cc_total_label',18,219,'cc_total_label',196,16,'cc_label'),txt('cc_days_label',232,219,'cc_days_label',196,16,'cc_label'),txt('cc_rate_label',446,219,'cc_rate_label',194,16,'cc_label'),
            txt('cc_total_value',18,238,'cc_ui_cost',196,28,'cc_number'),txt('cc_days_value',232,238,'cc_ui_days',196,28,'cc_number'),txt('cc_rate_value',446,238,'cc_ui_weekly',194,28,'cc_number'),
            txt('cc_host_delivery',18,273,f'[cc_{s}_delivery]',INNER,25,'cc_tiny'),txt('cc_host_requires',18,301,f'[cc_{s}_host_requires]',INNER,36,'cc_tiny')]
        actions=[];enables=[]
        for field,popup in [('host',1),('union',2),('scale',3)]:
            actions.append(f'cc_{field}_click = {{ if = {{ limit = {{ cc_{s}_editable = yes }} set_variable = {{ cc_ui_popup = {popup} }} set_variable = {{ cc_ui_choice_page = 0 }} cc_ui_choices = yes cc_ui_refresh = yes cc_touch = yes }} }}');enables.append(f'cc_{field}_click_enabled = {{ cc_{s}_editable = yes }}')
        name=f'cc_overview_{s}';gui.append(page(name,'\n'.join(body)))
        scripts.append(sg(name,name,visible=cv('cc_view_slot','=',s)+' '+cv('cc_view_tab','=',0)+' '+cv('cc_sheet','=',0),effects=' '.join(actions),triggers=' '.join(enables),properties='cc_page_mark = { frame = cc_ui_project } cc_host_flag = { image = "[?cc_ui_host.GetFlag]" } cc_union_flag = { image = "[?cc_ui_union.GetFlag]" }'))
        for leaf in range(2):
            body=[heading(s,False),txt('cc_terms_heading',18,82,'cc_terms_heading',INNER,22,'cc_registertab')];actions=[];enables=[];props=['cc_page_mark = { frame = cc_ui_project }']
            for row in range(2):
                j=leaf*2+row;y=106+row*84
                body += [btn(f'cc_offer_{j}',18,y,'','GFX_cc_offer'),icon(f'cc_offer_icon_{j}',52,y+8,'GFX_cc_offer_symbols',.77419),txt(f'cc_offer_title_{j}',85,y+11,f'[cc_{s}_offer_name_{j}]',539,20,'cc_registertab'),txt(f'cc_offer_summary_{j}',52,y+35,f'[cc_{s}_offer_summary_{j}]',570,40,'cc_small')]
                cases=[]
                for p in PROJECTS:
                    family=[i for i,(q,o) in enumerate(OFFERS,1) if q==p]
                    if j<len(family):cases.append(f'if = {{ limit = {{ cc_{s}_editable = yes OR = {{ '+' '.join(cv(f'global.cc_{s}_offer','=',i) for i in family)+f' }} }} set_variable = {{ global.cc_{s}_offer = {family[j]} }} cc_{s}_revise = yes }}')
                actions.append(f'cc_offer_{j}_click = {{ '+' '.join(cases)+' }');enables.append(f'cc_offer_{j}_click_enabled = {{ cc_{s}_editable = yes }}')
                for element in [f'cc_offer_{j}',f'cc_offer_icon_{j}',f'cc_offer_title_{j}',f'cc_offer_summary_{j}']:enables.append(f'{element}_visible = {{ check_variable = {{ cc_ui_offer_count > {j} }} }}')
                props += [f'cc_offer_{j} = {{ frame = cc_ui_offer_frame_{j} }}',f'cc_offer_icon_{j} = {{ frame = cc_ui_offer_icon_{j} }}']
            body += [txt('cc_cycle',18,270,'[cc_ui_cycle]',INNER,30,'cc_tiny'),txt('cc_requirements',18,302,f'[cc_{s}_requirements]',INNER,36,'cc_tiny')]
            name=f'cc_terms_{s}_{leaf}';gui.append(page(name,'\n'.join(body)))
            scripts.append(sg(name,name,visible=cv('cc_view_slot','=',s)+' '+cv('cc_view_tab','=',0)+' '+cv('cc_sheet','=',leaf+1),effects=' '.join(actions),triggers=' '.join(enables),properties=' '.join(props)))
        # All eight initial delegations fit on one sheet. Expanded memberships retain page turns.
        card=[country_flag('cc_card_flag',0,6),txt('cc_card_name',48,1,'cc_ui_card_name',144,38,'cc_tiny'),txt('cc_card_effects',202,1,f'[cc_{s}_card_compact]',300,38,'cc_registertab'),txt('cc_card_fees',514,1,f'[cc_{s}_card_compact_fees]',108,38,'cc_tiny'),icon('cc_card_rule',0,37,'GFX_cc_line_622')]
        gui.append(window(f'cc_recipient_{s}','\n'.join(card),INNER,38))
        body=[txt('cc_effects_timing',18,1,'cc_effects_timing',INNER,18,'cc_tiny'),txt('cc_effects_country',18,19,'cc_effects_country',192,17,'cc_registertab'),txt('cc_effects_benefits',220,19,'cc_effects_benefits',300,17,'cc_registertab'),txt('cc_effects_costs',532,19,'cc_effects_costs',108,17,'cc_registertab'),grid('cc_effects_list',18,36,INNER,304,38,INNER),txt('cc_empty_list',18,62,'cc_ui_empty',INNER,40,'cc_small')]
        name=f'cc_effects_{s}';gui.append(page(name,'\n'.join(body)))
        scripts.append(sg(name,name,visible=cv('cc_view_slot','=',s)+' '+cv('cc_view_tab','=',0)+' '+cv('cc_sheet','=',3),properties='cc_card_flag = { image = "[THIS.GetFlag]" }',triggers='cc_empty_list_visible = { check_variable = { cc_ui_recipient_count = 0 } }',lists=f'cc_effects_list = {{ array = cc_ui_recipients entry_container = cc_recipient_{s} change_scope = yes }}'))
        normal=loc(f'cc_{s}_contribution_amount',f'[?cc_{s}_share|0]% · $[?cc_{s}_weekly|3]B/week')
        local.append(defined(f'cc_{s}_contribution_line',[('is_ai = yes',loc('cc_passive_funding','Passive · no capital contribution'))],normal))
        for tab,kind in [(1,'contributions'),(2,'signatures')]:
            row=[country_flag('cc_delegate_flag',0,5),txt('cc_delegate_name',50,3,'[THIS.GetName]',335,22,'cc_country')]
            if tab==1:row += [txt('cc_delegate_share',396,4,f'[cc_{s}_contribution_line]',226,22,'cc_registertab'),icon('cc_funding_bar',0,28,'GFX_cc_funding',622/670)]
            else:row += [txt('cc_delegate_share',40,27,f'[cc_{s}_contribution_line]',345,20,'cc_registertab'),txt('cc_delegate_status',399,16,f'[cc_{s}_vote_status]',223,24,'cc_registertab')]
            row.append(icon('cc_delegate_rule',0,53,'GFX_cc_line_622'));gui.append(window(f'cc_{kind}_row_{s}','\n'.join(row),INNER,54))
            body=[heading(s,False),txt('cc_list_heading',18,68,'cc_'+kind+'_heading',INNER,20,'cc_registertab'),txt('cc_list_note',18,88,'cc_'+kind+'_note',INNER,32,'cc_tiny'),grid('cc_delegates',18,124,INNER,216,54,INNER)]
            name=f'cc_{kind}_{s}';gui.append(page(name,'\n'.join(body)))
            scripts.append(sg(name,name,visible=cv('cc_view_slot','=',s)+' '+cv('cc_view_tab','=',tab),properties='cc_delegate_flag = { image = "[THIS.GetFlag]" } '+(f'cc_funding_bar = {{ frame = cc_{s}_funding_frame }}' if tab==1 else ''),lists=f'cc_delegates = {{ array = cc_ui_delegates entry_container = cc_{kind}_row_{s} change_scope = yes }}'))
    from controls import compile_controls,compile_pickers
    compile_controls(gui,scripts,local)
    compile_pickers(gui,scripts)
    from council_ui import compile_office
    compile_office(gui,scripts,local)
    gui.append('}');scripts.append('}')
    write('interface/ICW_COMECON.gui','\n'.join(gui));write('common/scripted_guis/ICW_COMECON.txt','\n'.join(scripts));write('common/scripted_localisation/ICW_COMECON.txt',MARK+' paged dossier text\n'+'\n'.join(local))
