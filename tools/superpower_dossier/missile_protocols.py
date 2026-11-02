# IMPERIA COLD WAR — Verified MD missile reductions, consensual reserve ceilings and custom papers
"""Preserve old plan indices and never turn an old production clause into a new asset obligation."""
from treaties import TREATIES,EQUIPMENT,LEGACY_EQUIPMENT,ICBM,MRBM,CRUISE,defaults
import re

NUCLEAR_BALLISTIC=tuple(f'nuclear_ballistic_missile_equipment_{i}' for i in range(1,6))
BALLISTIC=tuple(f'ballistic_missile_equipment_{i}' for i in range(1,7))+NUCLEAR_BALLISTIC
ALL_CRUISE=tuple(f'guided_missile_equipment_{i}' for i in range(1,7))
INF=tuple(f'ballistic_missile_equipment_{i}' for i in range(1,4))+NUCLEAR_BALLISTIC[:2]+ALL_CRUISE
GROUPS={1:ICBM,2:BALLISTIC,3:ALL_CRUISE,4:EQUIPMENT,5:ICBM+NUCLEAR_BALLISTIC,6:INF}
LEGACY_GROUPS={1:ICBM,2:MRBM,3:CRUISE,4:LEGACY_EQUIPMENT}


def selected(equipment,scope,version):
    branches=[]
    for v,groups in ((0,LEGACY_GROUPS),(1,GROUPS)):
        choices=' '.join(f'check_variable = {{ {scope} = {g} }}' for g,models in groups.items() if equipment in models)
        if choices:branches.append(f'AND = {{ check_variable = {{ {version} = {v} }} OR = {{ {choices} }} }}')
    return 'OR = { '+' '.join(branches)+' }'


def cap_preview(prefix,n,mode):
    """Only temporary arithmetic, called inside a native non-executing tooltip."""
    rows=[f'if = {{ limit = {{ check_variable = {{ {prefix}reserve_limit = 1 }} }}']
    if mode=='standing':
        rows.append(f'if = {{ limit = {{ has_country_flag = icwt_member_{n} }} set_temp_variable = {{ icwt_preview_cap = icwt_cap_{n} }} }} else = {{')
    elif mode=='pending':
        rows.append(f'if = {{ limit = {{ check_variable = {{ icwt_plan_revision_{n} = global.icwt_p_revision }} }} set_temp_variable = {{ icwt_preview_cap = icwt_limit_plan_{n} }} }} else = {{')
    rows += ['set_temp_variable = { icwt_preview_cap = 0 }',f'set_temp_variable = {{ icwt_preview_fraction = {prefix}reduction }} divide_temp_variable = {{ icwt_preview_fraction = 100 }}']
    for e in EQUIPMENT:
        rows.append('if = { limit = { '+selected(e,prefix+'scope',prefix+'missile_version')+' } '+f'set_temp_variable = {{ icwt_preview_part = num_equipment@{e} }} set_temp_variable = {{ icwt_preview_retire = icwt_preview_part }} multiply_temp_variable = {{ icwt_preview_retire = icwt_preview_fraction }} round_temp_variable = icwt_preview_retire add_to_temp_variable = {{ icwt_preview_cap = icwt_preview_part }} subtract_from_temp_variable = {{ icwt_preview_cap = icwt_preview_retire }} }}')
    if mode in ('standing','pending'):rows.append('}')
    rows.append('add_to_variable = { icwt_preview_cap_display = icwt_preview_cap tooltip = icwt_reserve_cap_tt }\n}')
    return '\n'.join(rows)


