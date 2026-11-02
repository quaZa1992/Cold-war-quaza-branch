# IMPERIA COLD WAR — SSR isolated approval preview builder.
"""Writes only design documentation and a conversation preview, never game files."""
from pathlib import Path
import base64, hashlib, importlib.util, io, json, re, sys, zlib
from copy import deepcopy
from PIL import Image
sys.dont_write_bytecode=True
import content as c
import rules
import market

ROOT=c.ROOT
HERE=Path(__file__).resolve().parent
OUT=ROOT/'docs/design/ssr_1970_concept'
VIS=Path('C:/Users/Enes/.codex/visualizations/2026/10/24/01a16fe2-4dd4-7db2-af76-153d99ebf7bd')
MAIN=Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
spec=importlib.util.spec_from_file_location('ssr_native_font',ROOT/'tools/cuba_1970_concept/native_font.py')
font=importlib.util.module_from_spec(spec);spec.loader.exec_module(font)

def uri(im,lossless=True):
    buf=io.BytesIO();im.save(buf,'WEBP',lossless=lossless,quality=86,method=6)
    return 'data:image/webp;base64,'+base64.b64encode(buf.getvalue()).decode()

def registry():
    reg={}
    for root in [GAME,MAIN,ROOT]:
        for p in sorted((root/'interface').glob('*.gfx')):
            for m in re.finditer(r'spriteType\s*=\s*\{([^{}]*)\}',p.read_text(encoding='utf-8-sig',errors='replace'),re.I|re.S):
                name=re.search(r'\bname\s*=\s*"([^"]+)"',m[1]);tex=re.search(r'\btexturefile\s*=\s*"([^"]+)"',m[1],re.I)
                if name and tex:reg[name[1]]=(tex[1].replace('\\','/'),str(p))
    return reg

def blocks(text,key):
    for m in re.finditer(r'\b'+re.escape(key)+r'\s*=\s*\{',text):
        start=m.end();depth=1;quoted=False;escape=False;i=start
        while depth and i<len(text):
            ch=text[i]
            if ch=='"' and not escape:quoted=not quoted
            if not quoted:
                if ch=='{':depth+=1
                if ch=='}':depth-=1
            escape=(ch=='\\' and not escape);i+=1
        yield text[start:i-1]

def external():
    source=ROOT/'common/national_focus/COLDWAR_UNI_1970_union_joint.txt'
    text=re.sub(r'#[^\n]*','',source.read_text(encoding='utf-8-sig'))
    loc={}
    for path in (ROOT/'localisation/english').glob('*UNI*.yml'):
        loc.update(dict(re.findall(r'^\s*([^\s:#]+):\d*\s+"([^"\n]*)"',path.read_text(encoding='utf-8-sig'),re.M)))
    nodes=[];coords={}
    for b in blocks(text,'joint_focus'):
        key=re.search(r'\bid\s*=\s*(\w+)',b)[1]
        x=int(re.search(r'\bx\s*=\s*(-?\d+)',b)[1]);y=int(re.search(r'\by\s*=\s*(-?\d+)',b)[1])
        a=re.search(r'\brelative_position_id\s*=\s*(\w+)',b)
        if a:
            xx,yy=coords[a[1]];x+=xx;y+=yy
        else:x,y=70,0
        coords[key]=(x,y)
        prereq=[re.findall(r'\bfocus\s*=\s*(\w+)',v) for v in blocks(b,'prerequisite')]
        icon=re.search(r'\bicon\s*=\s*(\w+)',b)
        code='\n'.join(blocks(b,'completion_reward'))
        title=loc.get(key,key.removeprefix('COLDWAR_UNI_').replace('_',' ').title())
        n=dict(id=key,key=key,title=title,description=loc.get(key+'_desc','Existing Union Plan joint focus. The Soviet host and republics retain the current joint completion rules.'),
               group='union_plan',x=x,y=y,prerequisites=prereq,exclusive=[],cost=float(re.search(r'\bcost\s*=\s*([\d.]+)',b)[1]),
               phase='external',kind='institution',modifiers={},treasury=0,spirit=None,replace=None,remove=None,
               building=None,research=None,army_xp=0,doctrine=None,stability=0,decision=None,action=None,gate='union_member',
               ownership='Existing shared Union programme',source_sprite=icon[1] if icon else None,source_reward=code,
               source=str(source),anchor=a[1] if a else None)
        n['days']=n['cost']*7
        nodes.append(n)
    return nodes,dict(path=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                       generic_root=[240,0],soviet_root=[355,8],proposed_ssr_root=[70,0])

