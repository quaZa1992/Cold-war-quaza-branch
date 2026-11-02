# IMPERIA COLD WAR — isolated design exporter. Never writes loaded game directories.
"""Build the approval model, native-art preview and complete effect matrix."""
from pathlib import Path
from collections import defaultdict
from copy import deepcopy
import base64, hashlib, io, json, re, sys
from PIL import Image, ImageDraw
sys.dont_write_bytecode = True
import content as c
import native_font as font
import lifecycle as life

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'docs/design/cuba_1970_concept'
VIS = Path('C:/Users/Enes/.codex/visualizations/2026/10/23/01a16858-4604-7d63-8280-842aa85009b7')
MAIN = Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
PREFIX = c.PREFIX

# Deliberately edited native title variants, never automatic truncation.
SHORT = {
 'harvest_accounts':'Harvest Accounts','anap_cooperatives':'ANAP Cooperatives',
 'protected_enterprises':'Protected Firms','joint_ventures':'Joint Ventures',
 'teaching_hospitals':'Teaching Hospitals','far_reorganisation':'Reorganise the FAR',
 'expeditionary_forces':'Overseas Forces','territorial_defence':'Territorial Defence',
 'civil_military_pact':'Civil–Military Pact','island_diplomacy':'Island Diplomacy',
 'moscow_guarantee':'Soviet Assistance','washington_talks':'Washington Talks',
 'caribbean_neighbours':'Our Neighbours','development_protocol':'Use and Handover',
 'socialist_constitution':'The Constitution','protected_enterprises':'Protected Firms',
 'rectification':'Rectification','cuban_socialism':'Cuban Socialism',
 'unfinished_revolution':'The New Man','enterprise_accounts':'Enterprise Accounts',
 'manager_responsibility':'Managerial Duty','solidarity_profit':'Solidarity First',
 'professional_revolution':'Professional Rule','military_engineering':'Military Engineers',
 'accountable_officers':'Officer Standards','orderly_succession':'Orderly Succession',
 'veterans_directorate':'Veterans in Office','cuban_liberation':'Cuban Liberation',
 'veterans_civil_life':'Veterans into Work','compensation_bonds':'Claims and Bonds',
 'constitutional_order':'Civil Government','judicial_guarantees':'Judicial Guarantees',
 'investment_rights':'Investment Rights','independent_republic':'Independent Cuba',
 'pluralist_covenant':'Pluralist Covenant','provisional_charter':'Civilian Transition',
 'tricontinental_secretariat':'Tricontinental Office','professional_intelligence':'Intelligence Service',
}

def num(n):
    return f'{n:.5f}'.rstrip('0').rstrip('.') if isinstance(n,float) else str(n)

def pct(n):
    return f'{n*100:+.0f}%'

def uri(im,lossless=True):
    buf=io.BytesIO(); im.save(buf,format='WEBP',lossless=lossless,quality=88,method=6)
    return 'data:image/webp;base64,'+base64.b64encode(buf.getvalue()).decode()

def registry():
    result={}
    # Workspace overrides current MD; base game supplies shared titlebar/font art.
    for root in (GAME,MAIN,ROOT):
        for path in sorted((root/'interface').glob('*.gfx')):
            text=path.read_text(encoding='utf-8-sig',errors='replace')
            for m in re.finditer(r'(?:spriteType|SpriteType)\s*=\s*\{([^{}]*)\}',text,re.S):
                name=re.search(r'\bname\s*=\s*"([^"]+)"',m[1]); tex=re.search(r'\btexturefile\s*=\s*"([^"]+)"',m[1],re.I)
                if name and tex:
                    result[name[1]]=(tex[1].replace('\\','/'),str(path))
    return result

