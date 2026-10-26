# IMPERIA CW — Cold War: iraq 1970 concept — build concept.
"""COLDWAR_IRQ approval concept. Writes only this tool's docs and preview; never runtime files."""
from pathlib import Path
import base64, hashlib, io, json, re
from PIL import Image, ImageDraw, ImageFont
from native_font import width as title_width, concise

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT / 'docs/design/iraq_1970'
VIZ = Path('C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f4e-9042-7b61-be51-9d85f9facd82')
MD = Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
PREFIX = 'COLDWAR_IRQ_'
OUT.mkdir(parents=True, exist_ok=True)
# Native 2000-era domestic-helper reference charges, MD billions, NOT 1970 prices.
# They are retained for review, not debited: 7.5 is 229% of Iraq's calibrated1970
# GDP3.281. Explicit new Iraq project invoices use their proposedGDPshares instead.
BUILDING_REFERENCE_PRICES={'industrial_complex':7.5,'arms_factory':7.5,'dockyard':7.5,
                       'infrastructure':3.5,'offices':12.0,'fossil_powerplant':3.25,'agriculture_district':3.75}

# Exact keys used by MD. Values are balance proposals, never historical measurements.
LABELS = {
 'stability_factor': ('Stability', '%'),
 'political_power_factor': ('Political power gain', '%'),
 'drift_defence_factor': ('Ideology drift defence', '%'),
 'production_speed_buildings_factor': ('Construction speed', '%'),
 'industrial_capacity_factory': ('Military factory output', '%'),
 'production_factory_max_efficiency_factor': ('Production efficiency cap', '%'),
 'production_factory_efficiency_gain_factor': ('Production efficiency growth', '%'),
 'consumer_goods_factor': ('Consumer goods factor', '%'),
 'tax_gain_multiplier_modifier': ('Tax revenue multiplier', '%'),
 'oil_export_multiplier_modifier': ('Oil export revenue multiplier', '%'),
 'bureaucracy_cost_multiplier_modifier': ('Bureaucracy expenditure multiplier', '%'),
 'social_cost_multiplier_modifier': ('Social expenditure multiplier', '%'),
 'army_personnel_cost_multiplier_modifier': ('Army personnel expenditure multiplier', '%'),
 'interest_rate_multiplier_modifier': ('Interest rate', ' points'),
 'agricolture_productivity_modifier': ('Agriculture productivity modifier', '%'),
 'research_speed_factor': ('Research speed', '%'),
 'conscription_factor': ('Recruitable population factor', '%'),
 'army_org_factor': ('Division organisation', '%'),
 'army_morale_factor': ('Division recovery', '%'),
 'army_attack_factor': ('Division attack', '%'),
 'army_defence_factor': ('Division defence', '%'),
 'training_time_army_factor': ('Division training time', '%'),
 'supply_consumption_factor': ('Supply consumption', '%'),
 'army_fuel_consumption_factor': ('Army fuel consumption', '%'),
 'fuel_gain_factor': ('Fuel gain', '%'),
 'industrial_capacity_dockyard': ('Dockyard output', '%'),
 'opinion_gain_monthly_same_ideology_factor': ('Same outlook opinion gain', '%'),
 'foreign_influence_modifier': ('Foreign influence', '%'),
 'mdcw_cw_support_effectiveness': ('Foreign party support campaign effectiveness', '%'),
}
K = dict(st='stability_factor', pp='political_power_factor', dd='drift_defence_factor',
 build='production_speed_buildings_factor', out='industrial_capacity_factory', cap='production_factory_max_efficiency_factor',
 eff='production_factory_efficiency_gain_factor', cg='consumer_goods_factor', tax='tax_gain_multiplier_modifier',
 oil='oil_export_multiplier_modifier', admin='bureaucracy_cost_multiplier_modifier', social='social_cost_multiplier_modifier',
 milcost='army_personnel_cost_multiplier_modifier', rate='interest_rate_multiplier_modifier', agri='agricolture_productivity_modifier',
 research='research_speed_factor', man='conscription_factor', org='army_org_factor', morale='army_morale_factor',
 attack='army_attack_factor', defence='army_defence_factor', train='training_time_army_factor', supply='supply_consumption_factor',
 fuel='army_fuel_consumption_factor', refine='fuel_gain_factor', dock='industrial_capacity_dockyard',
 same='opinion_gain_monthly_same_ideology_factor', influence='foreign_influence_modifier', proxy='mdcw_cw_support_effectiveness')

def mods(**values):
    return {K[k]: v for k,v in values.items()}

