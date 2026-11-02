# IMPERIA COLD WAR — France revision 5; design data only, never loaded by HOI4.
"""Build a separately reviewable proposal without changing approved input/runtime."""
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OUT = Path('C:/Users/Enes/.codex/visualizations/2026/10/23/01a16840-34d5-7e60-8c3d-134a5e042a6a/coldwar_france_politics')
approved_bytes = (BASE/'approved_design.json').read_bytes()
A = json.loads(approved_bytes)
catalog = json.loads((HERE/'mechanics_catalog.json').read_text(encoding='utf-8'))
labels = copy.deepcopy(A['labels'])
labels.update({
    'repair_speed_factor':['Building Repair Speed','%',1],
    'repair_speed_infrastructure_factor':['Infrastructure Repair Speed','%',1],
    'land_reinforce_rate':['Reinforce Rate','pp',1],
    'land_doctrine_cost_factor':['Land Doctrine Cost','%',-1],
    'air_doctrine_cost_factor':['Air Doctrine Cost','%',-1],
    'naval_doctrine_cost_factor':['Naval Doctrine Cost','%',-1],
    'enemy_operative_detection_chance_factor':['Enemy Operative Detection Chance','%',1],
    'trade_opinion_factor':['Trade Deal Opinion Factor','%',1],
    'local_resources_factor':['Resource Extraction','%',1],
    'country_productivity_growth_modifier':['Productivity Growth Multiplier','%',1],
    'civilian_factories_productivity':['Civilian Factory Productivity','%',1],
    'energy_use_modifier_civs':['Civilian Industry Electricity Use','%',-1],
    'energy_use_modifier_mils':['Military Industry Electricity Use','%',-1],
    'pop_energy_use_multiplier':['Population Electricity Use','%',-1],
    'production_speed_agriculture_district_factor':['Agricultural District Construction','%',1],
    'imp_sanction_resistance':['Sanction Resistance','%',1],
    'imp_investment_in_extra':['Incoming Investment Capacity','number',1],
    'mdcw_cw_assistance_effectiveness':['Assistance Programme Effectiveness','%',1],
    'air_fuel_consumption_factor':['Air Force Fuel Consumption','%',-1],
    'airforce_personnel_cost_multiplier_modifier':['Air Force Personnel Expenditure','%',-1],
    'navy_personnel_cost_multiplier_modifier':['Navy Personnel Expenditure','%',-1],
    'air_training_xp_gain_factor':['Air Wing Training Experience Gain','%',1],
    'air_accidents_factor':['Air Accident Chance','%',-1],
    'naval_accidents_chance':['Naval Accident Chance','%',-1],
    'line_change_production_efficiency_factor':['Production Efficiency Retention','%',1],
    'foreign_influence_defense_modifier':['Foreign Influence Defence','%',1],
})
nodes=[]
for n in A['nodes']:
    if n['domain']=='foreign':
        continue
    keys=['id','key','group','title','description','history','xy','parents','exclusive','days','pp','mods','once','one_time_effects','transitions','domain','party_gate','requirements','condition','icon']
    item={k:copy.deepcopy(n[k]) for k in keys if k in n}
    item['revision']='retained'
    item['mods']={k:v for k,v in item['mods'].items() if v != 0}
    nodes.append(item)
by={n['key']:n for n in nodes}
groups=[{k:copy.deepcopy(g[k]) for k in ['id','entry','base','slots','history','context']} for g in A['groups']]
names={
 'institutions':'Republican Institutions','gaullist':'UDR / Gaullists','orthodox_gaullist':'Orthodox Gaullists',
 'liberal':'Independent Republicans','centre':'Democratic Centre','radical':'Radical Party',
 'socialist':'Socialist Party','communist':'French Communist Party','old_guard':'Communist Old Guard',
 'psu':'Unified Socialist Party','ecology':'Ecologist Movement','cid':'CID / Independent Traders','national':'National Front',
}
for g in groups:g['title']=names[g['id']]
registry=json.loads((BASE.parents[1]/'tools/party_registry_1970/data/FRA.json').read_text(encoding='utf-8'))
native_triggers={1:'western_conservatism_are_in_power',2:'western_liberals_are_in_power',3:'western_social_democrats_are_in_power',4:'emerging_communist_state_are_in_power',6:'emerging_reactionaries_are_in_power',7:'emerging_autocracy_are_in_power',14:'neutrality_neutral_conservatism_are_in_power',16:'neutrality_neutral_libertarians_are_in_power',17:'neutrality_neutral_green_are_in_power',18:'neutrality_neutral_social_are_in_power',20:'nationalist_right_wing_populists_are_in_power'}
for g in groups:
    if g['id']=='institutions':g['party_name']='Any governing party';continue
    slot=g['slots'][0]
    g['party_name']='National Front' if g['id']=='national' else registry['slots'][str(slot)][0]['english']
    g['native_party_trigger']=native_triggers[slot]

# Equipment bonuses belong to removable ideas, not irreversible add_equipment_bonus.
# One symbolic family expands into explicitly checked DLC-specific archetypes.
equipment={
 'infantry':{'label':'Infantry Weapons Production Cost','targets':{'all':['infantry_weapons_type']},'reference':'MD common/ideas/05_france.txt:1335'},
 'signals':{'label':'Command Equipment Production Cost','targets':{'all':['cnc_equipment_type']},'reference':'MD common/ideas/05_france.txt:1340'},
 'utility':{'label':'Utility Vehicle Production Cost','targets':{'all':['util_vehicle_type','heavy_util_vehicle_type']},'reference':'MD common/ideas/German.txt:581; 05_france.txt:145'},
 'tank':{'label':'Main Battle Tank Production Cost','targets':{'all':['medium_tank_chassis']},'reference':'MD common/ideas/05_france.txt:1366; legacy MBT_2 uses same archetype'},
 'aircraft':{'label':'Fighter Airframe Production Cost','targets':{'By Blood Alone':['small_plane_airframe'],'without By Blood Alone':['medium_plane_fighter_airframe']},'reference':'MD common/ideas/05_france.txt:1480; MD_x_plane_airframes.txt:332'},
 'multirole':{'label':'Multirole Airframe Production Cost','targets':{'By Blood Alone':['medium_plane_airframe'],'without By Blood Alone':['medium_plane_airframe']},'reference':'MD gen_4_medium enables medium_plane_airframe_2; MR_Fighter2 archetype at MD_x_plane_airframes.txt:1344'},
 'train':{'label':'Train Production Cost','targets':{'all':['train_equipment']},'reference':'MD common/ideas/German.txt:581'},
}

def change(key, mods, *, title=None, text=None, equip=None, award=None):
    n=by[key]
    n['mods']=mods
    n['revision']='reworked'
    # A revised transaction has its own complete awards; do not retain old receipts.
    n['once']=[]; n['one_time_effects']=[]
    if title:n['title']=title
    if text:n['description']=text
    if equip:n['equipment']=equip
    if award:n['awards']=award
    return n

def doctrine(branch,bonus=.5):
    return {'kind':'doctrine','branch':branch,'bonus':bonus,'uses':1}

def xp(kind,amount):return {'kind':kind+'_experience','amount':amount}