SHORT={
 'Diaspora Workshop Fund':'Diaspora Workshops','Green Workshop Permits':'Green Workshops',
 'Open Workshop Licences':'Workshop Licences','Revolutionary Command':'Cadre Command',
 'Worker-Owned Workshops':'Worker Workshops',
 'A Georgian Film Republic':'The Film Republic', 'A Georgian Workers\' Republic':'Workers\' Republic',
 'A Hunchakian Social Republic':'Hunchakian Republic', 'A Kazakh Workers\' Republic':'Workers\' Republic',
 'A Kyrgyz Workers\' Republic':'Workers\' Republic', 'A Latvian Labour Republic':'A Labour Republic',
 'A Latvian Workers\' Republic':'Workers\' Republic', 'A Lithuanian Labour Republic':'A Labour Republic',
 'A Lithuanian Workers\' Republic':'Workers\' Republic', 'A Moldavian Workers\' State':'A Workers\' State',
 'A Social Democratic Estonia':'Social Democracy', 'A Tajik Workers\' Republic':'Workers\' Republic',
 'A Turkmen Workers\' Republic':'Workers\' Republic', 'An Armenian Workers\' Republic':'Workers\' Republic',
 'An Azerbaijani Workers\' Republic':'Workers\' Republic', 'An Estonian Workers\' Republic':'Workers\' Republic',
 'An Uzbek Workers\' Republic':'Workers\' Republic', 'Christian Democratic Lithuania':'Christian Democracy',
 'Christian National Solidarity':'Christian Solidarity', 'Commercial Distribution':'Trade Distribution',
 'Community Endowments':'Local Endowments','Community Water Shares':'Local Water Shares',
 'Consumer Manufacturing':'Consumer Industry','Electronics and Research':'Electronics Research',
 'Gas Compressor Network':'Gas Compressor Works','Ground Forces and Logistics':'Ground Force Service',
 'Maritime Industry and Fleet':'Maritime Industry','National Unity Underground':'National Unity',
 'Permanent Service Depots':'Service Depots','Resources and Processing':'Resource Processing',
 'Santara-Sviesa Lithuania':'Santara-Sviesa','The Alash Constitutional League':'The Alash Legacy',
 'The Anti-Nuclear Assembly':'Anti-Nuclear Assembly','The Cassette Generation':'Cassette Generation',
 'The Estonian Government':'Exile Government','The Georgian Literary Republic':'Literary Republic',
 'The Kazakh Land Congress':'Land and Nation','The Latvian Diplomatic Service':'Diplomatic Continuity',
 'The Liberal Armenian Union':'A Liberal Republic','The Lithuanian Diplomatic Service':'Diplomatic Continuity',
 'The Manas Cultural Council':'The Manas Legacy','The Minsk Literary Circle':'Minsk Literary Circle',
 'The National Patriotic Front':'The Patriotic Front','The Samanid Cultural Council':'The Samanid Legacy',
 'The Tajik Workers\' Council':'Workers\' Council','The Turkmen Literary Council':'Literary Council',
 'The Turkmen Workers\' Council':'Workers\' Council','The Uzbek Literary Council':'Literary Council',
 'The Workers\' Council Republic':'Council Republic','Women in the Workshops':'Women\'s Workshops',
 'Administrative Discipline':'Cadre Discipline',
 'Revolutionary Authority':'Revolutionary Rule',
 'A Constitutional Republic':'Constitutional Rule',
 'Directives of the Ninth Plan':'Ninth Plan Orders', 'Directives of the Tenth Plan':'Tenth Plan Orders',
 'Directives of the Eleventh Plan':'Eleventh Plan Orders', 'Directives of the Twelfth Plan':'Twelfth Plan Orders',
 'The Eleventh Plan Fulfilled':'Eleventh Plan Met', 'The Twelfth Plan Fulfilled':'Twelfth Plan Met',
 'The Party Control Commission':'Party Commission', 'Food and Textile Balance':'Food and Textiles',
 'Skills for Reconstruction':'Reconstruction Skills', 'The Socialist Settlement':'Socialist Settlement',
 'Republican Secretariat':'Secretariat', 'Republican Accounts':'Republican Accounts',
 'Republican Mandate':'Republican Mandate', 'Professional Appointments':'Appointments',
 'State Production':'State Production', 'Public Enterprise Accounts':'Public Accounts',
 'Public Technical Schools':'Technical Schools', 'Constitutional Settlement':'The Constitution',
 'Community Representation':'Community Voice', 'National Representation':'National Voice',
 'Compensation Bonds':'Claims Bonds', 'An Independent Press':'A Free Press',
 'Collective Bargaining':'Labour Bargaining', 'Republican Reinvestment':'Reinvestment',
 'Defence Administration':'Defence Authority', 'Unsettled Defence Administration':'Defence Transition',
 'Train the Secretariat':'Secretariat School', 'Consumer Diversification':'Consumer Industry',
 'Machine-Building Complex':'Machine Building', 'Agricultural Processing':'Food Processing',
 'Mixed Republican Industry':'Mixed Industry', 'Oil-Shale Modernisation':'Oil-Shale Industry',
 'Technical Diversification':'Technical Industry', 'Port and Consumer Services':'Port Services',
 'Manufacturing Network':'Manufacturing', 'Agricultural Modernisation':'Modern Agriculture',
 'Tea and Processing':'Tea Processing', 'Light-Industrial Workshops':'Light Industry',
 'Engineering Institutes':'Engineering', 'Local Supply Workshops':'Local Workshops',
 'Refining and Equipment':'Refining Equipment', 'Industrial and Grain Orders':'Grain and Industry',
 'Regional Diversification':'Regional Industry', 'Water-Saving Diversification':'Water-Saving Farms',
 'Hydropower and Workshops':'Power and Industry', 'Cotton and Power Orders':'Cotton and Power',
 'Food and Regional Industry':'Food and Industry', 'National Officer School':'Officer School',
 'Defence Training Convention':'Training Convention', 'Civic Religious Education':'Civic Education',
 'Veterans and the State':'Veterans in the State', 'Commercial Standards':'Trade Standards',
 'Republican Development Priorities':'Regional Priorities',
}

