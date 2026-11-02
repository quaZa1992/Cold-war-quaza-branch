# IMPERIA COLD WAR — France party expansion design checks.
"""Validate uninstalled proposal semantics, native references and preservation."""
from collections import Counter,defaultdict
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
    b=json.loads((HERE/'BASELINE.json').read_text(encoding='utf-8'))
    a=json.loads((HERE/'ADDITIONS.json').read_text(encoding='utf-8'))
    frozen=json.loads((HERE/'RUNTIME_BASELINE.json').read_text(encoding='utf-8'))
    current={n['key']:n for n in d['nodes']};old={n['key']:n for n in b['nodes']}
    groups={g['id']:g for g in d['groups']}
    added={n['key'] for n in a['added_focuses']}
    issues=[]
    def check(ok,msg):
        if not ok:issues.append(msg)
    check(len(current)==len(d['nodes'])==176,'Roster/duplicate focus key')
    check(len({n['id'] for n in d['nodes']})==176,'Duplicate focus ID')
    check(len(added)==20 and set(current)-set(old)==added,'Exactly twenty new focuses')
    check(sum('offer' in n for n in d['nodes'])==35,'Keep thirty-five signed agreement designs')
    check(len(d['decisions'])==len(b['decisions'])==5,'No duplicated funding decision')
    for rel,digest in frozen['files'].items():
        check(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest,'Loaded runtime drift: '+rel)
    for key,n in old.items():
        if key in ('cid_tax','cid_cooperatives'):
            clean=dict(current[key])
            for fieldname in ('modifier_pool','spirit','spirit_name','programme_activation_conditions'):
                if fieldname in n:clean[fieldname]=n[fieldname]
                else:clean.pop(fieldname,None)
            check(clean==n,'Unexpected legacy CID change: '+key)
        else:check(current[key]==n,'Original focus changed: '+key)
    for n in d['nodes']:
        for parents in n['prerequisites']:
            check(bool(parents) and all(p in current for p in parents),n['key']+': prerequisite reference')
        for key in n['exclusions']:
            check(key in current and n['key'] in current[key]['exclusions'],n['key']+': reciprocal exclusion')
        if n.get('anchor'):
            root=next((p for p in d['nodes'] if p['id']==n['anchor']),None)
            check(root is not None,n['key']+': anchor')
            if root:
                check([n['x']-root['x'],n['y']-root['y']]==n['offset'],n['key']+': relative offset')
                check(d['nodes'].index(root)<d['nodes'].index(n),n['key']+': forward anchor')
    visiting=set();done=set()
    def visit(key):
        if key in done:return
        check(key not in visiting,'Prerequisite cycle at '+key)
        if key in visiting:return
        visiting.add(key)
        for parent in sum(current[key]['prerequisites'],[]):visit(parent)
        visiting.remove(key);done.add(key)
    for key in current:visit(key)
    modifiers='\n'.join(p.read_text(encoding='utf-8-sig',errors='replace') for folder in ('common/ideas','common/dynamic_modifiers') for p in (ROOT/folder).glob('*.txt'))
    technologies=(ROOT/'common/technology_tags/00_technology.txt').read_text(encoding='utf-8-sig')
    buildings=next(n for n in nodes((ROOT/'common/buildings/00_buildings.txt').read_text(encoding='utf-8-sig')) if n.key=='buildings')
    caps={}
    for building in buildings.children():
        cap=next((n for n in building.children() if n.key=='level_cap'),None)
        if cap and field(cap.children(),'state_max') is not None:caps[building.key]=int(field(cap.children(),'state_max'))
    sprites=set(re.findall(r'\bname\s*=\s*"([^"]+)"',(ROOT/'interface/COLDWAR_FRA2_polish_art.gfx').read_text()))
    counts=Counter();assets=Counter();initial={}
    for key in added:
        n=current[key];party=groups[n['group']]['trigger']+' = yes'
        check(party in n['conditions'] and party in n['reward_guards'],key+': exact party gate')
        check(n['lifetime']=='government',key+': party programme lifetime')
        check(n['icon'] in sprites and n['icon']+'_shine' in sprites,key+': native artwork')
        check(not any(x in n['title']+n['description'] for x in '\u2013\u2014'),key+': player punctuation')
        check(sum(e['kind']=='treasury_gdp' for e in n['effects'])==1,key+': setup fee count')
        for e in n['effects']:
            counts[e['kind']]+=1
            if e['kind']=='treasury_gdp':
                check(e['base']=='gdp_total' and e['payer']=='own_country' and e['once'],key+': current own-GDP fee')
                check(Decimal(str(e['percent']))/100==Decimal(e['runtime_share_literal']),key+': GDP fraction')
                check(len(e['runtime_share_literal'].split('.')[-1])<=5,key+': monetary precision')
            if e['kind']=='modifier':
                check(re.search(r'\b'+re.escape(e['key'])+r'\s*=',modifiers) is not None,key+': unsupported modifier '+e['key'])
                check('influence' not in e['key'] or e['value']>=0,key+': influence penalty')
                check(not any(x in e['key'] for x in ('productivity','efficiency_gain','workforce','recruitable_population')),key+': forbidden repeated productivity/workforce effect')
            if e['kind']=='research':check(e['category'] in technologies,key+': research category')
            if e['kind'] in ('building','state_slots'):
                state=e['state']
                for guard in (f'owns_state = {state}',f'controls_state = {state}',f'has_full_control_of_state = {state}'):
                    check(guard in n['reward_guards'],key+': missing site preflight '+guard)
                files=list((ROOT/'history/states').glob(str(state)+'-*.txt'))
                check(len(files)==1,key+': state reference')
                if files and state not in initial:
                    st=nodes(files[0].read_text(encoding='utf-8-sig'))[0]
                    hist=next(x for x in st.children() if x.key=='history')
                    levels={};owner=field(hist.children(),'owner');controller=owner
                    for section in [hist]+[x for x in hist.children() if re.fullmatch(r'\d+\.\d+\.\d+',x.key) and tuple(map(int,x.key.split('.')))<=(1970,1,1)]:
                        owner=field(section.children(),'owner',owner);controller=field(section.children(),'controller',controller)
                        for block in (x for x in section.children() if x.key=='buildings'):
                            levels.update({x.key:int(x.value) for x in block.children() if not x.children() and str(x.value).isdigit()})
                    check(owner==controller=='FRA',key+': 1970 site ownership/control')
                    initial[state]=levels
                if e['kind']=='building':
                    check(e['slots']==e['amount'] and e['slots_before_construction'] and e['once'],key+': slot/once contract')
                    cap=caps[e['building']]
                    check(any('building_level@'+e['building'] in g and 'value = '+str(cap-e['amount'])+' ' in g for g in n['reward_guards']),key+': physical cap')
                    check(initial[state].get(e['building'],0)+e['amount']<=cap,key+': full at 1970 start')
                    assets[(state,e['building'])]+=e['amount']
                else:check(e['native_effect']=='add_extra_state_shared_building_slots' and e['once'],key+': slot preparation provider')
    routes={}
    for gid in ('ri','centre','radical','ps','pcf','psu','ecology','right'):
        keys=[n['key'] for n in d['nodes'] if n['group']==gid]
        valid=[]
        for mask in range(1<<len(keys)):
            chosen={k for i,k in enumerate(keys) if mask>>i&1}
            if any(chosen.intersection(current[k]['exclusions']) or any(not chosen.intersection(p) for p in current[k]['prerequisites']) for k in chosen):continue
            valid.append(chosen)
        maximal=[s for s in valid if not any(s<t for t in valid)]
        routes[gid]=len(maximal)
        for key in added.intersection(keys):check(any(key in s for s in maximal),key+': unreachable')
    for key in ('cid_tax','cid_cooperatives','cid_wholesale_cooperatives','cid_rural_networks'):
        check(current[key].get('modifier_pool')=='CID' and 'date < 1972.10.5' in current[key].get('programme_activation_conditions',[]),key+': dated identity programme')
    change=a['decision_changes'][0]
    check(change['before']['effects']==change['after']['effects'],'Regional fund effects must not duplicate or change')
    check('OR = { has_completed_focus = COLDWAR_FRA2_public_banks has_completed_focus = COLDWAR_FRA2_ps_conversion_boards }' in change['after']['runtime_guards'],'Regional fund alternative mandate')
    # A deliberately conservative history-derived ceiling: count even mutually
    # exclusive grants. If this fits, every compatible subset also fits before
    # manual construction or other external development changes the state.
    all_awards=[e for n in d['nodes'] for e in n['effects']]
    all_awards += [e for n in d['nodes'] if n.get('offer') for side in ('france','recipient') for e in n['offer'][side]['effects']]
    all_awards += [e for decision in d['decisions'] for e in decision['effects']]
    all_grants=Counter((e['state'],e['building']) for e in all_awards if e['kind']=='building' and not e.get('province') and e['state'] in initial)
    upper_bounds=[]
    for (state,building),amount in sorted(all_grants.items()):
        cap=caps[building];start=initial[state].get(building,0)
        check(start+amount<=cap,f'History-based conservative asset ceiling exceeds {building} cap in {state}')
        upper_bounds.append(dict(state=state,building=building,history_start=start,all_design_grants=amount,cap=cap))
    report=dict(project='IMPERIA COLD WAR',phase='Design-only, not installed',proposal_sha256=hashlib.sha256((HERE/'proposal.json').read_bytes()).hexdigest(),baseline_focuses=156,proposed_focuses=176,new_focuses=20,original_lifecycle_revisions=2,offers=35,new_decisions=0,broadened_existing_decisions=1,exclusive_pairs=sum(len(n['exclusions']) for n in d['nodes'])//2,maximal_campaign_routes=routes,new_effect_counts=dict(counts),new_building_levels=sum(assets.values()),new_standalone_slots=sum(e['amount'] for n in a['added_focuses'] for e in n['effects'] if e['kind']=='state_slots'),conservative_asset_ceilings=upper_bounds,loaded_runtime_preserved=not any('runtime drift' in x for x in issues),native_engine_tested=False,issues=issues,passed=not issues)
    (HERE/'DESIGN_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));return bool(issues)


if __name__=='__main__':sys.exit(main())
