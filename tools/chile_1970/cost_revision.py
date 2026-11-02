# IMPERIA COLD WAR — Chile 1970 static GDP-scaled cost overlay.
"""Apply the frozen Chile 1970 monetary-cost revision without editing design data."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path
from typing import Any


REVISION_PATH = Path(__file__).with_name("cost_revision.json")


def _load_revision() -> dict[str, Any]:
    with REVISION_PATH.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def _scale(value: Any, factor: Decimal, field_path: str) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field_path} must be a numeric cost")
    amount = Decimal(str(value))
    if not amount.is_finite() or amount < 0:
        raise ValueError(f"{field_path} must be a finite, non-negative cost")
    scaled = (amount * factor).quantize(Decimal("0.00001"), rounding=ROUND_HALF_UP)
    if scaled == scaled.to_integral_value():
        return int(scaled)
    return float(scaled)


def _scale_cost_fields(record: dict[str, Any], fields: tuple[str, ...], factor: Decimal, path: str) -> None:
    for field in fields:
        if field in record:
            record[field] = _scale(record[field], factor, f"{path}.{field}")


def apply_costs(approved_data: dict[str, Any]) -> dict[str, Any]:
    """Return a deep-copied Chile design with only approved monetary fields rescaled."""
    revision = _load_revision()
    factor = Decimal(revision["factor"])
    revised = deepcopy(approved_data)

    for node in revised.get("nodes", []):
        _scale_cost_fields(node, ("money", "weekly"), factor, f"nodes[{node.get('key', '?')}]" )

    for agreement in revised.get("agreements", []):
        agreement_id = agreement.get("id", "?")
        for side in ("chile", "recipient"):
            record = agreement.get(side)
            if record is not None:
                _scale_cost_fields(record, ("setup", "weekly"), factor, f"agreements[{agreement_id}].{side}")

    for event in revised.get("events", []):
        event_id = event.get("id", "?")
        for index, option in enumerate(event.get("options", [])):
            _scale_cost_fields(option, ("money", "weekly"), factor, f"events[{event_id}].options[{index}]")

    for contract in revised.get("decision_contracts", []):
        _scale_cost_fields(contract, ("money", "weekly"), factor, f"decision_contracts[{contract.get('id', '?')}]" )

    return revised


def load_cost_adjusted_design(path: str | Path | None = None) -> dict[str, Any]:
    """Load the approved design and return its cost-adjusted copy."""
    source = Path(path) if path is not None else Path(__file__).with_name("approved_design.json")
    with source.open("r", encoding="utf-8") as stream:
        approved = json.load(stream)
    return apply_costs(approved)
