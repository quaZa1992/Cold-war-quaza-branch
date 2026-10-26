# IMPERIA CW — Cold War: israel 1970 — revised rewards.
"""Authored rewards, including legacy gates removed by direct_access.py.

Reference conventions: MD generic construction/research/interest groups,
Russia's visible variable tooltip increments, Israel's domestic institutions.
No proportional splitting of a generic modifier package between policy nodes.
"""
from pathlib import Path
import copy
import re

ART={}
SPECS={}
def cw(file):return 'gfx/interface/goals/coldwar/'+file
def isr(file):return 'gfx/interface/goals/israel_palestine/'+file+'.dds'
def pp(value):return f'add_political_power = {value}'
def stab(value):return f'add_stability = {value}'
def xp(kind,value):return f'{kind}_experience = {value}'
def opinion(group,value=10):return f'set_temp_variable = {{ temp_opinion = {value} }}\nchange_{group}_opinion = yes'
def tech(category,bonus=.5,uses=1):return f'add_tech_bonus = {{ name = ISR70_research_programme category = CAT_{category} uses = {uses} bonus = {bonus} }}'
def money(share):return f'set_temp_variable = {{ treasury_change = gdp_total }}\nmultiply_temp_variable = {{ treasury_change = {-share:g} }}\nmodify_treasury_effect = yes'
def build(state,kind,share=.01,level=1):
    shared=kind in ('industrial_complex','arms_factory','offices','agriculture_district','dockyard')
    return f'{state} = {{\n'+(f'\tadd_extra_state_shared_building_slots = {level}\n' if shared else '')+f'\tadd_building_construction = {{ type = {kind} level = {level} instant_build = yes }}\n}}\n'+money(share)
def popularity(slot,value=.03):return f'set_temp_variable = {{ party_index = {slot} }}\nset_temp_variable = {{ party_popularity_increase = {value} }}\nset_temp_variable = {{ temp_outlook_increase = {value} }}\nchange_relative_party_popularity = yes'
def elections(allowed,outlook):
    # HOI4 1.19's visible set_politics tooltip dereferences the ideology group.
    # Election-only blocks leave that group null and crash on hover. Each caller
    # names its existing party outlook; the focus requires that party in office.
    assert outlook in ('democratic','communism','neutrality','nationalist')
    return 'set_politics = { ruling_party = '+outlook+' elections_allowed = '+('yes' if allowed else 'no')+' }'
def S(key,art,body,code='',mods=None,**kwargs):
    assert key not in SPECS,key
    SPECS[key]={'art':art,'body':body,'code':code,'mods':mods or {},**kwargs}

# State institutions: practical administrative benefits, with visible MD effects.
S('january_1970',isr('ISR_independence'),'Set the cabinet agenda for the new decade and release political capital for the first reforms.',pp(100))
S('knesset',isr('knesset_speech'),'Secure the parliamentary mandate needed to organize parties, form cabinets and negotiate a constitution.',pp(100)+'\n'+stab(.02))
S('unity_cabinet',cw('generic_union_agreement.png'),'Replace the fragile starting coalition with a negotiated unity agreement. Its broader support improves stability and military confidence.',opinion('the_military',5)+'\nremove_ideas = ISR70_unity',{'stability_factor':.05,'political_power_factor':.05})
S('narrow_cabinet',cw('generic_parliament.png'),'A smaller working majority leaves the cabinet more political room and gives organized labor a clearer role.',pp(75)+'\n'+opinion('labour_unions',10)+'\nremove_ideas = ISR70_unity',{'political_power_factor':.10})
S('civil_service',cw('civil_service.png'),'Professional recruitment and common procurement rules reduce the recurring cost of the civil service.',pp(50),{'bureaucracy_cost_multiplier_modifier':-.10})
S('oversight',cw('generic_investigate_corruption.png'),'Give the State Comptroller enforceable audit powers and reduce corruption by one existing MD level.','decrease_corruption = yes',{'corruption_cost_factor':-.05})
S('local_councils',cw('generic_public_transport.png'),'Let local councils deliver roads and services faster without increasing the central bureaucracy.',opinion('small_medium_business_owners',5),{'production_speed_infrastructure_factor':.15,'bureaucracy_cost_multiplier_modifier':-.05})
S('central_planning',cw('construction_engineering.png'),'Coordinate national tenders and engineering standards for a faster state construction programme.',tech('construction',.5),{'production_speed_buildings_factor':.05})
S('basic_laws',cw('Adopt_New_Constitiution.tga'),'Strengthen the Basic Law framework and open the constitutional convention decision.',pp(100)+'\n'+stab(.03))

# Economic development uses actual MD buildings and staffed, owned states.
S('economic_plan',cw('Economic_Protectionism.dds'),'Approve a national industrial programme and fund two industrial research projects.',pp(50)+'\n'+tech('industry',.5,2))
S('water',cw('Create_water_Commission.tga'),'Improve the National Water Carrier and irrigation engineering. Agricultural research supports the next stage.',tech('agriculture',.5),{'production_speed_agriculture_district_factor':.15})
S('negev_agriculture',cw('Agricultural_Mechanization.dds'),'Build a new irrigated agricultural district in the Negev rather than granting an abstract growth bonus.',build(206,'agriculture_district',.008)+'\n'+opinion('farmers',10))
S('water_maintenance',cw('Focus_on_Water_and_Agricultural_Projects.dds'),'Fund pumps, workshops and repairs so farms and public utilities recover more quickly.',opinion('farmers',10),{'industry_repair_factor':.15})
S('haifa_industry',cw('CostalIndustry.dds'),'Expand the civilian industrial base in Haifa and give the new plant a funded capital budget.',build(205,'industrial_complex',.015)+'\n'+tech('industry',.5))
S('tel_aviv_offices',cw('generic_financial_markets.png'),'Add a commercial office district in Tel Aviv for services, export finance and municipal employment.',build(204,'offices',.012)+'\n'+opinion('small_medium_business_owners',10))
S('negev_roads',cw('generic_road_construction.png'),'Connect southern development towns with an additional infrastructure level in the Negev.',build(206,'infrastructure',.006)+'\n'+tech('infrastructure',.5))
S('power_grid',cw('1st_Electric_Program.dds'),'Expand fossil electricity generation to serve the growing industrial and office sectors.',build(204,'fossil_powerplant',.012)+'\n'+tech('energy_efficiency',.5))
S('exports',isr('diamond_gent'),'Support diamond cutting, precision tools and export finance. Local businesses gain confidence and offices expand faster.',opinion('small_medium_business_owners',10),{'production_speed_offices_factor':.10,'receiving_investment_cost_modifier':-.10})
S('import_substitution',cw('Economic_Protectionism.dds'),'Build industrial resilience against embargoes. Domestic factory output and Imperia sanction resistance improve.',opinion('industrial_conglomerates',5),{'imp_sanction_resistance':.15,'industrial_capacity_factory':.05})
S('export_specialization',cw('export_factories.tga'),'Specialize in higher-value exports and foreign investment. Greater world-market exposure makes external market swings more consequential.',opinion('small_medium_business_owners',10),{'return_on_investment_modifier':.005,'receiving_investment_cost_modifier':-.10,'mdcw_cw_market_exposure':.10})
S('diaspora_bonds',cw('agricultural_banks.dds'),'Create an administered diaspora investment programme. Its lasting reward is more effective Imperia investment, not free money.',pp(75),{'imp_investment_reward':.10})
S('investment_scrutiny',cw('generic_civilian_oversight.png'),'Publish investment contracts and audit concessions. Existing MD corruption falls by one level.','decrease_corruption = yes',{'corruption_cost_factor':-.05})
S('civil_electronics',isr('isr_computer'),'Develop civilian electronics and technical workshops, with two electronics research bonuses and stronger productivity growth.',tech('electronics',.5,2),{'productivity_growth_modifier':.10})
S('technion',cw('Universities.dds'),'Fund applied research at the Technion. Construction research and a permanent national research improvement support civilian and defense engineering.',tech('construction',.5,2),{'research_speed_factor':.03})
S('sme_credit',cw('generic_banking_legislation.png'),'Guarantee productive small-business credit and reduce the cost of incoming investment.',opinion('small_medium_business_owners',15),{'receiving_investment_cost_modifier':-.10,'production_speed_offices_factor':.05})
S('civil_plant',cw('factory_complex.png'),'Establish a civilian industrial complex in the Negev and develop its production methods.',build(206,'industrial_complex',.015)+'\n'+tech('industry',.5))
S('fiscal_review',cw('generic_banking_legislation.png'),'Prepare a fiscal review and give the cabinet political capital for its budget choice.',pp(100)+'\n'+opinion('small_medium_business_owners',5))
S('steady_budget',cw('generic_tackle_corruption.png'),'Improve sovereign credit through a credible consolidation programme. Interest rates fall without forcing new cuts into unrelated policies.',pp(50),{'interest_rate_multiplier_modifier':-.50,'bureaucracy_cost_multiplier_modifier':-.05})
S('development_budget',cw('construction.png'),'Commit a funded development budget to construction and industrial research.',money(.008)+'\n'+tech('construction',.5),{'production_speed_buildings_factor':.10})

