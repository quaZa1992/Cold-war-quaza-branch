# IMPERIA CW — Cold War: North Korea 1970 approval concept, never installs game files.
"""Canonical design data and review artifacts. Run only writes beside this script and the chat visualization root."""
from pathlib import Path
from collections import Counter, defaultdict
import json, re, base64, io, html, math, hashlib
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
VIS = Path(r'C:\Users\sonyz\.codex\visualizations\2026\10\23\01a1692a-5756-7333-ab22-85bb052e65ec')
P = 'COLDWAR_NKO_'
NODES, GROUPS = [], []

# Native modifier keys are deliberately explicit; labels are proposal tooltips, not new modifier definitions.
STATS = {
 'pp':('political_power_factor','Political power gain'), 'stab':('stability_factor','Stability'),
 'research':('research_speed_factor','Research speed'), 'prod':('productivity_growth_modifier','Productivity growth'),
 'build':('production_speed_buildings_factor','Construction speed'), 'civ':('production_speed_industrial_complex_factor','Civilian factory construction'),
 'milbuild':('production_speed_arms_factory_factor','Military factory construction'), 'output':('industrial_capacity_factory','Factory output'),
 'effcap':('production_factory_max_efficiency_factor','Production efficiency cap'), 'effgain':('production_factory_efficiency_gain_factor','Production efficiency growth'),
 'agri':('agricolture_productivity_modifier','Agricultural productivity'), 'agribuild':('production_speed_agriculture_district_factor','Agricultural district construction'),
 'energy':('energy_use_multiplier','Electricity consumption'), 'fossil':('fossil_pp_energy_generation_modifier','Fossil power generation'),
 'renew':('renewable_energy_gain_multiplier','Renewable power generation'), 'nucpower':('nuclear_energy_generation_modifier','Nuclear power generation'),
 'bureau':('bureaucracy_cost_multiplier_modifier','Weekly administration expenditure'),
 'police':('police_cost_multiplier_modifier','Weekly policing expenditure'), 'education':('education_cost_multiplier_modifier','Weekly education expenditure'),
 'health':('health_cost_multiplier_modifier','Weekly healthcare expenditure'), 'welfare':('social_cost_multiplier_modifier','Weekly social expenditure'),
 'personnel':('army_personnel_cost_multiplier_modifier','Weekly army personnel expenditure'), 'equipment':('equipment_cost_multiplier_modifier','Weekly equipment expenditure'),
 'tax':('tax_gain_multiplier_modifier','Tax revenue'), 'corptax':('corporate_tax_income_multiplier_modifier','Corporate tax revenue'),
 'interest':('interest_rate_multiplier_modifier','Interest rate multiplier'), 'trade':('trade_opinion_factor','Trade deal opinion factor'),
 'influence_def':('foreign_influence_defense_modifier','Foreign influence defence'),
 'org':('army_org_factor','Army organization'), 'defence':('army_core_defence_factor','Army defence on core territory'),
 'attack':('army_attack_factor','Army attack'), 'planning':('max_planning_factor','Maximum planning'),
 'supply':('supply_consumption_factor','Supply consumption'), 'training':('training_time_factor','Training time'),
 'armyxp':('experience_gain_army','Army experience gain'), 'special':('special_forces_cap','Special forces capacity'),
 'air':('air_mission_efficiency','Air mission efficiency'), 'navy':('navy_org_factor','Naval organization'),
 'fuel':('non_electric_fuel_consumption_modifier','Non-electric fuel consumption'),
 'sanction':('imp_sanction_resistance','Imperia sanction resistance'),
}
ICON = {
 'wpk':'kim_il_sung','kdp':'NKO_party_reform','chondo':'agriculture','cabinet':'NKO_anti_corruption',
 'kpa':'dprk_army','yanan':'NKO_party_reform','union':'NKO_workers','christian':'christianity',
 'economy':'economic_civil_industry','defence':'NKO_defence','diplomacy':'NKO_38_parallel','atomic':'NKO_nuclear',
}
def group(key, title, x, y, slot=None, status='National programme', note=''):
    GROUPS.append(dict(id=key,title=title,x=x,y=y,slot=slot,status=status,note=note,icon=ICON[key]))
def n(key,title,x,y,pre='',mods=None, money=0, cost=5, desc='', extra=None, gate='', icon=None, remove=None, duration=None):
    g = GROUPS[-1]
    groups = [[P+a for a in s.split(',')] for s in pre.split(';') if s]
    NODES.append(dict(id=P+key,key=key,title=title,group=g['id'],x=x+g['x'],y=y+g['y'],dx=x,dy=y,
        anchor=None if not any(v['group']==g['id'] for v in NODES) else next(v['id'] for v in NODES if v['group']==g['id']),
        prerequisites=groups,mutex=[],cost=cost,days=cost*7,money=money,
        modifiers={STATS[k][0]:v for k,v in (mods or {}).items()},
        labels={STATS[k][0]:STATS[k][1] for k in (mods or {})},
        description=desc,extra=extra or [],gate=gate,slot=g['slot'],icon=icon or g['icon'],
        ownership='Party programme' if g['slot'] is not None else 'National policy / durable development',
        remove=remove or [],duration=duration, historical_status=g['status']))
def mex(*keys):
    for a in keys:
        next(v for v in NODES if v['key']==a)['mutex'] += [P+b for b in keys if a!=b]
def building(kind,levels,region):
    return dict(kind='building',type=kind,levels=levels,region=region)
def tech(cat,bonus=.5,uses=1):
    return dict(kind='research',category=cat,bonus=bonus,uses=uses)
def offer(name,payer,cost,benefit,flag,conditions='Recipient exists, is independent, at peace with sender, and accepts.'):
    return dict(kind='offer',name=name,payer=payer,cost=cost,benefit=benefit,flag=P+flag,conditions=conditions)
def action(name,detail): return dict(kind='action',name=name,detail=detail,status='New country adapter required; native primitives identified')

# WPK: three separate policy dilemmas, no artificial focus to unlock the starting party.
group('wpk',"Workers' Party of Korea",10,0,4,'Historical government; internal alternatives',
      'Kim Il Sung remains the starting head of government. The heir is cultivated from 1974, not installed as ruler in 1970.')
