# IMPERIA CW — Cold War: Guest Worker Administration
"""Render emitted native controls with actual bitmap-font advances and flags.

Offline layout QA, not an engine screenshot. Native text wrapping is approximated
at spaces; lines, enabled/visible state, sprites and values use shipped inputs.
"""
from pathlib import Path
from functools import lru_cache
import json
import re
from PIL import Image
import validate as V
import validate_diaspora as T
from test_ministry import Machine

ROOT=V.ROOT
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')


@lru_cache(None)
def font(name):
    base=ROOT/'gfx/fonts'/name
    if not base.with_suffix('.fnt').exists():base=GAME/'gfx/fonts'/name
    raw=base.with_suffix('.fnt').read_text(encoding='utf-8-sig')
    chars={}
    for line in raw.splitlines():
        if line.startswith('char id='):
            row={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)};chars[row['id']]=row
    common=next(l for l in raw.splitlines() if l.startswith('common '))
    height=int(re.search(r'lineHeight=(\d+)',common)[1])
    return chars,Image.open(base.with_suffix('.dds')).convert('RGBA'),height


def receiving():
    m=Machine(*T.load())
    m.root.states[0].population=V.D(20000000)
    m.root.variables.update(gdp_total=V.D(200),population_total=V.D(200),gw_selected_origin=V.D(2))
    m.root.ideas.discard('mdcw_ni_overseas_employment_programme')
    m.call('mdcw_gw_ledger_initialize')
    for tag,amount,reg,house,protect in [('B',500,300,200,300),('C',250,100,50,50),('D',150,0,0,50),('E',100,0,0,0)]:
        if tag not in m.countries:m.countries[tag]=V.Country(tag)
        m.countries[tag].ideas.add('mdcw_ni_overseas_employment_programme')
        m.root.temporary['gw_lookup_origin']=V.D(list(m.countries).index(tag)+1)
        m.call('mdcw_gw_ensure_origin');i=int(m.get('gw_index'))
        for k,v in [('stock',amount),('registered',reg),('housed',house),('protected',protect)]:m.root.variables[f'gw_{k}^{i}']=V.D(v)
    m.call('mdcw_gw_recount_ledger');m.root.variables['gw_project_choice']=V.D(2);m.call('mdcw_gw_start_project')
    m.root.variables['health_gain']=V.D('.2')*(1+m.get('mdcw_gw_health_cost'))
    m.root.variables['bureaucracy_gain']=V.D('.1')*(1+m.get('mdcw_gw_bureaucracy_cost')+V.D('.05'))
    m.call('mdcw_gw_update_cost_receipt');m.call('mdcw_gw_refresh_dashboard')
    names={1:'German Democratic Republic',2:'Portugal',3:'Algeria',4:'Turkey',5:'Yugoslavia'}
    flags={1:'DDR_communism',2:'POR_neutrality',3:'ALG_neutrality',4:'TUR_democratic',5:'YUG_communism'}
    return m,names,flags


def sending():
    m=Machine(*T.load());m.root.ideas={'mdcw_ni_overseas_employment_programme'}
    m.root.variables.update(gw_abroad_k=V.D(100),mdcw_gw_remittance_pool_m=V.D(400),gw_ui_host=V.D(2))
    m.root.variables.update(mdcw_gw_net_emigration_k=V.D(100),gdp_per_capita=V.D(2))
    m.origin.variables['gdp_per_capita']=V.D(5)
    m.execute([('add_to_array','=',[('gw_hosts','=','2')])])
    m.origin.variables.update({'gw_origins^num':V.D(1),'gw_origins^0':V.D(1),'gw_stock^0':V.D(100),
                              'gw_registered^0':V.D(50),'gw_housed^0':V.D(40),'gw_protected^0':V.D(70)})
    m.call('mdcw_gw_ministry_counters')
    return m,{1:'Portugal',2:'German Democratic Republic'},{1:'POR_neutrality',2:'DDR_communism'}


