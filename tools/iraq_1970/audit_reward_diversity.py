# IMPERIA CW — Cold War: iraq 1970 — audit reward diversity.
"""Read-only inventory of the installed IRQ focus rewards for design review.

Writes audit documents only. Never imports/runs the country compiler, installs
content or treats the catalogue's obsolete reward_summary as live evidence.
"""
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re

from common import ROOT, P, parse, first, values, walk, emit

HERE = ROOT/'docs/design/iraq_1970/reward_diversity_2026_10_19'
LABELS = {
    'bureaucracy_cost_multiplier_modifier': 'Bureaucracy expenditure',
    'social_cost_multiplier_modifier': 'Social expenditure',
    'political_power_factor': 'Political power gain',
    'stability_factor': 'Stability (percentage points)',
    'tax_gain_multiplier_modifier': 'Tax-revenue multiplier',
    'drift_defence_factor': 'Ideological drift defence',
    'research_speed_factor': 'Research speed',
    'army_org_factor': 'Army organisation',
    'army_personnel_cost_multiplier_modifier': 'Army personnel expenditure',
    'production_factory_efficiency_gain_factor': 'Production efficiency growth',
    'conscription_factor': 'Recruitable-population factor (relative)',
    'production_factory_max_efficiency_factor': 'Production efficiency cap',
    'consumer_goods_factor': 'Consumer-goods factor (relative)',
    'production_speed_buildings_factor': 'Construction speed',
    'opinion_gain_monthly_same_ideology_factor': 'Same-outlook opinion gain',
    'foreign_influence_modifier': 'Offensive foreign influence',
    'army_defence_factor': 'Army defence',
    'army_morale_factor': 'Army recovery rate',
    'training_time_army_factor': 'Army training time',
    'supply_consumption_factor': 'Supply consumption',
    'industrial_capacity_factory': 'Military factory output',
    'agricolture_productivity_modifier': 'Agricultural productivity',
    'mdcw_cw_support_effectiveness': 'Imperia support effectiveness',
    'oil_export_multiplier_modifier': 'Oil-export revenue',
    'fuel_gain_factor': 'Fuel gain',
    'army_fuel_consumption_factor': 'Army fuel consumption',
    'industrial_capacity_dockyard': 'Dockyard output',
    'army_attack_factor': 'Army attack',
}
BUILDINGS = {'industrial_complex': 'Civilian Industry', 'arms_factory': 'Military Industry',
             'infrastructure': 'Infrastructure', 'agriculture_district': 'Agricultural District',
             'offices': 'Office Sector', 'dockyard': 'Dockyard'}
GENERIC = {'bureaucracy_cost_multiplier_modifier', 'political_power_factor',
           'stability_factor', 'drift_defence_factor'}


def read(path):
    return path.read_text(encoding='utf-8-sig')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def signed(value):
    return f'{value*100:+g}'


def modifiers_text(modifiers):
    return [f'{LABELS[key]}: {signed(value)}'+(' pp' if key == 'stability_factor' else '%')
            for key, value in modifiers.items()]


