# IMPERIA COLD WAR — France party expansion migration and lifecycle check.
"""Execute only the emitted party-pool migration and sync AST.

This is a restricted source-model check. It does not load HOI4 saves or emulate
native dynamic-modifier refresh timing.
"""
from __future__ import annotations

from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUNTIME = ROOT / "tools/france_1970_runtime"
EFFECTS = ROOT / "common/scripted_effects/COLDWAR_FRA2_1970_effects.txt"
PROPOSAL = HERE / "proposal.json"
ADDITIONS = HERE / "ADDITIONS.json"
DESIGN = RUNTIME / "runtime_design.json"
FOCUS_FILE = ROOT / "common/national_focus/COLDWAR_FRA2_1970_focus.txt"
TRIGGER_FILE = ROOT / "common/scripted_triggers/COLDWAR_FRA2_1970_triggers.txt"
DECISION_FILE = ROOT / "common/decisions/COLDWAR_FRA2_1970_decisions.txt"
LOC_FILE = ROOT / "localisation/english/COLDWAR_FRA2_1970_l_english.yml"
sys.path.insert(0, str(ROOT / "tools"))
from focus_prerequisite_ui import nodes, field

P = "COLDWAR_FRA2_"
MIGRATIONS = {
    P + "migrate_party_revision",
    P + "migrate_CID_pool",
    P + "migrate_starting_spirit_revision",
    P + "sync_programmes",
}
FORBIDDEN_FINITE = {
    "modify_treasury_effect", "add_building_construction",
    "add_extra_state_shared_building_slots", "add_tech_bonus",
    "add_doctrine_cost_reduction", "army_experience", "navy_experience",
    "air_experience", "add_political_power",
}


def number(value) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def date_number(value: str) -> int:
    year, month, day = (int(part) for part in value.split("."))
    return year * 10000 + month * 100 + day


