# IMPERIA CW — Cold War: isolated Syria focus-owned reform build and installation.
"""Generate in a temporary country-only tree. Never patch shared integration."""
from pathlib import Path
from copy import deepcopy
import hashlib,json,shutil,sys,tempfile,zipfile
import build_content as compiler

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
REPORT=ROOT/'docs/syria_1970_streamlining_20261021'
BASELINE=HERE/'streamlining_baseline.json'

def prepare():
    if BASELINE.exists():return
    REPORT.mkdir(parents=True,exist_ok=True)
    paths=sorted(p for directory in ['common','events','localisation/english'] for p in (ROOT/directory).rglob('COLDWAR_SYR*') if p.is_file())
    old=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
    baseline={'feature':'IMPERIA CW — Cold War: Syrian focus-owned rewards','hashes':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'nodes':{n['id']:{'modifiers':n['modifiers'],'xy':n['xy'],'prerequisites':n['prerequisites'],'mutually_exclusive':n['mutually_exclusive'],'days':n['days'],'treasury_cost_bn':n['treasury_cost_bn']} for n in old['nodes']}}
    with zipfile.ZipFile(REPORT/'before.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for p in paths:archive.write(p,p.relative_to(ROOT).as_posix())
        archive.write(HERE/'manifest.json','tools/syria_1970/manifest.json')
    BASELINE.write_text(json.dumps(baseline,indent=2)+'\n',encoding='utf-8')

def generate():
    import politics,foreign,streamlining,decision_presentation,negative_localisation
    from english_ui import improve
    prepare()
    data=compiler.clean(json.loads((HERE/'design_source.json').read_text(encoding='utf-8')))
    compiler.amend_costs(data);compiler.apply_english(data);compiler.apply_runtime_policy(data)
    politics.augment(data)
    compiler.LOC.clear();compiler.OUTPUTS.clear()
    original_write=compiler.write
    with tempfile.TemporaryDirectory(prefix='staging_streamlining_',dir=HERE) as temporary:
        stage=Path(temporary)
        assert stage.resolve().is_relative_to(HERE.resolve()),'Temporary cleanup must remain inside the tools workspace'
        for rel in ['tools/israel_1970/script_format.py','gfx/flags/SYR_BAATH_1970.tga']:
            target=stage/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,target)
        (stage/'tools/syria_1970').mkdir(parents=True,exist_ok=True)
        def write(relative,source,bom=False):
            target=stage/relative;target.parent.mkdir(parents=True,exist_ok=True)
            if 'IMPERIA CW' not in source:
                source=source.replace('l_english:\n','l_english:\n'+compiler.PROJECT_MARKER,1) if relative.endswith('.yml') else compiler.PROJECT_MARKER+source
            if relative.endswith('.txt'):source=compiler.FORMAT.format_script(source)
            target.write_text(source,encoding='utf-8-sig' if bom else 'utf-8',newline='\n')
        compiler.write=write
        try:
            politics.install(stage,data,shared=False);foreign.install(stage,data)
            streamlining.augment(data,json.loads(BASELINE.read_text(encoding='utf-8')))
            effects=compiler.programmes(data)+compiler.entry_reward_migration(data)
            compiler.compile_focuses(data);compiler.integration(data,effects,shared=False)
            # Original presentation pass reads only the isolated country build.
            decision_presentation.install(stage,data,write)
            improve(compiler.LOC)
            write('localisation/english/COLDWAR_SYR_focus_l_english.yml','l_english:\n'+'\n'.join(' '+k+':0 '+json.dumps(v,ensure_ascii=False) for k,v in compiler.LOC.items())+'\n',True)
            negative_localisation.install(stage,write)
            outputs={p.relative_to(stage).as_posix():p.read_text(encoding='utf-8-sig') for folder in ['common','events','localisation/english'] for p in (stage/folder).rglob('COLDWAR_SYR*') if p.is_file()}
            outputs,report=streamlining.transform(outputs,data)
        finally:compiler.write=original_write
    return outputs,data,report

def main():
    prepare()
    if '--prepare' in sys.argv:print('Syria source snapshot prepared.');return
    outputs,data,report=generate()
    snapshot=json.loads(BASELINE.read_text(encoding='utf-8'))
    hashes_path=HERE/'build_hashes.json';hashes=json.loads(hashes_path.read_text(encoding='utf-8'))
    installed=json.loads((HERE/'manifest.json').read_text(encoding='utf-8')).get('streamlining_revision')
    expected=hashes['outputs'] if installed else snapshot['hashes']
    changed=[]
    for rel,source in outputs.items():
        p=ROOT/rel;payload=source.lstrip('\ufeff').encode('utf-8-sig' if rel.endswith('.yml') else 'utf-8')
        actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
        if actual!=expected.get(rel):raise RuntimeError('File changed outside this build: '+rel)
        if p.exists() and p.read_bytes()==payload:continue
        changed.append(rel)
    if '--dry-run' not in sys.argv:
        for rel in changed:
            p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.coldwar_tmp');t.write_bytes(outputs[rel].lstrip('\ufeff').encode('utf-8-sig' if rel.endswith('.yml') else 'utf-8'));t.replace(p)
        (HERE/'manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        for rel in outputs:hashes['outputs'][rel]=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
        hashes['streamlining_revision']=data['streamlining_revision'];hashes_path.write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
    previous=json.loads((REPORT/'IMPLEMENTATION_REPORT.json').read_text(encoding='utf-8')) if (REPORT/'IMPLEMENTATION_REPORT.json').exists() else {}
    report.update(changed_files=sorted(set(changed)|set(previous.get('changed_files',[]))),written_files_this_run=changed,dry_run='--dry-run' in sys.argv,engine_tested=False)
    (REPORT/'IMPLEMENTATION_REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['retained_events','automatic_offers']},indent=2))

if __name__=='__main__':main()
