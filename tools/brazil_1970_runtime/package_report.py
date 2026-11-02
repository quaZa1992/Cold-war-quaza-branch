# IMPERIA COLD WAR — Brazil final package and frozen native-source comparison.
from pathlib import Path
import hashlib,json,sys
from common import ROOT,HERE

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    m=json.loads((HERE/'manifest.json').read_text());art=json.loads((HERE/'art_manifest.json').read_text());native=json.loads((HERE/'NATIVE_RESULT.json').read_text())
    errors=[];package={}
    for rel,expected in m['files'].items():
        p=ROOT/rel
        if not p.is_file():errors.append('Missing emitted file '+rel);continue
        actual=digest(p);package[rel]=actual
        if actual!=expected['sha256']:errors.append('Emitted drift '+rel)
    for family in ('focus_icons','event_pictures','idea_icons','group_idea_icons'):
        for row in art[family].values():
            rel=row.get('source_texture',row.get('asset'));p=ROOT/rel
            if not p.is_file():errors.append('Missing art '+rel)
            else:package[rel]=digest(p)
    for p in sorted(HERE.glob('*.py'))+sorted((HERE/'politics_templates').glob('*.txt')):
        rel=p.relative_to(ROOT).as_posix();package[rel]=digest(p)
        if not p.read_bytes().startswith('# IMPERIA COLD WAR — '.encode()):errors.append('Authoring marker '+rel)
    for name in ('approved_design.json','APPROVAL.json','art_manifest.json','leader_portraits.json','README.md','NOTICE.md','NATIVE_RESULT.json','NATIVE_CHECKPOINTS.txt','english_polish.json','focus_art_polish.json','POLISH_BASELINE.json'):
        p=HERE/name;package[p.relative_to(ROOT).as_posix()]=digest(p)
    sprite=ROOT/'interface/COLDWAR_BRA_1970.gfx';package[sprite.relative_to(ROOT).as_posix()]=digest(sprite)
    run_manifest=json.loads((Path(native['run'])/'manifest.json').read_text());frozen=run_manifest['frozen_sources'];drift=[];art_drift=[]
    for rel,h in frozen.items():
        if digest(ROOT/rel)!=h:drift.append(rel)
    errors.extend('Native-tested runtime drift '+p for p in drift)
    for rel,h in run_manifest.get('referenced_art_sha256',{}).items():
        if digest(ROOT/rel)!=h:art_drift.append(rel)
    errors.extend('Native-tested art drift '+p for p in art_drift)
    if not native['native_pass']:errors.append('Native fixture did not pass')
    if digest(HERE/'approved_design.json')!=m['approved_sha256']:errors.append('Approval changed')
    report=dict(project='IMPERIA COLD WAR',feature='Brazil 1970 final package',native_assertions=dict(expected=native['expected'],passed=native['passed'],feature_diagnostics=len(native['feature_diagnostics'])),native_tested_runtime_files=len(frozen),native_tested_art_references=len(run_manifest.get('referenced_art_sha256',{})),native_runtime_drift=drift,native_art_drift=art_drift,files=package,errors=errors,boundary='File/hash and bounded native behavior evidence. Full focus hover, save/reload, later campaign progression and network multiplayer are not verified.')
    (HERE/'PACKAGE_CHECK.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(files=len(package),native_tested_runtime_files=len(frozen),native_pass=native['native_pass'],runtime_drift=drift,errors=errors),indent=2))
    return int(bool(errors))
if __name__=='__main__':sys.dont_write_bytecode=True;sys.exit(main())
