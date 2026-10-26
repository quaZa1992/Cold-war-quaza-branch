# IMPERIA CW — Cold War: Syria 1970 content imported from quaZa.
"""Scenario regression checks against emitted Syrian foreign scripts.

The small interpreter models the documented treasury/war-goal interface only;
it does not substitute for HOI4's diplomatic or economic simulation.
"""
from pathlib import Path
import unittest
from validate_content import parse, first, vals, walk
from test_lifecycle import Country

ROOT = Path(__file__).resolve().parents[2]
P = "COLDWAR_SYR_"


class Scenario(Country):
    def __init__(self, bodies):
        super().__init__(bodies)
        self.variables.update(gdp_total=2.14, treasury=1, debt=.7, political_power=100)
        self.israel_exists = True
        self.israel_owns_golan = False
        self.israel_controls_golan = True
        self.same_faction = False
        self.at_war = False
        self.goals = []

    def condition(self, body):
        results = []
        for key, op, value in body:
            if key == "country_exists":
                results.append(self.israel_exists if value == "ISR" else False)
            elif key == "is_in_faction_with":
                results.append(self.same_faction)
            elif key == "has_war_with":
                results.append(self.at_war)
            elif key == "has_wargoal_against":
                results.append(bool(self.goals))
            elif key == "controls_state" and value == "587":
                results.append(not self.israel_controls_golan)
            elif key == "ISR":
                results.append(all(self.israel_controls_golan if k == "controls_state" else self.israel_owns_golan for k, _, _ in value))
            elif key in ("AND", "OR", "NOT"):
                children = [self.condition([clause]) for clause in value]
                results.append(all(children) if key == "AND" else any(children) if key == "OR" else not all(children))
            elif key in self.bodies and value == "yes":
                results.append(self.condition(self.bodies[key]))
            elif key == "check_variable" and first(value, "var"):
                a = self.number(first(value, "var"))
                b = self.number(first(value, "value"))
                results.append(a >= b if first(value, "compare") == "greater_than_or_equals" else a == b)
            else:
                results.append(super().condition([(key, op, value)]))
        return all(results)

    def execute(self, body):
        branch = None
        for key, op, value in body:
            if key == "if":
                branch = self.condition(first(value, "limit", []))
                if branch:
                    self.execute([clause for clause in value if clause[0] != "limit"])
            elif key == "else":
                if not branch:
                    self.execute(value)
            elif key == "set_temp_variable" and first(value, "wargoal_on"):
                self.temp["wargoal_on"] = "ISR"
            elif key == "set_temp_variable" and first(value, "wargoal_by"):
                self.temp["wargoal_by"] = "SYR"
            elif key in ("multiply_variable", "multiply_temp_variable"):
                target = self.temp if key == "multiply_temp_variable" else self.variables
                variable, _, amount = value[0]
                target[variable] *= self.number(amount)
            elif key == "create_wargoal":
                self.goals.append(dict((k, v) for k, _, v in value))
            elif key == "add_political_power":
                self.variables["political_power"] += float(value)
            elif key in ("add_threat_from_wargoal_effect", "update_money_dirty_variable"):
                pass
            elif key == "remove_ideas":
                self.ideas.discard(value)
            elif key == "add_timed_idea":
                self.ideas.add(first(value, "idea"))
            elif key == "country_event":
                pass
            else:
                super().execute([(key, op, value)])


