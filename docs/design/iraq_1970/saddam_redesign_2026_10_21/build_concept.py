# IMPERIA CW — Cold War: Saddam domestic-policy concept; does not write loaded game files.
"""Build reviewable design data and a self-contained native MD concept preview."""
from pathlib import Path
from itertools import product
from collections import defaultdict
import base64, gzip, hashlib, io, json, sys
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
DEST = Path('C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f4e-9042-7b61-be51-9d85f9facd82/saddam-domestic-paths.html')
sys.path[:0] = [str(ROOT/'tools/iraq_1970'),str(ROOT/'tools/iraq_1970_concept')]
from audit_design import load_design
from render_installed import read_tree, icon, title, SPRITES, GAME
from native_font import GLYPHS, KERNINGS, ATLAS, width

PREFIX = 'COLDWAR_IRQ_'
SOURCES = {
 'government': {'title':'US Interests Section, Baghdad: The Iraqi Political Scene, 1973', 'url':'https://history.state.gov/historicaldocuments/frus1969-76v27/d208'},
 'accession': {'title':'US Embassy Baghdad: Saddam succeeds al-Bakr, July 1979', 'url':'https://history.state.gov/historicaldocuments/frus1977-80v18/d138'},
 'economy': {'title':'Library of Congress Country Study: Role of Government', 'url':'https://countrystudies.us/iraq/50.htm'},
 'industry': {'title':'Library of Congress Country Study: Industrialization', 'url':'https://countrystudies.us/iraq/56.htm'},
 'education': {'title':'World Bank: Iraq Education Project performance audit, 1980', 'url':'https://documents.worldbank.org/curated/en/757591468914065199/pdf/multi-page.pdf'},
 'army': {'title':"US Department of Defense: Saddam's Generals", 'url':'https://www.govinfo.gov/app/details/GOVPUB-D-PURL-gpo16068'}
}
LABELS = {
 'political_power_factor':('Political power gain','%',1),
 'command_power_gain_mult':('Command power gain','%',1),
 'foreign_influence_defense_modifier':('Foreign influence defence','%',1),
 'police_cost_multiplier_modifier':('Police expenditure','%',-1),
 'army_intel_factor':('Army intelligence','%',1),
 'planning_speed':('Planning speed','%',1),
 'production_factory_efficiency_gain_factor':('Production efficiency growth','%',1),
 'production_factory_max_efficiency_factor':('Production efficiency cap','pp',1),
 'education_cost_multiplier_modifier':('Education expenditure','%',-1),
 'offices_productivity':('Office productivity','%',1),
 'civilian_factories_productivity':('Civilian industry productivity','%',1),
 'industrial_capacity_factory':('Military factory output','%',1),
 'consumer_goods_factor':('Consumer goods factor','%',-1),
 'production_lack_of_resource_penalty_factor':('Resource shortage penalty','%',-1),
 'receiving_investment_cost_modifier':('Incoming investment cost','%',-1),
 'population_tax_income_multiplier_modifier':('Population tax income','%',1),
 'office_park_income_tax_modifier':('Office tax income','%',1),
 'production_factory_start_efficiency_factor':('Starting production efficiency','pp',1),
 'army_org_factor':('Army organisation','%',1),
 'army_defence_factor':('Army defence','%',1),
 'army_personnel_cost_multiplier_modifier':('Army personnel expenditure','%',-1),
 'supply_consumption_factor':('Supply consumption','%',-1),
 'equipment_upgrade_xp_cost':('Equipment design XP cost','%',-1),
 'army_morale_factor':('Division recovery rate','%',1),
 'training_time_army_factor':('Army training time','%',-1),
 'line_change_production_efficiency_factor':('Production efficiency retention','%',1),
 'social_cost_multiplier_modifier':('Social expenditure','%',-1),
 'health_cost_multiplier_modifier':('Health expenditure','%',-1),
 'corporate_tax_income_multiplier_modifier':('Corporate tax income','%',1),
 'stability_factor':('Stability','pp',1),
 'production_speed_buildings_factor':('Construction speed','%',1),
 'research_speed_factor':('Research speed','%',1),
 'bureaucracy_cost_multiplier_modifier':('Administration expenditure','%',-1)
}
nodes=[]
def nid(s):return PREFIX+s
def research(category,bonus,uses=1):return {'type':'research','category':category,'bonus':bonus,'uses':uses}
def building(kind,state,levels=1):return {'type':'building','building':kind,'state':state,'levels':levels}
def xp(value):return {'type':'army_experience','value':value}
def focus(key,name,xy,days,gdp,desc,mods=None,instant=None,parents=(),pair=None,side=None,icon_from=None,history='',sources=(),notes=()):
    nodes.append({'id':nid(key),'t':name,'xy':list(xy),'days':days,'gdp':gdp,'d':desc,'m':mods or {},'instant':instant or [],
                  'p':[[nid(s) for s in row] for row in parents],'e':[],'pair':pair,'side':side,'g':'saddam','icon_from':icon_from or key,
                  'historical_basis':history,'sources':list(sources),'notes':list(notes),'status':'Proposed; not installed'})

