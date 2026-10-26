"""Review-only visual, native-card proof sheets and freshness check. No game writes."""
from pathlib import Path
import base64,hashlib,importlib.util,io,json
from PIL import Image,ImageDraw,ImageFont

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
VIZ=Path('C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f32-41dc-74b3-baa1-8f6916e026ed')

def main():
    inv=json.loads((HERE/'inventory.json').read_text(encoding='utf-8'))
    proposed=json.loads((HERE/'proposals.json').read_text(encoding='utf-8'))
    for rel,want in inv['hashes'].items():
        assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==want, 'Loaded source changed: '+rel
    nodes=[{k:v for k,v in n.items() if k not in ('availability','reward')} for n in inv['nodes']]
    data=dict(nodes=nodes,groups=inv['groups'],art=inv['art'],font=inv['font'],issues=proposed['issues'],choices=proposed['choices'])
    template=(VIZ/'coldwar-vietnam-impact.template.html').read_text(encoding='utf-8')
    fragment=template.replace('__AUDIT_DATA__',json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/'))
    path=VIZ/'coldwar-vietnam-impact.html'
    assert len(fragment.encode('utf-8'))<1_000_000
    path.write_text(fragment,encoding='utf-8',newline='\n')
    # Native bitmap label renderer is import-safe and performs no writes at import.
    spec=importlib.util.spec_from_file_location('proof_native',VIZ/'coldwar-vietnam-render.py')
    native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
    label=native.NativeLabelFont()
    bar=Image.open(native.asset('gfx/interface/focusview/titlebar/focus_unavailable_bg.dds')).convert('RGBA')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    by={n['id']:n for n in nodes}
    proofs=[]
    for group,start,end,title in [('chinh',0,9,'CURRENT: Chinh, 665 nominal days for a 157-day mandate'),('army',17,22,'CURRENT: Aircrew training behind the exclusive fleet branch'),('linh',6,9,'CURRENT: investment focus behind political pluralism')]:
        subset=[n for n in nodes if n['group']==group and start<=n['y']<=end]
        minx=min(n['x'] for n in subset)*96-125;maxx=max(n['x'] for n in subset)*96+125
        miny=start*130-70;maxy=end*130+100
        width=max(760,int(maxx-minx));height=int(maxy-miny)+80
        im=Image.new('RGBA',(width,height),'#202825');draw=ImageDraw.Draw(im)
        draw.text((16,13),title,font=font,fill='#eddbac')
        draw.text((16,39),'Loaded files / native art and glyphs / external connector approximation',font=font,fill='#c0c9bb')
        ox=(width-(maxx-minx))/2-minx;oy=80-miny
        def point(n):return round(n['x']*96+ox),round(n['y']*130+oy)
        ids={n['id'] for n in subset}
        for n in subset:
            x,y=point(n)
            for clause in n['prerequisites']:
                for pid in clause:
                    if pid not in ids:continue
                    px,py=point(by[pid]);sy=py+69;ey=y-43;mid=(sy+ey)//2
                    draw.line([(px,sy),(px,mid),(x,mid),(x,ey)],fill='#8c9e8c',width=2)
            for peer in n['exclusive']:
                if peer not in ids or peer<n['id']:continue
                px,py=point(by[peer]);left,right=sorted((x,px));mid=(left+right)//2;yy=y+45
                if right-left>165:
                    draw.line((left+83,yy,right-83,yy),fill='#bb8c7e',width=2)
                    draw.line((mid-5,yy-5,mid+5,yy+5),fill='#e2a38b',width=2)
                    draw.line((mid-5,yy+5,mid+5,yy-5),fill='#e2a38b',width=2)
        for n in subset:
            x,y=point(n);icon=Image.open(ROOT/n['icon']).convert('RGBA')
            im.alpha_composite(bar,(x-bar.width//2,y+20));im.alpha_composite(icon,(x-icon.width//2,y-icon.height//2))
            s=n['label']
            while label.getlength(s)>147:s=s[:-1]
            label.draw(im,(x,y+45),s,(230,224,211))
        out=VIZ/('coldwar-vietnam-impact-'+group+'.png');im.convert('RGB').save(out)
        proofs.append(dict(group=group,path=str(out),nodes=len(subset),size=im.size))
    report=dict(status='read-only source, card and proposal preview',html=str(path),html_bytes=path.stat().st_size,focuses=len(nodes),issues=len(data['issues']),choice_pairs=len(data['choices']),proofs=proofs,loaded_hashes_unchanged=True,engine_tested=False,browser_tested=False)
    (HERE/'preview_review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))

if __name__=='__main__':main()
