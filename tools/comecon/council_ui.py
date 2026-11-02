# IMPERIA COLD WAR — COMECON Council office, public catalogue and agenda correspondence
from native_ui import *
from view import native_wrap,reward_lines,service_rates
from pagination import slice_array,page_count


def compile_office_view():
    body=['save_event_target_as = cc_ui_viewer','set_variable = { cc_ui_chair = THIS.id } if = { limit = { cc_chair_alive = yes } set_variable = { cc_ui_chair = global.cc_chair } }',
        'if = { limit = { NOT = { has_variable = cc_office_page } } set_variable = { cc_office_page = 0 } } if = { limit = { NOT = { has_variable = cc_office_help } } set_variable = { cc_office_help = 0 } }',
        'if = { limit = { NOT = { has_variable = cc_catalog_offer } } set_variable = { cc_catalog_offer = 1 } }',
        f'clamp_variable = {{ var = cc_catalog_offer min = 1 max = {len(OFFERS)} }}',
        'if = { limit = { NOT = { has_variable = cc_catalog_tier } } set_variable = { cc_catalog_tier = 1 } } clamp_variable = { var = cc_catalog_tier min = 1 max = 3 }']
    for i,(p,o) in enumerate(OFFERS,1):
        family=[j for j,(q,r) in enumerate(OFFERS,1) if q==p]
        body.append(choose('cc_catalog_offer',i,var('cc_catalog_project',PROJECTS.index(p)+1)+' '+var('cc_catalog_choice',family.index(i)+1)+' '+var('cc_catalog_choices',len(family))))
    body += ['clear_array = cc_ui_agenda_all for_each_scope_loop = { array = global.cc_members if = { limit = { cc_human_member = yes check_variable = { cc_agenda_pending = 1 } } event_target:cc_ui_viewer = { add_to_array = { cc_ui_agenda_all = PREV } } } }',
        page_count('global.cc_ballot_candidates^num','cc_ui_candidate_pages',8),
        page_count('cc_ui_agenda_all^num','cc_ui_agenda_pages',4),
        var('cc_ui_office_pages','cc_ui_candidate_pages'),'add_to_variable = { cc_ui_office_pages = cc_ui_agenda_pages }',
        var('cc_ui_office_max','cc_ui_office_pages'),'subtract_from_variable = { cc_ui_office_max = 1 }',
        'clamp_variable = { var = cc_office_page min = 0 max = cc_ui_office_max }',
        'clear_array = cc_ui_candidates clear_array = cc_ui_requests',
        'if = { limit = { check_variable = { cc_office_page < cc_ui_candidate_pages } } set_variable = { cc_office_sheet = 0 } '+slice_array('global.cc_ballot_candidates','cc_ui_candidates','cc_office_page',8)+' } else = { set_variable = { cc_office_sheet = 1 } '+var('cc_ui_request_page','cc_office_page')+' subtract_from_variable = { cc_ui_request_page = cc_ui_candidate_pages } '+slice_array('cc_ui_agenda_all','cc_ui_requests','cc_ui_request_page',4)+' }',
        'if = { limit = { check_variable = { cc_view_tab = 3 } } '+var('cc_ui_leaf','cc_office_page')+' add_to_variable = { cc_ui_leaf = 1 } '+var('cc_ui_leaves','cc_ui_office_pages')+' }',
        'if = { limit = { check_variable = { cc_view_tab = 4 } } '+var('cc_ui_leaf','cc_catalog_choice')+' '+var('cc_ui_leaves','cc_catalog_choices')+' '+var('cc_ui_project','cc_catalog_project')+' }']
    body.append('if = { limit = { check_variable = { cc_view_tab = 3 } check_variable = { cc_office_help = 1 } } set_variable = { cc_ui_leaf = 1 } set_variable = { cc_ui_leaves = 1 } }')
    return block('cc_office_refresh','\n'.join(body))


