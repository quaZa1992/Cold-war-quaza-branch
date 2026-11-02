# IMPERIA COLD WAR — Bounded live-source closure audit for quaZa East Asia integration.
import ast
import hashlib
import json
import re
import sys
import struct
from collections import defaultdict
from pathlib import Path
from source import ROOT,REPORT

sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,walk,first,values


def main():
    errors=[];notes=[]
    def check(ok,message):
        if not ok:errors.append(message)
    imported=json.loads((REPORT/'INITIAL_IMPORT.json').read_text(encoding='utf-8'))['files']
    integrated=json.loads((REPORT/'INTEGRATION.json').read_text(encoding='utf-8'))['installed']
    paths={p for p in set(imported)|set(integrated) if p.startswith(('common/','events/','interface/','localisation/english/'))}
    paths.update(p.relative_to(ROOT).as_posix() for folder in ('common','events','interface','localisation/english') for p in (ROOT/folder).rglob('COLDWAR_NKO_1970_succession*'))
    scripts={};local_keys=set();callbacks=set();sprites={};custom=set();readers=defaultdict(set)
    for folder in ('scripted_effects','scripted_triggers'):
        for p in (ROOT/'common'/folder).glob('*.txt'):
            callbacks.update(re.findall(r'(?m)^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{',p.read_text(encoding='utf-8-sig',errors='replace')))
    for p in (ROOT/'localisation/english').rglob('*.yml'):
        local_keys.update(re.findall(r'(?m)^\s*([^\s:#]+):',p.read_text(encoding='utf-8-sig',errors='replace')))
    for p in (ROOT/'common/modifier_definitions').glob('*.txt'):
        custom.update(k for k,o,v in parse(p.read_text(encoding='utf-8-sig')))
    for p in (ROOT/'common/scripted_effects').glob('*.txt'):
        text=p.read_text(encoding='utf-8-sig',errors='replace')
        for key in set(re.findall(r'\bmodifier@([A-Za-z0-9_]+)',text)):readers[key].add(p.relative_to(ROOT).as_posix())
    native=(Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV/documentation/modifiers_documentation.md')).read_text(encoding='utf-8')
    native_keys=set(re.findall(r'(?m)^\* \[([A-Za-z0-9_]+)\]',native))
    for p in (ROOT/'common/units/unit_modifiers').glob('*.txt'):
        native_keys.update(v for k,o,v in walk(parse(p.read_text(encoding='utf-8-sig'))) if k=='_bare' and isinstance(v,str))
    buildings={k for k,o,v in first(parse((ROOT/'common/buildings/00_buildings.txt').read_text(encoding='utf-8')),'buildings',[])}
    for p in (ROOT/'interface').glob('*.gfx'):
        text=p.read_text(encoding='utf-8-sig',errors='replace')
        for name,texture in re.findall(r'name\s*=\s*"([^"\n]+)"\s*\n?\s*texturefile\s*=\s*"([^"\n]+)"',text):sprites[name]=texture
    modifier_usage=defaultdict(set)
    for relative in sorted(paths):
        p=ROOT/relative;check(p.exists(),'Missing live file: '+relative)
        if not p.exists():continue
        raw=p.read_bytes();text=raw.decode('utf-8-sig')
        if p.suffix=='.yml':
            check(raw.startswith(b'\xef\xbb\xbf'),'Localisation BOM: '+relative)
            check(text.replace('\r\n','\n').startswith('l_english:\n# IMPERIA COLD WAR — '),'Localisation header: '+relative)
            check('\ufffd' not in text,'Corrupt replacement character: '+relative)
            check(not any('\u2013' in line or '\u2014' in line for line in text.splitlines() if not line.lstrip().startswith('#')),'Player-text dash: '+relative)
            continue
        check(not raw.startswith(b'\xef\xbb\xbf'),'Script BOM: '+relative)
        check(text.startswith('# IMPERIA COLD WAR — '),'Missing file-start marker: '+relative)
        try:rows=parse(text);scripts[relative]=rows
        except ValueError as e:errors.append(relative+': '+str(e));continue
        for k,o,v in walk(rows):
            if k.startswith(('COLDWAR_NKO_','COLDWAR_KOR_','COLDWAR_JAP','COLDWAR_nr_')) and v in ('yes','no'):
                check(k in callbacks,'Missing scripted callback: '+k+' in '+relative)
            if k in {'tooltip','custom_effect_tooltip','unlock_decision_tooltip','localization_key'} and isinstance(v,str) and v.startswith('COLDWAR_'):
                check(v in local_keys,'Missing visible text: '+v+' in '+relative)
        if '/dynamic_modifiers/' in relative:
            for name,o,body in rows:
                for key,o,val in body:
                    if key in {'icon','enable','remove_trigger','allowed','show_only_in_tooltip'}:continue
                    modifier_usage[key].add(relative)
        if '/ideas/' in relative:
            for name,o,body in first(first(rows,'ideas',[]),'country',[]):
                for key,o,val in first(body,'modifier',[]):modifier_usage[key].add(relative)
    for key,files in modifier_usage.items():
        dynamic_building=key.startswith('production_speed_') and key.endswith('_factor') and key[len('production_speed_'):-len('_factor')] in buildings
        check(key in native_keys or key in custom or dynamic_building,'Unknown modifier key '+key+' in '+', '.join(files))
        if key in custom and not readers[key]:notes.append('Custom modifier has no direct modifier@ reader in scripted_effects: '+key)
    trees={}
    for tag,count in (('NKO',360),('KOR',300),('JAP',425)):
        relative='common/national_focus/COLDWAR_'+tag+'_1970_focus.txt'
        tree=first(scripts.get(relative,[]),'focus_tree',[]);foci=values(tree,'focus');by={first(f,'id'):f for f in foci}
        check(len(foci)==len(by)==count,'Focus count or duplicate IDs: '+tag)
        resolved={}
        def position(identifier,trail=()):
            if identifier in resolved:return resolved[identifier]
            check(identifier not in trail,'Relative anchor cycle: '+identifier)
            if identifier in trail:return (0,0)
            f=by[identifier];x=float(first(f,'x'));y=float(first(f,'y'));anchor=first(f,'relative_position_id')
            if anchor:
                check(anchor in by,'Missing anchor '+anchor)
                if anchor in by:ax,ay=position(anchor,trail+(identifier,));x+=ax;y+=ay
            resolved[identifier]=(x,y);return x,y
        declared=set()
        for identifier,f in by.items():
            position(identifier)
            anchor=first(f,'relative_position_id')
            check(not anchor or anchor in declared,'Forward relative anchor: '+identifier+' -> '+str(anchor))
            declared.add(identifier)
            check(first(f,'allow_branch') is None,'Hidden branch: '+identifier)
            check(identifier in local_keys and identifier+'_desc' in local_keys,'Missing focus name/description: '+identifier)
            for group in values(f,'prerequisite'):
                for pre in values(group,'focus'):check(pre in by,'Missing prerequisite: '+identifier+' -> '+pre)
            for other in values(first(f,'mutually_exclusive',[]),'focus'):
                check(other in by and identifier in values(first(by.get(other,[]),'mutually_exclusive',[]),'focus'),'Non-reciprocal exclusion: '+identifier+' -> '+other)
        check(len(set(resolved.values()))==len(resolved),'Duplicate absolute focus positions: '+tag)
        trees[tag]={'focuses':len(foci),'exclusive_focuses':sum(bool(first(f,'mutually_exclusive')) for f in foci),'bounds':{'x':[min(x for x,y in resolved.values()),max(x for x,y in resolved.values())],'y':[min(y for x,y in resolved.values()),max(y for x,y in resolved.values())]}}
    for relative,rows in scripts.items():
        if '/decisions/categories/' in relative:
            for key,op,body in rows:
                if key.startswith(('COLDWAR_NKO','COLDWAR_KOR','COLDWAR_JAP','COLDWAR_nuclear')):
                    check(isinstance(body,list),'Invalid category body: '+key)
                    check(key in local_keys,'Missing decision category text: '+key)
        elif relative.startswith('common/decisions/'):
            for key,op,body in rows:
                check(isinstance(body,list) and not any(k in {'icon','allowed','visible'} for k,o,v in body),'Category metadata in decision container: '+key)
    # Pillow's DX10 typeless export can decode locally yet fail in HOI4.
    for relative,size in [('gfx/Leaders/NKO/NKO_Coldwar_Kim_Il_Sung.dds',(156,210)),('gfx/Leaders/NKO/COLDWAR_NKO_Kim_Il_Sung_memorial.dds',(156,210)),('gfx/event_pictures/COLDWAR_NKO_1994_funeral.dds',(410,164))]:
        raw=(ROOT/relative).read_bytes()
        w,h=size
        check(raw[:4]==b'DDS ' and raw[84:88]==b'DXT5','Native DDS format: '+relative)
        check(struct.unpack_from('<III',raw,12)==(h,w,((w+3)//4)*((h+3)//4)*16),'Native DDS dimensions/linear size: '+relative)
        check(struct.unpack_from('<I',raw,28)[0]==1 and len(raw)==128+((w+3)//4)*((h+3)//4)*16,'Native DDS mip/payload: '+relative)
    report={'project':'IMPERIA COLD WAR','errors':errors,'notes':sorted(set(notes)),'trees':trees,'live_files':len(paths),'modifier_keys':len(modifier_usage),'custom_modifier_readers':{k:sorted(readers[k]) for k in sorted(modifier_usage) if k in custom},'scope':'Bounded emitted-source syntax, reference, native/custom key registration, visible text, encoding and graph checks. Direct readers recorded separately from gameplay magnitude. Not native or MP proof.'}
    (REPORT/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'project':'IMPERIA COLD WAR','trees':trees,'errors':len(errors),'error_sample':errors[:30],'notes':sorted(set(notes)),'modifier_keys':len(modifier_usage)}))
    return bool(errors)


if __name__=='__main__':raise SystemExit(main())
