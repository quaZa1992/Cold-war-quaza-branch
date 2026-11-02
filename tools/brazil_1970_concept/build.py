# IMPERIA COLD WAR — Isolated Brazil concept exporter and native-art renderer.
from pathlib import Path
import base64, hashlib, io, json, re, sys
from PIL import Image, ImageDraw, ImageFont
sys.dont_write_bytecode=True
import content as c

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/brazil_1970_concept'
VIZ=Path('C:/Users/sonyz/.codex/visualizations/2026/11/01/01a19886-0ea3-7cc3-b268-58354206f55f')
MD=Path('C:/Program Files (x86)/Steam/steamapps/workshop/content/394360/3374271790')
GAME=Path('C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV')
OUT.mkdir(parents=True,exist_ok=True)
ART=OUT/'art';ART.mkdir(exist_ok=True)

LABELS={
'political_power_factor':'Political Power Gain','stability_factor':'Stability',
'bureaucracy_cost_multiplier_modifier':'Bureaucracy Cost','research_speed_factor':'Research Speed',
'production_speed_buildings_factor':'Construction Speed','industrial_capacity_factory':'Factory Output',
'industrial_capacity_dockyard':'Dockyard Output','consumer_goods_factor':'Consumer Goods Factories',
'interest_rate_multiplier_modifier':'Interest Rate','social_cost_multiplier_modifier':'Social Spending Cost',
'education_cost_multiplier_modifier':'Education Cost','literacy_rate_education_modifier':'Education Literacy Growth',
'agricolture_productivity_modifier':'Agricultural Productivity','foreign_influence_modifier':'Foreign Influence Strength',
'foreign_influence_defense_modifier':'Foreign Influence Defence','equipment_cost_multiplier_modifier':'Equipment Cost',
'production_factory_efficiency_gain_factor':'Production Efficiency Growth',
'production_factory_max_efficiency_factor':'Production Efficiency Cap','country_productivity_growth_modifier':'Productivity Growth',
'corporate_tax_income_multiplier_modifier':'Corporate Tax Income','inflation_gain_multiplier_modifier':'Inflation Growth',
'inflation_cost_multiplier_modifier':'Inflation Cost','resource_export_multiplier_modifier':'Resource Export Income',
'steel_export_multiplier_modifier':'Steel Export Income','fuel_gain_factor':'Fuel Gain',
'army_org_factor':'Army Organisation','navy_org_factor':'Naval Organisation',
'army_infantry_attack_factor':'Infantry Attack','army_personnel_cost_multiplier_modifier':'Army Personnel Cost',
'navy_personnel_cost_multiplier_modifier':'Navy Personnel Cost','airforce_personnel_cost_multiplier_modifier':'Air Force Personnel Cost',
'military_spending_cost_multiplier_modifier':'Military Spending Cost','air_mission_efficiency':'Air Mission Efficiency',
'air_accidents_factor':'Air Accident Chance','production_speed_nuclear_reactor_factor':'Nuclear Reactor Construction Speed'}
BUILDINGS={'industrial_complex':'Civilian Factory','arms_factory':'Military Factory','offices':'Office','infrastructure':'Infrastructure','agriculture_district':'Agriculture District','renewable_energy_infra':'Renewable Energy Infrastructure','synthetic_refinery':'Synthetic Refinery','nuclear_reactor':'Nuclear Reactor','fuel_silo':'Fuel Silo','air_base':'Air Base','dockyard':'Naval Dockyard'}
CAT={'CAT_industry':'Industrial','CAT_electronics':'Electronics','CAT_agriculture':'Agricultural','CAT_aircraft':'Aircraft','CAT_energy':'Energy','CAT_energy_efficiency':'Energy Efficiency','CAT_nuclear_reactors':'Civil Nuclear','CAT_excavation':'Excavation'}

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def dumps(o):return json.dumps(o,ensure_ascii=False,indent=2)
def write(name,text):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def effects_text(effects):
    rows=[]
    for e in effects:
        k=e['kind']
        if k=='modifier':
            v=e['value'];number=f'{v:+g} percentage points' if e['key']=='interest_rate_multiplier_modifier' else f'{v*100:+g}%'
            rows.append(LABELS[e['key']]+': '+number)
        elif k=='treasury_gdp':rows.append(f'Treasury: {e["percent"]:+g}% of payer current GDP, once')
        elif k=='weekly_gdp_expense':rows.append(f'Weekly programme expense: {e["annual_gdp_percent"]:g}% of payer current annual GDP / 52')
        elif k=='building':rows += [f'{c.STATES[e["state"]]}: +{e["slots"]} shared building slots',f'{c.STATES[e["state"]]}: '+('Start construction: ' if not e.get('instant',True) else '')+f'+{e["amount"]} {BUILDINGS[e["building"]]}']
        elif k=='weekly_transfer':rows.append(f'Weekly {e["direction"]}: {e["annual_gdp_percent"]:g}% of {e["source"]} current GDP / 52, paid to {e["target"]}')
        elif k=='research':rows.append(f'{e["uses"]} x {e["bonus"]*100:g}% {CAT[e["category"]]} research bonus')
        elif k=='experience':rows.append(f'{e["service"].title()} experience: +{e["amount"]}')
        elif k=='faction_opinion':rows.append(f'If {e["faction"].replace("_"," ").title()} are active: Opinion {e["value"]:+g}')
        elif k=='remove_spirit':
            s=next(s for s in c.START if s['id']==e['spirit']);rows.append('Remove '+s['title'])
            rows += ['  '+s for s in effects_text([dict(v,value=-v['value']) for v in s['effects']])]
        elif k in ('unlock_decision','event','suspend_agreement'):rows.append(e['label'])
        else:raise ValueError(e)
    return rows