class ForeignScenarios(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bodies = {}
        for directory in ("common/scripted_effects", "common/scripted_triggers"):
            path = ROOT / directory / ("COLDWAR_SYR_foreign_effects.txt" if "effects" in directory else "COLDWAR_SYR_foreign_triggers.txt")
            cls.bodies.update({k: v for k, _, v in parse(path.read_text(encoding="utf-8-sig"))})
        parsed = parse((ROOT / "common/decisions/COLDWAR_SYR_foreign_decisions.txt").read_text(encoding="utf-8"))
        cls.decisions = dict((k, v) for k, _, v in first(parsed, P + "foreign_dossier"))
        ideas = parse((ROOT / "common/ideas/COLDWAR_SYR_foreign_ideas.txt").read_text(encoding="utf-8"))
        cls.ideas = dict((k, v) for k, _, v in first(first(ideas, "ideas"), "country"))
        events = parse((ROOT / "events/COLDWAR_SYR_foreign_events.txt").read_text(encoding="utf-8"))
        cls.events = {first(value, "id"): value for key, _, value in events if key == "country_event"}

    def test_occupied_syrian_land_uses_real_fallback_goal(self):
        c = Scenario(self.bodies)
        c.execute(self.bodies[P + "create_limited_wargoal"])
        self.assertEqual(c.goals[0]["type"], "annex_everything")
        self.assertEqual(c.goals[0]["expire"], "365")
        c.execute(self.bodies[P + "create_limited_wargoal"])
        self.assertEqual(len(c.goals), 1)

    def test_israeli_owned_land_uses_golan_state_goal(self):
        c = Scenario(self.bodies)
        c.israel_owns_golan = True
        c.execute(self.bodies[P + "create_limited_wargoal"])
        self.assertEqual(c.goals[0]["type"], "take_state_focus")
        self.assertTrue(c.goals[0]["generator"])

    def test_no_goal_during_war_after_recovery_or_for_an_ally(self):
        for change in ("at_war", "same_faction", "recovered", "israel_gone"):
            c = Scenario(self.bodies)
            if change == "recovered":
                c.israel_controls_golan = False
            elif change == "israel_gone":
                c.israel_exists = False
            else:
                setattr(c, change, True)
            c.execute(self.bodies[P + "create_limited_wargoal"])
            self.assertEqual(c.goals, [], change)

    def test_current_gdp_funding_and_exact_balance(self):
        c = Scenario(self.bodies)
        c.at_war = True
        c.flags.add(P + "limited_war_entry_implemented")
        c.execute(self.bodies[P + "update_operation_costs"])
        self.assertAlmostEqual(c.variables[P + "cost_three_quarter_percent_gdp"], .01605)
        c.variables["treasury"] = c.variables[P + "cost_three_quarter_percent_gdp"]
        c.execute(first(self.decisions[P + "decision_war_appropriation"], "remove_effect"))
        self.assertAlmostEqual(c.variables["treasury"], 0)
        self.assertIn(P + "operations_funded", c.flags)
        c.execute(first(self.decisions[P + "decision_war_appropriation"], "remove_effect"))
        self.assertAlmostEqual(c.variables["treasury"], 0)

    def test_appropriation_can_start_and_finish_with_a_negative_treasury(self):
        decision = self.decisions[P + "decision_war_appropriation"]
        for balance in (0, -.2):
            with self.subTest(balance=balance):
                c = Scenario(self.bodies)
                c.at_war = True
                c.flags.add(P + "limited_war_entry_implemented")
                c.execute(self.bodies[P + "update_operation_costs"])
                c.variables["treasury"] = balance
                self.assertTrue(c.condition(first(decision, "available")))
                # Expenditure elsewhere during preparations cannot cancel this payment.
                c.variables["treasury"] -= .1
                c.execute(first(decision, "remove_effect"))
                self.assertIn(P + "operations_funded", c.flags)
                self.assertIn(P + "decision_war_appropriation_completed", c.flags)
                self.assertAlmostEqual(c.variables["treasury"], balance - .1 - .01605)
                self.assertAlmostEqual(c.variables["debt"], .7)
                self.assertEqual(c.variables["political_power"], 100)
                paid_balance = c.variables["treasury"]
                c.execute(first(decision, "remove_effect"))
                self.assertAlmostEqual(c.variables["treasury"], paid_balance)

    def test_invalid_gdp_cancels_preparations_without_a_free_or_negative_cost(self):
        decision = self.decisions[P + "decision_war_appropriation"]
        for gdp in (0, -1):
            with self.subTest(gdp=gdp):
                c = Scenario(self.bodies)
                c.at_war = True
                c.flags.add(P + "limited_war_entry_implemented")
                c.variables.update(gdp_total=gdp, treasury=-.2)
                c.execute(first(decision, "remove_effect"))
                self.assertNotIn(P + "operations_funded", c.flags)
                self.assertNotIn(P + "decision_war_appropriation_completed", c.flags)
                self.assertAlmostEqual(c.variables["treasury"], -.2)
                self.assertEqual(c.variables["political_power"], 145)

    def test_syrian_decisions_and_training_request_have_no_cash_minimum(self):
        for name, decision in self.decisions.items():
            for field in ("available", "remove_effect"):
                for key, _, value in walk(first(decision, field, [])):
                    if key == "check_variable":
                        variable = first(value, "var", value[0][0])
                        self.assertNotEqual(variable, "treasury", (name, field))
        for key, _, value in walk(self.bodies[P + "training_can_request"]):
            if key == "check_variable":
                self.assertNotEqual(first(value, "var", value[0][0]), "treasury")
        for event_id in ("COLDWAR_SYR_WAR.5", "COLDWAR_SYR_WAR.13", "COLDWAR_SYR_FOREIGN.9"):
            for key, _, value in walk(self.events[event_id]):
                if key == "check_variable":
                    self.assertNotEqual(first(value, "var", value[0][0]), "treasury", event_id)

    def test_accepted_egyptian_operational_plan_charges_a_negative_treasury_once(self):
        event = self.events["COLDWAR_SYR_WAR.5"]
        option = next(option for option in vals(event, "option")
                      if any(key == "add_timed_idea" for key, _, _ in walk(first(option, "hidden_effect", []))))
        c = Scenario(self.bodies)
        c.at_war = True
        c.flags.update({P + "operational_mandate", P + "egypt_offer_pending", P + "egypt_offer_accepted"})
        c.variables["treasury"] = -.2
        c.execute(first(event, "immediate"))
        self.assertTrue(c.condition(first(option, "trigger")))
        c.execute(first(option, "hidden_effect"))
        self.assertIn(P + "war_joint_planning", c.ideas)
        self.assertAlmostEqual(c.variables["treasury"], -.20535)
        self.assertNotIn(P + "egypt_offer_pending", c.flags)
        self.assertAlmostEqual(c.variables["debt"], .7)
        c.execute(first(option, "hidden_effect"))
        self.assertAlmostEqual(c.variables["treasury"], -.20535)

    def test_accepted_peacetime_staff_plan_charges_syria_after_consent(self):
        event = self.events["COLDWAR_SYR_FOREIGN.9"]
        option = next(option for option in vals(event, "option")
                      if any(key == "add_timed_idea" for key, _, _ in walk(first(option, "hidden_effect", []))))
        execution = first(first(option, "hidden_effect"), "if")
        syrian_execution = first(execution, "FROM")
        c = Scenario(self.bodies)
        c.variables["treasury"] = -.2
        c.flags.add(P + "joint_plan_pending")
        c.execute(syrian_execution)
        self.assertIn(P + "peacetime_joint_planning", c.ideas)
        self.assertAlmostEqual(c.variables["treasury"], -.20535)
        self.assertNotIn(P + "joint_plan_pending", c.flags)
        self.assertAlmostEqual(c.variables["debt"], .7)
        c.execute(syrian_execution)
        self.assertAlmostEqual(c.variables["treasury"], -.20535)

    def test_counterparty_loan_grant_pipeline_and_supply_funding_remains_required(self):
        for event_id in ("COLDWAR_SYR_FOREIGN.1", "COLDWAR_SYR_FOREIGN.21",
                         "COLDWAR_SYR_FOREIGN.3", "COLDWAR_SYR_FOREIGN.8"):
            with self.subTest(event_id=event_id):
                conditions = [first(option, "trigger", []) for option in vals(self.events[event_id], "option")]
                self.assertTrue(any(key == "check_variable" and
                                    first(value, "var", value[0][0]) == "treasury"
                                    for condition in conditions for key, _, value in walk(condition)))

    def test_cleanup_preserves_unused_appropriation_and_public_debt(self):
        cleanup_if = vals(self.bodies[P + "foreign_weekly"], "if")[0]
        c = Scenario(self.bodies)
        c.flags.add(P + "operations_funded")
        c.execute([("if", "=", cleanup_if)])
        self.assertIn(P + "operations_funded", c.flags)
        c.flags.add(P + "operational_mandate")
        c.ideas.update({P + "war_reserve_readiness", P + "war_bridge_credit"})
        c.israel_controls_golan = False
        c.execute([("if", "=", cleanup_if)])
        self.assertNotIn(P + "war_reserve_readiness", c.ideas)
        self.assertIn(P + "war_bridge_credit", c.ideas)
        self.assertEqual(c.variables["debt"], .7)

    def test_timed_operational_idea_cancels_for_either_invalid_condition(self):
        cancel = first(self.ideas[P + "war_reserve_readiness"], "cancel")
        c = Scenario(self.bodies)
        c.at_war = True
        self.assertTrue(c.condition(cancel))
        c.flags.add(P + "operational_mandate")
        self.assertFalse(c.condition(cancel))
        c.israel_controls_golan = False
        self.assertTrue(c.condition(cancel))


if __name__ == "__main__":
    unittest.main()
