# IMPERIA COLD WAR — compile the approved universal SSR focus programme.
"""Owned SSR outputs and narrow, idempotent integration patches only."""
from pathlib import Path
import hashlib,json,re,sys
import shared
import art

ROOT=shared.ROOT
HERE=shared.HERE
sys.path.insert(0,str(ROOT/'tools'))
from building_grants.grants import rewrite_queries as _grant_queries, runtime_outputs as _grant_runtime

TREE='COLDWAR_SSR_1970_focus'
P='COLDWAR_SSR_'
LOC={}
OUTPUTS=[]
D=shared.data()
NODES=shared.nodes()
BY={n['id']:n for n in NODES}
NUMBERS=set(D['number_keys'])

def block(name,body):return name+' = {\n'+indent(body)+'\n}'
def indent(body):return '\n'.join('\t'+line if line else '' for line in body.splitlines())
def join(parts):return '\n'.join(v for v in parts if v)
def num(value):return shared.number(value)
def local(key,value):LOC[key]=value;return key
GRANT_OUTPUTS={'common/national_focus/COLDWAR_SSR_1970_focus.txt',
               'common/scripted_effects/COLDWAR_SSR_focus_rewards.txt'}

def prepare_output(path,body,loc=False):
    """Keep physical infrastructure grants independent of manual technology."""
    return _grant_queries(body,buildings={'infrastructure'}) if not loc and path in GRANT_OUTPUTS else body

def emit(path,body,loc=False):OUTPUTS.append(shared.write(path,prepare_output(path,body,loc),loc))
def key(n):return n['id'].removeprefix(P)

def native_keys():
    keys=set()
    for path in (ROOT/'localisation/english').glob('*.yml'):
        keys.update(re.findall(r'^\s*([^\s:#]+):',path.read_text(encoding='utf-8-sig',errors='replace'),re.M))
    return keys

NATIVE=native_keys()

def modifier_label(name):
    for candidate in ('MODIFIER_'+name.upper(),'MODIFIER_'+name,name):
        if candidate in NATIVE:return '$'+candidate+'$'
    assert name in D['labels'],name
    return D['labels'][name]

def stat_rows(modifiers,prefix='stat'):
    parts=[]
    for name,value in modifiers.items():
        costly=any(word in name for word in ('cost','consumption','training_time','energy_use','consumer_goods','worker_requirement')) or name=='agriculture_workers_modifier'
        fmt=('-=' if costly else '+=')+('3' if name in NUMBERS else '%2')
        tooltip=local(P+prefix+'_'+name+'_tt',modifier_label(name)+': $RIGHT|'+fmt+'$')
        parts.append(f'add_to_variable = {{ COLDWAR_SSR_preview_value = {num(value)} tooltip = {tooltip} }}')
    return '\n'.join(parts)

def named_change(n,name=None):
    label=local(P+'name_'+shared.slug(name or n.get('spirit') or n['ownership']),name or n.get('spirit') or n['ownership'])
    return f'custom_effect_tooltip = {{ localization_key = modifies_dynamic_modifier_tt MODIFIER = {label} }}'

def cost_preview(n):
    parts=[]
    if n.get('gdp_cost'):
        parts.append('custom_effect_tooltip = '+local(P+key(n)+'_gdp_cost_tt',f'Treasury: §R-{num(n["gdp_cost"]*100)}%§! of GDP'))
    if n.get('weekly_gdp_cost'):
        parts.append('custom_effect_tooltip = '+local(P+key(n)+'_weekly_cost_tt',f'Weekly programme budget: §R-{num(n["weekly_gdp_cost"]*100)}%§! of GDP'))
    return join(parts)

def gear_preview(equipment):
    parts=[]
    for item in equipment:
        target=item['target']
        assert target in D['equipment_labels'],target
        parts.append('custom_effect_tooltip = '+local(P+'equipment_'+target+'_tt','§Y$'+target+'$§!'))
        for name,value in item['modifiers'].items():
            label=D['gear_labels'][name]
            fmt='-=%2' if name=='build_cost_ic' else '+=%2'
            tt=local(P+'equipment_stat_'+name+'_tt',label+': $RIGHT|'+fmt+'$')
            parts.append(f'add_to_variable = {{ COLDWAR_SSR_preview_value = {num(value)} tooltip = {tt} }}')
    return join(parts)

def building_state_limit(building):
    name=building['type']
    base='is_owned_and_controlled_by = ROOT\nis_core_of = ROOT\n'
    if name=='dockyard':base+='is_coastal = yes\n'
    # Native capacity is distinct from the mandatory new shared slot.
    shared_slots=name in {'industrial_complex','arms_factory','dockyard','agriculture_district'}
    return base+f'free_building_slots = {{ building = {name} size > 0'+(' include_locked = yes' if shared_slots else '')+' }'

