# IMPERIA COLD WAR — Regional diplomacy, legacy migration and country lifecycle.
from .shared import *
from .deals import DEALS,preview,locals_for,local_relevant
from .aid import preview as aid_preview
from . import fiscal

def build(loc,fx,tr,ideas,decisions):
    rights_mods={'Stability':.03,'Police Cost':-.05,'Bureaucracy Cost':.02}
    loc[P+'domestic_rights']='Regional Political Settlement'
    loc[P+'domestic_rights_desc']='Agreed local rights and regional institutions address the political grievances behind the armed movement.'
    loc[P+'domestic_rights_weekly_tt']=fiscal.weekly_text('rights')
    ideas.append(idea('domestic_rights','','',rights_mods,weekly=True))
    domestic_reconcile=[];domestic_streams=[]
    # Live quote and display refreshes are cheap, country-local and independent
    # of whether the player currently has the decision window open.
    quote=P+'refresh_fiscal_host = yes'
    view='\n'.join([f'set_temp_variable = {{ {P}old_unrest = {P}ui_unrest }}',f'set_temp_variable = {{ {P}old_legacy = {P}ui_legacy }}',f'set_temp_variable = {{ {P}old_warning = {P}ui_warning }}',
      f'set_variable = {{ {P}ui_unrest = {P}unrest }}',f'round_variable = {P}ui_unrest',v('ui_legacy',0),
      guard(check('stabilisation','>',50),v('ui_legacy',2))+'\n'+b('else_if',[b('limit',check('stabilisation','>',5)),v('ui_legacy',1)]),
      v('ui_warning',0),guard(flag('warning'),v('ui_warning',1)),
      guard('OR = { NOT = { check_variable = { '+P+'ui_unrest = '+P+'old_unrest } } NOT = { check_variable = { '+P+'ui_legacy = '+P+'old_legacy } } NOT = { check_variable = { '+P+'ui_warning = '+P+'old_warning } } }',add('ui_dirty',1))])
    fx[P+'refresh_host']=quote+'\n'+view
    fx[P+'migrate_irq']=migration_script()
    tr[P+'legacy_irq_ready']=P+'usa_actor = yes\nhidden_trigger = { has_country_flag = COLDWAR_USA_gulf_programme_arm_front }\n'+P+'route_irq = yes\nNOT = { '+P+'rights_irq = yes }\nOR = { '+check('stage_irq','>',0)+' '+P+'slot_available = yes }\nOR = { '+P+'region_irq = yes KUR = { COLDWAR_USA_gulf_local_actor = yes } PUK = { COLDWAR_USA_gulf_local_actor = yes } }\ncustom_trigger_tooltip = { tooltip = '+P+'equipment_tt has_equipment = { infantry_weapons_1 > 999 } }'
    tr[P+'legacy_irq_ready']+='\n'+fiscal.affordable('us_legacy_quote')
    legacy_assets=P+'init_irq = yes\nadd_political_power = -25\nadd_equipment_to_stockpile = { type = infantry_weapons_1 amount = -1000 }\n'+add('cache_irq',1000)+'\nset_variable = { '+P+'legacy_irq_cash = '+P+'invoice }\n'+v('legacy_irq_rate',1)+'\n'+v('stage_irq',3)+'\n'+v('max_stage_irq',3)+'\n'+setflag('contact_irq')+'\n'+setflag('legacy_gulf_paid')+'\nclr_country_flag = '+P+'legacy_gulf_pending\nset_country_flag = COLDWAR_USA_gulf_initial_package_used\n'+P+'count_campaigns = yes\n'+P+'reconcile_aid = yes'
    legacy_execution=fiscal.purchase(fiscal.US_SETUP['legacy'],legacy_assets)
    fx[P+'legacy_irq_start']=P+'count_campaigns = yes\n'+guard(P+'legacy_irq_ready = yes\n'+noflag('legacy_gulf_paid'),legacy_execution)
    fx[P+'legacy_irq_preview']=effect_preview('add_political_power = -25\n'+fiscal.cost_rows(fiscal.US_SETUP['legacy'])+'\nadd_equipment_to_stockpile = { type = infantry_weapons_1 amount = -1000 }\n'+scalar_row('material',1000)+'\n'+fiscal.weekly_rows('us_legacy'))+'\n'+\
       '\n'.join(aid_preview('irq',t,'legacy') for t in ('KUR','PUK'))+'\nunlock_decision_tooltip = '+P+'irq_cache_kur\nunlock_decision_tooltip = '+P+'irq_cache_puk'
    loc[P+'enact_gulf']='Enact the northern military commitment';loc[P+'enact_gulf_desc']='Carry the authorised wartime assistance programme into effect when the necessary route and equipment are available.'
    decisions.append(b(P+'enact_gulf',['icon = GFX_decision_generic_political_discourse',b('visible',P+'usa_actor = yes\n'+flag('legacy_gulf_pending')+'\n'+noflag('legacy_gulf_paid')),b('available',P+'legacy_irq_ready = yes'),'cost = 0',b('complete_effect',visible_and_hidden(P+'legacy_irq_preview = yes',P+'legacy_irq_start = yes')),'ai_will_do = { factor = 1 }']))
    loc[P+'per_breach']='Break with Tehran';loc[P+'per_breach_desc']='Abandon cooperation with the Iranian government and authorise contacts with its regional opponents. Such a decision damages American credibility with its partners.'
    valid=P+'usa_actor = yes\nhas_completed_focus = '+P+'kurds\ncountry_exists = PER\n'+noflag('breach_per')
    body=setflag('breach_per')+'\nadd_timed_idea = { idea = '+P+'credibility_crisis days = 180 }\nadd_opinion_modifier = { target = PER modifier = '+P+'breach_opinion }\nPER = { add_opinion_modifier = { target = USA modifier = '+P+'breach_opinion } }\n'+P+'reconcile_deals = yes'
    decisions.append(b(P+'per_breach',['icon = GFX_decision_generic_political_discourse',b('visible',valid),'cost = 150',b('complete_effect',visible_and_hidden(effect_preview('add_timed_idea = { idea = '+P+'credibility_crisis days = 180 }\n'+modifier_rows({'Foreign Influence':-.10})+'\nadd_opinion_modifier = { target = PER modifier = '+P+'breach_opinion }'),guard(valid,body))),'ai_will_do = { factor = 0 }']))
    # An Iraqi political framework precedes the separate US guarantee focus.
    loc[P+'irq_offer_framework']='Propose a northern political settlement';loc[P+'irq_offer_framework_desc']='Invite Baghdad and the regional representatives to negotiate local rights within Iraq.'
    valid=P+'usa_actor = yes\nhas_completed_focus = '+P+'irq_autonomy\ncountry_exists = IRQ'
    decisions.append(b(P+'irq_offer_framework',['icon = GFX_decision_generic_political_discourse',b('visible',valid),b('available','IRQ = { NOT = { '+flag('framework_irq_pending')+' } NOT = { '+flag('framework_irq_accepted')+' } }'),'cost = 0',b('complete_effect',b('hidden_effect',guard(valid,'IRQ = { '+setflag('framework_irq_pending')+'\ncountry_event = { id = COLDWAR_USA_KS.102 } }'))),'ai_will_do = { factor = 1 }']))
    loc[P+'irq_accept_framework']='Accept northern political talks';loc[P+'irq_accept_framework_desc']='Accept a framework of local rights and negotiations. Any existing regional government must also approve its part of the settlement.'
    valid='tag = IRQ\n'+flag('framework_irq_pending')
    accept=setflag('framework_irq_accepted')+f'\nclr_country_flag = {P}framework_irq_pending'
    for t in ('KUR','PUK'):accept+='\n'+guard(local_relevant(t,'irq'),b(t,setflag('rights_irq_pending')))
    decisions.append(b(P+'irq_accept_framework',['icon = GFX_decision_generic_political_discourse',b('visible',valid),'cost = 0',b('complete_effect',visible_and_hidden(effect_preview(scalar_row('unrest',-25)),guard(valid,accept+'\n'+add('unrest',-25)+f'\nclamp_variable = {{ var = {P}unrest min = 0 max = 100 }}'))),'ai_will_do = { factor = 1 }']))
    loc[P+'irq_decline_framework']='Decline northern political talks';loc[P+'irq_decline_framework_desc']='Reject the proposed framework and retain the current regional policy.'
    decisions.append(b(P+'irq_decline_framework',['icon = GFX_decision_generic_political_discourse',b('visible',valid),'cost = 0',b('complete_effect',b('hidden_effect',f'clr_country_flag = {P}framework_irq_pending')),'ai_will_do = { factor = 0.5 }']))
    for h,d in HOSTS.items():
        tag=d['tag'];deal='irq_settlement' if h=='irq' else d['rights']
        consensus='\n'.join('OR = { NOT = { '+local_relevant(t,h)+' } '+t+' = { '+flag('rights_'+h+'_consent')+' } }' for t in locals_for(h))
        tr[P+'domestic_rights_'+h]=tag+' = { '+flag('domestic_rights_signed')+' }\n'+consensus
        tr[P+'rights_'+h]='OR = { AND = { '+tr[P+'rights_'+h]+' } '+P+'domestic_rights_'+h+' = yes }'
        formal='USA = { '+P+'deal_'+deal+'_active = yes }'
        ensure=guard(P+'domestic_rights_'+h+' = yes\nNOT = { '+formal+' }','add_ideas = '+P+'domestic_rights')+'\n'+b('else','remove_ideas = '+P+'domestic_rights')
        domestic_reconcile.append(guard('tag = '+tag,ensure))
        domestic_streams.append(guard('tag = '+tag+'\n'+P+'domestic_rights_'+h+' = yes\nNOT = { '+formal+' }',fiscal.stream('expense','rights')))
        fx[P+'local_rights_preview_'+h]=guard('USA = { '+flag('deal_'+deal+'_signed')+' }',preview(deal))+'\n'+b('else',effect_preview(tag+' = { add_ideas = '+P+'domestic_rights\n'+modifier_rows(rights_mods)+'\n'+fiscal.weekly_rows('rights')+' }'))
        ender=f'clr_country_flag = {P}rights_{h}_pending\nclr_country_flag = {P}rights_{h}_consent\n{tag} = {{ clr_country_flag = {P}domestic_rights_signed clr_country_flag = {P}rights_{h}_accepted remove_ideas = {P}domestic_rights }}\nUSA = {{ {P}deal_{deal}_end = yes {P}reconcile_deals = yes }}'
        fx[P+'local_rights_end_'+h]=guard('OR = { '+' '.join('tag = '+t for t in locals_for(h))+' }\nOR = { '+flag('rights_'+h+'_pending')+' '+flag('rights_'+h+'_consent')+' }',ender)
        key=P+h+'_autonomy';loc[key]='Offer a regional political settlement';loc[key+'_desc']='Offer local rights and regional institutions as an alternative to continued security operations. Existing regional authorities decide whether to accept the proposed settlement.'
        valid='tag = '+tag+'\n'+flag('tracked')+'\n'+noflag('domestic_rights_signed')+'\ncheck_variable = { gdp_total > 0 }\n'+at_least('treasury',P+'investment_quote')
        execute=setflag('domestic_rights_signed')+'\n'+setflag('rights_'+h+'_accepted')
        for t in locals_for(h):execute+='\n'+guard(local_relevant(t,h),b(t,f'clr_country_flag = {P}rights_{h}_consent\n'+setflag('rights_'+h+'_pending')))
        execute+='\n'+P+'reconcile_domestic = yes\nupdate_money_dirty_variable = yes'
        execute=fiscal.purchase(1,execute)
        proposal=effect_preview(fiscal.cost_rows(1)+'\ncustom_effect_tooltip = '+P+'if_accept_tt\nadd_ideas = '+P+'domestic_rights\n'+modifier_rows(rights_mods)+'\n'+fiscal.weekly_rows('rights'))
        decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible','tag = '+tag+'\n'+flag('tracked')),b('available',valid),'cost = 75',b('complete_effect',visible_and_hidden(proposal,guard(valid,execute))),'ai_will_do = { factor = 1 }']))
        key=P+h+'_end_rights';loc[key]='Withdraw the regional political offer';loc[key+'_desc']='End the political settlement and its continuing regional budget. Local grievances may return as earlier stabilisation fades.'
        end=f'clr_country_flag = {P}domestic_rights_signed\nremove_ideas = {P}domestic_rights\nupdate_money_dirty_variable = yes\n'+'\n'.join(b(t,f'clr_country_flag = {P}rights_{h}_pending\nclr_country_flag = {P}rights_{h}_consent') for t in locals_for(h))
        decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible','tag = '+tag+'\n'+flag('domestic_rights_signed')),'cost = 0',b('complete_effect',b('hidden_effect',end)),'ai_will_do = { factor = 0 }']))
        key=P+h+'_air_route';loc[key]='Covert air supply: '+d['name'];loc[key+'_desc']='Prepare an alternative paid supply route using American transport aircraft and airfields. Continuing flights carry a separate weekly logistics expense.'
        valid=P+'usa_actor = yes\n'+flag('contact_'+h)+'\n'+noflag('air_route_'+h)+'\nhas_equipment = { transport_plane1 > 4 }\nany_owned_state = { air_base > 0 is_controlled_by = USA }'
        valid+='\n'+fiscal.affordable('us_air_route_quote')
        decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible',P+'usa_actor = yes\n'+flag('contact_'+h)),b('available',valid),'cost = 25',b('complete_effect',visible_and_hidden(effect_preview(fiscal.cost_rows(fiscal.US_SETUP['air_route'])+'\n'+fiscal.weekly_rows('us_air')),guard(valid,fiscal.purchase(fiscal.US_SETUP['air_route'],setflag('air_route_'+h))))),'ai_will_do = { factor = 1 }']))
        if h in ('irq','syr'):
            key=P+h+'_challenge';loc[key]='Authorise regional pressure: '+d['name'];loc[key+'_desc']='Authorise a deliberate confrontation with the regional government and its policies toward local political movements.'
            valid=P+'usa_actor = yes\n'+flag('contact_'+h)+'\n'+noflag('breach_'+h)+'\ncountry_exists = '+d['tag']
            body=setflag('breach_'+h)+'\nadd_opinion_modifier = { target = '+d['tag']+' modifier = '+P+'breach_opinion }\n'+d['tag']+' = { add_opinion_modifier = { target = USA modifier = '+P+'breach_opinion } }'
            decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible',valid),'cost = 75',b('complete_effect',visible_and_hidden(effect_preview('add_opinion_modifier = { target = '+d['tag']+' modifier = '+P+'breach_opinion }'),guard(valid,body))),'ai_will_do = { factor = 0.2 }']))
        if h!='irq':
            key=P+h+'_mediation';loc[key]='Regional mediation: '+d['name'];loc[key+'_desc']='Offer a negotiated settlement to the regional government and its local political representatives.'
            valid=P+'usa_actor = yes\nhas_completed_focus = '+P+'shuttle\n'+P+'region_'+h+' = yes\nNOT = { has_completed_focus = '+P+d['front']+' }\n'+P+'deal_'+d['rights']+'_can_offer = yes'
            decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible',P+'usa_actor = yes\nhas_completed_focus = '+P+'shuttle'),b('available',valid),'cost = 25',b('complete_effect',visible_and_hidden(preview(d['rights']),guard(valid,P+'deal_'+d['rights']+'_offer = yes'))),'ai_will_do = { factor = 1 }']))
        # Local RP authorities can withdraw their settlement consent without
        # needing either Washington or the former central government to agree.
        for t in locals_for(h):
            key=P+h+'_withdraw_rights_'+t.lower();loc[key]='Withdraw from the regional settlement';loc[key+'_desc']='Withdraw our representatives from the standing political arrangement.'
            valid=f'tag = {t}\n'+flag('rights_'+h+'_consent')
            deal='irq_settlement' if h=='irq' else d['rights']
            decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible',valid),'cost = 0',b('complete_effect',b('hidden_effect',P+'local_rights_end_'+h+' = yes')),'ai_will_do = { factor = 0 }']))
    # The Chilean programme affects the actual opposition environment. It does
    # not change the government, trigger a coup or copy any local party identity.
    loc[P+'chile_pressure']='Foreign-Funded Political Opposition';loc[P+'chile_pressure_desc']='Outside support for political and media networks increases pressure on the government and the cost of policing political conflict.'
    ideas.append(idea('chile_pressure','','',{'Stability':-.03,'Police Cost':.02},'COLDWAR_USA_KS_institutions'))
    loc[P+'chile_end']='End Chilean political funding';loc[P+'chile_end_desc']='Withdraw the standing American subsidy to the Chilean political programme.'
    decisions.append(b(P+'chile_end',['icon = GFX_decision_generic_political_discourse',b('visible',P+'usa_actor = yes\n'+flag('chile_funding')),'cost = 0',b('complete_effect',b('hidden_effect',f'clr_country_flag = {P}chile_funding\nCHL = {{ remove_ideas = {P}chile_pressure }}\nupdate_money_dirty_variable = yes')),'ai_will_do = { factor = 0 }']))
    loc[P+'chile_funding']='Fund Chilean political networks';loc[P+'chile_funding_desc']="Restore the American programme of political and media assistance to a hostile government's opponents."
    valid=P+'usa_actor = yes\nhas_completed_focus = '+P+'chile\n'+noflag('chile_funding')+'\nCHL = { exists = yes }'
    decisions.append(b(P+'chile_funding',['icon = GFX_decision_generic_political_discourse',b('visible',P+'usa_actor = yes\nhas_completed_focus = '+P+'political'),b('available',valid),'cost = 25',b('complete_effect',visible_and_hidden(effect_preview(fiscal.weekly_rows('us_chile')),guard(valid,setflag('chile_funding')))),'ai_will_do = { factor = 1 }']))
    fx[P+'misc_reconcile']=guard('tag = USA\nIMP_is_1970_scenario = yes',
      guard(flag('chile_funding')+'\ncountry_exists = CHL\nCHL = { NOT = { '+flag('finance_oversight')+' } }','CHL = { add_ideas = '+P+'chile_pressure }')+'\n'+b('else','CHL = { remove_ideas = '+P+'chile_pressure }'))
    loc[P+'chile_oversight']='Political Finance Oversight';loc[P+'chile_oversight_desc']='Fund a year of investigations into foreign political financing and enforce transparent accounts for political organisations. Continued foreign funding can rebuild its networks when this oversight ends.'
    valid='tag = CHL\nhas_idea = '+P+'chile_pressure\ncheck_variable = { treasury > '+P+'investment_quote }'
    execute=fiscal.purchase(1,'set_country_flag = { flag = '+P+'finance_oversight value = 1 days = 365 }\nremove_ideas = '+P+'chile_pressure')
    decisions.append(b(P+'chile_oversight',['icon = GFX_decision_generic_political_discourse',b('visible','tag = CHL\nUSA = { '+flag('chile_funding')+' }'),b('available',valid),'cost = 50',b('complete_effect',visible_and_hidden(effect_preview(fiscal.cost_rows(1)+'\nremove_ideas = '+P+'chile_pressure'),guard(valid,execute))),'ai_will_do = { factor = 1 }']))
    fx[P+'reconcile_domestic']='\n'.join(domestic_reconcile)
    fx[P+'domestic_streams']='\n'.join(domestic_streams)

