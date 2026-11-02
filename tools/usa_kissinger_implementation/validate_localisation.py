# IMPERIA COLD WAR — Regional decision, event and dynamic localisation closure.
"""Read installed output. This checks references, not live text rendering."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from focus_prerequisite_ui import nodes,field

P='COLDWAR_USA_KS_'
STEM='COLDWAR_USA_kissinger'


def walk(rows):
    for node in rows:
        yield node
        yield from walk(node.children())


def main():
    loc_path=ROOT/f'localisation/english/{STEM}_l_english.yml'
    loc_rows=re.findall(r'^\s*([^#\s:]+):\d*\s+"(.*)"\s*$',loc_path.read_text(encoding='utf-8-sig'),re.M)
    loc=dict(loc_rows);findings=[]
    def require(ok,message):
        if not ok:findings.append(message)
    paths=[ROOT/f'common/{family}/{STEM}.txt' for family in ('decisions','scripted_effects','scripted_triggers','scripted_localisation')]
    paths += [ROOT/f'common/decisions/categories/{STEM}.txt',ROOT/f'events/{STEM}.txt',ROOT/f'interface/{STEM}.gui',ROOT/'events/COLDWAR_USA_triangular.txt',ROOT/'events/COLDWAR_USA_triangular_statecraft.txt']
    all_rows=[node for path in paths for node in walk(nodes(path.read_text(encoding='utf-8-sig')))]
    implicit=0
    for path in (paths[0],paths[4]):
        for category in nodes(path.read_text(encoding='utf-8-sig')):
            entries=category.children() if path==paths[0] else [category]
            for node in entries:
                if path==paths[0] and not any(child.key=='complete_effect' for child in node.children()):continue
                for key in (node.key,node.key+'_desc'):
                    require(key in loc,'Missing implicit localisation: '+key);implicit+=1
    event_references=0
    for node in all_rows:
        if node.key in ('title','desc','name') and isinstance(node.value,str) and node.value.startswith(('COLDWAR_USA_KS.','COLDWAR_USA_TD.','COLDWAR_USA_TDSP.')):
            require(node.value in loc,'Missing event text: '+node.value);event_references+=1
    defined={field(node.children(),'name') for node in all_rows if node.key=='defined_text'}
    for node in all_rows:
        if node.key=='text' and isinstance(node.value,str):
            for token in re.findall(r'\[('+P+r'Get\w+)\]',node.value):
                require(token in defined,'Undefined scripted text: '+token)
    variables=set()
    for node in all_rows:
        if node.key in ('set_variable','add_to_variable','subtract_from_variable','set_temp_variable','add_to_temp_variable'):
            for child in node.children():
                if child.key.startswith(P):variables.add(child.key)
                if child.key=='var' and str(child.value).startswith(P):variables.add(child.value)
    getters=set()
    for key,value in loc.items():
        for token in re.findall(r'\[('+P+r'Get\w+)\]',value):
            require(token in defined,'Undefined scripted event text '+token+' in '+key)
        for variable in re.findall(r'\[\?(?:[A-Z]{3}\.)?('+P+r'\w+)(?:\||\])',value):
            getters.add(variable)
            require(variable in variables,'Undefined displayed variable '+variable+' in '+key)
    require(len(loc_rows)==len(loc),'Duplicate keys in owned localisation')
    require(loc_path.read_bytes().startswith(b'\xef\xbb\xbf'),'Localisation BOM missing')
    # The only owned provider may not be shadowed by another English file.
    duplicates=[]
    pattern=re.compile(r'^\s*'+P+r'[^\s:]+:\d*\s+"',re.M)
    for path in loc_path.parent.glob('*.yml'):
        if path!=loc_path and pattern.search(path.read_text(encoding='utf-8-sig',errors='replace')):
            duplicates.append(str(path.relative_to(ROOT)))
    require(not duplicates,'Namespace shadowed by other English providers: '+', '.join(duplicates))
    report=dict(project='IMPERIA COLD WAR',scope='Regional decisions, country events, scripted status and dynamic-variable localisation closure',
      status='PASS' if not findings else 'FAIL',implicit_name_description_references=implicit,event_text_references=event_references,
      localisation_keys=len(loc),displayed_variables=sorted(getters),scripted_status_providers=sorted(defined),findings=findings,
      source_sha256={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [*paths,loc_path,Path(__file__)]},
      limits='Reference and scope checks, not live text rendering or multiplayer evidence.')
    output=ROOT/'docs/design/usa_kissinger_20261028/LOCALISATION_CONTROL_VALIDATION.json'
    output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:value for key,value in report.items() if key not in ('source_sha256','displayed_variables','scripted_status_providers')},indent=2))
    if findings:raise SystemExit(1)


if __name__=='__main__':main()
