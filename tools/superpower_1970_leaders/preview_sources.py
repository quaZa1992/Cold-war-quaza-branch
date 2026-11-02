# IMPERIA COLD WAR — Technical portrait source inspection thumbnails.
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps, ImageFont
import json
HERE=Path(__file__).resolve().parent
rows=json.loads((HERE/'sources.json').read_text(encoding='utf-8'))['portraits']
pending=[r for r in rows if r['status']=='reference_ready' and not (HERE/'generated'/(r['id']+'.json')).exists() and not (HERE/'generated'/(r['id']+'_error.json')).exists()]
sheet=Image.new('RGB',(1200,((len(pending)+5)//6)*285),'#20272b'); draw=ImageDraw.Draw(sheet)
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',12)
for i,r in enumerate(pending):
    path=HERE/r['reference']; im=Image.open(path).convert('RGB')
    print(r['id'],im.size,path.stat().st_size)
    if path.stat().st_size>15000000:
        im.thumbnail((2048,2048)); output=path.with_stem(path.stem+'_input').with_suffix('.jpg'); im.save(output,quality=95)
        r['generation_input']=output.relative_to(HERE).as_posix()
    x,y=i%6*200,i//6*285
    sheet.paste(ImageOps.fit(im,(186,250),centering=(.5,.1)),(x+7,y))
    draw.text((x+100,y+266),r['id'].split('_',1)[1],font=font,fill='white',anchor='mm')
sheet.save(HERE/'PENDING_SOURCE_REVIEW.png')
(HERE/'sources.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',portraits=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