focus('saddam_presidency',"Saddam's Presidency",(28,0),21,0,
 "The transfer of the presidency brings the party, the armed forces and the ministries under Saddam Hussein's authority. The new president must decide whether to govern through his own secretariat or give experienced ministers room to deliver his programme.",
 {'command_power_gain_mult':.12,'political_power_factor':.08,'stability_factor':-.03},
 history='Saddam was al-Bakr\'s deputy in January 1970. He formally assumed the presidency on 16 July 1979; earlier accession is alternate history.',sources=['government','accession'],
 notes=['Requires the Baath government and Saddam Hussein actually serving as leader. This focus does not appoint him or bypass succession.'])

focus('saddam_personal_state','Presidential Rule',(26,1),35,0,
 'Orders issued through the presidential secretariat can cut across rival offices and uncertain chains of command. Direct control gives the president greater freedom of action, but maintaining such an apparatus requires a permanent security establishment.',
 {'political_power_factor':.15,'command_power_gain_mult':.15,'foreign_influence_defense_modifier':.12,'police_cost_multiplier_modifier':.05},
 parents=[['saddam_presidency']],pair='government',side='A',history='Personal concentration of authority was historical. The choice concerns delegation inside an authoritarian state.',sources=['government'])
focus('saddam_party_cabinet','Ministerial Authority',(30,1),35,0,
 'Engineers, economists and experienced administrators cannot run their departments through daily political intervention. Protected ministerial responsibilities can improve industrial performance, at the price of leaving the presidency less freedom to redirect every appointment.',
 {'production_factory_efficiency_gain_factor':.12,'production_factory_max_efficiency_factor':.05,'education_cost_multiplier_modifier':-.04,'political_power_factor':-.05},
 parents=[['saddam_presidency']],pair='government',side='B',history='Non-Baath specialists held important posts. Stronger protected ministerial discretion is a plausible alternative priority, not democratisation.',sources=['government'])
focus('saddam_security_bureau','Security Directorates',(26,2),35,1.5,
 'The directorates must report reliably to the presidency rather than compete for its attention. Central intelligence assessments and a clear channel to the armed forces can improve preparation, while a larger surveillance establishment places further demands on the budget.',
 {'army_intel_factor':.08,'planning_speed':.10,'police_cost_multiplier_modifier':.03},parents=[['saddam_personal_state']],pair='government',side='A',icon_from='saddam_iran_dossier',
 history='Competing presidential and party security organisations are documented in 1973. Coordination is a design interpretation; repression is not given a casualty reward.',sources=['government'])
focus('saddam_technocrats','Retain Specialists',(30,2),35,1.5,
 'Technical appointments should survive changes in political fashion. Experienced managers and engineers can carry industrial projects from specification to production, provided the government accepts the cost of a professional civilian establishment.',
 {'offices_productivity':.05},[research('CAT_industry',.50)],parents=[['saddam_party_cabinet']],pair='government',side='B',
 history='Contemporary reporting records technicians outside the party occupying important positions.',sources=['government'])