def asset_effects(n):
    parts=[]
    if n.get('building'):
        b=n['building'];limit=building_state_limit(b)
        parts.append(block('random_owned_controlled_state',block('limit',limit)+'\n'+
            f'add_extra_state_shared_building_slots = {b["shared_slots"]}\n'+
            f'add_building_construction = {{ type = {b["type"]} level = {b["level"]} instant_build = yes }}'))
    if n.get('research'):
        r=n['research'];parts.append(f'add_tech_bonus = {{ name = {n["id"]} uses = {r["uses"]} bonus = {num(r["bonus"])} category = {r["category"]} }}')
    if n.get('doctrine'):
        r=n['doctrine'];parts.append(f'add_doctrine_cost_reduction = {{ name = {n["id"]} uses = {r["uses"]} cost_reduction = {num(r["bonus"])} category = {r["category"]} }}')
    for field,effect in [('army_xp','army_experience'),('air_xp','air_experience'),('navy_xp','navy_experience')]:
        if n.get(field):parts.append(effect+' = '+num(n[field]))
    if n.get('stability'):parts.append('add_stability = '+num(n['stability']))
    return join(parts)

def visible_requirements(n):
    trigger='COLDWAR_SSR_is_ssr' if n['phase']=='ssr' else 'COLDWAR_SSR_is_independent'
    text='A recognised Soviet Union republic' if n['phase']=='ssr' else 'An independent republic'
    tooltip=local(P+('requires_ssr' if n['phase']=='ssr' else 'requires_independence')+'_tt',text)
    parts=[block('custom_trigger_tooltip','tooltip = '+tooltip+'\n'+block('hidden_trigger',trigger+' = yes'))]
    if n['phase']=='party':parts.append(D['party_triggers'][n['gate'][4:]]+' = yes')
    if n.get('building'):parts.append(block('any_owned_state',building_state_limit(n['building'])))
    if n.get('geography')=='naval_coast':parts.append('any_owned_state = { is_owned_and_controlled_by = ROOT is_core_of = ROOT is_coastal = yes }')
    if n.get('needs_existing_resources'):
        tests='\n'.join('has_resources_amount = { resource = '+resource+' amount > 0 }' for resource in ['oil','aluminium','tungsten','steel','chromium'])
        parts.append(block('any_owned_state','is_owned_and_controlled_by = ROOT\n'+block('OR',tests)))
    if (n.get('action') or '').startswith('offer:'):
        label=local(P+'requires_offer_partner_tt','An eligible independent partner is available for a new agreement')
        parts.append(block('custom_trigger_tooltip','tooltip = '+label+'\n'+block('hidden_trigger',P+'can_offer_'+n['action'].split(':')[1]+' = yes')))
    return join(parts)

def runtime_guard(n):
    parts=[visible_requirements(n),'NOT = { has_country_flag = '+n['receipt']+' }']
    if n['scope_tag']:parts.append('original_tag = '+n['scope_tag'])
    for parents in n['prerequisites']:
        clauses=['has_country_flag = '+BY[parent]['receipt'] for parent in parents]
        parts.append(block('OR','\n'.join(clauses)) if len(clauses)>1 else clauses[0])
    for excluded in n['exclusive']:parts.append('NOT = { has_country_flag = '+BY[excluded]['receipt']+' }')
    return join(parts)

