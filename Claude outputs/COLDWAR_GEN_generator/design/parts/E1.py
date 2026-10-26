# IMPERIA CW — Cold War: parts — E1.
from dsl import *

# Emerging outlook: trunk + Communist State (cs), Anarchist Communism (ac), Conservative Emerging (ce).

TRUNKS = [dict(
    outlook='E',
    title='The Socialist Camp',
    note='The Emerging outlook is built either through workplace organisation (party cells: efficiency and union loyalty, '
         'business pays) or through the party press (campaign reach and ideological defence, paid for with newsprint '
         'subsidies). Both lead to the mass movement and to the revolutionary government that opens the six party paths.',
    foci={
        'T0': F('champion_emerging', 'Champion the Socialist Camp', [
            outlook('E', 0.05),
            timed('trunk_e_socialist_awakening', 1095, {'communism_drift': 0.05, 'mdcw_cw_ideological_defence': 0.10}, 'A Socialist Awakening'),
            fac('communist_cadres', 10), fac('wall_street', -5),
        ], 'In the early 1970s the left was on the rise from Chile (Allende 1970) to Portugal (1974); communist and socialist parties grew wherever they could organise openly.', old=True),
        'T1a': F('party_cells_in_the_factories', 'Party Cells in the Factories', [
            outlook('E', 0.03),
            timed('trunk_e_factory_cells', 1095, {'production_factory_efficiency_gain_factor': 0.10, 'stability_factor': 0.02}, 'Factory Cells'),
            fac('communist_cadres', 10), fac('labour_unions', 10), fac('industrial_conglomerates', -10),
        ], 'The Italian and French communist parties built their strength on factory cells, and Chile\'s "cordones industriales" (1972) organised whole industrial belts; employers lost control of the shop floor.', old=True),
        'T1b': F('the_workers_press', 'The Workers\' Press', [
            outlook('E', 0.03),
            timed('trunk_e_party_press', 1095, {'mdcw_cw_support_effectiveness': 0.10, 'mdcw_cw_ideological_defence': 0.15, 'communism_drift': 0.03}, 'The Party Press'),
            fac('communist_cadres', 5), literacy(0.02), money(-0.005),
        ], 'Party dailies such as L\'Humanité and l\'Unità sold hundreds of thousands of copies, and Radio Moscow and Radio Peking broadcast worldwide; the presses ran on subsidies.', old=True),
        'T2': F('the_toiling_masses_awaken', 'The Toiling Masses Awaken', [
            outlook('E', 0.05),
            timed('trunk_e_mass_movement', 1095, {'drift_defence_factor': 0.15, 'communism_drift': 0.05, 'party_popularity_stability_factor': 0.10}, 'The Mass Movement'),
        ], 'By 1975 communist parties polled a third of the vote in Italy and were a leading force in Portugal\'s revolution; a mass movement makes the outlook hard to dislodge.', old=True),
        'T3': F('a_revolutionary_government', 'A Revolutionary Government', [
            pp(75), stab(0.03), fac('communist_cadres', 10), outlook('W', -0.03),
            note('+50 political power more if The Toiling Masses Awaken is completed.'),
        ], 'A new socialist government first fills the ministries and key posts with its own people, as Allende\'s Popular Unity cabinet (1970) and Vasco Gonçalves\'s provisional governments in Portugal (1974-75) did.', old=True),
    },
)]

