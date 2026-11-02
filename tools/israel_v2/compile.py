# IMPERIA COLD WAR — Compile the approved Israel V2 tree into native MD content.
"""Pure build first. --write installs only a complete, validated payload.

The approved proposal is never overwritten. Domain emitters return files and
fully guarded actions. This compiler owns their coherent loaded integration.
"""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(ROOT/'tools/israel_1970'))
from script_format import format_script, read
from runtime_core import block, number
import runtime_core
import runtime_bilateral
import runtime_domestic
import runtime_territories
import runtime_layout
import runtime_art

MARKER='# IMPERIA COLD WAR — Israel V2 national focus implementation.\n'


def sha(value):
    return hashlib.sha256(value if isinstance(value,bytes) else value.encode('utf-8')).hexdigest()


def focus_tree(data,actions,sprites):
    groups={g['id']:g for g in data['groups']}
    anchors={g['id']:next(n for n in data['nodes'] if n['group']==g['id']) for g in data['groups']}
    ordered=[]
    for g in data['groups']:
        ordered.append(anchors[g['id']])
        ordered.extend(n for n in data['nodes'] if n['group']==g['id'] and n['id']!=anchors[g['id']]['id'])
    first=anchors['institutions']['xy']
    chunks=['id = ISR70_focus','country = { base = 0 modifier = { add = 100 ISR2_is_scenario = yes } }',
            'default = no','reset_on_civilwar = no',
            f'initial_show_position = {{ x = {first[0]} y = {first[1]} }}',
            f'continuous_focus_position = {{ x = 0 y = {(max(n["xy"][1] for n in data["nodes"])+3)*130} }}']
    for g in data['groups']:
        chunks.append(block('shortcut',f'name = ISR2_shortcut_{g["id"]}\ntarget = {anchors[g["id"]]["id"]}\nscroll_wheel_factor = 0.8'))
    for n in ordered:
        a=actions[n['id']]
        anchor=anchors[n['group']]
        relative=n['id']!=anchor['id']
        xy=[n['xy'][i]-(anchor['xy'][i] if relative else 0) for i in (0,1)]
        parts=[f'id = {n["id"]}',f'icon = {sprites[n["icon"]]}',
               f'x = {xy[0]}',f'y = {xy[1]}',f'cost = {number(n["days"]/7)}',
               'available_if_capitulated = no','cancel_if_invalid = yes','continue_if_invalid = no']
        if relative:
            parts.append('relative_position_id = '+anchor['id'])
        parts += [block('prerequisite','\n'.join('focus = '+p for p in row)) for row in n['pre']]
        if n['exclusive']:
            parts.append(block('mutually_exclusive','\n'.join('focus = '+p for p in n['exclusive'])))
        available=[]
        party=groups[n['group']].get('runtime_party_trigger')
        if party:
            available.append(party+' = yes')
        if a.get('visible_available'):
            available.append(a['visible_available'])
        available.append(block('hidden_trigger',a['available']))
        parts.append(block('available','\n'.join(available)))
        parts.append(block('search_filters','focus_filter = '+
            ('FOCUS_FILTER_POLITICAL' if groups[n['group']]['kind']=='party' or n['group']=='institutions' else
             'FOCUS_FILTER_ARMY' if n['group']=='reserves' else 'FOCUS_FILTER_RESEARCH' if n['group']=='arsenal' else 'FOCUS_FILTER_INDUSTRY')))
        preview=a['preview'].strip()
        if not preview.startswith('effect_tooltip'):
            preview=block('effect_tooltip',preview)
        if n.get('offer_target'):
            preview='custom_effect_tooltip = ISR2_if_they_accept\n'+preview
        parts.append(block('completion_reward',preview+'\n'+block('hidden_effect',a['reward']+'\nISR2_refresh = yes')))
        ai='factor = 1'
        if n['id']=='ISR2_security_emergency':
            ai+='\nmodifier = { factor = 0 has_war = no }'
        parts.append(block('ai_will_do',ai))
        chunks.append(block('focus','\n'.join(parts)))
    return MARKER+block('focus_tree','\n\n'.join(chunks))+'\n'