def modifier_preview(n):
    parts=[]
    if n.get('replace'):
        text='Replace §Y'+n['replace']+'§! with §Y'+n['spirit']+'§!'
        parts.append('custom_effect_tooltip = '+local(P+key(n)+'_replace_tt',text))
    elif n.get('modifiers'):parts.append(named_change(n))
    if n.get('modifiers'):parts.append(stat_rows(n.get('display_modifiers',n['modifiers'])))
    parts.append(gear_preview(n.get('equipment_bonuses',[])))
    if n.get('specialisation'):
        parts.append('custom_effect_tooltip = '+local(P+'independence_preview_tt','§YAfter independence:§!'))
        parts.append(named_change(n,n['legacy_spirit']))
        parts.append(stat_rows(n['legacy_modifiers']))
        parts.append(gear_preview(n.get('legacy_equipment_bonuses',[])))
        if n.get('legacy_weekly_gdp_cost'):
            parts.append('custom_effect_tooltip = '+local(P+key(n)+'_legacy_weekly_tt',f'Weekly programme budget: §R-{num(n["legacy_weekly_gdp_cost"]*100)}%§! of GDP'))
    if n.get('preparation_effect'):
        s=n['preparation_effect'];parts.extend(['custom_effect_tooltip = '+local(P+'prepared_preview_tt','§YOn independence:§!'),named_change(n,s['name']),stat_rows(s['delta'])])
    if n.get('exposure'):
        s=n['exposure'];parts.extend(['custom_effect_tooltip = '+local(P+'exposure_preview_tt','§YOn independence:§!'),named_change(n,s['name']),stat_rows(s['modifiers'])])
    if n.get('remove_exposure'):
        parts.append('custom_effect_tooltip = '+local(P+'remove_exposure_tt','If present: Remove §Y'+n['remove_exposure']+'§!'))
        parts.append(stat_rows({'tax_gain_multiplier_modifier':.04,'civilian_factories_productivity':.05}))
    for s in n.get('conditional_removals',[]):
        parts.extend(['custom_effect_tooltip = '+local(P+'remove_'+shared.slug(s['name'])+'_tt','If present: Remove §Y'+s['name']+'§!'),stat_rows(s['delta'])])
    if n.get('regional_aftercare'):
        for tag,model in shared.models().items():
            s=model['profile']['regional']
            text='If present: Replace §Y'+s['name']+'§! with §YManaged '+s['name']+'§!'
            rows='custom_effect_tooltip = '+local(P+'regional_aftercare_'+tag+'_tt',text)+'\n'+stat_rows({k:round(-v/2,5) for k,v in s['modifiers'].items()})
            parts.append(block('if',f'limit = {{ hidden_trigger = {{ original_tag = {tag} }} }}\n'+rows))
    if n.get('repair'):
        # The country-specific preview callback uses stored preparation/repair
        # state and emits native signed numeric changes, even before execution.
        parts.append(P+'preview_repair_'+n['repair']['spirit']+' = yes')
    return join(parts)

def preview(n):
    parts=[cost_preview(n),block('effect_tooltip',join([modifier_preview(n),asset_effects(n)]))]
    if n.get('market_course'):parts.append(P+'preview_market_'+n['market_course']+' = yes')
    if (n.get('action') or '').startswith('offer:'):parts.append(P+'preview_offer_'+n['action'].split(':')[1]+' = yes')
    if n.get('market_charter'):
        parts.extend(['unlock_decision_tooltip = COLDWAR_SSR_market_light_industry_auction','unlock_decision_tooltip = COLDWAR_SSR_market_light_industry_workers'])
    if n.get('public_charter'):parts.append('unlock_decision_tooltip = COLDWAR_SSR_market_light_industry_public')
    if n.get('market_course'):parts.append('unlock_decision_tooltip = COLDWAR_SSR_market_light_industry_liquidate')
    if n.get('party_transfer'):
        t=n['party_transfer'];name=P+key(n)+'_party_transfer_tt'
        parts.append('custom_effect_tooltip = '+local(name,f'{t["from_name"]}: §R-15%§! of current support\n{t["to_name"]}: receives the transferred support'))
    return join(parts)

def apply_reward(n):
    parts=[]
    if n.get('gdp_cost'):
        parts.extend([f'set_temp_variable = {{ treasury_change = {{ value = gdp_total multiply = {num(-n["gdp_cost"])} }} }}','modify_treasury_effect = yes'])
    parts.append(asset_effects(n))
    if n.get('party_transfer'):
        t=n['party_transfer'];parts.extend([f'set_temp_variable = {{ party_index = {t["from_slot"]} }}',f'set_temp_variable = {{ target_party_index = {t["to_slot"]} }}',f'set_temp_variable = {{ party_popularity_fraction = {num(t["fraction"])} }}','move_party_popularity = yes'])
    parts.append('set_country_flag = '+n['receipt'])
    if n.get('market_course'):parts.append(P+'start_market_'+n['market_course']+' = yes')
    if (n.get('action') or '').startswith('offer:'):parts.append(P+'offer_'+n['action'].split(':')[1]+' = yes')
    parts.append(P+'reconcile = yes')
    return block(P+'reward_'+key(n),block('if',block('limit',runtime_guard(n))+'\n'+join(parts)))

def icon_registry():
    result={}
    for path in (ROOT/'interface').glob('*.gfx'):
        text=path.read_text(encoding='utf-8-sig',errors='replace')
        for match in re.finditer(r'spriteType\s*=\s*\{([^{}]*)\}',text,re.S):
            name=re.search(r'\bname\s*=\s*"([^"]+)"',match[1])
            if name:result[name[1]]=str(path.relative_to(ROOT))
    return result

