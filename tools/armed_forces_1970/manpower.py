"""Emit a one-time, source-backed 1970 personnel ledger.

Counts in the data are people. Script variables use thousands: HOI's fixed-point
variables cannot safely represent a large country's population or total forces
as individual people. Unknowns are omitted, never converted to zero. The native
recruitment laws and manpower pool remain authoritative unless an explicit
``free_manpower`` observation has been supplied.
"""
from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path
from typing import Any, Mapping


HERE = Path(__file__).resolve().parent
PERSONNEL_FIELDS = (
    "active_total", "army", "navy", "air_force", "marines", "paramilitary",
    "trained_reserve", "free_manpower",
)


def load_personnel() -> dict[str, Any]:
    return json.loads((HERE / "data" / "personnel.json").read_text(encoding="utf-8"))


def load_population() -> dict[str, Any]:
    return json.loads((HERE / "data" / "population.json").read_text(encoding="utf-8"))


def _people(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{label} must be a nonnegative integer count of people")
    return value


def _k(value: int) -> str:
    return format(Decimal(value) / 1000, "f").rstrip("0").rstrip(".") if value % 1000 else str(value // 1000)


def emit_country(tag: str, record: Mapping[str, Any], context: Mapping[str, Any]) -> str:
    """Return native effects to execute in country scope after its OOB is loaded.

    Context accepts owned_population, core_population, modeled_manpower,
    historical_land_manpower, and optional union_population, all in people.
    Unmodeled active personnel can include uncovered combat formations as well
    as administrative/support personnel; the residual cannot identify their
    composition. They are not an extra recruitable population grant.
    Reserve figures are starting subsets, not a separately spendable currency.
    """
    personnel = record.get("personnel") or {}
    body = [
        "# Historical starting observations; no recurring manpower reset.",
        "# Unknown personnel/reserve fields are deliberately not initialized.",
        "set_country_flag = cw1970_personnel_initialized",
    ]
    law = record.get("starting_conscription_law")
    if law is not None:
        if law not in {"no_military", "volunteer_army", "partial_draft_army", "draft_army"}:
            raise ValueError(f"{tag}: unknown native conscription law {law!r}")
        if not record.get("military_service_source_ids"):
            raise ValueError(f"{tag}: starting law requires service-policy sources")
        body.extend([
            "# Native law approximates the documented service system; no new mobilization mechanic.",
            f"add_ideas = {law}",
        ])
    for field in PERSONNEL_FIELDS:
        value = personnel.get(field)
        if value is not None:
            body.append(f"set_variable = {{ cw1970_start_{field}_k = {_k(_people(value, field))} }}")

    for key in ("owned_population", "core_population", "modeled_manpower", "historical_land_manpower", "union_population"):
        value = context.get(key)
        if value is not None:
            body.append(f"set_variable = {{ cw1970_start_{key}_k = {_k(_people(value, key))} }}")

    active = personnel.get("active_total")
    modeled = context.get("modeled_manpower")
    if active is not None and modeled is not None:
        # Above-source modeled manpower must be reported, never hidden by a
        # negative 'support' total or destruction of already deployed troops.
        support = max(0, _people(active, "active_total") - _people(modeled, "modeled_manpower"))
        excess = max(0, modeled - active)
        body.append(f"set_variable = {{ cw1970_start_unmodeled_active_k = {_k(support)} }}")
        body.append(f"set_variable = {{ cw1970_start_modeled_excess_k = {_k(excess)} }}")

    if record.get("personnel_status", "missing") == "missing":
        body.append("set_country_flag = cw1970_personnel_source_missing")
    elif record.get("personnel_scope") == "USSR_union_member":
        body.append("set_country_flag = cw1970_personnel_in_soviet_union_total")
    else:
        body.append("set_country_flag = cw1970_personnel_source_available")

    free = personnel.get("free_manpower")
    if free is not None:
        free = _people(free, "free_manpower")
        reserve = personnel.get("trained_reserve")
        if reserve is not None and free < _people(reserve, "trained_reserve"):
            raise ValueError(f"{tag}: trained reserves cannot exceed the documented total free pool")
        if not record.get("free_manpower_source_ids"):
            raise ValueError(f"{tag}: an explicit initial free pool requires sources")
        # A documented trained-reserve subtotal may define a conservative
        # initial pool estimate, with its coverage stated in the source data.
        # Bounded chunking also handles large inherited native pools without
        # multiplying a large fixed-point variable into overflow.
        body.extend([
            "# This explicit total already includes any listed trained reserves.",
            f"set_temp_variable = {{ cw1970_pool_delta_k = {_k(free)} }}",
            "subtract_from_temp_variable = { cw1970_pool_delta_k = manpower_k }",
            "set_temp_variable = { cw1970_pool_done = 0 }",
            "for_loop_effect = {",
            "\tstart = 0",
            "\tend = 4096",
            "\tvalue = cw1970_pool_iteration",
            "\tbreak = cw1970_pool_done",
            "\tif = {",
            "\t\tlimit = { check_variable = { cw1970_pool_delta_k > 1000 } }",
            "\t\tadd_manpower = 1000000",
            "\t\tsubtract_from_temp_variable = { cw1970_pool_delta_k = 1000 }",
            "\t}",
            "\telse_if = {",
            "\t\tlimit = { check_variable = { cw1970_pool_delta_k < -1000 } }",
            "\t\tadd_manpower = -1000000",
            "\t\tadd_to_temp_variable = { cw1970_pool_delta_k = 1000 }",
            "\t}",
            "\telse = { set_temp_variable = { cw1970_pool_done = 1 } }",
            "}",
            "if = {",
            "\tlimit = { check_variable = { cw1970_pool_done = 1 } }",
            "\tmultiply_temp_variable = { cw1970_pool_delta_k = 1000 }",
            "\tadd_manpower = cw1970_pool_delta_k",
            "}",
            "else = { set_country_flag = cw1970_initial_pool_adjustment_incomplete }",
        ])
    else:
        body.append("# No sourced total free pool: retain native recruitment laws and available manpower.")

    return "if = {\n\tlimit = { NOT = { has_country_flag = cw1970_personnel_initialized } }\n" + "\n".join("\t" + line for line in body) + "\n}\n"
