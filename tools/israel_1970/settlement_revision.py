# IMPERIA COLD WAR — Israel 1970 settlement depth and diaspora finance.
"""Authored 1967-1973 policy choices. Values are gameplay balance proposals.

Historical rationale and source/API evidence are recorded in
docs/israel_1970_design/REWORK_20261027.md. No population or sovereignty is
created by this revision. Construction is handled by the funded project API.
"""
from policy_common import focus_id, ident, has, scope


NARRATIVE = {
    'land_survey': ('The Interministerial Settlement Committee', 'The cabinet must reconcile agricultural development, military plans and the claims of Palestinian landowners. A survey of the West Bank or Gaza will define the area in which the government commits its settlement budget.'),
    'settlement_budget': ('Land, Security and the Development Budget', 'The settlement departments compete with development towns and immigrant housing for engineers, credit and public services. Choose a negotiated freeze, a limited group of agricultural sites or a larger civilian settlement network.'),
    'freeze_new': ('Offer a Settlement Freeze', 'A halt to new settlement construction would leave more room for civilian administration and negotiations with Palestinian representatives. The cabinet must secure acceptance before it can rely on a local administrative arrangement.'),
    'municipal_works': ('Municipal Works Across the Green Line', 'Roads, workshops and civilian services can support the existing population without opening another settlement frontier. This programme ties Israeli investment to the negotiated freeze and requires continuing public expenditure.'),
    'land_compact': ('Negotiate a Civil Administration Compact', 'Palestinian representatives must decide whether to cooperate with a funded municipal administration. A practical agreement can reduce the burden on Israeli ministries and garrisons, while leaving the political dispute unresolved.'),
    'designated_sites': ('Nahal Agricultural Sites', 'Nahal combines agricultural training with military service. A limited group of sites can improve irrigation practice and frontier supply, but even a geographically restrained programme requires land administration and strains relations with Palestinian institutions.'),
    'settlement_services': ('Mekorot and Regional Service Roads', 'Water connections, repair crews and reliable road access turn isolated sites into workable communities. The logistical gain is real, while the extension of the settlement footprint increases local opposition.'),
    'settlement_ceiling': ('Consolidate a Limited Settlement Perimeter', 'Protect the existing sites and their workshops while ruling out another wave of expansion. A smaller perimeter is easier to maintain, although guarding civilian communities still adds to the security budget.'),
    'authorize_expansion': ('A Civilian Settlement Programme', 'The cabinet can place the settlement departments behind a broader civilian programme. Preparing development land and access routes will accelerate construction, while increasing administrative commitments and the dispute over the territory.'),
    'settlement_package': ('Cooperative Farms and Settlement Workshops', 'Cooperative farms, packing facilities and workshops will connect the new communities to Israeli production networks. Agricultural and manufacturing gains come with subsidised housing, public services and a larger capital commitment.'),
    'entrench_network': ('Regional Roads and Protected Supply Routes', 'A connected road network and prepared defensive positions make the settlement programme easier to supply and repair. The same network extends the area that the government must administer and protect.'),
    'settlement_compensation': ('Negotiate a Settlement Ceiling and Compensation', 'Offer a funded ceiling on further construction and compensation for affected claims. Palestinian representatives retain their choice over the proposal; accepting a limit reduces the burden of confrontation but closes the next expansion programme.'),
    'settlement_unilateral': ('Maintain the Unilateral Settlement Programme', 'The government can keep building without an agreed territorial settlement. Further agricultural and workshop projects remain possible, at the price of a wider garrison commitment, persistent local opposition and continuing public subsidies.'),
    'gi_sinai_admin': ('A Sinai Development Authority', 'A permanent development authority can coordinate the roads and services required by the Sinai programme. Distance and the unresolved Egyptian territorial claim make the administrative commitment expensive.'),
    'gi_sinai_housing': ('Housing on the Sinai Frontier', 'Settlement housing requires access roads and serviced land before families can move. The construction programme commits resources that could otherwise serve development towns within Israel.'),
    'gi_sinai_economy': ('Sinai Farms and Civilian Workshops', 'Agricultural sites and repair workshops offer a civilian economic base for the Sinai programme. Their viability depends on reliable supply links and continued Israeli control.'),
    'gi_frontier_families': ('Family Services for Frontier Communities', 'Clinics and family services can make remote communities more viable. A five-year commitment supports household growth while increasing the healthcare budget.'),
    'gi_canal_repair': ('Sinai Coastal Supply Stations', 'Repair the coastal road and its supply stations so civilian and military traffic can reach remote communities. Protecting those links adds another duty for the regional garrison.'),
    'gi_canal_industry': ('Sinai Coastal Workshops', 'Civilian workshops and a small dockyard can maintain vehicles, vessels and coastal installations closer to where they operate. The programme requires a substantial capital budget and dependable control of the coast.'),
    'gi_canal_navigation': ('Sinai Coastal Logistics', 'Coastal handling facilities and maintenance crews can improve local supply without depending on traffic through the Suez Canal. Running the service adds to the civil administration budget.'),
}


