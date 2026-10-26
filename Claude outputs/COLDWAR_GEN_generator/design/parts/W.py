# IMPERIA CW — Cold War: parts — W.
from dsl import *

# Western outlook: trunk + Western Autocracy, Conservatism, Liberalism, Social Democracy.

TRUNKS = [dict(
    outlook='W',
    title='The Western Cause',
    note='Civic Associations and A Free Press are now a choice (OR into The Democratic Majority); timed spirits replace the small PP and popularity crumbs.',
    foci={
        'T0': F('champion_western', 'Champion the Western Cause', [
            outlook('W', 0.05),
            timed('trunk_w_atlantic_values', 1095, {'democratic_drift': 0.05, 'trade_opinion_factor': 0.10}, 'Atlantic Values'),
            fac('international_bankers', 5), fac('communist_cadres', -5),
        ], 'Parties that looked West in the 1970s sold membership of the prosperous "free world": Marshall-era trade, American credit and the European example.', old=True),
        'T1a': F('civic_associations', 'Civic Associations', [
            outlook('W', 0.03), stab(0.03), fac('small_medium_business_owners', 10), fac('the_clergy', 5),
            timed('trunk_w_civil_society', 730, {'stability_factor': 0.03, 'party_popularity_stability_factor': 0.05}, 'A Civil Society'),
            fac('labour_unions', -5), money(-0.005),
        ], 'Chambers of commerce and church lay groups carried Christian Democracy, and personal support groups (koenkai) carried Japan\'s LDP politicians; they bring calm and a base, but cost subsidies.', old=True),
        'T1b': F('a_free_press', 'A Free Press', [
            outlook('W', 0.05),
            timed('trunk_w_free_press', 1095,{'research_speed_factor': 0.03, 'democratic_drift': 0.03, 'foreign_influence_defense_modifier': 0.10}, 'A Free Press'),
            fac('intelligence_community', -5), stab(-0.01),
        ], 'Watergate (1972-74) and the Pentagon Papers (1971) showed what an independent press could do: it spreads Western ideas fast and also exposes the government.', old=True),
        'T2': F('the_democratic_majority', 'The Democratic Majority', [
            outlook('W', 0.05), stab(0.02), outlook('E', -0.02),
            timed('trunk_w_democratic_majority', 1095,{'drift_defence_factor': 0.15, 'party_popularity_stability_factor': 0.10}, 'A Democratic Majority'),
        ], 'Portugal (1975-76) and Spain (1977) turned a democratic majority in the streets into a majority at the ballot box that the extremes could not overturn.', old=True),
        'T3': F('a_western_government', 'A Western Government', [
            pp(100), stab(0.03),
            timed('trunk_w_new_mandate', 365, {'political_power_factor': 0.10, 'bureaucracy_cost_multiplier_modifier': -0.05}, 'A New Mandate'),
            note('With The Democratic Majority completed: a further +50 political power.'),
        ], 'A new Western-oriented government arrives with a mandate: Brandt in 1969, Whitlam in 1972 and Suárez in 1977 all used their first year to push their programme.', old=True),
    },
)]