focus('saddam_planning','Presidential Planning',(28,3),35,1,
 'Oil revenues can finance a national investment programme, but scattered projects consume scarce contractors and imported machinery. The presidency will publish a common construction programme and make its ministries responsible for supplying it.',
 {'production_speed_buildings_factor':.05,'bureaucracy_cost_multiplier_modifier':.02},[research('CAT_construction',.35)],parents=[['saddam_security_bureau','saddam_technocrats']],icon_from='saddam_credit',
 history='The state directed investment and distributed oil revenues; the proposed council is a coordination priority, not a claim that planning began under Saddam.',sources=['economy'])

focus('saddam_industry','Public Corporations',(24,4),70,5,
 'Large public enterprises can bring machinery, steelworking and military orders into the same industrial programme. The next investment allocation will establish a civilian works in Baghdad and support state production, even where output must be sustained by protected domestic demand.',
 {'industrial_capacity_factory':.06,'consumer_goods_factor':.02},[building('industrial_complex',557)],parents=[['saddam_planning']],pair='industry',side='A',
 history='State industrial combines were central to Iraqi industrialisation. Exclusivity concerns one investment allocation, not abolition of private firms.',sources=['industry','economy'])
focus('saddam_contractors','Private Contractors',(26,4),70,5,
 'Iraqi merchants and contractors already supply the state. Commercial premises, reliable tenders and tax allowances can turn those connections into productive capacity. The government will give the next investment allocation to private suppliers, accepting lower household-tax receipts in exchange for a broader business base.',
 {'civilian_factories_productivity':.10,'offices_productivity':.10,'population_tax_income_multiplier_modifier':-.03},[building('offices',557)],parents=[['saddam_planning']],pair='industry',side='B',icon_from='industry_commercial_services',
 history='Private enterprises and public combines coexisted. Early private concessions are documented in 1973; broad asset sales belong especially to 1987.',sources=['government','economy'])
focus('saddam_integrated_works','Integrated Works',(24,5),35,1.5,
 'Separate state plants must agree on components, deliveries and production schedules. Common standards and purchasing arrangements will keep assembly lines running when imported materials become scarce, without creating another set of competing enterprises.',
 {'production_factory_efficiency_gain_factor':.10,'production_lack_of_resource_penalty_factor':-.10},parents=[['saddam_industry']],pair='industry',side='A',icon_from='industry_machine_tools',
 history='Iraq organised factories into sectoral state organisations. Coordination improves their existing capacity; it does not create oil or imported inputs.',sources=['industry'])
focus('saddam_merchant_credit','Merchant Credit',(26,5),35,1.5,
 'Commercial banks and contract guarantees can help local firms take on larger orders. Better access for genuine investment will reduce project costs, while a stronger assessment of office earnings brings part of the expanding commercial sector back into the treasury.',
 {'receiving_investment_cost_modifier':-.15,'office_park_income_tax_modifier':.10},parents=[['saddam_contractors']],pair='industry',side='B',icon_from='saddam_credit',
 history='A stronger commercial allocation is plausible alternate policy within Iraq\'s mixed economy.',sources=['economy'],notes=['Incoming-investment cost applies only to an actual investment. It grants no foreign cash and commits no other player.'])

focus('saddam_literate_generation','A Literate Generation',(30,4),49,2,
 'The literacy campaign must reach the adults who missed formal schooling. Evening instruction and provincial teaching teams can extend the work already begun in the 1970s. A more educated population strengthens research and urban employment, although agriculture loses part of its unskilled labour advantage.',
 {},[{'type':'literacy','value':.04}],parents=[['saddam_planning']],pair='education',side='A',icon_from='society_mass_literacy',
 history='Free education in 1974 and compulsory primary education in 1978 preceded Saddam\'s presidency. This is an additional allocation continuing those programmes, not their invention.',sources=['education'],
 notes=['Literacy is capped at 100%. Before the cap, +4 percentage points gives research +2pp, office productivity +2pp, education-expenditure contribution -4pp, productivity-growth contribution +0.08 and agricultural-productivity contribution -2pp through the current MD education system.'])
