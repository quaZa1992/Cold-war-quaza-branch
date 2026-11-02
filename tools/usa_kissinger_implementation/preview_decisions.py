# IMPERIA COLD WAR — Read-only source preview of regional decisions and events.
"""Compose a labelled preview. Never edit runtime files or a live game profile."""
from pathlib import Path
from decimal import Decimal as D
import argparse
import base64
import hashlib
import io
import json
import re
import sys
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from focus_prerequisite_ui import nodes,field
from usa_kissinger_implementation.test_runtime import Model,children
from usa_kissinger_implementation.shared import HOSTS,P,MODS

GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
STEM='COLDWAR_USA_kissinger'


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--output',required=True,type=Path)
    args=cli.parse_args();output=args.output.resolve()
    template=Path(__file__).with_name('preview_decisions.template.html').read_text(encoding='utf-8')
    loc_path=ROOT/f'localisation/english/{STEM}_l_english.yml'
    loc=dict(re.findall(r'^\s*([^#\s:]+):\d*\s+"(.*)"\s*$',loc_path.read_text(encoding='utf-8-sig'),re.M))
    loc={key:value.replace('\\n','\n').replace('\\"','"') for key,value in loc.items()}
    states={}
    for path in (ROOT/'localisation/english').glob('*state*.yml'):
        states.update(dict(re.findall(r'^\s*(STATE_\d+):\d*\s+"(.*)"',path.read_text(encoding='utf-8-sig',errors='replace'),re.M)))
    country_names={'USA':'The United States','IRQ':'Iraq','PER':'Iran','TUR':'Turkey','SYR':'Syria','SOV':'The Soviet Union','KUR':'Kurdistan','PUK':'Patriotic Union of Kurdistan','KPI':loc['KPI'],'KPT':loc['KPT'],'KPS':loc['KPS']}
    decisions={n.key:n for cat in nodes((ROOT/f'common/decisions/{STEM}.txt').read_text(encoding='utf-8')) for n in cat.children()}
    events={field(n.children(),'id'):n for n in nodes((ROOT/f'events/{STEM}.txt').read_text(encoding='utf-8')) if n.key=='country_event'}
    ideas={n.key:n for root in nodes((ROOT/f'common/ideas/{STEM}.txt').read_text(encoding='utf-8')) for group in root.children() if group.key=='country' for n in group.children()}
    assets={};provenance=[]
    def asset(key,relative):
        path=ROOT/relative
        if not path.exists():path=GAME/relative
        im=Image.open(path).convert('RGBA');buffer=io.BytesIO();im.save(buffer,format='PNG')
        assets[key]='data:image/png;base64,'+base64.b64encode(buffer.getvalue()).decode()
        provenance.append(dict(key=key,source=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),size=list(im.size),conversion='Lossless PNG encoding for browser display; original asset unmodified',original_author='Paradox / Millennium Dawn / project contributors, individual credit unknown',licence_or_permission='Unknown; retained source rights apply'))
    for key,relative in {'tile':'gfx/interface/tiles/tiled_decisions_bg_small.dds','row':'gfx/interface/decisionview/decision_item_bg_single.dds','category':'gfx/interface/decisionview/category_header_bg.dds','decision':'gfx/interface/decisions/decision_generic_political_discourse.dds','bar':'gfx/interface/autonomy/subject_progress_bar_long.dds','bar_bg':'gfx/interface/autonomy/subject_progress_bar_long_bg.dds','photo':'gfx/event_pictures/generic/elections/political_deal.dds','event_top':'gfx/interface/event_report_top_win.dds','event_mid':'gfx/interface/event_report_tileable_midsection.dds','event_bottom':'gfx/interface/event_report_bottom_win.dds','event_option':'gfx/interface/event_option_entry.dds'}.items():asset(key,relative)
    photo_notice=json.loads((ROOT/'gfx/event_pictures/COLDWAR_USA_KS/NOTICE.json').read_text(encoding='utf-8'))
    photo_sources=json.loads((Path(__file__).parent/'source/event_photos/NOTICE.json').read_text(encoding='utf-8'))
    for host,name in photo_sources['regional_files'].items():
        asset('photo_'+host,'gfx/event_pictures/COLDWAR_USA_KS/aftermath_'+host+'.dds')
        source=next(p for p in photo_sources['photos'] if p['file']==name)
        provenance[-1].update(original_author=source['author'],licence_or_permission=source['licence_or_permission'],source_record=source['source'],conversion=photo_notice['modifications'])
    scripted_text={field(n.children(),'name'):n for n in nodes((ROOT/f'common/scripted_localisation/{STEM}.txt').read_text(encoding='utf-8')) if n.key=='defined_text'}
    cosmetics={'IRQ':'IRQ_BAATH_1970','PER':'PER_IMPERIAL_1970','TUR':'TUR_1970','SYR':'SYR_BAATH_1970','SOV':'SOV_Coldwar_Communism_neutrality'}
    for tag in country_names:
        candidates=[f'gfx/flags/{cosmetics.get(tag,tag)}.tga',f'gfx/flags/{tag}_democratic.tga',f'gfx/flags/{tag}_neutrality.tga']
        path=next((name for name in candidates if (ROOT/name).exists() or (GAME/name).exists()),None)
        if path:asset('flag_'+tag,path)

    examples={}
    for host,data in HOSTS.items():
        tag=data['tag'];examples[host]={}
        for scene in ('crisis','peace','aftermath','warning'):
            m=Model();m.authorise_route();us=m.countries['USA'];local=m.countries[tag]
            us['vars'].update({P+'stage_'+host:D(3),P+'max_stage_'+host:D(3),P+'cache_'+host:D(2000),'gdp_total':D(1000),'treasury':D(60),'political_power':D(320)})
            m.call(P+'refresh_fiscal_usa')
            us['flags'].update({P+'contact_'+host,P+'breach_'+host});us['focuses'].add(P+data['front'])
            m.call(P+'init_'+host)
            local['vars'].update({'gdp_total':D(40),'treasury':D(12),'political_power':D(320),P+'unrest':D(68),P+'stabilisation':D(35),P+'organisation':D(20)})
            local['divisions'][data['states'][0]]=2
            if scene=='peace':
                local['vars'].update({P+'unrest':D(6),P+'stabilisation':D(95),P+'qualifying_weeks':D(156),P+'reform_credit':D(104)})
                local['flags'].update({P+'investment',P+'domestic_rights_signed',P+'rights_'+host+'_accepted',P+'reform_1',P+'reform_2'})
                local['ideas'].update({P+'investment_programme',P+'domestic_rights'})
            if scene=='aftermath':
                local['vars'].update({P+'unrest':D(18),P+'stabilisation':D(70),P+'qualifying_weeks':D(52),P+'last_civilian_losses':D(10000),P+'civilian_losses':D(10000),P+'trauma_weeks':D(156),P+'trauma_drift':D('1.5'),P+'repression_cooldown':D(104)})
                local['divisions'][data['states'][0]]=4
                local['flags'].add(P+'security');local['ideas'].update({P+'security_programme',P+'repression_legacy'})
            if scene=='warning':
                local['vars'].update({P+'unrest':D(94),P+'stabilisation':D(12),P+'qualifying_days':D(35),P+'warning_days':D(49)})
                local['divisions'][data['states'][0]]=1;local['flags'].update({P+'warning',P+'mobilisation_ready'})
            local['vars'][P+'incident_state']=D(data['states'][0]);local['vars'][P+'last_civilian_losses']=D(10000)
            m.call(P+'reconciliation_total',tag);m.call(P+'refresh_host',tag)

            def resolve(value,scope=tag):
                value=str(value)
                for ident,node in scripted_text.items():
                    if '['+ident+']' in value:
                        selected=next(row for row in node.children() if row.key=='text' and m.cond(children(row.children(),'trigger'),m.countries[scope]))
                        value=value.replace('['+ident+']',resolve(loc[field(selected.children(),'localization_key')],scope))
                value=re.sub(r'\[(\d+)\.GetName\]',lambda match:states.get('STATE_'+match[1],'State '+match[1]),value)
                for country,name in country_names.items():
                    value=value.replace('['+country+'.GetNameDef]',name)
                def number(match):
                    target=match[1] or scope;name=match[2];digits=int(match[3] or 0)
                    return f'{m.countries[target]["vars"][name]:,.{digits}f}'
                return re.sub(r'\[\?(?:([A-Z]{3})\.)?([A-Za-z_0-9]+)(?:\|(\d+))?\]',number,value)

            def requirements(rows,scope):
                result=[]
                for node in rows:
                    body=node.children()
                    if node.key=='custom_trigger_tooltip':
                        result.append(dict(text=resolve(loc.get(field(body,'tooltip'),field(body,'tooltip')),scope['tag']),ok=m.cond([node],scope)))
                    elif node.key in m.triggers:
                        if node.key==P+'usa_actor':continue
                        result+=requirements(m.triggers[node.key],scope)
                    elif node.key in m.countries:result+=requirements(body,m.countries[node.key])
                    elif node.key=='check_variable':
                        variable=field(body,'var') or (body[0].key if body else '')
                        if variable=='treasury':
                            target=field(body,'value') or body[0].value
                            quote=f'{m.value(target,scope):.5f}'.rstrip('0').rstrip('.')
                            result.append(dict(text='Treasury: $'+f'{scope["vars"]["treasury"]:.2f}'+' / $'+quote+' Billion required.',ok=m.cond([node],scope)))
                    elif node.key=='NOT' and len(body)==1 and body[0].key=='has_country_flag':
                        suffix=str(body[0].value).removeprefix(P)
                        names={'security':'Regional Security Operation is inactive.','investment':'Regional Development Programme is inactive.','domestic_rights_signed':'No standing domestic regional settlement.'}
                        if suffix in names:result.append(dict(text=names[suffix],ok=m.cond([node],scope)))
                return result

            def effect_rows(rows,scope,temporary=None):
                result=[];temporary={} if temporary is None else temporary;branch=False
                owner=scope.get('tag',scope.get('id'))
                def value(raw):
                    raw=str(raw)
                    if '.' in raw:
                        country,variable=raw.split('.',1)
                        if (country,variable) in temporary:return temporary[country,variable]
                    if (owner,raw) in temporary:return temporary[owner,raw]
                    return m.value(raw,scope)
                for node in rows:
                    key,raw=node.key,node.value;body=node.children()
                    if key=='if':
                        branch=m.cond(children(body,'limit'),scope)
                        if branch:result+=effect_rows([x for x in body if x.key!='limit'],scope,temporary)
                        continue
                    if key=='else_if':
                        if not branch and m.cond(children(body,'limit'),scope):result+=effect_rows([x for x in body if x.key!='limit'],scope,temporary);branch=True
                        continue
                    if key=='else':
                        if not branch:result+=effect_rows(body,scope,temporary)
                        branch=True;continue
                    branch=False
                    if key in ('hidden_effect','limit'):continue
                    if key=='effect_tooltip':result+=effect_rows(body,scope,temporary)
                    elif key in m.effects:result+=effect_rows(m.effects[key],scope,temporary)
                    elif key in m.countries:result+=effect_rows(body,m.countries[key],temporary)
                    elif key.isdigit():result+=effect_rows(body,m.states[int(key)],temporary)
                    elif key in ('set_temp_variable','set_variable'):
                        pair=next((x for x in body if x.key!='tooltip'),None)
                        if pair:
                            temporary[owner,pair.key]=value(pair.value)
                            tooltip=field(body,'tooltip')
                            if tooltip:result.append(dict(country=scope.get('tag','State'),text=loc[tooltip].replace('$RIGHT|0$',str(int(value(pair.value)))),tone='normal'))
                    elif key in ('multiply_temp_variable','multiply_variable','divide_temp_variable','divide_variable'):
                        pair=body[0]
                        temporary[owner,pair.key]=value(pair.key)/value(pair.value) if key.startswith('divide_') else value(pair.key)*value(pair.value)
                    elif key=='add_to_temp_variable':
                        pair=body[0];temporary[owner,pair.key]=value(pair.key)+value(pair.value)
                    elif key=='modify_treasury_effect':
                        amount=temporary.get((owner,'treasury_change'),D(0));result.append(dict(country=scope.get('tag','State'),text=f'Treasury: ${amount:+.5f} Billion',tone='good' if amount>0 else 'bad'))
                    elif key=='add_to_variable' and field(body,'tooltip'):
                        pair=body[0];amount=value(pair.value);label=loc[field(body,'tooltip')]
                        def formatted(match):
                            options=match[1];digits=re.search(r'(\d+)$',options);places=int(digits[1]) if digits else 0
                            scaled=amount*100 if '%' in options else amount
                            number=f'{scaled:+,.{places}f}' if '+' in options or '-' in options else f'{scaled:,.{places}f}'
                            return number+('%' if '%' in options else '')
                        text=re.sub(r'\$RIGHT\|([^$]+)\$',formatted,label)
                        positive_good='|+=' in label;result.append(dict(country=scope.get('tag','State'),text=text,tone='good' if (amount>0)==positive_good else 'bad'))
                    elif key in ('add_ideas','remove_ideas'):
                        if key=='remove_ideas' and raw not in scope.get('ideas',set()):continue
                        result.append(dict(country=scope.get('tag','State'),text=('Add National Spirit: ' if key=='add_ideas' else 'Remove National Spirit: ')+loc.get(raw,raw),tone='normal'))
                    elif key=='add_timed_idea':
                        result.append(dict(country=scope.get('tag','State'),text='Add National Spirit: '+loc.get(field(body,'idea'),field(body,'idea'))+' ('+field(body,'days')+' days)',tone='normal'))
                        idea=ideas.get(field(body,'idea'))
                        for modifier in children(idea.children(),'modifier') if idea else []:
                            entry=next(((label,cost) for label,(native,cost) in MODS.items() if native==modifier.key),None)
                            if entry:
                                label,cost=entry;amount=D(modifier.value)
                                result.append(dict(country=scope.get('tag','State'),text=f'{label}: {amount*100:+.1f}%',tone='good' if (amount>0)!=cost else 'bad'))
                    elif key=='add_equipment_to_stockpile':
                        amount=value(field(body,'amount'));result.append(dict(country=scope.get('tag','State'),text=f'Infantry weapons: {amount:+,.0f}',tone='good' if amount>0 else 'bad'))
                    elif key=='add_manpower':result.append(dict(country=states.get('STATE_'+str(scope.get('id')),'Regional state'),text=f'Population: {value(raw):+,.0f}',tone='bad'))
                    elif key=='add_stability':result.append(dict(country=scope.get('tag','State'),text=f'Stability: {value(raw)*100:+.0f}%',tone='good' if value(raw)>0 else 'bad'))
                    elif key=='add_political_power':result.append(dict(country=scope.get('tag','State'),text=f'Political Power: {value(raw):+,.0f}',tone='good' if value(raw)>0 else 'bad'))
                    elif key=='custom_effect_tooltip' and raw in loc:result.append(dict(country=scope.get('tag','State'),text=resolve(loc[raw],scope.get('tag',tag)),tone='heading'))
                    elif key=='add_opinion_modifier':result.append(dict(country=scope.get('tag','State'),text='Opinion of '+country_names.get(field(body,'target'),field(body,'target'))+': -50',tone='bad'))
                return result

            views={}
            for side,owner in (('host',tag),('usa','USA')):
                scope=m.countries[owner];m.root=scope;items=[]
                for key,node in decisions.items():
                    if not key.startswith(P+host+'_') or not m.cond(children(node.children(),'visible'),scope):continue
                    body=node.children();cost=int(field(body,'cost','0'));available=m.cond(children(body,'available'),scope) and scope['vars']['political_power']>=cost
                    rows=effect_rows(children(body,'complete_effect'),scope)
                    if cost:rows.insert(0,dict(country=owner,text=f'Political Power: -{cost}',tone='bad'))
                    items.append(dict(id=key,title=loc[key],description=resolve(loc[key+'_desc'],owner),cost=cost,available=available,requirements=requirements(children(body,'available'),scope),effects=rows))
                views[side]=items
            record=dict(country=country_names[tag],tag=tag,gdp=40,treasury=12,political_power=320,divisions=sum(local['divisions'].values()),unrest=int(local['vars'][P+'unrest']),stabilisation=float(local['vars'][P+'stabilisation']),reconciliation=int(local['vars'][P+'reconciliation_weeks']),category=loc[P+'region_'+host],heading=loc[P+host+'_heading'],legacy=loc[P+host+('_strong' if local['vars'][P+'stabilisation']>50 else '_fading' if local['vars'][P+'stabilisation']>5 else '_none')],status=resolve(loc[P+host+('_warning' if scene=='warning' else '_trauma' if scene=='aftermath' else '_reconciling' if scene=='peace' else '_quiet')]),views=views)
            index=list(HOSTS).index(host);record['events']={}
            for perspective,eid in (('host',210+index),('usa',220+index),('local',230+index),('world',240+index)):
                event=events['COLDWAR_USA_KS.'+str(eid)];body=event.children();options=[]
                recipient='SOV' if perspective=='world' else 'USA' if perspective=='usa' else data['rebel'] if perspective=='local' else tag
                for option in [x for x in body if x.key=='option']:
                    options.append(dict(label=loc[field(option.children(),'name')],effects=effect_rows([x for x in option.children() if x.key not in ('name','trigger','ai_chance')],m.countries[recipient])))
                # Aftermath event examples use the explicitly fictional 10,000-loss case.
                description=resolve(loc[field(body,'desc')],tag)
                record['events'][perspective]=dict(title=loc[field(body,'title')],description=description,options=options,photo='photo_'+host)
            examples[host][scene]=record
    payload=dict(project='IMPERIA COLD WAR',examples=examples,assets=assets,countries=country_names)
    emitted=template.replace('__REGIONAL_PREVIEW_DATA__',json.dumps(payload,separators=(',',':')).replace('</','<\\/'))
    assert len(emitted.encode('utf-8'))<1_000_000
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(emitted,encoding='utf-8')
    sources=[loc_path,ROOT/f'interface/{STEM}.gui',ROOT/'interface/countrydecisionview.gui',ROOT/'interface/eventwindow.gui',ROOT/f'events/{STEM}.txt',ROOT/f'common/scripted_localisation/{STEM}.txt',*[ROOT/f'common/{family}/{STEM}.txt' for family in ('decisions','scripted_effects','scripted_triggers','ideas')]]
    notice=dict(project='IMPERIA COLD WAR',purpose='Source-composed interactive preview, not a live HOI4 screenshot',data='Illustrative states; availability evaluated by the emitted-script model, not the engine',geometry='Custom panel 493 x 112, native category/row donors; surrounding browser composition approximate',sources=[str(path) for path in sources],source_sha256={str(path):hashlib.sha256(path.read_bytes()).hexdigest() for path in sources},assets=provenance,output_sha256=hashlib.sha256(output.read_bytes()).hexdigest())
    output.with_suffix('.notice.json').write_text(json.dumps(notice,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(project='IMPERIA COLD WAR',output=str(output),bytes=len(emitted.encode('utf-8')),hosts=4,example_states=4,views=3),indent=2))


if __name__=='__main__':main()
