# IMPERIA CW — Cold War: narrow Spain V2 integration and retired-tree cleanup.
"""Preserve other countries, native later starts, colour and historical party data."""
from pathlib import Path
import json,re,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MARK='# IMPERIA CW — Cold War: Spain V2 national programme.'

def write(path,text):
    blob=text.encode('utf-8')
    if not path.exists() or path.read_bytes()!=blob:path.write_bytes(blob)

def patch_party_registry(root):
    path=root/'common/scripted_localisation/mdcw_historical_parties.txt'
    text=path.read_bytes().decode('utf-8-sig');eol='\r\n' if '\r\n' in text else '\n'
    # The shared registry generator retains these exact single-line COLDWAR branches.
    text=re.sub(r'(?m)^.*# COLDWAR SPR V2 REGISTRY[^\r\n]*\r?\n','',text)
    text=re.sub(r'(?m)^\s*# IMPERIA CW — Cold War: Spain V2 cabinet identity\.\r?\n','',text)
    sets={
      'conservatism':[
        ('has_country_flag = COLDWAR_SPR_mandate_ap_pp date > 1988.12.31','pp'),
        ('has_country_flag = COLDWAR_SPR_mandate_ap_pp','ap'),
        ('has_country_flag = COLDWAR_SPR_mandate_ucd','ucd')],
      'liberalism':[('date > 1982.7.28','cds')],
      'communist_state':[('date > 1986.4.26','iu')],
      'Nat_Fascism':[('COLDWAR_SPR_franco_has_left_office = yes','falange')],
      'Nat_Autocracy':[('COLDWAR_SPR_government_continuity = yes','continuity')],
    }
    for ideology,rows in sets.items():
        for suffix in ['', '_desc', '_icon']:
            key='MDCW_HP_'+ideology+suffix
            pattern=r'(?m)^(\s*name = '+re.escape(key)+r'\s*\r?\n)'
            matches=list(re.finditer(pattern,text))
            if len(matches)!=1:raise ValueError('Registry definition changed '+key)
            branches='\t# IMPERIA CW — Cold War: Spain V2 cabinet identity.'+eol+''.join('\ttext = { trigger = { tag = SPR IMP_is_1970_scenario = yes '+gate+' } localization_key = COLDWAR_SPR_registry_'+label+suffix+' } # COLDWAR SPR V2 REGISTRY'+eol for gate,label in rows)
            at=matches[0].end();text=text[:at]+branches+text[at:]
    write(path,text)
    # MD's non-registry descriptions and outlook tooltips share the same identity.
    path=root/'common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt'
    text=path.read_bytes().decode('utf-8-sig')
    text=text.replace('has_country_flag = COLDWAR_SPR_cabinet_ap','has_country_flag = COLDWAR_SPR_mandate_ap_pp')
    text=text.replace('has_country_flag = COLDWAR_SPR_cabinet_ucd','has_country_flag = COLDWAR_SPR_mandate_ucd')
    text=text.replace('has_country_flag = COLDWAR_SPR_continuity_settlement','COLDWAR_SPR_government_continuity = yes')
    text=text.replace('# IMPERIA CW — Cold War: Spain 1970 national programme.',MARK)
    write(path,text)

def patch_bookmark(root):
    path=root/'common/bookmarks/blitzkrieg.txt';text=path.read_bytes().decode('utf-8-sig')
    for a,b in {'COLDWAR_SPR_1969_settlement':'COLDWAR_SPR_last_years','COLDWAR_SPR_administrative_reform':'COLDWAR_SPR_third_development_plan','COLDWAR_SPR_labour_charter':'COLDWAR_SPR_armed_forces_review'}.items():text=text.replace(a,b)
    if 'COLDWAR_SPR_last_years' not in text:raise ValueError('Spain bookmark route not found')
    anchor='\t\t\t\tCOLDWAR_SPR_last_years'
    if MARK not in text:text=text.replace(anchor,'\t\t\t\t'+MARK+'\n'+anchor)
    write(path,text)

def retire(root):
    snapshot=json.loads((HERE/'retired_snapshot.json').read_text(encoding='utf-8'))
    keep={'common/national_focus/COLDWAR_SPR_1970_focus.txt',
          'common/on_actions/COLDWAR_SPR_colour.txt','common/scripted_effects/COLDWAR_SPR_colour.txt',
          'localisation/english/COLDWAR_SPR_colour_l_english.yml','localisation/english/COLDWAR_SPR_registry_l_english.yml'}
    removed=[]
    for rel,sha in snapshot.items():
        if rel.startswith('tools/') or rel in keep:continue
        # Only the archived wholly custom basename family is owned here.
        path=(root/rel).resolve()
        if root.resolve() not in path.parents or not path.name.startswith('COLDWAR_SPR_'):raise ValueError('Unsafe retired path '+rel)
        if not path.exists():continue
        if hashlib.sha256(path.read_bytes()).hexdigest()!=sha:raise ValueError('Legacy file changed during implementation '+rel)
        path.unlink();removed.append(rel)
    # Old generation entry points must never reinstall the rejected 301-node design.
    oldroot=root/'tools/spain_1970'
    retired='''# IMPERIA CW — Cold War: retired Spain authoring entry point.
"""Compatibility redirect. The rejected Spain design is archived outside the mod."""
from pathlib import Path
import runpy,sys
target=Path(__file__).resolve().parents[1]/'spain_1970_v2'/'compile.py'
sys.path.insert(0,str(target.parent))
runpy.run_path(str(target),run_name='__main__')
'''
    # Archive has been created and the old canonical files have not changed.
    oldfiles=[]
    already_retired=(HERE/'retirement.json').exists()
    if oldroot.exists() and not already_retired:
        for path in oldroot.rglob('*'):
            if not path.is_file() or '__pycache__' in path.parts:continue
            rel=path.relative_to(root).as_posix()
            if rel not in snapshot:raise ValueError('Unexpected old tool '+rel)
            if hashlib.sha256(path.read_bytes()).hexdigest()!=snapshot[rel]:raise ValueError('Old tool changed '+rel)
            oldfiles.append(path)
        for path in oldfiles:path.unlink()
    oldroot.mkdir(exist_ok=True)
    for name in ['compile.py','rebuild.py']:write(oldroot/name,retired)
    write(oldroot/'README.md','# IMPERIA CW — Cold War: Spain authoring moved\n\nThe accepted 231-focus implementation is in `../spain_1970_v2`. Old command entry points redirect there. The rejected design and providers have been retired.\n')
    if not already_retired:
        (HERE/'retirement.json').write_text(json.dumps({'removed_loaded_files':removed,'retired_authoring_files':len(oldfiles),'preserved':sorted(keep),'backup':'External thread visualization directory / spain-new-concept/retired-spain-implementation.zip'},indent=2)+'\n',encoding='utf-8')
    return removed

def main():
    patch_party_registry(ROOT);patch_bookmark(ROOT)
    removed=retire(ROOT)
    print(json.dumps({'retired_loaded_files':len(removed),'registry':'actual cabinet mandates','bookmark':'approved opening/development/armed-forces IDs'}))

if __name__=='__main__':main()
