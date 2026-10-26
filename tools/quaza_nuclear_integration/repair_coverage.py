# IMPERIA CW — Cold War: complete reviewed uranium UI blocks and require developed mines.
import json,re
from port import ROOT,SOURCE,AUDIT,read,write
from adapt import blocks,block

MARKER='# IMPERIA CW — Cold War: complete uranium presentation and mine-based production.'

def gui(text,name):
    hits=list(re.finditer(r'\bname\s*=\s*"'+re.escape(name)+r'"',text))
    assert len(hits)==1,(name,len(hits))
    def walk(nodes):
        for n in nodes:
            yield n
            yield from walk(n['children'])
    return max((n for n in walk(blocks(text)) if n['open']<=hits[0].start()<n['close']),key=lambda n:n['open'])

def edit_gui(text,name,fn):
    n=gui(text,name)
    old=text[n['start']:n['end']]
    new=fn(old)
    assert old!=new,name
    return text[:n['start']]+new+text[n['end']:]

def replace_one(text,old,new):
    assert text.count(old)==1,(old,text.count(old))
    return text.replace(old,new,1)

def save(rel,text):
    old=read(ROOT/rel)
    if old==text:return
    before=AUDIT/'coverage_before'/rel
    if not before.exists():write(before,old)
    write(ROOT/rel,text)

