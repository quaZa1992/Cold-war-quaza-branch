# IMPERIA COLD WAR — COMECON native contract compiler
"""Compile the approved dossier into bounded, authoritative native contracts."""
import json
import re
import sys
from pathlib import Path

if __name__ == '__main__':
    sys.modules['build'] = sys.modules[__name__]

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MARK = '# IMPERIA COLD WAR — COMECON'
DATA = json.loads((HERE/'catalogue.json').read_text(encoding='utf-8'))
PROJECTS = list(DATA['catalogue'])
OFFERS = [(p,o) for p in PROJECTS for o in DATA['agreements'][p]]
TIERS = ('Limited','Standard','Major')
FOUNDERS = ('SOV','HUN','DDR','CZE','POL','BUL','ROM','MON')
SSRS = ('UKR','BLR','EST','LAT','LIT','ARM','AZE','GEO','KAZ','KYR','TAJ','TRK','UZB','MLV')
BUILDINGS = {'civilian factory':'industrial_complex','infrastructure level':'infrastructure',
             'agricultural district level':'agriculture_district','office':'offices','supply hub':'supply_node'}
HOST_KEYS = {'fossil power plant fuel consumption':'fossil_pp_fuel_consumption_modifier',
             'state productivity growth':'state_productivity_growth_modifier',
             'civilian industry construction speed':'production_speed_industrial_complex_factor'}
LOCS = {}
OUTPUTS = []

def n(x):
    return f'{x:.5f}'.rstrip('0').rstrip('.') if isinstance(x,float) else str(x)

def loc(key,value):
    LOCS[key] = value.replace('–','-').replace('—','-').replace('\n','\\n')
    return key

def write(rel,text):
    if rel.endswith(('.txt','.gui','.gfx','.yml')):
        text=re.sub(r'\bcc_[A-Za-z0-9_-]+',lambda match:match[0].replace('-','_'),text)
    if rel.endswith(('.txt','.gui','.gfx')):
        depth=0
        for token in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]',text):
            if token[0]=='{':depth+=1
            elif token[0]=='}':depth-=1
            assert depth>=0,(rel,'Unexpected close',text.count('\n',0,token.start())+1)
        assert depth==0,(rel,'Unclosed block',depth)
    p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(text.rstrip()+'\n',encoding='utf-8-sig' if rel.endswith('.yml') else 'utf-8')
    OUTPUTS.append(rel)

def block(key,body):return key+' = {\n'+body+'\n}\n'
def var(key,value):return f'set_variable = {{ {key} = {n(value)} }}'
def flag(key):return f'has_country_flag = {key}'
def cv(key,op,value):return f'check_variable = {{ {key} {op} {n(value)} }}'
def choose(key,value,body):return f'if = {{ limit = {{ {cv(key,"=",value)} }} {body} }}'
def ident(index,tier):return f'cc_terms_{index}_{tier+1}'

def offer_effects(p,o,t,host=False):
    """Signed native modifiers and category research. State effects stay in states."""
    mods={};research={};states=0
    if host and o['kind']!='shared' and not o.get('all'):
        h=DATA['hostPlans'][p]
        if h.get('research'):research[h['research']]=[15,25,35][t]
        if h.get('programme'):
            pr=h['programme'];mods[HOST_KEYS[pr['effect']]]=pr['values'][t]/100
            states=pr.get('states',[0,0,0])[t]
        if not o.get('includeHost'):return mods,research,states
    if o['kind']=='research':research[o['category']]=o['values'][t]
    if o['kind'] in ('modifier','shared','resource'):
        for e in o['effects']:mods[e['nativeKey']]=e['values'][t]/(100 if e['unit']=='%' else 1)
        states=o.get('states',[0,0,0])[t]
        if o.get('research'):research[o['research']['category']]=o['research']['values'][t]
    return mods,research,states

RESEARCH_CATS={'Industry':'CAT_industry','Agriculture':'CAT_agriculture','Computing':'CAT_computing',
 'Construction':'CAT_construction','Infrastructure':'CAT_infrastructure','Electrification':'CAT_electrification',
 'Excavation':'CAT_excavation','Civilian Reactor':'CAT_nuclear_reactors'}
MOD_KEYS=sorted({k for p,o in OFFERS for t in range(3) for h in (False,True)
                 for k in offer_effects(p,o,t,h)[0] if k!='state_productivity_growth_modifier'})

