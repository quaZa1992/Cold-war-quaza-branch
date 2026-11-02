# IMPERIA COLD WAR — Apply the approved MD 2.0.3 metadata and empty-file cleanup.
"""Fresh complete source recheck, guarded narrow edits and full preservation proof.

The user approved the recommended proposal after individual file inspection.
The original audit inventories are retained unchanged. Archives remain on E:.
"""
from pathlib import Path
import concurrent.futures
import datetime
import gzip
import hashlib
import json
import re
import subprocess
import sys
import time
import zipfile

from audit import ROOT,OUT,UP,PROJECT,scan,emit

MARK='# IMPERIA COLD WAR — MD 2.0.3 base metadata and version display.\n'
ARCHIVES=Path('E:/MDColdWar_Backups/Codex_Test_Archives')


def sha(value):return hashlib.sha256(value).hexdigest()


def hash_file(job):
    root,row=job;p=root/row['path'];before=p.stat(follow_symlinks=False);h=hashlib.sha256()
    with p.open('rb') as stream:
        while chunk:=stream.read(1024*1024):h.update(chunk)
    after=p.stat(follow_symlinks=False)
    assert (before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns)==(row['bytes'],row['mtime_ns']),str(p)+' changed while read'
    return row['path'].casefold(),h.hexdigest()


