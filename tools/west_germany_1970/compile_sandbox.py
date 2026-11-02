# IMPERIA COLD WAR — Bounded installation of the German two-player sandbox
"""Apply changed canonical nodes only; reject unrelated live-node divergence."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import os
import compile as generator
from compile_security import parse,first,spans

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
BASE=HERE/'audit_snapshots/sandbox_rails_20261023/before'
MARK='# IMPERIA COLD WAR — German two-player sandbox\n'
# These live strings still contained the retired guarantee score. The second
# key also changes meaning because safe deferral now precedes political choices.
RETIRED_SCORE_TEXT={'COLDWAR_GER_1970_tt_crackdown','COLDWAR_GGR.211.b.tt'}
LIVE_BEFORE=json.loads((HERE/'sandbox_audit/before_live.json').read_text(encoding='utf-8'))['files']
REPORT=HERE/'sandbox_integration.json'
PREVIOUS=json.loads(REPORT.read_text(encoding='utf-8')) if REPORT.exists() else {}
INSTALLED=PREVIOUS.get('installed_sha256',PREVIOUS.get('sha256',{}) if not PREVIOUS.get('dry_run',True) else {})


def entries(text,rel):
    rows=parse(text)
    if '/national_focus/' in rel:
        rows=[r for r in first(rows,'focus_tree') if r[0]=='focus'];field='id';wrapper='focus_tree'
    elif '/ideas/' in rel:
        rows=first(first(rows,'ideas'),'country');field=None;wrapper='country'
    elif rel.startswith('interface/'):
        wrapper='guiTypes' if rel.endswith('.gui') else 'spriteTypes';rows=first(rows,wrapper);field='name'
    elif '/scripted_guis/' in rel:
        wrapper='scripted_gui';rows=first(rows,wrapper);field=None
    elif '/decisions/' in rel and '/categories/' not in rel:
        return {(cat,key):dict(key=key,identity=None,node=value,wrapper=cat)
                for cat,op,nodes in rows if isinstance(nodes,list)
                for key,op,value in nodes if isinstance(value,list)}
    else:field=None;wrapper=None
    out={}
    for key,op,node in rows:
        if not isinstance(node,list):continue
        ident=field or ('id' if key in ('country_event','news_event') else 'name' if key=='defined_text' else None)
        value=str(first(node,ident)).strip('"') if ident else key
        out[(key,value)]=dict(key=key,identity=(ident,value) if ident else None,node=node,wrapper=wrapper)
    return out


def native_span(text,item):
    candidates=spans(text,item['key'],item['identity'])
    # An event declaration and an inline country_event call can share the ID.
    # Match the complete parsed node, so a nested dispatch can never be spliced.
    candidates=[r for r in candidates if first(parse(r[2]),item['key'])==item['node']]
    if item['wrapper'] and item['identity'] is None:
        a,b,_=spans(text,item['wrapper'])[0]
        candidates=[r for r in candidates if a<r[0]<r[1]<b]
    if len(candidates)!=1:raise ValueError('Ambiguous native block '+str(item))
    return candidates[0]


def update_script(old,before,new,rel,installed=False):
    a,b=entries(before,rel),entries(new,rel)
    current=entries(old,rel);result=old;changed=[]
    moved={identity for identity in current if rel.endswith('_windows_effects.txt') and identity[0].startswith('COLDWAR_GER_1970_rv_can_ratify_')} if installed else set()
    for identity in sorted(set(a)|set(b)|moved):
        pre=a.get(identity);post=b.get(identity);live=current.get(identity)
        if (pre or {}).get('node')==(post or {}).get('node') and identity not in moved:continue
        if (live or {}).get('node')==(post or {}).get('node'):continue
        if (live or {}).get('node')!=(pre or {}).get('node') and not installed:
            raise ValueError(f'{rel}: preserve divergent live node {identity}')
        if live:
            start,end,_=native_span(result,live)
            body=native_span(new,post)[2] if post else ''
            if body and not result[:start].endswith(MARK):body=MARK+body
            result=result[:start]+body+result[end:]
        else:
            body=MARK+native_span(new,post)[2]+'\n'
            if post['wrapper']:
                end=spans(result,post['wrapper'])[0][1]-1
                result=result[:end]+'\n'+body+result[end:]
            else:result+='\n'+body
        changed.append(identity)
    # Event namespaces are declarations, not brace blocks.
    for ns in re.findall(r'(?m)^add_namespace\s*=\s*(\w+)',new):
        if not re.search(r'(?m)^add_namespace\s*=\s*'+re.escape(ns)+r'\s*$',result):result=MARK+'add_namespace = '+ns+'\n'+result
    parse(result)
    return result,changed


def update_loc(old,before,new,rel,installed=False):
    pattern=r'(?m)^ ([^:\s]+):\d*\s+(".*")$'
    a,b,live=(dict(re.findall(pattern,t)) for t in (before,new,old))
    result=old;changed=[]
    for key in sorted(set(a)|set(b)):
        if a.get(key)==b.get(key) or live.get(key)==b.get(key):continue
        if live.get(key)!=a.get(key) and not installed:
            recorded=dict(re.findall(pattern,LIVE_BEFORE.get(rel,'')))
            if key not in RETIRED_SCORE_TEXT or live.get(key)!=recorded.get(key):
                raise ValueError('Preserve divergent live localisation '+key)
        line=r'(?m)^ '+re.escape(key)+r':\d*\s+".*"\n?'
        if key in b:
            replacement=f' {key}:0 {b[key]}\n'
            if key in live:result=re.sub(line,lambda _:replacement,result)
            else:result+=replacement
        else:result=re.sub(line,'',result)
        changed.append(key)
    return result,changed


def build_plan():
    captured={}
    generator.write=lambda root,rel,text,bom=False:captured.setdefault(rel,(text,bom)) and rel
    generator.build(str(ROOT),scripts_only=True)
    writes={};changes={}
    for rel,(new,bom) in captured.items():
        target=ROOT/rel;baseline=BASE/rel
        if not baseline.exists():
            if target.exists() and target.read_text(encoding='utf-8-sig')!=new:
                if INSTALLED.get(rel)!=hashlib.sha256(target.read_bytes()).hexdigest():
                    raise ValueError('New output collides with live file '+rel)
            if target.exists() and target.read_text(encoding='utf-8-sig')==new:continue
            writes[rel]=(new,bom);changes[rel]=['new dedicated file'];continue
        before=baseline.read_text(encoding='utf-8-sig')
        old=target.read_text(encoding='utf-8-sig')
        # Follow-up fixes may update our own installed nodes only when the
        # complete live file still has the exact recorded installation hash.
        installed=INSTALLED.get(rel)==hashlib.sha256(target.read_bytes()).hexdigest()
        result,changed=update_loc(old,before,new,rel,installed) if bom else update_script(old,before,new,rel,installed)
        if result!=old:writes[rel]=(result,bom)
        if changed:changes[rel]=changed
    return writes,changes


def main():
    cli=argparse.ArgumentParser();cli.add_argument('--dry-run',action='store_true');args=cli.parse_args()
    writes,changes=build_plan()
    if not args.dry_run:
        for rel,(text,bom) in writes.items():
            target=ROOT/rel;target.parent.mkdir(parents=True,exist_ok=True)
            blob=text.encode('utf-8-sig' if bom else 'utf-8')
            if not target.exists() or target.read_bytes()!=blob:
                # Write complete content before replacing the installed file.
                temporary=target.with_name(target.name+'.coldwar.tmp')
                temporary.write_bytes(blob)
                os.replace(temporary,target)
            INSTALLED[rel]=hashlib.sha256(blob).hexdigest()
    report=dict(project='IMPERIA COLD WAR',dry_run=args.dry_run,files=len(writes),
                changed_nodes=changes,engine_tested=False,installed_sha256=INSTALLED,
                sha256={r:hashlib.sha256(t.encode('utf-8-sig' if b else 'utf-8')).hexdigest() for r,(t,b) in writes.items()})
    (HERE/'sandbox_integration.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(files=len(writes),nodes=sum(map(len,changes.values())),dry_run=args.dry_run)))


if __name__=='__main__':main()
