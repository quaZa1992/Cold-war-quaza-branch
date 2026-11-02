# IMPERIA COLD WAR — Israel 1970 Version 2.0 researched design proposal.
"""Author a new focus catalogue and preview data, without touching loaded files.

Historical precedents motivate institutions; all numbers are proposed balance.
This is deliberately independent of the installed ISR70 generator/save IDs.
"""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT/'docs/israel_1970_v2'
sys.path.insert(0, str(ROOT/'tools/israel_1970'))
from player_rewards import modifier_line

SOURCES = [
    dict(id='election',title='IPU: Parliamentary Elections, Israel, 28 October 1969',url='https://data.ipu.org/election-summary/PDF/ISRAEL_1969_E.PDF',note='Contemporaneous parties, seats and coalition context.'),
    dict(id='knesset',title='Knesset: splits and mergers',url='https://main.knesset.gov.il/en/mk/apps/faction/general/split-merge',note='Labor/Mapam Alignment, Rafi and Free Center chronology.'),
    dict(id='economy',title='Bank of Israel: Annual Report 1970, Chapter I',url='https://www.boi.org.il/media/e50ggphb/pe_1.pdf',note='Full employment, defence imports, housing, exports and foreign-currency constraints.'),
    dict(id='labour',title='Bank of Israel: Annual Report 1970, Chapter IX',url='https://www.boi.org.il/media/fj5diyww/pe_9.pdf',note='Tripartite wage package, wage bonds, skilled immigration and labour participation.'),
    dict(id='histadrut',title='Histadrut: institutional history',url='https://global.histadrut.org.il/about-the-histadrut/',note='Hevrat HaOvdim, Solel Boneh, enterprises, cooperatives and health provision. Retrospective institutional account.'),
    dict(id='bonds',title='Israel Bonds: history since 1951',url='https://israelbonds.com/celebrating-75-years/',note='Diaspora bonds are borrowing, distinct from charitable grants.'),
    dict(id='absorption',title='JTA: new absorption ministry, 4 September 1968',url='https://www.jta.org/archive/israel-opens-gates-to-czechs-allon-explains-new-immigration-functions',note='Contemporaneous evidence for the ministry, ulpan and credential/settlement assistance.'),
    dict(id='netafim',title='Netafim: company origins',url='https://www.netafim.com/en/Netafim-irrigation-company-about-us/',note='Hatzerim and drip irrigation in 1965. No 1990s product lines are backdated.'),
    dict(id='mekorot',title='Mekorot: institutional history',url='https://www.mekorot-int.com/our-history/',note='The National Water Carrier already exists in 1970; this design expands distribution and maintenance.'),
    dict(id='technion',title='Technion: computing faculty founded in 1969',url='https://www.technion.ac.il/en/blog/2019/11/50-years-for-technions-faculty-of-computer-science/',note='Early specialist education, not the later venture-capital economy.'),
    dict(id='iai',title='Israel Aircraft Industries: history',url='https://www.iai.co.il/about/history/',note='Gabriel, ELTA, business aircraft and Arava precede or enter the 1970s. Dates concern development, not instant delivery.'),
    dict(id='merkava',title='Ministry of Defense: tank programme origins',url='https://www.mod.gov.il/en/departments/merkava-and-armored-vehicles-directorate',note='1970 programme decision, Tal and repair-facility origins. Operational Merkava is a later outcome.'),
    dict(id='mashav',title='MASHAV: agency history',url='https://mashav.mfa.gov.il/',note='Development cooperation established in 1958; agreements still require the RP recipient.'),
    dict(id='occupation',title='UN Security Council commission: settlements, 1979',url='https://www.un.org/unispal/document/auto-insert-182452/',note='Retrospective evidence concerning post-1967 settlement and military administration. Foreign-control footholds below are explicitly an RP abstraction.'),
]

GROUPS, NODES = [], []
def group(key, label, subtitle, col, row, party=None, gate=None):
    g=dict(id=key,label=label,subtitle=subtitle,kind='party' if party is not None else 'national',
           party_slot=party,gate=gate,origin=[7+col*14,row])
    GROUPS.append(g)
    return key

def E(label,value,tone='neutral',**extra):
    return dict(label=label,value=value,tone=tone,**extra)
def cash(share):
    return E('Treasury',f'{share:+g}% of annual GDP','gain' if share>0 else 'cost',native_key='treasury',amount=share/100,scope='once')
def debt(share):
    return E('Public Debt',f'{share:+g}% of annual GDP','cost' if share>0 else 'gain',native_key='debt',amount=share/100,scope='once')
def paid(share):
    return [cash(-share)]
def unlock(label):
    return E('Unlocks Decision',label)
def research(category,uses=1,bonus=50):
    return E('Research Bonus',f'{uses} x {bonus}%: {category}','gain')
def asset(state,building,levels=1):
    return [E(state+': Shared Building Slots',f'+{levels}','gain'),E(state+': '+building,f'+{levels}','gain')]
def budget(label,share,weeks=None):
    # Shares describe a weekly amount, never an unconverted annual payment.
    return E(label,f'{share:+g}% of annual GDP per week'+(f' for {weeks} weeks' if weeks else ''),
             'gain' if share>0 else 'cost',native_key='weekly_budget',amount=share/100,scope=weeks or 'ongoing')
def opinion(label,value):
    return E(label+' Opinion',f'{value:+g}','gain' if value>0 else 'cost')

def f(g,key,label,x,y,description,pre=(),mods=None,effects=(),cost=0,requirements=(),sources=(),
      icon='menorah',days=35,programme=None,mechanics=(),status='Historical basis',history_note=''):
    origin=next(row['origin'] for row in GROUPS if row['id']==g)
    rows=[]
    if cost: rows+=paid(cost)
    for k,v in (mods or {}).items():
        line=modifier_line(k,v)
        title,value=line.split(': ',1)
        negative_good=k.endswith('_cost_multiplier_modifier') or k in ('supply_consumption_factor','training_time_army_factor','receiving_investment_cost_modifier','interest_rate_multiplier_modifier','corruption_cost_factor')
        rows.append(E(title,value,'gain' if (v<0 if negative_good else v>0) else 'cost',native_key=k,amount=v,scope='programme'))
    rows+=list(effects)
    conditions=list(requirements)
    gg=next(row for row in GROUPS if row['id']==g)
    if gg['gate']:conditions.insert(0,gg['gate'])
    fullid='ISR2_'+key
    NODES.append(dict(id=fullid,group=g,label=label,xy=[origin[0]+x,origin[1]+y],days=days,
        description=description,icon='GFX_ISR70_focus_'+icon,pre=[['ISR2_'+p for p in row] if isinstance(row,(list,tuple)) else ['ISR2_'+row] for row in pre],
        exclusive=[],effects=rows,requirements=conditions,
        history=dict(status=status,sources=list(sources or (['election'] if gg['party_slot'] is not None else ['economy'])),note=history_note),
        mechanics=list(mechanics),programme=programme or ('Governing programme' if gg['party_slot'] is not None else 'Permanent'),
        modifiers=mods or {}))
    return key

def exclusive(*keys):
    for node in NODES:
        if node['id'] in {'ISR2_'+key for key in keys}:
            node['exclusive']=['ISR2_'+key for key in keys if 'ISR2_'+key!=node['id']]


