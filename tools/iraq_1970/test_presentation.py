# IMPERIA CW — Cold War: iraq 1970 — test presentation.
"""Read-only regression checks for the installed Iraqi focus presentation.

Run with ``python tools/iraq_1970/test_presentation.py``. The only written file
is PRESENTATION_TEST_REPORT.json beside this script. No compiler/generator is
run and no game file is changed. AST checks establish source consistency, not
the appearance of an actual HOI4 hover or runtime effect_tooltip behavior.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import unittest

import compile as compiler
import decisions_module
from common import ROOT, P, first, parse, values

HERE = Path(__file__).resolve().parent
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
MD = Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
REPORT_PATH = HERE / 'PRESENTATION_TEST_REPORT.json'
FOCUS_FILE = ROOT / 'common/national_focus/COLDWAR_IRQ_1970_focus.txt'
QUEUE_FILE = ROOT / 'common/decisions/COLDWAR_IRQ_1970_pending.txt'
REWARD_FILE = ROOT / 'common/scripted_effects/COLDWAR_IRQ_1970_rewards.txt'
TRIGGER_FILE = ROOT / 'common/scripted_triggers/COLDWAR_IRQ_1970_triggers.txt'
IDEA_FILE = ROOT / 'common/ideas/COLDWAR_IRQ_1970_starting_ideas.txt'
DYNAMIC_FILE = ROOT / 'common/dynamic_modifiers/COLDWAR_IRQ_1970_programmes.txt'
LOC_FILE = ROOT / 'localisation/english/COLDWAR_IRQ_1970_focus_l_english.yml'
LEADERS = {
    P + 'leader_bakr_in_office': 'Ahmed Hassan al-Bakr',
    P + 'leader_saddam_in_office': 'Saddam Hussein',
    P + 'leader_aziz_muhammad_in_office': 'Aziz Muhammad',
}
SPIRIT_NODES = {
    'ministerial_audit', 'autonomy_guarantees', 'professional_command',
    'national_front', 'baath_monopoly', 'foreign_border_delivery',
    'oil_state_company', 'oil_concession_delivery', 'oil_field_maintenance',
    'agri_cooperatives', 'agri_smallholders', 'agri_extension',
    'agri_distribution', 'agri_reform_delivery',
}
CUSTOM_SUPPORT_TT = P + 'presentation_support_effectiveness_tt'
CHECKS: dict = {}


def read(path):
    return path.read_text(encoding='utf-8-sig')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def walk(rows):
    for row in rows:
        yield row
        if isinstance(row[2], list):
            yield from walk(row[2])


def localization_lines(path):
    for number, line in enumerate(read(path).splitlines(), 1):
        match = re.match(r'^\s*([^\s:#]+):(?:\d+)?\s*"(.*)"\s*$', line)
        if match:
            yield match.group(1), match.group(2), number


def conjunction(children):
    """Canonicalize only associative AND; retain scopes and OR/NOT operators."""
    result = []
    for child in children:
        if child[0] == 'AND':
            result.extend(child[1])
        else:
            result.append(child)
    return 'AND', tuple(result)


def normalize_condition(row, leader_providers):
    key, operator, value = row
    if key in ('custom_trigger_tooltip', 'hidden_trigger'):
        return conjunction(normalize_condition(r, leader_providers)
                           for r in value if r[0] != 'tooltip')
    if key in leader_providers and value == 'yes':
        return conjunction(normalize_condition(r, leader_providers)
                           for r in leader_providers[key])
    if isinstance(value, list):
        if key == 'AND':
            return conjunction(normalize_condition(r, leader_providers) for r in value)
        if key == 'OR':
            children = []
            for child in value:
                item = normalize_condition(child, leader_providers)
                if item[0] == 'AND' and len(item[1]) == 1:
                    item = item[1][0]
                children.append(item)
            return key, operator, tuple(children)
        return key, operator, conjunction(normalize_condition(r, leader_providers)
                                          for r in value)
    return key, operator, value


def normalize(rows, leader_providers):
    return conjunction(normalize_condition(r, leader_providers) for r in rows)


class PresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        compiler.CONDITIONS.update(decisions_module.CONTRACTS)
        compiler.CONDITIONS.update(compiler.OWN_CONDITIONS)
        cls.nodes = [n for n in compiler.NODES if not n.get('audit_retired')]
        tree = first(parse(read(FOCUS_FILE)), 'focus_tree')
        cls.focuses = {first(body, 'id'): body for body in values(tree, 'focus')}
        queue = first(parse(read(QUEUE_FILE)), P + 'pending_projects')
        cls.deliveries = {key: body for key, op, body in queue if isinstance(body, list)}
        cls.appliers = {key: body for key, op, body in parse(read(REWARD_FILE))}
        cls.leaders = {key: body for key, op, body in parse(read(TRIGGER_FILE))
                       if key in LEADERS}
        cls.ideas = {key: body for key, op, body in
                     first(first(parse(read(IDEA_FILE)), 'ideas'), 'country')}
        cls.dynamic = {key: body for key, op, body in parse(read(DYNAMIC_FILE))}
        cls.loc = dict((key, text) for key, text, number in localization_lines(LOC_FILE))

    def test_approved_focus_set_and_named_leader_providers(self):
        self.assertEqual(len(self.focuses), 426)
        self.assertEqual(set(self.focuses), {n['id'] for n in compiler.NODES})
        for n in compiler.NODES:
            if n.get('audit_retired'):
                self.assertEqual(first(self.focuses[n['id']],'allow_branch'),[('always','=','no')])
                self.assertEqual(first(self.focuses[n['id']],'available'),[('always','=','no')])
        for key, name in LEADERS.items():
            self.assertEqual(self.leaders[key], [('has_country_leader', '=',
                             [('name', '=', '"' + name + '"'), ('ruling_only', '=', 'yes')])])
        CHECKS['focuses'] = len(self.focuses)

    def test_all_approved_modifier_operands_and_headings(self):
        node_count = operand_count = 0
        for n in self.nodes:
            rewards = first(self.focuses[n['id']], 'completion_reward')
            actual = []
            for tooltip in values(rewards, 'effect_tooltip'):
                for key, operator, value in walk(tooltip):
                    if key != 'add_to_variable':
                        continue
                    operands = [(k, op, v) for k, op, v in value if k != 'tooltip']
                    self.assertEqual(len(operands), 1, n['id'])
                    variable, assignment, number = operands[0]
                    self.assertEqual(assignment, '=', n['id'])
                    prefix = P + n['group'] + '_'
                    self.assertTrue(variable.startswith(prefix), (n['id'], variable))
                    modifier = variable[len(prefix):]
                    actual.append((modifier, float(number)))
                    expected_tt = compiler.presentation._modifier_tooltip(modifier)
                    self.assertEqual(first(value, 'tooltip'), expected_tt, n['id'])
            self.assertEqual(Counter(actual), Counter(n['modifiers'].items()), n['id'])
            if actual:
                node_count += 1
                heading = [('localization_key', '=', 'modifies_dynamic_modifier_tt'),
                           ('MODIFIER', '=', P + n['group'] + '_programme')]
                self.assertIn(heading, values(rewards, 'custom_effect_tooltip'), n['id'])
                self.assertIn(P + n['group'] + '_programme', self.dynamic)
                self.assertIn(P + n['group'] + '_programme', self.loc)
            operand_count += len(actual)
        self.assertEqual(node_count,sum(bool(n['modifiers']) for n in self.nodes))
        self.assertEqual(operand_count,sum(len(n['modifiers']) for n in self.nodes))
        CHECKS['numeric_focus_nodes'] = node_count
        CHECKS['exact_approved_modifier_operands'] = operand_count

    def test_all_852_availability_views_preserve_predicates(self):
        checked = 0
        for n in self.nodes:
            for delivery in (False, True):
                emitted = (self.deliveries[n['id'] + '_delivery'] if delivery
                           else self.focuses[n['id']])
                actual = first(emitted, 'available')
                expected = parse(compiler.eligible(n, delivery))
                self.assertEqual(normalize(actual, self.leaders),
                                 normalize(expected, self.leaders), (n['id'], delivery))
                checked += 1
        self.assertEqual(checked, 2*len(self.nodes))
        CHECKS['semantically_identical_availability_views'] = checked

    def test_one_hidden_actual_apply_and_no_executed_previews(self):
        for n in self.nodes:
            rewards = first(self.focuses[n['id']], 'completion_reward')
            helper = P + 'apply_' + n['key']
            self.assertIn(helper, self.appliers)
            self.assertEqual(values(rewards, 'hidden_effect'), [[(helper, '=', 'yes')]], n['id'])
            for key, operator, value in rewards:
                self.assertIn(key, ('custom_effect_tooltip', 'effect_tooltip', 'hidden_effect', 'unlock_decision_tooltip'), n['id'])
            complete = first(self.deliveries[n['id'] + '_delivery'], 'complete_effect')
            self.assertEqual(values(complete,'hidden_effect'),[[(helper, '=', 'yes')]],n['id'])
            self.assertTrue(all(k in ('custom_effect_tooltip','effect_tooltip','hidden_effect') for k,o,v in complete),n['id'])
        CHECKS['single_hidden_apply_helpers'] = len(self.nodes)
        CHECKS['preview_effects_execute_outside_effect_tooltip'] = 0

    def test_native_treasury_estimates_and_fixed_quotes(self):
        """Evaluate preview arithmetic, not the engine's tooltip renderer."""
        funded=unlocks=0
        for n in self.nodes:
            rewards=first(self.focuses[n['id']], 'completion_reward')
            self.assertEqual(values(rewards,'unlock_decision_tooltip'),[d['id'] for d in n['decisions']],n['id'])
            unlocks+=len(n['decisions'])
            bills=[body for body in values(rewards,'effect_tooltip') if first(body,'modify_treasury_effect')=='yes']
            if not n['budget_gdp_share']:
                self.assertFalse(bills,n['id']);continue
            funded+=1;self.assertEqual(len(bills),1,n['id'])
            for quoted,gdp,invoice in ((False,10,9),(False,20,9),(True,10,.725),(True,200,.725)):
                persistent={'gdp_total':gdp,n['id']+'_invoice':invoice};before=dict(persistent);temp={};seen=[]
                def execute(rows):
                    for key,op,body in rows:
                        if key=='set_temp_variable':
                            name,_,value=body[0];temp[name]=persistent.get(value,float(value) if re.fullmatch(r'-?\d+(?:\.\d+)?',value) else 0)
                        elif key=='multiply_temp_variable':
                            name,_,value=body[0];temp[name]*=float(value)
                        elif key=='if':
                            self.assertEqual(first(body,'limit'),[('has_country_flag','=',n['id']+'_quoted')])
                            if quoted:execute([r for r in body if r[0]!='limit'])
                        elif key=='modify_treasury_effect':
                            self.assertEqual(body,'yes');seen.append(temp['treasury_change'])
                        else:self.fail('Unexpected native-cost preview operation '+key)
                execute(bills[0])
                self.assertEqual(len(seen),1)
                self.assertAlmostEqual(seen[0],-invoice if quoted else -gdp*n['budget_gdp_share'],msg=n['id'])
                self.assertEqual(before,persistent,'Preview changed a quote or GDP')
        CHECKS['funded_focuses_with_native_treasury_preview']=funded
        CHECKS['native_decision_unlock_previews']=unlocks

    def test_front_and_monopoly_previews_share_actual_contract_conditions(self):
        """Prospective numbers stay visible; real grants retain treaty gates."""
        from test_audit_transactions import AuditWorld
        programmes = 'common/scripted_effects/COLDWAR_IRQ_1970_programmes.txt'
        migration = 'common/scripted_effects/COLDWAR_IRQ_1970_audit_migration.txt'
        direct = 'common/scripted_effects/COLDWAR_IRQ_1970_direct_rewards_v3.txt'
        installed = {path: read(ROOT / path) for path in (programmes, migration, direct)}
        cases = 0
        for key in ('national_front', 'baath_monopoly'):
            node = next(n for n in self.nodes if n['key'] == key)
            expected = parse(decisions_module.PROGRAMME_CONTRACT_GATES[node['id']])
            for emitted in (self.focuses[node['id']], self.deliveries[node['id']+'_delivery']):
                reward = first(emitted, 'completion_reward', first(emitted, 'complete_effect', []))
                conditional = [row for tooltip in values(reward, 'effect_tooltip')
                               for row in tooltip if row[0] == 'if'
                               and any(r[0] == 'add_to_variable' for r in row[2])]
                self.assertEqual(len(conditional), 0, key)
                label = P+'presentation_'+key+'_active_tt'
                self.assertIn(label, self.loc)
                self.assertIn(label,values(reward,'custom_effect_tooltip'))
                direct = [r for tooltip in values(reward, 'effect_tooltip')
                          for r in tooltip if r[0] == 'add_to_variable']
                self.assertEqual(len(direct),len(node['modifiers']))
            for state in ('none', 'signed', 'rights_missing', 'coalition_missing'):
                w = AuditWorld(installed); c = w.c['IRQ']
                c.flags[node['id']+'_package_earned'] = None
                c.flags[compiler.selection(node['id'])] = None
                if state != 'none':
                    c.flags[P+'front_accepted'] = None
                if state in ('signed', 'coalition_missing'):
                    c.flags[P+'legalization_accepted'] = None
                if state in ('signed', 'rights_missing'):
                    w.arrays['IRQ']['gov_coalition_array'] = {4}
                active = state == 'signed' if key == 'national_front' else state == 'none'
                self.assertEqual(w.tests(expected, c), active, (key, state))
                w.call_irq('reconcile_programmes')
                for modifier, value in node['modifiers'].items():
                    self.assertAlmostEqual(c.var[P+node['group']+'_'+modifier],
                                           value if active else 0, msg=(key, state, modifier))
                cases += 1
        CHECKS['conditional_contract_preview_consumer_cases'] = cases

    def test_all_14_spirit_previews_reference_real_current_stages(self):
        found = set()
        transitions = []
        for n in self.nodes:
            rewards = first(self.focuses[n['id']], 'completion_reward')
            for tooltip in values(rewards, 'effect_tooltip'):
                for key, operator, body in tooltip:
                    if key != 'if':
                        continue
                    swaps = values(body, 'swap_ideas')
                    removals = values(body, 'remove_ideas')
                    if not swaps and not removals:
                        continue
                    found.add(n['key'])
                    current = first(first(body, 'limit'), 'has_idea')
                    self.assertIn(current, self.ideas, n['id'])
                    self.assertEqual(len(swaps) + len(removals), 1, n['id'])
                    target = None
                    if swaps:
                        self.assertEqual(first(swaps[0], 'remove_idea'), current, n['id'])
                        target = first(swaps[0], 'add_idea')
                        self.assertIn(target, self.ideas, n['id'])
                        self.assertNotEqual(target, current, n['id'])
                    else:
                        self.assertEqual(removals[0], current, n['id'])
                    transitions.append({'focus': n['id'], 'current_idea': current,
                                        'target_idea': target})
        self.assertEqual(found, SPIRIT_NODES)
        self.assertEqual(len(found), 14)
        CHECKS['spirit_preview_focus_nodes'] = len(found)
        CHECKS['validated_current_stage_transitions'] = transitions

    def test_localization_is_bom_english_and_has_no_old_generic_or_list_text(self):
        self.assertEqual(LOC_FILE.read_bytes()[:3], b'\xef\xbb\xbf')
        text = read(LOC_FILE)
        self.assertTrue(text.startswith('l_english:'))
        self.assertNotIn('required government and office-holder; implemented prerequisite rewards.', text)
        self.assertIsNone(re.search(r'\[(?:\x27|\\?\")\w[^\n]*?(?:\x27|\\?\"),\s*(?:\x27|\\?\")%', text))
        for n in self.nodes:
            available = first(self.focuses[n['id']], 'available')
            for key, operator, value in walk(available):
                if key == 'tooltip':
                    self.assertIn(value, self.loc, (n['id'], value))
        arif = first(self.focuses[P + 'officer_council'], 'available')
        self.assertEqual(normalize(arif, self.leaders), normalize(parse(
            'COLDWAR_IRQ_campaign_active = yes check_variable = { ruling_party = 22 }'), self.leaders))
        self.assertIn('Republican Officers', self.loc[P + 'presentation_government_22'])
        CHECKS['english_bom_localization'] = True
        CHECKS['old_generic_or_list_repr_reward_text'] = False
        CHECKS['arif_node'] = {'focus': P + 'officer_council',
                               'title': self.loc[P + 'officer_council'],
                               'government': self.loc[P + 'presentation_government_22'],
                               'named_leader_requirement': False}

    def test_native_formatter_provider_references(self):
        modifiers = {key for n in self.nodes for key in n['modifiers']}
        keys = {compiler.presentation._modifier_tooltip(key) for key in modifiers}
        keys.add('modifies_dynamic_modifier_tt')
        providers = {key: [] for key in keys}
        for source, directory in (('game', GAME / 'localisation/english'),
                                  ('installed_md', MD / 'localisation/english'),
                                  ('workspace', ROOT / 'localisation/english')):
            for file in directory.rglob('*.yml'):
                for key, text, number in localization_lines(file):
                    if key in providers:
                        providers[key].append({'source': source, 'path': str(file),
                                               'line': number, 'text': text})
        for key, refs in providers.items():
            self.assertTrue(refs, key)
            # An English game or workspace provider must exist: the installed
            # reference mod alone would not prove the active load can resolve it.
            self.assertTrue(any(ref['source'] in ('game', 'workspace') for ref in refs), key)
            if key == 'modifies_dynamic_modifier_tt':
                self.assertTrue(any('$MODIFIER|Y$' in ref['text'] for ref in refs))
                continue
            for ref in refs:
                formats = re.findall(r'\$RIGHT\|([^$]+)\$', ref['text'])
                self.assertEqual(len(formats), 1, (key, ref))
                numeric_native={
                    'interest_rate_multiplier_modifier_tt':('-=2',),
                    'productivity_growth_modifier_tt':('+=2',),
                    P+'presentation_political_power_gain_tt':('+=2',),
                    'max_dig_in_tt':('+=1',),
                    'fossil_pp_fuel_consumption_modifier_tt':('-=%2',),
                }
                allowed=numeric_native.get(key,('+=%1', '+=%2', '-=%1', 'Y=%1'))
                self.assertIn(formats[0], allowed, (key, ref))
            if key not in (CUSTOM_SUPPORT_TT,P+'presentation_equipment_upgrade_xp_cost_tt',P+'presentation_political_power_gain_tt'):
                self.assertTrue(any(ref['source'] in ('game', 'installed_md') for ref in refs), key)
        CHECKS['modifier_types'] = len(modifiers)
        CHECKS['formatter_provider_keys'] = len(providers)
        CHECKS['formatter_providers'] = providers