def extend(ef,tr,events,loc,mark,root):
    def get(rows,name):return next(x for x in rows if x.startswith(name+' = {')).split('\n',1)[1].rsplit('\n}',1)[0]
    def put(rows,name,body):
        assert body.count('{')==body.count('}'),name
        rows[:]=[x for x in rows if not x.startswith(name+' = {')]
        rows.append(name+' = {\n'+body+'\n}')
    def effect(name,body):put(ef,name,body)
    def trigger(name,body):put(tr,name,body)
    loc('icwt_reserve_cap_tt','Missile reserve ceiling: $RIGHT|0$ missiles')
    loc('icwt_create','Historical proposal');loc('icwt_suggest','Suggested proposal')
    loc('icwt_create_custom','Create own agreement');loc('icwt_custom','Custom agreement')
    loc('icwt_pending_short','Pending paper');loc('icwt_regional','Other')
    loc('icwt_spirit_12','Bilateral Agreement')
    loc('icwt_cap_observed','Reserve ceiling observed')
    loc('icwt_cap_broken','Reserve ceiling exceeded')
    loc('icwt_cap_status_good','(our ceiling observed)');loc('icwt_cap_status_bad','(our ceiling exceeded)')
    # New papers have real MD missile terms. Old production clauses remain inert.
    trigger('icwt_md_edit_valid','''OR = {
 AND = { check_variable = { icwt_edit_missile_version = 1 } check_variable = { icwt_edit_restraint = 0 } }
 AND = { check_variable = { icwt_edit_missile_version = 0 } check_variable = { icwt_edit_restraint = 0 } check_variable = { icwt_edit_reserve_limit = 0 } }
}
OR = { check_variable = { icwt_edit_reserve_limit = 0 } check_variable = { icwt_edit_scope > 0 } }''')
    trigger('icwt_edit_valid',get(tr,'icwt_edit_valid')+'\nicwt_md_edit_valid = yes')
    effect('icwt_open_custom','icwt_edit_12 = yes icwt_display = yes')
    trigger('icwt_supported_paper','OR = { NOT = { icwt_pending = yes } check_variable = { global.icwt_p_addendum = 1 } check_variable = { global.icwt_p_restraint = 0 } }')
    opening='set_temp_variable = { icwt_opening_scope = 1 } set_temp_variable = { icwt_opening_missile_version = 1 } set_temp_variable = { icwt_opening_reduction = 0 } set_temp_variable = { icwt_opening_reserve_limit = 1 }\n'+cap_preview('icwt_opening_',1,'draft')
    effect('icwt_preview_opening_limit_1',opening)
    inspections=[];decisions=[]
    years={}
    for name in ('MD_nuclear_missiles.txt','MD_ballistic_missiles.txt','MD_guided_missiles.txt'):
        source=(root/'common/units/equipment'/name).read_text(encoding='utf-8')
        years.update({m[1]:int(m[2]) for m in re.finditer(r'^\s*(\w+_equipment_\d+)\s*=\s*\{\s*year\s*=\s*(\d+)',source,re.M)})
    assert set(EQUIPMENT)<=years.keys(),'Every dismantling priority needs its actual loaded model year'
    dismantling_order=sorted(EQUIPMENT,key=lambda e:(years[e],EQUIPMENT.index(e)))
    for n in range(1,len(TREATIES)+1):
        plan=[f'set_variable = {{ icwt_limit_plan_{n} = 0 }} set_variable = {{ icwt_plan_retire_total_{n} = 0 }}',
              f'set_variable = {{ icwt_plan_scope_{n} = icwt_calc_scope }} set_variable = {{ icwt_plan_version_{n} = icwt_calc_missile_version }} set_variable = {{ icwt_plan_limit_{n} = icwt_calc_reserve_limit }}',
              f'if = {{ limit = {{ check_variable = {{ global.icwt_pending = {n} }} }} set_variable = {{ icwt_plan_revision_{n} = global.icwt_p_revision }} }} else = {{ set_variable = {{ icwt_plan_revision_{n} = global.icwt_{n}_revision }} }}']
        for i,e in enumerate(EQUIPMENT):
            plan.append(f'set_variable = {{ icwt_plan_{n}_{i} = 0 }}\nif = {{ limit = {{ '+selected(e,'icwt_calc_scope','icwt_calc_missile_version')+' } '+f'set_variable = {{ icwt_plan_{n}_{i} = num_equipment@{e} }} multiply_variable = {{ icwt_plan_{n}_{i} = icwt_calc_fraction }} round_variable = icwt_plan_{n}_{i} add_to_variable = {{ icwt_limit_plan_{n} = num_equipment@{e} }} subtract_from_variable = {{ icwt_limit_plan_{n} = icwt_plan_{n}_{i} }} add_to_variable = {{ icwt_plan_retire_total_{n} = icwt_plan_{n}_{i} }} }}')
        effect(f'icwt_plan_{n}','\n'.join(plan)+f'\nicwt_inspect_plan_{n} = yes')
        effect(f'icwt_plan_context_{n}',f'''if = {{ limit = {{ check_variable = {{ global.icwt_pending = {n} }} }}
set_variable = {{ icwt_calc_missile_version = global.icwt_p_missile_version }} set_variable = {{ icwt_calc_reserve_limit = global.icwt_p_reserve_limit }}
}} else = {{ set_variable = {{ icwt_calc_missile_version = global.icwt_{n}_missile_version }} set_variable = {{ icwt_calc_reserve_limit = global.icwt_{n}_reserve_limit }} }}''')
        for action in ('send','review'):
            body=get(ef,f'icwt_{action}_{n}')
            body=body.replace(f'icwt_plan_{n} = yes',f'icwt_plan_context_{n} = yes icwt_plan_{n} = yes')
            effect(f'icwt_{action}_{n}',body)
        # Preflight totals are calculated from current stock, never GUI state.
        inspect=[f'set_variable = {{ icwt_current_plan_{n} = 0 }}']
        for e in EQUIPMENT:inspect.append('if = { limit = { '+selected(e,f'icwt_plan_scope_{n}',f'icwt_plan_version_{n}')+' } '+f'add_to_variable = {{ icwt_current_plan_{n} = num_equipment@{e} }} }}')
        inspect += [f'subtract_from_variable = {{ icwt_current_plan_{n} = icwt_plan_retire_total_{n} }}',f'set_variable = {{ icwt_cap_plan_ok_{n} = 0 }}',f'if = {{ limit = {{ check_variable = {{ var = icwt_limit_plan_{n} value = icwt_current_plan_{n} compare = greater_than_or_equals }} }} set_variable = {{ icwt_cap_plan_ok_{n} = 1 }} }}']
        effect(f'icwt_inspect_plan_{n}','\n'.join(inspect))
        trigger(f'icwt_assets_{n}',get(tr,f'icwt_assets_{n}')+f'\nOR = {{ NOT = {{ check_variable = {{ icwt_plan_limit_{n} = 1 }} }} check_variable = {{ icwt_cap_plan_ok_{n} = 1 }} }}')
        preflight=f'USA = {{ icwt_inspect_plan_{n} = yes }} SOV = {{ icwt_inspect_plan_{n} = yes }}\n'+get(ef,f'icwt_preflight_{n}')
        preflight+='\nif = { limit = { check_variable = { global.icwt_p_restraint > 0 } } set_variable = { global.icwt_preflight = 0 } }'
        effect(f'icwt_preflight_{n}',preflight)
        join=get(ef,f'icwt_join_{n}').replace(f'set_country_flag = icwt_member_{n}',f'set_variable = {{ icwt_cap_{n} = icwt_limit_plan_{n} }} set_country_flag = icwt_member_{n}',1)
        effect(f'icwt_join_{n}',f'icwt_inspect_plan_{n} = yes\n'+join)
        effect(f'icwt_accept_invite_{n}',f'icwt_inspect_plan_{n} = yes\n'+get(ef,f'icwt_accept_invite_{n}'))
        trigger(f'icwt_reviewed_{n}',get(tr,f'icwt_reviewed_{n}')+'\nicwt_supported_paper = yes')
        tally=[f'set_variable = {{ icwt_reserves_{n} = 0 }}']
        for e in EQUIPMENT:tally.append('if = { limit = { '+selected(e,f'global.icwt_{n}_scope',f'global.icwt_{n}_missile_version')+' } '+f'add_to_variable = {{ icwt_reserves_{n} = num_equipment@{e} }} }}')
        effect(f'icwt_count_reserves_{n}','\n'.join(tally))
        inspect_live=f'''if = {{ limit = {{ has_country_flag = icwt_member_{n} check_variable = {{ global.icwt_{n}_reserve_limit = 1 }} }}
icwt_count_reserves_{n} = yes
if = {{ limit = {{ check_variable = {{ icwt_reserves_{n} > icwt_cap_{n} }} }} set_country_flag = icwt_limit_broken_{n} }} else = {{ clr_country_flag = icwt_limit_broken_{n} }}
}} else = {{ clr_country_flag = icwt_limit_broken_{n} }}'''
        effect(f'icwt_inspect_reserves_{n}',inspect_live)
        trigger(f'icwt_observed_{n}',f'NOT = {{ has_country_flag = icwt_limit_broken_{n} }}')
        inspections.append(f'icwt_inspect_reserves_{n} = yes')
        # New missile commitments are immutable when changing only a programme.
        for pid,slot in ((1,9),(2,8),(3,1),(4,10)):
            if n!=slot:continue
            active=get(tr,f'icwt_programme_{pid}_active')
            if pid==3:
                active=active.replace(f'check_variable = {{ global.icwt_{n}_reserve_limit > 0 }}',f'OR = {{ check_variable = {{ global.icwt_{n}_reserve_limit > 0 }} AND = {{ check_variable = {{ global.icwt_{n}_missile_version = 0 }} check_variable = {{ global.icwt_{n}_restraint > 0 }} }} }}')
            trigger(f'icwt_programme_{pid}_active',active+f'\nUSA = {{ icwt_observed_{n} = yes }} SOV = {{ icwt_observed_{n} = yes }}')
        effect(f'icwt_preview_limit_pending_{n}',cap_preview('global.icwt_p_',n,'pending'))
        effect(f'icwt_preview_limit_standing_{n}',cap_preview(f'global.icwt_{n}_',n,'standing'))
        effect(f'icwt_preview_limit_draft_{n}',cap_preview('ROOT.icwt_edit_',n,'draft'))
        restore=[f'icwt_count_reserves_{n} = yes',f'set_temp_variable = {{ icwt_excess = icwt_reserves_{n} }} subtract_from_temp_variable = {{ icwt_excess = icwt_cap_{n} }} clamp_temp_variable = {{ var = icwt_excess min = 0 }}']
        for e in dismantling_order:
            restore.append('if = { limit = { '+selected(e,f'global.icwt_{n}_scope',f'global.icwt_{n}_missile_version')+' check_variable = { icwt_excess > 0 } } '+f'set_temp_variable = {{ icwt_remove = num_equipment@{e} }} if = {{ limit = {{ check_variable = {{ icwt_remove > icwt_excess }} }} set_temp_variable = {{ icwt_remove = icwt_excess }} }} subtract_from_temp_variable = {{ icwt_excess = icwt_remove }} multiply_temp_variable = {{ icwt_remove = -1 }} add_equipment_to_stockpile = {{ type = {e} amount = icwt_remove }} }}')
        # Preview uses temporary tally rather than writing the standing inspection cache.
        preview_restore='\n'.join(restore).replace(f'icwt_count_reserves_{n} = yes', '\n'.join(tally).replace('set_variable','set_temp_variable').replace('add_to_variable','add_to_temp_variable'))
        effect(f'icwt_restore_preview_{n}','effect_tooltip = {\n'+preview_restore+'\n}')
        effect(f'icwt_restore_{n}',f'if = {{ limit = {{ has_country_flag = icwt_member_{n} check_variable = {{ global.icwt_{n}_reserve_limit = 1 }} }}\n'+'\n'.join(restore)+'\nicwt_refresh = yes\n}')
        did=f'icwt_restore_decision_{n}'
        loc(did,'Restore the missile ceiling: '+TREATIES[n-1][1]);loc(did+'_desc','Dismantle only the excess covered reserve missiles, beginning with the older listed models. The agreement and its remaining term continue. Treaty benefits resume when the covered reserves comply with the signed ceiling.')
        decisions.append(f'{did} = {{ icon = icsd_file visible = {{ has_country_flag = icwt_member_{n} check_variable = {{ global.icwt_{n}_reserve_limit = 1 }} has_country_flag = icwt_limit_broken_{n} }} available = {{ has_country_flag = icwt_member_{n} }} cost = 0 complete_effect = {{ icwt_restore_preview_{n} = yes hidden_effect = {{ icwt_restore_{n} = yes }} }} ai_will_do = {{ factor = 0 }} }}')
    effect('icwt_refresh_compliance','for_each_scope_loop = { array = global.icwt_roster if = { limit = { exists = yes }\n'+'\n'.join(inspections)+'\n} }')
    # Bomb production modifiers are obsolete in this MD missile system.
    country=get(ef,'icwt_refresh_country');start=country.index('\n',country.index('add_ideas = icwt_restraint_50'))+1
    effect('icwt_refresh_country','remove_ideas = icwt_restraint_10 remove_ideas = icwt_restraint_25 remove_ideas = icwt_restraint_50\n'+country[start:])
    pair=get(ef,'icwt_pair_recalculate')
    refresh=get(ef,'icwt_refresh')
    for n in range(1,len(TREATIES)+1):
        pair=pair.replace(f'has_country_flag = icwt_member_{n} PREV = {{ has_country_flag = icwt_member_{n} }}',f'has_country_flag = icwt_member_{n} icwt_observed_{n} = yes PREV = {{ has_country_flag = icwt_member_{n} icwt_observed_{n} = yes }}')
        refresh=refresh.replace(f'has_country_flag = icwt_member_{n} NOT = {{ has_war_with = SOV }}',f'has_country_flag = icwt_member_{n} icwt_observed_{n} = yes NOT = {{ has_war_with = SOV }}')
        refresh=refresh.replace(f'SOV = {{ has_country_flag = icwt_member_{n} }}',f'SOV = {{ has_country_flag = icwt_member_{n} icwt_observed_{n} = yes }}')
    effect('icwt_pair_recalculate',pair)
    effect('icwt_refresh','icwt_refresh_compliance = yes\n'+refresh)
    return decisions