focus('saddam_engineers',"Republic's Engineers",(32,4),49,2,
 'New industrial machinery needs technicians who can operate and adapt it. The additional education allocation will support construction engineering and electronics, giving factories a more capable starting workforce while increasing the cost of specialist instruction.',
 {'production_factory_start_efficiency_factor':.05,'education_cost_multiplier_modifier':.05},[research('CAT_construction',.35),research('CAT_electronics',.35)],parents=[['saddam_planning']],pair='education',side='B',icon_from='society_technical_colleges',
 history='Technical and vocational education expanded alongside mass education. This choice directs extra funding rather than closing schools.',sources=['education'])
focus('saddam_provincial_schools','Provincial Schools',(30,5),49,3,
 'Schools outside Baghdad need roads, dependable supplies and teachers who can remain in their posts. A provincial building programme in Nineveh will connect classrooms to the wider economy and strengthen the institutions that sustain scientific education.',
 {'research_speed_factor':.03},[building('infrastructure',166)],parents=[['saddam_literate_generation']],pair='education',side='A',icon_from='society_teacher_deployment',
 history='A plausible provincial extension of the national education effort; the particular Nineveh allocation is a gameplay proposal.',sources=['education'])
focus('saddam_technical_institutes','Technical Institutes',(32,5),49,3,
 'Technical institutes should train the supervisors and production engineers who can turn imported designs into regular output. Equipment laboratories and industrial instruction will raise the ceiling of Iraqi production, with trained specialists remaining tied to an expensive education system.',
 {'production_factory_max_efficiency_factor':.04},[research('CAT_industry',.50)],parents=[['saddam_engineers']],pair='education',side='B',icon_from='society_technical_colleges',
 history='Technical training is historically grounded; its production-efficiency values are proposed balance.',sources=['education'])
focus('saddam_industrial_linkages','Industrial Linkages',(28,6),49,3,
 'Industrial investment and trained workers are useful only if goods can move between the northern plants and the markets around Baghdad. Road and utility improvements in Salahuddin will connect the programme to the existing industrial belt.',
 {},[building('infrastructure',167),research('CAT_construction',.50)],parents=[['saddam_integrated_works','saddam_merchant_credit'],['saddam_provincial_schools','saddam_technical_institutes']],icon_from='industry_power_grid',
 history='Salahuddin contains Baiji. The route joins one industrial and one education programme; both are genuinely required.',sources=['industry'])

focus('saddam_guard','Strategic Guard',(26,7),49,2,
 'The presidency can concentrate experienced soldiers, equipment and training in a strategic reserve. A better organised defence will be available when the front is under pressure, but such a formation requires a costly professional establishment.',
 {'army_org_factor':.03,'army_defence_factor':.04,'army_personnel_cost_multiplier_modifier':.06},[xp(25)],parents=[['saddam_industrial_linkages']],pair='army',side='A',
 history='The Republican Guard existed earlier but expanded as a combat force particularly after 1982. This is a strategic training and funding priority, not a massive Guard army already present in 1970.',sources=['army'],
 notes=['Organisation and defence affect the national army. The modifiers do not target only Guard templates. Both this route and the alternative retain regular units.'])
focus('saddam_regular_army','The Regular Army',(30,7),49,2,
 'A large army must be able to replace losses and restore exhausted formations without waiting for a privileged reserve. Standard training, dependable leave rotations and a wider professional cadre will improve recovery throughout the army, at a continuing personnel cost.',
 {'army_morale_factor':.08,'training_time_army_factor':-.10,'army_personnel_cost_multiplier_modifier':.04},[xp(25)],parents=[['saddam_industrial_linkages']],pair='army',side='B',
 history='The alternative concentrates scarce training and pay across the regular force. It is a plausible allocation choice, not the abolition of the Guard.',sources=['army'])
focus('saddam_guard_supply','Guard Supply',(26,8),35,1.5,
 'A strategic reserve cannot arrive short of transport, spare parts or ammunition. Standard supply arrangements and experienced equipment teams will reduce the burden of maintaining prepared forces and adapting their weapons.',
 {'supply_consumption_factor':-.05,'equipment_upgrade_xp_cost':-.08},parents=[['saddam_guard']],pair='army',side='A',
 history='Logistics and preparation support a reserve-based doctrine. Effects are army-wide, as required by the native modifiers.',sources=['army'])