n('fifth_congress','The Fifth Congress',0,0,mods={'pp':.05,'bureau':.03},cost=3,desc='Set the programme of the party congress after the extended Seven-Year Plan.',extra=[action('Planning decisions','Open a choice of the already designed national investment programmes; no separate reward for opening the menu.')])
n('monolithic','Monolithic Leadership',-4,1,'fifth_congress',{'pp':.16,'stab':.08,'research':-.06,'bureau':.10},desc='Concentrate authority in the Leader and his trusted cadre network.',remove=['monolithic_start'])
n('collective','Collective Deliberation',4,1,'fifth_congress',{'research':.07,'prod':.06,'stab':-.06,'bureau':.08},desc='Restore policy debate within the Workers’ Party while accepting a less unified command.',remove=['monolithic_start'])
mex('monolithic','collective')
n('loyalty','Loyalty in Appointments',-4,2,'monolithic',{'influence_def':.10,'prod':-.03},desc='Promote politically reliable officials, narrowing the pool of technical talent.')
n('debate','Reports without Reprisals',4,2,'collective',{'prod':.05,'pp':-.05},desc='Let ministries report missed targets without treating every failure as disloyalty.')
n('presidency','The Presidential State',-4,3,'loyalty',{'pp':.06,'police':.05},desc='Gather constitutional and administrative authority around Kim Il Sung.',gate='Historical timing: 1972 constitution or a separately negotiated earlier constitutional settlement.')
n('cabinet_reports','Cabinet Accountability',4,3,'debate',{'bureau':-.06,'pp':-.03},desc='Require ministers to defend plans and expenditure before a collective party leadership.')
n('ten_principles','The Ten Principles',-4,4,'presidency',{'stab':.04,'research':-.02},desc='Bind institutions to a uniform ideological hierarchy.',gate='Historical timing: 1974; earlier completion would be explicitly alternate history.')
n('cadre_tenure','Professional Cadre Tenure',4,4,'cabinet_reports',{'research':.04,'bureau':.04},desc='Protect experienced administrators while accepting a more entrenched bureaucracy.')
n('party_settlement','The Party Settlement',0,5,'ten_principles,cadre_tenure',{'influence_def':.06},desc='Consolidate the institutional settlement chosen by the congress.')
n('campaigns','Campaign Mobilization',-4,6,'party_settlement',{'build':.10,'prod':-.04,'welfare':.04},desc='Concentrate labour on visible projects at the expense of routine production and household provision.')
n('technical_cadres','Technical Cadres',4,6,'party_settlement',{'prod':.08,'build':-.05,'education':.08},money=1,desc='Replace emergency campaigns with trained supervision and measured investment.')
mex('campaigns','technical_cadres')
n('three_revolutions','Three Revolutions Groups',-4,7,'campaigns',{'effgain':.08,'bureau':.06},desc='Send ideological, technical and cultural teams into workplaces.',gate='Historical timing: movement organized from 1973.')
n('engineer_commissions','Engineers in the Ministries',4,7,'technical_cadres',{'effcap':.06,'bureau':.04},desc='Give technical commissions the authority to revise unrealistic orders.')
n('red_banner','The Red Banner Movement',-4,8,'three_revolutions',{'output':.06,'energy':.05,'stab':-.02},desc='Reward accelerated production and model work teams while placing further pressure on inputs.',gate='Historical timing: 1975 campaign.')
n('honest_targets','Publish Achievable Targets',4,8,'engineer_commissions',{'prod':.05,'pp':-.04},desc='Accept less spectacular headlines in return for plans that plants can deliver.')
n('plan_discipline','Discipline in the Plan',0,9,'red_banner,honest_targets',{'effgain':.04},desc='Carry the chosen management settlement into the next planning period.')
n('family_succession','Cultivate the Party Centre',-4,10,'plan_discipline',{'pp':.08,'bureau':.06,'research':-.02},desc='Build Kim Jong Il’s authority inside the party without displacing Kim Il Sung.',gate='From 1974; Kim Il Sung in office; successor alive.',icon='Kim_Jong_il')
n('committee_succession','A Collective Succession',4,10,'plan_discipline',{'research':.05,'prod':.04,'stab':-.06},desc='Prepare a committee succession instead of a hereditary transfer.',gate='From 1974; Kim Il Sung in office; an explicitly counterfactual settlement.')
mex('family_succession','committee_succession')
n('party_media','The Party and the Arts',-4,11,'family_succession',{'stab':.05,'welfare':.05},desc='Finance a cultural apparatus that presents the successor as the guardian of continuity.')
n('secretariat','A Responsible Secretariat',4,11,'committee_succession',{'bureau':-.05,'pp':-.03},desc='Distribute appointments among a responsible secretariat rather than the ruling household.')
n('sixth_congress','The Sixth Congress',-4,12,'party_media',{'influence_def':.08,'research':-.02},desc='Publicly confirm the successor’s party offices while the founding Leader remains in command.',gate='From October 1980; no automatic head-of-state replacement.',icon='Kim_Jong_il')
n('succession_rules','Rules for the Next Leader',4,12,'secretariat',{'stab':.04,'bureau':.03},desc='Set procedures for a future vacancy and bind commanders to the institutional settlement.',gate='Requires an agreed counterfactual succession settlement; no purge victim is resurrected.')
n('continuity','A State beyond the Founder',0,13,'sixth_congress,succession_rules',{'prod':.04,'bureau':.03},desc='Secure continuity through the leadership settlement the country has chosen.')

# Shared national development: capacity survives changes of government; programme burdens do too until replaced.
group('economy','Planning, Power and Living Standards',34,0,note='Industrial Korea with real bottlenecks, not a pre-industrial blank slate. Native building employment, fuel, power and maintenance remain active.')
n('plan_review','Review the Extended Plan',0,0,mods={'effgain':.04},cost=3,desc='Audit the gap between targets, installed capacity and available supplies.')
n('heavy_priority','Heavy Industry First',-6,1,'plan_review',{'milbuild':.12,'effcap':.08,'agri':-.06,'energy':.08},money=2,desc='Prioritize metals and machinery while scarce capital is withheld from agriculture and household output.')
n('light_priority','Food and Light Industry',0,1,'plan_review',{'agri':.12,'civ':.10,'milbuild':-.08,'welfare':.05},money=2,desc='Direct investment toward everyday supply at a cost to the defence-industrial build-up.')
n('balanced_priority','Measured Industrial Growth',6,1,'plan_review',{'prod':.08,'effgain':.06,'build':-.04,'bureau':.05},money=2,desc='Adopt a slower investment plan with more reliable input balances.')
mex('heavy_priority','light_priority','balanced_priority')
n('steelworks','Modernize the Steelworks',-6,2,'heavy_priority',money=4,desc='Re-equip one established industrial centre and pay the full investment cost.',extra=[building('arms_factory',1,'existing owned industrial state')])
n('food_district','Equip the Cooperatives',0,2,'light_priority',money=3,desc='Add a funded agricultural district rather than promising food without productive capacity.',extra=[building('agriculture_district',1,'owned western agricultural state')])
n('machine_tools','Machine Tool Standards',6,2,'balanced_priority',{'effcap':.06,'education':.04},money=2,desc='Improve interchangeability and maintenance rather than chasing gross output totals.')
n('input_balance','Balance the Inputs',0,3,'steelworks,food_district,machine_tools',{'prod':.04},desc='Bring transport, electricity and intermediate supplies into the investment plan.',remove=['plan_overstretch'])
n('coal_power','Coal-fired Expansion',-4,4,'input_balance',money=3,cost=7,desc='Add dependable generating capacity with the native fuel consumption and running costs.',extra=[building('fossil_powerplant',1,'owned industrial state')],icon='NKO_huichon')
n('hydro_power','Hydroelectric Investment',4,4,'input_balance',money=4,cost=7,desc='Finance renewable generating capacity and accept a higher initial capital cost.',extra=[building('renewable_energy_infra',1,'owned northern highland state')],icon='NKO_huichon')
mex('coal_power','hydro_power')
n('power_grid','Repair the Power Grid',0,5,'coal_power,hydro_power',{'energy':-.08},money=2,desc='Reduce transmission losses through paid grid maintenance.',remove=['power_bottleneck'])
n('rail_corridor','The Industrial Rail Corridor',-4,6,'power_grid',money=3,desc='Increase infrastructure along an owned industrial corridor.',extra=[building('infrastructure',1,'owned industrial state below the infrastructure cap')],icon='NKO_railways')
n('housing','Housing near the Plants',4,6,'power_grid',{'stab':.04,'welfare':.06},money=2,desc='Fund housing and urban services so industrial recruitment can be sustained.')
n('fertilizer','Fertilizer and Irrigation',-4,7,'rail_corridor',{'agri':.08,'energy':.04},money=2,desc='Improve yields through inputs that require electricity and dependable distribution.')
n('public_health','County Clinics',4,7,'housing',{'prod':.04,'health':.08},money=1,desc='Expand basic healthcare at a continuing public cost.')
n('living_standards','A Sustainable Ration',0,8,'fertilizer;public_health',{'agri':.05,'welfare':.03},desc='Improve the reliability of food distribution after investment in rural and urban supply.',remove=['ration_strain'])
n('state_procurement','State Procurement Boards',-4,9,'living_standards',{'agri':.08,'tax':.04,'prod':-.03,'bureau':.06},desc='Stabilize procurement through guaranteed state purchasing and closer supervision.')
n('household_plots','Licensed Household Plots',4,9,'living_standards',{'agri':.12,'prod':.04,'tax':-.05,'pp':-.03},desc='Let households retain more produce while accepting weaker state extraction.')
mex('state_procurement','household_plots')
n('distribution_reform','Regional Distribution Depots',0,10,'state_procurement,household_plots',{'supply':-.04,'bureau':.03},money=2,desc='Build a distribution network that reduces waste and supplies the army and civilian economy.')
n('domestic_finance','Invest from Domestic Savings',-4,11,'distribution_reform',{'interest':-.05,'build':-.04,'welfare':.04},desc='Avoid a hard-currency borrowing surge by accepting slower investment.')
n('western_credit','Purchase Western Machinery',4,11,'distribution_reform',{'prod':.12,'effcap':.06,'interest':.12},desc='Borrow to purchase foreign plant and accept debt service and a weaker credit position.',extra=[dict(kind='debt',amount=3),building('industrial_complex',1,'owned industrial state')])
mex('domestic_finance','western_credit')
n('technical_schools','Industrial Technical Schools',-4,12,'domestic_finance',{'research':.04,'education':.06},money=1,desc='Train technicians domestically instead of relying on a larger foreign-credit package.')
n('credit_reckoning','Meet the Foreign Bills',4,12,'western_credit',{'prod':.03},money=3,desc='Pay down the specific machinery loan; refusing repayment leads to a temporary credit crisis.',extra=[dict(kind='repay_loan',amount=3,only='western_credit')])
n('export_quality','Quality for Export',0,13,'technical_schools,credit_reckoning',{'prod':.04,'effgain':-.03},money=1,desc='Slow production-line changes to improve the consistency of saleable output.')
n('joint_ventures','Controlled Joint Ventures',0,14,'export_quality',{'prod':.06,'corptax':-.05,'influence_def':-.05},money=2,desc='Offer tightly limited partnerships and tax concessions without assuming foreign investors will provide free capital.',gate='Historical law from 1984, or an explicit earlier alternate reform.',extra=[action('Joint venture offers','Recipient-consent investment contracts use existing Imperia investment hooks; no unconditional foreign factory grant.')])

