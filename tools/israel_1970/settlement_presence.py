# IMPERIA COLD WAR — Unilateral settlement encroachment and controlled-state development.
"""State-linked Israeli funding without a host-government permission transaction.

The no-control route is an explicit RP abstraction, not a claimed historical
agreement. Period precedents and balance terms are in UNILATERAL_SETTLEMENTS.md.
"""
import copy
from policy_common import ident, has, scope

AREAS = [(208,'west_bank','West Bank',7107,'PAL'),(209,'gaza','Gaza',13207,'PAL'),
         (213,'sinai','Sinai',10099,'EGY'),(587,'golan','Golan',13205,'SYR')]
ISRAEL_MODS={'offices_productivity':.04,'agricolture_productivity_modifier':.03,
             'social_cost_multiplier_modifier':.01,'bureaucracy_cost_multiplier_modifier':.01,
             'police_cost_multiplier_modifier':.02,'personnel_cost_multiplier_modifier':.01}
HOST_MODS={'agricolture_productivity_modifier':-.03,'bureaucracy_cost_multiplier_modifier':.025,
           'police_cost_multiplier_modifier':.02,'stability_factor':-.01}
LOCAL_MODS={'state_production_speed_infrastructure_factor':-.10,'local_factories':-.05,
            'local_supplies_for_controller':-.05}


