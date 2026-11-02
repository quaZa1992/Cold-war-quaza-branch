# IMPERIA COLD WAR — Compact Argentina national-focus geometry.
"""Pack native-sized party columns and national programmes without changing gameplay."""
from __future__ import annotations
import argparse,copy,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
REVISION='Argentina compact layout 2026-11-01'
GEOMETRY={'x','y','dx','dy'}
PAIRS=[('military','udelpa'),('pj','montoneros'),('ucr','socialist'),('mid','unions'),('liberal','sra'),('conservative','catholic'),('pdc','cgta'),('pca','prt')]
NATIONAL=[('institutions','diplomacy'),('economy','science'),('defence','falklands')]

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def semantics(d):
    result=copy.deepcopy(d);result.pop('layout_revision',None)
    for n in result['nodes']:
        for k in GEOMETRY:n.pop(k,None)
    for g in result['groups']:
        for k in ('x','y'):g.pop(k,None)
    return result
def bounds(d):return dict(min_x=min(n['x'] for n in d['nodes']),max_x=max(n['x'] for n in d['nodes']),min_y=min(n['y'] for n in d['nodes']),max_y=max(n['y'] for n in d['nodes']))
def compact(d):
    if d.get('layout_revision',{}).get('revision')==REVISION:return d
    before=semantics(d);old_bounds=bounds(d);groups={g['id']:g for g in d['groups']};byid={n['id']:n for n in d['nodes']}
    local={}
    for gid,g in groups.items():
        ns=[n for n in d['nodes'] if n['group']==gid]
        rows=sorted({n['y']-g['y'] for n in ns})
        for n in ns:
            x=n['x']-g['x'];assert x%2==0,(n['id'],'unexpected half-column')
            local[n['id']]=[x//2,rows.index(n['y']-g['y'])]
    # Two four-card rows need an extra left lane after the half-width conversion.
    military_left=('ongania_corporate','presidency_discipline','corporate_labor','order_universities','career_officers','service_rotation','presidential_guard')
    island_left=('sovereignty_talks','islands_links','sovereignty_conference','leaseback_framework','joint_services','peaceful_patrols','sovereignty_treaty','fisheries_science')
    for key in military_left+island_left:local['COLDWAR_ARG_'+key][0]-=1
    def ext(gid):
        ps=[local[n['id']] for n in d['nodes'] if n['group']==gid]
        return min(p[0] for p in ps),max(p[0] for p in ps),max(p[1] for p in ps)
    cursor=2
    for column,pair in enumerate(PAIRS+NATIONAL):
        if column==len(PAIRS):cursor+=2
        left=max(-ext(g)[0] for g in pair);right=max(ext(g)[1] for g in pair)
        root_x=cursor+left
        for gid,root_y in ((pair[0],0),(pair[1],ext(pair[0])[2]+3)):
            groups[gid]['x']=root_x;groups[gid]['y']=root_y
            for n in d['nodes']:
                if n['group']==gid:n['x']=root_x+local[n['id']][0];n['y']=root_y+local[n['id']][1]
        cursor=root_x+right+4
    for n in d['nodes']:
        if n['anchor']:
            anchor=byid[n['anchor']];n['dx']=n['x']-anchor['x'];n['dy']=n['y']-anchor['y']
        else:n['dx']=n['x'];n['dy']=n['y']
    assert semantics(d)==before,'Layout changed non-geometric design data'
    d['layout_revision']=dict(project='IMPERIA COLD WAR',revision=REVISION,before=old_bounds,after=bounds(d),party_columns=PAIRS,national_columns=NATIONAL,continuous_focus_position=dict(x=2688,y=2600),continuous_focus_size=dict(width=770,height=380),reference_grid=dict(x=96,y=130),native_card=dict(width=165,height=128),semantics_sha256=digest(before))
    return d

def record_baseline():
    dest=HERE/'LAYOUT_BASELINE.json'
    if dest.exists():raise ValueError('The geometry baseline already exists; do not overwrite it')
    d=json.loads((HERE/'runtime_design.json').read_text(encoding='utf-8'))
    manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
    record=dict(project='IMPERIA COLD WAR',feature='Argentina compact layout input',authorization='User: Condense the Tree',semantics_sha256=digest(semantics(d)),before=bounds(d),positions={n['id']:{k:n[k] for k in ('x','y','dx','dy','anchor')} for n in d['nodes']},runtime_files=manifest['files'])
    dest.write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(dict(project='IMPERIA COLD WAR',baseline=str(dest),focuses=len(d['nodes']))))
def record_provider_semantics():
    # Recover exact baseline bytes from the frozen native fixture where another
    # country integration has since added only header comments to a shared file.
    sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
    from script_ast import parse
    baseline=json.loads((HERE/'LAYOUT_BASELINE.json').read_text());native=json.loads((HERE/'NATIVE_RESULT.json').read_text())
    frozen=Path(native['run'])/'fixture';providers={}
    for rel,h in baseline['runtime_files'].items():
        if rel.startswith('common/national_focus/'):continue
        source=ROOT/rel
        if hashlib.sha256(source.read_bytes()).hexdigest()!=h:source=frozen/rel
        assert hashlib.sha256(source.read_bytes()).hexdigest()==h,('No exact baseline provider available',rel)
        providers[rel]=dict(baseline_sha256=h,semantic_sha256=digest(parse(source.read_text(encoding='utf-8-sig'))) if rel.endswith('.txt') else h)
    dest=HERE/'LAYOUT_PROVIDER_SEMANTICS.json'
    if dest.exists():raise ValueError('Provider semantic baseline already recorded')
    dest.write_text(json.dumps(dict(project='IMPERIA COLD WAR',feature='Exact-byte-backed layout provider semantic baseline',providers=providers),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(project='IMPERIA COLD WAR',providers=len(providers))))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--record-baseline',action='store_true');ap.add_argument('--record-provider-semantics',action='store_true');args=ap.parse_args()
    if args.record_baseline:record_baseline()
    if args.record_provider_semantics:record_provider_semantics()
