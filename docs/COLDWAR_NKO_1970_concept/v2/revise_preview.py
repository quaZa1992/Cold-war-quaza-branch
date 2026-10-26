# IMPERIA CW — Cold War: review-only DPRK v2 data and visualization; never installs HOI4 files.
"""Reads the v1 proposal and writes only v2 review artifacts / the chat visualization."""
from pathlib import Path
import sys, json, re, copy, hashlib, io, base64, importlib
from collections import Counter
from PIL import Image, ImageDraw, ImageFont, ImageOps

OUT=Path(__file__).resolve().parent
BASE=OUT.parent
ROOT=BASE.parents[1]
VIS=Path(r'C:\Users\sonyz\.codex\visualizations\2026\10\23\01a1692a-5756-7333-ab22-85bb052e65ec')
P='COLDWAR_NKO_'
D=json.loads((BASE/'COLDWAR_NKO_1970_design.json').read_text(encoding='utf-8'))
D=copy.deepcopy(D)
N=D['nodes']; G=D['groups']; B={n['key']:n for n in N}
STATE_NAMES={601:'Hamgyong',602:'Pyongyang',603:'Hwanghae',1199:'Kangwon',1200:'North Pyongan',1201:'Chagang'}
COUNTRY_NAMES={'NKO':'North Korea','SOV':'Soviet Union','CHI':'China','KOR':'South Korea','DDR':'East Germany','BUL':'Bulgaria','ROM':'Romania','EGY':'Egypt','JAP':'Japan'}
BUILDING_NAMES={'arms_factory':'Military Factory','industrial_complex':'Civilian Factory','agriculture_district':'Agricultural District','infrastructure':'Infrastructure','fossil_powerplant':'Fossil Power Plant','renewable_energy_infra':'Renewable Energy Infrastructure','radar_station':'Radar Station','dockyard':'Naval Dockyard'}
LABELS={key:label for key,label in D['stats'].values()}
LABELS.update({'army_artillery_attack_factor':'Artillery Attack','modifier_army_sub_unit_SP_R_arty_Bat_attack_factor':'Rocket Artillery Attack',
 'modifier_army_sub_unit_Militia_Bat_defence_factor':'Militia Defense','modifier_army_sub_unit_Mot_Militia_Bat_defence_factor':'Motorized Militia Defense',
 'modifier_army_sub_unit_Mot_Inf_Bat_attack_factor':'Motorized Infantry Attack','modifier_army_sub_unit_Mech_Inf_Bat_attack_factor':'Mechanized Infantry Attack',
 'modifier_army_sub_unit_Special_Forces_attack_factor':'Special Forces Attack','modifier_army_sub_unit_Special_Forces_defence_factor':'Special Forces Defense',
 'air_interception_detect_factor':'Interception Detection','static_anti_air_damage_factor':'Static Anti-Air Damage',
 'navy_submarine_attack_factor':'Submarine Attack','navy_screen_defence_factor':'Screen Defense',
 'army_infantry_attack_factor':'Infantry Division Attack','army_infantry_defence_factor':'Infantry Division Defense',
 'army_armor_attack_factor':'Armored Division Attack','foreign_influence_modifier':'Foreign Influence',
 'fossil_pp_energy_generation_modifier':'Fossil Power Generation','research_sharing_per_country_bonus_factor':'Technology Sharing Bonus'})
# Reuse MD's terminology, stripping only icon/color markup for this external preview.
native=ROOT/'localisation/english/replace/replaced_from_vanilla_modifiers_l_english.yml'
if native.exists():
    loc={m.group(1):m.group(2) for line in native.read_text(encoding='utf-8-sig').splitlines() if (m:=re.match(r'\s*([^ :]+):\d*\s*"(.*)"',line))}
    for key in list(LABELS):
        value=loc.get(key,loc.get('MODIFIER_'+key.upper()))
        if value:
            value=re.sub(r'£[A-Za-z0-9_]+','',value)
            value=re.sub(r'§.','',value).replace('$agriculture_district$','Agricultural District')
            if '$' not in value:LABELS[key]=value.strip()
for short,(key,label) in D['stats'].items():D['stats'][short][1]=LABELS.get(key,label)

PRICE_BY_OLD={1:.002,2:.004,3:.0075,4:.01,7.5:.015,3.75:.01,3.25:.01,8.5:.02,3.5:.0075,1.75:.005}
for n in N:
    old=n.pop('money',0)
    n['cost_gdp_share']=PRICE_BY_OLD.get(old,.003 if old else 0)
    n['eligibility_notes']=n.pop('runtime_guards',[])
    n.pop('charge_contract',None);n.pop('code',None);n.pop('effects',None)
    n['requirements']=[]
    n['player_gate']=''
    for e in n['extra']:
        if e['kind']=='building':
            e['slots']=e['levels']
            for k in ('full_project_cost','pricing','state_selection'):e.pop(k,None)
            e['slot_rule']='Add the stated number of shared slots, then the building, in the same selected state.'
        elif e['kind']=='debt':
            e.pop('amount',None);e['principal_gdp_share']=.015;e['recorded_principal']='Saved cash quote at project completion'
        elif e['kind']=='repay_loan':
            e.pop('amount',None);e['recorded_principal']='Outstanding machinery-loan principal only'
    n['labels']={k:LABELS.get(k,k) for k in n['modifiers']}

# Specific combat programmes improve the stated weapon or troop class.
def mods(key,remove=(),add=None):
    for k in remove:B[key]['modifiers'].pop(k,None)
    B[key]['modifiers'].update(add or {})
mods('mass_artillery',('army_attack_factor',),{'army_artillery_attack_factor':.06,'modifier_army_sub_unit_SP_R_arty_Bat_attack_factor':.06})
mods('ammunition_standards',add={'army_artillery_attack_factor':.04,'modifier_army_sub_unit_SP_R_arty_Bat_attack_factor':.04})
mods('red_guards',('army_core_defence_factor',),{'modifier_army_sub_unit_Militia_Bat_defence_factor':.10,'modifier_army_sub_unit_Mot_Militia_Bat_defence_factor':.10})
mods('mobile_army',add={'modifier_army_sub_unit_Mot_Inf_Bat_attack_factor':.06,'modifier_army_sub_unit_Mech_Inf_Bat_attack_factor':.06})
mods('air_defence',('air_mission_efficiency',),{'air_interception_detect_factor':.10,'static_anti_air_damage_factor':.05})
mods('coastal_denial',('navy_org_factor',),{'navy_submarine_attack_factor':.08,'navy_screen_defence_factor':.06})
mods('special_operations',add={'modifier_army_sub_unit_Special_Forces_attack_factor':.08,'modifier_army_sub_unit_Special_Forces_defence_factor':.05})
B['readiness_inspections']['description']='Regular inspections will expose gaps in readiness and require units to spend longer meeting their training standards.'
B['mass_artillery']['description']='Concentrated artillery can overwhelm prepared positions, but it will require larger stocks of ammunition and dependable transport.'
B['ammunition_standards']['description']='Standardized shells and consistent charges will improve the reliability of artillery fire while limiting production flexibility.'

