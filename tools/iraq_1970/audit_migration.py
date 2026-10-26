# IMPERIA CW — Cold War: iraq 1970 — audit migration.
"""Once-only delivery credits and explicit, funded old-save upgrade projects.

Never infers delivery from a focus badge. The old successful transaction flag
is authoritative. New physical rewards are charged only for the unfinanced
share; previously delivered assets/XP/literacy cannot be collected twice.
"""
from itertools import combinations
from common import P,block,flag,check,group_gate,invoice,pay_var,locline

VERSION=P+'audit_2026_10_19_migrated'
QUOTE_VERSION=P+'audit_pending_quote_basis_repaired_v2'

def quote_basis_variable(n):return n['id']+'_audit_pending_quote_gdp'

def _pending_quote_repair(n,retired):
    """Preserve unpaid merged commitments, including already-v1 saves.

    A retired child's positive quoted invoice/original share is its historical
    GDP, not a payment credit. Multiple surviving commitments use the lowest
    implied GDP deterministically; actual paid invoices are deducted later.
    Retired pending flags were cleared by v1, so they are not reliable evidence.
    Completed component receipts remain authoritative and are never refunded.
    """
    sources=sorted((c for c in n.get('audit_legacy_cost_credits',[])
                    if c['source'] in retired and c['original_share']>0),
                   key=lambda c:c['source'])
    if not sources:return ''
    fid=n['id'];uid=fid+'_audit_upgrade';basis=quote_basis_variable(n)
    candidate=basis+'_candidate'
    body=f'set_variable = {{ {basis} = 0 }}\n'
    for source in sources:
        valid=flag(source['quoted_flag'])+'\nNOT = { '+flag(source['implemented_flag'])+' }\n'+check(source['invoice_variable'],0,'greater_than')
        lower=block('OR',check(basis,0,'less_than_or_equals')+'\n'+check(candidate,basis,'less_than'))
        body+=block('if',block('limit',valid)+
                    f'set_variable = {{ {candidate} = {source["invoice_variable"]} }}\ndivide_variable = {{ {candidate} = {source["original_share"]:g} }}\n'+
                    block('if',block('limit',lower)+f'set_variable = {{ {basis} = {candidate} }}'))
    missing=block('OR','\n'.join('NOT = { '+flag(c['receipt'])+' }' for c in n['audit_delivery_components']))
    upgrade=block('if',block('limit',flag(fid+'_implemented')+'\n'+flag(fid+'_audit_upgrade_pending')+'\n'+missing)+
                  'clr_country_flag = '+uid+'_quoted\n'+P+'quote_upgrade_'+n['key']+' = yes')
    normal=block('if',block('limit','NOT = { '+flag(fid+'_implemented')+' }\n'+flag(fid+'_pending'))+
                 f'set_variable = {{ {fid}_invoice = {basis} }}\nmultiply_variable = {{ {fid}_invoice = {n["budget_gdp_share"]:g} }}\nset_country_flag = {fid}_quoted')
    return body+block('if',block('limit',check(basis,0,'greater_than'))+upgrade+normal)

def credit_variable(component):return component['receipt']+'_credit'

def _possible_credits(component):
    amounts=list(component.get('legacy_amounts',{}).values())
    return sorted({sum(xs) for size in range(len(amounts)+1) for xs in combinations(amounts,size)},reverse=True)

def _raw(component,credit=0):
    kind=component['kind']
    if kind=='instant':return '\n'.join(component['instant']) if credit<1 else ''
    if kind=='building':
        state,building,count=component['building'];remaining=max(0,count-int(credit))
        return f'{state} = {{ add_building_construction = {{ type = {building} level = {remaining} instant_build = yes }} }}' if remaining else ''
    value=max(0,component['amount']-credit)
    if not value:return ''
    if kind=='army_xp':return f'army_experience = {value:g}'
    if kind=='literacy':return f'set_temp_variable = {{ LR_change = {value:g} }}\nupdate_literacy_rate = yes'
    raise ValueError('Unsupported one-time delivery component '+kind)

def component_reward(component):
    choices=''
    for index,credit in enumerate(_possible_credits(component)):
        choices+=block('if' if index==0 else 'else_if',block('limit',check(credit_variable(component),credit))+_raw(component,credit))
    return block('if',block('limit','NOT = { '+flag(component['receipt'])+' }')+choices+'set_country_flag = '+component['receipt'])

