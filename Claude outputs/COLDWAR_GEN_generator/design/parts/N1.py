# IMPERIA CW — Cold War: parts — N1.
from dsl import *

# Non-Aligned outlook trunk + Neutral Autocracy, Neutral Conservatism, Oligarchism.

TRUNKS = [dict(
    outlook='N',
    title='The Third Way',
    note='Champion the Non-Aligned outlook. The first step now forces a choice: carry neutrality abroad '
         '(Bandung diplomacy, aid from both blocs) or guard it at home (a neutral information order).',
    foci={
        'T0': F('champion_non_aligned', 'Champion the Third Way', [
            outlook('N', 0.05),
            timed('trunk_n_third_way', 730, {'neutrality_drift': 0.05, 'foreign_influence_defense_modifier': 0.10,
                                             'trade_opinion_factor': 0.05}, 'The Third Way'),
            stab(0.02),
        ], 'The Lusaka summit (1970), attended by more than fifty states, revived the movement founded by Tito, '
           'Nasser and Nehru and made its summits a regular forum for countries that refused to choose between the '
           'blocs.', old=True),
        'T1a': F('the_spirit_of_bandung', 'The Spirit of Bandung', [
            outlook('N', 0.03),
            timed('trunk_n_bandung', 730, {'foreign_influence_defense_modifier': 0.10, 'trade_opinion_factor': 0.10,
                                           'mdcw_cw_assistance_limit': 0.25, 'foreign_influence_modifier': 0.05},
                  'The Spirit of Bandung'),
            money(-0.005),
        ], 'Bandung (1955) and the Algiers summit (1973) made non-alignment a diplomacy of conferences and joint '
           'demands; delegations, embassies and summits cost money, while both blocs offered aid to win the members '
           'over.', old=True),
        'T1b': F('neutral_media', 'Neutral Media', [
            outlook('N', 0.03), stab(0.03),
            timed('trunk_n_neutral_media', 730, {'drift_defence_factor': 0.15, 'mdcw_cw_ideological_defence': 0.15,
                                                 'trade_opinion_factor': -0.05}, 'A Neutral Information Order'),
        ], 'The Non-Aligned News Agencies Pool (1975, coordinated by Tanjug) and the call for a New World Information '
           'Order sought to end dependence on Western news agencies; Western governments and press groups attacked it '
           'as a licence for state control.', old=True),
        'T2': F('the_nonaligned_majority', 'The Nonaligned Majority', [
            outlook('N', 0.05),
            timed('trunk_n_majority', 730, {'drift_defence_factor': 0.10, 'stability_factor': 0.03,
                                            'resource_export_multiplier_modifier': 0.10,
                                            'foreign_influence_modifier': 0.05}, 'The Nonaligned Majority'),
            outlook('W', -0.02), outlook('E', -0.02), fac('all', 3),
        ], 'By the mid-1970s non-aligned states held a majority in the UN General Assembly and, with the Group of 77, '
           'pushed through the 1974 declaration on a New International Economic Order over Western objections.', old=True),
        'T3': F('a_non_aligned_government', 'A Non-Aligned Government', [
            pp(75), stab(0.03),
            timed('trunk_n_mandate', 365, {'political_power_factor': 0.10, 'foreign_influence_defense_modifier': 0.10},
                  'A Non-Aligned Mandate'),
            note('Bonus with The Nonaligned Majority: +50 political power more.'),
        ], 'Yugoslavia, India and Indonesia turned non-alignment, and Finland and Austria neutrality, from a slogan '
           'into an organising principle of the state.', old=True),
    },
)]