def item(key, title, story, m=None, *, cost=5, cash=0, build=None, xp=0, decisions=None,
         instant=None, replaces=None, requires=None, icon=None, historic='Policy proposal',outcomes=None,active_requires=None):
    return dict(key=key, title=title, description=story, modifiers=m or {}, cost=cost,
                budget_gdp_share=cash, building=build, army_xp=xp, decisions=decisions or [],
                instant=instant or [], replaces=replaces, requires=requires or [], icon=icon,
                historical_status=historic,**({'outcomes':outcomes} if outcomes else {}),**({'active_requires':active_requires} if active_requires else {}))

GROUPS=[]
def group(key, title, outlook, party, gate, ownership, entries, *, icon='government_beu', note='', shape='fan',geometry=None,exclusions=None):
    assert len(entries)==len(geometry or FAN), (key,len(entries))
    GROUPS.append(dict(id=key,label=title,outlook=outlook,party=party,gate=gate,ownership=ownership,
                       entries=entries,icon=icon,note=note,shape=shape,**({'geometry':geometry,'exclusions':exclusions or {}} if geometry else {})))

def D(key,title,cost,days,summary,**kw):
    return dict(id=PREFIX+'decision_'+key,label=title,pp=cost,days=days,summary=summary,**kw)

# Three independently useful policy lanes below two explicit institutional choices.
# Each pair is a genuine exclusion. The convergence is OR, never an impossible AND.
FAN=[(0,0,[]),(-1,1,[[0]]),(1,1,[[0]]),(-1,2,[[1]]),(1,2,[[2]]),
     (0,3,[[3,4]]),(-1,4,[[5]]),(1,4,[[5]]),(-1,5,[[6]]),(1,5,[[7]]),
     (0,6,[[8,9]]),(-2,7,[[10]]),(0,7,[[10]]),(2,7,[[10]]),
     (-2,8,[[11]]),(0,8,[[12]]),(2,8,[[13]]),(0,9,[[14,15,16]])]

def authored_content():
    # The authored groups live separately so the visual and review catalogue share one source.
    import sys
    sys.path.insert(0,str(HERE))
    import content
    content.populate(group,item,mods,D)
    import iran_war
    iran_war.populate(group,item,mods,D)

SPIRITS=[
 dict(id=PREFIX+'spirit_july_state',label='The July State',owner='Baath government',
      description='The 1968 regime rests on the Revolutionary Command Council, party organization and coercive institutions. State consolidation conceals factional insecurity.',
      modifiers=mods(pp=.08,dd=.15,st=-.08,admin=.08),
      treatment='Baath institutional choices replace this spirit; suspend it when Baath leaves government. Never turn the later Saddam personality cult into a January 1970 fact.'),
 dict(id=PREFIX+'spirit_unsettled_north',label='An Unsettled Northern Question',owner='National situation',
      description='The Kurdish war and unresolved demands for autonomy strain Baghdad. The March 1970 accord is still a negotiation, not a starting achievement.',
      modifiers=mods(st=-.12,milcost=.10,supply=.04),
      treatment='A fulfilled autonomy contract reduces the national burden; negotiated federal settlement replaces it. Local insecurity is not simulated with resistance on Iraqi cores.'),
 dict(id=PREFIX+'spirit_ipc',label='Oil Beneath Foreign Concessions',owner='National situation',
      description='The Iraq Petroleum Company concession system and disputes over production constrain control over oil revenue despite the 1961 expropriation of undeveloped concession areas.',
      modifiers=mods(oil=-.18),
      treatment='Nationalization or a renegotiated concession replaces this modifier. Oil remains finite map resources; no second fictional oil income system.'),
 dict(id=PREFIX+'spirit_rural',label='The Unfinished Agrarian Reform',owner='National situation',
      description='Unequal landholding, weak delivery of reform, rural credit shortages and limited irrigation hinder agriculture and encourage migration.',
      modifiers=mods(agri=-.12,cg=.03),
      treatment='Agricultural credit, tenure and irrigation milestones remove separate penalties. Agriculture input values follow MD calculations, not literal historical output percentages.'),
 dict(id=PREFIX+'spirit_literacy',label='A Narrow Base of Skills',owner='National situation',
      description='Low literacy and uneven access to education restrict the capacity to absorb complex civilian and military technology.',
      modifiers={}, native_system='Native MD literacy/education dynamic modifier; proposed literacy_rate = 0.35, calibration pending historical evidence. No extra research penalty.',
      native_consequences={'Research speed': '-30%', 'Education expenditure multiplier': '+60%',
                           'Productivity growth input':'-1.20 MD points', 'Office productivity':'-30%',
                           'Agriculture productivity modifier':'+30% (native education workforce mapping)'},
      treatment='Initialize the missing1970 literacy input once, then use update_literacy_rate. Native education already calculates research, skills and costs. Proposed35% is a balance placeholder, not a verified historical statistic.'),
 dict(id=PREFIX+'spirit_patronage',label='Patronage and Parallel Chains of Command',owner='National situation',
      description='Personal networks and competing civilian, security and military authorities obstruct administration. This is not a claim that every Iraqi institution was equally dysfunctional.',
      modifiers=mods(admin=.10,tax=-.06,org=-.05),
      treatment='Civil service audit and command reforms address distinct components; no duplicated native corruption-tier penalty or free blanket corruption removal.'),
 dict(id=PREFIX+'spirit_frontier',label='The Shatt al-Arab Dispute',owner='Conditional frontier situation',
      description='The border and navigation dispute with Iran worsened in 1969. It is a diplomatic problem with potential military costs, not an unavoidable future war.',
      modifiers=mods(milcost=.05,influence=-.05),
      treatment='Accepted and fulfilled navigation/border settlement replaces this. Neither the 1975 settlement nor the 1980 invasion is applied at game start.'),
]

