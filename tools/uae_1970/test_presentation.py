# IMPERIA CW — Cold War: uae 1970 — test presentation.
"""Execute preview arithmetic against the actual programme reconciler AST."""
from __future__ import annotations
from copy import deepcopy
from itertools import product
import importlib.util
import json
import math
from pathlib import Path
import random

import presentation as ui
from revision import current_design
import test_focus_runtime as runtime
from test_focus_runtime import World, parse, first


class Preview(World):
    def __init__(self):
        super().__init__()
        self.lines = []
        self.removals = []
    def execute(self, rows, state=None):
        branch = False
        for key, op, value in rows:
            if key == 'if':
                branch = self.test(first(value, 'limit', []), state)
                if branch:
                    self.execute([r for r in value if r[0] != 'limit'], state)
            elif key == 'else':
                if not branch:
                    self.execute(value, state)
                branch = False
            elif key in {'hidden_effect', 'effect_tooltip'}:
                self.execute(value, state)
            elif key in {'set_variable', 'set_temp_variable', 'add_to_variable', 'subtract_from_variable',
                         'add_to_temp_variable', 'subtract_from_temp_variable', 'multiply_variable',
                         'multiply_temp_variable', 'divide_variable', 'divide_temp_variable'}:
                variable, _, operand = value[0]
                number = self.num(operand)
                if first(value, 'tooltip'):
                    self.lines.append((first(value, 'tooltip'), number))
                if key in {'set_variable', 'set_temp_variable'}:
                    self.variables[variable] = number
                elif key.startswith('multiply_'):
                    self.variables[variable] = self.num(variable) * number
                elif key.startswith('divide_'):
                    self.variables[variable] = self.num(variable) / number
                else:
                    self.variables[variable] = self.num(variable) + (-number if key.startswith('subtract') else number)
            elif key in {'clamp_variable', 'clamp_temp_variable'}:
                var = first(value, 'var')
                self.variables[var] = max(self.num(first(value, 'min', '-inf')), min(self.num(first(value, 'max', 'inf')), self.num(var)))
            elif key == 'remove_dynamic_modifier':
                self.removals.append(first(value, 'modifier'))
                self.dynamic.discard(first(value, 'modifier'))
            elif key in runtime.E:
                self.execute(runtime.E[key], state)
            else:
                super().execute([(key, op, value)], state)


def compiler_programme(data):
    path = ui.ROOT/'tools/uae_1970/compile.py'
    spec = importlib.util.spec_from_file_location('uae_presentation_compiler_fixture', path)
    compiler = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(compiler)
    text = compiler.programme_outputs(data)['common/scripted_effects/COLDWAR_UAE_1970_programmes.txt']
    return {k: v for k, _, v in parse(text)}


def refresh(world):
    world.execute(runtime.E[ui.P+'refresh_programmes'])


