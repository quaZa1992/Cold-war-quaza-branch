# IMPERIA COLD WAR — Native-AST checks for retired Israel callbacks and refunds.
"""Bounded source/transaction tests, not save-load or HOI4 engine evidence."""
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
import ast
import unittest

import runtime_legacy as emitter
from focus_prerequisite_ui import nodes, field

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = emitter.build()
REFUNDS = OUTPUT['metadata']['reservations']
PROTECTED = set(x for item in OUTPUT['metadata']['inventory'].values() for x in item['protected_events'])


class Country:
    def __init__(self, tag):
        self.tag = tag
        self.vars = {'treasury': Decimal(100)}
        self.temps = {}
        self.flags = set()
        self.exists = True


class Model:
    """Strictly execute actual guarded bodies and the current native cash helper."""
    def __init__(self):
        self.countries = {tag: Country(tag) for tag in ['ISR', 'PAL', 'EGY', 'USA', 'SYR']}
        self.controllers = {214: 'EGY'}
        self.global_flags = set()
        self.dirty = 0
        self.effects = {n.key: n.children() for n in nodes(OUTPUT['files']['common/scripted_effects/ISR2_legacy_effects.txt'])}
        native = (ROOT / 'common/scripted_effects/00_budget_effects.txt').read_bytes().decode('utf-8-sig')
        self.effects['modify_treasury_effect'] = next(n.children() for n in nodes(native) if n.key == 'modify_treasury_effect')
        # The complete Egyptian event is also compared byte-for-byte. The canal
        # world's independent implementation is not simulated by this fixture.
        self.effects['mdcw_suez_reopen_historical_canal'] = nodes('set_country_flag = EGY_CANAL_OPENED_TEST')
        self.countries['ISR'].flags.add('ISR2_enabled')

    def snapshot(self):
        return deepcopy((self.countries, self.controllers, self.global_flags, self.dirty))

    def state(self):
        return {tag: (dict(c.vars), dict(c.temps), set(c.flags), c.exists) for tag, c in self.countries.items()}, self.dirty

    def value(self, scope, raw):
        try: return Decimal(str(raw))
        except Exception: return scope.temps.get(str(raw), scope.vars.get(str(raw), Decimal(0)))

    def condition(self, rows, scope):
        for row in rows:
            key, value, children = row.key, row.value, row.children()
            if key == 'NOT': result = not self.condition(children, scope)
            elif key == 'AND': result = self.condition(children, scope)
            elif key == 'OR': result = any(self.condition([c], scope) for c in children)
            elif key in self.countries: result = self.condition(children, self.countries[key])
            elif key in ('tag', 'original_tag'): result = scope.tag == value
            elif key == 'has_country_flag': result = value in scope.flags
            elif key == 'has_variable': result = value in scope.vars
            elif key == 'exists': result = scope.exists == (value == 'yes')
            elif key == 'IMP_is_1970_scenario': result = True
            elif key == 'controls_state': result = self.controllers[int(value)] == scope.tag
            elif key == 'has_war_with': result = False
            elif key == 'has_global_flag': result = value in self.global_flags
            elif key == 'always': result = value == 'yes'
            elif key == 'check_variable':
                c = children[0]
                left, right = self.value(scope, c.key), self.value(scope, c.value)
                result = left > right if c.op == '>' else left == right
            else: raise AssertionError(('Unsupported condition reached', key))
            if not result: return False
        return True

    def execute(self, rows, scope='ISR'):
        scope = self.countries[scope] if isinstance(scope, str) else scope
        previous = None
        for row in rows:
            key, value, children = row.key, row.value, row.children()
            if key == 'if':
                limit = next(c.children() for c in children if c.key == 'limit')
                previous = self.condition(limit, scope)
                if previous: self.execute([c for c in children if c.key != 'limit'], scope)
            elif key == 'else':
                if previous is False: self.execute(children, scope)
                previous = None
            elif key in self.countries: self.execute(children, self.countries[key])
            elif key in ('set_variable', 'set_temp_variable', 'add_to_variable'):
                c = children[0]; target = scope.temps if key == 'set_temp_variable' else scope.vars
                amount = self.value(scope, c.value)
                target[c.key] = target.get(c.key, Decimal(0)) + amount if key == 'add_to_variable' else amount
            elif key == 'clear_variable': scope.vars.pop(value, None)
            elif key == 'set_country_flag': scope.flags.add(value)
            elif key == 'clr_country_flag': scope.flags.discard(value)
            elif key == 'custom_effect_tooltip': pass
            elif key == 'update_money_dirty_variable': self.dirty += 1
            elif key in self.effects: self.execute(self.effects[key], scope)
            else: raise AssertionError(('Retired effect unexpectedly reached', key))


