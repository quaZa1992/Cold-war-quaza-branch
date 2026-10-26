# IMPERIA CW — Cold War: Syria 1970 content imported from quaZa.
"""Read-only comparison of the two 19 October crash minidumps."""
from pathlib import Path
import struct,json

ROOT=Path(r'C:\Users\sonyz\Documents\Paradox Interactive\Hearts of Iron IV\crashes')
EXE=Path(r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\hoi4.exe').read_bytes()
PE=struct.unpack_from('<I',EXE,0x3c)[0]
NSEC=struct.unpack_from('<H',EXE,PE+6)[0]
OSIZE=struct.unpack_from('<H',EXE,PE+20)[0]
PREFERRED_BASE=struct.unpack_from('<Q',EXE,PE+24+24)[0]
SECTIONS=[struct.unpack_from('<8sIIII',EXE,PE+24+OSIZE+40*i) for i in range(NSEC)]

def parse(name):
    raw=(ROOT/name/'minidump.dmp').read_bytes()
    sig,version,count,dirrva=struct.unpack_from('<4sIII',raw)
    streams={}
    for i in range(count):
        kind,size,rva=struct.unpack_from('<III',raw,dirrva+12*i)
        streams[kind]=(size,rva)
    size,rva=streams[6]
    tid=struct.unpack_from('<I',raw,rva)[0]
    code,flags,record,address,np=struct.unpack_from('<IIQQI',raw,rva+8)
    params=list(struct.unpack_from('<15Q',raw,rva+40))[:np]
    csize,crva=struct.unpack_from('<II',raw,rva+160)
    names=['Rax','Rcx','Rdx','Rbx','Rsp','Rbp','Rsi','Rdi','R8','R9','R10','R11','R12','R13','R14','R15','Rip']
    regs=dict(zip(names,struct.unpack_from('<17Q',raw,crva+120)))
    modules=[]
    _,mrva=streams[4]
    mn=struct.unpack_from('<I',raw,mrva)[0]
    for i in range(mn):
        off=mrva+4+i*108
        base,msize,checksum,timestamp,nrva=struct.unpack_from('<QIIII',raw,off)
        nbytes=struct.unpack_from('<I',raw,nrva)[0]
        mname=raw[nrva+4:nrva+4+nbytes].decode('utf-16le')
        modules.append((base,msize,mname))
    memory=[]
    if 5 in streams:
        _,mm=streams[5]
        n=struct.unpack_from('<I',raw,mm)[0]
        for i in range(n):
            start,sz,rr=struct.unpack_from('<QII',raw,mm+4+i*16)
            memory.append((start,sz,rr))
    if 9 in streams:
        _,mm=streams[9]
        n,rr=struct.unpack_from('<QQ',raw,mm)
        for i in range(n):
            start,sz=struct.unpack_from('<QQ',raw,mm+16+i*16)
            memory.append((start,sz,rr));rr+=sz
    mainbase=next(b for b,s,n in modules if n.lower().endswith('hoi4.exe'))
    def read(addr,n):
        for start,sz,rr in memory:
            if start<=addr and addr+n<=start+sz:
                return raw[rr+addr-start:rr+addr-start+n]
        rv=addr-mainbase
        for name,vs,va,rs,rr in SECTIONS:
            if va<=rv and rv+n<=va+rs:return EXE[rr+rv-va:rr+rv-va+n]
        return None
    def mod_for(addr):
        for base,sz,name in modules:
            if base<=addr<base+sz:return Path(name).name+'+'+hex(addr-base)
    stack=[]
    sb=read(regs['Rsp'],1024)
    if sb:
        for i,v in enumerate(struct.unpack('<128Q',sb)):
            mod=mod_for(v)
            if mod:stack.append({'offset':hex(i*8),'address':hex(v),'module':mod})
    strings=[]
    for reg,addr in regs.items():
        b=read(addr,256)
        if b:
            s=b.split(b'\x00',1)[0]
            if len(s)>3 and all(32<=c<127 for c in s):strings.append({'register':reg,'ascii':s.decode()})
    objs={}
    for reg,addr in regs.items():
        if reg in ('Rip','Rax','Rcx','Rdi','R15'):continue
        b=read(addr,128)
        if b:
            vals=struct.unpack('<16Q',b)
            objs[reg]={'words':[hex(x) for x in vals],'pointers':[]}
            vf=read(vals[0]-8,8)
            if vf:
                coladdr=struct.unpack('<Q',vf)[0]
                if PREFERRED_BASE<=coladdr<PREFERRED_BASE+0x4000000:coladdr+=mainbase-PREFERRED_BASE
                col=read(coladdr,24)
                if col:
                    sig,off,cd,td,ch,selfr=struct.unpack('<6I',col)
                    if sig==1:
                        tdb=read(mainbase+td,192)
                        if tdb:objs[reg]['rtti']=tdb[16:].split(b'\0',1)[0].decode('ascii',errors='replace')
            for i,x in enumerate(vals):
                desc={'offset':hex(8*i),'value':hex(x)}
                pb=read(x,128)
                if pb:
                    desc['bytes']=pb.hex()
                    desc['ascii']=''.join(chr(c) if 32<=c<127 else '.' for c in pb)
                m=mod_for(x)
                if m:desc['module']=m
                if pb or m:objs[reg]['pointers'].append(desc)
    return {'name':name,'dump_bytes':len(raw),'thread':tid,'exception':{'code':hex(code),'address':hex(address),'module':mod_for(address),'params':[hex(p) for p in params]},'registers':{k:hex(v) for k,v in regs.items()},'module_return_candidates':stack,'register_strings':strings,'streams':streams,'instruction_bytes':(read(regs['Rip']-32,128) or b'').hex(),'caller_bytes':(read(struct.unpack_from('<Q',sb,0x38)[0]-128,192) or b'').hex(),'objects':objs,'main_module':next(({'name':n,'base':hex(b),'size':hex(s)} for b,s,n in modules if n.lower().endswith('hoi4.exe')),None)}

if __name__=='__main__':
    results=[parse(n) for n in ['hoi4_20261019_100834','hoi4_20261019_103748']]
    print(json.dumps(results,indent=2))
