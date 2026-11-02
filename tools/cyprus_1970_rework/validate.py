# IMPERIA COLD WAR — Cyprus 1970 static validation.
"""Read-only static checks for the installed compact Cyprus rework.

Run from any directory with ``python tools/cyprus_1970_rework/validate.py``.
The script writes only VALIDATION_REPORT.json beside itself. It never installs
or rewrites runtime files.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PREFIX = "COLDWAR_CYP_R2_"
EXPECTED_FOREIGN = {
    "COLDWAR_GRE_CYP_R2_gre_officers", "COLDWAR_GRE_CYP_R2_gre_treaty",
    "COLDWAR_GRE_CYP_R2_gre_network", "COLDWAR_GRE_CYP_R2_gre_consult",
    "COLDWAR_GRE_CYP_R2_gre_withdraw", "COLDWAR_GRE_CYP_R2_gre_coup",
    "COLDWAR_GRE_CYP_R2_gre_response", "COLDWAR_GRE_CYP_R2_gre_volunteers",
    "COLDWAR_GRE_CYP_R2_gre_escalate", "COLDWAR_TUR_CYP_R2_tur_consult",
    "COLDWAR_TUR_CYP_R2_tur_terms", "COLDWAR_TUR_CYP_R2_tur_operation",
    "COLDWAR_TUR_CYP_R2_tur_abstain", "COLDWAR_ENG_CYP_R2_eng_consult",
    "COLDWAR_ENG_CYP_R2_eng_mediation", "COLDWAR_ENG_CYP_R2_eng_restraint",
}
TURKISH_DECISIONS = {
    "COLDWAR_CYP_R2_army_rotate", "COLDWAR_CYP_R2_army_mandate",
    "COLDWAR_CYP_R2_army_control", "COLDWAR_CYP_R2_army_intervene",
}


def read_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8-sig")


def get_rows(text: str) -> list[tuple[str, str, Any]]:
    sys.path.insert(0, str(ROOT / "tools" / "vietnam_1970"))
    from script_ast import parse
    return parse(text)


def direct(rows: list[tuple[str, str, Any]], key: str) -> list[Any]:
    return [value for name, _op, value in rows if name == key]


def recursively(rows: list[tuple[str, str, Any]]):
    for key, op, value in rows:
        yield key, op, value
        if isinstance(value, list):
            yield from recursively(value)


def parse_tree_focuses(text: str, keys: set[str] = {"focus", "shared_focus"}) -> list[dict[str, Any]]:
    rows = get_rows(text)
    result = []
    for root_key, _op, root_value in rows:
        if root_key in keys and isinstance(root_value, list):
            ids = direct(root_value, "id")
            if ids:
                result.append({"id": str(ids[0]), "rows": root_value})
        if root_key != "focus_tree" or not isinstance(root_value, list):
            continue
        for key, _focus_op, value in root_value:
            if key in keys and isinstance(value, list):
                ids = direct(value, "id")
                if ids:
                    result.append({"id": str(ids[0]), "rows": value})
    return result


def parse_loc(text: str) -> dict[str, str]:
    loc: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r'^\s*([^\s:#]+):\d+\s+(".*")\s*$', line)
        if match:
            try:
                loc[match.group(1)] = json.loads(match.group(2))
            except json.JSONDecodeError:
                loc[match.group(1)] = match.group(2).strip('"')
    return loc


def ref_focuses(rows: list[tuple[str, str, Any]], key: str) -> set[str]:
    result: set[str] = set()
    for value in direct(rows, key):
        if isinstance(value, list):
            result.update(str(v) for name, _op, v in recursively(value) if name == "focus" and isinstance(v, str))
    return result


def effect_nodes(rows: list[tuple[str, str, Any]], key: str):
    return [value for name, _op, value in recursively(rows) if name == key and isinstance(value, list)]


def check(checks: list[dict[str, Any]], name: str, passed: bool, detail: Any = None, severity: str = "error") -> None:
    record = {"name": name, "status": "passed" if passed else severity}
    if detail is not None:
        record["detail"] = detail
    checks.append(record)


def main() -> int:
    checks: list[dict[str, Any]] = []
    generated: dict[str, str] = {}
    generated_loc: dict[str, str] = {}
    design: dict[str, Any] = {}
    import_error = None
    try:
        sys.path.insert(0, str(ROOT / "tools"))
        compiler = importlib.import_module("cyprus_1970_rework.compile")
        design, generated, generated_loc, _meta = compiler.generate()
        check(checks, "generator_import_and_pure_generation", True,
              {"generated_files": len(generated), "localisation_keys": len(generated_loc)})
    except Exception as exc:  # report the exact environment/generator failure
        import_error = f"{type(exc).__name__}: {exc}"
        check(checks, "generator_import_and_pure_generation", False, import_error)

    focus_path = "common/national_focus/COLDWAR_CYP_1970_focus.txt"
    actor_path = "common/national_focus/COLDWAR_CYP_R2_guarantor_focuses.txt"
    core_path = "common/scripted_effects/COLDWAR_CYP_R2_core.txt"
    core_trigger_path = "common/scripted_triggers/COLDWAR_CYP_R2_core.txt"
    crisis_effect_path = "common/scripted_effects/COLDWAR_CYP_R2_crisis.txt"
    crisis_trigger_path = "common/scripted_triggers/COLDWAR_CYP_R2_crisis.txt"
    crisis_event_path = "events/COLDWAR_CYP_R2_crisis.txt"
    decision_path = "common/decisions/COLDWAR_CYP_R2_crisis.txt"
    on_action_path = "common/on_actions/zzzzzz_COLDWAR_CYP_R2_on_actions.txt"
    loc_path = "localisation/english/COLDWAR_CYP_R2_l_english.yml"

    critical_paths = [focus_path, actor_path, core_path, core_trigger_path,
                      crisis_effect_path, crisis_trigger_path, crisis_event_path,
                      decision_path, on_action_path, loc_path]
    missing = [rel for rel in critical_paths if not (ROOT / rel).is_file()]
    check(checks, "required_runtime_files_present", not missing, missing)

    if not missing:
        focus_text = read_text(focus_path)
        actor_text = read_text(actor_path)
        core_text = read_text(core_path)
        core_trigger_text = read_text(core_trigger_path)
        crisis_effect_text = read_text(crisis_effect_path)
        crisis_trigger_text = read_text(crisis_trigger_path)
        crisis_event_text = read_text(crisis_event_path)
        decision_text = read_text(decision_path)
        on_action_text = read_text(on_action_path)
        loc_text = read_text(loc_path)
        loc = parse_loc(loc_text)

        cyprus_focuses = parse_tree_focuses(focus_text, {"focus"})
        actor_focuses = parse_tree_focuses(actor_text, {"shared_focus", "focus"})
        cyp_ids = {f["id"] for f in cyprus_focuses}
        actor_ids = {f["id"] for f in actor_focuses}
        check(checks, "cyprus_focus_count_100", len(cyprus_focuses) == 100,
              {"count": len(cyprus_focuses)})
        check(checks, "foreign_focus_ids_16_exact", actor_ids == EXPECTED_FOREIGN,
              {"count": len(actor_ids), "missing": sorted(EXPECTED_FOREIGN - actor_ids),
               "unexpected": sorted(actor_ids - EXPECTED_FOREIGN)})

        # Resolve every native prerequisite/exclusion and require symmetric exclusion edges.
        all_ids = cyp_ids | actor_ids
        focus_by_id = {f["id"]: f["rows"] for f in cyprus_focuses + actor_focuses}
        prereq_missing: list[str] = []
        exclusion_missing: list[str] = []
        asymmetric: list[str] = []
        anchor_missing: list[str] = []
        for fid, rows in focus_by_id.items():
            prereqs = ref_focuses(rows, "prerequisite")
            excludes = ref_focuses(rows, "mutually_exclusive")
            for ref in sorted(prereqs - all_ids):
                prereq_missing.append(f"{fid}->{ref}")
            for ref in sorted(excludes - all_ids):
                exclusion_missing.append(f"{fid}->{ref}")
            for ref in sorted(excludes & all_ids):
                other = focus_by_id.get(ref, [])
                if fid not in ref_focuses(other, "mutually_exclusive"):
                    asymmetric.append(f"{fid}<->{ref}")
            if fid in cyp_ids:
                for ref in direct(rows, "relative_position_id"):
                    if ref not in cyp_ids:
                        anchor_missing.append(f"{fid}->{ref}")

        native_focus_ids: set[str] = set()
        for host in ("common/national_focus/COLDWAR_GRE_1970_focus.txt",
                     "common/national_focus/mdcw_1970_generic_focus.txt"):
            if (ROOT / host).is_file():
                try:
                    native_focus_ids.update(f["id"] for f in parse_tree_focuses(read_text(host)))
                except Exception as exc:
                    anchor_missing.append(f"could not parse {host}: {exc}")
        known_anchors = all_ids | native_focus_ids
        for f in actor_focuses:
            for ref in direct(f["rows"], "relative_position_id"):
                if ref not in known_anchors:
                    anchor_missing.append(f"{f['id']}->{ref}")
        check(checks, "prerequisites_resolve", not prereq_missing, prereq_missing)
        check(checks, "exclusions_resolve", not exclusion_missing, exclusion_missing)
        check(checks, "exclusions_are_symmetric", not asymmetric, asymmetric)
        check(checks, "native_focus_anchors_resolve", not anchor_missing, anchor_missing)

        # Verify all R2 helper invocations in emitted files and wired external callers resolve.
        helper_definitions: set[str] = set()
        if generated:
            for rel, text in generated.items():
                if rel.startswith(("common/scripted_effects/", "common/scripted_triggers/")):
                    helper_definitions.update(re.findall(r"(?m)^\s*(COLDWAR_CYP_R2_\w+)\s*=\s*\{", text))
        helper_call_files = set(generated)
        helper_call_files.update({actor_path, focus_path, on_action_path,
                                  "history/countries/CYP - Cyprus.txt",
                                  "common/scripted_effects/00_leader_setup_scripted_effects.txt",
                                  "common/scripted_effects/00_money_system.txt",
                                  "common/scripted_effects/01_NATO_effects.txt",
                                  "common/ideas/Factions.txt"})
        external_unresolved: list[str] = []
        for rel in sorted(helper_call_files):
            path = ROOT / rel
            if not path.is_file():
                continue
            text = read_text(rel)
            for call in set(re.findall(r"\b(COLDWAR_CYP_R2_\w+)\s*=\s*yes\b", text)):
                if call not in helper_definitions:
                    external_unresolved.append(f"{rel}:{call}")
        check(checks, "emitted_and_external_helper_calls_resolve", not external_unresolved,
              {"definitions": len(helper_definitions), "unresolved": sorted(set(external_unresolved))})

        # Player-facing key references are required in the generated English localisation.
        missing_loc: list[str] = []
        for focus_id in cyp_ids | actor_ids:
            for key in (focus_id, focus_id + "_desc"):
                if key not in loc:
                    missing_loc.append(key)
        player_key_re = re.compile(
            r"\b(?:name|title|desc|tooltip|custom_[A-Za-z0-9_]*tooltip)\s*=\s*(COLDWAR_CYP_R2_[A-Za-z0-9_.]+)"
        )
        for rel in sorted(set(generated) | {actor_path, decision_path, crisis_event_path}):
            path = ROOT / rel
            if not path.is_file():
                continue
            for key in player_key_re.findall(read_text(rel)):
                if key not in loc:
                    missing_loc.append(f"{rel}:{key}")
        check(checks, "required_english_localisation_keys_exist", not missing_loc,
              sorted(set(missing_loc)))
        dash_keys = [key for key, value in loc.items() if "\u2013" in value or "\u2014" in value]
        german_chars = [key for key, value in loc.items() if re.search(r"[äöüÄÖÜß]", value)]
        check(checks, "player_text_uses_no_en_or_em_dash", not dash_keys, dash_keys)
        check(checks, "player_text_has_no_german_specific_characters", not german_chars, german_chars)
        generated_keys = sorted(set(generated_loc) - set(loc))
        check(checks, "generated_localisation_keys_present_installed", not generated_keys, generated_keys)

        # New code outputs must be UTF-8 without BOM and carry the project marker.
        generated_code = [p for p in generated if p.endswith((".txt", ".gui", ".gfx"))]
        marker_errors: list[str] = []
        bom_errors: list[str] = []
        for rel in generated_code:
            p = ROOT / rel
            if not p.is_file():
                marker_errors.append(f"missing:{rel}")
                continue
            raw = p.read_bytes()
            if raw.startswith(b"\xef\xbb\xbf"):
                bom_errors.append(rel)
            if not raw.decode("utf-8-sig").startswith("# IMPERIA COLD WAR"):
                marker_errors.append(rel)
        shared_custom = ["common/on_actions/zzzzzz_COLDWAR_CYP_R2_on_actions.txt",
                         "common/scripted_effects/01_NATO_effects.txt",
                         "common/ideas/Factions.txt",
                         "common/scripted_effects/00_money_system.txt",
                         "history/countries/CYP - Cyprus.txt"]
        for rel in shared_custom:
            if (ROOT / rel).is_file() and "IMPERIA COLD WAR" not in read_text(rel):
                marker_errors.append(f"custom_marker_absent:{rel}")
        check(checks, "generated_code_has_project_marker", not marker_errors, marker_errors)
        check(checks, "generated_code_is_utf8_without_bom", not bom_errors, bom_errors)
        loc_raw = (ROOT / loc_path).read_bytes()
        check(checks, "localisation_utf8_bom_and_marker_position",
              loc_raw.startswith(b"\xef\xbb\xbf") and loc_text.startswith("l_english:\n# IMPERIA COLD WAR"),
              {"bom": loc_raw.startswith(b"\xef\xbb\xbf"), "starts": loc_text[:70]})

        # Clausewitz parser and generated-vs-installed reproducibility.
        parse_errors = []
        if generated:
            for rel, text in generated.items():
                if not rel.endswith((".txt", ".gui", ".gfx")):
                    continue
                try:
                    get_rows(text)
                except Exception as exc:
                    parse_errors.append(f"generated:{rel}:{exc}")
        check(checks, "generated_scripts_parse", not parse_errors, parse_errors)
        mismatches: list[str] = []
        if generated:
            for rel, expected in generated.items():
                path = ROOT / rel
                if not path.is_file():
                    mismatches.append(f"missing:{rel}")
                elif read_text(rel) != expected:
                    mismatches.append(rel)
        check(checks, "generator_output_matches_installed_runtime", not mismatches,
              {"compared": len(generated), "mismatches": mismatches[:40], "mismatch_count": len(mismatches)})

        # Every scripted building action must grant its slots first, in the same state scope,
        # and remain beneath a one-time availability/receipt guard.
        core_rows = get_rows(core_text)
        state_records: list[dict[str, Any]] = []
        def scan_buildings(rows, parent_fn=""):
            for key, _op, value in rows:
                if not isinstance(value, list):
                    continue
                if key.isdigit() and any(k == "add_building_construction" for k, _o, _v in value):
                    slots_before: list[Any] = []
                    builds_seen = 0
                    constructions = [v for k, _o, v in value if k == "add_building_construction" and isinstance(v, list)]
                    for child_key, _child_op, child_value in value:
                        if child_key == "add_extra_state_shared_building_slots":
                            slots_before.append(child_value)
                        elif child_key == "add_building_construction":
                            builds_seen += 1
                            if len(slots_before) < builds_seen:
                                slots_before.append(0)
                    state_records.append({"state": key, "slots": slots_before, "constructions": constructions,
                                          "helper": parent_fn})
                scan_buildings(value, key if key.startswith(PREFIX) else parent_fn)
        scan_buildings(core_rows)
        bad_buildings: list[str] = []
        for record in state_records:
            constructions = record["constructions"]
            slots = record["slots"]
            if len(slots) < len(constructions):
                bad_buildings.append(f"state {record['state']} missing slot grant before each build")
            for block in constructions:
                levels = int(direct(block, "level")[0]) if direct(block, "level") else 1
                if not any(int(slot) >= levels for slot in slots if str(slot).isdigit()):
                    bad_buildings.append(f"state {record['state']} slot count below level count")
        building_actions = len(state_records)
        check(checks, "building_slot_grants_precede_construction", bool(state_records) and not bad_buildings,
              {"state_actions": building_actions, "errors": bad_buildings})
        building_focuses = [f for f in design.get("focuses", []) if any(e.get("type") == "building" for e in f.get("effects", []))]
        building_guard_errors: list[str] = []
        trigger_rows = get_rows(core_trigger_text)
        trigger_defs = {key: value for key, _op, value in recursively(trigger_rows)
                        if key.endswith("_available") and isinstance(value, list)}
        execution_defs = {key: value for key, _op, value in recursively(trigger_rows)
                          if key.endswith("_execution_valid") and isinstance(value, list)}
        for f in building_focuses:
            for e in f.get("effects", []):
                if e.get("type") != "building":
                    continue
                guard = e.get("guards", {})
                tid = f.get("id", "")
                trigger = trigger_defs.get(tid + "_available", [])
                exec_trigger = execution_defs.get(tid + "_execution_valid", [])
                trigger_tokens = {key for key, _op, _value in recursively(trigger)}
                trigger_text = " ".join(f"{key} {op} {value}" for key, op, value in recursively(trigger))
                exec_text = " ".join(f"{key} {op} {value}" for key, op, value in recursively(exec_trigger))
                state = str(e.get("state"))
                building = str(e.get("building"))
                cap_guard_present = (f"building_level@{building}" in trigger_text
                                     or "has_building_construction" in trigger_tokens
                                     or "any_province_building_level" in trigger_tokens)
                transaction_guard_present = "_enacted" in exec_text and "has_country_flag" in exec_text
                if (guard.get("owner") != "CYP" or guard.get("controller") != "CYP"
                        or not guard.get("native_building_cap") or not guard.get("slot_before_building")
                        or f"owns_state = {state}" not in trigger_text
                        or f"controls_state = {state}" not in trigger_text
                        or not cap_guard_present or not transaction_guard_present):
                    building_guard_errors.append(f.get("id", f.get("key", "?")))
        check(checks, "building_ownership_control_capacity_and_transaction_guards", not building_guard_errors,
              {"building_focuses": len(building_focuses), "missing_guard": building_guard_errors})

        # Decisions remain confined to the four finite Turkey army actions.
        decision_rows = get_rows(decision_text)
        decision_defs = [key for key, _op, val in recursively(decision_rows)
                         if key.startswith("COLDWAR_CYP_R2_army_") and isinstance(val, list)]
        stray_decisions = []
        for path in (ROOT / "common/decisions").rglob("*.txt"):
            if path == ROOT / decision_path:
                continue
            text = path.read_text(encoding="utf-8-sig")
            if re.search(r"(?m)^\s*(?:CYP_decisions|COLDWAR_CYP_1970_[A-Za-z0-9_]*decision)\s*=\s*\{", text):
                stray_decisions.append(path.relative_to(ROOT).as_posix())
        check(checks, "only_four_turkish_crisis_decisions", set(decision_defs) == TURKISH_DECISIONS and not stray_decisions,
              {"count": len(decision_defs), "unexpected": sorted(set(decision_defs) - TURKISH_DECISIONS),
               "missing": sorted(TURKISH_DECISIONS - set(decision_defs)), "legacy_cyprus_menus": stray_decisions})

        # Fixed-tag monthly transition observation only; native weekly streams must only read cached flags.
        lower_actions = on_action_text.lower()
        periodic_errors = []
        if re.search(r"\bon_daily\b|\bon_weekly\b", lower_actions):
            periodic_errors.append("daily/weekly on_action exists")
        if "every_country" in on_action_text:
            periodic_errors.append("all-country polling in on_actions")
        if re.search(r"enable_mod\s*=|has_game_rule\s*=\s*\{\s*rule\s*=\s*enable", "\n".join((core_text, core_trigger_text, crisis_effect_text, crisis_trigger_text, on_action_text)), re.I):
            periodic_errors.append("enable-mod polling or gate appears in feature runtime")
        if "on_monthly" not in on_action_text or "COLDWAR_CYP_R2_monthly = yes" not in on_action_text:
            periodic_errors.append("fixed-tag monthly dispatch missing")
        weekly_body = crisis_effect_text.split("COLDWAR_CYP_R2_crisis_weekly_streams = {", 1)[-1].split("\n}", 1)[0]
        if re.search(r"has_war|has_idea|country_exists|every_country|any_country", weekly_body):
            periodic_errors.append("weekly crisis stream performs relationship/eligibility polling")
        if not all(token in weekly_body for token in ("COLDWAR_CYP_R2_intervention_expense_cached", "COLDWAR_CYP_R2_volunteer_expense_active")):
            periodic_errors.append("weekly stream misses cached expense flags")
        check(checks, "monthly_only_reconciliation_and_cached_weekly_streams", not periodic_errors,
              periodic_errors)

        # Native defects already known from the first engine log remain explicit regression guards.
        invalid_effects = len(re.findall(r"\bremove_country_flag\s*=", crisis_effect_text + crisis_event_text))
        invalid_any_limit = bool(re.search(r"any_country\s*=\s*\{\s*limit\s*=", crisis_trigger_text + crisis_effect_text))
        nested_math = len(re.findall(r"\{\s*value\s*=\s*[^{}]+\s+multiply\s*=", crisis_effect_text + decision_text))
        check(checks, "crisis_native_flag_clear_effects", invalid_effects == 0, {"invalid_remove_country_flag": invalid_effects})
        check(checks, "crisis_any_country_trigger_shape", not invalid_any_limit, {"invalid_limit_wrapper": invalid_any_limit})
        check(checks, "crisis_uses_sequential_math_effects", nested_math == 0, {"nested_inline_math": nested_math})

        idea_text = read_text("common/ideas/COLDWAR_CYP_R2_crisis_ideas.txt") if (ROOT / "common/ideas/COLDWAR_CYP_R2_crisis_ideas.txt").is_file() else ""
        volunteer_lifecycle_ok = all(fragment in idea_text for fragment in (
            "COLDWAR_CYP_R2_cyprus_volunteer_mission", "rule = { can_send_volunteers = yes }",
            "add_relation_rule_override = { target = CYP can_send_volunteers = yes }",
            "remove_relation_rule_override = { target = CYP can_send_volunteers = yes }"))
        volunteer_helper = "".join((crisis_effect_text, crisis_event_text))
        false_unit_grant = bool(re.search(r"\b(?:create_unit|create_division|add_units)\s*=", volunteer_helper))
        check(checks, "volunteer_native_permission_lifecycle_without_fake_units",
              volunteer_lifecycle_ok and not false_unit_grant,
              {"permission_lifecycle": volunteer_lifecycle_ok, "scripted_unit_grant": false_unit_grant})

    report = {
        "project": "IMPERIA COLD WAR",
        "validator": "tools/cyprus_1970_rework/validate.py",
        "scope": "static installed-runtime and generator consistency; no runtime writes",
        "source_sha256": {},
        "status": "passed" if all(item["status"] == "passed" for item in checks) else "findings",
        "checks": checks,
    }
    for rel in critical_paths:
        path = ROOT / rel
        if path.is_file():
            report["source_sha256"][rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    if import_error:
        report["generator_error"] = import_error
    out = HERE / "VALIDATION_REPORT.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    failed = sum(item["status"] != "passed" for item in checks)
    print(json.dumps({"status": report["status"], "checks": len(checks), "failed": failed,
                      "report": str(out.relative_to(ROOT)),
                      "failed_names": [item["name"] for item in checks if item["status"] != "passed"]},
                     ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