def delivery(n):
    if 'audit_delivery_components' in n:
        return '\n'.join(component_reward(c) for c in n['audit_delivery_components'])
    raw=[]
    if n['building']:
        state,kind,count=n['building'];raw.append(f'{state} = {{ add_building_construction = {{ type = {kind} level = {count} instant_build = yes }} }}')
    raw+=n.get('instant',[])
    if n['army_xp']:raw.append('army_experience = '+str(n['army_xp']))
    return '\n'.join(raw)

def legacy_aliases(data,fid):
    return '\n'.join('set_country_flag = '+old+'_implemented' for old,target in data['retired_focuses'].items() if target==fid and old not in {P+'industry_survey',P+'defence_accounts',P+'society_literacy_accounts',P+'industry_delivery_review',P+'society_service_compact',P+'iran_gulf_credit',P+'iran_supplier_access'})

def generate(data,eligible,capacity):
    effects='';decs='';loc={};retired=data['retired_focuses']
    old=data['audit_retired_rewards'];nodes={n['id']:n for n in data['nodes']}
    recovery=[]
    for n in data['nodes']:
        if n.get('audit_retired'):continue
        recovery.append(block('if',block('limit',flag(n['id']+'_implemented'))+'\n'.join('set_country_flag = '+d['id']+'_unlocked' for d in n['decisions'])))
        previous=n.get('audit_previous_reward',{})
        old_share=previous.get('budget_gdp_share',0)
        if old_share and old_share!=n['budget_gdp_share']:
            fid=n['id']
            recovery.append(block('if',block('limit','NOT = { '+flag(fid+'_implemented')+' }\n'+flag(fid+'_quoted')+'\n'+check(fid+'_invoice',0,'greater_than'))+
              f'divide_variable = {{ {fid}_invoice = {old_share:g} }}\nmultiply_variable = {{ {fid}_invoice = {n["budget_gdp_share"]:g} }}'))
        components=n.get('audit_delivery_components',[])
        for component in components:
            var=credit_variable(component)
            recovery.append(f'set_variable = {{ {var} = 0 }}')
            for source,amount in component.get('legacy_amounts',{}).items():
                recovery.append(block('if',block('limit',flag(source+'_implemented'))+f'add_to_variable = {{ {var} = {amount:g} }}'))
            maximum=component['building'][2] if component['kind']=='building' else (1 if component['kind']=='instant' else component['amount'])
            recovery.append(block('if',block('limit',check(var,maximum))+'set_country_flag = '+component['receipt']))
        if components:
            missing=block('OR','\n'.join('NOT = { '+flag(c['receipt'])+' }' for c in components))
            recovery.append(block('if',block('limit',flag(n['id']+'_implemented')+'\n'+missing)+'set_country_flag = '+n['id']+'_audit_upgrade_pending'))
    # Only compatibility metadata is retired. Earned historical assets remain.
    for fid,target in retired.items():
        recovery.append('clr_country_flag = '+fid+'_pending')
        if fid in old:
            for d in old[fid]['legacy_decisions']:
                recovery.append(block('if',block('limit',flag(fid+'_implemented'))+'set_country_flag = '+d['id']+'_unlocked'))
    recovery.append('set_country_flag = '+VERSION)
    initial_migration=block('if',block('limit','COLDWAR_IRQ_campaign_active = yes\nNOT = { '+flag(VERSION)+' }')+'\n'.join(recovery))
    # Separate receipt: v1 may already have cleared a child's pending flag and
    # frozen an incorrect current-GDP replacement. Only outstanding work is
    # repriced; no treasury, delivered component or earned programme is replayed.
    repair='\n'.join(_pending_quote_repair(n,retired) for n in data['nodes']
                     if not n.get('audit_retired') and n.get('audit_delivery_components'))
    repair+='\nset_country_flag = '+QUOTE_VERSION
    effects+=block(P+'migrate_audit_revision',initial_migration+block('if',block('limit','COLDWAR_IRQ_campaign_active = yes\nNOT = { '+flag(QUOTE_VERSION)+' }')+repair))

    for n in data['nodes']:
        if n.get('audit_retired') or not n.get('audit_delivery_components'):continue
        fid=n['id'];uid=fid+'_audit_upgrade';quoted=uid+'_quoted'
        historical=block('if',block('limit',check(quote_basis_variable(n),0,'greater_than'))+f'set_variable = {{ {uid}_invoice = {quote_basis_variable(n)} }}')
        quote=block('if',block('limit','NOT = { '+flag(quoted)+' }\ncheck_variable = { gdp_total > 0 }')+f'set_variable = {{ {uid}_invoice = gdp_total }}\n'+historical+f'multiply_variable = {{ {uid}_invoice = {n["budget_gdp_share"]:g} }}\n'+
          '\n'.join(block('if',block('limit',flag(c['implemented_flag'])+'\n'+check(c['invoice_variable'],0,'greater_than'))+f'subtract_from_variable = {{ {uid}_invoice = {c["invoice_variable"]} }}') for c in n.get('audit_legacy_cost_credits',[]))+
          f'clamp_variable = {{ var = {uid}_invoice min = 0 }}\nset_country_flag = {quoted}')
        # Pure balance additions to an already funded programme are free.
        # A moved factory that is already delivered is never financed again
        # just because GDP grew before the new research bonus was introduced.
        physical=next((c for c in n['audit_delivery_components'] if c['kind']=='building'),None)
        previous=n.get('audit_previous_reward',{})
        if physical:
            zero=block('if',block('limit',flag(physical['receipt']))+f'set_variable = {{ {uid}_invoice = 0 }}')
        elif n['budget_gdp_share']<=previous.get('budget_gdp_share',0):
            zero=f'set_variable = {{ {uid}_invoice = 0 }}'
        else:zero=''
        if zero:
            # Insert before the quote's success marker so repeated refreshes
            # keep the very first correct supplementary bill.
            quote=quote.replace('set_country_flag = '+quoted,zero+'set_country_flag = '+quoted)
        conditions=eligible(n)+'\n'+capacity(n)+'\n'+flag(fid+'_audit_upgrade_pending')+'\n'+flag(quoted)+'\ncheck_variable = { gdp_total > 0 }\nNOT = { has_country_flag = MD_skip_treasury_cost }\n'+check('treasury',uid+'_invoice')
        payload=pay_var(uid+'_invoice')+'\n'+delivery(n)+'\n'+legacy_aliases(data,fid)+'\nclr_country_flag = '+fid+'_audit_upgrade_pending\nCOLDWAR_IRQ_reconcile_situations = yes\nCOLDWAR_IRQ_reconcile_programmes = yes'
        effects+=block(P+'upgrade_'+n['key'],quote+block('if',block('limit',conditions)+payload))
        # Inspection freezes the supplementary quote without spending it.
        effects+=block(P+'quote_upgrade_'+n['key'],quote)
        decision=uid+'_delivery'
        preview=block('effect_tooltip',pay_var(uid+'_invoice')+'\n'+delivery(n))
        decs+=block(decision,'icon = generic_construction\ncost = 0\nfire_only_once = no\n'+block('visible','COLDWAR_IRQ_campaign_active = yes\n'+flag(fid+'_audit_upgrade_pending'))+
          block('available',conditions)+'\n'+block('complete_effect',preview+'\n'+block('hidden_effect',P+'upgrade_'+n['key']+' = yes')))
        loc[decision]='Complete the '+n['title']+' Programme'
        loc[decision+'_desc']='Complete the remaining work under the revised programme. Previous investment and delivered assets are credited. Outstanding cost: $[?'+uid+'_invoice|2] billion.'
    # A bounded daily quote refresh makes a pending decision affordable without
    # requiring an extra player-facing bookkeeping event.
    quote_tick='\n'.join(block('if',block('limit',flag(n['id']+'_audit_upgrade_pending'))+P+'quote_upgrade_'+n['key']+' = yes') for n in data['nodes'] if not n.get('audit_retired') and n.get('audit_delivery_components'))
    effects+=block(P+'refresh_audit_upgrade_quotes',block('if',block('limit','COLDWAR_IRQ_campaign_active = yes')+quote_tick))
    return effects,decs,loc
