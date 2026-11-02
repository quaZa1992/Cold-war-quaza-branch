# IMPERIA COLD WAR — End-to-end verification of the dated history data and period labels.
import hashlib
import json
from pathlib import Path
import re
import sys
from implement import HERE, ROOT, PENDING, read_json, keyed, build_profiles, plan_changes
from history_patch import BEGIN, END, strip_profile, date_blocks

sys.path.insert(0, str(ROOT / "tools/spain_1970_v2"))
from script_ast import parse, first, walk
from test_history_patch import run_profile


def main():
    inventory, profiles = build_profiles()
    plan, files = plan_changes(inventory, profiles)
    assert not plan, "History is not synchronized with research; run implement.py --apply"
    checks = 0
    registries = {}
    for part, name in (("currency", "currency.json"), ("religion", "religion.json"), ("factions", "factions.json")):
        doc = read_json(name)
        registries[part] = doc.get("sources", doc.get("source_registry"))
        for record in keyed(doc).values():
            for source in record.get("source_ids", []):
                assert source in registries[part], (part, source)
                checks += 1
    forbidden_effects = {"every_country", "every_state", "every_owned_state", "random", "random_list", "country_event", "ingame_update_setup", "add_to_array", "resize_array", "add_to_variable"}
    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    total_blocks = 0
    for entry in inventory["countries"]:
        tag = entry["tag"]
        raw = (ROOT / entry["path"]).read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), entry["path"]
        assert hashlib.sha256(strip_profile(raw.decode("utf-8")).encode("utf-8")).hexdigest() == entry["sha256"], tag
        checks += 2
        if tag in PENDING:
            assert hashlib.sha256(raw).hexdigest() == entry["sha256"], tag
            assert BEGIN not in raw.decode("utf-8"), tag
            checks += 2
            continue
        profile = profiles[tag]
        source = raw.decode("utf-8")
        blocks = pattern.findall(source)
        assert len(blocks) == entry["snapshot_count"], tag
        assert len(set(blocks)) == 1, (tag, "same-date profiles differ")
        total_blocks += len(blocks)
        rows = parse(blocks[0])
        assert len(rows) == 1 and rows[0][0] == "if", tag
        assert first(rows[0][2], "limit") == [("IMP_is_1970_scenario", "=", "yes")], tag
        assert not forbidden_effects.intersection(k for k, _, _ in walk(rows)), tag
        assert "currency_strength" not in blocks[0], tag
        assert not re.findall(r"(?<![\w.])-?\d+\.\d{6,}(?![\w.])", blocks[0]), tag
        checks += 7
        groups = profile["factions"]
        initial = {groups[0] + "_opinion": 0, groups[1] + "_opinion": 73}
        for part, ids in profile["source_ids"].items():
            assert all(source_id in registries[part] for source_id in ids), (tag, part)
            checks += 1
        ideas, values = run_profile(rows, 1970, variables=initial)
        assert {profile["currency"], profile["religion"], *groups}.issubset(ideas), tag
        assert values["no_foreign_reserve"] == profile["no_foreign_reserve"], tag
        assert values[groups[0] + "_opinion"] == 0, tag
        assert values[groups[1] + "_opinion"] == 73, tag
        assert values[groups[2] + "_opinion"] == 50, tag
        assert run_profile(rows, 1970, ideas, values) == (ideas, values), tag
        checks += 6
        for year in (1985, 2000, 2017):
            original_ideas = {"sunni", "euro"}
            assert run_profile(rows, year, original_ideas, initial) == (original_ideas, initial), (tag, year)
            checks += 1
    labels = read_json("labels.json")
    assert hashlib.sha256((ROOT / labels["native_source"]).read_bytes()).hexdigest() == labels["native_source_sha256"]
    code_path = ROOT / "common/scripted_localisation/COLDWAR_1970_internal_faction_names.txt"
    loc_path = ROOT / "localisation/english/replace/COLDWAR_1970_internal_faction_names_l_english.yml"
    assert not code_path.read_bytes().startswith(b"\xef\xbb\xbf")
    assert loc_path.read_bytes().startswith(b"\xef\xbb\xbf")
    code = parse(code_path.read_text(encoding="utf-8"))
    functions = {first(v, "name"): v for k, _, v in code if k == "defined_text"}
    loc = loc_path.read_text(encoding="utf-8-sig")
    assert loc.startswith("l_english:")
    for row in labels["rows"]:
        body = functions[row["function"]]
        choices = [v for k, _, v in body if k == "text"]
        assert first(choices[0], "trigger") == parse(row["historical_condition"])
        assert first(choices[0], "trigger")[0] == ("IMP_is_1970_scenario", "=", "yes")
        if row["tag"] == "PER":
            assert "PER_IMPERIAL_1970" in row["historical_condition"]
            assert "emerging_moderate_shiite_are_in_power" in row["historical_condition"]
            assert "emerging_hardline_shiite_are_in_power" in row["historical_condition"]
        assert first(choices[0], "localization_key") == row["historical_key"]
        assert first(choices[1], "localization_key") == row["fallback_key"]
        assert row["key"] + ': "[' + row["function"] + ']"' in loc
        assert row["fallback_key"] + ": " + row["fallback_quoted"] in loc
        assert all(s in registries["factions"] for s in row["source_ids"])
        assert "\u2013" not in row["proposed_label"] and "\u2014" not in row["proposed_label"]
        checks += 7
    for path, digest in labels["generated_files"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
        checks += 1
    report = {
        "project": "IMPERIA COLD WAR", "date": "1970.1.1", "checks_passed": checks,
        "country_history_files": len(profiles), "same_date_profile_blocks": total_blocks,
        "pending_unchanged_tags": sorted(PENDING), "period_names": len(labels["rows"]),
        "source_reversal": "All original country-history bytes preserved outside marked insertions.",
        "bookmark_checks": [1970, 1985, 2000, 2017],
        "performance_scope": "Static history initialization and visible-name lookups only. No new recurring simulation hook.",
        "engine_or_mp_test": False,
    }
    (HERE / "validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
