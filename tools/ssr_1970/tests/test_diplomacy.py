# IMPERIA COLD WAR — Universal SSR diplomacy tests.
from __future__ import annotations

import sys
import unittest
import re
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
import diplomacy as dip


@dataclass
class TestCountry:
    tag: str
    gdp: float = 1000.0
    treasury: float = 100.0
    alive: bool = True
    independent: bool = True
    ssr: bool = False
    wars: set[str] = field(default_factory=set)
    embargoes: set[str] = field(default_factory=set)
    sanctions: set[tuple[str, str]] = field(default_factory=set)
    factories: int = 8
    divisions: int = 8
    oil: float = 1.0
    basin: bool = False
    neighbours: set[str] = field(default_factory=set)
    ideas: set[str] = field(default_factory=set)


class AgreementModel:
    """Small transaction model used to test the contract invariants."""

    def __init__(self, countries: dict[str, TestCountry]):
        self.countries = countries
        self.pending: dict[tuple[str, str], str] = {}
        self.active: dict[tuple[str, str], str] = {}
        self.retry_days: dict[tuple[str, str], int] = {}
        self.origin_history: set[tuple[str, str]] = set()

    def pair_clear(self, origin: str, recipient: str) -> bool:
        a, b = self.countries[origin], self.countries[recipient]
        return (a.alive and b.alive and recipient not in a.wars and origin not in b.wars
                and recipient not in a.embargoes and origin not in b.embargoes
                and (recipient, "dip") not in a.sanctions and (origin, "dip") not in b.sanctions
                and all((recipient, kind) not in a.sanctions and (origin, kind) not in b.sanctions
                        for kind in ("fin", "eco", "mil")))

    def eligible(self, key: str, origin: str, recipient: str) -> bool:
        a, b = self.countries[origin], self.countries[recipient]
        if not self.pair_clear(origin, recipient) or not b.independent or origin == recipient:
            return False
        if key == "clearing":
            return recipient == "SOV" or recipient == "REC"
        if key == "technical":
            return b.factories > 4
        if key == "training":
            return b.divisions > 5
        if key == "border":
            return recipient in a.neighbours and origin in b.neighbours
        if key == "energy":
            return recipient in a.neighbours and (a.oil > 0 or b.oil > 0)
        if key == "water":
            return a.basin and b.basin
        if key == "romanian":
            return origin == "MLV" and recipient == "ROM"
        return False

    def offer(self, key: str, origin: str, recipient: str) -> bool:
        pair = (origin, key)
        if pair in self.pending or pair in self.active or self.retry_days.get(pair, 0) > 0:
            return False
        if not self.countries[origin].independent or not self.eligible(key, origin, recipient):
            return False
        self.pending[pair] = recipient
        self.origin_history.add(pair)
        return True

    def accept(self, key: str, origin: str, actor: str | None = None) -> bool:
        pair = (origin, key)
        recipient = self.pending.get(pair)
        actor = recipient if actor is None else actor
        if (recipient is None or actor != recipient or not self.countries[origin].independent
                or not self.eligible(key, origin, recipient)):
            return False
        terms = dip.CONTRACTS[key]
        a, b = self.countries[origin], self.countries[recipient]
        ca = a.gdp * terms["origin"]["gdp_cost"]
        cb = b.gdp * terms["recipient"]["gdp_cost"]
        if a.treasury < ca or b.treasury < cb:
            return False
        # Both checks precede either debit, preserving an atomic transaction.
        a.treasury -= ca
        b.treasury -= cb
        self.active[pair] = recipient
        del self.pending[pair]
        return True

    def refuse(self, key: str, origin: str) -> bool:
        pair = (origin, key)
        if pair not in self.pending:
            return False
        del self.pending[pair]
        self.retry_days[pair] = 180
        return True

    def tick(self, days: int) -> None:
        for pair in list(self.retry_days):
            self.retry_days[pair] = max(0, self.retry_days[pair] - days)

    def valid_pairs(self, recipient: str, key: str) -> list[str]:
        return [origin for (origin, active_key), target in self.active.items()
                if active_key == key and target == recipient and self.pair_clear(origin, recipient)]

    def weekly_expense(self, tag: str) -> float:
        total = 0.0
        for (origin, key), recipient in self.active.items():
            if not self.pair_clear(origin, recipient):
                continue
            if tag == origin:
                total += self.countries[tag].gdp * dip.CONTRACTS[key]["origin"]["weekly_gdp_cost"]
        for key in dip.KEYS:
            if self.valid_pairs(tag, key):
                total += self.countries[tag].gdp * dip.CONTRACTS[key]["recipient"]["weekly_gdp_cost"]
        return total

    def active_recipient_idea_count(self, tag: str, key: str) -> int:
        return int(bool(self.valid_pairs(tag, key)))

    def has_activity(self, tag: str) -> bool:
        return any(origin == tag or target == tag for (origin, _), target in self.pending.items()) or any(
            origin == tag or target == tag for (origin, _), target in self.active.items()
        )

    def terminate(self, key: str, origin: str, actor: str | None = None) -> bool:
        pair = (origin, key)
        target = self.active.get(pair)
        if actor is not None and actor not in {origin, target}:
            return False
        return self.active.pop(pair, None) is not None


