# IMPERIA CW — Cold War: iraq 1970 — presentation.
"""Native MD presentation for IRQ focus rewards and availability.

No runtime mutation and no import of compile.py. reward_preview only returns
effect_tooltip blocks: the real transaction remains in the compiler's existing
hidden helper. available_ui preserves every parsed eligibility predicate.
"""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
import re
import sys
from common import ROOT, P, PARTIES, parse, emit, first
sys.path.append(str(ROOT/'tools'))
from focus_prerequisite_ui import hide_redundant_prerequisites

LOCALIZATION: dict[str, str] = {}
MD=Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
LEADERS={
    'COLDWAR_IRQ_leader_bakr_in_office':'Ahmed Hassan al-Bakr',
    'COLDWAR_IRQ_leader_saddam_in_office':'Saddam Hussein',
    'COLDWAR_IRQ_leader_aziz_muhammad_in_office':'Aziz Muhammad',
}
FORMATIONS={
    'COLDWAR_IRQ_puk_formed':'The Patriotic Union of Kurdistan has formed',
    'COLDWAR_IRQ_sciri_formed':'The Supreme Council for the Islamic Revolution in Iraq has formed',
}


@lru_cache(maxsize=1)
def _native_tooltips():
    found=set()
    paths=[GAME/'localisation/english/modifiers_l_english.yml',
           MD/'localisation/english/MD_dm_modifiers_l_english.yml',
           ROOT/'localisation/english/MD_dm_modifiers_l_english.yml',
           ROOT/'localisation/english/replace/replaced_from_vanilla_modifiers_l_english.yml']
    for path in paths:
        if path.exists():found.update(re.findall(r'^\s*([^\s:#]+):',path.read_text(encoding='utf-8-sig'),re.M))
    return found


def _modifier_tooltip(key):
    if key=='political_power_gain':
        # MD overrides the vanilla flat-gain formatter with a percent row.
        # Keep this country's actual per-day value in the native game format.
        name=P+'presentation_political_power_gain_tt'
        LOCALIZATION[name]='$MODIFIER_POLITICAL_POWER_GAIN$: $RIGHT|+=2$'
        return name
    native=key+'_tt'
    if native in _native_tooltips():return native
    # Explicit custom provider: registered percentage, color_type=good in
    # common/modifier_definitions/mdcw_cold_war_modifiers.txt:35-40.
    if key=='mdcw_cw_support_effectiveness':
        name=P+'presentation_support_effectiveness_tt'
        LOCALIZATION[name]='$mdcw_cw_support_effectiveness$: $RIGHT|+=%1$'
        return name
    if key=='equipment_upgrade_xp_cost':
        name=P+'presentation_equipment_upgrade_xp_cost_tt'
        LOCALIZATION[name]='$MODIFIER_EQUIPMENT_UPGRADE_XP_COST$: $RIGHT|-=%1$'
        return name
    raise ValueError('Unreviewed numeric tooltip format for '+key)


def reward_preview(n: dict, groupid: str, condition: str = '') -> str:
    """Return visible native heading/delta tooltips, with zero executed grants."""
    modifiers=n.get('modifiers',{})
    if not modifiers:return ''
    heading=('custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt '
             'MODIFIER = '+P+groupid+'_programme }\n')
    rows=[]
    for key,value in modifiers.items():
        rows.append(('add_to_variable','=',[(P+groupid+'_'+key,'=',f'{value:g}'),
                                          ('tooltip','=',_modifier_tooltip(key))]))
    if condition:
        # Negotiations are unlocked by these focuses, so their completion may
        # precede the agreement that activates their programme. Keep the native
        # conditional effects visible instead of promising an immediate grant.
        labels = {
            'national_front': 'While the National Front agreement is in force:',
            'baath_monopoly': 'While no National Front agreement is in force:',
        }
        label = P+'presentation_'+n['key']+'_active_tt'
        LOCALIZATION[label] = labels[n['key']]
        # Prospective values must remain visible before the agreement exists.
        # A conditional effect_tooltip suppresses its false branch in game.
        heading+='custom_effect_tooltip = '+label+'\n'
    return heading+emit([('effect_tooltip','=',rows)])+'\n'


