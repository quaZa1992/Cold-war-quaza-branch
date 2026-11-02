# IMPERIA COLD WAR — Independent emitted naval lifecycle source models.
"""Read actual runtime files. Never generate or mutate gameplay outputs.

The bounded model executes receipt, quote, money, building and idea transactions.
Research/mastery and existing internal-faction helpers are recorded as native
calls; their engine calculations and final faction-opinion clamps are outside
this model. Synthetic construction fixtures do not prove a real 1970 OOB/map.
"""
from __future__ import annotations

import copy
from decimal import Decimal
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from test_assets import Model as AssetModel, ROOT, parse, first, walk

EFFECTS_PATH = ROOT / 'common/scripted_effects/COLDWAR_NAVY_1970.txt'
TRIGGERS_PATH = ROOT / 'common/scripted_triggers/COLDWAR_NAVY_1970.txt'
FX = dict((k, v) for k, _, v in parse(EFFECTS_PATH.read_text(encoding='utf-8')))
TRIGGERS = dict((k, v) for k, _, v in parse(TRIGGERS_PATH.read_text(encoding='utf-8')))
MANIFEST = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))
RECORDS = {n['id']: n for items in MANIFEST['countries'].values() for n in items}
PROFILES = {p.stem: json.loads(p.read_text(encoding='utf-8')) for p in (HERE / 'profiles').glob('*.json')}
PAID = ('naval_bases', 'dockyards', 'large_ship_drydocks')
IDEA_MAP = {
    'combined_defense_industries_idea': 'combined_military_defense_industries',
    'equipment_conversion_efforts_idea': 'weapon_conversion_packages',
    'convoy_production_bonus': 'convoy_and_freighter_production',
    'repair_yard_focus': 'improved_repair_facilities',
    'naval_production_bonus4': 'vessel_production',
    'establishing_a_marine_corps_idea': 'establish_a_marine_corps',
}


class RuntimeModel(AssetModel):
    def __init__(self, tag):
        super().__init__()
        self.profile = PROFILES[tag]
        self.country['tag'] = tag
        self.country['vars'].update(treasury=Decimal(1000), gdp_total=Decimal(100))
        self.country.update(completed=set(), ideas={}, grants=[])
        self.scenario = self.exists = self.naval_doctrine = self.major = self.regional = True
        self.factories = self.yards = 30
        self.doctrines = {'escort_attack_subs'}
        self.day = 0
        targets = {int(r['state']) for key in ('port_targets', 'yard_targets') for r in self.profile[key]}
        self.states = {str(s): dict(state=s, owner=tag, controller=tag, coast=True, free=8,
            levels={'dockyard': 1, 'arms_factory': 1},
            ports={int(p['province']): 1 for p in self.profile['port_targets'] if int(p['state']) == s}) for s in targets}
        self.country['provinces'] = {int(p['province']) for p in self.profile['port_targets']}
        self.root = self.country

    def conditions(self, rows, scope):
        for key, op, value in rows:
            if key in TRIGGERS:ok = self.conditions(TRIGGERS[key], scope) == (value == 'yes')
            elif key == 'hidden_trigger':ok = self.conditions(value, scope)
            elif key == 'custom_trigger_tooltip':ok = self.conditions([r for r in value if r[0] != 'tooltip'], scope)
            elif key == 'exists':ok = self.exists == (value == 'yes')
            elif key == 'IMP_is_1970_scenario':ok = self.scenario == (value == 'yes')
            elif key == 'has_completed_focus':ok = value in scope['completed']
            elif key == 'num_of_factories':ok = self.compare(Decimal(self.factories), op, Decimal(value))
            elif key == 'num_of_naval_factories':ok = self.compare(Decimal(self.yards), op, Decimal(value))
            elif key == 'has_selected_naval_grand_doctrine':ok = self.naval_doctrine == (value == 'yes')
            elif key == 'has_at_least_major_power_status':ok = self.major == (value == 'yes')
            elif key == 'has_at_least_regional_power_status':ok = self.regional == (value == 'yes')
            elif key == 'has_doctrine':ok = value in self.doctrines
            else:ok = super().conditions([(key, op, value)], scope)
            if not ok:return False
        return True

    def execute(self, rows, scope):
        branch = False
        for key, op, value in rows:
            if key == 'if':
                branch = self.conditions(first(value, 'limit', []), scope)
                if branch:self.execute([r for r in value if r[0] != 'limit'], scope)
            elif key == 'else_if':
                if not branch and self.conditions(first(value, 'limit', []), scope):
                    self.execute([r for r in value if r[0] != 'limit'], scope);branch = True
            elif key == 'else':
                if not branch:self.execute(value, scope)
                branch = True
            elif key == 'effect_tooltip':pass
            elif key in FX:self.execute(FX[key], scope)
            elif key == 'set_variable':
                name, _, amount = value[0];scope['vars'][name] = self.num(amount, scope)
            elif key == 'multiply_variable':
                name, _, amount = value[0];scope['vars'][name] *= self.num(amount, scope)
            elif key == 'set_country_flag':
                assert isinstance(value, str), ('Unmodeled structured flag', value)
                scope['flags'].add(value)
            elif key == 'clr_country_flag':scope['flags'].discard(value)
            elif key == 'add_ideas':scope['ideas'][value] = None
            elif key == 'add_timed_idea':scope['ideas'][first(value, 'idea')] = self.day + int(first(value, 'days'))
            elif key in ('navy_experience', 'add_mastery', 'add_tech_bonus', 'change_defense_industry_opinion', 'change_maritime_industry_opinion', 'newline'):
                scope['grants'].append((key, copy.deepcopy(value)))
            else:super().execute([(key, op, value)], scope)

    def call(self, name):self.execute(FX[name], self.country)
    def snap(self):return copy.deepcopy((self.country, self.states, self.trace))
    def seed(self, record):
        for group in record['prerequisites']:
            parent = group[0];self.country['completed'].add(parent)
            if parent in RECORDS:self.seed(RECORDS[parent])
    def retry(self):self.call('COLDWAR_NAVY_' + self.profile['country'] + '_retry_pending')
    def price(self, key):
        coastal = self.profile['variant'] == 'coastal';gdp = self.country['vars']['gdp_total']
        if key == 'naval_bases':return gdp * Decimal('.002') if coastal else Decimal('.5')
        return gdp * Decimal('.008') if coastal else Decimal('15' if key == 'dockyards' else '7.5')


