# IMPERIA COLD WAR — USA source comparison and concept preview packaging.
"""Package data and existing MD art for the inline review. No runtime writes."""
from pathlib import Path
import base64, gzip, hashlib, io, json, re
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
MD=Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
OUT=Path('C:/Users/Enes/.codex/visualizations/2026/10/24/01a16eeb-40d0-7851-80fa-70784386712c')
proposal=json.loads((HERE/'proposal.json').read_text(encoding='utf-8'))

def clean(s):
    return str(s or '').replace('\u2014',':').replace('\u2013','-')
def short(block):
    def write(b,depth=0):
        return ' '.join(k+' '+op+' '+('{ '+write(v,depth+1)+' }' if isinstance(v,list) else str(v)) for k,op,v in b)
    s=write(block)
    return clean(s[:240]+(' ...' if len(s)>240 else ''))

def group(n,source):
    k=n['id']
    if source=='original':
        i=n['_index']
        if i<87:return 'Administrations'
        if i<166:return 'Military'
        if i<232:return 'Foreign policy'
        if i<289:return 'Regional economy'
        if i<301:return 'Space'
        if i<311:return 'Media'
        if i<322:return 'Drugs'
        if i<330:return 'Crisis'
        if i<334:return 'Constitution'
        return 'Alternative parties'
    if k.startswith('USA_1970_NIX'):return 'Nixon'
    if re.match(r'USA_1970_19',k):return 'Elections'
    if k.startswith('COLDWAR_USA_gulf'):return 'Gulf'
    for prefix,title in [('E','Economy'),('N','Energy'),('F','Foreign policy'),('S','Society'),('D','Defence')]:
        if k.startswith('USA_1970_'+prefix):return title
    return 'Foreign policy'

sprites={}
for base in [MD,ROOT]:
    for p in (base/'interface').glob('*.gfx'):
        text=p.read_text(encoding='utf-8-sig',errors='replace')
        for m in re.finditer(r'\b(?:spriteType|SpriteType|frameAnimatedSpriteType)\s*=\s*\{(.*?)\n\s*\}',text,re.S):
            name=re.search(r'\bname\s*=\s*"([^\"]+)"',m[1])
            texture=re.search(r'\btexturefile\s*=\s*"([^\"]+)"',m[1],re.I)
            if name and texture:sprites[name[1]]=(base,texture[1])