def build(api):
    for key, (label, text) in NARRATIVE.items():
        node = api.nodes[focus_id(key)]
        node.update(label=label, description=text, note=text)
        # Numeric project outcomes are appended from the actual project record.
        if any(p['unlock']==key for p in api.projects):
            node['policy_summary'] = []

    # Existing compiled project names follow their newly authored focus names.
    for project in api.projects:
        if project['unlock'] in NARRATIVE:
            label = api.nodes[focus_id(project['unlock'])]['label']
            api.localisation[ident('project_'+project['key'])] = label+': Fund the Project'
            idea = api.data['idea_definitions'].get('policy_project_'+project['key']+'_idea')
            if idea:
                idea.update(label=label, treatment=api.nodes[focus_id(project['unlock'])]['description'])

    # Three paid and individually bounded extensions, available only after the
    # explicitly unilateral choice. An accepted/funded ceiling prevents them.
    stages = []
    for state, province in ((208, 7107), (209, 13207)):
        previous = 'entrench_network_'+str(state)
        for phase in range(1, 4):
            key = f'settlement_extension_{phase}_{state}'
            gate = '\n'.join((has('target_'+str(state)),
                f'{state} = {{ is_owned_by = PAL }}', has('settlement_unilateral'),
                'NOT = { '+has('binding_settlement_ceiling')+' }',
                has('project_'+previous+'_done')))
            local = api.state_modifier(key+'_supply', f'Settlement Supply Network {phase}',
                'Additional local supply capacity from a funded civilian settlement extension.',
                {'local_supplies_for_controller': .05, 'required_garrison_factor': .05},
                enable=f'is_controlled_by = ISR is_owned_by = PAL ISR = {{ ISR70_is_scenario = yes {has("target_"+str(state))} }}')
            rid = 207000+state*10+phase
            tip = ident(key+'_resistance_tt')
            api.loc(tip, 'Local resistance target: +4 percentage points.')
            after = scope(state, f'add_dynamic_modifier = {{ modifier = {local} }}\n'
                f'remove_resistance_target = {rid}\nadd_resistance_target = {{ id = {rid} amount = 4 occupied = PAL occupier = ISR tooltip = {tip} }}')
            unlock = api.project(key, state,
                [{'type':'agriculture_district','levels':1}, {'type':'infrastructure','levels':1},
                 {'type':'bunker','levels':1,'province':province}],
                .012+phase*.003, 240+phase*30,
                mods={'agricolture_productivity_modifier':.04, 'industrial_capacity_factory':.01,
                      'social_cost_multiplier_modifier':.02, 'police_cost_multiplier_modifier':.02},
                after=after, available=gate, political_cost=25, unlock='settlement_unilateral')
            project = api.projects[-1]
            label = ('West Bank' if state==208 else 'Gaza')+f': Settlement Extension {phase}'
            api.localisation[ident('project_'+key)] = label
            api.effects[ident('complete_settlement_unilateral')] += '\nunlock_decision_tooltip = '+ident('project_'+key)
            stages.append(dict(key=key,state=state,phase=phase,share=project['share'],days=project['days'],
                               preview=project['preview_code']))
            previous = key

    # Show the next programme numerically in the focus without executing any
    # project or hiding terms behind the current policy/control conditions.
    for state in (208,209):
        first = next(s for s in stages if s['state']==state and s['phase']==1)
        api.effects[ident('complete_settlement_unilateral')] += '\n'+first['preview']

    # Strong capital mobilisation has an explicit balance sheet: bond proceeds
    # add precisely the same principal to MD debt and therefore incur its real
    # interest expense. Donations are separate, one-time non-state funding.
    bond = '''set_temp_variable = { treasury_change = gdp_total }
multiply_temp_variable = { treasury_change = 0.08 }
modify_treasury_effect = yes
set_temp_variable = { debt_change = gdp_total }
multiply_temp_variable = { debt_change = 0.08 }
modify_debt_effect = yes'''
    did = api.decision('diaspora_development_bonds', 'Israel Bonds: The Development Subscription',
        'Mobilise a major diaspora development subscription. Treasury and debt both rise by 8% of annual GDP. The new principal bears normal MD interest; the subscription can be issued once.',
        'diaspora_bonds', 'has_variable = gdp_total check_variable = { gdp_total > 0 }', bond, cost=50)
    api.nodes['ISR70_diaspora_bonds']['reward'] += '\nunlock_decision_tooltip = '+did+'\neffect_tooltip = {\n'+bond+'\n}'
    api.nodes['ISR70_diaspora_bonds'].setdefault('additional_reward_summary',[]).append(
        'Unlocks Israel Bonds: Treasury +8% of annual GDP and debt +8% of annual GDP, once. Normal MD debt interest applies.')
    services = api.idea('diaspora_absorption_services', 'United Jewish Appeal Absorption Services',
        'A one-time diaspora fundraising campaign supports immigrant housing and vocational placement. Continuing services remain a public budget commitment.',
        {'social_cost_multiplier_modifier':.03,'education_cost_multiplier_modifier':.02})
    donation = '''set_temp_variable = { treasury_change = gdp_total }
multiply_temp_variable = { treasury_change = 0.04 }
modify_treasury_effect = yes
add_ideas = '''+services
    did = api.decision('uja_absorption_campaign', 'United Jewish Appeal: Absorption Campaign',
        'A special diaspora fundraising campaign contributes 4% of annual GDP once. Expanded absorption services add 3% to social costs and 2% to education costs.',
        'absorption_reform', 'has_completed_focus = ISR70_diaspora_bonds has_variable = gdp_total check_variable = { gdp_total > 0 }', donation, cost=50)
    api.nodes['ISR70_absorption_reform']['reward'] += '\nunlock_decision_tooltip = '+did+'\neffect_tooltip = {\n'+donation+'\n}'
    api.nodes['ISR70_absorption_reform'].setdefault('additional_reward_summary',[]).append(
        'Unlocks the United Jewish Appeal campaign: Treasury +4% of annual GDP once; social costs +3%, education costs +2%. Requires the diaspora financing programme.')
    api.data['settlement_revision'] = {'project':'IMPERIA COLD WAR','revision':6,'states':[208,209],
        'max_extensions_per_selected_state':3,'extensions':stages,
        'national_finance':{'bond_gdp_share':.08,'matching_debt_share':.08,'donation_gdp_share':.04},
        'historical_numbers':False,'source_record':'docs/israel_1970_design/REWORK_20261027.md'}

    # Pure policy entry/offer focuses still need an accurate readable inspector.
    summaries = {
        'land_survey':['Treasury cost: 0.1% of annual GDP. Select the West Bank or Gaza as the project area.'],
        'settlement_budget':['Choose one programme: negotiated freeze, limited agricultural sites or civilian settlement expansion.'],
        'freeze_new':['Political Power: -75. Palestinian acceptance: local resistance target -5 points in the selected project area; Palestinian opinion of Israel +15.'],
        'land_compact':['Palestinian acceptance unlocks the funded compact: Treasury -0.3% of annual GDP, transferred to Palestine; bureaucracy cost -5%, local garrison requirement -20%, resistance target -5 points.'],
        'settlement_compensation':['Political Power: -75. If accepted and funded: Treasury -0.6% of annual GDP; local garrison requirement +5%, resistance target +3 points. Further settlement extensions are barred.'],
    }
    for key, lines in summaries.items():
        api.nodes[focus_id(key)]['policy_summary'] = lines
    api.nodes[focus_id('settlement_unilateral')]['policy_summary']=[
        'Political Power: -50. Local garrison requirement +15%, damage to garrisons +10%, resistance target +10 points. Unlocks up to three additional paid settlement phases in the selected area.']
    for key in list(api.localisation):
        if key.endswith('_condition_tt'):
            api.localisation[key]=api.flag_label(key.removesuffix('_condition_tt'))

    add_offer_displays(api)
    api.decision('renew_ceasefire_talks','Renew Ceasefire Negotiations',
        'Open another cabinet proposal after an inconclusive or rejected diplomatic round. Egypt decides whether to accept the resulting terms.',
        'rogers','EGY = { exists = yes } NOT = { has_country_flag = ISR70_ceasefire_accepted }',
        'country_event = { id = ISR70.10 days = 1 }',cost=35,repeatable=True,cooldown=90)
    for key,did in (('land_compact','implement_land_compact'),('settlement_compensation','fund_settlement_compensation')):
        api.effects[ident('complete_'+key)]+='\nunlock_decision_tooltip = '+ident('decision_'+did)
    # The funded compact's national saving follows the same selected territory
    # as its state modifier. Restore the idea alone, never its original transfer.
    compact_gate='OR = { '+ ' '.join('AND = { '+has('target_'+str(s))+f' {s} = {{ is_owned_by = PAL is_controlled_by = ISR }} }}' for s in (208,209))+' }'
    api.tick.append('if = { limit = { '+has('implement_land_compact_done')+' '+compact_gate+' } if = { limit = { NOT = { has_idea = ISR70_policy_land_compact } } add_ideas = ISR70_policy_land_compact } } else = { remove_ideas = ISR70_policy_land_compact }')