def host_builds(p,o,t):
    if o['kind']=='shared' or o.get('all'):return []
    return [(BUILDINGS[b['one']],b['levels'][t]) for b in DATA['hostPlans'][p]['buildings']]

def base_assets(p,o,t,host=False):
    return host_builds(p,o,t) if host else [('infrastructure',o['levels'][t])] if o['kind']=='building' else []

def ideas():
    out=[MARK+' membership and exact agreement previews','ideas = { country = {',
      'cc_member = { picture = cc_emblem allowed = { always = no } removal_cost = -1 }']
    loc('cc_member','Council for Mutual Economic Assistance')
    loc('cc_member_desc','Membership of the Council provides access to joint investment and technical co-operation agreements. Contributions and participation require national approval.')
    for i,(p,o) in enumerate(OFFERS,1):
        for t in range(3):
            for host in (False,True):
                key=ident(i,t)+('_host' if host else '')
                mods,research,states=offer_effects(p,o,t,host)
                out.append(f'{key} = {{ picture = cc_emblem allowed = {{ always = no }} removal_cost = -1')
                country_mods={k:v for k,v in mods.items() if k!='state_productivity_growth_modifier'}
                if country_mods:out.append('modifier = { '+' '.join(k+' = '+n(v) for k,v in country_mods.items())+' }')
                if research:out.append('research_bonus = { '+' '.join(RESEARCH_CATS[k]+' = '+n(v/100) for k,v in research.items())+' }')
                out.append('}')
                loc(key,o['name']+' - '+TIERS[t]+(' Host Programme' if host else ' Programme'))
                loc(key+'_desc',DATA['catalogue'][p]['description'])
    # Actual research support is strongest-per-category, independently from preview spirits.
    for category,key in RESEARCH_CATS.items():
        for amount in (10,15,20,25,35,50):
            slug=f'cc_research_{key}_{amount}'
            out.append(f'{slug} = {{ picture = cc_emblem allowed = {{ always = no }} removal_cost = -1 research_bonus = {{ {key} = {n(amount/100)} }} }}')
            loc(slug,category+' Research Co-operation')
    out.append('} }');write('common/ideas/ICW_COMECON.txt','\n'.join(out))
    dynamic=[MARK+' strongest active programme modifiers','cc_programmes = { icon = GFX_cc_emblem enable = { always = yes }']
    dynamic += [f'{key} = cc_mod_{key}' for key in MOD_KEYS]
    dynamic.append('}')
    dynamic.append('cc_state_programmes = { icon = GFX_cc_emblem enable = { always = yes } state_productivity_growth_modifier = cc_state_growth }')
    for value in (10,15,20):
        dynamic.append(f'cc_state_preview_{value} = {{ icon = GFX_cc_emblem state_productivity_growth_modifier = {n(value/100)} }}')
        loc(f'cc_state_preview_{value}','COMECON Plant Modernisation')
    write('common/dynamic_modifiers/ICW_COMECON.txt','\n'.join(dynamic))
    loc('cc_programmes','COMECON Technical Programmes');loc('cc_state_programmes','COMECON Plant Modernisation')

def site_capacity(buildings):
    out=[]
    for b,count in buildings:
        if b=='infrastructure':out.append(f'infrastructure < {7-count}')
        elif b=='supply_node':out.append('cc_hub_site_valid = yes')
        else:out.append(f'free_building_slots = {{ building = {b} size > {count-1} include_locked = no }}')
    return ' '.join(out)

