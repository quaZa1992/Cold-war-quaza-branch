# IMPERIA COLD WAR — Native layout preview for the independent island revision.
"""Refresh the existing MD preview without rewriting either approved baseline."""
from copy import deepcopy
from pathlib import Path
import base64
import io
import json
import sys
from cuba_runtime_design import MODEL, CONCEPT
from layout_repair import MILITARY_KEYS
from generic_navy_preview import build_nodes, native_art, title_image, LABELS as NAVAL_LABELS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT/'docs/design/cuba_foreign_1970/revision'
sys.path.insert(0,str(ROOT/'tools/cuba_1970_concept'))
import native_font as font


def rows(e):
    k=e['kind']; country=e.get('country','CUB')
    state_names={854:'Habana',855:'Camagüey',1121:'Pinar del Río',1252:'Cayo Blanco del Sur'}
    province_names={7590:'Guantánamo',9603:'Santiago de Cuba'}
    if k=='treasury': return [f'{country}: Treasury {e["amount"]:+.2f} billion']
    if k=='building':
        level=e.get('level',e.get('levels'))
        names={'bunker':'Land Fort','coastal_bunker':'Coastal Fort','agriculture_district':'Agriculture District','infrastructure':'Infrastructure','industrial_complex':'Civilian Industry'}
        place=province_names.get(e.get('province'),state_names.get(e['state'],str(e['state'])))
        return [f'{state_names.get(e["state"],e["state"])}: +{level} building slot'+('s' if level!=1 else ''),f'{place}: +{level} {names.get(e["building"],e["building"])}']
    if k=='rename_state':return [f'{state_names.get(e["state"],e["state"])}: rename to {e["name"]}']
    if k=='transfer_state':return [f'{e["to"]}: transfer Cayo Blanco del Sur; retain Cuban core']
    if k=='research':return [f'{country}: +{100*e["bonus"]:g}% {e["category"].removeprefix("CAT_").replace("_"," ").title()} research bonus, {e["uses"]} use'+('s' if e['uses']!=1 else '')]
    if k=='experience':return [f'{country}: +{e[t]} {t.title()} Experience' for t in ('army','navy','air') if e.get(t)]
    if k=='lift_mutual_sanctions':return ['Cuba and USA: remove mutual '+', '.join(e['classes'])+' sanctions and native embargoes']
    if k=='harvest_course':return ['Harvest course: '+e['course']]
    if k=='stability':return [f'Stability: {100*e["amount"]:+g}%']
    return []


