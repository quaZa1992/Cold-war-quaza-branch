# IMPERIA COLD WAR — Israel 1970 rework regression checks.
"""Bounded checks against emitted Clausewitz AST, not a native HOI4 test.

The small evaluator interprets the emitted guards and transactions. Native
staffing, province control and building-capacity predicates are explicit fixture
inputs; the native money helpers are represented by treasury/debt adapters.
Unrecognised commands fail instead of silently passing. This does not emulate
the economy, event scheduler, tooltip renderer, saves or multiplayer engine.
"""
from pathlib import Path
import copy
import hashlib
import json
import re

from script_format import read

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCES = [
    'tools/israel_1970/english_design.json',
    'common/national_focus/ISR70_focus.txt',
    'common/ideas/ISR70_ideas.txt',
    'common/scripted_effects/ISR70_policy_effects.txt',
    'common/scripted_triggers/ISR70_policy_triggers.txt',
    'common/decisions/ISR70_policy_decisions.txt',
    'events/ISR70_policy_events.txt',
    'common/scripted_effects/00_money_system.txt',
]
TEXT = {p: (ROOT / p).read_text(encoding='utf-8-sig') for p in SOURCES}
DATA = json.loads(TEXT[SOURCES[0]])
ERRORS = []
CHECKS = []


def check(ok, label):
    CHECKS.append(label)
    if not ok:
        ERRORS.append(label)


def scalar(block, key, default=None):
    return next((v for k, op, v in block if k == key and not isinstance(v, list)), default)


def child(block, key, default=None):
    return next((v for k, op, v in block if k == key and isinstance(v, list)), default)


def walk(block):
    for k, op, v in block:
        yield k, op, v
        if isinstance(v, list):
            yield from walk(v)


def root_blocks(path):
    return {k: v for k, op, v in read(TEXT[path]) if isinstance(v, list)}


EFFECTS = root_blocks(SOURCES[3])
TRIGGERS = root_blocks(SOURCES[4])
DECISIONS = child(read(TEXT[SOURCES[5]]), 'ISR70_policy_category')
DECISIONS = {k: v for k, op, v in DECISIONS if isinstance(v, list)}
EVENTS = {scalar(v, 'id'): v for k, op, v in read(TEXT[SOURCES[6]]) if k == 'country_event'}
FOCUSES = child(read(TEXT[SOURCES[1]]), 'focus_tree')
FOCUSES = {scalar(v, 'id'): v for k, op, v in FOCUSES if k == 'focus'}