# Distinct economic institutions. Values are balance proposals, not historical estimates.
economic = [
 ('social_gaullism', {'civilian_factories_productivity':.05,'country_productivity_growth_modifier':.10,'social_cost_multiplier_modifier':.08,'industrial_capacity_factory':-.03}, 'Negotiated Modernisation', 'Modernise with negotiated investment and employment guarantees. Civilian productivity benefits from continuity and retraining, while wage and social commitments narrow the room for arms output.'),
 ('competitive_gaullism', {'production_speed_offices_factor':.10,'imp_investment_in_extra':1,'corporate_tax_income_multiplier_modifier':-.08,'foreign_influence_defense_modifier':-.05}, 'Competitive Modernisation', 'Open more investment channels and give firms room to compete abroad. Tax concessions and exposure to foreign capital accompany the larger commercial programme.'),
 ('planned_supply_allocation', {'local_resources_factor':.10,'imp_sanction_resistance':.08,'civilian_factories_productivity':-.04}, 'Strategic Supply Allocation', 'Reserve extraction, stocks and contracts for strategically important production. The arrangement improves resilience under sanctions but ties civilian firms to administrative allocation.'),
 ('independent_supplier_compacts', {'civilian_factories_productivity':.06,'imp_investment_in_extra':1,'corporate_tax_income_multiplier_modifier':-.06}, 'Independent Supplier Compacts', 'Support a wider supplier base with investment access and procurement credit. More adaptable firms require continuing tax concessions rather than compulsory allocations.'),
 ('monetary_discipline', {'interest_rate_multiplier_modifier':-.5,'imp_investment_in_extra':1,'country_productivity_growth_modifier':-.08}, 'Monetary Discipline', 'Defend financial credibility and investment access by holding demand below the pace sought by industry. Borrowing becomes easier to sustain, while productivity catch-up slows.'),
 ('support_activity', {'country_productivity_growth_modifier':.15,'civilian_factories_productivity':.04,'tax_gain_multiplier_modifier':-.06,'interest_rate_multiplier_modifier':.25}, 'Support Industrial Activity', 'Keep industrial orders and technical investment moving through a weak market. Tax relief and public borrowing support activity at the cost of a less comfortable debt position.'),
 ('family_solidarity', {'country_productivity_growth_modifier':.10,'stability_factor':.04,'health_cost_multiplier_modifier':.08,'social_cost_multiplier_modifier':.05}, 'Family and Social Investment', 'Put family services and access to healthcare behind the social market. A healthier and more secure workforce brings long-term gains with a lasting expenditure commitment.'),
 ('fiscal_compact', {'interest_rate_multiplier_modifier':-.4,'tax_gain_multiplier_modifier':.04,'social_cost_multiplier_modifier':-.04,'stability_factor':-.035}, 'A Credible Fiscal Compact', 'Protect the public balance sheet and recover revenue with a tighter spending settlement. Credit improves, but households and local representatives bear the adjustment.'),
 ('public_research_contracts', {'country_productivity_growth_modifier':.12,'education_cost_multiplier_modifier':.08,'production_speed_arms_factory_factor':-.05}, 'Public Engineering Institutes', 'Fund public laboratories and engineering schools with a stable research mandate. The technical workforce benefits, while military construction competes with a stronger civilian claim on investment.'),
 ('small_firm_innovation_guarantee', {'imp_investment_in_extra':1,'civilian_factories_productivity':.05,'corporate_tax_income_multiplier_modifier':-.06}, 'Small-Firm Innovation Guarantees', 'Use credit guarantees to carry independent firms through development and production. A dispersed innovation network requires tax concessions and accepts uneven results.'),
 ('redistributive_mandate', {'civilian_factories_productivity':.08,'social_cost_multiplier_modifier':.10,'corporate_tax_income_multiplier_modifier':.04,'interest_rate_multiplier_modifier':.35}, 'Redistribution and Public Demand', 'Use public demand and redistribution to sustain industrial activity. Higher social expenditure and borrowing pressure make the settlement vulnerable to a difficult external balance.'),
 ('stabilisation_turn', {'interest_rate_multiplier_modifier':-.75,'tax_gain_multiplier_modifier':.05,'country_productivity_growth_modifier':-.08,'stability_factor':-.04}, 'The Stabilisation Settlement', 'Restore room to finance the state through tax recovery and a stricter demand settlement. The programme accepts a slower productivity transition and political opposition to restraint.'),
 ('state_enterprise_command', {'industrial_capacity_factory':.08,'local_resources_factor':.08,'country_productivity_growth_modifier':-.08,'energy_use_modifier_mils':.08}, 'A Unified Public Industry Plan', 'Guarantee large orders and direct inputs through a single public plan. Sustained series benefit from central allocation, but energy use and slower adaptation are real burdens.'),
 ('municipal_industrial_compacts', {'civilian_factories_productivity':.06,'repair_speed_factor':.15,'social_cost_multiplier_modifier':.06,'industrial_capacity_factory':-.03}, 'Municipal Industrial Compacts', 'Give public firms and municipalities room to renew workshops and local services together. Repair and civilian output improve while national arms orders lose priority.'),
 ('central_plan', {'civilian_factories_productivity':.08,'local_resources_factor':.10,'country_productivity_growth_modifier':-.10}, 'Civilian Planning Priority', 'Direct the plan toward civilian production and domestic inputs. The protected allocation sustains output, while its rigid targets slow technical adaptation.'),
 ('industrial_mobilisation', {'industrial_capacity_factory':.10,'production_speed_arms_factory_factor':.10,'energy_use_modifier_mils':.10,'production_speed_industrial_complex_factor':-.10}, 'Industrial Mobilisation Priority', 'Concentrate investment and energy on arms production. New capacity becomes easier to sustain, at the expense of civilian construction and electricity demand.'),
 ('workers_councils', {'country_productivity_growth_modifier':.12,'civilian_factories_productivity':.05,'industrial_capacity_factory':-.05}, 'Workers’ Councils', 'Let work collectives decide how to use technical skills and reinvestment. Adaptation and civilian output gain room, but centrally scheduled military orders become harder to coordinate.'),
 ('contractual_socialism', {'imp_investment_in_extra':1,'repair_speed_factor':.15,'social_cost_multiplier_modifier':.06}, 'Contractual Self-Management', 'Bind public credit, local authorities and independent enterprises through negotiated contracts. Investment and repair gain continuity alongside continuing social guarantees.'),
 ('ecological_conversion', {'energy_use_modifier_civs':-.10,'repair_speed_infrastructure_factor':.15,'industrial_capacity_factory':-.05}, 'Industrial Energy Conversion', 'Reduce industrial electricity waste and give infrastructure renewal priority. Conversion diverts engineering time from military production.'),
 ('local_sufficiency', {'production_speed_agriculture_district_factor':.15,'pop_energy_use_multiplier':-.05,'country_productivity_growth_modifier':-.10}, 'Local Sufficiency', 'Put rural services and lower household energy demand ahead of rapid industrial expansion. Local provision improves while the productivity catch-up programme becomes more modest.'),
 ('fiscal_concessions', {'production_speed_offices_factor':.15,'corporate_tax_income_multiplier_modifier':-.08,'social_cost_multiplier_modifier':.04}, 'Relief for Independent Traders', 'Reduce the burdens on independent businesses and help workshops and shops invest. The revenue loss makes promised social protection more expensive to maintain.'),
 ('simplified_administration', {'bureaucracy_cost_multiplier_modifier':-.10,'imp_investment_in_extra':1,'tax_gain_multiplier_modifier':-.04}, 'A Simpler Business Administration', 'Replace overlapping procedures with a simpler credit and licensing system. Lower administration costs and wider access come with fewer opportunities to recover revenue.'),
 ('tax_revolt', {'production_speed_offices_factor':.12,'trade_opinion_factor':.15,'corporate_tax_income_multiplier_modifier':-.08,'foreign_influence_defense_modifier':-.05}, 'Independent Enterprise Contracts', 'Favor commercial contracts and small-business investment. Tax concessions and external business ties leave the programme less insulated from foreign pressure.'),
 ('national_preference', {'imp_sanction_resistance':.10,'civilian_factories_productivity':.05,'corporate_tax_income_multiplier_modifier':-.06,'trade_opinion_factor':-.10}, 'Protected National Industry', 'Protect domestic supply and support French-controlled production. Subsidies and discriminatory procurement weaken commercial access and reduce the tax return from the protected sector.'),
]
for key,mods,title,text in economic:change(key,mods,title=title,text=text)