def treasury_preview(n: dict) -> str:
    """Native signed MD cost; the guarded transaction remains the sole payer.

    Main MD UK/AFG use the same temporary arithmetic inside effect_tooltip.
    A previously quoted project keeps its actual stored bill; an untouched
    project displays its current GDP-based estimate without fixing a quote.
    """
    share=n.get('budget_gdp_share',0)
    if not share:return ''
    key=n['id']
    rows=[('set_temp_variable','=',[('treasury_change','=','gdp_total')]),
          ('multiply_temp_variable','=',[('treasury_change','=',f'{-share:g}')]),
          ('if','=',[
              ('limit','=',[('has_country_flag','=',key+'_quoted')]),
              ('set_temp_variable','=',[('treasury_change','=',key+'_invoice')]),
              ('multiply_temp_variable','=',[('treasury_change','=','-1')])]),
          ('modify_treasury_effect','=','yes')]
    return emit([('effect_tooltip','=',rows)])+'\n'


@lru_cache(maxsize=1)
def _starting_ideas():
    """Read the actual generated static stage providers without writing them."""
    import starting_spirits
    text=starting_spirits.generate(ROOT)['common/ideas/COLDWAR_IRQ_1970_starting_ideas.txt']
    country=first(first(parse(text),'ideas'),'country')
    return {key:{k:float(value) for k,op,value in first(body,'modifier',[])}
            for key,op,body in country}


def _stage(base, modifiers):
    # Zero entries have no numerical effect; the command stage explicitly
    # retains its zero organisation component in the native idea provider.
    wanted={key:value for key,value in modifiers.items() if value}
    for key,actual in _starting_ideas().items():
        if key==base or key.startswith(base+'_'):
            if {k:v for k,v in actual.items() if v}==wanted:return key
    raise ValueError('Unprovided starting-spirit stage: '+base+' '+repr(wanted))


def situation_preview(n: dict) -> str:
    """Preview actual native idea swaps/removals; execute no game effects.

    Current-stage checks preserve the other component of a partially reformed
    burden. No absent card is manufactured for the tooltip. The two July State
    removals are included despite their empty catalogue ``replaces`` field.
    """
    key=n['key'];base=None;change=None;gate=''
    if key in ('national_front','baath_monopoly'):
        base=P+'spirit_july_state';change=lambda m:None
    elif key in ('ministerial_audit','professional_command'):
        base=P+'spirit_patronage'
        component,value=('bureaucracy_cost_multiplier_modifier',.07) if key=='ministerial_audit' else ('army_org_factor',0)
        change=lambda m:dict(m,**{component:value})
    elif key=='autonomy_guarantees':
        base=P+'spirit_unsettled_north'
        # A recognized federal settlement takes precedence in the real
        # reconciler. Preserve that distinction even in a stale card snapshot.
        rows=[]
        for current,mods in _starting_ideas().items():
            if current!=base and not current.startswith(base+'_'):continue
            for federal in (False,True):
                desired=({'stability_factor':-.03,'army_personnel_cost_multiplier_modifier':.04,'supply_consumption_factor':.01}
                         if federal else dict(mods,stability_factor=-.08))
                # A fulfilled existing federal settlement is never downgraded.
                if not federal and current==base+'_federal':continue
                target=_stage(base,desired)
                if target==current:continue
                condition='has_country_flag = COLDWAR_IRQ_federal_settlement'
                if not federal:condition='NOT = { '+condition+' }'
                rows+=_swap_preview(current,target,condition)
        return emit([('effect_tooltip','=',rows)])+'\n' if rows else ''
    elif key=='foreign_border_delivery':
        base=P+'spirit_frontier';change=lambda m:None
    elif key in ('oil_state_company','oil_concession_delivery','oil_field_maintenance'):
        base=P+'spirit_ipc'
        if key=='oil_state_company':
            rows=[]
            for current in _starting_ideas():
                if current!=base and not current.startswith(base+'_'):continue
                done='has_country_flag = COLDWAR_IRQ_oil_field_maintenance_implemented'
                rows+=_swap_preview(current,None,done)
                target=_stage(base,{'oil_export_multiplier_modifier':-.06})
                if current!=target:rows+=_swap_preview(current,target,'NOT = { '+done+' }')
            return emit([('effect_tooltip','=',rows)])+'\n' if rows else ''
        if key=='oil_concession_delivery':
            gate='NOT = { has_country_flag = COLDWAR_IRQ_oil_state_company_implemented }'
            change=lambda m:{'oil_export_multiplier_modifier':-.09}
        else:
            gate='has_country_flag = COLDWAR_IRQ_oil_state_company_implemented'
            change=lambda m:None
    elif key in ('agri_cooperatives','agri_smallholders','agri_cooperative_credit','agri_smallholder_credit','agri_extension','agri_distribution','agri_reform_delivery'):
        base=P+'spirit_rural'
        if key in ('agri_cooperatives','agri_smallholders','agri_cooperative_credit','agri_smallholder_credit'):
            change=lambda m:dict(m,agricolture_productivity_modifier=max(m['agricolture_productivity_modifier'],-.08))
        elif key=='agri_extension':
            change=lambda m:dict(m,agricolture_productivity_modifier=max(m['agricolture_productivity_modifier'],-.04))
        elif key=='agri_distribution':change=lambda m:dict(m,consumer_goods_factor=.01)
        else:change=lambda m:None
    if base is None:return ''
    rows=[]
    for current,mods in _starting_ideas().items():
        if current!=base and not current.startswith(base+'_'):continue
        desired=change(dict(mods));target=None if desired is None else _stage(base,desired)
        if target!=current:rows+=_swap_preview(current,target,gate)
    return emit([('effect_tooltip','=',rows)])+'\n' if rows else ''


