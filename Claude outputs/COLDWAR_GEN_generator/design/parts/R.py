# IMPERIA CW — Cold War: parts — R.
from dsl import *

# Nationalist outlook: trunk + Right-Wing Populism, Fascism, Monarchism (Military Junta lives in R_jun.py).

TRUNKS = [dict(
    outlook='R',
    title='The National Awakening',
    note='The nationalist camp chooses its street: mass patriotic leagues that mobilise and polarise, or the '
         'respectable veterans\' associations that bring discipline and the army\'s goodwill.',
    foci={
        'T0': F('champion_nationalist', 'Champion the National Awakening', [
            outlook('R', 0.05),
            timed('trunk_r_awakening', 730, {'nationalist_drift': 0.05, 'war_support_factor': 0.03}, 'The National Awakening'),
            ws(0.03),
        ], 'Nationalist movements gained ground around 1970, from Turkey\'s Nationalist Movement Party (1969) to the Rhodesian Front\'s republic (1970) and Perón\'s return to Argentina (1973).', old=True),
        'T1a': F('patriotic_leagues', 'Patriotic Leagues', [
            outlook('R', 0.04),
            timed('trunk_r_patriotic_leagues', 1095, {'conscription_factor': 0.03, 'war_support_factor': 0.03}, 'Patriotic Leagues'),
            fac('the_military', 5), ws(0.02), stab(-0.02),
        ], 'Mass leagues such as the Peronist Youth or Spain\'s Movimiento associations filled the streets with supporters, and with clashes.', old=True),
        'T1b': F('veterans_associations', "Veterans' Associations", [
            outlook('R', 0.03), xp('army', 25),
            timed('trunk_r_veterans', 1095, {'stability_factor': 0.02, 'army_morale_factor': 0.10}, "The Veterans' Code"),
            fac('the_military', 5), money(-0.005),
        ], 'Veterans\' bodies (the Spanish Hermandad de Alféreces, the Portuguese Liga dos Combatentes) lent nationalism respectability, at the price of their pensions.', old=True),
        'T2': F('the_nation_rises', 'The Nation Rises', [
            outlook('R', 0.05),
            timed('trunk_r_nation_rises', 1095, {'drift_defence_factor': 0.15, 'nationalist_drift': 0.03}, 'The Nation Rises'),
            outlook('W', -0.02), outlook('E', -0.02), stab(0.03),
        ], 'By the mid-1970s nationalists governed or shared power in Argentina, Rhodesia and Turkey (the 1975 Nationalist Front coalition), crowding out liberals and the left.', old=True),
        'T3': F('a_national_government', 'A National Government', [
            pp(100), stab(0.03),
            timed('trunk_r_national_mandate', 365, {'political_power_factor': 0.10, 'war_support_factor': 0.05}, 'A National Mandate'),
            note('With The Nation Rises: +50 political power'),
        ], 'A nationalist government arrives with a mandate to act quickly, as Perón did with his 62 % in September 1973.', old=True),
    },
)]

