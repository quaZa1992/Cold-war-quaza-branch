# IMPERIA COLD WAR — France V5 emitted-core regression checks.
"""Source-level checks for the installed V5 France political tree.

Run with: python tools/france_1970/test_core_v5.py
This does not start HOI4 or claim to validate Clausewitz runtime semantics.
"""
import json
import re
import unittest
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = json.loads((HERE / "approved_design_v5.json").read_text(encoding="utf-8"))
FOCUS_PATH = ROOT / "common/national_focus/COLDWAR_FRA_1970_focus.txt"
EFFECT_PATH = ROOT / "common/scripted_effects/COLDWAR_FRA_1970_effects.txt"
IDEA_PATH = ROOT / "common/ideas/COLDWAR_FRA_1970_ideas.txt"
TRIGGER_PATH = ROOT / "common/scripted_triggers/COLDWAR_FRA_1970_triggers.txt"
LOC_PATH = ROOT / "localisation/english/COLDWAR_FRA_1970_l_english.yml"
sys.path.insert(0, str(ROOT / "tools/vietnam_1970"))
from script_ast import parse, first, values


def read(path):
    return path.read_text(encoding="utf-8-sig")


def blocks(source, keyword):
    """Return (header, body) for balanced Clausewitz blocks named by regex."""
    found = []
    for match in re.finditer(keyword + r"\s*=\s*\{", source):
        start = match.end() - 1
        depth, quoted, escaped, comment = 0, False, False, False
        for pos in range(start, len(source)):
            c = source[pos]
            if comment:
                if c == "\n":
                    comment = False
                continue
            if quoted:
                if escaped:
                    escaped = False
                elif c == "\\":
                    escaped = True
                elif c == '"':
                    quoted = False
                continue
            if c == "#":
                comment = True
            elif c == '"':
                quoted = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    found.append((match.group(0), source[start + 1:pos]))
                    break
        else:
            raise AssertionError(f"unclosed block after {match.group(0)!r}")
    return found


def named_block(source, name):
    result = blocks(source, re.escape(name))
    if len(result) != 1:
        raise AssertionError(f"expected one {name} block, got {len(result)}")
    return result[0][1]


def ast_file(path):
    return parse(path.read_text(encoding="utf-8-sig"))


def numeric(value):
    try:
        return Decimal(str(value))
    except Exception:
        return None


EFFECT_AST = {k: v for k, _, v in ast_file(EFFECT_PATH)}
TRIGGER_AST = {k: v for k, _, v in ast_file(TRIGGER_PATH)}
IDEA_TREE = {k: v for k, _, v in ast_file(IDEA_PATH)}
IDEA_AST = {k: v for k, _, v in first(IDEA_TREE["ideas"], "country")}
DM_AST = {k: v for k, _, v in ast_file(ROOT / "common/dynamic_modifiers/COLDWAR_FRA_1970_dynamic_modifiers.txt")}


