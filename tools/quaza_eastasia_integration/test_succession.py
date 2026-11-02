# IMPERIA COLD WAR — Quaza East Asia: NKO succession emitted-script regression.
"""Execute the narrow Clausewitz subset used by the NKO succession emitter.

This proves generator-source behavior only. It does not prove native engine loading.
"""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/vietnam_1970"))
from script_ast import parse, first
sys.path.insert(0, str(ROOT / "tools/north_korea_1970"))
import succession


def defs(rows):
    return {key: value for key, _, value in rows if key != "_bare"}


class NativeSubset:
    def __init__(self, leader="Kim Il Sung", party=4, date=(1995, 1, 1)):
        self.leader = leader
        self.party = party
        self.date = date
        self.flags = set()
        self.global_flags = set()
        self.events = []
        self.killed = []
        self.created = []
        self.refreshes = 0

    def trigger(self, rows):
        for key, op, value in rows:
            if key in ("AND", "hidden_trigger"):
                ok = self.trigger(value)
            elif key == "OR":
                ok = any(self.trigger([row]) for row in value)
            elif key == "NOT":
                ok = not self.trigger(value)
            elif key == "tag":
                ok = value == "NKO"
            elif key == "original_tag":
                ok = value == "NKO"
            elif key == "IMP_is_1970_scenario":
                ok = value == "yes"
            elif key == "emerging_communist_state_are_in_power":
                ok = self.party == 4
            elif key == "check_variable":
                key2, op2, value2 = value[0]
                ok = key2 == "ruling_party" and op2 == "=" and self.party == int(value2)
            elif key == "has_country_flag":
                ok = value in self.flags
            elif key == "has_global_flag":
                ok = value in self.global_flags
            elif key == "has_country_leader":
                ok = self.leader == first(value, "name").strip('"')
            elif key == "always":
                ok = value == "yes"
            elif key == "date":
                date = tuple(int(part) for part in value.split("."))
                ok = {"<": self.date < date, "=": self.date == date, ">": self.date > date}[op]
            else:
                raise AssertionError(("unsupported trigger", key, op, value))
            if not ok:
                return False
        return True

    def effect(self, rows):
        previous_branch = False
        for key, op, value in rows:
            if key in ("if", "else_if"):
                previous_branch = self.trigger(first(value, "limit", []))
                if previous_branch:
                    self.effect([r for r in value if r[0] != "limit"])
            elif key == "else":
                if not previous_branch:
                    self.effect(value)
            elif key == "set_country_flag":
                self.flags.add(value)
            elif key == "clr_country_flag":
                self.flags.discard(value)
            elif key == "set_global_flag":
                self.global_flags.add(value)
            elif key == "kill_country_leader":
                self.killed.append(self.leader)
                self.leader = None
            elif key == "create_country_leader":
                leader = first(value, "name").strip('"')
                portrait = first(value, "picture").strip('"')
                self.created.append((leader, portrait))
                self.leader = leader
            elif key == "COLDWAR_NKO_refresh_programmes":
                self.refreshes += 1
            elif key == "news_event":
                self.events.append(first(value, "id"))
            elif key == "effect_tooltip":
                continue
            elif key == "hidden_effect":
                self.effect(value)
            elif key == "COLDWAR_NKO_install_kim_jong_il":
                self.effect(first(parse(succession.EFFECTS), key))
            else:
                raise AssertionError(("unsupported effect", key, op, value))

    def call_guarded_effect(self, body):
        # A scripted effect body is an if block whose guard is the outer limit.
        self.effect(body)


class SuccessionEmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.effects = defs(parse(succession.EFFECTS))
        cls.decisions = parse(succession.DECISIONS)
        cls.category = defs(parse(succession.CATEGORY))["COLDWAR_NKO_succession_category"]
        cls.events = parse(succession.EVENTS)

    def test_death_catches_up_once_and_leaves_mourning_government(self):
        m = NativeSubset(date=(1995, 1, 1))
        m.call_guarded_effect(self.effects["COLDWAR_NKO_succession_daily"])
        self.assertEqual(m.killed, ["Kim Il Sung"])
        self.assertEqual(m.created, [("Funeral Committee", "gfx/Leaders/NKO/COLDWAR_NKO_Kim_Il_Sung_memorial.dds")])
        self.assertEqual(m.leader, "Funeral Committee")
        self.assertIn("COLDWAR_NKO_kim_il_sung_death_recorded", m.flags)
        self.assertIn("COLDWAR_NKO_succession_pending", m.flags)
        self.assertNotIn("COLDWAR_NKO_kim_jong_il_succeeded", m.flags)
        self.assertNotIn("COLDWAR_NKO_1994_succession_announced", m.global_flags)
        self.assertEqual(m.events, ["COLDWAR_NKO_succession.1"])
        before = (list(m.killed), list(m.created), list(m.events), set(m.flags), set(m.global_flags))
        m.call_guarded_effect(self.effects["COLDWAR_NKO_succession_daily"])
        self.assertEqual((m.killed, m.created, m.events, m.flags, m.global_flags), before)

    def test_former_leader_is_not_killed_or_replaced(self):
        m = NativeSubset(leader="Alternate Leader", party=5)
        m.call_guarded_effect(self.effects["COLDWAR_NKO_succession_daily"])
        self.assertEqual(m.killed, [])
        self.assertEqual(m.created, [])
        self.assertEqual(m.leader, "Alternate Leader")
        self.assertIn("COLDWAR_NKO_kim_il_sung_death_recorded", m.flags)
        self.assertNotIn("COLDWAR_NKO_succession_pending", m.flags)

    def test_native_pool_spelling_also_dies_on_historical_date(self):
        m = NativeSubset(leader="Kim Il-sung", date=(1994, 7, 7))
        m.call_guarded_effect(self.effects["COLDWAR_NKO_succession_daily"])
        self.assertEqual(m.killed, [])
        m.date = (1994, 7, 8)
        m.call_guarded_effect(self.effects["COLDWAR_NKO_succession_daily"])
        self.assertEqual(m.killed, ["Kim Il-sung"])
        self.assertEqual(m.leader, "Funeral Committee")

    def test_mourning_router_repairs_caretaker_without_replaying_death(self):
        m = NativeSubset(leader="Alternate Leader")
        m.flags.update({"COLDWAR_NKO_kim_il_sung_death_recorded", "COLDWAR_NKO_succession_pending"})
        m.call_guarded_effect(self.effects["COLDWAR_NKO_preserve_mourning_government"])
        self.assertEqual(m.leader, "Funeral Committee")
        self.assertEqual(m.killed, [])
        self.assertEqual(m.events, [])
        self.assertEqual(m.created, [("Funeral Committee", "gfx/Leaders/NKO/COLDWAR_NKO_Kim_Il_Sung_memorial.dds")])

        blocked = NativeSubset(leader="Alternate Leader", party=5)
        blocked.flags.update(m.flags)
        blocked.call_guarded_effect(self.effects["COLDWAR_NKO_preserve_mourning_government"])
        self.assertEqual(blocked.leader, "Alternate Leader")
        self.assertEqual(blocked.created, [])

    def test_decision_is_reachable_under_caretaker_and_installs_once(self):
        m = NativeSubset(leader="Funeral Committee")
        m.flags.update({"COLDWAR_NKO_kim_il_sung_death_recorded", "COLDWAR_NKO_succession_pending"})
        category = first(self.decisions, "COLDWAR_NKO_succession_category")
        decision = first(category, "COLDWAR_NKO_confirm_kim_jong_il")
        available = first(decision, "available")
        self.assertTrue(m.trigger(available), "decision must not require Kim Jong Il already in office")
        self.assertTrue(m.trigger(first(self.category, "visible")))
        self.assertEqual(first(decision, "cost"), "0")
        complete = first(decision, "complete_effect")
        self.assertEqual(first(complete, "hidden_effect"), [("COLDWAR_NKO_install_kim_jong_il", "=", "yes")])
        m.effect([("effect_tooltip", "=", first(complete, "effect_tooltip"))])
        self.assertEqual(m.created, [], "prospective portrait preview must not install a leader")

        install = self.effects["COLDWAR_NKO_install_kim_jong_il"]
        m.effect(complete)
        self.assertEqual(m.leader, "Kim Jong-il")
        self.assertEqual(m.created, [("Kim Jong-il", "gfx/Leaders/NKO/Kim_Jong_il.dds")])
        self.assertNotIn("COLDWAR_NKO_succession_pending", m.flags)
        self.assertIn("COLDWAR_NKO_kim_jong_il_succeeded", m.flags)
        self.assertIn("COLDWAR_NKO_1994_succession_announced", m.global_flags)
        self.assertEqual(m.events, ["COLDWAR_NKO_succession.2"])
        self.assertEqual(m.refreshes, 1)
        snapshot = (list(m.created), list(m.events), m.refreshes, set(m.flags), set(m.global_flags))
        m.call_guarded_effect(install)
        self.assertEqual((m.created, m.events, m.refreshes, m.flags, m.global_flags), snapshot)

    def test_party_and_unavailability_rechecked_by_decision_and_effect(self):
        for party, unavailable in ((5, False), (4, True)):
            m = NativeSubset(leader="Funeral Committee", party=party)
            m.flags.update({"COLDWAR_NKO_kim_il_sung_death_recorded", "COLDWAR_NKO_succession_pending"})
            if unavailable:
                m.flags.add("COLDWAR_NKO_kim_jong_il_unavailable")
            category = first(self.decisions, "COLDWAR_NKO_succession_category")
            decision = first(category, "COLDWAR_NKO_confirm_kim_jong_il")
            self.assertFalse(m.trigger(first(decision, "available")))
            m.call_guarded_effect(self.effects["COLDWAR_NKO_install_kim_jong_il"])
            self.assertEqual(m.leader, "Funeral Committee")
            self.assertEqual(m.created, [])
            self.assertEqual(m.events, [])

    def test_death_news_does_not_claim_successor_installed(self):
        texts = [value for key, _, value in self.events[1][2] if key == "desc"]
        self.assertIn("COLDWAR_NKO_succession.1.d_incumbent", repr(texts))
        self.assertIn("COLDWAR_NKO_succession.1.d_former", repr(texts))
        loc = succession.ENGLISH_LOCALIZATION
        death_text = loc.split("COLDWAR_NKO_succession.2.t:", 1)[0]
        self.assertNotIn("Kim Jong Il has assumed", death_text)
        self.assertIn("COLDWAR_NKO_succession.2.d", succession.EVENTS)


if __name__ == "__main__":
    unittest.main()
