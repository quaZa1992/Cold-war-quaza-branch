# IMPERIA CW — Cold War: parts — E2.
from dsl import *

# Emerging outlook, part 2: Emerging Autocracy, Moderate Vilayat-e Faqih, Vilayat-e Faqih.
# The two Shia paths stay behind the existing GEN_1970_shia_path_allowed gate (entry foci unchanged).

PARTIES = [
# ======================================================================== Emerging Autocracy
dict(
    key='ea',
    title='The Revolutionary Command',
    identity='Officers and a single party make the revolution from above: a strongman rules through a command council, '
             'takes the economy into state hands and plays the superpowers against each other.',
    history='The 1970s officer-socialist regimes split the same ways: nationalisation (Iraq\'s oil 1972, Libya 1971-73) '
            'against opening (Sadat\'s Infitah 1974); party control of the army (Ba\'athist Iraq and Syria after 1970) against '
            'rule by a command council of officers (Libya\'s RCC, the Ethiopian Derg); people\'s militias against mass '
            'literacy campaigns (Iraq 1978, Somalia 1974); a Soviet friendship treaty (Iraq 1972, Somalia 1974) against '
            'sending the advisers home (Egypt 1972).',
    foci={
        'E': F('ea_the_revolutionary_command_council', 'The Revolutionary Command Council', [
            prog('political_power_factor', 0.08), prog('war_support_factor', 0.05),
            fac('the_military', 10), fac('communist_cadres', 5), law('increase_military_spending'),
        ], 'Post-coup regimes governed through a Revolutionary Command Council - Egypt 1952, Iraq 1968, Libya 1969 - and paid the army first.', old=True),

        # ---------------- the power question
        'POL': F('ea_one_party_one_revolution', 'One Party, One Revolution', [
            pp(100), pop(0.05), outlook('W', -0.03), outlook('N', -0.02),
        ], 'Egypt\'s Arab Socialist Union, Algeria\'s FLN and Somalia\'s Revolutionary Socialist Party (1976) channelled all politics into one organisation.'),
        'A1': F('ea_the_party_over_the_barracks', 'The Party Over the Barracks', [
            prog('stability_factor', 0.05), prog('drift_defence_factor', 0.15), pop(0.03), fac('communist_cadres', 10),
            fac('the_military', -10), prog('army_org_factor', -0.02),
        ], 'Ba\'athist Iraq after 1968 put party commissars into every unit and purged independent officers; the regime grew stable, the army less effective.'),
        'A2': F('ea_rule_of_the_command_council', 'Rule of the Command Council', [
            prog('war_support_factor', 0.05), prog('conscription_factor', 0.04), xp('army', 50), fac('the_military', 10),
            prog('bureaucracy_cost_multiplier_modifier', 0.05), prog('research_speed_factor', -0.02),
        ], 'Libya\'s RCC (1969) and Ethiopia\'s Derg (1974) kept power with the officers themselves; uniforms ran ministries that civil servants had run before.'),
        'A1f': F('ea_coup_proof_the_regime', 'Coup-Proof the Regime', [
            idea('ea_coup_proofing', {'stability_factor': 0.04, 'political_power_factor': 0.05, 'drift_defence_factor': 0.10,
                                      'army_attack_factor': -0.03}, 'Coup-Proofing', bound=True),
            prog('intelligence_agency_defense', 0.15), fac('intelligence_community', 10),
        ], 'After 1970 Assad and the Iraqi Ba\'ath built parallel guard units and party cells in every barracks; neither regime fell to a coup again.'),
        'A2f': F('ea_arms_for_the_revolution', 'Arms for the Revolution', [
            build('one_random_arms_factory'), tech(['CAT_armor', 'CAT_towed_artillery'], 0.35, 2), xp('army', 25),
            fac('defense_industry', 10), prog('army_personnel_cost_multiplier_modifier', 0.03),
        ], 'Libya\'s RCC spent oil money and the Derg Soviet credits on tanks and guns; by 1980 Ethiopia\'s army had grown into one of the largest in Africa.'),
        'PM': F('ea_a_national_charter', 'A National Charter', [
            prog('political_power_factor', 0.05), prog('bureaucracy_cost_multiplier_modifier', -0.05), stab(0.03),
            fac('communist_cadres', 5),
        ], 'Egypt\'s National Charter (1962), Syria\'s permanent constitution (1973) and Algeria\'s National Charter (1976) fixed the revolution in law.'),

        # ---------------- the economic model
        'ECO': F('ea_an_economy_for_the_revolution', 'An Economy for the Revolution', [
            prog('production_speed_buildings_factor', 0.05), prog('agricolture_productivity_modifier', 0.04), fac('farmers', 10),
        ], 'Land reform came early in the officers\' revolutions: Egypt 1952, Iraq 1958 and 1970, Ethiopia\'s nationalisation of rural land in 1975.'),
        'B1': F('ea_nationalise_foreign_assets', 'Nationalise Foreign Assets', [
            money(0.015), idea('ea_national_oil_company', {'resource_export_multiplier_modifier': 0.10,
                                                           'tax_gain_multiplier_modifier': 0.03}, 'The National Oil Company'),
            fac('communist_cadres', 10),
            prog('receiving_investment_cost_modifier', 0.10), fac('wall_street', -5),
        ], 'Iraq nationalised the Iraq Petroleum Company in June 1972 and Libya nationalised or took majority stakes in the foreign oil firms in 1971-74: a windfall, and Western capital grew wary.', old=True),
        'B2': F('ea_the_pragmatic_turn', 'The Pragmatic Turn', [
            prog('receiving_investment_cost_modifier', -0.15), prog('productivity_growth_modifier', 0.05),
            build('one_office_construction'), fac('communist_cadres', -10), outlook('W', 0.03),
        ], 'Sadat\'s Infitah (1974) opened Egypt to Western and Gulf capital; the party left protested and liberal ideas returned with the investors.', old=True),
        'B1f': F('ea_the_public_sector_commands', 'The Public Sector Commands', [
            build('two_random_industrial_complex'), prog('industrial_capacity_factory', 0.05),
            prog('production_speed_industrial_complex_factor', 0.05), fac('communist_cadres', 5),
            prog('productivity_growth_modifier', -0.03),
        ], 'Boumédiène\'s "industrialising industries" (1970-73 plan) put steel, petrochemicals and machinery under state companies such as Sonatrach and SNS.'),
        'B2f': F('ea_the_open_door', 'The Open Door', [
            build('two_office_construction'), prog('tax_gain_multiplier_modifier', 0.05), prog('trade_opinion_factor', 0.05),
            fac('small_medium_business_owners', 10), prog('mdcw_cw_market_exposure', 0.05),
        ], 'Egypt\'s Law 43 of 1974 created free zones and joint ventures; Gulf and Western money arrived, and so did the swings of the world market.', old=True),
        'EM': F('ea_a_revolutionary_five_year_plan', 'A Revolutionary Five-Year Plan', [
            growth(1), prog('production_speed_buildings_factor', 0.03), fac('communist_cadres', 5),
        ], 'Iraq\'s 1976-80 and Syria\'s 1976-80 plans poured the oil boom into factories, dams and roads.'),

        # ---------------- society and security
        'C1': F('ea_people_s_militias', "People's Militias", [
            prog('conscription_factor', 0.04), prog('army_core_defence_factor', 0.10), prog('war_support_factor', 0.03),
            prog('required_garrison_factor', -0.10), fac('the_military', -10),
        ], 'Iraq\'s Popular Army (1970), Libya\'s People\'s Militia and the Derg\'s militias armed party loyalists as a counterweight to the regular officers.', old=True),
        'C2': F('ea_the_national_literacy_drive', 'The National Literacy Drive', [
            literacy(0.06), prog('literacy_rate_education_modifier', 0.03), prog('research_speed_factor', 0.02), stab(0.02),
            fac('farmers', 5), money(-0.005),
        ], 'Iraq\'s compulsory literacy campaign (1978-80) and Somalia\'s 1974 rural campaign after the new script taught millions to read, at the treasury\'s expense.'),
        'CM': F('ea_the_popular_federations', 'The Popular Federations', [
            stab(0.04), pop(0.05), prog('drift_defence_factor', 0.10), prog('party_popularity_stability_factor', 0.05),
            fac('communist_cadres', 5),
        ], 'Party unions, youth leagues and women\'s federations (the General Federation of Iraqi Women, 1969) tied every part of society to the regime.'),

        # ---------------- arms and allies
        'D1': F('ea_the_treaty_of_friendship', 'The Treaty of Friendship', [
            tech(['CAT_aircraft', 'CAT_armor'], 0.35, 2), prog('mdcw_cw_assistance_limit', 0.25), xp('air', 50),
            prog('foreign_influence_defense_modifier', -0.05), tension(1),
        ], 'Iraq (1972), Somalia (1974) and Syria (1980) signed friendship treaties with Moscow: MiGs and T-62s on credit, and Soviet advisers in the staffs.'),
        'D2': F('ea_send_the_advisers_home', 'Send the Advisers Home', [
            prog('foreign_influence_defense_modifier', 0.10), prog('trade_opinion_factor', 0.10), stab(0.03),
            prog('training_time_army_factor', 0.05),
        ], 'In July 1972 Sadat ordered out some 15,000-20,000 Soviet military advisers; Egyptians cheered, Washington and the Gulf took note, and the army trained without them.'),
        'DM': F('ea_rebuild_the_army_of_the_revolution', 'Rebuild the Army of the Revolution', [
            xp('army', 50), build('one_anti_air'), tech(['CAT_surface_to_air_missiles', 'CAT_anti_tank'], 0.35, 1),
            prog('army_org_factor', 0.03), prog('army_personnel_cost_multiplier_modifier', 0.03),
        ], 'After 1967 Egypt and Syria rebuilt their armies around missile air defence and anti-tank infantry, the forces that crossed the Suez Canal and attacked on the Golan in October 1973.'),

        # ---------------- capstone
        'CAP': F('ea_the_leader_s_state', "The Leader's State", [
            idea('ea_the_leaders_state', {'political_power_factor': 0.10, 'stability_factor': 0.05, 'drift_defence_factor': 0.15,
                                          'war_support_factor': 0.05, 'research_speed_factor': -0.02}, "The Leader's State", bound=True),
            pop(0.05), fac('the_military', 5),
        ], 'By the late 1970s the revolutions had become personal states: Gaddafi\'s Jamahiriya (1977), Assad\'s Syria, Saddam\'s presidency (1979).', old=True),
    },
),

# ======================================================================== Moderate Vilayat-e Faqih
dict(
    key='mvf',
    title='The Republic of the Jurists and the Voters',
    identity='An Islamic republic in which the clergy guides but does not monopolise the state: elected bodies, a plural '
             'clergy and the bazaar share power.',
    history='The 1979 revolution had a moderate wing: Bazargan\'s provisional government, Grand Ayatollah Shariatmadari, '
            'Taleghani and later Montazeri; the bazaar-clergy alliance that financed it; the bonyads that inherited the '
            'Shah\'s assets. Lebanon\'s Amal (1974) worked as a Shia movement inside a plural system. '
            'The choices follow their real debates: elected bodies or clerical veto, bazaar or foundations, open '
            'universities or guided culture, normal neighbours or independence above all.',
    foci={
        'E': F('mvf_an_islamic_republic', 'An Islamic Republic', [
            prog('stability_factor', 0.04), prog('political_power_factor', 0.05), prog('drift_defence_factor', 0.10),
            fac('the_ulema', 10),
        ], 'The March 1979 referendum created an Islamic Republic with a broad coalition of clerics, liberals and the bazaar behind it.', old=True),

        # ---------------- the power question
        'POL': F('mvf_a_constitution_for_the_republic', 'A Constitution for the Republic', [
            pp(75), stab(0.03), pop(0.04),
        ], 'The Assembly of Experts drafted a constitution joining an elected president and Majlis to clerical guardianship, approved by referendum in December 1979.'),
        'A1': F('mvf_clerical_pluralism', 'Clerical Pluralism', [
            prog('stability_factor', 0.04), prog('research_speed_factor', 0.03), prog('trade_opinion_factor', 0.05),
            prog('party_popularity_stability_factor', 0.05),
            prog('foreign_influence_defense_modifier', -0.05), fac('the_ulema', -5),
        ], 'Grand Ayatollahs such as Shariatmadari wanted elected government with the clergy as advisers; in 1979-80 parties, papers and candidates still competed.', old=True),
        'A2': F('mvf_guardian_council_oversight', 'Guardian Council Oversight', [
            prog('political_power_factor', 0.10), prog('drift_defence_factor', 0.15), prog('mdcw_cw_ideological_defence', 0.10),
            fac('the_ulema', 10),
            prog('research_speed_factor', -0.02), fac('small_medium_business_owners', -5),
        ], 'The Guardian Council (1980) checked every law against Islamic law and the constitution, giving the jurists a veto over the elected Majlis.', old=True),
        'A1f': F('mvf_a_sovereign_majlis', 'A Sovereign Majlis', [
            idea('mvf_republican_institutions', {'stability_factor': 0.03, 'bureaucracy_cost_multiplier_modifier': -0.05,
                                                 'research_speed_factor': 0.02, 'political_power_factor': -0.03}, 'Republican Institutions'),
            stab(0.04), pop(0.04),
        ], 'Iran\'s first Majlis (1980) and the 1980 presidential election, won by a lay economist, showed a republic with real contests.'),
        'A2f': F('mvf_an_expediency_council', 'An Expediency Council', [
            prog('political_power_factor', 0.05), prog('bureaucracy_cost_multiplier_modifier', -0.10), stab(0.03),
            fac('the_ulema', 5),
        ], 'When the Guardian Council blocked the Majlis\' land and labour laws, Khomeini created the Expediency Council in 1988 to settle such deadlocks.'),
        'PM': F('mvf_rule_of_law_over_the_committees', 'Rule of Law over the Committees', [
            prog('stability_factor', 0.03), prog('police_cost_multiplier_modifier', -0.10), fac('the_ulema', 5),
        ], 'Bazargan\'s government tried in 1979 to bring the neighbourhood revolutionary committees under the police and the courts.'),

        # ---------------- the economic model
        'ECO': F('mvf_an_economy_without_usury', 'An Economy Without Usury', [
            prog('production_speed_buildings_factor', 0.03), prog('interest_rate_multiplier_modifier', -0.5),
            prog('tax_gain_multiplier_modifier', 0.03), fac('the_ulema', 5), fac('small_medium_business_owners', 5),
        ], 'Baqir al-Sadr\'s Iqtisaduna (1961) set out an Islamic economy between capitalism and socialism; Iran replaced interest-based banking in 1983.'),
        'B1': F('mvf_the_bazaar_economy', 'The Bazaar Economy', [
            fac('small_medium_business_owners', 10), prog('tax_gain_multiplier_modifier', 0.05), prog('trade_opinion_factor', 0.10),
            prog('productivity_growth_modifier', 0.05),
            prog('corruption_cost_factor', 0.10), fac('labour_unions', -5),
        ], 'The Tehran bazaar financed the revolution and expected free trade, light taxes and the protection of private property in return.', old=True),
        'B2': F('mvf_revolutionary_foundations', 'Revolutionary Foundations', [
            prog('social_cost_multiplier_modifier', -0.10), stab(0.03), money(0.01),
            corruption_chance(), fac('small_medium_business_owners', -5),
        ], 'The Foundation of the Oppressed (1979) took over the Pahlavi Foundation\'s assets to fund the poor, answering to no ministry.', old=True),
        'B1f': F('mvf_the_merchants_guilds', "The Merchants' Guilds", [
            build('two_office_construction'), prog('office_park_income_tax_modifier', 0.05), prog('trade_opinion_factor', 0.05),
            fac('small_medium_business_owners', 5),
        ], 'Bazaar guilds and merchant networks close to the clergy controlled much of the import trade and informal credit, keeping goods moving through revolution and war.'),
        'B2f': F('mvf_factories_of_the_disinherited', 'Factories of the Disinherited', [
            build('two_random_industrial_complex'), prog('social_cost_multiplier_modifier', -0.05), prog('health_cost_multiplier_modifier', -0.05), stab(0.02), pop(0.03),
            prog('bureaucracy_cost_multiplier_modifier', 0.05),
        ], 'The foundations ran hundreds of confiscated factories, hotels and farms and employed tens of thousands of the revolution\'s supporters.'),
        'EM': F('mvf_construction_jihad', 'Construction Jihad', [
            build('one_random_infrastructure'), prog('agricolture_productivity_modifier', 0.04), fac('farmers', 10),
        ], 'Construction Jihad (1979) sent volunteers to build roads, wells and power lines in the villages the old regime had neglected.'),

        # ---------------- society and culture
        'C1': F('mvf_reopen_the_universities', 'Reopen the Universities', [
            prog('research_speed_factor', 0.04), literacy(0.05), prog('literacy_rate_education_modifier', 0.03), stab(0.02),
            fac('the_ulema', -5), money(-0.005),
        ], 'Moderates pressed to reopen the universities closed in 1980 and to keep their secular faculty; they reopened in 1982-83.'),
        'C2': F('mvf_the_ministry_of_guidance', 'The Ministry of Guidance', [
            prog('stability_factor', 0.04), prog('drift_defence_factor', 0.10), prog('mdcw_cw_ideological_defence', 0.10),
            fac('the_ulema', 10), pop(0.04),
            prog('research_speed_factor', -0.02), prog('trade_opinion_factor', -0.05),
        ], 'The Ministry of Islamic Guidance (later Culture and Islamic Guidance) licensed books, films and newspapers, shaping public life through censorship rather than force.'),
        'CM': F('mvf_islamic_civil_society', 'Islamic Civil Society', [
            stab(0.04), pop(0.04), fac('the_ulema', 5),
            idea('mvf_islamic_associations', {'party_popularity_stability_factor': 0.05,
                                              'social_cost_multiplier_modifier': -0.05}, 'Islamic Associations'),
        ], 'Mosque associations, Islamic societies and charity funds gave the republic a social base that reached beyond the state.'),

        # ---------------- foreign stance and defence
        'D1': F('mvf_independence_before_alliances', 'Independence Before Alliances', [
            prog('foreign_influence_defense_modifier', 0.10), prog('mdcw_cw_ideological_defence', 0.10),
            prog('imp_sanction_resistance', 0.10), build('one_random_arms_factory'),
            prog('trade_opinion_factor', -0.10),
        ], '"Neither East nor West" (1979) refused both blocs; the republic paid in lost trade and spare parts and built its own workshops instead.'),
        'D2': F('mvf_good_neighbourliness', 'Good Neighbourliness', [
            prog('trade_opinion_factor', 0.10), prog('receiving_investment_cost_modifier', -0.10), build('one_office_construction'),
            tension(-1),
            fac('the_ulema', -5), prog('drift_defence_factor', -0.05),
        ], 'Bazargan\'s government kept trade and diplomatic ties with the neighbours and even the West in 1979, until the hostage crisis ended the course.'),
        'DM': F('mvf_trust_the_regular_army', 'Trust the Regular Army', [
            xp('army', 50), prog('army_org_factor', 0.03), fac('the_military', 10),
            tech(['CAT_helicopters', 'CAT_anti_tank'], 0.25, 2),
        ], 'Bazargan and Banisadr relied on the regular army rather than the new militias, and the regular army bore much of the early fighting after September 1980.'),

        # ---------------- capstone
        'CAP': F('mvf_islamic_social_justice', 'Islamic Social Justice', [
            idea('mvf_islamic_social_justice', {'stability_factor': 0.05, 'social_cost_multiplier_modifier': -0.10,
                                                'political_power_factor': 0.05, 'monthly_population': 0.05,
                                                'tax_gain_multiplier_modifier': -0.03}, 'Islamic Social Justice'),
            pop(0.05), fac('the_ulema', 5), fac('farmers', 5),
        ], 'The republic\'s founding promise was justice for the mostaz\'afin, the disinherited: subsidies, rural electrification and welfare paid by oil and the foundations.', old=True),
    },
),

# ======================================================================== Vilayat-e Faqih
dict(
    key='vf',
    title='The Guardianship of the Jurist',
    identity='The jurist rules: one guardian above all elected bodies, revolutionary guards beside the army and a '
             'revolution meant to be carried beyond the borders.',
    history='Khomeini\'s lectures on Velayat-e Faqih (1970) shaped the 1979 constitution; the Revolutionary Guards (1979) '
            'and the Basij (1980) built a parallel military; the Cultural Revolution closed the universities (1980-83); '
            'the banks were nationalised and the foundations inherited the old elite\'s wealth; rationing fed the war '
            'economy; Guards instructors went to Lebanon in 1982 while the state bought arms from any seller.',
    foci={
        'E': F('vf_guardianship_of_the_jurist', 'Guardianship of the Jurist', [
            prog('drift_defence_factor', 0.20), prog('political_power_factor', 0.10), prog('mdcw_cw_ideological_defence', 0.10),
            fac('the_ulema', 10), prog('research_speed_factor', -0.02),
        ], 'Khomeini\'s 1970 lectures in Najaf argued that a just jurist must govern in the absence of the Imam; the 1979 constitution made it law.', old=True),

        # ---------------- the power question
        'POL': F('vf_the_office_of_the_supreme_leader', 'The Office of the Supreme Leader', [
            pp(100), stab(0.03), outlook('W', -0.03), outlook('N', -0.03),
        ], 'The 1979 constitution placed the guardian jurist above president and Majlis, commanding the armed forces and appointing the top judges.'),
        'A1': F('vf_the_revolutionary_guard', 'The Revolutionary Guard', [
            prog('conscription_factor', 0.05), prog('army_morale_factor', 0.05), xp('army', 50), fac('iranian_quds_force', 10),
            fac('the_military', -10), prog('army_personnel_cost_multiplier_modifier', 0.05),
        ], 'The Revolutionary Guard Corps (May 1979) was built beside the distrusted regular army; the two competed for men, money and weapons all through the 1980s.', old=True),
        'A2': F('vf_islamisation_of_society', 'Islamisation of Society', [
            fac('the_ulema', 10), prog('stability_factor', 0.05), prog('mdcw_cw_ideological_defence', 0.10),
            prog('party_popularity_stability_factor', 0.05), pop(0.05),
            prog('research_speed_factor', -0.02), prog('trade_opinion_factor', -0.05),
        ], 'Dress codes, Islamic courts and the purge of secular officials (1980-81) remade public life; trade partners and the professional class drew back.', old=True),
        'A1f': F('vf_mobilise_the_basij', 'Mobilise the Basij', [
            prog('war_support_factor', 0.08), prog('conscription_factor', 0.05), prog('defensive_war_stability_factor', 0.15),
            prog('consumer_goods_factor', 0.02),
        ], 'The Basij (1980) organised millions of volunteers - students, villagers, the elderly - and sent them to the front in the war with Iraq.', old=True),
        'A2f': F('vf_cultural_councils', 'Cultural Councils', [
            idea('vf_cultural_revolution', {'drift_defence_factor': 0.10, 'mdcw_cw_ideological_defence': 0.15,
                                            'research_speed_factor': -0.03}, 'The Cultural Revolution', bound=True),
            prog('drift_defence_factor', 0.15), prog('stability_factor', 0.03), fac('the_ulema', 10),
        ], 'The Cultural Revolution Headquarters (1980) kept the universities closed until 1982-83 and rewrote curricula; councils kept watch over schools and media afterwards.', old=True),
        'PM': F('vf_the_revolutionary_courts', 'The Revolutionary Courts', [
            prog('political_power_factor', 0.05), prog('drift_defence_factor', 0.10), stab(0.02), fac('the_ulema', 5),
        ], 'Revolutionary courts tried the old regime\'s officials and then the new regime\'s opponents, outside the ordinary judiciary.'),

        # ---------------- the economic model
        'ECO': F('vf_the_banks_belong_to_the_revolution', 'The Banks Belong to the Revolution', [
            money(0.01), prog('interest_rate_multiplier_modifier', -0.5), prog('production_speed_buildings_factor', 0.03),
            fac('international_bankers', -5),
        ], 'In June 1979 Iran nationalised all private banks and insurers, and then large industry, putting credit under revolutionary control.'),
        'B1': F('vf_the_foundations_inherit', 'The Foundations Inherit', [
            money(0.015), build('one_random_industrial_complex'), prog('social_cost_multiplier_modifier', -0.05), fac('the_ulema', 5),
            corruption_chance(), prog('corruption_cost_factor', 0.10),
        ], 'The Foundation of the Oppressed and other bonyads took over the old elite\'s confiscated assets and ran them largely tax-free and without public audit.'),
        'B2': F('vf_the_coupon_economy', 'The Coupon Economy', [
            prog('consumer_goods_factor', -0.03), prog('industrial_capacity_factory', 0.05), stab(0.03),
            prog('social_cost_multiplier_modifier', -0.05), pop(0.03),
            prog('productivity_growth_modifier', -0.05), fac('small_medium_business_owners', -10),
        ], 'From 1980 the government rationed basic goods with coupons and fixed prices: the poor were fed, the bazaar was squeezed.'),
        'B1f': F('vf_the_foundations_empire', "The Foundations' Empire", [
            build('two_random_industrial_complex'), build('one_office_construction'),
            prog('production_speed_buildings_factor', 0.05), fac('the_ulema', 5),
            prog('corruption_cost_factor', 0.05),
        ], 'By the mid-1980s the Foundation of the Oppressed was one of the largest conglomerates in the Middle East: factories, shipping and real estate.'),
        'B2f': F('vf_self_sufficiency_in_wartime', 'Self-Sufficiency in Wartime', [
            build('one_random_arms_factory'),
            idea('vf_wartime_self_sufficiency', {'imp_sanction_resistance': 0.15, 'production_speed_arms_factory_factor': 0.05,
                                                 'agricolture_productivity_modifier': 0.04}, 'Wartime Self-Sufficiency'),
            prog('trade_opinion_factor', -0.05),
        ], 'Under the US embargo (1979) the planners pushed self-sufficiency in food, spare parts and munitions, rebuilding plants foreign suppliers had serviced.'),
        'EM': F('vf_the_martyrs_foundation', "The Martyrs' Foundation", [
            prog('stability_factor', 0.03), prog('war_support_factor', 0.03), pop(0.03), fac('the_ulema', 5),
        ], 'The Martyrs\' Foundation (1980) gave housing, pensions and university places to the families of the war dead, binding them to the state.'),

        # ---------------- society and security
        'C1': F('vf_the_revolutionary_committees', 'The Revolutionary Committees', [
            prog('drift_defence_factor', 0.10), prog('intelligence_agency_defense', 0.20), prog('required_garrison_factor', -0.10),
            fac('intelligence_community', 10),
            law('increase_policing_budget'), stab(-0.02),
        ], 'Neighbourhood committees (1979) policed morality and pursued opponents street by street until they were merged into the police in 1991.'),
        'C2': F('vf_friday_prayer_networks', 'Friday Prayer Networks', [
            prog('stability_factor', 0.04), prog('war_support_factor', 0.03), pop(0.04), fac('the_ulema', 10), literacy(0.02),
            money(-0.005),
        ], 'Friday prayer leaders appointed in every city and state-funded seminaries carried the leadership\'s message into every neighbourhood.'),
        'CM': F('vf_defend_the_revolution_s_values', "Defend the Revolution's Values", [
            mdidea('idea_focus_generic_counter_terrorism'), stab(0.03), prog('mdcw_cw_ideological_defence', 0.10),
            prog('intelligence_agency_defense', 0.10), fac('the_ulema', 5),
        ], 'After the 1981 bombings killed the president, the prime minister and dozens of officials, the regime built the security apparatus that broke the armed opposition.'),

        # ---------------- foreign stance and arms
        'D1': F('vf_aid_the_oppressed_abroad', 'Aid the Oppressed Abroad', [
            prog('mdcw_cw_support_effectiveness', 0.10), prog('foreign_influence_modifier', 0.10),
            prog('mdcw_cw_assistance_capacity', 1), fac('iranian_quds_force', 10), xp('army', 25),
            tension(1), prog('trade_opinion_factor', -0.05),
        ], 'Guards instructors went to Lebanon\'s Bekaa valley in 1982 and Tehran hosted Iraqi, Gulf and Afghan Shia exiles, at the price of regional isolation.'),
        'D2': F('vf_arms_from_any_seller', 'Arms from Any Seller', [
            tech(['CAT_anti_tank', 'CAT_surface_to_air_missiles'], 0.50, 2), prog('mdcw_cw_assistance_limit', 0.25),
            prog('trade_opinion_factor', 0.05),
            fac('the_ulema', -5), prog('mdcw_cw_ideological_defence', -0.05),
        ], 'During the war Iran bought weapons from North Korea, China, Libya and - secretly - Israel and the United States (Iran-Contra, 1985-86): the front came before ideology.'),
        'DM': F('vf_the_defence_industries_organisation', 'The Defence Industries Organisation', [
            xp('army', 50), build('one_random_arms_factory'), prog('army_morale_factor', 0.05),
            tech(['CAT_light_anti_tank', 'CAT_small_arms'], 0.25, 2),
            prog('army_personnel_cost_multiplier_modifier', 0.03),
        ], 'The Defence Industries Organisation and the Guards\' own workshops expanded production of rockets, mortars and small arms in the 1980s to outlast the embargo.'),

        # ---------------- capstone
        'CAP': F('vf_export_the_revolution', 'Export the Revolution', [
            idea('vf_revolution_without_borders', {'drift_defence_factor': 0.15, 'mdcw_cw_support_effectiveness': 0.20,
                                                   'war_support_factor': 0.05, 'political_power_factor': 0.05,
                                                   'trade_opinion_factor': -0.10}, 'The Revolution Without Borders', bound=True),
            stab(0.03), pop(0.05), fac('iranian_quds_force', 10), xp('army', 25), tension(1),
        ], 'The 1979 constitution pledged support for the oppressed everywhere; Guards units abroad and allied movements made it policy, and the neighbours armed against it.', old=True),
    },
),
]