# Armed forces: a national doctrine branch and four service programmes, no starting OOB changes.
group('defence',"The Korean People's Army",58,0,note='Native defense, personnel and equipment costs remain. No starting units, future technology or free stockpiles are granted.')
n('lessons_1969','Lessons of the Border Crisis',0,0,mods={'armyxp':.06,'personnel':.03},cost=3,desc='Review the 1968–69 confrontation and restore professional military reporting.')
n('fortress','The Fortress State',-4,1,'lessons_1969',{'defence':.12,'supply':-.06,'attack':-.06,'prod':-.04},desc='Prepare an economical territorial defence at the cost of offensive flexibility.')
n('mobile_army','A Mobile Field Army',4,1,'lessons_1969',{'org':.08,'planning':.08,'equipment':.12,'fuel':.08},desc='Build a more flexible field army that consumes more equipment and fuel.')
mex('fortress','mobile_army')
n('red_guards','Worker-Peasant Red Guards',-4,2,'fortress',{'defence':.06,'training':-.08,'prod':-.04},desc='Expand reserve training while removing civilian labour from regular production.',icon='WPRG')
n('staff_college','The General Staff College',4,2,'mobile_army',{'planning':.06,'armyxp':.06,'education':.05},money=1,desc='Improve staff work through a paid officer education programme.')
n('army_reorganization','Reorganize the Commands',0,3,'red_guards,staff_college',{'org':.04,'bureau':.03},desc='Translate the selected doctrine into command and logistics procedures.')
n('mass_artillery','Artillery Concentration',-6,4,'army_reorganization',{'attack':.06,'supply':.08,'equipment':.05},money=2,desc='Concentrate firepower while accepting greater ammunition and transport requirements.',icon='NKO_koksan')
n('air_defence','Air Defence Commands',-2,4,'army_reorganization',{'air':.06,'equipment':.06},money=2,desc='Improve coordination of air defence forces without granting future aircraft.',icon='NKO_fighter')
n('coastal_denial','Coastal Denial',2,4,'army_reorganization',{'navy':.06,'equipment':.04},money=2,desc='Concentrate naval training on denying coastal access.',icon='NKO_submarine')
n('special_operations','Special Operations Training',6,4,'army_reorganization',{'special':.12,'personnel':.06,'org':-.02},money=1,desc='Train specialist formations at a cost to the regular army’s resources.',icon='NKO_sso')
n('ammunition_standards','Ammunition Standards',-6,5,'mass_artillery',{'effcap':.06,'effgain':-.04},money=1,desc='Standardize ammunition at the expense of flexible production changes.')
n('air_warning','Air Warning Network',-2,5,'air_defence',money=2,desc='Fund an early-warning station in owned territory with available capacity.',extra=[building('radar_station',1,'owned northern state with radar capacity')])
n('naval_workshops','Coastal Naval Workshops',2,5,'coastal_denial',money=3,desc='Add a funded repair and shipbuilding facility with native staffing costs.',extra=[building('dockyard',1,'owned coastal state with free shared slots')])
n('reconnaissance','Reconnaissance Standards',6,5,'special_operations',{'planning':.05,'personnel':.03},desc='Improve reconnaissance training and the quality of operational preparation.')
n('joint_logistics','Joint Logistics',0,6,'ammunition_standards;air_warning;naval_workshops;reconnaissance',{'supply':-.06,'bureau':.04},money=2,desc='Unify logistics across all four service programmes.')
n('civilian_conversions','Convert Selected Workshops',-4,7,'joint_logistics',{'civ':.10,'milbuild':-.08,'equipment':.04},money=2,desc='Release industrial workshops for civilian production while reducing military expansion.')
n('arsenal_priority','Secure the National Arsenal',4,7,'joint_logistics',{'output':.08,'civ':-.08,'energy':.06},money=2,desc='Give defence plants priority over civilian construction and power allocation.')
mex('civilian_conversions','arsenal_priority')
n('logistics_reserve','A Maintained Reserve',0,8,'civilian_conversions,arsenal_priority',{'org':.04,'personnel':.05},desc='Maintain a sustainable reserve rather than a paper mobilization total.')
n('military_research','Military Technical Institutes',-4,9,'logistics_reserve',{'research':.03,'education':.04},money=1,desc='Improve domestic military engineering and testing.')
n('readiness_inspections','Readiness Inspections',4,9,'logistics_reserve',{'org':.03,'training':.04},desc='Make readiness reporting more demanding and allow more time for effective training.')

# Diplomacy: patron deals are mixable; Korean settlement and coercion are a real exclusive strategy choice.
group('diplomacy','Patrons and the Korean Question',82,0,note='Every agreement has a recipient-controlled reply. No forced faction membership, annexation, tribute or aid from another player.')
n('independent_diplomacy','Independent Diplomacy',0,0,mods={'influence_def':.08,'trade':-.05},cost=3,desc='Preserve freedom of action while bargaining with the larger powers.')
n('moscow_offer','A Machinery Offer to Moscow',-6,1,'independent_diplomacy',desc='Request a paid machinery package on terms Moscow can accept or refuse.',icon='align_to_russia',extra=[offer('Soviet machinery contract','NKO',2,'NKO receives 1 civilian factory; SOV receives $2.000 billion. No payout on refusal.','moscow_signed')])
n('beijing_offer','Repair Relations with Beijing',0,1,'independent_diplomacy',desc='Propose a paid agricultural and technical cooperation agreement.',icon='align_to_china',extra=[offer('Chinese agricultural cooperation','NKO',1,'NKO gains agricultural productivity +5% and research speed +2% for 730 days; CHI receives $1.000 billion.','beijing_signed')])
n('diaspora_trade','Trade through Chongryon',6,1,'independent_diplomacy',{'prod':.05,'corptax':-.04,'influence_def':-.03},money=1,desc='Use diaspora firms to widen technical and commercial contacts without treating remittances as unlimited income.',icon='NKO_money')
n('soviet_training','Soviet Technical Placements',-6,2,'moscow_offer',{'research':.04,'influence_def':-.04,'education':.03},money=1,desc='Place Korean engineers in Soviet institutions after an agreement is signed.',gate='Requires the Soviet machinery agreement, not merely completion of its offer focus.')
n('border_trade','Regularize Border Trade',0,2,'beijing_offer',{'agri':.04,'tax':-.02},money=1,desc='Provide customs and storage facilities for regulated trade.',gate='Requires the Chinese cooperation agreement, not merely completion of its offer focus.')
n('export_offices','Commercial Representation',6,2,'diaspora_trade',{'trade':.08,'bureau':.04},money=1,desc='Fund a professional commercial service rather than relying solely on political delegations.')
n('external_balance','Keep Both Doors Open',0,3,'soviet_training,border_trade,export_offices',{'influence_def':.05,'bureau':.03},desc='Maintain a diversified foreign procurement policy. Moscow and Beijing remain mixable partners.')
n('detente','Open the Inter-Korean Channel',-4,4,'external_balance',{'trade':.08,'attack':-.04,'police':.03},desc='Offer talks on divided families, communications and reduced tension.',extra=[offer('Inter-Korean channel','NKO',1,'Both receive stability +3 percentage points once and a 365-day trade-opinion factor +10%; KOR receives $1.000 billion for joint arrangements.','channel_signed')],icon='DPRK-ROK_shake_flags')
n('coercion','Pressure across the Armistice',4,4,'external_balance',{'planning':.08,'trade':-.15,'police':.08},desc='Use pressure and readiness as bargaining instruments while accepting a more difficult trade environment.')
mex('detente','coercion')
n('red_cross','Divided Families',-4,5,'detente',{'stab':.03,'bureau':.03},money=1,desc='Finance contact and travel arrangements only after both governments agree.',gate='Requires the signed inter-Korean channel.')
n('front_broadcasting','Reunification Broadcasting',4,5,'coercion',{'influence_def':.05,'police':.04},money=1,desc='Sustain the national front’s external propaganda; it does not manufacture a southern uprising.')
n('confederation_offer','A Confederation Proposal',-4,6,'red_cross',desc='Submit a negotiated confederal framework that protects both players’ control over their countries.',gate='Requires signed channel; both states independent and at peace.',extra=[offer('Confederal consultative council','NKO',2,'Signed council spirit in both countries: trade-opinion factor +10%, weekly administration expenditure +3%; no annexation or forced alliance.','council_signed')],icon='NKO_confederation_question')
n('armed_bargaining','Armed Bargaining',4,6,'front_broadcasting',{'defence':.05,'equipment':.05,'trade':-.05},desc='Maintain a stronger military negotiating position at a continuing financial cost.')
n('recognition','A Place in the Non-Aligned World',0,7,'confederation_offer,armed_bargaining',{'trade':.06,'bureau':.04},money=1,desc='Fund diplomatic representation among non-aligned states without automatically changing their alignment.')
n('civilian_export','Civilian Export Missions',-4,8,'recognition',{'trade':.10,'corptax':-.03},money=1,desc='Offer commercial concessions to win markets for civilian exports.')
n('security_export','Military Technical Missions',4,8,'recognition',{'armyxp':.08,'personnel':.06,'trade':-.06},money=1,desc='Send advisers only under voluntary bilateral contracts; arms revenue requires actual trade.')
mex('civilian_export','security_export')
n('external_resilience','Prepare for Unreliable Patrons',0,9,'civilian_export,security_export',{'sanction':.06,'prod':-.03},money=2,desc='Diversify inventories and replacement sources to reduce exposure to external restrictions.')

