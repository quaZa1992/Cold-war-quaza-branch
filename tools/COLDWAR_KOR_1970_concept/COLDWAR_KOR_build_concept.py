# IMPERIA CW — Cold War: South Korea 1970 concept data; never installs game content.
"""Author the approval-stage design, resolved layout and native-art preview data.

All outputs stay in docs/design/COLDWAR_KOR_1970. No loaded mod directory is
written. Policy values REPLACE a named slot; they are not cumulative upgrades.
"""
from pathlib import Path
import base64, csv, hashlib, io, json, re
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/design/COLDWAR_KOR_1970'
OUT.mkdir(parents=True, exist_ok=True)
PREFIX = 'COLDWAR_KOR_'
NODES, GROUPS = [], []

# Short keys below are authoring aliases, never invented runtime modifier keys.
KEYS = {
 'ic':'industrial_capacity_factory', 'build':'production_speed_buildings_factor',
 'civ':'production_speed_industrial_complex_factor', 'arms':'production_speed_arms_factory_factor',
 'dock':'industrial_capacity_dockyard', 'eff':'production_factory_max_efficiency_factor',
 'research':'research_speed_factor', 'pp':'political_power_factor', 'stab':'stability_factor',
 'cg':'consumer_goods_factor', 'interest':'interest_rate_multiplier_modifier',
 'bureau':'bureaucracy_cost_multiplier_modifier', 'police':'police_cost_multiplier_modifier',
 'education':'education_cost_multiplier_modifier', 'health':'health_cost_multiplier_modifier',
 'social':'social_cost_multiplier_modifier', 'personnel':'personnel_cost_multiplier_modifier',
 'equipment':'equipment_cost_multiplier_modifier', 'trade':'trade_opinion_factor',
 'foreign_def':'foreign_influence_defense_modifier', 'attack':'army_attack_factor',
 'defence':'army_defence_factor', 'core_def':'army_core_defence_factor', 'org':'army_org_factor',
 'morale':'army_morale_factor', 'training':'training_time_army_factor',
 'supply':'supply_consumption_factor', 'manpower':'conscription_factor',
 'intel':'intel_network_gain_factor', 'encryption':'encryption_factor',
 'workers':'buildings_worker_requirement_modifier', 'growth':'productivity_growth_modifier',
 'literacy':'literacy_rate_education_modifier', 'agri':'agricolture_productivity_modifier',
 'naval_org':'navy_org_factor', 'air_eff':'air_mission_efficiency',
}
LABELS = {
 'ic':'Factory output', 'build':'Construction speed', 'civ':'Civilian factory construction',
 'arms':'Military factory construction', 'dock':'Dockyard output', 'eff':'Production efficiency cap',
 'research':'Research speed', 'pp':'Political power gain', 'stab':'Stability',
 'cg':'Consumer goods factor', 'interest':'Interest rate (points before native clamps)',
 'bureau':'Weekly bureaucracy expenses', 'police':'Weekly police expenses',
 'education':'Weekly education expenses', 'health':'Weekly health expenses',
 'social':'Weekly social expenses', 'personnel':'Weekly personnel expenses',
 'equipment':'Weekly military equipment expenses', 'trade':'Trade opinion factor',
 'foreign_def':'Foreign influence defence', 'attack':'Division attack', 'defence':'Division defence',
 'core_def':'Division defence on core territory', 'org':'Division organization',
 'morale':'Division recovery rate', 'training':'Army training time', 'supply':'Supply consumption',
 'manpower':'Recruitable population factor', 'intel':'Intelligence network gain',
 'encryption':'Encryption', 'workers':'Building workforce requirement',
 'growth':'Productivity growth modifier', 'literacy':'Education literacy growth modifier',
 'agri':'Agricultural productivity', 'naval_org':'Naval organization', 'air_eff':'Air mission efficiency',
}

def effects(text):
    """Typed proposal effects. Helper/contract names are explicitly NEW design IDs."""
    e={'policies':[], 'cost':0, 'weekly':0, 'buildings':[], 'one_time':{}, 'actions':[]}
    for part in filter(None, text.split(';')):
        kind, _, value = part.partition(':')
        if kind=='p':
            slot, _, raw = value.partition(':')
            values={}
            for item in raw.split(','):
                k,v=item.split('='); values[KEYS[k]]=float(v)
            e['policies'].append({'slot':slot,'modifiers':values})
        elif kind in ('cost','weekly'): e[kind]=float(value)
        elif kind=='b':
            state,building,level=value.split(',')
            e['buildings'].append({'state':int(state),'type':building,'level':int(level)})
        elif kind in ('xp','pp_once','stability','war_support'):
            e['one_time'][kind]=float(value)
        elif kind in ('action','offer','remove','start_replace','condition','duration','leader','note'):
            e['actions'].append({'type':kind,'value':value})
        else: raise ValueError(part)
    return e

def node(g,key,title,xy,fx,desc,pre=None,gate=None,icon=None,days=35,owner=None):
    n={'id':PREFIX+key,'key':key,'group':g['id'],'label':title,'description':desc,
       'xy':list(xy),'days':days,'cost':days/7,'prerequisites':pre or [],
       'mutually_exclusive':[],'gate':gate or g['gate'],'ownership':owner or g['ownership'],
       'effects':effects(fx),'icon_family':icon or g['icon'],'history':g['history'],
       'reference':'KOR fork/join + Russia policy bundles; see md_reference_layout.md'}
    NODES.append(n); return n

def group(key,label,anchor,party=None,gate=None,icon='state',history='research_history.md',ownership=None):
    g={'id':key,'label':label,'anchor':list(anchor),'party':party,'icon':icon,'history':history,
       'gate':gate or (f'check_variable = {{ ruling_party = {party} }}' if party is not None else 'Independent KOR; 1970 scenario'),
       'ownership':ownership or ('party' if party is not None else 'national'), 'root':None}
    GROUPS.append(g); return g

def root(g,key,title,fx,desc,**kw):
    n=node(g,key,title,g['anchor'],fx,desc,**kw);g['root']=n['id'];return n

def stage(g,previous,index,left,right,join):
    """Native paired fork, parallel continuation and OR join, not an AND deadlock."""
    x,y=g['anchor']; y+=1+(index-1)*3
    a=node(g,*left[0:2],(x-2,y),*left[2:4],pre=[[previous['id']]])
    b=node(g,*right[0:2],(x+2,y),*right[2:4],pre=[[previous['id']]])
    a['mutually_exclusive']=[b['id']];b['mutually_exclusive']=[a['id']]
    aa=node(g,*left[4:6],(x-2,y+1),*left[6:8],pre=[[a['id']]])
    bb=node(g,*right[4:6],(x+2,y+1),*right[6:8],pre=[[b['id']]])
    return node(g,*join[0:2],(x,y+2),*join[2:4],pre=[[aa['id'],bb['id']]])

def pair_end(g,prev,y,left,right):
    x,ay=g['anchor']
    a=node(g,*left[:2],(x-2,ay+y),*left[2:4],pre=[[prev['id']]])
    b=node(g,*right[:2],(x+2,ay+y),*right[2:4],pre=[[prev['id']]])
    a['mutually_exclusive']=[b['id']];b['mutually_exclusive']=[a['id']]
    return a,b

g=group('drp','DRP · Park and the developmental state',(6,0),0,icon='park')
p=root(g,'developmental_state','The Developmental State','p:mandate:build=0.04,stab=-0.03;pp_once:50',
 'Park directs the ministries through the Economic Planning Board. Rapid execution rests on a contested presidential mandate.',days=14)