def target_conditions(s,p,o,t,host=False,assets=True):
    out=['exists = yes']
    mods,research,states=offer_effects(p,o,t,host)
    b=base_assets(p,o,t,host)
    if b and assets:
        sector='agriculture_district > 0' if p=='agromash' and host else ''
        out += ['NOT = { '+cv(f'cc_{s}_site1','=',0)+' }',f'var:cc_{s}_site1 = {{ is_owned_by = PREV is_controlled_by = PREV {site_capacity(b)} {sector} }}']
    if (not host or o.get('includeHost')) and o['kind']=='resource' and assets:
        out += ['NOT = { '+cv(f'cc_{s}_site1','=',0)+' }',f'var:cc_{s}_site1 = {{ is_owned_by = PREV is_controlled_by = PREV has_resources_amount = {{ resource = steel amount > 0 }} NOT = {{ has_state_flag = cc_steel_developed }} }}']
    for j in range(1,states+1):
        sector='agriculture_district > 0' if p=='agromash' else 'industrial_complex > 0'
        out += ['NOT = { '+cv(f'cc_{s}_site{j}','=',0)+' }',f'var:cc_{s}_site{j} = {{ is_owned_by = PREV is_controlled_by = PREV {sector} }}']
        for k in range(1,j):out.append(f'NOT = {{ {cv(f"cc_{s}_site{j}","=",f"cc_{s}_site{k}")} }}')
    if o['id']=='operator-safety':out += ['COLDWAR_nuc_player_programme = yes']
    if o['kind']=='equipment' and host:out += ['is_ai = no']
    if o['id']=='fuel-services':out += ['check_variable = { nuclear_reactors > 0 }','has_tech = mdcw_reactor_fuel_fabrication_1953']
    if o['id']=='reactor-support':out += ['OR = { has_tech = reactor1 has_country_flag = COLDWAR_turnkey_reactor_operator }']
    if any(k in mods for k in ['production_lack_of_resource_penalty_factor','production_factory_efficiency_gain_factor','production_factory_max_efficiency_factor']):out += ['num_of_military_factories > 0','OR = { is_ai = yes has_country_flag = cc_military_annex }']
    if 'agriculture_district_income_tax_modifier' in mods:out.append('any_owned_state = { agriculture_district > 0 }')
    if 'civilian_factories_productivity' in mods:out.append('num_of_civilian_factories > 0')
    if any('fossil' in k for k in mods):out.append('any_owned_state = { fossil_powerplant > 0 }')
    return ' '.join(out)

def triggers():
    from governance import compile_triggers
    write('common/scripted_triggers/ICW_COMECON.txt',compile_triggers())


def set_max(key,value):
    op='>' if value>0 else '<'
    return f'if = {{ limit = {{ NOT = {{ check_variable = {{ {key} {op} {n(value)} }} }} }} {var(key,value)} }}'

def refresh_effect():
    out=[]
    out += [var('cc_weekly_gdp',0),var('cc_weekly_fixed',0)]
    out += [var('cc_mod_'+k,0) for k in MOD_KEYS]
    for key in RESEARCH_CATS.values():
        out.append(var('cc_research_'+key,0))
        out.append('remove_ideas = { '+' '.join(f'cc_research_{key}_{v}' for v in (10,15,20,25,35,50))+' }')
    out.append('for_each_scope_loop = { array = cc_effect_states set_variable = { cc_state_growth = 0 } if = { limit = { has_dynamic_modifier = { modifier = cc_state_programmes } } remove_dynamic_modifier = { modifier = cc_state_programmes } } } clear_array = cc_effect_states')
    for s in range(1,5):
        choices=[]
        for i,(p,o) in enumerate(OFFERS,1):
            for t in range(3):
                branches=[]
                for host in (True,False):
                    mods,research,states=offer_effects(p,o,t,host)
                    effects=[]
                    for key,value in mods.items():
                        if key!='state_productivity_growth_modifier':effects.append(set_max('cc_mod_'+key,value))
                        else:
                            for j in range(1,states+1):
                                effects.append(f'var:cc_{s}_site{j} = {{ {set_max("cc_state_growth",value)} }} if = {{ limit = {{ NOT = {{ is_in_array = {{ array = cc_effect_states value = cc_{s}_site{j} }} }} }} add_to_array = {{ cc_effect_states = cc_{s}_site{j} }} }}')
                    for category,value in research.items():effects.append(set_max('cc_research_'+RESEARCH_CATS[category],value))
                    specialist=o['kind'] in ('modifier','resource','shared')
                    host_programme=host and bool(DATA['hostPlans'].get(p,{}).get('programme'))
                    national=(specialist and (not host or o['kind']=='shared' or o.get('includeHost'))) or host_programme
                    if national:effects.append(f'add_to_variable = {{ cc_weekly_gdp = {n([.00006,.00010,.00016][t])} }}')
                    if host and not DATA['catalogue'][p].get('campaign') and (specialist or host_programme):effects.append(f'add_to_variable = {{ cc_weekly_fixed = {n([.012,.020,.032][t])} }}')
                    effects=[f'if = {{ limit = {{ is_ai = no }} {e} }}' if e.startswith('add_to_variable = { cc_weekly_') else e for e in effects]
                    branches.append(('if' if host else 'else')+' = { '+(f'limit = {{ {cv("THIS.id","=",f"global.cc_{s}_host")} }} ' if host else '')+' '.join(effects)+' }')
                choices.append(choose(f'global.cc_{s}_offer',i,choose(f'global.cc_{s}_tier',t+1,' '.join(branches))))
        out.append(f'if = {{ limit = {{ has_country_flag = cc_{s}_beneficiary check_variable = {{ global.cc_{s}_operating = 1 }} }} '+'\n'.join(choices)+' }')
    for key in RESEARCH_CATS.values():
        for value in (10,15,20,25,35,50):out.append(choose('cc_research_'+key,value,f'add_ideas = cc_research_{key}_{value}'))
    any_mod='OR = { '+' '.join(f'NOT = {{ check_variable = {{ cc_mod_{key} = 0 }} }}' for key in MOD_KEYS)+' }'
    out.append('if = { limit = { '+any_mod+' } if = { limit = { NOT = { has_dynamic_modifier = { modifier = cc_programmes } } } add_dynamic_modifier = { modifier = cc_programmes } } } else_if = { limit = { has_dynamic_modifier = { modifier = cc_programmes } } remove_dynamic_modifier = { modifier = cc_programmes } }')
    out.append('for_each_scope_loop = { array = cc_effect_states if = { limit = { check_variable = { cc_state_growth > 0 } } add_dynamic_modifier = { modifier = cc_state_programmes } } }')
    out.append('cc_calculate_weekly_expense = yes update_money_dirty_variable = yes')
    return block('cc_refresh_country','\n'.join(out))

