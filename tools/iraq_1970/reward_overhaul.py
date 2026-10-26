# IMPERIA CW — Cold War: iraq 1970 — reward overhaul.
"""Direct national-focus rewards, with a separate v3 old-save entitlement.

Data authoring is split by chapter. This module is pure: generation returns
text and never installs it. Completed v2 work is credited by actual receipts;
old unfunded v2 supplements remain separate and must finish first. A v3 update
charges only a positive increase in the focus's GDP price, once quoted.
"""
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import json

from common import P, block, check, flag, invoice, pay_var, parse, first, values, emit

HERE=Path(__file__).resolve().parent
VERSION=P+'direct_rewards_v3_migrated'
REVISION='direct_rewards_2026_10_19_v3'
BONUS_LOCALISATION={}


def current(n):return n['id']+'_reward_v3_current'
def pending(n):return n['id']+'_reward_v3_pending'
def old_holder(n):return n['id']+'_reward_v3_legacy'
def legacy_source(n):return n['id']+'_reward_v3_credit_source'
def uid(n):return n['id']+'_reward_v3_upgrade'


def building_specs(n):
    combined={}
    for spec in ([n['building']] if n.get('building') else [])+n.get('buildings',[]):
        state,kind,count=spec
        assert int(count)==count and count>0,(n['id'],spec)
        combined[(int(state),kind)]=combined.get((int(state),kind),0)+int(count)
    return [[state,kind,count] for (state,kind),count in combined.items()]


def _payloads(n):
    """Semantic one-time units. Names do not create a second research grant."""
    result=[]
    for state,kind,count in building_specs(n):
        result.append({'kind':'building','state':state,'building_type':kind,'amount':count})
    army=float(n.get('army_xp',0));air=navy=0;literacy=0;raw=[]
    for command in n.get('instant',[])+n.get('audit_new_delivery_only',[]):
        rows=parse(command)
        # Physical rewards must be visible to the all-state capacity guard.
        from common import walk
        assert not any(k=='add_building_construction' for k,o,v in walk(rows)),('Use structured buildings',n['id'])
        for key,op,body in rows:
            if key in ('add_tech_bonus','add_doctrine_cost_reduction'):
                result.append({'kind':'tech' if key=='add_tech_bonus' else 'doctrine',
                    'category':first(body,'category'),'amount':int(first(body,'uses')),
                    'bonus':float(first(body,'bonus') if key=='add_tech_bonus' else first(body,'cost_reduction'))})
            elif key=='army_experience':army+=float(body)
            elif key=='air_experience':air+=float(body)
            elif key=='navy_experience':navy+=float(body)
            elif key=='set_temp_variable' and first(body,'LR_change') is not None:literacy+=float(first(body,'LR_change'))
            elif key=='update_literacy_rate':pass
            else:raw.append((key,op,body))
    for kind,amount in [('army_xp',army),('air_xp',air),('navy_xp',navy),('literacy',literacy)]:
        if amount:result.append({'kind':kind,'amount':amount})
    if raw:result.append({'kind':'instant','amount':1,'raw':emit(raw)})
    return result


def _identity(c):
    return (c['kind'],c.get('state'),c.get('building_type'),c.get('category'),c.get('raw'))


def _old_evidence(old,payload):
    wanted=_identity(payload)
    if old.get('audit_delivery_components') is None:
        return [{'flag':old['id']+'_implemented','amount':c['amount']}
                for c in _payloads(old) if _identity(c)==wanted]
    evidence=[]
    for component in old['audit_delivery_components']:
        fragment={'id':old['id'],'key':old['key'],'building':None,'army_xp':0,'instant':[]}
        kind=component['kind']
        if kind=='building':fragment['building']=component['building']
        elif kind=='army_xp':fragment['army_xp']=component['amount']
        elif kind=='literacy':fragment['instant']=[f'set_temp_variable = {{ LR_change = {component["amount"]:g} }}','update_literacy_rate = yes']
        elif kind=='instant':fragment['instant']=component['instant']
        else:raise ValueError(kind)
        for c in _payloads(fragment):
            if _identity(c)==wanted:evidence.append({'flag':component['receipt'],'amount':c['amount']})
    # v2 added this after its own component delivery, with the successful focus
    # transaction as its receipt (not any later programme reconciliation).
    if payload['kind']=='instant' and old.get('audit_new_delivery_only'):
        fragment={'id':old['id'],'key':old['key'],'building':None,'army_xp':0,'instant':old['audit_new_delivery_only']}
        for c in _payloads(fragment):
            if _identity(c)==wanted:evidence.append({'flag':old['id']+'_implemented','amount':c['amount']})
    return evidence


