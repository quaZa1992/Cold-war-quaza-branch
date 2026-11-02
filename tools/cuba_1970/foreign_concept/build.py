# IMPERIA COLD WAR — foreign policy approval concept only.
from pathlib import Path
import base64, copy, hashlib, io, json, re, sys
from collections import Counter

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = ROOT / 'docs/design/cuba_foreign_1970'
VIS = Path('C:/Users/Enes/.codex/visualizations/2026/10/23/01a16858-4604-7d63-8280-842aa85009b7')
sys.path.insert(0, str(ROOT/'tools/cuba_1970_concept'))
import native_font as font


def clean(x):
    if isinstance(x, str): return x.replace('\u2013', '-').replace('\u2014', ':').replace('\u2212', '-')
    if isinstance(x, list): return [clean(v) for v in x]
    if isinstance(x, dict): return {k: clean(v) for k,v in x.items()}
    return x


def uri(img):
    buf=io.BytesIO(); img.save(buf,format='PNG')
    return 'data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    oldfile=VIS/'cuba-1970-focus-concept.html'
    old=clean(json.loads(re.search(r'const DATA=(.*?);\nconst root=',oldfile.read_text(encoding='utf-8'),re.S).group(1)))
    approved=json.loads((ROOT/'tools/cuba_1970/approved_design.json').read_text(encoding='utf-8'))
    oldnodes={n['key']:n for n in old['nodes']}
    nodes=[copy.deepcopy(n) for n in old['nodes'] if n['group']!='foreign']
    by={n['key']:n for n in nodes}; merges=[]; replacement={}

    def merge(source,targets):
        donor=by[source]
        for key in targets:
            n=by[key]
            for mod,val in donor['modifiers'].items(): n['modifiers'][mod]=n['modifiers'].get(mod,0)+val
            n['effects']+=copy.deepcopy(donor['effects'])
            n['modrows']+=copy.deepcopy(donor.get('modrows',[]))
            n['effect_rows']+=copy.deepcopy(donor.get('effect_rows',[]))
            n['days']+=donor['days']; n['cost']+=donor['cost']
            n['consolidated_from']=n.get('consolidated_from',[])+[source]
        replacement[donor['id']]=[by[k]['id'] for k in targets]
        nodes.remove(donor)
        merges.append(dict(source=source,targets=targets,days=donor['days'],effects=donor['effects'],modifiers=donor['modifiers']))

    merge('rail_lorries',['finish_zafra','restore_sectors'])
    merge('mill_mechanisation',['sugar_exports'])
    merge('anap_cooperatives',['food_first'])
    merge('repair_grid',['moa_refinery'])
    merge('light_industry',['protected_enterprises','joint_ventures'])
    merge('oil_reserve',['havana_ports'])
    merge('militia_logistics',['territorial_defence'])
    # Overseas Forces and its school move to the new foreign section. They are
    # replaced rather than added a second time to the standing army bonuses.
    overseas=copy.deepcopy(by['expeditionary_forces']); school=copy.deepcopy(by['mission_schools'])
    replacement[overseas['id']]=['COLDWAR_CUB_foreign_expeditionary','COLDWAR_CUB_foreign_advisers']
    replacement[school['id']]=replacement[overseas['id']]
    nodes.remove(by['expeditionary_forces']); nodes.remove(by['mission_schools'])
    merges.append(dict(source='expeditionary_forces + mission_schools',targets=['foreign_expeditionary','foreign_advisers'],days=70,relocated=True))
    merge('social_promise',['rural_clinics','teaching_hospitals'])
    merge('science_schools',['medical_brigades','retain_doctors'])
    merge('tricontinental_secretariat',['diplomatic_solidarity','foreign_cadres'])

    for n in nodes:
        n['prerequisites']=[list(dict.fromkeys(x for pid in ps for x in replacement.get(pid,[pid]))) for ps in n['prerequisites']]
        n['prerequisites']=[ps for ps in n['prerequisites'] if n['id'] not in ps]
        n['mutually_exclusive']=[mid for mid in n['mutually_exclusive'] if mid not in replacement]
        if n['group'] not in ['economy','society','defence']: n['xy'][1]+=2
        if n['group']=='ospaaal': n['prerequisites']=[]
        n['is_existing']=True
        # The generic Cuban medical chooser is replaced by named foreign offers.
        if n['key']=='medical_brigades':
            n['effects']=[e for e in n['effects'] if e.get('kind')!='offer']
            n['effect_rows']=[s for s in n['effect_rows'] if 'medical_mission' not in s and 'mission offer' not in s.lower()]
        n['script']=''

    def add(key,title,xy,parents=(),excludes=(),icon='tradeagreementcuba',mods=None,desc='',partner=None,cub=None,other=None,costs=(0,0),spirit=None,requirements=(),history='',sources=(),days=35,instant=(),receipt=()):
        n=dict(id='COLDWAR_CUB_foreign_'+key,key='foreign_'+key,title=title,native_title=title,group='foreign',xy=list(xy),cost=days/7,days=days,
            prerequisites=[['COLDWAR_CUB_foreign_'+p for p in parents]] if parents else [],mutually_exclusive=['COLDWAR_CUB_foreign_'+p for p in excludes],icon=icon,
            description=desc,modifiers=mods or {},effects=[],effect_rows=list(instant),slot=None,extra_gate='',guards=[],is_existing=False,
            partner=partner,cub_modifiers=cub or {},partner_modifiers=other or {},setup_costs=list(costs),spirit=spirit,
            requirements=list(requirements),historical_status=history,sources=list(sources),receipt=list(receipt),lifetime='National policy' if not partner else 'Standing bilateral agreement',reference='Source-reviewed main MD native effects and recipient consent',modrows=[])
        nodes.append(n); return n

    SOV='https://history.state.gov/historicaldocuments/frus1977-80v06/d220'
    MEX='https://history.state.gov/historicaldocuments/frus1977-80v23/d131'
    SPAIN='https://boe.es/diario_boe/txt.php?id=BOE-A-1979-7815'
    RAIL='https://history.state.gov/historicaldocuments/frus1969-76ve11p1/d279'
    FISH='https://www.treaty-accord.gc.ca/text-texte.aspx?id=101418'
    DDR='https://germanhistorydocs.org/en/two-germanies-1961-1989/east-german-government-delegation-visits-cuba-1974'
    USA='https://history.state.gov/historicaldocuments/frus1977-80v23/d18'
    AFRICA='https://history.state.gov/historicaldocuments/frus1977-80v17p2/d16'
    JAM='https://mfaft.gov.jm/site/foreign-ministry-provides-update-on-cuban-medical-cooperation-programme/'
    ALG='https://mediccreview.org/wp-content/uploads/2015/08/mr_491.pdf'
    add('diplomacy','Island Diplomacy',(48,0),icon='cubanationalists',mods={'foreign_influence_modifier':.03,'bureaucracy_cost_multiplier_modifier':.02},desc="A small state needs a professional foreign service and more than one channel to the outside world. Havana can bargain with socialist partners, regional neighbours and Western governments without surrendering control of its own commitments.",instant=['Treasury: -$0.10 billion'],history='Historical setting. Institutional effects are proposed balance values.',days=21)
    add('soviet','Soviet Assistance',(36,1),['diplomacy'],icon='align_to_soviet_union',partner='SOV',cub={'imp_sanction_resistance':.10,'foreign_influence_defense_modifier':-.10},other={'foreign_influence_modifier':.04,'bureaucracy_cost_multiplier_modifier':.02},costs=(.10,.30),spirit='Technical Cooperation',desc='A negotiated technical mission can maintain Soviet equipment and train Cuban specialists. Moscow gains a durable planning relationship, while Cuba accepts dependence on external standards and spare parts.',history='Soviet technical assistance is historical. This standing package is a balance proposal.',sources=[SOV])
    add('cmea','Apply to COMECON',(34,2),['soviet'],icon='dealswithcommunistscuba',partner='SOV',costs=(.10,.10),spirit='COMECON Membership',desc='Cuba seeks admission to the Council for Mutual Economic Assistance. An accepted application creates the membership needed for the coordinated specialisation programme.',history='Cuba joined in 1972. Earlier admission is alternate history.',sources=[SOV],receipt=['Cuba: COMECON Membership','Soviet Union: Cuban Coordination Commission'])
    add('specialisation','Division of Labour',(34,3),['cmea'],icon='cubanewpoliticseco',partner='SOV',cub={'agriculture_district_income_tax_modifier':.08,'civilian_factories_productivity':-.04},other={'civilian_factories_productivity':.02,'bureaucracy_cost_multiplier_modifier':.01},costs=(.15,.10),spirit='Cuban Specialisation',requirements=['Cuba has actual COMECON membership'],desc='Members can coordinate demand, technical standards and specialised production. Cuba obtains an agricultural outlet while accepting less domestic industrial diversification.',history='Historical CMEA specialisation. Exact reciprocal modifiers are proposed.',sources=[SOV])
    add('sov_commodity','Commodity Credits',(38,2),['soviet'],['sov_industry'],icon='sugartobaccocuba',partner='SOV',cub={'agriculture_district_income_tax_modifier':.12,'resource_export_multiplier_modifier':.08,'foreign_influence_defense_modifier':-.08},other={'civilian_factories_productivity':.03,'foreign_influence_modifier':.04,'bureaucracy_cost_multiplier_modifier':.02},costs=(.15,.35),spirit='Commodity Protocol',desc='Prioritise a limited Soviet credit envelope around sugar and nickel deliveries. A longer planning horizon cushions market shocks but concentrates Cuba on one buyer and supplier.',history='Inspired by the 1976 to 1980 trade terms. The exclusive credit priority is a game policy choice.',sources=[SOV])
    add('sov_industry','Industrial Credits',(42,2),['soviet'],['sov_commodity'],icon='CUB_mining',partner='SOV',cub={'civilian_factories_productivity':.06,'production_speed_buildings_factor':.04,'education_cost_multiplier_modifier':.05},other={'research_speed_factor':.02,'resource_export_multiplier_modifier':.05,'education_cost_multiplier_modifier':.03},costs=(1.00,.25),spirit='Industrial Protocol',desc='Devote the available credit envelope to equipment and technical training. A defined Cuban industrial project expands production but creates continuing training and imported-parts obligations.',history='Soviet-assisted industry is historical. The exact funded plant is an alternate project.',sources=[SOV],receipt=['Oriente: +1 building slot','Oriente: +1 Civilian Industry'])
    add('mex_fuel','Mexican Fuel Contract',(46,2),['diplomacy'],['mex_agro'],icon='CUB_mining',partner='MEX',cub={'imp_sanction_resistance':.08,'civilian_factories_productivity':.04,'foreign_influence_defense_modifier':-.04},other={'resource_export_multiplier_modifier':.06,'foreign_influence_modifier':.03,'bureaucracy_cost_multiplier_modifier':.02},costs=(.15,.20),spirit='Fuel Logistics',desc='Use the bilateral project budget to purchase Mexican fuel services and coordinate shorter shipping routes. Mexico obtains orders and influence; Cuba diversifies access while becoming dependent on another delivery chain.',history='Inspired by the oil routing described in 1978. This proposal is bilateral and creates no Soviet obligation or free oil.',sources=[MEX])
    add('mex_agro','Agroindustrial Exchange',(50,2),['diplomacy'],['mex_fuel'],icon='cubaterreforms',partner='MEX',cub={'agricolture_productivity_modifier':.10,'research_speed_factor':.02,'education_cost_multiplier_modifier':.04},other={'agricolture_productivity_modifier':.04,'research_speed_factor':.02,'education_cost_multiplier_modifier':.03},costs=(.25,.15),spirit='Agricultural Commission',desc='Give processing equipment, applied agronomy and technician exchanges priority in the bilateral project budget. Both countries obtain useful expertise and take on the cost of maintaining a joint training programme.',history='Based on the 1975 and 1978 cooperation frameworks. Numerical terms are proposed.',sources=['https://treaties.un.org/doc/Publication/UNTS/Volume%201379/v1379.pdf'])
    add('spr_nickel','Nickel for Machinery',(54,2),['diplomacy'],['spr_training'],partner='SPR',cub={'resource_export_multiplier_modifier':.10,'civilian_factories_productivity':.05,'foreign_influence_defense_modifier':-.04},other={'production_speed_buildings_factor':.04,'resource_export_multiplier_modifier':.05,'bureaucracy_cost_multiplier_modifier':.03},costs=(.20,.20),spirit='Nickel and Machinery',desc='Commit the Spanish credit facility to machinery purchases secured against Cuban nickel deliveries. Spain gains a commodity outlet and equipment orders; Cuba obtains capital goods at the price of tighter delivery commitments.',history='Inspired by the commercial protocol of January 1979. Credit priorities are the game choice.',sources=[SPAIN])
    add('spr_training','Technical Scholarships',(58,2),['diplomacy'],['spr_nickel'],icon='free_higher_education',partner='SPR',cub={'production_speed_buildings_factor':.05,'research_speed_factor':.03,'education_cost_multiplier_modifier':.03},other={'research_speed_factor':.03,'civilian_factories_productivity':.03,'foreign_influence_defense_modifier':-.02},costs=(.30,.15),spirit='Technical Exchange',desc='Use the available Spanish cooperation facility for technical institutes, maintenance expertise and scholarships. The return is broader industrial knowledge rather than a larger immediate commodity commitment.',history='A plausible alternative within commercial and technical cooperation, not a claim that this exact package was signed.',sources=[SPAIN])
    add('can_rail','Canadian Rail Supply',(54,4),['diplomacy'],['can_fisheries'],icon='transporttr',partner='CAN',cub={'production_speed_buildings_factor':.08,'supply_consumption_factor':-.04,'foreign_influence_defense_modifier':-.04},other={'resource_export_multiplier_modifier':.06,'civilian_factories_productivity':.03,'bureaucracy_cost_multiplier_modifier':.02},costs=(.40,.10),spirit='Rail Supply',desc='Put the Canadian commercial facility into rolling stock, spares and maintenance. Canada gains orders and service work. Cuba gains transport efficiency but depends on external suppliers and export clearance.',history='A 1974 locomotive proposal was blocked by the United States. This contract is alternate history using suppliers or components lawfully available to both parties.',sources=[RAIL])
    add('can_fisheries','Atlantic Fisheries',(58,4),['diplomacy'],['can_rail'],icon='Cuban_Revolutionary_Navy_1',partner='CAN',cub={'resource_export_multiplier_modifier':.06,'supply_consumption_factor':-.03,'bureaucracy_cost_multiplier_modifier':.02},other={'resource_export_multiplier_modifier':.04,'research_speed_factor':.01,'bureaucracy_cost_multiplier_modifier':.02},costs=(.15,.10),spirit='Fisheries Cooperation',desc='Prioritise fishing access, conservation research and port services. Both governments obtain a more predictable commercial relationship and accept reporting, inspection and enforcement duties.',history='A bilateral fisheries agreement was concluded in 1977. Its priority over rail financing is a game policy choice.',sources=[FISH])
    add('ddr','Berlin and Havana',(38,4),['diplomacy'],icon='education_reform',partner='DDR',cub={'civilian_factories_productivity':.03,'education_cost_multiplier_modifier':.02},other={'resource_export_multiplier_modifier':.04,'education_cost_multiplier_modifier':.02},costs=(.10,.10),spirit='Industrial Training',desc='Machinery, tropical produce and technical placements give the relationship a practical basis. Each government must fund its own obligations and agree on the training arrangements.',history='Based on trade, technical cooperation and industrial training in the 1970s.',sources=[DDR])
    add('symbolic','A Name for Thälmann',(36,5),['ddr'],['cession'],icon='anti_fascism',partner='DDR',cub={'research_speed_factor':.02,'education_cost_multiplier_modifier':.03},other={'research_speed_factor':.02,'education_cost_multiplier_modifier':.03},costs=(.05,.05),spirit='Playa RDA Cooperation',requirements=['On or after 19 June 1972','Cuba owns and controls Cayo Blanco del Sur'],desc='Dedicate Cayo Blanco del Sur to Ernst Thälmann and propose a modest scientific and cultural programme. Cuban sovereignty continues. East German acceptance funds the exchange programme.',history='Historical symbolic dedication in 1972. The scientific modifiers are proposed.',sources=['https://www.swr.de/swrkultur/wissen/archivradio/fidel-castro-besucht-ddr-und-schenkt-ihr-eine-insel-100.html'],instant=['Cayo Blanco del Sur: rename to Ernst Thälmann Island'],days=70)
    add('cession','Cayo Blanco Agreement',(40,5),['ddr'],['symbolic'],icon='legislation',partner='DDR',cub={'foreign_influence_modifier':.04,'foreign_influence_defense_modifier':-.03},other={'foreign_influence_modifier':.04,'bureaucracy_cost_multiplier_modifier':.03},costs=(0,.40),spirit='Island Access Protocol',requirements=['On or after 19 June 1972','Cuba owns and controls Cayo Blanco del Sur'],desc='Propose a genuine territorial settlement with compensation and defined civilian access. The German Democratic Republic decides whether to accept responsibility. No military installation is included.',history='Explicit alternate history. The historical dedication transferred no sovereignty.',sources=[DDR],receipt=['Cuba: +$0.40 billion compensation','DDR: transfer State 1252','Cuba retains its core','No new DDR core, port or factory'],days=70)
    add('interests','Interests Sections',(46,4),['diplomacy'],icon='multypartycuba',partner='USA',cub={'foreign_influence_modifier':.03,'foreign_influence_defense_modifier':-.02},other={'foreign_influence_modifier':.03,'bureaucracy_cost_multiplier_modifier':.01},costs=(.05,.05),spirit='Interests Sections',desc='Permanent channels can handle prisoners, maritime incidents and migration without resolving every dispute. Both governments approve their own representation. The agreement can be signed while sanctions persist; its cooperation bonuses wait for mutual restrictions to end.',history='Interests Sections opened in September 1977. The no-sanctions activation rule is the requested game rule.',sources=[USA])
    add('limited','Trade before Claims',(44,5),['interests'],['settlement'],partner='USA',cub={'resource_export_multiplier_modifier':.06,'foreign_influence_defense_modifier':-.03},other={'resource_export_multiplier_modifier':.04,'foreign_influence_modifier':.02,'bureaucracy_cost_multiplier_modifier':.01},costs=(.15,.05),spirit='Limited Commercial Opening',desc='Seek a cheaper commercial opening while leaving the full property-claims settlement unresolved. Washington must approve the relaxation of its own economic restrictions. Outstanding diplomatic and military sanctions continue to suspend the cooperation spirits.',history='A plausible partial opening based on the 1970s negotiations. Not a historical end to the embargo.',sources=[USA],receipt=['USA and Cuba: lift mutual economic sanctions','Cuba: American Embargo becomes Limited Restrictions'])
    add('settlement','Claims Settlement',(48,5),['interests'],['limited'],icon='legislation',partner='USA',cub={'civilian_factories_productivity':.08,'research_speed_factor':.01,'foreign_influence_defense_modifier':-.08},other={'resource_export_multiplier_modifier':.08,'foreign_influence_modifier':.03,'political_power_factor':-.02},costs=(1.00,.10),spirit='Commercial Normalisation',desc='Commit substantial Cuban funds to compensation and ask Washington to settle the bilateral restrictions comprehensively. The United States obtains compensation and trade access, while assuming the domestic political cost of an agreement with Havana.',history='Explicit alternate-history settlement. It changes neither Cuban government nor Guantánamo sovereignty.',sources=[USA],receipt=['USA: +$0.60 billion compensation','Both countries: lift all four classes of mutual Imperia sanctions and native embargoes','Cuba: remove American Embargo and Limited Restrictions'])
    add('caribbean','Caribbean Cooperation',(54,5),['diplomacy'],icon='cubinvitejamaica',partner='JAM',cub={'foreign_influence_modifier':.04,'research_speed_factor':.01,'health_cost_multiplier_modifier':.03},other={'health_cost_multiplier_modifier':-.04,'research_speed_factor':.01,'education_cost_multiplier_modifier':.02},costs=(.10,.05),spirit='Caribbean Health Exchange',requirements=['Cuba has the Medical Brigades policy'],desc='Make regional diplomacy practical through a Jamaican health and training agreement. Jamaica receives services and skills; Cuba gains professional exchange and a dependable regional relationship while paying for overseas support.',history='Cuban-Jamaican medical cooperation began in 1976. Earlier agreement is plausible alternate history.',sources=[JAM])
    add('overseas','Overseas Service',(56,6),['diplomacy'],icon='cubaprof',mods={'send_volunteer_divisions_required':-.25,'send_volunteers_tension':-.05,'army_personnel_cost_multiplier_modifier':.04},desc='Prepare the legal authority, transport arrangements and support staff for overseas service. A smaller mobilisation can become eligible for deployment, but trained formations and the recipient government are still required.',history='Inspired by overseas commitments during the 1970s. The exact thresholds are balance proposals.',instant=['Treasury: -$0.20 billion','Volunteer deployment permitted'],sources=[AFRICA])
    add('advisers','Advisory Missions',(54,7),['overseas'],['expeditionary'],icon='army_planning',mods={'send_volunteer_size':1,'army_org_factor':.03,'army_personnel_cost_multiplier_modifier':.05},desc='Concentrate resources on instructors, staff work and limited formations. The programme develops deployable expertise with a smaller standing commitment than a large expeditionary force.',history='Historical advisory practice. This posture is the lower-cost alternative.',sources=[AFRICA],instant=['Treasury: -$0.15 billion','Land doctrine cost: -50% for 1 doctrine'],days=70)
    add('expeditionary','Expeditionary Brigades',(58,7),['overseas'],['advisers'],icon='cubacooparmyn',mods={'send_volunteer_size':2,'army_org_factor':.06,'special_forces_cap':.03,'army_personnel_cost_multiplier_modifier':.12,'supply_consumption_factor':.05,'army_fuel_consumption_factor':.05},desc='Maintain larger deployable contingents and the schools needed for distant operations. More formations can be sent abroad, with a higher military wage bill, fuel use and supply burden.',history='Replaces the old Overseas Forces and Mission Schools package. It is not an additional copy.',sources=[AFRICA],instant=['Treasury: -$0.35 billion','Land doctrine cost: -50% for 1 doctrine'],days=70)
    add('angola','Angolan Cooperation',(54,9),['advisers','expeditionary'],icon='cubacooparmyn',partner='ANG',cub={'foreign_influence_modifier':.04,'army_personnel_cost_multiplier_modifier':.03},other={'army_org_factor':.05,'foreign_influence_defense_modifier':-.04},costs=(.15,.10),spirit='Angolan Training Mission',requirements=['Independent Angola exists','Angolan government requests or accepts the mission'],desc='Offer an independent Angolan government a defined training and logistics mission. Angola gains military expertise; Cuba gains a continuing institutional relationship. Combat deployments remain a separate request and acceptance.',history='Inspired by Cuban assistance from 1975. No Angolan state, civil war or Cuban units are created by the focus.',sources=[AFRICA],instant=['Cuba: +15 Army Experience after mission acceptance'])
    add('ethiopia','Ethiopian Cooperation',(58,9),['advisers','expeditionary'],icon='cubadrills',partner='ETH',cub={'foreign_influence_modifier':.04,'army_fuel_consumption_factor':.03},other={'army_defence_factor':.05,'supply_consumption_factor':-.03,'foreign_influence_defense_modifier':-.05},costs=(.20,.10),spirit='Ethiopian Advisory Mission',requirements=['A compatible Ethiopian government accepts the agreement'],desc='Offer staff training, communications and logistical assistance with a clearly agreed mandate. Ethiopia obtains defensive expertise; Cuba takes on the operating cost and risk of a distant military relationship.',history='Inspired by the 1977 to 1978 intervention. The historical Derg and conflict are not forced into existence in 1970.',sources=[AFRICA],instant=['Cuba: +15 Army Experience after mission acceptance'])
    add('algeria','Algerian Medical Accord',(62,5),['diplomacy'],icon='generic_healthcare',partner='ALG',cub={'foreign_influence_modifier':.04,'education_cost_multiplier_modifier':.03},other={'health_cost_multiplier_modifier':-.05,'education_cost_multiplier_modifier':.02},costs=(.10,.10),spirit='Medical Training Exchange',requirements=['Cuba has the Medical Brigades policy'],desc='Extend a medical relationship that began in the early revolutionary years. Algeria gains clinical coverage and training; Cuba gains clinical exchange and diplomatic reach while supporting the education of replacement staff.',history='Cuban medical cooperation with Algeria began in 1963. These continuing reciprocal terms are proposed.',sources=[ALG])

    # Reserve two rows above the political programmes for the larger new section.
    # All surviving political programmes retain their relative positions.
    keys={n['key']:n for n in nodes}
    for key in ['protected_enterprises','joint_ventures']:
        keys[key]['prerequisites']=[['COLDWAR_CUB_moa_refinery']]
    keys['territorial_defence']['mutually_exclusive']=['COLDWAR_CUB_foreign_expeditionary']
    keys['foreign_expeditionary']['mutually_exclusive'].append('COLDWAR_CUB_territorial_defence')
    keys['air_defence']['prerequisites']=[['COLDWAR_CUB_far_reorganisation']]
    keys['foreign_angola']['partner']='AGL'
    keys['foreign_caribbean']['icon']='generic_healthcare'
    keys['foreign_sov_industry']['receipt']=['Camagüey: +1 building slot','Camagüey: +1 Civilian Industry']
    keys['foreign_sov_industry']['accepted_effects']=[dict(kind='building',state=855,building='industrial_complex',levels=1,extra_slots=1)]
    keys['foreign_specialisation']['receipt']=['Cuba: +25% Industry research bonus, 1 use']
    keys['foreign_specialisation']['accepted_effects']=[dict(kind='research',country='CUB',category='CAT_industry',bonus=.25,uses=1)]
    keys['foreign_cmea']['partner_modifiers']={'foreign_influence_modifier':.02,'bureaucracy_cost_multiplier_modifier':.01}
    keys['foreign_cmea']['partner_spirit']='Cuban Coordination Commission'
    keys['foreign_cmea']['requirements']=['Soviet Union approves Cuban admission']
    keys['foreign_cmea']['description']+=' Membership is the prerequisite for the following specialisation agreement.'
    keys['foreign_cession']['receipt']=['Cuba: +$0.40 billion compensation','DDR: transfer State 1252']
    keys['foreign_cession']['accepted_effects']=[dict(kind='treasury',country='CUB',amount=.4),dict(kind='transfer_state',state=1252,to='DDR',preserve_core='CUB')]
    keys['foreign_settlement']['accepted_effects']=[dict(kind='treasury',country='USA',amount=.6),dict(kind='lift_mutual_sanctions',countries=['CUB','USA'],classes=['diplomatic','financial','economic','military'],native_embargo=True)]
    keys['foreign_limited']['accepted_effects']=[dict(kind='lift_mutual_sanctions',countries=['CUB','USA'],classes=['economic'],native_embargo=True)]
    keys['foreign_symbolic']['immediate_effects']=[dict(kind='rename_state',state=1252,name='Ernst Thälmann Island')]
    for key in ['foreign_angola','foreign_ethiopia']:
        keys[key]['effect_rows']=[]
        keys[key]['receipt']=['Cuba: +15 Army Experience']
        keys[key]['accepted_effects']=[dict(kind='experience',country='CUB',army=15)]
    keys['foreign_overseas']['effect_rows']=['Treasury: -$0.20 billion']
    keys['foreign_overseas']['new_provider_requirements']=['Wire send_volunteer_divisions_required and send_volunteers_tension into a Cuban native modifier provider. Existing CUB sources currently read only volunteer size.']
    # The cross-domain exclusion denotes the original home-defence versus
    # overseas-formation budget. Advisers remain compatible with home defence.
    for n in nodes:
        n['title_width']=font.width(n['native_title'])
        n['title_art']=uri(font.raster(n['native_title']))
    groups=copy.deepcopy(old['groups'])
    for g in groups:
        g['nodes']=[n['id'] for n in nodes if n['group']==g['id']]
        if g['id']=='foreign':g['root']=[48,0];g['label']='Foreign Policy'
        elif g['id'] not in ['economy','society','defence']:g['root'][1]+=2
        first=next(n for n in nodes if n['id']==g['nodes'][0])
        g['root']=list(first['xy'])
        for nid in g['nodes']:
            n=next(n for n in nodes if n['id']==nid)
            n['anchor']=None if n is first else first['id']
            n['local_xy']=[n['xy'][0]-first['xy'][0],n['xy'][1]-first['xy'][1]]
    old.update(nodes=nodes,groups=groups,version='Foreign policy concept',merges=merges,
        foreign_views=[{'id':'foreign','label':'Außenpolitik gesamt','keys':[n['key'] for n in nodes if n['group']=='foreign']},
        {'id':'trade','label':'Handel und Kredite','keys':['foreign_'+k for k in ['soviet','cmea','specialisation','sov_commodity','sov_industry','mex_fuel','mex_agro','spr_nickel','spr_training','can_rail','can_fisheries']]},
        {'id':'atlantic','label':'DDR und USA','keys':['foreign_'+k for k in ['ddr','symbolic','cession','interests','limited','settlement']]},
        {'id':'missions','label':'Freiwillige und Medizin','keys':['foreign_'+k for k in ['overseas','advisers','expeditionary','angola','ethiopia','caribbean','algeria']]}],
        protocol=['Kuba wählt das konkrete Angebot durch einen Fokus. Nur das Partnerland erhält die Annahmeentscheidung.',
        'Beide Länder erhalten ihre eigenen dauerhaften Spirits nach ausdrücklicher Zustimmung. Abschlusskosten fallen einmalig an.',
        'Krieg zwischen den Partnern, ein natives Embargo oder eine diplomatische, finanzielle, wirtschaftliche oder militärische Sanktion eines Partners gegen den anderen pausiert beide Vertrags-Spirits.',
        'Nach Aufhebung werden beide Spirits beim nächsten täglichen Abgleich wieder aktiv. Sanktionen eines dritten Landes beenden dieses bilaterale Abkommen nicht.',
        'Ablehnung kostet nichts. Der Partner kann das bestehende kubanische Angebot später in seiner eigenen Diplomatie wieder aufrufen. Ein abgeschlossener Fokus wird dabei nicht erneut ausgeführt.',
        'Die kubanische Auswahl bleibt im Fokusbaum. Für Kuba gibt es kein zusätzliches Menü zur Auswahl der Vertragsvariante.',
        'Die Kreditgabeln wählen den Schwerpunkt eines begrenzten Finanzierungsrahmens. Sie behaupten keine historische Unvereinbarkeit normalen Handels.',
        'Freiwilligenboni gelten landesweit. Die normale Entsendung, vorhandene Divisionen und die Zustimmung des Empfängers bleiben erforderlich. Kuba startet in diesem Szenario ohne aufgestellte Einheiten.',
        'COMECON-Aufnahme und das echte Mitgliedsprogramm bleiben zwei Foki. Die historische Inselwidmung ist von einer tatsächlichen Gebietsabtretung getrennt.',
        '25 außenpolitische Foki. Gesamtvorschlag 120 durch zwölf freiwerdende Fokusplätze aus den ausgewiesenen Zusammenlegungen und Verlagerungen. Fidels 13 Foki bleiben vollständig erhalten.',
        'Soviet Air Defence wird ein gemeinsamer Militärfokus nach Reorganise the FAR. Die territoriale Verteidigung bleibt mit den großen Expeditionsbrigaden unvereinbar, ist aber mit begrenzten Beratermissionen kombinierbar.'],
        project='IMPERIA COLD WAR',native_approximation='Actual MD focus art and native bitmap titles. Engine connector routing and focus states are approximations. Concept only, not installed.',
        source_snapshot_sha256=hashlib.sha256((ROOT/'tools/cuba_1970/approved_design.json').read_bytes()).hexdigest())
    data=clean(old)
    for k in ['contracts','chronology','setup','lifecycles','rules','starting_spirits','baseline']:
        data.pop(k,None)
    used_art={n['icon'] for n in data['nodes']}
    data['art']={k:v for k,v in data['art'].items() if k in used_art}
    nodeids={n['id'] for n in data['nodes']}
    assert len(data['nodes'])==120
    assert sum(n['group']=='foreign' for n in data['nodes'])==25
    assert len(nodeids)==120
    for n in data['nodes']:
        assert all(p in nodeids for ps in n['prerequisites'] for p in ps),(n['key'],'parent')
        assert all(p in nodeids for p in n['mutually_exclusive']),(n['key'],'mutex')
        assert n['title_width']<=143,(n['title'],n['title_width'])
    (OUT/'FOREIGN_POLICY_CONCEPT.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    browser=copy.deepcopy(data)
    for n in browser['nodes']:
        for k in ['effects','reference','local_xy','anchor','title_width','script','guards','accepted_effects','immediate_effects','new_provider_requirements']:
            n.pop(k,None)
    payload=json.dumps(browser,ensure_ascii=False,separators=(',',':'))
    fragment=(HERE/'fragment.html').read_text(encoding='utf-8').replace('__DATA__',payload)
    assert '\u2013' not in fragment and '\u2014' not in fragment
    assert len(fragment.encode('utf-8'))<1_000_000
    (VIS/'cuba-foreign-policy-concept.html').write_text(fragment,encoding='utf-8')
    (OUT/'PREVIEW.html').write_text('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0">'+fragment+'</body></html>',encoding='utf-8')
    validation=dict(project='IMPERIA COLD WAR',focuses=120,foreign=25,counts=Counter(n['group'] for n in data['nodes']),merge_records=len(merges),freed_focus_slots=12,source_snapshot_sha256=data['source_snapshot_sha256'],runtime_changed=False)
    (OUT/'VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(validation))


if __name__=='__main__': main()
