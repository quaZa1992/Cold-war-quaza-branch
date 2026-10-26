# IMPERIA CW — Cold War: iraq 1970 — render installed.
"""Read-only render of installed IRQ and complete USA national focus trees.

Uses emitted coordinates, actual registered textures, native titlebar and
hoi_16mbs glyph atlas. All images are static approximations of locked cards;
orthogonal connectors approximate engine routing. No runtime file is written.
"""
from pathlib import Path
from functools import lru_cache
import hashlib
import json
import re
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
MD=Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
sys.path.insert(0,str(ROOT/'tools/iraq_1970_concept'))
from script_ast import parse,first,values
from native_font import raster,width
sys.path.insert(0,str(ROOT/'tools/iraq_1970'))
from audit_design import load_design

OUT=ROOT/'docs/design/iraq_1970/implementation'
REPORT={'scope':'Actual installed coordinates/cards/glyphs/art; static unavailable state. Connector routing approximates HOI4. No engine test.','sources':{},'trees':{},'renders':{}}
SPRITES={}
for base in [GAME,MD,ROOT]:
    for path in sorted((base/'interface').glob('*.gfx')):
        text=path.read_text(encoding='utf-8-sig',errors='replace')
        for m in re.finditer(r'\b(?:spriteType|SpriteType)\s*=\s*\{\s*name\s*=\s*"([^"\n]+)"\s+texture[Ff]ile\s*=\s*"([^"\n]+)"',text):
            SPRITES[m[1]]=(m[2].replace('\\','/'),str(path))
LOC={}
for base in [GAME,MD,ROOT]:
    for path in sorted((base/'localisation/english').glob('*.yml')):
        for m in re.finditer(r'^\s*([^\s:#]+):\d*\s+"(.*)"\s*(?:#.*)?$',path.read_text(encoding='utf-8-sig',errors='replace'),re.M):
            LOC[m[1]]=m[2].replace('\\"','"')


def source_hash(path):return hashlib.sha256(path.read_bytes()).hexdigest()


@lru_cache(maxsize=None)
def icon(name):
    assert name in SPRITES,('Unregistered installed sprite',name)
    rel,definition=SPRITES[name]
    path=next((base/rel for base in [ROOT,MD,GAME] if (base/rel).exists()),None)
    assert path,('Missing installed texture',name,rel)
    return Image.open(path).convert('RGBA')


def title(key):
    result=LOC.get(key,key)
    for _ in range(5):
        expanded=re.sub(r'\$([^$]+)\$',lambda m:LOC.get(m[1],m[0]),result)
        if expanded==result:break
        result=expanded
    return re.sub(r'§.','',result)


def read_tree(relative):
    path=ROOT/relative
    tree=first(parse(path.read_text(encoding='utf-8-sig')),'focus_tree')
    nodes={}
    for n in values(tree,'focus'):
        if first(first(n,'allow_branch',[]),'always')=='no':continue
        key=first(n,'id')
        assert key not in nodes,('Duplicate installed focus',key)
        nodes[key]={'id':key,'title':title(key),'icon':first(n,'icon'),'raw':[float(first(n,'x',0)),float(first(n,'y',0))],
                    'anchor':first(n,'relative_position_id'),'prerequisites':[[p for k,_,p in group if k=='focus'] for group in values(n,'prerequisite')],
                    'excludes':[p for group in values(n,'mutually_exclusive') for k,_,p in group if k=='focus'],
                    'offsets':len(values(n,'offset'))}
    def resolve(key,seen=()):
        assert key not in seen,('Anchor cycle',seen,key)
        n=nodes[key]
        if 'xy' not in n:
            x,y=n['raw']
            if n['anchor']:
                assert n['anchor'] in nodes,('Missing anchor',key,n['anchor'])
                ax,ay=resolve(n['anchor'],seen+(key,));x+=ax;y+=ay
            n['xy']=[x,y]
        return n['xy']
    for key in nodes:
        resolve(key)
        for group in nodes[key]['prerequisites']:
            for p in group:assert p in nodes,('Missing parent',key,p)
        icon(nodes[key]['icon'])
    tid=first(tree,'id')
    REPORT['sources'][relative]=source_hash(path)
    REPORT['trees'][tid]={'focuses':len(nodes),'bounds':[min(n['xy'][0] for n in nodes.values()),min(n['xy'][1] for n in nodes.values()),max(n['xy'][0] for n in nodes.values()),max(n['xy'][1] for n in nodes.values())],
       'conditional_offsets':sum(n['offsets'] for n in nodes.values()),'title_overflow':[{'id':n['id'],'title':n['title'],'native_width':width(n['title'])} for n in nodes.values() if width(n['title'])>147],
       'nodes':[{k:v for k,v in n.items() if k not in ('raw','offsets')} for n in nodes.values()]}
    return nodes


BAR=Image.open(GAME/'gfx/interface/focusview/titlebar/focus_unavailable_bg.dds').convert('RGBA')
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)


