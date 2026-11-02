# IMPERIA COLD WAR — Palestinian institutional costs of settlement fragmentation.
"""Bounded PAL consequences of active West Bank and Gaza settlement programmes.

Only delivered sites or an actually funded unilateral foothold qualify.
Numerical values are balance proposals, not historical causal estimates.
"""
from policy_common import ident, has

MODS={'stability_factor':-.02,'political_power_factor':-.025,'offices_productivity':-.04,
      'bureaucracy_cost_multiplier_modifier':.04,'social_cost_multiplier_modifier':.03}
NAMES={208:'West Bank',209:'Gaza'}


def modifier_id(state):return ident('palestinian_pressure_'+str(state))


def summary(state,level=1):
    return ('Palestine, if present: "'+NAMES[state]+': Territorial and Settlement Pressures": '
        f'Stability {-2*level:+g}%, Political Power Gain {-2.5*level:+g}%, Office Productivity {-4*level:+g}%, '
        f'Bureaucracy Cost {4*level:+g}%, Social Costs {3*level:+g}%.')


def preview(api,state,level=1,*,maximum=True):
    """Pure display arithmetic, using no fiscal or modifier provider."""
    name=modifier_id(state)
    heading=ident('palestinian_terms_'+str(state)+'_tt')
    api.loc(heading,'Palestine, if it exists')
    count=ident('display_pal_level_'+str(state))
    code=f'custom_effect_tooltip = {heading}\ncustom_effect_tooltip = {{ localization_key = modifies_dynamic_modifier_tt MODIFIER = {name} }}\n'
    code+=f'set_temp_variable = {{ {count} = {level} }}\n'
    if maximum:
        code+=f'if = {{ limit = {{ ISR = {{ has_variable = {ident("pal_level_"+str(state))} check_variable = {{ {ident("pal_level_"+str(state))} > {level} }} }} }} set_temp_variable = {{ {count} = ISR.{ident("pal_level_"+str(state))} }} }}\n'
    for key,value in MODS.items():
        amount=ident('display_pal_'+str(state)+'_'+key)
        code+=f'set_temp_variable = {{ {amount} = {count} }}\nmultiply_temp_variable = {{ {amount} = {value} }}\n'
        code+=f'add_to_variable = {{ ISR70_display_pal_row_{state}_{key} = {amount} tooltip = {key}_tt }}\n'
    return code


