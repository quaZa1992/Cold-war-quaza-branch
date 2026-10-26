# IMPERIA CW — Cold War: israel 1970 — player rewards.
"""Plain English reward descriptions, with the same units as MD modifiers."""
import re

LABELS={
 'offices_worker_requirement_modifier':'Office Worker Requirement','offices_productivity':'Office Productivity',
 'police_cost_multiplier_modifier':'Police Cost','personnel_cost_multiplier_modifier':'Personnel Cost',
 'local_supplies_for_controller':'Local Supplies for Controller','required_garrison_factor':'Local Garrison Requirement',
 'state_production_speed_infrastructure_factor':'Local Infrastructure Construction Speed',
 'political_power_factor':'Political Power Gain','stability_factor':'Stability','war_support_factor':'War Support',
 'bureaucracy_cost_multiplier_modifier':'Bureaucracy Cost','social_cost_multiplier_modifier':'Social Spending Cost',
 'health_cost_multiplier_modifier':'Healthcare Cost','education_cost_multiplier_modifier':'Education Cost',
 'corruption_cost_factor':'Corruption Cost','research_speed_factor':'Research Speed',
 'production_factory_max_efficiency_factor':'Production Efficiency Cap','industrial_capacity_factory':'Factory Output',
 'production_speed_buildings_factor':'Construction Speed','production_speed_offices_factor':'Office Construction Speed',
 'production_speed_industrial_complex_factor':'Civilian Industry Construction Speed','production_speed_arms_factory_factor':'Military Factory Construction Speed',
 'production_speed_infrastructure_factor':'Infrastructure Construction Speed','production_speed_agriculture_district_factor':'Agricultural District Construction Speed',
 'industry_repair_factor':'Industry Repair Speed','productivity_growth_modifier':'Monthly Productivity Growth',
 'receiving_investment_cost_modifier':'Incoming Investment Cost','return_on_investment_modifier':'Return on Investment',
 'interest_rate_multiplier_modifier':'Interest Rate','imp_sanction_resistance':'Imperia Sanction Resistance',
 'imp_investment_reward':'Imperia Investment Reward','mdcw_cw_market_exposure':'World-Market Exposure',
 'mdcw_cw_support_effectiveness':'Cold War Assistance Effectiveness','foreign_influence_defense_modifier':'Foreign Influence Defense',
 'mobilization_speed':'Mobilization Speed','training_time_army_factor':'Army Training Time',
 'recruitable_population_factor':'Recruitable Population Factor','army_org_factor':'Division Organization',
 'army_defence_factor':'Division Defense','planning_speed':'Planning Speed','max_dig_in':'Maximum Entrenchment',
 'army_armor_defence_factor':'Armor Division Defense','recon_factor':'Reconnaissance','supply_consumption_factor':'Supply Consumption',
 'air_mission_efficiency':'Air Mission Efficiency','resistance_damage_to_garrison':'Damage to Garrisons',
}
BUILDINGS={'industrial_complex':'Civilian Factory','arms_factory':'Military Factory','offices':'Office District','agriculture_district':'Agricultural District','infrastructure':'Infrastructure','fossil_powerplant':'Fossil Fuel Powerplant','air_base':'Air Base','dockyard':'Naval Dockyard','civilian_shelter':'Civilian Shelter'}
STATES={204:'Tel Aviv',205:'Haifa',206:'the Negev',207:'Jerusalem'}
CATEGORIES={'industry':'Industry','agriculture':'Agriculture','construction':'Construction','infrastructure':'Infrastructure','energy_efficiency':'Energy Efficiency','electronics':'Electronics','armor':'Armor','infantry_weapons':'Infantry Weapons','towed_artillery':'Towed Artillery','special_forces_equipment':'Special Forces Equipment','medium_aircraft':'Medium Aircraft','aircraft':'Aircraft','anti_air':'Anti-Air','military_electronics':'Military Electronics','corvettes':'Corvettes','submarines':'Submarines','decryption':'Decryption','encryption':'Encryption','fuel_refining':'Fuel Refining','nuclear_reactors':'Nuclear Reactors'}
GROUPS={'labour_unions':'Labor Unions','small_medium_business_owners':'Small and Medium Business Owners','industrial_conglomerates':'Industrial Conglomerates','farmers':'Farmers','the_priesthood':'Religious Institutions','the_military':'The Military','intelligence_community':'Intelligence Community'}