# Social choices have different outcomes rather than interchangeable stability.
S('social_contract',cw('generic_union_agreement.png'),'Agree a social compact between workers, employers and municipalities.',pp(75)+'\n'+opinion('labour_unions',5)+'\n'+opinion('small_medium_business_owners',5))
S('vocational',cw('BEL_prioritizetechnicaleducation.dds'),'Expand vocational schools for new immigrants and industrial workers. Training improves productivity and industrial research.',tech('industry',.5)+'\n'+opinion('labour_unions',10),{'productivity_growth_modifier':.10})
S('development_towns',cw('focus_public_housing.dds'),'Connect development towns to employment and public services with funded infrastructure in the Negev.',build(206,'infrastructure',.006),{'production_speed_infrastructure_factor':.10})
S('absorption_reform',cw('Fund_social_integration_Programs.tga'),'Replace the starting immigration bottleneck with integrated housing, employment and education. Population growth remains while the starting social-cost surcharge is removed.','swap_ideas = { remove_idea = ISR70_absorption add_idea = ISR70_integrated_immigration }\n'+stab(.03))
S('arab_citizens',isr('one_state_isr_pal'),'Include Arab citizens in the national development compact and strengthen confidence in common public institutions.',stab(.04)+'\n'+pp(50))
S('equal_local_services',cw('Generic_Healthcare.tga'),'Fund equal municipal provision. Better administration lowers the cost of social services and improves public confidence.',money(.005)+'\n'+stab(.03),{'social_cost_multiplier_modifier':-.10})
S('local_autonomy',isr('westbank_civic_organizations'),'Transfer routine municipal responsibilities to elected councils and reduce central administrative costs.',pp(75),{'bureaucracy_cost_multiplier_modifier':-.10})
S('religion_state',isr('menorah'),'Open negotiations over personal status, religious education and public service before choosing a settlement.',pp(75)+'\n'+opinion('the_priesthood',5))
S('religious_compromise',isr('Orthodox_jew'),'Renew the parliamentary religious compromise. Religious institutions gain confidence and a more stable settlement supports government.',opinion('the_priesthood',15),{'stability_factor':.05})
S('civil_marriage',cw('generic_female_rights.png'),'Introduce civilian personal-status options and strengthen secular civic institutions. This political reform grants a distinct gain in political capacity.',pp(100)+'\n'+stab(.03),{'political_power_factor':.05})
S('national_service',cw('conscription.png'),'Prepare a common public-service framework and strengthen the institutions that organize it.',pp(75)+'\n'+xp('army',15))
S('volunteer_service',cw('generic_workers_rights.png'),'Organize voluntary municipal civilian service. Social administration becomes cheaper and the civic settlement gains confidence.',stab(.03),{'social_cost_multiplier_modifier':-.05,'bureaucracy_cost_multiplier_modifier':-.05})
S('service_expansion',cw('generic_army_training.png'),'Expand training facilities and improve military call-up speed, with immediate army experience.',xp('army',35),{'mobilization_speed':.15,'training_time_army_factor':-.05})
S('universities',cw('expand_research_funding.tga'),'Increase university capacity in Jerusalem and Haifa, financing research staff and two electronics projects.',money(.008)+'\n'+tech('electronics',.5,2),{'research_speed_factor':.03})
S('public_health',cw('Generic_Healthcare.tga'),'Extend clinics and professional healthcare administration beyond the largest cities.',money(.006)+'\n'+stab(.02),{'health_cost_multiplier_modifier':-.10})

# Conventional 1970 defense: research support and experience, no future equipment.
S('staff',isr('goal_ISR_israeli_corps'),'Review the General Staff organization and turn the experience of the previous war into usable planning capacity.',xp('army',40)+'\n'+opinion('the_military',10))
S('reserve_system',cw('AST_upgrade_reserves.png'),'Replace the starting citizen-army spirit with an organized reserve system. Mobilization and unit cohesion improve.',xp('army',25)+'\nremove_ideas = ISR70_citizen_army',{'mobilization_speed':.25,'army_org_factor':.05})
S('defensive_depth',cw('generic_army_training.png'),'Train layered defenses and improve defensive coordination.',xp('army',30),{'army_defence_factor':.08,'max_dig_in':2})
S('maneuver',cw('doctrine_tank_warfare.png'),'Build mobile operational reserves around staff exercises and rapid planning.',xp('army',40),{'planning_speed':.15,'army_org_factor':.05})
S('armour_programme',cw('CHI_Domestic_Tanks.dds'),'Fund Tal\'s domestic tank-development programme with two armor research bonuses. It does not grant a finished future tank.',tech('armor',.5,2)+'\n'+xp('army',25))
S('survivability',cw('generic_tank_destroyer.png'),'Prioritize crew protection, repairability and standardized maintenance in the armored force.',tech('armor',.5),{'army_armor_defence_factor':.10})
S('armour_mobility',cw('generic_army_tanks2.png'),'Prioritize tactical mobility and armored coordination rather than the alternative protection package.',xp('army',35),{'army_org_factor':.05,'planning_speed':.10})
S('imi',cw('generic_artillery_factories.png'),'Add an IMI military factory in Tel Aviv and support contemporary infantry-weapons development.',build(204,'arms_factory',.015)+'\n'+tech('infantry_weapons',.5))
S('artillery',cw('artillery.png'),'Improve artillery and counter-battery practice with two research bonuses and operational experience.',tech('towed_artillery',.5,2)+'\n'+xp('army',20))
S('engineers',isr('ISR_mil_log'),'Improve field engineering, reconnaissance and combat supply rather than simply expanding the force.',xp('army',25),{'recon_factor':.10,'supply_consumption_factor':-.08})
S('special_forces',isr('isr_army3'),'Fund specialist training and contemporary special-forces equipment research.',tech('special_forces_equipment',.5,2)+'\n'+xp('army',30))
S('air_staff',isr('goal_ISR_israeli_air_force'),'Reorganize the air staff around sortie generation, training and the lessons of the arms embargo.',xp('air',40)+'\n'+opinion('the_military',5))
S('foreign_aircraft',cw('generic_air_fighter_new.png'),'Exploit an accepted American supply agreement through two medium-aircraft research bonuses and conversion training.',tech('medium_aircraft',.5,2)+'\n'+xp('air',25))
S('local_aircraft',cw('Generic_Airline_Industry.tga'),'Fund IAI development and two domestic aircraft research projects. Completing the maintenance programme can overcome the embargo bottleneck.',tech('aircraft',.5,2)+'\n'+xp('air',20)+'\nset_country_flag = ISR70_local_aircraft_programme')
S('air_maintenance',isr('isr_prof_flight'),'Improve training, spare parts and maintenance. A completed domestic aircraft programme removes the starting embargo penalty.',money(.006)+'\nif = { limit = { has_country_flag = ISR70_local_aircraft_programme } remove_ideas = ISR70_embargo }',{'air_mission_efficiency':.08})
S('airfield',cw('generic_air_command.png'),'Expand the southern airfield network by two levels and improve its engineering.',build(206,'air_base',.008,2)+'\n'+tech('construction',.5))
S('air_defense',cw('generic_radar_instillation.png'),'Improve contemporary ground-based air defense and military electronics.',tech('anti_air',.5)+'\n'+tech('military_electronics',.5)+'\n'+xp('air',15))
S('naval_staff',isr('goal_ISR_israeli_navy'),'Reorganize coastal operations and naval staff training.',xp('navy',40)+'\n'+opinion('the_military',5))
S('missile_boats',isr('isr_navy'),'Develop missile-boat tactics and contemporary corvette research.',tech('corvettes',.5,2)+'\n'+xp('navy',30))
S('submarines',cw('generic_submarine_base.png'),'Train covert naval reconnaissance and support submarine development.',tech('submarines',.5,2)+'\n'+xp('navy',30))
S('shipyards',cw('Drydock_Construction.tga'),'Build a funded naval dockyard in Haifa and improve shipbuilding practice.',build(205,'dockyard',.015)+'\n'+xp('navy',20))
S('intelligence',isr('isr_mossad'),'Strengthen Mossad and military intelligence. The intelligence community gains support and decryption research is funded.',opinion('intelligence_community',15)+'\n'+tech('decryption',.5))
S('intelligence_analysis',isr('the_research_department'),'Prioritize assessment, language training and independent analysis over operational expansion.',tech('decryption',.5),{'recon_factor':.10,'planning_speed':.10})
S('intelligence_operations',isr('isr_mossad_door'),'Build operational networks and secure communications. Foreign influence becomes harder to exert.',tech('encryption',.5)+'\n'+opinion('intelligence_community',10),{'foreign_influence_defense_modifier':.15})
S('civil_defense',cw('generic_construct_public_housing.png'),'Build two civilian shelter levels for northern border communities.',build(205,'civilian_shelter',.006,2)+'\n'+stab(.02))
S('preparedness',isr('ISR_more_def'),'Integrate the reserve, maintenance and civil-defense programmes into one readiness plan.',xp('army',30)+'\n'+xp('air',20)+'\n'+xp('navy',15),{'army_org_factor':.03,'supply_consumption_factor':-.05})

