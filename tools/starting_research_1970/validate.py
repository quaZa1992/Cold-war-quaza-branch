# IMPERIA COLD WAR — Independent January 1970 research preservation and behavior checks.
"""Validate the bounded research change, using --preview before runtime application."""

import argparse
import collections
import hashlib
import itertools
import json
import re
import sys
import traceback
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import build
from catalog import catalogue, first, parse

PROJECT = "IMPERIA COLD WAR"
DLCS = ("No Step Back", "By Blood Alone", "Gotterdammerung")
NEW_FLAG = "COLDWAR_1970_world_research_assigned"
APPLIED_FLAGS = {NEW_FLAG, "mdcw_1970_air_research_applied", "mdcw_1970_infantry_research_applied"}
MARKER = "# IMPERIA COLD WAR — January 1970 researched national technology baseline."
BEGIN, END = MARKER + " BEGIN", MARKER + " END"
VARIANT_MARKER = "# IMPERIA COLD WAR — January 1970 historical equipment variants."
VARIANT_BEGIN, VARIANT_END = VARIANT_MARKER + " BEGIN", VARIANT_MARKER + " END"
COMPONENT_PATH = ROOT / "common/technologies/COLDWAR_1970_service_components.txt"
DISPATCHERS = {
    "mdcw_apply_1970_air_research": "mdcw_1970_air_research_effects.txt",
    "mdcw_apply_1970_infantry_research": "mdcw_1970_infantry_research_effects.txt",
}
NEW_DATE_TAGS = {"KPI", "KPS", "KPT"}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def scalar(value):
    return value[1:-1] if isinstance(value, str) and value.startswith('"') and value.endswith('"') else value


def rows_for(rows, key):
    return [value for name, operator, value in rows if name == key]


def day(value):
    return tuple(int(part) for part in scalar(value).split("."))


def compare(left, operator, right):
    return {"=": lambda: left == right, "!=": lambda: left != right,
            "<": lambda: left < right, ">": lambda: left > right,
            "<=": lambda: left <= right, ">=": lambda: left >= right}[operator]()


class State:
    def __init__(self, tag, dlcs, scenario=True, flags=(), techs=()):
        self.tag, self.dlcs, self.scenario = tag, set(dlcs), scenario
        self.flags, self.techs = set(flags), set(techs)
        self.date = (1970, 1, 1) if scenario else (2000, 1, 1)
        self.grant_count = collections.Counter()


def condition(rows, state):
    """Small trigger interpreter, independent of compiler selection logic."""
    for key, operator, value in rows:
        if key in ("AND", "limit"):
            result = condition(value, state)
        elif key == "NOT":
            result = not condition(value, state)
        elif key == "OR":
            result = any(condition([row], state) for row in value)
        elif key == "has_dlc":
            result = scalar(value) in state.dlcs
        elif key == "IMP_is_1970_scenario":
            result = state.scenario == (value == "yes")
        elif key == "has_country_flag":
            result = scalar(value) in state.flags
        elif key == "has_tech":
            result = scalar(value) in state.techs
        elif key in ("original_tag", "tag"):
            result = compare(state.tag, operator, scalar(value))
        elif key == "date":
            result = compare(state.date, operator, day(value))
        elif key == "always":
            result = value == "yes"
        else:
            raise ValueError(f"Unsupported model trigger: {key}")
        if not result:
            return False
    return True


def execute(rows, state):
    """Allow only monotonic grants, flags and native conditional control flow."""
    previous_if = None
    for key, operator, value in rows:
        if key == "limit":
            continue
        if key == "if":
            previous_if = condition(first(value, "limit", []), state)
            if previous_if:
                execute(value, state)
        elif key == "else_if":
            if previous_if is None:
                raise ValueError("else_if without preceding if")
            if not previous_if and condition(first(value, "limit", []), state):
                execute(value, state)
                previous_if = True
        elif key == "else":
            if previous_if is None:
                raise ValueError("else without preceding if")
            if not previous_if:
                execute(value, state)
            previous_if = None
        elif key == "set_country_flag":
            state.flags.add(scalar(value))
            previous_if = None
        elif key == "set_technology":
            for tech, assignment, level in value:
                if tech == "popup":
                    if level != "no":
                        raise ValueError("Research popup not suppressed")
                    continue
                if assignment != "=" or level != "1":
                    raise ValueError(f"Non-monotonic technology assignment: {tech} {assignment} {level}")
                state.techs.add(tech)
                state.grant_count[tech] += 1
            previous_if = None
        else:
            raise ValueError(f"Unexpected generated effect: {key}")