group('atomic','Science and the Atomic Question',102,0,note='Uses the existing Imperia / Cold War nuclear programme. No automatic uranium output, mines, fissile material or completed weapon.')
n('science','The Academy of Sciences',0,0,mods={'research':.03,'education':.05},money=1,cost=3,desc='Support the scientific institutions needed for a long technical programme.')
n('reactor_training','Research Reactor Training',0,1,'science',money=2,desc='Fund reactor engineering studies and the preparation of qualified personnel.',extra=[tech('CAT_nuclear_reactors',.5)])
n('civil_atom','Civilian Atomic Cooperation',-3,2,'reactor_training',{'research':.04,'influence_def':-.04},desc='Seek foreign cooperation under verifiable limits on the programme.',extra=[offer('Civil nuclear engineering contract','NKO',3,'SOV receives $3.000 billion; NKO receives one additional 50% reactor research bonus and no free reactor.','atomic_cooperation')])
n('sovereign_atom','An Independent Atomic Programme',3,2,'reactor_training',{'research':.03,'education':.08,'sanction':-.06},money=3,desc='Invest in a national nuclear research programme while accepting cost and external suspicion.')
mex('civil_atom','sovereign_atom')
n('safeguards','Accept Reactor Safeguards',-3,3,'civil_atom',{'trade':.06,'bureau':.04},desc='Register safeguards obligations on the research programme.',gate='Signed civil cooperation; inspection obligations implemented through a new country adapter, not claimed as an existing NPT system.',extra=[action('Safeguards contract','Recipient-confirmed inspection contract. Violating the agreed terms suspends the contract rewards.')])
n('fuel_studies','The Domestic Fuel Cycle',3,3,'sovereign_atom',money=3,desc='Prepare a paid fuel-cycle programme using existing projects and construction requirements.',extra=[action('Nuclear project access','Only expose currently reachable native nuclear projects; no project completion, mine, uranium resource or fissile-material grant.')])
n('npt_offer','The NPT Bargain',-3,4,'safeguards',{'trade':.08,'influence_def':-.03},desc='Offer non-proliferation commitments in return for civil technical cooperation.',gate='Historical milestone December 1985, or an earlier negotiated alternate treaty; safeguards contract valid.',extra=[offer('Civil nuclear research extension','NKO',2,'SOV receives $2.000 billion; NKO gains nuclear power generation +8% only while safeguards remain valid. No promised Soviet reactor appears automatically.','npt_bargain')])
n('strategic_option','Authorize the Strategic Study',3,4,'fuel_studies',{'research':.03,'education':.06,'trade':-.08},money=4,cost=10,desc='Authorize a costly alternate-history weapons study, subject to the actual nuclear research and material requirements.',gate='Native nuclear programme eligibility and scientific prerequisites; this focus awards no nuclear weapon.',extra=[tech('CAT_nuclear_weapons',.35),action('Strategic programme','Research still pays the existing GDP/c- and inflation-scaled weekly nuclear development budget. Production still needs real material and native projects.')])

# Party-specific alternatives occupy distinct, collision-free footprints. All are conditional on actual rule.
group('kdp','Korean Democratic Party',6,17,5,'Satellite party; autonomous government is alternate history', 'Use KDP until 1981; KSDP thereafter through a name-only update. It is not an anarchist programme despite its inherited MD slot.')
n('kdp_charter','A Patriotic Democratic Charter',0,0,mods={'stab':.04,'pp':-.04},cost=3,desc='Give the party a governing charter grounded in civil administration and national reconciliation.')
n('kdp_social','A Social Republic',-3,1,'kdp_charter',{'prod':.06,'welfare':.10,'corptax':-.04},desc='Offer social protection and public investment with a larger recurrent budget.')
n('kdp_enterprise','A Republic of Enterprise',3,1,'kdp_charter',{'prod':.10,'corptax':-.08,'stab':-.04},desc='Support enterprise autonomy while accepting weaker revenue and a more unequal transition.')
mex('kdp_social','kdp_enterprise')
n('kdp_housing','Municipal Housing Boards',-3,2,'kdp_social',{'stab':.04,'bureau':.04},money=2,desc='Delegate housing budgets to municipal boards.')
n('kdp_licenses','Legal Small Enterprise',3,2,'kdp_enterprise',{'civ':.08,'bureau':.05},money=1,desc='Provide legal registration and supply contracts for small enterprise.')
n('kdp_budget','A Published Budget',0,3,'kdp_housing,kdp_licenses',{'interest':-.05,'pp':-.03},desc='Publish state accounts and reduce arbitrary fiscal intervention.')
n('kdp_courts','Independent Civil Courts',-3,4,'kdp_budget',{'prod':.05,'bureau':.06,'pp':-.03},money=1,desc='Make civil contracts enforceable beyond the ruling party’s immediate wishes.')
n('kdp_executive','A Strong Elected Executive',3,4,'kdp_budget',{'pp':.10,'stab':.04,'research':-.03},desc='Prefer a decisive civilian executive to wider institutional checks.')
mex('kdp_courts','kdp_executive')
n('kdp_civic','Civic Associations',-3,5,'kdp_courts',{'research':.04,'police':.04},desc='Permit professional and civic organization with a budget for public order.')
n('kdp_service','A Merit Civil Service',3,5,'kdp_executive',{'bureau':-.04,'education':.04},money=1,desc='Recruit civil servants through professional standards.')
n('kdp_social_compact','A Civilian Social Compact',0,6,'kdp_civic,kdp_service',{'stab':.04,'welfare':.03},desc='Bind the civilian government to the public services it has promised.')
n('kdp_reconciliation','Reconciliation First',-3,7,'kdp_social_compact',{'trade':.10,'attack':-.04,'influence_def':-.03},money=1,desc='Use the party’s civilian identity to support negotiated inter-Korean relations.')
n('kdp_sovereignty','Sovereignty before Settlement',3,7,'kdp_social_compact',{'influence_def':.10,'defence':.04,'trade':-.06},desc='Insist on sovereign equality while preparing a more guarded diplomacy.')
mex('kdp_reconciliation','kdp_sovereignty')
n('kdp_republic','A Durable Civil Republic',0,8,'kdp_reconciliation,kdp_sovereignty',{'prod':.04,'bureau':.03},desc='Consolidate the institutions of a civilian republic.')

group('chondo','Chondoist Chongu Party',22,17,7,'Satellite party; autonomous government is alternate history','Chondoism is an indigenous Korean religion and agrarian tradition, not a Muslim path or an imported theocracy.')
n('chondo_heaven','Humanity Is Heaven',0,0,mods={'stab':.05,'bureau':.03},cost=3,desc='Build a national programme around human dignity, rural community and Korean independence.')
n('chondo_cooperative','The Cooperative Village',-3,1,'chondo_heaven',{'agri':.12,'bureau':.08,'prod':-.02},desc='Retain common agricultural provision under stronger village institutions.')
n('chondo_household','The Family Holding',3,1,'chondo_heaven',{'agri':.15,'tax':-.06,'stab':-.03},desc='Give households greater control of land use and a larger share of their harvest.')
mex('chondo_cooperative','chondo_household')
n('chondo_granary','Village Granaries',-3,2,'chondo_cooperative',{'agri':.05,'welfare':.05},money=2,desc='Finance local storage and guaranteed village reserves.')
n('chondo_markets','Licensed Rural Markets',3,2,'chondo_household',{'prod':.05,'tax':-.03,'police':.03},money=1,desc='Legalize local exchange with enforceable market rules.')
n('chondo_land','A Rural Settlement',0,3,'chondo_granary,chondo_markets',{'agri':.04},desc='Consolidate the chosen rural property and procurement settlement.')
n('chondo_tolerance','Freedom of Conscience',-3,4,'chondo_land',{'research':.05,'stab':.03,'pp':-.05},desc='Protect believers and non-believers within a common citizenship.')
n('chondo_morality','A National Moral Order',3,4,'chondo_land',{'stab':.08,'pp':.05,'research':-.05},desc='Use Chondoist moral teaching to strengthen a more uniform national order.')
mex('chondo_tolerance','chondo_morality')
n('chondo_schools','County Schools',-3,5,'chondo_tolerance',{'research':.04,'education':.07},money=1,desc='Expand education in neglected rural districts.')
n('chondo_councils','Councils of Community',3,5,'chondo_morality',{'bureau':-.04,'prod':-.02},desc='Place local administration in the hands of established community networks.')
n('chondo_nation','The Donghak Inheritance',0,6,'chondo_schools,chondo_councils',{'influence_def':.08,'trade':-.03},desc='Present Korean independence as a shared national tradition.')
n('chondo_reforestation','Protect the Hillsides',-3,7,'chondo_nation',{'agri':.06,'agribuild':-.05},money=2,desc='Protect soil and catchments by limiting further cultivation of slopes.')
n('chondo_reclamation','Reclaim New Fields',3,7,'chondo_nation',money=3,desc='Finance agricultural capacity while accepting the full construction and staffing burden.',extra=[building('agriculture_district',1,'owned suitable coastal agricultural state')])
mex('chondo_reforestation','chondo_reclamation')
n('chondo_commonwealth','A Rural Commonwealth',0,8,'chondo_reforestation,chondo_reclamation',{'stab':.04,'welfare':.04},desc='Secure the rural services and institutions promised by the party.')

