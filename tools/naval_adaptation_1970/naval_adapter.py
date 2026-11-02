# IMPERIA COLD WAR — Country adaptations of the native generic naval branch.
"""Pure design/host integration plus a bounded writer for the five adapters.

Do not run a broad country compiler to apply this module. The CLI below patches
only marked naval additions against each current tree and writes owned runtime
providers. Country emitters call integrate_tree so later builds retain the graft.
"""
from __future__ import annotations

from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
import sys
from textwrap import indent

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DOC = ROOT / 'docs/design/naval_adaptation_1970_20261025'
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(HERE))
from focus_prerequisite_ui import nodes, field
from naval_adaptation_1970.assets import asset_package

MARKER = '# IMPERIA COLD WAR — Adapted generic naval programmes.\n'
PREFIX = 'COLDWAR_NAVY_'
REMOVED = {'submarines', 'nuclear_submarines', 'submarine_expansion_project',
           'aircraft_carriers', 'light_helicopter_operators'}
IDEAS = {
    'combined_defense_industries_idea': ('combined_military_defense_industries', None),
    'equipment_conversion_efforts_idea': ('weapon_conversion_packages', 730),
    'convoy_production_bonus': ('convoy_and_freighter_production', None),
    'repair_yard_focus': ('improved_repair_facilities', 365),
    'naval_production_bonus4': ('vessel_production', 730),
    'establishing_a_marine_corps_idea': ('establish_a_marine_corps', None),
}


def block(key, body):
    return key + ' = {\n' + indent(body.strip(), '\t') + '\n}'


def walk(items):
    for n in items:
        yield n
        yield from walk(n.children())


def body(text, node):
    return text[text.index('{', node.start) + 1:node.end - 1].strip()


def pretty(text):
    parsed = nodes(text)
    def render(n, level=0):
        pad = '\t' * level
        if n.key == '_bare': return pad + str(n.value)
        lead = n.key + ' ' + n.op + ' '
        if not isinstance(n.value, list): return pad + lead + str(n.value)
        children = n.children()
        if not children: return pad + lead + '{ }'
        if all(not isinstance(c.value, list) for c in children):
            flat = ' '.join(str(c.value) if c.key == '_bare' else c.key + ' ' + c.op + ' ' + str(c.value) for c in children)
            if len(flat) < 110: return pad + lead + '{ ' + flat + ' }'
        return pad + lead + '{\n' + '\n'.join(render(c, level + 1) for c in children) + '\n' + pad + '}'
    return text[:parsed[0].start] + '\n\n'.join(render(n) for n in parsed) + '\n'


@lru_cache(maxsize=1)
def donor():
    path = ROOT / 'common/national_focus/00_generic.txt'
    source = path.read_text(encoding='utf-8-sig')
    tree = next(n for n in nodes(source) if n.key == 'focus_tree')
    fs = {field(n.children(), 'id'): n for n in tree.children() if n.key == 'focus'}
    selected = {'GENERIC_naval_reform'}
    while True:
        additional = {key for key, n in fs.items() if any(c.value in selected for p in n.children() if p.key == 'prerequisite' for c in p.children())}
        if additional <= selected: break
        selected |= additional
    result = {key.removeprefix('GENERIC_'): (source[n.start:n.end], n) for key, n in fs.items() if key in selected}
    assert len(result) == 20, 'Review changed generic naval source before adapting it'
    return result


@lru_cache(maxsize=1)
def profiles():
    result = {p.stem: json.loads(p.read_text(encoding='utf-8')) for p in sorted((HERE / 'profiles').glob('*.json'))}
    assert set(result) == {'USA', 'SOV', 'DDR', 'IRQ', 'UAE'}
    for tag, p in result.items():
        expected = set(donor()) - (REMOVED if p['variant'] == 'coastal' else set())
        assert p['country'] == tag and set(p['titles']) == set(p['descriptions']) == expected
    return result


def ident(tag, key): return PREFIX + tag + '_' + key
def idea_id(tag, key): return ident(tag, 'idea_' + key)