def dlc_condition(rows, dlcs):
    """Evaluate only DLC-dependent branch restrictions, leaving other gates unknown."""
    results = []
    for key, operator, value in rows:
        if key == "has_dlc":
            result = scalar(value) in dlcs
        elif key in ("AND", "NOT", "OR"):
            children = [dlc_condition([row], dlcs) for row in value]
            if key == "OR":
                result = True if True in children else (None if None in children else False)
            else:
                result = False if False in children else (None if None in children else True)
                if key == "NOT" and result is not None:
                    result = not result
        else:
            result = None
        results.append(result)
    return False if False in results else (None if None in results else True)


def path_predecessor_gaps(technologies, known, dlcs, available):
    """Independently inspect incoming native paths, including cumulative forks."""
    incoming = collections.defaultdict(set)
    for parent, record in technologies.items():
        for child in record.get("paths", []):
            if child in technologies and available(record, dlcs):
                incoming[child].add(parent)
    gaps = []
    for child in sorted(known):
        candidates = incoming[child]
        cumulative = {parent for parent in candidates if not technologies[parent].get("xor")}
        gaps.extend((child, parent) for parent in sorted(cumulative-known))
        if candidates and not cumulative and not candidates & known:
            gaps.append((child, tuple(sorted(candidates))))
    return gaps


def without_new_guard(rows):
    guard = [("has_country_flag", "=", NEW_FLAG)]
    return [(key, operator, without_new_guard(value) if isinstance(value, list) else value)
            for key, operator, value in rows if not (key == "NOT" and value == guard)]


def extract_block(source):
    if source.count(BEGIN) != 1 or source.count(END) != 1:
        raise ValueError("Expected exactly one research block")
    start, end = source.index(BEGIN), source.index(END)
    if end <= start:
        raise ValueError("Research block markers reversed")
    body_start = source.index("\n", start) + 1
    return source[body_start:end], source[:start] + source[end + len(END):]


def remove_variant_block(source):
    if source.count(VARIANT_BEGIN) != 1 or source.count(VARIANT_END) != 1:
        raise ValueError("Expected exactly one separately validated historical variant block")
    start, end = source.index(VARIANT_BEGIN), source.index(VARIANT_END)
    if end <= start:
        raise ValueError("Variant block markers reversed")
    return source[:start] + source[end + len(VARIANT_END):]