# The user-approved 1994 succession applies to the incumbent Kim regime only.
for key,title,desc in [
 ('committee_succession','Collective Oversight','A stronger secretariat can restrain personal appointments and give the cabinet a larger role in governing the state.'),
 ('succession_rules','Cabinet Continuity','Preserve the cabinet’s authority through the next leadership transition without abandoning the party’s governing institutions.')]:
    B[key]['title']=title;B[key]['description']=desc
    B[key]['gate']='';B[key]['eligibility_notes']=[x for x in B[key]['eligibility_notes'] if 'date' not in x]
for key in ('family_succession','committee_succession','presidency'):
    B[key]['requirements'].append('Kim Il Sung is the national leader.')
    B[key]['availability_leader']='Kim Il Sung'

AGREEMENTS=[]
def agreement(key,partner,title,desc,nko,other,setup_nko,setup_partner,annual_nko,annual_partner,
              source,building=None,upgrades=None):
    a=dict(id=P+key,key=key,partner=partner,title=title,description=desc,
      recipient_decision='Consider the '+title,accept='Accept the Agreement',decline='Decline the Proposal',
      pending_days=90,perpetual=True,party_bound=False,
      resubmission='After refusal or expiry, a sender decision may reopen a completed focus proposal with fresh GDP quotes; no repeat completed-focus reward.',
      conditions=['Both countries exist.','Both countries have accepted the agreement.','Neither country is at war with the other.','Neither country imposes diplomatic, financial, economic or military sanctions on the other.'],
      nko=dict(spirit=title,modifiers=nko,setup_gdp_share=setup_nko,annual_commitment_gdp_share=annual_nko),
      recipient=dict(spirit=title,modifiers=other,setup_gdp_share=setup_partner,annual_commitment_gdp_share=annual_partner),
      provenance=source,buildings=building or [],upgrades=upgrades or [])
    for side in ('nko','recipient'):a[side]['weekly_formula']='current GDP × annual commitment ÷ 52'
    AGREEMENTS.append(a);return a

SOV=agreement('soviet_industry','SOV','Industrial Cooperation Protocol',
 'Pyongyang proposes a programme of machinery deliveries, power engineering and technical training under the existing treaty relationship.',
 {'productivity_growth_modifier':.06,'production_factory_max_efficiency_factor':.06,'fossil_pp_energy_generation_modifier':.08,'foreign_influence_defense_modifier':-.04},
 {'corporate_tax_income_multiplier_modifier':.015,'foreign_influence_modifier':.05,'education_cost_multiplier_modifier':.02},.01,.0002,.0015,.0002,
 ['1961 Soviet–DPRK treaty, articles 3–6','https://treaties.un.org/doc/Publication/UNTS/Volume%20420/volume-420-I-6045-English.pdf'],
 [dict(recipient='NKO',type='industrial_complex',levels=1,slots=1,state_ids=[602,1200])])
CHI=agreement('china_border','CHI','Border Cooperation Protocol',
 'Pyongyang proposes regular agricultural exchange and border supply arrangements as relations with Beijing recover.',
 {'agricolture_productivity_modifier':.08,'supply_consumption_factor':-.04,'foreign_influence_defense_modifier':-.03,'tax_gain_multiplier_modifier':-.02},
 {'tax_gain_multiplier_modifier':.01,'trade_opinion_factor':.05,'bureaucracy_cost_multiplier_modifier':.015},.0015,.0002,.001,.0003,
 ['1961 PRC–DPRK treaty; 1970 rapprochement','https://worldjpn.net/documents/texts/docs/19610711.T1E.html'])
KOR=agreement('korean_channel','KOR','Inter-Korean Exchange Agreement',
 'Pyongyang proposes a permanent channel for family contacts, communications and peaceful exchange under the principles of the July Joint Statement.',
 {'stability_factor':.04,'trade_opinion_factor':.10,'army_attack_factor':-.03,'bureaucracy_cost_multiplier_modifier':.02},
 {'stability_factor':.04,'trade_opinion_factor':.10,'army_attack_factor':-.03,'bureaucracy_cost_multiplier_modifier':.02},.001,.001,.0005,.0005,
 ['1972 joint statement; this permanent compact is an alternate agreement','https://history.state.gov/historicaldocuments/frus1969-76v19p1/d151'])
NUC=agreement('civil_atomic','SOV','Civil Atomic Cooperation',
 'Pyongyang proposes research and reactor-engineering cooperation under agreed safeguards.',
 {'research_speed_factor':.04,'foreign_influence_defense_modifier':-.03,'education_cost_multiplier_modifier':.02},
 {'research_speed_factor':.01,'foreign_influence_modifier':.03,'education_cost_multiplier_modifier':.02},.005,.0002,.0005,.0001,
 ['Soviet reactor cooperation and the 1985 NPT bargain','https://www.iaea.org/sites/default/files/dprk.pdf'])
DDR=agreement('gdr_machinery','DDR','Machinery and Materials Protocol',
 'Pyongyang proposes East German machinery and specialist training in exchange for reliable industrial deliveries.',
 {'production_factory_efficiency_gain_factor':.08,'productivity_growth_modifier':.05,'resource_export_multiplier_modifier':-.03},
 {'industrial_capacity_factory':.03,'corporate_tax_income_multiplier_modifier':.02,'education_cost_multiplier_modifier':.03},.002,.0003,.0012,.0002,
 ['1977 GDR–DPRK agreement for economic, scientific and technical cooperation','https://www.wilsoncenter.org/sites/default/files/media/documents/publication/CWIHP_Bulletin_14-15.pdf'])
BUL=agreement('bulgarian_engineering','BUL','Engineering Cooperation Agreement',
 'Pyongyang proposes joint work on milling, communications and agricultural engineering, with deliveries linked to agreed project schedules.',
 {'agricolture_productivity_modifier':.06,'research_speed_factor':.025,'bureaucracy_cost_multiplier_modifier':.03},
 {'corporate_tax_income_multiplier_modifier':.015,'research_speed_factor':.01,'education_cost_multiplier_modifier':.02},.0012,.0002,.0008,.0001,
 ['1972 Bulgarian credit and later engineering/agrobiology programmes','https://www.wilsoncenter.org/publication/korea-the-bulgarian-archives-1945-1995-introduction'])
ROM=agreement('romanian_exchange','ROM','Industrial Exchange Agreement',
 'Pyongyang proposes a modest programme of industrial and agricultural exchange to diversify its socialist trading partners.',
 {'productivity_growth_modifier':.04,'trade_opinion_factor':.05,'bureaucracy_cost_multiplier_modifier':.025},
 {'corporate_tax_income_multiplier_modifier':.01,'trade_opinion_factor':.04,'bureaucracy_cost_multiplier_modifier':.02},.001,.0002,.0006,.00015,
 ['1970s Romanian–DPRK trade diversification; conservative abstraction','https://www.wilsoncenter.org/publication/korea-the-bulgarian-archives-1945-1995-introduction'])
