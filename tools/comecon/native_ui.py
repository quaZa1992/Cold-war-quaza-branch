# IMPERIA COLD WAR — COMECON faithful native port of the approved dossier
from build import *
from view import compile_view,defined,reward_lines

def txt(name,x,y,value,width,height=21,font='cc_body'):
    return f'instantTextboxType = {{ name = "{name}" position = {{ x={x} y={y} }} text = "{value}" font = "{font}" maxWidth = {width} maxHeight = {height} fixedsize = yes format = left alwaystransparent = yes }}'

def icon(name,x,y,sprite,scale=1,frame=None):
    return f'iconType = {{ name = "{name}" position = {{ x={x} y={y} }} spriteType = {sprite} scale = {n(scale)}'+(f' frame = {frame}' if frame is not None else '')+' alwaystransparent = yes }'

def country_flag(name,x,y):
    return f'iconType = {{ name = "{name}" position = {{ x={x} y={y} }} quadTextureSprite = GFX_flag_small2 scale = 0.73 alwaystransparent = yes }}'

def btn(name,x,y,value,sprite,font='cc_button',tip=None):
    return f'buttonType = {{ name = "{name}" position = {{ x={x} y={y} }} quadTextureSprite = {sprite} buttonFont = {font} buttonText = "{value}" clicksound = click_default'+(f' pdx_tooltip = {tip}' if tip else '')+' }'

def grid(name,x,y,w,h,row,slotwidth=None):
    return f'gridboxType = {{ name = "{name}" position = {{ x={x} y={y} }} size = {{ width={w} height={h} }} slotsize = {{ width={slotwidth or w} height={row} }} max_slots_horizontal = 1 format = "UPPER_LEFT" }}'

def window(name,body,w=720,h=1700,x=0,y=0,extra=''):
    return f'containerWindowType = {{ name = "{name}" position = {{ x={x} y={y} }} size = {{ width={w} height={h} }} {extra}\n'+body+'\n}'

def dispatch(fn):
    return ' '.join(f'if = {{ limit = {{ hidden_trigger = {{ {cv("cc_view_slot","=",s)} }} }} {fn(s)} }}' for s in range(1,5))

def sg(name,win,body='',parent='cc_main',visible='',effects='',triggers='',properties='',lists=''):
    return f'{name} = {{ context_type = player_context window_name = "{win}" '+(f'parent_scripted_gui = {parent} ' if parent else '')+f'dirty = global.cc_dirty ai_enabled = {{ always = no }} visible = {{ {visible} }} '+(f'effects = {{ {effects} }} ' if effects else '')+(f'triggers = {{ {triggers} }} ' if triggers else '')+(f'properties = {{ {properties} }} ' if properties else '')+(f'dynamic_lists = {{ {lists} }} ' if lists else '')+body+' }'

def paper_heading(s):
    return '\n'.join([icon('cc_page_mark',25,23,'GFX_cc_project_large'),
        txt('cc_page_file',110,23,'[cc_ui_file_heading]',580,16,'cc_label'),
        txt('cc_page_title',110,44,f'[cc_{s}_programme_name]',585,32,'cc_heading'),
        txt('cc_page_description',110,82,f'[cc_{s}_description]',500,40,'cc_small'),
        icon('cc_heading_rule',0,134,'GFX_cc_line_720')])