def national_programmes():
    g=group('institutions','The Republic and Its Bargains','A parliamentary state with institutions stronger than any one cabinet.',0,0)
    f(g,'cabinet_ledger','Open the Cabinet Ledger',0,0,'A coalition cannot govern by invoking national necessity for every expenditure. Present the competing claims of defence, housing and civil administration to the Knesset.',effects=[unlock('Publish the Coalition Budget'),E('Political Power','+60','gain')],icon='knesset_speech')
    f(g,'broad_coalition','A Cabinet across the Aisle',-2,1,'Bringing the principal parliamentary blocs into the cabinet distributes responsibility for security. Every major appropriation will also need a broader political bargain.',pre=['cabinet_ledger'],mods={'stability_factor':.08,'political_power_factor':-.08},icon='generic_parliament',programme='Cabinet settlement')
    f(g,'working_majority','A Working Parliamentary Majority',2,1,'A narrower cabinet can carry a clear legislative programme. Its ability to govern will depend more closely on the demands of its remaining partners.',pre=['cabinet_ledger'],mods={'political_power_factor':.12,'stability_factor':-.03},icon='generic_parliament2',programme='Cabinet settlement')
    exclusive('broad_coalition','working_majority')
    f(g,'tender_commission','The Civil Service Commission',-2,2,'An open examination and tender system gives engineers and administrators a career beyond party appointments. The reform takes patronage out of the coalition bargain.',pre=[['broad_coalition','working_majority']],cost=.6,mods={'bureaucracy_cost_multiplier_modifier':-.08},effects=[opinion('Industrial Conglomerates',-10)],icon='civil_service')
    f(g,'comptroller','Let the Comptroller Follow the Money',2,2,'Public enterprises, emergency appropriations and municipal grants will answer to the same audit. Some political allies will find their customary contracts harder to defend.',pre=[['broad_coalition','working_majority']],effects=[E('Corruption','-1 level','gain'),opinion('Industrial Conglomerates',-15)],icon='generic_investigate_corruption',cost=.3)
    f(g,'religious_concord','Renew the Religious Status Quo',-2,3,'A renewed parliamentary understanding protects religious institutions without handing them every question of government. Separate educational commitments receive a defined budget.',pre=['tender_commission'],mods={'stability_factor':.05,'education_cost_multiplier_modifier':.06},effects=[opinion('Religious Institutions',15)],icon='jewish_sites_isr',programme='Constitutional settlement')
    f(g,'civil_charter','A Civic Charter for the Republic',2,3,'A common civil register and public-service standard would give the secular state a clearer identity. Religious parties will contest the loss of authority over family and communal affairs.',pre=['comptroller'],mods={'bureaucracy_cost_multiplier_modifier':-.05},effects=[E('Stability','+5%','gain'),opinion('Religious Institutions',-20),unlock('Enact the Civil Registration Statute')],icon='adopt_new_constitiution',status='Alternate policy',programme='Constitutional settlement')
    exclusive('religious_concord','civil_charter')
    f(g,'municipal_tenders','Equal Access to Municipal Tenders',0,4,'Development towns and Arab municipalities need functioning roads, utility connections and access to public contracts. Publish allocations instead of distributing them through informal political intermediaries.',pre=['tender_commission','comptroller'],cost=1.1,effects=asset('Selected Israeli Core State','Infrastructure')+[E('Corruption','-1 level','gain'),unlock('Municipal Engineering Grants')],requirements=['An owned and controlled Israeli core state with infrastructure capacity.'],icon='generic_public_transport',mechanics=['Each municipal grant is paid once. Palestinian occupied territory is not silently treated as an Israeli core.'])

    g=group('capital','Capital from Abroad','An unusually powerful funding network, with debt, obligations and exposure.',1,0)
    f(g,'bond_drive','The Israel Bonds Subscription',0,0,'A development loan can turn overseas confidence into capital at home. Subscribers receive a state obligation, and the treasury must meet its debt service after the campaign ends.',effects=[cash(8),debt(8)],sources=['bonds','economy'],icon='agricultural_banks',days=49,mechanics=['One subscription, one loan. Interest uses the existing MD public-debt economy.'])
    f(g,'absorption_appeal','The Overseas Absorption Appeal',-3,1,'Charitable partners can support homes, language courses and civilian services through the absorption institutions. This support is directed at settlement and welfare needs rather than unrestricted military procurement.',pre=['bond_drive'],effects=[E('Civilian Absorption Appropriation','+4% of annual GDP','gain'),unlock('Agency Housing and Training Grants')],sources=['absorption','labour'],icon='generic_refugee_focus',mechanics=['New proposed appropriation: offsets actual civilian housing/training payments up to the stated total. It is not an unrestricted donation to the military treasury.'],status='Alternate policy')
    f(g,'diamond_desk','The Diamond Bourse Dollar Desk',0,1,'The diamond trade already connects Israel to international finance. A foreign-currency desk can support specialist exporters, but a smaller range of overseas markets will carry more of the economy.',pre=['bond_drive'],cost=.5,mods={'offices_productivity':.10,'mdcw_cw_market_exposure':.10},icon='diamondsare4ever')
    f(g,'citrus_packhouses','Jaffa Citrus Export Houses',3,1,'Packing, refrigeration and marketing can make a familiar export earn more abroad. The resulting income still depends on access to distant customers and their prices.',pre=['bond_drive'],cost=1.2,mods={'agricolture_productivity_modifier':.10,'mdcw_cw_market_exposure':.05},effects=asset('Haifa','Agricultural District'),icon='export_factories')
    f(g,'bonds_plant','Turn Subscriptions into Workshops',-3,2,'Borrowed capital must leave productive assets behind. The development tender funds a civilian plant and the power and transport connections needed to keep it operating.',pre=['absorption_appeal'],cost=3,effects=asset('Haifa','Civilian Factory')+asset('Negev','Civilian Factory'),icon='factory_complex',days=70)
    f(g,'credit_guarantees','An Export Credit Guarantee Book',0,2,'A public guarantee lets smaller exporters accept contracts beyond their own balance sheets. The finance ministry must reserve funds against those commitments.',pre=['diamond_desk'],mods={'receiving_investment_cost_modifier':-.12},effects=[budget('Export Guarantee Provision',-.02,52),unlock('Approve an Export Credit Guarantee')],icon='generic_banking_legislation',mechanics=['New proposed programme: at most two guarantees, each lasting 52 weeks. No automatic payment from another RP country.'])
    f(g,'eilat_link','A Commercial Route through Eilat',3,2,'A southern route gives commerce another outlet when northern access is uncertain. Building it requires maintenance and dependable arrangements with the countries along the route.',pre=['citrus_packhouses'],cost=1,effects=asset('Negev','Infrastructure'),mods={'imp_sanction_resistance':.10},icon='oil_pipelines',requirements=['Israel owns and controls the Negev.'],sources=['economy'],days=49)
    f(g,'sterilise_inflow','Hold a Foreign-Currency Cushion',-2,3,'Reserving part of the capital inflow reduces the need to borrow during the next import shock. Fewer funds are available for immediate construction.',pre=['bonds_plant','credit_guarantees'],cost=2,mods={'interest_rate_multiplier_modifier':-.35,'imp_sanction_resistance':.10},icon='generic_financial_markets',programme='Capital allocation')
    f(g,'capital_acceleration','Let Development Spend the Inflow',2,3,'Release the reserve into productive construction while the funds are available. The treasury accepts dearer borrowing if the next external shock arrives before the projects mature.',pre=['credit_guarantees','eilat_link'],cost=2,mods={'production_speed_buildings_factor':.12,'interest_rate_multiplier_modifier':.25},icon='construction_engineering',programme='Capital allocation')
    exclusive('sterilise_inflow','capital_acceleration')
    f(g,'refinancing','A Long-Term Debt Calendar',0,4,'Match the repayment calendar to the time required for development assets to earn an income. The treasury exchanges part of its short-term flexibility for more predictable debt service.',pre=[['sterilise_inflow','capital_acceleration']],cost=.7,mods={'interest_rate_multiplier_modifier':-.20},effects=[unlock('Repay a Development Loan')],icon='generic_banking_legislation')

    g=group('absorption','People, Skills and a Place to Live','Three paid participation reforms. Added workforce reaches +15% in total.',2,0)
    f(g,'ulpan_jobs','An Ulpan with a Job at the End',0,0,'Language instruction becomes part of an employment service rather than a waiting room. Trained interpreters and placement officers help newcomers use skills they already possess.',cost=.7,mods={'total_workforce_modifier':.05,'education_cost_multiplier_modifier':.04},sources=['labour','absorption'],icon='school_is_in',days=49)
    f(g,'recognise_qualifications','Recognise the Engineer and the Nurse',-2,1,'Hospitals and factories cannot afford to leave qualified arrivals in unsuitable work. Professional boards will run conversion courses and practical examinations.',pre=['ulpan_jobs'],cost=.6,effects=[research('Electronics'),research('Industry')],mods={'education_cost_multiplier_modifier':.03},sources=['labour','absorption'],icon='bel_prioritizetechnicaleducation')
    f(g,'ort_workshops','ORT Workshops beyond the Coast',2,1,'Industrial training in development towns makes skilled employment possible without relocating every household to the coastal cities. Instructors and workshop equipment require a continuing education commitment.',pre=['ulpan_jobs'],cost=.9,mods={'total_workforce_modifier':.05,'education_cost_multiplier_modifier':.04},effects=[research('Industry')],sources=['labour'],icon='generic_working_class_family',days=49)
    f(g,'housing_connections','Homes Connected to Work',-3,2,'A housing estate without a road to employment merely moves a shortage elsewhere. Fund the utility links, transport and workshops around the new homes.',pre=['recognise_qualifications'],cost=1.8,effects=asset('Negev','Office District')+asset('Negev','Infrastructure'),icon='generic_construct_public_housing',requirements=['Israel owns and controls the Negev.'])
    f(g,'community_clinics','Kupat Holim in the Development Towns',0,2,'A clinic and a reliable referral system make a new town a place where families can remain. The health service must maintain staff outside its most convenient urban centres.',pre=['recognise_qualifications','ort_workshops'],cost=.6,mods={'health_cost_multiplier_modifier':.06},effects=[E('Stability','+5%','gain'),opinion('Labor Unions',10)],sources=['histadrut','labour'],icon='generic_healthcare')
    f(g,'daycare_shifts','Day Care for the Second Shift',3,2,'Childcare and suitable shift arrangements let more women remain in paid employment. The gain comes from participation, supported by a larger public-service budget.',pre=['ort_workshops'],cost=.8,mods={'total_workforce_modifier':.05,'social_cost_multiplier_modifier':.07},sources=['labour'],icon='generic_female_rights',days=49)
    f(g,'hearing_towns','Hear the Neighbourhood Committees',-2,3,'Newspapers and ministries do not experience a crowded neighbourhood in the same way as its residents. Give local committees a public hearing and a budgeted repair programme before resentment hardens.',pre=['housing_connections','community_clinics'],cost=.8,effects=[E('Stability','+6%','gain'),unlock('Development-Town Repair Grants')],icon='generic_workers_rights',status='Alternate policy',history_note='Responds to documented social gaps; it does not force a Black Panthers event or create that later organisation at the 1970 start.')
    f(g,'scholarships','Scholarships across the Social Divide',2,3,'Merit should not depend on the ability to leave home for years of study. Targeted bursaries and preparatory courses open technical education to households excluded by its incidental costs.',pre=['community_clinics','daycare_shifts'],cost=.8,mods={'research_speed_factor':.03,'education_cost_multiplier_modifier':.05},effects=[research('Electronics')],icon='universities',sources=['technion','labour'])
    f(g,'settled_skills','A Skilled Workforce That Stays',0,4,'Housing, professional recognition and practical training can turn arrival into a lasting career. The objective is a productive civilian economy with room for its citizens, not a limitless supply of reservists.',pre=['hearing_towns','scholarships'],cost=.5,mods={'civilian_factories_productivity':.08,'offices_productivity':.06},icon='fund_social_integration_programs',days=49,mechanics=['The three participation focuses add exactly +15% workforce together. No party, settlement or military focus adds further workforce. No population is removed from another RP country.'])

    g=group('water','Water, Workshops and the Negev','Turn scarce water and practical engineering into national advantages.',3,0)
    f(g,'carrier_workshops','Keep the National Carrier Running',0,0,'The National Water Carrier is already in service. Pumps, stores and repair crews determine whether its promise reaches the farms at the end of the network.',cost=.7,mods={'industry_repair_factor':.10},effects=[research('Agriculture')],sources=['mekorot'],icon='irrigation_pipes')
    f(g,'hatzerim','Hatzerim: More Crop per Drop',-2,1,'A kibbutz workshop can become an exporter of a practical answer to arid farming. Demonstration plots will make the new irrigation method usable beyond its first customers.',pre=['carrier_workshops'],cost=.8,mods={'agricolture_productivity_modifier':.12},effects=[research('Agriculture')],sources=['netafim'],icon='irrigation_canals',days=49)
    f(g,'negev_water','Connect the Southern Farms',2,1,'Distribution lines and roads must reach the same communities. Expanding cultivated land brings higher pumping and maintenance costs with it.',pre=['carrier_workshops'],cost=1.4,effects=asset('Negev','Agricultural District')+asset('Negev','Infrastructure'),sources=['mekorot'],icon='generic_agriculture',requirements=['Israel owns and controls the Negev.'])
    f(g,'water_discipline','Meter Water before Expanding Acreage',-3,2,'Use the next investment to reduce waste in existing cultivation. Farmers receive a more dependable system, but the ministry postpones its next wave of new districts.',pre=['hatzerim'],cost=.5,mods={'agricolture_productivity_modifier':.08,'production_speed_agriculture_district_factor':-.08},sources=['mekorot','netafim'],icon='agricultural_modernization',programme='Water priority')
    f(g,'reclamation','The Reclamation Budget',0,2,'Water used in the towns need not be lost to every other purpose. A paid treatment and distribution programme broadens the network without pretending that water is unlimited.',pre=['hatzerim','negev_water'],cost=1,mods={'agricolture_productivity_modifier':.06},effects=[budget('Water Treatment Maintenance',-.015)],sources=['mekorot'],icon='generic_electricity',status='Alternate policy')
    f(g,'new_acreage','New Districts in the Negev',3,2,'Concentrate the capital on additional cultivated districts. The productive gain arrives with a larger electricity and maintenance bill for the water authority.',pre=['negev_water'],cost=1.6,effects=asset('Negev','Agricultural District',2)+[budget('Southern Water Maintenance',-.02)],sources=['mekorot'],icon='agricultural_mechanization',programme='Water priority')
    exclusive('water_discipline','new_acreage')
    f(g,'precision_tools','Machine Tools from the Kibbutz',-2,3,'Cooperative workshops can manufacture components as well as repair farm equipment. An industrial order book gives rural employment a second source of income.',pre=[['water_discipline','new_acreage'],'reclamation'],cost=1.5,effects=asset('Negev','Civilian Factory'),sources=['netafim','histadrut'],icon='generic_improve_industry',days=49)
    f(g,'irrigation_exports','Sell the Irrigation System',2,3,'Export the equipment with the knowledge needed to use it. Overseas customers gain a useful system while Israeli suppliers gain a contract rather than an automatic diplomatic alignment.',pre=['reclamation'],effects=[unlock('Offer a Precision-Irrigation Contract')],sources=['netafim','mashav'],icon='african_diplomacy',mechanics=['Recipient-approved offer: buyer pays 0.8% of its GDP once and receives +10% agricultural productivity for 104 weeks. Israel receives that payment, pays setup equal to 0.3% of its own GDP and carries maintenance equal to 0.005% of its own GDP per week for 104 weeks. One contract per buyer.'])
    f(g,'applied_engineering','An Exportable School of Engineering',0,4,'Universities, agricultural stations and suppliers will share testing facilities. The programme turns specific engineering problems into products without promising the later venture-capital economy overnight.',pre=['precision_tools','irrigation_exports'],cost=.7,effects=[research('Agriculture',2),research('Industry')],sources=['technion','netafim'],icon='the_research_department',days=49)

    g=group('reserves','A Nation in Reserve','A sharp army whose mobilisation has a visible civilian bill.',0,8)
    f(g,'reserve_register','The Reservist and His Workshop',0,0,'The same people keep factories working and reserve formations ready. A common register lets the cabinet see what a call-up will cost before issuing it.',cost=.5,effects=[unlock('Limited Reserve Exercise'),unlock('National Reserve Call-Up'),E('Army Experience','+25','gain')],sources=['labour','economy'],icon='ast_upgrade_reserves',mechanics=['Proposed choices: exercise costs 0.2% GDP and gives +20 army XP with -5% civilian productivity for 35 days. National call-up gives +25% mobilisation speed and +8% division organisation, costs 0.04% GDP per week, and gives -12% civilian productivity and -8% office productivity for at most 70 days. It requires an actual war or an RP-authorised security emergency. No workforce-size penalty.'])
    f(g,'essential_workers','Keep Essential Workshops Open',-2,1,'Reserve assignments can protect the technicians who keep water, repair and power services functioning. Readiness will improve more slowly in units that release those specialists.',pre=['reserve_register'],cost=.4,mods={'industry_repair_factor':.15,'mobilization_speed':-.08},sources=['labour'],icon='generic_support_equipment',programme='Reserve priority')
    f(g,'ready_depots','Depots before Another Division',2,1,'A reservist reaches a useful formation only if its stores and transport are ready. Permanent depot staff cost money even when no mobilisation order is issued.',pre=['reserve_register'],cost=.8,mods={'mobilization_speed':.20,'supply_consumption_factor':-.05},effects=[budget('Reserve Depot Establishment',-.015)],icon='improve_supply_distribution_methods',programme='Reserve priority')
    exclusive('essential_workers','ready_depots')
    f(g,'armoured_school','Tal and the Armoured School',-3,2,'Tank crews need maintenance, gunnery and practical exercises more than another ceremonial command. A stronger school also means paying for vehicles, instructors and fuel.',pre=[['essential_workers','ready_depots']],cost=.7,effects=[E('Army Experience','+50','gain'),research('Armor',2)],sources=['merkava'],icon='doctrine_tank_warfare',days=49)
    f(g,'canal_works','Fortify the Canal Positions',0,2,'A defended position can save lives, but maintaining a fixed line commits the army to a particular frontier. Construction proceeds only where Israel actually controls the ground.',pre=[['essential_workers','ready_depots']],cost=1.2,effects=[E('Selected Controlled Sinai Province: Shared Building Slots','+2','gain'),E('Selected Controlled Sinai Province: Land Forts','+2','gain'),budget('Canal Position Maintenance',-.015)],requirements=['Israel controls Sinai and an eligible frontier province with fort capacity.'],icon='construction_engineering',programme='Frontier doctrine')
    f(g,'mobile_reserve','A Mobile Reserve behind the Front',3,2,'Keep a formation able to reinforce the threatened sector rather than distribute every unit among static positions. This requires a larger standing transport and personnel establishment.',pre=[['essential_workers','ready_depots']],cost=.8,mods={'planning_speed':.15,'supply_consumption_factor':-.05,'personnel_cost_multiplier_modifier':.06},icon='generic_army_tanks2',programme='Frontier doctrine')
    exclusive('canal_works','mobile_reserve')
    f(g,'after_action','A College for Lessons Learned',-2,3,'Junior commanders and technicians will be heard alongside the general staff. Turn exercise reports and combat experience into practical training before memory becomes institutional certainty.',pre=['armoured_school'],cost=.5,effects=[research('Land Doctrine'),E('Army Experience','+25','gain')],icon='generic_officer')
    f(g,'home_front','Clinics behind the Front',2,3,'The reserve system leaves families and workplaces exposed to the same emergency. Shelter construction and medical preparation make mobilisation a public responsibility rather than a military abstraction.',pre=[['canal_works','mobile_reserve']],cost=.8,effects=asset('Tel Aviv','Civilian Shelter')+[E('Casualty Trickleback','+10%','gain'),budget('Emergency Medical Establishment',-.01)],icon='generic_healthcare')
    f(g,'bounded_callup','A Readiness Calendar the Economy Can Bear',0,4,'Publish a reserve calendar that the army can train against and civilian employers can plan around. Emergency mobilisation remains available, but cannot become a permanent source of cheap readiness.',pre=['after_action','home_front'],cost=.6,effects=[E('Limited Reserve Exercise Duration','-7 days','gain'),E('National Reserve Call-Up Civilian Productivity Penalty','-12% becomes -8%','gain')],icon='conscription',mechanics=['Improves the named temporary call-up programme only. No permanent army bonus or extra workforce is added.'])

    g=group('arsenal','An Arsenal beyond the Embargo','Repair, adapt and eventually build. Expensive choices with civilian consequences.',1,8)
    f(g,'bedek','Bedek before a New Airframe',0,0,'Repair and overhaul are the foundation of aviation independence. Expand that capability before committing the country to an aircraft it cannot maintain.',cost=1.4,effects=asset('Tel Aviv','Military Factory')+[research('Aircraft')],sources=['iai'],icon='generic_air_command',days=49)
    f(g,'nesher','Fund the Nesher Engineering Line',-3,1,'Developing an indigenous fighter requires tooling, test work and imported components. Allocate a real engineering budget rather than treating a national name as a finished aircraft.',pre=['bedek'],cost=1.8,effects=[research('Aircraft',2,75),budget('Nesher Development',-.025,52)],sources=['iai'],icon='generic_air_fighter_new',days=70,mechanics=['Research and development only. No automatic 1970 fleet and no technology-year bypass.'])
    f(g,'elta','ELTA: Electronics at the Workbench',0,1,'Radar and communications suppliers can share a practical testing establishment. Reserving their work for defence makes the military customer less dependent on foreign deliveries.',pre=['bedek'],cost=.9,effects=[research('Military Electronics',2)],mods={'production_factory_efficiency_gain_factor':.08},sources=['iai'],icon='generic_radar_instillation')
    f(g,'arava','Give the Arava a Civilian Order Book',3,1,'A utility aircraft and a business-aviation workshop can earn income outside the defence budget. Civil certification and customer support require attention from the same engineers.',pre=['bedek'],cost=1,effects=asset('Tel Aviv','Civilian Factory')+[research('Medium Aircraft')],sources=['iai'],icon='generic_airline_industry',days=49)
    f(g,'tal_tank','Authorise Tal\'s Tank Programme',-3,2,'A tank programme begins with repair facilities, comparative trials and a design office. Crew protection is a design objective, and production independence is a long-term commitment.',pre=['nesher'],cost=1.6,effects=[research('Armor',2,75),budget('Domestic Tank Development',-.03,78)],sources=['merkava'],icon='generic_army_tanks3',days=70,mechanics=['Opens the domestic tank development project. It does not grant an operational Merkava at the scenario start.'])
    f(g,'gabriel','Gabriel and the Missile Boats',0,2,'A domestic anti-ship weapon needs vessels, training and reliable maintenance. Naval investment provides another answer to supplier uncertainty without replacing the whole fleet overnight.',pre=['elta'],cost=1.1,effects=[research('Corvettes'),research('Military Electronics')],sources=['iai'],icon='isr_navy',days=49)
    f(g,'civil_spillover','Open the Civilian Supplier Catalogue',3,2,'Civilian firms can use test equipment and subcontracting experience developed for defence. Some of the laboratory schedule will move away from military work.',pre=['arava','elta'],cost=.6,mods={'civilian_factories_productivity':.08,'offices_productivity':.05,'production_speed_arms_factory_factor':-.05},sources=['iai','technion'],icon='isr_computer',programme='Engineering priority')
    f(g,'defence_priority','Give Defence the Test Benches',-2,3,'Concentrate the testing establishment on the urgent military order book. The gain in defence production comes with a smaller civilian share of the engineering effort.',pre=['tal_tank','gabriel'],cost=.8,mods={'industrial_capacity_factory':.10,'production_speed_industrial_complex_factor':-.05},sources=['iai','merkava'],icon='armisrael',programme='Engineering priority')
    exclusive('civil_spillover','defence_priority')
    f(g,'technion_computing','The Technion\'s First Computing Classes',2,3,'The new computing faculty can supply engineers to laboratories and industry. A small country must fund its instructors and students before expecting a large research sector.',pre=['arava'],cost=.8,mods={'research_speed_factor':.04,'education_cost_multiplier_modifier':.06},effects=[research('Electronics',2)],sources=['technion'],icon='isr_computer',days=49)
    f(g,'arms_exports','An Export Order Is a Contract',0,4,'Domestic workshops need an order book larger than Israel alone can provide. A foreign customer must agree to an actual equipment sale, its price and delivery schedule.',pre=[['civil_spillover','defence_priority'],'technion_computing'],effects=[unlock('Offer an Israeli Equipment Production Contract')],sources=['iai'],icon='generic_positive_trade_relations_gold',mechanics=['New proposed contract: 250 units of a specified, mutually accessible infantry-equipment model. The buyer pays 1% of its annual GDP once; Israel receives it. Israel pays 0.4% of its own annual GDP and transfers 250 actual stockpiled units at delivery. While pending, factory output is -5% for at most 26 weeks. No delivery without the actual stockpile; cancellation refunds the buyer. Recipient approval is mandatory.'])
    f(g,'ambiguity','A Deliberate Policy of Ambiguity',-3,4,'Keep the strategic programme behind a restricted appropriation. Secrecy changes how the state presents its policy; it does not create weapons or remove the cost of nuclear research.',pre=['tal_tank'],effects=[unlock('Classified Nuclear Research Appropriation'),budget('Strategic Research Office',-.015)],icon='nuclear_research_lab',mechanics=['Integrates with the existing uranium, enrichment and nuclear-intelligence systems. Zero free uranium, mines, warheads or automatic foreign guarantees.'],status='Alternate policy')

    g=group('diplomacy','Connections without a Script','Offer cooperation and bargaining positions. Other players retain their decisions.',2,8)
    f(g,'foreign_service','A Foreign Service for a Small State',0,0,'Diplomats, commercial officers and technical advisers can open doors that military strength cannot keep open by itself. Give their work a permanent establishment.',cost=.5,effects=[unlock('Open a Bilateral Commercial Mission')],mods={'foreign_influence_defense_modifier':.08},sources=['mashav'],icon='foreign_diplomacy')
    f(g,'mashav','MASHAV: Agronomists at the Embassy',-3,1,'Technical cooperation can make an embassy useful to its host. An invitation must come from the partner government, and expertise sent abroad still has a budget at home.',pre=['foreign_service'],effects=[unlock('Offer a MASHAV Agricultural Mission')],sources=['mashav'],icon='african_diplomacy',mechanics=['If accepted: Israel pays setup of 0.3% of its own GDP and 0.01% of its own GDP per week for 52 weeks; receives +10 bilateral opinion. Recipient receives one 50% agriculture research bonus and +5% agricultural productivity for 52 weeks, and pays no fee. Both countries receive +10 bilateral opinion. No workforce is removed.'])
    f(g,'washington','Put a Procurement Offer to Washington',0,1,'Present a defined procurement and training request to the United States. Israeli planning can use an accepted offer; it cannot assume that another government has already signed it.',pre=['foreign_service'],effects=[unlock('Offer a US Aviation Training Agreement')],sources=['iai'],icon='generic_air_army_cooperation',status='Alternate policy',mechanics=['If accepted: Israel pays 0.8% of its own GDP to the United States and receives +35 air XP and one 50% aircraft research bonus. The United States receives the same payment and both countries receive +15 bilateral opinion. There is no automatic alliance, foreign spending mandate or free aircraft.'])
    f(g,'european_orders','A European Civilian Order Book',3,1,'Expand commercial relations through a civilian agreement that can survive disagreement over arms. The partner receives a concrete commercial proposal, not a change of alignment.',pre=['foreign_service'],effects=[unlock('Offer a Civilian Workshop Partnership')],icon='europe_trade',status='Alternate policy',mechanics=['If accepted: each country pays 0.5% of its own GDP once and receives +5% civilian-industry productivity for 104 weeks. Israel receives one 50% industry research bonus; partner receives one 50% electronics research bonus. Both receive +10 bilateral opinion.'])
    f(g,'jarring_channel','Keep a Channel to the Mediator',-2,2,'A diplomatic channel keeps proposals moving without obliging the cabinet to accept them. Territorial concessions and security guarantees must be negotiated with the governments concerned.',pre=['foreign_service'],effects=[unlock('Propose a Bilateral Ceasefire'),unlock('Reopen Territorial Talks')],icon='olive_branch',status='Alternate policy',mechanics=['No dated peace event, automatic refusal, automatic war, compulsory border or penalty for ignoring a historical plan. No focus forces Egypt, Jordan or Palestine to sign.'])
    f(g,'commercial_independence','A Commercial Service beyond One Patron',2,2,'Support several trading relationships instead of treating a single foreign capital as the answer to every economic problem. Maintaining the wider service has a recurring price.',pre=[['mashav','european_orders']],cost=.6,mods={'imp_sanction_resistance':.10},effects=[budget('Commercial Mission Network',-.01)],icon='generic_positive_trade_relations_gold')
    f(g,'liaison_limits','Put Limits on Intelligence Liaison',0,3,'Foreign intelligence assistance must have a defined remit and an Israeli authorising minister. A liaison agreement can improve technical work without conferring open-ended access.',pre=['washington','commercial_independence'],effects=[unlock('Offer a Limited Signals Liaison')],icon='isr_mossad',status='Alternate policy',mechanics=['If accepted: each country pays 0.25% of its own GDP once and 0.005% of its own GDP per week for 52 weeks. Each receives one 50% encryption research bonus and +10% foreign-influence defence for 52 weeks. Each may suspend the liaison. No automatic intelligence target is selected.'])

    g=group('territories','Territory, Settlements and Their Price','Separate administration, controlled construction and unilateral foreign footholds.',3,8)
    f(g,'occupation_accounts','Four Frontiers, Four Administration Bills',0,0,'The West Bank, Gaza, Sinai and the Golan do not present the same administrative problem. Show their separate military, civil-service and supply commitments in the budget.',effects=[unlock('Review Territorial Administration'),unlock('Fund or Withdraw a Settlement Programme')],sources=['occupation'],icon='isr_focus_egypt_israeli_tension',mechanics=['Starting resistance and budget burdens already apply before this focus. The focus does not create a free period of occupation or require a war sequence.'])
    f(g,'civil_admin','Pay for a Civil Administration',-3,1,'A functioning military administration needs records, courts, utilities and paid staff. Better administration can reduce friction while keeping its cost visible to the cabinet.',pre=['occupation_accounts'],cost=.6,effects=[E('Controlled Non-Core Territory: Compliance Gain','+10%','gain'),E('Controlled Non-Core Territory: Local Garrison Requirement','-10%','gain'),budget('Territorial Civil Administration',-.02)],sources=['occupation'],icon='civil_service',requirements=['At least one of West Bank, Gaza, Sinai or Golan is controlled by Israel and is not an Israeli core.'])
    f(g,'controlled_sites','Nahal: A Site behind the Perimeter',0,1,'Military-backed settlement development can only build on ground the state actually controls. Agricultural assets and a protected access road are paid projects, with a continuing security establishment.',pre=['occupation_accounts'],effects=[unlock('Controlled Settlement Development: West Bank'),unlock('Controlled Settlement Development: Gaza'),unlock('Controlled Settlement Development: Sinai'),unlock('Controlled Settlement Development: Golan')],sources=['occupation'],icon='generic_paramilitary',mechanics=['For each selected controlled area: treasury -1.5% of Israeli GDP, +3 state shared slots, +1 agricultural district, +1 infrastructure and +1 land fort. Israeli police cost +3%, personnel cost +2%; state agricultural productivity +8%, garrison requirement +10%. Three paid development tiers at most; each new tier has the same extra assets and charges. Actual control, ownership and province capacity are checked separately.'])
    f(g,'foreign_footholds','Back a Foothold beyond Israeli Control',3,1,'Fund an illegal settlement presence where Israel does not control the territory. Its external supply and investment network benefits Israel while imposing disruption and administrative pressure on the host.',pre=['occupation_accounts'],effects=[unlock('Unilateral Foothold: West Bank'),unlock('Unilateral Foothold: Gaza'),unlock('Unilateral Foothold: Sinai'),unlock('Unilateral Foothold: Golan')],sources=['occupation'],icon='generic_collaborate_local_elites',status='RP abstraction',history_note='Supporting a sustained foothold without territorial control is a proposed multiplayer abstraction, not a claim that this was a normal historical option in 1970.',mechanics=['Each selected area costs Israel 1% of its GDP once and 0.015% of its GDP per week while funded. Israel: office productivity +4%, agricultural productivity +3%. Actual host: agricultural productivity -3%, police cost +4%, bureaucracy cost +3%. State: local factory access -5 percentage points, local supplies -8%. Maximum two funded foreign areas. No host approval, payment to host, positive host reward, free construction, control transfer or core.'])
    f(g,'west_bank_projects','The West Bank Access-Road Programme',-3,2,'New roads and sites give the settlement programme a physical presence in the West Bank. Maintaining them raises the price of control and the burden on Palestinian institutions.',pre=['controlled_sites'],requirements=['Israel controls the West Bank.'],effects=[unlock('First West Bank Settlement Development')],icon='generic_road_construction',mechanics=['Uses the controlled project terms shown in Nahal. If Palestine exists with a West Bank core, each delivered tier adds office productivity -4% and bureaucracy cost +4%, up to two pressure tiers in this area. This consequence does not require Palestinian consent.'])
    f(g,'sinai_projects','An Agricultural Enclave in Sinai',0,2,'A paid enclave creates a farm, access route and defended position. Its benefit depends on retaining control and maintaining a costly desert connection.',pre=['controlled_sites'],requirements=['Israel controls Sinai.'],effects=[unlock('First Sinai Settlement Development')],icon='irrigation_pipes',mechanics=['Uses the controlled project terms shown in Nahal. It neither annexes Sinai nor removes its starting supply and personnel burden.'])
    f(g,'funded_network','A Funded External Support Network',3,2,'Support offices and transport arrangements keep a foreign foothold connected to the Israeli economy. Expanding the network also enlarges its recurring financial commitment.',pre=['foreign_footholds'],cost=.4,effects=[E('Foreign Foothold Weekly Cost per Area','0.015% becomes 0.02% of annual GDP','cost'),E('Office Productivity per Funded Foothold','+4% becomes +6%','gain')],icon='generic_financial_markets',status='RP abstraction',mechanics=['Still at most two funded foreign areas. Host and Palestinian penalties remain; no construction is granted in uncontrolled territory.'])
    f(g,'palestinian_accounts','Record the Cost to Palestinian Institutions',-3,3,'Settlement projects fragment access to workplaces, land and municipal services. A Palestinian state that exists outside Israeli control still faces these costs when its core territories are affected.',pre=['west_bank_projects'],effects=[E('Palestine per Active West Bank or Gaza Pressure Tier: Office Productivity','-4%','cost'),E('Palestine per Active West Bank or Gaza Pressure Tier: Bureaucracy Cost','+4%','cost'),E('Palestine per Active West Bank or Gaza Pressure Tier: Stability','-2%','cost')],icon='gaza_civic_organizations',mechanics=['Informational consolidation of automatic consequences, not an unlock required to impose them. Two tiers per area, four total. Foreign footholds count as one tier per affected area. Palestine receives no establishment vote. No population or workforce-size penalty.'])
    f(g,'cap_projects','Cap New Civilian Commitments',0,3,'Freeze new sites while retaining the ability to maintain or fund existing ones. A cabinet can limit its commitments without signing a territorial agreement on behalf of another government.',pre=['occupation_accounts'],effects=[unlock('Freeze New Settlement Projects'),E('Existing Settlement Maintenance','-20%','gain')],icon='generic_civilian_oversight',programme='Territorial commitment policy',status='Alternate policy',mechanics=['The reduction applies only while no new project starts. Starting another site restores the full maintenance bill. This is not a peace agreement.'])
    f(g,'negotiated_terms','Put Territory on the Negotiating Table',2,3,'The cabinet can propose withdrawal, compensation or a security arrangement. The other RP country receives the actual territorial offer and retains the right to refuse it.',pre=['civil_admin'],effects=[unlock('Offer a Negotiated Territorial Settlement'),unlock('Offer Funded Palestinian Service Compensation')],icon='beginnegotiations',status='Alternate policy',mechanics=['Compensation offer if accepted: Israel pays 0.02% of its own GDP per week to Palestine for 52 weeks; Palestine receives the identical payment and the chosen area pressure is capped at one tier for that period. Israel gains +10 bilateral opinion; Palestine gains +10 bilateral opinion. It neither authorises new settlements nor removes host penalties. Territorial terms have no preset borders or compulsory Rogers outcome.'])