# Native sprites are unchanged; only proportionate decoding for an external preview.
reg={}
for root in (GAME,MD,ROOT):
    for file in sorted((root/'interface').glob('*.gfx')):
        txt=file.read_text(encoding='utf-8-sig',errors='replace')
        for m in re.finditer(r'(?i)spriteType\s*=\s*\{([^{}]*)\}',txt,re.S):
            name=re.search(r'\bname\s*=\s*"([^"]+)"',m[1]);tex=re.search(r'(?i)\btexturefile\s*=\s*"([^"]+)"',m[1])
            if name and tex:reg[name[1]]=(tex[1].replace('\\','/'),file)
icons={'military':'brazilian_armed_forces','arena':'BRA_federalism','mdb':'BRA_mdb','ptb':'BRA_brazsocdem','ptb_late':'BRA_brazsocdem','pdt':'BRA_brazsocdem','pt':'workers_party','pfl':'BRA_federalism','psdb':'BRA_brazneolib','pcb':'democratic_socialism','pcdob':'land_reform','populist':'anti_establishment','prn':'anti_establishment','society':'BRA_federalism','economy':'BRA_economic_growth','energy':'nuclear_energy','defence':'brazilian_armed_forces','diplomacy':'BRA_Itamaraty'}
# Semantically specific existing MD motifs replace party logos where the historical logo is absent.
fallback={'BRA_federalism':'BRA_mdb','BRA_brazneolib':'BRA_economic_growth','democratic_socialism':'land_reform','nuclear_energy':'BRA_economic_growth'}
for k,v in list(icons.items()):
    if v not in reg:icons[k]=fallback.get(v,'BRA_economic_growth')
specific={'science':'brain_power','farm':'agriculture','build':'construction','air':'brazil_airforce','navy':'brazil_navy','arms':'industry_military','grid':'national_grid','land':'land_reform','oil':'BRA_petrobras_oil_benefits','environment':'BRA_protect_the_amazon','social':'BRA_public_housing_programs','law':'BRA_labor_laws','tax':'BRA_simplify_the_tax_system'}
assert all(v in reg for v in specific.values())
REQUIREMENTS={'military':'Brazilian Armed Forces','arena':'National Renewal Alliance','mdb':'Brazilian Democratic Movement','ptb':'Brazilian Labour Party (restored)','ptb_late':'Brazilian Labour Party','pdt':'Democratic Labour Party','pt':'Workers Party','pfl':'Liberal Front Party','psdb':'Brazilian Social Democracy Party','pcb':'Brazilian Communist Party','pcdob':'Communist Party of Brazil','populist':'Lacerdists','prn':'National Reconstruction Party'}
for g in c.GROUPS:
    if g['slot'] is not None:g['requirement_name']=REQUIREMENTS[g['id']];g['current_native_party_localisation']='MDCW_HP_BRA_'+str(g['slot'])+'_0' if g['id'] in ('military','arena','mdb','ptb','pcb','pcdob','populist') else 'Proposed identity registration required'
