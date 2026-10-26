# IMPERIA CW — Cold War: render native GUI files with the installed bitmap fonts.
"""Layout QA from the generated GUI/GFX/localisation, not a game screenshot."""
import json
import re
from pathlib import Path
from PIL import Image
import validate as V

ROOT=V.ROOT
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
OUT=ROOT/'docs/design/space_race_1970/native_review'
OUT.mkdir(parents=True,exist_ok=True)
LOC=dict(re.findall(r'^ ([\w.]+): "(.*)"$',(ROOT/'localisation/english/COLDWAR_space_race_l_english.yml').read_text(encoding='utf-8-sig'),re.M))
DEFINED={V.first(v,'name'):V.values(v,'text') for k,op,v in V.ASTS['common/scripted_localisation/COLDWAR_space_race_localisation.txt'] if k=='defined_text'}
SPRITES={V.first(v,'name').strip('"'):v for file,source in V.ASTS.items() if file.endswith('.gfx') for k,op,body in source if k=='spriteTypes' for k2,op2,v in body if k2=='spriteType'}
WINDOW=V.first(V.first(V.ASTS['interface/COLDWAR_space_race.gui'],'guiTypes'),'containerWindowType')
GUI=V.first(V.first(V.ASTS['common/scripted_guis/COLDWAR_space_race_gui.txt'],'scripted_gui'),'cw_sr_main')
VISIBLE={k.removesuffix('_visible'):v for k,op,v in V.first(GUI,'triggers') if k.endswith('_visible')}
ENABLED={k.removesuffix('_click_enabled'):v for k,op,v in V.first(GUI,'triggers') if k.endswith('_click_enabled')}
PROPERTIES={k:v for k,op,v in V.first(GUI,'properties',[])}
NAMES={p['id']:p['name'] for p in V.DATA['profiles']};NAMES['SAU']='Saudi Arabia'
OVERFLOWS=[]


def resolve(key,m,depth=0):
    if depth>10:return key
    key=key.strip('"')
    if key in DEFINED:
        for entry in DEFINED[key]:
            if m.test(V.first(entry,'trigger',[])):
                return resolve(V.first(entry,'localization_key'),m,depth+1)
    text=LOC.get(key,key).replace('\\n','\n')
    def replace(match):
        content=match[1]
        if content.startswith('?'):
            var,_,precision=content[1:].partition('|');return f'{m.get(var):.{int(precision or 0)}f}'
        if content=='ROOT.GetName':return NAMES[m.c.tag]
        if content=='GetDateText':return '1 January 1970'
        if content.startswith('event_target:') and content.endswith('.GetName'):
            target=content.split(':',1)[1].split('.')[0];return NAMES[m.targets[target].tag] if target in m.targets else '—'
        return resolve(content,m,depth+1)
    return re.sub(r'\[([^\]]+)\]',replace,text)