# Diplomacy: earned agreements and explicitly described proposals, never empty flags.
S('foreign_policy',cw('foreign_diplomacy.png'),'Give the foreign ministry a cabinet mandate and open the national diplomatic programme.',pp(100))
S('us_channel',cw('ArmIsrael.dds'),'Organize the Washington channel and unlock the American military or civilian cooperation proposal.',pp(50)+'\nset_country_flag = ISR70_us_talks')
S('us_security',isr('isr_usa_soldiers'),'Implement an accepted military supply agreement through training and more effective Imperia assistance.',xp('army',25)+'\n'+xp('air',25),{'mdcw_cw_support_effectiveness':.10})
S('us_civil',cw('generic_positive_trade_relations_gold.png'),'Implement an accepted civilian agreement through investment access and industrial research.',tech('industry',.5),{'receiving_investment_cost_modifier':-.15})
S('france_channel',cw('BeginNegotiations.dds'),'Ask Paris to reopen a commercial channel. The French government must accept before European cooperation can deepen.',pp(50)+'\nset_country_flag = ISR70_france_talks')
S('european_trade',cw('europe_trade.tga'),'Use the accepted European trade channel to improve investment returns and support commercial institutions.',opinion('small_medium_business_owners',10),{'return_on_investment_modifier':.005,'production_speed_offices_factor':.10})
S('soviet_channel',cw('BeginNegotiations.dds'),'Open a cautious channel to Moscow and unlock a proposal on emigration and diplomatic contacts.',pp(50)+'\nset_country_flag = ISR70_soviet_talks')
S('soviet_dialogue',cw('Generic_Refugee_Focus.tga'),'Implement an accepted emigration framework. A six-month absorption wave follows through the existing event and daily systems.',stab(.03)+'\n'+pp(50))
S('independent_diplomacy',isr('ISR_middle_east'),'Maintain independent negotiating room and protect domestic decision making against foreign influence.',pp(75),{'foreign_influence_defense_modifier':.10})
S('africa_contacts',cw('african_diplomacy.dds'),'Fund technical missions and cooperation abroad, increasing the effectiveness of Imperia assistance programmes.',money(.004)+'\n'+tech('agriculture',.5),{'mdcw_cw_support_effectiveness':.10})
S('jordan_backchannel',isr('israel_jordan_flags'),'Send a confidential border proposal to Amman. Jordan decides whether the channel becomes an agreement.',pp(50)+'\nset_country_flag = ISR70_jordan_talks')
S('iran_contacts',cw('Oil_Deal.dds'),'Propose supply cooperation with the Shah\'s Iran. The oil-security focus requires Iranian acceptance.',pp(50)+'\nset_country_flag = ISR70_iran_talks')
S('oil_security',cw('Oil_Pipelines.tga'),'Implement the accepted Iranian supply agreement, improving resilience against sanctions and fuel vulnerability.',tech('fuel_refining',.5),{'imp_sanction_resistance':.10})
S('nuclear_policy',cw('generic_secret_documents.png'),'Review the diplomatic implications of ambiguity and international transparency before choosing a policy.',pp(75))
S('keep_ambiguity',isr('isr_secrets'),'Replace the starting ambiguity spirit with a clearer policy of diplomatic independence. It grants no nuclear equipment.','remove_ideas = ISR70_ambiguity\n'+pp(50),{'foreign_influence_defense_modifier':.15})
S('nuclear_transparency',cw('focus_generic_democratic_science.dds'),'Exchange the starting ambiguity policy for civilian nuclear cooperation and stronger research. No nuclear weapon or completed technology is granted.','remove_ideas = ISR70_ambiguity\n'+tech('nuclear_reactors',.5,2),{'research_speed_factor':.02})

# War of Attrition and territorial choices preserve negotiated ownership checks.
S('suez',cw('generic_army_training.png'),'Assess the Suez front and give the cabinet a concrete military and political assessment.',xp('army',25)+'\n'+pp(75))
S('limited_attrition',cw('generic_civilian_oversight.png'),'Limit the conflict to a defensive posture with better field coordination and manageable supply use.',xp('army',20),{'army_defence_factor':.05,'supply_consumption_factor':-.05})
S('deep_raids',isr('isr_airforce'),'Commit resources to deep raids. Air and army experience rise, while Imperia Cold War tension increases by two points.',xp('air',35)+'\n'+xp('army',20)+'\n'+money(.006)+'\nset_temp_variable = { mdcw_cw_tension_delta = 2 }\ncustom_effect_tooltip = ISR70_cold_war_tension_tt\nhidden_effect = { mdcw_cw_add_tension = yes }')
S('rogers',cw('BeginNegotiations.dds'),'Choose a response to the Rogers Initiative. An Egyptian reply determines whether a ceasefire can be implemented.',pp(50)+'\nset_country_flag = ISR70_rogers_offer')
S('ceasefire',isr('olive_branch'),'Consolidate an accepted ceasefire, remove the starting War of Attrition costs and restore public confidence.','remove_ideas = ISR70_attrition\n'+stab(.05)+'\n'+pp(50))
S('armed_stalemate',isr('ISR_more_def'),'Maintain a fortified military posture instead of the negotiated ceasefire route. The War of Attrition burden remains.',xp('army',30),{'army_defence_factor':.08})
S('territorial_policy',isr('ISR_middle_east'),'Prepare the cabinet\'s territorial policy. The next choice determines which negotiated or administrative route can proceed.',pp(100))
S('all_on',cw('generic_road_construction.png'),'Adopt an Allon-oriented security plan. Defensive planning improves while negotiations remain possible.',xp('army',20)+'\nset_country_flag = ISR70_allon_policy',{'army_defence_factor':.05})
S('territorial_maximalism',isr('Jewish_sites_isr'),'Commit the cabinet to permanent territorial control and the administrative branch. This grants political support, not cores or automatic ownership.',pp(75)+'\nset_country_flag = ISR70_territorial_policy',{'war_support_factor':.05})
S('regional_compromise',isr('olive_branch'),'Authorize territorial compromise and give the negotiating team political capital for the peace route.',pp(100)+'\nset_country_flag = ISR70_peace_policy',{'foreign_influence_defense_modifier':.05})
S('sinai_negotiation',cw('BeginNegotiations.dds'),'Prepare Sinai security guarantees and unlock the Egyptian peace proposal. Egypt must agree before implementation.',pp(75)+'\nset_country_flag = ISR70_sinai_talks')
S('westbank_autonomy',isr('westbank_civic_organizations'),'Prepare a municipal autonomy proposal and unlock Palestinian negotiations. Local representatives retain the right to reject the offer.',pp(75)+'\nset_country_flag = ISR70_westbank_talks')
S('golan_review',isr('israel_jordan_flags'),'Send Syria a proposal for a Golan security framework. Talks do not transfer ownership or grant cores.',pp(50)+'\nset_country_flag = ISR70_golan_talks')
S('gaza_services',isr('gaza_civic_organizations'),'Improve civilian administration and local supplies in Gaza while Israel controls it. Legal ownership remains unchanged.',money(.004)+'\nset_country_flag = ISR70_gaza_services',{'bureaucracy_cost_multiplier_modifier':-.05})
S('egypt_peace',isr('go_to_camp_david'),'Implement an accepted Egyptian peace agreement, end the War of Attrition and improve the climate for civilian investment. Sinai control returns only under the agreed ownership checks.','remove_ideas = ISR70_attrition\n'+stab(.05)+'\n'+pp(100),{'receiving_investment_cost_modifier':-.10})
S('regional_normalization',isr('heveinu_shalom_aleichem'),'Build commercial and diplomatic institutions on the peace framework. Investment returns and office construction improve.',opinion('small_medium_business_owners',10),{'return_on_investment_modifier':.005,'production_speed_offices_factor':.10})
S('territory_administration',cw('civil_service.png'),'Fund a permanent administrative apparatus. It reduces garrison losses but has an explicit recurring bureaucratic cost.',money(.008),{'resistance_damage_to_garrison':-.15,'bureaucracy_cost_multiplier_modifier':.05})
S('annexation_review',isr('knesset_speech'),'Submit sovereignty claims to a parliamentary event with administrative, municipal and claim options. No option grants automatic cores.',pp(75)+'\nset_country_flag = ISR70_annexation_review')

