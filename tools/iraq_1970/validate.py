# IMPERIA CW — Cold War: iraq 1970 — validate.
"""Static integration/reference audit of the installed Iraq/USA package."""
import hashlib,json,re,sys,zipfile
from collections import Counter
from common import *
from audit_design import load_design

HERE=Path(__file__).resolve().parent
MD=Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
def read(rel):return parse((ROOT/rel).read_text(encoding='utf-8-sig'))
def positions(foci):
    fs={first(f,'id'):f for f in foci};cache={}
    def resolve(id,stack=()):
        assert id not in stack,('Relative-anchor cycle',id)
        if id not in cache:
            f=fs[id];x=float(first(f,'x',0));y=float(first(f,'y',0));anchor=first(f,'relative_position_id')
            if anchor:a,b=resolve(anchor,stack+(id,));x+=a;y+=b
            cache[id]=(x,y)
        return cache[id]
    return {id:resolve(id) for id in fs}

def main():
    d=load_design();manifest=json.loads((HERE/'manifest.json').read_text())
    # IMPERIA CW — Cold War: compare this task to its actual pre-change snapshot;
    # other chats may legitimately have advanced the original integration baseline.
    streamlined='--streamlining' in sys.argv
    scope=json.loads((ROOT/'docs/design/iraq_1970/decision_streamlining_2026_10_21/IMPLEMENTATION_REPORT.json').read_text()) if streamlined else None
    assert len(d['nodes'])==426
    paths=scope['changed_files'] if streamlined else list(manifest['generated'])+[a['path'] for a in manifest['adapters']]
    asts={rel:read(rel) for rel in paths if rel.endswith(('.txt','.gfx'))}
    loc={};loc_files=[]
    for f in (ROOT/'localisation/english').glob('*.yml'):
        text=f.read_text(encoding='utf-8-sig')
        for m in re.finditer(r'^\s*([\w.\-]+):\d*\s+"',text,re.M):loc.setdefault(m[1],str(f))
        if f.name.startswith(('COLDWAR_IRQ_','COLDWAR_USA_gulf_')):
            assert f.read_bytes().startswith(b'\xef\xbb\xbf') and not text.startswith('\ufeff'),('Localization BOM',f)
            assert text.startswith('l_english:'),f;loc_files.append(f.name)
    irq=first(asts['common/national_focus/COLDWAR_IRQ_1970_focus.txt'],'focus_tree');foci=values(irq,'focus');fs={first(f,'id'):f for f in foci};xy=positions(foci)
    assert len(fs)==426 and len(foci)==426
    for n in d['nodes']:
        f=fs[n['id']];assert xy[n['id']]==tuple(n['xy']),(n['id'],xy[n['id']],n['xy'])
        assert [values(p,'focus') for p in values(f,'prerequisite')]==n['prerequisites'],n['id']
        assert values(first(f,'mutually_exclusive',[]),'focus')==n['mutually_exclusive'],n['id']
        assert float(first(f,'cost'))*7==n['days'],n['id']
        assert n['id'] in loc and n['id']+'_desc' in loc,n['id']
        assert n['mutually_exclusive']==[] or all(n['id'] in next(x for x in d['nodes'] if x['id']==p)['mutually_exclusive'] for p in n['mutually_exclusive'])
    active={n['id'] for n in d['nodes'] if not n.get('audit_retired')}
    assert len({xy[fid] for fid in active})==len(active),'Overlapping active focus coordinates'
    # Every original USA focus remains byte-semantically identical after import.
    usa=first(read('common/national_focus/USA_1970.txt'),'focus_tree');newusa=values(usa,'focus')
    oldpath=HERE/'integration_baseline/common/national_focus/USA_1970.txt'
    old=values(first(parse(oldpath.read_text(encoding='utf-8-sig')),'focus_tree'),'focus')
    if streamlined:
        with zipfile.ZipFile(ROOT/'docs/design/iraq_1970/decision_streamlining_2026_10_21/before.zip') as archive:
            before_usa=parse(archive.read('common/national_focus/USA_1970.txt').decode('utf-8-sig'))
        assert read('common/national_focus/USA_1970.txt')==before_usa,'USA focuses changed during streamlining'
        old=newusa
    else:
        assert [f for f in newusa if not first(f,'id').startswith('COLDWAR_USA_gulf_')]==old,'Existing USA focuses changed'
        assert len(newusa)==len(old)+15
        staged=values(read('tools/iraq_1970/staged/USA_GULF_FOCUS_FRAGMENT.txt'),'focus')
        expected_usa=positions(staged)
        usaxy=positions(newusa)
        for fid,xy_expected in expected_usa.items():
            assert usaxy[fid]==(xy_expected[0]+30,xy_expected[1]),(fid,usaxy[fid])
    # Resolve providers across the current overlay and engine/MD fallback.
    effects=set();triggers=set();ideas=set();dynamic=set();sprites=set();events=set();definitions=set();legacy_parse=[]
    for dirname,registry in [('common/scripted_effects',effects),('common/scripted_triggers',triggers),('common/dynamic_modifiers',dynamic)]:
        for f in (ROOT/dirname).glob('*.txt'):
            source=f.read_text(encoding='utf-8-sig')
            try:registry.update(k for k,o,v in parse(source))
            except ValueError as e:
                # Unrelated pre-existing provider files may be malformed; they
                # are reported, not silently rewritten by this content package.
                legacy_parse.append({'path':str(f.relative_to(ROOT)),'error':str(e)})
                registry.update(re.findall(r'^([A-Za-z_][\w.]*)\s*=\s*\{',source,re.M))
    for base in [GAME,MD,ROOT]:
        for f in (base/'interface').glob('*.gfx'):
            try:a=parse(f.read_text(encoding='utf-8-sig'))
            except Exception:continue
            for c in values(a,'spriteTypes'):
                for s in values(c,'spriteType'):sprites.add(str(first(s,'name')).strip('"'))
        for f in (base/'common/ideas').glob('*.txt'):
            try:a=parse(f.read_text(encoding='utf-8-sig'))
            except Exception:continue
            for container in values(a,'ideas'):
                for k,o,v in container:
                    if isinstance(v,list):ideas.update(x for x,_,z in v)
    for rel,a in asts.items():
        definitions.update(k for k,o,v in walk(a) if k.startswith(('COLDWAR_IRQ_','COLDWAR_USA_gulf_')) and isinstance(v,list))
        if rel.startswith('events/'):
            events.update(first(v,'id') for v in values(a,'country_event'))
    for name in loc_files:
        source=(ROOT/'localisation/english'/name).read_text(encoding='utf-8-sig')
        for icon in re.findall(r'£(generic_[\w]+)',source):assert 'GFX_'+icon in sprites,('Missing inline party icon',name,icon)
    refs=[];miss=[]
    for rel,a in asts.items():
        for k,o,v in walk(a):
            if isinstance(v,str):
                clean=v.strip('"')
                if k.startswith(('COLDWAR_IRQ_','COLDWAR_USA_gulf_')) and v in ('yes','no'):
                    refs.append((rel,k));
                    if k not in effects|triggers:miss.append((rel,'provider',k))
                if k in ('add_ideas','remove_ideas','has_idea','idea') and clean.startswith(('COLDWAR_IRQ_','COLDWAR_USA_gulf_')) and clean not in ideas:miss.append((rel,'idea',clean))
                if k=='custom_effect_tooltip' and clean.startswith(('COLDWAR_IRQ_','COLDWAR_USA_gulf_')) and clean not in loc:miss.append((rel,'tooltip',clean))
                if k=='texturefile' and rel.startswith('interface/COLDWAR_IRQ_') and not any((base/clean).exists() for base in [ROOT,MD,GAME]):miss.append((rel,'texture',clean))
                if k=='icon' and rel.startswith('common/national_focus/COLDWAR_IRQ_') and clean not in sprites:miss.append((rel,'sprite',clean))
    assert not miss,miss
    # Native generated building modifier families are documented templates;
    # ordinary keys must exist in the installed engine or MD definitions.
    documentation=(GAME/'documentation/modifiers_documentation.md').read_text(encoding='utf-8-sig')
    modifiers=set(re.findall(r'^## ([\w]+)',documentation,re.M))
    for f in (ROOT/'common/modifier_definitions').glob('*.txt'):
        modifiers.update(k for k,o,v in parse(f.read_text(encoding='utf-8-sig')))
    building_defs=first(read('common/buildings/00_buildings.txt'),'buildings')
    assert 'production_speed_<Building>_factor' in documentation
    for building,_,_ in building_defs:
        modifiers.update('state_repair_speed_'+building+'_factor' for _ in [0])
        modifiers.add('repair_speed_'+building+'_factor')
        modifiers.add('production_speed_'+building+'_factor')
        modifiers.add('state_production_speed_'+building+'_factor')
    checked_modifiers=set()
    for rel,a in asts.items():
        if rel.startswith('common/ideas/'):
            for k,o,v in walk(a):
                if k in ('modifier','targeted_modifier') and isinstance(v,list):
                    for key,op,val in v:
                        if key=='tag':continue
                        assert key in modifiers,('Unsupported idea modifier',rel,key);checked_modifiers.add(key)
        if rel.startswith('common/dynamic_modifiers/'):
            for _,_,rows in a:
                for key,op,val in rows:
                    if key in ('icon','enable','remove_trigger','cancel_trigger'):continue
                    assert key in modifiers,('Unsupported dynamic modifier',rel,key);checked_modifiers.add(key)
    for rel,digest in manifest['generated'].items():
        if streamlined and rel not in paths:continue
        assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest,('Stale generation',rel)
    report={'scope':'Static graph, source preservation, localization and transitive COLDWAR references; no engine claim','iraq_focuses':len(foci),'iraq_active_focuses':len(active),'retired_compatibility_ids':len(foci)-len(active),'audit_revision':d['audit_revision'],'usa_existing_preserved':len(old),'usa_added':15,'parsed_generated_and_integration_files':len(asts),'scripted_calls_resolved':len(refs),'english_localization_files':loc_files,'missing_references':miss,'current_design_positions_and_grouped_prerequisites_preserved':True,'unrelated_legacy_parse_findings':legacy_parse}
    report['native_or_MD_modifier_keys_verified']=sorted(checked_modifiers)
    if streamlined:report.update(scope='Scoped streamlining integration against the 2026-10-21 snapshot; no engine claim',usa_added=0)
    destination=ROOT/'docs/design/iraq_1970/decision_streamlining_2026_10_21/VALIDATION_REPORT.json' if streamlined else HERE/'VALIDATION_REPORT.json'
    destination.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='unrelated_legacy_parse_findings'},indent=2))

if __name__=='__main__':main()
