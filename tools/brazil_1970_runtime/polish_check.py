# IMPERIA COLD WAR — Brazil-only polish scope and unchanged gameplay verification.
from common import ROOT,HERE
from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(ROOT/'tools'))
from focus_prerequisite_ui import nodes

def shape(n):return (n.key,[shape(x) for x in n.children()] if isinstance(n.value,list) else n.value)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    baseline=json.loads((HERE/'POLISH_BASELINE.json').read_text());model=json.loads((HERE/'runtime_design.json').read_text());m=json.loads((HERE/'manifest.json').read_text())
    canonical=[{k:n.get(k) for k in ('id','group','x','y','anchor','offset','prerequisites','exclusions','conditions','cost','effects','offer')} for n in model['nodes']]
    errors=[]
    if hashlib.sha256(json.dumps(canonical,sort_keys=True).encode()).hexdigest()!=baseline['gameplay_sha256']:errors.append('Gameplay changed')
    changed=[p for p,h in baseline['runtime_files'].items() if sha(ROOT/p)!=h]
    foreign=[p for p in changed if 'COLDWAR_BRA' not in p]
    if foreign:errors.append('Non-Brazil runtime changes: '+str(foreign))
    snapshot=Path(baseline['native_evidence']['run'])/'fixture'
    effect_drift=[];new_helpers=[]
    for rel in baseline['runtime_files']:
        if not rel.startswith('common/scripted_effects/') or 'COLDWAR_BRA' not in rel:continue
        before={n.key:shape(n) for n in nodes((snapshot/rel).read_text(encoding='utf-8-sig'))}
        after={n.key:shape(n) for n in nodes((ROOT/rel).read_text(encoding='utf-8-sig'))}
        effect_drift += [key for key in before if key not in after or before[key]!=after[key]]
        new_helpers += [key for key in after if key not in before]
    if effect_drift:errors.append('Existing gameplay helper changed: '+str(effect_drift))
    if any('_preview_' not in key for key in new_helpers):errors.append('New non-preview helper')
    report=dict(project='IMPERIA COLD WAR',feature='Brazil-only polish',changed_runtime_files=changed,non_brazil_runtime_changes=foreign,approved_gameplay_preserved=not errors,existing_effect_helper_changes=effect_drift,new_display_helpers=new_helpers,focuses=len(model['nodes']),distinct_focus_icons=len({n['icon'] for n in model['nodes']}),icon_selections_changed=model['presentation_polish']['focus_icon_changes'],english_overrides=model['presentation_polish']['english_overrides'],images='User owns further image work. No proposed event photograph replacement was applied.',errors=errors)
    (HERE/'POLISH_CHECK.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));return int(bool(errors))
if __name__=='__main__':sys.dont_write_bytecode=True;sys.exit(main())