# The historical Alignment and Gahal extensions keep their existing positions.
S('alignment_balance',isr('labour_party_israel'),'Negotiate a workable Labor-Mapam balance and improve union confidence inside the Alignment.',pp(75)+'\n'+opinion('labour_unions',10),{'political_power_factor':.05})
S('golda_labour',cw('Empower_Workers_UnionsUK.tga'),'Modernize Histadrut enterprises through negotiated workplace standards and worker training.',opinion('labour_unions',15),{'production_factory_max_efficiency_factor':.05,'productivity_growth_modifier':.10})
S('golda_manager',cw('generic_improve_industry.png'),'Give professional managers clearer production targets and invest in modern industrial methods.',tech('industry',.5)+'\n'+opinion('industrial_conglomerates',10),{'industrial_capacity_factory':.05})
S('golda_panthers',cw('Fund_social_integration_Programs.tga'),'Hear the development-town protest movement and choose a practical response in a municipal petition event.',pp(50)+'\n'+stab(.03))
S('golda_housing',cw('focus_public_housing.dds'),'Fund development-town housing and local infrastructure, reducing the cost of future social provision.',build(206,'infrastructure',.006),{'social_cost_multiplier_modifier':-.05})
S('golda_succession',isr('knesset_speech'),'Choose whether Golda Meir, Yitzhak Rabin or Shimon Peres leads the Alignment. The choice opens the corresponding cabinet focus.',pp(75))
S('rabin_cabinet',cw('generic_civilian_oversight.png'),'A Rabin cabinet emphasizes professional administration and readiness, with a one-level anti-corruption reform.','decrease_corruption = yes\n'+xp('army',25),{'bureaucracy_cost_multiplier_modifier':-.05})
S('peres_cabinet',cw('generic_artillery_factories.png'),'A Peres cabinet emphasizes industrial modernization and domestic defense engineering.',tech('armor',.5)+'\n'+tech('aircraft',.5),{'production_speed_arms_factory_factor':.10})
S('gahal_identity',isr('isr_liberals'),'Settle the working relationship between Herut and the Liberal Party before choosing a broad alliance or a united party.',pp(100)+'\n'+popularity(1,.03))
S('gahal_coalition',cw('generic_union_agreement.png'),'Keep Gahal as a broad alliance with room for its constituent parties.',pp(75),{'political_power_factor':.05})
S('likud_foundation',isr('Likud'),'Form a united Likud list as an explicit political foundation, increase its support and update its displayed identity.','set_country_flag = ISR70_likud_founded\n'+popularity(1,.05)+'\nupdate_party_name = yes\nupdate_dirty_politicsview_expanded = yes')

def P(slot,art,body,inst_code,inst_mods,finish_code,finish_mods):
    S(f'p{slot}_mandate',art,'Turn this party\'s electoral mandate into a working cabinet and strengthen its political base.',pp(75)+'\n'+popularity(slot,.03))
    S(f'p{slot}_institution',art,body,inst_code,inst_mods)
    S(f'p{slot}_finish',art,'Consolidate the institutions and the economic and civic choices made in this programme.',finish_code,finish_mods)
def Q(slot,choice,art,body,mods,code,deep_art,deep_body,deep_mods,deep_code):
    S(f'p{slot}_{choice}',art,body,code,mods)
    S(f'p{slot}_{choice}_deepen',deep_art,deep_body,deep_code,deep_mods)

# Party institutions and finales have distinct political and economic identities.
P(0,isr('menorah'),'Anchor religious Zionism in parliamentary institutions and strengthen its public-service organizations.',opinion('the_priesthood',10),{'political_power_factor':.05},pp(75)+'\n'+stab(.03),{'mobilization_speed':.05})
P(1,isr('isr_liberals'),'Coordinate Herut and Liberal representatives around a durable parliamentary leadership.',pp(75)+'\n'+opinion('small_medium_business_owners',5),{'political_power_factor':.05},xp('army',25)+'\n'+pp(75),{'industrial_capacity_factory':.03})
P(2,cw('generic_parliament2.png'),'Strengthen independent liberal institutions and build business confidence without merging into a larger bloc.',pp(75)+'\n'+opinion('small_medium_business_owners',10),{},tech('electronics',.5)+'\n'+stab(.03),{'research_speed_factor':.02})
P(3,isr('isr_labour'),'Reconcile Labor and Mapam around a cabinet programme rooted in the Histadrut and cooperative institutions.',opinion('labour_unions',15),{'political_power_factor':.05},pp(100)+'\n'+stab(.03),{'industrial_capacity_factory':.03})
P(4,cw('generic_workers_democracy.png'),'Organize a Jewish-Arab class alliance through workers\' organizations and public institutions.',opinion('labour_unions',15)+'\n'+stab(.02),{},tech('industry',.5)+'\n'+pp(75),{'social_cost_multiplier_modifier':-.05})
P(5,cw('generic_workers_democracy.png'),'Give municipal and producers\' councils a defined role in a federative political system.',pp(75)+'\n'+opinion('labour_unions',10),{'bureaucracy_cost_multiplier_modifier':-.05},stab(.04)+'\n'+pp(75),{'productivity_growth_modifier':.05})
P(6,isr('menorah'),'Build an independent political voice for traditional families and the development towns.',stab(.03)+'\n'+opinion('the_priesthood',10),{},pp(75)+'\n'+opinion('small_medium_business_owners',10),{'social_cost_multiplier_modifier':-.05})
P(7,cw('civil_service.png'),'Give the directorate a professional administrative core before choosing its economic and constitutional direction.',pp(75),{'bureaucracy_cost_multiplier_modifier':-.05},tech('construction',.5)+'\n'+pp(75),{'production_speed_buildings_factor':.05})
P(12,isr('arablist_party'),'Represent municipal interests through parliamentary negotiation and accountable local institutions.',stab(.03)+'\n'+pp(75),{},opinion('small_medium_business_owners',10)+'\n'+pp(75),{'bureaucracy_cost_multiplier_modifier':-.05})
P(13,isr('Orthodox_jew'),'Organize an Orthodox parliamentary bloc that negotiates education, community services and religious practice.',opinion('the_priesthood',15)+'\n'+pp(50),{},stab(.04)+'\n'+pp(75),{'social_cost_multiplier_modifier':-.05})
P(14,isr('knesset_speech'),'Build a pragmatic state leadership around professional administration and workable parliamentary support.',pp(100),{'bureaucracy_cost_multiplier_modifier':-.05},xp('army',20)+'\n'+pp(75),{'political_power_factor':.05})
P(15,cw('collaborate_local_elites.png'),'Create a development alliance between municipal notables and productive investment interests.',opinion('small_medium_business_owners',10)+'\n'+pp(50),{'production_speed_offices_factor':.05},tech('industry',.5)+'\n'+pp(75),{'imp_investment_reward':.05})
P(16,cw('generic_female_rights.png'),'Defend a free press and open political organization as the foundation of a secular civil-rights programme.',pp(100)+'\n'+stab(.02),{},tech('electronics',.5)+'\n'+pp(75),{'political_power_factor':.05})
P(17,cw('generic_agriculture.png'),'Create professional institutions for landscape protection, water policy and development planning.',tech('agriculture',.5)+'\n'+pp(50),{},tech('energy_efficiency',.5)+'\n'+stab(.03),{'research_speed_factor':.02})
P(18,cw('Democratic_Socialism.tga'),'Establish Mapam\'s independent political institutions after its separation from the Alignment.',opinion('labour_unions',15)+'\n'+pp(50),{},stab(.04)+'\n'+pp(75),{'social_cost_multiplier_modifier':-.05})
P(19,cw('generic_workers_rights.png'),'Build independent communist institutions around workers\' representation and Jewish-Arab cooperation.',opinion('labour_unions',10)+'\n'+pp(75),{},tech('industry',.5)+'\n'+stab(.03),{'productivity_growth_modifier':.05})
P(20,isr('ISR_independence'),'Build a national opposition with enough institutional depth to govern through its chosen constitutional route.',pp(100)+'\n'+xp('army',15),{},pp(75)+'\n'+stab(.03),{'war_support_factor':.05})
P(21,cw('generic_paramilitary.png'),'Organize a radical national alliance. Its later constitutional choice determines whether it accepts legal limits or an authoritarian order.',xp('army',30)+'\n'+pp(50),{},xp('army',30)+'\n'+pp(75),{'mobilization_speed':.10})
P(22,isr('goal_ISR_israeli_corps'),'Organize an emergency cabinet around defined military responsibilities and a genuine constitutional crisis.',xp('army',35),{'political_power_factor':.05},xp('army',25)+'\n'+pp(75),{'supply_consumption_factor':-.05})
P(23,isr('menorah'),'Create a constituent assembly for the explicitly chosen crown settlement. Its powers remain subject to the later constitutional choice.',pp(100)+'\n'+stab(.02),{},pp(100)+'\n'+stab(.03),{'political_power_factor':.05})

