# IMPERIA CW — Cold War: tools — focus prerequisite ui.
"""Hide duplicate national-focus prerequisite tooltips without changing gates.

Only equivalent checks for an existing prerequisite group are hidden. Extra
branch choices, negative checks, foreign scopes and funding remain visible.
Source spans preserve all unrelated bytes, comments, rewards and layout.
Country compilers may call hide_redundant_prerequisites on focus availability;
decision/reward execution guards should keep their existing presentation.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import re

ROOT=Path(__file__).resolve().parents[1]
TOKEN=re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|>=|<=|!=|[{}=<>]|[^\s{}=<>!#"]+')

@dataclass
class Node:
    key:str
    op:str
    value:object
    start:int
    end:int
    def children(self):return self.value if isinstance(self.value,list) else []

def nodes(text):
    tokens=[m for m in TOKEN.finditer(text) if not m[0].startswith('#')];i=0
    def read(nested=False):
        nonlocal i
        rows=[]
        while i<len(tokens):
            key=tokens[i];i+=1
            if key[0]=='}':
                if not nested:raise ValueError('Unexpected closing brace')
                return rows,key.end()
            if i<len(tokens) and tokens[i][0] in ('=','<','>','>=','<=','!='):
                op=tokens[i][0];i+=1
                value=tokens[i];i+=1
                if value[0]=='{':body,end=read(True)
                else:body,end=value[0],value.end()
                rows.append(Node(key[0],op,body,key.start(),end))
            else:rows.append(Node('_bare','=',key[0],key.start(),key.end()))
        if nested:raise ValueError('Unclosed block')
        return rows,len(text)
    return read()[0]

def field(rows,key,default=None):return next((n.value for n in rows if n.key==key),default)

def _and(parts):
    result={frozenset()}
    for part in parts:
        if part is None:return None
        result={a|b for a in result for b in part}
        if len(result)>4096:return None
    return frozenset(result)

def _forms(groups):
    group_forms=[frozenset(frozenset([p]) for p in group) for group in groups if group]
    result=set(group_forms)
    if group_forms:
        full=_and(group_forms)
        if full is not None:result.add(full)
    return result

def _milestones(node,parents):
    """Project only known predecessor receipts into focus-ID boolean form."""
    if node.op!='=':return None
    k,v=node.key,node.value
    parent=None
    if k=='has_completed_focus' and isinstance(v,str) and v in parents:parent=v
    elif k=='has_country_flag' and isinstance(v,str):
        parent=next((p for p in parents if v in (p+'_implemented',p+'_delivered',p+'_granted',p+'_reward_applied')),None)
        # Cyprus receipts are prefix-keyed, unlike the other country providers.
        if parent is None:
            prefix='COLDWAR_CYP_1970_'
            parent=next((p for p in parents if p.startswith(prefix) and v==prefix+'applied_'+p[len(prefix):]),None)
    elif k=='NOT' and isinstance(v,list) and len(v)==1:
        child=v[0];prefix='COLDWAR_CYP_1970_'
        if child.key=='has_country_flag' and child.op=='=' and isinstance(child.value,str):
            parent=next((p for p in parents if p.startswith(prefix) and child.value==prefix+'pending_completion_'+p[len(prefix):]),None)
    if parent:return frozenset([frozenset([parent])])
    if not isinstance(v,list):return None
    if k in ('AND','custom_trigger_tooltip'):
        children=[n for n in v if not (k=='custom_trigger_tooltip' and n.key=='tooltip')]
        return _and(_milestones(n,parents) for n in children) if children else None
    if k=='OR':
        children=[_milestones(n,parents) for n in v]
        if not children or any(c is None for c in children):return None
        return frozenset().union(*children)
    return None

def _edits(text,rows,groups):
    parents=set(itertools.chain.from_iterable(groups));forms=_forms(groups);edits=[]
    def visit(node):
        if node.key=='hidden_trigger':return
        form=_milestones(node,parents)
        if form is not None and form in forms:
            original=text[node.start:node.end]
            if '\n' not in original:replacement='hidden_trigger = { '+original+' }'
            else:
                margin=re.match(r'[\t ]*',text[text.rfind('\n',0,node.start)+1:node.start])[0]
                replacement='hidden_trigger = {\n'+margin+'\t'+original.replace('\n','\n\t')+'\n'+margin+'}'
            edits.append((node.start,node.end,replacement));return
        # Never reinterpret another country's scope, conditional branch or NOT.
        if node.key in ('AND','OR','custom_trigger_tooltip'):
            for child in node.children():visit(child)
    for row in rows:visit(row)
    return edits

def _apply(text,edits):
    for start,end,replacement in sorted(edits,reverse=True):text=text[:start]+replacement+text[end:]
    return text

def hide_redundant_prerequisites(availability,groups):
    return _apply(availability,_edits(availability,nodes(availability),groups))

def _canon_condition(node):
    k,v=node.key,node.value
    if not isinstance(v,list):return k,node.op,v
    if k in ('AND','hidden_trigger'):
        result=[]
        for child in v:
            item=_canon_condition(child)
            result.extend(item[1] if item[0]=='AND' else [item])
        if len(result)==1:return result[0]
        return 'AND',tuple(result)
    return k,node.op,tuple(_canon_condition(n) for n in v)

def _canonical(rows):
    result=[]
    for n in rows:
        if n.key=='available':
            result.append(('available',_canon_condition(Node('AND','=',n.children(),0,0))))
        else:result.append((n.key,n.op,_canonical(n.value) if isinstance(n.value,list) else n.value))
    return tuple(result)

def patch_tree(text):
    before=nodes(text);edits=[];changed=[];total=0
    for root in before:
        focuses=([root] if root.key=='shared_focus' else [n for n in root.children() if n.key=='focus'] if root.key=='focus_tree' else [])
        for focus in focuses:
            total+=1
            groups=[[n.value for n in p.children() if n.key=='focus'] for p in focus.children() if p.key=='prerequisite']
            availability=next((n for n in focus.children() if n.key=='available'),None)
            if availability is None:continue
            local=_edits(text,availability.children(),groups)
            if local:changed.append(field(focus.children(),'id'));edits.extend(local)
    after=_apply(text,edits)
    assert _canonical(before)==_canonical(nodes(after)),'A gate or another focus property changed'
    assert not _pending(after),'Suppression must be idempotent'
    return after,{'focuses_scanned':total,'focuses_changed':changed,'hidden_duplicate_blocks':len(edits)}

def _pending(text):
    count=0
    for root in nodes(text):
        focuses=([root] if root.key=='shared_focus' else [n for n in root.children() if n.key=='focus'] if root.key=='focus_tree' else [])
        for f in focuses:
            groups=[[n.value for n in p.children() if n.key=='focus'] for p in f.children() if p.key=='prerequisite']
            for a in f.children():
                if a.key=='available':count+=len(_edits(text,a.children(),groups))
    return count

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    report={'scope':'Presentation only; logical gates, prerequisites, rewards and all other properties preserved by AST comparison. No native hover test.','applied':args.apply,'files':[],'all_focuses_scanned':0}
    for file in sorted((ROOT/'common/national_focus').glob('*.txt')):
        original=file.read_bytes();text=original.decode('utf-8-sig');updated,details=patch_tree(text)
        report['all_focuses_scanned']+=details['focuses_scanned']
        if updated==text:continue
        data=(b'\xef\xbb\xbf' if original.startswith(b'\xef\xbb\xbf') else b'')+updated.encode('utf-8')
        if args.apply:file.write_bytes(data)
        report['files'].append({'path':file.relative_to(ROOT).as_posix(),'before_sha256':hashlib.sha256(original).hexdigest(),'after_sha256':hashlib.sha256(data).hexdigest(),**details})
    report['changed_files']=len(report['files']);report['changed_focuses']=sum(len(f['focuses_changed']) for f in report['files'])
    if args.apply:(ROOT/'tools/focus_prerequisite_ui_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))
    print(json.dumps([{k:v for k,v in f.items() if k in ('path','hidden_duplicate_blocks')} for f in report['files']],indent=2))

if __name__=='__main__':main()
