# IMPERIA CW — Cold War: vietnam 1970 — check rebuild.
"""Check one repeat build and preserve the current versions of shared/manual files."""
from pathlib import Path
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
m=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
manual=set(m['politics_sources']+m['politics_integration']+m['integration'])
paths=set(m['generated'])|manual|{str(p.relative_to(ROOT)).replace('\\','/') for p in HERE.glob('*.json') if p.name in {'approved_design.json','approved_campaigns.json','manifest.json','focus_timing.json','campaign_defence_overrides.json','reward_rework.json'}}
def hashes():return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(paths)}
before=hashes()
result=subprocess.run([sys.executable,'-X','utf8',str(HERE/'compile.py')],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
assert result.returncode==0,result.stderr
after=hashes();changed=[p for p in before if before[p]!=after[p]]
report=dict(status='pass' if not changed else 'fail',files_checked=len(paths),changed=changed,manual_files_preserved=all(before[p]==after[p] for p in manual),engine_tested=False)
(HERE/'rebuild_check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2));raise SystemExit(bool(changed))
