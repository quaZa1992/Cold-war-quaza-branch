# IMPERIA COLD WAR — Bounded Syrian, Libyan and generic grant repairs.
from pathlib import Path
import hashlib
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from building_grants import grants as G
from focus_prerequisite_ui import nodes,field

SYR_FOCI={'COLDWAR_SYR_agriculture_09','COLDWAR_SYR_infrastructure_09','COLDWAR_SYR_infrastructure_11'}
SYR_PATHS={'common/national_focus/COLDWAR_SYR_1970_focus.txt','common/scripted_effects/COLDWAR_SYR_focus_rewards.txt','common/decisions/COLDWAR_SYR_deferred_projects.txt','events/COLDWAR_SYR_foreign_events.txt'}

def _syria_fragment(text):
    return G.add_missing_slots(G.require_physical_owner(G.rewrite_queries(text,{'infrastructure','renewable_energy_infra'}),'SYR'))

def _foreign_project_preview(text):
    """Mirror escrow-funded assets with nonexecuting native option effects."""
    event=nodes(text)[0];edits=[]
    for option in event.children():
        if option.key!='option':continue
        name=field(option.children(),'name');raw=text[option.start:option.end]
        updates={'custom_effect_tooltip':''}
        if name in {'COLDWAR_SYR_FOREIGN.22.option_b','COLDWAR_SYR_FOREIGN.22.option_c'}:
            state,building=('186','industrial_complex') if name.endswith('_b') else ('189','infrastructure')
            updates['effect_tooltip']=G.block('effect_tooltip',G.block(state,G._grant(building)))
        replacement=G._fields(raw,updates)
        edits.append((option.start,option.end,replacement))
    for a,b,new in sorted(edits,reverse=True):text=text[:a]+new+text[b:]
    return text

def repair_syria_output(path,text):
    path=str(path).replace('\\','/')
    if path not in SYR_PATHS:return text
    ast=nodes(text);selected=[]
    if path.startswith('common/national_focus'):
        for tree in ast:
            if tree.key=='focus_tree':selected=[n for n in tree.children() if n.key=='focus' and field(n.children(),'id') in SYR_FOCI]
    elif path.startswith('common/scripted_effects'):
        selected=[n for n in ast if n.key in {k+'_implement' for k in SYR_FOCI}]
    elif path.startswith('common/decisions'):
        selected=[n for root in ast for n in root.children() if n.key in {k+'_resume' for k in SYR_FOCI}]
    else:selected=[n for n in ast if n.key=='country_event' and field(n.children(),'id')=='COLDWAR_SYR_FOREIGN.22']
    expected=1 if path.startswith('events') else 3
    assert len(selected)==expected,(path,len(selected),expected)
    for n in sorted(selected,key=lambda n:n.start,reverse=True):
        fragment=text[n.start:n.end];replacement=_syria_fragment(fragment)
        if path.startswith('events'):replacement=_foreign_project_preview(replacement)
        replacement=G.normal(replacement)
        prefix=text[text.rfind('\n',0,n.start)+1:n.start]
        prefix=prefix if not prefix.strip() else ''
        replacement=replacement.replace('\n','\n'+prefix)
        text=text[:n.start]+replacement+text[n.end:]
    if not text.startswith('# IMPERIA COLD WAR —'):text=G.MARK+text
    return text

def install():
    paths=list(sorted(SYR_PATHS));changed=[];hashes={}
    for path in paths:
        p=G.ROOT/path;text=p.read_text(encoding='utf-8-sig');new=repair_syria_output(path,text)
        assert repair_syria_output(path,new)==new,path
        if new!=text:p.write_text(new,encoding='utf-8',newline='\n');changed.append(path)
        hashes[path]=hashlib.sha256(p.read_bytes()).hexdigest()
    for tag in ('GENERIC1970','LBA'):
        path=G.scope()[tag]['tree'];p=G.ROOT/path;text=p.read_text(encoding='utf-8-sig');new=G.repair_focus_tree(tag,text)
        assert G.repair_focus_tree(tag,new)==new,tag
        if new!=text:p.write_text(new,encoding='utf-8',newline='\n');changed.append(path)
        hashes[path]=hashlib.sha256(p.read_bytes()).hexdigest()
    changed+=G.write_outputs()
    doc=G.ROOT/'docs/design/building_capacity_audit_20261027'
    result=dict(project='IMPERIA COLD WAR',changed=changed,hashes=hashes,scope='Three Syrian domestic programmes, the consented foreign project delivery, 37 reviewed generic focuses and one Libyan programme. Existing receipts and fees are retained.',native_engine_tested=False)
    (doc/'REMAINING_IMPLEMENTATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':install()
