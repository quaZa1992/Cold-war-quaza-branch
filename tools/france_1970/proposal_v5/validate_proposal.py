# IMPERIA COLD WAR — Proposal logic, scope and compatible-route checks; no engine claims.
import hashlib
import itertools
import json
import re
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
D=json.loads((HERE/'proposal.json').read_text(encoding='utf-8'))
A=json.loads((HERE.parent/'approved_design.json').read_text(encoding='utf-8'))
C=json.loads((HERE/'mechanics_catalog.json').read_text(encoding='utf-8'))
checks=0
def check(ok,message):
    global checks
    checks+=1
    assert ok,message
by={n['key']:n for n in D['nodes']}
check(len(by)==len(D['nodes'])==260,'Focus count or duplicate')
check(len({n['id'] for n in D['nodes']})==260,'Duplicate IDs')
check(hashlib.sha256((HERE.parent/'approved_design.json').read_bytes()).hexdigest()==D['approved_base_sha256'],'Frozen input changed')
tags=set()
for path in (ROOT/'common/country_tags').glob('*.txt'):
    tags.update(re.findall(r'^\s*([A-Z0-9]{3})\s*=',path.read_text(encoding='utf-8-sig'),re.M))
source_ids={s['id'] for s in D['sources']}
providers={e.get('key') for e in C['entries']}
providers.update(json.loads((HERE.parent/'MODIFIER_PROVIDERS.json').read_text(encoding='utf-8'))['modifiers'])
providers.update(['energy_use_modifier_mils','pop_energy_use_multiplier','production_speed_agriculture_district_factor'])
for n in D['nodes']:
    check(n['id']=='COLDWAR_FRA_'+n['key'],n['key']+' prefix')
    check(not (n['key'].startswith('v5_') and '_strategy_' in n['key']),'Ceremonial filler root remains')
    check(all(k in by for k in n['parents'][0]) if len(n['parents'])==1 else all(k in by for row in n['parents'] for k in row),n['key']+' missing parent')
    check(all(k in by and n['key'] in by[k]['exclusive'] for k in n['exclusive']),n['key']+' asymmetric exclusion')
    check(not any(v==0 for v in n['mods'].values()),n['key']+' zero modifier')
    check(all(k in D['labels'] for k in n['mods']),n['key']+' missing numeric label')
    check(all(k in providers for k in n['mods']),n['key']+' unverified provider '+str(set(n['mods'])-providers))
    check(all(k in D['equipment_families'] for k in n.get('equipment',{})),n['key']+' unknown equipment')
    check(all(s in source_ids for s in n.get('sources',[])),n['key']+' missing source')
for o in D['offers']:
    check(o['partner'] in tags,o['id']+' invalid country tag '+o['partner'])
    check(o['family'] in D['agreement_rules']['families'],o['id']+' family')
    check(all(s in source_ids for s in o['sources']),o['id']+' source')
    for t in [o['france'],o['partner_terms']]:
        check(t['political_power']<0 and t['treasury_millions']<0,o['id']+' no concrete setup cost')
        check(not t['awards'],o['id']+' repeatable finite reward')
        check(all(k in providers for k in t['mods']),o['id']+' missing effect provider')
        check(all(v!=0 for v in t['mods'].values()),o['id']+' zero treaty effect')
        signs=[v*D['labels'][k][2] for k,v in t['mods'].items()]
        signs.extend([-v for v in t['equipment'].values()])
        check(any(v>0 for v in signs) and any(v<0 for v in signs),o['id']+' missing ongoing benefit or cost')
for family in D['equipment_families'].values():
    for classes in family['targets'].values():
        for cls in classes:
            check(any(re.search(r'^\s*'+re.escape(cls)+r'\s*=\s*\{',p.read_text(encoding='utf-8-sig'),re.M) for p in (ROOT/'common/units/equipment').glob('*.txt')),f'Missing equipment class {cls}')

envelopes=[]
for g in D['groups']:
    ns=[n for n in D['nodes'] if n['group']==g['id']]
    pairs=sorted({tuple(sorted((n['key'],e))) for n in ns for e in n['exclusive']})
    routes=set()
    for choices in itertools.product([0,1],repeat=len(pairs)):
        forbidden={p[bit] for p,bit in zip(pairs,choices)}
        reached=set()
        for _ in ns:
            extra={n['key'] for n in ns if n['key'] not in reached|forbidden and all(any(p in reached for p in row) for row in n['parents'])}
            if not extra:break
            reached.update(extra)
        check(not any(a in reached and b in reached for a,b in pairs),g['id']+' incompatible route')
        routes.add(tuple(sorted(reached)))
    union=set().union(*(set(r) for r in routes))
    check(union=={n['key'] for n in ns},g['id']+' unreachable focuses '+str({n['key'] for n in ns}-union))
    # Filter partial routes produced by forbidding descendants of an unavailable path.
    routes={r for r in routes if not any(set(r)<set(s) for s in routes)}
    sums=[]
    for r in routes:
        total={};eq={}
        for k in r:
            for m,v in by[k]['mods'].items():total[m]=round(total.get(m,0)+v,6)
            for m,v in by[k].get('equipment',{}).items():eq[m]=round(eq.get(m,0)+v,6)
        sums.append((total,eq))
    keys=set().union(*(set(t[0]) for t in sums));eqkeys=set().union(*(set(t[1]) for t in sums))
    envelopes.append({'group':g['id'],'compatible_complete_routes':len(routes),'modifiers':{k:[min(t[0].get(k,0) for t in sums),max(t[0].get(k,0) for t in sums)] for k in sorted(keys)},'equipment_cost':{k:[min(t[1].get(k,0) for t in sums),max(t[1].get(k,0) for t in sums)] for k in sorted(eqkeys)}})

family_overlays=[]
for family in D['agreement_rules']['families']:
    terms=[o['france'] for o in D['offers'] if o['family']==family]
    keys=set().union(*(set(t['mods']) for t in terms));eqkeys=set().union(*(set(t['equipment']) for t in terms))
    family_overlays.append({'family':family,'independent_per_modifier_bounds_not_one_bundle':True,'modifiers':{k:[min(0,*(t['mods'].get(k,0) for t in terms)),max(0,*(t['mods'].get(k,0) for t in terms))] for k in sorted(keys)},'equipment_cost':{k:[min(0,*(t['equipment'].get(k,0) for t in terms)),max(0,*(t['equipment'].get(k,0) for t in terms))] for k in sorted(eqkeys)}})
report={'project':'IMPERIA COLD WAR','result':'pass','checks':checks,'focuses':len(by),'offers':len(D['offers']),'source_catalogue_entries':len(C['entries']),'modifiers_used':len({k for n in D['nodes'] for k in n['mods']}|{k for o in D['offers'] for t in [o['france'],o['partner_terms']] for k in t['mods']}),'route_scope':'Active domestic programme only; starting and residual spirits retained separately; up to one accepted treaty per family may overlay across governments. No addition of mutually exclusive programmes. Finite research and projects are eligibility-gated, not assumed instantly available.','programmes':envelopes,'family_overlays':family_overlays,'engine_tested':False}
(HERE/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['programmes','family_overlays','route_scope']}))