class Fixture:
    """An intentionally narrow interpreter of current emitted transaction AST."""

    def __init__(self):
        self.vars = {'treasury': 1000., 'debt': 20., 'gdp_total': 100.}
        self.flags = set()
        self.focuses = {'ISR70_diaspora_bonds', 'ISR70_absorption_reform'}
        self.ideas = set()
        self.events = []
        self.states = {s: {'owner': 'PAL', 'controller': 'ISR', 'full_control': True,
                           'capacity': True, 'slots': 0, 'buildings': {}, 'dynamic': set(),
                           'resistance': {}} for s in (208, 209)}
        self.staff = True
        self.scenario = True
        self.bankrupt = False

    def value(self, token, state=None):
        if isinstance(token, str) and token.startswith('building_level@'):
            assert state is not None, ('Building level needs a state scope', token)
            return self.states[state]['buildings'].get(token.split('@', 1)[1], 0)
        try:
            return float(token)
        except (TypeError, ValueError):
            if token not in self.vars:
                raise ValueError('Uninitialised fixture variable: ' + str(token))
            return self.vars[token]

    def condition(self, block, state=None, any_of=False):
        outcomes = []
        for k, op, v in block:
            if k.startswith('#') or k == 'tooltip':
                continue
            if k in ('AND', 'hidden_trigger', 'custom_trigger_tooltip'):
                ok = self.condition(v, state)
            elif k == 'OR':
                ok = self.condition(v, state, True)
            elif k == 'NOT':
                ok = not self.condition(v, state)
            elif k.isdigit():
                ok = self.condition(v, int(k))
            elif k in TRIGGERS:
                ok = self.condition(TRIGGERS[k], state) == (v == 'yes')
            elif k == 'ISR70_is_scenario':
                ok = self.scenario == (v == 'yes')
            elif k == 'always':
                ok = v == 'yes'
            elif k == 'has_country_flag':
                ok = v in self.flags
            elif k == 'has_completed_focus':
                ok = v in self.focuses
            elif k == 'has_variable':
                ok = v in self.vars
            elif k == 'has_idea':
                ok = v in self.ideas
            elif k == 'has_active_mission':
                assert v == 'bankruptcy_incoming_collapse', v
                ok = self.bankrupt
            elif k.startswith('can_staff_'):
                ok = self.staff
            elif k == 'is_owned_by':
                ok = self.states[state]['owner'] == v
            elif k == 'is_controlled_by':
                ok = self.states[state]['controller'] == v
            elif k == 'has_full_control_of_state':
                ok = self.states[int(v)]['full_control']
            elif k == 'free_building_slots':
                ok = self.states[state]['capacity']
            elif k == 'check_variable':
                if scalar(v, 'var'):
                    left = self.value(scalar(v, 'var'), state)
                    right = self.value(scalar(v, 'value'), state)
                    cmp = scalar(v, 'compare')
                    ok = {'greater_than': left > right,
                          'greater_than_or_equals': left >= right,
                          'less_than': left < right,
                          'less_than_or_equals': left <= right,
                          'equals': left == right}[cmp]
                else:
                    terms = [(a, b, c) for a, b, c in v if not a.startswith('#')]
                    assert len(terms) == 1, terms
                    a, b, c = terms[0]
                    left, right = self.value(a, state), self.value(c, state)
                    ok = {'>': left > right, '<': left < right, '=': left == right}[b]
            else:
                raise ValueError('Unsupported fixture condition: ' + k)
            outcomes.append(ok)
        return any(outcomes) if any_of else all(outcomes)

    def execute(self, block, state=None):
        previous_branch = None
        for k, op, v in block:
            if k.startswith('#') or k in ('custom_effect_tooltip', 'unlock_decision_tooltip', 'log'):
                continue
            if k == 'effect_tooltip':
                # Native display contract. A separate static purity check below
                # rejects providers/grants in the three new acceptance displays.
                continue
            if k in ('if', 'else_if'):
                allowed = (k == 'if' or previous_branch is False) and self.condition(child(v, 'limit', []), state)
                previous_branch = bool(allowed) or (previous_branch if k == 'else_if' else False)
                if allowed:
                    self.execute([(a, b, c) for a, b, c in v if a != 'limit'], state)
                continue
            if k == 'else':
                if previous_branch is False:
                    self.execute(v, state)
                previous_branch = None
                continue
            previous_branch = None
            adapter = getattr(self, 'native_adapter', None)
            if adapter is not None and adapter(k, v, state):
                continue
            if k == 'hidden_effect':
                self.execute(v, state)
            elif k.isdigit():
                self.execute(v, int(k))
            elif k in EFFECTS:
                assert v == 'yes', (k, v)
                self.execute(EFFECTS[k], state)
            elif k in ('set_variable', 'set_temp_variable', 'multiply_variable', 'multiply_temp_variable', 'add_to_variable'):
                terms = [(a, b, c) for a, b, c in v if a != 'tooltip']
                assert len(terms) == 1, terms
                name, _, value = terms[0]
                value = self.value(value)
                if k.startswith('multiply'):
                    self.vars[name] *= value
                elif k == 'add_to_variable':
                    self.vars[name] = self.vars.get(name, 0) + value
                else:
                    self.vars[name] = value
            elif k == 'clear_variable':
                self.vars.pop(v, None)
            elif k == 'set_country_flag':
                self.flags.add(v)
            elif k == 'clr_country_flag':
                self.flags.discard(v)
            elif k == 'modify_treasury_effect':
                self.vars['treasury'] += self.vars['treasury_change']
            elif k == 'modify_debt_effect':
                self.vars['debt'] += self.vars['debt_change']
            elif k == 'country_event':
                self.events.append((scalar(v, 'id'), int(scalar(v, 'days'))))
            elif k == 'add_ideas':
                self.ideas.add(v)
            elif k == 'add_extra_state_shared_building_slots':
                self.states[state]['slots'] += int(v)
            elif k == 'add_building_construction':
                kind, levels = scalar(v, 'type'), int(scalar(v, 'level'))
                buildings = self.states[state]['buildings']
                buildings[kind] = buildings.get(kind, 0) + levels
            elif k == 'add_dynamic_modifier':
                self.states[state]['dynamic'].add(scalar(v, 'modifier'))
            elif k == 'remove_resistance_target':
                self.states[state]['resistance'].pop(v, None)
            elif k == 'add_resistance_target':
                self.states[state]['resistance'][scalar(v, 'id')] = float(scalar(v, 'amount'))
            else:
                raise ValueError('Unsupported fixture effect: ' + k)

    def balance(self):
        return self.vars['treasury'], self.vars['debt']