def research(tag, key, categories, uses=2, bonus='.5'):
    return block('add_tech_bonus', f'name = {ident(tag,key)}\nuses = {uses}\nbonus = {bonus}\n' + '\n'.join('category = ' + c for c in categories))


def price_effect(p):
    tag = p['country']; base = PREFIX + tag + '_'
    if p['variant'] == 'coastal':
        amounts = f'set_variable = {{ {base}port_quote = gdp_total }}\nmultiply_variable = {{ {base}port_quote = .002 }}\nset_variable = {{ {base}yard_quote = gdp_total }}\nmultiply_variable = {{ {base}yard_quote = .008 }}'
    else:
        amounts = f'set_variable = {{ {base}port_quote = .5 }}\nset_variable = {{ {base}yard_quote = 7.5 }}'
    amounts += f'\nset_variable = {{ {base}yard_2_quote = {base}yard_quote }}\nmultiply_variable = {{ {base}yard_2_quote = 2 }}'
    return block('if', block('limit', f'tag = {tag}\nexists = yes\nIMP_is_1970_scenario = yes') + '\n' + amounts)


def _replace_ideas(text, tag):
    for original, (key, _) in IDEAS.items():
        text = re.sub(r'\b' + original + r'\b', idea_id(tag, key), text)
    return text


def reward(p, key, raw):
    tag = p['country']; row = nodes(raw)[0]
    value = body(raw, next(n for n in row.children() if n.key == 'completion_reward'))
    value = re.sub(r'(?m)^\s*log\s*=.*$', '', value)
    value = re.sub(r'\bGENERIC_(\w+)\b', lambda m: ident(tag, m[1]), value)
    value = _replace_ideas(value, tag)
    # Research and manufacturing remain real native systems. Future composite
    # factories and 2010 stealth prototypes are not completed by a 1970 focus.
    if key == 'naval_reform':
        value = 'navy_experience = 75\nif = { limit = { has_selected_naval_grand_doctrine = yes } add_mastery = { amount = 30 folder = naval } }\n' + research(tag,key,['CAT_naval_modules'],1) + '\nset_temp_variable = { temp_opinion = 10 }\nchange_maritime_industry_opinion = yes'
    if key == 'composite_industrial_expansion':
        value = research(tag,key,['CAT_industry'],1) + '\n' + research(tag,key+'_marine',['CAT_naval_engines'],1)
    if key == 'stealth_ships':
        value = research(tag,key,['CAT_naval_electronics'])
    if p['variant'] == 'coastal' and key == 'surface_ships':
        value = research(tag,key,['CAT_corvettes','CAT_patrol_boats'])
    package = None
    if key == 'naval_bases': package = asset_package(p,'port')
    if key == 'dockyards': package = asset_package(p,'yard',2 if p['variant'] != 'coastal' else 1)
    if key == 'large_ship_drydocks': package = asset_package(p,'yard')
    if key == 'combined_military_defense_industries':
        package = asset_package(p,'arms')
        value = f'add_ideas = {idea_id(tag,key)}\nset_temp_variable = {{ temp_opinion = 5 }}\nchange_defense_industry_opinion = yes\nchange_maritime_industry_opinion = yes'
    if package:
        if key != 'combined_military_defense_industries':
            value = 'set_temp_variable = { temp_opinion = 5 }\nchange_maritime_industry_opinion = yes'
        return value, package
    return value, None


def gates(p, key):
    public = ['controls_a_coastal_state = yes']
    if key == 'naval_doctrine_innovations': public.append('has_selected_naval_grand_doctrine = yes')
    if key == 'dockyards': public.append('num_of_factories > 0')
    counts = {'submarines':4,'surface_ships':3,'nuclear_submarines':7,'aircraft_carriers':10,'light_helicopter_operators':5,'large_ship_drydocks':5,'improved_repair_facilities':5,'convoy_and_freighter_production':0}
    if key in counts:
        minimum = counts[key] if p['variant'] != 'coastal' else 0
        public.append('num_of_naval_factories > ' + str(minimum))
    if key in ('aircraft_carriers','large_ship_drydocks','improved_repair_facilities') and p['variant'] != 'coastal':
        public.append('has_at_least_major_power_status = yes')
    if key == 'light_helicopter_operators': public.append('has_at_least_regional_power_status = yes')
    return '\n'.join(public)


