# IMPERIA COLD WAR — Budget controls and deterministic records/news navigation.
"""Execute generated callbacks and compare ordered command replays.

The model checks script behaviour. It does not simulate HOI4 networking or
establish that a live multiplayer session cannot go out of sync.
"""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path

import validate as V
from qa_news_partners import campaign


def run():
    gui = V.first(V.first(V.ASTS['common/scripted_guis/COLDWAR_space_race_gui.txt'], 'scripted_gui'), 'cw_sr_main')
    callbacks = {k: v for k, _, v in V.first(gui, 'effects')}
    enabled = {k: v for k, _, v in V.first(gui, 'triggers') if k.endswith('_click_enabled')}
    tags = ('USA', 'SOV', 'DDR')
    actions = 0

    def click(m, name):
        nonlocal actions
        if name + '_click_enabled' in enabled:
            V.check(m.test(enabled[name + '_click_enabled']), 'Disabled control: ' + name)
        m.run(callbacks[name + '_click'])
        actions += 1

    # Inspect all reachable script helpers, including branches not exercised
    # by the fixtures. Rendering conditions and localisation cannot call effects.
    roots = ['cw_sr_tab_6_click', 'cw_sr_tab_7_click', 'cw_sr_list_prev_click',
             'cw_sr_list_next_click', 'cw_sr_news_prev_click',
             'cw_sr_news_next_click', 'cw_sr_news_read_click']
    roots += [f'cw_sr_slot_{n}_wide_click' for n in range(12)]
    forbidden = {'random', 'random_list', 'random_country', 'set_temp_variable_to_random',
                 'modify_treasury_effect', 'add_political_power', 'add_manpower',
                 'add_tech_bonus', 'set_technology', 'save_global_event_target_as',
                 'clear_global_event_target', 'set_global_flag'}
    visited = set()

    # IMPERIA COLD WAR — Preserve the existing one-time historical tech bootstrap.
    # This branch also runs in initialize(), before any normal menu action.
    # Distinguish it from repeatable research awards in an archive callback.
    historical_guard = V.parse('NOT = { has_country_flag = cw_sr_hardware_history }')
    historical_blocks = []

    def without_historical_bootstrap(body):
        result = []
        for key, op, value in body:
            if key == 'if' and V.first(value, 'limit') == historical_guard:
                historical_blocks.append(value)
                continue
            result.append((key, op, without_historical_bootstrap(value) if isinstance(value, list) else value))
        return result

    def inspect(name, body):
        if name in visited:
            return
        visited.add(name)
        if name == 'cw_sr_technology_refresh':
            body = without_historical_bootstrap(body)
        for key, _, value in V.walk(body):
            V.check(key not in forbidden, f'Archive navigation reaches {key} through {name}')
            if key in V.EFFECTS and value == 'yes':
                inspect(key, V.EFFECTS[key])

    for name in roots:
        inspect(name, callbacks[name])
    from technology_integration import HISTORICAL_TECH
    V.check(len(historical_blocks) == 1, 'Historical technology bootstrap lost its one-time guard')
    expected_tech = Counter(tech for entries in HISTORICAL_TECH.values() for tech in entries)
    actual_tech = Counter(tech for key, _, value in V.walk(historical_blocks[0]) if key == 'set_technology'
                          for tech, _, enabled_tech in value if tech != 'popup' and enabled_tech == '1')
    V.check(actual_tech == expected_tech, 'Bootstrap grants technology outside the historical baseline')
    V.check(V.first(historical_blocks[0], 'set_country_flag') == 'cw_sr_hardware_history',
            'Historical technology bootstrap has no permanent receipt')
    read_surfaces = [('triggers', V.first(gui, 'triggers')), ('properties', V.first(gui, 'properties'))]
    read_surfaces += [(V.first(body, 'name'), body) for key, _, body in
                      V.ASTS['common/scripted_localisation/COLDWAR_space_race_localisation.txt'] if key == 'defined_text']
    for name, body in read_surfaces:
        for key, _, value in V.walk(body):
            V.check(key not in V.EFFECTS, 'Rendering calls an effect: ' + str(name) + ': ' + key)
    for name, event in V.EVENTS.items():
        if not name.startswith('cw_sr_report.'):
            continue
        V.check(V.first(event, 'immediate') is None and V.first(event, 'after') is None,
                'Report replay has an automatic effect: ' + name)
        for option in V.values(event, 'option'):
            V.check(all(k in {'name', 'custom_effect_tooltip'} for k, _, _ in option),
                    'Report acknowledgement has a gameplay effect: ' + name)

    def fixture():
        m = V.Machine(tags)
        m.g['num_days'] = V.D(100)
        for tag in tags:
            m.c = m.countries[tag]
            m.init()
            V.check('cw_sr_hardware_history' in m.c.flags, 'Historical hardware was not initialized before navigation')
            m.c.flags.add('cw_sr_open')
            # All seven record pages, plus distinct live bulletin types.
            for n in range(1, 85):
                m.put(f'cw_sr_p{n}_launches', 1)
            for n, stage, expires in [(27, 8, 465), (47, 1, 280), (84, 11, 465)]:
                m.put(f'cw_sr_p{n}_last_report', stage)
                m.put(f'cw_sr_p{n}_report_expires', expires)
            # Issuing a real bulletin also invalidates this cached count.
            m.put('cw_sr_news_next_cleanup', '100')
            m.put('cw_sr_selected', 27)
            m.call('cw_sr_refresh')
        return m

    def other_countries(m, tag):
        return {t: deepcopy(c) for t, c in m.countries.items() if t != tag}

    def persistent(m):
        return (deepcopy(m.countries), deepcopy(m.g), deepcopy(m.gf),
                {key: value.tag for key, value in m.targets.items()}, Counter(m.events), list(m.rolls))

    m = fixture()
    peer = deepcopy(m)
    initial = campaign(m)
    commands = (['cw_sr_tab_6'] + ['cw_sr_list_next'] * 6 + ['cw_sr_list_prev',
                'cw_sr_slot_0_wide', 'cw_sr_tab_7', 'cw_sr_news_next',
                'cw_sr_news_read', 'cw_sr_news_prev', 'cw_sr_news_read'])
    # Replay each country's same command order, reversing only the interleaving
    # of independent countries. Country state and event recipients must agree.
    for name in commands:
        for model, order in [(m, tags), (peer, tuple(reversed(tags)))]:
            for tag in order:
                model.c = model.countries[tag]
                others = other_countries(model, tag)
                click(model, name)
                V.check(other_countries(model, tag) == others, 'Archive click changed another country')
                V.check(campaign(model) == initial and not model.rolls,
                        'Archive click changed mission progress, rewards, research or finance')
                if name == 'cw_sr_tab_6':
                    V.check(model.get('cw_sr_list_count') == 84, 'Records omitted accepted launches')
                if name == 'cw_sr_news_read':
                    V.check(model.events[-1][2] == tag, 'Report replay reached the wrong recipient')
        V.check(persistent(m) == persistent(peer), 'Independent archive commands depend on country interleaving')

    # At the exact expiry, stale UI reads become inert, with no reward replay.
    for model in (m, peer):
        for day in (280, 465):
            model.g['num_days'] = V.D(day)
            for tag in tags:
                model.c = model.countries[tag]
                model.put('cw_sr_selected', 47)
                before = campaign(model)
                events = len(model.events)
                click(model, 'cw_sr_news_read')
                V.check(len(model.events) == events and campaign(model) == before,
                        'Expired bulletin fired an event or changed campaign state')
                click(model, 'cw_sr_tab_6')
                V.check(model.get('cw_sr_list_count') == 84, 'News expiry erased permanent records')
                click(model, 'cw_sr_tab_7')
                V.check(model.get('cw_sr_news_count') == (2 if day == 280 else 0),
                        'Archive expiry differs between countries')
        V.check(not model.rolls, 'Archive expiry consumed mission randomness')
    V.check(persistent(m) == persistent(peer), 'Archive expiry changed replay convergence')

    # Both sizes are weekly ceiling adjustments, not immediate appropriations.
    baseline = campaign(m)
    for tag in tags:
        m.c = m.countries[tag]
        m.put('cw_sr_tab', 4)
        m.put('cw_sr_budget', 1)
        for name, expected in [('up_large', '1.50'), ('up', '1.55'),
                               ('down_large', '1.05'), ('down', '1.00')]:
            others = other_countries(m, tag)
            click(m, 'cw_sr_budget_' + name)
            V.check(m.get('cw_sr_budget') == V.D(expected), 'Wrong weekly budget increment: ' + name)
            V.check(other_countries(m, tag) == others, 'Budget control changed another country')
            V.check(campaign(m) == baseline, 'Budget control charged funds or advanced engineering')
        m.put('cw_sr_budget', '.01')
        click(m, 'cw_sr_budget_down_large')
        V.check(m.get('cw_sr_budget') == 0, 'Large decrement crossed the zero floor')
        V.check(not m.test(enabled['cw_sr_budget_down_click_enabled']) and
                not m.test(enabled['cw_sr_budget_down_large_click_enabled']), 'Decrease is enabled at zero')
        m.put('cw_sr_budget', '11.53')
        click(m, 'cw_sr_budget_up_large')
        V.check(m.get('cw_sr_budget') == V.Q('11.53846'), 'Large increment crossed the ceiling')
        V.check(not m.test(enabled['cw_sr_budget_up_click_enabled']) and
                not m.test(enabled['cw_sr_budget_up_large_click_enabled']), 'Increase is enabled at the cap')
    # Runtime guards also reject stale clicks after quarantine or AI takeover.
    for disabled in ('ai', 'emergency'):
        t = deepcopy(m)
        if disabled == 'ai':
            t.c.ai = True
        else:
            t.gf.add('cw_sr_emergency_disabled')
        frozen = persistent(t)
        for name in ('cw_sr_budget_up_large', 'cw_sr_budget_down_large', 'cw_sr_tab_6',
                     'cw_sr_tab_7', 'cw_sr_news_next', 'cw_sr_news_read'):
            t.run(callbacks[name + '_click'])
        V.check(persistent(t) == frozen, 'Disabled client path changed state: ' + disabled)

    report = {'project': 'IMPERIA COLD WAR', 'status': 'passed', 'checks': V.CHECKS,
              'weekly_budget_steps_bn': [0.05, 0.5], 'weekly_budget_bounds_bn': [0, 11.53846],
              'human_countries': len(tags), 'executed_ui_actions': actions,
              'record_pages': 7, 'archive_call_graph_helpers': len(visited),
              'archive_navigation_mutates_campaign': False,
              'report_replay_grants_rewards_or_draws_rng': False,
              'independent_country_interleavings_converge': True,
              'expired_news_preserves_records': True,
              'ai_and_gc_quarantine_guards': 'passed',
              'live_multiplayer_tested': False, 'network_oos_tested': False,
              'limitations': 'Deterministic script-model replay, not a HOI4 network test. Same-country co-op shares country UI selections.'}
    Path(__file__).with_name('budget_archive_validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    run()