def main():
    rel='interface/countrytradeview.gui';s=read(ROOT/rel)
    s=replace_one(s,'size = { width = 422 height = 100%% }\n\t\t\t\tslotsize = { width = 73 height = 156 }\n\t\t\t\tmax_slots = { x = 8 y = 1 }',
       MARKER+'\n\t\t\t\tsize = { width = 603 height = 100%% }\n\t\t\t\tslotsize = { width = 67 height = 156 }\n\t\t\t\tmax_slots = { x = 9 y = 1 }')
    def filter_entry(t):
        t=replace_one(t,'quadTextureSprite ="GFX_missiles_gui_ledger_btn"','quadTextureSprite ="GFX_missiles_gui_ledger_btn"\n\t\t\t'+MARKER+'\n\t\t\tscale = 0.88')
        return replace_one(t,'position = { x = 25 y = 12 }','position = { x = 18 y = 10 }')
    save(rel,edit_gui(s,'resources_filter_entry',filter_entry))

    rel='interface/countryproductionlineview.gui';s=read(ROOT/rel)
    def production_entry(t):
        for old,new in [('size = { width = 70 height = 30 }',MARKER+'\n\t\tsize = { width = 57 height = 30 }'),
                        ('position = { x=4 y=2 }','position = { x=2 y=2 }'),
                        ('position = { x=35 y=7 }','position = { x=29 y=7 }'),
                        ('maxWidth = 50','maxWidth = 28')]:t=replace_one(t,old,new)
        # The old 70px click overlay also overlapped the following 58px resource slot.
        overlay=gui(t,'button')
        return t[:overlay['start']]+t[overlay['end']:]
    save(rel,edit_gui(s,'resource_strip_item',production_entry))

    rel='interface/MD_countryeconomyview.gui';s=read(ROOT/rel)
    for name,old,new in [('light_metals',84,74),('rubber',168,148),('technology_metals',252,222),
                         ('steel',336,296),('precious_metals',420,370),('microchips',504,444),('advanced_composities',587,518)]:
        s=edit_gui(s,name,lambda t,old=old,new=new:replace_one(t,f'position = {{ x={old} y=0 }}',MARKER+f'\n            position = {{ x={new} y=0 }}'))
    save(rel,s)

    # Same extra row as the current donor. Preserve the Cold War state actions.
    rel='interface/countrystateview.gui';s=read(ROOT/rel)
    for old,new in [('position = { x=-416 y=-715}','position = { x=-416 y=-752}'),
                    ('show_position = { x=-6 y =-715 }','show_position = { x=-6 y =-752 }'),
                    ('size = { width=456 height=710 }','size = { width=456 height=747 }'),
                    ('size = { width = 280 height = 270 }','size = { width = 280 height = 307 }'),
                    ('position = { x = 8 y = 320 }','position = { x = 8 y = 357 }'),
                    ('position = { x = 102 y = 335 }','position = { x = 102 y = 372 }'),
                    ('position = { x = -99999 y = 538 }','position = { x = -99999 y = 575 }'),
                    ('position = { x= 0 y=325}','position = { x= 0 y=362}'),
                    ('position = { x = 14 y = 560 }','position = { x = 14 y = 597 }')]:
        s=replace_one(s,old,MARKER+'\n\t\t'+new)
    save(rel,s)

    # Imperia's resource-concession controls must also recognize uranium-only states.
    rel='common/scripted_guis/imp_resource_scripted_gui.txt';s=read(ROOT/rel)
    s=re.sub(r'(?m)^(\s*)composites > 0$',lambda m:m[0]+'\n'+m[1]+MARKER+'\n'+m[1]+'uranium > 0',s)
    s=re.sub(r'(?m)^(\s*)has_resources_rights = \{ state = PREV resources = \{ composites \} \}$',lambda m:m[0]+'\n'+m[1]+MARKER+'\n'+m[1]+'has_resources_rights = { state = PREV resources = { uranium } }',s)
    save(rel,s)
    rel='events/imp_resources_events.txt';s=read(ROOT/rel)
    s=replace_one(s,'has_resources_rights = { state = event_target:TB_target_province resources = { composites } }',
       'has_resources_rights = { state = event_target:TB_target_province resources = { composites } }\n\t\t\t\t\t'+MARKER+'\n\t\t\t\t\thas_resources_rights = { state = event_target:TB_target_province resources = { uranium } }')
    save(rel,s)

    changed=[]
    for p in (ROOT/'history/states').glob('*.txt'):
        s=read(p)
        if not re.search(r'\buranium\s*=\s*[1-9]\d*',s):continue
        s=re.sub(r'\buranium\s*=\s*\d+','uranium = 0',s)
        # Existing import markers precede each affected resource block.
        s=s.replace('# IMPERIA CW — Cold War: quaZa uranium supply chain and raid integration.',MARKER)
        save(p.relative_to(ROOT).as_posix(),s);changed.append(p.name)

    rel='common/scripted_effects/COLDWAR_quaza_imp_uranium_effects.txt';s=read(ROOT/rel)
    start=s.index('#########################################################################################')
    end=s.index('@imp_uranium_per_enrichment_facility')
    intro='''# Cold War production starts at zero. Surveyed deposits unlock mine capacity;
# only completed, working mines add uranium to state resources. The non-1970
# deposit table is retained for compatibility; it does not grant production.
# Supply chain: uranium mines -> trade/reserves -> enrichment -> reactor fuel.
# Nuclear research, warheads and naval reactors also require natural uranium.
# Mine output: 3–12 units per working level, at most 1–3 levels by deposit.
# Damage reduces new mine output; reconciliation must never duplicate it.

'''
    save(rel,s[:start]+MARKER+'\n'+intro+s[end:])
    rel='localisation/english/COLDWAR_quaza_imp_uranium_l_english.yml';s=read(ROOT/rel)
    s=replace_one(s,'Geological surveys have identified a uranium-bearing district. Mining concessions and processing facilities can develop the deposit within its capacity.',
       'Geological surveys have identified a uranium-bearing district. The deposit produces no uranium until mines and processing facilities are built within its capacity.')
    save(rel,s)
    balance=json.loads(read(AUDIT/'coldwar_balance.json'))
    balance['starting_resources']={}
    balance['method']='Zero initial raw uranium production. The 52 surveyed Cold War districts unlock paid mine development; geological estimates describe capacity, not free output.'
    write(AUDIT/'coldwar_balance.json',json.dumps(balance,indent=2))
    write(AUDIT/'coverage_repair.json',json.dumps({'zeroed_states':changed,'zeroed_state_count':len(changed),
      'fixed':['Trade ninth column and filter geometry','Production resource-entry geometry and obsolete overlapping overlay','Nine market-price positions','State building-list eighth row','Imperia uranium-only resource concession controls'],
      'policy':'No free starting uranium. Production requires developed, working mines; surveyed deposits are retained.'},indent=2))
    ignore=read(AUDIT/'.gitignore')
    if 'coverage_before/' not in ignore:write(AUDIT/'.gitignore',ignore+'coverage_before/\n')
    print('Completed uranium coverage repair; zeroed',len(changed),'state histories.')

if __name__=='__main__':main()
