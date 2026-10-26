"""Render the existing design in one MD-style coordinate space; no game edits."""
from pathlib import Path
from PIL import Image
import base64
import io
import json
import re
import html
import textwrap

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MD=Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
VANILLA=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
data=json.loads((HERE/'coldwar_cyprus_1970_design.json').read_text(encoding='utf-8'))
registry={}
for root in (MD,ROOT):
    text=(root/'interface/goals.gfx').read_text(encoding='utf-8-sig')
    registry.update(re.findall(r'name\s*=\s*"([^"]+)"\s*\n\s*texturefile\s*=\s*"([^"]+)"',text,re.I))

assets={}; provenance={}
def asset(name,path=None):
    rel=path or registry[name]
    source=next((r/rel for r in (ROOT,MD,VANILLA) if (r/rel).exists()),None)
    if not source: raise FileNotFoundError(rel)
    image=Image.open(source).convert('RGBA')
    output=io.BytesIO(); image.save(output,format='WEBP',lossless=True,method=6)
    assets[name]='data:image/webp;base64,'+base64.b64encode(output.getvalue()).decode()
    provenance[name]={'source':str(source),'width':image.width,'height':image.height}

for name in ['Election_graphics','Focus_Parliament_Constitution','army_reform','diplomacy',
             'industry','construction','money','education_reform','agriculture','united_nations',
             'maritime_trade','generic_housing','Generic_Conservatism','Generic_Liberalism',
             'social_democracy','communism','nam','fascism','shia_government','saudi_royalty',
             'Generic_Policeman','electricity','trade','labor_unions']:
    asset(name)
asset('nameplate','gfx/interface/focusview/titlebar/focus_unavailable_bg.dds')

party_icons={0:'Election_graphics',1:'Generic_Conservatism',2:'Generic_Liberalism',3:'social_democracy',
             4:'communism',5:'labor_unions',6:'industry',7:'army_reform',8:'shia_government',
             9:'shia_government',10:'saudi_royalty',11:'saudi_royalty',12:'nam',13:'Election_graphics',
             14:'Generic_Conservatism',15:'money',16:'Generic_Liberalism',17:'agriculture',
             18:'social_democracy',19:'communism',20:'fascism',21:'fascism',22:'army_reform',23:'saudi_royalty'}
def pick_icon(node):
    title=node['title'].lower()
    if node['party'] is not None: return party_icons[node['party']]
    for words,icon in [(['constitution','republic','rights'],'Focus_Parliament_Constitution'),
        (['police','reprisal','checkpoint'],'Generic_Policeman'),(['school','technical'],'education_reform'),
        (['credit','budget','accounts','capital'],'money'),(['port','coast','shipping'],'maritime_trade'),
        (['electricity','fuel'],'electricity'),(['rural','irrigation'],'agriculture'),
        (['housing','displaced','livelihood'],'generic_housing'),(['united nations','conference'],'united_nations'),
        (['construction','roads','works'],'construction'),(['trade'],'trade')]:
        if any(word in title for word in words): return icon
    return {'constitution':'Election_graphics','economy':'industry','military':'army_reform',
            'diplomacy':'diplomacy','aftermath':'generic_housing','turkish_cypriots':'Focus_Parliament_Constitution','road_to_war':'army_reform'}[node['section']]

# One global transform, no subtree rescaling or reflow. UI reference item is165x128.
# Grid pitch is an explicitly documented preview scale, not an engine constant claim.
PITCH_X=90;PITCH_Y=130;PAD_X=190;PAD_Y=200
for node in data['focuses']:
    node['preview_icon']=pick_icon(node)
    node['world_x']=PAD_X+node['x']*PITCH_X
    node['world_y']=PAD_Y+node['y']*PITCH_Y
data['view']={'pitch_x':PITCH_X,'pitch_y':PITCH_Y,'pad_x':PAD_X,'pad_y':PAD_Y,
              'width':PAD_X*2+max(n['x'] for n in data['focuses'])*PITCH_X,
              'height':PAD_Y*2+max(n['y'] for n in data['focuses'])*PITCH_Y,
              'item_width':165,'item_height':128,
              'max_x':max(n['x'] for n in data['focuses']),'max_y':max(n['y'] for n in data['focuses']),
              'note':f'All{len(data["focuses"])} current design coordinates preserved. Uniform preview pitch90x130; MD nationalfocusview.gui item165x128. Not an engine screenshot.'}
