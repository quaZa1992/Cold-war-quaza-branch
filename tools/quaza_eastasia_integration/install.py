# IMPERIA COLD WAR — Selective source and owned-file import from pinned quaZa content.
"""Shared files are integrated separately; unrelated donor changes never apply."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
from source import ROOT,HERE,DONOR,SNAPSHOT,REPORT,PREFIX

MARK='# IMPERIA COLD WAR — quaZa East Asia and strategic-readiness integration.'
ARCHIVE_PARTS={'baseline','shared_baseline','runtime','profile','logs','before'}


def normalise(relative,raw):
    suffix=Path(relative).suffix
    if suffix not in {'.py','.txt','.gui','.gfx','.yml','.md'}:return raw
    text=raw.decode('utf-8-sig').replace('\r\n','\n')
    text=text.replace('# IMPERIA CW', '# IMPERIA COLD WAR')
    if suffix=='.yml':
        lines=text.splitlines()
        lines=[line for line in lines if line.strip()!='l_english:' and line!=MARK]
        if not lines or not lines[0].startswith('# IMPERIA COLD WAR — '):lines.insert(0,MARK)
        text='l_english:\n'+'\n'.join(lines)+'\n'
        # Punctuation is prose here; preserve the exact project-comment marker.
        text='\n'.join(line if line.lstrip().startswith('#') else line.replace('\u2014',': ').replace('\u2013','-') for line in text.splitlines())+'\n'
        return text.encode('utf-8-sig')
    if suffix=='.md':
        if not text.startswith('IMPERIA COLD WAR'):text='IMPERIA COLD WAR\n\n'+text
    elif not text.startswith('# IMPERIA COLD WAR \u2014 '):text=MARK+'\n'+text
    return text.encode('utf-8')


def initial_import():
    inventory=json.loads((REPORT/'SOURCE_INVENTORY.json').read_text(encoding='utf-8'))
    outputs={};deferred=[]
    for relative,meta in inventory['files'].items():
        parts=Path(relative).parts
        live=relative.startswith(('common/','events/','interface/','localisation/english/','gfx/')) and (PREFIX.search(relative) or 'COLDWAR_nuclear_escalation' in relative)
        source=relative.startswith(('tools/north_korea_1970/','tools/COLDWAR_KOR_1970_concept/','tools/japan_1970/','tools/nuclear_readiness/'))
        source=source and not ARCHIVE_PARTS.intersection(parts) and not Path(relative).name.startswith('before_')
        design=relative.startswith(('docs/COLDWAR_NKO_1970_concept/','docs/design/COLDWAR_KOR_1970/','docs/nuclear_readiness/'))
        if not (live or source or design):continue
        destination=ROOT/relative
        raw=(SNAPSHOT/relative).read_bytes()
        if raw.startswith(b'version https://git-lfs.github.com/spec/v1'):
            deferred.append(relative);continue
        if destination.exists():raise RuntimeError('Pre-existing import destination: '+relative)
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(normalise(relative,raw))
        outputs[relative]=hashlib.sha256(destination.read_bytes()).hexdigest()
    record={'project':'IMPERIA COLD WAR','source_commit':DONOR,'files':outputs,'deferred_lfs_assets':deferred,
            'scope':'New feature-owned content and canonical input only. No shared root file overwritten. Donor archival baselines remain on E:.'}
    (REPORT/'INITIAL_IMPORT.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'project':'IMPERIA COLD WAR','imported_files':len(outputs),'deferred_lfs_assets':len(deferred)}))


if __name__=='__main__':initial_import()
