"""Reviewable Greek1970 focus design. Never writes a game runtime directory."""
from pathlib import Path
import json, re
from collections import Counter
from regime_paths import add_paths, apply_gates, effect_lines, proposed_effects
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
P='COLDWAR_GRE_1970_'
nodes=[]; sections=[]
def slug(s): return re.sub('[^a-z0-9]+','_',s.lower()).strip('_')
def section(key,title,x,y,note=''):
    sections.append(dict(id=key,title=title,anchor=[x,y],description=note))
def node(key,title,sec,xy,parents=(),mods=None,cost=0,pp=0,stability=0,note='',requires='',days=35,icon='industry',slot=None,removes=(),event='',build=None,xp=None):
    a=next(s['anchor'] for s in sections if s['id']==sec)
    d=dict(id=P+key,key=key,title=title,section=sec,x=a[0]+xy[0],y=a[1]+xy[1],
      local_x=xy[0],local_y=xy[1],prerequisite_groups=[[P+p] for p in parents],excludes=[],
      days=days,focus_cost=round(days/7,5),modifiers=mods or {},treasury_cost_gdp_percent=cost,
      political_power=pp,stability=stability,note=note,requirements=requires,icon=icon,
      modifier_slot=slot,removes=list(removes),event_contract=event,building=build,xp=xp,
      status='Design proposal; not implemented or engine tested')
    nodes.append(d);return d
def either(n,*parents):n['prerequisite_groups']=[[P+p for p in parents]];return n
def exclusive(a,b):
    aa=next(n for n in nodes if n['key']==a);bb=next(n for n in nodes if n['key']==b)
    aa['excludes'].append(bb['id']);bb['excludes'].append(aa['id'])
def spirit(key,title,mods,note,scope='country',activation='start'):
    return dict(id=P+key,key=key,title=title,modifiers=mods,note=note,scope=scope,activation=activation)

spirits=[
 spirit('rule_by_decree','Rule by Decree',{'stability_factor':-.08,'political_power_factor':.05},'Suspended freedoms and decree government. Administrative coercion is not democratic legitimacy; institutional reform removes this package.'),
 spirit('security_state','Censorship, Detention and Torture',{'police_cost_multiplier_modifier':.15,'stability_factor':-.05},'Military courts, censorship, arbitrary detention and documented torture under the dictatorship. Victims and responsibility remain explicit; repression cannot erase the resulting grievance.'),
 spirit('politicised_officers','A Politicised Officer Corps',{'army_org_factor':-.08,'max_planning':-.05},'Personal networks, loyalty promotions and competing junta circles disrupt professional command. Not a claim that Greek soldiers are inherently ineffective.'),
 spirit('european_censure','European Censure',{'foreign_influence_defense_modifier':-.10},'Greece left the Council of Europe on12December1969 after the Greek Case. This is not expulsion from NATO or from a nonexistent1970 EU membership.'),
 spirit('uneven_regions','Uneven Regional Development',{'state_production_speed_buildings_factor':-.08,'state_productivity_growth_modifier':-.08},'Rural skills, fragmented holdings and weak local links limit convergence. Applied only to selected owned rural states, not every Greek resident.',scope='states139Thessaly /142Peloponnese /974WestThrace'),
 spirit('administrative_clientelism','Clientelism and Fragmented Administration',{'bureaucracy_cost_multiplier_modifier':.10},'Fragmented administration and patronage impose costs. Audits and professional recruitment reduce these; an ethnic group never constitutes the penalty.'),
 spirit('growth_foundations','Foundations of the Greek Expansion',{'production_speed_buildings_factor':.05},'Industrial expansion, shipping, tourism and emigrant remittances provide real strengths in1970. Values are gameplay proposals, not measured historical growth rates.'),
 spirit('crown_in_exile','A Crown in Exile',{'political_power_factor':-.03},'ConstantineII remains in exile and Zoitakis is regent inJanuary1970. A negotiated constitutional settlement or legitimate referendum can settle the issue.'),
 spirit('oil_shock','Oil Import Shock',{'production_speed_buildings_factor':-.08,'social_cost_multiplier_modifier':.08},'Conditional external supply/price shock, never a January1970 starting penalty. A world oil shock or actual import disruption must occur.',activation='conditional'),
 spirit('crisis_dislocation','Mobilisation and Civilian Dislocation',{'stability_factor':-.08,'social_cost_multiplier_modifier':.12},'Only actual mobilisation, fighting or displacement can activate this. Losses and humanitarian needs are recorded once, not paid for twice by overlapping systems.',activation='conditional')]

regime_packages=add_paths(section,node,either,exclusive,P)