class NavalLifecycleTests(unittest.TestCase):
    def test_all_85_previews_do_not_execute_and_rewards_deliver_once(self):
        self.assertEqual(len(RECORDS), 85)
        for record in RECORDS.values():
            with self.subTest(focus=record['id']):
                m = RuntimeModel(record['country']);m.seed(record);before = m.snap()
                m.call(record['completion'].replace('_complete_', '_preview_'));self.assertEqual(before, m.snap())
                m.call(record['completion']);self.assertIn(record['done'], m.country['flags']);self.assertNotIn(record['pending'], m.country['flags'])
                delivered = m.snap();m.call(record['completion']);self.assertEqual(delivered, m.snap())

    def test_all_12_funded_projects_retry_after_funds_return_only_once(self):
        funded = [r for r in RECORDS.values() if r['key'] in PAID and not PROFILES[r['country']].get('allow_deficit')]
        self.assertEqual(len(funded), 12)
        for record in funded:
            with self.subTest(focus=record['id']):
                m = RuntimeModel(record['country']);m.seed(record);m.country['vars']['treasury'] = Decimal(0)
                m.call(record['completion']);self.assertIn(record['pending'], m.country['flags']);self.assertNotIn(record['done'], m.country['flags'])
                self.assertFalse(m.trace);self.assertFalse(m.country['grants']);self.assertFalse(m.country['ideas'])
                m.country['vars']['treasury'] = Decimal(1000);price = m.price(record['key']);m.retry()
                self.assertIn(record['done'], m.country['flags']);self.assertEqual(m.country['vars']['treasury'], Decimal(1000) - price)
                delivered = m.snap();m.retry();self.assertEqual(delivered, m.snap())

    def test_all_three_uae_paid_projects_charge_once_from_negative_treasury(self):
        self.assertIs(PROFILES['UAE'].get('allow_deficit'), True)
        for key in PAID:
            with self.subTest(key=key):
                record = RECORDS['COLDWAR_NAVY_UAE_' + key];m = RuntimeModel('UAE');m.seed(record)
                m.country['vars']['treasury'] = Decimal(-2);price = m.price(key)
                m.call(record['completion']);self.assertIn(record['done'], m.country['flags']);self.assertNotIn(record['pending'], m.country['flags'])
                self.assertEqual(m.country['vars']['treasury'], Decimal(-2) - price)
                self.assertEqual([t for t in m.trace if t[0] == 'fee'], [('fee', -price)])
                delivered = m.snap();m.call(record['completion']);m.retry();self.assertEqual(delivered, m.snap())

    def test_all_20_asset_projects_wait_for_complete_capacity(self):
        for record in (r for r in RECORDS.values() if r['asset']):
            with self.subTest(focus=record['id']):
                m = RuntimeModel(record['country']);m.seed(record)
                kind = 'naval_base' if record['key'] == 'naval_bases' else 'arms_factory' if record['key'] == 'combined_military_defense_industries' else 'dockyard'
                for state in m.states.values():
                    if kind == 'naval_base':state['ports'] = {p: 10 for p in state['ports']}
                    else:state['levels'][kind] = int(first(first(m.definitions[kind], 'level_cap'), 'state_max'))
                m.call(record['completion']);self.assertIn(record['pending'], m.country['flags']);self.assertNotIn(record['done'], m.country['flags'])
                self.assertFalse(m.trace);self.assertFalse(m.country['grants']);self.assertFalse(m.country['ideas'])
                for state in m.states.values():
                    if kind == 'naval_base':state['ports'] = {p: 1 for p in state['ports']}
                    else:state['levels'][kind] = 1
                m.retry();self.assertIn(record['done'], m.country['flags']);delivered = m.snap();m.retry();self.assertEqual(delivered, m.snap())

    def test_carrier_and_helicopter_competitor_is_rechecked_on_execution(self):
        for record in (r for r in RECORDS.values() if r['exclusions']):
            with self.subTest(focus=record['id']):
                m = RuntimeModel(record['country']);m.seed(record);m.country['completed'].update(record['exclusions'])
                m.call(record['completion']);self.assertNotIn(record['done'], m.country['flags']);self.assertFalse(m.country['grants']);self.assertFalse(m.trace)
                m.retry();self.assertNotIn(record['done'], m.country['flags'])

    def test_each_required_parent_group_is_rechecked_for_all_85(self):
        for record in RECORDS.values():
            for missing in record['prerequisites']:
                with self.subTest(focus=record['id'], parent=missing):
                    m = RuntimeModel(record['country']);m.seed(record);m.country['completed'].difference_update(missing)
                    m.call(record['completion']);self.assertNotIn(record['done'], m.country['flags']);self.assertFalse(m.country['grants']);self.assertFalse(m.trace)
                    m.country['completed'].add(missing[0]);m.retry();self.assertIn(record['done'], m.country['flags'])

    def test_all_five_tags_reject_foreign_scope_or_later_scenario(self):
        for tag in PROFILES:
            record = RECORDS['COLDWAR_NAVY_' + tag + '_naval_reform']
            for wrong in ('country', 'scenario', 'exists'):
                with self.subTest(country=tag, wrong=wrong):
                    m = RuntimeModel(tag);m.seed(record)
                    if wrong == 'country':m.country['tag'] = 'ZZZ'
                    elif wrong == 'scenario':m.scenario = False
                    else:m.exists = False
                    before = m.snap();m.call(record['completion'])
                    if wrong == 'exists':
                        # A retained country scope may retain its pending
                        # receipt. Existence is required before material reward.
                        self.assertNotIn(record['done'], m.country['flags'])
                        self.assertEqual(before[0]['vars'], m.country['vars'])
                        self.assertFalse(m.country['grants']);self.assertFalse(m.country['ideas']);self.assertFalse(m.trace)
                    else:self.assertEqual(before, m.snap())

    def test_quotes_refresh_before_debit_with_changed_gdp(self):
        for tag in PROFILES:
            for key in PAID:
                with self.subTest(country=tag, key=key):
                    record = RECORDS['COLDWAR_NAVY_' + tag + '_' + key];m = RuntimeModel(tag);m.seed(record)
                    m.call('COLDWAR_NAVY_' + tag + '_quote_prices');m.country['vars']['gdp_total'] = Decimal(250)
                    for suffix in ('port', 'yard', 'yard_2'):m.country['vars']['COLDWAR_NAVY_' + tag + '_' + suffix + '_quote'] = Decimal('.00001')
                    price = m.price(key);m.call(record['completion'])
                    self.assertIn(record['done'], m.country['flags']);self.assertEqual(m.country['vars']['treasury'], Decimal(1000) - price)

    def test_coastal_zero_gdp_and_md_skip_never_give_unpaid_assets(self):
        for record in (r for r in RECORDS.values() if r['asset']):
            for blocked in ('skip', 'gdp'):
                if blocked == 'gdp' and (PROFILES[record['country']]['variant'] != 'coastal' or record['key'] not in PAID):continue
                with self.subTest(focus=record['id'], blocked=blocked):
                    m = RuntimeModel(record['country']);m.seed(record)
                    if blocked == 'skip':m.country['flags'].add('MD_skip_treasury_cost')
                    else:m.country['vars']['gdp_total'] = Decimal(0)
                    m.call(record['completion']);self.assertNotIn(record['done'], m.country['flags']);self.assertFalse(m.trace);self.assertFalse(m.country['ideas'])

    def test_lost_control_and_port_province_between_hover_and_delivery(self):
        for tag in PROFILES:
            for lost in ('state', 'province'):
                with self.subTest(country=tag, lost=lost):
                    record = RECORDS['COLDWAR_NAVY_' + tag + '_naval_bases'];m = RuntimeModel(tag);m.seed(record)
                    m.call('COLDWAR_NAVY_' + tag + '_quote_prices');self.assertTrue(m.conditions(TRIGGERS[record['ready']], m.country))
                    if lost == 'state':
                        for state in m.states.values():state['controller'] = 'ZZZ'
                    else:m.country['provinces'].clear()
                    m.call(record['completion']);self.assertNotIn(record['done'], m.country['flags']);self.assertFalse(m.trace)
                    for state in m.states.values():state['controller'] = tag
                    m.country['provinces'] = {int(p['province']) for p in m.profile['port_targets']}
                    m.retry();self.assertIn(record['done'], m.country['flags'])

    def test_timed_ideas_do_not_refresh_after_the_once_only_focus_expires(self):
        for tag in PROFILES:
            for key, duration in [('weapon_conversion_packages', 730), ('improved_repair_facilities', 365), ('vessel_production', 730)]:
                with self.subTest(country=tag, key=key):
                    record = RECORDS['COLDWAR_NAVY_' + tag + '_' + key];m = RuntimeModel(tag);m.seed(record);m.call(record['completion'])
                    idea = 'COLDWAR_NAVY_' + tag + '_idea_' + key;self.assertEqual(m.country['ideas'][idea], duration)
                    m.day = duration + 1;m.country['ideas'].pop(idea);m.call(record['completion']);m.retry();self.assertNotIn(idea, m.country['ideas'])

    def test_all_30_cloned_idea_payloads_match_the_real_donor(self):
        donor = first(first(parse((ROOT / 'common/ideas/generic_ideas.txt').read_text()), 'ideas'), 'country')
        emitted = first(first(parse((ROOT / 'common/ideas/COLDWAR_NAVY_1970.txt').read_text()), 'ideas'), 'country')
        self.assertEqual(len(emitted), 30)
        for tag in PROFILES:
            for original, key in IDEA_MAP.items():
                with self.subTest(country=tag, idea=original):
                    expected = [r for r in first(donor, original) if r[0] != 'name']
                    actual = [r for r in first(emitted, 'COLDWAR_NAVY_' + tag + '_idea_' + key) if r[0] != 'name']
                    self.assertEqual(expected, actual)

    def test_emitted_new_focus_prerequisites_and_categories_resolve(self):
        categories = (ROOT / 'common/technology_tags/00_technology.txt').read_text()
        for tag, profile in PROFILES.items():
            tree = first(parse((ROOT / profile['tree_file']).read_text()), 'focus_tree')
            focuses = {first(n, 'id'): n for k, _, n in tree if k == 'focus'}
            expected = 15 if profile['variant'] == 'coastal' else 20
            self.assertEqual(len([f for f in focuses if f.startswith('COLDWAR_NAVY_' + tag + '_')]), expected)
            for record in MANIFEST['countries'][tag]:
                actual = [firsts for k, _, p in focuses[record['id']] if k == 'prerequisite' for firsts in [[v for f, _, v in p if f == 'focus']]]
                self.assertEqual(actual, record['prerequisites'])
                self.assertTrue(all(p in focuses for group in actual for p in group))
        for body in FX.values():
            for key, _, value in walk(body):
                if key == 'add_tech_bonus':
                    for field, _, category in value:
                        if field == 'category':self.assertIn(category, categories)
        self.assertNotIn('sp:', EFFECTS_PATH.read_text());self.assertNotIn('sp:', TRIGGERS_PATH.read_text())

    def test_public_requirements_preserve_runtime_price_and_skip_guards(self):
        for tag, profile in PROFILES.items():
            tree = first(parse((ROOT / profile['tree_file']).read_text()), 'focus_tree')
            focuses = {first(n, 'id'): n for k, _, n in tree if k == 'focus'}
            for record in (r for r in MANIFEST['countries'][tag] if r['asset']):
                with self.subTest(focus=record['id']):
                    availability = first(focuses[record['id']], 'available')
                    self.assertFalse(any(k == 'check_variable' for k, _, v in availability))
                    m = RuntimeModel(tag);m.seed(record);m.call('COLDWAR_NAVY_' + tag + '_quote_prices')
                    for blocked in ('none', 'money', 'skip', 'gdp', 'province'):
                        baseline = copy.deepcopy(m.country)
                        if blocked == 'money':m.country['vars']['treasury'] = Decimal(0)
                        elif blocked == 'skip':m.country['flags'].add('MD_skip_treasury_cost')
                        elif blocked == 'gdp':m.country['vars']['gdp_total'] = Decimal(0);m.call('COLDWAR_NAVY_' + tag + '_quote_prices')
                        elif blocked == 'province':m.country['provinces'].clear()
                        self.assertEqual(m.conditions(availability, m.country), m.conditions(TRIGGERS[record['ready']], m.country), blocked)
                        m.country.clear();m.country.update(baseline)


if __name__ == '__main__':
    unittest.main(verbosity=2)