def _swap_preview(current, target, gate=''):
    conditions=[('has_idea','=',current)]+parse(gate)
    change=(('swap_ideas','=',[('remove_idea','=',current),('add_idea','=',target)])
            if target else ('remove_ideas','=',current))
    return [('if','=',[('limit','=',conditions),change])]


def _tooltip(key: str, text: str, rows: list) -> tuple:
    LOCALIZATION[key]=text
    return ('custom_trigger_tooltip','=',[('tooltip','=',key)]+rows)


def _party_tooltip(slot, row):
    slot=int(slot)
    if slot not in PARTIES:return row
    party,family,_=PARTIES[slot]
    outlook='Western' if slot<=3 else 'Emerging' if slot<=9 else 'Non-Aligned' if slot<=19 else 'Nationalist'
    return _tooltip(P+f'presentation_government_{slot}',f'Governing party: {party} (${family}$; {outlook} outlook)',[row])


def _semantic(row):
    k,op,v=row
    if k=='COLDWAR_IRQ_campaign_active' and v=='yes':
        return ('hidden_trigger','=',[row])
    if k in ('COLDWAR_IRQ_constitution_executive_active','COLDWAR_IRQ_constitution_representative_active') and v=='yes':
        text='The current constitutional settlement permits '+('executive authority' if 'executive' in k else 'representative government')
        return _tooltip(k+'_presentation_tt',text,[row])
    if k in LEADERS and v=='yes':
        return ('has_country_leader','=',[('name','=',f'"{LEADERS[k]}"'),('ruling_only','=','yes')])
    if k=='NOT' and v==[('has_country_flag','=','MD_skip_treasury_cost')]:
        return _tooltip(P+'presentation_treasury_payments_tt','Normal treasury payments are enabled',[row])
    if k=='check_variable' and isinstance(v,list):
        direct=next((x for x in v if x[0]=='ruling_party' and x[1]=='='),None)
        if direct:return _party_tooltip(direct[2],row)
        vals={a:c for a,b,c in v}
        if vals.get('var')=='ruling_party' and vals.get('compare')=='equals':return _party_tooltip(vals['value'],row)
        var=vals.get('var','');value=vals.get('value','');compare=vals.get('compare','')
        if var.startswith(P) and var.endswith('_invoice') and value=='0' and compare=='greater_than':
            return _tooltip(var+'_positive_presentation_tt','The implementation invoice is valid (more than $0.00 billion)',[row])
        if var=='treasury' and value.startswith(P) and value.endswith('_invoice') and compare=='greater_than_or_equals':
            return _tooltip(value+'_funded_presentation_tt','Treasury: $[?treasury|2] billion; required: $[?'+value+'|2] billion',[row])
    if k=='has_country_flag' and isinstance(v,str):
        if v.startswith(P) and v.endswith('_quoted'):
            invoice=v.removesuffix('_quoted')+'_invoice'
            return _tooltip(v+'_presentation_tt','The implementation invoice is fixed at $[?'+invoice+'|2] billion',[row])
        if v.endswith('_implemented'):
            focus=v.removesuffix('_implemented')
            return _tooltip(v+'_presentation_tt','$'+focus+'$ has been implemented',[row])
        if v in FORMATIONS:return _tooltip(v+'_presentation_tt',FORMATIONS[v],[row])
    if isinstance(v,list) and k not in ('check_variable','has_country_flag','has_country_leader','custom_trigger_tooltip'):
        return k,op,[_semantic(child) for child in v]
    return row


