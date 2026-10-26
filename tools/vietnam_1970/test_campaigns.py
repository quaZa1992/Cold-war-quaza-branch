# IMPERIA CW — Cold War: vietnam 1970 — test campaigns.
"""Focused, fail-closed execution tests of installed campaign script AST.

Follows test_transactions.py's small-interpreter approach without importing its
report-writing test runner or either generator. This is not an HOI4 emulator.
Unimplemented trigger/effect keys raise rather than silently passing. Reports
JSON to stdout only and does not mutate game content or the baseline reports.
"""
from pathlib import Path
from dataclasses import dataclass, field
import copy
import json

from script_ast import parse, first, values, walk

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
P = 'COLDWAR_VIE_'


def read(rel):
    return parse((ROOT / rel).read_text(encoding='utf-8-sig'))


def read_campaign(folder):
    output = []
    for path in sorted((ROOT / folder).glob('COLDWAR_VIE_campaign*.txt')):
        output.extend(parse(path.read_text(encoding='utf-8-sig')))
    return output


@dataclass
class Country:
    tag: str
    gov: str = 'communism'
    exists: bool = True
    scenario: bool = True
    variables: dict = field(default_factory=lambda: {'treasury': 10., 'ruling_party': 4.})
    flags: dict = field(default_factory=dict)
    ideas: dict = field(default_factory=dict)
    wars: set = field(default_factory=set)
    subjects: set = field(default_factory=set)
    divisions: int = 0
    capitulated: bool = False
    stability: float = .7
    faction: str = ''
    access: set = field(default_factory=set)
    goals: set = field(default_factory=set)
    technologies: dict = field(default_factory=dict)


@dataclass
class State:
    id: int
    owner: str
    controller: str
    cores: set = field(default_factory=set)
    divisions: dict = field(default_factory=dict)
    flags: dict = field(default_factory=dict)


