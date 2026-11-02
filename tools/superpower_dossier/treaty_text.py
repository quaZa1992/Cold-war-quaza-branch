# IMPERIA COLD WAR — Briefing prose, configurable protocol text and exact prospective effects
from treaties import TREATIES,FIELDS,OPTIONS,EQUIPMENT,ICBM,MRBM,SANCTIONS,defaults
from missile_protocols import selected


def build(write,loc,defined,mark):
    effects=[mark];scripts=[mark]
    def effect(n,b):effects.append(n+' = {\n'+b+'\n}')
    def text(n,rows,fallback='icsd_empty'):scripts.append(defined(n,rows,fallback))
    labels={'scope':'Covered missiles','reduction':'Missile reduction','reserve_limit':'Reserve ceiling','sanctions':'Core sanctions relief','trade':'Trade protocol','investment':'Investment protocol','duration':'Term','regional':'Core military withdrawal','programme':'Joint programme'}
    values={
     'scope':{0:'No missile commitment',1:'Stored nuclear ICBMs',2:'Stored ballistic missiles',3:'Stored cruise missiles',4:'All listed missile reserves',5:'Nuclear-capable reserves',6:'INF-range reserves'},
     'reduction':{0:'No retirement',10:'Retire 10%',25:'Retire 25%',50:'Retire 50%',100:'Retire 100%'},
     'reserve_limit':{0:'No continuing ceiling',1:'Cap post-reduction reserves'},
     'sanctions':{0:'No sanctions relief',1:'Diplomatic sanctions',2:'Financial sanctions',3:'Economic sanctions',4:'Military sanctions',5:'All four sanction classes'},
     'trade':{0:'No commercial protocol',1:'Trade +50 / Relations +10',2:'Trade +100 / Relations +25'},
     'investment':{0:'No investment protocol',1:'Cost -5% / Duration -5%',2:'Cost -10% / Duration -10%'},
     'duration':{0:'Until withdrawal',180:'180 days',365:'365 days',730:'730 days',1825:'1825 days',5475:'5475 days (15 years)'},
     'regional':{0:'No withdrawal protocol',1:'Recall own attaches',2:'Recall own volunteers',3:'Recall both mission types'},
     'programme':{0:'No joint programme',1:'Scientific cooperation',2:'Civilian supply',3:'Strategic consultations',4:'Regional cooperation'}}
    for field,items in values.items():
        loc('icwt_label_'+field,labels[field])
        for value,label in items.items():loc(f'icwt_{field}_{value}',label)
        text('icwt_value_'+field,[(f'check_variable = {{ icwt_show_{field} = {v} }}',f'icwt_{field}_{v}') for v in items])
    for key,value in {
      'decline_short':'Decline','invite_active':'Invite government','arms':'Arms','economic':'Trade','regional':'Other','terms':'Terms','parties':'Participants','create':'Historical proposal','pending_button':'Review pending paper',
      'review_full':'Review complete terms','submit':'Submit for signature','sign':'Sign agreement','counter':'Revise / decline','amend':'Amend terms',
      'effect_preview':'Prospective effects','effect_preview_tip':'[!icwt_effect_preview_click]',
      'pick_usa':'Select American mission recipient','pick_sov':'Select Soviet mission recipient','invite':'Invite an additional government',
      'optional_note':'Optional invitations do not delay the core accord. Each invited government decides for itself. Choose a country on the map to address an invitation.',
      'participant_names':'CORE PARTIES\nUnited States\nSoviet Union\n\nAMERICAN MISSION: [icwt_usa_mission_name]\nSOVIET MISSION: [icwt_sov_mission_name]\n\nINVITATIONS: [?icwt_edit_invites^num|0] of 6',
      'reciprocity':'Both core parties sign the same terms. Joining governments decide separately. Retirement removes actual stored equipment.',
      'exit_review':'Review treaty withdrawal','exit_confirm':'Confirm withdrawal','consult':'Request consultation',
      'register_note':'Withdrawal ends our ongoing effects. Completed concessions remain.',
      'terms_summary':'Missiles: [icwt_value_scope]\nReduction: [icwt_value_reduction]\nCeiling: [icwt_value_reserve_limit] [icwt_limit_status]\nSanctions: [icwt_value_sanctions]\nTrade: [icwt_value_trade]\nInvestment: [icwt_value_investment]\nTerm: [icwt_value_duration]\nMissions: [icwt_value_regional]\nProgramme: [icwt_value_programme]',
      'consult_title':'Consultation requested','consult_desc':'[FROM.GetName] requests a consultation on the standing agreements between our governments. Their delegations remain responsible for any proposed amendment.',
      'register_member':'PARTICIPATION IN FORCE\nParticipants: [icwt_member_names]',
      'register_unilateral':'UNILATERAL OBSERVANCE\nOur government is the remaining signatory.',
      'register_former':'OUR PARTICIPATION HAS ENDED\nOur treaty spirit and ongoing effects have been removed.',
      'register_none':'No treaty has been selected. Choose an entry from the register.',
      'remaining_open':'Until withdrawal','remaining_days':'[?icwt_show_days|0] days',
      'tab_usa':'Soviet activities','tab_sov':'American activities','tab_detente':'Detente & agreements','tab_register':'Treaties & commitments',
      'mark_usa':'SOVIET ACTIVITY','mark_sov':'AMERICAN ACTIVITY','mark_own':'OUR COMMITMENT','index_report':'RIVAL ACTIVITY','index_own':'OUR COMMITMENTS','index_treaty':'DETENTE AGENDA',
      'kicker_catalog':'BILATERAL NEGOTIATING CHANNEL','kicker_edit':'NEGOTIATING INSTRUMENT','kicker_review':'PAPER FOR SIGNATURE','kicker_register':'TREATY REGISTER',
      'salutation_usa':'MR. PRESIDENT,','salutation_sov':'COMRADE GENERAL SECRETARY,','assessment_label':'SERVICE ASSESSMENT',
      'ledger_own':'Own commitments','ledger_treaty':'Treaty register','history_current':'Current activities','history_mail':'Correspondence',
      'investment_1_effect':'Bilateral investment cost: §G-5%§!\nBilateral investment duration: §G-5%§!',
      'investment_2_effect':'Bilateral investment cost: §G-10%§!\nBilateral investment duration: §G-10%§!',
      'participants_preview':'Parties','participants_tip':'Core parties: United States, Soviet Union\nOptional invitations: [icwt_invite_names]\nAmerican mission recipient: [icwt_usa_mission_name]\nSoviet mission recipient: [icwt_sov_mission_name]',
      'members_tip':'SIGNATORIES\n[icwt_member_names]','register_group':'PARTICIPATION IN FORCE\n[?icwt_show_members|0] signatories. Inspect Participants for the full register.',
      'invites_none':'No additional governments',
    }.items():loc('icwt_'+key,value)
    for f,description in {
      'scope':'Only the listed stored missile models are covered. Deployed forces, launchers and unlisted equipment are outside this reduction.',
      'reduction':'The selected share of each covered reserve model is retired once upon signature or accession. Exact quantities appear in Prospective effects. Withdrawal does not return retired equipment.',
      'reserve_limit':'Caps the total covered missile reserves at the quantity remaining after the agreed reduction. Compliance is inspected weekly. Covered production above this ceiling pauses linked benefits; excess missiles are not confiscated automatically.',
      'sanctions':'Lifts the selected Imperia sanction classes between the United States and Soviet Union. Each existing class lifted costs its imposing government 35 political power. Reimposition is suspended while both participate. National embargoes remain under their own controls.',
      'trade':'Improves trade acceptance and relations between participating governments at peace with each other. The strongest applicable commercial accord applies. It creates no free resource shipments.',
      'investment':'Reduces the cost and construction time of normal investments between participating governments at peace. Choose 5% or 10%. The strongest applicable bilateral rate applies. Construction remains subject to the recipient government and normal investment requirements.',
      'duration':'Choose continuing participation or a fixed term from conclusion. Any participant may withdraw earlier. Withdrawal removes its spirit and continuing benefits. Completed concessions remain in effect.',
      'regional':'Each core government recalls its own attaches or volunteers from its named recipient. Volunteer recall requires the normal game rule, 50 political power and 15 command power when a deployment exists. This does not end another country\'s war.',
      'programme':'An optional American-Soviet programme is negotiated as part of this paper. Both core governments must approve its complete benefits and GDP-based costs. It requires the corresponding investment, trade, production or regional protocol. Other signatories do not join this bilateral programme. Benefits and weekly funding pause during war, embargoes, sanctions or the end of joint participation.'
    }.items():loc('icwt_help_'+f,description)
    for side in ('usa','sov'):
        loc('icwt_'+side+'_mission_set',f'[?icwt_show_{side}_target.GetName]')
        text('icwt_'+side+'_mission_name',[(f'check_variable = {{ icwt_show_{side}_target > 0 }}','icwt_'+side+'_mission_set')],'icwt_mission_none')
    loc('icwt_mission_none','None specified')
    for role,label in ((1,'Select American mission recipient'),(2,'Select Soviet mission recipient'),(3,'Invite this government'),(4,'Invite this government')):loc(f'icwt_picker_{role}',label)
    text('icwt_picker_label',[(f'ROOT = {{ check_variable = {{ icwt_pick_role = {role} }} }}',f'icwt_picker_{role}') for role in range(1,5)],'icsd_picker_label')
    loc('icwt_names_text',''.join(f'[icwt_member_name_{i}]' for i in range(8)))
    text('icwt_member_names',[],'icwt_names_text')
    for i in range(8):
        loc(f'icwt_member_label_{i}',('' if i==0 else ', ')+f'[?icwt_names^{i}.GetName]')
        text(f'icwt_member_name_{i}',[(f'check_variable = {{ icwt_names^num > {i} }}',f'icwt_member_label_{i}')])
    loc('icwt_invites_text',''.join(f'[icwt_invite_name_{i}]' for i in range(6)))
    text('icwt_invite_names',[('check_variable = { icwt_invited_names^num > 0 }','icwt_invites_text')],'icwt_invites_none')
    for i in range(6):
        loc(f'icwt_invite_label_{i}',('' if i==0 else ', ')+f'[?icwt_invited_names^{i}.GetName]')
        text(f'icwt_invite_name_{i}',[(f'check_variable = {{ icwt_invited_names^num > {i} }}',f'icwt_invite_label_{i}')])
    text('icwt_tab_1',[('tag = USA','icwt_tab_usa')],'icwt_tab_sov');text('icwt_tab_2',[],'icwt_tab_detente');text('icwt_tab_3',[],'icwt_tab_register')
    text('icwt_salutation',[('tag = USA','icwt_salutation_usa')],'icwt_salutation_sov')
    text('icwt_report_mark',[('check_variable = { icsd_tab = 3 }','icwt_mark_own'),('tag = USA','icwt_mark_usa')],'icwt_mark_sov')
    text('icwt_index_title',[('check_variable = { icsd_tab = 2 }','icwt_index_treaty'),('check_variable = { icsd_tab = 3 }','icwt_index_own')],'icwt_index_report')
    loc('icwt_kicker_addendum','PROGRAMME ADDENDUM')
    loc('icwt_addendum_desc','Our delegations have received a programme addendum to the standing agreement. Review its cooperation and funding terms before deciding. Existing treaty commitments remain in force.')
    loc('icwt_pending_paper_desc','[icwt_paper_explanation]')
    text('icwt_paper_explanation',[('check_variable = { global.icwt_p_addendum = 1 }','icwt_addendum_desc')],'icwt_invitation_desc')
    text('icwt_document_kicker',[('check_variable = { icsd_tab = 3 }','icwt_kicker_register'),('check_variable = { icwt_show_addendum = 1 }','icwt_kicker_addendum'),('check_variable = { icwt_screen = 3 }','icwt_kicker_review'),('check_variable = { icwt_screen > 0 }','icwt_kicker_edit')],'icwt_kicker_catalog')
    text('icwt_ledger_toggle',[('check_variable = { icwt_register = 1 }','icwt_ledger_own')],'icwt_ledger_treaty')
    text('icwt_history_label',[('check_variable = { icsd_history = 1 }','icwt_history_current')],'icwt_history_mail')
    text('icwt_remaining',[('check_variable = { icwt_show_end > 0 }','icwt_remaining_days')],'icwt_remaining_open')
    text('icwt_selected_spirit',[(f'check_variable = {{ icwt_template = {n} }}',f'icwt_spirit_{n}') for n in range(1,len(TREATIES)+1)])
    # Spirit hovers read their own immutable record, never the menu selection.
    for n in range(1,len(TREATIES)+1):
        for f,items in values.items():
            text(f'icwt_policy_{n}_{f}',[(f'check_variable = {{ global.icwt_pending = {n} }} check_variable = {{ global.icwt_p_{f} = {v} }}',f'icwt_{f}_{v}') for v in items]+[(f'check_variable = {{ global.icwt_{n}_{f} = {v} }}',f'icwt_{f}_{v}') for v in items])
        loc(f'icwt_spirit_{n}_desc','Our government participates in this agreement.\n\n'+'\n'.join(labels[f]+f': [icwt_policy_{n}_{f}]' for f in values)+'\n\nParticipation may be ended through the treaty register. Completed concessions are not reversed.')
    for n in range(1,len(TREATIES)+1):
        loc(f'icwt_status_member_{n}','§GSignatory§!: $icwt_spirit_'+str(n)+'$')
    text('icwt_register_status',[(f'check_variable = {{ icwt_template = {n} }} has_country_flag = icwt_member_{n} check_variable = {{ icwt_show_members = 1 }}','icwt_register_unilateral') for n in range(1,len(TREATIES)+1)]+[('check_variable = { icwt_show_member = 1 } check_variable = { icwt_show_members > 3 }','icwt_register_group')]+[(f'check_variable = {{ icwt_template = {n} }} has_country_flag = icwt_member_{n}','icwt_register_member') for n in range(1,len(TREATIES)+1)]+[('check_variable = { icwt_template > 0 }','icwt_register_former')],'icwt_register_none')
    for i in range(4):text(f'icwt_register_name_{i}',[(f'check_variable = {{ icwt_rows^{i} = {n} }}',f'icwt_title_{n}') for n in range(1,len(TREATIES)+1)])
    brief={
     1:'[?icsd_selected_actor.GetName] maintains an active lend-lease connection with [?icsd_selected_target.GetName]. The relationship is confirmed; the record does not establish delivered quantities or successful arrivals.',
     2:'[?icsd_selected_actor.GetName] has committed volunteer forces to [?icsd_selected_target.GetName]. These are deployed forces, rather than a diplomatic promise of future assistance.',
     3:'[?icsd_selected_actor.GetName] maintains a military attache in [?icsd_selected_target.GetName]. The mission establishes a direct military liaison with that government.',
     4:'[?icsd_selected_actor.GetName] is imposing sanctions on [?icsd_selected_target.GetName]. These measures are a concrete instrument of pressure and may be addressed in negotiations.',
     5:'[?icsd_selected_actor.GetName] and [?icsd_selected_target.GetName] maintain an improved trade agreement. The commercial relationship provides a continuing diplomatic stake.',
     6:'The file records a trade proposal or response involving [?icsd_selected_actor.GetName] and [?icsd_selected_target.GetName]. Its recorded status is [icsd_selected_state_L].',
     7:'The file records a financial proposal or response involving [?icsd_selected_actor.GetName] and [?icsd_selected_target.GetName]. A proposal is distinct from a completed transfer.',
     8:'[?icsd_selected_actor.GetName] has committed to an active construction investment in [?icsd_selected_target.GetName]. Detailed project information depends on the access described in this file.',
     9:'[?icsd_selected_actor.GetName] maintains a [icsd_programme] in [?icsd_selected_target.GetName]. This is an existing government assistance commitment.',
     10:'[?icsd_selected_actor.GetName] is openly backing [icsd_party] in [?icsd_selected_target.GetName]. The record identifies a public political campaign, rather than an inference from election results.',
     11:'Financial and political reporting has corroborated a completed influence action by [?icsd_selected_actor.GetName] in [?icsd_selected_target.GetName].',
     12:'A completed economic aid payment from [?icsd_selected_actor.GetName] to [?icsd_selected_target.GetName] has been corroborated.',
     13:'[?icsd_selected_actor.GetName] is providing weekly financial subsidies to [?icsd_selected_target.GetName]. The programme commits real recurring treasury funding.'}
    for n,s in brief.items():loc('icwt_brief_'+str(n),s)
    text('icwt_briefing',[(f'check_variable = {{ icsd_selected_kind = {n} }}','icwt_brief_'+str(n)) for n in brief])
    loc('icwt_assessment_military','The commitment gives the supporting government a stake in this country. We can reinforce a competing position, apply pressure or negotiate the withdrawal of our own and their contributions.')
    loc('icwt_assessment_economic','The relationship gives the provider a continuing economic or political stake. A competing offer requires our own resources and the recipient government\'s consent.')
    loc('icwt_assessment_opponent','Our commitments also involve [?icsd_context_opponent.GetName], an opponent of the reported recipient. Both powers therefore have a concrete stake in the same conflict.')
    text('icwt_assessment',[('check_variable = { icsd_context_opponent > 0 }','icwt_assessment_opponent'),('OR = { check_variable = { icsd_selected_kind = 1 } check_variable = { icsd_selected_kind = 2 } check_variable = { icsd_selected_kind = 3 } }','icwt_assessment_military')],'icwt_assessment_economic')
    # Views derive only from already saved data. This effect is invoked by meaningful UI/state changes.
    body='''
if = { limit = { check_variable = { icwt_template < 1 } } set_variable = { icwt_template = 1 } }
if = { limit = { check_variable = { icwt_category < 1 } } set_variable = { icwt_category = 1 } }
clear_array = icwt_list clear_array = icwt_names clear_array = icwt_rows clear_array = icwt_invited_names clear_variable = icwt_show_member clear_variable = icwt_show_addendum
if = { limit = { check_variable = { icsd_tab = 2 } check_variable = { icwt_screen > 0 } } set_variable = { icwt_show_addendum = icwt_edit_addendum } }
if = { limit = { icwt_pending = yes check_variable = { icwt_template = global.icwt_pending } } set_variable = { icwt_show_addendum = global.icwt_p_addendum } }
'''
    for n in range(1,len(TREATIES)+1):body+=f'if = {{ limit = {{ OR = {{ has_country_flag = icwt_member_{n} check_variable = {{ icwt_receipt_{n} > 0 }} }} }} add_to_array = {{ icwt_list = {n} }} }}\n'
    body+='''
if = { limit = { check_variable = { icwt_register_offset < 0 } } clear_variable = icwt_register_offset }
if = { limit = { NOT = { check_variable = { icwt_list^num > icwt_register_offset } } } clear_variable = icwt_register_offset }
set_variable = { icwt_register_next = icwt_register_offset } add_to_variable = { icwt_register_next = 4 }
if = { limit = { check_variable = { icsd_tab = 3 } check_variable = { icwt_register = 1 } NOT = { is_in_array = { array = icwt_list value = var:icwt_template } } }
set_variable = { icwt_template = icwt_list^0 }
}
'''
    for i in range(4):body+=f'set_temp_variable = {{ icwt_register_index = icwt_register_offset }} add_to_temp_variable = {{ icwt_register_index = {i} }} if = {{ limit = {{ check_variable = {{ icwt_list^num > icwt_register_index }} }} add_to_array = {{ icwt_rows = icwt_list^icwt_register_index }} }}\n'
    for n in range(1,len(TREATIES)+1):
        body+=f'if = {{ limit = {{ check_variable = {{ icwt_template = {n} }} }}\n'
        body+='if = { limit = { check_variable = { global.icwt_pending = '+str(n)+' } }\n'+'\n'.join(f'set_variable = {{ icwt_show_{f} = global.icwt_p_{f} }}' for f in FIELDS)+'\n} else_if = { limit = { check_variable = { icsd_tab = 2 } check_variable = { icwt_edit_addendum = 1 } check_variable = { icwt_screen > 0 } }\n'+'\n'.join(f'set_variable = {{ icwt_show_{f} = icwt_edit_{f} }}' for f in FIELDS)+'\n} else_if = { limit = { OR = { check_variable = { icsd_tab = 3 } check_variable = { global.icwt_'+str(n)+'_members^num > 0 } } }\n'+'\n'.join(f'set_variable = {{ icwt_show_{f} = global.icwt_{n}_{f} }}' for f in FIELDS)+'\n} else_if = { limit = { check_variable = { icwt_screen = 0 } }\n'+'\n'.join(f'set_variable = {{ icwt_show_{f} = {v} }}' for f,v in defaults(n).items())+'\n} else = {\n'+'\n'.join(f'set_variable = {{ icwt_show_{f} = icwt_edit_{f} }}' for f in FIELDS)+'\n}\n'
        body+=f'for_each_loop = {{ array = global.icwt_{n}_members value = icwt_member_id add_to_array = {{ icwt_names = icwt_member_id }} }}\n'
        body+=f'''if = {{ limit = {{ check_variable = {{ global.icwt_pending = {n} }} }} for_each_loop = {{ array = global.icwt_p_invites value = icwt_invited_id add_to_array = {{ icwt_invited_names = icwt_invited_id }} }} }} else = {{ for_each_loop = {{ array = icwt_edit_invites value = icwt_invited_id add_to_array = {{ icwt_invited_names = icwt_invited_id }} }} }}\n'''
        body+=f'if = {{ limit = {{ has_country_flag = icwt_member_{n} }} set_variable = {{ icwt_show_member = 1 }} }}\n'
        body+=f'set_variable = {{ icwt_show_members = global.icwt_{n}_members^num }} set_variable = {{ icwt_show_end = global.icwt_{n}_end }} set_variable = {{ icwt_show_days = icwt_show_end }} subtract_from_variable = {{ icwt_show_days = global.num_days }} clamp_variable = {{ var = icwt_show_days min = 0 max = 5475 }}\n}}\n'
    body+='icsd_touch = yes'
    effect('icwt_display',body)
    effect('icwt_counteroffer','''
if = { limit = { icwt_core = yes icwt_pending = yes }
set_variable = { icwt_edit_addendum = global.icwt_p_addendum } set_variable = { icwt_edit_base_revision = global.icwt_p_base_revision }
'''+ '\n'.join(f'set_variable = {{ icwt_edit_{f} = global.icwt_p_{f} }}' for f in FIELDS)+'''
set_variable = { icwt_template = global.icwt_pending } clear_array = icwt_edit_invites
for_each_loop = { array = global.icwt_p_invites value = icwt_invited add_to_array = { icwt_edit_invites = icwt_invited } }
clear_variable = global.icwt_pending icwt_clear_reviews = yes set_variable = { icwt_edit_missile_version = 1 } clear_variable = icwt_edit_restraint set_variable = { icwt_screen = 1 } icwt_display = yes icwt_touch_core = yes
}
''')
    effect('icwt_consult','if = { limit = { icwt_core = yes } if = { limit = { tag = USA country_exists = SOV } SOV = { country_event = { id = icwt.501 } } } else_if = { limit = { tag = SOV country_exists = USA } USA = { country_event = { id = icwt.501 } } } }')
    # Exact stockpile quantities and applicable ideas appear in the native effect tooltip.
    preview=[]
    for n in range(1,len(TREATIES)+1):
        segment=[f'if = {{ limit = {{ check_variable = {{ icwt_template = {n} }} }} effect_tooltip = {{ if = {{ limit = {{ NOT = {{ check_variable = {{ ROOT.icwt_show_addendum = 1 }} }} }}']
        for tag in ('USA','SOV'):
            segment.append(f'{tag} = {{ add_ideas = icwt_spirit_{n}')
            segment.append(f'''if = {{ limit = {{ check_variable = {{ global.icwt_pending = {n} }} }}
icwt_preview_assets_{n} = yes
if = {{ limit = {{ check_variable = {{ icwt_plan_fee_{n} > 0 }} }} set_temp_variable = {{ icwt_preview_fee = icwt_plan_fee_{n} }} multiply_temp_variable = {{ icwt_preview_fee = -1 }} add_political_power = icwt_preview_fee }}
if = {{ limit = {{ check_variable = {{ icwt_plan_cp_{n} > 0 }} }} add_command_power = -15 }}
}} else = {{''')
            for equip in EQUIPMENT:
                group=1 if equip in ICBM else 2 if equip in MRBM else 3
                segment.append('if = { limit = { '+selected(equip,'ROOT.icwt_edit_scope','ROOT.icwt_edit_missile_version')+f''' }}
set_temp_variable = {{ icwt_preview_qty = num_equipment@{equip} }} multiply_temp_variable = {{ icwt_preview_qty = ROOT.icwt_edit_reduction }} divide_temp_variable = {{ icwt_preview_qty = 100 }} round_temp_variable = icwt_preview_qty multiply_temp_variable = {{ icwt_preview_qty = -1 }} add_equipment_to_stockpile = {{ type = {equip} amount = icwt_preview_qty }} }}''')
            segment.append('}')
            other='SOV' if tag=='USA' else 'USA'
            segment.append(f'if = {{ limit = {{ NOT = {{ check_variable = {{ global.icwt_pending = {n} }} }} }} set_temp_variable = {{ icwt_preview_fee = 0 }}')
            for typ,num in SANCTIONS:
                segment.append(f'if = {{ limit = {{ OR = {{ check_variable = {{ ROOT.icwt_edit_sanctions = {num} }} check_variable = {{ ROOT.icwt_edit_sanctions = 5 }} }} is_in_array = {{ array = imp_{typ}_sanc_by_us value = {other} }} }} subtract_from_temp_variable = {{ icwt_preview_fee = 35 }} }}')
            segment.append(f'''if = {{ limit = {{ tag = USA }} set_temp_variable = {{ icwt_preview_target = ROOT.icwt_edit_usa_target }} }} else = {{ set_temp_variable = {{ icwt_preview_target = ROOT.icwt_edit_sov_target }} }}
if = {{ limit = {{ OR = {{ check_variable = {{ ROOT.icwt_edit_regional = 2 }} check_variable = {{ ROOT.icwt_edit_regional = 3 }} }} check_variable = {{ icwt_preview_target > 0 }} var:icwt_preview_target = {{ exists = yes has_volunteers_amount_from = {{ tag = PREV count > 0 }} }} }} subtract_from_temp_variable = {{ icwt_preview_fee = 50 }} add_command_power = -15 }}
if = {{ limit = {{ check_variable = {{ icwt_preview_fee < 0 }} }} add_political_power = icwt_preview_fee }} }}''')
            segment.append(f'if = {{ limit = {{ check_variable = {{ global.icwt_pending = {n} }} }} icwt_preview_limit_pending_{n} = yes }} else_if = {{ limit = {{ check_variable = {{ ROOT.icsd_tab = 3 }} }} icwt_preview_limit_standing_{n} = yes }} else = {{ icwt_preview_limit_draft_{n} = yes }}')
            for level,op in ((1,10),(2,25)):
                segment.append(f'if = {{ limit = {{ check_variable = {{ ROOT.icwt_show_trade = {level} }} }} add_opinion_modifier = {{ target = {other} modifier = icwt_trade_{level} }} add_opinion_modifier = {{ target = {other} modifier = icwt_relations_{level} }} }}')
                segment.append(f'if = {{ limit = {{ check_variable = {{ ROOT.icwt_show_investment = {level} }} }} custom_effect_tooltip = icwt_investment_{level}_effect }}')
            segment.append('}')
        segment.append('}\nicwt_programme_terms_selected = yes\nicwt_tension_terms_'+str(n)+' = yes')
        segment.append('} }');preview.extend(segment)
    effect('icwt_preview_selected','\n'.join(preview))
    write('common/scripted_effects/ICW_superpower_treaty_ui.txt','\n'.join(effects)+'\n')
    from treaty_help import build as help_text
    scripts.extend(help_text(loc,defined))
    write('common/scripted_localisation/ICW_superpower_treaty_ui.txt','\n'.join(scripts)+'\n')
