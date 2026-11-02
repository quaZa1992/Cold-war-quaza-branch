# IMPERIA COLD WAR — Complete read-only MD 2.0.3 migration inventory.
"""Compare the archived MD baseline, supplied Workshop source and live Cold War.

Only this task's compact audit reports are written. No runtime file is changed.
Hashes prove equality to the recorded source, not third-party ownership.
"""
from pathlib import Path
import collections
import concurrent.futures
import codecs
import datetime
import gzip
import hashlib
import json
import os
import stat
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/md_update_203_20261028'
UP=Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
ARCHIVE=Path('E:/MDColdWar_Backups/mdcoldwar_2026-10-13_old_mod_and_migration_archive/docs/md_2_0_migration_20261008')
BASE=ARCHIVE/'inventory_md.jsonl.gz'
PROJECT='IMPERIA COLD WAR'
PRIVATE={'.git','.agents','node_modules','__pycache__','.vendor'}
GAME={'common','events','gfx','history','interface','localisation','map','music','portraits','sound','scenario_tests','tutorial','descriptions'}


def emit(path,obj):
    temp=path.with_name(path.name+'.tmp')
    temp.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    temp.replace(path)


def scan(root):
    files={};exceptions=[];stack=[root]
    while stack:
        folder=stack.pop()
        try: entries=list(os.scandir(folder))
        except OSError as exc:
            exceptions.append(dict(path=folder.relative_to(root).as_posix(),kind='scan_error',error=str(exc)));continue
        for entry in entries:
            path=Path(entry.path);rel=path.relative_to(root).as_posix();key=rel.casefold()
            if entry.name in PRIVATE or (root==ROOT and rel in ('docs/md_update_203_20261028','tools/md_update_203')):
                exceptions.append(dict(path=rel,kind='private_or_audit_output_excluded'));continue
            try: meta=entry.stat(follow_symlinks=False)
            except OSError as exc:
                exceptions.append(dict(path=rel,kind='stat_error',error=str(exc)));continue
            if meta.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                exceptions.append(dict(path=rel,kind='reparse_point_not_followed',target=os.readlink(path)));continue
            if entry.is_dir(follow_symlinks=False):stack.append(path);continue
            if not stat.S_ISREG(meta.st_mode):
                exceptions.append(dict(path=rel,kind='non_regular_file'));continue
            if key in files:raise RuntimeError('Case-insensitive collision: '+rel)
            files[key]=dict(path=rel,bytes=meta.st_size,mtime_ns=meta.st_mtime_ns)
    return files,exceptions


def digest(job):
    root,row=job;path=root/row['path'];h=hashlib.sha256();norm=hashlib.sha256()
    decoder=codecs.getincrementaldecoder('utf-8-sig')('strict');pending='';valid=True;size=0
    try:
        before=path.stat(follow_symlinks=False)
        with path.open('rb') as stream:
            opened=os.fstat(stream.fileno())
            while chunk:=stream.read(1024*1024):
                size+=len(chunk);h.update(chunk)
                if valid:
                    try:
                        text=pending+decoder.decode(chunk);pending=''
                        if text.endswith('\r'):pending='\r';text=text[:-1]
                        norm.update(text.replace('\r\n','\n').replace('\r','\n').encode('utf-8'))
                    except UnicodeDecodeError:valid=False
            if valid:
                try:norm.update((pending+decoder.decode(b'',final=True)).replace('\r\n','\n').replace('\r','\n').encode('utf-8'))
                except UnicodeDecodeError:valid=False
            closed=os.fstat(stream.fileno())
        after=path.stat(follow_symlinks=False)
        observations=(before,opened,closed,after)
        stable=all((s.st_size,s.st_mtime_ns)==(row['bytes'],row['mtime_ns']) for s in observations) and size==row['bytes']
        if not stable:raise RuntimeError('File changed while read: '+row['path'])
        return dict(row,sha256=h.hexdigest(),normalized_utf8_sha256=norm.hexdigest() if valid else None,status='ok')
    except (OSError,RuntimeError) as exc:return dict(row,status='error',error=str(exc))


def equal(a,b):
    if a is None or b is None:return a is b
    return a.get('sha256')==b.get('sha256') or bool(a.get('normalized_utf8_sha256') and a['normalized_utf8_sha256']==b.get('normalized_utf8_sha256'))


def classify(b,u,c):
    if equal(b,u):return 'unchanged_all' if equal(b,c) else 'cold_war_only_keep'
    if equal(u,c):return 'already_matches_new_md'
    if b is None:
        return 'new_md_file_review' if c is None else 'both_added_different_review'
    if u is None:
        return 'md_deleted_review' if equal(b,c) else 'md_deleted_cold_war_modified_review'
    if c is None:return 'md_changed_cold_war_removed_review'
    if equal(b,c):return 'md_only_update_review'
    return 'both_changed_merge_review'


