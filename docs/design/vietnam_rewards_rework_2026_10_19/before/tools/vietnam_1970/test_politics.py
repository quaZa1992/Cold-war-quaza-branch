"""Execute the installed political helper AST in a small native-workflow model.

Run: python tools/vietnam_1970/test_politics.py
No files are written. This proves script-level sequencing, not HOI4 engine/UI
behaviour. Unsupported statements fail instead of being silently ignored.
"""
from copy import deepcopy
from pathlib import Path
import unittest

from script_ast import first, parse, values, walk

ROOT = Path(__file__).resolve().parents[2]
POLITICS = ROOT / "common/scripted_effects/COLDWAR_VIE_1970_politics.txt"
PROVIDER = ROOT / "common/scripted_effects/VIE_political_leaders.txt"
POOLS = ROOT / "common/scripted_effects/mdcw_historical_native_pools.txt"
DISPATCH = ROOT / "common/scripted_effects/00_leader_setup_scripted_effects.txt"
HELPERS = {key: body for key, _, body in parse(POLITICS.read_text(encoding="utf-8-sig"))}
VIE_PROVIDER = first(parse(PROVIDER.read_text(encoding="utf-8-sig")), "set_leader_VIE")


class Country:
    """Subset interpreter using authored AST and the actual VIE provider.

    native_dispatch models MD's observed sync -> kill -> country-provider
    order. The global source-order contract is independently asserted below.
    Other countries' country-specific providers are intentionally delegated.
    """
    def __init__(self, date="1970.1.1", leader="Le Duan", tag="VIE", scenario=True, dynamic=False):
        self.variables = {"ruling_party": 4}
        self.flags = set()
        self.leader = leader
        self.date = date
        self.tag, self.scenario, self.dynamic = tag, scenario, dynamic
        self.installs = 0
        self.native_calls = 0
        self.kills = 0
        self.programme_refreshes = 0
        self.trace = []

    def number(self, value):
        try:
            return float(value)
        except ValueError:
            return self.variables.get(value, 0)

    def condition(self, rows):
        results = []
        for key, op, value in rows:
            if key in ("AND", "limit"):
                result = self.condition(value)
            elif key == "OR":
                result = any(self.condition([entry]) for entry in value)
            elif key == "NOT":
                result = not self.condition(value)
            elif key == "original_tag":
                result = self.tag == value
            elif key == "IMP_is_1970_scenario":
                result = self.scenario == (value == "yes")
            elif key == "is_dynamic_country":
                result = self.dynamic == (value == "yes")
            elif key == "has_country_flag":
                result = value in self.flags
            elif key == "has_variable":
                result = value in self.variables
            elif key == "has_country_leader":
                result = self.leader == first(value, "name", "").strip('"')
            elif key == "check_variable":
                result = self.condition(value)
            elif key == "date":
                left = tuple(map(int, self.date.split(".")))
                right = tuple(map(int, value.split(".")))
                result = {"=": left == right, ">": left > right, "<": left < right}[op]
            else:
                left, right = self.variables.get(key, 0), self.number(value)
                result = {"=": left == right, ">": left > right, "<": left < right}[op]
            results.append(result)
        return all(results)

    def execute(self, rows):
        active = False
        for key, _, value in rows:
            if key == "if":
                active = self.condition(first(value, "limit", []))
                if active:
                    self.execute([entry for entry in value if entry[0] != "limit"])
            elif key == "else_if":
                if not active:
                    active = self.condition(first(value, "limit", []))
                    if active:
                        self.execute([entry for entry in value if entry[0] != "limit"])
            elif key == "else":
                if not active:
                    self.execute(value)
                active = False
            else:
                active = False
                if key in ("set_variable", "set_temp_variable"):
                    for variable, _, operand in value:
                        self.variables[variable] = self.number(operand)
                elif key == "add_to_variable":
                    for variable, _, operand in value:
                        self.variables[variable] = self.variables.get(variable, 0) + self.number(operand)
                elif key == "subtract_from_variable":
                    for variable, _, operand in value:
                        self.variables[variable] = self.variables.get(variable, 0) - self.number(operand)
                elif key == "clear_variable":
                    self.variables.pop(value, None)
                elif key == "set_country_flag":
                    self.flags.add(value)
                elif key == "hidden_effect":
                    self.execute(value)
                elif key == "kill_country_leader":
                    self.leader = None
                    self.kills += 1
                elif key == "create_country_leader":
                    self.leader = first(value, "name").strip('"')
                    self.installs += 1
                elif key == "set_leader":
                    self.native_dispatch()
                elif key in HELPERS:
                    self.call(key)
                elif key == "COLDWAR_VIE_sync_programmes":
                    assert self.leader is not None, "Programme sync ran before a leader existed"
                    self.programme_refreshes += 1
                elif key in ("update_set_politics", "update_dirty_politicsview_expanded", "set_correct_ideology_trait"):
                    pass
                else:
                    raise AssertionError("Unhandled authored effect: " + key)

    def call(self, name):
        self.execute(HELPERS[name])

    def native_dispatch(self):
        self.native_calls += 1
        if self.tag != "VIE" or self.dynamic:
            self.trace.append("delegated_other_country")
            return
        if self.scenario and self.variables["ruling_party"] == 4:
            self.trace.append("native_counter_sync")
            self.call("COLDWAR_VIE_1970_sync_leader_counter")
        self.trace.append("native_kill")
        self.leader = None
        self.kills += 1
        self.trace.append("country_provider")
        self.execute(VIE_PROVIDER)

    def retire(self):
        self.variables["MDCW_HP_native_retirement"] = 1
        self.native_dispatch()
        self.variables["MDCW_HP_native_retirement"] = 0

    def enter_party(self, slot):
        self.variables["ruling_party"] = slot
        self.native_dispatch()

    def tick(self, date):
        self.date = date
        self.call("COLDWAR_VIE_1970_update_politics")