def effects(n):
    rows=[]
    if n.get('gdp_cost'):rows.append(f'Treasury -{n["gdp_cost"]*100:g}% of GDP (one time)')
    if n.get('weekly_gdp_cost'):rows.append(f'Weekly programme budget -{n["weekly_gdp_cost"]*100:g}% of GDP')
    if n.get('replace'):rows.append('Replace '+n['replace']+' with '+str(n['spirit']))
    elif n.get('remove'):rows.append('Remove '+n['remove'])
    if n.get('modifiers'):
        if not n.get('replace'):rows.append(('Modify ' if n.get('effect_mode')=='modify' else 'Add ')+str(n['spirit']))
        rows.extend(modifier_rows(n.get('display_modifiers',n['modifiers'])))
    if n.get('building'):
        b=n['building'];rows += [b['target']+f': shared building slots +{b["shared_slots"]}',b['target']+f': {BUILDINGS[b["type"]]} +{b["level"]}']
    if n.get('research'):
        r=n['research'];rows.append(f'{r["uses"]} x {r["bonus"]*100:g}% research bonus: {CATEGORIES.get(r["category"],r["category"])}')
    if n.get('doctrine'):
        r=n['doctrine'];rows.append(f'{r["uses"]} x {r["bonus"]*100:g}% doctrine cost reduction: {r["category"]}')
    if n.get('army_xp'):rows.append(f'Army experience +{n["army_xp"]}')
    if n.get('air_xp'):rows.append(f'Air experience +{n["air_xp"]}')
    if n.get('navy_xp'):rows.append(f'Naval experience +{n["navy_xp"]}')
    if n.get('stability'):rows.append(f'Stability {n["stability"]*100:+g} percentage points')
    if n.get('decision'):rows.append('Unlock decision: '+n['decision'])
    if n.get('market_charter'):rows.append('Unlock decisions: Competitive Sale, Worker Buyout')
    if n.get('public_charter'):rows.append('Unlock decision: Public Retooling')
    if n.get('party_transfer'):
        t=n['party_transfer'];rows += [f'{t["from_name"]}: current party support -{t["fraction"]*100:g}% (relative)',t['to_name']+': gain the transferred support']
    for idea in n.get('timed_ideas',[]):
        rows.append(f'Add {idea["name"]} for {idea["days"]} days')
        rows.extend(modifier_rows(idea['modifiers']))
    for idea in n.get('persistent_ideas',[]):
        rows.append('Add '+idea['name']);rows.extend(modifier_rows(idea['modifiers']))
    for gear in n.get('equipment_bonuses',[]):
        rows.append(EQUIPMENT.get(gear['target'],gear['target']))
        rows.extend(f'{GEAR_LABELS.get(k,k)} {v*100:+g}%' for k,v in gear['modifiers'].items())
    if n.get('specialisation'):
        rows.append('After independence: '+n['legacy_spirit'])
        rows.extend(modifier_rows(n['legacy_modifiers']))
        for gear in n.get('legacy_equipment_bonuses',[]):
            rows.append(EQUIPMENT.get(gear['target'],gear['target']))
            rows.extend(f'{GEAR_LABELS.get(k,k)} {v*100:+g}%' for k,v in gear['modifiers'].items())
        if n.get('legacy_weekly_gdp_cost'):rows.append(f'Weekly programme budget -{n["legacy_weekly_gdp_cost"]*100:g}% of GDP')
    if n.get('repair_variants'):
        for variant in n['repair_variants']['abrupt']:
            rows.append('With '+str(variant['before_count'])+' completed repairs: '+('Remove ' if variant['before_count']==2 else 'Modify ')+variant['name'])
            rows.extend(f'{c.LABELS[k]} {v*100:+g}%' for k,v in variant['delta'].items())
    if n.get('preparation_effect'):
        rows.append('On independence: Modify '+n['preparation_effect']['name'])
        rows.extend(f'{c.LABELS[k]} {v*100:+g}%' for k,v in n['preparation_effect']['delta'].items())
    if n.get('exposure'):
        rows.append('On independence: Add '+n['exposure']['name'])
        rows.extend(f'{c.LABELS[k]} {v*100:+g}%' for k,v in n['exposure']['modifiers'].items())
    if n.get('remove_exposure'):rows.append('Remove '+n['remove_exposure'])
    for s in n.get('conditional_removals',[]):
        rows.append('If present: Remove '+s['name'])
        rows.extend(f'{c.LABELS[k]} {v*100:+g}%' for k,v in s['delta'].items())
    if n.get('regional_aftercare'):
        s=n['regional_aftercare'];rows.append('If present: Replace '+s['old']+' with '+s['new'])
        rows.extend(f'{c.LABELS[k]} {v*100:+g}%' for k,v in s['delta'].items())
    action=n.get('action') or ''
    if action.startswith('offer:'):
        contract=c.CONTRACTS[action[6:]];rows.append('If they accept: '+contract['title'])
        for role in ['origin','recipient']:
            t=contract[role];rows += [role.title()+': '+t['spirit'],f'Treasury -{t["gdp_cost"]*100:g}% of GDP',f'Weekly programme budget -{t["weekly_gdp_cost"]*100:g}% of GDP']
            rows.extend(f'{c.LABELS[k]} {v*100:+g}%' for k,v in t['modifiers'].items())
    return rows