EGY=agreement('egyptian_technical','EGY','Scientific and Technical Accord',
 'Pyongyang proposes scientific exchange, technical placements and maintenance training under the bilateral cooperation framework.',
 {'research_speed_factor':.025,'experience_gain_army':.04,'army_personnel_cost_multiplier_modifier':.03},
 {'research_speed_factor':.025,'equipment_cost_multiplier_modifier':-.03,'education_cost_multiplier_modifier':.03},.001,.0003,.0005,.0003,
 ['1969 scientific agreement and 1983 Egyptian–DPRK cooperation accord','https://sis.gov.eg/en/international-relations/bilateral-relations/north-korea/'])
JAP=agreement('japan_fisheries','JAP','Fisheries and Commerce Protocol',
 'Pyongyang proposes government authorization for a limited fisheries and commercial arrangement without diplomatic recognition.',
 {'agricolture_productivity_modifier':.04,'corporate_tax_income_multiplier_modifier':.01,'police_cost_multiplier_modifier':.02},
 {'agricolture_productivity_modifier':.02,'trade_opinion_factor':.03,'bureaucracy_cost_multiplier_modifier':.01},.001,.0002,.0003,.0001,
 ['Private fisheries arrangements reported in Japan’s 1980 Bluebook; a new state-approved protocol is alternate history','https://www.mofa.go.jp/mofaj/gaiko/bluebook/1980/s55-2010101-3.htm'])

def upgrade(a,key,title,nko,other,cost_nko=.001,cost_other=.0001):
    u=dict(key=key,title=title,nko=nko,recipient=other,setup_nko_gdp_share=cost_nko,setup_recipient_gdp_share=cost_other,
      requires_active_base=True,requires_recipient_decision=True,replaces_base=True)
    a['upgrades'].append(u);return u
upgrade(SOV,'soviet_training','Technical Placements',{'research_speed_factor':.03},{'research_speed_factor':.01})
upgrade(CHI,'border_trade','Border Logistics',{'agricolture_productivity_modifier':.02,'supply_consumption_factor':-.02},{'trade_opinion_factor':.02})
upgrade(KOR,'confederation_offer','Inter-Korean Consultative Council',{'productivity_growth_modifier':.03,'trade_opinion_factor':.04,'bureaucracy_cost_multiplier_modifier':.02},{'productivity_growth_modifier':.03,'trade_opinion_factor':.04,'bureaucracy_cost_multiplier_modifier':.02},.002,.002)
upgrade(NUC,'npt_offer','Civil Nuclear Power Protocol',{'nuclear_energy_generation_modifier':.08,'bureaucracy_cost_multiplier_modifier':.025},{'foreign_influence_modifier':.02,'bureaucracy_cost_multiplier_modifier':.015},.003,.0002)
upgrade(DDR,'gdr_training','Machine-Tool Standards',{'production_factory_max_efficiency_factor':.04},{'research_speed_factor':.015})
upgrade(BUL,'bulgarian_agrobiology','Agricultural Laboratories',{'agricolture_productivity_modifier':.04},{'agricolture_productivity_modifier':.02})
upgrade(ROM,'romanian_trade','Reciprocal Trade Schedules',{'trade_opinion_factor':.04},{'trade_opinion_factor':.03})
upgrade(EGY,'egyptian_missions','Technical Missions',{'experience_gain_army':.04},{'equipment_cost_multiplier_modifier':-.02})
upgrade(JAP,'japan_ports','Commercial Port Access',{'productivity_growth_modifier':.025,'police_cost_multiplier_modifier':.01},{'corporate_tax_income_multiplier_modifier':.005,'bureaucracy_cost_multiplier_modifier':.01})

for key,a in [('moscow_offer',SOV),('beijing_offer',CHI),('detente',KOR),('civil_atom',NUC)]:
    B[key]['extra']=[dict(kind='agreement',agreement=a['key'],stage='base')]
    B[key]['cost_gdp_share']=0
    # Benefits from these bilateral offers belong to the paired contract, not a unilateral focus receipt.
    if key in ('detente','civil_atom'):B[key]['modifiers']={}
for key,a in [('soviet_training',SOV),('border_trade',CHI),('confederation_offer',KOR),('npt_offer',NUC)]:
    B[key]['extra']=[dict(kind='agreement',agreement=a['key'],stage=key)]
    B[key]['cost_gdp_share']=0;B[key]['modifiers']={}
    B[key]['requirements']=['The '+a['title']+' is active.']
B['red_cross']['requirements']=['The Inter-Korean Exchange Agreement is active.']
B['confederation_offer']['requirements']+=['South Korea exists and is independent.','North Korea is at peace with South Korea.']
B['confederation_offer']['eligibility_notes']+=['KOR = { exists = yes is_subject = no }','NOT = { has_war_with = KOR }']
B['safeguards']['requirements']=['Civil Atomic Cooperation is active.']
B['safeguards']['extra']=[dict(kind='policy_note',text='Record the agreed safeguards commitments.')]

# New national Foreign Diplomacy branch. Contacts remain mixable, never mutually exclusive by patron.
foreign=dict(id='foreign',title='Foreign Diplomacy',x=68,y=0,slot=None,status='National programme',icon='trade',
 note='Bilateral cooperation with East Germany, Bulgaria, Romania, Egypt and Japan.')
G.append(foreign)
def add(key,title,group,x,y,pre=(),stats=None,price=0,cost=5,desc='',extra=None,icon='trade',requirements=None):
    gg=next(g for g in G if g['id']==group)
    parentgroups=[[P+a for a in p.split(',')] for p in pre]
    roots=[n for n in N if n['group']==group]
    v=dict(id=P+key,key=key,title=title,long_title=title,group=group,x=gg['x']+x,y=gg['y']+y,dx=x,dy=y,
       anchor=roots[0]['id'] if roots else None,prerequisites=parentgroups,mutex=[],cost=cost,days=cost*7,
       cost_gdp_share=price,modifiers=stats or {},labels={},description=desc,extra=extra or [],gate='',
       slot=gg['slot'],icon=icon,ownership='Party programme' if gg['slot'] is not None else 'National programme',
       remove=[],duration=None,historical_status=gg['status'],requirements=requirements or [],player_gate='',eligibility_notes=[])
    N.append(v);B[key]=v;return v
add('foreign_missions','A Wider Foreign Service','foreign',0,0,stats={'foreign_influence_modifier':.05,'bureaucracy_cost_multiplier_modifier':.04},price=.002,cost=3,
    desc='A professional foreign service can pursue trade and technical exchange while defending the republic’s freedom of action.',icon='goal_generic_positive_trade_relations')
for key,title,a,x in [('gdr_machinery','East German Machinery',DDR,-4),('bulgarian_engineering','Bulgarian Engineering',BUL,0),('romanian_exchange','Romanian Exchange',ROM,4)]:
    add(key,title,'foreign',x,1,['foreign_missions'],desc=a['description'],extra=[dict(kind='agreement',agreement=a['key'],stage='base')],icon='economic_civil_industry')