class DiplomacyStaticTests(unittest.TestCase):
    def test_contract_schema_and_script_callbacks(self):
        self.assertEqual(set(dip.KEYS), {"clearing", "technical", "border", "training", "energy", "water", "romanian"})
        effects = dip._render_effects()
        triggers = dip._render_triggers()
        for key in dip.KEYS:
            self.assertIn(f"COLDWAR_SSR_offer_{key} =", effects)
            self.assertIn(f"COLDWAR_SSR_preview_offer_{key} =", effects)
            self.assertIn(f"COLDWAR_SSR_can_offer_{key} =", triggers)
            self.assertIn(dip._idea_id(key, "origin"), effects)
            self.assertIn(dip._idea_id(key, "recipient"), effects)
        self.assertIn("COLDWAR_SSR_diplomacy_reconcile =", effects)
        self.assertIn("COLDWAR_SSR_diplomacy_refresh_budget =", effects)
        self.assertIn("COLDWAR_SSR_diplomacy_weekly_expense", effects)
        self.assertIn("COLDWAR_SSR_negotiated_transition_active =", triggers)

    def test_pair_guards_cover_all_four_mirrored_sanctions(self):
        triggers = dip._render_triggers()
        for kind in ("dip", "fin", "eco", "mil"):
            for direction in ("on_us", "by_us"):
                self.assertIn(f"imp_{kind}_sanc_{direction}", triggers)
        self.assertIn("has_war_with", triggers)
        self.assertIn("is_embargoing", triggers)

    def test_recipient_pair_trigger_binds_saved_recipient_and_delegates_to_origin_scope(self):
        triggers = dip._render_triggers()
        recipient = triggers.split("COLDWAR_SSR_dip_pair_technical_UKR_to = {", 1)[1].split("\n}", 1)[0]
        origin = triggers.split("COLDWAR_SSR_dip_pair_technical_UKR_from = {", 1)[1].split("\n}", 1)[0]
        self.assertIn("tag = event_target:COLDWAR_SSR_dip_to_technical_UKR", recipient)
        self.assertIn("event_target:COLDWAR_SSR_dip_from_technical_UKR = { COLDWAR_SSR_dip_pair_technical_UKR_from = yes }", recipient)
        self.assertNotIn("COLDWAR_SSR_dip_pair_technical_UKR_from = yes", recipient.split("event_target:COLDWAR_SSR_dip_from_technical_UKR", 1)[0])
        self.assertIn("event_target:COLDWAR_SSR_dip_to_technical_UKR", origin)
        self.assertIn("num_of_factories > 4", origin)
        self.assertIn("COLDWAR_SSR_is_independent = yes", origin)

    def test_recipient_reconcile_and_budget_call_pair_trigger_in_recipient_scope(self):
        effects = dip._render_effects()
        reconcile = effects.split("COLDWAR_SSR_diplomacy_reconcile = {", 1)[1].split("COLDWAR_SSR_diplomacy_refresh_budget = {", 1)[0]
        budget = effects.split("COLDWAR_SSR_diplomacy_refresh_budget = {", 1)[1].split("\n}", 1)[0]
        for source in (reconcile, budget):
            self.assertIn("has_country_flag = COLDWAR_SSR_dip_in_technical_from_UKR_active COLDWAR_SSR_dip_pair_technical_UKR_to = yes", source)
            self.assertNotIn("UKR = { COLDWAR_SSR_dip_pair_technical_UKR_to = yes }", source)
        self.assertIn("NOT = { has_idea = COLDWAR_SSR_diplomacy_technical_recipient }", reconcile)
        self.assertIn("has_idea = COLDWAR_SSR_diplomacy_technical_recipient", reconcile)
        self.assertIn("NOT = { has_idea = COLDWAR_SSR_diplomacy_technical_origin }", reconcile)

    def test_refresh_budget_zeros_idle_country_and_guards_all_repeated_work(self):
        effects = dip._render_effects()
        budget = effects.split("COLDWAR_SSR_diplomacy_refresh_budget = {", 1)[1].split("\n}", 1)[0]
        self.assertLess(budget.index("set_variable = { COLDWAR_SSR_diplomacy_weekly_expense = 0 }"), budget.index(f"limit = {{ has_country_flag = {dip.ACTIVITY_FLAG} }}"))
        self.assertIn(f"limit = {{ has_country_flag = {dip.ACTIVITY_FLAG} }}\n        COLDWAR_SSR_diplomacy_reconcile = yes", budget)
        reconcile = effects.split("COLDWAR_SSR_diplomacy_reconcile = {", 1)[1].split("COLDWAR_SSR_diplomacy_refresh_budget = {", 1)[0]
        self.assertIn(f"limit = {{ has_country_flag = {dip.ACTIVITY_FLAG} }}", reconcile)
        update = effects.split("COLDWAR_SSR_diplomacy_update_activity = {", 1)[1].split("\n}", 1)[0]
        self.assertIn("COLDWAR_SSR_dip_in_clearing_from_UKR_pending", update)
        self.assertIn("COLDWAR_SSR_dip_clearing_active", update)
        terminate = dip._terminate_effect("technical", "UKR")
        origin_cleanup = terminate.split("UKR = {", 1)[1].split("\n        }", 1)[0]
        self.assertLess(origin_cleanup.index("COLDWAR_SSR_diplomacy_reconcile = yes"), origin_cleanup.index("COLDWAR_SSR_diplomacy_update_activity = yes"))
        recipient_cleanup = terminate.split("clr_country_flag = COLDWAR_SSR_dip_in_technical_from_UKR_active", 1)[1]
        self.assertLess(recipient_cleanup.index("COLDWAR_SSR_diplomacy_reconcile = yes"), recipient_cleanup.index("COLDWAR_SSR_diplomacy_update_activity = yes"))

    def test_daily_origin_reconcile_propagates_idea_transitions_to_recipient(self):
        effects = dip._render_effects()
        reconcile = effects.split("COLDWAR_SSR_diplomacy_reconcile = {", 1)[1].split("COLDWAR_SSR_diplomacy_refresh_budget = {", 1)[0]
        origin = reconcile.split("tag = UKR has_country_flag = COLDWAR_SSR_dip_technical_active", 1)[1].split("tag = UKR NOT = { has_country_flag = COLDWAR_SSR_dip_technical_active", 1)[0]
        notify = "event_target:COLDWAR_SSR_dip_to_technical_UKR = { COLDWAR_SSR_diplomacy_reconcile = yes }"
        self.assertLess(origin.index("add_ideas = COLDWAR_SSR_diplomacy_technical_origin"), origin.index(notify))
        self.assertLess(origin.index("remove_ideas = COLDWAR_SSR_diplomacy_technical_origin"), origin.rindex(notify))
        self.assertIn("COLDWAR_SSR_dip_pair_technical_UKR_from = yes", origin)
        self.assertIn("COLDWAR_SSR_dip_pair_technical_UKR_from = no", origin)
        lifecycle_source = (HERE.parent / "lifecycle.py").read_text(encoding="utf-8")
        self.assertIn("COLDWAR_SSR_market_reconcile = yes COLDWAR_SSR_diplomacy_reconcile = yes", lifecycle_source)

    def test_recipient_decision_hides_routing_receipts_and_category_tracks_active_pairs(self):
        decisions = dip._render_decisions()
        accept = decisions.split("COLDWAR_SSR_dip_accept_technical_UKR = {", 1)[1].split("\n    COLDWAR_SSR_dip_refuse_technical_UKR", 1)[0]
        hidden, visible = accept.split("} ", 1)
        self.assertIn("hidden_trigger = {", hidden)
        self.assertIn("tag = event_target:COLDWAR_SSR_dip_to_technical_UKR", hidden)
        self.assertNotIn("tag = event_target:COLDWAR_SSR_dip_from_technical_UKR", hidden)
        self.assertIn("has_country_flag = COLDWAR_SSR_dip_in_technical_from_UKR_pending", hidden)
        self.assertIn("has_war_with = event_target:COLDWAR_SSR_dip_from_technical_UKR", visible)
        self.assertIn("imp_mil_sanc_by_us", visible)
        self.assertIn("COLDWAR_SSR_is_independent = yes", visible)
        category = dip._render_decision_category()
        self.assertIn("allowed = { always = yes }", category)
        self.assertIn("has_country_flag = COLDWAR_SSR_dip_in_clearing_from_UKR_active", category)

    def test_accept_effect_binds_recipient_and_capability_to_current_target(self):
        effect = dip._accept_effect("technical", "UKR")
        self.assertIn("tag = event_target:COLDWAR_SSR_dip_to_technical_UKR", effect)
        self.assertNotIn("tag = event_target:COLDWAR_SSR_dip_from_technical_UKR", effect)
        self.assertIn("num_of_factories > 4", effect)
        self.assertNotIn("UKR = { num_of_factories > 4 }", effect)
        effect = dip._accept_effect("training", "UKR")
        self.assertIn("num_divisions > 5", effect)
        self.assertNotIn("UKR = { num_divisions > 5 }", effect)

    def test_all_static_real_tags_are_selectable_and_dynamic_tags_are_excluded(self):
        events = dip._render_events()
        self.assertTrue(set(dip.TAGS).issubset(dip.PARTNERS))
        self.assertNotIn("D01", dip.PARTNERS)
        for tag in dip.PARTNERS:
            self.assertIn(f"COLDWAR_SSR_select_clearing_{tag}", events)
        blocks = []
        for match in re.finditer(r"^country_event = \{", events, flags=re.MULTILINE):
            depth = 0
            end = match.start()
            for end in range(match.start(), len(events)):
                if events[end] == "{":
                    depth += 1
                elif events[end] == "}":
                    depth -= 1
                    if depth == 0:
                        break
            blocks.append(events[match.start():end + 1])
        self.assertEqual(len(blocks), 7 * (1 + len(dip.PARTNER_ROOT_GROUPS) + len(dip.PARTNER_SUBGROUPS) + len(dip.PARTNER_PAGES) + 1))
        option_counts = [len(re.findall(r"^    option = \{", block, flags=re.MULTILINE)) for block in blocks]
        self.assertLessEqual(max(option_counts), 8)
        self.assertIn("COLDWAR_SSR_select_clearing_group_0", events)
        self.assertNotRegex(events, r"option\s*=\s*\{[^{}]*\beffect\s*=")

    def test_preview_has_both_sides_and_percent_costs_even_without_a_target(self):
        effects = dip._render_effects()
        for key in dip.KEYS:
            preview = effects.split(f"COLDWAR_SSR_preview_offer_{key} =", 1)[1].split("\n\n", 1)[0]
            self.assertIn("COLDWAR_SSR_origin_scope_tt", preview)
            self.assertIn("COLDWAR_SSR_prospective_partner_tt", preview)
            self.assertIn("COLDWAR_SSR_setup_origin_share_tt", preview)
            self.assertIn("COLDWAR_SSR_setup_recipient_share_tt", preview)
            self.assertIn(dip._idea_id(key, "origin"), preview)
            self.assertIn(dip._idea_id(key, "recipient"), preview)

    def test_generated_scripts_are_balanced_and_marked(self):
        scripts = {
            "ideas": dip._render_ideas(),
            "triggers": dip._render_triggers(),
            "effects": dip._render_effects(),
            "events": dip._render_events(),
            "decisions": dip._render_decisions(),
            "category": dip._render_decision_category(),
        }
        for name, script in scripts.items():
            depth = 0
            quoted = False
            escaped = False
            for line in script.splitlines():
                line = line.split("#", 1)[0]
                for char in line:
                    if quoted:
                        if escaped:
                            escaped = False
                        elif char == "\\":
                            escaped = True
                        elif char == '"':
                            quoted = False
                    elif char == '"':
                        quoted = True
                    elif char == "{":
                        depth += 1
                    elif char == "}":
                        depth -= 1
                        self.assertGreaterEqual(depth, 0, f"{name} closes early")
            self.assertFalse(quoted, name)
            self.assertEqual(depth, 0, name)
        for rel in (
            "common/ideas/COLDWAR_SSR_diplomacy.txt",
            "common/scripted_triggers/COLDWAR_SSR_diplomacy.txt",
            "common/scripted_effects/COLDWAR_SSR_diplomacy.txt",
            "events/COLDWAR_SSR_diplomacy.txt",
            "common/decisions/COLDWAR_SSR_diplomacy.txt",
            "common/decisions/categories/COLDWAR_SSR_diplomacy.txt",
        ):
            self.assertTrue((ROOT / rel).read_text(encoding="utf-8").startswith("# IMPERIA COLD WAR"), rel)
        loc = (ROOT / "localisation/english/COLDWAR_SSR_diplomacy_l_english.yml").read_text(encoding="utf-8-sig")
        self.assertTrue(loc.startswith("l_english:\n# IMPERIA COLD WAR"))