def event_map(source):
    return {field(n.children(), 'id'): n for n in nodes(source) if n.key == 'country_event'}


class LegacyRuntimeTests(unittest.TestCase):
    def test_pure_fresh_patch_is_idempotent_and_keeps_canals_exactly(self):
        before = {path: (ROOT/path).read_bytes() for path in emitter.EVENT_PATHS + emitter.OCCUPATION_PATHS}
        first = emitter.build()
        second = emitter.build(sources=first['files'])
        self.assertEqual(first['files'], second['files'])
        for path, raw in before.items():
            self.assertEqual((ROOT/path).read_bytes(), raw, path)
            self.assertTrue(first['files'][path].startswith(emitter.MARK if path in emitter.EVENT_PATHS else emitter.OCC_MARK))
            if path not in emitter.EVENT_PATHS: continue
            original = event_map(raw.decode('utf-8-sig'))
            if emitter.EXEMPT in original:
                old = original[emitter.EXEMPT]
                source = first['files'][path]; new = event_map(source)[emitter.EXEMPT]
                self.assertEqual(raw.decode('utf-8-sig')[old.start:old.end], source[new.start:new.end])

    def test_every_retired_callback_and_option_is_effect_guarded(self):
        self.assertEqual(len(PROTECTED), 76)
        self.assertEqual(len(REFUNDS), 40)
        effect_bodies = []
        for path in emitter.EVENT_PATHS:
            for event_id, event in event_map(OUTPUT['files'][path]).items():
                if event_id == emitter.EXEMPT: continue
                trigger = next(n for n in event.children() if n.key == 'trigger')
                self.assertTrue(emitter.contains_guard(trigger.children()), event_id)
                for child in event.children():
                    if child.key == 'immediate': effect_bodies.append(child.children())
                    if child.key == 'option' and field(child.children(), 'name') != emitter.DISMISS:
                        option_trigger = next(n for n in child.children() if n.key == 'trigger')
                        self.assertTrue(emitter.contains_guard(option_trigger.children()), event_id)
                        effect_bodies.append([n for n in child.children() if n.key not in emitter.OPTION_METADATA])
        self.assertEqual(len(effect_bodies), 115)  # 72 options plus43 immediate callbacks.
        for tag in ['ISR', 'PAL', 'EGY', 'USA', 'SYR']:
            model = Model(); before = model.state()
            # Deliberately bypass all event/option trigger checks, as an already
            # open or forced callback can do. Only the real effect guards matter.
            for body in effect_bodies: model.execute(body, tag)
            self.assertEqual(model.state(), before, tag)

    def test_already_open_visible_events_have_a_nontransactional_exit(self):
        count = 0
        for path in emitter.EVENT_PATHS:
            for event_id, event in event_map(OUTPUT['files'][path]).items():
                if event_id == emitter.EXEMPT or field(event.children(), 'hidden') == 'yes': continue
                options = [n for n in event.children() if n.key == 'option' and field(n.children(), 'name') == emitter.DISMISS]
                self.assertEqual(len(options), 1)
                trigger = next(n.children() for n in options[0].children() if n.key == 'trigger')
                for tag in ['ISR', 'PAL', 'EGY']:
                    model = Model()
                    self.assertTrue(model.condition(trigger, model.countries[tag]))
                self.assertTrue(all(n.key in emitter.OPTION_METADATA for n in options[0].children()))
                count += 1
        self.assertEqual(count, 33)

    def test_exact_original_amount_returns_once_without_gdp_requotation(self):
        self.assertNotIn('gdp_total', OUTPUT['files']['common/scripted_effects/ISR2_legacy_effects.txt'])
        for i, record in enumerate(REFUNDS):
            model = Model(); israel = model.countries['ISR']
            amount = Decimal('0.00001') + Decimal(i) / Decimal(10000)
            israel.vars[record['paid']] = amount
            israel.vars['gdp_total'] = Decimal(999999)
            israel.flags.add(record['active'])
            model.execute(model.effects['ISR2_legacy_refund_pending'])
            self.assertEqual(israel.vars['treasury'], Decimal(100)+amount)
            self.assertNotIn(record['paid'], israel.vars)
            self.assertNotIn(record['active'], israel.flags)
            before = model.state(); model.execute(model.effects['ISR2_legacy_refund_pending'])
            self.assertEqual(model.state(), before)

    def test_completed_unpaid_and_orphan_records_are_never_refunded(self):
        record = REFUNDS[0]
        for variant in ['done', 'zero', 'negative', 'no_active', 'no_paid', 'new_save']:
            model = Model(); israel = model.countries['ISR']
            if variant != 'new_save':
                israel.flags.add(record['active']); israel.vars[record['paid']] = Decimal(2)
            if variant == 'done': israel.flags.add(record['done'])
            if variant == 'zero': israel.vars[record['paid']] = Decimal(0)
            if variant == 'negative': israel.vars[record['paid']] = Decimal(-2)
            if variant == 'no_active': israel.flags.remove(record['active'])
            if variant == 'no_paid': israel.vars.pop(record['paid'])
            before = model.state(); model.execute(model.effects['ISR2_legacy_refund_pending'])
            self.assertEqual(model.state(), before, variant)
        self.assertNotIn('remove_building', OUTPUT['files']['common/scripted_effects/ISR2_legacy_effects.txt'])
        self.assertNotIn('add_building', OUTPUT['files']['common/scripted_effects/ISR2_legacy_effects.txt'])

    def test_skip_treasury_flag_defers_claim_without_erasing_it(self):
        record = REFUNDS[1]; model = Model(); israel = model.countries['ISR']
        israel.vars[record['paid']] = Decimal('0.62874'); israel.flags.update([record['active'], 'MD_skip_treasury_cost'])
        before = model.state(); model.execute(model.effects['ISR2_legacy_refund_pending'])
        self.assertEqual(model.state(), before)
        israel.flags.remove('MD_skip_treasury_cost'); model.execute(model.effects['ISR2_legacy_refund_pending'])
        self.assertEqual(israel.vars['treasury'], Decimal('100.62874'))

    def test_refund_helper_never_pays_other_country_scopes(self):
        record = REFUNDS[2]; model = Model(); egypt = model.countries['EGY']
        egypt.flags.update(['ISR2_enabled', record['active']]); egypt.vars[record['paid']] = Decimal(5)
        before = model.state(); model.execute(model.effects['ISR2_legacy_refund_pending'], 'EGY')
        self.assertEqual(model.state(), before)

    def test_egypt_1160_still_completes_or_refunds_its_own_project(self):
        source = OUTPUT['files']['events/ISR70_policy_events.txt']
        event = event_map(source)[emitter.EXEMPT]
        body = next(n.children() for n in event.children() if n.key == 'immediate')
        for success in [True, False]:
            model = Model(); egypt = model.countries['EGY']
            egypt.flags.add('ISR70_policy_egypt_canal_project')
            egypt.vars['ISR70_policy_egypt_canal_paid'] = Decimal('0.75')
            if not success: model.controllers[214] = 'ISR'
            model.execute(body, 'EGY')
            self.assertEqual('EGY_CANAL_OPENED_TEST' in egypt.flags, success)
            self.assertEqual(egypt.vars['treasury'], Decimal(100) if success else Decimal('100.75'))
            self.assertNotIn('ISR70_policy_egypt_canal_paid', egypt.vars)
            self.assertNotIn('ISR70_policy_egypt_canal_project', egypt.flags)

    def test_durable_global_marker_survives_israeli_annexation_and_beta_upgrades(self):
        beta = {path: OUTPUT['files'][path].replace(emitter.ENABLED, emitter.ACTOR_ENABLED) for path in emitter.EVENT_PATHS}
        upgraded = emitter.build(sources=beta)
        self.assertEqual(upgraded['files'], emitter.build(sources=upgraded['files'])['files'])
        model = Model(); model.countries['ISR'].flags.clear(); model.countries['ISR'].exists = False
        model.global_flags.add('ISR2_legacy_replaced')
        before = model.state()
        for path in emitter.EVENT_PATHS:
            for event_id, event in event_map(upgraded['files'][path]).items():
                if event_id == emitter.EXEMPT: continue
                for child in event.children():
                    if child.key == 'immediate': model.execute(child.children(), 'PAL')
                    if child.key == 'option':
                        if field(child.children(), 'name') == emitter.DISMISS:
                            trigger = next(n.children() for n in child.children() if n.key == 'trigger')
                            self.assertTrue(model.condition(trigger, model.countries['PAL']))
                        else:
                            model.execute([n for n in child.children() if n.key not in emitter.OPTION_METADATA], 'PAL')
        self.assertEqual(model.state(), before)
        record = REFUNDS[0]
        model.countries['ISR'].flags.add(record['active'])
        model.countries['ISR'].vars[record['paid']] = Decimal(7)
        before = model.state(); model.execute(model.effects['ISR2_legacy_refund_pending'])
        self.assertEqual(model.state(), before)  # A global marker cannot pay a dead or unenabled actor.

    def test_four_legacy_state_enables_and_template_change_only_scope(self):
        path, template_path = emitter.OCCUPATION_PATHS
        original = (ROOT/path).read_bytes().decode('utf-8-sig')
        patched = OUTPUT['files'][path]
        old = {n.key: n for n in nodes(original)}
        new = {n.key: n for n in nodes(patched)}
        self.assertEqual(set(old), set(new))
        wanted = {f'ISR70_policy_occupation_{s}_local': s for s in (208, 209, 213, 587)}
        for key, prior in old.items():
            after = new[key]
            if key not in wanted:
                self.assertEqual(original[prior.start:prior.end], patched[after.start:after.end], key)
                continue
            self.assertEqual(emitter.semantic([n for n in prior.children() if n.key != 'enable']),
                             emitter.semantic([n for n in after.children() if n.key != 'enable']))
            enable = next(n for n in after.children() if n.key == 'enable')
            self.assertFalse(any(n.key in ['is_controlled_by', 'is_core_of', 'NOT'] for n in enable.children()))
            wrapper = next(n for n in enable.children() if n.key == str(wanted[key]))
            self.assertEqual(emitter.semantic(wrapper.children()), emitter.semantic(nodes('is_controlled_by = ISR NOT = { is_core_of = ISR }')))
        before_ast = ast.parse((ROOT/template_path).read_bytes().decode('utf-8-sig'))
        after_ast = ast.parse(OUTPUT['files'][template_path])
        before_gate = next(n for n in ast.walk(before_ast) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'state_gate' for t in n.targets))
        after_gate = next(n for n in ast.walk(after_ast) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'state_gate' for t in n.targets))
        gate_expression = ast.Expression(after_gate.value)
        self.assertTrue(all(isinstance(n, (ast.Expression, ast.JoinedStr, ast.FormattedValue, ast.Constant, ast.Name, ast.Load)) for n in ast.walk(gate_expression)))
        for state in wanted.values():
            result = eval(compile(gate_expression, '<state_gate>', 'eval'), {'__builtins__': {}}, {'state': state})
            parsed = nodes(result)
            self.assertEqual(parsed[0].key, str(state))
            self.assertEqual(emitter.semantic(parsed[0].children()), emitter.semantic(nodes('is_controlled_by = ISR NOT = { is_core_of = ISR }')))
        before_gate.value = ast.Constant('SCOPE_ONLY')
        after_gate.value = ast.Constant('SCOPE_ONLY')
        self.assertEqual(ast.dump(before_ast), ast.dump(after_ast))


if __name__ == '__main__':
    unittest.main(verbosity=2)
