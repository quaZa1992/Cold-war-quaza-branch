# IMPERIA COLD WAR — Private Cyprus domestic native-engine fixture.
"""Build isolated assertions against installed Cyprus focus runtime helpers."""
from __future__ import annotations


def _slot_counter(variable: str, maximum: int = 60) -> str:
    """Count native headroom through free_building_slots trigger thresholds.

    The engine exposes no direct scripted variable for extra shared slots. For
    ordinary shared buildings, capacity delta is free slots delta plus the
    tested building-level delta. Province forts do not consume a shared slot,
    so their capacity delta is the free-slot delta alone.
    """
    rows = [f"set_variable = {{ {variable} = 0 }}"]
    for threshold in range(maximum):
        rows.append(
        "if = { limit = { free_building_slots = { building = industrial_complex "
        f"size > {threshold} include_locked = no }} }} "
            f"add_to_variable = {{ {variable} = 1 }} }}"
        )
    return "\n".join(rows)


def _province_level_counter(variable: str, building: str, province: int, maximum: int = 10) -> str:
    """Count province fort levels in state scope through native triggers."""
    rows = [f"set_variable = {{ {variable} = 0 }}"]
    for threshold in range(maximum):
        rows.append(
            "if = { limit = { any_province_building_level = { province = { id = "
            f"{province} }} building = {building} level > {threshold} }} }} "
            f"add_to_variable = {{ {variable} = 1 }} }}"
        )
    return "\n".join(rows)


def _snapshot(state: int, key: str, building: str, province: int | None = None) -> str:
    level = (
        _province_level_counter(f"CYP_R2_ENGINE_{key}_level", building, province)
        if province is not None
        else f"set_variable = {{ CYP_R2_ENGINE_{key}_level = building_level@{building} }}"
    )
    return f"{state} = {{\n{level}\n{_slot_counter(f'CYP_R2_ENGINE_{key}_slots')}\n}}\n"


def _delta(state: int, key: str, building: str, building_delta: bool, province: int | None = None) -> str:
    level_after = (
        _province_level_counter(f"CYP_R2_ENGINE_{key}_level_after", building, province)
        if province is not None
        else f"set_variable = {{ CYP_R2_ENGINE_{key}_level_after = building_level@{building} }}"
    )
    rows = [
        f"{state} = {{",
        level_after,
        f"set_variable = {{ CYP_R2_ENGINE_{key}_level_delta = CYP_R2_ENGINE_{key}_level_after }}",
        f"subtract_from_variable = {{ CYP_R2_ENGINE_{key}_level_delta = CYP_R2_ENGINE_{key}_level }}",
        f'log = "CYP_R2_ENGINE DIAG {key} level_delta=[?CYP_R2_ENGINE_{key}_level_delta]"',
        "}",
        f"{state} = {{",
        f"{_slot_counter(f'CYP_R2_ENGINE_{key}_slots_after')}",
        f"set_variable = {{ CYP_R2_ENGINE_{key}_capacity_delta = CYP_R2_ENGINE_{key}_slots_after }}",
        f"subtract_from_variable = {{ CYP_R2_ENGINE_{key}_capacity_delta = CYP_R2_ENGINE_{key}_slots }}",
        f'log = "CYP_R2_ENGINE DIAG {key} slots_before=[?CYP_R2_ENGINE_{key}_slots] slots_after=[?CYP_R2_ENGINE_{key}_slots_after] capacity_delta=[?CYP_R2_ENGINE_{key}_capacity_delta]"',
    ]
    if building_delta:
        rows.append(f"add_to_variable = {{ CYP_R2_ENGINE_{key}_capacity_delta = CYP_R2_ENGINE_{key}_level_delta }}")
    rows.extend(["}"])
    return "\n".join(rows)


