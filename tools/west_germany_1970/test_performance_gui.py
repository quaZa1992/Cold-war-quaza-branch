# IMPERIA COLD WAR — Scoped politics panel launchers and GUI refresh regression
"""Execute emitted GUI effects in the existing strict script harness.

Run with Python; no generated mod files are written. This checks scripted work
and refresh behaviour, not engine frame times or HOI4's GUI implementation.
The border scan itself is covered by the separate differential border test.
"""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys

# Use the compiler's canonical import order; importing unity alone cannot resolve
# its focus anchors. Importing this module does not call build() or write files.
import compile as generator  # noqa: F401
import gui
import rivalry
import unity
import security_contract
import ddr_relations
import sandbox_state
from cw_lib import P, check_braces

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('cwger_gui_harness', ROOT / 'tools/guest_workers/validate.py')
V = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = V
spec.loader.exec_module(V)

gui.build()
ddr_files = ddr_relations.files()
refresh_text = gui.refresh_effects()
scripted_gui_text = gui.scripted_gui_file()
check_braces(refresh_text, 'GUI refresh effects')
check_braces(scripted_gui_text, 'scripted GUIs')
EFFECTS = {key: value for key, _, value in V.parse(refresh_text + unity.EXTRA)}
# IMPERIA CW — Cold War: execute the real lifecycle providers used by refresh.
EFFECTS.update((key, value) for key, _, value in V.parse(security_contract.effects()))
EFFECTS.update((key, value) for key, _, value in V.parse(ddr_files['common/scripted_effects/COLDWAR_DDR_1970_relations.txt']))
# The runtime scan must remain reachable independently of whether a window is
# open. Its exact state/division calculations are tested against the old scan.
EFFECTS[rivalry.R + '_border_count'] = V.parse('add_to_variable = { gui_test_border_samples = 1 }')
TRIGGERS = {key: value for key, _, value in V.parse(rivalry.trigger_file())}
TRIGGERS.update((key,value) for key,_,value in V.parse(generator.security.triggers()))
TRIGGERS.update((key, value) for key, _, value in V.parse(security_contract.triggers()))
TRIGGERS.update((key, value) for key, _, value in V.parse(ddr_files['common/scripted_triggers/COLDWAR_DDR_1970_relations.txt']))
TRIGGERS.update((key,value) for key,_,value in V.parse(sandbox_state.files()['common/scripted_triggers/COLDWAR_GER_1970_sandbox.txt']))
native_ddr=V.parse((ROOT/'common/scripted_triggers/COLDWAR_DDR_1970_scripted_triggers.txt').read_text(encoding='utf-8'))
TRIGGERS['COLDWAR_DDR_ladder_border_active']=V.first(native_ddr,'COLDWAR_DDR_ladder_border_active')
TRIGGERS['IMP_is_1970_scenario'] = V.parse('always = yes')
GUIS = {key: value for key, _, value in V.first(V.parse(scripted_gui_text), 'scripted_gui')}
WINDOWS = [window for window, _ in gui.WINDOWS]
checks = 0


def check(condition, message):
    global checks
    checks += 1
    assert condition, message


class GuiMachine(V.ScriptMachine):
    def __init__(self):
        super().__init__(EFFECTS, TRIGGERS)
        self.countries = {tag: V.Country(tag) for tag in ('GER', 'DDR', 'USA', 'SOV', 'ENG', 'FRA', 'POL', 'global')}
        self.current = self.root = self.countries['GER']
        self.origin = self.previous = self.current
        self.display_operations = 0

    def test(self, body):
        # Native forms used by this country's emitted GUI and active trigger.
        native = []
        for key, op, value in body:
            if key in self.triggers and value == 'no':
                native.append(('NOT', '=', [(key, op, 'yes')]))
            elif key == 'country_exists':
                native.append((value, '=', [('exists', '=', 'yes')]))
            elif key == 'original_tag':
                native.append(('tag', op, value))
            elif key == 'has_global_flag':
                native.append(('global', '=', [('has_country_flag', op, value)]))
            elif key == 'date':
                day = (1977, 10, 1)
                target = tuple(map(int, value.split('.')))
                answer = {'<': day < target, '>': day > target, '=': day == target}[op]
                native.append(('always', '=', 'yes' if answer else 'no'))
            elif key in ('has_completed_focus', 'has_war_with'):
                attribute = 'completed_focuses' if key == 'has_completed_focus' else 'wars'
                answer = value in getattr(self.current, attribute, set())
                native.append(('always', '=', 'yes' if answer else 'no'))
            else:
                native.append((key, op, value))
        return super().test(native)

    def execute(self, body):
        for key, _, value in body:
            if key.endswith('_variable') and not key.startswith(('check_', 'set_temp_', 'divide_temp_')):
                target = value if isinstance(value, str) else V.first(value, 'var', value[0][0])
                if target.startswith(('cwgg_g_', 'cwsec_g_')):
                    self.display_operations += 1
        return super().execute(body)