p=stage(g,p,1,
 ('yushin','The Yushin Constitution','p:constitution:pp=0.18,stab=-0.08,trade=-0.05;action:yushin_institutions',
  'Concentrate executive authority and replace direct presidential competition with controlled institutions.',
  'emergency_decrees','Emergency Decrees','p:constitution:pp=0.23,stab=-0.1,police=0.08,trade=-0.05',
  'Emergency powers accelerate decisions while surveillance and repression widen the legitimacy crisis.'),
 ('constitutional_drp','Constitutional Conservatism','p:constitution:stab=0.05,pp=-0.08;action:competitive_election_guarantees',
  'Retain conservative development policy under a competitive constitutional settlement.',
  'assembly_bargain','Bargain with the Assembly','p:constitution:stab=0.08,pp=-0.1,bureau=0.04',
  'Accept legislative bargaining and scrutiny in return for a more durable civilian mandate.'),
 ('presidential_administration','A Professional Cabinet','p:cabinet:build=0.04,bureau=0.04;cost:1',
  'A professional cabinet gives either constitutional settlement an administrative foundation.'))
p=stage(g,p,2,
 ('chaebol_compact','The Chaebol Compact','p:credit:ic=0.06,interest=0.35;weekly:0.003',
  'Channel policy credit through major business groups; concentrated guarantees deepen financial exposure.',
  'export_targets','Enforce Export Targets','p:credit:ic=0.09,eff=0.03,interest=0.45,stab=-0.03;weekly:0.004',
  'Reward firms that meet overseas sales targets, at the cost of leverage and workplace pressure.'),
 ('competitive_credit','Competitive Development Credit','p:credit:civ=0.08,ic=-0.02,interest=-0.2;cost:1',
  'Distribute development finance to smaller exporters, sacrificing conglomerate economies of scale.',
  'subcontractor_guarantees','Protect Subcontractors','p:credit:civ=0.1,ic=-0.02,interest=-0.2,bureau=0.04',
  'Enforce contracts and protect provincial suppliers from dominant buyers.'),
 ('planning_board','Strengthen the EPB','p:planning:build=0.03,bureau=0.03;cost:1',
  'Strengthen the existing Economic Planning Board rather than create a parallel economic authority.'))
p=stage(g,p,3,
 ('mobilized_villages','Mobilize the Villages','p:rural:agri=0.08,pp=0.04,stab=-0.02;weekly:0.002',
  'Use state-led village mobilization to deliver rural development and extend presidential influence.',
  'performance_grants','Competitive Village Grants','p:rural:agri=0.12,pp=0.04,stab=-0.03;weekly:0.003',
  'Reward successful villages, accepting uneven access and political dependence.'),
 ('rural_cooperatives','Autonomous Rural Cooperatives','p:rural:agri=0.07,stab=0.03,pp=-0.04;weekly:0.002',
  'Give cooperatives control over rural credit and priorities, limiting central mobilization.',
  'village_accounts','Elected Village Accounts','p:rural:agri=0.09,stab=0.05,pp=-0.05,bureau=0.03;weekly:0.002',
  'Local audits improve trust while slowing central allocation.'),
 ('balanced_provinces','Connect the Provinces','cost:2;b:606,infrastructure,1;b:607,infrastructure,1',
  'Extend transport links beyond the dominant southeastern corridor.'))
pair_end(g,p,10,
 ('dynastic_presidency','Presidential Continuity','p:succession:pp=0.12,stab=-0.05;condition:Yushin settlement;action:managed_succession',
  'Entrench continuity through a managed civilian succession; no hereditary transfer or automatic incumbent replacement.'),
 ('civilian_handover','A Civilian Handover','p:succession:stab=0.06,pp=-0.08;action:open_succession',
  'Prepare a constitutional transfer, trading presidential discretion for legitimacy.'))

g=group('ndp','NDP · constitutional opposition',(20,0),1,icon='parliament')
p=root(g,'parliamentary_government','Restore Parliamentary Government','p:mandate:stab=0.04,pp=-0.05;action:restore_civil_liberties',
 'A governing New Democratic Party restores parliamentary opposition rights and independent political association.',days=14)
p=stage(g,p,1,
 ('parliamentary_republic','A Parliamentary Republic','p:constitution:stab=0.07,pp=-0.1;action:parliamentary_republic',
  'Build a cabinet responsible to the Assembly; coalition bargaining constrains executive speed.',
  'coalition_committees','Coalition Committees','p:constitution:stab=0.09,pp=-0.12,bureau=0.03',
  'Make committee oversight permanent despite the administrative cost.'),
 ('checked_presidency','A Checked Presidency','p:constitution:pp=0.06,stab=0.02;action:presidential_term_limits',
  'Keep an effective presidency subject to term limits and parliamentary scrutiny.',
  'constitutional_court','An Independent Court','p:constitution:pp=0.04,stab=0.06,bureau=0.04;cost:1',
  'Judicial review strengthens rights while imposing an additional administrative burden.'),
 ('civil_service_review','Review the Civil Service','p:service:bureau=-0.04,pp=-0.03;cost:1',
  'Replace political appointments with accountable professional administration.'))
p=stage(g,p,2,
 ('market_conservatives','A Competitive Market','p:enterprise:interest=-0.35,civ=0.06,ic=-0.02',
  'Open credit allocation and restrain preferential guarantees, accepting slower conglomerate expansion.',
  'open_tenders','Open Public Tenders','p:enterprise:interest=-0.4,civ=0.09,ic=-0.02,bureau=0.03',
  'Transparent procurement benefits new suppliers at an administrative cost.'),
 ('social_conservatives','A Social Market Compact','p:enterprise:stab=0.06,eff=0.03,social=0.08;weekly:0.002',
  'Preserve private enterprise while underwriting social compromise.',
  'pension_contributions','Contributory Protection','p:enterprise:stab=0.08,eff=0.04,social=0.1,cg=0.01;weekly:0.002',
  'Contributory benefits broaden security but reduce resources available for immediate investment.'),
 ('regional_compromise','A Regional Development Pact','cost:2;b:607,industrial_complex,1',
  'Fund an industrial project in Honam to reduce the regional imbalance.'))
a,b=pair_end(g,p,7,
 ('civilian_security','Civilian Security Oversight','p:security:stab=0.05,intel=-0.04;action:intelligence_oversight',
  'Subject security agencies to civilian warrants and legislative oversight.'),
 ('security_compromise','Retain the Security Bargain','p:security:intel=0.08,stab=-0.04,police=0.04',
  'Retain parts of the security apparatus, accepting continued civic distrust.'))
node(g,'democratic_conservatism','Democratic Conservatism',(20,8),'p:settlement:trade=0.08,pp=-0.04',
 'Consolidate a constitutional conservative government with a credible international reputation.',pre=[[a['id'],b['id']]])

# The Two Kims are successive possible office holders, never permanently exclusive.
g=group('reform','Reform liberals · the Two Kims',(36,0),2,icon='democracy')
p=root(g,'reform_mandate','A Reform Mandate','p:mandate:stab=0.05,pp=-0.05;action:political_prisoner_review',
 'A reform government reopens civic politics and reviews political imprisonment.',days=14)
ys=node(g,'ys_civilian_authority','Kim Young-sam: Civilian Authority',(32,1),
 'p:ys_base:pp=0.06,org=-0.03;leader:Kim Young-sam',
 'Assert civilian authority over the officer corps, accepting a difficult transition in command.',
 pre=[[p['id']]],gate='ruling_party = 2 AND incumbent Kim Young-sam',owner='leader:Kim Young-sam')
dj=node(g,'dj_people_economy',"Kim Dae-jung: A People's Economy",(40,1),
 'p:dj_base:stab=0.06,social=0.06;leader:Kim Dae-jung',
 'Link civil rights to household welfare and regional inclusion.',
 pre=[[p['id']]],gate='ruling_party = 2 AND incumbent Kim Dae-jung',owner='leader:Kim Dae-jung')
