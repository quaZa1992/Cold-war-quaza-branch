# IMPERIA COLD WAR — COMECON exact concept typography as native bitmap fonts
import math
from PIL import Image,ImageDraw,ImageFont
from build import ROOT,HERE,MARK,write

SPECS={
 'body':('segoeui.ttf',14,21,0,'302c27'),
 'small':('segoeui.ttf',12,18,0,'736b60'),
 'country':('segoeui.ttf',13,20,0,'302c27'),
 'tiny':('segoeui.ttf',11,17,0,'736b60'),
 'title':('georgia.ttf',25,29,0,'302c27'),
 'heading':('georgia.ttf',23,29,0,'302c27'),
 'number':('georgia.ttf',19,25,0,'302c27'),
 'kicker':('cour.ttf',12,17,2,'913c37'),
 'label':('cour.ttf',11,16,1,'736b60'),
 'mono':('cour.ttf',13,21,0,'913c37'),
 'cardmono':('cour.ttf',12,18,0,'913c37'),
 'button':('cour.ttf',13,18,0,'302c27'),
 'entry':('cour.ttf',13,18,0,'302c27'),
 'registertab':('cour.ttf',11,16,0,'302c27'),
 'flags':('segoeui.ttf',20,22,0,'302c27'),
 'primary':('cour.ttf',13,18,0,'fff7ed'),
}

def build_fonts():
    folder=ROOT/'gfx/fonts/COMECON';folder.mkdir(parents=True,exist_ok=True)
    chars=[0,8,9,10,13,29,31]+list(range(32,384))+[8216,8217,8220,8221,8230,9662,65279]
    declarations=['bitmapfonts = {']
    for name,(filename,size,lineheight,spacing,colour) in SPECS.items():
        font=ImageFont.truetype('C:/Windows/Fonts/'+filename,size)
        cell=size+12;cols=24;rows=math.ceil(len(chars)/cols)
        atlas=Image.new('RGBA',(cols*cell,rows*cell),(255,255,255,0));draw=ImageDraw.Draw(atlas)
        slug='cc_'+name
        lines=[f'info face="IMPERIA COLD WAR - {font.getname()[0]}" size={size} bold=0 italic=0 unicode=1',
               MARK+' concept font atlas',f'common lineHeight={lineheight} base={size} scaleW={atlas.width} scaleH={atlas.height} pages=1 packed=0',
               f'page id=0 file="{slug}.dds"',f'chars count={len(chars)}']
        for index,code in enumerate(chars):
            if code<32 or code==65279:
                advance=round(font.getlength(' ')) if code==9 else 0
                lines.append(f'char id={code} x=0 y=0 width=0 height=0 xoffset=0 yoffset=0 xadvance={advance} page=0 chnl=15');continue
            glyph=chr(code);box=font.getbbox(glyph);x=index%cols*cell;y=index//cols*cell
            draw.text((x-box[0]+2,y-box[1]+2),glyph,font=font,fill=(255,255,255,255))
            lines.append(f'char id={code} x={x} y={y} width={max(1,box[2]-box[0]+4)} height={max(1,box[3]-box[1]+4)} xoffset={box[0]-2} yoffset={box[1]-2} xadvance={round(font.getlength(glyph))+spacing} page=0 chnl=15')
        atlas.save(folder/(slug+'.dds'));(folder/(slug+'.fnt')).write_text('\n'.join(lines)+'\n',encoding='utf-8')
        declarations.append(f'bitmapfont = {{ name = "{slug}" path = "gfx/fonts/COMECON/{slug}" color = 0xff{colour} textcolors = {{ H = {{ 145 60 55 }} R = {{ 145 60 55 }} G = {{ 48 100 58 }} W = {{ 48 44 39 }} }} }}')
    declarations.append('}')
    return '\n'.join(declarations)
