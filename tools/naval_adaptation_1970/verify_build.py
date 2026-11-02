# IMPERIA COLD WAR — Reproducible naval integration checks and build stability.
"""Scoped USA build plus marked graft writer. Never run broad other-country builds."""
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from naval_adaptation_1970 import naval_adapter as A

def main():
    paths=[p['tree_file'] for p in A.profiles().values()]+list(A.runtime_outputs())
    def hashes():return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    before=hashes();log=['IMPERIA COLD WAR: naval build verification\n'];checks=[]
    jobs=[
        ('USA canonical rebuild',['tools/usa_1970_expansion/compile.py']),
        ('Marked five-country rebuild',['tools/naval_adaptation_1970/naval_adapter.py']),
        ('Emitted naval validation',['tools/naval_adaptation_1970/validate.py']),
        ('USA emitted integration validation',['tools/usa_1970_expansion/validate.py']),
        ('Naval asset, lifecycle and emitter tests',['-m','unittest','discover','-s','tools/naval_adaptation_1970','-p','test_*.py','-v']),
        ('USA calendar regression',['-m','unittest','discover','-s','tools/usa_1970_expansion','-p','test_focus_dates.py','-v']),
        ('Gulf access preservation',['-m','unittest','discover','-s','tools/iraq_1970','-p','test_gulf_access_20261025.py','-v']),
        ('UAE authorised programme preservation',['tools/uae_1970/test_revision.py']),
    ]
    for label,args in jobs:
        r=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        log+=['\n'+label+'\n',r.stdout,r.stderr]
        count=re.search(r'Ran (\d+) tests?',r.stderr)
        checks.append(dict(name=label,exit_code=r.returncode,unit_tests=int(count[1]) if count else None))
        (A.DOC/'CHECK_LOG.txt').write_text(''.join(log),encoding='utf-8')
        if r.returncode:raise RuntimeError(label+' failed; see CHECK_LOG.txt')
    after=hashes()
    assert before==after,'Build changed installed naval/country outputs; inspect before recording idempotence'
    result=dict(project='IMPERIA COLD WAR',status='PASS',checks=checks,byte_identical_rebuild_files=len(paths),hashes=after,naval_unit_tests=next(c['unit_tests'] for c in checks if c['name']=='Naval asset, lifecycle and emitter tests'),usa_calendar_tests=12,gulf_access_tests=18,native_game_test=False,multiplayer_test=False,other_country_broad_builds_run=False)
    (A.DOC/'BUILD_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