def snapshot(game):
    return copy.deepcopy((game.vars, game.flags, game.ideas, game.events, game.states))


def asset_snapshot(game):
    return copy.deepcopy((game.ideas, game.states))


def slots_before_construction(block, label):
    """Each state's physical grant must have preceding slots in that same block."""
    for k, op, v in block:
        if k.isdigit() and isinstance(v, list):
            credit = 0
            for command, _, payload in v:
                if command == 'add_extra_state_shared_building_slots':
                    credit += int(payload)
                if command == 'add_building_construction':
                    credit -= int(scalar(payload, 'level'))
                    check(credit >= 0, label + ': slots precede ' + scalar(payload, 'type'))
        if isinstance(v, list):
            slots_before_construction(v, label)


def main():
    revision = DATA['settlement_revision']
    check(revision.get('project') == 'IMPERIA COLD WAR', 'Project identity is recorded')
    nodes = {n['id']: n for n in DATA['nodes']}
    workforce = {n['id']: n['modifiers']['total_workforce_modifier'] for n in DATA['nodes']
                 if 'total_workforce_modifier' in n.get('modifiers', {})}
    check(abs(sum(max(v, 0) for v in workforce.values()) - .15) < 1e-8,
          'All focus workforce bonuses total exactly +15%')
    check(all(v >= 0 for v in workforce.values()), 'No negative workforce modifier in the reworked focus catalogue')
    ideas = child(child(read(TEXT[SOURCES[2]]), 'ideas'), 'country')
    emitted_workforce = [float(v) for k, op, v in walk(ideas) if k == 'total_workforce_modifier']
    check(abs(sum(emitted_workforce) - .15) < 1e-8 and all(v >= 0 for v in emitted_workforce),
          'Emitted Israeli spirit workforce bonuses also total +15% with no negatives')
    readers = TEXT[SOURCES[7]]
    for key in ('total_workforce_modifier', 'offices_productivity', 'civilian_factories_productivity',
                'agricolture_productivity_modifier'):
        check('modifier@' + key in readers, 'Native economy consumes ' + key)

    finance = [
        ('diaspora_development_bonds', .08, .08),
        ('uja_absorption_campaign', .04, 0),
    ]
    for name, cash, debt in finance:
        decision = DECISIONS['ISR70_policy_decision_' + name]
        game = Fixture()
        before = game.balance()
        game.execute(child(decision, 'complete_effect'))
        check(all(abs(a-b-c) < 1e-8 for a,b,c in zip(game.balance(), before, (100*cash, 100*debt))),
              name + ': actual hidden effects have the correct treasury/debt deltas')
        check('ISR70_policy_' + name + '_done' in game.flags, name + ': completion stores its receipt')
        game.vars['gdp_total'] = 900
        changed = snapshot(game)
        game.execute(child(decision, 'complete_effect'))
        check(snapshot(game) == changed, name + ': duplicate completion cannot repeat proceeds at changed GDP')
        game = Fixture()
        game.focuses.clear()
        before = snapshot(game)
        game.execute(child(decision, 'complete_effect'))
        check(snapshot(game) == before, name + ': missing prerequisite blocks actual payment')

    extensions = revision['extensions']
    check(len(extensions) == 6 and set(revision['states']) == {208,209}, 'Exactly six settlement extension projects')
    for state in (208,209):
        check(sorted(s['phase'] for s in extensions if s['state'] == state) == [1,2,3],
              str(state) + ': exactly three extension phases')
    projects = {p['key']: p for p in DATA['policy_expansion']['projects']}
    for extension in extensions:
        key = extension['key']
        p = projects[key]
        state = extension['state']
        phase = extension['phase']
        start = EFFECTS['ISR70_policy_start_' + key]
        callback = child(EVENTS[p['callback']], 'immediate')
        active = 'ISR70_policy_project_' + key + '_active'
        previous = 'entrench_network_' + str(state) if phase == 1 else f'settlement_extension_{phase-1}_{state}'

        def seeded():
            game = Fixture()
            game.flags.update(('ISR70_policy_target_' + str(state), 'ISR70_policy_settlement_unilateral',
                               'ISR70_policy_project_' + previous + '_done'))
            game.execute(EFFECTS['ISR70_policy_refresh_costs'])
            return game

        start_terms = {(k, v) for k, op, v in walk(start) if not isinstance(v, list)}
        check(('is_owned_by','PAL') in start_terms and ('is_controlled_by','ISR') in start_terms,
              key + ': emitted start checks actual owner and controller')
        check(('has_country_flag',p['done']) in start_terms and ('has_country_flag',active) in start_terms,
              key + ': emitted start contains done and active checks')
        slots_before_construction(callback, key)
        game = seeded()
        game.execute(start)
        quote = game.vars[p['paid']]
        check(abs(quote-100*p['share']) < 1e-8 and abs(game.vars['treasury']-(1000-quote)) < 1e-8,
              key + ': emitted start reserves and pays the quoted budget')
        check(active in game.flags and game.events == [(p['callback'],p['days'])], key + ': callback is scheduled once')
        waiting = snapshot(game)
        game.execute(start)
        check(snapshot(game) == waiting, key + ': duplicate start is inert')
        game.vars['gdp_total'] = 700
        game.execute(EFFECTS['ISR70_policy_refresh_costs'])
        before_cash = game.vars['treasury']
        game.execute(callback)
        check(game.vars['treasury'] == before_cash and p['done'] in game.flags and active not in game.flags
              and p['paid'] not in game.vars, key + ': delivery completes without another charge and clears reservation')
        expected = {b['type']: b['levels'] for b in p['buildings']}
        check(game.states[state]['buildings'] == expected and game.states[state]['slots'] == p['slot_total'],
              key + ': actual callback grants exactly the recorded buildings and slots')
        delivered = snapshot(game)
        game.execute(callback)
        game.execute(start)
        check(snapshot(game) == delivered, key + ': duplicate callback and restart cannot replay assets')

        failures = ('control','owner','ceiling','capacity','staff','province_control','target')
        for failure in failures:
            game = seeded()
            game.execute(start)
            game.vars['gdp_total'] = 700
            game.execute(EFFECTS['ISR70_policy_refresh_costs'])
            if failure == 'control': game.states[state]['controller'] = 'PAL'
            if failure == 'owner': game.states[state]['owner'] = 'ISR'
            if failure == 'ceiling': game.flags.add('ISR70_policy_binding_settlement_ceiling')
            if failure == 'capacity': game.states[state]['capacity'] = False
            if failure == 'staff': game.staff = False
            if failure == 'province_control': game.states[state]['full_control'] = False
            if failure == 'target': game.flags.discard('ISR70_policy_target_' + str(state))
            assets = asset_snapshot(game)
            game.execute(callback)
            check(abs(game.vars['treasury']-1000) < 1e-8 and asset_snapshot(game) == assets
                  and p['done'] not in game.flags and active not in game.flags and p['paid'] not in game.vars,
                  key + ': ' + failure + ' failure refunds original reservation and grants no assets')
            refunded = snapshot(game)
            game.execute(callback)
            check(snapshot(game) == refunded, key + ': duplicate ' + failure + ' callback cannot refund twice')
        for failure in ('target','ceiling','owner','control','poor','previous','scenario','bankruptcy'):
            game = seeded()
            if failure == 'target': game.flags.discard('ISR70_policy_target_' + str(state))
            if failure == 'ceiling': game.flags.add('ISR70_policy_binding_settlement_ceiling')
            if failure == 'owner': game.states[state]['owner'] = 'ISR'
            if failure == 'control': game.states[state]['controller'] = 'PAL'
            if failure == 'poor': game.vars['treasury'] = 0
            if failure == 'previous': game.flags.discard('ISR70_policy_project_' + previous + '_done')
            if failure == 'scenario': game.scenario = False
            if failure == 'bankruptcy': game.bankrupt = True
            before = snapshot(game)
            game.execute(start)
            check(snapshot(game) == before, key + ': invalid ' + failure + ' start is inert')

    for state in (208,209):
        # Reach the later phases from the actual earlier callback receipts rather
        # than seeding their predecessors independently.
        game = Fixture()
        game.flags.update(('ISR70_policy_target_'+str(state), 'ISR70_policy_settlement_unilateral',
                           'ISR70_policy_project_entrench_network_'+str(state)+'_done'))
        game.execute(EFFECTS['ISR70_policy_refresh_costs'])
        for extension in sorted((e for e in extensions if e['state']==state), key=lambda e:e['phase']):
            p = projects[extension['key']]
            game.execute(EFFECTS['ISR70_policy_start_'+p['key']])
            game.execute(child(EVENTS[p['callback']],'immediate'))
        check(game.states[state]['buildings'] == {'agriculture_district':3,'infrastructure':3,'bunker':3}
              and game.states[state]['slots'] == 9,
              str(state)+': three phases are reachable sequentially from their actual completion receipts')
        other = 209 if state == 208 else 208
        # Even with the other perimeter prepared, the selected-area flag remains
        # necessary. No implicit second three-phase route is available.
        game.flags.add('ISR70_policy_project_entrench_network_'+str(other)+'_done')
        before = snapshot(game)
        game.execute(EFFECTS[f'ISR70_policy_start_settlement_extension_1_{other}'])
        check(snapshot(game) == before, str(state)+': selected area does not unlock the other territory')

    # These particular offer-display blocks have the stricter pure-display
    # contract: only temporary arithmetic and dummy-variable tooltip rows.
    forbidden = {'modify_treasury_effect','modify_debt_effect','add_ideas','remove_ideas',
                 'add_dynamic_modifier','add_building_construction','add_extra_state_shared_building_slots',
                 'set_country_flag','clr_country_flag','add_resistance_target','remove_resistance_target'}
    for key, event_id in (('freeze_new','ISR70P.401'),('land_compact','ISR70P.402'),
                          ('settlement_compensation','ISR70P.403')):
        for location, block in [('focus helper', EFFECTS['ISR70_policy_complete_' + key]),
                                ('acceptance option', child(EVENTS[event_id],'option'))]:
            displays = [v for k, op, v in block if k == 'effect_tooltip']
            check(bool(displays), key + ': ' + location + ' has prospective effects')
            for preview in displays:
                terms = list(walk(preview))
                check(not any(k in forbidden or k in EFFECTS for k,op,v in terms),
                      key + ': ' + location + ' preview has no real provider or grant')
                for command, op, payload in terms:
                    if command == 'add_to_variable':
                        targets = [k for k, _, _ in payload if k != 'tooltip']
                        check(all(k.startswith('ISR70_display_') for k in targets),
                              key + ': preview variables are isolated dummy rows')

    for focus_id, block in FOCUSES.items():
        slots_before_construction(child(block,'completion_reward',[]), focus_id)

    nodes={n['id']:n for n in DATA['nodes']}
    check(nodes['ISR70_territorial_policy']['prerequisites']==[['ISR70_january_1970']],
          'civil territorial policy opens independently from historical military outcomes')
    check(nodes['ISR70_rogers']['prerequisites']==[['ISR70_suez']],
          'negotiations can open before choosing a military confrontation policy')
    for key in ('ISR70_land_survey','ISR70_gi_resident_status'):
        check(nodes[key]['prerequisites']==[['ISR70_territorial_policy']],
              key+': settlement and civil-status choices do not require maximalist retention')
    check(not any('Rogers' in n['label'] for n in DATA['nodes']),
          'no mandatory named Rogers initiative in the player focus labels')
    check('ISR70_armed_stalemate' not in nodes['ISR70_ceasefire']['mutually_exclusive'],
          'a defensive posture does not permanently block a later accepted truce')
    for key in ('ISR70_golda_succession','ISR70_golda_panthers'):
        check('date ' not in nodes[key]['available'],key+': selectable domestic initiative has no forced historical calendar')
    check('ISR70_policy_decision_renew_ceasefire_talks' in DECISIONS,
          'inconclusive or refused ceasefire negotiations can be renewed')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        ERRORS.append(type(exc).__name__ + ': ' + str(exc))
    report = {
        'project': 'IMPERIA COLD WAR',
        'status': 'FAIL' if ERRORS else 'PASS',
        'checks': len(CHECKS),
        'errors': ERRORS,
        'passed': [c for c in CHECKS if c not in ERRORS],
        'source_sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES},
        'method': 'Emitted-AST transaction evaluation with explicit native-leaf fixtures; static economy-reader and preview checks.',
        'limitations': ['No native HOI4 execution, UI, save or multiplayer test.',
                        'Staffing, province control and capacity are supplied predicate outcomes, not a native building model.',
                        'Treasury/debt providers are fixture adapters; interest and weekly budget ticks are not simulated.',
                        'The three new acceptance displays are checked; this does not certify every legacy bilateral offer.'],
        'runtime_test': False,
    }
    target = ROOT/'docs/israel_1970_design/rework_validation.json'
    target.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','passed')}, indent=2))
    raise SystemExit(bool(ERRORS))