def main():
    inputs = [FOCUS_FILE, QUEUE_FILE, REWARD_FILE, TRIGGER_FILE, IDEA_FILE,
              DYNAMIC_FILE, LOC_FILE, HERE / 'approved_iraq.json',
              HERE / 'presentation.py', HERE / 'manifest.json',
              HERE / 'flavour.py', HERE / 'flavour_politics.json', HERE / 'flavour_national.json']
    initial = {str(path.relative_to(ROOT)): sha(path) for path in inputs}
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PresentationTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    final = {str(path.relative_to(ROOT)): sha(path) for path in inputs}
    report = {
        'scope': 'Read-only installed focus, localization and source predicate regression checks',
        'limits': 'Does not establish actual HOI4 hover rendering, formatter-assert origin, live effects, save/reload or multiplayer behavior.',
        'success': result.wasSuccessful() and initial == final,
        'tests_run': result.testsRun,
        'failures': [{'test': str(test), 'details': details} for test, details in result.failures],
        'errors': [{'test': str(test), 'details': details} for test, details in result.errors],
        'inputs_unchanged_during_review': initial == final,
        'input_sha256': final,
        'checks': CHECKS,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
    print(f'Presentation report: {REPORT_PATH}')
    raise SystemExit(0 if report['success'] else 1)


if __name__ == '__main__':
    main()