for short,lead,base,cx,choices in [
 ('ys','Kim Young-sam',ys,32,[
 ('financial_disclosure','Financial Disclosure','p:ys_finance:interest=-0.4,pp=-0.05;cost:1',
  'Require disclosure and curb hidden political finance.',
  'real_name_accounts','Real-Name Finance','p:ys_finance:interest=-0.55,pp=-0.07,bureau=0.04;cost:1',
  'Introduce accountable financial identities as an early alternate reform.'),
 ('negotiated_cleanup','A Negotiated Cleanup','p:ys_finance:build=0.06,interest=0.2',
  'Secure business cooperation through phased accountability.',
  'corporate_transition','Corporate Transition Rules','p:ys_finance:build=0.08,interest=0.25,stab=-0.02',
  'Preserve investment momentum while deferring part of the cleanup.')]),
 ('dj','Kim Dae-jung',dj,40,[
 ('broad_welfare','Universal Social Insurance','p:dj_welfare:stab=0.08,social=0.15;weekly:0.003',
  'Build broad social protection with a substantial recurring public commitment.',
  'national_health_cover','Broaden Health Coverage','p:dj_welfare:stab=0.1,social=0.15,health=0.08;weekly:0.004',
  'Extend coverage to groups left outside employment-based protection.'),
 ('targeted_welfare','Targeted Social Protection','p:dj_welfare:stab=0.04,eff=0.04,bureau=0.06;weekly:0.001',
  'Target vulnerable households while keeping the fiscal commitment narrower.',
  'regional_equalization','Regional Equalization','p:dj_welfare:stab=0.06,eff=0.05,bureau=0.08;weekly:0.002',
  'Direct assistance to excluded regions, accepting administrative complexity.')])]:
    a,b=pair_end({**g,'anchor':[cx,0]},base,2,choices[0][:4],choices[1][:4])
    a['ownership']=b['ownership']='leader:'+lead;a['gate']=b['gate']=f'ruling_party = 2 AND incumbent {lead}'
    aa=node(g,*choices[0][4:6],(cx-2,3),*choices[0][6:8],pre=[[a['id']]],gate=a['gate'],owner=a['ownership'])
    bb=node(g,*choices[1][4:6],(cx+2,3),*choices[1][6:8],pre=[[b['id']]],gate=b['gate'],owner=b['ownership'])
    end=node(g,short+'_civil_coalition','Civilian Reform Coalition' if short=='ys' else 'Rights and Regional Inclusion',
     (cx,4),'p:'+short+'_coalition:trade=0.06,pp=-0.03;cost:1',
     'Build a durable civilian reform coalition with an ongoing cost in political bargaining.',
     pre=[[aa['id'],bb['id']]],gate=a['gate'],owner=a['ownership'])
    node(g,short+'_consolidation','Civilian Appointments' if short=='ys' else 'Independent Labour Mediation',
     (cx,5),'p:'+short+'_consolidation:stab=0.04,bureau=0.04',
     'Entrench accountable institutions rather than personal patronage.',pre=[[end['id']]],gate=a['gate'],owner=a['ownership'])
p=node(g,'sixth_republic','A Durable Civilian Republic',(36,7),
 'p:republic:stab=0.05,pp=-0.04;action:competitive_election_guarantees',
 'Consolidate competitive institutions under either reform leader.',
 pre=[[PREFIX+'ys_consolidation',PREFIX+'dj_consolidation']])
a,b=pair_end(g,p,8,
 ('democratic_alliance','Democracy within the Alliance','p:foreign:trade=0.1,foreign_def=-0.05',
  'Use democratic credibility to deepen the US alliance while accepting closer external influence.'),
 ('reform_nordpolitik','A Democratic Nordpolitik','p:foreign:trade=0.06,foreign_def=0.06,pp=-0.06;action:nordpolitik_negotiations',
  'Explore northern diplomatic openings while keeping decisions under civilian oversight.'))

g=group('army','Army / DJP · Chun and Roh',(52,0),22,icon='army')
p=root(g,'military_cabinet','The Military Establishment','p:mandate:org=0.05,stab=-0.05;xp:15;condition:actual military government',
 'A military-led government relies on discipline and command networks rather than a civilian mandate.',days=14)
p=stage(g,p,1,
 ('fifth_republic','The Fifth Republic','p:constitution:pp=0.15,stab=-0.07,police=0.08;condition:Chun incumbent;action:controlled_constitution',
  'Institutionalize Chun’s controlled presidency and civilian party vehicle.',
  'press_consolidation','Consolidate the Press','p:constitution:pp=0.19,stab=-0.09,police=0.1,trade=-0.04',
  'Centralize media and political supervision at a lasting cost to credibility.'),
 ('managed_liberalization','Managed Liberalization','p:constitution:stab=0.06,pp=-0.07;action:direct_election_settlement',
  'Accept a negotiated constitutional opening while retaining conservative institutions.',
  'june_declaration','Accept Direct Elections','p:constitution:stab=0.1,pp=-0.1;action:competitive_election_guarantees',
  'Restore direct presidential competition; this changes election rules rather than installing a predetermined winner.'),
 ('professional_officers','Professionalize the Officer Corps','p:officers:org=0.04,personnel=0.05;cost:1',
  'Promote professional competence while funding a better paid officer corps.'))
p=stage(g,p,2,
 ('stabilization_first','Stabilization First','p:stabilize:interest=-0.6,ic=-0.04,stab=-0.02',
  'Restrain inflation and implicit guarantees through a difficult industrial adjustment.',
  'industrial_rationalization','Rationalize Heavy Industry','p:stabilize:interest=-0.7,eff=0.06,ic=-0.03;cost:2',
  'Restructure overextended industrial groups while preserving viable plants.'),
 ('industrial_continuity','Protect Industrial Momentum','p:stabilize:ic=0.07,interest=0.45;weekly:0.003',
  'Support strategic enterprises through the downturn, accepting renewed financial exposure.',
  'export_recovery','An Export Recovery Pact','p:stabilize:ic=0.1,interest=0.5,stab=-0.03;weekly:0.004',
  'Coordinate export recovery through wage restraint and public support.'),
 ('civil_administration','A Civil Administration','p:administration:bureau=-0.04,pp=-0.03;cost:1',
  'Put routine administration in professional civilian hands.'))
p=stage(g,p,3,
 ('hanahoe_compact','Retain the Officer Networks','p:command:org=0.06,pp=0.04,stab=-0.05',
  'Preserve loyal command networks, accepting political interference and civic distrust.',
  'security_continuity','Security Continuity','p:command:org=0.08,intel=0.06,stab=-0.07,police=0.04',
  'Retain coordinated security control under military-linked leadership.'),
 ('retire_political_officers','Retire Political Officers','p:command:stab=0.06,org=-0.03;cost:1',
  'Remove political commands, accepting temporary disruption in exchange for public trust.',
  'civilian_promotions','Civilian Promotion Oversight','p:command:stab=0.09,org=-0.02,bureau=0.04',
  'Make promotion accountable to civilian institutions rather than private officer clubs.'),
 ('olympic_republic','An International Opening','p:opening:trade=0.08,bureau=0.03;cost:1;condition:no active nationwide martial law',
  'Use international engagement to improve access and recognition; sporting prestige cannot erase repression.'))
pair_end(g,p,10,
 ('roh_nordpolitik','Roh’s Nordpolitik','p:legacy:trade=0.1,pp=-0.06;condition:Roh incumbent and competitive elections;action:nordpolitik_negotiations',
  'An elected Roh government explores diplomatic recognition and northern trade.'),
 ('conservative_merger','A Conservative Merger','p:legacy:pp=0.12,stab=-0.04;offer:conservative_merger',
  'Negotiate an elite conservative coalition. No opposition party or incumbent is transferred without political agreement.'))

g=group('usp','USP · social democracy',(6,14),3,icon='labour')
p=root(g,'social_democratic_cabinet','A Social Democratic Cabinet','p:mandate:stab=0.04,social=0.05;condition:legal USP government',
 'Kim Chul’s small socialist tradition becomes a governing coalition through a credible democratic opening.',days=14)
