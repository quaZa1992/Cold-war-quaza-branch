# IMPERIA CW — Cold War: iraq 1970 — test audit rewards.
"""Focused source/data tests; writes no generated files and runs no compiler."""
from __future__ import annotations
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

import audit_rewards as audit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.append(str(ROOT / "tools/vietnam_1970"))
from script_ast import parse, first, values

FROZEN = HERE / "approved_iraq.json"
SHA = "82deef2b498d5e67d2b5dc157eda3ba534c2a8d35de215e7f7de679ffcc24eff"

class AuditRewardsTest(unittest.TestCase):
    def setUp(self):
        self.original = json.loads(FROZEN.read_text(encoding="utf-8-sig"))
        self.data = deepcopy(self.original)
        audit.apply(self.data)
        self.nodes = {n["key"]: n for n in self.data["nodes"]}
        self.old = {n["key"]: n for n in self.original["nodes"]}

    def test_frozen_input_and_idempotence(self):
        self.assertEqual(hashlib.sha256(FROZEN.read_bytes()).hexdigest(), SHA)
        before = deepcopy(self.data)
        self.assertIs(audit.apply(self.data), self.data)
        self.assertEqual(before, self.data)
        self.assertNotIn("audit_rewards_revision", self.original)

    def test_graph_and_starting_contracts_are_untouched(self):
        self.assertEqual(len(self.data["nodes"]), 426)
        for key in self.nodes:
            for field in ["id", "xy", "anchor", "offset", "prerequisites", "mutually_exclusive", "requires", "replaces", "group", "available", "active_condition"]:
                self.assertEqual(self.nodes[key][field], self.old[key][field], (key, field))
        for field in ["starting_spirits", "iran_war_ideas", "groups", "layout"]:
            self.assertEqual(self.data[field], self.original[field])

    def test_six_pairs_costs_and_own_one_building(self):
        for key, days, share, building in [
            ("industry_heavy", 49, .05, [557, "industrial_complex", 1]),
            ("industry_light", 49, .04, [166, "industrial_complex", 1]),
            ("oil_revenue_state", 49, .035, [171, "infrastructure", 1]),
            ("oil_diversification", 49, .04, [557, "industrial_complex", 1]),
        ]:
            n = self.nodes[key]
            self.assertEqual((n["days"], n["budget_gdp_share"], n["building"]), (days, share, building))
            self.assertEqual(len([c for c in n["audit_delivery_components"] if c["kind"] == "building"]), 1)
            source = audit.MERGED_SOURCES[n["id"]][0]
            component = next(c for c in n["audit_delivery_components"] if c["kind"] == "building")
            self.assertEqual(component["legacy_amounts"], {source: 1})
            self.assertEqual(len(n["audit_legacy_cost_credits"]), 1 if key == "oil_revenue_state" else 2)

    def test_conservative_military_values(self):
        expected = {
            "defence_professional": {"army_org_factor": .08, "army_personnel_cost_multiplier_modifier": .06},
            "defence_mass": {"conscription_factor": .15, "army_morale_factor": .08, "army_org_factor": -.03},
            "saddam_guard": {"army_org_factor": .03, "army_defence_factor": .04, "army_personnel_cost_multiplier_modifier": .10},
            "saddam_regular_army": {"army_morale_factor": .06, "training_time_army_factor": -.08, "army_personnel_cost_multiplier_modifier": .04},
            "defence_staff_training": {"training_time_army_factor": .04},
        }
        for key, modifiers in expected.items():
            self.assertEqual(self.nodes[key]["modifiers"], modifiers)
        self.assertEqual(self.nodes["defence_staff_training"]["army_xp"], 35)
        self.assertEqual(self.nodes["defence_professional"]["army_xp"], 25)
        self.assertEqual(self.nodes["defence_mass"]["army_xp"], 25)
        self.assertEqual(self.nodes["army_command_review"]["modifiers"], self.old["army_command_review"]["modifiers"])
        self.assertEqual(self.nodes["professional_command"]["modifiers"], self.old["professional_command"]["modifiers"])

    def test_real_compatible_route_totals(self):
        # Same military-contributing focuses as the 37/58-node prerequisite
        # closures independently recorded in the audit. No incompatible party.
        shared = ["army_command_review", "professional_command", "saddam_bounded_deterrence", "defence_professional", "defence_staff_training", "defence_land_schools"]
        routes = {
            "A": shared + ["saddam_guard", "saddam_guard_supply"],
            "B": shared + ["saddam_regular_army", "saddam_staff_college", "war_offensive_option", "war_economy", "iran_southern_command", "iran_sustained_war", "iran_mobilisation_base", "iran_war_of_reserves", "iran_no_easy_exit"],
        }
        keys = ["army_org_factor", "army_morale_factor", "training_time_army_factor", "army_personnel_cost_multiplier_modifier"]
        expected = {"A": [.16, .03, .04, .27], "B": [.21, .12, -.04, .68]}
        for route, names in routes.items():
            for i, modifier in enumerate(keys):
                actual = sum(self.nodes[k]["modifiers"].get(modifier, 0) for k in names)
                self.assertAlmostEqual(actual, expected[route][i])

    def test_partial_xp_and_literacy_credit(self):
        staff = self.nodes["defence_staff_training"]
        xp = next(c for c in staff["audit_delivery_components"] if c["kind"] == "army_xp")
        self.assertEqual(xp["amount"], 35)
        self.assertEqual(xp["legacy_amounts"], {audit.fid("defence_staff_training"): 15})
        lit = self.nodes["society_mass_literacy"]["audit_delivery_components"]
        self.assertEqual(len(lit), 1)
        self.assertEqual(lit[0]["kind"], "literacy")
        self.assertEqual(lit[0]["amount"], .06)
        self.assertEqual(lit[0]["legacy_amounts"], {audit.fid("society_mass_literacy"): .025})
        self.assertEqual(len(lit[0]["instant"]), 2)
        self.assertAlmostEqual(lit[0]["amount"] - next(iter(lit[0]["legacy_amounts"].values())), .035)

    def test_native_research_experience_doctrine_payloads(self):
        payloads = {
            "industry_heavy": [("CAT_industry", .35, 1)],
            "society_teacher_first": [("CAT_industry", .25, 1)],
            "industry_machine_tools": [("CAT_industry", .35, 2)],
            "society_technical_colleges": [("CAT_construction", .5, 1), ("CAT_industry", .25, 1)],
            "defence_air_maintenance": [("CAT_aircraft", .35, 1)],
            "defence_mixed_supply": [("CAT_aircraft", .35, 1)],
            "oil_technical_training": [("CAT_industry", .35, 1)],
            "oil_concession_delivery": [("CAT_industry", .25, 1)],
            "baath_future": [("CAT_industry", .25, 1)],
        }
        bonus_names = []
        for key, expected in payloads.items():
            tree = parse("\n".join(self.nodes[key]["instant"]))
            got = []
            for b in values(tree, "add_tech_bonus"):
                got.append((first(b, "category"), float(first(b, "bonus")), int(first(b, "uses"))))
                name = first(b, "name")
                self.assertIn(name, audit.BONUS_LOCALISATION)
                bonus_names.append(name)
                self.assertIsNone(first(b, "ahead_reduction"))
            self.assertEqual(got, expected, key)
        self.assertEqual(len(set(bonus_names)), len(bonus_names))
        air = parse("\n".join(self.nodes["defence_air_maintenance"]["instant"]))
        self.assertEqual(first(air, "air_experience"), "15")
        doctrine = values(parse("\n".join(self.nodes["defence_staff_training"]["instant"])), "add_doctrine_cost_reduction")[0]
        self.assertEqual(first(doctrine, "category"), "land_doctrine")
        self.assertEqual(float(first(doctrine, "cost_reduction")), .25)
        self.assertEqual(int(first(doctrine, "uses")), 1)

    def test_1970_technology_consumers_exist(self):
        # Fuel refining is not chosen: its first actual main-MD tech is1990.
        targets = {c: [] for c in ["CAT_industry", "CAT_construction", "CAT_aircraft"]}
        for path in (ROOT / "common/technologies").glob("*.txt"):
            tree = parse(path.read_text(encoding="utf-8-sig"))
            for container in values(tree, "technologies"):
                for key, op, body in container:
                    if not isinstance(body, list):
                        continue
                    year = first(body, "start_year")
                    if year is None or not 1960 <= float(year) <= 1975:
                        continue
                    cats = {v if k == "_bare" else k for k, op, v in first(body, "categories", [])}
                    for c in targets:
                        if c in cats:
                            targets[c].append(key)
        self.assertTrue(all(targets.values()), targets)

    def test_merged_and_review_unlocks_preserved(self):
        for key in ["industry_heavy", "industry_light"]:
            ids = [d["id"] for d in self.nodes[key]["decisions"]]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertIn(audit.fid("decision_industry_pipeline"), ids)
            self.assertIn(audit.fid("decision_industry_reallocate"), ids)
        self.assertIn(audit.fid("decision_society_revision"), [d["id"] for d in self.nodes["society_baseline"]["decisions"]])
        for source, target in audit.RETIRED.items():
            metadata = self.data["audit_retired_rewards"][source]
            self.assertEqual(metadata["target"], target)
            self.assertTrue(metadata["completion_is_not_delivery"])
            self.assertFalse(metadata["refund"])

    def test_new_administrative_and_agricultural_packages(self):
        self.assertEqual(self.nodes["industry_heavy"]["title"], "Basic Industries First")
        self.assertEqual(self.nodes["industry_light"]["title"], "Consumer Expansion")
        self.assertEqual(self.nodes["courts_budget"]["modifiers"], {"tax_gain_multiplier_modifier": .05, "bureaucracy_cost_multiplier_modifier": .02})
        self.assertEqual(self.nodes["courts_budget"]["budget_gdp_share"], .015)
        self.assertEqual(self.nodes["budget_accounts"]["modifiers"], {"tax_gain_multiplier_modifier": .04, "bureaucracy_cost_multiplier_modifier": -.03})
        self.assertEqual(self.nodes["budget_accounts"]["budget_gdp_share"], .005)
        coop = self.nodes["agri_cooperatives"]
        self.assertEqual(coop["days"], 49)
        self.assertEqual(coop["budget_gdp_share"], .04)
        self.assertEqual(coop["building"], [1141, "agriculture_district", 1])
        self.assertEqual(coop["modifiers"], {"agricolture_productivity_modifier": .12, "bureaucracy_cost_multiplier_modifier": .03})
        component = next(c for c in coop["audit_delivery_components"] if c["kind"] == "building")
        self.assertEqual(component["legacy_amounts"], {audit.fid("agri_wasit"): 1})
        self.assertEqual({x["source"] for x in coop["audit_legacy_cost_credits"]}, {audit.fid("agri_cooperative_credit"), audit.fid("agri_wasit")})
        small = self.nodes["agri_smallholders"]
        self.assertEqual(small["days"], 35)
        self.assertEqual(small["budget_gdp_share"], .025)
        self.assertEqual(small["modifiers"], {"agricolture_productivity_modifier": .08, "consumer_goods_factor": -.02, "social_cost_multiplier_modifier": .02})
        self.assertEqual(self.nodes["agri_dhiqar"], self.old["agri_dhiqar"])
        buildings = first(parse((ROOT / "common/buildings/00_buildings.txt").read_text(encoding="utf-8-sig")), "buildings")
        self.assertIsNotNone(first(buildings, "agriculture_district"))
        self.assertIsNotNone(first(buildings, "infrastructure"))

    def test_concession_gives_real_accepted_asset_without_double_fee(self):
        n = self.nodes["oil_concession_delivery"]
        self.assertEqual(n["building"], [171, "infrastructure", 1])
        self.assertEqual(n["requires"], ["Accepted revised oil concession"])
        self.assertEqual(n["budget_gdp_share"], 0)
        self.assertEqual(n["modifiers"], self.old["oil_concession_delivery"]["modifiers"])
        self.assertEqual(len(n["audit_delivery_components"]), 2)
        self.assertTrue(all(not c["legacy_amounts"] for c in n["audit_delivery_components"]))

    def test_procurement_priority_is_material_and_consent_does_not_transfer_equipment(self):
        standard = self.nodes["defence_soviet_standard"]
        mixed = self.nodes["defence_mixed_supply"]
        self.assertEqual(standard["modifiers"], {"supply_consumption_factor": -.10, "foreign_influence_modifier": -.03})
        self.assertEqual(mixed["modifiers"], {"supply_consumption_factor": .03})
        self.assertEqual(standard["budget_gdp_share"], .02)
        self.assertEqual(mixed["budget_gdp_share"], .02)
        self.assertEqual(len(mixed["audit_delivery_components"]), 1)
        self.assertEqual(mixed["audit_delivery_components"][0]["legacy_amounts"], {})
        self.assertFalse(any("send_equipment" in effect or "add_equipment" in effect for effect in mixed["instant"]))
        self.assertEqual(self.nodes["defence_soviet_offer"], self.old["defence_soviet_offer"])

    def test_readiness_matches_in_all_catalogue_owners(self):
        for collection in [self.data["decisions"]] + [n["decisions"] for n in self.data["nodes"]]:
            for d in collection:
                if d["id"] == audit.fid("decision_defence_readiness_cycle"):
                    self.assertEqual(d["budget_gdp_share"], .005)
                    self.assertEqual(d["days"], 90)
                    self.assertEqual(d["cooldown"], 180)
                    self.assertEqual(d["modifiers"], {"army_org_factor": .04, "army_morale_factor": .04, "army_personnel_cost_multiplier_modifier": .04})

    def test_finales_and_merged_industrial_values(self):
        self.assertEqual(self.nodes["state_compact"]["modifiers"], {"bureaucracy_cost_multiplier_modifier": -.06, "tax_gain_multiplier_modifier": .04})
        self.assertEqual(self.nodes["baath_future"]["modifiers"], {"political_power_factor": .03})
        self.assertEqual(self.nodes["bakr_succession_plan"]["days"], 21)
        self.assertEqual(self.nodes["bakr_succession_plan"]["modifiers"], {})
        self.assertEqual(self.nodes["industry_maintenance"]["modifiers"], {"production_factory_efficiency_gain_factor": .08, "production_factory_max_efficiency_factor": .02, "industrial_capacity_factory": -.01, "bureaucracy_cost_multiplier_modifier": .02})
        self.assertEqual(self.nodes["industry_maintenance"]["budget_gdp_share"], .02)
        generic = {"stability_factor": .03, "political_power_factor": -.02}
        for key in ["icp_socialist_republic", "aziz_party_renewal", "civic_mandate", "royal_settlement", "kdp_common_republic", "puk_federal_mandate", "dawa_government_review", "sciri_iraqi_mandate", "iip_government_mandate"]:
            self.assertNotEqual(self.nodes[key]["modifiers"], generic)
            self.assertIn(audit.fid(key), audit.DESCRIPTIONS)

    def test_every_component_receipt_is_unique_and_no_unrelated_payload_changes(self):
        seen = set()
        for n in self.data["nodes"]:
            for c in n.get("audit_delivery_components", []):
                self.assertNotIn(c["receipt"], seen)
                self.assertTrue(c["receipt"].startswith("COLDWAR_IRQ_"))
                seen.add(c["receipt"])
            if "audit_revision" not in n:
                self.assertEqual(n, self.old[n["key"]])

if __name__ == "__main__":
    unittest.main(verbosity=2)
