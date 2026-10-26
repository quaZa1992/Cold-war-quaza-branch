# IMPERIA CW — Cold War: approved Spanish succession and native cabinet integration.
"""Political provider for the immutable Spain v2 design; emits only owned files.

Programme modifiers, ordinary focus rewards and starting spirits belong to compile.py.
This module owns legal packages, capacity, the real cabinet and native leader routing.
"""
from pathlib import Path
import json

HEADER = '# IMPERIA CW — Cold War: Spain 1970 succession and constitutional government.\n'
HERE = Path(__file__).resolve().parent
GROUPS = {'continuity':22, 'falange':21, 'crown':23, 'ucd':1,
          'ap_pp':1, 'cds':2, 'psoe':3, 'pce_iu':4}
LEGAL = {'fundamental':'COLDWAR_SPR_legal_authoritarian',
         'royal':'COLDWAR_SPR_legal_royal',
         'parliamentary':'COLDWAR_SPR_legal_representative'}

def fmt(value):
    return ('%.5f' % value).rstrip('0').rstrip('.') or '0'

def build(root, design):
    root = Path(root)
    output, effects, triggers, ideas, decisions, events, loc, metadata = {}, [], [], [], [], [], {}, {}
    decision_previews = {}
    def local(key, text):
        loc[key] = text
        return key
    def effect(key, code):
        effects.append(key + ' = {\n' + code + '\n}\n')
    def trigger(key, code):
        triggers.append(key + ' = { ' + code + ' }\n')
    def flag(key): return 'has_country_flag = COLDWAR_SPR_' + key
    def setflag(key): return 'set_country_flag = COLDWAR_SPR_' + key
    def clearflag(key): return 'clr_country_flag = COLDWAR_SPR_' + key
    def idea(key, title, description, modifiers, picture='generic_political_reform'):
        local(key, title); local(key+'_desc', description)
        ideas.append(key+' = { allowed = { always = no } picture = '+picture+' modifier = { '+
                     ' '.join(k+' = '+fmt(v) for k,v in modifiers.items())+' } }\n')
    def event(number, title, description, options, immediate='', trigger_code='', authority=''):
        ident = 'COLDWAR_SPR_v2_politics.'+str(number)
        local(ident+'.t', title); local(ident+'.d', description)
        opts=[]
        for index, (name, code, gate) in enumerate(options):
            key=local(ident+'.'+chr(97+index),name)
            if authority:
                gate=authority+(' '+gate if gate else '')
                code='if = { limit = { '+gate+' } '+code+' }'
            opts.append('option = { name = '+key+(' trigger = { '+gate+' }' if gate else '')+'\n'+code+'\n}')
        if authority:
            stale=local(ident+'.stale','Refer this question to the incumbent cabinet.')
            opts.append('option = { name = '+stale+' trigger = { NOT = { '+authority+' } } }')
        events.append('country_event = { id = '+ident+' title = '+ident+'.t desc = '+ident+'.d picture = GFX_election_day is_triggered_only = yes\n'+
                      ('trigger = { '+trigger_code+' }\n' if trigger_code else '')+
                      ('immediate = { '+immediate+' }\n' if immediate else '')+'\n'.join(opts)+'\n}\n')
    def decision(key, title, description, cost, visible, available, complete, days=None):
        local(key,title); local(key+'_desc',description)
        decisions.append(key+' = { icon = generic_political_discourse cost = '+str(cost)+'\nvisible = { '+visible+' }\navailable = { '+available+' }\n'+
                         ('days_remove = '+str(days)+'\nremove_effect = { '+complete+' }\ncomplete_effect = { }' if days else 'complete_effect = { '+complete+' }')+
                         '\nai_will_do = { factor = 1 }\n}\n')
    def tooltip(key,text):
        local(key,text)
        return 'custom_effect_tooltip = '+key

    # Every authority predicate follows the actual MD ruling_party variable.
    trigger('COLDWAR_SPR_campaign','tag = SPR original_tag = SPR is_dynamic_country = no IMP_is_1970_scenario = yes')
    trigger('COLDWAR_SPR_franco_in_office','COLDWAR_SPR_campaign = yes NOT = { '+flag('franco_departed')+' } check_variable = { ruling_party = 21 } OR = { has_country_leader = { name = "Francisco Franco" ruling_only = yes } AND = { '+flag('franco_incumbency')+' date > 1975.11.19 date < 1975.11.21 } }')
    trigger('COLDWAR_SPR_franco_has_left_office','COLDWAR_SPR_campaign = yes '+flag('franco_departed'))
    trigger('COLDWAR_SPR_franco_alive','COLDWAR_SPR_franco_in_office = yes')
    trigger('COLDWAR_SPR_franco_dead','COLDWAR_SPR_franco_has_left_office = yes')
    trigger('COLDWAR_SPR_representative_settlement','COLDWAR_SPR_campaign = yes '+flag('legal_representative')+' has_elections = yes')
    trigger('COLDWAR_SPR_authoritarian_settlement','COLDWAR_SPR_campaign = yes OR = { '+flag('legal_authoritarian')+' '+flag('legal_royal')+' } has_elections = no')
    trigger('COLDWAR_SPR_democratic_constitution','COLDWAR_SPR_representative_settlement = yes')
    for group,slot in GROUPS.items():
        code='COLDWAR_SPR_franco_has_left_office = yes check_variable = { ruling_party = '+str(slot)+' }'
        if group=='ucd': code+=' '+flag('mandate_ucd')+' NOT = { '+flag('mandate_ap_pp')+' }'
        if group=='ap_pp': code+=' '+flag('mandate_ap_pp')+' NOT = { '+flag('mandate_ucd')+' }'
        if group=='crown': code+=' NOT = { '+flag('parliamentary_republic')+' }'
        trigger('COLDWAR_SPR_government_'+group,code)
        local('COLDWAR_SPR_government_'+group+'_tt', 'The '+next(g['label'] for g in design['groups'] if g['id']==group)+' governs Spain.')
    for alias,current in [('ap','ap_pp'),('liberal','cds'),('pce','pce_iu')]:
        trigger('COLDWAR_SPR_government_'+alias,'COLDWAR_SPR_government_'+current+' = yes')
    trigger('COLDWAR_SPR_carlist_traditionalists','COLDWAR_SPR_campaign = yes '+flag('carlist_traditionalist_agreement')+' check_variable = { COLDWAR_SPR_carlist_party = ruling_party } check_variable = { COLDWAR_SPR_carlist_generation = COLDWAR_SPR_government_generation }')
    trigger('COLDWAR_SPR_carlist_social_federalists','COLDWAR_SPR_representative_settlement = yes '+flag('carlist_social_federalist_agreement')+' check_variable = { COLDWAR_SPR_carlist_party = ruling_party } check_variable = { COLDWAR_SPR_carlist_generation = COLDWAR_SPR_government_generation }')
    trigger('COLDWAR_SPR_revision_eligible',flag('revision_unlocked')+' '+flag('settlement_recorded')+' NOT = { '+flag('revision_in_progress')+' } check_variable = { COLDWAR_SPR_government_generation > COLDWAR_SPR_settlement_generation }')

    # Capacity is a separate health stock; preparations never add to it.
    for suffix,amount,title in [('early',-.10,'Ageing Leadership'),('late',-.15,'Diminishing Executive Capacity'),('critical',-.20,'A Head of State Incapacitated'),('late_delegated',-.10,'Delegated Executive Authority'),('critical_delegated',-.15,'A Delegated Headship')]:
        idea('COLDWAR_SPR_capacity_'+suffix,title,'The administration must conduct public business while the head of state is increasingly unable to intervene.',{'political_power_factor':amount},'COLDWAR_SPR_v2_ageing')
    idea('COLDWAR_SPR_personal_command_spirit','Personal Command','Cabinet authority continues to depend on the personal intervention of the head of state.',{'political_power_factor':.10})
    idea('COLDWAR_SPR_succession_disruption','Disrupted Succession','Unresolved instructions impede the administration during the transfer of authority.',{'political_power_factor':-.10})
    idea('COLDWAR_SPR_medical_bulletin','An Official Medical Bulletin','Publication of an official bulletin has temporarily reduced uncertainty.',{'stability_factor':.02})
    idea('COLDWAR_SPR_republic_constituent_period','The Constituent Period','The elected Cortes is negotiating the transfer of the headship of state.',{'stability_factor':-.05})
    for legal,nodeid in [('fundamental','COLDWAR_SPR_fundamental_settlement'),('royal','COLDWAR_SPR_royal_executive'),('parliamentary','COLDWAR_SPR_parliamentary_settlement')]:
        n=next(n for n in design['nodes'] if n['id']==nodeid)
        mods={e['key']:e['amount'] for e in n['effects'] if e['type']=='modifier'}
        idea('COLDWAR_SPR_legal_'+legal,n['title'],n['description'],mods)

    effect('COLDWAR_SPR_initialize', '''if = { limit = { COLDWAR_SPR_campaign = yes }
 COLDWAR_SPR_initialize_core = yes
 COLDWAR_SPR_initialize_agreements = yes
 if = { limit = { NOT = { has_country_flag = COLDWAR_SPR_v2_politics_initialized } }
  set_country_flag = COLDWAR_SPR_v2_politics_initialized
  set_variable = { COLDWAR_SPR_capacity = 75 }
  set_variable = { COLDWAR_SPR_preparedness = 20 }
  set_variable = { COLDWAR_SPR_observed_ruling_party = ruling_party }
  set_variable = { COLDWAR_SPR_government_generation = 0 }
  set_variable = { COLDWAR_SPR_health_month = 0 }
  if = { limit = { check_variable = { ruling_party = 21 } } set_country_flag = COLDWAR_SPR_franco_incumbency }
 }
 COLDWAR_SPR_refresh_politics = yes
}''')
    effect('COLDWAR_SPR_clamp_health', '''clamp_variable = { var = COLDWAR_SPR_capacity min = 0 max = 100 }
clamp_variable = { var = COLDWAR_SPR_preparedness min = 0 max = 100 }''')
    health_ideas=' '.join('remove_ideas = COLDWAR_SPR_capacity_'+s for s in ['early','late','critical','late_delegated','critical_delegated'])
    effect('COLDWAR_SPR_sync_health', '''COLDWAR_SPR_clamp_health = yes
remove_ideas = COLDWAR_SPR_caudillo_last_years
'''+health_ideas+'''
if = { limit = { COLDWAR_SPR_franco_in_office = yes }
 if = { limit = { check_variable = { COLDWAR_SPR_capacity < 25 } }
  if = { limit = { OR = { has_country_flag = COLDWAR_SPR_delegation_active has_country_flag = COLDWAR_SPR_cabinet_delegated } } add_ideas = COLDWAR_SPR_capacity_critical_delegated }
  else = { add_ideas = COLDWAR_SPR_capacity_critical }
 }
 else_if = { limit = { check_variable = { COLDWAR_SPR_capacity < 50 } }
  if = { limit = { OR = { has_country_flag = COLDWAR_SPR_delegation_active has_country_flag = COLDWAR_SPR_cabinet_delegated } } add_ideas = COLDWAR_SPR_capacity_late_delegated }
  else = { add_ideas = COLDWAR_SPR_capacity_late }
 }
 else = { add_ideas = COLDWAR_SPR_capacity_early }
}
else = { remove_ideas = COLDWAR_SPR_personal_command_spirit }''')
    effect('COLDWAR_SPR_health_monthly', '''if = { limit = { COLDWAR_SPR_franco_in_office = yes }
 if = { limit = { has_country_flag = COLDWAR_SPR_serious_illness } subtract_from_variable = { COLDWAR_SPR_capacity = 1.5 } }
 else = { subtract_from_variable = { COLDWAR_SPR_capacity = 0.5 } }
 COLDWAR_SPR_sync_health = yes
}''')
    # Date milestones are catch-up safe and terminal departure has a hard upper bound.
    effect('COLDWAR_SPR_health_daily', '''if = { limit = { date > 1973.12.19 NOT = { has_country_flag = COLDWAR_SPR_carrero_crisis_resolved } }
 set_country_flag = COLDWAR_SPR_carrero_crisis_resolved
 set_country_flag = COLDWAR_SPR_carrero_dead
 country_event = { id = COLDWAR_SPR_v2_politics.1 }
}
if = { limit = { COLDWAR_SPR_franco_in_office = yes date > 1974.7.8 NOT = { has_country_flag = COLDWAR_SPR_serious_illness } }
 set_country_flag = COLDWAR_SPR_serious_illness
 subtract_from_variable = { COLDWAR_SPR_capacity = 25 }
 country_event = { id = COLDWAR_SPR_v2_politics.2 }
}
if = { limit = { COLDWAR_SPR_franco_in_office = yes date > 1974.7.29 has_country_flag = COLDWAR_SPR_serious_illness NOT = { has_country_flag = COLDWAR_SPR_partial_recovery } }
 set_country_flag = COLDWAR_SPR_partial_recovery
 add_to_variable = { COLDWAR_SPR_capacity = 10 }
}
if = { limit = { date > 1975.10.14 NOT = { has_country_flag = COLDWAR_SPR_franco_departed } }
 if = { limit = { NOT = { has_country_flag = COLDWAR_SPR_terminal_crisis } }
  set_country_flag = COLDWAR_SPR_terminal_crisis
  set_variable = { COLDWAR_SPR_capacity = 10 }
  country_event = { id = COLDWAR_SPR_v2_politics.3 }
 }
 if = { limit = { date > 1975.11.19 } set_country_flag = COLDWAR_SPR_franco_dead COLDWAR_SPR_franco_departure = yes }
 else_if = { limit = { date > 1975.10.29 } random = { chance = 5 set_country_flag = COLDWAR_SPR_franco_dead COLDWAR_SPR_franco_departure = yes } }
}
COLDWAR_SPR_sync_health = yes''')
    effect('COLDWAR_SPR_franco_departure', '''if = { limit = { NOT = { has_country_flag = COLDWAR_SPR_franco_departed } }
 set_country_flag = COLDWAR_SPR_franco_departed
 clr_country_flag = COLDWAR_SPR_delegation_active
 if = { limit = { check_variable = { COLDWAR_SPR_preparedness >= 80 } } add_stability = -0.05 }
 else_if = { limit = { check_variable = { COLDWAR_SPR_preparedness >= 50 } } add_stability = -0.10 }
 else = { add_stability = -0.20 add_timed_idea = { idea = COLDWAR_SPR_succession_disruption days = 180 } }
 COLDWAR_SPR_sync_health = yes
 if = { limit = { check_variable = { ruling_party = 21 } has_elections = no }
  set_temp_variable = { rul_party_temp = 23 }
  set_temp_variable = { disable_elections = 1 }
  change_ruling_party_effect = yes
 }
 COLDWAR_SPR_refresh_politics = yes
 if = { limit = { has_country_flag = COLDWAR_SPR_franco_dead } country_event = { id = COLDWAR_SPR_v2_politics.4 } }
 else = { country_event = { id = COLDWAR_SPR_v2_politics.5 } }
}''')

    # A legal settlement is an exclusive live package, independent of focus history.
    effect('COLDWAR_SPR_remove_legal_packages','\n'.join('remove_ideas = COLDWAR_SPR_legal_'+s for s in LEGAL)+'\n'+
           '\n'.join('clr_country_flag = '+s for s in LEGAL.values()))
    for legal,slot in [('fundamental',22),('royal',23),('parliamentary',None)]:
        code='COLDWAR_SPR_remove_legal_packages = yes\nset_country_flag = '+LEGAL[legal]+'\nadd_ideas = COLDWAR_SPR_legal_'+legal+'\nset_country_flag = COLDWAR_SPR_settlement_recorded\nset_variable = { COLDWAR_SPR_settlement_generation = COLDWAR_SPR_government_generation }\n'
        if slot:
            code+='set_temp_variable = { rul_party_temp = '+str(slot)+' }\nset_temp_variable = { disable_elections = 1 }\nchange_ruling_party_effect = yes\nset_variable = { COLDWAR_SPR_settlement_generation = COLDWAR_SPR_government_generation }\n'
        else:
            code+='set_politics = { elections_allowed = yes }\n'
        code+='clr_country_flag = COLDWAR_SPR_revision_in_progress\nCOLDWAR_SPR_refresh_politics = yes'
        effect('COLDWAR_SPR_enact_legal_'+legal,code)
    effect('COLDWAR_SPR_legalise_parties', '''clr_country_flag = partyall_banned
clr_country_flag = generic_election_killswitch
resize_array = { array = party_banned_array size = 24 value = 0 }
for_loop_effect = { start = 0 end = 24 value = COLDWAR_SPR_party_index set_variable = { party_banned_array^COLDWAR_SPR_party_index = 0 } }
set_country_flag = COLDWAR_SPR_parties_legal
update_dirty_politicsview_expanded = yes''')
    effect('COLDWAR_SPR_begin_legal_reform', '''if = { limit = { NOT = { has_country_flag = COLDWAR_SPR_reform_in_progress } }
 set_country_flag = COLDWAR_SPR_reform_in_progress
 set_variable = { COLDWAR_SPR_reform_generation = COLDWAR_SPR_government_generation }
 country_event = { id = COLDWAR_SPR_v2_politics.10 }
}''')
    effect('COLDWAR_SPR_call_constituent_election', '''if = { limit = { NOT = { has_country_flag = elections_in_progress } }
 COLDWAR_SPR_legalise_parties = yes
 set_politics = { elections_allowed = yes }
 set_elections_48_months = yes
 set_country_flag = COLDWAR_SPR_constituent_campaign_pending
 country_event = { id = MD4_election_campaign.0 days = 1 }
}''')

    # Focus decision payloads are immediate grants/unlocks, never duplicate clicks.
    handlers={
      'succession_preparations':setflag('succession_preparations_unlocked'),
      'delegated_cabinet':'add_to_variable = { COLDWAR_SPR_preparedness = 10 }\n'+setflag('cabinet_delegated'),
      'personal_command':'subtract_from_variable = { COLDWAR_SPR_preparedness = 15 }\nadd_ideas = COLDWAR_SPR_personal_command_spirit',
      'cabinet_files':'add_to_variable = { COLDWAR_SPR_preparedness = 5 }',
      'continuity_protocol':'add_to_variable = { COLDWAR_SPR_preparedness = 5 }\n'+setflag('continuity_protocol'),
      'command_protocol':'add_to_variable = { COLDWAR_SPR_preparedness = 5 }\n'+setflag('command_protocol'),
      'interregnum_plan':'add_to_variable = { COLDWAR_SPR_preparedness = 10 }\n'+setflag('regency_preparation_unlocked'),
      'royal_briefing':'add_to_variable = { COLDWAR_SPR_preparedness = 5 }\n'+setflag('royal_briefed'),
      'regency_protocol':'add_to_variable = { COLDWAR_SPR_preparedness = 5 }\n'+setflag('regency_protocol'),
      'prepared_succession':'add_to_variable = { COLDWAR_SPR_preparedness = 10 }',
      'settlement_talks':setflag('settlement_talks_open'),
      'continuity_settlement':'COLDWAR_SPR_enact_legal_fundamental = yes',
      'royal_settlement':'COLDWAR_SPR_enact_legal_royal = yes',
      'political_reform':'COLDWAR_SPR_begin_legal_reform = yes',
      'review_settlement':setflag('revision_unlocked'),
      'parliamentary_crown':setflag('parliamentary_monarchy')+'\n'+clearflag('parliamentary_republic')+'\nCOLDWAR_SPR_enact_legal_parliamentary = yes',
      'republic_constituent_vote':setflag('republic_vote_pending')+'\nset_variable = { COLDWAR_SPR_republic_generation = COLDWAR_SPR_government_generation }\nadd_timed_idea = { idea = COLDWAR_SPR_republic_constituent_period days = 180 }\ncountry_event = { id = COLDWAR_SPR_v2_politics.16 days = 180 }',
      'legal_succession':setflag('legal_succession'),
      'carlist_bargain':setflag('carlist_bargain_unlocked')+'\nCOLDWAR_SPR_request_carlist_agreement = yes',
    }
    previews={
      'succession_preparations':'Unlock preparations for the transfer of authority. Capacity and Succession Preparedness range from 0 to 100.',
      'delegated_cabinet':'Delegation reduces the late-stage executive penalty by §G5 percentage points§!.',
      'personal_command':'Personal command lasts while Franco remains in office.',
      'cabinet_files':'',
      'continuity_protocol':'The administrative stability loss in a presidential vacancy is reduced from §R5%§! to §R2%§!.',
      'command_protocol':'',
      'interregnum_plan':'Agree procedures for the Council of Regency.',
      'royal_briefing':'The designated successor may accept acting duties during serious illness.',
      'regency_protocol':'',
      'prepared_succession':'',
      'settlement_talks':'Open negotiations on the legal settlement. Succession stability loss: §R5%§! with preparedness 80+, §R10%§! with 50–79, otherwise §R20%§! and Political Power gain §R-10%§! for §Y180 days§!.',
      'continuity_settlement':'The Fundamental Laws remain in force. National elections remain suspended.',
      'royal_settlement':'The crown appoints and directs the government. National elections remain suspended.',
      'political_reform':'Begin the reform agreement: legal guarantees, a referendum, competitive elections and a constituent Cortes.',
      'review_settlement':'A subsequent governing mandate may convene constitutional revision for §Y100 Political Power§! and §Y60 days§!. The revised constitutional package replaces its predecessor.',
      'parliamentary_crown':'Ratify parliamentary monarchy under representative government.',
      'republic_constituent_vote':'Convene the constitutional vote after a §Y180-day§! constituent period.',
      'legal_succession':'Publish the lawful handover procedure. Institutional preparation remains voluntary.',
      'carlist_bargain':'Negotiate a traditionalist or social-federalist Carlist cabinet agreement. The agreement ends with a change of governing party or a renewed electoral mandate.',
    }
    preparedness={'delegated_cabinet':10,'personal_command':-15,'cabinet_files':5,'continuity_protocol':5,'command_protocol':5,'interregnum_plan':10,'royal_briefing':5,'regency_protocol':5,'prepared_succession':10}
    local('COLDWAR_SPR_preparedness_tt','Succession Preparedness: $RIGHT|+=0$')
    for node in design['nodes']:
        owned=[e for e in node['effects'] if e['type']=='decision' and e['id'].removeprefix('COLDWAR_SPR_') in handlers]
        if not owned: continue
        preview=[]
        for e in owned:
            suffix=e['id'].removeprefix('COLDWAR_SPR_')
            code=handlers[suffix]
            gate='COLDWAR_SPR_campaign = yes'
            if node['gate'].get('Franco_in_office'): gate+=' COLDWAR_SPR_franco_in_office = yes'
            if node['gate'].get('Franco_has_left_office'): gate+=' COLDWAR_SPR_franco_has_left_office = yes'
            if node['gate'].get('representative_legal_settlement'): gate+=' COLDWAR_SPR_representative_settlement = yes'
            effect(e['id']+'_effect','if = { limit = { '+gate+' NOT = { has_country_flag = '+e['id']+'_delivered } }\n'+code+'\nset_country_flag = '+e['id']+'_delivered\nCOLDWAR_SPR_clamp_health = yes\nCOLDWAR_SPR_refresh_politics = yes\n}')
            one_preview=[]
            if suffix in preparedness: one_preview.append('add_to_variable = { COLDWAR_SPR_preparedness = '+str(preparedness[suffix])+' tooltip = COLDWAR_SPR_preparedness_tt }')
            if previews[suffix]: one_preview.append(tooltip(e['id']+'_effect_tt',previews[suffix]))
            if suffix=='personal_command': one_preview.append('add_ideas = COLDWAR_SPR_personal_command_spirit')
            if suffix=='continuity_settlement': one_preview.append('add_ideas = COLDWAR_SPR_legal_fundamental')
            if suffix=='royal_settlement': one_preview.append('add_ideas = COLDWAR_SPR_legal_royal')
            if suffix=='republic_constituent_vote': one_preview.append('add_timed_idea = { idea = COLDWAR_SPR_republic_constituent_period days = 180 }')
            decision_previews[e['id']]='\n'.join(one_preview)
            preview.extend(one_preview)
        metadata[node['id']]={'preview':'\n'.join(preview),'available':''}
    for ident,trig in [('traditionalist_bargain','carlist_traditionalists'),('social_federal_bargain','carlist_social_federalists')]:
        metadata['COLDWAR_SPR_'+ident]={'available':'custom_trigger_tooltip = { tooltip = COLDWAR_SPR_'+trig+'_tt COLDWAR_SPR_'+trig+' = yes }','preview':''}
        local('COLDWAR_SPR_'+trig+'_tt','A current cabinet agreement recognises the '+('traditionalist' if ident.startswith('traditionalist') else 'social-federalist')+' Carlist current.')

    # Health decisions have costs and executable, clamped preparation changes.
    office='COLDWAR_SPR_franco_in_office = yes '+flag('succession_preparations_unlocked')
    gates={
      'delegate_business':'NOT = { has_completed_focus = COLDWAR_SPR_personal_authority }',
      'brief_prince':flag('royal_briefed'),
      'consult_commands':'OR = { has_completed_focus = COLDWAR_SPR_command_channels has_completed_focus = COLDWAR_SPR_carrero_guarantees }',
      'issue_bulletin':flag('serious_illness')+' NOT = { has_idea = COLDWAR_SPR_medical_bulletin } OR = { AND = { '+flag('terminal_crisis')+' NOT = { '+flag('bulletin_terminal')+' } } AND = { NOT = { '+flag('terminal_crisis')+' } NOT = { '+flag('bulletin_serious')+' } } }',
      'temporary_delegation':flag('serious_illness')+' check_variable = { COLDWAR_SPR_capacity < 30 } '+flag('royal_briefed')+' OR = { '+flag('regency_protocol')+' '+flag('legal_succession')+' '+flag('regency_preparation_unlocked')+' }',
    }
    for entry in design['health']['decisions']:
        key=entry['id']; suffix=key.removeprefix('COLDWAR_SPR_')
        visible=office
        if suffix!='issue_bulletin': visible+=' NOT = { has_country_flag = '+key+'_used }'
        available=office+' '+gates[suffix]
        if suffix!='issue_bulletin': available+=' NOT = { has_country_flag = '+key+'_used }'
        code='if = { limit = { '+available+' } add_to_variable = { COLDWAR_SPR_preparedness = '+str(entry['preparedness'])+' }\n'
        if suffix=='issue_bulletin':
            code+='add_timed_idea = { idea = COLDWAR_SPR_medical_bulletin days = 90 }\nif = { limit = { '+flag('terminal_crisis')+' } '+setflag('bulletin_terminal')+' } else = { '+setflag('bulletin_serious')+' }\n'
        else: code+='set_country_flag = '+key+'_used\n'
        if suffix=='delegate_business': code+=setflag('cabinet_delegated')+'\n'
        if suffix=='temporary_delegation': code+=setflag('delegation_active')+'\n'
        code+='COLDWAR_SPR_clamp_health = yes COLDWAR_SPR_sync_health = yes }'
        descriptions={
          'delegate_business':'Ministers will conduct routine cabinet business under delegated authority. Succession Preparedness §G+15§!; reduce the late-stage executive penalty by §G5 percentage points§! while Franco remains in office. One use.',
          'brief_prince':'Brief the designated successor on the business of state. Succession Preparedness §G+10§!. One use.',
          'consult_commands':'The military regions will receive the agreed lawful handover procedure. Succession Preparedness §G+10§!. One use.',
          'issue_bulletin':'Publish an official report during serious illness. Succession Preparedness §G+5§!; Stability §G+2%§! for §Y90 days§!. Once during serious illness and once during the terminal crisis.',
          'temporary_delegation':'The designated successor assumes acting duties while Franco retains formal headship. Succession Preparedness §G+10§!; reduce the late-stage executive penalty by §G5 percentage points§!. One use.',
        }
        requirements={
          'delegate_business':'Franco remains in office; preparations are authorised; Personal Authority has not been adopted. Available once.',
          'brief_prince':"Franco remains in office; The Prince's Briefings have been completed. Available once.",
          'consult_commands':"Franco remains in office; Command Channels or Carrero's Guarantees have been completed. Available once.",
          'issue_bulletin':'A serious or terminal illness has begun; no official medical bulletin is active; no bulletin has yet been issued during this stage.',
          'temporary_delegation':"Franco remains in office after serious illness; capacity is below 30; the prince has been briefed and the legal handover or regency protocol has been agreed. Available once.",
        }
        local(key+'_requirements_tt',requirements[suffix])
        decision(key,entry['title'],descriptions[suffix],entry['cost_pp'],visible,
                 'custom_trigger_tooltip = { tooltip = '+key+'_requirements_tt '+available+' }',code)

    # The government generation changes only on real authority changes or new mandates.
    effect('COLDWAR_SPR_invalidate_old_mandate', '''clr_country_flag = COLDWAR_SPR_carlist_traditionalist_agreement
clr_country_flag = COLDWAR_SPR_carlist_social_federalist_agreement
clr_country_flag = COLDWAR_SPR_mandate_pending
clr_country_flag = COLDWAR_SPR_carlist_negotiation_pending
clr_country_flag = COLDWAR_SPR_revision_in_progress
clr_country_flag = COLDWAR_SPR_republic_vote_pending
remove_ideas = COLDWAR_SPR_republic_constituent_period
if = { limit = { NOT = { has_country_flag = COLDWAR_SPR_constituent_campaign_pending } }
 clr_country_flag = COLDWAR_SPR_reform_in_progress
 clr_country_flag = COLDWAR_SPR_reform_referendum_pending
}
else = {
 set_variable = { COLDWAR_SPR_reform_generation = COLDWAR_SPR_government_generation }
 if = { limit = { has_country_flag = COLDWAR_SPR_constituent_ratification_pending }
  set_variable = { COLDWAR_SPR_constituent_generation = COLDWAR_SPR_government_generation }
  country_event = { id = COLDWAR_SPR_v2_politics.12 hours = 1 }
 }
}''')
    effect('COLDWAR_SPR_observe_government', '''if = { limit = { NOT = { check_variable = { COLDWAR_SPR_observed_ruling_party = ruling_party } } }
 add_to_variable = { COLDWAR_SPR_government_generation = 1 }
 set_variable = { COLDWAR_SPR_observed_ruling_party = ruling_party }
 COLDWAR_SPR_invalidate_old_mandate = yes
 if = { limit = { check_variable = { ruling_party = 1 } } COLDWAR_SPR_request_mandate = yes }
}
if = { limit = { check_variable = { ruling_party = 1 } NOT = { OR = { has_country_flag = COLDWAR_SPR_mandate_ucd has_country_flag = COLDWAR_SPR_mandate_ap_pp } } } COLDWAR_SPR_request_mandate = yes }''')
    effect('COLDWAR_SPR_request_mandate', '''if = { limit = { check_variable = { ruling_party = 1 } NOT = { has_country_flag = elections_in_progress } NOT = { has_country_flag = coalition_forming } NOT = { has_country_flag = COLDWAR_SPR_native_campaign_seen } NOT = { has_country_flag = COLDWAR_SPR_mandate_pending } }
 set_country_flag = COLDWAR_SPR_mandate_pending
 set_variable = { COLDWAR_SPR_mandate_generation = COLDWAR_SPR_government_generation }
 country_event = { id = COLDWAR_SPR_v2_politics.20 }
}''')
    effect('COLDWAR_SPR_request_carlist_agreement', '''if = { limit = { COLDWAR_SPR_franco_has_left_office = yes NOT = { has_country_flag = COLDWAR_SPR_carlist_negotiation_pending } }
 set_country_flag = COLDWAR_SPR_carlist_negotiation_pending
 set_variable = { COLDWAR_SPR_carlist_negotiation_generation = COLDWAR_SPR_government_generation }
 country_event = { id = COLDWAR_SPR_v2_politics.30 }
}''')
    effect('COLDWAR_SPR_refresh_politics', '''if = { limit = { COLDWAR_SPR_campaign = yes }
 COLDWAR_SPR_observe_government = yes
 COLDWAR_SPR_sync_health = yes
 COLDWAR_SPR_sync_programmes = yes
 COLDWAR_SPR_refresh_agreements = yes
 COLDWAR_SPR_refresh_colour = yes
}''')

    decision('COLDWAR_SPR_revise_constitution','Convene Constitutional Revision','A new governing mandate may reopen the constitutional pact. The Cortes and the head of state must complete a negotiated revision.',100,
             flag('revision_unlocked')+' COLDWAR_SPR_franco_has_left_office = yes', 'COLDWAR_SPR_revision_eligible = yes',
             'if = { limit = { COLDWAR_SPR_revision_eligible = yes } '+setflag('revision_in_progress')+' set_variable = { COLDWAR_SPR_revision_generation = COLDWAR_SPR_government_generation } country_event = { id = COLDWAR_SPR_v2_politics.14 days = 60 } }')
    decision('COLDWAR_SPR_resume_legal_reform','Reconvene Political Reform Talks','The cabinet may return a rejected reform agreement to negotiations. Ratification still requires a public vote and competitive elections.',0,
             flag('COLDWAR_SPR_political_reform_delivered'.removeprefix('COLDWAR_SPR_'))+' COLDWAR_SPR_franco_has_left_office = yes NOT = { COLDWAR_SPR_representative_settlement = yes }',
             'NOT = { '+flag('reform_in_progress')+' } NOT = { '+flag('revision_in_progress')+' }',
             'COLDWAR_SPR_begin_legal_reform = yes')
    decision('COLDWAR_SPR_negotiate_carlist_agreement','Negotiate a Carlist Cabinet Agreement','Representatives of a Carlist current may support the incumbent cabinet under a published agreement. A change of governing party or renewed electoral mandate ends the agreement.',25,
             flag('carlist_bargain_unlocked')+' COLDWAR_SPR_franco_has_left_office = yes',
             'NOT = { OR = { COLDWAR_SPR_carlist_traditionalists = yes COLDWAR_SPR_carlist_social_federalists = yes } }',
             'COLDWAR_SPR_request_carlist_agreement = yes')

    reform_authority=flag('reform_in_progress')+' check_variable = { COLDWAR_SPR_reform_generation = COLDWAR_SPR_government_generation } COLDWAR_SPR_franco_has_left_office = yes'
    referendum_authority=reform_authority+' '+flag('reform_referendum_pending')
    revision_authority=flag('revision_in_progress')+' check_variable = { COLDWAR_SPR_revision_generation = COLDWAR_SPR_government_generation }'
    republic_authority=flag('republic_vote_pending')+' check_variable = { COLDWAR_SPR_republic_generation = COLDWAR_SPR_government_generation } COLDWAR_SPR_representative_settlement = yes'
    mandate_authority=flag('mandate_pending')+' check_variable = { COLDWAR_SPR_mandate_generation = COLDWAR_SPR_government_generation } check_variable = { ruling_party = 1 }'
    carlist_authority=flag('carlist_negotiation_pending')+' check_variable = { COLDWAR_SPR_carlist_negotiation_generation = COLDWAR_SPR_government_generation }'

    event(1,'The Presidency Falls Vacant','Carrero Blanco has been killed. The government must preserve its chain of command while the Council of the Realm considers the presidency.',
          [('Apply the continuity protocol.','add_stability = -0.02',flag('continuity_protocol')),
           ('Reconstitute the administration.','add_stability = -0.05','NOT = { '+flag('continuity_protocol')+' }')])
    event(2,'A Serious Illness','The head of state has been admitted to hospital. The designated successor and ministers are preparing for a possible delegation of authority.',[('Keep the administration informed.','COLDWAR_SPR_sync_health = yes','')])
    event(3,'The Final Illness','The medical authorities report a critical decline. The Council of Regency and the government must be ready to apply the succession law.',[('Maintain the lawful chain of command.','COLDWAR_SPR_sync_health = yes','')])
    event(4,'The Transfer of Authority','Franco has died. The institutions must now conduct the affairs of state without his personal arbitration.',[('The state continues.','','')])
    event(5,'A New Head of State','Franco has relinquished office. The government and the institutions of state must now settle the distribution of authority without his final arbitration.',[('Apply the lawful handover.','','')])
    event(10,'The Political Reform Agreement','The government proposes legal guarantees for political association and a referendum on competitive representation. The Cortes will be asked to approve an orderly transfer of authority.',
          [('Submit the agreement to a public vote.','COLDWAR_SPR_legalise_parties = yes\n'+setflag('reform_referendum_pending')+'\ncountry_event = { id = COLDWAR_SPR_v2_politics.11 days = 60 }',''),
           ('Return the agreement for negotiation.',clearflag('reform_in_progress'),'')],authority=reform_authority)
    event(11,'The Reform Referendum','The proposed reform is before the electorate. Ratification authorises a competitive election and a constituent Cortes; the form of the headship remains open.',
          [('Ratify reform and call the election.',clearflag('reform_referendum_pending')+' COLDWAR_SPR_call_constituent_election = yes',''),
           ('Reopen negotiations.',clearflag('reform_referendum_pending')+' '+clearflag('reform_in_progress'),'')],authority=referendum_authority)
    event(12,'The Constituent Cortes','The election has returned a government and representatives authorised to settle the constitutional rules. The head of state and the cabinet must now promulgate the agreement.',
          [('Promulgate representative government.','COLDWAR_SPR_enact_legal_parliamentary = yes\n'+clearflag('reform_in_progress')+'\n'+clearflag('constituent_ratification_pending')+'\n'+clearflag('constituent_campaign_pending'),'')],trigger_code='COLDWAR_SPR_campaign = yes '+flag('reform_in_progress'),authority=flag('constituent_ratification_pending')+' check_variable = { COLDWAR_SPR_constituent_generation = COLDWAR_SPR_government_generation }')
    event(14,'A Revised Constitutional Pact','The government has completed negotiations with the institutions of state. The revised settlement will replace the previous constitutional terms.',
          [('Refer representative reform to the electorate.','COLDWAR_SPR_begin_legal_reform = yes\n'+clearflag('revision_in_progress'),'NOT = { COLDWAR_SPR_representative_settlement = yes }'),
           ('Adopt executive monarchy.','COLDWAR_SPR_enact_legal_royal = yes','check_variable = { ruling_party = 23 }'),
           ('Retain the Fundamental Laws.','COLDWAR_SPR_enact_legal_fundamental = yes','OR = { check_variable = { ruling_party = 21 } check_variable = { ruling_party = 22 } }'),
           ('Renew the representative pact.','COLDWAR_SPR_enact_legal_parliamentary = yes','COLDWAR_SPR_representative_settlement = yes'),
           ('Keep the existing settlement.',clearflag('revision_in_progress'),'')],authority=revision_authority)
    event(16,'The Republican Constitutional Vote','The constituent period has ended. The elected Cortes must ratify the transfer of the headship under the agreed constitutional guarantees.',
          [('Ratify the republic.',setflag('parliamentary_republic')+'\n'+clearflag('parliamentary_monarchy')+'\n'+clearflag('republic_vote_pending')+'\nremove_ideas = COLDWAR_SPR_republic_constituent_period\nCOLDWAR_SPR_enact_legal_parliamentary = yes','COLDWAR_SPR_representative_settlement = yes'),
           ('Retain the present headship.',clearflag('republic_vote_pending')+'\nremove_ideas = COLDWAR_SPR_republic_constituent_period','')],authority=republic_authority)
    event(20,'The Conservative Cabinet Mandate','The conservative parliamentary group must agree the political mandate of its cabinet. The Union of the Centre and Popular Alliance retain distinct leadership and programmes within this outlook.',
          [('A Union of the Centre cabinet.',setflag('mandate_ucd')+'\n'+clearflag('mandate_ap_pp')+'\n'+clearflag('mandate_pending')+'\nCOLDWAR_SPR_set_scenario_leader = yes',''),
           ('A Popular Alliance cabinet.',setflag('mandate_ap_pp')+'\n'+clearflag('mandate_ucd')+'\n'+clearflag('mandate_pending')+'\nCOLDWAR_SPR_set_scenario_leader = yes','')],trigger_code='COLDWAR_SPR_campaign = yes check_variable = { ruling_party = 1 }',authority=mandate_authority)
    carlist_stamp='clr_country_flag = COLDWAR_SPR_carlist_negotiation_pending\nset_variable = { COLDWAR_SPR_carlist_party = ruling_party }\nset_variable = { COLDWAR_SPR_carlist_generation = COLDWAR_SPR_government_generation }\nCOLDWAR_SPR_sync_programmes = yes'
    event(30,'A Carlist Cabinet Agreement','Carlist representatives offer support to the incumbent administration. Any agreement recognises their current within the existing political institutions and lasts for this governing mandate.',
          [('Recognise traditionalist support.',setflag('carlist_traditionalist_agreement')+'\n'+clearflag('carlist_social_federalist_agreement')+'\n'+carlist_stamp,'OR = { check_variable = { ruling_party = 1 } check_variable = { ruling_party = 21 } check_variable = { ruling_party = 22 } check_variable = { ruling_party = 23 } }'),
           ('Recognise social-federalist support.',setflag('carlist_social_federalist_agreement')+'\n'+clearflag('carlist_traditionalist_agreement')+'\n'+carlist_stamp,'COLDWAR_SPR_representative_settlement = yes OR = { check_variable = { ruling_party = 2 } check_variable = { ruling_party = 3 } check_variable = { ruling_party = 4 } }'),
           ('Govern without a Carlist agreement.',clearflag('carlist_negotiation_pending'),'')],trigger_code='COLDWAR_SPR_campaign = yes '+flag('carlist_bargain_unlocked')+' COLDWAR_SPR_franco_has_left_office = yes',authority=carlist_authority)

    # Historical roster has monotonic per-party indices and death-safe protection.
    roster = json.loads((HERE/'politics_roster.json').read_text(encoding='utf-8'))
    _leaders(roster,effect,trigger)
    daily='''COLDWAR_SPR_initialize = yes
if = { limit = { has_country_flag = COLDWAR_SPR_franco_incumbency NOT = { has_country_flag = COLDWAR_SPR_franco_departed } NOT = { has_country_leader = { name = "Francisco Franco" ruling_only = yes } } date < 1975.11.20 } COLDWAR_SPR_franco_departure = yes }
COLDWAR_SPR_health_daily = yes
COLDWAR_SPR_refresh_politics = yes
COLDWAR_SPR_retry_completed_focuses = yes
if = { limit = { has_country_flag = elections_in_progress } set_country_flag = COLDWAR_SPR_native_campaign_seen }
if = { limit = { has_country_flag = COLDWAR_SPR_native_campaign_seen NOT = { has_country_flag = elections_in_progress } NOT = { has_country_flag = coalition_forming } }
 clr_country_flag = COLDWAR_SPR_native_campaign_seen
 add_to_variable = { COLDWAR_SPR_government_generation = 1 }
 COLDWAR_SPR_invalidate_old_mandate = yes
 if = { limit = { check_variable = { ruling_party = 1 } } COLDWAR_SPR_request_mandate = yes }
 COLDWAR_SPR_refresh_politics = yes
}
if = { limit = { has_country_flag = COLDWAR_SPR_constituent_campaign_pending has_country_flag = elections_in_progress } set_country_flag = COLDWAR_SPR_constituent_campaign_seen }
if = { limit = { has_country_flag = COLDWAR_SPR_constituent_campaign_seen NOT = { has_country_flag = elections_in_progress } NOT = { has_country_flag = coalition_forming } }
 clr_country_flag = COLDWAR_SPR_constituent_campaign_seen
 set_country_flag = COLDWAR_SPR_constituent_ratification_pending
 set_variable = { COLDWAR_SPR_constituent_generation = COLDWAR_SPR_government_generation }
 country_event = { id = COLDWAR_SPR_v2_politics.12 }
}'''
    on_actions='on_actions = {\non_daily_SPR = { effect = { if = { limit = { COLDWAR_SPR_campaign = yes } '+daily+' } } }\n'+ \
      'on_monthly_SPR = { effect = { if = { limit = { COLDWAR_SPR_campaign = yes } COLDWAR_SPR_health_monthly = yes COLDWAR_SPR_historical_succession = yes } } }\n'+ \
      'on_ruling_party_change = { effect = { if = { limit = { COLDWAR_SPR_campaign = yes } COLDWAR_SPR_refresh_politics = yes } } }\n'+ \
      '}\n'
    output['common/scripted_effects/COLDWAR_SPR_v2_politics.txt']=HEADER+'\n'.join(effects)
    output['common/scripted_triggers/COLDWAR_SPR_v2_politics.txt']=HEADER+'\n'.join(triggers)
    output['common/ideas/COLDWAR_SPR_v2_politics.txt']=HEADER+'ideas = { country = {\n'+''.join(ideas)+'\n} }\n'
    output['common/decisions/categories/COLDWAR_SPR_v2_politics.txt']=HEADER+'COLDWAR_SPR_v2_politics = { icon = generic_political_actions allowed = { original_tag = SPR } visible = { COLDWAR_SPR_campaign = yes } }\n'
    local('COLDWAR_SPR_v2_politics','The State and Its Succession')
    local('COLDWAR_SPR_v2_politics_desc',"The head of state's capacity: §Y[?COLDWAR_SPR_capacity|0]/100§!\nSuccession preparedness: §Y[?COLDWAR_SPR_preparedness|0]/100§!\nPreparations preserve administrative continuity as authority passes between institutions.")
    output['common/decisions/COLDWAR_SPR_v2_politics.txt']=HEADER+'COLDWAR_SPR_v2_politics = {\n'+''.join(decisions)+'\n}\n'
    output['events/COLDWAR_SPR_v2_politics.txt']=HEADER+'add_namespace = COLDWAR_SPR_v2_politics\n'+''.join(events)
    output['common/on_actions/COLDWAR_SPR_v2_politics.txt']=HEADER+on_actions
    output['localisation/english/COLDWAR_SPR_v2_politics_l_english.yml']=('\ufeffl_english:\n '+HEADER+''.join(' '+k+':0 "'+v.replace('"','\\"').replace('\n','\\n')+'"\n' for k,v in loc.items())).encode('utf-8')
    output['tools/spain_1970_v2/politics_focus_map.json']=json.dumps(metadata,indent=2)+'\n'
    output['tools/spain_1970_v2/politics_previews.json']=json.dumps(decision_previews,indent=2)+'\n'
    return output