def area(path):
    parts=path.split('/')
    return '/'.join(parts[:2]) if parts[0] in ('common','gfx','history','localisation') and len(parts)>1 else parts[0]


def main():
    started=time.time();OUT.mkdir(parents=True,exist_ok=True)
    baseline={}
    with gzip.open(BASE,'rt',encoding='utf-8') as stream:
        for row in map(json.loads,stream):
            if row.get('kind')!='regular_file' or row.get('hash_status')!='ok':raise RuntimeError('Incomplete archived baseline')
            key=row['path'].casefold()
            if key in baseline:raise RuntimeError('Baseline case collision')
            baseline[key]={k:row[k] for k in ('path','sha256','normalized_utf8_sha256')}
            baseline[key]['bytes']=row['bytes_read']
    sources={};coverage={};all_errors=[]
    for name,root in [('new_md',UP),('cold_war',ROOT)]:
        files,exceptions=scan(root);results={}
        print(json.dumps(dict(phase='scan',source=name,files=len(files),gb=round(sum(r['bytes'] for r in files.values())/1e9,2))),flush=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            for count,row in enumerate(pool.map(digest,((root,row) for row in files.values()),chunksize=32),1):
                results[row['path'].casefold()]=row
                if row['status']!='ok':all_errors.append(dict(source=name,**row))
                if count%10000==0:print(json.dumps(dict(phase='hash',source=name,done=count,total=len(files))),flush=True)
        final,final_exceptions=scan(root)
        drift=[files[k]['path'] for k in files.keys()&final.keys() if files[k]!=final[k]]
        drift+=sorted(files.keys()^final.keys())
        if drift:all_errors.append(dict(source=name,kind='final_scan_drift',paths=drift))
        coverage[name]=dict(root=str(root),regular_files=len(results),bytes=sum(r['bytes'] for r in results.values()),
            hashed_ok=sum(r['status']=='ok' for r in results.values()),exceptions=exceptions,final_scan_drift=drift,
            case_collisions=0)
        sources[name]=results
    if all_errors:
        emit(OUT/'errors.json',dict(project=PROJECT,errors=all_errors));raise RuntimeError('Inventory errors; see errors.json')
    counts=collections.Counter();areas=collections.defaultdict(collections.Counter);changed=[];rows=[]
    union=sorted(baseline.keys()|sources['new_md'].keys()|sources['cold_war'].keys())
    for key in union:
        b,u,c=baseline.get(key),sources['new_md'].get(key),sources['cold_war'].get(key)
        if b is None and u is None:kind='cold_war_addition_keep'
        else:kind=classify(b,u,c)
        path=(u or c or b)['path'];group=area(path);counts[kind]+=1;areas[group][kind]+=1
        row=dict(project=PROJECT,path=path,area=group,runtime=path.split('/')[0] in GAME,classification=kind,
            baseline=b,new_md=u,cold_war=c,upstream_changed=not equal(b,u))
        rows.append(row)
        if row['upstream_changed']:changed.append(row)
    with gzip.open(OUT/'all_files.jsonl.gz','wt',encoding='utf-8',compresslevel=6) as stream:
        for row in rows:stream.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
    emit(OUT/'upstream_changes.json',dict(project=PROJECT,files=changed))
    summary=dict(project=PROJECT,mode='Read-only inventory; no runtime files copied or merged',
        date='2026-10-28',head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        baseline=dict(source=str(BASE),sha256=hashlib.sha256(BASE.read_bytes()).hexdigest(),files=len(baseline),
            recorded_date='2026-10-08',description='Archived actual MD source inventory used for the earlier migration, not an assumed Git ancestor'),
        sources=coverage,union_files=len(union),classification_counts=dict(counts),
        upstream_changed_files=len(changed),upstream_changed_runtime_files=sum(r['runtime'] for r in changed),
        areas={a:dict(v) for a,v in sorted(areas.items())},elapsed_seconds=round(time.time()-started,2),
        runtime_writes=0,limitations=['Hash classification is not a semantic review or a native HOI4/MP test.',
            'Original bytes for overlapping changes must be recovered and hash-verified before three-way merges.',
            'Private caches, Git metadata, task audit outputs and every reparse point are explicitly excluded.'])
    emit(OUT/'inventory_summary.json',summary)
    print(json.dumps({k:summary[k] for k in ('union_files','classification_counts','upstream_changed_files','upstream_changed_runtime_files','elapsed_seconds')},indent=2),flush=True)


if __name__=='__main__':main()
