# IMPERIA COLD WAR — Approved dossier typography as private native bitmap fonts
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SPECS={
 'body':('cour.ttf',12,16,0,'34342f'),
 'small':('cour.ttf',11,17,0,'66675e'),
 'kicker':('cour.ttf',11,17,1,'8c3730'),
 'label':('cour.ttf',11,17,1,'66675e'),
 'heading':('georgia.ttf',22,29,0,'34342f'),
 'prose':('segoeui.ttf',12,18,0,'34342f'),
 'button':('cour.ttf',11,17,0,'34342f'),
 'primary':('cour.ttf',11,17,0,'faf6e9'),
 'registry_font':('cour.ttf',11,17,1,'f5e8c9'),
}


def build_fonts(root,mark):
    folder=root/'gfx/fonts/superpower_dossier';folder.mkdir(parents=True,exist_ok=True)
    chars=[0,8,9,10,13,29,31]+list(range(32,384))+list(range(1024,1280))+[8216,8217,8220,8221,8230,9662,65279]
    declarations=['bitmapfonts = {']
    for name,(filename,size,height,spacing,colour) in SPECS.items():
        font=ImageFont.truetype('C:/Windows/Fonts/'+filename,size)
        cell=size+12;columns=24;rows=math.ceil(len(chars)/columns)
        atlas=Image.new('RGBA',(columns*cell,rows*cell),(255,255,255,0));draw=ImageDraw.Draw(atlas)
        slug='icsd_'+name
        lines=[f'info face="IMPERIA COLD WAR - {font.getname()[0]}" size={size} bold=0 italic=0 unicode=1',mark.strip(),
               f'common lineHeight={height} base={size} scaleW={atlas.width} scaleH={atlas.height} pages=1 packed=0',
               f'page id=0 file="{slug}.dds"',f'chars count={len(chars)}']
        for index,code in enumerate(chars):
            if code<32 or code==65279:
                advance=round(font.getlength(' ')) if code==9 else 0
                lines.append(f'char id={code} x=0 y=0 width=0 height=0 xoffset=0 yoffset=0 xadvance={advance} page=0 chnl=15');continue
            glyph=chr(code);box=font.getbbox(glyph);x=index%columns*cell;y=index//columns*cell
            draw.text((x-box[0]+2,y-box[1]+2),glyph,font=font,fill=(255,255,255,255))
            lines.append(f'char id={code} x={x} y={y} width={max(1,box[2]-box[0]+4)} height={max(1,box[3]-box[1]+4)} xoffset={box[0]-2} yoffset={box[1]-2} xadvance={round(font.getlength(glyph))+spacing} page=0 chnl=15')
        atlas.save(folder/(slug+'.dds'));(folder/(slug+'.fnt')).write_text('\n'.join(lines)+'\n',encoding='utf-8')
        declarations.append(f'bitmapfont = {{ name = "{slug}" path = "gfx/fonts/superpower_dossier/{slug}" color = 0xff{colour} textcolors = {{ H = {{ 100 70 35 }} R = {{ 140 55 48 }} G = {{ 45 90 60 }} W = {{ 52 52 47 }} }} }}')
    declarations.append('}')
    return '\n'.join(declarations)
