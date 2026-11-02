# IMPERIA CW — Cold War: bounded RAF integration build; preserve unrelated live work.
"""Render canonical German sources in memory, install only security-owned blocks."""
from pathlib import Path
import hashlib
import json
import re
import sys
import compile as generator

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/spain_1970_v2'))
from script_ast import parse,first,walk
P='COLDWAR_GER_1970'


def spans(text,key=None,identity=None):
    """Brace-aware spans retaining all bytes outside selected native blocks."""
    out=[]
    for m in re.finditer(r'(?m)^[ \t]*([\w.]+)\s*=\s*\{',text):
        if key is not None and m[1]!=key:continue
        start=m.start();brace=text.index('{',m.start(),m.end());depth=1;i=brace+1;quote=False;comment=False
        while depth:
            c=text[i]
            if comment:
                if c=='\n':comment=False
            elif quote:
                if c=='\\':i+=1
                elif c=='"':quote=False
            elif c=='"':quote=True
            elif c=='#':comment=True
            elif c=='{':depth+=1
            elif c=='}':depth-=1
            i+=1
        if identity is not None:
            node=first(parse(text[start:i]),m[1]);field,value=identity
            if first(node,field,'').strip('"')!=value:continue
        out.append((start,i,text[start:i]))
    return out


def replace(old,new,key,identity=None):
    source=spans(new,key,identity);target=spans(old,key,identity)
    if len(source)!=1 or len(target)!=1:raise ValueError('Ambiguous block '+str((key,identity,len(source),len(target))))
    a,b,_=target[0]
    return old[:a]+source[0][2]+old[b:]


def main():
    captured={}
    def capture(root,rel,text,bom=False):
        if not bom and not text.startswith('# IMPERIA CW'):text=generator.HEADER+text
        captured[rel]=(text,bom)
        return rel
    generator.write=capture
    generator.build(str(ROOT),scripts_only=True)
    writes={};review={}
    def read(rel):return (ROOT/rel).read_text(encoding='utf-8-sig')
    for rel,(new,bom) in captured.items():
        names=[]
        if 'COLDWAR_DDR_1970_relations' in rel:continue
        if rel.endswith('_security_contract.txt'):
            writes[rel]=(new,bom);continue
        old=read(rel);result=old
        if rel==f'common/scripted_effects/{P}_effects.txt':
            names=[P+'_terror_tick',P+'_monthly']
        elif rel==f'common/scripted_effects/{P}_windows_effects.txt':
            names=[k for k,o,v in parse(new) if k.startswith(P+'_sec_')]
        elif rel==f'common/scripted_triggers/{P}_windows_triggers.txt':
            names=[k for k,o,v in parse(new) if k.startswith(P+'_sec_')]
        elif rel==f'common/scripted_guis/{P}_windows.txt':
            names=[k for k,o,v in first(parse(new),'scripted_gui') if str(first(v,'window_name','')).strip('"').startswith('cwgg_sec_')]
        elif rel==f'interface/{P}_windows.gui':
            for k,o,v in first(parse(new),'guiTypes'):
                name=first(v,'name','').strip('"')
                if k=='containerWindowType' and name.startswith('cwgg_sec_'):
                    result=replace(result,new,k,('name',name));review.setdefault(rel,[]).append(name)
        elif rel==f'common/scripted_localisation/{P}_windows.txt':
            for k,o,v in parse(new):
                name=first(v,'name','').strip('"') if isinstance(v,list) else ''
                if k=='defined_text' and name.startswith('SEC_'):
                    if spans(result,k,('name',name)):result=replace(result,new,k,('name',name))
                    else:result+='\n'+spans(new,k,('name',name))[0][2]+'\n'
                    review.setdefault(rel,[]).append(name)
        elif rel==f'common/national_focus/{P}_focus.txt':
            for k,o,v in first(parse(new),'focus_tree'):
                if k=='focus' and P+'_sec_gui_refresh' in {x for x,y,z in walk(first(v,'completion_reward',[]))}:
                    name=first(v,'id');result=replace(result,new,k,('id',name));review.setdefault(rel,[]).append(name)
        elif rel==f'events/{P}_events.txt':
            result=replace(result,new,'country_event',('id','COLDWAR_GER.57'));review[rel]=['COLDWAR_GER.57']
        elif rel==f'localisation/english/{P}_l_english.yml':
            lines=dict(re.findall(r'(?m)^ ([^:\s]+):0 (".*")$',new))
            old_lines=dict(re.findall(r'(?m)^ ([^:\s]+):0 (".*")$',result))
            for key,value in lines.items():
                if not (key.startswith(('cwgg_sec_','cwsec_log_','cwfo_tt_unlock_cwsec_',P+'_security_')) or key==P+'_tt_sec_window'):continue
                if key in old_lines:result=re.sub(r'(?m)^ '+re.escape(key)+r':0 ".*"$',lambda _:f' {key}:0 {value}',result)
                else:result+=f' {key}:0 {value}\n'
                review.setdefault(rel,[]).append(key)
        for name in names:
            result=replace(result,new,name);review.setdefault(rel,[]).append(name)
        if result!=old:writes[rel]=(result,bom)
    # Write only after every expected existing block has been found exactly once.
    for rel,(text,bom) in writes.items():
        path=ROOT/rel;blob=text.encode('utf-8-sig' if bom else 'utf-8')
        if not path.exists() or path.read_bytes()!=blob:path.write_bytes(blob)
    report=dict(files=sorted(writes),blocks=review,sha256={rel:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() for rel in writes},engine_tested=False)
    (Path(__file__).parent/'security_integration.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(files=len(writes),blocks=sum(map(len,review.values())),engine_tested=False)))


if __name__=='__main__':main()