# Important party programmes follow the domestic regime settlement.
routes=[
 dict(key='pap',title='PAPADOPOULOS · REGIME & LIBERALISATION',x=6,party=22,leader='Georgios Papadopoulos',icon='junta',gate='Nationalist military junta in office AND Papadopoulos is the actual ruling leader.',
 names=['The Papadopoulos Cabinet','Consolidate the Decree Government','Controlled Liberalisation','Retain Military Tutelage','Civilian Technocrats','Loyalty before Expertise','Define the Successor State','Development through the Banks','Tourism Concessions','Productive Export Credit','The Coastal Hotel Programme','Industrial Credit Windows','Review the Investment Regime','Selective European Opening','Bilateral Patronage','Rights Benchmarks for Talks','Security Bargains with Patrons','A Sustainable Opening','A Cabinet with Civilian Reach','The Regime after the Colonels'],
 choices=[({'political_power_factor':.03,'stability_factor':.03},{'political_power_factor':.07,'stability_factor':-.02}),({'production_speed_buildings_factor':.07,'social_cost_multiplier_modifier':.04},{'production_factory_max_efficiency_factor':.06,'bureaucracy_cost_multiplier_modifier':.03}),({'foreign_influence_defense_modifier':.04},{'foreign_influence_defense_modifier':-.04,'political_power_factor':.04})],
 notes=['A controlled opening is a risky political proposal, not a completed democracy. Refusal by opposition and officer obstruction remain possible.','Security tutelage preserves officer leverage and the documented coercive state; the rights grievance remains.','Tourism produces investment but dependence on seasonal foreign earnings.','Export credit trades slower visible consumption gains for productive capacity.','European institutions and other players must accept terms; never grants automatic membership.','A patron must actually agree; military access and influence have an explicit price.']),
 dict(key='ioa',title='IOANNIDIS · SECURITY RULE',x=18,party=22,leader='Dimitrios Ioannidis',icon='junta',gate='Nationalist military junta in office AND an actual domestic leadership change has placed Ioannidis in power; Gizikis may be formal president.',
 names=['The Security Directorate','Control the Junta Networks','A Closed Officer Circle','Broaden the Officer Compact','ESA Surveillance','Service-Wide Bargaining','Resolve the Command Rivalry','A Siege-Economy Budget','Priority Military Procurement','Preserve Civilian Production','Army Supply Workshops','Civilian Suppliers under Contract','Review Emergency Spending','Maximum Pressure on Nicosia','Restrain the Cyprus Plotters','Authorise a Covert Proposal','Keep the Guard out of Politics','Command without Illusions','Account for the Security State','A Regime Facing its Costs'],
 choices=[({'political_power_factor':.08,'stability_factor':-.04,'police_cost_multiplier_modifier':.08},{'army_org_factor':.05,'political_power_factor':-.02}),({'production_factory_max_efficiency_factor':.06,'production_speed_buildings_factor':-.04},{'production_speed_buildings_factor':.05}),({'army_org_factor':.03,'foreign_influence_defense_modifier':-.08},{'stability_factor':.04,'foreign_influence_defense_modifier':.04})],
 notes=['ESA policing and torture are named explicitly. Surveillance can consolidate the ruler while increasing security costs and unresolved opposition grievances.','A broader compact improves coordination but reduces the ruler’s personal control.','Priority procurement crowds out civilian investment; no free divisions or weapons.','Civilian orders maintain the tax and industrial base.','A covert approach sends a proposal into the Cyprus/Greek-officer crisis system. Only actual accepted preparation can enable a coup; Turkish/Greek-Cypriot responses are independent.','Restraint can break with hardliners; no scripted invasion is needed to make the choice meaningful.']),
 dict(key='nd',title='KANELLOPOULOS / KARAMANLIS · ERE → ND',x=30,party=1,leader='Panagiotis Kanellopoulos / Konstantinos Karamanlis',icon='republic',gate='Conservative civilian government in office, an actual electoral/constitutional mandate and the appropriate contemporary leader. ERE before4October1974; ND only after its actual formation.',
 names=['A Civilian Conservative Mandate','Return the State to Parliament','Prosecute the Torturers','A Limited Officer Amnesty','Independent Courts','Negotiated Military Retirement','A Civilian Chain of Command','The Social-Market Programme','Competitive Export Industry','Protect Strategic Enterprises','SME Credit and Competition','Public Utilities with Audits','A Credible Fiscal Settlement','Negotiate European Association','First Rebuild National Capacity','An Accession Dossier','Domestic Regulatory Readiness','A State beyond the Junta','Balanced Regional Investment','A European Parliamentary Republic'],
 choices=[({'stability_factor':.05,'political_power_factor':-.02},{'army_org_factor':.04,'stability_factor':-.02}),({'production_factory_max_efficiency_factor':.07},{'production_speed_buildings_factor':.07,'bureaucracy_cost_multiplier_modifier':.04}),({'foreign_influence_defense_modifier':.03},{'production_speed_buildings_factor':.04})],
 notes=['Accountability reduces the security-state legacy after actual judicial implementation; temporary officer resistance remains a political risk.','Amnesty eases bargaining with the army but leaves victim claims unresolved and cannot also claim the accountability reward.','Competition supports productive exporters without an automatic foreign subsidy.','State enterprises retain strategic capacity with recurring administrative costs.','Association/entry requires counterpart consent and implemented legal conditions. Greece is not an EEC member in1970.','Domestic readiness is a viable economic route if European players decline.']),
 dict(key='centre',title='MAVROS · THE LIBERAL CENTRE',x=42,party=2,leader='Georgios Mavros',icon='election',gate='Liberal civilian party in office and a genuine parliamentary mandate. Centre Union; Centre Union–New Forces only in its contemporary phase.',
 names=['Rebuild the Liberal Centre','A Coalition for Civil Liberties','Independent Justice','A Broad Reconciliation Pact','Civilian Police Oversight','Local Reconciliation Boards','A Parliament that Can Govern','Enterprise without Patronage','Break the Credit Cartels','A Social Credit Compact','Open Bank Tendering','Cooperative Local Banks','A Tax Base beyond Athens','Open the European Channel','Lead a Regional Mediation','Association on Equal Terms','A Balkan Trade Conference','The Centre Holds','Professional Public Appointments','A Liberal Democratic Settlement'],
 choices=[({'stability_factor':.05},{'political_power_factor':.04,'stability_factor':.02}),({'production_factory_max_efficiency_factor':.06,'bureaucracy_cost_multiplier_modifier':-.03},{'production_speed_buildings_factor':.06,'social_cost_multiplier_modifier':.03}),({'foreign_influence_defense_modifier':.03},{'political_power_factor':.03})],
 notes=['Judicial accountability follows civilian due process, not arbitrary collective punishment.','Reconciliation can reduce polarisation while retaining obligations to victims.','Competition and public tenders break protected financial networks.','Social credit broadens access but requires a funded guarantee scheme.','Counterpart agreement is necessary; no instant European accession.','Mediation requires participation by the other states; it cannot order them to settle Cyprus.']),
 dict(key='pasok',title='ANDREAS PAPANDREOU · PAK → PASOK',x=54,party=3,leader='Andreas Papandreou',icon='social',gate='Social-democratic government in office, legal party competition and an electoral mandate. PAK opposition before1974; PASOK requires its actual formation, no earlier than3September1974.',
 names=['A Mandate for Change','Bring the Exiles Home','Parliamentary Socialism','Executive-Led Transformation','A Pluralist Labour Movement','A Central Programme Office','Recognise the Civil-War Excluded','Social Investment on the Mainland','Universal Public Provision','Targeted Rural Transfers','Build a National Health Network','Cooperative Farm Services','Pay for the Social Contract','Negotiate the Western Relationship','Pursue Non-Aligned Autonomy','Bargain over Base Access','Diversify Trade Partners','Change that Can Be Financed','Regional Universities and Skills','Democratic Social Transformation'],
 choices=[({'stability_factor':.05,'political_power_factor':.02},{'political_power_factor':.07,'bureaucracy_cost_multiplier_modifier':.04}),({'research_speed_factor':.04,'social_cost_multiplier_modifier':.08},{'production_speed_buildings_factor':.06,'social_cost_multiplier_modifier':.04}),({'foreign_influence_defense_modifier':.04},{'foreign_influence_defense_modifier':.07,'production_factory_max_efficiency_factor':-.02})],
 notes=['A parliamentary route recognises pluralism and preserves competitive elections.','Executive centralisation speeds programme coordination while increasing administration and patronage risks.','Public provision is an ongoing spending commitment, not free stability or free healthcare.','Targeted transfers leave some urban needs unmet but concentrate scarce funds.','US/NATO players can accept or decline renegotiated access. No forced foreign base removal.','Non-alignment is an alternate policy requiring actual trade arrangements; it never creates Soviet aid.']),
 dict(key='kke',title='KOLIGIANNIS / FLORAKIS · KKE',x=66,party=4,leader='Kostas Koligiannis / Charilaos Florakis',icon='communism',gate='KKE legally holds executive power through an actual mandate or a separately resolved domestic revolution. Koligiannis beforeDecember1972, Florakis thereafter; no automatic communist takeover.',
 names=['The KKE Enters Government','Settle the Civil-War Legacy','A Popular Democratic Coalition','A Single-Party Vanguard','Independent Trade Unions','Party Control of the Workplace','Determine the Socialist Constitution','A Programme of Social Ownership','Worker-Managed Cooperatives','Central Investment Planning','Elected Factory Councils','A State Planning Commission','Account for the Plan','Diversified Socialist Trade','A Soviet Security Orientation','Non-Aligned Commercial Missions','Negotiate an Eastern Accord','A Socialist Economy that Functions','Returnees, Housing and Skills','The Greek Socialist Settlement'],
 choices=[({'stability_factor':.05,'political_power_factor':.02},{'political_power_factor':.08,'stability_factor':-.03,'police_cost_multiplier_modifier':.06}),({'production_factory_max_efficiency_factor':.06,'bureaucracy_cost_multiplier_modifier':.02},{'production_speed_buildings_factor':.08,'bureaucracy_cost_multiplier_modifier':.08}),({'foreign_influence_defense_modifier':.06},{'army_org_factor':.04,'foreign_influence_defense_modifier':-.08})],
 notes=['The coalition retains political competition; this is distinct from a one-party state.','A vanguard state concentrates authority and introduces new repression risks. It cannot also claim pluralist legitimacy.','Cooperative management decentralises decisions and needs skilled administration.','Central planning can mobilise investment but carries administrative and allocation costs.','Trade diversification requires actual agreements, not gifted resources or factories.','The Soviet player must accept any security agreement; alignment has a sovereignty cost and never spawns an ally army.']),
 dict(key='royal',title='CONSTANTINE II · A CONTESTED RESTORATION',x=78,party=23,leader='Constantine II',icon='crown',gate='A monarchy has actually been restored through a valid constitutional settlement. The exiled king is not the starting government and the regent is not a party leader.',
 names=['Negotiate the King’s Return','A Settlement beyond the Failed Counter-Coup','A Parliamentary Crown','A Crown above Parliament','A Politically Neutral Palace','A Royal Officer Network','Define the Crown’s Reserve Powers','A Royal Development Programme','Regional Enterprise Funds','Palace-Directed Strategic Capital','Rural Roads and Small Business','Audited National Enterprises','Publish the Civil List','A Parliamentary European Course','An Autonomous Royal Diplomacy','A Constitutional Foreign Mandate','Negotiate Bilateral Guarantees','A Crown with Public Consent','A Civil Service beyond Patronage','The Settlement Put to the Voters'],
 choices=[({'stability_factor':.05},{'political_power_factor':.06,'stability_factor':-.03}),({'production_speed_buildings_factor':.06,'bureaucracy_cost_multiplier_modifier':-.02},{'production_factory_max_efficiency_factor':.06,'bureaucracy_cost_multiplier_modifier':.04}),({'foreign_influence_defense_modifier':.03},{'foreign_influence_defense_modifier':.05,'political_power_factor':-.02})],
 notes=['A constitutional monarch accepts parliamentary supremacy and civilian oversight.','Royal prerogative revives opposition and officer-network risks; restoration is not universal support.','Regional funds decentralise credit through audited eligibility.','Palace direction concentrates strategic capital but creates patronage costs.','European partners judge the constitutional arrangement and may refuse talks.','Bilateral guarantees need the named foreign players; there is no automatic royal alliance.'])]