class World:
    def __init__(self):
        self.countries = {t: Country(t) for t in ('VIE', 'CBD', 'CAM', 'CHI', 'SVN', 'SOV', 'USA', 'LAO')}
        self.states = {s: State(s, 'VIE', 'VIE', {'VIE'}) for s in (519, 520, 521, 522, 523, 524)}
        self.states.update({s: State(s, 'CBD', 'CBD', {'CBD'}) for s in (511, 512, 513, 514)})
        self.states.update({s: State(s, 'CHI', 'CHI', {'CHI'}) for s in (574, 578)})
        self.provinces = {7376: 'CBD'}
        self.global_flags = set()
        self.day = 0
        self.date = '1970.1.1'
        self.events, self.doctrines, self.wargoals, self.calls, self.research = [], [], [], [], []
        self.effects = {k: v for k, _, v in read_campaign('common/scripted_effects')}
        self.triggers = {k: v for k, _, v in read_campaign('common/scripted_triggers')}
        self.triggers[P + 'is_1970'] = first(read('common/scripted_triggers/COLDWAR_VIE_1970_triggers.txt'), P + 'is_1970')
        budget = {k: v for k, _, v in read('common/scripted_effects/00_budget_effects.txt')}
        self.effects['modify_treasury_effect'] = budget['modify_treasury_effect']
        self.ideas = {k: v for k, _, v in first(first(read_campaign('common/ideas'), 'ideas', []), 'country', [])}
        self.eventdefs = {first(b, 'id'): b for b in values(read_campaign('events'), 'country_event')}

    @property
    def vie(self):
        return self.countries['VIE']

    def number(self, value, country):
        if value == 'global.num_days': return self.day
        try:
            return float(value)
        except (TypeError, ValueError):
            return country.variables.get(value, 0.)

    def flag(self, country, key):
        return key in country.flags and (country.flags[key] is None or country.flags[key] > self.day)

    def idea(self, country, key):
        return key in country.ideas and (country.ideas[key] is None or country.ideas[key] > self.day)

    def scope(self, key, country, root):
        if key == 'ROOT': return root
        if key in self.countries: return self.countries[key]
        if key.isdigit() and int(key) in self.states: return self.states[int(key)]
        return None

    def test(self, rows, country=None, root=None):
        country = country or self.vie
        root = root or country
        return all(self.condition(k, o, v, country, root) for k, o, v in rows)

    def condition(self, key, op, value, country, root):
        if key in ('AND', 'limit', 'hidden_trigger'): return self.test(value, country, root)
        if key == 'OR': return any(self.condition(k, o, v, country, root) for k, o, v in value)
        if key == 'NOT': return not self.test(value, country, root)
        if key == 'custom_trigger_tooltip': return self.test([r for r in value if r[0] != 'tooltip'], country, root)
        scoped = self.scope(key, country, root)
        if scoped is not None: return self.test(value, scoped, root)
        if key in self.triggers: return self.test(self.triggers[key], country, root) == (value == 'yes')
        if key == 'IMP_is_1970_scenario': return country.scenario == (value == 'yes')
        if key in ('original_tag', 'tag'): return country.tag == value
        if key == 'exists': return country.exists == (value == 'yes')
        if key == 'has_government': return country.gov == value
        if key == 'has_country_flag': return self.flag(country, value)
        if key == 'has_state_flag': return self.flag(country, value)
        if key == 'has_idea': return self.idea(country, value)
        if key == 'has_tech': return country.technologies.get(value, 0) > 0
        if key == 'has_war': return bool(country.wars) == (value == 'yes')
        if key == 'has_war_with': return value in country.wars
        if key == 'has_wargoal_against': return value in country.goals
        if key == 'has_military_access_to': return value in country.access
        if key == 'has_global_flag': return value in self.global_flags
        if key == 'is_in_faction_with': return bool(country.faction) and country.faction == self.countries[value].faction
        if key == 'controls_province': return self.provinces.get(int(value)) == country.tag
        if key == 'stability': return country.stability < float(value) if op == '<' else country.stability > float(value)
        if key == 'num_divisions': return country.divisions > int(value) if op == '>' else country.divisions == int(value)
        if key == 'num_divisions_in_states':
            states = [int(v) for _, _, v in first(value, 'states')]
            return sum(self.states[s].divisions.get(country.tag, 0) for s in states) == int(first(value, 'count'))
        if key == 'has_capitulated': return country.capitulated == (value == 'yes')
        if key == 'owns_state': return self.states[int(value)].owner == country.tag
        if key == 'controls_state': return self.states[int(value)].controller == country.tag
        if key == 'is_owned_and_controlled_by':
            tag=root.tag if value=='ROOT' else value
            return country.owner == tag and country.controller == tag
        if key == 'is_owned_by': return country.owner == value
        if key == 'is_controlled_by': return country.controller == value
        if key == 'is_core_of': return value in country.cores
        if key == 'is_subject_of': return country.tag in self.countries[value].subjects
        if key == 'is_subject': return any(country.tag in c.subjects for c in self.countries.values()) == (value == 'yes')
        if key == 'has_variable': return value in country.variables
        if key == 'check_variable':
            if first(value, 'var'):
                a, b = self.number(first(value, 'var'), country), self.number(first(value, 'value'), country)
                return {'greater_than_or_equals': a >= b, 'less_than_or_equals': a <= b, 'greater_than': a > b, 'less_than': a < b, 'equals': a == b}[first(value, 'compare', 'equals')]
            name, operator, rhs = value[0]
            a, b = self.number(name, country), self.number(rhs, country)
            return a > b if operator == '>' else a < b if operator == '<' else a == b
        if key == 'always': return value == 'yes'
        raise AssertionError('Unhandled campaign trigger: ' + repr((key, op, value)))

    def call(self, key, country=None, root=None):
        assert key in self.effects, 'Missing emitted helper: ' + key
        self.run(self.effects[key], country or self.vie, root or country or self.vie)

    def remove_idea(self, country, key, root=None):
        if key in country.ideas:
            country.ideas.pop(key)
            self.run(first(self.ideas.get(key, []), 'on_remove', []), country, root or country)

    def run(self, rows, country=None, root=None):
        country = country or self.vie
        root = root or country
        chain = False
        for key, op, value in rows:
            if key == 'if':
                chain = self.test(first(value, 'limit', []), country, root)
                if chain: self.run([r for r in value if r[0] != 'limit'], country, root)
                continue
            if key == 'else_if':
                if not chain and self.test(first(value, 'limit', []), country, root):
                    self.run([r for r in value if r[0] != 'limit'], country, root)
                    chain = True
                continue
            if key == 'else':
                if not chain: self.run(value, country, root)
                chain = False
                continue
            chain = False
            scoped = self.scope(key, country, root)
            if scoped is not None:
                self.run(value, scoped, root)
                continue
            if key in self.effects:
                self.call(key, country, root)
                continue
            if key in ('hidden_effect', 'immediate'):
                self.run(value, country, root)
                continue
            if key in ('effect_tooltip', 'custom_effect_tooltip', 'update_money_dirty_variable', 'log', 'name', 'trigger', 'ai_chance'):
                continue
            if key in ('set_variable', 'set_temp_variable', 'add_to_variable'):
                name, _, val = next(r for r in value if r[0] != 'tooltip')
                country.variables[name] = (country.variables.get(name, 0) if key == 'add_to_variable' else 0) + self.number(val, country)
                continue
            if key == 'set_country_flag':
                country.flags[first(value, 'flag') if isinstance(value, list) else value] = self.day + int(first(value, 'days')) if isinstance(value, list) else None
                continue
            if key == 'clr_country_flag': country.flags.pop(value, None); continue
            if key == 'add_ideas': country.ideas[value] = None; continue
            if key == 'remove_ideas': self.remove_idea(country, value, root); continue
            if key == 'add_timed_idea': country.ideas[first(value, 'idea')] = self.day + int(first(value, 'days')); continue
            if key == 'army_experience': country.variables['xp'] = country.variables.get('xp', 0) + float(value); continue
            if key == 'add_doctrine_cost_reduction': self.doctrines.append(copy.deepcopy(value)); continue
            if key == 'add_tech_bonus': self.research.append(copy.deepcopy(value)); continue
            if key == 'create_wargoal': self.wargoals.append((country.tag, copy.deepcopy(value))); continue
            if key == 'country_event': self.events.append((country.tag, first(value, 'id'))); continue
            if key == 'add_opinion_modifier': self.calls.append((country.tag, key, copy.deepcopy(value))); continue
            if key == 'set_technology':
                for technology, _, level in value:
                    if technology != 'popup': country.technologies[technology] = int(level)
                continue
            if key in ('mdcw_cw_refresh_player_view', 'mdcw_cw_touch_gui'):
                self.calls.append((country.tag, key, value))
                continue  # Record the native UI delegation; do not emulate its implementation.
            raise AssertionError('Unhandled campaign effect: ' + repr((key, op, value)))

    def war(self, tag, active=True):
        if active:
            self.vie.wars.add(tag)
            self.countries[tag].wars.add('VIE')
        else:
            self.vie.wars.discard(tag)
            self.countries[tag].wars.discard('VIE')

    def advance(self, days):
        self.day += days
        for c in self.countries.values():
            for key in list(c.ideas):
                cancel = first(self.ideas.get(key, []), 'cancel')
                if not self.idea(c, key) or (cancel is not None and self.test(cancel, c, c)):
                    self.remove_idea(c, key)

    def stamp(self, suffix):
        key = suffix if suffix.startswith(P) else P + suffix
        self.vie.flags[key + '_reward_applied'] = None

    def ready(self, suffix):
        key = suffix if suffix.startswith(P) else P + suffix
        for group in NODES[key]['prerequisites']:
            self.stamp(group[0])

    def grant(self, suffix):
        key = suffix.removeprefix(P)
        self.call(P + 'campaign_apply_' + key)

    def update(self):
        self.call(P + 'campaign_daily_update')

    def native_programme(self, donor='VIE', target='CBD', active=True):
        country = self.countries[donor]
        country.variables.update({f'mdcw_cw_p6_state@{target}': 1 if active else 0,
                                  f'mdcw_cw_p6_size@{target}': 1,
                                  f'mdcw_cw_p6_end@{target}': self.day + 180})

    def response(self, event_id, actor, option=0):
        self.run(values(self.eventdefs[event_id], 'option')[option], self.countries[actor])

    def policy_option(self, event_id, suffix):
        helper = P + suffix + '_activate'
        return next(option for option in values(self.eventdefs[event_id], 'option') if any(k == helper for k, _, _ in walk(option)))