def run():
    data = current_design()
    runtime.E.update(compiler_programme(data))
    checks, cases = 0, []
    def check(ok, message):
        nonlocal checks
        checks += 1
        assert ok, message
    loc = {}
    for node in data['nodes']:
        for function in (ui.spirit_change_preview, ui.programme_preview, ui.maritime_oil_preview, ui.special_preview):
            parse(function(node, data, loc))
    used_fallback_keys = sorted(k for k in loc if k.startswith(ui.P+'tt_'))
    check(all(k in ui.native_tooltip_keys() or k in loc for k in
              [ui.native_tooltip_key(k, data, loc) for k in data['modifier_labels']]), 'Unprovided native formatter')
    for modifier in ('political_power_factor', 'stability_factor', 'interest_rate_multiplier_modifier',
                     'research_speed_factor', 'army_org_factor', 'training_time_factor'):
        check(ui.native_tooltip_key(modifier, data, loc) == modifier+'_tt', ('Native formatter replaced', modifier))
    check('$imp_sanction_resistance$' in loc[ui.P+'tt_imp_sanction_resistance'], 'Custom fallback lost native modifier name')
    check('$RIGHT|+=0$' in loc[ui.P+'tt_imp_investment_in_extra'], 'Investment slot fallback wrong units')
    cases.append('Native MD/vanilla formatter preference, named Imperia fallback and numeric units')
    rng = random.Random(1970)
    relief_nodes = [node for node in data['nodes'] if node.get('spirit_changes')]
    for node in relief_nodes:
        others = [n for n in relief_nodes if n['id'] != node['id']]
        scenarios = [set(), {ui._done(node)}, {ui._done(n) for n in others}]
        scenarios += [{ui._done(n) for n in relief_nodes if rng.choice((False, True))} for _ in range(12)]
        for earned, mediation, cabinet in product(scenarios, (False, True), (False, True)):
            before = Preview()
            before.flags = {flag: None for flag in earned}
            if mediation:
                before.flags[ui.P+'mediate_settled'] = None
            if cabinet:
                before.flags[ui.P+'cabinet_settled'] = None
            refresh(before)
            after = deepcopy(before)
            after.flags[ui._done(node)] = None
            refresh(after)
            preview = deepcopy(before)
            preview.lines, preview.removals = [], []
            preview.execute(parse(ui.spirit_change_preview(node, data, loc)))
            expected = []
            seen = set()
            for change in node['spirit_changes']:
                pair = change['spirit'], change['component']
                if pair in seen:
                    continue
                seen.add(pair)
                variable = pair[0]+'_'+pair[1]
                expected.append((ui.native_tooltip_key(pair[1], data, loc), after.num(variable)-before.num(variable)))
            check(len(preview.lines) == len(expected), (node['id'], 'Missing spirit component'))
            for actual, wanted in zip(preview.lines, expected):
                check(actual[0] == wanted[0] and math.isclose(actual[1], wanted[1], abs_tol=1e-9),
                      (node['id'], earned, mediation, cabinet, actual, wanted))
            for spirit in preview.removals:
                check(spirit in before.dynamic and spirit not in after.dynamic, (node['id'], 'Incorrect spirit removal preview'))
    cases.append('Every spirit-change focus against actual reconciler: earned progress, strongest family, cross-family credit, clamps, mediation and cabinet relief')
    # Known marginal examples catch nominal credit being shown as actual relief.
    for focus, earned, expected in [('federal_ministries', {'seven_emirates'}, -0.10),
                                    ('emirate_commands', {'dual_veto'}, 0.02),
                                    ('dual_veto', {'union_command'}, 0.0),
                                    ('technical_institutes', {'national_training', 'technical_cadres'}, 0.0)]:
        node = next(n for n in data['nodes'] if ui._suffix(n) == focus)
        world = Preview(); world.flags = {ui.P+'done_'+key: None for key in earned}; refresh(world)
        world.lines = []; world.execute(parse(ui.spirit_change_preview(node, data, loc)))
        check(math.isclose(world.lines[0][1], expected, abs_tol=1e-9), (focus, 'Nominal relief displayed instead of marginal relief', world.lines))
    cases.append('Explicit incremental examples: federal administration, stronger command credit and already-cleared research burden')
    # The approved routes currently stay below the political stability cap.
    # A copied synthetic candidate proves the same renderer at/near the cap
    # without editing the approved data or changing any actual reward.
    synthetic = deepcopy(data)
    candidate = deepcopy(next(n for n in data['nodes'] if ui._suffix(n) == 'majlis'))
    candidate['id'] = ui.P+'presentation_test_candidate'
    candidate['modifiers'] = {'stability_factor': 0.05}
    synthetic['nodes'].append(candidate)
    runtime.E.update(compiler_programme(synthetic))
    for earned, expected in [({'majlis', 'rulers_compact', 'succession_compact'}, 0.01),
                             ({'majlis', 'rulers_compact', 'succession_compact', 'presentation_test_candidate'}, 0.0),
                             (set(), 0.05)]:
        before = Preview(); before.flags = {ui.P+'done_'+key: None for key in earned}; refresh(before)
        after = deepcopy(before); after.flags[ui._done(candidate)] = None; refresh(after)
        preview = deepcopy(before); preview.lines = []
        preview.execute(parse(ui.programme_preview(candidate, synthetic, loc)))
        actual = preview.lines[0][1]
        check(math.isclose(actual, expected, abs_tol=1e-9) and
              math.isclose(actual, after.num(ui.P+'monarchy_stability_factor')-before.num(ui.P+'monarchy_stability_factor'), abs_tol=1e-9),
              ('Political stability marginal cap incorrect', earned, actual))
    runtime.E.update(compiler_programme(data))
    cases.append('Actual capped political stability marginal: +1pp near cap, zero when earned, full value below cap')
    for focus, earned, expected in [
        ('water_network', {'schools_clinics', 'citizen_housing', 'worker_towns'}, .20),
        ('citizen_housing', {'schools_clinics', 'water_network', 'worker_towns', 'efficient_services'}, 0),
        ('water_network', set(), .30),
    ]:
        candidate = next(n for n in data['nodes'] if ui._suffix(n) == focus)
        before = Preview(); before.flags = {ui.P+'done_'+key: None for key in earned}; refresh(before)
        after = deepcopy(before); after.flags[ui._done(candidate)] = None; refresh(after)
        preview = deepcopy(before); preview.lines = []
        preview.execute(parse(ui.programme_preview(candidate, data, loc)))
        displayed = next(value for key, value in preview.lines if key == 'monthly_population_tt')
        actual = after.num(ui.P+'society_monthly_population')-before.num(ui.P+'society_monthly_population')
        check(math.isclose(displayed, expected, abs_tol=1e-9) and math.isclose(displayed, actual, abs_tol=1e-9),
              ('Population cap marginal preview incorrect', focus, displayed, actual))
    cases.append('Population reward preview shows actual growth below, at and across the total+200% cap')
    oil_phases = ('oil_accounts', 'onshore_expansion', 'offshore_expansion', 'offshore_second_phase')
    scaled = ('agricolture_productivity_modifier', 'offices_productivity', 'social_cost_multiplier_modifier')
    by_suffix = {ui._suffix(n): n for n in data['nodes']}
    for count in range(5):
        for fisheries in ('trading_coast', 'port_planning'):
            before = Preview(); before.flags = {ui.P+'done_'+key: None for key in oil_phases[:count]}
            refresh(before)
            preview = deepcopy(before); preview.lines = []
            node = by_suffix[fisheries]
            preview.execute(parse(ui.programme_preview(node, data, loc)))
            for modifier, original in node['modifiers'].items():
                expected = original*max(.2, 1-.2*count) if modifier in scaled else original
                check(any(key == ui.native_tooltip_key(modifier, data, loc) and math.isclose(value, expected, abs_tol=1e-9)
                          for key, value in preview.lines), (fisheries, count, modifier, 'Wrong scaled advertised fisheries reward', preview.lines))
    cases.append('Both maritime focus previews show current retained80/60/40/20% values after oil development while harbour construction/admin/energy remain full')
    # Compare the real current-to-after reconciler delta with every numeric
    # oil-loss row, including late oil investment and already-earned phases.
    for phase, earned_count, maritime_count, already_done in product(oil_phases, range(5), range(3), (False, True)):
        flags = {ui.P+'done_'+key: None for key in oil_phases[:earned_count] if key != phase}
        flags.update({ui.P+'done_'+key: None for key in ('trading_coast', 'port_planning')[:maritime_count]})
        flags[ui.P+'done_free_zone'] = None  # Must not be reduced by the coastal loss preview.
        if already_done:
            flags[ui.P+'done_'+phase] = None
        before = Preview(); before.flags = flags; refresh(before)
        after = deepcopy(before); after.flags[ui.P+'done_'+phase] = None; refresh(after)
        preview = deepcopy(before); preview.lines = []
        preview.execute(parse(ui.maritime_oil_preview(by_suffix[phase], data, loc)))
        wanted = []
        for modifier in scaled:
            variable = ui.P+'maritime_livelihoods_'+modifier
            wanted.append((ui.native_tooltip_key(modifier, data, loc), after.num(variable)-before.num(variable)))
        if maritime_count:
            for modifier in scaled:
                variable = ui.P+'commerce_'+modifier
                wanted.append((ui.native_tooltip_key(modifier, data, loc), after.num(variable)-before.num(variable)))
        check(len(preview.lines) == len(wanted), (phase, earned_count, maritime_count, already_done, 'Missing oil-transition rows'))
        for actual, expected in zip(preview.lines, wanted):
            check(actual[0] == expected[0] and math.isclose(actual[1], expected[1], abs_tol=1e-9),
                  (phase, earned_count, maritime_count, already_done, actual, expected))
        if not already_done:
            check(preview.lines[0][1] < 0 and preview.lines[2][1] > 0, 'Oil losses must show reduced productivity and increased social costs')
        else:
            check(all(math.isclose(value, 0, abs_tol=1e-9) for _, value in preview.lines), 'Already delivered oil phase previews a duplicate coastal loss')
    cases.append('All four oil previews match actual marginal starting/earned coastal losses in120 contexts, including positive social-cost increases, unrelated commerce retention and no duplicate losses')
    for key in ('nine_states', 'state_participation', 'british_friendship'):
        node = next(n for n in data['nodes'] if ui._suffix(n) == key)
        code = ui.programme_preview(node, data, loc)
        check('custom_effect_tooltip = TT_IF_THEY_ACCEPT' in code, (key, 'Future agreement terms not labelled'))
    charter = next(n for n in data['nodes'] if ui._suffix(n) == 'nine_states')
    world = Preview(); world.execute(parse(ui.programme_preview(charter, data, loc)))
    check(len(world.lines) == 2 and world.lines[-1][1] == 1, 'Unaccepted broad settlement hides its prospective investment reward')
    refresh(world)
    check(world.num(ui.P+'union_imp_investment_in_extra') == 0, 'Preview accidentally activates the unaccepted investment contribution')
    world.flags[ui.P+'broad_charter_accepted'] = None; world.lines = []
    world.execute(parse(ui.programme_preview(charter, data, loc)))
    check(len(world.lines) == 2 and world.lines[-1][1] == 1, 'Accepted broad settlement capacity missing')
    cases.append('Native acceptance label advertises future numbers; actual agreement delivery remains gated')
    conditional_count = 0
    for node in data['nodes']:
        if not node['modifiers'] or node['active_condition'].strip() == 'always = yes':
            continue
        prospective = Preview(); prospective.subject = None
        prospective.variables['ruling_party'] = 2; prospective.governments = {'western_liberals_are_in_power'}
        prospective.execute(parse(ui.programme_preview(node, data, loc)))
        check(bool(prospective.lines), (node['id'], 'Empty numeric preview when its programme is currently inactive'))
        conditional_count += 1
    check(conditional_count == 51, 'Conditional main-programme audit coverage changed')
    shared = next(n for n in data['nodes'] if ui._suffix(n) == 'protected_administration')
    prospective = Preview(); prospective.execute(parse(ui.programme_preview(shared, data, loc)))
    check(('offices_productivity_tt', .08) in prospective.lines and
          ('bureaucracy_cost_multiplier_modifier_tt', -.05) in prospective.lines,
          'The reported Shared Administration hover still omits its actual advertised numbers')
    refresh(prospective)
    check(prospective.num(ui.P+'british_offices_productivity') == 0,
          'Inspecting inactive Shared Administration grants actual office productivity')
    cases.append('All51 conditional main programmes advertise numbers while real delivery remains inactive; screenshot regression shows+8%offices/-5%bureaucracy')
    by = {ui._suffix(n): n for n in data['nodes']}
    planning = ui.special_preview(by['sovereign_union'], data, loc)
    check(planning == 'custom_effect_tooltip = COLDWAR_UAE_unlock_proclamation_tt' and
          loc['COLDWAR_UAE_unlock_proclamation_tt'] == 'Unlocks §Y$COLDWAR_UAE_proclaim_federation$§!.',
          'Planning focus lacks concise truthful continuation')
    proclamation = ui.special_preview(by['proclaim_federation'], data, loc)
    check(proclamation.startswith('drop_cosmetic_tag = yes'), 'Proclamation lacks native name effect')
    check('limit = { COLDWAR_UAE_monarchy_government = yes }' in proclamation,
          'Proclamation promises a dynastic leader for other parties')
    for name, date in [('Zayed bin Sultan Al Nahyan', None), ('Khalifa bin Zayed Al Nahyan', '2004.11.1'),
                       ('Mohammed bin Zayed Al Nahyan', '2022.5.12')]:
        check('name = "'+name+'"' in proclamation and (date is None or 'date > '+date in proclamation),
              (name, 'Missing dated native presidency'))
    check('prime_minister_maktoum' in proclamation and 'prime_minister_rashid' in proclamation,
          'Native cabinet office status omitted')
    check(ui.special_preview(by['dirham'], data, loc) == 'add_ideas = COLDWAR_UAE_dirham_currency', 'Dirham lacks native currency idea')
    for key, event in [('renew_protection', 1001), ('british_friendship', 3001)]:
        check('COLDWAR_UAE_1970_contracts.'+str(event) in ui.special_preview(by[key], data, loc), (key, 'Wrong native event title preview'))
    check('country_event' not in ui.special_preview(by['petition_independence'], data, loc), 'Retired handover event reappeared in preview')
    check('NOT = { has_country_flag = COLDWAR_UAE_friendship_accepted }' in ui.special_preview(by['british_friendship'], data, loc), 'Friendship replay guard absent')
    # Execute the actual politics provider and the native appointment preview
    # across boundaries, exact native party slots and negotiated cabinet terms.
    from test_politics import Country
    dates = ['1971.12.2', '1990.10.6', '1990.10.7', '2004.11.1', '2004.11.2',
             '2006.1.3', '2006.1.4', '2022.5.12', '2022.5.13']
    for date, slot, cabinet in product(dates, (0, 23, 1, 4), (False, True)):
        actual = Country(date=date); actual.subject = None; actual.variables['ruling_party'] = slot
        if cabinet:
            actual.flags.add(ui.P+'cabinet_settled')
        actual.call('politics_sync')
        preview = deepcopy(actual)
        actual.flags.update({ui.P+'done_sovereign_union', ui.P+'done_proclaim_federation', ui.P+'founders_consented'})
        actual.call('form_federation')
        preview.execute(parse(proclamation))
        check((preview.leader, preview.portrait, preview.leader_ideology, preview.traits) ==
              (actual.leader, actual.portrait, actual.leader_ideology, actual.traits),
              ('Native proclamation appointment differs from provider', date, slot, cabinet))
        check(preview.ideas == actual.ideas, ('Native proclamation cabinet differs from provider', date, slot, cabinet))
    cases.append('Native formation, currency and bilateral event previews follow actual dispatch scope')
    report = {'ok': True, 'checks': checks, 'focuses': len(data['nodes']), 'cases': cases,
              'native_formatter_count': len(ui.native_tooltip_keys()), 'fallback_keys': used_fallback_keys,
              'inventory_fallback_keys': sorted(k for k in loc if k.startswith(ui.P+'tt_')),
              'limits': 'Generated AST and actual reconciler comparison; native hover rendering remains unobserved.'}
    (Path(__file__).resolve().parent/'PRESENTATION_VALIDATION.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    run()
