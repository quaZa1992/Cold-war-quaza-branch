# IMPERIA COLD WAR — Cross-system audit of native UI, finance and contract lifecycle.
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import validate as V
import render_preview as R
from qa_crew import setup, invite as crew_invite
from qa_cooperation import invite as work_invite
from cooperation import order, field
from mission_rules import REQUIREMENTS


def run():
    # Dictionary comprehensions must not hide duplicate runtime definitions.
    for directory in ['scripted_effects', 'scripted_triggers']:
        names = Counter(k for path, nodes in V.ASTS.items() if '/'+directory+'/' in path for k, _, v in nodes)
        V.check(not [k for k, count in names.items() if count > 1], 'Duplicate ' + directory + ' definitions')
    events = [V.first(v, 'id') for path, nodes in V.ASTS.items() if path.startswith('events/') for k, _, v in nodes if k in ['country_event', 'news_event']]
    V.check(len(events) == len(set(events)), 'Duplicate native event IDs')
    window = V.first(V.first(V.ASTS['interface/COLDWAR_space_race.gui'], 'guiTypes'), 'containerWindowType')
    widgets = [v for k, _, v in window if isinstance(v, list) and V.first(v, 'name')]
    names = [V.first(v, 'name') for v in widgets]
    V.check(len(names) == len(set(names)), 'Duplicate native GUI name across widget types')
    source = (V.ROOT/'localisation/english/COLDWAR_space_race_l_english.yml').read_text(encoding='utf-8-sig')
    V.check('[event_target:' not in source, 'Native localisation rejects event_target: promotions')
    conditions = next(v for v in widgets if V.first(v, 'name') == '"cw_sr_control_conditions"')
    V.check(R.LOC[V.first(conditions, 'text').strip('"')] == '[CW_SR_Control_Conditions]', 'Operations button overwrote the appropriation panel text')
    # Exercise real named targets, including a newly earned world-first record.
    m, _ = setup();m.call('cw_sr_rank');m.call('cw_sr_refresh')
    for rank, tag in [(1, 'USA'), (2, 'SOV'), (3, 'FRA')]:
        V.check(R.NAMES[tag] in R.resolve('[CW_SR_Rank_'+str(rank)+']', m), 'Missing native rank country name')
    m.call('cw_sr_p15_success')
    V.check('Soviet Union' in R.resolve('[cw_sr_world_first_register]', m), 'World-first country target did not localise')
    # Negative cash must never invert a native clamp or buy paid progress.
    template = V.Machine(('SAU',));template.init()
    finance_cases = 0
    for n, p in enumerate(V.DATA['programmes'], 1):
        for state in [1, 6]:
            for cash in [-100, -.001, 0]:
                t = deepcopy(template);t.put(f'cw_sr_p{n}_state', state)
                t.put(f'cw_sr_p{n}_im', 3);t.put(f'cw_sr_p{n}_ic', 1)
                t.put('treasury', cash);t.put('cw_sr_allocation', 1000, True)
                paid = [t.get(f'cw_sr_p{n}_{k}') for k in ['work', 'spent', 'im', 'ic']]
                t.call(f'cw_sr_p{n}_week')
                V.check(t.get('treasury') == V.Q(cash) and paid == [t.get(f'cw_sr_p{n}_{k}') for k in ['work', 'spent', 'im', 'ic']], 'Unfunded engineering/inquiry advanced or changed treasury')
                finance_cases += 1
    # All 17 crew architectures must release preflight reservations when the
    # exact operator/seat binding is gone, without charging another week.
    crew_cases = 0
    from crew import eligible, field as seat
    for n, p in enumerate(V.DATA['programmes'], 1):
        if not eligible(p):continue
        for cause in ['operator_ai', 'war', 'annexed', 'serial', 'seat', 'host_status']:
            t, _ = setup(n);crew_invite(t, n, 1, 'DDR', False)
            host = t.countries['SOV'];t.c = t.countries['DDR']
            if cause == 'operator_ai':host.ai = True
            elif cause == 'war':t.wars.add(frozenset(('SOV', 'DDR')))
            elif cause == 'annexed':host.exists = False
            elif cause == 'serial':host.variables[seat(n, 1, 'serial')] += 1
            elif cause == 'seat':host.variables[seat(n, 1, 'country')] = t.country_ids['POL']
            else:host.variables[seat(n, 1, 'status')] = V.D(1)
            cash = t.get('treasury');weeks = t.get('cw_sr_crew_weeks')
            t.call('cw_sr_crew_training_weekly')
            V.check(t.get('treasury') == cash and t.get('cw_sr_crew_weeks') == weeks, 'Invalid crew agreement bought another training week: '+cause)
            t.call('cw_sr_crew_daily')
            V.check(t.get('cw_sr_crew_status') == 0, 'Orphaned preflight crew reservation: '+cause)
            if cause in ['serial', 'seat']:
                V.check(host.variables[seat(n, 1, 'country')] > 0, 'Stale withdrawal erased a replacement seat binding')
            crew_cases += 1
    # A disappeared operator cannot reserve the delegation indefinitely. If its
    # country later returns, its frozen old report must preserve the new binding.
    t, _ = setup();crew_invite(t, 27, 1, 'DDR');t.rolls.append(0);t.call('cw_sr_p27_launch')
    t.countries['SOV'].exists = False;t.c = t.countries['DDR'];cash = t.get('treasury')
    t.call('cw_sr_crew_daily')
    V.check(t.get('cw_sr_crew_status') == 0 and t.get('treasury') == cash, 'Annexed flight operator stranded a crew reservation or refunded money')
    t.c = t.countries['POL'];t.put('cw_sr_p27_state', 3);t.put('cw_sr_crew_candidate', t.country_ids['DDR']);t.call('cw_sr_p27_crew_invite1')
    t.c = t.countries['DDR'];t.call('cw_sr_crew_accept_27')
    new_binding = [t.get('cw_sr_crew_'+key) for key in ['host', 'programme', 'slot', 'serial', 'status']]
    V.check(new_binding[0] == t.country_ids['POL'] and new_binding[-1] == 2, 'Released delegation could not accept another operator')
    t.countries['SOV'].exists = True;t.c = t.countries['SOV'];t.call('cw_sr_p27_success')
    t.c = t.countries['DDR']
    V.check([t.get('cw_sr_crew_'+key) for key in ['host', 'programme', 'slot', 'serial', 'status']] == new_binding, 'Old resumed flight erased a replacement delegation')
    # Both outbound order slots use the same binding for billing and cleanup.
    operation_cases = 0
    for cause in ['operator_ai', 'war', 'annexed', 'serial', 'country', 'role', 'host_status']:
        for which in [1, 2]:
            t, _ = setup(35);first = work_invite(t, 35, 1, train=False);n = 35
            if which == 2:
                t.put('cw_sr_p36_state', 3);n = 36
                work_invite(t, 36, 2, train=False)
            host = t.countries['SOV'];t.c = t.countries['DDR']
            if cause == 'operator_ai':host.ai = True
            elif cause == 'war':t.wars.add(frozenset(('SOV', 'DDR')))
            elif cause == 'annexed':host.exists = False
            elif cause == 'serial':host.variables[field(n, 'serial')] += 1
            elif cause == 'country':host.variables[field(n, 'country')] = t.country_ids['POL']
            elif cause == 'role':host.variables[field(n, 'role')] = V.D(4)
            else:host.variables[field(n, 'status')] = V.D(1)
            cash = t.get('treasury');weeks = t.get(order(which, 'weeks'))
            # With slot 2 under review the other valid work order still pays.
            t.call('cw_sr_op_weekly')
            V.check(t.get(order(which, 'weeks')) == weeks, 'Invalid work order bought more qualification: '+cause)
            if which == 1 or cause in ['operator_ai', 'war', 'annexed']:
                V.check(t.get('treasury') == cash, 'Invalid provider order was charged')
            t.call('cw_sr_op_daily')
            V.check(t.get(order(which, 'status')) == 0, 'Orphaned operational work order: '+cause)
            if which == 2 and cause in ['serial', 'country', 'role', 'host_status']:
                V.check(t.get(order(first, 'status')) == 2, 'Cleanup cancelled an unrelated live order')
            operation_cases += 1
    # A qualified launch remains valid with three unrelated development places.
    t, p = setup()
    for n in [47, 48, 49]:t.put(f'cw_sr_p{n}_state', 1)
    t.call('cw_sr_refresh')
    V.check(t.get('cw_sr_active') == 3 and t.test(V.TRIGGERS['cw_sr_p27_launch_allowed']), 'Unrelated development blocked a qualified mission')
    V.check('MET' in R.resolve('[CW_SR_Capacity_27]', t), 'Readiness falsely requires an extra development place')
    # Numerical preview must deduct partial prestige before sharing its remainder.
    t, p = setup();crew_invite(t, 27, 1, 'DDR');t.rolls.append(0);t.call('cw_sr_p27_launch');t.call('cw_sr_p27_partial')
    t.put('cw_sr_allocation', 1000, True)
    for _ in range(20):
        if t.get('cw_sr_p27_state') == 3:break
        t.call('cw_sr_p27_week')
    V.check(t.get('cw_sr_p27_state') == 3, 'Funded partial-result review did not finish')
    crew_invite(t, 27, 1, 'DDR', False);t.c = t.countries['DDR']
    for _ in range(6):t.call('cw_sr_crew_training_weekly')
    t.c = t.countries['SOV'];t.call('cw_sr_refresh')
    expected = (V.D(p['prestige'])-t.get('cw_sr_p27_partial_award'))*V.D('.8')
    V.check(t.get('cw_sr_crew_host_prestige') == expected, 'Crew preview promises prestige already paid for partial results')
    initial = t.get('cw_sr_prestige');t.rolls.append(0);t.call('cw_sr_p27_launch');t.call('cw_sr_p27_success')
    V.check(t.get('cw_sr_prestige')-initial == expected, 'First-success preview differs from actual shared award')
    # The legacy foreign pilot is a mission loss, not a national personnel loss.
    t, _ = setup(78);t.rolls.extend([9999, 0]);t.call('cw_sr_p78_launch')
    V.check(t.get('cw_sr_fatalities') == 1 and t.get('cw_sr_p78_fatalities') == 2 and t.c.manpower == 99999, 'Interkosmos foreign pilot was counted as a national astronaut')
    # Every compiled UI action still refuses AI, irrespective of cached state.
    gui = V.first(V.first(V.ASTS['common/scripted_guis/COLDWAR_space_race_gui.txt'], 'scripted_gui'), 'cw_sr_main')
    t, _ = setup();t.c.ai = True;before = deepcopy(t.c.variables);events_before = len(t.events)
    for name, _, body in V.first(gui, 'effects'):t.run(body)
    V.check(t.c.variables == before and len(t.events) == events_before, 'AI executed a native player UI callback')
    report = {'project': 'IMPERIA COLD WAR', 'status': 'passed', 'checks': V.CHECKS,
              'negative_cash_cases': finance_cases, 'invalid_crew_assignments': crew_cases,
              'invalid_operational_orders': operation_cases, 'duplicate_widgets': [],
              'invalid_localisation_promotions': [], 'first_success_preview_matches_payment': True, 'annexed_operator_and_replacement_delegation': 'passed', 'legacy_national_casualties': 'passed',
              'live_engine_evidence': 'Prior log contains 1015 invalid rank promotions and one duplicate operations widget warning.',
              'live_game_retested': False, 'live_multiplayer_tested': False}
    Path(__file__).with_name('system_audit_validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':run()
