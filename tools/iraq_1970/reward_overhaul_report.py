# IMPERIA CW — Cold War: iraq 1970 — reward overhaul report.
"""Document the installed direct-reward revision; never installs content."""
from collections import Counter
from pathlib import Path
import hashlib,json
from audit_design import load_design
from common import ROOT,first,values,parse
import reward_overhaul as overhaul

DEST=ROOT/'docs/design/iraq_1970/reward_overhaul_2026_10_19'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def total(nodes):
    active=[n for n in nodes if not n.get('audit_retired')]
    return {
        'active_focuses':len(active),
        'positive_bureaucracy_focuses':sum(n['modifiers'].get('bureaucracy_cost_multiplier_modifier',0)>0 for n in active),
        'any_bureaucracy_focuses':sum('bureaucracy_cost_multiplier_modifier' in n['modifiers'] for n in active),
        'any_stability_focuses':sum('stability_factor' in n['modifiers'] for n in active),
        'building_focuses':sum(bool(overhaul.building_specs(n)) for n in active),
        'limited_instruction_pools':sum(c['kind'] in ('tech','doctrine') for n in active for c in overhaul._payloads(n)),
        'decision_unlock_focuses':sum(bool(n['decisions']) for n in active),
    }

def payload(n):
    parts=[f'`{key}` {value:+g}' for key,value in n['modifiers'].items()]
    for c in n.get('overhaul_components',[]):
        if c['kind']=='building':parts.append(f'{c["amount"]:g} × `{c["building_type"]}` (state {c["state"]})')
        elif c['kind'] in ('army_xp','air_xp','navy_xp'):parts.append(f'+{c["amount"]:g} {c["kind"]}')
        elif c['kind']=='literacy':parts.append(f'+{100*c["amount"]:g} percentage points literacy')
        elif c['kind'] in ('tech','doctrine'):parts.append(f'{c["amount"]:g} × {100*c["bonus"]:g}% `{c["category"]}` '+('research bonus' if c['kind']=='tech' else 'doctrine cost reduction'))
        else:parts.append('`'+c['raw'].replace('\n',' ').replace('|','\\|')+'`')
    return '; '.join(parts)

def main():
    design=load_design();old=load_design(False)
    manifest_path=ROOT/'tools/iraq_1970/manifest.json';manifest=json.loads(manifest_path.read_text())
    assert all(sha(ROOT/p)==v for p,v in manifest['generated'].items())
    tree=first(parse((ROOT/'common/national_focus/COLDWAR_IRQ_1970_focus.txt').read_text(encoding='utf-8-sig')),'focus_tree')
    emitted={first(f,'id'):f for f in values(tree,'focus')}
    nodes=[n for n in design['nodes'] if not n.get('audit_retired')]
    assert len(nodes)==410 and all(n['id'] in emitted for n in nodes)
    stats={'revision':design['audit_revision'],'manifest_sha256':sha(manifest_path),'before':total(old['nodes']),'after':total(nodes),
           'limits':'Source/provider and bounded transaction checks are separate from native gameplay, hover, save/reload and multiplayer testing.'}
    DEST.mkdir(parents=True,exist_ok=True)
    (DEST/'INSTALLED_REWARD_COUNTS.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
    lines=['# Installed Iraqi direct focus rewards','',
        'All410 active focuses in the installed direct_rewards_2026_10_19_v3 revision. The 16 hidden compatibility IDs are excluded. English focus names and canonical final values match the installed reward/programme providers checked by the presentation and independent emitted-output review.','',
        'Numbers below are script operands, not a promise of equal national GDP growth. Percentage-factor modifiers use decimal fractions; interest-rate and productivity-growth fields have native numeric units. Buildings, XP, literacy, finite instructions and claims/core/war-goal effects are one-time deliveries. Standing programmes follow their actual party, leader, policy and contract gates. Mutually exclusive routes cannot be summed together. Positive programme stability keeps the existing fifteen-point cap.','',
        'Decision unlocks are not included as material rewards in this inventory. Existing genuine diplomatic, electoral, war-planning and policy-revision decisions remain. The 410 focuses all have their own direct material outcome or actual starting-spirit reform. An unfunded or territorially blocked physical project retains its guarded delivery contract.','',
        '| Focus | Chapter | Days | Price (% annual GDP) | Direct reward operands / deliveries |',
        '|---|---|---:|---:|---|']
    for n in nodes:
        lines.append('| '+n['title'].replace('|','\\|')+' (`'+n['id']+'`) | '+n['group']+' | '+str(n['days'])+' | '+f'{100*n["budget_gdp_share"]:g}'+' | '+payload(n)+' |')
    (DEST/'ALL_FOCUS_REWARDS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(stats,indent=2))

if __name__=='__main__':main()