def one_off(n, idea_payloads):
    results = []
    if n['building']:
        state, kind, amount = n['building']
        results.append(f'{amount} {BUILDINGS.get(kind,kind)} in state {state}')
    if n['army_xp']:
        results.append(f"{n['army_xp']:g} Army XP")
    text = '\n'.join(n['instant']+n.get('audit_new_delivery_only', []))
    if not text:
        return results
    rows = parse(text)
    for key, op, body in walk(rows):
        if key == 'add_tech_bonus':
            results.append(f"{first(body,'uses')} × {float(first(body,'bonus'))*100:g}% research bonus ({first(body,'category')})")
        elif key == 'add_doctrine_cost_reduction':
            results.append(f"{first(body,'uses')} × {float(first(body,'cost_reduction'))*100:g}% doctrine cost reduction ({first(body,'category')})")
        elif key == 'set_temp_variable' and first(body,'LR_change') is not None:
            results.append(f"Literacy: {float(first(body,'LR_change'))*100:+g} percentage points")
        elif key == 'add_timed_idea':
            idea=first(body,'idea')
            extra='; '.join(modifiers_text(idea_payloads.get(idea,{})))
            results.append(f"{idea}: {first(body,'days')} days"+(' ('+extra+')' if extra else ''))
        elif key in ('air_experience', 'add_political_power', 'add_war_support', 'add_compliance'):
            scale = 100 if key == 'add_war_support' else 1
            results.append(f'{key}: {float(body)*scale:+g}')
        elif key == 'add_resource':
            results.append(f"Resource deposit: {first(body,'type')} +{first(body,'amount')} (state scope in source)")
        elif key in ('add_state_claim', 'add_core_of'):
            results.append(f'{key}: {body} (actual state/peace conditions apply)')
        elif key == 'create_wargoal':
            results.append(f"War goal: {first(body,'type')} against {first(body,'target')}; {first(body,'expire')} days")
    if not results and rows:
        results.append('Policy/operation marker: '+emit(rows).strip())
    return results


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    design = json.loads(read(ROOT/'tools/iraq_1970/current_design.json'))
    manifest_path = ROOT/'tools/iraq_1970/manifest.json'
    manifest = json.loads(read(manifest_path))
    owned = {**manifest['generated'], **{a['path']:a['sha256'] for a in manifest['adapters']}}
    before = {path:sha(ROOT/path) for path in owned}
    assert all(before[path] == expected for path, expected in manifest['generated'].items())
    adapter_drift = [a['path'] for a in manifest['adapters'] if before[a['path']] != a['sha256']]
    source = read(ROOT/'common/national_focus/COLDWAR_IRQ_1970_focus.txt')
    tree = first(parse(source), 'focus_tree')
    focuses = {first(body,'id'):body for body in values(tree,'focus')}
    effects = dict((key,body) for key,op,body in parse(read(ROOT/'common/scripted_effects/COLDWAR_IRQ_1970_rewards.txt')))
    loc = dict(re.findall(r'^\s+([^\s:]+):0 "(.*)"$', read(ROOT/'localisation/english/COLDWAR_IRQ_1970_focus_l_english.yml'), re.M))
    for path in (ROOT/'localisation/english').glob('COLDWAR_IRQ_1970_*l_english.yml'):
        loc.update(re.findall(r'^\s+([^\s:]+):0 "(.*)"$',read(path),re.M))
    ideas = {key:dict((k,float(v)) for k,op,v in first(body,'modifier',[]))
             for key,op,body in first(first(parse(read(ROOT/'common/ideas/COLDWAR_IRQ_1970_starting_ideas.txt')),'ideas'),'country')}
    temporary_ideas={key:dict((k,float(v)) for k,op,v in first(body,'modifier',[]))
                     for key,op,body in first(first(parse(read(ROOT/'common/ideas/COLDWAR_IRQ_1970_audit_ideas.txt')),'ideas'),'country')}
    def spirit_change(current,target=None):
        previous=ideas[current]; following=ideas.get(target,{})
        changes={key:following.get(key,0)-previous.get(key,0) for key in previous.keys()|following.keys()
                 if following.get(key,0)!=previous.get(key,0)}
        return ('Conditional spirit removal: ' if target is None else 'Conditional spirit improvement: ')+loc.get(current,current)+' ('+'; '.join(modifiers_text(changes))+')'
    branches = {g['id']:g['label'] for g in design['groups']}
    proposals = {}
    for name in ('ECONOMIC_PROPOSALS.json', 'POLITICAL_PROPOSALS.json', 'STATE_PROPOSALS.json'):
        path = HERE/name
        if path.exists():
            addition = json.loads(read(path))
            assert not (set(addition)&set(proposals)), 'Overlapping recommendation ownership'
            proposals.update(addition)
    records = []
    for n in design['nodes']:
        if n.get('audit_retired'):
            continue
        fid = n['id']; focus = focuses[fid]; reward = first(focus,'completion_reward',[])
        # Establish that the current modifier catalogue agrees with the actual
        # installed numeric preview, including conditional Front/monopoly rows.
        actual = []
        for tooltip in values(reward,'effect_tooltip'):
            for key,op,body in walk(tooltip):
                if key == 'add_to_variable':
                    var,assignment,number = next(row for row in body if row[0] != 'tooltip')
                    prefix = P+n['group']+'_'
                    assert var.startswith(prefix)
                    actual.append((var[len(prefix):],float(number)))
        assert Counter(actual) == Counter(n['modifiers'].items()), fid
        apply = effects[P+'apply_'+n['key']]
        if n['budget_gdp_share']:
            assert any(key == 'multiply_variable' and (fid+'_invoice','=',f"{n['budget_gdp_share']:g}") in body
                       for key,op,body in walk(apply)), fid
        decisions = [d['label'] for d in n['decisions']]
        assert values(reward,'unlock_decision_tooltip') == [d['id'] for d in n['decisions']], fid
        once = one_off(n,temporary_ideas)
        spirit = []
        for tooltip in values(reward,'effect_tooltip'):
            for key,op,body in walk(tooltip):
                if key == 'remove_ideas':
                    spirit.append(spirit_change(body))
                elif key == 'swap_ideas':
                    spirit.append(spirit_change(first(body,'remove_idea'),first(body,'add_idea')))
        spirit = list(dict.fromkeys(spirit))
        other = []
        # Explicit financing API unlocks are useful even when the old catalogue
        # has no decision entry. Read the actual applier rather than its title.
        for key,op,body in walk(apply):
            if key.startswith('COLDWAR_IRQ_gulf_unlock_'):
                other.append(key)
        issue = []
        if n['modifiers'].get('bureaucracy_cost_multiplier_modifier',0)>0:
            issue.append('bureaucracy')
        if n['modifiers'].get('social_cost_multiplier_modifier',0)>0:
            issue.append('social_cost')
        if n['modifiers'].get('stability_factor',0)>0:
            issue.append('stability_cap')
        if n['modifiers'] and set(n['modifiers']) <= GENERIC and not once and not decisions and not spirit and not other:
            issue.append('generic_only')
        records.append({
            'id':fid,'key':n['key'],'name':loc[fid],'branch':n['group'],'branch_name':branches[n['group']],
            'days':float(first(focus,'cost'))*7,'gdp_cost_percent':n['budget_gdp_share']*100,
            'modifiers':n['modifiers'],'current_modifiers':modifiers_text(n['modifiers']),
            'one_time':once,'decisions':decisions,'spirit_changes':spirit,'extra_unlocks':other,
            'conditions':n.get('requires',[]),'ownership':n['ownership'],
            'exclusive_with':n['mutually_exclusive'],'prerequisites':n['prerequisites'],
            'review_tags':issue,'recommendation':proposals.get(n['key']),
            'source_line':source[:source.index('id = '+fid+'\n')].count('\n')+1,
        })
    assert len(records)==410
    assert set(proposals) <= {r['key'] for r in records}
    count = Counter(key for r in records for key in r['modifiers'])
    pos = Counter(key for r in records for key,value in r['modifiers'].items() if value>0)
    negative = Counter(key for r in records for key,value in r['modifiers'].items() if value<0)
    signatures = defaultdict(list)
    for r in records:
        if r['modifiers']:
            signatures[tuple(sorted(r['modifiers'].items()))].append(r['id'])
    repeats = [{'modifiers':dict(signature),'focuses':ids} for signature,ids in signatures.items() if len(ids)>1]
    repeats.sort(key=lambda row:-len(row['focuses']))
    stats = {
        'focuses':len(records),'modifier_occurrences':sum(count.values()),'modifier_types':len(count),
        'modifier_counts':count,'positive_modifier_counts':pos,'negative_modifier_counts':negative,
        'focuses_with_building':sum(bool(n['building']) for n in design['nodes'] if not n.get('audit_retired')),
        'focuses_with_research_bonus':sum(any('add_tech_bonus' in text for text in n['instant']) for n in design['nodes'] if not n.get('audit_retired')),
        'focuses_with_decisions':sum(bool(r['decisions']) for r in records),
        'generic_only_screening_flags':sum('generic_only' in r['review_tags'] for r in records),
        'manual_recommendations':len(proposals),
        'branch_summary':[{ 'id':gid,'name':label,'focuses':sum(r['branch']==gid for r in records),
            'bureaucracy_increases':sum(r['branch']==gid and r['modifiers'].get('bureaucracy_cost_multiplier_modifier',0)>0 for r in records),
            'social_cost_increases':sum(r['branch']==gid and r['modifiers'].get('social_cost_multiplier_modifier',0)>0 for r in records)} for gid,label in branches.items()],
        'repeated_modifier_vectors':repeats,
    }
    result = {'scope':'Read-only design audit of every active installed IRQ focus. New recommendations are unimplemented balance proposals.',
              'manifest_sha256':sha(manifest_path),'revision':manifest['audit_revision'],
              'shared_adapters_changed_since_manifest':adapter_drift,
              'limits':'Exact catalogue/live-preview operands and invoice shares checked; native political/economic activation still follows live guards. Count flags are screening, not proof of a bad focus. Do not sum mutually exclusive parties or routes.',
              'stats':stats,'records':records}
    (HERE/'FOCUS_INVENTORY.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    with (HERE/'FOCUS_INVENTORY.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        fields=['id','name','branch_name','days','gdp_cost_percent','current_modifiers','one_time','decisions','spirit_changes','extra_unlocks','conditions','review_tags','recommendation']
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
        for r in records:
            row={key:r[key] for key in fields}
            for key in fields:
                if isinstance(row[key],list):row[key]=' | '.join(row[key])
            row['recommendation']=json.dumps(row['recommendation'],ensure_ascii=False) if row['recommendation'] else ''
            writer.writerow(row)
    lines=['# Vollständiges Irak-Fokusinventar', '',
           '410 aktive Foki. English names and exact installed values; recommendations remain unimplemented. '
           'Bureaucracy/social costs and consumer goods are relative factors. Positive programme stability has a shared 15-point cap. '
           'One-time costs are GDP percentages; agreement/decision costs are additional only where stated in their actual options. '
           'Conditional spirit rows show possible state changes, never simultaneous grants. Full keys, conditions and proposals: FOCUS_INVENTORY.json / .csv.','']
    for gid,label in branches.items():
        lines += ['## '+label,'','| Focus | Days / GDP cost | Current programme | One-time / spirits / decisions |','|---|---|---|---|']
        for r in records:
            if r['branch']!=gid:continue
            extras=r['one_time']+r['spirit_changes']+['Decision: '+x for x in r['decisions']]+r['extra_unlocks']
            clean=lambda text:str(text).replace('|','/').replace('\n',' ')
            lines.append('| '+clean(r['name'])+' (`'+r['key']+'`) | '+f"{r['days']:g} d / {r['gdp_cost_percent']:g}%"+' | '+clean('; '.join(r['current_modifiers']) or '—')+' | '+clean('; '.join(extras) or 'No direct asset, spirit or decision reward; inspect its prerequisite role')+' |')
        lines.append('')
    (HERE/'FOCUS_INVENTORY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    recommendations=['# Konkrete Empfehlungen nach Fokus','','44 einzeln zugeordnete Bewertungen; davon sind einige bewusst „behalten“. Alle Änderungen sind Entwürfe, keine installierten Werte.','']
    for r in records:
        proposal=r['recommendation']
        if not proposal:continue
        recommendations += ['## '+r['name']+' — '+r['branch_name'],'',
            f"`{r['id']}` · {r['days']:g} Tage · {r['gdp_cost_percent']:g}% BIP einmalig",'',
            '**Aktuell:** '+('; '.join(r['current_modifiers']+r['one_time']+r['spirit_changes']) or 'Kein direkter numerischer/physischer Effekt')+'.',
            ('Entscheidungen: '+', '.join(r['decisions'])+'.') if r['decisions'] else '', '',
            '**Befund:** '+proposal['issue'],'','**Vorschlag:** '+proposal['proposal'],'','**Begründung:** '+proposal['reason'],'']
    (HERE/'RECOMMENDATIONS.md').write_text('\n'.join(recommendations)+'\n',encoding='utf-8')
    template=read(ROOT/'tools/iraq_1970/reward_diversity_fragment.html')
    fragment=template.replace('AUDIT_DATA_HERE',json.dumps(result,separators=(',',':'),ensure_ascii=False).replace('</','<\\/'))
    destination=Path('C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f4e-9042-7b61-be51-9d85f9facd82/iraq-reward-diversity-audit.html')
    assert len(fragment.encode('utf-8'))<1_000_000
    destination.write_text(fragment,encoding='utf-8',newline='\n')
    unchanged = all(sha(ROOT/path)==digest for path,digest in before.items())
    assert unchanged,'Loaded content changed during audit; review concurrent changes'
    snapshot={'manifest_sha256':sha(manifest_path),'installed_files_unchanged':unchanged,
              'generated_files':len(manifest['generated']),'adapters':len(manifest['adapters']),
              'installed_hashes':before,'shared_adapters_changed_since_manifest':adapter_drift,
              'audit_script_sha256':sha(Path(__file__)),
              'catalogue_hash':sha(ROOT/'tools/iraq_1970/current_design.json'),
              'verification':'All410 actual numeric previews, exact invoice multipliers, actual decision unlock lists and English names checked. Obsolete reward_summary strings excluded.'}
    (HERE/'AUDIT_SOURCE_SNAPSHOT.json').write_text(json.dumps(snapshot,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:stats[k] for k in ('focuses','modifier_occurrences','modifier_types','focuses_with_building','focuses_with_research_bonus','focuses_with_decisions','generic_only_screening_flags','manual_recommendations')},indent=2))
    print('Positive bureaucracy focuses:',pos['bureaucracy_cost_multiplier_modifier'])


if __name__=='__main__':
    main()
