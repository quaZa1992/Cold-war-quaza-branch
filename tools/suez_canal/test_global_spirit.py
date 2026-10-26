# IMPERIA CW — Cold War: suez canal — test global spirit.
"""Execute the Suez burden's authored script subset against small country fixtures.

These bounded source checks cover calculation, classification, and modifier
reconciliation. HOI4 remains responsible for routing convoys and rendering UI.
"""
from dataclasses import dataclass, field
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    'suez_script_ast', ROOT / 'tools/vietnam_1970/script_ast.py')
PARSER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PARSER)
parse, first, walk = PARSER.parse, PARSER.first, PARSER.walk


def source(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')


def definitions(path):
    return {key: value for key, op, value in parse(source(path))}


EFFECTS = definitions('common/scripted_effects/mdcw_suez_global_effects.txt')
EXPOSURE = definitions('common/scripted_triggers/mdcw_suez_exposure_triggers.txt')
TRIGGERS = dict(EXPOSURE)
for filename in ('00_continent_triggers.txt', 'MD_Country_Groups_Triggers.txt'):
    TRIGGERS.update(definitions('common/scripted_triggers/' + filename))
DYNAMIC = definitions('common/dynamic_modifiers/mdcw_suez_dynamic_modifiers.txt')[
    'mdcw_suez_canal_closure']
MONEY_ENTRY = definitions('common/scripted_effects/00_money_system.txt')['ingame_update_setup']
SPIRIT = 'mdcw_suez_canal_closure'
FLAG = 'SUEZ_CANAL_BLOCKED'
EXPECTED = {
    'production_speed_buildings_factor': ('mdcw_suez_construction', -.20),
    'investment_cost_modifier': ('mdcw_suez_investment_cost', .20),
    'civilian_factories_productivity': ('mdcw_suez_civilian_productivity', -.12),
    'industrial_capacity_factory': ('mdcw_suez_factory_output', -.08),
    'industrial_capacity_dockyard': ('mdcw_suez_dockyard_output', -.08),
    'resource_export_multiplier_modifier': ('mdcw_suez_export_revenue', -.24),
}


@dataclass
class State:
    coastal: bool = True
    core: bool = True
    controlled: bool = True
    continent: str = 'africa'


@dataclass
class Country:
    tag: str
    variables: dict = field(default_factory=lambda: {'globalism_value': 75.0})
    equilibrium: float = 50.0
    continent: str = 'africa'
    states: list = field(default_factory=lambda: [State()])
    dynamic: set = field(default_factory=set)
    additions: int = 0
    removals: int = 0
    refreshes: int = 0
    fiscal_refreshes: int = 0
    fiscal_snapshot: dict = field(default_factory=dict)


class Model:
    """Fail on unsupported script, rather than silently ignoring new behavior."""
    def __init__(self, *countries, closed=True):
        self.countries = list(countries)
        self.flags = {FLAG} if closed else set()
        self.native_depth = 0
        self.effect_depth = 0
        self.temp = {}

    def test(self, rows, country, state=None):
        return all(self.condition(k, v, country, state) for k, op, v in rows)

    def condition(self, key, arg, country, state=None):
        if key == 'AND':
            return self.test(arg, country, state)
        if key == 'OR':
            return any(self.condition(k, v, country, state) for k, op, v in arg)
        if key == 'NOT':
            return not self.test(arg, country, state)
        if key in TRIGGERS:
            result = self.test(TRIGGERS[key], country, state)
            return result if arg == 'yes' else not result
        if key == 'original_tag':
            return country.tag == arg
        if key == 'has_variable':
            return arg in country.variables
        if key == 'has_global_flag':
            return arg in self.flags
        if key == 'has_dynamic_modifier':
            return first(arg, 'modifier') in country.dynamic
        if key == 'check_variable':
            for variable, op, token in arg:
                left, right = self.number(variable, country), self.number(token, country)
                comparisons = {'=': left == right, '!=': left != right,
                               '>': left > right, '<': left < right,
                               '>=': left >= right, '<=': left <= right}
                if op not in comparisons:
                    raise AssertionError('Unsupported variable comparator: ' + op)
                if not comparisons[op]:
                    return False
            return True
        if key == 'capital_scope':
            return self.test(arg, country, State(continent=country.continent))
        if key == 'is_on_continent':
            return state.continent == arg
        if key == 'any_owned_state':
            return any(self.test(arg, country, item) for item in country.states)
        if key == 'is_coastal':
            return state.coastal == (arg == 'yes')
        if key == 'is_core_of':
            assert arg == 'PREV', arg
            return state.core
        if key == 'is_controlled_by':
            assert arg == 'PREV', arg
            return state.controlled
        raise AssertionError('Unsupported trigger: ' + key)

    def number(self, token, country):
        try:
            return float(token)
        except ValueError:
            if token == 'modifier@globalism_equilibrium':
                return country.equilibrium
            if token in self.temp.get(id(country), {}):
                return self.temp[id(country)][token]
            return country.variables.get(token, 0.0)

    def run(self, name, country=None):
        if not self.effect_depth:
            self.temp = {}
        self.effect_depth += 1
        try:
            self.execute(EFFECTS[name], country)
        finally:
            self.effect_depth -= 1

    def execute(self, rows, country):
        branch_taken = None
        for key, op, arg in rows:
            if key in ('if', 'else_if', 'else'):
                if key == 'if':
                    branch_taken = False
                elif branch_taken is None:
                    raise AssertionError('Orphan else branch')
                if not branch_taken and (key == 'else' or self.test(first(arg, 'limit'), country)):
                    self.execute([row for row in arg if row[0] != 'limit'], country)
                    branch_taken = True
                continue
            branch_taken = None
            if key in EFFECTS:
                assert arg == 'yes', (key, arg)
                self.run(key, country)
            elif key == 'every_country':
                for item in self.countries:
                    self.execute(arg, item)
            elif key in ('set_variable', 'set_temp_variable', 'multiply_variable', 'add_to_variable'):
                assert len(arg) == 1, arg
                variable, _, token = arg[0]
                value = self.number(token, country)
                if key == 'set_temp_variable':
                    self.temp.setdefault(id(country), {})[variable] = value
                elif key == 'set_variable':
                    country.variables[variable] = value
                elif key == 'multiply_variable':
                    country.variables[variable] = country.variables.get(variable, 0) * value
                else:
                    country.variables[variable] = country.variables.get(variable, 0) + value
            elif key == 'clamp_variable':
                variable = first(arg, 'var')
                country.variables[variable] = max(
                    self.number(first(arg, 'min'), country),
                    min(self.number(first(arg, 'max'), country), country.variables.get(variable, 0)))
            elif key == 'clear_variable':
                country.variables.pop(arg, None)
            elif key == 'add_dynamic_modifier':
                country.dynamic.add(first(arg, 'modifier'))
                country.additions += 1
            elif key == 'remove_dynamic_modifier':
                country.dynamic.discard(first(arg, 'modifier'))
                country.removals += 1
            elif key == 'force_update_dynamic_modifier':
                country.refreshes += 1
            elif key == 'ingame_update_setup':
                # Bounded native boundary: execute its real leading Suez effect,
                # then record what the downstream fiscal calculations would see.
                # A country/world recursion through this entry point must fail.
                if self.native_depth:
                    raise AssertionError('Recursive fiscal refresh')
                self.native_depth += 1
                try:
                    self.execute(MONEY_ENTRY[:1], country)
                    country.fiscal_refreshes += 1
                    country.fiscal_snapshot = dict(country.variables)
                finally:
                    self.native_depth -= 1
            else:
                raise AssertionError('Unsupported effect: ' + key)


class CalculationTests(unittest.TestCase):
    def calculate(self, tag='EGY', globalism=75, **kwargs):
        country = Country(tag, variables={'globalism_value': globalism}, **kwargs)
        Model(country).run('mdcw_suez_calculate_exposure', country)
        return country

    def test_all_six_maxima_and_dynamic_modifier_mapping(self):
        country = self.calculate(globalism=100)
        self.assertEqual(country.variables['mdcw_suez_burden'], 1)
        metadata = {'icon', 'enable', 'remove_trigger', 'custom_modifier_tooltip'}
        actual_mapping = {k: v for k, op, v in DYNAMIC if k not in metadata}
        self.assertEqual(actual_mapping, {key: pair[0] for key, pair in EXPECTED.items()})
        for variable, maximum in EXPECTED.values():
            self.assertAlmostEqual(country.variables[variable], maximum)

    def test_floor_and_formula_examples(self):
        for tag in ('EGY', 'RAJ', 'PER', 'CHI', 'USA'):
            country = self.calculate(tag, 0)
            self.assertAlmostEqual(country.variables['mdcw_suez_burden'], .20)
            for variable, maximum in EXPECTED.values():
                self.assertAlmostEqual(country.variables[variable], maximum * .20)
        for tag, expected in (('EGY', .8), ('USA', .44), ('PER', .6425)):
            self.assertAlmostEqual(self.calculate(tag).variables['mdcw_suez_burden'], expected)

    def test_monotonic_globalism_and_route_exposure(self):
        tags = ('USA', 'SOV', 'CHI', 'PER', 'RAJ', 'EGY')
        for tag in tags:
            burdens = [self.calculate(tag, g).variables['mdcw_suez_burden']
                       for g in (0, 25, 50, 75, 100)]
            self.assertEqual(burdens, sorted(burdens))
            self.assertGreater(burdens[-1], burdens[0])
        for globalism in (25, 50, 75, 100):
            burdens = [self.calculate(tag, globalism).variables['mdcw_suez_burden'] for tag in tags]
            self.assertEqual(burdens, sorted(burdens))

    def test_input_and_intermediate_clamps(self):
        low, high = self.calculate(globalism=-90), self.calculate(globalism=500)
        self.assertEqual(low.variables['mdcw_suez_globalism'], 0)
        self.assertEqual(high.variables['mdcw_suez_globalism'], 100)
        self.assertAlmostEqual(low.variables['mdcw_suez_burden'], .20)
        self.assertAlmostEqual(high.variables['mdcw_suez_burden'], 1)
        self.assertEqual(low.variables['globalism_value'], -90)
        self.assertEqual(high.variables['globalism_value'], 500)
        # Execute the actual authored clamp nodes with boundary-breaking inputs.
        for key, op, arg in EFFECTS['mdcw_suez_calculate_exposure']:
            if key == 'clamp_variable' and first(arg, 'var') in ('mdcw_suez_route', 'mdcw_suez_burden'):
                variable = first(arg, 'var')
                for start, expected in ((-1, float(first(arg, 'min'))), (9, float(first(arg, 'max')))):
                    high.variables[variable] = start
                    Model(high).execute([(key, op, arg)], high)
                    self.assertEqual(high.variables[variable], expected)

    def test_missing_globalism_falls_back_without_writing_actual_globalism(self):
        country = Country('EGY', variables={'unrelated': 7}, equilibrium=75)
        Model(country).run('mdcw_suez_calculate_exposure', country)
        self.assertEqual(country.variables['mdcw_suez_globalism'], 75)
        self.assertAlmostEqual(country.variables['mdcw_suez_burden'], .8)
        self.assertNotIn('globalism_value', country.variables)
        self.assertEqual(country.variables['unrelated'], 7)

    def test_real_country_tags_and_route_groups(self):
        tags = {}
        for path in (ROOT / 'common/country_tags').glob('*.txt'):
            tags.update({k: v.strip('"') for k, op, v in parse(path.read_text(encoding='utf-8-sig'))})
        for tag, country_file in (('RAJ', 'British Raj'), ('IND', 'Indonesia'),
                                  ('MRT', 'Mauritius'), ('MAU', 'Mauritania'), ('SYE', 'South Yemen')):
            self.assertIn(country_file, tags[tag])
        exposure_rows = [(k, '=', v) for k, v in EXPOSURE.items()]
        for tag in {v for k, op, v in walk(exposure_rows) if k == 'original_tag'}:
            self.assertIn(tag, tags)
        for tag, route in (('RAJ', .85), ('IND', .65), ('MRT', .85), ('MAU', .20),
                           ('SYE', 1), ('CBD', .40), ('CAM', .20), ('SOV', .35)):
            self.assertAlmostEqual(self.calculate(tag).variables['mdcw_suez_route'], route)
        self.assertAlmostEqual(self.calculate('GER', continent='europe').variables['mdcw_suez_route'], .85)
        self.assertAlmostEqual(self.calculate('AST', continent='australia').variables['mdcw_suez_route'], .40)

    def test_home_coast_requires_owned_controlled_core_and_no_colonial_upgrade(self):
        for states in ([], [State(coastal=False)], [State(core=False)], [State(controlled=False)]):
            self.assertAlmostEqual(self.calculate('RAJ', states=states).variables['mdcw_suez_route'], .51)
        self.assertAlmostEqual(self.calculate('RAJ', states=[State(), State(core=False)]).variables['mdcw_suez_route'], .85)
        # A European colony neither makes an American capital European nor gives
        # an otherwise inland home economy a controlled core coast.
        overseas = Country('USA', continent='north_america', states=[State(core=False, continent='europe')])
        Model(overseas).run('mdcw_suez_calculate_exposure', overseas)
        self.assertAlmostEqual(overseas.variables['mdcw_suez_route'], .12)


class ReconciliationTests(unittest.TestCase):
    def test_world_add_refresh_reopen_and_reclose_are_idempotent(self):
        countries = [Country('EGY'), Country('USA'), Country('RAJ')]
        model = Model(*countries)
        for _ in range(3):
            model.run('mdcw_suez_update_world')
        for country in countries:
            self.assertEqual(country.dynamic, {SPIRIT})
            self.assertEqual(country.additions, 1)
        countries[0].variables['globalism_value'] = 25
        model.run('mdcw_suez_update_world')
        self.assertAlmostEqual(countries[0].variables['mdcw_suez_burden'], .4)
        model.flags.clear()
        for _ in range(3):
            model.run('mdcw_suez_update_world')
        for country in countries:
            self.assertFalse(country.dynamic)
            self.assertEqual(country.removals, 1)
            self.assertFalse(any(key.startswith('mdcw_suez_') for key in country.variables))
            self.assertIn('globalism_value', country.variables)
        model.flags.add(FLAG)
        model.run('mdcw_suez_update_world')
        self.assertTrue(all(country.dynamic == {SPIRIT} and country.additions == 2 for country in countries))

    def test_new_country_and_special_exclusions(self):
        model = Model(Country('EGY'), Country('ZOM'), Country('ALN'))
        model.run('mdcw_suez_update_world')
        self.assertEqual(model.countries[0].dynamic, {SPIRIT})
        for country in model.countries[1:]:
            self.assertFalse(country.dynamic)
            self.assertFalse(any(key.startswith('mdcw_suez_') for key in country.variables))
        released = Country('SYE', variables={})
        model.countries.append(released)
        model.run('mdcw_suez_update_country', released)
        self.assertEqual(released.dynamic, {SPIRIT})
        released.tag = 'ZOM'
        model.run('mdcw_suez_update_country', released)
        self.assertFalse(released.dynamic)
        self.assertEqual(released.variables, {'last_productivity_check': -1})

    def test_orphan_modifier_and_open_start_cleanup(self):
        country = Country('USA', variables={'unrelated': 7}, dynamic={SPIRIT})
        model = Model(country, closed=False)
        model.run('mdcw_suez_update_country', country)
        model.run('mdcw_suez_update_country', country)
        self.assertFalse(country.dynamic)
        self.assertEqual(country.removals, 1)
        self.assertEqual(country.variables, {'unrelated': 7, 'last_productivity_check': -1})
        clean = Country('EGY')
        model.run('mdcw_suez_update_country', clean)
        self.assertEqual(clean.additions, 0)
        self.assertFalse(any(key.startswith('mdcw_suez_') for key in clean.variables))

    def test_native_productivity_cache_invalidates_only_when_burden_changes(self):
        country = Country('EGY', variables={'globalism_value': 75, 'last_productivity_check': 500})
        model = Model(country)
        model.run('mdcw_suez_update_country', country)
        self.assertEqual(country.variables['last_productivity_check'], -1)
        self.assertNotIn('mdcw_suez_previous_burden', country.variables)
        country.variables['last_productivity_check'] = 500
        model.run('mdcw_suez_update_country', country)
        self.assertEqual(country.variables['last_productivity_check'], 500)
        country.variables['globalism_value'] = 25
        model.run('mdcw_suez_update_country', country)
        self.assertEqual(country.variables['last_productivity_check'], -1)
        self.assertAlmostEqual(country.variables['mdcw_suez_burden'], .4)
        country.variables['last_productivity_check'] = 500
        model.flags.clear()
        model.run('mdcw_suez_update_country', country)
        self.assertEqual(country.variables['last_productivity_check'], -1)
        self.assertFalse(any(key.startswith('mdcw_suez_') for key in country.variables))
        country.variables['last_productivity_check'] = 500
        model.run('mdcw_suez_update_country', country)
        self.assertEqual(country.variables['last_productivity_check'], 500)

    def test_dynamic_runtime_enable_and_remove_guards(self):
        for closed in (False, True):
            for tag in ('EGY', 'USA', 'ZOM', 'ALN'):
                country = Country(tag)
                model = Model(country, closed=closed)
                should_enable = closed and tag not in ('ZOM', 'ALN')
                self.assertEqual(model.test(first(DYNAMIC, 'enable'), country), should_enable)
                self.assertEqual(model.test(first(DYNAMIC, 'remove_trigger'), country), not should_enable)

    def test_only_initialized_transition_targets_refresh_fiscal_cache(self):
        initialized = Country('EGY', variables={'globalism_value': 75, 'last_quarter_gdp_total': 100})
        bootstrap = Country('USA')
        special = Country('ZOM', variables={'last_quarter_gdp_total': 100})
        model = Model(initialized, bootstrap, special)
        model.run('mdcw_suez_update_world')
        self.assertEqual(initialized.fiscal_refreshes, 1)
        self.assertEqual(initialized.fiscal_snapshot['mdcw_suez_burden'], .8)
        self.assertAlmostEqual(initialized.fiscal_snapshot['mdcw_suez_export_revenue'], -.192)
        self.assertEqual(bootstrap.fiscal_refreshes, 0)
        self.assertEqual(bootstrap.dynamic, {SPIRIT})
        self.assertEqual(special.fiscal_refreshes, 0)
        # Regular country/weekly updates reconcile their spirit without a full
        # global fiscal recalculation or native-entry recursion.
        initialized.variables['globalism_value'] = 25
        model.run('mdcw_suez_update_country', initialized)
        self.assertAlmostEqual(initialized.variables['mdcw_suez_burden'], .4)
        self.assertEqual(initialized.fiscal_refreshes, 1)
        model.flags.clear()
        model.run('mdcw_suez_update_world')
        self.assertEqual(initialized.fiscal_refreshes, 2)
        self.assertNotIn('mdcw_suez_burden', initialized.fiscal_snapshot)
        self.assertNotIn('mdcw_suez_export_revenue', initialized.fiscal_snapshot)
        self.assertEqual(bootstrap.fiscal_refreshes, 0)
        self.assertEqual(special.fiscal_refreshes, 0)
        model.run('mdcw_suez_update_world')
        self.assertEqual(initialized.fiscal_refreshes, 2)
        self.assertEqual(model.native_depth, 0)

    def test_initialized_orphan_refreshes_and_native_order_precedes_receipts(self):
        orphan = Country('USA', variables={'last_quarter_gdp_total': 100}, dynamic={SPIRIT})
        model = Model(orphan, closed=False)
        model.run('mdcw_suez_update_world')
        self.assertEqual(orphan.fiscal_refreshes, 1)
        self.assertFalse(orphan.dynamic)
        # These assertions check the actual native entry source, rather than
        # teaching the stub its desired ordering or reimplementing MD finance.
        self.assertEqual(MONEY_ENTRY[0], ('mdcw_suez_update_country', '=', 'yes'))
        keys = [key for key, op, arg in MONEY_ENTRY]
        for receipt in ('update_state_variables', 'calculate_resource_sale_rate', 'calculate_tax_gain'):
            self.assertLess(keys.index('mdcw_suez_update_country'), keys.index(receipt))
        country_calls = {key for key, op, arg in walk(EFFECTS['mdcw_suez_update_country'])}
        exposure_calls = {key for key, op, arg in walk(EFFECTS['mdcw_suez_calculate_exposure'])}
        self.assertTrue({'ingame_update_setup', 'mdcw_suez_update_world'}.isdisjoint(country_calls | exposure_calls))
        weekly = first(definitions('common/on_actions/zzzzzzz_mdcw_suez_on_actions.txt')['on_actions'], 'on_weekly')
        weekly_calls = {key for key, op, arg in walk(weekly)}
        self.assertIn('mdcw_suez_update_country', weekly_calls)
        self.assertTrue({'ingame_update_setup', 'mdcw_suez_update_world'}.isdisjoint(weekly_calls))

    def test_icon_texture_and_english_localization(self):
        icon = first(DYNAMIC, 'icon')
        self.assertEqual(icon, 'GFX_idea_suez_canal_blocked')
        sprites = [value for key, op, value in walk(parse(source('interface/MD_ideas.gfx')))
                   if key == 'spriteType' and first(value, 'name') == '"' + icon + '"']
        self.assertEqual(len(sprites), 1)
        texture = first(sprites[0], 'texturefile').strip('"')
        self.assertTrue((ROOT / texture).is_file())
        path = ROOT / 'localisation/english/mdcw_suez_l_english.yml'
        self.assertTrue(path.read_bytes().startswith(b'\xef\xbb\xbf'))
        localized = path.read_text(encoding='utf-8-sig')
        self.assertTrue(localized.startswith('l_english:'))
        for key in (SPIRIT, SPIRIT + '_desc', first(DYNAMIC, 'custom_modifier_tooltip')):
            self.assertIn('\n ' + key + ':', localized)
        for variable in ('mdcw_suez_globalism', 'mdcw_suez_route', 'mdcw_suez_burden'):
            self.assertIn('[?' + variable + '|', localized)


if __name__ == '__main__':
    unittest.main(verbosity=2)
