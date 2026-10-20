"""English-only presentation and 1970 political identities for Israel's authored tree."""
PARTIES = [
 ('Mafdal - Religious Zionism','Parliamentary religious Zionism links public institutions, national service and the religious status quo.','Religion in the Public State','Religious Study and Vocational Education','Municipal Religious Welfare','Bnei Akiva and National Service','Religious Settlement Policy','Religion and the Republic'),
 ('Gahal - Herut and the Liberals','Begin must hold together the revisionist and liberal wings of Gahal. A later Likud foundation is a choice, not an anachronistic starting party.','Hold Herut and the Liberals Together','An Entrepreneurial Israel','Retain Strategic State Enterprises','The Rule of Law and Opposition','Indivisible Security Interests','The Conservative Transfer of Power'),
 ('Independent Liberals','An independent liberal cabinet can promote small business, civil rights or a pragmatic security policy without importing parties from the twenty-first century.','Liberal Government Responsibility','Small Business over Monopolies','Capital and Export Industry','Entrench Civil Rights','A Liberal Security State','A Liberal Republic'),
 ('Alignment - Golda\'s Israel','The Labor Party and Mapam share the Alignment. Golda Meir governs through a broad coalition, a citizen army and the institutions of Labor Zionism.','The Labor Zionist Alliance','Modernize the Histadrut','Kibbutzim as Development Centers','Social Balance in the Cities','Security through Negotiating Strength','A Second Building of Israel'),
 ('Rakah - The Communist Course','A Jewish-Arab communist government is an alternative electoral outcome. Parliamentary socialism and Soviet alignment remain separate decisions.','A Jewish-Arab Class Alliance','Parliamentary Communism','A Central Economic Plan','Equal Citizens','Soviet Security Cooperation','A Socialist Peace Settlement'),
 ('Federative Council Left','An explicitly alternative council-socialist movement can decentralize production and negotiate a federal or common civic constitution.','Communes over Party Headquarters','Autonomous Producers\' Councils','A Coordinated Cooperative Federation','Jewish-Arab Federalism','A Common Civic Republic','A Federation of Municipalities'),
 ('Mizrahi Traditionalist Alliance','An alternative traditionalist movement gives development towns an independent voice. Shas remains a later foundation rather than a party transplanted into 1970.','Represent the Periphery','Crafts and Family Businesses','Municipal Development Funds','Tradition and Shared Education','Traditional Social Partnership','The Rise of the Development Towns'),
 ('Development Directorate','An explicitly alternative emergency directorate must choose between professional administration and patronage, and between a civilian transition and enduring presidential power.','A Limited Directorate','A Technocratic Development Plan','Patronage through State Corporations','Return to Parliamentary Government','Permanent Presidential Rule','The Directorate State'),
 ('Shiite Consensus Council','This extreme alternative is available only after an explicitly accepted successor-state constitution. It is not a Jewish Israeli political party.','A Civilian Council Government','Municipal Reconstruction Cooperatives','Foreign Reconstruction Investment','Confessional Pluralism','Religious Arbitration Courts','A Negotiated Successor State'),
 ('Revolutionary Guardian Council','A revolutionary successor-state constitution is required before this extreme alternative can form a government.','Revolutionary State Building','Cooperative Reconstruction','Centralized Defense Industry','Civilian Security Institutions','Political Guardian Organizations','The Revolutionary Council Republic'),
 ('Salafist Monarchy','A new state identity and an explicit foundation are required. This is a successor-state alternative, not a Jewish Salafist monarchy.','A Dynastic Founding Settlement','Family Trade and Endowments','State-Led Reconstruction','A Consultative Assembly','Dynastic Centralization','A New Monarchy'),
 ('Salafist Revolutionary State','A constitutional crisis and a freely selected successor-state foundation precede this extreme alternative. Reconstruction and militarized expansion are different policies.','The Revolutionary Constituent Assembly','Local Supply Autonomy','A Central War Economy','Reconstruction before Expansion','Militarize the Revolution','A New Revolutionary State Order'),
 ('Islamic Municipal Reform List','A parliamentary organization of Arab municipalities can prioritize trade, charitable provision or a common civic settlement.','Municipal Interests in the Knesset','Arab Commercial Centers','Social Endowments and Municipal Aid','Integration into the Civic Order','Autonomous Municipal Institutions','A Political Voice for the Municipalities'),
 ('Agudat Israel and Poalei Agudat','The Orthodox parties defend their communities through parliamentary bargaining, religious education and local social institutions.','The Orthodox Parliamentary Bloc','Vocational Education and Religious Study','Community Social Provision','The Religious Status Quo','Voluntary Civilian Service','A Sustainable Religious Compromise'),
 ('State List and Pragmatic Right','A pragmatic cabinet can professionalize public enterprises or encourage private business, while choosing between defensive pragmatism and territorial negotiations.','Pragmatic State Leadership','Professional State Enterprises','Promote Private Enterprise','Security Pragmatism','Territorial Negotiations','Pragmatism as Statecraft'),
 ('Development and Enterprise Bloc','An explicitly alternative alliance of entrepreneurs and municipal notables must choose transparent investment or privileged concessions and patronage.','An Elite Development Alliance','Diaspora Capital with Oversight','Privileged Concessions','Transparent Investment Contracts','Political Patronage Networks','The Investment State'),
 ('HaOlam HaZeh - Free Citizens','A secular civil-rights movement can defend a free press and equal citizenship. Radical market reform is a separate alternative policy.','A Free Press and Political Public Life','A Civil-Rights Reform Economy','Radical Debureaucratization','A Secular Civic State','Decentralized Municipalities','A State of Free Citizens'),
 ('Landscape and Environment League','An alternative early environmental organization addresses the real development choices of land, water, industry and public infrastructure.','Development and Landscape Protection','Water-Efficient Agriculture','Clean Industry and Research','Municipal Conservation Planning','Social and Environmental Infrastructure','A Livable Development Strategy'),
 ('Mapam and the Independent Left','Mapam brings the cooperative movement, organized workers and a commitment to Jewish-Arab equality into the debate over Israel\'s future.','An Independent Socialist Left','A Cooperative Welfare State','Municipal Development and Education','A Negotiated Peace','A Binational Constitutional Convention','Socialism and Equal Rights'),
 ('Maki - Independent Communism','An independent communist cabinet chooses its own relationship between workers\' institutions, parliamentary rights and economic planning.','Independent Workers\' Politics','Jewish-Arab Industrial Enterprises','Democratic Economic Planning','Parliamentary Workers\' Rights','Constitutionally Limited Councils','An Independent Workers\' Republic'),
 ('Free Center and National Alliance','A national opposition can remain parliamentary or seek a presidential mandate. It is not a later national-religious party transplanted into 1970.','A New National Opposition','Small Business in Development Towns','A National Industrial Pact','Parliamentary National Populism','A Presidential Popular Mandate','A National Majority Movement'),
 ('Radical National Front','An explicit alternative radicalization precedes this movement. Autarky, mobilization and an authoritarian security order have real economic consequences.','Form a Radical Alliance','An Autonomous Defense Industry','A National Mobilization Fund','Radical Politics within Legal Limits','An Authoritarian Security State','The Radical State Order'),
 ('Military Emergency Cabinet','A genuine constitutional emergency is required. The armed forces are not treated as an ordinary electoral party in January 1970.','The Emergency Mandate','Centralize Defense Logistics','Bring in Civilian Technocrats','A Limited Emergency with Elections','Permanent Military Rule','The Future of the Emergency Cabinet'),
 ('Constitutional Hebrew Crown','A freely selected constitutional founding process is required. A crown is an explicit alternative, not a reinterpretation of a modern religious party.','A Constituent Crown Assembly','Endowments and Public Works','Royal Industrial Companies','A Parliamentary Crown','Personal Royal Government','The Crown and Israeli Statehood'),
]
IDEOLOGIES=['Western_Autocracy','conservatism','liberalism','socialism','communist_state','anarchist_communism','Conservative','Autocracy','Mod_Vilayat_e_Faqih','Vilayat_e_Faqih','Kingdom','Caliphate','Neutral_Muslim_Brotherhood','Neutral_Autocracy','Neutral_conservatism','oligarchism','Neutral_Libertarian','Neutral_green','neutral_Social','Neutral_Communism','Nat_Populism','Nat_Fascism','Nat_Autocracy','Monarchist']
COMMON = dict(line.split('|',1) for line in '''january_1970|Israel in January 1970
knesset|The Seventh Knesset
unity_cabinet|Negotiate a Unity Cabinet
narrow_cabinet|A Parliamentary Working Majority
civil_service|A Professional Civil Service
oversight|The Comptroller and Parliamentary Oversight
local_councils|Municipal Freedom of Action
central_planning|Coordinated State Planning
basic_laws|The Unfinished Basic Laws
alignment_balance|Labor and Mapam in the Alliance
golda_labour|Include the Unions in Modernization
golda_manager|Professional Enterprise Management
golda_panthers|Take the Social Protest Seriously
golda_housing|Housing for the Development Towns
golda_succession|Leadership after Golda
rabin_cabinet|Rabin's Reform Cabinet
peres_cabinet|Peres and the Industrial Future
gahal_identity|Herut and the Liberals: The Identity Question
gahal_coalition|Retain Gahal as a Broad Alliance
likud_foundation|Found a United Likud List
economic_plan|An Economic Plan for the Seventies
water|Water as a Basis for Development
negev_agriculture|Irrigation and Agronomy in the Negev
water_maintenance|Maintain the Water Network
haifa_industry|Haifa as an Industrial Center
tel_aviv_offices|Services in Tel Aviv
negev_roads|Roads to the Development Towns
power_grid|A Reliable Electricity Network
exports|Diamonds, Tools and Export Orders
import_substitution|Strategic Import Substitution
export_specialization|Specialize for Export Markets
diaspora_bonds|Diaspora Capital for Real Projects
investment_scrutiny|Scrutinize Investment Contracts
civil_electronics|Civilian Electronics and Skilled Workers
technion|Technion and Applied Research
sme_credit|Credit for Productive Small Businesses
civil_plant|Further Industrial Development
fiscal_review|Growth and Public Finances
steady_budget|Gradual Fiscal Consolidation
development_budget|Development before Short-Term Consolidation
social_contract|A Social Development Compact
vocational|Vocational Education for New Citizens
development_towns|Connect the Development Towns
absorption_reform|Integrate Immigration for the Long Term
arab_citizens|Arab Citizens in the Development Compact
equal_local_services|Equal Municipal Services
local_autonomy|Strengthen Municipal Self-Government
religion_state|Negotiate Religion and the State
religious_compromise|Renew the Religious Compromise
civil_marriage|Civil Personal-Status Options
national_service|The Question of Shared Service
volunteer_service|Voluntary Municipal Civilian Service
service_expansion|Expand Military Training
universities|Research between Jerusalem and Haifa
public_health|Healthcare beyond the Metropolises
staff|The General Staff and the Security Situation
reserve_system|Keep the Reserve Ready
defensive_depth|Defense in Depth
maneuver|Mobile Operational Reserves
armour_programme|Tal and the Domestic Tank Programme
survivability|Crew Protection and Maintenance
armour_mobility|Mobility and Tactical Employment
imi|IMI and Domestic Manufacturing
artillery|Artillery and Counter-Battery Reconnaissance
engineers|Engineers and Combat Supply
special_forces|Special Forces with Clear Missions
air_staff|The Air Force after the Embargo
foreign_aircraft|Delivery Contracts over Domestic Development
local_aircraft|IAI and a Domestic Aircraft Industry
air_maintenance|Training, Maintenance and Spare Parts
airfield|A Resilient Airfield Network
air_defense|Radar and Contemporary Air Defense
naval_staff|Secure the Coast and Sea Lanes
missile_boats|Missile Boats and Coastal Operations
submarines|Submarines and Covert Reconnaissance
shipyards|Shipbuilding Capacity in Haifa
intelligence|Mossad and Military Intelligence
intelligence_analysis|Analysis before Easy Certainties
intelligence_operations|Operational Intelligence Networks
civil_defense|Civil Defense for Border Communities
preparedness|A Coordinated Readiness Plan
foreign_policy|The Foreign-Policy Situation of 1970
us_channel|Strengthen the Washington Channel
us_security|Negotiate Security Cooperation
us_civil|Negotiate Civilian Economic Cooperation
france_channel|Approach Paris Again
european_trade|Develop European Export Markets
soviet_channel|A Cautious Opening to Moscow
soviet_dialogue|Emigration and Diplomatic Contacts
independent_diplomacy|An Independent Diplomacy
africa_contacts|Maintain African Contacts
jordan_backchannel|Confidential Talks with Amman
iran_contacts|Relations with the Shah's Iran
oil_security|Contractual Oil-Supply Security
nuclear_policy|Ambiguity or International Transparency
keep_ambiguity|Preserve Nuclear Ambiguity
nuclear_transparency|Offer International Transparency
suez|Assess the Suez Front
limited_attrition|Limit the Conflict
deep_raids|Increase Military Pressure
rogers|Respond to the Rogers Initiative
ceasefire|A Controlled Ceasefire
armed_stalemate|Maintain the Armed Stalemate
territorial_policy|The Question of the Controlled Territories
all_on|Defensible Borders: An Allon-Oriented Plan
territorial_maximalism|Permanent Territorial Control
regional_compromise|Negotiate Territorial Compromises
sinai_negotiation|Sinai and Egyptian Security Interests
westbank_autonomy|Autonomy in the West Bank
golan_review|A Security Settlement for the Golan
gaza_services|A Civil Administration for Gaza
egypt_peace|A Negotiated Peace with Egypt
regional_normalization|A Regional Peace Framework
territory_administration|The Costs of Permanent Administration
annexation_review|Submit Annexation to Parliament'''.splitlines())
DECISIONS=dict(line.split('|',1) for line in '''mapam_split|Organize Mapam as an Independent List
reserve_exercise|Conduct a Reserve Exercise
reserve_mobilize|Temporary Reserve Readiness
negev_productivity|A Negev Vocational Training Project
galilee_productivity|Agricultural Advice in Galilee
shelters|An Additional Civilian Shelter
civil_industry|A Civilian Development Project
office_project|A Municipal Service Center
armi_project|Expand Defense Manufacturing
equipment_trials|Domestic Equipment Trials
debt_repayment|Targeted Debt Repayment
export_mission|Send an Export Delegation
talks_us|Send a Delivery Proposal to Washington
talks_sov|Send a Dialogue Proposal to Moscow
talks_egypt|A Round of Security Talks
talks_pal|Include Municipal Representatives and Palestine
roster_likud|An Early Alternative Likud Foundation
later_shas|Form a Shas List
later_hadash|Found the Hadash Front
constitutional_convention|Convene a Constitutional Convention'''.splitlines())
GROUPS={'state':'State and Knesset','economy':'Economy and Imperia','society':'Society, Education and Integration','defense':'IDF, Defense Industry and Intelligence','diplomacy':'The Cold War and Foreign Policy','territories':'Suez, Borders and Peace'}
SPIRITS={'citizen_army':('Citizen Army and Reserve','The citizen army combines a small standing force with a trained reserve. Readiness and civilian employment must be balanced.'),'histadrut':('Histadrut and the Building Society','The labor federation and cooperative institutions remain major pillars of industrial development and social provision.'),'unity':('The Unity Government of 1969','A broad parliamentary majority provides stability but requires sustained negotiation between distinct political partners.'),'attrition':('The War of Attrition','An unresolved conflict consumes personnel resources. A mutually accepted ceasefire can remove this burden.'),'embargo':('Lessons of the French Embargo','Restricted external deliveries make defense manufacturing harder until reliable contracts or a domestic production programme are established.'),'absorption':('Immigration and Development Gaps','Immigration sustains population growth but requires housing, education and social provision.'),'ambiguity':('Nuclear Ambiguity','A policy of ambiguity supports diplomatic independence without granting weapons or bypassing technology and material requirements.'),'integrated_immigration':('Integrated Immigration','Education, employment and municipal development support continued immigration without the original social-cost surcharge.'),'temporary_readiness':('Temporary Reserve Readiness','A temporary call-up accelerates mobilization but increases personnel expenses and diverts civilian production for sixty days.')}