PARTIES = [
    # ======================================================================== Western Autocracy
    dict(
        key='wa',
        title='The Developmental State',
        identity='An anti-communist strongman trades political freedom for growth: technocrats plan, the security services guard, '
                 'and the alliance with Washington pays for loyalty.',
        history='Asia and the Middle East offered the models: martial law (Marcos 1972) against managed elections and a new '
                'constitution (Park\'s Yushin 1972, Suharto\'s Golkar elections); export-led growth (Taiwan\'s and Korea\'s free '
                'export zones) against the heavy-industry drive (Korea\'s HCI plan 1973, Iran\'s steel); village development '
                '(Saemaul Undong 1970) against anti-communist mobilisation; the US alliance against self-reliant defence.',
        foci={
            'E': F('wa_the_developmental_strongman', 'The Developmental Strongman', [
                prog('political_power_factor', 0.10), prog('stability_factor', 0.03),
                fac('the_military', 10), fac('industrial_conglomerates', 5),
            ], 'Park Chung-hee, Suharto and the Shah justified personal rule by development: the leader stands above parties and answers for growth.', old=True),

            # ---------------- power question
            'POL': F('wa_rule_from_the_palace', 'Rule from the Palace', [
                pp(100), prog('drift_defence_factor', 0.10), fac('intelligence_community', 10),
            ], 'Decisions moved from parliament to the palace: Park\'s Blue House secretariat, Marcos in Malacañang and the Shah\'s court ran the state directly.'),
            'A1': F('wa_martial_law', 'Martial Law', [
                prog('drift_defence_factor', 0.15), prog('stability_factor', 0.04), stab(0.03),
                prog('required_garrison_factor', -0.10),
                prog('research_speed_factor', -0.02), law('increase_policing_budget'),
            ], 'Marcos proclaimed martial law in September 1972 (Proclamation 1081), closed Congress and the newspapers: calm streets, empty campuses, a growing constabulary.', old=True),
            'A2': F('wa_controlled_elections', 'Controlled Elections', [
                pop(0.05), prog('stability_factor', 0.03), prog('party_popularity_stability_factor', 0.10),
                prog('trade_opinion_factor', 0.10),
                prog('political_power_factor', -0.05), money(-0.005),
            ], 'Suharto\'s New Order won managed elections through Golkar (1971, 1977); the mandate on paper reassured donors, but patronage and campaign money had to be paid.', old=True),
            'A1f': F('wa_silence_the_opposition', 'Silence the Opposition', [
                outlook('E', -0.05), outlook('N', -0.03), prog('mdcw_cw_ideological_defence', 0.10),
                prog('intelligence_agency_defense', 0.15), prog('intel_network_gain_factor', 0.10),
                prog('encryption_factor', 0.10), prog('decryption_factor', 0.10),
                fac('intelligence_community', 10), corruption_chance(),
            ], 'The KCIA abducted Kim Dae-jung from Tokyo (1973) and the Emergency Decrees made criticism of the constitution a crime; the opposition was driven underground.', old=True),
            'A2f': F('wa_a_new_constitution', 'A New Constitution', [
                idea('wa_presidential_constitution', {'political_power_factor': 0.10, 'stability_factor': 0.03,
                                                      'bureaucracy_cost_multiplier_modifier': -0.05}, 'The Presidential Constitution', bound=True),
                stab(0.03),
            ], 'Korea\'s Yushin Constitution (1972) kept elections, but the president was chosen by the National Conference for Unification, a non-party body he chaired, and nominated a third of the Assembly: legality and an assured majority at once.', old=True),
            'PM': F('wa_a_mandate_for_growth', 'A Mandate for Growth', [
                prog('political_power_factor', 0.05), prog('production_speed_buildings_factor', 0.05),
                fac('the_military', 5), fac('industrial_conglomerates', 5),
            ], '"Economy first" was the official answer to every demand for freedom: Park and Suharto legitimised their rule through growth figures.'),

            # ---------------- economic model
            'ECO': F('wa_the_economic_planning_board', 'The Economic Planning Board', [
                prog('production_speed_buildings_factor', 0.05), prog('tax_gain_multiplier_modifier', 0.03),
                fac('industrial_conglomerates', 5), fac('chaebols', 5),
            ], 'Korea\'s Economic Planning Board, Taiwan\'s CEPD and Indonesia\'s Bappenas gave a small team of technocrats direct access to the ruler.'),
            'B1': F('wa_exports_first', 'Exports First', [
                prog('trade_opinion_factor', 0.10), prog('office_park_income_tax_modifier', 0.10),
                prog('productivity_growth_modifier', 0.10), fac('chaebols', 10),
                prog('mdcw_cw_market_exposure', 0.10),
            ], 'Korea and Taiwan tied credit and tax breaks to export performance, and Park reviewed the targets at monthly export promotion meetings; growth followed world demand - in both directions.'),
            'B2': F('wa_the_heavy_industry_drive', 'The Heavy Industry Drive', [
                prog('industrial_capacity_factory', 0.10), prog('production_speed_industrial_complex_factor', 0.10),
                fac('industrial_conglomerates', 10), fac('defense_industry', 5),
                debt(0.02),
            ], 'Korea\'s Heavy and Chemical Industry plan (1973), financed largely with foreign loans, and the Shah\'s oil-funded steel and petrochemical projects built heavy industry at speed.'),
            'B1f': F('wa_free_export_zones', 'Free Export Zones', [
                build('two_office_construction'), prog('receiving_investment_cost_modifier', -0.10), money(0.005),
                fac('labour_unions', -5),
            ], 'The Kaohsiung (1966) and Masan (1970) free export zones drew foreign assembly plants with tax holidays and cheap labour.'),
            'B2f': F('wa_steel_mills_and_shipyards', 'Steel Mills and Shipyards', [
                build('two_random_industrial_complex'), build('one_random_dockyard'),
                prog('industrial_capacity_dockyard', 0.10), fac('chaebols', 5),
                prog('consumer_goods_factor', 0.02),
            ], 'POSCO\'s Pohang steelworks (1973) and the Hyundai shipyard at Ulsan (1974) were built by state order, cheap credit and suppressed consumption.'),
            'EM': F('wa_the_developmental_miracle', 'The Developmental Miracle', [
                growth(1), stab(0.03), fac('industrial_conglomerates', 5),
            ], 'Double-digit growth became the regime\'s claim to rule: Korea grew about 10 % a year in the 1970s, Taiwan and Indonesia not far behind.'),

            # ---------------- society and security
            'C1': F('wa_the_new_village_movement', 'The New Village Movement', [
                build('one_random_agriculture_district'), build('one_random_infrastructure'),
                prog('agricolture_productivity_modifier', 0.05), fac('farmers', 10),
                money(-0.005),
            ], 'Korea\'s Saemaul Undong (1970) gave villages cement and steel for roads, roofs and irrigation, and tied the countryside to the president.'),
            'C2': F('wa_anti_communist_mobilisation', 'Anti-Communist Mobilisation', [
                prog('conscription_factor', 0.04), prog('war_support_factor', 0.05),
                prog('mdcw_cw_ideological_defence', 0.10), xp('army', 25),
                stab(-0.02),
            ], 'Korea\'s Homeland Reserve Forces (1968) and Taiwan\'s mobilisation laws put millions of citizens in reserve units and anti-communist drills.'),
            'CM': F('wa_discipline_and_diligence', 'Discipline and Diligence', [
                prog('stability_factor', 0.03), prog('productivity_growth_modifier', 0.05), stab(0.03), pop(0.03),
                prog('consumer_goods_factor', -0.02),
            ], 'National education charters, morning drills and anti-luxury campaigns preached hard work and order as patriotic duties.'),

            # ---------------- alliance and arms
            'D1': F('wa_the_treaty_ally', 'The Treaty Ally', [
                tech(['CAT_aircraft', 'CAT_armor'], 0.35, 2), prog('mdcw_cw_assistance_limit', 0.25), xp('army', 50),
                prog('foreign_influence_defense_modifier', -0.05),
            ], 'Korea rotated some 320,000 troops through Vietnam (1964-73) and received American aid, weapons and procurement contracts in return - and American advice with them.'),
            'D2': F('wa_self_reliant_defence', 'Self-Reliant Defence', [
                build('one_random_arms_factory'), tech(['CAT_small_arms', 'CAT_towed_artillery'], 0.35, 2),
                fac('defense_industry', 10), prog('production_speed_arms_factory_factor', 0.05),
                money(-0.005),
            ], 'After the Nixon Doctrine (1969) and the US troop cuts, Korea\'s Yulgok plan (1974) and Taiwan built their own arms industries at their own expense.'),
            'DM': F('wa_the_defence_build_up', 'The Defence Build-Up', [
                xp('army', 50), xp('air', 25), prog('army_org_factor', 0.03), prog('military_factories_productivity', 0.05),
            ], 'Iran became the largest buyer of American arms in the 1970s and Korea levied a special defence tax (1975) to pay for its build-up: the strongman\'s army was his showcase.'),

            # ---------------- capstone
            'CAP': F('wa_developmental_dictatorship', 'Developmental Dictatorship', [
                idea('wa_developmental_state', {'production_speed_buildings_factor': 0.10, 'industrial_capacity_factory': 0.05,
                                                'political_power_factor': 0.05, 'stability_factor': 0.03,
                                                'research_speed_factor': -0.02}, 'The Developmental State', bound=True),
                build('two_random_industrial_complex'), fac('industrial_conglomerates', 10),
            ], 'At its height the developmental dictatorship fused party, planners and conglomerates into one machine for growth, as in Korea under Yushin or Taiwan in the 1970s.', old=True),
        },
    ),

    # ======================================================================== Conservatism
    dict(
        key='con',
        title='Order and Property',
        identity='A centre-right government of order, property and sound money that must decide whether conservatism means '
                 'the market or the nation\'s social peace.',
        history='The 1970s centre right split between a strong executive (Gaullism, Pompidou) and broad coalitions (CDU/CSU, '
                'Japan\'s LDP factions); between the Selsdon market programme and Heath\'s 1972 U-turn to incomes policy and '
                'One Nation welfare; between family-and-faith conservatism (Italy\'s 1974 divorce referendum) and modernisers '
                '(Giscard\'s 1974-75 reforms); between Atlantic loyalty and Gaullist independence.',
        foci={
            'E': F('con_a_conservative_government', 'A Conservative Government', [
                prog('stability_factor', 0.03), prog('political_power_factor', 0.05), prog('drift_defence_factor', 0.10),
                fac('wall_street', 5), fac('small_medium_business_owners', 5),
            ], 'Conservative governments promised competence rather than ideology: Heath announced a "quiet revolution" in 1970, while Pompidou (1969) and Fukuda (1976) presented themselves as sound managers.', old=True),

            # ---------------- how to rule
            'POL': F('con_the_party_of_government', 'The Party of Government', [
                pp(75), prog('party_popularity_stability_factor', 0.10), fac('the_clergy', 5),
            ], 'Christian Democrats in Italy and Germany and the LDP in Japan saw themselves as the natural party of government, rooted in church, business and countryside.'),
            'A1': F('con_a_strong_executive', 'A Strong Executive', [
                prog('political_power_factor', 0.10), prog('bureaucracy_cost_multiplier_modifier', -0.05),
                prog('drift_defence_factor', 0.10), stab(0.03),
                pop(-0.02), fac('labour_unions', -5),
            ], 'Gaullism concentrated power in the presidency and governed by decree and referendum; effective, but it alienated parliament and the unions.'),
            'A2': F('con_the_broad_church', 'The Broad Church', [
                stab(0.04), prog('stability_factor', 0.03), fac('all', 5), pop(0.05),
                prog('political_power_factor', -0.05),
            ], 'The CDU/CSU union and the LDP\'s factions held liberals, farmers, Catholics and business together - at the price of endless bargaining.'),
            'A1f': F('con_appeal_to_the_nation', 'Appeal to the Nation', [
                idea('con_presidential_authority', {'political_power_factor': 0.05, 'stability_factor': 0.03,
                                                    'drift_defence_factor': 0.10}, 'Presidential Authority', bound=True),
                pop(0.05), outlook('E', -0.03),
            ], 'De Gaulle and Pompidou went over the heads of the parties with referendums (1969, 1972) and television addresses to the nation.'),
            'A2f': F('con_the_coalition_agreement', 'The Coalition Agreement', [
                prog('party_popularity_stability_factor', 0.10), prog('internal_factions_cost_factor', -0.20),
                stab(0.03), fac('all', 5),
            ], 'West Germany\'s written coalition agreements (the first in 1961) and the LDP\'s factional quotas for cabinet posts kept multi-party and multi-faction governments together for years at a time.'),
            'PM': F('con_law_and_order', 'Law and Order', [
                prog('drift_defence_factor', 0.10), prog('police_cost_multiplier_modifier', -0.10),
                stab(0.02), fac('the_military', 5),
            ], 'Facing terrorism and strikes, conservatives ran on law and order: Nixon in 1968 and 1972, and the West German CDU/CSU, which pressed for ever tougher anti-terror laws in the 1970s.', old=True),

            # ---------------- economic model
            'ECO': F('con_the_spending_review', 'The Spending Review', [
                prog('bureaucracy_cost_multiplier_modifier', -0.10), prog('tax_gain_multiplier_modifier', 0.03),
                money(0.005), fac('wall_street', 5), fac('small_medium_business_owners', 5),
                fac('labour_unions', -5),
            ], 'Heath\'s 1970 White Paper on central government merged ministries into giant departments, and Barber\'s October 1970 package cut public spending to pay for lower income tax.'),
            'B1': F('con_fiscal_discipline', 'Fiscal Discipline', [
                prog('bureaucracy_cost_multiplier_modifier', -0.10), prog('interest_rate_multiplier_modifier', -0.5),
                prog('receiving_investment_cost_modifier', -0.10), fac('wall_street', 10),
                law('decrease_social_spending'), fac('labour_unions', -10),
            ], 'The Selsdon programme (1970) promised to end subsidies to "lame duck" industries and cut public spending; the unions answered with strikes.', old=True),
            'B2': F('con_one_nation_conservatism', 'One-Nation Conservatism', [
                prog('stability_factor', 0.04), prog('social_cost_multiplier_modifier', -0.05), prog('health_cost_multiplier_modifier', -0.05), fac('labour_unions', 10),
                stab(0.02), money(-0.005),
            ], 'Heath nationalised the bankrupt Rolls-Royce (1971), then in his 1972 U-turn rescued Upper Clyde Shipbuilders and brought in an incomes policy to buy social peace.', old=True),
            'B1f': F('con_balance_the_budget', 'Balance the Budget', [
                prog('interest_rate_multiplier_modifier', -0.5), money(0.01), prog('tax_gain_multiplier_modifier', 0.05),
                fac('international_bankers', 10), fac('labour_unions', -5),
            ], 'Sound money as a programme: the Bundesbank\'s stability course and Fukuda\'s tight budget policy against the "crazy prices" of 1974 won the trust of bankers and savers.', old=True),
            'B2f': F('con_homes_for_the_nation', 'Homes for the Nation', [
                build('two_random_infrastructure'), stab(0.03), pop(0.03), prog('monthly_population', 0.05),
                money(-0.005),
            ], 'Tanaka\'s Plan for Remodelling the Japanese Archipelago (1972) and the Tories\' home-ownership drive built roads, towns and loyal voters.', old=True),
            'EM': F('con_the_social_market_economy', 'The Social Market Economy', [
                prog('productivity_growth_modifier', 0.05), prog('production_speed_buildings_factor', 0.05),
                fac('industrial_conglomerates', 5), fac('small_medium_business_owners', 5),
            ], 'The West German model of competition plus social insurance remained the reference point of every 1970s centre-right programme.'),

            # ---------------- society
            'C1': F('con_family_and_faith', 'Family and Faith', [
                prog('stability_factor', 0.03), fac('the_clergy', 10), prog('monthly_population', 0.05),
                prog('drift_defence_factor', 0.10), pop(0.03),
                prog('research_speed_factor', -0.02),
            ], 'Italy\'s Christian Democrats campaigned to repeal divorce in the 1974 referendum and lost, 59 to 41 %; the stand rallied the devout but alienated the cities and the young.'),
            'C2': F('con_a_modern_conservatism', 'A Modern Conservatism', [
                pop(0.05), prog('research_speed_factor', 0.03), prog('democratic_drift', 0.03), literacy(0.02),
                prog('party_popularity_stability_factor', 0.05),
                fac('the_clergy', -10),
            ], 'Giscard d\'Estaing lowered the voting age to 18 and legalised divorce by consent and abortion (1974-75), winning the young but angering the Church.'),
            'CM': F('con_the_property_owning_democracy', 'The Property-Owning Democracy', [
                build('one_office_construction'), prog('population_tax_income_multiplier_modifier', 0.05),
                stab(0.03), fac('small_medium_business_owners', 10),
            ], 'Conservatives from Eden to Thatcher promised a "property-owning democracy": every homeowner and shareholder a stakeholder in order.'),

            # ---------------- alliance and defence
            'D1': F('con_the_atlantic_alliance', 'The Atlantic Alliance', [
                tech(['CAT_medium_aircraft', 'CAT_anti_tank'], 0.35, 2), prog('mdcw_cw_assistance_limit', 0.25),
                prog('trade_opinion_factor', 0.05), xp('air', 25),
                prog('personnel_cost_multiplier_modifier', 0.05),
            ], 'The CDU and the British Conservatives kept NATO at the centre: American technology and markets, alliance force goals to pay for.'),
            'D2': F('con_national_independence', 'National Independence', [
                build('one_random_arms_factory'), tech(['CAT_main_battle_tanks', 'CAT_light_aircraft'], 0.35, 2),
                prog('foreign_influence_defense_modifier', 0.10), prog('military_factories_productivity', 0.05),
                prog('trade_opinion_factor', -0.05), money(-0.005),
            ], 'Gaullist France left NATO\'s integrated command (1966) and built its own Mirage jets and AMX tanks: independent, respected and expensive.'),
            'DM': F('con_a_credible_deterrent', 'A Credible Deterrent', [
                xp('army', 50), xp('air', 50), prog('army_defence_factor', 0.05),
                law('increase_military_spending'),
            ], 'Whether in the alliance or alone, the centre right promised a defence strong enough to deter, and raised the budget to match.'),

            # ---------------- capstone
            'CAP': F('con_the_natural_party_of_government', 'The Natural Party of Government', [
                idea('con_natural_party', {'stability_factor': 0.05, 'political_power_factor': 0.05,
                                           'party_popularity_stability_factor': 0.10, 'drift_defence_factor': 0.10},
                     'The Natural Party of Government', bound=True),
                pop(0.05), fac('all', 5),
            ], 'The LDP governed Japan from 1955 to 1993 and Italy\'s Christian Democrats led every government from late 1945 to 1981: the right as the permanent establishment.'),
        },
    ),

    # ======================================================================== Liberalism
    dict(
        key='lib',
        title='Free Citizens, Free Markets',
        identity='Free citizens and free markets: liberals must decide which freedom comes first, and who pays for the reforms.',
        history='The 1970s liberals split between civil-rights reformers (the FDP\'s Freiburg Theses 1971, Trudeau\'s Just Society) '
                'and electoral reformers (votes at 18, proportional representation); between market liberals (floating currencies, '
                'bank and airline deregulation, monetarism) and social liberals (worker capital formation, environmental law); '
                'between regional free trade and human-rights diplomacy (Helsinki 1975, Carter 1977).',
        foci={
            'E': F('lib_a_liberal_government', 'A Liberal Government', [
                prog('research_speed_factor', 0.03), prog('productivity_growth_modifier', 0.05), prog('democratic_drift', 0.03),
                fac('small_medium_business_owners', 10), fac('wall_street', 5),
            ], 'Liberals entered government as reformers: the FDP with Brandt (1969), Trudeau\'s Liberals (1968), D66 in the Netherlands (1973).', old=True),

            # ---------------- which freedom first
            'POL': F('lib_the_reform_cabinet', 'The Reform Cabinet', [
                pp(75), prog('bureaucracy_cost_multiplier_modifier', -0.05), prog('research_speed_factor', 0.02),
            ], 'The social-liberal coalitions of the early 1970s drew up long reform lists for justice, education and the civil service.'),
            'A1': F('lib_civil_liberties', 'Civil Liberties', [
                prog('research_speed_factor', 0.03), stab(0.03), prog('democratic_drift', 0.05), pop(0.05),
                prog('drift_defence_factor', -0.10),
            ], 'Trudeau\'s 1969 reform partly decriminalised homosexuality - "there\'s no place for the state in the bedrooms of the nation" - and liberals across Europe reformed criminal law; open societies are also open to rival ideas.', old=True),
            'A2': F('lib_electoral_reform', 'Electoral Reform', [
                pop(0.05), prog('party_popularity_stability_factor', 0.10), prog('stability_factor', 0.03), stab(0.02),
                prog('political_power_factor', -0.05),
            ], 'Liberal parties campaigned for proportional representation (the UK Liberals after February 1974): fairer seats, more stable consent, but coalition government.'),
            'A1f': F('lib_freedom_of_information_act', 'Freedom of Information Act', [
                corruption(-1), prog('bureaucracy_cost_multiplier_modifier', -0.05), prog('research_speed_factor', 0.02),
                prog('corruption_cost_factor', -0.10), stab(0.02),
                fac('intelligence_community', -10),
            ], 'After Watergate the US strengthened its Freedom of Information Act (1974) over a presidential veto; officials and secret services lost their shield.', old=True),
            'A2f': F('lib_votes_at_eighteen', 'Votes at Eighteen', [
                pop(0.05), stab(0.03), prog('democratic_drift', 0.03),
                idea('lib_extended_franchise', {'party_popularity_stability_factor': 0.10, 'stability_factor': 0.02}, 'An Extended Franchise'),
            ], 'Britain (1969), West Germany (1970) and the US (26th Amendment, 1971) lowered the voting age to 18 and brought a new generation into the system.'),
            'PM': F('lib_the_liberal_moment', 'The Liberal Moment', [
                prog('political_power_factor', 0.05), stab(0.02), prog('trade_opinion_factor', 0.05),
                fac('small_medium_business_owners', 5),
            ], 'With the reforms passed, liberals held the balance of power: the FDP decided who governed Bonn from 1969 to 1982.'),

            # ---------------- market or social liberalism
            'ECO': F('lib_float_the_currency', 'Float the Currency', [
                prog('interest_rate_multiplier_modifier', -0.5), prog('trade_opinion_factor', 0.05),
                prog('receiving_investment_cost_modifier', -0.05),
                fac('international_bankers', 10), money(0.005), prog('mdcw_cw_market_exposure', 0.05),
            ], 'After Nixon closed the gold window (1971) the Smithsonian pegs collapsed; from 1973 most Western currencies floated and capital controls began to fall (the US in 1974, Britain in 1979).'),
            'B1': F('lib_free_trade', 'Free Trade', [
                prog('return_on_investment_modifier', 0.005), prog('receiving_investment_cost_modifier', -0.10),
                prog('trade_opinion_factor', 0.10), prog('office_park_income_tax_modifier', 0.05),
                prog('mdcw_cw_market_exposure', 0.05),
            ], 'The Tokyo Round (1973-79) cut industrial tariffs by a third; open economies grew with world trade and caught its shocks.', old=True),
            'B2': F('lib_social_liberalism', 'Social Liberalism', [
                prog('productivity_growth_modifier', 0.05), fac('labour_unions', 10), prog('stability_factor', 0.03),
                prog('social_cost_multiplier_modifier', -0.05), prog('health_cost_multiplier_modifier', -0.05),
                money(-0.005),
            ], 'The FDP\'s Freiburg Theses (1971) demanded a liberalism of social reform: workers\' share in capital, environmental protection, co-determination.'),
            'B1f': F('lib_deregulate_the_banks', 'Deregulate the Banks', [
                build('two_office_construction'), prog('office_park_income_tax_modifier', 0.05),
                fac('international_bankers', 10), fac('wall_street', 10),
                prog('mdcw_cw_market_exposure', 0.05),
            ], 'London\'s Competition and Credit Control (1971) and the eurodollar boom freed the banks; credit grew fast, and the secondary banking crisis of 1973-75 followed.', old=True),
            'B2f': F('lib_shares_for_the_workers', 'Shares for the Workers', [
                idea('lib_capital_for_workers', {'productivity_growth_modifier': 0.10, 'consumer_goods_factor': -0.02},
                     'Capital for Workers'),
                stab(0.03), fac('labour_unions', 5), fac('small_medium_business_owners', 5),
            ], 'West Germany\'s 624-Mark Act (1970) doubled state support for workers\' savings and share schemes: wealth for employees through ownership rather than nationalisation.'),
            'EM': F('lib_an_open_economy', 'An Open Economy', [
                prog('productivity_growth_modifier', 0.05), growth(1), fac('small_medium_business_owners', 5),
            ], 'Liberal economics promised growth from competition rather than plans, a theme that came to dominate Western economic policy by the end of the 1970s.'),

            # ---------------- society
            'C1': F('lib_environmental_protection', 'Environmental Protection', [
                prog('stability_factor', 0.02), prog('monthly_population', 0.05), pop(0.05), fac('farmers', 5),
                prog('health_cost_multiplier_modifier', -0.10),
                fac('fossil_fuel_industry', -10),
            ], 'The US created the EPA and passed the Clean Air Act in 1970; West Germany\'s liberal interior ministry wrote the first environmental programme (1971).'),
            'C2': F('lib_open_the_universities', 'Open the Universities', [
                literacy(0.05), prog('research_speed_factor', 0.02), tech('CAT_computing', 0.5, 2), pop(0.02),
                law('increase_education_budget'), money(-0.005),
            ], 'The Open University (1971) and the wave of new German and Dutch universities opened higher education to the children of workers.'),
            'CM': F('lib_quality_of_life', 'Quality of Life', [
                stab(0.04), prog('monthly_population', 0.05), pop(0.04), build('one_random_infrastructure'),
            ], '"Quality of life" became a slogan of Western reformers in the early 1970s, from Bonn\'s social-liberal coalition to the new environmental groups: clean towns, public transport and leisure, not growth alone.'),

            # ---------------- foreign policy
            'D1': F('lib_a_regional_free_trade_area', 'A Regional Free Trade Area', [
                prog('trade_opinion_factor', 0.10), prog('resource_export_multiplier_modifier', 0.10),
                prog('globalism_equilibrium', 5), prog('office_park_income_tax_modifier', 0.05),
                fac('farmers', -10),
            ], 'EFTA, the enlarged EEC (1973) and ASEAN\'s preferential trade (1977) opened neighbouring markets to industrial goods; farmers, who feared open competition, fought to keep their protection.'),
            'D2': F('lib_human_rights_diplomacy', 'Human Rights Diplomacy', [
                prog('mdcw_cw_support_effectiveness', 0.10), prog('foreign_influence_modifier', 0.15),
                tension(-2), prog('democratic_drift', 0.03),
                fac('defense_industry', -10),
            ], 'The Helsinki Final Act (1975) and Carter\'s human-rights policy (1977) made liberal values a foreign-policy tool; arms exporters lost customers.'),
            'DM': F('lib_defence_on_a_budget', 'Defence on a Budget', [
                prog('personnel_cost_multiplier_modifier', -0.05), xp('army', 25),
                tech(['CAT_anti_tank', 'CAT_manpads'], 0.35, 2), prog('army_defence_factor', 0.03),
            ], 'Liberal finance ministers bought precision instead of mass: guided anti-tank weapons and shoulder-fired missiles for a smaller, cheaper army.'),

            # ---------------- capstone
            'CAP': F('lib_the_open_society', 'The Open Society', [
                idea('lib_open_society', {'research_speed_factor': 0.05, 'productivity_growth_modifier': 0.10,
                                          'stability_factor': 0.03, 'drift_defence_factor': -0.10}, 'The Open Society'),
                pop(0.05), build('one_office_construction'), fac('small_medium_business_owners', 10),
            ], 'Karl Popper\'s "open society" became the liberal creed of the Cold War: a state that can be criticised and corrected, prosperous because it is free.', old=True),
        },
    ),

    # ======================================================================== Social Democracy
    dict(
        key='sd',
        title='The People\'s Home',
        identity='Prosperity shared through the state and the unions: social democrats choose between wage restraint and '
                 'redistribution, and between détente and the alliance.',
        history='1970s social democracy offered several models: the union-led Social Contract (Wilson/Callaghan 1974) and Austria\'s '
                'social partnership against Schmidt\'s pragmatic crisis management; codetermination (West Germany 1976) and the '
                'Meidner wage-earner funds (Sweden 1976) against Keynesian full-employment spending; comprehensive schools against '
                'universal health care (Medibank 1975, Italy\'s SSN 1978); Brandt\'s Ostpolitik against Schmidt\'s alliance '
                'solidarity.',
        foci={
            'E': F('sd_a_social_democratic_government', 'A Social Democratic Government', [
                prog('stability_factor', 0.03), prog('party_popularity_stability_factor', 0.05),
                fac('labour_unions', 10), pop(0.03),
                law('increase_social_spending'),
            ], 'Social democrats took power across the West around 1970: Brandt (1969), Kreisky (1970), Palme (1969), Whitlam (1972) - and raised social spending at once.', old=True),

            # ---------------- unions or chancellor
            'POL': F('sd_dare_more_democracy', 'Dare More Democracy', [
                pp(75), pop(0.03), prog('democratic_drift', 0.03), stab(0.02),
            ], 'Brandt\'s 1969 government statement "Mehr Demokratie wagen" promised to open schools, workplaces and the state to participation.'),
            'A1': F('sd_the_social_contract', 'The Social Contract', [
                prog('consumer_goods_factor', -0.02), prog('stability_factor', 0.03), prog('productivity_growth_modifier', 0.05),
                fac('labour_unions', 10), stab(0.02),
                prog('political_power_factor', -0.05),
            ], 'Britain\'s Social Contract (1974): the unions accepted wage restraint in return for social policy - and gained great influence over government policy.'),
            'A2': F('sd_the_pragmatic_chancellor', 'The Pragmatic Chancellor', [
                prog('political_power_factor', 0.10), prog('bureaucracy_cost_multiplier_modifier', -0.10),
                fac('industrial_conglomerates', 5), stab(0.02),
                fac('labour_unions', -10),
            ], 'Helmut Schmidt (1974-82) governed as a crisis manager rather than a party ideologue: efficient and trusted by business, suspected by the left.'),
            'A1f': F('sd_the_parity_commission', 'The Parity Commission', [
                idea('sd_parity_commission', {'stability_factor': 0.03, 'consumer_goods_factor': -0.02,
                                              'internal_factions_cost_factor': -0.20}, 'The Parity Commission'),
                fac('labour_unions', 5), fac('industrial_conglomerates', 5),
            ], 'Austria\'s Parity Commission let unions and employers settle wages and prices together; Kreisky\'s Austria had one of the lowest strike rates in the Western world.'),
            'A2f': F('sd_crisis_management', 'Crisis Management', [
                prog('political_power_factor', 0.05), prog('interest_rate_multiplier_modifier', -0.5), money(0.005),
                stab(0.03), fac('international_bankers', 5), prog('trade_opinion_factor', 0.05),
                fac('labour_unions', -5),
            ], 'Schmidt\'s "Modell Deutschland" (1976) steered the economy through the oil crisis with low inflation and international summitry.'),
            'PM': F('sd_the_peoples_home', 'The People\'s Home', [
                prog('stability_factor', 0.02), prog('social_cost_multiplier_modifier', -0.05), prog('health_cost_multiplier_modifier', -0.05), pop(0.02),
            ], 'Per Albin Hansson\'s folkhem (1928) - society as a good home for all - became shorthand for the Swedish welfare state and a model for social democrats elsewhere.'),

            # ---------------- economic model
            'ECO': F('sd_the_budget_of_reforms', 'The Budget of Reforms', [
                prog('tax_gain_multiplier_modifier', 0.05), prog('population_tax_income_multiplier_modifier', 0.08),
                fac('labour_unions', 5),
            ], 'Higher progressive taxes paid for the reform programmes: by the late 1970s Swedish and Danish tax revenues exceeded 40 % of GDP, among the highest in the OECD.'),
            'B1': F('sd_codetermination', 'Codetermination', [
                fac('labour_unions', 10), prog('productivity_growth_modifier', 0.10), prog('stability_factor', 0.02), pop(0.03),
                prog('production_factory_efficiency_gain_factor', 0.05),
                fac('industrial_conglomerates', -10),
            ], 'West Germany\'s Codetermination Act (1976) gave employees half the supervisory board seats in firms with over 2,000 staff, with a shareholder casting vote; employers challenged it in the Constitutional Court and lost (1979).', old=True),
            'B2': F('sd_keynesian_expansion', 'Keynesian Expansion', [
                growth(1), prog('production_speed_buildings_factor', 0.10), build('one_random_infrastructure'),
                debt(0.02),
            ], 'Whitlam\'s Australia and Kreisky\'s "Austro-Keynesianism" ran deficits to keep demand and employment up after 1973.', old=True),
            'B1f': F('sd_wage_earner_funds', 'Wage-Earner Funds', [
                idea('sd_wage_earner_funds', {'productivity_growth_modifier': 0.10, 'consumer_goods_factor': -0.02,
                                              'stability_factor': 0.03, 'corporate_tax_income_multiplier_modifier': -0.04},
                     'Wage-Earner Funds'),
                build('one_random_industrial_complex'), fac('labour_unions', 10), pop(0.03),
                fac('wall_street', -10),
            ], 'Rudolf Meidner\'s plan, adopted by the LO unions in 1976, proposed union-run funds that would buy up Swedish firms out of profits; business mobilised against it, and only a diluted version passed in 1983.'),
            'B2f': F('sd_full_employment_programme', 'Full Employment Programme', [
                prog('social_cost_multiplier_modifier', -0.05), prog('health_cost_multiplier_modifier', -0.05), build('two_random_infrastructure'), fac('labour_unions', 5), stab(0.02),
                debt(0.01),
            ], 'Austria and Sweden kept unemployment at around 2 % through the 1970s with public works, training schemes and subsidised jobs.', old=True),
            'EM': F('sd_the_welfare_state_matures', 'The Welfare State Matures', [
                prog('stability_factor', 0.02), prog('productivity_growth_modifier', 0.05),
                prog('health_cost_multiplier_modifier', -0.05), fac('labour_unions', 5),
            ], 'By the late 1970s the Nordic welfare states provided pensions, health care and childcare as universal, tax-funded public services.'),

            # ---------------- schools or health
            'C1': F('sd_comprehensive_schools', 'Comprehensive Schools', [
                literacy(0.05), prog('research_speed_factor', 0.03), prog('literacy_rate_education_modifier', 0.05),
                fac('labour_unions', 5),
                money(-0.005),
            ], 'Sweden (1962) and Britain (from 1965) replaced selective schools with comprehensives, and SPD-led German Länder opened Gesamtschulen, to open education to every class.', old=True),
            'C2': F('sd_a_universal_health_service', 'A Universal Health Service', [
                prog('health_cost_multiplier_modifier', -0.15), prog('monthly_population', 0.05), stab(0.03), pop(0.02),
                law('increase_healthcare_budget'), money(-0.005),
            ], 'Canada\'s medicare covered every province by 1971, Australia launched Medibank (1975) and Italy its national health service (1978).'),
            'CM': F('sd_the_equality_reforms', 'The Equality Reforms', [
                prog('population_tax_income_multiplier_modifier', 0.05), prog('buildings_worker_requirement_modifier', -0.10),
                pop(0.04), stab(0.04),
                fac('the_clergy', -5),
            ], 'Separate taxation of spouses (Sweden 1971) and equal pay (Australia 1972) brought women into work and into the tax base; traditionalists, many in the churches, defended the single-breadwinner family.'),

            # ---------------- détente or alliance
            'D1': F('sd_ostpolitik', 'Ostpolitik', [
                tension(-2), prog('trade_opinion_factor', 0.15), prog('mdcw_cw_assistance_limit', 0.15), stab(0.02),
                outlook('E', 0.02), prog('drift_defence_factor', -0.10),
            ], 'Brandt\'s Moscow and Warsaw treaties (1970) and the Basic Treaty (1972) accepted the post-war borders in return for trade, contacts and easier travel; critics said they legitimised the Eastern regimes.', old=True),
            'D2': F('sd_alliance_solidarity', 'Alliance Solidarity', [
                tech(['CAT_surface_to_air_missiles', 'CAT_anti_tank'], 0.35, 2), prog('army_defence_factor', 0.03),
                xp('army', 25), prog('trade_opinion_factor', 0.05),
                law('increase_military_spending'), fac('labour_unions', -5), pop(-0.02),
            ], 'Schmidt\'s 1977 London speech helped prompt NATO\'s double-track decision (1979): social democrats stood by the alliance against their own peace wing.'),
            'DM': F('sd_common_security', 'Common Security', [
                tension(-1), prog('foreign_influence_defense_modifier', 0.10), prog('mdcw_cw_support_effectiveness', 0.10),
                stab(0.02), prog('trade_opinion_factor', 0.05),
            ], 'The Palme Commission (1980-82) and the Socialist International argued that security could only be achieved together with the adversary, not against it.'),

            # ---------------- capstone
            'CAP': F('sd_the_welfare_model', 'The Welfare Model', [
                idea('sd_welfare_model', {'stability_factor': 0.05, 'productivity_growth_modifier': 0.10,
                                          'social_cost_multiplier_modifier': -0.10, 'population_tax_income_multiplier_modifier': 0.05},
                     'The Welfare Model'),
                pop(0.05), fac('labour_unions', 10),
            ], 'The Scandinavian and Austrian model of high taxes, full employment and universal welfare was widely cited as a social model in the 1970s.'),
        },
    ),
]