def machine(ai=False, open_windows=False):
    m = GuiMachine()
    m.root.is_ai = ai
    m.root.flags['cwgg_initialized'] = V.D(0)
    m.root.flags[P + '_initialized'] = V.D(0)
    m.root.flags['cwsec_initialized'] = V.D(0)
    m.root.variables.update(cwgg_klima=V.D(25), cwgg_stufe=V.D(3), cwgg_init_brd=V.D(4),
                            cwger_terror_left=V.D(43), cwger_security=V.D(62), cwger_rechtsstaat=V.D(42),
                            cwger_bka_level=V.D(2), cwger_gsg9_tier=V.D(3), cwger_raf_gen=V.D(2),
                            cwger_raf_cadre=V.D(24), cwger_raf_milieu=V.D(48), cwgg_u_agreed=V.D(99),
                            cwgg_u_ch_1=V.D(1), cwgg_u_ch_3=V.D(3), cwgg_u_ch_5=V.D(2))
    m.countries['global'].variables['num_days'] = V.D(100)
    if open_windows:
        for w in WINDOWS:
            m.root.flags[w.flag] = V.D(0)
    return m


def click(m, window, panel, name):
    effects = V.first(GUIS[window.id + '_' + panel], 'effects')
    m.execute(V.first(effects, window.id + '_' + name + '_click'))


savings = {}
per_window_operations = {}
for w in WINDOWS:
    baseline = machine(open_windows=True)
    baseline.execute(V.parse('\n'.join(w.runtime_refresh + w.topbar_refresh + w.refresh)))
    optimized = machine(open_windows=True)
    optimized.call(f'{P}_{w.id[5:]}_gui_refresh')
    expected = {key: value for key, value in baseline.root.variables.items()
                if key.startswith(('cwgg_g_', 'cwsec_g_'))}
    actual = {key: value for key, value in optimized.root.variables.items()
              if key.startswith(('cwgg_g_', 'cwsec_g_'))}
    check(actual == expected, w.id + ': open presentation differs from unconditional calculation')
    check(optimized.display_operations == baseline.display_operations, w.id + ': open refresh arithmetic changed')
    per_window_operations[w.id] = optimized.display_operations

for ai in (False, True):
    for opened in (False, True):
        m = machine(ai, opened)
        untouched = deepcopy(m.countries['USA'])
        for w in WINDOWS:
            m.call(f'{P}_{w.id[5:]}_gui_refresh')
        check(m.get('gui_test_border_samples') == 1, f'{ai}/{opened}: border runtime lost')
        check(m.get('cwgg_u_agreed') == 3, f'{ai}/{opened}: unity chapter count lost')
        check(m.countries['USA'] == untouched, f'{ai}/{opened}: another player country changed')
        check(m.countries['global'].variables == {'treasury': V.D(100), 'population_total': V.D(10),
                                                 'gdp_per_capita': V.D(2), 'num_days': V.D(100)},
              f'{ai}/{opened}: country refresh wrote global data')
        check((m.display_operations > 0) == (opened and not ai), f'{ai}/{opened}: offscreen/AI arithmetic')
        for w in WINDOWS:
            check(m.get(w.gui_dirty) == (0 if ai else 1), f'{ai}/{opened}: own dirty counter')
        if not ai and opened:
            check(m.get('cwgg_g_marker') == 454, 'opening did not calculate climate marker')
            check(m.get('cwgg_g_scales') == 13, 'opening did not calculate security scales')
            savings['open_human_display_operations'] = m.display_operations

