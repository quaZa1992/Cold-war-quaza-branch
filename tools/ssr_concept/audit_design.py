# IMPERIA COLD WAR — static audit of the SSR 1970 concept design.
"""Audit generated design data only. Does not test or modify loaded game content."""
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/design/ssr_1970_concept'
DESIGN_PATH = OUT / 'DESIGN.json'
AUDIT_PATH = OUT / 'DESIGN_AUDIT.json'
EXPECTED_TAGS = {'UKR','BLR','MLV','EST','LAT','LIT','GEO','ARM','AZE','KAZ','UZB','TRK','KYR','TAJ'}
SPEC_ROLES = {'aircraft','armour','artillery','army','navy','agriculture','industry','resources','electronics'}
SPEC_SUFFIXES = {'mandate','works','schools','left','right','left_follow','right_follow','office','priority','efficiency','settlement'}
PARTY_TRIGGER_KEYS = {0,1,2,3,4,12,14,18,20,21}
NAVAL_SEAS = {'UKR':'Black Sea','EST':'Baltic Sea','LAT':'Baltic Sea','LIT':'Baltic Sea','GEO':'Black Sea',
              'AZE':'Caspian Sea','KAZ':'Caspian Sea','TRK':'Caspian Sea'}
BAD_WORDS = ('cost','consumption','training_time','energy_use','consumer_goods')


def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))


def price_digits(value):
    try:
        return max(0,-Decimal(str(value)).as_tuple().exponent)
    except (InvalidOperation, ValueError):
        return 99


def is_benefit(key,value):
    bad=any(word in key for word in BAD_WORDS)
    return value < 0 if bad else value > 0


def expected_legacy(key,value):
    return round(value*(.20 if is_benefit(key,value) else .75),5)


def walk(value,path='$'):
    yield path,value
    if isinstance(value,dict):
        for key,item in value.items():
            yield from walk(item,path+'.'+str(key))
    elif isinstance(value,list):
        for index,item in enumerate(value):
            yield from walk(item,f'{path}[{index}]')


def historical_core(node,warnings,tag):
    description=node.get('description','').strip()
    marker='Historical precedent:'
    position=description.rfind(marker)
    if position < 1 or position < len(description)*.35 or not description.endswith('.'):
        warnings.add(f'{tag} specialization history is not a terminal Historical precedent suffix: {node["id"]}')
        return description
    return description[:position].rstrip().rstrip('.;:').rstrip()


def node_map(model):
    return {node['id']:node for node in model['nodes']+model.get('external',[])}


def node_reference_keys(node,by_id):
    def key(ref):
        return by_id.get(ref,{}).get('key',ref)
    return {
        'prerequisites':[[key(ref) for ref in group] for group in node.get('prerequisites',[])],
        'exclusive':[key(ref) for ref in node.get('exclusive',[])],
        'anchor':key(node['anchor']) if node.get('anchor') else None,
    }


def reachable_subsets(nodes):
    """Reachable completed subsets within a group, assuming outside-group prerequisites are met."""
    by_id={node['id']:node for node in nodes}
    outside={ref for node in nodes for group in node.get('prerequisites',[]) for ref in group if ref not in by_id}
    seen={frozenset()}
    todo=[frozenset()]
    while todo:
        done=todo.pop()
        for node in nodes:
            if node['id'] in done or any(ref in done for ref in node.get('exclusive',[]) if ref in by_id):
                continue
            if any(not any(ref in done or ref in outside for ref in group) for group in node.get('prerequisites',[])):
                continue
            new=done|{node['id']}
            if new not in seen:
                seen.add(new);todo.append(new)
    return seen,by_id


def delta_for(node,known):
    if node.get('replace'):
        if node.get('display_modifiers') is not None:
            return node['display_modifiers']
        old=known.get(node['replace'],{})
        return {key:round(node.get('modifiers',{}).get(key,0)-old.get(key,0),5)
                for key in set(old)|set(node.get('modifiers',{}))}
    return node.get('modifiers',{})


