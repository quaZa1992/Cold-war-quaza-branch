# IMPERIA CW — Cold War: iraq 1970 — starting spirits.
"""Visible native country ideas for the approved Iraqi starting burdens.

Constant stages make the actual modifiers visible in country selection and in
the national-spirit panel. Runtime reconciliation selects one stage per burden;
the original derived variables remain the authoritative calculation/cache.
"""
import json
from pathlib import Path
from common import ROOT,P,block,locline,check

def generate(root=ROOT):
    data=json.loads(Path(__file__).with_name('approved_iraq.json').read_text(encoding='utf-8-sig'))
    spirits={s['id']:s for s in data['starting_spirits']};ideas=[];effects=[];legacy=[];loc={}
    families={};selection=[]
    def idea(base,suffix,mods):
        key=base+('_'+suffix if suffix else '')
        s=spirits[base]
        ideas.append(block(key,'picture = '+base+'\nallowed = { tag = IRQ }\nremoval_cost = -1\n'+block('modifier','\n'.join(k+' = '+f'{v:g}' for k,v in mods.items()))))
        loc[key]=s['label'];loc[key+'_desc']=s['description']
        families.setdefault(base,[]).append(key)
        return key
    def choose(base,cases):
        """cases is [(actual predicate, target idea or None)], first match wins."""
        for i,(gate,target) in enumerate(cases):
            payload=''
            for other in families[base]:
                if other!=target:payload+=block('if',block('limit','has_idea = '+other)+'remove_ideas = '+other)
            if target:payload+=block('if',block('limit','NOT = { has_idea = '+target+' }')+'add_ideas = '+target)
            selection.append(block('if' if i==0 else 'else_if',block('limit',gate)+payload))
    for base,s in spirits.items():
        if base.endswith('literacy'):
            ideas.append(block(base,'picture = '+base+'\nallowed = { tag = IRQ }\nremoval_cost = -1\ncancel = { has_country_flag = EDU_cleared_previously }\nmodifier = { }'))
            loc[base]=s['label'];loc[base+'_desc']=s['description']+' Literacy: [?literacy_rate|%0]. The native Education modifier applies the research, expenditure and workforce effects.'
            continue
        # Old saves can still deserialize the previous dynamic IDs. Disable and
        # explicitly detach them before attaching the native static equivalent.
        legacy.append(block(base,'icon = GFX_idea_'+base+'\nenable = { always = no }\n'+ '\n'.join(k+' = '+base+'_'+k for k in s['modifiers'])))
        idea(base,'',s['modifiers'])
    july=P+'spirit_july_state'
    choose(july,[('check_variable = { ruling_party = 21 }\nNOT = { has_country_flag = COLDWAR_IRQ_national_front_implemented }\nNOT = { has_country_flag = COLDWAR_IRQ_baath_monopoly_implemented }',july),('always = yes',None)])
    north=P+'spirit_unsettled_north'
    autonomy=idea(north,'autonomy',dict(spirits[north]['modifiers'],stability_factor=-.08))
    federal=idea(north,'federal',{'stability_factor':-.03,'army_personnel_cost_multiplier_modifier':.04,'supply_consumption_factor':.01})
    loc[autonomy+'_desc']='The autonomy settlement is being respected. Disputes over revenue, security and the reach of Baghdad still burden the state; renewed conflict would restore the full northern crisis.'
    loc[federal+'_desc']='A respected federal settlement has reduced the northern crisis. Shared security and administration still require resources, and the arrangement depends on Baghdad continuing to honour its guarantees.'
    choose(north,[(check(north+'_stability_factor',-.03,'equals'),federal),(check(north+'_stability_factor',-.08,'equals'),autonomy),('always = yes',north)])
    ipc=P+'spirit_ipc'
    transition=idea(ipc,'transition',{'oil_export_multiplier_modifier':-.06})
    concession=idea(ipc,'concession',{'oil_export_multiplier_modifier':-.09})
    choose(ipc,[(check(ipc+'_oil_export_multiplier_modifier',0,'greater_than_or_equals'),None),(check(ipc+'_oil_export_multiplier_modifier',-.06,'equals'),transition),(check(ipc+'_oil_export_multiplier_modifier',-.09,'equals'),concession),('always = yes',ipc)])
    patron=P+'spirit_patronage'
    audited=idea(patron,'audited',dict(spirits[patron]['modifiers'],bureaucracy_cost_multiplier_modifier=.07))
    command=idea(patron,'command',dict(spirits[patron]['modifiers'],army_org_factor=0))
    professional=idea(patron,'audited_command',dict(spirits[patron]['modifiers'],bureaucracy_cost_multiplier_modifier=.07,army_org_factor=0))
    a=check(patron+'_bureaucracy_cost_multiplier_modifier',.07,'equals');c=check(patron+'_army_org_factor',0,'equals')
    choose(patron,[(a+'\n'+c,professional),(a,audited),(c,command),('always = yes',patron)])
    rural=P+'spirit_rural';cases=[(check(rural+'_agricolture_productivity_modifier',0,'greater_than_or_equals')+'\n'+check(rural+'_consumer_goods_factor',0,'less_than_or_equals'),None)]
    for agr,level in [(-.04,'extension'),(-.08,'credit'),(-.12,'land')]:
        for cg,dist in [(.01,'distribution'),(.03,'original')]:
            target=rural if agr==-.12 and cg==.03 else idea(rural,level+'_'+dist,{'agricolture_productivity_modifier':agr,'consumer_goods_factor':cg})
            cases.append((check(rural+'_agricolture_productivity_modifier',agr,'equals')+'\n'+check(rural+'_consumer_goods_factor',cg,'equals'),target))
    cases.append(('always = yes',rural));choose(rural,cases)
    frontier=P+'spirit_frontier'
    choose(frontier,[('NOT = { COLDWAR_IRQ_border_settlement_active = yes }',frontier),('always = yes',None)])
    cleanup=''.join(block('if',block('limit','has_dynamic_modifier = { modifier = '+base+' }')+'remove_dynamic_modifier = { modifier = '+base+' }') for base in families)
    refresh=cleanup+'\n'+''.join(selection)
    effects.append(block(P+'refresh_starting_spirit_cards',block('if',block('limit','COLDWAR_IRQ_campaign_active = yes')+refresh)))
    basecards=' '.join(s['id'] for s in data['starting_spirits'])
    seed=cleanup+'''if = {
 limit = { NOT = { has_country_flag = COLDWAR_IRQ_starting_spirits_seeded } }
 set_country_flag = COLDWAR_IRQ_starting_spirits_seeded
 if = { limit = { NOT = { has_variable = literacy_rate } } set_variable = { literacy_rate = 0.35 } }
 add_ideas = { '''+basecards+''' }
}
'''
    # This helper is also called directly inside the already dated 1970 history
    # snapshot. Do not depend on on_startup or an established has_start_date for
    # that pre-game display; real campaign updates keep the strict live gate.
    effects.append(block(P+'seed_starting_spirits',block('if',block('limit','tag = IRQ\noriginal_tag = IRQ\nis_dynamic_country = no\nOR = { COLDWAR_IRQ_campaign_active = yes AND = { date > 1969.12.31 date < 1985.1.1 } }')+seed)))
    return {
      'common/ideas/COLDWAR_IRQ_1970_starting_ideas.txt':block('ideas',block('country',''.join(ideas))),
      'common/dynamic_modifiers/COLDWAR_IRQ_1970_situations.txt':''.join(legacy),
      'common/scripted_effects/COLDWAR_IRQ_1970_starting_spirits.txt':''.join(effects),
      'localisation/english/COLDWAR_IRQ_1970_starting_spirits_l_english.yml':'l_english:\n# IMPERIA CW — Cold War: iraq 1970 English localisation.\n'+'\n'.join(locline(k,v) for k,v in loc.items())+'\n',
    }