def build(check):
    """Return fixture-only native effects, ready to insert in a CYP effect scope.

    The fixture seeds only its own funds, prerequisite receipts, confidence,
    and communal assent. It calls the installed focus apply helpers so the
    tested building grants and party programmes use production runtime code.
    """
    p = "COLDWAR_CYP_R2_"
    rows = [
        "# Fixture-only values and prerequisite receipts. Never add to country history.",
        "set_variable = { treasury = 1000 }",
        "set_variable = { gdp_total = 10 }",
        "set_variable = { COLDWAR_CYP_R2_communal_confidence = 50 }",
        "set_country_flag = COLDWAR_CYP_R2_greek_delegation_assent",
        "set_country_flag = COLDWAR_CYP_R2_turkish_delegation_assent",
        check("domestic_fixture_context", "tag = CYP original_tag = CYP IMP_is_1970_scenario = yes has_country_flag = COLDWAR_CYP_R2_initialized"),
        "",
        "# Party programmes: apply each branch's true entry focus under its native party slot.",
        "set_politics = { ruling_party = democratic elections_allowed = yes }",
        "set_variable = { ruling_party = 1 }",
        p + "presidential_service_apply = yes",
        p + "refresh_programmes = yes",
        check("party1_entry_completed", "has_country_flag = COLDWAR_CYP_R2_presidential_service_enacted"),
        check("party1_programme_active", "has_dynamic_modifier = { modifier = COLDWAR_CYP_R2_programme_presidential_programme }") ,
        "set_politics = { ruling_party = democratic elections_allowed = yes }",
        "set_variable = { ruling_party = 2 }",
        p + "refresh_programmes = yes",
        check("party1_programme_removed_on_switch", "NOT = { has_dynamic_modifier = { modifier = COLDWAR_CYP_R2_programme_presidential_programme } }") ,
        p + "enterprise_apply = yes",
        p + "refresh_programmes = yes",
        check("party2_entry_completed", "has_country_flag = COLDWAR_CYP_R2_enterprise_enacted"),
        check("party2_native_outlook", "western_liberals_are_in_power = yes"),
        check("party2_programme_active", "has_dynamic_modifier = { modifier = COLDWAR_CYP_R2_programme_eniaion_economic_programme }") ,
        "set_politics = { ruling_party = communism elections_allowed = yes }",
        "set_variable = { ruling_party = 4 }",
        p + "refresh_programmes = yes",
        check("party2_programme_removed_on_switch", "NOT = { has_dynamic_modifier = { modifier = COLDWAR_CYP_R2_programme_eniaion_economic_programme } }") ,
        p + "labour_apply = yes",
        p + "refresh_programmes = yes",
        check("party4_entry_completed", "has_country_flag = COLDWAR_CYP_R2_labour_enacted"),
        check("party4_native_outlook", "emerging_communist_state_are_in_power = yes"),
        check("party4_programme_active", "has_dynamic_modifier = { modifier = COLDWAR_CYP_R2_programme_akel_social_programme }") ,
        "set_politics = { ruling_party = democratic elections_allowed = yes }",
        "set_variable = { ruling_party = 1 }",
        p + "refresh_programmes = yes",
        check("party4_programme_removed_on_switch", "NOT = { has_dynamic_modifier = { modifier = COLDWAR_CYP_R2_programme_akel_social_programme } }") ,
        check("party1_programme_restored", "has_dynamic_modifier = { modifier = COLDWAR_CYP_R2_programme_presidential_programme }") ,
        check("makarios_authority_restored", "has_idea = COLDWAR_CYP_R2_idea_makarios_presidential_authority"),
        "",
        "# Utilities: infrastructure plus one shared slot in owned and controlled state 146.",
        "set_country_flag = COLDWAR_CYP_R2_clinics_enacted",
        _snapshot(146, "infra", "infrastructure"),
        p + "utilities_apply = yes",
        check("infrastructure_focus_receipt", "has_country_flag = COLDWAR_CYP_R2_utilities_enacted"),
        _delta(146, "infra", "infrastructure", False),
        check("infrastructure_plus_one", "146 = { check_variable = { var = CYP_R2_ENGINE_infra_level_delta value = 1 compare = equals } }"),
        check("infrastructure_shared_capacity_plus_one", "146 = { check_variable = { var = CYP_R2_ENGINE_infra_capacity_delta value = 1 compare = equals } }"),
        "146 = { set_variable = { CYP_R2_ENGINE_infra_replay_level = building_level@infrastructure } "
        + _slot_counter("CYP_R2_ENGINE_infra_replay_slots") + " }",
        p + "utilities_apply = yes",
        "146 = { set_variable = { CYP_R2_ENGINE_infra_replay_level_after = building_level@infrastructure } "
        + _slot_counter("CYP_R2_ENGINE_infra_replay_slots_after")
        + " set_variable = { CYP_R2_ENGINE_infra_replay_level_delta = CYP_R2_ENGINE_infra_replay_level_after } "
        + "subtract_from_variable = { CYP_R2_ENGINE_infra_replay_level_delta = CYP_R2_ENGINE_infra_replay_level } "
        + "set_variable = { CYP_R2_ENGINE_infra_replay_capacity_delta = CYP_R2_ENGINE_infra_replay_slots_after } "
        + "subtract_from_variable = { CYP_R2_ENGINE_infra_replay_capacity_delta = CYP_R2_ENGINE_infra_replay_slots } }",
        check("infrastructure_replay_no_second_level", "146 = { check_variable = { var = CYP_R2_ENGINE_infra_replay_level_delta value = 0 compare = equals } }"),
        check("infrastructure_replay_no_second_slot", "146 = { check_variable = { var = CYP_R2_ENGINE_infra_replay_capacity_delta value = 0 compare = equals } }"),
        "",
        "# Workshops: industrial complex plus one slot in owned and controlled state 145.",
        "set_country_flag = COLDWAR_CYP_R2_technical_enacted",
        _snapshot(145, "factory", "industrial_complex"),
        p + "workshops_apply = yes",
        check("factory_focus_receipt", "has_country_flag = COLDWAR_CYP_R2_workshops_enacted"),
        _delta(145, "factory", "industrial_complex", True),
        check("factory_plus_one", "145 = { check_variable = { var = CYP_R2_ENGINE_factory_level_delta value = 1 compare = equals } }"),
        check("factory_shared_capacity_plus_one", "145 = { check_variable = { var = CYP_R2_ENGINE_factory_capacity_delta value = 1 compare = equals } }"),
        "145 = { set_variable = { CYP_R2_ENGINE_factory_replay_level = building_level@industrial_complex } "
        + _slot_counter("CYP_R2_ENGINE_factory_replay_slots") + " }",
        p + "workshops_apply = yes",
        "145 = { set_variable = { CYP_R2_ENGINE_factory_replay_level_after = building_level@industrial_complex } "
        + _slot_counter("CYP_R2_ENGINE_factory_replay_slots_after")
        + " set_variable = { CYP_R2_ENGINE_factory_replay_level_delta = CYP_R2_ENGINE_factory_replay_level_after } "
        + "subtract_from_variable = { CYP_R2_ENGINE_factory_replay_level_delta = CYP_R2_ENGINE_factory_replay_level } "
        + "set_variable = { CYP_R2_ENGINE_factory_replay_capacity_delta = CYP_R2_ENGINE_factory_replay_slots_after } "
        + "subtract_from_variable = { CYP_R2_ENGINE_factory_replay_capacity_delta = CYP_R2_ENGINE_factory_replay_slots } }",
        check("factory_replay_no_second_level", "145 = { check_variable = { var = CYP_R2_ENGINE_factory_replay_level_delta value = 0 compare = equals } }"),
        check("factory_replay_no_second_slot", "145 = { check_variable = { var = CYP_R2_ENGINE_factory_replay_capacity_delta value = 0 compare = equals } }"),
        "",
        "# Territorial positions: both province forts add a state slot although they consume none.",
        "set_country_flag = COLDWAR_CYP_R2_territorial_enacted",
        _snapshot(145, "bunker", "bunker", 11984),
        _snapshot(146, "coastal_fort", "coastal_bunker", 7193),
        p + "positions_apply = yes",
        check("province_fort_focus_receipt", "has_country_flag = COLDWAR_CYP_R2_positions_enacted"),
        _delta(145, "bunker", "bunker", False, 11984),
        _delta(146, "coastal_fort", "coastal_bunker", False, 7193),
        check("province_bunker_plus_one", "145 = { check_variable = { var = CYP_R2_ENGINE_bunker_level_delta value = 1 compare = equals } }"),
        check("coastal_fort_plus_one", "146 = { check_variable = { var = CYP_R2_ENGINE_coastal_fort_level_delta value = 1 compare = equals } }"),
        check("province_fort_shared_capacity_plus_one", "145 = { check_variable = { var = CYP_R2_ENGINE_bunker_capacity_delta value = 1 compare = equals } }"),
        check("coastal_fort_shared_capacity_plus_one", "146 = { check_variable = { var = CYP_R2_ENGINE_coastal_fort_capacity_delta value = 1 compare = equals } }"),
        "145 = { " + _province_level_counter("CYP_R2_ENGINE_bunker_replay_level", "bunker", 11984)
        + " " + _slot_counter("CYP_R2_ENGINE_bunker_replay_slots") + " }",
        "146 = { " + _province_level_counter("CYP_R2_ENGINE_coastal_replay_level", "coastal_bunker", 7193)
        + " " + _slot_counter("CYP_R2_ENGINE_coastal_replay_slots") + " }",
        p + "positions_apply = yes",
        "145 = { " + _province_level_counter("CYP_R2_ENGINE_bunker_replay_level_after", "bunker", 11984)
        + "set_variable = { CYP_R2_ENGINE_bunker_replay_level_delta = CYP_R2_ENGINE_bunker_replay_level_after } "
        + "subtract_from_variable = { CYP_R2_ENGINE_bunker_replay_level_delta = CYP_R2_ENGINE_bunker_replay_level } "
        + _slot_counter("CYP_R2_ENGINE_bunker_replay_slots_after")
        + " set_variable = { CYP_R2_ENGINE_bunker_replay_capacity_delta = CYP_R2_ENGINE_bunker_replay_slots_after } "
        + "subtract_from_variable = { CYP_R2_ENGINE_bunker_replay_capacity_delta = CYP_R2_ENGINE_bunker_replay_slots } }",
        "146 = { " + _province_level_counter("CYP_R2_ENGINE_coastal_replay_level_after", "coastal_bunker", 7193)
        + "set_variable = { CYP_R2_ENGINE_coastal_replay_level_delta = CYP_R2_ENGINE_coastal_replay_level_after } "
        + "subtract_from_variable = { CYP_R2_ENGINE_coastal_replay_level_delta = CYP_R2_ENGINE_coastal_replay_level } "
        + _slot_counter("CYP_R2_ENGINE_coastal_replay_slots_after")
        + " set_variable = { CYP_R2_ENGINE_coastal_replay_capacity_delta = CYP_R2_ENGINE_coastal_replay_slots_after } "
        + "subtract_from_variable = { CYP_R2_ENGINE_coastal_replay_capacity_delta = CYP_R2_ENGINE_coastal_replay_slots } }",
        check("province_bunker_replay_no_level_or_slot", "145 = { check_variable = { var = CYP_R2_ENGINE_bunker_replay_level_delta value = 0 compare = equals } check_variable = { var = CYP_R2_ENGINE_bunker_replay_capacity_delta value = 0 compare = equals } }"),
        check("coastal_fort_replay_no_level_or_slot", "146 = { check_variable = { var = CYP_R2_ENGINE_coastal_replay_level_delta value = 0 compare = equals } check_variable = { var = CYP_R2_ENGINE_coastal_replay_capacity_delta value = 0 compare = equals } }"),
    ]
    return "\n".join(rows) + "\n"