focus('saddam_staff_college','Staff Colleges',(30,8),35,1.5,
 'Officers need practice coordinating divisions and restoring a damaged front. Staff colleges will draw lessons from field exercises and build a body of doctrine that can be applied across the regular army.',
 {},[xp(35),research('land_doctrine',.35)],parents=[['saddam_regular_army']],pair='army',side='B',
 history='Professional staff education is a plausible institutional emphasis. The doctrine reward must use the MD doctrine-cost form when implemented.',sources=['army'])
focus('saddam_war_industries','War Industries',(28,9),70,5,
 'The army remains dependent on imported machinery and weapons. A new military production line in Basrah, supported by domestic engineering and stable procurement, will increase the capacity to maintain an Iraqi war economy. Reserving industrial resources for it will tighten civilian supply.',
 {'line_change_production_efficiency_factor':.05,'consumer_goods_factor':.01},[building('arms_factory',171)],parents=[['saddam_guard_supply','saddam_staff_college']],icon_from='defence_armaments',
 history='Defence industry expanded under Saddam. The Basrah allocation is a design proposal, not a claim to reproduce a specific historical factory.',sources=['industry'])

focus('saddam_social_wage','The Social Wage',(26,10),49,2.5,
 'Cheap necessities and public services bind household welfare to the state. Protecting that social wage and coordinating medical purchasing will ease civilian demand and health expenditure, but subsidies and public provision must be paid from a larger social budget.',
 {'consumer_goods_factor':-.08,'health_cost_multiplier_modifier':-.05,'social_cost_multiplier_modifier':.06},parents=[['saddam_war_industries']],pair='households',side='A',icon_from='society_universal_services',
 history='Oil revenue funded subsidies and social provision. Exclusivity concerns the next household-and-employment settlement, not whether Iraq has welfare at all.',sources=['economy'])
focus('saddam_production_incentives','Production Incentives',(30,10),49,2.5,
 'Managers should reward delivered output rather than maintain every position regardless of performance. Performance pay and targeted tax allowances can raise civilian productivity and accelerate production, although the treasury must surrender part of its household-tax income.',
 {'civilian_factories_productivity':.08,'production_factory_efficiency_gain_factor':.08,'population_tax_income_multiplier_modifier':-.03},parents=[['saddam_war_industries']],pair='households',side='B',icon_from='industry_machine_tools',
 history='Productivity incentives and the removal of employment guarantees were especially prominent in 1987. Earlier adoption is plausible alternate policy, not a historical 1970 measure.',sources=['economy'])
focus('saddam_family_services','Family Services',(26,11),49,3,
 'Household support should include primary care and the roads needed to reach it. A service programme in Maysan will improve access while shared medical purchasing reduces the expense of the health system.',
 {'health_cost_multiplier_modifier':-.05},[building('infrastructure',1124)],parents=[['saddam_social_wage']],pair='households',side='A',icon_from='society_primary_care',
 history='A specific Maysan service-and-road allocation is proposed alternate development within the historical welfare model.',sources=['economy'])
focus('saddam_performance_contracts','Performance Contracts',(30,11),49,3,
 'State orders can be renewed against delivery targets and taxable earnings. More demanding contracts will improve the treasury\'s return from businesses, but workers and managers will resent a settlement that weakens the security of established posts.',
 {'corporate_tax_income_multiplier_modifier':.06,'office_park_income_tax_modifier':.08,'stability_factor':-.02},parents=[['saddam_production_incentives']],pair='households',side='B',icon_from='saddam_credit',
 history='The 1987 productivity and employment reforms provide the precedent. Additional instability represents the loss of job security.',sources=['economy'])
focus('saddam_national_market','A National Market',(28,12),49,3.5,
 'The presidency\'s programme must connect public orders, private trade and household purchasing power. A commercial centre in Basrah will link southern industry and services to the national market, while transport and contract standards support civilian production.',
 {'civilian_factories_productivity':.05},[building('offices',171)],parents=[['saddam_family_services','saddam_performance_contracts']],icon_from='industry_commercial_services',
 history='A concrete civilian-development conclusion, rather than a ceremonial legacy focus. Its location and reward are a balance proposal.',sources=['industry','economy'])