shape=[(0,0),(0,2),(-3,4),(3,4),(-3,6),(3,6),(0,8),(0,10),(-3,12),(3,12),(-3,14),(3,14),(0,16),(-3,18),(3,18),(-3,20),(3,20),(0,22),(-3,24),(3,24)]
parents=[[],[0],[1],[1],[2],[3],[4,5],[6],[7],[7],[8],[9],[10,11],[12],[12],[13],[14],[15,16],[17],[17]]
for route in routes:
    k=route['key'];section(k,route['title'],route['x'],44,route['gate'])
    for i,(title,xy) in enumerate(zip(route['names'],shape)):
        ps=[k+'_'+str(j) for j in parents[i]]
        if i==0:ps=['state_dossier']
        mods={};cost=0;pp=0;st=0;note='';icon=route['icon'];slot=None
        if i in (2,3,8,9,13,14):
            pair={2:0,3:0,8:1,9:1,13:2,14:2}[i]; side=0 if i in (2,8,13) else 1
            mods=route['choices'][pair][side];note=route['notes'][pair*2+side];slot=['institutions','economy','alignment'][pair]
            cost=.8 if pair==1 else 0;icon=route['icon'] if pair==0 else 'industry' if pair==1 else 'diplomacy'
        elif i in (4,5):pp=25;note='Implements the chosen institutional policy. Does not award the opposing policy package.'
        elif i in (7,10,11,12,18,19):
            cost={7:.5,10:1,11:1,12:.5,18:.8,19:.8}[i];icon='industry' if i<13 else 'education'
            if i in (10,11):mods={'production_speed_buildings_factor':.03};slot='regional_programme';note='Funded implementation bonus for365days. Refreshes this slot rather than stacking an additional permanent idea.'
            elif i==12:pp=35;note='Audit the fiscal cost of the current programme. No automatic debt cancellation or free funds.'
            elif i in (18,19):mods={'bureaucracy_cost_multiplier_modifier':-.03} if i==18 else {'research_speed_factor':.025};slot='administration' if i==18 else 'skills';note='Conditional implementation reward; government programmes share national slot ceilings.'
        elif i in (15,16):note='A foreign-policy dossier is submitted. A counterpart can negotiate, accept, defer or refuse; no reward is paid before implementation.';icon='diplomacy'
        elif i in (6,17):st=.025;note='An implemented domestic settlement is required. This is not an automatic regime change.'
        else:pp=25
        n=node(k+'_'+str(i),title,k,xy,ps,mods,cost,pp,st,note,route['gate'],days=49 if i in (6,12,17,19) else 35,icon=icon,slot=slot)
        n['party']=route['party'];n['leader']=route['leader']
        if i in (6,12,17):either(n,*ps)
        if i in (15,16):n['event_contract']=note;n['execution_mode']='proposal'
        if i in (10,11):n['duration_days']=365
    for a,b in [(2,3),(8,9),(13,14)]:exclusive(k+'_'+str(a),k+'_'+str(b))