class Font:
    def __init__(self,name):
        self.color=(24,32,38) if name.startswith('cw_sr_dark_') else (156,170,170) if name.startswith('cw_sr_muted_') else (220,228,223)
        name=name.replace('cw_sr_dark_','cw_sr_ui_').replace('cw_sr_muted_','cw_sr_ui_')
        path=ROOT/f'gfx/fonts/{name}.fnt'
        if name.startswith('cw_sr_ui_'):path=ROOT/f'gfx/fonts/COLDWAR_space_race/{name}.fnt'
        if not path.exists():path=GAME/f'gfx/fonts/{name}.fnt'
        source=path.read_text(encoding='utf-8-sig')
        self.height=int(re.search(r'lineHeight=(\d+)',source)[1])
        self.glyphs={}
        pages={}
        for i,file in re.findall(r'page id=(\d+) file="([^"]+)"',source):
            atlas=path.parent/file
            if not atlas.exists():atlas=path.with_suffix('.dds')
            pages[int(i)]=Image.open(atlas).convert('RGBA')
        for line in source.splitlines():
            if not line.startswith('char id='):continue
            fields={k:int(v) for k,v in re.findall(r'(\w+)=\s*(-?\d+)',line)}
            x,y,w,h=(fields[k] for k in ['x','y','width','height']);glyph=pages[fields['page']].crop((x,y,x+w,y+h))
            mask=glyph.getchannel('A')
            self.glyphs[fields['id']]=(mask,fields['xoffset'],fields['yoffset'],fields['xadvance'])

    def width(self,text):
        return sum(self.glyphs.get(ord(c),self.glyphs[32])[3] for c in re.sub('§.','',text))

    def draw(self,canvas,text,x,y,width,height,name,center=False):
        color=self.color;colors={'H':(208,183,124),'G':(169,198,173),'T':(145,193,197),'g':(164,183,188),'R':(212,149,132),'!':self.color}
        lines=[]
        for paragraph in text.split('\n'):
            if self.width(paragraph)<=width:lines.append(paragraph);continue
            line=''
            for word in paragraph.split(' '):
                if line and self.width(line+' '+word)>width:lines.append(line);line=word
                else:line+=((' ' if line else '')+word)
            lines.append(line)
        if len(lines)*self.height>height:OVERFLOWS.append({'element':name,'required_height':len(lines)*self.height,'height':height,'text':text})
        if canvas is None:return
        for row,line in enumerate(lines):
            if row*self.height>=height:break
            pen=x+(max(0,(width-self.width(line))//2) if center else 0);cy=y+row*self.height
            i=0
            while i<len(line):
                c=line[i]
                if c=='§' and i+1<len(line):color=colors.get(line[i+1],color);i+=2;continue
                mask,dx,dy,advance=self.glyphs.get(ord(c),self.glyphs[32])
                canvas.paste(color,(pen+dx,cy+dy),mask);pen+=advance;i+=1


FONTS={name:Font(name) for name in {V.first(v,'font',V.first(v,'buttonFont','"cw_sr_ui_13"')).strip('"') for k,op,v in WINDOW if k in ['instantTextBoxType','buttonType']}}
TEXTURES={}


def texture(path):
    if path not in TEXTURES:TEXTURES[path]=Image.open(ROOT/path).convert('RGBA')
    return TEXTURES[path]


def render(m,name,layout_only=False):
    canvas=None if layout_only else Image.open(ROOT/'gfx/interface/COLDWAR_space_race/panel.dds').convert('RGBA')
    for kind,op,body in WINDOW:
        if kind not in ['buttonType','instantTextBoxType','iconType']:continue
        element=V.first(body,'name').strip('"')
        if element in VISIBLE and not m.test(VISIBLE[element]):continue
        pos=V.first(body,'position');x=int(V.first(pos,'x'));y=int(V.first(pos,'y'))
        if kind=='instantTextBoxType':
            font=FONTS[V.first(body,'font').strip('"')]
            font.draw(canvas,resolve(V.first(body,'text'),m),x,y,int(V.first(body,'maxWidth')),int(V.first(body,'maxHeight')),element)
        else:
            sprite=SPRITES[V.first(body,'spriteType').strip('"')];im=texture(V.first(sprite,'texturefile').strip('"'))
            frames=int(V.first(sprite,'noOfFrames','1'));w=im.width//frames;h=im.height
            frame=2 if element in ENABLED and not m.test(ENABLED[element]) else 0
            if element in PROPERTIES:frame=max(0,min(frames-1,int(m.get(V.first(PROPERTIES[element],'frame')))-1))
            im=im.crop((w*frame,0,w*(frame+1),h))
            if canvas is not None:canvas.alpha_composite(im,(x,y))
            if kind=='buttonType':
                font=FONTS[V.first(body,'buttonFont').strip('"')];value=resolve(V.first(body,'buttonText'),m)
                line_height=font.height*(value.count('\n')+1)
                font.draw(canvas,value,x+6,y+max(0,(h-line_height)//2),w-12,h-2,element,True)
    if canvas is not None:canvas.convert('RGB').save(OUT/(name+'.png'))


def main():
    m=V.Machine(('USA','SOV','FRA'));m.init();m.c.flags.add('cw_sr_open')
    for tag,score in [('USA',105),('SOV',87),('FRA',24)]:
        m.c=m.countries[tag];m.init();m.put('cw_sr_prestige',score)
    m.c=m.countries['USA'];m.call('cw_sr_rank')
    for system,region,selected,name in [(1,2,16,'earth'),(2,8,27,'moon'),(3,14,84,'mars')]:
        m.put('cw_sr_tab',1);m.put('cw_sr_system',system);m.put('cw_sr_region',region);m.put('cw_sr_selected',selected);m.call('cw_sr_refresh');render(m,name)
    us=V.Machine(('USA',));us.init();us.put('treasury',120);us.put('political_power',30);us.c.flags.add('cw_sr_open');us.put('cw_sr_selected',47);us.call('cw_sr_rank');us.call('cw_sr_selected_map');us.call('cw_sr_refresh');render(us,'us-ground-redesign')
    for country in m.countries.values():country.variables['cw_sr_prestige']=V.D(0)
    m.c=m.countries['SOV'];m.put('treasury',61);m.call('cw_sr_rank');m.c.flags.add('cw_sr_open');m.put('cw_sr_selected',31);m.put('cw_sr_tab',1);m.call('cw_sr_selected_map');m.call('cw_sr_refresh');render(m,'reference-soviet-l1')
    for tab,name in [(2,'national-brief'),(3,'catalogue'),(4,'funding'),(5,'missions'),(6,'records'),(7,'news-empty')]:
        m.put('cw_sr_tab',tab);m.call('cw_sr_refresh');render(m,name)
    saudi=V.Machine(('SAU',));saudi.init();saudi.c.flags.add('cw_sr_open');saudi.put('cw_sr_tab',7);saudi.put('cw_sr_selected',27);saudi.put('cw_sr_p27_last_report',8);saudi.call('cw_sr_refresh');render(saudi,'saudi-lunar-bulletin')
    saudi.put('cw_sr_tab',1);saudi.c.flags.add('cw_sr_requirements_open');saudi.put('cw_sr_details_mode',0);saudi.call('cw_sr_refresh');render(saudi,'lunar-requirements')
    us.put('cw_sr_details_mode',1);us.c.flags.add('cw_sr_requirements_open');us.call('cw_sr_refresh');render(us,'national-effects')
    m.put('cw_sr_tab',1)
    for n,p in enumerate(V.DATA['programmes'],1):
        region=next(r for r in V.DATA['regions'] if r['id']==p['region']);r=V.DATA['regions'].index(region)+1
        same=[x for x in V.DATA['programmes'] if x['region']==p['region']]
        m.put('cw_sr_region',r);m.put('cw_sr_system',{'earth':1,'cislunar':2,'deep':3}[region['system']]);m.put('cw_sr_selected',n);m.put('cw_sr_page',same.index(p)//4);m.call('cw_sr_refresh');render(m,p['id'],True)
        m.c.flags.add('cw_sr_requirements_open');m.put('cw_sr_details_mode',0);render(m,p['id']+'-requirements',True);m.c.flags.discard('cw_sr_requirements_open')
    (OUT/'layout.json').write_text(json.dumps({'programmes_checked':84,'overflows':OVERFLOWS,'renderer':'Generated native GUI/GFX and installed bitmap-font atlas; layout reference, not a live game capture'},indent=2)+'\n')
    print(json.dumps({'previews':11,'programmes_checked':84,'overflows':len(OVERFLOWS)}))


if __name__=='__main__':main()
