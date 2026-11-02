# IMPERIA COLD WAR — Validate live costs, conversion exemptions and country-specific briefings.
"""Focused source interpreter; not an emulator of the full HOI4 engine."""
from pathlib import Path
from decimal import Decimal
import copy
import hashlib
import json
import re
import subprocess
import sys
from patch import reverse_edits

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools/spain_1970_v2'))
from script_ast import parse, first, walk

D = Decimal
CHECKS = []


def check(value, message):
    if not value:
        raise AssertionError(message)
    CHECKS.append(message)


def source(name):
    return parse((ROOT / name).read_text(encoding='utf-8-sig'))


def number(value, state):
    if isinstance(value, list):
        result = D(0)
        for key, op, operand in value:
            right = number(operand, state)
            if key == 'value': result = right
            elif key == 'add': result += right
            elif key == 'multiply': result *= right
            elif key == 'max': result = max(result, right)
            elif key == 'min': result = min(result, right)
            else: raise AssertionError(('Unsupported math', key))
        return result
    try:
        return D(value)
    except Exception:
        return state['vars'].get(value, D(0))


def assign(rows, state, action='set'):
    for key, op, value in rows:
        right = number(value, state)
        if action == 'set': state['vars'][key] = right
        elif action == 'add': state['vars'][key] = state['vars'].get(key, D(0)) + right
        elif action == 'subtract': state['vars'][key] = state['vars'].get(key, D(0)) - right


def enabled(rows, state, countries):
    def condition(key, op, value):
        if key in ('AND', 'hidden_trigger', 'custom_trigger_tooltip'):
            return enabled(value, state, countries)
        if key == 'OR': return any(enabled([r], state, countries) for r in value)
        if key == 'NOT': return not enabled(value, state, countries)
        if key == 'tooltip': return True
        if key == 'exists': return state['exists'] == (value == 'yes')
        if key == 'tag': return state['tag'] == value
        if key == 'country_exists': return value in countries and countries[value]['exists']
        if key == 'has_idea': return value in state['ideas']
        if key == 'has_country_flag': return value in state['flags']
        if key == 'set_temp_variable':
            assign(value, state)
            return True
        if key == 'check_variable':
            if first(value, 'var') is not None:
                left = number(first(value, 'var'), state)
                right = number(first(value, 'value'), state)
                comparison = first(value, 'compare', 'equals')
            else:
                variable, comparison, target = value[0]
                left, right = number(variable, state), number(target, state)
            return {'>': left > right, '<': left < right, '=': left == right,
                    'greater_than_or_equals': left >= right}[comparison]
        if key == 'ICW_reserve_currency_affordable':
            return enabled(first(TRIGGERS, key), state, countries)
        raise AssertionError(('Unsupported condition', key))
    return all(condition(*row) for row in rows)


def execute(rows, state, countries, queued):
    last_if = None
    for key, op, value in rows:
        if key in ('if', 'else_if', 'else'):
            run = (key == 'if' or not last_if) and (key == 'else' or enabled(first(value, 'limit', []), state, countries))
            if key == 'if': last_if = run
            elif run: last_if = True
            if run: execute([r for r in value if r[0] != 'limit'], state, countries, queued)
        elif key == 'hidden_effect': execute(value, state, countries, queued)
        elif key in ('set_temp_variable', 'set_variable'): assign(value, state)
        elif key == 'add_to_variable': assign(value, state, 'add')
        elif key == 'subtract_from_variable': assign(value, state, 'subtract')
        elif key == 'clear_variable': state['vars'].pop(value, None)
        elif key == 'clr_country_flag': state['flags'].discard(value)
        elif key == 'custom_effect_tooltip': pass
        elif key == 'update_money_dirty_variable': state['dirty'] += 1
        elif key == 'modify_treasury_effect': execute(TREASURY, state, countries, queued)
        elif key in ('ICW_charge_reserve_realignment', 'ICW_report_dollar_departure'):
            execute(first(EFFECTS, key), state, countries, queued)
        elif key == 'country_event':
            queued.append({'id': first(value, 'id'), 'root': state['tag'], 'from': state.get('sender', state['tag']), 'hours': first(value, 'hours', '0')})
        elif key in countries:
            target = countries[key]
            old_sender = target.get('sender')
            target['sender'] = state['tag']
            execute(value, target, countries, queued)
            if old_sender is None: target.pop('sender', None)
            else: target['sender'] = old_sender
        elif key in ('add_ideas', 'remove_ideas'):
            values = [value] if isinstance(value, str) else [v for k, o, v in value if k == '_bare']
            for idea in values:
                if key == 'add_ideas':
                    if idea in LAWS:
                        for old in set(state['ideas']) & LAWS.keys() - {idea}:
                            state['ideas'].discard(old)
                            if old == 'us_dollar':
                                execute(first(EFFECTS, 'ICW_report_dollar_departure'), state, countries, queued)
                    state['ideas'].add(idea)
                    # The actual on_add callback's new transaction call is exercised here.
                    if idea in LAWS: execute(first(EFFECTS, 'ICW_charge_reserve_realignment'), state, countries, queued)
                else:
                    state['ideas'].discard(idea)
        else:
            raise AssertionError(('Unsupported effect', key))