for key,title,a,x,parent in [('gdr_training','Machine-Tool Standards',DDR,-4,'gdr_machinery'),('bulgarian_agrobiology','Agricultural Science',BUL,0,'bulgarian_engineering'),('romanian_trade','Reciprocal Trade',ROM,4,'romanian_exchange')]:
    add(key,title,'foreign',x,2,[parent],desc='Propose a further programme of specialist exchange and reliable deliveries under the existing agreement.',extra=[dict(kind='agreement',agreement=a['key'],stage=key)],icon='education_reform',requirements=['The '+a['title']+' is active.'])
add('technical_exchange','Technical Exchange Council','foreign',0,3,['gdr_training,bulgarian_agrobiology,romanian_trade'],{'research_speed_factor':.025,'education_cost_multiplier_modifier':.03},.002,
    desc='Coordinate the foreign placements and technical standards required to make cooperation productive.',icon='socialist_science')
for key,title,a,x in [('egyptian_technical','The Egyptian Accord',EGY,-2),('japan_fisheries','Fisheries Negotiations',JAP,2)]:
    add(key,title,'foreign',x,4,['technical_exchange'],desc=a['description'],extra=[dict(kind='agreement',agreement=a['key'],stage='base')],icon='trade')
for key,title,a,x,parent in [('egyptian_missions','Technical Missions',EGY,-2,'egyptian_technical'),('japan_ports','Commercial Port Access',JAP,2,'japan_fisheries')]:
    add(key,title,'foreign',x,5,[parent],desc='Propose broader technical and commercial arrangements through the established bilateral channel.',extra=[dict(kind='agreement',agreement=a['key'],stage=key)],icon='goal_generic_positive_trade_relations',requirements=['The '+a['title']+' is active.'])

# Korean policy: détente, pressure and armed reunification are three distinct strategies.
def move(key,dx,dy):
    gg=next(g for g in G if g['id']==B[key]['group']);B[key].update(dx=dx,dy=dy,x=gg['x']+dx,y=gg['y']+dy)
for key,y in [('detente',4),('red_cross',5),('confederation_offer',6)]:move(key,-4,y)
for key,y in [('coercion',4),('front_broadcasting',5),('armed_bargaining',6)]:move(key,0,y)
move('recognition',-2,7);move('civilian_export',-4,8);move('security_export',0,8);move('external_resilience',-2,9)
war=add('war_line','The Liberation Line','diplomacy',4,4,['external_balance'],{'army_infantry_attack_factor':.06,'production_speed_industrial_complex_factor':-.10,'trade_opinion_factor':-.15},.005,
    desc='Reunification by force will demand a costly concentration of military power and the abandonment of a negotiated settlement.',icon='NKO_road_war')
for key in ('detente','coercion'):
    B[key]['mutex'].append(war['id']);war['mutex'].append(B[key]['id'])
add('forward_batteries','Forward Artillery','diplomacy',4,5,['war_line'],{'army_artillery_attack_factor':.10,'modifier_army_sub_unit_SP_R_arty_Bat_attack_factor':.10,'supply_consumption_factor':.06,'equipment_cost_multiplier_modifier':.05},.0075,
    desc='Forward batteries can strike southern defensive positions, but their deployment and ammunition stocks will be difficult to conceal.',icon='artillery')
add('forward_supply','Forward Supply Depots','diplomacy',4,6,['forward_batteries'],{'supply_consumption_factor':-.08,'army_personnel_cost_multiplier_modifier':.04},.0075,
    desc='Concentrate transport and stores behind the armistice line to sustain an offensive beyond its opening phase.',icon='focus_generic_supply_line')
add('war_mobilization','General Mobilization','diplomacy',4,7,['forward_supply'],{'army_infantry_attack_factor':.06,'army_armor_attack_factor':.06,'productivity_growth_modifier':-.08,'army_personnel_cost_multiplier_modifier':.08},.01,
    desc='Mobilize reserves and place industry on a war footing, drawing skilled workers away from civilian production.',icon='NKO_reserve')
add('campaign_command','A Southern Command','diplomacy',4,8,['war_mobilization'],{'max_planning_factor':.08,'army_org_factor':.04,'bureaucracy_cost_multiplier_modifier':.04},.005,
    desc='Establish the command arrangements needed to coordinate a sustained campaign south of the armistice line.',icon='dprk_army')
add('armed_reunification','Reunification by Force','diplomacy',4,9,['campaign_command'],price=.02,cost=10,
    desc='The leadership has resolved to pursue reunification through a renewed campaign against the South.',icon='NKO_38_parallel',
    requirements=['South Korea exists and is independent.','North Korea is at peace with South Korea.'],
    extra=[dict(kind='wargoal',target='KOR',type='annex_everything')])

G.append(dict(id='jongil',title='Kim Jong Il’s Leadership',x=64,y=17,slot=4,status='Historical succession from 8 July 1994',icon='Kim_Jong_il',note='Available only after Kim Jong Il succeeds the incumbent Kim regime.'))
add('jongil_authority','The Successor’s Authority','jongil',0,0,stats={'political_power_factor':.06,'bureaucracy_cost_multiplier_modifier':.04},cost=3,
    desc='Kim Jong Il must turn the authority accumulated under his father into an enduring command over party and state.',icon='Kim_Jong_il',requirements=['Kim Jong Il is the national leader.'])
add('jongil_cadres','The Party Centre','jongil',-2,1,['jongil_authority'],{'stability_factor':.06,'political_power_factor':.05,'research_speed_factor':-.03},.003,
    desc='Rely on the established party apparatus to preserve discipline and continuity through the transition.',icon='WPRG')
add('jongil_cabinet','A Cabinet Mandate','jongil',2,1,['jongil_authority'],{'productivity_growth_modifier':.06,'research_speed_factor':.03,'political_power_factor':-.05,'bureaucracy_cost_multiplier_modifier':.04},.003,
    desc='Give the cabinet greater authority to manage production and external procurement under the new leadership.',icon='parliament_box')
B['jongil_cadres']['mutex']=[B['jongil_cabinet']['id']];B['jongil_cabinet']['mutex']=[B['jongil_cadres']['id']]
add('jongil_settlement','The New Leadership','jongil',0,2,['jongil_cadres,jongil_cabinet'],{'stability_factor':.03,'bureaucracy_cost_multiplier_modifier':.02},
    desc='Consolidate the leadership settlement chosen for the Republic after the founding generation.',icon='Kim_Jong_il')
for n in N:
    if n['group']=='jongil':n['requirements']=['Kim Jong Il is the national leader.'];n['leader_bound']='Kim Jong Il'
    n['labels']={k:LABELS.get(k,k) for k in n['modifiers']}
    n['effects']=[]
    # Localized narrative is kept separate from internal routing and authoring evidence.
    if n['key']=='credit_reckoning':n['description']='Settle the machinery account or seek a revised schedule that the country can sustain.'
    if n['key']=='diaspora_trade':n['description']='Overseas Koreans provide a bridge for commerce and family contacts despite the absence of formal relations with Tokyo.'
    if n['key']=='joint_ventures':n['description']='Offer tightly controlled partnerships and tax concessions to attract foreign machinery and management expertise.'
    if n['key']=='kpa_handover':n['extra']=[dict(kind='policy_note',text='Open negotiations for a civilian transition.')]
    n['gate']=''
    if not n['eligibility_notes']:n['eligibility_notes']=['original_tag = NKO','IMP_is_1970_scenario = yes']
