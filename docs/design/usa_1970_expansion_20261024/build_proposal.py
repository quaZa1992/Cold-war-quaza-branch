# IMPERIA COLD WAR — USA expansion concept catalogue.
"""Build review data only. Does not emit or change loaded game files."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
current = json.loads((HERE / 'current_inventory.json').read_text(encoding='utf-8'))
live = {n['id']: n for n in current['focuses']}
nodes = []

def node(key, name, module, xy, parents, effects, description, *, days=42, replace=None, exclude=(), requirements=(), lifetime='Standing national programme', history='Plausible policy alternative; numeric balance proposal', technical=''):
    item = dict(id=key, name=name, module=module, xy=xy, prerequisites=[[p] if isinstance(p,str) else p for p in parents], mutually_exclusive=list(exclude), days=days, effects=effects, description=description, requirements=list(requirements), lifetime=lifetime, history=history, technical=technical, status='Rework' if replace else 'New')
    if replace:
        item['replaces'] = replace
        item['source_line'] = live[replace]['line']
        item['xy'] = [live[replace]['resolved_x'], live[replace]['resolved_y']]
    nodes.append(item)
    return item

def revise(suffix, name, module, effects, description, **kwargs):
    key='USA_1970_'+suffix
    kwargs.setdefault('days',round(float(live[key]['cost'])*7,1))
    return node(key,name,module,[0,0],[],effects,description,replace=key,**kwargs)

def new(suffix,name,module,xy,parents,effects,description,**kwargs):
    return node('USA_X_'+suffix,name,module,xy,parents,effects,description,**kwargs)

# The listed spirit values are final programme packages replacing overlapping
# current helpers, not additional layers on top of the entire existing route.
a=revise('E1','Federal Industrial Grants','Industry',[
    'Treasury: -$30.00 billion','Add National Industrial Renewal: factory output +5%; production efficiency growth +5%; consumer goods factor +1%',
    'Great Lakes industrial programme: 2 civilian factories; +2 shared building slots'],
    'Federal procurement and modernisation grants can keep older industrial regions competitive. Long-term employment and supplier capacity take priority over the cheapest immediate return.',
    exclude=['USA_1970_E2'],history='Regional industrial renewal is a policy extrapolation from existing federal development and procurement; MD mechanical benchmark: USA_focus_from_rust_to_refined.',technical='Replace E1 output/bureaucracy rewards; final recipient states selected from actual US-owned, controlled eligible Great Lakes states.')
b=revise('E2','Market Investment Zones','Industry',[
    'Treasury: -$20.00 billion','Add Competitive Investment Zones: construction speed +7%; maximum production efficiency +3%; tax collection efficiency -2%',
    'Metropolitan development programme: 2 office levels; +2 shared building slots'],
    'Investment zones trade a narrower tax base for faster private investment. New commercial centres gain an advantage while industrial renewal depends more heavily on private demand.',exclude=['USA_1970_E1'])
new('industrial_tools','Modern Machine-Tool Contracts','Industry',[-25,8],['USA_1970_E1'],[
    'Treasury: -$12.00 billion','2 x 50% research bonuses: industry','Modify National Industrial Renewal: factory output +2%; production efficiency growth +3%'],
    'Federal contracts give domestic machine-tool firms an assured market. Modern equipment improves the plants already receiving industrial assistance.',requirements=['National Industrial Renewal is active'])
new('industrial_skills','Community College Partnerships','Industry',[-25,9],['USA_X_industrial_tools'],[
    'Treasury: -$8.00 billion','Modify National Industrial Renewal: production efficiency retention +5%; education cost +2%'],
    'Local colleges and industrial employers can share responsibility for technical training. Reliable skills matter as much as replacement machinery.',requirements=['National Industrial Renewal is active'])
new('venture_tools','Small Business Investment Partnerships','Industry',[-21,8],['USA_1970_E2'],[
    'Treasury: -$10.00 billion','2 x 50% research bonuses: electronics','Modify Competitive Investment Zones: production efficiency growth +5%; construction speed +2%'],
    'Investment partnerships bring capital to specialised suppliers and young technology firms. Regional growth becomes more dependent on an active private investment market.',requirements=['Competitive Investment Zones is active'])
new('export_credit','Export Credit Facilities','Industry',[-21,9],['USA_X_venture_tools'],[
    'Treasury: -$8.00 billion','Modify Competitive Investment Zones: factory output +3%; tax collection efficiency -1%','Unlock decision: Export Credit Guarantees'],
    'Export credit can turn competitive new firms into durable overseas suppliers. The Treasury accepts a smaller immediate return in exchange for broader industrial markets.',requirements=['Competitive Investment Zones is active'])

revise('E10','The Information Economy','Civil priorities',[
    'Treasury: -$25.00 billion','Add Civilian Technology Network: research speed +3%; production efficiency growth +5%; education cost +3%',
    '2 x 50% research bonuses: electronics'],
    'Civilian laboratories, universities and electronics suppliers can turn public research into a wider industrial capability. Education and procurement remain continuing commitments.',exclude=['USA_1970_E11'])
revise('E11','The Post-Industrial Bargain','Civil priorities',[
    'Treasury: -$25.00 billion','Add Regional Adjustment Compact: stability +4%; production efficiency retention +8%; consumer goods factor +1%',
    'Regional adjustment programme: 2 office levels; +2 shared building slots'],
    'Retraining, redevelopment and local employment agreements give communities a greater stake in structural change. Adjustment is slower and more expensive than leaving displaced workers to absorb it alone.',exclude=['USA_1970_E10'])
new('commercial_labs','Civilian Technology Demonstrators','Civil priorities',[-25,11],['USA_1970_E10'],[
    'Treasury: -$10.00 billion','2 x 50% research bonuses: industry','Modify Civilian Technology Network: factory output +2%'],
    'Demonstration contracts help firms take promising laboratory designs into industrial use. Public funding supports practical applications rather than speculative breakthroughs.')
new('redevelopment','Industrial Site Redevelopment','Civil priorities',[-21,11],['USA_1970_E11'],[
    'Treasury: -$12.00 billion','Industrial redevelopment: 2 civilian factories; +2 shared building slots','Modify Regional Adjustment Compact: construction speed +3%'],
    'Cleared industrial sites and existing transport links can support new employment. The programme concentrates assistance on regions already facing the costs of economic change.')

# Ordinary nuclear, conservation, grid and hydrocarbon development stay shared.
# Only the first major discretionary federal demonstration appropriation forks.
new('nuclear_priority','Standard Reactor Demonstrations','Energy',[-33,7],[['USA_1970_N3','USA_1970_N6']],[
    'Treasury: -$30.00 billion','Add Standard Reactor Programme: nuclear energy generation +10%; nuclear-reactor construction speed +10%; research speed +2%','Weekly programme expense: -$0.03 billion',
    '2 x 50% research bonuses: nuclear technology'],
    'A first federal demonstration appropriation can standardise reactor design and concentrate engineering experience. Large projects require stable long-term financing.',exclude=['USA_X_efficiency_priority'],technical='Specific construction modifier/category must be verified against current MD technology/building providers before implementation. No uranium production or mines are granted.')
new('efficiency_priority','Industrial Energy Audits','Energy',[-29,7],['USA_1970_N6'],[
    'Treasury: -$18.00 billion','Add Industrial Energy Efficiency: energy consumption -6%; factory output +3%','Add Retrofit Adjustment for 730 days: construction speed -2%',
    'Industrial retrofit programme: 2 infrastructure levels; +2 shared building slots'],
    'The first major demonstration appropriation can instead reduce industrial energy demand through retrofits and practical engineering. Construction is temporarily diverted toward existing facilities.',exclude=['USA_X_nuclear_priority'],technical='Energy-consumption sign and consumer must be verified in the current MD energy system. Construction malus is proposed for the 730-day retrofit phase only; other gains remain standing.')
new('nuclear_training','Reactor Engineering Schools','Energy',[-33,8],['USA_X_nuclear_priority'],[
    'Treasury: -$10.00 billion','Modify Standard Reactor Programme: research speed +1%; education cost +2%'],
    'Dedicated engineering courses make standard designs easier to operate and maintain. Safe operation requires a durable technical workforce.')
new('efficiency_standards','Appliance and Industrial Standards','Energy',[-29,8],['USA_X_efficiency_priority'],[
    'Treasury: -$8.00 billion','Modify Industrial Energy Efficiency: energy consumption -2%; production efficiency retention +4%'],
    'Practical standards extend energy savings beyond the first industrial retrofits. Existing manufacturers receive a predictable schedule for adapting their products.')

revise('D1','The All-Volunteer Force','Force structure',[
    'Treasury: -$15.00 billion','Change military law: Draft Army to Volunteer Army',
    'Native law change: recruitable population -2.5 percentage points; division organisation +20%; organisation regain +20%; army attack +20%; army defence +20%; core attack -20%; core defence -20%; training time +20%; personnel cost +80%; workforce +1.5%; migration factor +10%; daily army experience +0.04; daily naval experience +0.02; daily air experience +0.02',
    'Add Professional Force Establishment: division organisation +3%; army experience gain +5%; training time +3%'],
    'A professional force offers continuity, technical competence and a more stable relationship with civilian society. Better pay and longer preparation make each formation more expensive.',exclude=['USA_1970_D2'],history='Gates Commission and US all-volunteer transition, 1968 to 1974; Army Center of Military History.')
revise('D2','Renew National Service','Force structure',[
    'Treasury: -$10.00 billion','Retain military law: Draft Army',
    'Draft Army: recruitable population 5%; division organisation -10%; organisation regain -10%; army attack -20%; army defence -20%; core attack +20%; core defence +20%; training time -20%; daily army experience +0.02; daily naval experience +0.01; daily air experience +0.01; workforce -4%; migration factor -10%',
    'Add National Service Establishment: recruitable population factor +8%; training time -8%; army experience gain +5%; stability -2%'],
    'A renewed selective-service system sustains a larger reserve of trained citizens. Broader participation improves mobilisation at a continuing political cost.',exclude=['USA_1970_D1'],history='Credible continuation of selective service; alternate to the historical volunteer transition.')
new('nco_corps','Career NCO Development','Force structure',[21,7],['USA_1970_D1'],[
    'Treasury: -$8.00 billion','Modify Professional Force Establishment: organisation regain +5%; training time +2%','1 x 50% land doctrine cost reduction'],
    'Experienced noncommissioned officers turn technical training into reliable unit leadership. Career development requires additional time before a formation is ready.')
new('reserve_readiness','Reserve Equipment Pools','Force structure',[25,7],['USA_1970_D2'],[
    'Treasury: -$8.00 billion','Modify National Service Establishment: mobilisation speed +10%; equipment cost +2%','Army experience: +25'],
    'Standard equipment pools and regular reserve exercises make national service useful after initial training. Maintaining equipment outside active units has a continuing cost.')
revise('D3','Intelligence under Law','Intelligence',[
    'Treasury: -$5.00 billion','Add Statutory Intelligence Oversight: stability +3%; counterintelligence +5%; intelligence agency upgrade time +5%'],
    'Legislative oversight can restore confidence in intelligence institutions and improve the defence against foreign penetration. Formal review slows the expansion of sensitive programmes.',exclude=['USA_1970_D4'],technical='Independent of military procurement doctrine; agency modifier scope requires native-provider verification.')
revise('D4','Keep the Covert Hand Free','Intelligence',[
    'Treasury: -$5.00 billion','Add Executive Intelligence Direction: civilian intelligence +5%; intelligence agency upgrade time -10%; stability -2%'],
    'Central executive direction gives intelligence agencies more freedom to organise overseas programmes. Wider discretion increases the political cost of secrecy at home.',exclude=['USA_1970_D3'])
new('army_mass','Sustained Continental Operations','Army doctrine',[21,9],['USA_1970_D5'],[
    'Treasury: -$15.00 billion','Add Continental Sustainment Doctrine: supply consumption -6%; planning speed +10%; army fuel consumption +3%',
    '2 x 50% land doctrine cost reductions'],
    'A continental force needs maintenance, transport and command arrangements suited to prolonged combined-arms operations. Heavy formations remain costly to move.',exclude=['USA_X_army_precision'],history='Post-Vietnam combined-arms reform; later AirLand Battle is a follow-through rather than a 1970 starting doctrine.')
new('army_precision','Precision and Rapid Deployment','Army doctrine',[25,9],['USA_1970_D5'],[
    'Treasury: -$18.00 billion','Add Rapid Deployment Doctrine: division organisation +3%; planning speed +5%; equipment cost +3%',
    '2 x 50% research bonuses: eligible 1970-period aircraft and electronics'],
    'Mobile formations and precision systems promise more useful force without a larger permanent overseas army. Expensive equipment and specialist support limit how widely the model can be applied.',exclude=['USA_X_army_mass'],technical='Resolve exact current MD aircraft/electronics categories and the existing Second Offset rewards before integration; no ahead-of-time unlocks.')
new('logistics_schools','Joint Logistics Schools','Army doctrine',[21,10],['USA_X_army_mass'],[
    'Treasury: -$8.00 billion','Modify Continental Sustainment Doctrine: organisation regain +3%','Army experience: +25'],
    'Joint logistics instruction gives headquarters a common language for transport and maintenance. The benefit is operational endurance rather than a universal increase in combat power.')
new('test_ranges','Joint Operational Test Ranges','Army doctrine',[25,10],['USA_X_army_precision'],[
    'Treasury: -$8.00 billion','1 x 50% air doctrine cost reduction','Air experience: +25'],
    'Operational trials connect new sensors and weapons to realistic deployment plans. Evaluation follows actual service requirements rather than speculative technology.')
new('sea_control','Carrier Sea Control','Naval priorities',[21,12],['USA_1970_D6'],[
    'Treasury: -$20.00 billion','Add Carrier Readiness Programme: naval organisation +5%; naval experience gain +10%; naval personnel cost +4%',
    '2 x 50% naval doctrine cost reductions'],
    'Carrier readiness concentrates funds on air groups, escorts and sustained deployment. High readiness demands expensive maintenance and replacement equipment.',exclude=['USA_X_sea_denial'])
new('sea_denial','Atlantic Escort and Undersea Warfare','Naval priorities',[25,12],['USA_1970_D6'],[
    'Treasury: -$15.00 billion','Add Atlantic Escort Programme: convoy escort efficiency +8%; submarine detection +5%; naval personnel cost +3%',
    '2 x 50% research bonuses: eligible destroyer and submarine technology'],
    'Escorts, maritime surveillance and undersea forces protect Atlantic communications. This priority favours dependable sea lanes over a larger visible carrier presence.',exclude=['USA_X_sea_control'],technical='Navy-specific modifier and research category names need exact live MD verification; design values are not claims of registered APIs.')

revise('S1','Federal Enforcement','Civil rights',[
    'Treasury: -$12.00 billion','Add Federal Civil Rights Enforcement: stability +4%; political power gain -3%; drift defence +5%',
    'Fair housing programme: 1 office level; +1 shared building slot'],
    'Federal enforcement establishes a consistent national standard for civil rights. Implementing that standard spends political capital and requires institutions capable of defending it.',exclude=['USA_1970_S2'])
revise('S2','State-Negotiated Compliance','Civil rights',[
    'Treasury: -$8.00 billion','Add State Compliance Agreements: construction speed +4%; tax collection efficiency +2%; political power gain -2%',
    'State implementation programme: 2 infrastructure levels; +2 shared building slots'],
    'State implementation agreements combine enforceable civil-rights requirements with local investment. Negotiation takes longer and offers less immediate national political reassurance.',exclude=['USA_1970_S1'],technical='A credible implementation model with enforceable standards, not a reward for continued segregation. Slower relief of existing social tension is the opportunity cost.')
new('rights_legal_aid','Community Legal Services','Civil rights',[-16,7],['USA_1970_S1'],[
    'Treasury: -$6.00 billion','Modify Federal Civil Rights Enforcement: stability +1%; consumer goods factor +0.5%'],
    'Local legal services make federal protections usable in everyday disputes. Durable rights require access to institutions as well as statutory language.')
new('rights_local_projects','Local Compliance Investment','Civil rights',[-12,7],['USA_1970_S2'],[
    'Treasury: -$10.00 billion','Local redevelopment programme: 1 civilian factory; +1 shared building slot','Modify State Compliance Agreements: production efficiency retention +3%'],
    'Local investment gives negotiated compliance a practical economic foundation. Public money follows implementation rather than promises alone.')

# Foreign doctrine remains a national choice; geography stays broadly reachable.
revise('F1',"The Salesman's Republic",'Foreign doctrine',[
    'Add Commercial Diplomacy Mandate: factory output +2%; production efficiency growth +3%; war support -2%'],
    'Commercial statecraft makes export credit and civilian contracts the preferred instruments of influence. It leaves less political room for expensive security commitments.',exclude=['USA_1970_F2','USA_1970_F3'])
revise('F2','Rules-Based Leadership','Foreign doctrine',[
    'Add Multilateral Diplomacy Mandate: political power gain +3%; stability +2%; bureaucracy cost +1%'],
    'Multilateral consultation gives commitments greater legitimacy and a wider institutional base. Negotiation and shared standards make those programmes more expensive.',exclude=['USA_1970_F1','USA_1970_F3'])
revise('F3','The Interventionist Will','Foreign doctrine',[
    'Add Security Assistance Mandate: army experience gain +5%; war support +3%; personnel cost +2%','1 x 50% land doctrine cost reduction','1 x 50% air doctrine cost reduction'],
    'A more active security policy favours training missions and sustained military readiness. Maintaining that posture requires a larger foreign programme budget.',exclude=['USA_1970_F1','USA_1970_F2'],technical='No forced intervention or third-country war. Doctrine cannot bypass recipient authority.')

def offer(suffix, name, module, xy, parents, participants, description, *, exclude=(), requirements=(), history='', technical='', days=35, lifetime='Standing; no fixed expiry'):
    item=new(suffix,name,module,xy,parents,[],description,days=days,exclude=exclude,requirements=requirements,lifetime=lifetime,history=history or 'Historically grounded negotiated extension; all numerical terms are balance proposals.',technical=technical)
    item['offer']=participants
    item['common_requirements']=['Both signatories exist','Bilateral peace','No native bilateral embargo or Imperia diplomatic, financial, economic or military sanctions in either direction','No conflicting active agreement in the same family']
    return item

def party(spirit, rows, **extra):
    return dict(spirit=spirit,effects=rows,**extra)

offer('germany_forward','Bonn Forward Defence Agreement','Atlantic',[10,7],['USA_1970_F4'],{
    'USA':party('Forward Defence Commitments',['Treasury: -$8.00 billion','Weekly programme expense: -$0.04 billion','Weekly offset income from West Germany: +$0.02 billion','Division organisation: +3%','Planning speed: +5%','Personnel cost: +3%']),
    'GER':party('Atlantic Forward Defence',['Treasury: -$4.00 billion','Weekly offset payment to the United States: -$0.02 billion','Division organisation: +4%','Organisation regain: +4%','Equipment cost: +2%','1 x 50% land doctrine cost reduction'])},
    'Bonn and Washington can renew forward defence on the basis of shared readiness and a negotiated financial offset. West German support helps sustain an American commitment whose political and operating costs remain visible.',
    exclude=['USA_X_germany_sustain'],requirements=['United States and West Germany have the actual active NATO membership spirit'],history='FRUS 1969-1976, Volume XLI, documents 57, 77 and 78: real 1971 offset negotiations and signed agreement.',technical='Offset income and GER expense must be one matched weekly transfer. USA gross recurring cost 0.04, income 0.02, net cost 0.02. Do not reduce the operating cost twice. Native NATO membership idea ID must be resolved.')
offer('germany_sustain','Bonn European Sustainment Agreement','Atlantic',[14,7],['USA_1970_F4'],{
    'USA':party('European Sustainment Partnership',['Treasury: -$8.00 billion','Weekly programme expense: -$0.02 billion','Personnel cost: -2%','Army experience gain: +3%','Equipment cost: +1%']),
    'GER':party('European Maintenance Capacity',['Treasury: -$8.00 billion','Weekly programme expense: -$0.02 billion','Supply consumption: -5%','Factory output: +3%','Personnel cost: +2%','Maintenance facilities: 1 military factory; +1 shared building slot','1 x 50% industry research bonus'])},
    'A different offset settlement places more maintenance and sustainment responsibility in West German hands. It offers less forward American readiness in exchange for a stronger local support base.',exclude=['USA_X_germany_forward'],requirements=['United States and West Germany have the actual active NATO membership spirit'],history='Alternative balance of procurement and local support within the documented offset debate. Not a claim that this exact package existed.')
offer('canada','Expand the Auto Pact','Atlantic',[18,7],['USA_1970_E9'],{
    'USA':party('Continental Production Networks',['Treasury: -$6.00 billion','Factory output: +3%','Production efficiency retention: +4%','Tax collection efficiency: -1%','1 x 50% industry research bonus']),
    'CAN':party('Continental Supplier Development',['Treasury: -$4.00 billion','Factory output: +4%','Production efficiency growth: +5%','Tax collection efficiency: -1%','Supplier development: 1 civilian factory; +1 shared building slot','1 x 50% industry research bonus'])},
    'The existing automotive agreement provides a foundation for deeper supplier integration. Both governments can expand industrial cooperation while accepting reduced fiscal flexibility in the protected sectors.',history='1965 Canada-US Automotive Products Agreement; expansion rather than founding a new 1970 trade bloc.')
offer('britain','North Atlantic Escort Exercises','Atlantic',[22,7],['USA_1970_F4'],{
    'USA':party('Atlantic Escort Exercises',['Treasury: -$3.00 billion','Weekly programme expense: -$0.01 billion','Convoy escort efficiency: +5%','Naval equipment cost: +2%','Naval experience: +20','1 x 50% naval doctrine cost reduction']),
    'ENG':party('Atlantic Escort Exercises',['Treasury: -$2.00 billion','Weekly programme expense: -$0.01 billion','Convoy escort efficiency: +5%','Naval equipment cost: +2%','Naval experience: +20','1 x 50% naval doctrine cost reduction'])},
    'A time-limited exercise programme develops common escort procedures and maritime coordination. Both navies carry the maintenance burden of a more active deployment schedule.',requirements=['Both countries have actual active NATO membership'],lifetime='365 days from acceptance',history='NATO January 1969 communiqué: naval cooperation, force plans and common infrastructure.',technical='No permanent free XP loop; repeat exercises require a newly priced joint renewal with a 365-day cooldown after expiry.')
offer('japan','Pacific Alliance Consultation','Pacific',[10,10],['USA_1970_NIX_F6'],{
    'USA':party('Consultative Pacific Presence',['Treasury: -$5.00 billion','Weekly programme expense: -$0.02 billion','Supply consumption: -3%','Naval organisation: +3%','Political power gain: -1%']),
    'JAP':party('Consultative Pacific Partnership',['Treasury: -$3.00 billion','Production efficiency retention: +4%','Convoy escort efficiency: +4%','Personnel cost: +2%','1 x 50% naval doctrine cost reduction'])},
    'A consultative basing arrangement can preserve American access while giving Japan a greater political role in regional security. Readiness is balanced against the obligations of consultation.',history='1969 consultations and 1971 Okinawa Reversion Agreement.',technical='Do not transfer state 618: JAP already owns it in the current 1970 map. State 827 is a distinct US base. Any future transfer/access change is a separate recipient-approved transaction.')
offer('south_vietnam','A Defined Advisory Mission','Pacific',[14,10],['USA_1970_NIX_V5'],{
    'USA':party('Limited Advisory Commitment',['Treasury: -$5.00 billion','Weekly programme expense: -$0.04 billion','Army experience gain: +5%','Personnel cost: +2%','Army experience: +15']),
    'SVN':party('National Training Mission',['Treasury: -$1.00 billion','Division organisation: +5%','Training time: -5%','Personnel cost: +3%','Army experience: +20','1 x 50% land doctrine cost reduction'])},
    'A clearly defined mission can strengthen South Vietnamese training without making acceptance an automatic American entry into war. The host government chooses whether the commitment suits its own strategy.',lifetime='730 days from acceptance',history='Nixon Doctrine and Vietnamization; exact programme is a balance proposal.',technical='Verified recipient SVN: history/countries/SVN - South Vietnam.txt. VIE is North Vietnam in January 1970. No equipment creation or transfer promised in this package.')
offer('china','A Limited Commercial Opening','Rival diplomacy',[10,13],['USA_1970_NIX_F4'],{
    'USA':party('Sino-American Commercial Contacts',['Treasury: -$4.00 billion','Factory output: +2%','Production efficiency growth: +3%','Tax collection efficiency: -1%']),
    'CHI':party('Sino-American Commercial Contacts',['Treasury: -$2.00 billion','Factory output: +3%','Production efficiency growth: +4%','Political power gain: -2%','1 x 50% industry research bonus'])},
    'Limited commercial contacts can test the value of a wider relationship without settling the Taiwan question. Each government accepts modest domestic adjustment in exchange for new industrial opportunities.',requirements=['Accepted Beijing channel and commercial negotiations'],history='Shanghai Communiqué and rapprochement, 1972.',technical='No automatic recognition change, ROC status change, faction membership or Taiwan cession. Existing national embargo must first be eased through explicit mutually approved relief, not silently bypassed.')
offer('soviet_exchange','Scientific Exchange with Moscow','Rival diplomacy',[14,13],['USA_1970_NIX_F5'],{
    'USA':party('Soviet-American Scientific Exchange',['Treasury: -$4.00 billion','Weekly programme expense: -$0.01 billion','Research speed: +2%','Counterintelligence: -2%','1 x 50% industry research bonus']),
    'SOV':party('Soviet-American Scientific Exchange',['Treasury: -$4.00 billion','Weekly programme expense: -$0.01 billion','Research speed: +2%','Counterintelligence: -2%','1 x 50% industry research bonus'])},
    'A limited scientific exchange turns diplomatic access into practical civilian cooperation. Both governments gain expertise while accepting a more open institutional relationship.',lifetime='730 days from acceptance',history='Civilian cooperation within détente is a historically grounded extension. Coordinate space cooperation with the existing Cold War space system.',technical='This is not SALT and grants no pretend strategic limits. A separate arms-control treaty requires explicit integration with the actual nuclear programme and equal enforcement for both signatories.')
offer('bahrain','Bahrain Naval Facilities Agreement','Middle East',[18,10],['USA_1970_F6'],{
    'USA':party('Bahrain Support Facilities',['Treasury: -$6.00 billion','Weekly facility payment to Bahrain: -$0.02 billion','Naval organisation: +3%','Supply consumption: -2%','Naval equipment cost: +2%']),
    'BHR':party('Naval Facilities Partnership',['Treasury: +$6.00 billion','Weekly facility income: +$0.02 billion','Construction speed: +4%','Stability: -1%','Port support programme: 1 naval-base level; +1 shared building slot'])},
    'A facilities agreement offers Bahrain an income and infrastructure package while preserving its territorial sovereignty. The United States gains support capacity at a continuing financial and political cost.',history='Negotiated naval facilities are plausible in the context of Britain\'s Gulf withdrawal; verify precise historical terms before implementation.',technical='New optional alternative to the current state-624 cession offer, not a silent rewrite of the already implemented Bahrain route. Cannot coexist with state cession in the same agreement family. Six-billion setup transfer is matched, not newly minted USA income.')
offer('israel','Defensive Industrial Assistance','Middle East',[22,10],['USA_1970_F6'],{
    'USA':party('Defensive Supply Partnership',['Treasury: -$8.00 billion','Weekly programme expense: -$0.03 billion','Production efficiency retention: +3%','Equipment cost: +1%','Army experience: +15']),
    'ISR':party('Defensive Industrial Assistance',['Treasury: -$2.00 billion','Equipment cost: -3%','Division defence: +3%','Personnel cost: +2%','Industrial support: 1 military factory; +1 shared building slot','1 x 50% land doctrine cost reduction'])},
    'A defensive industrial programme can support Israeli readiness through training and production capacity. American funding carries a continuing cost without settling any territorial dispute.',lifetime='730 days from acceptance',history='Existing US-Israeli assistance channel, Rogers diplomacy and 1970 regional security debates.',technical='Check existing Israel/AIPAC and supplier deals so these benefits replace the same aid package rather than stack with duplicate versions.')
offer('saudi','Saudi Technical Services Commission','Middle East',[26,10],['USA_1970_F6'],{
    'USA':party('Saudi Technical Contracts',['Treasury: -$3.00 billion','Weekly technical-service income from Saudi Arabia: +$0.02 billion','Factory output: +2%','Production efficiency retention: -1%']),
    'SAU':party('Technical Development Commission',['Treasury: -$8.00 billion','Weekly technical-service payment: -$0.02 billion','Construction speed: +5%','Factory output: +3%','Education cost: +2%','1 x 50% industry research bonus'])},
    'Technical services and industrial training can broaden an energy relationship into civilian development. Saudi funding supports foreign expertise while creating a continuing dependence on specialist services.',requirements=['1974 or a separately negotiated early commission'],history='US-Saudi Joint Commission established in 1974; an earlier start is explicitly alternate history.',technical='No automatic oil flow, resource production, free refineries or guaranteed embargo immunity. Resource trade requires actual native transactions.')
offer('mexico','Border Industrial Development','Americas',[18,13],['USA_1970_E9'],{
    'USA':party('Border Production Partnership',['Treasury: -$8.00 billion','Production efficiency growth: +4%','Factory output: +2%','Tax collection efficiency: -1%']),
    'MEX':party('Border Industrial Development',['Treasury: -$3.00 billion','Construction speed: +4%','Production efficiency growth: +4%','Education cost: +2%','Border industrial programme: 1 civilian factory; +1 shared building slot','1 x 50% industry research bonus'])},
    'A negotiated expansion of border industry can connect Mexican employment and American supplier demand. Both governments retain control over labour and customs policy while funding the skills needed for integration.',history='Mexico\'s border industrialisation programme began in 1965; this is an additional negotiated programme, not NAFTA.',technical='Select an actual Mexican-owned, controlled border state; verify historical primary source before implementation. No workforce transfer or migration penalty.')
offer('rogers','A Renewed Rogers Initiative','Middle East',[18,16],['USA_1970_F6'],{
    'USA':party('Rogers Mediation Mandate',['Treasury: -$3.00 billion','Weekly programme expense: -$0.02 billion','Political power gain: +3%','War support: -2%']),
    'EGY':party('Rogers Negotiating Channel',['Treasury: -$1.00 billion','Political power: +25','Stability: +2%','Production efficiency retention: +3%','Army experience gain: -3%']),
    'ISR':party('Rogers Negotiating Channel',['Treasury: -$1.00 billion','Political power: +25','Stability: +2%','Production efficiency retention: +3%','Army experience gain: -3%'])},
    'A renewed mediation mandate gives Israel and Egypt separate opportunities to authorise talks. Diplomatic benefits begin only after all three governments have agreed on the mandate.',lifetime='180 days from final acceptance',history='Rogers II accepted by Israel and Egypt in 1970, establishing a three-month ceasefire.',technical='Three-party atomic activation: separate EGY and ISR recipient decisions, no benefits after only one response; final revalidation for all. This package opens talks, not an enforced peace, ceasefire, border change or Suez reopening.')

# Continuations give signed partnerships a second meaningful chapter.
new('atlantic_research','Transatlantic Standards Board','Atlantic',[12,9],[['USA_X_germany_forward','USA_X_germany_sustain']],[],
    'A second jointly approved programme can turn a successful defence relationship into practical industrial standards.',days=35,requirements=['Active signed German agreement'],lifetime='730 days from separate acceptance',technical='Requires a new recipient decision. Reuse offer lifecycle, not a unilateral follow-up reward.')['offer']={
        'USA':party('Transatlantic Standards Board',['Treasury: -$3.00 billion','Production efficiency retention: +3%','Education cost: +1%','1 x 50% industry research bonus']),
        'GER':party('Transatlantic Standards Board',['Treasury: -$3.00 billion','Production efficiency retention: +3%','Education cost: +1%','1 x 50% industry research bonus'])}
new('canada_retool','Joint Automotive Retooling','Atlantic',[18,9],['USA_X_canada'],[],
    'A second industrial programme can update established suppliers while dividing the investment between both governments.',days=35,requirements=['Active Continental Production Networks and Continental Supplier Development'],lifetime='730 days from separate acceptance')['offer']={
        'USA':party('Joint Automotive Retooling',['Treasury: -$8.00 billion','Maximum production efficiency: +3%','Consumer goods factor: +0.5%','1 civilian factory; +1 shared building slot']),
        'CAN':party('Joint Automotive Retooling',['Treasury: -$5.00 billion','Maximum production efficiency: +3%','Consumer goods factor: +0.5%','1 civilian factory; +1 shared building slot'])}
new('pacific_maintenance','Pacific Maintenance Standards','Pacific',[10,12],['USA_X_japan'],[],
    'Shared maintenance standards can make a consultative partnership operationally useful without enlarging the territorial footprint.',days=35,requirements=['Active Consultative Pacific Presence and Consultative Pacific Partnership'],lifetime='730 days from separate acceptance')['offer']={
        'USA':party('Pacific Maintenance Standards',['Treasury: -$3.00 billion','Naval organisation: +2%','Naval equipment cost: +1%','1 x 50% naval doctrine cost reduction']),
        'JAP':party('Pacific Maintenance Standards',['Treasury: -$3.00 billion','Naval organisation: +2%','Naval equipment cost: +1%','1 x 50% naval doctrine cost reduction'])}

# Selected later administrations receive distinct internal appropriation
# priorities rather than another obligatory unlock of the already ruling party.
def election_choice(suffix,name,xy,parent,effects,description,party_name,exclusion,history):
    return new(suffix,name,'Election priorities',xy,[parent],effects,description,
        exclude=['USA_X_'+exclusion],requirements=[party_name+' is in power'],
        lifetime='Party programme; earned assets remain on a party change',history=history,
        technical='Use exact native western_liberals_are_in_power (Democratic Party, slot 2) or western_conservatism_are_in_power (Republican Party, slot 1) in availability, completion and programme activation. Keep this branch visible outside government. This is a specific appropriation priority, not a ban on complementary policies.')

election_choice('dem72_public','Public Employment Works',[-15,15],
    'USA_1970_1972_dem_2_jobs_before_fine_tuning',
    ['Treasury: -$18.00 billion','Add Public Employment Programme: construction speed +5%; stability +3%; consumer goods factor +1%','Urban investment: 2 infrastructure levels; +2 shared building slots'],
    'A Democratic recovery appropriation can put federal employment and public works first. Visible local improvements carry a larger ongoing public commitment.',
    'Democratic Party','dem72_hiring','Plausible 1972 Democratic recovery priority; employment programmes and federal job training are institutional precedents, not a claim this exact package passed.')
election_choice('dem72_hiring','Employment and Training Credits',[-11,15],
    'USA_1970_1972_dem_2_jobs_before_fine_tuning',
    ['Treasury: -$12.00 billion','Add Employment and Training Credits: factory output +4%; production efficiency growth +5%; tax collection efficiency -2%','1 x 50% industry research bonus'],
    'The same recovery appropriation can instead encourage private hiring and training. Firms gain flexibility while the Treasury accepts a narrower revenue base.',
    'Democratic Party','dem72_public','Alternate funding priority grounded in the period\'s work-incentive and job-training debates.')
new('dem72_public_follow','Neighbourhood Works Authorities','Election priorities',[-15,16],['USA_X_dem72_public'],[
    'Treasury: -$8.00 billion','Modify Public Employment Programme: construction speed +2%; bureaucracy cost +1%','Local offices: 1 office level; +1 shared building slot'],
    'Neighbourhood authorities give the employment programme a stable local administrative base. Local oversight turns a recovery appropriation into a continuing public institution.',requirements=['Democratic Party is in power'],lifetime='Democratic Party programme')
new('dem72_hiring_follow','Apprenticeship Partnerships','Election priorities',[-11,16],['USA_X_dem72_hiring'],[
    'Treasury: -$8.00 billion','Modify Employment and Training Credits: production efficiency retention +4%; education cost +2%'],
    'Employer and college partnerships turn hiring credits into durable skills. Public training support remains part of the programme after the first recovery contracts.',requirements=['Democratic Party is in power'],lifetime='Democratic Party programme')
election_choice('rep72_states','State Revenue Compacts',[11,18],
    'USA_1970_1972_rep_2_new_federalism_in_practice',
    ['Treasury: -$12.00 billion','Add State Revenue Compacts: construction speed +6%; bureaucracy cost -3%; tax collection efficiency -2%','State investment: 2 infrastructure levels; +2 shared building slots'],
    'Republican revenue sharing can give states broad discretion over a new development appropriation. Federal administration shrinks while Washington gives up part of its fiscal control.',
    'Republican Party','rep72_contracts','New Federalism and General Revenue Sharing are historical; the competing appropriation package is a balance proposal.')
election_choice('rep72_contracts','Federal Performance Contracts',[15,18],
    'USA_1970_1972_rep_2_new_federalism_in_practice',
    ['Treasury: -$12.00 billion','Add Federal Performance Contracts: production efficiency growth +5%; tax collection efficiency +2%; bureaucracy cost +2%','1 x 50% industry research bonus'],
    'The same appropriation can retain federal performance contracts and clear national priorities. More administration buys tighter oversight of how public investment is used.',
    'Republican Party','rep72_states','Plausible institutional alternative within debates over categorical aid and revenue sharing.')
new('rep72_states_follow','State Capital Programmes','Election priorities',[11,19],['USA_X_rep72_states'],[
    'Treasury: -$8.00 billion','Modify State Revenue Compacts: construction speed +2%','Regional development: 1 civilian factory; +1 shared building slot'],
    'Multi-year capital programmes let states plan beyond the first revenue-sharing payment. Physical development survives later changes of government.',requirements=['Republican Party is in power'],lifetime='Republican Party programme')
new('rep72_contracts_follow','National Procurement Standards','Election priorities',[15,19],['USA_X_rep72_contracts'],[
    'Treasury: -$8.00 billion','Modify Federal Performance Contracts: production efficiency retention +4%; factory output +2%'],
    'Common procurement standards make federal performance contracts more useful to specialist suppliers. Oversight produces a practical industrial result.',requirements=['Republican Party is in power'],lifetime='Republican Party programme')
election_choice('dem80_retool','Industrial Retooling Boards',[-15,29],
    'USA_1970_1980_dem_4_the_industrial_modernization_act',
    ['Treasury: -$20.00 billion','Add Industrial Retooling Boards: factory output +5%; production efficiency retention +5%; bureaucracy cost +2%','2 x 50% industry research bonuses'],
    'A Democratic modernisation appropriation can concentrate on existing industrial centres and shared investment boards. Stable production carries more public coordination.',
    'Democratic Party','dem80_newfirms','Plausible 1980 industrial-policy alternative, not an enacted historical institution.')
election_choice('dem80_newfirms','Regional Enterprise Funds',[-11,29],
    'USA_1970_1980_dem_4_the_industrial_modernization_act',
    ['Treasury: -$15.00 billion','Add Regional Enterprise Funds: construction speed +6%; production efficiency growth +5%; tax collection efficiency -2%','Regional enterprise programme: 1 office level; +1 shared building slot'],
    'The same modernisation appropriation can favour new firms and regional enterprise rather than established producers. Growth is more flexible but brings less immediate support for existing plants.',
    'Democratic Party','dem80_retool','Plausible alternative within late-1970s and 1980 industrial renewal debates.')
new('dem80_retool_follow','Supplier Renewal Contracts','Election priorities',[-15,30],['USA_X_dem80_retool'],[
    'Treasury: -$10.00 billion','Modify Industrial Retooling Boards: maximum production efficiency +3%','Industrial support: 1 civilian factory; +1 shared building slot'],
    'Supplier contracts bring smaller producers into industrial renewal. Modernisation reaches the firms on which major manufacturers depend.',requirements=['Democratic Party is in power'],lifetime='Democratic Party programme')
new('dem80_newfirms_follow','Regional Technology Centres','Election priorities',[-11,30],['USA_X_dem80_newfirms'],[
    'Treasury: -$10.00 billion','Modify Regional Enterprise Funds: research speed +1%; education cost +2%','1 x 50% electronics research bonus'],
    'Technology centres give new regional firms access to practical engineering support. Research funding follows local industrial needs.',requirements=['Democratic Party is in power'],lifetime='Democratic Party programme')
election_choice('rep80_invest','Accelerated Investment Allowances',[11,29],
    'USA_1970_1980_rep_4_supply_side_investment_zones',
    ['Treasury: -$12.00 billion','Add Accelerated Investment Allowances: factory output +5%; production efficiency growth +6%; tax collection efficiency -3%','1 x 50% industry research bonus'],
    'A Republican growth appropriation can favour rapid capital replacement through tax allowances. Stronger private investment comes with a visible loss of public revenue.',
    'Republican Party','rep80_fiscal','1981 tax and depreciation reform is historical; the specific alternative package is proposed game balance.')
election_choice('rep80_fiscal','Fiscal Consolidation Bargain',[15,29],
    'USA_1970_1980_rep_6_the_1981_budget_resolution',
    ['Treasury: -$8.00 billion','Add Fiscal Consolidation Bargain: tax collection efficiency +3%; bureaucracy cost -4%; construction speed +3%; stability -1%'],
    'The growth appropriation can instead be tied to a stronger fiscal settlement and administrative savings. A more reliable public balance carries a modest political cost.',
    'Republican Party','rep80_invest','Plausible conservative budget alternative; do not claim this exact compact passed historically.')
new('rep80_invest_follow','Capital Equipment Partnerships','Election priorities',[11,30],['USA_X_rep80_invest'],[
    'Treasury: -$10.00 billion','Modify Accelerated Investment Allowances: production efficiency retention +4%','1 x 50% industry research bonus'],
    'Capital equipment partnerships extend the investment allowance beyond large firms. Supplier upgrading makes the tax reform more durable.',requirements=['Republican Party is in power'],lifetime='Republican Party programme')
new('rep80_fiscal_follow','Federal Asset Modernisation','Election priorities',[15,30],['USA_X_rep80_fiscal'],[
    'Treasury: -$10.00 billion','Modify Fiscal Consolidation Bargain: construction speed +2%; production efficiency growth +3%'],
    'A consolidated budget leaves room to renew existing public assets. The programme uses the fiscal settlement for practical development rather than another abstract review.',requirements=['Republican Party is in power'],lifetime='Republican Party programme')

# Final review corrections are applied to the same catalogue used by the view.
layout_overrides={
    'USA_X_germany_sustain':[13,7], 'USA_X_canada':[16,7],
    'USA_X_britain':[19,7], 'USA_X_atlantic_research':[11.5,9],
    'USA_X_canada_retool':[16,9], 'USA_X_bahrain':[10,14],
    'USA_X_israel':[14,14], 'USA_X_saudi':[18,14],
    'USA_X_rogers':[14,16],
    'USA_X_dem80_retool':[-15,33], 'USA_X_dem80_newfirms':[-11,33],
    'USA_X_dem80_retool_follow':[-15,34], 'USA_X_dem80_newfirms_follow':[-11,34],
    'USA_X_rep80_invest':[11,33], 'USA_X_rep80_fiscal':[15,33],
    'USA_X_rep80_invest_follow':[11,34], 'USA_X_rep80_fiscal_follow':[15,34]
}
for item in nodes:
    if item['id'] in layout_overrides:item['xy']=layout_overrides[item['id']]
    item['effects']=[s.replace('counterintelligence','encryption').replace('Counterintelligence','Encryption').replace('naval equipment cost','naval personnel cost').replace('Naval equipment cost','Naval personnel cost') for s in item['effects']]
    for terms in item.get('offer',{}).values():
        terms['effects']=[s.replace('Counterintelligence','Encryption').replace('Naval equipment cost','Naval personnel cost') for s in terms['effects']]
    if item['id']=='USA_X_japan':
        item['prerequisites']=[['USA_1970_NIX_F6','USA_1970_F0']]
        item['requirements']=['Japan authorises the consultative mandate through this offer or an accepted existing channel']
    if item['id']=='USA_X_south_vietnam':
        item['prerequisites']=[['USA_1970_NIX_V5','USA_1970_F0']]
    if item['id']=='USA_X_china':
        item['prerequisites']=[['USA_1970_NIX_F4','USA_1970_F5']]
        item['requirements']=['China authorises commercial talks through this offer or the accepted Beijing channel']
    if item['id']=='USA_X_soviet_exchange':
        item['prerequisites']=[['USA_1970_NIX_F5','USA_1970_F5']]
    if item['id'] in ('USA_X_japan','USA_X_south_vietnam','USA_X_china','USA_X_soviet_exchange'):
        item['technical'] += ' Old Nixon focus completion is an optional entry receipt, not a compulsory predecessor. The permanent foreign-policy parent provides later presidents with a fresh recipient-approved channel. No old rejection flag permanently disables the new mandate.'
    if item['id']=='USA_X_bahrain':
        item['mutually_exclusive']=['COLDWAR_USA_bahrain_base_request']
        item['requirements'].append('No signed Bahrain territorial cession')
    if item['id']=='USA_X_rogers':
        item['common_requirements']=['USA, Egypt and Israel exist','USA is at peace with Egypt and with Israel','No USA-Egypt or USA-Israel embargo or any mirrored sanction class blocking the channel','Egyptian-Israeli war or sanctions do not themselves block talks','Both Egypt and Israel explicitly accept; USA consent is the signed offer']

proposal = dict(project='IMPERIA COLD WAR',status='Design only; not implemented',date='2026-10-24',nodes=nodes,
    balance_contract=[
        'All numerical terms are game-balance proposals in current MD treasury units, not converted historical budgets.',
        'Reworked spirit packages replace overlapping current helper rewards. Final mapping must reconcile starting burdens, Nixon decisions and all reachable later programmes.',
        'No new general research slot, free technology unlock, free division, forced ideology, puppet, war entry or territorial transfer is proposed.',
        'Plain construction always grants one extra shared slot per level in the actual receiving state before construction; ownership, control and native capacity remain separate conditions.',
        'All offer nodes require real recipient approval. Follow-up programmes with partner rewards require new approval too.',
        'Temporary programme duration runs from final acceptance; suspension does not pause the calendar. One-time assets and earned research/XP remain after suspension or expiry.',
        'Standing agreements have no expiry; both signatories may terminate. Government changes alone do not revoke a state treaty; exact-party domestic programmes deactivate separately.',
        'Pending offers expire after 90 days without acceptance; silence never counts as consent. A refusal permits reopening the same focus-origin mandate after 90 days through its existing diplomatic channel, without an opinion punishment.',
        'Persistent country-and-agreement-family receipts survive termination, renegotiation and switch of German variants. Setup transfer fees may be newly negotiated but buildings, research coupons and experience grants are never replayed by reopening. Exercise renewals are separately priced, explicitly limited programmes.',
        'Flat weekly treaty flows need an explicit integration into the actual MD income/expense consumers. Existing Cuba spirits do not prove such a ledger exists.',
        'Every offer has fixed, inspectable terms. Doctrine grants its own programme and does not silently change partner payments.',
        'All proposed country/building/research modifiers must be resolved to actual supported providers before implementation; unverified mappings are identified in the technical notes.'
    ],
    lifecycle=['Offer focus completed','Named recipient receives accept/refuse decision','Final eligibility and capacity rechecked','All parties consented: setup transaction once, paired spirits activate','Weekly signed costs and transfers while active','War/embargo/sanction/parent failure: both sides suspend','Conditions restored: restore without setup replay','Term expires or signatory terminates: both sides end'],
    rewiring=[
        dict(focus='USA_1970_E3',prerequisites=[['USA_1970_E1','USA_1970_E2']],reason='Ordinary agricultural development remains accessible after either funding model.'),
        dict(focus='USA_1970_E4',prerequisites=[['USA_1970_E1','USA_1970_E2']],reason='Office development is compatible with both industrial funding models.'),
        dict(focus='USA_1970_D3',prerequisites=[['USA_1970_D1','USA_1970_D2']],reason='Oversight is independent of recruitment model.'),
        dict(focus='USA_1970_D4',prerequisites=[['USA_1970_D1','USA_1970_D2']],reason='Executive intelligence is independent of recruitment model.'),
        dict(focus='USA_1970_D5',prerequisites=[['USA_1970_D1','USA_1970_D2']],reason='Army development cannot be locked behind an intelligence policy.'),
        dict(focus='USA_1970_D7',prerequisites=[['USA_1970_D1','USA_1970_D2']],reason='Technology investment cannot be locked behind an intelligence policy.'),
        dict(focus='USA_1970_F4',prerequisites=[['USA_1970_F1','USA_1970_F2','USA_1970_F3']],reason='Every US doctrine can maintain an Atlantic alliance.'),
        dict(focus='USA_1970_F5',prerequisites=[['USA_1970_F1','USA_1970_F2','USA_1970_F3']],reason='Beijing and Moscow channels are not mutually exclusive.'),
        dict(focus='USA_1970_F6',prerequisites=[['USA_1970_F1','USA_1970_F2','USA_1970_F3']],reason='Every doctrine retains Middle Eastern diplomacy.'),
        dict(focus='USA_1970_F7',remove_exclusion=True,reason='Replace region-wide exclusivity with individual commitment/mandate terms.'),
        dict(focus='USA_1970_F8',remove_exclusion=True,reason='Mediation and Arab trade can coexist; conflict applies to specific aid/truce commitments.'),
        dict(focus='USA_1970_F9',remove_exclusion=True,reason='Arab trade cannot be blocked by all Israeli relations.')
        ,dict(focus='COLDWAR_USA_bahrain_base_request',add_exclusion=['USA_X_bahrain'],reason='Territorial cession and sovereignty-preserving facilities are alternative agreement families.')
    ])
for item in nodes:
    if item.get('replaces'):
        item['prerequisites']=live[item['replaces']]['prerequisites']
    if 'offer' in item:
        item.setdefault('common_requirements', ['All signatories exist','Bilateral peace','No bilateral native embargo or any of the four Imperia sanction classes in either direction','Actual active parent agreement where required'])
proposal['counts'] = dict(current=229, original=776, reworked=sum(n['status']=='Rework' for n in nodes), new=sum(n['status']=='New' for n in nodes), offers=sum('offer' in n for n in nodes))
proposal['counts']['concept_total']=229+proposal['counts']['new']
(HERE / 'proposal.json').write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(proposal['counts']))
