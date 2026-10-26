# IMPERIA CW — Cold War: vietnam 1970 — validate rewards.
"""Independent numeric comparison of the explicit revision with emitted native AST."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from script_ast import parse,first,values,walk
from runtime_design import load_design,load_campaign_design

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];P='COLDWAR_VIE_'
spec=json.loads((HERE/'reward_rework.json').read_text(encoding='utf-8'))
def read(path):return parse((ROOT/path).read_text(encoding='utf-8-sig'))
effects=dict((k,v) for k,op,v in read('common/scripted_effects/COLDWAR_VIE_1970_effects.txt'))
ideas=dict((k,v) for k,op,v in first(first(read('common/ideas/COLDWAR_VIE_campaign_ideas.txt'),'ideas'),'country'))
D=load_design();C=load_campaign_design();by={n['id']:n for n in D['nodes']+C['nodes']}
errors=[];checks=0
def check(ok,message):
    global checks
    checks+=1
    if not ok:errors.append(message)
check(len(spec['focuses'])==239 and len(spec['campaigns'])==68,'Incomplete full-tree review')
check(set(p['id'] for p in spec['focuses']+spec['campaigns'])==set(by),'Revision IDs differ from installed tree')
for p in spec['focuses']:
    key=p['id'];n=by[key];prefix=P+n.get('programme_group',n['group'])+'_'
    inner=first(first(effects[P+'apply_'+key.removeprefix(P)],'if'),'if')
    actual={}
    for k,op,v in inner:
        if k=='add_to_variable':
            name,_,amount=next(r for r in v if r[0]!='tooltip')
            check(name.startswith(prefix),'Wrong programme owner: '+key)
            actual[name.removeprefix(prefix)]=float(amount)
    check(actual==p['modifiers'],'Wrong absolute focus contribution: '+key)
    rewards=[(k,v) for k,o,v in inner if k in ('add_tech_bonus','add_doctrine_cost_reduction')]
    expected=[r for r in p.get('rewards',[]) if r['type'] in ('research_bonus','doctrine_bonus')]
    check(len(rewards)==len(expected),'Finite reward count differs: '+key)
    for (kind,row),want in zip(rewards,expected):
        field='bonus' if want['type']=='research_bonus' else 'cost_reduction'
        check(kind==('add_tech_bonus' if field=='bonus' else 'add_doctrine_cost_reduction'),'Finite reward API differs: '+key)
        check(float(first(row,field))==want[field] and int(first(row,'uses'))==want['uses'] and first(row,'category')==want['category'],'Finite reward value/category differs: '+key)
    check('country_productivity_growth_modifier' not in p['modifiers'],'Signed growth sold as generic gain: '+key)
for p in spec['campaigns']:
    key=p['id']
    for e in p['effects']:
        if e['type']!='idea':continue
        row=ideas[key+'_policy']
        actual={k:float(v) for k,o,v in first(row,'modifier') if k!='custom_modifier_tooltip'}
        check(actual==e['modifiers'],'Campaign policy numbers differ: '+key)
        check('country_productivity_growth_modifier' not in actual,'Signed growth campaign reward: '+key)
        targeted=first(row,'targeted_modifier',[])
        check(first(targeted,'tag')==e['target'],'Wrong opponent scope: '+key)
        check({k:float(v) for k,o,v in targeted if k!='tag'}==e['targeted_modifiers'],'Wrong opponent numbers: '+key)
for q in D['decisions']:
    check(q['modifiers']==spec['decisions'][q['id']],'Decision revision omitted: '+q['id'])
    check('country_productivity_growth_modifier' not in q['modifiers'],'Signed growth decision reward: '+q['id'])
pairs={tuple(sorted((n['id'],peer))) for n in by.values() for peer in n['exclusive']}
for a,b in pairs:
    check(a in by[b]['exclusive'] and b in by[a]['exclusive'],'Nonreciprocal exclusive choice: '+a)
check(len(pairs)==55,'Expected two additional direct resource choices')
for key in ('chinh_schools','chinh_experts'):
    n=by[P+key];check(n['y']==1 and n['days']==70,'Core Chinh choice unreachable in his historical mandate')
    check(n['programme_group']=='chinh_training','Cadre knowledge expires with one chief')
check(by[P+'army_aircrew']['prerequisites']==[[P+'army_coast']],'Aircrew still requires dockyard')
for key in ('linh_limited','linh_guarantee'):
    check(by[P+key]['prerequisites']==[[P+'linh_monopoly',P+'linh_pluralism']],'Capital opening still requires political pluralism')
check(by[P+'industry_root']['instant_build'] and by[P+'industry_root']['building']==[522,'industrial_complex'],'No physical rehabilitation')
check(by[P+'industry_goods']['building'] is None,'Hanoi civilian factory is granted twice')
check(sum(bool(n['building']) for n in D['nodes'])==16,'Construction reward count unexpectedly changed')
for a in by.values():
    for b in by.values():
        if a['id']>=b['id']:continue
        # Native titlebar/card envelope, at exact resolved source positions.
        hit=abs(a['x']-b['x'])*96<164 and abs(a['y']-b['y'])*130<123
        check(not hit,'Native card overlap: '+a['id']+' '+b['id'])
manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
external=json.loads((ROOT/'docs/design/vietnam_rewards_rework_2026_10_19/external_edits_preserved.json').read_text(encoding='utf-8'))['hashes']
for rel in manifest['politics_sources']+manifest['politics_integration']+manifest['integration']:
    check((ROOT/rel).exists(),'Manual dependency missing: '+rel)
for name,want in [('approved_design.json','a75e577703dbfa708f5e7493539f46e5280628d1a1e940b3204a38d46082d3d2'),('approved_campaigns.json','ddce90a402e021c24693adf1eb61c3c92eab2cd49f2c2b0005de8a9f25e4e7d3')]:
    check(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==want,'Approval snapshot rewritten')
report=dict(status='pass' if not errors else 'fail',checks=checks,errors=errors,reviewed_focuses=len(by),exclusive_pairs=len(pairs),decision_programmes_rewritten=len(spec['decisions']),external_manual_edits_preserved=list(external),engine_tested=False)
(HERE/'reward_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2));raise SystemExit(bool(errors))
