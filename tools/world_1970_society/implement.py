# IMPERIA COLD WAR — Research-backed native society and monetary history integration.
"""Generate/validate a reviewable plan, then apply only marked 1970 history insertions."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools/spain_1970_v2"))
from script_ast import parse, first
from history_patch import patched, strip_profile, date_blocks

PENDING = {"ALN", "ZOM", "C01", "ADS"}
FORBIDDEN_1970_CURRENCIES = {"euro", "bitcoin", "brazilian_real", "chinese_yuan_2", "chinese_yuan_3"}
FORBIDDEN_1970_FACTIONS = {"the_donju", "iranian_quds_force", "foreign_jihadis"}


def read_json(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def write_json(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def keyed(data):
    for key in ("records", "countries"):
        if key in data:
            value = data[key]
            return {row["tag"]: row for row in value} if isinstance(value, list) else value
    raise ValueError("Research document has no records/countries")


def native_faction_definitions():
    tree = parse((ROOT / "common/ideas/AA_law_internal_factions.txt").read_text(encoding="utf-8-sig"))
    return {k: v for k, _, v in first(first(tree, "ideas"), "internal_factions") if isinstance(v, list)}


def allowed_for_tag(rows, tag):
    # These native restrictions use static original_tag tests. Unknown dynamic
    # predicates are intentionally not silently accepted by this limited evaluator.
    result = []
    for k, _, v in rows:
        if k == "original_tag": answer = tag == v
        elif k == "OR": answer = any(allowed_for_tag([row], tag) for row in v)
        elif k == "AND": answer = allowed_for_tag(v, tag)
        elif k == "NOT": answer = not allowed_for_tag(v, tag)
        elif k in ("check_variable", "is_in_array"): answer = False
        else: raise ValueError("Unreviewed native allowed condition: " + k)
        result.append(answer)
    return all(result)


def build_profiles():
    inventory = read_json("inventory.json")
    currency_doc, religion_doc, faction_doc = (read_json(name) for name in ("currency.json", "religion.json", "factions.json"))
    currency, religion, factions = (keyed(doc) for doc in (currency_doc, religion_doc, faction_doc))
    expected = {c["tag"] for c in inventory["countries"]}
    for name, rows in (("currency", currency), ("religion", religion), ("factions", factions)):
        if set(rows) != expected: raise ValueError(f"{name}: incomplete or unexpected country coverage: {expected ^ set(rows)}")
    candidates = read_json("initialiser_candidates.json")["countries"]
    definitions = native_faction_definitions()
    known = inventory["native_ideas"]
    profiles = {}
    for country in inventory["countries"]:
        tag = country["tag"]
        if tag in PENDING: continue
        c, r, f = currency[tag], religion[tag], factions[tag]
        choice = c.get("reserve_currency", c.get("idea"))
        belief = r.get("idea", r.get("religion"))
        groups = f.get("ideas", f.get("factions"))
        assert choice in known["reserve_currency"], (tag, choice)
        assert choice not in FORBIDDEN_1970_CURRENCIES, (tag, choice)
        assert belief in known["religion"], (tag, belief)
        assert isinstance(groups, list) and len(groups) == 3 and len(set(groups)) == 3, (tag, groups)
        assert not set(groups) & FORBIDDEN_1970_FACTIONS, (tag, groups)
        for group in groups:
            assert group in definitions, (tag, group)
            assert allowed_for_tag(first(definitions[group], "allowed", []), tag), (tag, group, "not allowed")
        for component in (c, r, f):
            assert component.get("source_ids"), (tag, "missing evidence linkage")
        assert c["no_foreign_reserve"] in (0, 1), tag
        previous = candidates.get(tag, {})
        old = set(country["1970_relevant_ideas"] + country["base_relevant_ideas"])
        old.update(previous.get("religion", []))
        old.update(previous.get("reserve_currency", []))
        conflicts = old & set(known["religion"] + known["reserve_currency"])
        conflicts -= {choice, belief}
        retained = sorted(set(previous.get("internal_factions", [])) - set(groups))
        profiles[tag] = {
            "name": country["name"], "path": country["path"],
            "currency": choice, "no_foreign_reserve": c["no_foreign_reserve"], "religion": belief,
            "factions": groups, "retained_authored_faction_candidates": retained,
            "remove_ideas": sorted(conflicts),
            "opinion_policy": "Preserve existing authored values; initialize absent selected opinions to native neutral50.",
            "source_ids": {"currency": c["source_ids"], "religion": r["source_ids"], "factions": f["source_ids"]},
            "historical_rationale": {"currency": c["rationale"], "religion": r["rationale"], "factions": f["rationale"]},
        }
    return inventory, profiles


def plan_changes(inventory, profiles):
    plan, files = [], []
    for country in inventory["countries"]:
        path = ROOT / country["path"]
        raw = path.read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), str(path)
        text = raw.decode("utf-8")
        assert digest(strip_profile(text).encode("utf-8")) == country["sha256"], "Concurrent history changes: " + str(path)
        if country["tag"] in PENDING:
            assert digest(raw) == country["sha256"], "Pending tag modified: " + country["tag"]
            continue
        updated = patched(text, profiles[country["tag"]])
        assert strip_profile(updated) == strip_profile(text), str(path)
        assert patched(updated, profiles[country["tag"]]) == updated, "Not idempotent: " + str(path)
        parse(updated)
        files.append({"path": country["path"], "tag": country["tag"], "before_sha256": country["sha256"], "after_sha256": digest(updated.encode("utf-8")), "snapshot_blocks": len(date_blocks(updated))})
        if updated != text: plan.append((path, updated.encode("utf-8")))
    return plan, files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply already validated direct-history insertions")
    args = parser.parse_args()
    inventory, profiles = build_profiles()
    plan, files = plan_changes(inventory, profiles)
    write_json("profiles.json", {"project": "IMPERIA COLD WAR", "date": "1970.1.1", "pending_unchanged_tags": sorted(PENDING), "profiles": profiles})
    write_json("changes.json", {"project": "IMPERIA COLD WAR", "date": "1970.1.1", "applied": args.apply, "pending_unchanged_tags": sorted(PENDING), "files": files})
    if args.apply:
        for path, raw in plan:
            temporary = path.with_name(path.name + ".cw1970.tmp")
            try:
                temporary.write_bytes(raw)
                os.replace(temporary, path)
            finally:
                if temporary.exists(): temporary.unlink()
    print(f"Profiles validated: {len(profiles)}. History files {'updated' if args.apply else 'planned'}: {len(plan)}. Pending tags untouched: {', '.join(sorted(PENDING))}.")


if __name__ == "__main__":
    main()
