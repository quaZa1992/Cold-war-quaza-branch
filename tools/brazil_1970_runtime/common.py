# IMPERIA COLD WAR — Brazil 1970 native runtime writer utilities.
from pathlib import Path
from decimal import Decimal
import json
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/south_america_event_art'))
from sa_photo_catalogue import picture_for
HERE=Path(__file__).resolve().parent
MARK='# IMPERIA COLD WAR — Brazil 1970 national programmes.\n'
P='COLDWAR_BRA_'
TREE=P+'1970_focus'
def num(v):
    s=format(Decimal(str(v)).quantize(Decimal('.00001')),'f').rstrip('0').rstrip('.')
    return s if s not in ('','-0') else '0'
def share(v):return num(Decimal(str(v))/100)
def block(key,*rows):
    body='\n'.join(x for x in rows if x)
    return key+' = {\n'+'\n'.join('\t'+s for s in body.splitlines())+'\n}'
def neg(s):return block('NOT',s)
def flag(s):return 'has_country_flag = '+P+s
def earned(k):return flag('earned_'+k)
def setflag(k):return 'set_country_flag = '+P+k
def clearflag(k):return 'clr_country_flag = '+P+k
def once(k):return neg(flag(k))
def country(tag,s):return block(tag,s)
def guard(*rows):return block('limit',*rows)
def iff(check,*rows):return block('if',guard(check),*rows)
def native_effects_file(body):return MARK+body.rstrip()+'\n'
def loc_text(values):
    rows=['l_english:',MARK.rstrip()]
    for k,v in sorted(values.items()):
        assert '\u2013' not in v and '\u2014' not in v,(k,v)
        v=v.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n').replace('\\\\n','\\n')
        rows.append(f' {k}:0 "{v}"')
    return '\n'.join(rows)+'\n'
def idea_id(k):return P+'policy_'+k
def idea_def(i,title,effects,group,loc,description=''):
    loc[i]=title;loc[i+'_desc']=description or 'A funded national policy and its institutional commitments.'
    mods=[e['key']+' = '+num(e['value']) for e in effects if e['kind']=='modifier']
    return block(i,'picture = COLDWAR_BRA_group_'+group,'allowed = { always = no }','allowed_civil_war = { always = yes }','removal_cost = -1',block('modifier',*mods) if mods else '')
def construction(e):
    return country(str(e['state']),block('add_building_construction','type = '+e['building'],'level = '+str(e['amount']),'instant_build = '+('yes' if e.get('instant',True) else 'no')))
def building(e):
    return country(str(e['state']),'add_extra_state_shared_building_slots = '+str(e['slots'])+'\n'+block('add_building_construction','type = '+e['building'],'level = '+str(e['amount']),'instant_build = '+('yes' if e.get('instant',True) else 'no')))
def asset_transaction(scoped_assets,success):
    """Grant slots before construction; validate native post-grant capacity before any fee.

    Native effects execute in one transaction. Failed capacity preflight rolls
    back only the newly added slots and never charges, earns or constructs.
    """
    if not scoped_assets:return '\n'.join(success)
    grants=[];rollback=[];ready=[]
    for tag,e in scoped_assets:
        grants.append(country(tag,country(str(e['state']),'add_extra_state_shared_building_slots = '+str(e['slots']))))
        rollback.append(country(tag,country(str(e['state']),'add_extra_state_shared_building_slots = -'+str(e['slots']))))
        if e['building'] in SHARED:
            ready.append(country(tag,country(str(e['state']),block('free_building_slots','building = '+e['building'],'size > '+str(e['amount']-1),'include_locked = no'))))
    if not ready:return '\n'.join(grants+success)
    return '\n'.join(grants+[iff('\n'.join(ready),*success),block('else',*rollback)])
CAPS={'industrial_complex':50,'arms_factory':35,'offices':50,'dockyard':20,'infrastructure':6,'agriculture_district':10,'renewable_energy_infra':20,'synthetic_refinery':2,'nuclear_reactor':20,'fuel_silo':5,'air_base':10}
SHARED={'industrial_complex','arms_factory','offices','dockyard','agriculture_district','synthetic_refinery'}
def asset_checks(e):
    sid=e['state'];kind=e['building'];amount=e['amount']
    cap=CAPS[kind]
    return '\n'.join([f'owns_state = {sid}',f'controls_state = {sid}',f'has_full_control_of_state = {sid}',country(str(sid),f'check_variable = {{ var = building_level@{kind} value = {cap-amount} compare = less_than_or_equals }}')])
def node_conditions(n):
    rows=[]
    for c in n.get('conditions',[]):
        if c.endswith('_are_in_power = yes') or c.startswith('Governing party identity:'):continue
        if c=='has_tech = reactor1':rows.append(c)
        elif c=='Angola is independent and recognised':rows.append('AGL = { is_subject = no }')
        elif c=='Active Brazil-Paraguay Itaipu agreement':rows.append('has_idea = '+P+'itaipu_BRA')
        elif c.startswith('Active ') and c.endswith(' agreement'):
            if 'Argentine Nuclear' in c:rows.append('has_idea = '+P+'arg_nuclear_BRA')
            else:raise ValueError(c)
        else:raise ValueError(('Unlowered condition',n['key'],c))
    return rows
def gdp_fee(e):return 'set_temp_variable = { treasury_change = { value = gdp_total multiply = '+share(e['percent'])+' } }\nmodify_treasury_effect = yes'
def native_faction(e):
    target=num(e['value']);name=e['faction']
    rows=['set_temp_variable = { temp_opinion = '+target+' }']
    if e['value']>0:
        auto=block('OR','western_autocrats_are_in_power = yes',*[f'check_variable = {{ ruling_party = {i} }}' for i in (7,13,21,22)])
        rows.append(iff(auto,'divide_temp_variable = { temp_opinion = 2 }'))
    rows.append('change_'+name+'_opinion = yes')
    return iff('has_idea = '+name,*rows)
def finite_effect(e,key,index=0):
    k=e['kind']
    if k=='treasury_gdp':return gdp_fee(e)
    if k=='building':return building(e)
    if k=='research':return block('add_tech_bonus',f'name = {P}{key}_research_{index}',f'bonus = {num(e["bonus"])}',f'uses = {e["uses"]}',f'category = {e["category"]}')
    if k=='experience':return e['service']+'_experience = '+str(e['amount'])
    if k=='faction_opinion':return native_faction(e)
    if k=='remove_spirit':return 'remove_ideas = '+e['spirit']
    if k=='unlock_decision':return 'unlock_decision_tooltip = '+e['id']
    if k=='suspend_agreement':return P+'terminate_'+e['agreement']+' = yes'
    raise ValueError(('Finite lowering',key,e))
def weekly_preview(e,key,loc,source='gdp_total',income=False):
    v=P+'quote_'+key;amount=e['annual_gdp_percent']
    loc[v+'_tt']=('§YAdditional Income§!' if income else '§YAdditional Expenses§!')+' '+('§G+' if income else '§R+')+'$$[?'+v+'_million|2] Million/week§!'
    return '\n'.join(['set_temp_variable = { '+v+' = { value = '+source+' multiply = '+share(amount)+' divide = 52 } }','set_temp_variable = { '+v+'_million = { value = '+v+' multiply = 1000 } }','custom_effect_tooltip = '+v+'_tt'])
def output(path,text):return {path:native_effects_file(text)}
def all_effect_sets(d):
    for n in d['nodes']:
        yield n,n['effects'],'BRA'
        if n.get('offer'):
            for s in ('brazil','recipient'):yield n,n['offer'][s]['effects'],'BRA' if s=='brazil' else n['offer']['partner']