def audit_design(design,design_bytes):
    errors=[]
    warnings=set()
    reports={}
    models=design.get('models',{})
    if set(models)!=EXPECTED_TAGS:
        errors.append(f'model tag set mismatch: {sorted(set(models)^EXPECTED_TAGS)}')
    if design.get('project')!='IMPERIA COLD WAR':
        errors.append('missing project identifier')

    labels=set(design.get('labels',{}))
    party_triggers={int(key):value for key,value in design.get('party_triggers',{}).items()}
    if not PARTY_TRIGGER_KEYS.issubset(party_triggers):
        errors.append('party trigger table omits a used native MD slot')

    # GDP shares are the only script-defined treasury prices. Native focus PP costs remain separate.
    monetary_keys={'gdp_cost','weekly_gdp_cost','legacy_weekly_gdp_cost','gdp_income'}
    for path,value in walk(design):
        if isinstance(value,dict):
            for forbidden in ('cash','fixed_cash_cost','fixed_money_cost','usd_cost'):
                if forbidden in value and value[forbidden] not in (0,None,''):
                    errors.append(f'fixed-currency field {path}.{forbidden}')
            for key in monetary_keys:
                if key in value:
                    amount=value[key]
                    if not isinstance(amount,(int,float)) or amount < 0:
                        errors.append(f'invalid GDP amount {path}.{key}={amount!r}')
                    elif price_digits(amount)>5:
                        errors.append(f'GDP amount exceeds five fractional digits {path}.{key}={amount!r}')

    # Market course clique, duration, prices, finite methods and finite sector lots.
    market=design.get('market',{})
    courses=market.get('courses',{})
    expected_courses={'shock','gradual','directed'}
    if set(courses)!=expected_courses:
        errors.append(f'market course set mismatch: {sorted(set(courses)^expected_courses)}')
    for course_key,course in courses.items():
        for timed in ('window','fiscal'):
            if course.get(timed,{}).get('days')!=730:
                errors.append(f'{course_key} {timed} course duration is not 730 days')
        for amount_key in ('gdp_cost','weekly_gdp_cost'):
            if amount_key not in course:
                errors.append(f'{course_key} missing GDP price {amount_key}')
    expected_methods={'auction','workers','liquidate','public'}
    sectors=market.get('sectors',[])
    methods=market.get('methods',{})
    decisions=market.get('decisions',[])
    sector_keys={entry[0] for entry in sectors if isinstance(entry,(list,tuple)) and entry}
    combos={(item.get('sector'),item.get('method')) for item in decisions}
    expected_combos={(sector,method) for sector in sector_keys for method in expected_methods}
    if len(sector_keys)!=6 or set(methods)!=expected_methods or combos!=expected_combos or len(decisions)!=24:
        errors.append('market catalogue is not exactly six sectors by four one-use methods')
    finite_text=market.get('rules',{}).get('finite','').lower()
    window_text=market.get('rules',{}).get('window','').lower()
    prices_text=market.get('rules',{}).get('prices','').lower()
    if not all(term in finite_text for term in ('six sector lots','settled once','only one lot')):
        errors.append('market rules do not specify six finite one-use sector lots with a single active project')
    if not all(term in window_text for term in ('730-day','once','cannot restart or extend')):
        errors.append('market rules do not specify a one-time 730-day country reform window')
    if not all(term in prices_text for term in ('share of the relevant country', 'current gdp', 'no fixed dollar price')):
        errors.append('market price rules do not fully specify GDP-linked setup and weekly costs')
    for decision in decisions:
        method=decision.get('method')
        if decision.get('closure')!=(1 if method=='liquidate' else 0):
            errors.append(f'only liquidation may remove a civilian factory: {decision.get("id")}')
        if 'gdp_cost' not in decision or 'gdp_income' not in decision:
            errors.append(f'market lot lacks GDP fee/receipt: {decision.get("id")}')

    # Nine common SSR specialisations are inspected individually, never summed into one route.
    normalized_spec={}
    reference_spec=None
    for tag,model in models.items():
        nodes=model.get('nodes',[])
        all_by_id=node_map(model)
        by_id={node['id']:node for node in nodes}
        grouped=defaultdict(list)
        for node in nodes:
            grouped[node['group']].append(node)

        for node in nodes:
            if node.get('phase')=='ssr':
                if node.get('gate') is not None or any('_are_in_power' in item for item in node.get('runtime_contract',[])):
                    errors.append(f'{tag} SSR status node has a party gate: {node["id"]}')
            if node.get('phase')=='party':
                gate=node.get('gate','')
                if not gate.startswith('slot'):
                    errors.append(f'{tag} party node lacks exact slot gate: {node["id"]}')
                else:
                    try: slot=int(gate[4:])
                    except ValueError: slot=-1
                    expected_trigger=party_triggers.get(slot)
                    party_slots={party.get('slot') for party in model.get('profile',{}).get('parties',[])}
                    if slot not in party_slots or not expected_trigger or expected_trigger not in node.get('runtime_contract',[]):
                        errors.append(f'{tag} party node has no matching actual MD party trigger: {node["id"]}')
                    visible=' '.join(node.get('requirements',[]))
                    party=next((p for p in model.get('profile',{}).get('parties',[]) if p.get('slot')==slot),{})
                    if party and party.get('name') and party['name'] not in visible:
                        errors.append(f'{tag} party node does not display its actual party name: {node["id"]}')
            if node.get('phase')=='independent' and not any('recorded actual SSR independence' in item for item in node.get('runtime_contract',[])):
                errors.append(f'{tag} independent node lacks actual sovereignty contract: {node["id"]}')
            if node.get('building'):
                building=node['building']
                if building.get('shared_slots')!=building.get('level') or building.get('level',0)<=0:
                    errors.append(f'{tag} building lacks one shared slot per level: {node["id"]}')
            for key in node.get('modifiers',{}):
                if labels and key not in labels:errors.append(f'{tag} unsupported modifier label {key}: {node["id"]}')
            for field in ('prerequisites','exclusive'):
                for group in node.get(field,[]) if field=='prerequisites' else [node.get(field,[])]:
                    for ref in group:
                        if ref not in all_by_id:errors.append(f'{tag} dangling {field} reference {ref}: {node["id"]}')
            if node.get('anchor') and node['anchor'] not in all_by_id:
                errors.append(f'{tag} dangling anchor {node["anchor"]}: {node["id"]}')
            if node.get('anchor') and node['anchor'] in all_by_id:
                anchor=all_by_id[node['anchor']]
                if anchor.get('group')!=node.get('group') or anchor.get('y',0)>node.get('y',0):
                    errors.append(f'{tag} invalid relative anchor: {node["id"]}')
            for ref in node.get('exclusive',[]):
                other=all_by_id.get(ref,{})
                if node['id'] not in other.get('exclusive',[]):errors.append(f'{tag} asymmetric exclusive link {node["id"]} / {ref}')

        specs=[node for node in nodes if node.get('specialisation')]
        roles={node['specialisation'] for node in specs}
        if roles!=SPEC_ROLES or len(specs)!=len(SPEC_ROLES)*len(SPEC_SUFFIXES):
            errors.append(f'{tag} does not have nine full eleven-focus specialisations')
        spec_groups={}
        legacy_ok=True
        for role in SPEC_ROLES:
            role_nodes=[node for node in specs if node.get('specialisation')==role]
            expected_keys={f'special_{role}_{suffix}' for suffix in SPEC_SUFFIXES}
            if {node['key'] for node in role_nodes}!=expected_keys:
                errors.append(f'{tag} {role} focus structure differs from the eleven-node contract')
            groups={node['group'] for node in role_nodes}
            if len(groups)!=1:
                errors.append(f'{tag} {role} spans multiple groups')
            spec_groups[role]=role_nodes
            navy=role=='navy'
            expected_sea=NAVAL_SEAS.get(tag,'Landlocked')
            for node in role_nodes:
                expected_modifiers={key:expected_legacy(key,value) for key,value in node.get('modifiers',{}).items()}
                if canonical(expected_modifiers)!=canonical(node.get('legacy_modifiers',{})):
                    errors.append(f'{tag} incorrect 20/75 legacy modifier scaling: {node["id"]}');legacy_ok=False
                expected_weekly=round(node.get('weekly_gdp_cost',0)*.5,5)
                if abs(node.get('legacy_weekly_gdp_cost',0)-expected_weekly)>1e-10:
                    errors.append(f'{tag} incorrect half-cost legacy weekly funding: {node["id"]}');legacy_ok=False
                if abs(node.get('legacy_retention',-1)-.20)>1e-10:
                    errors.append(f'{tag} incorrect beneficial legacy retention: {node["id"]}');legacy_ok=False
                original_gear=node.get('equipment_bonuses',[])
                inherited_gear=node.get('legacy_equipment_bonuses',[])
                expected_gear=[dict(target=item.get('target'),modifiers={key:expected_legacy(key,value) for key,value in item.get('modifiers',{}).items()}) for item in original_gear]
                if canonical(expected_gear)!=canonical(inherited_gear):
                    errors.append(f'{tag} incorrect scoped equipment legacy scaling: {node["id"]}');legacy_ok=False
                if navy:
                    if node.get('geography')!='naval_coast' or node.get('sea_context')!=expected_sea:
                        errors.append(f'{tag} navy specialization lacks its correct legal coast context: {node["id"]}')
                    if not any('owned and controlled coast with a legal naval project site' in req for req in node.get('requirements',[])):
                        errors.append(f'{tag} navy specialization lacks visible native coast/site requirement: {node["id"]}')
                elif node.get('geography')=='naval_coast':
                    errors.append(f'{tag} non-naval specialization has naval coast gate: {node["id"]}')
        roots=[next((node for node in specs if node['specialisation']==role and node['key'].endswith('_mandate')),None) for role in sorted(SPEC_ROLES)]
        for root in roots:
            if root is None:continue
            expected={node['id'] for node in roots if node and node['id']!=root['id']}
            if set(root.get('exclusive',[])) != expected:
                errors.append(f'{tag} specialization roots are not a complete exclusive clique')

        # Compare every role/node to UKR after removing country IDs and terminal historical references.
        by_key={node['key']:node for node in specs}
        normalized={}
        for key,node in by_key.items():
            refs=node_reference_keys(node,all_by_id)
            description=historical_core(node,warnings,tag)
            fields=('title','cost','days','modifiers','gdp_cost','weekly_gdp_cost','building','research','army_xp','air_xp','navy_xp',
                    'doctrine','stability','effect_mode','spirit','replace','remove','gate','phase','ownership','specialisation',
                    'equipment_bonuses','legacy_modifiers','legacy_weekly_gdp_cost','legacy_equipment_bonuses','legacy_retention','choice_set',
                    'geography','kind','x','y')
            normalized[key]={field:node.get(field) for field in fields}
            normalized[key].update(refs)
            normalized[key]['description_core']=description
        normalized_spec[tag]=normalized
        parity=True
        if tag=='UKR':reference_spec=normalized
        elif normalized!=reference_spec:
            different=[key for key in set(normalized)|set(reference_spec) if normalized.get(key)!=reference_spec.get(key)]
            errors.append(f'{tag} specialization mechanics/text/geometry differ from UKR: {different[:5]}')
            parity=False

        courses_in_tree=[node for node in nodes if node.get('market_course')]
        course_clique_ok={node.get('market_course') for node in courses_in_tree}==expected_courses and len(courses_in_tree)==3
        if not course_clique_ok:
            errors.append(f'{tag} does not expose exactly three mutually-exclusive market courses')
        if any(node.get('phase')!='independent' for node in courses_in_tree):
            errors.append(f'{tag} reform course is not gated to the independent phase')
        course_ids={node['market_course']:node['id'] for node in courses_in_tree}
        for course,node_id in course_ids.items():
            node=by_id[node_id]
            for other,other_id in course_ids.items():
                if other!=course and other_id not in node.get('exclusive',[]):
                    errors.append(f'{tag} market course clique missing {course} / {other}')
                    course_clique_ok=False

        # Groupwise maxima are not additive. Each group is reported separately and excludes baseline.
        known={spirit['name']:spirit['modifiers'] for spirit in design.get('starting',[])}
        known[model['profile']['regional']['name']]=model['profile']['regional']['modifiers']
        known.update({node['spirit']:node['modifiers'] for node in nodes if node.get('effect_mode')=='add' and node.get('spirit')})
        group_reports={};reachable_ids=set();route_counts={}
        for group_id,group_nodes in grouped.items():
            states,group_by_id=reachable_subsets(group_nodes)
            route_counts[group_id]=len(states)
            reachable_ids.update(set().union(*states))
            maxima=defaultdict(lambda:float('-inf'))
            for done in states:
                values=defaultdict(float)
                for node_id in done:
                    node=group_by_id[node_id]
                    for modifier,amount in delta_for(node,known).items():values[modifier]+=amount
                for modifier in labels:maxima[modifier]=max(maxima[modifier],values[modifier])
            group_reports[group_id]={key:round(value*100,3) for key,value in sorted(maxima.items()) if value}
        for node in nodes:
            if node['id'] not in reachable_ids:errors.append(f'{tag} unreachable focus: {node["id"]}')

        # Layout safety: focus card envelopes and exact coordinate collisions across all nodes.
        coords={}
        all_nodes=nodes+model.get('external',[])+design.get('external',[])
        unique={node['id']:node for node in all_nodes}
        for node in all_nodes:
            grid=(node.get('x'),node.get('y'))
            if grid in coords:errors.append(f'{tag} duplicate focus grid coordinate {grid}: {coords[grid]} / {node["id"]}')
            coords[grid]=node['id']
        for index,left in enumerate(all_nodes):
            ax=left.get('x',0)*96;ay=left.get('y',0)*130
            for right in all_nodes[index+1:]:
                bx=right.get('x',0)*96;by=right.get('y',0)*130
                if ax+5<bx+169 and bx+5<ax+169 and ay-32<by+90 and by-32<ay+90:
                    errors.append(f'{tag} focus card collision {left["id"]} / {right["id"]}')
            panel=design.get('layout',{}).get('continuous_focus_position',{})
            if ax+5<panel.get('x',0)+panel.get('width',0) and panel.get('x',0)<ax+169 and ay-32<panel.get('y',0)+panel.get('height',0) and panel.get('y',0)<ay+90:
                errors.append(f'{tag} continuous-focus panel collision {left["id"]}')
        shortcuts=design.get('layout',{}).get('shortcuts',[])
        for shortcut in shortcuts:
            if shortcut not in unique:errors.append(f'{tag} dangling tree shortcut {shortcut}')

        ssr_count=sum(node.get('phase')=='ssr' for node in nodes)
        reports[tag]={
            'new_focuses':len(nodes),'ssr_status_only':ssr_count,'reachable_focuses':len(reachable_ids),
            'party_programmes':len(model.get('profile',{}).get('parties',[])),
            'route_states_by_group':route_counts,
            'group_modifier_maxima_percent':group_reports,
            'specialisation_modifier_maxima_percent':{role:group_reports.get(next(iter({n['group'] for n in spec_groups[role]}),''),{}) for role in sorted(SPEC_ROLES)},
            'checks':{
                'nine_complete_specialisations':len(specs)==99 and roles==SPEC_ROLES,
                'specialisation_mechanics_and_gear_match_across_all_countries':parity,
                'legacy_scaling_20_percent_benefits_75_percent_penalties_50_percent_weekly':legacy_ok,
                'specialisation_choices_are_mutually_exclusive':all(set(root.get('exclusive',[]))=={candidate['id'] for candidate in roots if candidate and candidate['id']!=root['id']} for root in roots if root),
                'three_course_market_clique':course_clique_ok,
                'naval_geography_checks':all(n.get('geography')=='naval_coast' for n in spec_groups.get('navy',[])),
                'party_slot_gates':all(n.get('gate','').startswith('slot') for n in nodes if n.get('phase')=='party'),
                'ssr_status_only':all(n.get('gate') is None for n in nodes if n.get('phase')=='ssr'),
            }
        }

    # Record explicit audit scope and never present mutually exclusive role maxima as one attainable stack.
    report={
        'project':'IMPERIA COLD WAR','revision':design.get('revision'),'design_sha256':hashlib.sha256(design_bytes).hexdigest(),
        'status':'Static design-data audit only. Loaded-game, save, multiplayer and runtime binding checks are untested.',
        'scope':'Modifier maxima are computed separately for each focus group and each one of the nine specialization branches. Group maxima are not additive. The nine mutually exclusive specialization branches are never summed into a country total. Baseline spirits, timed mechanics, state-bound effects, equipment stacking and runtime modifiers are excluded from these group maxima.',
        'errors':errors,'warnings':sorted(warnings),
        'market_audit':{
            'course_count':len(courses),'course_keys':sorted(courses),'duration_days':{key:{field:course.get(field,{}).get('days') for field in ('window','fiscal')} for key,course in courses.items()},
            'sector_count':len(sector_keys),'method_keys':sorted(methods),'lot_method_decisions':len(decisions),
            'closure_method':'liquidate only','market_lots_have_GDP_fees_and_receipts':all('gdp_cost' in item and 'gdp_income' in item for item in decisions),
            'course_clique_all_models':all(report['checks']['three_course_market_clique'] for report in reports.values()),
            'all_script_treasury_costs_use_GDP_fields':not any(any(k in item for k in ('cash','fixed_cash_cost','fixed_money_cost','usd_cost')) for _,item in walk(design) if isinstance(item,dict)),
            'finite_one_use_rules_recorded':all(term in finite_text for term in ('six sector lots','settled once','only one lot')),
            'once_per_country_and_transactionality':'Design contract recorded; runtime enforcement not tested.',
        },
        'runtime_checks':'Not tested: native focus loading, decision execution, party activation, state ownership/control and capacity, building slot ordering, coast project legality, timed suspension/restoration, independence transition, and save/load persistence.',
        'models':reports,
    }
    return report


def main():
    design_bytes=DESIGN_PATH.read_bytes()
    design=json.loads(design_bytes.decode('utf-8-sig'))
    report=audit_design(design,design_bytes)
    AUDIT_PATH.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    summary={tag:{'new_focuses':model['new_focuses'],'ssr_status_only':model['ssr_status_only'],'groups':len(model['group_modifier_maxima_percent'])}
             for tag,model in report['models'].items()}
    print(json.dumps({'errors':report['errors'],'warnings':report['warnings'],'models':len(report['models']),'summary':summary,'design_sha256':report['design_sha256']}))
    if report['errors']:
        raise SystemExit(1)


if __name__=='__main__':
    main()