def build():
    approved=json.loads((HERE/'design.json').read_text(encoding='utf-8'))
    data=runtime_domestic.extend_data(runtime_bilateral.extend_data(approved))
    from runtime_titles import apply as apply_titles
    data=apply_titles(data)
    for n in data['nodes']:
        if any('Poalei Agudat has actual governing representation.'==r for r in n['requirements']):
            n['requirements']=[r for r in n['requirements'] if r!='Poalei Agudat has actual governing representation.']
            n['description']+=' The government funds a contract with the religious workers\' cooperatives; the programme changes no party or coalition membership.'
            n['runtime_adaptation']='Funded cooperative contract under the native governing-party check; no unsupported claim of separate Poalei cabinet representation.'
    data=runtime_layout.arrange(data)
    modules=[runtime_bilateral.build(data),runtime_domestic.build(data),runtime_territories.build(data)]
    actions={}
    files={}
    loc={}
    def merge(mapping,key,value):
        if key in mapping and mapping[key]!=value:
            raise ValueError(('Conflicting generated owner',key))
        mapping[key]=value
    for module in modules:
        for key,value in module['actions'].items():merge(actions,key,value)
        for key,value in module['files'].items():merge(files,key,value)
        for key,value in module['loc'].items():merge(loc,key,value)
        for fid,override in module.get('preview_adaptations',{}).items():
            n=next(n for n in data['nodes'] if n['id']==fid)
            n.update(deepcopy(override))
    core=runtime_core.build(data,actions)
    if core['unresolved']:
        raise ValueError(('Unimplemented approved effects',core['unresolved']))
    modules.append(core)
    for key,value in core['actions'].items():merge(actions,key,value)
    for key,value in core['files'].items():merge(files,key,value)
    for key,value in core['loc'].items():merge(loc,key,value)
    assert set(actions)=={n['id'] for n in data['nodes']},'Every focus must have exactly one runtime owner'
    art=runtime_art.build(data)
    for key,value in art['files'].items():merge(files,key,value)
    files['common/national_focus/ISR70_focus.txt']=focus_tree(data,actions,art['sprite_map'])
    from runtime_integration import integrate
    integration=integrate(data,modules)
    for key,value in integration['files'].items():merge(files,key,value)
    for key,value in integration.get('loc',{}).items():merge(loc,key,value)
    from runtime_money import integrate as integrate_money
    for key,value in integrate_money()['files'].items():merge(files,key,value)
    from runtime_legacy import build as build_legacy
    legacy=build_legacy()
    for key,value in legacy['files'].items():merge(files,key,value)
    for key,value in legacy.get('loc',{}).items():merge(loc,key,value)
    for n in data['nodes']:
        if n['id']=='ISR2_negotiated_terms':
            n['description']='Offer a paid civil-service programme in a Palestinian area affected by settlement pressure. The agreement funds practical services and administrative relief while leaving borders and territorial claims to separate negotiations.'
        if n['id']=='ISR2_gahal_settlement_match':
            n['description']=n['description'].replace('same limited public and private contribution',
                'same limited public appropriation and accepted partner capital')
        loc[n['id']]=n['label']
        loc[n['id']+'_desc']=n['description']
    for g in data['groups']:loc['ISR2_shortcut_'+g['id']]=g['label']
    loc['ISR2_if_they_accept']='§YIf they accept:§!'
    text='l_english:\n # IMPERIA COLD WAR — Israel V2 native national programmes.\n'
    for key,value in sorted(loc.items()):
        assert '\u2013' not in value and '\u2014' not in value,(key,value)
        text+=' '+key+':0 "'+value.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n')+'"\n'
    files['localisation/english/ISR2_l_english.yml']=text.encode('utf-8-sig')
    for key,value in list(files.items()):
        if isinstance(value,str) and Path(key).suffix in {'.txt','.gfx','.gui'}:
            if Path(key).name.startswith('ISR2_') or key=='common/national_focus/ISR70_focus.txt':
                value=format_script(value)
            read(value)
            assert value.startswith('# IMPERIA COLD WAR'),key
            files[key]=value.encode('utf-8')
        elif isinstance(value,str):
            files[key]=value.encode('utf-8')
    data['status']='Implemented native runtime; validation status recorded separately'
    data['revision']='2.2-runtime-20261028'
    for n in data['nodes']:
        n['runtime_action']=actions[n['id']]
        n['icon']=art['sprite_map'][n['icon']]
    data['layout']['icons']=art['preview_icons']
    audit=runtime_layout.audit(data)
    if audit.get('status') not in {None,'PASS'}:
        raise ValueError(('Native layout audit',audit))
    manifest=dict(project='IMPERIA COLD WAR',phase='NATIVE_IMPLEMENTATION',focuses=len(data['nodes']),
        groups=len(data['groups']),runtime_focus_tree='ISR70_focus',
        approved_design_sha256=sha((HERE/'design.json').read_bytes()),
        artifacts={key:dict(sha256=sha(value),bytes=len(value)) for key,value in files.items()},
        layout=audit,art=art['metadata'],
        limitations=['Source generation is not an engine or multiplayer test.'])
    return dict(files=files,data=data,manifest=manifest,actions=actions)


def main():
    result=build()
    out=ROOT/'docs/israel_1970_v2'
    out.mkdir(parents=True,exist_ok=True)
    (out/'runtime_manifest.json').write_text(json.dumps(result['manifest'],indent=2)+'\n',encoding='utf-8')
    (out/'runtime_design.json').write_text(json.dumps(result['data'],ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    if '--write' in sys.argv:
        for key,value in result['files'].items():
            path=ROOT/key
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(value)
    print(json.dumps(dict(project='IMPERIA COLD WAR',status='BUILT',installed='--write' in sys.argv,
                         files=len(result['files']),focuses=len(result['data']['nodes']))))


if __name__=='__main__':main()