# Common branches are independent roots, as in MD. The common branches do not
# require completing a rival party programme or a foreign player's focus.
def common(key,title,x,titles,choices,icon='industry',note=''):
    section(key,title,x,76,note)
    for i,(name,xy) in enumerate(zip(titles,shape)):
        ps=[key+'_'+str(j) for j in parents[i]]
        mods={};cost=0;pp=0;details='';slot=None
        if i in (2,3,8,9,13,14):
            q={2:0,3:0,8:1,9:1,13:2,14:2}[i];side=0 if i in (2,8,13) else 1
            mods=choices[q][side];slot=key+'_policy_'+str(q);details='Alternative policy packages replace this slot. Benefits require funded implementation; the opposing choice is excluded.'
        elif i in (4,5,10,11,18,19):cost=1;details='Domestic implementation programme funded from current GDP. Recheck funds, ownership and capacity when completed; no partial unpaid reward.'
        else:pp=20
        n=node(key+'_'+str(i),name,key,xy,ps,mods,cost,pp,note=details,requires='Greece exists;1970scenario; programme conditions remain met.',days=49 if i in (7,12,17,19) else 35,icon=icon,slot=slot)
        if i in (6,12,17):either(n,*ps)
    for a,b in [(2,3),(8,9),(13,14)]:exclusive(key+'_'+str(a),key+'_'+str(b))

common('economy','ECONOMY · REGIONS & EXTERNAL EARNINGS',6,
 ['Survey the National Economy','Map the Regional Gaps','Export Manufacturing','Domestic Enterprise Networks','Industrial Standards and Skills','SME Credit Guarantees','A Broader Productive Base','Thessaly and the Rural Economy','Cooperative Farm Services','Agribusiness Consolidation','Irrigation and Veterinary Access','Agricultural Logistics','Connect the Regional Markets','Tourism at Scale','Protect the Coastline','Regional Airports and Hotels','Heritage and Island Access','Invest Beyond the Capital','Professional Tax Collection','A More Resilient Expansion'],
 [({'production_factory_max_efficiency_factor':.07},{'production_speed_buildings_factor':.06}),({'production_speed_buildings_factor':.05,'social_cost_multiplier_modifier':.03},{'production_factory_max_efficiency_factor':.07,'stability_factor':-.015}),({'production_speed_buildings_factor':.06,'social_cost_multiplier_modifier':.04},{'stability_factor':.03,'production_speed_buildings_factor':.03})],note='Preserve1970 growth while addressing rural gaps and dependence on shipping, tourism and remittances.')
common('army','ARMY · PROFESSIONAL COMMAND',21,
 ['Audit the Hellenic Army','Separate Rank from Patronage','Civilian Defence Oversight','A Professional Service Council','Publish the Promotion Rules','Merit-Based Officer Boards','A Credible Chain of Command','A Mainland Defence Review','Mobile Reserve Forces','Prepared Defensive Sectors','Modernise Signals and Transport','Dispersed Mobilisation Stores','A Funded Mobilisation Plan','Domestic Maintenance Capacity','Licensed Foreign Systems','Repair Workshops and Tooling','Submit Procurement Contracts','An Army Greece Can Sustain','Mountain and Island Exercises','A National Defence Doctrine'],
 [({'army_org_factor':.05,'political_power_factor':-.02},{'max_planning':.06}),({'army_org_factor':.05,'max_planning':-.02},{'max_planning':.08,'army_org_factor':-.02}),({'production_factory_max_efficiency_factor':.05},{'army_org_factor':.04,'foreign_influence_defense_modifier':-.03})],icon='army')
common('navy','NAVY · THE AEGEAN & THE MERCHANT MARINE',36,
 ['An Aegean Maritime Review','Audit the Fleet and Dockyards','Sea Denial in the Aegean','Escort and Sea-Lane Protection','Submarine and Torpedo Training','Convoy Escort Coordination','A Fleet Mission within Means','Connect the Island Ports','Concentrate at Major Bases','Disperse Island Support','Expand Existing Naval Facilities','Fuel and Repair across the Islands','Sustain the Maritime Network','Merchant Shipping Incentives','Bind Support to Domestic Investment','A Competitive Shipping Registry','Domestic Training and Yard Orders','Civil-Military Maritime Planning','Damage Control and Rescue','A Sustainable Hellenic Fleet'],
 [({'naval_coordination':.06},{'naval_coordination':.04}),({'naval_coordination':.05},{'naval_coordination':.04,'production_speed_buildings_factor':-.015}),({'production_speed_buildings_factor':.05,'bureaucracy_cost_multiplier_modifier':.03},{'production_factory_max_efficiency_factor':.05})],icon='navy')
