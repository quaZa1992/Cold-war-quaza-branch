# IMPERIA CW — Cold War: faithful-coordinate concept preview and English catalogue.
from pathlib import Path
import base64, hashlib, html, io, json, math, re
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/design/COLDWAR_KOR_1970'
HERE=Path(__file__).resolve().parent
VIZ=Path('C:/Users/sonyz/.codex/visualizations/2026/10/24/01a16eac-abda-7393-822c-036cb1025900')
D=json.loads((OUT/'COLDWAR_KOR_design.json').read_text(encoding='utf-8'))
COLORS={'bg':'#202b30','text':'#e3dfca','muted':'#aab5b7','line':'#84999e','gold':'#cfba7d','exclusive':'#cb8e70'}
SOURCES={
 'park':'gfx/interface/goals/south_korea/south_korea_authoritarnism.dds',
 'state':'gfx/interface/goals/00_politics/government_beu.dds',
 'parliament':'gfx/interface/goals/coldwar/generic_parliament.png',
 'democracy':'gfx/interface/goals/00_politics/Election_graphics.dds',
 'army':'gfx/interface/goals/coldwar/generic_army_high_command.png',
 'labour':'gfx/interface/goals/coldwar/generic_workers_rights.png',
 'students':'gfx/interface/goals/coldwar/focus_generic_democratic_science.dds',
 'revolution':'gfx/interface/goals/00_politics/national_unity_red.dds',
 'security':'gfx/interface/goals/00_security/Generic_Intelligence_Gathering.dds',
 'industry':'gfx/interface/goals/coldwar/factory_complex.png',
 'diplomacy':'gfx/interface/goals/south_korea/rok_emblem.dds',
 'korea':'gfx/interface/goals/south_korea/korean_peninsula2.dds',
 'rural':'gfx/interface/goals/coldwar/LEP_subsidize_villages.png',
 'research':'gfx/interface/goals/coldwar/expand_research_funding.tga',
 'roads':'gfx/interface/goals/coldwar/generic_road_construction.png',
 'oversight':'gfx/interface/goals/coldwar/generic_civilian_oversight.png',
 'air':'gfx/interface/goals/coldwar/generic_air_command.png',
 'navy':'gfx/interface/goals/coldwar/generic_submarine_base.png',
 'nuclear':'gfx/interface/goals/coldwar/KOR/50s/investment_on_nuclear_power_research.dds',
 'elections':'gfx/interface/goals/coldwar/generic_elections.png',
 'training':'gfx/interface/goals/coldwar/generic_army_training.png',
 'welfare':'gfx/interface/goals/00_politics/welfare.dds',
 'police':'gfx/interface/goals/00_security/police_funding_bonus.dds',
 'cooperation':'gfx/interface/goals/coldwar/generic_union_agreement.png',
 'housing':'gfx/interface/goals/coldwar/generic_construct_public_housing.png',
 'energy':'gfx/interface/goals/coldwar/generic_electricity.png',
}
IMG={}
FONT=ImageFont.truetype('C:/Windows/Fonts/georgia.ttf',14)
SMALL=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
HEADER=ImageFont.truetype('C:/Windows/Fonts/georgia.ttf',24)

def pngdata(im):
    b=io.BytesIO();im.save(b,format='PNG',optimize=True)
    return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()