def build(api):
    records=[];calculate=[];palestine=[]
    for state,label in NAMES.items():
        slug='west_bank' if state==208 else 'gaza'
        basic=[f'project_designated_sites_{state}_done','project_controlled_'+slug+'_done']
        extensive=[f'project_settlement_package_{state}_done',f'project_entrench_network_{state}_done']
        extensive += [f'project_settlement_extension_{phase}_{state}_done' for phase in (1,2,3)]
        delivered='OR = { '+' '.join(has(key) for key in basic+extensive)+' }'
        larger='OR = { '+' '.join(has(key) for key in extensive)+' }'
        claim=f'{state} = {{ OR = {{ is_owned_by = PAL is_core_of = PAL }} }}'
        funded_presence=[ident('presence_established_'+str(state)),ident('presence_capital_paid_'+str(state))]
        funded='AND = { '+' '.join('has_country_flag = '+key for key in funded_presence)+' }'
        controlled=f'{state} = {{ is_controlled_by = ISR }} OR = {{ {delivered} {funded} }}'
        foreign=ident('presence_active_'+str(state))+' = yes'
        trigger=api.trigger('pal_pressure_active_'+str(state),
            f'country_exists = PAL country_exists = ISR ISR70_is_scenario = yes {claim} OR = {{ AND = {{ {controlled} }} {foreign} }}')
        level=ident('pal_level_'+str(state));saved=ident('pal_level_applied_'+str(state))
        values={key:ident('pal_'+str(state)+'_'+key) for key in MODS}
        mid=api.state_modifier('palestinian_pressure_'+str(state),label+': Territorial and Settlement Pressures',
            'Israeli settlement commitments in '+label+' constrain Palestinian administration, fragment commercial activity and divide the political agenda. A funded settlement ceiling and compensation programme can ease the burden.',
            values,enable=f'tag = PAL country_exists = PAL country_exists = ISR ISR = {{ {trigger} = yes }}')
        calculate.append(f'''set_variable = {{ {level} = 0 }}
if = {{ limit = {{ {trigger} = yes }}
set_variable = {{ {level} = 1 }}
if = {{ limit = {{ {state} = {{ is_controlled_by = ISR }} {larger} }} set_variable = {{ {level} = 2 }} }}
if = {{ limit = {{ {has('target_'+str(state))} {has('fund_settlement_compensation_done')} }} set_variable = {{ {level} = 1 }} }}
}}''')
        updates='\n'.join(f'set_variable = {{ {var} = ISR.{level} }}\nmultiply_variable = {{ {var} = {MODS[key]} }}' for key,var in values.items())
        palestine.append(f'''if = {{ limit = {{ NOT = {{ has_variable = {saved} }} }} set_variable = {{ {saved} = 0 }} }}
if = {{ limit = {{ NOT = {{ check_variable = {{ var = {saved} value = ISR.{level} compare = equals }} }} }}
set_variable = {{ {saved} = ISR.{level} }}
{updates}
if = {{ limit = {{ check_variable = {{ {saved} > 0 }} }} add_dynamic_modifier = {{ modifier = {mid} }} }}
else = {{ remove_dynamic_modifier = {{ modifier = {mid} }} }}
update_money_dirty_variable = yes
}} else_if = {{ limit = {{ check_variable = {{ {saved} > 0 }} NOT = {{ has_dynamic_modifier = {{ modifier = {mid} }} }} }}
add_dynamic_modifier = {{ modifier = {mid} }} update_money_dirty_variable = yes
}} else_if = {{ limit = {{ check_variable = {{ {saved} = 0 }} has_dynamic_modifier = {{ modifier = {mid} }} }}
remove_dynamic_modifier = {{ modifier = {mid} }} update_money_dirty_variable = yes
}}''')
        records.append(dict(state=state,label=label,modifier=mid,active_trigger=trigger,level_variable=level,
            applied_variable=saved,modifier_variables=values,per_level_modifiers=MODS,
            basic_receipts=[ident(k) for k in basic],extensive_receipts=[ident(k) for k in extensive],
            funded_presence_receipts=funded_presence,max_level=2))

    helper=api.effect('reconcile_palestinian_pressure','\n'.join(calculate)+'\nif = { limit = { country_exists = PAL } PAL = {\n'+'\n'.join(palestine)+'\n} }')
    api.tick.append(helper+' = yes')
    api.effects[ident('reconcile_presence')]+='\n'+helper+' = yes'

    # Extend existing project forecasts without changing execution or receipts.
    # The standard daily reconciliation sees the delivered receipt, never a
    # mere focus completion, offer, reserved budget or failed callback.
    for p in api.projects:
        if p['states'] not in ([208],[209]):continue
        state=p['states'][0];key=p['key']
        if key.startswith(('municipal_works','authorize_expansion')):continue
        if not key.startswith(('designated_sites','settlement_services','settlement_ceiling',
            'settlement_package','entrench_network','settlement_extension','controlled_')):continue
        tier=2 if key.startswith(('settlement_package','entrench_network','settlement_extension')) else 1
        extra='effect_tooltip = {\n'+preview(api,state,tier)+'\n}'
        old=p['preview_code'];new=old+'\n'+extra
        p['preview_code']=new
        effect=ident('complete_'+p['unlock'])
        api.effects[effect]=api.effects[effect].replace(old,new)
        did=ident('project_'+key)
        api.decisions=[body.replace(old,new) if body.startswith(did+' = {') else body for body in api.decisions]
        note=summary(state,tier)
        if tier==1:note+=' Extensive settlement network: '+summary(state,2)
        p['effect_summary']+=' '+note;p['delivery_summary']+=' '+note
        api.localisation[did+'_desc']=p['delivery_summary']
    # A financed compensation ceiling also relieves the affected Palestinian
    # institutions. Display the complete resulting programme on every consent
    # and payment surface, independent of current acceptance or funding.
    compensation='effect_tooltip = {\nif = { limit = { ISR = { '+has('target_209')+' } }\n'+preview(api,209,1,maximum=False)+'\n} else = {\n'+preview(api,208,1,maximum=False)+'\n}\n}'
    api.effects[ident('complete_settlement_compensation')]+='\n'+compensation
    for i,event in enumerate(api.events):
        if 'id = ISR70P.403\n' in event:
            api.events[i]=event.replace('name = ISR70P.403.a','name = ISR70P.403.a\n'+compensation,1)
    did=ident('decision_fund_settlement_compensation')
    api.decisions=[body.replace('complete_effect = {','complete_effect = {\n'+compensation,1) if body.startswith(did+' = {') else body for body in api.decisions]
    node=api.nodes['ISR70_settlement_compensation']
    node['policy_summary'].append('Palestine, if present: the selected "West Bank: Territorial and Settlement Pressures" or "Gaza: Territorial and Settlement Pressures" programme retains Stability -2%, Political Power Gain -2.5%, Office Productivity -4%, Bureaucracy Cost +4%, Social Costs +3%.')
    node['description']+=' Funded compensation also eases the pressure on Palestinian administration and commerce.'
    node['note']=node['description']
    api.data['palestinian_pressure']={'project':'IMPERIA COLD WAR','revision':1,'states':records,
        'max_total_level':4,'per_level_modifiers':MODS,'reconcile_effect':helper,
        'activation':'An existing PAL country retains territorial ownership/core and an actual Israeli settlement programme remains active in the West Bank or Gaza.',
        'exclusions':['No penalty from unfunded settlement plans.','No Palestine penalty from Sinai or Golan alone.','No workforce-size changes.'],
        'historical_numbers':False,'source_record':'docs/israel_1970_design/PALESTINIAN_PRESSURE.md'}