common('air','AIR FORCE · READINESS & PROCUREMENT',51,
 ['Audit Air Readiness','Map Airfield Vulnerabilities','Air Defence First','A Balanced Strike Force','Radar and Interception Drills','Joint Strike Coordination','A Mission for Every Squadron','Build a Technical Training Base','Train at Home','Exchange Training Abroad','Airframe and Engine Workshops','Negotiate Instructor Access','Ground Crews before Prestige','Disperse Existing Airfields','Concentrate Training Resources','Shelters, Fuel and Repair','A Common Training Centre','Measure Operational Availability','Secure a Procurement Budget','Aircraft that Can Be Maintained'],
 [({'air_mission_efficiency':.06},{'air_mission_efficiency':.04}),({'air_mission_efficiency':.04,'research_speed_factor':.02},{'air_mission_efficiency':.05,'foreign_influence_defense_modifier':-.03}),({'air_mission_efficiency':.05,'production_speed_buildings_factor':-.015},{'air_mission_efficiency':.03})],icon='air')
common('foreign','FOREIGN POLICY · ALLIES WITHOUT BLANK CHEQUES',66,
 ['Review the Treaty Commitments','Separate NATO from the Council of Europe','Meet Human-Rights Benchmarks','Retain the Security Exceptions','Invite Independent Monitoring','Account for Continued Censure','A Credible European Dossier','Negotiate the American Relationship','Base Access for Written Terms','Greater Operational Autonomy','A Reciprocal Access Agreement','National Command Arrangements','Document What Partners Accepted','Reopen the Balkan Channels','Mediterranean Commercial Diplomacy','Propose Trade with Yugoslavia','Open Multi-Partner Shipping Talks','A Foreign Policy that Can Be Delivered','Fund the Diplomatic Service','Implement Negotiated Commitments'],
 [({'foreign_influence_defense_modifier':.06,'political_power_factor':-.02},{'political_power_factor':.04,'foreign_influence_defense_modifier':-.04}),({'army_org_factor':.03,'foreign_influence_defense_modifier':-.04},{'foreign_influence_defense_modifier':.07}),({'foreign_influence_defense_modifier':.03},{'production_speed_buildings_factor':.03})],icon='diplomacy')
common('cyprus','CYPRUS · GUARANTOR CHOICES & CRISIS RESPONSE',81,
 ['The Cyprus Policy Dossier','Review the Officer Mission','Support the Civilian Guard','Encourage the Coup Networks','A Written Non-Interference Protocol','Submit a Covert Sponsorship Proposal','Record the Actual Mission Outcome','Ankara and Nicosia Must Respond','Offer a Guarantor Conference','Prepare a National Contingency','Send the Negotiating Instructions','Verify Greek Mobilisation Capacity','A Joint Crisis Record','Support an Implemented Ceasefire','Retain an Armed Posture','Propose Monitored Separation','Prepare Defensive Sustainment','Record the Outcome without Rewriting It','Civilian Relief and Missing Persons','Reconstruction with Accountability'],
 [({'army_org_factor':.03,'foreign_influence_defense_modifier':.03},{'political_power_factor':.03,'stability_factor':-.04}),({'foreign_influence_defense_modifier':.03},{'max_planning':.04,'production_speed_buildings_factor':-.03}),({'stability_factor':.04},{'army_org_factor':.03,'social_cost_multiplier_modifier':.04})],icon='cyprus',note='No automaticCyprus coup, Turkish intervention, enosis, ceasefire or border change. All foreign seats retain their decisions.')

# Targeted rewards and outcome contracts override generic programme scaffolding.
by={n['key']:n for n in nodes}
for key,state,kind,level in [('economy_16',143,'naval_base',1),('navy_10',141,'dockyard',1),('air_15',144,'air_base',1),('economy_18',139,'infrastructure',1)]:
    by[key]['building']={'state':state,'type':kind,'level':level,'instant_build':False}
    if kind=='naval_base':by[key]['building']['province']=10007
    by[key]['requirements']+=' Own AND control the state; native building cap and slot checks; one queue entry only.'
    by[key]['note']+=' Adds normal construction to the queue, never a free completed building.'
    by[key]['treasury_cost_gdp_percent']=1.5;by[key]['days']=56;by[key]['focus_cost']=8
for key,kind,amount in [('army_4','army',15),('army_5','army',15),('navy_4','navy',20),('navy_5','navy',20),('air_4','air',15),('air_5','air',15)]:by[key]['xp']=[kind,amount]
for key in ['army_16','air_11','foreign_10','foreign_15','foreign_16','foreign_19']:
    by[key]['event_contract']='Submit a named bilateral proposal. Counterpart chooses accept, negotiate, defer or refuse. Pay agreed costs and grant only the implemented domestic share once.'
    by[key]['execution_mode']='proposal';by[key]['modifiers']={};by[key]['political_power']=0
for i in range(20):
    n=by['cyprus_'+str(i)]
    n['modifiers']={};n['political_power']=0;n['stability']=0;n['treasury_cost_gdp_percent']=0
    n['execution_mode']='proposal' if i in (2,3,4,5,8,10,13,15) else 'event_milestone' if i in (6,7,12,17) else 'normal'
    n['event_contract']='A focus is a proposal or record, never foreign consent. GRE/TUR/CYP/ENG each answer in their own scope. Decline and timeout are distinct outcomes. Outcome flags are not rewards.'
    n['requirements']='Actual current crisis phase and counterpart eligibility, not a July1974 calendar gate. Early and late alternate-history crises are possible.'
    n['note']='Fast crisis responses resolve immediately in country-scoped events. If used, complete the matching record focus without paying a second reward.'
for i in (6,7,12,17):
    by['cyprus_'+str(i)]['prerequisite_groups']=[]
    by['cyprus_'+str(i)]['requirements']+=' Require the matching observed outcome flag; bypass never counts as acceptance.'
for a,b in [(2,3),(8,9),(13,14)]:
    # Crisis posture can change after real events; do not hard-lock diplomacy
    # forever after mobilisation. Visual links retain a clear choice marker.
    by['cyprus_'+str(a)]['choice_scope']='current crisis phase; reviewed after a material event'
    by['cyprus_'+str(b)]['choice_scope']='current crisis phase; reviewed after a material event'
    by['cyprus_'+str(a)]['excludes']=[]
    by['cyprus_'+str(b)]['excludes']=[]
