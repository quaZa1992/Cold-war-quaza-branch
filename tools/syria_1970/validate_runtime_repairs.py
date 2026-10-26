# IMPERIA CW — Cold War: Syria 1970 content imported from quaZa.
"""Independent emitted-source regressions for the five October runtime reports."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from validate_content import parse, first, vals, walk

ROOT = Path(__file__).resolve().parents[2]
EVENT_NAMESPACES = ('COLDWAR_SYR_POL.', 'COLDWAR_SYR_WAR.', 'COLDWAR_SYR_FOREIGN.')
MATERIAL = {'add_stability', 'add_war_support', 'add_political_power', 'add_ideas',
            'remove_ideas', 'add_timed_idea', 'modify_treasury_effect', 'modify_debt_effect'}


def audit(root=ROOT):
    root = Path(root)
    errors, checks, hashes, loc = [], Counter(), {}, {}

    def check(condition, message):
        if not condition:
            errors.append(message)

    def read(relative):
        path = root / relative
        raw = path.read_bytes()
        hashes[relative] = hashlib.sha256(raw).hexdigest()
        return raw.decode('utf-8-sig')

    for path in (root / 'localisation/english').glob('COLDWAR_SYR*.yml'):
        for key, encoded in re.findall(r'^\s+(\S+):\d+\s+(".*")\s*$', read(path.relative_to(root).as_posix()), re.M):
            check(key not in loc, 'Duplicate English key: ' + key)
            loc[key] = json.loads(encoded)
    scripts = {}
    for directory in ('common/national_focus', 'common/decisions', 'common/scripted_effects', 'common/scripted_triggers', 'events'):
        for path in (root / directory).glob('COLDWAR_SYR*.txt'):
            relative = path.relative_to(root).as_posix()
            text = read(relative)
            check(not re.search(r'\b(?:_bare|_list)\s*=', text), 'Serialized parser sentinel: ' + relative)
            scripts[relative] = parse(text)
    references = set()
    for ast in scripts.values():
        for key, _, body in walk(ast):
            if key in ('custom_trigger_tooltip', 'custom_override_tooltip') and isinstance(body, list):
                tip = first(body, 'tooltip')
                if isinstance(tip, str) and tip.startswith('COLDWAR_SYR_'):
                    references.add((tip, first(body, 'not_tooltip', tip + '_NOT')))
    for positive, negative in sorted(references):
        check(bool(loc.get(positive)), 'Missing positive requirement: ' + positive)
        check(bool(loc.get(negative)), 'Missing negative requirement: ' + str(negative))
        inverse = loc.get(negative, '')
        check('already answered' not in inverse, 'Absent pending offer incorrectly implies a response: ' + negative)
        check('not been funded and remains valid' not in inverse,
              'Partial negation of funding conjunction: ' + negative)
        check('not been reviewed and their decisions implemented' not in inverse,
              'Partial negation of citizenship conjunction: ' + negative)
        check('before the civil-project proposal cannot be sent' not in inverse,
              'Incorrect donor-selection inverse: ' + negative)
        checks['positive_and_negative_requirement_pairs'] += 1
    pictured = loc.get('COLDWAR_SYR_requirement_088259282155e6a3_NOT', '')
    check('not yet accepted a command settlement' in pictured, 'Pictured command-settlement inverse missing')

    manifest = json.loads(read('tools/syria_1970/manifest.json'))
    original = {n['id']: n for n in json.loads(read('tools/syria_1970/design_source.json'))['nodes']}
    policy = json.loads(read('tools/syria_1970/runtime_policy.json'))
    amendments = {**policy['entry_rewards'], **json.loads(read('tools/syria_1970/additional_entry_rewards.json'))}
    check(len(amendments) == 29, 'Expected 29 reviewed entry/unlock reward bundles')
    focus_ast = scripts['common/national_focus/COLDWAR_SYR_1970_focus.txt']
    focuses = {first(f, 'id'): f for f in vals(first(focus_ast, 'focus_tree'), 'focus')}
    helpers = {k: body for k, _, body in scripts['common/scripted_effects/COLDWAR_SYR_focus_rewards.txt']}
    check(len(focuses) == 420, 'Expected 420 focuses')

    def treasury_gate(body):
        return any(k == 'check_variable' and isinstance(v, list)
                   and (first(v, 'var') == 'treasury' or any(ck == 'treasury' for ck, _, _ in walk(v)))
                   for k, _, v in walk(body))

    for node in manifest['nodes']:
        ident = node['id']
        focus, helper = focuses[ident], helpers[ident + '_implement']
        check(not treasury_gate(first(focus, 'available', [])), 'Focus cash gate: ' + ident)
        check(not treasury_gate(helper), 'Focus payout cash gate: ' + ident)
        guard = first(first(first(helper, 'if', []), 'limit', []), 'NOT', [])
        check(first(guard, 'has_country_flag') == ident + '_implemented', 'Missing once-only guard: ' + ident)
        charges = sum(k == 'modify_treasury_effect' for k, _, _ in walk(helper))
        check(charges == bool(node['treasury_cost_bn']), 'Incorrect treasury charge count: ' + ident)
        costs = [first(v, 'treasury_change') for k, _, v in walk(helper)
                 if k == 'set_temp_variable' and isinstance(v, list) and first(v, 'treasury_change') is not None]
        check(not node['treasury_cost_bn'] or costs == [str(-node['treasury_cost_bn']).removesuffix('.0')]
              or len(costs) == 1 and float(costs[0]) == -node['treasury_cost_bn'], 'Wrong focus expenditure: ' + ident)
        checks['paid_focuses_with_one_charge'] += bool(node['treasury_cost_bn'])
        for field in ('anchor', 'offset', 'prerequisites', 'mutually_exclusive'):
            check(node.get(field) == original[ident].get(field), 'Approved geometry/links changed: ' + ident + ' ' + field)
        check([int(first(focus, 'x')), int(first(focus, 'y'))] == original[ident]['offset']
              and first(focus, 'relative_position_id') == original[ident]['anchor'], 'Emitted focus position changed: ' + ident)
        check([vals(row, 'focus') for row in vals(focus, 'prerequisite')] == original[ident]['prerequisites'],
              'Emitted prerequisite groups changed: ' + ident)
        if ident in amendments:
            check(node['modifiers'] == amendments[ident]['modifiers'], 'Reward bundle mismatch: ' + ident)
            check('_policy_choices_tt' not in node['preview_reward_code'], 'Stale branch-opening text: ' + ident)
            for modifier, amount in amendments[ident]['modifiers'].items():
                variable = node['owner'] + '_' + modifier
                actual = [v for k, _, v in walk(helper) if k == 'add_to_variable' and isinstance(v, list)
                          and first(v, variable) is not None]
                preview = [v for k, _, v in walk(first(first(focus, 'completion_reward', []), 'effect_tooltip', []))
                           if k == 'add_to_variable' and isinstance(v, list) and first(v, variable) is not None]
                check(len(actual) == len(preview) == 1 and float(first(actual[0], variable)) == amount
                      and float(first(preview[0], variable)) == amount, 'Reward preview/payout mismatch: ' + ident + ' ' + modifier)
            checks['entry_reward_bundles'] += 1
        checks['focuses_without_cash_gate'] += 1
    check(checks['paid_focuses_with_one_charge'] == 332, 'Paid-focus coverage changed unexpectedly')
    deferred = scripts['common/decisions/COLDWAR_SYR_deferred_projects.txt']
    for _, _, category in deferred:
        for ident, _, body in category:
            if not isinstance(body, list):
                continue
            check(not treasury_gate(first(body, 'available', [])), 'Resumption cash gate: ' + ident)
            checks['resumptions_without_cash_gate'] += 1
    check(checks['resumptions_without_cash_gate'] == 420, 'Expected 420 resumption decisions')
    check(policy.get('decision_borrowing_allowed'), 'Approved decision-borrowing policy missing')
    for relative, ast in scripts.items():
        if not relative.startswith('common/decisions/'):
            continue
        for _, _, category in ast:
            for ident, _, body in category:
                if not isinstance(body, list) or ident.endswith('_resume'):
                    continue
                for field in ('available', 'complete_effect', 'remove_effect'):
                    check(not treasury_gate(first(body, field, [])), 'Decision cash gate: ' + ident + ' ' + field)
                checks['gameplay_decisions_without_cash_gate'] += 1
    check(checks['gameplay_decisions_without_cash_gate'] == 69, 'Expected all 69 gameplay decisions')
    politics_events = scripts['events/COLDWAR_SYR_politics_events.txt']
    tenure = next(event for event in vals(politics_events, 'country_event') if first(event, 'id') == 'COLDWAR_SYR_POL.5')
    tenure_option = next(option for option in vals(tenure, 'option') if first(option, 'name') == 'COLDWAR_SYR_POL.5.option_a')
    check(not treasury_gate(tenure_option), 'Syrian tenure-review payment still requires cash')
    training = first(scripts['common/scripted_triggers/COLDWAR_SYR_foreign_triggers.txt'], 'COLDWAR_SYR_training_can_request')
    check(isinstance(training, list) and not treasury_gate(training), 'Syrian training request still requires cash')
    goals = [body for k, _, body in walk(scripts['common/scripted_effects/COLDWAR_SYR_foreign_effects.txt'])
             if k == 'create_wargoal' and isinstance(body, list) and first(body, 'type') == 'take_state_focus']
    check(len(goals) == 1 and first(goals[0], 'generator') == [('_bare', '=', '587')],
          'Golan wargoal must retain native generator = { 587 }')

    def execution(body):
        result = []
        for k, op, v in body:
            if k in ('effect_tooltip', 'custom_effect_tooltip', 'trigger', 'name', 'ai_chance'):
                continue
            result.append((k, op, execution(v) if isinstance(v, list) and k != 'limit' else v))
        return result

    def material(body, scope=()):
        found = Counter()
        for k, op, v in body:
            if k == 'limit':
                continue
            if k in MATERIAL or (k in ('set_temp_variable', 'multiply_temp_variable') and isinstance(v, list)
                                 and v and v[0][0] in ('treasury_change', 'debt_change')):
                found[json.dumps((scope, k, op, v), separators=(',', ':'))] += 1
            elif isinstance(v, list):
                scoped = k.startswith(('var:', 'event_target:')) or bool(re.fullmatch(r'(?:[A-Z]{3}|ROOT|FROM|PREV|THIS)(?:\.[A-Z]+)*', k))
                found.update(material(v, scope + (k,) if scoped else scope))
        return found

    for relative, ast in scripts.items():
        if not relative.startswith('events/'):
            continue
        for event in vals(ast, 'country_event'):
            eid = first(event, 'id')
            if not eid.startswith(EVENT_NAMESPACES):
                continue
            signatures = set()
            for option in vals(event, 'option'):
                name = first(option, 'name')
                check(name != first(event, 'desc') and name != first(event, 'title'), 'Option/description collision: ' + name)
                check('.option_' in name and bool(loc.get(name)), 'Missing safe option label: ' + str(name))
                direct = vals(option, 'custom_effect_tooltip')
                outcome = name + '_outcome_tt'
                check(outcome in direct and bool(loc.get(outcome)), 'Missing direct choice outcome: ' + name)
                actual = execution(option)
                check(not any(k in ('kill_country_leader', 'retire_country_leader', 'create_country_leader')
                              for k, _, _ in walk(first(option, 'effect_tooltip', []))), 'Internal leader operation exposed: ' + name)
                if actual:
                    signature = json.dumps(actual, separators=(',', ':'))
                    check(signature not in signatures, 'Identical executed options: ' + eid)
                    signatures.add(signature)
                expected = material(actual)
                if expected:
                    previews = vals(option, 'effect_tooltip')
                    check(len(previews) == 1, 'Material choice needs unconditional native preview: ' + name)
                    check(material(previews[0] if previews else []) == expected, 'Choice material preview differs: ' + name)
                    checks['material_choice_previews'] += 1
                checks['event_options_with_outcomes'] += 1
            checks['new_events_reviewed'] += 1
    check(checks['new_events_reviewed'] == 66, 'Expected all 66 new events')
    politics = scripts['common/scripted_effects/COLDWAR_SYR_politics_effects.txt']
    check(not any(k == 'kill_country_leader' for k, _, _ in walk(politics)), 'Internal political helper still kills leaders')
    return {'ok': not errors, 'checks': dict(checks), 'errors': errors, 'source_sha256': hashes,
            'engine_tested_after_changes': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', default='tools/syria_1970/runtime_repairs_validation.json')
    args = parser.parse_args()
    result = audit()
    (ROOT / args.report).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'source_sha256'}, indent=2))
    raise SystemExit(0 if result['ok'] else 1)
