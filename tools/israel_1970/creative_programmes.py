# IMPERIA COLD WAR — Israel 1970 institutional programmes and opportunity costs.
"""Authored revision applied after the legacy narrative layer.

Historical institutions motivate the choices; all numerical effects are game
balance proposals, not measurements of a historical policy's causal effects.
Unhistorical governments retain their existing explicit alternative-history
status, political gates, assets and constitutional decisions.
"""

RESEARCH = [
    ('Bank of Israel, Annual Report 1970, published 1971-05-31',
     'https://www.boi.org.il/22165?culture=en',
     'Contemporaneous sector accounts and the public-finance setting.'),
    ('Knesset, 1969/70 budget record',
     'https://main.knesset.gov.il/About/pages/budget/budgethistorypage.aspx?budget=21',
     'Supplementary appropriations tied defence, housing and export promotion together.'),
    ('Mekorot, Our History and Visitors Center',
     'https://www.mekorot-int.com/our-history/',
     'The national carrier preceded 1970; expansion means pumps, irrigation and maintenance.'),
    ('Technion, Faculty of Computer Science anniversary, 2019-11-07',
     'https://www.technion.ac.il/en/blog/2019/11/50-years-for-technions-faculty-of-computer-science/',
     'A computer-science faculty began in 1969; its first class graduated in 1972.'),
    ('Technion, History', 'https://www.technion.ac.il/en/the-history-of-the-technion/',
     'Medicine expanded in 1969, followed by biology in 1971.'),
    ('Israel Ministry of Defense, Merkava and Armored Vehicles Directorate',
     'https://www.mod.gov.il/en/departments/merkava-and-armored-vehicles-directorate',
     'The 1970 domestic tank decision used existing repair and industrial capacity.'),
    ('Israel Ministry of Defense Archives, General Israel Tal',
     'https://archives.mod.gov.il/sites/English/Exhibitions/Pages/General-Israel-Tal.aspx',
     'Crew protection and comparative development informed the tank programme.'),
    ('Israel Aerospace Industries, History', 'https://www.iai.co.il/about/history/',
     'Gabriel in 1964, ELTA in 1967, and Arava development before 1970 support period research.'),
    ('Israel Democracy Institute, The Black Panthers',
     'https://en.idi.org.il/israeli-elections-and-parties/parties/black-panthers/',
     'The movement was founded in 1971; existing protest timing must remain intact.'),
    ('Bank of Israel, Annual Report 1975, labour force table XII-4',
     'https://www.boi.org.il/media/4yylac4w/pe_12.pdf',
     'Retrospective CBS surveys document low female participation around 1970. Participation reforms below are selectable balance proposals, not claimed historical gains.'),
]


