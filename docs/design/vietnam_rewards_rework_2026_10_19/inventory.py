"""Read-only installed Vietnam inventory and preview assets. Never rebuild game content."""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import sys,json,re,hashlib,base64,io,importlib.util
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
VIZ=Path('C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f32-41dc-74b3-baa1-8f6916e026ed')
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from runtime_design import load_design,load_campaign_design
from script_ast import parse,first,values,emit

def encoded(im,compact=False):
    out=io.BytesIO()
    if compact:im.convert('RGBA').save(out,format='WEBP',quality=90,method=6)
    else:im.convert('RGBA').save(out,format='PNG',optimize=True)
    return 'data:image/'+('webp' if compact else 'png')+';base64,'+base64.b64encode(out.getvalue()).decode('ascii')

def main():
    d,c=load_design(),load_campaign_design()
    definitions={n['id']:n for n in d['nodes']+c['nodes']}
    focus_path=ROOT/'common/national_focus/COLDWAR_VIE_1970_focus.txt'
    tree=first(parse(focus_path.read_text(encoding='utf-8-sig')),'focus_tree')
    actual={first(n,'id'):n for n in values(tree,'focus')}
    assert set(actual)==set(definitions) and len(actual)==307
    text=(ROOT/'localisation/english/COLDWAR_VIE_1970_l_english.yml').read_text(encoding='utf-8-sig')
    loc={k:json.loads(v) for k,v in re.findall(r'^ ([^ :]+):0 (".*")$',text,re.M)}
    gfx=first(parse((ROOT/'interface/COLDWAR_VIE_1970_goals.gfx').read_text(encoding='utf-8-sig')),'spriteTypes')
    sprites={first(n,'name').strip('"'):first(n,'texturefile').strip('"') for n in values(gfx,'spriteType')}
    @lru_cache(None)
    def xy(key):
        row=actual[key];x,y=float(first(row,'x')),float(first(row,'y'))
        anchor=first(row,'relative_position_id')
        if anchor:
            ax,ay=xy(anchor);x+=ax;y+=ay
        return x,y
    assets={};nodes=[]
    for key,row in actual.items():
        n=definitions[key];x,y=xy(key)
        assert (x,y)==(n['x'],n['y'])
        icon=first(row,'icon');texture=sprites[icon]
        if texture not in assets:assets[texture]=encoded(Image.open(ROOT/texture),compact=True)
        nodes.append(dict(id=key,label=loc[key],description=loc[key+'_desc'],group=n['group'],x=x,y=y,
            days=float(first(row,'cost'))*7,prerequisites=[[v for k,_,v in group if k=='focus'] for group in values(row,'prerequisite')],
            exclusive=[v for group in values(row,'mutually_exclusive') for k,_,v in group if k=='focus'],
            icon=texture,cash=n.get('cash',0),building=n.get('building'),relief=n.get('relief'),terrain=n.get('terrain_training'),
            modifiers=n.get('modifiers',{}),effects=n['effects'],lifecycle=n.get('lifecycle','timed_or_campaign'),
            availability=emit(first(row,'available',[])),reward=emit(first(first(row,'completion_reward'),'effect_tooltip',[]))))
    # This previously inspected renderer has only definitions at import; main/run own all writes.
    source=VIZ/'coldwar-vietnam-render.py'
    spec=importlib.util.spec_from_file_location('audit_native_label',source)
    native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
    font=native.NativeLabelFont()
    font_data=dict(atlas=encoded(font.atlas),chars=font.chars,kerns={f'{a},{b}':v for (a,b),v in font.kerns.items()})
    titlebar=native.asset('gfx/interface/focusview/titlebar/focus_unavailable_bg.dds')
    assets['titlebar']=encoded(Image.open(titlebar))
    groups=[dict(id=g['id'],label=g['label'].replace(' — ',': '),gate=g.get('gate',''),leader=g.get('leader')) for g in d['groups']+c['groups']]
    manifest=json.loads((ROOT/'tools/vietnam_1970/manifest.json').read_text(encoding='utf-8'))
    tracked=manifest['generated']+manifest['integration']+manifest['politics_sources']+manifest['politics_integration']
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in tracked}
    pairs={tuple(sorted((n['id'],other))) for n in nodes for other in n['exclusive']}
    report=dict(status='read-only installed source reconstruction; proposals are separate',date='2026-10-19',nodes=nodes,groups=groups,
        counts=dict(focuses=len(nodes),groups=len(groups),exclusive_pairs=len(pairs),duration_days=dict(Counter(int(n['days']) for n in nodes))),
        hashes=hashes,art=assets,font=font_data,geometry=dict(x_step=96,y_step=130),
        limits='Native art and bitmap labels. Connectors and camera are external approximations, not engine UI or an observed game state.')
    HERE.mkdir(parents=True,exist_ok=True)
    (HERE/'inventory.json').write_text(json.dumps(report,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    print(json.dumps(dict(nodes=len(nodes),groups=len(groups),pairs=len(pairs),assets=len(assets),bytes=(HERE/'inventory.json').stat().st_size)))

if __name__=='__main__':main()