def parents(p, key, source_node):
    tag = p['country']
    if key == 'naval_reform': return p['parent_groups']
    groups = [[ident(tag,c.value.removeprefix('GENERIC_')) for c in n.children() if c.key == 'focus'] for n in source_node.children() if n.key == 'prerequisite']
    replacements = {
        'combined_military_defense_industries': [['dockyards'],['surface_ships']],
        'composite_industrial_expansion': [['combined_military_defense_industries']],
        'weapon_conversion_packages': [['combined_military_defense_industries']],
        'aircraft_carriers': [['surface_ships'],['naval_doctrine_innovations']],
        'light_helicopter_operators': [['surface_ships'],['naval_doctrine_innovations']],
    }
    if p['variant'] == 'coastal':
        replacements.update(vessel_production=[['surface_ships'],['dockyards']], large_ship_drydocks=[['surface_ships']])
    return [[ident(tag,k) for k in group] for group in replacements[key]] if key in replacements else groups


@lru_cache(maxsize=5)
def build_country(tag):
    p = profiles()[tag]; loc = {}; effects = {}; triggers = {}; focuses = []; records = []; pending = []
    effects[ident(tag,'quote_prices')] = price_effect(p)
    for key, (raw, _) in donor().items():
        if key not in p['titles']: continue
        node = nodes(raw)[0]; children = node.children(); fid = ident(tag,key)
        root = key == 'naval_reform'; x,y = p['anchor'] if root else (field(children,'x'),field(children,'y'))
        groups = parents(p,key,node)
        excludes = [ident(tag,c.value.removeprefix('GENERIC_')) for n in children if n.key == 'mutually_exclusive' for c in n.children() if c.value.removeprefix('GENERIC_') in p['titles']]
        loc[fid] = p['titles'][key]; loc[fid+'_desc'] = p['descriptions'][key]
        actual, asset = reward(p,key,raw)
        done = ident(tag,'done_'+key); receipt = ident(tag,'pending_'+key); ready = ident(tag,'ready_'+key)
        public = gates(p,key)
        real = f'tag = {tag}\nexists = yes\nIMP_is_1970_scenario = yes\nNOT = {{ has_country_flag = {done} }}\n' + public
        for group in groups: real += '\n' + block('OR','\n'.join('has_completed_focus = '+parent for parent in group))
        for other in excludes: real += '\nNOT = { has_completed_focus = '+other+' }'
        availability = block('hidden_trigger',f'tag = {tag}\nIMP_is_1970_scenario = yes\nNOT = {{ has_country_flag = {done} }}') + '\n' + public
        if asset:
            asset_rows = nodes(asset['ready']); capacity = next(n for n in asset_rows if n.key == 'OR')
            cap = ident(tag,'capacity_'+key); triggers[cap] = body(asset['ready'],capacity)
            # Preserve the OR wrapper of eligible sites, not an AND of sites.
            triggers[cap] = block('OR',triggers[cap])
            loc[cap+'_tt'] = ('An owned and controlled coastal province has room for one naval-base level.' if key=='naval_bases' else 'An owned and controlled state has capacity for the complete industrial project.')
            availability += '\n' + block('hidden_trigger',asset['ready'])
            availability += '\n' + block('custom_trigger_tooltip',f'tooltip = {cap}_tt\n{cap} = yes')
            for n in asset_rows:
                if n.key != 'check_variable': continue
                condition = asset['ready'][n.start:n.end]
                if field(n.children(),'var') == 'treasury':
                    funded = ident(tag,'funded_'+key+'_tt')
                    quote = field(n.children(),'value')
                    loc[funded] = 'Treasury: $[?treasury|5] billion; required: $[?'+quote+'|5] billion.'
                    availability += '\n' + block('custom_trigger_tooltip',f'tooltip = {funded}\n'+condition)
            real += '\n' + asset['ready']
            preview = asset['preview'] + '\n' + actual
            actual = asset['execute'] + '\n' + actual
        else: preview = actual
        triggers[ready] = real
        effects[ident(tag,'preview_'+key)] = block('effect_tooltip',preview)
        delivered = actual + f'\nset_country_flag = {done}\nclr_country_flag = {receipt}'
        effects[ident(tag,'complete_'+key)] = block('if', block('limit',f'tag = {tag}\nIMP_is_1970_scenario = yes\nNOT = {{ has_country_flag = {done} }}') + f'\nset_country_flag = {receipt}\n{ident(tag,"quote_prices")} = yes\n' + block('if',block('limit',ready+' = yes')+'\n'+delivered))
        pending.append(block('if',f'limit = {{ has_country_flag = {receipt} }}\n{ident(tag,"complete_"+key)} = yes'))
        cost = p.get('focus_cost',field(children,'cost'))
        fields = [f'id = {fid}',f'icon = {field(children,"icon")}',f'x = {x}',f'y = {y}']
        if not root: fields.append('relative_position_id = '+ident(tag,'naval_reform'))
        fields.append(f'cost = {cost}')
        fields += [block('prerequisite','\n'.join('focus = '+parent for parent in group)) for group in groups]
        if excludes: fields.append(block('mutually_exclusive','\n'.join('focus = '+other for other in excludes)))
        filters=[str(c.value) for n in children if n.key=='search_filters' for c in n.children()]
        if 'FOCUS_FILTER_NAVY' not in filters: filters.append('FOCUS_FILTER_NAVY')
        ai='factor = 2'
        if asset and key != 'combined_military_defense_industries':
            ai+='\nmodifier = { factor = 0 is_ai = yes ai_has_high_deficit = yes }'
        fields += [block('search_filters',' '.join(filters)),block('available',availability),'cancel_if_invalid = yes','continue_if_invalid = no',block('completion_reward',ident(tag,'preview_'+key)+' = yes\n'+block('hidden_effect',ident(tag,'complete_'+key)+' = yes')),block('ai_will_do',ai)]
        focuses.append(block('focus','\n'.join(fields)))
        records.append(dict(id=fid,country=tag,donor='GENERIC_'+key,key=key,name=loc[fid],description=loc[fid+'_desc'],xy=[float(x) if root else p['anchor'][0]+float(x),float(y) if root else p['anchor'][1]+float(y)],cost=str(cost),prerequisites=groups,exclusions=excludes,asset=bool(asset),ready=ready,done=done,pending=receipt,completion=ident(tag,'complete_'+key)))
    effects[ident(tag,'retry_pending')] = '\n'.join(pending)
    loc[ident(tag,'shortcut')] = 'Naval Development'
    return dict(profile=p,focuses=focuses,records=records,loc=loc,effects=effects,triggers=triggers)


