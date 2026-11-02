# IMPERIA COLD WAR — Bulletin retention and human partner UI transactions.
from copy import deepcopy
import json
from pathlib import Path
import validate as V
from qa_crew import setup
from qa_cooperation import qualify
from cooperation import field, order
from news_archive import REGULAR_DAYS, MAJOR_DAYS


def campaign(m):
    """Disposable archive and view caches are deliberately excluded."""
    fields = ['treasury', 'cw_sr_prestige', 'cw_sr_science', 'cw_sr_spent', 'cw_sr_fatalities']
    fields += [f'cw_sr_p{n}_{suffix}' for n in range(1, 85) for suffix in
               ['state', 'work', 'months', 'successes', 'launches', 'days', 'im', 'ic']]
    return {tag: ([c.variables.get(k, V.D(0)) for k in fields],
                  c.pp, c.manpower, deepcopy(c.tech_bonuses), deepcopy(c.technologies),
                  {f for f in c.flags if f.endswith(('_awarded', '_deployed', '_completed')) or f.startswith('cw_sr_cap_')})
            for tag, c in m.countries.items()}


def run():
    gui = V.first(V.first(V.ASTS['common/scripted_guis/COLDWAR_space_race_gui.txt'], 'scripted_gui'), 'cw_sr_main')
    callbacks = {k: v for k, _, v in V.first(gui, 'effects')}
    enabled = {k: v for k, _, v in V.first(gui, 'triggers') if k.endswith('_click_enabled')}

    def click(m, name):
        if name + '_click_enabled' in enabled:
            V.check(m.test(enabled[name + '_click_enabled']), 'Disabled control: ' + name)
        m.run(callbacks[name + '_click'])

    m = V.Machine(('SAU',));m.init();m.g['num_days'] = V.D(100)
    m.call('cw_sr_p47_start');m.call('cw_sr_refresh')
    V.check(m.get('cw_sr_p47_report_expires') == 100 + REGULAR_DAYS, 'Routine bulletin expiry missing')
    m.call('cw_sr_p27_success');m.put('cw_sr_selected', 27);m.c.flags.add('cw_sr_open')
    click(m, 'cw_sr_tab_7')
    V.check(m.get('cw_sr_p27_report_expires') == 100 + MAJOR_DAYS and m.get('cw_sr_news_count') == 2, 'Success retention or archive count wrong')
    before = campaign(m);expiry = m.get('cw_sr_p27_report_expires');m.g['num_days'] = V.D(279)
    for _ in range(3):click(m, 'cw_sr_news_read')
    V.check(campaign(m) == before and m.get('cw_sr_p27_report_expires') == expiry, 'Reading renewed expiry or changed mission benefits')
    # Persisted clocks, not loaded-session countdowns, drive the same expiry.
    loaded = deepcopy(m);loaded.g['num_days'] = V.D(280);loaded.call('cw_sr_refresh')
    V.check('cw_sr_p47_last_report' not in loaded.c.variables and 'cw_sr_p47_report_expires' not in loaded.c.variables, 'Routine report variables were not removed')
    V.check(loaded.get('cw_sr_news_count') == 1 and loaded.get('cw_sr_view_report') == 8, 'Expiry removed a retained success or kept a stale view')
    V.check(campaign(loaded) == before, 'Archive cleanup changed permanent records or research')
    loaded.g['num_days'] = V.D(465);loaded.call('cw_sr_refresh');old_events = len(loaded.events)
    loaded.call('cw_sr_replay_bulletin')
    V.check(loaded.get('cw_sr_news_count') == 0 and loaded.get('cw_sr_view_report') == 0 and len(loaded.events) == old_events, 'Expired report remained replayable')
    V.check(campaign(loaded) == before, 'Success expiry removed mission achievements')
    # Existing saves get one finite migration lease; navigation never extends it.
    t = V.Machine(('SAU',));t.init();t.g['num_days'] = V.D(1000)
    for n in range(1, 85):t.put(f'cw_sr_p{n}_last_report', 8 if n % 2 else 1)
    t.call('cw_sr_news_cleanup')
    V.check(t.get('cw_sr_news_count') == 84, 'Archive capacity or old-save migration wrong')
    snapshot = deepcopy(t.c.variables)
    t.g['num_days'] = V.D(1001);t.call('cw_sr_news_cleanup')
    V.check(t.c.variables == snapshot, 'Archive scanned before its due date')
    t.g['num_days'] = V.D(1180);t.call('cw_sr_news_cleanup')
    V.check(t.get('cw_sr_news_count') == 42, 'Routine legacy reports failed to expire')
    t.g['num_days'] = V.D(1365);t.call('cw_sr_news_cleanup')
    V.check(t.get('cw_sr_news_count') == 0, 'Legacy reports received an infinite migration lease')
    # A newly issued report replaces one pointer rather than appending history.
    m.g['num_days'] = V.D(500);m.call('cw_sr_p27_failure');m.call('cw_sr_news_cleanup')
    V.check(m.get('cw_sr_p27_last_report') == 10 and m.get('cw_sr_p27_report_expires') == 680 and m.get('cw_sr_news_count') == 1, 'New outcome did not replace expired bulletin')
    # Actual generated GUI callbacks must handle SP, paused joins and AI takeover.
    sp, _ = setup()
    for tag in ['DDR', 'POL', 'USA']:sp.countries[tag].ai = True
    sp.c.flags.add('cw_sr_open');sp.put('cw_sr_tab', 8)
    click(sp, 'cw_sr_control_crew')
    V.check(sp.get('cw_sr_partner_count') == 0 and sp.get('cw_sr_crew_candidate') == 0, 'SP offered an AI partner')
    before = campaign(sp);click(sp, 'cw_sr_crew_partner')
    V.check(campaign(sp) == before and sp.get('cw_sr_crew_candidate') == 0, 'Empty selector initialized or funded AI countries')
    sp.countries['DDR'].ai = False;sp.countries['POL'].ai = False
    click(sp, 'cw_sr_crew_partner')
    V.check(sp.get('cw_sr_partner_count') == 2 and sp.get('cw_sr_crew_candidate') == sp.country_ids['DDR'], 'Paused player join was not discovered by refresh')
    click(sp, 'cw_sr_crew_partner');V.check(sp.get('cw_sr_crew_candidate') == sp.country_ids['POL'], 'MP partner did not advance')
    click(sp, 'cw_sr_crew_partner');V.check(sp.get('cw_sr_crew_candidate') == sp.country_ids['DDR'], 'MP partner selector did not wrap')
    # A selection is merely a proposal; the recipient must consent in its scope.
    click(sp, 'cw_sr_crew_guest1_choose')
    V.check(sp.countries['DDR'].variables['cw_sr_crew_status'] == 1 and sp.countries['POL'].variables.get('cw_sr_crew_status', 0) == 0, 'Invitation delivered to the wrong player')
    sp.c = sp.countries['DDR'];sp.call('cw_sr_crew_accept_27')
    V.check(sp.get('cw_sr_crew_status') == 2, 'Selected player could not accept the crew invitation')
    sp.c = sp.countries['SOV'];sp.wars.add(frozenset(('SOV', 'DDR')))
    click(sp, 'cw_sr_crew_partner')
    V.check(sp.get('cw_sr_partner_count') == 1 and sp.get('cw_sr_crew_candidate') == sp.country_ids['POL'], 'Enemy or stale selection retained')
    sp.countries['POL'].ai = True;sp.g['num_days'] = V.D(1);sp.call('cw_sr_refresh')
    V.check(sp.get('cw_sr_partner_count') == 0 and sp.get('cw_sr_crew_candidate') == 0, 'Visible partner list did not recover from AI takeover')
    # Both selectors use the same human-country catalogue and signed transactions.
    op, _ = setup(35);op.c.flags.add('cw_sr_open');op.put('cw_sr_tab', 8)
    op.countries['USA'].ai = True
    qualify(op, 'DDR');qualify(op, 'POL')
    click(op, 'cw_sr_control_operations')
    V.check(op.get('cw_sr_crew_candidate') == op.country_ids['DDR'], 'Operational page did not select its first human partner')
    click(op, 'cw_sr_op_candidate')
    V.check(op.get('cw_sr_crew_candidate') == op.country_ids['POL'], 'Operational selector failed to cycle')
    click(op, 'cw_sr_op_invite');w = int(op.get(field(35, 'order')))
    V.check(w in [1, 2] and op.countries['POL'].variables[order(w, 'status')] == 1, 'Operational offer went to the wrong player')
    op.c = op.countries['POL'];op.call('cw_sr_op_accept_35')
    V.check(op.get(order(w, 'status')) == 2, 'Selected player could not approve the work package')
    # The emergency switch still makes all new entry points inert.
    op.gf.add('cw_sr_emergency_disabled');frozen = deepcopy(op.c.variables)
    for name in ['cw_sr_news_cleanup', 'cw_sr_partner_scan', 'cw_sr_partner_refresh', 'cw_sr_crew_candidate_next']:
        op.call(name)
    V.check(op.c.variables == frozen, 'New archive or partner function bypassed GC quarantine')
    window = V.first(V.first(V.ASTS['interface/COLDWAR_space_race.gui'], 'guiTypes'), 'containerWindowType')
    names = {V.first(v, 'name') for k, _, v in window if isinstance(v, list)}
    V.check('"cw_sr_date"' not in names and '"cw_sr_footer"' not in names, 'Duplicate campaign date remains in the interface')
    report = {'project': 'IMPERIA COLD WAR', 'status': 'passed', 'checks': V.CHECKS,
              'ordinary_retention_days': REGULAR_DAYS, 'success_disaster_retention_days': MAJOR_DAYS,
              'maximum_reports_per_country': 84, 'old_save_migration': 'finite lease',
              'replay_renews_retention': False, 'permanent_achievements_affected': False,
              'partner_tests': 'actual generated GUI callbacks, SP, multiple human countries, war, paused join, AI takeover, crew and work-package recipient consent',
              'live_game_tested': False, 'live_multiplayer_tested': False}
    Path(__file__).with_name('news_partner_validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':run()