PARTIES = [
    # ======================================================================== Neutral Autocracy
    dict(
        key='na',
        title='The Strongman Between the Blocs',
        identity='A strongman rules for himself rather than for a bloc: personality cult, patronage and a security service '
                 'at home, aid and arms from every side abroad.',
        history='Tito\'s personal rule against the institutionalised 1974 constitution and collective presidency; '
                'Franco\'s "organic democracy"; Mobutu\'s authenticité (1971) and Zairianisation (1973) against '
                'Suharto\'s IGGI-financed development; Indira Gandhi\'s Emergency (1975-77) against Indonesia\'s '
                'Pancasila courses; Tito, Mobutu and Ne Win buying arms from several suppliers across the blocs.',
        foci={
            'E': F('na_the_strongman', 'The Strongman', [
                prog('political_power_factor', 0.10), prog('stability_factor', 0.03),
                fac('the_military', 5), fac('intelligence_community', 5),
            ], 'Ne Win (1962), Mobutu (1965) and Suharto (1966-67) took power in non-aligned states and made their '
               'own office the only centre of power, backed by the army and the secret service.', old=True),

            # ---------------- how the strongman rules
            'POL': F('na_the_presidential_palace', 'The Presidential Palace', [
                pp(100), prog('drift_defence_factor', 0.10), fac('the_military', 5),
            ], 'Mobutu\'s single party (MPR, 1967) and Ne Win\'s Revolutionary Council (1962) concentrated every '
               'decision around the leader; ministers served at his pleasure.'),
            'A1': F('na_personal_rule', 'Personal Rule', [
                prog('political_power_factor', 0.10), prog('drift_defence_factor', 0.10),
                timed('na_cult_of_personality', 1095, {'war_support_factor': 0.05, 'party_popularity_stability_factor': 0.10},
                      'Cult of Personality'),
                corruption(1),
            ], 'Mobutu renamed the country Zaire (1971) and himself Mobutu Sese Seko (1972), and his image opened the '
               'television news; the cult bound the nation to one man, while the patronage behind it hollowed out the '
               'state.', old=True),
            'A2': F('na_institutionalise_the_regime', 'Institutionalise the Regime', [
                prog('stability_factor', 0.05), prog('bureaucracy_cost_multiplier_modifier', -0.10), fac('all', 3),
                prog('political_power_factor', -0.05),
            ], 'Yugoslavia\'s 1974 constitution set up a collective presidency and federal checks to take over after '
               'Tito; Franco\'s Organic Law of the State (1967) likewise laid down institutions meant to outlast him '
               'in Spain.', old=True),
            'A1f': F('na_the_secret_police', 'The Secret Police', [
                prog('drift_defence_factor', 0.15), prog('intelligence_agency_defense', 0.20),
                prog('intel_network_gain_factor', 0.20), fac('intelligence_community', 10),
                law('increase_policing_budget'), prog('research_speed_factor', -0.02),
            ], 'Yugoslavia\'s UDBA, Zaire\'s CND, Burma\'s Military Intelligence Service and Indonesia\'s Kopkamtib '
               'watched and detained opponents, and the UDBA also pursued émigrés abroad; student politics was '
               'curbed.', old=True),
            'A2f': F('na_organic_democracy', 'Organic Democracy', [
                stab(0.03), fac('all', 5),
                idea('na_corporate_chambers', {'stability_factor': 0.03, 'party_popularity_stability_factor': 0.05,
                                               'internal_factions_cost_factor': -0.10}, 'Corporate Chambers', bound=True),
                pop(0.03),
            ], 'Franco\'s Cortes were chosen through family, municipality and syndicate; Suharto\'s Golkar, which won '
               'the 1971 election, organised civil servants, farmers and workers as "functional groups" instead of '
               'parties.', old=True),
            'PM': F('na_the_single_movement', 'The Single Movement', [
                pop(0.05), outlook('W', -0.03), outlook('E', -0.03), prog('political_power_factor', 0.05), stab(0.02),
                fac('labour_unions', -5),
            ], 'Burma\'s 1974 one-party constitution, Zaire\'s MPR and Indonesia\'s Golkar folded unions, youth and '
               'women\'s groups into one regime movement, while the old parties were banned or, in Indonesia (1973), '
               'forced to merge.'),

            # ---------------- the presidential economy
            'ECO': F('na_the_presidential_economy', 'The Presidential Economy', [
                prog('production_speed_buildings_factor', 0.05), prog('tax_gain_multiplier_modifier', 0.03),
                fac('oligarchs', 5), fac('industrial_conglomerates', 5),
            ], 'Strongmen ran the economy through state firms answerable to the palace: Pertamina under Ibnu Sutowo, '
               'Gécamines in Zaire, the Burmese state corporations.'),
            'B1': F('na_take_over_foreign_firms', 'Take Over the Foreign Firms', [
                money(0.015), fac('oligarchs', 10), fac('small_medium_business_owners', 5),
                prog('foreign_influence_defense_modifier', 0.10), prog('receiving_investment_cost_modifier', 0.10),
            ], 'Zairianisation (1973) and Nigeria\'s Indigenisation Decree (1972) transferred foreign-owned firms or '
               'shares to nationals: a windfall for the regimes\' clients, but foreign investors grew wary.'),
            'B2': F('na_aid_from_both_blocs', 'Aid From Both Blocs', [
                prog('mdcw_cw_assistance_limit', 0.25), prog('receiving_investment_cost_modifier', -0.10),
                prog('trade_opinion_factor', 0.10), prog('interest_rate_multiplier_modifier', -0.5), debt(0.015),
            ], 'Suharto\'s IGGI consortium (1967) brought Western credit, while Tito drew IMF loans and Soviet trade '
               'at the same time; both regimes financed growth with borrowed money.'),
            'B1f': F('na_firms_for_the_loyal', 'Firms for the Loyal', [
                build('two_random_industrial_complex'), fac('oligarchs', 10), fac('the_military', 5),
                prog('industrial_capacity_factory', 0.05), prog('foreign_influence_defense_modifier', 0.05),
                corruption_chance(),
            ], 'In Zaire the "acquéreurs" of the zairianised firms were mostly politicians, officers and regime '
               'insiders; many businesses soon failed, and from 1976 part of them was handed back to the former '
               'owners.'),
            'B2f': F('na_the_development_consortium', 'The Development Consortium', [
                build('two_random_infrastructure'), build('one_random_industrial_complex'),
                prog('productivity_growth_modifier', 0.05),
            ], 'IGGI and World Bank credit financed Indonesia\'s Repelita plans from 1969: roads, ports, irrigation and '
               'fertiliser plants.'),
            'EM': F('na_the_presidential_fund', 'The Presidential Fund', [
                growth(1), prog('tax_gain_multiplier_modifier', 0.03), fac('industrial_conglomerates', 5),
            ], 'Indonesia\'s presidential instruction (Inpres) programmes, such as the primary-school drive of 1973, '
               'let the palace pay directly for schools, markets and clinics – and take the credit for them.'),

            # ---------------- order at home
            'C1': F('na_emergency_rule', 'Emergency Rule', [
                prog('drift_defence_factor', 0.15), prog('political_power_factor', 0.05),
                prog('mdcw_cw_ideological_defence', 0.10), stab(0.03),
                fac('the_military', 5), fac('intelligence_community', 5),
                prog('trade_opinion_factor', -0.05), outlook('W', 0.02),
            ], 'India\'s Emergency (1975-77) postponed elections and suspended civil liberties in the name of order; '
               'the jailed opposition united as the Janata Party and defeated the government in 1977.'),
            'C2': F('na_the_national_ideology', 'The National Ideology', [
                stab(0.04), literacy(0.03), prog('drift_defence_factor', 0.10),
                prog('party_popularity_stability_factor', 0.05), pop(0.03), money(-0.005),
            ], 'Indonesia\'s P4 courses (1978) made civil servants and students study Pancasila; Mobutism and the '
               '"Burmese Way to Socialism" were taught the same way.'),
            'CM': F('na_loyal_governors', 'Loyal Governors', [
                prog('stability_factor', 0.03), prog('required_garrison_factor', -0.10), fac('the_military', 5),
                prog('bureaucracy_cost_multiplier_modifier', -0.05), prog('tax_gain_multiplier_modifier', 0.03),
                law('increase_centralization'), pop(0.03),
            ], 'Strongmen put officers and loyalists in charge of the provinces: military governors in Suharto\'s '
               'Indonesia, Mobutu\'s appointed regional commissioners, Ne Win\'s Security and Administrative '
               'Committees.'),

            # ---------------- arms and allies
            'D1': F('na_playing_the_blocs', 'Playing the Blocs', [
                prog('mdcw_cw_assistance_limit', 0.25), tech(['CAT_aircraft', 'CAT_helicopters'], 0.35, 1),
                tension(-1), prog('trade_opinion_factor', 0.05), xp('air', 25),
                prog('foreign_influence_defense_modifier', -0.05),
            ], 'Yugoslavia flew American and then Soviet jets, and Mobutu was courted by Washington, Paris and '
               'Beijing at once: non-aligned strongmen took support from several sides and let foreign advisers in.'),
            'D2': F('na_the_presidential_guard', 'The Presidential Guard', [
                build('one_random_arms_factory'), tech(['CAT_small_arms', 'CAT_utility_vehicles'], 0.35, 1),
                prog('special_forces_cap', 0.10), xp('army', 50), money(-0.005),
            ], 'Mobutu\'s Division Spéciale Présidentielle (1985) and Syria\'s Defence Companies under Rifaat al-Assad '
               '(1971) were elite forces armed and paid by the regime, separate from the regular army.'),
            'DM': F('na_arms_from_every_supplier', 'Arms From Every Supplier', [
                xp('army', 50), xp('air', 25), tech(['CAT_armor', 'CAT_anti_air'], 0.35, 1),
                prog('army_personnel_cost_multiplier_modifier', -0.05), fac('the_military', 5),
            ], 'Yugoslavia and India flew Soviet MiG-21s alongside licence-built French helicopters (Gazelle, '
               'Alouette III) and used rival offers to bargain over price and licences.'),

            # ---------------- capstone
            'CAP': F('na_the_balancing_act', 'The Balancing Act', [
                idea('na_balancing_act', {'political_power_factor': 0.10, 'stability_factor': 0.05,
                                          'mdcw_cw_assistance_limit': 0.25, 'foreign_influence_defense_modifier': 0.10,
                                          'research_speed_factor': -0.02}, 'The Balancing Act', bound=True),
                tension(-1), fac('all', 3),
            ], 'Tito, a founder of the Non-Aligned Movement, took credits from both Washington and Moscow; Mobutu and '
               'Suharto stayed in power for over three decades by making themselves useful to outside patrons.', old=True),
        },
    ),

    # ======================================================================== Neutral Conservatism
    dict(
        key='ncon',
        title='The Armed Neutral',
        identity='A prosperous, armed and stable neutral state that keeps out of both blocs and lives from consensus, '
                 'hard money and trust.',
        history='Swiss and Swedish armed neutrality and total defence against Austrian and Finnish active neutrality '
                '(Helsinki CSCE 1975, Vienna UN City 1979); the Swiss low-tax model against Austria\'s social partnership; '
                'the Schwarzenbach initiative (1970) against Sweden\'s 1975 immigrant policy; Finland\'s and Austria\'s EEC '
                'free-trade treaties (1972-73) against Finland\'s clearing trade with the USSR.',
        foci={
            'E': F('ncon_conservative_neutrality', 'Conservative Neutrality', [
                prog('stability_factor', 0.03), prog('foreign_influence_defense_modifier', 0.10),
                fac('small_medium_business_owners', 5), fac('international_bankers', 5),
            ], 'Switzerland and, after the 1955 State Treaty, Austria made permanent neutrality the core of national '
               'identity and a foundation of their economic success.', old=True),

            # ---------------- the neutral doctrine
            'POL': F('ncon_the_consensus_cabinet', 'The Consensus Cabinet', [
                stab(0.03), prog('political_power_factor', 0.05), fac('all', 3), pp(50),
            ], 'Switzerland\'s "magic formula" (1959) gave all four large parties seats in the Federal Council: '
               'consensus at home matched neutrality abroad.'),
            'A1': F('ncon_total_defence', 'Total Defence', [
                prog('army_core_defence_factor', 0.10), prog('conscription_factor', 0.05), xp('army', 25),
                prog('army_personnel_cost_multiplier_modifier', 0.05),
            ], 'Sweden\'s totalförsvar and the Swiss militia army, planned to mobilise some 600,000 men within 48 '
               'hours, were meant to make an invasion too costly for either bloc.', old=True),
            'A2': F('ncon_the_neutral_mediator', 'The Neutral Mediator', [
                tension(-1), prog('political_power_factor', 0.05), prog('foreign_influence_modifier', 0.10),
                prog('trade_opinion_factor', 0.10), prog('war_support_factor', -0.03),
            ], 'Finland hosted the CSCE in Helsinki (1975), Austria built the UN City in Vienna (1979) and Switzerland '
               'offered its good offices: neutrality as a service both blocs needed.', old=True),
            'A1f': F('ncon_civil_defence_shelters', 'Civil Defence Shelters', [
                prog('production_speed_bunker_factor', 0.10), prog('production_speed_bunker_factor', 0.20),
                prog('defensive_war_stability_factor', 0.20), stab(0.02), money(-0.005),
            ], 'The Swiss shelter law of 1963 required shelters in new buildings, with the goal of a protected place '
               'for every resident; construction peaked in the mid-1970s at up to 400,000 places a year.', old=True),
            'A2f': F('ncon_a_neutral_banking_centre', 'A Neutral Banking Centre', [
                build('two_office_construction'), prog('return_on_investment_modifier', 0.005),
                prog('office_park_income_tax_modifier', 0.05), fac('international_bankers', 10),
                prog('corruption_cost_factor', 0.10),
            ], 'Banking secrecy (Swiss law of 1934) and neutrality made Zurich, Geneva and Vienna havens for capital '
               'from both blocs and the Third World, including flight capital and illicit funds.', old=True),
            'PM': F('ncon_credible_neutrality', 'Credible Neutrality', [
                prog('foreign_influence_defense_modifier', 0.05), stab(0.03), prog('drift_defence_factor', 0.10),
                fac('the_military', 5),
            ], 'Swedish and Swiss doctrine held that neutrality was only credible if it was armed and economically '
               'independent; both blocs had to believe it.'),

            # ---------------- the economic model
            'ECO': F('ncon_sound_money', 'Sound Money', [
                prog('interest_rate_multiplier_modifier', -0.5), prog('tax_gain_multiplier_modifier', 0.03),
                prog('return_on_investment_modifier', 0.005),
                fac('international_bankers', 5), fac('small_medium_business_owners', 5), money(0.005),
                fac('industrial_conglomerates', -5),
            ], 'The Swiss franc and the Austrian schilling (hard-currency policy from the 1970s) kept inflation below '
               'that of most of Western Europe through the oil shocks.'),
            'B1': F('ncon_the_low_tax_state', 'The Low-Tax State', [
                prog('productivity_growth_modifier', 0.10), prog('receiving_investment_cost_modifier', -0.10),
                prog('office_park_income_tax_modifier', 0.10), fac('small_medium_business_owners', 5),
                prog('tax_gain_multiplier_modifier', -0.05),
            ], 'Low-tax Swiss cantons such as Zug offered privileged rates to holding and domicile companies and drew '
               'in multinationals and commodity traders in the 1960s and 1970s.'),
            'B2': F('ncon_the_social_partners', 'The Social Partners', [
                prog('stability_factor', 0.04), fac('labour_unions', 10), fac('industrial_conglomerates', 10),
                prog('industrial_capacity_factory', 0.05), prog('social_cost_multiplier_modifier', 0.05),
            ], 'Austria\'s Parity Commission (1957) negotiated wages and prices, and the Swiss labour peace agreement '
               '(1937) replaced strikes with bargaining: almost no strikes in the 1970s, bought with costly social '
               'compromises.'),
            'B1f': F('ncon_holding_companies', 'Holding Companies and Trading Houses', [
                build('one_office_construction'), money(0.01), prog('corporate_tax_income_multiplier_modifier', 0.10),
                fac('wall_street', 10), prog('foreign_influence_defense_modifier', -0.05),
            ], 'Commodity traders and holding companies settled in low-tax neutral states in the 1970s (Marc Rich + '
               'Co. in Zug, 1974), paying their taxes there but bringing foreign interests with them.'),
            'B2f': F('ncon_precision_industry', 'Precision Industry', [
                build('two_random_industrial_complex'), tech('CAT_computing', 0.35, 1),
                fac('industrial_conglomerates', 5), prog('production_factory_max_efficiency_factor', 0.03),
            ], 'Swiss machine tools, Swedish engineering (ASEA, SKF) and Austria\'s VOEST thrived on stable wages and '
               'long-term planning.'),
            'EM': F('ncon_quiet_prosperity', 'Quiet Prosperity', [
                growth(1), stab(0.02), pop(0.03),
            ], 'Neutral Switzerland and Sweden had some of the highest incomes in Europe in the 1970s, and Austria '
               'was catching up fast.'),

            # ---------------- foreign workers
            'C1': F('ncon_limit_foreign_workers', 'Limit Foreign Workers', [
                law('increase_migration_law'), stab(0.03), prog('stability_factor', 0.03), pop(0.04),
                prog('party_popularity_stability_factor', 0.05),
                outlook('R', -0.03), prog('productivity_growth_modifier', -0.05),
            ], 'The Schwarzenbach initiative against "over-foreignisation" won 46 % of the vote in 1970; the Federal '
               'Council had capped foreign labour with national quotas that year, and employers had to recruit fewer '
               'workers.'),
            'C2': F('ncon_integrate_the_guest_workers', 'Integrate the Guest Workers', [
                law('decrease_migration_law'), prog('monthly_population', 0.05), prog('productivity_growth_modifier', 0.05),
                prog('buildings_worker_requirement_modifier', -0.05), prog('production_speed_buildings_factor', 0.05),
                fac('small_medium_business_owners', 5), fac('industrial_conglomerates', 5),
                stab(-0.02), outlook('R', 0.02),
            ], 'Sweden\'s 1975 immigrant policy gave foreign residents language courses and, from 1976, the vote in '
               'local elections; employers kept the labour they needed, and an anti-immigration group, Keep Sweden '
               'Swedish, formed in 1979.'),
            'CM': F('ncon_the_referendum_democracy', 'The Referendum Democracy', [
                stab(0.03), literacy(0.02), prog('drift_defence_factor', 0.10), fac('all', 3),
                prog('party_popularity_stability_factor', 0.05), pop(0.03),
            ], 'Swiss voters decided the big questions by referendum – women\'s suffrage in 1971, the foreign-worker '
               'initiatives – which bound every camp to the result.'),

            # ---------------- trade partners
            'D1': F('ncon_free_trade_with_the_community', 'Free Trade With the Community', [
                prog('trade_opinion_factor', 0.10), prog('productivity_growth_modifier', 0.05),
                prog('return_on_investment_modifier', 0.005), prog('receiving_investment_cost_modifier', -0.05),
                fac('industrial_conglomerates', 5), outlook('W', 0.02), prog('mdcw_cw_market_exposure', 0.05),
            ], 'Austria, Switzerland, Sweden and Finland signed free-trade agreements with the EEC in 1972-73 without '
               'joining it, and tied their markets to the West.'),
            'D2': F('ncon_clearing_trade_with_the_east', 'Clearing Trade With the East', [
                prog('imp_oil_price_resistance', 0.10), prog('imp_sanction_resistance', 0.10),
                build('one_random_dockyard'),
                prog('resource_export_multiplier_modifier', 0.05), fac('industrial_conglomerates', 5),
                outlook('E', 0.02), prog('foreign_influence_defense_modifier', -0.05),
            ], 'Finland\'s bilateral clearing trade with the USSR swapped ships and machinery for Soviet oil and cushioned '
               'the 1973 oil shock – at the price of Soviet influence ("Finlandisation").'),
            'DM': F('ncon_a_neutral_arms_industry', 'A Neutral Arms Industry', [
                build('one_random_arms_factory'), tech(['CAT_medium_aircraft', 'CAT_anti_air'], 0.35, 2),
                fac('defense_industry', 10), prog('military_industry_tax_modifier', 0.05),
            ], 'A neutral state could not rely on allied arsenals: Sweden built the Saab Viggen, Switzerland its own tanks '
               'and Oerlikon guns, Austria its Steyr vehicles.'),

            # ---------------- capstone
            'CAP': F('ncon_a_neutral_fortress', 'A Neutral Fortress', [
                idea('ncon_neutral_fortress', {'foreign_influence_defense_modifier': 0.15, 'drift_defence_factor': 0.15,
                                               'army_core_defence_factor': 0.10, 'stability_factor': 0.03,
                                               'personnel_cost_multiplier_modifier': 0.03}, 'A Neutral Fortress'),
                tension(-1), xp('army', 25),
            ], 'By the late 1970s Switzerland and Sweden were the models of armed neutrality: rich, stable, defended '
               'by the whole nation and taken seriously by both blocs.', old=True),
        },
    ),

    # ======================================================================== Oligarchism
    dict(
        key='oli',
        title='The Great Families',
        identity='A narrow circle of great families – landlords, merchant houses and their industrial heirs – runs the state '
                 'as a family business and buys peace with patronage.',
        history='Colombia\'s power-sharing National Front (1958-74) against the Somoza dynasty in Nicaragua; urban '
                'family conglomerates (Philippine and Lebanese clans) against the coffee, sugar and banana estates of '
                'Central America; the Philippine land reform of 1972 against El Salvador\'s ORDEN militias; '
                'Washington-backed regimes against merchant houses that traded with both blocs.',
        foci={
            'E': F('oli_rule_of_the_notables', 'Rule of the Notables', [
                prog('political_power_factor', 0.05), prog('stability_factor', 0.03),
                fac('oligarchs', 10), fac('landowners', 10),
            ], 'In much of Central America, in Lebanon and in the Philippines a few dozen landed and merchant '
               'families dominated 1970s politics through their own parties and networks of patrons.', old=True),

            # ---------------- who among the families rules
            'POL': F('oli_the_great_families', 'The Great Families', [
                pp(50), prog('drift_defence_factor', 0.10), fac('oligarchs', 5), stab(0.02),
            ], 'El Salvador\'s "fourteen families", the Somozas in Nicaragua, a handful of zu\'ama in Lebanon: politics was '
               'the business of a few houses.'),
            'A1': F('oli_the_pact_of_families', 'The Pact of Families', [
                stab(0.04), fac('all', 5), prog('stability_factor', 0.03),
                prog('internal_factions_cost_factor', -0.10), prog('political_power_factor', -0.05),
            ], 'Lebanon\'s National Pact (1943) divided offices among the confessional elites and Colombia\'s Sitges '
               'agreement (1957) between the two traditional parties: peace among the notables, but every decision '
               'needed all of them.'),
            'A2': F('oli_the_ruling_dynasty', 'The Ruling Dynasty', [
                prog('political_power_factor', 0.10), fac('oligarchs', 10), fac('the_military', 10),
                prog('drift_defence_factor', 0.15), corruption_chance(),
            ], 'The Somozas ruled Nicaragua from 1936 to 1979 like a family firm: one house held the presidency, the '
               'National Guard and a large share of the country\'s land and industry.'),
            'A1f': F('oli_alternating_presidency', 'Alternating Presidency', [
                stab(0.03),
                idea('oli_power_sharing', {'stability_factor': 0.04, 'party_popularity_stability_factor': 0.05,
                                           'political_power_factor': 0.05, 'bureaucracy_cost_multiplier_modifier': 0.05},
                     'The Power-Sharing Pact', bound=True),
                pop(0.03), outlook('W', -0.02),
            ], 'Colombia\'s National Front (1958-74) alternated the presidency between Liberals and Conservatives and '
               'split every office between them: it ended the partisan Violencia, but shut out other movements, some '
               'of which took up arms.'),
            'A2f': F('oli_the_family_guard', 'The Family Guard', [
                fac('the_military', 10), prog('drift_defence_factor', 0.15), prog('required_garrison_factor', -0.10),
                xp('army', 25), prog('political_power_factor', 0.05), law('increase_military_spending'),
            ], 'Nicaragua\'s Guardia Nacional was commanded by the Somoza family itself and served the dynasty rather than '
               'the state.'),
            'PM': F('oli_the_club_of_notables', 'The Club of Notables', [
                pp(75), fac('oligarchs', 5), fac('landowners', 5), prog('bureaucracy_cost_multiplier_modifier', -0.05),
            ], 'In El Salvador the coffee growers\' associations and in Argentina the landowners\' Sociedad Rural '
               'shaped economic policy, often more than parliament did.'),

            # ---------------- where the fortune comes from
            'ECO': F('oli_the_merchant_houses', 'The Merchant Houses', [
                prog('tax_gain_multiplier_modifier', 0.03), prog('trade_opinion_factor', 0.05),
                prog('resource_export_multiplier_modifier', 0.05),
                fac('small_medium_business_owners', 5), fac('oligarchs', 5),
            ], 'A few trading families controlled imports, exports and banking in the Gulf, Lebanon and Central '
               'America, and governments depended on their goodwill.'),
            'B1': F('oli_crony_capitalism', 'Crony Capitalism', [
                prog('production_speed_buildings_factor', 0.10), prog('industrial_capacity_factory', 0.05),
                fac('oligarchs', 10), fac('industrial_conglomerates', 5), corruption(1),
            ], 'In Marcos\'s Philippines state contracts, cheap credit and trading monopolies went to presidential '
               'cronies such as Eduardo Cojuangco (coconuts, later San Miguel beer) and Roberto Benedicto (sugar).', old=True),
            'B2': F('oli_the_landed_interest', 'The Landed Interest', [
                prog('agriculture_tax_modifier', 0.10), prog('agricolture_productivity_modifier', 0.10),
                prog('resource_export_multiplier_modifier', 0.05), fac('landowners', 10), fac('farmers', -10),
            ], 'Coffee, sugar and cotton planters dominated Central American states; export taxes on the estates '
               'funded the state, while landless peasants worked them for low wages.', old=True),
            'B1f': F('oli_the_family_firms', 'The Family Firms', [
                build('two_random_industrial_complex'), fac('industrial_conglomerates', 5),
                prog('corporate_tax_income_multiplier_modifier', 0.05), prog('office_park_income_tax_modifier', 0.05),
            ], 'The Somozas, the Philippine Ayala and Lopez clans and Lebanese merchant houses turned land and trade '
               'fortunes into banks, utilities, property and industry.', old=True),
            'B2f': F('oli_plantation_exports', 'Plantation Exports', [
                build('two_random_agriculture_district'), prog('resource_export_multiplier_modifier', 0.05),
                prog('agriculture_tax_modifier', 0.05), fac('landowners', 5),
            ], 'Coffee, bananas, cotton and sugar earned most of Central America\'s export income in the 1970s, as '
               'sugar and coconut products did much of the Philippines\'; the estate owners carried decisive political '
               'weight.', old=True),
            'EM': F('oli_the_commodity_boom', 'The Commodity Boom', [
                money(0.01), growth(1), fac('landowners', 5), fac('labour_unions', -5),
            ], 'The commodity boom of 1973-77 (sugar in 1974, coffee in 1976) filled the treasuries of the oligarchic '
               'states – for a while.'),

            # ---------------- the countryside
            'C1': F('oli_a_controlled_land_reform', 'A Controlled Land Reform', [
                stab(0.03), prog('stability_factor', 0.03), fac('farmers', 10), outlook('E', -0.03),
                prog('agricolture_productivity_modifier', 0.05), fac('landowners', -10),
            ], 'The Philippine land reform of 1972 (PD 27) covered only tenanted rice and corn land and spared the '
               'sugar and coconut estates: it gave some tenants land and angered the rice and corn landlords.'),
            'C2': F('oli_the_rural_militias', 'The Rural Militias', [
                prog('drift_defence_factor', 0.15), prog('required_garrison_factor', -0.15), fac('landowners', 10),
                prog('conscription_factor', 0.02), prog('intel_network_gain_factor', 0.10), stab(-0.03),
            ], 'El Salvador\'s ORDEN and the Philippine Civilian Home Defence Forces (1976) armed loyal villagers '
               'against peasant organisers and rebels; their abuses fed the insurgencies that followed.'),
            'CM': F('oli_patrons_and_clients', 'Patrons and Clients', [
                stab(0.03), pop(0.04), fac('all', 3), prog('party_popularity_stability_factor', 0.05),
                prog('stability_factor', 0.02),
            ], 'In Lebanon, the Philippines and Central America oligarchic rule rested on clientelism: the patron '
               'found jobs, loans and doctors for his clients, and they voted as he told them.'),

            # ---------------- friends abroad
            'D1': F('oli_friends_in_washington', 'Friends in Washington', [
                prog('mdcw_cw_assistance_limit', 0.25), tech(['CAT_small_arms', 'CAT_helicopters'], 0.35, 1),
                prog('receiving_investment_cost_modifier', -0.10), xp('army', 25),
                prog('foreign_influence_defense_modifier', -0.05),
            ], 'The Somozas and Central American planters relied on American aid, investors and the embassy\'s goodwill; '
               'the embassy expected to be heard in return.'),
            'D2': F('oli_trade_with_all_comers', 'Trade With All Comers', [
                prog('trade_opinion_factor', 0.10), prog('resource_export_multiplier_modifier', 0.05),
                prog('imp_sanction_resistance', 0.10), fac('oligarchs', 5), prog('mdcw_cw_market_exposure', 0.05),
            ], 'Merchant oligarchies sold to whoever paid: Argentine grain went to the USSR during the 1980 US embargo, '
               'Lebanese and Gulf houses traded with both blocs.'),
            'DM': F('oli_offshore_fortunes', 'Offshore Fortunes', [
                build('one_office_construction'), prog('return_on_investment_modifier', 0.005), fac('international_bankers', 10),
                prog('interest_rate_multiplier_modifier', -0.5), fac('oligarchs', 5),
            ], 'Oligarch families kept their fortunes in Miami, Geneva and Panama; the connections brought foreign banks '
               'and cheap credit home.'),

            # ---------------- capstone
            'CAP': F('oli_the_oligarchic_order', 'The Oligarchic Order', [
                idea('oli_oligarchic_order', {'stability_factor': 0.05, 'political_power_factor': 0.10,
                                              'corporate_tax_income_multiplier_modifier': 0.10, 'agriculture_tax_modifier': 0.10,
                                              'productivity_growth_modifier': -0.05}, 'The Oligarchic Order', bound=True),
                fac('oligarchs', 10), fac('labour_unions', -10),
            ], 'At its height the oligarchic order looked unshakeable: the families held the land, the banks, the '
               'army and the vote – until the Sandinista revolution in Nicaragua and the coup and civil war in El '
               'Salvador (1979-80).', old=True),
        },
    ),
]
