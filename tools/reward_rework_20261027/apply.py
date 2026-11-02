# IMPERIA COLD WAR — Ordered installation of the Korea/Japan reward revision.
"""Own country exports only; do not rebuild unrelated readiness or other countries."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'docs/reward_rework_20261027'
BACKUP=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/reward_rework_20261027/before')
sys.path.insert(0,str(ROOT/'tools/quaza_eastasia_integration'))
import apply_reviewed as installer
from focus_art import gfx_source
installer.BEFORE=BACKUP
installer.CHANGED=[]
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,emit


def run(path):
    result=subprocess.run([sys.executable,'-B',path],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    COMMANDS.append({'command':[sys.executable,'-B',path],'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
    if result.returncode:raise RuntimeError(path+'\n'+result.stdout+'\n'+result.stderr)


def copy(source,target):
    installer.write(target,(ROOT/source).read_bytes())


def merge_localisation(source,target):
    new=(ROOT/source).read_text(encoding='utf-8-sig')
    text=(ROOT/target).read_text(encoding='utf-8-sig')
    for line in new.splitlines():
        match=re.match(r'\s+([^\s:#]+):',line)
        if not match:continue
        pattern=r'(?m)^\s+'+re.escape(match[1])+r':[^\n]*$'
        if re.search(pattern,text):text=re.sub(pattern,lambda _:line,text)
        else:text=text.rstrip()+'\n'+line+'\n'
    installer.write(target,text.encode('utf-8-sig'))


def replace_terminal_effects():
    source='tools/japan_1970/staging/constitution/terminal_effects.txt'
    target='common/scripted_effects/COLDWAR_JAP_1970_constitution.txt'
    replacements={k:body for k,op,body in parse((ROOT/source).read_text(encoding='utf-8'))}
    rows=parse((ROOT/target).read_text(encoding='utf-8'))
    assert set(replacements).issubset({k for k,o,b in rows})
    revised=[(k,o,replacements.get(k,b)) for k,o,b in rows]
    header='# IMPERIA COLD WAR — Japan 1970 constitutional rewards and original referendum integration.\n# Existing quaZa constitutional system retained; terminal rewards revised.\n'
    installer.write(target,(header+emit(revised)+'\n').encode('utf-8'))


def main():
    global COMMANDS
    COMMANDS=[]
    try:
        installer.write('interface/COLDWAR_EASTASIA_1970_focus_icons.gfx', gfx_source().encode('utf-8'))
        run('tools/north_korea_1970/compile.py')
        run('tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_runtime.py')
        run('tools/japan_1970/generate_staged_effects.py')
        run('tools/japan_1970/build_party_rewards.py')
        run('tools/japan_1970/build_constitution_rewards.py')
        foreign='tools/japan_1970/staging/foreign/'
        for name,target in (
            ('COLDWAR_JAP70_foreign_project_decisions.txt','common/decisions/'),
            ('COLDWAR_JAP70_bilateral_events.txt','events/'),
            ('COLDWAR_JAP70_bilateral_ideas.txt','common/ideas/'),
            ('COLDWAR_JAP70_bilateral_l_english.yml','localisation/english/'),
            ('COLDWAR_JAP70_multilateral_project_effects.txt','common/scripted_effects/'),
        ):copy(foreign+name,target+name)
        run('tools/japan_1970/build_diplomatic_runtime.py')
        run('tools/japan_1970/stage_focus_graph.py')
        kor=json.loads((ROOT/'docs/design/COLDWAR_KOR_1970/COLDWAR_KOR_runtime_manifest.json').read_text(encoding='utf-8'))
        stage=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/quaza_eastasia_20261027/kor_stage')
        for relative,digest in kor['files'].items():
            raw=(stage/relative).read_bytes()
            assert hashlib.sha256(raw).hexdigest()==digest,relative
            installer.write(relative,raw)
        base='tools/japan_1970/staging/'
        for source,target in (
            ('graph/focus_tree.txt','common/national_focus/COLDWAR_JAP_1970_focus.txt'),
            ('graph/focus_l_english.yml','localisation/english/COLDWAR_JAP_1970_focus_l_english.yml'),
            ('national_economy_focus_effects_scripted_effects.txt','common/scripted_effects/COLDWAR_JAP_1970_national_economy.txt'),
            ('national_economy_focus_effects_dynamic_modifiers.txt','common/dynamic_modifiers/COLDWAR_JAP_1970_national_economy.txt'),
            ('national_economy_focus_effects_l_english.yml','localisation/english/COLDWAR_JAP_1970_national_economy_l_english.yml'),
            ('party/COLDWAR_JAP_1970_party_effects.txt','common/scripted_effects/COLDWAR_JAP_1970_party_effects.txt'),
            ('party/COLDWAR_JAP_1970_party_dynamic_modifiers.txt','common/dynamic_modifiers/COLDWAR_JAP_1970_party_modifiers.txt'),
            ('party/COLDWAR_JAP_1970_party_modifiers_l_english.yml','localisation/english/COLDWAR_JAP_1970_party_modifiers_l_english.yml'),
            ('constitution/effects.txt','common/scripted_effects/COLDWAR_JAP_1970_constitution_rewards.txt'),
            ('constitution/ideas.txt','common/ideas/COLDWAR_JAP_1970_constitution_climate.txt'),
            ('constitution/localisation.yml','localisation/english/COLDWAR_JAP_1970_constitution_climate_l_english.yml'),
            ('constitution/terminal_ideas.txt','common/ideas/COLDWAR_JAP_1970_constitution.txt'),
            ('foreign/scripted_effects/COLDWAR_JAP70_native_foreign_previews.txt','common/scripted_effects/COLDWAR_JAP70_native_foreign_previews.txt'),
        ):copy(base+source,target)
        merge_localisation(base+'constitution/terminal_localisation.yml','localisation/english/COLDWAR_JAP_1970_constitution_l_english.yml')
        replace_terminal_effects()
        # Normalize only the three owned country namespaces, including new files.
        for folder in ('common','events','interface','localisation/english'):
            for path in (ROOT/folder).rglob('*'):
                if path.is_file() and re.match(r'COLDWAR_(NKO|KOR|JAP)',path.name) and path.suffix in ('.txt','.gfx','.gui','.yml'):
                    installer.write(path.relative_to(ROOT).as_posix(),path.read_bytes())
        # NK's foreign bridge is co-owned by the final KOR stage. Record the
        # final output, rather than the intermediate standalone NK compilation.
        manifest_path=ROOT/'tools/north_korea_1970/emission_manifest.json'
        manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
        manifest['project']='IMPERIA COLD WAR'
        manifest['integration_owner']='tools/reward_rework_20261027/apply.py'
        manifest['rebuild_sequence']='NKO, KOR, Japan policy/party/constitution/foreign writers, final country installation'
        manifest['output_sha256']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in manifest['root_outputs']}
        manifest_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
        success=True
    except Exception as exc:
        success=False
        COMMANDS.append({'error':str(exc)})
    result={'project':'IMPERIA COLD WAR','success':success,'commands':COMMANDS,'installed':sorted(set(installer.CHANGED)),'backup':str(BACKUP),'scope':'Country rewards and existing integration hooks. Readiness, other countries and their pending work are not rebuilt.'}
    (REPORT/'EMISSION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'success':success,'installed':len(result['installed']),'errors':[r for r in COMMANDS if 'error' in r]}))
    return not success


if __name__=='__main__':raise SystemExit(main())
