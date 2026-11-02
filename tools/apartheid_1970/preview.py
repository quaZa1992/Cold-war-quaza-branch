# IMPERIA COLD WAR — Faithful apartheid branch and full generic focus preview.
"""Render coordinates and prospective effects from the emitted focus file."""
from pathlib import Path
import html
import importlib.util
import json
import re
import sys
import textwrap
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,walk
compiler_spec=importlib.util.spec_from_file_location('apartheid_compiler',HERE/'compile.py')
compiler=importlib.util.module_from_spec(compiler_spec)
compiler_spec.loader.exec_module(compiler)
DOMAINS,P,focus_positions=compiler.DOMAINS,compiler.P,compiler.focus_positions
DEST=ROOT/'docs/design/apartheid_1970'


def main():
    DEST.mkdir(parents=True,exist_ok=True)
    generic,positions=focus_positions()
    rows=parse((ROOT/'common/national_focus/COLDWAR_AP_1970_shared.txt').read_text(encoding='utf-8'))
    own={first(row,'id'):row for key,op,row in rows if key=='shared_focus'}
    def resolve(key):
        if key in positions:return positions[key]
        row=own[key];x=int(first(row,'x'));y=int(first(row,'y'));parent=first(row,'relative_position_id')
        if parent:
            a,b=resolve(parent);x+=a;y+=b
        positions[key]=(x,y);return x,y
    for key in own:resolve(key)
    local={}
    for path in (ROOT/'localisation/english').glob('*generic*focus*.yml'):
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            match=re.match(r'\s+([^\s:]+):\d*\s+"(.*)"',line)
            if match:local[match[1]]=match[2]
    records=[]
    for key,row in {**generic,**own}.items():
        domain=next((d for d in DOMAINS if key==P+d+'_focus'),None)
        groups=[[v for k,o,v in group if k=='focus'] for kind,op,group in row if kind=='prerequisite']
        record={'id':key,'name':DOMAINS[domain]['name'] if domain else local.get(key,key.replace('GEN_1970_','').replace('_',' ').title()),'x':positions[key][0],'y':positions[key][1],'own':domain is not None,'prerequisite_groups':groups,'prerequisites':[key for group in groups for key in group],'cost':first(row,'cost'),'effects':[]}
        if domain:
            record['description']=DOMAINS[domain]['desc']
            for mod,base in DOMAINS[domain]['mods'].items():
                record['effects'].append({'modifier':mod,'base':str(base),'change':str(-float(base)/4)})
            if domain=='political':record['effects'] += [{'modifier':k,'base':str(v),'change':str(-v/4)} for k,v in [('Worldwide trade opinion',-20),('Sub-Saharan trade opinion',-50),('Sub-Saharan diplomatic opinion',-50)]]
        records.append(record)
    own_records=[r for r in records if r['own']]
    # Normal-size branch crop, using the exact emitted absolute coordinates.
    im=Image.new('RGB',(1240,510),'#162028');draw=ImageDraw.Draw(im)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
    title=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',23)
    draw.text((34,24),'Racial policy and reform',font=title,fill='#f1e1b4')
    draw.text((34,59),'Layout preview from installed focus coordinates. This is not a game screenshot.',font=small,fill='#a8b8bd')
    minx=min(r['x'] for r in own_records);miny=min(r['y'] for r in own_records)
    centers={r['id']:((r['x']-minx)*78+140,(r['y']-miny)*115+150) for r in own_records}
    for r in own_records:
        for parent in r['prerequisites']:
            if parent in centers:
                x,y=centers[r['id']];px,py=centers[parent]
                draw.line([(px,py+42),(px,py+85),(x,py+85),(x,y-42)],fill='#b5a67d',width=2)
    for r in own_records:
        x,y=centers[r['id']]
        draw.rounded_rectangle((x-105,y-45,x+105,y+45),radius=7,fill='#253641',outline='#baaa7d',width=2)
        lines=textwrap.wrap(r['name'],24)
        for i,line in enumerate(lines):
            box=draw.textbbox((0,0),line,font=font);draw.text((x-(box[2]-box[0])/2,y-26+i*21),line,font=font,fill='#f4edda')
        draw.text((x-55,y+53),'35 days | first reform',font=small,fill='#bbd2ca')
    im.save(DEST/'FOCUS_PREVIEW.png')
    safe=json.dumps(records).replace('</','<\\/')
    document='''<!doctype html>
<!-- IMPERIA COLD WAR — Dynamic 1970 apartheid policy preview. -->
<html lang="en"><meta charset="utf-8"><title>IMPERIA COLD WAR Apartheid focus integration</title>
<style>body{margin:0;background:#162028;color:#e5ece9;font:15px system-ui}header{padding:18px 24px}h1{font-size:24px;margin:0 0 8px}button{background:#354954;color:#fff;border:1px solid #b5a67d;padding:8px 14px;cursor:pointer}main{display:grid;grid-template-columns:1fr 350px;gap:18px;padding:0 24px 24px}img{max-width:100%;border:1px solid #455a63}#map{overflow:auto;height:580px;border:1px solid #455a63;background:#10191f}svg{display:block;transform-origin:0 0}aside{background:#22323d;padding:18px;border:1px solid #455a63}td,th{padding:7px;border-bottom:1px solid #455a63;text-align:left}small{color:#b5c3c7}h2{font-size:19px}rect{cursor:pointer}</style>
<header><h1>IMPERIA COLD WAR Apartheid policy integration</h1><small>Installed coordinates and prerequisites. Layout preview, not a live game screenshot.</small></header>
<main><section><img src="FOCUS_PREVIEW.png" alt="Five focus policy branch"><p><button id="overview">Full tree overview</button> <button id="branch">Focus on the new branch</button> <button id="normal">Normal scale</button></p><div id="map"><svg id="tree" xmlns="http://www.w3.org/2000/svg"></svg></div></section><aside id="details"><h2>Inspect a focus</h2><p>Click a gold node to inspect its exact first reform contribution and starting base. The grey nodes preserve the existing generic tree.</p></aside></main>
<script>const rows=DATA;const svg=document.getElementById('tree'),map=document.getElementById('map');const ns='http://www.w3.org/2000/svg';let scale=.16;const width=(Math.max(...rows.map(r=>r.x))+3)*88,height=(Math.max(...rows.map(r=>r.y))+2)*100;svg.setAttribute('viewBox',`0 0 ${width} ${height}`);function el(name,attrs){const n=document.createElementNS(ns,name);for(const [k,v]of Object.entries(attrs))n.setAttribute(k,v);svg.append(n);return n}for(const r of rows){for(const id of r.prerequisites){const p=rows.find(n=>n.id===id);if(p)el('path',{d:`M${(p.x+1)*88} ${(p.y+1)*100+23} V${(r.y+1)*100-42} H${(r.x+1)*88} V${(r.y+1)*100-23}`,stroke:r.own?'#c5b47f':'#34434b',fill:'none','stroke-width':2})}}for(const r of rows){const x=(r.x+1)*88,y=(r.y+1)*100;const box=el('rect',{x:x-75,y:y-23,width:150,height:46,rx:5,fill:r.own?'#695a32':'#28343c',stroke:r.own?'#e0c783':'#50616a'});const t=el('text',{x,y:y+4,'text-anchor':'middle',fill:r.own?'#fff0b9':'#aab8bf','font-size':11});t.textContent=r.name.length>25?r.name.slice(0,24)+'…':r.name;box.onclick=()=>{if(!r.own)return;const panel=document.getElementById('details');panel.replaceChildren();const h=document.createElement('h2');h.textContent=r.name;panel.append(h);const p=document.createElement('p');p.textContent=r.description;panel.append(p);const info=document.createElement('p');info.textContent='35 days. Applies the first quarter-step reform and unlocks further revision and restoration decisions.';panel.append(info);const table=document.createElement('table');const head=table.insertRow();for(const v of ['Modifier','Base','Change']){const c=document.createElement('th');c.textContent=v;head.append(c)}for(const fx of r.effects){const tr=table.insertRow();for(const v of [fx.modifier,fx.base,fx.change])tr.insertCell().textContent=v}panel.append(table)}}function zoom(s){scale=s;svg.style.width=width*s+'px';svg.style.height=height*s+'px'}document.getElementById('overview').onclick=()=>{zoom(.055);map.scrollTo(0,0)};document.getElementById('normal').onclick=()=>zoom(1);document.getElementById('branch').onclick=()=>{zoom(1);const r=rows.find(r=>r.own);map.scrollTo(Math.max(0,(r.x-7)*88),(r.y-.6)*100)};zoom(.16);</script></html>'''.replace('DATA',safe)
    (DEST/'FOCUS_PREVIEW.html').write_text(document,encoding='utf-8')
    (HERE/'layout.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','existing_focuses':len(generic),'new_focuses':own_records,'native_game_screenshot':False},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'existing_focuses':len(generic),'new_focuses':len(own_records),'preview':str(DEST/'FOCUS_PREVIEW.html')}))


if __name__=='__main__':main()