# Each policy implementation differs from its preceding choice: construction,
# research, interest-group support, institutional reform or a further modifier.
Q(0,'ea',cw('BEL_prioritizetechnicaleducation.dds'),'Connect religious study to vocational education and industrial qualifications.',{'research_speed_factor':.02},tech('industry',.5),
  cw('School_is_in.tga'),'Train technical teachers and improve the productivity of religious vocational graduates.',{'productivity_growth_modifier':.05,'education_cost_multiplier_modifier':-.05},opinion('the_priesthood',10))
Q(0,'eb',isr('Orthodox_jew'),'Expand municipal religious welfare institutions and community provision.',{'social_cost_multiplier_modifier':-.05},opinion('the_priesthood',10),
  cw('focus_public_housing.dds'),'Fund a development-town service network and infrastructure in the Negev.',{},build(206,'infrastructure',.006)+'\n'+stab(.02))
Q(0,'ca',cw('conscription.png'),'Link Bnei Akiva and national service to military preparation.',{'mobilization_speed':.10},xp('army',25),
  cw('generic_army_training.png'),'Professionalize the service framework and reduce the time needed for army training.',{'training_time_army_factor':-.05,'recruitable_population_factor':.03},xp('army',20))
Q(0,'cb',isr('Jewish_sites_isr'),'Support religious settlement policy through defensive organization rather than automatic territorial cores.',{'army_defence_factor':.05},pp(75),
  isr('ISR_more_def'),'Coordinate the defense and supply of border communities.',{'army_org_factor':.03,'supply_consumption_factor':-.05},xp('army',25))

Q(1,'ea',cw('generic_privatization.png'),'Make private enterprise and commercial employment the engine of development.',{'receiving_investment_cost_modifier':-.10},opinion('small_medium_business_owners',10),
  cw('generic_financial_markets.png'),'Build a funded commercial office district in Tel Aviv.',{},build(204,'offices',.012)+'\n'+tech('industry',.5))
Q(1,'eb',cw('generic_takeover_industries.png'),'Retain strategic public enterprises while improving their industrial methods.',{'industrial_capacity_factory':.05},tech('industry',.5),
  cw('factory_complex.png'),'Expand Haifa\'s civilian industrial base under strategic state ownership.',{},build(205,'industrial_complex',.015)+'\n'+opinion('labour_unions',5))
Q(1,'ca',cw('generic_civilian_oversight.png'),'Defend the rule of law and subject the government to effective scrutiny.',{},'decrease_corruption = yes\n'+pp(75),
  cw('generic_parliament2.png'),'Entrench parliamentary safeguards and a more efficient civilian administration.',{'bureaucracy_cost_multiplier_modifier':-.05,'stability_factor':.03},pp(50))
Q(1,'cb',isr('ISR_more_def'),'Make security interests the center of the government\'s civic mandate.',{'war_support_factor':.05},xp('army',30),
  isr('ISR_mil_log'),'Fund a more cohesive force with better operational supply.',{'army_org_factor':.05,'supply_consumption_factor':-.05},xp('army',20))

Q(2,'ea',cw('generic_banking_legislation.png'),'Prioritize small businesses over protected monopolies.',{'receiving_investment_cost_modifier':-.10},opinion('small_medium_business_owners',15),
  cw('generic_financial_markets.png'),'Build a Tel Aviv office district serving small firms and local commerce.',{},build(204,'offices',.012))
Q(2,'eb',cw('export_factories.tga'),'Support capital formation and manufacturers that compete in export markets.',{'return_on_investment_modifier':.005},tech('industry',.5),
  cw('factory_complex.png'),'Build a civilian factory in Haifa and modernize production methods.',{'production_factory_max_efficiency_factor':.05},build(205,'industrial_complex',.015))
Q(2,'ca',cw('generic_female_rights.png'),'Entrench civil rights through accountable parliamentary institutions.',{'political_power_factor':.05},stab(.03)+'\n'+pp(50),
  cw('generic_civilian_oversight.png'),'Enforce those rights through audits and a lower-cost civil service.',{'bureaucracy_cost_multiplier_modifier':-.05},'decrease_corruption = yes')
Q(2,'cb',cw('generic_army_training.png'),'A liberal security policy emphasizes professional planning and trained reserves.',{'planning_speed':.10},xp('army',30),
  isr('the_research_department'),'Invest in defensive analysis and secure communications.',{'foreign_influence_defense_modifier':.10},tech('encryption',.5))

Q(3,'ea',cw('generic_union_agreement.png'),'Modernize Histadrut enterprises through negotiated production and workplace reform.',{'production_factory_max_efficiency_factor':.05},opinion('labour_unions',15),
  cw('factory_complex.png'),'Add a modern civilian industrial complex in Haifa as the programme\'s concrete investment.',{'productivity_growth_modifier':.05},build(205,'industrial_complex',.015))
Q(3,'eb',cw('Agricultural_Modernization.dds'),'Use kibbutzim as agricultural development and technical-training centers.',{'production_speed_agriculture_district_factor':.15},tech('agriculture',.5)+'\n'+opinion('farmers',10),
  cw('Agricultural_Mechanization.dds'),'Create an irrigated agricultural district in the Negev and improve rural productivity.',{'productivity_growth_modifier':.05},build(206,'agriculture_district',.008))
Q(3,'ca',cw('focus_public_housing.dds'),'Make urban social balance and development-town provision a cabinet priority.',{'social_cost_multiplier_modifier':-.05},stab(.03),
  cw('Generic_Healthcare.tga'),'Fund local services and development-town infrastructure.',{'health_cost_multiplier_modifier':-.05},build(206,'infrastructure',.006))
Q(3,'cb',isr('ISR_more_def'),'Use organized military readiness as the basis for negotiations from strength.',{'army_org_factor':.05},xp('army',30),
  isr('olive_branch'),'Strengthen diplomatic independence and give the cabinet political room to negotiate.',{'foreign_influence_defense_modifier':.10},pp(100))

Q(4,'ea',cw('Democratic_Socialism.tga'),'Commit parliamentary communism to organized labor and accountable public production.',{'production_factory_max_efficiency_factor':.05},opinion('labour_unions',15),
  cw('generic_workers_rights.png'),'Train workers and strengthen the productivity of parliamentary public enterprises.',{'productivity_growth_modifier':.10},tech('industry',.5))
Q(4,'eb',cw('Centrally_Planned_Economy.tga'),'Coordinate industrial construction through a central economic plan.',{'production_speed_industrial_complex_factor':.10},tech('construction',.5),
  cw('factory_complex.png'),'Build a funded public industrial complex in Haifa.',{'industrial_capacity_factory':.03},build(205,'industrial_complex',.015))
Q(4,'ca',isr('one_state_isr_pal'),'Make equal citizenship the legal basis of the Jewish-Arab class alliance.',{'stability_factor':.04},pp(75),
  cw('Generic_Healthcare.tga'),'Improve equal access to municipal social provision.',{'social_cost_multiplier_modifier':-.10},stab(.02))
Q(4,'cb',cw('generic_army_cooperation.png'),'Pursue Soviet-oriented security cooperation through contemporary training and assistance capacity.',{'mdcw_cw_support_effectiveness':.10},xp('army',25),
  cw('FocusImportSovietTanks.dds'),'Prepare the armored force for contemporary foreign designs without granting a free tank model.',{},tech('armor',.5,2)+'\n'+xp('army',20))

Q(5,'ea',cw('generic_workers_democracy.png'),'Give producers\' councils practical control of workplace training and production.',{'production_factory_max_efficiency_factor':.05},opinion('labour_unions',15),
  cw('generic_market_socialism.png'),'Spread council-led technical training and industrial research.',{'productivity_growth_modifier':.10},tech('industry',.5))
Q(5,'eb',cw('Agricultural_Modernization.dds'),'Coordinate the cooperative federation\'s agricultural and industrial investment.',{'production_speed_buildings_factor':.05},tech('agriculture',.5),
  cw('Agricultural_Mechanization.dds'),'Fund a cooperative agricultural district in the Negev.',{},build(206,'agriculture_district',.008)+'\n'+opinion('farmers',10))
Q(5,'ca',isr('one_state_isr_pal'),'Define Jewish-Arab federalism through accountable municipal powers.',{'bureaucracy_cost_multiplier_modifier':-.10},pp(75),
  cw('generic_parliament2.png'),'Protect local representation and the stability of the federal settlement.',{'stability_factor':.04},pp(75))
Q(5,'cb',cw('generic_female_rights.png'),'Build a common civic republic through equal public institutions.',{'political_power_factor':.05},stab(.03),
  cw('Generic_Healthcare.tga'),'Deliver common civic services rather than merely proclaiming them.',{'social_cost_multiplier_modifier':-.10},money(.005)+'\n'+stab(.02))

Q(6,'ea',cw('generic_banking_legislation.png'),'Give craftspeople and family businesses access to productive credit.',{'receiving_investment_cost_modifier':-.10},opinion('small_medium_business_owners',15),
  cw('generic_financial_markets.png'),'Create a municipal commercial office district in the Negev.',{},build(206,'offices',.012))