class CountryModel:
    """Small interpreter for the emitted effect/trigger subset used by this tree."""
    def __init__(self, group, dlcs=()):
        self.flags = set()
        self.ideas = set()
        self.dynamic = set()
        self.variables = defaultdict(Decimal)
        self.tech = set()
        self.projects = {"sp_armoured_vehicle_project", "sp_aircraft_project", "sp_naval_vessel_project"}
        self.dlcs = set(dlcs)
        self.day = (1973, 1, 1) if group == "national" else (1970, 1, 1)
        self.pp = Decimal(0)
        self.awards = []
        self.xp = defaultdict(Decimal)
        self.doctrine = []
        self.equipment_ideas = set()
        self.can_send = True
        self.sent_offers = []
        gate = next(n["party_gate"] for n in DESIGN["nodes"] if n["group"] == group)
        self.variables["ruling_party"] = Decimal(gate.get("ruling_party_equals", 1))

    def value(self, value):
        parsed = numeric(value)
        return parsed if parsed is not None else self.variables[str(value)]

    def condition(self, rows, any_=False):
        outcomes = []
        for key, op, value in rows:
            if key == "OR":
                ok = self.condition(value, True)
            elif key in ("AND", "hidden_trigger", "limit", "custom_trigger_tooltip"):
                ok = self.condition(value)
            elif key == "NOT":
                ok = not self.condition(value)
            elif key in TRIGGER_AST:
                ok = self.condition(TRIGGER_AST[key]) == (value == "yes")
            elif key == "has_country_flag":
                ok = value in self.flags
            elif key == "has_idea":
                ok = value in self.ideas
            elif key == "has_dynamic_modifier":
                ok = first(value, "modifier") in self.dynamic
            elif key.startswith("COLDWAR_FRA_v5_") and key.endswith("_can_send"):
                ok = self.can_send
            elif key == "has_tech":
                ok = value in self.tech
            elif key == "has_dlc":
                ok = value.strip('"') in self.dlcs
            elif key == "is_special_project_completed":
                ok = value.removeprefix("sp:") in self.projects
            elif key == "date":
                day = tuple(int(x) for x in value.split("."))
                ok = self.day < day if op == "<" else self.day > day
            elif key == "check_variable":
                if first(value, "var"):
                    a = self.value(first(value, "var")); b = self.value(first(value, "value"))
                    compare = first(value, "compare", "equals")
                    ok = {"equals": a == b, "greater_than_or_equals": a >= b, "less_than": a < b}[compare]
                else:
                    a, compare, b = value[0]; a = self.value(a); b = self.value(b)
                    ok = a == b if compare == "=" else a > b if compare == ">" else a < b
            elif key in ("tag", "original_tag"):
                ok = value == "FRA"
            elif key in ("exists", "IMP_is_1970_scenario", "always"):
                ok = value == "yes"
            elif key in ("tooltip", "custom_effect_tooltip", "_bare"):
                continue
            else:
                raise AssertionError(f"Unsupported model trigger: {(key, op, value)}")
            outcomes.append(ok)
        return any(outcomes) if any_ else all(outcomes)

    def execute(self, rows):
        previous = None
        for key, op, value in rows:
            if key == "if":
                previous = self.condition(first(value, "limit", []))
                if previous:
                    self.execute([row for row in value if row[0] != "limit"])
            elif key == "else":
                if previous is False:
                    self.execute(value)
                previous = None
            elif key == "set_variable":
                name, _, val = value[0]; self.variables[name] = self.value(val)
            elif key == "add_to_variable":
                name, _, val = value[0]; self.variables[name] += self.value(val)
            elif key == "set_country_flag": self.flags.add(value)
            elif key == "clr_country_flag": self.flags.discard(value)
            elif key == "add_ideas":
                self.ideas.add(value)
                if value in IDEA_AST and any(k == "equipment_bonus" for k, _, _ in IDEA_AST[value]):
                    self.equipment_ideas.add(value)
            elif key == "remove_ideas":
                self.ideas.discard(value); self.equipment_ideas.discard(value)
            elif key == "swap_ideas":
                self.ideas.discard(first(value, "remove_idea")); self.ideas.add(first(value, "add_idea"))
            elif key == "add_dynamic_modifier": self.dynamic.add(first(value, "modifier"))
            elif key == "remove_dynamic_modifier": self.dynamic.discard(first(value, "modifier"))
            elif key == "add_political_power": self.pp += self.value(value)
            elif key == "add_stability": self.variables["stability"] += self.value(value)
            elif key in ("army_experience", "navy_experience", "air_experience"):
                self.xp[key] += self.value(value)
            elif key == "add_tech_bonus": self.awards.append(value)
            elif key == "add_doctrine_cost_reduction": self.doctrine.append(value)
            elif key == "add_to_array": pass
            elif key == "COLDWAR_FRA_refresh_programmes": self.execute(EFFECT_AST[key])
            elif key in ("COLDWAR_FRA_offer_maintenance", "COLDWAR_FRA_v5_offer_maintenance"): pass
            elif key.startswith("COLDWAR_FRA_v5_") and key.endswith("_can_send"):
                continue  # The deterministic external offer stub approves this modelled dispatch.
            elif key.startswith("COLDWAR_FRA_v5_") and key.endswith("_send"):
                self.sent_offers.append(key)
            elif key in EFFECT_AST: self.execute(EFFECT_AST[key])
            elif key in ("force_update_dynamic_modifier", "mark_focus_tree_layout_dirty", "log"):
                pass
            else: raise AssertionError(f"Unsupported model effect: {(key, op, value)}")

    def call(self, name): self.execute(EFFECT_AST[name])

    def available(self, name):
        # Extract emitted available block from the focus block by exact ID.
        focus = next(body for _, body in blocks(FOCUS_PATH.read_text(encoding="utf-8-sig"), r"focus")
                     if re.search(r"\bid\s*=\s*" + re.escape(name) + r"\b", body))
        available = blocks(focus, r"available")
        return self.condition(parse("x = {" + available[0][1] + "}")[0][2])

    def snapshot_finite(self):
        return (self.pp, len(self.awards), dict(self.xp), len(self.doctrine))

    def party_wrong(self, group):
        node = next(n for n in DESIGN["nodes"] if n["group"] == group and not n["party_gate"].get("any_governing_party"))
        self.variables["ruling_party"] = Decimal(999)
        return node