PAIRS=[
 {'id':'government','title':'Authority inside the presidency','question':'Personal command or protected ministerial discretion?','left':'saddam_personal_state','right':'saddam_party_cabinet','why':'A single presidential chain of command cannot simultaneously promise ministers protected discretion over the same appointments and orders.'},
 {'id':'industry','title':'The next industrial allocation','question':'Public combines or private suppliers?','left':'saddam_industry','right':'saddam_contractors','why':'One investment allocation goes to public corporations or private contractors. Both kinds of enterprise continue to exist.'},
 {'id':'education','title':'The additional education allocation','question':'Wider literacy or scarce technical specialists?','left':'saddam_literate_generation','right':'saddam_engineers','why':'The additional instructors, equipment and funding have one priority. Both routes retain basic schooling and existing technical education.'},
 {'id':'army','title':'Training and personnel priorities','question':'A strategic reserve or the regular force?','left':'saddam_guard','right':'saddam_regular_army','why':'Experienced trainers and professional pay are concentrated in a reserve or spread through the regular army. Neither route deletes the other formations.'},
 {'id':'households','title':'The household and employment settlement','question':'A protected social wage or output incentives?','left':'saddam_social_wage','right':'saddam_production_incentives','why':'The same settlement cannot prioritise unconditional job-and-subsidy protection and performance-linked employment guarantees.'}
]

