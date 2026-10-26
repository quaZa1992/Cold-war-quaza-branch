# IMPERIA COLD WAR: Check agency creation eligibility, native button coverage and scripted reward bypasses.
from pathlib import Path
import importlib.util
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('clausewitz_ast', ROOT / 'tools/spain_1970_v2/script_ast.py')
AST = importlib.util.module_from_spec(spec)
spec.loader.exec_module(AST)
TRIGGER = 'COLDWAR_can_create_intelligence_agency'
SSR = 'autonomy_soviet_republic_1985'


def read(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')


def parse(path):
    return AST.parse(read(path))


def first(rows, key):
    return AST.first(rows, key)


ELIGIBILITY = first(parse('common/scripted_triggers/COLDWAR_SSR_intelligence.txt'), TRIGGER)


def eligible(rows, autonomy='autonomy_free', agency=False, ai=False, dlc=True):
    results = []
    for key, _, value in rows:
        if key == 'NOT':
            result = not eligible(value, autonomy, agency, ai, dlc)
        elif key == 'OR':
            result = any(eligible([row], autonomy, agency, ai, dlc) for row in value)
        elif key == 'has_autonomy_state':
            result = autonomy == value
        elif key == 'has_intelligence_agency':
            result = agency == (value == 'yes')
        elif key == 'is_ai':
            result = ai == (value == 'yes')
        elif key == 'has_dlc':
            assert value == '"La Resistance"'
            result = dlc
        elif key == TRIGGER:
            result = eligible(ELIGIBILITY, autonomy, agency, ai, dlc) == (value == 'yes')
        else:
            raise AssertionError('Unsupported condition: ' + key)
        results.append(result)
    return all(results)


class SSRIntelligenceChecks(unittest.TestCase):
    def test_all_fourteen_subject_republics_are_blocked_and_independence_restores_eligibility(self):
        autonomy = first(parse('common/autonomous_states/99_1985_soviet_republic_autonomies.txt'), 'autonomy_state')
        self.assertEqual(first(autonomy, 'id'), SSR)
        tags = [v for k, _, v in first(first(autonomy, 'allowed'), 'OR') if k == 'original_tag']
        self.assertEqual(set(tags), {'UKR', 'BLR', 'EST', 'LAT', 'LIT', 'ARM', 'AZE', 'GEO', 'KAZ', 'KYR', 'TAJ', 'TRK', 'UZB', 'MLV'})
        for tag in tags:
            with self.subTest(tag=tag):
                self.assertFalse(eligible(ELIGIBILITY, autonomy=SSR))
                self.assertTrue(eligible(ELIGIBILITY, autonomy='autonomy_free'))
        self.assertTrue(eligible(ELIGIBILITY, autonomy='autonomy_puppet'))

    def test_player_blocker_covers_only_ssr_creation_and_has_no_stale_dirty_cache(self):
        gui = first(first(parse('common/scripted_guis/COLDWAR_SSR_intelligence.txt'), 'scripted_gui'), 'COLDWAR_SSR_agency_creation_blocker')
        visible = first(gui, 'visible')
        self.assertTrue(eligible(visible, autonomy=SSR))
        for kwargs in [{'autonomy': 'autonomy_free'}, {'autonomy': SSR, 'ai': True},
                       {'autonomy': SSR, 'dlc': False}, {'autonomy': SSR, 'agency': True}]:
            self.assertFalse(eligible(visible, **kwargs))
        button = first(first(gui, 'triggers'), 'COLDWAR_SSR_agency_locked_button_click_enabled')
        self.assertFalse(eligible(button, autonomy=SSR))
        self.assertNotIn('dirty', [k for k, _, _ in gui])
        self.assertEqual(first(gui, 'parent_window_name'), '"countryintelligenceagencyview"')

    def test_both_input_layers_exactly_cover_the_current_md_creation_button(self):
        native = first(first(parse('interface/countryintelligenceagencyview.gui'), 'guiTypes'), 'containerWindowType')
        panel = next(row for row in AST.values(native, 'containerWindowType') if first(row, 'name') == '"before_creation_panel"')
        button = next(row for row in AST.values(panel, 'buttonType') if first(row, 'name') == '"creation_button"')
        self.assertIsNone(first(button, 'shortcut'))
        position = {axis: int(first(first(panel, 'position'), axis)) + int(first(first(button, 'position'), axis)) for axis in ['x', 'y']}
        overlay = first(first(parse('interface/COLDWAR_SSR_intelligence.gui'), 'guiTypes'), 'containerWindowType')
        layers = AST.values(overlay, 'buttonType')
        self.assertEqual(len(layers), 2)
        for layer in layers:
            self.assertEqual({axis: int(first(first(layer, 'position'), axis)) for axis in ['x', 'y']}, position)
            self.assertEqual(first(layer, 'quadTextureSprite'), first(button, 'quadTextureSprite'))
            self.assertEqual(first(layer, 'Orientation'), first(button, 'Orientation'))
            self.assertIn('COLDWAR_SSR_agency_blocked_tt:', read('localisation/english/COLDWAR_SSR_intelligence_l_english.yml'))
        self.assertEqual(first(layers[0], 'name'), '"COLDWAR_SSR_agency_input_sink"')
        self.assertEqual(first(layers[1], 'name'), '"COLDWAR_SSR_agency_locked_button"')

    def test_ai_factory_budget_restriction_ends_on_independence(self):
        plan = first(parse('common/ai_strategy/COLDWAR_SSR_intelligence.txt'), 'COLDWAR_SSR_no_independent_agency')
        self.assertTrue(eligible(first(plan, 'enable'), autonomy=SSR, ai=True))
        self.assertFalse(eligible(first(plan, 'enable'), autonomy='autonomy_free', ai=True))
        self.assertEqual(first(plan, 'abort_when_not_enabled'), 'yes')
        strategy = first(plan, 'ai_strategy')
        self.assertEqual(first(strategy, 'type'), 'intelligence_agency_usable_factories')
        self.assertLessEqual(int(first(strategy, 'value')), -999)

    def test_faction_reward_does_not_create_a_republican_agency(self):
        goal = first(parse('common/factions/goals/faction_goals_short_term.txt'), 'faction_goal_spy_master')
        creation = next(row for row in AST.values(first(goal, 'complete_effect'), 'every_faction_member')
                        if first(row, 'create_intelligence_agency') == 'yes')
        self.assertFalse(eligible(first(creation, 'limit'), autonomy=SSR))
        self.assertTrue(eligible(first(creation, 'limit'), autonomy='autonomy_free'))

    def test_generic_reward_guard_preserves_all_original_rewards_for_eligible_countries(self):
        path = 'common/scripted_effects/00_lar_effects.txt'
        current = parse(path)
        baseline = json.loads((Path(__file__).parent / 'baseline.json').read_text(encoding='utf-8'))
        def fingerprint(value):
            return hashlib.sha256(json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode('utf-8')).hexdigest()
        wrapper = first(first(current, 'gain_random_agency_upgrade'), 'if')
        guard = first(wrapper, 'limit')
        self.assertFalse(eligible(guard, autonomy=SSR))
        self.assertTrue(eligible(guard, autonomy='autonomy_free'))
        self.assertTrue(eligible(guard, autonomy=SSR, agency=True))
        unwrapped = [row for row in wrapper if row[0] != 'limit']
        self.assertEqual(fingerprint(unwrapped), baseline['random_reward_tokens_sha256'])
        self.assertEqual(fingerprint([r for r in current if r[0] != 'gain_random_agency_upgrade']),
                         baseline['other_effects_tokens_sha256'])

    def test_no_1970_republic_history_grants_an_agency(self):
        tags = ['UKR', 'BLR', 'EST', 'LAT', 'LIT', 'ARM', 'AZE', 'GEO', 'KAZ', 'KYR', 'TAJ', 'TRK', 'UZB', 'MLV']
        def walk(rows, date=0):
            for key, _, value in rows:
                current_date = int(key.split('.')[0]) if key[:4].isdigit() and '.' in key else date
                if key == 'create_intelligence_agency':
                    self.assertGreater(current_date, 1970)
                if isinstance(value, list):
                    walk(value, current_date)
        for tag in tags:
            paths = list((ROOT / 'history/countries').glob(tag + ' - *.txt'))
            self.assertEqual(len(paths), 1)
            walk(AST.parse(paths[0].read_text(encoding='utf-8-sig')))

    def test_new_files_have_required_encoding_markers_and_no_recurring_hooks(self):
        paths = ['common/scripted_triggers/COLDWAR_SSR_intelligence.txt',
                 'common/scripted_guis/COLDWAR_SSR_intelligence.txt',
                 'common/ai_strategy/COLDWAR_SSR_intelligence.txt',
                 'interface/COLDWAR_SSR_intelligence.gui',
                 'localisation/english/COLDWAR_SSR_intelligence_l_english.yml']
        for path in paths:
            blob = (ROOT / path).read_bytes()
            self.assertEqual(blob.startswith(b'\xef\xbb\xbf'), path.endswith('.yml'))
            text = blob.decode('utf-8-sig')
            self.assertIn('IMPERIA COLD WAR', text)
            for command in ['on_daily', 'on_weekly', 'on_monthly', 'every_country', 'every_state']:
                self.assertNotIn(command + ' =', text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