def compatible_routes(group):
    nodes = [n for n in DESIGN["nodes"] if n["group"] == group]
    pairs = sorted({tuple(sorted((n["key"], p))) for n in nodes for p in n["exclusive"]})
    routes = set()
    import itertools
    for bits in itertools.product((0, 1), repeat=len(pairs)):
        forbidden = {pair[bit] for pair, bit in zip(pairs, bits)}
        reached = set()
        for _ in nodes:
            extra = {n["key"] for n in nodes
                     if n["key"] not in reached | forbidden
                     and all(any(p.removeprefix("COLDWAR_FRA_") in reached for p in row) for row in n["parents"])}
            if not extra:
                break
            reached.update(extra)
        routes.add(tuple(sorted(reached)))
    return {r for r in routes if not any(set(r) < set(other) for other in routes)}


def expected_equipment(route_nodes, dlc):
    totals = defaultdict(Decimal)
    for node in route_nodes:
        for family, amount in node.get("equipment", {}).items():
            targets = DESIGN["equipment_families"][family]["targets"]
            chosen = targets.get("all", targets.get("By Blood Alone" if dlc else "without By Blood Alone", []))
            for target in chosen:
                totals[target] += Decimal(str(amount))
    return dict(totals)


def actual_equipment(country):
    totals = defaultdict(Decimal)
    for idea_id in country.equipment_ideas:
        idea = IDEA_AST[idea_id]
        for bonus in values(idea, "equipment_bonus"):
            for equipment, _, modifiers in bonus:
                for modifier, _, amount in modifiers:
                    if modifier == "build_cost_ic":
                        totals[equipment] += Decimal(amount)
    return dict(totals)