def hash_tree(root,label):
    files,exceptions=scan(root)
    assert not [e for e in exceptions if e['kind'].endswith('error')],exceptions
    print(json.dumps(dict(phase='scan',source=label,files=len(files))),flush=True)
    hashes={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for index,(key,digest) in enumerate(pool.map(hash_file,((root,row) for row in files.values())),1):
            hashes[key]=digest
            if index%20000==0:print(json.dumps(dict(phase='hash',source=label,done=index,total=len(files))),flush=True)
    final,_=scan(root);assert final==files,label+' changed during hashing'
    return files,hashes,exceptions


def read_inventory():
    with gzip.open(OUT/'all_files.jsonl.gz','rt',encoding='utf-8') as stream:return list(map(json.loads,stream))


def header(raw,localisation=False):
    value=raw.decode('utf-8-sig')
    if localisation:
        match=re.match(r'(l_[a-z_]+:[^\r\n]*\r?\n)',value)
        assert match,'Missing localisation header'
        value=value[:match.end()]+MARK+value[match.end():]
        return b'\xef\xbb\xbf'+value.encode('utf-8')
    return (MARK+value).encode('utf-8')


def main():
    start=time.time();report_path=OUT/'implementation.json'
    assert not report_path.exists(),'An implementation record already exists; verify it rather than applying twice.'
    records=read_inventory();expected_md={r['new_md']['path'].casefold():r['new_md']['sha256'] for r in records if r['new_md']}
    expected_cw={r['cold_war']['path'].casefold():r['cold_war']['sha256'] for r in records if r['cold_war']}
    records_cw={r['cold_war']['path'].casefold():r['cold_war'] for r in records if r['cold_war']}
    paths_cw={key:row['path'] for key,row in records_cw.items()}
    if '--resume-verified-source' in sys.argv:
        prior=json.loads((OUT/'source_recheck.json').read_text(encoding='utf-8'))
        assert prior['status']=='PASS' and prior['original_inventory_sha256']==sha((OUT/'all_files.jsonl.gz').read_bytes())
        source_files,source_exclusions=scan(UP)
        old_meta={r['new_md']['path'].casefold():{k:r['new_md'][k] for k in ('path','bytes','mtime_ns')} for r in records if r['new_md']}
        assert source_files==old_meta,'Source metadata changed after fresh complete hash verification'
        source_hashes=expected_md.copy()
    else:
        source_files,source_hashes,source_exclusions=hash_tree(UP,'fresh_MD_source')
    drift=[dict(path=source_files[k]['path'],before=expected_md.get(k),current=source_hashes.get(k)) for k in source_hashes.keys()|expected_md.keys() if source_hashes.get(k)!=expected_md.get(k)]
    emit(OUT/'source_recheck.json',dict(project=PROJECT,status='FAIL' if drift else 'PASS',files=len(source_hashes),
        source=str(UP),changed_since_review=drift,original_inventory_sha256=sha((OUT/'all_files.jsonl.gz').read_bytes()),
        original_upstream_delta_paths=73,original_baseline_files=79721,exclusions=source_exclusions))
    assert not drift,'Workshop source changed after approval. No runtime edits applied.'
    plan=json.loads((OUT/'adoption_plan.json').read_text(encoding='utf-8'))
    changes={};deletions=[]
    for row in plan['files']:
        action=row['action'];relative=row['path'];path=ROOT/relative
        if not action.startswith('ASK_'):continue
        raw=path.read_bytes();assert sha(raw)==row['cold_war_sha256'],'Reviewed target changed: '+relative
        if action=='ASK_REMOVE_EMPTY_LEGACY_FILE':
            content=raw.decode('utf-8-sig');body='\n'.join(line for line in content.splitlines() if not line.lstrip().startswith('#')).strip()
            assert body in ('','l_english:'),'Nonempty legacy file: '+relative
            deletions.append(relative);continue
        if relative.startswith('descriptions/'):
            new,count=re.subn(rb'(?m)(^\[b\][^\r\n]*\[/b\]\s*v?)2\.0\.[012](?=\r?$)',lambda m:m[1]+b'2.0.3',raw)
            new,checks=re.subn(rb'(?m)^\[b\][^\r\n]*\[/b\]\s*(?:8751|ccc6)\s*\r?\n',b'',new)
            assert count==checks==1,'Unexpected description version/checksum metadata: '+relative
        elif action=='ASK_UPDATE_UPSTREAM_NOTE':
            source=(UP/relative).read_bytes();new=('IMPERIA COLD WAR: MD 2.0.3 upstream update note\n\n'
                'Source: the user-supplied Millennium Dawn 2.0.3 Workshop folder.\n'
                'The original note below retains its upstream v2.0.2 heading.\n\n').encode()+source
        else:
            assert b'2.0.2' in raw,relative
            new=raw.replace(b'2.0.2',b'2.0.3')
            if path.suffix=='.mod':new=header(new)
            elif path.suffix=='.yml':new=header(new,True)
        changes[relative]=new
    internal='mdcoldwar.mod';raw=(ROOT/internal).read_bytes()
    assert sha(raw)==expected_cw[internal]
    assert 'path="mod/mdcoldwar"' in raw.decode('utf-8-sig')
    changes[internal]=header(raw.replace(b'version="2.0.2"',b'version="2.0.3"',1))
    readme=(ROOT/'README.md').read_bytes();assert sha(readme)==expected_cw['readme.md']
    changes['README.md']=readme.replace(b'# MD Cold War',b'# IMPERIA COLD WAR: MD Cold War',1).replace(b'Millennium Dawn 2.0.2 base',b'Millennium Dawn 2.0.3 base',1)
    notice=(ROOT/'IMPERIA_COLD_WAR_NOTICE.md').read_bytes();assert sha(notice)==expected_cw['imperia_cold_war_notice.md']
    lines=notice.decode('utf-8-sig').splitlines(True)
    entry=('\n<!-- IMPERIA COLD WAR — Verified MD 2.0.3 base update. -->\n'
        '- MD 2.0.3 adoption: `docs/md_update_203_20261028/IMPLEMENTED.md` records the approved source choices, full-file hash comparison, preserved Cold War features, metadata-only updates, empty legacy-file cleanup and verification limits. Existing MD and Cold War authorship and licences are retained; no artwork is replaced.\n')
    changes['IMPERIA_COLD_WAR_NOTICE.md']=(lines[0]+entry+''.join(lines[1:])).encode('utf-8')
    external=ROOT.parent/'mdcoldwar.mod';external_raw=external.read_bytes();external_text=external_raw.decode('utf-8-sig')
    match=re.search(r'(?m)^path\s*=\s*"([^"]+)"',external_text)
    assert match and Path(match[1]).resolve()==ROOT.resolve(),'Launcher points to a different mod'
    external_new=header(external_raw.replace(b'version="2.0.2"',b'version="2.0.3"',1))
    assert len(deletions)==12 and len(changes)==26,(len(deletions),len(changes))
    before_scan,_=scan(ROOT)
    # Protect concurrent edits instead of adopting an unrelated fresh baseline.
    changed_meta=[key for key,row in before_scan.items() if key in paths_cw and (row['bytes'],row['mtime_ns'])!=(records_cw[key]['bytes'],records_cw[key]['mtime_ns'])]
    for key in changed_meta:
        assert sha((ROOT/before_scan[key]['path']).read_bytes())==expected_cw[key],'Unrelated source drift: '+key
    assert set(before_scan)==set(expected_cw),'Cold War file paths changed since review'
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    backup=ARCHIVES/('MD_203_before_update_'+stamp+'.zip');backup.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(backup,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for rel in sorted(set(changes)|set(deletions)):archive.write(ROOT/rel,'mod/'+rel)
        archive.writestr('launcher/mdcoldwar.mod',external_raw)
        archive.writestr('IMPERIA_COLD_WAR_ARCHIVE.json',json.dumps(dict(project=PROJECT,scope='Approved metadata updates and twelve verified empty legacy files',external_launcher=str(external))))
    expected_after=expected_cw.copy();transactions=[]
    for relative,new in changes.items():
        path=ROOT/relative;old=path.read_bytes();key=relative.casefold()
        assert sha(old)==expected_cw[key],relative
        temp=path.with_name(path.name+'.md203tmp');temp.write_bytes(new);temp.replace(path)
        expected_after[key]=sha(new);transactions.append(dict(path=relative,operation='update',before=sha(old),after=sha(new)))
    for relative in deletions:
        path=ROOT/relative;key=relative.casefold();assert sha(path.read_bytes())==expected_cw[key]
        path.unlink();expected_after.pop(key);transactions.append(dict(path=relative,operation='remove_empty',before=expected_cw[key],after=None))
    assert external.read_bytes()==external_raw
    temp=external.with_name(external.name+'.md203tmp');temp.write_bytes(external_new);temp.replace(external)
    report=dict(project=PROJECT,status='APPLIED_PENDING_PRESERVATION_CHECK',date='2026-10-28',
        approval='User approved all recommended source choices after individual review.',backup=str(backup),backup_sha256=sha(backup.read_bytes()),
        source_recheck_files=len(source_hashes),upstream_changed_paths=73,transactions=transactions,
        external_launcher=dict(path=str(external),before=sha(external_raw),after=sha(external_new)),
        runtime_gameplay_files_replaced=0,artwork_replaced=0,native_test=False)
    emit(report_path,report)
    print(json.dumps(dict(phase='applied',updated_files=len(changes),removed_empty_files=len(deletions),external_launchers=1,backup=str(backup))),flush=True)
    current,after_hashes,exceptions=hash_tree(ROOT,'Cold_War_preservation')
    unexpected=[dict(path=current[k]['path'] if k in current else paths_cw[k],expected=expected_after.get(k),actual=after_hashes.get(k))
        for k in expected_after.keys()|after_hashes.keys() if expected_after.get(k)!=after_hashes.get(k)]
    final_md,_=scan(UP);assert final_md==source_files,'MD updated during migration'
    report.update(status='PASS' if not unexpected else 'FAIL',files_verified=len(after_hashes),
        files_preserved_byte_for_byte=len(expected_cw)-len(changes)-len(deletions),unexpected_changes=unexpected,
        source_unchanged_during_migration=True,elapsed_seconds=round(time.time()-start,2),exclusions=exceptions)
    emit(report_path,report);assert not unexpected,unexpected
    print(json.dumps({k:report[k] for k in ('status','files_verified','files_preserved_byte_for_byte','upstream_changed_paths','elapsed_seconds')},indent=2),flush=True)


if __name__=='__main__':main()