def main():
    data=deepcopy(CONCEPT)
    data['nodes']=deepcopy(MODEL['nodes'])
    data['groups']=deepcopy(MODEL['groups'])
    data['project']='IMPERIA COLD WAR'
    data['layout_repair']=MODEL['layout_repair']
    old={n['key']:n for n in json.loads((ROOT/'docs/design/cuba_foreign_1970/FOREIGN_POLICY_CONCEPT.json').read_text(encoding='utf8'))['nodes']}
    for n in data['nodes']:
        n['title']=n['native_title']
        n['title_width']=font.width(n['native_title'])
        buff=io.BytesIO();font.raster(n['native_title']).save(buff,format='PNG')
        n['title_art']='data:image/png;base64,'+base64.b64encode(buff.getvalue()).decode()
        if n['key'] in ('finish_zafra','restore_sectors'):
            n['effect_rows']=sum((rows(e) for e in n['effects']),[])
        elif n['key'] in ('medical_brigades','retain_doctors'):
            n['effect_rows']+=deepcopy(old['health_workforce']['effect_rows'])
        elif n['key'] in ('coastal_patrols','civil_military_pact'):
            n['effect_rows']=sum((rows(e) for e in n['effects']),[])
        if n.get('partner'):
            name=n.get('spirit') or n['title']
            n['partner_spirit']=n.get('partner_spirit') or (name if name.startswith('Cuban') else 'Cuban '+name)
            n['effect_rows']=sum((rows(e) for e in n.get('immediate_effects',[])),[])
            n['receipt']=sum((rows(e) for e in n.get('accepted_effects',[])),[])
            if n['key']=='foreign_cmea': n['receipt']=['Cuba: COMECON Membership','Soviet Union: Cuban Coordination Commission']
            if n['key']=='foreign_limited':n['receipt']+=['Cuba: remove American Embargo; add Limited Restrictions']
            if n['key']=='foreign_settlement':n['receipt']+=['Cuba: remove American Embargo and Limited Restrictions']
        n['sources']=[s if s.startswith('http') else 'https://germanhistorydocs.org/en/two-germanies-1961-1989/east-german-government-delegation-visits-cuba-1974' for s in n.get('sources',[])]
    # IMPERIA COLD WAR — Add the source-faithful generic naval block and feeder focuses.
    imported=build_nodes()
    for n in imported:
        n['title_width']=font.width(n['native_title'])
        art,wrapped=title_image(n['native_title'],font)
        buff=io.BytesIO();art.save(buff,format='PNG')
        n['title_art']='data:image/png;base64,'+base64.b64encode(buff.getvalue()).decode()
        n['title_wrapped']=wrapped
    data['nodes'].extend(imported)
    data['groups'] += [
        {'id':'naval','label':'Generic naval tree','slot':None},
        {'id':'navy_feeders','label':'Naval prerequisite feeders','slot':None},
    ]
    data['art'].update(native_art(n['icon'] for n in imported))
    data['labels'].update(NAVAL_LABELS)
    keys=lambda *parts:[n['key'] for n in data['nodes'] if n['key'] in parts]
    data['foreign_views'][0]['keys']=[n['key'] for n in data['nodes'] if n['group']=='foreign']
    data['foreign_views'][2]['keys']+=['foreign_ddr_industry','foreign_ddr_science']
    data['foreign_views'] += [
        dict(id='ddr',label='Island and DDR partnerships',keys=keys('foreign_symbolic','foreign_cession','foreign_ddr','foreign_ddr_industry','foreign_ddr_science')),
        dict(id='defence',label='Armed forces and overseas service',keys=list(MILITARY_KEYS)),
        dict(id='usa',label='US blockade negotiations',keys=keys('foreign_interests','foreign_limited','foreign_settlement')),
        dict(id='health',label='Health policy continuation',keys=keys('rural_clinics','teaching_hospitals','medical_brigades','retain_doctors')),
        dict(id='navy',label='Generic naval tree and feeder focuses',keys=[n['key'] for n in imported]),
    ]
    view_labels={'foreign':'Foreign policy','trade':'Trade and credit','atlantic':'DDR and United States',
        'missions':'Overseas service and medicine','ddr':'Island and DDR partnerships',
        'defence':'Armed forces and overseas service','usa':'US blockade negotiations',
        'health':'Health policy continuation','navy':'Generic naval tree and feeders'}
    for view in data['foreign_views']:
        view['label']=view_labels.get(view['id'],view['label'])
    data['native_approximation']='The naval branch uses native Millennium Dawn focus icons, donor titles and descriptions. Browser inspection is not a native game hover test.'
    data['focus_total']=146
    data['budget_rows']=[['Cuba revision',120],['Generic naval subtree',20],['Required feeder focuses',6],['Total',146]]
    data['protocol']=[
        '27 foreign focuses and 146 total. The 20-focus generic naval subtree retains its donor geometry, descriptions, focus costs, prerequisites and exclusive carrier choice. Six prerequisite feeder focuses are included.',
        'The island routes remain independent of Soviet assistance. Berlin and Havana requires a ratified island agreement. Its two follow-ups require the active Berlin and Havana agreement.',
        'Cuban offer focuses send proposals to the named recipient country. Only the recipient makes the accept or refuse decision.',
        'Accepted bilateral benefits stay active while both countries exist and remain at peace without mutual sanctions or embargoes.',
    ]
    text=(HERE/'foreign_concept/fragment.html').read_text(encoding='utf8')
    text=text.replace('foreign policy proposal, not loaded game code.','native preview of the implemented Cuba revision.')
    text=text.replace('DESIGN PROPOSAL','IMPLEMENTED REVISION').replace('25 Außenpolitik-Foki · Vorschlag mit insgesamt 120 Foki','27 foreign focuses · 146 focuses total')
    text=text.replace("view:'foreign',selected:'COLDWAR_CUB_foreign_expeditionary'","view:'ddr',selected:'COLDWAR_CUB_foreign_cession'")
    text=text.replace('version:2','version:3').replace('p.version!==2','p.version!==3')
    text=text.replace("['Economy',15,9],['Society',7,5],['Defence',8,5],['Foreign policy',13,25]","['Economy',15,8],['Society',7,4],['Defence',8,5],['Foreign policy',13,27]")
    text=text.replace('Dieser Entwurf ist nicht in den geladenen Spielbaum eingebaut.','This revision is installed in the Cuba focus tree.')
    text=text.replace('Originale MD-Grafiken · Alle Foki anklickbar','Native MD icons · All focuses clickable')
    text=text.replace('Ansicht','View').replace('Baumansicht','Focus tree view')
    text=text.replace('Verkleinern','Zoom out').replace('Vergrößern','Zoom in').replace('Einpassen','Fit view')
    text=text.replace('Fokusdetails','Focus details').replace('Vertragsregeln','Agreement rules').replace('120-Foki-Budget','146-focus budget')
    text=text.replace('Historischer Bezug und Konzeptprüfung','Historical context and design notes')
    text=text.replace('Zusammengeführt mit:','Merged from:').replace('Quelle ','Source ')
    text=text.replace('Kubanischer Fokusbaum. Ziehen verschiebt die View. Jeder Fokus lässt sich anklicken.','Cuban focus tree. Drag to pan. Click any focus to inspect it.')
    text=text.replace('aria-label="Konzeptinformationen"','aria-label="Preview information"')
    text=text.replace("detail.innerHTML='<h2>Fokus, Angebot, Zustimmung, Vertrag</h2>'+list(D.protocol)+'<h3>Freiwillige</h3><div class=\"fp-columns\"><div><p>Overseas Service</p>'+mods(by.get('COLDWAR_CUB_foreign_overseas').modifiers)+'</div><div><p>Advisory Missions oder Expeditionary Brigades</p><p>+1 oder +2 mögliche Freiwilligendivisionen. Das globale Minimum ist in MD bereits auf sieben Divisionen reduziert. Die neue Schwellenreduktion wirkt auf dieses Minimum. Vorhandene Truppen und die normale Empfängerzustimmung bleiben nötig.</p></div></div>';save()", "detail.innerHTML='<h2>Focus, proposal, consent and agreement</h2>'+list(D.protocol)+'<h3>Overseas service</h3><div class=\"fp-columns\"><div><p>Overseas Service policy</p>'+mods(by.get('COLDWAR_CUB_foreign_overseas').modifiers)+'</div><div><p>Advisory missions or expeditionary brigades</p><p>+1 or +2 eligible volunteer divisions. The normal recipient approval and availability of trained Cuban units still apply.</p></div></div>';save()")
    text=text.replace("label:'Gesamter Baum: 120 Foki'","label:'Full focus tree: 146 focuses'")
    text=text.replace("b.innerHTML='<img class=\"fp-art\" alt=\"\" draggable=\"false\" src=\"'+D.art[n.icon]+'\"><img class=\"fp-bar\" alt=\"\" draggable=\"false\" src=\"'+D.titlebars.available+'\"><img class=\"fp-title\" alt=\"\" draggable=\"false\" src=\"'+n.title_art+'\">';", "b.innerHTML='<img class=\"fp-art\" alt=\"\" draggable=\"false\" src=\"'+D.art[n.icon]+'\"><img class=\"fp-bar\" alt=\"\" draggable=\"false\" src=\"'+D.titlebars.available+'\"><img class=\"fp-title\" alt=\"\" draggable=\"false\" src=\"'+n.title_art+'\">';if(n.title_wrapped){const ti=b.querySelector('.fp-title');ti.style.top='96px';ti.style.height='26px'}")
    text=text.replace("let html='<h2>'+esc(n.title)+'</h2><div class=\"fp-meta\">'+n.days+' days · '+(n.is_existing?'Bestehender Fokus im Gesamtvorschlag':'Neuer außenpolitischer Fokus')+' · Grid '+n.xy.join(', ')+'</div><p>'+esc(n.description)+'</p>';", "let html='<h2>'+esc(n.title)+'</h2><div class=\"fp-meta\">'+n.cost+' focus cost · '+n.days+' days · '+(n.source_focus_id?'Copied generic focus':n.is_existing?'Existing Cuba focus':'New Cuba focus')+' · Grid '+n.xy.join(', ')+'</div><p>'+esc(n.description)+'</p>';" )
    text=text.replace("detail.innerHTML='<h2>120 Foki mit erhaltenen politischen Pfaden</h2><table", "detail.innerHTML='<h2>146 focuses: Cuba revision plus generic naval tree</h2><table")
    text=text.replace("[['Economy',15,8],['Society',7,4],['Defence',8,5],['Foreign policy',13,27],['OSPAAAL',3,2],['Other political programmes',74,74],['Total',120,120]]", "[['Cuba revision',120],['Generic naval focuses',20],['Required feeder focuses',6],['Total',146]]")
    text=text.replace('<th>Bereich</th><th>Bisher</th><th>Vorschlag</th>','<th>Scope</th><th>Focuses</th>')
    text=text.replace('Fidels 13 Foki und die übrigen politischen Alternativen bleiben erhalten. OSPAAAL behält seine zwei konkurrierenden Programme. Bei Zusammenlegungen bleiben Gebäude samt Bauplätzen, Forschung, Kosten und die gesamte Fokusdauer auf der jeweiligen Route erhalten.','The 13 focuses centered on Fidel Castro and all political alternatives remain in the 120-focus Cuba revision. The copied naval tree preserves its 20-focus donor graph. Six feeder focuses satisfy its external prerequisites.')
    text=text.replace('Vorgeschlagene Zusammenlegungen','Preserved focus consolidations')
    text=text.replace('Die räumliche Vorschau enthält alle 120 vorgeschlagenen Foki. Politische Abschnitte sind für den zusätzlichen Außenpolitikplatz um zwei Rasterzeilen nach unten versetzt.','The preview shows the full 146-focus tree.')
    text=text.replace("esc(n.description)+'</p>'","esc(n.description)+'</p><p class=\"fp-meta\">'+esc(n.lifetime||'')+'</p>'")
    # The same native sprite assets and independent relative coordinates are reused.
    for n in data['nodes']:
        for k in ('script','title_art_unused','modrows'):n.pop(k,None)
    payload=json.dumps(data,ensure_ascii=False,separators=(',',':'))
    text=text.replace('__DATA__',payload)
    assert '\u2013' not in text and '\u2014' not in text
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'PREVIEW.html').write_text('<!-- IMPERIA COLD WAR — Cuba focus tree preview. -->\n<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0">'+text+'</body></html>',encoding='utf8')
    (OUT/'PREVIEW_DATA.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    (OUT/'IMPERIA_COLD_WAR_NOTICE.md').write_text('# IMPERIA COLD WAR: native preview provenance\n\nThe preview and PNG captures are generated from the approved Cuba revision plus the user-requested local copy of the installed Millennium Dawn generic naval tree and six required prerequisite feeders. Focus icons, title bars and the bitmap font reference or render installed Millennium Dawn and Hearts of Iron IV assets. Millennium Dawn contributors are credited in the donor record; individual artists and applicable upstream permissions are unknown here. This record grants no ownership or redistribution permission. See the repository IMPERIA_COLD_WAR_NOTICE.md and installed mods for original credits. Modifications: namespaced focus identifiers, preserved relative geometry, preview effect summaries and title wrapping.\n',encoding='utf8')
    print(json.dumps({'project':'IMPERIA COLD WAR','focuses':len(data['nodes']),'naval_nodes':len(imported),'native_titles_fit':True,'path':str(OUT/'PREVIEW.html')}))


if __name__=='__main__':main()
