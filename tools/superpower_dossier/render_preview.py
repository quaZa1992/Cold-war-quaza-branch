# IMPERIA COLD WAR — Compose current native GUI, sprites and font atlases for visual QA
"""An asset composition with fixture records, explicitly not a live game screenshot."""
import json
from pathlib import Path
import re
from PIL import Image
from behavior_tests import parser,ROOT,HERE
from test_treaties import TreatyModel as Model


def fields(rows):return {k:v for k,o,v in rows}


class Renderer:
    def __init__(self,side):
        self.model=Model();self.tag=side;self.ctx=(side,side,side);self.overflows=[]
        self.names={1:'United States',2:'Soviet Union',3:'Egypt',4:'Israel',5:'China',6:'France',7:'United Kingdom',8:'Cuba',-447:'Cairo'}
        self.strings={k:bytes(v,'utf-8').decode('utf-8').replace('\\n','\n') for k,v in re.findall(r'^\s*(\w+):(?:\d+)?\s*"(.*)"\s*$',(ROOT/'localisation/english/ICW_superpower_dossier_l_english.yml').read_text(encoding='utf-8-sig'),re.M)}
        self.defined={fields(b)['name']:b for p in (ROOT/'common/scripted_localisation').glob('ICW_superpower*.txt') for k,o,b in parser.parse(p.read_text()) if k=='defined_text'}
        self.sprites={fields(b)['name']:str(fields(b)['texturefile']).strip('"') for k,o,v in parser.parse((ROOT/'interface/ICW_superpower_dossier.gfx').read_text()) if k=='spriteTypes' for k,o,b in v}
        self.fonts={}
        for p in (ROOT/'gfx/fonts/superpower_dossier').glob('*.fnt'):
            s=p.read_text();height=int(re.search(r'lineHeight=(\d+)',s)[1]);glyphs={}
            for line in s.splitlines():
                if line.startswith('char '):
                    f={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)};glyphs[f['id']]=f
            self.fonts[p.stem]=(Image.open(p.with_suffix('.dds')).convert('RGBA'),height,glyphs)
        from typography import SPECS
        self.colours={'icsd_'+k:'#'+v[4] for k,v in SPECS.items()}
        # Populate the actual emitted cache and selection effects with the approved example sequence.
        for actor,target,kind in [(2,3,1),(1,4,1),(1,6,2),(2,7,3),(1,8,4)]:
            self.model.packet(actor=actor,target=target,kind=kind,date=100);self.model.call('icsd_publish_live')
        self.model.v[side]['icsd_tab']=1;self.model.call('icsd_build_view',side)
        self.model.call('icsd_select_0',side)
        self.model.v[side]['icsd_response_target']=4 if side=='USA' else 3
        scripted=parser.parse((ROOT/'common/scripted_guis/ICW_superpower_dossier.txt').read_text())[0][2]
        self.visible=fields(next(b for k,o,b in scripted if k=='icsd_main'))['triggers']
        self.triggers=fields(self.visible)

    def resolve(self,value,depth=0):
        if depth>12:return value
        value=value.strip('"')
        if value in self.strings:value=self.strings[value]
        def sub(m):
            key=m[1]
            if key.startswith('?'):
                key=key[1:];key,_,fmt=key.partition('|')
                if key.endswith('.GetName'):
                    return self.names.get(self.model.value(key[:-8],self.ctx),'Country')
                if 'GetDateString' in key:return '1 January 1970'
                return str(int(self.model.value(key,self.ctx)))
            if key in self.defined:
                for k,o,b in self.defined[key]:
                    if k!='text':continue
                    f=fields(b)
                    if 'trigger' not in f or self.model.test(f['trigger'],self.ctx):return self.resolve(f['localization_key'],depth+1)
                return ''
            return self.resolve(self.strings.get(key,key),depth+1)
        new=re.sub(r'\[([^]]+)\]',sub,value)
        return self.resolve(new,depth+1) if '[' in new and new!=value else new

    def width(self,text,font):return sum(self.fonts[font][2].get(ord(c),{}).get('xadvance',0) for c in text)

    def draw_text(self,canvas,text,font,x,y,width,height,center=False):
        if not text:return
        atlas,lineheight,glyphs=self.fonts[font];lines=[]
        for paragraph in text.split('\n'):
            line=''
            for word in paragraph.split(' '):
                if self.width(word,font)>width:self.overflows.append(dict(text=word,width=width,reason='unbroken word exceeds field'))
                candidate=(line+' '+word).strip()
                if line and self.width(candidate,font)>width:lines.append(line);line=word
                else:line=candidate
            lines.append(line)
        if len(lines)*lineheight>height:self.overflows.append(dict(text=text,width=width,height=height,lines=len(lines),line_height=lineheight))
        layer=Image.new('RGBA',(max(1,width),max(1,height)),(0,0,0,0));top=max(0,(height-len(lines)*lineheight)//2) if center else 0
        for number,line in enumerate(lines):
            pos=max(0,(width-self.width(line,font))//2) if center else 0
            for char in line:
                g=glyphs.get(ord(char))
                if not g:continue
                tile=atlas.crop((g['x'],g['y'],g['x']+g['width'],g['y']+g['height']))
                tint=Image.new('RGBA',tile.size,self.colours[font]);tint.putalpha(tile.getchannel('A'))
                layer.alpha_composite(tint,(pos+g['xoffset'],top+number*lineheight+g['yoffset']))
                pos+=g['xadvance']
        canvas.alpha_composite(layer,(x,y))

    def elements(self,canvas,rows,offset=(0,0)):
        for kind,o,body in rows:
            if kind not in ('containerWindowType','instantTextboxType','iconType','buttonType'):continue
            f=fields(body);name=f['name'].strip('"');test=self.triggers.get(name+'_visible')
            if test and not self.model.test(test,self.ctx):continue
            pos=fields(f.get('position',[]));x=offset[0]+int(pos.get('x',0));y=offset[1]+int(pos.get('y',0))
            if kind=='containerWindowType':self.elements(canvas,body,(x,y));continue
            sprite=str(f.get('spriteType',f.get('quadTextureSprite','')))
            size=(0,0)
            if sprite:
                texture=Image.open(ROOT/self.sprites[sprite]).convert('RGBA');size=texture.size;canvas.alpha_composite(texture,(x,y))
            if kind=='instantTextboxType':
                value=self.resolve(f['text']);typeface=f['font'].strip('"');width=int(f['maxWidth'])
                if f.get('format')=='right':x+=max(0,width-self.width(value,typeface));width=max(1,self.width(value,typeface))
                self.draw_text(canvas,value,typeface,x,y,width,int(f['maxHeight']))
            elif kind=='buttonType' and f.get('buttonText','""')!='""':
                self.draw_text(canvas,self.resolve(f['buttonText']),f['buttonFont'],x+7,y,max(1,size[0]-14),size[1],True)

    def render(self):
        gui=parser.parse((ROOT/'interface/ICW_superpower_dossier.gui').read_text())[0][2]
        main=next(b for k,o,b in gui if k=='containerWindowType' and fields(b)['name']=='"icsd_main_window"')
        canvas=Image.new('RGBA',(790,794),(0,0,0,0));self.elements(canvas,main)
        return canvas


def main():
    folder=HERE/'previews';folder.mkdir(exist_ok=True);report={}
    for side in ('USA','SOV'):
        def save(renderer,name):
            renderer.overflows=[];renderer.render().save(folder/(name+'.png'));report[name]=renderer.overflows
        renderer=Renderer(side);save(renderer,side.lower())
        m=renderer.model;m.v[side]['icsd_tab']=2;m.call('icwt_select_1',side);m.call('icwt_display',side);save(renderer,side.lower()+'-historical-proposal')
        m.call('icwt_open_custom',side);m.call('icwt_display',side);save(renderer,side.lower()+'-custom-editor')
        m=renderer.model;m.v[side].update(icsd_tab=2,icwt_page=1);m.call('icwt_select_5',side);m.call('icwt_display',side);save(renderer,side.lower()+'-catalog')
        m.call('icwt_edit_5',side);m.v[side].update(icwt_edit_sanctions=5,icwt_edit_trade=2,icwt_edit_investment=1,icwt_edit_duration=365)
        m.call('icwt_display',side);save(renderer,side.lower()+'-terms')
        m.v[side]['icwt_screen']=2;m.v[side].update(icwt_edit_usa_target=4,icwt_edit_sov_target=3);m.a[side]['icwt_edit_invites']=[6,7];m.call('icwt_display',side);save(renderer,side.lower()+'-parties')
        m.v[side]['icwt_screen']=3;m.call('icwt_display',side);save(renderer,side.lower()+'-review')
        m.call('icwt_send_5',side);other='SOV' if side=='USA' else 'USA';m.call('icwt_review_5',other);m.call('icwt_sign_5',other)
        m.v[side].update(icsd_tab=3,icwt_register=1,icwt_screen=0);m.call('icwt_display',side);save(renderer,side.lower()+'-register')
        m.call('icwt_leave_5',side);m.call('icwt_display',side);save(renderer,side.lower()+'-withdrawn')
        # Current programme editor/review geometry, with real emitted clause fields.
        m.call('icwt_edit_9',side);m.flags['USA'].add('icwt_programme_1_unlocked');m.v[side]['icwt_edit_programme']=1
        m.v[side].update(icsd_tab=2,icwt_screen=1);m.call('icwt_display',side);save(renderer,side.lower()+'-programme-terms')
        m.v[side]['icwt_screen']=3;m.call('icwt_display',side);save(renderer,side.lower()+'-programme-review')
        # All twelve receipts exercise the four-row final register page and long titles.
        renderer=Renderer(side);m=renderer.model
        for n in range(1,13):
            m.call(f'icwt_edit_{n}',side);m.v[side]['icwt_edit_regional']=0
            m.call(f'icwt_send_{n}',side);other='SOV' if side=='USA' else 'USA'
            m.call(f'icwt_review_{n}',other);m.call(f'icwt_sign_{n}',other)
        m.v[side].update(icsd_tab=3,icwt_register=1,icwt_screen=0,icwt_register_offset=8,icwt_template=12)
        m.call('icwt_display',side);save(renderer,side.lower()+'-register-last-page')
    (folder/'NOTICE.md').write_text('IMPERIA COLD WAR: compositions of current native GUI geometry, DDS sprites and font glyphs using illustrative fixture records. Not live game screenshots. Approved visual reference: intelligence-dossiers.html. Asset provenance: ../art_notice.json.\n',encoding='utf-8')
    (HERE/'presentation-report.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',scope='Native asset composition and text overflow inspection. Not native UI execution.',overflows=report),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
