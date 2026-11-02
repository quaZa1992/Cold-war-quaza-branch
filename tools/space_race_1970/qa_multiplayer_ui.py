# IMPERIA COLD WAR — Interleaved human-country command-room isolation.
"""Executes native callbacks in a shared model; this is not a network/OOS test."""
from copy import deepcopy
import json
from pathlib import Path
import validate as V
from qa_crew import setup


def run():
    gui = V.first(V.first(V.ASTS['common/scripted_guis/COLDWAR_space_race_gui.txt'], 'scripted_gui'), 'cw_sr_main')
    callbacks = {k: v for k, _, v in V.first(gui, 'effects')}
    enabled = {k: v for k, _, v in V.first(gui, 'triggers') if k.endswith('_click_enabled')}
    fields = ['selected', 'tab', 'region', 'system', 'page', 'list_page', 'filter_region', 'filter_national', 'filter_kind', 'filter_ready', 'crew_candidate']

    def view(m, tag):
        return [m.countries[tag].variables.get('cw_sr_'+k, V.D(0)) for k in fields]

    def economy(m):
        keys = ['treasury', 'cw_sr_prestige', 'cw_sr_science', 'cw_sr_spent', 'cw_sr_fatalities']
        keys += [f'cw_sr_p{n}_{k}' for n in range(1, 85) for k in ['state', 'work', 'days', 'launches', 'successes']]
        return {tag: ([c.variables.get(k, V.D(0)) for k in keys], c.pp, c.manpower, deepcopy(c.tech_bonuses)) for tag, c in m.countries.items()}

    m, _ = setup();tags = ['SOV', 'USA', 'DDR']
    for tag, selected in zip(tags, [27, 84, 35]):
        m.c = m.countries[tag];m.put('cw_sr_selected', selected);m.call('cw_sr_open_from_ledger')
    initial = economy(m);actions = 0
    for turn in range(12):
        for index, tag in enumerate(tags):
            m.c = m.countries[tag];others = {t: view(m, t) for t in tags if t != tag}
            name = 'cw_sr_tab_'+str(1+(turn+index) % 7)
            m.run(callbacks[name+'_click']);actions += 1
            V.check(all(view(m, t) == state for t, state in others.items()), 'Navigation overwrote another country view')
            V.check(economy(m) == initial and not m.rolls, 'Interleaved menu navigation spent money, advanced flights or drew RNG')
    # Partner lists and close/reopen actions remain country-scoped as well.
    for tag in tags:
        m.c = m.countries[tag];others = {t: view(m, t) for t in tags if t != tag}
        m.call('cw_sr_crew_candidate_next');m.run(callbacks['cw_sr_close_click']);m.call('cw_sr_open_from_ledger');actions += 3
        V.check(all(view(m, t) == state for t, state in others.items()), 'Partner selection or close/reopen changed another country view')
        V.check(all('cw_sr_open' in m.countries[t].flags for t in tags), 'Closing one country menu closed another country window')
    # Two operators competing for one guest cannot reserve that guest twice.
    m.c = m.countries['SOV'];m.put('cw_sr_crew_candidate', m.country_ids['DDR']);m.call('cw_sr_p27_crew_invite1')
    m.c = m.countries['USA'];m.put('cw_sr_p27_state', 3);m.put('cw_sr_crew_candidate', m.country_ids['DDR']);m.call('cw_sr_p27_crew_invite1')
    V.check(m.countries['SOV'].variables.get('cw_sr_p27_guest1_country') == m.country_ids['DDR'] and m.get('cw_sr_p27_guest1_country') == 0, 'Two operators reserved the same pending guest')
    m.c = m.countries['DDR'];m.call('cw_sr_crew_accept_27')
    V.check(m.get('cw_sr_crew_host') == m.country_ids['SOV'] and m.get('cw_sr_crew_status') == 2, 'Competing offer replaced the accepted operator')
    # Two national outcomes can contend for one world first. The global receipt
    # must select exactly the first processed outcome, in either ordering.
    for winner, later in [('SOV', 'USA'), ('USA', 'SOV')]:
        t, _ = setup();t.c = t.countries[winner];t.call('cw_sr_p15_success')
        ident = next(i for i, item in enumerate(V.DATA['milestones'], 1) if item['capability'] == 'orbital-station')
        t.c = t.countries[later];t.call('cw_sr_p15_success')
        V.check(t.targets['cw_sr_first_holder_'+str(ident)].tag == winner, 'Later national result stole a world first')
        V.check(sum(event[1] == 'cw_sr_world.'+str(9000+ident) for event in t.events) == 1, 'World-first news was awarded twice')
    report = {'project': 'IMPERIA COLD WAR', 'status': 'passed', 'checks': V.CHECKS,
              'interleaved_human_countries': len(tags), 'ui_actions': actions,
              'independent_country_views': True, 'navigation_changes_campaign_state': False,
              'competing_guest_reservations': 'one accepted operator', 'competing_world_firsts': 'both orderings, one receipt and news event',
              'cooperative_players_same_country': 'country-scoped selections are shared',
              'native_dirty_counter': 'global GUI invalidation, not a shared programme selection',
              'live_multiplayer_tested': False, 'network_oos_tested': False}
    Path(__file__).with_name('multiplayer_ui_validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8');print(json.dumps(report))


if __name__ == '__main__':run()