def apply(data):
    if data.get('reward_overhaul_revision')==REVISION:return data
    by={n['key']:n for n in data['nodes'] if not n.get('audit_retired')}
    overrides={}
    for filename in ('reward_overhaul_economy.json','reward_overhaul_politics.json'):
        additions=json.loads((HERE/filename).read_text(encoding='utf-8-sig'))
        assert not set(additions)&set(overrides),'Overlapping chapter ownership'
        overrides.update(additions)
    # IMPERIA CW — Cold War: move optional menus into reviewed focus outcomes.
    from decision_streamlining import augment_overrides
    augment_overrides(overrides)
    assert set(overrides)<=set(by),'Unknown/retired focus key'
    allowed={'title','modifiers','building','buildings','army_xp','instant','budget_gdp_share','days','description','reference','rationale'}
    for key,patch in overrides.items():
        assert not set(patch)-allowed,(key,set(patch)-allowed)
        n=by[key];old=deepcopy(n)
        n['overhaul_previous_modifiers']=old['modifiers']
        for field,value in patch.items():
            if field not in ('reference','rationale'):n[field]=deepcopy(value)
        if 'instant' in patch:
            # The new full instant payload must explicitly retain any prior
            # timed campaign cost; never silently append an obsolete reward.
            n.pop('audit_new_delivery_only',None)
        if 'days' in patch:n['cost']=n['days']/7
        n['overhaul_reference']=patch.get('reference','')
        n['overhaul_rationale']=patch.get('rationale','')
        n['overhaul_price_increment']=max(0,n['budget_gdp_share']-old['budget_gdp_share'])
        n['overhaul_previous_share']=old['budget_gdp_share']
        components=[];payloads=_payloads(n)
        identities=[_identity(c) for c in payloads]
        assert len(identities)==len(set(identities)),('Duplicate semantic reward; merge uses first',key)
        for index,payload in enumerate(payloads):
            c=deepcopy(payload);c['receipt']=P+'reward_v3_'+key+'_'+str(index)
            c['credit']=c['receipt']+'_credit';c['evidence']=_old_evidence(old,c)
            if c['kind'] in ('tech','doctrine'):
                c['name']=P+'reward_v3_'+key+'_'+str(index)+'_instruction'
                BONUS_LOCALISATION[c['name']]=n['title']+' — '+('Doctrine Instruction' if c['kind']=='doctrine' else 'Technical Instruction')
            components.append(c)
        n['overhaul_components']=components
        n['overhaul_changed']=True
    data['reward_overhaul_revision']=REVISION
    return data


def _raw(c,amount):
    if amount<=0:return ''
    kind=c['kind']
    if kind=='building':return f'{c["state"]} = {{ add_building_construction = {{ type = {c["building_type"]} level = {int(amount)} instant_build = yes }} }}'
    if kind in ('army_xp','air_xp','navy_xp'):return f'{kind.removesuffix("_xp")}_experience = {amount:g}'
    if kind=='literacy':return f'set_temp_variable = {{ LR_change = {amount:g} }}\nupdate_literacy_rate = yes'
    if kind=='instant':return c['raw']
    if kind=='tech':return f'add_tech_bonus = {{ name = {c["name"]} bonus = {c["bonus"]:g} uses = {int(amount)} category = {c["category"]} }}'
    if kind=='doctrine':return f'add_doctrine_cost_reduction = {{ name = {c["name"]} cost_reduction = {c["bonus"]:g} uses = {int(amount)} category = {c["category"]} }}'
    raise ValueError(kind)


def credit_refresh(n):
    body=''
    for c in n['overhaul_components']:
        body+=f'set_variable = {{ {c["credit"]} = 0 }}\n'
        for evidence in c['evidence']:
            body+=block('if',block('limit',flag(legacy_source(n))+'\n'+flag(evidence['flag']))+
                f'add_to_variable = {{ {c["credit"]} = {evidence["amount"]:g} }}')
        body+=f'clamp_variable = {{ var = {c["credit"]} min = 0 max = {c["amount"]:g} }}\n'
        body+=block('if',block('limit',check(c['credit'],c['amount']))+'set_country_flag = '+c['receipt'])
    return body


def missing(n):
    return block('OR','\n'.join('NOT = { '+flag(c['receipt'])+' }' for c in n['overhaul_components'])) if n['overhaul_components'] else 'always = no'


def delivery(n,preview=False,defer_streamlined=False):
    if not n.get('overhaul_changed'):raise ValueError(n['id'])
    body=''
    for c in n['overhaul_components']:
        # IMPERIA CW — Cold War: the new Basrah office is paid by the separate
        # streamlining appropriation, never by the older v2 -> v3 supplement.
        if defer_streamlined and n['key']=='foreign_kuwait' and c['kind']=='building':continue
        if preview:body+=_raw(c,c['amount'])+'\n';continue
        amounts=[e['amount'] for e in c['evidence']]
        credits=sorted({min(c['amount'],sum(xs)) for size in range(len(amounts)+1) for xs in combinations(amounts,size)}|{c['amount']},reverse=True)
        choices=''
        for index,credit in enumerate(credits):
            choices+=block('if' if index==0 else 'else_if',block('limit',check(c['credit'],credit))+_raw(c,c['amount']-credit))
        body+=block('if',block('limit','NOT = { '+flag(c['receipt'])+' }')+choices+'set_country_flag = '+c['receipt'])
    if not preview:body+='set_country_flag = '+current(n)+'\nclr_country_flag = '+pending(n)
    return body


