# IMPERIA COLD WAR — Independent faction and period-name integration checks.
"""Read-only runtime/history QA. Writes its own provenance report only."""
from pathlib import Path
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools/spain_1970_v2"))
from script_ast import parse, first, values, walk
from implement import allowed_for_tag

PENDING = {"ADS", "ALN", "C01", "ZOM"}
FORBIDDEN = {"oligarchs", "the_donju", "iranian_quds_force", "foreign_jihadis"}
CHECKS = []

def check(name, answer, detail=None):
    CHECKS.append({"check": name, "passed": bool(answer), **({"detail": detail} if detail is not None else {})})

def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))

def localisations(text):
    return dict(re.findall(r'^\s*([A-Za-z0-9_]+):\s*(?:\d+\s*)?("(?:\\.|[^"\\])*")\s*$', text, re.M))

# IMPERIA COLD WAR — Evaluate actual period-name and native Iranian routing predicates.
def name_condition(rows, facts):
    answers = []
    for key, _, value in rows:
        if key in ("AND", "PER"):
            answer = name_condition(value, facts)
        elif key == "OR":
            answer = any(name_condition([row], facts) for row in value)
        elif key == "NOT":
            answer = not name_condition(value, facts)
        elif key == "IMP_is_1970_scenario":
            answer = facts["start1970"]
        elif key == "has_cosmetic_tag":
            if value != "PER_IMPERIAL_1970": raise AssertionError(value)
            answer = facts["imperial_cosmetic"]
        elif key == "emerging_moderate_shiite_are_in_power":
            answer = facts["moderate_shia"]
        elif key == "emerging_hardline_shiite_are_in_power":
            answer = facts["hardline_shia"]
        else:
            raise AssertionError("Unhandled live name predicate: " + key)
        answers.append(answer)
    return all(answers)

def resolve_name_key(provider, facts):
    for branch in values(provider, "text"):
        if name_condition(first(branch, "trigger", []), facts):
            return first(branch, "localization_key")
    raise AssertionError("No name branch matched")

