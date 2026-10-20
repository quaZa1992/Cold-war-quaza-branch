"""Static integration checks for actual game-facing assets and references."""
import json
import re
from pathlib import Path
from PIL import Image
from roster import IDEOLOGIES, PARTIES, MILITARY

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
errors=[]
def check(ok,message):
    if not ok: errors.append(message)

files=[*ROOT.glob('common/**/COLDWAR_EGY_1970*roster*.txt'),
       ROOT/'common/characters/COLDWAR_EGY_1970_characters.txt',
       ROOT/'common/scripted_effects/EGY_political_leaders.txt',
       ROOT/'common/scripted_effects/COLDWAR_EGY_1970_scripted_effects.txt',
       ROOT/'common/national_focus/COLDWAR_EGY_1970_focus.txt',
       ROOT/'common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt',
       ROOT/'interface/COLDWAR_EGY_1970_parties.gfx',
       ROOT/'history/countries/EGY - Egypt.txt',
       *ROOT.glob('common/decisions/**/COLDWAR_EGY_1970_reserve_officers.txt'),
       *ROOT.glob('common/decisions/**/COLDWAR_EGY_1970_party_formations.txt')]
for path in files:
    text=path.read_text(encoding='utf-8-sig')
    # Strip comments and strings together so '#' inside strings remains a string.
    stripped=re.sub(r'"(?:[^"\\]|\\.)*"|#[^\n]*','',text)
    depth=0
    for char in stripped:
        if char=='{': depth+=1
        elif char=='}': depth-=1
        if depth<0: break
    check(depth==0,f'Unbalanced braces: {path.relative_to(ROOT)}')
    for asset in re.findall(r'(?:picture|large|small|texturefile)\s*=\s*"(gfx/[^"]+)"',text):
        if '/1970/' in asset or path.suffix=='.gfx':
            check((ROOT/asset).exists(),f'Missing asset: {asset}')

dispatch=(ROOT/'common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt').read_text()
effect=(ROOT/'common/scripted_effects/COLDWAR_EGY_1970_roster_effects.txt').read_text()
traits='\n'.join(p.read_text(encoding='utf-8-sig') for p in (ROOT/'common/country_leader').glob('*.txt'))
all_traits=set(re.findall(r'^\s*(\w+)\s*=\s*\{',traits,re.M))
all_sprites='\n'.join(p.read_text(encoding='utf-8-sig') for p in (ROOT/'interface').rglob('*.gfx'))
sprite_names=set(re.findall(r'name\s*=\s*"([^"]+)"',all_sprites))
for idx,ideology in enumerate(IDEOLOGIES):
    for suffix in ('','_desc','_icon'):
        block=re.search(rf'name = {re.escape(ideology)}_L{suffix}\s*\n(.*?)(?=\n\}})',dispatch,re.S)
        expected=f'localization_key = COLDWAR_EGY_1970_party_{idx}{suffix}'
        check(bool(block and expected in block.group(1)),f'Missing dispatch: {ideology}{suffix}')
        if block:
            entries=block.group(1).splitlines()
            check(any(expected in line for line in entries[:2]),f'1970 dispatch is shadowed: {ideology}{suffix}')
    check(f'check_variable = {{ ruling_party = {idx} }}' in effect,f'Missing leader slot {idx}')
    check('GFX_COLDWAR_EGY_1970_party_'+str(idx) in sprite_names,f'Missing party sprite {idx}')
for lang in ('english','german'):
    path=ROOT/f'localisation/{lang}/COLDWAR_EGY_1970_parties_l_{lang}.yml'
    check(path.read_bytes().startswith(b'\xef\xbb\xbf'),f'No localisation BOM: {lang}')
    text=path.read_text(encoding='utf-8-sig')
    keys=re.findall(r'^ ([^:]+):',text,re.M)
    check(len(keys)==len(set(keys)),f'Duplicate localisation keys: {lang}')
    for idx in range(24):
        for suffix in ('','_desc','_icon'):
            check(f'COLDWAR_EGY_1970_party_{idx}{suffix}' in keys,f'Missing localisation {lang} {idx}{suffix}')