class State:
    def __init__(self, flags=(), variables=None, dynamic=(), scenario=True,
                 tag="FRA", day="1970.1.1",
                 party="nationalist_right_wing_populists_are_in_power"):
        self.flags = set(flags)
        self.variables = {k: number(v) for k, v in (variables or {}).items()}
        self.dynamic = set(dynamic)
        self.scenario = scenario
        self.tag = tag
        self.day = date_number(day)
        self.party = party
        self.ideas = set()

    def condition(self, row):
        key, value = row.key, row.value
        kids = row.children()
        if key in ("limit", "AND"):
            return all(self.condition(child) for child in kids)
        if key == "OR":
            return any(self.condition(child) for child in kids)
        if key == "NOT":
            return not all(self.condition(child) for child in kids)
        if key == "has_country_flag":
            return value in self.flags
        if key == "has_idea":
            return value in self.ideas
        if key == "has_dynamic_modifier":
            return field(kids, "modifier") in self.dynamic
        if key == P + "is_1970" or key == "IMP_is_1970_scenario":
            return self.scenario
        if key == "tag":
            return value == self.tag
        if key == "exists":
            return str(value) == "yes"
        if key == "date" or key.startswith("date "):
            if not re.fullmatch(r"\d+\.\d+\.\d+", str(value)):
                raise AssertionError(f"Unsupported date predicate: {value!r}")
            op, raw = row.op, str(value)
            target = date_number(raw)
            return {"<": self.day < target, "<=": self.day <= target,
                    ">": self.day > target, ">=": self.day >= target,
                    "=": self.day == target}[op]
        if key in ("nationalist_right_wing_populists_are_in_power",
                   "western_social_democrats_are_in_power",
                   "western_liberals_are_in_power",
                   "western_conservatism_are_in_power",
                   "neutrality_neutral_conservatism_are_in_power",
                   "neutrality_neutral_libertarians_are_in_power",
                   "neutrality_neutral_social_are_in_power",
                   "neutrality_neutral_green_are_in_power",
                   "emerging_communist_state_are_in_power"):
            return (key == self.party) == (str(value) == "yes")
        raise AssertionError(f"Unsupported trigger: {key} = {value}")

    @staticmethod
    def _assignment(row):
        children = row.children()
        ignored = {"tooltip", "name", "value"}
        assignment = next((c for c in children if c.key not in ignored), None)
        if assignment is None:
            var = field(children, "var")
            val = field(children, "value")
            if var is None or val is None:
                raise AssertionError(f"Unsupported variable operation: {row.key}")
            return str(var), number(val)
        return assignment.key, number(assignment.value)

    def execute(self, rows, providers, stack=()):
        i = 0
        while i < len(rows):
            row = rows[i]
            key = row.key
            if key == "if":
                limit = next(c for c in row.children() if c.key == "limit")
                passed = self.condition(limit)
                if passed:
                    self.execute([c for c in row.children() if c.key != "limit"], providers, stack)
                if i + 1 < len(rows) and rows[i + 1].key == "else":
                    if not passed:
                        self.execute(rows[i + 1].children(), providers, stack)
                    i += 1
            elif key == "else":
                raise AssertionError("Unpaired else")
            elif key in ("set_variable", "add_to_variable"):
                name, value = self._assignment(row)
                if key == "set_variable":
                    self.variables[name] = value
                else:
                    self.variables[name] = self.variables.get(name, Decimal(0)) + value
            elif key == "set_country_flag":
                assert isinstance(row.value, str), "Migration may only preserve/add durable receipts"
                self.flags.add(row.value)
            elif key in ("clr_country_flag", "clear_country_flag"):
                self.flags.discard(row.value)
            elif key == "force_update_dynamic_modifier":
                pass
            elif key in ("add_dynamic_modifier", "remove_dynamic_modifier"):
                modifier = field(row.children(), "modifier")
                if key == "add_dynamic_modifier":
                    self.dynamic.add(modifier)
                else:
                    self.dynamic.discard(modifier)
            elif key == "swap_ideas":
                self.ideas.discard(field(row.children(), "remove_idea"))
                self.ideas.add(field(row.children(), "add_idea"))
            elif key == "add_ideas":
                self.ideas.add(row.value)
            elif key == "remove_ideas":
                self.ideas.discard(row.value)
            elif key in MIGRATIONS:
                if key in stack:
                    raise AssertionError(f"Recursive provider call: {key}")
                self.execute(providers[key].children(), providers, stack + (key,))
            elif key in FORBIDDEN_FINITE:
                raise AssertionError(f"Finite effect found in migration/sync: {key}")
            elif key == "_bare":
                raise AssertionError(f"Unresolved bare token: {row.value}")
            else:
                raise AssertionError(f"Unsupported effect in migration/sync: {key}")
            i += 1


def pool_key(node):
    return node.get("modifier_pool") or node["group"]


def earned_totals(design, receipts, pools):
    totals = {}
    for node in design["nodes"]:
        pool = pool_key(node)
        if pool not in pools or node.get("offer") or P + "earned_" + node["key"] not in receipts:
            continue
        for effect in node.get("effects", []):
            if effect.get("kind") == "modifier":
                var = f"{P}{pool}_{effect['key']}"
                totals[var] = totals.get(var, Decimal(0)) + number(effect["value"])
    return totals


