# IMPERIA CW — Cold War: Native MD art preview of an approval-only North Korean concept.
from build_concept import *

def art_library():
    text=(ROOT/'interface/goals.gfx').read_text(encoding='utf-8-sig')
    paths=dict(re.findall(r'name\s*=\s*"([^"]+)"\s*\n\s*texturefile\s*=\s*"([^"]+)"',text,re.I))
    wanted={v['icon'] for v in NODES}|set(ICON.values())
    images={}; sources={}
    for name in wanted:
        assert name in paths, 'Unresolved native sprite '+name
        p=ROOT/paths[name]
        assert p.exists(),p
        im=Image.open(p).convert('RGBA')
        b=io.BytesIO(); im.quantize(colors=192,method=Image.Quantize.FASTOCTREE).save(b,format='PNG',optimize=True)
        images[name]='data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
        sources[name]=dict(sprite=name,path=str(p),size=list(im.size),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    for key,file in [('available','focus_can_start_bg.dds'),('unavailable','focus_unavailable_bg.dds')]:
        p=ROOT/'gfx/interface/focusview/titlebar'/file
        if not p.exists():
            p=Path(r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV')/'gfx/interface/focusview/titlebar'/file
        im=Image.open(p).convert('RGBA'); b=io.BytesIO(); im.save(b,format='PNG',optimize=True)
        images[key]='data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
        sources[key]=dict(path=str(p),size=list(im.size))
    (OUT/'art_manifest.json').write_text(json.dumps(sources,indent=2),encoding='utf-8')
    return images,sources

def effects(v):
    rows=[]
    if v['money']:rows.append(f"Treasury: −${v['money']:.3f} billion once; native borrowing remains available.")
    for k,a in v['modifiers'].items():
        amount=f'{a:+.2f} percentage points' if k=='interest_rate_multiplier_modifier' else f'{a:+.0%}'
        rows.append(f"{v['labels'][k]}: {amount}"+(' of its native weekly baseline.' if 'Weekly' in v['labels'][k] else '.'))
    for a in v['extra']:
        if a['kind']=='building':rows.append(f"Fund {a['levels']} {a['type'].replace('_',' ')} level. Candidate states in priority order: {', '.join(map(str,a['state_ids']))}. Full price ${a['full_project_cost']:.3f} billion; ownership, control, free capacity, staffing, power and maintenance apply. No second building charge.")
        elif a['kind']=='research':rows.append(f"{a['category']}: {a['uses']} × {a['bonus']:.0%} research bonus; no free technology.")
        elif a['kind']=='offer':rows.append(f"Offer — {a['name']}: {a['benefit']} Payer: {a['payer']}, ${a['cost']:.3f} billion on acceptance. Recipient may refuse; no reward or charge then. Offer expires after {a['expire_days']} days.")
        elif a['kind']=='debt':rows.append(f"Machinery credit: borrow ${a['amount']:.3f} billion, spend the loan on the financed factory; native principal and interest remain.")
        elif a['kind']=='repay_loan':rows.append(f"Repay at most ${a['amount']:.3f} billion of the recorded machinery principal; payment and principal reduction occur once, not twice.")
        else:rows.append(a['name']+' — '+a['detail'])
    if v['remove']:rows.append('Starting constraint replaced/removed: '+', '.join(v['remove'])+'.')
    if v['duration']:rows.append(f"Programme duration: {v['duration']} days.")
    return rows

def code(v):
    lines=['# IMPERIA CW — Cold War: proposed '+v['title'], '# Review recipe: NEW country adapters and state reservation are not implemented.', 'available = {','  hidden_trigger = {']
    lines += ['    '+s for s in v['runtime_guards'] if not s.startswith('check_variable = { ruling_party')]
    lines+=['  }']
    if v['slot'] is not None:
        lines += ['  custom_trigger_tooltip = {',f"    tooltip = {P}party_{v['slot']}_in_power_tt",f"    check_variable = {{ ruling_party = {v['slot']} }}",'  }']
    lines += ['  # Signed agreements and material gates also get meaningful localized requirement tooltips.']
    lines += ['}', 'completion_reward = {','  if = {','    limit = {']+['      '+s for s in v['runtime_guards']]+['    }']
    if v['money']:lines += [f"  set_temp_variable = {{ treasury_change = -{v['money']:g} }}",'  modify_treasury_effect = yes']
    if v['modifiers']:lines += ['  # New modifier definition below; this ID is proposed, not currently installed.',f"  add_dynamic_modifier = {{ modifier = {v['id']}_programme }}"]
    for a in v['extra']:
        if a['kind']=='research':lines += ['  add_tech_bonus = {',f"    name = {v['id']} category = {a['category']} uses = {a['uses']} bonus = {a['bonus']}",'  }']
        elif a['kind']=='building':lines += ['  # NEW adapter reserves the first valid owned AND controlled state before payment.', '  # Candidate state IDs: '+', '.join(map(str,a['state_ids'])), '  # It checks free_building_slots / level cap / coastline, then applies:', '  # IN THAT STATE SCOPE:',f"  # add_building_construction = {{ type = {a['type']} level = {a['levels']} instant_build = yes }}"]
        elif a['kind']=='offer':lines += [f"  # NEW adapter needed: {a['name']}; no unilateral completion payout.",f"  # Pending / accept / refuse / expire / feedback; receipt {a['flag']}"]
        elif a['kind']=='debt':lines += [f"  # Native take_manual_debt_effect; record and spend {a['amount']:g}bn principal only if loan succeeds.", '  # Exact parameterization and factory transaction checked at implementation.']
        elif a['kind']=='repay_loan':lines += ['  # One repayment transaction: cash debit and matching recorded principal reduction.']
        else:lines += ['  # NEW country adapter: '+a['name']]
    lines+=['  }']
    lines+=['}']
    if v['modifiers']:
        lines+=['',f"{v['id']}_programme = {{",'  icon = GFX_idea_economic_increase','  enable = { original_tag = NKO IMP_is_1970_scenario = yes'+(f" check_variable = {{ ruling_party = {v['slot']} }}" if v['slot'] is not None else '')+' '+' '.join(v.get('policy_enable_guards',[]))+' }']
        lines += [f'  {k} = {a:g}' for k,a in v['modifiers'].items()]
        lines+=['}']
    return '\n'.join(lines)

def catalogue(data):
    text=['# COLDWAR — DPRK, January 1970–1990: approval concept',
      '',f"**{len(NODES)} focuses. Concept only. No loaded game files have been changed.**",'',
      'All focus titles and descriptions are proposed English localization. Numerical values are balance proposals; API support is source-audited, engine behavior is not yet tested.',
      '', '## Decisions to approve', '',
      '- A historical WPK programme and seven conditional alternatives use the existing government slots, with 30 pairwise mutual exclusions across distinct policy dilemmas.',
      '- KDP and Chondoist party governments, a military or technocratic government, and the smaller civic/left alternatives are explicitly counterfactual. Their branches unlock when the actual registered party governs; a focus does not manufacture that accession.',
      '- Physical development, loan principal and signed interstate obligations survive government changes. Party programme modifiers deactivate on loss of office and return with the party, without replaying factories, money or research bonuses.',
      '- No Salafi, Shia or other Muslim paths; no new independent paths for implausible registry filler. No resurrection of purged leaders, forced reunification, starting OOB changes, free uranium mines or instant weapons.',
      '', '## Exact spatial plan', '',
      'Native grid: 96 × 130 px; native item container 165 × 128 px; name field 147 × 20 px. Each section has an absolute root; all other coordinates are emitted relative to that root. Separate prerequisite blocks mean AND; members of one block mean OR. Visible connectors preserve those groups.',
      '', '| Section | Root | Focuses | Government |', '|---|---:|---:|---|']
    for g in GROUPS:text.append(f"| {g['title']} | ({g['x']}, {g['y']}) | {sum(v['group']==g['id'] for v in NODES)} | "+(f"slot {g['slot']}" if g['slot'] is not None else 'all governments')+' |')
    text+=['','Initial camera: WPK root (6,0). Shortcuts: WPK, Economy, Armed Forces, Diplomacy, Atomic Programme, and each alternative programme. Continuous focuses occupy the lower-right pocket after the alternative branches; proposed position (5800,3750) px, pending engine verification. No unapproved shared joint-focus tree is attached.',
      '', 'All-government overview deliberately shows every proposed branch. In the game, native conditional branch visibility is only a presentation aid; actual party availability and reward guards remain authoritative. Dynamic hiding/reappearing of focus nodes is not promised until the native reevaluation mechanism is verified. The inspector includes all government states.',
      '', '## Starting national spirits', '']
    for s in START_SPIRITS:
        text+=['### '+s['title'],'',s['description'],'']
        text += [f"- {STATS[k][1]}: {v:+.0%}" for k,v in s['mods'].items()]
        text+=['',s['remedy'],'']
    text+=['## Native rewards and integration contract','',
      'Country policies use explicit dynamic modifier definitions. Small ongoing expenditure changes are modifiers of the relevant **weekly native budget**, not invented flat daily/monthly fees. Investment costs are one-time billions through `treasury_change` / `modify_treasury_effect`; normal MD borrowing applies. Numeric expense modifiers are relative percentages, not absolute billions. The native budget calculation determines the weekly cash amount.',
      '', 'Buildings are paid grants only if a suitable owned state has actual capacity. Reserve/validate that state before charging the player. The descriptive regional selectors below must be resolved to real state predicates during implementation; no imported foreign state IDs are used.',
      '', 'Foreign agreements are proposed adapters around native effects, not existing named NKO APIs. The recipient sees concrete numeric option effects and may refuse. Charge and grant only at acceptance after both sides are rechecked, once per signed receipt; send accepted/refused/expired feedback and clear pending flags. A government change during negotiations invalidates a party-specific offer. Subsequent cooperation requires a still-valid signed agreement.',
      '', 'Party lifecycle: save completed-focus receipts; reconcile at startup, government change, monthly maintenance and load. Reattach earned conditional modifiers if the engine removes disabled entries. Reconciliation must never run one-time completion rewards. In-progress party focus: cancel on loss of rule, with the same party guard in its actual reward. Retain old branch completion and earned receipts for a later return.',
      '', 'Starting-spirit replacements are conditional on receipts. On load or party return, never restore the original monolithic spirit after one of its two replacements was earned. Shared policy choices remain mutually exclusive across government changes.',
      '', '## Conditional incidents','']
    for incident in INCIDENTS:
        text += ['### '+incident['name'],'',incident['trigger'],'',incident['note'],'']
        if 'choices' in incident:
            for choice in incident['choices']:
                text += ['- '+choice['name']+': '+json.dumps({k:v for k,v in choice.items() if k!='name'},ensure_ascii=False)]
        else:text += ['- '+incident['mitigation'],'- '+json.dumps(incident['modifiers'])]
        text+=['']
    text+=['## Focus catalogue','']
    for g in GROUPS:
        text+=['### '+g['title'],'',g['note'],'']
        for v in [v for v in NODES if v['group']==g['id']]:
            pre=' AND '.join('('+' OR '.join(a.removeprefix(P) for a in p)+')' for p in v['prerequisites']) or 'Section entry'
            text += [f"#### {v['title']}",'',f"`{v['id']}` · ({v['x']},{v['y']}) · relative ({v['dx']},{v['dy']}) · {v['days']} days · {v['ownership']}",'',v['description'],'',f'Prerequisites: {pre}.']
            if v['mutex']:text+=['Mutually exclusive: '+', '.join(v['mutex'])+'.']
            if v['slot'] is not None:text += [f"Availability and guarded reward: actual ruling subparty = {v['slot']}."]
            if v['gate']:text += ['Additional requirement: '+v['gate']]
            text+=['']+['- '+a for a in effects(v)]+['']
    text+=['## Evidence and remaining validation','',
      'See [MD layout reference](md_layout_reference.md), [mechanics trace](mechanics_reference.md) and [historical research](history_research.md). Full design source: `COLDWAR_NKO_1970_design.json`. Preview uses the same resolved coordinates, title strings and dependency groups; genuine local MD art is embedded. Browser typography and connector routing approximate HOI4, and the overview is reduced in scale. Select a section for readable artwork and inspect exact rewards.',
      '', 'Concept validation covers IDs, references, AND/OR histories and full item bounds. It does not establish engine tooltips, save/load timing, balance in a real multiplayer campaign, native branch visibility refresh or nuclear programme availability. These remain implementation/engine checks after approval.',
      '', 'No loaded national focus, history, idea, localization, event, GUI or economic file has been edited. Approval is requested for this concrete design, not for claimed completed implementation.']
    (OUT/'COLDWAR_NKO_1970_CONCEPT.md').write_text('\n'.join(text)+'\n',encoding='utf-8')

def preview(data,images):
    for v in data['nodes']:v['effects']=effects(v);v['code']=code(v)
    source=(OUT/'preview_template.html').read_text(encoding='utf-8')
    fragment=source.replace('__DATA__',json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__ART__',json.dumps(images,separators=(',',':')))
    VIS.mkdir(parents=True,exist_ok=True)
    (VIS/'coldwar-nko-1970.html').write_text(fragment,encoding='utf-8')
    # A durable local review copy; never loaded by HOI4.
    (OUT/'COLDWAR_NKO_1970_preview.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>COLDWAR DPRK 1970 concept</title><style>body{margin:0;background:#202420;color:#e5e5d9;font:14px Arial,sans-serif}button,select{font:inherit}</style></head><body>'+fragment+'</body></html>',encoding='utf-8')
    (OUT/'preview_syntax_check.js').write_text(fragment.split('<script>',1)[1].split('</script>',1)[0],encoding='utf-8')

def proposed_localization():
    # This review copy is outside localisation/; only localisation YAML uses a BOM.
    lines=['# IMPERIA CW — Cold War: North Korean 1970 CONCEPT, not installed.', 'l_english:']
    for v in NODES:
        lines += [' '+v['id']+':0 '+json.dumps(v['title'],ensure_ascii=False),
                  ' '+v['id']+'_desc:0 '+json.dumps(v['description'],ensure_ascii=False)]
    for s in START_SPIRITS:
        lines += [' '+s['id']+':0 '+json.dumps(s['title'],ensure_ascii=False),
                  ' '+s['id']+'_desc:0 '+json.dumps(s['description'],ensure_ascii=False)]
    for g in GROUPS:
        if g['slot'] is not None:
            lines += [' '+P+'party_'+str(g['slot'])+'_in_power_tt:0 '+json.dumps(g['title']+' is the governing party or institution.',ensure_ascii=False)]
    (OUT/'COLDWAR_NKO_1970_proposed_l_english.yml').write_text('\n'.join(lines)+'\n',encoding='utf-8-sig')

def static_images(data,images,sources):
    font=ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',14)
    small=ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',12)
    title=ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf',22)
    icons={k:Image.open(ROOT/v['path']).convert('RGBA') for k,v in sources.items() if k not in ('available','unavailable')}
    bg=Image.open(sources['unavailable']['path']).convert('RGBA')
    def draw(nodes,name,scale=1):
        minx=min(v['x'] for v in nodes);maxx=max(v['x'] for v in nodes)
        miny=min(v['y'] for v in nodes);maxy=max(v['y'] for v in nodes)
        w=int((maxx-minx)*96+210);h=int((maxy-miny)*130+220)
        im=Image.new('RGBA',(w,h),(34,40,36,255));d=ImageDraw.Draw(im)
        def pos(v):return (int((v['x']-minx)*96+105),int((v['y']-miny)*130+78))
        ids={v['id']:v for v in nodes}
        for v in nodes:
            x,y=pos(v)
            for p in v['prerequisites']:
                for a in p:
                    if a not in ids:continue
                    ax,ay=pos(ids[a]);end=y;start=ay+128;mid=(end+start)//2
                    d.line([(ax,start),(ax,mid),(x,mid),(x,end)],fill=(145,150,136),width=2)
            for a in v['mutex']:
                if a not in ids or v['id']>a:continue
                ax,ay=pos(ids[a]);yy=y+113
                if any(b['y']==v['y'] and min(v['x'],ids[a]['x'])<b['x']<max(v['x'],ids[a]['x']) and b['id'] in v['mutex'] for b in nodes):continue
                d.line([(min(x,ax)+83,yy),(max(x,ax)-83,yy)],fill=(181,100,87),width=2)
        for v in nodes:
            x,y=pos(v);ico=icons[v['icon']].copy();ico.thumbnail((112,98))
            im.alpha_composite(ico,(x-ico.width//2,y+3))
            bar=bg.copy();im.alpha_composite(bar,(x-bar.width//2,y+73))
            s=v['title'];f=font if d.textlength(s,font=font)<=147 else small
            if d.textlength(s,font=f)>147:
                while d.textlength(s+'…',font=f)>147:s=s[:-1]
                s+='…'
            d.text((x,y+98),s,fill=(233,231,210),font=f,anchor='mm')
        for g in GROUPS:
            gs=[v for v in nodes if v['group']==g['id']]
            if gs:
                x,y=pos(gs[0]);d.text((x,y-40),g['title'],font=title,fill=(210,196,145),anchor='mm')
        if scale!=1:im=im.resize((int(w*scale),int(h*scale)),Image.Resampling.LANCZOS)
        im.convert('RGB').save(OUT/name)
    draw(NODES,'COLDWAR_NKO_1970_overview.png',.42)
    for g in GROUPS:draw([v for v in NODES if v['group']==g['id']],'branch_'+g['id']+'.png')
    sheet=Image.new('RGB',(800,math.ceil(len(icons)/6)*150),(38,44,39));d=ImageDraw.Draw(sheet)
    for i,(name,im) in enumerate(sorted(icons.items())):
        ico=im.copy();ico.thumbnail((100,105));x=(i%6)*132+15;y=(i//6)*150+5
        sheet.paste(ico,(x,y),ico);d.text((x,y+112),name[:22],font=small,fill=(240,235,215))
    sheet.save(OUT/'native_art_contact_sheet.png')

if __name__=='__main__':
    report=validate();data=dict(namespace=P,status='CONCEPT — approval required; not installed',groups=GROUPS,nodes=NODES,starting_spirits=START_SPIRITS,incidents=INCIDENTS,stats=STATS,validation=report)
    images,sources=art_library()
    catalogue(data);preview(data,images);static_images(data,images,sources);proposed_localization()
    print(json.dumps(dict(nodes=len(NODES),icons=len(sources),preview=str(VIS/'coldwar-nko-1970.html'))))