p=stage(g,p,1,
 ('universal_insurance','Universal Social Provision','p:welfare:stab=0.08,social=0.16;weekly:0.003',
  'Make social protection a national entitlement financed by a broad public commitment.',
  'rural_health','Rural Health Provision','p:welfare:stab=0.1,social=0.16,health=0.08;weekly:0.004',
  'Extend protection to farming and informal households outside large-company employment.'),
 ('contributory_welfare','Contributory Welfare','p:welfare:stab=0.05,eff=0.04,bureau=0.05;weekly:0.001',
  'Build a narrower, employment-funded system with lower immediate public spending.',
  'portable_benefits','Portable Benefits','p:welfare:stab=0.07,eff=0.05,bureau=0.07;weekly:0.002',
  'Carry benefits across employers while accepting a complex contribution system.'),
 ('independent_unions','Recognize Independent Unions','p:labour:stab=0.05,ic=-0.03;action:independent_union_law',
  'Legalize independent collective organization; exporters must accommodate bargaining.'))
p=stage(g,p,2,
 ('public_credit','Public Development Credit','p:ownership:civ=0.08,interest=0.25,bureau=0.04;cost:1',
  'Keep credit allocation accountable to public institutions rather than conglomerates.',
  'cooperative_industry','Cooperative Industry','p:ownership:civ=0.1,eff=0.03,interest=0.3,bureau=0.05;cost:2',
  'Support producer cooperatives at the cost of capital and administrative effort.'),
 ('social_market_industry','A Bargained Social Market','p:ownership:eff=0.06,ic=-0.02,social=0.05',
  'Preserve private industry under binding employment and wage agreements.',
  'works_councils','Works Councils','p:ownership:eff=0.08,ic=-0.02,pp=-0.04,social=0.05',
  'Give labor representation in company decisions, exchanging speed for coordination.'),
 ('balanced_development','Equal Provincial Opportunity','cost:2;b:607,industrial_complex,1',
  'Support industrial employment outside established corporate centers.'))
a,b=pair_end(g,p,7,
 ('socialist_alliance','An Independent Socialist Voice','p:external:foreign_def=0.1,trade=-0.04;action:socialist_international_contacts',
  'Maintain an independent democratic left and cultivate foreign social-democratic contacts.'),
 ('neutral_peace','Armed Neutral Diplomacy','p:external:foreign_def=0.06,defence=0.04,personnel=0.06;offer:neutrality_guarantees',
  'Negotiate international neutrality while maintaining a funded defense. Treaty withdrawal needs a separate accepted settlement.'))
node(g,'labour_republic','A Republic of Social Partnership',(6,22),'p:settlement:stab=0.05,pp=-0.05',
 'Consolidate a democratic labor settlement without adopting Pyongyang’s political system.',pre=[[a['id'],b['id']]])

# Two distinct small political trees, not a claim that the minjung movement was one party.
g=group('minjung','Students and independent Marxists',(20,14),gate='Exact governing slot 5 or 19; separate roots below',icon='students',ownership='party')
for cx,slot,key,title,fx,desc,choices,cap in [
 (17,5,'student_cabinet','A Civic Reconstruction Cabinet','p:student_base:research=0.03,pp=-0.07;condition:legalized student-led civilian government',
  'A radical civic coalition turns campus mobilization into accountable government; this is alternate history.',
  [('campus_pluralism','Campus Pluralism','p:student_education:research=0.05,education=0.08',
    'Protect universities and open debate while funding a wider educational mission.',
    'technical_scholarships','Technical Scholarships','p:student_education:research=0.07,education=0.1;cost:1',
    'Widen technical education instead of relying only on elite institutions.'),
   ('national_service_schools','National Service Schools','p:student_education:training=-0.08,manpower=0.04,education=0.06,pp=-0.05',
    'Link civic service to technical education, diverting young people from civilian careers.',
    'community_service','Community Technical Service','p:student_education:training=-0.1,manpower=0.06,education=0.08,pp=-0.05',
    'Expand a compulsory service programme with practical training and a wider obligation.')],
  ('civic_charter','A Civic Charter','p:student_charter:stab=0.06,pp=-0.05;action:civic_pluralism',
   'Make the civic coalition constitutional rather than a permanent campus emergency.')),
 (23,19,'independent_left','An Independent Socialist Government','p:left_base:foreign_def=0.08,trade=-0.05;condition:legal independent Marxist government',
  'A southern socialist coalition claims independence from both blocs; it is an explicitly alternate route.',
  [('worker_management','Worker Management','p:left_ownership:eff=0.07,pp=-0.08,bureau=0.05',
    'Give workplace councils managerial authority, accepting slower investment decisions.',
    'industrial_councils','Industrial Councils','p:left_ownership:eff=0.1,pp=-0.1,bureau=0.07',
    'Coordinate sector-wide worker management under a public investment plan.'),
   ('strategic_public_sector','A Strategic Public Sector','p:left_ownership:ic=0.06,interest=0.3,bureau=0.05;cost:2',
    'Nationalize strategic credit and infrastructure without absorbing every small enterprise.',
    'public_holding_fund','A Public Holding Fund','p:left_ownership:ic=0.09,interest=0.4,bureau=0.07;cost:2',
    'Concentrate capital in publicly owned industrial holdings with explicit financial exposure.')],
  ('southern_socialism','An Independent Southern Socialism','p:left_charter:foreign_def=0.08,defence=0.04,trade=-0.04;offer:independent_left_dialogue',
   'Open dialogue with the North without conceding Southern sovereignty or automatic annexation.'))
]:
    gg={**g,'anchor':[cx,14],'gate':f'check_variable = {{ ruling_party = {slot} }}','ownership':f'party:{slot}'}
    p0=node(gg,key,title,(cx,14),fx,desc,days=14)
    if g['root'] is None:g['root']=p0['id']
    a,b=pair_end(gg,p0,1,choices[0][:4],choices[1][:4])
    aa=node(gg,*choices[0][4:6],(cx-2,16),*choices[0][6:8],pre=[[a['id']]])
    bb=node(gg,*choices[1][4:6],(cx+2,16),*choices[1][6:8],pre=[[b['id']]])
    cc=node(gg,*cap[:2],(cx,17),*cap[2:4],pre=[[aa['id'],bb['id']]])
    node(gg,key+'_public_accounts','Public Investment Accounts',(cx,18),
     'p:'+key+'_accounts:interest=-0.2,pp=-0.03;cost:1',
     'Publish investment accounts to constrain insider privilege and improve public credit.',pre=[[cc['id']]])

g=group('rpr','RPR · revolutionary reunification',(36,14),4,icon='revolution')
p=root(g,'revolutionary_cabinet','A Revolutionary Southern Cabinet','p:mandate:ic=0.04,stab=-0.08,trade=-0.08;condition:actual revolutionary government',
 'An underground movement becomes a government only after a resolved revolutionary or political transition. This is a difficult alternate history.',days=14)
p=stage(g,p,1,
 ('southern_front','A Southern Popular Front','p:front:stab=0.06,pp=-0.08,foreign_def=0.06',
  'Broaden the revolutionary coalition while protecting a separate Southern government.',
  'pluralist_socialism','Pluralist Socialist Institutions','p:front:stab=0.09,pp=-0.1,foreign_def=0.06;action:left_pluralism',
  'Accept independent socialist and civic representation rather than a monopoly party.'),
 ('vanguard_party','A Vanguard Party','p:front:pp=0.18,stab=-0.07,police=0.08',
  'Centralize the revolution under a disciplined party-state.',
  'party_cadres','Party Cadres in Industry','p:front:pp=0.2,ic=0.04,stab=-0.09,police=0.1',
  'Embed cadres in workplaces while accepting coercion and managerial interference.'),
 ('revolutionary_reconstruction','Reconstruct Southern Industry','cost:3;b:606,industrial_complex,1;p:rebuild:interest=0.35',
  'Rebuild production under a public investment guarantee.'))
