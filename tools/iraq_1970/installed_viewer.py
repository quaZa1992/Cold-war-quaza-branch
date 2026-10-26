# IMPERIA CW — Cold War: iraq 1970 — installed viewer.
"""Generate the self-contained viewer from actual installed focus sources.

Never writes game files or the approved concept. Data is gzip-compressed to
keep the inline fragment below one megabyte; the browser unpacks it locally.
"""
from pathlib import Path
import base64
import gzip
import hashlib
import io
import json
import re
import sys
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
DEST=Path('C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f4e-9042-7b61-be51-9d85f9facd82/iraq-1970-installed.html')
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,values,emit
sys.path.insert(0,str(ROOT/'tools/iraq_1970_concept'))


def picture(im,lossless=False):
    b=io.BytesIO();im.convert('RGBA').save(b,format='WEBP',quality=88,method=6,lossless=lossless)
    return 'data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()


def fragment_for(packed):
    fragment=(HERE/'installed_viewer_fragment.html').read_text(encoding='utf-8')
    fragment=fragment.replace('<!-- INSTALLED_DATA -->',f'<script type="application/octet-stream" id="cw-installed-data">{packed}</script>')
    assert len(fragment.encode())<1_000_000,len(fragment.encode())
    assert '<html' not in fragment.lower() and '<!doctype' not in fragment.lower()
    return fragment


def refresh_template():
    """Refresh UI-only edits without re-encoding unchanged installed assets."""
    old=DEST.read_text(encoding='utf-8')
    packed=re.search(r'id="cw-installed-data">([^<]+)',old)[1]
    content=fragment_for(packed);DEST.write_text(content,encoding='utf-8',newline='\n')
    path=HERE/'staged/INSTALLED_VIEWER_REPORT.json'
    report=json.loads(path.read_text(encoding='utf-8'));report['bytes']=len(content.encode());path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')


