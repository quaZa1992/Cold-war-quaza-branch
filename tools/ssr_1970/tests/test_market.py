# IMPERIA COLD WAR — Focused tests for the SSR market transition module.
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "tools" / "ssr_1970"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(ROOT / "tools" / "vietnam_1970"))
import market
import shared
from script_ast import first, parse, values, walk


class MarketProtocol:
    """Small behavioral harness for the generated market transaction contract."""
    AUTHORITY_METHODS = {"auction": "market", "workers": "market", "public": "public"}

    def __init__(self):
        self.started = False
        self.course = None
        self.deadline = 0
        self.independent = True
        self.original_burden = 0
        self.burden = 0
        self.pending = None
        self.receipts = set()
        self.cooldown = 0
        self.treasury = 0
        self.settlement_modifiers = {}
        self.state = None

    def start(self, course):
        if self.started:
            return False
        item = shared.data()["market"]["courses"][course]
        self.started = True
        self.course = course
        self.deadline = item["window"]["days"]
        self.original_burden = item["burden"]["modifiers"]["consumer_goods_factor"]
        self.burden = self.original_burden
        return True

    def tick(self, days, independent=None):
        if independent is not None:
            self.independent = independent
        self.deadline = max(0, self.deadline - days)
        self.cooldown = max(0, self.cooldown - days)

    def active_window(self):
        return self.independent and self.started and self.deadline > 0

    def weekly_expense(self, gdp):
        if not self.independent or not self.started or self.burden <= 0:
            return 0
        return gdp * shared.data()["market"]["courses"][self.course]["weekly_gdp_cost"]

    def authorize(self, party, receipts):
        self.party = party
        self.authority_receipts = set(receipts)

    def begin(self, sector, method, state=None):
        if self.pending or self.cooldown or sector in self.receipts:
            return False
        self.pending = (sector, method, state)
        return True

    def cancel(self):
        self.pending = None

    def settle(self, gdp, independent=None):
        if not self.pending:
            return False
        sector, method, state = self.pending
        data = shared.data()["market"]["methods"][method]
        if independent is not None:
            self.independent = independent
        authority_kind = self.AUTHORITY_METHODS.get(method)
        valid_authority = authority_kind is None or (
            getattr(self, "party", None) is not None
            and getattr(self, "authority_receipts", set())
            and (authority_kind, self.party) in self.authority_receipts
        )
        valid_state = method != "liquidate" or (
            state and state["owned"] and state["controlled"] and state["core"] and state["civ"] >= 2
        )
        fee = gdp * data["gdp_cost"]
        if not self.independent or not valid_authority or not valid_state or self.treasury <= fee:
            self.pending = None
            return False
        self.treasury -= fee
        self.treasury += gdp * data["gdp_income"]
        if method == "liquidate":
            state["civ"] -= 1
        self.receipts.add(sector)
        self.cooldown = 30
        self.burden = max(0, self.burden - self.original_burden / 6)
        for key, value in data["modifiers"].items():
            self.settlement_modifiers[key] = self.settlement_modifiers.get(key, 0) + value
        self.pending = None
        return True


class MarketContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        market.generate()
        cls.effects = (ROOT / "common/scripted_effects/COLDWAR_SSR_market.txt").read_text(encoding="utf-8")
        cls.triggers = (ROOT / "common/scripted_triggers/COLDWAR_SSR_market.txt").read_text(encoding="utf-8")
        cls.decisions = (ROOT / "common/decisions/COLDWAR_SSR_market.txt").read_text(encoding="utf-8")
        cls.category = (ROOT / "common/decisions/categories/COLDWAR_SSR_market.txt").read_text(encoding="utf-8")
        cls.dynamic = (ROOT / "common/dynamic_modifiers/COLDWAR_SSR_market.txt").read_text(encoding="utf-8")
        cls.preview_ideas = (ROOT / "common/ideas/COLDWAR_SSR_market_preview.txt").read_text(encoding="utf-8")

    def test_course_deadline_is_once_only_persists_through_save_and_status_change(self):
        model = MarketProtocol()
        self.assertTrue(model.start("shock"))
        self.assertFalse(model.start("gradual"))
        saved = copy.deepcopy(model)
        saved.tick(100, independent=False)
        self.assertEqual(saved.deadline, 630)
        self.assertFalse(saved.active_window())
        restored = copy.deepcopy(saved)
        restored.tick(30, independent=True)
        self.assertEqual(restored.deadline, 600)
        self.assertTrue(restored.active_window())
        self.assertFalse(restored.start("directed"))
        for course in shared.data()["market"]["courses"]:
            start = self.effects.split(f"COLDWAR_SSR_start_market_{course} = {{", 1)[1].split("\n}\n", 1)[0]
            self.assertIn("NOT = { has_country_flag = COLDWAR_SSR_market_course_started }", start)
            self.assertIn(f"flag = COLDWAR_SSR_market_{course}_deadline value = 1 days = 730", start)
            self.assertNotIn("clr_country_flag", start)

    def test_all_timed_market_flags_are_set_to_one(self):
        timed_flags = []
        for source in (self.effects, self.decisions):
            for key, op, value in walk(parse(source)):
                if key == "set_country_flag" and op == "=" and isinstance(value, list) and first(value, "days") is not None:
                    flag = first(value, "flag")
                    timed_flags.append(flag)
                    self.assertEqual(first(value, "value"), "1", flag)
        self.assertTrue(timed_flags)
        self.assertEqual(
            {flag.removeprefix("COLDWAR_SSR_market_") for flag in timed_flags},
            {"shock_deadline", "gradual_deadline", "directed_deadline", "lot_cooldown", "pending_timer"},
        )

    def test_weekly_operating_share_follows_unresolved_burden_past_deadline(self):
        model = MarketProtocol()
        model.start("gradual")
        model.treasury = 1_000_000
        rate = shared.data()["market"]["courses"]["gradual"]["weekly_gdp_cost"]
        model.tick(730)
        self.assertEqual(model.deadline, 0)
        self.assertFalse(model.active_window())
        self.assertEqual(model.weekly_expense(2000), 2000 * rate)

        budget = self.effects.split("COLDWAR_SSR_market_refresh_budget = {", 1)[1].split("\n}", 1)[0]
        self.assertIn("COLDWAR_SSR_is_independent = yes has_country_flag = COLDWAR_SSR_market_course_started", budget)
        self.assertIn("has_country_flag = COLDWAR_SSR_market_gradual_started check_variable = { COLDWAR_SSR_market_burden_remaining > 0 }", budget)
        self.assertIn(f"value = gdp_total multiply = {shared.number(rate)}", budget)
        self.assertNotIn("COLDWAR_SSR_market_gradual_deadline", budget)

        model.independent = False
        self.assertEqual(model.weekly_expense(2000), 0)
        model.independent = True
        self.assertEqual(model.weekly_expense(4000), 4000 * rate)

        sectors = [d["sector"] for d in shared.data()["market"]["decisions"] if d["method"] == "liquidate"]
        for index, sector in enumerate(sectors):
            self.assertTrue(model.begin(sector, "liquidate", {"owned": True, "controlled": True, "core": True, "civ": 2}))
            self.assertTrue(model.settle(gdp=4000, independent=True))
            if index < len(sectors) - 1:
                model.tick(30)
        self.assertEqual(model.burden, 0)
        self.assertEqual(model.weekly_expense(4000), 0)

    def test_preview_callbacks_are_nonexecuting_and_show_all_course_modifiers(self):
        for course in shared.data()["market"]["courses"]:
            block = self.effects.split(f"COLDWAR_SSR_preview_market_{course} = {{", 1)[1].split("\n}", 1)[0]
            self.assertIn("effect_tooltip =", block)
            self.assertIn(f"COLDWAR_SSR_market_preview_{course}_window", block)
            self.assertIn(f"COLDWAR_SSR_market_preview_{course}_fiscal", block)
            self.assertIn(f"COLDWAR_SSR_market_preview_{course}_burden", block)
            self.assertNotIn("modify_treasury_effect", block)
            self.assertNotIn("set_country_flag", block)
        self.assertIn("consumer_goods_factor = 0.18", self.preview_ideas)

    def test_preview_ideas_have_native_wrapper_and_all_transitive_references_resolve(self):
        parsed = parse(self.preview_ideas)
        root = first(parsed, "ideas")
        self.assertIsInstance(root, list)
        country = first(root, "country")
        self.assertIsInstance(country, list)
        idea_blocks = {key: value for key, op, value in country if op == "=" and isinstance(value, list)}

        expected = {
            *(f"COLDWAR_SSR_market_preview_{course}_{suffix}"
              for course in shared.data()["market"]["courses"]
              for suffix in ("window", "fiscal", "burden")),
            *(f"COLDWAR_SSR_market_method_preview_{method}"
              for method in shared.data()["market"]["methods"]),
        }
        self.assertEqual(set(idea_blocks), expected)

        for idea_id, idea in idea_blocks.items():
            self.assertEqual(first(idea, "picture"), "industrial_concern", idea_id)
            self.assertEqual(first(first(idea, "allowed"), "always"), "no", idea_id)
            self.assertEqual(first(first(idea, "allowed_civil_war"), "always"), "yes", idea_id)
            self.assertIsInstance(first(idea, "modifier"), list, idea_id)

        references = set()
        for key, op, value in (*walk(parse(self.effects)), *walk(parse(self.decisions))):
            if key == "idea" and op == "=" and isinstance(value, str):
                references.add(value)
            elif key == "add_ideas" and op == "=" and isinstance(value, str):
                if value.startswith(("COLDWAR_SSR_market_preview_", "COLDWAR_SSR_market_method_preview_")):
                    references.add(value)
        self.assertEqual(references, expected)

        localisation = (ROOT / "localisation/english/COLDWAR_SSR_market_l_english.yml").read_text(encoding="utf-8-sig")
        for idea_id in expected:
            self.assertRegex(localisation, rf"(?m)^\s*{idea_id}:0\s+\"")
            self.assertRegex(localisation, rf"(?m)^\s*{idea_id}_desc:0\s+\"")

    def test_party_change_suspends_property_charters_and_completed_lots_stay_receipted(self):
        model = MarketProtocol()
        model.start("gradual")
        model.treasury = 100
        model.authorize("conservative", {("market", "liberal")})
        self.assertTrue(model.begin("light_industry", "auction"))
        self.assertFalse(model.settle(gdp=100, independent=True))
        self.assertEqual(model.treasury, 100)
        self.assertNotIn("light_industry", model.receipts)
        model.authorize("liberal", {("market", "liberal")})
        self.assertTrue(model.begin("light_industry", "auction"))
        self.assertTrue(model.settle(gdp=100, independent=True))
        self.assertIn("light_industry", model.receipts)
        self.assertFalse(model.begin("light_industry", "public"))
        self.assertIn("western_liberals_are_in_power = yes has_country_flag = COLDWAR_SSR_UKR_p2_market_rewarded", self.triggers)
        self.assertIn("neutrality_neutral_conservatism_are_in_power = yes has_country_flag = COLDWAR_SSR_UZB_p14_public_rewarded", self.triggers)

    def test_cancel_and_failed_validation_charge_nothing(self):
        model = MarketProtocol()
        model.start("shock")
        model.treasury = 20
        model.begin("food_processing", "workers")
        model.cancel()
        self.assertEqual(model.treasury, 20)
        self.assertFalse(model.receipts)
        model.authorize("liberal", {("market", "liberal")})
        model.begin("food_processing", "workers")
        self.assertFalse(model.settle(gdp=100, independent=False))
        self.assertEqual(model.treasury, 20)
        self.assertFalse(model.receipts)
        self.assertIn("COLDWAR_SSR_market_cancel_pending = yes", self.decisions)
        self.assertIn("COLDWAR_SSR_market_cancel_pending = {", self.effects)

    def test_settlement_price_uses_current_gdp_and_only_one_pending_lot(self):
        model = MarketProtocol()
        model.start("directed")
        model.treasury = 10
        self.assertTrue(model.begin("light_industry", "auction"))
        self.assertFalse(model.begin("food_processing", "workers"))
        model.authorize("liberal", {("market", "liberal")})
        before = model.treasury
        self.assertTrue(model.settle(gdp=200, independent=True))
        self.assertEqual(model.treasury, before - 200 * 0.0005 + 200 * 0.0015)
        self.assertEqual(model.cooldown, 30)
        self.assertIn("set_temp_variable = { treasury_change = { value = gdp_total multiply = -0.0005 } }", self.decisions)
        self.assertIn("COLDWAR_SSR_market_method_preview_auction", self.decisions)
        self.assertIn("COLDWAR_SSR_market_relief_preview_dynamic_modifier", self.decisions)

    def test_liquidation_rechecks_state_before_payment_and_removes_one_civ(self):
        model = MarketProtocol()
        model.start("shock")
        model.treasury = 10
        state = {"owned": True, "controlled": True, "core": True, "civ": 2}
        model.begin("consumer_durables", "liquidate", state)
        state["controlled"] = False
        before = model.treasury
        self.assertFalse(model.settle(gdp=100, independent=True))
        self.assertEqual(model.treasury, before)
        self.assertEqual(state["civ"], 2)
        state["controlled"] = True
        model.begin("consumer_durables", "liquidate", state)
        self.assertTrue(model.settle(gdp=100, independent=True))
        self.assertEqual(state["civ"], 1)
        close = self.effects.split("COLDWAR_SSR_market_complete_consumer_durables_liquidate = {", 1)[1].split("\n}", 1)[0]
        self.assertIn("check_variable = { building_level@industrial_complex > 1 }", close)
        self.assertIn("remove_building = { type = industrial_complex level = 1 }", close)
        self.assertLess(close.index("any_state ="), close.index("modify_treasury_effect"))
        self.assertNotIn("else = {", close)
        for tag in shared.TAGS:
            self.assertIn(f"COLDWAR_SSR_market_selected_{tag}", close)
        self.assertNotIn("selected_liquidation_state", close)
        decision = self.decisions.split("COLDWAR_SSR_market_consumer_durables_liquidate = {", 1)[1].split("\n\t}", 1)[0]
        self.assertIn("building_level@industrial_complex > 1", decision)
        self.assertNotIn("buildings = { industrial_complex", decision)

    def test_decision_completion_reserves_single_pending_transaction_immediately(self):
        start = self.decisions.split("COLDWAR_SSR_market_light_industry_auction = {", 1)[1].split("\n\t}", 1)[0]
        self.assertIn("complete_effect = {", start)
        self.assertNotIn("days_remove", start)
        self.assertLess(start.index("set_country_flag = COLDWAR_SSR_market_pending_light_industry_auction"), start.index("set_country_flag = COLDWAR_SSR_market_pending_transaction"))
        self.assertIn("NOT = { has_country_flag = COLDWAR_SSR_market_pending_transaction }", start)
        self.assertIn("COLDWAR_SSR_market_cancel_pending = yes", self.decisions)
        self.assertNotIn("COLDWAR_SSR_market_market_cancel_pending", self.decisions)

    def test_failed_liquidation_cannot_reach_factory_removal(self):
        close = self.effects.split("COLDWAR_SSR_market_complete_consumer_durables_liquidate = {", 1)[1].split("\n}\n", 1)[0]
        transaction = close.split("if = {", 1)[1].split("\n\t}\n", 1)[0]
        self.assertIn("limit = { COLDWAR_SSR_is_independent", transaction)
        self.assertIn("check_variable = { treasury > COLDWAR_SSR_market_transaction_cost }", transaction)
        self.assertIn("remove_building = { type = industrial_complex level = 1 }", transaction)
        self.assertNotIn("else =", close)
        # Exactly one removal command exists, and it is nested in the guarded success block.
        self.assertEqual(close.count("remove_building = { type = industrial_complex level = 1 }"), len(shared.TAGS))

    def test_decision_preview_contains_native_dynamic_cost_and_signed_rewards(self):
        auction = self.decisions.split("COLDWAR_SSR_market_light_industry_auction = {", 1)[1].split("\n\t}", 1)[0]
        preview = auction.split("effect_tooltip = {", 1)[1].split("\n\t\t}", 1)[0]
        self.assertIn("multiply = -0.0005", preview)
        self.assertIn("multiply = 0.0015", preview)
        self.assertIn("add_ideas = COLDWAR_SSR_market_method_preview_auction", preview)
        self.assertIn("add_dynamic_modifier = { modifier = COLDWAR_SSR_market_relief_preview_dynamic_modifier }", preview)
        self.assertIn("civilian_factories_productivity = 0.01", self.preview_ideas)

    def test_modifier_reconciliation_is_guarded_and_category_is_registered(self):
        reconcile = self.effects.split("COLDWAR_SSR_market_reconcile = {", 1)[1].split("\n}", 1)[0]
        self.assertIn("has_country_flag = COLDWAR_SSR_market_window_applied", reconcile)
        self.assertIn("has_country_flag = COLDWAR_SSR_market_burden_dirty", reconcile)
        self.assertIn("has_country_flag = COLDWAR_SSR_market_settlements_dirty", reconcile)
        self.assertNotIn("reconcile_authority", reconcile)
        self.assertNotIn("COLDWAR_SSR_market_refresh_budget = yes", reconcile)
        self.assertIn("COLDWAR_SSR_market_category = {", self.category)
        self.assertIn("visible_when_empty = yes", self.category)

    def test_each_market_modifier_removal_checks_actual_modifier_presence(self):
        reconcile = first(parse(self.effects), "COLDWAR_SSR_market_reconcile")

        def removals_with_guards(rows, guards=frozenset()):
            for key, op, value in rows:
                if key == "if" and isinstance(value, list):
                    limit = first(value, "limit", [])
                    local_guards = {
                        first(trigger, "modifier")
                        for trigger in values(limit, "has_dynamic_modifier")
                        if isinstance(trigger, list)
                    }
                    yield from removals_with_guards(value, guards | local_guards)
                elif key == "remove_dynamic_modifier" and isinstance(value, list):
                    yield first(value, "modifier"), guards
                elif isinstance(value, list):
                    yield from removals_with_guards(value, guards)

        observed = list(removals_with_guards(reconcile))
        expected = {
            "COLDWAR_SSR_market_window_dynamic_modifier",
            "COLDWAR_SSR_market_fiscal_dynamic_modifier",
            "COLDWAR_SSR_market_burden_dynamic_modifier",
            "COLDWAR_SSR_market_settlements_dynamic_modifier",
        }
        self.assertEqual({modifier for modifier, _ in observed}, expected)
        for modifier, guards in observed:
            self.assertIn(modifier, guards, f"unguarded removal of {modifier}")

    def test_outputs_have_project_marker_and_correct_encoding(self):
        for rel in (
            "common/scripted_effects/COLDWAR_SSR_market.txt",
            "common/scripted_triggers/COLDWAR_SSR_market.txt",
            "common/decisions/COLDWAR_SSR_market.txt",
            "common/decisions/categories/COLDWAR_SSR_market.txt",
            "common/dynamic_modifiers/COLDWAR_SSR_market.txt",
            "common/ideas/COLDWAR_SSR_market_preview.txt",
        ):
            raw = (ROOT / rel).read_bytes()
            self.assertFalse(raw.startswith(b"\xef\xbb\xbf"), rel)
            self.assertTrue(raw.startswith("# IMPERIA COLD WAR \u2014 Universal SSR focus programme.".encode("utf-8")), rel)
        loc = (ROOT / "localisation/english/COLDWAR_SSR_market_l_english.yml").read_bytes()
        self.assertTrue(loc.startswith(b"\xef\xbb\xbf"))
        self.assertTrue(loc.decode("utf-8-sig").startswith("l_english:\r\n" + shared.MARKER))


if __name__ == "__main__":
    unittest.main()
