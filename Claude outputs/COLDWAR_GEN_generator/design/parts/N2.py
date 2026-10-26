# IMPERIA CW — Cold War: parts — N2.
from dsl import *

# Non-Aligned parties II: Neutral Libertarianism, Neutral Green, Neutral Social, Neutral Communism.

NLIB = dict(
    key='nlib',
    title='The Free Port State',
    identity='The state shrinks to a night-watchman: low flat taxes, free ports and open capital, with growth bought '
             'at the price of welfare and of organised labour\'s voice.',
    history='Hong Kong\'s laissez-faire under Cowperthwaite (1961-71) and Haddon-Cave\'s "positive non-interventionism" '
            '(1971-81), Singapore\'s free port, Lebanon\'s laissez-faire banking republic before 1975 and the '
            'monetarist experiments of Chile (1975) and Argentina (1976-81). The variants split between an unelected '
            'administrative state and constitutional limits, between a low flat tax and selling the state, between '
            'offshore banking and a neutral trading port.',
    foci={
        'E': F('nlib_the_minimal_state', 'The Minimal State', [
            prog('bureaucracy_cost_multiplier_modifier', -0.15), prog('productivity_growth_modifier', 0.05),
            fac('small_medium_business_owners', 10), law('decrease_social_spending'),
        ], 'Hong Kong\'s Financial Secretary John Cowperthwaite (1961-71) kept the state small: low spending, no '
           'industrial subsidies or industrial policy, and minimal social welfare.', old=True),

        # ---------------- the power question
        'POL': F('nlib_the_clean_government_commission', 'The Clean Government Commission', [
            corruption(-1), prog('corruption_cost_factor', -0.10), stab(0.03),
        ], 'Hong Kong\'s Independent Commission Against Corruption (1974) broke up the police corruption syndicates '
           'within a few years; a small state depends on clean officials.'),
        'A1': F('nlib_government_by_experts', 'Government by Experts', [
            prog('political_power_factor', 0.10), prog('bureaucracy_cost_multiplier_modifier', -0.05),
            prog('research_speed_factor', 0.03), prog('tax_gain_multiplier_modifier', 0.03), fac('international_bankers', 5),
            prog('party_popularity_stability_factor', -0.05),
        ], 'Colonial Hong Kong was run by appointed administrators, and Singapore by a technocratic cabinet facing no '
           'opposition in parliament (1968-81); decisions came fast, but the public had little say in them.'),
        'A2': F('nlib_constitutional_limits', 'Constitutional Limits', [
            prog('stability_factor', 0.05), prog('foreign_influence_defense_modifier', 0.05),
            prog('receiving_investment_cost_modifier', -0.05), prog('interest_rate_multiplier_modifier', -0.25),
            prog('drift_defence_factor', 0.10), prog('political_power_factor', -0.05),
        ], 'Classical liberals from Hayek (The Constitution of Liberty, 1960) to the US tax revolt (California\'s '
           'Proposition 13, 1978) wanted firm limits on taxing and spending; investors trusted the rules, the '
           'government lost room to act.'),
        'A1f': F('nlib_administrative_absorption', 'Administrative Absorption', [
            idea('nlib_executive_led_government', {'political_power_factor': 0.05, 'bureaucracy_cost_multiplier_modifier': -0.10,
                                                   'stability_factor': 0.02}, 'Executive-Led Government', bound=True),
            prog('drift_defence_factor', 0.10), fac('small_medium_business_owners', 5), fac('labour_unions', -5),
        ], 'Hong Kong co-opted business and community leaders into hundreds of advisory boards instead of holding '
           'general elections (the "administrative absorption of politics", Ambrose King 1975).'),
        'A2f': F('nlib_a_balanced_budget_rule', 'A Balanced-Budget Rule', [
            idea('nlib_balanced_budget_rule', {'interest_rate_multiplier_modifier': -0.5, 'stability_factor': 0.03,
                                               'receiving_investment_cost_modifier': -0.05}, 'The Balanced-Budget Rule'),
            fac('international_bankers', 10), pop(0.03),
        ], 'Hong Kong held the growth of public spending to the growth of the economy, and the 1970s American '
           'campaign for a balanced-budget amendment sought to write such a rule into the constitution.'),
        'PM': F('nlib_the_night_watchman_state', 'The Night-Watchman State', [
            pp(75), prog('political_power_factor', 0.05), stab(0.02), prog('tax_gain_multiplier_modifier', 0.03),
            fac('small_medium_business_owners', 5),
        ], 'Robert Nozick\'s Anarchy, State, and Utopia (1974) gave the minimal state its manifesto: courts, police and '
           'defence, and little else.'),

        # ---------------- the economic model
        'ECO': F('nlib_positive_non_interventionism', 'Positive Non-Interventionism', [
            prog('productivity_growth_modifier', 0.05), prog('receiving_investment_cost_modifier', -0.05),
            prog('office_park_income_tax_modifier', 0.05), prog('return_on_investment_modifier', 0.005), fac('wall_street', 5),
        ], 'Financial Secretary Haddon-Cave (1971-81) called Hong Kong\'s doctrine "positive non-interventionism": the '
           'state set the framework and stayed out of the market unless intervention was clearly justified.'),
        'B1': F('nlib_a_flat_tax', 'A Flat Tax', [
            prog('productivity_growth_modifier', 0.10), prog('receiving_investment_cost_modifier', -0.10),
            prog('office_park_income_tax_modifier', 0.10), fac('small_medium_business_owners', 10),
            prog('tax_gain_multiplier_modifier', -0.05),
        ], 'Hong Kong\'s standard tax rate of about 15 % on salaries and profits drew firms and capital from across '
           'the region, but left the treasury with less to spend.', old=True),
        'B2': F('nlib_privatise_state_enterprises', 'Privatise State Enterprises', [
            money(0.015), prog('productivity_growth_modifier', 0.05), prog('corporate_tax_income_multiplier_modifier', 0.06),
            prog('production_factory_efficiency_gain_factor', 0.05), fac('wall_street', 10), fac('labour_unions', -15), stab(-0.02),
        ], 'Between 1974 and 1978 Chile returned or sold most of the firms taken over under Allende, raising revenue '
           'while the unions, already curbed by the junta, lost their strongest workplaces.', old=True),
        'B1f': F('nlib_free_enterprise_zones', 'Free Enterprise Zones', [
            build('two_office_construction'), build('one_random_infrastructure'),
            prog('office_park_income_tax_modifier', 0.05), prog('trade_opinion_factor', 0.05),
            prog('mdcw_cw_market_exposure', 0.05),
        ], 'Ireland\'s Shannon Free Zone (1959), Taiwan\'s Kaohsiung zone (1966) and South Korea\'s Masan (1970) drew foreign '
           'assemblers with tax holidays and duty-free ports, tying the economy to world demand.', old=True),
        'B2f': F('nlib_sell_the_state_railways', 'Sell the State Railways', [
            money(0.01), build('one_random_infrastructure'), prog('production_speed_infrastructure_factor', 0.10),
            prog('production_speed_buildings_factor', 0.03), fac('labour_unions', -5),
        ], 'Chile deregulated road transport and port labour from the late 1970s and sold its electricity and '
           'telephone companies in 1985-89; Japan broke up and privatised its national railways in 1987.', old=True),
        'EM': F('nlib_capital_without_borders', 'Capital Without Borders', [
            prog('return_on_investment_modifier', 0.005), prog('receiving_investment_cost_modifier', -0.05),
            prog('interest_rate_multiplier_modifier', -0.25), prog('office_park_income_tax_modifier', 0.05),
            fac('international_bankers', 10), prog('mdcw_cw_market_exposure', 0.05),
        ], 'Hong Kong dropped its exchange controls in the early 1970s and Britain abolished its own in 1979: capital '
           'flowed in freely, and out again whenever the world market turned.'),

        # ---------------- society
        'C1': F('nlib_vouchers_and_private_clinics', 'Vouchers and Private Clinics', [
            prog('education_cost_multiplier_modifier', -0.10), prog('health_cost_multiplier_modifier', -0.10),
            money(0.01), fac('small_medium_business_owners', 5), stab(-0.03),
        ], 'Milton Friedman proposed school vouchers in 1955, and Chile introduced vouchers and private health '
           'insurers (ISAPREs) in 1980-81: public spending fell, and critics pointed to a widening gap between rich '
           'and poor.'),
        'C2': F('nlib_a_negative_income_tax', 'A Negative Income Tax', [
            prog('stability_factor', 0.04), prog('bureaucracy_cost_multiplier_modifier', -0.05),
            prog('productivity_growth_modifier', 0.05), prog('social_cost_multiplier_modifier', -0.05), pop(0.04),
            fac('labour_unions', 5), prog('tax_gain_multiplier_modifier', -0.03),
        ], 'Friedman\'s negative income tax (1962) proposed replacing welfare offices with one cash payment; the US '
           'tested it in New Jersey (1968-72) and in Seattle and Denver during the 1970s.'),
        'CM': F('nlib_a_society_of_self_help', 'A Society of Self-Help', [
            stab(0.03), literacy(0.03), prog('research_speed_factor', 0.03), prog('health_cost_multiplier_modifier', -0.05),
            pop(0.03),
        ], 'Hong Kong\'s kaifong neighbourhood associations, clan societies and charities such as the Tung Wah '
           'hospitals carried much of the social work into the 1970s, with limited help from the state.'),

        # ---------------- foreign stance and defence
        'D1': F('nlib_a_port_for_every_flag', 'A Port for Every Flag', [
            prog('trade_opinion_factor', 0.10), prog('imp_sanction_resistance', 0.05), prog('globalism_equilibrium', 5),
            build('one_random_infrastructure'), prog('mdcw_cw_market_exposure', 0.05),
        ], 'Hong Kong and Singapore traded with both Cold War camps at once, from Western banks to Chinese and Soviet '
           'shipping, and felt every swing in world trade first.'),
        'D2': F('nlib_offshore_banking_haven', 'Offshore Banking Haven', [
            build('one_office_construction'), prog('office_park_income_tax_modifier', 0.10),
            prog('return_on_investment_modifier', 0.005), fac('international_bankers', 10),
            prog('foreign_influence_defense_modifier', -0.05), prog('corruption_cost_factor', 0.05),
        ], 'Beirut until 1975 and the Bahamas, the Cayman Islands and Luxembourg prospered on bank secrecy and low '
           'taxes; foreign money also brought foreign influence and illicit funds.'),
        'DM': F('nlib_an_all_volunteer_force', 'An All-Volunteer Force', [
            xp('army', 50), prog('experience_gain_army_factor', 0.10), prog('army_org_factor', 0.03),
            prog('training_time_army_factor', -0.05), prog('army_morale_factor', 0.05),
            tech('CAT_small_arms', 0.35, 1), prog('conscription_factor', -0.03),
        ], 'The Gates Commission (1970), with Milton Friedman as a member, recommended ending the US draft, which '
           'stopped in 1973: a smaller, professional force replaced the conscripts.'),

        # ---------------- capstone
        'CAP': F('nlib_the_free_society', 'The Free Society', [
            idea('nlib_free_society', {'productivity_growth_modifier': 0.10, 'research_speed_factor': 0.03,
                                       'receiving_investment_cost_modifier': -0.10, 'office_park_income_tax_modifier': 0.05,
                                       'social_cost_multiplier_modifier': 0.05}, 'The Free Society'),
            build('two_office_construction'), outlook('N', 0.03),
        ], 'Hayek (Nobel 1974) and Friedman (Nobel 1976) gave free-market ideas new prestige, and Hong Kong\'s economy '
           'grew by about 9 % a year in real terms through the 1970s.', old=True),
    },
)