class InstalledCoreV5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.focus = read(FOCUS_PATH)
        cls.effects = read(EFFECT_PATH)
        cls.ideas = read(IDEA_PATH)
        cls.triggers = read(TRIGGER_PATH)
        cls.loc = read(LOC_PATH)
        cls.nodes = DESIGN["nodes"]

    def test_emitted_inventory_and_unique_focus_ids(self):
        self.assertEqual(DESIGN["project"], "IMPERIA COLD WAR")
        self.assertEqual(DESIGN["revision"], 5)
        parsed = blocks(self.focus, r"focus")
        ids = [re.search(r"\bid\s*=\s*(\S+)", body).group(1) for _, body in parsed]
        expected = [n["id"] for n in self.nodes]
        self.assertEqual(len(expected), 260)
        self.assertEqual(len(set(expected)), len(expected))
        self.assertEqual(set(ids), set(expected))
        self.assertEqual(len(ids), len(set(ids)))

    def test_each_reward_helper_is_once_only_and_rechecks_runtime_gates(self):
        for node in self.nodes:
            helper = named_block(self.effects, "COLDWAR_FRA_apply_" + node["id"].removeprefix("COLDWAR_FRA_"))
            self.assertIn(f'COLDWAR_FRA_{node["group"]}_government = yes', helper, node["id"])
            self.assertIn(f'NOT = {{ has_country_flag = {node["id"]}_earned }}', helper, node["id"])
            for parent_set in node["parents"]:
                for parent in parent_set:
                    self.assertIn(f'has_country_flag = COLDWAR_FRA_{parent}_earned', helper, node["id"])
            for excluded in node["exclusive"]:
                self.assertIn(f'NOT = {{ has_country_flag = COLDWAR_FRA_{excluded}_earned }}', helper, node["id"])
            self.assertIn(f'set_country_flag = {node["id"]}_earned', helper, node["id"])
            self.assertIn("COLDWAR_FRA_refresh_programmes = yes", helper, node["id"])

    def test_focus_visibility_keeps_real_party_and_research_requirements(self):
        for node in self.nodes:
            # Verify the ID by selecting the block containing the exact focus id.
            body = next(b for _, b in blocks(self.focus, r"focus") if re.search(r"\bid\s*=\s*" + re.escape(node["id"]) + r"\b", b))
            gate = node["party_gate"]
            if "ruling_party_equals" in gate:
                self.assertIn(f'COLDWAR_FRA_{node["group"]}_government = yes', body)
                self.assertIn("COLDWAR_FRA_is_1970", self.triggers)
                self.assertIn(f'check_variable = {{ ruling_party = {gate["ruling_party_equals"]} }}', self.triggers)
            for effect in node.get("one_time_effects", []):
                if effect["kind"] == "tech_bonus":
                    for variant in effect.get("target_variants", []):
                        for tech in variant["technologies"]:
                            self.assertIn(f"has_tech = {tech}", body, node["id"])
                        for project in variant.get("required_projects", []):
                            self.assertIn(f"is_special_project_completed = sp:{project}", body, node["id"])
                    if effect.get("target_variants"):
                        self.assertIn("custom_trigger_tooltip", body, node["id"])

    def test_equipment_ideas_are_government_and_earned_bound_and_refreshable(self):
        refresh = named_block(self.effects, "COLDWAR_FRA_refresh_programmes")
        for node in self.nodes:
            if not node.get("equipment"):
                continue
            idea_ids = re.findall(r"\b(COLDWAR_FRA_" + re.escape(node["id"].removeprefix("COLDWAR_FRA_")) + r"_equipment(?:_bba|_legacy)?)[ \t]*=\s*\{", self.ideas)
            self.assertTrue(idea_ids, node["id"])
            for idea_id in idea_ids:
                idea = named_block(self.ideas, idea_id)
                self.assertIn(f'COLDWAR_FRA_{node["group"]}_government = yes', idea)
                self.assertIn(f'has_country_flag = {node["id"]}_earned', idea)
                self.assertIn("equipment_bonus = {", idea)
                self.assertIn(f"has_idea = {idea_id}", refresh)
                self.assertIn(f"add_ideas = {idea_id}", refresh)
                self.assertIn(f"remove_ideas = {idea_id}", refresh)
            # The refresh reconstructs removable modifiers only; permanent research,
            # XP, doctrine, or PP rewards must stay inside focus apply helpers.
            self.assertNotRegex(refresh, r"\b(add_tech_bonus|add_doctrine_cost_reduction|army_experience|add_political_power)\s*=")

    def test_starting_spirits_and_initializer_are_guarded_once(self):
        init = named_block(self.effects, "COLDWAR_FRA_1970_initialize")
        self.assertIn("COLDWAR_FRA_is_1970 = yes", init)
        self.assertIn("NOT = { has_country_flag = COLDWAR_FRA_1970_initialized }", init)
        for spirit in ("presidential_republic", "unsettled_social_compromise", "uneven_modernisation"):
            self.assertIn(f"add_ideas = COLDWAR_FRA_{spirit}", init)
            self.assertEqual(len(re.findall(r"\bCOLDWAR_FRA_" + spirit + r"\s*=\s*\{", self.ideas)), 1)

    def test_emitted_ast_completion_replay_party_and_research_guards(self):
        start_ideas = {s["id"] for s in DESIGN["spirits"]}
        for node in self.nodes:
            action = "COLDWAR_FRA_apply_" + node["key"]
            for dlcs in ((), ("No Step Back", "By Blood Alone")):
                c = CountryModel(node["group"], dlcs)
                c.ideas.update(start_ideas)
                for parents in node["parents"]:
                    c.flags.add("COLDWAR_FRA_" + parents[0] + "_earned")
                c.call(action)
                self.assertIn(node["id"] + "_earned", c.flags, f"completion rejected: {node['id']} {dlcs}")
                self.assertEqual(c.pp, Decimal(str(node["pp"])), node["id"])
                expected_awards = 0
                for e in node.get("one_time_effects", []):
                    if e["kind"] != "tech_bonus":
                        continue
                    variants = e.get("target_variants")
                    if not variants:
                        expected_awards += 1
                    elif any(all((v in dlcs) if k == "has_dlc" else (v not in dlcs) for k, v in spec.get("when", {}).items()) for spec in variants):
                        expected_awards += 1
                self.assertEqual(len(c.awards), expected_awards, f"research award count: {node['id']} {dlcs}")
                for transition in node.get("transitions", []):
                    self.assertNotIn(transition["source"], c.ideas, node["id"])
                    if transition["target"]:
                        self.assertIn(transition["target"], c.ideas, node["id"])
                snapshot = c.snapshot_finite()
                c.call(action)
                self.assertEqual(c.snapshot_finite(), snapshot, f"focus replayed finite reward: {node['id']}")
                c.call("COLDWAR_FRA_refresh_programmes")
                self.assertEqual(c.snapshot_finite(), snapshot, f"refresh replayed finite reward: {node['id']}")

                if node["group"] != "institutions":
                    wrong = CountryModel(node["group"], dlcs)
                    for parents in node["parents"]:
                        wrong.flags.add("COLDWAR_FRA_" + parents[0] + "_earned")
                    wrong.variables["ruling_party"] = Decimal(999)
                    wrong.call(action)
                    self.assertNotIn(node["id"] + "_earned", wrong.flags, f"wrong-party completion: {node['id']}")
                    self.assertEqual(wrong.pp, 0, node["id"])
                    self.assertFalse(wrong.awards, node["id"])

                for excluded in node["exclusive"]:
                    blocked = CountryModel(node["group"], dlcs)
                    for parents in node["parents"]:
                        blocked.flags.add("COLDWAR_FRA_" + parents[0] + "_earned")
                    blocked.flags.add("COLDWAR_FRA_" + excluded + "_earned")
                    blocked.call(action)
                    self.assertNotIn(node["id"] + "_earned", blocked.flags, f"exclusive completed: {node['id']}")
                    self.assertEqual(blocked.pp, 0, node["id"])

                for effect in (x for x in node.get("one_time_effects", []) if x.get("target_variants")):
                    active = next(v for v in effect["target_variants"] if all((val in dlcs) if key == "has_dlc" else (val not in dlcs) for key, val in v.get("when", {}).items()))
                    exhausted = CountryModel(node["group"], dlcs)
                    for parents in node["parents"]:
                        exhausted.flags.add("COLDWAR_FRA_" + parents[0] + "_earned")
                    exhausted.tech.update(active["technologies"])
                    exhausted.call(action)
                    self.assertNotIn(node["id"] + "_earned", exhausted.flags, f"fully researched focus available: {node['id']}")
                    self.assertEqual(exhausted.pp, 0, node["id"])
                    if active.get("required_projects"):
                        missing = CountryModel(node["group"], dlcs)
                        for parents in node["parents"]:
                            missing.flags.add("COLDWAR_FRA_" + parents[0] + "_earned")
                        missing.projects.clear()
                        missing.call(action)
                        self.assertNotIn(node["id"] + "_earned", missing.flags, f"missing project allowed: {node['id']}")

                if node.get("offer_id"):
                    declined = CountryModel(node["group"], dlcs); declined.can_send = False
                    for parents in node["parents"]:
                        declined.flags.add("COLDWAR_FRA_" + parents[0] + "_earned")
                    declined.call(action)
                    self.assertNotIn(node["id"] + "_earned", declined.flags)
                    self.assertFalse(declined.sent_offers)

    def test_all_252_routes_rebuild_modifiers_and_equipment_without_replay(self):
        route_count = 0
        for group in DESIGN["groups"]:
            gid = group["id"]
            routes = compatible_routes(gid)
            route_count += len(routes)
            group_nodes = {n["key"]: n for n in self.nodes if n["group"] == gid}
            modifier_names = sorted({m for n in group_nodes.values() for m in n["mods"]})
            for route in routes:
                route_nodes = [group_nodes[key] for key in route]
                for dlc in (False, True):
                    c = CountryModel(gid, ("No Step Back", "By Blood Alone") if dlc else ())
                    c.flags.update("COLDWAR_FRA_" + key + "_earned" for key in route)
                    c.ideas.update(s["id"] for s in DESIGN["spirits"])
                    c.call("COLDWAR_FRA_refresh_programmes")
                    for modifier in modifier_names:
                        expected = sum((Decimal(str(n["mods"].get(modifier, 0))) for n in route_nodes), Decimal(0))
                        self.assertEqual(c.variables[f"COLDWAR_FRA_{gid}_{modifier}"], expected, f"route sum {gid}/{modifier}/{route}")
                    self.assertIn(f"COLDWAR_FRA_{gid}_programme", c.dynamic, gid)
                    self.assertEqual(actual_equipment(c), expected_equipment(route_nodes, dlc), f"equipment profile {gid}/{route}/{dlc}")
                    finite = c.snapshot_finite()
                    c.variables["ruling_party"] = Decimal(999)
                    c.call("COLDWAR_FRA_refresh_programmes")
                    self.assertEqual(f"COLDWAR_FRA_{gid}_programme" in c.dynamic, gid == "institutions", f"government modifier ownership: {gid}")
                    if gid != "institutions":
                        self.assertFalse(c.equipment_ideas, f"wrong-party equipment lingered: {gid}")
                    self.assertEqual(c.snapshot_finite(), finite, "party switch replayed one-time effect")
                    gate = next(n["party_gate"] for n in self.nodes if n["group"] == gid)
                    c.variables["ruling_party"] = Decimal(gate.get("ruling_party_equals", 1))
                    c.day = (1970, 1, 1) if gid == "cid" else (1973, 1, 1) if gid == "national" else (1970, 1, 1)
                    c.call("COLDWAR_FRA_refresh_programmes")
                    self.assertIn(f"COLDWAR_FRA_{gid}_programme", c.dynamic, f"programme failed to reactivate: {gid}")
                    self.assertEqual(actual_equipment(c), expected_equipment(route_nodes, dlc), f"equipment failed to reactivate: {gid}")
                    self.assertEqual(c.snapshot_finite(), finite, "reactivation replayed finite effect")
        self.assertEqual(route_count, 252)

    def test_programme_party_eligibility_and_startup_scenario_guards(self):
        c = CountryModel("gaullist")
        c.call("COLDWAR_FRA_1970_initialize")
        self.assertEqual(c.ideas, {s["id"] for s in DESIGN["spirits"]})
        c.ideas.remove("COLDWAR_FRA_unsettled_social_compromise")
        c.call("COLDWAR_FRA_1970_initialize")
        self.assertNotIn("COLDWAR_FRA_unsettled_social_compromise", c.ideas)
        cid = CountryModel("cid")
        cid.flags.add("COLDWAR_FRA_shopkeepers_voice_earned")
        cid.call("COLDWAR_FRA_refresh_programmes")
        self.assertIn("COLDWAR_FRA_cid_programme", cid.dynamic)
        cid.day = (1972, 10, 5)
        cid.call("COLDWAR_FRA_refresh_programmes")
        self.assertNotIn("COLDWAR_FRA_cid_programme", cid.dynamic)
        national = CountryModel("national")
        national.flags.add("COLDWAR_FRA_small_traders_earned")
        national.call("COLDWAR_FRA_refresh_programmes")
        self.assertIn("COLDWAR_FRA_national_programme", national.dynamic)

    def test_encoding_markers_and_localisation(self):
        for path in (FOCUS_PATH, EFFECT_PATH, IDEA_PATH, TRIGGER_PATH):
            self.assertFalse(path.read_bytes().startswith(b"\xef\xbb\xbf"), path)
            self.assertIn("# IMPERIA COLD WAR", path.read_text(encoding="utf-8"), path)
        self.assertTrue(LOC_PATH.read_bytes().startswith(b"\xef\xbb\xbf"))
        self.assertIn("# IMPERIA COLD WAR", self.loc)


if __name__ == "__main__":
    result = unittest.main(verbosity=2, exit=False).result
    report = {"project": "IMPERIA COLD WAR", "kind": "Emitted AST source-model tests; not HOI4",
              "revision": 5, "tests": result.testsRun, "focuses": 260,
              "dlc_configurations": 2, "compatible_routes": 252,
              "result": "pass" if result.wasSuccessful() else "fail",
              "external_offer_model": "Separate test_offers_v5.py; stubbed in the domestic model",
              "engine_tested": False}
    (HERE / "PROGRAMME_TESTS.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    raise SystemExit(not result.wasSuccessful())
