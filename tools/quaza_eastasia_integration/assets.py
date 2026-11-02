# IMPERIA COLD WAR — Verified LFS assets for the reviewed quaZa feature import.
from pathlib import Path
import hashlib
import json
import re
import subprocess
from source import ROOT,DONOR,REPORT,read

INPUTS=('tools/nuclear_readiness/art/command_emblem_master.png',
        'docs/COLDWAR_NKO_1970_concept/v2/assets/COLDWAR_NKO_1994_funeral_colorized.png')


def main():
    imported=json.loads((REPORT/'INITIAL_IMPORT.json').read_text(encoding='utf-8'))
    rows={}
    for relative in tuple(imported['deferred_lfs_assets'])+INPUTS:
        raw=read(relative)
        pointer=re.fullmatch(rb'version https://git-lfs.github.com/spec/v1\noid sha256:([0-9a-f]{64})\nsize (\d+)\n',raw.replace(b'\r\n',b'\n'))
        if pointer:
            raw=subprocess.run(['git','lfs','smudge','--',relative],cwd=ROOT,input=raw,capture_output=True,check=True).stdout
            assert hashlib.sha256(raw).hexdigest()==pointer[1].decode(),relative
            assert len(raw)==int(pointer[2]),relative
        destination=ROOT/relative
        assert not destination.exists(),relative
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(raw)
        rows[relative]={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
    report={'project':'IMPERIA COLD WAR','source_commit':DONOR,'assets':rows,
            'source':'Unchanged quaZa source assets. See donor event-art credits and design provenance; unknown authors or permissions remain unknown.'}
    (REPORT/'ASSETS.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'project':'IMPERIA COLD WAR','assets':len(rows),'bytes':sum(v['bytes'] for v in rows.values())}))


if __name__=='__main__':main()