cache_path=HERE/'icon_cache.json'
cache=json.loads(cache_path.read_text(encoding='utf-8')) if cache_path.exists() else {}
icons=cache.get('icons',{});icon_sources=cache.get('sources',{})
def icon(key):
    candidates=[key,'GFX_goal_'+str(key),'GFX_'+str(key)]
    for candidate in candidates:
        if candidate in icons:return candidate
        if candidate not in sprites:continue
        base,rel=sprites[candidate];p=base/rel
        if not p.exists():continue
        try:
            im=Image.open(p).convert('RGBA')
            if im.width>im.height*2:continue
            # A reduced-size preview only. Source pixels and game files unchanged.
            im.thumbnail((24,24),Image.Resampling.LANCZOS)
            buf=io.BytesIO();im.save(buf,format='WEBP',quality=60,method=4)
            icons[candidate]='data:image/webp;base64,'+base64.b64encode(buf.getvalue()).decode('ascii')
            icon_sources[candidate]=dict(source=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
            return candidate
        except (OSError,ValueError):continue
    return None

sets={}
for source,file in [('current','current_inventory.json'),('original','original_inventory.json')]:
    ns=json.loads((HERE/file).read_text(encoding='utf-8'))['focuses']
    result=[]
    for i,n in enumerate(ns):
        n['_index']=i
        ik=n.get('icon')
        if not ik:
            m=re.search(r'\bicon\s*=\s*([^\s{}]+)',n['raw']);ik=m[1] if m else ''
        desc=clean(n['description'])
        if source=='original':desc=desc[:160]+(' ...' if len(desc)>160 else '')
        result.append(dict(id=n['id'],name=clean(n['name']),description=desc,xy=[n['resolved_x'],n['resolved_y']],days=round(float(n['cost'])*7,1),
            prerequisites=n['prerequisites'],mutually_exclusive=n['mutually_exclusive'],module=group(n,source),icon=icon(ik),line=n['line'],source=source,status='Existing',
            source_effects=short(n['completion_reward']) if source=='current' else '',requirements=[short(n['available'])] if n['available'] and source=='current' else []))
    sets[source]=result

sets['concept']=json.loads(json.dumps(sets['current']))
byid={n['id']:n for n in sets['concept']}
icon_by_module={'Industry':'factory_planning','Civil priorities':'research','Energy':'nuclear_power','Force structure':'united_states_army','Intelligence':'helmet_knife','Army doctrine':'combined_arms','Naval priorities':'united_states_navy','Civil rights':'pass_legislation','Foreign doctrine':'diplomatic_treaty','Atlantic':'diplomatic_treaty','Pacific':'united_states_navy','Rival diplomacy':'diplomatic_treaty','Middle East':'diplomatic_treaty','Americas':'factory_planning','Election priorities':'pass_legislation'}
for n in proposal['nodes']:
    p=json.loads(json.dumps(n));p['source']='concept'
    if p['id'] in byid:
        original=byid[p['id']]
        p['icon']=original['icon'];p['source_effects']=original['source_effects']
        original.update(p)
    else:
        p['icon']=icon(icon_by_module.get(p['module'],'diplomatic_treaty'))
        if not p['icon']:
            parents=[pid for row in p.get('prerequisites',[]) for pid in row]
            p['icon']=next((byid[pid].get('icon') for pid in parents if pid in byid and byid[pid].get('icon')),byid['USA_1970_E0']['icon'])
        sets['concept'].append(p);byid[p['id']]=p
for rw in proposal['rewiring']:
    p=byid[rw['focus']]
    if 'prerequisites' in rw:p['prerequisites']=rw['prerequisites']
    if rw.get('remove_exclusion'):p['mutually_exclusive']=[]
    p['mutually_exclusive']+=rw.get('add_exclusion',[])
    p['rewiring']=rw['reason']
    if p['status']=='Existing':p['status']='Rewired'

# Apply conceptual rewiring to reworked nodes too, without mutating live data.
modules=['Industry','Civil priorities','Energy','Civil rights','Force structure','Intelligence','Army doctrine','Naval priorities','Election priorities','Foreign doctrine','Atlantic','Pacific','Rival diplomacy','Middle East','Americas']
overlays=[n for n in sets.pop('concept') if n['status']!='Existing']
data=dict(project='IMPERIA COLD WAR',sets=sets,overlays=overlays,proposal={k:v for k,v in proposal.items() if k!='nodes'},icons=icons,modules=modules)
payload=base64.b64encode(gzip.compress(json.dumps(data,ensure_ascii=False,separators=(',',':')).encode('utf-8'),mtime=0)).decode('ascii')
template=(HERE/'review_fragment.html').read_text(encoding='utf-8')
fragment=template.replace('__USA_DATA__',payload)
cache_path.write_text(json.dumps(dict(project='IMPERIA COLD WAR',icons=icons,sources=icon_sources),separators=(',',':')),encoding='utf-8')
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'usa-tree-review.html').write_text(fragment,encoding='utf-8')
(HERE/'preview_provenance.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',author='OpenAI Codex concept packaging',credits='Millennium Dawn contributors; IMPERIA COLD WAR project authors',licence_or_permission='Existing local project review; separate redistribution permission unknown',modifications='DDS icons decoded and reduced to 24px lossy WebP for this concept viewer; source assets unchanged. Layout connectors and web font approximate engine rendering. Original MD descriptions are shortened; complete records remain in original_inventory.json.',icons=icon_sources,fragment_bytes=len(fragment.encode('utf-8')),counts=proposal['counts']),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(bytes=len(fragment.encode('utf-8')),icons=len(icons),counts=proposal['counts'])))