def political_programmes():
    g=group('alignment','Alignment: the Histadrut State','A wage bargain, public enterprises and Sapir\'s development priorities.',0,16,3,'Alignment is in Power.')
    f(g,'package_deal','Negotiate the 1970 Package Deal',0,0,'The government, Histadrut and employers can negotiate wages and investment together. A settlement must say who receives cash, who holds state obligations and who carries the social contributions.',effects=[unlock('Conclude a Tripartite Wage Settlement'),opinion('Labor Unions',15)],sources=['labour'],icon='focuselectmapai',mechanics=['Direct governing-party entry. No focus is spent installing the already-governing Alignment.'])
    f(g,'wage_bonds','Wages Partly in State Bonds',-2,1,'Preserve funds for development by meeting part of the wage settlement with state obligations. Workers receive a claim on the treasury rather than the same increase in immediate spending power.',pre=['package_deal'],mods={'industrial_capacity_factory':.08},effects=[debt(1.5),opinion('Labor Unions',-10)],sources=['labour'],icon='generic_union_agreement',programme='Wage settlement: 365 days',mechanics=['Does not pay 1.5% GDP into the treasury as a second free loan. Proposed bond amount is balance, not a historical measurement.'])
    f(g,'cash_wages','Pay the Wage Settlement in Cash',2,1,'A cash settlement supports household purchasing power and gives the government a clearer agreement with labour. Public funds will move to wages before the next development tender.',pre=['package_deal'],cost=1.5,mods={'stability_factor':.06},effects=[opinion('Labor Unions',15)],sources=['labour'],icon='generic_workers_rights',programme='Wage settlement: 365 days')
    exclusive('wage_bonds','cash_wages')
    f(g,'koor','Koor\'s Machine Shops',-3,2,'The labour movement already possesses an industrial organisation able to carry state orders. A major tender expands its workshops while favouring an established conglomerate over smaller competitors.',pre=['wage_bonds'],cost=2.4,effects=asset('Haifa','Civilian Factory')+asset('Tel Aviv','Military Factory')+[opinion('Small and Medium Business Owners',-10)],sources=['histadrut'],icon='factory_complex',days=70)
    f(g,'solel_boneh','Solel Boneh Builds a Working Town',0,2,'Use the labour construction network to connect housing with employment. The cabinet pays for the project and accepts the political influence of the contractor that carries it.',pre=[['wage_bonds','cash_wages']],cost=1.8,effects=asset('Negev','Civilian Factory')+asset('Negev','Infrastructure'),sources=['histadrut'],icon='focus_public_housing',days=49)
    f(g,'sapir_book','Sapir\'s Development Notebook',3,2,'Development policy can identify a promising workshop before it becomes a safe banking proposition. The finance ministry backs selected tenders instead of offering an unlimited subsidy.',pre=['cash_wages'],effects=[unlock('Sapir Development Tender: Two Projects'),E('Development Tender State Contribution','50%, capped at 1.5% of annual GDP','cost')],sources=['economy'],icon='industrial_subsidies',mechanics=['Two projects total: each offers one actual civilian factory with one shared slot in an owned controlled core state. Total normal cost is 1.5% GDP per project; half is paid by treasury, half by a genuine accepted private investment. No project is delivered without the other half.'])
    f(g,'clalit','Pool the Kupat Holim Purchasing Budget',-2,3,'The health network can purchase medicines and supplies together without withdrawing clinics from small communities. Modernise its purchasing office rather than reducing service through an accounting trick.',pre=['koor','solel_boneh'],cost=.8,mods={'health_cost_multiplier_modifier':-.08},sources=['histadrut'],icon='generic_healthcare')
    f(g,'industrial_compact','A Compact for Industrial Exports',2,3,'Government, employers and unions commit to an export programme with a predictable order book. Additional social contributions are part of the bargain rather than an invisible cost.',pre=['solel_boneh','sapir_book'],mods={'production_factory_efficiency_gain_factor':.10,'social_cost_multiplier_modifier':.06},effects=[research('Industry')],sources=['labour'],icon='export_factories',days=49)
    f(g,'histadrut_balance','A Histadrut Strong Enough to Bargain',0,4,'Institutional strength is valuable when it produces a bargain rather than a permanent emergency. Keep the national assets and a negotiated labour settlement without granting every enterprise a monopoly.',pre=[['clalit','industrial_compact']],mods={'civilian_factories_productivity':.06},effects=[unlock('Renew the Wage Settlement')],sources=['histadrut','labour'],icon='generic_democratic_socialism',mechanics=['The wage settlement can be renewed only after its term, with its new cost. No repeated factories or bond cash.'])

    g=group('gahal','Gahal: Ownership and National Resolve','Liberal ownership, Herut\'s social appeal and competing spending priorities.',1,16,1,'Gahal is in Power.')
    f(g,'property_register','Put Public Assets on the Register',0,0,'The liberal wing wants a government that can explain what it owns and why. An asset register begins a programme of disposal and competition without pretending that every sale creates new national wealth.',cost=.3,effects=[unlock('Auction a Public Commercial Enterprise')],icon='focuselectherut',mechanics=['One proposed auction: treasury +3% GDP once; permanent public-enterprise dividend loss of 0.01% GDP per week. Sold asset cannot be auctioned again by a new cabinet.'])
    f(g,'competitive_credit','Credit outside the Conglomerates',-2,1,'Guarantees and competitive bank access give smaller firms a route past public and labour monopolies. The cabinet will meet resistance from the institutions whose privileged access it is ending.',pre=['property_register'],cost=.7,mods={'receiving_investment_cost_modifier':-.15,'offices_productivity':.08},effects=[opinion('Labor Unions',-15)],icon='generic_privatization')
    f(g,'herut_charter','Herut\'s Social Appeal',2,1,'Begin\'s national programme must speak to households outside the governing establishment. A defined development-town allowance makes this a social commitment as well as a change of ownership.',pre=['property_register'],mods={'stability_factor':.05,'social_cost_multiplier_modifier':.06},effects=[opinion('Small and Medium Business Owners',10)],icon='generic_working_class_family')
    f(g,'private_workshops','A Tender the Small Firm Can Win',-3,2,'Divide public orders into contracts that smaller manufacturers can actually fulfil. The state gets a wider supplier base instead of another protected national champion.',pre=['competitive_credit'],cost=1.6,effects=asset('Tel Aviv','Civilian Factory')+[research('Industry')],icon='generic_improve_industry',days=49)
    f(g,'household_savings','Make Household Savings Investable',0,2,'Commercial savings should be available to firms that can repay them. Improve investment access while accepting greater exposure to overseas financial conditions.',pre=['competitive_credit','herut_charter'],cost=.4,mods={'offices_productivity':.08,'mdcw_cw_market_exposure':.10},icon='generic_financial_markets')
    f(g,'herut_clinics','An Independent Community Health Network',3,2,'A labour movement should not be the only route to a dependable clinic. Fund the expansion of alternative community provision, accepting the cost of a less concentrated system.',pre=['herut_charter'],cost=.8,effects=[E('Stability','+4%','gain')],mods={'health_cost_multiplier_modifier':.05},icon='generic_healthcare',status='Alternate policy')
    f(g,'supplier_competition','Let Suppliers Compete for Defence Orders',-2,3,'The defence budget can support competing workshops without guaranteeing every producer an order. Competition broadens production at the expense of the old networks.',pre=['private_workshops'],cost=.8,mods={'production_factory_efficiency_gain_factor':.08},effects=[research('Military Electronics'),opinion('Industrial Conglomerates',-10)],icon='generic_support_equipment')
    f(g,'national_bargain','National Resolve without a Blank Cheque',2,3,'A government can defend its territorial position while deciding separately what it can afford to build. Submit the next settlement appropriation to an explicit budget vote.',pre=['herut_clinics','household_savings'],effects=[unlock('Gahal Settlement Appropriation: 1% of GDP'),unlock('Gahal Civilian Housing Appropriation: 1% of GDP')],icon='isr_independence',mechanics=['The cabinet chooses one appropriation: settlement funding reduces the next two controlled settlement project costs by 0.5% GDP each; civilian funding reduces the next two domestic housing/training project costs by 0.5% GDP each. Treasury pays 1% GDP at selection. No free programme and no mandatory settlement policy.'])

    g=group('mafdal','Mafdal: Faith, Service and Land','Religious Zionist institutions with separate service and settlement choices.',2,16,0,'Mafdal is in Power.')
    f(g,'mafdal_budget','A Religious-Zionist Budget Agreement',0,0,'Mafdal brings religious education, local institutions and a national-service tradition to government. Its coalition bargain must say which institutions the state is undertaking to fund.',mods={'political_power_factor':.06,'education_cost_multiplier_modifier':.06},effects=[opinion('Religious Institutions',15)],icon='focuselecthapoelhamizrachi')
    f(g,'hesder','Fund the Hesder Training Establishment',-2,1,'A religious study and service framework needs instructors, transport and training places. Fund those practical arrangements without treating religious schooling as an automatic scientific or combat advantage.',pre=['mafdal_budget'],cost=.6,effects=[E('Army Experience','+30','gain'),research('Infantry Weapons')],mods={'personnel_cost_multiplier_modifier':.04},icon='generic_army_training')
    f(g,'mizrahi_coops','Hapoel HaMizrahi Cooperative Credit',2,1,'Religious workers\' cooperatives need equipment and dependable credit alongside their communal institutions. A paid farm-and-workshop programme gives those communities an economic base.',pre=['mafdal_budget'],cost=1.4,effects=asset('Negev','Agricultural District')+asset('Negev','Civilian Factory'),icon='agricultural_banks',days=49)
    f(g,'religious_towns','A School and a Workshop in the Same Town',-2,2,'A development town should not have to choose between community life and an economic future. Fund the technical workshop alongside the local religious school.',pre=['hesder'],cost=.8,effects=[research('Industry')],mods={'industry_repair_factor':.10,'education_cost_multiplier_modifier':.03},icon='school_is_in')
    f(g,'mafdal_survey','The Settlement Department\'s Survey',2,2,'The movement can direct its political energy toward domestic agricultural communities or toward contested territory. A ministry survey must identify the route and the appropriation rather than merging them into a single slogan.',pre=['mizrahi_coops'],effects=[unlock('Choose the Religious-Zionist Land Appropriation')],icon='jewish_sites_isr',mechanics=['Choose once: domestic cooperative grant costs 1% GDP and adds one agricultural district plus one shared slot in the Negev. Contested-territory grant costs 1% GDP and gives the next controlled settlement site +10% local agricultural productivity, with +5% local garrison requirement. No host veto is created for foreign footholds.'])
    f(g,'service_bargain','A Service Bargain with the Cabinet',0,3,'Religious institutions and the army need a service arrangement they can budget and plan against. The cabinet protects the agreed study allocation while carrying a larger permanent training establishment.',pre=['religious_towns','mafdal_survey'],mods={'training_time_army_factor':-.08,'personnel_cost_multiplier_modifier':.04},effects=[opinion('Religious Institutions',10)],icon='generic_union_agreement')

    g=group('orthodox','Agudat Israel and Poalei Agudat','Communal autonomy and a distinct religious workers\' continuation.',3,16,13,'Agudat Israel and Poalei Agudat is in Power.')
    f(g,'communal_budget','A Communal Budget in Black and White',0,0,'Orthodox parties negotiate defined support for their communities rather than a general programme of military expansion. A written budget makes their bargain visible to the rest of the cabinet.',mods={'stability_factor':.05,'education_cost_multiplier_modifier':.08},effects=[opinion('Religious Institutions',20)],icon='orthodox_jew')
    f(g,'study_guarantees','Protect the Independent School Budget',-2,1,'Keep communal educational provision outside changing ministerial priorities. The state assumes an enduring obligation while the communities retain authority over their own institutions.',pre=['communal_budget'],effects=[opinion('Religious Institutions',15),E('Political Power','+50','gain')],mods={'education_cost_multiplier_modifier':.06},icon='school_is_in',programme='Governing programme: protected educational allocation')
    f(g,'poalei_workshops','Poalei Agudat\'s Working Communities',2,1,'Religious workers\' communities need productive employment as well as a protected school. A cooperative workshop gives this programme a different economic direction from communal budget protection alone.',pre=['communal_budget'],cost=1.6,effects=asset('Negev','Civilian Factory'),icon='generic_working_class_family',days=49)
    f(g,'communal_welfare','A Communal Relief Network',-2,2,'Relief organisations can coordinate the help they already provide without making the whole health service dependent on them. The cabinet underwrites the supplies and local facilities.',pre=['study_guarantees'],cost=.5,mods={'social_cost_multiplier_modifier':-.05},effects=[budget('Communal Relief Grant',-.01)],icon='generic_healthcare')
    f(g,'religious_agriculture','Tools for the Religious Farm Cooperatives',2,2,'Practical farming institutions can purchase machinery and market their produce together. The state pays for the district; the cooperative carries the working programme.',pre=['poalei_workshops'],cost=.9,effects=asset('Negev','Agricultural District')+[research('Agriculture')],icon='generic_agriculture')

    g=group('liberals','Independent Liberals: Small Firms, Open Doors','Commercial law, tourism and two approaches to foreign-currency risk.',0,23,2,'Independent Liberals is in Power.')
    f(g,'commercial_courts','Commercial Courts for Small Firms',0,0,'A small firm cannot spend years pursuing an unpaid contract. Accessible commercial arbitration makes credit and public tenders less dependent on the largest business networks.',cost=.5,mods={'bureaucracy_cost_multiplier_modifier':-.06,'receiving_investment_cost_modifier':-.08},icon='generic_banking_legislation')
    f(g,'tourism','A Tourism Ministry with an Order Book',-2,1,'Tourism needs transport, trained staff and commercial facilities rather than only overseas publicity. A civilian visitor economy brings income and a particular exposure to regional uncertainty.',pre=['commercial_courts'],cost=1.2,effects=asset('Jerusalem','Office District')+asset('Haifa','Office District'),mods={'mdcw_cw_market_exposure':.08},icon='generic_airline_industry',days=49)
    f(g,'workshop_guarantees','Guarantees for the Independent Workshop',2,1,'Reserve a limited credit guarantee book for smaller suppliers. Public backing broadens access to capital while the treasury carries a defined provision against losses.',pre=['commercial_courts'],mods={'offices_productivity':.08},effects=[budget('Small-Firm Guarantee Provision',-.015,52),unlock('Independent Workshop Credit Guarantee')],icon='agricultural_banks')
    f(g,'open_fx','Liberalise Commercial Currency Access',-2,2,'Make overseas payments and commercial finance easier for productive firms. An economy more open to capital also becomes more exposed to its withdrawal.',pre=['tourism'],mods={'receiving_investment_cost_modifier':-.12,'mdcw_cw_market_exposure':.15},icon='generic_financial_markets',status='Alternate policy',programme='Commercial currency policy')
    f(g,'selective_fx','Reserve Foreign Currency for Export Inputs',2,2,'Keep controls but make access predictable for essential machinery and export inputs. The treasury retains a cushion at the price of a larger licensing establishment.',pre=['workshop_guarantees'],mods={'imp_sanction_resistance':.12,'bureaucracy_cost_multiplier_modifier':.04},effects=[research('Industry')],icon='economic_protectionism',programme='Commercial currency policy')
    exclusive('open_fx','selective_fx')
    f(g,'export_services','A Commercial Service for Smaller Exporters',0,3,'Pooling legal, shipping and marketing services can let a workshop sell abroad without becoming a conglomerate first. Keep the service open to firms beyond the governing party\'s own network.',pre=[['open_fx','selective_fx']],cost=.6,mods={'offices_productivity':.06},effects=[unlock('Small-Exporter Commercial Mission')],icon='export_factories')

    g=group('haolam','HaOlam HaZeh - Koah Hadash','A secular parliamentary challenge: scrutiny, civil registration and municipal rights.',1,23,16,'HaOlam HaZeh - Koah Hadash is in Power.')
    f(g,'press_scrutiny','Publish the Emergency Appropriations',0,0,'A parliament cannot scrutinise a budget it never sees. Publish the civilian and aggregate security appropriations while protecting operational details that can actually endanger lives.',cost=.3,effects=[E('Corruption','-1 level','gain'),opinion('The Military',-10)],icon='generic_secret_documents')
    f(g,'civil_register','A Civil Register beside the Rabbinate',-2,1,'Provide a secular route through civil registration rather than making every household depend on religious jurisdiction. The proposal will face organised resistance from religious institutions.',pre=['press_scrutiny'],cost=.7,mods={'bureaucracy_cost_multiplier_modifier':-.05},effects=[E('Stability','+4%','gain'),opinion('Religious Institutions',-20)],icon='adopt_new_constitiution',status='Alternate policy')
    f(g,'arab_municipalities','A Budget for Arab Municipal Services',2,1,'Arab citizens should be able to pursue municipal works through public institutions rather than intermediaries. Fund a road and commercial connection in a controlled Israeli core state.',pre=['press_scrutiny'],cost=1.2,effects=asset('Selected Israeli Core State','Infrastructure')+asset('Selected Israeli Core State','Office District'),requirements=['An owned controlled Israeli core state with the appropriate local project and capacity.'],icon='gaza_civic_organizations',mechanics=['Uses a domestic municipal project, not a settlement project in Palestinian occupied territory. No ownership transfer or population change.'])
    f(g,'parliamentary_watch','A Standing Parliamentary Watchdog',0,2,'Make scrutiny a standing parliamentary responsibility instead of an occasional scandal. Ministers retain authority, but investigations and covert appropriations must answer to a committee.',pre=['civil_register','arab_municipalities'],mods={'corruption_cost_factor':-.12,'political_power_factor':-.04},effects=[unlock('Review a Covert-Action Appropriation')],icon='generic_civilian_oversight')
    f(g,'civil_equalities','Rights in the Civil Service',0,3,'Publish common recruitment and promotion rules for the civilian state. Removing barriers makes better use of existing skills without inventing a new population or treating a newspaper as an army reform.',pre=['parliamentary_watch'],cost=.5,mods={'offices_productivity':.06},effects=[E('Corruption','-1 level','gain')],icon='civil_service',status='Alternate policy')

    g=group('rakah','Rakah: A Jewish-Arab Communist Cabinet','A genuine alternative government with a real foreign-policy choice.',2,23,4,'Rakah is in Power.')
    f(g,'rakah_civic','Toubi\'s Civic Equality Programme',0,0,'A Rakah cabinet would have to turn its Jewish-Arab programme into public employment and municipal services. Its electoral victory would not by itself settle Israel\'s borders or choose a foreign patron.',cost=.7,effects=[unlock('Public Employment and Municipal Works Programme')],mods={'production_speed_infrastructure_factor':.12},icon='generic_workers_rights',status='Alternate policy')
    f(g,'public_ownership','Public Ownership with Compensation',-2,1,'Acquire strategic workshops through an explicit compensation budget. Public planning gains assets while private investors face a state-led economy.',pre=['rakah_civic'],cost=2,mods={'civilian_factories_productivity':.10,'receiving_investment_cost_modifier':.12},effects=[opinion('Industrial Conglomerates',-25)],icon='centrally_planned_economy',status='Alternate policy')
    f(g,'joint_committees','Joint Workplace Committees',2,1,'Put Jewish and Arab workers into the same bargaining institutions. A common wage and training programme can improve production while increasing the social commitments of public employers.',pre=['rakah_civic'],cost=.6,mods={'production_factory_efficiency_gain_factor':.08,'social_cost_multiplier_modifier':.05},effects=[opinion('Labor Unions',15)],icon='generic_workers_democracy',status='Alternate policy')
    f(g,'eastern_credit','Negotiate an Eastern Development Loan',-2,2,'A communist cabinet may seek credit from Moscow, but an RP Soviet government must decide whether to lend. Borrowing is a financial contract rather than a compulsory faction choice.',pre=['public_ownership'],effects=[unlock('Offer a Soviet Development Loan')],icon='focusimportsoviettanks',status='Alternate policy',mechanics=['If accepted: Soviet Union transfers 4% of Israeli annual GDP to Israel. Israel receives that treasury amount and records equal debt; Soviet Union pays the identical amount and records the claim. Israel repays the principal over 104 weeks plus 4% annual simple interest, and the Soviet Union receives the identical payments. Both receive +15 bilateral opinion. This requires a new bilateral loan ledger integrated with MD debt, not duplicate anonymous interest. No automatic Soviet ally or territorial settlement.'])
    f(g,'uncommitted_left','An Uncommitted Parliamentary Left',2,2,'Keep the programme answerable to parliament and finance it domestically. The cabinet forgoes the overseas loan and bears the cost of its own industrial education programme.',pre=['joint_committees'],cost=1,effects=[research('Industry',2),research('Agriculture')],mods={'education_cost_multiplier_modifier':.05},icon='democratic_socialism',status='Alternate policy')
    exclusive('eastern_credit','uncommitted_left')
    f(g,'rakah_talks','A Mandate to Offer Territorial Talks',0,3,'The government can seek a negotiated settlement while retaining responsibility for the costs of occupation until an agreement is executed. The other governments decide whether its offer is acceptable.',pre=[['eastern_credit','uncommitted_left']],effects=[unlock('Rakah Territorial Negotiating Mandate'),unlock('Fund Palestinian Service Compensation')],icon='one_state_isr_pal',status='Alternate policy',mechanics=['No automatic withdrawal, federation, Palestinian consent to settlements or forced peace. Exact accepted agreement terms determine actual transfers.'])

    g=group('state_list','State List: the Administrative Republic','Rafi\'s dissident continuation: professional management over a party economy.',3,23,14,'State List is in Power.')
    f(g,'state_tenders','Tender Boards above Party Appointments',0,0,'A State List cabinet can challenge the way party institutions control appointments and public contracts. Give professional boards authority over a defined development budget.',cost=.5,mods={'bureaucracy_cost_multiplier_modifier':-.08},effects=[E('Corruption','-1 level','gain')],icon='generic_tackle_corruption')
    f(g,'state_enterprises','Professional Managers for State Enterprises',-2,1,'Public ownership need not mean that every management appointment is a coalition appointment. A paid reorganisation protects the state\'s share while improving the use of its existing plants.',pre=['state_tenders'],cost=1,mods={'civilian_factories_productivity':.10},effects=[opinion('Labor Unions',-10)],icon='civil_service')
    f(g,'procurement_board','A Procurement Board with a Ceiling',2,1,'Compare domestic manufacture and foreign purchases before committing the defence budget. The board will fund one major technical study rather than promise every procurement plan at once.',pre=['state_tenders'],cost=.7,effects=[research('Armor',1,75),research('Aircraft',1,75)],icon='generic_investigate_corruption')
    f(g,'technical_state','The Technical State',0,2,'Link the civil service, technical colleges and public enterprises through practical standards and competitive recruitment. The professional establishment is an enduring expense, not a free cure for politics.',pre=['state_enterprises','procurement_board'],cost=.6,mods={'productivity_growth_modifier':.06,'education_cost_multiplier_modifier':.04},effects=[research('Industry')],icon='the_research_department',days=49)

    g=group('mapam','Mapam: the Cooperative Left','Inside the Alignment at the start; independent leadership is an alternate political outcome.',0,30,18,'Mapam is in Power.')
    f(g,'mapam_coops','Hashomer Hatzair\'s Industrial Cooperatives',0,0,'A Mapam-led cabinet would give cooperative production a different role from appointment through a public conglomerate. Start with a paid workshop and a practical agricultural order book.',cost=1.6,effects=asset('Negev','Civilian Factory')+[research('Agriculture')],icon='focuselectmapam',status='Alternate policy',history_note='Mapam starts in the Alignment. This programme requires a genuine independent governing outcome, not a second simultaneous government bonus.')
    f(g,'councils','Workplace Councils over Political Appointments',-2,1,'Workers\' councils receive authority over the organisation of production. Public employers must bargain over the resulting social commitments rather than pocketing every productivity gain.',pre=['mapam_coops'],mods={'productivity_growth_modifier':.06,'social_cost_multiplier_modifier':.05},effects=[opinion('Labor Unions',15)],icon='generic_workers_democracy',status='Alternate policy')
    f(g,'cooperative_farming','A Cooperative Machinery Pool',2,1,'Shared machinery and marketing let farming communities use expensive equipment without purchasing it separately. The treasury pays for the district and training programme.',pre=['mapam_coops'],cost=1.2,effects=asset('Negev','Agricultural District')+[research('Agriculture')],icon='agricultural_mechanization')
    f(g,'common_workplaces','A Common Jewish-Arab Wage Table',0,2,'Use public contracts to establish equal terms in the same workplace. A common wage table broadens the social programme while increasing the cost of public employment.',pre=['councils','cooperative_farming'],mods={'industrial_capacity_factory':.06,'social_cost_multiplier_modifier':.06},effects=[E('Stability','+4%','gain')],icon='generic_workers_rights',status='Alternate policy')
    f(g,'independent_coops','Cooperatives without a Foreign Party Line',0,3,'The cooperative programme will be financed and defended in Israel\'s own parliament. Diplomatic negotiations remain choices of the cabinet and the governments it approaches.',pre=['common_workplaces'],cost=.7,effects=[research('Industry',2),unlock('Cooperative Export Contract')],icon='generic_market_socialism',status='Alternate policy')

    g=group('maki','Maki: Independent Communism','A shorter parliamentary continuation, separate from Rakah\'s Soviet option.',1,30,19,'Maki is in Power.')
    f(g,'maki_parliament','Sneh\'s Parliamentary Communism',0,0,'Maki\'s continuation is not a duplicate of Rakah. A parliamentary communist government must defend its labour programme while maintaining its own national and international position.',cost=.6,effects=[opinion('Labor Unions',20),research('Industry')],icon='democratic_socialism',status='Alternate policy')
    f(g,'maki_public','Public Workshops and Civilian Contracts',-2,1,'Direct the public development budget to civilian production. The programme buys a real workshop instead of treating public ownership itself as another source of cash.',pre=['maki_parliament'],cost=1.7,effects=asset('Haifa','Civilian Factory'),icon='factory_complex',status='Alternate policy',days=49)
    f(g,'maki_laboratories','Laboratories with a Civilian Remit',2,1,'Reserve a scientific appropriation for industrial and agricultural work. The research gains have their own public budget and do not imply an eastern alliance.',pre=['maki_parliament'],cost=.8,effects=[research('Industry'),research('Agriculture')],mods={'education_cost_multiplier_modifier':.04},icon='universities',status='Alternate policy')
    f(g,'maki_budget','A Civilian Budget before New Commitments',0,2,'Put a ceiling on new military construction while the civilian programme is funded. The government gains room for productive development by postponing another arms-factory expansion.',pre=['maki_public','maki_laboratories'],mods={'civilian_factories_productivity':.08,'production_speed_arms_factory_factor':-.08},icon='generic_civilian_oversight',status='Alternate policy')

    g=group('free_center','Free Center: a Different National Opposition','A compact alternative to Gahal, not another generic nationalist tree.',2,30,20,'Free Center is in Power.')
    f(g,'center_reform','A National Opposition against Patronage',0,0,'The Free Center can challenge the governing establishment without accepting every institution of Gahal. Its first task is a public appointments and procurement reform.',cost=.4,effects=[E('Corruption','-1 level','gain')],mods={'political_power_factor':.08},icon='generic_parliament2',status='Alternate policy')
    f(g,'center_reserves','Readiness by Contract and Inspection',-2,1,'The government funds equipment inspections and reserve depots before announcing more formations. Readiness improves because the stores exist and the staff are paid.',pre=['center_reform'],cost=.8,mods={'mobilization_speed':.15},effects=[E('Army Experience','+35','gain'),budget('Reserve Inspection Establishment',-.01)],icon='ast_upgrade_reserves',status='Alternate policy')
    f(g,'center_enterprise','An Independent Supplier Base',2,1,'Break public orders into contracts that suppliers outside the established party economy can fulfil. The government pays for a new workshop and a technical training allocation.',pre=['center_reform'],cost=1.6,effects=asset('Haifa','Civilian Factory')+[research('Military Electronics')],icon='generic_improve_industry',status='Alternate policy',days=49)
    f(g,'center_cabinet','A Parliamentary National Cabinet',0,2,'Bring the national programme back through a working parliamentary majority. An enduring majority is an achievement of coalition bargaining, not an automatic presidential constitution.',pre=['center_reserves','center_enterprise'],mods={'stability_factor':.05},effects=[unlock('Negotiate a Parliamentary Coalition Compact')],icon='knesset_speech',status='Alternate policy')


