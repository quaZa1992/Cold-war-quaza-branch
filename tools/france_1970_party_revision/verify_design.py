# IMPERIA COLD WAR — France party proposal contract checks.
"""Validate the proposal and prove that the installed game files are untouched."""
from __future__ import annotations
from collections import Counter, defaultdict
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from focus_prerequisite_ui import nodes,field

def main():
    d=json.loads((HERE/'proposal.json').read_text(encoding='utf-8'))
    base=json.loads((HERE/'BASELINE.json').read_text(encoding='utf-8'))
    baseline=json.loads((HERE/'RUNTIME_BASELINE.json').read_text())
    changes=json.loads((HERE/'CHANGES.json').read_text(encoding='utf-8'))
    bykey={n['key']:n for n in d['nodes']};old={n['key']:n for n in base['nodes']}
    groups={g['id']:g for g in d['groups']}
    issues=[]
    def check(ok,message):
        if not ok:issues.append(message)
    check(len(bykey)==len(d['nodes'])==156,'Focus roster/duplicate keys')
    check(len({n['id'] for n in d['nodes']})==156,'Duplicate focus IDs')
    for rel,digest in baseline['loaded_files'].items():
        check(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest,'Loaded game file changed: '+rel)
    check(hashlib.sha256((ROOT/'tools/france_1970_runtime/runtime_design.json').read_bytes()).hexdigest()==baseline['runtime_design_sha256'],'Installed design changed')
    changed={c['key'] for c in changes['changes']}
    check(len(changed)==39,'Expected 39 changed/new focuses')
    for n in d['nodes']:
        key=n['key']
        if key not in changed:check(n==old[key],key+': unlisted edit')
        for group in n['prerequisites']:
            check(bool(group) and all(p in bykey for p in group),key+': invalid prerequisite group')
        for other in n['exclusions']:
            check(other in bykey and key in bykey[other]['exclusions'],key+': nonreciprocal exclusion')
        if n.get('anchor'):
            anchor=next((a for a in d['nodes'] if a['id']==n['anchor']),None)
            check(anchor is not None,key+': missing anchor')
            if anchor:check([n['x']-anchor['x'],n['y']-anchor['y']]==n['offset'],key+': incorrect relative offset')
        if key in changed:
            check(groups[n['group']]['trigger']+' = yes' in n['conditions'],key+': missing exact party requirement')
        for fieldname in ('title','description'):
            check(not any(c in n[fieldname] for c in '\u2013\u2014'),key+': player punctuation')
    # Satisfiability: prerequisites are OR within one group and AND across groups.
    alternatives={}
    for gid,g in groups.items():
        if g.get('slot') is None or gid=='udr_nato':continue
        own=[n for n in d['nodes'] if n['group']==gid];keys=[n['key'] for n in own]
        routes=[]
        for mask in range(1<<len(keys)):
            chosen={k for i,k in enumerate(keys) if mask>>i&1}
            valid=True
            for key in chosen:
                n=bykey[key]
                if chosen.intersection(n['exclusions']):valid=False;break
                for parents in n['prerequisites']:
                    local=[p for p in parents if bykey[p]['group']==gid]
                    if len(local)==len(parents) and not chosen.intersection(local):valid=False;break
                if not valid:break
            if valid:routes.append(chosen)
        for key in keys:check(any(key in r for r in routes),key+': unreachable political route')
        maximal=[r for r in routes if not any(r<s for s in routes)]
        alternatives[gid]=len(maximal)
    check(bykey['pcf_energy_contract']['exclusions']==['pcf_shipping_contract'],'PCF energy exclusive choice')
    check(bykey['pcf_shipping_contract']['exclusions']==['pcf_energy_contract'],'PCF shipping exclusive choice')
    check(bykey['communist_settlement']['prerequisites']==[['independent_communism','pcf_energy_contract','pcf_shipping_contract']],'PCF consolidation OR join')
    # Keep the previous 19 shared agreements byte-semantically unchanged.
    for n in base['nodes']:
        if n.get('offer'):check(bykey[n['key']]==n,n['key']+': existing shared offer changed')
    offers=[n for n in d['nodes'] if n.get('offer') and n['key'] in changed]
    check(len(offers)==16,'Expected 16 party-specific agreements')
    check(sum('offer' in n for n in d['nodes'])==35,'Expected 35 total agreements')
    offerkeys={n['key'] for n in offers}
    for n in offers:
        o=n['offer']
        check(o['proposal_party']==n['group'],n['key']+': wrong proposing party')
        for side,tag in [('france','FRA'),('recipient',o['partner'])]:
            ef=o[side]['effects']
            check(o[side]['payer']==tag,n['key']+': payer country')
            check(sum(e['kind']=='treasury_gdp' for e in ef)==1,n['key']+': setup price count')
            check(sum(e['kind']=='weekly_gdp_expense' for e in ef)==1,n['key']+': weekly price count')
            check(any((e['kind'] in ('building','research','experience','doctrine')) or (e['kind']=='modifier' and e['value']>0) for e in ef),n['key']+': no partner benefit')
    entries=[]
    for n in d['nodes']:
        if n['key'] not in changed:continue
        entries.extend((n['key'],'FRA',e) for e in n['effects'])
        if n.get('offer'):
            for side,tag in [('france','FRA'),('recipient',n['offer']['partner'])]:entries.extend((n['key']+'/'+side,tag,e) for e in n['offer'][side]['effects'])
    for dec in d['decisions']:
        if dec['id'].startswith('COLDWAR_FRA2P_'):entries.extend((dec['id'],'FRA',e) for e in dec['effects'])
    counts=Counter()
    categories=(ROOT/'common/technology_tags/00_technology.txt').read_text(encoding='utf-8-sig') if (ROOT/'common/technology_tags/00_technology.txt').exists() else ''
    for origin,payer,e in entries:
        counts[e['kind']]+=1
        check(e['kind'] not in ('treasury','weekly_expense'),origin+': flat price')
        if e['kind'] in ('treasury_gdp','weekly_gdp_expense'):
            percent=e.get('percent',e.get('annual_gdp_percent'))
            check(Decimal(str(percent))/100==Decimal(e['runtime_share_literal']),origin+': imprecise GDP share')
            check(len(e['runtime_share_literal'].split('.')[-1])<=5,origin+': native precision')
            check(e['base']=='gdp_total' and e['payer']=='own_country',origin+': GDP base/payer')
            if e['kind']=='weekly_gdp_expense':check(e['divisor']==52,origin+': weekly conversion')
        if e['kind']=='building':
            check(e['slots']==e['amount'] and e['once'] and e['slots_before_construction'],origin+': slots/replay contract')
            files=list((ROOT/'history/states').glob(str(e['state'])+'-*.txt'))
            check(len(files)==1,origin+': state ID')
            if files:
                state=nodes(files[0].read_text(encoding='utf-8-sig'))[0]
                hist=next(c for c in state.children() if c.key=='history')
                snap=next((c for c in hist.children() if c.key=='1970.1.1'),None)
                owner=field(snap.children(),'owner',field(hist.children(),'owner')) if snap else field(hist.children(),'owner')
                check(owner==payer,origin+': wrong state owner '+str(owner))
        if e['kind']=='modifier':
            check(e['key'] not in ('available_workforce_factor','workforce_size_modifier','recruitable_population_factor') or e['value']>=0,origin+': negative workforce')
    report=dict(project='IMPERIA COLD WAR',phase='Design-only, not installed',proposal_sha256=hashlib.sha256((HERE/'proposal.json').read_bytes()).hexdigest(),
                focuses=156,changed_focuses=39,new_party_offers=16,total_offers=35,new_decisions=2,party_maximal_routes=alternatives,
                effect_counts_in_revision=dict(counts),loaded_runtime_preserved=not any('changed' in x or 'Installed design' in x for x in issues),
                native_engine_tested=False,issues=issues,passed=not issues)
    (HERE/'DESIGN_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    return bool(issues)

if __name__=='__main__':sys.exit(main())
