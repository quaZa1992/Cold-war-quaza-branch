# IMPERIA COLD WAR — Territorial runtime source and state-transition checks.
"""Execute the emitted native effect AST in a bounded model, not HOI4.

External funding and restricted-appropriation helpers are explicit fixtures of
their published interfaces. Those providers require their own integration tests.
"""
from collections import defaultdict
from copy import deepcopy
from datetime import date, timedelta
from pathlib import Path
import json
import re
import sys
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from focus_prerequisite_ui import nodes, field
from runtime_territories import build, AREAS, STATE_PROFILES

DATA = json.loads((HERE / 'design.json').read_text(encoding='utf-8'))
EXPORT = build(DATA)
EFFECTS = {n.key: n.children() for n in nodes(EXPORT['files']['common/scripted_effects/ISR2_territories_effects.txt'])}
TRIGGERS = {n.key: n.children() for n in nodes(EXPORT['files']['common/scripted_triggers/ISR2_territories_triggers.txt'])}
DYNAMIC = {n.key: n.children() for n in nodes(EXPORT['files']['common/dynamic_modifiers/ISR2_territories_modifiers.txt'])}
EFFECTS['ISR2_private_commit'] = nodes('''
set_variable = { ISR2_private_paid = 0 }
set_variable = { ISR2_private_paid_USA = 0 }
set_variable = { ISR2_private_paid_GER = 0 }
set_variable = { ISR2_private_paid_ROM = 0 }
if = { limit = { ISR2_private_ready = yes }
set_variable = { ISR2_private_paid = ISR2_private_required }
set_variable = { ISR2_private_paid_USA = ISR2_private_required }
subtract_from_variable = { ISR2_private_available = ISR2_private_required }
}''')
EFFECTS['ISR2_private_recalculate'] = []
EFFECTS['ISR2_project_support_quote'] = nodes('set_variable = { ISR2_project_net_cost = ISR2_project_cost }')
EFFECTS['ISR2_project_support_commit'] = EFFECTS['ISR2_project_support_quote']


class Scope:
    def __init__(self, name):
        self.name = name; self.vars = defaultdict(float); self.flags = {}; self.flag_values = {}; self.mods = set()
        self.buildings = defaultdict(int); self.extra_slots = 0; self.owner = None; self.controller = None
        self.cores = set(); self.exists = True; self.state_flags = set(); self.resistance = 0
        self.compliance = 0; self.forts = 0; self.staff = True; self.party = 'western_social_democrats'
        self.temps = defaultdict(float); self.completed = set()