def focus_icon(n):
    return art.focus_icon(n)

SPRITES=icon_registry()

def focus(n):
    parts=['id = '+n['id'],'icon = '+focus_icon(n)]
    if n.get('anchor'):
        a=BY[n['anchor']];parts.extend([f'x = {n["x"]-a["x"]}',f'y = {n["y"]-a["y"]}','relative_position_id = '+a['id']])
    else:parts.extend([f'x = {n["x"]}',f'y = {n["y"]}'])
    parts.extend(['cost = '+num(n['cost']),'cancel_if_invalid = yes','continue_if_invalid = no'])
    if n['scope_tag']:parts.append('allow_branch = { original_tag = '+n['scope_tag']+' }')
    for parents in n['prerequisites']:parts.append('prerequisite = { '+' '.join('focus = '+v for v in parents)+' }')
    if n['exclusive']:parts.append('mutually_exclusive = { '+' '.join('focus = '+v for v in n['exclusive'])+' }')
    parts.append(block('available',visible_requirements(n)))
    filters={'army':'FOCUS_FILTER_RESEARCH FOCUS_FILTER_ARMY_BONUS','air':'FOCUS_FILTER_RESEARCH FOCUS_FILTER_AIRFORCE_BONUS',
      'navy':'FOCUS_FILTER_RESEARCH FOCUS_FILTER_NAVY_BONUS','research':'FOCUS_FILTER_RESEARCH',
      'industry':'FOCUS_FILTER_INDUSTRY','agriculture':'FOCUS_FILTER_INDUSTRY','diplomacy':'FOCUS_FILTER_FOREIGN_POLICY',
      'institution':'FOCUS_FILTER_POLITICAL','society':'FOCUS_FILTER_STABILITY'}
    parts.append('search_filters = { '+filters[n['kind']]+' }')
    parts.append(block('completion_reward',preview(n)+'\n'+block('hidden_effect',P+'reward_'+key(n)+' = yes')))
    parts.append('ai_will_do = { factor = 1 }')
    local(n['id'],n['title']);local(n['id']+'_desc',n['description'])
    return block('focus',join(parts))

def generate_base():
    header=['id = '+TREE,'country = { factor = 0 modifier = { add = 80 IMP_is_1970_scenario = yes OR = { '+' '.join('original_tag = '+tag for tag in shared.TAGS)+' } } }',
      'default = no','reset_on_civilwar = no','initial_show_position = { focus = COLDWAR_SSR_secretariat }',
      'continuous_focus_position = { x = 6100 y = 650 }','shared_focus = COLDWAR_UNI_the_union_plan']
    for identifier in ['secretariat','economic_accounts','social_accounts','defence_commission','special_aircraft_mandate','public_authority','payment_register','defence_authority','foreign_service']:
        header.append('shortcut = { name = '+P+identifier+' target = '+P+identifier+' scroll_wheel_factor = 0.8 }')
    emit('common/national_focus/COLDWAR_SSR_1970_focus.txt',block('focus_tree',join(header)+'\n'+'\n'.join(focus(n) for n in NODES)))
    loader=block(P+'load_tree',block('if','limit = { IMP_is_1970_scenario = yes OR = { '+' '.join('original_tag = '+tag for tag in shared.TAGS)+' } NOT = { has_focus_tree = '+TREE+' } }\nload_focus_tree = { tree = '+TREE+' keep_completed = yes }'))
    emit('common/scripted_effects/COLDWAR_SSR_focus_rewards.txt',loader+'\n'+'\n'.join(apply_reward(n) for n in NODES))
    emit('localisation/english/COLDWAR_SSR_focus_l_english.yml',shared.loc_text(LOC),True)

def main():
    OUTPUTS.extend(art.generate())
    generate_base()
    for module_name in ['lifecycle','market','diplomacy']:
        module=__import__(module_name)
        OUTPUTS.extend(module.generate())
    import integration
    OUTPUTS.extend(integration.generate())
    # Shared grant dependencies are included after country-specific providers.
    for path,text in _grant_runtime().items():emit(path,text,path.endswith('.yml'))
    manifest=shared.baseline();manifest.update(status='Implemented; verification recorded separately',art_catalogue_sha256=hashlib.sha256((HERE/'art_catalogue.json').read_bytes()).hexdigest(),focuses=len(NODES),country_views={tag:len(m['nodes']) for tag,m in shared.models().items()},
       outputs={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in OUTPUTS})
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(dict(focuses=len(NODES),outputs=len(OUTPUTS))))

if __name__=='__main__':main()