by['cyprus_3']['requirements']+=' Only the appropriate authoritarian leadership AND actual Greek authorisation and Cypriot participation; no direct force-government effect.'
by['cyprus_2']['title']='Support Civilian Control of the Guard'
by['cyprus_7']['event_contract']='GRE, TUR, CYP and ENG retain separate pending/accepted/refused/timed-out statuses. The first real guarantor response records the response milestone; a bilateral measure additionally needs the actual affected Cypriot party’s consent. Silence is never agreement.'
by['cyprus_4']['note']='Reduces coup pressure only after actual non-interference implementation. Hook: existingCYPwar_civilian_guard / officer-withdrawal contract.'
by['cyprus_5']['note']='Hook: existingCYPwar_plot / gre_authorized_coup. Sponsorship is not a successful coup; military support and the consequences are not free.'
by['cyprus_7']['title']='Record the First Guarantor Response'
by['cyprus_7']['note']='Only the first real guarantor response completes this response record. Each other seat retains a separate pending/accepted/refused/timed-out status. Separate Greek conference/contingency choices unlock after a bounded unanswered window; silence never completes this record or supplies foreign consent.'
for key in ('cyprus_8','cyprus_9'):
    by[key]['prerequisite_groups']=[]
    by[key]['observed_from']=[P+'cyprus_7']
by['cyprus_18']['treasury_cost_gdp_percent']=.8
by['cyprus_18']['note']='Relief activates only after actual civilian harm/displacement. Verify recipients and distribute funds once; never pay both Greek and Cyprus ledgers for the same invoice.'
by['cyprus_19']['treasury_cost_gdp_percent']=1.5
by['cyprus_19']['note']='Reconstruction/claims require an implemented settlement, local ownership/consent and recorded damage. Repression cannot remove civilian-harm penalties.'
for index,origins in {6:[4,5],7:[6],12:[10,11],17:[15,16]}.items():
    by['cyprus_'+str(index)]['observed_from']=[P+'cyprus_'+str(i) for i in origins]
for a,b in [(2,3),(8,9),(13,14)]:
    by['cyprus_'+str(a)]['revisable_with']=[P+'cyprus_'+str(b)]
    by['cyprus_'+str(b)]['revisable_with']=[P+'cyprus_'+str(a)]
for key in ['nd_4','centre_4','opening_dummy']:
    if key in by:by[key]['removes']=['security_state']
by['army_6']['removes']=['politicised_officers']
by['economy_17']['removes']=['uneven_regions']
by['economy_18']['removes']=['administrative_clientelism']
by['foreign_6']['conditional_removals']=[{'spirit':'european_censure','when':'Human-rights benchmarks actually met AND the institution has actually restored relations.'}]
by['foreign_6']['note']='The dossier records either restored relations or continued censure. A refusal never blocks unrelated diplomacy. Remove EuropeanCensure only after actual rights reform and institutional acceptance; no automatic membership.'
by['nd_13']['title']='Reactivate the Association Framework'
by['nd_13']['note']+=' The1961EEC association already existed and was frozen after the1967coup; this reactivates it rather than inventing a new1970association.'
for n in nodes:
    if n['section']=='pasok':n['requirements']=n['requirements'].replace('Social-democratic government','An Andreas-led socialist government (mapped to the MD social-democratic slot)')
    if n['section']=='pap':n['note']+=' Papadopoulos is the regime’s controlling figure; Markezinis can be prime minister during the1973opening. Formal office and political control are distinct.'
    if n['section']=='royal':
        n['requirements']='Monarchist executive mandate and an active constitutional restoration process. The proposal may be rejected; a republican outcome remains valid.'
        if int(n['key'].split('_')[-1])>=7:n['requirements']+=' The restoration settlement has actually been ratified.'
        n['note']+=' Any monarchy-specific bonus is pending until the settlement is actually ratified; rejected restoration gives no royal powers.'
by['royal_6']['title']='Ratify a Constitutional Settlement'
by['royal_6']['event_contract']='A legitimate ratification can accept the proposed monarchy or retain a republic. Royal programme benefits require actual acceptance; defeat does not block the country’s civilian alternatives.'
by['royal_19']['title']='Renew the Constitutional Mandate'
for key,title,xy,cost,stability,notes in [
 ('pasok_return_narrow','Historically Narrow Return Eligibility',(-3,27),.5,.01,'The1982return decision restricted eligibility to refugees of Greek origin; the1985property law retained a related restriction. This is a restrictive policy with excluded refugees’ claims left unresolved. The smaller budget funds fewer actual claims, not an inherent benefit of ancestry.'),
 ('pasok_return_equal','Equal Return and Restitution',(3,27),1.0,.025,'An explicitly inclusive alternate policy covers otherwise excluded returnees. Requires funded processing, property verification and housing; does not claim the historical1982law treated every exile equally.')]:
    n=node(key,title,'pasok',xy,['pasok_18','pasok_19'],cost=cost,stability=stability,days=49,icon='constitution',requires='An Andreas-led government, an actual legal mandate and a documented return/restitution caseload. Earlier adoption is an alternate-history reform.',note=notes+' PACE Doc11356annexes reproduce translations; they are not authenticated original Gazette scans.')
    either(n,'pasok_18','pasok_19');n['party']=3;n['leader']='Andreas Papandreou'
exclusive('pasok_return_narrow','pasok_return_equal')

section('contingency','CONDITIONAL · ENERGY, CREDIT & ACCOUNTABILITY',42,107)
node('energy_shock','Respond to an Actual Oil Shock','contingency',(0,0),days=21,icon='electricity',requires='A world oil-price/supply shock or actual disruption is active; not a1970starting event.')
node('energy_ration','Targeted Fuel Rationing','contingency',(-3,2),['energy_shock'],{'production_speed_buildings_factor':-.03,'stability_factor':-.02},days=28,icon='electricity',note='Reduces the fuel-import burden but restricts domestic activity. Update the oil-shock package; do not stack full relief with the opposing choice.')
node('energy_diversify','Finance Supply Diversification','contingency',(3,2),['energy_shock'],cost=1.5,days=49,icon='electricity',event='A real supplier and transport route must accept the contract; no free imported fuel.')
exclusive('energy_ration','energy_diversify')
node('credit_review','Choose How to Fund the Gap','contingency',(0,4),days=28,icon='money',requires='A documented treasury/import-financing gap, not an automatically imposed recession.')
node('credit_taxes','Temporary Revenue Measures','contingency',(-3,6),['credit_review'],stability=-.02,days=28,icon='money',note='Use the existing tax/budget system with a defined sunset. No one-off fictitious GDP increase.')
node('credit_loan','Negotiate a Funded Credit Line','contingency',(3,6),['credit_review'],days=28,icon='money',event='Match lender treasury debit to Greek treasury/debt credit at actual acceptance. No minimum0.5billion helper hidden behind a2%-GDP label.')
exclusive('credit_taxes','credit_loan')
recovery=node('energy_recovery','Implement the Recovery Package','contingency',(0,8),['energy_ration','energy_diversify'],cost=.8,stability=.025,days=49,icon='industry',removes=['oil_shock'],requires='Actual verified supply recovery; funded domestic programme.')
either(recovery,'energy_ration','energy_diversify')
next(n for n in nodes if n['key']=='energy_ration')['spirit_changes']=[{'id':P+'oil_shock','operation':'replace','modifiers_after':{'production_speed_buildings_factor':-.04,'social_cost_multiplier_modifier':.04}}]
recovery['removes']+=['energy_ration_programme']
recovery['removes']+=['oil_shock_rationed']

