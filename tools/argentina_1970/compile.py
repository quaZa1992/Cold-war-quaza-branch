# IMPERIA COLD WAR — Bounded Argentina 1970 runtime installation.
"""Compile the immutable approved design and patch only named integration points."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, re, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
REPORT=ROOT/'docs/design/COLDWAR_ARG_1970'
MARK='# IMPERIA COLD WAR — Argentina 1970 custom integration.\n'
sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,format_code
from core import runtime_design,build as build_core

def module(name):
    spec=importlib.util.spec_from_file_location('argentina_1970_'+name,HERE/(name+'.py'))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def section(text,name,body,anchor=None):
    start='# IMPERIA COLD WAR — ARG '+name+' BEGIN'
    end='# IMPERIA COLD WAR — ARG '+name+' END'
    replacement=start+'\n'+body.rstrip()+'\n'+end
    if start in text:
        a=text.index(start);b=text.index(end,a)+len(end)
        return text[:a]+replacement+text[b:]
    if anchor is None:return text.rstrip()+'\n\n'+replacement+'\n'
    if text.count(anchor)!=1:raise ValueError(('Nonunique integration anchor',name,anchor,text.count(anchor)))
    return text.replace(anchor,replacement+'\n'+anchor,1)

def find_braced(text,start):
    opening=text.index('{',start);depth=1;i=opening+1;quoted=False;comment=False;escaped=False
    while depth and i<len(text):
        c=text[i]
        if comment:
            if c=='\n':comment=False
        elif quoted:
            if escaped:escaped=False
            elif c=='\\':escaped=True
            elif c=='"':quoted=False
        elif c=='#':comment=True
        elif c=='"':quoted=True
        elif c=='{':depth+=1
        elif c=='}':depth-=1
        i+=1
    if depth:raise ValueError('Unclosed integration block')
    return opening,i-1

def shared_sources():
    result={};original={}
    def read(rel):
        path=ROOT/rel;raw=path.read_bytes();original[rel]=hashlib.sha256(raw).hexdigest()
        return raw.decode('utf-8-sig')
    def keep(rel,s):
        if not s.startswith(MARK):s=MARK+s
        parse(s);result[rel]=s
    rel='history/countries/ARG - Argentina.txt';s=read(rel)
    if 'COLDWAR_ARG_INITIAL_HISTORY_BEGIN' not in s:
        old='load_focus_tree = mdcw_1970_generic_focus'
        if s.count(old)!=1:raise ValueError('ARG history fallback changed; review')
        s=s.replace(old,'# COLDWAR_ARG_INITIAL_HISTORY_BEGIN\n\t\tload_focus_tree = COLDWAR_ARG_1970_focus\n\t\t# COLDWAR_ARG_INITIAL_HISTORY_END',1)
    # The junta has no civilian Peronist coalition partner in January 1970.
    start=s.index('1970.1.1 =');a,b=find_braced(s,start)
    chunk=s[a:b]
    if 'add_to_array = { gov_coalition_array = 13 }' in chunk:
        chunk=chunk.replace('add_to_array = { gov_coalition_array = 13 }','# IMPERIA COLD WAR — ARG military government has no civilian PJ coalition partner.',1)
        s=s[:a]+chunk+s[b:]
    keep(rel,s)
    rel='common/scripted_effects/mdcw_1970_focus_tree_effects.txt';s=read(rel)
    body='if = { limit = { tag = ARG IMP_is_1970_scenario = yes } COLDWAR_ARG_initialize = yes }'
    s=section(s,'AUTHORED FALLBACK',body,'mdcw_load_1970_fallback_tree = {') if False else s
    if '# IMPERIA COLD WAR — ARG AUTHORED FALLBACK BEGIN' not in s:
        at=s.index('{',s.index('mdcw_load_1970_fallback_tree ='))+1
        s=s[:at]+'\n'+section('','AUTHORED FALLBACK',body)+s[at:]
    if '# IMPERIA COLD WAR — ARG FALLBACK EXEMPTION BEGIN' not in s:
        needle='\t\t\t\tOR = {'
        if s.count(needle)!=1:raise ValueError('Fallback exemption anchor changed')
        s=s.replace(needle,needle+'\n'+section('','FALLBACK EXEMPTION','AND = { tag = ARG IMP_is_1970_scenario = yes }'),1)
    keep(rel,s)
    rel='common/scripted_effects/00_money_system.txt';s=read(rel)
    # Patch the actual aggregators, not similarly named helpers or copies.
    for func,call in [('calculate_additional_income_rate','COLDWAR_ARG_add_weekly_income'),('calculate_additional_expense_rate','COLDWAR_ARG_add_weekly_expenses')]:
        m=re.search(r'^'+func+r'\s*=\s*\{',s,re.M)
        if not m:raise ValueError('Missing native money aggregator '+func)
        a,b=find_braced(s,m.start());body=s[a+1:b]
        body=section(body,func.upper(),call+' = yes')
        s=s[:a+1]+body+s[b:]
    keep(rel,s)
    rel='common/scripted_effects/ARG_political_leaders.txt';s=read(rel)
    if '# IMPERIA COLD WAR — ARG LEADER ROUTING BEGIN' not in s:
        m=re.search(r'^set_leader_ARG\s*=\s*\{',s,re.M);a,b=find_braced(s,m.start());legacy=s[a+1:b]
        route='if = { limit = { COLDWAR_ARG_is_scenario = yes }\nif = { limit = { has_variable = COLDWAR_ARG_leader_routed_party NOT = { check_variable = { var = COLDWAR_ARG_leader_routed_party value = ruling_party compare = equals } } } set_country_flag = COLDWAR_ARG_leader_transition_authorized }\nCOLDWAR_ARG_select_leader_for_current_party = yes\n}\nelse = {\n'+legacy+'\n}'
        s=s[:a+1]+'\n'+section('','LEADER ROUTING',route)+s[b:]
    keep(rel,s)
    rel='common/scripted_triggers/mdcw_historical_retirement_alternatives.txt';s=read(rel)
    if '# IMPERIA COLD WAR — ARG RETIREMENT GUARD BEGIN' not in s:
        at=s.index('{',s.index('MDCW_HP_retirement_has_alternative ='))+1
        # Preserve actual incumbents; succession is handled by real country events and ballots.
        s=s[:at]+'\n'+section('','RETIREMENT GUARD','NOT = { COLDWAR_ARG_is_scenario = yes }')+s[at:]
    keep(rel,s)
    rel='common/scripted_triggers/IMP_1970_party_name_triggers.txt';s=read(rel)
    old='AND = { original_tag = ARG AND = { has_variable = ruling_party check_variable = { ruling_party = 22 } } }'
    if old in s:s=s.replace(old,'# IMPERIA COLD WAR — ARG approved 1970 party registry remains the local identity under every governing programme.\n\t\tAND = { original_tag = ARG has_variable = ruling_party }',1)
    keep(rel,s)
    rel='events/MD_Elections.txt';s=read(rel)
    if '# IMPERIA COLD WAR — ARG NATIVE BALLOT BEGIN' not in s:
        m=re.search(r'(?m)^\tid\s*=\s*MD4_election\.0\s*$',s)
        if not m:raise ValueError('Missing native MD4_election.0 event definition')
        a,b=find_braced(s,s.index('hidden_effect',m.end()))
        body=s[a+1:b];needle='hold_elections = yes';split=body.index(needle)+len(needle)
        prefix,tail=body[:split],body[split:]
        replacement=prefix+'\n'+section('','NATIVE BALLOT','if = { limit = { COLDWAR_ARG_is_scenario = yes } COLDWAR_ARG_record_native_election = yes }')+tail
        s=s[:a+1]+replacement+s[b:]
    keep(rel,s)
    return result,original

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--install',action='store_true');args=ap.parse_args()
    approved=(HERE/'approved_design.json').read_bytes();record=json.loads((HERE/'APPROVAL_RECORD.json').read_text())
    assert hashlib.sha256(approved).hexdigest()==record['approved_sha256'],'Immutable approved input changed'
    design=runtime_design(json.loads(approved));outputs=build_core(ROOT,design)
    for name in ('politics','treaties'):
        generated=module(name).build(ROOT,design)
        assert not set(outputs)&set(generated),(name,set(outputs)&set(generated))
        outputs.update(generated)
    art=module('event_art').build(ROOT,design)
    shared,oldhashes=shared_sources();outputs.update(shared)
    for rel,text in outputs.items():
        text=text.lstrip('\ufeff')
        if rel in shared:
            current=(ROOT/rel).read_text(encoding='utf-8-sig')
            # Retain other country integrations' comments when the actual script
            # already contains the same Argentina integration and native bodies.
            if parse(text)==parse(current):text=current
        if rel.endswith('.txt'):
            # Canonicalize owned files only. Shared native files retain upstream whitespace/comments.
            if rel not in shared:text=text.split('\n',1)[0]+'\n'+format_code(text)
            parse(text)
            if re.search(r'(?m)^\s*_(?:bare|list)\s*=',text):raise ValueError('Invalid parser sentinel '+rel)
        if rel.endswith('.yml'):
            assert text.startswith('l_english:\n# IMPERIA COLD WAR'),rel
            for line in text.splitlines()[2:]:
                if line.lstrip().startswith('#') or not line.strip():continue
                if not re.match(r'^\s+[A-Za-z0-9_.\-]+:\d+\s+"',line):raise ValueError(('Bad localisation',rel,line))
        else:assert text.startswith('# IMPERIA COLD WAR'),rel
        outputs[rel]=text
    if args.install:
        # Detect changes by another task between reading a shared file and this write.
        for rel,h in oldhashes.items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,('Concurrent shared edit',rel)
        for rel,text in outputs.items():
            path=ROOT/rel;path.parent.mkdir(parents=True,exist_ok=True)
            raw=text.encode('utf-8-sig' if rel.endswith('.yml') else 'utf-8')
            if not path.exists() or path.read_bytes()!=raw:path.write_bytes(raw)
        (HERE/'runtime_design.json').write_text(json.dumps(design,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        previews=module('preview').build_preview(ROOT,design)
        manifest=dict(project='IMPERIA COLD WAR',approved_sha256=record['approved_sha256'],files={rel:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() for rel in outputs},art=art,adjustments=design['implementation_adjustments'],previews={k:dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for k,p in previews.items()})
        (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(dict(project='IMPERIA COLD WAR',mode='installed' if args.install else 'checked',files=len(outputs),focuses=len(design['nodes']),agreements=len(design['agreements']),events=len(design['events']),decision_contracts=len(design['decisions'])),ensure_ascii=False))

if __name__=='__main__':main()
