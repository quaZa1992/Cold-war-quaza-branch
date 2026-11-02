# IMPERIA COLD WAR — France 1970 approved party expansion.
"""Merge the approved 20-focus expansion onto the frozen 156-focus runtime."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
APPROVED_PATH = HERE / "approved_expansion.json"
APPROVAL_PATH = HERE / "EXPANSION_APPROVAL.json"
APPROVED_SHA256 = "c8e6ab3933bf72a14b043c3a92d846826f3d1937f902efc7cc3d0dd64364c055"
BASELINE_SHA256 = "00d5e2721934ad527360ce0265f1213e345a1df8b0f1999c22599f23199dbbe9"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _stable_design_bytes(design: dict[str, Any]) -> bytes:
    return (json.dumps(design, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _keyed(records: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    result = {record[key]: record for record in records}
    if len(result) != len(records):
        raise ValueError(f"Duplicate design {key} values")
    return result


def _copy_allowed_fields(
    current: dict[str, Any], target: dict[str, Any], allowed: set[str], context: str,
) -> None:
    for field in set(current) | set(target):
        if field in allowed:
            continue
        if current.get(field) != target.get(field):
            raise ValueError(f"Unexpected approved-baseline drift at {context}.{field}")
    for field in sorted(allowed):
        if field in target:
            current[field] = deepcopy(target[field])
        else:
            current.pop(field, None)


def _approved_records() -> tuple[dict[str, Any], dict[str, Any], bytes]:
    raw = APPROVED_PATH.read_bytes()
    actual = _sha(raw)
    if actual != APPROVED_SHA256:
        raise ValueError(f"Immutable France expansion input hash mismatch: {actual}")
    design = json.loads(raw.decode("utf-8"))
    approval = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    if approval.get("project") != "IMPERIA COLD WAR":
        raise ValueError("Expansion approval record is missing the project identifier")
    if approval.get("approved_input_sha256") != APPROVED_SHA256:
        raise ValueError("Expansion approval record does not match the frozen input hash")
    if design.get("proposal_baseline_sha256") != BASELINE_SHA256:
        raise ValueError("Expansion snapshot points to an unexpected runtime baseline")
    return design, approval, raw


def apply_expansion_revision(design: dict[str, Any]) -> dict[str, Any]:
    """Add the approved nodes and narrow CID/decision lifecycle changes.

    The incoming design must serialize to the exact runtime file from which the
    visualized proposal was authored. Only proposal-marked additions and the
    two reviewed focus metadata changes plus the single prerequisite change are
    merged. Existing focus payloads and all newer runtime overlays are retained.
    """
    if design.get("expansion_revision"):
        raise ValueError("France expansion overlay has already been applied")
    baseline_actual = _sha(_stable_design_bytes(design))
    if baseline_actual != BASELINE_SHA256:
        raise ValueError(f"France expansion baseline mismatch: {baseline_actual}")

    approved, approval, _ = _approved_records()
    current = deepcopy(design)
    current_nodes = _keyed(current["nodes"], "key")
    approved_nodes = _keyed(approved["nodes"], "key")
    new_nodes = [node for node in approved["nodes"] if node.get("expansion_change") == "new"]
    expected_keys = set(approval["added_focus_keys"])
    actual_keys = {node["key"] for node in new_nodes}
    if len(new_nodes) != 20 or actual_keys != expected_keys:
        raise ValueError(f"Expected the exact approved 20-focus set, got {sorted(actual_keys)}")
    if any(node["key"] in current_nodes for node in new_nodes):
        raise ValueError("An expansion focus key already exists in the runtime design")

    building_levels = 0
    building_slots = 0
    standalone_slots = 0
    for node in new_nodes:
        for effect in node.get("effects", []):
            if effect.get("kind") == "building":
                amount, slots = int(effect["amount"]), int(effect.get("slots", 0))
                if amount < 1 or slots != amount or not effect.get("slots_before_construction"):
                    raise ValueError(f"Building slots do not match levels in {node['key']}: {effect}")
                building_levels += amount
                building_slots += slots
            elif effect.get("kind") == "state_slots":
                if effect.get("native_effect") != "add_extra_state_shared_building_slots":
                    raise ValueError(f"Unknown native state-slot effect in {node['key']}: {effect}")
                standalone_slots += int(effect["amount"])
    if (building_levels, building_slots, standalone_slots) != (32, 32, 5):
        raise ValueError(
            f"Expansion physical package changed: levels={building_levels}, "
            f"building_slots={building_slots}, standalone_slots={standalone_slots}"
        )
    current["nodes"].extend(deepcopy(new_nodes))

    for key in ("cid_tax", "cid_cooperatives"):
        target = approved_nodes[key]
        _copy_allowed_fields(current_nodes[key], target, {
            "spirit", "spirit_name", "modifier_pool", "programme_activation_conditions",
        }, f"focus.{key}")

    current_decisions = _keyed(current.get("decisions", []), "id")
    approved_decisions = _keyed(approved.get("decisions", []), "id")
    fund_id = "COLDWAR_FRA2P_regional_conversion"
    if fund_id not in current_decisions or fund_id not in approved_decisions:
        raise ValueError("The existing Regional Conversion Fund is missing")
    before_effects = current_decisions[fund_id].get("effects", [])
    after_effects = approved_decisions[fund_id].get("effects", [])
    if before_effects != after_effects:
        raise ValueError("The Regional Conversion Fund fee or finite reward changed")
    _copy_allowed_fields(current_decisions[fund_id], approved_decisions[fund_id], {
        "conditions", "runtime_guards",
    }, "decision.regional_conversion")
    expected_or = "OR = { has_completed_focus = COLDWAR_FRA2_public_banks has_completed_focus = COLDWAR_FRA2_ps_conversion_boards }"
    if expected_or not in current_decisions[fund_id].get("runtime_guards", []):
        raise ValueError("Regional Conversion Fund runtime guard lacks its two-parent OR")

    current["expansion_revision"] = {
        "project": "IMPERIA COLD WAR",
        "approval_record": str(APPROVAL_PATH.relative_to(HERE.parents[1])).replace("\\", "/"),
        "approved_input_sha256": APPROVED_SHA256,
        "baseline_runtime_design_sha256": BASELINE_SHA256,
        "added_focus_keys": sorted(actual_keys),
        "added_focus_count": len(new_nodes),
        "added_building_levels": building_levels,
        "added_building_slots": building_slots,
        "added_standalone_slots": standalone_slots,
        "cid_focus_keys": ["cid_tax", "cid_cooperatives", "cid_wholesale_cooperatives", "cid_rural_networks"],
        "cid_programme_activation_conditions": [
            "nationalist_right_wing_populists_are_in_power = yes",
            "date < 1972.10.5",
        ],
        "regional_conversion_prerequisite": expected_or,
    }
    return current