GR = dict(
    key='gr',
    title='The Steady-State Republic',
    identity='Growth is no longer the measure: the party trades industrial expansion for clean energy, protected land and '
             'small-scale enterprise, and refuses both blocs\' arms race.',
    history='The Club of Rome\'s Limits to Growth (1972), Schumacher\'s Small Is Beautiful (1973), New Zealand\'s Values Party '
            '(1972), India\'s Chipko movement (1973), the Austrian Zwentendorf (1978) and Swedish (1980) nuclear referendums '
            'and the West German Greens (1980). The movement split between grassroots radicals and realists, between '
            'conservation and the anti-nuclear struggle, and between pacifism and non-offensive defence.',
    foci={
        'E': F('gr_the_limits_to_growth', 'The Limits to Growth', [
            prog('stability_factor', 0.03), prog('research_speed_factor', 0.02), prog('party_popularity_stability_factor', 0.05),
            fac('farmers', 10), pop(0.04), fac('fossil_fuel_industry', -10),
        ], 'The Club of Rome\'s report (1972) sold millions of copies and turned "limits to growth" into a political '
           'programme; economists and industry attacked its forecasts from the start.', old=True),

        # ---------------- the power question
        'POL': F('gr_the_citizens_initiatives', 'The Citizens\' Initiatives', [
            stab(0.03), prog('drift_defence_factor', 0.10), pop(0.03), fac('small_medium_business_owners', 5),
        ], 'West Germany counted thousands of local citizens\' initiatives (Bürgerinitiativen) by the mid-1970s, '
           'from Wyhl to Brokdorf; the green parties grew out of them.'),
        'A1': F('gr_grassroots_democracy', 'Grassroots Democracy', [
            prog('stability_factor', 0.05), prog('party_popularity_stability_factor', 0.10),
            prog('mdcw_cw_ideological_defence', 0.10), pop(0.05),
            prog('political_power_factor', -0.05), prog('production_speed_buildings_factor', -0.03),
        ], 'The early West German Greens rotated their Bundestag deputies (from 1983), bound them to the party base '
           'and decided in open assemblies; the base trusted them, but decisions were slow.'),
        'A2': F('gr_the_realist_wing', 'The Realist Wing', [
            pp(100), prog('political_power_factor', 0.10), prog('bureaucracy_cost_multiplier_modifier', -0.05),
            fac('labour_unions', 10), fac('farmers', -5), prog('drift_defence_factor', -0.05),
        ], 'The "Realos" around Joschka Fischer accepted ministries and coalitions (Hesse 1985) to get results, at '
           'the cost of bitter conflict with the party\'s radical wing.'),
        'A1f': F('gr_the_people_decide', 'The People Decide', [
            idea('gr_referendum_democracy', {'stability_factor': 0.04, 'drift_defence_factor': 0.10,
                                             'foreign_influence_defense_modifier': 0.05}, 'Referendum Democracy'),
            pop(0.04), fac('all', 3),
        ], 'Austria\'s Zwentendorf referendum (1978) stopped a finished nuclear plant, and Sweden voted on nuclear power in '
           '1980: citizens could overrule government and industry.'),
        'A2f': F('gr_a_ministry_for_the_environment', 'A Ministry for the Environment', [
            idea('gr_environment_ministry', {'research_speed_factor': 0.03, 'monthly_population': 0.05,
                                             'health_cost_multiplier_modifier': -0.05}, 'Ministry for the Environment'),
            prog('political_power_factor', 0.05), stab(0.03), prog('bureaucracy_cost_multiplier_modifier', 0.03),
        ], 'Britain (1970), Japan (1971) and West Germany\'s Federal Environment Agency (1974) gave the environment its own '
           'ministry or agency, with real powers and a new bureaucracy.'),
        'PM': F('gr_spaceship_earth', 'Spaceship Earth', [
            prog('stability_factor', 0.02), prog('research_speed_factor', 0.02), literacy(0.02), pop(0.03), fac('farmers', 5),
        ], 'Boulding\'s "spaceship earth" (1966), the first Earth Day (1970) and the UN Stockholm conference (1972) put '
           'ecology into schools and newspapers.'),

        # ---------------- the economic model
        'ECO': F('gr_the_polluter_pays', 'The Polluter Pays', [
            prog('tax_gain_multiplier_modifier', 0.05), prog('health_cost_multiplier_modifier', -0.05),
            prog('monthly_population', 0.05), fac('farmers', 5), fac('fossil_fuel_industry', -5),
        ], 'The OECD adopted the polluter-pays principle in 1972, and Dutch (1970) and West German (1976) '
           'water-pollution levies made industry pay for its discharges while funding the clean-up.'),
        'B1': F('gr_conservation_laws', 'Conservation Laws', [
            prog('monthly_population', 0.05), prog('stability_factor', 0.03), prog('agricolture_productivity_modifier', 0.05),
            prog('health_cost_multiplier_modifier', -0.05), fac('farmers', 10),
            prog('production_speed_buildings_factor', -0.05),
        ], 'Clean air and water laws (US 1970-72, Japan\'s "Pollution Diet" of 1970) protected health and farmland but '
           'slowed approval of new factories and dams.', old=True),
        'B2': F('gr_a_nuclear_free_future', 'A Nuclear-Free Future', [
            mdtimed('hydroelectric_energy_production_idea', 1095), build('one_random_renewable_energy_infra'),
            pop(0.04), prog('stability_factor', 0.02), prog('energy_gain_multiplier', -0.05),
            flag('GEN_1970_nuclear_free', 'The foci §YThe Atomic Future§! and §YFirst Nuclear Power Station§! are no longer available'),
        ], 'After Wyhl (1975) and Zwentendorf (1978) the anti-nuclear movement became central to green politics; it '
           'bet on water, sun and wind instead of the atom.', old=True),
        'B1f': F('gr_protected_landscapes', 'Protected Landscapes', [
            idea('gr_national_parks', {'stability_factor': 0.03, 'agricolture_productivity_modifier': 0.08,
                                       'trade_opinion_factor': 0.05}, 'National Parks and Reserves'),
            build('one_random_agriculture_district'), fac('farmers', 5), fac('landowners', -5),
        ], 'India\'s Chipko movement (1973) defended village forests against commercial logging, Project Tiger (1973) '
           'created protected reserves, and the Forest Conservation Act (1980) curbed the clearing of forest land.', old=True),
        'B2f': F('gr_small_is_beautiful', 'Small Is Beautiful', [
            prog('productivity_growth_modifier', 0.10), prog('buildings_worker_requirement_modifier', -0.05),
            build('one_random_renewable_energy_infra'), tech('CAT_agriculture', 0.5, 1),
            fac('small_medium_business_owners', 10), prog('industrial_capacity_factory', -0.03),
        ], 'Schumacher\'s Small Is Beautiful (1973) and his Intermediate Technology group promoted small workshops and '
           'village power instead of giant plants.', old=True),
        'EM': F('gr_the_soft_energy_path', 'The Soft Energy Path', [
            build('one_random_renewable_energy_infra'), prog('energy_gain_multiplier', 0.05),
            prog('imp_oil_price_resistance', 0.10), stab(0.02), fac('fossil_fuel_industry', -5),
        ], 'Amory Lovins\' "soft energy path" (1976) answered the oil shock with efficiency and renewables instead of new '
           'oil and nuclear plants.'),

        # ---------------- security
        'C1': F('gr_civilian_based_defence', 'Civilian-Based Defence', [
            prog('defensive_war_stability_factor', 0.30), prog('drift_defence_factor', 0.15),
            prog('mdcw_cw_ideological_defence', 0.10), prog('foreign_influence_defense_modifier', 0.05),
            law('decrease_military_spending'),
            prog('conscription_factor', -0.03),
        ], 'Gene Sharp\'s The Politics of Nonviolent Action (1973) inspired plans for defence by strikes and '
           'non-cooperation; the Danish, Dutch and Swedish governments commissioned studies of the idea.'),
        'C2': F('gr_non_offensive_defence', 'Non-Offensive Defence', [
            prog('army_core_defence_factor', 0.10), prog('production_speed_bunker_factor', 0.20),
            prog('production_speed_bunker_factor', 0.10), tech(['CAT_light_anti_tank', 'CAT_anti_tank'], 0.35, 2),
            prog('army_attack_factor', -0.05),
        ], 'Horst Afheldt\'s "defensive defence" (1976) wanted an army that could hold its own ground but threaten no '
           'one - dispersed light infantry with anti-tank weapons instead of tank divisions.'),
        'CM': F('gr_swords_into_ploughshares', 'Swords into Ploughshares', [
            tension(-1), stab(0.03), money(0.005), prog('consumer_goods_factor', -0.02),
            prog('production_speed_industrial_complex_factor', 0.10), pop(0.03), fac('defense_industry', -10),
        ], 'The "Swords into Ploughshares" badge of the East German church peace movement (1980-81) and the '
           'Euromissile protests (1981-83) brought millions onto the streets to demand disarmament and lower arms '
           'spending.'),

        # ---------------- foreign stance
        'D1': F('gr_a_nuclear_free_zone', 'A Nuclear-Free Zone', [
            tension(-2), prog('foreign_influence_defense_modifier', 0.10), prog('mdcw_cw_ideological_defence', 0.10),
            stab(0.02), pop(0.04), prog('trade_opinion_factor', -0.05),
        ], 'Latin America\'s Tlatelolco treaty (1967) banned nuclear weapons from the region, and New Zealand\'s '
           'nuclear-free policy (1984) closed its ports to nuclear-armed ships, straining its alliance with the '
           'United States.'),
        'D2': F('gr_fair_trade_and_development', 'Fair Trade and Development', [
            prog('trade_opinion_factor', 0.10), prog('mdcw_cw_support_effectiveness', 0.10),
            prog('foreign_influence_modifier', 0.10), prog('mdcw_cw_assistance_capacity', 1), money(-0.005),
        ], 'The first fair-trade shops (1969-73), the call for a New International Economic Order (1974) and the '
           'Brandt Report (1980) pressed for fairer trade and more aid for the South - paid from the budget.'),
        'DM': F('gr_the_green_international', 'The Green International', [
            pop(0.04), outlook('N', 0.03), prog('foreign_influence_modifier', 0.10), prog('research_speed_factor', 0.02),
            stab(0.02),
        ], 'European green parties coordinated from 1979 and formed the Rainbow Group in the European Parliament (1984), '
           'spreading ideas and contacts across borders.'),

        # ---------------- capstone
        'CAP': F('gr_neither_growth_nor_bloc', 'Neither Growth nor Bloc', [
            idea('gr_steady_state_economy', {'stability_factor': 0.05, 'monthly_population': 0.05,
                                             'productivity_growth_modifier': 0.05, 'consumer_goods_factor': -0.02,
                                             'industrial_capacity_factory': -0.03}, 'The Steady-State Economy'),
            tension(-1), outlook('N', 0.04), build('one_random_renewable_energy_infra'), fac('farmers', 5),
        ], 'Herman Daly\'s Steady-State Economics (1977) gave the movement its economics, and Petra Kelly\'s West '
           'German Greens opposed the missiles of both blocs, protesting in East Berlin in 1983.', old=True),
    },
)