for n in c.NODES:
    n['icon']=icons[n['group']]
    if n['key'].endswith('_0'):continue
    text=(n['key']+' '+n['title']).lower();effects=n['effects']+ (n['offer']['brazil']['effects'] if 'offer' in n else [])
    if re.search(r'school|education|literacy|research|technical|science|telecom|institute|teachers|nuclear|reactor',text):n['icon']=specific['science'] if not re.search('nuclear|reactor',text) else 'nuclear_energy'
    elif re.search('farm|agro|agronomy|agric|cerrado|cooperativ|peasant|land title',text):n['icon']=specific['farm']
    elif re.search('frontier|amazon|territor',text):n['icon']=specific['environment']
    elif re.search('naval|navy|fleet|escort|ocean',text):n['icon']=specific['navy']
    elif re.search('air|flight|flying|embraer|mirage',text):n['icon']=specific['air']
    elif re.search('arms|procurement|workshop|rocket|engineer',text):n['icon']=specific['arms']
    elif re.search('oil|fuel|petrobras|refin',text):n['icon']=specific['oil']
    elif re.search('power|grid|hydro|energy|itaipu',text):n['icon']=specific['grid']
    elif re.search('wage|worker|union|labour|labor|workplace',text):n['icon']=specific['law']
    elif re.search('health|social|service|municipal|urban|neighbour',text):n['icon']=specific['social']
    elif re.search('tax|treasury|fiscal|budget|audit|account',text):n['icon']=specific['tax']
    elif any(e['kind']=='building' for e in effects):n['icon']=specific['build']
assets={};provenance=[]
for sprite in {n['icon'] for n in c.NODES}|{'GFX_focus_unavailable','GFX_focus_can_start'}:
    assert sprite in reg,sprite
    rel,provider=reg[sprite];source=next((p/rel for p in (ROOT,MD,GAME) if (p/rel).is_file()),None)
    assert source,(sprite,rel)
    im=Image.open(source).convert('RGBA');bio=io.BytesIO();im.save(bio,format='PNG',optimize=True)
    (ART/(sprite+'.png')).write_bytes(bio.getvalue())
    assets[sprite]='data:image/png;base64,'+base64.b64encode(bio.getvalue()).decode()
    provenance.append(dict(sprite=sprite,source=str(source),provider=str(provider),sha256=digest(source),source_size=list(im.size),original_author='Millennium Dawn / upstream asset authors; individual artist unknown',licence='Applicable upstream Millennium Dawn and Paradox terms; separate permission unknown',modifications='Decoded to PNG for local approval preview, proportionately displayed; source untouched'))
for n in c.NODES:
    asset_sets=[dict(scope='BRA',effects=n['effects'])]
    if 'offer' in n:asset_sets += [dict(scope='BRA',effects=n['offer']['brazil']['effects']),dict(scope=n['offer']['partner'],effects=n['offer']['recipient']['effects'])]
    n['execution_contract']=dict(hidden=['BRA country scope','1970 scenario routing','One-time receipt for this focus or agreement'],party=dict(native_trigger=c.TRIGGERS[next(g for g in c.GROUPS if g['id']==n['group'])['slot']],exact_identity=next(g for g in c.GROUPS if g['id']==n['group'])['identity']) if next(g for g in c.GROUPS if g['id']==n['group'])['slot'] is not None else None,buildings=[dict(scope=s['scope'],state=e['state'],checks=['Owns state','Fully controls state','Native building type capacity','Shared capacity after the extra slot grant'],transaction_order=['Mark one-time receipt only after all acceptance checks','Debit setup once','Grant shared slots','Add building construction']) for s in asset_sets for e in s['effects'] if e['kind']=='building'],preview='Prospective effect display only; no awards, payments or flags.')
for event in c.EVENTS:
    event['lifetime']='government' if event['id'].endswith('officer_council') else 'national' if event['id'].endswith(('constitution','party_reform','party_split')) else '365 days'
    for i,o in enumerate(event['options']):o['spirit_name']=event['title']+': '+o['title'];o['exclusive_options']=True

