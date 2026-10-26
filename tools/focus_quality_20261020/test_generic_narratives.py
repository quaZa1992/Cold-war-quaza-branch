# IMPERIA CW — Cold War: focus quality 20261020 — test generic narratives.
"""Coverage and live/canonical consistency for authored generic military prose."""
import json
from pathlib import Path
import re
import runpy

ROOT = Path(__file__).resolve().parents[2]
api = runpy.run_path(str(ROOT/'tools/egypt_1970/apply_quality_merges_20261020.py'))
parse, first, walk = (api[k] for k in ('parse','first','walk'))
module = runpy.run_path(str(ROOT/'Claude outputs/COLDWAR_GEN_generator/gen_quality_narratives.py'))
narratives = module['NARRATIVES']
path = ROOT/'localisation/english/mdcw_1970_generic_focus_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
checks=0


def check(ok, message):
    global checks
    checks+=1
    assert ok, message


focuses = [f for k,_,f in walk(parse((ROOT/'common/national_focus/mdcw_1970_generic_focus.txt').read_text(encoding='utf-8')))
           if k=='focus' and isinstance(f,list)]
by={first(f,'id'):f for f in focuses}
start=next(i for i,f in enumerate(focuses) if first(f,'id')=='GEN_1970_military_emergency')
expected={first(f,'id')+'_desc' for f in focuses[start:]}
check(expected<=set(narratives),'Missing base military narrative')
check(len(narratives)==64,'Authored description inventory changed; review coverage')
check(len(set(narratives.values()))==len(narratives),'Duplicated narrative')
for key,value in narratives.items():
    check(key.removesuffix('_desc') in by,'Unknown focus '+key)
    matches=re.findall(r'^\s*'+re.escape(key)+r':\d*\s*"(.*)"\s*$',text,re.M)
    check(matches==[value],'Live description differs from authored source '+key)
    check('\n' not in value and '"' not in value,'Unescaped localisation control '+key)
    check(not any(s in value for s in ['1970scenario','Effect:', 'Conditions:', 'implementation guard']),
          'Developer scaffolding '+key)
check(module['apply_narratives'](text)==text,'Narrative pass not idempotent')
check(path.read_bytes().startswith(b'\xef\xbb\xbf'),'Localisation missing BOM')
air=by['GEN_1970_air_cavalry_doctrine']
check(first(air,'cost')=='10','AirCavalry duration changed')
reward=first(air,'completion_reward')
bonuses=[n for k,_,n in walk(reward) if k=='add_tech_bonus' and isinstance(n,list)]
check(len(bonuses)==1 and first(bonuses[0],'bonus')=='0.35' and first(bonuses[0],'uses')=='2',
      'Approved AirCavalry rewards changed')
check(first(bonuses[0],'category')=='CAT_attack_helicopters','Wrong AirCavalry research category')
print(f'PASS: {checks} checks; {len(expected)} military and {len(narratives)-len(expected)} R&D descriptions.')