NS = dict(
    key='ns',
    title='Socialism of Our Own',
    identity='A socialism between the blocs: the party nationalises the commanding heights, mobilises the villages and '
             'keeps aid from both camps flowing.',
    history='Nyerere\'s Arusha Declaration and Ujamaa villages (1967-76), Indira Gandhi\'s bank nationalisation (1969) and '
            '"Garibi Hatao" (1971), the Bandaranaike United Front in Sri Lanka (1970-77), Allende\'s Popular Unity (1970-73), '
            'Peru\'s social property and Guyana\'s Cooperative Republic (1970). They split between one-party mobilisation '
            'and pluralist popular fronts, between village socialism and state-led industry, between aid from both camps '
            'and collective self-reliance of the South.',
    foci={
        'E': F('ns_non_aligned_socialism', 'Non-Aligned Socialism', [
            prog('stability_factor', 0.03), prog('production_speed_buildings_factor', 0.05), fac('labour_unions', 10),
            pop(0.03), law('increase_social_spending'),
        ], 'The Arusha Declaration (1967) promised a socialism neither copied from Moscow nor from Beijing, built on '
           'self-reliance and social spending.', old=True),

        # ---------------- the power question
        'POL': F('ns_the_socialist_charter', 'The Socialist Charter', [
            pp(100), stab(0.02), fac('labour_unions', 5),
        ], 'Socialist charters such as Arusha (1967), Zambia\'s Mulungushi reforms (1968) and Guyana\'s Cooperative Republic '
           '(1970) turned party programmes into state doctrine.'),
        'A1': F('ns_the_one_party_state', 'The One-Party State', [
            prog('political_power_factor', 0.10), prog('drift_defence_factor', 0.15), prog('mdcw_cw_ideological_defence', 0.10),
            stab(0.03), outlook('W', -0.02), prog('research_speed_factor', -0.02), fac('small_medium_business_owners', -5),
        ], 'Tanzania (1965) and Zambia (1972) made the ruling party the only legal one: power and unity were secured, open '
           'debate and private business shrank.'),
        'A2': F('ns_the_popular_front', 'The Popular Front', [
            prog('stability_factor', 0.04), prog('party_popularity_stability_factor', 0.10), fac('all', 3), pop(0.05),
            prog('political_power_factor', -0.05), outlook('W', 0.02),
        ], 'Allende\'s Popular Unity (1970) and Sri Lanka\'s United Front (1970) governed as multi-party coalitions '
           'within parliamentary systems: broad alliances, constant bargaining.'),
        'A1f': F('ns_the_party_is_supreme', 'The Party Is Supreme', [
            idea('ns_party_supremacy', {'political_power_factor': 0.05, 'stability_factor': 0.03,
                                        'bureaucracy_cost_multiplier_modifier': -0.05, 'drift_defence_factor': 0.10},
                 'Party Supremacy', bound=True),
            stab(0.02), fac('labour_unions', 5), corruption_chance(),
        ], 'Tanzania\'s 1975 amendment declared party supremacy over the state, and party and state offices '
           'increasingly merged, which also bred patronage.'),
        'A2f': F('ns_the_constitutional_road', 'The Constitutional Road', [
            idea('ns_constitutional_road', {'stability_factor': 0.03, 'foreign_influence_defense_modifier': 0.05,
                                            'research_speed_factor': 0.02}, 'The Constitutional Road'),
            pop(0.04), fac('small_medium_business_owners', 5),
        ], 'Allende\'s "Chilean road to socialism" (1970-73) kept parliament, courts and press, and Sri Lanka\'s United Front '
           'won and lost power at the ballot box.'),
        'PM': F('ns_the_mass_organisations', 'The People\'s Organisations', [
            prog('stability_factor', 0.02), prog('conscription_factor', 0.02), prog('war_support_factor', 0.03),
            fac('labour_unions', 5), pop(0.03),
        ], 'Youth leagues, women\'s unions and cooperative federations, such as TANU\'s Youth League, carried the '
           'programme into villages and workplaces.'),

        # ---------------- the economic model
        'ECO': F('ns_the_planning_commission', 'The Planning Commission', [
            prog('production_speed_buildings_factor', 0.05), prog('industrial_capacity_factory', 0.03), stab(0.02),
        ], 'India\'s Planning Commission (1950) and its five-year plans became a model for many non-aligned '
           'governments that wanted planning without Soviet control.'),
        'B1': F('ns_village_socialism', 'Village Socialism', [
            prog('agricolture_productivity_modifier', 0.10), build('one_random_agriculture_district'), fac('farmers', 10),
            prog('monthly_population', 0.05), stab(0.02), fac('landowners', -10), prog('productivity_growth_modifier', -0.05),
        ], 'Tanzania\'s Ujamaa policy (1967-76) moved millions of peasants into planned villages with communal plots; '
           'schools and water came closer, but forced villagisation (1973-76) disrupted farm output.', old=True),
        'B2': F('ns_command_of_the_heights', 'Command of the Heights', [
            money(0.01), prog('production_speed_buildings_factor', 0.08), prog('interest_rate_multiplier_modifier', -0.50),
            prog('production_speed_industrial_complex_factor', 0.05), fac('labour_unions', 5), fac('international_bankers', -15), prog('receiving_investment_cost_modifier', 0.05),
        ], 'India nationalised its 14 largest banks in 1969 and Sri Lanka its company-owned plantations in 1975: '
           'credit was steered to state priorities, and foreign investors held back.', old=True),
        'B1f': F('ns_cooperative_literacy_drive', 'Cooperative Literacy Drive', [
            literacy(0.05), prog('literacy_rate_education_modifier', 0.03), build('one_random_infrastructure'),
            fac('farmers', 5), stab(0.02),
        ], 'Tanzania\'s adult literacy campaigns of the 1970s, organised in the villages by party and government, '
           'roughly doubled the share of adults who could read.', old=True),
        'B2f': F('ns_abolish_poverty', 'Abolish Poverty', [
            build('two_random_industrial_complex'), stab(0.03), prog('social_cost_multiplier_modifier', -0.05),
            law('increase_social_spending'),
        ], 'Indira Gandhi won the 1971 election on "Garibi Hatao" (abolish poverty): nationalised banks lent to '
           'farmers and small firms, and the state expanded public-sector plants and social programmes.', old=True),
        'EM': F('ns_the_public_sector_backbone', 'The Public Sector Backbone', [
            growth(1), prog('industrial_capacity_factory', 0.03), fac('labour_unions', 5),
        ], 'By the late 1970s public-sector firms produced most of India\'s steel and power and much of its '
           'fertiliser, and played a similar role in many other non-aligned states.'),

        # ---------------- society
        'C1': F('ns_national_service_corps', 'National Service Corps', [
            prog('conscription_factor', 0.03), prog('war_support_factor', 0.03), build('one_random_infrastructure'),
            xp('army', 25), prog('training_time_army_factor', -0.05), prog('stability_factor', -0.02),
        ], 'Tanzania\'s National Service (JKT, compulsory for graduates from 1966) and the Zambia National Service '
           '(1971) sent young people to build roads and farms; Tanzanian students protested in 1966.'),
        'C2': F('ns_universal_primary_education', 'Universal Primary Education', [
            literacy(0.04), prog('literacy_rate_education_modifier', 0.04), prog('research_speed_factor', 0.02), stab(0.02),
            pop(0.04),
            prog('education_cost_multiplier_modifier', 0.05),
        ], 'Tanzania\'s Musoma Resolution (1974) promised a primary school place for every child by 1977; enrolment '
           'nearly doubled within three years, and education spending rose sharply.'),
        'CM': F('ns_the_socialist_citizen', 'The Socialist Citizen', [
            prog('stability_factor', 0.02), pop(0.04), prog('drift_defence_factor', 0.10),
            prog('productivity_growth_modifier', 0.05), literacy(0.03), fac('labour_unions', 5),
        ], 'Nyerere\'s "Education for Self-Reliance" (1967) wanted citizens who worked for the community; schools ran farms '
           'and workshops.'),

        # ---------------- foreign stance
        'D1': F('ns_aid_from_both_camps', 'Aid from Both Camps', [
            prog('mdcw_cw_assistance_limit', 0.25), build('two_random_infrastructure'),
            prog('production_speed_infrastructure_factor', 0.10), prog('foreign_influence_defense_modifier', -0.05),
        ], 'China built the TAZARA railway (1970-75) while Sweden and the other Nordic states became Tanzania\'s main '
           'donors; India took Soviet steel plants and American grain - and the influence that came with them.'),
        'D2': F('ns_collective_self_reliance', 'Collective Self-Reliance', [
            prog('imp_sanction_resistance', 0.10), prog('trade_opinion_factor', 0.05),
            prog('mdcw_cw_market_exposure', -0.10), prog('resource_export_multiplier_modifier', 0.05),
            prog('mdcw_cw_assistance_limit', -0.15),
        ], 'The Group of 77 (1964) and the Arusha Programme for Collective Self-Reliance (1979) urged the South to trade '
           'with itself and depend less on donors.'),
        'DM': F('ns_a_voice_for_the_south', 'A Voice for the South', [
            pp(50), prog('foreign_influence_modifier', 0.05), prog('mdcw_cw_support_effectiveness', 0.10), outlook('N', 0.03),
            stab(0.02), tension(-1),
        ], 'The UN declared a New International Economic Order in 1974, and Non-Aligned summits (Algiers 1973, Colombo 1976) '
           'made the South a voice in world politics.'),

        # ---------------- capstone
        'CAP': F('ns_self_reliant_socialism', 'Self-Reliant Socialism', [
            idea('ns_self_reliant_socialism', {'production_speed_buildings_factor': 0.05, 'stability_factor': 0.03,
                                               'imp_sanction_resistance': 0.10, 'productivity_growth_modifier': 0.05,
                                               'consumer_goods_factor': 0.02}, 'Self-Reliant Socialism'),
            growth(1), outlook('N', 0.03),
        ], 'Self-reliance (kujitegemea) was the stated goal of Nyerere\'s socialism: a mostly public economy meant to '
           'stand without either bloc, though Tanzania stayed heavily dependent on foreign aid.', old=True),
    },
)