def generate(data,eligible,capacity):
    effects='';queue='';loc={};changed=[n for n in data['nodes'] if n.get('overhaul_changed')]
    migration=''
    for n in changed:
        fid=n['id'];oldshare=n['overhaul_previous_share'];newshare=n['budget_gdp_share']
        row=block('if',block('limit',flag(fid+'_implemented'))+'set_country_flag = '+old_holder(n))
        sources=sorted({e['flag'] for c in n['overhaul_components'] for e in c['evidence']})
        if sources:
            # An old funded programme can still have unfinished v2 work. Pin
            # its eligibility now so those later receipts receive v3 credit.
            row+=block('if',block('limit',block('OR',flag(old_holder(n))+'\n'+'\n'.join(flag(s) for s in sources)))+'set_country_flag = '+legacy_source(n))
        row+=credit_refresh(n)
        # An unimplemented ordinary project retains the GDP basis of its old
        # positive quote. No Treasury change occurs during save recovery.
        if oldshare and oldshare!=newshare:
            row+=block('if',block('limit','NOT = { '+flag(fid+'_implemented')+' }\n'+flag(fid+'_quoted')+'\n'+check(fid+'_invoice',0,'greater_than'))+
                f'divide_variable = {{ {fid}_invoice = {oldshare:g} }}\nmultiply_variable = {{ {fid}_invoice = {newshare:g} }}')
        outstanding=block('OR',missing(n)+'\n'+('always = yes' if n['overhaul_price_increment'] else 'always = no'))
        row+=block('if',block('limit',flag(old_holder(n)))+
            block('if',block('limit',outstanding)+'set_country_flag = '+pending(n))+
            block('else','set_country_flag = '+current(n)))
        migration+=row
    effects+=block(P+'migrate_direct_rewards_v3',block('if',block('limit','COLDWAR_IRQ_campaign_active = yes\nNOT = { '+flag(VERSION)+' }')+migration+'set_country_flag = '+VERSION))
    tick=''
    for n in changed:
        name=uid(n);share=n['overhaul_price_increment']
        basis=n['id']+'_audit_pending_quote_gdp'
        quote=invoice(name,share) if share else f'set_variable = {{ {name}_invoice = 0 }}\nset_country_flag = {name}_quoted'
        # Once v2 has a recovered historic commitment, use that same basis for
        # the additional v3 scope rather than pricing the expansion at live GDP.
        if share:
            replacement=f'set_variable = {{ {name}_invoice = gdp_total }}'
            quote=quote.replace(replacement,replacement+'\n'+block('if',block('limit',check(basis,0,'greater_than'))+f'set_variable = {{ {name}_invoice = {basis} }}'))
        ready='COLDWAR_IRQ_campaign_active = yes\n'+flag(pending(n))+'\nNOT = { '+flag(n['id']+'_audit_upgrade_pending')+' }'
        gate=ready+'\n'+eligible(n)+'\n'+capacity(n)+'\n'+flag(name+'_quoted')+'\ncheck_variable = { gdp_total > 0 }\nNOT = { has_country_flag = MD_skip_treasury_cost }\n'+check('treasury',name+'_invoice')
        refresh=P+'refresh_reward_v3_'+n['key']
        adopted=''
        if not share:
            adopted=block('if',block('limit','NOT = { '+missing(n)+' }')+'set_country_flag = '+current(n)+'\nclr_country_flag = '+pending(n))
        effects+=block(refresh,block('if',block('limit',ready)+credit_refresh(n)+adopted+quote))
        helper=P+'upgrade_reward_v3_'+n['key']
        actual=pay_var(name+'_invoice')+'\n'+delivery(n,defer_streamlined=True)+'\nCOLDWAR_IRQ_reconcile_situations = yes\nCOLDWAR_IRQ_reconcile_programmes = yes'
        effects+=block(helper,refresh+' = yes\n'+block('if',block('limit',gate)+actual))
        decision=name+'_delivery'
        # Native conditional receipts preview only the outstanding supplement.
        # The main focus still shows its complete prospective reward package.
        preview=block('effect_tooltip',pay_var(name+'_invoice')+'\n'+delivery(n,defer_streamlined=True))
        queue+=block(decision,'icon = generic_construction\ncost = 0\nfire_only_once = no\n'+
            block('visible','COLDWAR_IRQ_campaign_active = yes\n'+flag(pending(n)))+
            block('available',gate)+block('complete_effect',preview+block('hidden_effect',helper+' = yes')))
        loc[decision]='Complete '+n['title']
        loc[decision+'_desc']='Complete the expanded programme. Existing deliveries are credited. Additional cost: $[?'+name+'_invoice|2] billion.'
        tick+=block('if',block('limit',flag(pending(n)))+refresh+' = yes')
    effects+=block(P+'refresh_direct_reward_quotes_v3',block('if',block('limit','COLDWAR_IRQ_campaign_active = yes')+tick))
    return effects,queue,loc