def finish():
    national_programmes()
    political_programmes()
    by_id={n['id']:n for n in NODES}
    assert len(by_id)==len(NODES)
    for node in NODES:
        assert node['effects'],node['id']
        assert not any(mark in node['label']+node['description'] for mark in ('\u2013','\u2014'))
        for row in node['pre']:
            assert row and all(key in by_id for key in row),(node['id'],row)
        for other in node['exclusive']:
            assert node['id'] in by_id[other]['exclusive']
    workforce=[(n['id'],n['modifiers'].get('total_workforce_modifier',0)) for n in NODES if 'total_workforce_modifier' in n['modifiers']]
    assert len(workforce)==3 and abs(sum(value for _,value in workforce)-.15)<1e-9
    old=json.loads((ROOT/'tools/israel_1970/english_design.json').read_text(encoding='utf-8'))
    keys=set(n['icon'] for n in NODES)
    fallback={
        'GFX_ISR70_focus_generic_collaborate_local_elites':'GFX_ISR70_focus_collaborate_local_elites',
        'GFX_ISR70_focus_generic_air_army_cooperation':'GFX_ISR70_focus_generic_army_cooperation',
        'GFX_ISR70_focus_generic_democratic_socialism':'GFX_ISR70_focus_democratic_socialism',
    }
    for n in NODES:
        n['icon']=fallback.get(n['icon'],n['icon'])
    icons={key:old['layout']['icons'][key] for key in set(n['icon'] for n in NODES)}
    starting=[
        dict(label='A Citizen Army in a Working Economy',description='Reserve readiness and civilian production draw on the same trained people. Call-ups are temporary, paid national choices.',effects=[E('Army Training Time','-10%','gain'),E('Personnel Cost','+8%','cost')]),
        dict(label='The Histadrut Establishment',description='An unusual network of unions, enterprises, builders and health services. Reform, compete with it, or bargain through it.',effects=[E('Civilian Factory Construction Speed','+8%','gain'),E('Healthcare Cost','-5%','gain'),E('Incoming Investment Cost','+8%','cost')]),
        dict(label='Absorption without Enough Connections',description='Professional recognition, access to work and local services lag behind the needs of arriving households. No workforce-size penalty is imposed.',effects=[E('Research Speed','-5%','cost'),E('Social Spending Cost','+8%','cost')]),
        dict(label='An Import-Dependent Development Economy',description='Capital inflows and specialist exports sustain a high-investment economy. An external shock can still interrupt its essential imports.',effects=[E('World-Market Exposure','+10%','cost'),E('Incoming Investment Cost','-5%','gain')]),
        dict(label='West Bank: Military Administration',description='Controlled non-core territory, with a permanent budget and resistance burden.',effects=[E('Initial Resistance / Compliance','18% / 25%'),E('Resistance Target','+15 percentage points','cost'),E('Local Garrison Requirement','+40%','cost'),E('Damage to Garrisons','+20%','cost'),E('Local Factory Access','-15 percentage points','cost'),E('Israeli Police / Bureaucracy / Personnel Cost','+5% / +3% / +2%','cost')]),
        dict(label='Gaza: Military Administration',description='Dense communities and contested control create a different burden from the desert frontier.',effects=[E('Initial Resistance / Compliance','25% / 15%'),E('Resistance Target','+25 percentage points','cost'),E('Local Garrison Requirement','+60%','cost'),E('Damage to Garrisons','+35%','cost'),E('Local Factory Access','-20 percentage points','cost'),E('Israeli Police / Bureaucracy / Personnel Cost','+8% / +4% / +3%','cost')]),
        dict(label='Sinai: the Desert Commitment',description='Supply distances and dispersed positions dominate the military administration bill.',effects=[E('Initial Resistance / Compliance','8% / 30%'),E('Resistance Target','+5 percentage points','cost'),E('Local Garrison Requirement','+20%','cost'),E('Local Supplies','-12%','cost'),E('Israeli Police / Bureaucracy / Personnel Cost','+2% / +3% / +8%','cost')]),
        dict(label='Golan: a Contested Upland Frontier',description='Defended positions and regional administration remain an expense even between wars.',effects=[E('Initial Resistance / Compliance','10% / 20%'),E('Resistance Target','+8 percentage points','cost'),E('Local Garrison Requirement','+25%','cost'),E('Local Supplies','-5%','cost'),E('Israeli Police / Bureaucracy / Personnel Cost','+2% / +2% / +5%','cost')]),
    ]
    data=dict(project='IMPERIA COLD WAR',title='Israel 1970: Institutions under Pressure',revision='2.0-concept-20261028',
        status='Design proposal. Not installed. Numerical balance proposals, not historical measurements.',
        groups=GROUPS,nodes=NODES,sources=SOURCES,starting=starting,
        layout=dict(x_unit=82,y_unit=178,icons=icons),
        workforce_cap=dict(total=.15,focuses=workforce),
        provenance=dict(authorship='IMPERIA COLD WAR design with Codex; existing Millennium Dawn/Imperia focus icons reused for review only.',
            art_source='Current tools/israel_1970/english_design.json embedded icon register; original individual artists/licences unknown where not identified in inherited notices.',
            art_modifications='No raster art modification. Existing icons embedded unchanged.',
            installed_source='common/national_focus/ISR70_focus.txt',installed_sha256=hashlib.sha256((ROOT/'common/national_focus/ISR70_focus.txt').read_bytes()).hexdigest()))
    # Complete bilateral terms are displayed alongside the offer, before consent.
    for node in NODES:
        if node['id'] in {'ISR2_irrigation_exports','ISR2_arms_exports','ISR2_mashav','ISR2_washington','ISR2_european_orders','ISR2_liaison_limits','ISR2_eastern_credit','ISR2_negotiated_terms'}:
            node['agreement_preview']=node['mechanics'][:]
    # Historical Arab parliamentary lists are represented through coalition and
    # municipal institutions, rather than an invented Islamic governing slot.
    f('institutions','municipal_lists','Progress and Development at the Budget Table',-3,5,
      'Progress and Development can bargain for municipal works through the coalition. The appropriation creates an actual commercial facility and a service connection in a domestic core state.',
      pre=['municipal_tenders'],cost=1.2,
      effects=asset('Selected Israeli Core State','Office District')+asset('Selected Israeli Core State','Infrastructure'),
      requirements=['Progress and Development is represented in the governing coalition.','An eligible owned and controlled Israeli core state.'],
      icon='gaza_civic_organizations',sources=['election'],status='Alternate policy',
      mechanics=['Requires a real list/coalition identity in the political data. No invented ruling-party slot is assumed, and this is not a Palestinian occupation project.'])
    f('institutions','brotherhood_compact','Cooperation and Brotherhood: Local Contracts',3,5,
      'The second real Arab parliamentary list has its own local constituency. Publish a paid municipal works contract instead of folding its representation into a fictional religious movement.',
      pre=['municipal_tenders'],cost=.8,
      effects=asset('Selected Israeli Core State','Civilian Factory'),
      requirements=['Cooperation and Brotherhood is represented in the governing coalition.','An eligible owned and controlled Israeli core state.'],
      icon='generic_working_class_family',sources=['election'],status='Alternate policy',
      mechanics=['The political identity must be integrated before implementation. This design does not silently reassign an occupied Palestinian state.'])
    # Consequences already in force are inspectable starting conditions, never
    # a player-paid focus whose only reward is an informational explanation.
    NODES[:]=[node for node in NODES if node['id']!='ISR2_palestinian_accounts']
    by_id={node['id']:node for node in NODES}
    arsenal=next(g for g in GROUPS if g['id']=='arsenal')['origin']
    for key,x,y in [('technion_computing',3,2),('civil_spillover',2,3),('defence_priority',-2,3)]:
        by_id['ISR2_'+key]['xy']=[arsenal[0]+x,arsenal[1]+y]
    by_id['ISR2_civil_spillover']['pre']=[['ISR2_technion_computing'],['ISR2_elta']]
    by_id['ISR2_technion_computing']['pre']=[['ISR2_arava']]
    by_id['ISR2_bonds_plant']['pre']=[['ISR2_bond_drive']]
    for node_id in ['ISR2_after_action','ISR2_hesder']:
        rows=by_id[node_id]['effects']
        rows[:]=[row for row in rows if not(row['label']=='Research Bonus' and ('Land Doctrine' in row['value'] or 'Infantry Weapons' in row['value']))]
        rows.append(E('Doctrine Cost Reduction','1 x 50%: Land Doctrine','gain'))
    by_id['ISR2_national_bargain']['description']='A government can defend its territorial position while deciding separately what it can afford to build. A matched public appropriation supports one clearly stated programme rather than giving the next commitment a blank cheque.'
    by_id['ISR2_national_bargain']['effects']=[unlock('Matched Gahal Settlement Appropriation'),unlock('Matched Gahal Civilian Housing Appropriation')]
    by_id['ISR2_national_bargain']['mechanics']=['Choose one programme and pay 0.5% GDP. Its matched public/private development commitment gives a total 1% GDP contribution to the next two eligible projects, 0.5% each. The treasury records its 0.5% payment and the matched 0.5% must come from a real accepted investment, not a second treasury charge. Settlement and domestic housing/training remain separate choices. No mandatory territorial policy.']
    by_id['ISR2_national_bargain']['effects'] += [
        E('Treasury on Programme Selection','-0.5% of annual GDP','cost'),
        E('Accepted Private Matched Investment','+0.5% of annual GDP','gain'),
        E('Contribution to the Next Two Eligible Projects','0.5% of annual GDP each','gain')]
    by_id['ISR2_controlled_sites']['mechanics']=['For each selected controlled area: treasury -1.5% of Israeli GDP, +3 state shared slots, +1 agricultural district, +1 infrastructure and +1 land fort. Israeli police cost +3%, personnel cost +2%; state garrison requirement +10%. Three paid development tiers at most. Actual agricultural income comes from the real agricultural district, not an unsupported state-scoped country-productivity modifier. Control, ownership and native province capacity are checked separately.']
    by_id['ISR2_mafdal_survey']['mechanics']=['Choose once: domestic cooperative grant costs 1% GDP and adds one agricultural district plus one shared slot in the Negev. Contested-territory grant costs 1% GDP and adds one additional agricultural district plus one shared slot to the next paid controlled settlement site, with +5% local garrison requirement. No host veto is created for foreign footholds.']
    f('arsenal','armour_repair','Turn the Tank Repair Hall into a Design Office',-5,0,
      'Tank rebuilding has already created a pool of mechanics, tools and practical knowledge. A dedicated design office gives that establishment a route toward a domestic vehicle programme.',
      cost=.8,effects=[research('Armor'),E('Army Experience','+20','gain')],sources=['merkava'],icon='generic_army_tanks2',days=49)
    f('arsenal','atomic_commission','The Atomic Energy Commission\'s Appropriation',5,0,
      'The commission and its research centres predate the present cabinet. Give its civilian scientific work a defined appropriation while keeping any strategic programme subject to the actual nuclear-development system.',
      cost=.9,effects=[research('Nuclear Reactors'),unlock('Civil Nuclear Research Appropriation')],sources=['iaec'],icon='nuclear_research_lab',days=49,
      mechanics=['Uses existing nuclear projects, uranium development and recurring-budget readers. No uranium production, free mines or finished weapons are granted.'])
    by_id={node['id']:node for node in NODES}
    by_id['ISR2_tal_tank']['pre']=[['ISR2_armour_repair']]
    by_id['ISR2_ambiguity']['pre']=[['ISR2_atomic_commission']]
    by_id['ISR2_ambiguity']['xy']=[arsenal[0]+5,arsenal[1]+2]
    by_id['ISR2_ambiguity']['history']['sources']=['nuclear_policy']
    SOURCES.extend([
        dict(id='iaec',title='Prime Minister\'s Office: Israel Atomic Energy Commission',url='https://www.gov.il/he/departments/units/atomic_energy_committee',note='Commission established in June 1952; Soreq and Negev research centres predate 1970.'),
        dict(id='nuclear_policy',title='US FRUS: Israeli Nuclear Program, 19 July 1969',url='https://history.state.gov/historicaldocuments/frus1969-76v23/d38',note='Contemporaneous policy debate on possession, public acknowledgement, procurement and ambiguity. It is not a claim that a focus creates a warhead.'),
    ])
    by_id['ISR2_settled_skills']['effects'] += [
        E('Removes National Spirit','Absorption without Enough Connections','gain'),
        E('Research Speed','+5%','gain'),E('Social Spending Cost','-8%','gain')]
    by_id['ISR2_controlled_sites']['mechanics'].append('Palestine, if it exists with the affected West Bank or Gaza core: each delivered tier adds office productivity -4%, bureaucracy cost +4% and stability -2%, capped at two tiers per area. These costs apply automatically; no separate focus or Palestinian approval is required.')
    by_id['ISR2_foreign_footholds']['mechanics'].append('Palestine, if it exists with the affected West Bank or Gaza core: one pressure tier per funded foothold, giving office productivity -4%, bureaucracy cost +4% and stability -2%. Two affected areas are bounded separately. No host consent or Palestinian decision is involved.')
    by_id['ISR2_controlled_sites']['effects'] += [
        dict(row,heading='Per Funded Controlled Development Tier: Israel') for row in [cash(-1.5),E('Police Cost','+3%','cost'),E('Personnel Cost','+2%','cost')]]
    by_id['ISR2_controlled_sites']['effects'] += [
        dict(row,heading='Per Funded Controlled Development Tier: Selected State') for row in [
            E('Shared Building Slots','+3','gain'),E('Agricultural District','+1','gain'),E('Infrastructure','+1','gain'),E('Land Fort in Eligible Province','+1','gain'),E('Local Garrison Requirement','+10%','cost')]]
    by_id['ISR2_controlled_sites']['effects'] += [
        dict(row,heading='Palestine: Per West Bank or Gaza Pressure Tier') for row in [
            E('Office Productivity','-4%','cost'),E('Bureaucracy Cost','+4%','cost'),E('Stability','-2%','cost')]]
    by_id['ISR2_foreign_footholds']['requirements'] += ['The chosen state is not controlled by Israel. Its actual controller exists.','At most two foreign footholds are funded at once.']
    by_id['ISR2_foreign_footholds']['effects'] += [
        dict(row,heading='Per Funded Foreign Foothold: Israel') for row in [
            cash(-1),budget('Foothold Funding',-.015),E('Office Productivity','+4%','gain'),E('Agricultural Productivity','+3%','gain')]]
    by_id['ISR2_foreign_footholds']['effects'] += [
        dict(row,heading='Per Funded Foreign Foothold: Actual Host') for row in [
            E('Agricultural Productivity','-3%','cost'),E('Police Cost','+4%','cost'),E('Bureaucracy Cost','+3%','cost')]]
    by_id['ISR2_foreign_footholds']['effects'] += [
        dict(row,heading='Per Funded Foreign Foothold: Selected State') for row in [
            E('Local Factory Access','-5 percentage points','cost'),E('Local Supplies','-8%','cost')]]
    by_id['ISR2_foreign_footholds']['effects'] += [
        dict(row,heading='Palestine: Per Affected West Bank or Gaza Area') for row in [
            E('Office Productivity','-4%','cost'),E('Bureaucracy Cost','+4%','cost'),E('Stability','-2%','cost')]]

    def terms(key,country,rows):
        node=by_id['ISR2_'+key]
        for row in rows:
            node['effects'].append(dict(row,heading='If they accept: '+country))
    terms('irrigation_exports','Israel',[
        E('Treasury','+0.8% of recipient annual GDP','gain'),cash(-.3),
        budget('Irrigation Contract Maintenance',-.005,104),opinion('Recipient',10)])
    terms('irrigation_exports','Recipient',[
        cash(-.8),E('National Spirit','Precision Irrigation Contract, 104 weeks','gain'),
        E('Agricultural Productivity','+10%','gain'),opinion('Israel',10)])
    terms('arms_exports','Israel',[
        E('Treasury','+1% of buyer annual GDP','gain'),cash(-.4),
        E('Specified Infantry Equipment at Delivery','-250','cost'),
        E('National Spirit','Export Production Commitment, at most 26 weeks','cost'),E('Factory Output','-5%','cost')])
    terms('arms_exports','Buyer',[cash(-1),E('Specified Infantry Equipment at Delivery','+250','gain')])
    terms('mashav','Israel',[cash(-.3),budget('MASHAV Mission Expense',-.01,52),opinion('Recipient',10)])
    terms('mashav','Recipient',[research('Agriculture'),
        E('National Spirit','MASHAV Agricultural Mission, 52 weeks','gain'),E('Agricultural Productivity','+5%','gain'),opinion('Israel',10)])
    terms('washington','Israel',[cash(-.8),E('Air Experience','+35','gain'),research('Aircraft'),opinion('United States',15)])
    terms('washington','United States',[E('Treasury','+0.8% of Israeli annual GDP','gain'),opinion('Israel',15)])
    for country in ['Israel','Recipient']:
        terms('european_orders',country,[cash(-.5),
            E('National Spirit','Civilian Workshop Partnership, 104 weeks','gain'),
            E('Civilian Industry Productivity','+5%','gain'),research('Industry' if country=='Israel' else 'Electronics'),opinion('Partner',10)])
        terms('liaison_limits',country,[cash(-.25),budget('Signals Liaison Expense',-.005,52),
            research('Encryption'),E('National Spirit','Limited Signals Liaison, 52 weeks','gain'),
            E('Foreign Influence Defense','+10%','gain')])
    terms('eastern_credit','Israel',[cash(4),debt(4),
        E('Loan Principal Repayment','-0.03846% of quoted Israeli GDP per week for 104 weeks','cost'),
        E('Loan Interest','-0.00308% of quoted Israeli GDP per week for 104 weeks','cost'),opinion('Soviet Union',15)])
    terms('eastern_credit','Soviet Union',[
        E('Treasury','-4% of quoted Israeli GDP','cost'),
        E('Loan Principal Receipt','+0.03846% of quoted Israeli GDP per week for 104 weeks','gain'),
        E('Loan Interest Receipt','+0.00308% of quoted Israeli GDP per week for 104 weeks','gain'),opinion('Israel',15)])
    terms('negotiated_terms','Israel',[
        E('Treasury Transfer to Palestine','-0.02% of quoted Israeli GDP per week for 52 weeks','cost'),opinion('Palestine',10)])
    terms('negotiated_terms','Palestine',[
        E('Treasury Transfer from Israel','+0.02% of quoted Israeli GDP per week for 52 weeks','gain'),
        E('Selected Area Pressure','Maximum 1 tier for 52 weeks','gain'),
        E('Office Productivity Relief at Tier 2','+4%','gain'),E('Bureaucracy Cost Relief at Tier 2','-4%','gain'),
        E('Stability Relief at Tier 2','+2%','gain'),opinion('Israel',10)])
    # Final independent content review: prices follow the actual order, public
    # guarantees cannot become free permanent bonuses, and party identities
    # must remain institutionally different beyond their names.
    for key in ['credit_guarantees','workshop_guarantees']:
        node=by_id['ISR2_'+key]
        node['programme']='Funded guarantee programme: 52 weeks'
        node['mechanics'].append('The matching productivity/investment benefit and its provision run for the same 52 weeks. Renewal charges a new full provision; expiry removes the benefit. No free permanent guarantee bonus.')
    savings=by_id['ISR2_household_savings']
    savings['label']='Bid for Domestic Development Credit'
    savings['description']='Invite competing domestic subscriptions for a defined development note. The treasury gains an additional source of capital while retaining the debt obligation and the need for competitive borrowing terms.'
    savings['effects']=[row for row in savings['effects'] if row.get('native_key') not in ['offices_productivity','mdcw_cw_market_exposure']]
    savings['effects'] += [cash(2),debt(2),E('Interest Rate','-0.15 percentage points','gain',native_key='interest_rate_multiplier_modifier',amount=-.15)]
    savings['modifiers']={'interest_rate_multiplier_modifier':-.15}
    schools=by_id['ISR2_study_guarantees']
    schools['label']='Independent Schools, Shared Purchasing'
    schools['description']='Keep community authority over the schools while pooling supplies, maintenance and purchasing. A joint service office can reduce the cost of the protected network without converting its curriculum into a government department.'
    schools['effects']=paid(.6)+[E('Education Cost','-6%','gain',native_key='education_cost_multiplier_modifier',amount=-.06),opinion('Religious Institutions',15)]
    schools['modifiers']={'education_cost_multiplier_modifier':-.06}
    welfare=by_id['ISR2_communal_welfare']
    welfare['description']='Communal organisations will take on a defined share of clinics, meals and household relief while purchasing supplies through a common office. The state saves part of its central service bill and underwrites a continuing grant.'
    welfare['effects']=paid(.8)+[
        E('Healthcare Cost','-10%','gain',native_key='health_cost_multiplier_modifier',amount=-.10),
        E('Social Spending Cost','-8%','gain',native_key='social_cost_multiplier_modifier',amount=-.08),
        budget('Communal Relief Grant',-.005)]
    welfare['modifiers']={'health_cost_multiplier_modifier':-.10,'social_cost_multiplier_modifier':-.08}
    welfare['programme']='Governing programme while communal relief is funded'
    arms=by_id['ISR2_arms_exports']
    arms['effects']=[unlock('Offer an Israeli Equipment Production Contract')]
    arms['mechanics']=['Proposed standard order: 1,000 infantry-equipment sets of an agreed accessible model, with spares and training. Both countries see the same fixed $0.01 billion invoice; this is a proposed balance quote, not a historical equipment price. Israel receives the buyer payment and spends $0.004 billion on setup. It transfers 1,000 actual stockpiled units at delivery. Pending orders impose -5% factory output for at most 26 weeks. One pending order per seller; one completed order per buyer per 52 weeks. No delivery without stock; cancellation refunds the buyer. The contract must use the existing equipment trade and equipment references, not conjure a new model.']
    terms('arms_exports','Israel',[
        E('Treasury: Buyer Payment','+$0.01000 billion','gain'),E('Treasury: Setup','-$0.00400 billion','cost'),
        E('Agreed Infantry Equipment at Delivery','-1,000','cost'),
        E('National Spirit','Export Production Commitment, at most 26 weeks','cost'),
        E('Factory Output','-5%','cost'),E('Army Experience','+5','gain')])
    terms('arms_exports','Buyer',[
        E('Treasury','-$0.01000 billion','cost'),E('Agreed Infantry Equipment at Delivery','+1,000','gain'),E('Army Experience','+10','gain')])
    by_id['ISR2_arms_exports']['agreement_preview']=arms['mechanics'][:]
    terms('eastern_credit','Israel',[
        E('Public Debt Principal','-0.03846% of quoted Israeli GDP per week for 104 weeks','gain')])
    by_id['ISR2_eastern_credit']['mechanics'].append('The final principal instalment corrects five-digit rounding. Bilateral interest replaces, rather than duplicates, the debt ledger charge on this instrument; that routing is a required new integration.')
    talks=by_id['ISR2_rakah_talks']
    talks['label']='A Municipal Employment Order Book'
    talks['description']='Put the public-employment programme into workshops and services in actual communities. Territorial talks remain available through the common diplomatic branch; they are not a compulsory finale for a communist government.'
    talks['effects']=paid(2)+asset('Selected Israeli Core State','Office District',2)+asset('Selected Israeli Core State','Infrastructure')
    talks['requirements'] += ['An owned and controlled Israeli core state with capacity.']
    talks['mechanics']=['A one-time paid domestic project. It grants no core, changes no border and does not count as a settlement in occupied territory.']
    trigger_map={0:'western_autocrats_are_in_power',1:'western_conservatism_are_in_power',2:'western_liberals_are_in_power',3:'western_social_democrats_are_in_power',4:'emerging_communist_state_are_in_power',13:'neutrality_neutral_autocracy_are_in_power',14:'neutrality_neutral_conservatism_are_in_power',16:'neutrality_neutral_libertarians_are_in_power',18:'neutrality_neutral_social_are_in_power',19:'neutrality_neutral_communism_are_in_power',20:'nationalist_right_wing_populists_are_in_power'}
    for gg in GROUPS:
        gg['runtime_party_trigger']=trigger_map.get(gg['party_slot'])
    for node in NODES:
        gg=next(g for g in GROUPS if g['id']==node['group'])
        if gg['kind']=='party' and node['programme']=='Governing programme' and not node['modifiers']:
            node['programme']='One-time achievement; national assets remain'
    from policy_expansion import expand
    data['policy_expansion']=expand(globals())
    from focus_actions import convert
    data['focus_actions']=convert(globals())
    from focus_layout import arrange
    arrange(NODES, GROUPS)
    data['revision']='2.2-focus-only-20261028'
    data['version']='2.2'
    data['default_focus']='ISR2_mafdal_survey'
    data['nodes']=NODES
    data['layout']['icons']={key:old['layout']['icons'][key] for key in set(n['icon'] for n in NODES)}
    data['starting'].append(dict(label='Palestinian Institutional Pressure',
        description='Applies automatically if Palestine exists and its West Bank or Gaza core is affected. Two tiers per area, four tiers at most. A foreign foothold counts as one tier. No Palestinian approval is required.',
        effects=[E('Office Productivity per Tier','-4%','cost'),E('Bureaucracy Cost per Tier','+4%','cost'),E('Stability per Tier','-2%','cost')]))
    HERE.mkdir(exist_ok=True)
    OUT.mkdir(parents=True,exist_ok=True)
    (HERE/'design.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'design.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(project=data['project'],focuses=len(NODES),groups=len(GROUPS),party_groups=sum(g['kind']=='party' for g in GROUPS),icons=len(icons),workforce=sum(value for _,value in workforce)),indent=2))


if __name__=='__main__':
    finish()
