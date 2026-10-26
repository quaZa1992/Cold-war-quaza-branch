# IMPERIA CW — Cold War: israel 1970 — focus art.
"""Register selected existing Cold War/Israel art and matching focus shine sprites."""
import base64
import io
from PIL import Image,ImageDraw,ImageFont

def register(root,data,art,write):
    plain=['# Israel 1970 | existing Cold War and Israeli focus artwork.','spriteTypes = {']
    shine=['# Israel 1970 | native MD completion shine.','spriteTypes = {']
    preview={};textures={}
    for name,source in sorted(art.items()):
        path=root/source
        im=Image.open(path).convert('RGBA')
        # DDS/TGA are used directly; PNG sources receive a lossless DDS copy for
        # Clausewitz texture compatibility. Original artwork is never altered.
        if path.suffix.lower()=='.png':
            texture='gfx/interface/goals/israel_1970/'+name.removeprefix('GFX_ISR70_focus_')+'.dds'
            dest=root/texture;dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest)
        else:texture=source
        textures[name]=texture
        idea=name.replace('GFX_ISR70_focus_','GFX_idea_ISR70_spirit_')
        for sprite in (name,idea):plain+=['\tspriteType = {',f'\t\tname = "{sprite}"',f'\t\ttexturefile = "{texture}"','\t}']
        shine+=['\tspriteType = {',f'\t\tname = "{name}_shine"',f'\t\ttexturefile = "{texture}"','\t\teffectFile = "gfx/FX/buttonstate.lua"']
        for rotation in (-90,90):
            shine+=['\t\tanimation = {',f'\t\t\tanimationmaskfile = "{texture}"','\t\t\tanimationtexturefile = "gfx/interface/goals/shine_overlay.dds"',f'\t\t\tanimationrotation = {rotation}.0','\t\t\tanimationlooping = no','\t\t\tanimationtime = 0.75','\t\t\tanimationdelay = 0','\t\t\tanimationblendmode = "add"','\t\t\tanimationtype = "scrolling"','\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }','\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 }','\t\t}']
        shine+=['\t\tlegacy_lazy_load = no','\t}']
        im.thumbnail((72,66),Image.Resampling.LANCZOS)
        indexed=im.quantize(colors=96,method=Image.Quantize.FASTOCTREE)
        b=io.BytesIO();indexed.save(b,format='PNG',optimize=True)
        preview[name]='data:image/png;base64,'+base64.b64encode(b.getvalue()).decode('ascii')
    plain.append('}');shine.append('}')
    write('interface/ISR70_focus.gfx','\n'.join(plain)+'\n')
    write('interface/ISR70_focus_shine.gfx','\n'.join(shine)+'\n')
    data['layout']['icons']=preview
    data['focus_art']=textures
    return textures

def contact_sheet(root,data):
    keys=['water','negev_agriculture','haifa_industry','civil_service','oversight','technion',
          'reserve_system','armour_programme','air_staff','naval_staff','intelligence','rogers',
          'p3_ea','p3_eb','p1_ea','p13_institution','p2_ca','p7_ca']
    nodes={n['id'].removeprefix('ISR70_'):n for n in data['nodes']}
    sheet=Image.new('RGB',(1000,720),'#202b30');draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for i,key in enumerate(keys):
        n=nodes[key];im=Image.open(root/data['focus_art'][n['icon']]).convert('RGBA');im.thumbnail((120,108),Image.Resampling.LANCZOS)
        x=(i%6)*166;y=(i//6)*240
        sheet.paste(im,(x+(166-im.width)//2,y+12),im)
        words=n['label'].split();lines=['']
        for word in words:
            if draw.textlength(lines[-1]+' '+word,font=font)>150:lines.append(word)
            else:lines[-1]=(lines[-1]+' '+word).strip()
        for j,line in enumerate(lines):draw.text((x+8,y+130+20*j),line,fill='#e4e4d7',font=font)
    sheet.save(root/'docs/israel_1970_design/revised_icons.png')
    assets=sorted(set(data['focus_art'].values()))
    # Candidate alternatives are inspected alongside the chosen art: many old
    # Cold War filenames conceal country flags, so filenames alone are unsafe.
    candidates=['generic_improve_industry.png','factory_complex.png','generic_army_tanks2.png','generic_army_tanks3.png','generic_road_construction.png','Focus_on_Water_and_Agricultural_Projects.dds','Creative_Substiutes_to_water.tga','generic_civilian_oversight.png','generic_army_cooperation.png','generic_air_command.png','generic_submarine_base.png']
    assets+=['gfx/interface/goals/coldwar/'+name for name in candidates if 'gfx/interface/goals/coldwar/'+name not in assets]
    for page in range((len(assets)+29)//30):
        sheet=Image.new('RGB',(1200,1000),'#202b30');draw=ImageDraw.Draw(sheet)
        for i,source in enumerate(assets[page*30:(page+1)*30]):
            im=Image.open(root/source).convert('RGBA');im.thumbnail((110,100),Image.Resampling.LANCZOS)
            x=(i%6)*200;y=(i//6)*200;sheet.paste(im,(x+(200-im.width)//2,y+6),im)
            name=source.rsplit('/',1)[1]
            for j in range((len(name)+22)//23):draw.text((x+5,y+115+j*18),name[j*23:(j+1)*23],fill='#e4e4d7',font=font)
        sheet.save(root/f'docs/israel_1970_design/art_audit_{page+1}.png')
