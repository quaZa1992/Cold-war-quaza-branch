# IMPERIA COLD WAR — Approved Brazil 1970 complete runtime compiler.
import argparse,hashlib,json,re,sys
from common import *
APPROVED='0b14031fbad84b84ad72a1599e47cf444a3b52523bcc26070c8f7fd94bc55875'
def sha(b):return hashlib.sha256(b).hexdigest()
def build(shared=True):
    from core import build_core
    from diplomacy import build_diplomacy
    from politics import get_build_politics
    from integration import build_integrations,build_on_actions
    raw=(HERE/'approved_design.json').read_bytes();assert sha(raw)==APPROVED
    from native_adjustments import runtime_design
    from presentation import polish_design,polish_localisation
    d=polish_design(runtime_design(json.loads(raw)));core=build_core(d);dip=build_diplomacy(d);pol=get_build_politics(d)
    from politics_presentation import polish_politics
    pol=polish_politics(pol)
    outputs={};loc={}
    for pack in (core,dip):
        for path,text in pack['files'].items():assert path not in outputs;outputs[path]=text.encode('utf-8')
        for key,val in pack['loc'].items():assert key not in loc or loc[key]==val,(key,loc.get(key),val);loc[key]=val
    for path,text in pol['files'].items():assert path not in outputs;outputs[path]=text.encode('utf-8')
    outputs.update({k:v.encode('utf-8') for k,v in build_on_actions().items()})
    if shared:
        for path,text in build_integrations(loc).items():
            assert path not in outputs
            outputs[path]=text.encode('utf-8-sig' if path.endswith('.yml') else 'utf-8')
    # Each unique finite research reward gets its own localised receipt name.
    for data in list(outputs.values()):
        text=data.decode('utf-8-sig')
        for name in re.findall(r'\bname\s*=\s*(COLDWAR_BRA_[A-Za-z0-9_]+_research_\d+)\b',text):
            loc.setdefault(name,'Brazilian Technical Programme')
    polish_localisation(loc,pol['loc'])
    outputs['localisation/english/COLDWAR_BRA_1970_politics_l_english.yml']=loc_text(pol['loc']).encode('utf-8-sig')
    outputs['localisation/english/COLDWAR_BRA_1970_l_english.yml']=loc_text(loc).encode('utf-8-sig')
    runtime=dict(d);runtime.update(status='IMPLEMENTED. Approved Brazil 1970 national programme.',approved_source_sha256=APPROVED,runtime=core['metadata'],politics_integration=pol.get('integrations',{}))
    runtime['party_integration']['status']='Implemented through native 24-slot elections, exact registered identities and scoped leader callbacks.'
    runtime['party_integration']['later']='Implemented PDS, PMDB, restored historic PTB, later PTB, PDT, PT, PFL, PSDB and PRN registration and congress decisions; PCB and PCdoB remain separate.'
    runtime['verification_limits']=['External concept renders reconstruct native geometry and artwork; they are not game screenshots.','See NATIVE_RESULT.json for bounded engine evidence. Save/reload, full campaign balance, all later successions and network multiplayer are not established by the fixture.','Unmatched historical leaders use the existing neutral portrait; no face is fabricated.']
    outputs['tools/brazil_1970_runtime/runtime_design.json']=(json.dumps(runtime,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    from catalogue import catalogue
    outputs['tools/brazil_1970_runtime/RUNTIME_CATALOGUE.md']=catalogue(runtime).encode('utf-8')
    manifest=dict(project='IMPERIA COLD WAR',feature='Brazil 1970 implementation',approved_sha256=APPROVED,focus_tree=TREE,focuses=len(d['nodes']),offers=sum('offer' in n for n in d['nodes']),english_keys=len(loc)+len(pol['loc']),shared_integration=shared,files={p:dict(sha256=sha(b),bytes=len(b)) for p,b in sorted(outputs.items())})
    for path,data in outputs.items():
        if path.endswith('.txt') or path.endswith('.gfx'):assert data.startswith(b'# IMPERIA COLD WAR') and not data.startswith(b'\xef\xbb\xbf'),path
        if path.endswith('.yml'):assert data.startswith(b'\xef\xbb\xbfl_english:\n# IMPERIA COLD WAR'),path
    return outputs,manifest
def main():
    a=argparse.ArgumentParser();a.add_argument('--check',action='store_true');a.add_argument('--generated-only',action='store_true');args=a.parse_args()
    outputs,m=build(not args.generated_only);changed=[]
    for path,b in outputs.items():
        target=ROOT/path;assert target.resolve().is_relative_to(ROOT.resolve())
        if not target.exists() or target.read_bytes()!=b:
            changed.append(path)
            if not args.check:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
    if not args.check:(HERE/'manifest.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
    print(json.dumps(dict(project='IMPERIA COLD WAR',focuses=m['focuses'],offers=m['offers'],shared=m['shared_integration'],changed=changed),indent=2))
    return int(args.check and bool(changed))
if __name__=='__main__':sys.dont_write_bytecode=True;sys.exit(main())