group('cabinet','Cabinet and Planning Commission',38,17,13,'Institutional technocratic alternative','A cabinet government is alternate history; it is not a new political party. Preserve historical Kim Il Sung at the start.')
n('cabinet_accounts','Accounts before Slogans',0,0,mods={'prod':.06,'pp':-.05},cost=3,desc='Make accurate accounts the basis of cabinet authority.')
n('cabinet_plant','Plant Manager Autonomy',-3,1,'cabinet_accounts',{'effcap':.10,'prod':.06,'corptax':-.05},desc='Delegate production decisions and allow plants to retain investment funds.')
n('cabinet_plan','An Integrated National Plan',3,1,'cabinet_accounts',{'build':.10,'effgain':.08,'bureau':.10},desc='Coordinate supplies centrally through a better funded planning apparatus.')
mex('cabinet_plant','cabinet_plan')
n('cabinet_contracts','Enforce Supply Contracts',-3,2,'cabinet_plant',{'prod':.04,'bureau':.04},money=1,desc='Require suppliers and plants to honour realistic delivery contracts.')
n('cabinet_statistics','A Statistical Service',3,2,'cabinet_plan',{'prod':.04,'education':.04},money=1,desc='Build professional statistical capacity throughout the ministries.')
n('cabinet_currency','A Hard-Currency Budget',0,3,'cabinet_contracts,cabinet_statistics',{'interest':-.06,'build':-.03},desc='Tie foreign procurement to the country’s ability to meet external bills.')
n('cabinet_austerity','Investment before Consumption',-3,4,'cabinet_currency',{'build':.10,'stab':-.05,'welfare':-.04},desc='Hold down current consumption to fund a higher investment share.')
n('cabinet_consumption','A Consumer Recovery',3,4,'cabinet_currency',{'agri':.06,'stab':.06,'build':-.06,'welfare':.06},desc='Use increased consumption to restore confidence while slowing capital formation.')
mex('cabinet_austerity','cabinet_consumption')
n('cabinet_training','Train the Next Administrators',0,5,'cabinet_austerity,cabinet_consumption',{'research':.04,'education':.05},money=1,desc='Make professional administrative training a durable cabinet priority.')
n('cabinet_settlement','A Governable Plan',0,6,'cabinet_training',{'prod':.04,'bureau':.03},desc='Consolidate a plan that the ministries can finance and administer.')

group('kpa','Military Emergency Government',54,17,22,'Counterfactual military government','A KPA government is an emergency alternative, not historical Songun in 1970. Officers do not inherit all WPK programme bonuses.')
n('kpa_council','The Emergency Council',0,0,mods={'org':.06,'pp':.05,'stab':-.05,'personnel':.06},cost=3,desc='Place the officer corps at the centre of an emergency administration.')
n('kpa_party','Retain Party Commissars',-3,1,'kpa_council',{'stab':.06,'org':.04,'research':-.04},desc='Keep party control inside the forces to stabilize an uneasy military government.')
n('kpa_professional','A Professional Officer Corps',3,1,'kpa_council',{'org':.08,'planning':.06,'stab':-.04,'personnel':.08},desc='Reduce party interference in command while accepting a political legitimacy problem.')
mex('kpa_party','kpa_professional')
n('kpa_loyalty','Rebuild the Command Compact',-3,2,'kpa_party',{'influence_def':.08,'bureau':.04},desc='Rebuild a compact between commanders and the ruling party apparatus.')
n('kpa_merit','Promotion by Competence',3,2,'kpa_professional',{'armyxp':.08,'education':.04},money=1,desc='Select officers for technical and operational competence.')
n('kpa_rations','Guarantee Military Supply',0,3,'kpa_loyalty,kpa_merit',{'supply':-.06,'agri':-.05,'equipment':.05},desc='Secure military supply while diverting productive inputs from civilian provision.')
n('kpa_fortress','An Entrenched Garrison',-3,4,'kpa_rations',{'defence':.10,'prod':-.06,'personnel':.06},desc='Accept a long military administration and its continuing civilian burden.')
n('kpa_handover','A Civilian Handover Charter',3,4,'kpa_rations',{'trade':.10,'stab':.05,'pp':-.06},desc='Commit to an orderly civilian transition without installing a party by focus reward.',extra=[action('Handover commitment','Opens a political commitment through existing government change rules. A later government change disables this KPA programme.')])
mex('kpa_fortress','kpa_handover')
n('kpa_budget','A Costed Defence Budget',0,5,'kpa_fortress,kpa_handover',{'equipment':-.04,'bureau':.03},desc='Bring defence procurement under a budget that the treasury can sustain.')
n('kpa_legacy','The Army and the Republic',0,6,'kpa_budget',{'org':.04,'personnel':.03},desc='Settle the role of the armed forces in the chosen political order.')

group('yanan',"Yan'an Reform Communist Programme",70,17,2,'Explicit exile-return counterfactual','The purged faction has no domestic organization in 1970. Only an actual government change in the existing outlook system opens this programme; no purged leader is revived.')
n('yanan_return','A Socialist Reassessment',0,0,mods={'research':.05,'stab':-.06},cost=3,desc='Begin a counterfactual reassessment of party rule after a fundamental political change.')
n('yanan_councils','Factory Councils',-3,1,'yanan_return',{'prod':.08,'pp':-.05,'bureau':.04},desc='Give workers and technical staff a stronger voice in plant decisions.')
n('yanan_discipline','A Reformed Party Discipline',3,1,'yanan_return',{'effgain':.08,'pp':.06,'research':-.03},desc='Retain centralized party command while ending the personal cult.')
mex('yanan_councils','yanan_discipline')
n('yanan_rehabilitation','Review Political Sentences',0,2,'yanan_councils,yanan_discipline',{'research':.04,'influence_def':-.04,'bureau':.04},desc='Review sentences and recover professional talent without bringing back the dead.')
n('yanan_experts','Welcome Foreign Experts',-3,3,'yanan_rehabilitation',{'research':.07,'prod':.06,'influence_def':-.10},money=2,desc='Accept technical assistance and the influence that accompanies it.')
n('yanan_domestic','Rebuild Domestic Expertise',3,3,'yanan_rehabilitation',{'research':.04,'prod':.04,'education':.08},money=2,desc='Develop expertise at home with slower returns and higher education expenditure.')
mex('yanan_experts','yanan_domestic')
n('yanan_socialism','A Korean Reform Socialism',0,4,'yanan_experts,yanan_domestic',{'agri':.05,'welfare':.04},desc='Combine socialist institutions with a less punitive economic programme.')
n('yanan_guarantees','Guarantees against a New Cult',0,5,'yanan_socialism',{'prod':.04,'pp':-.04},desc='Limit arbitrary appointments and personal command inside the party state.')