PARTIES = [
    # ================================================================ Right-Wing Populism
    dict(
        key='rwp',
        title='The People Against the Elites',
        identity='A leader speaks directly to the "little man" against parties, bankers and old families, and must decide '
                 'whether his base is the trade unions or the law-and-order middle class.',
        history='The populist right of the period came in two forms: labour populism with a social pact (Perón 1973-74) '
                'and middle-class revolts against taxes and bureaucracy (heirs of 1950s Poujadism, Glistrup\'s Progress Party 1973, '
                'George Wallace 1968/72); both promised national dignity, between the blocs or as a bulwark against communism.',
        foci={
            'E': F('rwp_the_people_s_champion', "The People's Champion", [
                prog('stability_factor', 0.03), prog('political_power_factor', 0.05), pop(0.05),
                fac('labour_unions', 5), fac('small_medium_business_owners', 5),
            ], 'Populists came to power on personal popularity as much as on party machines: Perón won 62 % on his return in 1973.', old=True),

            # ---------------- whose movement
            'POL': F('rwp_a_direct_line_to_the_people', 'A Direct Line to the People', [
                pp(75), pop(0.03), prog('political_power_factor', 0.05), outlook('W', -0.02), outlook('E', -0.02),
            ], 'Velasco Ibarra was president of Ecuador five times (1934-72), relying on radio speeches and rallies more than on any party.'),
            'A1': F('rwp_justice_for_the_workers', 'Justice for the Workers', [
                fac('labour_unions', 10), prog('stability_factor', 0.05), pop(0.03),
                prog('social_cost_multiplier_modifier', -0.05), prog('health_cost_multiplier_modifier', -0.05),
                law('increase_social_spending'), fac('wall_street', -10),
            ], 'Peronism rested on the CGT unions; social spending and union rights kept the base loyal and frightened investors.', old=True),
            'A2': F('rwp_the_silent_majority', 'The Silent Majority', [
                prog('drift_defence_factor', 0.15), prog('war_support_factor', 0.05), prog('mdcw_cw_ideological_defence', 0.10),
                pop(0.03), stab(0.02), fac('the_military', 5),
                fac('labour_unions', -10),
            ], 'George Wallace\'s campaigns and Nixon\'s 1969 "silent majority" speech courted the patriotic middle class against anti-war protesters and radicals.', old=True),
            'A1f': F('rwp_the_social_pact', 'The Social Pact', [
                idea('rwp_social_pact', {'consumer_goods_factor': -0.03, 'stability_factor': 0.05, 'productivity_growth_modifier': -0.05},
                     'The Social Pact', bound=True),
                fac('labour_unions', 10), fac('industrial_conglomerates', 5), stab(0.03),
            ], 'The Peronist government\'s 1973 Pacto Social froze prices and wages by agreement of the CGT unions and the CGE employers: inflation fell for a year, then the pact broke down in 1974-75.'),
            'A2f': F('rwp_against_the_old_elites', 'Against the Old Elites', [
                prog('political_power_factor', 0.10), corruption(-1), pop(0.04), money(0.005),
                fac('small_medium_business_owners', 10), fac('oligarchs', -15), fac('landowners', -5),
            ], 'Populists campaigned against "the establishment": anti-corruption purges and back-tax drives against the old families followed.', old=True),
            'PM': F('rwp_the_will_of_the_people', 'The Will of the People', [
                prog('political_power_factor', 0.05), stab(0.03), pop(0.03), fac('small_medium_business_owners', 5),
            ], 'Plebiscites and mass rallies rivalled parliament as a source of legitimacy, as in Perón\'s Plaza de Mayo addresses.'),

            # ---------------- who pays
            'ECO': F('rwp_prices_the_people_can_pay', 'Prices the People Can Pay', [
                prog('consumer_goods_factor', -0.03), stab(0.02), pop(0.02), fac('small_medium_business_owners', 5),
            ], 'Price controls on bread, fuel and rents were a common first measure of populist governments, as in Argentina in 1973.'),
            'B1': F('rwp_economic_nationalism', 'Economic Nationalism', [
                prog('production_speed_buildings_factor', 0.10), prog('imp_sanction_resistance', 0.10),
                fac('small_medium_business_owners', 10), fac('industrial_conglomerates', 5),
                prog('receiving_investment_cost_modifier', 0.10),
            ], 'Protection for national producers and limits on foreign capital (Argentina\'s 1973 foreign investment law) built at home but scared investors away.', old=True),
            'B2': F('rwp_the_taxpayers_revolt', "The Taxpayers' Revolt", [
                prog('bureaucracy_cost_multiplier_modifier', -0.15), prog('productivity_growth_modifier', 0.05),
                fac('small_medium_business_owners', 10), pop(0.03),
                prog('population_tax_income_multiplier_modifier', -0.05), law('decrease_social_spending'),
            ], 'Mogens Glistrup\'s Progress Party (Denmark 1973) won 16 % promising to abolish income tax and most of the bureaucracy.'),
            'B1f': F('rwp_buy_national', 'Buy National', [
                build('two_random_industrial_complex'), prog('industrial_capacity_factory', 0.05), fac('labour_unions', 5),
            ], 'State credit and "buy national" procurement grew domestic industry behind tariff walls, as across Latin America in the early 1970s.'),
            'B2f': F('rwp_abolish_the_paper_pushers', 'Abolish the Paper-Pushers', [
                idea('rwp_lean_state', {'bureaucracy_cost_multiplier_modifier': -0.10, 'production_speed_offices_factor': 0.10,
                                        'tax_gain_multiplier_modifier': -0.03}, 'The Lean State'),
                build('one_office_construction'), money(0.005), fac('small_medium_business_owners', 5),
            ], 'Glistrup famously proposed replacing Denmark\'s defence with an answering machine; his party demanded deep cuts in both state staff and taxes.'),
            'EM': F('rwp_prosperity_for_the_little_man', 'Prosperity for the Little Man', [
                growth(1), pop(0.03), prog('stability_factor', 0.02),
            ], 'Populism lived on visible results for ordinary families: jobs, cheap goods and a rising standard of living.'),

            # ---------------- the street
            'C1': F('rwp_the_law_and_order_ticket', 'The Law-and-Order Ticket', [
                prog('drift_defence_factor', 0.10), prog('stability_factor', 0.03), mdidea('idea_focus_generic_counter_terrorism'),
                fac('intelligence_community', 5), law('increase_policing_budget'), prog('police_cost_multiplier_modifier', 0.05),
            ], '"Law and order" was the theme of the Wallace and Nixon campaigns of 1968: more police, harder sentences, and a larger police bill.'),
            'C2': F('rwp_give_me_a_balcony', 'Give Me a Balcony', [
                pop(0.08), prog('political_power_factor', 0.05), prog('war_support_factor', 0.05), outlook('W', -0.03),
                fac('labour_unions', 5), prog('stability_factor', -0.02),
            ], '"Give me a balcony and I will be president," said Velasco Ibarra; charisma mobilised crowds but wore down institutions.'),
            'CM': F('rwp_a_movement_not_a_party', 'A Movement, Not a Party', [
                stab(0.04), prog('drift_defence_factor', 0.10), prog('mdcw_cw_ideological_defence', 0.10), pop(0.03), fac('all', 3),
            ], 'Peronism called itself a movement, not a party: unions, youth and women\'s branches all answered to the leader.'),

            # ---------------- national dignity abroad
            'D1': F('rwp_the_third_position', 'The Third Position', [
                prog('foreign_influence_defense_modifier', 0.15), prog('mdcw_cw_assistance_capacity', 1), tension(-1), pop(0.03),
                fac('industrial_conglomerates', 5), prog('trade_opinion_factor', -0.05),
            ], 'Perón\'s Tercera Posición - neither Washington nor Moscow - led Argentina to trade with the Eastern bloc and to grant Cuba a credit of 1.2 billion dollars for Argentine goods in 1973-74.'),
            'D2': F('rwp_bulwark_against_communism', 'Bulwark Against Communism', [
                tech(['CAT_small_arms', 'CAT_utility_vehicles'], 0.35, 2), prog('mdcw_cw_assistance_limit', 0.25),
                xp('army', 25), outlook('E', -0.03), fac('the_military', 5),
                prog('foreign_influence_defense_modifier', -0.05), tension(1),
            ], 'Turkey\'s Demirel and other anti-communist populists traded loyalty to the West for American aid and equipment.'),
            'DM': F('rwp_national_dignity', 'National Dignity', [
                xp('army', 50), prog('war_support_factor', 0.05), prog('army_morale_factor', 0.05), fac('the_military', 5),
            ], 'Populists promised the army respect and the nation pride, as Perón did in courting the armed forces after his 1973 return.'),

            'CAP': F('rwp_national_renewal', 'National Renewal', [
                idea('rwp_national_renewal', {'stability_factor': 0.05, 'political_power_factor': 0.10, 'nationalist_drift': 0.03,
                                              'productivity_growth_modifier': 0.05}, 'National Renewal', bound=True),
                pop(0.05), build('one_random_infrastructure'),
            ], 'At its height a populist government claimed to have renewed the nation itself, as Peronism did in its "Argentina Potencia" programme.', old=True),
        },
    ),

    # ================================================================ Fascism
    dict(
        key='fas',
        title='The New State',
        identity='A single-party state with corporatist institutions decides whether the party or the technocrats run it, '
                 'and whether the economy serves the corporations or the barracks.',
        history='The surviving authoritarian-nationalist regimes of the 1970s (Franco\'s Movimiento until 1975, Portugal\'s Estado Novo '
                'under Caetano until 1974, the Rhodesian Front) swung between the party "bunker" and Opus Dei technocrats, between '
                'corporatist syndicates and a war economy, and between censorship and a controlled opening to the West.',
        foci={
            'E': F('fas_the_national_revolution', 'The National Revolution', [
                prog('political_power_factor', 0.05), prog('drift_defence_factor', 0.15), ws(0.05), fac('the_military', 5),
            ], 'The regime presents itself as a national revolution against party politics and class war, as the Estado Novo did.', old=True),

            # ---------------- party or technocrats
            'POL': F('fas_the_single_party', 'The Single Party', [
                pp(100), prog('political_power_factor', 0.05), outlook('W', -0.03), outlook('E', -0.03),
            ], 'Spain\'s Movimiento Nacional and Portugal\'s União Nacional (Acção Nacional Popular from 1970) were the only legal parties.'),
            'A1': F('fas_the_party_above_the_state', 'The Party Above the State', [
                prog('drift_defence_factor', 0.15), prog('mdcw_cw_ideological_defence', 0.10),
                prog('party_popularity_stability_factor', 0.10), pop(0.05), fac('the_military', 5),
                prog('bureaucracy_cost_multiplier_modifier', 0.05),
            ], 'The Falangist "bunker" of 1973-75 insisted on the Movimiento\'s primacy over reformist ministers; ideology rose and administration slowed.'),
            'A2': F('fas_the_technocrats', 'The Technocrats', [
                prog('productivity_growth_modifier', 0.10), prog('research_speed_factor', 0.03),
                prog('production_factory_efficiency_gain_factor', 0.10),
                fac('industrial_conglomerates', 5), fac('international_bankers', 5),
                pop(-0.02), prog('drift_defence_factor', -0.05),
            ], 'From 1957 Franco handed the economy to Opus Dei technocrats (López Rodó, Ullastres); growth came, the old guard lost ground.'),
            'A1f': F('fas_national_youth_movement', 'National Youth Movement', [
                ws(0.05), prog('training_time_army_factor', -0.10), prog('conscription_factor', 0.03), pop(0.03),
            ], 'The Frente de Juventudes and the Mocidade Portuguesa organised youth in camps, parades and pre-military training.', old=True),
            'A2f': F('fas_the_development_plans', 'The Development Plans', [
                build('one_random_infrastructure'), build('one_random_industrial_complex'),
                prog('research_speed_factor', 0.02), prog('production_speed_buildings_factor', 0.05),
            ], 'Spain\'s three Development Plans (1964-75) steered investment into growth poles and infrastructure.'),
            'PM': F('fas_the_organic_law', 'The Organic Law of the State', [
                prog('stability_factor', 0.04), prog('bureaucracy_cost_multiplier_modifier', -0.05), stab(0.02),
            ], 'Spain\'s Organic Law of the State (1967) codified the regime\'s institutions so that it could outlive its founder.'),

            # ---------------- corporations or barracks
            'ECO': F('fas_the_national_economy', 'The National Economy', [
                prog('production_speed_buildings_factor', 0.05), prog('imp_sanction_resistance', 0.10),
            ], 'Isolated regimes learned to live with embargoes: Rhodesia withstood UN sanctions after 1966 through import substitution and trade via South Africa.'),
            'B1': F('fas_the_corporate_state', 'The Corporate State', [
                prog('production_speed_buildings_factor', 0.10), prog('stability_factor', 0.03),
                prog('industrial_capacity_factory', 0.03), fac('industrial_conglomerates', 10),
                fac('labour_unions', -20),
            ], 'The Estado Novo\'s corporations united employers and workers under state arbitration; strikes were banned.', old=True),
            'B2': F('fas_the_militarised_society', 'The Militarised Society', [
                prog('conscription_factor', 0.05), xp('army', 50), prog('military_factories_productivity', 0.10),
                prog('consumer_goods_factor', 0.03),
            ], 'Portugal spent around 40 % of its budget on the colonial wars (1961-74); four years of service became normal.', old=True),
            'B1f': F('fas_the_vertical_syndicates', 'The Vertical Syndicates', [
                build('two_random_industrial_complex'), fac('labour_unions', 10), prog('consumer_goods_factor', -0.02),
            ], 'Spain\'s compulsory Organización Sindical bound workers and owners into one syndicate per branch and enforced labour peace by law, until clandestine Workers\' Commissions spread in the 1960s.'),
            'B2f': F('fas_rearmament_programme', 'Rearmament Programme', [
                build('two_random_arms_factory'), fac('defense_industry', 10),
                tech(['CAT_small_arms', 'CAT_armored_fighting_vehicles'], 0.25, 2),
            ], 'Wartime regimes built their own arsenals: Portugal\'s Braço de Prata arsenal and Rhodesia\'s sanctions-era workshops armed the troops.', old=True),
            'EM': F('fas_a_nation_that_builds', 'A Nation That Builds', [
                growth(1), prog('industrial_capacity_factory', 0.03), fac('small_medium_business_owners', 5),
            ], 'Spain\'s "miracle" (1959-74) gave the regime its strongest argument: dams, factories and tourism instead of the hunger years.'),

            # ---------------- control or opening
            'C1': F('fas_the_censorship_board', 'The Censorship Board', [
                prog('drift_defence_factor', 0.15), prog('mdcw_cw_ideological_defence', 0.10), prog('stability_factor', 0.03),
                prog('foreign_influence_defense_modifier', 0.10), prog('research_speed_factor', -0.02),
            ], 'Prior censorship (Portugal\'s Exame Prévio, Spain before 1966) kept dissent out of print and much literature and scholarship with it.'),
            'C2': F('fas_the_controlled_opening', 'The Controlled Opening', [
                prog('research_speed_factor', 0.04), prog('trade_opinion_factor', 0.10), prog('receiving_investment_cost_modifier', -0.10),
                outlook('W', 0.03), stab(-0.02),
            ], 'Fraga\'s Press Law (1966) and Caetano\'s "evolution in continuity" opened the regime to Europe, and to its critics.'),
            'CM': F('fas_years_of_peace_and_order', 'Years of Peace and Order', [
                stab(0.05), prog('stability_factor', 0.04), pop(0.03), fac('the_clergy', 5),
            ], 'Spain\'s "25 Years of Peace" campaign (1964) presented order and stability as the regime\'s gift to a war-scarred generation.'),

            # ---------------- frontier or alliance
            'D1': F('fas_defend_the_frontier', 'Defend the Frontier', [
                xp('army', 50), prog('required_garrison_factor', -0.10), ws(0.05),
                mdidea('light_infantry_special_forces_idea'), money(-0.005),
            ], 'Portugal in Africa and the Rhodesian bush war (escalating from 1972) made counter-insurgency the army\'s school, and drained the treasury.'),
            'D2': F('fas_the_atlantic_bargain', 'The Atlantic Bargain', [
                tech(['CAT_aircraft', 'CAT_anti_air'], 0.35, 2), prog('mdcw_cw_assistance_limit', 0.25), money(0.005),
                xp('air', 25), prog('foreign_influence_defense_modifier', -0.05),
            ], 'Spain rented bases to the US (1953, renewed 1970) and Portugal kept the Azores in NATO: aid and arms for American influence.'),
            'DM': F('fas_a_professional_officer_corps', 'A Professional Officer Corps', [
                xp('army', 50), xp('air', 25), prog('army_org_factor', 0.03), prog('experience_gain_army_factor', 0.10),
            ], 'Staff colleges and NATO courses produced professional officers who later led or accepted the transitions in Portugal and Spain.'),

            'CAP': F('fas_the_greater_nation', 'The Greater Nation', [
                idea('fas_greater_nation', {'war_support_factor': 0.05, 'conscription_factor': 0.03, 'political_power_factor': 0.10,
                                            'stability_factor': 0.03, 'trade_opinion_factor': -0.05}, 'The Greater Nation', bound=True),
                timed('fas_heritage_of_the_nation', 365, {'conscription_factor': 0.03, 'stability_factor': 0.03}, 'The Heritage of the Nation'), pop(0.05), fac('the_military', 5),
                note('No forced war and no war goals: the spirit only raises recruitment and stability'),
            ], 'The regime\'s founding myth of national greatness, kept alive in parades and schoolbooks until its end in 1974-75.', old=True),
        },
    ),

    # ================================================================ Monarchism
    dict(
        key='mon',
        title='Crown and Nation',
        identity='The throne must decide whether it reigns through a constitution or rules itself, whether it modernises '
                 'from above or guards the royal patrimony - Ethiopia 1974 showed what happens to crowns that do neither.',
        history='1970s monarchies chose differently: Juan Carlos and Thailand\'s Bhumibol (1973) backed constitutions, Hassan II and '
                'Nepal\'s panchayat kept power with the king; Iran\'s White Revolution modernised from above while Morocco\'s Makhzen '
                'built a royal economy; the Green March (1975) and the Nixon Doctrine arms boom showed two roads to security.',
        foci={
            'E': F('mon_crown_and_nation', 'Crown and Nation', [
                prog('stability_factor', 0.05), prog('political_power_factor', 0.05), pop(0.03), fac('landowners', 5),
            ], 'Monarchies drew legitimacy from dynasty and nation alike, as Jordan\'s Hashemites and Morocco\'s Alaouites did.', old=True),

            # ---------------- reign or rule
            'POL': F('mon_the_royal_prerogative', 'The Royal Prerogative', [
                pp(100), prog('drift_defence_factor', 0.10), fac('the_military', 5),
            ], 'The kings of Morocco, Jordan and Nepal appointed and dismissed governments at will under their constitutions.'),
            'A1': F('mon_constitutional_monarchy', 'Constitutional Monarchy', [
                prog('stability_factor', 0.03), prog('research_speed_factor', 0.02), prog('trade_opinion_factor', 0.10),
                prog('foreign_influence_defense_modifier', 0.05), pop(0.03),
                prog('political_power_factor', -0.05), outlook('W', 0.03),
            ], 'Thailand\'s king backed the students and a new constitution in October 1973; Juan Carlos did the same in Spain after 1975.', old=True),
            'A2': F('mon_absolute_monarchy', 'Absolute Monarchy', [
                prog('political_power_factor', 0.10), prog('drift_defence_factor', 0.15), prog('political_power_factor', 0.07), prog('tax_gain_multiplier_modifier', 0.03), prog('bureaucracy_cost_multiplier_modifier', 0.02),
                fac('landowners', 5), fac('the_military', 5),
                outlook('W', -0.02), stab(-0.03),
            ], 'Hassan II\'s 1970 constitution and Nepal\'s panchayat kept power with the king - and Haile Selassie\'s refusal to share it ended in 1974.', old=True),
            'A1f': F('mon_the_crown_in_parliament', 'The Crown in Parliament', [
                idea('mon_crown_in_parliament', {'stability_factor': 0.05, 'foreign_influence_defense_modifier': 0.05,
                                                 'political_power_factor': -0.03}, 'The Crown in Parliament'),
                pop(0.04), prog('bureaucracy_cost_multiplier_modifier', -0.05), outlook('E', -0.03),
            ], 'Spain\'s Constitution of 1978 made the crown the guarantor of democracy and bound the army to it.'),
            'A2f': F('mon_the_royal_guard', 'The Royal Guard', [
                fac('the_military', 10), prog('army_core_defence_factor', 0.10), xp('army', 25),
                prog('intelligence_agency_defense', 0.15),
            ], 'After the coup attempts of Skhirat (1971) and the 1972 attack on his jet, Hassan II took personal command of the armed forces and tightened his palace security.', old=True),
            'PM': F('mon_the_kings_cabinet', "The King's Cabinet", [
                prog('political_power_factor', 0.05), prog('bureaucracy_cost_multiplier_modifier', -0.05), fac('all', 3), stab(0.02),
            ], 'Royal courts (Morocco\'s royal cabinet, Jordan\'s Royal Hashemite Court) worked beside the government and kept the notables in line.'),

            # ---------------- modernise or patrimony
            'ECO': F('mon_the_royal_economic_council', 'The Royal Economic Council', [
                prog('production_speed_buildings_factor', 0.05), prog('tax_gain_multiplier_modifier', 0.03),
                fac('landowners', 5), fac('industrial_conglomerates', 5),
            ], 'Planning bodies answering to the throne set the economic course above party politics, as Iran\'s Plan and Budget Organisation did under the Shah.'),
            'B1': F('mon_the_white_revolution', 'The White Revolution', [
                fac('farmers', 10), literacy(0.05), prog('agricolture_productivity_modifier', 0.08), pop(0.02),
                tech('CAT_agriculture', 0.35, 2),
                fac('landowners', -15), fac('the_clergy', -5),
            ], 'Iran\'s White Revolution (from 1963) gave land to peasants and sent a literacy corps to the villages; landlords and clergy turned against the Shah.'),
            'B2': F('mon_the_royal_patrimony', 'The Royal Patrimony', [
                prog('production_speed_buildings_factor', 0.05), prog('corporate_tax_income_multiplier_modifier', 0.08),
                fac('industrial_conglomerates', 10), fac('landowners', 5), money(0.01),
                corruption_chance(), prog('corruption_cost_factor', 0.10),
            ], 'Royal holdings and court favourites ran key businesses, from Iran\'s Pahlavi Foundation to Morocco\'s palace-linked firms: dependable, and dependent on patronage.'),
            'B1f': F('mon_royal_development_projects', 'Royal Development Projects', [
                build('two_random_agriculture_district'), build('one_random_infrastructure'), fac('farmers', 10),
            ], 'Thailand\'s royal development projects (from 1969) built dams, roads and model farms in the poorest provinces.', old=True),
            'B2f': F('mon_indigenise_the_economy', 'Indigenise the Economy', [
                money(0.01), build('two_office_construction'), fac('small_medium_business_owners', 10), fac('industrial_conglomerates', 5),
                fac('international_bankers', -5), prog('receiving_investment_cost_modifier', 0.05),
            ], 'Morocco\'s Moroccanisation decree (1973) forced foreign firms to sell majorities to nationals - many of them close to the palace.'),
            'EM': F('mon_the_crowns_prosperity', "The Crown's Prosperity", [
                growth(1), prog('stability_factor', 0.02), fac('small_medium_business_owners', 5),
            ], 'The oil and phosphate booms of 1973-74 let monarchies fund palaces, subsidies and loyal middle classes.'),

            # ---------------- faith or modern court
            'C1': F('mon_commander_of_the_faithful', 'Commander of the Faithful', [
                prog('stability_factor', 0.03), prog('drift_defence_factor', 0.15), prog('mdcw_cw_ideological_defence', 0.10),
                fac('the_clergy', 10), fac('the_ulema', 10),
                prog('research_speed_factor', -0.02),
            ], 'Hassan II ruled as Amir al-Mu\'minin and Thailand\'s king as patron of Buddhism: faith anchored the throne, not the laboratories.'),
            'C2': F('mon_the_modern_court', 'The Modern Court', [
                prog('research_speed_factor', 0.04), literacy(0.04), prog('trade_opinion_factor', 0.05), prog('productivity_growth_modifier', 0.05),
                fac('small_medium_business_owners', 5), fac('the_clergy', -10), fac('the_ulema', -5),
            ], 'The Shah\'s court pushed women\'s rights (Family Protection Law 1967) and Western education, and alienated the clergy.'),
            'CM': F('mon_the_royal_jubilee', 'The Royal Jubilee', [
                stab(0.05), pop(0.05), prog('war_support_factor', 0.03), prog('stability_factor', 0.02),
                prog('foreign_influence_modifier', 0.05), money(-0.005),
            ], 'The Persepolis celebrations of 1971 dazzled the world\'s leaders, and their cost was remembered at home.'),

            # ---------------- shield or cause
            'D1': F('mon_the_western_shield', 'The Western Shield', [
                tech(['CAT_aircraft', 'CAT_main_battle_tanks'], 0.35, 2), prog('mdcw_cw_assistance_limit', 0.25), xp('air', 50),
                prog('foreign_influence_defense_modifier', -0.05), outlook('W', 0.02),
            ], 'Under the Nixon Doctrine (1969-72) Iran and Saudi Arabia bought American jets and tanks as the Gulf\'s "twin pillars", and hosted American advisers.'),
            'D2': F('mon_the_national_cause', 'The National Cause', [
                pop(0.05), prog('war_support_factor', 0.05), prog('conscription_factor', 0.03), stab(0.03),
                outlook('E', -0.02), outlook('W', -0.02),
                tension(2), prog('trade_opinion_factor', -0.05),
            ], 'The Green March of 1975 rallied every Moroccan party behind the king on a national claim, and strained relations abroad.'),
            'DM': F('mon_the_royal_armed_forces', 'The Royal Armed Forces', [
                xp('army', 50), prog('army_morale_factor', 0.05), prog('experience_gain_army_factor', 0.10), fac('the_military', 5),
                build('one_air_base'),
            ], 'Royal armies were the throne\'s last line: Jordan\'s army, heir to the Arab Legion, decided the Black September conflict of 1970 in the king\'s favour.'),

            'CAP': F('mon_the_throne_endures', 'The Throne Endures', [
                idea('mon_throne_endures', {'stability_factor': 0.05, 'political_power_factor': 0.05, 'drift_defence_factor': 0.15,
                                            'defensive_war_stability_factor': 0.10}, 'The Throne Endures', bound=True),
                pop(0.03), fac('all', 5),
            ], 'Hussein survived Black September, Hassan two coups and Bhumibol 1973 - the monarchies that adapted outlasted the decade.', old=True),
        },
    ),
]
