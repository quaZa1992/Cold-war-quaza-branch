# IMPERIA CW — Cold War: Spain V2 installed provider/encoding/reference checks.
"""Source checks only; not an HOI4 engine or multiplayer certification."""
from pathlib import Path
from collections import defaultdict
import json,hashlib,re
from script_ast import parse,walk,first
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
P='COLDWAR_SPR_'

def main():
    manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
    failures=[];parsed={};loc={};count=0
    for rel,expected in manifest['generated'].items():
        path=ROOT/rel
        if not path.exists():failures.append('Missing output '+rel);continue
        blob=path.read_bytes()
        if hashlib.sha256(blob).hexdigest()!=expected:failures.append('Generated hash changed '+rel)
        if rel.endswith('.yml'):
            if not blob.startswith(b'\xef\xbb\xbf') or blob[3:].startswith(b'\xef\xbb\xbf'):failures.append('Localization BOM '+rel)
            for k,value in re.findall(r'^\s*([^\s:#]+):\d*\s*"(.*)"\s*$',blob.decode('utf-8-sig'),re.M):
                if k in loc:failures.append('Duplicate localization '+k)
                loc[k]=value
        elif rel.endswith(('.txt','.gfx')):
            if blob.startswith(b'\xef\xbb\xbf'):failures.append('Script BOM '+rel)
            try:parsed[rel]=parse(blob.decode('utf-8'));count+=1
            except ValueError as e:failures.append(rel+': '+str(e))
            if re.search(r'(?<!\w)\d+\.\d{6,}(?!\w)',blob.decode('utf-8')):failures.append('Fixed point precision '+rel)
    # Resolve actual runtime providers, including retained native MD APIs.
    definitions={'effects':{},'triggers':{},'ideas':{},'dynamic':{},'events':{}}
    declarations={'effects':defaultdict(list),'triggers':defaultdict(list),'dynamic':defaultdict(list)}
    for folder,kind in [('common/scripted_effects','effects'),('common/scripted_triggers','triggers'),('common/ideas','ideas'),('common/dynamic_modifiers','dynamic'),('events','events')]:
        for path in (ROOT/folder).glob('*.txt'):
            if kind in ['effects','triggers','dynamic']:
                # Top-level named blocks; whole native world parsing is unnecessary for this bounded closure.
                for name in re.findall(r'^([^\s#{}=]+)\s*=\s*\{',path.read_text(encoding='utf-8-sig'),re.M):
                    definitions[kind][name]=str(path.relative_to(ROOT))
                    declarations[kind][name].append(path.name)
            elif path.name.startswith(P):
                ast=parse(path.read_text(encoding='utf-8-sig'))
                if kind=='ideas':
                    for k,o,v in first(first(ast,'ideas',[]),'country',[]):definitions[kind][k]=str(path.relative_to(ROOT))
                else:
                    for k,o,v in ast:
                        if k=='country_event':definitions[kind][first(v,'id')]=str(path.relative_to(ROOT))
    for rel,ast in parsed.items():
        if rel.startswith('common/scripted_effects/') or rel.startswith('common/scripted_triggers/'):
            # Detect duplicate exported custom aliases across old/new files.
            for k,o,v in ast:
                if k.startswith(P):
                    kind='effects' if 'scripted_effects' in rel else 'triggers'
                    hits=declarations[kind][k]
                    if len(hits)!=1:failures.append('Duplicate or missing provider '+k+' '+str(hits))
        for k,o,v in walk(ast):
            if isinstance(v,str) and k.startswith(P) and v in ('yes','no'):
                if k not in definitions['effects'] and k not in definitions['triggers']:
                    failures.append('Unresolved custom call '+k+' in '+rel)
            if k in ['has_idea','add_ideas','remove_ideas','add_idea','remove_idea'] and isinstance(v,str) and v.startswith(P):
                if v not in definitions['ideas']:failures.append('Unresolved idea '+v+' in '+rel)
            if k in ['custom_effect_tooltip','tooltip','localization_key','title','desc','name'] and isinstance(v,str) and v.startswith(P):
                if k=='name' and v not in loc:continue # named technology/doctrine reward, not localisation
                if v not in loc:failures.append('Unresolved English text '+v+' in '+rel)
            if k=='id' and isinstance(v,str) and v.startswith(P) and '.' in v:
                if v not in definitions['events']:failures.append('Unresolved event '+v+' in '+rel)
    # The old custom providers and observers must not coexist with the new implementation.
    retired=json.loads((HERE/'retirement.json').read_text(encoding='utf-8'))
    for rel in retired['removed_loaded_files']:
        if (ROOT/rel).exists():failures.append('Retired provider reappeared '+rel)
    report={'source_validation':'failed' if failures else 'passed','generated_outputs':len(manifest['generated']),'parsed_script_gfx_files':count,'english_keys':len(loc),'approved_sha256':hashlib.sha256((HERE/'approved_design.json').read_bytes()).hexdigest(),'errors':sorted(set(failures)),'engine_tested':False}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))
    if failures:raise SystemExit(1)

if __name__=='__main__':main()