def apply_english(data):
    groupmap={g['id']:g for g in data['groups']}
    for g in data['groups']:
        if g['party'] is not None:g['label'],g['description']=PARTIES[g['party']][:2]
        elif g['id'].startswith('outlook_'):
            label={'western':'Western','emerging':'Emerging','salafist':'Salafist','nonaligned':'Non-Aligned','nationalist':'Nationalist'}[g['outlook']]
            g['label']=label+' Outlook';g['description']='Build a political base, earn a government mandate and unlock the programme of the governing party.'
        else:g['label']=GROUPS[g['id']];g['description']='A shared state branch whose institutional achievements survive changes of government.'
        g['history']=g['description']
    for n in data['nodes']:
        key=n['id'].removeprefix('ISR70_');g=groupmap[n['group']]
        if key in COMMON:n['label']=COMMON[key]
        elif g['party'] is not None:
            suffix=key.split('_',1)[1];party=PARTIES[g['party']]
            names={'mandate':party[0]+': A Government Mandate','institution':party[2],'ea':party[3],'eb':party[4],'ca':party[5],'cb':party[6],'finish':party[7]}
            n['label']=names[suffix.removesuffix('_deepen')]+(': Implementation' if suffix.endswith('_deepen') else '')
        else:n['label']=g['label']+': '+{'debate':'A New Direction','campaign':'A Social Base','mandate':'A Government Mandate'}[key.rsplit('_',1)[1]]
        n['note']=g['description']
        n['description']=g['description']+' '+(('The governing party must decide which institutions and policies to strengthen. Programme modifiers apply only while this party governs.') if g['party'] is not None else 'Investments, diplomacy and public institutions must match the resources and circumstances of the country.')
    for d in data['decisions']:
        key=d['id'].removeprefix('ISR70_decision_')
        if key.startswith('campaign_'):d['label']=PARTIES[int(key.split('_')[1])][0]+': Political Campaign'
        elif key.startswith('found_'):d['label']='Found '+PARTIES[int(key.split('_')[1])][0]
        else:d['label']=DECISIONS[key]
        d['note']='Requires the indicated focus and conditions. '+('May be repeated after the stated cooldown.' if d['repeatable'] else 'This initiative can only be completed once.')
    for key,s in data['idea_definitions'].items():
        if key in SPIRITS:s['label'],s['treatment']=SPIRITS[key]
        else:
            focus=next((n for n in data['nodes'] if n['id']==('ISR70_'+key).removesuffix('_idea')),None)
            s['label']=focus['label'] if focus else key.replace('_',' ').title();s['treatment']='An institutional policy implemented through the national focus tree.'
    for key,s in data['starting_spirits'].items():s.update(data['idea_definitions'][key])
    data['title']='Israel 1970 - State Building, Security and Political Choices';data['status']='Implemented content with English-only localisation; static validation does not replace an in-game test.'
    return data