def render(name,nodes,selected=None,bounds=None,overview=False):
    chosen=selected or set(nodes)
    ns=[nodes[key] for key in nodes if key in chosen]
    if bounds is None:
        left=min(n['xy'][0]*96 for n in ns)-35
        top=min(n['xy'][1]*130 for n in ns)-115
        right=max(n['xy'][0]*96 for n in ns)+205
        bottom=max(n['xy'][1]*130 for n in ns)+140
    else:left,top,right,bottom=bounds
    w,h=round(right-left),round(bottom-top)
    im=Image.new('RGBA',(w,h),'#22343c');draw=ImageDraw.Draw(im)
    # Native GUI's link begin/end offsets; orthogonal bends are approximate.
    for n in nodes.values():
        x,y=n['xy'][0]*96-left,n['xy'][1]*130-top
        for group in n['prerequisites']:
            for key in group:
                p=nodes[key];px,py=p['xy'][0]*96-left,p['xy'][1]*130-top
                if n['id'] not in chosen and key not in chosen:continue
                mid=(py+64+y)//2
                draw.line([(px+80,py+64),(px+80,mid),(x+80,mid),(x+80,y)],fill='#a2b2b5',width=2)
        for key in n['excludes']:
            if key<n['id'] or key not in nodes:continue
            q=nodes[key];qx,qy=q['xy'][0]*96-left,q['xy'][1]*130-top
            a,b=min(x,qx)+172,max(x,qx)+12
            for xx in range(round(a),round(b),9):draw.line([(xx,y+24),(min(xx+4,b),y+24)],fill='#d9a287',width=2)
    for n in nodes.values():
        x,y=round(n['xy'][0]*96-left),round(n['xy'][1]*130-top)
        asset=icon(n['icon'])
        if x+180<0 or x>w or y+125<0 or y-asset.height>h:continue
        im.alpha_composite(asset,(round(x+87.5-asset.width/2),round(y+20-asset.height/2)))
        im.alpha_composite(BAR,(x+5,y+40));im.alpha_composite(raster(n['title']),(x+15,y+58))
    draw.rectangle((0,0,min(w,1450),75),fill='#192a32')
    draw.text((20,12),name.replace('_',' ')+' | INSTALLED SOURCE',font=FONT,fill='#e3cf90')
    draw.text((20,36),'Native 96 x 130 grid | Installed art, cards and bitmap font',font=FONT,fill='#c4cdcb')
    draw.text((20,56),'Static locked state | Approximate links | No engine test',font=FONT,fill='#c4cdcb')
    native_size=im.size
    if overview and w>2600:
        im.thumbnail((2600,10000),Image.Resampling.LANCZOS)
    destination=OUT/(name+'.png');im.convert('RGB').save(destination)
    REPORT['renders'][destination.name]={'native_canvas':native_size,'export_size':im.size,'selected':len(ns),'all_nodes_drawn_if_in_bounds':True,'bounds_pixels':[left,top,right,bottom]}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    irq=read_tree('common/national_focus/COLDWAR_IRQ_1970_focus.txt')
    usa=read_tree('common/national_focus/USA_1970.txt')
    approved=load_design()
    expected={n['id']:n for n in approved['nodes'] if not n.get('audit_retired')}
    assert set(irq)==set(expected)
    for key,n in irq.items():
        a=expected[key]
        assert n['xy']==a['xy'],('Installed coordinate drift',key,n['xy'],a['xy'])
        assert n['prerequisites']==a['prerequisites'],('Prerequisite drift',key)
        assert n['excludes']==a['mutually_exclusive'],('Exclusion drift',key)
    staged=values(parse((ROOT/'tools/iraq_1970/staged/USA_GULF_FOCUS_FRAGMENT.txt').read_text(encoding='utf-8-sig')),'focus')
    gulf_ids=set()
    for a in staged:
        if first(first(a,'allow_branch',[]),'always')=='no':continue
        fid=first(a,'id');gulf_ids.add(fid);n=usa[fid]
        assert n['xy']==[float(first(a,'x'))+30,float(first(a,'y'))],('USA translation drift',fid)
        assert n['prerequisites']==[values(g,'focus') for g in values(a,'prerequisite')]
    render('IRQ_FULL_OVERVIEW',irq,overview=True)
    render('USA_FULL_OVERVIEW',usa,overview=True)
    for group in ['state','baath','bakr','saddam','communists','kurds','puk','oil','industry','defence','war','iran_war']:
        chosen={n['id'] for n in approved['nodes'] if n['group']==group and not n.get('audit_retired')}
        render('IRQ_NATIVE_'+group,irq,chosen)
    render('USA_NATIVE_GULF',usa,gulf_ids)
    render('USA_GULF_WITH_EXISTING_DEFENCE',usa,gulf_ids,bounds=(21*96,-115,40*96+205,12*130+140))
    REPORT['approved_irq_sha256']=source_hash(ROOT/'tools/iraq_1970/approved_iraq.json')
    REPORT['node_graph_parity']={'irq_active':len(irq),'irq_legacy_retired':len(approved['retired_focuses']),'usa_total_active':len(usa),'usa_gulf_active':len(gulf_ids),'usa_translation':[30,0]}
    (OUT/'INSTALLED_RENDER_REPORT.json').write_text(json.dumps(REPORT,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'renders':len(REPORT['renders']),'graph_parity':REPORT['node_graph_parity'],'overflow':{k:len(v['title_overflow']) for k,v in REPORT['trees'].items()},'out':str(OUT)},indent=2))


if __name__=='__main__':main()