Q(6,'eb',cw('focus_public_housing.dds'),'Direct development funds toward municipal services in the periphery.',{'social_cost_multiplier_modifier':-.05},stab(.03),
  cw('generic_road_construction.png'),'Fund an additional infrastructure level for southern development towns.',{'production_speed_infrastructure_factor':.10},build(206,'infrastructure',.006))
Q(6,'ca',isr('Orthodox_jew'),'Combine traditional institutions with shared vocational education.',{'research_speed_factor':.02},opinion('the_priesthood',10),
  cw('BEL_prioritizetechnicaleducation.dds'),'Train teachers and skilled workers for the development towns.',{'productivity_growth_modifier':.10},tech('industry',.5))
Q(6,'cb',cw('generic_union_agreement.png'),'Negotiate a traditional social partnership between employers, workers and religious institutions.',{'stability_factor':.04},opinion('labour_unions',10),
  cw('Generic_Healthcare.tga'),'Use that partnership to improve community welfare administration.',{'social_cost_multiplier_modifier':-.10},opinion('the_priesthood',5))

Q(7,'ea',cw('civil_service.png'),'Build a technocratic development plan around transparent procurement and engineering.',{'bureaucracy_cost_multiplier_modifier':-.10},tech('construction',.5),
  cw('factory_complex.png'),'Deliver a funded public industrial complex in Haifa.',{'industrial_capacity_factory':.03},build(205,'industrial_complex',.015))
Q(7,'eb',cw('generic_takeover_industries.png'),'Use state corporations and favored contractors for rapid construction. Patronage increases corruption-related costs.',{'production_speed_industrial_complex_factor':.15,'corruption_cost_factor':.05},opinion('industrial_conglomerates',10),
  cw('industrial_subsidies.tga'),'Deliver the state-corporation industrial programme and reward its sponsors.',{},build(206,'industrial_complex',.015)+'\n'+opinion('industrial_conglomerates',10))
Q(7,'ca',cw('generic_parliament.png'),'Restore elections and commit the directorate to parliamentary government.',{'stability_factor':.04},elections(True,'communism')+'\n'+pp(75),
  cw('generic_civilian_oversight.png'),'Submit the civilian transition to an effective audit and strengthen public confidence.',{},'decrease_corruption = yes\n'+stab(.03))
Q(7,'cb',cw('generic_stable_government.png'),'Establish permanent presidential rule and suspend ordinary elections.',{'political_power_factor':.10},elections(False,'communism')+'\n'+pp(75),
  cw('civil_service.png'),'Centralize presidential administration and construction planning.',{'bureaucracy_cost_multiplier_modifier':-.05,'production_speed_buildings_factor':.05},pp(75))

Q(12,'ea',cw('generic_financial_markets.png'),'Build Arab commercial centers around local enterprise and parliamentary representation.',{'receiving_investment_cost_modifier':-.10},opinion('small_medium_business_owners',10),
  cw('collaborate_local_elites.png'),'Fund an office district serving northern municipal commerce.',{},build(205,'offices',.012))
Q(12,'eb',cw('Generic_Healthcare.tga'),'Use social endowments for municipal welfare and charitable provision.',{'social_cost_multiplier_modifier':-.10},stab(.02),
  cw('focus_public_housing.dds'),'Improve the roads and public-service links used by municipal institutions.',{},build(205,'infrastructure',.006)+'\n'+stab(.02))
Q(12,'ca',isr('one_state_isr_pal'),'Integrate the municipal reform movement into common civic institutions.',{'political_power_factor':.05},pp(75)+'\n'+stab(.02),
  cw('generic_civilian_oversight.png'),'Make common civic institutions accountable through a public audit.',{'bureaucracy_cost_multiplier_modifier':-.05},'decrease_corruption = yes')
Q(12,'cb',isr('gaza_civic_organizations'),'Give municipal institutions greater administrative autonomy.',{'bureaucracy_cost_multiplier_modifier':-.10},pp(75),
  cw('generic_public_transport.png'),'Improve autonomous municipal services and community confidence.',{'social_cost_multiplier_modifier':-.05},stab(.04))

Q(13,'ea',isr('Orthodox_jew'),'Connect religious study and vocational qualifications without treating Orthodox representation as a dictatorship.',{'research_speed_factor':.02},opinion('the_priesthood',10),
  cw('BEL_prioritizetechnicaleducation.dds'),'Fund technical training alongside religious study.',{'productivity_growth_modifier':.05},tech('industry',.5))
Q(13,'eb',cw('Generic_Working_Class_Family.tga'),'Expand community social provision and local welfare institutions.',{'social_cost_multiplier_modifier':-.10},opinion('the_priesthood',10),
  cw('Generic_Healthcare.tga'),'Professionalize community healthcare and charitable administration.',{'health_cost_multiplier_modifier':-.05},stab(.03))
Q(13,'ca',isr('menorah'),'Renew the religious status quo through parliamentary negotiation.',{'stability_factor':.05},opinion('the_priesthood',15),
  cw('generic_parliament.png'),'Give the compromise a durable parliamentary settlement.',{'political_power_factor':.05},pp(75))
Q(13,'cb',cw('generic_workers_rights.png'),'Develop voluntary civilian service that respects the movement\'s religious institutions.',{'bureaucracy_cost_multiplier_modifier':-.05},stab(.03),
  cw('focus_public_housing.dds'),'Fund service links for development-town communities.',{'social_cost_multiplier_modifier':-.05},build(206,'infrastructure',.006))

Q(14,'ea',cw('civil_service.png'),'Professionalize state enterprises through clear procurement and production rules.',{'production_factory_max_efficiency_factor':.05},opinion('industrial_conglomerates',10),
  cw('factory_complex.png'),'Expand the civilian industrial base in Haifa under professional management.',{},build(205,'industrial_complex',.015))
Q(14,'eb',cw('generic_privatization.png'),'Promote private enterprise and competitive investment.',{'receiving_investment_cost_modifier':-.10},opinion('small_medium_business_owners',15),
  cw('generic_financial_markets.png'),'Fund a Tel Aviv office district for private commerce.',{'return_on_investment_modifier':.003},build(204,'offices',.012))
Q(14,'ca',isr('ISR_more_def'),'Pursue pragmatic security through trained forces and defensive planning.',{'army_defence_factor':.05},xp('army',30),
  isr('ISR_mil_log'),'Improve the practical supply burden of that defensive posture.',{'supply_consumption_factor':-.08},xp('army',20))
Q(14,'cb',cw('BeginNegotiations.dds'),'Give territorial negotiators a pragmatic cabinet mandate. This does not impose an agreement on a neighbor.',{'foreign_influence_defense_modifier':.10},pp(100),
  isr('olive_branch'),'Build public confidence around a negotiated territorial policy.',{'stability_factor':.04},pp(75))

Q(15,'ea',cw('generic_banking_legislation.png'),'Channel diaspora capital through supervised and published investment contracts.',{'imp_investment_reward':.10},opinion('small_medium_business_owners',10),
  cw('generic_financial_markets.png'),'Build a supervised commercial office district in Tel Aviv.',{},build(204,'offices',.012)+'\n'+tech('industry',.5))
Q(15,'eb',cw('collaborate_local_elites.png'),'Accelerate investment through privileged concessions. The price is higher corruption-related expenditure.',{'receiving_investment_cost_modifier':-.15,'corruption_cost_factor':.05},opinion('industrial_conglomerates',15),
  cw('industrial_subsidies.tga'),'Fund an industrial concession in Haifa and improve the sponsors\' production methods.',{'industrial_capacity_factory':.03},build(205,'industrial_complex',.015))
Q(15,'ca',cw('generic_investigate_corruption.png'),'Require public oversight of investment contracts and concession income.',{'corruption_cost_factor':-.05},'decrease_corruption = yes',
  cw('generic_civilian_oversight.png'),'Professionalize contract administration and lower recurring bureaucratic costs.',{'bureaucracy_cost_multiplier_modifier':-.10},pp(75))
Q(15,'cb',cw('collaborate_local_elites2.png'),'Build patronage networks that secure political capacity at the expense of clean public spending.',{'political_power_factor':.10,'corruption_cost_factor':.05},pp(75),
  cw('generic_stable_government.png'),'Consolidate the political investment network and its construction programme.',{'production_speed_offices_factor':.10},opinion('industrial_conglomerates',10)+'\n'+pp(50))

Q(16,'ea',cw('generic_workers_rights.png'),'Combine a civil-rights reform economy with investment access and public education.',{'receiving_investment_cost_modifier':-.10},opinion('small_medium_business_owners',10),
  cw('BEL_prioritizetechnicaleducation.dds'),'Improve technical qualifications and research in civilian electronics.',{'productivity_growth_modifier':.05},tech('electronics',.5))