def effect_body(n,g):
    parts=[]
    if n['modifiers']:
        parts.append('# Store this earned package once; reconciliation sums implemented, selected and currently eligible packages.')
        parts.append(f'set_country_flag = {n["id"]}_package_earned')
    if n['building']:
        state,building,amount=n['building']
        parts.append(f'# Delivery requires owned AND controlled state {state}, free shared slots and no previous grant.\n{state} = {{ add_building_construction = {{ type = {building} level = {amount} instant_build = yes }} }}')
    if n['army_xp']: parts.append(f'army_experience = {n["army_xp"]}')
    parts.extend(n['instant'])
    for d in n['decisions']: parts.append(f'set_country_flag = {d["id"]}_unlocked # NEW authored decision, fully specified in catalogue')
    if n['replaces']:
        parts.append(f'set_country_flag = {n["id"]}_situation_delivered')
        parts.append(f'{PREFIX}reconcile_situations = yes # NEW component-replacement helper; exact ledger in catalogue')
    return '\n'.join(parts)

def effect_text(n,g):
    body=n['effect_body']; quoted=n['id']+'_invoice'; done=n['id']+'_implemented'
    lines=['# APPROVAL SPECIMEN. Native effects below; NEW reconcilers are not existing MD APIs.',
           'if = {',f'\tlimit = {{ NOT = {{ has_country_flag = {done} }} }}']
    if n['budget_gdp_share']:
        lines += ['\tif = {',f'\t\tlimit = {{ NOT = {{ has_country_flag = {quoted}_frozen }} }}',
                  f'\t\tset_variable = {{ {quoted} = gdp_total }}',
                  f'\t\tmultiply_variable = {{ {quoted} = {n["budget_gdp_share"]:g} }}']
        if n['building_price_floor']:
            lines += [f'\t\tclamp_variable = {{ var = {quoted} min = {n["building_price_floor"]:g} }}']
        lines += [f'\t\tset_country_flag = {quoted}_frozen','\t}']
    limits=[n['available']]
    if n['budget_gdp_share']: limits.append(f'check_variable = {{ var = treasury value = {quoted} compare = greater_than_or_equals }}')
    if n['building']:
        state,building,count=n['building']
        limits.append(f'{state} = {{ is_owned_and_controlled_by = IRQ free_building_slots = {{ building = {building} size > {count-1} include_locked = no }} }}')
    lines += ['\tif = {','\t\tlimit = {']+['\t\t\t'+v for v in limits]+['\t\t}']
    if n['budget_gdp_share']:
        lines += [f'\t\tset_temp_variable = {{ treasury_change = {quoted} }}',
                  '\t\tmultiply_temp_variable = { treasury_change = -1 }','\t\tmodify_treasury_effect = yes']
    lines += ['\t\t'+v for v in body.splitlines()]
    lines += [f'\t\tset_country_flag = {done}',f'\t\tclr_country_flag = {n["id"]}_pending']
    if n['modifiers']: lines += ['\t\tCOLDWAR_IRQ_reconcile_programmes = yes # NEW helper; after implemented flag, no one-time grants']
    lines += [
              '\t}', '\telse = {',f'\t\tset_country_flag = {n["id"]}_pending','\t}','}']
    return '\n'.join(lines)