def build(api):
    from occupation_profiles import build as occupation
    occupation(api)
    api.data['groups'].append(dict(id='policy_presence',label='Settlement Presence and Territorial Development',
        description='Unilateral settlement encroachment beyond Israeli control, or funded development under Israeli control.',
        outlook=None,party=None,trigger=None,history='Period settlement institutions with an explicit unilateral RP extension.'))
    template=copy.deepcopy(api.nodes['ISR70_land_survey']);created=[]

    def add(key,label,text,parents,xy,art,code,available='',summary=None,days=35):
        node=copy.deepcopy(template);helper=api.effect('complete_'+key,code)
        node.update(id='ISR70_'+key,group='policy_presence',label=label,description=text,note=text,
            prerequisites=parents,mutually_exclusive=[],modifiers={},reward=helper+' = yes',available=available,
            days=days,policy_key=key,policy_local_xy=list(xy),policy_effect=helper,
            policy_summary=summary or [],duration_days=None,icon=api.nodes[art]['icon'],art_source=api.nodes[art]['art_source'])
        for old in ('choice_group','policy_mutable_choice','additional_reward_summary'):node.pop(old,None)
        api.nodes[node['id']]=node;api.data['nodes'].append(node);created.append(node['id']);return node

    for key,label,xy,art in (
        ('external_associations','Settlement Division Networks',(0,0),'ISR70_diaspora_bonds'),
        ('controlled_settlement_engineering','Settlement Engineering Department',(0,4),'ISR70_negev_roads')):
        text=('Settlement departments, cooperative associations and private patrons can finance civilian footholds beyond Israel\'s military perimeter. Unilateral expansion creates competing land claims and imposes costs on the affected administration.' if key=='external_associations' else
              'Surveyors, water engineers and settlement departments can prepare funded agricultural sites and access roads in areas under Israeli control. Each project carries its own security and public-service commitment.')
        pay=api.money(.002)
        reward=('set_temp_variable = { temp_opinion = 5 } change_small_medium_business_owners_opinion = yes' if key=='external_associations' else
                'add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.25 }')
        add(key,label,text,[['ISR70_territorial_policy']],xy,art,
            'if = { limit = { ISR70_is_scenario = yes '+api._gates(pay)+' } '+pay+'\n'+reward+' }',available=api._gates(pay),
            summary=['Treasury: -0.2% of annual GDP.',('Small and Medium Business Owners Opinion: +5.' if key=='external_associations' else '1 x 25% construction research bonus.')],days=21)

    contracts=[]
    for index,(state,slug,label,province,origin) in enumerate(AREAS):
        pending=ident('presence_pending_'+str(state));active=ident('presence_established_'+str(state))
        paid=ident('presence_capital_paid_'+str(state));host_pending=ident('presence_offer_'+str(state))
        host_signed=ident('presence_host_'+str(state));target=ident('presence_partner_'+str(state))
        quote=ident('presence_quote_'+str(state));migration=ident('presence_unilateral_migrated_'+str(state))
        host_valid=api.trigger('presence_host_valid_'+str(state),
            f'country_exists = ISR NOT = {{ tag = ISR }} exists = yes controls_state = {state}')
        eligible=api.trigger('presence_eligible_'+str(state),
            f'has_variable = gdp_total check_variable = {{ gdp_total > 0 }} {state} = {{ NOT = {{ is_controlled_by = ISR }} controller = {{ {host_valid} = yes }} }}')
        api.loc(eligible+'_tt',label+' is controlled by another existing country.')
        api.triggers[eligible]='custom_trigger_tooltip = { tooltip = '+eligible+'_tt '+api.triggers[eligible]+' }'
        current=api.trigger('presence_active_'+str(state),
            f'country_exists = ISR ISR70_is_scenario = yes tag = ISR has_country_flag = {active} has_country_flag = {paid} {eligible} = yes')
        israel=api.state_modifier('presence_israel_'+str(state),label+': Israeli Settlement Holdings',
            'Israeli settlement holdings and commercial networks yield returns while requiring policing, personnel and civilian services.',ISRAEL_MODS,
            enable=f'tag = ISR {current} = yes')
        host=api.state_modifier('presence_host_budget_'+str(state),label+': Settlement Encroachment',
            'Unilateral Israeli settlement activity diverts agricultural resources, contests land administration and adds policing costs. The affected government has granted no permission.',HOST_MODS,
            enable=f'{host_valid} = yes ISR = {{ {current} = yes }}')
        local=api.state_modifier('presence_local_'+str(state),'Israeli Settlement Encroachment: '+label,
            'Contested land and protected settlement links disrupt local construction, industrial access and supply. Israeli commercial holdings are financed separately.',LOCAL_MODS,
            enable=f'NOT = {{ is_controlled_by = ISR }} controller = {{ {host_valid} = yes }} ISR = {{ {current} = yes }}')

        def rows(mods,prefix):
            return '\n'.join(f'add_to_variable = {{ ISR70_display_{prefix}_{state}_{key} = {value} tooltip = {tooltip(api,key)} }}' for key,value in mods.items())
        cash=f'''if = {{ limit = {{ ISR = {{ has_country_flag = {paid} }} }} set_temp_variable = {{ treasury_change = 0 }} }}
else = {{ set_temp_variable = {{ treasury_change = ISR.gdp_total }} multiply_temp_variable = {{ treasury_change = -0.01 }} }}
custom_effect_tooltip = modify_treasury_effect_tt'''
        preview='effect_tooltip = {\nISR = {\n'+cash+f'\ncustom_effect_tooltip = {{ localization_key = modifies_dynamic_modifier_tt MODIFIER = {israel} }}\n'+rows(ISRAEL_MODS,'israel')+'\n}\n'
        preview+=scope(state,f'custom_effect_tooltip = {{ localization_key = modifies_dynamic_modifier_tt MODIFIER = {local} }}\n'+rows(LOCAL_MODS,'local')+'\ncontroller = {\n'+f'custom_effect_tooltip = {{ localization_key = modifies_dynamic_modifier_tt MODIFIER = {host} }}\n'+rows(HOST_MODS,'host')+'\n}')+'\n'
        if state in (208,209):
            from palestinian_pressure import preview as palestinian_preview
            preview+=palestinian_preview(api,state,1,maximum=False)+'\n'
        preview+='}'
        cost=api.money(.01);afford='ISR70_policy_afford_'+api.cost_token(.01)
        gate=f'ISR70_is_scenario = yes tag = ISR {eligible} = yes NOT = {{ has_country_flag = {active} }}'
        # Recompute the current price inside execution. Only Israeli funds pay;
        # there is no recipient, acceptance, refusal, host grant or host veto.
        offer=api.effect('offer_presence_'+str(state),f'''if = {{ limit = {{ {gate} }}
set_variable = {{ {quote} = gdp_total }} multiply_variable = {{ {quote} = 0.01 }}
if = {{ limit = {{ has_country_flag = {paid} }} set_variable = {{ {quote} = 0 }} }}
if = {{ limit = {{ NOT = {{ has_active_mission = bankruptcy_incoming_collapse }} check_variable = {{ var = treasury value = {quote} compare = greater_than_or_equals }} }}
if = {{ limit = {{ NOT = {{ has_country_flag = {paid} }} }}
set_temp_variable = {{ treasury_change = {quote} }} multiply_temp_variable = {{ treasury_change = -1 }} modify_treasury_effect = yes
set_country_flag = {paid}
}}
set_country_flag = {active} clr_country_flag = {pending}
ISR70_policy_reconcile_presence = yes
}} }}''')
        # Retain the former helper ID as an inert save/reference compatibility stub.
        accept=api.effect('accept_presence_'+str(state),'# Superseded recipient transaction.\nhidden_effect = { }')
        cancel=api.effect('cancel_presence_'+str(state),f'''if = {{ limit = {{ tag = ISR ISR70_is_scenario = yes }}
clr_country_flag = {pending} clr_country_flag = {active}
ISR70_policy_reconcile_presence = yes
}}''')
        visible_gate=f'{eligible} = yes NOT = {{ has_country_flag = {active} }} OR = {{ hidden_trigger = {{ has_country_flag = {paid} }} {afford} = yes }}'
        fid='presence_'+slug
        summary=[f'Israel: "{label}: Israeli Settlement Holdings": Office Productivity +4%, Agricultural Productivity +3%, Social Costs +1%, Bureaucracy Cost +1%, Police Cost +2%, Personnel Cost +1%.',
            f'Affected government: "{label}: Settlement Encroachment": Agricultural Productivity -3%, Bureaucracy Cost +2.5%, Police Cost +2%, Stability -1%.',
            f'{label}: "Israeli Settlement Encroachment": Local Infrastructure Construction Speed -10%, Local Factory Access -5%, Local Supplies -5%.',
            'Israel Treasury: -1% of annual GDP for initial establishment.']
        if state in (208,209):
            from palestinian_pressure import summary as palestinian_summary
            summary.append(palestinian_summary(state,1))
        node=add(fid,'Establish a '+label+' Settlement Foothold',
            'Finance Israeli settlement holdings and protected commercial links in '+label+' without the consent of the government controlling the area. These illegal settlements impose land, production and administrative burdens on that government. Israel assumes the financial and security commitment.',
            [['ISR70_external_associations']],(-6+index*4,2),'ISR70_diaspora_bonds',
            preview+'\nhidden_effect = { '+offer+' = yes }',available=visible_gate,summary=summary)
        node['requirement_summary']=['Israel does not control '+label+'.','Another existing government controls the area.','The initial settlement funding can be covered.']
        api.decision('renew_presence_'+str(state),'Re-establish the '+label+' Settlement Presence',
            'Restore Israeli funding for the existing settlement holdings and commercial links. The affected government does not authorize this programme.',fid,
            visible_gate,preview+'\nhidden_effect = { '+offer+' = yes }',cost=25,repeatable=True,cooldown=90)
        api.decision('end_presence_'+str(state),'End Israeli Settlement Funding in '+label,
            'End this foreign settlement programme and its associated commercial returns. The original investment is not refunded.',fid,
            'has_country_flag = '+active,cancel+' = yes',repeatable=True,cooldown=7)

        # Controlled development grants assets only in the named controlled
        # state. It cannot bypass a binding freeze in the selected project area.
        develop='develop_'+slug;receipt=ident('project_controlled_'+slug+'_done')
        controlled_gate=f'OR = {{ {state} = {{ is_owned_by = {origin} }} {state} = {{ is_owned_by = ISR }} }}'
        if state in (208,209):
            controlled_gate+='\nNOT = { AND = { '+has('target_'+str(state))+' OR = { '+has('freeze_agreed')+' '+has('binding_settlement_ceiling')+' } } }'
        advantage=api.state_modifier('controlled_settlement_'+str(state),label+': Settlement Supply Stations',
            'Funded farms and protected access roads improve local supply while extending the garrison perimeter.',
            {'local_supplies_for_controller':.10,'required_garrison_factor':.10},
            enable=f'is_controlled_by = ISR ISR = {{ ISR70_is_scenario = yes }}')
        node=add(develop,'Develop Settlement Sites in '+label,
            'Fund an agricultural site, an access road and a protected local position in '+label+'. The resulting assets remain in the state; their security perimeter adds to the burden of occupation.',
            [['ISR70_controlled_settlement_engineering']],(-6+index*4,6),'ISR70_negev_agriculture','',
            available=f'{state} = {{ is_controlled_by = ISR }}\n'+controlled_gate,summary=[])
        node['requirement_summary']=['Israel controls '+label+'.','A binding freeze or settlement ceiling in this project area prevents new construction.']
        unlock=api.project('controlled_'+slug,state,[{'type':'agriculture_district','levels':1},{'type':'infrastructure','levels':1},{'type':'bunker','levels':1,'province':province}],
            .015,270,after=scope(state,'add_dynamic_modifier = { modifier = '+advantage+' scope = ISR }'),available=controlled_gate,political_cost=25,unlock=develop)
        api.effects[node['policy_effect']]=unlock
        contracts.append(dict(state=state,slug=slug,label=label,focus='ISR70_'+fid,controlled_focus='ISR70_'+develop,
            host_target=target,pending=pending,active=active,paid=paid,host_pending=host_pending,host_signed=host_signed,migration=migration,
            quote=quote,eligible=eligible,current=current,host_valid=host_valid,israel_modifier=israel,
            host_modifier=host,state_modifier=local,offer=offer,accept=accept,cancel=cancel,preview=preview,
            israel_modifiers=ISRAEL_MODS,host_modifiers=HOST_MODS,state_modifiers=LOCAL_MODS))

    reconcile=[]
    for c in contracts:
        s=c['state'];isr=c['israel_modifier'];host=c['host_modifier'];local=c['state_modifier'];target=c['host_target']
        reconcile.append(f'''if = {{ limit = {{ NOT = {{ has_country_flag = {c['migration']} }} }}
clr_country_flag = {c['pending']}
if = {{ limit = {{ has_event_target = {target} country_exists = event_target:{target} }} event_target:{target} = {{ clr_country_flag = {c['host_pending']} clr_country_flag = {c['host_signed']} update_money_dirty_variable = yes }} }}
update_money_dirty_variable = yes
set_country_flag = {c['migration']}
}}
if = {{ limit = {{ has_event_target = {target} country_exists = event_target:{target} }} event_target:{target} = {{
if = {{ limit = {{ has_dynamic_modifier = {{ modifier = {host} }} NOT = {{ AND = {{ {c['host_valid']} = yes ISR = {{ {c['current']} = yes }} }} }} }}
remove_dynamic_modifier = {{ modifier = {host} }} update_money_dirty_variable = yes
}} }} }}
if = {{ limit = {{ {c['current']} = yes }}
if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {isr} }} }} }} add_dynamic_modifier = {{ modifier = {isr} }} update_money_dirty_variable = yes }}
{s} = {{
if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {local} }} }} }} add_dynamic_modifier = {{ modifier = {local} }} }}
controller = {{
if = {{ limit = {{ NOT = {{ has_event_target = {target} }} }} update_money_dirty_variable = yes }}
else_if = {{ limit = {{ has_event_target = {target} NOT = {{ country_exists = event_target:{target} }} }} update_money_dirty_variable = yes }}
else_if = {{ limit = {{ has_event_target = {target} country_exists = event_target:{target} NOT = {{ tag = event_target:{target} }} }} update_money_dirty_variable = yes }}
save_global_event_target_as = {target}
if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {host} }} }} }} add_dynamic_modifier = {{ modifier = {host} }} update_money_dirty_variable = yes }}
}} }}
}} else = {{
if = {{ limit = {{ has_dynamic_modifier = {{ modifier = {isr} }} }} remove_dynamic_modifier = {{ modifier = {isr} }} update_money_dirty_variable = yes }}
{s} = {{ if = {{ limit = {{ has_dynamic_modifier = {{ modifier = {local} }} }} remove_dynamic_modifier = {{ modifier = {local} }} }} }}
}}''')
    api.effect('reconcile_presence','\n'.join(reconcile));api.tick.append('ISR70_policy_reconcile_presence = yes')
    api.presence_responses='ISR70_presence_responses = { }';api.additional_decision_count=0
    api.data['settlement_presence']={'project':'IMPERIA COLD WAR','revision':2,'focuses':created,'contracts':contracts,
        'capital_share':.01,'recipient_decisions':0,'alternative_history':True,'unilateral':True,
        'host_receives_capital':False,'host_scope':'actual state controller',
        'source_record':'docs/israel_1970_design/UNILATERAL_SETTLEMENTS.md'}


def tooltip(api,key):
    if key in ('offices_productivity','bureaucracy_cost_multiplier_modifier','police_cost_multiplier_modifier',
               'personnel_cost_multiplier_modifier','stability_factor'):return key+'_tt'
    native={'social_cost_multiplier_modifier':'social_cost_multiplier_modifier',
            'agricolture_productivity_modifier':'agricolture_productivity_modifier',
            'state_production_speed_infrastructure_factor':'modifier_state_production_speed_infrastructure_factor',
            'local_factories':'MODIFIER_LOCAL_FACTORIES','local_supplies_for_controller':'MODIFIER_LOCAL_SUPPLIES_FOR_CONTROLLER'}
    loc=ident('display_'+key+'_tt')
    if loc not in api.localisation:
        api.loc(loc,'$'+native[key]+'$: $RIGHT|'+('-=' if key.endswith('cost_multiplier_modifier') else '+=')+'%1$')
    return loc
