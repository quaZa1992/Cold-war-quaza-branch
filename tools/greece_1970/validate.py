# IMPERIA CW — Cold War: greece 1970 — validate.
"""Structural checks and executable state-machine tests, not an engine test."""
from pathlib import Path
import importlib.util
import json
import re
import hashlib
from collections import defaultdict
from rewards import apply_rewards
from layout import apply_layout

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('native_parser', ROOT / 'tools/cyprus_1970/validate.py')
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)
parse, first, vals, walk = parser.parse, parser.first, parser.vals, parser.walk
P = 'COLDWAR_GRE_1970_'
M = json.loads((HERE / 'manifest.json').read_text())
D = json.loads((ROOT / 'docs/greece_1970_design/coldwar_greece_1970_design.json').read_text())
REWARD_REVIEW = apply_rewards(D)
LAYOUT = apply_layout(D)
AST = {r: parse((ROOT / r).read_text(encoding='utf-8-sig')) for r in M['generated'] if r.endswith(('.txt', '.gfx'))}
EFFECTS = dict((k, v) for k, op, v in AST['common/scripted_effects/COLDWAR_GRE_1970_tree_effects.txt'])
EVENTS = {first(e, 'id'): e for e in vals(AST['events/COLDWAR_GRE_1970_tree_events.txt'], 'country_event')}
TREE = first(AST['common/national_focus/COLDWAR_GRE_1970_focus.txt'], 'focus_tree')
FOCUSES = {first(f, 'id'): f for f in vals(TREE, 'focus')}
ERRORS = []
CASES = []
BOUNDS = {}


def check(ok, message):
    if not ok: ERRORS.append(message)


