# IMPERIA COLD WAR — Bounded installation of West German programme rewards.
"""Render GER canon in memory and patch only the approved focus/English loc nodes."""

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import compile as generator
import compile_sandbox
import reward_overlay

BASE = Path(r"E:/HOI4_Mod_Tools/mdcoldwar/runtime/german_reward_revision_20261027/before")
FOCUS = "common/national_focus/COLDWAR_GER_1970_focus.txt"
LOC = "localisation/english/COLDWAR_GER_1970_l_english.yml"
DYNAMIC = "common/dynamic_modifiers/COLDWAR_GER_1970_dynamic_modifiers.txt"
CLEANUP = "common/scripted_effects/COLDWAR_GER_1970_trust_cleanup.txt"
DYNAMIC_CORE = "COLDWAR_GER_1970_core_energie"
MARK = "# IMPERIA COLD WAR — West German reward revision\n"
DYNAMIC_MARK = "# IMPERIA COLD WAR — West German Energy Mix percentage mapping\n"


def focus_nodes(text):
    return compile_sandbox.entries(text, FOCUS)


def anchors_first(text, canonical):
    """Move only the proven late Mannheim anchor ahead of LaFontaine."""
    result = text
    current = focus_nodes(result)
    anchor_ident = ("focus", "COLDWAR_GER_1970_mannheim_congress")
    dependent_ident = ("focus", "COLDWAR_GER_1970_lafontaine_keynes")
    anchor, dependent = current.get(anchor_ident), current.get(dependent_ident)
    if not anchor or not dependent:
        raise ValueError("Missing Mannheim anchor or LaFontaine dependent in GER tree")
    rel = compile_sandbox.first(dependent["node"], "relative_position_id")
    if str(rel).strip('"') != anchor_ident[1]:
        raise ValueError("Unexpected LaFontaine relative anchor; preserve live geometry")
    if list(current).index(anchor_ident) > list(current).index(dependent_ident):
        start, end, body = compile_sandbox.native_span(result, anchor)
        result = result[:start] + result[end:]
        current = focus_nodes(result)
        dependent_start, _, _ = compile_sandbox.native_span(result, current[dependent_ident])
        result = result[:dependent_start] + body + "\n" + result[dependent_start:]
    compile_sandbox.parse(result)
    return result


def previous_party_variant_matches(live_node, post_node, key):
    """Accept only the installed legacy party tooltip/raw gate on these three nodes."""
    party_id, trigger, tooltip = {
        "bafoeg": ("3", "western_social_democrats_are_in_power", "COLDWAR_GER_1970_trg_582cd7c67b"),
        "works_constitution": ("3", "western_social_democrats_are_in_power", "COLDWAR_GER_1970_trg_582cd7c67b"),
        "barzel_social_market": ("1", "western_conservatism_are_in_power", "COLDWAR_GER_1970_trg_c78a444bb5"),
    }.get(key, (None, None, None))
    if party_id is None:
        return False
    variant = copy.deepcopy(live_node)
    party_check = ("check_variable", "=", [("ruling_party", "=", party_id)])
    old_wrapper = ("custom_trigger_tooltip", "=", [
        ("tooltip", "=", tooltip), party_check])
    native_gate = (trigger, "=", "yes")
    available = compile_sandbox.first(variant, "available")
    replaced = sum(item == old_wrapper for item in available)
    if replaced != 1:
        return False
    available = [native_gate if item == old_wrapper else item for item in available]
    variant = [(k, op, available if k == "available" else value)
               for k, op, value in variant]

    count = [0]
    def normalize(block):
        result = []
        for k, op, value in block:
            if k == "check_variable" and value == [("ruling_party", "=", party_id)]:
                count[0] += 1
                result.append(native_gate)
            elif isinstance(value, list):
                result.append((k, op, normalize(value)))
            else:
                result.append((k, op, value))
        return result

    normalized = []
    for k, op, value in variant:
        if k == "completion_reward" and isinstance(value, list):
            normalized.append((k, op, normalize(value)))
        else:
            normalized.append((k, op, value))
    return count[0] == 1 and normalized == post_node


def patch_focus(old, baseline, new):
    old_nodes, before_nodes, new_nodes = map(focus_nodes, (old, baseline, new))
    result = old
    changed = []
    for key in sorted(reward_overlay.PROGRAMMES):
        ident = ("focus", f"COLDWAR_GER_1970_{key}")
        before, post, live = before_nodes.get(ident), new_nodes.get(ident), old_nodes.get(ident)
        if not before or not post or not live:
            raise ValueError(f"Missing focus node in bounded overlay: {ident}")
        if live["node"] == post["node"]:
            continue
        if (live["node"] != before["node"] and
                not previous_party_variant_matches(live["node"], post["node"], key)):
            raise ValueError(f"Preserve divergent live focus: {ident}")
        start, end, _ = compile_sandbox.native_span(result, live)
        body = MARK + compile_sandbox.native_span(new, post)[2]
        result = result[:start] + body + result[end:]
        changed.append(key)
    result = anchors_first(result, new)
    compile_sandbox.parse(result)
    if not result.startswith("# IMPERIA COLD WAR"):
        result = MARK + result
    return result, changed