B['jongil_authority']['title']='Succession Authority'
B['external_balance']['title']='External Channels'
B['external_balance']['description']='Maintain diplomatic and commercial channels to secure machinery and markets while preserving freedom of action.'
B['technical_exchange']['description']='Put foreign technical placements and agreed standards to work in domestic production.'
for key,desc in {
    'gdr_training':'Agree machine-tool standards and specialist placements to make imported East German plant easier to operate and maintain.',
    'bulgarian_agrobiology':'Arrange field trials and exchanges with Bulgarian agronomists to improve the use of fertilizer, seed and agricultural machinery.',
    'romanian_trade':'Agree reciprocal industrial and agricultural delivery schedules that both trading partners can sustain.',
    'egyptian_missions':'Exchange technical missions and maintenance specialists to improve equipment support and practical training.',
    'japan_ports':'Negotiate limited port access and commercial services for authorized fisheries and trade without diplomatic recognition.'
}.items():B[key]['description']=desc
B['armed_reunification']['eligibility_notes']+=['KOR = { exists = yes is_subject = no }','NOT = { has_war_with = KOR }']
B['safeguards']['extra'][0].update(receipt=P+'safeguards_valid',producer='Set on guarded Safeguards focus completion. Retain the commitment until an explicit withdrawal; withdrawal clears this receipt and disables the safeguarded upgrade at both endpoints.')
B['npt_offer']['requirements'].append('The safeguards commitments remain in force.')
B['family_succession']['requirements'].append('Kim Jong Il remains available for succession.')
B['family_succession']['eligibility_notes'].append('NOT = { has_country_flag = COLDWAR_NKO_kim_jong_il_unavailable }')
for key in ('fuel_studies','strategic_option'):B[key]['requirements'].append('Developed or emerging economy.')
legacy_receipts={'COLDWAR_NKO_moscow_signed':P+'soviet_industry_accepted','COLDWAR_NKO_beijing_signed':P+'china_border_accepted',
    'COLDWAR_NKO_channel_signed':P+'korean_channel_accepted','COLDWAR_NKO_atomic_cooperation':P+'civil_atomic_accepted'}
for n in N:
    for field in ('eligibility_notes','policy_enable_guards'):
        if field not in n:continue
        for i,text in enumerate(n[field]):
            for old,new in legacy_receipts.items():text=text.replace(old,new)
            n[field][i]=text.replace('name = "Kim Jong Il"','name = "Kim Jong-il"')
    if n['group']=='jongil':n['eligibility_notes']+=['check_variable = { ruling_party = 4 }','has_country_leader = { name = "Kim Jong-il" ruling_only = yes }']
    if n['slot'] is not None:
        partyguard='check_variable = { ruling_party = '+str(n['slot'])+' }'
        if partyguard not in n['eligibility_notes']:n['eligibility_notes'].append(partyguard)
    e=next((e for e in n['extra'] if e['kind']=='agreement'),None)
    if e:
        a=next(a for a in AGREEMENTS if a['key']==e['agreement'])
        n['eligibility_notes']+=['Recipient '+a['partner']+' exists; recheck the shared agreement predicate on completion and on recipient acceptance.']
        if e['stage']!='base':n['eligibility_notes']+=['Require the accepted base agreement to be active on BOTH tags (peace and all four sanctions in both directions).']
B['western_credit']['conditional_packages']=[dict(id=P+'machinery_credit_risk',title='Machinery Credit Exposure',
    modifiers={'interest_rate_multiplier_modifier':B['western_credit']['modifiers'].pop('interest_rate_multiplier_modifier')},
    condition='Recorded machinery principal remains outstanding.',ends='Remove this risk premium after the recorded principal is fully settled; retained industrial benefits do not disappear.')]
for a in AGREEMENTS:
    a['receipts']=dict(accepted=P+a['key']+'_accepted',initial_grant=P+a['key']+'_initial_grant_applied',
        pending=P+a['key']+'_pending',quote='Saved payer-specific setup amounts; validity checked again on acceptance.',
        rule='Accepted/upgrade/initial-grant receipts are immutable and shared on both tags. Reconciliation never repeats a setup fee, factory, slots or research grant. Pending state is cleared on accept, decline, expiry or invalidation.')
    for u in a['upgrades']:u['receipt']=P+a['key']+'_'+u['key']+'_accepted'

# Replace fixed-dollar incidents with GDP quotes / the recorded principal.
D['incidents']=[dict(id=P+'machinery_account',name='The Machinery Account',
 trigger='730 days after the saved 1.50%-of-GDP machinery loan, if recorded principal remains.',
 choices=[dict(name='Settle the Account',payment='Recorded outstanding principal, paid once; matched debt reduction.'),
          dict(name='Reschedule the Account',cost_gdp_share=.002,days=730,modifiers={'interest_rate_multiplier_modifier':1.0,'trade_opinion_factor':-.10}),
          dict(name='Suspend Repayments',cost_gdp_share=0,days=730,modifiers={'interest_rate_multiplier_modifier':2.0,'trade_opinion_factor':-.15,'stability_factor':-.03})]),
 dict(id=P+'patron_disruption',name='External Support Disrupted',trigger='A real accepted supply agreement becomes inactive through war, bilateral sanctions, or the loss of its partner.',
      agreement_keys=['soviet_industry','china_border'],transition='Active to inactive only. One non-stacking adjustment penalty; monthly maintenance never retriggers it.',
      days=365,modifiers={'industrial_capacity_factory':-.08,'research_speed_factor':-.03},mitigation_cost_gdp_share=.004,
      note='The agreement itself does not expire. Both spirits and ongoing agreement fees suspend together; restoration never repeats one-time grants.')]
D['news']=dict(date='8 July 1994',id=P+'world_news_kim_il_sung_dies',title='Kim Il Sung Has Died',
 description='Pyongyang has announced the death of Kim Il Sung at the age of 82. Kim Jong Il has assumed the leadership of North Korea, ending the founder’s forty-six years in power.',
 alternative_description='Kim Il Sung, North Korea’s former leader, has died at the age of 82. His death closes the era of the Republic’s founding generation.',
 option='The end of an era.',broadcast='One global major news event, visible to all countries.',
 succession='Install Kim Jong Il only if the incumbent Kim regime was in office immediately before the death. Alternative governments remain in office.',
 succession_guard='Record incumbent Kim Il Sung before his existing 1994.7.8 leader expiry; a one-time global receipt prevents duplicate death / succession events.',
 formal_titles='National leader from July 1994; not automatically President or WPK General Secretary in 1994.',
    native_leader_name='Kim Jong-il',native_portrait='gfx/Leaders/NKO/Kim_Jong_il.dds',native_ideology='communist_state',
    availability_receipt=dict(id=P+'kim_jong_il_unavailable',status='Proposed country lifecycle receipt, not an existing MD API.',producer='Normally absent in the historical 1970–1994 course. Explicit RP mortality or permanent retirement of the successor must set it; family promotion and succession recheck it.'),
 image='assets/COLDWAR_NKO_1994_funeral_colorized.png',
 source_image='assets/kim_il_sung_funeral_1994_source.jpg',
 image_credit='KCNA / Korea News Service via Associated Press; July 1994 funeral procession. AI color restoration for concept review.',
 image_source='https://www.dailyherald.com/20111226/news/what-to-look-for-at-north-koreas-funeral-for-kim-jong-il/')