BUILDINGS=dict(industrial_complex='Civilian factory',arms_factory='Military factory',dockyard='Naval dockyard',
 infrastructure='Infrastructure',fossil_powerplant='Fossil fuel power plant',agriculture_district='Agricultural district')
CATEGORIES=dict(CAT_industry='Industry',CAT_electronics='Electronics',CAT_infantry='Infantry',
 CAT_artillery='Artillery',CAT_tanks='Tanks',CAT_aircraft='Aircraft',CAT_corvettes='Corvettes',CAT_destroyers='Destroyers')
EQUIPMENT={}
for _name in ['plane_designer_l_english.yml','equipment_l_english.yml','equip_naval_l_english.yml']:
    _text=(ROOT/'localisation/english'/_name).read_text(encoding='utf-8-sig')
    EQUIPMENT.update(dict(re.findall(r'^\s*([^\s:#]+):\d*\s+"([^"\n]*)"',_text,re.M)))
# Keep only equipment names used by this concept, sourced from native MD text.
_targets={'small_plane_airframe','small_plane_strike_airframe','small_plane_cas_airframe',
 'medium_plane_airframe','medium_plane_fighter_airframe','medium_plane_cas_airframe',
 'large_plane_air_transport_airframe','medium_tank_chassis','artillery_equipment',
 'medium_tank_artillery_chassis','medium_tank_rocket_chassis','infantry_weapons_type',
 'util_vehicle_type','cnc_equipment_type','patrol_boat','corvette','frigate'}