def _leaders(roster,effect,trigger):
    """The same provider serves native elections, retirement and delayed catch-up."""
    keep=[]; remember=[]; providers=[]; catchup=[]; retire=[]
    for family, rows in roster.items():
        slot=rows[0]['slot']; ordinal='COLDWAR_SPR_roster_'+family
        family_gate='check_variable = { ruling_party = '+str(slot)+' }'
        if family=='ucd': family_gate+=' NOT = { has_country_flag = COLDWAR_SPR_mandate_ap_pp }'
        if family=='ap_pp': family_gate+=' has_country_flag = COLDWAR_SPR_mandate_ap_pp'
        if family=='falange': family_gate+=' COLDWAR_SPR_franco_has_left_office = yes'
        for index,row in enumerate(rows,1):
            alive='date < '+row.get('death','2100.1.1')
            current='has_country_leader = { name = "'+row['name']+'" ruling_only = yes }'
            keep.append('AND = { '+family_gate+' '+alive+' '+current+' }')
            remember.append('if = { limit = { '+family_gate+' '+current+' check_variable = { '+ordinal+' < '+str(index)+' } } set_variable = { '+ordinal+' = '+str(index)+' } }')
            if index<len(rows):
                successor=rows[index]
                retire.append(('if' if not retire else 'else_if')+' = { limit = { '+family_gate+' '+current+' date < '+successor.get('death','2100.1.1')+' } set_variable = { '+ordinal+' = '+str(index+1)+' } }')
        choices=[]
        for index,row in reversed(list(enumerate(rows,1))):
            # Evaluate newest due first, never regress the persistent ordinal.
            gate='OR = { date > '+row['from']+' check_variable = { '+ordinal+' >= '+str(index)+' } } check_variable = { '+ordinal+' <= '+str(index)+' } date < '+row.get('death','2100.1.1')
            picture=(' picture = "'+row['picture']+'"') if row.get('picture') else ''
            create='create_country_leader = { name = "'+row['name']+'"'+picture+' ideology = '+row['ideology']+' expire = "'+row.get('death','2100.1.1')+'" }'
            choices.append(('if' if not choices else 'else_if')+' = { limit = { '+gate+' }\n'+create+'\nset_variable = { '+ordinal+' = '+str(index)+' }\n}')
        providers.append(('if' if not providers else 'else_if')+' = { limit = { '+family_gate+' }\n'+'\n'.join(choices)+'\n}')
        for index,row in reversed(list(enumerate(rows,1))):
            if index==1:continue
            catchup.append('if = { limit = { '+family_gate+' date > '+row['from']+' check_variable = { '+ordinal+' < '+str(index)+' } NOT = { COLDWAR_SPR_keep_current_incumbent = yes } } COLDWAR_SPR_dispatch_leader = yes }')
    trigger('COLDWAR_SPR_keep_current_incumbent','has_country_flag = do_not_retire OR = { AND = { COLDWAR_SPR_franco_in_office = yes check_variable = { ruling_party = 21 } has_country_leader = { name = "Francisco Franco" ruling_only = yes } } '+' '.join(keep)+' }')
    effect('COLDWAR_SPR_remember_incumbent','\n'.join(remember))
    effect('COLDWAR_SPR_advance_native_retirement','if = { limit = { check_variable = { MDCW_HP_native_retirement = 1 } NOT = { has_country_flag = do_not_retire } }\n'+'\n'.join(retire)+'\n}')
    effect('COLDWAR_SPR_set_scenario_leader','''if = { limit = { COLDWAR_SPR_franco_in_office = yes check_variable = { ruling_party = 21 } }
 create_country_leader = { name = "Francisco Franco" picture = "gfx/Leaders/SPR/SPR_Coldwar_FRANCO.dds" expire = "1975.11.20" ideology = Nat_Fascism }
}
else = {
'''+ '\n'.join(providers)+'''
}
update_party_name = yes
COLDWAR_SPR_refresh_politics = yes''')
    effect('COLDWAR_SPR_dispatch_leader','''if = { limit = { COLDWAR_SPR_campaign = yes }
 COLDWAR_SPR_remember_incumbent = yes
 COLDWAR_SPR_advance_native_retirement = yes
 if = { limit = { has_country_flag = COLDWAR_SPR_franco_incumbency NOT = { has_country_flag = COLDWAR_SPR_franco_departed } OR = { NOT = { check_variable = { ruling_party = 21 } } AND = { check_variable = { MDCW_HP_native_retirement = 1 } NOT = { has_country_flag = do_not_retire } } } } COLDWAR_SPR_franco_departure = yes }
 if = { limit = { date > 1975.11.19 NOT = { has_country_flag = COLDWAR_SPR_franco_departed } } set_country_flag = COLDWAR_SPR_franco_dead COLDWAR_SPR_franco_departure = yes }
 COLDWAR_SPR_observe_government = yes
 if = { limit = { OR = { COLDWAR_SPR_keep_current_incumbent = yes AND = { COLDWAR_SPR_franco_in_office = yes NOT = { check_variable = { MDCW_HP_native_retirement = 1 } } } } } update_set_politics = yes }
 else = { kill_country_leader = yes update_set_politics = yes COLDWAR_SPR_set_scenario_leader = yes set_correct_ideology_trait = yes }
 COLDWAR_SPR_refresh_politics = yes
}''')
    effect('COLDWAR_SPR_historical_succession','COLDWAR_SPR_remember_incumbent = yes\n'+'\n'.join(catchup))

if __name__=='__main__':
    root=HERE.parents[1]
    design=json.loads((HERE/'approved_design.json').read_text(encoding='utf-8-sig'))
    for rel,data in build(root,design).items():
        path=root/rel;path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data if isinstance(data,bytes) else data.encode('utf-8'))