def compile_office(gui,scripts,local):
    from compact_ui import page
    labels={
      'cc_tab_office':'Council','cc_tab_catalogue':'Catalogue','cc_office_tip':'[cc_ballot_status]\n\nPresiding delegation: [cc_chair_current]. Consult the electoral register and correspondence of the delegations.',
      'cc_chair_label':'PRESIDING DELEGATION','cc_chair_name':'[?global.cc_chair.GetName]',
      'cc_chair_vacant':'No accredited delegation','cc_office_kicker':'CMEA / COUNCIL OFFICE',
      'cc_office_title':'Election of the Presiding Delegation',
      'cc_ballot_guide':'Select a national flag to lodge your delegation\'s ballot. The seal is final. The largest tally appoints the chair.',
      'cc_ballot_open_text':'Ballots close in [?global.cc_ballot_days_left|0] days · [?global.cc_ballots_received|0] ballots lodged',
      'cc_ballot_closed_text':'The annual ballot is concluded. The next register opens in the new calendar year.',
      'cc_ballot_candidate':'[?v.GetAdjective]','cc_ballot_candidate_tip':'[?v.GetName]\n\nSelect this delegation to lodge your sealed ballot.\n[?v.cc_ballot_tally|0] ballots lodged.','cc_ballot_tally':'[?v.cc_ballot_tally|0] ballots',
      'cc_ballot_selected':'Your ballot is sealed for [?cc_ballot_target.GetName].',
      'cc_ballot_waiting':'The Secretariat awaits your delegation\'s sealed ballot.',
      'cc_ballot_observer':'The electoral register lists the member delegations represented at the opening of this session.',
      'cc_ballot_rules_button':'Rules of Procedure','cc_rules_back':'Return to Council','cc_ballot_receive':'Receive Ballot',
      'cc_ballot_rules':'The Secretariat issues ballots once in each calendar year. Voting remains open for fifteen days. Each accredited member delegation has one vote, irrespective of its capital contribution.\n\nSelect a national flag to seal your ballot. A lodged ballot cannot be replaced. The highest tally appoints the presiding delegation; the outgoing chair remains in office until the count is concluded.\n\nEqual tallies are settled in the Council register\'s order of succession, beginning after the outgoing chair. If no ballots are lodged, that same order supplies the next chair.\n\nOnly delegations represented on the opening register may vote or stand. A delegation that ceases to be represented is excluded from the count. Union republics are represented through the Soviet delegation.\n\nThe presiding delegation prepares agreements and submits them for Council review. Each financing government offers its own contribution and signs the agreed terms. The Secretariat in Moscow maintains the Council\'s records.',
      'cc_agenda_title':'Correspondence of the Delegations','cc_agenda_guide':'Select a referral to examine it. The presiding delegation may prepare it in the chosen working file.',
      'cc_agenda_empty':'No referrals await consideration. Consult the Catalogue to place a programme before the chair.',
      'cc_agenda_sender':'[?v.GetName]','cc_agenda_subject':'[cc_agenda_row_subject]',
      'cc_catalogue_kicker':'CMEA / PROGRAMME CATALOGUE','cc_catalogue_host':'HOST DELIVERY','cc_catalogue_partner':'PARTNER BENEFITS',
      'cc_catalogue_refer':'Request Agenda Item','cc_catalogue_prepare':'Prepare Draft',
      'cc_catalogue_guide':'Consult the schedule, then refer an item to the presiding delegation. Capital is committed only through a signed agreement.',
      'cc_catalogue_requirements':'Requirements','cc_catalogue_requirements_tip':'[cc_catalogue_requirements]','cc_catalogue_footer_hint':'Refer this programme to the chair.','cc_catalogue_referred':'Your referral is recorded. The chair will consider it for a working file.',
      'cc_catalogue_capital_note':'Capital schedule: [cc_catalogue_capital]',
      'cc_catalogue_next':'Next offer','cc_catalogue_previous':'Previous offer',
      'cc_draft_prepare_tt':'The presiding delegation may prepare this programme in an unsigned working file.',
      'cc_agenda_prepare':'Prepare Referral','cc_catalogue_access':'Every delegation may inspect the Catalogue. Refer a programme to the chair for consideration.',
    }
    for k,v in labels.items():loc(k,v)
    for key in ('cc_ballot_guide','cc_agenda_guide','cc_catalogue_guide','cc_agenda_empty','cc_ballot_closed_text','cc_ballot_observer'):
        loc(key,native_wrap(LOCS[key].replace('\\n','\n'),622,11))
    loc('cc_ballot_closed_text',native_wrap(LOCS['cc_ballot_closed_text'].replace('\\n','\n'),460,11,'cour.ttf'))
    local.append(defined('cc_tab_office_label',[(cv('global.cc_ballot_open','=',1),loc('cc_office_vote_label','Council Ballot'))],'cc_tab_office'))
    local.append(defined('cc_chair_current',[('cc_chair_alive = yes','cc_chair_name')],'cc_chair_vacant'))
    local.append(defined('cc_ballot_status',[(cv('global.cc_ballot_open','=',1),'cc_ballot_open_text')],'cc_ballot_closed_text'))
    local.append(defined('cc_ballot_instruction',[(cv('cc_ballot_receipt','=','global.cc_ballot_round')+' '+cv('global.cc_ballot_round','>',0),'cc_ballot_selected'),('cc_ballot_can_vote = yes','cc_ballot_waiting')],'cc_ballot_observer'))
    local.append(defined('cc_ui_office_sheet',[(cv('cc_office_help','=',1),loc('cc_office_rules_name','RULES OF PROCEDURE'))]+[(cv('cc_office_sheet','=',1),loc('cc_office_agenda_name','AGENDA REGISTER'))],loc('cc_office_election_name','ELECTORAL REGISTER')))
    local.append(defined('cc_agenda_row_subject',[(f'var:v = {{ {cv("cc_agenda_offer","=",i)} }}',loc('cc_agenda_subject_'+str(i),DATA['catalogue'][p]['title'])) for i,(p,o) in enumerate(OFFERS,1)]))
    rules='\n\n'.join(native_wrap(p,622,11) for p in LOCS['cc_ballot_rules'].replace('\\n','\n').split('\n\n'))
    loc('cc_rules_body',rules)
    gui.append(page('cc_office_rules',txt('cc_rules_kicker',18,10,'cc_office_kicker',622,16,'cc_label')+txt('cc_rules_heading',18,31,'cc_ballot_rules_button',622,26,'cc_number')+txt('cc_rules_body',18,66,'cc_rules_body',622,268,'cc_tiny')))
    scripts.append(sg('cc_office_rules','cc_office_rules',visible=cv('cc_view_tab','=',3)+' '+cv('cc_office_help','=',1)))
    candidate=[icon('cc_ballot_tile',0,0,'GFX_cc_ballot_tile'),icon('cc_ballot_seal',0,0,'GFX_cc_ballot_seal'),
      btn('cc_ballot_flag',54,4,'','GFX_flag_small2',tip='cc_ballot_candidate_tip'),country_flag('cc_ballot_chosen_flag',54,4),
      txt('cc_candidate_name',4,34,'cc_ballot_candidate',140,26,'cc_tiny'),txt('cc_candidate_tally',4,60,'cc_ballot_tally',140,14,'cc_label')]
    gui.append(window('cc_ballot_entry','\n'.join(candidate),148,74))
    body=[txt('cc_office_kicker',18,10,'cc_office_kicker',622,16,'cc_label'),txt('cc_office_title',18,31,'cc_office_title',622,26,'cc_number'),
      txt('cc_ballot_guide',18,65,'cc_ballot_guide',622,40,'cc_tiny'),txt('cc_ballot_status',18,118,'[cc_ballot_status]',460,32,'cc_registertab'),
      btn('cc_ballot_rules',490,111,'cc_ballot_rules_button','GFX_cc_action_150','cc_registertab',tip='cc_ballot_rules'),
      grid('cc_ballot_list',18,154,622,152,76,153).replace('max_slots_horizontal = 1','max_slots_horizontal = 4'),
      txt('cc_ballot_instruction',18,315,'[cc_ballot_instruction]',622,24,'cc_tiny')]
    gui.append(page('cc_office_election','\n'.join(body)))
    chosen='check_variable = { cc_ballot_receipt = global.cc_ballot_round } check_variable = { cc_ballot_target = v }'
    scripts.append(sg('cc_office_election','cc_office_election',visible=cv('cc_view_tab','=',3)+' '+cv('cc_office_help','=',0)+' '+cv('cc_office_sheet','=',0),
      effects='cc_ballot_rules_click = { set_variable = { cc_office_help = 1 } cc_ui_refresh = yes cc_touch = yes } cc_ballot_flag_click = { set_variable = { cc_ballot_proposed = v } cc_ballot_cast = yes }',
      triggers='cc_ballot_flag_click_enabled = { cc_ballot_can_vote = yes check_variable = { cc_ballot_view_round = global.cc_ballot_round } var:v = { cc_human_member = yes } } cc_ballot_chosen_flag_visible = { '+chosen+' } cc_ballot_seal_visible = { '+chosen+' }',
      properties='cc_ballot_flag = { image = "[?v.GetFlag]" } cc_ballot_chosen_flag = { image = "[?v.GetFlag]" }',
      lists='cc_ballot_list = { array = cc_ui_candidates entry_container = cc_ballot_entry change_scope = no }'))
    row=btn('cc_referral_select',0,0,'','GFX_cc_agenda_row')+icon('cc_referral_selection',0,0,'GFX_cc_agenda_selection')+country_flag('cc_referral_flag',5,7)+txt('cc_referral_sender',55,4,'cc_agenda_sender',550,20,'cc_country')+txt('cc_referral_subject',55,28,'[cc_agenda_row_subject]',550,22,'cc_tiny')
    gui.append(window('cc_referral_entry',row,622,56))
    body=[txt('cc_agenda_kicker',18,10,'cc_office_kicker',622,16,'cc_label'),txt('cc_agenda_title',18,31,'cc_agenda_title',622,26,'cc_number'),txt('cc_agenda_guide',18,65,'cc_agenda_guide',622,36,'cc_tiny'),grid('cc_referrals',18,110,622,224,56),txt('cc_agenda_empty',18,118,'cc_agenda_empty',622,40,'cc_small')]
    gui.append(page('cc_office_agenda','\n'.join(body)))
    scripts.append(sg('cc_office_agenda','cc_office_agenda',visible=cv('cc_view_tab','=',3)+' '+cv('cc_office_help','=',0)+' '+cv('cc_office_sheet','=',1),
      effects='cc_referral_select_click = { if = { limit = { var:v = { cc_human_member = yes check_variable = { cc_agenda_pending = 1 } } } set_variable = { cc_agenda_selected = v } var:v = { set_variable = { PREV.cc_agenda_selected_revision = cc_agenda_revision } } cc_touch = yes } }',
      triggers='cc_agenda_empty_visible = { check_variable = { cc_ui_agenda_all^num = 0 } } cc_referral_selection_visible = { check_variable = { cc_agenda_selected = v } cc_agenda_selection_valid = yes }',properties='cc_referral_flag = { image = "[?v.GetFlag]" }',
      lists='cc_referrals = { array = cc_ui_requests entry_container = cc_referral_entry change_scope = no }'))
    gui.append(window('cc_office_footer',btn('cc_receive_ballot',0,0,'cc_ballot_receive','GFX_cc_action_140')+btn('cc_rules_back',0,0,'cc_rules_back','GFX_cc_action_150')+txt('cc_office_footer_note',150,6,'cc_catalogue_access',482,26,'cc_tiny'),640,35,240,541))
    scripts.append(sg('cc_office_footer','cc_office_footer',visible=cv('cc_view_tab','=',3),effects='cc_rules_back_click = { set_variable = { cc_office_help = 0 } cc_ui_refresh = yes cc_touch = yes } cc_receive_ballot_click = { if = { limit = { cc_ballot_can_vote = yes } set_variable = { cc_ballot_view_round = global.cc_ballot_round } cc_touch = yes } }',triggers='cc_rules_back_visible = { check_variable = { cc_office_help = 1 } } cc_receive_ballot_visible = { check_variable = { cc_office_help = 0 } check_variable = { cc_office_sheet = 0 } cc_ballot_can_vote = yes NOT = { check_variable = { cc_ballot_view_round = global.cc_ballot_round } } } cc_office_footer_note_visible = { check_variable = { cc_office_help = 0 } check_variable = { cc_office_sheet = 0 } }'))
    compile_catalogue(gui,scripts,local)
    paging=[]
    for direction,delta in [('previous',-1),('next',1)]:
        cases=[]
        for i,(p,o) in enumerate(OFFERS,1):
            family=[j for j,(q,r) in enumerate(OFFERS,1) if q==p];index=family.index(i)+delta
            if 0<=index<len(family):cases.append(('if' if not cases else 'else_if')+f' = {{ limit = {{ {cv("cc_catalog_offer","=",i)} }} set_variable = {{ cc_catalog_offer = {family[index]} }} }}')
        paging.append(block('cc_catalogue_'+direction,' '.join(cases)+' cc_ui_refresh = yes cc_touch = yes'))
    write('common/scripted_effects/ICW_COMECON_office_view.txt',MARK+' presentation caches only\n'+compile_office_view()+'\n'.join(paging))