D['agreements']=AGREEMENTS
for spirit in D['starting_spirits']:
    if spirit['key']=='byungjin_start':spirit['title']='Economic and Defence Construction'
    if spirit['key']=='juche_start':spirit['remedy']='External Channels replaces this with strategic autonomy: +6% influence defense / −3% trade opinion. Signed cooperation provides additional technical benefits.'
D['starting_spirits'][0]['remedy']='Replaced by Monolithic Leadership or Collective Deliberation. Earned WPK policies apply while the WPK governs and return with that government.'
D['policy_lifecycle']=dict(party='Earned policies apply only under their registered governing party or institution; reconcile on government change, monthly maintenance and load. Return earned spirits without repeating one-time rewards.',
    leader='Kim-family and Kim Jong Il policies also require their respective leader conditions. Kim Jong Il succession on 8 July 1994 replaces only the incumbent Kim regime.',
    treaties='Signed bilateral agreements survive government changes. Suspend both copies and weekly fees together during mutual war or bilateral sanctions; resume without repeating setup grants.',
    resubmission='Completed offer focuses unlock sender decisions to resubmit after refusal or expiry, with fresh quotes and a new 90-day response period. Only one offer per agreement/stage may be pending.')
D['bootstrap_contract']=dict(status='Implementation after approval only.',
    scenario='Attach this tree and the six defined opening spirit packages in the guarded 1970 NKO startup. Existing 2000 add_ideas are not the 1970 starting package.',
    guards='original_tag = NKO; IMP_is_1970_scenario = yes; existing governing-party variable. The monolithic starting policy is WPK-bound; the other five opening constraints are national.',
    reconciliation='A one-time initialization receipt plus earned replacement receipts prevents duplicate startup or restoration of a removed opening constraint. Reconcile on load without rerunning buildings, cash or research grants.',
    scope='No starting OOB, troops, ships, aircraft, uranium production or built uranium mines are added.')
D['revision']='v2 — GDP costs, specific combat bonuses, equal state slots, recipient decisions, war route and 1994 succession'
D['status']='CONCEPT — awaiting approval; no game code installed'
D['stats_labels']=LABELS
D['state_names']=STATE_NAMES;D['country_names']=COUNTRY_NAMES
D['budget_contract']=dict(one_off='Current payer gdp_total × chosen share; no fixed-dollar floor.',
 quote='Save both countries’ GDP-based setup quotes when the offer is sent; charge exactly those saved amounts only on recipient acceptance.',
 weekly='Current payer GDP × annual commitment ÷ 52. Aggregate once in the native weekly expense system only while the paired agreement is active.',
 borrowing='Normal MD weekly automatic borrowing remains available; no added current-cash gate.',
 slots='Every building level grants the same number of extra shared slots in the same owned and controlled state; enforce non-slot caps and placement rules.')

def percentage(v):return f'{v*100:.2f}%'
def statlines(m):
    def amount(v):return f'{v*100:+.2f}'.rstrip('0').rstrip('.')+'%'
    return [f"{LABELS.get(k,k)}: {v:+.2f} percentage points" if k=='interest_rate_multiplier_modifier' else f"{LABELS.get(k,k)}: {amount(v)}" for k,v in m.items()]
def player_effects(n):
    rows=[]
    if n['cost_gdp_share']:rows.append('Expenditure: '+percentage(n['cost_gdp_share'])+' of GDP')
    rows+=statlines(n['modifiers'])
    for package in n.get('conditional_packages',[]):rows+=['While the machinery account is outstanding: '+s for s in statlines(package['modifiers'])]
    for e in n['extra']:
        if e['kind']=='building':
            locations=' or '.join(STATE_NAMES[s] for s in e['state_ids'])
            rows.append(f"Add {e['levels']} {BUILDING_NAMES[e['type']]} and {e['slots']} Building Slot in {locations}")
        elif e['kind']=='research':rows.append(f"{e['bonus']:.0%} research bonus ({e['uses']} use): "+{'CAT_nuclear_reactors':'Nuclear Reactors','CAT_nuclear_weapons':'Nuclear Weapons'}.get(e['category'],e['category']))
        elif e['kind']=='agreement':
            a=next(a for a in AGREEMENTS if a['key']==e['agreement'])
            rows.append('Send a cooperation proposal to '+COUNTRY_NAMES[a['partner']])
            rows.append('Agreement: '+(a['title'] if e['stage']=='base' else next(u['title'] for u in a['upgrades'] if u['key']==e['stage'])))
        elif e['kind']=='debt':rows.extend(['Machinery credit: +1.50% of GDP in treasury and debt','Machinery procurement: −1.50% of GDP'])
        elif e['kind']=='repay_loan':rows.append('Resolve the recorded machinery account')
        elif e['kind']=='wargoal':rows.append('Gain an Annexation War Goal against South Korea')
        elif e['kind']=='policy_note':rows.append(e['text'])
        elif e['kind']=='action':
            texts={'Planning decisions':'Open the National Investment Programme','Replace Byungjin burden':'Replace Economic and Defence Construction: Core Defense +4%; Civilian Factory Construction Speed −4%','Imported-input residual':'Replace Power and Imported Inputs: Population Non-Electric Fuel Demand +6%','Strategic autonomy settlement':'Replace Juche and the Two Patrons: Foreign Influence Defense +6%; Trade Opinion −3%','Joint venture offers':'Open foreign investment proposals','Strategic programme':'Support the strategic nuclear research programme'}
            if e['name'] in texts:rows.append(texts[e['name']])
    if n['remove']:
        titles={s['key']:s['title'] for s in D['starting_spirits']}
        for key in n['remove']:
            rows.append('Remove '+titles.get(key,{'byungjin_residual':'the remaining Byungjin burden','imported_input_residual':'the imported-input constraint'}.get(key,key)))
    return rows
B['technical_exchange']['title']='Technical Exchange'
B['technical_exchange']['requirements']=['At least one East German, Bulgarian or Romanian cooperation programme is active.']
for n in N:n['effects']=player_effects(n)

