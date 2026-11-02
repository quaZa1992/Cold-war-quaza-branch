# IMPERIA COLD WAR — Bounded source, native-reference and encoding checks for Union orders.
import ast
import hashlib
import json
import re
import sys
from pathlib import Path
from catalogue import FAMILIES, CHANNELS, POLICIES, TEMPORARY_POLICIES, PERIOD, OUTCOME_DAYS

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,walk,first


def main():
    manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
    errors=[]
    def check(ok,message):
        if not ok:errors.append(message)
    parsed={}
    for path in HERE.glob('*.py'):
        source=path.read_text(encoding='utf-8')
        check(source.startswith('# IMPERIA COLD WAR \u2014 '),'Tool project marker: '+path.name)
        try:ast.parse(source,filename=str(path))
        except SyntaxError as error:errors.append(str(error))
    for rel,digest in manifest['outputs'].items():
        path=ROOT/rel
        check(path.exists(),'Missing output: '+rel)
        if not path.exists():continue
        raw=path.read_bytes()
        check(hashlib.sha256(raw).hexdigest()==digest,'Manifest drift: '+rel)
        if path.suffix=='.yml':
            check(raw.startswith(b'\xef\xbb\xbf'),'Missing localisation BOM: '+rel)
            check(raw.decode('utf-8-sig').replace('\r\n','\n').startswith('l_english:\n# IMPERIA COLD WAR'),'Localisation header: '+rel)
        elif path.suffix=='.txt':
            check(not raw.startswith(b'\xef\xbb\xbf'),'Script BOM: '+rel)
            check(raw.decode('utf-8').startswith('# IMPERIA COLD WAR'),'Project marker: '+rel)
            try:parsed[rel]=parse(raw.decode('utf-8'))
            except ValueError as error:errors.append(rel+': '+str(error))
    defs={}
    for rel,rows in parsed.items():
        for k,o,v in rows:
            if k.startswith('COLDWAR_ORD_'):defs.setdefault(k,[]).append(rel)
    decisions={}
    for rel,rows in parsed.items():
        if rel.startswith('common/decisions/') and '/categories/' not in rel:
            for _,_,category in rows:
                for k,o,v in category:
                    check(k not in decisions,'Duplicate decision: '+k)
                    decisions[k]=v
    ideas=parsed['common/ideas/COLDWAR_UNION_orders.txt'][0][2][0][2]
    idea_ids={k for k,o,v in ideas}
    legacy_decisions={k for _,_,category in parse((ROOT/'common/decisions/COLDWAR_UNI_1970_decisions.txt').read_text(encoding='utf-8')) for k,o,v in category}
    script=(ROOT/'common/scripted_effects/COLDWAR_UNION_orders.txt').read_text(encoding='utf-8')
    effect_rows=parse(script)
    for k,o,v in walk(parse(script)):
        if k in {'activate_mission','remove_mission'}:check(v in decisions or v in legacy_decisions,'Unknown mission: '+v)
        if k=='add_timed_idea':check(first(v,'idea') in idea_ids,'Unknown outcome spirit')
    for name,body in decisions.items():
        timeout=first(body,'days_mission_timeout')
        if timeout:
            expected=30 if '_proposal_' in name else OUTCOME_DAYS if any(t in name for t in ('_success_clock_','_failure_clock_','_shortfall_clock','_policy_clock_')) else PERIOD
            check(float(timeout)==expected,'Wrong mission period: '+name)
            if first(first(body,'allowed',[]),'always')=='no':
                check(first(body,'visible') is None,'Hidden clock blocks native activation: '+name)
    tokens={v for k,o,v in parsed['common/synchronized_dynamic_tokens/COLDWAR_UNION_orders.txt'] if k=='_bare'}
    missions={name for name,body in decisions.items() if first(body,'days_mission_timeout') is not None}
    check(tokens==missions,'Synchronized mission token coverage differs from native clocks')
    for rel,rows in parsed.items():
        for k,o,v in walk(rows):
            if k.startswith('COLDWAR_ORD_') and v in ('yes','no'):
                check(k in defs,'Unknown scripted callback: '+k+' in '+rel)
    snapshot=first(effect_rows,'COLDWAR_ORD_snapshot_proposals',[])
    for f in FAMILIES:
        serial='COLDWAR_ORD_review_serial_'+f.key
        check(serial in str(snapshot),'Missing reviewed proposal identity: '+f.key)
        for operation in ('approve','reject'):
            body=first(effect_rows,'COLDWAR_ORD_'+operation+'_'+f.key,[])
            check(serial in str(body),'Unreviewed proposal '+operation+': '+f.key)
        if f.equipment and not f.counter:
            body=first(effect_rows,'COLDWAR_ORD_certify_'+f.key,[])
            check('COLDWAR_ORD_return_serial' in str(body),'Unreviewed production certification: '+f.key)
    equipment=set()
    for path in (ROOT/'common/units/equipment').glob('*.txt'):
        for k,o,v in parse(path.read_text(encoding='utf-8-sig')):
            if k in {'equipments','duplicate_archetypes'} and isinstance(v,list):equipment.update(a for a,b,c in v)
    docs=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV/documentation/dynamic_variables_documentation.md').read_text(encoding='utf-8')
    art=(ROOT/'interface/COLDWAR_SSR_icons.gfx').read_text(encoding='utf-8')
    for f in FAMILIES:
        for eqid in f.equipment:check(eqid in equipment,'Unknown equipment target: '+eqid)
        if f.counter:check('### '+f.counter+'\n' in docs,'Unknown production counter: '+f.counter)
        check('GFX_idea_COLDWAR_SSR_'+f.art+'"' in art,'Unknown small idea art: '+f.art)
    for name in ('COLDWAR_UNI_target_failed','COLDWAR_UNI_directive_failed','COLDWAR_UNI_add_shortfall','COLDWAR_UNI_pripiski_exposed'):
        body=first(parsed['common/scripted_effects/COLDWAR_UNI_1970_scripted_effects.txt'],name)
        check('COLDWAR_ORD_enabled' in str(body) and 'is_ai' in str(body),'Unguarded legacy punishment: '+name)
    event10=next(v for k,o,v in parsed['events/COLDWAR_UNI_1970_events.txt'] if k=='country_event' and first(v,'id')=='COLDWAR_UNI.10')
    check('COLDWAR_ORD_enabled' in str(first(event10,'trigger')),'Queued legacy judgement not guarded')
    loc=(ROOT/'localisation/english/COLDWAR_UNION_orders_l_english.yml').read_text(encoding='utf-8-sig')
    local_keys=set(re.findall(r'^\s*([^\s:#]+):',loc,re.M))
    for rel,rows in parsed.items():
        for k,o,v in walk(rows):
            if k in {'custom_effect_tooltip','tooltip','localization_key'} and isinstance(v,str) and v.startswith('COLDWAR_ORD_'):
                check(v in local_keys,'Missing visible text: '+v+' in '+rel)
    for name,body in decisions.items():
        if first(first(body,'allowed',[]),'always')!='no':
            check(name in local_keys and name+'_desc' in local_keys,'Missing decision name/description: '+name)
    check('\u2013' not in loc and '\u2014' not in '\n'.join(loc.splitlines()[2:]),'Dash in new game text')
    check('3: fulfilled' not in loc,'Internal state labels in game text')
    check(len(idea_ids)==len(CHANNELS)*2+1+len(POLICIES)+len(TEMPORARY_POLICIES),'Outcome idea count mismatch')
    report={'project':'IMPERIA COLD WAR','errors':errors,'families':len(FAMILIES),'decision_and_mission_definitions':len(decisions),'spirits':len(idea_ids),'outputs':len(manifest['outputs']),'scope':'Static source, IDs, manifest, native equipment/counter references, dates, migration guards and encoding. Not native or live multiplayer evidence.'}
    (HERE/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))
    return bool(errors)


if __name__=='__main__':raise SystemExit(main())