def compile_catalogue(gui,scripts,local):
    from compact_ui import page
    fields={k:[] for k in ('title','description','offer','host','partner','capital','requirements','host_fees','partner_fees')}
    for i,(p,o) in enumerate(OFFERS,1):
        cond=cv('cc_catalog_offer','=',i)
        for key,text in [('title',DATA['catalogue'][p]['title']),('description',native_wrap(DATA['catalogue'][p]['description'],622,11)),('offer',o['name'])]:
            fields[key].append((cond,loc(f'cc_cat_{key}_{i}',text)))
        for t in range(3):
            condition=cond+' '+cv('cc_catalog_tier','=',t+1)
            for host,key in [(True,'host'),(False,'partner')]:
                lines=reward_lines(1,p,o,t,host)
                if o['kind']=='equipment':lines[-1]=f'Train transfer: {t+1} per 5% partner contribution'
                lines=[text.replace('[?cc_1_site1.GetName]','one eligible steel-producing state') for text in lines]
                text='\n'.join(native_wrap(line,298,11) for line in lines)
                fields[key].append((condition,loc(f'cc_cat_{key}_{i}_{t}',text)))
                national,support=service_rates(p,o,t,host)
                fees=[]
                if national:fees.append(f'Administration: -{national:.3f}% GDP/week')
                if support:fees.append(f'Technical services: -${support}M/week')
                fields[key+'_fees'].append((condition,loc(f'cc_cat_{key}_fees_{i}_{t}','\n'.join(fees))))
            base=(o.get('base') or DATA['catalogue'][p]['cost'])[t]/1000
            same=o['kind']=='shared' or o.get('all') or o.get('includeHost')
            fields['capital'].append((condition,loc(f'cc_cat_capital_{i}_{t}',f'${base:g}B fixed + ${o["extra"][t]/1000:g}B per '+('recipient' if same else 'partner'))))
            requirement=o['requires'].replace('[states]',str(t+1)).replace('state(s)','states')
            if p in DATA['hostPlans']:requirement+='\nHost: '+DATA['hostPlans'][p]['requires'].replace('[states]',str(t+1)).replace('state(s)','states')
            if o['kind']=='equipment':requirement+='\nThe supplying delegation provides its agreed deliveries from existing train stock.'
            fields['requirements'].append((condition,loc(f'cc_cat_require_{i}_{t}',requirement)))
    for key,cases in fields.items():local.append(defined('cc_catalogue_'+key,cases))
    body=[txt('cc_catalogue_kicker',18,10,'cc_catalogue_kicker',622,16,'cc_label'),txt('cc_catalogue_title',18,31,'[cc_catalogue_title]',622,26,'cc_number'),
      txt('cc_catalogue_description',18,64,'[cc_catalogue_description]',622,40,'cc_tiny'),txt('cc_catalogue_offer',18,102,'[cc_catalogue_offer]',622,21,'cc_registertab')]
    effects=[]
    for tier,label in [(1,'cc_limited'),(2,'cc_standard'),(3,'cc_major')]:
        body.append(btn('cc_cat_tier_'+str(tier),18+(tier-1)*148,126,label,'GFX_cc_action_140','cc_registertab'))
        effects.append(f'cc_cat_tier_{tier}_click = {{ set_variable = {{ cc_catalog_tier = {tier} }} cc_ui_refresh = yes cc_touch = yes }}')
    body += [btn('cc_catalogue_requirements',490,126,'cc_catalogue_requirements','GFX_cc_action_150','cc_registertab',tip='cc_catalogue_requirements_tip'),
      txt('cc_catalogue_host_heading',18,168,'cc_catalogue_host',298,17,'cc_label'),txt('cc_catalogue_partner_heading',342,168,'cc_catalogue_partner',298,17,'cc_label'),
      txt('cc_catalogue_host',18,190,'[cc_catalogue_host]',298,100,'cc_tiny'),txt('cc_catalogue_partner',342,190,'[cc_catalogue_partner]',298,100,'cc_tiny'),
      txt('cc_catalogue_host_fees',18,284,'[cc_catalogue_host_fees]',298,34,'cc_tiny'),txt('cc_catalogue_partner_fees',342,284,'[cc_catalogue_partner_fees]',298,34,'cc_tiny'),
      txt('cc_catalogue_capital',18,319,'cc_catalogue_capital_note',622,20,'cc_registertab')]
    gui.append(page('cc_catalogue','\n'.join(body)));scripts.append(sg('cc_catalogue','cc_catalogue',visible=cv('cc_view_tab','=',4),effects=' '.join(effects)))
    gui.append(window('cc_catalogue_footer',btn('cc_catalogue_refer',0,0,'cc_catalogue_refer','GFX_cc_action_240')+txt('cc_catalogue_note',250,4,'cc_catalogue_footer_hint',210,30,'cc_tiny'),640,35,240,541))
    scripts.append(sg('cc_catalogue_footer','cc_catalogue_footer',visible=cv('cc_view_tab','=',4),effects='cc_catalogue_refer_click = { cc_agenda_submit = yes }',triggers='cc_catalogue_refer_click_enabled = { cc_human_member = yes }'))
    for s in range(1,5):
        name=f'cc_{s}_office_actions';prefix=f'cc_{s}_office_'
        body=btn(prefix+'catalogue',476,0,'cc_catalogue_prepare','GFX_cc_primary_156','cc_primary',tip='cc_draft_prepare_tt')+btn(prefix+'agenda',476,0,'cc_agenda_prepare','GFX_cc_primary_156','cc_primary',tip='cc_draft_prepare_tt')
        gui.append(window(name,body,640,35,240,541))
        effects=f'{prefix}catalogue_click = {{ cc_{s}_prepare_catalogue = yes }} {prefix}agenda_click = {{ cc_{s}_prepare_agenda = yes }}'
        triggers=f'{prefix}catalogue_visible = {{ check_variable = {{ cc_view_tab = 4 }} }} {prefix}agenda_visible = {{ check_variable = {{ cc_view_tab = 3 }} check_variable = {{ cc_office_sheet = 1 }} check_variable = {{ cc_office_help = 0 }} }} {prefix}catalogue_click_enabled = {{ cc_{s}_editable = yes }} {prefix}agenda_click_enabled = {{ cc_{s}_editable = yes cc_agenda_selection_valid = yes }}'
        scripts.append(sg(name,name,visible=cv('cc_view_slot','=',s)+' OR = { '+cv('cc_view_tab','=',3)+' '+cv('cc_view_tab','=',4)+' }',effects=effects,triggers=triggers))
