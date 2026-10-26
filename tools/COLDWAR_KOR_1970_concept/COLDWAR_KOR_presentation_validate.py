# IMPERIA CW — Cold War: independent presentation surface and preservation audit.
"""Compare executable semantics, not merely counts, before installing polish."""
from pathlib import Path
import argparse,hashlib,json,re,sys
HERE=Path(__file__).parent;ROOT=HERE.parents[1];DOC=ROOT/'docs/design/COLDWAR_KOR_1970'
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,values
from COLDWAR_KOR_alliance_revision import load_design

def digest(value):return hashlib.sha256(repr(value).encode()).hexdigest()
def data(rows):return tuple((k,o,data(v) if isinstance(v,list) else v) for k,o,v in rows)

def conjunction(items):
    flattened=[]
    for item in items:
        flattened.extend(item[1] if item[0]=='AND' else [item])
    distinct=tuple(sorted(set(flattened),key=repr))
    return distinct[0] if len(distinct)==1 else ('AND',distinct)

def predicate(rows,triggers,trail=()):
    atoms=[]
    for k,o,v in rows:
        if k in ('hidden_trigger','AND'):atom=predicate(v,triggers,trail)
        elif k=='custom_trigger_tooltip':atom=predicate([x for x in v if x[0] not in ('tooltip','not_tooltip')],triggers,trail)
        elif k=='NOT':atom=('NOT',predicate(v,triggers,trail))
        elif k=='OR':atom=('OR',tuple(sorted((predicate([x],triggers,trail) for x in v),key=repr)))
        elif k in triggers and v in ('yes','no'):
            assert k not in trail,k
            atom=predicate(triggers[k],triggers,trail+(k,))
            if v=='no':atom=('NOT',atom)
        elif k in ('check_variable','has_country_leader','has_dynamic_modifier','free_building_slots'):atom=(k,o,data(v))
        elif isinstance(v,list):atom=(k,o,predicate(v,triggers,trail))
        else:atom=(k,o,v)
        atoms.append(atom)
    return conjunction(atoms)

def executable(rows,triggers):
    result=[]
    for k,o,v in rows:
        if k in ('effect_tooltip','custom_effect_tooltip'):continue
        if k=='hidden_effect':result.extend(executable(v,triggers));continue
        if isinstance(v,list):
            v=predicate(v,triggers) if k in ('available','visible','allowed','enable','trigger','limit') else executable(v,triggers)
        result.append((k,o,v))
    return tuple(result)

def load_scripts(base,manifest):
    parsed={rel:parse((base/rel).read_text(encoding='utf-8')) for rel in manifest['files'] if rel.endswith(('.txt','.gfx','.gui'))}
    triggers={k:v for rel,rows in parsed.items() if rel.startswith('common/scripted_triggers/COLDWAR_KOR_') for k,o,v in rows}
    hashes={}
    for rel,rows in parsed.items():
        if rel.startswith('common/scripted_triggers/COLDWAR_KOR_'):
            canonical=tuple((k,o,predicate(v,triggers)) for k,o,v in rows)
        else:canonical=executable(rows,triggers)
        hashes[rel]=digest(canonical)
    return parsed,triggers,hashes

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--installed',action='store_true');a=ap.parse_args()
    base=ROOT if a.installed else HERE/'runtime_staged'
    manifest=json.loads((DOC/'COLDWAR_KOR_runtime_manifest.json').read_text())
    parsed,triggers,hashes=load_scripts(base,manifest)
    baseline=DOC/'COLDWAR_KOR_presentation_baseline.json'
    if not baseline.exists():
        assert not a.installed,'Capture installed pre-polish baseline before installing'
        old,oldtriggers,oldhashes=load_scripts(ROOT,manifest)
        baseline.write_text(json.dumps({'source':'Installed scripts before release prose/presentation polish','semantics':oldhashes},indent=2)+'\n',encoding='utf-8')
    original=json.loads(baseline.read_text())['semantics']
    errors=[]
    if not manifest.get('delivery_revision'):
        for path,before in original.items():
            if hashes.get(path)!=before:errors.append('Executable semantics changed: '+path)
    loc={}
    for line in (base/'localisation/english/COLDWAR_KOR_1970_l_english.yml').read_text(encoding='utf-8-sig').splitlines():
        match=re.match(r'\s+([^ :]+):\d+\s+"(.*)"$',line)
        if match:loc[match[1]]=match[2]
    decisions=0;checked_labels=set();seen_helpers=set()
    def surface(rows,where,protected=False):
        for k,o,v in rows:
            if k=='hidden_trigger':continue
            if k=='custom_trigger_tooltip':
                key=first(v,'tooltip');opposite=first(v,'not_tooltip',str(key)+'_NOT')
                for label in (key,opposite):
                    if label not in loc:errors.append('Missing requirement text: '+str(label))
                    else:
                        checked_labels.add(label)
                        if re.search(r'COLDWAR_|ruling_party|array\^|Not fulfilled:',loc[label]):errors.append('Internal language in '+label)
                continue
            if k in triggers:
                if k not in seen_helpers:seen_helpers.add(k);surface(triggers[k],where+' -> '+k)
                continue
            if k=='has_country_flag' and str(v).startswith('COLDWAR_'):errors.append('Raw flag in '+where+': '+v)
            if k=='check_variable':errors.append('Raw variable requirement in '+where+': '+repr(v))
            if isinstance(v,list):surface(v,where)
    for path,rows in parsed.items():
        if not path.startswith('common/decisions/COLDWAR_KOR_'):continue
        for cat,o,body in rows:
            for key,o,decision in body:
                if not isinstance(decision,list):continue
                decisions+=1
                surface(first(decision,'available',[]),key)
                surface(first(decision,'visible',[]),key)
                for suffix in ('','_desc'):
                    if key+suffix not in loc:errors.append('Missing decision text '+key+suffix)
                reward=first(decision,'complete_effect',[])
                if not first(reward,'hidden_effect'):errors.append('Unseparated decision execution '+key)
    descs=[loc[n['id']+'_desc'] for n in load_design()['nodes']]
    if len(set(descs))!=len(descs):errors.append('Repeated focus descriptions')
    for key,value in loc.items():
        if key.endswith(('_weekly_tt','_offer_tt','.accepted_tt')):
            if any(x in value for x in ('Active programme commitment','replaces the previous commitment','On acceptance only','Terms last')):errors.append('Old accounting prose '+key)
    report={'status':'FAIL' if errors else 'PASS','target':'installed' if a.installed else 'staged','decisions':decisions,'requirement_labels_checked':len(checked_labels),'unique_focus_descriptions':len(set(descs)),'executable_semantics':'Authorized USFK/diplomatic gameplay revision; see delivery validation' if manifest.get('delivery_revision') else 'unchanged from pre-polish installed scripts','errors':errors,'scope':'Source-level UI coverage; no claim of live HOI4 rendering'}
    (DOC/'COLDWAR_KOR_presentation_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