p=stage(g,p,2,
 ('confederal_revolution','A Confederal Revolution','p:korea:foreign_def=0.08,pp=-0.06;offer:sovereign_confederation',
  'Offer Pyongyang a sovereign confederation. The other Korea may reject every constitutional concession.',
  'southern_guarantees','Southern Institutional Guarantees','p:korea:foreign_def=0.1,stab=0.04,pp=-0.08;condition:accepted sovereign_confederation',
  'Entrench separate Southern institutions inside an accepted inter-Korean framework.'),
 ('northern_alignment','Align with Pyongyang','p:korea:org=0.06,trade=-0.1,foreign_def=-0.08;offer:northern_security_compact',
  'Seek a Northern security compact at the cost of external access and policy autonomy.',
  'joint_planning','Joint Economic Planning','p:korea:ic=0.08,trade=-0.1,foreign_def=-0.1;weekly:0.003;condition:accepted northern_security_compact',
  'Coordinate selected industrial plans after bilateral agreement, without a free transfer of territory.'),
 ('southern_settlement','A Southern Constitutional Settlement','p:settlement:stab=0.05,bureau=0.05;action:southern_ratification',
  'Ratify the Southern settlement; any eventual unified state still requires both players’ approval.'))
node(g,'revolutionary_diplomacy','Recognition of the Southern Government',(36,21),
 'offer:revolutionary_recognition;note:No guaranteed grants or treaty removal',
 'Seek external recognition of the new government. Recognition does not force a partner into an alliance.',pre=[[p['id']]])

g=group('security','KCIA · an exceptional security cabinet',(52,14),7,icon='security')
p=root(g,'security_cabinet','A Security Directorate','p:mandate:intel=0.08,stab=-0.08,police=0.08;condition:actual KCIA-led government',
 'A security agency governing directly is an exceptional alternate outcome, not the normal Park starting government.',days=14)
p=stage(g,p,1,
 ('internal_directorate','An Internal Directorate','p:service:intel=0.1,pp=0.08,stab=-0.08,police=0.08',
  'Concentrate domestic intelligence and political surveillance.',
  'national_files','Centralize National Files','p:service:intel=0.14,pp=0.1,stab=-0.1,police=0.1',
  'Central records improve surveillance while extending arbitrary state power.'),
 ('external_service','An External Intelligence Service','p:service:intel=0.08,encryption=0.05,bureau=0.06',
  'Redirect resources toward counterintelligence and external threats.',
  'warranted_operations','Warrants and Professional Standards','p:service:intel=0.1,encryption=0.08,bureau=0.08,pp=-0.04',
  'Professional safeguards limit political operations and require oversight.'),
 ('counter_infiltration','Counter-Infiltration Coordination','p:border:core_def=0.04,police=0.04;cost:1',
  'Coordinate border intelligence without creating a parallel combat force.'))
p=stage(g,p,2,
 ('security_technocrats','Technocrats under Protection','p:governance:build=0.07,stab=-0.04,interest=0.2',
  'Protect a technocratic cabinet through the security apparatus.',
  'protected_planning','Protected Industrial Planning','p:governance:build=0.1,stab=-0.06,interest=0.3;weekly:0.002',
  'Guarantee strategic planning at a political and financial cost.'),
 ('civilian_exit','Negotiate a Civilian Exit','p:governance:stab=0.07,pp=-0.1;action:civilian_transition_agreement',
  'Negotiate safeguards for a return to civilian politics.',
  'disclose_archives','Open the Political Archives','p:governance:stab=0.1,pp=-0.12,intel=-0.03;action:political_case_review',
  'Accept a controlled disclosure process and the loss of political intelligence assets.'),
 ('security_settlement','A National Security Settlement','p:settlement:core_def=0.04,bureau=0.04;cost:1',
  'Institutionalize security responsibilities under the chosen governing settlement.'))
node(g,'security_handover','Guarantees for a Handover',(52,21),
 'action:security_transition_terms;pp_once:75;stability:-0.03',
 'Offer a concrete transition compact. A change of government ends this directorate’s active programme.',pre=[[p['id']]])

g=group('economy','National development · industry and society',(70,0),icon='industry')
p=root(g,'third_plan','Review the Development Plan','cost:1;p:planning:build=0.04,bureau=0.03',
 'Review the next development plan against credit, workforce and energy constraints.',days=21)
p=stage(g,p,1,
 ('heavy_chemical_drive','The Heavy and Chemical Drive','p:industrial_model:ic=0.06,eff=0.03,interest=0.4;cost:3',
  'Commit to capital-intensive steel, machinery and chemicals, increasing credit concentration.',
  'pohang_foundry','Commission Pohang Capacity','cost:3;b:605,industrial_complex,1;p:industrial_model:ic=0.08,eff=0.04,interest=0.5',
  'Bring paid industrial capacity into operation; no free raw resource or uranium grant.'),
 ('light_export_model','Diversify Light Exports','p:industrial_model:civ=0.09,ic=-0.02,workers=0.03;cost:2',
  'Expand labor-intensive exports and smaller firms rather than concentrating on heavy plants.',
  'provincial_export_zones','Provincial Export Zones','cost:2;b:606,industrial_complex,1;p:industrial_model:civ=0.11,ic=-0.02,workers=0.04',
  'Create a paid provincial export base with a continuing demand for labor.'),
 ('freight_corridors','Complete the Freight Corridors','cost:2;b:604,infrastructure,1;b:605,infrastructure,1;start_replace:rural',
  'Improve the Seoul–southeast transport corridor and reduce the infrastructure gap.'))
p=stage(g,p,2,
 ('assembly_contracts','Assembly and Technology Licences','p:technology:eff=0.05,foreign_def=-0.05;cost:1;offer:technology_licence',
  'Negotiate imported production knowledge. A signed licence provides access, not a free future technology.',
  'technical_colleges','Technical Colleges','p:technology:eff=0.07,research=0.02,education=0.06,foreign_def=-0.05;cost:1',
  'Train technicians to absorb licensed production methods.'),
 ('domestic_engineering','Domestic Engineering Institutes','p:technology:research=0.04,education=0.08;cost:2',
  'Fund local engineering capacity, accepting higher costs and a slower initial industrial payoff.',
  'industrial_laboratories','Industrial Laboratories','p:technology:research=0.06,education=0.1;cost:2',
  'Develop local laboratories without bypassing research-year or special-project restrictions.'),
 ('industrial_skills','A Skilled Industrial Workforce','p:skills:workers=-0.03,education=0.04;cost:1',
  'Raise workforce efficiency through vocational training; this does not force an Imperia development tier.'))
p=stage(g,p,3,
 ('labor_discipline','Preserve Wage Discipline','p:labour:ic=0.07,stab=-0.06;start_replace:labour',
  'Preserve export margins through constrained bargaining, leaving a continuing legitimacy cost.',
  'controlled_arbitration','State-Controlled Arbitration','p:labour:ic=0.09,stab=-0.07,police=0.04',
  'Resolve disputes through state arbitration and security pressure.'),
 ('labor_compact','A National Labour Compact','p:labour:stab=0.06,eff=0.04,ic=-0.03;start_replace:labour',
  'Accept wage bargaining and labor protection in exchange for cooperation and social trust.',
  'safety_inspectorate','An Independent Safety Inspectorate','p:labour:stab=0.08,eff=0.05,ic=-0.03,bureau=0.05;cost:1',
  'Enforce workplace safety through an independent public service.'),
 ('urban_services','Housing and Urban Services','cost:2;p:urban:stab=0.03,cg=0.01;start_replace:rural',
  'Reduce the social burden of migration through paid urban services.'))
p=stage(g,p,4,
 ('export_credit_guarantees','Guarantee Export Credit','p:finance:ic=0.06,interest=0.4;weekly:0.002;start_replace:finance',
  'Use state guarantees to sustain export investment through external shocks.',
  'strategic_refinancing','Strategic Refinancing','p:finance:ic=0.08,interest=0.5;weekly:0.003',
  'Keep strategic firms operating at the cost of larger public exposure.'),
 ('banking_discipline','Discipline the Banks','p:finance:interest=-0.5,ic=-0.03;start_replace:finance',
  'Restrain connected lending and hidden guarantees, accepting slower near-term industrial expansion.',
  'orderly_restructuring','Orderly Industrial Restructuring','p:finance:interest=-0.6,eff=0.04,ic=-0.02;cost:2',
  'Restructure overextended firms without a direct debt reset.'),
 ('energy_planning','A Diversified Energy Plan','cost:1;action:energy_project_options;start_replace:energy',
  'Open existing energy-project decisions and reduce reliance on a single imported fuel route.'))
