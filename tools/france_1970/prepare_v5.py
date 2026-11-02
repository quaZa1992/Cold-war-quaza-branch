# IMPERIA COLD WAR — Freeze the user-approved V5 design and preserve the V4 runtime.
import hashlib
import json
import shutil
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
source=HERE/'proposal_v5/proposal.json'
target=HERE/'approved_design_v5.json'
data=source.read_bytes()
if target.exists():
    assert target.read_bytes()==data,'Approved V5 input already differs; do not overwrite it.'
else:
    target.write_bytes(data)
archive=HERE/'archive_v4/runtime'
snapshots=[]
for folder,suffix in [('common/national_focus','txt'),('common/scripted_effects','txt'),('common/scripted_triggers','txt'),('common/dynamic_modifiers','txt'),('common/ideas','txt'),('common/on_actions','txt'),('common/decisions','txt'),('common/decisions/categories','txt'),('events','txt'),('interface','gfx'),('localisation/english','yml')]:
    for path in (ROOT/folder).glob('COLDWAR_FRA_1970*.'+suffix):
        # Preserve the original files only; re-running preparation never replaces them.
        if '_v5_' in path.name:continue
        relative=path.relative_to(ROOT)
        saved=archive/relative
        if not saved.exists():
            saved.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(path,saved)
        snapshots.append({'path':relative.as_posix(),'sha256':hashlib.sha256(saved.read_bytes()).hexdigest()})
record={'project':'IMPERIA COLD WAR','approval_date':'2026-10-23','authorization':'baue das alles ein genau wie du es vorberietet hast','source':'proposal_v5/proposal.json','frozen_input':target.name,'sha256':hashlib.sha256(data).hexdigest(),'scope':{'focuses':260,'country_offers':50,'domestic_reworked_packages':96},'v4_approved_input_preserved':hashlib.sha256((HERE/'approved_design.json').read_bytes()).hexdigest(),'v4_runtime_archive':snapshots}
(HERE/'V5_APPROVAL.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'approved_sha256':record['sha256'],'archived_files':len(snapshots)}))