def main():
    from render_installed import read_tree,icon,title,SPRITES,GAME,LOC
    from native_font import GLYPHS,KERNINGS,ATLAS
    from audit_design import load_design
    approved=load_design()
    approved_by={n['id']:n for n in approved['nodes']}
    gulf=json.loads((ROOT/'docs/design/iraq_1970/usa_gulf/COLDWAR_USA_GULF_CONCEPT.json').read_text())
    gulf_by={n['id']:n for n in gulf['nodes']}
    code={};providers={}
    # Only direct COLDWAR/USA1970 providers are embedded. Ordinary native engine
    # effects remain verbatim in the emitted completion payload, not invented.
    for folder in ['common/scripted_effects','common/scripted_triggers']:
        for path in (ROOT/folder).glob('*.txt'):
            if not ('COLDWAR_IRQ' in path.name or 'COLDWAR_USA_gulf' in path.name or 'USA_1970' in path.name):continue
            try:rows=parse(path.read_text(encoding='utf-8-sig'))
            except Exception:continue
            for key,_,body in rows:
                if isinstance(body,list):
                    code[key]=emit([(key,'=',body)])
                    providers[key]=str(path.relative_to(ROOT)).replace('\\','/')
    for folder in ['common/ideas','common/dynamic_modifiers']:
        for path in (ROOT/folder).glob('COLDWAR_*.txt'):
            if not any(s in path.name for s in ['COLDWAR_IRQ','COLDWAR_USA_gulf']):continue
            rows=parse(path.read_text(encoding='utf-8-sig'))
            if folder=='common/ideas':rows=first(first(rows,'ideas',[]),'country',[])
            for key,_,body in rows:
                if isinstance(body,list):code[key]=emit([(key,'=',body)]);providers[key]=str(path.relative_to(ROOT)).replace('\\','/')
    for path in (ROOT/'events').glob('COLDWAR_*.txt'):
        if not any(s in path.name for s in ['COLDWAR_IRQ','COLDWAR_USA_gulf']):continue
        for body in values(parse(path.read_text(encoding='utf-8-sig')),'country_event'):
            key=first(body,'id');code[key]=emit([('country_event','=',body)]);providers[key]=str(path.relative_to(ROOT)).replace('\\','/')
    data={'trees':{},'icons':{},'images':[],'code':code,'providers':providers,'source_hashes':{},'phase':'Implemented; HOI4 gameplay untested'}
    for tag,path in [('IRQ','common/national_focus/COLDWAR_IRQ_1970_focus.txt'),('USA','common/national_focus/USA_1970.txt')]:
        full=read_tree(path)
        parsed=first(parse((ROOT/path).read_text(encoding='utf-8-sig')),'focus_tree')
        raw={first(n,'id'):n for n in values(parsed,'focus')}
        ns=[]
        for key,n in full.items():
            a=approved_by.get(key,{})
            g=gulf_by.get(key,{})
            if tag=='IRQ':group=a['group']
            elif g:group='gulf'
            else:
                stem=key.removeprefix('USA_1970_').split('_')[0]
                group='USA '+re.sub(r'\d+$','',stem)
            reward=emit(first(raw[key],'completion_reward',[]))
            available=emit(first(raw[key],'available',[]))
            refs=sorted(set(re.findall(r'\b((?:COLDWAR_|USA_1970_)[A-Za-z0-9_]+)\s*=\s*yes\b',reward)))
            references=reward+'\n'+'\n'.join(code.get(ref,'') for ref in refs)
            event_refs=sorted({key for key in re.findall(r'\bid\s*=\s*(COLDWAR_[A-Za-z0-9_.]+)',references) if key in code and providers[key].startswith('events/')})
            refs+=event_refs;references+='\n'+'\n'.join(code[key] for key in event_refs)
            refs+=sorted({key for key in re.findall(r'\bCOLDWAR_[A-Za-z0-9_]+',references) if key in code and ('common/ideas/' in providers.get(key,'') or 'common/dynamic_modifiers/' in providers.get(key,''))})
            if a.get('modifiers') and 'COLDWAR_IRQ_'+group+'_programme' in code:refs.append('COLDWAR_IRQ_'+group+'_programme')
            ns.append({'id':key,'t':n['title'],'d':title(key+'_desc'),'xy':n['xy'],'i':n['icon'],'g':group,'p':n['prerequisites'],'e':n['excludes'],
                       'days':float(first(raw[key],'cost',0))*7,'m':a.get('modifiers',{}),'r':reward,'a':available,'refs':refs})
        groups={g['id']:g['label'].replace('\ufffd','-') for g in approved['groups']} if tag=='IRQ' else {n['g']:('Gulf and Kurdish Self-Rule' if n['g']=='gulf' else n['g']) for n in ns}
        data['trees'][tag]={'nodes':ns,'groups':groups}
        data['source_hashes'][path]=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
    image_cache={}
    for name in sorted({n['i'] for t in data['trees'].values() for n in t['nodes']}):
        rel=SPRITES[name][0]
        if rel not in image_cache:
            image_cache[rel]=len(data['images']);data['images'].append(picture(icon(name)))
        data['icons'][name]=image_cache[rel]
    data['bar']=picture(Image.open(GAME/'gfx/interface/focusview/titlebar/focus_unavailable_bg.dds'))
    used={ord(c) for t in data['trees'].values() for n in t['nodes'] for c in n['t']}|{63}
    # Copy only used native atlas glyphs; preserve their geometry/kerning. The
    # inherited font contains thousands of unused glyphs and is not embedded.
    native=Image.open(ATLAS).convert('RGBA');atlas=Image.new('RGBA',(512,512));glyphs={};x=y=row_height=0
    for cp in sorted(used):
        if cp not in GLYPHS:continue
        g=GLYPHS[cp];w,h=g['width'],g['height']
        if x+w>512:x=0;y+=row_height+1;row_height=0
        atlas.alpha_composite(native.crop((g['x'],g['y'],g['x']+w,g['y']+h)),(x,y))
        glyphs[cp]=[x,y,w,h,g['xoffset'],g['yoffset'],g['xadvance']]
        x+=w+1;row_height=max(row_height,h)
    atlas=atlas.crop((0,0,512,y+row_height+1));data['font']=picture(atlas,lossless=True);data['glyphs']=glyphs
    data['kern']={str(a)+','+str(b):v for (a,b),v in KERNINGS.items() if a in used and b in used}
    packed=base64.b64encode(gzip.compress(json.dumps(data,separators=(',',':'),ensure_ascii=False).encode(),mtime=0)).decode()
    print(json.dumps({'packed':len(packed),'font_bytes':len(data['font']),'unique_textures':len(image_cache),'icon_encoded_bytes':sum(len(v) for v in data['images']),'code_bytes':sum(len(v) for v in code.values())}),flush=True)
    fragment=fragment_for(packed)
    DEST.write_text(fragment,encoding='utf-8',newline='\n')
    report={'path':str(DEST),'bytes':len(fragment.encode()),'focuses':{k:len(t['nodes']) for k,t in data['trees'].items()},'provider_blocks':len(code),'source_hashes':data['source_hashes'],'engine_tested':False}
    (HERE/'staged/INSTALLED_VIEWER_REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