a,b=pair_end(g,p,13,
 ('civil_nuclear','Safeguarded Civil Nuclear Power','cost:2;action:existing_civil_nuclear_projects;condition:native safeguards, technology and projects',
  'Fund access to the existing civilian nuclear programme. Reactors, fuel and running costs follow current Imperia rules.'),
 ('thermal_diversification','Thermal and Fuel Diversification','cost:2;p:energy:ic=0.04,interest=0.2;action:existing_energy_purchase_options',
  'Diversify imported fuel and thermal generation; supply contracts still require a willing partner.'))
node(g,'advanced_export_economy','An Advanced Export Economy',(70,14),
 'p:maturity:eff=0.04,workers=-0.03,education=0.04;cost:2',
 'Consolidate industrial skills and quality control through the existing development system.',pre=[[a['id'],b['id']]])

g=group('defence','Defence · deterrence and autonomy',(84,0),icon='army')
p=root(g,'defence_review','Review National Defence','xp:25;p:readiness:core_def=0.04,personnel=0.04;cost:1',
 'Review readiness after the 1968 raids and the Nixon Doctrine. No starting units or stockpiles are created.',days=21)
p=stage(g,p,1,
 ('dmz_deterrence','A Fortified DMZ','p:posture:core_def=0.08,attack=-0.03;weekly:0.002',
  'Prioritize prepared positions and defensive depth over offensive maneuver.',
  'counter_infiltration_units','Counter-Infiltration Training','p:posture:core_def=0.1,org=0.03,attack=-0.03;weekly:0.003;xp:15',
  'Train the existing force to respond to infiltration and local attacks.'),
 ('mobile_deterrence','A Mobile Deterrent','p:posture:attack=0.05,org=0.04,supply=0.05;weekly:0.002',
  'Keep a mobile reserve and limited offensive options at greater logistical cost.',
  'combined_arms_training','Combined-Arms Training','p:posture:attack=0.07,org=0.05,supply=0.07;weekly:0.003;xp:15',
  'Develop coordinated maneuver without granting out-of-period equipment.'),
 ('defence_logistics','Military Transport and Logistics','cost:2;b:606,infrastructure,1;p:logistics:supply=-0.03,personnel=0.03',
  'Fund transport capacity and logistical staff.'))
p=stage(g,p,2,
 ('allied_procurement','Allied Procurement','p:procurement:equipment=-0.06,foreign_def=-0.06;offer:allied_procurement_contract',
  'Negotiate access to affordable allied systems while accepting dependence on suppliers.',
  'licensed_maintenance','Licensed Maintenance','p:procurement:equipment=-0.08,eff=0.03,foreign_def=-0.07;cost:1;condition:accepted allied_procurement_contract',
  'Build maintenance capability after a procurement agreement; no automatic foreign stockpile.'),
 ('domestic_defence_industry','Domestic Defence Industry','cost:3;p:procurement:arms=0.1,ic=0.03,interest=0.3',
  'Fund domestic armament production at the cost of capital and civilian opportunity.',
  'changwon_production','A Changwon Production Base','cost:3;b:605,arms_factory,1;p:procurement:arms=0.12,ic=0.04,interest=0.4',
  'Create a paid military-industrial production base using existing equipment technologies.'),
 ('defence_quality','Defence Quality Standards','p:quality:eff=0.04,bureau=0.03;cost:1',
  'Improve standards and inspections across the selected procurement model.'))
p=stage(g,p,3,
 ('reserve_army','The Reserve Army','p:service:manpower=0.08,training=-0.06,workers=0.04;weekly:0.001',
  'Maintain a broad trained reserve, diverting labor and training time from civilian life.',
  'civil_defence_training','Civil Defence Training','p:service:manpower=0.1,training=-0.08,workers=0.05;weekly:0.002',
  'Expand readiness obligations without generating free military formations.'),
 ('professional_core','A Professional Core','p:service:org=0.06,morale=0.05,personnel=0.1;weekly:0.001',
  'Invest in a smaller professional core with higher personnel costs.',
  'career_ncos','A Career NCO Corps','p:service:org=0.08,morale=0.07,personnel=0.12;weekly:0.002;xp:15',
  'Build experienced small-unit leadership through a funded career structure.'),
 ('joint_staff','An Integrated Joint Staff','p:staff:org=0.03,bureau=0.04;xp:10',
  'Coordinate service planning without giving the military a domestic political mandate.'))
a,b=pair_end(g,p,10,
 ('coastal_defence','Coastal Denial','p:maritime:naval_org=0.08,air_eff=-0.03;cost:2;b:608,radar_station,1',
  'Prioritize coastal warning and maritime readiness over air-force investment.'),
 ('air_defence','Air Defence Priority','p:maritime:air_eff=0.06,naval_org=-0.03;cost:2;b:604,anti_air_building,1',
  'Prioritize air-defense coverage while accepting slower maritime modernization.'))
node(g,'coastal_logistics','Coastal Logistics',(82,11),'cost:2;b:605,dockyard,1',
 'Fund a coastal yard for fleet support; no modern warship or task force is spawned.',pre=[[a['id']]])
node(g,'air_command','Integrated Air Command',(86,11),'p:air:air_eff=0.03,equipment=0.04;cost:1',
 'Improve air coordination through a funded command structure.',pre=[[b['id']]])

g=group('foreign','Foreign policy · alliances and markets',(98,0),icon='diplomacy')
p=root(g,'diplomatic_review','A Diplomatic Review','p:service:trade=0.05,bureau=0.03;cost:1',
 'Review the alliance, Japanese cooperation and new market access from a divided peninsula.',days=21)
p=stage(g,p,1,
 ('alliance_bargain','Renew the Alliance Bargain','p:alignment:core_def=0.05,foreign_def=-0.05;offer:us_alliance_assurance',
  'Seek American assurances after the troop drawdown. A focus cannot command US deployments.',
  'burden_sharing','A Burden-Sharing Agreement','p:alignment:org=0.04,core_def=0.05,foreign_def=-0.07;weekly:0.003;condition:accepted us_alliance_assurance',
  'Fund agreed local readiness in return for a credible alliance settlement.'),
 ('strategic_autonomy','Strategic Autonomy','p:alignment:foreign_def=0.1,trade=-0.04;cost:1',
  'Broaden diplomatic room while accepting narrower privileged access.',
  'diverse_partners','Diversify Security Partners','p:alignment:foreign_def=0.12,trade=0.02,bureau=0.05;offer:security_partner_contacts',
  'Seek multiple limited partners without automatically changing treaties or factions.'),
 ('vietnam_legacy','Settle the Vietnam Commitment','offer:vietnam_withdrawal_settlement;condition:active Vietnam commitment;note:bypass with no rewards if no commitment',
  'Negotiate an end to the existing commitment and veterans’ obligations. No units, experience or cash from an absent expedition.'))
p=stage(g,p,2,
 ('japan_pragmatism','Pragmatic Cooperation with Japan','p:japan:trade=0.08,stab=-0.04;offer:japan_technology_finance',
  'Seek capital and production cooperation while accepting domestic controversy over colonial claims.',
  'joint_technical_training','Joint Technical Training','p:japan:trade=0.1,eff=0.03,stab=-0.05;cost:1;condition:accepted japan_technology_finance',
  'Fund training agreed with Japanese partners; no automatic transfer of research.'),
 ('claims_first','Put Historical Claims First','p:japan:stab=0.06,foreign_def=0.05,trade=-0.06;offer:historical_claims_dialogue',
  'Prioritize public legitimacy and historical claims while accepting more difficult economic cooperation.',
  'alternative_capital','Alternative Sources of Capital','p:japan:stab=0.06,foreign_def=0.06,interest=0.2,trade=-0.03;offer:alternative_finance_contacts',
  'Seek less concentrated capital sources with higher financing and diplomatic costs.'),
 ('overseas_workers','Protect Overseas Workers','cost:1;action:existing_guest_worker_contracts;condition:existing overseas-employment system',
  'Extend the existing miners’ and nurses’ programme through negotiated contracts; remittances use the shared system.'))