group('union','Industrial Labour Programme',86,17,3,'Counterfactual government of a WPK mass organization','GFTUK is a state-directed federation, not an independent opposition party in the historical start.')
n('union_compact','A Workers’ Governing Compact',0,0,mods={'stab':.05,'welfare':.04},cost=3,desc='Base a counterfactual government on wages, rations, safety and industrial representation.')
n('union_wages','Wages and Household Supply',-3,1,'union_compact',{'prod':.06,'welfare':.10,'corptax':-.04},desc='Give workers a larger share of output at a higher social cost.')
n('union_reinvestment','Workers’ Investment Funds',3,1,'union_compact',{'civ':.10,'stab':-.04,'bureau':.06},desc='Direct retained earnings toward new investment instead of current consumption.')
mex('union_wages','union_reinvestment')
n('union_safety','Industrial Safety Committees',0,2,'union_wages,union_reinvestment',{'prod':.04,'output':-.03,'bureau':.04},money=1,desc='Allow inspections to slow unsafe production rather than pursuing quotas at any cost.')
n('union_bargaining','Negotiated Production Norms',-3,3,'union_safety',{'prod':.06,'pp':-.05},desc='Negotiate achievable work norms with factory representatives.')
n('union_mobilization','A New Chollima Compact',3,3,'union_safety',{'output':.08,'prod':-.04,'welfare':.05},desc='Link accelerated output to material provision while keeping the strain of mass mobilization.',icon='chollima_speed')
mex('union_bargaining','union_mobilization')
n('union_training','Paid Technical Training',0,4,'union_bargaining,union_mobilization',{'research':.04,'education':.06},money=1,desc='Train skilled workers during paid time away from production.')
n('union_representation','Permanent Worker Representation',0,5,'union_training',{'stab':.04,'bureau':.04},desc='Give industrial representation an enduring place in the governing institutions.')

group('christian','Christian Federation Programme',102,17,14,'Counterfactual civic and religious settlement','KCF is a supervised remnant under Kang Ryang-uk, not a mass Christian party waiting freely to contest power. No automatic conversion of the country.')
n('christian_citizenship','Citizenship and Conscience',0,0,mods={'stab':.05,'pp':-.04},cost=3,desc='Protect freedom of conscience through a counterfactual civic settlement.')
n('christian_welfare','Public Social Provision',-3,1,'christian_citizenship',{'prod':.05,'health':.08,'welfare':.06},money=1,desc='Build publicly funded welfare services with room for religious participation.')
n('christian_community','Community Associations',3,1,'christian_citizenship',{'bureau':-.06,'stab':.05,'prod':-.02},money=1,desc='Use local associations to provide services with less uniform coverage.')
mex('christian_welfare','christian_community')
n('christian_education','Schools for a Common Citizenship',0,2,'christian_welfare,christian_community',{'research':.05,'education':.07},money=1,desc='Provide education that protects civic equality across beliefs.')
n('christian_tolerance','A Plural Civic Compact',-3,3,'christian_education',{'research':.05,'pp':-.05},desc='Bind the government to equal citizenship for believers and non-believers.')
n('christian_moral','A Christian Social Charter',3,3,'christian_education',{'stab':.08,'research':-.04,'police':.03},desc='Make Christian social teaching a stronger public norm while retaining civil protections.')
mex('christian_tolerance','christian_moral')
n('christian_relations','Family and Religious Contacts',0,4,'christian_tolerance,christian_moral',{'trade':.08,'police':.04},money=1,desc='Support permitted family and religious contacts across the division of Korea.')
n('christian_republic','A Commonwealth of Citizens',0,5,'christian_relations',{'prod':.04,'welfare':.04},desc='Consolidate a civic order without granting any faith ownership of the state.')

START_SPIRITS = [
 dict(key='monolithic_start',title='The Monolithic Ideological System',slot=4,
      mods={'pp':.10,'stab':.06,'research':-.05,'bureau':.08},
      description='The purges have secured the Leader’s command while suppressing independent reporting and technical disagreement.',
      remedy='Replaced, not stacked, by Monolithic Leadership or Collective Deliberation. Party-bound and inactive outside WPK rule.'),
 dict(key='byungjin_start',title='Byungjin: Economy and Defence',slot=None,
      mods={'defence':.08,'milbuild':.08,'civ':-.10,'personnel':.10},
      description='The parallel build-up strengthens deterrence while defence absorbs labour, capital and public expenditure.',
      remedy='Army reorganization reduces this to a residual +4% core defence / -4% civilian construction burden; final national arsenal/civilian conversion choice replaces the residual.'),
 dict(key='plan_overstretch',title='The Extended Seven-Year Plan',slot=None,
      mods={'prod':-.12,'effgain':-.10,'bureau':.08},
      description='A developed industrial base is constrained by missed targets, weak input balances and repeated plan extensions.',
      remedy='Balance the Inputs removes this spirit after one substantive industrial priority and a funded project.'),
 dict(key='power_bottleneck',title='Power and Imported Inputs',slot=None,
      mods={'output':-.08,'energy':.08,'fuel':.06},
      description='Power shortages and imported machinery and fuel limit the use of installed industrial capacity.',
      remedy='Repair the Power Grid removes the electricity/output component. Residual imported-input fuel burden remains until external resilience.'),
 dict(key='ration_strain',title='An Uneven Civilian Supply',slot=None,
      mods={'agri':-.08,'stab':-.04,'welfare':.06},
      description='Civilian supply competes with heavy industry and defence; rural inputs and urban distribution remain uneven.',
      remedy='A Sustainable Ration removes this after both irrigation/fertilizer and county clinics. This is not the 1990s famine.'),
 dict(key='juche_start',title='Juche and the Two Patrons',slot=None,
      mods={'influence_def':.12,'trade':-.08,'research':-.03},
      description='Political autonomy is defended through cautious access to foreign technology and competition between external patrons.',
      remedy='Keep Both Doors Open replaces it with strategic autonomy: +6% influence defence / -3% trade deal opinion; signed external cooperation offsets selected technical disadvantages.'),
]

# IMPERIA CW — Cold War: independent concept-audit corrections and native labels.
STATS['armyfuel'] = ('army_fuel_consumption_factor', 'Army fuel consumption')
STATS['fuel'] = ('non_electric_fuel_consumption_modifier', 'Population non-electric fuel demand')
STATS['interest'] = ('interest_rate_multiplier_modifier', 'Annual interest rate, percentage points')
STATS['trade'] = ('trade_opinion_factor', 'Trade opinion factor')
_mobile = next(v for v in NODES if v['key'] == 'mobile_army')
_mobile['modifiers']['army_fuel_consumption_factor'] = _mobile['modifiers'].pop('non_electric_fuel_consumption_modifier')
_mobile['labels'].pop('non_electric_fuel_consumption_modifier')
_mobile['labels']['army_fuel_consumption_factor'] = 'Army fuel consumption'
_credit = next(v for v in NODES if v['key'] == 'credit_reckoning')
_credit['money'] = 0
_credit['description'] = 'Resolve the machinery account through repayment or a negotiated rescheduling.'
# Complete review-level transactions and prerequisites. These are data, not installed helpers.
_bykey = {v['key']:v for v in NODES}
_bykey['western_credit']['extra'][0]['amount'] = 7.5
_bykey['western_credit']['modifiers']['interest_rate_multiplier_modifier'] = 1.25
_bykey['credit_reckoning']['extra'][0]['amount'] = 7.5
_bykey['domestic_finance']['modifiers']['interest_rate_multiplier_modifier'] = -.35
_bykey['cabinet_currency']['modifiers']['interest_rate_multiplier_modifier'] = -.25
_bykey['kdp_budget']['modifiers']['interest_rate_multiplier_modifier'] = -.25
_prices = {'arms_factory':7.5, 'industrial_complex':7.5,'agriculture_district':3.75,
           'fossil_powerplant':3.25,'renewable_energy_infra':8.5,'infrastructure':3.5,'radar_station':1.75,'dockyard':7.5}
_states = {'steelworks':[602,601], 'food_district':[603,602], 'coal_power':[602,601],
           'hydro_power':[1201,1199], 'rail_corridor':[602,1200,601], 'air_warning':[601,1200],
           'naval_workshops':[601,1199,602], 'western_credit':[602,1200], 'chondo_reclamation':[603,1200]}
for _v in NODES:
    _v['runtime_guards'] = ['original_tag = NKO', 'IMP_is_1970_scenario = yes']
    if _v['slot'] is not None:
        _v['runtime_guards'].append('check_variable = { ruling_party = '+str(_v['slot'])+' }')
    for _a in _v['extra']:
        if _a['kind']=='building':
            _a['state_ids'] = _states[_v['key']]
            _a['state_selection'] = 'First owned AND controlled candidate with genuine free capacity; coastal for dockyards; below per-type level cap.'
            _a['full_project_cost'] = _prices[_a['type']]
            _a['pricing'] = 'Full one-time focus-funded project price; no second native purchase fee.'
            if _v['key']!='western_credit':_v['money'] = _prices[_a['type']]
        if _a['kind']=='offer':
            _a['acceptance_guards'] = ['Sender and recipient exist, are independent, and are at peace with each other.',
               'Offer is pending and not already signed; still-valid government and project guards.',
               'Same receipt stored on both parties; charge and reward exactly once on acceptance; expire after 90 days.']
            _a['expire_days']=90
