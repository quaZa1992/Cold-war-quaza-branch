# IMPERIA COLD WAR — shared contracts for the approved universal SSR implementation.
from pathlib import Path
from copy import deepcopy
import hashlib,json,re

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
SOURCE=HERE/'approved_design.json'
TAGS=('UKR','BLR','MLV','EST','LAT','LIT','GEO','ARM','AZE','KAZ','UZB','TRK','KYR','TAJ')
MARKER='# IMPERIA COLD WAR — Universal SSR focus programme.'

def number(value):
    result=f'{value:.5f}'.rstrip('0').rstrip('.')
    return result if result and result!='-0' else '0'

def slug(value):return re.sub(r'[^a-z0-9]+','_',value.lower()).strip('_')

def write(relative,body,localisation=False):
    path=ROOT/relative;path.parent.mkdir(parents=True,exist_ok=True)
    if localisation:
        text='l_english:\n'+MARKER+'\n'+body.lstrip('\ufeff\n')
        encoding='utf-8-sig'
    else:
        text=MARKER+'\n'+body.lstrip('\ufeff\n');encoding='utf-8'
    temporary=path.with_name(path.name+'.coldwar.tmp')
    temporary.write_text(text,encoding=encoding)
    temporary.replace(path)
    return str(path.relative_to(ROOT))

def loc_text(mapping):
    return '\n'.join(' '+key+':0 '+json.dumps(str(value),ensure_ascii=False) for key,value in mapping.items())+'\n'

def data():
    source=json.loads(SOURCE.read_text(encoding='utf-8'))
    amendment_path=HERE/'approved_amendments.json'
    if amendment_path.exists():
        amendments=json.loads(amendment_path.read_text(encoding='utf-8'))
        for model in source['models'].values():
            for node in model['nodes']:
                change=amendments.get('nodes',{}).get(node['key'])
                if not change:continue
                node['modifiers'].update(change.get('modifiers',{}))
                for key,value in change.get('modifiers',{}).items():
                    if node.get('specialisation'):
                        node.setdefault('legacy_modifiers',{})[key]=round(value*.2,5)
                if change.get('description_insert'):
                    body,separator,history=node['description'].partition(' Historical precedent: ')
                    node['description']=body+' '+change['description_insert']+(separator+history if separator else '')
        source['labels'].update(amendments.get('labels',{}))
    return source

def canonical_id(node,tag):
    if node.get('specialisation'):return 'COLDWAR_SSR_'+node['key']
    return node['id']

def models():
    source=data();result={}
    for tag,model in source['models'].items():
        model=deepcopy(model)
        ids={node['id']:canonical_id(node,tag) for node in model['nodes']}
        for node in model['nodes']:
            node['source_id']=node['id'];node['id']=ids[node['id']]
            node['prerequisites']=[[ids[value] for value in group] for group in node['prerequisites']]
            node['exclusive']=[ids[value] for value in node['exclusive']]
            node['anchor']=ids.get(node.get('anchor'))
            node['scope_tag']=tag if node['phase']=='party' or node['group']=='regional' else None
            node['group_key']=('party_'+tag+'_'+node['gate'][4:] if node['phase']=='party' else
                               'regional_'+tag if node['group']=='regional' else node['group'])
            node['receipt']=node['id']+'_rewarded'
        result[tag]=model
    return result

def nodes():
    result={}
    for model in models().values():
        for node in model['nodes']:result.setdefault(node['id'],node)
    return list(result.values())

def receipt(node):return node['receipt']

def baseline():
    record=dict(project='IMPERIA COLD WAR',approved_source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest())
    amendments=HERE/'approved_amendments.json'
    if amendments.exists():record['approved_amendments_sha256']=hashlib.sha256(amendments.read_bytes()).hexdigest()
    return record