class World:
    """Interpret the emitted native subset with explicit countries and clocks."""
    def __init__(self, scenario=True):
        self.scenario = scenario
        self.date = (1970, 1, 1)
        self.queue = []
        self.scheduled = []
        self.changes = []
        self.countries = {tag: dict(flags=set(), ideas=set(), timed=set(), done=set(), variables={'gdp_total': 100, 'treasury': 20, 'debt': 0, 'ruling_party': 22 if tag == 'GRE' else 1, 'imp_oil_factor_t': 20}, temp={}, pp=0, stability=0, xp=0, leader='Georgios Papadopoulos', builds=[], modifiers=set(), elections=False, tree=None, war=False) for tag in ('GRE', 'ENG', 'USA', 'CYP', 'TUR', 'SER', 'SOV')}
        self.states = {str(s): dict(owner='GRE', controller='GRE', slots=True, modifiers=set(), builds=[]) for s in (139, 140, 141, 142, 143, 144, 974, 1062)}

    def env(self, scope):
        return self.countries[scope] if scope in self.countries else self.states[scope]

    def value(self, value, scope):
        if isinstance(value, list): raise AssertionError('Unexpected expression ' + repr(value))
        try: return float(value)
        except ValueError: pass
        if '.' in value and value.split('.')[0] in self.countries:
            target, key = value.split('.', 1)
            return self.value(key, target)
        e = self.env(scope)
        return e.get('temp', {}).get(value, e.get('variables', {}).get(value, 0))

    def condition(self, tree, scope='GRE'):
        def item(k, op, v):
            e = self.env(scope)
            if k == 'OR': return any(item(*x) for x in v)
            if k in ('AND','hidden_trigger'): return self.condition(v, scope)
            if k == 'NOT': return not self.condition(v, scope)
            if k in self.countries or k in self.states: return self.condition(v, k)
            if k == 'original_tag': return scope == v
            if k == 'exists': return v == 'yes'
            if k == 'country_exists': return v in self.countries
            if k == 'IMP_is_1970_scenario': return self.scenario == (v == 'yes')
            if k == 'has_country_flag': return v in e['flags']
            if k == 'has_idea': return v in e['ideas']
            if k == 'has_completed_focus': return v in e['done']
            if k == 'has_variable': return v in e['variables']
            if k == 'has_war': return e['war'] == (v == 'yes')
            if k == 'has_elections': return e['elections'] == (v == 'yes')
            if k == 'has_country_leader': return json.loads(first(v, 'name')) == e['leader']
            if k in ('owns_state', 'controls_state'): return self.states[v]['owner' if k == 'owns_state' else 'controller'] == scope
            if k == 'any_owned_state': return any(state['owner']==scope and self.condition(v,identifier) for identifier,state in self.states.items())
            if k in ('is_owned_by', 'is_controlled_by'): return e['owner' if k == 'is_owned_by' else 'controller'] == ('GRE' if v=='ROOT' else v)
            if k == 'free_building_slots': return e['slots']
            if k == 'check_variable':
                if first(v, 'var') is not None:
                    a, b = self.value(first(v, 'var'), scope), self.value(first(v, 'value'), scope)
                    cmp = first(v, 'compare', 'greater_than_or_equals')
                    return {'equals': a == b, 'greater_than_or_equals': a >= b, 'less_than_or_equals': a <= b, 'greater_than': a > b, 'less_than': a < b}[cmp]
                return all(self.value(a, scope) == self.value(b, scope) if cmp == '=' else self.value(a, scope) > self.value(b, scope) if cmp == '>' else self.value(a, scope) < self.value(b, scope) for a, cmp, b in v)
            if k == 'date': return self.date > tuple(map(int, v.split('.'))) if op == '>' else self.date < tuple(map(int, v.split('.')))
            raise AssertionError('Uninterpreted trigger ' + k)
        return all(item(*x) for x in tree)

    def execute(self, tree, scope='GRE', depth=0):
        assert depth < 30, 'Recursive effects'
        chain = False
        for k, op, v in tree:
            e = self.env(scope)
            if k in ('if', 'else_if', 'else'):
                if k == 'if': chain = False
                if not chain and (k == 'else' or self.condition(first(v, 'limit', []), scope)):
                    self.execute([(a, b, c) for a, b, c in v if a != 'limit'], scope, depth + 1)
                    chain = True
            elif k in EFFECTS: self.execute(EFFECTS[k], scope, depth + 1)
            elif k in self.countries or k in self.states: self.execute(v, k, depth + 1)
            elif k == 'set_country_flag': e['flags'].add(first(v, 'flag') if isinstance(v, list) else v)
            elif k == 'clr_country_flag': e['flags'].discard(v)
            elif k in ('add_ideas', 'remove_ideas'):
                (e['ideas'].add if k == 'add_ideas' else e['ideas'].discard)(v)
            elif k == 'add_timed_idea':
                e['ideas'].add(first(v, 'idea')); e['timed'].add(first(v, 'idea'))
            elif k == 'swap_ideas':
                e['ideas'].discard(first(v, 'remove_idea')); e['ideas'].add(first(v, 'add_idea'))
            elif k == 'country_event': self.queue.append((scope, first(v, 'id')))
            elif k in ('set_variable', 'set_temp_variable', 'multiply_variable', 'multiply_temp_variable', 'add_to_variable', 'subtract_from_variable'):
                store = e['temp'] if 'temp' in k else e['variables']
                if first(v, 'var') is not None: a, b = first(v, 'var'), first(v, 'value')
                else: a, _, b = v[0]
                value = self.value(b, scope)
                store[a] = store.get(a, 0) * value if 'multiply' in k else store.get(a, 0) + value if k == 'add_to_variable' else store.get(a, 0) - value if k == 'subtract_from_variable' else value
            elif k == 'modify_treasury_effect':
                change = self.value('treasury_change', scope)
                e['variables']['treasury'] += change
                self.changes.append((scope, change))
            elif k == 'modify_debt_effect': e['variables']['debt'] += self.value('debt_change', scope)
            elif k == 'modify_corporate_tax_rate_effect': e['variables']['corporate_tax_rate'] = max(0, min(50, self.value('corporate_tax_rate', scope) + self.value('corp_change', scope)))
            elif k == 'change_ruling_party_effect':
                party = self.value('rul_party_temp', scope)
                e['variables']['ruling_party'] = party
                e['elections'] = self.value('disable_elections', scope) == 0
                leaders = {1: 'Panagiotis Kanellopoulos', 2: 'Georgios Mavros', 3: 'Andreas Papandreou', 4: 'Kostas Koligiannis', 22: 'Georgios Papadopoulos', 23: 'Constantine II'}
                e['leader'] = 'Dimitrios Ioannidis' if P + 'selected_ioannidis' in e['flags'] else leaders[party]
            elif k == 'add_tech_bonus': e.setdefault('research', []).append(v)
            elif k == 'custom_effect_tooltip': pass
            elif k == 'decrease_corruption':
                for i in range(10, 1, -1):
                    if 'corruption_level_' + str(i).zfill(2) in e['ideas']:
                        e['ideas'].remove('corruption_level_' + str(i).zfill(2))
                        e['ideas'].add('corruption_level_' + str(i - 1).zfill(2)); break
            elif k == 'add_political_power': e['pp'] += float(v)
            elif k == 'add_stability': e['stability'] += float(v)
            elif k.endswith('_experience'): e['xp'] += float(v)
            elif k == 'load_focus_tree': e['tree'] = v
            elif k == 'add_building_construction': e['builds'].append(v)
            elif k == 'random_owned_controlled_state':
                eligible=[identifier for identifier,state in self.states.items() if state['owner']==scope and state['controller']==scope and self.condition(first(v,'limit',[]),identifier)]
                if eligible:self.execute([(a,b,c) for a,b,c in v if a!='limit'],eligible[0],depth+1)
            elif k == 'add_dynamic_modifier': e['modifiers'].add(first(v, 'modifier'))
            elif k == 'remove_dynamic_modifier': e['modifiers'].discard(v)
            elif k == 'clamp_variable':
                a = first(v, 'var'); e['variables'][a] = max(float(first(v, 'min')), min(float(first(v, 'max')), self.value(a, scope)))
            elif k == 'COLDWAR_CYP_1970_GRE_publish_response':
                if self.scenario and 'COLDWAR_CYP_1970_crisis_active' in self.countries['CYP']['flags']:
                    self.countries['CYP']['flags'].add('COLDWAR_CYP_1970_guarantor_response_recorded')
            else: raise AssertionError('Uninterpreted effect ' + k)

    def call(self, key): self.execute(EFFECTS[P + key])

    def complete(self, key):
        fid = P + key
        f = FOCUSES[fid]
        assert self.condition(first(f, 'available')), 'Unavailable ' + key
        for group in vals(f, 'prerequisite'):
            assert any(v in self.countries['GRE']['done'] for k, op, v in group), 'Missing prerequisite ' + key
        assert not any(v in self.countries['GRE']['done'] for g in vals(f, 'mutually_exclusive') for k, op, v in g), 'Excluded ' + key
        self.countries['GRE']['done'].add(fid)
        self.execute(first(f, 'completion_reward'))

    def answer(self, num, index=0):
        eid = 'COLDWAR_GRE_TREE.' + str(num)
        i = next(i for i, (_, eventid) in enumerate(self.queue) if eventid == eid)
        scope, _ = self.queue.pop(i)
        e = EVENTS[eid]
        assert self.condition(first(e, 'trigger', []), scope), 'Event is stale: ' + eid
        opt = vals(e, 'option')[index]
        assert self.condition(first(opt, 'trigger', []), scope), 'Option unavailable'
        self.execute([(k, op, v) for k, op, v in opt if k not in ('name', 'trigger', 'ai_chance')], scope)