def _human_requirement(text):
    text=text.replace('IRQ','Iraq').replace('Irans',"Iran's")
    text=re.sub(r'(?<=[A-Za-z])(?=\d)|(?<=\d)(?=[A-Za-z])',' ',text)
    text=text.replace('state 165','Kirkuk').replace('state 399','Khuzestan')
    replacements={
        'Actual active war against Iran':'Iraq is at war with Iran',
        'Actual active war involving Iraq':'Iraq is at war',
        'Recorded Iraqi-Iranian war participation':'Iraq has participated in a war against Iran',
        'Recorded Iraqi war participation and civilian/veteran obligations':'Iraq has participated in a war and has civilian or veteran obligations',
        'War ended; recorded emergency mobilization':'Iraq is at peace after wartime mobilization',
        'Khuzestan is eligible for Iraqi core integration':'Khuzestan is owned and controlled by Iraq, remains a non-core, has infrastructure at least 3, compliance at least 60 and resistance below 15; Iraq has held it continuously for 730 days and is at peace with Iran',
        'Mustafa, Idris or Masoud actually leads the eligible KDP lineage':'The Kurdistan Democratic Party governs under Mustafa, Idris or Masoud Barzani',
    }
    return replacements.get(text,text)


def available_ui(n: dict, raw_gate: str, requirement_codes: dict | None=None, hide_prerequisites=False) -> str:
    """Return the same raw eligibility with decomposed, readable native UI.

    Pass the compiler's merged condition-code mapping as requirement_codes to
    label complete contracts. Unmatched conditions remain present and receive
    native formatting rather than being silently omitted.
    """
    rows=parse(raw_gate)
    requirement_codes=requirement_codes or {}
    # Wrap complete top-level AND sequences in a truthful contract label, using
    # exact parsed matching. No boolean group is flattened or reinterpreted.
    for index,meaning in enumerate(n.get('requires',[])):
        if meaning not in requirement_codes:continue
        required=parse(requirement_codes[meaning])
        if not required:continue
        for offset in range(len(rows)-len(required)+1):
            if rows[offset:offset+len(required)]==required:
                label=n['id']+f'_presentation_requirement_{index}'
                rows[offset:offset+len(required)]=[_tooltip(label,_human_requirement(meaning),required)]
                break
    result=emit([_semantic(row) for row in rows])+'\n'
    # The graph already displays these edges. Keep delivery checks in place,
    # and retain their explanations in the pending-project decisions.
    if hide_prerequisites:result=hide_redundant_prerequisites(result,n['prerequisites'])
    return result


def build_loc() -> dict[str,str]:
    """Return English localisation for the root compiler's BOM writer."""
    return dict(LOCALIZATION)
