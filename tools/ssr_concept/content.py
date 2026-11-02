# IMPERIA COLD WAR — SSR approval concept content.
"""Design data only. Does not emit or modify loaded game content."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
PREFIX = 'COLDWAR_SSR_'
LABELS = {
 'stability_factor':'Stability', 'political_power_factor':'Political power gain',
 'production_speed_buildings_factor':'Construction speed',
 'industrial_capacity_factory':'Military factory output',
 'production_factory_max_efficiency_factor':'Production efficiency cap',
 'production_factory_efficiency_gain_factor':'Production efficiency growth',
 'civilian_factories_productivity':'Civilian industry productivity',
 'research_speed_factor':'Research speed', 'army_org_factor':'Division organisation',
 'army_morale_factor':'Division recovery rate', 'army_defence_factor':'Division defence',
 'training_time_army_factor':'Division training time',
 'supply_consumption_factor':'Supply consumption',
 'army_fuel_consumption_factor':'Army fuel consumption',
 'tax_gain_multiplier_modifier':'Tax revenue multiplier',
 'bureaucracy_cost_multiplier_modifier':'Bureaucracy expenditure multiplier',
 'social_cost_multiplier_modifier':'Social expenditure multiplier',
 'army_personnel_cost_multiplier_modifier':'Army personnel expenditure multiplier',
 'foreign_influence_modifier':'Foreign influence gain',
 'agricolture_productivity_modifier':'Agricultural productivity',
 'energy_use_multiplier':'Energy use',
 'productivity_growth_modifier':'Productivity growth',
 'consumer_goods_factor':'Consumer goods factor',
 'corporate_tax_income_multiplier_modifier':'Corporate tax revenue multiplier',
 'production_speed_industrial_complex_factor':'Civilian factory construction speed',
 'production_speed_arms_factory_factor':'Military factory construction speed',
 'production_speed_air_base_factor':'Air base construction speed',
 'production_speed_naval_base_factor':'Naval base construction speed',
 'industrial_capacity_dockyard':'Dockyard output',
 'air_training_xp_gain_factor':'Air training experience gain',
 'air_fuel_consumption_factor':'Air fuel consumption',
 'navy_org_factor':'Naval organisation',
 'navy_fuel_consumption_factor':'Naval fuel consumption',
 'energy_gain_multiplier':'Energy generation',
 'oil_export_multiplier_modifier':'Fossil fuel export revenue multiplier',
 'local_resources_oil_factor':'Fossil fuel extraction',
 'local_resources_aluminium_factor':'Light metal extraction',
 'local_resources_tungsten_factor':'Technology metal extraction',
 'local_resources_steel_factor':'Steel extraction',
 'local_resources_chromium_factor':'Precious metal extraction',
}
KEYS = dict(st='stability_factor',pp='political_power_factor',build='production_speed_buildings_factor',
 out='industrial_capacity_factory',cap='production_factory_max_efficiency_factor',
 eff='civilian_factories_productivity',research='research_speed_factor',org='army_org_factor',
 morale='army_morale_factor',defence='army_defence_factor',train='training_time_army_factor',
 supply='supply_consumption_factor',fuel='army_fuel_consumption_factor',tax='tax_gain_multiplier_modifier',
 admin='bureaucracy_cost_multiplier_modifier',social='social_cost_multiplier_modifier',
 milcost='army_personnel_cost_multiplier_modifier',influence='foreign_influence_modifier',
 agri='agricolture_productivity_modifier',energy='energy_use_multiplier',growth='productivity_growth_modifier',
 cg='consumer_goods_factor',corp='corporate_tax_income_multiplier_modifier',civbuild='production_speed_industrial_complex_factor',
 milbuild='production_speed_arms_factory_factor',airbase='production_speed_air_base_factor',navalbase='production_speed_naval_base_factor',
 dock='industrial_capacity_dockyard',airtrain='air_training_xp_gain_factor',airfuel='air_fuel_consumption_factor',
 navalorg='navy_org_factor',navalfuel='navy_fuel_consumption_factor',power='energy_gain_multiplier',oilexport='oil_export_multiplier_modifier',
 oil='local_resources_oil_factor',light='local_resources_aluminium_factor',techmetals='local_resources_tungsten_factor',
 steel='local_resources_steel_factor',precious='local_resources_chromium_factor')
NUMBER_KEYS={'productivity_growth_modifier'}
def M(**kw): return {KEYS[k]:v if KEYS[k] in NUMBER_KEYS else v/100 for k,v in kw.items()}

STARTING = [
 dict(id='plan_shortages',name='Plan Targets and Shortages',modifiers=M(cap=-10,eff=-10),
      description='Output targets reward volume while bottlenecks, unsuitable deliveries and weak incentives slow adaptation.',
      resolution='Enterprise accounting and either productive investment or consumer supply reform. These improve different parts of the problem.'),
 dict(id='cadre_patronage',name='Republican Patronage Networks',modifiers=M(pp=-10,admin=8),
      description='Republican cadres mediate access to appointments and resources. Their local knowledge coexists with protection and concealed failure.',
      resolution='Professional appointments or a political discipline campaign. The former costs money; the latter disrupts established networks.'),
 dict(id='social_guarantees',name='Soviet Social Guarantees',modifiers=M(st=8,social=10),
      description='Employment, subsidised services and republican welfare institutions offer security at a substantial fiscal cost.',
      resolution='Retain an affordable service settlement or reorganise provision after sovereignty. The service cost and stability are a single package.'),
 dict(id='union_network',name='Union Technical Network',modifiers=M(research=5,supply=-5),
      description='Union institutes, technical standards and military logistics give the republic access to capabilities beyond its own budget.',
      resolution='Active only with genuine SSR status and operating Union links. Independence removes these advantages; cooperation must then be negotiated.'),
]
TRANSITION = [
 dict(id='broken_supply',name='Fractured Supply Chains',modifiers=M(out=-15,eff=-15,build=-10),
      description='Formerly internal orders become cross-border contracts. Payment disputes and missing components interrupt production.'),
 dict(id='state_accounts',name='Unsettled State Accounts',modifiers=M(tax=-15,admin=15,pp=-10),
      description='The republic must establish a tax administration, settle public accounts and replace Union budget arrangements.'),
 dict(id='command_gap',name='Unsettled Defence Administration',modifiers=M(org=-12,train=10,milcost=10),
      description='Personnel, command authority and maintenance obligations must be reassigned. Existing forces are not automatically transferred.'),
]

GROUPS=[]
NODES=[]
def G(key,title,x,y,phase='ssr',note=''):
    programmes={'secretariat':'Republican Administration','planning':'Republican Economic Programme',
      'society':'Republican Social Institutions','union_defence':'Union Defence Contribution',
      'statehood':'State Administration','transition_economy':'Economic Reconstruction',
      'national_defence':'National Defence Administration','foreign':'Foreign Service',
      'regional':'Republican Development Programme'}
    group=dict(id=key,title=title,x=x,y=y,phase=phase,note=note,programme=programmes.get(key,title+' Programme'))
    GROUPS.append(group)
    return group
def F(g,key,title,desc,x,y,parents=(),*,mod=None,gdp_cost=0,cost=5,kind='institution',
      spirit=None,replace=None,remove=None,building=None,research=None,xp=0,doctrine=None,
      stability=0,decision=None,action=None,ownership=None,gate=None,**extra):
    p=[[v] if isinstance(v,str) else list(v) for v in parents]
    # Russia's ordinary two-way policy forks use -2/+2 native grid offsets.
    x=2 if x==3 else (-2 if x==-3 else x)
    n=dict(id=PREFIX+key,key=key,title=title,description=desc,group=g['id'],
           x=g['x']+x,y=g['y']+y,prerequisites=[[PREFIX+k for k in v] for v in p],exclusive=[],
           cost=cost,days=cost*7,modifiers=mod or {},gdp_cost=gdp_cost,kind=kind,
           spirit=spirit or (g['programme'] if mod else None),effect_mode='add' if spirit else 'modify',replace=replace,remove=remove,
           building=building,research=research,army_xp=xp,doctrine=doctrine,stability=stability,
           decision=decision,action=action,gate=None if g['phase']=='ssr' else gate,phase=g['phase'],
           ownership=ownership or ('SSR programme' if g['phase']=='ssr' else 'National institution'))
    n.update(extra)
    NODES.append(n)
    return key
def X(a,b):
    aa=next(n for n in NODES if n['key']==a);bb=next(n for n in NODES if n['key']==b)
    aa['exclusive'].append(bb['id']);bb['exclusive'].append(aa['id'])
def B(name,level=1): return dict(type=name,level=level,shared_slots=level,target='Project state')
def R(cat,bonus=50,uses=1): return dict(category=cat,bonus=bonus/100,uses=uses)

def common():
    g=G('secretariat','The Republican Administration',8,0,note='The First Secretary is the political leader in January 1970. If the Union or republic changes its political system, the shared programme continues under its actual republican leadership.')
    F(g,'secretariat','Republican Mandate','The republican leadership must reconcile local development with obligations to the Union. In January 1970 the First Secretary leads this work. Existing political and succession institutions determine who holds office after a constitutional change.',0,0,mod=M(pp=5,admin=3),spirit='Republican Administration')
    F(g,'moscow_cadres','Union Appointments','Accept greater central oversight in return for administrative access and predictable investment priorities.',-3,1,['secretariat'],mod=M(pp=8,build=5,admin=4),spirit='Union Cadre Compact')
    F(g,'local_cadres','Republican Cadres','Promote cadres who understand local production and language. A stronger republican machine is harder for the centre to supervise.',3,1,['secretariat'],mod=M(admin=-8,st=5,research=-3),spirit='Republican Cadre Compact');X('moscow_cadres','local_cadres')
    F(g,'appointment_school','Cadre Schools','Training administrators improves routine work without settling the political balance between the centre and republic.',0,2,[['moscow_cadres','local_cadres']],gdp_cost=0.0008,mod=M(admin=-5))
    F(g,'audit_staff','Professional Audits','Use accountants and engineers to expose concealed failures, paying for a permanent inspection service.',-3,3,['appointment_school'],gdp_cost=0.0005,replace='Republican Patronage Networks',mod=M(admin=-3,research=3),spirit='Professional Appointments')
    F(g,'discipline_campaign','Administrative Discipline','A concentrated administrative campaign can break patronage quickly, but removals unsettle officials and enterprises.',3,3,['appointment_school'],replace='Republican Patronage Networks',mod=M(pp=8,st=-4),spirit='Cadre Discipline',stability=-0.03);X('audit_staff','discipline_campaign')
    F(g,'complaints_office','Public Petitions','Give workers a channel for complaints within the Soviet institutions, increasing scrutiny of republican administration.',0,4,[['audit_staff','discipline_campaign']],mod=M(st=4,admin=3))
    F(g,'plan_bargain','Plan Negotiations','Bring verified republican needs into the Union planning process. Local proposals gain substance when backed by credible accounts.',0,5,['complaints_office'],mod=M(build=5,pp=-3))
    F(g,'priority_orders','Union Priorities','Give strategic Union orders priority over local consumer demand.',-3,6,['plan_bargain'],mod=M(out=10,social=4),spirit='Strategic Order Book')
    F(g,'local_retention','Local Reinvestment','Reserve more managerial attention and investment for production serving republican needs.',3,6,['plan_bargain'],mod=M(build=8,out=-4),spirit='Republican Reinvestment');X('priority_orders','local_retention')
    F(g,'successor_training','Train the Secretariat','A trained second rank reduces dependence on one officeholder. This does not appoint a successor outside the existing political system.',0,7,[['priority_orders','local_retention']],gdp_cost=0.0005,mod=M(pp=5,admin=-3))
    F(g,'controlled_debate','Controlled Debate','Allow published criticism inside the party and republican institutions, accepting a less uniform political message.',-3,8,['successor_training'],mod=M(research=5,pp=-5))
    F(g,'unified_line','A Unified Line','Concentrate the political apparatus around an agreed line. Administrative certainty comes at the expense of independent expertise.',3,8,['successor_training'],mod=M(pp=10,research=-4));X('controlled_debate','unified_line')
    F(g,'republican_statute','Republican Statute','Clarify the republican administration within the Union constitution without proclaiming independence.',0,9,[['controlled_debate','unified_line']],mod=M(admin=-4,st=3))
    F(g,'union_delegate','Republican Delegation','Represent republican priorities through the institutions of the continuing Union. The delegation serves the republic regardless of either government\'s political outlook.',0,10,['republican_statute'],mod=M(pp=5,admin=-3))

    g=G('planning','The Republican Economy',20,0)
    F(g,'economic_accounts','Republican Accounts','Establish a reliable account of republican inputs, deliveries and investment before choosing a development priority.',0,0,mod=M(tax=3,admin=3))
    F(g,'combine_priority','Industrial Combines','Concentrate investment in a modern industrial combine connected to Union supply chains.',-3,1,['economic_accounts'],gdp_cost=0.015,building=B('industrial_complex'),mod=M(energy=3),kind='industry',cost=10)
    F(g,'consumer_priority','Consumer Supply','Improve consumer production and distribution rather than expanding a large industrial combine. Resources move away from military production.',3,1,['economic_accounts'],gdp_cost=0.004,mod=M(st=6,tax=4,out=-3),kind='industry');X('combine_priority','consumer_priority')
    F(g,'enterprise_accounts','Enterprise Accounts','Apply enterprise accounting to make costs visible while keeping the political choice of production priorities.',0,2,[['combine_priority','consumer_priority']],replace='Plan Targets and Shortages',mod=M(cap=-5,eff=-5),spirit='Revised Plan Targets',ownership='Inherited national constraint')
    F(g,'output_incentives','Output Incentives','Reward enterprises for technically demanding deliveries, accepting pressure on energy and input use.',-3,3,['enterprise_accounts'],mod=M(cap=10,out=5,energy=4),spirit='Production Incentives',kind='industry')
    F(g,'quality_contracts','Quality Contracts','Prioritise dependable components and quality controls over gross tonnage.',3,3,['enterprise_accounts'],mod=M(eff=12,research=3,out=-3),spirit='Quality Standards',kind='research');X('output_incentives','quality_contracts')
    F(g,'rail_depots','Freight Connections','Improve a republican freight corridor, with investment limited to a state the republic actually owns and controls.',0,4,[['output_incentives','quality_contracts']],gdp_cost=0.003,building=B('infrastructure'),kind='industry',cost=7)
    F(g,'rural_processing','Food Processing','Expand local processing and storage so that agricultural output reaches consumers in useful form.',-3,5,['rail_depots'],gdp_cost=0.002,mod=M(agri=10,energy=2),kind='agriculture')
    F(g,'machine_tools','Machine Tools','Upgrade production machinery and engineering capability within the research available to the 1970 scenario.',3,5,['rail_depots'],gdp_cost=0.002,research=R('CAT_industry'),kind='research')
    F(g,'service_networks','Distribution Network','Connect processing and industrial production to reliable distribution institutions.',0,6,['rural_processing','machine_tools'],gdp_cost=0.001,mod=M(tax=3,admin=2),kind='industry')
    F(g,'new_power','Power Investment','Add conventional generation appropriate to the republic. A survey does not create a uranium mine or a nuclear station.',-3,7,['service_networks'],gdp_cost=0.008,building=B('fossil_powerplant'),mod=M(energy=2),kind='industry',cost=10)
    F(g,'energy_savings','Energy Discipline','Use meters, insulation and industrial audits to lower demand rather than building another power plant.',3,7,['service_networks'],gdp_cost=0.002,mod=M(energy=-8,out=-2),kind='industry');X('new_power','energy_savings')
    F(g,'maintenance_stocks','Maintenance Stocks','Protect maintenance supplies against plan bottlenecks, financing stores instead of adding another headline construction project.',0,8,[['new_power','energy_savings']],gdp_cost=0.0012,mod=M(energy=-3,supply=-3),kind='industry')
    F(g,'diversify_orders','Diversify Orders','Build republican commercial and planning competence before any possible change of constitutional status.',-3,9,['maintenance_stocks'],gdp_cost=0.001,mod=M(tax=3,out=-2),action='Supply disruption preparedness +1',kind='industry')
    F(g,'deepen_specialisation','Specialised Orders','Deepen a productive Union specialisation. The efficiency gain increases exposure to the loss of those orders.',3,9,['maintenance_stocks'],mod=M(out=8,cap=5),action='Supply disruption exposure +1',kind='industry');X('diversify_orders','deepen_specialisation')
    F(g,'plan_settlement','Investment Settlement','Complete the investment cycle with a defined improvement to enterprise performance.',0,10,[['diversify_orders','deepen_specialisation']],replace='Revised Plan Targets',mod=M(eff=3),spirit='Republican Production Standards',kind='industry',ownership='Permanent national improvement')

    g=G('society','Society and Institutions',32,0)
    F(g,'social_accounts','Social Institutions','Measure the cost and reach of republican education, housing and health institutions before expanding them.',0,0,gdp_cost=0.0003,mod=M(admin=-3),kind='society')
    F(g,'technical_institutes','Technical Institutes','Invest in engineers and applied science for the republic and Union economy.',-3,1,['social_accounts'],gdp_cost=0.003,mod=M(research=5,social=4),research=R('CAT_electronics'),kind='research')
    F(g,'vocational_schools','Vocational Schools','Prioritise skilled workers and maintenance staff over research institutes.',3,1,['social_accounts'],gdp_cost=0.002,mod=M(eff=6,train=-5,social=4),kind='society');X('technical_institutes','vocational_schools')
    F(g,'housing_repairs','Housing Repairs','Improve existing housing and municipal services rather than promising a free city-building programme.',0,2,[['technical_institutes','vocational_schools']],gdp_cost=0.0015,mod=M(st=4,social=3),kind='society')
    F(g,'republican_culture','Republican Culture','Support republican language and cultural institutions within the Union framework. The local political settlement varies by republic.',-3,3,['housing_repairs'],mod=M(st=5,admin=3),kind='society')
    F(g,'union_curriculum','Union Curriculum','Standardise technical and administrative education for Union mobility, accepting less room for local priorities.',3,3,['housing_repairs'],mod=M(research=5,st=-3),kind='research');X('republican_culture','union_curriculum')
    F(g,'public_health','Public Health','Finance preventive medicine and local services through republican institutions.',0,4,[['republican_culture','union_curriculum']],gdp_cost=0.0012,mod=M(st=3,social=3),kind='society')
    F(g,'collective_farms','Farm Machinery','Modernise collective agriculture with machinery and repair capacity.',-3,5,['public_health'],gdp_cost=0.002,mod=M(agri=12,energy=3),kind='agriculture')
    F(g,'household_plots','Household Supply','Give household plots and local markets a larger role in food supply, with more difficult accounting and oversight.',3,5,['public_health'],mod=M(agri=8,st=4,tax=-3),kind='agriculture');X('collective_farms','household_plots')
    F(g,'water_accounts','Water and Land','Record the true costs of irrigation, industrial waste and land management. The regional programme supplies the specific response.',0,6,[['collective_farms','household_plots']],gdp_cost=0.0008,mod=M(agri=4,admin=2),kind='agriculture')
    F(g,'environmental_controls','Protect Land and Water','Enforce environmental limits even when established enterprises resist slower or more expensive production.',-3,7,['water_accounts'],gdp_cost=0.001,mod=M(agri=8,out=-3),kind='agriculture')
    F(g,'remediation_fund','Remediation Fund','Finance practical repairs while allowing existing production to continue.',3,7,['water_accounts'],gdp_cost=0.003,mod=M(agri=4,eff=4),kind='industry');X('environmental_controls','remediation_fund')
    F(g,'service_settlement','Service Settlement','Put recurring service commitments on a more durable fiscal basis without abolishing their social value.',0,8,[['environmental_controls','remediation_fund']],replace='Soviet Social Guarantees',mod=M(st=8,social=6),spirit='Republican Social Guarantees',ownership='Permanent national institution',kind='society')
    F(g,'civil_registers','Civil Registers','Prepare trained administrators and usable civil records for the republic, whatever constitutional settlement follows.',0,9,['service_settlement'],gdp_cost=0.0008,action='State accounts preparedness +1',mod=M(admin=-3),ownership='Permanent national improvement',kind='society')

    g=G('union_defence','The Union Defence Contribution',44,0,note='The 1970 SSR does not gain a sovereign army. Industry, civil defence and training remain inside Union command.')
    F(g,'defence_commission','Defence Commission','Coordinate republican industry, training and civil defence under the Union armed forces.',0,0,gdp_cost=0.0005,mod=M(train=-5,milcost=3),kind='army')
    F(g,'military_components','Military Components','Invest in components and repair workshops for existing Union procurement.',-3,1,['defence_commission'],gdp_cost=0.012,building=B('arms_factory'),mod=M(energy=3),kind='army',cost=10)
    F(g,'dual_use_industry','Dual-Use Workshops','Develop civilian workshops with defence applications rather than a dedicated arms factory.',3,1,['defence_commission'],gdp_cost=0.003,mod=M(eff=6,research=3,out=-3),research=R('CAT_industry'),kind='industry');X('military_components','dual_use_industry')
    F(g,'technical_reserves','Technical Reserves','Train repair personnel and reserve specialists without creating new divisions or taking Union equipment.',0,2,[['military_components','dual_use_industry']],xp=15,mod=M(train=-5,milcost=2),kind='army')
    F(g,'specialist_training','Specialist Training','Use longer technical instruction to improve the quality of republican military personnel.',-3,3,['technical_reserves'],gdp_cost=0.0008,mod=M(org=5,train=5),research=R('CAT_infantry'),kind='army')
    F(g,'mass_training','Broad Reserve Training','Prepare a larger body of reservists with a less specialised curriculum.',3,3,['technical_reserves'],gdp_cost=0.0005,mod=M(train=-10,org=-3),xp=20,kind='army');X('specialist_training','mass_training')
    F(g,'military_repairs','Repair Standards','Standardise repair documentation and spare-parts handling within Union logistics.',0,4,[['specialist_training','mass_training']],gdp_cost=0.001,mod=M(supply=-5),kind='army')
    F(g,'civil_shelters','Civil Defence','Fund shelters, warning services and emergency exercises for civilian protection.',-3,5,['military_repairs'],gdp_cost=0.0012,mod=M(st=4,admin=3),kind='society')
    F(g,'strategic_transport','Strategic Transport','Upgrade a corridor serving both local transport and Union mobilisation.',3,5,['military_repairs'],gdp_cost=0.003,building=B('infrastructure'),kind='industry',cost=7)
    F(g,'officer_education','Officer Education','Give republican personnel access to technical military education inside the existing Union command system.',0,6,['civil_shelters','strategic_transport'],research=R('CAT_artillery'),xp=15,kind='army')
    F(g,'fuel_discipline','Fuel Discipline','Improve military fuel handling through stricter maintenance routines.',-3,7,['officer_education'],mod=M(fuel=-8,train=3),kind='army')
    F(g,'ready_stocks','Readiness Stocks','Finance ready spare parts and exercises to improve recovery, accepting a more expensive personnel establishment.',3,7,['officer_education'],gdp_cost=0.0012,mod=M(morale=8,milcost=5),kind='army');X('fuel_discipline','ready_stocks')
    F(g,'defence_records','Defence Records','Prepare accurate personnel and maintenance records for future negotiations over republican responsibilities.',0,8,[['fuel_discipline','ready_stocks']],gdp_cost=0.0005,action='Defence administration preparedness +1',kind='army',ownership='Permanent national improvement')
    F(g,'combined_exercises','Combined Exercises','Exercise within Union command. The training result does not grant equipment, foreign territory or an independent armed force.',0,9,['defence_records'],xp=25,doctrine=dict(category='land_doctrine',bonus=0.35,uses=1),kind='army',cost=7)

    g=G('statehood','Sovereignty and Statehood',8,14,'independent',note='Independence is resolved by existing diplomacy and the Soviet system. This chapter is immediately reachable after actual independence, even if no SSR focus was completed.')
    F(g,'public_authority','Public Authority','Establish the republic as a functioning independent state. Constitution-making follows the actual political settlement, not a required Soviet-era focus chain.',0,0,gdp_cost=0.0005,mod=M(pp=5,admin=3),kind='institution')
    F(g,'citizenship_civic','Civic Citizenship','Offer broad equal citizenship and participation while paying for multilingual administration.',-3,1,['public_authority'],mod=M(st=5,admin=5),spirit='Civic Citizenship',kind='society')
    F(g,'citizenship_restoration','Legal Restoration','Use prior legal continuity or a national restoration settlement to strengthen authority. New residents and minorities require a separate accommodation.',3,1,['public_authority'],mod=M(pp=12,st=-4),spirit='Restoration Settlement',kind='institution');X('citizenship_civic','citizenship_restoration')
    F(g,'rights_commission','Rights Commission','Provide an independent procedure for grievances rather than assuming constitutional words settle every local dispute.',0,2,[['citizenship_civic','citizenship_restoration']],gdp_cost=0.0008,mod=M(research=2,admin=2),kind='society')
    F(g,'unitary_services','Unitary Services','Concentrate services and revenues under a single republican administration.',-3,3,['rights_commission'],mod=M(admin=-8,pp=5,st=-3))
    F(g,'local_guarantees','Local Guarantees','Negotiate local representation and service rights without promising automatic territorial transfers.',3,3,['rights_commission'],mod=M(st=4,admin=6,pp=-4));X('unitary_services','local_guarantees')
    F(g,'revenue_service','Revenue Service','Rebuild the collection and legal machinery of state revenue.',0,4,[['unitary_services','local_guarantees']],gdp_cost=0.0012,action='State accounts recovery +1',mod=M(tax=3),ownership='Permanent national improvement')
    F(g,'court_review','Judicial Review','Make administrative action reviewable by courts, improving confidence at the cost of a slower political executive.',-3,5,['revenue_service'],gdp_cost=0.0008,mod=M(tax=5,pp=-5))
    F(g,'executive_service','Executive Service','Use a concentrated executive to rebuild public authority, accepting weaker external scrutiny.',3,5,['revenue_service'],mod=M(pp=10,admin=-4,research=-3));X('court_review','executive_service')
    F(g,'registered_accounts','Registered Accounts','Finish the fiscal settlement after the revenue service and a budget course have been established.',0,6,[['court_review','executive_service']],action='State accounts recovery +1',ownership='Permanent national improvement')
    F(g,'social_compact','Social Compact','Negotiate a public commitment on wages and services. It preserves social security while making its cost visible.',0,7,['registered_accounts'],gdp_cost=0.001,mod=M(st=3,social=4),kind='society')

    g=G('transition_economy','The Economic Transition',20,14,'independent')
    F(g,'payment_register','Payments Register','Identify interrupted contracts and unpaid deliveries before choosing a response to the economic rupture.',0,0,gdp_cost=0.0005,action='Supply recovery +1',kind='industry')
    F(g,'gradual_conversion','Gradual Conversion','Keep essential enterprises operating while changing contracts and ownership in stages.',-3,1,['payment_register'],mod=M(st=4,eff=5,tax=-5),spirit='Gradual Conversion',kind='industry')
    F(g,'rapid_conversion','Rapid Conversion','Harden enterprise budgets and speed conversion, accepting immediate social losses.',3,1,['payment_register'],mod=M(tax=8,build=5,st=-6),spirit='Rapid Conversion',kind='industry');X('gradual_conversion','rapid_conversion')
    F(g,'supplier_contracts','Supplier Contracts','Replace internal plan deliveries with enforceable contracts. International agreements can complement this work but cannot substitute for domestic institutions.',0,2,[['gradual_conversion','rapid_conversion']],gdp_cost=0.001,action='Supply recovery +1',kind='industry')
    F(g,'worker_ownership','Worker Participation','Give employees a role in restructuring. This can protect trust and practical knowledge but complicates investment decisions.',-3,3,['supplier_contracts'],mod=M(st=4,eff=5,build=-3),kind='industry')
    F(g,'open_tenders','Open Tenders','Use competitive restructuring and sale procedures to attract investment, while accepting disruption to established workforces.',3,3,['supplier_contracts'],mod=M(build=10,tax=4,st=-4),kind='industry');X('worker_ownership','open_tenders')
    F(g,'industrial_conversion','Industrial Conversion','Convert production lines and maintenance standards for new customers.',0,4,[['worker_ownership','open_tenders']],gdp_cost=0.003,research=R('CAT_industry'),action='Supply recovery +1',kind='industry')
    F(g,'budget_protection','Protect Public Services','Finance the fiscal transition with a broader revenue effort while protecting basic services.',-3,5,['industrial_conversion'],mod=M(st=3,tax=4,build=-3,social=4),action='State accounts recovery +1',kind='society')
    F(g,'budget_consolidation','Fiscal Consolidation','Cut administrative commitments quickly while rebuilding the tax base, accepting a difficult social adjustment.',3,5,['industrial_conversion'],mod=M(admin=-10,tax=6,st=-5),action='State accounts recovery +1');X('budget_protection','budget_consolidation')
    F(g,'commercial_standards','Commercial Standards','Complete a common standard for contracts, banking documentation and enterprise accounts.',0,6,[['budget_protection','budget_consolidation']],gdp_cost=0.001,mod=M(eff=5),kind='industry')
    F(g,'export_conversion','Export Conversion','Pay to replace specialised old orders with competitive production for new customers.',-3,7,['commercial_standards'],gdp_cost=0.004,mod=M(out=6,build=4,st=-2),action='Remove specialised-order transition exposure',kind='industry')
    F(g,'domestic_chains','Domestic Suppliers','Rebuild local supplier networks rather than relying on a new external export market.',3,7,['commercial_standards'],gdp_cost=0.003,mod=M(eff=8,energy=3),action='Remove specialised-order transition exposure',kind='industry');X('export_conversion','domestic_chains')
    F(g,'transition_settlement','Economic Settlement','Conclude the domestic reconstruction programme. Supply and state-account recovery remain tied to completed reforms rather than a timer.',0,8,[['export_conversion','domestic_chains']],mod=M(tax=3),kind='industry')

    g=G('national_defence','Independent Defence',32,14,'independent')
    F(g,'defence_authority','Defence Authority','Establish civilian responsibility for defence. Personnel and equipment settlements with other states require their agreement.',0,0,gdp_cost=0.0008,action='Defence administration recovery +1',kind='army')
    F(g,'professional_force','Professional Force','Concentrate resources on a smaller professional establishment with stronger unit cohesion.',-3,1,['defence_authority'],mod=M(org=8,train=5,milcost=10),spirit='Professional Service',kind='army')
    F(g,'territorial_force','Territorial Service','Build a broad territorial reserve and local defence network at the cost of less standardised training.',3,1,['defence_authority'],mod=M(defence=8,train=-8,org=-4),spirit='Territorial Service',kind='army');X('professional_force','territorial_force')
    F(g,'maintenance_command','Maintenance Command','Fund a national repair and personnel administration before promising combat expansion.',0,2,[['professional_force','territorial_force']],gdp_cost=0.002,action='Defence administration recovery +1',research=R('CAT_infantry'),kind='army')
    F(g,'local_officers','National Officer School','Train officers for the new chain of command. This does not duplicate foreign training benefits.',-3,3,['maintenance_command'],gdp_cost=0.002,xp=25,research=R('CAT_artillery'),kind='army')
    F(g,'reserve_records','Reserve Records','Build a usable register and training service for reserve personnel.',3,3,['maintenance_command'],gdp_cost=0.0008,mod=M(train=-5,milcost=3),xp=15,kind='army')
    F(g,'defence_settlement','Command Settlement','Complete a coherent command and maintenance structure after both the officer and reserve services are established.',0,4,['local_officers','reserve_records'],action='Defence administration recovery +1',kind='army')
    F(g,'mobile_defence','Mobile Defence','Train for mobile manoeuvre while accepting higher fuel demand.',-3,5,['defence_settlement'],mod=M(org=5,fuel=8),doctrine=dict(category='land_doctrine',bonus=0.35,uses=1),kind='army')
    F(g,'prepared_defence','Prepared Defence','Prioritise sustained territorial defence with a larger logistical burden.',3,5,['defence_settlement'],mod=M(defence=8,supply=4),doctrine=dict(category='land_doctrine',bonus=0.35,uses=1),kind='army');X('mobile_defence','prepared_defence')

    g=G('foreign','An Independent Foreign Policy',44,14,'independent')
    F(g,'foreign_service','Foreign Service','Our republic must now speak with its own voice. A professional diplomatic service will defend its interests abroad and negotiate the relationships on which lasting independence depends.',0,0,gdp_cost=0.0005,mod=M(influence=5,admin=3),kind='diplomacy')
    F(g,'old_market_offer','Clearing Agreement','Propose a standing clearing and industrial supply arrangement to the Soviet state or its actual successor. The other government decides whether to accept.',-3,1,['foreign_service'],action='offer:clearing',kind='diplomacy')
    F(g,'new_market_offer','Technical Partnership','Industrial reconstruction requires machinery and expertise beyond our borders. A technical partnership will connect our enterprises to experienced suppliers and new commercial standards.',3,1,['foreign_service'],action='offer:technical',kind='diplomacy')
    F(g,'border_offer','Border Commission','Propose a joint commission with a real neighbour to regulate crossings and practical border administration. No territorial change is implied.',-7,2,[['old_market_offer','new_market_offer']],action='offer:border',kind='diplomacy')
    F(g,'training_offer','Training Convention','Offer a mutual training convention with a selected capable partner. It grants no military base or automatic faction membership.',-3,3,['foreign_service'],action='offer:training',kind='diplomacy')
    F(g,'civil_neutrality','Civil Neutrality','Prioritise independent territorial readiness and civilian diplomacy over a foreign military training convention.',3,3,['foreign_service'],mod=M(defence=5,influence=5,org=-2),kind='diplomacy');X('training_offer','civil_neutrality')
    F(g,'energy_offer','Energy and Transit','Offer an energy-transit convention to a suitable neighbour or supplier, based on an existing route and real local capacity.',-3,4,[['training_offer','civil_neutrality']],action='offer:energy',kind='diplomacy')
    F(g,'river_offer','Water Commission','Offer a standing water and environmental commission to a country sharing the relevant basin.',3,4,[['training_offer','civil_neutrality']],action='offer:water',kind='diplomacy')
    F(g,'regional_service','Regional Diplomacy','Train officials to manage practical agreements without assuming admission to a modern organisation.',0,5,[['energy_offer','river_offer']],gdp_cost=0.0008,mod=M(influence=5,admin=2),kind='diplomacy')

# Standing bilateral numbers are complete for both parties. The target has a real
# accept/refuse decision. Costs are distinct from native subject subsidies.
CONTRACTS={
 'clearing':dict(title='Industrial Clearing Convention',target='SOV or its actual recognised successor',
   origin=dict(spirit='Industrial Clearing Convention',gdp_cost=0.0005,weekly=-0.0004,modifiers=M(out=6,tax=3,build=-2)),
   recipient=dict(spirit='Republican Supply Convention',gdp_cost=0.0003,weekly=-0.0002,modifiers=M(out=3,tax=2,admin=2)),basis='Continuity of inter-republic contracts, bilateral clearing and the trade-payment problems of the early transition.'),
 'technical':dict(title='Technical Cooperation Convention',target='Selected capable independent RP partner',
   origin=dict(spirit='Technical Cooperation Convention',gdp_cost=0.0008,weekly=-0.0005,modifiers=M(research=6,eff=5,admin=3)),
   recipient=dict(spirit='Republican Technical Partnership',gdp_cost=0.0003,weekly=-0.0003,modifiers=M(research=2,tax=3,admin=2)),basis='Technical licensing, training and enterprise restructuring partnerships. This is an alternate-history treaty based on those practices.'),
 'border':dict(title='Border Administration Convention',target='Selected actual neighbouring RP country',
   origin=dict(spirit='Joint Border Administration',gdp_cost=0.0003,weekly=-0.0002,modifiers=M(st=3,tax=2,admin=2)),
   recipient=dict(spirit='Joint Border Administration',gdp_cost=0.0003,weekly=-0.0002,modifiers=M(st=3,tax=2,admin=2)),basis='Successor-state border and customs administration. No settlement of a disputed border or third-country rights without consent.'),
 'training':dict(title='Defence Training Convention',target='Selected capable independent RP partner',
   origin=dict(spirit='Defence Training Convention',gdp_cost=0.0008,weekly=-0.0005,modifiers=M(org=5,train=-5,milcost=4)),
   recipient=dict(spirit='Reciprocal Training Mission',gdp_cost=0.0003,weekly=-0.0003,modifiers=M(morale=3,influence=3,milcost=3)),basis='Bilateral training missions and successor-state defence cooperation. This is a practical convention, not automatic collective security.'),
 'energy':dict(title='Energy Transit Convention',target='Selected eligible supplier or transit neighbour',
   origin=dict(spirit='Energy Transit Convention',gdp_cost=0.0008,weekly=-0.0004,modifiers=M(eff=5,tax=3,admin=2)),
   recipient=dict(spirit='Energy Transit Convention',gdp_cost=0.0005,weekly=-0.0003,modifiers=M(tax=4,build=3,admin=2)),basis='Post-Soviet fuel supply and transit interdependence. No energy units, resource deposits or pipelines are created by this administrative agreement.'),
 'water':dict(title='Shared Basin Convention',target='Selected RP country sharing the actual basin',
   origin=dict(spirit='Shared Basin Commission',gdp_cost=0.0005,weekly=-0.0003,modifiers=M(agri=6,st=2,admin=3)),
   recipient=dict(spirit='Shared Basin Commission',gdp_cost=0.0005,weekly=-0.0003,modifiers=M(agri=6,st=2,admin=3)),basis='The 1992 Almaty water-cooperation agreement and earlier shared irrigation management provide a later historical analogue. Earlier agreements are alternate history.'),
}

# Each formal programme has its own real governing-slot requirement. Institutions
# in the inherited 1970 roster are explicitly labelled alternate-history coalitions.
SELECTION={
 'UKR':[(4,'communist'),(0,'liberation'),(1,'national'),(2,'liberal'),(3,'social'),(20,'nationalist'),(21,'authoritarian')],
 'BLR':[(4,'communist'),(1,'national'),(2,'liberal'),(3,'social')],
 'MLV':[(4,'communist'),(1,'conservative'),(2,'liberal'),(3,'social'),(20,'unionist')],
 'EST':[(4,'communist'),(0,'restoration'),(1,'national'),(2,'liberal'),(3,'social')],
 'LAT':[(4,'communist'),(0,'restoration'),(1,'national'),(2,'liberal'),(3,'social')],
 'LIT':[(4,'communist'),(0,'restoration'),(1,'conservative'),(2,'liberal'),(3,'social'),(20,'nationalist')],
 'GEO':[(4,'communist'),(1,'national'),(2,'liberal'),(3,'social')],
 'ARM':[(4,'communist'),(0,'national_social'),(1,'liberal'),(18,'social'),(20,'national')],
 'AZE':[(4,'communist'),(1,'national'),(2,'liberal'),(3,'social')],
 'KAZ':[(4,'communist'),(2,'liberal'),(3,'social'),(20,'national')],
 'UZB':[(4,'communist'),(1,'national'),(2,'liberal'),(3,'social'),(14,'conservative')],
 'TRK':[(4,'communist'),(1,'national'),(2,'liberal'),(3,'social'),(14,'conservative')],
 'KYR':[(4,'communist'),(1,'national'),(2,'liberal'),(3,'social'),(14,'conservative')],
 'TAJ':[(4,'communist'),(1,'national'),(2,'liberal'),(3,'social'),(12,'faith_civic')],
}
LEADERS={
 'UKR':('Ukrainian SSR','Petro Shelest','Heavy industry, coal and Union defence orders','Industrial Balance','Consumer Diversification'),
 'BLR':('Byelorussian SSR','Pyotr Masherov','Machine building, chemicals and integrated Union markets','Machine-Building Complex','Food and Light Industry'),
 'MLV':('Moldavian SSR','Ivan Bodiul','Food processing, agriculture and cross-Dniester industry','Agricultural Processing','Mixed Republican Industry'),
 'EST':('Estonian SSR','Johannes Käbin','Oil shale, engineering and Baltic maritime connections','Oil-Shale Modernisation','Technical Diversification'),
 'LAT':('Latvian SSR','Augusts Voss','Engineering, ports and a large Union industrial workforce','Engineering Orders','Port and Consumer Services'),
 'LIT':('Lithuanian SSR','Antanas Sniečkus','Manufacturing, agriculture and local cadre institutions','Manufacturing Network','Agricultural Modernisation'),
 'GEO':('Georgian SSR','Vasil Mzhavanadze','Subtropical agriculture, light industry and informal trade','Tea and Processing','Light-Industrial Workshops'),
 'ARM':('Armenian SSR','Anton Kochinyan','Engineering, scientific institutions and imported inputs','Engineering Institutes','Local Supply Workshops'),
 'AZE':('Azerbaijan SSR','Heydar Aliyev','Oil refining, engineering and the Caspian economy','Refining and Equipment','Non-Oil Industry'),
 'KAZ':('Kazakh SSR','Dinmukhamed Kunaev','Mining, grain, Union industry and environmental damage','Industrial and Grain Orders','Regional Diversification'),
 'UZB':('Uzbek SSR','Sharaf Rashidov','Cotton specialisation, irrigation and Union industrial inputs','Cotton Processing','Food and Textile Balance'),
 'TRK':('Turkmen SSR','Muhammetnazar Gapurov','Gas, irrigated cotton and long transport distances','Gas and Textile Orders','Water-Saving Diversification'),
 'KYR':('Kirghiz SSR','Turdakun Usubaliev','Hydropower, livestock, industry and budget transfers','Hydropower and Workshops','Rural Processing'),
 'TAJ':('Tajik SSR','Jabar Rasulov','Irrigated cotton, hydropower and regional inequalities','Cotton and Power Orders','Food and Regional Industry'),
}
LATER={
 'UKR':'Rukh (1989)', 'BLR':'Belarusian Popular Front (1989)', 'MLV':'Popular Front of Moldova (1989)',
 'EST':'Rahvarinne and restoration movements (1988)', 'LAT':'Latvian Popular Front (1988)',
 'LIT':'Sajudis (1988)', 'GEO':'Round Table-Free Georgia (1990)', 'ARM':'Armenian National Movement (1989)',
 'AZE':'Azerbaijani Popular Front (1989)', 'KAZ':'Nevada-Semipalatinsk (1989) and Azat (1990)',
 'UZB':'Birlik (1989) and Erk (1990)', 'TRK':'Agzibirlik (late 1980s)',
 'KYR':'Democratic Movement of Kyrgyzstan (1990)', 'TAJ':'Rastokhez (1989) and Islamic Renaissance Party (1990)',
}
REGIONAL={
 'UKR':('Heavy-Industrial Imbalance',M(eff=-5,energy=4),M(out=8,cap=5,energy=4),M(eff=8,st=3,out=-3)),
 'BLR':('Dependence on Union Orders',M(eff=-5,cap=-3),M(out=6,cap=8,energy=3),M(agri=10,tax=4,out=-3)),
 'MLV':('Uneven Processing Networks',M(agri=-5,eff=-3),M(agri=12,tax=4,energy=3),M(eff=8,build=4,agri=-3)),
 'EST':('Costs of Oil-Shale Industry',M(energy=5,eff=-3),M(eff=10,energy=-3,social=3),M(research=6,build=5,out=-3)),
 'LAT':('Union Industrial Dependence',M(eff=-5,energy=3),M(out=7,cap=6,energy=4),M(tax=7,eff=5,out=-3)),
 'LIT':('Competing Farm and Factory Needs',M(build=-5,energy=3),M(eff=9,out=4,energy=3),M(agri=12,st=3,tax=-3)),
 'GEO':('Protected Informal Networks',M(tax=-6,admin=5),M(agri=12,tax=3,energy=3),M(eff=8,build=5,agri=-3)),
 'ARM':('Imported Industrial Inputs',M(eff=-6,energy=3),M(research=7,out=5,energy=4),M(eff=10,st=3,cap=-3)),
 'AZE':('Ageing Oil-Industrial Equipment',M(eff=-5,energy=5),M(eff=10,cap=5,energy=3),M(build=7,research=4,out=-3)),
 'KAZ':('Industrial and Environmental Burdens',M(social=5,agri=-4),M(out=7,agri=8,energy=5),M(eff=7,agri=5,cap=-3)),
 'UZB':('Cotton and Irrigation Dependence',M(agri=-8,tax=-3),M(eff=7,agri=8,energy=4),M(agri=10,st=4,out=-3)),
 'TRK':('Irrigated Desert Economy',M(agri=-6,admin=4),M(eff=8,tax=5,energy=4),M(agri=12,energy=-3,out=-3)),
 'KYR':('Seasonal Water and Energy Imbalance',M(eff=-4,energy=3),M(eff=8,out=5,energy=3),M(agri=10,st=4,tax=-3)),
 'TAJ':('Uneven Regional Investment',M(admin=6,build=-4),M(agri=10,out=5,energy=4),M(agri=8,build=6,cap=-3)),
}

def party_profile(tag):
    registry=json.loads((ROOT/f'tools/party_registry_1970/data/{tag}.json').read_text(encoding='utf-8-sig'))
    parties=[]
    for slot,family in SELECTION[tag]:
        entry=registry['slots'][str(slot)][0]
        formal=(slot==4 or (tag,slot) in {('UKR',0),('UKR',1),('UKR',3),('UKR',20),('UKR',21),('BLR',1),('EST',0),('EST',1),('EST',3),('LAT',0),('LAT',1),('LAT',3),('LIT',0),('LIT',1),('LIT',2),('LIT',3),('LIT',20),('GEO',3),('ARM',0),('ARM',1),('ARM',18),('ARM',20),('AZE',1),('MLV',1),('MLV',20)})
        parties.append(dict(slot=slot,family=family,name=entry['english'],registered_name=entry['name'],
                            status='Existing party, exile body or underground organisation' if formal else 'Alternate-history governing coalition drawn from the registered 1970 institution or circle',
                            description=entry['text'].replace('\u2013','-').replace('\u2014',':')))
    name,leader,context,a,b=LEADERS[tag]
    regional_name,regional_mod,regional_a,regional_b=REGIONAL[tag]
    independent={'UKR':'Ukraine','BLR':'Belarus','MLV':'Moldova','EST':'Estonia','LAT':'Latvia','LIT':'Lithuania',
      'GEO':'Georgia','ARM':'Armenia','AZE':'Azerbaijan','KAZ':'Kazakhstan','UZB':'Uzbekistan',
      'TRK':'Turkmenistan','KYR':'Kyrgyzstan','TAJ':'Tajikistan'}[tag]
    return dict(tag=tag,name=name,independent_name=independent,leader=leader,leader_title='First Secretary',context=context,
                regional_choices=[a,b],regional=dict(name=regional_name,modifiers=regional_mod,
                description=context+'. This spirit abstracts a documented constraint; its percentages are balance proposals.',
                choices=[regional_a,regional_b]),later=LATER[tag],parties=parties)

def regional_module(profile):
    # One country-specific policy fork. Names differ, but not arbitrary ethnic traits.
    g=G('regional','Republican Development Priorities',56,0)
    F(g,'regional_review','Regional Priorities',profile['context']+'. The republican development choice addresses this actual specialisation.',0,0,gdp_cost=0.0003,kind='industry')
    F(g,'regional_orders',profile['regional_choices'][0],'Modernise the established regional specialisation. Its productive strengths come with continued input and energy exposure.',-3,1,['regional_review'],gdp_cost=0.002,mod=profile['regional']['choices'][0],kind='industry')
    F(g,'regional_diversify',profile['regional_choices'][1],'Build a broader local supplier and consumer base, accepting a smaller immediate return from the established specialisation.',3,1,['regional_review'],gdp_cost=0.002,mod=profile['regional']['choices'][1],action='Supply disruption preparedness +1',kind='industry');X('regional_orders','regional_diversify')
    F(g,'regional_standards','Regional Standards','Bring the chosen sector under credible technical and financial supervision. This reduces the regional constraint without pretending to erase its structural or environmental legacy.',0,2,[['regional_orders','regional_diversify']],gdp_cost=0.0005,research=R('CAT_industry'),replace=profile['regional']['name'],mod={k:round(v/2,5) for k,v in profile['regional']['modifiers'].items()},spirit='Managed '+profile['regional']['name'],ownership='Permanent national improvement',kind='research')

CONTRACTS['romanian']=dict(title='Romanian Cultural Convention',target='Romania',
 origin=dict(spirit='Romanian Cultural Convention',gdp_cost=0.0003,weekly=-0.0002,modifiers=M(research=3,st=2,admin=2)),
 recipient=dict(spirit='Moldavian Cultural Convention',gdp_cost=0.0003,weekly=-0.0002,modifiers=M(research=3,st=2,admin=2)),
 basis='Romanian-Moldavian linguistic and cultural links. This alternate-history convention has no territorial reward.')

def design(tag):
    GROUPS.clear();NODES.clear()
    p=party_profile(tag)
    common();regional_module(p)
    import revision_2
    revision_2.apply(p)
    # One universal tree with a common core and static country-selected modules.
    # Party-specific branches never disappear when their governing party changes.
    renamed={n['id']:PREFIX+tag+'_'+n['key'] for n in NODES if n['phase']=='party' or n['group']=='regional' or n.get('specialisation')}
    for n in NODES:
        n['id']=renamed.get(n['id'],n['id'])
        n['prerequisites']=[[renamed.get(v,v) for v in group] for group in n['prerequisites']]
        n['exclusive']=[renamed.get(v,v) for v in n['exclusive']]
        n['country_module']=tag if n['phase']=='party' or n['group']=='regional' or n.get('specialisation') else None
    for n in NODES:
        # Earlier declarations are stable anchors; exact offsets are recorded for implementation.
        first=next(v for v in NODES if v['group']==n['group'])
        n['anchor']=None if first is n else first['id']
        n['offset']=[n['x'],n['y']] if first is n else [n['x']-first['x'],n['y']-first['y']]
    return dict(profile=p,groups=list(GROUPS),nodes=list(NODES))