def main():
    research = load("factions.json")
    inventory = {r["tag"]: r for r in load("inventory.json")["countries"]}
    rows = {r["tag"]: r for r in research["countries"]}
    profiles = load("profiles.json")["profiles"]
    authored = load("initialiser_candidates.json")["countries"]
    labels = load("labels.json")
    native_script = parse((ROOT / "common/ideas/AA_law_internal_factions.txt").read_text(encoding="utf-8"))
    definitions = dict((k, v) for k, _, v in first(first(native_script, "ideas"), "internal_factions") if isinstance(v, list))
    check("All397 inventory records covered", len(rows) == 397 and set(rows) == set(inventory))
    check("Only393 reviewed profiles enter integration", set(profiles) == set(rows) - PENDING)

    allowed_checks = 0
    retained_exceptions = []
    for tag, row in rows.items():
        if tag in PENDING:
            check(tag + " has no research assignment", row["ideas"] == [] and row["status"] == "pending_user_review")
            path = ROOT / inventory[tag]["path"]
            check(tag + " history unchanged", hashlib.sha256(path.read_bytes()).hexdigest() == inventory[tag]["sha256"])
            continue
        p = profiles[tag]
        effective = set(p["factions"] + p["retained_authored_faction_candidates"])
        check(tag + " integrated proposal matches research", p["factions"] == row["ideas"])
        check(tag + " has3 distinct representative groups", len(row["ideas"]) == len(set(row["ideas"])) == 3)
        check(tag + " excludes modern faction institutions", not effective & FORBIDDEN)
        check(tag + " has traceable research", bool(row["source_ids"]) and set(row["source_ids"]) <= research["sources"].keys())
        prior = set(authored.get(tag, {}).get("internal_factions", []))
        check(tag + " retained extras preexist in authored setup", set(p["retained_authored_faction_candidates"]) <= prior)
        for group in row["ideas"]:
            valid = group in definitions and allowed_for_tag(first(definitions[group], "allowed", []), tag)
            check(tag + ": native allowed " + group, valid)
            allowed_checks += 1
        for group in p["retained_authored_faction_candidates"]:
            if not allowed_for_tag(first(definitions[group], "allowed", []), tag):
                retained_exceptions.append({"tag": tag, "idea": group, "reason": "Existing authored membership retained; no new membership introduced by this profile. Native original-tag allowed restriction is recorded for review."})

    provider = ROOT / "common/scripted_localisation/COLDWAR_1970_internal_faction_names.txt"
    locfile = ROOT / "localisation/english/replace/COLDWAR_1970_internal_faction_names_l_english.yml"
    script_raw, loc_raw = provider.read_bytes(), locfile.read_bytes()
    check("Name provider UTF8 without BOM", not script_raw.startswith(b"\xef\xbb\xbf"))
    check("English localisation UTF8 with BOM", loc_raw.startswith(b"\xef\xbb\xbf"))
    check("Provider project marker", script_raw.decode("utf-8").startswith("# IMPERIA COLD WAR — "))
    tree = parse(script_raw.decode("utf-8"))
    providers = {first(v, "name"): v for k, _, v in tree if k == "defined_text"}
    output = localisations(loc_raw.decode("utf-8-sig"))
    native = localisations((ROOT / "localisation/english/MD_internal_factions_l_english.yml").read_text(encoding="utf-8-sig"))
    wanted = {
        n["key"]: n for t, p in profiles.items() for n in rows[t]["localisation_notes"]
        if n["idea"] in set(p["factions"] + p["retained_authored_faction_candidates"])
    }
    check("Generated label set matches effective researched groups", {r["key"] for r in labels["rows"]} == wanted.keys())
    check("Provider count equals manifest", len(providers) == len(labels["rows"]))
    for row in labels["rows"]:
        name = row["key"]
        block = providers[row["function"]]
        branches = values(block, "text")
        check(name + ": default native branch last", first(branches[-1], "localization_key") == row["fallback_key"] and first(branches[-1], "trigger") is None)
        for branch in branches[:-1]:
            trigger = first(branch, "trigger", [])
            check(name + ": historical branch explicitly1970", ("IMP_is_1970_scenario", "=", "yes") in list(walk(trigger)))
        quoted = native.get(name, native[row["idea"]])
        check(name + ": exact outside1970 native value", output[row["fallback_key"]] == quoted == row["fallback_quoted"])
        check(name + ": era text matches research", json.loads(output[row["historical_key"]]) == wanted[name]["proposed_label"])
        visible = json.loads(output[row["historical_key"]])
        check(name + ": ordinary English institution name", not re.search(r"fallback|technical|proxy|approximation|unknown|debug|placeholder|disclaimer", visible, re.I) and "\u2013" not in visible and "\u2014" not in visible)
        check(name + ": no localisation self-reference", row["function"] not in output[row["fallback_key"]])
    # IMPERIA COLD WAR — The initial imperial name must not mask a later native IRGC switch.
    iran_row = next(row for row in labels["rows"] if row["key"] == "PER_the_military")
    iran_wrapper = providers[iran_row["function"]]
    iran_native_tree = parse((ROOT / "common/scripted_localisation/99_PER_scripted_localisation.txt").read_text(encoding="utf-8"))
    iran_native = next(value for key, _, value in iran_native_tree if key == "defined_text" and first(value, "name") == "PER_army_int_faction")
    iran_history = parse((ROOT / inventory["PER"]["path"]).read_text(encoding="utf-8"))
    iran_start = first(iran_history, "1970.1.1", [])
    check("Iran1970 snapshot supplies the imperial cosmetic", ("set_cosmetic_tag", "=", "PER_IMPERIAL_1970") in list(walk(iran_start)))
    for start1970 in (False, True):
        for imperial_cosmetic in (False, True):
            for moderate_shia in (False, True):
                for hardline_shia in (False, True):
                    facts = dict(start1970=start1970, imperial_cosmetic=imperial_cosmetic, moderate_shia=moderate_shia, hardline_shia=hardline_shia)
                    case = "Iran route: " + str(facts)
                    is_imperial = start1970 and imperial_cosmetic and not moderate_shia and not hardline_shia
                    selected = resolve_name_key(iran_wrapper, facts)
                    expected = iran_row["historical_key"] if is_imperial else iran_row["fallback_key"]
                    check(case + " uses correct wrapper branch", selected == expected)
                    # This executes the original existing party-dependent provider,
                    # including a revolution while the imperial cosmetic is stale.
                    native_key = resolve_name_key(iran_native, facts)
                    expected_native = "PER_irgc_name" if moderate_shia or hardline_shia else "PER_artesh_name"
                    check(case + " keeps native regime routing reachable", native_key == expected_native and (is_imperial or json.loads(output[selected]) == "[PER_army_int_faction]"))
    check("Name provider contains no effects or regular callbacks", all(k == "defined_text" for k, _, _ in tree) and not any(k in {"every_country", "every_state", "country_event", "add_ideas", "set_variable", "on_daily", "on_monthly"} for k, _, _ in walk(tree)))
    result = {
        "project": "IMPERIA COLD WAR", "date": "1970.1.1", "checks": CHECKS,
        "summary": {"passed": sum(r["passed"] for r in CHECKS), "failed": sum(not r["passed"] for r in CHECKS), "new_native_memberships_checked": allowed_checks, "generated_period_names": len(labels["rows"])},
        "retained_existing_allowed_exceptions": retained_exceptions,
        "limitations": "Static script/localisation/profile validation only. No HOI4 executable rendering, save-load simulation or multiplayer OOS run performed. Existing scripted country initializers are conservative call-graph candidates, not a full engine evaluation.",
    }
    (HERE / "factions_validation.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"]))
    print("Retained native allowed exceptions:", retained_exceptions)
    for item in CHECKS:
        if not item["passed"]: print("FAILED", item["check"], item.get("detail", ""))
    return 1 if result["summary"]["failed"] else 0

if __name__ == "__main__": raise SystemExit(main())