def validate():
    errors=[];ids={n['id']:n for n in N}
    if len(ids)!=len(N):errors.append('duplicate ID')
    for n in N:
        for pg in n['prerequisites']:
            for p in pg:
                if p not in ids:errors.append('missing '+p)
                elif ids[p]['y']>=n['y']:errors.append('backward edge '+p+' / '+n['id'])
        for p in n['mutex']:
            if n['id'] not in ids[p]['mutex']:errors.append('asymmetric '+p)
        for e in n['extra']:
            if e['kind']=='building' and e['slots']!=e['levels']:errors.append('slot mismatch '+n['id'])
        if 'money' in n:errors.append('fixed money survived '+n['id'])
    for i,a in enumerate(N):
        for b in N[i+1:]:
            if abs(a['x']-b['x'])*96<165 and abs(a['y']-b['y'])*130<128:errors.append('overlap '+a['id']+' / '+b['id'])
    memo={}
    def history(key):
        if key in memo:return memo[key]
        node=ids[key];valid=[frozenset()]
        for pg in node['prerequisites']:
            options=[s for p in pg for s in history(p)]
            valid=list(set(a|b for a in valid for b in options if not any(set(ids[k]['mutex'])&(a|b) for k in a|b)))
        valid=[s|{key} for s in valid if not set(node['mutex'])&s];memo[key]=valid;return valid
    for n in N:
        if not history(n['id']):errors.append('unreachable '+n['id'])
    for a in AGREEMENTS:
        if not a['perpetual'] or a['party_bound']:errors.append('agreement duration/party '+a['id'])
        for b in a['buildings']:
            if b['slots']!=b['levels']:errors.append('agreement slots '+a['id'])
    components=[];visited=set()
    for n in N:
        if not n['mutex'] or n['id'] in visited:continue
        todo=[n['id']];component=set()
        while todo:
            key=todo.pop()
            if key in component:continue
            component.add(key);todo+=ids[key]['mutex']
        visited|=component;components.append(sorted(component))
    buildings=[e for n in N for e in n['extra'] if e['kind']=='building']+[e for a in AGREEMENTS for e in a['buildings']]
    for n in N:
        if round(n['cost_gdp_share'],5)!=n['cost_gdp_share']:errors.append('overprecise price '+n['id'])
        if n['anchor']:
            anchor=ids[n['anchor']]
            if (anchor['x']+n['dx'],anchor['y']+n['dy'])!=(n['x'],n['y']):errors.append('anchor mismatch '+n['id'])
    report=dict(nodes=len(N),groups=dict(Counter(n['group'] for n in N)),edges=sum(len(pg) for n in N for pg in n['prerequisites']),
      choice_groups=len(components),building_records=len(buildings),bilateral_base_agreements=len(AGREEMENTS),bilateral_upgrade_offers=sum(len(a['upgrades']) for a in AGREEMENTS),
      exclusions=sum(len(n['mutex']) for n in N)//2,bounds=[min(n['x'] for n in N),max(n['x'] for n in N),min(n['y'] for n in N),max(n['y'] for n in N)],
      errors=errors,engine_tested=False)
    assert len(N)<=250
    assert not errors,errors
    return report