# Personnel choices: twelve distinct institutional tensions, not universal attack buffs.
personnel={
 'gaullist':[
 ('gaullist_national_readiness','Mechanised Conscription',{'land_reinforce_rate':.01,'land_doctrine_cost_factor':-.10,'supply_consumption_factor':.05},[xp('army',25)],'Maintain an army of trained conscripts and mechanised formations for a major European emergency. Reinforcement and doctrine gain priority, with a larger supply requirement.'),
 ('gaullist_reserve_modernisation','A Mobile Intervention Cadre',{'training_time_army_factor':-.10,'army_org_regain':.08,'army_personnel_cost_multiplier_modifier':.12},[xp('air',20)],'Keep a specialist cadre ready for limited operations beyond the main European front. Faster preparation and recovery require sustained professional pay and specialist training.')],
 'orthodox_gaullist':[
 ('orthodox_force_de_dissuasion','Undersea and Command Continuity',{'naval_doctrine_cost_factor':-.15,'industrial_capacity_dockyard':.06,'production_speed_arms_factory_factor':-.07},[doctrine('naval')],'Protect the independent deterrent’s industrial base and naval command skills. Shipyard priority constrains new land-armament investment; it grants no warheads or strategic authority.'),
 ('orthodox_combined_arms_training','Conventional Freedom of Action',{'supply_consumption_factor':-.08,'land_reinforce_rate':.01,'army_personnel_cost_multiplier_modifier':.10},[doctrine('land')],'Give France the trained conventional forces and sustainment capacity needed below the nuclear threshold. Greater freedom to act brings an enduring personnel commitment.')],
 'liberal':[
 ('liberal_professional_readiness','Professional Sustainment Corps',{'supply_consumption_factor':-.10,'training_time_army_factor':-.08,'army_personnel_cost_multiplier_modifier':.10},[xp('army',20)],'Invest in maintenance specialists and logistical training instead of a larger nominal establishment. The force consumes fewer supplies but has a higher professional payroll.'),
 ('liberal_citizen_reserve','A Technical Citizen Reserve',{'land_reinforce_rate':.015,'army_personnel_cost_multiplier_modifier':-.06,'training_time_army_factor':.08},[doctrine('land')],'Preserve a technically trained reserve on a restrained standing-force budget. Reinforcement depth and lower pay costs require longer initial training and dependable civilian employers.')],
 'centre':[
 ('centre_civil_defence_service','Territorial Engineer Service',{'repair_speed_infrastructure_factor':.20,'supply_consumption_factor':-.06,'army_personnel_cost_multiplier_modifier':.06},[xp('army',20)],'Train military engineers and reserve services to keep roads, depots and civil protection working. Useful territorial skills require a regular service and equipment budget.'),
 ('centre_joint_service_readiness','Maritime and Joint-Service Readiness',{'naval_doctrine_cost_factor':-.12,'army_org_regain':.06,'production_speed_arms_factory_factor':-.05},[xp('navy',25)],'Make escort, communications and joint staff practice the first call on technical training. Naval coordination competes with rapid expansion of the land procurement base.')],
 'radical':[
 ('territorial_citizen_reserve','A Republican Territorial Reserve',{'land_reinforce_rate':.0125,'army_core_defence_factor':.05,'training_time_army_factor':.10},[xp('army',20)],'Tie reserve service to territorial units and civilian oversight. A prepared home defence gains depth at the cost of slower training cycles for the standing force.'),
 ('technical_defence_cadre','Technical Defence Establishments',{'supply_consumption_factor':-.08,'land_doctrine_cost_factor':-.12,'education_cost_multiplier_modifier':.07},[doctrine('land')],'Maintain a smaller technical establishment through engineering education and applied trials. Better doctrine and sustainment depend on continuing public education expenditure.')],
 'socialist':[
 ('socialist_citizen_reserve','Six-Month Service and Regional Reserves',{'land_reinforce_rate':.015,'army_personnel_cost_multiplier_modifier':-.08,'training_time_army_factor':.10},[xp('army',20)],'Develop the Common Programme’s shorter service and trained regional reserves as a governing alternative. A lighter standing payroll buys mobilisation depth while specialist preparation takes longer.'),
 ('socialist_professional_cadre','A Rapid Action Force',{'army_org_regain':.10,'supply_consumption_factor':-.07,'army_personnel_cost_multiplier_modifier':.12},[xp('army',30)],'Prioritise a trained rapid-action cadre while retaining civilian authority over deployments. Readiness and sustainment improve, but professional personnel make a lasting claim on the social budget.')],
 'communist':[
 ('communist_workers_defence','Regional Popular Defence',{'army_core_defence_factor':.07,'land_reinforce_rate':.01,'training_time_army_factor':.10},[doctrine('land')],'Translate the Common Programme’s trained regional reserves into a defensive military institution. Territorial defence improves while longer preparation limits immediate expeditionary readiness.'),
 ('communist_party_command','Public General Staff and Technical Schools',{'land_doctrine_cost_factor':-.15,'supply_consumption_factor':-.07,'education_cost_multiplier_modifier':.08},[xp('army',25)],'Fund the staff and technical schools needed to operate a modern public armaments sector. This is a governing extrapolation, with specialist education rather than foreign command at its centre.')],
 'old_guard':[
 ('old_guard_conscript_reserve','Mass Territorial Establishments',{'land_reinforce_rate':.02,'army_personnel_cost_multiplier_modifier':-.06,'training_time_army_factor':.15},[xp('army',20)],'Maintain a large trained territorial reserve with a restrained professional establishment. Depth depends on longer training and a less immediately available force.'),
 ('old_guard_professional_staff','Central Technical Staff',{'land_doctrine_cost_factor':-.15,'army_org_regain':.08,'army_personnel_cost_multiplier_modifier':.10},[doctrine('land')],'Concentrate scarce specialists in a central staff and maintenance corps. This counterfactual hard-line programme buys readiness through sustained professional expenditure.')],
 'psu':[
 ('psu_civilian_control_force','A Civilian-Controlled Technical Force',{'supply_consumption_factor':-.08,'enemy_operative_detection_chance_factor':.10,'army_personnel_cost_multiplier_modifier':.10},[xp('army',20)],'Retain a small technical force under parliamentary authority, with accountable counter-infiltration and supply services. A professional core costs more than a civic reserve.'),
 ('psu_citizen_defence','Popular Defence and Civil Service',{'repair_speed_infrastructure_factor':.20,'army_core_defence_factor':.06,'industrial_capacity_factory':-.04},[doctrine('land')],'Explore the PSU’s later popular-defence current through reserve engineering and civil service. Civilian resilience and territorial preparation take priority over central arms throughput.')],
 'ecology':[
 ('civil_protection_network','A Territorial Rescue Service',{'repair_speed_factor':.20,'repair_speed_infrastructure_factor':.15,'army_personnel_cost_multiplier_modifier':.06},[xp('army',15)],'Build rescue, engineering and emergency logistics around existing civil-protection services. Repair capacity has a continuing personnel cost; it creates neither troops nor an automatic foreign deployment.'),
 ('protective_professional_force','A Small Protective Force',{'supply_consumption_factor':-.10,'army_core_defence_factor':.06,'army_personnel_cost_multiplier_modifier':.10},[doctrine('land')],'Preserve a professional defensive force rather than converting every military workshop to civilian service. Efficient territorial defence requires a larger standing payroll.')],
 'cid':[
 ('territorial_readiness_compact','A Lean Standing Establishment',{'army_personnel_cost_multiplier_modifier':-.10,'equipment_cost_multiplier_modifier':-.06,'land_reinforce_rate':-.005},[doctrine('land')],'Restrain the regular establishment and extend the life of existing equipment. Lower weekly costs leave fewer trained replacements immediately available.'),
 ('local_defence_contracts','Employer-Supported Reservists',{'land_reinforce_rate':.015,'repair_speed_infrastructure_factor':.12,'corporate_tax_income_multiplier_modifier':-.05},[xp('army',25)],'Pay independent employers to retain trained reservists and emergency workshops. Mobilisation and repair improve through a tax concession that reduces public revenue.')],
 'national':[
 ('national_service_reserve','Territorial National Service',{'army_core_defence_factor':.08,'land_reinforce_rate':.01,'training_time_army_factor':.10},[xp('army',25)],'Prioritise national service and territorial mobilisation. This is an alternate governing programme: it strengthens home defence but takes longer to train than a specialist standing force.'),
 ('professional_expedition_cadre','A Professional Intervention Establishment',{'army_org_regain':.10,'supply_consumption_factor':-.08,'army_personnel_cost_multiplier_modifier':.15},[doctrine('land')],'Fund a professional force able to act beyond territorial defence. It offers readiness without automatic intervention, alongside a substantial recurring payroll.')],
}
for group,entries in personnel.items():
    for key,title,mods,award,text in entries:change(key,mods,title=title,text=text,award=award)

