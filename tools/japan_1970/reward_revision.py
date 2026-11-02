# IMPERIA COLD WAR — Japan 1970 reward revision overlay.
"""Resolve the authorized JAP reward redesign over its approved graph.

`effect_inventory.json` remains an audit snapshot of the pre-revision draft.
All JAP reward consumers must call these accessors instead of loading that
snapshot directly. The overlay changes effect payloads only: focus IDs, names,
descriptions, gates, coordinates, prerequisites, exclusions, and durations are
owned by approved_design.json and are preserved here.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OVERLAY_PATH = ROOT / "reward_revision_20261027.json"


def load_overlay():
    return json.loads(OVERLAY_PATH.read_text(encoding="utf-8"))


def effective_design(design=None):
    if design is None:
        design = json.loads((ROOT / "approved_design.json").read_text(encoding="utf-8"))["design"]
    result = deepcopy(design)
    replacements = load_overlay().get("effect_text", {})
    for section in result["sections"]:
        for node in section["nodes"]:
            if node["id"] in replacements:
                node["effects"] = replacements[node["id"]]
    return result


def effective_inventory(records=None):
    if records is None:
        records = json.loads((ROOT / "effect_inventory.json").read_text(encoding="utf-8"))
    result = {row["id"]: deepcopy(row) for row in records}
    revisions = load_overlay().get("inventory", {})
    for ident, patch in revisions.items():
        if ident not in result:
            raise ValueError(f"JAP reward overlay references missing inventory ID: {ident}")
        result[ident].update(deepcopy(patch))
        result[ident]["id"] = ident
    return result


def effective_party_map(data=None):
    if data is None:
        data = json.loads((ROOT / "party_map.json").read_text(encoding="utf-8"))
    result = deepcopy(data)
    revisions = load_overlay().get("party", {})
    for ident, patch in revisions.items():
        if ident not in result["focus_helpers"]:
            raise ValueError(f"JAP reward overlay references missing party ID: {ident}")
        result["focus_helpers"][ident].update(deepcopy(patch))
    return result


def effect_text_by_id():
    return load_overlay().get("effect_text", {})


def party_preview_overrides():
    previews = deepcopy(load_overlay().get("party_preview", {}))
    mapping = effective_party_map()
    tooltip_overrides = {
        "research_speed_factor": "COLDWAR_research_speed_factor_tt",
        "experience_gain_navy_factor": "COLDWAR_experience_gain_navy_factor_tt",
        "consumer_goods_factor": "COLDWAR_consumer_goods_factor_tt",
    }
    for ident, record in mapping["focus_helpers"].items():
        one_time = record.get("one_time_effects", [])
        if not any(reward.get("type") == "building" for reward in one_time):
            continue
        lines = ["effect_tooltip = {"]
        variable_prefix = f"COLDWAR_JAP_1970_{record['party']}_"
        for modifier, amount in sorted(record.get("modifier_increments", {}).items()):
            tooltip = tooltip_overrides.get(modifier, f"{modifier}_tt")
            lines.append(f"\tadd_to_variable = {{ var = {variable_prefix}{modifier} value = {amount:.5f} tooltip = {tooltip} }}")
        for reward in one_time:
            kind = reward.get("type")
            if kind == "treasury":
                lines += [f"\tset_temp_variable = {{ treasury_change = {reward['amount']:.5f} }}", "\tmodify_treasury_effect = yes"]
            elif kind == "treasury_gdp_share":
                lines += [
                    f"\tset_temp_variable = {{ treasury_change = {{ value = gdp_total multiply = -{reward['share']:.5f} }} }}",
                    "\tmodify_treasury_effect = yes",
                ]
            elif kind == "building":
                state_id = reward["state_id"]
                level = reward["level"]
                lines += [
                    f"\t{state_id} = {{",
                    f"\t\tadd_extra_state_shared_building_slots = {level}",
                    f"\t\tadd_building_construction = {{ type = {reward['building']} level = {level} instant_build = yes }}",
                    "\t}",
                ]
            elif kind == "research_bonus":
                if reward.get("category") not in {"CAT_industry", "CAT_agriculture"}:
                    raise ValueError(f"{ident}: unverified party preview research category {reward.get('category')}")
                lines += [
                    "\tadd_tech_bonus = {",
                    f"\t\tname = {reward['name']}",
                    f"\t\tbonus = {reward['bonus']:.2f}",
                    f"\t\tuses = {reward['uses']}",
                    f"\t\tcategory = {reward['category']}",
                    "\t}",
                ]
            elif kind == "political_power":
                lines.append(f"\tadd_political_power = {reward['amount']:g}")
            else:
                raise ValueError(f"{ident}: unsupported party preview reward {reward}")
        lines.append("}")
        previews[ident] = "\n".join(lines)
    return previews