def docs():
    lines=['# COLDWAR — DPRK concept, revision 2','',f"**{len(N)} focuses. Design and preview only; no loaded game files changed.**",'',
      '## Revision requested','',
      '- Every cash price is a GDP share. Normal project prices range from 0.20% to 2.00% of the payer’s current internal GDP; agreements quote each payer separately. The user’s GDP pricing instruction supersedes the earlier fixed-dollar preference.',
      '- Artillery and comparable specialist programmes use the actual relevant MD combat modifiers. Towed/self-propelled artillery use `army_artillery_attack_factor`; rocket artillery uses its separately registered battalion key. No artillery programme grants a general army attack bonus.',
      '- Every building level, including infrastructure, energy and radar, grants one additional shared building slot in the same selected state. Slots and the building are a single one-time reward. Check ownership/control, coastline and hard type/level caps before charging; missing existing shared slots are supplied by this reward.',
      '- Foreign Diplomacy adds five new country programmes (East Germany, Bulgaria, Romania, Egypt and Japan), alongside four base packages in the patron, Korean and atomic sections: nine base agreements with eight partner countries in total. All bilateral offer focuses create acceptance and refusal decisions for the recipient country; an information event may notify but never accepts the agreement.',
      '- Accepted agreements grant both countries persistent contract spirits with reciprocal benefits and burdens; the Inter-Korean package is symmetric. They do not expire or depend on a domestic governing party. All four direct sanction classes in either direction or mutual war suspend BOTH spirits and their weekly contract costs. Both resume when those conditions clear, without replaying buildings, cash or research grants.',
      '- The Korean policy fork now offers negotiated exchange, coercive pressure and armed reunification. The final military focus grants a war goal against KOR. It does not automatically declare war, annex territory, or involve other players.',
      '- Kim Il Sung dies on 8 July 1994 and one major global news event is broadcast. Kim Jong Il succeeds only the incumbent Kim regime, as explicitly confirmed by the user. Other governments remain. Existing leader expiry and the succession event share one receipt to avoid an empty leader slot or duplicate transfer.',
      '- English focus descriptions follow native MD’s short narrative style. Prices, requirements and effects are separate tooltip lines. Internal flags, state-routing and implementation notes are excluded from ordinary player text.',
      '', '## GDP accounting','',json.dumps(D['budget_contract'],indent=2),'',
      'The saved machinery loan principal is `GDP × 0.015` at completion. Book principal and cash proceeds once, then spend that same quote on the factory. Later repayment uses the saved outstanding cash amount, not a newly calculated GDP fraction. Rescheduling charges 0.20% of then-current GDP. Fees use fractions with at most five fractional digits and a separate divide-by-52 operation, never a long weekly literal.',
      '', '## Exact spatial plan','', '| Section | Root | Focuses |', '|---|---:|---:|']
    for g in G:lines.append(f"| {g['title']} | ({g['x']},{g['y']}) | {sum(n['group']==g['id'] for n in N)} |")
    lines+=['','Initial camera: WPK (6,0). Continuous focuses: reserved at (7300,3750) px beyond the full tree; engine position remains to be checked. All graph data and previews share the same resolved coordinates and grouped prerequisites.',
      '', '## Recipient decision and paired spirits','',
      'On offer, save both countries’ GDP quotes and a pending receipt on both tags for 90 days. The foreign player receives **Accept the Agreement** and **Decline the Proposal** decisions. Acceptance rechecks peace, all four sanction arrays, existence, prerequisites and any project cap, then clears pending state, pays the saved setup amounts, records a durable receipt in both countries and grants both spirits. Refusal/expiry makes no charge. Upgrade offers use the same recipient process and replace/extend the existing package rather than stacking duplicate base modifiers.',
      '', 'The same active predicate is evaluated at both endpoints: both signed receipts, both countries exist, no mutual war, no diplomatic/financial/economic/military sanctions from NKO to partner and no such sanctions from partner to NKO. Call bilateral reconciliation on acceptance, war/peace and sanctions add/remove, plus monthly/save-load backstops. An `enable` block alone is not assumed to reattach an engine-removed modifier.',
      '', 'After refusal or expiry, the sending country may resubmit through a decision unlocked by the completed offer focus. A fresh 90-day offer receives fresh quotes; no reapplication of completed-focus rewards. Pending offers are unique per agreement and stage. An accepted base or upgrade cannot be purchased twice.',
      '', '## Starting national spirits','']
    for s in D['starting_spirits']:
        lines += ['### '+s['title'],'',s['description'],'']
        lines += ['- '+STATS_LABEL+': '+f'{value*100:+.2f}'.rstrip('0').rstrip('.')+'%' for key,value in s['mods'].items() for STATS_LABEL in [D['stats'][key][1]]]
        lines += ['',s['remedy'],'']
    lines += ['## Guarded 1970 initialization','',json.dumps(D['bootstrap_contract'],indent=2,ensure_ascii=False),'',
      '## Policy lifecycle','',json.dumps(D['policy_lifecycle'],indent=2,ensure_ascii=False),'',
      '## Conditional credit and supply incidents','',json.dumps(D['incidents'],indent=2,ensure_ascii=False),'',
      '## Agreement catalogue','']
    for a in AGREEMENTS:
        lines += ['### '+a['title']+' — '+COUNTRY_NAMES[a['partner']],'',a['description'],'']
        for side,label in [('nko','North Korea'),('recipient',COUNTRY_NAMES[a['partner']])]:
            x=a[side];lines += ['**'+label+'**','',f"- Setup: {percentage(x['setup_gdp_share'])} of own quoted GDP",f"- Weekly cost: current GDP × {x['annual_commitment_gdp_share']:.5f} ÷ 52"]+['- '+s for s in statlines(x['modifiers'])]+['']
        for b in a['buildings']:lines+=['- On first acceptance: '+str(b['levels'])+' '+BUILDING_NAMES[b['type']]+' and '+str(b['slots'])+' building slot in the same NKO state ('+', '.join(STATE_NAMES[s] for s in b['state_ids'])+').']
        for u in a['upgrades']:lines+=['- Recipient-approved upgrade: '+u['title']+'; added NKO effects '+json.dumps(u['nko'])+'; added partner effects '+json.dumps(u['recipient'])+'. Base effects are included once, not duplicated.']
        lines+=['','Historical precedent: '+a['provenance'][0]+'. '+a['provenance'][1],'']
    lines+=['## Global death event and succession','',json.dumps(D['news'],indent=2,ensure_ascii=False),'',
      'The illustrative source photograph depicts the funeral procession later in July 1994, not the moment of death. The source caption identifies KCNA / Korea News Service via AP. The color treatment is an AI restoration; retain source and prompt provenance. No open-license claim is made for the press photograph.',
      '', '## Focus catalogue','']
    for g in G:
        lines+=['### '+g['title'],'']
        for n in [n for n in N if n['group']==g['id']]:
            lines += ['#### '+n['title'],'',f"`{n['id']}` · ({n['x']},{n['y']}) · {n['days']} days",'',n['description'],'']
            if n['prerequisites']:lines += ['Requires: '+' AND '.join('('+' OR '.join(B[p.removeprefix(P)]['title'] for p in pg)+')' for pg in n['prerequisites'])+'.']
            if n['mutex']:lines+=['Excludes: '+', '.join(B[p.removeprefix(P)]['title'] for p in n['mutex'])+'.']
            lines += ['- '+x for x in n['effects']]+['']
    lines+=['## Verification','',
      'Source references: parent-folder mechanics_revision_v2.md, mechanics_revision_v2_addendum.md, history_revision_v2.md and localization_layout_revision_v2.md. The v2 structural report checks all IDs, reciprocal exclusions, AND/OR histories, full card overlap, GDP pricing fields and equal slots. External browser typography and line routing approximate HOI4. This is neither installed nor engine tested. No gameplay script or game localization has been emitted for this revision.']
    (OUT/'COLDWAR_NKO_V2_REVIEW.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (OUT/'english_localization_review.json').write_text(json.dumps({n['id']:{'name':n['title'],'description':n['description']} for n in N},indent=2,ensure_ascii=False),encoding='utf-8')

def render():
    sys.path.insert(0,str(BASE))
    import render_concept as R
    R.OUT=OUT;R.NODES=N;R.GROUPS=G
    images,sources=R.art_library()
    # Preview-only thumbnail of the already generated restoration, not a creative image edit.
    im=Image.open(OUT/D['news']['image']).convert('RGB');im.thumbnail((760,520));buf=io.BytesIO();im.save(buf,format='JPEG',quality=82)
    images['news_photo']='data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode()
    game=Path(r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV')
    for name,file in [('news_background','event_news_bg.dds')]:
        im=Image.open(game/'gfx/interface'/file).convert('RGB');b=io.BytesIO();im.save(b,format='JPEG',quality=78,optimize=True)
        images[name]='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
    fragment=(OUT/'preview_v2_template.html').read_text(encoding='utf-8').replace('__DATA__',json.dumps(D,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__ART__',json.dumps(images,separators=(',',':')))
    assert len(fragment.encode('utf-8'))<1_000_000,'Inline visualization exceeds 1 MB'
    VIS.mkdir(exist_ok=True,parents=True)
    (VIS/'coldwar-nko-1970-v2.html').write_text(fragment,encoding='utf-8')
    (OUT/'COLDWAR_NKO_v2_preview.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>COLDWAR DPRK v2</title><style>body{margin:0;background:#202720}</style>'+fragment+'</html>',encoding='utf-8')
    (OUT/'preview_syntax_check.js').write_text(fragment.split('<script>',1)[1].split('</script>',1)[0],encoding='utf-8')
    R.static_images(D,images,sources)
    news=Image.open(game/'gfx/interface/event_news_bg.dds').convert('RGBA')
    photo=ImageOps.fit(Image.open(OUT/D['news']['image']).convert('RGB'),(398,152),method=Image.Resampling.LANCZOS)
    news.paste(photo,(59,91));draw=ImageDraw.Draw(news)
    title=ImageFont.truetype(r'C:\Windows\Fonts\georgiab.ttf',22)
    body=ImageFont.truetype(r'C:\Windows\Fonts\georgia.ttf',16)
    draw.text((257,260),D['news']['title'],font=title,fill=(35,35,28),anchor='mt')
    words=D['news']['description'].split();rows=[];row=''
    for word in words:
        candidate=(row+' '+word).strip()
        if draw.textlength(candidate,font=body)>450:rows.append(row);row=word
        else:row=candidate
    rows.append(row)
    for i,row in enumerate(rows):draw.text((39,295+i*24),row,font=body,fill=(35,35,28))
    draw.rectangle((80,506,448,548),fill=(57,65,49),outline=(101,108,84),width=2)
    draw.text((264,526),D['news']['option'],font=body,fill=(231,229,210),anchor='mm')
    news.save(OUT/'COLDWAR_NKO_1994_news_preview.png')
    return len(fragment.encode('utf-8'))

if __name__=='__main__':
    report=validate();D['validation']=report
    (OUT/'COLDWAR_NKO_v2_design.json').write_text(json.dumps(D,indent=2,ensure_ascii=False),encoding='utf-8')
    (OUT/'structural_validation_v2.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    docs();size=render()
    print(json.dumps(dict(**report,fragment_bytes=size),indent=2))