# Each armaments allocation is an exclusive two-step chain. Foreign roots continue
# these investments, so an industrial decision changes available partnership terms.
arms={
 'gaullist':[
 ('National Arsenal Series',{'industrial_capacity_factory':.06,'equipment_cost_multiplier_modifier':.05},{'tank':-.08},'Long Production Runs',{'production_factory_max_efficiency_factor':.08,'production_factory_efficiency_gain_factor':-.05},{'tank':-.04}),
 ('European Airframe Workshare',{'air_doctrine_cost_factor':-.08,'education_cost_multiplier_modifier':.06},{'aircraft':-.08},'Shared Components and Tooling',{'civilian_factories_productivity':.04,'foreign_influence_defense_modifier':-.05},{'aircraft':-.04})],
 'orthodox_gaullist':[
 ('Protected Naval Arsenals',{'industrial_capacity_dockyard':.08,'production_speed_arms_factory_factor':-.06},None,'Undersea Design Continuity',{'naval_doctrine_cost_factor':-.10,'education_cost_multiplier_modifier':.06},None),
 ('Sovereign Land Procurement',{'industrial_capacity_factory':.06,'equipment_cost_multiplier_modifier':.06},{'tank':-.08},'National Signals and Mobility',{'supply_consumption_factor':-.06,'energy_use_modifier_mils':.05},{'signals':-.08})],
 'liberal':[
 ('Competitive Aircraft Contracts',{'corporate_tax_income_multiplier_modifier':-.05,'production_factory_max_efficiency_factor':.05},{'aircraft':-.10},'Export Certification and Avionics',{'air_doctrine_cost_factor':-.10,'education_cost_multiplier_modifier':.05},None),
 ('Repair Before Replacement',{'equipment_cost_multiplier_modifier':-.10,'industrial_capacity_factory':-.04},None,'Common Maintenance Fleets',{'supply_consumption_factor':-.06,'production_factory_max_efficiency_factor':-.04},{'utility':-.10})],
 'centre':[
 ('Regional Land-Supplier Compact',{'production_speed_arms_factory_factor':.08,'corporate_tax_income_multiplier_modifier':-.05},{'utility':-.08},'Common Depot Standards',{'supply_consumption_factor':-.07,'education_cost_multiplier_modifier':.04},{'signals':-.05}),
 ('Escort and Shipyard Procurement',{'industrial_capacity_dockyard':.08,'industrial_capacity_factory':-.04},None,'Fleet Training and Refit',{'naval_doctrine_cost_factor':-.10,'education_cost_multiplier_modifier':.05},None)],
 'radical':[
 ('Open Engineering Trials',{'country_productivity_growth_modifier':.08,'education_cost_multiplier_modifier':.07},None,'Independent Test Establishments',{'land_doctrine_cost_factor':-.10,'production_speed_arms_factory_factor':-.04},{'signals':-.08}),
 ('A Territorial Procurement Budget',{'equipment_cost_multiplier_modifier':-.08,'production_speed_arms_factory_factor':-.05},{'infantry':-.08},'Repair and Regional Tooling',{'repair_speed_infrastructure_factor':.15,'corporate_tax_income_multiplier_modifier':-.04},{'utility':-.06})],
 'socialist':[
 ('Public Aerospace Investment',{'air_doctrine_cost_factor':-.08,'education_cost_multiplier_modifier':.07},{'aircraft':-.08},'Protected Technical Employment',{'country_productivity_growth_modifier':.08,'social_cost_multiplier_modifier':.07},None),
 ('Armaments Conversion Guarantees',{'civilian_factories_productivity':.05,'industrial_capacity_factory':-.05},None,'A Smaller Sustained Fleet',{'equipment_cost_multiplier_modifier':-.10,'education_cost_multiplier_modifier':.05},{'utility':-.08})],
 'communist':[
 ('National Armaments Plan',{'industrial_capacity_factory':.08,'energy_use_modifier_mils':.08},{'infantry':-.08},'Standardised Production Series',{'production_factory_max_efficiency_factor':.08,'production_factory_efficiency_gain_factor':-.06},{'signals':-.06}),
 ('Autonomous Arsenal Councils',{'repair_speed_factor':.15,'production_factory_max_efficiency_factor':-.04},{'utility':-.06},'Regional Prototype Workshops',{'country_productivity_growth_modifier':.10,'education_cost_multiplier_modifier':.07},None)],
 'old_guard':[
 ('Central Armaments Directorate',{'industrial_capacity_factory':.10,'civilian_factories_productivity':-.05},{'infantry':-.10},'Mobilisation Production Schedules',{'production_factory_max_efficiency_factor':.10,'production_factory_efficiency_gain_factor':-.08},None),
 ('Domestic Repair Establishments',{'equipment_cost_multiplier_modifier':-.12,'production_speed_arms_factory_factor':-.06},None,'National Transport Tooling',{'supply_consumption_factor':-.06,'energy_use_modifier_mils':.04},{'utility':-.10})],
 'psu':[
 ('Worker-Managed Arsenal Suppliers',{'production_factory_efficiency_gain_factor':.10,'production_factory_max_efficiency_factor':-.05},{'infantry':-.06},'Cooperative Maintenance Networks',{'equipment_cost_multiplier_modifier':-.08,'social_cost_multiplier_modifier':.05},None),
 ('Dual-Use Industrial Conversion',{'civilian_factories_productivity':.06,'industrial_capacity_factory':-.06},None,'Civilian Technical Institutes',{'country_productivity_growth_modifier':.12,'education_cost_multiplier_modifier':.07},None)],
 'ecology':[
 ('Civilian Workshop Conversion',{'repair_speed_factor':.15,'industrial_capacity_factory':-.05},{'utility':-.08},'Civil-Protection Instrumentation',{'energy_use_modifier_civs':-.06,'education_cost_multiplier_modifier':.05},{'signals':-.05}),
 ('Retained Defence Workshops',{'equipment_cost_multiplier_modifier':-.08,'production_speed_arms_factory_factor':-.05},{'infantry':-.06},'Service-Life Engineering',{'supply_consumption_factor':-.06,'production_factory_max_efficiency_factor':-.03},{'utility':-.06})],
 'cid':[
 ('Independent Repair Contracts',{'equipment_cost_multiplier_modifier':-.10,'corporate_tax_income_multiplier_modifier':-.04},None,'Workshop Tooling Credit',{'repair_speed_infrastructure_factor':.15,'production_factory_max_efficiency_factor':-.03},{'utility':-.08}),
 ('Small-Supplier Workshare',{'production_speed_arms_factory_factor':.06,'corporate_tax_income_multiplier_modifier':-.05},{'infantry':-.08},'Interchangeable Local Components',{'supply_consumption_factor':-.06,'education_cost_multiplier_modifier':.04},{'signals':-.06})],
 'national':[
 ('National Sourcing Requirement',{'imp_sanction_resistance':.08,'equipment_cost_multiplier_modifier':.06},{'tank':-.08},'Protected Domestic Assembly',{'production_factory_max_efficiency_factor':.07,'trade_opinion_factor':-.10},{'infantry':-.06}),
 ('Intergovernmental Production Standards',{'foreign_influence_defense_modifier':-.06,'education_cost_multiplier_modifier':.05},{'signals':-.08},'Coordinated Vehicle Tooling',{'supply_consumption_factor':-.06,'corporate_tax_income_multiplier_modifier':-.04},{'utility':-.08})],
}
for group,options in arms.items():
    for letter,pack in zip('ab',options):
        title,mods,equip,follow,fmods,fequip=pack
        change(f'armament_{group}_{letter}',mods,title=title,equip=equip)
        change(f'armament_{group}_{letter}_followup',fmods,title=follow,equip=fequip)

# Named-country proposals. These are hypothetical negotiated terms inspired by
# documented institutions/deals; no historical contract is silently enacted.
def terms(mods=None, equip=None, funds=50, pp=20, awards=None):
    return {'mods':mods or {},'equipment':equip or {},'treasury_millions':-funds,'political_power':-pp,'awards':awards or []}

# Six non-stacking families allow several enduring partnerships without accumulating
# duplicate versions of one programme across government changes.
offers=[]
def offer(group,side,tag,title,family,mods,*,equip=None,fr=None,pt=None,basis='',sources=None):
    tag={'YUG':'SER','NOR':'NRY','NETH':'HOL'}.get(tag,tag)
    key=f'v5_{group}_{tag.lower()}_{len(offers)+1:02d}'
    t=terms(mods,equip)
    item={'id':'COLDWAR_FRA_'+key,'key':key,'group':group,'side':side,'partner':tag,'title':title,'family':family,'france':fr or copy.deepcopy(t),'partner_terms':pt or copy.deepcopy(t),'historical_basis':basis,'sources':sources or [],'status':'Proposed RP agreement; historical precedent is not automatic enactment'}
    offers.append(item)