def requirement_code(text):
    direct={
      'Actual active war involving Iraq':'has_war = yes',
      'IRQ owns and controls state165; one-time surveyed resource grant':'165 = { is_owned_and_controlled_by = IRQ }',
      'Actual active war against Iran':'has_war_with = PER',
      'Recorded Iraqi-Iranian war participation':'has_country_flag = COLDWAR_IRQ_iran_first_war_seen',
      'Iran owns Khuzestan; Iraq is independent, outside Irans faction and not at war with Iran':'country_exists = PER is_subject = no NOT = { has_war_with = PER } NOT = { is_in_faction_with = PER } PER = { owns_state = 399 }',
      'Iraq holds the Khuzestan claim; no live accepted Iran border settlement':'399 = { is_claimed_by = IRQ } NOT = { has_country_flag = COLDWAR_IRQ_live_iran_border_settlement }',
      'Iraq controls Khuzestan':'controls_state = 399',
      'Iraq owns and controls Khuzestan':'399 = { is_owned_and_controlled_by = IRQ }',
      'Iraq owns and controls Khuzestan; it remains a non-core':'399 = { is_owned_and_controlled_by = IRQ NOT = { is_core_of = IRQ } }',
      'Iraq owns and controls Khuzestan with infrastructure at least3':'399 = { is_owned_and_controlled_by = IRQ infrastructure > 2 }',
      'Iraq owns and controls Khuzestan and is at peace with Iran':'399 = { is_owned_and_controlled_by = IRQ } NOT = { has_war_with = PER }',
      'Iraq has fought Iran continuously for at least90days':'has_war_with = PER has_country_flag = { flag = COLDWAR_IRQ_iran_current_war_start days > 89 }',
      'Iraq has fought Iran continuously for at least180days':'has_war_with = PER has_country_flag = { flag = COLDWAR_IRQ_iran_current_war_start days > 179 }',
      'Khuzestan is eligible for Iraqi core integration':'399 = { is_owned_and_controlled_by = IRQ NOT = { is_core_of = IRQ } infrastructure > 2 NOT = { compliance < 60 } resistance < 15 } NOT = { has_war_with = PER } has_country_flag = { flag = COLDWAR_IRQ_khuzestan_hold_since days > 729 }',
    }
    if text in direct: return direct[text]
    slug=re.sub('[^a-z0-9]+','_',text.lower()).strip('_')[:72]
    return 'has_country_flag = '+PREFIX+'condition_'+slug

def topic_icon(entry,group,index):
    if entry['icon']:return entry['icon']
    if index==0:return group['icon']
    title=entry['title'].lower()
    rules=[
      (('literacy','teacher','school','education'),'focus_generic_education'),
      (('university','universities','college','technical','laborator'),'generic_university'),
      (('court','judicial','legal','rights','citizenship','constitution'),'focus_generic_court'),
      (('budget','accounts','tax ','finance','credit','debt','treasury','repay','revenue','balance sheet'),'balance_buget'),
      (('treaty','talks','negotiat','accord','conference','diplomacy','cooperation','charter','relations'),'diplomatic_treaty'),
      (('navy','naval','coastal','fleet','ship','dockyard'),'naval_upgrade'),
      (('logistic','supply','fuel','maintenance','procurement'),'focus_generic_supply_line'),
      (('oil','petroleum','refin','concession','export'),'oil_production2'),
      (('rural','agri','irrig','water','grain','field','peasant','marsh','land claims'),'economic_water_supply'),
      (('road','route','infrastructure','grid'),'economic_railroads'),
      (('clinic','medical','welfare','social guarantee','veteran','social bargain','services','housing','women'),'welfare'),
      (('army','force','officer','guard','promotion','defence','armed','war','security'),'army_reform'),
      (('industry','industrial','factory','enterprise','workshop','production','public works'),'crane_and_tower'),
      (('elect','congress','mandate'),'Election_graphics'),
      (('civil','council','party','cabinet','presiden','register','leader','politic','member'),'government_beu'),
    ]
    return next((icon for terms,icon in rules if any(term in title for term in terms)),group['icon'])

def signed(value,unit):
    if unit=='%': return f'{value*100:+g}%'
    return f'{value:+g}{unit}'