payload={**data,'assets':assets}
template=(HERE/'md-view.template.html').read_text(encoding='utf-8')
fragment=template.replace('__COLDWAR_DATA__',json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
(HERE/'coldwar-cyprus-md-layout.html').write_text(fragment,encoding='utf-8')
(HERE/'coldwar-cyprus-preview.html').write_text(fragment,encoding='utf-8')
(HERE/'MD_VIEW_ASSETS.json').write_text(json.dumps({'assets':provenance,'view':data['view']},indent=2)+'\n',encoding='utf-8')

# Full-size vector companion: every English label visible at100%, all coordinates.
v=data['view']; parts=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{v["width"]}" height="{v["height"]}" viewBox="0 0 {v["width"]} {v["height"]}">',
    '<rect width="100%" height="100%" fill="#252a29"/>',
    '<style>text{font-family:Arial,sans-serif;fill:#e4dcc1} .edge{fill:none;stroke:#b4a77e;stroke-width:2} .exclude{fill:none;stroke:#b77e69;stroke-width:2;stroke-dasharray:7 6}</style>',
    '<defs>']
for name,uri in assets.items(): parts.append(f'<image id="asset-{name}" href="{uri}" width="94" height="80"/>')
parts+=['</defs>', '<text x="100" y="55" font-size="30">CYPRUS · COLD WAR1970 · FULL FOCUS LAYOUT</text>',
        f'<text x="100" y="90" font-size="18">{len(data["focuses"])} focuses · 6 major political/economic routes · 39 Turkish Cypriot focuses · 22 road-to-war focuses · design preview</text>']
byid={n['id']:n for n in data['focuses']}
for section in data['sections']:
    xx=PAD_X+section['anchor'][0]*PITCH_X; yy=PAD_Y+section['anchor'][1]*PITCH_Y-100
    for j,line in enumerate(textwrap.wrap(section['title'],40)):
        parts.append(f'<text x="{xx}" y="{yy+j*23}" font-size="20" text-anchor="middle">{html.escape(line)}</text>')
for node in data['focuses']:
    x=node['world_x'];y=node['world_y']
    for group in node['prerequisite_groups']:
        for parent in group:
            a=byid[parent]; start=a['world_y']+82;end=y-43;mid=(start+end)/2
            parts.append(f'<path class="edge" d="M{a["world_x"]},{start}V{mid}H{x}V{end}"/>')
    for other_id in node['excludes']:
        if node['id']<other_id:
            b=byid[other_id];left,right=sorted((node,b),key=lambda n:n['world_x']);mid=(left['world_x']+right['world_x'])/2
            parts.append(f'<path class="exclude" d="M{left["world_x"]+85},{left["world_y"]}H{mid}V{right["world_y"]}H{right["world_x"]-85}"/><text x="{mid}" y="{(left["world_y"]+right["world_y"])/2-5}" font-size="22" text-anchor="middle">×</text>')
for node in data['focuses']:
    x=node['world_x'];y=node['world_y'];label=html.escape(node['title'])
    parts.append(f'<g><title>{label} — x{node["x"]}, y{node["y"]} — {node["id"]}</title><use href="#asset-{node["preview_icon"]}" x="{x-47}" y="{y-40}"/>')
    for j,line in enumerate(textwrap.wrap(node['title'],25)):
        parts.append(f'<text x="{x}" y="{y+47+j*13}" font-size="12" text-anchor="middle">{html.escape(line)}</text>')
    parts.append(f'<text x="{x}" y="{y+88}" fill="#aab2a7" font-size="11" text-anchor="middle">({node["x"]}, {node["y"]}) ·{node["days"]}d</text></g>')
parts.append('</svg>')
(HERE/'coldwar-cyprus-full-layout.svg').write_text('\n'.join(parts),encoding='utf-8')
print(json.dumps({'focuses':len(data['focuses']),'world':data['view'],'fragment_bytes':len(fragment.encode()),'assets':len(assets)}))
