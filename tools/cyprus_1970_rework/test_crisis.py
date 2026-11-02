# IMPERIA COLD WAR — Cyprus 1970 crisis generator tests.
"""Compact static checks for the generated Cyprus crisis module."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from tools.cyprus_1970_rework.crisis import ACTORS, build


ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / "docs" / "cyprus_1970_rework_20261027" / "concept.json"


class CrisisGeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.design = json.loads(DESIGN.read_text(encoding="utf-8"))
        cls.result = build(cls.design)
        cls.files = cls.result["files"]

    def test_actor_api_and_project_markers(self) -> None:
        self.assertEqual(set(self.result["meta"]["actor_helpers"]), set(ACTORS))
        self.assertEqual(len(self.result["meta"]["actor_helpers"]), 16)
        for path, text in self.files.items():
            self.assertTrue(text.startswith("# IMPERIA COLD WAR"), path)
            self.assertFalse(text.encode("utf-8").startswith(b"\xef\xbb\xbf"), path)
            depth = 0
            for char in text:
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                    self.assertGreaterEqual(depth, 0, path)
            self.assertEqual(depth, 0, path)

    def test_every_focus_preview_is_an_unconditional_native_effect_tooltip(self) -> None:
        effects = self.files["common/scripted_effects/COLDWAR_CYP_R2_crisis.txt"]
        for key in ACTORS:
            match = re.search(
                rf"COLDWAR_CYP_R2_ACT_{re.escape(key)}_preview = \{{(.*?)\n\}}",
                effects,
                re.S,
            )
            self.assertIsNotNone(match, key)
            body = match.group(1)
            self.assertIn("effect_tooltip = {", body, key)
            self.assertNotIn("_available =", body, key)
            self.assertNotIn("_apply =", body, key)
            self.assertNotIn(f"COLDWAR_CYP_R2_ACT_{key}_preview_tt", body, key)

    def test_consultation_expiry_does_not_create_a_crisis(self) -> None:
        events = self.files["events/COLDWAR_CYP_R2_crisis.txt"]
        deadline = events.split("id = COLDWAR_CYP_R2_CRISIS.10", 1)[1].split("id = COLDWAR_CYP_R2_CRISIS.21", 1)[0]
        self.assertIn("clr_country_flag = COLDWAR_CYP_R2_consultation_open", deadline)
        self.assertNotIn("remove_country_flag = COLDWAR_CYP_R2_consultation_open", deadline)
        self.assertIn("has_country_flag = COLDWAR_CYP_R2_crisis_active", deadline)
        self.assertNotIn("set_country_flag = COLDWAR_CYP_R2_crisis_active", deadline)
        self.assertIn("COLDWAR_CYP_R2_start_army_crisis = yes", deadline)

    def test_coup_uses_disclosed_base_plus_preparedness_and_ties_defend(self) -> None:
        effects = self.files["common/scripted_effects/COLDWAR_CYP_R2_crisis.txt"]
        events = self.files["events/COLDWAR_CYP_R2_crisis.txt"]
        self.assertIn("set_variable = { COLDWAR_CYP_R2_coup_defense = 40 }", effects)
        self.assertIn("add_to_variable = { COLDWAR_CYP_R2_coup_defense = COLDWAR_CYP_R2_presidential_preparedness }", effects)
        self.assertIn("COLDWAR_CYP_R2_officer_penetration > COLDWAR_CYP_R2_coup_defense", events)

    def test_mediation_has_distinct_response_and_deadline_events(self) -> None:
        effects = self.files["common/scripted_effects/COLDWAR_CYP_R2_crisis.txt"]
        events = self.files["events/COLDWAR_CYP_R2_crisis.txt"]
        self.assertIn("country_event = { id = COLDWAR_CYP_R2_CRISIS.32 hours = 1 }", effects)
        self.assertIn("country_event = { id = COLDWAR_CYP_R2_CRISIS.33 days = 14 }", effects)
        self.assertIn("id = COLDWAR_CYP_R2_CRISIS.33", events)
        definitions = re.findall(r"(?m)^\s*id = COLDWAR_CYP_R2_CRISIS\.(\d+)\s*$", events)
        self.assertEqual(len(definitions), len(set(definitions)))
        self.assertEqual(len(definitions), events.count("picture = GFX_COLDWAR_CYP_R2_agreement"))

    def test_four_turkish_actions_have_real_native_effects(self) -> None:
        decisions = self.files["common/decisions/COLDWAR_CYP_R2_crisis.txt"]
        self.assertEqual(decisions.count("\tCOLDWAR_CYP_R2_army_"), 4)
        self.assertNotIn("custom_effect_tooltip = COLDWAR_CYP_R2_crisis_ability", decisions)
        self.assertIn("COLDWAR_CYP_R2_budget_turkish_025", decisions)
        self.assertIn("add_to_variable = { COLDWAR_CYP_R2_military_pressure = -25 tooltip = COLDWAR_CYP_R2_military_pressure_tt }", decisions)
        self.assertIn("declare_war_on = { target = CYP type = annex_everything }", decisions)

    def test_nato_return_is_member_specific_and_has_a_live_leader_guard(self) -> None:
        triggers = self.files["common/scripted_triggers/COLDWAR_CYP_R2_crisis.txt"]
        return_trigger = triggers.split("COLDWAR_CYP_R2_nato_return_allowed = {", 1)[1]
        self.assertIn("NATO_currently_exists = yes", return_trigger)
        self.assertIn("has_idea = NATO_member", return_trigger)
        self.assertIn("is_faction_leader = yes", return_trigger)
        self.assertIn("NOT = { is_in_faction = yes }", return_trigger)
        self.assertIn("COLDWAR_CYP_R2_nato_was_member", self.files["common/scripted_effects/COLDWAR_CYP_R2_crisis.txt"])

    def test_reconcile_can_run_after_cyprus_is_eliminated(self) -> None:
        effects = self.files["common/scripted_effects/COLDWAR_CYP_R2_crisis.txt"]
        reconcile = effects.split("COLDWAR_CYP_R2_crisis_reconcile = {", 1)[1].split("\n}", 1)[0]
        self.assertNotIn("original_tag = CYP", reconcile)
        self.assertIn("NOT = { country_exists = CYP }", reconcile)
        self.assertIn("GRE = { COLDWAR_CYP_R2_try_nato_return = yes }", reconcile)
        triggers = self.files["common/scripted_triggers/COLDWAR_CYP_R2_crisis.txt"]
        self.assertIn("NOT = { country_exists = CYP }", triggers.split("COLDWAR_CYP_R2_nato_join_allowed = {", 1)[1])

    def test_turkish_coup_uses_native_party_slot_and_leader_dispatcher(self) -> None:
        events = self.files["events/COLDWAR_CYP_R2_crisis.txt"]
        self.assertIn("set_variable = { ruling_party = 22 }", events)
        self.assertIn("set_politics = { ruling_party = nationalist elections_allowed = no }", events)
        self.assertIn("COLDWAR_TUR_1970_set_leader = yes", events)
        self.assertNotIn("set_politics = { ruling_party = 22", events)

    def test_paid_focus_and_decision_transactions_refresh_current_gdp_prices(self) -> None:
        effects = self.files["common/scripted_effects/COLDWAR_CYP_R2_crisis.txt"]
        turkey_focus = effects.split("COLDWAR_CYP_R2_ACT_tur_operation_apply = {", 1)[1].split("\n}", 1)[0]
        self.assertLess(turkey_focus.index("set_variable = { COLDWAR_CYP_R2_budget_intervention_050"),
                        turkey_focus.index("COLDWAR_CYP_R2_ACT_tur_operation_available = yes"))
        decisions = self.files["common/decisions/COLDWAR_CYP_R2_crisis.txt"]
        intervene = decisions.split("COLDWAR_CYP_R2_army_intervene = {", 1)[1]
        intervene = intervene.split("complete_effect = {", 1)[1]
        self.assertLess(intervene.index("set_variable = { COLDWAR_CYP_R2_budget_intervention_050"),
                        intervene.index("check_variable = { treasury >= COLDWAR_CYP_R2_budget_intervention_050"))

    def test_weekly_stream_has_only_cached_flags_and_monthly_reconcile(self) -> None:
        effects = self.files["common/scripted_effects/COLDWAR_CYP_R2_crisis.txt"]
        weekly = effects.split("COLDWAR_CYP_R2_crisis_weekly_streams = {", 1)[1].split("\n}", 1)[0]
        self.assertNotIn("has_war", weekly)
        self.assertNotIn("has_idea", weekly)
        self.assertIn("has_country_flag = COLDWAR_CYP_R2_intervention_expense_cached", weekly)
        self.assertIn("has_country_flag = COLDWAR_CYP_R2_volunteer_expense_active", weekly)
        monthly = effects.split("COLDWAR_CYP_R2_crisis_monthly = {", 1)[1].split("\n}", 1)[0]
        self.assertIn("COLDWAR_CYP_R2_crisis_reconcile = yes", monthly)
        self.assertNotRegex(weekly, r"0\.\d{6,}")

    def test_native_flag_math_and_country_iteration_syntax(self) -> None:
        effects = self.files["common/scripted_effects/COLDWAR_CYP_R2_crisis.txt"]
        triggers = self.files["common/scripted_triggers/COLDWAR_CYP_R2_crisis.txt"]
        decisions = self.files["common/decisions/COLDWAR_CYP_R2_crisis.txt"]
        self.assertNotIn("remove_country_flag =", effects)
        self.assertNotIn("remove_country_flag =", self.files["events/COLDWAR_CYP_R2_crisis.txt"])
        self.assertNotRegex(effects + triggers, r"any_country\s*=\s*\{\s*limit\s*=")
        self.assertNotRegex(effects + decisions, r"\{\s*value\s*=\s*[^{}]+\s+multiply\s*=")
        self.assertIn("multiply_temp_variable = { treasury_change = -0.005 }", effects)

    def test_volunteer_mission_uses_native_permission_and_targeted_lifecycle(self) -> None:
        ideas = self.files["common/ideas/COLDWAR_CYP_R2_crisis_ideas.txt"]
        idea = ideas.split("COLDWAR_CYP_R2_cyprus_volunteer_mission = {", 1)[1]
        self.assertIn("rule = { can_send_volunteers = yes }", idea)
        self.assertIn("add_relation_rule_override = { target = CYP can_send_volunteers = yes }", idea)
        self.assertIn("remove_relation_rule_override = { target = CYP can_send_volunteers = yes }", idea)
        effects = self.files["common/scripted_effects/COLDWAR_CYP_R2_crisis.txt"]
        self.assertNotRegex(effects, r"\b(?:create_unit|create_division|add_units)\s*=")


if __name__ == "__main__":
    unittest.main()