class Game:
    def __init__(self):
        self.countries = {tag: Scope(tag) for tag in ['ISR', 'PAL', 'EGY', 'SYR', 'USA', 'GER', 'ROM']}
        self.states = {s: Scope(s) for s in [205, 206, 208, 209, 213, 587]}
        for s, state in self.states.items():
            state.owner = {205: 'ISR', 206: 'ISR', 208: 'PAL', 209: 'PAL', 213: 'EGY', 587: 'SYR'}[s]
            state.controller = 'ISR'; state.cores.add(state.owner)
        self.day = 0; self.scenario = True; self.dirty = 0; self.claim_requests = []
        self.modifier_adds = defaultdict(int)
        self.countries['ISR'].vars.update(gdp_total=100, treasury=100)
        self.execute(EFFECTS['ISR2_territories_init'])

    @property
    def israel(self):
        return self.countries['ISR']

    def value(self, scope, raw, temp=False):
        raw = str(raw)
        try: return float(raw)
        except ValueError: pass
        if raw.startswith('building_level@'):
            return scope.buildings[raw.split('@', 1)[1]]
        return (scope.temps if temp else scope.vars)[raw]

    def compare(self, left, op, right):
        if op in ['=', 'equals']: return abs(left-right) < 1e-8
        if op in ['>', 'greater_than']: return left > right
        if op in ['<', 'less_than']: return left < right
        if op == 'greater_than_or_equals': return left >= right-1e-8
        if op == 'less_than_or_equals': return left <= right+1e-8
        raise AssertionError(('comparison', op))

    def flag(self, scope, key):
        return key in scope.flags and scope.flag_values.get(key, 1) > 0 and (scope.flags[key] is None or self.day < scope.flags[key])

    def condition(self, rows, scope=None):
        scope = scope or self.israel
        for n in rows:
            key, value = n.key, n.value
            children = n.children()
            if key == 'AND': ok = self.condition(children, scope)
            elif key == 'OR': ok = any(self.condition([c], scope) for c in children)
            elif key == 'NOT': ok = not self.condition(children, scope)
            elif key == 'custom_trigger_tooltip': ok = self.condition([c for c in children if c.key != 'tooltip'], scope)
            elif key in self.countries: ok = self.condition(children, self.countries[key])
            elif key.isdigit(): ok = self.condition(children, self.states[int(key)])
            elif key in ('owner', 'controller'): ok = self.condition(children, self.countries[getattr(scope, key)])
            elif key == 'exists': ok = scope.exists == (value == 'yes')
            elif key == 'tag': ok = scope.name == value
            elif key == 'date':
                now = date(1970, 1, 1) + timedelta(days=self.day)
                parts = [int(p) for p in str(value).split('.')]
                other = date(*parts)
                ok = now < other if n.op == '<' else now > other
            elif key == 'ISR2_is_scenario': ok = self.scenario and scope.name == 'ISR'
            elif key in TRIGGERS: ok = self.condition(TRIGGERS[key], scope)
            elif key == 'ISR2_private_ready': ok = scope.vars['ISR2_private_required'] > 0 and scope.vars['ISR2_private_available']+1e-8 >= scope.vars['ISR2_private_required']
            elif key == 'has_variable': ok = value in scope.vars
            elif key == 'has_country_flag': ok = self.flag(scope, value)
            elif key == 'has_state_flag': ok = value in scope.state_flags
            elif key == 'has_completed_focus': ok = value in scope.completed
            elif key == 'has_dynamic_modifier': ok = self.modifier_key(scope, children) in scope.mods
            elif key == 'has_resistance': ok = scope.resistance > 0
            elif key.endswith('_are_in_power'): ok = scope.party + '_are_in_power' == key
            elif key.startswith('can_staff_'): ok = scope.staff
            elif key in ('controls_state', 'has_full_control_of_state'):
                ok = self.states[int(value)].controller == scope.name
            elif key == 'owns_state': ok = self.states[int(value)].owner == scope.name
            elif key == 'is_controlled_by': ok = scope.controller == value
            elif key == 'is_core_of': ok = value in scope.cores
            elif key == 'free_building_slots':
                size = next(c for c in children if c.key == 'size')
                ok = self.compare(7-scope.forts, size.op, float(size.value))
            elif key == 'check_variable':
                var_key = field(children, 'var')
                if var_key:
                    ok = self.compare(self.value(scope, var_key), field(children, 'compare', '='), self.value(scope, field(children, 'value')))
                else:
                    c = children[0]; ok = self.compare(self.value(scope, c.key), c.op, self.value(scope, c.value))
            else: raise AssertionError(('unsupported condition', key, scope.name))
            if not ok: return False
        return True

    def execute(self, rows, scope=None):
        scope = scope or self.israel
        prior = None
        for n in rows:
            key, value = n.key, n.value; children = n.children()
            if key == 'if':
                prior = self.condition(next(c.children() for c in children if c.key == 'limit'), scope)
                if prior: self.execute([c for c in children if c.key != 'limit'], scope)
            elif key == 'else':
                if prior is False: self.execute(children, scope)
                prior = None
            elif key in self.countries: self.execute(children, self.countries[key])
            elif key.isdigit(): self.execute(children, self.states[int(key)])
            elif key in ('owner', 'controller'): self.execute(children, self.countries[getattr(scope, key)])
            elif key == 'every_country':
                limit = next((c.children() for c in children if c.key == 'limit'), [])
                for country in self.countries.values():
                    if self.condition(limit, country): self.execute([c for c in children if c.key != 'limit'], country)
            elif key in ('set_variable', 'add_to_variable', 'subtract_from_variable', 'multiply_variable',
                         'set_temp_variable', 'multiply_temp_variable'):
                c = children[0]; target = scope.temps if 'temp' in key else scope.vars
                amount = self.value(scope, c.value, temp='temp' in key and key != 'set_temp_variable')
                if key.startswith('set_'): target[c.key] = amount
                elif key.startswith('add_'): target[c.key] += amount
                elif key.startswith('subtract_'): target[c.key] -= amount
                else: target[c.key] *= amount
            elif key == 'modify_treasury_effect': scope.vars['treasury'] += scope.temps['treasury_change']
            elif key == 'clamp_variable':
                key_var = field(children, 'var')
                minimum = field(children, 'min'); maximum = field(children, 'max')
                if minimum is not None: scope.vars[key_var] = max(scope.vars[key_var], self.value(scope, minimum))
                if maximum is not None: scope.vars[key_var] = min(scope.vars[key_var], self.value(scope, maximum))
            elif key == 'set_country_flag':
                if isinstance(value, list):
                    name = field(children, 'flag')
                    scope.flags[name] = self.day + int(field(children, 'days'))
                    scope.flag_values[name] = float(field(children, 'value', 0))
                else:
                    scope.flags[value] = None
                    scope.flag_values[value] = 1
            elif key == 'clr_country_flag':
                scope.flags.pop(value, None)
                scope.flag_values.pop(value, None)
            elif key == 'set_state_flag': scope.state_flags.add(value)
            elif key == 'add_dynamic_modifier':
                modifier = self.modifier_key(scope, children)
                scope.mods.add(modifier)
                self.modifier_adds[scope.name, modifier] += 1
            elif key == 'remove_dynamic_modifier': scope.mods.discard(self.modifier_key(scope, children))
            elif key == 'add_extra_state_shared_building_slots': scope.extra_slots += int(value)
            elif key == 'add_building_construction':
                kind, amount = field(children, 'type'), int(field(children, 'level'))
                if kind == 'bunker': scope.forts += amount
                else: scope.buildings[kind] += amount
            elif key == 'uncomplete_national_focus': scope.completed.discard(field(children, 'focus'))
            elif key == 'start_resistance': scope.resistance = 1
            elif key == 'set_resistance': scope.resistance = float(value)
            elif key == 'set_compliance': scope.compliance = float(value)
            elif key == 'update_money_dirty_variable': self.dirty += 1
            elif key == 'ISR2_private_claim_credit':
                self.claim_requests.append({k: scope.vars[k] for k in ['ISR2_private_claim_id', 'ISR2_private_claim_amount',
                    'ISR2_private_claim_share_USA', 'ISR2_private_claim_share_GER', 'ISR2_private_claim_share_ROM']})
            elif key in EFFECTS: self.execute(EFFECTS[key], scope)
            else: raise AssertionError(('unsupported effect', key))

    def modifier_key(self, scope, rows):
        key = field(rows, 'modifier')
        # Track the source attached to a state provider separately. An explicit
        # ISR query must match its explicit ISR installation; country fixtures
        # retain their existing single-provider representation.
        return (key, field(rows, 'scope', scope.name)) if isinstance(scope.name, int) else key

    def action(self, key):
        fid = 'ISR2_' + key
        helper = nodes(EXPORT['actions'][fid]['reward'])[0].key
        self.israel.completed.add(fid)
        self.execute(EFFECTS[helper])

    def daily(self, days=0):
        self.day += days
        self.execute(EFFECTS['ISR2_territories_daily'])


