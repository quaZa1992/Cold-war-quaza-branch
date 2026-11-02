# IMPERIA COLD WAR — Independent native-asset focus geometry composition for proposal QA
"""A bounded composition, not a browser screenshot or live HOI4 rendering."""
from pathlib import Path
from io import BytesIO
import base64
import json
import re
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/design/usa_african_contest_20261030'
VIZ=OUT/'previews'
VIZ.mkdir(exist_ok=True)
source=(OUT/'preview.html').read_text(encoding='utf-8')
data=json.loads(re.search(r'<script type="application/json" id="af-data">(.*?)</script>',source,re.S)[1])
byid={n['id']:n for n in data['nodes']}
font=lambda size:ImageFont.truetype('C:/Windows/Fonts/arial.ttf',size)
fonts={size:font(size) for size in (11,12,13,14,18,24)}
icons={k:Image.open(BytesIO(base64.b64decode(v.split(',')[1]))).convert('RGBA') for k,v in data['assets'].items()}
INK='#ece8d8';MUTED='#c2c6b5';GOLD='#ead083';LINE='#798271';BG='#20261f';PANEL='#292f28'

def wrapped(text,width,size=12):
    rows=[]
    for paragraph in text.split('\n'):
        row=''
        for word in paragraph.split():
            trial=(row+' '+word).strip()
            if row and fonts[size].getlength(trial)>width:rows.append(row);row=word
            else:row=trial
        rows.append(row)
    return rows

def shown_for(area):
    nodes=[dict(n,sx=n['x'],sy=n['y']) for n in data['nodes'] if n['area']==area]
    if area=='overview':
        for i,key in enumerate(('angola','kinshasa','ethiopia','pretoria')):nodes.append(dict(byid[key],parents=[['contest']],sx=.25 if i%2==0 else .75,sy=3+i//2))
    return nodes

def routes(nodes,width):
    positions={n['id']:(n['sx']*width,18+n['sy']*150) for n in nodes};paths=[]
    for n in nodes:
        x,y=positions[n['id']]
        for group in n['parents']:
            for parent in group:
                if parent not in positions:continue
                px,py=positions[parent];start=py+122;end=y+7
                if y-py>151:points=[(px,start),(px,start+10),(width/2,start+10),(width/2,y-5),(x,y-5),(x,end)]
                else:middle=(start+end)/2;points=[(px,start),(px,middle),(x,middle),(x,end)]
                paths.append((parent,n['id'],points))
    return paths

def main():
    issues=[];views=[]
    for width in (694,320):
        for area in ('operations','overview','angola','central','horn','southern'):
            nodes=shown_for(area);bounds={}
            for n in nodes:
                title_height=max(37,len(wrapped(n['title'],130 if width==320 else 138))*14.4+8)
                height=84+title_height+(19 if area=='overview' and n['area']!='overview' else 0)
                x=n['sx']*width;y=18+n['sy']*150
                bounds[n['id']]=(x-(71 if width==320 else 75),y,x+(71 if width==320 else 75),y+height)
                if bounds[n['id']][0]<0 or bounds[n['id']][2]>width:issues.append([area,width,n['id'],'outside canvas'])
            for i,a in enumerate(nodes):
                for b in nodes[i+1:]:
                    ax,ay,ar,ab=bounds[a['id']];bx,by,br,bb=bounds[b['id']]
                    if max(ax,bx)<min(ar,br) and max(ay,by)<min(ab,bb):issues.append([area,width,a['id'],b['id'],'card overlap'])
            # Check long and adjacent native-style orthogonal connectors against unrelated cards.
            for parent,child,points in routes(nodes,width):
                for a,b in zip(points,points[1:]):
                    for key,(left,top,right,bottom) in bounds.items():
                        if key in (parent,child):continue
                        if a[0]==b[0] and left+1<a[0]<right-1 and max(min(a[1],b[1]),top+1)<min(max(a[1],b[1]),bottom-1):issues.append([area,width,parent,child,key,'vertical connector intersects card'])
                        if a[1]==b[1] and top+1<a[1]<bottom-1 and max(min(a[0],b[0]),left+1)<min(max(a[0],b[0]),right-1):issues.append([area,width,parent,child,key,'horizontal connector intersects card'])
            if width==320:continue
            height=int(max(v[3] for v in bounds.values())+72)
            image=Image.new('RGBA',(width,height),BG);draw=ImageDraw.Draw(image)
            for parent,child,points in routes(nodes,width):draw.line(points,fill=LINE,width=2)
            for priority in ('angola','central','horn','southern'):
                pair=[n for n in nodes if n['priority']==priority]
                if len(pair)==2 and pair[0]['sy']==pair[1]['sy']:
                    a,b=sorted(pair,key=lambda n:n['sx']);yy=18+a['sy']*150+46
                    for xx in range(int(a['sx']*width+47),int(b['sx']*width-47),9):draw.line((xx,yy,min(xx+4,b['sx']*width-47),yy),fill=GOLD,width=1)
            for n in nodes:
                x=n['sx']*width;y=18+n['sy']*150;im=icons[n['icon']].copy();im.thumbnail((84,84),Image.Resampling.LANCZOS);image.alpha_composite(im,(round(x-im.width/2),round(y)))
                title=wrapped(n['title'],138);h=max(37,len(title)*14.4+8);draw.rounded_rectangle((x-75,y+84,x+75,y+84+h),radius=5,fill='#363d31',outline='#99b8a2' if n['existing'] else '#858874')
                for i,line in enumerate(title):draw.text((x,y+84+h/2+(i-(len(title)-1)/2)*14.4),line,font=fonts[12],fill=INK,anchor='mm')
                if area=='overview' and n['area']!='overview':draw.text((x,y+84+h+10),{'angola':'Angola','central':'Zaire & Zambia','horn':'Horn of Africa','southern':'Southern Africa'}[n['area']],font=fonts[11],fill=MUTED,anchor='mm')
            draw.text((14,height-22),'IMPERIA COLD WAR: proposed geometry, native icons, approximate typography',font=fonts[11],fill=MUTED)
            name='african-contest-'+area+'-review.png';image.save(VIZ/name);views.append(name)
    report=dict(project='IMPERIA COLD WAR',status='PASS' if not issues else 'FAIL',views=views,tested_widths=[694,320],findings=issues,scope='Independent card bounds, native-icon composition and orthogonal connector approximation. Not browser CSS or HOI4 engine geometry.')
    (OUT/'LAYOUT_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
    assert not issues,issues

if __name__=='__main__':main()
