# IMPERIA CW — Cold War: egypt 1970 — test quality merges 20261020.
"""Regression checks for the approved SOV/EGY focus-quality patch.

Checks real source AST, graph equivalence through removed receipt nodes, and
unchanged rewards/party conditions. Does not simulate HOI4 rendering or runtime.
"""
from pathlib import Path
import ast
import itertools
import json
import runpy

ROOT = Path(__file__).resolve().parents[2]
API = runpy.run_path(str(ROOT / 'tools/egypt_1970/apply_quality_merges_20261020.py'))
parse, first, values, walk = (API[k] for k in ('parse', 'first', 'values', 'walk'))
checks = 0
# A separately approved concurrent native-modifier migration touched these five
# rewards after the merge receipt was recorded. Permit only that exact field
# and tooltip substitution on these IDs; all amounts/other rewards remain exact.
NATIVE_DRIFT_MIGRATION = {
    'COLDWAR_EGY_tag_a_socialism_of_our_own',
    'COLDWAR_EGY_cp_the_mukhabarat_state',
    'COLDWAR_EGY_grd_the_principlists',
    'COLDWAR_EGY_ndp_the_emergency_state',
    'COLDWAR_EGY_rcc_revolutionary_purity',
}


def check(ok, message):
    global checks
    checks += 1
    assert ok, message


def focuses(path):
    raw = path.read_text(encoding='utf-8')
    return {first(v, 'id'): v for k, _, v in walk(parse(raw))
            if k == 'focus' and isinstance(v, list)}


receipt = json.loads((ROOT / 'docs/tree_quality_audit_20261020/sov_egy_implementation.json').read_text(encoding='utf-8'))
egy = focuses(ROOT / 'common/national_focus/COLDWAR_EGY_1970_focus.txt')
removed = set(receipt['removed'])
check(len(egy) == receipt['original_focus_count'] - len(removed), 'Egypt focus count')
check(not removed & set(egy), 'Removed debates remain')
for fid, node in egy.items():
    for group in values(node, 'prerequisite'):
        for ref in values(group, 'focus'):
            check(ref in egy, f'Broken prerequisite {fid}: {ref}')
    for ref in values(first(node, 'mutually_exclusive', []), 'focus'):
        check(ref in egy, f'Broken exclusivity {fid}: {ref}')
    anchor = first(node, 'relative_position_id')
    check(not anchor or anchor in egy, f'Broken anchor {fid}: {anchor}')
for change in receipt['modified']:
    fid = change['id']; node = egy[fid]
    expected_reward=json.dumps(change['reward_before'])
    if fid in NATIVE_DRIFT_MIGRATION:
        check(expected_reward.count('mdcw_cw_ideological_defence') == 2,
              'Migration fixture must contain exactly the variable and tooltip '+fid)
        expected_reward=expected_reward.replace('mdcw_cw_ideological_defence','drift_defence_factor')
    check(json.dumps(first(node, 'completion_reward', [])) == expected_reward,
          f'Reward changed: {fid}')
    av = first(node, 'available', [])
    for rule in change['available_before']:
        check(json.dumps(rule) in [json.dumps(x) for x in av], f'Lost availability {fid}: {rule}')
    for rule in change.get('inherited_available', []):
        check(any(json.dumps(rule) == json.dumps(r) for _, _, b in av if isinstance(b, list)
                  for r in b), f'Lost inherited availability {fid}: {rule}')
    check([values(g, 'focus') for g in values(node, 'prerequisite')] == change['new_pre'],
          f'Changed AND/OR replacement {fid}')
    check(float(first(node, 'cost')) == change['new_cost'], f'Cost {fid}')
    check(int(first(node, 'y')) == change['new_y'], f'Y {fid}')
    # Exhaustive truth table on the immediate non-debate prerequisites proves
    # AND/OR expansion instead of trusting a second copy of the rewrite output.
    removed_pre=receipt['removed_prerequisite_groups']
    def leaves(groups):
        return {leaf for group in groups for ref in group for leaf in
                (leaves(removed_pre[ref]) if ref in removed_pre else {ref})}
    refs=sorted(leaves(change['old_pre']))
    def evaluate(groups, state):
        return all(any(evaluate(removed_pre[ref],state) if ref in removed_pre else state[ref]
                       for ref in group) for group in groups)
    for combination in itertools.product((False,True),repeat=len(refs)):
        state=dict(zip(refs,combination))
        check(evaluate(change['old_pre'],state)==evaluate(change['new_pre'],state),
              f'Prerequisite Boolean mismatch {fid}: {state}')
