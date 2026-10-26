# IMPERIA CW — Cold War: Cold War SOV design — parse.
import re, json, sys
TOK = re.compile(r'"[^"]*"|[{}=<>]|[^\s{}=<>#"]+|#[^\n]*')
def tokenize(s):
    return [t for t in TOK.findall(s) if not t.startswith('#')]
def parse(tokens, i=0):
    out=[]
    while i < len(tokens):
        t=tokens[i]
        if t=='}': return out, i+1
        if i+1<len(tokens) and tokens[i+1] in ('=','<','>'):
            op=tokens[i+1]; v=tokens[i+2]
            if v=='{':
                sub,i=parse(tokens,i+3); out.append((t,op,sub))
            else:
                out.append((t,op,v)); i+=3
        elif t=='{':
            sub,i=parse(tokens,i+1); out.append(('',None,sub))
        else:
            out.append((t,None,None)); i+=1
    return out,i
def load(path):
    s=open(path,encoding='utf-8-sig',errors='replace').read()
    return parse(tokenize(s))[0]
def get(block,key):
    return [v for k,o,v in block if k==key]
def dump(block,ind=0):
    r=[]
    for k,o,v in block:
        if isinstance(v,list):
            r.append('\t'*ind+f'{k} {o or ""} {{'); r+=dump(v,ind+1); r.append('\t'*ind+'}')
        else:
            r.append('\t'*ind+(f'{k} {o} {v}' if o else k))
    return r
def walk_keys(block, acc):
    for k,o,v in block:
        acc.append(k)
        if isinstance(v,list): walk_keys(v,acc)