class PoliticsTests(unittest.TestCase):
    def start(self):
        country = Country()
        country.call("COLDWAR_VIE_1970_initialize_politics")
        return country

    def test_start_is_preserved_and_initialization_is_idempotent(self):
        country = self.start()
        country.call("COLDWAR_VIE_1970_initialize_politics")
        self.assertEqual(country.leader, "Le Duan")
        self.assertEqual(country.variables["ruling_party"], 4)
        self.assertEqual(country.variables["communist_state_leader"], 0)
        self.assertEqual((country.installs, country.kills), (0, 0))

    def test_early_native_retirement_and_legacy_counter(self):
        country = self.start()
        for index, name in [(1, "Truong Chinh"), (2, "Nguyen Van Linh"), (3, "Vo Van Kiet"), (0, "Le Duan")]:
            country.retire()
            self.assertEqual(country.leader, name)
            self.assertEqual(country.variables["communist_state_leader"], index)
        self.assertIn("COLDWAR_VIE_1970_alternate_succession", country.flags)
        self.assertEqual(country.trace[:3], ["native_counter_sync", "native_kill", "country_provider"])

    def test_do_not_retire_preserves_actual_incumbent(self):
        country = self.start()
        country.retire()
        country.flags.add("do_not_retire")
        country.retire()
        self.assertEqual(country.leader, "Truong Chinh")
        self.assertEqual(country.variables["communist_state_leader"], 1)

    def test_party_away_return_remembers_person(self):
        country = self.start()
        country.retire()
        country.enter_party(2)
        self.assertEqual(country.leader, "Nghiem Xuan Yem")
        country.tick("1986.12.20")
        self.assertEqual(country.leader, "Nghiem Xuan Yem")
        country.enter_party(4)
        self.assertEqual(country.leader, "Truong Chinh")
        country.tick("1986.12.21")
        self.assertEqual(country.leader, "Truong Chinh")

    def test_socialist_secondary_and_reentry(self):
        country = self.start()
        country.enter_party(3)
        self.assertEqual(country.leader, "Nguyen Xien")
        country.retire()
        self.assertEqual(country.leader, "Hoang Minh Giam")
        country.enter_party(2)
        country.enter_party(3)
        self.assertEqual(country.leader, "Hoang Minh Giam")

    def test_historical_date_boundaries(self):
        country = self.start()
        for date, name in [("1986.7.13", "Le Duan"), ("1986.7.14", "Truong Chinh"), ("1986.12.17", "Truong Chinh"), ("1986.12.18", "Nguyen Van Linh")]:
            country.tick(date)
            self.assertEqual(country.leader, name)
        self.assertEqual((country.native_calls, country.installs), (2, 2))

    def test_expired_duan_in_four_day_gap(self):
        country = self.start()
        country.leader = None  # Engine expiry on 10 July need not preserve the name.
        country.tick("1986.7.13")
        self.assertIsNone(country.leader)
        country.tick("1986.7.14")
        self.assertEqual(country.leader, "Truong Chinh")
        self.assertEqual((country.native_calls, country.installs), (1, 1))

    def test_expiry_with_engine_fallback_name(self):
        country = self.start()
        country.leader = "Engine generated fallback"
        country.tick("1986.7.14")
        self.assertEqual(country.leader, "Truong Chinh")

    def test_december_catchup_installs_linh_once(self):
        country = self.start()
        country.leader = None
        country.tick("1986.12.18")
        self.assertEqual(country.leader, "Nguyen Van Linh")
        self.assertEqual((country.native_calls, country.installs, country.kills), (1, 1, 1))
        # Saved state/reload and subsequent daily ticks do not replay installation.
        country = deepcopy(country)
        country.tick("1986.12.19")
        self.assertEqual((country.native_calls, country.installs), (1, 1))

    def test_known_later_human_choice_beats_stale_memory(self):
        country = self.start()
        country.leader = "Vo Van Kiet"
        country.tick("1987.1.1")
        self.assertEqual(country.leader, "Vo Van Kiet")
        self.assertEqual(country.variables["communist_state_leader"], 3)
        self.assertEqual(country.installs, 0)

    def test_alternate_chinh_mandate_and_expiry(self):
        country = self.start()
        country.retire()
        country.tick("1986.12.18")
        self.assertEqual(country.leader, "Truong Chinh")
        country.leader = None
        country.tick("1988.9.30")
        self.assertEqual(country.leader, "Nguyen Van Linh")

    def test_collective_providers(self):
        country = self.start()
        for slot, name in [(0, "Nationalist Return Committee"), (19, "Fatherland Front Presidium"), (22, "Provisional Military Council")]:
            country.enter_party(slot)
            self.assertEqual(country.leader, name)

    def test_other_scenarios_countries_and_dynamic_tags(self):
        for kwargs in [{"scenario": False}, {"tag": "ROM"}, {"dynamic": True}]:
            country = Country(**kwargs)
            before = deepcopy(country.__dict__)
            country.call("COLDWAR_VIE_1970_initialize_politics")
            country.tick("1989.1.1")
            self.assertEqual(country.leader, before["leader"])
            self.assertEqual(country.variables, before["variables"])
            self.assertEqual(country.flags, before["flags"])
            self.assertEqual(country.installs, 0)
        modern = Country(scenario=False)
        modern.enter_party(2)
        self.assertEqual(modern.leader, "Do Hoang Diem")
        self.assertNotIn("COLDWAR_VIE_1970_communist_incumbent", modern.variables)

    def test_native_source_contract_and_supported_syntax(self):
        dispatch = first(parse(DISPATCH.read_text(encoding="utf-8-sig")), "set_leader")
        flattened = [key for key, _, _ in walk(dispatch)]
        self.assertLess(flattened.index("MDCW_HP_sync_native_counter"), flattened.index("kill_country_leader"))
        pool_ast = parse(POOLS.read_text(encoding="utf-8-sig"))
        pool = first(pool_ast, "MDCW_HP_native_pool_VIE_4")
        self.assertEqual(first(pool, "COLDWAR_VIE_1970_set_leader"), "yes")
        sync = first(pool_ast, "MDCW_HP_sync_native_counter")
        self.assertIn("COLDWAR_VIE_1970_sync_leader_counter", [key for key, _, _ in walk(sync)])
        for path in (POLITICS, PROVIDER, POOLS):
            self.assertFalse(any(op in (">=", "<=", "!=") for _, op, _ in walk(parse(path.read_text(encoding="utf-8-sig")))))


if __name__ == "__main__":
    unittest.main(verbosity=2)