def main():
    proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    raw = EFFECTS.read_bytes()
    parsed = nodes(raw.decode("utf-8"))
    providers = {row.key: row for row in parsed if row.key.startswith(P)}
    focus_text = FOCUS_FILE.read_text(encoding="utf-8")
    focus_roots = nodes(focus_text)
    focus_tree = next(row for row in focus_roots if row.key == "focus_tree")
    focus_map = {field(row.children(), "id"): row for row in focus_tree.children() if row.key == "focus"}
    trigger_rows = nodes(TRIGGER_FILE.read_text(encoding="utf-8"))
    trigger_map = {row.key: row for row in trigger_rows if row.key.startswith(P)}
    trigger_text = TRIGGER_FILE.read_text(encoding="utf-8")
    loc_text = LOC_FILE.read_text(encoding="utf-8-sig")
    loc_keys = re.findall(r"^ (\S+):\d+ ", loc_text, re.M)
    decision_roots = nodes(DECISION_FILE.read_text(encoding="utf-8"))
    decision_map = {row.key: row for root in decision_roots for row in root.children()
                    if row.key == "COLDWAR_FRA2P_regional_conversion"}
    additions = json.loads(ADDITIONS.read_text(encoding="utf-8"))
    expected_focuses = len(design["nodes"])
    issues = []
    implementation_checks = 0

    def require(ok, message):
        if not ok:
            issues.append(message)

    current_roster = 176 + design.get('foreign_policy_revision', {}).get('added_focus_count', 0)
    manifest = json.loads((ROOT/'tools/france_1970_runtime/manifest.json').read_text(encoding='utf-8'))
    require(expected_focuses == current_roster, "Compiled roster retains the party expansion and authorized later additions")
    require(len(loc_keys) == len(set(loc_keys)) == manifest['english_localisation_keys'],
            "Compiled English localisation has unique keys and matches the current manifest")
    design_keys = {node["key"] for node in design["nodes"]}
    require(set(proposal["expansion_focus_keys"]).issubset(design_keys), "All approved expansion focuses must be integrated")
    require(len(set(proposal["expansion_focus_keys"])) == 20, "Approved expansion must contain twenty unique focus keys")
    groups = {group["id"]: group for group in design["groups"]}
    for key in proposal["expansion_focus_keys"]:
        spec = next((node for node in design["nodes"] if node["key"] == key), None)
        focus = focus_map.get(P + key)
        require(spec is not None and focus is not None, f"Compiled focus exists: {key}")
        if spec is None or focus is None:
            continue
        rows = focus.children()
        available = next((row for row in rows if row.key == "available"), None)
        reward = next((row for row in rows if row.key == "completion_reward"), None)
        require(available is not None and reward is not None, f"Availability and reward blocks exist: {key}")
        if available is None or reward is None:
            continue
        avail = focus_text[available.start:available.end]
        reward_text = focus_text[reward.start:reward.end]
        hidden_availability = next((row for row in available.children() if row.key == "hidden_trigger"), None)
        hidden_text = focus_text[hidden_availability.start:hidden_availability.end] if hidden_availability else ""
        visible_text = "\n".join(focus_text[row.start:row.end] for row in available.children()
                                  if row.key != "hidden_trigger")
        group_trigger = groups[spec["group"]].get("trigger")
        if group_trigger:
            require(f"{group_trigger} = yes" in visible_text, f"Exact native party availability stays visible: {key}")
        require(f"{P}is_1970 = yes" in hidden_text and
                f"NOT = {{ has_country_flag = {P}earned_{key} }}" in hidden_text,
                f"Scenario and replay guards remain in hidden availability: {key}")
        require(f"{P}is_1970 = yes" not in visible_text and
                f"has_country_flag = {P}earned_{key}" not in visible_text,
                f"Internal scenario and receipt checks are hidden from visible requirements: {key}")
        require("effect_tooltip" in reward_text and "hidden_effect" in reward_text,
                f"Native preview and execution are separated: {key}")
        actual_provider = P + "complete_" + key
        actual = providers.get(actual_provider)
        require(actual is not None, f"Completion provider resolves: {key}")
        actual_text = raw.decode("utf-8")[actual.start:actual.end] if actual else ""
        require(f"{actual_provider} = yes" in reward_text,
                f"Focus dispatches its guarded completion provider: {key}")
        require(f"set_country_flag = {P}earned_{key}" in actual_text,
                f"Earned receipt is written by the guarded transaction: {key}")
        require(f"{P}is_1970 = yes" in actual_text and f"NOT = {{ has_country_flag = {P}earned_{key} }}" in actual_text,
                f"Completion provider repeats scenario and replay guards: {key}")
        if any(effect["kind"] == "treasury_gdp" for effect in spec["effects"]):
            require("gdp_total > 0" in hidden_text, f"Positive own-GDP guard remains hidden: {key}")
            require("gdp_total > 0" not in visible_text, f"GDP guard is hidden from visible requirements: {key}")
            hidden = next((row for row in reward.children() if row.key == "hidden_effect"), None)
            tooltip = next((row for row in reward.children() if row.key == "effect_tooltip"), None)
            preview_text = focus_text[tooltip.start:tooltip.end] if tooltip else ""
            require(actual_text.count("modify_treasury_effect = yes") == 1,
                    f"Single actual GDP setup debit: {key}")
            require(preview_text.count("modify_treasury_effect = yes") == 1,
                    f"Single native preview treasury row: {key}")
        buildings = [effect for effect in spec["effects"] if effect["kind"] == "building"]
        slot_effects = [effect for effect in spec["effects"] if effect["kind"] == "state_slots"]
        if buildings or slot_effects:
            require(f"{P}assets_ready_{key} = yes" in avail,
                    f"Visible asset tooltip and preflight gate focus completion: {key}")
            require(f"tooltip = {P}asset_requirement_{key}" in visible_text,
                    f"Asset requirement tooltip is visible: {key}")
            require(f"{P}asset_requirement_{key}" in loc_text,
                    f"Visible asset requirement localisation exists: {key}")
            actual_calls = re.findall(rf"{P}build_{re.escape(key)}_[A-Za-z0-9_]+ = yes", actual_text)
            require(len(actual_calls) == len(buildings), f"One guarded construction helper per building row: {key}")
            for call in actual_calls:
                helper = call.split(" = ", 1)[0]
                require(helper in providers, f"Building helper resolves: {helper}")
                if helper in providers:
                    helper_text = raw.decode("utf-8")[providers[helper].start:providers[helper].end]
                    require("add_extra_state_shared_building_slots" in helper_text and
                            "add_building_construction" in helper_text,
                            f"Building helper grants slots before construction: {helper}")
            ready = trigger_map.get(f"{P}assets_ready_{key}")
            ready_text = (trigger_text[ready.start:ready.end] if ready else "")
            require(ready is not None, f"Asset preflight provider resolves: {key}")
            for asset in buildings + slot_effects:
                require(f"owns_state = {asset['state']}" in ready_text and
                        f"has_full_control_of_state = {asset['state']}" in ready_text,
                        f"Ownership and full control guard state {asset['state']}: {key}")
                require(f"controls_state = {asset['state']}" in ready_text,
                        f"Current control guard state {asset['state']}: {key}")
            for asset in buildings:
                require(f"building_level@{asset['building']}" in ready_text,
                        f"Native physical capacity guard {asset['building']}: {key}")
        implementation_checks += 1

    # The old domestic transaction is only unlocked by an alternate focus
    # receipt. Its payment, asset and research effects remain unchanged.
    changed = next((entry for entry in additions.get("decision_changes", [])
                    if entry.get("after", {}).get("id") == "COLDWAR_FRA2P_regional_conversion"), None)
    require(changed is not None, "Approved Regional Conversion Fund prerequisite revision exists")
    if changed:
        require(changed["before"]["effects"] == changed["after"]["effects"],
                "Regional Conversion Fund fee, asset, and finite research reward are unchanged")
    decision = decision_map.get("COLDWAR_FRA2P_regional_conversion")
    require(decision is not None, "Existing Regional Conversion Fund decision remains emitted")
    if decision:
        decision_text = DECISION_FILE.read_text(encoding="utf-8")
        available = next((row for row in decision.children() if row.key == "available"), None)
        complete = next((row for row in decision.children() if row.key == "complete_effect"), None)
        available_text = decision_text[available.start:available.end] if available else ""
        complete_text = decision_text[complete.start:complete.end] if complete else ""
        require("has_completed_focus = COLDWAR_FRA2_public_banks" in available_text and
                "has_completed_focus = COLDWAR_FRA2_ps_conversion_boards" in available_text,
                "Fund is unlocked by either approved parent focus")
        require("western_social_democrats_are_in_power = yes" in available_text and
                "COLDWAR_FRA2_assets_ready_regional_conversion = yes" in available_text,
                "Fund keeps its native party and current asset preflight guards")
        require(complete_text.count("modify_treasury_effect = yes") == 2,
                "Fund has one preview fee row and one actual fee transaction")
        require("set_country_flag = COLDWAR_FRA2P_regional_conversion_completed" in complete_text,
                "Fund remains one-time")
        implementation_checks += 1
    required_providers = {P + "migrate_party_revision", P + "migrate_CID_pool",
                          P + "migrate_starting_spirit_revision", P + "sync_programmes"}
    require(required_providers.issubset(providers), "Migration and programme-sync providers are emitted")
    if not required_providers.issubset(providers) or expected_focuses != current_roster:
        report = {"project": "IMPERIA COLD WAR", "scope": "Compiled source AST check; no native engine/save loading",
                  "passed": False, "issues": issues}
        print(json.dumps(report, indent=2))
        return 1

    def walk(rows):
        for row in rows:
            yield row
            yield from walk(row.children())

    for name in required_providers:
        for row in walk(providers[name].children()):
            require(row.key not in FORBIDDEN_FINITE,
                    f"One-time migration/sync provider contains finite effect {row.key}: {name}")

    # A legacy save has the old CID deltas stored under Right, alongside a
    # genuine FN programme receipt. Start the variables with stale values to
    # prove the migration clears and reconstructs pools rather than adding on.
    receipts = {P + "earned_cid_tax", P + "earned_cid_cooperatives", P + "earned_fn_defence"}
    right = earned_totals(design, receipts, {"right"})
    cid = earned_totals(design, receipts, {"CID"})
    legacy_values = {}
    for node in design["nodes"]:
        pool = pool_key(node)
        if pool in {"right", "CID"}:
            for effect in node.get("effects", []):
                if effect.get("kind") == "modifier":
                    legacy_values[f"{P}_{pool}_{effect['key']}"] = Decimal("7.25")
    for var in right:
        legacy_values[var] = Decimal("7.25")
    for var in cid:
        legacy_values[var] = Decimal("-4.5")

    state = State(flags=receipts, variables=legacy_values,
                  dynamic={P + "right_programme", P + "CID_programme"})
    state.execute(providers[P + "migrate_CID_pool"].children(), providers)
    state.execute(providers[P + "migrate_party_revision"].children(), providers)
    for var in set(right) | set(cid):
        expected = right.get(var, Decimal(0)) + cid.get(var, Decimal(0))
        require(state.variables.get(var, Decimal(0)) == expected, f"Rebuilt party variable {var}")
    require(receipts.issubset(state.flags), "Existing earned focus receipts must be retained")
    require(P + "right_programme" not in state.dynamic and P + "CID_programme" in state.dynamic,
            "CID migration detaches the stale Right container once and keeps the earned CID container")
    after_migration = (state.variables.copy(), state.flags.copy(), state.dynamic.copy())
    state.execute(providers[P + "migrate_CID_pool"].children(), providers)
    state.execute(providers[P + "migrate_party_revision"].children(), providers)
    require((state.variables, state.flags, state.dynamic) == after_migration, "Migrations are one-time and replay-safe")
    migration_replay_safe = (state.variables, state.flags, state.dynamic) == after_migration

    # Run actual programme sync through government turnover and the CID-to-FN
    # date transition. The synthetic interpreter only models its authored AST.
    state.flags.update({P + "party_revision_20261029_investment_migrated",
                        P + "CID_pool_20261030_migrated",
                        P + "starting_spirit_revision_20261029_migrated"})
    before_receipts = state.flags.copy()
    state.party = "nationalist_right_wing_populists_are_in_power"
    state.day = date_number("1970.1.1")
    state.execute(providers[P + "sync_programmes"].children(), providers)
    require(P + "CID_programme" in state.dynamic and P + "right_programme" in state.dynamic,
            "Before 5 October 1972, CID and earned FN/right programmes can be active together")
    require(state.flags == before_receipts, "Government sync must not replay or clear earned receipts")

    state.party = "western_liberals_are_in_power"
    state.execute(providers[P + "sync_programmes"].children(), providers)
    require(P + "CID_programme" not in state.dynamic and P + "right_programme" not in state.dynamic,
            "Leaving the right party suspends both dated CID and right programmes")
    require(state.flags == before_receipts, "Party turnover must preserve completed focus receipts")

    state.party = "nationalist_right_wing_populists_are_in_power"
    state.execute(providers[P + "sync_programmes"].children(), providers)
    require(P + "CID_programme" in state.dynamic and P + "right_programme" in state.dynamic,
            "Returning to the right party restores both earned programmes before the identity transition")

    state.day = date_number("1972.10.5")
    state.execute(providers[P + "sync_programmes"].children(), providers)
    require(P + "CID_programme" not in state.dynamic,
            "CID modifier pool ends on 5 October 1972 when FN replaces the dated identity")
    require(P + "right_programme" in state.dynamic,
            "The ordinary FN/right modifier pool remains active after the CID cutoff")
    require(state.flags == before_receipts, "Date transition changes no focus receipts or finite rewards")

    # An old save can have CID receipts but no earned FN/right receipt. Its
    # previous shared Right modifier may still be attached and must be removed.
    cid_only_receipts = {P + "earned_cid_tax", P + "earned_cid_cooperatives"}
    cid_only_expected = earned_totals(design, cid_only_receipts, {"CID"})
    stale_right = earned_totals(design, cid_only_receipts, {"right"})
    cid_only_vars = {**{key: Decimal("6.5") for key in cid_only_expected},
                     **{key: Decimal("-8") for key in stale_right}}
    old_cid_only = State(flags=cid_only_receipts, variables=cid_only_vars,
                         dynamic={P + "right_programme"})
    old_cid_only.execute(providers[P + "migrate_CID_pool"].children(), providers)
    old_cid_only.execute(providers[P + "migrate_party_revision"].children(), providers)
    require(P + "right_programme" not in old_cid_only.dynamic,
            "CID-only old save must clear the stale Right dynamic modifier during migration")
    for var in stale_right:
        require(old_cid_only.variables.get(var, Decimal(0)) == 0,
                f"CID-only save must clear obsolete Right variable {var}")
    require(old_cid_only.flags == cid_only_receipts | {
        P + "party_revision_20261029_investment_migrated", P + "CID_pool_20261030_migrated"},
        "CID-only migration preserves focus receipts and adds only migration receipts")
    old_cid_only.execute(providers[P + "sync_programmes"].children(), providers)
    require(P + "CID_programme" in old_cid_only.dynamic and P + "right_programme" not in old_cid_only.dynamic,
            "After sync, an old CID-only save has CID active without restoring the stale Right pool")
    require(cid_only_receipts.issubset(old_cid_only.flags), "CID-only sync retains the original earned receipts")

    report = {
        "project": "IMPERIA COLD WAR",
        "scope": "Restricted execution of compiled France migration and party-sync AST; not native engine, save loading, or multiplayer evidence",
        "proposal_sha256": hashlib.sha256(PROPOSAL.read_bytes()).hexdigest(),
        "compiled_design_sha256": hashlib.sha256(DESIGN.read_bytes()).hexdigest(),
        "core_generator_sha256": hashlib.sha256((RUNTIME / "core.py").read_bytes()).hexdigest(),
        "compiled_design_focuses": expected_focuses,
        "english_localisation_keys": len(loc_keys),
        "approved_expansion_focuses": 20,
        "targeted_focus_transaction_checks": implementation_checks - (1 if decision else 0),
        "regional_fund_transaction_check": decision is not None,
        "building_levels_and_slots": [
            sum(effect.get("amount", 0) for node in design["nodes"] if node["key"] in proposal["expansion_focus_keys"]
                for effect in node.get("effects", []) if effect["kind"] == "building"),
            sum(effect.get("slots", 0) for node in design["nodes"] if node["key"] in proposal["expansion_focus_keys"]
                for effect in node.get("effects", []) if effect["kind"] == "building"),
        ],
        "standalone_shared_slots": sum(effect["amount"] for node in design["nodes"]
                                       if node["key"] in proposal["expansion_focus_keys"]
                                       for effect in node.get("effects", []) if effect["kind"] == "state_slots"),
        "emitted_effects_sha256": hashlib.sha256(raw).hexdigest(),
        "emitted_focus_sha256": hashlib.sha256(FOCUS_FILE.read_bytes()).hexdigest(),
        "emitted_trigger_sha256": hashlib.sha256(TRIGGER_FILE.read_bytes()).hexdigest(),
        "emitted_decision_sha256": hashlib.sha256(DECISION_FILE.read_bytes()).hexdigest(),
        "emitted_english_localisation_sha256": hashlib.sha256(LOC_FILE.read_bytes()).hexdigest(),
        "legacy_receipts": sorted(flag.removeprefix(P + "earned_") for flag in receipts),
        "migration_replay_safe": migration_replay_safe,
        "cases": ["old CID receipts migrate from Right to CID", "one-time replay", "right party leaves and returns",
                  "CID pool ends at 1972-10-05 while FN/right pool remains"],
        "issues": issues,
        "passed": not issues,
    }
    (HERE / "IMPLEMENTATION_CHECKS.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
