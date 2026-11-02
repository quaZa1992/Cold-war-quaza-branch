# IMPERIA COLD WAR — Brazil native artwork and English presentation refinements.
from copy import deepcopy
from common import HERE,P
import hashlib,json

def package(name):
    p=HERE/name
    if not p.exists():return None
    data=json.loads(p.read_text(encoding='utf-8'))
    assert data['project']=='IMPERIA COLD WAR',name
    return data

def polish_design(model):
    d=deepcopy(model);copy=package('english_polish.json');art=package('focus_art_polish.json')
    strings=copy['overrides'] if copy else {};icons=art['focus_icon_overrides'] if art else {}
    known={n['id'] for n in d['nodes']};assert not set(icons)-known
    for n in d['nodes']:
        assert n['id'] not in strings,'Focus titles belong to the approved layout'
        n['description']=strings.get(n['id']+'_desc',n['description'])
        if n['id'] in icons:n['icon']=icons[n['id']]['native_icon']
    for s in d['starting_spirits']:s['description']=strings.get(s['id']+'_desc',s['description'])
    for i,e in enumerate(d['events']):e['description']=strings.get('COLDWAR_BRA.'+str(i+1)+'.d',e['description'])
    d['presentation_polish']=dict(project='IMPERIA COLD WAR',focus_icon_changes=len(icons),english_overrides=len(strings),sources={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ('english_polish.json','focus_art_polish.json') if (HERE/name).exists()},scope='Native art aliases and English copy. Approved titles, graph, rewards and costs preserved.')
    return d

def polish_localisation(general,politics):
    copy=package('english_polish.json')
    if not copy:return
    for key,value in copy['overrides'].items():
        assert isinstance(value,str) and not any(c in value for c in '\u2013\u2014'),key
        assert key in general or key in politics,'Unknown English override '+key
        (politics if key in politics else general)[key]=value