_signed_guards = {'soviet_training':('SOV','moscow_signed'),'border_trade':('CHI','beijing_signed'),
                  'red_cross':('KOR','channel_signed'),'confederation_offer':('KOR','channel_signed'),
                  'safeguards':('SOV','atomic_cooperation'),'npt_offer':('SOV','atomic_cooperation')}
for _key,(_tag,_flag) in _signed_guards.items():
    _bykey[_key]['runtime_guards'] += ['has_country_flag = '+P+_flag,
        _tag+' = { exists = yes has_country_flag = '+P+_flag+' }']
_bykey['presidency']['runtime_guards'].append('OR = { date > 1972.12.26 has_country_flag = COLDWAR_NKO_early_constitution }')
_bykey['ten_principles']['runtime_guards'].append('OR = { date > 1974.1.1 has_country_flag = COLDWAR_NKO_early_principles }')
_bykey['three_revolutions']['runtime_guards'].append('date > 1973.1.1')
_bykey['red_banner']['runtime_guards'].append('date > 1975.10.1')
for _key in ('family_succession','committee_succession'):_bykey[_key]['runtime_guards'].append('date > 1974.1.1')
_bykey['sixth_congress']['runtime_guards'].append('date > 1980.10.9')
_bykey['joint_ventures']['runtime_guards'].append('OR = { date > 1984.9.7 has_country_flag = COLDWAR_NKO_early_venture_law }')
_bykey['npt_offer']['runtime_guards'] += ['OR = { date > 1985.12.11 has_country_flag = COLDWAR_NKO_early_npt_negotiation }','has_country_flag = COLDWAR_NKO_safeguards_valid']
_bykey['safeguards']['extra'][0]['signed_flag'] = P+'safeguards_valid'
_bykey['fuel_studies']['runtime_guards'].append('COLDWAR_nuc_economy_allows = yes')
_bykey['strategic_option']['runtime_guards'].append('COLDWAR_nuc_economy_allows = yes')
_offer = _bykey['moscow_offer']['extra'][0]
_offer['cost']=7.5
_offer['benefit']='NKO receives 1 civilian factory in an eligible owned and controlled industrial state; SOV receives $7.500 billion. No payout on refusal.'
_offer['outcomes']=[dict(recipient='NKO',kind='building',type='industrial_complex',levels=1,state_ids=[602,1200]),dict(recipient='SOV',kind='treasury',amount=7.5)]
_bykey['beijing_offer']['extra'][0]['outcomes']=[dict(recipient='NKO',kind='timed_modifier',days=730,modifiers={'agricolture_productivity_modifier':.05,'research_speed_factor':.02}),dict(recipient='CHI',kind='treasury',amount=1)]
_bykey['detente']['extra'][0]['outcomes']=[dict(recipient='BOTH',kind='stability',amount=.03),dict(recipient='BOTH',kind='timed_modifier',days=365,modifiers={'trade_opinion_factor':.10}),dict(recipient='KOR',kind='treasury',amount=1)]
_bykey['confederation_offer']['extra'][0]['outcomes']=[dict(recipient='BOTH',kind='conditional_modifier',requires_both_receipts=P+'council_signed',modifiers={'trade_opinion_factor':.10,'bureaucracy_cost_multiplier_modifier':.03}),dict(recipient='KOR',kind='treasury',amount=2)]
_bykey['confederation_offer']['extra'][0]['benefit']='KOR receives $2.000 billion. Both countries receive trade opinion +10% and weekly administration expenditure +3% while the council agreement is valid; no annexation or forced alliance.'
_bykey['civil_atom']['extra'][0]['outcomes']=[dict(recipient='NKO',kind='research',category='CAT_nuclear_reactors',bonus=.5,uses=1),dict(recipient='SOV',kind='treasury',amount=3)]
_bykey['npt_offer']['extra'][0]['outcomes']=[dict(recipient='NKO',kind='conditional_modifier',requires_both_receipts=P+'npt_bargain',requires_flag=P+'safeguards_valid',modifiers={'nuclear_energy_generation_modifier':.08}),dict(recipient='SOV',kind='treasury',amount=2)]
_bykey['army_reorganization']['extra'].append(action('Replace Byungjin burden','Replace the starting Byungjin spirit with core defence +4% and civilian factory construction -4%.'))
for _key in ('civilian_conversions','arsenal_priority'):_bykey[_key]['remove'].append('byungjin_residual')
_bykey['power_grid']['extra'].append(action('Imported-input residual','Replace the power bottleneck spirit with population non-electric fuel demand +6%; remove this residual at Patron Resilience.'))
_bykey['external_resilience']['remove'].append('imported_input_residual')
_bykey['external_balance']['extra'].append(action('Strategic autonomy settlement','Replace Juche and the Two Patrons with foreign influence defence +6% and trade opinion -3%.'))

# Specific native art avoids modern politicians/equipment and the modern Russian flag.
_icons = {'monolithic':'juche3','collective':'NKO_party_reform','loyalty':'WPRG','debate':'parliament_box',
 'ten_principles':'juche','cadre_tenure':'education_reform','party_settlement':'WPRG','campaigns':'chollima_speed',
 'technical_cadres':'NKO_workers','three_revolutions':'chollima_speed','engineer_commissions':'economic_civil_industry',
 'red_banner':'WPRG','honest_targets':'NKO_anti_corruption','plan_discipline':'economic_civil_industry',
 'party_media':'NKO_theatre','secretariat':'parliament_box','succession_rules':'NKO_party_reform','continuity':'juche3',
 'moscow_offer':'align_to_soviet_union','diaspora_trade':'trade_with_japan','coal_power':'coal_mining',
 'hydro_power':'NKO_self_power','air_defence':'jet_mig21','mass_artillery':'artillery','special_operations':'focus_generic_secret_service_agency'}
for _key,_icon in _icons.items():_bykey[_key]['icon']=_icon
_bykey['christian_republic']['title']='Civic Commonwealth'
_icons_more = {'light_priority':'NKO_food','balanced_priority':'NKO_workers','food_district':'agriculture',
 'machine_tools':'NKO_worker','input_balance':'NKO_rebuild','hydro_power':'hydroelectric',
 'power_grid':'power_plant','housing':'NKO_buildings','fertilizer':'agriculture','public_health':'NKO_healthcare',
 'living_standards':'NKO_food','state_procurement':'agriculture','household_plots':'NKO_food',
 'distribution_reform':'NKO_new_routes','domestic_finance':'money','western_credit':'trade_with_europe',
 'technical_schools':'education_reform','credit_reckoning':'money','export_quality':'NKO_worker',
 'joint_ventures':'trade_with_japan','staff_college':'education_reform','army_reorganization':'army_reform',
 'ammunition_standards':'artillery','air_warning':'jet_mig21','naval_workshops':'NKO_submarine',
 'reconnaissance':'focus_generic_secret_service_agency','joint_logistics':'NKO_new_routes',
 'civilian_conversions':'economic_civil_industry','arsenal_priority':'dprk_army',
 'military_research':'education_reform','soviet_training':'education_reform','border_trade':'trade_with_china',
 'export_offices':'trade','external_balance':'NKO_no_sactions','red_cross':'DPRK-ROK_shake_flags',
 'recognition':'goal_generic_positive_trade_relations','civilian_export':'trade',
 'security_export':'focus_generic_arms_trade','external_resilience':'NKO_new_routes',
 'science':'socialist_science','reactor_training':'education_reform','safeguards':'parliament_box',
 'fuel_studies':'socialist_science','kdp_budget':'money','kdp_courts':'parliament_box',
 'kdp_housing':'NKO_buildings','kdp_licenses':'economic_civil_industry','kdp_civic':'NKO_workers',
 'kdp_service':'education_reform','kdp_reconciliation':'DPRK-ROK_shake_flags',
 'chondo_schools':'education_reform','chondo_tolerance':'parliament_box',
 'cabinet_statistics':'education_reform','cabinet_training':'education_reform','cabinet_currency':'money',
 'kpa_merit':'education_reform','kpa_budget':'money','yanan_experts':'education_reform',
 'union_safety':'NKO_workers','union_training':'education_reform','christian_education':'education_reform'}