def strip_tree(tag, text):
    """Remove only our marked chapter before an owning AST formatter."""
    start=f'# IMPERIA COLD WAR — {tag} naval adaptation BEGIN';end=f'# IMPERIA COLD WAR — {tag} naval adaptation END'
    pattern=r'(?m)^[\t ]*'+re.escape(start)+r'.*?^[\t ]*'+re.escape(end)+r'\n?'
    return re.sub(pattern,'',text,flags=re.S)


def integrate_tree(tag, text):
    """Pure marked append against the current country emitter's output."""
    text=strip_tree(tag,text)
    start=f'# IMPERIA COLD WAR — {tag} naval adaptation BEGIN';end=f'# IMPERIA COLD WAR — {tag} naval adaptation END'
    tree=next(n for n in nodes(text) if n.key=='focus_tree')
    owned=[n for n in tree.children() if n.key=='focus' and str(field(n.children(),'id')).startswith(PREFIX+tag+'_')]
    assert not owned,'Unmarked naval focus IDs would duplicate the graft'
    country=build_country(tag)
    fragment='\n\n'.join(country['focuses'])+'\n'+block('shortcut',f'name = {ident(tag,"shortcut")}\ntarget = {ident(tag,"naval_reform")}\nscroll_wheel_factor = 0.8')
    addition='\n\t'+start+'\n'+indent(pretty(fragment).strip(),'\t')+'\n\t'+end+'\n'
    text=text[:tree.end-1].rstrip()+addition+text[tree.end-1:]
    if not text.startswith('# IMPERIA COLD WAR'):
        text=f'# IMPERIA COLD WAR — {tag} naval adaptation integrated with retained country content.\n'+text
    return text


