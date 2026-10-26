# IMPERIA CW — Cold War: regression checks for focus-owned Syrian reforms.
"""Execute the emitted authored AST, with named native HOI4 API boundaries.

This is not an engine, budget simulation, save/load or multiplayer-session test.
Unsupported authored conditions/effects fail rather than silently succeeding.
"""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

from validate_content import parse, first, vals, walk
from test_lifecycle import Country

ROOT = Path(__file__).resolve().parents[2]
P = 'COLDWAR_SYR_'


class ReformCountry(Country):
    """Strict local scenario; calls into native politics are recorded boundaries."""
    def __init__(self, bodies):
        super().__init__(bodies)
        self.tag = 'SYR'
        self.variables.update(gdp_total=2.14, political_power=200)
        self.coalition = set()
        self.events = []
        self.native_calls = []
        self.timed_ideas = {}
        self.flag_durations = {}
        self.leader = 'Nureddin al-Atassi'
        self.wars = set()
        self.golan_occupied = True
        self.wargoals = set()
        self.existing_countries = {'SYR', 'SOV', 'IRQ', 'PER', 'EGY', 'LBA', 'LEB', 'ISR', 'USA', 'SAU', 'KUW'}
        self.world = None
        self.from_tag = None
        self.root_tag = self.tag

    def condition(self, body):
        results = []
        for key, op, value in body:
            if key == 'original_tag' or key == 'tag':
                results.append(value == self.tag)
            elif key == 'exists':
                results.append((self.tag in self.existing_countries) == (value == 'yes'))
            elif self.world and key in ('FROM', 'ROOT', *self.world):
                target = self.world[self.from_tag if key == 'FROM' else self.root_tag if key == 'ROOT' else key]
                results.append(target.condition(value))
            elif key == 'check_variable' and first(value, 'var'):
                left, right = self.number(first(value, 'var')), self.number(first(value, 'value'))
                comparison = first(value, 'compare', 'equals')
                results.append({'greater_than_or_equals': left >= right,
                                'greater_than': left > right,
                                'less_than': left < right,
                                'less_than_or_equals': left <= right,
                                'equals': abs(left-right) < 1e-8}[comparison])
            elif key == 'is_in_array':
                slot = first(value, 'value')
                if slot is None:
                    slot = first(value, 'gov_coalition_array')
                results.append(self.number(slot) in self.coalition)
            elif key == 'country_exists':
                results.append(value in self.existing_countries)
            elif key == 'has_war_with':
                results.append((self.from_tag if value == 'FROM' else value) in self.wars)
            elif key == 'has_wargoal_against':
                results.append(value in self.wargoals)
            elif key == 'is_in_faction_with':
                results.append(False)
            elif key == 'ISR':
                results.append(all((self.golan_occupied if field == 'controls_state' else False)
                                   for field, _, target in value))
            elif key == 'has_war':
                results.append(bool(self.wars) == (value == 'yes'))
            elif key == 'has_elections':
                results.append(bool(self.variables.get('elections_allowed', 0)) == (value == 'yes'))
            elif key == 'has_completed_focus':
                results.append(value+'_implemented' in self.flags)
            elif key in self.bodies and value == 'yes':
                results.append(self.condition(self.bodies[key]))
            else:
                results.append(super().condition([(key, op, value)]))
        return all(results)

    def execute(self, body):
        branch = None
        for key, op, value in body:
            if key == 'if':
                branch = self.condition(first(value, 'limit', []))
                if branch:
                    self.execute([row for row in value if row[0] != 'limit'])
            elif key == 'else_if':
                if not branch:
                    branch = self.condition(first(value, 'limit', []))
                    if branch:
                        self.execute([row for row in value if row[0] != 'limit'])
            elif key == 'else':
                if not branch:
                    self.execute(value)
            elif key == 'add_timed_idea':
                idea = first(value, 'idea')
                self.ideas.add(idea)
                self.timed_ideas[idea] = int(first(value, 'days'))
            elif key == 'set_country_flag' and isinstance(value, list):
                flag = first(value, 'flag')
                self.flags.add(flag)
                if first(value, 'days'):
                    self.flag_durations[flag] = int(first(value, 'days'))
            elif key == 'add_ideas':
                self.ideas.add(value)
            elif key == 'remove_ideas':
                self.ideas.discard(value)
                self.timed_ideas.pop(value, None)
            elif key == 'clamp_variable':
                variable = first(value, 'var')
                self.variables[variable] = max(self.number(first(value, 'min')), min(self.number(first(value, 'max')), self.number(variable)))
            elif key in ('multiply_variable', 'divide_variable', 'multiply_temp_variable'):
                variable, _, amount = value[0]
                target = self.temp if key == 'multiply_temp_variable' else self.variables
                target[variable] = self.number(variable)*self.number(amount) if key != 'divide_variable' else self.number(variable)/self.number(amount)
            elif key == 'country_event':
                self.events.append((first(value, 'id'), first(value, 'days', '0')))
            elif self.world and key in ('FROM', 'ROOT', *self.world):
                target = self.world[self.from_tag if key == 'FROM' else self.root_tag if key == 'ROOT' else key]
                target.execute(value)
            elif key in self.existing_countries:
                # Foreign recipient dispatch is recorded, never executed as if
                # it were Syria. Monetary foreign scopes require their own model.
                self.assert_dispatch_only(value)
                self.events.extend((key, first(event, 'id'), first(event, 'days', '0'))
                                   for event in vals(value, 'country_event'))
            elif key == 'set_politics':
                # Only the authored call shape is tested; MD's actual elections
                # and country-ideology assignment are outside this interpreter.
                self.native_calls.append((key, deepcopy(value)))
                if first(value, 'elections_allowed'):
                    self.variables['elections_allowed'] = int(first(value, 'elections_allowed') == 'yes')
            elif key == 'add_coalition_members_effect':
                self.native_calls.append((key, dict(self.temp)))
                self.coalition.add(self.number('add_col_one'))
            elif key in ('unban_party_scripted_call', 'update_dirty_politicsview_expanded',
                         'update_government_coalition_strength', 'update_set_politics',
                         'update_money_dirty_variable', 'force_update_dynamic_modifier',
                         'modify_corporate_tax_rate_effect'):
                self.native_calls.append((key, deepcopy(value)))
            elif key == 'add_political_power':
                self.variables['political_power'] += self.number(value)
            elif key == 'modify_debt_effect':
                self.variables['debt'] += self.number('debt_change')
            else:
                super().execute([(key, op, value)])

    @staticmethod
    def assert_dispatch_only(body):
        if any(key != 'country_event' for key, _, _ in body):
            raise AssertionError('Foreign scope needs explicit modelling: '+str(body))