def modifier_line(key,value):
    assert key in LABELS,('Missing player-facing modifier label',key)
    if key in ('productivity_growth_modifier','max_dig_in'):unit='';amount=value
    elif key=='interest_rate_multiplier_modifier':unit=' percentage points';amount=value
    else:unit='%';amount=value*100
    return LABELS[key]+': '+f'{amount:+g}'+unit

def summarize(node,data):
    if node.get('policy_extension'):return node['policy_summary']
    lines=[];code=node['reward']
    for effect,label,scale,unit in [('add_political_power','Political Power',1,''),('add_stability','Stability',100,'%'),('add_war_support','War Support',100,'%'),('army_experience','Army Experience',1,''),('air_experience','Air Experience',1,''),('navy_experience','Navy Experience',1,'')]:
        for amount in re.findall(r'\b'+effect+r'\s*=\s*(-?[\d.]+)',code):lines.append(label+': '+f'{float(amount)*scale:+g}'+unit)
    for slot,value in re.findall(r'party_index = (\d+) \}\nset_temp_variable = \{ party_popularity_increase = ([\d.]+)',code):
        lines.append('Strengthens this party through the MD popularity system by '+f'{float(value)*100:g}'+' percentage points before relative rebalancing.')
    for ideology,value in re.findall(r'add_popularity = \{ ideology = (\w+) popularity = ([\d.]+)',code):
        names={'democratic':'Western','communism':'Emerging','neutrality':'Non-Aligned','nationalist':'Nationalist'}
        lines.append(names[ideology]+' Outlook Popularity: '+f'{float(value)*100:+g}'+' percentage points; MD recalculates party shares.')
    for state,kind,level in re.findall(r'(\d+) = \{\s*(?:add_extra_state_shared_building_slots = \d+\s*)?add_building_construction = \{ type = (\w+) level = (\d+)',code):
        lines.append(f'+{level} '+BUILDINGS[kind]+(' level' if kind in ('infrastructure','air_base','civilian_shelter') else '')+('s' if int(level)>1 else '')+' in '+STATES[int(state)]+'.')
    for category,uses,bonus in re.findall(r'add_tech_bonus = \{ name = \w+ category = CAT_(\w+) uses = (\d+) bonus = ([\d.]+)',code):
        lines.append(f'{uses} x {float(bonus)*100:g}% research bonus: '+CATEGORIES[category]+'.')
    for amount,group in re.findall(r'set_temp_variable = \{ temp_opinion = (-?[\d.]+) \}\nchange_(\w+)_opinion = yes',code):
        lines.append(GROUPS[group]+' Opinion: '+f'{float(amount):+g}'+'.')
    for share in re.findall(r'treasury_change = gdp_total \}\nmultiply_temp_variable = \{ treasury_change = -([\d.]+)',code):
        lines.append('Treasury cost on completion: '+f'{float(share)*100:g}'+'% of annual GDP.')
    if 'decrease_corruption = yes' in code:lines.append('Reduces existing MD corruption by one level, down to its minimum.')
    if 'elections_allowed = yes' in code:lines.append('Enables ordinary elections.')
    if 'elections_allowed = no' in code:lines.append('Disables ordinary elections.')
    for key in re.findall(r'(?m)^remove_ideas = ISR70_(\w+)',code):
        spirit=data['idea_definitions'].get(key)
        if spirit:lines.append('Removes the national spirit "'+spirit['label']+'".')
    if 'swap_ideas = { remove_idea = ISR70_absorption' in code:lines.append('Replaces "Immigration and Development Gaps" with "Integrated Immigration"; removes its +5% social-cost surcharge while retaining population growth.')
    if 'mdcw_cw_add_tension = yes' in code:lines.append('Imperia Cold War Tension: +2 points.')
    if node['modifiers']:
        lines.append(('While this party governs:' if node['group'].startswith('party_') else 'National spirit:'))
        lines.extend(modifier_line(k,v) for k,v in node['modifiers'].items())
    unlocked=[d['label'] for d in data['decisions'] if d['unlock']==node['id']]
    if unlocked:lines.append('Unlocks decisions: '+', '.join(unlocked)+'.')
    return lines