def augment_rendered_technologies(outputs, technologies, require):
    """Parse pending hidden component definitions independently of compiler metadata."""
    source = outputs.get(COMPONENT_PATH)
    if source is None:
        return set()
    definitions = first(parse(source), "technologies", [])
    names, component_sets = set(), set()
    for name, operator, rows in definitions:
        require(name not in names, "unique_service_component_bundle", technology=name)
        names.add(name)
        fields = {key for key, op, value in rows}
        require(fields <= {"allow", "allow_branch", "research_cost", "start_year", "enable_equipment_modules", "enable_equipments", "ai_will_do"},
                "service_bundle_only_enables_exact_components_and_reviewed_bare_types", technology=name, fields=sorted(fields))
        require(first(rows, "allow") == [("always", "=", "no")] and first(rows, "start_year") == "1969",
                "component_bundle_hidden_nonresearchable_pre1970", technology=name)
        components = [value for key, op, value in first(rows, "enable_equipment_modules", []) if key == "_bare"]
        bare_types = [value for key, op, value in first(rows, "enable_equipments", []) if key == "_bare"]
        branch = first(rows, "allow_branch", [])
        valid_branches = [[]] + [[("has_dlc", "=", '"'+dlc+'"')] for dlc in DLCS] + [[("NOT", "=", [("has_dlc", "=", '"'+dlc+'"')])] for dlc in DLCS]
        require(branch in valid_branches, "service_bundle_only_simple_dlc_branch_guard", technology=name, branch=branch)
        signature = (tuple(sorted(components)), tuple(sorted(bare_types)), json.dumps(branch))
        require(bool(components or bare_types) and len(components) == len(set(components)) and len(bare_types) == len(set(bare_types)), "service_bundle_has_exact_unique_native_content", technology=name)
        require(signature not in component_sets, "component_sets_deduplicated", technology=name)
        component_sets.add(signature)
        technologies[name] = {"file": COMPONENT_PATH.relative_to(ROOT).as_posix(), "year": 1969,
                              "folders": [], "categories": [], "paths": [], "xor": [], "dependencies": [],
                              "allow": first(rows, "allow"), "allow_branch": branch, "doctrine": None,
                              "enable_equipments": bare_types, "enable_equipment_modules": components, "special_projects": []}
    return names


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", action="store_true", help="Validate compiler output without requiring an installed runtime change")
    args = parser.parse_args()
    diagnostics, checks = [], collections.Counter()
    report = {"project": PROJECT, "feature": "Independent worldwide January 1970 research validation",
              "mode": "preview" if args.preview else "installed", "command": [sys.executable, *sys.argv],
              "created_utc": datetime.now(timezone.utc).isoformat(), "status": "running",
              "evidence_level": "Source parsing, archived semantic comparison and bounded script model; no live engine or multiplayer validation."}

    def fail(category, **details):
        diagnostics.append({"severity": "error", "category": category, **details})

    def warning(category, **details):
        diagnostics.append({"severity": "warning", "category": category, **details})

    def require(test, category, **details):
        checks[category] += 1
        if not test:
            fail(category, **details)
        return bool(test)

    try:
        fixture = {
            "foundation": {"paths": ["intermediate", "advanced"], "xor": []},
            "intermediate": {"paths": ["advanced"], "xor": []},
            "advanced": {"paths": [], "xor": []},
        }
        require(("advanced", "intermediate") in path_predecessor_gaps(fixture, {"foundation", "advanced"}, set(), lambda row, dlcs: True),
                "negative_control_shortcut_cannot_hide_missing_intermediate")
        branches = {
            "rifle_a": {"paths": ["later"], "xor": ["rifle_b"]},
            "rifle_b": {"paths": ["later"], "xor": ["rifle_a"]},
            "later": {"paths": [], "xor": []},
        }
        require(not path_predecessor_gaps(branches, {"rifle_a", "later"}, set(), lambda row, dlcs: True),
                "xor_predecessors_remain_alternatives")
        require(bool(path_predecessor_gaps(branches, {"later"}, set(), lambda row, dlcs: True)),
                "negative_control_missing_entire_alternative_branch")
        expected, manifest = build.outputs()
        techs, duplicates = catalogue()
        require(not duplicates, "duplicate_technology_definitions", ids=duplicates)
        component_bundles = augment_rendered_technologies(expected, techs, require)
        variant_tags = {tag for tag, record in manifest.items()
                        if VARIANT_BEGIN in expected[ROOT / record["history_file"]]}
        if variant_tags:
            require(variant_tags == set(manifest), "variant_blocks_cover_all_countries", missing=sorted(set(manifest)-variant_tags))
        history_files = {p.stem[:3]: p for p in (ROOT / "history/countries").glob("*.txt")}
        require(len(history_files) == len(manifest) == 400 and set(history_files) == set(manifest),
                "exact_country_coverage", actual_files=len(history_files), profiles=len(manifest),
                missing=sorted(set(history_files) - set(manifest)), extra=sorted(set(manifest) - set(history_files)))
        require(len(expected) == 402 + int(COMPONENT_PATH in expected), "bounded_output_scope", outputs=len(expected))
        baseline = json.loads((HERE / "before_hashes.json").read_text(encoding="utf-8"))
        require(baseline.get("project") == PROJECT, "baseline_project_identifier")
        archive_path = Path(baseline["archive"])
        require(archive_path.is_file(), "archive_present", path=str(archive_path))
        originals = {}
        with zipfile.ZipFile(archive_path) as archive:
            require(len(archive.namelist()) == 402, "archive_entry_count", actual=len(archive.namelist()))
            for rel, recorded_hash in baseline["before_sha256"].items():
                raw = archive.read(rel)
                require(sha(raw) == recorded_hash, "archive_hash_preservation", path=rel)
                originals[rel] = raw.decode("utf-8-sig")
        report["archive"] = str(archive_path)
        report["archive_sha256"] = sha(archive_path.read_bytes())
        report["compiler_sources_sha256"] = {p.name: sha(p.read_bytes()) for p in (HERE / "build.py", HERE / "catalog.py", *[HERE / name for name in build.PROFILE_FILES])}
        allowed_outputs = set(baseline["before_sha256"]) | ({COMPONENT_PATH.relative_to(ROOT).as_posix()} if COMPONENT_PATH in expected else set())
        require({path.relative_to(ROOT).as_posix() for path in expected} == allowed_outputs,
                "exact_bounded_runtime_paths")
        chosen_sources = {}
        for path, rendered in expected.items():
            rel = path.relative_to(ROOT).as_posix()
            raw = rendered.encode("utf-8") if args.preview else path.read_bytes()
            require(raw == rendered.encode("utf-8"), "compiler_output_matches", path=rel)
            require(not raw.startswith(b"\xef\xbb\xbf"), "utf8_without_bom", path=rel)
            source = raw.decode("utf-8")
            require(source.startswith("# IMPERIA COLD WAR — "), "file_start_project_marker", path=rel)
            require(not re.search(r"(?m)^(<<<<<<<|=======|>>>>>>>)", source), "no_conflict_markers", path=rel)
            parse(source)
            checks["runtime_parse"] += 1
            chosen_sources[rel] = source

        definitions = {}
        for effect, name in DISPATCHERS.items():
            rel = "common/scripted_effects/" + name
            actual = parse(chosen_sources[rel])
            prior = parse(originals[rel])
            require(without_new_guard(actual) == prior, "legacy_effect_semantics_preserved", path=rel)
            effect_rows = first(actual, effect)
            limit = first(first(effect_rows, "if", []), "limit", [])
            new_guard = ("NOT", "=", [("has_country_flag", "=", NEW_FLAG)])
            require(new_guard in limit, "new_flag_suppresses_legacy_dispatcher", effect=effect)
            def guard_count(rows):
                return sum(int((key, operator, value) == new_guard) + (guard_count(value) if isinstance(value, list) else 0)
                           for key, operator, value in rows)
            require(guard_count(actual) == 1, "only_one_approved_legacy_dispatcher_guard", effect=effect)
            definitions[effect] = effect_rows
            definitions.update({key: value for key, operator, value in actual if isinstance(value, list)})

        trigger_path = ROOT / "common/scripted_triggers/IMP_cold_war_scenario_triggers.txt"
        trigger = first(parse(trigger_path.read_text(encoding="utf-8-sig")), "IMP_is_1970_scenario")
        require(trigger == [("has_start_date", ">", "1969.12.31"), ("has_start_date", "<", "1970.1.2")],
                "scenario_gate_uses_stable_bookmark", trigger=trigger)
        no_prior_date = set()
        preserved_duplicate_dates = {}
        per_country = {}
        exceptional_dates = []
        unique_techs = set()
        for tag, row in sorted(manifest.items()):
            rel = row["history_file"]
            source = chosen_sources[rel]
            own_source, stripped = extract_block(source)
            if tag in variant_tags:
                stripped = remove_variant_block(stripped)
            own_rows = parse(own_source)
            before_rows, after_rows = parse(originals[rel]), parse(stripped)
            prior_dates = rows_for(before_rows, "1970.1.1")
            if not prior_dates:
                no_prior_date.add(tag)
                require(tag in NEW_DATE_TAGS, "only_approved_new_date_blocks", tag=tag)
                require(rows_for(after_rows, "1970.1.1") == [[]], "new_date_block_contains_only_research", tag=tag)
                after_rows = [entry for entry in after_rows if entry[0] != "1970.1.1"]
            require(before_rows == after_rows, "all_unrelated_history_semantics_preserved", tag=tag)
            dates = rows_for(parse(source), "1970.1.1")
            expected_dates = max(1, len(prior_dates))
            require(len(dates) == expected_dates and dates[0][:len(own_rows)] == own_rows,
                    "research_precedes_old_initializers", tag=tag, actual_date_blocks=len(dates),
                    baseline_date_blocks=len(prior_dates))
            if len(prior_dates) > 1:
                preserved_duplicate_dates[tag] = len(prior_dates)
            require(len(own_rows) == 1 and own_rows[0][0] == "if" and first(own_rows[0][2], "limit") == [("IMP_is_1970_scenario", "=", "yes")],
                    "generated_block_is_scenario_only", tag=tag)

            group_sets = {key: set(values) for key, values in row["technology_groups"].items()}
            all_requested = set().union(*group_sets.values())
            for key in sorted(all_requested):
                if not require(key in techs, "valid_technology_id", tag=tag, technology=key):
                    continue
                year = techs[key]["year"]
                exception = row.get("dated_exceptions", {}).get(key)
                require(year is None or year <= 1969 or bool(exception), "technology_not_after_cutoff", tag=tag, technology=key, year=year, exception=exception)
                if year is not None and year >= 1970:
                    exceptional_dates.append({"tag": tag, "technology": key, "year": year, "reason": exception})
            counts = []
            for nsb, bba, got in itertools.product((False, True), repeat=3):
                dlcs = {name for name, enabled in zip(DLCS, (nsb, bba, got)) if enabled}
                expected_set = group_sets["common"] | group_sets["nsb" if nsb else "legacy"] | group_sets["bba" if bba else "non_bba"] | group_sets["got" if got else "non_got"]
                label = "+".join(sorted(dlcs)) or "none"
                state = State(tag, dlcs)
                execute(own_rows, state)
                require(state.techs == expected_set, "independent_grant_interpreter", tag=tag, dlcs=label, missing=sorted(expected_set-state.techs), extra=sorted(state.techs-expected_set))
                require(state.flags == APPLIED_FLAGS, "assignment_flags_set", tag=tag, dlcs=label, flags=sorted(state.flags))
                require(all(count == 1 for count in state.grant_count.values()), "no_duplicate_active_grants", tag=tag, dlcs=label)
                from tools.starting_research_1970.validate_variants import active_technology
                gaps = path_predecessor_gaps(techs, state.techs, dlcs, active_technology)
                require(not gaps, "complete_active_native_path_predecessors", tag=tag, dlcs=label, missing=gaps)
                grant_order={key:index for index,key in enumerate(state.grant_count)}
                late=[]
                for parent,record in techs.items():
                    if parent not in state.techs:continue
                    for child in record.get('paths',[]):
                        if child in state.techs and grant_order[parent]>grant_order[child]:late.append((parent,child))
                for child in state.techs:
                    late.extend((parent,child) for parent in techs[child]['dependencies'] if parent in state.techs and grant_order[parent]>grant_order[child])
                require(not late,"prerequisites_granted_before_descendants",tag=tag,dlcs=label,late=late)
                unique_techs.update(state.techs)
                for key in sorted(state.techs):
                    record = techs[key]
                    require(dlc_condition(record["allow_branch"], dlcs) is not False, "native_dlc_branch_respected", tag=tag, technology=key, dlcs=label)
                    missing = sorted(set(record["dependencies"]) - state.techs)
                    require(not missing, "hard_technology_dependencies_present", tag=tag, technology=key, missing=missing, dlcs=label)
                    conflicts = sorted(set(record["xor"]) & state.techs)
                    require(not conflicts, "no_mutually_exclusive_technology_conflicts", tag=tag, technology=key, conflicts=conflicts, dlcs=label)
                snapshot = (set(state.techs), set(state.flags))
                execute(own_rows, state)
                require((state.techs, state.flags) == snapshot, "repeated_history_model_is_idempotent", tag=tag, dlcs=label)
                state.techs.add("__future_research_progress_sentinel__")
                execute(own_rows, state)
                require(state.techs == snapshot[0] | {"__future_research_progress_sentinel__"}, "replay_preserves_future_research_progress", tag=tag, dlcs=label)
                outside = State(tag, dlcs, scenario=False, flags={"__existing_flag__"}, techs={"__existing_technology__"})
                execute(own_rows, outside)
                require(outside.techs == {"__existing_technology__"} and outside.flags == {"__existing_flag__"}, "later_bookmark_receives_no_1970_grants", tag=tag, dlcs=label)
                for effect in DISPATCHERS:
                    suppressed = State(tag, dlcs, flags={NEW_FLAG}, techs=snapshot[0])
                    execute(definitions[effect], suppressed)
                    require(suppressed.techs == snapshot[0] and suppressed.flags == {NEW_FLAG}, "legacy_dispatcher_suppressed_without_old_flag", tag=tag, effect=effect, dlcs=label)
                inherited = State(tag, dlcs, flags=snapshot[1], techs=snapshot[0])
                execute(definitions["mdcw_inherit_jet_generation_research"], inherited)
                require(inherited.techs == snapshot[0], "startup_air_inheritance_adds_no_unplanned_technology", tag=tag, dlcs=label, extra=sorted(inherited.techs-snapshot[0]))
                counts.append(len(snapshot[0]))
            per_country[tag] = {"history_file": rel, "semantics_preserved": before_rows == after_rows,
                                "technology_count_min": min(counts), "technology_count_max": max(counts),
                                "dlc_combinations": 8, "output_sha256": sha(source.encode("utf-8"))}
        require(no_prior_date == NEW_DATE_TAGS, "exact_three_new_1970_blocks", tags=sorted(no_prior_date))
        if variant_tags:
            # Stripping the second block is permitted only with its independent
            # native fitting, ordering, DLC and replay validator executed here.
            from tools.starting_research_1970.validate_variants import main as validate_equipment
            variant_result = validate_equipment(["--preview"] if args.preview else [])
            require(variant_result == 0, "independent_variant_behavior_and_fitting_passed",
                    report="tools/starting_research_1970/variant_validation.json")
        for path in (HERE / "build.py", HERE / "catalog.py", HERE / "prerequisites.py", Path(__file__)):
            raw = path.read_bytes()
            require(raw.startswith("# IMPERIA COLD WAR — ".encode("utf-8")) and not raw.startswith(b"\xef\xbb\xbf"), "tool_marker_and_encoding", path=path.relative_to(ROOT).as_posix())
        warning("native_engine_not_run", detail="These are deterministic source/model checks, not a live save-load or multiplayer run.")
        warning("inherited_technology_granularity", detail="Coarse existing MD nodes may bundle components or retain later country-specific display names. The research source records distinguish these abstractions from exact equipment introduction dates.")
        report.update({"countries": len(manifest), "runtime_outputs": len(expected), "dlc_combinations": len(manifest)*8,
                       "selected_unique_technology_ids": len(unique_techs), "dated_exceptions": exceptional_dates,
                       "historical_variant_blocks_checked": len(variant_tags), "component_bundles_checked": len(component_bundles),
                       "preserved_baseline_duplicate_1970_date_blocks": preserved_duplicate_dates,
                       "countries_checked": per_country})
    except Exception as error:
        fail("validation_exception", type=type(error).__name__, message=str(error), traceback=traceback.format_exc())
    errors = sum(item["severity"] == "error" for item in diagnostics)
    report.update({"status": "passed" if not errors else "failed", "error_count": errors,
                   "warning_count": sum(item["severity"] == "warning" for item in diagnostics),
                   "check_counts": dict(sorted(checks.items())), "diagnostics": diagnostics,
                   "finished_utc": datetime.now(timezone.utc).isoformat()})
    (HERE / "validation.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: report.get(key) for key in ("project", "mode", "status", "countries", "dlc_combinations", "error_count", "warning_count")}))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