def regional_research():
    # The existing KUR/PUK minimum, without the Jan-1-only country dispatcher.
    # A local authority receives early technical knowledge, never free stores.
    techs=('mdcw_infantry_weapons_1940','mdcw_util_vehicle_1940','mdcw_cnc_equipment_1940',
      'mdcw_support_weapons_1940','mdcw_special_forces_1940','mdcw_camouflage_1940',
      'mdcw_body_armor_1945','mdcw_anti_tank_1940')
    return b('set_technology',['popup = no',*(key+' = 1' for key in techs)])+'\n'+\
      guard('has_dlc = "No Step Back"',b('set_technology','popup = no\nmdcw_nsb_anti_air_1940 = 1'))+'\n'+\
      b('else',b('set_technology','popup = no\nmdcw_anti_air_1940 = 1'))

def country_init():
    # Called only for a country that did not exist before this uprising. Never
    # use broad civil-war/startup replication helpers on an existing RP player.
    return '\n'.join(['set_variable = { treasury = 0 }','set_variable = { debt = 0 }','set_variable = { int_investments = 0 }',
      'set_variable = { nation_to_copy_from = 0 }','set_variable = { corporate_tax_rate = 20 }','set_variable = { population_tax_rate = 20 }',
      'set_variable = { domestic_influence_amount = 100 }','set_popularities = { neutrality = 100 }','set_politics = { ruling_party = neutrality elections_allowed = no }',
      'start_politics_input = yes','set_variable = { party_pop_array^18 = 1 }','set_variable = { ruling_party = 18 }','startup_politics = yes',
      'setup_employment_variables = yes','set_law_vars = yes','currency_startup = yes','ingame_update_setup = yes',
      'set_variable = { gdpc_converging_var = gdp_per_capita }','init_auto_influence_array = yes','ingame_init_investment_system = yes','research_slot_init_for_country = yes','setup_init_factions = yes',
      'set_variable = { last_quarter_gdp_total = gdp_total }','set_variable = { last_quarter_gdpc_total = gdp_per_capita }',
      P+'regional_research = yes',setflag('regional_actor'),
      'if = { limit = { NOT = { is_in_array = { array = global.Unrecognised_States value = THIS } } } add_to_array = { array = global.Unrecognised_States value = THIS } }'])