EQUIPMENT={key:EQUIPMENT[key] for key in sorted(_targets)}
GEAR_LABELS=dict(build_cost_ic='Production cost',reliability='Reliability',armor_value='Armour',soft_attack='Soft attack')
def modifier_rows(mods):
    return [f'{c.LABELS[k]} {v:+.3f}' if k in c.NUMBER_KEYS else f'{c.LABELS[k]} {v*100:+g}%' for k,v in mods.items()]

def pack_nodes(payload):
    """Share identical fields across the 14 views without changing their model."""
    samples={}
    for model in payload['models'].values():
        id_key={n['id']:n['key'] for n in model['nodes']}
        for n in model['nodes']:
            n.pop('id')
            n['prerequisites']=[[id_key[v] for v in group] for group in n['prerequisites']]
            n['exclusive']=[id_key[v] for v in n['exclusive']]
            n['anchor']=id_key[n['anchor']] if n.get('anchor') else None
            if n.get('country_module'):n['country_module']=True
            if n['phase']=='party':n.pop('spirit',None)
            samples.setdefault(n['key'],[]).append(n)
    templates={}
    for key,ns in samples.items():
        first=ns[0]
        templates[key]={k:v for k,v in first.items() if all(k in n and n[k]==v for n in ns)}
    for model in payload['models'].values():
        model['nodes']=[dict(key=n['key'],**{k:v for k,v in n.items() if k!='key' and k not in templates[n['key']]}) for n in model['nodes']]
    payload['node_templates']=templates

