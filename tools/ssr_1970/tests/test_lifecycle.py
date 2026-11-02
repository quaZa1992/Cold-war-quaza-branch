# IMPERIA COLD WAR — Persistent SSR lifecycle contract tests.
"""Static and arithmetic regressions for generated SSR lifecycle behavior."""

import json
import math
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "tools" / "ssr_1970"
sys.path.insert(0, str(SRC))
import lifecycle
import shared


IDEAS_PATH = ROOT / "common/ideas/COLDWAR_SSR_lifecycle_ideas.txt"
EFFECTS_PATH = ROOT / "common/scripted_effects/COLDWAR_SSR_lifecycle_effects.txt"
TRIGGERS_PATH = ROOT / "common/scripted_triggers/COLDWAR_SSR_lifecycle_triggers.txt"
ON_ACTIONS_PATH = ROOT / "common/on_actions/COLDWAR_SSR_lifecycle_on_actions.txt"
LOC_PATH = ROOT / "localisation/english/COLDWAR_SSR_lifecycle_l_english.yml"


def _read(path):
    return path.read_text(encoding="utf-8-sig")


def _named_block(text, name):
    """Return a brace-balanced script block by its top-level identifier."""
    match = re.search(rf"(?m)^{re.escape(name)}\s*=\s*\{{", text)
    if not match:
        raise AssertionError(f"Missing script block {name}")
    opening = text.find("{", match.start())
    depth = 0
    for index in range(opening, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[match.start():index + 1]
    raise AssertionError(f"Unclosed script block {name}")


def _idea_blocks(text):
    """Parse top-level idea entries under the emitted country idea container."""
    lines = text.splitlines()
    parsed = {}
    index = 0
    while index < len(lines):
        match = re.fullmatch(r"\t\t([A-Za-z0-9_]+)\s*=\s*\{", lines[index])
        if not match:
            index += 1
            continue
        name = match.group(1)
        start = index + 1
        depth = 1
        index += 1
        while index < len(lines) and depth:
            depth += lines[index].count("{") - lines[index].count("}")
            index += 1
        if depth:
            raise AssertionError(f"Unclosed idea {name}")
        parsed[name] = "\n".join(lines[start:index - 1])
    return parsed


def _section_body(body, section, indent):
    opener = "\t" * indent + section + " = {"
    lines = body.splitlines()
    try:
        start = lines.index(opener) + 1
    except ValueError:
        return None
    close = "\t" * indent + "}"
    try:
        end = lines.index(close, start)
    except ValueError as exc:
        raise AssertionError(f"Unclosed {section} block") from exc
    return lines[start:end]


def _modifier_map(body):
    lines = _section_body(body, "modifier", 3)
    if lines is None:
        return {}
    result = {}
    for line in lines:
        match = re.fullmatch(r"\t{3}([A-Za-z0-9_]+)\s*=\s*(-?[0-9]+(?:\.[0-9]+)?)", line)
        if match:
            result[match.group(1)] = float(match.group(2))
    return result


def _equipment_map(body):
    lines = _section_body(body, "equipment_bonus", 3)
    if lines is None:
        return {}
    result = {}
    index = 0
    while index < len(lines):
        target = re.fullmatch(r"\t{4}([A-Za-z0-9_]+)\s*=\s*\{", lines[index])
        if not target:
            index += 1
            continue
        target_name = target.group(1)
        index += 1
        values = {}
        while index < len(lines) and lines[index] != "\t\t\t\t}":
            entry = re.fullmatch(r"\t{5}([A-Za-z0-9_]+)\s*=\s*([-A-Za-z0-9.]+)", lines[index])
            if entry and entry.group(1) != "instant":
                values[entry.group(1)] = float(entry.group(2))
            elif entry and entry.group(1) == "instant":
                values[entry.group(1)] = entry.group(2)
            index += 1
        if index == len(lines):
            raise AssertionError(f"Unclosed equipment target {target_name}")
        result[target_name] = values
        index += 1
    return result


def _loc_map(text):
    result = {}
    for line in text.splitlines():
        match = re.match(r'^\s*([A-Za-z0-9_]+):0\s+(".*")\s*$', line)
        if match:
            result[match.group(1)] = json.loads(match.group(2))
    return result


def _assert_map_almost_equal(test, actual, expected, places=5):
    test.assertEqual(set(actual), set(expected))
    for key, value in expected.items():
        test.assertAlmostEqual(actual[key], value, places=places, msg=key)


class LifecycleContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = shared.data()
        cls.models = shared.models()
        cls.nodes = shared.nodes()
        cls.ideas_text = _read(IDEAS_PATH)
        cls.effects_text = _read(EFFECTS_PATH)
        cls.triggers_text = _read(TRIGGERS_PATH)
        cls.on_actions_text = _read(ON_ACTIONS_PATH)
        cls.loc = _loc_map(_read(LOC_PATH))
        cls.idea_blocks = _idea_blocks(cls.ideas_text)

    def test_participant_identity_is_country_scoped_and_admission_is_explicit(self):
        participant = _named_block(self.triggers_text, "COLDWAR_SSR_is_participant")
        self.assertIn("has_country_flag = COLDWAR_SSR_lifecycle_accepted_admission", participant)
        for tag in shared.TAGS:
            self.assertIn(
                f"AND = {{ original_tag = {tag} has_country_flag = COLDWAR_SSR_lifecycle_scenario_identity }}",
                participant,
            )
        self.assertNotRegex(participant, r"(?m)^\s*(?:UKR|BLR|MLV|EST|LAT|LIT|GEO|ARM|AZE|KAZ|UZB|TRK|KYR|TAJ)\s*=\s*\{")
        self.assertIn("COLDWAR_SSR_is_participant = yes", _named_block(self.triggers_text, "COLDWAR_SSR_is_independent"))

    def test_replacement_receipts_are_static_reforms_not_double_counted_in_groups(self):
        groups = _named_block(self.effects_text, "COLDWAR_SSR_lifecycle_rebuild_groups")
        for node in self.nodes:
            if node.get("replace"):
                self.assertNotIn(f"has_country_flag = {node['receipt']}", groups, node["key"])
        regional = [n for n in self.nodes if n["group"] == "regional" and not n.get("replace") and not n.get("specialisation")]
        self.assertTrue(regional)
        for node in regional:
            if node["modifiers"]:
                self.assertIn(f"has_country_flag = {node['receipt']}", groups, node["key"])

    def test_starting_replacement_priority_and_persistent_plan_standards(self):
        for tag in shared.TAGS:
            start = _named_block(self.effects_text, f"COLDWAR_SSR_lifecycle_starting_{tag}")
            self.assertIn("has_country_flag = COLDWAR_SSR_plan_settlement_rewarded", start)
            self.assertIn(f"add_ideas = COLDWAR_SSR_lifecycle_{tag}_plan_republican", start)
            self.assertIn("else_if = { limit = { has_country_flag = COLDWAR_SSR_industrial_conversion_rewarded } }", start)
            self.assertIn("has_country_flag = COLDWAR_SSR_enterprise_accounts_rewarded", start)
            self.assertIn("has_country_flag = COLDWAR_SSR_audit_staff_rewarded", start)
            self.assertIn("add_ideas = COLDWAR_SSR_lifecycle_" + tag + "_professional", start)
            self.assertIn("has_country_flag = COLDWAR_SSR_discipline_campaign_rewarded", start)
            self.assertIn("NOT = { OR = { has_country_flag = COLDWAR_SSR_court_review_rewarded has_country_flag = COLDWAR_SSR_executive_service_rewarded } }", start)
            self.assertIn("has_country_flag = COLDWAR_SSR_service_settlement_rewarded", start)

    def test_specialisation_ideas_match_every_reachable_receipt_state(self):
        catalog = lifecycle.specialisation_catalog(self.models)
        self.assertEqual(set(catalog), {"aircraft", "armour", "artillery", "army", "navy", "agriculture", "industry", "resources", "electronics"})
        self.assertEqual(sum(len(states) for states in catalog.values()), 162)
        expected_ids = set()
        for role, states in catalog.items():
            self.assertEqual(len(states), 18, role)
            root = next(n for n in self.models["UKR"]["nodes"] if n.get("specialisation") == role and n["key"].endswith("_mandate"))
            for variant in states:
                for kind in ("full", "legacy"):
                    idea_id = variant[f"{kind}_idea"]
                    expected_ids.add(idea_id)
                    self.assertIn(idea_id, self.idea_blocks)
                    self.assertEqual(self.loc[idea_id], variant[f"{kind}_name"])
                    self.assertEqual(variant[f"{kind}_name"], root["spirit"] if kind == "full" else root["legacy_spirit"])
                    block = self.idea_blocks[idea_id]
                    _assert_map_almost_equal(self, _modifier_map(block), variant[f"{kind}_modifiers"])
                    parsed_gear = _equipment_map(block)
                    expected_gear = variant[f"{kind}_equipment"]
                    self.assertEqual(set(parsed_gear), set(expected_gear), idea_id)
                    for target, values in expected_gear.items():
                        self.assertEqual(set(parsed_gear[target]), set(values) | {"instant"}, (idea_id, target))
                        self.assertEqual(parsed_gear[target]["instant"], "yes", (idea_id, target))
                        _assert_map_almost_equal(self, {k: v for k, v in parsed_gear[target].items() if k != "instant"}, values)
        self.assertEqual(len(expected_ids), 324)

    def test_specialisation_rebuild_swaps_full_and_legacy_without_reissuing_assets(self):
        rebuild = _named_block(self.effects_text, "COLDWAR_SSR_lifecycle_rebuild_specialisation")
        self.assertNotIn("add_equipment_to_stockpile", rebuild)
        self.assertNotIn("add_equipment_bonus", rebuild)
        self.assertNotIn("treasury_change", rebuild)
        for role, states in lifecycle.specialisation_catalog(self.models).items():
            root_receipt = f"COLDWAR_SSR_special_{role}_mandate"
            spec_nodes = [n for n in self.models["UKR"]["nodes"] if n.get("specialisation") == role]
            all_node_ids = {n["id"] for n in spec_nodes}
            for state in states:
                if root_receipt not in state["receipts"]:
                    continue
                full_id = state["full_idea"]
                legacy_id = state["legacy_idea"]
                positive = sorted(state["receipts"])
                negative = sorted(all_node_ids - set(positive))
                exact_state = " ".join(f"has_country_flag = {receipt}_rewarded" for receipt in positive)
                if exact_state:
                    exact_state += " "
                exact_state += " ".join(f"NOT = {{ has_country_flag = {node_id}_rewarded }}" for node_id in negative)
                exact_gate = f"AND = {{ {exact_state} }}"
                self.assertIn(f"COLDWAR_SSR_is_ssr = yes has_country_flag = COLDWAR_SSR_special_{role}_mandate_rewarded", rebuild)
                self.assertIn(f"NOT = {{ has_idea = {full_id} }}", rebuild)
                self.assertIn(f"COLDWAR_SSR_is_independent = yes has_country_flag = COLDWAR_SSR_special_{role}_mandate_rewarded", rebuild)
                self.assertIn(f"NOT = {{ has_idea = {legacy_id} }}", rebuild)
                full_branch = f"COLDWAR_SSR_is_ssr = yes has_country_flag = COLDWAR_SSR_special_{role}_mandate_rewarded {exact_gate} NOT = {{ has_idea = {full_id} }}"
                legacy_branch = f"COLDWAR_SSR_is_independent = yes has_country_flag = COLDWAR_SSR_special_{role}_mandate_rewarded {exact_gate} NOT = {{ has_idea = {legacy_id} }}"
                self.assertIn(full_branch, rebuild, f"full state gate {role}/{state['index']}")
                self.assertIn(legacy_branch, rebuild, f"legacy state gate {role}/{state['index']}")
                for branch, selected_id in ((full_branch, full_id), (legacy_branch, legacy_id)):
                    start = rebuild.index(branch)
                    branch_start = rebuild.rfind("\tif = { limit = {", 0, start)
                    self.assertGreaterEqual(branch_start, 0)
                    depth = 0
                    branch_end = None
                    for pos in range(rebuild.index("{", branch_start), len(rebuild)):
                        if rebuild[pos] == "{":
                            depth += 1
                        elif rebuild[pos] == "}":
                            depth -= 1
                            if depth == 0:
                                branch_end = pos + 1
                                break
                    self.assertIsNotNone(branch_end)
                    branch_text = rebuild[branch_start:branch_end]
                    for variant in states:
                        self.assertIn(f"remove_ideas = {variant['full_idea']}", branch_text)
                        self.assertIn(f"remove_ideas = {variant['legacy_idea']}", branch_text)
                    self.assertEqual(branch_text.count("\n\t\tadd_ideas = "), 1)
                    self.assertIn(f"add_ideas = {selected_id}", branch_text)

    def test_agriculture_workforce_benefits_retain_twenty_percent(self):
        workforce = {"agriculture_district_worker_requirement_modifier", "agriculture_workers_modifier"}
        nodes = [n for m in self.models.values() for n in m["nodes"] if n.get("specialisation") == "agriculture"]
        amended = 0
        for node in nodes:
            for key in workforce & set(node["modifiers"]):
                amended += 1
                self.assertLess(node["modifiers"][key], 0)
                self.assertAlmostEqual(node["legacy_modifiers"][key], node["modifiers"][key] * 0.2, places=5, msg=(node["key"], key))
                self.assertNotAlmostEqual(node["legacy_modifiers"][key], node["modifiers"][key] * 0.75, places=5)
        self.assertGreater(amended, 0)

    def test_transition_math_covers_all_profiles_preparations_repairs_and_negotiation(self):
        tested_paths = 0
        for tag, model in self.models.items():
            abrupt = {item["id"]: item["modifiers"] for item in model["initial_transition"]["abrupt"]}
            for liability in ("broken_supply", "state_accounts", "command_gap"):
                prep_max = len(lifecycle.PREP[liability])
                self.assertIn(liability, abrupt)
                for prep_count in range(prep_max + 1):
                    for repair_count in range(4):
                        for negotiated in (False, True):
                            actual = lifecycle._transition_values(model, tag, liability, prep_count, repair_count, negotiated)
                            prep_factor = max(0, 1 - 0.25 * prep_count)
                            repair_factor = max(0, (3 - repair_count) / 3)
                            agreement_factor = 0.6 if negotiated else 1
                            expected = {key: round(value * prep_factor * repair_factor * agreement_factor, 5) for key, value in abrupt[liability].items()}
                            self.assertEqual(actual, expected, (tag, liability, prep_count, repair_count, negotiated))
                            if repair_count == 3:
                                self.assertTrue(all(value == 0 for value in actual.values()), (tag, liability, prep_count, negotiated))
                            tested_paths += 1
        self.assertEqual(tested_paths, 14 * (3 + 2 + 2) * 4 * 2)

    def test_emitted_transition_branch_count_matches_exact_combinations(self):
        for tag, model in self.models.items():
            for liability in ("broken_supply", "state_accounts", "command_gap"):
                block = _named_block(self.effects_text, f"COLDWAR_SSR_lifecycle_update_transition_{tag}")
                entry = next(item for item in model["initial_transition"]["abrupt"] if item["id"] == liability)
                prep_states = len(lifecycle.PREP[liability]) + 1
                repair_patterns = sum(math.comb(3, count) for count in range(4))
                branches = prep_states * repair_patterns * 2
                for key in entry["modifiers"]:
                    assignment = f"set_variable = {{ COLDWAR_SSR_lifecycle_transition_{liability}_{key} ="
                    self.assertEqual(block.count(assignment), branches, (tag, liability, key))
                for count in range(prep_states):
                    self.assertIn(f"has_country_flag = COLDWAR_SSR_lifecycle_prep_snapshot_{liability}_{count}", block)
                self.assertIn("COLDWAR_SSR_negotiated_transition_active = yes", block)
                self.assertIn("NOT = { COLDWAR_SSR_negotiated_transition_active = yes }", block)

    def test_snapshot_is_one_time_and_rebuilds_do_not_charge_or_issue_assets(self):
        reconcile = _named_block(self.effects_text, "COLDWAR_SSR_reconcile")
        capture = _named_block(self.effects_text, "COLDWAR_SSR_lifecycle_capture_transition")
        self.assertIn("NOT = { has_country_flag = COLDWAR_SSR_lifecycle_transition_recorded }", reconcile)
        self.assertIn("set_country_flag = COLDWAR_SSR_lifecycle_transition_recorded", reconcile)
        self.assertIn("COLDWAR_SSR_lifecycle_snapshot_preparation_UKR = yes", capture)
        self.assertIn("COLDWAR_SSR_lifecycle_snapshot_preparation_TAJ = yes", capture)
        check_status = _named_block(self.effects_text, "COLDWAR_SSR_lifecycle_check_status")
        self.assertIn("NOT = { has_country_flag = COLDWAR_SSR_lifecycle_transition_recorded }", check_status)
        self.assertIn("COLDWAR_SSR_lifecycle_snapshot_preparation_UKR = yes", capture)
        rebuild_groups = _named_block(self.effects_text, "COLDWAR_SSR_lifecycle_rebuild_groups")
        rebuild_specs = _named_block(self.effects_text, "COLDWAR_SSR_lifecycle_rebuild_specialisation")
        for block in (reconcile, capture, rebuild_groups, rebuild_specs):
            for forbidden in ("treasury_change", "add_manpower", "add_equipment_to_stockpile", "add_equipment_bonus", "set_country_flag = { flag ="):
                self.assertNotIn(forbidden, block)

    def test_dynamic_modifier_removals_are_guarded(self):
        removals = re.findall(
            r"remove_dynamic_modifier = \{ modifier = ([A-Za-z0-9_]+) \}",
            self.effects_text,
        )
        self.assertTrue(removals)
        for modifier in set(removals):
            guarded = f"if = {{ limit = {{ has_dynamic_modifier = {{ modifier = {modifier} }} }} remove_dynamic_modifier = {{ modifier = {modifier} }} }}"
            self.assertEqual(self.effects_text.count(guarded), removals.count(modifier), modifier)

    def test_daily_status_watcher_covers_delayed_release_transition(self):
        for tag in shared.TAGS:
            self.assertIn(
                f"on_daily_{tag} = {{ effect = {{ {tag} = {{ COLDWAR_SSR_lifecycle_check_status = yes COLDWAR_SSR_market_reconcile = yes COLDWAR_SSR_diplomacy_reconcile = yes }} }} }}",
                self.on_actions_text,
            )
        for hook in ("on_subject_free", "on_release_as_free", "on_release_as_puppet"):
            self.assertIn(f"{hook} = {{ effect = {{ ROOT = {{ COLDWAR_SSR_lifecycle_check_status = yes }} }} }}", self.on_actions_text)
        check_status = _named_block(self.effects_text, "COLDWAR_SSR_lifecycle_check_status")
        self.assertIn("COLDWAR_SSR_is_participant = yes has_country_flag = COLDWAR_SSR_lifecycle_ever_ssr is_subject = no", check_status)
        self.assertIn("NOT = { has_country_flag = COLDWAR_SSR_lifecycle_transition_recorded }", check_status)
        self.assertIn("COLDWAR_SSR_lifecycle_capture_transition = yes", check_status)

    def test_approved_agriculture_keys_and_runtime_outputs_are_registered(self):
        amendments = json.loads((SRC / "approved_amendments.json").read_text(encoding="utf-8"))
        labels = amendments["labels"]
        self.assertEqual(labels["agriculture_district_worker_requirement_modifier"], "Agricultural district workforce requirement")
        self.assertEqual(labels["agriculture_workers_modifier"], "Subsistence agricultural workforce requirement")
        agriculture_states = lifecycle.specialisation_catalog(self.models)["agriculture"]
        self.assertTrue(any("agriculture_district_worker_requirement_modifier" in s["full_modifiers"] for s in agriculture_states))
        self.assertTrue(any("agriculture_workers_modifier" in s["full_modifiers"] for s in agriculture_states))

    def test_market_courses_are_costed_only_by_the_market_provider(self):
        lifecycle_budget = _named_block(self.effects_text, "COLDWAR_SSR_lifecycle_refresh_budget")
        market_nodes = [n for n in self.nodes if n.get("market_course")]
        self.assertEqual({n["key"] for n in market_nodes}, {"gradual_conversion", "rapid_conversion", "directed_reform"})
        for node in market_nodes:
            self.assertNotIn(node["receipt"], lifecycle_budget, node["key"])
        market_budget = _named_block(_read(ROOT / "common/scripted_effects/COLDWAR_SSR_market.txt"), "COLDWAR_SSR_market_refresh_budget")
        self.assertIn("COLDWAR_SSR_market_weekly_expense = { value = gdp_total multiply = 0.00005 }", market_budget)
        self.assertIn("COLDWAR_SSR_market_weekly_expense = { value = gdp_total multiply = 0.00015 }", market_budget)
        for node in self.nodes:
            if node.get("weekly_gdp_cost") and not node.get("specialisation") and not node.get("market_course"):
                if node["phase"] in ("ssr", "independent", "party"):
                    self.assertIn(node["receipt"], lifecycle_budget, node["key"])

    def test_generated_scripts_use_project_marker_and_expected_encoding(self):
        for path in (IDEAS_PATH, EFFECTS_PATH, TRIGGERS_PATH, ROOT / "common/dynamic_modifiers/COLDWAR_SSR_lifecycle_dynamic_modifiers.txt"):
            raw = path.read_bytes()
            self.assertFalse(raw.startswith(b"\xef\xbb\xbf"), str(path))
            self.assertTrue(raw.startswith(shared.MARKER.encode("utf-8")), str(path))
        raw_loc = LOC_PATH.read_bytes()
        self.assertTrue(raw_loc.startswith(b"\xef\xbb\xbf"))
        self.assertTrue(_read(LOC_PATH).startswith("l_english:"))


if __name__ == "__main__":
    unittest.main()