Q(16,'eb',cw('generic_privatization.png'),'Cut routine bureaucracy and let private firms enter services more easily.',{'bureaucracy_cost_multiplier_modifier':-.10},pp(75),
  cw('generic_financial_markets.png'),'Create commercial capacity through a funded Tel Aviv office district.',{'production_speed_offices_factor':.05},build(204,'offices',.012))
Q(16,'ca',cw('generic_female_rights.png'),'Establish secular civic institutions and a free public sphere.',{'political_power_factor':.10},stab(.03),
  cw('generic_civilian_oversight.png'),'Enforce secular accountability through an independent public audit.',{'stability_factor':.03},'decrease_corruption = yes')
Q(16,'cb',cw('generic_parliament2.png'),'Decentralize public decisions to elected municipalities.',{'bureaucracy_cost_multiplier_modifier':-.10},pp(75),
  cw('generic_public_transport.png'),'Fund municipal links and practical local services in the Negev.',{},build(206,'infrastructure',.006)+'\n'+stab(.02))

Q(17,'ea',cw('Create_water_Commission.tga'),'Use water-efficient agriculture as the basis of landscape protection.',{'production_speed_agriculture_district_factor':.15},tech('agriculture',.5),
  cw('Agricultural_Modernization.dds'),'Fund a carefully planned agricultural district in the Negev.',{'productivity_growth_modifier':.05},build(206,'agriculture_district',.008))
Q(17,'eb',cw('generic_electricity.png'),'Invest in cleaner industrial methods and energy-efficiency research.',{'research_speed_factor':.02},tech('energy_efficiency',.5),
  cw('generic_improve_industry.png'),'Improve industrial repair and efficient production rather than simply increasing land use.',{'industry_repair_factor':.15,'production_factory_max_efficiency_factor':.05},tech('industry',.5))
Q(17,'ca',cw('generic_agriculture.png'),'Give municipalities professional conservation and land-use planning.',{'bureaucracy_cost_multiplier_modifier':-.05},pp(75),
  cw('generic_road_construction.png'),'Apply conservation planning to public infrastructure delivery.',{'production_speed_infrastructure_factor':.15},tech('infrastructure',.5))
Q(17,'cb',cw('generic_public_transport.png'),'Combine environmental goals with social and public-transport provision.',{'social_cost_multiplier_modifier':-.05},stab(.03),
  cw('Generic_Healthcare.tga'),'Fund healthier local services and development-town infrastructure.',{'health_cost_multiplier_modifier':-.05},build(206,'infrastructure',.006))

Q(18,'ea',cw('Democratic_Socialism.tga'),'Build a cooperative welfare economy around organized labor.',{'social_cost_multiplier_modifier':-.10},opinion('labour_unions',15),
  cw('Agricultural_Modernization.dds'),'Fund a cooperative agricultural district in the Negev.',{'production_factory_max_efficiency_factor':.05},build(206,'agriculture_district',.008))
Q(18,'eb',cw('focus_public_housing.dds'),'Prioritize municipal development and education over expanding the cooperative production sector.',{'bureaucracy_cost_multiplier_modifier':-.05},pp(75),
  cw('Universities.dds'),'Fund applied education and local infrastructure in the development towns.',{'research_speed_factor':.02},build(206,'infrastructure',.006)+'\n'+tech('construction',.5))
Q(18,'ca',isr('olive_branch'),'Give negotiated peace a clear parliamentary mandate.',{'foreign_influence_defense_modifier':.10},pp(100),
  cw('generic_parliament.png'),'Build confidence in the elected institutions that will scrutinize any peace agreement.',{'stability_factor':.04},pp(75))
Q(18,'cb',isr('one_state_isr_pal'),'Prepare a binational constitutional convention through equal civic institutions. It does not automatically annex another state.',{'political_power_factor':.05},pp(100),
  cw('generic_civilian_oversight.png'),'Put civil rights and municipal accountability into the proposed constitutional settlement.',{'bureaucracy_cost_multiplier_modifier':-.05,'stability_factor':.03},'decrease_corruption = yes')

Q(19,'ea',cw('generic_workers_rights.png'),'Support Jewish-Arab industrial enterprises through common worker training.',{'production_factory_max_efficiency_factor':.05},opinion('labour_unions',15),
  cw('factory_complex.png'),'Build a civilian industrial complex in Haifa under the independent workers\' programme.',{},build(205,'industrial_complex',.015)+'\n'+tech('industry',.5))
Q(19,'eb',cw('generic_market_socialism.png'),'Use democratic economic planning to coordinate public investment.',{'production_speed_buildings_factor':.05},tech('construction',.5),
  cw('BEL_prioritizetechnicaleducation.dds'),'Improve planning skills and the productivity of public enterprises.',{'productivity_growth_modifier':.10},tech('industry',.5))
Q(19,'ca',cw('generic_parliament.png'),'Entrench parliamentary workers\' rights and open elections.',{'political_power_factor':.05},elections(True,'neutrality')+'\n'+stab(.03),
  cw('generic_workers_democracy.png'),'Enforce accountable worker representation and audit the state administration.',{'bureaucracy_cost_multiplier_modifier':-.05},'decrease_corruption = yes')
Q(19,'cb',cw('generic_workers_democracy.png'),'Give workers\' councils constitutionally limited administrative powers.',{'bureaucracy_cost_multiplier_modifier':-.10},pp(75),
  cw('generic_union_agreement.png'),'Negotiate a durable balance between councils and the elected legislature.',{'stability_factor':.04},opinion('labour_unions',10))

Q(20,'ea',cw('generic_banking_legislation.png'),'Use development-town small businesses as a national economic base.',{'receiving_investment_cost_modifier':-.10},opinion('small_medium_business_owners',15),
  cw('generic_financial_markets.png'),'Build a commercial office district in the Negev.',{'production_speed_offices_factor':.05},build(206,'offices',.012))
Q(20,'eb',cw('generic_union_agreement.png'),'Negotiate a national industrial pact with workers and manufacturers.',{'industrial_capacity_factory':.05},opinion('labour_unions',10)+'\n'+opinion('industrial_conglomerates',10),
  cw('factory_complex.png'),'Deliver the pact through an industrial complex in Haifa.',{},build(205,'industrial_complex',.015))
Q(20,'ca',cw('generic_parliament2.png'),'Keep national populism within a parliamentary system with ordinary elections.',{'stability_factor':.04},elections(True,'nationalist')+'\n'+pp(75),
  cw('generic_civilian_oversight.png'),'Professionalize the parliamentary government and its oversight.',{'bureaucracy_cost_multiplier_modifier':-.05},'decrease_corruption = yes')
Q(20,'cb',cw('generic_stable_government.png'),'Seek an elected presidential mandate while preserving elections.',{'political_power_factor':.10},elections(True,'nationalist')+'\n'+pp(100),
  isr('ISR_independence'),'Consolidate the popular mandate and national mobilization institutions.',{'war_support_factor':.05},stab(.03)+'\n'+xp('army',20))

Q(21,'ea',cw('generic_artillery_factories.png'),'Build an autonomous domestic defense industry to reduce external dependence.',{'imp_sanction_resistance':.10},tech('infantry_weapons',.5),
  cw('arty_industry_1.dds'),'Add a military factory in Tel Aviv under a funded domestic-arms programme.',{'industrial_capacity_factory':.05},build(204,'arms_factory',.015))
Q(21,'eb',cw('generic_paramilitary.png'),'Create a mobilization fund for reserve training and military production.',{'mobilization_speed':.15},xp('army',35),
  cw('generic_army_training.png'),'Expand the practical training programme and support arms-factory construction.',{'training_time_army_factor':-.05,'production_speed_arms_factory_factor':.10},money(.008)+'\n'+xp('army',25))
Q(21,'ca',cw('generic_parliament.png'),'Accept legal limits on radical political organization and retain ordinary elections.',{'stability_factor':.04},elections(True,'nationalist')+'\n'+pp(75),
  cw('generic_civilian_oversight.png'),'Give civilian institutions the authority to enforce those limits.',{'bureaucracy_cost_multiplier_modifier':-.05},'decrease_corruption = yes')
Q(21,'cb',cw('generic_police_state.png'),'Establish an authoritarian security order and suspend elections. The constitutional confrontation causes an immediate stability loss.',{'political_power_factor':.10},elections(False,'nationalist')+'\n'+stab(-.03)+'\n'+xp('army',25),
  cw('generic_officer.png'),'Consolidate the security apparatus and its military organization.',{'army_org_factor':.05},opinion('the_military',10)+'\n'+pp(75))

Q(22,'ea',isr('ISR_mil_log'),'Centralize defense logistics to reduce the supply burden of the emergency force.',{'supply_consumption_factor':-.10},xp('army',30),
  cw('generic_artillery_factories.png'),'Create a military factory in Tel Aviv for the emergency procurement programme.',{'production_speed_arms_factory_factor':.10},build(204,'arms_factory',.015))