a,b=pair_end(g,p,7,
 ('nordpolitik','Open Northern Diplomacy','p:markets:trade=0.08,pp=-0.05;offer:nordpolitik_recognition',
  'Explore recognition and market access with socialist states under accepted bilateral terms.'),
 ('pacific_exports','A Pacific Export Network','p:markets:eff=0.04,trade=0.06,foreign_def=-0.04;offer:pacific_trade_contacts',
  'Deepen market access among existing Pacific partners at the cost of external dependence.'))
node(g,'middle_power','A Diplomatic Middle Power',(98,8),'p:standing:trade=0.05,bureau=0.04;cost:1',
 'Build a larger diplomatic service to sustain the selected overseas orientation.',pre=[[a['id'],b['id']]])

g=group('korea','North Korea · rivalry, dialogue and settlement',(112,0),icon='korea')
p=root(g,'korean_question','The Korean Question','action:inter_korean_channels;pp_once:50',
 'A divided peninsula requires a policy toward Pyongyang. Diplomatic offers preserve both players’ control.',days=14)
p=stage(g,p,1,
 ('red_cross_channel','A Red Cross Channel','offer:red_cross_channel',
  'Offer talks on separated families through the existing North Korean channel architecture.',
  'family_reunions','Negotiate Family Reunions','cost:1;offer:family_reunions;condition:accepted red_cross_channel',
  'Offer a funded programme of limited family visits, subject to agreement on both sides.'),
 ('armed_vigilance','Armed Vigilance','p:opening:core_def=0.06,trade=-0.03;weekly:0.002',
  'Keep channels limited and fund a higher state of defensive readiness.',
  'incident_hotline','A Military Incident Hotline','offer:military_hotline;p:opening:core_def=0.07,trade=-0.03;weekly:0.002',
  'Offer an incident channel while maintaining a deterrent posture.'),
 ('review_korean_policy','Review Peninsula Policy','p:coordination:foreign_def=0.04,bureau=0.03;cost:1',
  'Coordinate diplomacy, defense and civilian oversight regardless of the first approach.'))
p=stage(g,p,2,
 ('peaceful_coexistence','A Coexistence Proposal','offer:nonaggression_compact',
  'Offer nonaggression and reciprocal restraint. Neither side is forced to disarm or abandon allies.',
  'verified_restraint','Verified Military Restraint','offer:verified_restraint;condition:accepted nonaggression_compact',
  'Negotiate reciprocal notification and verification with explicit funding and withdrawal terms.'),
 ('competitive_legitimacy','Compete for Korean Legitimacy','p:strategy:foreign_def=0.06,pp=0.04,trade=-0.04;cost:1',
  'Compete diplomatically while keeping military and humanitarian contacts available.',
  'defector_protection','Protect Defectors and Refugees','p:strategy:foreign_def=0.07,stab=0.02,social=0.06;weekly:0.001',
  'Fund protection and resettlement while accepting additional social responsibilities.'),
 ('reciprocal_contacts','Reciprocal Working Contacts','offer:working_contacts;note:Alternative to a stalled nonaggression agreement',
  'Offer narrow working contacts even when a larger political settlement has failed.'))
p=stage(g,p,3,
 ('sovereign_confederation','Offer a Sovereign Confederation','offer:sovereign_confederation;condition:accepted working_contacts OR nonaggression_compact',
  'Propose a confederal forum with separate governments, armed forces and economies.',
  'confederal_secretariat','A Joint Confederal Secretariat','cost:1;offer:confederal_secretariat;condition:accepted sovereign_confederation',
  'Offer a modest joint secretariat; cost and benefits begin only after both sides accept.'),
 ('two_governments','Recognition without Merger','offer:parallel_recognition;condition:accepted working_contacts OR nonaggression_compact',
  'Negotiate equal external representation and coexistence without dissolving either state.',
  'limited_trade','Limited Inter-Korean Trade','offer:limited_trade;condition:accepted parallel_recognition',
  'Offer a capped, funded trade arrangement with reciprocal obligations.'),
 ('korean_settlement','A Negotiated Korean Settlement','action:joint_ratification;condition:accepted confederal_secretariat OR limited_trade',
  'Ratify the chosen settlement. Territorial integration, annexation and faction transfers require a separate explicit bilateral treaty.'))

# A significant conservative party/leader has a separate civilian programme.
g=group('kjp','Kim Jong-pil · civilian conservatism',(6,26),0,
 gate='ruling_party = 0 AND incumbent Kim Jong-pil; NDRP identity after reorganization',icon='parliament')
p=root(g,'kjp_civilian_cabinet','Kim Jong-pil: Civilian Conservatism',
 'p:mandate:pp=0.06,bureau=-0.03,stab=-0.02;condition:actual Kim Jong-pil government',
 'A civilian conservative government combines administrative experience with the contested legacy of the 1961 order.',days=14,owner='leader:Kim Jong-pil')
p=stage(g,p,1,
 ('kjp_coalition','A Conservative Coalition','p:coalition:stab=0.06,pp=-0.06;action:conservative_merger',
  'Build a parliamentary conservative coalition without a return to presidential emergency rule.',
  'kjp_coalition_committees','Coalition Committees','p:coalition:stab=0.08,pp=-0.08,bureau=0.03',
  'Share parliamentary authority and preserve a civilian political organization.'),
 ('kjp_executive','An Administrative Presidency','p:coalition:build=0.06,pp=0.06,stab=-0.04',
  'Preserve executive coordination while accepting suspicions of the old governing networks.',
  'kjp_professional_cabinet','A Professional Cabinet','p:coalition:build=0.08,pp=0.06,stab=-0.05,bureau=0.03',
  'Professional ministers coordinate development under a strong civilian executive.'),
 ('kjp_provincial_credit','Provincial Development Credit','cost:2;b:606,industrial_complex,1',
  'Invest in Chungcheong without a permanent regional loyalty bonus.'))
p=stage(g,p,2,
 ('kjp_small_enterprise','A Small-Enterprise Compact','p:enterprise:civ=0.08,eff=0.03,ic=-0.02;cost:1',
  'Broaden credit access beyond dominant industrial groups.',
  'kjp_supplier_networks','Provincial Supplier Networks','p:enterprise:civ=0.1,eff=0.04,ic=-0.02,bureau=0.03',
  'Give provincial suppliers access to procurement and enforceable contracts.'),
 ('kjp_large_industry','A Strategic Industry Compact','p:enterprise:ic=0.06,interest=0.3;weekly:0.002',
  'Preserve industrial scale through negotiated state guarantees.',
  'kjp_export_compromise','An Export Compromise','p:enterprise:ic=0.08,interest=0.4,stab=-0.02;weekly:0.003',
  'Combine export targets and executive bargaining with larger financial exposure.'),
 ('kjp_party_settlement','A Civilian Party Settlement','p:settlement:stab=0.05,pp=-0.04;action:constitutional_party_guarantees',
  'Consolidate an independent civilian conservative party; a 1990-style merger remains a separate political bargain.'))
node(g,'kjp_korean_policy','Pragmatic Korean Diplomacy',(6,33),
 'offer:working_contacts;p:foreign:trade=0.04,pp=-0.03',
 'Offer practical working contacts while preserving separate Southern institutions.',pre=[[p['id']]])

# The mutual-exclusion at each stage is a deliberate policy opportunity cost.
# Failed diplomatic offers do not block the common domestic continuation: the
# join can also be satisfied by a visible recorded refusal/expiry of that offer.
for n in NODES:
    n['anchor']=next(g['root'] for g in GROUPS if g['id']==n['group'])
    anchor=next(x for x in NODES if x['id']==n['anchor'])
    n['offset']=[n['xy'][0]-anchor['xy'][0],n['xy'][1]-anchor['xy'][1]]
    if n['id']==n['anchor']:n['anchor']=None;n['offset']=n['xy'][:]
    n['receipt_policy']='one-time effects never replay; latest policy in each slot replaces prior values'

