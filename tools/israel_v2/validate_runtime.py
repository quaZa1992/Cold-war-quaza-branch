# IMPERIA COLD WAR — Israel V2 compiled-payload and installed-file validation.
"""Check the runtime contract separately from the immutable proposal checks."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re

import compile as compiler
from script_format import read


ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/israel_1970_v2/runtime_validation.json'
APPROVED='aa480fcaf2c1609d7d8531164978a3d2dc0023728331775261f26eae09962706'


def sha(raw):return hashlib.sha256(raw).hexdigest()
def field(rows,key):return next((value for name,_,value in rows if name==key),None)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--installed',action='store_true')
    args=parser.parse_args()
    payload=compiler.build();files=payload['files'];checks=[]
    def check(value,label):
        if not value:raise AssertionError(label)
        checks.append(label)
    check(sha((ROOT/'tools/israel_v2/design.json').read_bytes())==APPROVED,'Immutable approved catalogue preserved')
    data=payload['data'];nodes={n['id']:n for n in data['nodes']}
    check(len(nodes)==217 and len(data['groups'])==19,'217 unique live focuses in 19 programmes')
    check(set(nodes)==set(payload['actions']),'Every live focus has exactly one action owner')
    check(not any(key.startswith('common/decisions/') for key in files if Path(key).name.startswith('ISR2_')),'No new decision menus')
    source=files['common/national_focus/ISR70_focus.txt'].decode('utf-8')
    rows=field(read(source),'focus_tree')
    focuses=[value for key,_,value in rows if key=='focus']
    check({field(n,'id') for n in focuses}==set(nodes),'Loaded focus tree matches runtime catalogue')
    check('allow_branch' not in source,'All political branches remain visible')
    check(all(field(n,'completion_reward') for n in focuses),'Every loaded focus has a completion effect')
    registry=field(read(files['common/national_focus/ISR2_legacy_focus_registry.txt'].decode('utf-8')),'focus_tree')
    inert=[v for k,_,v in registry if k=='focus']
    check(len(inert)==399 and all(field(n,'completion_reward')==[] and field(n,'available')==[('always','=','no')] for n in inert),'399 old IDs remain registered only as inert compatibility references')
    providers=set()
    for path,raw in files.items():
        if path.startswith(('common/scripted_effects/','common/scripted_triggers/')):
            providers.update(key for key,_,value in read(raw.decode('utf-8-sig')) if isinstance(value,list))
    calls=set()
    for path,raw in files.items():
        if Path(path).suffix in {'.txt','.gui','.gfx'}:
            check(not raw.startswith(b'\xef\xbb\xbf'),path+': UTF-8 without BOM')
            text=raw.decode('utf-8')
            check(text.startswith('# IMPERIA COLD WAR'),path+': project integration marker')
            read(text)
            calls.update(re.findall(r'\b(ISR2_[A-Za-z0-9_]+)\s*=\s*yes\b',text))
            for flag in re.findall(r'\bset_(?:country|global)_flag\s*=\s*\{([^{}]+)\}',text):
                if re.search(r'\bflag\s*=\s*ISR2_',flag) and re.search(r'\bdays\s*=',flag):
                    check(bool(re.search(r'\bvalue\s*=\s*1\b',flag)),path+': every temporary Israel flag has explicit native value 1')
        elif path.endswith('.yml'):
            check(raw.startswith(b'\xef\xbb\xbf'),path+': localisation BOM')
            check(raw.decode('utf-8-sig').startswith('l_english:\n # IMPERIA COLD WAR'),path+': English localisation marker')
        elif path.endswith('.py'):
            ast.parse(raw.decode('utf-8-sig'),filename=path)
    check(not(calls-providers),'Every generated ISR2 scripted helper resolves: '+str(sorted(calls-providers)))
    workforce=[n['modifiers']['total_workforce_modifier'] for n in nodes.values() if 'total_workforce_modifier' in n['modifiers']]
    check(len(workforce)==3 and all(value>0 for value in workforce) and abs(sum(workforce)-.15)<1e-9,'Exactly three positive workforce reforms capped at +15%')
    integration=files['common/scripted_effects/ISR2_integration_effects.txt'].decode('utf-8')
    check('set_global_flag = ISR2_legacy_replaced' in integration,'Legacy-event retirement survives annexation of Israel')
    history_route=field(read(files['common/scripted_effects/ISR70_effects.txt'].decode('utf-8')),'ISR70_initialize')
    def helper_calls(rows):
        result=set()
        for key,_,value in rows:
            if isinstance(value,list):result.update(helper_calls(value))
            elif value=='yes':result.add(key)
        return result
    check('ISR2_initialize' not in helper_calls(history_route),'Country-history route defers occupation and state-modifier initialization to startup')
    refresh=field(read(integration),'ISR2_refresh')
    refresh_guard=field(field(refresh,'if'),'limit')
    check(('has_country_flag','=','ISR2_initialized') in refresh_guard,'Early budget and government callbacks cannot refresh an uninitialized Israel module')
    restrictions=field(read(files['common/scripted_effects/ISR70_effects.txt'].decode('utf-8')),'ISR70_restrict_party_slots')
    removals=[]
    for key,_,value in restrictions:
        if key!='if':continue
        command=field(value,'remove_from_array')
        if command is None:continue
        predicate=field(field(value,'limit'),'is_in_array')
        check(predicate==command and field(command,'array')=='gov_coalition_array',
            'Coalition removal checks the same actual party value before removing it')
        removals.append(int(field(command,'value')))
    check(removals==[8,9,10,11],'Unsupported party values are removed without deleting unrelated coalition positions')
    check(not any('ISR2_poalei_governing' in raw.decode('utf-8',errors='replace') for key,raw in files.items() if Path(key).suffix in {'.txt','.yml'}),'No invented Poalei governing-representation flag')
    if args.installed:
        changed=[path for path,raw in files.items() if not(ROOT/path).is_file() or (ROOT/path).read_bytes()!=raw]
        check(not changed,'All installed artifacts match a fresh compiler build: '+str(changed))
    report=dict(project='IMPERIA COLD WAR',status='PASS_SOURCE_AND_INSTALL' if args.installed else 'PASS_SOURCE',
        installed_checked=args.installed,focuses=len(nodes),artifacts=len(files),checks=checks,
        payload_sha256=sha(json.dumps({p:sha(raw) for p,raw in sorted(files.items())},separators=(',',':')).encode('utf-8')),
        limitations=['Static compiled-payload checks do not establish native rendering, saves or multiplayer stability.'])
    OUT.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in {'checks','limitations'}}))


if __name__=='__main__':main()