for _key,_icon in _icons_more.items():_bykey[_key]['icon']=_icon
for _key in ('distribution_reform','joint_logistics','external_resilience'):_bykey[_key]['icon']='focus_generic_supply_line'
_bykey['western_credit']['icon']='trade'
# Fuel-cycle studies grant a concrete existing-category bonus, not a fictional unlock.
_bykey['fuel_studies']['extra']=[tech('CAT_nuclear_reactors',.5)]
_bykey['fuel_studies']['description']='Develop fuel-cycle engineering through a funded national research programme.'
_descriptions = {
 'steelworks':'Refit the established steel and engineering complexes that support national industrialization.',
 'food_district':'Equip the cooperatives with machinery and storage, and stabilize the delivery of rural inputs.',
 'coal_power':'Expand coal-fired generating capacity to sustain the industrial plan.',
 'hydro_power':'Invest in inland water power to reduce dependence on imported fossil fuels.',
 'air_defence':'Improve coordination of fighter aviation, warning services and ground-based air defence.',
 'air_warning':'Extend early warning and communications coverage across the northern approaches.',
 'naval_workshops':'Expand the coastal yards to maintain the fleet and sustain a modest naval-industrial base.',
 'front_broadcasting':'Strengthen the united front’s radio services and political messaging toward the South.',
 'confederation_offer':'Propose a confederal consultative council based on continued sovereignty and negotiated cooperation.',
 'recognition':'Build diplomatic representation among non-aligned states and seek wider recognition of the Republic.',
 'civilian_export':'Offer commercial concessions to establish dependable markets for civilian exports.',
 'security_export':'Develop bilateral military training and advisory missions with willing partners.',
 'reactor_training':'Train engineers in research-reactor operation, radiation science and laboratory practice.',
 'civil_atom':'Seek foreign technical cooperation under verifiable limits on the atomic programme.',
 'strategic_option':'Direct the Academy and defence establishment to study the strategic applications of nuclear research.',
 'kpa_handover':'Commit the emergency council to an orderly transition under an agreed civilian charter.',
 'yanan_rehabilitation':'Review political sentences and restore surviving specialists to professional life.'}
for _key,_description in _descriptions.items():_bykey[_key]['description']=_description
for _key in ('presidency','family_succession','committee_succession'):
    _bykey[_key]['runtime_guards'].append('has_country_leader = { name = "Kim Il Sung" ruling_only = yes }')
for _key in ('family_succession','party_media','sixth_congress'):
    _bykey[_key]['policy_enable_guards']=['OR = { has_country_leader = { name = "Kim Il Sung" ruling_only = yes } has_country_leader = { name = "Kim Jong Il" ruling_only = yes } }']
for _v in NODES:_v['charge_contract']='One-time full focus cost through treasury_change / modify_treasury_effect after reward/state guards; no duplicate investment-helper fee; normal weekly automatic borrowing handles a deficit.'
for _s in START_SPIRITS:
    _s['id']=P+_s['key']
    _s['remedy']=_s['remedy'].replace('trade deal opinion','trade opinion')
INCIDENTS = [
 dict(id=P+'machinery_account',name='The Machinery Account',trigger='730 days after the recorded machinery loan, if its recorded principal remains outstanding.',
      choices=[dict(name='Settle the account',treasury='-min(7.5, recorded outstanding principal, total debt)',debt='Same principal reduction as the cash debit; one transaction. Normal native borrowing may cover the cash payment.'),
               dict(name='Negotiate a rescheduling',treasury=-2,days=730,modifiers={'interest_rate_multiplier_modifier':1.0,'trade_opinion_factor':-.10},debt='Principal remains; no debt write-off.'),
               dict(name='Suspend repayments',treasury=0,days=730,modifiers={'interest_rate_multiplier_modifier':2.0,'trade_opinion_factor':-.15,'stability_factor':-.03},debt='Principal remains; normal interest and credit consequences continue.')],
      note='Only a country that chose the loan can receive this crisis. No automatic historical default in January 1970. Meet the Foreign Bills resolves this account by one chosen response, not necessarily full repayment.'),
 dict(id=P+'patron_disruption',name='External Support Disrupted',trigger='A real signed supply/support agreement ceases or its provider changes terms; no forced behavior by SOV or CHI and no automatic calendar punishment.',
      days=365,modifiers={'industrial_capacity_factory':-.08,'research_speed_factor':-.03},
      mitigation='A signed replacement procurement agreement, or a $2.000 billion spare-parts programme. Patron Resilience halves this temporary penalty.',
      note='New NKO event adapter around actual accepted/cancelled cooperation. It models late-Cold-War vulnerability without moving the 1990s famine into 1970.')]

for _v in NODES:
    for _stat in ('fuel', 'interest', 'trade'):
        if STATS[_stat][0] in _v['labels']:
            _v['labels'][STATS[_stat][0]] = STATS[_stat][1]
    _v['long_title'] = _v['title']
_short = OUT / 'short_titles.json'
if _short.exists():
    for _key, _title in json.loads(_short.read_text(encoding='utf-8-sig')).items():
        next(v for v in NODES if v['key'] == _key)['title'] = _title

# IMPERIA CW — Cold War: native-width choice fans; semantic content unchanged.
_roots={'wpk':(6,0),'economy':(16,0),'defence':(30,0),'diplomacy':(44,0),'atomic':(54,0),
        'kdp':(4,17),'chondo':(12,17),'cabinet':(20,17),'kpa':(28,17),
        'yanan':(36,17),'union':(44,17),'christian':(52,17)}
for _g in GROUPS:_g['x'],_g['y']=_roots[_g['id']]
for _v in NODES:
    _dx=_v['dx']
    if _v['group']=='wpk':_dx={-4:-2,4:2}.get(_dx,_dx)
    elif _v['group']=='economy':_dx={-6:-4,6:4,-4:-2,4:2}.get(_dx,_dx)
    elif _v['group']=='defence':_dx={-4:-2,4:2}.get(_dx,_dx)
    elif _v['group']=='diplomacy':_dx={-6:-4,6:4,-4:-2,4:2}.get(_dx,_dx)
    elif _v['group']=='atomic':_dx={-3:-2,3:2}.get(_dx,_dx)
    else:_dx={-3:-2,3:2}.get(_dx,_dx)
    _v['dx']=_dx
    _v['x']=_roots[_v['group']][0]+_dx
    _v['y']=_roots[_v['group']][1]+_v['dy']

def validate():
    ids={v['id']:v for v in NODES}
    errors=[]
    if len(ids)!=len(NODES):errors.append('Duplicate focus ID')
    for v in NODES:
        if not v['id'].startswith(P):errors.append('Missing COLDWAR namespace '+v['id'])
        for g in v['prerequisites']:
            for p in g:
                if p not in ids: errors.append('Missing prerequisite '+p)
                elif ids[p]['y']>=v['y']: errors.append('Backward edge '+p+' -> '+v['id'])
        for p in v['mutex']:
            if v['id'] not in ids[p]['mutex']: errors.append('Asymmetric exclusion '+p)
    for i,a in enumerate(NODES):
        for b in NODES[i+1:]:
            if abs(a['x']-b['x'])*96<165 and abs(a['y']-b['y'])*130<128:
                errors.append('Full card overlap '+a['id']+' / '+b['id'])
    # Branch reachability: carry minimal valid histories, preserving AND blocks / OR members.
    cache={}
    def histories(key):
        if key in cache:return cache[key]
        v=ids[key]; valid=[frozenset()]
        for g in v['prerequisites']:
            options=[s for p in g for s in histories(p)]
            merged=[]
            for a in valid:
                for b in options:
                    s=a|b
                    if not any(set(ids[k]['mutex'])&s for k in s):merged.append(s)
            valid=list(set(merged))
        valid=[s|{key} for s in valid if not set(v['mutex'])&s]
        cache[key]=valid
        return valid
    for v in NODES:
        if not histories(v['id']):errors.append('Unreachable choice history '+v['id'])
    unseen=set(ids);choice_groups=0
    while unseen:
        key=unseen.pop()
        if not ids[key]['mutex']:continue
        choice_groups+=1;pending=list(ids[key]['mutex'])
        while pending:
            nxt=pending.pop()
            if nxt not in unseen:continue
            unseen.remove(nxt);pending.extend(ids[nxt]['mutex'])
    report=dict(nodes=len(NODES),groups=dict(Counter(v['group'] for v in NODES)),choice_groups=choice_groups,
      exclusions=sum(len(v['mutex']) for v in NODES)//2,edges=sum(sum(map(len,v['prerequisites'])) for v in NODES),
      bounds=[min(v['x'] for v in NODES),max(v['x'] for v in NODES),min(v['y'] for v in NODES),max(v['y'] for v in NODES)],
      checks=['IDs and prerequisite targets','reciprocal exclusions','acyclic forward edges','AND/OR choice-history reachability','165x128 full-card rectangle overlap at 96x130 grid'],
      errors=errors,engine_tested=False)
    (OUT/'structural_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    assert not errors,errors
    assert len(NODES)<=250
    return report

if __name__=='__main__':
    report=validate()
    data=dict(namespace=P,status='CONCEPT — APPROVAL REQUIRED; not installed',groups=GROUPS,nodes=NODES,
              starting_spirits=START_SPIRITS,incidents=INCIDENTS,stats=STATS,validation=report)
    (OUT/'COLDWAR_NKO_1970_design.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(report,indent=2))