def art():
    manifest={}
    for family,source in SOURCES.items():
        path=ROOT/source;assert path.is_file(),source
        im=Image.open(path).convert('RGBA');im.thumbnail((94,90),Image.Resampling.LANCZOS)
        IMG[family]=im
        small=im.quantize(colors=80,method=Image.Quantize.FASTOCTREE)
        manifest[family]={'source':source,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'data':pngdata(small)}
    for n in D['nodes']:
        key=n['key'];family=n['icon_family']
        if any(x in key for x in ('constitution','yushin','cabinet','administration','planning_board','planning','credit','finance','restructur','rational')):family='state'
        if any(x in key for x in ('coalition','assembly','parliament','court','republic','party_settlement')):family='parliament'
        if any(x in key for x in ('election','declaration','handover','mandate','civilian_exit')):family='elections'
        if any(x in key for x in ('union','arbitration','workers','labor','labour','safety')):family='labour'
        if any(x in key for x in ('insurance','welfare','health','pension','defector')):family='welfare'
        if any(x in key for x in ('police','emergency','files','press')):family='police'
        if any(x in key for x in ('training','ncos','reserve','professional','civil_defence')):family='training'
        if any(x in key for x in ('bargain','compact','cooperation','contracts','contacts','trade','reunion','hotline','guarantees')):family='cooperation'
        if any(x in key for x in ('rural','village','cooperative')):family='rural'
        if any(x in key for x in ('research','technical','college','laborator','engineering','scholarship')):family='research'
        if any(x in key for x in ('freight','corridor','logistics','provinces')):family='roads'
        if any(x in key for x in ('oversight','court','disclose','accounts','transparency')):family='oversight'
        if key in ('air_defence','air_command'):family='air'
        if key in ('coastal_defence','coastal_logistics'):family='navy'
        if key=='civil_nuclear':family='nuclear'
        if key in ('urban_services',):family='housing'
        if key in ('energy_planning','thermal_diversification'):family='energy'
        n['icon_family']=family;n['art_source']=SOURCES[family]
    D['art']=manifest
    # True native titlebar texture; image conversion is a preview asset only.
    frame=ROOT/'gfx/interface/focusview/titlebar/focus_can_start_bg.dds'
    if not frame.exists():frame=Path('C:/Program Files (x86)/Steam/steamapps/workshop/content/394360/2777392649/gfx/interface/focusview/titlebar/focus_can_start_bg.dds')
    if not frame.exists():frame=Path('C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV/gfx/interface/focusview/titlebar/focus_can_start_bg.dds')
    im=Image.open(frame).convert('RGBA')
    D['titlebar_data']=pngdata(im)
    sheet=Image.new('RGB',(1000,math.ceil(len(IMG)/6)*180),COLORS['bg']);draw=ImageDraw.Draw(sheet)
    for i,(family,im) in enumerate(IMG.items()):
        x=(i%6)*166;y=(i//6)*180;sheet.paste(im,(x+(166-im.width)//2,y+12),im)
        draw.text((x+10,y+112),family,font=SMALL,fill=COLORS['text'])
    sheet.save(OUT/'COLDWAR_KOR_art_contact_sheet.png')

def summary(n):
    e=n['effects'];r=[]
    if e['cost']:r.append(f'Treasury: -${e["cost"]:g}bn (once)')
    if e['weekly']:r.append(f'Active programme: ${e["weekly"]:.5f}bn/week (replacement slot)')
    inv={v:k for k,v in D['modifier_labels'].items()}
    for p in e['policies']:
        r.append('Replace '+p['qualified_slot']+':')
        for k,v in p['modifiers'].items():
            label=D['modifier_labels'].get(k,k)
            r.append(f'{label}: {v:+g} percentage points' if k=='interest_rate_multiplier_modifier' else f'{label}: {v*100:+g}%')
        if p.get('active_condition'):r.append('Active only after '+p['active_condition'])
    for b in e['buildings']:r.append(f'State {b["state"]}: +{b["level"]} {b["type"]} (paid, once)')
    for k,v in e['one_time'].items():r.append(f'{k}: {v:+g} (once)')
    for a in e['actions']:r.append(a['type']+': '+a['value'])
    if n.get('start_replacements'):r.append('Replace starting problem: '+', '.join(n['start_replacements']))
    return r

def catalogue():
    text=['# South Korea — January 1970–1990 national focus concept','',
      f'**{len(D["nodes"])} focuses; {sum(len(n["mutually_exclusive"]) for n in D["nodes"])//2} mutual-exclusion links; {len(D["groups"])} programme clusters. Approval-stage design only.**','',
      'All names, descriptions, conditions and effect text below are English. Numbers are multiplayer balance proposals grounded in documented institutions, not estimates of historical causal effects. The historical starting leader remains Park Chung Hee. No loaded game content has been edited.','',
      'The complete spatial preview and catalogue use the same resolved JSON coordinates. Native MD grid is 96×130 pixels, item 165×128, name field 147×20. Browser fonts and connector routing approximate the game; final engine appearance requires an in-game check.','',
      '## Programme map','',
      '| Programme | Anchor | Focuses | Government |','|---|---:|---:|---|']
    for g in D['groups']:
        ns=[n for n in D['nodes'] if n['group']==g['id']]
        text.append(f'| {g["label"]} | {tuple(g["anchor"])} | {len(ns)} | {g["gate"]} |')
    text+=['','## Important design decisions','',
      '- Park/DRP, NDP, the Two Kims, Chun/Roh, USP, students, independent Marxists, RPR, exceptional KCIA rule and Kim Jong-pil have playable continuations. Fringe religious, monarchy and Ilmin paths are excluded.',
      '- The Two Kims are possible successive incumbents. Their policy choices are exclusive; becoming president does not permanently ban the other person from returning later.',
      '- A36-focus national transition programme now connects the historical succession, opposition coalition, constitutional negotiations, ratification, election and civilian institutions; all actual crises and ballots still resolve through events/decisions and native politics.',
      '- Political programmes deactivate when their exact owner leaves government; earned policy values return with that owner. Buildings, cash, XP and other one-time outcomes never replay.',
      '- National economic choices remain earned institutions across ordinary government changes. A separately approved policy-reversal decision would be needed to undo an exclusive national choice; changing party is not a free respec.',
      '- A government adopting competitive civilian institutions cannot retain emergency-constitution bonuses, even if the same individual remains president.',
      '- Offers require the other player’s response. Refused treaty-only follow-ups bypass with no payout, allowing common domestic continuation. No automatic annexation, unification, equipment shipment, treaty withdrawal or troop deployment.',
      '- National development uses supported MD/Imperia modifiers and paid construction. No focus directly assigns a development tier, resets debt, reruns GDP initialization, grants future technology or creates starting armed forces.','',
      '## Starting national spirits','']
    for s in D['starting_spirits']:
        text += ['### '+s['label'],'',s['history'],'','`'+s['id']+'` — '+s['owner'],'']
        for k,v in s['modifiers'].items():
            label=D['modifier_labels'].get(k,k);value=f'{v:+g} percentage points' if k=='interest_rate_multiplier_modifier' else f'{v*100:+g}%'
            text.append(f'- {label}: {value}')
        if not s['modifiers']:text.append('- Preserve the actual existing idea and remittance system; no invented duplicate values.')
        text+=['',s['resolution'],'']
    text+=['## Party integration before implementation','',D['party_migration']['confirmed_problem'],'',D['party_migration']['proposal'],'',D['party_migration']['safety'],'']
    for g in D['groups']:
        text+=['## '+g['label'],'','Entry condition: '+g['gate']+'.','']
        for n in [n for n in D['nodes'] if n['group']==g['id']]:
            text+=['### '+n['label'],'',f'`{n["id"]}` · **{n["days"]} days** · grid {tuple(n["xy"])} · owner: {n["ownership"]}','',n['description'],'',
              'Prerequisites: '+(' AND '.join('('+ ' OR '.join(x.removeprefix('COLDWAR_KOR_') for x in row)+')' for row in n['prerequisites']) or 'Independent programme entry')+'.',
              'Exclusive with: '+(', '.join(x.removeprefix('COLDWAR_KOR_') for x in n['mutually_exclusive']) or 'none')+'.','']
            text+=['- '+s for s in summary(n)]
            for requirement in n.get('requirements',[]):text.append('- Requirement: '+requirement)
            if n.get('bypass'):text+=['','Bypass: '+str(n['bypass'])]
            if n.get('conditional_completion'):text+=['','Completion alternatives: '+json.dumps(n['conditional_completion'],ensure_ascii=False)]
            if n.get('state_effects'):text+=['','Institutional outcomes: `'+json.dumps(n['state_effects'])+'`']
            if n.get('temporary_effect'):text+=['','Temporary adjustment: `'+json.dumps(n['temporary_effect'])+'`']
            text+=['']
    text+=['## Agreement option effects','',
      'Terms are offered by KOR; both players remain free to refuse. The following are proposed new content contracts built with existing MD primitives. Each has 60-day pending expiry, a 180-day failed-offer cooldown, two-party revalidation, a once-only signature, visible response effects and proposer notification. All recurring charges/income use native weekly rates.','']
    for c in D['contracts']:
        text+=['### '+c['key'].replace('_',' ').title(),'',f'`{c["id"]}` · recipient: **{c["recipient"]}** · term: {str(c["duration_days"])+" days" if c["duration_days"] else "political framework; no perpetual passive stat grant"}','',c['description'],'',
          f'- KOR payment on acceptance: ${c["KOR_cost_bn"]:g}bn once; ${c["KOR_weekly_bn"]:.5f}bn/week.',
          '- KOR accepted policy: `'+json.dumps(c['KOR_policy'])+'`.',
          '- Recipient accepted effects: `'+json.dumps(c['recipient_effects'])+'`.','',c['refusal'],'']
        if c.get('KOR_on_accept'):text+=['- KOR membership effect: `'+json.dumps(c['KOR_on_accept'])+'`.','']
    text+=['## Event and decision timeline','']
    for e in D['transition_events']:
        text+=['### '+e['label'],'',e['historical_context'],'','Trigger: '+e['trigger'], '']
        for c in e['choices']:text+=['- **'+c['label']+':** '+c['effects']]
        text+=['']
    if D.get('transition_system'):
        text+=['## Military-to-democratic transition rules','',
          'Research was completed before expansion. Constitutional approval, an election result and civilian command are separate milestones.','']
        for key,value in D['transition_system'].items():text+=['- **'+key+':** '+(value if isinstance(value,str) else json.dumps(value,ensure_ascii=False))]
        text+=['','### Constitutional decisions and implementation costs','']
        for decision in D['transition_decisions']:
            text+=['- **'+decision['id']+':** '+decision['cost']+'. '+decision['reader']]
        text+=['','Command-resolution choice: '+D['proposed_transition_events']['COLDWAR_KOR_transition.12']['success_cost'],'']
        text+=['','## Research-led expansion','',json.dumps(D['expansion_summary'],ensure_ascii=False,indent=2),'']
    text+=['## Verification boundary','',
      'Source inspections and automated graph checks can establish native API patterns, defined modifier keys, coordinates, prerequisites and slot arithmetic. They cannot prove engine acceptance, exact hover tooltips, save behavior or runtime political transitions. No HOI4 game test is claimed. New Korean adapters, events, ideas, decisions and party migration are designs awaiting implementation approval.','',
      'Reference reports: `research_history.md`, `md_reference_layout.md`, `mechanics_feasibility.md`; final review status is recorded separately in `COLDWAR_KOR_review_resolution.md`.','']
    (OUT/'COLDWAR_KOR_concept.md').write_text('\n'.join(text),encoding='utf-8')
    recipes=['# South Korea — native MD implementation recipes','',
      '**Approval-stage specifications. No COLDWAR_KOR runtime helper is claimed to exist yet.**','',D['economic_effect_semantics'],'',
      '## Existing primitives and source evidence','']
    for key,value in D['native_api_evidence'].items():recipes+=['- **'+key+':** '+value]
    recipes+=['','## Native political change contract','','```hoi4',D['native_party_change_recipe'],'```','',D['party_migration']['additional_router_fix'],'',
      '## New Korean providers to implement','']
    for key,value in D['new_helpers'].items():recipes+=['- `'+key+'`: '+value]
    recipes+=['','## Exceptional and civilian accession routes','']
    for r in D['political_entry_routes']:
        recipes+=['### '+r['id'],'',r['available'],'','Cost: '+r['cost'],'',r['effect'],'']
    recipes+=['## Native examples','']
    for key,value in D['native_examples'].items():recipes+=['### '+key,'','```hoi4',value,'```','']
    recipes+=['## NKO agreement compatibility','']
    for key,value in D['NKO_compatibility_adapter'].items():recipes+=['- **'+key+':** '+str(value)]
    recipes+=['','## Legal accountability follow-up','',json.dumps(D['rights_followup_decision'],indent=2),'']
    recipes+=['## Shared transition providers, decisions and events','']
    for section in ('transition_receipt_providers','transition_decisions','proposed_transition_events','transition_maintenance_recipe','transition_maintenance_note'):
        if section in D:recipes+=['### '+section.replace('_',' ').title(),'','```json',json.dumps(D[section],ensure_ascii=False,indent=2),'```','']
    recipes+=['','## Per-focus native guards and leaves','',
      'These country-scope bodies supplement exact grouped prerequisites and reciprocal exclusions in the JSON. Leaf variable assignments require the declared latest-slot selector and mapped dynamic modifiers. Additional semantic requirements remain explicit; this is not ready-to-install generated game code.','']
    for n in D['nodes']:
        recipes+=['### '+n['id'],'','```hoi4',n['proposed_trigger']+' = {',n['native_gate_body'],'}',
          '# One-time completion leaves; new programme/offer handlers remain separate.',n['native_leaf_effects'] or '# No unilateral leaf reward; see the accepted contract or action definition.','```','']
        if n.get('native_bypass_body'):recipes+=['Native focus-level bypass (no reward):','','```hoi4','bypass = {',n['native_bypass_body'],'}','```','']
    (OUT/'COLDWAR_KOR_native_recipes.md').write_text('\n'.join(recipes),encoding='utf-8')

def image_view(ids,path,scale=1,title='',subtitle='CONCEPT · Native grid and art · Font and connectors approximate'):
    ns=[n for n in D['nodes'] if n['group'] in ids]
    minx=min(n['xy'][0] for n in ns)*96-110;miny=min(n['xy'][1] for n in ns)*130-95
    maxx=max(n['xy'][0] for n in ns)*96+110;maxy=max(n['xy'][1] for n in ns)*130+100
    full=len(ids)==len(D['groups'])
    if full:
        panel_x,panel_y=D['layout']['continuous_focus_position']
        maxx=max(maxx,panel_x+550);maxy=max(maxy,panel_y+550)
    if maxx-minx<720:
        extra=(720-(maxx-minx))/2;minx-=extra;maxx+=extra
    im=Image.new('RGB',(int(maxx-minx),int(maxy-miny)+75),COLORS['bg']);dr=ImageDraw.Draw(im)
    byid={n['id']:n for n in ns}
    def pt(n):return (n['xy'][0]*96-minx,n['xy'][1]*130-miny+75)
    for n in ns:
        x,y=pt(n)
        for row in n['prerequisites']:
            for parent in row:
                if parent not in byid:continue
                px,py=pt(byid[parent]);middle=(py+86+y-35)/2
                dr.line([(px,py+82),(px,middle),(x,middle),(x,y-35)],fill=COLORS['line'],width=2)
        for target in n['mutually_exclusive']:
            if target in byid and n['id']<target:
                other=byid[target]
                if any(q['xy'][1]==n['xy'][1] and min(n['xy'][0],other['xy'][0])<q['xy'][0]<max(n['xy'][0],other['xy'][0]) and q['id'] in n['mutually_exclusive'] and target in q['mutually_exclusive'] for q in ns):continue
                tx,ty=pt(byid[target]);left,right=min(x,tx),max(x,tx);dr.line((left+68,y+25,right-68,ty+25),fill=COLORS['exclusive'],width=2)
                dr.text(((x+tx)/2-6,y+12),'×',font=HEADER,fill=COLORS['exclusive'])
    for n in ns:
        x,y=pt(n);icon=IMG[n['icon_family']]
        im.paste(icon,(round(x-icon.width/2),round(y-25)),icon)
        dr.rectangle((x-82,y+66,x+82,y+95),fill='#34413e',outline='#807450')
        label=n['label']
        while dr.textlength(label,font=FONT)>147:label=label[:-2]+'…'
        dr.text((x-dr.textlength(label,font=FONT)/2,y+70),label,font=FONT,fill=COLORS['text'])
    dr.text((20,15),title,font=HEADER,fill=COLORS['text'])
    dr.text((20,45),subtitle,font=SMALL,fill=COLORS['muted'])
    if full:
        px=panel_x-minx;py=panel_y-miny+75
        dr.rectangle((px,py,px+550,py+550),outline=COLORS['line'],width=2)
        dr.text((px+20,py+20),'Native continuous-focus panel',font=HEADER,fill=COLORS['text'])
        dr.text((px+20,py+58),'Reserved footprint · existing MD content',font=SMALL,fill=COLORS['muted'])
    if scale!=1:im=im.resize((int(im.width*scale),int(im.height*scale)),Image.Resampling.LANCZOS)
    im.save(OUT/path)

def main():
    art();catalogue()
    # Exact displayed rewards remain in the inline view; duplicated audit/code
    # maps stay in the full JSON instead of pushing the fragment over1MB.
    keep=('status','country','start','horizon','prefix','groups','starting_spirits','modifier_labels','layout','rules','party_migration','contracts','transition_events','art','titlebar_data','revision','expansion_summary','transition_system','state_outcome_labels','transition_decisions','proposed_transition_events')
    payload={k:D[k] for k in keep if k in D}
    node_keep=('id','key','group','label','description','xy','days','prerequisites','mutually_exclusive','gate','ownership','effects','icon_family','requirements','bypass','conditional_completion','start_replacements','state_effects','temporary_effect','native_gate_body','native_leaf_effects','economic_effect_note','added_in_revision','historicity','transition_link')
    payload['nodes']=[{k:n[k] for k in node_keep if k in n} for n in D['nodes']]
    assert all(a['id']==b['id'] and a['xy']==b['xy'] and a['effects']==b['effects'] and a['prerequisites']==b['prerequisites'] for a,b in zip(D['nodes'],payload['nodes']))
    blob=json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    template=(HERE/'COLDWAR_KOR_tree_fragment.html').read_text(encoding='utf-8')
    frag=template.replace('<!-- COLDWAR_KOR_DATA -->','<script type="application/json" id="coldwar-kor-data">'+blob+'</script>')
    assert len(frag.encode('utf-8'))<1_000_000,len(frag.encode('utf-8'))
    VIZ.mkdir(parents=True,exist_ok=True)
    dest=VIZ/'coldwar-south-korea-focus-concept.html';dest.write_text(frag,encoding='utf-8')
    (OUT/'COLDWAR_KOR_preview_data.json').write_text(json.dumps(D,ensure_ascii=False,indent=2),encoding='utf-8')
    for gid,name in [('drp','DRP'),('reform','Two_Kims'),('korea','North_Korea'),('army','Chun_Roh'),('economy','Economy'),('kjp','Kim_Jong_pil'),('transition','Democratic_Transition'),('defence','Defence'),('foreign','Foreign')]:
        image_view([gid],'COLDWAR_KOR_'+name+'_detail.png',title=next(g['label'] for g in D['groups'] if g['id']==gid))
    image_view([g['id'] for g in D['groups']],'COLDWAR_KOR_entire_tree.png',scale=.35,title='SOUTH KOREA · 1970–1990')
    print(json.dumps({'visualization':str(dest),'bytes':len(frag.encode('utf-8')),'catalogue':str(OUT/'COLDWAR_KOR_concept.md')}))

if __name__=='__main__':main()