char_text=(ROOT/'common/characters/COLDWAR_EGY_1970_characters.txt').read_text()
for key,role,skills,slot,trait,date in MILITARY:
    check(trait in all_traits,f'Unknown advisor trait: {trait}')
    check(f'COLDWAR_EGY_1970_{key} = {{' in char_text,f'Missing character: {key}')
    recruited=f'recruit_character = COLDWAR_EGY_1970_{key}' in effect
    check(recruited==(date is None),f'Incorrect starting/retired officer status: {key}')

for path in (ROOT/'gfx/leaders/EGY/1970').glob('*.dds'):
    with Image.open(path) as im: check(im.size==(156,210),f'Wrong portrait size: {path.name}')
for path in (ROOT/'gfx/leaders/EGY/1970/small').glob('*.dds'):
    with Image.open(path) as im: check(im.size==(65,67),f'Wrong small portrait size: {path.name}')
for key in ('shia_reform_council','shia_guardian_council','baath_council','sinai_council'):
    check((HERE/'generated'/f'{key}.png').exists(),f'Missing final council artwork: {key}')
for block in re.split(r'(?m)^\tfocus = \{',(ROOT/'common/national_focus/COLDWAR_EGY_1970_focus.txt').read_text())[1:]:
    fid=re.search(r'id = (\w+)',block)
    if not fid or 'power_to' not in fid[1]: continue
    for line in re.findall(r'create_country_leader = \{[^\n]+',block):
        check('picture =' in line,f'Party-accession leader has no explicit portrait: {fid[1]}')
history=(ROOT/'history/countries/EGY - Egypt.txt').read_text()
start=history.split('2000.1.1 = {')[0]
check('COLDWAR_EGY_recruit_1970_military = yes' in start,'Roster is not connected to 1970 history')
check('expire = "1970.9.28"' not in start,'Nasser expiry can bypass succession event')
check('set_naval_oob = "mdcw_1970_empty_naval"' in start,'Empty starting fleet was unexpectedly replaced')
check('set_air_oob = "mdcw_1970_empty_air"' in start,'Empty starting air force was unexpectedly replaced')
check('COLDWAR_EGY_nasser_deceased' in (ROOT/'common/scripted_effects/COLDWAR_EGY_1970_scripted_effects.txt').read_text(),'Nasser death flag is not connected')
check('COLDWAR_EGY_set_party_leader_1970 = yes' in (ROOT/'common/scripted_effects/EGY_political_leaders.txt').read_text(),'1970 leader dispatcher is disconnected')
for path,kind in [(ROOT/'common/decisions/COLDWAR_EGY_1970_reserve_officers.txt','decision'),
                  (ROOT/'common/decisions/categories/COLDWAR_EGY_1970_reserve_officers.txt','decision_category'),
                  (ROOT/'common/decisions/COLDWAR_EGY_1970_party_formations.txt','decision'),
                  (ROOT/'common/decisions/categories/COLDWAR_EGY_1970_party_formations.txt','decision_category')]:
    for icon in re.findall(r'icon\s*=\s*(\w+)',path.read_text()):
        check(f'GFX_{kind}_{icon}' in sprite_names,f'Unregistered {kind} icon: {icon}')
manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
check(not manifest['missing_portraits'],'Missing portraits: '+', '.join(manifest['missing_portraits']))
result={'passed':not errors,'errors':errors,'party_slots':24,'military_characters':10,
        'starting_military':sum(m[5] is None for m in MILITARY),
        'reserve_military':sum(m[5] is not None for m in MILITARY),
        'portrait_assets':len(list((ROOT/'gfx/leaders/EGY/1970').glob('*.dds'))),
        'council_group_portraits':4,
        'in_game_test_performed':False}
(HERE/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
raise SystemExit(1 if errors else 0)
