# IMPERIA COLD WAR — France 1970 pressure runtime audit.
"""Read-only static audit of the emitted France 1970 pressure package."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUNTIME = ROOT / "tools/france_1970_runtime"
sys.path.insert(0, str(ROOT / "tools"))
from focus_prerequisite_ui import nodes, field
TAGS = ("NGR", "GAB", "SEN", "CAM", "CDI", "CHA")
PREFIX = "COLDWAR_FRA2_pressure"
TAG_PREFIX = "COLDWAR_FRA2_pressure_"
MD_DONOR = Path("E:/SteamLibrary/steamapps/workshop/content/394360/2777392649")
GAME_DOCS = Path("E:/SteamLibrary/steamapps/common/Hearts of Iron IV/documentation")


def check(condition: bool, label: str, details: str = "") -> dict:
    return {"check": label, "passed": bool(condition), "details": details}


def load(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8-sig")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    contracts = json.loads((RUNTIME / "pressure_contracts.json").read_text(encoding="utf-8"))
    manifest = json.loads((RUNTIME / "manifest.json").read_text(encoding="utf-8"))
    design = json.loads((RUNTIME / "runtime_design.json").read_text(encoding="utf-8"))
    files = {
        "effects": load("common/scripted_effects/COLDWAR_FRA2_pressure_effects.txt"),
        "triggers": load("common/scripted_triggers/COLDWAR_FRA2_pressure_triggers.txt"),
        "decisions": load("common/decisions/COLDWAR_FRA2_pressure_decisions.txt"),
        "categories": load("common/decisions/categories/COLDWAR_FRA2_pressure_categories.txt"),
        "events": load("events/COLDWAR_FRA2_pressure_events.txt"),
        "ideas": load("common/ideas/COLDWAR_FRA2_pressure_ideas.txt"),
        "diplomacy": load("common/scripted_effects/COLDWAR_FRA2_diplomacy_effects.txt"),
        "diplomacy_triggers": load("common/scripted_triggers/COLDWAR_FRA2_diplomacy_triggers.txt"),
        "on_actions": load("common/on_actions/COLDWAR_FRA2_1970_on_actions.txt"),
        "money": load("common/scripted_effects/00_money_system.txt"),
        "english": load("localisation/english/COLDWAR_FRA2_1970_l_english.yml"),
    }
    checks: list[dict] = []

    checks.append(check(contracts.get("project") == "IMPERIA COLD WAR", "Project marker in pressure contract"))
    checks.append(check(set(row["tag"] for row in contracts["partners"]) == set(TAGS), "Six intended country tags"))
    checks.append(check(contracts["host_annual_gdp_levy_percent"] == 1.0, "1% annual host GDP levy"))
    checks.append(check(contracts["french_aid_freeze_days"] == 180 and contracts["withdrawal_crisis_days"] == 90,
                        "180-day aid freeze and 90-day crisis"))
    checks.append(check(contracts["send_cost_political_power"] == 35 and contracts["pending_days"] == 30
                        and contracts["pressure_cooldown_days"] == 365,
                        "Political cost, pending period, and reissue cooldown"))

    for path_key in (
        "tools/france_1970_runtime/pressure.py",
        "tools/france_1970_runtime/pressure_contracts.json",
    ):
        manifest_key = "pressure_source_sha256" if path_key.endswith("pressure.py") else "pressure_contracts_sha256"
        checks.append(check(manifest.get(manifest_key) == sha(ROOT / path_key),
                            f"Manifest matches {Path(path_key).name}"))

    expected_outputs = {
        "common/scripted_effects/COLDWAR_FRA2_pressure_effects.txt",
        "common/scripted_triggers/COLDWAR_FRA2_pressure_triggers.txt",
        "common/ideas/COLDWAR_FRA2_pressure_ideas.txt",
        "common/decisions/categories/COLDWAR_FRA2_pressure_categories.txt",
        "common/decisions/COLDWAR_FRA2_pressure_decisions.txt",
        "events/COLDWAR_FRA2_pressure_events.txt",
    }
    installed = manifest.get("files", {})
    checks.append(check(expected_outputs <= set(installed), "All pressure outputs recorded in manifest"))
    for path_key in sorted(expected_outputs):
        entry = installed.get(path_key, {})
        output_path = ROOT / path_key
        checks.append(check(output_path.is_file() and entry.get("sha256") == sha(output_path),
                            f"Manifest matches emitted {Path(path_key).name}"))

    native_keys = set()
    provider_files = []
    for folder in (MD_DONOR / "common/ideas", MD_DONOR / "common/dynamic_modifiers", MD_DONOR / "common/modifier_definitions"):
        for path in folder.rglob("*.txt"):
            if path.is_symlink():
                continue
            text = path.read_text(encoding="utf-8-sig")
            native_keys.update(re.findall(r"^\s*([A-Za-z0-9_]+)\s*=", text, re.M))
            provider_files.append((str(path.relative_to(MD_DONOR)), sha(path)))
    expected_modifier_keys = set(contracts["host_charter_modifiers"]) | set(contracts["france_charter_modifiers"]) | set(contracts["withdrawal_crisis_modifiers"])
    unsupported = sorted(expected_modifier_keys - native_keys)
    checks.append(check(not unsupported, "All charter and crisis modifier keys have native MD providers",
                        ", ".join(unsupported)))
    for idea_id, modifiers in (
        *((f"{PREFIX}_charter_host_{tag}", contracts["host_charter_modifiers"]) for tag in TAGS),
        *((f"{PREFIX}_charter_france_{tag}", contracts["france_charter_modifiers"]) for tag in TAGS),
        (f"{PREFIX}_withdrawal_crisis", contracts["withdrawal_crisis_modifiers"]),
    ):
        block = files["ideas"].split(idea_id + " = {", 1)[1].split("\n\t}", 1)[0] if idea_id + " = {" in files["ideas"] else ""
        missing = [f"{key} = {value}" for key, value in modifiers.items() if f"{key} = {str(value).rstrip('0').rstrip('.')}" not in block]
        checks.append(check(not missing, f"Emitted modifier payload for {idea_id}", "; ".join(missing)))
    checks.append(check("interest_rate_multiplier_modifier = 0.5" in files["ideas"],
                        "Crisis premium emitted as native +0.50 numeric rate change"))

    for tag in TAGS:
        quote = f"{PREFIX}_levy_quote_{tag}"
        cache = f"{PREFIX}_cache_levy_quote_{tag}"
        checks.append(check(f"set_variable = {{ {quote} = {{ value = {tag}.gdp_total multiply = 0.01 divide = 52 }} }}" in files["effects"],
                            f"{tag} quote uses host GDP at annual 1% / 52"))
        checks.append(check(f"FRA = {{ {cache} = yes }}" in files["effects"] and f"{cache} = yes" in files["effects"],
                            f"{tag} expense and income callbacks use the same FRA quote cache"))
        checks.append(check(f"additional_expenses_rate = FRA.{quote}" in files["effects"]
                            and f"COLDWAR_FRA2_cooperation_weekly_expenses = FRA.{quote}" in files["effects"],
                            f"{tag} levy payer contributes to native expense and cooperation totals"))
        checks.append(check(f"additional_income_rate = {quote}" in files["effects"]
                            and f"COLDWAR_FRA2_cooperation_weekly_income = {quote}" in files["effects"],
                            f"{tag} levy recipient contributes to native income and cooperation totals"))
        checks.append(check(f"COLDWAR_FRA2_pressure_can_send_{tag}" in files["triggers"]
                            and f"COLDWAR_FRA2_pressure_can_accept_{tag}" in files["triggers"]
                            and f"COLDWAR_FRA2_pressure_can_timeout_{tag}" in files["triggers"],
                            f"{tag} send, acceptance, and timeout guards emitted"))
        checks.append(check(f"has_country_flag = {TAG_PREFIX}pending_{tag}" in files["triggers"]
                            and f"{tag} = {{ has_country_flag = {TAG_PREFIX}pending_{tag} }}" in files["triggers"],
                            f"{tag} proposal requires paired pending receipts"))
        event_id = TAGS.index(tag) + 1
        checks.append(check(f"id = COLDWAR_FRA2_pressure.{event_id}" in files["events"]
                            and f"country_event = {{ id = COLDWAR_FRA2_pressure.{event_id} days = 30 }}" in files["effects"],
                            f"{tag} 30-day timeout event is scheduled by pending offer"))
        checks.append(check(f"{tag} = {{ NOT = {{ has_country_flag = {TAG_PREFIX}pending_{tag} }} }}" in files["effects"]
                            and f"NOT = {{ has_country_flag = {TAG_PREFIX}pending_{tag} }} {tag} = {{ has_country_flag = {TAG_PREFIX}pending_{tag} }}" in files["effects"],
                            f"{tag} orphan pending receipt cleanup is bidirectional"))
        checks.append(check(f"NOT = {{ {PREFIX}_base_active_{tag} = yes COLDWAR_FRA2_pair_{tag}_clear = yes }}" in files["effects"],
                            f"{tag} pending proposal clears on base/peace eligibility loss"))
        checks.append(check(f"{PREFIX}_send_{tag}" in files["decisions"]
                            and f"{PREFIX}_accept_decision_{tag}" in files["decisions"]
                            and f"{PREFIX}_refuse_decision_{tag}" in files["decisions"],
                            f"{tag} fixed-recipient send, accept and refuse decisions emitted"))

    freeze_flag_counts = {tag: files["diplomacy"].count(f"NOT = {{ has_country_flag = {TAG_PREFIX}aid_freeze_{tag} }}") for tag in TAGS}
    design_nodes = {node["key"]: node for node in design["nodes"]}
    expected_frozen_pairs = {}
    for tag in TAGS:
        pair_count = 0
        for key, node in design_nodes.items():
            offer = node.get("offer", {})
            if offer.get("partner") != tag:
                continue
            for row in offer.get("france", {}).get("effects", []):
                if row.get("kind") == "weekly_transfer" and row.get("payer") == "FRA" and row.get("flow") == "expense":
                    pair_count += 1
        expected_frozen_pairs[tag] = pair_count
        checks.append(check(freeze_flag_counts[tag] >= 2 * pair_count if pair_count else freeze_flag_counts[tag] == 0,
                            f"{tag} every FRA-funded transfer expense and matched income skip together",
                            f"expected at least {2 * pair_count} guard uses; emitted {freeze_flag_counts[tag]}"))

    refusal_blocks_ok = True
    for tag in TAGS:
        marker = f"COLDWAR_FRA2_pressure_register_refusal_{tag} = {{"
        if marker not in files["effects"]:
            refusal_blocks_ok = False
            continue
        block = files["effects"].split(marker, 1)[1].split("\n}\n", 1)[0]
        if (f"FRA = {{ {PREFIX}_refusal_qualifies_{tag} = yes }}" not in block
                or "add_timed_idea = { idea = COLDWAR_FRA2_pressure_withdrawal_crisis days = 90 }" not in block
                or "give_military_access" in block or "give_guarantee" in block
                or "diplomatic_relation" in block or "remove_resource_rights" in block):
            refusal_blocks_ok = False
    checks.append(check(refusal_blocks_ok, "Refusal freezes French aid and adds crisis without changing base access, guarantees, or resource rights"))

    effects = files["effects"]
    receipt_cleanup_ok = True
    for tag in TAGS:
        for receipt, relation in (
            (f"{TAG_PREFIX}access_owned_{tag}", f"relation = military_access"),
            (f"{TAG_PREFIX}guarantee_owned_{tag}", f"relation = guarantee"),
        ):
            if receipt not in effects or relation not in effects:
                receipt_cleanup_ok = False
        if f"has_country_flag = {TAG_PREFIX}access_owned_{tag}" not in effects or f"has_country_flag = {TAG_PREFIX}guarantee_owned_{tag}" not in effects:
            receipt_cleanup_ok = False
        if f"clr_country_flag = {TAG_PREFIX}access_owned_{tag}" not in effects or f"clr_country_flag = {TAG_PREFIX}guarantee_owned_{tag}" not in effects:
            receipt_cleanup_ok = False
    checks.append(check(receipt_cleanup_ok, "Access and guarantee are receipt-owned and receipt-cleared on suspension"))

    checks.append(check("COLDWAR_FRA2_cleanup_orphaned_recipient_ideas = yes" in files["on_actions"],
                        "Recipient-side France-death cleanup is called from the daily lifecycle"))
    checks.append(check("COLDWAR_FRA2_pressure_sync_all = yes" in files["diplomacy"]
                        and "COLDWAR_FRA2_sync_treaties = yes" in files["on_actions"],
                        "Pressure reconciliation is called by the bounded France treaty lifecycle"))
    checks.append(check(files["diplomacy"].count("COLDWAR_FRA2_pressure_add_weekly_expenses = yes") == 1
                        and files["diplomacy"].count("COLDWAR_FRA2_pressure_add_weekly_income = yes") == 1
                        and "COLDWAR_FRA2_add_weekly_income = yes" in files["money"]
                        and "COLDWAR_FRA2_add_weekly_expenses = yes" in files["money"],
                        "Pressure streams are wired once into both native weekly money calculations"))
    checks.append(check("COLDWAR_FRA2_cooperation_weekly_income" in files["english"]
                        and "COLDWAR_FRA2_cooperation_weekly_expenses" in files["english"],
                        "Native cooperation-budget display providers are present"))
    checks.append(check("IMP_sanctions_add_" not in files["effects"] and "imp_dip_sanc_" not in files["effects"],
                        "Pressure uses aid freeze rather than creating a separate sanction"))

    # Parse the actual emitted script and inspect transaction branches rather than
    # treating generator configuration as evidence of runtime behavior.
    effect_ast = nodes(files["effects"])
    trigger_ast = nodes(files["triggers"])
    decision_ast = nodes(files["decisions"])
    category_ast = nodes(files["categories"])
    event_ast = nodes(files["events"])
    diplomacy_ast = nodes(files["diplomacy"])
    diplomacy_trigger_ast = nodes(files["diplomacy_triggers"])
    def top_map(rows):
        return {row.key: row for row in rows if row.key != "_bare"}
    effect_map = top_map(effect_ast)
    trigger_map = top_map(trigger_ast)
    category_map = top_map(category_ast)
    diplomacy_map = top_map(diplomacy_ast)
    diplomacy_trigger_map = top_map(diplomacy_trigger_ast)
    all_decisions = {row.key: row for root in decision_ast for row in root.children()}
    all_events = {field(row.children(), "id"): row for row in event_ast if row.key == "country_event"}
    def descendants(row):
        for child in row.children():
            yield child
            yield from descendants(child)
    def has_node(row, key, value=None):
        return any(n.key == key and (value is None or n.value == value) for n in descendants(row))
    def immediate_children(row, key):
        return [n for n in row.children() if n.key == key]
    def paired_if_else(rows, predicate):
        for idx, item in enumerate(rows):
            if item.key == "if" and idx + 1 < len(rows) and rows[idx + 1].key == "else" and predicate(item):
                return item, rows[idx + 1]
            found = paired_if_else(item.children(), predicate)
            if found:
                return found
        return None
    hidden_decision_paths = True
    for tag in TAGS:
        for suffix, helper in (("accept", f"{PREFIX}_accept_{tag}"),
                               ("refuse", f"{PREFIX}_refuse_{tag}")):
            dec = all_decisions.get(f"{PREFIX}_{suffix}_decision_{tag}")
            complete = next(iter(immediate_children(dec, "complete_effect")), None) if dec else None
            preview = next(iter(immediate_children(complete, "effect_tooltip")), None) if complete else None
            hidden = next(iter(immediate_children(complete, "hidden_effect")), None) if complete else None
            if not (preview and hidden and has_node(preview, f"{PREFIX}_preview_{tag}", "yes")
                    and has_node(hidden, helper, "yes") and not has_node(preview, helper, "yes")):
                hidden_decision_paths = False
    for tag in TAGS:
        dec = all_decisions.get(f"{PREFIX}_send_{tag}")
        complete = next(iter(immediate_children(dec, "complete_effect")), None) if dec else None
        preview = next(iter(immediate_children(complete, "effect_tooltip")), None) if complete else None
        hidden = next(iter(immediate_children(complete, "hidden_effect")), None) if complete else None
        if not (preview and hidden and has_node(preview, f"{PREFIX}_preview_{tag}", "yes")
                and has_node(hidden, f"{PREFIX}_start_{tag}", "yes")):
            hidden_decision_paths = False
    checks.append(check(hidden_decision_paths,
                        "Emitted decision AST separates display previews from one hidden transaction call"))

    setup_transaction_ok = True
    no_replay_ok = True
    sync_block = effect_map.get(f"{PREFIX}_sync_all")
    for tag in TAGS:
        accept = effect_map.get(f"{PREFIX}_accept_{tag}")
        start = effect_map.get(f"{PREFIX}_start_{tag}")
        refuse = effect_map.get(f"{PREFIX}_refuse_{tag}")
        register_refusal = effect_map.get(f"{PREFIX}_register_refusal_{tag}")
        if (not accept or not start or not refuse or not register_refusal
                or f"value = gdp_total multiply = -0.0004" not in files["effects"]
                or f"value = gdp_total multiply = -0.001" not in files["effects"]
                or not has_node(accept, "modify_treasury_effect")
                or has_node(start, "modify_treasury_effect")
                or has_node(refuse, "modify_treasury_effect")
                or has_node(register_refusal, "modify_treasury_effect")):
            setup_transaction_ok = False
        if accept and (has_node(accept, "add_building_construction") or has_node(accept, "add_tech_bonus")
                       or has_node(accept, "army_experience") or has_node(accept, "add_doctrine_cost_reduction")):
            setup_transaction_ok = False
        if not sync_block or any(has_node(sync_block, effect) for effect in
                                 ("modify_treasury_effect", "add_building_construction", "add_tech_bonus",
                                  "army_experience", "add_doctrine_cost_reduction")):
            no_replay_ok = False
    checks.append(check(setup_transaction_ok,
                        "Only accepted charter execution charges the two own-GDP setup fees; send/refusal paths do not charge or award finite assets"))
    checks.append(check(no_replay_ok,
                        "Treaty sync restores ongoing status only, without replaying setup costs, buildings, research, XP, or doctrine awards"))

    category_ok = (category_map.get("COLDWAR_FRA2_pressure_send_category") is not None
                   and category_map.get("COLDWAR_FRA2_pressure_response_category") is not None
                   and has_node(category_map["COLDWAR_FRA2_pressure_send_category"], "allowed")
                   and has_node(category_map["COLDWAR_FRA2_pressure_response_category"], "allowed"))
    checks.append(check(category_ok, "Both emitted decision categories use native allowed/visible schema"))

    loc_keys = set(re.findall(r"^\s*([^\s:]+):\d+\s+", files["english"], re.M))
    required_loc = set()
    for row in all_decisions.values():
        required_loc.add(row.key)
        required_loc.add(row.key + "_desc")
        for item in descendants(row):
            if item.key in ("tooltip", "custom_effect_tooltip", "custom_cost_text") and isinstance(item.value, str):
                required_loc.add(item.value)
    for category_id in ("COLDWAR_FRA2_pressure_send_category", "COLDWAR_FRA2_pressure_response_category"):
        required_loc.update((category_id, category_id + "_desc"))
    missing_loc = sorted(required_loc - loc_keys)
    checks.append(check(not missing_loc, "All pressure decision/category names, descriptions, and custom tooltip keys resolve to English localization",
                        ", ".join(missing_loc)))

    event_paths_ok = True
    for index, tag in enumerate(TAGS, 1):
        evt = all_events.get(f"COLDWAR_FRA2_pressure.{index}")
        immediate = next(iter(immediate_children(evt, "immediate")), None) if evt else None
        rows = immediate.children() if immediate else []
        pos = next((i for i, row in enumerate(rows) if row.key == "if"), -1)
        if pos < 0 or pos + 1 >= len(rows) or rows[pos + 1].key != "else":
            event_paths_ok = False
            continue
        branch = rows[pos]
        fallback = rows[pos + 1]
        if (not has_node(branch, f"{PREFIX}_can_timeout_{tag}", "yes")
                or not has_node(branch, f"{PREFIX}_refuse_{tag}", "yes")
                or not has_node(fallback, f"{PREFIX}_cancel_{tag}", "yes")):
            event_paths_ok = False
    checks.append(check(event_paths_ok, "Timeout AST refuses only while base and bilateral eligibility still hold; otherwise cancels"))

    # The acceptance guard is evaluated from emitted trigger AST, with external
    # native pair and base-offer providers represented as controlled fixture inputs.
    # This is a narrow source-model, not a HOI4 runtime simulation.
    class Fixture:
        def __init__(self, recipient, flags=(), gdp=100, france_gdp=100, exists=True, base=True, clear=True):
            self.recipient = recipient
            self.flags = {"FRA": set(), recipient: set()}
            for scope, flag in flags:
                self.flags.setdefault(scope, set()).add(flag)
            self.gdp = {"FRA": france_gdp, recipient: gdp}
            self.exists = {recipient: exists, "FRA": True}
            self.base = base
            self.clear = clear
        def trigger(self, name, scope, stack=()):
            if name in stack or name not in trigger_map and name not in diplomacy_trigger_map:
                if name.startswith("COLDWAR_FRA2_offer_active_"):
                    return self.base
                raise KeyError(name)
            row = trigger_map.get(name) or diplomacy_trigger_map.get(name)
            return all(self.condition(child, scope, stack + (name,)) for child in row.children())
        def condition(self, row, scope, stack=()):
            key, value = row.key, row.value
            kids = row.children()
            if key in ("AND", "limit"):
                return all(self.condition(ch, scope, stack) for ch in kids)
            if key == "OR":
                return any(self.condition(ch, scope, stack) for ch in kids)
            if key == "NOT":
                return not all(self.condition(ch, scope, stack) for ch in kids)
            if key in ("FRA", self.recipient) and isinstance(value, list):
                return all(self.condition(ch, key, stack) for ch in kids)
            if key == "tag": return str(value) == scope
            if key == "country_exists": return self.exists.get(str(value), False)
            if key == "has_country_flag": return str(value) in self.flags.get(scope, set())
            if key == "check_variable":
                if isinstance(value, list):
                    child = value[0]
                    if child.key == "gdp_total": return self.gdp.get(scope, 0) > float(child.value)
                return False
            if key.startswith("COLDWAR_FRA2_pressure_") or key.startswith("COLDWAR_FRA2_pair_"):
                if str(value) != "yes": return False
                if key.endswith("_clear"): return self.clear
                if key.startswith("COLDWAR_FRA2_pressure_base_active_"): return self.base
                return self.trigger(key, scope, stack)
            if key.startswith("COLDWAR_FRA2_offer_active_"): return self.base
            if key == "IMP_is_1970_scenario": return True
            if key == "has_completed_focus": return True
            if key in ("is_at_war_with", "has_war_with", "is_embargoing"):
                return False
            if key == "is_in_array": return False
            if key == "_bare": return False
            raise KeyError(f"unmodeled trigger {key}={value!r}")
    trace_cases = []
    trace_ok = True
    for tag in TAGS:
        pending = TAG_PREFIX + "pending_" + tag
        signed = TAG_PREFIX + "charter_signed_" + tag
        paired = [("FRA", pending), (tag, pending)]
        cases = [
            ("accept-ready", "can_accept", paired, {}, True),
            ("reject-war", "can_accept", paired, {"clear": False}, False),
            ("reject-embargo", "can_accept", paired, {"clear": False}, False),
            ("reject-diplomatic-sanction", "can_accept", paired, {"clear": False}, False),
            ("reject-financial-sanction", "can_accept", paired, {"clear": False}, False),
            ("reject-economic-sanction", "can_accept", paired, {"clear": False}, False),
            ("reject-military-sanction", "can_accept", paired, {"clear": False}, False),
            ("reject-invalid-base", "can_accept", paired, {"base": False}, False),
            ("reject-zero-host-gdp", "can_accept", paired, {"gdp": 0}, False),
            ("reject-zero-france-gdp", "can_accept", paired, {"france_gdp": 0}, False),
            ("reject-one-sided-pending", "can_accept", [("FRA", pending)], {}, False),
            ("reject-replay-france-receipt", "can_accept", paired + [("FRA", signed)], {}, False),
            ("reject-replay-host-receipt", "can_accept", paired + [(tag, signed)], {}, False),
            ("timeout-ready", "can_timeout", paired, {}, True),
            ("timeout-base-lost", "can_timeout", paired, {"base": False}, False),
            ("timeout-bilateral-blocked", "can_timeout", paired, {"clear": False}, False),
            ("timeout-zero-gdp", "can_timeout", paired, {"gdp": 0}, False),
            ("refusal-crisis-eligible", "refusal_qualifies", [], {}, True),
            ("refusal-base-lost-no-crisis", "refusal_qualifies", [], {"base": False}, False),
            ("refusal-bilateral-blocked-no-crisis", "refusal_qualifies", [], {"clear": False}, False),
            ("refusal-zero-gdp-no-crisis", "refusal_qualifies", [], {"gdp": 0}, False),
        ]
        for label, trigger_suffix, flags, options, expected in cases:
            fx = Fixture(tag, flags, **options)
            actual = fx.trigger(f"{PREFIX}_{trigger_suffix}_{tag}", tag)
            trace_cases.append({"tag": tag, "case": label, "expected": expected, "actual": actual,
                                "pair_clear_is_controlled_fixture": "bilateral" in label or any(word in label for word in ("war", "embargo", "sanction"))})
            if actual != expected: trace_ok = False
    checks.append(check(trace_ok,
                        "Emitted-trigger source-model traces cover acceptance, replay, timeout, refusal qualification, base/GDP, and pair blocks"))

    # Verify each FRA-funded transfer row in the compiled catalogue has one
    # payer-GDP quote and matched expense/income consumers from that same quote.
    transfer_match_ok = True
    transfer_rows_checked = 0
    for node in design.get("nodes", []):
        offer = node.get("offer")
        if not isinstance(offer, dict) or offer.get("partner") not in TAGS:
            continue
        partner = offer["partner"]
        fr_effects = offer.get("france", {}).get("effects", [])
        host_effects = offer.get("recipient", {}).get("effects", [])
        all_rows = fr_effects + host_effects
        transfers = [r for r in all_rows if r.get("kind") == "weekly_transfer"]
        for i in range(0, len(transfers), 2):
            pair = transfers[i:i + 2]
            expense = next((r for r in pair if r.get("flow") == "expense"), None)
            income = next((r for r in pair if r.get("flow") == "income"), None)
            if not expense or not income or expense.get("payer") != "FRA" or income.get("payer") != "FRA":
                continue
            transfer_rows_checked += 1
            key = node["key"]
            quote = f"COLDWAR_FRA2_transfer_quote_{key}_{i // 2}"
            fraction = expense.get("gdp_fraction")
            expected_formula = (f"set_variable = {{ {quote} = {{ value = FRA.gdp_total multiply = "
                                f"{str(fraction)} divide = 52 }} }}")
            payer_expense = f"additional_expenses_rate = FRA.{quote}"
            recipient_income = f"additional_income_rate = FRA.{quote}"
            if (expected_formula not in files["diplomacy"]
                    or payer_expense not in files["diplomacy"]
                    or recipient_income not in files["diplomacy"]
                    or f"COLDWAR_FRA2_cooperation_weekly_expenses = FRA.{quote}" not in files["diplomacy"]
                    or f"COLDWAR_FRA2_cooperation_weekly_income = FRA.{quote}" not in files["diplomacy"]
                    or f"COLDWAR_FRA2_pressure_aid_freeze_{partner}" not in files["diplomacy"]):
                transfer_match_ok = False
    checks.append(check(transfer_match_ok and transfer_rows_checked > 0,
                        "Every emitted France-funded weekly transfer uses one France-GDP quote for matched payment, receipt, and fiscal totals",
                        f"checked {transfer_rows_checked} transfer rows"))

    # Native owned-vs-preexisting diplomatic rights: set ownership receipts only
    # on a grant made by this helper; remove only if that receipt exists.
    owned_relation_ok = True
    owned_relation_details = []
    sync_block = effect_map.get(f"{PREFIX}_sync_all")
    for tag in TAGS:
        pair = paired_if_else(sync_block.children(), lambda n: has_node(n, f"{PREFIX}_active_{tag}", "yes")) if sync_block else None
        if not pair:
            owned_relation_ok = False
            owned_relation_details.append(f"{tag}: missing if/else reconciliation pair")
            continue
        active_block, inactive_block = pair
        for relation, exists_trigger, ownership_flag in (
            ("give_guarantee", "has_guaranteed", f"{TAG_PREFIX}guarantee_owned_{tag}"),
            ("give_military_access", "has_military_access_to", f"{TAG_PREFIX}access_owned_{tag}"),
        ):
            if (not has_node(active_block, relation)
                    or not has_node(active_block, exists_trigger)
                    or not has_node(active_block, "set_country_flag", ownership_flag)
                    or not has_node(active_block, "NOT")):
                owned_relation_ok = False
                owned_relation_details.append(f"{tag}: active grant block missing {relation}/{exists_trigger}/{ownership_flag} or negative existence guard")
        for ownership_flag, relation in (
            (f"{TAG_PREFIX}guarantee_owned_{tag}", "guarantee"),
            (f"{TAG_PREFIX}access_owned_{tag}", "military_access"),
        ):
            if (not has_node(inactive_block, "has_country_flag", ownership_flag)
                    or not has_node(inactive_block, "diplomatic_relation")
                    or not has_node(inactive_block, "relation", relation)
                    or not has_node(inactive_block, "active", "no")
                    or not has_node(inactive_block, "clr_country_flag", ownership_flag)):
                owned_relation_ok = False
                owned_relation_details.append(f"{tag}: inactive block missing owned {ownership_flag} removal receipt")
    checks.append(check(owned_relation_ok,
                        "Relation reconciliation records grants only when absent and removes only feature-owned guarantees/access",
                        "; ".join(owned_relation_details)))

    # Verify access direction against the installed HOI4 documentation, then
    # verify the emitted base and pressure grant/revoke scopes follow it.
    trigger_doc = (GAME_DOCS / "triggers_documentation.md").read_text(encoding="utf-8")
    effect_doc = (GAME_DOCS / "effects_documentation.md").read_text(encoding="utf-8")
    relation_doc = effect_doc.split("## diplomatic_relation", 1)[1].split("## ", 1)[0]
    access_trigger_doc = trigger_doc.split("## has_military_access_to", 1)[1].split("## ", 1)[0]
    access_effect_doc = effect_doc.split("## give_military_access", 1)[1].split("## ", 1)[0]
    docs_semantics_ok = ("check country has military access to specified country" in access_trigger_doc
                         and "gives military access to the specified country" in access_effect_doc
                         and "no to cancel existing one" in relation_doc)

    access_design = []
    for node in design.get("nodes", []):
        offer = node.get("offer")
        if not isinstance(offer, dict):
            continue
        for side in ("france", "recipient"):
            for item in offer.get(side, {}).get("effects", []):
                if item.get("kind") == "access" and item.get("relation") == "military_access":
                    relation = (node["key"], item["grantor"], item["beneficiary"])
                    if relation not in access_design:
                        access_design.append(relation)
    emitted_access_ok = True
    access_cases = []
    normalized_diplomacy = re.sub(r"\s+", " ", files["diplomacy"])
    def is_tag_scope(n):
        return n.key.isalpha() and len(n.key) == 3 and isinstance(n.value, list)
    for key, grantor, beneficiary in access_design:
        receipt = f"COLDWAR_FRA2_access_owned_{key}_{grantor}"
        grant = (f"if = {{ limit = {{ {beneficiary} = {{ NOT = {{ has_military_access_to = {grantor} }} }} }} "
                 f"{grantor} = {{ give_military_access = {beneficiary} set_country_flag = {receipt} }} }}")
        revoke = (f"if = {{ limit = {{ {grantor} = {{ has_country_flag = {receipt} }} }} "
                  f"{beneficiary} = {{ if = {{ limit = {{ has_military_access_to = {grantor} }} "
                  f"diplomatic_relation = {{ country = {grantor} relation = military_access active = no }} }} }} "
                  f"{grantor} = {{ clr_country_flag = {receipt} }} }}")
        grant_ok = grant in normalized_diplomacy
        removal_ok = revoke in normalized_diplomacy
        if not grant_ok or not removal_ok:
            emitted_access_ok = False
            access_cases.append({"offer": key, "grantor": grantor, "beneficiary": beneficiary,
                                 "grantor_preflight_and_receipt": grant_ok, "beneficiary_scope_revoke": removal_ok})

    # Pressure charter's fixed relation is grantor host -> beneficiary France.
    pressure_access_ok = True
    normalized_pressure = re.sub(r"\s+", " ", files["effects"])
    for tag in TAGS:
        receipt = f"{TAG_PREFIX}access_owned_{tag}"
        grant = (f"if = {{ limit = {{ NOT = {{ has_military_access_to = {tag} }} }} "
                 f"{tag} = {{ give_military_access = FRA set_country_flag = {receipt} }} }}")
        revoke = (f"if = {{ limit = {{ {tag} = {{ has_country_flag = {receipt} }} }} "
                  f"if = {{ limit = {{ has_military_access_to = {tag} }} "
                  f"diplomatic_relation = {{ country = {tag} relation = military_access active = no }} }} "
                  f"{tag} = {{ clr_country_flag = {receipt} }} }}")
        if grant not in normalized_pressure or revoke not in normalized_pressure:
            pressure_access_ok = False
    checks.append(check(docs_semantics_ok and emitted_access_ok and pressure_access_ok,
                        "Military access direction matches installed native docs for all base and pressure grants/revocations",
                        json.dumps({"native_docs": docs_semantics_ok, "base_relations": access_cases,
                                    "pressure_relations": pressure_access_ok}, ensure_ascii=False)))

    timed_refresh_ok = True
    for tag in TAGS:
        freeze = f"{TAG_PREFIX}aid_freeze_{tag}"
        refresh = f"{TAG_PREFIX}aid_freeze_refresh_{tag}"
        if (f"flag = {freeze} value = 1 days = 180" not in files["effects"]
                or f"flag = {refresh}" not in files["effects"]
                or f"has_country_flag = {refresh} NOT = {{ has_country_flag = {freeze} }}" not in files["effects"]
                or f"add_timed_idea = {{ idea = {PREFIX}_withdrawal_crisis days = 90 }}" not in files["effects"]):
            timed_refresh_ok = False
    checks.append(check(timed_refresh_ok,
                        "Refusal applies a 180-day France aid freeze and 90-day host crisis with expiry-driven money refresh"))

    # Verify all eight mirrored sanction array classes are in each bilateral clear trigger.
    pair_checks_ok = True
    arrays = {f"imp_{kind}_sanc_{direction}_us" for kind in ("dip", "fin", "eco", "mil") for direction in ("on", "by")}
    for tag in TAGS:
        row = diplomacy_trigger_map.get(f"COLDWAR_FRA2_pair_{tag}_clear")
        used = {str(n.value) for n in descendants(row) if n.key == "array"} if row else set()
        if (not arrays.issubset(used)
                or not has_node(row, "has_war_with")
                or not has_node(row, "is_embargoing")
                or not has_node(row, "country_exists", tag)
                or not has_node(row, "country_exists", "FRA")):
            pair_checks_ok = False
    checks.append(check(pair_checks_ok, "Each emitted bilateral guard checks peace, embargo, and all four sanction classes in both directions"))

    # Ensure the host orphan cleanup preserves the permanent agreement receipt.
    orphan_ok = True
    orphan_effect = diplomacy_map.get("COLDWAR_FRA2_cleanup_orphaned_recipient_ideas")
    if not orphan_effect:
        orphan_ok = False
    else:
        for tag in TAGS:
            host_branch = None
            for candidate in descendants(orphan_effect):
                if candidate.key != "if":
                    continue
                limit = next(iter(immediate_children(candidate, "limit")), None)
                if (limit and has_node(limit, "tag", tag)
                        and has_node(limit, "country_exists", "FRA")):
                    host_branch = candidate
                    break
            if (not host_branch
                    or not has_node(host_branch, "remove_ideas", f"{PREFIX}_charter_host_{tag}")
                    or not has_node(host_branch, "clr_country_flag", f"{TAG_PREFIX}access_owned_{tag}")
                    or not has_node(host_branch, "clr_country_flag", f"{TAG_PREFIX}pending_{tag}")
                    or has_node(host_branch, "diplomatic_relation")
                    or has_node(host_branch, "clr_country_flag", f"{TAG_PREFIX}charter_signed_{tag}")):
                orphan_ok = False
    checks.append(check(orphan_ok, "France-death cleanup removes host spirit and local receipts without touching signed lifetime or an expired relation"))

    passed = sum(c["passed"] for c in checks)
    results = {
        "project": "IMPERIA COLD WAR",
        "feature": "France 1970 recipient-approved procurement pressure",
        "contract_sha256": sha(RUNTIME / "pressure_contracts.json"),
        "pressure_generator_sha256": sha(RUNTIME / "pressure.py"),
        "compiled_manifest_sha256": sha(RUNTIME / "manifest.json"),
        "compiled_pressure_outputs": {p: installed.get(p, {}).get("sha256") for p in sorted(expected_outputs)},
        "checks_passed": passed,
        "checks_total": len(checks),
        "checks": checks,
        "source_model_cases": trace_cases,
        "matched_france_transfer_rows": transfer_rows_checked,
        "native_modifier_provider_source": {
            "path": str(MD_DONOR),
            "provider_file_count": len(provider_files),
            "provider_sources_sha256": hashlib.sha256("\n".join(f"{p}:{h}" for p, h in sorted(provider_files)).encode("utf-8")).hexdigest(),
        },
        "native_access_semantics_sources": {
            "trigger_document": {
                "path": str(GAME_DOCS / "triggers_documentation.md"),
                "sha256": sha(GAME_DOCS / "triggers_documentation.md"),
                "heading": "has_military_access_to, line 4208",
            },
            "effect_document": {
                "path": str(GAME_DOCS / "effects_documentation.md"),
                "sha256": sha(GAME_DOCS / "effects_documentation.md"),
                "headings": ["diplomatic_relation, line 3564", "give_military_access, line 4587"],
            },
            "native_directional_cleanup_example": "events/Tajikistan.txt:2204-2212",
        },
        "limitations": ["Emitted AST/source-model checks only. External native pair guards are controlled fixture inputs; no HOI4 engine or live-save test performed by this checker."],
    }
    out = HERE / "PRESSURE_RUNTIME_CHECKS.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"project": results["project"], "passed": passed, "total": len(checks), "failures": [c for c in checks if not c["passed"]], "output": str(out)}, ensure_ascii=False, indent=2))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