def patch_dynamic(old, baseline, new):
    old_nodes, before_nodes, new_nodes = (
        compile_sandbox.entries(text, DYNAMIC) for text in (old, baseline, new))
    ident = (DYNAMIC_CORE, DYNAMIC_CORE)
    before, post, live = before_nodes.get(ident), new_nodes.get(ident), old_nodes.get(ident)
    if not before or not post or not live:
        raise ValueError(f"Missing GER Energy Mix dynamic modifier block: {ident}")
    if live["node"] == post["node"]:
        return old, []
    if live["node"] != before["node"]:
        raise ValueError("Preserve divergent live GER Energy Mix dynamic modifier block")
    start, end, _ = compile_sandbox.native_span(old, live)
    body = DYNAMIC_MARK + compile_sandbox.native_span(new, post)[2]
    result = old[:start] + body + old[end:]
    compile_sandbox.parse(result)
    return result, [DYNAMIC_CORE]


def patch_cleanup(old, baseline, new):
    effect_id = "COLDWAR_GER_1970_retired_trust_cleanup"
    identity = (effect_id, effect_id)
    old_nodes, before_nodes, new_nodes = (
        compile_sandbox.entries(text, CLEANUP) for text in (old, baseline, new))
    before, post, live = before_nodes.get(identity), new_nodes.get(identity), old_nodes.get(identity)
    if not before or not post or not live:
        raise ValueError(f"Missing GER retired-trust cleanup effect: {identity}")
    if live["node"] == post["node"]:
        return old, []
    if live["node"] != before["node"]:
        raise ValueError("Preserve divergent live GER retired-trust cleanup")
    start, end, _ = compile_sandbox.native_span(old, live)
    result = old[:start] + compile_sandbox.native_span(new, post)[2] + old[end:]
    compile_sandbox.parse(result)
    return result, [effect_id]


def loc_rows(text):
    pattern = r'(?m)^ ([^:\s]+):\d*\s+(".*")$'
    return dict(re.findall(pattern, text))


def patch_loc(old, baseline, new):
    before, post, live = map(loc_rows, (baseline, new, old))
    result = old
    changed = []
    for key in sorted(reward_overlay.NEW_LOC_KEYS):
        if key not in post:
            raise ValueError(f"Missing generated localisation key: {key}")
        if live.get(key) == post[key]:
            continue
        if live.get(key) != before.get(key):
            raise ValueError(f"Preserve divergent live localisation: {key}")
        line = r'(?m)^ ' + re.escape(key) + r':\d*\s+".*"\n?'
        replacement = f' {key}:0 {post[key]}\n'
        if key in live:
            result = re.sub(line, lambda _: replacement, result)
        else:
            result += replacement
        changed.append(key)
    if not result.startswith("\ufeffl_english:") and not result.startswith("l_english:"):
        raise ValueError("GER localisation header missing")
    return result, changed


def build_plan():
    captured = {}

    def capture(_root, rel, text, bom=False):
        captured[rel] = (text, bom)
        return rel

    generator.write = capture
    generator.build(str(ROOT), scripts_only=True)
    plan = {}
    results = {}
    for rel, transform in ((FOCUS, patch_focus), (LOC, patch_loc),
                           (DYNAMIC, patch_dynamic), (CLEANUP, patch_cleanup)):
        if rel not in captured or not (BASE / rel).exists():
            raise FileNotFoundError(f"Missing captured GER output or snapshot baseline: {rel}")
        new, bom = captured[rel]
        current_path = ROOT / rel
        old = current_path.read_text(encoding="utf-8-sig")
        baseline = (BASE / rel).read_text(encoding="utf-8-sig")
        result, changed = transform(old, baseline, new)
        expected_bom = bom
        results[rel] = dict(changed=changed, bom=expected_bom,
                            sha256=hashlib.sha256(result.encode("utf-8-sig" if bom else "utf-8")).hexdigest())
        if result != old:
            plan[rel] = (result, bom)
    return plan, results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Install the three GER outputs after bounded checks")
    args = parser.parse_args()
    plan, results = build_plan()
    if args.write:
        for rel, (text, bom) in plan.items():
            path = ROOT / rel
            blob = text.encode("utf-8-sig" if bom else "utf-8")
            temp = path.with_name(path.name + ".reward.tmp")
            temp.write_bytes(blob)
            os.replace(temp, path)
    report = {
        "project": "IMPERIA COLD WAR",
        "feature": "West German national programme rewards and Energy Mix unit correction",
        "dry_run": not args.write,
        "output_paths": sorted(results),
        "files_to_write": sorted(plan),
        "nodes": results,
        "engine_tested": False,
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