def add_offer_displays(api):
    """Display only: no treasury provider, national idea, state modifier,
    resistance or receipt effect is invoked by these preview snippets.

    Uses native MD variable-delta formatters and the same Treasury text as
    00_budget_effects. effect_tooltip itself follows main MD ENG's alternative
    Omani terms (05_united_kingdom.txt around 20914). Only temporary display
    arithmetic and isolated dummy-variable tooltip rows occur here.
    """
    api.loc('ISR70_policy_selected_area_tt','Selected project area')
    api.loc('ISR70_policy_preview_israel_tt','Israel')
    api.loc('ISR70_policy_preview_palestine_tt','Palestine')
    api.loc('ISR70_policy_preview_resistance_tt','Resistance Target: $RIGHT|-=%0$')
    api.loc('ISR70_policy_preview_pal_opinion_tt','Palestinian Opinion of Israel: $RIGHT|+0$')
    def row(name,value,tooltip):
        return f'add_to_variable = {{ ISR70_display_{name} = {value} tooltip = {tooltip} }}'
    def cash(share):
        # Crucially, this never calls modify_treasury_effect or changes treasury.
        return f'set_temp_variable = {{ treasury_change = ISR.gdp_total }}\nmultiply_temp_variable = {{ treasury_change = {share} }}\ncustom_effect_tooltip = modify_treasury_effect_tt'
    def display(key,number,code):
        preview='custom_effect_tooltip = TT_IF_THEY_ACCEPT\neffect_tooltip = {\n'+code+'\n}'
        api.effects[ident('complete_'+key)]+='\n'+preview
        for i,event in enumerate(api.events):
            if f'id = ISR70P.{number}\n' in event:
                api.events[i]=event.replace(f'name = ISR70P.{number}.a',f'name = ISR70P.{number}.a\n'+preview,1)
    israel='custom_effect_tooltip = ISR70_policy_preview_israel_tt\n'
    palestine='custom_effect_tooltip = ISR70_policy_preview_palestine_tt\n'
    area='custom_effect_tooltip = ISR70_policy_selected_area_tt\n'
    display('freeze_new',401,israel+area+row('freeze_resistance',-.05,'ISR70_policy_preview_resistance_tt')+'\n'+palestine+row('freeze_opinion',15,'ISR70_policy_preview_pal_opinion_tt'))
    display('land_compact',402,israel+cash(-.003)+'\ncustom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_policy_land_compact }\n'+row('compact_bureaucracy',-.05,'bureaucracy_cost_multiplier_modifier_tt')+'\n'+area+row('compact_garrison',-.20,'required_garrison_factor_tt')+'\n'+row('compact_resistance',-.05,'ISR70_policy_preview_resistance_tt')+'\n'+palestine+'PAL = { '+cash(.003)+' }')
    display('settlement_compensation',403,israel+cash(-.006)+'\n'+area+row('compensation_garrison',.05,'required_garrison_factor_tt')+'\n'+row('compensation_resistance',.03,'ISR70_policy_preview_resistance_tt'))
    api.nodes[focus_id('settlement_compensation')]['description']='Offer an Israeli-funded property compensation programme and a binding ceiling on further settlement construction. Palestinian representatives decide whether the local terms are acceptable. The Israeli treasury funds the domestic compensation programme after acceptance.'
    api.nodes[focus_id('settlement_compensation')]['note']=api.nodes[focus_id('settlement_compensation')]['description']
