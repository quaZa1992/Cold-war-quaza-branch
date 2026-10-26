# IMPERIA CW — Cold War: parts — S.
from dsl import *

# Salafist outlook trunk + Salafist Kingdom, Caliphate, Muslim Brotherhood (Non-Aligned outlook).

TRUNKS = [dict(
    outlook='S',
    title='The Islamic Awakening',
    note='The awakening chooses its base: the mosque networks (ulema, preaching, ideological defence) or the charitable '
         'societies (welfare, calm, a popular following). Either opens the Faithful Majority.',
    foci={
        'T0': F('champion_salafist', 'Champion the Islamic Awakening', [
            outlook('S', 0.05),
            timed('trunk_s_the_call', 730, {'fascism_drift': 0.05, 'mdcw_cw_ideological_defence': 0.10}, 'The Call'),
            fac('the_ulema', 5), fac('the_wahabi_ulema', 5),
        ], 'After 1967 the Islamic revival (al-sahwa) filled the space left by Arab nationalism; preachers, students and Gulf money spread it across the Muslim world.', old=True),
        'T1a': F('mosque_networks', 'Mosque Networks', [
            outlook('S', 0.03), fac('the_ulema', 10), fac('the_wahabi_ulema', 10),
            timed('trunk_s_mosque_networks', 730, {'drift_defence_factor': 0.15, 'fascism_drift': 0.03, 'research_speed_factor': -0.02}, 'The Mosque Networks'),
        ], 'The Muslim World League (1962) financed mosques, preachers and imams across Asia and Africa; the pulpit, more than the university, became the movement\'s school.', old=True),
        'T1b': F('charitable_societies', 'Charitable Societies', [
            outlook('S', 0.03), stab(0.03), fac('small_medium_business_owners', 5), literacy(0.01),
            timed('trunk_s_charitable_societies', 730, {'stability_factor': 0.03, 'social_cost_multiplier_modifier': -0.05, 'political_power_factor': -0.05}, 'The Charitable Societies'),
        ], 'Islamic charities such as Egypt\'s al-Jam\'iyya al-Shar\'iyya or Kuwait\'s Social Reform Society ran clinics and schools the state could not provide, and answered to their own boards, not to the government.', old=True),
        'T2': F('the_faithful_majority', 'The Faithful Majority', [
            outlook('S', 0.05), outlook('W', -0.02), fac('the_ulema', 5),
            timed('trunk_s_faithful_majority', 1095, {'drift_defence_factor': 0.10, 'mdcw_cw_ideological_defence': 0.15, 'stability_factor': 0.02}, 'The Faithful Majority'),
        ], 'By the late 1970s Islamist lists were winning student unions from Cairo to Kuala Lumpur, and in the 1980s Egypt\'s professional syndicates: the revival had become a mass movement.', old=True),
        'T3': F('an_islamic_government', 'An Islamic Government', [
            pp(75), stab(0.03),
            timed('trunk_s_islamic_mandate', 365, {'political_power_factor': 0.10, 'stability_factor': 0.03}, 'The Islamic Mandate'),
            note('+50 political power if The Faithful Majority is completed.'),
        ], 'Islamic governments of the period (Saudi Arabia, Pakistan after 1977, Sudan after 1983) claimed a religious mandate and governed largely by decree.', old=True),
    },
)]

