# IMPERIA COLD WAR — Native-asset previews of all five installed naval additions.
"""Reuse the installed donor renderer for bounded native country views."""
import importlib.util
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from naval_adaptation_1970 import naval_adapter as A

def main():
    spec=importlib.util.spec_from_file_location('naval_native_renderer',ROOT/'tools/iraq_1970/render_installed.py')
    R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)
    out=A.DOC/'installed';out.mkdir(parents=True,exist_ok=True);R.OUT=out
    overview=Image.new('RGB',(1800,1620),'#192a32');draw=ImageDraw.Draw(overview)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',23)
    asset_sources={}
    for i,(tag,p) in enumerate(A.profiles().items()):
        ns=R.read_tree(p['tree_file']);new={k for k in ns if k.startswith(A.PREFIX+tag+'_')}
        xs=[ns[k]['xy'][0] for k in new];ys=[ns[k]['xy'][1] for k in new]
        left=min(xs)-3;right=max(xs)+3;top=min(ys)-5;bottom=max(ys)+2
        for n in ns.values():
            if not(left-2<=n['xy'][0]<=right+2 and top-2<=n['xy'][1]<=bottom+2):continue
            sprite=n['icon']
            if sprite in asset_sources:continue
            relative,definition=R.SPRITES[sprite]
            texture=next(base/relative for base in (ROOT,R.MD,R.GAME) if (base/relative).exists())
            asset_sources[sprite]=dict(texture=str(texture),definition=definition,texture_sha256=hashlib.sha256(texture.read_bytes()).hexdigest(),definition_sha256=hashlib.sha256(Path(definition).read_bytes()).hexdigest(),modifications='None; rendered unchanged for local review',individual_author='Unknown',separate_permission='Unknown')
        R.render(tag+'_NAVAL_WITH_NEIGHBOURS',ns,new,bounds=(left*96-35,top*130-115,right*96+205,bottom*130+140))
        R.render(tag+'_NAVAL',ns,new)
        image=Image.open(out/(tag+'_NAVAL.png'));image.thumbnail((865,455),Image.Resampling.LANCZOS)
        x=(i%2)*900+15;y=(i//2)*530+60
        overview.paste(image,(x,y));draw.text((x,y-30),tag+' : '+str(len(new))+' naval focuses',font=font,fill='#e3cf90')
    draw.text((915,1150),'Installed native assets and bitmap titles',font=font,fill='#e3cf90')
    draw.text((915,1190),'Static source composition. No live game test.',font=font,fill='#c4cdcb')
    overview.save(out/'FIVE_COUNTRY_NAVAL_OVERVIEW.png')
    font_source=R.raster.__wrapped__.__globals__
    common_sources=[R.GAME/'gfx/interface/focusview/titlebar/focus_unavailable_bg.dds',font_source['FONT'],font_source['ATLAS'],Path('C:/Windows/Fonts/arial.ttf')]
    common_assets={str(p):dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),modifications='Source unchanged; glyphs/frame rendered into local review composition',individual_author='Unknown',separate_permission='Unknown') for p in common_sources}
    R.REPORT.update(project='IMPERIA COLD WAR',asset_sources=asset_sources,common_assets=common_assets,credits='Existing Millennium Dawn, HOI4 and IMPERIA COLD WAR contributors. Microsoft Arial supplies review annotations. Individual texture/font authors and separate redistribution permission unknown; unchanged existing assets composed for local review.',modifications='No source asset edits. Native source reconstruction at 96x130 grid; combined contact sheet downsampled.')
    (out/'LAYOUT_EVIDENCE.json').write_text(json.dumps(R.REPORT,indent=2)+'\n',encoding='utf-8')
    (out/'NOTICE.md').write_text('IMPERIA COLD WAR\n\nLocal installed-source previews using unchanged existing Millennium Dawn, HOI4 and project art and bitmap fonts. Original individual authors and separate redistribution permission are unknown. Native card composition and approximate connectors; no live screenshot. Provenance and hashes: LAYOUT_EVIDENCE.json.\n',encoding='utf-8')
    print(json.dumps(dict(project='IMPERIA COLD WAR',renders=len(R.REPORT['renders'])+1,out=str(out))))

if __name__=='__main__':main()
