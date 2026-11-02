# IMPERIA COLD WAR — Read-only cross-country building-capacity inventory.
"""Classify source candidates. A match alone is never a confirmed gameplay bug.

Never writes runtime scripts, walks asset junctions, or invokes country builds.
Only compact query metadata and reference links are written to the design report.
"""
from collections import Counter,defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/design/building_capacity_audit_20261027'
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT/'tools/usa_1970_expansion'))
from focus_prerequisite_ui import nodes,field
from usa_building_capacity import building_definitions

def walk(rows):
    for n in rows:
        yield n
        yield from walk(n.children())

def source(path):return path.read_text(encoding='utf-8-sig',errors='replace')

def main():
    definitions=building_definitions();techs=[];countries=defaultdict(set);active=set();hashes={}
    for path in (ROOT/'history/countries').glob('*.txt'):
        s=source(path)
        for match in re.finditer(r'load_focus_tree\s*=\s*(\w+)',s):countries[match[1]].add(path.name[:3])
        if '1970.1.1' not in s:continue
        for block in nodes(s):
            if block.key=='1970.1.1':
                active.update(n.value for n in walk(block.children()) if n.key=='load_focus_tree' and isinstance(n.value,str))
    active.update(('mdcw_1970_generic_focus','COLDWAR_SSR_1970_focus'))
    # A dated block may also reference a future replacement in an else arm.
    # This inventory targets authored1970providers, not1985/2000replacements.
    active={t for t in active if '1970' in t or t.startswith('ISR70')}
    for path in (ROOT/'common/technologies').glob('*.txt'):
        s=source(path)
        if 'enable_building' not in s:continue
        hashes[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
        for container in nodes(s):
            for tech in container.children():
                for n in tech.children():
                    if n.key=='enable_building':
                        techs.append(dict(technology=tech.key,year=field(tech.children(),'start_year'),building=field(n.children(),'building'),level=field(n.children(),'level'),source=path.relative_to(ROOT).as_posix()))
    tech_by_building=defaultdict(list)
    for row in techs:tech_by_building[row['building']].append(row)
    candidates=[];parse_errors=[]
    query_pattern=re.compile(r'\bfree_building_slots\s*=\s*\{[^{}]*\}',re.S)
    for folder in ('common/national_focus','common/scripted_triggers','common/scripted_effects','events','common/decisions'):
        for path in (ROOT/folder).glob('*.txt'):
            s=source(path);suspected=[]
            for match in query_pattern.finditer(s):
                b=re.search(r'\bbuilding\s*=\s*(\w+)',match[0])
                if b and b[1] in definitions and not definitions[b[1]]['shares_slots'] and not re.search(r'\bprovince\s*=',match[0]):suspected.append((match,b[1]))
            if not suspected:continue
            try:ast=nodes(s)
            except Exception as e:parse_errors.append([path.relative_to(ROOT).as_posix(),str(e)]);continue
            hashes[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
            def locate(pos,rows,trail=()):
                for n in rows:
                    if n.start<=pos<n.end:
                        label=field(n.children(),'id') if n.key in ('focus','focus_tree','country_event') else None
                        return locate(pos,n.children(),trail+(label or n.key,)) if n.children() else trail+(label or n.key,)
                return trail
            for match,building in suspected:
                trail=locate(match.start(),ast)
                candidates.append(dict(file=path.relative_to(ROOT).as_posix(),line=s.count('\n',0,match.start())+1,building=building,query=re.sub(r'\s+',' ',match[0]),path=trail,countries=sorted(countries.get(trail[0],set())),active1970_direct_tree=bool(folder=='common/national_focus' and trail[0] in active),technology_provider_found=bool(tech_by_building[building])))
    # Trace the exact native selectors used by random grant helpers, then
    # inventory direct callers in the actual 1970 national trees.
    trigger_path=ROOT/'common/scripted_triggers/00_scripted_triggers.txt'
    selectors={}
    for n in nodes(source(trigger_path)):
        affected=[c for c in walk(n.children()) if c.key=='free_building_slots' and tech_by_building.get(field(c.children(),'building')) and not definitions[field(c.children(),'building')]['shares_slots'] and not field(c.children(),'province')]
        if affected:selectors[n.key]=sorted(set(field(c.children(),'building') for c in affected))
    helper_path=ROOT/'common/scripted_effects/00_scripted_effects.txt';helpers={}
    for n in nodes(source(helper_path)):
        called={c.key for c in walk(n.children()) if c.key in selectors and c.value=='yes'}
        grants=[c for c in walk(n.children()) if c.key=='add_building_construction' and field(c.children(),'instant_build')=='yes']
        buildings=sorted({field(c.children(),'type') for c in grants if tech_by_building.get(field(c.children(),'type'))})
        if called and buildings:helpers[n.key]=dict(buildings=buildings,selectors=sorted(called),instant=True)
    callers=[]
    for path in (ROOT/'common/national_focus').glob('*.txt'):
        s=source(path)
        if not any(name in s for name in helpers):continue
        for tree in nodes(s):
            if tree.key!='focus_tree' or field(tree.children(),'id') not in active:continue
            tree_id=field(tree.children(),'id')
            hashes[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
            for focus in tree.children():
                if focus.key!='focus':continue
                for n in walk(focus.children()):
                    if n.key in helpers and n.value=='yes':
                        callers.append(dict(tree=tree_id,focus=field(focus.children(),'id'),file=path.relative_to(ROOT).as_posix(),line=s.count('\n',0,n.start)+1,helper=n.key,**helpers[n.key]))
    OUT.mkdir(parents=True,exist_ok=True)
    hashes[Path(__file__).relative_to(ROOT).as_posix()]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (OUT/'CANDIDATES.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',scope='All nonshared-state slot queries without explicit province. Candidate matches only; verify actual focus contract and current technology before declaring a defect.',parse_errors=parse_errors,candidates=candidates),indent=2)+'\n',encoding='utf-8')
    (OUT/'TECH_UNLOCKS.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',enables=techs),indent=2)+'\n',encoding='utf-8')
    result=dict(project='IMPERIA COLD WAR',scope='Read-only source inventory. Direct and native-helper queries are candidates; deferred construction and researched technology contracts require separate review.',candidate_queries=len(candidates),candidate_files=len({r['file'] for r in candidates}),active1970_tree_ids=sorted(active),native_helper_callers=callers,direct_active1970_candidates=[r for r in candidates if r['active1970_direct_tree']],source_hashes=hashes,parse_errors=parse_errors,runtime_files_modified=0,native_engine_tested=False)
    (OUT/'INVENTORY.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(candidate_queries=len(candidates),candidate_files=result['candidate_files'],parse_errors=parse_errors,active1970_trees=len(active),direct_native_helper_calls=len(callers),unique_helper_focuses=len({r['focus'] for r in callers}),by_tree=dict(Counter(r['tree'] for r in callers))),indent=2))

if __name__=='__main__':main()