START = [
 {'id':PREFIX+'start_presidency','label':'A Contested Presidential Mandate','owner':'incumbent Park / DRP; reform replaces it',
  'modifiers':{'political_power_factor':0.08,'stability_factor':-0.08},
  'history':'1969 third-term amendment; Yushin is not yet in force.',
  'resolution':'First DRP constitutional choice replaces this slot; a constitutional opposition settlement removes it.'},
 {'id':PREFIX+'start_finance','label':'Concentrated Development Credit','owner':'national problem slot finance',
  'modifiers':{'industrial_capacity_factory':0.04,'interest_rate_multiplier_modifier':0.5},
  'history':'State-directed credit mobilizes industrial capital but concentrates leverage and guarantees.',
  'resolution':'National finance policy replaces this slot. Party credit policies can coexist and show their extra exposure.'},
 {'id':PREFIX+'start_labour','label':'The Human Cost of Export Growth','owner':'national problem slot labour',
  'modifiers':{'industrial_capacity_factory':0.03,'stability_factor':-0.08,'research_speed_factor':-0.02},
  'history':'Restricted bargaining, long hours and unsafe workplaces undermine legitimacy and skills.',
  'resolution':'Either national labor policy replaces it: discipline retains a legitimacy malus; compromise sacrifices output.'},
 {'id':PREFIX+'start_rural','label':'An Unevenly Developed Republic','owner':'national problem slot rural',
  'modifiers':{'production_speed_buildings_factor':-0.07,'stability_factor':-0.03},
  'history':'Rural infrastructure gaps and rapid urban migration constrain balanced development.',
  'resolution':'Freight corridors improve it to construction -3%, stability -2%; urban services remove the remainder.'},
 {'id':PREFIX+'start_alliance','label':'An Alliance under Adjustment','owner':'national external exposure',
  'modifiers':{'army_core_defence_factor':0.05,'foreign_influence_defense_modifier':-0.1},
  'history':'The US commitment deters attack while the Nixon Doctrine raises uncertainty and demands local responsibility.',
  'resolution':'An accepted US assurance deal replaces it; strategic autonomy trades defense backing for independence.'},
 {'id':PREFIX+'start_energy','label':'Imported Energy, Imported Risk','owner':'national problem slot energy',
  'modifiers':{'industrial_capacity_factory':-0.04,'interest_rate_multiplier_modifier':0.2},
  'history':'Rapid industrialization depends on imported fuel and external finance; this is exposure, not a 1973 shock in 1970.',
  'resolution':'Diversified energy planning reduces it; completed and funded existing energy projects remove remaining exposure.'},
 {'id':'mdcw_ni_overseas_employment_programme','label':'Overseas Employment Programme','owner':'existing starting idea; preserve actual code',
  'modifiers':{},'history':'Government-organized miners and nurses in West Germany; already granted in KOR country history.',
  'resolution':'Use existing guest-worker contracts and remittance accounting; never grant remittances twice.'},
]

def dump(path,obj):
    (OUT/path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    # Prove each icon source and modifier vocabulary against current target files.
    mod_text='\n'.join(p.read_text(encoding='utf-8-sig',errors='replace') for folder in
      ('common/ideas','common/dynamic_modifiers','common/modifier_definitions') for p in (ROOT/folder).glob('*.txt'))
    used={k for n in NODES for p in n['effects']['policies'] for k in p['modifiers']}
    used|={k for s in START for k in s['modifiers']}
    assert all(re.search(r'(?m)^\s*'+re.escape(k)+r'\s*=',mod_text) for k in used)
    data={'status':'CONCEPT — awaiting owner approval; no loaded game files changed','country':'South Korea',
      'start':'1970-01-01','horizon':'1970–1990','prefix':PREFIX,'groups':GROUPS,'nodes':NODES,
      'starting_spirits':START,'modifier_labels':{KEYS[k]:v for k,v in LABELS.items()},
      'layout':{'grid':[96,130],'item':[165,128],'title':[147,20],
        'initial_focus':PREFIX+'developmental_state','continuous_focus_position':[7200,3000],
        'geometry_source':'interface/nationalfocusview.gui:446-493,573-585',
        'approximation':'Native art and grid. Browser font, symbol placement, connector routing and states approximate engine presentation.'},
      'rules':{
        'politics':'Exact ruling_party slot plus incumbent leader where required, checked at start AND completion. Coalition membership alone never unlocks an incumbent programme.',
        'lifecycle':'Earned national/party/leader slots retained; only active owner contributes. Refresh on government change, load and monthly failsafe. No grant or construction in refresh.',
        'weekly':'Latest per-focus weekly commitment replaces earlier value in the same policy slot; active commitments are summed into COLDWAR_KOR_weekly_cost and consumed by native calculate_additional_expense_rate. NEW adapter required; not an existing KOR API.',
        'money':'Treasury_change then modify_treasury_effect; billions; paid projects 1–10bn; normal native borrowing; no treasury>=cost gate for domestic expenditure.',
        'buildings':'Require owned and controlled intended state and room for the stated building; no silent alternative recipient. Conditions visible. Commit price and grant atomically; a full state prevents the focus from starting/completing.',
        'offers':'Offer dispatch is not acceptance. Recipient may accept/refuse. No material agreement bonus or payment before acceptance; finite pending time, both-party revalidation and once-only signature required.',
        'gates':'No universal year locks. Actual party office, constitutional settlement, research/project stage, peace and signed agreements supply meaningful gates.',
        'focus_time':'Short administrative entries 14/21d, normal programmes 35d; paid construction and major constitutions 49/70d assigned explicitly in final catalogue.',
      },
      'party_migration':{
        'confirmed_problem':'Registry has NDP=1, Forties=2, USP=3; native leader pools/retirement alternatives still put Kim Young-sam at1, Kim Dae-jung at3. Roh absent.',
        'proposal':'Preserve Park and start DRP=0/EPB coalition13. Reconcile leader pools and retirement alternatives to the registry: both reform Kims in2, Kim Chul/USP in3; NDP elders1; Chun and new Roh in22 with dated identity labels DJP. This is a proposed migration, not existing runtime behavior.',
        'safety':'Roh is not a 1970 alternate starting leader. Add nomination/office transitions through current native political machinery. All Kim/Chun/Roh office flags read actual incumbent; future RDP/PDP/DJP labels reflect real office/history, not invented ideology tokens.',
        'minor_slots':'No Islamic, monarchy, Confucian or Ilmin ruling branches. EPB, agricultural cooperatives and business associations influence policy rather than receive fictitious historical mass-party careers.',
      }}
    # Treasury is the economic cost; duration is a meaningful programme cost too.
    for n in data['nodes']:
        if n['effects']['buildings']: n['days']=49;n['cost']=7
        if n['key'] in ('yushin','parliamentary_republic','checked_presidency','fifth_republic','managed_liberalization','sovereign_confederation'):
            n['days']=70;n['cost']=10
        if n['key']=='sixth_republic':n['days']=49;n['cost']=7
    from COLDWAR_KOR_contracts import enrich
    from COLDWAR_KOR_review_fixes import refine
    from COLDWAR_KOR_native_plan import declare
    from COLDWAR_KOR_expansion import expand
    from COLDWAR_KOR_transition_plan import complete_plan
    data=enrich(data)
    data=refine(data)
    data=expand(data,effects)
    data=complete_plan(data)
    data=declare(data)
    dump('COLDWAR_KOR_design.json',data)
    with (OUT/'COLDWAR_KOR_focus_manifest.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(['id','title','group','x','y','anchor','dx','dy','days','gate','prerequisite_groups','exclusive','effects'])
        for n in NODES:w.writerow([n['id'],n['label'],n['group'],*n['xy'],n['anchor'],*n['offset'],n['days'],n['gate'],json.dumps(n['prerequisites']),','.join(n['mutually_exclusive']),json.dumps(n['effects'])])
    print(json.dumps({'focuses':len(NODES),'groups':len(GROUPS),'exclusive_pairs':sum(len(n['mutually_exclusive']) for n in NODES)//2,'output':str(OUT)}))

if __name__=='__main__':main()