D=dict(project='IMPERIA COLD WAR',country='BRA',revision='Brazil 1970 concept 1.1',status='UNAPPROVED CONCEPT. No tree, national spirit, party, event or localisation is installed.',scenario='1970-01-01',historical_leader='Emilio Garrastazu Medici',starting_government=22,groups=sorted(c.GROUPS,key=lambda g:(g['y'],g['x'])),nodes=c.NODES,starting_spirits=c.START,decisions=c.DECISIONS,events=c.EVENTS,labels=LABELS,building_labels=BUILDINGS,category_labels=CAT,state_names=c.STATES,navigation=dict(initial_government='military',initial_focus='military_0',preview_section='military',initial_show_position=[4,0],shortcuts=[dict(name=label,focus=next(n['id'] for n in c.NODES if n['group']==key)) for key,label in [('military','State and Conservatives'),('pdt','Labour and Liberals'),('pcb','Communists and Populists'),('society','Institutions and Society'),('economy','Industry and Agriculture'),('energy','Energy and Resources'),('defence','Armed Services'),('diplomacy','Itamaraty')]],continuous_focus_position=dict(x=0,y=2500)),geometry=dict(stride=[96,130],card=[165,128],native_title=[147,20],source='Current native GUI plus prior measured MD preview profile; external icon and connector reconstruction',extent=[min(n['x'] for n in c.NODES),max(n['x'] for n in c.NODES),min(n['y'] for n in c.NODES),max(n['y'] for n in c.NODES)]),party_integration=dict(status='Proposed, requires approval and later registry integration',preserve='All existing 24 slot identities, starting Medici, leader succession and election systems.',later='PDS and PMDB continuations; separate historic PTB/later PTB/PDT/PT, PFL, PSDB and PRN identities must be registered through the existing party system. Same outlook alone never enables all programmes.',early='Plural Party Law permits plausible early alternate organisations; historical branding appears through genuine formation events. No blanket year barrier.',gates='Native ruling-party trigger AND exact active identity; availability and payout both checked. No allow_branch hiding.'),lifecycle=dict(government='Earned policy modifiers and weekly programme appropriations active only for the actual governing identity. Reapply on its return without replaying assets, research or setup money. Durable national reforms and assets stay.',agreements='No expiry. Both exist, no bilateral war, no native embargo and none of four mirrored sanction classes. Suspend/restore both spirits and budgets together; never repeat finite rewards.',parent='Every dependent offer needs actual active parent agreement in availability and reward execution. Parent suspension suspends children.',finance='Setup at execution/acceptance from payer own current gdp_total. Weekly expenses reprice at own current GDP share / 52. No additional treasury availability gate; native borrowing retained.'),verification_limits=['Not implemented or tested in HOI4.','Native art reused, Arial label metrics and external connector reconstruction are approximations.','Later party identities need a separately approved native-registry integration.','Historical policy sources justify direction; modifier magnitudes are gameplay proposals.'])
write('concept.json',dumps(D))
write('ART_PROVENANCE.json',dumps(dict(project='IMPERIA COLD WAR',assets=provenance)))
write('art/NOTICE.md','IMPERIA COLD WAR\n\nLocal concept preview assets, decoded unchanged from the installed Millennium Dawn/native assets. Individual artists and separate redistribution permissions are unknown unless recorded in ART_PROVENANCE.json. All upstream rights remain. Party motifs may be visual proxies, not authenticated 1970 logos. Native sources are unmodified. The project marker establishes no ownership or licence.\n')

# Structural checks deliberately do not claim engine validation.
by={n['key']:n for n in c.NODES};assert len(by)==len(c.NODES)
issues=[]
for n in c.NODES:
    for block in n['prerequisites']:
        for k in block:
            if k not in by:issues.append('Missing prerequisite '+k)
            elif by[k]['y']>=n['y']:issues.append('Non-forward prerequisite '+n['key']+' '+k)
    for k in n['exclusions']:
        if n['key'] not in by[k]['exclusions']:issues.append('Asymmetric exclusion '+n['key'])
    if n['anchor']:
        a=next(a for a in c.NODES if a['id']==n['anchor'])
        assert [a['x']+n['offset'][0],a['y']+n['offset'][1]]==[n['x'],n['y']]
    sets=[n['effects']]+([n['offer']['brazil']['effects'],n['offer']['recipient']['effects']] if 'offer' in n else [])
    for effects in sets:
        for e in effects:
            if e['kind']=='building':assert e['slots']==e['amount']>0
            if e['kind']=='modifier':assert e['key'] in LABELS
            if e['kind']=='research':assert e['category'] in CAT
            if e['kind']=='weekly_gdp_expense':assert e['divisor']==52
            if e['kind']=='weekly_transfer':assert e['source']=='BRA' and e['target']=='PAR' and e['direction'] in ('expense','income') and e['annual_gdp_percent']==.08
            if e['kind']=='faction_opinion':assert e['if_idea']==e['faction'] and e['faction']!='farmers'
    if 'offer' in n and n['effects']:issues.append('Offer pays before acceptance '+n['key'])
    if 'offer' in n:
        transfers=[(s,e) for s in ('brazil','recipient') for e in n['offer'][s]['effects'] if e['kind']=='weekly_transfer']
        if transfers:
            assert len(transfers)==2
            assert transfers[0][0]=='brazil' and transfers[0][1]['direction']=='expense'
            assert transfers[1][0]=='recipient' and transfers[1][1]['direction']=='income'
            assert all(transfers[0][1][k]==transfers[1][1][k] for k in ('source','target','annual_gdp_percent'))