PARTIES = [
    # ------------------------------------------------------------------ Salafist Kingdom
    dict(
        key='sk',
        title='The Custodian Kingdom',
        identity='A dynasty that rules through a bargain with the ulema: the clerics own society, the royal family owns the '
                 'state and the oil, and the money buys development.',
        history='Faisal\'s Saudi Arabia (1964-75) set the pattern: five-year plans from 1970, girls\' schools under clerical '
                'control, the religious police, Petromin and participation in Aramco, the 1973 oil embargo and pan-Islamic '
                'diplomacy (Muslim World League, OIC, Islamic Development Bank). After the 1979 Grand Mosque seizure the '
                'kingdom split the difference: more power to the ulema and a bigger National Guard.',
        foci={
            'E': F('sk_custodian_of_the_faith', 'Custodian of the Faith', [
                prog('stability_factor', 0.05), prog('drift_defence_factor', 0.10), prog('political_power_factor', 0.05),
                fac('the_wahabi_ulema', 10),
            ], 'Saudi kings ruled as protectors of the faith; the alliance of the House of Saud with the Wahhabi scholars was the founding bargain of the state.', old=True),

            # ---------------- the power question
            'POL': F('sk_the_royal_diwan', 'The Royal Diwan', [
                pp(100), stab(0.02), fac('the_ulema', 5), outlook('W', -0.02),
            ], 'Faisal centralised power in the Royal Diwan and the Council of Ministers after replacing King Saud in 1964; princes held the key ministries.'),
            'A1': F('sk_royal_modernisation', 'Royal Modernisation', [
                prog('research_speed_factor', 0.03), prog('production_speed_buildings_factor', 0.05), literacy(0.04),
                fac('small_medium_business_owners', 5), fac('the_wahabi_ulema', -10),
            ], 'Faisal backed state girls\' schools (1960) and introduced television (1965) despite clerical protest; modernisation came from the palace, and the ulema resented it.', old=True),
            'A2': F('sk_the_ulema_compact', 'The Ulema Compact', [
                prog('stability_factor', 0.05), prog('drift_defence_factor', 0.15), fac('the_wahabi_ulema', 10), fac('the_ulema', 5),
                prog('research_speed_factor', -0.02),
            ], 'The kingdom could also govern through the clerics: education, courts and morals stayed theirs in exchange for loyalty, at a cost to universities and science.', old=True),
            'A1f': F('sk_the_five_year_development_plan', 'The Five-Year Development Plan', [
                build('two_random_industrial_complex'), build('one_random_infrastructure'),
                prog('production_speed_buildings_factor', 0.05), fac('industrial_conglomerates', 5),
            ], 'The first Saudi five-year plan (1970-75) built roads, power and industry with oil money; the second (1975-80) planned almost 142 billion dollars of spending.', old=True),
            'A2f': F('sk_religious_police', 'Religious Police', [
                idea('sk_virtue_committees', {'mdcw_cw_ideological_defence': 0.20, 'drift_defence_factor': 0.10,
                                              'required_garrison_factor': -0.10}, 'The Virtue Committees', bound=True),
                prog('stability_factor', 0.02), fac('the_wahabi_ulema', 10),
                law('increase_policing_budget'), fac('small_medium_business_owners', -5),
            ], 'The Committee for the Promotion of Virtue and the Prevention of Vice (the mutawwi\'in) policed prayer times, dress and shops; merchants complained, but the streets stayed quiet.', old=True),
            'PM': F('sk_the_council_of_senior_scholars', 'The Council of Senior Scholars', [
                prog('political_power_factor', 0.05), prog('drift_defence_factor', 0.05), prog('bureaucracy_cost_multiplier_modifier', -0.05),
                stab(0.02), fac('the_ulema', 10),
            ], 'In 1971 the king founded the Council of Senior Scholars: the clerics gained an official voice, and the crown gained fatwas when it needed them.'),

            # ---------------- the economic model
            'ECO': F('sk_the_ministry_of_planning', 'The Ministry of Planning', [
                build('one_office_construction'), prog('tax_gain_multiplier_modifier', 0.05), fac('industrial_conglomerates', 5),
            ], 'Saudi Arabia upgraded its Central Planning Organisation (1965) to a Ministry of Planning in 1975 to spend the oil boom.'),
            'B1': F('sk_participation_in_the_concessions', 'Participation in the Concessions', [
                money(0.015), prog('resource_export_multiplier_modifier', 0.10), prog('corporate_tax_income_multiplier_modifier', 0.05),
                fac('fossil_fuel_industry', 10),
                prog('receiving_investment_cost_modifier', 0.10), fac('wall_street', -5),
            ], 'Under Yamani\'s "participation" (1972) the Gulf states bought into the foreign oil concessions step by step; revenues rose, and foreign capital grew wary.'),
            'B2': F('sk_recycle_the_petrodollars', 'Recycle the Petrodollars', [
                prog('return_on_investment_modifier', 0.015), prog('interest_rate_multiplier_modifier', -0.5),
                prog('office_park_income_tax_modifier', 0.10), fac('international_bankers', 10),
                prog('foreign_influence_defense_modifier', -0.05), prog('mdcw_cw_market_exposure', 0.05),
            ], 'After 1974 Saudi surpluses flowed into US Treasury bills and Western banks under a quiet agreement with Washington: high returns, tied to the Western market.'),
            'B1f': F('sk_national_petrochemicals', 'National Petrochemicals', [
                build('two_random_industrial_complex'), money(0.01), prog('resource_export_multiplier_modifier', 0.05),
                fac('fossil_fuel_industry', 10), corruption_chance(),
            ], 'SABIC (1976) and the new industrial cities of Jubail and Yanbu turned flared gas into petrochemicals owned by the state.'),
            'B2f': F('sk_the_sovereign_investment_fund', 'The Sovereign Investment Fund', [
                idea('sk_future_generations_fund', {'return_on_investment_modifier': 0.01, 'interest_rate_multiplier_modifier': -0.5,
                                                    'stability_factor': 0.02}, 'Fund for Future Generations'),
                build('one_office_construction'), fac('international_bankers', 5), money(-0.005),
            ], 'Kuwait\'s Fund for Future Generations and the Abu Dhabi Investment Authority (both 1976) saved oil money abroad for the day the wells ran dry.'),
            'EM': F('sk_the_development_boom', 'The Development Boom', [
                growth(1), prog('production_speed_buildings_factor', 0.05), fac('small_medium_business_owners', 5),
                law('decrease_migration_law'),
            ], 'The boom of 1974-81 brought cranes, contractors and more than a million foreign workers into the Gulf kingdoms.'),

            # ---------------- after the siege
            'C1': F('sk_the_ulema_bargain', 'The Ulema Bargain', [
                prog('stability_factor', 0.05), prog('drift_defence_factor', 0.10), prog('mdcw_cw_ideological_defence', 0.10),
                fac('the_wahabi_ulema', 10), stab(0.03), prog('research_speed_factor', -0.03),
            ], 'After the Grand Mosque seizure of November 1979 the government gave the clerics more money, more control over schools and the closure of cinemas; public life grew more restrictive for a generation.'),
            'C2': F('sk_expand_the_national_guard', 'Expand the National Guard', [
                prog('required_garrison_factor', -0.15), prog('intelligence_agency_defense', 0.15), prog('army_org_factor', 0.03),
                xp('army', 25), fac('the_military', 10),
                law('increase_military_spending'), prog('army_personnel_cost_multiplier_modifier', 0.05),
            ], 'The tribal National Guard, trained by the American firm Vinnell from 1975, was expanded after the 1979 siege as the regime\'s main internal security force.'),
            'CM': F('sk_the_kingdom_secured', 'The Kingdom Secured', [
                stab(0.05), prog('stability_factor', 0.02), prog('drift_defence_factor', 0.05),
                prog('mdcw_cw_ideological_defence', 0.05), fac('the_ulema', 5),
            ], 'By the early 1980s the monarchy had absorbed the shock of 1979 and the Shia unrest in the east; dissent went underground or abroad.'),

            # ---------------- allies and arms
            'D1': F('sk_the_american_umbrella', 'The American Umbrella', [
                tech(['CAT_medium_aircraft', 'CAT_surface_to_air_missiles'], 0.35, 2), prog('mdcw_cw_assistance_limit', 0.25), xp('air', 50),
                prog('foreign_influence_defense_modifier', -0.05), outlook('W', 0.02),
            ], 'The US-Saudi Joint Commission (1974), F-15s (1978) and AWACS (1981) made Washington the kingdom\'s protector, and gave it a say in Riyadh.'),
            'D2': F('sk_chequebook_diplomacy', 'Chequebook Diplomacy', [
                prog('foreign_influence_modifier', 0.15), prog('mdcw_cw_support_effectiveness', 0.10),
                prog('mdcw_cw_assistance_capacity', 1), fac('the_ulema', 10),
                money(-0.005), tension(1),
            ], 'Faisal championed the OIC (1969) and the Islamic Development Bank (agreed 1973), subsidised the frontline states and used the 1973 embargo: influence bought with money, at some risk.'),
            'DM': F('sk_the_petrodollar_arsenal', 'The Petrodollar Arsenal', [
                build('one_air_base'), build('one_anti_air'), tech('CAT_anti_air', 0.25, 1), xp('air', 25),
                prog('experience_gain_air_factor', 0.10),
            ], 'The Gulf monarchies spent billions on air bases, Hawk missiles and fighters in the 1970s; the air force was the prestige service of every royal family.'),

            # ---------------- capstone
            'CAP': F('sk_pan_islamic_solidarity', 'Pan-Islamic Solidarity', [
                idea('sk_custodian_kingdom', {'stability_factor': 0.05, 'political_power_factor': 0.10, 'drift_defence_factor': 0.15,
                                              'mdcw_cw_support_effectiveness': 0.10, 'research_speed_factor': -0.02},
                     'Pan-Islamic Solidarity', bound=True),
                prog('foreign_influence_modifier', 0.05), fac('the_wahabi_ulema', 10), outlook('S', 0.03),
            ], 'Faisal\'s pan-Islamism offered the Muslim world an alternative to Nasser\'s Arab socialism; it outlived him as the kingdom\'s foreign identity.', old=True),
        },
    ),

    # ------------------------------------------------------------------ Caliphate
    dict(
        key='cal',
        title='The Sharia State',
        identity='A revolutionary Islamist state that claims to rule by sharia alone: it trades openness and growth for '
                 'ideological unity, and must decide whether to build courts or mobilise the faithful.',
        history='No caliphate existed in the 1970s; the path is built on the Islamising states of the period: Zia ul-Haq\'s '
                'Pakistan (Hudood Ordinances 1979, Federal Shariat Court and zakat 1980, interest-free banking, the '
                'Majlis-e-Shura 1981), Nimeiry\'s September Laws in Sudan (1983), Libya\'s Islamic-revolutionary '
                'self-reliance after 1969, and the volunteer networks of the Afghan war in the 1980s.',
        foci={
            'E': F('cal_proclaim_the_caliphate', 'Proclaim the Caliphate', [
                prog('war_support_factor', 0.10), prog('conscription_factor', 0.05), prog('political_power_factor', 0.10),
                prog('drift_defence_factor', 0.20), fac('the_ulema', 10),
                prog('stability_factor', -0.05), prog('trade_opinion_factor', -0.10), tension(1),
            ], 'Islamising regimes began by proclaiming sharia the basis of law, as Zia did with the Hudood Ordinances in 1979 and Nimeiry in 1983; it rallied followers and alarmed neighbours and trade partners.', old=True),

            # ---------------- courts or mobilisation
            'POL': F('cal_the_consultative_council', 'The Consultative Council', [
                pp(100), prog('bureaucracy_cost_multiplier_modifier', -0.05), fac('the_ulema', 10),
            ], 'Zia replaced parliament with a nominated Majlis-e-Shura (1981): a consultative council of loyal notables and scholars instead of elected deputies.'),
            'A1': F('cal_sharia_courts', 'Sharia Courts', [
                prog('stability_factor', 0.05), prog('required_garrison_factor', -0.10), prog('drift_defence_factor', 0.10),
                fac('the_ulema', 10), prog('research_speed_factor', -0.03),
            ], 'Pakistan\'s Federal Shariat Court (1980) and Sudan\'s emergency "decisive justice" courts (1983-84) gave religious law priority over civil law; the regimes gained authority while legal and academic debate narrowed.', old=True),
            'A2': F('cal_the_holy_war', 'The Holy War', [
                prog('war_support_factor', 0.10), xp('army', 50), fac('foreign_jihadis', 10),
                prog('consumer_goods_factor', 0.03), tension(1),
            ], 'Some regimes ruled through permanent mobilisation instead of courts, framing every policy as a struggle for the faith; the barracks grew and the shops emptied.', old=True),
            'A1f': F('cal_religious_administration', 'Religious Administration', [
                prog('bureaucracy_cost_multiplier_modifier', -0.10), prog('political_power_factor', 0.05), prog('stability_factor', 0.02),
                fac('the_ulema', 10),
            ], 'A ministry of religious affairs and endowments (awqaf) and Pakistan\'s Council of Islamic Ideology brought religious scholars into the administration of the state.', old=True),
            'A2f': F('cal_foreign_volunteers', 'Foreign Volunteers', [
                prog('conscription_factor', 0.05), prog('weekly_manpower', 300), prog('army_morale_factor', 0.05),
                xp('army', 50), fac('foreign_jihadis', 10),
                prog('stability_factor', -0.02), prog('trade_opinion_factor', -0.05),
            ], 'The Afghan war drew thousands of volunteers through Peshawar\'s service bureaus in the 1980s; they brought fighters and zeal, and foreign suspicion.', old=True),
            'PM': F('cal_the_oath_of_allegiance', 'The Oath of Allegiance', [
                prog('political_power_factor', 0.05), stab(0.03), fac('the_ulema', 5),
                outlook('W', -0.03), outlook('E', -0.03),
            ], 'Rulers claiming religious authority expected the bay\'ah, the oath of allegiance: Nimeiry styled himself imam in 1984, and Pakistan banned all political parties from 1979 to 1985.'),

            # ---------------- the Islamic economy
            'ECO': F('cal_the_bait_al_mal', 'The Bait al-Mal', [
                prog('tax_gain_multiplier_modifier', 0.03), prog('corruption_cost_factor', -0.10), money(0.005), corruption(-1),
                fac('small_medium_business_owners', 5), fac('oligarchs', -5),
            ], 'Islamising states promised a treasury run on Islamic principles, on the model of the early bait al-mal, and an end to the corruption of the old order.'),
            'B1': F('cal_zakat_and_ushr', 'Zakat and Ushr', [
                prog('social_cost_multiplier_modifier', -0.10), prog('stability_factor', 0.03), prog('agriculture_tax_modifier', 0.10),
                fac('the_ulema', 5), fac('landowners', -10), fac('small_medium_business_owners', -5),
            ], 'Pakistan\'s Zakat and Ushr Ordinance (1980) deducted 2.5 % from bank savings and a tithe on harvests to fund welfare; landowners and savers paid.'),
            'B2': F('cal_abolish_riba', 'Abolish Riba', [
                money(0.01), prog('mdcw_cw_assistance_limit', 0.15), prog('receiving_investment_cost_modifier', -0.05),
                fac('small_medium_business_owners', 10), fac('the_ulema', 10),
                fac('international_bankers', -10), prog('productivity_growth_modifier', -0.03),
            ], 'Pakistan (from 1981) and Sudan (1984) began moving banking to interest-free profit sharing; Gulf-backed Islamic banks welcomed it, Western lenders grew wary.'),
            'B1f': F('cal_village_zakat_committees', 'Village Zakat Committees', [
                idea('cal_zakat_system', {'social_cost_multiplier_modifier': -0.05, 'stability_factor': 0.03, 'tax_gain_multiplier_modifier': 0.03},
                     'The Zakat System'),
                build('one_random_agriculture_district'), fac('farmers', 5),
            ], 'Pakistan created tens of thousands of local zakat committees that paid widows, orphans and students; the tithe on harvests funded village works.'),
            'B2f': F('cal_profit_and_loss_sharing', 'Profit-and-Loss Sharing', [
                build('one_office_construction'), prog('office_park_income_tax_modifier', 0.05), prog('return_on_investment_modifier', 0.005),
                prog('interest_rate_multiplier_modifier', -0.5), fac('small_medium_business_owners', 5),
            ], 'Interest-free banks financed trade through mudaraba and musharaka partnerships; the first Islamic banks of the late 1970s grew fast on pious savings.'),
            'EM': F('cal_the_just_economy', 'The Just Economy', [
                prog('production_speed_buildings_factor', 0.05), prog('social_cost_multiplier_modifier', -0.05), stab(0.02),
                fac('the_ulema', 5),
            ], 'The regime\'s economists promised a third way between capitalism and socialism, an economy of justice rather than growth.'),

            # ---------------- society
            'C1': F('cal_islamise_the_schools', 'Islamise the Schools', [
                literacy(0.03), prog('drift_defence_factor', 0.10), prog('mdcw_cw_ideological_defence', 0.10), stab(0.02),
                prog('education_cost_multiplier_modifier', -0.05), fac('the_ulema', 10), prog('research_speed_factor', -0.03),
            ], 'Zia\'s education policy Islamised curricula and channelled zakat money to a fast-growing madrasa sector in the 1980s, while science teaching lost ground.'),
            'C2': F('cal_gradual_islamisation', 'Gradual Islamisation', [
                stab(0.03), prog('productivity_growth_modifier', 0.10), prog('political_power_factor', 0.05), literacy(0.02),
                fac('small_medium_business_owners', 10), fac('the_ulema', -10), fac('foreign_jihadis', -5),
            ], 'Zia kept civil courts, technocrats and the business class alongside the new religious institutions; stricter Islamists criticised the compromise, and the economy kept growing.'),
            'CM': F('cal_a_society_of_believers', 'A Society of Believers', [
                stab(0.05), prog('stability_factor', 0.02), prog('drift_defence_factor', 0.05), outlook('S', 0.03),
                fac('the_ulema', 5),
            ], 'Within a decade the Islamising states had reshaped public life: prayer at work, religious broadcasting and new laws on family and morals.'),

            # ---------------- patrons or self-reliance
            'D1': F('cal_gulf_patronage', 'Gulf Patronage', [
                prog('mdcw_cw_assistance_limit', 0.25), money(0.01), build('one_random_infrastructure'),
                fac('the_wahabi_ulema', 10), prog('foreign_influence_defense_modifier', -0.05),
            ], 'Saudi and Gulf money helped fund Pakistan\'s madrasas and the Afghan resistance in the 1980s, and Gulf preachers came with it.'),
            'D2': F('cal_revolutionary_self_reliance', 'Revolutionary Self-Reliance', [
                prog('imp_sanction_resistance', 0.10), prog('foreign_influence_defense_modifier', 0.10), prog('mdcw_cw_ideological_defence', 0.10),
                timed('cal_economic_autarky', 730, {'industrial_capacity_factory': 0.05, 'resource_export_multiplier_modifier': 0.07}, 'Economic Autarky'), prog('trade_opinion_factor', -0.05), tension(1),
            ], 'Libya after 1969 expelled foreign bases, nationalised oil and declared an Islamic third way; independence came with isolation and sanctions.'),
            'DM': F('cal_the_army_of_the_faithful', 'The Army of the Faithful', [
                xp('army', 50), prog('army_morale_factor', 0.05), prog('conscription_factor', 0.03),
                tech(['CAT_small_arms', 'CAT_light_anti_tank'], 0.35, 1),
            ], 'Islamising regimes put chaplains, prayer and religious instruction into the army; Zia made the Pakistani army the guardian of the ideology of the state.'),

            # ---------------- capstone
            'CAP': F('cal_the_unbroken_banner', 'The Unbroken Banner', [
                idea('cal_unbroken_banner', {'political_power_factor': 0.10, 'drift_defence_factor': 0.20, 'war_support_factor': 0.05,
                                             'stability_factor': 0.03, 'trade_opinion_factor': -0.10}, 'The Unbroken Banner', bound=True),
                fac('the_ulema', 10), outlook('S', 0.05), xp('army', 25),
            ], 'The ideological state at its height: a single law, a single banner and a population mobilised for it, admired by its followers and isolated abroad.', old=True),
        },
    ),

    # ------------------------------------------------------------------ Muslim Brotherhood
    dict(
        key='mb',
        title='The Brotherhood in Power',
        identity='A mass Islamic movement of the pious middle class: it wins through charity, syndicates and the ballot, '
                 'and must choose between parliamentary coalitions and quiet control of the state from inside.',
        history='In the 1970s the Brotherhood came out of the prisons: Sadat released its leaders (1971-75) and let it publish again (1976); '
                'in Jordan it remained legal and loyal to the throne; in Sudan Turabi joined Nimeiry\'s government after the 1977 '
                'reconciliation and placed cadres in the state; Faisal Islamic Bank (1977) and Malaysia\'s ABIM (1971) built '
                'an Islamic economy and a student generation; in the 1980s the movement won Egypt\'s professional syndicates.',
        foci={
            'E': F('mb_islamic_democracy', 'Islamic Democracy', [
                prog('stability_factor', 0.03), prog('political_power_factor', 0.05), pop(0.05),
                fac('the_ulema', 10), fac('small_medium_business_owners', 5),
            ], 'Brotherhood movements argued that Islam and elections were compatible; where they could stand, as in Jordan or Kuwait, they won seats.', old=True),

            # ---------------- ballot or cadres
            'POL': F('mb_the_guidance_office', 'The Guidance Office', [
                pp(75), stab(0.02), prog('political_power_factor', 0.03), fac('the_ulema', 5), outlook('N', 0.02),
            ], 'The Brotherhood was run by its Guidance Office under the General Guide; in power, the movement\'s leadership sat beside the cabinet.'),
            'A1': F('mb_parliamentary_islam', 'Parliamentary Islam', [
                prog('stability_factor', 0.04), pop(0.05), prog('trade_opinion_factor', 0.10), fac('small_medium_business_owners', 5),
                prog('political_power_factor', -0.05),
            ], 'Jordan\'s Brotherhood worked within the parliamentary order and won 22 of 80 seats in 1989; coalition politics brought legitimacy and slow decisions.'),
            'A2': F('mb_the_tanzim', 'The Tanzim', [
                prog('political_power_factor', 0.10), prog('drift_defence_factor', 0.15), prog('bureaucracy_cost_multiplier_modifier', -0.05),
                fac('the_ulema', 5), fac('the_military', -10),
            ], 'Turabi\'s Islamic movement (from 1985 the National Islamic Front) built a disciplined organisation inside the Sudanese state after 1977; it worked, and the officers distrusted it.'),
            'A1f': F('mb_the_islamic_alliance', 'The Islamic Alliance', [
                pop(0.05), prog('party_popularity_stability_factor', 0.10), stab(0.03), prog('trade_opinion_factor', 0.05),
            ], 'In 1987 the Egyptian Brotherhood ran in an Islamic Alliance with the Labour and Liberal parties and became the largest opposition bloc.'),
            'A2f': F('mb_cadres_in_the_ministries', 'Cadres in the Ministries', [
                prog('bureaucracy_cost_multiplier_modifier', -0.15), prog('political_power_factor', 0.05), prog('drift_defence_factor', 0.10),
                prog('mdcw_cw_ideological_defence', 0.10), fac('intelligence_community', 5), corruption_chance(),
            ], 'Sudanese Islamists took posts in the judiciary, the Islamic banks and the civil service in the early 1980s; the network ran the state, and patronage followed.'),
            'PM': F('mb_reconciliation_with_the_state', 'Reconciliation with the State', [
                stab(0.03), prog('stability_factor', 0.02), prog('drift_defence_factor', 0.05), fac('the_military', 5), fac('the_ulema', 5),
            ], 'Sadat\'s releases (1971-75) and Nimeiry\'s national reconciliation (1977) ended years of persecution: for a time, the movement and the state made peace.'),

            # ---------------- charity or banking
            'ECO': F('mb_islamic_economics', 'An Islamic Economic Programme', [
                prog('tax_gain_multiplier_modifier', 0.03), prog('corruption_cost_factor', -0.10), prog('productivity_growth_modifier', 0.05),
                fac('small_medium_business_owners', 10),
            ], 'The first International Conference on Islamic Economics (Mecca, 1976) gave the Islamic movement an economic vocabulary of zakat, honest trade and interest-free finance.'),
            'B1': F('mb_charity_and_grassroots', 'Charity and Grassroots', [
                prog('social_cost_multiplier_modifier', -0.10), prog('health_cost_multiplier_modifier', -0.05),
                prog('stability_factor', 0.03), pop(0.03), fac('labour_unions', 5),
                money(-0.005),
            ], 'Brotherhood clinics, schools and relief committees reached the poor quarters faster than the state; it cost money and earned loyalty.', old=True),
            'B2': F('mb_islamic_banking', 'Islamic Banking', [
                prog('tax_gain_multiplier_modifier', 0.03), prog('return_on_investment_modifier', 0.005), money(0.01),
                fac('small_medium_business_owners', 10), fac('international_bankers', -10),
            ], 'Faisal Islamic Bank (Egypt and Sudan, 1977) collected the savings of the pious and of migrant workers in the Gulf; conventional banks lost deposits.', old=True),
            'B1f': F('mb_mosque_schools', 'Mosque Schools', [
                literacy(0.05), prog('education_cost_multiplier_modifier', -0.10), prog('drift_defence_factor', 0.05),
                fac('the_ulema', 5),
            ], 'Community schools and literacy classes attached to mosques spread in the 1970s and 1980s, teaching reading and carrying the movement\'s message.', old=True),
            'B2f': F('mb_the_pious_merchants', 'The Pious Merchants', [
                build('one_office_construction'), build('one_random_industrial_complex'),
                prog('office_park_income_tax_modifier', 0.05), prog('production_speed_buildings_factor', 0.03),
                fac('small_medium_business_owners', 5),
            ], 'Islamic investment companies and merchant networks financed workshops, trade and housing with the savings of the faithful.', old=True),
            'EM': F('mb_islamic_finance_houses', 'Islamic Finance Houses', [
                idea('mb_islamic_finance', {'return_on_investment_modifier': 0.005, 'interest_rate_multiplier_modifier': -0.5,
                                            'receiving_investment_cost_modifier': -0.05}, 'Islamic Finance'),
                fac('small_medium_business_owners', 5),
            ], 'By the early 1980s Islamic banks and finance houses were a sector of their own from Khartoum to Kuala Lumpur.'),

            # ---------------- society
            'C1': F('mb_public_morality_laws', 'Public Morality Laws', [
                prog('drift_defence_factor', 0.15), prog('mdcw_cw_ideological_defence', 0.10),
                prog('foreign_influence_defense_modifier', 0.10), stab(0.02), fac('the_ulema', 10),
                prog('trade_opinion_factor', -0.05), fac('small_medium_business_owners', -5),
            ], 'Islamists in parliament pressed for bans on alcohol and stricter dress rules, as in Kuwait and in Egypt\'s sharia debates of the late 1970s; tourism and business interests resisted.'),
            'C2': F('mb_win_the_syndicates', 'Win the Syndicates', [
                prog('research_speed_factor', 0.04), prog('productivity_growth_modifier', 0.10), pop(0.03), fac('labour_unions', 10),
                fac('the_ulema', -5), prog('drift_defence_factor', -0.05),
            ], 'Islamist doctors, engineers and lawyers took over Egypt\'s professional syndicates in the 1980s, and ABIM organised Malaysia\'s graduates: a modern, educated Islam.'),
            'CM': F('mb_the_student_generation', 'The Student Generation', [
                stab(0.03), prog('stability_factor', 0.02), prog('research_speed_factor', 0.02), literacy(0.02), pop(0.03),
                fac('small_medium_business_owners', 5),
            ], 'The Islamic student associations of the 1970s produced a generation of pious professionals who carried the movement into the middle class.'),

            # ---------------- abroad
            'D1': F('mb_gulf_remittances', 'Gulf Remittances', [
                money(0.01), prog('mdcw_cw_assistance_limit', 0.15), prog('population_tax_income_multiplier_modifier', 0.08),
                fac('small_medium_business_owners', 5), prog('foreign_influence_defense_modifier', -0.05),
            ], 'Millions of Egyptians, Sudanese and Jordanians worked in the Gulf after 1973; their remittances and Gulf donors helped fund the movement, and brought Gulf influence.'),
            'D2': F('mb_the_islamic_conference', 'The Islamic Conference', [
                prog('foreign_influence_modifier', 0.15), prog('trade_opinion_factor', 0.10), prog('foreign_influence_defense_modifier', 0.05),
                tension(-1), fac('the_military', -5), prog('war_support_factor', -0.03),
            ], 'Through the Organisation of the Islamic Conference (1969) governments could mediate between Muslim states and stay outside both blocs; the generals found it soft.'),
            'DM': F('mb_the_brotherhood_abroad', 'The Brotherhood Abroad', [
                idea('mb_international_organisation', {'mdcw_cw_support_effectiveness': 0.15, 'foreign_influence_modifier': 0.10},
                     'The International Organisation', bound=True),
                prog('mdcw_cw_assistance_capacity', 1), prog('drift_defence_factor', 0.05), fac('the_ulema', 5),
            ], 'The movement\'s international organisation, formalised in 1982, linked branches across the Arab world, Europe and Asia.'),

            # ---------------- capstone
            'CAP': F('mb_the_islamic_middle_way', 'The Islamic Middle Way', [
                idea('mb_middle_way', {'stability_factor': 0.05, 'political_power_factor': 0.05, 'productivity_growth_modifier': 0.05,
                                       'drift_defence_factor': 0.10, 'bureaucracy_cost_multiplier_modifier': 0.03},
                     'The Islamic Middle Way', bound=True),
                build('one_office_construction'), outlook('N', 0.03), pop(0.03), fac('the_ulema', 5),
            ], 'The movement\'s thinkers called it wasatiyya, the middle way between secularism and extremism: a pious, prosperous and electoral Islam.', old=True),
        },
    ),
]