def register_text():
    local=compile_view()
    labels={'cc_empty':'','cc_title':'Council for Mutual\\nEconomic Assistance','cc_subtitle':'Consult the Catalogue to refer a programme to the chair.',
        'cc_kicker':'SECRETARIAT · MOSCOW','cc_register_projects':'Investment\\nprojects','cc_register_joint':'Joint\\nprogrammes',
        'cc_register_caption':'[cc_ui_register_caption]','cc_caption_projects':'PROJECT REGISTER\\n90 DAYS','cc_caption_joint':'JOINT PROGRAMMES\\n180 DAYS',
        'cc_tab_programme':'Programme','cc_tab_contributions':'Contributions','cc_tab_signatures':'Signatures',
        'cc_open_tt':'COMECON\\nJoint investment and technical co-operation.\\nShift+C',
        'cc_host_label':'01 / HOST COUNTRY','cc_coordinator_label':'01 / CO-ORDINATING COUNTRY','cc_scale_label':'02 / INVESTMENT SCALE',
        'cc_union_label':'03 / SOVIET PROGRAMME RECIPIENT','cc_total_label':'TOTAL BUDGET','cc_days_label':'FUNDED PROJECT','cc_rate_label':'JOINT WEEKLY COST',
        'cc_ui_cost':'$[?cc_ui_cost|2]B','cc_ui_days':'[?cc_ui_days|0] days','cc_ui_weekly':'$[?cc_ui_weekly|3]B',
        'cc_ui_host':'[?cc_ui_host.GetName]','cc_ui_union':'[?cc_ui_union.GetName]',
        'cc_ui_union_note':'Soviet delegation: one agreed programme recipient, with one Council vote.',
        'cc_terms_heading':'04 / AGREEMENT TERMS · SELECT ONE OFFER','cc_outcomes_heading':'05 / PROSPECTIVE EFFECTS BY COUNTRY',
        'cc_contributions_heading':'04 / NATIONAL CONTRIBUTIONS','cc_signatures_heading':'04 / COUNCIL SIGNATURES',
        'cc_contributions_note':'Each financing government offers its own share. Contributions are fixed during Council review.',
        'cc_signatures_note':'Review Terms, then sign the sealed agreement. Passive recipients need no Council signature.',
        'cc_ui_coverage':'Financing schedule: [?cc_ui_coverage|0]% covered.',
        'cc_ui_own_share':'Your contribution: [?cc_ui_share|0]% · $[?cc_ui_own_weekly|3]B/week',
        'cc_ui_file_selector':'CONTRACT FILE [?cc_view_slot|0] / 4','cc_ui_actor':'[THIS.GetFlag]  [THIS.GetName]',
        'cc_ui_preview':'Agreed Effects','cc_ui_ratify':'Ratify Agreement','cc_ui_reset':'New Draft','cc_ui_resume':'Resume Funding',
        'cc_ui_approve':'Approve','cc_ui_decline':'Decline','cc_ui_local':'Confirm Local Implementation','cc_plus':'+5%','cc_minus':'-5%',
        'cc_limited':'Limited programme','cc_standard':'Standard programme','cc_major':'Major programme',
        'cc_ui_file_number':'CMEA / [cc_ui_sector] / FILE [?cc_ui_project|02] · REV. [?cc_ui_revision|0]',
        'cc_ui_popup_row':'[?v.GetFlag]  [?v.GetName]','cc_ui_card_name':'[THIS.GetName]',
        'cc_ui_footer_draft':'Working copy. Select the host, contribution schedule and agreement terms.',
        'cc_ui_footer_active':'[cc_ui_phase_name] · [?cc_ui_remaining|0] active days remaining.',
        'cc_ui_preview_tt':'[cc_ui_requirements]\\n\\n§HEffects:§!\\n[!cc_ui_preview_click]',
        'cc_ui_ratify_tt':'§HPrerequisites:§!\\n[!cc_ui_ratify_click_enabled]\\n[cc_ui_requirements]\\n\\n§HEffects:§!\\n[!cc_ui_ratify_click]',
        'cc_ui_approve_tt':'[cc_ui_requirements]\\n\\n§HAgreed Effects:§!\\n[!cc_ui_approve_click]',
        'cc_ui_decline_tt':'Decline the current agreement.',
        'cc_weekly_cost_tt':'Weekly contribution: $[?cc_preview_weekly|+3]B',
        'cc_weekly_support_tt':'Weekly programme support: $[?cc_preview_weekly|+3]B',
        'cc_weekly_gdp_tt':'Weekly national programme cost: [?cc_preview_gdp|%+3] of GDP',
        'cc_active_days_tt':'Programme duration: [?cc_preview_days|0] active days',
        'cc_secretariat_tt':'The presiding delegation submits and ratifies Council agreements.',
        'cc_human_funder_tt':'At least one participating government provides the financing.',
        'cc_ready_sites_tt':'All agreed recipient sites meet the programme requirements.',
        'cc_reviewed_terms_tt':'The current sealed terms have been reviewed.',
        'cc_financing_covered_tt':'The agreed contributions cover exactly 100% of the budget.',
        'cc_two_delegations_tt':'At least two national delegations participate.',
        'cc_signed_sites_tt':'All required signatures, local confirmations, eligible programme sites and agreed delivery stocks are secured.'}
    for k,v in labels.items():loc(k,v)
    local += [defined('cc_ui_register_caption',[(cv('cc_register','=',1),'cc_caption_joint')],'cc_caption_projects'),
        defined('cc_ui_scale',[(cv('cc_ui_tier','=',2),'cc_standard'),(cv('cc_ui_tier','=',3),'cc_major')],'cc_limited'),
        defined('cc_ui_footer',[(cv('cc_ui_phase','>',1),'cc_ui_footer_active')],'cc_ui_footer_draft')]
    for getter in ['requirements','programme_name','description']:
        local.append(defined('cc_ui_'+getter,[(cv('cc_view_slot','=',s),loc(f'cc_ui_route_{getter}_{s}',f'[cc_{s}_{getter}]')) for s in range(1,5)]))
    local.append(defined('cc_ui_phase_name',[(cv('cc_ui_phase','=',i),loc(f'cc_phase_{i}',name)) for i,name in enumerate(['Draft','Council Review','Funded Implementation','Partner Programmes','Completed'])]))
    local.append(defined('cc_ui_sector',[(cv('cc_ui_project','=',i),loc('cc_sector_'+p,DATA['catalogue'][p]['sector'])) for i,p in enumerate(PROJECTS,1)]))
    local.append(defined('cc_ui_file_heading',[(cv('cc_ui_project','=',i),loc('cc_file_heading_'+p,f'CMEA / {DATA["catalogue"][p]["sector"]} / FILE {DATA["catalogue"][p]["file"]} · REV. [?cc_ui_revision|0]')) for i,p in enumerate(PROJECTS,1)]))
    return local

def compile_ui():
    from compact_ui import compile_compact_ui
    compile_compact_ui()