class TerritorialRuntimeTests(unittest.TestCase):
    def test_native_zero_default_requires_explicit_timed_value_and_keeps_cover_and_cooldown(self):
        game = Game()
        game.execute(nodes('set_country_flag = { flag = unvalued_timed_fixture days = 5 }'))
        self.assertEqual(game.israel.flag_values['unvalued_timed_fixture'], 0)
        self.assertFalse(game.flag(game.israel, 'unvalued_timed_fixture'))

        def check_timed_values(rows):
            for row in rows:
                if row.key == 'set_country_flag' and row.children():
                    self.assertEqual(field(row.children(), 'value'), '1')
                check_timed_values(row.children())
        for body in EFFECTS.values():
            check_timed_values(body)

        # Native probe 3 reached the receipt and quote but immediately refunded
        # the reserve because its unvalued term was false. Reproduce its inputs.
        game.israel.vars.update(gdp_total=10, treasury=100.5, ISR2_private_available=.2)
        game.action('labor_yanai')
        self.assertTrue(game.flag(game.israel, 'ISR2_territories_yanai_term'))
        self.assertTrue(game.flag(game.israel, 'ISR2_territories_done_labor_yanai'))
        self.assertFalse(game.flag(game.israel, 'ISR2_territories_yanai_settled'))
        self.assertAlmostEqual(game.israel.vars['ISR2_territories_yanai_reserve'], .02)
        self.assertAlmostEqual(game.israel.vars['treasury'], 100.48)
        game.action('controlled_sites')
        self.assertAlmostEqual(game.israel.vars['treasury'], 100.38)
        self.assertAlmostEqual(game.israel.vars['ISR2_private_available'], .15)
        self.assertAlmostEqual(game.israel.vars['ISR2_private_paid'], .05)
        self.assertEqual(game.israel.vars['ISR2_territories_yanai_used'], 1)
        self.assertTrue(game.flag(game.israel, 'ISR2_territories_cooldown_controlled_sites'))
        before = (deepcopy(game.states[208].buildings), game.states[208].extra_slots,
                  deepcopy(game.israel.vars))
        game.action('controlled_sites')
        for _ in range(12): game.execute(EFFECTS['ISR2_territories_refresh'])
        self.assertEqual(game.states[208].buildings, before[0])
        self.assertEqual(game.states[208].extra_slots, before[1])
        for key in ('treasury', 'ISR2_private_available', 'ISR2_territories_yanai_reserve',
                    'ISR2_territories_yanai_used', 'ISR2_territories_tiers_208'):
            self.assertAlmostEqual(game.israel.vars[key], before[2][key])

    def test_state_modifier_queries_match_the_installed_source_and_refresh_is_cached(self):
        game = Game()
        initial_adds = deepcopy(game.modifier_adds)
        self.assertTrue(initial_adds)
        for _ in range(12):
            game.execute(EFFECTS['ISR2_territories_refresh'])
        self.assertEqual(game.modifier_adds, initial_adds)
        for state in AREAS.values():
            key = 'ISR2_territories_occupation_' + str(state) + '_local'
            self.assertTrue(game.condition(nodes('has_dynamic_modifier = { modifier = ' + key + ' scope = ISR }'), game.states[state]))
            self.assertFalse(game.condition(nodes('has_dynamic_modifier = { modifier = ' + key + ' scope = EGY }'), game.states[state]))

        def check_state_queries(rows, in_state=False):
            for row in rows:
                if in_state and row.key in ('has_dynamic_modifier', 'remove_dynamic_modifier'):
                    self.assertEqual(field(row.children(), 'scope'), 'ISR')
                child_scope = True if row.key.isdigit() else False if row.key in ('ISR', 'PAL', 'owner', 'controller', 'every_country') else in_state
                check_state_queries(row.children(), child_scope)
        for body in EFFECTS.values():
            check_state_queries(body)
        for action in EXPORT['actions'].values():
            check_state_queries(nodes(action['preview']))

    def test_partner_preview_rows_follow_actual_draws_without_changing_native_payload(self):
        before = deepcopy(DATA)
        with patch('runtime_territories._preview_adaptations', return_value={}):
            without_adaptation = build(DATA)
        adapted = build(DATA)
        self.assertEqual(DATA, before)
        for key in ('files', 'actions', 'loc', 'init', 'refresh', 'daily'):
            self.assertEqual(adapted[key], without_adaptation[key], key)
        overrides = adapted['preview_adaptations']
        self.assertEqual(len(overrides), 11)
        draws = {'controlled_sites': '-0.5%', 'west_bank_projects': '-0.5%',
                 'sinai_projects': '-0.5%', 'gaza_projects': '-0.5%', 'golan_projects': '-0.5%',
                 'mafdal_regularise_sites': '-0.3%', 'liberal_sinai_resort': '-0.6%',
                 'liberal_coastal_resort': '-0.6%'}
        for slug, value in draws.items():
            rows = overrides['ISR2_' + slug]['effects']
            row = next(row for row in rows if row['label'] == 'Partner Project Capital')
            self.assertEqual(row['value'], value + ' of annual GDP')
            self.assertEqual(row['tone'], 'cost')
        for slug in ('labor_yanai', 'mafdal_land_committee', 'liberal_hotel_credit'):
            rows = overrides['ISR2_' + slug]['effects']
            self.assertFalse(any('Capital' in row['label'] or 'Private Tier' in row['label'] for row in rows))
        self.assertEqual(overrides['ISR2_labor_yanai']['requirements'], ['Alignment is in Power.'])
        self.assertTrue(any('is available' in line for line in overrides['ISR2_liberal_hotel_credit']['requirements']))

    def test_all_actions_parse_without_decision_helpers(self):
        self.assertEqual(len(EXPORT['actions']), 33)
        for path, source in EXPORT['files'].items():
            self.assertTrue(source.startswith('# IMPERIA COLD WAR'))
            self.assertNotIn('unlock_decision_tooltip', source)
            self.assertTrue(nodes(source), path)
        for action in EXPORT['actions'].values():
            for key, text in action.items():
                self.assertTrue(nodes(text) or key == 'visible_available')

    def test_visible_requirements_use_real_conditions_and_readable_labels(self):
        for focus, action in EXPORT['actions'].items():
            self.assertIn('visible_available', action)
            visible = action['visible_available']
            self.assertNotIn('always = yes', visible)
            self.assertNotIn('ISR2_is_scenario', visible)
            self.assertNotIn('gdp_total >', visible)
            self.assertNotIn('_are_in_power', visible)
            def visit(rows):
                for n in rows:
                    if n.key == 'custom_trigger_tooltip':
                        label = field(n.children(), 'tooltip')
                        self.assertIn(label, EXPORT['loc'])
                        self.assertNotIn('ISR2_', EXPORT['loc'][label])
                        self.assertTrue([c for c in n.children() if c.key != 'tooltip'])
                    visit(n.children())
            visit(nodes(visible))
        game = Game()
        visible = nodes(EXPORT['actions']['ISR2_controlled_sites']['visible_available'])
        self.assertTrue(game.condition(visible))
        game.states[208].buildings['agriculture_district'] = 10
        self.assertFalse(game.condition(visible))
        game.states[208].buildings['agriculture_district'] = 0
        game.israel.vars['ISR2_territories_tiers_208'] = 3
        self.assertFalse(game.condition(visible))
        game.israel.vars['ISR2_territories_tiers_208'] = 0
        game.israel.flags['ISR2_territories_freeze_parliament'] = None
        self.assertFalse(game.condition(visible))
        game.israel.flags.pop('ISR2_territories_freeze_parliament')
        game.israel.flags['ISR2_territories_cooldown_controlled_sites'] = game.day + 182
        self.assertFalse(game.condition(visible))
        game.israel.party = 'western_liberals'
        hotel = nodes(EXPORT['actions']['ISR2_liberal_hotel_credit']['visible_available'])
        self.assertFalse(game.condition(hotel))
        game.israel.vars['ISR2_private_available'] = .6
        self.assertTrue(game.condition(hotel))

    def test_three_controlled_tiers_have_real_assets_slots_and_shared_cap(self):
        game = Game()
        for count in range(1, 4):
            game.action('controlled_sites'); game.daily(183)
            self.assertEqual(game.israel.vars['ISR2_territories_tiers_208'], count)
            self.assertEqual(game.states[208].buildings['agriculture_district'], count)
            self.assertEqual(game.states[208].extra_slots, 3*count)
            self.assertEqual(game.states[208].forts, count)
        before = game.israel.vars['treasury']
        game.action('west_bank_projects')
        self.assertEqual(game.israel.vars['treasury'], before)
        self.assertEqual(game.israel.vars['ISR2_territories_tiers_208'], 3)

    def test_party_site_counts_once_and_keeps_cost_after_government_change(self):
        game = Game(); game.action('labor_valley')
        self.assertEqual(game.israel.vars['ISR2_territories_tiers_208'], 1)
        self.assertAlmostEqual(game.israel.vars['ISR2_territories_weekly_expense'], .015)
        assets = dict(game.states[208].buildings)
        game.israel.party = 'western_conservatism'; game.daily()
        self.assertAlmostEqual(game.israel.vars['ISR2_territories_weekly_expense'], .015)
        self.assertEqual(dict(game.states[208].buildings), assets)
        game.states[208].controller = 'PAL'; game.daily()
        self.assertEqual(game.israel.vars['ISR2_territories_weekly_expense'], 0)
        game.states[208].controller = 'ISR'; game.daily()
        self.assertAlmostEqual(game.israel.vars['ISR2_territories_weekly_expense'], .015)
        self.assertEqual(dict(game.states[208].buildings), assets)

    def test_physical_capacity_failure_changes_nothing(self):
        for failure in ['farm', 'infra', 'fort', 'staff', 'control']:
            game = Game()
            if failure == 'farm': game.states[208].buildings['agriculture_district'] = 10
            if failure == 'infra': game.states[208].buildings['infrastructure'] = 6
            if failure == 'fort': game.states[208].forts = 7
            if failure == 'staff': game.israel.staff = False
            if failure == 'control': game.states[208].controller = 'PAL'
            before = game.israel.vars['treasury']
            game.action('controlled_sites')
            self.assertEqual(game.israel.vars['treasury'], before, failure)
            self.assertEqual(game.israel.vars['ISR2_territories_tiers_208'], 0)
            self.assertNotIn('ISR2_controlled_sites', game.israel.completed)

    def test_foreign_host_moves_and_global_two_area_cap(self):
        game = Game()
        for state in [208, 209, 213]: game.states[state].controller = game.states[state].owner
        game.action('foreign_footholds'); game.action('gaza_foothold')
        self.assertEqual(game.israel.vars['ISR2_territories_foreign_count'], 2)
        before = game.israel.vars['treasury']; game.action('sinai_foothold')
        self.assertEqual(game.israel.vars['treasury'], before)
        self.assertIn('ISR2_territories_foreign_208_host', game.countries['PAL'].mods)
        game.states[208].controller = 'EGY'; game.daily()
        self.assertNotIn('ISR2_territories_foreign_208_host', game.countries['PAL'].mods)
        self.assertIn('ISR2_territories_foreign_208_host', game.countries['EGY'].mods)
        self.assertEqual(game.states[208].extra_slots, 0)

    def test_foreign_freeze_network_cost_and_closure_are_exact(self):
        game = Game(); game.states[208].controller = 'PAL'
        game.action('foreign_footholds'); game.action('funded_network'); game.action('cap_projects')
        self.assertAlmostEqual(game.israel.vars['ISR2_territories_weekly_expense'], .016)
        game.action('close_west_bank')
        self.assertEqual(game.israel.vars['ISR2_territories_weekly_expense'], 0)
        self.assertNotIn('ISR2_territories_foreign_208_host', game.countries['PAL'].mods)
        self.assertNotIn('ISR2_territories_foreign_208_israel', game.israel.mods)

    def test_foreign_closure_cannot_strip_controlled_site_burdens(self):
        game = Game(); game.action('controlled_sites')
        before = deepcopy(game.israel.mods); game.action('close_west_bank')
        self.assertEqual(game.israel.mods, before)
        self.assertIn('ISR2_territories_nahal_208_1_budget', game.israel.mods)

    def test_pressure_caps_relief_and_country_reappearance(self):
        game = Game()
        for _ in range(3): game.action('controlled_sites'); game.daily(183)
        self.assertEqual(game.israel.vars['ISR2_territories_pressure_208'], 2)
        game.israel.flags['ISR2_pal_service_relief_active'] = None
        game.israel.vars['ISR2_pal_service_relief_state'] = 208; game.daily()
        self.assertEqual(game.israel.vars['ISR2_territories_effective_pressure_total'], 1)
        game.countries['PAL'].exists = False; game.daily()
        self.assertEqual(game.israel.vars['ISR2_territories_effective_pressure_total'], 0)
        game.countries['PAL'].exists = True; game.daily()
        self.assertEqual(game.israel.vars['ISR2_territories_effective_pressure_total'], 1)

    def test_guarantee_requires_actual_escrow_and_includes_cash_reserve(self):
        game = Game(); game.action('labor_yanai')
        game.israel.vars['ISR2_private_available'] = 1
        game.action('controlled_sites'); game.daily(183); game.action('west_bank_projects')
        self.assertAlmostEqual(game.israel.vars['treasury'], 97.8)
        self.assertAlmostEqual(game.israel.vars['ISR2_private_available'], 0)
        game.states[208].controller = 'PAL'; game.daily()
        self.assertAlmostEqual(game.israel.vars['treasury'], 96.4)
        self.assertEqual(len(game.claim_requests), 2)
        self.assertEqual([r['ISR2_private_claim_id'] for r in game.claim_requests], [1, 2])
        for claim in game.claim_requests:
            self.assertAlmostEqual(claim['ISR2_private_claim_amount'], .8)
            self.assertAlmostEqual(claim['ISR2_private_claim_share_USA'], .5)
        again = game.israel.vars['treasury']; game.daily()
        self.assertAlmostEqual(game.israel.vars['treasury'], again)
        game.daily(183)
        self.assertAlmostEqual(game.israel.vars['treasury'], again)

    def test_missing_private_capital_uses_full_public_price(self):
        game = Game(); game.action('labor_yanai'); game.action('controlled_sites')
        self.assertAlmostEqual(game.israel.vars['treasury'], 98.3)
        self.assertEqual(game.israel.vars['ISR2_territories_yanai_used'], 0)

    def test_hotel_is_one_real_matched_project_and_claim_extra_is_point_seven(self):
        game = Game(); game.israel.party = 'western_liberals'
        game.israel.vars['ISR2_private_available'] = .6
        game.action('liberal_hotel_credit'); self.assertAlmostEqual(game.israel.vars['ISR2_private_available'], .6)
        game.action('liberal_sinai_resort')
        self.assertAlmostEqual(game.israel.vars['treasury'], 98.7)
        self.assertAlmostEqual(game.israel.vars['ISR2_private_available'], 0)
        self.assertEqual(game.states[213].extra_slots, 3)
        self.assertEqual(game.states[213].buildings['offices'], 2)
        before = game.israel.vars['treasury']; game.action('liberal_coastal_resort')
        self.assertEqual(game.israel.vars['treasury'], before)
        self.assertEqual(game.states[205].buildings['offices'], 0)
        game.states[213].controller = 'EGY'; game.daily()
        self.assertAlmostEqual(game.israel.vars['treasury'], 98)
        self.assertEqual(game.claim_requests[-1]['ISR2_private_claim_id'], 3)
        self.assertAlmostEqual(game.claim_requests[-1]['ISR2_private_claim_share_USA'], .6)

    def test_native_state_enables_have_explicit_state_wrappers(self):
        state_only = {'is_controlled_by', 'is_owned_by', 'is_core_of', 'has_state_flag'}
        def check_scope(rows, in_state=False):
            for n in rows:
                if n.key in state_only: self.assertTrue(in_state, n.key)
                check_scope(n.children(), True if n.key.isdigit() else False if n.key in ['ISR', 'PAL'] else in_state)
        for dynamic in DYNAMIC.values():
            enable = next(n.children() for n in dynamic if n.key == 'enable')
            check_scope(enable)

    def test_native_public_focus_cost_remains_real_even_in_deficit(self):
        game = Game(); game.israel.vars['treasury'] = 0
        game.action('controlled_sites')
        self.assertAlmostEqual(game.israel.vars['treasury'], -1.5)
        self.assertEqual(game.states[208].buildings['agriculture_district'], 1)
        self.assertEqual(game.israel.vars['ISR2_private_available'], 0)

    def test_real_appropriation_provider_quotes_without_consuming_and_commits_once(self):
        import runtime_domestic
        actual = {}; runtime_domestic._support(actual)
        actual = {k: nodes(v) for k, v in actual.items()}
        with patch.dict(EFFECTS, actual):
            game = Game()
            game.israel.vars.update(ISR2_domestic_settlement_balance=1, ISR2_domestic_settlement_projects=2,
                                    ISR2_project_procurement=1)
            game.israel.flags['ISR2_domestic_tank_coupon'] = None
            game.daily()
            self.assertAlmostEqual(game.israel.vars['ISR2_territories_preview_cost_controlled_sites'], 1)
            self.assertEqual(game.israel.vars['ISR2_domestic_settlement_balance'], 1)
            self.assertEqual(game.israel.vars['ISR2_domestic_settlement_projects'], 2)
            self.assertEqual(game.israel.vars['ISR2_project_procurement'], 0)
            game.action('controlled_sites')
            self.assertAlmostEqual(game.israel.vars['treasury'], 99)
            self.assertAlmostEqual(game.israel.vars['ISR2_domestic_settlement_balance'], .5)
            self.assertEqual(game.israel.vars['ISR2_domestic_settlement_projects'], 1)
            self.assertTrue(game.flag(game.israel, 'ISR2_domestic_tank_coupon'))
            game.action('sinai_projects')
            self.assertAlmostEqual(game.israel.vars['treasury'], 98)
            self.assertEqual(game.israel.vars['ISR2_domestic_settlement_projects'], 0)
            game.action('gaza_projects')
            self.assertAlmostEqual(game.israel.vars['treasury'], 96.5)

    def test_missing_matched_capital_or_control_never_consumes_resort_money(self):
        for failure in ['capital', 'control']:
            game = Game(); game.israel.party = 'western_liberals'; game.israel.vars['ISR2_private_available'] = .6
            game.action('liberal_hotel_credit')
            if failure == 'capital': game.israel.vars['ISR2_private_available'] = 0
            else: game.states[213].controller = 'EGY'
            before = game.israel.vars['treasury']; capital = game.israel.vars['ISR2_private_available']
            game.action('liberal_sinai_resort')
            self.assertEqual(game.israel.vars['treasury'], before)
            self.assertEqual(game.israel.vars['ISR2_private_available'], capital)
            self.assertEqual(game.states[213].buildings['offices'], 0)
            self.assertNotIn('ISR2_liberal_sinai_resort', game.israel.completed)

    def test_refresh_has_no_calendar_advance_or_resistance_reseed(self):
        game = Game(); game.action('labor_yanai')
        expires = game.israel.flags['ISR2_territories_yanai_term']
        game.states[208].resistance = 71
        money = game.israel.vars['treasury']
        for _ in range(20): game.execute(EFFECTS['ISR2_territories_refresh'])
        self.assertEqual(game.israel.flags['ISR2_territories_yanai_term'], expires)
        self.assertEqual(game.israel.vars['treasury'], money)
        self.assertEqual(game.states[208].resistance, 71)
        game.execute(EFFECTS['ISR2_territories_init'])
        self.assertEqual(game.states[208].resistance, 71)


if __name__ == '__main__':
    unittest.main(verbosity=2)
