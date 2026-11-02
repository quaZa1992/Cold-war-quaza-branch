# IMPERIA COLD WAR — Economic organisation native-asset layout review
"""Render emitted GUI coordinates and installed bitmap fonts; not a game screenshot."""
import json
import re
from pathlib import Path
from PIL import Image
import validate as V

GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
OUT=V.OUT/'native_review';OUT.mkdir(parents=True,exist_ok=True)
LOC=dict(re.findall(r'^ (\w+): "(.*)"$',(V.ROOT/'localisation/english/ICW_economic_organisation_l_english.yml').read_text(encoding='utf-8-sig'),re.M))
SPRITES={V.first(v,'name'):v for k,o,v in V.first(V.ASTS['interface/ICW_economic_organisation.gfx'],'spriteTypes')}
OVERFLOWS=[]

class Font:
    def __init__(self,name):
        path=V.ROOT/f'gfx/fonts/{name}.fnt'
        if not path.exists():path=GAME/f'gfx/fonts/{name}.fnt'
        source=path.read_text(encoding='utf-8-sig');self.height=int(re.search(r'lineHeight=(\d+)',source)[1]);self.glyphs={};pages={}
        for i,file in re.findall(r'page id=(\d+) file="([^"]+)"',source):
            atlas=path.parent/file
            if not atlas.exists():atlas=path.with_suffix('.dds')
            pages[int(i)]=Image.open(atlas).convert('RGBA')
        for line in source.splitlines():
            if not line.startswith('char id='):continue
            d={k:int(v) for k,v in re.findall(r'(\w+)=\s*(-?\d+)',line)}
            mask=pages[d['page']].crop((d['x'],d['y'],d['x']+d['width'],d['y']+d['height'])).getchannel('A')
            self.glyphs[d['id']]=(mask,d['xoffset'],d['yoffset'],d['xadvance'])
    def width(self,text):return sum(self.glyphs.get(ord(c),self.glyphs[32])[3] for c in re.sub('§.','',text))
    def draw(self,canvas,text,x,y,w,h,name,center=False):
        lines=[]
        for para in text.split('\n'):
            line=''
            for word in para.split(' '):
                if line and self.width(line+' '+word)>w:lines.append(line);line=word
                else:line+=(' ' if line else '')+word
            lines.append(line)
        if len(lines)*self.height>h:OVERFLOWS.append({'element':name,'text':text,'required_height':len(lines)*self.height,'height':h})
        color=(220,228,223);colors={'Y':(220,197,126),'G':(143,198,133),'R':(220,128,112),'!':(220,228,223)}
        for row,line in enumerate(lines):
            px=x+(max(0,(w-self.width(line))//2) if center else 0);py=y+row*self.height;i=0
            while i<len(line):
                if line[i]=='§' and i+1<len(line):color=colors.get(line[i+1],color);i+=2;continue
                mask,dx,dy,advance=self.glyphs.get(ord(line[i]),self.glyphs[32]);canvas.paste(color,(px+dx,py+dy),mask);px+=advance;i+=1

FONTS={}
CONTEXT=None
FUNCTIONS={V.first(body,'name'):body for key,op,body in V.ASTS['common/scripted_localisation/ICW_economic_organisation.txt'] if key=='defined_text'}

def font(name):
    if name not in FONTS:FONTS[name]=Font(name)
    return FONTS[name]
def resolve(text,slug,pos):
    text=text.strip('"')
    replacements={'[icw_econ_current_name]':LOC['icw_econ_'+slug],'[icw_econ_current_modifiers]':LOC['icw_econ_effects_'+slug],'[icw_econ_status]':LOC['icw_econ_status_ready'],'[icw_econ_enact_label]':LOC['icw_econ_enact'],'[?icw_econ_position|+0]':f'{pos:+d}'}
    for key,value in replacements.items():text=text.replace(key,value)
    def function(match):
        body=FUNCTIONS.get(match[1])
        if body is None:return match[0]
        for choice in V.vals(body,'text'):
            if CONTEXT.test(V.first(choice,'trigger',[])):
                return LOC[V.first(choice,'localization_key')]
        return ''
    for _ in range(12):
        previous=text;text=LOC.get(text,text)
        text=re.sub(r'\[(icw_econ_\w+)\]',function,text)
        text=re.sub(r'\[\?(\w+)\|([+]?[0-9]+)\]',lambda m:format(CONTEXT.number(m[1]),('+' if m[2].startswith('+') else '')+'.'+m[2].lstrip('+')+'f'),text)
        if previous==text:break
    return text.replace('\\n','\n').replace('£pol_power','PP').replace('$$','$')

def render(window,slug,pos,name,selected=3):
    global CONTEXT
    CONTEXT=V.Country();CONTEXT.call('icw_econ_initialize');CONTEXT.variables.update(icw_econ_position=pos,icw_econ_selected_reform=selected,icw_econ_market_high_water=pos,gdp_total=100)
    CONTEXT.call('icw_econ_refresh_tier')
    size=V.first(window,'size');w=int(V.first(size,'width'));h=int(V.first(size,'height'))
    bg=Image.open(V.ROOT/'gfx/interface/tiles/md_tiled_window1.dds').convert('RGBA')
    canvas=bg.resize((w,h))
    for kind,o,body in window:
        if kind.lower() not in ['instanttextboxtype','buttontype','icontype']:continue
        element=V.first(body,'name').strip('"');xy=V.first(body,'position');x=int(V.first(xy,'x'));y=int(V.first(xy,'y'))
        if kind.lower()=='instanttextboxtype':
            fontname=V.first(body,'font').strip('"');face=font(fontname);face.draw(canvas,resolve(V.first(body,'text'),slug,pos),x,y,int(V.first(body,'maxWidth')),int(V.first(body,'maxHeight')),element)
            continue
        key=V.first(body,'spriteType',V.first(body,'quadTextureSprite'))
        if key not in SPRITES:continue
        sprite=SPRITES[key];path=Path(V.first(sprite,'texturefile').strip('"'));path=V.ROOT/path if (V.ROOT/path).exists() else GAME/path
        im=Image.open(path).convert('RGBA');frames=int(V.first(sprite,'noOfFrames',1));im=im.crop((0,0,im.width//frames,im.height))
        scale=float(V.first(body,'scale',1));im=im.resize((round(im.width*scale),round(im.height*scale)))
        if element.endswith('_needle'):x=round((pos+100)*2.7+59)
        canvas.alpha_composite(im,(x,y))
        if kind.lower()=='buttontype':
            fontname=V.first(body,'buttonFont').strip('"');face=font(fontname);face.draw(canvas,resolve(V.first(body,'text'),slug,pos),x+5,y+(im.height-face.height)//2,im.width-10,im.height,element,True)
    canvas.convert('RGB').save(OUT/(name+'.png'))

# IMPERIA COLD WAR — Native economic decision category layout review
def render_decisions(blocked=False):
    donor=V.parse((V.ROOT/'interface/countrydecisionview.gui').read_text(encoding='utf-8'))
    windows=V.vals(V.first(donor,'guiTypes'),'containerWindowType')
    header=next(w for w in windows if V.first(w,'name')=='"category_header"')
    row=next(w for w in windows if V.first(w,'name')=='"decision_item"')
    description=next(w for w in windows if V.first(w,'name')=='"decision_category_desc"')
    def field(window,name):return next(v for k,o,v in window if isinstance(v,list) and V.first(v,'name')=='"'+name+'"')
    def position(body):return tuple(int(V.first(V.first(body,'position'),axis)) for axis in ('x','y'))
    def texture(rel,frames=1,frame=1):
        path=V.ROOT/rel if (V.ROOT/rel).exists() else GAME/rel
        image=Image.open(path).convert('RGBA');width=image.width//frames
        return image.crop(((frame-1)*width,0,frame*width,image.height))
    face=font('hoi_16mbs')
    text=resolve(resolve('icw_econ_category_desc','liberal',45),'liberal',45)
    desc_height=len(text.split('\n'))*face.height+16
    row_y=58+desc_height
    canvas=Image.new('RGBA',(529,row_y+41*len(V.REFORMS)+6),'#202321')
    canvas.alpha_composite(texture('gfx/interface/decisionview/category_header_bg.dds'),(3,8))
    sprites=dict(re.findall(r'name\s*=\s*"([^"]+)"\s+texturefile\s*=\s*"([^"]+)"',(V.ROOT/'interface/MD_decisions.gfx').read_text(encoding='utf-8')))
    category=V.first(V.ASTS['common/decisions/categories/ICW_economic_organisation.txt'],'icw_econ_category')
    canvas.alpha_composite(texture(sprites[V.first(category,'icon')]),(18,19))
    title=field(header,'name_text');tx,ty=position(title)
    Font('hoi_20b').draw(canvas,LOC['icw_econ_category'],tx+8,ty,int(V.first(title,'maxWidth')),40,'decision_category_title',True)
    tile=texture('gfx/interface/tiles/tiled_decisions_bg_small.dds')
    # Preserve the native 16-pixel border around the automatically sized description.
    for x0,x1,dx0,dx1 in [(0,16,0,16),(16,32,16,498),(32,48,498,514)]:
        for y0,y1,dy0,dy1 in [(0,16,0,16),(16,32,16,desc_height-16),(32,48,desc_height-16,desc_height)]:
            canvas.alpha_composite(tile.crop((x0,y0,x1,y1)).resize((dx1-dx0,dy1-dy0)),(5+dx0,57+dy0))
    full_text=field(description,'full_text');dx,dy=position(full_text)
    face.draw(canvas,text,5+dx,58+dy,int(V.first(full_text,'maxWidth')),desc_height-12,'decision_category_description')
    decisions=V.first(V.ASTS['common/decisions/ICW_economic_organisation.txt'],'icw_econ_category')
    for index,(slug,name,delta,cost,desc) in enumerate(V.REFORMS):
        y=row_y+index*41;decision=V.first(decisions,'icw_econ_decision_'+slug)
        canvas.alpha_composite(texture('gfx/interface/decisionview/decision_item_bg.dds',3),(6,y))
        icon=texture(sprites[V.first(decision,'icon')]);ix,iy=position(field(row,'icon'))
        canvas.alpha_composite(icon,(6+ix-icon.width//2,y+iy-icon.height//2))
        name_field=field(row,'name_text');nx,ny=position(name_field)
        face.draw(canvas,name,6+nx,y+ny+8,int(V.first(name_field,'maxWidth')),32,'decision_name_'+slug)
        base=V.first(decision,'custom_cost_text');cost_text=LOC[base+('_blocked' if blocked else '')].replace('£pol_power','PP')
        cx,cy=position(field(row,'cost_and_timer_text'));right=6+cx+int(V.first(field(row,'cost_and_timer_text'),'maxWidth'))
        face.draw(canvas,cost_text,right-face.width(cost_text),y+cy,60,32,'decision_cost_'+slug)
        if 6+nx+face.width(name)+12>right-face.width(cost_text):OVERFLOWS.append({'element':'decision_name_cost_overlap_'+slug})
        for element,rel,frames in [('track_decision_checkbox','checkbox_small4.dds',2),('btn_select','decision_select_icon_strip.dds',4)]:
            bx,by=position(field(row,element));canvas.alpha_composite(texture('gfx/interface/decisionview/'+rel,frames,2),(6+bx,y+by))
    canvas.convert('RGB').save(OUT/('decisions_blocked.png' if blocked else 'decisions_available.png'))

def main():
    windows=V.vals(V.first(V.ASTS['interface/ICW_economic_organisation.gui'],'guiTypes'),'containerWindowType')
    for slug,pos in [('command',-80),('mixed',0),('laissez',85)]:
        render(windows[0],slug,pos,'compact_'+slug);render(windows[1],slug,pos,'dialog_'+slug)
    for slug,pos,selected in [('planning',-65,1),('command',-75,3),('regulated',25,4),('regulated',35,4),('liberal',65,4),('development',-20,3)]:
        render(windows[1],slug,pos,'dialog_'+slug+'_'+str(pos)+'_'+str(selected),selected)
    render_decisions();render_decisions(blocked=True)
    report={'project':'IMPERIA COLD WAR','scope':'Emitted GUI and native decision donor, native textures and bitmap-font measurements. Decision costs use PP in place of the inline political-power glyph. Not a game screenshot or a pointer-interaction test.','overflows':OVERFLOWS}
    (OUT/'layout_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    (OUT/'NOTICE.md').write_text('IMPERIA COLD WAR\n\nLayout review images combine the generated economic interface with installed Hearts of Iron IV/MD fonts and textures. The decision category review uses the complete category and decision-row donor definitions in interface/countrydecisionview.gui, existing decisionview frames, the MD description tile and the reform icons registered in interface/MD_decisions.gfx. Costs use PP in place of the inline political-power glyph. Original third-party credit: Paradox Interactive and Millennium Dawn contributors; individual artists and separate redistribution permission unknown. These are local QA renders, not engine screenshots. The economic controls and review composition were generated by OpenAI Codex for Enes. See ../IMPLEMENTATION.md and gfx/interface/ICW_economic_organisation/NOTICE.md for source details.\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    assert not OVERFLOWS,'Text does not fit'

if __name__=='__main__':main()
