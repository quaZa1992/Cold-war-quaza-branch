# IMPERIA CW — Cold War: egypt 1970 — apply quality merges 20261020.
"""Apply the approved, bounded Soviet/Egypt audit corrections without rebuilding trees.

Preserves other live rewards, party gates, unrelated generator output and save IDs
of surviving focuses. Writes an audit receipt used by the focused regression check.
"""
from pathlib import Path
import ast
import itertools
import json
import re

ROOT = Path(__file__).resolve().parents[2]
NS = {'re': re}
parser_path = ROOT / 'tools/israel_1970/validate_content.py'
tree = ast.parse(parser_path.read_text(encoding='utf-8'))
funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)
         and n.name in {'tokens', 'parse', 'first', 'values', 'walk'}]
exec(compile(ast.Module(body=funcs, type_ignores=[]), str(parser_path), 'exec'), NS)
parse, first, values, walk = (NS[k] for k in ('parse', 'first', 'values', 'walk'))


def save(path, text, bom=False):
    path.write_text(text, encoding='utf-8-sig' if bom else 'utf-8', newline='\n')


def focus_blocks(raw):
    blocks = {}
    for match in re.finditer(r'(?m)^\tfocus = \{\s*\n', raw):
        # Focus closing braces are at precisely one tab in emitted native trees.
        end = raw.index('\n\t}', match.end()) + len('\n\t}')
        block = raw[match.start():end]
        fid = re.search(r'\bid = ([\w]+)', block)[1]
        blocks[fid] = (match.start(), end, block)
    return blocks