def build():
    authored_content()
    # Current user correction: major historical parties/leaders, not a catalogue
    # of hypothetical communist secretaries. No extra governing programmes for
    # Zaki/Amir/Nuri/Central Command are emitted.
    order=['state','baath','bakr','saddam','officers','nasserist','communists','aziz','civic','monarchy','foreign',
           'kurds','puk','dawa','sciri','sunni','oil','industry','agriculture','society','defence','war','iran_war']
    selected={g['id']:g for g in GROUPS}
    GROUPS[:]=[selected[k] for k in order]
    aliases=json.loads((HERE/'short_titles.json').read_text(encoding='utf-8'))
    nodes=[]; decisions=[]; groups=[]
    for gi,g in enumerate(GROUPS):
        g['icon']={'baath':'baathist_iraq','bakr':'baathist_iraq','saddam':'COLDWAR_IRQ_saddam_leadership',
                   'communists':'IRQ_iraq_communism','aziz':'IRQ_iraq_communism','zaki':'IRQ_iraq_communism',
                   'amir':'IRQ_iraq_communism','nuri':'IRQ_iraq_communism',
                   'monarchy':'home_defense','officers':'army_reform','defence':'army_reform'}.get(g['id'],g['icon'])
        # Two Russia-like horizontal tiers; every group reserves its entire 8-unit footprint.
        gx=4+(gi%11)*8; gy=2+(gi//11)*13
        if g['id']=='iran_war':gx,gy=94,15
        ids=[PREFIX+e['key'] for e in g['entries']]
        geometry=[(dx,dy,[list(row) for row in pre]) for dx,dy,pre in FAN]
        variant='compact'
        if g['id'] in ['baath','communists','oil','agriculture','civic']:
            geometry=[(dx+1 if j else 0,dy,pre) for j,(dx,dy,pre) in enumerate(geometry)];variant='right-offset'
        elif g['id'] in ['bakr','aziz','puk','dawa','defence']:
            geometry=[(dx-1 if j else 0,dy,pre) for j,(dx,dy,pre) in enumerate(geometry)];variant='left-offset'
        elif g['id'] in ['saddam','monarchy','industry','society','war']:
            geometry=[(dx*2 if j in [1,2,3,4,6,7,8,9] else dx,dy,pre) for j,(dx,dy,pre) in enumerate(geometry)];variant='broad-fork'
        if g['id'] in ['industry','agriculture','society']:
            geometry[17]=(geometry[17][0],9,[[14],[15],[16]])
        if g['id']=='defence':geometry[17]=(geometry[17][0],9,[[14,16],[15]])
        if g['id'] in ['industry','baath','communists','kurds','oil']:
            # Funded or negotiated delivery stays on a side spur. A refused
            # contract never vetoes all later domestic institutional work.
            cx=geometry[5][0]
            geometry[3]=(cx-3,2,[[1]]);geometry[4]=(cx+3,2,[[2]])
            if g['id']=='industry':geometry[3]=(-2,2,[[1]])
            geometry[5]=(cx,2,[[1,2]])
            geometry=[(dx,dy-1 if j>5 else dy,pre) for j,(dx,dy,pre) in enumerate(geometry)]
            variant='institutional-delivery-spurs'
        if g['id'] in ['oil','agriculture','puk','civic']:
            cx=geometry[10][0];cy=geometry[8][1]
            geometry[8]=(cx-3,cy,[[6]]);geometry[9]=(cx+3,cy,[[7]])
            geometry[10]=(cx,cy,[[6,7]])
            geometry=[(dx,dy-1 if j>10 else dy,pre) for j,(dx,dy,pre) in enumerate(geometry)]
            variant='conditional-delivery-spurs'+(' / two stages' if g['id']=='oil' else '')
        if g.get('geometry'):
            geometry=g['geometry'];variant='campaign-spine / optional-credit-spurs / two war doctrines'
        g['shape']=variant
        for j,(e,(dx,dy,pre)) in enumerate(zip(g['entries'],geometry)):
            authored_title=e['title'];short=aliases.get(e['key'],concise(authored_title));short=short[0].upper()+short[1:]
            assert title_width(short)<=143,(e['key'],short,title_width(short))
            n={**e,'id':ids[j],'group':g['id'],'xy':[gx+dx,gy+dy],
               'title':short,'narrative_title':authored_title,'native_title_width':title_width(short),
               'anchor':ids[0] if j else None,'offset':[dx,dy] if j else [gx,gy],
               'prerequisites':[[ids[k] for k in row] for row in pre],
               'mutually_exclusive':([ids[k] for k in g['exclusions'].get(j,[])] if g.get('geometry') else [ids[3-j]] if j in [1,2] else [ids[13-j]] if j in [6,7] else []),
               'days':e['cost']*7,'available':g['gate']+' '+' '.join(requirement_code(r) for r in e['requires']),'ownership':g['ownership'],
               'icon':topic_icon(e,g,j)}
            # A paid prerequisite must have actually delivered, not merely become a completed pending focus.
            for row in n['prerequisites']:
                flags=' '.join('has_country_flag = '+v+'_implemented' for v in row)
                n['available']+=' '+(flags if len(row)==1 else 'OR = { '+flags+' }')
            n['building_price_floor']=0
            n['native_building_reference_price']=BUILDING_REFERENCE_PRICES[n['building'][1]]*n['building'][2] if n['building'] else 0
            # Awarded development remains; emergency or current-contract effects require live qualification.
            n['active_condition']=n['available']
            # Explicit live programme requirements are distinct from one-time delivery gates.
            # Reconciliation still requires this package to be earned and selected.
            if n.get('active_requires'):n['active_condition']=g['gate']+' '+' '.join(requirement_code(r) for r in n['active_requires'])
            n['requirement_contracts']=[{'meaning':r,'proposed_code':requirement_code(r)} for r in e['requires']]
            n['effect_body']=effect_body(n,g)
            n['effect_code']=effect_text(n,g)
            n['reward_summary']=[f'{LABELS[k][0]}: {signed(v,LABELS[k][1])}' for k,v in n['modifiers'].items()]
            n['reward_summary']+=n.get('outcomes',[])
            if n.get('active_requires'):n['reward_summary'].append('Programme modifiers apply only while: '+'; '.join(n['active_requires'])+'. Paid buildings and once-only effects remain delivered.')
            if n['budget_gdp_share']:
                floor=f', minimum {n["building_price_floor"]:g} MD billion (native helper-price reference)' if n['building_price_floor'] else ''
                n['reward_summary'].append(f'One-time invoice: {n["budget_gdp_share"]*100:g}% of current MD GDP{floor}; frozen at first completion attempt and charged only when all delivery checks pass.')
            if n['building']:
                n['reward_summary'].append(f'Funded delivery: {n["building"][2]} {n["building"][1]} in state {n["building"][0]}; owned/control and native capacity checks.')
                n['reward_summary'].append(f'Price calibration proposal: the native2000 helper reference is {n["native_building_reference_price"]:g} MD billion; the separately charged1970 Iraqi project uses the GDP invoice above. No native historical discount is claimed.')
            if n['army_xp']: n['reward_summary'].append(f'Army experience: +{n["army_xp"]}.')
            if n['replaces']: n['reward_summary'].append('Situation improvement: '+n['replaces'])
            if n['instant']: n['reward_summary'].append('Additional one-time effect: see exact effect specimen.')
            if n['decisions']: n['reward_summary'].append('Decisions: '+', '.join(d['label'] for d in n['decisions']))
            for d in n['decisions']: decisions.append({**d,'unlock':n['id'],'group':g['id']})
            nodes.append(n)
        groups.append({k:v for k,v in g.items() if k!='entries'}|{'anchor':ids[0],'xy':[gx,gy]})
    decisions.append(dict(id=PREFIX+'decision_retry_pending',label='Deliver a Pending Programme',pp=0,days=0,
       summary='Available from start when any completed focus has a pending delivery. Select one pending item; recheck its exact government, live contract, ownership/control, native capacity and frozen invoice. Execute its same once-only delivery guard. Failed retry charges nothing. No new quote or duplicated reward.',
       unlock='START',group='state',repeatable=True,cooldown=0,
       proposed_provider=PREFIX+'retry_selected_pending_programme',
       eligibility='IRQ; at least one COLDWAR_IRQ_<focus>_pending flag; chosen focus not yet implemented'))
    for outlook,label,party in [('western','Western',None),('emerging','Emerging',4),('nonaligned','Non-Aligned',None),('nationalist','Nationalist',21)]:
        decisions.append(dict(id=PREFIX+'decision_organize_'+outlook,label='Organize the '+label+' Outlook',pp=55,days=90,
          summary='Available from start without a focus or governing-party requirement. Select an actually registered party of this outlook; a completed campaign supplies native +3-point party-support and +3-point outlook inputs, followed by MD normalization. Final gains follow the native array calculation. Costs55PP;180day cooldown. Does not install a government. Western/Non-Aligned historical parties require approved roster registration.',
          unlock='START',group='state',repeatable=True,cooldown=180,outlook=outlook,known_party_slot=party,
          effect_code='set_temp_variable = { party_index = COLDWAR_IRQ_selected_registered_party }\nset_temp_variable = { party_popularity_increase = 0.03 }\nset_temp_variable = { temp_outlook_increase = 0.03 }\nchange_relative_party_popularity = yes\nset_temp_variable = { temp_outlook_increase = 0 }',
          proposed_provider=PREFIX+'selected_registered_party'))
    data={'status':'CONCEPT — APPROVAL REQUIRED; no game files changed','country':'IRQ','scenario':'1970-01-01',
          'language':'English','groups':groups,'nodes':nodes,'decisions':decisions,'starting_spirits':SPIRITS,
          'layout':{'x_unit':96,'y_unit':130,'node_width':165,'node_height':128,'font':'Native hoi_16mbs UbuntuBold16 atlas and glyph advances; all titles <=143px inside native147px text region',
                    'initial_focus':PREFIX+'bakr_presidency','continuous_focus_position':{'x':0,'y':4300},
                    'shortcuts':['state','baath','communists','civic','kurds','oil','defence','foreign','iran_war']},
          'modifier_labels':LABELS}
    data['programme_rules']={
      'stability_cap':0.15,
      'stability_cap_scope':'min(sum positive active policy contributions, 0.15) + sum negative active policy contributions. Original situation spirits are separate; negative choices remain fully effective above the positive cap.',
      'reconciliation':'Recompute group variables from earned, selected, currently eligible packages; variables are derived caches, not re-awarded one-time effects.',
      'policy_selection':'The original18-focus programmes use two separate selected-policy slots. Iran has two independent explicit choices: Short War versus Sustained War, and Equal Citizenship versus Central State Rule. Its river and Khuzestan demand lanes are compatible. Descendants follow their selected slot; revisions never replay original effects.',
      'funding':'Frozen invoice, pay on valid delivery. Explicit Iraq1970 price proposals use stated GDPshares; native2000 helper prices remain comparison data, not automatic charges. No deposit/refund. Unfunded delivery exposes a start-accessible retry with zero reward; dependent focuses require delivered predecessors. Early oil/agriculture/factory projects are optional funded spurs.',
      'price_calibration':'Native7.5-billion factory price equals229% of the existing Iraqi1970 GDP3.281, so copying it wholesale would obstruct the campaign. GDPshare project quotes are NEW balance proposals using existing treasury/construction APIs; engine budget calibration remains untested. Office-only project gives no free power plant.',
      'party_availability':'Branches remain visible and become unavailable without governing-party/leader qualification; dynamic programmes detach and reattach. Never promise runtime branch disappearance.',
      'iran_campaign':'The Khuzestan claim and conquest goal are unilateral focus rewards, not permission requests to Iran. Declaration is a player action. One-use opening ideas target PER; no permanent global attack bonus is granted. First-war timing, automatic180day attrition, settlement repudiation and paid decision transactions need new authored integration.',
      'khuzestan_integration':'A separate alternate-history integration continuation can grant an Iraqi core after730continuous days of actual ownership/control, peace with Iran, infrastructure3, compliance60+, resistance below15 and a6%GDP invoice. The selected civic/central costs continue while holding the state. No re-awards or removal of other countries cores.',
    }
    from iran_war import IDEAS,idea_specimen,campaign_specimen
    data['iran_war_ideas']=IDEAS
    (OUT/'COLDWAR_IRQ_IRAN_IDEA_SPECIMEN.txt').write_text(idea_specimen(),encoding='utf-8')
    (OUT/'COLDWAR_IRQ_IRAN_CAMPAIGN_SPECIMEN.txt').write_text(campaign_specimen(),encoding='utf-8')
    (OUT/'COLDWAR_IRQ_1970_CONCEPT.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    source_hash=hashlib.sha256((OUT/'COLDWAR_IRQ_1970_CONCEPT.json').read_bytes()).hexdigest()
    index=['# COLDWAR_IRQ — exact layout index','','Approval concept; resolved coordinates are the source of both preview and emitted specimen.','',f'JSON SHA256: `{source_hash}`','','| Area | Root | Full X range | Full Y range | Geometry |','|---|---|---|---|---|']
    byid={n['id']:n for n in nodes}
    for g in groups:
        ns=[n for n in nodes if n['group']==g['id']];xs=[n['xy'][0] for n in ns];ys=[n['xy'][1] for n in ns]
        index.append(f'| {g["label"]} | {g["xy"]} | {min(xs)}..{max(xs)} | {min(ys)}..{max(ys)} | {g["shape"]} |')
    for g in groups:
        index+=['','## '+g['label'],'','| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |','|---|---|---|---|---|---|']
        for n in (n for n in nodes if n['group']==g['id']):
            pre=' AND '.join('('+' OR '.join(byid[v]['title'] for v in row)+')' for row in n['prerequisites']) or 'Entry'
            exc=', '.join(byid[v]['title'] for v in n['mutually_exclusive']) or '—'
            index.append(f'| `{n["id"]}` | {n["title"]} | {n["xy"]} | {n["days"]} | {pre} | {exc} |')
    (OUT/'COLDWAR_IRQ_LAYOUT_INDEX.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
    # Review specimen intentionally outside common/ and history/. Not installable by this script.
    specimen=['# COLDWAR_IRQ CONCEPT ONLY. Effects and new helpers require implementation after approval.','focus_tree = {','\tid = COLDWAR_IRQ_1970_CONCEPT','\tdefault = no','\tcountry = { factor = 0 }','\tinitial_show_position = { focus = COLDWAR_IRQ_bakr_presidency }','\tcontinuous_focus_position = { x = 0 y = 4300 }']
    for key in data['layout']['shortcuts']:
        gg=next(g for g in groups if g['id']==key)
        specimen += ['\tshortcut = {',f'\t\tname = COLDWAR_IRQ_shortcut_{key}',f'\t\ttarget = {gg["anchor"]}','\t\tscroll_wheel_factor = 0.80','\t}']
    for n in nodes:
        specimen += ['\tfocus = {',f'\t\tid = {n["id"]}',f'\t\ticon = {n["icon"]}',f'\t\tx = {n["offset"][0]}',f'\t\ty = {n["offset"][1]}',f'\t\tcost = {n["cost"]}']
        if n['anchor']: specimen += [f'\t\trelative_position_id = {n["anchor"]}']
        filters=['FOCUS_FILTER_POLITICAL']
        if n['budget_gdp_share']:filters.append('FOCUS_FILTER_EXPENDITURE')
        specimen += ['\t\tsearch_filters = { '+' '.join(filters)+' }']
        for row in n['prerequisites']: specimen += ['\t\tprerequisite = { '+' '.join('focus = '+v for v in row)+' }']
        for ex in n['mutually_exclusive']: specimen += [f'\t\tmutually_exclusive = {{ focus = {ex} }}']
        specimen += ['\t\tavailable = { '+n['available']+' }','\t\tcompletion_reward = {',f'\t\t\tlog = "[GetDateText]: [Root.GetName]: Focus {n["id"]}"']
        specimen += ['\t\t\t'+line for line in n['effect_code'].splitlines()]
        specimen += ['\t\t}','\t\tai_will_do = { base = 1 }','\t}']
    specimen += ['}']
    (OUT/'COLDWAR_IRQ_FOCUS_SPECIMEN.txt').write_text('\n'.join(specimen)+'\n',encoding='utf-8')
    mapping=['# COLDWAR_IRQ CONCEPT: variables bind to existing MD modifier keys. Not loaded.',
             '# Recompute caches using each earned package active_condition and selected-policy slot.',
             '# Stability is excluded from these per-group modifiers and combined/capped once below.']
    for g in groups:
        keys=sorted(set(k for n in nodes if n['group']==g['id'] for k in n['modifiers']))
        mapping += [PREFIX+g['id']+'_programme = {','\t# Eligibility must be true now; completed focuses never imply current authority.','\tenable = { '+g['gate']+' }']
        mapping += [f'\t{k} = {PREFIX}{g["id"]}_{k}' for k in keys if k!='stability_factor']
        mapping += ['}']
    mapping += ['COLDWAR_IRQ_active_policy_stability = {','\tenable = { tag = IRQ }','\tstability_factor = COLDWAR_IRQ_active_policy_stability_value','}',
                '# NEW reconcile helper: min(sum positive policy stability,0.15) + sum negative policy stability. Starting spirits stay separate.']
    (OUT/'COLDWAR_IRQ_MODIFIER_SPECIMEN.txt').write_text('\n'.join(mapping)+'\n',encoding='utf-8')
    loc=['l_english:\n# IMPERIA CW — Cold War: iraq 1970 concept English localisation.']
    def localize(key,value): loc.append(' '+key+':0 '+json.dumps(value,ensure_ascii=False))
    for n in nodes:
        localize(n['id'],n['title']);localize(n['id']+'_desc',n['description'])
    for d in decisions:
        localize(d['id'],d['label']);localize(d['id']+'_desc',d['summary'])
    for s in SPIRITS:
        localize(s['id'],s['label']);localize(s['id']+'_desc',s['description'])
    for key,idea in IDEAS.items():
        localize(key,idea['label']);localize(key+'_desc',idea['description'])
    for key in data['layout']['shortcuts']:
        localize('COLDWAR_IRQ_shortcut_'+key,next(g['label'] for g in groups if g['id']==key))
    (OUT/'COLDWAR_IRQ_CONCEPT_l_english.yml').write_text('\n'.join(loc)+'\n',encoding='utf-8-sig')
    print(f'{len(nodes)} focuses; {len(groups)} sections; {len(decisions)} decision designs; {len(SPIRITS)} starting spirits')
    return data

if __name__=='__main__':
    build()
