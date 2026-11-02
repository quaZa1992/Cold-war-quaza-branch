# IMPERIA COLD WAR — Installed Chile focus-tree review preview.
"""Overlay independently parsed installed scripts on the retained approval viewer."""
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
DOCS=ROOT/'docs/CHILE_COLDWAR_CONCEPT_1970_1990'
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
sys.path.insert(0,str(HERE))
from script_ast import parse, first, emit
from current_design import load_design

def build():
    manifest=json.loads((DOCS/'IMPLEMENTATION_MANIFEST.json').read_text(encoding='utf-8'))
    assert manifest['installed'], 'Install before generating an installed-code preview'
    data=load_design()
    effects={};triggers={};focuses={};transition=[];political_events=[]
    for item in manifest['outputs']:
        rel=item['path'];path=ROOT/rel
        assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'], 'Installed output drift: '+rel
        if not rel.endswith('.txt') or 'COLDWAR_CHL' not in rel:continue
        ast=parse(path.read_text(encoding='utf-8'))
        if '/scripted_effects/' in rel:effects.update({k:v for k,o,v in ast})
        elif '/scripted_triggers/' in rel:triggers.update({k:v for k,o,v in ast})
        elif '/national_focus/' in rel:
            focuses={first(v,'id'):v for k,o,v in first(ast,'focus_tree') if k=='focus'}
        elif rel=='common/decisions/COLDWAR_CHL_1970_politics.txt':
            transition=[('COLDWAR_CHL_political_transition','=',first(ast,'COLDWAR_CHL_political_transition'))]
        elif rel=='events/COLDWAR_CHL_1970_politics.txt':
            political_events=[(k,o,v) for k,o,v in ast if k=='country_event' and first(v,'id') in ('COLDWAR_CHL.5','COLDWAR_CHL.6')]
    assert len(focuses)==len(data['nodes'])==184
    resolved={}
    def position(key):
        if key in resolved:return resolved[key]
        f=focuses[key];x,y=int(first(f,'x')),int(first(f,'y'))
        anchor=first(f,'relative_position_id')
        if anchor:
            ax,ay=position(anchor);x+=ax;y+=ay
        resolved[key]=(x,y);return x,y
    for node in data['nodes']:
        assert position(node['id'])==(node['x'],node['y']),node['id']
        node['availability_code']=emit([('COLDWAR_CHL_can_complete_'+node['key'],'=',triggers['COLDWAR_CHL_can_complete_'+node['key']])])
        keys=['COLDWAR_CHL_preview_focus_'+node['key'],'COLDWAR_CHL_apply_'+node['key']]
        if node.get('agreement'):keys+=['COLDWAR_CHL_preview_'+node['key']]
        node['proposed_code']=emit([('focus','=',focuses[node['id']])]+[(k,'=',effects[k]) for k in keys])
        if node['key'] in ('military_staff','pinochet_command'):
            guard_keys=['COLDWAR_CHL_intervention_context','COLDWAR_CHL_can_prepare_intervention','COLDWAR_CHL_can_resolve_rupture']
            node['proposed_code']+='\n'+emit(transition+[(k,'=',triggers[k]) for k in guard_keys]+political_events)
        node['requirements']=[r.replace('Diplomatic relations with Cuba.','Relations with Cuba exceed -25.') for r in node['requirements']]
    for agreement in data['agreements']:
        agreement['requirements']=[r.replace('Diplomatic relations with Cuba.','Relations with Cuba exceed -25.') for r in agreement['requirements']]
    data['status']='IMPLEMENTED: source checked; live HOI4 test omitted by user.'
    data['integration']['sync']='Installed code is shown below. Source checks do not establish live HOI4 rendering or multiplayer execution.'
    old=(DOCS/'preview-review.html').read_text(encoding='utf-8')
    offset=old.index(',art=')+len(',art=')
    art,_=json.JSONDecoder().raw_decode(old[offset:])
    template=(DOCS/'preview.template.html').read_text(encoding='utf-8')
    template=template.replace('Cold War Chile approval concept','Installed Cold War Chile review preview')
    template=template.replace('FOCUS TREE CONCEPT','INSTALLED FOCUS TREE')
    template=template.replace('Concept composition. Native font and connector routing approximated.','Code-based composition. Native font and connector routing approximated.')
    template=template.replace('Design record and native API references','Installed scripts and native API references')
    old_money="const money=v=>'$'+Number(v.toFixed(5)).toFixed(v%1?Math.min(5,Math.max(3,(String(v).split('.')[1]||'').length)):3)+' billion';"
    new_money="const money=v=>v<1?'$'+Number((v*1000).toFixed(3))+' million':'$'+Number(v.toFixed(3))+' billion';"
    assert old_money in template
    template=template.replace(old_money,new_money)
    template=template.replace('Native primitives and proposed modifier records. New Chile providers and guards require implementation after approval. Source-level audit does not establish live HOI4 behavior.','Installed focus, requirement, preview and execution scripts. Live HOI4 behavior remains untested.')
    fragment=template.replace('__DATA__',json.dumps(data,ensure_ascii=False,separators=(',',':'))).replace('__ART__',json.dumps(art,separators=(',',':')))
    output='<!-- IMPERIA COLD WAR — Installed Chile review wrapper. -->\n<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0">'+fragment+'</body></html>'
    target=DOCS/'IMPLEMENTED_preview.html';target.write_text(output,encoding='utf-8')
    provenance={'project':'IMPERIA COLD WAR','feature':'Chile installed-code preview','source':'Frozen approval plus current_design cost/layout/political-route overlays and the installed script manifest','approval_sha256':manifest['approved_sha256'],'installed_focus_sha256':next(x['sha256'] for x in manifest['outputs'] if '/national_focus/' in x['path']),'focuses':len(focuses),'positions_verified':len(resolved),'art':'Unchanged embedded approval-preview donor assets. See PREVIEW_PROVENANCE.json and EVENT_ART_REVIEW.md. Original individual artists and separate permissions remain unknown where not identified upstream.','native_screenshot':False,'live_engine_tested':False}
    provenance['revision']=manifest.get('revision',{})
    (DOCS/'IMPLEMENTED_PREVIEW_PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')
    print(target)

if __name__=='__main__':build()