for key in ['tp_a_strong_presidency','tp_return_power_to_the_assembly']:
    node=egy['COLDWAR_EGY_'+key]
    check(float(first(node,'cost'))*7 == 49, 'Explicit49-day constitution choice')
    check(values(first(node,'prerequisite'),'focus') == ['COLDWAR_EGY_tp_the_governorates_reform'],
          'Constitution choice not directly reachable')
for fid,old_y in receipt['anchor_y_before'].items():
    check(not first(egy[fid],'relative_position_id'),'Section anchor gained relative scope '+fid)
    check(int(first(egy[fid],'y'))==old_y,'Absolute section anchor moved '+fid)
design=json.loads((ROOT/'Claude outputs/COLDWAR_EGY_generator/egy_tree.json').read_text(encoding='utf-8'))
by={f['id']:f for f in design['foci']}
for f in design['foci']:
    check(f['id'].replace('EGY_1970_','COLDWAR_EGY_') not in removed, 'Canonical removed node')
    for group in f['pre']:
        check(all(ref in by for ref in group), 'Canonical dangling reference')
for key in ['tp_a_strong_presidency','tp_return_power_to_the_assembly']:
    check(by['EGY_1970_'+key]['cost']==7, 'Canonical cost')
    check(by['EGY_1970_'+key]['pre']==[['EGY_1970_tp_the_governorates_reform']], 'Canonical constitutional prerequisite')
sov=focuses(ROOT/'common/national_focus/COLDWAR_SOV_1970_focus.txt')
for fid, value in [('COLDWAR_SOV_rd_the_directors_banks', '-0.25'),('COLDWAR_SOV_open_the_gates','-0.1')]:
    vals=[v for k, _, v in walk(first(sov[fid],'completion_reward'))
          if k=='COLDWAR_SOV_gosplan_interest_rate_multiplier_modifier']
    check(vals==[value], 'Soviet interest value '+fid)
loc=(ROOT/'localisation/english/COLDWAR_SOV_1970_l_english.yml').read_text(encoding='utf-8-sig')
line=next(l for l in loc.splitlines() if l.startswith(' COLDWAR_SOV_mod_interest_rate_multiplier_modifier_tt:'))
check('$RIGHT|-=2$ percentage points' in line and '%1' not in line, 'Soviet rate-point tooltip')
formatter=runpy.run_path(str(ROOT/'Claude outputs/COLDWAR_SOV_generator/cw_common.py'))
formatter['mod_tt_key']('interest_rate_multiplier_modifier')
check('$RIGHT|-=2$ percentage points' in formatter['LOC']['COLDWAR_SOV_mod_interest_rate_multiplier_modifier_tt'],
      'Canonical Soviet formatter differs from live tooltip')
dsl_path=ROOT/'Claude outputs/COLDWAR_SOV_design/sov_dsl.py'
dsl_ast=ast.parse(dsl_path.read_text(encoding='utf-8'))
fmt_function=next(n for n in dsl_ast.body if isinstance(n,ast.FunctionDef) and n.name=='fmt_mod')
fmt_ns={'MODL':{}}
exec(compile(ast.Module(body=[fmt_function],type_ignores=[]),str(dsl_path),'exec'),fmt_ns)
for amount in [-0.25,-0.10]:
    check(fmt_ns['fmt_mod']('interest_rate_multiplier_modifier',amount)==f'Interest rate {amount:+g} percentage points',
          'Design preview incorrectly converts interest units')
for path in [ROOT/'common/national_focus/COLDWAR_EGY_1970_focus.txt',ROOT/'common/national_focus/COLDWAR_SOV_1970_focus.txt']:
    check(not path.read_bytes().startswith(b'\xef\xbb\xbf'),'BOM in script')
check((ROOT/'localisation/english/COLDWAR_SOV_1970_l_english.yml').read_bytes().startswith(b'\xef\xbb\xbf'),'Localisation missing BOM')
# Trace the real additive reader; prevents regression to percentage multiplication.
money=(ROOT/'common/scripted_effects/00_money_system.txt').read_text(encoding='utf-8')
check('add = modifier@interest_rate_multiplier_modifier' in money,'Interest reader changed; re-audit units')
print(f'PASS: {checks} focused AST/graph/encoding checks. No engine execution claimed.')