def migration_script():
    """Convert existing receipts without another invoice, cache or army grant."""
    old='COLDWAR_USA_gulf_'
    cache=[setflag('legacy_cache_migrated'),f'add_to_variable = {{ {P}cache_irq = {old}cache }}',
        guard(f'check_variable = {{ {old}support_days > 0 }}',
            v('stage_irq',2)+'\n'+v('max_stage_irq',2)+'\n'+v('legacy_irq_rate',1)),
        f'set_variable = {{ {old}cache = 0 }}']
    liaison=[setflag('legacy_liaison_migrated')]
    for i,t in enumerate(('KUR','PUK')):
        body=[v('stage_irq',2),v('max_stage_irq',2),v('legacy_irq_rate',1),
            'clear_array = '+P+'payees_irq',f'add_to_array = {{ array = {P}payees_irq value = {t} }}',
            b(t,[setflag('partner_irq'),guard('has_country_flag = '+old+'organized_opposition',setflag('participate_irq'))])]
        liaison.append(b('if' if i==0 else 'else_if',[b('limit','has_country_flag = '+old+'support_'+t.lower()),'\n'.join(body)]))
    liaison += ['clr_country_flag = '+old+'support_kur','clr_country_flag = '+old+'support_puk',
        'KUR = { remove_ideas = COLDWAR_KUR_us_advisers }','PUK = { remove_ideas = COLDWAR_KUR_us_advisers }']
    for t in ('KUR','PUK'):
        liaison.append(guard(t+' = { OR = { has_country_flag = '+old+'cache_received has_country_flag = '+old+'initial_aid_received } }',
            v('delivered_irq_'+t.lower(),1000)+'\n'+t+' = { '+setflag('partner_irq')+' }'))
    us=[P+'init_irq = yes',guard(noflag('legacy_cache_migrated'),'\n'.join(cache)),
        guard(noflag('legacy_liaison_migrated'),'\n'.join(liaison)),
        f'set_variable = {{ {old}support_days = 0 }}',P+'count_campaigns = yes']
    states=HOSTS['irq']['states']
    unrest=[setflag('legacy_unrest_migrated'),
        guard('OR = { '+' '.join(str(s)+' = { has_resistance = yes resistance > 79 }' for s in states)+' }',v('unrest',80))]
    cleanup=[]
    for s in states:
        clean=guard('has_state_flag = '+old+'owns_forced_override\nNOT = { has_state_flag = MD_protests_active@IRQ }',
            'force_enable_resistance = { clear = yes occupier = IRQ }\n'+guard('is_owned_and_controlled_by = IRQ','cancel_resistance = yes')+'\nclr_state_flag = '+old+'owns_forced_override')
        cleanup.append(b(str(s),guard('OR = { has_state_flag = '+old+'seeded has_state_flag = '+old+'owns_forced_override }',
            'clr_state_flag = '+old+'seeded\nremove_resistance_target = 19709101\nremove_resistance_target = 19709102\n'+clean)))
    security=[setflag('legacy_security_migrated'),
        guard('OR = { has_idea = '+old+'security_small has_idea = '+old+'security_major }',setflag('security')+'\nadd_ideas = '+P+'security_programme'),
        guard('OR = { '+' '.join(str(s)+' = { check_variable = { '+old+'security_local_days > 29 } }' for s in states)+' }',v('stabilisation',15)),
        'remove_ideas = '+old+'security_small','remove_ideas = '+old+'security_major','clr_country_flag = '+old+'security_delivery',
        '\n'.join(str(s)+' = { remove_resistance_target = 19709102 }' for s in states)]
    host=[guard(noflag('legacy_unrest_migrated'),'\n'.join(unrest)),guard(noflag('legacy_security_migrated'),'\n'.join(security)),'\n'.join(cleanup),P+'refresh_host = yes']
    condition='IMP_is_1970_scenario = yes\ncountry_exists = IRQ\nOR = { IRQ = { COLDWAR_IRQ_campaign_active = yes } IRQ = { has_country_flag = '+old+'northern_campaign_tracked } USA = { check_variable = { '+old+'cache > 0 } } }'
    return guard(condition,b('USA',us)+'\n'+b('IRQ',host))
