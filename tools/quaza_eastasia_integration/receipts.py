# IMPERIA COLD WAR — Final shared-output receipts after reviewed East Asia integration.
"""Update only known shared ownership records; never rebuild unrelated features."""
from pathlib import Path
import hashlib
import json
from source import ROOT, REPORT, DONOR


def digest(relative):
    return hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()


def reconcile():
    changes=[]
    path=ROOT/'tools/north_korea_1970/emission_manifest.json'
    if path.exists():
        doc=json.loads(path.read_text(encoding='utf-8'))
        doc['project']='IMPERIA COLD WAR'
        doc['integration_owner']='tools/quaza_eastasia_integration/apply_reviewed.py'
        doc['rebuild_sequence']='NKO compiler, current KOR staging, reviewed integration apply'
        doc['output_sha256']={p:digest(p) for p in doc['root_outputs']}
        path.write_text(json.dumps(doc,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'tools/ssr_1970/manifest.json'
    doc=json.loads(path.read_text(encoding='utf-8'))
    targets={'common/scripted_effects/00_money_system.txt','common/scripted_effects/mdcw_1970_focus_tree_effects.txt'}
    for key,old in doc['outputs'].items():
        if Path(key).as_posix() in targets:
            new=digest(key)
            if new!=old:changes.append({'path':Path(key).as_posix(),'previous_sha256':old,'current_sha256':new})
            doc['outputs'][key]=new
    if changes:
        doc.setdefault('reviewed_shared_integrations',[]).append({'project':'IMPERIA COLD WAR','feature':'quaZa East Asia and nuclear readiness','source_commit':DONOR,'paths':changes})
        path.write_text(json.dumps(doc,indent=2)+'\n',encoding='utf-8')
    history=[r for r in doc.get('reviewed_shared_integrations',[]) if r.get('source_commit')==DONOR]
    (REPORT/'SHARED_RECEIPTS.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','source_commit':DONOR,'updated_this_run':changes,'ssr_shared_receipt_history':history,'scope':'Only final shared-file hash receipts. No SSR content or gameplay changed; no full SSR verification claim.'},indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    reconcile()
