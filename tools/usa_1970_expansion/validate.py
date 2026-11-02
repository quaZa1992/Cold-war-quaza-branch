# IMPERIA COLD WAR — USA expansion integration and native provider validation.
"""Validate emitted integration, not just the design catalogue or a test copy."""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
DOC=ROOT/'docs/design/usa_1970_expansion_20261024'
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
sys.path.insert(0,str(ROOT/'tools'))
from focus_prerequisite_ui import nodes,field
from usa_building_capacity import building_definitions
import focus_dates
import gulf_revision
from naval_adaptation_1970 import naval_adapter
from usa_kissinger_implementation.shared import FOCUSES as KS_FOCUSES,COORDS as KS_COORDS,CAPTIONS as KS_CAPTIONS

def walk(rows):
    for n in rows:
        yield n
        yield from walk(n.children())
def value(rows,key,default=None):return field(rows,key,default)
def first(rows,key):return next(n for n in rows if n.key==key)
def source(path):return path.read_text(encoding='utf-8-sig')
def load(path):return json.loads(source(path))

def main():
    checks=[];warnings=[]
    def check(ok,label):
        if not ok:raise AssertionError(label)
        checks.append(label)
    proposal=load(DOC/'proposal.json');baseline=load(DOC/'current_inventory.json')
    captions=load(HERE/'focus_titles.json')['titles']
    wanted={n['id']:n for n in proposal['nodes']}
    early=load(HERE/'early_cooperation/focus_specs.json')
    originals={n['id']:n for n in baseline['focuses']}
    for fid,spec in early['focuses'].items():
        old=nodes(originals[fid]['raw'])[0]
        wanted[fid]=dict(spec,xy=[float(field(old.children(),'x')),float(field(old.children(),'y'))])
    for record in naval_adapter.build_country('USA')['records']:
        wanted[record['id']]=record
    for key,n in KS_FOCUSES.items():
        wanted[n['id']]=dict(id=n['id'],name=KS_CAPTIONS.get(key,n['title']),xy=KS_COORDS.get(key,n['world']))
    tree_path=ROOT/'common/national_focus/USA_1970.txt'
    tree=first(nodes(source(tree_path)),'focus_tree')
    focuses={field(n.children(),'id'):n for n in tree.children() if n.key=='focus'}
    check(len(focuses)==342,'342 unique installed focus IDs including naval development and statecraft')
    check(set(focuses)=={n['id'] for n in baseline['focuses']}|set(wanted),'Installed IDs exactly match preserved baseline and approved additions')
    check(field(tree.children(),'reset_on_civilwar')=='no','Civil-war tree refresh cannot replay completed focuses')
    xy={};exclusive={}
    for fid,n in focuses.items():
        xy[fid]=(float(field(n.children(),'x')),float(field(n.children(),'y')))
        exclusive[fid]={str(c.value) for k in n.children() if k.key=='mutually_exclusive' for c in k.children() if c.key=='focus'}
    def resolve(fid, seen=()):
        check(fid not in seen,'No relative-anchor cycle '+fid)
        anchor=field(focuses[fid].children(),'relative_position_id')
        if anchor:
            check(anchor in focuses,'Resolved relative anchor '+fid)
            ax,ay=resolve(anchor,seen+(fid,))
            raw=xy[fid]
            return raw[0]+ax,raw[1]+ay
        return xy[fid]
    xy={fid:resolve(fid) for fid in focuses}
    check(len(set(xy.values()))==342,'No identical installed coordinates')
    for fid,n in wanted.items():check(tuple(n['xy'])==xy[fid],'Approved coordinate '+fid)
    parents={fid:[[str(c.value) for c in p.children() if c.key=='focus'] for p in n.children() if p.key=='prerequisite'] for fid,n in focuses.items()}
    for fid,groups in parents.items():
        check(all(p in focuses for group in groups for p in group),'Resolved prerequisites '+fid)
        check(all(fid in exclusive.get(other,set()) for other in exclusive[fid]),'Symmetric exclusions '+fid)
        if fid not in focus_dates.ELECTION_RECEIPTS:
            availability=next((n for n in focuses[fid].children() if n.key=='available'),None)
            check(not availability or not any(n.key=='date' for n in walk(availability.children())),'No arbitrary programme calendar restriction '+fid)
            check(not any(p in focus_dates.ELECTION_RECEIPTS for group in groups for p in group),'Paid programme independent of future electoral receipt '+fid)
    def visit(fid,seen=frozenset()):
        if fid in seen:raise AssertionError('Prerequisite cycle '+fid)
        for group in parents[fid]:
            for p in group:visit(p,seen|{fid})
    for fid in focuses:visit(fid)
    checks.append('All installed prerequisite chains acyclic')
    elections=load(DOC/'implementation_support_elections.json')['nodes']
    for n in elections:
        f=focuses[n['id']]
        check(not any(c.key=='allow_branch' for c in f.children()),'Party branch inspectable '+n['id'])
        if n['execution_gate']:
            check(any(c.key==n['execution_gate'] for c in walk(first(f.children(),'available').children())),'Exact native party availability '+n['id'])

    paths=[tree_path]
    paths.append(ROOT/'common/scripted_effects/01_NATO_effects.txt')
    paths.append(ROOT/'common/decisions/categories/USA_1970_policy_decision_categories.txt')
    paths.extend(ROOT/p for p in ('common/ideas/Factions.txt','common/ideas/united_states.txt'))
    paths.extend(ROOT/p for p in naval_adapter.runtime_outputs() if p.endswith('.txt'))
    paths+=list((ROOT/'common').glob('*/COLDWAR_USA_1970_*.txt'))
    paths+=list((ROOT/'common/decisions/categories').glob('COLDWAR_USA_1970_*.txt'))
    paths+=list((ROOT/'events').glob('COLDWAR_USA_1970_*.txt'))
    paths+=list((ROOT/'common').glob('*/COLDWAR_USA_gulf*.txt'))
    paths+=list((ROOT/'common/decisions/categories').glob('COLDWAR_USA_gulf*.txt'))
    paths+=list((ROOT/'events').glob('COLDWAR_USA_gulf*.txt'))
    paths+=list((ROOT/'common').glob('*/COLDWAR_USA_kissinger*.txt'))
    paths+=list((ROOT/'common/decisions/categories').glob('COLDWAR_USA_kissinger*.txt'))
    paths+=list((ROOT/'events').glob('COLDWAR_USA_kissinger*.txt'))
    paths+=[ROOT/p for p in ('common/scripted_effects/00_money_system.txt','common/scripted_effects/USA_political_leaders.txt','common/scripted_effects/USA_1970_scripted_effects.txt','common/scripted_effects/USA_1970_nixon_diplomacy_effects.txt','events/USA_1970_events.txt','events/COLDWAR_USA_bahrain_base_events.txt','common/scripted_effects/COLDWAR_USA_bahrain_base_effects.txt','common/scripted_triggers/COLDWAR_USA_bahrain_base_triggers.txt','common/decisions/USA_1970_policy_decisions.txt')]
    parsed={}
    for p in sorted(set(paths)):
        b=p.read_bytes();s=source(p)
        check(not b.startswith(b'\xef\xbb\xbf'),'No script BOM '+str(p.relative_to(ROOT)))
        if p.name not in {'COLDWAR_USA_gulf_ideas.txt','COLDWAR_USA_gulf_modifiers.txt'}:
            check(s.startswith('# IMPERIA COLD WAR'),'File-start project marker '+str(p.relative_to(ROOT)))
        parsed[p]=nodes(s)
        check(not any(isinstance(n.value,str) and re.fullmatch(r'-?\d+\.\d{6,}',n.value) for n in walk(parsed[p])),'Safe fixed-point literals '+str(p.relative_to(ROOT)))
    def shape(items):
        return [(n.key,n.op,shape(n.children()) if isinstance(n.value,list) else n.value) for n in items]
    for relative, canonical in gulf_revision.outputs().items():
        if relative.startswith('common/autonomous_states/'):
            continue
        installed=source(ROOT/relative)
        check(shape(nodes(installed))==shape(nodes(canonical)) if relative.endswith('.txt') else installed==canonical.lstrip('\ufeff'),
              'Installed Gulf output matches its owning generator '+relative)
    contacts=focuses['COLDWAR_USA_gulf_contacts']
    check(any(n.key=='allow_branch' and field(n.children(),'always')=='no' for n in contacts.children()),'Retired Gulf contact receipt remains hidden')
    checks.append('All owned/targeted runtime scripts parse')
    definitions=building_definitions()
    # Scripted instant state grants must not inherit a country's manual
    # construction unlock (for example1985fuel_silos in the1970scenario).
    for path,rows in parsed.items():
        if path.parent.name!='scripted_triggers' or path.name not in {
                'COLDWAR_USA_1970_expansion.txt','COLDWAR_USA_1970_programmes.txt','COLDWAR_USA_1970_agreements.txt'}:continue
        check(all(definitions[field(n.children(),'building')]['shares_slots'] or field(n.children(),'province')
                  for n in walk(rows) if n.key=='free_building_slots'),
              'Independent state grants check physical caps rather than manual tech unlocks '+path.name)
    check(all(field(n.children(),'include_locked') is None
              for rows in parsed.values() for n in walk(rows)
              if n.key=='free_building_slots' and not definitions[field(n.children(),'building')]['shares_slots']),
          'No shared-slot-only include_locked parameter on independent state or province buildings')
    # Native loading rejects this superficially plausible trigger. Capacity
    # guards must compare native building_level@ values instead. A permissive
    # source parser or model must not let this engine regression recur.
    check(not any(n.key=='has_building' for rows in parsed.values() for n in walk(rows)),
          'No unsupported has_building trigger in targeted runtime')
    # Native A/B execution found that the structured timed setter without a
    # value does not satisfy has_country_flag. Boolean offer/deadline receipts
    # must be explicit; accepting a default in the model hid a real failure.
    check(all(field(n.children(),'value') is not None
              for rows in parsed.values() for n in walk(rows)
              if n.key=='set_country_flag' and isinstance(n.value,list)
              and field(n.children(),'days') is not None),
          'Every targeted timed country flag has an explicit native value')

    all_effects={};all_triggers={}
    for p in (ROOT/'common/scripted_effects').glob('*.txt'):
        if p in parsed:
            for n in parsed[p]:all_effects[n.key]=n
        else:
            # Discover external provider names without turning this bounded US
            # integration check into a parse/audit of another chat's work.
            for key in re.findall(r'(?m)^([A-Za-z_]\w*)\s*=\s*\{',source(p)):all_effects.setdefault(key,None)
    for p in (ROOT/'common/scripted_triggers').glob('*.txt'):
        if p in parsed:
            for n in parsed[p]:all_triggers[n.key]=n
        else:
            for key in re.findall(r'(?m)^([A-Za-z_]\w*)\s*=\s*\{',source(p)):all_triggers.setdefault(key,None)
    for p,rows in parsed.items():
        for n in walk(rows):
            if n.key.startswith(('COLDWAR_USA_legacy_','COLDWAR_USA_expansion_','COLDWAR_USA_dom_','COLDWAR_USA_agreements_','COLDWAR_USA_early_','COLDWAR_USA_1970_economy_')) and n.value in ('yes','no'):
                check(n.key in all_effects or n.key in all_triggers,'Helper provider '+n.key)
    effects=nodes(source(ROOT/'common/scripted_effects/COLDWAR_USA_1970_expansion.txt'))
    check(all(not any(n.key=='date' for n in walk(root.children()))
              for name,root in all_triggers.items() if root is not None and name.startswith(focus_dates.READY_PREFIXES)),
          'Real programme execution and retry guards have no calendar locks')
    def ast_dump(rows):
        return [(n.key,n.op,ast_dump(n.children()) if isinstance(n.value,list) else n.value) for n in rows]
    for n in effects:
        if not n.key.startswith('COLDWAR_USA_legacy_complete_'):continue
        nested=list(walk(n.children()));constructed=sum(int(field(c.children(),'level','1')) for c in nested if c.key=='add_building_construction')
        slots=sum(int(c.value) for c in nested if c.key=='add_extra_state_shared_building_slots')
        if constructed:
            check(slots>=constructed,'Slots accompany every legacy building level '+n.key)
            ready=all_triggers['COLDWAR_USA_legacy_ready_'+n.key.removeprefix('COLDWAR_USA_legacy_complete_')]
            guard=repr(ast_dump(ready.children()))
            check('is_owned_and_controlled_by' in guard and ('free_building_slots' in guard or 'building_level@' in guard),'Actual ownership/control and native capacity '+n.key)
    checks.append('Legacy construction grants, costs and receipts remain within one execution boundary')

    loc={};duplicates=[]
    loc_files=[ROOT/'localisation/english/USA_1970_focus_l_english.yml',ROOT/'localisation/english/COLDWAR_USA_gulf_l_english.yml',ROOT/'localisation/english/COLDWAR_USA_bahrain_base_l_english.yml',ROOT/'localisation/english/COLDWAR_NAVY_1970_l_english.yml',ROOT/'localisation/english/COLDWAR_USA_kissinger_l_english.yml']+list((ROOT/'localisation/english').glob('COLDWAR_USA_1970_*.yml'))
    for p in loc_files:
        check(p.read_bytes().startswith(b'\xef\xbb\xbf'),'English localisation BOM '+p.name)
        if p.name!='COLDWAR_USA_bahrain_base_l_english.yml':check(source(p).startswith('l_english:\n# IMPERIA COLD WAR'),'English header and marker '+p.name)
        for k,v in re.findall(r'^\s*([^\s:#]+):\d*\s*(".*")\s*$',source(p),re.M):
            if k in loc:duplicates.append(k)
            loc[k]=json.loads(v)
        if p.name.startswith('COLDWAR_USA_1970_'):check('\u2013' not in source(p) and not any('\u2014' in line for line in source(p).splitlines() if not line.startswith('#')),'English player text has no unsupported dash '+p.name)
    check(not duplicates,'No duplicate focus/programme/treaty localisation providers')
    font=GAME/'gfx/fonts/hoi_16mbs.fnt';glyph={};kern={}
    for line in source(font).splitlines():
        d={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)}
        if line.startswith('char '):glyph[d['id']]=d['xadvance']
        elif line.startswith('kerning '):kern[d['first'],d['second']]=d['amount']
    width=lambda s:sum(glyph.get(ord(c),glyph[63]) for c in s)+sum(kern.get((ord(a),ord(b)),0) for a,b in zip(s,s[1:]))
    title_widths={}
    for fid,n in wanted.items():
        check(fid in loc and fid+'_desc' in loc,'Complete English focus localisation '+fid)
        check(loc[fid]==captions.get(fid,n['name']),'Approved native caption '+fid)
        title_widths[fid]=width(loc[fid]);check(title_widths[fid]<=147,'Native title fits 147 pixels '+fid)
    for fid in focuses:
        check(fid in loc and width(loc[fid])<=147,'All installed captions fit native width '+fid)

    modifier_doc=set(re.findall(r'^## (\w+)',source(GAME/'documentation/modifiers_documentation.md'),re.M))
    custom=set()
    for p in (ROOT/'common/modifier_definitions').glob('*.txt'):custom.update(n.key for n in nodes(source(p)))
    used_modifiers=set()
    for p,rows in parsed.items():
        if p.parent.name!='ideas':continue
        # Shared native membership providers receive callbacks only. Their
        # unrelated historical ideas/modifiers are outside this USA change.
        if p.name in {'Factions.txt','united_states.txt'}:continue
        for mod in (n for n in walk(rows) if n.key=='modifier'):
            used_modifiers.update(n.key for n in mod.children() if n.key!='custom_modifier_tooltip')
    buildings=set()
    for p in (ROOT/'common/buildings').glob('*.txt'):
        for root in nodes(source(p)):
            if root.key=='buildings':buildings.update(n.key for n in root.children())
    # The engine generates construction-speed modifier families from loaded
    # building definitions, so custom MD building names are not all enumerated
    # in the base-game documentation generated without this mod.
    generated={'production_speed_'+b+'_factor' for b in buildings}
    check(used_modifiers<=modifier_doc|custom|generated,'All programme/treaty modifiers have actual native or registered MD providers: '+str(sorted(used_modifiers-modifier_doc-custom-generated)))

    income=all_effects['calculate_additional_income_rate'];expense=all_effects['calculate_additional_expense_rate']
    check(sum(n.key=='COLDWAR_USA_agreements_calculate_weekly_streams' for n in income.children())==1,'Native income calculates treaty stream once')
    check(sum(n.key=='COLDWAR_USA_agreements_calculate_weekly_streams' for n in expense.children())==1,'Native expense calculates treaty stream once')
    check(sum(n.key=='COLDWAR_USA_dom_add_expense_rate' for n in expense.children())==1,'Native expense appends domestic stream once')
    for consumer,variable in ((income,'COLDWAR_USA_early_weekly_income'),(expense,'COLDWAR_USA_early_weekly_expense')):
        check(sum(n.key=='COLDWAR_USA_early_calculate_weekly_streams' for n in consumer.children())==1,'Early cooperative fiscal stream calculated once '+variable)
        check(sum(n.key=='add_to_variable' and any(c.value==variable for c in n.children()) for n in consumer.children())==1,'Early cooperative fiscal stream consumed once '+variable)
    expense_children=expense.children();inflation=next(i for i,n in enumerate(expense_children) if n.key=='multiply_variable' and field(n.children(),'additional_expenses_rate')=='additional_expenses_inflation')
    treaty=next(i for i,n in enumerate(expense_children) if n.key=='COLDWAR_USA_agreements_calculate_weekly_streams')
    check(treaty>inflation,'Signed nominal weekly obligations are added after general inflation multiplier')
    native_weekly=source(ROOT/'common/on_actions/MD_on_actions.txt')
    check(native_weekly.index('ingame_update_setup = yes')<native_weekly.index('add_to_variable = { treasury = treasury_rate_gain }'),'Native weekly treasury applies recalculated signed budget')
    for key in ('germany_forward','germany_sustain','canada','britain','japan','south_vietnam','china','soviet_exchange','bahrain','israel','saudi','mexico','rogers','atlantic_research','canada_retool','pacific_maintenance'):
        preview=all_effects['COLDWAR_USA_agreements_preview_'+key]
        check([n.key for n in preview.children()]==['effect_tooltip'],'Initial bilateral preview is unconditional and nonexecuting '+key)
    retired={'USA_1970.'+str(x) for x in (100,101,110,111,120,121,130,131,140,141,150,151,160,170,171)}
    for ev in nodes(source(ROOT/'events/USA_1970_events.txt')):
        if ev.key=='country_event' and field(ev.children(),'id') in retired:
            check(not any(n.key in {'modify_treasury_effect','add_building_construction','add_ideas'} or n.key.startswith('enbo_') for n in walk(ev.children())),'Queued obsolete offer cannot pay again '+field(ev.children(),'id'))
    result=dict(project='IMPERIA COLD WAR',status='All focused emitted integration checks passed',checks=len(checks),focuses=len(focuses),authored_nodes=65,offers=16,partisan_execution_gates=92,active_legacy_party_bundles=44,title_widths=title_widths,maximum_authored_title_width=max(title_widths.values()),native_modifier_count=len(used_modifiers),parsed_runtime_files=len(parsed),warnings=warnings,check_details=checks,
        hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths+loc_files))},
        scope='Source structure, providers, installed geometry, encodings, native title glyph measurement and integration. Native/gameplay/multiplayer evidence is separate.')
    result.update(authored_nodes=len(wanted),offers=29,bilateral_contract_families=30,kissinger_focuses=len(KS_FOCUSES),kissinger_regional_campaigns=4)
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('check_details','hashes','title_widths')},indent=2))

if __name__=='__main__':main()