def main():
    existing=load_design(); original=read_tree('common/national_focus/COLDWAR_IRQ_1970_focus.txt')
    by={n['id']:n for n in existing['nodes']}; proposed={n['id']:n for n in nodes}
    for n in nodes:
        n['i']=original[nid(n['icon_from'])]['icon']
        n['label_width']=width(n['t'])
        assert n['label_width']<=147,(n['t'],n['label_width'])
    for p in PAIRS:
        a,b=nid(p['left']),nid(p['right']);proposed[a]['e']=[b];proposed[b]['e']=[a]
    assert len(nodes)==25 and len(proposed)==25
    assert all(p in proposed for n in nodes for row in n['p'] for p in row)
    for n in nodes:
        assert all(proposed[p]['xy'][1]<n['xy'][1] for row in n['p'] for p in row)
        assert set(n['m'])<=set(LABELS)
    model={'feature':'IMPERIA CW — Cold War: Saddam domestic choices','phase':'Concept only; approval required before game implementation',
           'starting_identity':'Ahmed Hassan al-Bakr is president in January 1970. Saddam is his deputy.',
           'gate':'Baath government, party slot 21, and Saddam Hussein actually leading Iraq. No new party system or automatic accession.',
           'cost_contract':'One-time programme cost as a percentage of annual GDP; preserve existing guarded funding and project completion rules on implementation.',
           'lifecycle':'Programme modifiers active while Saddam and the Baath government rule; earned policies return on re-accession. Buildings, research grants, army XP and literacy are awarded once and never replayed.',
           'retention':'Iran/Kuwait, Gulf-credit and war-debt mechanics remain in their existing shared branches. Before implementation, preserve every old Saddam-specific dossier/finance access condition and migrate old receipts explicitly; this concept does not claim that migration is written.',
           'sources':SOURCES,'labels':LABELS,'pairs':PAIRS,'nodes':nodes,'original_saddam_ids':[n['id'] for n in existing['nodes'] if n['group']=='saddam' and not n.get('audit_retired')]}
    (HERE/'CONCEPT.json').write_text(json.dumps(model,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    routes=[]
    for bits in product('AB',repeat=5):
        choices=dict(zip((p['id'] for p in PAIRS),bits));taken=[n for n in nodes if not n['pair'] or choices[n['pair']]==n['side']]
        included={n['id'] for n in taken};totals=defaultdict(float)
        for n in taken:
            assert all(any(p in included for p in row) for row in n['p'])
            for k,v in n['m'].items():totals[k]+=v
        routes.append({'choices':choices,'focuses':len(taken),'focus_days':sum(n['days'] for n in taken),'gdp_percent_sum':round(sum(n['gdp'] for n in taken),2),
                       'modifiers':{k:round(v,5) for k,v in totals.items()},'one_time':[r for n in taken for r in n['instant']]})
    (HERE/'ROUTE_AUDIT.json').write_text(json.dumps({'scope':'All 32 compatible Saddam programme routes; GDP percentage sum is not a fixed treasury forecast. Other branch contributions are excluded here. Native literacy-derived changes are recorded separately in CONCEPT.json.',
                                                  'routes':routes},indent=2)+'\n',encoding='utf-8')
    # Unchanged neighbours stay sourced from the currently loaded tree, not a stale screenshot.
    all_nodes=[]
    for key,n in original.items():
        if by[key]['group']=='saddam':continue
        a=by[key]
        all_nodes.append({'id':key,'t':n['title'],'xy':n['xy'],'i':n['icon'],'g':a['group'],'p':n['prerequisites'],'e':n['excludes'],
                          'd':title(key+'_desc'),'m':a.get('modifiers',{}),'context':True})
    all_nodes+=nodes
    assert len(all_nodes)==len(original)-18+25
    for n in all_nodes:
        for row in n['p']:
            for p in row:assert p in {x['id'] for x in all_nodes},('Unmigrated external prerequisite',n['id'],p)
    payload={'nodes':all_nodes,'pairs':PAIRS,'sources':SOURCES,'labels':LABELS,'images':[],'icons':{},'groups':{g['id']:g['label'].replace('\ufffd','-') for g in existing['groups']},
             'gate':model['gate'],'lifecycle':model['lifecycle'],'retention':model['retention'],'source_hash':hashlib.sha256((ROOT/'common/national_focus/COLDWAR_IRQ_1970_focus.txt').read_bytes()).hexdigest()}
    def picture(im):
        stream=io.BytesIO();im.convert('RGBA').save(stream,format='WEBP',quality=88,method=6)
        return 'data:image/webp;base64,'+base64.b64encode(stream.getvalue()).decode()
    cache={}
    for name in sorted({n['i'] for n in all_nodes}):
        texture=SPRITES[name][0]
        if texture not in cache:cache[texture]=len(payload['images']);payload['images'].append(picture(icon(name)))
        payload['icons'][name]=cache[texture]
    payload['bar']=picture(Image.open(GAME/'gfx/interface/focusview/titlebar/focus_unavailable_bg.dds'))
    used={ord(c) for n in all_nodes for c in n['t']}|{63};native=Image.open(ATLAS).convert('RGBA');atlas=Image.new('RGBA',(512,512));glyphs={};x=y=h=0
    for cp in sorted(used):
        if cp not in GLYPHS:continue
        g=GLYPHS[cp];w,gh=g['width'],g['height']
        if x+w>512:x=0;y+=h+1;h=0
        atlas.alpha_composite(native.crop((g['x'],g['y'],g['x']+w,g['y']+gh)),(x,y))
        glyphs[cp]=[x,y,w,gh,g['xoffset'],g['yoffset'],g['xadvance']];x+=w+1;h=max(h,gh)
    payload['font']=picture(atlas.crop((0,0,512,y+h+1)));payload['glyphs']=glyphs
    payload['kern']={f'{a},{b}':v for (a,b),v in KERNINGS.items() if a in used and b in used}
    packed=base64.b64encode(gzip.compress(json.dumps(payload,separators=(',',':'),ensure_ascii=False).encode(),compresslevel=9,mtime=0)).decode()
    html=(HERE/'preview_fragment.html').read_text(encoding='utf-8').replace('<!-- CONCEPT_DATA -->',f'<script type="application/octet-stream" id="cw-saddam-data">{packed}</script>')
    assert len(html.encode())<1_000_000,len(html.encode())
    assert '<html' not in html.lower() and '<!doctype' not in html.lower()
    DEST.write_text(html,encoding='utf-8',newline='\n')
    print(json.dumps({'nodes':len(nodes),'exclusive_pairs':len(PAIRS),'routes':len(routes),'full_tree':len(all_nodes),'bytes':len(html.encode()),'destination':str(DEST)}))

if __name__=='__main__':main()
