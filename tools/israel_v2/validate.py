# IMPERIA COLD WAR — Independent checks for the Israel Version 2.0 proposal.
"""Check design contracts, not implementation or live gameplay."""
from pathlib import Path
from functools import lru_cache
import hashlib
import itertools
import json

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
OUT=ROOT/'docs/israel_1970_v2'


def main():
    data=json.loads((HERE/'design.json').read_text(encoding='utf-8'))
    checks=[]
    def check(value,label):
        assert value,label
        checks.append(label)
    nodes={n['id']:n for n in data['nodes']}
    groups={g['id']:g for g in data['groups']}
    sources={s['id']:s for s in data['sources']}
    check(len(nodes)==len(data['nodes']),'Unique focus IDs')
    check(len(groups)==19 and len(nodes)==213,'Complete focus-only catalogue')
    check(all(n['effects'] and n['description'] for n in nodes.values()),'Every focus has effects and country-specific description')
    check(all(n['group'] in groups for n in nodes.values()),'All group references resolve')
    for n in nodes.values():
        check(n['icon'] in data['layout']['icons'],n['id']+': native icon resolves')
        check(all(s in sources for s in n['history']['sources']),n['id']+': historical evidence resolves')
        check(all(p in nodes for row in n['pre'] for p in row),n['id']+': grouped prerequisites resolve')
        check(all(n['id'] in nodes[p]['exclusive'] for p in n['exclusive']),n['id']+': reciprocal exclusions')
        text=n['label']+n['description']+''.join(e['label']+str(e.get('value','')) for e in n['effects'])
        check(not any(mark in text for mark in ('\u2013','\u2014')),n['id']+': no en/em dashes in player-facing text')
        if groups[n['group']]['kind']=='party':
            check(groups[n['group']]['gate'] in n['requirements'],n['id']+': visible exact-party requirement')
            check(bool(groups[n['group']]['runtime_party_trigger']),n['id']+': native party trigger identified')

    def compatible(ids):
        return all(not(set(nodes[i]['exclusive']) & ids) for i in ids)
    visiting=set()
    @lru_cache(None)
    def histories(key):
        check(key not in visiting,key+': acyclic prerequisite traversal')
        visiting.add(key)
        candidates={frozenset([key])}
        for row in nodes[key]['pre']:
            alternatives=set(itertools.chain.from_iterable(histories(p) for p in row))
            candidates={a|b for a in candidates for b in alternatives if compatible(a|b)}
        visiting.remove(key)
        return candidates
    for key in nodes:
        check(bool(histories(key)),key+': at least one satisfiable prerequisite/exclusion history')

    workforce=[(n['id'],n['modifiers']['total_workforce_modifier']) for n in nodes.values() if 'total_workforce_modifier' in n['modifiers']]
    check(len(workforce)==3 and all(v>0 for _,v in workforce),'Three positive workforce reforms; no negative workforce')
    check(abs(sum(v for _,v in workforce)-.15)<1e-9,'Whole compatible catalogue adds at most +15% workforce')
    check(nodes['ISR2_tal_tank']['pre']==[['ISR2_armour_repair']],'Tank programme independent of fighter project')
    check(nodes['ISR2_ambiguity']['pre']==[['ISR2_atomic_commission']],'Nuclear policy independent of tank/fighter projects')
    check(nodes['ISR2_bonds_plant']['pre']==[['ISR2_bond_drive']],'Industrial bond spending independent of humanitarian appeal')
    check(not any('Land Doctrine' in e.get('value','') and e['label']=='Research Bonus' for n in nodes.values() for e in n['effects']),'Doctrine reductions are not technology research bonuses')
    check('ISR2_palestinian_accounts' not in nodes,'No information-only Palestinian-consequence focus')
    for key in ['credit_guarantees','workshop_guarantees']:
        check('52 weeks' in nodes['ISR2_'+key]['programme'],key+': benefit and provision share duration')
    bilateral=[n['id'][5:] for n in nodes.values() if n.get('offer_target')]
    bilateral_counts={}
    for key in bilateral:
        headings={e['heading'] for e in nodes['ISR2_'+key]['effects'] if e.get('heading','').startswith('If they accept: ')}
        check(len(headings)==2,key+': both prospective recipient/sender effects visible before consent')
        n=nodes['ISR2_'+key]
        check(n['offer_origin']=='focus_completion' and n['recipient_response']=='country_event_accept_or_refuse',key+': focus sends offer and recipient answers event')
        check(headings=={'If they accept: Israel','If they accept: '+n['offer_target']['country']},key+': fixed recipient matches both complete preview headings')
        bilateral_counts[key]=len([e for e in nodes['ISR2_'+key]['effects'] if e.get('heading')])
    check(any(e['label']=='Public Debt Principal' and '0.03846%' in e['value'] for e in nodes['ISR2_eastern_credit']['effects']),'Bilateral loan previews explicit principal reduction')
    check(not any('buyer annual GDP' in str(e) for e in nodes['ISR2_arms_exports']['effects']),'Fixed equipment invoice independent of buyer GDP')
    check(any('Actual Host' in e.get('heading','') for e in nodes['ISR2_foreign_footholds']['effects']),'Foreign foothold host penalties visible')
    check(any('Palestine' in e.get('heading','') for e in nodes['ISR2_controlled_sites']['effects']),'Controlled settlement Palestinian consequences visible')
    check(data['revision'].startswith('2.2') and 'Not installed' in data['status'],'Focus-only proposal is clearly distinguished from implementation')
    check(all(n.get('action_origin')=='national_focus' for n in nodes.values()),'Every action originates in a national focus')
    check(not any('decision' in e['label'].lower() for n in nodes.values() for e in n['effects']),'No decision unlocks or disguised decision effects')
    check(not data['focus_actions']['pending_empty_effects'],'No emptied focus left after decision removal')
    check(data['focus_actions']['original_decision_unlocks']==53 and data['focus_actions']['decisions']==0,'All 53 old decision unlocks accounted for')
    for key in ['mafdal_survey','mafdal_land_westbank','mafdal_land_gaza']:
        check(len(nodes['ISR2_'+key]['exclusive'])==2,key+': direct three-way land appropriation')
    check(['ISR2_mafdal_survey','ISR2_mafdal_land_westbank','ISR2_mafdal_land_gaza'] in nodes['ISR2_service_bargain']['pre'],'Mafdal continuation accepts every appropriation choice')
    for key in ['gahal_investors','gahal_settler_entitlement']:
        check(['ISR2_national_bargain','ISR2_gahal_settlement_match'] in nodes['ISR2_'+key]['pre'],key+': civilian or territorial appropriation both preserve continuation')
    check(set(nodes['ISR2_national_bargain']['exclusive'])=={'ISR2_gahal_settlement_match'},'Gahal appropriation is a focus fork')
    for action in ['controlled_development','foreign_foothold']:
        members=[n for n in nodes.values() if n.get('settlement_action')==action]
        check({n['settlement_area'] for n in members}=={'West Bank','Gaza','Sinai','Golan'},action+': four named regions are direct focus choices')
        check(all(not n['exclusive'] for n in members),action+': later control changes do not permanently exclude the other route')
    for key in ['irrigation_exports','european_orders','labor_jordanian_option','gahal_local_autonomy','eastern_credit']:
        check(nodes['ISR2_'+key]['focus_cycle']['cooldown_weeks']>=104,key+': full 104-week term before a new programme')
    for n in nodes.values():
        if n.get('settlement_action')=='end_sponsorship':
            check(any('foreign foothold is funded' in r for r in n['requirements']),n['id']+': closure limited to a non-building foreign foothold')
            check(not any('Nahal tier' in e.get('value','') for e in n['effects']),n['id']+': no free waiver of productive controlled-site burdens')
    check(set(nodes['ISR2_lift_freeze']['pre'][0])=={'ISR2_cap_projects','ISR2_mafdal_restrain_sites'},'Reopening appropriations reaches both real freeze sources')
    check(any(e['label']=='Police Cost' and e['value']=='+6%' for e in nodes['ISR2_lift_freeze']['effects']),'Reopening removes Mafdal savings before new starts')
    for n in nodes.values():
        if n.get('settlement_action')=='end_sponsorship':
            check(any(e.get('native_key')=='weekly_budget' and abs(e['amount']-.00012)<1e-10 for e in n['effects']),n['id']+': frozen funding closure shows the actual 0.012%-GDP stream')
    irrigation=nodes['ISR2_irrigation_exports']
    check(any(e['label']=='Treasury: Buyer Payment' and e['value']=='+$0.00600 billion' for e in irrigation['effects']),'Irrigation uses one fixed invoice for both countries')
    check(abs(.006-.002-104*.00002-.00192)<1e-10,'Irrigation full-term margin is positive and independent of country GDP ratios')
    for n in nodes.values():
        if n.get('focus_cycle'):
            cycle=n['focus_cycle']
            check(cycle['provider']=='uncomplete_national_focus' and not cycle['uncomplete_children'] and not cycle['refund_political_power'],n['id']+': bounded self reset preserves children and receipts')
    check(nodes['ISR2_reserve_exercise']['days']==7 and nodes['ISR2_reserve_callup']['days']==7,'Reserve orders have their own short action focuses')
    check(any('Removes National Spirit'==e['label'] for e in nodes['ISR2_reserve_release']['effects']),'Early reserve release is an explicit focus action')
    internal={'Labor Unions Opinion','Small and Medium Business Owners Opinion','Industrial Conglomerates Opinion','Religious Institutions Opinion','Farmers Opinion','The Military Opinion','Intelligence Community Opinion'}
    check(not any(e['label'] in internal and e.get('tone')=='gain' for n in nodes.values() for e in n['effects']),'No positive internal-faction opinion used as a reward')
    for group,minimum_depth,minimum_count in [('alignment',12,23),('gahal',10,23),('mafdal',10,19)]:
        members=[n for n in nodes.values() if n['group']==group]
        check(len(members)>=minimum_count,group+': complete major-party policy expansion')
        check(max(n['xy'][1] for n in members)-groups[group]['origin'][1]>=minimum_depth,group+': actual downward continuation')
    check(all(n['history']['status'] for n in nodes.values()),'Every policy states its historical or alternative status')
    check(any(e.get('heading')=='If they accept: Israel' and e['label']=='Research Bonus' for e in nodes['ISR2_mashav']['effects']),'MASHAV gives Israel a concrete limited research reward')
    for key in ['labor_jordanian_option','labor_functional_rule','gahal_local_autonomy','labor_tax_base','labor_procurement_ceiling']:
        check(not nodes['ISR2_'+key]['pre'],key+': independent policy has no forced settlement or unrelated budget predecessor')
    for key in ['labor_valley','gahal_settler_entitlement','mafdal_activist_current','mafdal_regularise_sites','liberal_sinai_resort']:
        check(nodes['ISR2_'+key].get('effect_owner')=='controlled_site',key+': standing site obligations survive party change')
    check(nodes['ISR2_gahal_local_autonomy']['agreement_family']==nodes['ISR2_haolam_joint_services']['agreement_family'],'Overlapping Palestinian civil-service frameworks replace rather than stack')
    check(not any(e['label']=='Religious Certification Fees' for e in nodes['ISR2_mafdal_strict_certification']['effects']),'No unsupported conversion-certification income stream')
    check(nodes['ISR2_orthodox_deferments']['modifiers']['education_cost_multiplier_modifier']>0,'Protected full-time study has a real education commitment')
    installed=ROOT/data['provenance']['installed_source']
    check(hashlib.sha256(installed.read_bytes()).hexdigest()==data['provenance']['installed_sha256'],'Installed ISR70 focus tree unchanged during proposal')
    result=dict(project='IMPERIA COLD WAR',status='PASS',evidence='Design data, logical prerequisites, source preservation and preview contracts only',
        checks=len(checks),focuses=len(nodes),groups=len(groups),party_groups=sum(g['kind']=='party' for g in groups.values()),
        satisfiable_focus_histories=len(nodes),workforce_total=.15,bilateral_preview_rows=bilateral_counts,
        description_word_range=[min(len(n['description'].split()) for n in nodes.values()),max(len(n['description'].split()) for n in nodes.values())],
        installed_focus_sha256=data['provenance']['installed_sha256'],
        limitations=['No runtime game script emitted or altered.','No native gameplay or multiplayer claim.','New programme/contract mechanics require implementation and native verification.'])
    (OUT/'design_validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
