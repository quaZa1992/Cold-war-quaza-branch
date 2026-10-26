# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Focused AST regressions for the four explicitly approved royal mappings."""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import monarchy_runtime as runtime
from build import Builder, load_catalog
from dispatch import _candidate_effect, _restore_setter

sys.path.insert(0, str(runtime.ROOT / "tools/vietnam_1970"))
from script_ast import first, parse, values, walk


def main():
    checks = 0
    def check(ok, message):
        nonlocal checks
        checks += 1
        assert ok, message

    countries = load_catalog()
    outputs = runtime.build(countries)
    before = {name: (runtime.ROOT / name).read_text(encoding="utf-8-sig") for name in outputs}
    asts = {name: parse(text) for name, text in outputs.items()}
    old = {name: parse(text) for name, text in before.items()}
    check(len(outputs) == 3 + len(runtime.TAGS), "Only assigned runtime files may be generated")
    pools = dict((k, v) for k, _, v in asts[runtime.POOL_FILE])
    old_pools = dict((k, v) for k, _, v in old[runtime.POOL_FILE])
    selected = lambda key: bool(re.fullmatch(r"MDCW_HP_native_pool_" + runtime.TAG_PATTERN + r"_\d+", key))
    check({k:v for k,v in pools.items() if k != runtime.SYNC_EFFECT and not selected(k)} ==
          {k:v for k,v in old_pools.items() if k != runtime.SYNC_EFFECT and not selected(k)},
          "Unrelated historical pool effects must remain identical")
    check(pools["MDCW_HP_native_pool_BHR_8"] == old_pools["MDCW_HP_native_pool_BHR_8"],
          "Bahrain's Shiite opposition is unchanged")
    check(pools["MDCW_HP_native_pool_PER_9"] == old_pools["MDCW_HP_native_pool_PER_9"],
          "Iran's revolutionary Shiite pool is unchanged")

    def country_of(row):
        return first(first(row, "limit", []), "original_tag")
    def other_sync(rows):
        return [r for r in first(rows, "if", []) if r[0] != "if" or country_of(r[2]) not in runtime.TAGS]
    check(other_sync(pools[runtime.SYNC_EFFECT]) == other_sync(old_pools[runtime.SYNC_EFFECT]),
          "Unrelated native counter synchronization must remain identical")
    def iran_nine(rows):
        return [row for row in rows if isinstance(row[2], list) and
                first(row[2], "original_tag") == "PER" and
                first(first(row[2], "check_variable", []), "ruling_party") == "9"]
    def iran_nine_sync(rows):
        return [row for row in first(rows, "if", []) if row[0] == "if" and
                iran_nine([("limit", "=", first(row[2], "limit", []))])]
    check(iran_nine_sync(pools[runtime.SYNC_EFFECT]) == iran_nine_sync(old_pools[runtime.SYNC_EFFECT]),
          "Iran's revolutionary native counter synchronization must remain identical")
    for path, container in ((runtime.POOL_TRIGGER_FILE, "OR"), (runtime.RETIREMENT, "NOT")):
        def unrelated(rows):
            return [r for r in walk(rows) if r[0] == "AND" and
                    first(r[2], "original_tag") not in runtime.TAGS]
        check(unrelated(asts[path]) == unrelated(old[path]), "Unrelated country tests changed: " + path)
        check(iran_nine(list(walk(asts[path]))) == iran_nine(list(walk(old[path]))),
              "Iran's revolutionary trigger/retirement conditions changed: " + path)

    for tag in runtime.TAGS:
        key = f"MDCW_HP_native_pool_{tag}_0"
        check(key in pools and f"MDCW_HP_native_pool_{tag}_23" not in pools, tag + " family correction")
        body = pools[key]
        creations = [v for k, _, v in walk(body) if k == "create_country_leader"]
        check(all(first(c, "ideology") == "Western_Autocracy" and
                  ("_bare", "=", "king") in first(c, "traits", []) for c in creations),
              tag + " sovereigns retain king in the Western Autocracy family")
        check(not any(k in ("set_politics", "change_ruling_party_effect") or
                      (k == "set_variable" and first(v, "ruling_party") is not None)
                      for k, _, v in walk(body)), tag + " pool cannot restore a government")
        path = f"common/scripted_effects/{tag}_political_leaders.txt"
        check(_restore_setter(outputs[path], tag) == _restore_setter(before[path], tag),
              tag + " modern fallback changed")
        setter = asts[path][0][2]
        routes = [r for r in setter if r[0] in ("if", "else_if")]
        check(any(first(first(r[2], "limit", []), "IMP_is_1970_scenario") == "yes" and
                  first(first(first(r[2], "limit", []), "check_variable", []), "ruling_party") == "0"
                  for r in routes), tag + " setter must reach slot zero only in 1970")

        # Inspect each emitted counter transition, including protected rollback
        # and the out-of-range fallback; two-person pools cycle 0 -> 1 -> 0.
        branches = [v for k, _, v in body if k in ("if", "else_if", "else")]
        size = len(branches) - 1
        transitions = []
        for number, branch in enumerate(branches):
            selected_slot = number if number < size else 0
            counter_if = next(v for k, _, v in branch if k == "if")
            counter_else = next(v for k, _, v in branch if k == "else")
            protected = first(counter_if, "set_variable")[0][2]
            ordinary = first(counter_else, "set_variable")[0][2]
            transitions.append((protected, ordinary))
            check(int(protected) == selected_slot and int(ordinary) == (selected_slot + 1) % size,
                  tag + " incorrect ordinary/protected counter transition")

    guards = [v for k, _, v in walk(asts[runtime.RETIREMENT]) if k == "AND" and
              first(v, "original_tag") in runtime.TAGS]
    guard_keys = {(first(row, "original_tag"), first(first(row, "check_variable"), "ruling_party"))
                  for row in guards}
    check(guard_keys == {("KUW", "0"), ("PER", "0"), ("PER", "9")},
          "Sole-candidate retirement guards must cover Kuwait0, Shah0 and unchanged Iran9")

    builder = Builder({tag: countries[tag] for tag in runtime.TAGS})
    builder.leaders()
    # Rebuild against a disposable installed snapshot. The approved-portrait
    # provider still reads the real reviewed manifest; these files satisfy only
    # the downstream existence guards, not portrait approval.
    with tempfile.TemporaryDirectory(prefix=".monarchy-runtime-test-", dir=Path(__file__).resolve().parent) as directory:
        fixture = Path(directory)
        assert fixture.resolve().is_relative_to(Path(__file__).resolve().parent)
        for name, text in outputs.items():
            dest = fixture / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text, encoding="utf-8")
        for person in builder.ready:
            asset = fixture / person["portrait"]
            asset.parent.mkdir(parents=True, exist_ok=True)
            asset.touch()
        for tag in runtime.TAGS:
            history = next((runtime.ROOT / "history/countries").glob(tag + " - *.txt"))
            dest = fixture / "history/countries" / history.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(history.read_bytes())
        with patch.object(runtime, "ROOT", fixture):
            check(runtime.build(countries) == outputs, "Narrow runtime generation must be idempotent")

    try:
        _candidate_effect("BHR", 0, "Western_Autocracy_leader", [{
            "id": "invalid", "name": "Invalid", "portrait": "portrait.dds",
            "available_from": "1970.1.1", "traits": ["king } set_politics = {"]}])
    except ValueError:
        check(True, "Invalid trait rejected")
    else:
        check(False, "Explicit traits must be native identifier tokens")
    print(json.dumps({"ok": True, "checks": checks, "runtime_files": list(outputs),
                      "approved_people": len(builder.ready), "pending_portraits": len(builder.pending),
                      "engine_tested": False}, indent=2))


if __name__ == "__main__":
    main()