REG=registry(); ART={}
def asset(sprite,kind='focus'):
    if sprite in ART:return ART[sprite]
    assert sprite in REG, f'Unregistered {kind} sprite: {sprite}'
    rel,provider=REG[sprite]
    path=next((root/rel for root in (ROOT,MAIN,GAME) if (root/rel).is_file()),None)
    assert path, (sprite,rel)
    im=Image.open(path).convert('RGBA')
    ART[sprite]=dict(uri=uri(im,False),width=im.width,height=im.height,path=str(path),provider=provider,kind=kind,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    return ART[sprite]

def effect_text(e):
    kind=e['kind']
    if kind=='treasury':return f'Treasury {e["amount"]:+.2f} (one time)'
    if kind=='debt':return f'Debt principal {e["amount"]:+.2f}; cash is a separate effect'
    if kind=='stability':return f'Stability {e["amount"]*100:+.0f} percentage points'
    if kind=='building':return f'State {e["state"]}: +{e["level"]} {e["building"].replace("_"," ")}' + (f' · province {e["province"]}' if e.get('province') else '')
    if kind=='research':return f'{e["uses"]} × {e["bonus"]*100:.0f}% research bonus · {e["category"]}'
    if kind=='doctrine':return f'{e["uses"]} × {e["bonus"]*100:.0f}% land doctrine cost reduction'
    if kind=='experience':return ' · '.join(f'{key.title()} experience +{e[key]}' for key in ('army','navy','air') if e[key])
    if kind=='law':
        if e['helper']=='decrease_corruption':return 'Corruption −1 native tier; at tier 1: named Public Oversight (weekly bureaucracy expenditure −3%, once, non-stacking); missing tier blocks enactment'
        if e['helper']=='increase_corruption':return 'Increase corruption by one native tier'
        return ('Education' if 'education' in e['helper'] else 'Healthcare')+' budget +1 native tier; at maximum: named service efficiency (weekly sector expenditure −3%); missing tier blocks enactment'
    if kind=='offer':return 'Propose '+c.CONTRACTS[e['contract']]['title']+'; acceptance is a separate decision'
    if kind=='relations':return 'Opinion '+str(e['value'])+' · '+', '.join(e['targets'])
    if kind=='harvest_course':return 'Record harvest course: '+e['course']+'; campaign modifiers expire with the July 1970 harvest settlement'
    if kind=='enterprise_reform':return 'Replace The Revolutionary Offensive; retain national assets across later governments'
    if kind=='rename_island':return 'State 1252 → '+e['name']+'; ownership remains CUB'
    if kind=='contract_followup':return 'Publish ratified island use protocol; compensation and research are NOT paid a second time'
    if kind=='transition_charter':return 'Enact a 365-day civilian transition charter; oversight: Stability +3 points, Political power gain −5%; expiry opens a civilian governing settlement'
    raise AssertionError(e)

def modrows(modifiers):
    return [dict(key=k,label=c.LABELS[k],value=v,text=(f'{v:+.0f}' if k=='send_volunteer_size' else pct(v)),good=(v<0 if k in c.BAD_HIGH else v>0)) for k,v in modifiers.items()]

def guard(n):
    rows=[]
    if n['slot'] is not None:rows.append(f'check_variable = {{ ruling_party = {n["slot"]} }}')
    for e in n['effects']:
        if e['kind']=='building':
            s=e['state'];b=e['building'];v=e.get('province')
            rows += [f'owns_state = {s}',f'controls_state = {s}']
            rows.append(f'{s} = {{ free_building_slots = {{ building = {b} size > 0 include_locked = no'+(f' province = {v}' if v else '')+' } }')
        if e['kind']=='law' and e['helper'] in ('increase_education_budget','increase_healthcare_budget'):
            p,maxi=('edu',5) if 'education' in e['helper'] else ('health',6)
            rows.append('OR = { '+' '.join(f'has_idea = {p}_{i:02d}' for i in range(1,maxi+1))+' }')
        if e['kind']=='law' and e['helper']=='decrease_corruption':rows.append('OR = { '+' '.join(f'has_idea = corruption_level_{i:02d}' for i in range(1,11))+' }')
    k=n['key']
    target='SOV' if k in ('moscow_guarantee','cmea_application','air_defence') else 'USA' if k=='washington_talks' else 'DDR' if k in ('berlin_havana','thaelmann_name','caribbean_treaty','playa_rda') else None
    if target:rows += [f'country_exists = {target}',f'NOT = {{ has_war_with = {target} }}']
    if k=='division_labour':rows.append('has_idea = COLDWAR_CUB_cmea_member')
    if k in ('berlin_havana','thaelmann_name','caribbean_treaty','playa_rda'):rows+=['owns_state = 1252','controls_state = 1252']
    if k in ('thaelmann_name','caribbean_treaty'):rows.append('date > 1972.6.18')
    if k=='development_protocol':rows+=['has_country_flag = COLDWAR_CUB_island_cession_ratified','DDR = { owns_state = 1252 }']
    return list(dict.fromkeys(rows))

def direct_code(e,node):
    k=e['kind']; eid=node['id']
    if k=='treasury':return f'set_temp_variable = {{ treasury_change = {num(e["amount"])} }}\nmodify_treasury_effect = yes'
    if k=='debt':return f'set_temp_variable = {{ debt_change = {num(e["amount"])} }}\nmodify_debt_effect = yes'
    if k=='stability':return 'add_stability = '+num(e['amount'])
    if k=='building':return f'{e["state"]} = {{ add_building_construction = {{ type = {e["building"]} level = 1 instant_build = yes'+(f' province = {e["province"]}' if e.get('province') else '')+' } }'
    if k=='research':return f'add_tech_bonus = {{ name = {eid}_research bonus = {num(e["bonus"])} uses = {e["uses"]} category = {e["category"]} }}'
    if k=='doctrine':return f'add_doctrine_cost_reduction = {{ name = {eid}_doctrine cost_reduction = {num(e["bonus"])} uses = {e["uses"]} category = land_doctrine }}'
    if k=='experience':return '\n'.join(f'{x}_experience = {num(e[x])}' for x in ('army','navy','air') if e[x])
    if k=='law':
        helper=e['helper']
        if helper=='decrease_corruption':
            return ('if = {\n limit = { OR = { '+' '.join(f'has_idea = corruption_level_{i:02d}' for i in range(2,11))+' } }\n decrease_corruption = yes\n}\nelse_if = {\n limit = { has_idea = corruption_level_01 }\n add_ideas = COLDWAR_CUB_oversight_efficiency\n}\nelse = { set_country_flag = COLDWAR_CUB_corruption_initialization_pending }')
        if helper not in ('increase_education_budget','increase_healthcare_budget'):return helper+' = yes'
        p,maxi,sector=('edu',5,'education') if 'education' in helper else ('health',6,'health')
        return ('if = {\n limit = { OR = { '+' '.join(f'has_idea = {p}_{i:02d}' for i in range(1,maxi))+' } }\n '+helper+' = yes\n}\nelse_if = {\n limit = { has_idea = '+p+f'_{maxi:02d}'+' }\n add_ideas = COLDWAR_CUB_'+sector+'_efficiency\n}\nelse = { set_country_flag = COLDWAR_CUB_'+sector+'_budget_initialization_pending }')
    # Custom contracts are intentionally named requirements, not fictitious stock effects.
    if k=='offer':return '# NEW CUSTOM CONTRACT — recipient-owned offer, not a stock MD effect:\n# COLDWAR_CUB_offer_'+e['contract']+' = yes'
    if k=='relations':return '\n'.join(f'{t} = {{ add_opinion_modifier = {{ target = ROOT modifier = COLDWAR_CUB_opinion_{e["value"]} }} }}' for t in e['targets'])
    if k=='rename_island':return '1252 = { set_state_name = COLDWAR_CUB_ernst_thaelmann_island }'
    return '# NEW CUSTOM CONTRACT — '+effect_text(e)

def native_block(n):
    rows=['# COLDWAR_CUB — IMPERIA CW: REVIEW EXCERPT; incomplete custom contracts are commented.', 'focus = {',f' id = {n["id"]}',f' icon = {n["icon"]}']
    if n['anchor']:rows.append(' relative_position_id = '+n['anchor'])
    x,y=n['local_xy'] if n['anchor'] else n['xy']
    rows += [f' x = {x}',f' y = {y}',f' cost = {n["cost"]}',' cancel_if_invalid = yes']
    rows += [' prerequisite = { '+' '.join('focus = '+p for p in ps)+' }' for ps in n['prerequisites']]
    if n['mutually_exclusive']:rows.append(' mutually_exclusive = { '+' '.join('focus = '+p for p in n['mutually_exclusive'])+' }')
    rows += [' available = {','  hidden_trigger = {']
    visible=[]
    for g in n['guards']:
        if g=='has_idea = COLDWAR_CUB_cmea_member' or g.startswith(('owns_state','controls_state','NOT = { has_war_with')) or 'free_building_slots' in g:visible.append(g)
        else:rows.append('   '+g)
    rows+=['  }']
    rows+=['  '+g for g in visible]
    rows += [' }',' completion_reward = {','  if = {','   limit = { '+' '.join(n['guards'])+' }']
    for e in n['effects']:rows+=['   '+line for line in direct_code(e,n).splitlines()]
    if n['modifiers']:rows.append('   # Set completion receipt; refresh the named national/party programme with the deltas listed below.')
    for k,v in n['modifiers'].items():rows.append(f'   # {k} = {num(v)}')
    rows+=['  }',' }','}']
    return '\n'.join(rows)

def enrich():
    nodes=deepcopy(c.NODES); groups=deepcopy(c.GROUPS)
    by={n['id']:n for n in nodes}
    for g in groups:
        g['nodes']=[n['id'] for n in nodes if n['group']==g['id']]
        for i,nid in enumerate(g['nodes']):by[nid]['anchor']=g['nodes'][0] if i else None
    # Artwork checked as pixels on ART_CONTACT_SHEET.png. Avoid modern EU/Russian
    # tricolour agreement art in Cold War diplomacy; retain actual registered sprites.
    icons={
      'harvest_accounts':'cuban_economy_peso_new','finish_zafra':'sugartobaccocuba','restore_sectors':'transporttr',
      'anap_cooperatives':'cubaterreforms','protected_enterprises':'cubanewpoliticseco','joint_ventures':'cubaconract',
      'havana_ports':'transporttr','oil_reserve':'CUB_mining','social_promise':'education_reform',
      'rural_clinics':'education_reform','teaching_hospitals':'free_higher_education','health_workforce':'mobilizeyoungpeoplecub',
      'medical_brigades':'cubtieslatinamerica','retain_doctors':'education_reform','science_schools':'free_higher_education',
      'territorial_defence':'cubaterdef','expeditionary_forces':'cubacooparmyn','militia_logistics':'cubadrills',
      'mission_schools':'cubaprof','coastal_patrols':'Cuban_Revolutionary_Navy_1','civil_military_pact':'army_planning',
      'island_diplomacy':'cubanationalists','moscow_guarantee':'align_to_soviet_union','havana_voice':'cubtieslatinamerica',
      'cmea_application':'dealswithcommunistscuba','division_labour':'cubanewpoliticseco',
      'caribbean_neighbours':'cubinvitejamaica','african_mandate':'cubacooparmyn',
      'berlin_havana':'anti_fascism','thaelmann_name':'anti_fascism','caribbean_treaty':'legislation',
      'playa_rda':'education_reform','development_protocol':'cubaconract',
      'party_ministries':'cubabattleofidea','juceplan_mandate':'cubanewpoliticseco','first_congress':'cubabattleofidea',
      'sdpe_continuity':'cubanewpoliticseco','rectification':'mobilizeyoungpeoplecub','cuban_socialism':'education_reform',
      'family_code':'legislation','family_doctor_teams':'generic_healthcare','biological_front':'science',
      'peasant_markets':'cubaterreforms','revive_microbrigades':'infra_habanna',
      'old_party':'dealswithcommunistscuba','five_year_balances':'sugartobaccocuba','enterprise_accounts':'cubanewpoliticseco',
      'cadre_schools':'education_reform','manager_responsibility':'cubaconract','soviet_standards':'align_to_soviet_union',
      'planned_republic':'cubabattleofidea','moral_incentives':'mobilizeyoungpeoplecub','workers_assemblies':'cubanewpoliticseco',
      'young_brigades':'CUB_youtharmy','factory_councils':'cubaconract','solidarity_profit':'cubacooparmyn',
      'barracks_workshops':'CUB_reborning','soldiers_not_managers':'cubaprof','military_engineering':'transporttr',
      'command_college':'army_planning','accountable_officers':'stability','orderly_succession':'legislation',
      'authentic_republic':'revivalofrpcub','labour_guarantee':'mobilizeyoungpeoplecub','investment_rights':'cubaconract',
      'mixed_economy':'cubanewpoliticseco','shame_money':'stability','independent_republic':'cubanationalists',
      'social_republic':'education_reform','public_accounts':'stability','land_labour':'cubaterreforms',
      'civic_reconciliation':'revivalofrpcub','subsidiarity':'cubanewpoliticseco','social_market':'cubaconract',
      'parish_municipality':'education_reform','family_wages':'mobilizeyoungpeoplecub',
      'courts_factions':'stability','compensation_bonds':'legislation','restitution':'cubaconract',
      'judicial_guarantees':'stability','commercial_courts':'cubaconract','open_press':'crushcensourcuba',
      'cuban_liberation':'cubanationalists','civic_resistance':'revivalofrpcub','veterans_directorate':'risemilitarismcub',
      'veterans_civil_life':'demilitarizationcuba','armed_sovereignty':'cubaterdef',
      'tricontinental_secretariat':'cubtieslatinamerica','professional_intelligence':'cub_spy_agency',
    }
    for n in nodes:
        n['icon']=icons.get(n['key'],n['icon'])
        if n['key']=='exile_directorate':n['icon']='revivalofrpcub'
        n['native_title']=SHORT.get(n['key'],n['title'])
        n['title_width']=font.width(n['native_title'])
        n['modrows']=modrows(n['modifiers']);n['effect_rows']=[effect_text(e) for e in n['effects']]
        if n['key']=='finish_zafra':n['lifetime']='Temporary harvest programme; all listed programme modifiers expire on 26 July 1970'
        if n['key'] in ('food_first','light_industry'):n['effect_rows'].append('Reduce the Sugar and Soviet Oil dependency to the exact variant in Integration & Balance')
        if n['key'] in ('socialist_constitution','accountable_officers','professional_intelligence'):
            n['effect_rows'].append('Professional Security replaces Committees of Defence: counterintelligence +10%, political power gain −4%, research −2% (one national institution)')
        if n['key'] in ('authentic_settlement','promise_1940','pluralist_covenant','constitutional_order','provisional_charter','veterans_civil_life'):
            n['effect_rows'].append('Civilian Security replaces the earlier security institution: counterintelligence +5%, weekly bureaucracy expenditure +3% (one national institution)')
        n['guards']=guard(n);n['script']=native_block(n)
        asset(n['icon'])
        n['title_art']=uri(font.raster(n['native_title']))
    spirits=deepcopy(c.STARTING_SPIRITS)
    for s in spirits:
        if s['id'].endswith('social_achievements'):s['picture']='health_care'
        asset('GFX_idea_'+s['picture'],'idea');s['modrows']=modrows(s['modifiers'])
    return dict(prefix=PREFIX,version='Approval concept · 23 October 2026',nodes=nodes,groups=groups,starting_spirits=spirits,art={k:v['uri'] for k,v in ART.items()},contracts=c.CONTRACTS,chronology=sorted(getattr(c,'CHRONOLOGY',[]),key=lambda e:e['date']),setup=life.SETUP,lifecycles=life.LIFECYCLES,rules=c.RULES,labels=c.LABELS,grid=dict(x=96,y=130,card=[165,128],title=[147,20]),baseline=dict(leader='Fidel Castro',party='PCC',slot=4,date='1 January 1970',education='Proposed: edu_02',healthcare='Proposed: health_02'))

def validate(model):
    errors=[]; nodes=model['nodes'];by={n['id']:n for n in nodes}
    if len(nodes)>120:errors.append('Focus cap exceeded')
    if len(by)!=len(nodes):errors.append('Duplicate IDs')
    for n in nodes:
        code=re.sub(r'#.*','',n['script'])
        if code.count('{')!=code.count('}'):errors.append('Unbalanced review excerpt '+n['key'])
        if n['title_width']>143:errors.append('Native title overflow '+n['key'])
        for p in sum(n['prerequisites'],[]):
            if p not in by:errors.append('Missing parent '+p)
            elif by[p]['xy'][1]>=n['xy'][1]:errors.append('Non-downward prerequisite '+n['key'])
        for mid in n['mutually_exclusive']:
            if n['id'] not in by[mid]['mutually_exclusive']:errors.append('Asymmetric exclusion '+n['key'])
        for other in nodes:
            if n['id']<other['id'] and abs(n['xy'][0]-other['xy'][0])*96<165 and abs(n['xy'][1]-other['xy'][1])*130<128:errors.append('Card collision '+n['key']+' / '+other['key'])
    # Every shared or party programme must have real country development, not an unlock-only root.
    for g in model['groups']:
        root=by[g['nodes'][0]]
        if not root['effects'] and not root['modifiers']:errors.append('Empty programme root '+g['id'])
    return dict(errors=errors,focuses=len(nodes),groups=len(model['groups']),government_programmes=sum(g['slot'] is not None for g in model['groups']),exclusive_pairs=sum(len(n['mutually_exclusive']) for n in nodes)//2,prerequisite_edges=sum(len(p) for n in nodes for p in n['prerequisites']),native_title_max=max(n['title_width'] for n in nodes))

def write_docs(model,qa):
    by={n['id']:n for n in model['nodes']}
    md=['# COLDWAR_CUB — Cuba 1970–1990 approval concept','',f'{len(by)} focuses; 13 governing programmes; 7 initial spirits. English localisation only. No runtime installation.','', 'All numerical values are proposed balance values, not historical measurements. Sources verify institutions, constraints and API support.','', '## Programme structure','', '| Programme | Root x,y | Focuses | Ruling slot |','|---|---|---:|---:|']
    md += [f'| {g["label"]} | {g["root"][0]},{g["root"][1]} | {len(g["nodes"])} | {g["slot"] if g["slot"] is not None else "Shared"} |' for g in model['groups']]
    md += ['', '## Initial situation','', 'Fidel Castro is Prime Minister; the PCC governs through exact subparty slot 4. No starting army, industry, money or party popularity is invented by this design.','',life.SETUP['text'],'',life.SETUP['guard'],'']
    for s in model['starting_spirits']:
        md += ['### '+s['title'],'',s['description'],'', '; '.join(r['label']+' '+r['text'] for r in s['modrows'])+'.','', 'Resolution: '+s['resolution'],'']
    md+=['## Complete focus matrix','']
    for g in model['groups']:
        md+=['### '+g['label'],'',g['summary'],'']
        for nid in g['nodes']:
            n=by[nid]
            prereq=' AND '.join(' OR '.join(by[p]['title'] for p in row) for row in n['prerequisites']) or 'Programme root'
            md += [f'#### {n["title"]} · {n["days"]} days · ({n["xy"][0]},{n["xy"][1]})','', n['description'],'',f'`{nid}` · Native card title: {n["native_title"]}.', '', 'Prerequisite: '+prereq+'.', '', 'Effects: '+('; '.join(r['label']+' '+r['text'] for r in n['modrows'])+'; ' if n['modrows'] else '')+'; '.join(n['effect_rows'])+'.', '', 'Lifetime: '+n['lifetime']+'.', '', 'Requirements: '+(n['extra_gate'] or ('Exact governing subparty '+str(n['slot']) if n['slot'] is not None else 'Shared national programme'))+'.','']
            if n['mutually_exclusive']:md+=['Excludes: '+', '.join(by[p]['title'] for p in n['mutually_exclusive'])+'.','']
    md+=['## Bilateral agreements','']
    for k,v in model['contracts'].items():md+=['### '+v['title'],'', '\n'.join('- '+x for x in v['terms']),'', 'Guard: '+v['guard'],'','Implementation: '+v['custom'],'']
    md+=['## Historical event layer','']
    for ev in model['chronology']:
        md+=['### '+ev['title']+' · '+ev['date'],'',ev['trigger'],'',ev['duration'],'']
        md+=['- '+x['title']+': '+('; '.join(x['effects']) if isinstance(x['effects'],list) else x['effects']) for x in ev['choices']]
        md+=['',ev['history'],'']
    md+=['## Fidel-era expansion: historical research','',
         'The five added PCC focuses cover the Family Code and employment supports (1975), family doctor-and-nurse teams (1984), the Biological Front/CIB/CIGB programme (1981–86), free peasant markets (1980–86) and the microbrigade revival (1986–87). The market experiment existed historically; keeping it after the rectification turn is the alternate continuation. The funded social and scientific programmes are complementary, while the two economic follow-ups inherit the existing SDPE/Rectification exclusion.', '',
         'See [the dedicated research memo](FIDEL_EXPANSION_RESEARCH.md), [mechanics and reference review](FIDEL_EXPANSION_MECHANICS_REVIEW.md), and [layout review](FIDEL_EXPANSION_LAYOUT_REVIEW.md). The First PCC Congress is not a predecessor to the Family Code, which historically came first. Numerical rewards are balance proposals, not historical budget/output measurements.','']
    md+=['## Integration contract','']+['- '+x for x in model['rules']]
    for lc in model['lifecycles']:md+=['','### '+lc['title'],'']+['- '+x for x in lc['rules']]
    md+=['','## Review and limits','', 'The structure and effects were checked separately against main MD Cuba/Russia, January 1970 country history, party registry, current modifier readers and historical research. Read `history_research.md`, `HISTORICAL_REVIEW.md`, `md_reference_profile.md`, `effect_api_audit.md`, `MECHANICS_REVIEW.md` and `LAYOUT_REVIEW.md` for source evidence and independent findings.','', 'This directory is an approval design. The native excerpts deliberately comment out custom contract calls and dynamic programme updates. They are not a runnable tree and must never be copied into game folders as-is. Bilateral event handlers, receipts, conditional starting-spirit replacements, on-change cleanup and English effect localisation require implementation after approval. No engine or multiplayer test is claimed.','', 'Government availability and reward guards use exact ruling subparty. Existing native government-change callbacks must invoke the Cuba refresh. Refresh recalculates only active modifiers from completed receipts. It never repeats construction, money, research or treaty payments. Run at initialization, government change and a weekly reconciliation. The party programme is removed when its slot leaves office and restored when the same slot returns. Construction and international contracts revalidate before any payment.','', 'Historical branching uses political conditions rather than mandatory dates, except genuinely commemorative actions. Counterfactual governments require an actual negotiated, elite/security or conflict settlement; no focus manufactures domestic electoral support.','', 'Static checks: '+json.dumps(qa)+'.']
    (OUT/'CUBA_1970_CONCEPT.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    excerpts='\n\n'.join(n['script'] for n in model['nodes'])
    (OUT/'FOCUS_REVIEW_EXCERPTS.txt').write_text(excerpts+'\n',encoding='utf-8')
    (OUT/'COLDWAR_CUB_1970_CONCEPT.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'STATIC_VALIDATION.json').write_text(json.dumps(qa,indent=2)+'\n',encoding='utf-8')
    provenance={k:{x:v for x,v in a.items() if x!='uri'} for k,a in ART.items()}
    (OUT/'ART_PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')

def main():
    OUT.mkdir(parents=True,exist_ok=True);VIS.mkdir(parents=True,exist_ok=True)
    model=enrich();qa=validate(model)
    if qa['errors']:raise SystemExit(json.dumps(qa,indent=2))
    # Real native titlebar pixels; all preview assets are embedded, no network dependency.
    model['titlebars']={}
    for state,file in [('available','focus_can_start_bg'),('locked','focus_unavailable_bg'),('completed','focus_completed_bg')]:
        p=GAME/'gfx/interface/focusview/titlebar'/(file+'.dds')
        model['titlebars'][state]=uri(Image.open(p).convert('RGBA'))
    # Native three-frame exclusive marker, first (centre) frame only.
    exclusive=Image.open(GAME/'gfx/interface/focusview/focus_link_exclusive.dds').convert('RGBA')
    model['exclusive_art']=uri(exclusive.crop((0,0,exclusive.width//3,exclusive.height)))
    write_docs(model,qa)
    template=(Path(__file__).with_name('tree_fragment.html')).read_text(encoding='utf-8')
    fragment=template.replace('__CUBA_DATA__',json.dumps(model,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
    path=VIS/'cuba-1970-focus-concept.html';path.write_text(fragment,encoding='utf-8')
    assert len(path.read_bytes())<1000000, len(path.read_bytes())
    (OUT/'PREVIEW.html').write_text('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;background:#161b1d;color:#ded9cb;font:14px Arial}</style></head><body>'+fragment+'</body></html>',encoding='utf-8')
    print(json.dumps(dict(**qa,bytes=path.stat().st_size,preview=str(path))))

if __name__=='__main__':main()