def loaded_artifacts():
    outputs = {}
    for directory in ['common/scripted_effects', 'common/scripted_triggers',
                      'common/decisions', 'events', 'common/national_focus',
                      'localisation/english']:
        for path in (ROOT/directory).glob('COLDWAR_SYR*'):
            if path.is_file() and path.suffix in ('.txt', '.yml'):
                outputs[path.relative_to(ROOT).as_posix()] = path.read_text(encoding='utf-8-sig')
    return outputs


class StreamliningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if getattr(cls, 'installed', False):
            cls.outputs = loaded_artifacts()
            cls.design = json.loads((ROOT/'tools/syria_1970/manifest.json').read_text(encoding='utf-8'))
        else:
            from streamlining_build import generate
            cls.outputs, cls.design, cls.report = generate()
        cls.bodies = {}
        cls.events = {}
        cls.decisions = {}
        for relative, text in cls.outputs.items():
            if not relative.endswith('.txt'):
                continue
            rows = parse(text)
            if relative.startswith(('common/scripted_effects/', 'common/scripted_triggers/')):
                cls.bodies.update({k: body for k, _, body in rows if isinstance(body, list)})
            elif relative.startswith('events/'):
                cls.events.update({first(body, 'id'): body for body in vals(rows, 'country_event')})
            elif relative.startswith('common/decisions/') and not relative.endswith('COLDWAR_SYR_deferred_projects.txt'):
                for _, _, category in rows:
                    cls.decisions.update({key: body for key, _, body in category if isinstance(body, list)})
        cls.focuses = {first(body, 'id'): body for body in vals(first(parse(cls.outputs['common/national_focus/COLDWAR_SYR_1970_focus.txt']), 'focus_tree'), 'focus')}
        cls.nodes = {n['id']: n for n in cls.design['nodes']}

    def country(self, slot=7):
        country = ReformCountry(self.bodies)
        country.variables['ruling_party'] = slot
        country.execute(self.bodies[P+'initialize_programme_variables'])
        return country

    def focus(self, country, suffix):
        country.execute(self.bodies[P+suffix+'_implement'])

    def linked_world(self):
        tags = ['SYR', 'SOV', 'IRQ', 'PER', 'EGY', 'LBA', 'LEB', 'ISR', 'USA', 'SAU', 'KUW']
        world = {tag: ReformCountry(self.bodies) for tag in tags}
        for tag, country in world.items():
            country.tag = country.root_tag = tag
            country.world = world
        world['ISR'].control.add(587)
        world['SYR'].execute(self.bodies[P+'initialize_programme_variables'])
        return world

    def test_focus_geometry_prerequisites_and_exclusions_preserved(self):
        approved = json.loads((ROOT/'tools/syria_1970/design_source.json').read_text(encoding='utf-8-sig'))
        self.assertEqual(len(self.focuses), 420)
        for node in approved['nodes']:
            focus = self.focuses[node['id']]
            self.assertEqual(float(first(focus, 'x')), node['offset'][0], node['id'])
            self.assertEqual(float(first(focus, 'y')), node['offset'][1], node['id'])
            self.assertEqual(first(focus, 'relative_position_id'), node['anchor'], node['id'])
            self.assertEqual([vals(row, 'focus') for row in vals(focus, 'prerequisite')], node['prerequisites'], node['id'])
            self.assertEqual(vals(first(focus, 'mutually_exclusive', []), 'focus'), node['mutually_exclusive'], node['id'])

    def test_removed_domestic_menus_are_not_advertised(self):
        removed = {P+'decision_'+key for key in ['officer_bargain', 'cabinet_mediation', 'corrective_vote',
                   'guard_bargain', 'front_offer', 'citizenship_review', 'arab_belt', 'enterprise_audit',
                   'tabqa_resettle', 'irrigation_trial', 'budget_review', 'military_transfer']}
        self.assertFalse(removed & self.decisions.keys())
        for relative, text in self.outputs.items():
            if relative.startswith(('common/national_focus/', 'common/decisions/')):
                for key, _, value in walk(parse(text)):
                    if key == 'unlock_decision_tooltip':
                        self.assertNotIn(value, removed, relative)

    def test_pruned_event_and_scripted_provider_references_resolve(self):
        for relative, text in self.outputs.items():
            if not relative.endswith('.txt'):
                continue
            for key, _, value in walk(parse(text)):
                if key == 'country_event':
                    event = first(value, 'id')
                    if event and event.startswith('COLDWAR_SYR_'):
                        self.assertIn(event, self.events, relative)
                elif key.startswith(P) and value == 'yes':
                    self.assertIn(key, self.bodies, relative)

    def test_syrian_focuses_retain_native_deficit_financing(self):
        for suffix in ['opening_military', 'industry_03', 'agriculture_06', 'agriculture_10']:
            with self.subTest(suffix=suffix):
                country = self.country()
                country.variables['treasury'] = -1
                debt = country.variables['debt']
                self.focus(country, suffix)
                node = self.nodes[P+suffix]
                self.assertIn(P+suffix+'_implemented', country.flags)
                self.assertAlmostEqual(country.variables['treasury'], -1-node['treasury_cost_bn'])
                self.assertEqual(country.variables['debt'], debt)
                paid = country.variables['treasury']
                self.focus(country, suffix)
                self.assertAlmostEqual(country.variables['treasury'], paid)

    def test_opening_rewards_secure_compact_without_premature_presidency(self):
        country = self.country()
        self.focus(country, 'opening_military')
        self.assertGreaterEqual(country.variables[P+'officer_backing'], 2)
        self.focus(country, 'opening_corrective')
        for flag in ['cabinet_consent', 'dual_command_resolved', 'corrective_transition']:
            self.assertIn(P+flag, country.flags)
        self.assertEqual(country.leader, 'Nureddin al-Atassi')
        self.focus(country, 'opening_settlement')
        self.focus(country, 'opening_khatib')
        self.assertEqual(country.leader, 'Ahmad al-Khatib')
        self.focus(country, 'opening_khatib_presidential')
        self.assertEqual(country.leader, 'Hafez al-Assad')

    def test_civilian_arbitration_preserves_current_policy_mandate(self):
        country = self.country()
        country.variables[P+'baath_mandate'] = 1
        self.focus(country, 'opening_civilian')
        self.assertEqual(country.variables[P+'baath_mandate'], 1)
        self.assertEqual(country.leader, 'Nureddin al-Atassi')
        self.assertIn(P+'cabinet_consent', country.flags)
        self.assertIn(P+'dual_command_resolved', country.flags)

    def test_appeals_focus_actually_completes_citizenship_review_once(self):
        country = self.country()
        self.focus(country, 'citizenship_03')
        self.assertIn(P+'appeals_commission_open', country.flags)
        self.assertIn(P+'citizenship_review_completed', country.flags)
        self.assertEqual(country.variables[P+'citizenship_stages'], 3)
        self.assertNotIn(P+'discriminatory_settlement', country.flags)
        paid = country.variables['treasury']
        self.focus(country, 'citizenship_03')
        self.assertEqual(country.variables[P+'citizenship_stages'], 3)
        self.assertEqual(country.variables['treasury'], paid)

    def test_audits_resettlement_and_trials_have_real_completion_providers(self):
        cases = [('industry_03', 'enterprise_audits_completed', 'enterprise_audits'),
                 ('fiscal_02', 'enterprise_audits_completed', 'enterprise_audits'),
                 ('agriculture_06', 'reservoir_resettlement_completed', None),
                 ('agriculture_10', 'irrigation_trials_completed', 'irrigation_trials')]
        for suffix, flag, counter in cases:
            with self.subTest(suffix=suffix):
                country = self.country()
                self.focus(country, suffix)
                self.assertIn(P+flag, country.flags)
                if counter:
                    self.assertEqual(country.variables[P+counter], 3)
                paid = country.variables['treasury']
                self.focus(country, suffix)
                self.assertEqual(country.variables['treasury'], paid)

    def test_civilian_transfer_legalises_elections_without_installing_a_party(self):
        country = self.country(slot=22)
        country.leader = 'Provisional Military Council'
        self.focus(country, 'military_council_09')
        self.assertIn(P+'military_transfer_agreed', country.flags)
        self.assertIn(P+'national_pact', country.flags)
        self.assertEqual(country.variables['ruling_party'], 22)
        self.assertEqual(country.leader, 'Provisional Military Council')
        self.assertEqual(country.variables['elections_allowed'], 1)

    def test_recipient_consent_and_real_loan_transfer_remain(self):
        loan = self.events['COLDWAR_SYR_FOREIGN.1']
        self.assertEqual(first(first(loan, 'trigger'), 'tag'), 'SOV')
        consent = next(option for option in vals(loan, 'option')
                       if any(key == 'modify_treasury_effect' for key, _, value in walk(option)))
        actual = first(consent, 'hidden_effect', [])
        transfers = [float(first(value, 'treasury_change')) for key, _, value in walk(actual)
                     if key == 'set_temp_variable' and first(value, 'treasury_change') is not None]
        self.assertEqual(sorted(transfers), [-.2, .2])
        self.assertTrue(any(key == 'set_temp_variable' and float(first(value, 'debt_change', '0')) == .2
                            for key, _, value in walk(actual)))
        for event_id in ['COLDWAR_SYR_WAR.13', 'COLDWAR_SYR_FOREIGN.3', 'COLDWAR_SYR_FOREIGN.6', 'COLDWAR_SYR_FOREIGN.21', 'COLDWAR_SYR_FOREIGN.40']:
            self.assertIn(event_id, self.events)
            self.assertGreaterEqual(len(vals(self.events[event_id], 'option')), 2)

    def test_legacy_modifier_delta_credits_completed_work_without_replaying_grants(self):
        baseline = json.loads((ROOT/'tools/syria_1970/streamlining_baseline.json').read_text(encoding='utf-8'))
        for suffix in ['baath_01', 'industry_03', 'agriculture_06']:
            with self.subTest(suffix=suffix):
                country = self.country()
                node = self.nodes[P+suffix]
                owner = node['owner']
                old = baseline['nodes'][node['id']]['modifiers']
                for modifier, amount in old.items():
                    country.variables[owner+'_'+modifier] = amount
                # Another earned contribution must survive the conversion.
                extra_key = owner+'_'+next(iter(node['modifiers']))
                country.variables[extra_key] = country.number(extra_key)+.17
                country.flags.update({node['id']+'_implemented', owner+'_earned'})
                before = (country.variables['treasury'], country.variables['debt'],
                          deepcopy(country.buildings), deepcopy(country.events), country.leader,
                          deepcopy(country.timed_ideas))
                country.execute(self.bodies[P+'migrate_streamlining_20261021'])
                for modifier in old.keys() | node['modifiers'].keys():
                    key = owner+'_'+modifier
                    self.assertAlmostEqual(country.number(key), node['modifiers'].get(modifier, 0)+(.17 if key == extra_key else 0), modifier)
                self.assertIn(node['id']+'_streamlined_20261021', country.flags)
                self.assertEqual((country.variables['treasury'], country.variables['debt'], country.buildings,
                                  country.events, country.leader, country.timed_ideas), before)
                saved = deepcopy(country.variables)
                country.execute(self.bodies[P+'migrate_streamlining_20261021'])
                self.assertEqual(country.variables, saved)

    def test_fresh_focus_marks_compatibility_before_refresh_and_cannot_double_modifiers(self):
        country = self.country()
        self.focus(country, 'baath_01')
        node = self.nodes[P+'baath_01']
        self.assertIn(node['id']+'_streamlined_20261021', country.flags)
        for modifier, amount in node['modifiers'].items():
            self.assertAlmostEqual(country.number(node['owner']+'_'+modifier), amount)
        before = deepcopy(country.variables)
        country.execute(self.bodies[P+'migrate_streamlining_20261021'])
        self.assertEqual(country.variables, before)

    def test_automatic_pipeline_offer_preserves_authority_and_has_no_free_pp_refund(self):
        country = self.country()
        helper = self.bodies[P+'offer_pipeline']
        political_power = country.variables['political_power']
        country.execute(helper)
        self.assertFalse(country.events)
        self.assertEqual(country.variables['political_power'], political_power)
        country.flags.add(P+'arab_world_09_implemented')
        country.existing_countries.remove('IRQ')
        country.execute(helper)
        self.assertFalse(country.events)
        country.existing_countries.add('IRQ')
        country.wars.add('IRQ')
        country.execute(helper)
        self.assertFalse(country.events)
        country.wars.clear()
        country.execute(helper)
        self.assertIn(P+'pipeline_pending', country.flags)
        self.assertTrue(any(row[0] == 'IRQ' and row[1] == 'COLDWAR_SYR_FOREIGN.3' for row in country.events))
        dispatched = deepcopy(country.events)
        country.execute(helper)
        self.assertEqual(country.events, dispatched)
        self.assertEqual(country.variables['political_power'], political_power)

    def test_invisible_timeouts_clear_state_without_forcing_a_recipient_answer(self):
        events = [body for event_id, body in self.events.items()
                  if event_id.startswith('COLDWAR_SYR_FOREIGN.') and int(event_id.split('.')[1]) >= 100]
        self.assertTrue(events)
        for event in events:
            self.assertEqual(first(event, 'hidden'), 'yes', first(event, 'id'))
            effects = first(event, 'immediate', [])
            self.assertTrue(effects, first(event, 'id'))
            self.assertFalse(any(key == 'modify_treasury_effect' for key, _, value in walk(effects)), first(event, 'id'))

    def test_golan_entry_charges_real_gdp_appropriation_once_despite_deficit(self):
        country = self.country()
        country.wars.add('ISR')
        country.flags.add(P+'limited_war_route')
        country.variables['treasury'] = -.1
        self.focus(country, 'limited_war_entry')
        cost = self.nodes[P+'limited_war_entry']['treasury_cost_bn'] + country.variables['gdp_total']*.0075
        self.assertAlmostEqual(country.variables['treasury'], -.1-cost)
        self.assertIn(P+'operations_funded', country.flags)
        self.assertIn(P+'war_budget_submitted', country.flags)
        paid = country.variables['treasury']
        self.focus(country, 'limited_war_entry')
        self.assertEqual(country.variables['treasury'], paid)

    def test_refused_one_time_pipeline_proposal_can_be_reopened(self):
        country = self.country()
        country.flags.add(P+'arab_world_09_implemented')
        helper = self.bodies[P+'offer_pipeline']
        country.execute(helper)
        self.assertIn(P+'pipeline_pending', country.flags)
        first_dispatch = len(country.events)
        country.flags.discard(P+'pipeline_pending')  # the actual refusal/expiry outcome
        country.execute(helper)
        self.assertGreater(len(country.events), first_dispatch)
        self.assertIn(P+'pipeline_pending', country.flags)

    def test_real_lender_exact_cash_acceptance_and_duplicate_expiry_refusal_guards(self):
        event = self.events['COLDWAR_SYR_FOREIGN.1']
        accept = next(option for option in vals(event, 'option')
                      if any(key == 'modify_treasury_effect' for key, _, value in walk(first(option, 'hidden_effect', []))))
        actual = first(accept, 'hidden_effect')
        for state in ['insufficient', 'exact', 'expired', 'war', 'wrong_recipient']:
            with self.subTest(state=state):
                syria = self.country()
                soviet = ReformCountry(self.bodies)
                soviet.tag = 'USA' if state == 'wrong_recipient' else 'SOV'
                soviet.root_tag = soviet.tag
                soviet.from_tag = 'SYR'
                soviet.variables['treasury'] = .19999 if state == 'insufficient' else .2
                world = {'SYR': syria, 'SOV': soviet, 'USA': soviet}
                syria.world = soviet.world = world
                syria.root_tag = soviet.tag
                if state != 'expired':
                    syria.flags.add(P+'credit_pending')
                if state == 'war':
                    soviet.wars.add('SYR')
                before = (syria.variables['treasury'], syria.variables['debt'], soviet.variables['treasury'])
                soviet.execute(actual)
                after = (syria.variables['treasury'], syria.variables['debt'], soviet.variables['treasury'])
                if state == 'exact':
                    self.assertAlmostEqual(after[0], before[0]+.2)
                    self.assertAlmostEqual(after[1], before[1]+.2)
                    self.assertAlmostEqual(after[2], 0)
                    self.assertNotIn(P+'credit_pending', syria.flags)
                    soviet.execute(actual)
                    self.assertEqual((syria.variables['treasury'], syria.variables['debt'], soviet.variables['treasury']), after)
                else:
                    self.assertEqual(after, before)

    def test_broader_front_admits_only_supported_partners_without_changing_government(self):
        country = self.country()
        country.variables.update({'party_pop_array^4': .08, 'party_pop_array^13': .04})
        self.focus(country, 'baath_02')
        self.assertEqual(country.coalition, {4})
        self.assertEqual(country.variables['party_banned_array^4'], 0)
        self.assertEqual(country.variables['ruling_party'], 7)
        self.assertEqual(country.leader, 'Nureddin al-Atassi')
        paid = country.variables['treasury']
        country.variables['party_pop_array^13'] = .20
        self.focus(country, 'baath_02')
        self.assertEqual(country.coalition, {4})
        self.assertEqual(country.variables['treasury'], paid)

    def test_old_opening_settlements_restore_access_without_replaying_office(self):
        for suffix, expected in [('opening_military', []),
                                 ('opening_civilian', ['cabinet_consent', 'dual_command_resolved']),
                                 ('opening_corrective', ['cabinet_consent', 'dual_command_resolved', 'corrective_transition'])]:
            with self.subTest(suffix=suffix):
                country = self.country()
                country.flags.add(P+suffix+'_implemented')
                country.variables[P+'baath_mandate'] = 1
                country.variables[P+'baath_head'] = 2
                country.leader = 'Hafez al-Assad'
                snapshot = (country.variables['treasury'], country.variables['debt'],
                            country.leader, country.variables[P+'baath_mandate'], country.variables[P+'baath_head'],
                            deepcopy(country.buildings), deepcopy(country.events))
                country.execute(self.bodies[P+'migrate_streamlining_20261021'])
                if suffix == 'opening_military':
                    self.assertGreaterEqual(country.variables[P+'officer_backing'], 2)
                for flag in expected:
                    self.assertIn(P+flag, country.flags)
                self.assertEqual((country.variables['treasury'], country.variables['debt'],
                                  country.leader, country.variables[P+'baath_mandate'], country.variables[P+'baath_head'],
                                  country.buildings, country.events), snapshot)

    def test_standing_preparations_survive_weekly_refresh_before_a_mandate(self):
        world = self.linked_world()
        country = world['SYR']
        country.flags.add(P+'limited_war_route')
        for suffix in ['limited_war_reserves', 'limited_war_depots', 'limited_war_sustainment']:
            self.focus(country, suffix)
        self.assertNotIn(P+'operational_mandate', country.flags)
        owner = self.nodes[P+'limited_war_reserves']['owner']
        relevant = {key: value for key, value in country.variables.items() if key.startswith(owner+'_')}
        costs = country.variables['treasury']
        for _ in range(3):
            country.execute(self.bodies[P+'foreign_weekly'])
            country.execute(self.bodies[P+'refresh_programmes'])
        self.assertEqual({key: value for key, value in country.variables.items() if key.startswith(owner+'_')}, relevant)
        self.assertIn(owner, country.dynamic)
        self.assertGreater(country.variables[owner+'_army_personnel_cost_multiplier_modifier'], 0)
        self.assertGreater(country.variables[owner+'_health_cost_multiplier_modifier'], 0)
        self.assertEqual(country.variables['treasury'], costs)

    def test_legacy_short_lived_preparation_ideas_are_replaced_once(self):
        cases = [('limited_war_reserves', 'war_reserve_readiness'),
                 ('limited_war_depots', 'war_supply_preparation'),
                 ('limited_war_sustainment', 'war_medical_service')]
        for suffix, idea in cases:
            with self.subTest(suffix=suffix):
                country = self.country()
                country.flags.add(P+suffix+'_implemented')
                country.ideas.add(P+idea)
                country.timed_ideas[P+idea] = 120
                country.execute(self.bodies[P+'migrate_streamlining_20261021'])
                self.assertNotIn(P+idea, country.ideas)
                self.assertNotIn(P+idea, country.timed_ideas)
                # A repeated synchronization cannot become a blanket purge.
                country.ideas.add(P+idea)
                country.execute(self.bodies[P+'migrate_streamlining_20261021'])
                self.assertIn(P+idea, country.ideas)

    def test_operational_cabinet_credits_live_funding_and_only_renews_expired_budget(self):
        decision = self.decisions[P+'decision_war_appropriation']
        for authority in ['war', 'goal', 'invalid']:
            for funded in [False, True]:
                with self.subTest(authority=authority, funded=funded):
                    world = self.linked_world()
                    country = world['SYR']
                    country.flags.add(P+'limited_war_entry_implemented')
                    country.variables['treasury'] = -.2
                    if authority == 'war':
                        country.wars.add('ISR')
                    elif authority == 'goal':
                        country.wargoals.add('ISR')
                    if funded:
                        country.flags.add(P+'operations_funded')
                    available = country.condition(first(decision, 'available'))
                    self.assertEqual(available, authority != 'invalid')
                    if not available:
                        continue
                    country.execute(first(decision, 'remove_effect'))
                    expected = -.2 - (0 if funded else country.variables['gdp_total']*.0075)
                    self.assertAlmostEqual(country.variables['treasury'], expected)
                    self.assertIn(P+'operational_mandate', country.flags)
                    self.assertIn(P+'operations_funded', country.flags)
                    self.assertFalse(country.condition(first(decision, 'available')))
                    country.execute(first(decision, 'remove_effect'))
                    self.assertAlmostEqual(country.variables['treasury'], expected)

    def test_weekly_pipeline_transfer_credits_old_month_and_handles_exact_or_failed_payment(self):
        for payment in [.00093, .00092]:
            with self.subTest(payment=payment):
                world = self.linked_world()
                syria, iraq = world['SYR'], world['IRQ']
                syria.flags.update({P+'pipeline_operating', P+'pipeline_payment_month'})
                iraq.flags.add(P+'pipeline_operating')
                syria.ideas.add(P+'pipeline_administration')
                iraq.ideas.add(P+'pipeline_access')
                iraq.variables['treasury'] = payment
                balance = syria.variables['treasury']
                syria.execute(self.bodies[P+'foreign_weekly'])
                self.assertEqual(iraq.variables['treasury'], payment)
                self.assertEqual(syria.variables['treasury'], balance)
                self.assertNotIn(P+'pipeline_payment_week', syria.flags)
                # The fixture advances the pre-existing timer explicitly; it
                # does not claim to simulate HOI4's flag expiry clock.
                syria.flags.discard(P+'pipeline_payment_month')
                syria.execute(self.bodies[P+'foreign_weekly'])
                self.assertEqual(syria.flag_durations[P+'pipeline_payment_week'], 7)
                if payment == .00093:
                    self.assertAlmostEqual(iraq.variables['treasury'], 0)
                    self.assertAlmostEqual(syria.variables['treasury'], balance+.00093)
                    after = (iraq.variables['treasury'], syria.variables['treasury'])
                    syria.execute(self.bodies[P+'foreign_weekly'])
                    self.assertEqual((iraq.variables['treasury'], syria.variables['treasury']), after)
                else:
                    self.assertEqual(iraq.variables['treasury'], payment)
                    self.assertEqual(syria.variables['treasury'], balance)
                    self.assertNotIn(P+'pipeline_operating', syria.flags)
                    self.assertNotIn(P+'pipeline_operating', iraq.flags)
                    self.assertNotIn(P+'pipeline_administration', syria.ideas)
                    self.assertNotIn(P+'pipeline_access', iraq.ideas)


if __name__ == '__main__':
    if '--installed' in sys.argv:
        sys.argv.remove('--installed')
        # A class attribute avoids passing a non-unittest flag to its parser.
        StreamliningTests.installed = True
    unittest.main(verbosity=2)
