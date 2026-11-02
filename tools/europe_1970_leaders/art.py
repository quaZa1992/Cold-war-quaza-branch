# IMPERIA COLD WAR — Period portrait conversion and existing Eastern asset replacement.
"""Convert approved restorations to native DDS. No photographic retouching here."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageOps,ImageDraw,ImageFont

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
UNUSED={'SOV_boris_nemtsov','SOV_gennady_zyuganov','SOV_grigory_yavlinsky','SOV_vladimir_putin','SOV_vladimir_zhirinovsky','SOV_yury_luzhkov','SOV_maria_vladimirovna'}
# Technical framing only: omit peripheral figures and an invented sleeve detail.
MASTER_CROPS={'heinz_stehr':(.12,0,.9,.61),'ernst_goldenbaum':(0,0,.73,1)}

def approved():
    return {r['id']:r for r in json.loads((HERE/'approved_portraits.json').read_text(encoding='utf8'))['portraits']}

def sources():
    rows={r['id']:r for r in json.loads((HERE/'sources.json').read_text(encoding='utf8'))['portraits']}
    for key,record in approved().items():
        old=rows[key]
        rows[key]=dict(project='IMPERIA COLD WAR',id=key,name=old['name'],groups=old.get('groups',[]),bindings=old.get('bindings',[]),status='approved_original',reference=record['reference'],source_author=record['source_author'],licence=record['licence'],licence_url='unknown',date='Original photograph date unknown; the exact previously approved project texture is retained.',source_page='https://github.com/Imperia-MD/mdcoldwar/blob/'+record['git_commit']+'/'+record['original_binding'],approval_record=record)
    return rows

def master(source):
    key=source['id'];error=HERE/'generated'/(key+'_error.json')
    if key in approved():
        record=approved()[key];path=HERE/record['reference']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256'],'Approved portrait source was changed: '+key
        return path,'Previously approved original DDS retained byte-for-byte; no image edits'
    if error.exists():
        return HERE/source['generation_input'],'Identified period photograph; AI restoration rejected by the image service'
    record=HERE/'generated'/(key+'.json')
    assert record.exists(),'Missing restoration: '+key
    data=json.loads(record.read_text(encoding='utf8'))
    assert data.get('source_input_hash')==hashlib.sha256((HERE/source['generation_input']).read_bytes()).hexdigest(),'Superseded input: '+key
    return HERE/data['master'],'Identity-preserving AI colour restoration and photographic enhancement'

def convert(source,destination):
    if source['id'] in approved():
        record=approved()[source['id']];path,method=master(source);raw=path.read_bytes()
        for target in {destination,record['original_binding'],*record.get('compatibility_aliases',[])}:
            out=ROOT/target;out.parent.mkdir(parents=True,exist_ok=True)
            if not out.exists() or out.read_bytes()!=raw:out.write_bytes(raw)
        return method
    path,method=master(source);im=Image.open(path).convert('RGBA')
    if source['id'] in MASTER_CROPS and not (HERE/'generated'/(source['id']+'_error.json')).exists():
        im=im.crop(tuple(round(v*im.size[i%2]) for i,v in enumerate(MASTER_CROPS[source['id']])))
    destination=ROOT/destination;destination.parent.mkdir(parents=True,exist_ok=True)
    ImageOps.fit(im,(156,210),method=Image.Resampling.LANCZOS,centering=(.5,.15)).save(destination,format='DDS')
    return method

def eastern():
    return {k:r for k,r in sources().items() if k[:3].isupper() and k not in UNUSED}

def install_eastern():
    records=eastern();assert len(records)==25,len(records)
    for row in records.values():
        assert row['bindings'],row['id']
        for path in sorted(set(row['bindings'])):
            assert (ROOT/path).exists(),'Do not invent a second leader binding: '+path
            convert(row,path)

def contact(items,destination,columns=8):
    sheet=Image.new('RGB',(columns*170,((len(items)+columns-1)//columns)*245),'#20272b')
    draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',12)
    for i,(name,path) in enumerate(items):
        x,y=i%columns*170,i//columns*245
        sheet.paste(Image.open(ROOT/path).convert('RGB'),(x+7,y))
        draw.text((x+85,y+219),name,font=font,fill='white',anchor='mm')
    sheet.save(HERE/destination)

def document(data):
    all_sources=sources();assets=[]
    for key in sorted({p['key'] for p in data.values()}|set(eastern())):
        row=all_sources[key]
        bindings=sorted({p['portrait'] for p in data.values() if p['key']==key}) if not key[:3].isupper() else sorted(set(row['bindings']))
        if key in approved():
            record=approved()[key];bindings=sorted(set(bindings)|{record['original_binding'],*record.get('compatibility_aliases',[])})
        _,method=master(row)
        assets.append(dict(project='IMPERIA COLD WAR',id=key,name=row['name'],source=row,
            modifications=method if key in approved() else method+'; technical crop and resize to 156 x 210 DDS',
            technical_master_crop=MASTER_CROPS.get(key),
            bindings=[dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in bindings]))
    (HERE/'ASSET_MANIFEST.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',assets=assets),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    notice=['IMPERIA COLD WAR: German leadership and Eastern portrait provenance','',
        'Assets include restored photographs and the unchanged, previously approved portraits of Willy Brandt, Walter Ulbricht and Leonid Brezhnev. A project marker does not establish ownership. Source credits and reported licences are reproduced below; unknown permission is not a grant of redistribution rights.',
        'Requested treatment: "Kolorisiere das Bild und mache es qualitativ wie ein Handyfoto." Facial identity, period age and clothing are retained. Masters were produced with the image service. Python performs technical framing, resizing and DDS export only.',
        'Breschnew/Brezhnev and all Eastern entries retain their existing leader definitions and texture bindings. No duplicate person entries are introduced.',
        'Restoration rejections use the identified source photograph without AI enhancement. Full source metadata, hashes and installed bindings are in ASSET_MANIFEST.json.','','']
    for a in assets:
        s=a['source'];meta=s.get('commons_metadata',{}).get('extmetadata',{})
        date=s.get('date') or meta.get('DateTimeOriginal',{}).get('value') or 'unknown'
        notice.extend(['## '+a['name'],'',f"- Source: {s.get('source_page') or s.get('source_url') or 'unknown'}",f"- Original author/credit: {s.get('source_author') or 'unknown'}",f"- Source date: {date}",f"- Reported licence/permission: {s.get('licence') or 'unknown'}",f"- Licence URL: {s.get('licence_url') or 'unknown'}",'- Modifications: '+a['modifications'], '- Installed assets: '+', '.join('`'+b['path']+'`' for b in a['bindings']),''])
    (HERE/'ASSET_NOTICE.md').write_text('\n'.join(notice)+'\n',encoding='utf8')
    for tag in ('GER','DDR'):
        contact([(p['name'],p['portrait']) for p in data.values() if p['tag']==tag],tag+'_PORTRAIT_REVIEW.png')
    contact([(r['name'],r['bindings'][0]) for r in eastern().values()],'EAST_PORTRAIT_REVIEW.png')
    contact([(all_sources[key]['name'],record['original_binding']) for key,record in approved().items()],'APPROVED_PORTRAITS.png',columns=3)