def main():
    receipt = ROOT / 'docs/tree_quality_audit_20261020/sov_egy_implementation.json'
    if receipt.exists():
        raise SystemExit('Already applied; run test_quality_merges_20261020.py instead.')
    egy_dir = ROOT / 'Claude outputs/COLDWAR_EGY_generator'
    design_path = egy_dir / 'egy_tree.json'
    design = json.loads(design_path.read_text(encoding='utf-8'))
    tree_path = ROOT / 'common/national_focus/COLDWAR_EGY_1970_focus.txt'
    raw = tree_path.read_text(encoding='utf-8')
    blocks = focus_blocks(raw)
    live = {first(v, 'id'): v for k, _, v in walk(parse(raw))
            if k == 'focus' and isinstance(v, list)}
    by_id = {f['id'].replace('EGY_1970_', 'COLDWAR_EGY_'): f for f in design['foci']}
    candidates = []
    for fid, node in live.items():
        reward = first(node, 'completion_reward', [])
        if reward and all(k in {'log', 'add_political_power'} for k, _, _ in reward):
            candidates.append(fid)
    # Keep distinct shared historical/constitutional entries. The repeated party
    # question nodes have no institutional effect or external scripted consumer.
    retained = [fid for fid in candidates if by_id[fid]['sec'] in
                {'trunk', 'war', 'pw', 'eco', 'nile'}]
    removed = set(candidates) - set(retained)
    assert len(candidates) == 52 and len(removed) == 46
    source_id = lambda fid: fid.replace('COLDWAR_EGY_', 'EGY_1970_')
    removed_source = {source_id(fid) for fid in removed}
    # Repeated question nodes must not carry an extra condition that would be
    # lost when the child is attached directly to the question's predecessors.
    for fid in removed:
        f = by_id[fid]
        assert f['cost'] == 3 and not f['mx'] and not f['bypass']
        child_nodes = [n for n in live.values() if any(
            fid in values(g, 'focus') for g in values(n, 'prerequisite'))]
        assert child_nodes
        parent_av = first(live[fid], 'available', [])
        missing = [rule for child in child_nodes for rule in parent_av
                   if rule not in first(child, 'available', [])]
        assert all(rule[0] == 'date' and not isinstance(rule[2], list) for rule in missing), fid
    # The source universe was checked for runtime references outside this tree;
    # recheck the relevant generated EGY systems before changing prerequisite IDs.
    id_pattern = re.compile(r'\b(' + '|'.join(sorted(removed)) + r')\b')
    for folder in ('common/scripted_effects', 'common/scripted_triggers', 'events',
                   'common/decisions', 'common/on_actions'):
        for path in (ROOT / folder).glob('*EGY*.txt'):
            assert not id_pattern.search(path.read_text(encoding='utf-8-sig')), str(path)

    def expand(groups, lookup, deleted, key):
        result = []
        for group in groups:
            terms = [[]]
            for fid in group:
                replacements = (expand(lookup[fid][key], lookup, deleted, key)
                                if fid in deleted else [[fid]])
                terms = [list(dict.fromkeys(a + b)) for a, b in itertools.product(terms, replacements)]
            for term in terms:
                if term not in result:
                    result.append(term)
        return result

    # CNF expansion preserves AND between blocks and OR inside each block.
    live_groups = {fid: {'pre': [values(g, 'focus') for g in values(n, 'prerequisite')]}
                   for fid, n in live.items()}
    source_lookup = {f['id']: f for f in design['foci']}
    changes = []
    removed_rows = {}
    for sec in {f['sec'] for f in by_id.values()}:
        gone = {int(first(live[fid], 'y')) for fid in removed if by_id[fid]['sec'] == sec
                and first(live[fid], 'relative_position_id')}
        occupied = {int(first(live[fid], 'y')) for fid in live if fid in by_id
                    and by_id[fid]['sec'] == sec and fid not in removed
                    and first(live[fid], 'relative_position_id')}
        removed_rows[sec] = gone - occupied
    modified = []
    for fid, (start, end, block) in blocks.items():
        if fid in removed:
            changes.append((start, end, ''))
            continue
        if fid not in by_id:
            continue
        f = by_id[fid]
        old_pre = live_groups[fid]['pre']
        new_pre = expand(old_pre, live_groups, removed, 'pre')
        old_cost = float(first(live[fid], 'cost', 10))
        new_cost = max(old_cost, 7) if any(set(g) & removed for g in old_pre) else old_cost
        new = block
        inherited = []
        for group in old_pre:
            for gone in set(group) & removed:
                for rule in first(live[gone], 'available', []):
                    if rule not in first(live[fid], 'available', []) and rule not in inherited:
                        inherited.append(rule)
        if inherited:
            guards = ' '.join(' '.join(rule) for rule in inherited)
            # Preserve the pre-existing succession date while hiding its raw routing check.
            addition = 'hidden_trigger = { '+guards+' }'
            new = new.replace('\t\tavailable = {\n', '\t\tavailable = {\n\t\t\t'+addition+'\n', 1)
            f['av_raw'] = (f.get('av_raw', '')+'\n'+addition).strip()
        if old_pre != new_pre:
            new = re.sub(r'(?m)^\t\tprerequisite = \{[^\n]+\}\n', '', new)
            reqs = ''.join('\t\tprerequisite = { ' + ' '.join('focus = '+p for p in g) + ' }\n'
                           for g in new_pre)
            new = re.sub(r'(?m)^(\t\tcost = [^\n]+\n)', lambda m:m[1]+'\n'+reqs, new, count=1)
        if new_cost != old_cost:
            new = re.sub(r'(?m)^\t\tcost = [^\n]+', '\t\tcost = '+str(int(new_cost)), new, count=1)
        old_y = int(first(live[fid], 'y'))
        new_y = (old_y - sum(row < old_y for row in removed_rows[f['sec']])
                 if first(live[fid], 'relative_position_id') else old_y)
        if old_y != new_y:
            new = re.sub(r'(?m)^\t\ty = -?\d+', '\t\ty = '+str(new_y), new, count=1)
        if new != block:
            changes.append((start, end, new))
            modified.append(dict(id=fid, old_pre=old_pre, new_pre=new_pre,
                                 old_cost=old_cost, new_cost=new_cost,
                                 old_y=old_y, new_y=new_y,
                                 inherited_available=inherited,
                                 reward_before=first(live[fid], 'completion_reward', []),
                                 available_before=first(live[fid], 'available', [])))
        f['pre'] = expand(f['pre'], source_lookup, removed_source, 'pre')
        f['cost'] = int(new_cost) if new_cost.is_integer() else new_cost
    for start, end, replacement in sorted(changes, reverse=True):
        raw = raw[:start] + replacement + raw[end:]
    design['foci'] = [f for f in design['foci'] if f['id'] not in removed_source]
    save(tree_path, raw)
    save(design_path, json.dumps(design, ensure_ascii=False, indent=1)+'\n')

    sov = ROOT / 'Claude outputs/COLDWAR_SOV_generator'
    design_sov = ROOT / 'Claude outputs/COLDWAR_SOV_design'
    p = design_sov / 'd_parties.py'
    t = p.read_text(encoding='utf-8')
    old = 'dm("gp", {"interest_rate_multiplier_modifier": -0.05, "office_park_income_tax_modifier": 0.05})'
    assert t.count(old) == 1
    save(p, t.replace(old, old.replace('-0.05', '-0.25', 1)))
    p = sov / 'overrides/g6_economy_kgb.json'
    data = json.loads(p.read_text(encoding='utf-8'))
    data['foci']['COLDWAR_SOV_open_the_gates']['set'][0]['e']['mods']['interest_rate_multiplier_modifier'] = -0.10
    save(p, json.dumps(data, ensure_ascii=False, indent=1)+'\n')
    p = design_sov / 'sov_tree_full.json'
    data = json.loads(p.read_text(encoding='utf-8'))
    for f in data['foci']:
        if f['id'] == 'COLDWAR_SOV_rd_the_directors_banks':
            f['eff'][0]['mods']['interest_rate_multiplier_modifier'] = -0.25
            f['eff'][0]['t'] = 'Gosplan: interest rate -0.25 percentage points; office income +5%.'
    save(p, json.dumps(data, ensure_ascii=False, indent=1)+'\n')
    p = design_sov / 'sov_dsl.py'
    t = p.read_text(encoding='utf-8')
    old = '    lab = MODL.get(k) or k\n'
    assert t.count(old) == 1
    t = t.replace(old, '    if k == "interest_rate_multiplier_modifier":\n'
                  '        return f"Interest rate {v:+g} percentage points"\n'+old)
    save(p,t)
    p = sov / 'cw_common.py'
    t = p.read_text(encoding='utf-8')
    old = '        if mod in COUNT_KEYS:\n'
    assert t.count(old) == 1
    t = t.replace(old, '        if mod == "interest_rate_multiplier_modifier":\n'
                  '            LOC[k] = f"{label}: $RIGHT|-=2$ percentage points"\n'
                  '            return k\n' + old)
    save(p, t)
    p = ROOT / 'common/national_focus/COLDWAR_SOV_1970_focus.txt'
    t = p.read_text(encoding='utf-8')
    for fid, oldv, newv in [('COLDWAR_SOV_rd_the_directors_banks','-0.05','-0.25'),
                            ('COLDWAR_SOV_open_the_gates','-0.06','-0.1')]:
        start,end,b = focus_blocks(t)[fid]
        old = 'COLDWAR_SOV_gosplan_interest_rate_multiplier_modifier = '+oldv+' tooltip'
        assert b.count(old) == 1
        b = b.replace(old, old.replace(oldv,newv))
        t = t[:start] + b + t[end:]
    save(p,t)
    p = ROOT / 'localisation/english/COLDWAR_SOV_1970_l_english.yml'
    t = p.read_text(encoding='utf-8-sig')
    t,n = re.subn(r'(?m)^( COLDWAR_SOV_mod_interest_rate_multiplier_modifier_tt:\d* )".*"$',
                 r'\1"Interest Rates: $RIGHT|-=2$ percentage points"',t)
    assert n == 1
    save(p,t,bom=True)
    receipt.parent.mkdir(parents=True,exist_ok=True)
    receipt.write_text(json.dumps(dict(removed=sorted(removed),retained_shared_questions=retained,
                                       removed_prerequisite_groups={fid:live_groups[fid]['pre'] for fid in removed},
                                       modified=modified,original_focus_count=len(live),
                                       anchor_y_before={fid:int(first(node,'y')) for fid,node in live.items()
                                                        if not first(node,'relative_position_id')},
                                       reason='Merge redundant party debate receipts into substantive choice focuses; preserve meaningful shared historical entries.'),
                                  ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'egypt_removed':len(removed),'egypt_survivors':len(live)-len(removed),
                      'egypt_modified':len(modified),'soviet_values':[-.25,-.10]}))


if __name__ == '__main__':
    main()
