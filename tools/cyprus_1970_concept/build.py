# IMPERIA COLD WAR — Compact Cyprus replacement concept, October 2026.
"""Design artifacts only. Never emits or changes loaded game files."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import base64, hashlib, html, io, json, math, re
from intervention import extend as extend_intervention, document as intervention_document

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/cyprus_1970_rework_20261027'
VIS = Path('C:/Users/Enes/.codex/visualizations/2026/10/27/01a17ef0-dd9d-7a11-b0e5-985305e237a1')
PREFIX = 'COLDWAR_CYP_R2_'
OUT.mkdir(parents=True, exist_ok=True)

GROUPS = [
 ('constitution','Constitution',8,0,12), ('community','Two Communities',24,0,12),
 ('crisis','Road to War',40,0,10), ('economy','Development',58,0,14),
 ('defence','National Defence',76,0,10), ('diplomacy','Foreign Agreements',92,0,6),
 ('centre','Presidential Centre',16,11,12), ('liberal','Eniaion',44,11,12),
 ('akel','AKEL',72,11,12)]
PARTIES = {'centre':(1,'western_conservatism_are_in_power'),
           'liberal':(2,'western_liberals_are_in_power'),
           'akel':(4,'emerging_communist_state_are_in_power')}
LABELS = {
 'stability_factor':'Stability','political_power_factor':'Political power gain',
 'research_speed_factor':'Research speed','army_org_factor':'Army organization',
 'training_time_factor':'Unit training time','army_defence_factor':'Army defence',
 'army_attack_factor':'Army attack','war_support_factor':'War support',
 'production_speed_buildings_factor':'Construction speed',
 'production_speed_industrial_complex_factor':'Civilian factory construction',
 'production_speed_infrastructure_factor':'Infrastructure construction',
 'industrial_capacity_factory':'Military factory output',
 'production_factory_max_efficiency_factor':'Production efficiency cap',
 'bureaucracy_cost_multiplier_modifier':'Bureaucracy cost',
 'education_cost_multiplier_modifier':'Education cost',
 'health_cost_multiplier_modifier':'Health cost',
 'office_park_income_tax_modifier':'Office sector tax income',
 'agricolture_productivity_modifier':'Agricultural productivity',
 'foreign_influence_defense_modifier':'Foreign influence defence',
 'special_forces_cap':'Special forces capacity',
 'special_forces_training_time_factor':'Special forces training time'}

F=[]
def mod(spirit, **values): return {'type':'modifier_delta','spirit':spirit,'values':values}
def building(state, name, levels=1, province=None):
 return {'type':'building','state':state,'building':name,'levels':levels,'shared_slots':levels,'province':province}
def bonus(category, amount=.5, uses=1): return {'type':'research','category':category,'bonus':amount,'uses':uses}
def doctrine(amount=.5, uses=1): return {'type':'doctrine','category':'land_doctrine','bonus':amount,'uses':uses}
def event(title, recipients): return {'type':'country_event','title':title,'recipients':recipients}
def remove(name): return {'type':'remove_spirit','name':name}
def change(name, amount): return {'type':'crisis_value','name':name,'amount':amount}
def pp(value): return {'type':'political_power','value':value}
def xp(value): return {'type':'army_experience','value':value}
def offer(key): return {'type':'offer','key':key}
def temp(spirit, days, **values): return {'type':'temporary_spirit','spirit':spirit,'days':days,'values':values}
def add(group,key,title,x,y,pre=(),ex=(),effects=(),cost=5,setup=0,weekly=0,req='',desc='',source='politics'):
 # pre is a sequence of OR groups; distinct groups are AND.
 if isinstance(pre,str): pre=[[pre]]
 else: pre=[[v] if isinstance(v,str) else list(v) for v in pre]
 anchor=next(g for g in GROUPS if g[0]==group)
 prior_root=next((f for f in F if f['group']==group),None)
 F.append(dict(id=PREFIX+key,key=key,title=title,group=group,x=anchor[2]+x,y=anchor[3]+y,
  offset=[x,y],anchor=prior_root['id'] if prior_root else None,
  emitted_xy=[x,y] if prior_root else [anchor[2]+x,anchor[3]+y],prerequisites=pre,exclusive=list(ex),
  cost=cost,days=round(cost*7),setup_gdp_percent=setup,weekly_gdp_percent=weekly,
  requirements=req,description=desc,effects=list(effects),source=source,
  party_trigger=PARTIES.get(group,(None,None))[1],party_slot=PARTIES.get(group,(None,None))[0]))

# Constitution: presidential legitimacy and constitutional partnership are different questions.
add('constitution','republic','The Republic at Ten',0,0,effects=[mod('Republican Institutions',foreign_influence_defense_modifier=.05),pp(35)],cost=2.5,
 desc='The republic has survived its first decade, but its common institutions no longer command the confidence of both communities. Independence needs a functioning political settlement as well as international recognition.')
add('constitution','cabinet','Cabinet Responsibility',0,1,'republic',effects=[mod('Republican Institutions',political_power_factor=.05,bureaucracy_cost_multiplier_modifier=.03)],setup=.25,
 desc='A cabinet answerable for security, expenditure and negotiations can reduce the personal burden on the presidency. A stronger centre also needs a larger permanent secretariat.')
add('constitution','mediation','Presidential Mediation',-3,3,'cabinet',['scrutiny'],[mod('Republican Institutions',political_power_factor=.10,stability_factor=.05,bureaucracy_cost_multiplier_modifier=.05)],
 desc='Makarios can arbitrate between parliamentary allies, the Church and the security services. Personal authority accelerates decisions but leaves oversight dependent on the presidency.')
add('constitution','scrutiny','Parliamentary Scrutiny',3,3,'cabinet',['mediation'],[mod('Republican Institutions',political_power_factor=-.05,stability_factor=.10,bureaucracy_cost_multiplier_modifier=-.05)],
 desc='Stronger parliamentary scrutiny can build confidence in public decisions. Ministers must accept slower negotiations and less freedom to govern through presidential understandings.')
add('constitution','church_talks','Church Mediation',-3,5,'mediation',effects=[mod('Republican Institutions',foreign_influence_defense_modifier=.10,education_cost_multiplier_modifier=.05)],
 desc='The Orthodox Church has land, schools and an authority that reaches beyond party organizations. Its mediation can protect independence while reinforcing expectations of public support for religious institutions.')
add('constitution','audit','Independent Audit Office',3,5,'scrutiny',effects=[mod('Republican Institutions',bureaucracy_cost_multiplier_modifier=-.10)],setup=.75,
 desc='An independent audit office will examine procurement and public contracts. The initial expense buys administrative savings while the parliamentary route retains its slower political bargaining.')
add('constitution','ballot','Protect the Ballot',0,7,[['church_talks','audit']],effects=[mod('Republican Institutions',stability_factor=.05),change('Communal confidence',5)],setup=.25,
 desc='Electoral competition must not become a contest over who controls the police or the polling station. Protected campaigning and impartial administration can make lawful opposition credible.')
add('constitution','conference','Constitutional Talks',0,8,'ballot',effects=[mod('Republican Institutions',political_power_factor=.03,bureaucracy_cost_multiplier_modifier=.03),change('Communal confidence',5)],req='Communal confidence at least 40.',
 desc='Representatives of both communities must debate executive powers, representation and security. Opening a conference commits the government to negotiations without deciding their result.')
add('constitution','restore_1960','The 1960 Balance',-3,10,'conference',['new_compact'],[mod('Constitutional Settlement',foreign_influence_defense_modifier=.10,political_power_factor=-.05)],setup=.5,req='Communal confidence at least 65. Proposed safeguards receive a communal response event.',
 desc='A repaired partnership can retain the constitutional framework of independence. Restored vetoes and communal protections constrain executive action in exchange for stronger guarantees.')
add('constitution','new_compact','A Federal Compact',3,10,'conference',['restore_1960'],[mod('Constitutional Settlement',stability_factor=.08,bureaucracy_cost_multiplier_modifier=.10)],setup=.75,req='Communal confidence at least 65. Both delegations and all treaty parties receive response events.',
 desc='A negotiated federal settlement can distribute powers more explicitly between a common government and communal authorities. The additional institutions impose a lasting administrative cost.',source='settlement')
add('constitution','rights','Guaranteed Communal Rights',0,12,[['restore_1960','new_compact']],effects=[mod('Constitutional Settlement',stability_factor=.05),change('Communal confidence',10)],req='The selected constitutional agreement is ratified by both communal delegations.',
 desc='Rights to representation, worship, education and legal protection must survive changes of government. Their enforcement will be entrusted to institutions accepted by both communities.',source='settlement')
add('constitution','endure','A Republic That Endures',0,13,'rights',effects=[remove('Broken Constitutional Partnership'),pp(75)],req='The agreed institutions operate and the country is at peace.',
 desc='The republic can replace emergency improvisation with an accepted constitutional order. The settlement does not erase political disagreement or transfer territory by decree.',source='settlement')

# Community choices represent institutions and restrictions, never an ethnic workforce malus.
add('community','talks','Resume the Talks',0,0,effects=[change('Communal confidence',10),mod('Communal Arrangements',bureaucracy_cost_multiplier_modifier=.02)],cost=2.5,
 desc='Clerides and Denktash have been conducting intercommunal talks since 1968. A permanent liaison channel can keep local disputes from becoming another general confrontation.',source='community')
add('community','passage','Safe Civilian Passage',-3,2,'talks',['checkpoints'],[mod('Communal Arrangements',production_speed_buildings_factor=.05,bureaucracy_cost_multiplier_modifier=.03),change('Communal confidence',10)],setup=.25,
 desc='Agreed routes for workers, patients and goods can reconnect communities. Liaison staff and supervised crossings cost money and require security services to relinquish some discretion.',source='community')
add('community','checkpoints','Retain Security Checks',3,2,'talks',['passage'],[mod('Communal Arrangements',army_defence_factor=.05,production_speed_buildings_factor=-.03),change('Communal confidence',-5)],
 desc='Security checkpoints can reassure exposed villages and preserve inspection powers. They also obstruct ordinary commerce and deepen suspicion of the central government.',source='community')
add('community','clinics','Joint Medical Access',-3,4,'passage',effects=[mod('Communal Arrangements',stability_factor=.05,health_cost_multiplier_modifier=.05),change('Communal confidence',10)],setup=.25,
 desc='Access to hospitals and emergency treatment can become a practical common interest. The state must fund transport, interpreters and care without discriminatory restrictions.',source='community')
add('community','liaison','Local Security Liaison',3,4,'checkpoints',effects=[mod('Communal Arrangements',army_org_factor=.05,bureaucracy_cost_multiplier_modifier=.05),change('Communal confidence',5)],
 desc='Joint incident reporting can improve security without pretending that the communities already share a trusted command structure. Separate liaison offices will remain an administrative burden.',source='community')
add('community','utilities','Reconnect Utilities',0,6,[['clinics','liaison']],effects=[building(146,'infrastructure'),change('Communal confidence',10)],setup=1,req='The state is owned and controlled. Both communal delegations accept the works.',
 desc='Electricity, water and road access should not depend on bargaining at every local checkpoint. A supervised infrastructure programme can improve services while leaving constitutional claims for negotiation.',source='economy')
add('community','municipal','Shared Municipal Funds',-3,8,'utilities',['autonomy'],[mod('Communal Arrangements',production_speed_buildings_factor=.08,bureaucracy_cost_multiplier_modifier=.05)],weekly=.002,req='Both communal delegations accept the municipal funding terms.',
 desc='A common fund can direct investment to neglected districts under joint supervision. Reliable funding reduces local uncertainty but creates an enduring budget commitment.',source='community')
add('community','autonomy','Communal Administration',3,8,'utilities',['municipal'],[mod('Communal Arrangements',stability_factor=.08,political_power_factor=-.05)],setup=.5,req='Both communal delegations accept the division of local powers.',
 desc='Recognized communal administrative powers may provide security without demanding immediate institutional integration. The common government must accept a narrower field of direct authority.',source='settlement')
add('community','accountability','Joint Accounts',-3,10,'municipal',effects=[mod('Communal Arrangements',bureaucracy_cost_multiplier_modifier=-.05),change('Communal confidence',5)],setup=.25,
 desc='Published accounts can show how communal funds are divided and used. Common supervision makes future investment easier to defend to taxpayers in both communities.',source='community')
add('community','representation','Return to Representation',3,10,'autonomy',effects=[mod('Communal Arrangements',political_power_factor=.05),change('Communal confidence',5)],req='Both communal delegations accept their representation arrangements.',
 desc='Reserved representation cannot become effective through a unilateral appointment. Negotiated participation must give the Turkish Cypriot community a credible voice in shared decisions.',source='settlement')
add('community','movement','An Island of Open Routes',0,12,[['accountability','representation']],effects=[remove('Separate Communal Administrations'),mod('Communal Arrangements',production_speed_buildings_factor=.03)],req='Communal confidence at least 65. Both delegations accept the mobility and administrative settlement.',
 desc='A durable mobility agreement can remove the economic penalties of fragmentation. It requires functioning local guarantees rather than an assertion that the communal dispute has disappeared.',source='community')
add('community','safeguards','Enforce the Safeguards',0,13,'movement',effects=[mod('Communal Arrangements',stability_factor=.05,bureaucracy_cost_multiplier_modifier=.03),change('Communal confidence',5)],
 desc='A standing review commission can investigate violations and preserve confidence when a government changes. The commission adds expense but gives ordinary grievances a lawful remedy.',source='settlement')

# Road to war: exclusive focus preparations, with only immediate country-event responses.
add('crisis','officers','The Officer Question',0,0,effects=[mod('Command Settlement',army_org_factor=.03,bureaucracy_cost_multiplier_modifier=.03),pp(35)],cost=2.5,
 desc='Greek officers provide military expertise while Athens is ruled by a junta. The presidency must decide how much of the National Guard command it can safely leave dependent on an external government.',source='security')
add('crisis','cypriot_command','Cypriot Command',-3,2,'officers',['greek_mission'],[change('Officer penetration',-15),temp('Command Reorganization',90,army_org_factor=-.05),mod('Command Settlement',training_time_factor=.05)],setup=.5,
 desc='Replacing exposed commanders can strengthen loyalty to the republic. The change disrupts existing chains of command and slows training while Cypriot officers gain experience.',source='security')
add('crisis','greek_mission','Retain Greek Missions',3,2,'officers',['cypriot_command'],[offer('greek_training')],
 desc='A renewed Greek training mission can improve the Guard quickly. Acceptance leaves Cyprus dependent on officers whose government may pursue a different political objective.',source='alliance')
add('crisis','police','Police Counterweights',-3,4,'cypriot_command',effects=[mod('Command Settlement',army_defence_factor=.05,bureaucracy_cost_multiplier_modifier=.05),change('Officer penetration',-10)],setup=.5,weekly=.002,
 desc='A lawful police reserve can prevent the Guard from monopolizing armed power. Rival chains of command must be coordinated and supported from the public budget.',source='security')
add('crisis','military_terms','Military Terms in Writing',3,4,'greek_mission',effects=[doctrine(.25),change('Officer penetration',-5)],req='The Greek Training Mission agreement is active.',
 desc='Written terms for postings, training and withdrawal can moderate dependence on Greek officers. The agreement improves accountability while retaining the mission and its political risks.',source='alliance')
add('crisis','networks','Expose Armed Networks',0,6,[['police','military_terms']],effects=[change('Officer penetration',-10),temp('Security Investigations',90,stability_factor=-.03)],setup=.25,
 desc='Investigations can disrupt clandestine violence, including the National Front and later EOKA B. Arrests and searches also risk polarizing Greek Cypriot politics.',source='security')
add('crisis','consult','Consult the Guarantors',-3,8,'networks',effects=[event('Guarantor Consultations',['GRE','TUR','ENG'])],
 desc='The Treaty of Guarantee calls for consultation when its obligations are threatened. Greece, Turkey and Britain must each choose whether to cooperate in restoring constitutional government.',source='guarantee')
add('crisis','emergency','Presidential Contingency',3,8,'networks',effects=[change('Presidential preparedness',25),mod('Command Settlement',foreign_influence_defense_modifier=.05)],setup=.25,
 desc='A protected communications network and clear succession orders can help the legal government survive a sudden attack. Preparedness is useful only if loyal institutions act when the crisis comes.',source='security')
add('crisis','civilian_rule','Restore Civilian Rule',-3,10,[['consult','emergency']],effects=[remove('Divided National Guard Command'),remove('Enosis Underground Networks'),mod('Command Settlement',political_power_factor=.05)],req='The coup threat is resolved. Cyprus has a civilian government and is at peace.',
 desc='A failed coup or a negotiated restoration must be followed by a command settlement and the dismantling of armed political networks. Neither a calendar date nor a foreign promise is enough.',source='security')
add('crisis','geneva','The Geneva Conference',3,10,[['consult','emergency']],effects=[event('Ceasefire and Constitutional Restoration',['GRE','TUR','ENG']),mod('Command Settlement',stability_factor=.03,bureaucracy_cost_multiplier_modifier=.03)],req='A guarantor crisis, coup or armed conflict has actually occurred.',
 desc='A crisis conference can seek a ceasefire, constitutional restoration and practical guarantees. If negotiations fail, the involved states retain control over their next military and diplomatic choices.',source='1974')

# Development reflects a growing pre-war economy, not a fictitious collapsed 1970 state.
add('economy','plan','Complete the Second Plan',0,0,effects=[bonus('CAT_industry',.5),mod('Development Policy',production_speed_buildings_factor=.05)],setup=.5,cost=2.5,
 desc='The Second Five-Year Plan has supported roads, utilities and productive investment. Completing its priorities can sustain the growth already achieved during the 1960s.',source='economy')
add('economy','technical','Technical Institutes',0,1,'plan',effects=[remove('Limited Technical Capacity'),bonus('CAT_industry',.5)],setup=.75,weekly=.002,
 desc='A small island needs engineers, technicians and administrators as well as labour. Technical institutes address specialist shortages through education rather than restricting the national workforce.',source='economy')
add('economy','tourism','A Visitor Economy',-3,3,'technical',['workshops'],[mod('Development Policy',office_park_income_tax_modifier=.12,production_speed_buildings_factor=.05)],setup=.75,req='Cyprus is at peace.',
 desc='Hotels and visitor services can earn foreign exchange and employ a growing urban population. Concentrating investment on visitors increases the losses the island suffers during a security crisis.',source='economy')
add('economy','workshops','Export Workshops',3,3,'technical',['tourism'],[building(145,'industrial_complex'),mod('Development Policy',industrial_capacity_factory=.08,office_park_income_tax_modifier=-.03)],setup=1.5,
 desc='Light manufacturing offers a different export base from tourism. Imported machinery and industrial priorities absorb capital that could otherwise support commercial services.',source='economy')
add('economy','coastal_services','Coastal Services',-3,5,'tourism',effects=[building(145,'offices'),mod('Development Policy',bureaucracy_cost_multiplier_modifier=.03)],setup=1.5,req='Owned and controlled state with native office capacity.',
 desc='Commercial offices and reliable public services can support the visitor economy. A larger service centre also requires municipal administration and exposes more revenue to interruption.',source='economy')
add('economy','industrial_standards','Industrial Standards',3,5,'workshops',effects=[mod('Development Policy',production_factory_max_efficiency_factor=.10),bonus('CAT_industry',.5)],setup=.5,
 desc='Standards, quality control and vocational instruction help small firms reach external markets. The programme consolidates the manufacturing route instead of duplicating the service investment.',source='economy')
add('economy','water','Water for the Island',0,7,[['coastal_services','industrial_standards']],effects=[building(145,'infrastructure'),mod('Development Policy',agricolture_productivity_modifier=.05)],setup=1,
 desc='Water storage and distribution protect agriculture and growing towns from seasonal shortages. The same investment can serve villages, exporters and the tourist economy.',source='economy')
add('economy','cooperatives','Rural Cooperatives',-3,9,'water',['commercial_credit'],[mod('Development Policy',agricolture_productivity_modifier=.12,bureaucracy_cost_multiplier_modifier=.05)],setup=.75,
 desc='Cooperatives can pool credit, storage and marketing for small producers. Public supervision and guarantees add fiscal responsibilities while broadening access to investment.',source='economy')
add('economy','commercial_credit','Commercial Credit',3,9,'water',['cooperatives'],[mod('Development Policy',office_park_income_tax_modifier=.08,production_speed_industrial_complex_factor=.10,stability_factor=-.03)],setup=.5,
 desc='Private credit can channel savings toward expanding businesses. A more selective commercial system favours profitable borrowers and leaves some small producers dissatisfied.',source='economy')
add('economy','land_improvement','Land Improvement',-3,11,'cooperatives',effects=[mod('Development Policy',agricolture_productivity_modifier=.08),building(146,'infrastructure')],setup=1,req='Owned and controlled state. Communal works agreement accepted.',
 desc='Irrigation and access works can raise rural output without taking communal land through administrative fiat. Projects in sensitive districts require the agreement of the affected representatives.',source='economy')
add('economy','small_firms','Small Firm Expansion',3,11,'commercial_credit',effects=[building(145,'industrial_complex'),bonus('CAT_industry',.5)],setup=1.5,
 desc='A second stage of investment can connect small firms to machinery and export finance. Its assets remain national gains even if a later government changes economic policy.',source='economy')
add('economy','ports','A Commercial Gateway',0,13,[['land_improvement','small_firms']],effects=[building(145,'naval_base',1,11984),mod('Development Policy',office_park_income_tax_modifier=.05)],setup=1,req='Province 11984 is owned and controlled, coastal and below its native naval-base cap.',
 desc='Improved port facilities can serve exports and essential imports. Reliable handling, storage and coastal access will support the commercial routes on which the island depends.',source='economy')
add('economy','recovery','Recovery and Housing',-9,9,'water',effects=[remove('Displaced Families'),building(145,'infrastructure')],setup=1.5,req='Actual displacement has occurred. The state is owned and controlled.',
 desc='If conflict disrupts the economy, housing, services and lost commercial links become urgent priorities. Relief must be directed toward the disruption that actually occurred.',source='1974')
add('economy','resilience','Reserves for a Crisis',9,9,'water',effects=[mod('Development Policy',foreign_influence_defense_modifier=.08,office_park_income_tax_modifier=-.03)],setup=1,req='Cyprus has not suffered the conflict damage addressed by Recovery and Housing.',
 desc='Emergency reserves and redundant supply contracts make peaceful development less vulnerable to pressure. Keeping resources in reserve reduces the return available from ordinary commercial investment.',source='economy')

# National defence: no free formations, no microstate superpower industry.
add('defence','guard','The National Guard',0,0,effects=[xp(15),bonus('CAT_infantry',.35)],cost=2.5,
 desc='The Guard needs training, communications and a command responsible to the republic. A modest defence programme must distinguish useful readiness from politically dangerous dependence.',source='security')
add('defence','territorial','Territorial Defence',-3,2,'guard',['mobile'],[mod('Defence Programme',army_defence_factor=.10,army_attack_factor=-.05)],setup=.5,
 desc='Local defensive plans can make a small force harder to dislodge from important positions. The resulting posture sacrifices offensive flexibility and cannot promise control of the sea.',source='security')
add('defence','mobile','Mobile Reserves',3,2,'guard',['territorial'],[mod('Defence Programme',army_org_factor=.10,training_time_factor=.10)],setup=.75,weekly=.002,
 desc='A trained mobile reserve can respond to threats before isolated positions are overwhelmed. It requires longer instruction and a continuing readiness budget.',source='security')
add('defence','positions','Prepared Positions',-3,4,'territorial',effects=[building(145,'bunker',1,11984),building(146,'coastal_bunker',1,7193)],setup=1,req='Both provinces are owned and controlled. Each fort is below its native cap.',
 desc='Limited fieldworks can protect selected approaches and landing sites. Their value depends on the forces available to hold them and on the geography represented by the current map.',source='security')
add('defence','signals','Signals and Logistics',3,4,'mobile',effects=[mod('Defence Programme',army_org_factor=.05),bonus('CAT_infantry',.5)],setup=.5,
 desc='Reliable communications and maintenance improve the usefulness of a reserve force. The programme favours coordination and endurance over additional formations.',source='security')
add('defence','infantry','Modern Infantry Training',0,6,[['positions','signals']],effects=[bonus('CAT_infantry',.5,2),xp(20)],setup=.5,
 desc='Infantry training and equipment standards must reflect the Guard that Cyprus can actually sustain. Modernization will improve existing forces without conjuring new divisions.',source='security')
add('defence','special','A Small Commando Arm',-3,8,'infantry',['civil_defence'],[mod('Defence Programme',special_forces_cap=.02,special_forces_training_time_factor=.10),doctrine(.35)],setup=.5,weekly=.002,
 desc='A small specialist arm can cover difficult terrain and demanding missions. Its soldiers require longer training and dedicated support, limiting how widely the model can be applied.',source='security')
add('defence','civil_defence','Civil Defence Network',3,8,'infantry',['special'],[mod('Defence Programme',stability_factor=.05,health_cost_multiplier_modifier=.05,army_defence_factor=.03)],setup=.5,weekly=.002,
 desc='Shelters, evacuation planning and medical coordination can reduce civilian exposure during a crisis. The network commits resources that cannot also fund a larger specialist force.',source='security')
add('defence','doctrine','A Cypriot Defence Doctrine',0,10,[['special','civil_defence']],effects=[doctrine(.5,2),xp(25)],setup=.5,
 desc='The Guard should train around the island, its available forces and its political obligations. A coherent doctrine can reconcile the selected defence posture with realistic national resources.',source='security')
add('defence','coast','Coastal Watch',0,12,'doctrine',effects=[bonus('CAT_naval',.5),mod('Defence Programme',army_defence_factor=.05,bureaucracy_cost_multiplier_modifier=.03)],setup=.5,
 desc='Coastal observation and civilian reporting can improve warning. They provide information to the Guard without pretending that Cyprus can build a great-power fleet.',source='security')

# Six foreign focuses plus the Greek mission create seven concrete consented agreements.
add('diplomacy','nonaligned','Non-Aligned Partners',0,0,effects=[offer('yugoslavia')],cost=2.5,
 desc='Cyprus and Yugoslavia share the diplomatic traditions of the Non-Aligned Movement. A technical and commercial arrangement can build on that connection without becoming a military alliance.',source='nonaligned')
add('diplomacy','bases','Base Area Arrangements',-3,2,'nonaligned',effects=[offer('britain')],
 desc='Civil access, employment and services around the British Sovereign Base Areas need practical agreements. Accommodation can protect livelihoods while leaving British sovereignty over the bases intact.',source='guarantee')
add('diplomacy','czech','Supervised Arms Supply',3,2,'nonaligned',effects=[offer('czechoslovakia')],
 desc='Czechoslovak supply offers an alternative source of equipment and expertise. UN inspection and agreed storage can reduce the resulting tension at the cost of secrecy and autonomy.',source='arms')
add('diplomacy','association','European Association',0,4,[['bases','czech']],effects=[offer('eec')],
 desc='Association can open commercial opportunities without granting Community membership. A trade agreement must secure the approval of the actual Community partners and preserve its negotiated conditions.',source='eec')
add('diplomacy','greek_civil','Civilian Greek Links',-3,6,'association',effects=[offer('greek_civil')],
 desc='Education and civilian technical cooperation with Greece need not place the Guard under political tutelage. Both governments must fund the exchange and accept its civilian character.',source='alliance')
add('diplomacy','turkish_pact','Guarantees with Turkey',3,6,'association',effects=[offer('turkey')],req='A communal safeguards agreement has been accepted by both communal delegations.',
 desc='A confidence agreement with Turkey can reduce external fears once communal guarantees are credible. It supplements Turkish Cypriot consent and cannot replace it.',source='settlement')

# Three substantial political programmes. All remain visible, and only the actual party governs them.
add('centre','presidential_service','Presidential Service',0,0,effects=[mod('Presidential Programme',political_power_factor=.10,bureaucracy_cost_multiplier_modifier=.05)],
 desc='The presidential centre can coordinate a broad coalition around independence. A stronger secretariat improves political direction but increases the cost of administration.')
add('centre','coalition','A Republican Coalition',0,1,'presidential_service',effects=[mod('Presidential Programme',stability_factor=.05,political_power_factor=.05,health_cost_multiplier_modifier=-.03,bureaucracy_cost_multiplier_modifier=.03)],
 desc='The presidential centre can propose a cooperation agreement with EDEK around independence and social provision. The parties must negotiate a common programme and preserve their distinct political organizations.')
add('centre','church_welfare','Church Social Covenant',-3,3,'coalition',['civil_service'],[mod('Presidential Programme',stability_factor=.08,health_cost_multiplier_modifier=-.05,education_cost_multiplier_modifier=.05)],setup=.5,
 desc='Parish institutions can help deliver social support and strengthen the presidency in rural society. Public cooperation also reinforces the Church role in education and public life.')
add('centre','civil_service','A Secular Civil Service',3,3,'coalition',['church_welfare'],[mod('Presidential Programme',research_speed_factor=.05,bureaucracy_cost_multiplier_modifier=-.08,political_power_factor=-.05)],setup=.75,
 desc='Professional recruitment can improve technical administration beyond confessional or personal networks. The reform weakens some of the political instruments on which a presidential coalition relies.')
add('centre','parish','Parish Relief Network',-3,5,'church_welfare',effects=[mod('Presidential Programme',health_cost_multiplier_modifier=-.05,stability_factor=.03)],weekly=.002,
 desc='Reliable parish relief can reach families outside the largest towns. Public funding formalizes the partnership while retaining the educational compromise of the social covenant.')
add('centre','merit','Merit Appointments',3,5,'civil_service',effects=[bonus('CAT_industry',.5),mod('Presidential Programme',bureaucracy_cost_multiplier_modifier=-.04)],setup=.5,
 desc='Technical appointments and open examinations can turn professional administration into a durable advantage. The presidency accepts the limits that impartial recruitment places on patronage.')
add('centre','independent','An Independent Presidency',0,7,[['parish','merit']],effects=[mod('Presidential Programme',foreign_influence_defense_modifier=.10),pp(50)],
 desc='The presidency can seek support abroad without placing Cyprus under a foreign political command. Independence remains a negotiating position that must be sustained through institutions and resources.')
add('centre','sovereignty','Sovereignty First',-3,9,'independent',['federal_centre'],[mod('Presidential Programme',foreign_influence_defense_modifier=.15,political_power_factor=.05),change('Communal confidence',-5)],
 desc='A firm central position can resist outside pressure and defend the recognized republic. It makes communal concessions harder to negotiate and reduces confidence in a shared settlement.')
add('centre','federal_centre','A Negotiated Centre',3,9,'independent',['sovereignty'],[mod('Presidential Programme',stability_factor=.08,production_speed_buildings_factor=.05,bureaucracy_cost_multiplier_modifier=.08),change('Communal confidence',10)],
 desc='The centre can invest its political authority in a bicommunal agreement. A more complex government may buy confidence and investment at a continuing administrative cost.',source='settlement')
add('centre','diplomatic_service','Diplomatic Service',-3,11,'sovereignty',effects=[mod('Presidential Programme',foreign_influence_defense_modifier=.10,bureaucracy_cost_multiplier_modifier=.03),bonus('CAT_industry',.35)],setup=.5,
 desc='A professional diplomatic service can broaden the republic external options. Representation abroad is a continuing administrative commitment, even when it protects room for manoeuvre.')
add('centre','settlement_fund','Settlement Investment',3,11,'federal_centre',effects=[building(145,'industrial_complex'),change('Communal confidence',5)],setup=1.5,req='The communal settlement is accepted and Cyprus is at peace.',
 desc='Investment linked to an accepted settlement can demonstrate that compromise produces tangible national gains. Construction remains conditional on control, capacity and the agreed safeguards.',source='settlement')
add('centre','succession','Constitutional Succession',0,13,[['diplomatic_service','settlement_fund']],effects=[mod('Presidential Programme',political_power_factor=.05,stability_factor=.05)],
 desc='The presidential centre needs lawful continuity beyond Makarios himself. A durable parliamentary organization and clear constitutional succession can preserve independence through a change of leadership.')

add('liberal','enterprise','Enterprise and Law',0,0,effects=[mod('Eniaion Economic Programme',office_park_income_tax_modifier=.08,stability_factor=-.02)],
 desc='Clerides centre-right current can support private enterprise under a republican legal order. Reforms favouring commercial initiative will face criticism over the distribution of their gains.')
add('liberal','institutions','Independent Institutions',0,1,'enterprise',effects=[mod('Eniaion Economic Programme',foreign_influence_defense_modifier=.05,bureaucracy_cost_multiplier_modifier=-.05)],setup=.5,
 desc='Predictable courts and professional administration can protect investment and lawful opposition. The reform depends on initial spending and limits discretionary political favours.')
add('liberal','open_capital','Open Capital Markets',-3,3,'institutions',['national_firms'],[mod('Eniaion Economic Programme',production_speed_industrial_complex_factor=.15,office_park_income_tax_modifier=.08,foreign_influence_defense_modifier=-.10)],setup=.5,
 desc='Foreign capital can finance expansion beyond the island limited savings. Greater reliance on outside investors also increases exposure to external political and commercial pressure.')
add('liberal','national_firms','National Enterprise',3,3,'institutions',['open_capital'],[mod('Eniaion Economic Programme',industrial_capacity_factory=.10,production_factory_max_efficiency_factor=.10,production_speed_buildings_factor=-.05)],setup=.75,
 desc='A domestic enterprise strategy can retain local control and improve production standards. Restricted access to outside capital slows the pace at which the building sector can expand.')
add('liberal','services','Commercial Services',-3,5,'open_capital',effects=[building(145,'offices'),mod('Eniaion Economic Programme',education_cost_multiplier_modifier=.03)],setup=1.5,
 desc='Professional services can complement tourism and external commerce. Their expansion increases demand for educated staff and should not be confused with an instant offshore-finance boom.')
add('liberal','supply_chains','Domestic Supply Chains',3,5,'national_firms',effects=[building(145,'industrial_complex'),bonus('CAT_industry',.5)],setup=1.5,
 desc='Local suppliers and common quality standards can strengthen manufacturing. Reliable contracts and technical training will help island firms compete for a greater share of export production.')
add('liberal','republican_right','The Republican Right',0,7,[['services','supply_chains']],effects=[mod('Eniaion Economic Programme',stability_factor=.05,political_power_factor=.05)],
 desc='A republican right can distinguish constitutional competition from coercive Enosis. Its support for independence leaves room for close cultural relations with Greece.')
add('liberal','pragmatism','Settlement Pragmatism',-3,9,'republican_right',['hard_guarantees'],[change('Communal confidence',10),mod('Eniaion Economic Programme',production_speed_buildings_factor=.08,political_power_factor=-.05)],
 desc='A negotiated settlement can reduce uncertainty for households and businesses. Compromise on communal powers has a political cost among voters seeking firmer national guarantees.',source='settlement')
add('liberal','hard_guarantees','Security Before Terms',3,9,'republican_right',['pragmatism'],[mod('Eniaion Economic Programme',army_defence_factor=.08,foreign_influence_defense_modifier=.10),change('Communal confidence',-5)],weekly=.002,
 desc='Negotiations can be conditioned on stronger security guarantees. The position supports defence and bargaining leverage while requiring more resources and delaying communal confidence.',source='security')
add('liberal','island_market','An Island-Wide Market',-3,11,'pragmatism',effects=[mod('Eniaion Economic Programme',office_park_income_tax_modifier=.08),bonus('CAT_industry',.5)],req='A mobility agreement is accepted by both communal delegations.',
 desc='Agreed access can make the island a larger effective market without requiring communities to abandon their institutions. Commercial benefits depend on the mobility settlement remaining credible.',source='community')
add('liberal','reserve_service','Reserve Service Standards',3,11,'hard_guarantees',effects=[doctrine(.5),mod('Eniaion Economic Programme',army_org_factor=.05,training_time_factor=.05)],setup=.5,
 desc='A capable reserve gives substance to demands for security. Longer training and continuing readiness remain part of the price of this approach.',source='security')
add('liberal','clerides','A Constitutional Alternative',0,13,[['island_market','reserve_service']],effects=[mod('Eniaion Economic Programme',political_power_factor=.05,stability_factor=.05)],
 desc='The movement around Clerides can become a lasting constitutional alternative to the presidential centre. Its programme connects private enterprise, a republican legal order and a negotiated national settlement.')

add('akel','labour','Organized Labour',0,0,effects=[mod('AKEL Social Programme',stability_factor=.08,office_park_income_tax_modifier=-.03)],
 desc='AKEL draws strength from organized workers and a parliamentary commitment to independence. Its social programme improves security for households while placing greater demands on commercial returns.')
add('akel','parliamentary_left','The Parliamentary Left',0,1,'labour',effects=[mod('AKEL Social Programme',political_power_factor=.10,foreign_influence_defense_modifier=.05)],
 desc='A parliamentary strategy can connect the labour movement to the republic institutions. Opposition rights, coalition bargaining and electoral organization can extend its influence while preserving constitutional competition.')
add('akel','cooperative_sector','A Cooperative Sector',-3,3,'parliamentary_left',['public_industry'],[mod('AKEL Social Programme',agricolture_productivity_modifier=.15,stability_factor=.05,bureaucracy_cost_multiplier_modifier=.05)],setup=.75,
 desc='Cooperative credit and marketing can strengthen small producers alongside organized labour. Public oversight and guarantees increase administrative responsibilities.',source='economy')
add('akel','public_industry','Public Industrial Holdings',3,3,'parliamentary_left',['cooperative_sector'],[building(145,'industrial_complex'),mod('AKEL Social Programme',industrial_capacity_factory=.12,bureaucracy_cost_multiplier_modifier=.08)],setup=2,
 desc='Public holdings can concentrate scarce investment on industrial capacity. Acquisitions and management must be financed, and political ownership does not remove production constraints.',source='economy')
add('akel','rural_processing','Rural Processing',-3,5,'cooperative_sector',effects=[building(145,'industrial_complex'),mod('AKEL Social Programme',agricolture_productivity_modifier=.05)],setup=1.25,
 desc='Processing and storage can retain more of the value of rural exports on the island. The investment complements cooperative organization and remains useful after a change of government.',source='economy')
add('akel','public_standards','Public Production Standards',3,5,'public_industry',effects=[mod('AKEL Social Programme',production_factory_max_efficiency_factor=.10),bonus('CAT_industry',.5)],setup=.5,
 desc='Technical standards and professional management can improve public industrial performance. The programme develops the selected public-holdings route while retaining its administrative costs.',source='economy')
add('akel','services_for_all','Services for All',0,7,[['rural_processing','public_standards']],effects=[mod('AKEL Social Programme',research_speed_factor=.05,stability_factor=.05,health_cost_multiplier_modifier=.08,education_cost_multiplier_modifier=.05)],weekly=.004,
 desc='Wider access to education and health care can support both social confidence and technical skills. The commitment requires continuing public expenditure instead of a one-time declaration.')
add('akel','bicommunal_labour','Bicommunal Labour Links',-3,9,'services_for_all',['eastern_terms'],[change('Communal confidence',10),mod('AKEL Social Programme',stability_factor=.05,political_power_factor=-.05)],
 desc='Trade-union contacts can rebuild practical cooperation between Greek Cypriot and Turkish Cypriot workers. A common labour agenda asks the party to spend political capital on compromise.',source='community')
add('akel','eastern_terms','Eastern Technical Methods',3,9,'services_for_all',['bicommunal_labour'],[bonus('CAT_industry',.5,2),mod('AKEL Social Programme',research_speed_factor=.05,foreign_influence_defense_modifier=-.08)],setup=.5,
 desc='Eastern industrial methods can offer another source of technical knowledge. A stronger reliance on this model narrows diplomatic flexibility without automatically making Cyprus a Soviet ally.')
add('akel','social_compact','A Common Social Compact',-3,11,'bicommunal_labour',effects=[mod('AKEL Social Programme',agricolture_productivity_modifier=.05,stability_factor=.03),change('Communal confidence',5)],weekly=.002,req='Both communal delegations accept access and labour safeguards.',
 desc='Agreed social rights can give cooperation a material foundation across the communal divide. Services must be funded and administered with the consent of both sides.',source='community')
add('akel','planning_school','Industrial Planning School',3,11,'eastern_terms',effects=[mod('AKEL Social Programme',production_speed_industrial_complex_factor=.10,education_cost_multiplier_modifier=.05),bonus('CAT_industry',.5)],setup=.5,
 desc='A planning school can train the administrators needed for the public industrial programme. It expands domestic expertise at an additional educational cost.')
add('akel','democratic_socialism','Democratic Socialism',0,13,[['social_compact','planning_school']],effects=[mod('AKEL Social Programme',political_power_factor=.05,stability_factor=.05)],
 desc='A durable social programme must win support within the republic political system. Labour rights, public services and national independence can form a common platform for continued democratic competition.')

# Use native one-row progression; the draft's logical stages are not empty spacer rows.
for group,_,ax,ay,_ in GROUPS:
 rows=sorted({f['offset'][1]for f in F if f['group']==group})
 for f in [f for f in F if f['group']==group]:
  f['offset'][1]=rows.index(f['offset'][1]);f['y']=ay+f['offset'][1]
  f['emitted_xy']=[f['offset'][0],f['offset'][1]]if f['anchor']else[f['x'],f['y']]

TITLES={'cabinet':'Cabinet Government','audit':'Audit Office','rights':'Communal Rights','endure':'A Durable Republic',
 'autonomy':'Communal Autonomy','representation':'Shared Representation','movement':'Open Island Routes',
 'military_terms':'Written Mission Terms','emergency':'Presidential Safeguards','plan':'The Second Plan',
 'infantry':'Infantry Training','special':'Commando Training','doctrine':'Defence Doctrine',
 'bases':'Base Area Access','czech':'Inspected Arms Supply','public_industry':'Public Industry',
 'public_standards':'Public Standards','independent':'An Independent State','clerides':'Constitutional Right',
 'diplomatic_service':'Diplomatic Corps','parliamentary_left':'Parliamentary Strategy','bicommunal_labour':'Bicommunal Labour','reserve_service':'Reserve Standards',
 'social_compact':'Common Social Rights','planning_school':'Planning School','presidential_service':'Presidential Service'}
# Reduce accumulated stability before the whole compatible-route audit, rather than wasting benefits at the cap.
STABILITY={'mediation':.03,'scrutiny':.04,'ballot':.02,'new_compact':.03,'rights':.01,
 'clinics':.02,'autonomy':.03,'safeguards':.01,'geneva':.02,'civil_defence':.03,
 'coalition':.02,'church_welfare':.03,'parish':.01,'federal_centre':.02,'succession':.02,
 'enterprise':-.02,'republican_right':.03,'clerides':.02,'labour':.04,'cooperative_sector':.02,
 'services_for_all':.02,'bicommunal_labour':.01,'social_compact':.01,'democratic_socialism':.02}
for f in F:
 f['title']=TITLES.get(f['key'],f['title'])
 for e in f['effects']:
  if f['key'] in STABILITY and e['type']=='modifier_delta' and 'stability_factor'in e['values']:
   e['values']['stability_factor']=STABILITY[f['key']]
 if f['key']in('civilian_rule','geneva'):
  f['offset'][1]=7;f['y']=7;f['emitted_xy'][1]=7
 confidence_gate={'passage':40,'utilities':40,'municipal':50,'autonomy':50,'movement':65}.get(f['key'])
 if confidence_gate is not None:
  f['requirements']=f'Communal confidence at least {confidence_gate}. '+f['requirements']
 if f['key']in('association','czech'):
  f['historicity']='Later historical precedent. Earlier negotiated terms are deliberate alternate history.'
 for e in f['effects']:
  if e['type']=='building':
   e['guards']={'owner':'CYP','controller':'CYP','native_capacity':True,'native_building_cap':True,
    'province_in_state':e['province']if e['province']else None,'coastal':e['building']in('naval_base','coastal_bunker'),
    'one_time_receipt':f['id'],'slot_before_building':True}
   guard=f"State{e['state']} owned and controlled by Cyprus; native {e['building']} capacity and cap available."
   f['requirements']=(f['requirements']+' '+guard).strip()

ACTOR_FOCUSES=[
 dict(tag='GRE',key='gre_officers',title='Officers on Cyprus',x=3,y=0,pre=[],exclusive=[],effects=['Army organization +2%','Training time -5%'],requirements='Greece and Cyprus exist; an actual Greek officer footprint exists.'),
 dict(tag='GRE',key='gre_treaty',title='Honour the Republic',x=0,y=1,pre=['gre_officers'],exclusive=['gre_network'],effects=['Foreign influence defence +5%','Stability +2%','Officer penetration in Cyprus -10'],requirements='No war with Cyprus.'),
 dict(tag='GRE',key='gre_network',title='The Officer Network',x=6,y=1,pre=['gre_officers'],exclusive=['gre_treaty'],effects=['Political power -50','Treasury -0.25% of current Cyprus GDP','Officer penetration in Cyprus +20','Stability -2%'],requirements='Greece is ruled by the actual military-junta party. Greek officer footprint remains. Once per campaign.'),
 dict(tag='GRE',key='gre_consult',title='A Guarantor Settlement',x=0,y=2,pre=['gre_treaty'],exclusive=[],effects=['Greece, Turkey and Britain receive Guarantor Consultations','Political power +50'],requirements='An actual constitutional crisis exists.'),
 dict(tag='GRE',key='gre_withdraw',title='Withdraw the Network',x=4,y=2,pre=['gre_network'],exclusive=['gre_coup'],effects=['Officer penetration in Cyprus -20','Stability +3%'],requirements='The coup has not launched.'),
 dict(tag='GRE',key='gre_coup',title='Overthrow Makarios',x=8,y=2,pre=['gre_network'],exclusive=['gre_withdraw'],effects=['Political power -100','Treasury -0.5% of current Cyprus GDP','Cyprus receives Coup Warning','If successful: Sampson becomes the authored coup-government leader'],requirements='Actual Greek junta remains in power. Officer penetration at least60. Officer footprint exists. Cyprus remains independent and at peace with Greece. Once per campaign.'),
 dict(tag='TUR',key='tur_consult',title='Consult the Guarantors',x=3,y=0,pre=[],exclusive=[],effects=['Greece and Britain receive Guarantor Consultations','Political power +35'],requirements='An actual constitutional rupture in Cyprus has occurred.'),
 dict(tag='TUR',key='tur_terms',title='Negotiated Safeguards',x=0,y=1,pre=['tur_consult'],exclusive=['tur_operation'],effects=['Turkey: Stability +3%','Turkey: Army attack -2%','Cyprus receives Communal Guarantees Proposal'],requirements='Both communal delegations must separately accept local terms. A foreign signature cannot replace them.'),
 dict(tag='TUR',key='tur_operation',title='Invoke Article IV',x=6,y=1,pre=['tur_consult'],exclusive=['tur_terms'],effects=['Political power -75','Cyprus receives Constitutional Restoration Ultimatum','An unresolved ultimatum leads to the explicitly selected Turkish operation'],requirements='Consultations failed. Actual coup government or unresolved constitutional rupture remains. No automatic claim of legal justification.'),
 dict(tag='ENG',key='eng_consult',title='Consultation in London',x=3,y=0,pre=[],exclusive=[],effects=['Greece and Turkey receive Guarantor Consultations','Political power +35'],requirements='An actual constitutional crisis exists.'),
 dict(tag='ENG',key='eng_mediation',title='A Joint Mediation',x=0,y=1,pre=['eng_consult'],exclusive=['eng_restraint'],effects=['Cyprus receives Joint Restoration Proposal','Bureaucracy cost +1%','Political power +50'],requirements='Greece and Turkey accept coordinated diplomacy through response events.'),
 dict(tag='ENG',key='eng_restraint',title='Limit the Commitment',x=6,y=1,pre=['eng_consult'],exclusive=['eng_mediation'],effects=['Bureaucracy cost -1%','Foreign influence defence -3%','Political power +50'],requirements='Britain abstains from a joint enforcement commitment; the treaty record remains.'),
]
for a in ACTOR_FOCUSES:
 a['id']='COLDWAR_'+a['tag']+'_CYP_R2_'+a['key'];a['cost']=2 if a['key']in('gre_coup','tur_operation')else 5
 a['party_trigger']='nationalist_military_junta_are_in_power'if a['key']in('gre_network','gre_coup')else None

SPIRITS=[
 dict(name='Broken Constitutional Partnership',values={'stability_factor':-.10,'political_power_factor':-.10},remedy='A Republic That Endures',basis='Joint institutions ceased to operate normally after the 1963 breakdown. This is an institutional condition, not an ethnic characteristic.'),
 dict(name='Separate Communal Administrations',values={'production_speed_buildings_factor':-.08,'agricolture_productivity_modifier':-.05,'bureaucracy_cost_multiplier_modifier':.03},remedy='Open Island Routes, after both communal delegations accept',basis='Separate institutions and restricted access fragment public services and rural markets. These are institutional costs, not ethnic characteristics. The1970 map has no accurate enclave mosaic.'),
 dict(name='Divided National Guard Command',values={'army_org_factor':-.10,'training_time_factor':.15},remedy='Restore Civilian Rule',basis='External officer dependence and competing loyalties undermine unified command.'),
 dict(name='Enosis Underground Networks',values={'stability_factor':-.05,'political_power_factor':-.05},remedy='Restore Civilian Rule, after actual network dismantling',basis='The National Front is relevant at the start. EOKA B is introduced only after its formation in 1971.'),
 dict(name='Limited Technical Capacity',values={'research_speed_factor':-.05},remedy='Technical Institutes',basis='The small technical and educational base constrains specialist capacity. No workforce-size penalty.'),
 dict(name='Makarios Presidential Authority',values={'political_power_factor':.15,'stability_factor':.05},remedy='Attached only while Makarios actually leads; no automatic transfer to a successor',basis='An independent president and archbishop with a broad electoral mandate; not a DIKO government in 1970.'),
 dict(name='UNFICYP Presence',values={'stability_factor':.05,'war_support_factor':-.05},remedy='Remains with the actual peacekeeping arrangement',basis='The peacekeeping force and its de-escalatory role predate 1970.'),
 dict(name='1960 Treaty of Guarantee',values={},remedy='Permanent baseline on CYP, GRE, TUR and ENG; political treaty revision requires the participants',basis='The same treaty appears for all four parties. No free defence guarantee, automatic war or permanent combat bonus.')]

SPIRIT_DESCRIPTIONS=[
 'The constitutional partnership has broken down. Representation, executive powers and security remain disputed, weakening the authority of common institutions.',
 'Greek Cypriot and Turkish Cypriot communities rely on separate administrations and restricted routes. Fragmented services and markets raise costs and obstruct shared investment.',
 'Dependence on Greek officers and competing political loyalties complicate civilian control of the National Guard. Training and command reforms require time and resources.',
 'Armed supporters of union with Greece challenge the authority of the republic. Clandestine intimidation and violence weaken lawful political competition.',
 'Ministries, schools and industry compete for a limited pool of trained specialists. Technical education must expand if national development is to continue.',
 'Makarios combines the presidency with the authority of the Orthodox archbishopric. His broad personal mandate can hold together allies with different political aims.',
 'The United Nations force helps prevent renewed communal fighting and maintains channels between the sides. Its presence encourages restraint during local security disputes.',
 'The1960 settlement protects the independence and territorial integrity of Cyprus and prohibits union or partition. Greece, Turkey and Britain undertake to consult when the treaty order is threatened.']
for s,description in zip(SPIRITS,SPIRIT_DESCRIPTIONS):s['description']=description
SPIRITS[0]['remedy']='Removed by A Durable Republic after the constitutional settlement operates.'
SPIRITS[5]['remedy']='Removed when Makarios leaves the presidency.'
SPIRITS[7]['remedy']='Held by Cyprus, Greece, Turkey and the United Kingdom. Treaty revision requires the participants.'

OFFERS={
 'greek_training':dict(name='Greek Training Mission',senders=['CYP'],recipients=['GRE'],setup={'CYP':.5,'GRE':0},weekly={'CYP':.002,'GRE':0},
  sides={'CYP':dict(spirit='Greek Training Mission',values={'army_org_factor':.08,'training_time_factor':-.10,'foreign_influence_defense_modifier':-.10},research=[],other=['Army experience +20','Officer penetration +15']),
         'GRE':dict(spirit='Cyprus Training Commitment',values={'army_org_factor':.02,'bureaucracy_cost_multiplier_modifier':.02},research=[],other=[])},basis='alliance'),
 'yugoslavia':dict(name='Non-Aligned Technical Exchange',recipients=['SER'],setup={'CYP':.5,'SER':0},weekly={'CYP':.002,'SER':0},
  sides={'CYP':dict(spirit='Non-Aligned Technical Exchange',values={'research_speed_factor':.05,'education_cost_multiplier_modifier':.05},research=[bonus('CAT_industry',.5)],other=[]),
         'SER':dict(spirit='Cypriot Technical Contracts',values={'office_park_income_tax_modifier':.02,'education_cost_multiplier_modifier':.01},research=[],other=['Income +0.002% of Cyprus GDP per week'])},basis='nonaligned'),
 'britain':dict(name='Base Area Civil Access',recipients=['ENG'],setup={'CYP':.25,'ENG':0},weekly={'CYP':0,'ENG':0},
  sides={'CYP':dict(spirit='Base Area Civil Access',values={'office_park_income_tax_modifier':.08,'foreign_influence_defense_modifier':-.05},research=[],other=[]),
         'ENG':dict(spirit='Cypriot Base Liaison',values={'army_org_factor':.02,'bureaucracy_cost_multiplier_modifier':.01},research=[],other=[])},basis='guarantee'),
 'czechoslovakia':dict(name='Supervised Czechoslovak Supply',recipients=['CZE'],setup={'CYP':.5,'CZE':0},weekly={'CYP':.002,'CZE':0},
  sides={'CYP':dict(spirit='Supervised Czechoslovak Supply',values={'army_org_factor':.05,'foreign_influence_defense_modifier':-.05},research=[bonus('CAT_infantry',.5)],other=['Army experience +25']),
         'CZE':dict(spirit='Cypriot Supply Contracts',values={'office_park_income_tax_modifier':.02,'bureaucracy_cost_multiplier_modifier':.01},research=[],other=['Income +0.002% of Cyprus GDP per week'])},basis='arms'),
 'eec':dict(name='Cyprus Association Protocol',recipients=['GER','FRA','ITA','BEL','HOL','LUX'],setup={'CYP':1,'GER':0,'FRA':0,'ITA':0,'BEL':0,'HOL':0,'LUX':0},weekly={'CYP':0},
  sides={'CYP':dict(spirit='European Association',values={'office_park_income_tax_modifier':.10,'production_speed_industrial_complex_factor':.05,'bureaucracy_cost_multiplier_modifier':.05},research=[],other=[]),
         'each_recipient':dict(spirit='Cyprus Association Protocol',values={'office_park_income_tax_modifier':.001,'bureaucracy_cost_multiplier_modifier':.0005},research=[],other=[])},basis='eec'),
 'greek_civil':dict(name='Greek-Cypriot Civil Exchange',recipients=['GRE'],setup={'CYP':.5,'GRE':0},weekly={'CYP':.002,'GRE':0},
  sides={'CYP':dict(spirit='Greek-Cypriot Civil Exchange',values={'research_speed_factor':.05,'education_cost_multiplier_modifier':.05},research=[bonus('CAT_industry',.35)],other=[]),
         'GRE':dict(spirit='Cypriot Educational Exchange',values={'research_speed_factor':.01,'education_cost_multiplier_modifier':.01},research=[],other=['Income +0.002% of Cyprus GDP per week'])},basis='alliance'),
 'turkey':dict(name='Communal Guarantees Protocol',recipients=['TUR'],setup={'CYP':.25,'TUR':0},weekly={'CYP':0,'TUR':0},
  sides={'CYP':dict(spirit='Communal Guarantees Protocol',values={'stability_factor':.03,'foreign_influence_defense_modifier':.05,'army_attack_factor':-.03},research=[],other=[]),
         'TUR':dict(spirit='Cyprus Confidence Protocol',values={'stability_factor':.02,'foreign_influence_defense_modifier':.03,'army_attack_factor':-.01},research=[],other=[])},basis='settlement')}

SOURCES={
 'politics':dict(title='IPU: Cyprus parliamentary election, 5 July 1970',url='https://data.ipu.org/election-summary/PDF/CYPRUS_1970_E.PDF',note='Contemporary party programmes and seats. Prefer seats to the non-comparable candidate-vote percentages.'),
 'community':dict(title='IPU: separate communal institutions in 1970',url='https://data.ipu.org/election-summary/PDF/CYPRUS_1970_E.PDF',note='Separate Turkish Cypriot assembly; reserved Republic seats uncontested. Talks since 1968 also documented by World Bank.'),
 'economy':dict(title='World Bank: Cyprus economic memorandum, 11 May 1973',url='https://documents1.worldbank.org/curated/en/714871468027642843/pdf/multi0page.pdf',note='Rapid 1960s growth, 1967-71 plan, tourism, agriculture, investment and specialist needs. Used as retrospective evidence, not a claim that all 1973 figures apply to January 1970.'),
 'guarantee':dict(title='UN Treaty Series 382: 1960 settlement',url='https://treaties.un.org/doc/Publication/UNTS/Volume%20382/v382.pdf',note='Treaty of Guarantee pp.3-7; Establishment Treaty and UK declaration separately. Consultation first; union and partition barred. Lawfulness of later military action is not settled by a game tooltip.'),
 'security':dict(title='UNFICYP: the 1967 crisis and subsequent developments',url='https://unficyp.unmissions.org/en/1967-crisis',note='1970 assassination attempt, clandestine pro-Enosis activity, 1972 inspection and storage arrangements.'),
 '1974':dict(title='UNFICYP: events in summer 1974',url='https://unficyp.unmissions.org/en/events-summer-1974',note='Greek-officer-directed coup 15 July, Turkish operation 20 July, UNSCR353. Consequences occur only if the campaign actually produces conflict/displacement.'),
 'settlement':dict(title='UN Secretary-General: 1977 high-level agreement',url='https://digitallibrary.un.org/record/564485/files/S_12323-EN.pdf',note='Independent, non-aligned bicommunal federal framework; also consider 1979 high-level terms. These are later precedents for a negotiated alternative, not a settled 1970 constitution.'),
 'alliance':dict(title='US FRUS: the 1959-60 settlement',url='https://history.state.gov/historicaldocuments/frus1958-60v10p1/d310',note='Treaty of Alliance is distinct from Treaty of Guarantee. Authorised Greek/Turkish contingents are not an unrestricted right to control the Guard.'),
 'arms':dict(title='UNFICYP: arms inspection arrangements',url='https://unficyp.unmissions.org/en/1967-crisis',note='Historical 1972 Czechoslovak imports and subsequent UN storage/inspection support the concept; the proposed exact economic and modifier terms are balance proposals.'),
 'eec':dict(title='Council of the European Union: 1972 association agreement',url='https://www.consilium.europa.eu/en/documents/treaties-agreements/agreement/?docLanguage=en&id=1972002',note='Signed 19 December1972, effective1 June1973. Association is not membership. Multi-party approval is approximated by six fixed country recipients, pending native EU-system integration review.'),
 'nonaligned':dict(title='NAM: founding and history',url='https://www.nam-pn.org/history',note='Cyprus and Yugoslavia were founding participants in 1961. Bilateral technical terms are proposed alternate history, not an asserted historical contract.'),
 'plot':dict(title='US FRUS: January1970 assassination plot warning',url='https://history.state.gov/historicaldocuments/frus1969-76v29/d350',note='Records warning passed to Makarios15 January; March attempt is later. Do not equate a historical warning with proof of every alleged sponsor.'),
 'diko':dict(title='DIKO: party history',url='https://democraticparty.org.cy/profile/',note='Party self-description; later founding/succession cross-checked against parliamentary chronology. Makarios remains independent in1970.'),
 '1983':dict(title='UN Security Council resolution541(1983)',url='https://digitallibrary.un.org/record/58970',note='The separate-state declaration was deemed legally invalid. No recognised NCY sovereign state exists at the 1970 start.')}

COUNTRIES={'CYP':'Cyprus','GRE':'Greece','TUR':'Turkey','ENG':'United Kingdom','SER':'Yugoslavia','CZE':'Czechoslovakia','GER':'West Germany','FRA':'France','ITA':'Italy','BEL':'Belgium','HOL':'Netherlands','LUX':'Luxembourg'}
for key,side in [('yugoslavia','SER'),('czechoslovakia','CZE')]:
 OFFERS[key]['sides'][side]['values']={'office_park_income_tax_modifier':.001,'bureaucracy_cost_multiplier_modifier':.0005}
OFFERS['britain']['sides']['ENG']['values']={'army_org_factor':.005,'bureaucracy_cost_multiplier_modifier':.001}
OFFERS['greek_training']['sides']['GRE']['values']={'army_org_factor':.01,'bureaucracy_cost_multiplier_modifier':.001}

CRISIS=[
 dict(key='baseline',title='January 1970',actor='Cyprus / Greece / Turkey / Britain',next=['choice'],text='Makarios; Greek junta; communal confidence35; officer penetration45. The Treaty appears on all four countries. There is no separate Turkish Cypriot sovereign state.'),
 dict(key='choice',title='Two Security Strategies',actor='CYP',next=['autonomy','mission'],text='Cypriot Command reduces officer penetration15 and temporarily costs organization5%. Greek mission requires GRE acceptance and grants organization8% / training time-10%, but penetration+15.'),
 dict(key='autonomy',title='Cypriot Command',actor='CYP',next=['consultation'],text='Domestic professionalization and police counterweights. Stronger resistance to a coup, slower training and real administrative costs.'),
 dict(key='mission',title='Greek Training Mission',actor='GRE accepts or refuses',next=['network','consultation'],text='The mission never grants Greece a unilateral government change. The Greek player must separately choose political interference.'),
 dict(key='network',title='The Greek Exclusive Paths',actor='Greece focus module',next=['warning'],text='Honour the Republic excludes The Officer Network. The network focus costs50PP and0.25% Cyprus GDP, adds20 penetration and requires an actual junta and officer footprint. Withdraw the Network then excludes Overthrow Makarios.'),
 dict(key='warning',title='Overthrow Makarios',actor='Greece focus; Cyprus notice event',next=['failed','coup'],text='The Greek coup focus costs100PP and0.5% Cyprus GDP; penetration must reach60. A14-day warning event precedes resolution. Cyprus defences come from its completed focus path. No crisis decision menu or daily meter.'),
 dict(key='failed',title='Constitutional Government Survives',actor='Cyprus focus preparations',next=['consultation'],text='Coup strength equals penetration. Defence=40+25 if Presidential Safeguards was completed. Written Mission Terms and Expose Armed Networks reduce penetration before resolution. Defender wins ties. No paid counter-decision or extra response menu.'),
 dict(key='coup',title='Coup Government in Nicosia',actor='GRE / CYP',next=['consultation'],text='Only a resolved successful attempt changes the CYP government to the authored Sampson regime. No annexation, no free armies, no automatic war. A restoration choice remains available.'),
 dict(key='consultation',title='Article IV Consultation',actor='Greece / Turkey / Britain; Cyprus invited',next=['settlement','intervention'],text='Response events carry14-day offers. Silence is abstention. Small guarantor focus forks determine mediation or restraint. Coordinated terms need each real signature. Treaty status does not suspend like a paid commercial agreement.'),
 dict(key='settlement',title='Restoration and Negotiation',actor='CYP + both communities + guarantors',next=[],text='Ceasefire/restoration needs the actual belligerents. Communal constitutional terms need separate local acceptance. No automatic province transfer or restoration of one-time assets.'),
 dict(key='intervention',title='Safeguards or Intervention',actor='Turkey exclusive focus fork',next=['aftermath'],text='Negotiated Safeguards excludes Invoke Article IV. The latter requires failed consultation and an unresolved constitutional rupture, then delivers an ultimatum event. A real Turkish focus choice drives escalation. UN diplomacy remains available; the game does not certify the disputed legality of military action.'),
 dict(key='aftermath',title='Actual Territorial and Civilian Consequences',actor='Belligerents and CYP',next=['settlement'],text='Only actual combat/control/displacement enables relief, loss of tourism revenue and later settlement routes. State146 is a coarse map unit, not the1970 enclave geography. A separate-state declaration requires a new RP choice and diplomatic consequences, never an automatic1983 release.')]

def fmt(v): return f'{v*100:+g}%'
def effect_lines(e):
 t=e['type']
 if t in ('modifier_delta','temporary_spirit'):
  title=e['spirit']+(f" ({e['days']} days)" if 'days'in e else '')
  return [title+': '+LABELS[k]+' '+fmt(v) for k,v in e['values'].items()]
 if t=='building':return [f"State {e['state']}: shared building slots +{e['shared_slots']}",f"State {e['state']}"+(f", province {e['province']}"if e['province']else '')+f": {e['building']} +{e['levels']}"]
 if t=='research':return [f"{e['uses']}x {e['bonus']*100:g}% research bonus: {e['category']}"]
 if t=='doctrine':return [f"{e['uses']}x {e['bonus']*100:g}% land-doctrine cost reduction"]
 if t=='country_event':return [', '.join(COUNTRIES[k]for k in e['recipients'])+': '+e['title']]
 if t=='remove_spirit':return ['Remove '+e['name']]
 if t=='crisis_value':return [e['name']+f" {e['amount']:+g}"]
 if t=='political_power':return [f"Political power {e['value']:+g}"]
 if t=='army_experience':return [f"Army experience {e['value']:+g}"]
 return []

def offer_lines(o):
 lines=['If they accept:']
 sides={}
 for side,terms in o['sides'].items():
  for country in (o['recipients']if side=='each_recipient'else[side]):sides[country]=terms
 for side,terms in sides.items():
  who=COUNTRIES[side]
  lines.append(who+': '+terms['spirit'])
  lines.extend(LABELS[k]+' '+fmt(v)for k,v in terms['values'].items())
  price=o['setup'].get(side,0)
  lines.append(f'Treasury -{price:g}% of Cyprus GDP'if price else 'Setup cost: 0')
  recurring=o['weekly'].get(side,0)
  lines.append(f'Expense +{recurring:g}% of Cyprus GDP per week'if recurring else 'Recurring expense: 0')
  for b in terms['research']:lines+=effect_lines(b)
  lines+=terms['other']
 return lines

def validate():
 assert len(F)==100,len(F)
 keys={f['key']:f for f in F}; assert len(keys)==100
 for g,_,_,_,expected in GROUPS:assert sum(f['group']==g for f in F)==expected
 assert len({(f['x'],f['y'])for f in F})==100
 for f in F:
  for group in f['prerequisites']:
   assert group
   for p in group: assert p in keys,(f['key'],p)
  for x in f['exclusive']:
   assert x in keys and f['key'] in keys[x]['exclusive'],(f['key'],x)
  for e in f['effects']:
   assert e['type']not in('unlock','unlock_decision','decision'),(f['key'],e)
   if 'values'in e:assert set(e['values'])<=set(LABELS),(f['key'],e)
   if e['type']=='building':assert e['levels']==e['shared_slots']
  assert not any(c in f['title']+f['description']for c in '\u2013\u2014')
 # Search satisfiable predecessor histories rather than reachability ignoring exclusions.
 def histories(key,trail=()):
  assert key not in trail,('cycle',key)
  acc=[{key}]
  for group in keys[key]['prerequisites']:
   candidates=[h for p in group for h in histories(p,trail+(key,))]
   acc=[a|b for a in acc for b in candidates if not any(set(keys[k]['exclusive'])&(a|b)for k in a|b)]
  return acc
 for f in F:assert histories(f['key']),('unreachable',f['key'])
 return {'project':'IMPERIA COLD WAR','focus_count':100,'group_counts':{g:sum(f['group']==g for f in F)for g,*_ in GROUPS},
  'reciprocal_exclusive_pairs':sum(len(f['exclusive'])for f in F)//2,'unique_positions':100,
  'all_prerequisites_satisfiable':True,'runtime_files_written':False,'periodic_reconciliation':'monthly',
  'native_decision_unlocks':0,'foreign_actor_focuses':len(ACTOR_FOCUSES),
  'live_HOI4_test':False,'live_multiplayer_test':False,'native_font_exact_match':False}

ICON_SOURCE=json.loads((ROOT/'docs/cyprus_1970_design/runtime_icon_map.json').read_text('utf-8'))['focuses']
ICON_LIST=list(dict.fromkeys(v['texture']for v in ICON_SOURCE.values()))
GROUP_ICON={
 'constitution':'gfx/interface/goals/coldwar/constitutional_guarantees.png',
 'community':'gfx/interface/goals/coldwar/BeginNegotiations.dds',
 'crisis':'gfx/interface/goals/coldwar/generic_civilian_oversight.png',
 'economy':'gfx/interface/goals/coldwar/factory_complex.png',
 'defence':'gfx/interface/goals/coldwar/generic_army_training.png',
 'diplomacy':'gfx/interface/goals/coldwar/generic_mediterranean.png',
 'centre':'gfx/interface/goals/coldwar/generic_council.png',
 'liberal':'gfx/interface/goals/coldwar/ideology_market_liberal.png',
 'akel':'gfx/interface/goals/coldwar/generic_workers_rights.png'}

def image_uri(rel):
 im=Image.open(ROOT/rel).convert('RGBA');im.thumbnail((100,100))
 b=io.BytesIO();im.save(b,format='PNG');return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()

def main():
 report=validate()
 for f in F:
  f['preview_effects']=([f"Treasury -{f['setup_gdp_percent']:g}% of current Cyprus GDP"]if f['setup_gdp_percent']else [])
  if f['weekly_gdp_percent']:f['preview_effects'] += [f"Expense +{f['weekly_gdp_percent']:g}% of current Cyprus GDP per week"]
  for e in f['effects']:
   f['preview_effects'] += offer_lines(OFFERS[e['key']])if e['type']=='offer'else effect_lines(e)
  f['icon']=GROUP_ICON[f['group']]
  if f['key']in('restore_1960','new_compact'):
   f['ratification']={'communal_confidence_minimum':65,'communities':['Greek Cypriot delegation','Turkish Cypriot delegation'],
    'foreign_parties':['GRE','TUR','ENG']if f['key']=='new_compact'else[],
    'numeric_rewards_only_after_acceptance':True,'responses':'country_events_only'}
   f['preview_effects'].insert(0,'If the constitutional terms are accepted:')
 data=dict(project='IMPERIA COLD WAR',status='CONCEPT ONLY. Approval pending. Supersedes the old295/296-focus design.',
  date='2026-10-27',focuses=F,groups=[dict(key=g,title=t,x=x,y=y,count=n)for g,t,x,y,n in GROUPS],
  starting_spirits=SPIRITS,offers=OFFERS,sources=SOURCES,crisis=CRISIS,actor_focuses=ACTOR_FOCUSES,countries=COUNTRIES,modifier_labels=LABELS,
  reconciliation='Monthly fixed-tag fallback plus targeted transition hooks. No daily or weekly relationship polling.',
  geometry=dict(grid_x_px=85,grid_y_px=130,card_width=165,card_height=128,source='Native GUI card bounds verified; grid-to-pixel conversion is a preview approximation. Native font and connector routing remain unverified.'),
  art={g:image_uri(rel)for g,rel in GROUP_ICON.items()})
 data=extend_intervention(data)
 report['foreign_actor_focuses']=len(data['actor_focuses'])
 report['turkey_crisis_decisions']=len(data['crisis_decisions'])
 report['decision_policy']=data['decision_policy']
 report['intervention_bonus_days']=data['intervention']['intervention_buff']['days']
 (OUT/'INTERVENTION_EXTENSION.md').write_text(intervention_document(data),encoding='utf-8')
 (OUT/'concept.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 manifest={ 'project':'IMPERIA COLD WAR','sources':{} }
 for rel in ['common/national_focus/COLDWAR_CYP_1970_focus.txt','tools/cyprus_1970/compile.py','history/countries/CYP - Cyprus.txt','interface/nationalfocusview.gui']:
  manifest['sources'][rel]=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
 (OUT/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 lines=['IMPERIA COLD WAR: Cyprus1970 compact replacement concept','',
 'Concept only. Awaiting approval. The old runtime has not been deleted or rebuilt during the design phase. The requested replacement includes retirement of the old generator and dependent hooks; deleting its focus file alone would leave explicit history/script references dangling. No loaded game files were changed.','',
 f"100 Cyprus focuses plus{len(data['actor_focuses'])}small supporting focus concepts for Greece, Turkey and Britain. Three full Cyprus political programmes: the independent presidential centre with later DIKO, Eniaion with later DISY, and AKEL. EDEK remains an explicitly represented coalition actor. All party branches remain visible; exact native ruling-party predicates gate execution and active programme modifiers. No Cyprus decision menu or dossier. Latest user exception: four finite Turkish army-crisis decisions. Foreign consent uses country-event options.",'',
 'All numeric values are proposed game balance, not historical statistical measurements. All names and descriptions below are English. Historical evidence is linked per focus family.','',
 '## January1970 baseline','',
 'MakariosIII is the independent president and archbishop. Fazil Kucuk heads the Turkish Cypriot Transitional Administration; Rauf Denktash is its leading negotiator, not yet its1973 head. The parliamentary contest is still ahead. Eniaion, AKEL and EDEK exist; DIKO, DISY and EOKA B do not yet exist. NCY is not an independent1970 state. Rapid1960s growth coexists with fragmented public institutions and security risks. No1974 refugee starting condition.','',
 '## Starting spirits','']
 for s in SPIRITS:
  lines+=['### '+s['name'],'',s['basis'],'']
  lines += ['- '+LABELS[k]+': '+fmt(v)for k,v in s['values'].items()]
  if not s['values']:lines+=['- No numeric bonus. Treaty role and available diplomatic actions only.']
  lines+=['','Remedy/lifecycle: '+s['remedy']+'.','']
 lines+=['## Spatial design','',
  'Absolute grid bounds: x2..98, y0..18. Six shared pillars in the upper band; three party programmes in the lower band. Shared roots and party entry programmes are independently available when their real requirements hold. No redundant unlock focus for a party already governing. Initial camera on The Republic at Ten; shortcuts for every section. Continuous-focus panel below y21, outside all branch footprints. No relative anchor can refer forward in the eventual output.','',
  '| Section | Anchor(x,y) | Focuses |','|---|---:|---:|']
 for g,t,x,y,n in GROUPS:lines += [f'| {t} |({x},{y}) | {n} |']
 lines+=['','The inspector and full layout use the same absolute coordinates and grouped prerequisites. Native card165x128px and title width147px are verified from the local GUI. The85x130 grid conversion, fonts, icon assignment and connectors are concept rendering choices and require in-engine review.','',
 '## Money, programmes and construction','',
 'Ordinary setup percentages use the paying country current GDP; for these CYP focuses that is Cyprus GDP. All foreign offer setup, payments and receipts are expressly based on current Cyprus GDP and shown to every recipient. GDP means the native gdp_total figure in MD billions. Setup0.5%=GDP*0.005 once. Expense0.002%GDP per week=GDP*0.00002 per native weekly economic calculation. Do not divide the weekly percentage by52. No scripted budget literal may have more than five fractional digits. There is no EEC pooled cash payment or long fractional recipient share. Foreign preview country names use historical1970 identity:SER is the actual registered game tag for Yugoslavia, not a claim that Serbia is a sovereign1970 state.','',
 'The native economy keeps its normal weekly bookkeeping. It reads cached active programme/deal state and adds the corresponding weekly streams once; it performs no relationship checks. Relationship/programme reconciliation is monthly, with targeted immediate hooks for war, sanction, termination, country disappearance and government changes. Recompute cached monetary amounts monthly and at signing/termination. No permanent per-country daily observer, global country iteration or new dynamic-modifier enable polling.','',
 'Party modifier deltas accumulate only within that party programme. Monthly reconciliation and exact-party transition hooks attach the governing programme and detach inactive programmes. Earned variables remain. Returning to office restores only earned programme modifiers; it never repeats buildings, research, cash or experience. All permanent institutional policies persist unless an explicit enacted-policy reversal exists.','',
 'Every construction grant adds one shared state slot per level before construction inside the same one-time transaction. Infrastructure and both fort types are included. Owner, control, province, coastal status and native cap must be checked separately. Map states145/146 are coarse; no fictional enclave states or forced transfers. `offices` is used as the native office-building key only after source verification.','',
 '## Communal consent and minority representation','',
 'The debuff is institutional separation and restricted access, never Turkish Cypriot ethnicity. Communal confidence starts35/100 as a balance proposal. Officer penetration starts45/100, also proposed balance. Focus completions and targeted outcome events change them; neither drifts daily. Only accepted mobility/service agreements remove Separate Communal Administrations.','',
 'There is no separate Turkish Cypriot sovereign player seat in1970. The CYP player selects exclusive focus terms; a Turkish Cypriot delegation outcome event applies disclosed confidence and safeguard rules. This is simulated institutional consent, not another human player. Safe passage requires confidence40 and protected local access; autonomy/municipal terms require50; a final constitutional/mobility settlement requires65 and agreed representation/security safeguards. There is no extra choice menu for a CYP player to bypass the focus fork. Ankara cannot sign for the community. A real separate communal human seat would require a separately approved actor/map design.','',
 'The armed Enosis route belongs to the Greek junta/crisis layer; it is not a fourth full party tree. EOKA B appears only after its1971 founding. A possible Sampson coup government keeps common crisis/defence/development access, but none of the three civilian programme modifiers. EDEK participates through the coalition agreement and social/constitutional choices. This compression does not deny its importance.','',
 '## Treaty and road to war','',
 'The1960 Treaty of Guarantee spirit is present on CYP,GRE,TUR,ENG. ArticleI/II prohibit union and partition; ArticleIV begins with consultation and restricts the stated aim of action to restoration of the treaty order. Treaty of Alliance and British Sovereign Base arrangements are distinct instruments. The concept does not equate the Treaty with an automatic native military guarantee or a legal verdict on1974.','']
 for c in data['crisis']:lines += ['### '+c['title'],'','Actor: '+c['actor']+'. '+c['text'],'']
 lines += ['Coup resolution: Greek coup strength equals current officer penetration. Constitutional defence is40 plus25 if Presidential Safeguards is complete. Defender wins ties. Greek launch focus creates one14-day warning and one delayed resolution event. Cyprus uses its completed safeguards and command-policy path; there is no extra paid counter-decision. Recheck Greece remains a junta and its officer footprint exists, otherwise abort. A hostile attempt does not require victim consent. Failed attempt dismantles the network. One attempted coup per campaign prevents repeated action spam. A mission route with no further reforms reaches80 strength after Greek preparation; Written Mission Terms and Expose Armed Networks reduce it to65, which prepared defence65 can stop. The complete Cypriot-command route prevents the penetration threshold being reached. These are explicit balance consequences, not hidden random rolls.','',
 'Emergency aftermath proposals: actual displacement adds Displaced Families(stability-10%, construction-10%, health cost+10%); actual war plus Visitor Economy adds Tourism Interrupted(office tax income-15%). Visitor policy benefits suspend while war lasts and restore at peace through the monthly/event transition update. Recovery and Housing is the actual paid focus remedy for Displaced Families. No relief decisions, automatic population moves, property transfers, separate-state release,1960 troop deployments or free armies are included.','',
 '## Seven signed agreements','',
 'Each offer begins in its named Cyprus focus. Named recipients receive Accept/Refuse country-event options with complete numeric prospective effects. These agreements add no decision menus. Pending offers expire after90days through one guarded delayed event; signed deals have no expiry. Terms are quoted at proposal, rechecked on response and requoted through a renewed event if the monetary price changed. Both countries must exist, be at peace with one another, impose no native embargo in either direction, and have none of imp_dip/imp_fin/imp_eco/imp_mil sanctions in any mirrored incoming/outgoing array on either side. All matching spirits and weekly streams suspend together; restoration never repeats setup fees or one-time assets. A finite policy-reversal focus can terminate the selected agreement; no recurring termination decision is introduced. Third-country war or sanctions alone do not cancel the pair.','',
 'The EEC association is an explicit multiplayer abstraction of Community ratification: all six fixed founding partners approve before activation, each is named individually with its full modest modifiers and zero cash receipts/costs. All six retain required actual native Community membership. A failed relationship pauses the whole protocol. Cyprus is an associate, not a member. Earlier access than the historical1972/73 agreement is a deliberate negotiated alternative, as is a pre1972 inspected Czech supply. Native European-system integration remains unverified; no parallel Community UI/system is approved.','',
 'At most11 distinct foreign pairs are cached for this design(SER,ENG,CZE,GRE,TUR and six Community partners). Two Greek agreements share one eligibility result. A rough upper bound is about250 atomic eligibility predicates per monthly fallback, plus domestic programme checks. Targeted hooks evaluate only the changed pair. This is a static operation estimate, not an engine performance measurement.','']
 for key,o in OFFERS.items():
  lines += ['### '+o['name'],'','Recipient event options: '+', '.join(COUNTRIES[t]for t in o['recipients'])+'.','']
  lines += ['- '+s for s in offer_lines(o)]
  lines += ['','Historical basis: '+SOURCES[o['basis']]['url']+'. Exact reciprocal terms are a balance proposal.','']
 lines+=['## Supporting guarantor focus paths','',f"These{len(data['actor_focuses'])}focuses are additions to the respective existing country trees, not extra Cyprus focuses. They use focus prerequisite/exclusion semantics. Only the Turkish army crisis uses its four explicitly requested finite decisions. Relative mini-module coordinates reserve a footprint; attachment to the complete foreign trees still needs integration review.",'']
 for a in data['actor_focuses']:
  lines += ['### '+COUNTRIES[a['tag']]+': '+a['title'],'',
   'ID:`'+a['id']+'`. Position:('+str(a['x'])+','+str(a['y'])+'). Prerequisite:'+(', '.join(a['pre'])or'None')+'. Excludes:'+(', '.join(a['exclusive'])or'None')+'.','',a['requirements'],'']
  lines += ['- '+e for e in a['effects']]
  lines += ['']
 lines+=['## Intervention extension','',intervention_document(data),'']
 lines+=['## Focus catalogue','',
 'Effects for ordinary permanent/party programmes are signed deltas to the named programme. No source of a delta is reapplied during synchronization. Independent programme components are additive; exclusive siblings cannot stack. Every focus can be inspected outside its active party. Research grants are one-time. Full offer terms are repeated in the focus inspector regardless of current eligibility.','']
 for g,title,_,_,_ in GROUPS:
  lines+=['## '+title,'']
  for f in [f for f in F if f['group']==g]:
   pre=' AND '.join('('+' OR '.join(p)+')'for p in f['prerequisites'])or'None'
   lines += ['### '+f['title'], '',f['description'],'',f"ID: `{f['id']}`. Position:({f['x']},{f['y']}). Duration:{f['days']}days(cost{f['cost']}).",'',
    'Prerequisites: '+pre+'. Exclusive: '+(', '.join(f['exclusive'])or'None')+'.',
    'Requirements: '+('`'+f['party_trigger']+'`. 'if f['party_trigger']else '')+(f['requirements']or'Normal focus requirements.') ,'']
   lines+=['- '+s for s in f['preview_effects']]
   lines+=['','Basis: ['+SOURCES[f['source']]['title']+']('+SOURCES[f['source']]['url']+').','']
 lines+=['## Source and API evidence','',
  'Main MD source root: E:/SteamLibrary/steamapps/workshop/content/394360/2777392649. Study performed27October2026. Descriptor/UI revision labels differ(2.0.2/2.0.3); this is recorded rather than a claim of a proven single version. See source_manifest.json for current local baseline hashes.','',
  '- Native layout:05_israel.txt:47-76,117-127 and shortcuts15-44;05_russia.txt:51-165;00_generic.txt:54-150. Relative anchors, short spines,2-4column forks and grouped joins. This compact arrangement is adapted, not copied coordinates.',
  '- Presentation calibration: Russia putinism focus389-413(named spirit,50PP,+2%stability); army reform23088-23108(+5%special-forces attack/defence,-20%training); Slavneft34216-34251(-2treasury and assets). These large-country amounts are not copied.',
  '- Exact party predicates:common/scripted_triggers/01_political_triggers.txt:176,183,197 for slots1,2,4.',
  '- Fiscal modifiers and readers:common/modifier_definitions/money_modifier_definitions.txt:51,65,72,268,353;common/scripted_effects/00_money_system.txt:3354,3417,3519,532-536,6094. Literal agricultural key is agric olture with no space:agricolture_productivity_modifier. Health key is health_cost_multiplier_modifier.',
  '- Influence:common/modifier_definitions/influence_modifier_definitions.txt:1 andcommon/scripted_effects/00_influence_scripted_effects.txt:253-265.',
  '- Native construction/efficiency:main MDcommon/ideas/!_generic_faction_goals.txt:6,15;03_CHI_NKO_joint.txt:9,18,28;03_CHI_SOV_joint.txt:9.',
  '- Research:main MDturkey.txt:3189-3199(CAT_infantry),05_israel.txt:29600-29608(CAT_industry),30479-30485(CAT_naval). Doctrine API:add_doctrine_cost_reduction,05_israel.txt:13045-13056.',
  '- Weekly money integration:00_money_system.txt:817/3686 resets income/expense accumulators;4749 derives treasury_rate. ExistingCOLDWAR_USA_1970_agreements.txt:2890-2910 is an idempotent recurring-stream precedent. Monthly agreement caching is the requested new policy, separate from native bookkeeping.',
  '- Main MDcommon/dynamic_modifiers/README.md explicitly recommends owning add/remove transitions instead of recurring enable checks. Apply that rule to three CYP party programmes.',
  '- Sanction precedent:tools/cuba_1970/bilateral.py:77-99 checks four classes, two mirrored directions, both signatories, and native embargo/war. This is a contract reference, not proof that new events/hooks have been implemented.',
  '- Every modifier in this concept has a native MD source use or custom definition/consumer reference. Native loading, numeric formatting, event response delivery, current capacity, all transition hooks, EEC integration and live MP still require implementation testing.','',
 '## Historical references','']
 for s in SOURCES.values():lines+=['- ['+s['title']+']('+s['url']+'): '+s['note']]
 lines+=['','## Approval and retirement boundary','',
 'Approval authorizes a separate implementation step. Retire the old generated focus tree together with its generator, focus-ID consumers, history load/initialize calls, daily observer, old party programmes and superseded decisions. Preserve unrelated regional portraits, characters, native later history and other countries integrations. Keep original approved snapshots immutable. Archive old runtime privately on E:/MDColdWar_Backups/Codex_Test_Archives before removal; no archive is written inside the mod. This design does not silently delete the existing implementation while its replacement awaits review.','',
 'Checks:100unique IDs;100unique grid positions;reciprocal exclusions;all grouped prerequisite histories satisfiable;allbuilding slots match granted levels;noen/emdashesinplayertext. Visual rendering and independent review results are recorded separately. No HOI4or multiplayer test claimed.']
 lines+=['','Treaty transition caveat: immediate war/sanction/embargo changes require actual native or owning scripted hooks. Their complete coverage has not yet been implemented or verified. A monthly fallback alone can detect an unhooked change up to one month late. This concept does not promise instant suspension for an unobserved native action. There is no performance justification to silently reintroduce a daily or weekly observer.','',
  'Communal ratification: the two constitutional branch focuses send terms through response events. Their complete numeric benefits and costs are visible before acceptance, but are executed only after all required local and foreign ratifications. The selected branch remains selected after refusal; a new negotiated focus proposal needs a separately designed continuation rather than a hidden decision menu.']
 (OUT/'CONCEPT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 # High-resolution overview retains every focus label and exactly the inspector coordinates.
 svg=['<!-- IMPERIA COLD WAR — Cyprus compact concept, not a game screenshot. -->',
  '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="8500" height="2800" viewBox="0 0 8500 2800">',
  '<rect width="8500" height="2800" fill="#20282a"/>',
  '<text x="80" y="35" fill="#e7e3d1" font-family="Arial" font-size="22">IMPERIA COLD WAR: Cyprus1970, 100-focus concept. Approval pending.</text>', '<defs>']
 for g in GROUP_ICON:svg.append(f'<image id="icon-{g}" width="85" height="85" xlink:href="{data["art"][g]}"/>')
 svg.append('</defs>')
 by={f['key']:f for f in F}
 for f in F:
  x,y=f['x']*85+30,f['y']*130+65
  for group in f['prerequisites']:
   for key in group:
    p=by[key];px,py=p['x']*85+30,p['y']*130+65;mid=(py+85+y)/2
    svg.append(f'<path d="M{px+82},{py+108} V{mid} H{x+82} V{y+5}" fill="none" stroke="#829086" stroke-width="2"/>')
  for key in f['exclusive']:
   if key>f['key']:
    p=by[key];px,py=p['x']*85+30,p['y']*130+65
    svg.append(f'<path d="M{x+125},{y+45} H{px+40}" fill="none" stroke="#c8b778" stroke-width="3" stroke-dasharray="7 5"/>')
 for g,t,x,y,n in GROUPS:svg.append(f'<text x="{x*85-150}" y="{max(52,y*130+40)}" fill="#c8b778" font-family="Arial" font-size="21">{html.escape(t)} ({n})</text>')
 for f in F:
  x,y=f['x']*85+30,f['y']*130+65
  svg.extend([f'<use xlink:href="#icon-{f["group"]}" x="{x+40}" y="{y}"/>',
   f'<rect x="{x+5}" y="{y+85}" width="155" height="32" fill="#35413c" stroke="#677063"/>',
   f'<text x="{x+82}" y="{y+105}" text-anchor="middle" fill="#ece4c8" font-family="Arial" font-size="12">{html.escape(f["title"])}</text>'])
 svg.append('</svg>')
 (OUT/'full-tree.svg').write_text('\n'.join(svg)+'\n',encoding='utf-8')
 template=(Path(__file__).parent/'preview.html').read_text('utf-8')
 fragment=template.replace('/*__CONCEPT__*/',json.dumps(data,ensure_ascii=False,separators=(',',':')))
 fragment=fragment.replace('/*__INTERVENTION_JS__*/',(Path(__file__).parent/'intervention-preview.js').read_text('utf-8'))
 (VIS/'cyprus-1970-rework.html').write_text(fragment,encoding='utf-8')
 # A standalone local review copy is useful alongside the durable design files.
 (OUT/'preview.html').write_text('<!doctype html><!-- IMPERIA COLD WAR — Cyprus compact concept. --><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>IMPERIA COLD WAR: Cyprus1970</title><body style="margin:0;background:#1e2424;color:#e8e5d8;font:14px Arial">'+fragment+'</body></html>',encoding='utf-8')
 print(json.dumps(report))

if __name__=='__main__':main()