offer('gaullist','a','GRE','Greek Mirage Maintenance Convention','military_industry',{'equipment_cost_multiplier_modifier':-.04,'education_cost_multiplier_modifier':.025},equip={'aircraft':-.04},basis='Greece ordered Mirage F1 aircraft in 1974. The continuing reciprocal training and production spirit is a proposed extension.',sources=['dassault_greece'])
offer('gaullist','a','ROM','Romanian Vehicle-Licensing Protocol','civil_industry',{'civilian_factories_productivity':.025,'corporate_tax_income_multiplier_modifier':-.025},equip={'utility':-.04},basis='Renault–Dacia licensing contract in 1966; local assembly from 1968. Military utility tooling is an explicit dual-use extrapolation.',sources=['dacia_1966'])
offer('gaullist','b','GER','German Airframe Workshare','military_industry',{'education_cost_multiplier_modifier':.03},equip={'aircraft':-.05},basis='Airbus 1970 and the Franco-German Alpha Jet programme; shared production has workshare and training costs.',sources=['airbus_1970','alpha_jet'])
offer('gaullist','b','ENG','British Aircraft Integration Programme','training',{'air_doctrine_cost_factor':-.075,'education_cost_multiplier_modifier':.03},basis='Anglo-French aerospace cooperation, including Concorde and Jaguar, provides the industrial precedent. The reciprocal training institution is proposed.',sources=['jaguar'])
offer('gaullist','shared','SOV','Soviet Civil-Space Instrumentation Mission','science_energy',{'country_productivity_growth_modifier':.04,'education_cost_multiplier_modifier':.03,'foreign_influence_defense_modifier':-.025},basis='The 1966 peaceful-space agreement and later joint missions support civilian instrumentation exchanges. No strategic weapons technology is shared.',sources=['cnes_1966'])

offer('orthodox_gaullist','a','SOV','Soviet Civil-Science Consultation','science_energy',{'country_productivity_growth_modifier':.04,'education_cost_multiplier_modifier':.03,'foreign_influence_defense_modifier':-.025},basis='The 1970 consultation protocol and 1975 cooperation declaration support civilian scientific contact alongside independent French defence.',sources=['fr_ussr_1975'])
offer('orthodox_gaullist','a','ENG','British Naval Staff Consultation','training',{'naval_doctrine_cost_factor':-.08,'education_cost_multiplier_modifier':.03},basis='An alternate bilateral naval-staff institution: both states retain separate strategic forces and release authority. No actual joint deterrent is claimed.',sources=['S07','S08'])
offer('orthodox_gaullist','b','GER','German Conventional Crisis Protocol','training',{'land_reinforce_rate':.005,'education_cost_multiplier_modifier':.03},basis='Franco-German defence consultation and later exercises provide precedent. Earlier or deeper adoption is a negotiated RP alternative.',sources=['S09'])
offer('orthodox_gaullist','b','GRE','Greek Sovereign-Supplier Agreement','military_industry',{'equipment_cost_multiplier_modifier':-.04,'corporate_tax_income_multiplier_modifier':-.025},equip={'aircraft':-.04},basis='Greek Mirage purchases support an independent-supplier relationship; no guarantee or transfer of aircraft is imposed.',sources=['dassault_greece'])
offer('orthodox_gaullist','shared','USA','American Alliance Deconfliction Channel','training',{'land_doctrine_cost_factor':-.05,'foreign_influence_defense_modifier':-.04,'education_cost_multiplier_modifier':.02},basis='Ailleret–Lemnitzer and later cooperation allowed alliance coordination without integrated command. The bounded continuing programme is proposed.',sources=['nato_france'])

offer('liberal','a','GER','German Avionics Supplier Compact','military_industry',{'education_cost_multiplier_modifier':.025,'foreign_influence_defense_modifier':-.025},equip={'aircraft':-.05,'signals':-.04},basis='Alpha Jet and civil aerospace workshare support a supplier and avionics compact.',sources=['alpha_jet','airbus_1970'])
offer('liberal','a','ENG','British Export-Certification Accord','commerce',{'trade_opinion_factor':.10,'corporate_tax_income_multiplier_modifier':-.025},equip={'aircraft':-.03},basis='Jaguar and civil-aerospace cooperation provide precedent for reciprocal certification and export coordination.',sources=['jaguar'])
offer('liberal','b','USA','American Computing Standards Exchange','science_energy',{'country_productivity_growth_modifier':.04,'education_cost_multiplier_modifier':.03,'foreign_influence_defense_modifier':-.03},basis='Rambouillet-era economic consultation and computing-industry links are an inspiration; this agreement is a proposed continuing civilian channel.',sources=['S12'])
offer('liberal','b','NETH','Dutch Investment-Clearance Accord','commerce',{'imp_investment_in_extra':1,'corporate_tax_income_multiplier_modifier':-.03},basis='Common Market investment links provide the setting. This bilateral clearance agreement is a counterfactual fiscal alternative, not the automatic EMS or a new EU institution.',sources=['S11'])

offer('centre','a','BEL','Belgian Depot and Border-Service Compact','civil_resilience',{'supply_consumption_factor':-.04,'repair_speed_infrastructure_factor':.08,'education_cost_multiplier_modifier':.03},basis='Neighbouring EEC institutions and cross-border cooperation provide a setting; reciprocal depot and emergency procedures are a proposed bilateral programme.',sources=['madrid_1980'])
offer('centre','a','GER','German Officer-Education Protocol','training',{'land_doctrine_cost_factor':-.08,'education_cost_multiplier_modifier':.03},basis='Franco-German military consultation and officer education developed during the period; no army integration or nuclear delegation is enacted.',sources=['S09'])
offer('centre','b','ITA','Italian Mediterranean Escort Courses','training',{'naval_doctrine_cost_factor':-.08,'education_cost_multiplier_modifier':.03},basis='A proposed conventional training programme consistent with Lecanuet’s European defence stance; no specific 1970 bilateral treaty or war guarantee is claimed.',sources=['S13','S14'])
offer('centre','b','ENG','British Maritime Workshop Standards','military_industry',{'industrial_capacity_dockyard':.04,'production_speed_arms_factory_factor':-.025},basis='Industrial and maritime cooperation is a plausible European procurement option; the numeric naval compact is counterfactual.',sources=['S14'])

offer('radical','a','BEL','Belgian Public Engineering Exchange','civil_resilience',{'repair_speed_factor':.10,'production_speed_infrastructure_factor':.05,'education_cost_multiplier_modifier':.03},basis='Cross-border local-authority cooperation is an institutional precedent; the public-engineering exchange is proposed.',sources=['madrid_1980'])
offer('radical','a','SWI','Swiss Applied Instrumentation Network','science_energy',{'energy_use_modifier_civs':-.04,'country_productivity_growth_modifier':.03,'education_cost_multiplier_modifier':.03},basis='A proposed reciprocal instrumentation and public-research network; not a documented Radical government treaty.',sources=['S17'])
offer('radical','b','ITA','Italian Territorial Engineering Courses','training',{'supply_consumption_factor':-.04,'education_cost_multiplier_modifier':.03},equip={'utility':-.04},basis='A hypothetical engineering and reserve-transport compact, grounded in regional-service reform priorities rather than a claimed joint defence platform.',sources=['S17'])
offer('radical','b','SPR','Spanish Regional Works Exchange','civil_resilience',{'production_speed_infrastructure_factor':.08,'repair_speed_infrastructure_factor':.08,'education_cost_multiplier_modifier':.035},basis='Madrid’s 1980 framework offers a later precedent for regional cooperation. An earlier bilateral technical agreement is an RP alternative; it does not require or grant EEC membership.',sources=['madrid_1980'])

offer('socialist','a','GER','German Conventional Staff and Airframe Compact','military_industry',{'education_cost_multiplier_modifier':.03,'foreign_influence_defense_modifier':-.025},equip={'aircraft':-.05},basis='Airbus and later Franco-German defence cooperation support conventional workshare under separate national command.',sources=['airbus_1970','S09'])
offer('socialist','a','ENG','British Rapid-Response Staff Courses','training',{'supply_consumption_factor':-.04,'army_org_regain':.04,'army_personnel_cost_multiplier_modifier':.03},basis='A proposed staff programme consistent with a PS rapid-action establishment. No foreign troops, access rights or intervention are created.',sources=['far_1983'])
offer('socialist','b','ALG','Algerian Energy and Industrial Co-Development','science_energy',{},fr=terms({'energy_use_modifier_civs':-.04,'civilian_factories_productivity':.02,'corporate_tax_income_multiplier_modifier':-.035},funds=75),pt=terms({'civilian_factories_productivity':.04,'country_productivity_growth_modifier':.04,'education_cost_multiplier_modifier':.04},funds=50),basis='The 1982 gas agreement and co-development debate exposed a real tradeoff between supply, industrial orders and French public costs. The proposed spirit models efficiency and skills, not free gas or an automatic resource trade.',sources=['algeria_1982','gas_budget_1983'])
offer('socialist','b','YUG','Yugoslav Civil Engineering Programme','civil_industry',{'civilian_factories_productivity':.03,'country_productivity_growth_modifier':.03,'education_cost_multiplier_modifier':.035},basis='The 1966 France–Yugoslavia scientific and technical treaty supports reciprocal applied research; industrial-conversion terms are proposed.',sources=['fr_yugoslavia_1966'])