aegean_review=ROOT/'tools/greece_1970_design/graph_history_review.json'
if aegean_review.exists():
    review=json.loads(aegean_review.read_text(encoding='utf-8'))
    package=review['aegean_section']
    section('aegean','AEGEAN · SURVEYS, RESTRAINT & NEGOTIATION',64,107)
    for a in package['focuses']:
        key=a['key'].removeprefix(P)
        n=node(key,a['title'],'aegean',(a['x']-64,a['y']-74),days=35,icon='cyprus',requires=a['conditions'],note=a['reward_intent']+' '+a['tradeoff_intent'])
        n['prerequisite_groups']=a['prerequisite_groups'];n['excludes']=a['excludes']
        n['event_contract']='Named counterpart responses remain independent. An answer or a bounded explicit no-response result records the outcome; no guaranteed treaty, war, oil deposit or legal victory.'
        n['execution_mode']='proposal' if key in ('aegean_2','aegean_5','aegean_6') else 'event_milestone' if key=='aegean_4' else 'normal'
        n['treasury_cost_gdp_percent']=.5 if key in ('aegean_1','aegean_3','aegean_6','aegean_7') else 0
        if key=='aegean_7':n['modifiers']={'naval_coordination':.02};n['modifier_slot']='aegean_readiness'

apply_gates(nodes,P)

# Allocate the shared national budget in the actual individual values, rather
# than promise bonuses that a hidden late clamp would discard. Starting spirits
# are not scaled. Replacement-slot totals are checked independently by reviewers.
scales={'production_speed_buildings_factor':.30,'production_factory_max_efficiency_factor':.35,'army_org_factor':.40,'air_mission_efficiency':.65}
for n in nodes:
    n['modifiers']={k:round(v*scales.get(k,1),4) for k,v in n['modifiers'].items()}

# Draft native effects expose proposed wrappers without claiming that they
# already exist in the installed mod. Every primitive is audited separately.
for n in nodes:
    reward=[]
    if n['political_power']:reward.append('add_political_power = '+str(n['political_power']))
    if n['stability']:reward.append('add_stability = '+str(n['stability']))
    if n['xp']:reward.append(n['xp'][0]+'_experience = '+str(n['xp'][1]))
    reward.extend(effect_lines(n,nodes,P))
    if n['modifiers']:
        if n['modifier_slot']:
            for other in nodes:
                if other['id']!=n['id'] and other.get('modifier_slot')==n['modifier_slot'] and other['modifiers']:
                    reward.append('remove_ideas = '+other['id']+'_programme')
        if n.get('duration_days'):
            reward.append('add_timed_idea = { idea = '+n['id']+'_programme days = '+str(n['duration_days'])+' } # NEW Greek idea; refresh the slot, never stack it')
        else:reward.append('add_ideas = '+n['id']+'_programme # NEW Greek idea; replace the previous idea in this policy slot')
    for change in n.get('spirit_changes',[]):
        if change['operation']=='replace':
            replacement=change['id']+'_rationed'
            reward.append('swap_ideas = { remove_idea = '+change['id']+' add_idea = '+replacement+' } # NEW partial-shock idea; modifiers '+str(change['modifiers_after']))
    for r in n['removes']:reward.append('remove_ideas = '+P+r+' # only after the stated implementation gate')
    if n['building']:
        b=n['building'];reward.append(str(b['state'])+' = { add_building_construction = { type = '+b['type']+' level = '+str(b['level'])+(' province = '+str(b['province']) if 'province' in b else '')+' instant_build = no } } # ownership/control/capacity rechecked')
    if n['event_contract']:reward.append('# NEW Greek proposal/outcome adapter required. Reuse native country_event and guarded flags; no remote commands or automatic consent.')
    if not reward:reward.append('# Record the implemented milestone once; no extra reward.')
    payload='\n'.join(reward)
    if n['treasury_cost_gdp_percent']:
        fraction=n['treasury_cost_gdp_percent']/100
        payload=('set_temp_variable = { GRE_programme_cost = gdp_total }\nmultiply_temp_variable = { GRE_programme_cost = '+str(fraction)+' }\nif = {\n limit = { check_variable = { gdp_total > 0 } check_variable = { var = treasury value = GRE_programme_cost compare = greater_than_or_equals } }\n set_temp_variable = { treasury_change = GRE_programme_cost }\n multiply_temp_variable = { treasury_change = -1 }\n modify_treasury_effect = yes\n '+payload.replace('\n','\n ')+'\n set_country_flag = '+n['id']+'_granted\n}\nelse = { set_country_flag = '+n['id']+'_awaiting_funding }')
    else:payload+='\nset_country_flag = '+n['id']+'_granted'
    n['reward_code']='if = {\n limit = { NOT = { has_country_flag = '+n['id']+'_granted } }\n '+payload.replace('\n','\n ')+'\n}\n# Proposed adapter must also recheck actual implementation and slot ceilings before grants.'
    n['available_code']='original_tag = GRE\nIMP_is_1970_scenario = yes\n# '+n['requirements']
    if n.get('actual_outcome_flag'):
        n['available_code']+='\nhas_country_flag = '+P+n['actual_outcome_flag']+' # NEW factual domestic outcome, never a calendar flag'
    if n.get('required_regime_flags'):
        flags=['has_country_flag = '+P+key for key in n['required_regime_flags']]
        n['available_code']+='\n'+(flags[0] if len(flags)==1 else 'OR = { '+' '.join(flags)+' }')
    for key in n.get('required_completed_focus',[]):
        n['available_code']+='\nhas_completed_focus = '+P+key
    if n.get('required_active_idea'):
        n['available_code']+='\nhas_idea = '+P+n['required_active_idea']
    if 'party' in n:
        names=[x.strip() for x in n['leader'].split('/')]
        gates=['has_country_leader = { name = "'+name+'" ruling_only = yes }' for name in names]
        n['available_code']+='\ncheck_variable = { ruling_party = '+str(n['party'])+' }'
        if n['section'] in ('nd','centre','pasok'):
            n['available_code']+='\nhas_country_flag = '+P+'current_electoral_mandate_verified # actual current civilian winner; cleared when mandate ends'
        if n['section']!='royal':n['available_code']+='\n'+(gates[0] if len(gates)==1 else 'OR = { '+' '.join(gates)+' }')
        else:
            n['available_code']+='\nhas_country_flag = '+P+'restoration_process_authorised # NEW domestic mandate flag'
            if int(n['key'].split('_')[-1])>=7:n['available_code']+='\nhas_country_flag = '+P+'monarchy_restored # actual ratification, never a calendar action'
    if n['section']=='cyprus':
        n['available_code']+='\ncountry_exists = CYP'
        observed={6:'coup_attempt_resolved',7:'guarantor_response_recorded',12:'settlement_talks_open',17:'final_settlement_implemented'}
        if n['key'] in ['cyprus_'+str(i) for i in observed]:
            index=int(n['key'].split('_')[-1]);existing='CYP = { has_country_flag = COLDWAR_CYP_1970_'+observed[index]+' }'
            alternatives={6:'has_country_flag = '+P+'civilian_control_protocol_implemented has_country_flag = '+P+'mission_proposal_refused',12:'has_country_flag = '+P+'crisis_diplomatic_status_recorded',17:'CYP = { has_country_flag = COLDWAR_CYP_1970_second_phase_combat } has_country_flag = '+P+'unresolved_crisis_recorded'}
            n['available_code']+='\n'+(existing if index==7 else 'OR = { '+existing+' '+alternatives[index]+' }\n# GRE alternatives are NEW factual outcome flags set only by the proposed crisis adapter; never foreign consent.')
        if n['key'] in ('cyprus_8','cyprus_9'):
            n['available_code']+='\nOR = { has_completed_focus = '+P+'cyprus_7 has_country_flag = '+P+'response_window_closed }\n# A closed unanswered window unlocks Greek choices, not a foreign consent/response record.'
        if n['key'] in ('cyprus_3','cyprus_5'):
            n['available_code']+='\ncheck_variable = { ruling_party = 22 }\n# Actual domestic Greek authorisation and Cypriot participation rechecked by the proposed adapter.'
    if n['section']=='contingency':
        n['available_code']+='\n'+(('OR = { has_idea = '+P+'oil_shock has_idea = '+P+'oil_shock_rationed }' if n['key']=='energy_recovery' else 'has_idea = '+P+'oil_shock') if n['key'].startswith('energy_') else 'has_country_flag = '+P+'financing_gap_verified # NEW Greek outcome flag, not a pre-existing engine trigger')
    n.setdefault('party',None)
    for field in ('title','note','requirements','event_contract'):
        n[field]=re.sub(r'(?<=[A-Za-z])(?=19\d{2})',' ',n[field])
    n['idea_definition']='modifier = { '+' '.join(k+' = '+str(v) for k,v in n['modifiers'].items())+' }' if n['modifiers'] else ''
    n['effect_mode']='proposed new Greek wrapper around existing native/MD primitives; not installed runtime'

