# IMPERIA COLD WAR — Pinned quaZa East Asia and nuclear-readiness source inventory.
"""Keep donor snapshots on E:. Never replace a complete upstream checkout."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
DONOR='7bef99f058f5796788feb839c617407171141c1d'
URL='https://github.com/quaZa1992/Cold-war-quaza-branch'
SNAPSHOT=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/quaza_eastasia_20261027/donor')
REPORT=ROOT/'docs/quaza_eastasia_integration_20261027'
PREFIX=re.compile(r'COLDWAR_(?:NKO|KOR|JAP|JAP70|nuclear_readiness)')
SOURCE_ROOTS=('tools/north_korea_1970/','tools/COLDWAR_KOR_1970_concept/','tools/japan_1970/','tools/nuclear_readiness/',
              'docs/COLDWAR_NKO_1970_concept/','docs/design/COLDWAR_KOR_1970/','docs/nuclear_readiness/')
TEXT_SUFFIXES={'.py','.md','.json','.jsonl','.csv','.txt','.yml','.html','.js','.cjs','.gfx','.gui'}


def git(*args):
    return subprocess.run(['git',*args],cwd=ROOT,capture_output=True,check=True).stdout


def read(relative):
    return git('show',DONOR+':'+relative)


def inventory():
    files={}
    for record in git('ls-tree','-r','-l','-z',DONOR).split(b'\0'):
        if not record:continue
        metadata,path=record.split(b'\t',1)
        mode,kind,oid,size=metadata.decode().split()
        files[path.decode('utf-8')]={'git_oid':oid,'bytes':int(size),'mode':mode}
    refs=git('grep','-I','-l','-E',r'COLDWAR_(NKO|KOR|JAP|JAP70|nr_)',DONOR,'--','common','events','interface','history','localisation/english').decode('utf-8').splitlines()
    referenced={line.split(':',1)[1] for line in refs}
    selected={p for p in files if (p.startswith(('common/','events/','interface/','localisation/english/','gfx/')) and PREFIX.search(p))
              or (p.startswith(SOURCE_ROOTS) and Path(p).suffix in TEXT_SUFFIXES and '/runtime/' not in p and '/profile/' not in p and '/logs/' not in p)}|referenced
    # Design source used by Japan lives outside the tools directory.
    selected.update(p for p in files if p.startswith(('docs/design/japan','docs/japan_1970','docs/COLDWAR_JAP')) and Path(p).suffix in TEXT_SUFFIXES)
    selected.update('history/countries/'+name for name in ('NKO - North Korea.txt','KOR - Korea.txt','JAP - Japan.txt'))
    result={'project':'IMPERIA COLD WAR','source_repository':URL,'source_commit':DONOR,
            'baseline_commit':git('rev-parse','HEAD').decode().strip(),'snapshot':str(SNAPSHOT),
            'files':{p:files[p] for p in sorted(selected)}}
    REPORT.mkdir(parents=True,exist_ok=True)
    (REPORT/'SOURCE_INVENTORY.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result


def export(data):
    for relative,metadata in data['files'].items():
        parts=PurePosixPath(relative).parts
        assert not relative.startswith('/') and '..' not in parts and metadata['mode']=='100644',relative
        raw=read(relative)
        destination=SNAPSHOT.joinpath(*parts)
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(raw)
        metadata['sha256']=hashlib.sha256(raw).hexdigest()
    (REPORT/'SOURCE_INVENTORY.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    data=inventory()
    if '--export' in sys.argv:export(data)
    print(json.dumps({'project':'IMPERIA COLD WAR','source_commit':DONOR,'files':len(data['files']),
                      'bytes':sum(v['bytes'] for v in data['files'].values()),'snapshot_exported':'--export' in sys.argv}))