offer('communist','a','SOV','Soviet Public-Industry Standards Mission','civil_industry',{'production_factory_max_efficiency_factor':.04,'production_factory_efficiency_gain_factor':-.025,'education_cost_multiplier_modifier':.02},basis='Civilian industrial and scientific exchange is documented in the 1975 declaration. No Pact accession or military command transfer occurs.',sources=['fr_ussr_1975'])
offer('communist','a','DDR','East German Machine-Tool and Signals Mission','military_industry',{'equipment_cost_multiplier_modifier':-.04,'education_cost_multiplier_modifier':.03},equip={'signals':-.05},basis='The 1973 industrial and technical agreement supports machine-tool exchanges. Military signals tooling is an explicitly counterfactual dual-use extension.',sources=['fr_gdr_1973'])
offer('communist','b','ITA','Italian Public-Enterprise Repair Network','civil_resilience',{'repair_speed_factor':.12,'social_cost_multiplier_modifier':.025},equip={'train':-.04},basis='A proposed public-enterprise exchange inspired by Eurocommunist dialogue. The Italian government’s ideology is not assumed and its player decides.',sources=['pcf_1976'])
offer('communist','b','ALG','Algerian Survey and Agricultural Schools','civil_industry',{'production_speed_agriculture_district_factor':.08,'repair_speed_infrastructure_factor':.08,'education_cost_multiplier_modifier':.03},basis='1968 cartographic cooperation and agricultural training agreements provide concrete civilian precedents.',sources=['fr_algeria_1968','fr_algeria_agri'])

offer('old_guard','a','SOV','Soviet Staff and Maintenance Mission','training',{'land_doctrine_cost_factor':-.08,'education_cost_multiplier_modifier':.035,'foreign_influence_defense_modifier':-.04},basis='Military staff cooperation is a hard-line governing counterfactual, not an effect established by the real civilian Franco-Soviet treaty.',sources=['fr_ussr_1975'])
offer('old_guard','a','DDR','East German Standard-Series Workshops','military_industry',{'production_factory_max_efficiency_factor':.04,'production_factory_efficiency_gain_factor':-.025,'education_cost_multiplier_modifier':.02},equip={'infantry':-.04},basis='Real 1973 industrial cooperation is the civilian precedent; common military series are a negotiated alternate-history extension.',sources=['fr_gdr_1973'])
offer('old_guard','b','ROM','Romanian Licensed-Vehicle Workshops','civil_industry',{'civilian_factories_productivity':.025,'corporate_tax_income_multiplier_modifier':-.025},equip={'utility':-.04},basis='The Renault–Dacia arrangement is a documented state-industry precedent. Extending it under a French hard-line government remains counterfactual.',sources=['dacia_1966'])
offer('old_guard','b','YUG','Yugoslav Independent Technical Channel','science_energy',{'country_productivity_growth_modifier':.04,'education_cost_multiplier_modifier':.035},basis='A real 1966 technical treaty supports an autonomous civilian channel. Cooperation with Yugoslav institutions is deliberately distinct from copying Soviet military standards.',sources=['fr_yugoslavia_1966'])

offer('psu','a','YUG','Yugoslav Cooperative Workshop Exchange','civil_industry',{'production_factory_efficiency_gain_factor':.05,'production_factory_max_efficiency_factor':-.025,'social_cost_multiplier_modifier':.02},basis='Yugoslav self-management and the bilateral science treaty provide institutional precedents; successful transplantation is not presumed.',sources=['yugoslavia_constitution_1974','fr_yugoslavia_1966'])
offer('psu','a','ALG','Algerian Technical-School Partnership','civil_resilience',{'production_speed_agriculture_district_factor':.08,'repair_speed_infrastructure_factor':.08,'education_cost_multiplier_modifier':.03},basis='Agricultural education and cartographic cooperation support practical civilian capacity-building.',sources=['fr_algeria_agri','fr_algeria_1968'])
offer('psu','b','SWI','Swiss Civil-Service Rescue Protocol','civil_resilience',{'repair_speed_factor':.12,'army_personnel_cost_multiplier_modifier':.025},equip={'utility':-.03},basis='The 1987 mutual disaster-assistance agreement is a later precedent. A PSU-led earlier version is a counterfactual civic-service arrangement.',sources=['swiss_rescue_1987'])
offer('psu','b','GER','German Civilian Instrumentation Programme','science_energy',{'energy_use_modifier_civs':-.05,'education_cost_multiplier_modifier':.035},basis='Cross-border industrial science and water monitoring provide a civilian precedent. This does not force the PSU to accept a common armaments policy.',sources=['rhine'])

offer('ecology','a','GER','German Rhine Monitoring Convention','science_energy',{'energy_use_modifier_civs':-.04,'production_speed_infrastructure_factor':.06,'education_cost_multiplier_modifier':.035},basis='The Rhine commission dates to 1950; the 1976 pollution conventions provide a concrete environmental negotiation and monitoring precedent.',sources=['rhine'])
offer('ecology','a','SWI','Swiss Alpine Disaster-Assistance Protocol','civil_resilience',{'repair_speed_infrastructure_factor':.15,'army_personnel_cost_multiplier_modifier':.03},equip={'utility':-.03},basis='The bilateral disaster-assistance agreement was signed in 1987. An earlier programme is proposed; repair bonuses are a game abstraction, not a pollution or rescue simulation.',sources=['swiss_rescue_1987'])
offer('ecology','b','ENG','British Channel Pollution-Response Compact','civil_resilience',{'repair_speed_factor':.12,'education_cost_multiplier_modifier':.03},equip={'utility':-.03},basis='The 1969 Bonn Agreement provided surveillance, research, exercises and requested mutual assistance against marine pollution.',sources=['bonn_1969'])
offer('ecology','b','NOR','Norwegian Industrial Safety Exchange','science_energy',{'energy_use_modifier_civs':-.05,'education_cost_multiplier_modifier':.035},basis='Norway was a Bonn Agreement signatory; the 1977 Ekofisk incident illustrates the shared safety problem. The bilateral efficiency programme is a proposed extension.',sources=['bonn_1969'])

offer('cid','a','BEL','Belgian Independent-Workshop Credit Accord','commerce',{'imp_investment_in_extra':1,'corporate_tax_income_multiplier_modifier':-.03},basis='CID sought an independent commerce and craft bank in 1970. Exporting that model through a Belgian credit arrangement is a governing extrapolation, not a documented CID foreign policy.',sources=['cid_1970'])
offer('cid','a','SWI','Swiss Repair and Apprenticeship Accord','civil_resilience',{'equipment_cost_multiplier_modifier':-.04,'education_cost_multiplier_modifier':.025},equip={'utility':-.04},basis='A proposed small-workshop and apprenticeship pact, anchored in CID’s constituency and reciprocal border cooperation. No CID defence doctrine is claimed.',sources=['cid_1970','madrid_1980'])
offer('cid','b','ITA','Italian Component-Workshop Convention','military_industry',{'corporate_tax_income_multiplier_modifier':-.025},equip={'infantry':-.04,'signals':-.04},basis='A counterfactual reciprocal supplier agreement for artisan firms. The commercial constituency is historical; the military procurement terms are proposed.',sources=['cid_1970'])
offer('cid','b','SPR','Spanish Rural-Supplier Exchange','civil_industry',{'production_speed_agriculture_district_factor':.08,'production_speed_offices_factor':.06,'corporate_tax_income_multiplier_modifier':-.03},basis='A proposed rural supplier and small-trade network. It changes no Spanish institutions, government, borders or market law.',sources=['cid_1970'])

offer('national','a','GRE','Greek Independent-Aircraft Supplier Convention','military_industry',{'equipment_cost_multiplier_modifier':-.04,'corporate_tax_income_multiplier_modifier':-.03},equip={'aircraft':-.04},basis='Greek Mirage orders in 1974 and 1985 supply the contract precedent; an FN-led agreement is counterfactual and grants no automatic arms delivery.',sources=['dassault_greece'])
offer('national','a','ROM','Romanian Sovereign Vehicle-Licensing Accord','civil_industry',{'civilian_factories_productivity':.025,'corporate_tax_income_multiplier_modifier':-.025},equip={'utility':-.04},basis='A commercial licensing channel inspired by Renault–Dacia, separate from alignment with the supplier’s political system.',sources=['dacia_1966'])
offer('national','b','ENG','British Independent Defence Consultation','training',{'naval_doctrine_cost_factor':-.08,'education_cost_multiplier_modifier':.035},basis='The FN’s 1973 platform sought priority political agreement with Britain for defence coordination. The proposed compact shares staff education only, never nuclear release authority.',sources=['fn_1973','fn_1988'])
offer('national','b','GER','German Conventional Equipment Standards','military_industry',{'foreign_influence_defense_modifier':-.035,'education_cost_multiplier_modifier':.025},equip={'tank':-.04,'signals':-.04},basis='The 1988 FN defence statement proposed European standardisation and conventional Franco-German cooperation. Earlier adoption is explicitly an RP alternative, not the January 1970 platform.',sources=['fn_1988'])

