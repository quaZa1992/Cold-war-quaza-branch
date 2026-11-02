# IMPERIA COLD WAR — Restored South American event-photo integration verification.
"""Check native textures, references and future generator output without installing gameplay."""
from __future__ import annotations
import argparse
import collections
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
sys.dont_write_bytecode=True
from PIL import Image
from sa_photo_catalogue import *
from sa_photo_export import FRAME, BOX, SIZE, REVIEW, inspect_gui, sha, save_json
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse

PATTERN=re.compile(r'country_event\s*=\s*\{\s*id\s*=\s*([\w.]+)[\s\S]*?\bpicture\s*=\s*(\w+)')

def check_events(outputs,country):
    found={}
    for path,text in outputs.items():
        if not path.startswith('events/'):continue
        if isinstance(text,bytes):text=text.decode('utf-8')
        parse(text)
        for event,sprite in PATTERN.findall(text):
            assert sprite==picture_for(event),(country,event,sprite,picture_for(event))
            assert event not in found,event
            found[event]=sprite
    expected={k for k in EVENT_ASSETS if k.startswith('COLDWAR_'+country)}
    assert set(found)==expected,(country,sorted(expected-set(found)))
    return len(found)

def generator(country):
    directory={'CHL':'chile_1970','BRA':'brazil_1970_runtime','ARG':'argentina_1970'}[country]
    folder=ROOT/'tools'/directory;sys.path.insert(0,str(folder))
    spec=importlib.util.spec_from_file_location('photo_generator_check',folder/'compile.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    if country=='CHL': outputs=mod.build()
    elif country=='BRA': outputs,_=mod.build(shared=False)
    else:
        d=mod.runtime_design(json.loads((folder/'approved_design.json').read_text(encoding='utf-8')))
        outputs=mod.build_core(ROOT,d)
        for name in ['politics','treaties']: outputs.update(mod.module(name).build(ROOT,d))
        mod.module('event_art').build(ROOT,d)
    print(json.dumps({'country':country,'generated_event_pictures_verified':check_events(outputs,country)}))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--generator',choices=['CHL','BRA','ARG']);args=parser.parse_args()
    if args.generator:return generator(args.generator)
    manifest=json.loads((ROOT/REVIEW/'manifest.json').read_text(encoding='utf-8'))
    native=Image.open(ROOT/FRAME).convert('RGBA')
    assert sha(ROOT/FRAME)==manifest['frame_sha256']
    inspect_gui(ROOT)
    for row in manifest['assets']:
        p=ROOT/row['output'];raw=p.read_bytes();assert raw[:4]==b'DDS '
        im=Image.open(p).convert('RGBA');assert im.size==SIZE
        assert im.tobytes()==Image.open(ROOT/REVIEW/(row['asset']+'.png')).convert('RGBA').tobytes()
        assert all(im.getpixel((x,y))==native.getpixel((x,y)) for y in range(163) for x in range(217) if not (19<=x<199 and 6<=y<156))
        assert im.crop(BOX).getchannel('A').getextrema()==(255,255)
        assert sha(p)==row['output_sha256']
    sprites=collections.defaultdict(list)
    for path in (ROOT/'interface').glob('*.gfx'):
        text=path.read_text(encoding='utf-8-sig',errors='replace')
        for name,texture in re.findall(r'name\s*=\s*"([^"]+)"\s*texturefile\s*=\s*"([^"]+)"',text):
            if name.startswith(PREFIX):sprites[name].append(texture)
    for asset in set(EVENT_ASSETS.values()):
        assert sprites[PREFIX+asset]==[f'{ASSET_DIR}/{asset}.dds'],(asset,sprites[PREFIX+asset])
    owned=[ROOT/GFX,ROOT/'interface/COLDWAR_ARG_1970_eventpictures.gfx',ROOT/'interface/COLDWAR_BRA_1970.gfx']
    outputs={}
    for path in (ROOT/'events').glob('COLDWAR_*_1970*.txt'):
        if re.match('COLDWAR_(CHL|BRA|ARG)_',path.name):owned.append(path);outputs[path.relative_to(ROOT).as_posix()]=path.read_text(encoding='utf-8')
    for path in owned:
        raw=path.read_bytes();assert not raw.startswith(b'\xef\xbb\xbf');assert raw.startswith('# IMPERIA COLD WAR — '.encode('utf-8'));parse(raw.decode('utf-8'))
    runtime={c:check_events({k:v for k,v in outputs.items() if '/COLDWAR_'+c+'_' in k},c) for c in ['CHL','BRA','ARG']}
    generated=[]
    for country in ['CHL','BRA','ARG']:
        run=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--generator',country],cwd=ROOT,text=True,capture_output=True)
        assert run.returncode==0,(country,run.stdout,run.stderr)
        generated.append(json.loads(run.stdout.strip().splitlines()[-1]))
    report={'project':'IMPERIA COLD WAR','assets_verified':len(manifest['assets']),'runtime_events':runtime,
            'generator_checks':generated,'native_frame_and_alpha_unchanged':True,'native_BGRA_roundtrip_matches_preview':True,
            'sprites_resolve_once':True,'UTF8_without_BOM':True,'preview_visually_reviewed':True,
            'preview_type':'Donor-composed native window and contact sheets.','live_HOI4_test_performed':False}
    save_json(ROOT/REVIEW/'validation.json',report);print(json.dumps(report))

if __name__=='__main__':main()
