# IMPERIA COLD WAR — World Ledger news-local Georgia bitmap fonts.
import math
from PIL import Image, ImageDraw, ImageFont

MARK = '# IMPERIA COLD WAR — World Ledger news-local serif font atlas.'
FOLDER = 'gfx/fonts/ICW_news'

def build(dds):
    chars = sorted(set([0,8,9,10,13,29,31] + list(range(32,592)) + list(range(0x370,0x530)) + list(range(0x2010,0x2028)) + [0x20ac,0x20bd,0x2122,0xfeff]))
    files = {};records = [];fontpaths={}
    for slug,filename,size,lineheight in [('icw_news_title','georgiab.ttf',24,26),('icw_news_body','georgia.ttf',16,23)]:
        font = ImageFont.truetype('C:/Windows/Fonts/'+filename,size)
        groups=[chars] if size<=20 else [[code for code in chars if code<256 or code>=0x2000],[code for code in chars if 256<=code<592],[code for code in chars if 0x370<=code<0x400],[code for code in chars if 0x400<=code<0x530]]
        fontpaths[slug]=[]
        for page_index,page_chars in enumerate(groups):
            atlas_name=slug if page_index==0 else slug+'_'+str(page_index)
            fontpaths[slug].append('"'+FOLDER+'/'+atlas_name+'"')
            boxes={code:font.getbbox(chr(code)) for code in page_chars if code>=32}
            cell=max(size+12,max(max(b[2]-b[0],b[3]-b[1])+4 for b in boxes.values()))
            width=1024;cols=width//cell;rows=math.ceil(len(page_chars)/cols)
            height=2**math.ceil(math.log2(rows*cell))
            assert height<=1024,(atlas_name,width,height)
            atlas=Image.new('RGBA',(width,height),(255,255,255,0));draw=ImageDraw.Draw(atlas)
            lines=[f'info face="IMPERIA COLD WAR News - {font.getname()[0]}" size={size} bold={int(filename=="georgiab.ttf")} italic=0 unicode=1',MARK,f'common lineHeight={lineheight} base={size} scaleW={width} scaleH={height} pages=1 packed=0 alphaChnl=1 redChnl=0 greenChnl=0 blueChnl=0',f'page id=0 file="{atlas_name}.dds"',f'chars count={len(page_chars)}']
            for i,code in enumerate(page_chars):
                if code<32 or code==0xfeff:
                    advance=round(font.getlength(' ')) if code==9 else 0
                    lines.append(f'char id={code} x=0 y=0 width=0 height=0 xoffset=0 yoffset=0 xadvance={advance} page=0 chnl=15');continue
                c=chr(code);b=boxes[code];x=(i%cols)*cell;y=(i//cols)*cell
                w=max(1,b[2]-b[0]+4);h=max(1,b[3]-b[1]+4)
                assert w<=cell and h<=cell,(atlas_name,code,w,h,cell)
                draw.text((x-b[0]+2,y-b[1]+2),c,font=font,fill=(255,255,255,255))
                lines.append(f'char id={code} x={x} y={y} width={w} height={h} xoffset={b[0]-2} yoffset={b[1]-2} xadvance={round(font.getlength(c))} page=0 chnl=15')
            files[f'{FOLDER}/{atlas_name}.dds']=dds(atlas)
            files[f'{FOLDER}/{atlas_name}.fnt']=('\n'.join(lines)+'\n').encode('utf-8')
            records.append(dict(name=atlas_name,system_source=filename,size=size,line_height=lineheight,base=size,characters=len(page_chars),atlas=list(atlas.size)))
    colours='textcolors = { G = { 42 116 48 } R = { 178 45 45 } Y = { 135 103 22 } H = { 135 103 22 } T = { 41 41 41 } W = { 41 41 41 } }'
    declarations='bitmapfonts = {\n'
    # Live MD BMFonts use fontfiles, not the legacy path/TGA loader.
    # Every fallback page retains exactly the same base and lineHeight.
    for slug,paths in fontpaths.items():
        declarations+='bitmapfont = { name = "'+slug+'" fontfiles = { '+' '.join(paths)+' } color = 0xff292929 '+colours+' }\n'
    declarations+='}\n'
    return files,declarations,records
