# IMPERIA CW — Cold War: vietnam 1970 — reward rework.
"""User-requested whole-tree reward revision, layered over immutable approvals.

Only design data is changed here. Importing or loading never writes game files.
Finite rewards stay in the once-stamped completion transaction, not reconciliation.
"""
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
P='COLDWAR_VIE_'

def specification():
    path=HERE/'reward_rework.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else None

def reward_code(n):
    group=n.get('programme_group',n['group']);mod=P+group+'_programme';rows=[]
    if n['modifiers']:
        rows += [f'if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {mod} }} }} }} add_dynamic_modifier = {{ modifier = {mod} }} }}',
                 f'custom_effect_tooltip = {{ localization_key = modifies_dynamic_modifier_tt MODIFIER = {mod} }}']
        for key,value in n['modifiers'].items():
            rows.append(f'add_to_variable = {{ {P}{group}_{key} = {value:g} tooltip = {P}tt_{key} }}')
    if n['cash']:rows += [f'set_temp_variable = {{ treasury_change = {-n["cash"]:g} }}','modify_treasury_effect = yes']
    if n['building']:
        state,kind=n['building'];instant='yes' if n.get('instant_build') else 'no'
        rows.append(f'{state} = {{ add_building_construction = {{ type = {kind} level = 1 instant_build = {instant} }} }}')
    if n['unlock']:rows.append('set_country_flag = '+P+'unlock_'+n['unlock'])
    if n['support']:
        slot,amount=n['support'];rows += [f'set_temp_variable = {{ party_index = {slot} }}',f'set_temp_variable = {{ party_popularity_increase = {amount:g} }}',f'set_temp_variable = {{ temp_outlook_increase = {amount:g} }}','change_relative_party_popularity = yes']
    if n['xp']:rows.append(f'army_experience = {n["xp"]:g}')
    for i,e in enumerate(n.get('additional_rewards',[]),1):
        kind=e['type']
        if kind in ('army_xp','navy_xp','air_xp'):
            rows.append(f'{kind.removesuffix("_xp")}_experience = {e["amount"]:g}')
        elif kind=='research_bonus':
            rows.append(f'add_tech_bonus = {{ name = {n["id"]}_research_{i} bonus = {e["bonus"]:g} uses = {e["uses"]} category = {e["category"]} }}')
        elif kind=='doctrine_bonus':
            rows.append(f'add_doctrine_cost_reduction = {{ name = {n["id"]}_doctrine_{i} cost_reduction = {e["cost_reduction"]:g} uses = {e["uses"]} category = {e["category"]} }}')
        else:raise ValueError('Unsupported finite reward '+str(e))
    rows.extend(n.get('preserved_crisis_code',[]))
    if n['relief']:
        family,stage=n['relief'];key=P+family
        rows.append(f'if = {{ limit = {{ check_variable = {{ {key}_stage < {stage} }} }}\n'+'\n'.join('remove_ideas = '+key+'_'+str(i) for i in range(4))+f'\nadd_ideas = {key}_{stage}\nset_variable = {{ {key}_stage = {stage} }}\n}}')
    rows += ['hidden_effect = { force_update_dynamic_modifier = yes }']
    return '\n'.join(rows)

def programme_groups(design):
    groups=[g.copy() for g in design['groups']]
    if any(n.get('programme_group')=='chinh_training' for n in design['nodes']):
        g=next(g for g in design['groups'] if g['id']=='chinh').copy()
        g.update(id='chinh_training',leader=None,root_focus=P+'chinh_root',art_group='chinh',programme_name='Cadre Education and Economic Advice')
        groups.append(g)
    return groups