data={'country':'GRE','start':'1970.1.1','prefix':P,'focuses':nodes,'sections':sections,'routes':routes,'starting_spirits':spirits,'regime_packages':regime_packages,
 'rules':['English localisation only.','All political focuses require the actual governing party/leader, not merely an outlook.','Programme bonuses occupy replacement slots; parties cannot stack seven governments’ institutional/economic bonuses.','No forced coups, wars, treaty changes or guaranteed foreign acceptance. Only Cyprus AI follows the separate dedicated historical path.','Seven days per native focus point. All numeric effects are balance proposals, not historical measurements.','No foreign factories, aircraft, resources, loans or alliance memberships appear without actual contract implementation.','Cyprus and Aegean civilian harm is conditional, recorded once and not erased by coercion.'],
 'balance_caps':{'construction_programmes':.15,'factory_efficiency_programmes':.12,'army_organisation_programmes':.12,'air_mission_programmes':.12,'research_programmes':.115,'maximum_planning_programmes':.18,'policy':'Individual effects are allocated below these budgets under replacement slots and at most one active government programme. No hidden payoff clamp.'},
 'sources':['https://history.state.gov/historicaldocuments/frus1969-76v29/d314','https://70.coe.int/1969-greece-withdraws-en.html','https://pasok.gr/history/'],
 'state_reference':{'139':'Thessaly','140':'SouthernMacedonia','141':'CentralGreece','142':'Peloponnese','143':'AegeanIslands','144':'Crete','974':'WestThrace','1062':'IonianIslands'},
 'status':'DESIGN ONLY. No Greek runtime tree, starting spirit or foreign-event adapter installed by this build.'}
ids={n['id'] for n in nodes};assert len(ids)==len(nodes)
assert len({(n['x'],n['y']) for n in nodes})==len(nodes),'Coordinate collision'
for n in nodes:
    for g in n['prerequisite_groups']:
        assert g and all(p in ids for p in g)
        assert all(next(a for a in nodes if a['id']==p)['y']<n['y'] for p in g)
    assert all(e in ids for e in n['excludes'])
    assert abs(n['focus_cost']*7-n['days'])<.001
out=HERE/'coldwar_greece_1970_design.json';out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'proposed_scripted_effects.txt').write_text(proposed_effects(nodes,P),encoding='utf-8')
(HERE/'GRAPH_QA.json').write_text(json.dumps({'focuses':len(nodes),'sections':len(sections),'political_routes':7,'coordinate_collisions':0,'exclusive_pairs':sum(len(n['excludes']) for n in nodes)//2,'focus_point_days':7,'runtime_installed':False},indent=2)+'\n')
print(json.dumps({'focuses':len(nodes),'sections':len(sections),'routes':Counter(n['section'] for n in nodes)}))
