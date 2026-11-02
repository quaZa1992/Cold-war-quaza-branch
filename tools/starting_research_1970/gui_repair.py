# IMPERIA COLD WAR — Research years, scrolling and continuous native backgrounds.
"""Patch research viewport controls while preserving native MD content and assets."""
import argparse
import hashlib
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PATH=ROOT/'interface/countrytechtreeview.gui'
BASELINE=HERE/'gui_repair_inputs.json'
MARK='# IMPERIA COLD WAR — Research years, scrolling and continuous native backgrounds.'
BEGIN='# IMPERIA COLD WAR research viewport BEGIN'
END='# IMPERIA COLD WAR research viewport END'
TOKEN=re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}=]|[^\s{}=#"]+')


def nodes(source):
    tokens=[m for m in TOKEN.finditer(source) if not m[0].startswith('#')]
    def read(i,stop=False):
        result=[]
        while i<len(tokens):
            if tokens[i][0]=='}':return result,i+1
            key=tokens[i];i+=1
            if i>=len(tokens) or tokens[i][0]!='=':continue
            i+=1
            if i>=len(tokens):break
            value=tokens[i];i+=1;children=[]
            if value[0]=='{':
                children,i=read(i,True);end=tokens[i-1].end()
            else:end=value.end()
            result.append({'key':key[0],'value':value[0].strip('"'),'start':key.start(),'end':end,'vstart':value.start(),'children':children})
        return result,i
    return read(0)[0]


def field(node,key):
    return next((n for n in node['children'] if n['key'].lower()==key.lower()),None)


def named(node):
    n=field(node,'name');return n['value'] if n else ''


def walk(items):
    for item in items:
        yield item
        yield from walk(item['children'])


def replace(source,edits):
    for start,end,value in sorted(edits,reverse=True):source=source[:start]+value+source[end:]
    return source


def value(node,key,default=0):
    n=field(node,key)
    try:return int(n['value']) if n else default
    except ValueError:return default


def capture(source):
    folders={};bba={}
    for n in walk(nodes(source)):
        name=named(n)
        if n['key'].lower()!='containerwindowtype' or not name.endswith('_folder') or not field(n,'drag_scroll'):continue
        stripes=next((x for x in n['children'] if named(x)=='techtree_stripes'),None)
        pos=field(stripes,'position') if stripes else None
        size=field(stripes,'size') if stripes else None
        folders[name]={'x':value(pos,'x') if pos else 0,'y':value(pos,'y') if pos else 0,
                       'width':value(size,'width',2600) if size else 2600,'height':value(size,'height',1600) if size else 1600}
        if name=='bba_aircraft_folder':
            for child in n['children']:
                p=field(child,'position')
                if p and child['key'].lower() in ('instanttextboxtype','gridboxtype'):
                    bba[named(child)]=value(p,'y')
    return {'project':'IMPERIA COLD WAR','source_sha256':hashlib.sha256(source.encode()).hexdigest(),'folders':folders,'bba_original_y':bba}


def output(source,baseline):
    # Remove only this generator's inserted blocks before rebuilding them.
    source=re.sub(r'(?m)^[ \t]*'+re.escape(BEGIN)+r'\n.*?^[ \t]*'+re.escape(END)+r'\n','',source,flags=re.S)
    edits=[];report={}
    for folder in walk(nodes(source)):
        name=named(folder)
        if name not in baseline['folders'] or folder['key'].lower()!='containerwindowtype':continue
        original=baseline['folders'][name]
        x,y=original['x'],original['y']
        width=original['width']+abs(min(x,0))+320
        height=original['height']+abs(min(y,0))+192
        if name=='bba_aircraft_folder':width,height=3480,2480
        wheel=field(folder,'scroll_wheel_factor')
        if wheel:edits.append((wheel['vstart'],wheel['end'],'40'))
        else:
            anchor=field(folder,'horizontalScrollbar')
            edits.append((anchor['end'],anchor['end'],'\n\t\t\tscroll_wheel_factor = 40 # IMPERIA COLD WAR: native research scrolling.'))
        # A single continuous native tile removes the old finite stripe edge.
        # The old stripe container keeps its dimensions: right-anchored year
        # captions and existing technology geometry must not move with it.
        for child in folder['children']:
            if named(child)=='techtree_stripes':
                bg=field(child,'background')
                if bg and any(n['value']=='GFX_techtree_stripes' for n in bg['children']):edits.append((bg['start'],bg['end'],'# IMPERIA COLD WAR: continuous canvas supplies the native stripes.'))
        frame=field(folder,'background')
        assert frame,name
        canvas=f'''\n\t\t\t{BEGIN}
\t\t\tcontainerWindowType = {{
\t\t\t\tname = "mdcw_research_canvas"
\t\t\t\tposition = {{ x = {x} y = {y} }}
\t\t\t\tsize = {{ width = {width} height = {height} min = {{ width = 100%% height = 100%% }} }}
\t\t\t\talwaystransparent = yes
\t\t\t\tbackground = {{ name = "Background" quadTextureSprite = "GFX_techtree_stripes" }}
\t\t\t}}
\t\t\t{END}\n'''
        edits.append((frame['end'],frame['end'],canvas))
        for child in walk(folder['children']):
            if child['key'].lower()=='icontype':
                sprite=field(child,'spriteType')
                if sprite and (sprite['value'].endswith('_bg') or 'tech_tree_bg' in sprite['value']):
                    transparent=field(child,'alwaystransparent')
                    if transparent:edits.append((transparent['vstart'],transparent['end'],'yes'))
                    else:edits.append((child['end']-1,child['end']-1,'\n\t\t\t\talwaystransparent = yes\n\t\t\t'))
        if name=='bba_aircraft_folder':
            for child in folder['children']:
                child_name=named(child)
                if child['key'].lower()=='instanttextboxtype' and (child_name.startswith('airtech_year') or child_name.startswith('mdcw_airtech_year_')):
                    edits.append((child['start'],child['end'],''));continue
                if child_name in baseline['bba_original_y']:
                    position=field(child,'position');fy=field(position,'y')
                    edits.append((fy['vstart'],fy['end'],str(baseline['bba_original_y'][child_name]+96)))
            # Match the actual BBA year axis: 1945/50/55 are three slots apart,
            # then five calendar years correspond to two native 70px slots.
            labels=[]
            for year in range(1945,2050,5):
                slot={1945:-7,1950:-4,1955:-1}.get(year,2+(year-1960)*2/5)
                left=int(570+70*slot-50)
                labels.append(f'\t\t\tinstantTextBoxType = {{ name = "mdcw_research_year_{year}" position = {{ x = {left} y = 96 }} font = "hoi_36header" borderSize = {{ x = 0 y = 0 }} text = "{year}" maxWidth = 100 maxHeight = 40 format = center Orientation = "UPPER_LEFT" }}')
            edits.append((folder['end']-1,folder['end']-1,'\n\t\t\t'+BEGIN+'\n'+'\n'.join(labels)+'\n\t\t\t'+END+'\n\t\t'))
        report[name]={'canvas':[x,y,width,height],'wheel':40,'header_offset':96 if name=='bba_aircraft_folder' else 0}
    source=replace(source,edits)
    block_pattern=re.compile(r'[ \t\r\n]*'+re.escape(BEGIN)+r'\n(.*?)^[ \t]*'+re.escape(END)+r'[ \t\r\n]*',re.M|re.S)
    def canonical(match):
        following=source[match.end():match.end()+1]
        indent='\t\t' if following=='}' else '\t\t\t'
        return '\n\t\t\t'+BEGIN+'\n'+match[1].rstrip()+'\n\t\t\t'+END+'\n'+indent
    source=block_pattern.sub(canonical,source)
    if not source.startswith(MARK+'\n'):source=MARK+'\n'+source
    return source,report


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--apply',action='store_true');ap.add_argument('--check',action='store_true');args=ap.parse_args()
    source=PATH.read_text(encoding='utf-8-sig').replace('\r\n','\n')
    if not BASELINE.exists():BASELINE.write_text(json.dumps(capture(source),indent=2)+'\n',encoding='utf-8')
    result,folders=output(source,json.loads(BASELINE.read_text()))
    from catalog import parse
    parse(result)
    if args.apply:PATH.write_bytes(result.encode('utf-8'))
    if args.check:assert PATH.read_bytes()==result.encode('utf-8'),'Research GUI differs from generator'
    (HERE/'gui_repair_report.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','folders':folders,'output_sha256':hashlib.sha256(result.encode()).hexdigest(),'native_ui_verified':False},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'project':'IMPERIA COLD WAR','research_folders':len(folders),'mode':'apply' if args.apply else 'check' if args.check else 'preview'}))


if __name__=='__main__':main()
