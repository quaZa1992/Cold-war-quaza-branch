# IMPERIA CW — Cold War: Check rural labour allocation, additive policies and native integration.
from pathlib import Path
import importlib.util
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('selector_art', ROOT / 'tools/selector_icons/build.py')
art = importlib.util.module_from_spec(spec)
spec.loader.exec_module(art)


def read(relative):
    return (ROOT / relative).read_text(encoding='utf-8-sig')


def block(relative, identifier):
    text = read(relative)
    return next(text[start:end] for name, start, end in art.entries(text) if name == identifier)


GREEN = block('common/ideas/mdcw_1970_era_national_ideas.txt', 'COLDWAR_era_green_revolution')
URBAN = block('common/ideas/COLDWAR_IMPERIA_directed_urbanisation.txt', 'COLDWAR_ni_directed_urbanisation')
MONEY = read('common/scripted_effects/00_money_system.txt')
CURVE = read('common/scripted_effects/mdcw_imperia_gdp_balance_effects.txt')


def modifier(text, name):
    match = re.search(r'\b' + re.escape(name) + r'\s*=\s*(-?[0-9.]+)\b', text)
    return float(match[1]) if match else 0.0


def subsistence(remaining_workforce, normal_share, *policies, other=0):
    # Country modifiers add before the native percentage is clamped to 0–90%.
    factor = 1 + other + sum(modifier(p, 'agriculture_workers_modifier') for p in policies)
    return remaining_workforce * min(0.9, max(0.0, normal_share * factor))


class RuralPolicyChecks(unittest.TestCase):
    def test_native_subsistence_consumer_releases_workforce_before_factories(self):
        start = MONEY.index('mdcw_imperia_agriculture_employment_fraction = yes')
        allocate = MONEY.index('multiply = agriculture_workers_percentage', start)
        release = MONEY.index('subtract_from_temp_variable = { workforce_total = agriculture_workers }', allocate)
        factories = MONEY.index('# Factories & Offices Employment', release)
        self.assertLess(start, allocate)
        self.assertLess(allocate, release)
        self.assertLess(release, factories)
        self.assertIn('modifier@agriculture_workers_modifier', CURVE)
        self.assertIn('agriculture_workers_perc_modifier = 1', CURVE)

    def test_rural_workers_can_fill_industrial_vacancies(self):
        # Six million workers, 60% normal subsistence allocation and ample vacancies.
        normal = subsistence(6_000_000, 0.6)
        green = subsistence(6_000_000, 0.6, GREEN)
        urban = subsistence(6_000_000, 0.6, URBAN)
        self.assertAlmostEqual(normal - green, 540_000)
        self.assertAlmostEqual(normal - urban, 1_080_000)
        self.assertGreater(6_000_000 - green, 6_000_000 - normal)
        self.assertGreater(6_000_000 - urban, 6_000_000 - green)

    def test_stacking_is_additive_and_does_not_duplicate_workers(self):
        combined = subsistence(6_000_000, 0.6, GREEN, URBAN)
        self.assertAlmostEqual(combined, 1_980_000)
        self.assertAlmostEqual(3_600_000 - combined, 1_620_000)
        # Existing +10% requirement stacks with the policies in the same sum.
        self.assertAlmostEqual(subsistence(6_000_000, 0.6, GREEN, URBAN, other=0.1), 2_340_000)

    def test_native_bounds_cover_extreme_existing_modifiers(self):
        self.assertEqual(subsistence(6_000_000, 0.6, GREEN, URBAN, other=-1), 0)
        self.assertEqual(subsistence(6_000_000, 0.9, GREEN, URBAN, other=4), 5_400_000)
        self.assertIn('agriculture_workers_percentage min = 0.0 max = 0.9', CURVE)

    def test_district_requirement_uses_the_other_native_modifier(self):
        value = modifier(GREEN, 'agriculture_district_worker_requirement_modifier')
        self.assertAlmostEqual(188_000 * (1 + value), 159_800)
        self.assertEqual(modifier(URBAN, 'agriculture_district_worker_requirement_modifier'), 0)
        self.assertIn('add = modifier@agriculture_district_worker_requirement_modifier', MONEY)
        self.assertIn('workers_per_agriculture_district = 0.188', MONEY)

    def test_tradeoff_is_real_in_the_agricultural_gdp_formula(self):
        self.assertIn('add = modifier@agricolture_productivity_modifier', MONEY)
        self.assertLess(modifier(URBAN, 'agricolture_productivity_modifier'), 0)
        self.assertGreater(modifier(URBAN, 'production_speed_industrial_complex_factor'), 0)
        self.assertLess(modifier(URBAN, 'stability_factor'), 0)
        self.assertGreater(modifier(URBAN, 'social_cost_multiplier_modifier'), 0)
        self.assertGreater(modifier(URBAN, 'bureaucracy_cost_multiplier_modifier'), 0)
        self.assertGreater(modifier(URBAN, 'health_cost_multiplier_modifier'), 0)
        self.assertGreater(modifier(URBAN, 'consumer_goods_factor'), 0)

    def test_no_population_creation_or_new_periodic_jobs(self):
        for text in (GREEN, URBAN):
            self.assertNotRegex(text, r'\b(add_manpower|add_state_population|country_event|every_country|every_state|daily|monthly)\s*=')
            self.assertEqual(text.count('ingame_update_setup = yes'), 2)

    def test_success_does_not_remove_urbanisation_and_its_costs(self):
        self.assertIn('check_variable = { agriculture_workers > 0 }', URBAN)
        self.assertIn('days = 1440', URBAN)
        self.assertIn('NOT = { has_country_flag = COLDWAR_directed_urbanisation_commitment }', URBAN)
        self.assertIn('cancel_if_invalid = no', URBAN)

    def test_custom_modifiers_are_defined_and_consumed(self):
        definitions = read('common/modifier_definitions/money_modifier_definitions.txt')
        for name in ['agriculture_workers_modifier', 'agriculture_district_worker_requirement_modifier',
                     'agricolture_productivity_modifier', 'social_cost_multiplier_modifier',
                     'bureaucracy_cost_multiplier_modifier', 'health_cost_multiplier_modifier']:
            self.assertRegex(definitions, r'(?m)^' + name + r'\s*=')
            self.assertIn('modifier@' + name, MONEY + CURVE)

    def test_english_localisation_and_native_green_asset(self):
        from PIL import Image
        loc_path = ROOT / 'localisation/english/COLDWAR_IMPERIA_directed_urbanisation_l_english.yml'
        self.assertTrue(loc_path.read_bytes().startswith(b'\xef\xbb\xbf'))
        self.assertIn('45%', loc_path.read_text(encoding='utf-8-sig'))
        self.assertIn('Has workers employed in subsistence agriculture', loc_path.read_text(encoding='utf-8-sig'))
        manifest = json.loads(read('tools/selector_icons/manifest.json'))
        entry = next(a for a in manifest['assets'] if a['id'] == 'COLDWAR_ni_directed_urbanisation')
        self.assertEqual(entry['category'], 2)
        self.assertIn('forest green', entry['color'])
        texture = ROOT / 'gfx/interface/ideas/COLDWAR_selector/COLDWAR_ni_directed_urbanisation.dds'
        self.assertEqual(texture.stat().st_size, 16512)
        with Image.open(texture) as image:
            self.assertEqual(image.size, (64, 64))
            self.assertEqual(image.convert('RGBA').getpixel((0, 0))[3], 0)
        gfx = read('interface/COLDWAR_IMPERIA_selector_icons.gfx')
        self.assertEqual(gfx.count('name = "GFX_idea_' + entry['picture'] + '"'), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