NC = dict(
    key='nc',
    title='Communism Without Moscow',
    identity='Communism outside the Soviet bloc: the party guards its sovereignty against both camps and chooses between '
             'Yugoslav self-management and a Romanian-style national Stalinism.',
    history='Tito\'s Yugoslavia (self-management, the 1974 constitution, Total National Defence from 1969), Ceausescu\'s '
            'Romania (refusal to join the 1968 invasion, the July Theses of 1971, systematisation from 1974), Hoxha\'s '
            'Albania (self-reliance, the 1976 ban on foreign credits) and Eurocommunism (the PCI\'s historic compromise, 1973). '
            'The split ran between market self-management and centralised national Stalinism, between Western credits '
            'and autarky, between leading the Non-Aligned and playing the maverick between the blocs.',
    foci={
        'E': F('nc_our_own_road_to_socialism', 'Our Own Road to Socialism', [
            prog('drift_defence_factor', 0.15), prog('foreign_influence_defense_modifier', 0.10),
            fac('communist_cadres', 10), pop(0.03),
        ], 'Tito\'s break with Stalin (1948) and Romania\'s refusal to join the invasion of Czechoslovakia (1968) '
           'defined communist parties that took no orders from Moscow.', old=True),

        # ---------------- the power question
        'POL': F('nc_the_league_of_communists', 'The League of Communists', [
            pp(100), prog('political_power_factor', 0.05), fac('communist_cadres', 5),
        ], 'The Yugoslav party renamed itself a "League" (1952) to stress that it led society rather than administered it; '
           'its congresses set the line for the state.'),
        'A1': F('nc_workers_self_management', 'Workers\' Self-Management', [
            prog('productivity_growth_modifier', 0.10), prog('bureaucracy_cost_multiplier_modifier', -0.10),
            fac('labour_unions', 10), pop(0.04), prog('political_power_factor', -0.05), fac('communist_cadres', -5),
        ], 'Yugoslav workers\' councils (from 1950) helped choose managers and divided enterprise income, and the 1974 '
           'constitution and 1976 Associated Labour Act extended self-management across the whole economy.', old=True),
        'A2': F('nc_national_stalinism', 'National Stalinism', [
            prog('political_power_factor', 0.10), prog('industrial_capacity_factory', 0.05), prog('drift_defence_factor', 0.10),
            prog('mdcw_cw_ideological_defence', 0.10), fac('communist_cadres', 10), prog('research_speed_factor', -0.02), prog('consumer_goods_factor', 0.02),
        ], 'After his 1971 visit to China and North Korea and the July Theses, Ceausescu centralised power and pushed '
           'heavy industry in Romania; culture and consumer goods suffered.', old=True),
        'A1f': F('nc_market_socialism', 'Market Socialism', [
            prog('receiving_investment_cost_modifier', -0.10), prog('consumer_goods_factor', -0.02),
            prog('trade_opinion_factor', 0.05), build('one_office_construction'), fac('labour_unions', 5),
            prog('mdcw_cw_market_exposure', 0.05),
        ], 'Yugoslavia\'s 1965 reform gave self-managed firms more freedom over prices, investment and foreign trade; '
           'Western credits and consumer goods followed, and so did exposure to world markets.', old=True),
        'A2f': F('nc_systematisation', 'Systematisation', [
            prog('production_speed_buildings_factor', 0.15), build('one_random_infrastructure'), fac('communist_cadres', 5),
            stab(-0.02), fac('farmers', -10),
        ], 'Romania\'s systematisation law (1974) planned to turn villages into agro-industrial towns; when the plan '
           'was revived in 1988, villages began to be razed and the programme drew international protest.', old=True),
        'PM': F('nc_the_tenth_party_congress', 'The Tenth Party Congress', [
            stab(0.03), prog('political_power_factor', 0.05), fac('communist_cadres', 5), pop(0.03),
        ], 'The Romanian (1969) and Yugoslav (1974) tenth congresses confirmed their leaders\' lines and filled the central '
           'committees with loyal cadres.'),

        # ---------------- the economic model
        'ECO': F('nc_the_social_plan', 'The Social Plan', [
            prog('production_speed_buildings_factor', 0.05), prog('industrial_capacity_factory', 0.03),
            prog('production_speed_industrial_complex_factor', 0.05), fac('labour_unions', 5),
        ], 'Yugoslav "social plans" and Romanian five-year plans set investment priorities for the whole economy, '
           'outside Comecon\'s division of labour.'),
        'B1': F('nc_western_credits', 'Western Credits', [
            build('two_random_industrial_complex'), prog('receiving_investment_cost_modifier', -0.10),
            prog('research_speed_factor', 0.02), prog('consumer_goods_factor', -0.02), debt(0.02),
        ], 'Romania joined the IMF and World Bank (1972) and Yugoslavia borrowed heavily from Western banks: new plants '
           'quickly, and a debt crisis in the 1980s.'),
        'B2': F('nc_fortress_self_reliance', 'Fortress Self-Reliance', [
            prog('imp_sanction_resistance', 0.10), prog('foreign_influence_defense_modifier', 0.10),
            prog('drift_defence_factor', 0.10), prog('mdcw_cw_market_exposure', -0.10),
            prog('productivity_growth_modifier', -0.05),
            prog('trade_opinion_factor', -0.05),
        ], 'Albania\'s 1976 constitution banned foreign credits and concessions; after the break with China (1978) it '
           'stood alone, shielded from outside pressure but cut off from foreign technology.'),
        'B1f': F('nc_licensed_western_factories', 'Licensed Western Factories', [
            build('one_random_industrial_complex'), tech(['CAT_utility_vehicles', 'CAT_computing'], 0.35, 1),
            prog('research_speed_factor', 0.02), prog('industrial_capacity_factory', 0.03),
            prog('production_factory_efficiency_gain_factor', 0.05), prog('interest_rate_multiplier_modifier', 0.25),
        ], 'Dacia built Renaults under a 1966 licence, Zastava built Fiats and Oltcit (founded 1976) Citroëns; '
           'Western licences brought technology, paid for in hard currency.'),
        'B2f': F('nc_heavy_industry_first', 'Heavy Industry First', [
            build('one_random_industrial_complex'), build('one_random_arms_factory'),
            build('one_random_fossil_fuel_powerplant'), prog('industrial_capacity_factory', 0.03),
            fac('communist_cadres', 5), prog('consumer_goods_factor', 0.02),
        ], 'Albania\'s Chinese-built Elbasan steel works (1970s) and Romania\'s Galati steel plant put steel, power and '
           'arms ahead of consumer goods.'),
        'EM': F('nc_the_industrial_republic', 'The Industrial Republic', [
            growth(1), prog('production_factory_max_efficiency_factor', 0.03), fac('labour_unions', 5),
        ], 'Yugoslavia grew by about 6 % a year in the 1970s and Romania, by official figures, even faster, turning '
           'both into industrial countries within a generation.'),

        # ---------------- security and society
        'C1': F('nc_brotherhood_and_unity', 'Brotherhood and Unity', [
            prog('stability_factor', 0.04), prog('required_garrison_factor', -0.10), fac('all', 3), stab(0.02),
            timed('nc_self_governing_communes', 730, {'production_speed_buildings_factor': 0.05, 'bureaucracy_cost_multiplier_modifier': -0.07}, 'Self-Governing Communes'), prog('political_power_factor', -0.05),
        ], 'Yugoslavia\'s 1974 constitution gave its republics and provinces near-sovereign powers to keep the peace between '
           'its nations, weakening the centre.'),
        'C2': F('nc_the_state_security_apparatus', 'The State Security Apparatus', [
            prog('drift_defence_factor', 0.20), prog('intelligence_agency_defense', 0.20),
            prog('mdcw_cw_ideological_defence', 0.10), fac('intelligence_community', 10), law('increase_policing_budget'), prog('research_speed_factor', -0.02),
        ], 'Romania\'s Securitate and Albania\'s Sigurimi built dense informer networks and closely watched contacts '
           'with foreigners; the police budget grew and dissent was suppressed.'),
        'CM': F('nc_socialist_patriotism', 'Socialist Patriotism', [
            prog('war_support_factor', 0.05), prog('conscription_factor', 0.02), prog('army_morale_factor', 0.05),
            stab(0.03), pop(0.03),
        ], 'Ceausescu\'s July Theses (1971) mixed communism with national pride and history; independent communist states '
           'leaned on patriotism to stay united.'),

        # ---------------- foreign stance and arms
        'D1': F('nc_leader_of_the_non_aligned', 'Leader of the Non-Aligned', [
            prog('foreign_influence_modifier', 0.10), prog('mdcw_cw_support_effectiveness', 0.10),
            prog('trade_opinion_factor', 0.05), prog('mdcw_cw_assistance_capacity', 1), outlook('N', 0.03), money(-0.005),
        ], 'Tito co-founded the Non-Aligned Movement (Belgrade 1961) and was still its elder statesman at Havana (1979); '
           'summits, aid and prestige cost money.'),
        'D2': F('nc_the_maverick_between_the_blocs', 'The Maverick Between the Blocs', [
            prog('trade_opinion_factor', 0.10), prog('mdcw_cw_assistance_limit', 0.25), tension(-1),
            prog('receiving_investment_cost_modifier', -0.10), prog('foreign_influence_defense_modifier', -0.05),
        ], 'Ceausescu hosted Nixon (1969), kept ties to Israel and West Germany and won US most-favoured-nation status '
           '(1975), opening Romania to Western partners and their influence.'),
        'DM': F('nc_an_arms_industry_of_our_own', 'An Arms Industry of Our Own', [
            build('one_random_arms_factory'), tech(['CAT_main_battle_tanks', 'CAT_light_aircraft'], 0.35, 2),
            fac('defense_industry', 10), xp('army', 25),
        ], 'Yugoslavia and Romania jointly developed the Orao/IAR-93 jet (first flight 1974), and Yugoslavia built '
           'the M-84 tank under Soviet licence and its own warships, to reduce their dependence on either bloc.'),

        # ---------------- capstone
        'CAP': F('nc_general_people_s_defence', 'General People\'s Defence', [
            idea('nc_total_national_defence', {'army_core_defence_factor': 0.15, 'conscription_factor': 0.04,
                                               'defensive_war_stability_factor': 0.15, 'weekly_manpower': 300,
                                               'foreign_influence_defense_modifier': 0.05}, 'Total National Defence'),
            xp('army', 50), law('increase_military_spending'),
        ], 'After 1968 Yugoslavia (law of 1969) and Romania organised the whole population for territorial war so that no '
           'bloc could occupy them as the Warsaw Pact had occupied Czechoslovakia.', old=True),
    },
)

PARTIES = [NLIB, GR, NS, NC]
