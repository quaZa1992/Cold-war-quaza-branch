# IMPERIA COLD WAR — COMECON native dossier textures and provenance
import hashlib
import random
from PIL import Image, ImageDraw, ImageFont
from build import *

def paper_surface(size,colour,seed,grain=2):
    rng=random.Random(seed);base=tuple(int(colour.lstrip('#')[i:i+2],16) for i in (0,2,4));pixels=[]
    for _ in range(size[0]*size[1]):
        delta=rng.randint(-grain,grain)
        pixels.append(tuple(max(0,min(255,c+delta)) for c in base)+(255,))
    result=Image.new('RGBA',size);result.putdata(pixels)
    fibres=Image.new('RGBA',size,(0,0,0,0));dr=ImageDraw.Draw(fibres)
    for _ in range(size[0]*size[1]//260):
        x=rng.randrange(size[0]);y=rng.randrange(size[1]);length=rng.randint(2,10)
        dr.line((x,y,min(size[0]-1,x+length),y),fill=(97,74,43,rng.randint(5,13)))
    result.alpha_composite(fibres);return result

def build_assets():
    folder=ROOT/'gfx/interface/comecon';folder.mkdir(parents=True,exist_ok=True)
    donor=ROOT/'gfx/interface/help_gui/EU_help_button_custom.dds'
    frame=Image.open(donor).convert('RGBA')
    emblem=Image.open(HERE/'user-emblem.png').convert('RGBA')
    white=emblem.convert('L').point(lambda x:255 if x>245 else 0)
    box=white.getbbox();glyph=white.crop(box);glyph.thumbnail((31,31),Image.Resampling.LANCZOS)
    overlay=Image.new('RGBA',frame.size,(0,0,0,0));draw=ImageDraw.Draw(overlay)
    draw.ellipse((3,3,42,42),fill=(166,22,28,255))
    glyph_image=Image.new('RGBA',glyph.size,(255,252,241,255));glyph_image.putalpha(glyph)
    overlay.alpha_composite(glyph_image,((46-glyph.width)//2,(46-glyph.height)//2))
    frame.alpha_composite(overlay);frame.save(folder/'toolbar.dds');frame.resize((184,184),Image.Resampling.NEAREST).save(ROOT/'docs/design/comecon/toolbar-preview.png')
    board='#d4c5aa';paper='#f6f1e6';ink='#302c27';rule='#c9bcaa';red='#913c37'
    art=paper_surface((900,580),board,1970,3);d=ImageDraw.Draw(art)
    # Manila spine, pressed folds, inset seams and two small staple marks.
    d.rectangle((0,0,11,579),fill='#aa9270');d.line((12,1,12,578),fill='#ecdcc0');d.line((16,2,16,577),fill='#b39c7b')
    d.line((20,108,880,108),fill='#b6a083');d.line((20,109,880,109),fill='#e3d3b6')
    for x in (25,48):
        d.line((x+1,10,x+16,10),fill='#8a745c',width=3);d.line((x,8,x+15,8),fill='#716e67',width=2);d.line((x+1,7,x+14,7),fill='#d4d1c4')
    # Several separate sheets remain visible along the right and lower edges.
    d.rectangle((225,159,884,536),fill='#9d876b');d.rectangle((224,158,882,534),fill='#e4d8c2',outline='#ac987a')
    art.alpha_composite(paper_surface((659,377),paper,1949,2),(222,156));d=ImageDraw.Draw(art)
    d.rectangle((222,156,880,532),outline='#b7a68e');d.line((240,498,864,498),fill='#c9bcaa')
    d.polygon(((868,156),(880,168),(868,168)),fill='#d9cdb6');d.line((868,156,868,168,880,168),fill='#bcae96')
    # Light pressure creases and edge wear leave the writing area unobstructed.
    wear=Image.new('RGBA',art.size,(0,0,0,0));wd=ImageDraw.Draw(wear)
    wd.line((208,119,208,566),fill=(95,66,35,22),width=1);wd.line((210,119,210,566),fill=(255,245,218,35),width=1)
    for radius in (30,31):wd.arc((-20,494,40+radius,554+radius),38,140,fill=(104,71,33,11),width=1)
    rng=random.Random(1991)
    for _ in range(130):
        x=rng.choice([rng.randrange(0,5),rng.randrange(895,900)]);y=rng.randrange(580)
        wd.line((x,y,x+1,y+rng.randrange(1,5)),fill=(78,54,26,35))
    art.alpha_composite(wear);d=ImageDraw.Draw(art);d.rectangle((0,0,899,579),outline='#a48d6d')
    art.save(folder/'dossier.dds')
    emblem.resize((74,49),Image.Resampling.LANCZOS).save(folder/'header-logo.dds')
    symbols=Image.new('RGBA',(48*len(PROJECTS),48),(0,0,0,0))
    for index,p in enumerate(PROJECTS):
        symbol=Image.new('RGBA',(48,48),(0,0,0,0));symbol.alpha_composite(emblem.resize((48,32),Image.Resampling.LANCZOS),(0,0))
        source=HERE/'source-art'/('symbol-'+DATA['catalogue'][p].get('icon',p)+'.png')
        tool=Image.open(source).convert('RGBA');tool.thumbnail((36,36),Image.Resampling.LANCZOS);symbol.alpha_composite(tool,(48-tool.width,48-tool.height))
        symbols.alpha_composite(symbol,(index*48,0))
    symbols.save(folder/'programme-symbols.dds')
    large=Image.new('RGBA',(70*len(PROJECTS),75),(0,0,0,0))
    for index,p in enumerate(PROJECTS):
        symbol=Image.new('RGBA',(70,75),(0,0,0,0));symbol.alpha_composite(emblem.resize((70,47),Image.Resampling.LANCZOS),(0,0))
        source=HERE/'source-art'/('symbol-'+DATA['catalogue'][p].get('icon',p)+'.png')
        tool=Image.open(source).convert('RGBA');tool.thumbnail((54,54),Image.Resampling.LANCZOS);symbol.alpha_composite(tool,(70-tool.width,75-tool.height));large.alpha_composite(symbol,(index*70,0))
    large.save(folder/'programme-large.dds')
    sprites=[MARK+' native GUI art; donor credits in tools/comecon/ART_NOTICE.md','spriteTypes = {',
      'spriteType = { name = GFX_cc_toolbar texturefile = "gfx/interface/comecon/toolbar.dds" legacy_lazy_load = no }',
      'spriteType = { name = GFX_cc_emblem texturefile = "gfx/interface/comecon/toolbar.dds" }',
      f'spriteType = {{ name = GFX_cc_project_symbols texturefile = "gfx/interface/comecon/programme-symbols.dds" noOfFrames = {len(PROJECTS)} }}',
      f'spriteType = {{ name = GFX_cc_project_large texturefile = "gfx/interface/comecon/programme-large.dds" noOfFrames = {len(PROJECTS)} }}',
      'spriteType = { name = GFX_cc_header_logo texturefile = "gfx/interface/comecon/header-logo.dds" }',
      'spriteType = { name = GFX_idea_cc_emblem texturefile = "gfx/interface/comecon/toolbar.dds" }',
      'spriteType = { name = GFX_cc_dossier texturefile = "gfx/interface/comecon/dossier.dds" }']
    def texture(name,images,button=False):
        w,h=images[0].size;strip=Image.new('RGBA',(w*len(images),h),(0,0,0,0))
        for i,im in enumerate(images):strip.alpha_composite(im,(i*w,0))
        strip.save(folder/(name+'.dds'))
        sprites.append(f'spriteType = {{ name = GFX_cc_{name} texturefile = "gfx/interface/comecon/{name}.dds" noOfFrames = {len(images)}'+(' effectFile = "gfx/FX/buttonstate.lua"' if button else '')+' }')
    offer_icons=[]
    for p,o in OFFERS:
        source=HERE/'source-art'/('symbol-'+o.get('icon',DATA['catalogue'][p].get('icon',p))+'.png')
        mark=Image.open(source).convert('RGBA');mark.thumbnail((31,31),Image.Resampling.LANCZOS)
        tile=Image.new('RGBA',(31,31),(0,0,0,0));tile.alpha_composite(mark,((31-mark.width)//2,(31-mark.height)//2));offer_icons.append(tile)
    texture('offer_symbols',offer_icons)
    funding=[]
    for value in range(0,101,5):
        im=Image.new('RGBA',(670,18),(0,0,0,0));dr=ImageDraw.Draw(im);dr.rounded_rectangle((0,7,669,11),radius=2,fill='#c9bcaa')
        x=round(6+657*value/100)
        dr.rounded_rectangle((0,7,x,11),radius=2,fill=red);dr.ellipse((x-6,3,x+6,15),fill=red);funding.append(im)
    texture('funding',funding)
    for width in (104,135,112):
        states=[]
        for fill in ('#bda98c',paper):
            im=Image.new('RGBA',(width,36),(0,0,0,0));dr=ImageDraw.Draw(im);dr.rounded_rectangle((0,0,width-1,41),radius=6,fill=fill,outline='#b4a084',width=1);states.append(im)
        texture('tab_'+str(width),states,True)
    states=[]
    for selected in (False,True):
        im=paper_surface((84,36),paper if selected else board,1971+selected);dr=ImageDraw.Draw(im);dr.rectangle((0,0,83,35),outline=red if selected else '#b4a084');states.append(im)
    texture('register_tab',states,True)
    states=[]
    for selected in (False,True):
        im=paper_surface((182,50),paper if selected else board,1972+selected);dr=ImageDraw.Draw(im);dr.line((0,49,181,49),fill='#bcab91')
        if selected:dr.rectangle((0,0,2,49),fill=red)
        states.append(im)
    texture('register_row',states,True)
    for width in (300,622):
        im=Image.new('RGBA',(width,32),(0,0,0,0));dr=ImageDraw.Draw(im);dr.line((0,31,width-1,31),fill='#aa9780');dr.polygon(((width-13,12),(width-7,12),(width-10,16)),fill=ink);texture('field_'+str(width),[im],True)
    states=[]
    for selected in (False,True):
        im=paper_surface((622,76),'#eee0d6' if selected else '#f2eadc',1973+selected);dr=ImageDraw.Draw(im);dr.rectangle((0,0,621,75),outline=red if selected else rule);dr.ellipse((10,13,20,23),outline=red if selected else '#736b60')
        if selected:dr.ellipse((13,16,17,20),fill=red)
        states.append(im)
    texture('offer',states,True)
    for width in (622,):texture('line_'+str(width),[Image.new('RGBA',(width,1),rule)])
    for width in (60,80,120,140,150,240,156):
        primary=width==156;im=Image.new('RGBA',(width,32),red if primary else '#eee4d3');dr=ImageDraw.Draw(im);dr.rectangle((0,0,width-1,31),outline=red if primary else '#ad9b82');texture(('primary_' if primary else 'action_')+str(width),[im],True)
    for name,size,fill in [('tiny_button',(26,28),'#eee4d3'),('choice_row',(350,32),paper),('scale_row',(326,36),paper),('picker',(380,270),paper),('scale_picker',(342,124),paper)]:
        im=Image.new('RGBA',size,fill);dr=ImageDraw.Draw(im)
        if name not in ('choice_row','scale_row'):dr.rectangle((0,0,size[0]-1,size[1]-1),outline='#b7a68e')
        texture(name,[im],name not in ('picker','scale_picker'))
    close=Image.new('RGBA',(25,25),(0,0,0,0));dr=ImageDraw.Draw(close);dr.line((6,6,18,18),fill=red,width=2);dr.line((18,6,6,18),fill=red,width=2);texture('close',[close],True)
    stamps=[]
    for title,subtitle in [('WORKING COPY','FOR COUNCIL REVIEW'),('APPROVED','COUNCIL AGREEMENT')]:
        im=Image.new('RGBA',(680,248),(0,0,0,0));dr=ImageDraw.Draw(im);dr.rectangle((2,2,677,245),outline=red,width=6)
        dr.text((340,65),title,font=ImageFont.truetype('C:/Windows/Fonts/cour.ttf',56),fill=red,anchor='mm');dr.text((340,157),subtitle,font=ImageFont.truetype('C:/Windows/Fonts/cour.ttf',40),fill=red,anchor='mm')
        im=im.rotate(4,resample=Image.Resampling.BICUBIC,expand=True);im.thumbnail((180,80),Image.Resampling.LANCZOS);out=Image.new('RGBA',(180,80),(0,0,0,0));out.alpha_composite(im,((180-im.width)//2,(80-im.height)//2));stamps.append(out)
    texture('stamp',stamps)
    tile=paper_surface((148,74),'#eee4d3',1976,1);dr=ImageDraw.Draw(tile);dr.rectangle((0,0,147,73),outline=rule)
    texture('ballot_tile',[tile])
    seal=Image.new('RGBA',(148,74),(0,0,0,0));dr=ImageDraw.Draw(seal);dr.rectangle((0,0,147,73),outline=red,width=2);dr.line((132,8,136,12,142,4),fill=red,width=2)
    texture('ballot_seal',[seal])
    row=paper_surface((622,56),paper,1977,1);dr=ImageDraw.Draw(row);dr.line((0,55,621,55),fill=rule)
    texture('agenda_row',[row],True)
    selected=Image.new('RGBA',(622,56),(0,0,0,0));dr=ImageDraw.Draw(selected);dr.rectangle((0,0,621,55),outline=red,width=2)
    texture('agenda_selection',[selected])
    for name,size,colour in [('scroll_bg',(10,18),paper),('scroll_track',(4,4),paper),('scroll_grip',(8,24),'#b9a78c'),('scroll_up',(8,8),'#b9a78c'),('scroll_down',(8,8),'#b9a78c')]:texture(name,[Image.new('RGBA',size,colour)])
    from fonts import build_fonts
    sprites += ['}',build_fonts()]
    write('interface/ICW_COMECON.gfx','\n'.join(sprites))
    # Pick a deterministic existing railway junction per state. The engine checks capacity again.
    railway=ROOT/'map/railways.txt';degree={};neighbours={}
    for line in railway.read_text(encoding='utf-8-sig').splitlines():
        raw=line.split('#',1)[0].split()
        if len(raw)>2:
            try:points=list(map(int,raw[2:]))
            except ValueError:continue
            for pid in points:degree[pid]=degree.get(pid,0)+1
            for a,b in zip(points,points[1:]):
                neighbours.setdefault(a,set()).add(b);neighbours.setdefault(b,set()).add(a)
    candidates={}
    for p in (ROOT/'history/states').glob('*.txt'):
        source=re.sub(r'#[^\n]*','',p.read_text(encoding='utf-8-sig',errors='replace'))
        state=re.search(r'\bid\s*=\s*(\d+)',source);provinces=re.search(r'\bprovinces\s*=\s*\{([^}]+)\}',source,re.S)
        if not state or not provinces:continue
        values=[int(x) for x in re.findall(r'\d+',provinces.group(1)) if int(x) in degree]
        if values:candidates[int(state.group(1))]=sorted(set(values),key=lambda pid:(-degree[pid],pid))[:8]
    trig=[MARK+' existing rail junctions and native province capacity','cc_hub_site_valid = { OR = {']
    effect=[MARK+' deterministic rail-linked hub construction','cc_build_hub = {']
    preview=[MARK+' prospective hub reward at the agreed state','cc_preview_hub = {']
    for state,points in sorted(candidates.items()):
        guards=[]
        effect.append(f'if = {{ limit = {{ hidden_trigger = {{ state = {state} }} }}')
        preview.append(f'if = {{ limit = {{ hidden_trigger = {{ state = {state} }} }}')
        for index,pid in enumerate(points):
            links='OR = { '+' '.join(f'AND = {{ PREV = {{ controls_province = {other} }} has_railway_connection = {{ path = {{ {pid} {other} }} }} }}' for other in sorted(neighbours.get(pid,())))+' }'
            guard=f'PREV = {{ controls_province = {pid} }} free_building_slots = {{ building = supply_node size > 0 include_locked = no province = {pid} }} {links}'
            guards.append('AND = { '+guard+' }')
            reward=f'add_building_construction = {{ type = supply_node level = 1 instant_build = yes province = {pid} }}'
            effect.append(('if' if index==0 else 'else_if')+f' = {{ limit = {{ hidden_trigger = {{ {guard} }} }} {reward} }}')
            preview.append(('if' if index==0 else 'else_if')+f' = {{ limit = {{ hidden_trigger = {{ {guard} }} }} {reward} }}')
        preview.append(f'else = {{ add_building_construction = {{ type = supply_node level = 1 instant_build = yes province = {points[0]} }} }}')
        effect.append('}');preview.append('}')
        trig.append(f'AND = {{ state = {state} OR = {{ '+' '.join(guards)+' } }')
    trig.append('} }');effect += ['}','cc_rebuild_hub_sites = { }'];preview.append('}')
    write('common/scripted_triggers/ICW_COMECON_hubs.txt','\n'.join(trig));write('common/scripted_effects/ICW_COMECON_hubs.txt','\n'.join(effect+preview))
    records={'project':'IMPERIA COLD WAR','user_emblem_sha256':hashlib.sha256((HERE/'user-emblem.png').read_bytes()).hexdigest(),'donor':donor.relative_to(ROOT).as_posix(),'donor_sha256':hashlib.sha256(donor.read_bytes()).hexdigest(),'rail_junctions':len(candidates),'modifications':'Retain the native EU circular outer rim and alpha; replace its inner disc and stars with a red field and the white interior symbol from the user-supplied emblem. Original procedural dossier and button textures. No national flag texture is copied; country flags use native GetFlag.'}
    write('tools/comecon/art-record.json',json.dumps(records,indent=2))

