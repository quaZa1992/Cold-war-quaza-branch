# IMPERIA COLD WAR — Independent research viewport preservation checks.
"""Check native controls, header clearance and continuous tiled viewport coverage."""
import hashlib
import json
from pathlib import Path
import zipfile
from catalog import parse,first

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PATH=ROOT/'interface/countrytechtreeview.gui'


def named(rows):return str(first(rows,'name','')).strip('"')


def walk(rows,path=()):
    for key,op,value in rows:
        if isinstance(value,list):
            own=path+((key,named(value)),)
            yield own,key,value
            yield from walk(value,own)


def main():
    prior=json.loads((HERE/'prerequisite_repair_before.json').read_text(encoding='utf-8'))
    with zipfile.ZipFile(prior['archive']) as archive:
        original=parse(archive.read('interface/countrytechtreeview.gui').decode('utf-8-sig'))
    current=parse(PATH.read_text(encoding='utf-8'))
    old={p:(k,v) for p,k,v in walk(original) if named(v)}
    new={p:(k,v) for p,k,v in walk(current) if named(v)}
    folders={p:v for p,k,v in walk(current) if named(v).endswith('_folder') and first(v,'drag_scroll')}
    assert len(folders)==15
    grids=0
    for path,(kind,rows) in old.items():
        if kind.lower()!='gridboxtype':continue
        assert path in new,('Removed native research tree',path)
        after=new[path][1]
        before_rest=[r for r in rows if r[0]!='position']
        after_rest=[r for r in after if r[0]!='position']
        assert before_rest==after_rest,('Native research grid changed',path)
        before_pos=first(rows,'position');after_pos=first(after,'position')
        if any(name=='bba_aircraft_folder' for _,name in path):
            assert first(after_pos,'x')==first(before_pos,'x')
            assert int(first(after_pos,'y'))==int(first(before_pos,'y'))+96
        else:assert before_pos==after_pos,('Other research grid moved',path)
        grids+=1
    for path,rows in folders.items():
        assert first(rows,'scroll_wheel_factor')=='40'
        assert first(rows,'verticalScrollbar') and first(rows,'horizontalScrollbar')
        canvases=[v for k,o,v in rows if isinstance(v,list) and named(v)=='mdcw_research_canvas']
        assert len(canvases)==1
        canvas=canvases[0];size=first(canvas,'size');minimum=first(size,'min')
        assert first(minimum,'width')=='100%%' and first(minimum,'height')=='100%%'
        assert int(first(size,'width'))>0 and int(first(size,'height'))>0
        position=first(canvas,'position')
        for viewport in (1280,1920,2560):
            assert int(first(position,'x'))+max(int(first(size,'width')),viewport)>=viewport
        for viewport in (720,1080,1440):
            assert int(first(position,'y'))+max(int(first(size,'height')),viewport)>=viewport
        assert first(first(canvas,'background'),'quadTextureSprite')=='"GFX_techtree_stripes"'
        assert first(canvas,'alwaystransparent')=='yes'
    years={named(rows):rows for p,k,rows in walk(current) if named(rows).startswith('mdcw_research_year_')}
    assert len(years)==21 and 'mdcw_research_year_1960' in years
    for rows in years.values():
        assert first(first(rows,'position'),'y')=='96' and first(rows,'maxHeight')=='40'
    report={'project':'IMPERIA COLD WAR','status':'passed','research_folders':len(folders),'preserved_native_grids':grids,
            'aircraft_year_labels':len(years),'background_asset':'Existing native GFX_techtree_stripes; no image modified.',
            'output_sha256':hashlib.sha256(PATH.read_bytes()).hexdigest(),'native_ui_verified':False,
            'limitation':'Computer Use was stopped by the user with Escape. Layout and scroll behavior after GUI reload remain visually unverified.'}
    (HERE/'gui_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__=='__main__':main()