class DiplomacyTransactionTests(unittest.TestCase):
    def setUp(self):
        self.countries = {
            "UKR": TestCountry("UKR", ssr=True, basin=True, neighbours={"POL", "BLR"}),
            "BLR": TestCountry("BLR", ssr=True, basin=True, neighbours={"UKR", "POL"}),
            "POL": TestCountry("POL", factories=20, divisions=15, neighbours={"UKR", "BLR"}),
            "GER": TestCountry("GER", factories=80, divisions=40),
            "ENG": TestCountry("ENG", factories=80, divisions=40),
            "SOV": TestCountry("SOV", factories=100, divisions=100),
            "MLV": TestCountry("MLV", ssr=True),
            "ROM": TestCountry("ROM", factories=20),
        }
        self.model = AgreementModel(self.countries)

    def test_offer_requires_real_consent_and_atomic_acceptance(self):
        self.assertTrue(self.model.offer("technical", "UKR", "POL"))
        self.assertNotIn(("UKR", "technical"), self.model.active)
        self.assertEqual(self.countries["UKR"].treasury, 100)
        self.assertEqual(self.countries["POL"].treasury, 100)
        self.assertTrue(self.model.accept("technical", "UKR"))
        self.assertAlmostEqual(self.countries["UKR"].treasury, 96)
        self.assertAlmostEqual(self.countries["POL"].treasury, 98.5)

    def test_only_named_recipient_can_accept(self):
        self.assertIn("GER", dip.PARTNERS)
        self.assertTrue(self.model.offer("technical", "UKR", "GER"))
        self.assertFalse(self.model.accept("technical", "UKR", actor="ROM"))
        self.assertIn(("UKR", "technical"), self.model.pending)
        self.assertEqual(self.countries["UKR"].treasury, 100)
        self.assertEqual(self.countries["ROM"].treasury, 100)
        self.assertTrue(self.model.accept("technical", "UKR", actor="GER"))

    def test_activity_receipt_tracks_pending_and_suspended_signed_terms(self):
        self.assertFalse(self.model.has_activity("UKR"))
        self.assertTrue(self.model.offer("technical", "UKR", "POL"))
        self.assertTrue(self.model.has_activity("UKR"))
        self.assertTrue(self.model.has_activity("POL"))
        self.assertTrue(self.model.accept("technical", "UKR"))
        self.countries["UKR"].wars.add("POL")
        self.assertTrue(self.model.has_activity("UKR"))
        self.assertTrue(self.model.has_activity("POL"))
        self.assertEqual(self.model.weekly_expense("UKR"), 0)
        self.countries["UKR"].wars.clear()
        self.assertTrue(self.model.has_activity("UKR"))
        self.assertTrue(self.model.terminate("technical", "UKR"))
        self.assertFalse(self.model.has_activity("UKR"))
        self.assertFalse(self.model.has_activity("POL"))

    def test_named_event_delivery_works_for_england_as_a_candidate(self):
        self.assertIn("ENG", dip.PARTNERS)
        self.assertTrue(self.model.offer("technical", "UKR", "ENG"))
        self.assertFalse(self.model.accept("technical", "UKR", actor="GER"))
        self.assertTrue(self.model.accept("technical", "UKR", actor="ENG"))

    def test_independent_origin_does_not_need_to_be_an_ssr(self):
        self.countries["UKR"].ssr = False
        self.assertTrue(self.model.offer("technical", "UKR", "POL"))
        self.assertTrue(self.model.accept("technical", "UKR"))

    def test_capability_and_geography_filters_are_contract_specific(self):
        self.assertTrue(self.model.eligible("technical", "UKR", "POL"))
        self.countries["POL"].factories = 4
        self.assertFalse(self.model.eligible("technical", "UKR", "POL"))
        self.countries["POL"].factories = 20
        self.assertTrue(self.model.eligible("training", "UKR", "POL"))
        self.countries["POL"].divisions = 5
        self.assertFalse(self.model.eligible("training", "UKR", "POL"))
        self.assertTrue(self.model.eligible("border", "UKR", "BLR"))
        self.assertTrue(self.model.eligible("energy", "UKR", "BLR"))
        self.assertTrue(self.model.eligible("water", "UKR", "BLR"))
        self.assertTrue(self.model.eligible("romanian", "MLV", "ROM"))

    def test_insufficient_either_side_charges_neither(self):
        self.assertTrue(self.model.offer("technical", "UKR", "POL"))
        self.countries["POL"].treasury = 1
        self.assertFalse(self.model.accept("technical", "UKR"))
        self.assertEqual(self.countries["UKR"].treasury, 100)
        self.assertEqual(self.countries["POL"].treasury, 1)
        self.assertIn(("UKR", "technical"), self.model.pending)

    def test_refusal_has_no_fee_and_reopens_after_180_days(self):
        self.assertTrue(self.model.offer("technical", "UKR", "POL"))
        self.assertTrue(self.model.has_activity("UKR"))
        self.assertTrue(self.model.has_activity("POL"))
        self.assertTrue(self.model.refuse("technical", "UKR"))
        self.assertFalse(self.model.has_activity("UKR"))
        self.assertFalse(self.model.has_activity("POL"))
        self.assertEqual(self.countries["UKR"].treasury, 100)
        self.assertEqual(self.countries["POL"].treasury, 100)
        self.assertFalse(self.model.offer("technical", "UKR", "POL"))
        self.model.tick(179)
        self.assertFalse(self.model.offer("technical", "UKR", "POL"))
        self.model.tick(1)
        self.assertTrue(self.model.offer("technical", "UKR", "POL"))

    def test_shared_recipient_modifiers_and_weekly_cost_are_deduplicated(self):
        self.assertTrue(self.model.offer("technical", "UKR", "POL"))
        self.assertTrue(self.model.accept("technical", "UKR"))
        self.assertTrue(self.model.offer("technical", "BLR", "POL"))
        self.assertTrue(self.model.accept("technical", "BLR"))
        self.assertEqual(self.model.active_recipient_idea_count("POL", "technical"), 1)
        expected = 1000 * (dip.CONTRACTS["technical"]["recipient"]["weekly_gdp_cost"]
                           + dip.CONTRACTS["technical"]["origin"]["weekly_gdp_cost"] * 0)
        self.assertAlmostEqual(self.model.weekly_expense("POL"), expected)

    def test_failure_suspends_both_sides_then_restores_without_repayment(self):
        self.model.offer("border", "UKR", "BLR")
        self.model.accept("border", "UKR")
        spent_ukr = self.countries["UKR"].treasury
        self.countries["UKR"].wars.add("BLR")
        self.assertEqual(self.model.active_recipient_idea_count("BLR", "border"), 0)
        self.assertEqual(self.model.weekly_expense("UKR"), 0)
        self.countries["UKR"].wars.clear()
        self.assertEqual(self.model.active_recipient_idea_count("BLR", "border"), 1)
        self.assertEqual(self.countries["UKR"].treasury, spent_ukr)
        self.countries["BLR"].sanctions.add(("UKR", "eco"))
        self.assertEqual(self.model.active_recipient_idea_count("BLR", "border"), 0)

    def test_either_side_can_terminate(self):
        self.model.offer("technical", "UKR", "POL")
        self.model.accept("technical", "UKR")
        self.assertTrue(self.model.terminate("technical", "UKR", actor="POL"))
        self.model.offer("technical", "BLR", "POL")
        self.model.accept("technical", "BLR")
        self.assertTrue(self.model.terminate("technical", "BLR", actor="BLR"))
        self.assertFalse(self.model.active)
        self.assertEqual(self.model.weekly_expense("POL"), 0)


if __name__ == "__main__":
    unittest.main()