SPEC = json.loads((HERE / 'approved_campaigns.json').read_text(encoding='utf-8'))
NODES = {n['id']: n for n in SPEC['nodes']}


def equal(a, b):
    assert abs(a - b) < 1e-9, (a, b)


def money(world):
    return world.vie.variables['treasury']


def main():
    results = []

    def case(name, fn):
        fn()
        results.append(name)

    def root_transaction():
        w = World(); key = P + 'guerrilla_lessons'
        tree = first(read('common/national_focus/COLDWAR_VIE_1970_focus.txt'), 'focus_tree')
        focus = next(f for f in values(tree, 'focus') if first(f, 'id') == key)
        completion = first(focus, 'completion_reward')
        w.vie.variables['treasury'] = .009
        before = copy.deepcopy(w.vie)
        w.run([('effect_tooltip', '=', first(completion, 'effect_tooltip'))])
        assert w.vie == before and not w.doctrines
        w.run(completion)
        equal(money(w), .009)
        assert w.flag(w.vie, key + '_pending') and not w.doctrines
        w.vie.variables['treasury'] = .01
        w.run(completion)
        equal(money(w), 0)
        assert len(w.doctrines) == 1 and w.flag(w.vie, key + '_reward_applied')
        assert not w.flag(w.vie, key + '_pending')
        w.run(completion)
        equal(money(w), 0)
        assert len(w.doctrines) == 1
    case('Preview is inert; insufficient funds defer; exact funds pay once; completion cannot replay', root_transaction)

    def china_policy():
        w = World(); w.ready('china_survey')
        w.grant('china_survey')
        equal(money(w), 9.98)
        assert w.idea(w.vie, P + 'china_survey_policy')
        body = w.ideas[P + 'china_survey_policy']
        targeted = values(body, 'targeted_modifier')
        assert not targeted
        assert {k: float(v) for k, _, v in first(body, 'modifier')} == {'max_dig_in': 1., 'dig_in_speed_factor': .10}
        w.ready('china_liaison'); w.grant('china_liaison')
        equal(money(w), 9.955)
        assert not w.idea(w.vie, P + 'china_survey_policy') and w.idea(w.vie, P + 'china_liaison_policy')
        w.advance(366)
        assert not w.idea(w.vie, P + 'china_liaison_policy')
        w.update(); w.grant('china_liaison')
        equal(money(w), 9.955)
        assert not w.idea(w.vie, P + 'china_liaison_policy')
    case('Defensive reconnaissance grants flat entrenchment and speed without opponent scalars or supply penalties; paid family replacement expires', china_policy)

    def temporary_terrain_training():
        hold = P + 'china_hold_terrain_training'; depth = P + 'china_depth_terrain_training'
        w = World(); w.war('CHI'); w.ready('china_hold'); w.grant('china_hold')
        assert w.vie.technologies.get(hold) == 1 and not w.vie.technologies.get(depth)
        w.ready('china_depth'); w.grant('china_depth')
        assert not w.idea(w.vie, P + 'china_hold_policy') and w.idea(w.vie, P + 'china_depth_policy')
        assert w.vie.technologies[hold] == 0 and w.vie.technologies[depth] == 1
        w.advance(366)
        # This assertion precedes the daily observer: the actual emitted idea's
        # on_remove executes on timed expiry and owns its terrain cleanup.
        assert not w.idea(w.vie, P + 'china_depth_policy') and w.vie.technologies[depth] == 0
        before = copy.deepcopy(w.vie.variables); w.update()
        assert w.vie.variables == before and not w.vie.technologies[depth]
        w = World(); w.war('CHI'); w.ready('china_hold'); w.grant('china_hold')
        w.vie.technologies[hold] = 0; w.vie.technologies[depth] = 1
        before = copy.deepcopy(w.vie.variables); w.update()
        assert w.vie.technologies[hold] == 1 and w.vie.technologies[depth] == 0
        assert w.vie.variables == before
        w.war('CHI', False); w.update()
        assert not w.idea(w.vie, P + 'china_hold_policy') and w.vie.technologies[hold] == 0
        # A retained research flag without its real paid idea cannot survive load
        # reconciliation, nor can reconciliation renew an expired paid policy.
        w.vie.technologies[depth] = 1; w.update()
        assert w.vie.technologies[depth] == 0 and not w.idea(w.vie, P + 'china_depth_policy')
    case('Temporary forest and jungle training clears through real idea removal on replacement, expiry and peace; save reconciliation never replays payment', temporary_terrain_training)

    def live_combat():
        for tag in (None, 'CBD', 'CHI'):
            w = World(); w.ready('china_hold')
            if tag: w.war(tag)
            w.grant('china_hold')
            assert w.idea(w.vie, P + 'china_hold_policy') == (tag == 'CHI')
            equal(money(w), 9.965)  # First operational term is prepaid during preparation.
            if tag == 'CHI':
                w.war('CHI', False); w.update()
                assert not w.idea(w.vie, P + 'china_hold_policy')
        w = World(); w.ready('guerrilla_offensive'); w.war('CHI'); w.grant('guerrilla_offensive')
        assert w.idea(w.vie, P + 'guerrilla_offensive_policy')
        w.war('CHI', False); w.update()
        assert not w.idea(w.vie, P + 'guerrilla_offensive_policy')
    case('Combat rewards require the real opponent; prepared operations also work against China', live_combat)

    def paid_renewal():
        w = World(); w.ready('china_survey'); w.grant('china_survey')
        w.ready('china_liaison'); w.grant('china_liaison'); w.advance(366)
        q = P + 'china_decision_renew_readiness'; before = money(w)
        w.call(q + '_execute'); equal(money(w), before)
        option = w.policy_option(w.events[-1][1], 'china_liaison')
        w.vie.variables['treasury'] = .024
        w.run(option); equal(money(w), .024)
        assert not w.idea(w.vie, P + 'china_liaison_policy')
        w.vie.variables['treasury'] = .025
        w.vie.ideas[P + 'china_survey_policy'] = w.day + 30
        w.run(option); equal(money(w), 0)
        assert w.vie.ideas[P + 'china_liaison_policy'] == w.day + 365
        assert not w.idea(w.vie, P + 'china_survey_policy')
    case('Programme review is free; renewed policy rechecks exact funds, replaces family and starts a real term', paid_renewal)

    def foreign_transaction():
        q = P + 'china_decision_commission'
        w = World(); w.stamp('china_talks')
        w.call(q + '_execute')
        assert w.flag(w.vie, q + '_offer_pending') and w.flag(w.countries['CHI'], q + '_inbox')
        equal(money(w), 10)
        eid = w.events[-1][1]
        w.response(eid, 'CBD'); equal(money(w), 10)
        assert w.flag(w.vie, q + '_offer_pending')
        w.response(eid, 'CHI'); equal(money(w), 9.99)
        assert w.flag(w.vie, P + 'campaign_china_commission')
        assert not w.flag(w.vie, q + '_offer_pending') and not w.flag(w.countries['CHI'], q + '_inbox')
        w.response(eid, 'CHI'); equal(money(w), 9.99)
    case('Current recipient accepts once; wrong actor and replay cannot pay or impose terms', foreign_transaction)

    def foreign_expiry():
        q = P + 'china_decision_commission'
        for mode in ('expired', 'unfunded', 'unearned'):
            w = World(); w.stamp('china_talks'); w.call(q + '_execute'); eid = w.events[-1][1]
            if mode == 'expired': w.advance(91)
            elif mode == 'unfunded': w.vie.variables['treasury'] = .001
            else: w.vie.flags.pop(P + 'china_talks_reward_applied')
            before = money(w)
            w.response(eid, 'CHI')
            equal(money(w), before)
            assert not w.flag(w.vie, P + 'campaign_china_commission')
            if mode == 'expired':
                w.update(); before_events = len(w.events); w.call(q + '_execute')
                assert len(w.events) == before_events and w.flag(w.countries['CHI'], q + '_inbox')
                w.response(eid, 'CHI', 2)
                assert not w.flag(w.countries['CHI'], q + '_inbox')
                w.call(q + '_execute')
                assert w.flag(w.vie, q + '_offer_pending')
    case('Delayed acceptance rechecks expiry, current funds and earned access; stale inbox blocks reissue', foreign_expiry)

    def two_fronts():
        key = P + 'burden_two_fronts'
        w = World(); w.update(); assert not w.idea(w.vie, key)
        w.war('CHI'); w.update(); assert not w.idea(w.vie, key)
        w.war('CBD'); w.update(); assert w.idea(w.vie, key)
        w.war('CBD', False); w.update(); assert not w.idea(w.vie, key)
        w.native_programme(); w.update(); assert w.idea(w.vie, key)
        w.native_programme(active=False); w.update(); assert not w.idea(w.vie, key)
        w.war('CHI', False); w.states[511].controller = 'VIE'; w.update()
        assert not w.idea(w.vie, key) and w.idea(w.vie, P + 'burden_cambodia')
    case('Two front burden requires actual Chinese war plus an actual Cambodian war or funded commitment', two_fronts)

    def victory_guards():
        w = World(); w.ready('cambodia_aftermath')
        w.provinces[7376] = 'VIE'
        w.grant('cambodia_aftermath')
        equal(money(w), 10); assert not w.doctrines
        w.war('CBD'); w.update(); w.grant('cambodia_aftermath')
        equal(money(w), 10); assert not w.doctrines
        w.war('CBD', False); w.provinces[7376] = 'CBD'; w.update()
        w.grant('cambodia_aftermath'); equal(money(w), 10)
        w.vie.flags[P + 'campaign_security_agreement'] = w.day + 365
        w.grant('cambodia_aftermath')
        equal(money(w), 9.98)
        assert w.vie.variables.get('xp') == 25 and len(w.doctrines) == 1
        assert first(w.doctrines[0], 'uses') == '2' and first(w.doctrines[0], 'cost_reduction') == '0.2'
        w.grant('cambodia_aftermath'); equal(money(w), 9.98)
        assert w.vie.variables.get('xp') == 25 and len(w.doctrines) == 1
    case('Capital control alone, ongoing war and unfriendly peace cannot claim victory; actual friendly result pays once', victory_guards)

    def partner_dividend():
        w = World(); w.ready('cambodia_partner')
        w.war('CBD'); w.provinces[7376] = 'VIE'; w.update(); w.war('CBD', False)
        w.vie.subjects.add('CBD'); w.provinces[7376] = 'CBD'
        w.grant('cambodia_partner')
        equal(money(w), 10)
        w.vie.flags[P + 'campaign_security_agreement'] = w.day + 365
        w.grant('cambodia_partner'); equal(money(w), 10)
        w.call(P + 'cambodia_decision_victory_review_execute')
        assert w.flag(w.vie, P + 'campaign_victory_verified')
        w.grant('cambodia_partner'); equal(money(w), 9.97)
        idea = P + 'cambodia_partner_policy'
        assert w.idea(w.vie, idea)
        before = copy.deepcopy(w.vie.variables)
        w.states[520].controller = 'SVN'; w.update(); assert not w.idea(w.vie, idea)
        w.states[520].controller = 'VIE'; w.update(); assert w.idea(w.vie, idea)
        assert w.vie.variables == before
        w.vie.flags.pop(P + 'campaign_security_agreement'); w.update()
        assert not w.idea(w.vie, idea)
    case('Secured Southwest requires actual victory, current consent and controlled homeland; restoration never repays', partner_dividend)

    def drawdown():
        w = World(); q = P + 'cambodia_decision_withdrawal'
        w.stamp('cambodia_leave'); w.native_programme(); w.update()
        assert w.idea(w.vie, P + 'burden_cambodia')
        w.call(q + '_execute'); eid = w.events[-1][1]
        w.update(); assert w.idea(w.vie, P + 'burden_cambodia')
        assert not w.flag(w.vie, P + 'campaign_withdrawal_terms')
        w.response(eid, 'CBD'); equal(money(w), 9.99)
        verify = P + 'cambodia_decision_verify_drawdown'
        w.stamp('cambodia_verify')
        for state in (511, 512, 513, 514):
            w.states[state].divisions['VIE'] = 1
            w.call(verify + '_execute')
            equal(money(w), 9.99)
            assert not w.flag(w.vie, P + 'campaign_cbd_drawdown_verified')
            w.states[state].divisions['VIE'] = 0
        w.vie.access.add('CBD'); w.call(verify + '_execute'); equal(money(w), 9.99)
        w.vie.access.clear()
        w.states[511].controller = 'VIE'; w.call(verify + '_execute'); equal(money(w), 9.99)
        assert not w.flag(w.vie, P + 'campaign_cbd_drawdown_verified')
        w.states[511].controller = 'CBD'
        w.vie.ideas[P + 'cambodia_stay_policy'] = w.day + 180
        w.call(verify + '_execute'); equal(money(w), 9.975)
        assert w.flag(w.vie, P + 'campaign_cbd_drawdown_verified')
        assert not w.idea(w.vie, P + 'cambodia_stay_policy')
        assert not w.idea(w.vie, P + 'burden_cambodia') and w.idea(w.vie, P + 'campaign_burden_cambodia_light')
        w.call(verify + '_execute'); equal(money(w), 9.975)
        w.vie.access.add('CBD'); w.update()
        assert not w.flag(w.vie, P + 'campaign_cbd_drawdown_verified')
        assert w.idea(w.vie, P + 'burden_cambodia') and not w.idea(w.vie, P + 'campaign_burden_cambodia_light')
        w.native_programme(active=False); w.update()
        assert not w.idea(w.vie, P + 'burden_cambodia') and not w.idea(w.vie, P + 'campaign_burden_cambodia_light')
    case('Sent withdrawal removes nothing; accepted timetable checks every Cambodian state, access and real mission end', drawdown)

    def native_readiness():
        w = World(); w.ready('cambodia_train')
        w.vie.flags[P + 'campaign_security_agreement'] = w.day + 365
        w.countries['CBD'].divisions = 5
        q = P + 'cambodia_decision_partner_readiness'
        w.vie.flags[P + 'cambodia_decision_train_partner_accepted'] = None
        w.grant('cambodia_train'); equal(money(w), 10)
        assert not w.flag(w.vie, P + 'cambodia_train_reward_applied')
        # A made-up acceptance badge is insufficient: actual donor-native slot
        # state, positive size and a future programme end are all mandatory.
        for mode in ('state', 'size', 'end'):
            w.native_programme()
            w.vie.variables['mdcw_cw_p6_' + mode + '@CBD'] = 0
            w.grant('cambodia_train'); equal(money(w), 10)
        w.native_programme(); w.grant('cambodia_train'); equal(money(w), 9.96)
        assert not w.flag(w.vie, P + 'campaign_partner_readiness')
        w.call(q + '_execute'); equal(money(w), 9.94)
        assert w.flag(w.vie, P + 'campaign_partner_readiness')
        assert w.idea(w.vie, P + 'campaign_burden_cambodia_light')
        assert not w.idea(w.vie, P + 'burden_cambodia')
        w.countries['CBD'].divisions = 0; w.update()
        assert not w.idea(w.vie, P + 'campaign_burden_cambodia_light') and w.idea(w.vie, P + 'burden_cambodia')
        w.native_programme(active=False); w.update()
        assert not w.idea(w.vie, P + 'burden_cambodia') and not w.idea(w.vie, P + 'cambodia_train_policy')
    case('Partner training has no readiness circularity; only active funded native assistance and actual forces lighten burden', native_readiness)

    def refusal_learning():
        w = World(); q = P + 'china_decision_soviet_assistance'
        w.stamp('china_soviet'); w.global_flags.add('mdcw_cw_initialized')
        w.call(q + '_execute'); eid = w.events[-1][1]
        w.response(eid, 'SOV', 1)
        equal(money(w), 10)
        assert w.flag(w.vie, P + 'campaign_soviet_response')
        assert not w.test([(P + 'campaign_sov_native_assistance', '=', 'yes')])
        w.ready('china_assistance'); w.grant('china_assistance')
        equal(money(w), 9.965)
        assert w.vie.variables.get('xp') == 20 and len(w.doctrines) == 1
        assert not w.test([(P + 'campaign_sov_native_assistance', '=', 'yes')])
    case('Soviet refusal resolves the doctrinal learning route without fabricating any funded programme', refusal_learning)

    def free_soviet_request():
        w = World(); q = P + 'china_decision_soviet_assistance'
        w.stamp('china_soviet'); w.global_flags.add('mdcw_cw_initialized')
        w.vie.variables['treasury'] = -.4
        w.call(q + '_execute')
        assert w.flag(w.vie, q + '_offer_pending') and w.flag(w.countries['SOV'], q + '_inbox')
        equal(money(w), -.4)
        eid = next(event_id for actor, event_id in reversed(w.events) if actor == 'SOV')
        w.response(eid, 'SOV')
        equal(money(w), -.4)
        equal(w.countries['SOV'].variables['treasury'], 10)
        assert w.flag(w.vie, P + 'campaign_soviet_approach_accepted')
        assert not w.flag(w.vie, q + '_offer_pending') and not w.flag(w.countries['SOV'], q + '_inbox')
        assert not w.test([(P + 'campaign_sov_native_assistance', '=', 'yes')])
        assert ('SOV', 'mdcw_cw_refresh_player_view', 'yes') in w.calls
        w.response(eid, 'SOV'); equal(money(w), -.4)
    case('Free Soviet contact can be sent and accepted with negative Vietnamese treasury without charging either country', free_soviet_request)

    def limited_peace():
        w = World(); q = P + 'cambodia_decision_commission'
        w.stamp('cambodia_channel'); w.call(q + '_execute'); w.response(w.events[-1][1], 'CBD')
        w.stamp('cambodia_monitor')
        w.states[511].controller = 'VIE'; before = money(w)
        w.grant('cambodia_border_settlement'); equal(money(w), before)
        assert not w.flag(w.vie, P + 'cambodia_border_settlement_reward_applied')
        w.states[511].controller = 'CBD'; w.grant('cambodia_border_settlement')
        w.grant('cambodia_limited_commitment'); w.grant('cambodia_talks')
        assert not w.flag(w.vie, P + 'cambodia_talks_reward_applied')
        w.call(P + 'cambodia_decision_limited_review_execute')
        assert w.flag(w.vie, P + 'campaign_limited_verified')
        w.grant('cambodia_talks'); w.grant('cambodia_limits')
        assert not w.flag(w.vie, P + 'cambodia_limits_reward_applied')
        conference = P + 'cambodia_decision_conference'
        w.call(conference + '_execute'); w.response(w.events[-1][1], 'CBD')
        w.grant('cambodia_limits')
        assert w.flag(w.vie, P + 'cambodia_limits_reward_applied')
        assert not w.flag(w.vie, P + 'cambodia_aftermath_reward_applied')
        assert not w.flag(w.vie, P + 'campaign_cbd_war_seen')
        assert not w.idea(w.vie, P + 'cambodia_partner_policy')
        assert not w.test([(P + 'campaign_cbd_victory', '=', 'yes')])
    case('Consenting limited peace reaches regional security without occupation, invented victory or partner dividend', limited_peace)

    def general_guarantees():
        w = World(); w.ready('guerrilla_guarantees')
        assert not w.test([(P + 'campaign_domestic_grievance', '=', 'yes')])
        w.grant('guerrilla_guarantees')
        equal(money(w), 9.975)
        assert w.idea(w.vie, P + 'guerrilla_guarantees_policy')
        w = World(); w.ready('guerrilla_security'); w.grant('guerrilla_security')
        equal(money(w), 10)
        assert not w.idea(w.vie, P + 'guerrilla_security_policy')
        w.vie.flags[P + 'campaign_war_seen'] = None; w.vie.stability = .5
        w.grant('guerrilla_security'); equal(money(w), 9.975)
        assert w.idea(w.vie, P + 'guerrilla_security_policy')
    case('General postwar guarantees need no invented grievance; emergency security requires real governed postwar strain', general_guarantees)

    def china_verification():
        w = World(); q = P + 'china_decision_standdown'; verify = P + 'china_decision_verify'
        w.stamp('china_opening'); w.stamp('china_standdown'); w.war('CHI'); w.update()
        w.call(q + '_execute'); w.response(w.events[-1][1], 'CHI')
        equal(money(w), 9.99)
        w.call(verify + '_execute'); equal(money(w), 9.99)
        assert w.idea(w.vie, P + 'burden_frontier') and not w.flag(w.vie, P + 'campaign_china_drawdown_verified')
        w.war('CHI', False)
        for state, tag in ((574, 'VIE'), (578, 'VIE'), (522, 'CHI'), (523, 'CHI'), (524, 'CHI')):
            w.states[state].divisions[tag] = 1
            w.call(verify + '_execute'); equal(money(w), 9.99)
            assert not w.flag(w.vie, P + 'campaign_china_drawdown_verified')
            w.states[state].divisions[tag] = 0
        w.call(verify + '_execute'); equal(money(w), 9.975)
        assert w.flag(w.vie, P + 'campaign_china_drawdown_verified') and not w.idea(w.vie, P + 'burden_frontier')
        w.call(verify + '_execute'); equal(money(w), 9.975)
        w.countries['CHI'].goals.add('VIE')
        w.call(q + '_execute'); w.response(w.events[-1][1], 'CHI')
        equal(money(w), 9.965)
        assert not w.flag(w.vie, P + 'campaign_china_drawdown_verified')
    case('Chinese stand down needs actual peace and reciprocal land checks; new accepted terms invalidate the old verification', china_verification)

    def scenario_actor_guards():
        w = World(); w.vie.scenario = False; w.grant('guerrilla_lessons')
        equal(money(w), 10); assert not w.doctrines
        w = World(); w.call(P + 'campaign_apply_guerrilla_lessons', w.countries['CAM'])
        equal(w.countries['CAM'].variables['treasury'], 10); assert not w.doctrines
    case('Only actual VIE in the Cold War scenario can execute campaign rewards', scenario_actor_guards)

    def prepared_first_term():
        w=World();w.ready('china_hold');w.grant('china_hold');equal(money(w),9.965)
        assert not w.idea(w.vie,P+'china_hold_policy')
        w.update();assert not w.idea(w.vie,P+'china_hold_policy')
        w.war('CHI');w.update()
        assert w.idea(w.vie,P+'china_hold_policy') and w.vie.technologies[P+'china_hold_terrain_training']==1
        equal(money(w),9.965)
        w.advance(366);w.update();assert not w.idea(w.vie,P+'china_hold_policy')
        w.war('CHI',False);w.update();w.war('CHI');w.update()
        assert not w.idea(w.vie,P+'china_hold_policy')
        equal(money(w),9.965)
    case('Prepaid defensive preparation activates on real war immediately and never renews from expiry or a second war',prepared_first_term)

    def durable_schools():
        w=World();w.ready('guerrilla_training');w.grant('guerrilla_training')
        school=P+'guerrilla_training_policy'
        assert w.vie.ideas[school] is None and len(w.research)==1
        before=(money(w),copy.deepcopy(w.vie.variables),copy.deepcopy(w.research),copy.deepcopy(w.doctrines))
        w.advance(2000);w.update();assert w.idea(w.vie,school)
        w.vie.ideas.pop(school);w.update();assert w.idea(w.vie,school)
        assert (money(w),w.vie.variables,w.research,w.doctrines)==before
        w.ready('guerrilla_staff');w.grant('guerrilla_staff')
        assert not w.idea(w.vie,school) and w.idea(w.vie,P+'guerrilla_staff_policy')
        n=len(w.research);w.update();w.grant('guerrilla_staff');assert len(w.research)==n
    case('Schools are durable replacement institutions; restoration grants no research, XP or money again',durable_schools)

    def genuine_cooperation():
        w=World();w.ready('china_talks');w.grant('china_talks')
        idea=P+'china_talks_policy';assert not w.idea(w.vie,idea)
        q=P+'china_decision_commission';w.call(q+'_execute');w.response(w.events[-1][1],'CHI')
        before=money(w);w.update();assert w.idea(w.vie,idea);equal(money(w),before)
        w.advance(366);w.update();assert not w.idea(w.vie,idea)
    case('The new cooperation dividend needs a current accepted commission and ends with that agreement',genuine_cooperation)

    report = dict(status='pass', count=len(results), tests=results, engine_tested=False,
                  limits='Focused interpreter of installed campaign AST. It models flags, money, ideas and on_remove callbacks, technology levels, war/state predicates, reciprocal land divisions and recipient transactions. Terrain combat calculations, engine UI, troop movement, warfare, native assistance execution, opinion formulas, actual doctrine purchasing and peace conferences are not simulated.')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
