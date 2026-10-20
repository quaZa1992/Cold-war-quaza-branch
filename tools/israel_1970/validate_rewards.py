"""Check the requested reward/icon revision, including visible tooltip coverage."""
from pathlib import Path
import json
import re
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'english_design.json').read_text(encoding='utf-8'))
baseline=json.loads((HERE/'reward_revision_baseline.json').read_text(encoding='utf-8'))
manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
errors=[]
def check(value,message):
    if not value:errors.append(message)
loc=(ROOT/'localisation/english/ISR70_l_english.yml').read_text(encoding='utf-8-sig')
all_loc='\n'.join(p.read_text(encoding='utf-8-sig') for p in (ROOT/'localisation/english').rglob('*.yml'))
keys=set(re.findall(r'^\s*([A-Za-z0-9_]+):',all_loc,re.M))
sprites='\n'.join((ROOT/f'interface/ISR70_{name}.gfx').read_text(encoding='utf-8') for name in ('focus','focus_shine'))
registered=set(re.findall(r'name = "([^"]+)"',sprites))
changed=0;increments=0
for n in data['nodes']:
    old=baseline.get(n['id'])
    if old:
        if not n.get('policy_extension'):
            for key in ('group','mutually_exclusive'):check(n[key]==old[key],'Policy structure changed: '+n['id']+'/'+key)
            expected=[[p for p in row if p not in data['removed_unlock_focuses']] for row in old['prerequisites']]
            check(n['prerequisites']==[row for row in expected if row],'Policy dependencies changed: '+n['id'])
        changed+=n['reward']!=old['reward'] or n['modifiers']!=old['modifiers']
    check(n.get('reward_revision')==(3 if n.get('policy_extension') else 2) and bool(n.get('reward_summary')),'Missing rewritten reward: '+n['id'])
    check(n['icon'] in registered and n['icon']+'_shine' in registered,'Missing focus/shine sprite: '+n['id'])
    check(n['art_source'].startswith(('gfx/interface/goals/coldwar/','gfx/interface/goals/israel_palestine/')),'Unreviewed art source: '+n['id'])
    check(not any(x in n['art_source'] for x in ('CostalIndustry','CHI_Domestic','diamond_gent','ISR_middle_east','go_to_camp_david','Empower_Workers_UnionsUK','arty_industry_1')),'Rejected artwork remains: '+n['id'])
    if n['group'].startswith('party_'):
        for mod,value in n['modifiers'].items():
            pattern=r'add_to_variable = \{ ISR70_p\d+_'+re.escape(mod)+r' = [-\d.]+ tooltip = (\w+) \}'
            match=re.search(pattern,n['completion_reward_code'])
            check(bool(match),'Hidden or unlabeled programme change: '+n['id']+'/'+mod)
            if match:check(match[1] in keys,'Undefined modifier tooltip: '+match[1]);increments+=1
    description=next((line for line in loc.splitlines() if line.startswith(' '+n['id']+'_desc:')),'')
    check('Rewards on completion:' not in description and '\\n• ' not in description,'Duplicated rewards in description: '+n['id'])
check(changed==sum(n['id'] in baseline for n in data['nodes']),'Not all legacy focus rewards were rewritten: '+str(changed))
for key,encoded in re.findall(r'^ (ISR70_\w+_tt):0 (".*")$',loc,re.M):
    value=json.loads(encoded)
    for reference in re.findall(r'\$([A-Za-z0-9_]+)\$',value):check(reference in keys,'Unknown native label in tooltip: '+key+'/'+reference)
for name,texture in manifest['focus_art'].items():
    try:
        im=Image.open(ROOT/texture);check(im.width>0 and im.height>0,'Empty graphic: '+texture)
    except OSError:errors.append('Unreadable focus graphic: '+texture)
effects=(ROOT/'common/scripted_effects/ISR70_effects.txt').read_text(encoding='utf-8')
check('ISR70_sync_reward_revision = {' in effects and 'ISR70_sync_reward_revision = yes' in effects,'Old saves cannot synchronize programme modifiers')
# Actual civic consequences, not only a different bonus with a political name.
nodes={n['id']:n for n in data['nodes']}
for slot in (7,21,22,23):
    for suffix,value in (('ca','yes'),('cb','no')):check('elections_allowed = '+value in nodes[f'ISR70_p{slot}_{suffix}']['reward'],'Constitutional choice has no election consequence: '+str(slot)+'/'+suffix)
result={'status':'FAIL' if errors else 'PASS','errors':errors,'focus_rewards_rewritten':changed,'policy_choices_preserved':not any('Policy' in e for e in errors),'removed_unlock_focuses':len(data['removed_unlock_focuses']),'visible_programme_increments':increments,'reviewed_focus_textures':len(manifest['focus_art']),'language':'English only','runtime_test':False}
(ROOT/'docs/israel_1970_design/reward_revision_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2));raise SystemExit(bool(errors))