for i,a in enumerate(c.NODES):
    for b in c.NODES[i+1:]:
        if abs(a['x']-b['x'])*96<165 and abs(a['y']-b['y'])*130<128:issues.append('Card collision '+a['key']+' '+b['key'])
assert not issues,issues
report=dict(project='IMPERIA COLD WAR',kind='Concept static checks, no loaded output or engine test',focuses=len(c.NODES),groups=len(c.GROUPS),exclusive_pairs=sum(len(n['exclusions']) for n in c.NODES)//2,offers=sum('offer' in n for n in c.NODES),starting_spirits=len(c.START),events=len(c.EVENTS),card_collisions=0,missing_references=0,anchor_mismatches=0,concept_sha256=digest(OUT/'concept.json'),errors=issues)
write('STATIC_CHECKS.json',dumps(report))

catalog=['IMPERIA COLD WAR','','# Brazil: complete proposed focus catalogue','',D['status'],'','All player-facing text is English. Coordinates are resolved grid units. Separate prerequisite groups are AND; alternatives inside one group are OR. Every reward magnitude is a balance proposal.','']
for g in c.GROUPS:
    catalog += ['## '+g['title'],'',g['context'],'']
    for n in [n for n in c.NODES if n['group']==g['id']]:
        catalog += ['### '+n['title'],'',f'`{n["id"]}` | ({n["x"]}, {n["y"]}) | {n["days"]} days | {n["lifetime"]}','',n['description'],'','Requirements: '+('; '.join(n['conditions']) or 'Shared national programme'), 'Prerequisites: '+(' AND '.join('('+' OR '.join(by[k]['title'] for k in block)+')' for block in n['prerequisites']) or 'None'),'Mutually exclusive: '+('; '.join(by[k]['title'] for k in n['exclusions']) or 'None'),'','Effects:','']
        catalog += ['* '+s for s in effects_text(n['effects'])] or ['* No direct payout. Recipient offer only.']
        if 'offer' in n:
            catalog+=['','If they accept:','']
            for side in ('brazil','recipient'):
                s=n['offer'][side];catalog+=['**'+s['name']+'**','']+['* '+v for v in effects_text(s['effects'])]+['']
        catalog+=['']
catalog+=['# Event options','']
for e in c.EVENTS:
    catalog+=['## '+e['title'],'',e['description'],'','Policy duration: '+e['lifetime'],'']
    for o in e['options']:catalog+=['### '+o['title'],'']+['* '+s for s in effects_text(o['effects'])]+['']
write('FOCUS_CATALOGUE.md','\n'.join(catalog))

template=(Path(__file__).parent/'preview_template.html').read_text(encoding='utf-8')
fragment=template.replace('__DESIGN__',json.dumps(D,ensure_ascii=False,separators=(',',':'))).replace('__ART__',json.dumps(assets,separators=(',',':')))
assert len(fragment.encode())<1024*1024,len(fragment.encode())
VIZ.mkdir(parents=True,exist_ok=True)
(VIZ/'brazil-cold-war.html').write_text(fragment,encoding='utf-8')
write('PREVIEW.html','<!doctype html>\n<!-- IMPERIA COLD WAR — Brazil external concept preview. -->\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>IMPERIA COLD WAR: Brazil</title><style>body{margin:0;background:#161b19}</style></head><body>'+fragment+'</body></html>')
print(json.dumps(dict(report,preview_bytes=len(fragment.encode())),ensure_ascii=False))
