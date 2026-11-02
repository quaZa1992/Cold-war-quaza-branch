# IMPERIA COLD WAR — Canonical ordered East Asia regeneration and parity check.
"""Run after stopping the game; private shared-file backups/staging stay on E:."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
from source import ROOT, REPORT


def main():
    old=json.loads((REPORT/'ENGINE_REPORT.json').read_text(encoding='utf-8'))
    paths=set(old['source_sha256'])
    before={p:(ROOT/p).read_bytes() for p in paths}
    commands=[
        'tools/north_korea_1970/compile.py',
        'tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_runtime.py',
        'tools/japan_1970/build_diplomatic_runtime.py',
        'tools/japan_1970/stage_focus_graph.py',
        'tools/quaza_eastasia_integration/apply_reviewed.py',
    ]
    # The explicit later reward revision owns all country writer stages.
    if (ROOT/'tools/reward_rework_20261027/apply.py').is_file():
        commands=['tools/reward_rework_20261027/apply.py']
    results=[]
    for path in commands:
        r=subprocess.run([sys.executable,'-B',path],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        results.append({'command':[sys.executable,'-B',path],'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
        if r.returncode:break
    sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
    from script_ast import parse
    changed=[];semantic=[]
    for p,raw in before.items():
        new=(ROOT/p).read_bytes()
        if raw==new:continue
        row={'path':p,'previous_sha256':hashlib.sha256(raw).hexdigest(),'current_sha256':hashlib.sha256(new).hexdigest()}
        if p.endswith(('.txt','.gfx','.gui')):
            row['ast_equal']=parse(raw.decode('utf-8-sig'))==parse(new.decode('utf-8-sig'))
        elif p.endswith('.yml'):
            row['text_equal']=raw.decode('utf-8-sig').replace('\r\n','\n')==new.decode('utf-8-sig').replace('\r\n','\n')
        else:row['ast_equal']=False
        changed.append(row)
        if not (row.get('ast_equal') or row.get('text_equal')):semantic.append(p)
    result={'project':'IMPERIA COLD WAR','commands':results,'changed':changed,'semantic_changes':semantic,'success':all(r['exit_code']==0 for r in results) and not semantic,'scope':'Ordered source regeneration. AST equality is a source comparison, not an additional engine execution. Immutable approval snapshots are not replaced.'}
    (REPORT/'REBUILD.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'success':result['success'],'changed':changed,'semantic_changes':semantic}))
    return not result['success']


if __name__=='__main__':raise SystemExit(main())