def structures():
    check(len(FOCUSES) == 313, 'Expected 313 focuses')
    check(hashlib.sha256((ROOT / 'docs/greece_1970_design/coldwar_greece_1970_design.json').read_bytes()).hexdigest() == M['design_sha256'], 'Design changed after compile')
    for n in D['focuses']:
        f = FOCUSES[n['id']]
        check((float(first(f, 'x')), float(first(f, 'y'))) == (n['x'], n['y']), 'Geometry changed: ' + n['id'])
        check(abs(float(first(f, 'cost')) * 7 - n['days']) < .001, 'Duration changed: ' + n['id'])
        check([vals(g, 'focus') for g in vals(f, 'prerequisite')] == n['prerequisite_groups'], 'Prerequisites changed: ' + n['id'])
        check(set(vals(first(f, 'mutually_exclusive', []), 'focus')) == set(n['excludes']), 'Exclusions changed: ' + n['id'])
    raw = (ROOT / 'localisation/english/COLDWAR_GRE_1970_tree_l_english.yml').read_bytes()
    check(raw.startswith(b'\xef\xbb\xbf'), 'Missing localisation BOM')
    pairs = re.findall(r'^ (\S+):0 (".*")$', raw.decode('utf-8-sig'), re.M)
    local = {k: json.loads(v) for k, v in pairs}
    check(len(pairs) == len(local), 'Duplicate localisation')
    all_effects = set()
    for path in (ROOT / 'common/scripted_effects').glob('*.txt'):
        all_effects.update(re.findall(r'^([\w]+)\s*=\s*\{', path.read_text(encoding='utf-8-sig'), re.M))
    all_ideas = set(re.findall(r'^\s*([\w]+)\s*=\s*\{', '\n'.join(p.read_text(encoding='utf-8-sig') for p in (ROOT / 'common/ideas').glob('*.txt')), re.M))
    all_events = set(re.findall(r'\bid\s*=\s*(\w+\.\d+)', '\n'.join(p.read_text(encoding='utf-8-sig') for p in (ROOT / 'events').glob('*.txt'))))
    sprites = {json.loads(v) for tree in AST.values() for k, op, v in walk(tree) if k == 'name' and isinstance(v, str) and v.startswith('"GFX_')}
    for rel, tree in AST.items():
        for k, op, v in walk(tree):
            if k in ('texturefile', 'animationmaskfile', 'animationtexturefile'):
                source = json.loads(v)
                check((ROOT / source).exists() or (Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV') / source).exists(), 'Missing texture: ' + v)
            if k in ('add_ideas', 'remove_ideas', 'remove_idea', 'add_idea', 'idea') and isinstance(v, str):
                check(v in all_ideas, 'Undefined idea: ' + v)
            if k.startswith(P) and v == 'yes': check(k in all_effects, 'Undefined scripted effect: ' + k)
            if k == 'id' and v.startswith('COLDWAR_GRE_TREE.'): check(v in all_events, 'Undefined event: ' + v)
            if k in ('title', 'desc', 'name', 'custom_effect_tooltip') and isinstance(v, str) and v.startswith(P): check(v in local, 'Missing localisation: ' + v)
            if k == 'icon' and v.startswith('GFX_' + P): check(v in sprites, 'Missing icon: ' + v)
    for iid in all_ideas:
        if iid.startswith(P):
            check(iid in local, 'Missing idea localisation: ' + iid)
            check('GFX_idea_' + iid in sprites, 'Missing idea icon: ' + iid)
    # New flag gates must have a producer in this feature or the existing roster.
    region = (ROOT / 'common/scripted_effects/COLDWAR_GRE_1970_regional_effects.txt').read_text()
    text = '\n'.join((ROOT / r).read_text(encoding='utf-8-sig') for r in M['generated']) + region + (ROOT / 'common/decisions/COLDWAR_GRE_1970_regional_decisions.txt').read_text()
    produced = set(re.findall(r'set_country_flag\s*=\s*(?:\{\s*flag\s*=\s*)?(' + P + r'\w+)', text))
    required = set(re.findall(r'has_country_flag\s*=\s*(' + P + r'\w+)', text))
    check(not required - produced, 'Unreachable flag gates: ' + str(sorted(required - produced)))
    history = (ROOT / 'history/countries/GRE - Greece.txt').read_text()
    check('load_focus_tree = ' + P + 'focus' in history.split('2000.1.1 = {')[0], '1970 history not wired')
    fallback = (ROOT / 'common/scripted_effects/mdcw_1970_focus_tree_effects.txt').read_text()
    check('original_tag = GRE IMP_is_1970_scenario = yes' in fallback, 'Fallback can erase Greek progress')
    check(not any(k in text for k in ('declare_war_on =', 'annex_country =', 'add_to_faction =')), 'Unintended forced foreign action')
    native = '\n'.join(p.read_text(encoding='utf-8-sig') for folder in ('common/ideas', 'common/dynamic_modifiers', 'common/modifiers', 'common/country_leader') for p in (ROOT / folder).glob('*.txt') if not p.name.startswith('COLDWAR_GRE_1970'))
    used = {k for n in D['focuses'] for k in n['modifiers']} | {k for s in D['starting_spirits'] for k in s['modifiers']}
    for key in used: check(bool(re.search(r'\b' + key + r'\s*=', native)), 'Unsupported modifier: ' + key)
    catalogue = (ROOT / 'common/technology_tags/00_technology.txt').read_text()
    for n in D['focuses']:
        if n['treasury_cost_gdp_percent']:
            check(any(n.get(f) for f in ('modifiers', 'state_programme', 'research_bonuses', 'political_power', 'stability', 'xp', 'regime_package', 'transition_package', 'building', 'radar_project', 'removes')), 'Paid focus with no gameplay outcome: ' + n['key'])
        for bonus in n.get('research_bonuses', []):
            check(bool(re.search(r'\b' + bonus['category'] + r'\b', catalogue)), 'Unknown research category: ' + bonus['category'])
        if n['modifiers'] or n.get('state_programme') or n.get('research_bonuses'):
            check(n['id'] + '_programme_effects_tt' in local, 'Missing explicit effect tooltip: ' + n['key'])
    # Conservative per-stat upper bounds: sum common permanent programmes,
    # choose at most one policy per slot and one current government/regime.
    # Values are independent bounds, not one simultaneously attainable build.
    def subtotal(nodes, modifier):
        slots = defaultdict(list); total = 0
        for n in nodes:
            if n.get('duration_days'): continue
            value = max(0, n['modifiers'].get(modifier, 0))
            if n['modifier_slot']: slots[n['modifier_slot']].append(value)
            else: total += value
        return total + sum(max(v) for v in slots.values())
    cap_modifiers = {'construction_programmes': 'production_speed_buildings_factor', 'factory_efficiency_programmes': 'production_factory_max_efficiency_factor', 'army_organisation_programmes': 'army_org_factor', 'air_mission_programmes': 'air_mission_efficiency', 'research_programmes': 'research_speed_factor', 'maximum_planning_programmes': 'max_planning'}
    for cap, modifier in cap_modifiers.items():
        common = subtotal([n for n in D['focuses'] if n['party'] is None], modifier)
        parties = max(subtotal([n for n in D['focuses'] if n['section'] == s], modifier) for s in ('pap', 'ioa', 'nd', 'centre', 'pasok', 'kke', 'royal'))
        regime = max([0] + [max(0, n.get('regime_package', {}).get('modifiers', {}).get(modifier, 0)) for n in D['focuses']])
        BOUNDS[modifier] = round(common + parties + regime, 5)
        check(BOUNDS[modifier] <= D['balance_caps'][cap] + .00001, 'Programme cap exceeded: ' + modifier)


def opening():
    w = World(); w.call('tree_initialize')
    for k in ('greece_1970', 'state_dossier', 'officer_loyalties', 'civilian_contacts'): w.complete(k)
    return w


def behavioral():
    for route in ('direct', 'controlled', 'junta', 'veto', 'hardline'):
        w = opening()
        if route == 'direct':
            w.complete('civilian_transition'); w.answer(3)
            for k in ('transition_offer', 'civilian_preparation', 'legal_parties'): w.complete(k)
            w.answer(5)
        elif route == 'controlled':
            w.complete('controlled_opening'); w.answer(2); w.complete('supervised_cabinet')
            w.complete('renounce_veto'); w.answer(5); w.complete('opening_handover')
        elif route == 'junta':
            w.complete('retain_junta'); w.answer(1); w.complete('military_compact')
            for k in ('professional_compact', 'service_procurement', 'lasting_junta'): w.complete(k)
            w.answer(3); w.complete('military_exit'); w.answer(5)
        else:
            w.complete('controlled_opening'); w.answer(2); w.complete('supervised_cabinet')
            for k in ('retain_veto', 'tutelary_charter'): w.complete(k)
            if route == 'hardline':
                w.answer(4); w.complete('reverse_opening')
            w.answer(3); w.complete('military_exit'); w.answer(5)
        for k in ('civilian_institutions', 'civilian_accountability', 'open_courts'): w.complete(k)
        w.answer(6); w.complete('credible_election'); w.answer(7)
        for k in ('constitutional_question', 'civilian_enterprise', 'civilian_settlement'): w.complete(k)
        e = w.countries['GRE']
        assert P + 'civilian_order' in e['ideas']
        assert not {P + x for x in ('military_order', 'controlled_order', 'rule_by_decree', 'security_state')} & e['ideas']
        assert P + 'current_electoral_mandate_verified' in e['flags']
        assert P + 'unresolved_victim_claims' in e['ideas']
        w.complete('nd_0')
        CASES.append('Reachable civilian settlement: ' + route)
    w = opening(); e = w.countries['GRE']
    w.complete('retain_junta'); w.answer(1); w.complete('military_compact')
    w.complete('professional_compact'); w.complete('service_procurement'); w.complete('lasting_junta')
    w.answer(3, 1); w.call('tree_weekly_tick')
    assert P + 'military_order' in e['ideas'] and P + 'civilian_order' not in e['ideas']
    CASES.append('Lasting junta survives a refused handover')
    w = opening(); e = w.countries['GRE']; e['variables']['treasury'] = 0
    w.complete('civilian_transition'); w.answer(3); w.complete('transition_offer')
    assert P + 'transition_offer_granted' not in e['flags']
    assert not w.condition(first(FOCUSES[P + 'civilian_preparation'], 'available'))
    e['variables']['treasury'] = 20
    w.call('complete_transition_offer'); treasury = e['variables']['treasury']
    w.call('complete_transition_offer')
    assert e['variables']['treasury'] == treasury == 19.5
    CASES.append('Unfunded predecessor blocks descendants; retry charges once')
    w = opening(); e = w.countries['GRE']
    w.complete('economy_0'); w.complete('economy_1'); w.complete('economy_2')
    e['flags'].add(P + 'economy_3_granted'); e['flags'].add(P + 'economy_3_selected'); e['flags'].discard(P + 'economy_2_selected')
    w.call('reconcile_programmes_effect')
    assert P + 'economy_3_programme' in e['ideas'] and P + 'economy_2_programme' not in e['ideas']
    CASES.append('Reconciliation preserves a single current policy per slot')
    w = opening(); e = w.countries['GRE']; e['flags'].add(P + 'financing_gap_verified')
    w.complete('credit_review'); w.complete('credit_loan')
    eid = next(int(eid.split('.')[-1]) for scope, eid in w.queue if scope == 'USA')
    assert P + 'credit_loan_granted' not in e['flags']
    lender = w.countries['USA']['variables']['treasury']; treasury = e['variables']['treasury']
    w.answer(eid)
    assert w.countries['USA']['variables']['treasury'] == lender - 2
    assert e['variables']['treasury'] == treasury + 2 and e['variables']['debt'] == 2
    w.call('complete_credit_loan')
    assert e['variables']['debt'] == 2
    CASES.append('Credit consent balances both treasuries and Greek debt exactly once')
    w = opening(); w.complete('cyprus_0'); w.complete('cyprus_1'); w.complete('cyprus_2')
    eid = int(w.queue[-1][1].split('.')[-1]); w.answer(eid, 1)
    assert P + 'civilian_control_protocol_implemented' not in w.countries['GRE']['flags']
    assert P + 'mission_proposal_refused' in w.countries['GRE']['flags']
    assert 'COLDWAR_CYP_1970_coup_attempt_resolved' not in w.countries['CYP']['flags']
    CASES.append('Cypriot refusal creates neither agreement nor coup')
    w = opening(); w.complete('cyprus_0'); w.complete('cyprus_1'); w.complete('cyprus_2')
    e = w.countries['GRE']; e['flags'].discard(P + 'cyprus_2_live_CYP'); w.call('tree_weekly_tick')
    assert P + 'cyprus_2_timed_out_CYP' in e['flags'] and P + 'cyprus_2_accepted_CYP' not in e['flags']
    assert P + 'mission_proposal_refused' not in e['flags']
    CASES.append('No-response timeout is distinct from refusal and consent')
    w = World(False); w.call('tree_weekly_tick')
    assert not w.countries['GRE']['ideas'] and w.countries['GRE']['tree'] is None
    CASES.append('2000 scenario remains untouched')
    w = opening(); w.call('tree_initialize')
    assert P + 'oil_shock' not in w.countries['GRE']['ideas']
    w.countries['GRE']['variables']['imp_oil_factor_t'] = 100; w.call('tree_weekly_tick')
    assert P + 'oil_shock' in w.countries['GRE']['ideas']
    CASES.append('Oil penalty requires an actual price shock')
    for winner, route in ((1, 'centre'), (2, 'pasok'), (3, 'kke'), (4, 'royal')):
        w = opening(); e = w.countries['GRE']
        w.complete('civilian_transition'); w.answer(3)
        for k in ('transition_offer', 'civilian_preparation', 'legal_parties'): w.complete(k)
        w.answer(5)
        for k in ('civilian_institutions', 'civilian_retirement', 'retirement_guarantees'): w.complete(k)
        w.answer(6, winner); w.complete('credible_election'); w.answer(7); w.complete('constitutional_question')
        w.complete(route + '_0'); w.complete(route + '_1')
        if route == 'kke':
            w.answer(8); w.complete('kke_3')
            assert P + 'socialist_executive_order' in e['ideas'] and P + 'civilian_order' not in e['ideas']
        elif route == 'royal':
            w.answer(9); w.complete('royal_3'); w.complete('royal_5'); w.complete('royal_6'); w.answer(10, 1)
            assert e['variables']['ruling_party'] == 1 and P + 'civilian_order' in e['ideas']
            assert P + 'royal_executive_order' not in e['ideas']
        CASES.append('Elected party route and constitutional outcome: ' + route)
    w = opening(); e = w.countries['GRE']
    e['variables']['corporate_tax_rate'] = 49
    e['flags'].add(P + 'financing_gap_verified'); w.complete('credit_review'); w.complete('credit_taxes')
    assert e['variables']['corporate_tax_rate'] == 50 and e['variables'][P + 'tax_increment'] == 1
    e['ideas'].discard(P + 'temporary_revenue'); w.call('tree_weekly_tick')
    assert e['variables']['corporate_tax_rate'] == 49
    CASES.append('Tax sunset reverses only the actual increment at the native tax ceiling')
    w = opening(); e = w.countries['GRE']
    w.complete('cyprus_0'); w.complete('cyprus_1'); w.complete('cyprus_2')
    eid = w.queue[-1][1]
    w.countries['CYP']['variables']['COLDWAR_CYP_1970_crisis_instance'] = 1
    event = EVENTS[eid]; accept = vals(event, 'option')[0]
    assert not w.condition(first(accept, 'trigger'), 'CYP')
    w.call('send_cyprus_2'); w.answer(int(eid.split('.')[-1]))
    assert P + 'civilian_control_protocol_implemented' in e['flags']
    CASES.append('New Cyprus crisis invalidates the previous offer; a fresh offer can succeed')
    w = opening(); e = w.countries['GRE']
    e['flags'].add(P + 'civilian_transfer_implemented'); e['elections'] = True
    e['variables']['ruling_party'] = 2
    w.call('record_elected_mandate')
    assert P + 'current_electoral_mandate_verified' in e['flags'] and e['variables'][P + 'mandate_party'] == 2
    e['variables']['ruling_party'] = 22; w.call('tree_weekly_tick')
    assert P + 'current_electoral_mandate_verified' not in e['flags']
    CASES.append('Native elections renew the mandate; an unelected party change revokes it')
    w = opening(); e = w.countries['GRE']; w.complete('economy_0'); w.complete('economy_1')
    # A construction grant must recheck ownership, control, and actual capacity.
    node = next(n for n in D['focuses'] if n['building'] and n['building']['type'] == 'infrastructure')
    state = str(node['building']['state']); e['variables']['treasury'] = 20
    w.states[state]['controller'] = 'TUR'; w.call('grant_' + node['key'])
    assert not w.states[state]['builds']
    w.states[state]['controller'] = 'GRE'; w.states[state]['slots'] = False; w.call('grant_' + node['key'])
    assert not w.states[state]['builds']
    w.states[state]['slots'] = True; w.call('grant_' + node['key']); w.call('grant_' + node['key'])
    assert len(w.states[state]['builds']) == 1
    CASES.append('Construction requires owned controlled capacity and enters the normal queue once')
    w = opening(); e = w.countries['GRE']
    w.call('grant_economy_4'); balance = e['variables']['treasury']
    assert P + 'economy_4_programme' in e['ideas'] and len(e['research']) == 1
    w.call('grant_economy_4')
    assert e['variables']['treasury'] == balance and len(e['research']) == 1
    CASES.append('Paid industry standards grant productivity and one research bonus exactly once')
    w = opening(); e = w.countries['GRE']; w.call('grant_economy_10')
    assert all(P + 'economy_10_local_programme' in w.states[str(s)]['modifiers'] for s in (139, 142, 974))
    balance = e['variables']['treasury']; w.states['139']['controller'] = 'TUR'; w.call('tree_weekly_tick')
    assert P + 'economy_10_local_programme' not in w.states['139']['modifiers']
    w.states['139']['controller'] = 'GRE'; w.call('tree_weekly_tick')
    assert P + 'economy_10_local_programme' in w.states['139']['modifiers'] and e['variables']['treasury'] == balance
    CASES.append('Rural productivity applies locally and suspends under foreign occupation')
    for level in (1, 3):
        w = opening(); e = w.countries['GRE']; e['ideas'].add('corruption_level_' + str(level).zfill(2)); pp = e['pp']
        w.call('grant_economy_18'); w.call('grant_economy_18')
        assert 'corruption_level_' + str(max(1, level - 1)).zfill(2) in e['ideas'] and e['pp'] == pp
    CASES.append('Tax reform grants real revenue and at most one corruption step without a floor PP exploit')
    w = opening(); e = w.countries['GRE']; e['flags'].add(P + 'military_government_active')
    w.call('grant_pap_7'); assert P + 'pap_7_programme' in e['ideas']
    e['variables']['ruling_party'] = 1; e['leader'] = 'Panagiotis Kanellopoulos'
    e['flags'].update({P + 'civilian_transfer_implemented', P + 'current_electoral_mandate_verified'})
    w.call('grant_nd_7'); w.call('reconcile_programmes_effect')
    assert P + 'nd_7_programme' in e['ideas'] and P + 'pap_7_programme' not in e['ideas']
    e['variables']['ruling_party'] = 22; e['leader'] = 'Georgios Papadopoulos'; w.call('reconcile_programmes_effect')
    assert P + 'pap_7_programme' in e['ideas'] and P + 'nd_7_programme' not in e['ideas']
    CASES.append('Distinct government economies replace one another and restore paid policies without stacking')
    w = opening(); e = w.countries['GRE']; w.call('grant_army_10'); w.call('grant_navy_19'); w.call('grant_air_10')
    assert {P + x for x in ('army_10_programme', 'navy_19_programme', 'air_10_programme')} <= e['ideas']
    assert len(e['research']) == 3
    CASES.append('Signals, shipyards and air maintenance deliver their native modifiers and research')


def main():
    structures()
    try: behavioral()
    except (AssertionError, KeyError, StopIteration) as error:
        ERRORS.append('Behavioral failure: ' + repr(error))
        import traceback
        traceback.print_exc()
    result = {'passed': not ERRORS, 'focuses': len(FOCUSES), 'events': len(EVENTS), 'revised_reward_focuses': REWARD_REVIEW['revised_focuses'], 'native_modifier_types': len({k for n in D['focuses'] for k in n['modifiers']}), 'research_bonuses': sum(len(n.get('research_bonuses', [])) for n in D['focuses']), 'programme_upper_bounds': BOUNDS, 'layout': LAYOUT['qa'], 'behavioral_cases': CASES, 'errors': ERRORS, 'in_game_test_performed': False,
              'generated_hashes': {r: hashlib.sha256((ROOT / r).read_bytes()).hexdigest() for r in M['generated']}}
    (HERE / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'generated_hashes'}, indent=2))
    raise SystemExit(0 if result['passed'] else 1)


if __name__ == '__main__': main()
