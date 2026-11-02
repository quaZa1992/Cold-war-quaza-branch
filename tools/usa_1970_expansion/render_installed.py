# IMPERIA COLD WAR — USA installed-output layout evidence.
"""Render actual loaded coordinates, native art/titlebars and bitmap glyphs.

The shared renderer is imported without running its Iraq compiler or main.
All output is confined to this USA implementation's evidence directory.
"""
from pathlib import Path
import hashlib
import importlib.util
import json

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/design/usa_1970_expansion_20261024/installed'

def main():
    spec=importlib.util.spec_from_file_location('usa_installed_native_renderer',ROOT/'tools/iraq_1970/render_installed.py')
    render=importlib.util.module_from_spec(spec);spec.loader.exec_module(render)
    OUT.mkdir(parents=True,exist_ok=True);render.OUT=OUT
    nodes=render.read_tree('common/national_focus/USA_1970.txt')
    assert len(nodes)==300  # 301 registered IDs; the obsolete contact receipt stays hidden.
    widths={key:render.width(n['title']) for key,n in nodes.items()}
    assert max(widths.values())<=147,[(k,w) for k,w in widths.items() if w>147]
    render.render('USA_FULL_INSTALLED',nodes,overview=True)
    views={
        'USA_ENERGY_INDUSTRY':(-35,-18,-1,13),
        'USA_DEFENCE':(19,28,-1,15),
        'USA_FOREIGN':(9,21,1,18),
        'USA_1972_PRIORITIES':(-17,17,12,20),
        'USA_1980_PRIORITIES':(-17,17,26,36),
        'USA_GULF':(29,39,-1,8),
        'USA_NAVAL':(18,34,10,23)
    }
    for name,(left,right,top,bottom) in views.items():
        chosen={k for k,n in nodes.items() if left<=n['xy'][0]<=right and top<=n['xy'][1]<=bottom}
        render.render(name,nodes,selected=chosen,bounds=(left*96-35,top*130-115,right*96+205,bottom*130+140))
    report=dict(project='IMPERIA COLD WAR',scope='Actual installed source reconstruction: 301 registered IDs, 300 visible cards. Registered MD/HOI4 textures, native 96x130 grid, 165x128 containers and 147x20 bitmap titles. Locked-state treatment and connectors approximate the engine; these are not live screenshots.',source_sha256=hashlib.sha256((ROOT/'common/national_focus/USA_1970.txt').read_bytes()).hexdigest(),focuses=301,visible_focuses=len(nodes),hidden_legacy_ids=['COLDWAR_USA_gulf_contacts'],maximum_title_width=max(widths.values()),continuous_focus=dict(x=-3200,y=1800,width=770,height=380,placement='Clear lower-left space below energy programmes; no focus footprint overlaps.'),title_widths=widths,renders=render.REPORT['renders'],sources=render.REPORT['sources'],credits='Existing Millennium Dawn and HOI4 contributors; IMPERIA COLD WAR project authors. Native rendering helper by existing project tools.',licence_or_permission='Local project review; separate third-party redistribution permission unknown.',modifications='Source assets unchanged. Bitmap icons/titlebar/glyphs composed at native scale; only whole-tree overview is downsampled.')
    (OUT/'layout_evidence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    (OUT/'NOTICE.md').write_text('IMPERIA COLD WAR\n\nInstalled USA focus-tree source previews. These are native-asset composites, not live game screenshots. Source textures and bitmap glyphs belong to their existing HOI4, Millennium Dawn and project authors. Separate redistribution permission is unknown. Full provenance, source hashes and preview transformations are recorded in layout_evidence.json.\n',encoding='utf-8')
    print(json.dumps(dict(focuses=301,views=len(views)+1,maximum_title_width=max(widths.values()),source_sha256=report['source_sha256'])))

if __name__=='__main__':main()
