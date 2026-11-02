# IMPERIA COLD WAR — Independent fiscal and asset contract checks for the France concept.
from pathlib import Path
from decimal import Decimal
from collections import Counter
import hashlib
import json
import re

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
design=json.loads((OUT/'concept.json').read_text(encoding='utf-8'))
baseline=json.loads((OUT/'GDP_REWARD_BASELINE.json').read_text(encoding='utf-8'))
nodes={n['key']:n for n in design['nodes']}
issues=[]
def require(ok,message):
    if not ok:issues.append(message)
require(set(nodes)==set(baseline['nodes']),'Focus roster changed')
for key,old in baseline['nodes'].items():
    for field in ('x','y','group','prerequisites','exclusions'):
        require(nodes[key][field]==old[field],key+': changed '+field)

entries=[]
for n in design['nodes']:
    entries.extend((n['key'],'FRA',e) for e in n['effects'])
    require(n['reward_guards']==n['conditions'],n['key']+': stale reward guards')
    if n.get('offer'):
        offer=n['offer']
        for side,payer in [('france','FRA'),('recipient',offer['partner'])]:
            require(offer[side]['payer']==payer,n['key']+': wrong payer scope')
            entries.extend((n['key']+'/'+side,payer,e) for e in offer[side]['effects'])
        for field in ('acceptance_conditions','acceptance_transaction','asset_execution','payment_contract'):
            require(bool(offer.get(field)),n['key']+': missing '+field)
for d in design['decisions']:entries.extend((d['id'],'FRA',e) for e in d['effects'])

buildings=(ROOT/'common/buildings/00_buildings.txt').read_text(encoding='utf-8-sig')
factions=(ROOT/'common/scripted_effects/00_internal_faction_effects.txt').read_text(encoding='utf-8-sig')
counts=Counter()
for origin,payer,e in entries:
    kind=e['kind'];counts[kind]+=1
    require(kind not in ('treasury','weekly_expense'),origin+': fixed monetary amount')
    if kind in ('treasury_gdp','weekly_gdp_expense'):
        percent=e['percent'] if kind=='treasury_gdp' else e['annual_gdp_percent']
        expected=Decimal(str(percent))/100
        require(Decimal(e['runtime_share_literal'])==expected,origin+': inexact GDP literal')
        require(len(e['runtime_share_literal'].split('.')[-1])<=5,origin+': over-precise native literal')
        require(Decimal(str(e['gdp_fraction']))==expected,origin+': wrong GDP fraction')
        require(e['base']=='gdp_total' and e['payer']=='own_country',origin+': wrong GDP base')
        if kind=='treasury_gdp':
            require(e['once'] and e['valuation']=='at_payment',origin+': setup valuation/replay')
        else:
            require(e['divisor']==52 and e['valuation']=='weekly_recalculation',origin+': weekly conversion')
    if kind=='building':
        require(e['slots']==e['amount']>0 and e['slots_before_construction'] and e['once'],origin+': missing slot/order/receipt')
        require(bool(re.search(r'^\s*'+re.escape(e['building'])+r'\s*=\s*\{',buildings,re.M)),origin+': unsupported building')
        paths=list((ROOT/'history/states').glob(str(e['state'])+'-*.txt'))
        require(len(paths)==1,origin+': unresolved state')
        if paths:
            state=paths[0].read_text(encoding='utf-8-sig')
            require(bool(re.search(r'\bowner\s*=\s*'+payer+r'\b',state)),origin+': wrong asset-country reference')
            if e.get('province'):
                provinces=re.search(r'\bprovinces\s*=\s*\{([^}]*)\}',state,re.S)
                require(bool(provinces and str(e['province']) in provinces.group(1).split()),origin+': province outside state')
    if kind=='faction_opinion':
        require(e['parameter']=='temp_opinion' and e['once'],origin+': wrong opinion contract')
        require(bool(re.search(r'^'+re.escape(e['provider'])+r'\s*=\s*\{',factions,re.M)),origin+': unsupported faction helper')
    if kind=='modifier' and e['key'] in ('recruitable_population','recruitable_population_factor','available_workforce_factor','workforce_size_modifier'):
        require(e['value']>=0,origin+': negative workforce modifier')

sha=hashlib.sha256((OUT/'concept.json').read_bytes()).hexdigest()
qa=json.loads((OUT/'BROWSER_QA.json').read_text(encoding='utf-8'))
require(qa['concept_sha256']==sha and not qa['errors'],'Browser QA stale or failed')
report=dict(project='IMPERIA COLD WAR',revision=design['revision'],concept_sha256=sha,
    scope='Design contracts and local browser evidence only; no executable France runtime or HOI4 engine test',
    graph_preserved=len(baseline['nodes']),effect_counts=dict(counts),offers=sum('offer' in n for n in nodes.values()),
    revised_focuses=len(design['reward_revision']['changed_focuses']),browser_focus_clicks=qa['focus_clicks'],
    engine_tested=False,issues=issues)
(OUT/'GDP_REWARD_CHECKS.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
if issues:raise SystemExit(1)