# Spatial proposal: preserve political/economic lanes, retain the 30-unit party
# stride, move military policies down to leave genuine connector channels.
orientations={
 'gaullist':('Sovereign Arsenal and Export Contracts','European Production Scale'),
 'orthodox_gaullist':('Deterrence and Protected Naval Expertise','Conventional Autonomy and Suppliers'),
 'liberal':('Competitive Aviation and Export Markets','Sustainment and Financial Credibility'),
 'centre':('Continental Land-Service Cooperation','European Maritime Specialisation'),
 'radical':('Public Engineering Partnerships','Territorial and Regional Compacts'),
 'socialist':('Public Aerospace and Conventional Cooperation','Conversion and Civilian Co-Development'),
 'communist':('Central Public-Industry Cooperation','Municipal and Mediterranean Cooperation'),
 'old_guard':('Soviet-Standard Technical Cooperation','French-Controlled Civilian Partnerships'),
 'psu':('Cooperative Producer Networks','Civilian Technical and Rescue Networks'),
 'ecology':('Continental Water and Civil Protection','Maritime Safety and Energy Conservation'),
 'cid':('Independent Repair and Credit Networks','Small-Supplier Production Networks'),
 'national':('National Supply and Sovereign Contracts','A Confederation of Defence Partners'),
}
for g in groups:
    gid=g['id'];base=g['base']
    if gid=='institutions':continue
    p=personnel[gid]
    # Two distinct personnel approaches; arms allocation remains a separate choice.
    for dx,(key,*_) in zip([8,12],p):by[key]['xy']=[base+dx,1]
    for letter,dx in zip('ab',[8,12]):
        by[f'armament_{gid}_{letter}']['xy']=[base+dx,2]
        by[f'armament_{gid}_{letter}_followup']['xy']=[base+dx,3]
        for suffix,y in [('',2),('_followup',3)]:
            n=by[f'armament_{gid}_{letter}{suffix}']
            n['description']=(f"{n['title']} gives the {names[gid]} programme a distinct procurement priority. "
                'Its technical and fiscal commitments compete with the alternative allocation; cooperation remains subject to a partner government’s consent.')
        r=by[f'research_{gid}_{letter}'];r['xy']=[base+dx,4]
        # Research follows the selected arms allocation. It never needs foreign consent.
        r['parents']=[[f'armament_{gid}_{letter}_followup']]
        r['revision']='relinked'
    for letter,dx in zip('ab',[19,25]):
        key=f'v5_{gid}_strategy_{letter}'
        n={'id':'COLDWAR_FRA_'+key,'key':key,'group':gid,'domain':'foreign',
          'title':orientations[gid][0 if letter=='a' else 1],'xy':[base+dx,6],
          'description':'Carry the selected procurement allocation into reciprocal international negotiations. Each named-country focus sends that government an offer; it decides whether to accept the published terms.',
          'history':g['history'],'parents':[[f'armament_{gid}_{letter}_followup']],
          'exclusive':[f'v5_{gid}_strategy_'+('b' if letter=='a' else 'a')],
          'mods':{},'days':35,'pp':-20,'revision':'new',
          'awards':[doctrine('naval' if gid in ['orthodox_gaullist','centre'] and letter==('a' if gid=='orthodox_gaullist' else 'b') else ('air' if gid in ['gaullist','liberal','socialist'] and letter==('b' if gid=='gaullist' else 'a') else 'land'),.25)],
          'party_gate':copy.deepcopy(by[g['entry']]['party_gate'])}
        nodes.append(n);by[key]=n
    positions={'a':[(18,4),(20,6)],'b':[(24,4),(26,6)],'shared':[(16,1)]}
    counts={'a':0,'b':0,'shared':0}
    for o in [o for o in offers if o['group']==gid]:
        side=o['side'];dx,y=positions[side][counts[side]];counts[side]+=1
        key=o['key'];parent=g['entry'] if side=='shared' else f'v5_{gid}_strategy_{side}'
        n={'id':'COLDWAR_FRA_'+key,'key':key,'group':gid,'domain':'foreign','title':o['title'],
          'xy':[base+dx,y],'parents':[[parent]],'exclusive':[],'mods':{},'days':56,'pp':-25,
          'description':f"Offer {o['title']} to {o['partner']}. The recipient government may accept or decline. The continuing agreement survives changes of government and ends if the signatories fight one another, impose bilateral sanctions or withdraw.",
          'history':o['historical_basis'],'offer_id':o['id'],'revision':'new','party_gate':copy.deepcopy(by[g['entry']]['party_gate'])}
        nodes.append(n);by[key]=n

# Remove ceremonial strategy roots: the funded armaments choice IS the strategic
# fork. Civilian exchanges must not award unrelated land-doctrine receipts.
nodes=[n for n in nodes if not (n['key'].startswith('v5_') and '_strategy_' in n['key'])]
for n in nodes:
    if n.get('offer_id'):
        o=next(o for o in offers if o['id']==n['offer_id'])
        n['parents']=[[next(g for g in groups if g['id']==n['group'])['entry'] if o['side']=='shared' else f"armament_{n['group']}_{o['side']}_followup"]]
        country={'GRE':'Greece','GER':'West Germany','ENG':'the United Kingdom','SOV':'the Soviet Union','ROM':'Romania','BEL':'Belgium','ITA':'Italy','USA':'the United States','HOL':'the Netherlands','SWI':'Switzerland','SPR':'Spain','SER':'Yugoslavia','ALG':'Algeria','DDR':'East Germany','NRY':'Norway'}[o['partner']]
        n['description']=n['description'].replace(f"to {o['partner']}", 'to '+country)
for key in ['armament_liberal_a','armament_liberal_a_followup','armament_socialist_a']:
    n=by[key]
    if 'equipment' in n:n['equipment']={('multirole' if k=='aircraft' else k):v for k,v in n['equipment'].items()}
for o in offers:
    if o['partner']=='GRE':
        for term in [o['france'],o['partner_terms']]:
            term['mods'].pop('equipment_cost_multiplier_modifier',None)
            term['mods']['air_fuel_consumption_factor']=-.04
    o['sources']=['S05' if s=='S09' else s for s in o['sources']]
    if o['group'] in ['liberal','socialist']:
        for term in [o['france'],o['partner_terms']]:
            term['equipment']={('multirole' if k=='aircraft' else k):v for k,v in term['equipment'].items()}
