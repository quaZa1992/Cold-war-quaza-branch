# IMPERIA COLD WAR — Semantic review of the complete MD update delta.
"""Read actual source, recover hash-verified ancestors and write review artifacts.

No loaded files are changed. Missing Git blobs are never fetched into the old
archive. Two historical text files may be read from the official public tag.
"""
from pathlib import Path
import collections
import csv
import difflib
import hashlib
import json
import re
import subprocess
import tempfile
import urllib.parse
import urllib.request

from audit import ROOT,OUT,UP,PROJECT,equal,emit

TOKEN=re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|>=|<=|!=|=|<|>|[^\s{}<>=!#"]+')
SCRIPT={'.txt','.gui','.gfx','.asset','.mod','.lua','.info'}


def text(data):return data.decode('utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def tokens(value):return [m[0] for m in TOKEN.finditer(value) if not m[0].startswith('#')]
def norm_sha(data):return hashlib.sha256(text(data).encode('utf-8')).hexdigest()
def loc(value):
    return {m[1]:m[2] for m in re.finditer(r'^\s+([^\s:#]+):(?:\d+)?\s*(".*")\s*$',value,re.M)}


def probe_merge(ours,base,theirs):
    folder=Path(tempfile.mkdtemp(prefix='_merge_probe_',dir=OUT)).resolve()
    assert folder.parent==OUT.resolve()
    paths=[folder/name for name in ('ours.probe','base.probe','theirs.probe')]
    try:
        for path,value in zip(paths,(ours,base,theirs)):path.write_text(value,encoding='utf-8',newline='\n')
        run=subprocess.run(['git','merge-file','-p','--diff3',*[str(p) for p in paths]],capture_output=True)
        merged=run.stdout.decode('utf-8')
        if run.returncode==0:
            return dict(status='already_present' if tokens(merged)==tokens(ours) else 'clean_additional_changes',
                        candidate_diff=''.join(difflib.unified_diff(ours.splitlines(True),merged.splitlines(True),fromfile='current',tofile='candidate',n=3)))
        if run.returncode<0 or run.returncode>127:raise RuntimeError(run.stderr.decode('utf-8'))
        return dict(status='textual_conflict_requires_review',conflict_count=run.returncode,
            conflict_blocks=re.findall(r'^<<<<<<< .*?^>>>>>>> .*?$',merged,re.M|re.S))
    finally:
        for path in paths:path.unlink(missing_ok=True)
        folder.rmdir()


def main():
    rows=json.loads((OUT/'upstream_changes.json').read_text(encoding='utf-8'))['files']
    batch=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    result=[];updiff=['# IMPERIA COLD WAR — Verified original MD to supplied MD update delta.\n']
    localdiff=['# IMPERIA COLD WAR — Remaining Cold War differences from supplied MD.\n']
    for row in rows:
        path=row['path'];b=row['baseline'];up=UP/path;cw=ROOT/path
        raw_u=up.read_bytes() if up.is_file() else None;raw_c=cw.read_bytes() if cw.is_file() else None
        raw_b=None;proof=None
        if b:
            batch.stdin.write(('c2ab8aca1:'+path+'\n').encode());batch.stdin.flush()
            header=batch.stdout.readline().decode().split()
            if header[-1]!='missing':
                candidate=batch.stdout.read(int(header[-1]));batch.stdout.read(1)
                if hashlib.sha256(candidate).hexdigest()==b['sha256'] or norm_sha(candidate)==b['normalized_utf8_sha256']:
                    raw_b=candidate;proof='git:c2ab8aca1:'+path
            if raw_b is None:
                if path=='descriptor.mod' and raw_u:
                    candidate=raw_u.replace(b'version="2.0.3"',b'version="2.0.2"',1)
                    if hashlib.sha256(candidate).hexdigest()==b['sha256']:
                        raw_b=candidate;proof='Exact archived raw SHA256 recovered by reversing only the supplied descriptor version literal.'
                if raw_b is None:
                    url='https://raw.githubusercontent.com/MillenniumDawn/Millennium-Dawn/v2.0.2/'+urllib.parse.quote(path)
                    with urllib.request.urlopen(url,timeout=30) as response:candidate=response.read()
                    if hashlib.sha256(candidate).hexdigest()==b['sha256'] or norm_sha(candidate)==b['normalized_utf8_sha256']:
                        raw_b=candidate;proof=url
                    else:proof='Official tag bytes do not match archived installed baseline; not used as ancestor.'
        r=dict(project=PROJECT,path=path,classification=row['classification'],runtime=row['runtime'],
            baseline_verified=raw_b is not None,baseline_source=proof,
            baseline_sha256=hashlib.sha256(raw_b).hexdigest() if raw_b is not None else None,
            new_md_sha256=row['new_md']['sha256'] if row['new_md'] else None,
            cold_war_sha256=row['cold_war']['sha256'] if row['cold_war'] else None)
        suffix=Path(path).suffix.casefold()
        if suffix not in SCRIPT|{'.yml','.md'}:
            r.update(semantic='non_runtime_binary_reference',proposal='Do not import Cold War preview images found inside the supplied MD folder.',choice='source_hygiene')
            result.append(r);continue
        u=text(raw_u) if raw_u is not None else '';c=text(raw_c) if raw_c is not None else ''
        if raw_b is not None:
            before=text(raw_b)
            hunks=list(difflib.unified_diff(before.splitlines(True),u.splitlines(True),fromfile='verified_old_MD/'+path,tofile='supplied_MD/'+path,n=3))
            updiff+=hunks;r['upstream_diff_lines']=len(hunks)
            r['upstream_added_lines']=sum(s.startswith('+') and not s.startswith('+++') for s in hunks)
            r['upstream_removed_lines']=sum(s.startswith('-') and not s.startswith('---') for s in hunks)
        if raw_u is None:
            empty=(not loc(c)) if suffix=='.yml' else not tokens(c)
            r.update(semantic='deleted_upstream_local_empty_stub' if empty else 'deleted_upstream_local_active_content',
                proposal='Remove the obsolete empty compatibility file only after checking remaining references.' if empty else 'Retain and inspect local functionality before removing anything.',choice='agency_cleanup')
        elif suffix=='.yml':
            new,local=loc(u),loc(c)
            missing={k:v for k,v in new.items() if k not in local};different={k:dict(md=v,cold_war=local[k]) for k,v in new.items() if k in local and v!=local[k]}
            r.update(semantic='same_localisation_keys_and_values' if not missing and not different else 'localisation_differences',
                md_keys_missing_locally=missing,changed_shared_keys=different,local_only_keys=sorted(local.keys()-new.keys()),
                proposal='Keep local text and preserve the supplied MD fixes; inspect only listed key differences.',choice='research_and_localisation' if 'research_' in path else 'version_and_text')
        else:
            same=tokens(u)==tokens(c)
            r.update(semantic='same_executable_tokens' if same else 'executable_or_text_differences',
                proposal='Already integrated apart from comments/formatting.' if same else 'Preserve Cold War-specific changes and review the full diff.',
                choice='metadata' if suffix=='.mod' or path=='Changelog.txt' else ('version_and_text' if path.startswith('descriptions/') else 'shared_code'))
        if r['semantic'] not in ('same_executable_tokens','same_localisation_keys_and_values'):
            hunks=list(difflib.unified_diff(u.splitlines(True),c.splitlines(True),fromfile='supplied_MD/'+path,tofile='Cold_War/'+path,n=3))
            localdiff+=hunks;r['local_diff_lines']=len(hunks)
        if raw_b is not None and raw_u is not None and raw_c is not None:
            r['merge_probe']=probe_merge(c,text(raw_b),u)
        result.append(r)
    batch.stdin.close();batch.wait()
    (OUT/'upstream_delta.diff').write_text(''.join(updiff),encoding='utf-8')
    (OUT/'local_preservation.diff').write_text(''.join(localdiff),encoding='utf-8')
    emit(OUT/'semantic_review.json',dict(project=PROJECT,runtime_writes=0,files=result,
        counts=dict(collections.Counter(r['semantic'] for r in result)),
        merge_probe_counts=dict(collections.Counter(r['merge_probe']['status'] for r in result if 'merge_probe' in r)),
        limitations=['Full token/localisation comparison preserves order and quoted text, but is not a native execution test.',
            'Unverified historical content is never silently substituted as a three-way ancestor.']))
    with (OUT/'decisions.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        fields=['project','path','classification','semantic','baseline_verified','choice','proposal']
        writer=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(result)
    print(json.dumps(dict(files=len(result),baseline_verified=sum(r['baseline_verified'] for r in result),
        counts=dict(collections.Counter(r['semantic'] for r in result)),merge_probe_counts=dict(collections.Counter(r['merge_probe']['status'] for r in result if 'merge_probe' in r)),
        unverified=[r['path'] for r in result if r['classification']!='new_md_file_review' and not r['baseline_verified']]),indent=2))


if __name__=='__main__':main()
