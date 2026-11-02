# IMPERIA COLD WAR — France 1970 starting-spirit recovery revision.
"""Return a bounded overlay for the approved France 1970 design.

The approved concept stays immutable. This overlay adds only the three audited
recovery tracks and their native spirit transitions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

PREFIX = "COLDWAR_FRA2"

_SPIRIT_DATA = [
    {
        "id": f"{PREFIX}_institutional_balance_residual",
        "name": "Unsettled Institutional Balance",
        "description": "The first constitutional reform has changed the presidency, but parliamentary scrutiny and public trust remain unsettled. The existing political-power advantage has ended; the remaining administrative and stability costs persist until the wider civic settlement.",
        "picture": f"{PREFIX}_idea_political_power_bonus",
        "modifiers": {
            "stability_factor": -0.02,
            "bureaucracy_cost_multiplier_modifier": 0.04,
        },
    },
    {
        "id": f"{PREFIX}_higher_education_pressures",
        "name": "Higher Education Expansion Pressures",
        "description": "New colleges and universities widen access, while staffing, laboratories and technical instruction take time to catch up. These adjustment costs remain part of the national education system.",
        "picture": f"{PREFIX}_idea_research_minstry",
        "modifiers": {
            "education_cost_multiplier_modifier": 0.04,
            "production_factory_efficiency_gain_factor": -0.01,
        },
    },
    {
        "id": f"{PREFIX}_oil_dependence_intermediate",
        "name": "Reduced but Persistent Oil Dependence",
        "description": "The chosen generation programme moderates civilian fuel demand, but transport and industrial production still rely on imported petroleum.",
        "picture": f"{PREFIX}_idea_energy_preferred_fossils_idea",
        "modifiers": {"energy_use_modifier_civs": 0.06},
    },
    {
        "id": f"{PREFIX}_oil_dependence_residual",
        "name": "Persistent Oil Dependence",
        "description": "Energy investment has reduced civilian fuel demand, but France remains exposed to imported petroleum prices and supply disputes.",
        "picture": f"{PREFIX}_idea_energy_preferred_fossils_idea",
        "modifiers": {"energy_use_modifier_civs": 0.03},
    },
]


def _transition(source: str, target: str | None) -> dict[str, Any]:
    return {"kind": "transition_spirit", "from": source, "to": target}


def _replace_spirit_effect(node: dict[str, Any], source: str, target: str) -> None:
    matches = [
        index for index, effect in enumerate(node.get("effects", []))
        if effect.get("kind") == "remove_spirit" and effect.get("spirit") == source
    ]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {source} removal in {node['key']}, found {len(matches)}")
    node["effects"][matches[0]] = _transition(source, target)


def _replace_spirit_transition(
    node: dict[str, Any], expected_source: str,
    transition_source: str, target: str,
) -> None:
    matches = [
        index for index, effect in enumerate(node.get("effects", []))
        if effect.get("kind") == "remove_spirit" and effect.get("spirit") == expected_source
    ]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {expected_source} removal in {node['key']}, found {len(matches)}")
    node["effects"][matches[0]] = _transition(transition_source, target)


def apply_starting_spirit_revision(design: dict[str, Any]) -> dict[str, Any]:
    """Return a deep-copied design with staged spirit transitions attached."""
    result = deepcopy(design)
    nodes = {node["key"]: node for node in result.get("nodes", [])}
    spirits = {spirit["id"]: spirit for spirit in result.get("starting_spirits", [])}

    expected_spirits = {
        f"{PREFIX}_presidency", f"{PREFIX}_education", f"{PREFIX}_oil",
        f"{PREFIX}_postcolonial",
    }
    if not expected_spirits.issubset(spirits):
        raise ValueError(f"France recovery overlay missing required starting spirits: {sorted(expected_spirits - spirits.keys())}")
    required_nodes = {
        "executive", "parliament", "civic_settlement", "technical_colleges",
        "mass_universities", "nuclear_scale", "diverse_energy", "oil_resilience",
    }
    if not required_nodes.issubset(nodes):
        raise ValueError(f"France recovery overlay missing required focus nodes: {sorted(required_nodes - nodes.keys())}")

    for node_key in ("executive", "parliament"):
        _replace_spirit_effect(
            nodes[node_key], f"{PREFIX}_presidency",
            f"{PREFIX}_institutional_balance_residual",
        )
    for node_key in ("technical_colleges", "mass_universities"):
        _replace_spirit_effect(
            nodes[node_key], f"{PREFIX}_education",
            f"{PREFIX}_higher_education_pressures",
        )
    for node_key in ("nuclear_scale", "diverse_energy"):
        nodes[node_key]["effects"].append(_transition(
            f"{PREFIX}_oil", f"{PREFIX}_oil_dependence_intermediate",
        ))
    _replace_spirit_transition(
        nodes["oil_resilience"], f"{PREFIX}_oil",
        f"{PREFIX}_oil_dependence_intermediate",
        f"{PREFIX}_oil_dependence_residual",
    )
    nodes["civic_settlement"]["effects"].append(_transition(
        f"{PREFIX}_institutional_balance_residual", None,
    ))
    nodes["civic_settlement"]["description"] = (
        "Complete the housing and recognition settlement while rebuilding trust "
        "in constitutional institutions. National reconciliation and civic "
        "oversight address the remaining administrative and stability costs."
    )

    remedies = {
        f"{PREFIX}_presidency": (
            "Executive Safeguards or Parliamentary Checks replaces The Fifth "
            "Republic with Unsettled Institutional Balance: bureaucracy cost "
            "+4% and stability -2%. The starting +10% political-power bonus ends. "
            "Civic Settlement clears the residual after its funded housing and "
            "reconciliation path."
        ),
        f"{PREFIX}_education": (
            "Technical Colleges or Mass Universities replaces this spirit with "
            "Higher Education Expansion Pressures: education cost +4% and factory "
            "efficiency growth -1%. This adjustment is permanent."
        ),
        f"{PREFIX}_oil": (
            "Nuclear Expansion or Diversified Energy reduces civilian fuel demand "
            "from +8% to +6%. Cut Oil Dependence reduces it to a permanent +3%; "
            "imported petroleum exposure remains."
        ),
    }
    for spirit_id, remedy in remedies.items():
        spirits[spirit_id]["remedy"] = remedy
        description = spirits[spirit_id].get("description", "").rstrip()
        spirits[spirit_id]["description"] = f"{description}\n\nRelief: {remedy}"

    result["recovery_stages"] = deepcopy(_SPIRIT_DATA)
    result["recovery_revision"] = {
        "project": "IMPERIA COLD WAR",
        "id": "france_1970_starting_spirit_stages_20261029",
        "scope": "Three focused spirit transitions; other starting spirits and the 270-day franc spirit are unchanged.",
        "idea_receipts_are_finite_rewards": False,
        "migration_receipts": {
            "presidency": ["executive", "parliament", "civic_settlement"],
            "education": ["technical_colleges", "mass_universities"],
            "oil": ["nuclear_scale", "diverse_energy", "oil_resilience"],
        },
    }
    return result