Q(22,'eb',cw('civil_service.png'),'Bring civilian technocrats into the emergency government and reduce administrative waste.',{'bureaucracy_cost_multiplier_modifier':-.10},pp(75),
  cw('generic_improve_industry.png'),'Apply civilian technical standards to industrial and construction planning.',{'productivity_growth_modifier':.05},tech('industry',.5)+'\n'+tech('construction',.5))
Q(22,'ca',cw('generic_parliament.png'),'Limit the emergency and restore ordinary elections.',{'stability_factor':.05},elections(True,'nationalist')+'\n'+pp(75),
  cw('generic_civilian_oversight.png'),'Audit emergency procurement and strengthen civilian confidence.',{'bureaucracy_cost_multiplier_modifier':-.05},'decrease_corruption = yes\n'+stab(.02))
Q(22,'cb',cw('generic_officer.png'),'Make military rule permanent and suspend ordinary elections.',{'political_power_factor':.10},elections(False,'nationalist')+'\n'+opinion('the_military',10),
  isr('goal_ISR_israeli_corps'),'Consolidate the standing command structure and military mobilization programme.',{'army_org_factor':.05,'mobilization_speed':.10},xp('army',35))

Q(23,'ea',cw('focus_public_housing.dds'),'Use public endowments for local works rather than private royal industrial corporations.',{'production_speed_infrastructure_factor':.15},pp(75),
  cw('generic_road_construction.png'),'Fund a public-works infrastructure level in the Negev.',{'social_cost_multiplier_modifier':-.05},build(206,'infrastructure',.006))
Q(23,'eb',cw('generic_takeover_industries.png'),'Create professionally run royal industrial companies under the new constitutional settlement.',{'production_speed_industrial_complex_factor':.10},tech('industry',.5),
  cw('factory_complex.png'),'Build the royal industrial programme\'s civilian complex in Haifa.',{'industrial_capacity_factory':.03},build(205,'industrial_complex',.015))
Q(23,'ca',cw('generic_parliament2.png'),'Establish a parliamentary crown with ordinary elections and a responsible cabinet.',{'stability_factor':.05},elections(True,'nationalist')+'\n'+pp(75),
  cw('generic_civilian_oversight.png'),'Place crown expenditure and administration under parliamentary scrutiny.',{'bureaucracy_cost_multiplier_modifier':-.05},'decrease_corruption = yes')
Q(23,'cb',cw('generic_stable_government.png'),'Establish personal royal government and suspend ordinary elections.',{'political_power_factor':.10},elections(False,'nationalist')+'\n'+pp(100),
  isr('menorah'),'Consolidate the crown\'s executive institutions and national-service mandate.',{'mobilization_speed':.10},stab(.03)+'\n'+pp(50))

def apply(data,root):
    """Change content and art only; preserve IDs, positions and graph structure."""
    data=copy.deepcopy(data)
    from programme_narrative import enrich
    enrich(SPECS)
    nodes={n['id'].removeprefix('ISR70_'):n for n in data['nodes']}
    for outlook,ideology,art in [('western','democratic','generic_parliament.png'),('emerging','communism','generic_workers_democracy.png'),('nonaligned','neutrality','foreign_diplomacy.png'),('nationalist','nationalist','generic_stable_government.png')]:
        for stage in ('debate','campaign','mandate'):
            key=outlook+'_'+stage
            body={'debate':'Open a national debate on this outlook and release political capital for organizing its parties.',
                  'campaign':'Build a social base for this outlook. The boost applies to outlook popularity; the existing MD system recalculates party shares.',
                  'mandate':'Give the governing party of this outlook political capacity to implement its distinct programme.'}[stage]
            code=pp(75) if stage=='debate' else f'add_popularity = {{ ideology = {ideology} popularity = 0.05 }}\nrecalculate_party = yes' if stage=='campaign' else pp(100)+'\n'+stab(.02)
            S(key,cw(art),body,code)
    assert set(nodes)==set(SPECS),(set(nodes)-set(SPECS),set(SPECS)-set(nodes))
    # Reviewed as contact sheets, not selected by filename alone. Some inherited
    # files contain foreign flags or politicians from the 2000-era Israel tree.
    substitutions={
      cw('CostalIndustry.dds'):cw('generic_improve_industry.png'),
      cw('CHI_Domestic_Tanks.dds'):cw('generic_army_tanks3.png'),
      cw('Create_water_Commission.tga'):cw('Irrigation_Pipes.dds'),
      cw('Focus_on_Water_and_Agricultural_Projects.dds'):cw('Irrigation_Canals.tga'),
      cw('Empower_Workers_UnionsUK.tga'):cw('generic_workers_rights.png'),
      cw('arty_industry_1.dds'):cw('generic_artillery_factories.png'),
      cw('focus_generic_democratic_science.dds'):cw('Nuclear_Research_Lab.png'),
      isr('diamond_gent'):cw('DiamondsAre4ever.dds'),
      isr('ISR_middle_east'):cw('ISR_Israel.dds'),
      isr('ISR_mil_log'):cw('Improve_supply_distribution_methods.tga'),
      isr('ISR_more_def'):cw('ISR_Focus_Israeli_Army.dds'),
      isr('isr_army3'):cw('ISR_israel_defense_forces.dds'),
      isr('goal_ISR_israeli_corps'):cw('ISR_Focus_Israeli_Army.dds'),
      isr('isr_mossad_door'):cw('generic_secret_documents.png'),
      isr('isr_secrets'):cw('Nuclear_Research_Lab.png'),
      isr('isr_prof_flight'):cw('generic_support_equipment.png'),
      isr('isr_usa_soldiers'):cw('ArmIsrael.dds'),
      isr('go_to_camp_david'):isr('olive_branch'),
      isr('heveinu_shalom_aleichem'):isr('olive_branch'),
      isr('isr_airforce'):cw('generic_air_fighter_new.png'),
      isr('arablist_party'):cw('generic_parliament2.png'),
      isr('westbank_civic_organizations'):cw('generic_public_transport.png'),
      isr('isr_labour'):cw('FocusElectMapai.dds'),
      isr('labour_party_israel'):cw('FocusElectMapai.dds'),
      isr('isr_liberals'):cw('FocusElectHerut.dds'),
    }
    # Give the historical political spines their actual Cold War insignia.
    for key in ('p0_mandate','p0_institution','p0_finish'):SPECS[key]['art']=cw('FocusElectHapoelHaMizrachi.dds')
    for key in ('p18_mandate','p18_institution','p18_finish'):SPECS[key]['art']=cw('FocusElectMapam.dds')
    SPECS['golan_review']['art']=cw('BeginNegotiations.dds')
    SPECS['suez']['art']=cw('ISR_Focus_Egypt-Israeli_Tension.dds')
    base={k:copy.deepcopy(v) for k,v in data['idea_definitions'].items() if k in data['starting_spirits'] or k in ('integrated_immigration','temporary_readiness')}
    for key,n in nodes.items():
        spec=SPECS[key]
        source=substitutions.get(spec['art'],spec['art'])
        path=root/source;assert path.is_file(),(key,path)
        slug=re.sub('[^a-z0-9_]+','_',path.stem.lower()).strip('_')
        icon='GFX_ISR70_focus_'+slug
        if icon in ART:assert ART[icon]==source,(icon,ART[icon],source)
        ART[icon]=source
        n.update(icon=icon,reward=spec['code'],modifiers=spec['mods'],duration_days=None,
                 description=spec['body'],note=spec['body'],reward_revision=2,art_source=source)
        n['label'] = spec.get('label', n['label'])
        # Existing party-specific political gates remain. New building scopes get
        # ownership, control, staffing and affordability checks in the compiler.
        n['effect_explanation']=spec['body']
        if not n['group'].startswith('party_') and n['modifiers']:
            base[key+'_idea']={'label':n['label'],'treatment':spec['body'],'modifiers':spec['mods'],'picture':icon.replace('GFX_ISR70_focus_','ISR70_spirit_')}
    data['idea_definitions']=base
    spirit_art={'citizen_army':'reserve_system','histadrut':'golda_labour','unity':'unity_cabinet','attrition':'suez','embargo':'local_aircraft','absorption':'absorption_reform','ambiguity':'keep_ambiguity','integrated_immigration':'absorption_reform','temporary_readiness':'reserve_system'}
    for spirit,focus in spirit_art.items():base[spirit]['picture']=nodes[focus]['icon'].replace('GFX_ISR70_focus_','ISR70_spirit_')
    # Retain empty definitions for superseded spirits so existing saves can load
    # before the one-time revision synchronizer removes those old entries.
    obsolete=[]
    for key,old in data.get('legacy_idea_definitions',{}).items():
        if key not in base:
            obsolete.append(key)
            base[key]={'label':old['label'],'treatment':'This older policy is superseded by the revised 1970 programme.','modifiers':{},'picture':'ISR70_spirit_generic_union_agreement'}
    data['obsolete_spirits']=obsolete
    data['reward_revision']=2
    return data