def main():
    OUT.mkdir(parents=True,exist_ok=True);VIS.mkdir(parents=True,exist_ok=True)
    shared,shared_info=external()
    models={tag:c.design(tag) for tag in c.SELECTION}
    for tag,d in models.items():
        d['initial_transition']={key:rules.initial(tag,key) for key in rules.CASES}
        spirits={s['name']:s['modifiers'] for s in c.STARTING}
        spirits[d['profile']['regional']['name']]=d['profile']['regional']['modifiers']
        spirits.update({n['spirit']:n['modifiers'] for n in d['nodes'] if n.get('effect_mode')=='add' and n.get('spirit')})
        for n in d['nodes']:
            rules.prepare_node(n,tag)
            if n.get('replace'):
                old=spirits[n['replace']]
                n['display_modifiers']={k:round(n['modifiers'].get(k,0)-old.get(k,0),5) for k in sorted(set(old)|set(n['modifiers']))}
                n['display_modifiers']={k:v for k,v in n['display_modifiers'].items() if v}
            if n.get('repair'):
                n['repair_variants']={}
                for case in rules.CASES:
                    s=next(v for v in rules.initial(tag,case) if v['id']==n['repair']['spirit'])
                    n['repair_variants'][case]=[]
                    for count in range(3):
                        before={k:round(v*(3-count)/3,5) for k,v in s['modifiers'].items()}
                        after={k:round(v*(2-count)/3,5) for k,v in s['modifiers'].items()}
                        n['repair_variants'][case].append(dict(name=s['name'],before_count=count,
                            delta={k:round(after[k]-before[k],5) for k in after}))
            if n.get('preparation'):
                s=next(v for v in rules.initial(tag,'abrupt') if v['id']==n['preparation']['spirit'])
                n['preparation_effect']=dict(name=s['name'],delta={k:round(-v*n['preparation']['reduction'],5) for k,v in s['modifiers'].items()})
    allnodes=[n for d in models.values() for n in d['nodes']]+shared
    for n in allnodes:
        n['full_title']=n['title'];n['title']=SHORT.get(n['title'],n['title'])
    long=sorted({(n['title'],font.width(n['title'])) for n in allnodes if font.width(n['title'])>143})
    if long:
        print(json.dumps({'long_titles':long}));return
    reg=registry();art={};provenance=[]
    sprites=dict(institution='GFX_COLDWAR_goal_constitutional_guarantees',industry='GFX_COLDWAR_goal_Expand_Heavy_Industry',
                 research='GFX_COLDWAR_goal_Invest_in_Education',society='GFX_COLDWAR_goal_SOV_Kickstart_Rural_Healthcare',
                 army='GFX_COLDWAR_goal_generic_army_training',agriculture='GFX_COLDWAR_goal_agricultural_banks',
                 diplomacy='GFX_goal_generic_trade',air='GFX_COLDWAR_goal_SOV_AF',navy='GFX_COLDWAR_goal_SOV_the_soviet_navy')
    themed={
      'secretariat':'Democratic_Centralism','moscow_cadres':'Elite_Communist_Party','local_cadres':'Civil_Service_Decisions',
      'appointment_school':'Invest_in_Education','audit_staff':'Crackdown_on_Party_Corruption',
      'discipline_campaign':'Bring_the_soviet_people_into_line','complaints_office':'Generic_Factionalism',
      'plan_bargain':'BeginNegotiations','priority_orders':'CommunistProductionFocus',
      'local_retention':'Focus_on_the_Needs_of_the_Working_Class','successor_training':'Elite_Communist_Party',
      'controlled_debate':'Communist_Liberalization','unified_line':'Democratic_Centralism',
      'republican_statute':'constitutional_guarantees','union_delegate':'COMECON2',
      'economic_accounts':'Five_Year_Plan','enterprise_accounts':'Centrally_Planned_Economy',
      'rail_depots':'Connect_the_Union','technical_institutes':'CommunistScientists',
      'water_accounts':'Focus_on_Water_and_Agricultural_Projects','foreign_service':'Form_the_Ministry_of_Foreign_Affairs',
      'border_offer':'FocusBorderTroops','training_offer':'generic_army_training',
      'old_market_offer':'BeginNegotiations','new_market_offer':'Foriegn_Investment',
      'defence_commission':'Generic_Red_Army','technical_reserves':'Conscription',
    }
    special_icons={'aircraft':'SOV_AF','armour':'generic_army_tanks2',
      'artillery':'generic_rocket_artillery','army':'generic_army_training',
      'navy':'TheRedFleet','agriculture':'agricultural_banks',
      'industry':'Expand_Heavy_Industry','resources':'generic_coal_mining',
      'electronics':'Microelectronics_industry'}
    for n in allnodes:
        if n.get('specialisation'):
            programme=n['specialisation'];role=n['key'].removeprefix('special_'+programme+'_')
            sprite={'works':'Expand_Heavy_Industry','schools':'Invest_in_Education',
                    'office':'Civil_Service_Decisions','priority':'CommunistProductionFocus',
                    'efficiency':'Five_Year_Plan','settlement':'COMECON2',
                    'left_follow':'CommunistScientists','right_follow':'Invest_in_Education'}.get(role,special_icons[programme])
            n['art_key']='special_'+sprite;sprites[n['art_key']]='GFX_COLDWAR_goal_'+sprite
        elif n['key'] in themed:
            n['art_key']='theme_'+n['key'];sprites[n['art_key']]='GFX_COLDWAR_goal_'+themed[n['key']]
        elif n['phase']=='external' and n.get('source_sprite') in reg:
            n['art_key']='shared_'+n['key'];sprites[n['art_key']]=n['source_sprite']
        elif n['phase']=='party' and n['key'].endswith('_root'):
            profile=next(d['profile'] for d in models.values() if n in d['nodes'])
            family=next(p['family'] for p in profile['parties'] if 'slot'+str(p['slot'])==n['gate'])
            party_sprite={'communist':'A_developed_socialism','liberal':'new_democratic_elections',
                          'restoration':'constitutional_guarantees','social':'Democratic_Socialism',
                          'national_social':'Democratic_Socialism','nationalist':'national_party',
                          'authoritarian':'national_party'}.get(family,'Brotherhood_and_Unity')
            n['art_key']='party_'+family; sprites[n['art_key']]='GFX_COLDWAR_goal_'+party_sprite
        else:n['art_key']=n['kind']
    for kind,sprite in sprites.items():
        rel,provider=reg[sprite];p=next(r/rel for r in (ROOT,MAIN,GAME) if (r/rel).is_file())
        im=Image.open(p).convert('RGBA');im.thumbnail((104,104),Image.Resampling.LANCZOS)
        art[kind]=uri(im,False)
        provenance.append(dict(sprite=sprite,path=str(p),provider=provider,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                               author='Unknown; inherited MD or Cold War asset',licence='Unknown; project preview reuse only',modification='Preview resampling and WebP compression only'))
    titlebars={}
    for state,filename in [('available','focus_can_start_bg'),('locked','focus_unavailable_bg')]:
        p=GAME/f'gfx/interface/focusview/titlebar/{filename}.dds';titlebars[state]=uri(Image.open(p).convert('RGBA'))
        provenance.append(dict(path=str(p),author='Paradox Interactive',licence='Proprietary game asset; local preview only',modification='None'))
    used={ord(ch) for n in allnodes for ch in n['title']};used.add(63)
    font_data=dict(uri=uri(font.atlas()),glyphs={key:val for key,val in font.GLYPHS.items() if key in used},
                   kernings={str(a)+'_'+str(b):v for (a,b),v in font.KERNINGS.items() if a in used and b in used})
    qa={};catalogue=['IMPERIA COLD WAR\n# Universal SSR focus concept\n\nApproval draft, 25 October 2026. No loaded game content is changed.\n']
    for tag,d in models.items():
        ids={n['id']:n for n in d['nodes']};errors=[]
        for n in d['nodes']:
            for group in n['prerequisites']:
                for parent in group:
                    if parent not in ids:errors.append('Missing '+parent)
                    elif ids[parent]['y']>=n['y']:errors.append('Non-forward edge '+n['id'])
            for ex in n['exclusive']:
                if n['id'] not in ids[ex]['exclusive']:errors.append('Asymmetric exclusion '+n['id'])
            if n['anchor'] and list(ids).index(n['anchor'])>=list(ids).index(n['id']):errors.append('Forward anchor '+n['id'])
            for k in n['modifiers']:
                if k not in c.LABELS:errors.append('Unknown modifier '+k)
        coords={}
        for n in d['nodes']:
            key=n['x'],n['y']
            if key in coords:errors.append('Overlapping nodes '+n['id'])
            coords[key]=n['id']
        qa[tag]=dict(new_focuses=len(ids),ssr_focuses=sum(n['phase']=='ssr' for n in d['nodes']),parties=len(d['profile']['parties']),errors=errors)
        catalogue += [f'\n## {tag}: {d["profile"]["name"]}\n\nFirst Secretary: {d["profile"]["leader"]}.\n']
        for n in d['nodes']:
            catalogue.append(f'\n### {n["id"]}: {n["title"]}\n\n{n["description"]}\n\nPosition: ({n["x"]}, {n["y"]}). Cost: {n["cost"]}; {n["days"]} days. {n["ownership"]}.\n\nPrerequisites (groups are AND; entries are OR): '+json.dumps(n['prerequisites'])+'\n\nEffects:\n\n'+'\n'.join('- '+v for v in effects(n))+'\n')
        d['groups'].append(dict(id='union_plan',title='The Union Plan: Existing Shared Tree',x=70,y=0,phase='external',note='Current shared content retained; proposed SSR host relocation only.'))
    assert not any(v['errors'] for v in qa.values()),qa
    manifest=dict(project='IMPERIA COLD WAR',revision=2,status='Unapproved concept only',date='2026-10-25',models=models,
                  starting=c.STARTING,transition=c.TRANSITION,contracts=c.CONTRACTS,labels=c.LABELS,external=shared,shared_source=shared_info,
                  number_keys=sorted(c.NUMBER_KEYS),building_labels=BUILDINGS,research_labels=CATEGORIES,equipment_labels=EQUIPMENT,gear_labels=GEAR_LABELS,
                  market=dict(courses=market.COURSES,methods=market.METHODS,sectors=market.SECTORS,decisions=market.decisions(),rules=market.RULES),
                  qa=qa,provenance=provenance,rules=rules.CONTRACT,cases=rules.CASES,party_triggers=rules.PARTY_TRIGGERS,
                  layout=dict(grid=[96,130],initial_show_position='COLDWAR_SSR_secretariat',
                    continuous_focus_position=dict(x=6100,y=650,width=770,height=380),
                    shortcuts=['COLDWAR_SSR_secretariat','COLDWAR_SSR_economic_accounts','COLDWAR_SSR_social_accounts',
                      'COLDWAR_SSR_defence_commission','COLDWAR_SSR_public_authority','COLDWAR_SSR_payment_register',
                      'COLDWAR_SSR_defence_authority','COLDWAR_SSR_foreign_service','COLDWAR_UNI_the_union_plan']))
    (OUT/'DESIGN.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'FOCUS_CATALOGUE.md').write_text('\n'.join(catalogue),encoding='utf-8')
    (OUT/'STRUCTURE_CHECKS.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',checks=qa),indent=2),encoding='utf-8')
    payload=dict(**manifest,art=art,titlebars=titlebars,font=font_data)
    # Full source records stay in DESIGN.json. The viewer needs no duplicate
    # runtime contracts, full registry essays or verbose provenance per country.
    payload=deepcopy(payload)
    payload.pop('provenance');payload.pop('qa');payload.pop('shared_source')
    for d in payload['models'].values():
        for p in d['profile']['parties']:p['description']=p['description'].split('\n\n')[0]
        for n in d['nodes']:
            for field in ['full_title','offset']:n.pop(field,None)
            if n.get('runtime_contract'):
                n['runtime_contract']=[v if len(v)<130 else ('Recognised SSR status contract' if n['phase']=='ssr' else 'Recognised sovereign-state transition contract') for v in n['runtime_contract']]
    pack_nodes(payload)
    encoded=base64.b64encode(zlib.compress(json.dumps(payload,ensure_ascii=False,separators=(',',':')).encode(),9)).decode()
    fragment=(HERE/'tree_fragment.html').read_text(encoding='utf-8').replace('__SSR_DATA__',encoded)
    fragment=fragment.replace('__SSR_EFFECT_RENDERER__',(HERE/'effect_view.js').read_text(encoding='utf-8'))
    fragment=fragment.replace('__SSR_PANELS__',(HERE/'panel_view.js').read_text(encoding='utf-8'))
    path=VIS/'ssr-focus-concept-v2.html';path.write_text(fragment,encoding='utf-8')
    assert path.stat().st_size<1000000
    for alias in ['ssr-focus-concept.html','ssr-focus-click-fix.html','ssr-equipment-costs.html']:
        (VIS/alias).write_text(fragment,encoding='utf-8')
    (OUT/'PREVIEW.html').write_text('<!-- IMPERIA COLD WAR — SSR concept preview wrapper. -->\n<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;font:14px Arial;background:#20262a;color:#e5e2d5}</style></head><body>'+fragment+'</body></html>',encoding='utf-8')
    (OUT/'ASSET_NOTICE.md').write_text('IMPERIA COLD WAR\n# Preview asset provenance\n\nExisting MD, Cold War and Paradox assets are embedded only in this local concept. The project marker does not establish ownership. Original individual authors and specific licences are unknown where stated. No redistribution permission is inferred. The inherited font is the game hoi_16mbs atlas, rendered into title images. New policy text and layout are original concept work.\n\n'+ '\n'.join('- '+json.dumps(p,ensure_ascii=False) for p in provenance),encoding='utf-8')
    print(json.dumps(dict(bytes=path.stat().st_size,preview=str(path),counts={tag:v['new_focuses'] for tag,v in qa.items()},external=len(shared))))

if __name__=='__main__':main()