PARTIES = [
    # =====================================================================================================
    dict(
        key='cs',
        title='The Party-State',
        identity='The vanguard party owns the state, the plan and the future, and must decide whether to freeze the system '
                 'in stability or to reform it before it stagnates.',
        history='The Soviet-type states of the 1970s chose between Brezhnev\'s "stability of cadres" and the reform line of '
                'Kosygin (1965) and Kádár\'s New Economic Mechanism (1968); between Honecker\'s consumer welfare (1971) and the '
                'heavy industry of the military-industrial commission; between Husák\'s normalisation and Kádár\'s quiet '
                'tolerance; between bloc integration (Comecon Complex Programme 1971) and trade with the West in détente.',
        foci={
            'E': F('cs_the_vanguard_party', 'The Vanguard Party', [
                prog('political_power_factor', 0.05), prog('drift_defence_factor', 0.10), prog('stability_factor', 0.02),
                fac('communist_cadres', 10), pop(0.05), law('increase_centralization'),
            ], 'The ruling communist party places itself above the state: the party leads, the ministries execute, as most Soviet-type constitutions came to state outright.', old=True),

            # ---------------- the power question
            'POL': F('cs_the_politburo_decides', 'The Politburo Decides', [
                pp(100), stab(0.02), fac('communist_cadres', 5), outlook('W', -0.03),
            ], 'After Khrushchev\'s fall (1964) the Soviet Presidium, renamed Politburo in 1966, ruled as a collective leadership around Brezhnev; the bloc parties copied the model of decisions taken in a closed circle.'),
            'A1': F('cs_the_stability_of_cadres', 'The Stability of Cadres', [
                prog('stability_factor', 0.05), prog('political_power_factor', 0.05), prog('drift_defence_factor', 0.15),
                fac('communist_cadres', 10), prog('productivity_growth_modifier', -0.05), prog('corruption_cost_factor', 0.05),
            ], 'Brezhnev\'s "stability of cadres", proclaimed after Khrushchev\'s constant reshuffles, left officials in post for decades; the apparatus was grateful and loyal, the economy slowly stagnated.', old=True),
            'A2': F('cs_reform_communism', 'Reform Communism', [
                prog('productivity_growth_modifier', 0.10), prog('research_speed_factor', 0.03), prog('consumer_goods_factor', -0.02),
                prog('production_factory_efficiency_gain_factor', 0.10),
                fac('communist_cadres', -10), stab(-0.02),
            ], 'The Kosygin reform (1965) and Hungary\'s New Economic Mechanism (1968) gave enterprises profit targets and more freedom; the party conservatives saw their control slip.', old=True),
            'A1f': F('cs_the_nomenklatura', 'The Nomenklatura', [
                pp(100), prog('bureaucracy_cost_multiplier_modifier', -0.10), fac('communist_cadres', 10),
                idea('cs_nomenklatura_system', {'political_power_factor': 0.10, 'stability_factor': 0.03, 'corruption_cost_factor': 0.10},
                     'The Nomenklatura System', bound=True),
                corruption_chance(),
            ], 'Every important post from factory director to editor was filled from the party\'s nomenklatura lists; the system was reliable and slowly became a caste.', old=True),
            'A2f': F('cs_economic_accounting_reform', 'Economic Accounting Reform', [
                prog('industrial_capacity_factory', 0.05), prog('consumer_goods_factor', -0.02), prog('tax_gain_multiplier_modifier', 0.03),
                build('two_random_industrial_complex'), fac('communist_cadres', -5),
            ], 'Under "khozraschet" (cost accounting) enterprises kept part of their profits for bonus and investment funds; Hungary\'s NEM went further, freeing many prices and ending compulsory plan targets for firms.', old=True),
            'PM': F('cs_the_congress_line', 'The Congress Line', [
                prog('political_power_factor', 0.05), stab(0.03), pop(0.03), fac('communist_cadres', 5),
            ], 'Each five-yearly party congress fixed the line for the next plan; the 24th CPSU Congress (1971) set the course of the decade.'),

            # ---------------- the economic model
            'ECO': F('cs_the_new_five_year_plan', 'The New Five-Year Plan', [
                prog('production_speed_buildings_factor', 0.05), prog('industrial_capacity_factory', 0.03), fac('communist_cadres', 5),
                build('one_random_industrial_complex'),
            ], 'The Soviet ninth five-year plan (1971-75) was the first to promise that consumer goods would grow faster than heavy industry.'),
            'B1': F('cs_unity_of_economic_and_social_policy', 'Unity of Economic and Social Policy', [
                prog('consumer_goods_factor', -0.04), prog('stability_factor', 0.04), prog('monthly_population', 0.10),
                law('increase_social_spending'), debt(0.01),
            ], 'Honecker\'s 1971 programme promised flats, subsidised prices and consumer goods (the 1973 housing programme); welfare bought loyalty and ran up a debt.'),
            'B2': F('cs_the_heavy_industry_line', 'The Heavy Industry Line', [
                prog('industrial_capacity_factory', 0.05), prog('production_speed_arms_factory_factor', 0.10), fac('defense_industry', 10),
                build('one_random_arms_factory'), prog('consumer_goods_factor', 0.03),
            ], 'Soviet planning kept priority for "Group A" heavy industry and the defence sector under Dmitri Ustinov; consumer supply lagged while the arsenals grew.'),
            'B1f': F('cs_licences_from_the_west', 'Licences from the West', [
                build('two_random_industrial_complex'), tech('CAT_computing', 0.35, 2), prog('productivity_growth_modifier', 0.05),
                prog('receiving_investment_cost_modifier', -0.10), debt(0.02),
            ], 'Gierek\'s Poland bought Western licences (Fiat cars, Massey Ferguson tractors) and whole plants on credit in the 1970s; modern factories rose and the foreign debt passed 20 billion dollars by 1980.'),
            'B2f': F('cs_the_military_industrial_commission', 'The Military-Industrial Commission', [
                build('two_random_arms_factory'), tech(['CAT_main_battle_tanks', 'CAT_medium_aircraft'], 0.35, 1),
                prog('military_factories_productivity', 0.05), fac('defense_industry', 10), fac('labour_unions', -5),
            ], 'The Soviet VPK coordinated the defence ministries and gave them first call on steel, engineers and research institutes.'),
            'EM': F('cs_the_comecon_complex_programme', 'The Comecon Complex Programme', [
                prog('imp_sanction_resistance', 0.10), prog('trade_opinion_factor', 0.05),
                prog('production_factory_efficiency_gain_factor', 0.05),
            ], 'Comecon\'s Complex Programme (1971) divided production between the member states through specialisation and joint projects such as the Soyuz gas pipeline, keeping most of their trade inside the bloc.'),

            # ---------------- society and security
            'C1': F('cs_normalisation', 'Normalisation', [
                prog('drift_defence_factor', 0.15), prog('mdcw_cw_ideological_defence', 0.10), prog('intelligence_agency_defense', 0.10),
                fac('intelligence_community', 10), stab(0.03),
                prog('research_speed_factor', -0.02), law('increase_policing_budget'),
            ], 'After 1969 Husák expelled or struck off hundreds of thousands of party members in Czechoslovakia and bought quiet with consumer goods; thousands of academics, writers and artists lost their posts.'),
            'C2': F('cs_socialist_legality', 'Socialist Legality', [
                prog('research_speed_factor', 0.03), prog('stability_factor', 0.03), prog('party_popularity_stability_factor', 0.10),
                fac('small_medium_business_owners', 10), prog('foreign_influence_defense_modifier', -0.05), outlook('W', 0.02),
            ], 'Kádár\'s "who is not against us is with us" (1961) let Hungarians travel, read and trade a little; it was widely seen as the most liberal regime in the bloc and the most open to Western ideas.'),
            'CM': F('cs_the_leading_role_of_the_party', 'The Leading Role of the Party', [
                stab(0.05), pop(0.03),
                idea('cs_leading_role_article', {'political_power_factor': 0.05, 'drift_defence_factor': 0.10, 'stability_factor': 0.02},
                     'The Leading Role Article', bound=True),
            ], 'The Soviet constitution of 1977 (Article 6) and the GDR constitution of 1968 wrote the party\'s leading role into the basic law.'),

            # ---------------- allies and arms
            'D1': F('cs_fraternal_assistance', 'Fraternal Assistance', [
                tech(['CAT_armor', 'CAT_medium_aircraft'], 0.35, 2), prog('mdcw_cw_assistance_limit', 0.25), xp('army', 50),
                prog('foreign_influence_defense_modifier', -0.05), tension(1),
            ], 'Soviet arms, advisers and staff training tied the Warsaw Pact armies to Moscow after the 1969 reform of the Pact\'s joint command.'),
            'D2': F('cs_detente_and_trade', 'Détente and Trade', [
                tension(-2), prog('trade_opinion_factor', 0.10), prog('research_speed_factor', 0.02),
                prog('receiving_investment_cost_modifier', -0.10), prog('drift_defence_factor', -0.10), outlook('W', 0.02),
            ], 'Détente brought Western grain, credits and technology to the East (Brandt\'s treaties 1970-72, Helsinki 1975), and with them Western ideas.'),
            'DM': F('cs_socialist_military_doctrine', 'Socialist Military Doctrine', [
                xp('army', 50), prog('army_org_factor', 0.03), prog('conscription_factor', 0.03), prog('command_power_gain', 0.10),
                law('increase_military_spending'),
            ], 'Warsaw Pact armies trained for a fast offensive war in Europe; large exercises such as "Soyuz" and "Zapad" (1981) tested the doctrine.'),

            # ---------------- capstone
            'CAP': F('cs_developed_socialism', 'Developed Socialism', [
                idea('cs_developed_socialism', {'stability_factor': 0.05, 'production_factory_max_efficiency_factor': 0.05,
                                                'political_power_factor': 0.05, 'productivity_growth_modifier': -0.05},
                     'Developed Socialism', bound=True),
                build('two_random_industrial_complex'), fac('communist_cadres', 10),
            ], 'In 1971 Brezhnev declared the USSR a "developed socialist society": a mature, stable system that no longer needed upheaval, and slowly stopped changing.', old=True),
        },
    ),

    # =====================================================================================================
    dict(
        key='ac',
        title='Power to the Masses',
        identity='The radical left distrusts the bureaucratic state: power goes to communes, councils and mass campaigns, '
                 'and the party must choose between workers\' self-government and permanent revolution.',
        history='The radical currents of the 1960s-70s offered two roads: self-management by councils (Yugoslavia\'s 1974 '
                'constitution, Chile\'s cordones 1972, Portugal\'s occupations 1975) or permanent revolution through mass '
                'campaigns (China\'s Cultural Revolution 1966-76, Down to the Countryside, Albania\'s self-reliance). '
                'Cambodia (1975-79) showed where forced collectivisation without limits ends.',
        foci={
            'E': F('ac_power_to_the_communes', 'Power to the Communes', [
                prog('stability_factor', 0.03), prog('bureaucracy_cost_multiplier_modifier', -0.10),
                fac('farmers', 10), fac('labour_unions', 10), law('decrease_centralization'),
            ], 'The radical left hands authority to local communes and councils, as the Paris Commune ideal and Yugoslav "social self-government" promised.', old=True),

            # ---------------- the power question
            'POL': F('ac_the_general_assembly', 'The General Assembly', [
                pp(75), pop(0.04), prog('party_popularity_stability_factor', 0.05), outlook('W', -0.03), fac('communist_cadres', 5),
            ], 'Assemblies of delegates from factories and villages take the place of party parliaments, as in Yugoslavia\'s 1974 delegate system or the popular assemblies proposed in Portugal in 1975.'),
            'A1': F('ac_workers_councils', 'Workers\' Councils', [
                prog('productivity_growth_modifier', 0.10), prog('bureaucracy_cost_multiplier_modifier', -0.10), fac('labour_unions', 10),
                prog('production_factory_efficiency_gain_factor', 0.05), prog('political_power_factor', -0.05),
            ], 'Yugoslav workers\' councils chose the managers and divided the income; the factories worked, but the centre lost its grip on decisions.', old=True),
            'A2': F('ac_cultural_revolution', 'Cultural Revolution', [
                prog('war_support_factor', 0.10), prog('drift_defence_factor', 0.20), prog('mdcw_cw_ideological_defence', 0.10), pop(0.04),
                prog('research_speed_factor', -0.03), stab(-0.02),
            ], 'China\'s Cultural Revolution (1966-76) mobilised the young against "revisionists" in the party; it bred fervent loyalty to Mao but also violent purges, and schools and universities closed for years.', old=True),
            'A1f': F('ac_federation_of_communes', 'Federation of Communes', [
                prog('production_speed_buildings_factor', 0.10), prog('bureaucracy_cost_multiplier_modifier', -0.05),
                fac('farmers', 5), fac('labour_unions', 5),
            ], 'The 1974 Yugoslav constitution devolved power to the republics, communes and self-managed enterprises; investment no longer waited for Belgrade, though projects were often duplicated.', old=True),
            'A2f': F('ac_down_to_the_countryside', 'Down to the Countryside', [
                prog('agricolture_productivity_modifier', 0.10), prog('buildings_worker_requirement_modifier', -0.05),
                build('two_random_agriculture_district'), prog('research_speed_factor', -0.02),
            ], 'From 1968 some seventeen million Chinese urban youths were sent to the villages over a decade; fields gained hands, the universities lost a generation.', old=True),
            'PM': F('ac_the_mass_line', 'The Mass Line', [
                stab(0.03), pop(0.04), fac('communist_cadres', 10), prog('drift_defence_factor', 0.05),
            ], '"From the masses, to the masses": the Maoist mass line made cadres live and work among the people they governed.'),

            # ---------------- the economic model
            'ECO': F('ac_expropriate_the_estates', 'Expropriate the Estates', [
                prog('agricolture_productivity_modifier', 0.05), prog('production_speed_agriculture_district_factor', 0.10),
                fac('farmers', 10), money(0.005), fac('landowners', -10),
            ], 'The 1975 land occupations in Portugal\'s Alentejo turned the great estates into collective farms run by the labourers.'),
            'B1': F('ac_rely_on_our_own_strength', 'Rely on Our Own Strength', [
                prog('imp_sanction_resistance', 0.10), prog('production_speed_buildings_factor', 0.05), prog('globalism_equilibrium', -5),
                prog('industrial_capacity_factory', 0.05), prog('resource_export_multiplier_modifier', 0.07), prog('trade_opinion_factor', -0.10),
            ], 'China\'s "self-reliance" (zili gengsheng) and Albania\'s isolation after 1978 made the economy hard to blockade but cut it off from foreign technology and trade.'),
            'B2': F('ac_mass_mobilisation_campaigns', 'Mass Mobilisation Campaigns', [
                prog('production_speed_buildings_factor', 0.10), prog('production_speed_infrastructure_factor', 0.15),
                build('one_random_agriculture_district'), prog('productivity_growth_modifier', -0.05), stab(-0.02),
            ], 'Campaigns like "Learn from Dazhai" (1964-) and Cuba\'s ten-million-ton harvest (1970) threw whole populations at dams, terraces and canefields; much was built, much was wasted.'),
            'B1f': F('ac_local_industry_in_every_county', 'Local Industry in Every County', [
                build('two_random_industrial_complex'), build('one_random_fossil_fuel_powerplant'),
                prog('production_speed_industrial_complex_factor', 0.10), fac('farmers', 5), prog('industrial_capacity_factory', -0.02),
            ], 'China\'s "five small industries" (1970) put steel, cement, fertiliser, machine and power plants in county after county; small, inefficient and independent.'),
            'B2f': F('ac_volunteer_labour_brigades', 'Volunteer Labour Brigades', [
                build('two_random_infrastructure'), prog('production_speed_infrastructure_factor', 0.10), stab(0.02),
                prog('social_cost_multiplier_modifier', -0.05), fac('labour_unions', 5), prog('consumer_goods_factor', 0.02),
            ], 'Cuba\'s microbrigades (1970-) built housing with volunteer labour and Chinese water-conservancy campaigns dug canals by hand; the workplaces they left had to make up their output.'),
            'EM': F('ac_moral_not_material_incentives', 'Moral, Not Material, Incentives', [
                prog('consumer_goods_factor', -0.04), prog('stability_factor', 0.02), fac('communist_cadres', 5), pop(0.03),
                prog('productivity_growth_modifier', -0.03),
            ], 'Guevara\'s "new man" and the Maoist campaigns replaced bonuses with honours and emulation; less went on consumer goods, but absenteeism spread (Cuba passed an anti-loafing law in 1971).'),

            # ---------------- society and security
            'C1': F('ac_revolutionary_committees', 'Revolutionary Committees', [
                prog('drift_defence_factor', 0.10), prog('political_power_factor', 0.05), prog('bureaucracy_cost_multiplier_modifier', -0.05),
                prog('mdcw_cw_ideological_defence', 0.10), prog('war_support_factor', 0.03), fac('the_military', 5),
                fac('communist_cadres', -5), stab(-0.02),
            ], 'From 1967 Chinese "three-in-one" committees of soldiers, cadres and rebels replaced the party committees and governments of every province by 1968.'),
            'C2': F('ac_barefoot_doctors', 'Barefoot Doctors', [
                prog('health_cost_multiplier_modifier', -0.10), literacy(0.04), prog('monthly_population', 0.05), stab(0.02),
                money(-0.005),
            ], 'From 1968 over a million Chinese "barefoot doctors" and night schools brought basic medicine and reading to the villages at a fraction of the cost.'),
            'CM': F('ac_serve_the_people', 'Serve the People', [
                stab(0.05), pop(0.04), prog('party_popularity_stability_factor', 0.10),
            ], 'The "Serve the People" and Lei Feng campaigns (1963-) held up selfless service as the model citizen of the new society.'),

            # ---------------- allies and arms
            'D1': F('ac_support_the_world_revolution', 'Support the World Revolution', [
                prog('mdcw_cw_support_effectiveness', 0.10), prog('mdcw_cw_assistance_capacity', 1), prog('foreign_influence_modifier', 0.10),
                xp('army', 50), tension(1), money(-0.005),
            ], 'China and Cuba trained, armed and funded liberation movements in the 1960s-70s, from Africa to Latin America (Cuba in Angola, 1975).'),
            'D2': F('ac_a_people_s_war_defence', 'A People\'s War Defence', [
                prog('army_core_defence_factor', 0.10), prog('defensive_war_stability_factor', 0.15), prog('production_speed_bunker_factor', 0.20),
                money(-0.005),
            ], 'Mao\'s "people\'s war" and Albania\'s bunker programme (1967-86, over 170,000 bunkers) prepared every village to resist an invasion.'),
            'DM': F('ac_the_armed_masses', 'The Armed Masses', [
                prog('conscription_factor', 0.05), xp('army', 50), tech('CAT_small_arms', 0.5, 1),
            ], 'People\'s militias armed the population on a mass scale: the Chinese militia counted tens of millions in the early 1970s.'),

            # ---------------- capstone
            'CAP': F('ac_the_new_society', 'The New Society', [
                idea('ac_new_society', {'stability_factor': 0.05, 'drift_defence_factor': 0.20, 'productivity_growth_modifier': 0.05,
                                        'bureaucracy_cost_multiplier_modifier': -0.10, 'research_speed_factor': -0.03},
                     'The New Society', bound=True),
                fac('communist_cadres', 10), fac('labour_unions', 5), pop(0.05),
            ], 'The radical left promised a society without bosses or bureaucrats; where it governed, it built communes, councils and a deep suspicion of experts.', old=True),
        },
    ),

    # =====================================================================================================
    dict(
        key='ce',
        title='The Institutional Revolution',
        identity='The revolution has become an institution: a dominant party rules through patronage, corporatist pacts and '
                 'the state sector, and must choose between buying peace and renewing itself.',
        history='Post-revolutionary dominant parties of the 1970s - Mexico\'s PRI, Algeria\'s FLN under Boumédiène, Tanzania\'s '
                'TANU, Egypt\'s Arab Socialist Union, Burma\'s BSPP - chose between corporatist patronage and technocratic '
                'renewal, between resource nationalism (Algeria 1971) and opening to capital (Egypt\'s Infitah 1974), and '
                'between a Soviet treaty and playing the blocs against each other.',
        foci={
            'E': F('ce_the_ruling_party_endures', 'The Ruling Party Endures', [
                prog('stability_factor', 0.05), prog('political_power_factor', 0.05),
                fac('labour_unions', 5), fac('industrial_conglomerates', 5),
            ], 'Mexico\'s PRI had ruled under various names since 1929 and Algeria\'s FLN since 1962: the party is the state, and the state hands out the jobs.', old=True),

            # ---------------- the power question
            'POL': F('ce_heirs_of_the_revolution', 'Heirs of the Revolution', [
                pp(100), pop(0.04), prog('drift_defence_factor', 0.05),
            ], 'Dominant parties ruled in the name of a founding revolution (1910 in Mexico, 1954 in Algeria, 1952 in Egypt) and claimed its legitimacy for every new leader.'),
            'A1': F('ce_the_corporatist_pact', 'The Corporatist Pact', [
                fac('labour_unions', 10), fac('farmers', 10), fac('industrial_conglomerates', 10), prog('stability_factor', 0.05),
                corruption_chance(),
            ], 'The PRI organised society in sectors (CTM labour, CNC peasants, CNOP middle class): every group had a seat at the table and a share of the patronage.', old=True),
            'A2': F('ce_technocratic_renewal', 'Technocratic Renewal', [
                prog('research_speed_factor', 0.03), prog('productivity_growth_modifier', 0.05),
                prog('bureaucracy_cost_multiplier_modifier', -0.10), prog('production_factory_efficiency_gain_factor', 0.05),
                fac('oligarchs', -5), fac('labour_unions', -5),
            ], 'In the 1970s planners and economists ("técnicos") gained ground against the old party bosses in Mexico and Algeria; efficiency rose, the old networks resented it.', old=True),
            'A1f': F('ce_official_trade_unions', 'Official Trade Unions', [
                prog('stability_factor', 0.03), prog('party_popularity_stability_factor', 0.10), fac('labour_unions', 10),
                idea('ce_sector_organisations', {'stability_factor': 0.03, 'political_power_factor': 0.05, 'corruption_cost_factor': 0.10},
                     'The Sector Organisations', bound=True),
                law('increase_social_spending'),
            ], 'Fidel Velázquez\'s CTM delivered Mexican labour peace for decades in exchange for wages, housing funds (INFONAVIT 1972) and seats in Congress.', old=True),
            'A2f': F('ce_the_planning_ministry', 'The Planning Ministry', [
                prog('production_speed_buildings_factor', 0.10), build('one_office_construction'), tech('CAT_computing', 0.35, 2),
                money(-0.005),
            ], 'Algeria\'s Secretariat of Planning and Mexico\'s Ministry of Programming and Budget (1976) gave the technocrats their own power base.', old=True),
            'PM': F('ce_the_chosen_successor', 'The Chosen Successor', [
                stab(0.03), prog('political_power_factor', 0.05), fac('all', 3), prog('drift_defence_factor', 0.05),
            ], 'The PRI\'s outgoing president named his successor (the "dedazo", 1970 and 1976); the party closed ranks and the transfer of power stayed peaceful.'),

            # ---------------- the economic model
            'ECO': F('ce_the_state_sector', 'The State Sector', [
                prog('production_speed_buildings_factor', 0.05), prog('tax_gain_multiplier_modifier', 0.03), fac('industrial_conglomerates', 5),
                build('one_random_industrial_complex'),
            ], 'State firms such as Pemex, Sonatrach and Egypt\'s public sector companies were the backbone of the dominant-party economy.'),
            'B1': F('ce_nationalise_the_resources', 'Nationalise the Resources', [
                money(0.015), prog('resource_export_multiplier_modifier', 0.10), prog('imp_oil_price_resistance', 0.10), fac('fossil_fuel_industry', 10),
                prog('receiving_investment_cost_modifier', 0.10), fac('wall_street', -5),
            ], 'On 24 February 1971 Algeria took 51 % of the French oil companies; Iraq (1972) and Venezuela (1976) followed. Revenue flowed home and foreign investors grew wary.'),
            'B2': F('ce_the_opening_to_capital', 'The Opening to Capital', [
                prog('receiving_investment_cost_modifier', -0.15), prog('office_park_income_tax_modifier', 0.05),
                fac('small_medium_business_owners', 10), fac('wall_street', 5),
                prog('mdcw_cw_market_exposure', 0.05), fac('labour_unions', -5),
            ], 'Sadat\'s Infitah (1974) and Mexico\'s border industry programme (1965) invited foreign investors with tax breaks; business boomed and the economy became exposed.'),
            'B1f': F('ce_industrialising_industries', 'Industrialising Industries', [
                build('two_random_industrial_complex'), build('one_random_synthetic_refinery'),
                prog('industrial_capacity_factory', 0.03), prog('energy_gain_multiplier', 0.05), debt(0.01),
            ], 'Boumédiène spent the oil money on "industrialising industries": the El Hadjar steelworks, gas liquefaction and petrochemicals (plans 1970-77).'),
            'B2f': F('ce_joint_ventures', 'Joint Ventures', [
                build('two_office_construction'), prog('productivity_growth_modifier', 0.05), prog('trade_opinion_factor', 0.05),
                money(0.005), stab(-0.02),
            ], 'Egypt\'s Infitah brought joint ventures with Western and Gulf capital; when subsidies were cut the 1977 bread riots followed.'),
            'EM': F('ce_shared_development', 'Shared Development', [
                growth(1), stab(0.03), law('increase_social_spending'),
            ], 'Echeverría\'s "desarrollo compartido" (1970-76) expanded state investment and social programmes to share the fruits of growth.'),

            # ---------------- society
            'C1': F('ce_subsidies_and_patronage', 'Subsidies and Patronage', [
                prog('consumer_goods_factor', -0.05), stab(0.05), pop(0.06),
                prog('social_cost_multiplier_modifier', 0.05), corruption_chance(),
            ], 'Cheap bread, fuel and staples through CONASUPO in Mexico and Egypt\'s ration system kept the cities quiet and the budget strained.'),
            'C2': F('ce_the_agrarian_revolution', 'The Agrarian Revolution', [
                build('two_random_agriculture_district'), prog('agricolture_productivity_modifier', 0.05),
                prog('production_speed_agriculture_district_factor', 0.10), fac('farmers', 10),
                fac('landowners', -10), stab(-0.02),
            ], 'Algeria\'s Agrarian Revolution (1971) handed large estates to cooperatives against the landowners\' resistance, and Tanzania\'s villagisation (1973-76) moved millions of peasants into Ujamaa villages, often by force.'),
            'CM': F('ce_the_mass_organisations', 'The Mass Organisations', [
                literacy(0.03), prog('drift_defence_factor', 0.10), prog('mdcw_cw_ideological_defence', 0.10), pop(0.04), stab(0.03),
            ], 'Youth, women\'s and peasant unions of the ruling party (the FLN\'s UNJA, the ASU youth) reached into every village and school.'),

            # ---------------- foreign stance
            'D1': F('ce_a_treaty_of_friendship', 'A Treaty of Friendship', [
                tech(['CAT_armor', 'CAT_surface_to_air_missiles'], 0.35, 2), prog('mdcw_cw_assistance_limit', 0.25), xp('army', 50),
                outlook('E', 0.02),
                prog('foreign_influence_defense_modifier', -0.05), tension(1),
            ], 'Egypt (1971), India (1971), Iraq (1972) and Somalia (1974) signed friendship treaties with Moscow: arms and advisers in return for influence.'),
            'D2': F('ce_play_the_blocs', 'Play the Blocs Against Each Other', [
                prog('foreign_influence_defense_modifier', 0.10), prog('trade_opinion_factor', 0.10), prog('foreign_influence_modifier', 0.05),
                prog('political_power_factor', 0.03), tension(-1), outlook('N', 0.03), money(-0.005),
            ], 'Sadat expelled the Soviet advisers in 1972 and courted Washington, and Algeria led the Non-Aligned Movement (1973): trade and favours from both sides, loyalty to neither.'),
            'DM': F('ce_party_and_army_united', 'Party and Army United', [
                xp('army', 50), prog('army_org_factor', 0.03), fac('the_military', 10), tech('CAT_small_arms', 0.35, 2),
                law('increase_military_spending'),
            ], 'In Algeria, Egypt and Burma soldiers had made the regime (the Free Officers in 1952, Ne Win in 1962, Boumédiène in 1965); the dominant party kept the army inside the regime with budgets and honours.'),

            # ---------------- capstone
            'CAP': F('ce_sovereign_development', 'Sovereign Development', [
                idea('ce_sovereign_development', {'stability_factor': 0.05, 'production_speed_buildings_factor': 0.05,
                                                  'political_power_factor': 0.05, 'tax_gain_multiplier_modifier': 0.05,
                                                  'corruption_cost_factor': 0.10}, 'Sovereign Development'),
                growth(1), pop(0.04),
            ], 'The dominant parties defined success as development on their own terms: Mexico\'s "stabilising development" (1954-70) and Algeria\'s plans delivered long years of rapid growth.', old=True),
        },
    ),
]
