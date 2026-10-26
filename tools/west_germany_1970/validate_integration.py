# IMPERIA CW — Cold War: selective quaZa import regression checks.
"""Exercise native POP transactions and protect the existing political registry.

This executes the authored effect AST in the established strict script harness;
it does not claim to replace a new-game HOI4 smoke test.
"""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('cwger_native_harness', ROOT / 'tools/guest_workers/validate.py')
V = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = V
spec.loader.exec_module(V)
issues = []
checks = 0


def check(ok, message):
    global checks
    checks += 1
    if not ok:
        issues.append(message)


def script(path):
    return V.parse(path.read_text(encoding='utf-8-sig'))


effects_path = ROOT / 'common/scripted_effects/COLDWAR_GER_1970_effects.txt'
effects = {key: value for key, _, value in script(effects_path)}


class MigrationMachine(V.ScriptMachine):
    # IMPERIA CW — Cold War: source events also use the native country-existence trigger.
    def test(self, body):
        return super().test([(value, '=', [('exists', '=', 'yes')])
                             if key == 'country_exists' else (key, op, value)
                             for key, op, value in body])


def migration_machine(people, valid=True, reserve_side_effect=0):
    m = MigrationMachine(effects, {})
    m.countries = {tag: V.Country(tag) for tag in ('GER', 'DDR')}
    for tag, country in m.countries.items():
        country.states = [V.State(owner=tag, controller=tag)]
    m.current = m.root = m.countries['GER']
    m.origin = m.countries['DDR']
    m.previous = m.current
    if valid == 'origin_occupied':
        m.origin.states[0].controller = 'GER'
    elif valid == 'destination_occupied':
        m.current.states[0].controller = 'DDR'
    elif valid == 'insufficient_population':
        m.origin.states[0].population = V.D(people)
    elif valid == 'origin_missing':
        m.origin.exists = False
    if reserve_side_effect:
        def hook(machine, state, delta):
            if state.owner == 'DDR' and delta < 0:
                machine.countries['DDR'].military_manpower += V.D(reserve_side_effect)
        m.state_population_hook = hook
    return m


for people in (600, 1500, 3000, 6000, 15000, 20000, 30000):
    for validity in (True, 'origin_occupied', 'destination_occupied', 'insufficient_population', 'origin_missing'):
        for reserve_side_effect in (0, 337):
            m = migration_machine(people, validity, reserve_side_effect)
            before = deepcopy(m.countries)
            m.call(f'COLDWAR_GER_1970_transfer_uebersiedler_{people}')
            success = validity is True
            for tag, sign in (('GER', 1), ('DDR', -1)):
                country, old = m.countries[tag], before[tag]
                check(country.states[0].population == old.states[0].population + (sign * people if success else 0),
                      f'{people}/{validity}: {tag} state population transaction')
                check(country.military_manpower == old.military_manpower,
                      f'{people}/{validity}: {tag} military reserve changed')
                check(country.refreshes == (1 if success else 0), f'{people}/{validity}: budget refresh')
            check(m.root.variables.get('cwger_uebersiedler_k', V.D(0)) == (V.D(people) / 1000 if success else 0),
                  f'{people}/{validity}: arrival stock')
            check(m.root.temporary.get('cwger_ue_arrived', V.D(0)) == (people if success else 0),
                  f'{people}/{validity}: successful-arrival flag')
            check('imp_refugees_taken_k' not in m.root.variables,
                  f'{people}/{validity}: native delayed refugee integration would duplicate POP')
            check(not any(k.startswith('gw_') for k in m.root.variables),
                  f'{people}/{validity}: German resettlers became guest workers')

# IMPERIA CW — Cold War: queued acceptance must not charge for a failed arrival.
exodus = next(body for kind, _, body in script(ROOT / 'events/COLDWAR_GER_1970_events.txt')
              if kind == 'country_event' and V.first(body, 'id') == 'COLDWAR_GER.130')
accept = next(body for body in V.values(exodus, 'option')
              if V.first(body, 'name') == 'COLDWAR_GER.130.a')
option_effects = [node for node in accept if node[0] not in ('name', 'ai_chance', 'trigger')]
for validity in (True, 'origin_missing', 'origin_occupied', 'destination_occupied', 'insufficient_population'):
    m = migration_machine(20000, validity)
    m.root.variables.update(gdp_total=V.D(1000), cwger_unity=V.D(17))
    m.origin.variables['cwddr_exit_pressure'] = V.D(33)
    before = deepcopy(m.countries)
    m.execute(option_effects)
    success = validity is True
    check(m.root.variables['treasury'] == before['GER'].variables['treasury'] - (1 if success else 0),
          str(validity) + ': Exodus charges without a completed arrival')
    check(m.root.variables['cwger_unity'] == 17 + (5 if success else 0),
          str(validity) + ': Exodus unity reward without a completed arrival')
    check(m.origin.variables['cwddr_exit_pressure'] == 33 + (5 if success else 0),
          str(validity) + ': Exodus pressure effect without a completed arrival')
    check(m.root.states[0].population == before['GER'].states[0].population + (20000 if success else 0),
          str(validity) + ': Exodus reception population')
    check(m.origin.states[0].population == before['DDR'].states[0].population - (20000 if success else 0),
          str(validity) + ': Exodus departure population')

# Native party files and popularity arrays remain authoritative.
registry = ROOT / 'tools/party_registry_1970/data/GER.json'
check(hashlib.sha256(registry.read_bytes()).hexdigest() ==
      '1427bdab8e264418b0fb475a270b0bdfa114099166ced84d6f40012a11cac562',
      'Existing West German party registry differs from the pre-import snapshot')
for compatibility_noop in ('setup_politics', 'assert_1969_coalition'):
    check(not effects['COLDWAR_GER_1970_' + compatibility_noop], compatibility_noop + ' must remain inert')
for native in ('party_pop_array', 'party_pop_elect_array', 'gov_coalition_array'):
    check(not any(k == 'set_variable' and isinstance(v, list) and
                  any(name.startswith(native) for name, _, _ in v) for k, _, v in V.walk(effects['COLDWAR_GER_1970_initialize'])),
          'Initialization overwrites native ' + native)
check(('set_leader_GER', '=', 'yes') in V.first(effects['COLDWAR_GER_1970_set_leader'], 'else', []),
      'Other native West German parties lost their leader provider')

# Event namespaces belong to their imported module, never the authored DDR chain.
incoming = ROOT / 'events/COLDWAR_GER_1970_events.txt'
check(not re.search(r'\bCOLDWAR_DDR(?:\.|\s*$)', incoming.read_text(encoding='utf-8'), re.M),
      'Incoming events still occupy the authored DDR namespace')
events = {}
for path in (ROOT / 'events').glob('*.txt'):
    for kind, _, body in script(path):
        if kind not in ('country_event', 'news_event', 'state_event') or not isinstance(body, list):
            continue
        event_id = V.first(body, 'id')
        if event_id:
            events.setdefault(event_id, []).append(str(path.relative_to(ROOT)))
for event_id, paths in events.items():
    if any(Path(p).name == incoming.name for p in paths):
        check(len(paths) == 1, 'Imported event collision: ' + event_id + ': ' + str(paths))

for path in HERE.rglob('*.py'):
    compile(path.read_text(encoding='utf-8-sig'), str(path), 'exec')

print(json.dumps({'checks': checks, 'errors': issues}, indent=2))
raise SystemExit(bool(issues))
