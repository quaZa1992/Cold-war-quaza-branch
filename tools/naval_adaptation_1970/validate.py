# IMPERIA COLD WAR — Validate installed country naval adaptations.
"""Bounded source/provider/geometry checks. This is not native game evidence."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from focus_prerequisite_ui import nodes,field
from naval_adaptation_1970 import naval_adapter as A

DOC=A.DOC
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')

def shape(rows):
    return [(n.key,n.op,shape(n.children()) if isinstance(n.value,list) else n.value) for n in rows]

def main():
    checks=[];hashes={};summaries={}
    def check(ok,label):
        if not ok:raise AssertionError(label)
        checks.append(label)
    def read(relative):
        p=ROOT/relative;b=p.read_bytes();s=b.decode('utf-8-sig')
        hashes[relative]=hashlib.sha256(b).hexdigest()
        check(b.startswith(b'\xef\xbb\xbf')==relative.endswith('.yml'),'Correct encoding '+relative)
        check(s.startswith('l_english:\n# IMPERIA COLD WAR —') if relative.endswith('.yml') else s.startswith('# IMPERIA COLD WAR —'),'Exact file marker '+relative)
        return s
    expected=A.runtime_outputs();parsed={}
    for relative,canonical in expected.items():
        s=read(relative)
        if relative.endswith('.txt'):
            parsed[relative]=nodes(s)
            check(shape(nodes(s))==shape(nodes(canonical)),'Installed runtime equals canonical '+relative)
            check(not any(isinstance(n.value,str) and re.fullmatch(r'-?\d+\.\d{6,}',n.value) for n in A.walk(parsed[relative])),'Native literal precision '+relative)
        else:check(s==canonical,'Installed localisation equals canonical '+relative)
    effects={n.key:n for n in parsed['common/scripted_effects/COLDWAR_NAVY_1970.txt']}
    triggers={n.key:n for n in parsed['common/scripted_triggers/COLDWAR_NAVY_1970.txt']}
    loc=dict(re.findall(r'^ ([^\s:]+):0 (".*")$',expected['localisation/english/COLDWAR_NAVY_1970_l_english.yml'],re.M))
    loc={k:json.loads(v) for k,v in loc.items()}
    font=(GAME/'gfx/fonts/hoi_16mbs.fnt').read_text(encoding='utf-8-sig')
    glyph={};kern={}
    for line in font.splitlines():
        d={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)}
        if line.startswith('char '):glyph[d['id']]=d['xadvance']
        elif line.startswith('kerning '):kern[d['first'],d['second']]=d['amount']
    def width(s):return sum(glyph.get(ord(c),glyph[63]) for c in s)+sum(kern.get((ord(a),ord(b)),0) for a,b in zip(s,s[1:]))
    categories=set()
    for p in (ROOT/'common/technologies').glob('*.txt'):
        for n in A.walk(nodes(p.read_text(encoding='utf-8-sig'))):
            if n.key=='categories':categories.update(str(c.value) for c in n.children() if c.key=='_bare')
    all_sprites=set()
    for base in (GAME,ROOT):
        for p in (base/'interface').glob('*.gfx'):
            all_sprites.update(re.findall(r'\bname\s*=\s*"([^"\n]+)"',p.read_text(encoding='utf-8-sig',errors='replace')))
    counts={'USA':301,'SOV':856,'DDR':836,'IRQ':441,'UAE':129}
    total=0
    for tag,p in A.profiles().items():
        s=read(p['tree_file']);tree=next(n for n in nodes(s) if n.key=='focus_tree')
        rows=[n for n in tree.children() if n.key=='focus'];fs={field(n.children(),'id'):n for n in rows}
        check(len(rows)==len(fs)==counts[tag],'Unique installed count '+tag)
        own={k:v for k,v in fs.items() if k.startswith(A.PREFIX+tag+'_')}
        planned=A.build_country(tag);records={r['id']:r for r in planned['records']}
        check(set(own)==set(records),'Exact donor closure '+tag)
        check(A.integrate_tree(tag,s)==s,'Idempotent tree integration '+tag)
        xy={}
        def resolve(fid,seen=()):
            check(fid not in seen,'Acyclic anchor '+fid)
            if fid in xy:return xy[fid]
            n=fs[fid];x=float(field(n.children(),'x',0));y=float(field(n.children(),'y',0));anchor=field(n.children(),'relative_position_id')
            if anchor:
                check(anchor in fs,'Anchor exists '+fid);ax,ay=resolve(anchor,seen+(fid,));x+=ax;y+=ay
            xy[fid]=(x,y);return xy[fid]
        for fid in fs:resolve(fid)
        parents={fid:[[c.value for c in n.children() if c.key=='focus'] for n in row.children() if n.key=='prerequisite'] for fid,row in fs.items()}
        def ancestors(fid,seen=()):
            check(fid not in seen,'Acyclic prerequisite '+fid)
            for group in parents[fid]:
                for parent in group:
                    check(parent in fs,'Existing prerequisite '+fid+' '+parent);ancestors(parent,seen+(fid,))
        widths={}
        for raw in planned['focuses']:
            canon=nodes(raw)[0];fid=field(canon.children(),'id');n=own[fid];r=records[fid]
            check(shape(n.children())==shape(canon.children()),'Actual focus equals adaptation '+fid)
            check(xy[fid]==tuple(r['xy']),'Resolved installed coordinate '+fid)
            ancestors(fid)
            check(parents[fid]==r['prerequisites'],'Complete prerequisite groups '+fid)
            for other in r['exclusions']:
                check(other in own and fid in records[other]['exclusions'],'Symmetric exclusion '+fid)
                check('NOT' in [n.key for n in triggers[r['ready']].children()],'Execution exclusion guard '+fid)
            check(fid in loc and fid+'_desc' in loc,'English focus text '+fid)
            widths[fid]=width(loc[fid]);check(widths[fid]<=147,'Native caption width '+fid)
            check(not any(c in loc[fid]+loc[fid+'_desc'] for c in ('\u2013','\u2014')),'Player text dash convention '+fid)
            check(str(field(n.children(),'icon')).strip('"') in all_sprites,'Registered native icon '+fid)
            check(not any(c.key in ('allow_branch','date') for c in A.walk(n.children())),'Inspectable programme without calendar lock '+fid)
            for other,coord in xy.items():
                if fid==other:continue
                check(not(abs(coord[0]-xy[fid][0])<1.75 and abs(coord[1]-xy[fid][1])<.99),'No card collision '+fid+' '+other)
            ready=triggers[r['ready']];complete=effects[r['completion']];preview=effects[A.ident(tag,'preview_'+r['key'])]
            check([c.key for c in preview.children()]==['effect_tooltip'],'Nonexecuting concrete preview '+fid)
            check(all(x in repr(shape(ready.children())) for x in (tag,'IMP_is_1970_scenario',r['done'])),'Country/scenario/once execution guard '+fid)
            check(any(c.key=='set_country_flag' and c.value==r['pending'] for c in A.walk(complete.children())),'Pending receipt '+fid)
            check(any(c.key=='set_country_flag' and c.value==r['done'] for c in A.walk(complete.children())),'Successful once receipt '+fid)
            check(any(c.key=='clr_country_flag' and c.value==r['pending'] for c in A.walk(complete.children())),'Successful pending cleanup '+fid)
        total+=len(own)
        summaries[tag]=dict(new_focuses=len(own),installed_focuses=len(fs),variant=p['variant'],maximum_title_width=max(widths.values()),bounds=[min(xy[f][0] for f in own),min(xy[f][1] for f in own),max(xy[f][0] for f in own),max(xy[f][1] for f in own)])
    all_nodes=list(A.walk(parsed['common/scripted_effects/COLDWAR_NAVY_1970.txt']))
    for n in all_nodes:
        if n.key.startswith(A.PREFIX) and n.value=='yes':check(n.key in effects or n.key in triggers,'Resolved helper '+n.key)
        if n.key=='category':check(n.value in categories,'Actual native technology category '+str(n.value))
    check(not any(n.key in ('create_unit','load_oob','load_oob_and_tech','add_special_project_progress') for n in all_nodes),'No free fleets, OOB or future prototype completion')
    # Check each actual construction site's immediately preceding slot grant.
    def sites(rows):
        for i,n in enumerate(rows):
            if n.key=='add_building_construction':
                check(i>0 and rows[i-1].key=='add_extra_state_shared_building_slots' and int(rows[i-1].value)==int(field(n.children(),'level')),'One same-state slot per construction level '+str(n.start))
            sites(n.children())
    sites(parsed['common/scripted_effects/COLDWAR_NAVY_1970.txt'])
    actions=parsed['common/on_actions/COLDWAR_NAVY_1970.txt'][0].children()
    check({n.key for n in actions}=={'on_startup'}|{'on_daily_'+t for t in A.profiles()},'Five country hooks plus startup, no world scan')
    check(total==85,'85 total additions')
    result=dict(project='IMPERIA COLD WAR',status='PASS',checks=len(checks),countries=summaries,hashes=hashes,details=checks,native_game_test='Not run for this change',multiplayer_test='Not run for this change',scope='Actual emitted source, canonical equality, guarded rewards, providers, fonts, encodings and card footprints. Source checks do not prove native execution or engine connector routing.')
    DOC.mkdir(parents=True,exist_ok=True)
    (DOC/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('details','hashes')},indent=2))

if __name__=='__main__':main()