def assets(s,p,o,t,host=False,preview=False):
    b=base_assets(p,o,t,host);out=[]
    if b:
        effects=[f'add_extra_state_shared_building_slots = {sum(v for _,v in b)}']
        for building,count in b:
            if building=='supply_node':effects.append('cc_preview_hub = yes' if preview else 'cc_build_hub = yes')
            else:effects.append(f'add_building_construction = {{ type = {building} level = {count} instant_build = yes }}')
        out.append(f'var:cc_{s}_site1 = {{ '+' '.join(effects)+' }')
    if o['kind']=='resource' and (not host or o.get('includeHost')):
        out.append(f'var:cc_{s}_site1 = {{ add_resource = {{ type = steel amount = 1 }} '+('' if preview else 'set_state_flag = cc_steel_developed')+' }')
    if o['kind']=='equipment':
        if preview:
            amount=f'global.cc_{s}_train_negative' if host else f'cc_{s}_train_quota'
            out.append(f'add_equipment_to_stockpile = {{ type = mdcw_steam_train_equipment_1940 amount = {amount} }}')
        elif not host:
            out.append(f'var:global.cc_{s}_host = {{ send_equipment = {{ equipment = mdcw_steam_train_equipment_1940 amount = PREV.cc_{s}_train_quota target = PREV }} }}')
    mods,research,states=offer_effects(p,o,t,host)
    if preview and states:
        value=round(mods['state_productivity_growth_modifier']*100)
        out += [f'var:cc_{s}_site{j} = {{ add_dynamic_modifier = {{ modifier = cc_state_preview_{value} days = 90 }} }}' for j in range(1,states+1)]
    if preview:
        specialist=o['kind'] in ('modifier','resource','shared')
        host_programme=host and bool(DATA['hostPlans'].get(p,{}).get('programme'))
        national=(specialist and (not host or o['kind']=='shared' or o.get('includeHost'))) or host_programme
        if national:
            out.append(f'if = {{ limit = {{ is_ai = no }} add_to_variable = {{ cc_preview_gdp = {n(-[.00006,.0001,.00016][t])} tooltip = cc_weekly_gdp_tt }} }}')
        if host and not DATA['catalogue'][p].get('campaign') and (specialist or host_programme):out.append(f'if = {{ limit = {{ is_ai = no }} add_to_variable = {{ cc_preview_weekly = {n(-[.012,.020,.032][t])} tooltip = cc_weekly_support_tt }} }}')
        out.append('add_to_variable = { cc_preview_days = '+('180' if DATA['catalogue'][p].get('campaign') else '90')+' tooltip = cc_active_days_tt }')
    return ' '.join(out)

