# IMPERIA COLD WAR — COMECON generated source, references and transaction boundaries
import ast
import hashlib
import json
import re
from pathlib import Path
from PIL import Image
from build import ROOT,HERE,MARK,OFFERS,DATA,PROJECTS

# Reuse the existing repository parser without importing its historical test runner.
parser=ast.parse((ROOT/'tools/economic_organisation/validate.py').read_text(encoding='utf-8-sig'))
node=next(x for x in parser.body if isinstance(x,ast.FunctionDef) and x.name=='parse')
scope={'re':re};exec(compile(ast.Module(body=[node],type_ignores=[]),'<project-native-parser>','exec'),scope)
parse=scope['parse']

def main():
    checks=[]
    def check(ok,label):
        checks.append({'check':label,'pass':bool(ok)})
    manifest=json.loads((HERE/'generated.json').read_text())
    trees={};hashes={}
    for rel in manifest['generated']:
        path=ROOT/rel;raw=path.read_bytes();hashes[rel]=hashlib.sha256(raw).hexdigest()
        if rel.endswith(('.txt','.gui','.gfx')):
            check(not raw.startswith(b'\xef\xbb\xbf'),rel+' UTF-8 without BOM')
            check(raw.decode('utf-8').startswith(MARK),rel+' project marker')
            try:trees[rel]=parse(raw.decode('utf-8'));check(True,rel+' native structure')
            except Exception as error:check(False,rel+' structure: '+str(error))
            check(not re.search(r'(?<![\w.])\d+\.\d{6,}',raw.decode('utf-8')),rel+' fixed-point precision')
        elif rel.endswith('.yml'):
            check(raw.startswith(b'\xef\xbb\xbf'),rel+' localisation BOM')
            lines=raw.decode('utf-8-sig').splitlines()
            check(lines[0]=='l_english:' and lines[1].startswith(MARK),rel+' mandatory header')
            check(all(re.fullmatch(r' \w+:0 "[^"\n]*"',line) for line in lines[2:]),rel+' complete single-line localisation records')
    allcode='\n'.join((ROOT/r).read_text(encoding='utf-8-sig') for r in manifest['generated'] if r.endswith(('.txt','.gui','.gfx')))
    check(not re.search(r'\b(?:cc_\{[a-z_]+\}|cc_\w*\{s\})',allcode),'all compiler placeholders expanded')
    definitions=set(re.findall(r'^\s*(cc_\w+)\s*=\s*\{',allcode,re.M))
    references=set(re.findall(r'\b(cc_\w+)\s*=\s*(?:yes|no)\b',allcode))
    check(not references-definitions,'all COMECON effect and trigger references resolve: '+', '.join(sorted(references-definitions)))
    def walk(body):
        for key,op,value in body:
            yield key,op,value
            if isinstance(value,list):yield from walk(value)
    ui=trees['common/scripted_guis/ICW_COMECON.txt'][0][2]
    for name,op,body in ui:
        for key,op,value in body:
            if key in ('effects','triggers','properties'):
                keys=[k for k,o,v in value]
                check(len(keys)==len(set(keys)),name+' unique '+key)
    effects=dict((k,v) for k,o,v in trees['common/scripted_effects/ICW_COMECON.txt'])
    check(len(OFFERS)==44 and len(PROJECTS)==22,'complete approved 22-entry / 44-offer catalogue')
    check(all(b['levels']==[1,1,1] for h in DATA['hostPlans'].values() for b in h['buildings']),'one host level per building type in every tier')
    check('type = nuclear_reactor' not in allcode,'no COMECON reactor grant')
    check('steel reserve units' not in allcode,'steel reserves replaced')
    for s in range(1,5):
        prepay=str(effects[f'cc_{s}_prepay'])
        check(prepay.index('treasury')<prepay.index('modify_treasury_effect'),f'file {s} affordability checked before charging')
        check('cc_'+str(s)+'_liability' in prepay and 'cc_'+str(s)+'_paid' in prepay,f'file {s} final invoice settles remaining liability')
        check('cc_'+str(s)+'_delivered_revision' in str(effects[f'cc_{s}_complete']),f'file {s} delivery receipt')
        check('global.cc_'+str(s)+'_payers' in allcode,f'file {s} captured payers survive membership changes')
        # Every building transaction puts slots before native construction or its rail-hub adapter.
        complete=(ROOT/'common/scripted_effects/ICW_COMECON.txt').read_text()
        for match in re.finditer(r'var:cc_'+str(s)+r'_site1 = \{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}',complete):
            body=match.group(1)
            if 'add_building_construction' in body or 'cc_build_hub = yes' in body:
                check('add_extra_state_shared_building_slots' in body and body.index('add_extra_state_shared_building_slots')<max(body.find('add_building_construction'),body.find('cc_build_hub = yes')),f'file {s} slot before construction')
    for rel in manifest['integrations']:
        path=ROOT/rel;raw=path.read_bytes();check(not raw.startswith(b'\xef\xbb\xbf'),rel+' retains native encoding')
    money=(ROOT/'common/scripted_effects/00_money_system.txt').read_text()
    check(money.count('add_to_variable = { additional_expenses_rate = cc_weekly_expenses }')==1,'national weekly stream enters the native accumulator exactly once')
    art=Image.open(ROOT/'gfx/interface/comecon/toolbar.dds').convert('RGBA');donor=Image.open(ROOT/'gfx/interface/help_gui/EU_help_button_custom.dds').convert('RGBA')
    check(art.size==donor.size==(46,46),'toolbar retains native EU dimensions')
    check(all(art.getpixel((x,y))==donor.getpixel((x,y)) for y in range(46) for x in range(46) if (x-22.5)**2+(y-22.5)**2>21**2),'toolbar outer rim and alpha retained')
    check('GetFlag' in (ROOT/'localisation/english/ICW_COMECON_l_english.yml').read_text(encoding='utf-8-sig'),'current native country flags')
    gui=(ROOT/'interface/ICW_COMECON.gui').read_text(encoding='utf-8')
    binding=(ROOT/'common/scripted_guis/ICW_COMECON.txt').read_text(encoding='utf-8')
    triggers=(ROOT/'common/scripted_triggers/ICW_COMECON.txt').read_text(encoding='utf-8')
    clock=(ROOT/'common/on_actions/zzzzzzzz_ICW_COMECON.txt').read_text(encoding='utf-8')
    check('max_slots_horizontal = 13' in gui,'header flags have a horizontal native grid')
    check('cc_flag = { image = "[THIS.GetFlag]" }' in binding,'header flags use current full-size native flag images')
    check('cc_toolbar_window" position = { x=788 y=38 }' in gui and 'x = global.var_missiles_button_x' in binding,'launcher shares the native EU row and DLC-dependent offset')
    check(not re.search(r'cc_\d_site\d\s*>\s*0',triggers),'encoded state scope pointers are checked for zero, never positive numeric IDs')
    check('on_startup = { effect = { SOV = { cc_initialize = yes } } }' in clock,'initialisation has an explicit country scope in the native startup hook')
    check(Image.open(ROOT/'gfx/interface/comecon/dossier.dds').size==(900,580),'compact cover matches the 900 x 580 native window')
    check('height=304' in gui and 'height=38' in gui and 36+8*38<=340,'all eight country rows fit the effects viewport')
    check('cc_ui_recipients' in binding and 'cc_ui_delegates' in binding,'country lists use bounded private page arrays')
    from view import compact_rewards,native_wrap
    compact_rows=[compact_rewards(1,p,o,t,host) for p,o in OFFERS for t in range(3) for host in (False,True)]
    check(all(len(text.splitlines())<=2 for text in compact_rows),'every agreement and investment scale retains all numeric benefits within two table lines')
    check(all(len(native_wrap(d['description']).splitlines())<=2 for d in DATA['catalogue'].values()),'all programme descriptions fit their explicit two-line fields')
    for atlas in (ROOT/'gfx/fonts/COMECON').glob('*.fnt'):
        source=atlas.read_text(encoding='utf-8');size=re.search(r'scaleW=(\d+) scaleH=(\d+)',source)
        texture=Image.open(atlas.with_suffix('.dds'))
        check(texture.size==tuple(map(int,size.groups())),atlas.name+' native atlas dimensions')
        rects=[tuple(map(int,m)) for m in re.findall(r'char id=\d+ x=(\d+) y=(\d+) width=(\d+) height=(\d+)',source)]
        check(all(x+w<=texture.width and y+h<=texture.height for x,y,w,h in rects),atlas.name+' glyphs remain inside the atlas')
    from safety_checks import run as safety_checks
    safety_checks(check,trees)
    from council_checks import run as council_checks
    council_checks(check,trees)
    report={'project':'IMPERIA COLD WAR','scope':'Generated source, native parser, references, encoding and transaction structure. Not live multiplayer evidence.','success':all(x['pass'] for x in checks),'checks':checks,'sha256':hashes}
    (ROOT/'docs/design/comecon/source-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'success':report['success'],'checks':len(checks),'failures':[x for x in checks if not x['pass']]}))
    if not report['success']:raise SystemExit(1)

if __name__=='__main__':main()
