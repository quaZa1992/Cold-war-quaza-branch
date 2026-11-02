# IMPERIA COLD WAR — enumerate compatible completed policy programmes.
"""Audit new direct modifiers, not a simulated MD economy or an engine test."""
from collections import defaultdict
from itertools import product
from pathlib import Path
import json,sys
sys.dont_write_bytecode=True
import content as c

OUT=Path(__file__).resolve().parents[2]/'docs/design/cuba_1970_concept'
BY={n['id']:n for n in c.NODES}

def terminal_paths(group):
    nodes=[n for n in c.NODES if n['group']==group]
    pairs=sorted({tuple(sorted((n['id'],other))) for n in nodes for other in n['mutually_exclusive']})
    results=[]
    for choices in product((0,1),repeat=len(pairs)):
        blocked={pair[1-ch] for pair,ch in zip(pairs,choices)}
        active=set()
        for n in sorted(nodes,key=lambda n:n['xy'][1]):
            if n['id'] not in blocked and all(any(p in active for p in block) for block in n['prerequisites']):active.add(n['id'])
        if active not in results:results.append(active)
    return results

def totals(ids):
    result=defaultdict(float)
    for nid in ids:
        n=BY[nid]
        if n['key']=='finish_zafra':continue # campaign is expired in the mature comparison
        for k,v in n['modifiers'].items():result[k]+=v
    return result

def main():
    shared=[g for g in c.GROUPS if g['slot'] is None]
    government=[g for g in c.GROUPS if g['slot'] is not None]
    common=[set().union(*paths) for paths in product(*(terminal_paths(g['id']) for g in shared))]
    reports=[];total_cases=0
    for g in government:
        values=[]
        for base in common:
            for route in terminal_paths(g['id']):
                ids=base|route;t=totals(ids)
                # Mature tree: reform removes the original Offensive and campaign;
                # both food/industry mitigations have been completed where compatible.
                for s in c.STARTING_SPIRITS:
                    if s['id'].endswith(('zafra_campaign','revolutionary_offensive','sugar_oil','committees_defence')):continue
                    for k,v in s['modifiers'].items():t[k]+=v
                food=c.PREFIX+'food_first' in ids;industry=c.PREFIX+'light_industry' in ids
                dep={'agricolture_productivity_modifier':0 if food else .05,'imp_sanction_resistance':-.02 if food else -.06,'foreign_influence_defense_modifier':-.03 if food else -.06}
                for k,v in dep.items():t[k]+=v
                civic=g['id'] in ('autentico','ortodoxo','christian','liberal','rece') or (g['id']=='alpha' and c.PREFIX+'veterans_civil_life' in ids)
                professional=g['id'] in ('pcc','far') or (g['id']=='minint' and c.PREFIX+'professional_intelligence' in ids)
                institution={'intelligence_agency_defense':.05,'bureaucracy_cost_multiplier_modifier':.03} if civic else {'intelligence_agency_defense':.10,'political_power_factor':-.04,'research_speed_factor':-.02} if professional else {'intelligence_agency_defense':.15,'political_power_factor':-.08,'research_speed_factor':-.03}
                for k,v in institution.items():t[k]+=v
                values.append(dict(t))
        keys=sorted(set().union(*(x.keys() for x in values)));total_cases+=len(values)
        ranges={k:[round(min(t.get(k,0) for t in values),5),round(max(t.get(k,0) for t in values),5)] for k in keys}
        reports.append(dict(programme=g['label'],cases=len(values),ranges=ranges))
    report=dict(cases=total_cases,common_terminal_routes=len(common),programmes=reports,limits='Direct new focus and starting-spirit modifier deltas only. Accepted treaty grants, native law-tier effects, cap fallbacks, influence calculations, other mods, events and temporary crises excluded. This is a combinatorial ceiling/floor audit, not projected national GDP or an in-game tooltip total.')
    (OUT/'BALANCE_RANGES.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    keys=['civilian_factories_productivity','production_speed_buildings_factor','research_speed_factor','total_workforce_modifier','bureaucracy_cost_multiplier_modifier','resource_export_multiplier_modifier']
    fmt=lambda v:f'{v[0]*100:+.0f}…{v[1]*100:+.0f}%'
    md=['# COLDWAR_CUB — compatible programme ranges','',report['limits'],'',f'{total_cases} compatible mature configurations across {len(common)} shared national routes and {len(government)} governments. Mutually exclusive choices and downstream reachability are respected. No two government programmes are stacked.','', '| Government | Civilian productivity | Construction | Research | Workforce | Weekly bureaucracy | Resource export revenue |','|---|---:|---:|---:|---:|---:|---:|']
    md += ['| '+r['programme']+' | '+' | '.join(fmt(r['ranges'].get(k,[0,0])) for k in keys)+' |' for r in reports]
    md += ['', 'These are per-modifier ranges, not a single simultaneously attainable best route. Correlated costs remain attached to their focus. This is an eligibility-satisfied terminal comparison: the CMEA programme requires accepted membership in the Moscow routes. Completing all common programmes also requires paid infrastructure and factories, actual partner consent for treaties, and recurring native budget tier costs.','', 'The shared harvest campaign expires. The original Offensive is removed by enterprise reform. Sugar dependency is replaced by its diversification variant. The security institution is replaced by the completed professional/civic settlement. These are replacements, not hidden extra bonuses. The default US restriction and exile skills burden remain in this comparison; normalization and actual registered returns are optional negotiated improvements.','', 'Assessment: the alternatives prioritize different output, public expenditure and political autonomy; one preference-independent ranking is not assumed. The stronger late industrial/research totals accumulate national reconstruction and one current political programme over several years. Validate the native law and economy totals in a new 1970 engine session after implementation; source checks alone cannot establish final MP balance.']
    (OUT/'BALANCE_REVIEW.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=total_cases,common_routes=len(common),governments=len(government))))

if __name__=='__main__':main()