def native_previews():
    out=[]
    for s in range(1,5):
        body=[]
        for i,(p,o) in enumerate(OFFERS,1):
            for t in range(3):
                hostassets=assets(s,p,o,t,True,True)
                partnerassets=assets(s,p,o,t,False,True)
                effect=f'if = {{ limit = {{ hidden_trigger = {{ {cv("THIS.id","=",f"global.cc_{s}_host")} }} }} add_ideas = {ident(i,t)}_host {hostassets} }} else = {{ add_ideas = {ident(i,t)} {partnerassets} }}'
                body.append(f'if = {{ limit = {{ hidden_trigger = {{ {cv(f"global.cc_{s}_offer","=",i)} {cv(f"global.cc_{s}_tier","=",t+1)} }} }} {effect} }}')
        out.append(block(f'cc_{s}_preview_self','effect_tooltip = { '+'\n'.join(body)+' }'))
        from mechanics import participants,recipients
        out.append(block(f'cc_{s}_preview_all','effect_tooltip = { '+participants(s,f'if = {{ limit = {{ cc_human_member = yes }} add_to_variable = {{ cc_preview_weekly = cc_{s}_weekly_negative tooltip = cc_weekly_cost_tt }} }}')+' '+recipients(s,f'cc_{s}_preview_self = yes')+' }'))
    return '\n'.join(out)

def main():
    ideas();triggers()
    effects=[MARK+' native contracts and fiscal lifecycle',refresh_effect(),native_previews()]
    effects.append(block('cc_touch','cc_refresh_open_views = yes add_to_variable = { global.cc_dirty = 1 }'))
    effects.append(block('cc_calculate_weekly_expense','set_variable = { cc_weekly_expenses = 0 } if = { limit = { is_ai = no } set_variable = { cc_weekly_expenses = gdp_total } multiply_variable = { cc_weekly_expenses = cc_weekly_gdp } add_to_variable = { cc_weekly_expenses = cc_weekly_fixed } }'))
    from mechanics import compile_mechanics
    compile_mechanics(effects)
    write('common/scripted_effects/ICW_COMECON.txt','\n'.join(effects))
    from native_ui import compile_ui
    compile_ui()
    from assets import build_assets
    build_assets()
    # Integrate only this stream; retain all concurrent USA and main-MD changes.
    money=ROOT/'common/scripted_effects/00_money_system.txt'
    source=money.read_text(encoding='utf-8-sig')
    marker='# IMPERIA COLD WAR — COMECON weekly national programme expenses'
    if marker not in source:
        needle='calculate_additional_expense_rate = {\n\tset_variable = { additional_expenses_rate = 0 }'
        assert source.count(needle)==1
        source=source.replace(needle,needle+'\n\t'+marker+'\n\tcc_calculate_weekly_expense = yes\n\tadd_to_variable = { additional_expenses_rate = cc_weekly_expenses }',1)
        money.write_text(marker+' integration.\n'+source,encoding='utf-8')
    alerts=ROOT/'interface/alerts.gui';source=alerts.read_text(encoding='utf-8-sig')
    marker='# IMPERIA COLD WAR — COMECON toolbar space beside the European Communities button.'
    if not source.startswith(marker+'\n'):
        source=marker+'\n'+source.replace('x = 723 y = 40','x = 779 y = 40',1).replace('x = 786 y = 40','x = 835 y = 40',1)
        alerts.write_text(source,encoding='utf-8')
    write('localisation/english/ICW_COMECON_l_english.yml','l_english:\n'+MARK+' English presentation\n'+'\n'.join(f' {k}:0 "{v.replace(chr(34),chr(39))}"' for k,v in LOCS.items()))
    report={'project':'IMPERIA COLD WAR','offers':len(OFFERS),'projects':len(PROJECTS),'slots':4,'generated':OUTPUTS,'integrations':['common/scripted_effects/00_money_system.txt','interface/alerts.gui']}
    write('tools/comecon/generated.json',json.dumps(report,indent=2))
    print(json.dumps({'generated':len(OUTPUTS),'offers':len(OFFERS),'slots':4}))

if __name__=='__main__':main()
