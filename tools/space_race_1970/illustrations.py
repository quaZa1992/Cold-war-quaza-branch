# IMPERIA CW — Cold War: native programme pictograms and astronomical map bodies.
"""Code-native interface artwork; no national achievement photograph is repurposed."""
import math
import random
from PIL import Image, ImageDraw, ImageFont


def category(p):
    value=(p['id']+' '+p['name']).lower()
    if p['region']=='ground':return 'ground'
    if any(k in value for k in ['launcher','launch vehicle','propulsion','booster','heavy-lift','rocket']):return 'rocket'
    if any(k in value for k in ['station','laboratory','skylab','salyut','mir ']):return 'station'
    if any(k in value for k in ['landing','lander','rover','sample return']):return 'lander'
    if p['crewSize']>0 or any(k in value for k in ['crew','astronaut','cosmonaut','capsule']):return 'crew'
    if p['region'] in ['leo','meo','heo','polar','geo']:return 'satellite'
    return 'probe'


def programme_art(kind,font_path):
    scale=3
    im=Image.new('RGB',(300*scale,88*scale),'#0b1a24');d=ImageDraw.Draw(im)
    def line(points,color='#8bbec6',width=1):d.line([(round(x*scale),round(y*scale)) for x,y in points],fill=color,width=width*scale)
    def rect(box,fill=None,outline='#9db8b7',width=1):d.rectangle(tuple(round(a*scale) for a in box),fill=fill,outline=outline,width=width*scale)
    def ellipse(box,fill=None,outline='#7fa0ac',width=1):d.ellipse(tuple(round(a*scale) for a in box),fill=fill,outline=outline,width=width*scale)
    def poly(points,fill='#374c58',outline='#abc4c4'):d.polygon([(round(x*scale),round(y*scale)) for x,y in points],fill=fill,outline=outline,width=scale)
    rng=random.Random(1970)
    for _ in range(85):
        x,y=rng.randrange(900),rng.randrange(264);d.point((x,y),fill=rng.choice(['#24414e','#335465','#6b858c']))
    for x in range(0,301,30):line([(x,0),(x,88)],'#112936')
    for y in range(0,89,22):line([(0,y),(300,y)],'#112936')
    ellipse((220,-18,343,105),fill='#182f3b',outline='#365767')
    d.arc((234*scale,-4*scale,328*scale,92*scale),65,250,fill='#587e8a',width=scale)
    if kind=='ground':
        line([(12,72),(210,72)],'#637a7d')
        for x in [38,97]:
            poly([(x,68),(x+11,45),(x+22,68)],'#253e4a')
            line([(x+11,46),(x-1,26)],'#d1bd8a',2)
            d.arc(((x-12)*scale,16*scale,(x+24)*scale,47*scale),0,180,fill='#aac7c9',width=2*scale)
            line([(x-12,32),(x+24,32)],'#aac7c9')
        rect((139,46,207,70),'#2c424c');rect((151,29,196,46),'#52656b')
        for x in range(145,204,10):rect((x,52,x+4,56),'#9bc3c7',None)
        line([(178,29),(178,13)],'#d0b77c');ellipse((176,10,180,14),'#d0b77c')
    elif kind=='rocket':
        poly([(99,16),(104,6),(109,16),(109,65),(99,65)],'#d6dbd4')
        poly([(99,51),(89,70),(99,64)],'#798f98');poly([(109,51),(119,70),(109,64)],'#798f98')
        for y in [24,39,54]:line([(99,y),(109,y)],'#3c5964',2)
        poly([(101,66),(104,82),(108,66)],'#c39b56','#e7bf78')
        line([(146,16),(146,73),(174,73)],'#536f79')
        for y in range(20,70,10):line([(137,y),(155,y)],'#607a80')
        line([(137,17),(155,70)],'#607a80');line([(155,17),(137,70)],'#607a80')
        line([(109,26),(144,26)],'#d0b77c')
    elif kind in ['satellite','station','probe']:
        rect((102,33,131,55),'#c1c7bf');rect((107,29,126,33),'#617b85')
        if kind=='station':
            rect((79,38,157,49),'#a4b3b3');ellipse((151,36,163,51),'#6d8792')
            rect((117,16,125,69),'#8fa5ac');rect((165,20,200,64),'#183a56','#6090a6')
        else:
            line([(94,44),(139,44)],'#d0b77c',2)
            rect((43,27,94,60),'#183a56','#6090a6');rect((139,27,190,60),'#183a56','#6090a6')
        for left,right in [(43,94),(139,190)]:
            if kind=='station' and left==43:continue
            for x in range(left+6,right,9):line([(x,28),(x,59)],'#446b80')
            line([(left+1,43),(right-1,43)],'#446b80')
        if kind=='probe':
            d.arc((100*scale,7*scale,134*scale,38*scale),0,180,fill='#d0b77c',width=2*scale)
            line([(117,25),(117,8)],'#d0b77c');ellipse((115,5,119,9),'#ddd4b4')
        else:line([(120,29),(140,12)],'#c1c7bf');ellipse((138,9,142,13),'#d0b77c')
    elif kind=='crew':
        poly([(99,17),(116,17),(140,54),(76,54)],'#d0d6cf')
        rect((75,54,142,61),'#758d98');ellipse((98,25,114,36),'#132d3b','#789aa4')
        poly([(83,62),(136,62),(145,75),(74,75)],'#405c6b');line([(93,21),(86,52)],'#8da2a8')
        line([(151,31),(166,44),(150,59)],'#d0b77c');line([(168,31),(183,44),(167,59)],'#7196a0')
    else:
        poly([(8,85),(38,70),(61,74),(79,65),(108,72),(142,69),(182,77),(216,68),(245,83)],'#303b40','#64757a')
        rect((92,35,125,53),'#b9bcb0');poly([(88,35),(99,19),(119,19),(130,35)],'#a9babe')
        ellipse((102,25,115,33),'#1d3645','#6f9ba6')
        poly([(90,51),(82,60),(138,60),(127,51)],'#9d864e','#d0b77c')
        for points in [[(93,58),(72,75),(62,75)],[(126,58),(147,75),(159,75)]]:line(points,'#c9c5ad',2)
        line([(113,20),(113,8)],'#c8d6d2');line([(139,74),(139,29)],'#bcb8a1');poly([(140,29),(164,30),(164,42),(140,41)],'#334d5e','#7895a1')
    labels={'ground':'GROUND SYSTEMS','rocket':'LAUNCH VEHICLE','satellite':'ORBITAL SYSTEMS','station':'ORBITAL STATION','probe':'DEEP-SPACE PROBE','crew':'CREWED SPACECRAFT','lander':'SURFACE EXPLORATION'}
    font=ImageFont.truetype(str(font_path),9*scale)
    d.text((188*scale,74*scale),labels[kind],font=font,fill='#b6c7c7',anchor='mm')
    rect((0,0,299,87),None,'#425963')
    return im.resize((300,88),Image.Resampling.LANCZOS)


def planet(d,x,y,r,color):
    from PIL import ImageColor
    base=ImageColor.getrgb(color)
    for py in range(-r,r+1):
        for px in range(-r,r+1):
            depth=1-(px*px+py*py)/(r*r)
            if depth<0:continue
            light=max(.12,.25+.75*max(0,(-px/r*.55-py/r*.35+math.sqrt(depth)*.65)))
            d.point((x+px,y+py),fill=tuple(min(255,int(c*light)) for c in base))