def enrich(specs):
    from revised_rewards import money, tech, xp, opinion, pp, stab

    def edit(key, label=None, body=None, mods=None, code=None, extra=''):
        row = specs[key]
        if label is not None: row['label'] = label
        if body is not None: row['body'] = body
        if mods is not None: row['mods'] = mods
        if code is not None: row['code'] = code
        if extra: row['code'] += '\n' + extra

    # Shared programmes: productive capacity is paid for, and institutions compete
    # for engineering, public funds and ministerial attention. These remain earned
    # national institutions; party-owned programmes below switch with government.
    edit('unity_cabinet', 'A Cabinet across the Party Lines',
         'A broad coalition can distribute responsibility for national security across the major parties. Its members will expect a say in appointments and spending, slowing the passage of a common legislative programme.',
         {'stability_factor': .05, 'political_power_factor': -.03, 'planning_speed': .05})
    edit('narrow_cabinet', 'A Disciplined Parliamentary Majority',
         'A smaller coalition gives ministers clearer authority over the legislative agenda. Dependence on fewer parliamentary partners leaves the government more exposed to every dispute within its majority.',
         {'political_power_factor': .10, 'stability_factor': -.02})
    edit('civil_service', 'The Civil Service Commission',
         'Merit examinations and common personnel standards can make a young state less dependent on party appointments. Professional administration will be cheaper to sustain, but the coalition will lose some of the patronage through which it has held together.',
         {'bureaucracy_cost_multiplier_modifier': -.08, 'political_power_factor': -.02},
         code=tech('industry', .25))
    edit('local_councils', 'Municipal Engineering Offices',
         'Local councils know which roads and service connections their communities need. Permanent engineering offices will speed municipal works while adding a modest standing administrative commitment.',
         {'production_speed_infrastructure_factor': .15, 'bureaucracy_cost_multiplier_modifier': .02})
    edit('central_planning', 'Sapir\'s Development Tenders',
         'Central tenders can concentrate scarce engineers and capital on projects that private investors would otherwise overlook. The same priority system gives established contractors greater protection from competition.',
         {'production_speed_buildings_factor': .07, 'receiving_investment_cost_modifier': .04})
    edit('water', 'Pumps for the National Water Carrier',
         'The National Water Carrier already links northern water sources to the south. New pumping equipment and irrigation connections can support more cultivation, provided the treasury accepts the cost of operating an increasingly complex network.',
         {'production_speed_agriculture_district_factor': .15, 'industry_repair_factor': .05,
          'bureaucracy_cost_multiplier_modifier': .015}, extra=money(.004))
    edit('water_maintenance', 'Mekorot\'s Workshops and Reservoirs',
         'A water network is only as dependable as its pumps, repair crews and reserve storage. Dedicated workshops will restore damaged utilities more quickly and protect investment in irrigation, at the price of a continuing maintenance establishment.',
         {'industry_repair_factor': .15, 'production_speed_agriculture_district_factor': .05,
          'bureaucracy_cost_multiplier_modifier': .01}, extra=tech('energy_efficiency', .25))
    edit('exports', 'Diamonds, Citrus and Precision Workshops',
         'Established exporters can introduce smaller workshops to overseas orders and commercial credit. A stronger export network will draw investment into services while making those firms more sensitive to conditions beyond Israel.',
         {'production_speed_offices_factor': .10, 'receiving_investment_cost_modifier': -.06,
          'mdcw_cw_market_exposure': .04})
    edit('import_substitution', 'Produce What the Embargo Denies',
         'Local production of essential components can cushion the effects of an embargo. Protected suppliers will keep more work at home, but sheltering them from competition makes commercial investment less attractive.',
         {'imp_sanction_resistance': .15, 'production_factory_max_efficiency_factor': .05,
          'receiving_investment_cost_modifier': .06}, extra=tech('industry', .25))
    edit('export_specialization', 'An Economy of Specialist Exporters',
         'A small domestic market cannot absorb every product of modern engineering. Specialised exporters will gain from international investment and orders, while relying more heavily on access to foreign customers.',
         {'return_on_investment_modifier': .005, 'receiving_investment_cost_modifier': -.10,
          'mdcw_cw_market_exposure': .12}, extra=tech('electronics', .25))
    edit('diaspora_bonds', 'Israel Bonds Development Offices',
         'Diaspora subscription campaigns can connect long-term investors to national development. Professional offices will improve the use of that capital, while continuing campaigns and reporting require a standing administrative staff.',
         {'imp_investment_reward': .10, 'bureaucracy_cost_multiplier_modifier': .015},
         code=opinion('small_medium_business_owners', 10))
    edit('civil_electronics', 'ELTA\'s Civilian Suppliers',
         'An expanding electronics sector can give civilian workshops access to testing and production skills. Reserving some engineering capacity for civilian applications means defence orders will have to compete with a broader industrial programme.',
         {'productivity_growth_modifier': .08, 'production_factory_efficiency_gain_factor': .05,
          'production_speed_arms_factory_factor': -.03}, extra=money(.005))
    edit('technion', 'The Technion\'s New Computing Faculty',
         'The new computer-science faculty gives Israel a place to train specialists for research and industrial work. Sustained support for laboratories and academic staff will broaden technical capability, with higher education becoming a larger public commitment.',
         {'research_speed_factor': .025, 'education_cost_multiplier_modifier': .04},
         code=money(.006)+'\n'+tech('electronics', .5, 2))
    edit('sme_credit', 'Credit beyond the Large Enterprises',
         'Small workshops and family firms need credit outside the networks of the largest public and private employers. Loan guarantees can broaden commercial opportunity, while exposing the public administration to supervision and recovery costs.',
         {'receiving_investment_cost_modifier': -.08, 'production_speed_offices_factor': .08,
          'bureaucracy_cost_multiplier_modifier': .015})
    edit('fiscal_review', 'Sapir\'s Budget Conference',
         'Defence orders, immigrant housing and industrial investment all compete for the same public funds. A common budget conference will identify priorities before the cabinet chooses between credit restraint and accelerated development.',
         {}, code=pp(50)+'\n'+tech('industry', .25))
    edit('steady_budget', 'Credit before New Commitments',
         'A credible budget can improve the state\'s borrowing terms and protect essential services. Restraining new commitments also slows public construction, making the cabinet choose which projects can wait.',
         {'interest_rate_multiplier_modifier': -.50, 'production_speed_buildings_factor': -.04,
          'bureaucracy_cost_multiplier_modifier': -.03})
    edit('development_budget', 'A Treasury for Development',
         'The treasury will sustain a faster programme of housing, infrastructure and industrial construction. The productive assets will take time to earn their keep, while the new commitments make public credit more expensive.',
         {'production_speed_buildings_factor': .10, 'interest_rate_multiplier_modifier': .20})
    edit('social_contract', 'Wages, Prices and the Histadrut',
         'Ministers, employers and the Histadrut can settle wage disputes before they interrupt production. A negotiated compact will make industrial change more predictable, while narrowing the cabinet\'s freedom to impose a settlement of its own.',
         {'production_factory_efficiency_gain_factor': .04, 'political_power_factor': -.015},
         code=opinion('labour_unions', 10)+'\n'+opinion('industrial_conglomerates', 5))
    edit('vocational', 'ORT Workshops for a Changing Economy',
         'Practical instruction can help immigrants and development-town residents enter skilled industrial work. Teacher preparation and workshop equipment will cost more than a general promise of employment, but they give modernisation a broader social foundation.',
         {'productivity_growth_modifier': .08, 'education_cost_multiplier_modifier': .03})
    edit('development_towns', 'Work within Reach of the Development Towns',
         'Roads can connect the development towns to jobs and public services instead of leaving housing isolated from the wider economy. The cabinet must fund and maintain those links even where the immediate commercial return is modest.',
         {'production_speed_infrastructure_factor': .10, 'social_cost_multiplier_modifier': .015})
    edit('religious_compromise', 'Renew the Status Quo Agreement',
         'Religious parties will accept a parliamentary settlement that protects their institutions and communal services. The compromise can steady the coalition, while support for separate educational provision places a lasting claim on public funds.',
         {'stability_factor': .05, 'education_cost_multiplier_modifier': .03})
    edit('civil_marriage', 'A Civil Personal-Status Register',
         'A civil register would let households settle their personal status outside religious jurisdiction. It will broaden civil choice while bringing the government into direct conflict with those who regard religious authority as part of the founding compact.',
         {'political_power_factor': .05, 'stability_factor': -.015},
         extra=opinion('the_priesthood', -15))
    edit('volunteer_service', 'Municipal Volunteers and Emergency Aid',
         'Volunteer placements can strengthen local emergency and welfare services without extending military obligation. Councils will need supervisors and dependable placements if the programme is to deliver more than a symbolic national gesture.',
         {'social_cost_multiplier_modifier': -.05, 'bureaucracy_cost_multiplier_modifier': .015},
         extra=opinion('labour_unions', 5))
    edit('service_expansion', 'A Wider Call-Up and Training System',
         'A broader service framework can bring trained recruits to their units more quickly. Larger training establishments and more frequent call-ups will also increase the continuing cost of military personnel.',
         {'mobilization_speed': .15, 'training_time_army_factor': -.05,
          'personnel_cost_multiplier_modifier': .035})
    edit('universities', 'Laboratories beyond the Defence Establishment',
         'Universities in Jerusalem and Haifa need laboratories capable of supporting an independent civilian research agenda. Greater academic capacity will widen the country\'s technical choices while increasing the cost of maintaining its education system.',
         {'research_speed_factor': .025, 'education_cost_multiplier_modifier': .035})
    edit('public_health', 'Clinics and the New Medical Faculties',
         'More clinics and medical training can bring qualified care beyond the largest urban centres. Better administration will make treatment less costly, but training the additional professionals requires a stronger educational commitment.',
         {'health_cost_multiplier_modifier': -.08, 'education_cost_multiplier_modifier': .02})

    # Readiness now has an economic price, while exclusive doctrines change the
    # force's behaviour instead of accumulating another generic organisation bonus.
    edit('reserve_system', 'Miluim: A Trained Reserve',
         'The reserve system depends on civilian specialists arriving at the right units with usable equipment and current training. Reliable mobilisation improves readiness, while employers and the defence budget must absorb more frequent periods of service.',
         {'mobilization_speed': .20, 'army_org_factor': .04,
          'personnel_cost_multiplier_modifier': .04})
    edit('defensive_depth', 'A Fortified Screen and Local Reserves',
         'Prepared positions and rehearsed relief plans can hold a front while reserves assemble. A force organised around that screen will dig in effectively, but its planning routines will be less suited to sudden changes of axis.',
         {'army_defence_factor': .07, 'max_dig_in': 2, 'planning_speed': -.06})
    edit('maneuver', 'Operational Reserves for Mobile War',
         'Mobile reserves must practise changing direction and concentrating before an opponent can react. Faster planning and armoured movement will give the staff more options, at the cost of a heavier field-supply requirement.',
         {'planning_speed': .15, 'army_armor_speed_factor': .05, 'supply_consumption_factor': .04})
    edit('armour_programme', 'Tal\'s Tank Development Directorate',
         'A domestic tank programme can bring repair centres and industrial suppliers into a common engineering effort. Prototypes and trials will require funds long before a new tank enters service.',
         {}, extra=money(.012))
    edit('survivability', 'The Crew Comes First',
         'Armour design and field repair will prioritise keeping experienced crews alive. Additional protection can strengthen the force\'s staying power, with weight and servicing demands limiting its tactical speed.',
         {'army_armor_defence_factor': .10, 'army_armor_speed_factor': -.04})
    edit('armour_mobility', 'Armoured Tempo and Recovery Teams',
         'A mobile armoured force needs crews and recovery teams able to sustain rapid movement. Faster vehicles and planning give the staff a different instrument from heavier protection, while consuming more supplies on campaign.',
         {'army_armor_speed_factor': .08, 'planning_speed': .08, 'supply_consumption_factor': .025})
    edit('engineers', 'Bridging Columns and Field Workshops',
         'Bridging crews and field workshops can keep a small army moving through damaged routes and difficult terrain. Concentrating specialists on those tasks improves supply economy, while leaving fewer resources for rapid entrenchment.',
         {'recon_factor': .08, 'supply_consumption_factor': -.06, 'max_dig_in': -1})
    edit('special_forces', 'Selection and Long-Range Patrol Schools',
         'Specialist patrols need careful selection, language preparation and sustained field training. Their experience will improve the army\'s specialist capability, while small professional establishments carry a higher personnel cost.',
         {'special_forces_cap': .02, 'personnel_cost_multiplier_modifier': .015}, extra=money(.004))
    edit('foreign_aircraft', 'Conversion Schools for American Aircraft',
         'An accepted American supply relationship must be followed by conversion training and maintenance arrangements. Concentrated instruction can improve sortie preparation while leaving more of the air force dependent on an external supply system.',
         {'air_mission_efficiency': .04, 'imp_sanction_resistance': -.04}, extra=money(.004))
    edit('local_aircraft', 'From Bedek Workshops to Israeli Designs',
         'IAI can turn maintenance experience into a broader design and manufacturing programme. Domestic competence will reduce exposure to embargoes, but laboratories and tooling compete with immediate expansion of production lines.',
         {'imp_sanction_resistance': .05, 'production_speed_arms_factory_factor': -.03}, extra=money(.010))
    edit('air_maintenance', 'Spare Engines and Dispersed Workshops',
         'Spare engines and dispersed workshops can turn aircraft on the inventory into aircraft ready for missions. Better servicing will improve operational availability, while the air force must maintain a larger technical establishment.',
         {'air_mission_efficiency': .06, 'air_accidents_factor': -.08,
          'airforce_personnel_cost_multiplier_modifier': .04})
    edit('missile_boats', 'Gabriel and the Missile-Boat Flotilla',
         'Small missile boats need coordinated manoeuvre and crews able to fight in coastal waters. Concentrating the navy on this flotilla will improve its tactical organisation while requiring intensive training and specialist upkeep.',
         {'naval_coordination': .06, 'positioning': .04,
          'navy_personnel_cost_multiplier_modifier': .04}, extra=money(.006))
    edit('submarines', 'A School for Submarine Crews',
         'Submarine operations demand a long apprenticeship in navigation, machinery and concealment. Dedicated instruction will support contemporary submarine research, with the navy accepting higher personnel expenditure for a small force.',
         {'naval_coordination': .04, 'navy_personnel_cost_multiplier_modifier': .025},
         extra=money(.005))
    edit('intelligence_analysis', 'An Independent Assessment Desk',
         'Language specialists and competing assessments can give the cabinet a less complacent picture of its neighbours. Careful evaluation improves reconnaissance and planning, while independent review slows the immediate political use of intelligence.',
         {'recon_factor': .10, 'planning_speed': .08, 'political_power_factor': -.02})
    edit('intelligence_operations', 'Networks beyond the Frontier',
         'Operational stations and secure communications can strengthen foreign networks and protect the state from outside influence. The cabinet must sustain the administrative cost and political responsibility of a larger clandestine establishment.',
         {'foreign_influence_defense_modifier': .15, 'bureaucracy_cost_multiplier_modifier': .025})
    edit('preparedness', 'Readiness within the National Budget',
         'The General Staff must bring reserve call-ups, servicing and civilian protection into one sustainable plan. Better coordination reduces waste in field supply, while the commitment to keep trained forces ready continues in peacetime.',
         {'army_org_factor': .025, 'supply_consumption_factor': -.035,
          'personnel_cost_multiplier_modifier': .02})
    edit('oil_security', 'Stocks for the Iranian Supply Route',
         'An accepted Iranian arrangement can support fuel stocks and more reliable supply planning. Storage and distribution reduce vulnerability to interruption, but dedicated facilities will require continuing administration.',
         {'imp_sanction_resistance': .08, 'fuel_gain_factor': .05,
          'bureaucracy_cost_multiplier_modifier': .015}, extra=money(.004))
    edit('keep_ambiguity', 'Amimut and Cabinet Discipline',
         'A disciplined policy of ambiguity can protect freedom of action without an open declaration. Compartmentalised research and decision-making also make it harder to share knowledge across civilian institutions.',
         {'foreign_influence_defense_modifier': .12, 'research_speed_factor': -.01})
    edit('nuclear_transparency', 'A Civilian Research Accounting',
         'Opening more of the research establishment to public and international scrutiny can broaden civilian scientific exchange. The government will accept less freedom to keep strategic questions outside external discussion.',
         {'research_speed_factor': .025, 'foreign_influence_defense_modifier': -.05})
    edit('golda_labour', 'Renegotiate the Histadrut Production Compact',
         'The Alignment can ask Histadrut enterprises to modernise in exchange for negotiated wages and training. More efficient production will require ministers to share decisions with organised labour rather than direct the enterprises alone.',
         {'production_factory_max_efficiency_factor': .05, 'productivity_growth_modifier': .06,
          'political_power_factor': -.02})
    edit('golda_manager', 'Commercial Accounts for Public Enterprises',
         'Professional managers can give public enterprises clearer responsibility for production and investment. Stronger commercial discipline will improve output while testing the cabinet\'s relationship with workers who expect political protection.',
         {'industrial_capacity_factory': .04}, extra=opinion('labour_unions', -5))
    edit('golda_housing', 'Housing with Municipal Services',
         'New housing must be connected to work, schools and treatment rather than standing alone at the edge of a development town. Maintaining those services will cost more, but dependable links give the next building programme a stronger base.',
         {'production_speed_infrastructure_factor': .08, 'social_cost_multiplier_modifier': .02})
    edit('rabin_cabinet', 'Rabin\'s Professional Cabinet',
         'A Rabin cabinet will place professional responsibility and reserve readiness above a wider system of political appointments. Administrative savings and faster mobilisation will come with a larger continuing personnel commitment.',
         {'bureaucracy_cost_multiplier_modifier': -.05, 'mobilization_speed': .05,
          'personnel_cost_multiplier_modifier': .015})
    edit('peres_cabinet', 'Peres\'s Industrial Cabinet',
         'A Peres cabinet will give domestic defence engineering a larger place in national investment. Faster military-industrial construction will require funds and contracts that might otherwise have expanded civilian commercial activity.',
         {'production_speed_arms_factory_factor': .10, 'production_speed_offices_factor': -.04},
         extra=money(.004))

    # Party policy choices keep their existing direct rewards and follow-ups.
    # The table below replaces their persistent policy package and narrative.
    # Each row is explicit: no percentage split, generic malus template or new
    # historical claim about a hypothetical government is inferred at runtime.
    policies = {
      0: [
        ('Religious Workshops and Technical Schools', 'Mafdal will connect religious study to industrial qualifications. Technical training can broaden skilled employment, while separate educational institutions require additional funding.', {'research_speed_factor': .015, 'education_cost_multiplier_modifier': .03}),
        ('Community Welfare through Religious Councils', 'Mafdal will use religious councils to coordinate community welfare. Social provision can become less costly, at the price of maintaining a larger local administrative network.', {'social_cost_multiplier_modifier': -.06, 'bureaucracy_cost_multiplier_modifier': .02}),
        ('Bnei Akiva and Prepared National Service', 'Religious-Zionist youth organisations can prepare recruits for national service. Quicker mobilisation gives the state trained cadres while increasing expenditure on preparation and personnel.', {'mobilization_speed': .10, 'personnel_cost_multiplier_modifier': .02}),
        ('A Religious Settlement Security Network', 'Mafdal will organise the defence and supply of communities that its settlement movement supports. Better local coordination brings a continuing security bill and a heavier obligation to sustain isolated positions.', {'army_defence_factor': .04, 'supply_consumption_factor': .02, 'personnel_cost_multiplier_modifier': .015}),
      ],
      1: [
        ('The Liberal Wing\'s Commercial Programme', 'Gahal\'s Liberals will open more opportunities for private enterprise. Incoming investment can expand commerce, while a greater reliance on overseas capital increases exposure to external markets.', {'receiving_investment_cost_modifier': -.10, 'mdcw_cw_market_exposure': .04}),
        ('Herut\'s Strategic Public Enterprises', 'Herut will retain selected public enterprises as instruments of national development. Protected production can sustain industrial capacity while making competing commercial investment more difficult.', {'industrial_capacity_factory': .05, 'receiving_investment_cost_modifier': .04}),
        ('The Opposition\'s Parliamentary Safeguards', 'Gahal can carry its opposition experience into government by defending parliamentary scrutiny. Independent scrutiny will make administration more credible while limiting the executive\'s immediate political freedom.', {'corruption_cost_factor': -.03, 'political_power_factor': -.015}),
        ('A Cabinet of Security Priorities', 'Gahal will give military readiness a larger share of the cabinet\'s attention and budget. Units gain a clearer mandate, while permanent security commitments make military personnel more expensive.', {'war_support_factor': .05, 'personnel_cost_multiplier_modifier': .025}),
      ],
      2: [
        ('Independent Credit for Small Firms', 'The Independent Liberals will favour small firms over protected concentrations of capital. Broader access to investment requires officials to supervise a larger number of borrowers and guarantees.', {'receiving_investment_cost_modifier': -.10, 'bureaucracy_cost_multiplier_modifier': .015}),
        ('Manufacturers in Overseas Markets', 'Export-oriented manufacturers will receive the Liberals\' support for capital formation. Better returns will connect productive firms more closely to foreign orders and international market risk.', {'return_on_investment_modifier': .005, 'mdcw_cw_market_exposure': .05}),
        ('Civil Rights with Independent Review', 'Liberal ministers will accept review of their own decisions as the price of enforceable civil rights. More accountable institutions will be harder to direct as a single partisan instrument.', {'stability_factor': .025, 'political_power_factor': -.015}),
        ('A Professional Liberal Defence Policy', 'A liberal security policy will rely on trained planners and carefully assessed missions. Better staff preparation will require a small but continuing commitment to professional personnel.', {'planning_speed': .10, 'personnel_cost_multiplier_modifier': .015}),
      ],
      3: [
        ('The Histadrut Industrial Bargain', 'The Alignment will modernise Histadrut enterprises through negotiated changes in production. Factory efficiency can improve while a stronger role for organised labour limits unilateral ministerial decisions.', {'production_factory_max_efficiency_factor': .05, 'political_power_factor': -.015}),
        ('Kibbutz Workshops and Irrigation', 'Cooperative farms can combine agricultural production with technical instruction. Faster rural investment requires maintenance, extension staff and a lasting public commitment to the cooperative network.', {'production_speed_agriculture_district_factor': .15, 'bureaucracy_cost_multiplier_modifier': .015}),
        ('Development-Town Services before Prestige Projects', 'The Alignment will direct greater attention to municipal services in the periphery. Dependable services can ease social expenditure, while redirecting engineering capacity slows the expansion of military industry.', {'social_cost_multiplier_modifier': -.05, 'production_speed_arms_factory_factor': -.03}),
        ('Negotiations from a Prepared Reserve', 'The Alignment will sustain military readiness as the basis for its negotiating position. Better organised units give the cabinet options, at the cost of more expensive reserve preparation.', {'army_org_factor': .04, 'personnel_cost_multiplier_modifier': .025}),
      ],
      4: [
        ('An Accountable Public-Enterprise Sector', 'The communist parliamentary cabinet will invest in public enterprises with organised worker representation. Improved industrial routines will require ministers to negotiate rather than issue every instruction directly.', {'production_factory_max_efficiency_factor': .05, 'political_power_factor': -.02}),
        ('A State Plan for Industrial Construction', 'Central planners will concentrate engineering and credit on industrial construction. New production capacity comes ahead of the commercial services that independent firms would otherwise have expanded.', {'production_speed_industrial_complex_factor': .12, 'production_speed_offices_factor': -.05}),
        ('Common Citizenship and Public Provision', 'Equal citizenship will be supported through common public provision. Stable civic institutions require a greater educational commitment if formal equality is to become practical access.', {'stability_factor': .04, 'education_cost_multiplier_modifier': .025}),
        ('Training for a Soviet Supply Relationship', 'A Soviet-oriented security programme will prepare technical personnel for foreign equipment and assistance. Improved support capacity also makes the army more dependent on the continuing foreign relationship.', {'mdcw_cw_support_effectiveness': .10, 'imp_sanction_resistance': -.04}),
      ],
      5: [
        ('Producers\' Councils in the Workshops', 'The council left will place workplace training in producers\' hands. Sharing practical knowledge can improve industrial efficiency, while negotiating between autonomous workplaces slows central direction.', {'production_factory_max_efficiency_factor': .05, 'political_power_factor': -.02}),
        ('A Cooperative Investment Federation', 'The federation will pool investment for projects that individual cooperatives cannot undertake. Faster construction requires a standing organisation to settle priorities among its members.', {'production_speed_buildings_factor': .06, 'bureaucracy_cost_multiplier_modifier': .02}),
        ('Municipal Powers in a Federal Charter', 'A federal charter will place defined powers in local institutions. Less routine work falls on the central administration, while national construction programmes must accept additional local negotiation.', {'bureaucracy_cost_multiplier_modifier': -.08, 'production_speed_buildings_factor': -.03}),
        ('Shared Civic Services across Communities', 'Common civic services will give the federation a practical national role. Shared provision can reduce social costs, while coordination across autonomous councils requires more public administration.', {'social_cost_multiplier_modifier': -.06, 'bureaucracy_cost_multiplier_modifier': .02}),
      ],
      6: [
        ('Family Workshops in the Development Towns', 'The traditionalist alliance will broaden credit for family businesses and craftspeople. Local enterprise gains room to grow while small-loan supervision places new demands on the municipal administration.', {'receiving_investment_cost_modifier': -.10, 'bureaucracy_cost_multiplier_modifier': .015}),
        ('Municipal Services for the Periphery', 'Southern municipalities will receive priority for public works and services. Faster local connections will require a greater continuing commitment to social provision.', {'production_speed_infrastructure_factor': .12, 'social_cost_multiplier_modifier': .02}),
        ('A Traditional Path into Skilled Work', 'Community teachers and technical schools will offer qualifications without requiring young people to leave their social institutions. The resulting skills will require sustained expenditure on education.', {'research_speed_factor': .015, 'education_cost_multiplier_modifier': .025}),
        ('Community Institutions at the Bargaining Table', 'Workers, employers and religious institutions will negotiate the social partnership together. A stable settlement gives each institution influence and leaves the cabinet less freedom to act alone.', {'stability_factor': .04, 'political_power_factor': -.02}),
      ],
      7: [
        ('Procurement under Engineering Standards', 'The directorate will use professional engineering rules to reduce administrative waste. Transparent tendering can make the state less costly while slowing contracts that previously moved through favoured channels.', {'bureaucracy_cost_multiplier_modifier': -.08, 'production_speed_buildings_factor': -.02}),
        ('Corporations for Accelerated Construction', 'The directorate will concentrate construction in state corporations and favoured contractors. Faster industrial development makes the state more dependent on politically protected suppliers.', {'production_speed_industrial_complex_factor': .15, 'corruption_cost_factor': .06}),
        ('Return the Budget to Parliament', 'Restored elections will give public expenditure a broader mandate and expose it to parliamentary scrutiny. Civilian legitimacy will limit the speed with which the directorate can command new projects.', {'stability_factor': .04, 'political_power_factor': -.02}),
        ('The Permanent Presidential Planning Office', 'A permanent presidency can concentrate authority over appointments and planning. Clearer command will be accompanied by a larger protected administrative establishment.', {'political_power_factor': .10, 'bureaucracy_cost_multiplier_modifier': .04}),
      ],
      12: [
        ('Commercial Credit for Arab Municipalities', 'Municipal representatives will connect local firms to commercial credit. More investment can support employment while requiring additional offices to supervise a wider network of borrowers.', {'receiving_investment_cost_modifier': -.10, 'bureaucracy_cost_multiplier_modifier': .015}),
        ('Local Endowments and Welfare Boards', 'Community endowments will help councils organise welfare services. Lower social costs will be accompanied by the administrative work of coordinating public and charitable provision.', {'social_cost_multiplier_modifier': -.08, 'bureaucracy_cost_multiplier_modifier': .02}),
        ('A Place in Common Civic Institutions', 'Municipal representatives will seek enforceable participation in national institutions. Civic confidence can improve, while ministers must accept a more negotiated parliamentary agenda.', {'stability_factor': .03, 'political_power_factor': -.015}),
        ('Autonomous Municipal Administration', 'Councils will take responsibility for more routine administration. Central costs can fall while national infrastructure planning must accommodate a larger number of local decisions.', {'bureaucracy_cost_multiplier_modifier': -.08, 'production_speed_infrastructure_factor': -.04}),
      ],
      13: [
        ('Trades alongside the Yeshiva', 'Orthodox representatives will connect religious learning with practical qualifications. New skills can serve community employment, with separate training arrangements raising educational expenditure.', {'research_speed_factor': .015, 'education_cost_multiplier_modifier': .03}),
        ('Community Welfare and Charitable Accounts', 'Religious welfare organisations will receive a larger role under published accounts. More efficient social provision will require officials to coordinate a more complex network of institutions.', {'social_cost_multiplier_modifier': -.08, 'bureaucracy_cost_multiplier_modifier': .02}),
        ('Protect the Parliamentary Status Quo', 'The bloc will negotiate religious accommodation through parliament. A steadier coalition will require the state to sustain the separate educational institutions protected by the settlement.', {'stability_factor': .05, 'education_cost_multiplier_modifier': .03}),
        ('Voluntary Service through Community Institutions', 'Community organisations will provide civilian placements and local supervision. The programme can support social services while requiring a continuing administrative commitment.', {'social_cost_multiplier_modifier': -.04, 'bureaucracy_cost_multiplier_modifier': .015}),
      ],
      14: [
        ('Commercial Discipline in Public Enterprises', 'The State List will ask public managers to answer for production and costs. Efficient industrial routines will come with fewer political guarantees for the workers and interests accustomed to them.', {'production_factory_efficiency_gain_factor': .07}),
        ('A Competitive Private Sector', 'A pragmatic cabinet will open commercial opportunities beyond the established enterprises. Foreign investment can become more attractive while a greater part of development depends on external market conditions.', {'receiving_investment_cost_modifier': -.10, 'mdcw_cw_market_exposure': .04}),
        ('A Sustainable Defensive Posture', 'Professional preparation will support a defensive posture with limited objectives. Better coordination improves defence, while trained readiness continues to cost money between crises.', {'army_defence_factor': .05, 'personnel_cost_multiplier_modifier': .02}),
        ('Cabinet Authority for Territorial Talks', 'Negotiators will receive a clear cabinet mandate to explore territorial agreements. Diplomatic freedom will require a domestic political effort that leaves less room for unrelated legislation.', {'foreign_influence_defense_modifier': .08, 'political_power_factor': -.015}),
      ],
      15: [
        ('Published Contracts for Diaspora Capital', 'Investors will receive clear contracts and public reporting. Better use of development capital requires officials to supervise the terms instead of leaving them to personal connections.', {'imp_investment_reward': .10, 'bureaucracy_cost_multiplier_modifier': .02}),
        ('Concessions for the Development Sponsors', 'The alliance will accelerate development through favoured investors and concessions. Attractive terms will bring investment while raising the public cost of politically protected business.', {'receiving_investment_cost_modifier': -.15, 'corruption_cost_factor': .06}),
        ('Independent Review of Investment Contracts', 'Independent reviewers will inspect the alliance\'s contracts. Lower corruption costs will require governing politicians to surrender some control over the allocation of favours.', {'corruption_cost_factor': -.05, 'political_power_factor': -.02}),
        ('The Notables\' Investment Network', 'The alliance will use municipal notables and investors to consolidate its governing network. Stronger political organisation will carry the cost of public spending shaped by patronage.', {'political_power_factor': .10, 'corruption_cost_factor': .06}),
      ],
      16: [
        ('Education for a Civilian Economy', 'The civil-rights movement will connect investment access to public technical education. Civilian opportunity will broaden, while educational expenditure rises to support the new qualifications.', {'receiving_investment_cost_modifier': -.08, 'education_cost_multiplier_modifier': .025}),
        ('Service Firms beyond Party Patronage', 'The movement will simplify entry into services and commercial work. A cheaper central administration will leave municipalities with more responsibility for maintaining local provision.', {'bureaucracy_cost_multiplier_modifier': -.08, 'social_cost_multiplier_modifier': .015}),
        ('A Secular Public Sphere', 'A free public sphere will let citizens challenge ministers and religious authorities. Greater political initiative will provoke resistance among institutions that regard the change as a threat to their established role.', {'political_power_factor': .08}),
        ('Power to the Elected Municipalities', 'Elected municipalities will receive more responsibility for local decisions. Less central administration will be offset by slower agreement on construction that crosses municipal boundaries.', {'bureaucracy_cost_multiplier_modifier': -.08, 'production_speed_buildings_factor': -.03}),
      ],
      17: [
        ('Water Budgets for Cultivation', 'Conservation planners will favour cultivation that can justify its water requirements. Faster agricultural investment will depend on a standing service of surveyors and extension officers.', {'production_speed_agriculture_district_factor': .15, 'bureaucracy_cost_multiplier_modifier': .02}),
        ('Engineering for Energy Efficiency', 'Cleaner industrial methods will become a technical research priority. Better efficiency will require dedicated laboratories and higher expenditure on scientific education.', {'research_speed_factor': .02, 'education_cost_multiplier_modifier': .025}),
        ('Landscape Review before Construction', 'Municipal planners will review land use before approving major works. More careful public administration can improve repair and maintenance, while slowing new construction.', {'industry_repair_factor': .10, 'production_speed_buildings_factor': -.03}),
        ('Public Transport and Healthy Communities', 'The environmental alternative will connect public transport to local health and social provision. Services can become less costly when coordinated, but the network needs additional public administration.', {'social_cost_multiplier_modifier': -.05, 'bureaucracy_cost_multiplier_modifier': .02}),
      ],
      18: [
        ('Mapam\'s Cooperative Social Compact', 'An independent Mapam will defend cooperative production and a broad welfare commitment. Efficient social provision will depend on collective bargaining that limits unilateral cabinet action.', {'social_cost_multiplier_modifier': -.08, 'political_power_factor': -.02}),
        ('Schools and Services in the Periphery', 'Mapam will favour municipal services and education over another round of prestige industrial projects. Administrative savings will accompany a greater educational commitment.', {'bureaucracy_cost_multiplier_modifier': -.05, 'education_cost_multiplier_modifier': .025}),
        ('A Parliamentary Mandate for Peace', 'The government will establish a negotiating mandate through public and parliamentary debate. Greater diplomatic independence will cost political attention before an agreement is within reach.', {'foreign_influence_defense_modifier': .08, 'political_power_factor': -.015}),
        ('Equal Institutions before a Binational Convention', 'A binational alternative will begin with common civic institutions and an accountable convention. Greater political capacity must be supported by a larger educational and administrative effort.', {'political_power_factor': .05, 'education_cost_multiplier_modifier': .025}),
      ],
      19: [
        ('Joint Jewish-Arab Industrial Training', 'Independent communist institutions will organise common worker training across community lines. Factory routines can improve while industrial education becomes a larger public commitment.', {'production_factory_max_efficiency_factor': .05, 'education_cost_multiplier_modifier': .025}),
        ('Public Investment through an Elected Plan', 'An elected planning process will coordinate public investment. Faster building requires additional staff to reconcile enterprise and municipal priorities.', {'production_speed_buildings_factor': .06, 'bureaucracy_cost_multiplier_modifier': .02}),
        ('Workers\' Rights under Ordinary Elections', 'Workers\' rights will be secured through parliament and ordinary elections. Accountable government can be more stable while leaving ministers less freedom to bypass negotiated procedures.', {'stability_factor': .035, 'political_power_factor': -.015}),
        ('Limited Powers for Workers\' Councils', 'Workers\' councils will receive defined administrative powers alongside the elected legislature. Less central bureaucracy will be accompanied by slower coordination of national building priorities.', {'bureaucracy_cost_multiplier_modifier': -.08, 'production_speed_buildings_factor': -.03}),
      ],
      20: [
        ('Local Enterprise as a National Programme', 'The national opposition will promote workshops and small businesses in the development towns. New investment opportunities will require a larger network of credit supervision.', {'receiving_investment_cost_modifier': -.10, 'bureaucracy_cost_multiplier_modifier': .015}),
        ('A National Pact for Industrial Production', 'Workers and manufacturers will be brought into a national production pact. Better output depends on negotiated obligations that reduce the cabinet\'s freedom to settle industrial disputes alone.', {'industrial_capacity_factory': .05, 'political_power_factor': -.02}),
        ('A National Opposition under Parliamentary Rules', 'National populism will accept ordinary elections and parliamentary accountability. A stable constitutional position requires ministers to share power with institutions outside the movement.', {'stability_factor': .04, 'political_power_factor': -.015}),
        ('An Elected Presidency with a Popular Mandate', 'The movement will seek an elected president while preserving competition for office. Concentrated political authority requires a larger presidency and administrative staff.', {'political_power_factor': .10, 'bureaucracy_cost_multiplier_modifier': .025}),
      ],
      21: [
        ('A Domestic Arms-Supply Network', 'The radical national alliance will support domestic suppliers to resist external pressure. Greater resilience will protect strategic work while making foreign commercial investment less attractive.', {'imp_sanction_resistance': .10, 'receiving_investment_cost_modifier': .05}),
        ('The Reserve Mobilisation Fund', 'The alliance will keep more of the reserve establishment ready for mobilisation. Faster call-ups require recurring expenditure on personnel and training.', {'mobilization_speed': .15, 'personnel_cost_multiplier_modifier': .04}),
        ('Legal Limits on the National Movement', 'The alliance will accept ordinary elections and legal limits on political organisation. Civilian confidence can improve, but its leaders will lose some freedom to act through the movement alone.', {'stability_factor': .04, 'political_power_factor': -.02}),
        ('A Permanent Security Executive', 'An authoritarian security executive will suspend ordinary political competition. Concentrated authority will make the government more forceful while the expanded apparatus consumes public funds.', {'political_power_factor': .10, 'bureaucracy_cost_multiplier_modifier': .04}),
      ],
      22: [
        ('One Emergency Logistics Command', 'The emergency cabinet will centralise logistics and procurement. More efficient field supply will rely on a professional establishment with a larger continuing personnel bill.', {'supply_consumption_factor': -.08, 'personnel_cost_multiplier_modifier': .025}),
        ('Civilian Technocrats in the Emergency Cabinet', 'Civilian specialists will take responsibility for procurement and industrial planning. A cheaper administration will come with more review before new projects are authorised.', {'bureaucracy_cost_multiplier_modifier': -.08, 'production_speed_buildings_factor': -.02}),
        ('Return the Emergency Budget to Civilian Control', 'Ordinary elections will restore a civilian mandate for the emergency budget. Confidence can recover while officers and ministers accept limits on unilateral action.', {'stability_factor': .05, 'political_power_factor': -.02}),
        ('Permanent Rule by the Command Council', 'The command council will retain authority beyond the emergency. Concentrated political control will require a standing military and administrative establishment.', {'political_power_factor': .10, 'personnel_cost_multiplier_modifier': .04}),
      ],
      23: [
        ('Public Endowments for Local Works', 'Under the alternate crown settlement, public endowments will finance local works. Faster infrastructure development will bring a continuing commitment to social provision.', {'production_speed_infrastructure_factor': .15, 'social_cost_multiplier_modifier': .02}),
        ('Industrial Companies under the Crown', 'The crown\'s industrial alternative will concentrate investment in public companies. Faster industrial construction will compete with private commercial development for capital.', {'production_speed_industrial_complex_factor': .12, 'receiving_investment_cost_modifier': .04}),
        ('A Crown Responsible to Parliament', 'A parliamentary crown will accept ordinary elections and a responsible cabinet. A stable constitutional settlement will limit the executive\'s freedom to direct public affairs alone.', {'stability_factor': .05, 'political_power_factor': -.02}),
        ('Personal Government from the Crown', 'Personal royal government will suspend ordinary elections and concentrate executive power. A larger household and central administration will make that authority more costly to sustain.', {'political_power_factor': .10, 'bureaucracy_cost_multiplier_modifier': .04}),
      ],
    }
    for slot, rows in policies.items():
        for choice, (label, body, mods) in zip(('ea', 'eb', 'ca', 'cb'), rows):
            edit(f'p{slot}_{choice}', label, body, mods)

    # Opposition has concrete interest-group consequences rather than invented
    # automatic resistance reductions, loyalty, demographic changes or cores.
    for key, group, delta in [
        ('p14_ea', 'labour_unions', -5),
        ('p16_ca', 'the_priesthood', -10),
        ('p1_ca', 'the_military', -5),
        ('p2_ea', 'industrial_conglomerates', -5),
        ('p0_cb', 'small_medium_business_owners', -5),
        ('p21_cb', 'labour_unions', -10),
        ('p22_cb', 'small_medium_business_owners', -10),
    ]:
        edit(key, extra=opinion(group, delta))

    # Rarely selected follow-ups gain a concrete speciality. Existing funded
    # factories, infrastructure and constitutional effects remain in place.
    followups = {
        'p0_ea_deepen': {'productivity_growth_modifier': .05, 'education_cost_multiplier_modifier': -.015},
        'p0_ca_deepen': {'training_time_army_factor': -.05, 'recruitable_population_factor': .02},
        'p0_cb_deepen': {'army_org_factor': .025, 'supply_consumption_factor': -.035},
        'p1_cb_deepen': {'production_factory_efficiency_gain_factor': .05, 'supply_consumption_factor': -.035},
        'p2_cb_deepen': {'foreign_influence_defense_modifier': .08, 'recon_factor': .04},
        'p3_ea_deepen': {'productivity_growth_modifier': .04},
        'p3_eb_deepen': {'production_factory_efficiency_gain_factor': .03},
        'p4_ea_deepen': {'productivity_growth_modifier': .07},
        'p5_ea_deepen': {'productivity_growth_modifier': .07},
        'p6_ca_deepen': {'productivity_growth_modifier': .07},
        'p7_cb_deepen': {'production_speed_buildings_factor': .06, 'corruption_cost_factor': .015},
        'p12_cb_deepen': {'social_cost_multiplier_modifier': -.05, 'production_speed_infrastructure_factor': .05},
        'p13_eb_deepen': {'health_cost_multiplier_modifier': -.05, 'education_cost_multiplier_modifier': .01},
        'p14_ca_deepen': {'supply_consumption_factor': -.06, 'planning_speed': .04},
        'p15_cb_deepen': {'production_speed_offices_factor': .10, 'corruption_cost_factor': .02},
        'p16_eb_deepen': {'production_speed_offices_factor': .08},
        'p17_eb_deepen': {'industry_repair_factor': .12, 'production_factory_max_efficiency_factor': .04},
        'p18_cb_deepen': {'bureaucracy_cost_multiplier_modifier': -.04, 'stability_factor': .025},
        'p19_eb_deepen': {'productivity_growth_modifier': .07},
        'p20_cb_deepen': {'war_support_factor': .04, 'mobilization_speed': .04},
        'p21_cb_deepen': {'army_org_factor': .04, 'stability_factor': -.015},
        'p22_cb_deepen': {'army_org_factor': .04, 'mobilization_speed': .08, 'stability_factor': -.015},
        'p23_cb_deepen': {'mobilization_speed': .08, 'stability_factor': -.015},
    }
    for key, mods in followups.items():
        edit(key, mods=mods)

    # New numeric costs must be explicit in the normal effect field. Their
    # political context is placed in descriptions, not custom effect essays.
    caution = {
        'p7_cb_deepen': ' Presidential discretion also leaves more room for politically favoured contracts.',
        'p15_cb_deepen': ' The privileged network increases the cost of patronage as its reach expands.',
        'p21_cb_deepen': ' Permanent exceptional powers continue to erode civilian confidence.',
        'p22_cb_deepen': ' Prolonged military government continues to weaken civilian confidence.',
        'p23_cb_deepen': ' Personal executive authority continues to divide public opinion.',
    }
    for key, sentence in caution.items():
        specs[key]['body'] += sentence

    # User-directed Israeli workforce/economic path. The native MD reader
    # adds these six compatible participation gains before its +50% overall cap.
    # The +15% route is a game-balance choice; it creates no people and does not
    # assert that historical Israel already had an unusually large workforce.
    workforce = {
        'social_contract': .02,
        'vocational': .03,
        'development_towns': .02,
        'absorption_reform': .04,
        'universities': .02,
        'public_health': .02,
    }
    for key, value in workforce.items():
        specs[key]['mods']['total_workforce_modifier'] = value
    specs['social_contract']['body'] += ' Agreed recruitment and working arrangements will also bring more adults into regular employment.'
    specs['vocational']['body'] += ' Retraining women and adults outside skilled employment will expand the available labour force.'
    specs['development_towns']['body'] += ' Bringing jobs within reach allows more residents to enter paid employment.'
    edit('absorption_reform', 'Ulpan, Qualifications and a First Job',
         'Language instruction and recognition of qualifications will connect immigrants to work that uses their skills. Housing, job placement and bridging courses can turn an absorption system into a route to regular employment, while the state accepts continuing educational obligations.',
         {'total_workforce_modifier': .04, 'education_cost_multiplier_modifier': .025})
    specs['universities']['body'] += ' Qualifications and specialist conversion courses will broaden access to professional work.'
    specs['public_health']['body'] += ' Dependable treatment and community care also help more adults remain in paid work.'

    # Financial strength is delivered through actual MD productivity/tax readers,
    # assets and investment mechanics, rather than an unexplained free treasury.
    for key, changes in {
        'economic_plan': {'industrial_capacity_factory': .05, 'civilian_factories_productivity': .08},
        'haifa_industry': {'industrial_capacity_factory': .05, 'civilian_factories_productivity': .10},
        'tel_aviv_offices': {'offices_productivity': .12},
        'exports': {'offices_productivity': .10},
        'export_specialization': {'return_on_investment_modifier': .01, 'offices_productivity': .08},
        'civil_electronics': {'productivity_growth_modifier': .20, 'production_factory_efficiency_gain_factor': .08},
        'negev_agriculture': {'agricolture_productivity_modifier': .12},
        'water_maintenance': {'agricolture_productivity_modifier': .06},
        'sme_credit': {'offices_productivity': .06},
    }.items():
        specs[key]['mods'].update(changes)
    specs['economic_plan']['body'] = 'Pinhas Sapir\'s development programme will link public credit, industrial estates and engineering research. A broader manufacturing base can increase production and tax receipts, while the treasury must continue to choose between civilian development and defence procurement.'
    specs['tel_aviv_offices']['body'] = 'Commercial offices in Tel Aviv will bring export finance, technical services and accounting into a more productive urban network. The investment strengthens the service economy while competing with industrial and peripheral projects for capital.'
    specs['negev_agriculture']['body'] = 'Irrigation, technical instruction and a funded agricultural district will give the Negev a more productive farming base. The programme relies on water infrastructure and capital that other regions and industries also need.'
    for key in workforce:
        assert specs[key]['mods']['total_workforce_modifier'] > 0
    assert abs(sum(workforce.values()) - .15) < .00001