def country(tag='FRA', gdp='100', debt='500', treasury='1000'):
    return {'tag': tag, 'vars': {'gdp_total': D(gdp), 'debt': D(debt), 'treasury': D(treasury)},
            'exists': True, 'flags': set(), 'ideas': {'us_dollar'}, 'dirty': 0}


TRIGGERS = source('common/scripted_triggers/ICW_reserve_currency_realignment.txt')
EFFECTS = source('common/scripted_effects/ICW_reserve_currency_realignment.txt')
TREASURY = first(source('common/scripted_effects/00_budget_effects.txt'), 'modify_treasury_effect')
EVENTS = source('events/ICW_reserve_currency_realignment.txt')
MANIFEST = json.loads((HERE / 'changes.json').read_text(encoding='utf-8'))
LAWS = MANIFEST['laws']


def main():
    check(len(LAWS) == 18, 'All 18 existing reserve laws are integrated')
    for name, record in MANIFEST['files'].items():
        data = (ROOT / name).read_bytes()
        reverse_edits(data, record)
        check(not data.startswith(b'\xef\xbb\xbf'), 'Script has no BOM: ' + name)
        parse(data.decode('utf-8'))
        check(True, 'Exact insertion reversal and valid script structure: ' + name)
    for idea, name in LAWS.items():
        category = first(first(source(name), 'ideas'), 'reserve_currency')
        law = first(category, idea)
        check(sum(k == 'ICW_charge_reserve_realignment' for k, o, v in walk(first(law, 'on_add'))) == 1, idea + ': exactly one payment callback')
        check(first(law, 'available')[0] == ('ICW_reserve_currency_affordable', '=', 'yes'), idea + ': live affordability evaluated before other requirements')
        check(('custom_modifier_tooltip', '=', 'ICW_reserve_currency_realignment_tt') in first(law, 'modifier'), idea + ': cost formula visible in native law tooltip')
        check(first(law, 'removal_cost') == '-1', idea + ': standalone removal stays disabled')

    # Every real scripted grant/removal stays bracketed; effect previews remain pure.
    conversions = 0
    from patch import parse as span_parse, walk as span_walk
    for name in MANIFEST['files']:
        for node, parents in span_walk(span_parse((ROOT / name).read_text(encoding='utf-8'))):
            if node.key not in ('add_ideas', 'remove_ideas', 'add_idea', 'remove_idea'):
                continue
            values = [node.value] if isinstance(node.value, str) else [n.value for n in node.value if n.key == '_bare']
            if not set(values) & LAWS.keys() or any(p.key == 'effect_tooltip' for p in parents):
                continue
            operation = parents[-1] if parents[-1].key == 'swap_ideas' else node
            parent = parents[-2] if operation is not node else parents[-1]
            position = parent.value.index(operation)
            before, after = parent.value[:position], parent.value[position + 1:]
            def depth_change(nodes, action):
                return any(n.key == action and any(c.key == 'ICW_reserve_scripted_depth' and c.value == '1' for c in n.value) for n in nodes)
            check(depth_change(before, 'add_to_variable') and depth_change(after, 'subtract_from_variable'), name + ': reserve operation is exempt from a second selector charge')
            conversions += 1
    check(conversions > 40, 'All authored conversion sites were checked, including swaps and fallback removals')

    usd = first(first(first(source(LAWS['us_dollar']), 'ideas'), 'reserve_currency'), 'us_dollar')
    check(sum(k == 'ICW_report_dollar_departure' for k, o, v in walk(first(usd, 'on_remove'))) == 1, 'Exactly one departure report on the actual Dollar removal hook')
    check(any(k == 'subtract_from_variable' and first(v, 'global.usd_reserve_adoption_count') == '1' for k, o, v in walk(first(usd, 'on_remove'))), 'The native Dollar network reduction remains active')

    cases = [('100', '0', '10'), ('100', '50', '15'), ('100', '100', '20'),
             ('100', '500', '60'), ('100', '5000', '510'), ('0', '500', '50'),
             ('0.01', '0.01', '0.002'), ('-10', '-100', '0')]
    for gdp, debt, expected in cases:
        amount = D(expected)
        for cash, allowed in [(amount, True), (amount + D('0.001'), True), (amount - D('0.001'), False)]:
            state = country(gdp=gdp, debt=debt, treasury=str(cash))
            result = enabled(first(TRIGGERS, 'ICW_reserve_currency_affordable'), state, {'FRA': state})
            check(result == allowed, f'Cash boundary GDP={gdp}, debt={debt}, cash={cash}')
            check(state['vars']['ICW_reserve_switch_quote'] == amount, f'Correct uncapped quote GDP={gdp}, debt={debt}')
            check(state['vars']['treasury'] == cash and state['vars']['debt'] == D(debt), 'Reading the affordability tooltip spends nothing')
        state = country(gdp=gdp, debt=debt)
        before = copy.deepcopy(state)
        execute(first(EFFECTS, 'ICW_charge_reserve_realignment'), state, {'FRA': state}, [])
        check(state['vars']['treasury'] == before['vars']['treasury'] - amount, f'Exact one-time payment GDP={gdp}, debt={debt}')
        check(state['vars']['debt'] == D(debt) and state['vars']['gdp_total'] == D(gdp), 'Debt and GDP are not consumed or converted')
        check(state['dirty'] == 1, 'Payment uses native treasury dirty refresh exactly once')

    state = country()
    enabled(first(TRIGGERS, 'ICW_reserve_currency_affordable'), state, {'FRA': state})
    state['vars']['debt'] = D('1000')
    execute(first(EFFECTS, 'ICW_charge_reserve_realignment'), state, {'FRA': state}, [])
    check(state['vars']['treasury'] == D('890'), 'Execution uses live debt, not the earlier displayed quote')
    state = country()
    state['vars']['ICW_reserve_scripted_depth'] = D(1)
    execute(first(EFFECTS, 'ICW_charge_reserve_realignment'), state, {'FRA': state}, [])
    check(state['vars']['treasury'] == D('1000') and state['dirty'] == 0, 'Authored scripted changes are exempt')

    # Run an actual emitted conversion sequence with a nested reserve grant.
    script = source('common/scripted_effects/00_currency_effects.txt')
    branch = first(first(script, 'adopt_chinese_yuan_reserve'), 'else')
    state = country()
    execute(branch, state, {'FRA': state}, [])
    check(state['vars']['treasury'] == D('1000'), 'Actual Yuan conversion does not pay twice')
    check('ICW_reserve_scripted_depth' not in state['vars'], 'Conversion depth is cleared after execution')
    state['vars']['ICW_reserve_scripted_depth'] = D(1)
    execute(branch, state, {'FRA': state}, [])
    check(state['vars']['ICW_reserve_scripted_depth'] == 1, 'Nested conversion preserves its outer exemption')

    initializer = [v for k, o, v in first(script, 'currency_startup') if k == 'if'][-1]
    state = country('GER')
    us = country('USA')
    sink = []
    execute([r for r in initializer if r[0] != 'limit'], state, {'GER': state, 'USA': us}, sink)
    check(state['vars']['treasury'] == D('1000') and not sink, 'Actual German initialization neither charges nor reports a dollar departure')
    check(not any(key.startswith('ICW_reserve_') for key in state['vars']), 'Initializer clears both nested exemption counters')

    euro = first(first(first(source(LAWS['euro']), 'ideas'), 'reserve_currency'), 'euro')
    fallback = [v for k, o, v in first(euro, 'on_remove') if k == 'if'][-1]
    state = country()
    state['ideas'].clear()
    state['vars']['ICW_reserve_scripted_depth'] = D(1)
    execute([r for r in fallback if r[0] != 'limit'], state, {'FRA': state}, [])
    check('no_foreign_reserve' in state['ideas'] and state['vars']['treasury'] == D('1000'), 'Actual euro fallback cannot create a second monetary charge')
    check(state['vars']['ICW_reserve_scripted_depth'] == 1, 'Euro fallback does not clear its outer conversion exemption')

    dispatch = next(v for k, o, v in EVENTS if k == 'country_event' and first(v, 'id') == 'ICW_reserve_currency.2')
    visible = next(v for k, o, v in EVENTS if k == 'country_event' and first(v, 'id') == 'ICW_reserve_currency.1')
    us = country('USA')
    countries = {'USA': us, 'FRA': country('FRA'), 'ITA': country('ITA')}
    queued = []
    for tag in ('FRA', 'ITA'):
        state = countries[tag]
        execute(first(EFFECTS, 'ICW_report_dollar_departure'), state, countries, queued)
        state['ideas'].clear()
    check([event['root'] for event in queued] == ['FRA', 'ITA'], 'Simultaneous departures have independent delayed country contexts')
    check(all(event['hours'] == '1' and event['id'] == 'ICW_reserve_currency.2' for event in queued), 'Departures settle before dispatch')
    delivered = []
    for event in queued:
        execute(first(dispatch, 'immediate'), countries[event['root']], countries, delivered)
    check([event['from'] for event in delivered] == ['FRA', 'ITA'] and all(event['root'] == 'USA' for event in delivered), 'Both US briefings retain the correct departing country')
    for case in ('restored', 'annexed', 'usa_absent', 'self', 'initializing'):
        state, us = country(), country('USA')
        countries = {'USA': us, 'FRA': state}
        if case == 'annexed': state['exists'] = False
        if case == 'usa_absent': us['exists'] = False
        if case == 'self': state = us
        if case == 'initializing': state['vars']['ICW_reserve_initializing_depth'] = D(1)
        if case == 'restored':
            sink = []
            execute(first(dispatch, 'immediate'), state, countries, sink)
        else:
            sink = []
            execute(first(EFFECTS, 'ICW_report_dollar_departure'), state, countries, sink)
        check(not sink, 'No false presidential briefing: ' + case)
    check(first(visible, 'option') == [('name', '=', 'ICW_reserve_currency.1.a')], 'Acknowledgement does not impose unapproved countermeasures')
    check(first(visible, 'is_triggered_only') == 'yes' and first(dispatch, 'is_triggered_only') == 'yes', 'Neither event introduces a polling trigger')

    locpath = ROOT / 'localisation/english/ICW_reserve_currency_realignment_l_english.yml'
    check(locpath.read_bytes().startswith(b'\xef\xbb\xbf'), 'English localisation has the required BOM')
    loc = locpath.read_text(encoding='utf-8-sig')
    labels = dict(re.findall(r'^ (\S+): "(.*)"$', loc, re.M))
    for key in ('ICW_reserve_currency.1.t', 'ICW_reserve_currency.1.d', 'ICW_reserve_currency.1.a', 'ICW_reserve_currency_realignment_tt', 'ICW_reserve_currency_treasury_required_tt'):
        check(key in labels, 'Required English localisation: ' + key)
    check('[FROM.GetNameDef]' in labels['ICW_reserve_currency.1.d'] and 'Mr. President' in labels['ICW_reserve_currency.1.d'] and 'countermeasures' in labels['ICW_reserve_currency.1.d'], 'Briefing names the country and advises the President')
    check(not any(char in '\n'.join(labels.values()) for char in ('\u2013', '\u2014')), 'Player-facing prose contains no en/em dashes')
    for name in ('common/scripted_effects/ICW_reserve_currency_realignment.txt', 'common/scripted_triggers/ICW_reserve_currency_realignment.txt', 'events/ICW_reserve_currency_realignment.txt'):
        data = (ROOT / name).read_bytes()
        check(not data.startswith(b'\xef\xbb\xbf'), 'New script has no BOM: ' + name)
        check(data.decode('utf-8').startswith('# IMPERIA COLD WAR — '), 'New script has the project marker: ' + name)
        check(not re.search(r'\b(on_daily|on_weekly|on_monthly|every_country|every_state)\b', data.decode('utf-8')), 'No recurring pulse or world scan: ' + name)
    result = subprocess.run([sys.executable, '-B', str(HERE / 'build.py')], cwd=ROOT, capture_output=True, text=True)
    check(result.returncode == 0, 'Integration recognizes its current source')
    check(json.loads(result.stdout)['up_to_date'], 'Regeneration produces exactly the current files with no missing integration sites')
    summary = {'project': 'IMPERIA COLD WAR', 'passed': len(CHECKS), 'laws': len(LAWS), 'capped': False,
               'historical_rates_claimed': False, 'engine_or_multiplayer_test': False, 'checks': CHECKS}
    (HERE / 'validation.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in summary.items() if k != 'checks'}))


if __name__ == '__main__':
    main()