def render(m,names,flags,name):
    loc={};defined={}
    for p in (ROOT/'localisation/english').glob('mdcw_*english.yml'):
        loc.update({k:json.loads(v) for k,v in re.findall(r'^ (\S+):\d+ (".*")$',p.read_text(encoding='utf-8-sig'),re.M)})
    for p in (ROOT/'common/scripted_localisation').glob('mdcw_*txt'):
        for key,_,v in V.read_script(p.relative_to(ROOT).as_posix()):
            if key=='defined_text':defined[V.first(v,'name')]=v
    def text(key,depth=0):
        if depth>10:raise AssertionError('Recursive localisation: '+key)
        if key in defined:
            for entry in V.values(defined[key],'text'):
                if m.test(V.first(entry,'trigger',[])):
                    return text(V.first(entry,'localization_key'),depth+1)
        value=loc.get(key,key)
        def variable(match):
            expr=match[1]
            if expr.endswith('.GetName'):return names.get(int(m.get(expr[:-8])),'Unknown')
            var,_,fmt=expr.partition('|');n=m.get(var)
            if fmt.startswith('%'):return f'{n*100:.{int(fmt[1:] or 0)}f}%'
            return f'{n:,.{int(fmt or 0)}f}'
        value=re.sub(r'\[\?([^\]]+)\]',variable,value)
        value=re.sub(r'\[([^\]]+)\]',lambda q:text(q[1],depth+1),value)
        return re.sub(r'§.','',value).replace('$$','$')
    gui=V.first(V.first(V.read_script('interface/mdcw_diaspora.gui'),'guiTypes',[]),'containerWindowType',[])
    body=V.first(V.first(V.read_script('common/scripted_guis/mdcw_diaspora_gui.txt'),'scripted_gui',[]),'mdcw_gw_dashboard',[])
    visible=dict((k,v) for k,_,v in V.first(body,'triggers',[]));props=dict((k,v) for k,_,v in V.first(body,'properties',[]))
    sprites={V.first(v,'name').strip('"'):v for k,_,v in V.first(V.read_script('interface/mdcw_diaspora.gfx'),'spriteTypes',[])}
    picture=Image.new('RGBA',(510,740));overflows=[];boxes=[]
    def draw(value,x,y,fname,width,height,align='left',color=(31,37,29,255),control=''):
        chars,atlas,lineheight=font(fname)
        advance=lambda s:sum(chars.get(ord(c),chars[32])['xadvance'] for c in s)
        lines=[]
        for raw in value.splitlines() or ['']:
            line=''
            for word in raw.split(' '):
                test=(line+' '+word).strip()
                if advance(test)>width and line:lines.append(line);line=word
                else:line=test
            lines.append(line)
        if len(lines)*lineheight>height:overflows.append({'control':control,'text':value,'height':len(lines)*lineheight,'available':height})
        for i,line in enumerate(lines):
            w=advance(line)
            if w>width:overflows.append({'control':control,'text':line,'width':w,'available':width})
            dx=x+(width-w if align=='right' else ((width-w)//2 if align=='center' else 0))
            for c in line:
                ch=chars.get(ord(c),chars[32]);glyph=atlas.crop((ch['x'],ch['y'],ch['x']+ch['width'],ch['y']+ch['height']))
                ink=Image.new('RGBA',glyph.size,color);ink.putalpha(glyph.getchannel('A'))
                picture.alpha_composite(ink,(int(dx+ch['xoffset']),int(y+i*lineheight+ch['yoffset'])))
                dx+=ch['xadvance']
        boxes.append({'control':control,'text':value,'x':x,'y':y,'width':width,'height':len(lines)*lineheight})
    for kind,_,c in gui:
        if not isinstance(c,list) or V.first(c,'name') is None:continue
        key=V.first(c,'name').strip('"')
        if key+'_visible' in visible and not m.test(visible[key+'_visible']):continue
        pos=V.first(c,'position',[]);x=int(V.first(pos,'x','0'));y=int(V.first(pos,'y','0'))
        if kind=='instantTextBoxType':
            fname=V.first(c,'font').strip('"')
            draw(text(V.first(c,'text').strip('"')),x,y,fname,int(V.first(c,'maxWidth')),int(V.first(c,'maxHeight')),V.first(c,'format'),
                 (241,232,208,255) if not fname.startswith('hoi4_typewriter') else (31,37,29,255),key)
        elif kind=='buttonType' and V.first(c,'quadTextureSprite').strip('"')=='GFX_flag_small2':
            expr=V.first(props[key],'image').strip('"')[2:-9]
            # [?gw_origin.GetFlag] -> its native country flag, using the fixture identity.
            identity=int(m.get(expr))
            filename=flags[identity]+'.tga';path=ROOT/'gfx/flags'/filename
            if not path.exists():path=GAME/'gfx/flags'/filename
            image=Image.open(path).convert('RGBA').resize((41,26),Image.Resampling.LANCZOS)
            picture.alpha_composite(image,(x,y))
        elif kind in ('buttonType','iconType'):
            sprite=V.first(c,'quadTextureSprite' if kind=='buttonType' else 'spriteType').strip('"');definition=sprites[sprite]
            image=Image.open(ROOT/V.first(definition,'texturefile').strip('"')).convert('RGBA');frames=int(V.first(definition,'noOfFrames','1'));w=image.width//frames
            frame=int(m.get(V.first(props.get(key,[]),'frame','1')))-1 if V.first(props.get(key,[]),'frame') else 0
            picture.alpha_composite(image.crop((frame*w,0,(frame+1)*w,image.height)),(x,y))
            if kind=='buttonType':
                value=text(V.first(c,'buttonText').strip('"'));fname=V.first(c,'buttonFont').strip('"')
                enabled=key+'_click_enabled' not in visible or m.test(visible[key+'_click_enabled'])
                color=((241,232,208,255) if enabled else (181,181,177,255)) if not fname.startswith('hoi4_typewriter') else (31,37,29,255)
                draw(value,x,y+6,fname,w,image.height-6,'center',color,key)
    path=ROOT/'docs/guest_workers_ministry'/f'{name}.png';path.parent.mkdir(parents=True,exist_ok=True);picture.save(path)
    return {'file':str(path.relative_to(ROOT)),'size':[510,740],'text_overflows':overflows,'visible_text':boxes}


def main():
    reports=[]
    for tab,name in [(0,'overview'),(1,'communities'),(2,'recruitment')]:
        m,names,flags=receiving()
        if tab==2:m.call('mdcw_gw_ministry_list_partners')
        m.root.variables['gw_ui_tab']=V.D(tab)
        reports.append(render(m,names,flags,name))
        # IMPERIA CW — Cold War: Show the actual dirty-refreshed pending state.
        if tab==2:
            m.call('mdcw_gw_ui_recruit_25000')
            reports.append(render(m,names,flags,'recruitment_pending'))
        if tab==1:
            m.root.flags['gw_ui_return_open']=V.D(0);reports.append(render(m,names,flags,'repatriation'))
    m,names,flags=sending();reports.append(render(m,names,flags,'sender_overview'))
    m.root.flags['gw_ui_show_abroad']=V.D(0);m.root.variables['gw_ui_tab']=V.D(1);m.call('mdcw_gw_ministry_host_page')
    reports.append(render(m,names,flags,'abroad'))
    # IMPERIA CW — Cold War: Preview the new policy page in both national roles.
    m.call('mdcw_dp_prepare_selected');m.root.variables['gw_ui_tab']=V.D(3)
    reports.append(render(m,names,flags,'sender_policies'))
    m.call('mdcw_dp_request_trade')
    reports.append(render(m,names,flags,'policy_pending'))
    m.advance_days(1)
    offer=next(e for e in m.open_events if e[1]=='mdcw_dp.1')
    m.choose(offer,0);m.call('mdcw_dp_prepare_selected')
    reports.append(render(m,names,flags,'active_policies'))
    m,names,flags=receiving();m.call('mdcw_gw_ministry_host_page');m.call('mdcw_dp_prepare_selected');m.root.variables['gw_ui_tab']=V.D(3)
    reports.append(render(m,names,flags,'receiver_policies'))
    m,names,flags=receiving();m.root.variables.update(gw_unrecorded_k=V.D(25),gw_ui_tab=V.D(0))
    reports.append(render(m,names,flags,'legacy_overview'))
    m,names,flags=receiving()
    for c in m.countries.values():c.ideas.discard('mdcw_ni_overseas_employment_programme')
    m.call('mdcw_gw_ministry_list_partners');m.root.variables['gw_ui_tab']=V.D(2)
    reports.append(render(m,names,flags,'empty_recruitment'))
    result={'kind':'Offline native-asset layout proof, not HOI4 execution','views':reports}
    (ROOT/'docs/guest_workers_ministry/layout.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    # Preserve the established entry point used by project documentation.
    Image.open(ROOT/reports[0]['file']).save(ROOT/'docs/guest_workers_dashboard_preview.png')
    (ROOT/'docs/guest_workers_dashboard_layout.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    problems=[x for r in reports for x in r['text_overflows']]
    print(json.dumps({'views':len(reports),'overflows':problems},indent=2))
    return bool(problems)


if __name__=='__main__':raise SystemExit(main())