by['research_centre_a']['parents']=[['armament_centre_b_followup']]
by['research_centre_a']['xy']=[next(g for g in groups if g['id']=='centre')['base']+12,4]
by['research_centre_b']['parents']=[['armament_centre_a_followup']]
by['research_centre_b']['xy']=[next(g for g in groups if g['id']=='centre')['base']+8,4]
by['armament_socialist_b_followup']['title']='Long-Service Armoured Support'
by['research_socialist_b']['title']='Armoured Service-Life Modernisation'
change('gaullist_reserve_modernisation',{'air_training_xp_gain_factor':.08,'army_org_regain':.08,'army_personnel_cost_multiplier_modifier':.12},title='A Mobile Intervention Cadre',text='Preserve a specialist intervention cadre, supported by regular air-wing exercises and trained recovery services. The force gains practice and endurance without an automatic deployment or foreign commitment, while professional personnel require sustained expenditure.',award=[xp('air',20)])
change('liberal_professional_readiness',{'supply_consumption_factor':-.08,'air_accidents_factor':-.08,'army_personnel_cost_multiplier_modifier':.10,'airforce_personnel_cost_multiplier_modifier':.05},title='Professional Sustainment Corps',text='Pay the maintenance and training specialists needed to keep land and air units serviceable. Fewer supplies and fewer flying accidents reward professional standards, at the expense of a larger army and air-force payroll.',award=[xp('army',20)])
change('centre_joint_service_readiness',{'naval_doctrine_cost_factor':-.12,'naval_accidents_chance':-.06,'navy_personnel_cost_multiplier_modifier':.10},title='Maritime and Joint-Service Readiness',text='Train crews and staffs together around escort procedures, navigation and safe operation. Doctrine and accident prevention improve through a continuing naval personnel commitment, rather than a free expansion of the fleet.',award=[xp('navy',25)])
by['armament_orthodox_gaullist_a_followup']['mods']={'naval_accidents_chance':-.10,'navy_personnel_cost_multiplier_modifier':.08}
by['armament_radical_a_followup']['mods']={'line_change_production_efficiency_factor':.08,'production_speed_arms_factory_factor':-.04}
by['armament_socialist_a']['mods']={'air_training_xp_gain_factor':.10,'airforce_personnel_cost_multiplier_modifier':.08}
by['armament_liberal_b_followup']['mods']={'supply_consumption_factor':-.06,'line_change_production_efficiency_factor':.05,'production_factory_max_efficiency_factor':-.04}
by['armament_psu_a']['mods']={'line_change_production_efficiency_factor':.08,'production_factory_max_efficiency_factor':-.05}
for o in offers:
    for term in [o['france'],o['partner_terms']]:
        if 'naval_doctrine_cost_factor' in term['mods']:
            term['mods'].pop('education_cost_multiplier_modifier',None)
            term['mods']['navy_personnel_cost_multiplier_modifier']=.03
        if o['group']=='gaullist' and o['partner']=='ENG':
            term['mods']={'air_training_xp_gain_factor':.06,'air_accidents_factor':-.04,'airforce_personnel_cost_multiplier_modifier':.035}
        if o['group']=='communist' and o['partner']=='SOV':
            term['mods']={'line_change_production_efficiency_factor':.04,'production_factory_efficiency_gain_factor':-.025,'education_cost_multiplier_modifier':.02}
        if o['group']=='psu' and o['partner']=='SER':
            term['mods']={'line_change_production_efficiency_factor':.04,'production_factory_max_efficiency_factor':-.025,'social_cost_multiplier_modifier':.02}
for g in groups:
    if g['id'] in orientations:g['strategic_options']=list(orientations[g['id']])
descriptions=json.loads((HERE/'armament_descriptions.json').read_text(encoding='utf-8'))
if 'descriptions' in descriptions:descriptions=descriptions['descriptions']
for n in nodes:
    if n['key'] in descriptions:
        value=descriptions[n['key']]
        n['description']=value if isinstance(value,str) else value.get('description',n['description'])
    if n['key']=='armament_socialist_b_followup':
        n['description']='Keep a smaller armoured fleet credible through overhauls, common replacement parts and workshop training. Support contracts lower the weekly burden of land equipment and make utility vehicles cheaper to produce, while technical education remains a continuing expense. This is a selective modernisation programme alongside conversion, rather than a return to unrestricted arms expansion.'
    if n['key']=='armament_radical_a_followup':
        n['description']='Independent test establishments can make a new design easier to introduce without abandoning all the methods and tooling of its predecessor. Engineers compare components and production trials before ministers place a large order. This preserves more efficiency when a line changes, while the additional scrutiny slows the expansion of armaments factories and keeps defence investment under civilian review.'
    if n['key']=='armament_socialist_a':
        n['description']='A public aerospace programme needs trained crews as well as airframes. Fund regular wing exercises and a technical establishment able to turn industrial investment into usable flying experience. Common multirole production becomes cheaper, but the air force must sustain the personnel who operate and maintain it. The programme preserves national deployment decisions without presuming that another government will accept French industrial terms.'
    n['sources']=next((o['sources'] for o in offers if o['id']==n.get('offer_id')),[])

# Source notes accompany the proposal; no citation strings enter runtime tooltips.
source_map={s['id']:s for s in json.loads((HERE/'research_root.json').read_text(encoding='utf-8'))['sources']}
source_map.update({s['id']:{**s,'title':s['id'].replace('_',' ').title()} for s in json.loads((HERE/'research_left.json').read_text(encoding='utf-8'))['sources']})
import re
for line in (HERE/'right_centre_sources.md').read_text(encoding='utf-8').splitlines():
    m=re.search(r'\*\*(S\d+)\s+—\s+(.+?)\.\*\*\s*\[(https?[^\]]+)\]',line)
    if m:source_map[m[1]]={'id':m[1],'title':m[2],'url':m[3]}

# Rebuild exact references from the displayed graph, retain all three starting spirits.
for n in nodes:
    g=next(g for g in groups if g['id']==n['group'])
    n['anchor']=None if n['key']==g['entry'] else 'COLDWAR_FRA_'+g['entry']
    n['offset']=n['xy'] if n['anchor'] is None else [n['xy'][0]-by[g['entry']]['xy'][0],n['xy'][1]-by[g['entry']]['xy'][1]]
    n['prerequisites']=[['COLDWAR_FRA_'+k for k in row] for row in n['parents']]

proposal={
 'project':'IMPERIA COLD WAR','revision':5,'status':'Proposal only — explicit approval required before game implementation',
 'approved_base_sha256':hashlib.sha256(approved_bytes).hexdigest(),
 'groups':groups,'nodes':nodes,'offers':offers,'labels':labels,'equipment_families':equipment,'sources':list(source_map.values()),
 'spirits':A['spirits'],'residual_spirits':A['residual_spirits'],'technology_targets':A['technology_targets'],
 'agreement_rules':{
   'dispatch':'Completing a fixed-country focus gives that named recipient an ordinary country decision pair: Accept / Decline. France has no initial country-selection decision.',
   'pending_days':90,'setup_costs':'Both sides must be able to pay the displayed PP and treasury costs at acceptance. Acceptance pays both and adds both spirits in one guarded transaction. Decline or expiry grants neither.',
   'government':'The exact French party is required to propose and while pending. Accepted bilateral spirits survive government changes. Domestic party programme modifiers deactivate and return with their own government.',
   'duration':'Indefinite; no annual renewal or yearly charge.',
   'validity':'No war between signatories; no diplomatic, financial, economic or military Imperia sanctions in either direction. Withdrawal, lost sovereignty or a missing signatory ends both spirits.',
   'families':['military_industry','civil_industry','science_energy','civil_resilience','commerce','training'],
   'stacking':'One active France-linked compact per family for each signatory, across all French parties. No duplicate family stacking. Several different families may coexist. Existing family agreement must be withdrawn before another offer is accepted.',
   'reissue':'After a 180-day cooldown, the completed country focus permits a fixed-partner Reissue decision if no agreement/pending quote exists. No country picker; recipient gets fresh accept/decline decisions. No automatic reinstatement.',
   'maintenance':'Only registered active counterpart entries, at most six France-linked families; bilateral sanction-array lookups. No daily every_country scans. Actual engine scope/lifecycle verification required at implementation.',
   'foreign_sovereignty':'No forced access, alliance, war, ideology, equipment delivery, research completion or government change. Refusal never blocks domestic reform/research.',
 },
 'layout':{'party_stride':30,'institution_root':[4,0],'party_roots':[g['base'] for g in groups if g['id']!='institutions'],'military_x':[8,12],'military_y':[1,2,3,4],'foreign_x':[16,18,20,24,26],'foreign_y':[1,4,6],'opening_camera':'COLDWAR_FRA_progress_contracts','shortcuts':[{'group':g['id'],'focus':'COLDWAR_FRA_'+g['entry']} for g in groups],'grid':'All offsets relative to each party entry; all parties remain visible. Political/economic neighbours retained; compact military spine uses consecutive rows, research linked to its actual procurement chain. Both valid personnel approaches feed an OR-merge into an independent arms allocation. Shared horizontal bus connectors, not diagonal X routes. Preview uses these exact resolved coordinates; card bounds and routing are approximations, not a HOI4 render.'},
 'excluded_mechanics':['Flat daily XP and flat counter-intelligence modifiers excluded from new bundles because main MD overrides their native formatter as percentages. No 0.0 placeholder rows.','Agricolture productivity is not promised as food output: its reviewed reader is an agricultural-tax formula.','No permanent add_equipment_bonus used for retractable programme or treaty production-cost reductions.','No generic build_cost reduction, automatic resource mine, automatic nuclear weapon or future special-project completion.'],
 'references':['research_right_centre.json','research_left.json','research_root.json','mechanics_catalog.json','CATALOG_REVIEW.md'],
}
(HERE/'proposal.json').write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert hashlib.sha256((BASE/'approved_design.json').read_bytes()).hexdigest()==proposal['approved_base_sha256']
print(json.dumps({'focuses':len(nodes),'offers':len(offers),'reworked':sum(n['revision']=='reworked' for n in nodes),'output':str(HERE/'proposal.json')}))