def apply_base(design):
    spec=specification()
    if spec is None:return design
    patches={p['id']:p for p in spec['focuses']};by={n['id']:n for n in design['nodes']}
    assert set(patches)==set(by),'Every original focus needs an explicit reward review'
    for key,n in by.items():
        patch=patches[key]
        from script_ast import parse,emit
        n['preserved_crisis_code']=[emit([row]) for row in parse(n['raw_reward_code']) if row[0]=='add_timed_idea']
        for field in ('modifiers','cash','building','instant_build','label','days','prerequisites','exclusive','description','support','x','y','emitted_x','emitted_y','anchor'):
            if field in patch:n[field]=patch[field]
        if 'description' in patch:n['reward_description']=patch['description']
        rewards=patch.get('rewards',[])
        # An explicit army-XP item replaces its old grant, rather than duplicating it.
        ax=[e['amount'] for e in rewards if e['type']=='army_xp']
        if ax:n['xp']=sum(ax)
        n['additional_rewards']=[e for e in rewards if e['type']!='army_xp']
        n['reward_review']=dict(why_player_wants_it=patch['why_player_wants_it'],role=patch.get('role',''),pair_rationale=patch.get('pair_rationale',''))
        n['effects']=[dict(kind='programme',key=k,value=v) for k,v in n['modifiers'].items()]
        if n['unlock']:n['effects'].append(dict(kind='decision_unlock',category=n['unlock']))
        if n['relief']:n['effects'].append(dict(kind='spirit_stage',spirit=n['relief'][0],stage=n['relief'][1]))
        if n['xp']:n['effects'].append(dict(kind='army_experience',value=n['xp']))
        n['effects'] += [dict(kind=e['type'],**{k:v for k,v in e.items() if k!='type'}) for e in n['additional_rewards']]
    # The next extraordinary cadre allocation has two mutually exclusive uses.
    for ids in spec.get('new_exclusive_sets',[]):
        for key in ids:by[key]['exclusive']=list(dict.fromkeys(by[key]['exclusive']+[x for x in ids if x!=key]))
    # Chinh's substantive education choice must be usable during his short tenure.
    rename={P+'chinh_orthodox':P+'chinh_schools',P+'chinh_schools':P+'chinh_orthodox',P+'chinh_evidence':P+'chinh_experts',P+'chinh_experts':P+'chinh_evidence'}
    graph={k:{f:by[k][f] for f in ('x','y','emitted_x','emitted_y','anchor','prerequisites','exclusive')} for k in by if by[k]['group']=='chinh'}
    for old,fields in graph.items():
        target=by[rename.get(old,old)]
        for field,value in fields.items():
            if field=='prerequisites':value=[[rename.get(p,p) for p in clause] for clause in value]
            elif field=='exclusive':value=[rename.get(p,p) for p in value]
            elif field=='anchor':value=rename.get(value,value)
            target[field]=value
    for key in (P+'chinh_schools',P+'chinh_experts'):
        by[key]['programme_group']='chinh_training';by[key]['lifecycle']='party_bound'
    # Unrelated diplomacy does not share a single exclusive agreement slot.
    for q in design['decisions']:
        q['modifiers']=spec['decisions'][q['id']]
        if q['family']=='foreign':q['family']='foreign_'+(q['target'] or q['unlock'])
        if q['id']==P+'decision_withdrawal':q['extra_code']+='\nCOLDWAR_VIE_campaign_cbd_land_drawdown = yes\nNOT = { has_war_with = CBD }'
    for n in design['nodes']:n['raw_reward_code']=reward_code(n)
    design['reward_revision']=spec['revision']
    return design

def apply_campaigns(design):
    spec=specification()
    if spec is None:return design
    from script_ast import parse,emit
    patches={p['id']:p for p in spec['campaigns']};by={n['id']:n for n in design['nodes']}
    assert set(patches)==set(by),'Every campaign focus needs an explicit reward review'
    for key,n in by.items():
        patch=patches[key]
        for field in ('effects','cash','description','label','activation','war_target','policy_lifetime','policy_activation_mode','reserve_first_term'):
            if field in patch:n[field]=patch[field]
        if 'description' in patch:n['reward_description']=patch['description']
        n['reward_review']=patch['why_player_wants_it']
        if 'effects' not in patch:continue
        rows=[]
        if n['cash']:rows += parse(f'set_temp_variable = {{ treasury_change = {-n["cash"]:g} }}\nmodify_treasury_effect = yes')
        for i,e in enumerate(n['effects'],1):
            kind=e['type']
            if kind=='idea':
                idea=key+'_policy'
                rows += parse(f'add_timed_idea = {{ idea = {idea} days = {e["duration"]} }}' if e['duration'] else 'add_ideas = '+idea)
                modifier='\n'.join(k+' = '+f'{v:g}' for k,v in e['modifiers'].items())
                targeted=''
                if e.get('target'):
                    targeted='\ntargeted_modifier = { tag = '+e['target']+'\n'+'\n'.join(k+' = '+f'{v:g}' for k,v in e.get('targeted_modifiers',{}).items())+'\n}'
                if n.get('terrain_training'):modifier+='\ncustom_modifier_tooltip = '+key+'_terrain_tt'
                n['idea_definitions']=idea+' = { picture = national_defenders\nmodifier = {\n'+modifier+'\n}'+targeted+'\n}'
            elif kind=='xp':rows+=parse(f'army_experience = {e["value"]:g}')
            elif kind=='doctrine':rows+=parse(f'add_doctrine_cost_reduction = {{ name = {key}_doctrine_{i} cost_reduction = {e["value"]:g} uses = {e["uses"]} category = land_doctrine }}')
            elif kind=='research':rows+=parse(f'add_tech_bonus = {{ name = {key}_research_{i} bonus = {e["bonus"]:g} uses = {e["uses"]} category = {e["category"]} }}')
            elif kind=='unlock':
                # Preserve the original native unlock flag rather than guessing by label.
                original=[r for r in parse(n['raw_reward_code']) if r[0]=='set_country_flag']
                rows+=original
            elif kind=='wargoal':
                original=[r for r in parse(n['raw_reward_code']) if r[0]=='create_wargoal']
                assert original,'A war goal must retain an approved native provider'
                rows+=original
            else:raise ValueError('Unsupported campaign reward '+str(e))
        n['raw_reward_code']=emit(rows)
    design['reward_revision']=spec['revision']
    return design
