# IMPERIA COLD WAR — Period-correct English names for selected native internal factions.
"""Reuse native tag keys, with exact native fallback outside the 1970 bookmark."""
import hashlib
import json
import re
from pathlib import Path
from implement import HERE, ROOT, read_json, keyed, write_json

SCRIPT = ROOT / "common/scripted_localisation/COLDWAR_1970_internal_faction_names.txt"
LOCALISATION = ROOT / "localisation/english/replace/COLDWAR_1970_internal_faction_names_l_english.yml"
NATIVE = ROOT / "localisation/english/MD_internal_factions_l_english.yml"


def build():
    native = dict(re.findall(r'^\s*([A-Za-z0-9_]+):\s*(?:\d+\s*)?("(?:\\.|[^"\\])*")\s*$', NATIVE.read_text(encoding="utf-8-sig"), re.M))
    profiles = read_json("profiles.json")["profiles"]
    factions = keyed(read_json("factions.json"))
    rows = []
    for tag, profile in profiles.items():
        effective = set(profile["factions"] + profile["retained_authored_faction_candidates"])
        for note in factions[tag].get("localisation_notes", []):
            if note["idea"] not in effective: continue
            key = note["key"]
            original = native.get(key, native[note["idea"]])
            function = "COLDWAR_1970_name_" + key
            historical = function + "_historical"
            fallback = function + "_native"
            condition = "IMP_is_1970_scenario = yes"
            # IMPERIA COLD WAR — Keep Iran's native post-revolution institution routing reachable.
            if key in ("PER_the_military", "PER_intelligence_community"):
                condition += " PER = { has_cosmetic_tag = PER_IMPERIAL_1970 NOT = { OR = { emerging_moderate_shiite_are_in_power = yes emerging_hardline_shiite_are_in_power = yes } } }"
            rows.append({"tag": tag, **note, "function": function, "historical_key": historical, "fallback_key": fallback, "fallback_quoted": original, "historical_condition": condition})
    code = [
        "# IMPERIA COLD WAR — Period-correct internal-faction names in the 1970 bookmark.",
        "# Native faction naming credit: Birdy and Killerrabbit. Runtime faction effects remain unchanged.",
        "",
    ]
    loc = ["l_english:", " # IMPERIA COLD WAR — Period-correct native faction names; no change to later bookmarks."]
    for row in rows:
        code += [
            "# IMPERIA COLD WAR — " + row["key"] + " period name.",
            "defined_text = {", "\tname = " + row["function"],
            "\ttext = {", "\t\ttrigger = { " + row["historical_condition"] + " }",
            "\t\tlocalization_key = " + row["historical_key"], "\t}",
            "\ttext = { localization_key = " + row["fallback_key"] + " }", "}", "",
        ]
        loc += [
            " # IMPERIA COLD WAR — " + row["key"] + " period name.",
            " " + row["key"] + ': "[' + row["function"] + ']"',
            " " + row["historical_key"] + ": " + json.dumps(row["proposed_label"], ensure_ascii=False),
            " " + row["fallback_key"] + ": " + row["fallback_quoted"],
        ]
    SCRIPT.write_bytes(("\n".join(code) + "\n").encode("utf-8"))
    LOCALISATION.parent.mkdir(exist_ok=True)
    LOCALISATION.write_bytes(("\n".join(loc) + "\n").encode("utf-8-sig"))
    write_json("labels.json", {
        "project": "IMPERIA COLD WAR", "date": "1970.1.1", "scope": "Names only, selected or already authored faction memberships. No simulation hooks.",
        "native_source": NATIVE.relative_to(ROOT).as_posix(), "native_source_sha256": hashlib.sha256(NATIVE.read_bytes()).hexdigest(),
        "source_credit": "Native localisation: Birdy and Killerrabbit. Individual label authors and block-specific redistribution licence unknown. New historical labels and routing authored for this project; no new licence assigned.",
        "rows": rows,
        "generated_files": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in (SCRIPT, LOCALISATION)},
    })
    print(f"Historical faction names generated: {len(rows)}. Native fallback retained outside 1970.")


if __name__ == "__main__":
    build()
