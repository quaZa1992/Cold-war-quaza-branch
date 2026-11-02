# IMPERIA COLD WAR — Install reviewed East Asia outputs and narrow native integrations.
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import re
from source import ROOT,REPORT,SNAPSHOT,DONOR
from install import normalise,MARK

BEFORE=SNAPSHOT.parent/'before'
CHANGED=[]


def write(relative,raw):
    path=ROOT/relative
    old=path.read_bytes() if path.exists() else None
    if old is not None:
        backup=BEFORE/relative
        if not backup.exists():backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(old)
    owned=re.search(r'COLDWAR_(?:NKO|KOR|JAP|JAP70|nuclear_)',relative)
    if owned:raw=normalise(relative,raw)
    else:
        text=raw.decode('utf-8-sig').replace('\r\n','\n')
        baseline=(BEFORE/relative).read_text(encoding='utf-8-sig') if (BEFORE/relative).exists() else ''
        original_lines=set(baseline.splitlines())
        lines=[]
        for line in text.splitlines():
            original=line.replace('# IMPERIA COLD WAR','# IMPERIA CW',1)
            lines.append(original if original!=line and original in original_lines else line)
        if relative.endswith('.yml'):
            lines=[line for line in lines if line.strip()!='l_english:' and line!=MARK]
            raw=('l_english:\n'+MARK+'\n'+'\n'.join(lines)+'\n').encode('utf-8-sig')
        else:
            text='\n'.join(lines)+'\n'
            if not text.startswith('# IMPERIA COLD WAR — '):text=MARK+'\n'+text
            raw=text.encode('utf-8')
    if old!=raw:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
    CHANGED.append(relative)


def patch(relative,transform):
    path=ROOT/relative
    write(relative,transform(path.read_text(encoding='utf-8-sig')).encode('utf-8'))


def japan_history(text):
    if 'load_focus_tree = COLDWAR_JAP_1970_focus' in text:return text
    old='load_focus_tree = mdcw_1970_generic_focus'
    assert text.count(old)==1
    return text.replace(old,MARK+'\n\t\tload_focus_tree = COLDWAR_JAP_1970_focus\n\t\tadd_ideas = { COLDWAR_JAP_1970_article9_self_defence COLDWAR_JAP_1970_okinawa_and_the_bases }\n\t\tCOLDWAR_JAP_1970_initialize_starting_modifiers = yes\n\t\tCOLDWAR_JAP_1970_party_modifiers_initialize = yes',1)


def japan_fallback(text):
    body='AND = { original_tag = JAP IMP_is_1970_scenario = yes }'
    if body in text:return text
    anchor='\t\t\t\t\toriginal_tag = USA'
    assert text.count(anchor)==1
    return text.replace(anchor,'\t\t\t\t\t'+MARK+'\n\t\t\t\t\t'+body+'\n'+anchor,1)


def main():
    manifest=json.loads((ROOT/'docs/design/COLDWAR_KOR_1970/COLDWAR_KOR_runtime_manifest.json').read_text(encoding='utf-8'))
    stage=SNAPSHOT.parent/'kor_stage'
    for relative,digest in manifest['files'].items():
        raw=(stage/relative).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==digest,relative
        write(relative,raw)
    here=ROOT/'tools/japan_1970/staging'
    for source,target in (
        ('graph/focus_tree.txt','common/national_focus/COLDWAR_JAP_1970_focus.txt'),
        ('graph/focus_l_english.yml','localisation/english/COLDWAR_JAP_1970_focus_l_english.yml'),
        ('national_economy_focus_effects_scripted_effects.txt','common/scripted_effects/COLDWAR_JAP_1970_national_economy.txt'),
        ('national_economy_focus_effects_dynamic_modifiers.txt','common/dynamic_modifiers/COLDWAR_JAP_1970_national_economy.txt'),
        ('national_economy_focus_effects_l_english.yml','localisation/english/COLDWAR_JAP_1970_national_economy_l_english.yml'),
        ('foreign/scripted_effects/COLDWAR_JAP70_native_foreign_previews.txt','common/scripted_effects/COLDWAR_JAP70_native_foreign_previews.txt'),
    ):write(target,(here/source).read_bytes())
    patch('history/countries/JAP - Japan.txt',japan_history)
    patch('common/scripted_effects/mdcw_1970_focus_tree_effects.txt',japan_fallback)
    # Import functions only. The donor's __main__ writer is never run over this
    # checkout, and its obsolete baseline archives are never created here.
    path=ROOT/'tools/nuclear_readiness/integrate.py'
    spec=importlib.util.spec_from_file_location('reviewed_readiness_integration',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    for relative,transform in (
        ('common/raids/nuclear_raids.txt',module.raids),
        ('common/scripted_effects/00_money_system.txt',module.economy),
        ('common/scripted_effects/mdcw_imperia_nuclear_effects.txt',module.damage),
        ('common/scripted_triggers/01_raids_triggers.txt',module.doctrine),
        ('common/decisions/categories/99_SOV_decision_categories.txt',module.legacy),
        ('localisation/english/MD_money_l_english.yml',module.money_loc),
    ):patch(relative,transform)
    # Export generated readiness text without re-rendering approved binary art.
    sys.path.insert(0,str(ROOT/'tools/nuclear_readiness'))
    import build
    for relative,text in build.FILES.items():write(relative,text.encode('utf-8'))
    loc=build.localisation_source(MARK)
    write('localisation/english/COLDWAR_nuclear_readiness_l_english.yml',loc.encode('utf-8'))
    # All newly-owned live files have a valid first marker and encoding.
    imported=json.loads((REPORT/'INITIAL_IMPORT.json').read_text(encoding='utf-8'))
    for relative in imported['files']:
        if relative.startswith(('common/','events/','interface/','localisation/english/')):
            write(relative,(ROOT/relative).read_bytes())
    result={'project':'IMPERIA COLD WAR','source_commit':DONOR,'installed':sorted(set(CHANGED)),
            'scope':'Reviewed feature outputs and selected native hooks. Existing unrelated country, economy, raid policy and pending working-tree changes retained.'}
    (REPORT/'INTEGRATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    from receipts import reconcile
    reconcile()
    print(json.dumps({'project':'IMPERIA COLD WAR','installed':len(result['installed'])}))


if __name__=='__main__':
    current=ROOT/'tools/reward_rework_20261027/apply.py'
    if current.is_file():
        import subprocess
        raise SystemExit(subprocess.run([sys.executable,'-B',str(current)],cwd=ROOT).returncode)
    main()
