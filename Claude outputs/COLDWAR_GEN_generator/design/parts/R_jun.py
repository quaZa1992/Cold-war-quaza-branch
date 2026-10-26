# IMPERIA CW — Cold War: parts — R jun.
from dsl import *

# Reference party (written first, the quality bar for all other parties).
PARTIES = [dict(
    key='jun',
    title='The Officers\' State',
    identity='The army governs as an institution, not as one man: the officer corps decides who rules, how long, '
             'and which economic model pays for the barracks.',
    history='1970s juntas split along the same lines everywhere: caretaker regimes that handed back power (Turkey 1973, '
            'Nigeria 1979, Ghana 1979) against institutional military states (Brazil 1964-85, Chile 1973-90, Argentina 1976-83); '
            'free-market technocrats (Chile\'s Chicago Boys) against military developmentalists (Brazil\'s "miracle", '
            'Velasco\'s Peru); repression (Operation Condor) against civic action (Indonesia, Thailand, Peru).',
    foci={
        'E': F('jun_the_generals_take_charge', 'The Generals Take Charge', [
            prog('political_power_factor', 0.05), prog('stability_factor', 0.03), prog('army_morale_factor', 0.05),
            fac('the_military', 10), fac('defense_industry', 5), law('increase_military_spending'),
        ], 'A junta first secures the barracks with larger budgets and privileges for the officer corps, as in Greece after 1967 or Chile after 1973.', old=True),

        # ---------------- the power question
        'POL': F('jun_communique_number_one', 'Communiqué Number One', [
            pp(100), stab(0.03), outlook('W', -0.03), outlook('E', -0.03),
        ], 'Coups from Greece (1967) to Chile (1973) and Turkey (1980) opened with numbered radio communiqués; parliament was dissolved and the parties suspended or banned soon after.'),
        'A1': F('jun_a_caretaker_junta', 'A Caretaker Junta', [
            prog('stability_factor', 0.05), stab(0.05),
            timed('jun_return_promise', 730, {'foreign_influence_defense_modifier': 0.10, 'trade_opinion_factor': 0.10}, 'A Promised Return'),
            outlook('W', 0.03), outlook('N', 0.03), fac('the_military', -5),
        ], 'Nigeria\'s military government (1975-79) set a timetable for civilian rule and Ghana\'s AFRC (1979) kept the scheduled elections; the promise bought calm and foreign goodwill but let the parties recover.', old=True),
        'A2': F('jun_permanent_military_rule', 'Permanent Military Rule', [
            prog('political_power_factor', 0.10), prog('conscription_factor', 0.05),
            prog('drift_defence_factor', 0.10), fac('the_military', 10), prog('research_speed_factor', -0.02),
        ], 'Brazil (1964-85) and Chile (1973-90) turned the coup into a regime with its own constitution; the universities and the middle class paid with their freedoms.', old=True),
        'A1f': F('jun_the_return_to_the_barracks', 'The Return to the Barracks', [
            stab(0.05), pop(0.05),
            idea('jun_guardian_army', {'stability_factor': 0.03, 'defensive_war_stability_factor': 0.15, 'army_personnel_cost_multiplier_modifier': -0.05}, 'The Guardian Army'),
            fac('the_military', -10),
        ], 'After the 1973 elections the Turkish army stepped back but kept its voice in the National Security Council as guardian of the state; the officers lost office but kept their prestige.', old=True),
        'A2f': F('jun_national_security_doctrine', 'National Security Doctrine', [
            prog('drift_defence_factor', 0.20), prog('intel_network_gain_factor', 0.20), mdidea('idea_focus_generic_counter_terrorism'),
            fac('intelligence_community', 10), law('increase_policing_budget'), corruption_chance(),
        ], 'Brazil\'s Escola Superior de Guerra taught that the enemy was internal; the Southern Cone juntas adopted versions of the doctrine and the police budget grew with it.', old=True),
        'PM': F('jun_rule_by_decree_law', 'Rule by Decree-Law', [
            prog('political_power_factor', 0.10), prog('bureaucracy_cost_multiplier_modifier', -0.10), fac('the_military', 5),
            fac('labour_unions', -5),
        ], 'Juntas governed through numbered decree-laws (Chile\'s junta issued some 3,500 by 1980): fast, but without the consent parliament had provided.'),

        # ---------------- the economic model
        'ECO': F('jun_the_economic_team', 'The Economic Team', [
            prog('production_speed_buildings_factor', 0.05), prog('tax_gain_multiplier_modifier', 0.03),
            fac('industrial_conglomerates', 5), fac('small_medium_business_owners', 5),
        ], 'Most juntas appointed civilian economists under a general: Roberto Campos in Brazil, Martínez de Hoz in Argentina, the ODEPLAN team in Chile.'),
        'B1': F('jun_the_chicago_boys', 'The Chicago Boys', [
            prog('productivity_growth_modifier', 0.10), prog('receiving_investment_cost_modifier', -0.15), money(0.01),
            fac('wall_street', 10), fac('labour_unions', -15), prog('consumer_goods_factor', 0.02),
        ], 'Chile\'s 1975 "shock treatment" (Sergio de Castro and other Chicago-trained economists) sold state firms and opened the economy; wages and unions bore the cost.'),
        'B2': F('jun_military_developmentalism', 'Military Developmentalism', [
            prog('production_speed_buildings_factor', 0.10), prog('industrial_capacity_factory', 0.05),
            fac('industrial_conglomerates', 10), debt(0.02),
        ], 'Brazil\'s "economic miracle" (1968-73) and Velasco\'s Peru built state industries with foreign loans; growth was real and so was the debt that came due in the 1980s.'),
        'B1f': F('jun_privatise_the_state_firms', 'Privatise the State Firms', [
            build('two_office_construction'), money(0.01), prog('tax_gain_multiplier_modifier', 0.05),
            fac('labour_unions', -5), stab(-0.02),
        ], 'Between 1974 and 1978 Chile returned or sold off most of the several hundred firms taken over under Allende, cutting state losses and raising some revenue.'),
        'B2f': F('jun_state_enterprises_in_uniform', 'State Enterprises in Uniform', [
            build('two_random_industrial_complex'), build('one_random_arms_factory'), fac('defense_industry', 10),
            tech(['CAT_aircraft'], 0.25, 2), prog('corruption_cost_factor', 0.10),
        ], 'Brazil\'s Embraer (1969) and Argentina\'s Fabricaciones Militares put officers in charge of steel, aircraft and arms plants.'),
        'EM': F('jun_order_and_progress', 'Order and Progress', [
            growth(1), prog('stability_factor', 0.02), fac('the_military', 5),
        ], 'Juntas justified themselves by results: while the economy grew, the barracks and the middle class stayed loyal.'),

        # ---------------- internal security
        'C1': F('jun_the_counter_subversion_campaign', 'The Counter-Subversion Campaign', [
            prog('drift_defence_factor', 0.15), prog('mdcw_cw_ideological_defence', 0.10),
            prog('intelligence_agency_defense', 0.15), prog('encryption_factor', 0.10), prog('decryption_factor', 0.10), fac('intelligence_community', 10),
            prog('trade_opinion_factor', -0.05), stab(-0.02),
        ], 'Operation Condor (1975) linked the Southern Cone secret services to pursue opponents across borders; over such abuses the US Congress cut military aid to Chile (1976) and Argentina (1978).'),
        'C2': F('jun_civic_action', 'Civic Action', [
            build('three_random_infrastructure'), literacy(0.03), stab(0.03),
            prog('training_time_army_factor', 0.05), money(-0.005),
        ], 'Peruvian, Thai and Indonesian (dwifungsi) officers built roads, schools and clinics in the countryside to win the villages; the troops trained less.'),
        'CM': F('jun_pacification_declared', 'Pacification Declared', [
            stab(0.05), prog('war_support_factor', 0.05), prog('required_garrison_factor', -0.10), fac('the_military', 5),
        ], 'Once the insurgency was broken the regime declared victory and lifted the state of siege, as Chile\'s junta did in March 1978, replacing it with a state of emergency.'),

        # ---------------- arms and allies
        'D1': F('jun_the_pentagon_connection', 'The Pentagon Connection', [
            tech(['CAT_aircraft', 'CAT_helicopters'], 0.35, 2), prog('mdcw_cw_assistance_limit', 0.25),
            xp('air', 50), outlook('W', 0.02), prog('foreign_influence_defense_modifier', -0.05),
        ], 'US military aid and IMET training (F-5 fighters, Huey helicopters) equipped most anti-communist juntas, along with American influence over their officers.'),
        'D2': F('jun_arms_without_strings', 'Arms Without Strings', [
            build('two_random_arms_factory'), tech(['CAT_small_arms', 'CAT_armor'], 0.35, 2), fac('defense_industry', 10),
            money(-0.005),
        ], 'After the US human-rights embargoes, and Brazil\'s 1977 break with US military aid, the juntas bought from France and Israel and built their own weapons (Brazil\'s Engesa, Chile\'s FAMAE): independent but expensive.'),
        'DM': F('jun_modernise_the_armed_forces', 'Modernise the Armed Forces', [
            xp('army', 50), xp('air', 25), tech(['CAT_main_battle_tanks', 'CAT_surface_ships'], 0.25, 2),
            prog('army_org_factor', 0.05), prog('army_personnel_cost_multiplier_modifier', 0.03),
        ], 'The juntas spent their money on the forces that kept them in power: Argentina\'s junta bought Israeli and French jets and German-designed tanks and warships between 1976 and 1982.'),

        # ---------------- capstone
        'CAP': F('jun_the_officer_corps_state', 'The Officer Corps State', [
            idea('jun_officer_corps_state', {'political_power_factor': 0.10, 'stability_factor': 0.05, 'army_org_factor': 0.05,
                                              'conscription_factor': 0.03, 'research_speed_factor': -0.03}, 'The Officer Corps State', bound=True),
            fac('the_military', 10), xp('army', 25),
        ], 'At its height the military state ran ministries, governorships and state firms through serving officers, as in Brazil under Médici or Argentina under the Proceso.', old=True),
    },
)]
