# IMPERIA COLD WAR — Argentina compact layout and semantic preservation audit.
"""Resolve emitted native coordinates and inspect full card/connector footprints."""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,values
from layout import semantics,digest
TREE='common/national_focus/COLDWAR_ARG_1970_focus.txt'
def main():
    d=json.loads((HERE/'runtime_design.json').read_text(encoding='utf-8'));baseline=json.loads((HERE/'LAYOUT_BASELINE.json').read_text(encoding='utf-8'))
    fs=values(first(parse((ROOT/TREE).read_text()),'focus_tree'),'focus');byid={first(f,'id'):f for f in fs};positions={};checks=[]
    def ck(ok,name):checks.append(dict(name=name,passed=bool(ok)))
    def resolve(fid,stack=()):
        if fid in positions:return positions[fid]
        assert fid not in stack,('Cyclic focus anchor',fid)
        f=byid[fid];p=first(f,'relative_position_id');x=int(first(f,'x'));y=int(first(f,'y'))
        if p:a,b=resolve(p,stack+(fid,));x+=a;y+=b
        positions[fid]=(x,y);return x,y
    for fid in byid:resolve(fid)
    ck(digest(semantics(d))==baseline['semantics_sha256'],'all non-geometric design data preserved')
    semantic_path=HERE/'LAYOUT_PROVIDER_SEMANTICS.json'
    provider_semantics=json.loads(semantic_path.read_text())['providers'] if semantic_path.exists() else {}
    comment_only_changes=[]
    for rel,h in baseline['runtime_files'].items():
        if rel==TREE:continue
        exact=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h
        expected=provider_semantics.get(rel,{})
        same=exact or (rel.endswith('.txt') and expected.get('baseline_sha256')==h and digest(parse((ROOT/rel).read_text(encoding='utf-8-sig')))==expected.get('semantic_sha256'))
        if same and not exact:comment_only_changes.append(rel)
        ck(same,'unchanged runtime provider semantics '+rel)
    for n in d['nodes']:ck(positions[n['id']]==(n['x'],n['y']),n['id']+' parsed coordinate matches current preview')
    boxes={fid:(x*96,y*130,x*96+165,y*130+128) for fid,(x,y) in positions.items()}
    overlaps=[];cuts=[]
    def intersect(a,b):return min(a[2],b[2])>max(a[0],b[0]) and min(a[3],b[3])>max(a[1],b[1])
    for i,(fid,a) in enumerate(boxes.items()):
        for oid,b in list(boxes.items())[i+1:]:
            if intersect(a,b):overlaps.append((fid,oid))
    ck(not overlaps,'no full native card overlaps')
    links=0
    for fid,f in byid.items():
        for group in values(f,'prerequisite'):
            for parent in values(group,'focus'):
                links+=1;ax,ay=positions[parent];bx,by=positions[fid]
                ck(by>ay,parent+' -> '+fid+' descends')
                x1=ax*96+82.5;y1=ay*130+115;x2=bx*96+82.5;y2=by*130+12;mid=(y1+y2)/2
                segments=((x1,y1,x1,mid),(min(x1,x2),mid,max(x1,x2),mid),(x2,mid,x2,y2))
                for oid,rect in boxes.items():
                    if oid in (fid,parent):continue
                    for sx,sy,ex,ey in segments:
                        # Strict interior avoids flagging a shared rail in the two-pixel row gap.
                        hit=(rect[0]+1<sx<rect[2]-1 and max(sy,ey)>rect[1]+1 and min(sy,ey)<rect[3]-1) if sx==ex else (rect[1]+1<sy<rect[3]-1 and ex>rect[0]+1 and sx<rect[2]-1)
                        if hit:cuts.append(dict(parent=parent,child=fid,card=oid));break
    # This route is a faithful review approximation, not the engine's native routing algorithm.
    ck(not cuts,'no unrelated card intersections in orthogonal preview routes')
    pocket=d['layout_revision']['continuous_focus_position'];size=d['layout_revision']['continuous_focus_size']
    rect=(pocket['x'],pocket['y'],pocket['x']+size['width'],pocket['y']+size['height'])
    ck(not any(intersect(rect,r) for r in boxes.values()),'native 770 x 380 continuous-focus pocket clear')
    old=baseline['before'];new=d['layout_revision']['after'];ow=(old['max_x']-old['min_x'])*96+165;oh=(old['max_y']-old['min_y'])*130+128;nw=(new['max_x']-new['min_x'])*96+165;nh=(new['max_y']-new['min_y'])*130+128
    result=dict(project='IMPERIA COLD WAR',passed=all(c['passed'] for c in checks),checks=len(checks),failed=[c['name'] for c in checks if not c['passed']],focuses=len(fs),prerequisite_links=links,before=old,after=new,width_reduction_percent=round((1-nw/ow)*100,2),height_reduction_percent=round((1-nh/oh)*100,2),area_reduction_percent=round((1-nw*nh/(ow*oh))*100,2),card_overlaps=overlaps,preview_connector_intersections=cuts,continuous_focus_position=pocket,concurrent_comment_only_changes=comment_only_changes,boundary='Source and full native-sized browser card footprint audit; native engine connector routing and GUI remain separate checks.')
    (HERE/'LAYOUT_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result));return not result['passed']
if __name__=='__main__':raise SystemExit(main())