# Opening a legacy save with stale geometry and no country dirty counters must
# calculate current values immediately; tab/close changes must remain visible.
for w in WINDOWS:
    m = machine()
    other = next(other for other in WINDOWS if other is not w)
    m.root.variables[w.tabvar] = V.D(99)
    m.root.variables['cwgg_g_marker'] = V.D(-99)
    m.countries['global'].variables['cwgg_gui_dirty'] = V.D(456)
    click(m, w, 'topbar', 'topbar_bg')
    check(w.flag in m.root.flags, w.id + ': opening flag')
    check(m.get(w.tabvar) == 1, w.id + ': invalid saved tab was not reset')
    check(m.display_operations > 0, w.id + ': opening did not rebuild geometry')
    check(m.get(w.gui_dirty) > 0, w.id + ': opening did not invalidate saved GUI')
    check(m.get(other.gui_dirty) == 0, w.id + ': opening invalidated another window')
    before = m.get(w.gui_dirty)
    click(m, w, 'main', 'tab_2_button')
    check(m.get(w.tabvar) == 2 and m.get(w.gui_dirty) > before, w.id + ': tab click stale')
    check(m.get(other.gui_dirty) == 0, w.id + ': tab invalidated another window')
    before = m.get(w.gui_dirty)
    click(m, w, 'main', 'close_button')
    check(w.flag not in m.root.flags and m.get(w.gui_dirty) > before, w.id + ': close stale')
    operations = m.display_operations
    m.call(f'{P}_{w.id[5:]}_gui_refresh')
    check(m.display_operations == operations, w.id + ': closed window still calculated geometry')
    click(m, w, 'topbar', 'topbar_bg')
    check(w.flag in m.root.flags and m.display_operations > operations, w.id + ': reopening stale')

# Topbar hostage countdown survives a closed security window; it is also clamped
# after an expired deadline. Actual source data changes refresh open geometry.
m = machine()
m.root.flags[P + '_hostage_ultimatum'] = V.D(0)
for end, expected in ((117, 17), (97, 0)):
    m.root.variables['cwsec_ult_end'] = V.D(end)
    m.call(P + '_sec_gui_refresh')
    check(m.get('cwsec_ult_days') == expected, 'closed topbar hostage deadline stale')
    check(m.display_operations == 0, 'closed topbar calculated full security window')
m.root.flags['cwgg_open'] = V.D(0)
m.root.variables['cwgg_klima'] = V.D(-50)
m.call(P + '_rv_gui_refresh')
check(m.get('cwgg_g_marker') == 244, 'action refresh left source change stale')

# Cross-country events enter GER from a DDR ROOT. The country variable writes
# must follow the effect scope; GUI ROOT is the player_context country instead.
m = machine()
m.root = m.countries['DDR']
m.current = m.countries['GER']
m.call(P + '_rv_gui_refresh')
check(m.countries['GER'].variables['cwgg_rv_gui_dirty'] == 1, 'foreign event missed German dirty counter')
check('cwgg_rv_gui_dirty' not in m.countries['DDR'].variables, 'foreign event dirtied DDR player GUI')

# IMPERIA COLD WAR — Politics launchers remain independent of the economy bar.
m = machine(open_windows=True)
m.countries['DDR'].exists = False
m.countries['global'].flags[P + '_unity_achieved'] = V.D(0)
for w in WINDOWS:
    m.call(f'{P}_{w.id[5:]}_gui_refresh')
    check(m.test(V.first(GUIS[w.id + '_topbar'], 'visible')), w.id + ': topbar visibility changed')
    check(m.test(V.first(GUIS[w.id + '_main'], 'visible')), w.id + ': open visibility changed')
m.root.flags['hide_money'] = V.D(0)
for w in WINDOWS:
    node=GUIS[w.id + '_topbar']
    check(m.test(V.first(node, 'visible')), w.id + ': economy bar hid politics launcher')
    check(V.first(node,'parent_window_token')=='politics_tab',w.id+': launcher outside politics panel')

# Every emitted main/bar/topbar GUI uses its own country counter, including child
# bars with parent_scripted_gui. No AI cycle can invalidate other clients.
for w in WINDOWS:
    entries = [body for key, body in GUIS.items() if key.startswith(w.id + '_')]
    check(len(entries) == 2 + len(w.bars), w.id + ': missing GUI block')
    for body in entries:
        check(V.first(body, 'dirty') == 'ROOT.' + w.gui_dirty, w.id + ': shared/global dirty counter')
check('global.cwgg_gui_dirty' not in refresh_text + scripted_gui_text, 'global dirty contract remains')

print(json.dumps({'checks': checks, 'display_operations_per_open_refresh': per_window_operations,
                  'display_operations': savings,
                  'closed_or_ai_display_operations': 0, 'errors': []}, indent=2))