def _idea_outputs():
    source=(ROOT/'common/ideas/generic_ideas.txt').read_text(encoding='utf-8-sig')
    defs={n.key:n for n in walk(nodes(source)) if n.key in IDEAS}
    assert set(defs)==set(IDEAS)
    definitions=[];loc={}
    for tag,p in profiles().items():
        for original,(key,days) in IDEAS.items():
            content=body(source,defs[original])
            content=re.sub(r'(?m)^\s*name\s*=.*$','',content)
            new=idea_id(tag,key)
            content='name = '+new+'\n'+content
            definitions.append(block(new,content))
            loc[new]=p['titles'][key]
            loc[new+'_desc']=p['descriptions'][key]
    return MARKER+block('ideas',block('country','\n\n'.join(definitions)))+'\n',loc


def runtime_outputs():
    effects={};triggers={};loc={};actions=[]
    ideas,idea_loc=_idea_outputs();loc.update(idea_loc)
    for tag in profiles():
        country=build_country(tag);effects.update(country['effects']);triggers.update(country['triggers']);loc.update(country['loc'])
        calls=ident(tag,'quote_prices')+' = yes\n'+ident(tag,'retry_pending')+' = yes'
        actions.append(block('on_daily_'+tag,block('effect',calls)))
    startup='\n'.join(block(tag,ident(tag,'quote_prices')+' = yes\n'+ident(tag,'retry_pending')+' = yes') for tag in profiles())
    actions.insert(0,block('on_startup',block('effect',startup)))
    return {
        'common/ideas/COLDWAR_NAVY_1970.txt':pretty(ideas),
        'common/scripted_effects/COLDWAR_NAVY_1970.txt':pretty(MARKER+'\n\n'.join(block(k,v) for k,v in effects.items())+'\n'),
        'common/scripted_triggers/COLDWAR_NAVY_1970.txt':pretty(MARKER+'\n\n'.join(block(k,v) for k,v in triggers.items())+'\n'),
        'common/on_actions/COLDWAR_NAVY_1970.txt':pretty(MARKER+block('on_actions','\n\n'.join(actions))+'\n'),
        'localisation/english/COLDWAR_NAVY_1970_l_english.yml':'l_english:\n'+MARKER+'\n'.join(' '+k+':0 '+json.dumps(v,ensure_ascii=False) for k,v in loc.items())+'\n'
    }


def write(path,text):
    target=ROOT/path;data=text.encode('utf-8-sig' if path.endswith('.yml') else 'utf-8')
    if target.exists() and target.read_bytes()==data:return False
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data);return True


def compile_all():
    changed=[]
    for tag,p in profiles().items():
        path=p['tree_file'];text=(ROOT/path).read_text(encoding='utf-8-sig')
        if write(path,integrate_tree(tag,text)):changed.append(path)
    for path,text in runtime_outputs().items():
        if write(path,text):changed.append(path)
    manifest=dict(project='IMPERIA COLD WAR',donor='common/national_focus/00_generic.txt',donor_sha256=hashlib.sha256((ROOT/'common/national_focus/00_generic.txt').read_bytes()).hexdigest(),registered_new_focuses=sum(len(build_country(t)['records']) for t in profiles()),countries={t:build_country(t)['records'] for t in profiles()},owned_runtime=list(runtime_outputs()),scope='Copied native generic maritime structure with 1970 and national adaptations. No OOB, ship formation, foreign offer or politics is created.')
    write('tools/naval_adaptation_1970/manifest.json',json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(project='IMPERIA COLD WAR',focuses=manifest['registered_new_focuses'],changed=changed),indent=2))


if __name__=='__main__':compile_all()
