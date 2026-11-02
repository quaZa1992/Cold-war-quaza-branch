# IMPERIA COLD WAR — France 1970 core runtime generator.
"""Build the French national tree and domestic providers as a reviewable map."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from pressure import pressure_unlocks_by_entry

PREFIX = "COLDWAR_FRA2"
PREVIOUS_DESIGN_SHA256 = "4f57a4c6e3d13eba6b7ec4129cb81fd8b9a2a645e9fac10c5ebf8d36588c18b5"
PARTY_REVISION_MIGRATION_FLAG = f"{PREFIX}_party_revision_20261029_investment_migrated"
RECOVERY_MIGRATION_FLAG = f"{PREFIX}_starting_spirit_revision_20261029_migrated"
RECOVERY_REVISION_ID = "france_1970_starting_spirit_stages_20261029"
CID_POOL_MIGRATION_FLAG = f"{PREFIX}_CID_pool_20261030_migrated"
PARTY_TRIGGERS = {
    "udr": "western_conservatism_are_in_power",
    "ri": "western_liberals_are_in_power",
    "centre": "neutrality_neutral_conservatism_are_in_power",
    "radical": "neutrality_neutral_libertarians_are_in_power",
    "ps": "western_social_democrats_are_in_power",
    "pcf": "emerging_communist_state_are_in_power",
    "psu": "neutrality_neutral_social_are_in_power",
    "ecology": "neutrality_neutral_green_are_in_power",
    "right": "nationalist_right_wing_populists_are_in_power",
}
PARTY_NAMES = {
    "udr": "conservatism_L", "ri": "liberalism_L",
    "centre": "Neutral_conservatism_L", "radical": "Neutral_Libertarian_L",
    "ps": "socialism_L", "pcf": "communist_state_L",
    "psu": "neutral_Social_L", "ecology": "Neutral_green_L",
    "right": "Nat_Populism_L",
}
FILTERS = {
    "economy": "FOCUS_FILTER_INDUSTRY",
    "defence": "FOCUS_FILTER_RESEARCH FOCUS_FILTER_ARMY",
    "udr_nato": "FOCUS_FILTER_RESEARCH FOCUS_FILTER_ARMY",
}
CUSTOM_MODIFIER_TT = {
    "army_org_factor": "$MODIFIER_ARMY_ORG_FACTOR$",
    "production_factory_efficiency_gain_factor": "$MODIFIER_PRODUCTION_FACTORY_EFFICIENCY_GAIN_FACTOR$",
    "production_factory_max_efficiency_factor": "$MODIFIER_PRODUCTION_FACTORY_MAX_EFFICIENCY_FACTOR$",
    "production_speed_infrastructure_factor": "$modifier_production_speed_infrastructure_factor$",
    "research_speed_factor": "$MODIFIER_RESEARCH_SPEED_FACTOR$",
}

PROSE_CONDITIONS = {
    "CID dated identity; before 5 October 1972": ("date < 1972.10.5", False, None),
    "FN identity; founded on or after 5 October 1972": ("date > 1972.10.4", False, None),
    "FN identity": ("date > 1972.10.4", False, None),
    "Actual civil nuclear technology and reactor construction capacity": (
        f"{PREFIX}_nuclear_construction_ready = yes", True,
        f"{PREFIX}_nuclear_construction_ready_tt"),
    "Chosen civil nuclear strategy: a supplied French reactor operates; or the funded diversified generation and conservation programme is in place": (
        f"{PREFIX}_oil_strategy_ready = yes", True,
        f"{PREFIX}_oil_strategy_ready_tt"),
    "Both countries have the actual active Algerian Energy and Industrial Cooperation spirit": (
        f"{PREFIX}_algeria_energy_active = yes", True,
        f"{PREFIX}_algeria_energy_active_tt"),
}


def _num(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.5f}".rstrip("0").rstrip(".") or "0"
    return str(value)


def _parent_ideas(node: dict[str, Any]) -> list[str]:
    values = []
    for condition in node.get("conditions", []) + node.get("activation_conditions", []):
        match = re.fullmatch(r"has_idea\s*=\s*(COLDWAR_FRA2_[A-Za-z0-9_]+)", condition)
        if match and match.group(1) != "NATO_member":
            values.append(match.group(1))
    return sorted(set(values))


def _pool_key(node: dict[str, Any]) -> str:
    if node.get("modifier_pool"):
        return node["modifier_pool"]
    parents = _parent_ideas(node)
    if not parents:
        return node["group"]
    suffix = "_and_".join(p.removeprefix(PREFIX + "_").removesuffix("_france") for p in parents)
    return f"{node['group']}_parent_{suffix}"


def _block(key: str, *rows: str) -> str:
    body = "\n".join(str(row) for row in rows if row)
    return f"{key} = {{\n" + "\n".join("\t" + line for line in body.splitlines()) + "\n}"


def _loc(loc: dict[str, str], key: str, value: str) -> str:
    loc[key] = value
    return key


def _file(files: dict[str, str], path: str, body: str) -> None:
    files[path] = "# IMPERIA COLD WAR — France 1970 runtime output.\n" + body.rstrip() + "\n"


def _modifier_tooltip(modifier: str) -> str:
    return f"{PREFIX}_modifier_{modifier}_tt" if modifier in CUSTOM_MODIFIER_TT else f"{modifier}_tt"


def _previous_approved_design() -> dict[str, Any]:
    baseline_path = Path(__file__).with_name("approved_design.json")
    payload = baseline_path.read_bytes()
    actual_hash = hashlib.sha256(payload).hexdigest()
    if actual_hash != PREVIOUS_DESIGN_SHA256:
        raise ValueError(f"France party migration baseline hash mismatch: {actual_hash}")
    return json.loads(payload.decode("utf-8"))


def _modifier_pool_map(design: dict[str, Any]) -> dict[str, set[str]]:
    pools: dict[str, set[str]] = defaultdict(set)
    for node in design.get("nodes", []):
        pool = _pool_key(node)
        pools[pool].update(
            effect["key"] for effect in node.get("effects", [])
            if effect.get("kind") == "modifier"
        )
    return pools


def _retired_modifier_pools(old_design: dict[str, Any], new_design: dict[str, Any]) -> dict[str, set[str]]:
    old_pools = _modifier_pool_map(old_design)
    new_pools = _modifier_pool_map(new_design)
    return {pool: modifiers for pool, modifiers in old_pools.items() if pool not in new_pools}


def _party_modifier_rebuild(new_design: dict[str, Any], old_design: dict[str, Any]) -> list[str]:
    """Rebuild earned programme pools without replaying any one-time reward.

    The old approved snapshot supplies the exact stale variable names to clear.
    Current values come only from current non-offer focus modifiers and their
    existing `earned` receipts. Offer focuses are intentionally excluded.
    """
    variables: set[tuple[str, str]] = set()
    for design in (old_design, new_design):
        for node in design.get("nodes", []):
            pool = _pool_key(node)
            variables.update(
                (pool, effect["key"])
                for effect in node.get("effects", [])
                if effect.get("kind") == "modifier"
            )
    rows: list[str] = []
    for pool, modifier in sorted(variables):
        variable = f"{PREFIX}_{pool}_{modifier}"
        rows.append(f"set_variable = {{ {variable} = 0 tooltip = {_modifier_tooltip(modifier)} }}")
    for node in new_design.get("nodes", []):
        if node.get("offer"):
            continue
        pool = _pool_key(node)
        for effect in node.get("effects", []):
            if effect.get("kind") != "modifier" or float(effect["value"]) == 0:
                continue
            variable = f"{PREFIX}_{pool}_{effect['key']}"
            rows.append(_block("if", _block("limit", f"has_country_flag = {PREFIX}_earned_{node['key']}"),
                f"add_to_variable = {{ {variable} = {_num(effect['value'])} tooltip = {_modifier_tooltip(effect['key'])} }}"))
    return rows


def _cid_pool_rebuild_rows(new_design: dict[str, Any], old_design: dict[str, Any]) -> list[str]:
    """Move earned dated CID deltas out of legacy Right variables without replay."""
    variables: set[tuple[str, str]] = set()
    for source_design in (old_design, new_design):
        for node in source_design.get("nodes", []):
            pool = _pool_key(node)
            if pool not in {"right", "CID"}:
                continue
            variables.update(
                (pool, effect["key"])
                for effect in node.get("effects", [])
                if effect.get("kind") == "modifier"
            )
    rows = [
        f"set_variable = {{ {PREFIX}_{pool}_{modifier} = 0 tooltip = {_modifier_tooltip(modifier)} }}"
        for pool, modifier in sorted(variables)
    ]
    for node in new_design.get("nodes", []):
        if node.get("offer"):
            continue
        pool = _pool_key(node)
        if pool not in {"right", "CID"}:
            continue
        for effect in node.get("effects", []):
            if effect.get("kind") != "modifier" or float(effect["value"]) == 0:
                continue
            variable = f"{PREFIX}_{pool}_{effect['key']}"
            rows.append(_block("if", _block("limit", f"has_country_flag = {PREFIX}_earned_{node['key']}"),
                f"add_to_variable = {{ {variable} = {_num(effect['value'])} tooltip = {_modifier_tooltip(effect['key'])} }}"))
    rows.append("force_update_dynamic_modifier = yes")
    return rows


def _recovery_migration_rows(design: dict[str, Any]) -> list[str]:
    """Reconcile prior earned removals into staged spirit state, with no replay."""
    rows: list[str] = []

    def earned(*keys: str) -> str:
        return _block("OR", *[f"has_country_flag = {PREFIX}_earned_{key}" for key in keys])

    presidency = f"{PREFIX}_presidency"
    institutional = f"{PREFIX}_institutional_balance_residual"
    civic_done = f"has_country_flag = {PREFIX}_earned_civic_settlement"
    rows.append(_block("if", _block("limit", earned("executive", "parliament"),
        f"NOT = {{ {civic_done} }}", f"NOT = {{ has_idea = {institutional} }}"),
        _block("if", _block("limit", f"has_idea = {presidency}"),
            _block("swap_ideas", f"remove_idea = {presidency}", f"add_idea = {institutional}")),
        _block("else", f"add_ideas = {institutional}")))
    rows.append(_block("if", _block("limit", civic_done, f"has_idea = {institutional}"),
        f"remove_ideas = {institutional}"))

    education = f"{PREFIX}_education"
    education_residual = f"{PREFIX}_higher_education_pressures"
    rows.append(_block("if", _block("limit", earned("technical_colleges", "mass_universities"),
        f"NOT = {{ has_idea = {education_residual} }}"),
        _block("if", _block("limit", f"has_idea = {education}"),
            _block("swap_ideas", f"remove_idea = {education}", f"add_idea = {education_residual}")),
        _block("else", f"add_ideas = {education_residual}")))

    oil = f"{PREFIX}_oil"
    oil_intermediate = f"{PREFIX}_oil_dependence_intermediate"
    oil_residual = f"{PREFIX}_oil_dependence_residual"
    rows.append(_block("if", _block("limit", earned("oil_resilience"),
        f"NOT = {{ has_idea = {oil_residual} }}"),
        f"remove_ideas = {oil}", f"remove_ideas = {oil_intermediate}", f"add_ideas = {oil_residual}"))
    rows.append(_block("if", _block("limit", earned("nuclear_scale", "diverse_energy"),
        f"NOT = {{ has_country_flag = {PREFIX}_earned_oil_resilience }}",
        f"NOT = {{ has_idea = {oil_intermediate} }}"),
        _block("if", _block("limit", f"has_idea = {oil}"),
            _block("swap_ideas", f"remove_idea = {oil}", f"add_idea = {oil_intermediate}")),
        _block("else", f"add_ideas = {oil_intermediate}")))
    return rows


def _gdp(effect: dict[str, Any]) -> str:
    share = effect.get("runtime_share_literal", f"{float(effect['percent']) / 100:.5f}")
    return "\n".join((
        f"set_temp_variable = {{ treasury_change = {{ value = gdp_total multiply = {share} }} }}",
        "modify_treasury_effect = yes",
    ))


def _apply_effect(effect: dict[str, Any], node: dict[str, Any]) -> str:
    kind = effect["kind"]
    if kind == "treasury_gdp":
        return _gdp(effect)
    if kind == "modifier":
        pool = node.get("modifier_pool", node["group"])
        return f"add_to_variable = {{ {PREFIX}_{pool}_{effect['key']} = {_num(effect['value'])} tooltip = {_modifier_tooltip(effect['key'])} }}"
    if kind == "building":
        return f"{PREFIX}_build_{node['key']}_{_asset_suffix(effect)} = yes"
    if kind == "state_slots":
        native = effect.get("native_effect")
        if native != "add_extra_state_shared_building_slots":
            raise ValueError(f"Unsupported state slot effect in {node['id']}: {effect}")
        return _block(str(int(effect["state"])), f"{native} = {int(effect['amount'])}")
    if kind == "research":
        return _block("add_tech_bonus", f"name = {node['id']}_research", f"bonus = {_num(effect['bonus'])}", f"uses = {int(effect['uses'])}", f"category = {effect['category']}")
    if kind == "doctrine":
        return _block("add_doctrine_cost_reduction", f"cost_reduction = {_num(effect['reduction'])}", f"uses = {int(effect['uses'])}", f"category = {effect['category']}")
    if kind == "experience":
        service = {"army": "army", "navy": "navy", "air": "air"}[effect["service"]]
        return f"{service}_experience = {_num(effect['amount'])}"
    if kind == "political_power":
        return f"add_political_power = {_num(effect['value'])}"
    if kind == "remove_spirit":
        return f"remove_ideas = {effect['spirit']}"
    if kind == "transition_spirit":
        source, target = effect["from"], effect.get("to")
        if target is None:
            change = f"remove_ideas = {source}"
        else:
            change = _block("swap_ideas", f"remove_idea = {source}", f"add_idea = {target}")
        return _block("if", _block("limit", f"has_idea = {source}"), change)
    if kind == "unlock_decision":
        return f"unlock_decision_tooltip = {effect['id']}"
    if kind == "faction_opinion":
        provider = effect.get("provider")
        if not provider:
            raise ValueError(f"No native opinion provider for {node['id']}: {effect}")
        return f"set_temp_variable = {{ temp_opinion = {_num(effect['value'])} }}\n{provider} = yes"
    raise ValueError(f"Unsupported effect kind {kind!r} in {node['id']}")


def _preview_building(effect: dict[str, Any]) -> str:
    state = int(effect["state"])
    rows = [f"add_extra_state_shared_building_slots = {int(effect.get('slots', effect['amount']))}"]
    construction = [f"type = {effect['building']}", f"level = {int(effect['amount'])}", "instant_build = yes"]
    if effect.get("province") is not None:
        construction.append(f"province = {int(effect['province'])}")
    rows.append(_block("add_building_construction", *construction))
    return _block(str(state), *rows)


def _preview_effect(effect: dict[str, Any], node: dict[str, Any]) -> str:
    if effect["kind"] == "building":
        return _preview_building(effect)
    if effect["kind"] == "transition_spirit":
        source, target = effect["from"], effect.get("to")
        if target is None:
            return f"remove_ideas = {source}"
        return _block("swap_ideas", f"remove_idea = {source}", f"add_idea = {target}")
    if effect["kind"] == "state_slots":
        native = effect.get("native_effect")
        if native != "add_extra_state_shared_building_slots":
            raise ValueError(f"Unsupported state slot preview in {node['id']}: {effect}")
        return _block(str(int(effect["state"])), f"{native} = {int(effect['amount'])}")
    # MD's helper previews signed opinion points and its native adjustments.
    # A value such as -5 is not a fractional percentage modifier.
    return _apply_effect(effect, node)


def _asset_suffix(effect: dict[str, Any]) -> str:
    state = int(effect["state"])
    province = effect.get("province")
    location = f"province_{int(province)}" if province is not None else "state"
    return f"state_{state}_{location}_{effect['building']}"


def _asset_helper_id(key: str, effect: dict[str, Any]) -> str:
    return f"{PREFIX}_build_{key}_{_asset_suffix(effect)}"


def _decision_key(decision_id: str) -> str:
    """Return the local suffix for both legacy FRA2 and party FRA2P decisions."""
    if decision_id.startswith(PREFIX + "P_"):
        return decision_id[len(PREFIX + "P_"):]
    if decision_id.startswith(PREFIX + "_"):
        return decision_id[len(PREFIX + "_"):]
    raise ValueError(f"Unexpected France decision ID: {decision_id}")


def _decision_conditions(d: dict[str, Any], key: str, did: str) -> list[str]:
    """Resolve authored decision gates to strict native trigger rows."""
    if d.get("runtime_guards"):
        guards = d["runtime_guards"]
        for guard in guards:
            if not isinstance(guard, str) or "=" not in guard or guard.count("{") != guard.count("}"):
                raise ValueError(f"Malformed native runtime guard for {did}: {guard!r}")
        state = 62 if key == "participation_workshops" else 54 if key == "regional_conversion" else None
        predecessor = {
            "participation_workshops": f"has_completed_focus = {PREFIX}_participation",
            "regional_conversion": f"has_completed_focus = {PREFIX}_public_banks",
        }.get(key)
        if key == "regional_conversion":
            predecessor = f"OR = {{ has_completed_focus = {PREFIX}_public_banks has_completed_focus = {PREFIX}_ps_conversion_boards }}"
        building = {"participation_workshops": "offices", "regional_conversion": "industrial_complex"}.get(key)
        contracted_conditions: dict[str, list[str]] = {}
        if state and predecessor and building:
            contracted_conditions = {
                ("Gaullist Participation" if key == "participation_workshops" else "Public Bank Credit") + " completed": [predecessor],
                "Public Bank Credit or Conversion Boards completed": [predecessor],
                ("western_conservatism_are_in_power" if key == "participation_workshops" else "western_social_democrats_are_in_power") + " = yes": [
                    ("western_conservatism_are_in_power" if key == "participation_workshops" else "western_social_democrats_are_in_power") + " = yes"],
                ("Own and fully control Rhone-Alpes (62)" if key == "participation_workshops" else "Own and fully control Hauts-de-France (54)"): [
                    f"owns_state = {state}", f"has_full_control_of_state = {state}"],
                ("Native office capacity" if key == "participation_workshops" else "Native civilian-factory capacity"): [
                    f"{state} = {{ check_variable = {{ var = building_level@{building} value = 49 compare = less_than_or_equals }} }}"],
                "Once only": [f"NOT = {{ has_country_flag = {did}_completed }}"],
            }
        for condition in d.get("conditions", []):
            expected = contracted_conditions.get(condition)
            if expected is None:
                if condition in PARTY_TRIGGERS.values():
                    expected = [condition]
                else:
                    raise ValueError(f"Unmapped authored condition for {did}: {condition!r}")
            if any(row not in guards for row in expected):
                raise ValueError(f"Authored condition is missing from runtime guards for {did}: {condition!r}")
        return list(dict.fromkeys(guards))

    checks = [f"{PREFIX}_is_1970 = yes", f"NOT = {{ has_country_flag = {did}_completed }}"]
    for condition in d.get("conditions", []):
        if condition == "Energy Review completed":
            checks.append(f"has_completed_focus = {PREFIX}_energy_review")
        elif condition == "Accelerated Nuclear Programme completed":
            checks.append(f"has_completed_focus = {PREFIX}_nuclear_scale")
        elif condition == "Uses existing native Community voting and admission decisions; no unilateral membership award":
            checks.append(f"has_completed_focus = {PREFIX}_community_entry")
        elif condition == "Actual reactor construction technology":
            checks.append("has_tech = reactor1")
        elif condition == "Own and control Loire (59)":
            checks.extend(["owns_state = 59", "controls_state = 59"])
        elif condition == "Native reactor and shared-slot capacity" or condition == "Once only":
            continue
        elif condition.startswith("has_idea = ") or " = yes" in condition:
            checks.append(condition)
        else:
            raise ValueError(f"Unmapped decision condition for {did}: {condition!r}")
    return list(dict.fromkeys(checks))


def _asset_predicate(effect: dict[str, Any]) -> str:
    state = int(effect["state"])
    if effect["kind"] == "state_slots":
        return "\n".join((f"owns_state = {state}", f"controls_state = {state}", f"has_full_control_of_state = {state}"))
    building = effect["building"]
    amount = int(effect["amount"])
    province = effect.get("province")
    caps = {
        "infrastructure": 6, "industrial_complex": 50, "offices": 50,
        "agriculture_district": 10, "arms_factory": 35, "fossil_powerplant": 20,
        "internet_station": 11, "dockyard": 20, "naval_base": 10,
        "nuclear_reactor": 20,
    }
    cap = caps[building]
    rows = [
        f"owns_state = {state}",
        f"controls_state = {state}",
        f"has_full_control_of_state = {state}",
    ]
    state_checks = []
    if province is None:
        state_checks.append(f"check_variable = {{ var = building_level@{building} value = {cap - amount} compare = less_than_or_equals }}")
    else:
        rows.append(f"controls_province = {int(province)}")
        state_checks.append(_block("any_province_building_level",
            _block("province", f"id = {int(province)}"), f"building = {building}", f"level < {cap - amount + 1}"))
    rows.append(_block(str(state), *state_checks))
    return "\n".join(rows)


def _asset_helper(node: dict[str, Any], effect: dict[str, Any]) -> str:
    key = node["key"]
    state = int(effect["state"])
    building = effect["building"]
    amount = int(effect["amount"])
    slots = int(effect.get("slots", amount))
    province = effect.get("province")
    suffix = _asset_suffix(effect)
    helper = _asset_helper_id(key, effect)
    checks = [f"NOT = {{ has_country_flag = {PREFIX}_asset_{key}_{suffix} }}", _asset_predicate(effect)]
    shares_slots = building in {"industrial_complex", "offices", "agriculture_district", "arms_factory", "dockyard"}
    construction = _block("add_building_construction", f"type = {building}", f"level = {amount}", "instant_build = yes", f"province = {province}" if province is not None else "")
    state_rows = [f"add_extra_state_shared_building_slots = {slots}"]
    if shares_slots:
        state_rows.append(_block("if", _block("limit", _block("free_building_slots", f"building = {building}", f"size > {amount - 1}", "include_locked = no")), construction, f"ROOT = {{ set_country_flag = {PREFIX}_asset_{key}_{suffix} }}"))
    else:
        state_rows.extend([construction, f"ROOT = {{ set_country_flag = {PREFIX}_asset_{key}_{suffix} }}"])
    apply = _block(str(state), *state_rows)
    return _block(helper, _block("if", _block("limit", *checks), apply))


def _node_guard(node: dict[str, Any]) -> list[str]:
    rows = [f"{PREFIX}_is_1970 = yes", f"NOT = {{ has_country_flag = {PREFIX}_earned_{node['key']} }}"]
    if any(e["kind"] == "treasury_gdp" for e in node.get("effects", [])):
        rows.append("check_variable = { gdp_total > 0 }")
    group = node["group"]
    if group in PARTY_TRIGGERS:
        rows.append(f"{PARTY_TRIGGERS[group]} = yes")
    if group == "udr_nato":
        rows.append("has_idea = NATO_member")
        rows.append(f"{PARTY_TRIGGERS['udr']} = yes")
    for condition, _, _ in _condition_specs(node):
        if condition not in rows:
            rows.append(condition)
    rows.extend(
        f"has_idea = {source}"
        for source in dict.fromkeys(
            effect["from"] for effect in node.get("effects", [])
            if effect.get("kind") == "transition_spirit"
        )
    )
    for effect in node.get("effects", []):
        if effect.get("kind") == "state_slots":
            state = int(effect["state"])
            for guard in (f"owns_state = {state}", f"controls_state = {state}", f"has_full_control_of_state = {state}"):
                if guard not in rows:
                    rows.append(guard)
    for parent_group in node.get("prerequisites", []):
        rows.append(_block("OR", *[f"has_completed_focus = {PREFIX}_{p}" for p in parent_group]))
    rows.extend(f"NOT = {{ has_completed_focus = {PREFIX}_{x} }}" for x in node.get("exclusions", []))
    if any(e["kind"] == "building" for e in node.get("effects", [])):
        rows.append(f"{PREFIX}_assets_ready_{node['key']} = yes")
    return rows


def _condition_specs(node: dict[str, Any]) -> list[tuple[str, bool, str | None]]:
    """Map authored requirement descriptions to executable, reviewed triggers.

    The design includes a small number of human-readable requirements. They
    must never be copied into HOI trigger blocks as though they were script.
    This is deliberately strict so a new prose condition fails generation.
    """
    raw_conditions = (
        [(raw, True) for raw in node.get("conditions", [])]
        + [(raw, True) for raw in node.get("activation_conditions", [])]
        + [(raw, False) for raw in node.get("reward_guards", [])]
        + [(raw, True) for raw in (node.get("offer", {}) or {}).get("activation_conditions", [])]
    )
    specs: list[tuple[str, bool, str | None]] = []
    seen: set[str] = set()
    for raw, default_visible in raw_conditions:
        if raw in PROSE_CONDITIONS:
            expression, visible, tooltip = PROSE_CONDITIONS[raw]
        else:
            expression, visible, tooltip = raw, default_visible, None
            if not isinstance(raw, str) or "=" not in raw or raw.count("{") != raw.count("}"):
                raise ValueError(f"Unmapped prose or malformed condition in {node['key']}: {raw!r}")
        if expression not in seen:
            specs.append((expression, visible, tooltip))
            seen.add(expression)
    return specs


def _condition_tooltip_for_nested(expression: str, node: dict[str, Any], index: int, loc: dict[str, str]) -> str | None:
    match = re.fullmatch(r"\s*([A-Z]{3})\s*=\s*\{\s*(has_tech|has_idea)\s*=\s*([A-Za-z0-9_]+)\s*\}\s*", expression)
    if not match:
        return None
    tag, kind, value = match.groups()
    if kind == "has_tech":
        title = {"internet_1": "1G Internet Technology"}.get(value, value.replace("_", " ").title())
        phrase = f"[{tag}.GetName] has completed {title}."
    elif value == "NATO_member":
        phrase = f"[{tag}.GetName] is a member of NATO."
    elif value == "COLDWAR_FRA2_algeria_energy_ALG":
        phrase = "Algeria has the active Algerian Energy and Industrial Cooperation spirit."
    else:
        phrase = f"[{tag}.GetName] holds the required active programme."
    key = f"{PREFIX}_{node['key']}_external_requirement_{index}"
    loc[key] = phrase
    return key


def _visible_requirements(node: dict[str, Any], loc: dict[str, str]) -> tuple[list[str], list[str]]:
    visible: list[str] = []
    hidden: list[str] = []
    group = node["group"]
    if group in PARTY_TRIGGERS:
        visible.append(f"{PARTY_TRIGGERS[group]} = yes")
    if group == "udr_nato":
        visible.append(f"{PARTY_TRIGGERS['udr']} = yes")

    seen = set(visible)
    for index, (condition, is_visible, tooltip) in enumerate(_condition_specs(node)):
        if condition in seen:
            continue
        seen.add(condition)
        if not is_visible:
            hidden.append(condition)
            continue
        tooltip = tooltip or _condition_tooltip_for_nested(condition, node, index, loc)
        if tooltip:
            visible.append(_block("custom_trigger_tooltip", f"tooltip = {tooltip}", condition))
        else:
            visible.append(condition)
    return visible, hidden


def _focus_search_filters(node: dict[str, Any]) -> str:
    """Choose native search tags, keeping reciprocal offers foreign-policy led."""
    if node["group"] in FILTERS:
        return FILTERS[node["group"]]
    offer = node.get("offer")
    if not offer:
        return "FOCUS_FILTER_POLITICAL"

    effects = []
    for side in ("france", "recipient"):
        effects.extend((offer.get(side) or {}).get("effects", []))
    categories = {str(e.get("category", "")).lower() for e in effects if e.get("kind") in {"research", "doctrine"}}
    services = {str(e.get("service", "")).lower() for e in effects if e.get("kind") == "experience"}
    if "air" in services or any("aircraft" in category for category in categories):
        domain = "FOCUS_FILTER_AIRCRAFT"
    elif "navy" in services or any("naval_doctrine" in category for category in categories):
        domain = "FOCUS_FILTER_NAVY_XP"
    elif "army" in services or any("land_doctrine" in category for category in categories):
        domain = "FOCUS_FILTER_ARMY"
    elif any(e.get("kind") == "research" for e in effects):
        domain = "FOCUS_FILTER_RESEARCH"
    elif any(e.get("kind") == "building" for e in effects):
        domain = "FOCUS_FILTER_INDUSTRY"
    else:
        domain = "FOCUS_FILTER_INDUSTRY"
    return f"FOCUS_FILTER_FOREIGN_POLICY {domain}"


def _decision_file(design: dict[str, Any], loc: dict[str, str]) -> tuple[str, str, list[str], list[str]]:
    helper_bodies = []
    timed_ideas = []
    decisions = []
    descriptions = {
        "energy_audit": "French industry depends heavily on imported fuel. Review supply, transport and demand before a disruption reaches public services.",
        "fund_reactor": "Begin the Loire project only after France has completed reactor construction research and can add another unit within the area's native capacity.",
        "community_negotiations": "Use the Community's established procedures to pursue enlargement and institutional reform. Membership and treaty decisions remain subject to their existing votes.",
        "participation_workshops": "Support practical worker participation through regional workshops in Rhône-Alpes. The programme funds technical instruction and administrative capacity.",
        "regional_conversion": "Direct public-bank credit toward industrial renewal in Hauts-de-France. The grant supports a production site and technical instruction.",
    }
    for d in design.get("decisions", []):
        did = d["id"]
        key = _decision_key(did)
        loc[did] = d["title"]
        loc[did + "_desc"] = d.get("description", descriptions.get(key, "A national measure with the requirements shown."))
        checks = _decision_conditions(d, key, did)
        assets = [e for e in d.get("effects", []) if e["kind"] == "building"]
        asset_check = f"{PREFIX}_assets_ready_{key} = yes" if assets else ""
        if asset_check and asset_check not in checks:
            checks.append(asset_check)
        if any(e["kind"] == "treasury_gdp" for e in d.get("effects", [])):
            gdp_check = "check_variable = { gdp_total > 0 }"
            if gdp_check not in checks:
                checks.append(gdp_check)
        # Party gates are player-facing native MD predicates. Scenario, replay,
        # predecessor, GDP and physical-capacity receipts remain runtime guards.
        for condition in d.get("conditions", []):
            if condition in PARTY_TRIGGERS.values() and condition not in checks:
                raise ValueError(f"Party trigger missing from runtime guards for {did}: {condition}")
        preview, actual = [], []
        for effect in d.get("effects", []):
            if effect["kind"] == "building":
                helper_bodies.append(_asset_helper({"key": key}, effect))
                actual.append(f"{PREFIX}_build_{key}_{_asset_suffix(effect)} = yes")
                preview.append(_preview_building(effect))
            elif effect["kind"] == "modifier":
                continue
            else:
                preview.append(_preview_effect(effect, {"id": did, "key": key, "group": "institutions"}))
                actual.append(_apply_effect(effect, {"id": did, "key": key, "group": "institutions"}))
        modifiers = [e for e in d.get("effects", []) if e["kind"] == "modifier"]
        if modifiers:
            timed = f"{did}_timed"
            loc[timed] = d["title"]
            loc[timed + "_desc"] = "A temporary national programme applies these policy changes for the stated duration."
            mod_rows = [f"{e['key']} = {_num(e['value'])}" for e in modifiers]
            idea = _block(timed, "picture = political_reform", "allowed = { original_tag = FRA }", "removal_cost = -1", _block("modifier", *mod_rows))
            timed_ideas.append(idea)
            days = int(d.get("days", 730))
            for effect in modifiers:
                preview.append(f"add_to_variable = {{ {PREFIX}_{key}_preview_{effect['key']} = {_num(effect['value'])} tooltip = {_modifier_tooltip(effect['key'])} }}")
            actual.append(_block("add_timed_idea", f"idea = {timed}", f"days = {days}"))
            preview.append(_block("add_timed_idea", f"idea = {timed}", f"days = {days}"))
        internal_checks = {
            f"{PREFIX}_is_1970 = yes",
            f"NOT = {{ has_country_flag = {did}_completed }}",
            "check_variable = { gdp_total > 0 }",
            asset_check,
        }
        internal_checks.update(
            c for c in checks if c.startswith("has_completed_focus = ")
        )
        # The composite asset tooltip conveys state/province ownership, control
        # and native capacity together without exposing implementation helpers.
        internal_checks.update(c for c in checks if c.startswith("check_variable = { var = building_level@"))
        internal_checks.update(c for c in checks if re.match(r"\s*\d+ = \{", c) and "building_level@" in c)
        visible_checks = [c for c in checks if c not in internal_checks]
        hidden_checks = [c for c in checks if c not in visible_checks]
        available_rows = [_block("hidden_trigger", *hidden_checks), *visible_checks]
        if assets:
            asset_tip = f"{PREFIX}_asset_requirement_{key}"
            available_rows.append(_block("custom_trigger_tooltip", f"tooltip = {asset_tip}", asset_check))
        decision = _block(did, "icon = GFX_decision_industry", "cost = 0",
            _block("available", *available_rows),
            _block("visible", "tag = FRA", "IMP_is_1970_scenario = yes"),
            _block("complete_effect", _block("if", _block("limit", *checks),
                _block("effect_tooltip", *preview),
                _block("hidden_effect", *actual, f"set_country_flag = {did}_completed"))))
        decisions.append(decision)
    category_id = f"{PREFIX}_domestic_programmes"
    decisions_file = _block(category_id, *decisions)
    category_file = _block(
        category_id,
        "icon = GFX_decision_category_generic_industry",
        "allowed = { original_tag = FRA }",
        "priority = 145",
        _block("visible", "tag = FRA", "IMP_is_1970_scenario = yes"),
    )
    return decisions_file, category_file, helper_bodies, timed_ideas


def build_core(design: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Return {'files': repo-relative UTF-8 text, 'loc': English entries}."""
    if design.get("recovery_revision", {}).get("id") != RECOVERY_REVISION_ID:
        raise ValueError("Apply starting_spirit_revision.apply_starting_spirit_revision() before build_core().")
    nodes = design["nodes"]
    groups = {g["id"]: g for g in design["groups"]}
    old_design = _previous_approved_design()
    retired_modifier_pools = _retired_modifier_pools(old_design, design)
    helper_ids: list[str] = []
    for node in nodes:
        helper_ids.extend(
            _asset_helper_id(node["key"], e)
            for e in node.get("effects", []) if e["kind"] == "building"
        )
    for decision in design.get("decisions", []):
        key = _decision_key(decision["id"])
        helper_ids.extend(
            _asset_helper_id(key, e)
            for e in decision.get("effects", []) if e["kind"] == "building"
        )
    if len(helper_ids) != len(set(helper_ids)):
        duplicates = sorted(k for k, count in Counter(helper_ids).items() if count > 1)
        raise ValueError(f"Duplicate building helper/receipt IDs: {duplicates}")
    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in nodes:
        by_group[node["group"]].append(node)
    nodes_runtime = {n["key"]: {**n, "modifier_pool": _pool_key(n)} for n in nodes}
    by_pool: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in nodes_runtime.values():
        by_pool[node["modifier_pool"]].append(node)
    migration_rows = _party_modifier_rebuild(design, old_design)
    for pool in sorted(retired_modifier_pools):
        modifier_id = f"{PREFIX}_{pool}_programme"
        migration_rows.append(_block("if", _block("limit", f"has_dynamic_modifier = {{ modifier = {modifier_id} }}"),
            f"remove_dynamic_modifier = {{ modifier = {modifier_id} }}"))
    migration_rows.append(f"set_country_flag = {PARTY_REVISION_MIGRATION_FLAG}")
    loc: dict[str, str] = {}
    files: dict[str, str] = {}
    effects, triggers, dynamics, focus_nodes = [], [], [], []
    pressure_unlocks = pressure_unlocks_by_entry()
    used_modifiers = {
        e["key"] for record in nodes + design.get("decisions", [])
        for e in record.get("effects", []) if e.get("kind") == "modifier"
    }
    for modifier, label in CUSTOM_MODIFIER_TT.items():
        if modifier in used_modifiers:
            loc[f"{PREFIX}_modifier_{modifier}_tt"] = f"{label}: $RIGHT|+=%1$"

    triggers.append(_block(f"{PREFIX}_is_1970", "tag = FRA", "exists = yes", "IMP_is_1970_scenario = yes"))
    for group, trigger in PARTY_TRIGGERS.items():
        triggers.append(_block(f"{PREFIX}_{group}_party", f"{trigger} = yes"))
    triggers.append(_block(
        f"{PREFIX}_nuclear_construction_ready",
        "has_tech = reactor1", "owns_state = 59", "controls_state = 59",
        "has_full_control_of_state = 59",
        _block("59", "check_variable = { var = building_level@nuclear_reactor value = 19 compare = less_than_or_equals }"),
    ))
    triggers.append(_block(
        f"{PREFIX}_oil_strategy_ready",
        _block("OR",
            _block("AND", f"has_completed_focus = {PREFIX}_nuclear_scale", "has_nuclear_reactors = yes", "check_variable = { nuclear_energy_generation > 0 }"),
            f"has_completed_focus = {PREFIX}_diverse_energy"),
    ))
    triggers.append(_block(
        f"{PREFIX}_algeria_energy_active",
        "FRA = { has_idea = COLDWAR_FRA2_algeria_energy_france }",
        "ALG = { has_idea = COLDWAR_FRA2_algeria_energy_ALG }",
    ))
    loc.update({
        f"{PREFIX}_nuclear_construction_ready_tt": "France must have reactor construction technology and room to build in Loire.",
        f"{PREFIX}_oil_strategy_ready_tt": "A French reactor must be generating power, or the funded diversified energy programme must be complete.",
        f"{PREFIX}_algeria_energy_active_tt": "France and Algeria must both have the active Algerian Energy and Industrial Cooperation agreement.",
    })
    for node in nodes:
        assets = [e for e in node.get("effects", []) if e["kind"] in {"building", "state_slots"}]
        if assets:
            triggers.append(_block(f"{PREFIX}_assets_ready_{node['key']}", *[_asset_predicate(e) for e in assets]))
            requirement_key = f"{PREFIX}_asset_requirement_{node['key']}"
            loc[requirement_key] = ("France must own and fully control the state receiving the building slots."
                if all(e["kind"] == "state_slots" for e in assets)
                else "France must own and control the relevant state and province, with room under the native building limit.")
    for decision in design.get("decisions", []):
        assets = [e for e in decision.get("effects", []) if e["kind"] == "building"]
        if assets:
            key = _decision_key(decision["id"])
            triggers.append(_block(f"{PREFIX}_assets_ready_{key}", *[_asset_predicate(e) for e in assets]))
            loc[f"{PREFIX}_asset_requirement_{key}"] = "France must own and control the relevant state, with room under the native building limit."

    for group, members in by_pool.items():
        mods = sorted({e["key"] for n in members for e in n.get("effects", []) if e["kind"] == "modifier"})
        if not mods:
            continue
        modifier = f"{PREFIX}_{group}_programme"
        base_group = members[0]["group"]
        icon_suffix = groups[base_group].get("idea_picture", "generic")
        dynamics.append(_block(modifier, f"icon = GFX_idea_{icon_suffix}", *[f"{m} = {PREFIX}_{group}_{m}" for m in mods]))
        if group == "CID":
            loc[modifier] = members[0].get("spirit_name", "CID Programme")
            loc[modifier + "_desc"] = "The Citizens and Shopkeepers Independence programme, active before 5 October 1972 while its party governs."
        elif "_parent_" in group:
            label = "NATO Agreement"
            loc[modifier] = f"{label} Programme"
            loc[modifier + "_desc"] = groups[base_group].get("context", f"The active policy programme of {label}.")

    old_groups = {group["id"]: group for group in old_design.get("groups", [])}
    for pool, modifiers in sorted(retired_modifier_pools.items()):
        base_group = pool.split("_parent_", 1)[0]
        legacy_id = f"{PREFIX}_{pool}_programme"
        icon_suffix = groups.get(base_group, old_groups.get(base_group, {})).get("idea_picture", "generic")
        dynamics.append(_block(legacy_id, f"icon = GFX_idea_{icon_suffix}",
            *[f"{modifier} = {PREFIX}_{pool}_{modifier}" for modifier in sorted(modifiers)]))
        title = groups.get(base_group, old_groups.get(base_group, {})).get("title", "France")
        loc[legacy_id] = f"{title} Programme"
        loc[legacy_id + "_desc"] = groups.get(base_group, old_groups.get(base_group, {})).get("context", "A national policy programme.")

    idea_blocks = []
    for spirit in design.get("starting_spirits", []):
        sid = spirit["id"]
        mods = [f"{e['key']} = {_num(e['value'])}" for e in spirit.get("effects", []) if e["kind"] == "modifier"]
        idea_blocks.append(_block(sid, f"picture = {spirit.get('picture', 'political_reform')}", "allowed = { original_tag = FRA }", "removal_cost = -1", _block("modifier", *mods)))
    for spirit in design.get("recovery_stages", []):
        sid = spirit["id"]
        mods = [f"{key} = {_num(value)}" for key, value in spirit["modifiers"].items()]
        idea_blocks.append(_block(sid, f"picture = {spirit.get('picture', 'political_reform')}", "allowed = { original_tag = FRA }", "removal_cost = -1", _block("modifier", *mods)))
        loc[sid] = spirit["name"]
        loc[sid + "_desc"] = spirit["description"]

    migration_effect = _block(f"{PREFIX}_migrate_party_revision",
        _block("if", _block("limit", f"{PREFIX}_is_1970 = yes", f"NOT = {{ has_country_flag = {PARTY_REVISION_MIGRATION_FLAG} }}"),
            *migration_rows))
    effects.append(migration_effect)
    cid_migration_rows = _cid_pool_rebuild_rows(design, old_design)
    # Old saves could still have the Right programme spirit attached solely
    # because one of the dated CID focuses had earned it. Rebuild both pools,
    # detach that stale container once, then the normal sync immediately below
    # reattaches Right only when a surviving Right focus receipt warrants it.
    legacy_right_modifier = f"{PREFIX}_right_programme"
    cid_migration_rows.append(_block("if", _block("limit", f"has_dynamic_modifier = {{ modifier = {legacy_right_modifier} }}"),
        f"remove_dynamic_modifier = {{ modifier = {legacy_right_modifier} }}"))
    cid_migration_rows.append(f"set_country_flag = {CID_POOL_MIGRATION_FLAG}")
    effects.append(_block(f"{PREFIX}_migrate_CID_pool",
        _block("if", _block("limit", f"{PREFIX}_is_1970 = yes", f"NOT = {{ has_country_flag = {CID_POOL_MIGRATION_FLAG} }}"),
            *cid_migration_rows)))
    recovery_migration_rows = _recovery_migration_rows(design) + [f"set_country_flag = {RECOVERY_MIGRATION_FLAG}"]
    effects.append(_block(f"{PREFIX}_migrate_starting_spirit_revision",
        _block("if", _block("limit", f"{PREFIX}_is_1970 = yes", f"NOT = {{ has_country_flag = {RECOVERY_MIGRATION_FLAG} }}"),
            *recovery_migration_rows)))
    sync_rows = [f"{PREFIX}_migrate_CID_pool = yes", f"{PREFIX}_migrate_starting_spirit_revision = yes", f"{PREFIX}_migrate_party_revision = yes"]
    for group, members in by_pool.items():
        mods = sorted({e["key"] for n in members for e in n.get("effects", []) if e["kind"] == "modifier"})
        if not mods:
            continue
        mod_id = f"{PREFIX}_{group}_programme"
        relevant = [n for n in members if any(e["kind"] == "modifier" for e in n.get("effects", []))]
        any_earned = _block("OR", *[f"has_country_flag = {PREFIX}_earned_{n['key']}" for n in relevant])
        activate = _block("if", _block("limit", any_earned),
            _block("if", _block("limit", f"NOT = {{ has_dynamic_modifier = {{ modifier = {mod_id} }} }}"),
                f"add_dynamic_modifier = {{ modifier = {mod_id} }}"))
        deactivate = _block("if", _block("limit", f"has_dynamic_modifier = {{ modifier = {mod_id} }}"), f"remove_dynamic_modifier = {{ modifier = {mod_id} }}")
        active = list(dict.fromkeys(
            condition
            for member in members
            for condition in member.get("programme_activation_conditions", [])
        ))
        base_group = members[0]["group"]
        if not active and base_group in PARTY_TRIGGERS:
            active.append(f"{PARTY_TRIGGERS[base_group]} = yes")
        if not active and base_group == "udr_nato":
            active.append(f"{PARTY_TRIGGERS['udr']} = yes")
            active.append("has_idea = NATO_member")
        for parent in _parent_ideas(members[0]):
            active.append(f"has_idea = {parent}")
        if active:
            sync_rows.append(_block("if", _block("limit", *active), activate))
            sync_rows.append(_block("else", deactivate))
        else:
            sync_rows.append(activate)
    sync_rows.append("force_update_dynamic_modifier = yes")
    effects.append(_block(f"{PREFIX}_sync_programmes", *sync_rows))
    effects.append(_block("COLDWAR_FRA2_add_domestic_weekly_expenses"))

    for node in nodes:
        key, group, nid = node["key"], node["group"], node["id"]
        body = [f"id = {nid}", f"icon = {node['icon']}",
            f"x = {int(node['offset'][0])}", f"y = {int(node['offset'][1])}"]
        if node.get("anchor"):
            anchor = node["anchor"] if node["anchor"].startswith(PREFIX + "_") else f"{PREFIX}_{node['anchor']}"
            body.append(f"relative_position_id = {anchor}")
        body += [f"cost = {_num(node['cost'])}", "cancel_if_invalid = yes", "continue_if_invalid = no"]
        body.append(_block("search_filters", _focus_search_filters(node)))
        for parents in node.get("prerequisites", []):
            body.append(_block("prerequisite", *[f"focus = {PREFIX}_{p}" for p in parents]))
        if node.get("exclusions"):
            body.append(_block("mutually_exclusive", *[f"focus = {PREFIX}_{x}" for x in node["exclusions"]]))
        visible_requirements, hidden_requirements = _visible_requirements(node, loc)
        hidden_availability = [f"{PREFIX}_is_1970 = yes", f"NOT = {{ has_country_flag = {PREFIX}_earned_{key} }}"]
        hidden_availability.extend(
            f"has_idea = {source}"
            for source in dict.fromkeys(
                effect["from"] for effect in node.get("effects", [])
                if effect.get("kind") == "transition_spirit"
            )
        )
        if any(e["kind"] == "treasury_gdp" for e in node.get("effects", [])):
            hidden_availability.append("check_variable = { gdp_total > 0 }")
        hidden_availability.extend(hidden_requirements)
        avail = [_block("hidden_trigger", *hidden_availability)]
        avail += visible_requirements
        if any(e["kind"] in {"building", "state_slots"} for e in node.get("effects", [])):
            requirement_key = f"{PREFIX}_asset_requirement_{key}"
            avail.append(_block("custom_trigger_tooltip", f"tooltip = {requirement_key}", f"{PREFIX}_assets_ready_{key} = yes"))
        body.append(_block("available", *avail))
        preview, modifier_preview, actual = [], [], []
        runtime_node = nodes_runtime[key]
        for effect in node.get("effects", []):
            if effect["kind"] == "unlock_decision" and node.get("offer"):
                continue
            if effect["kind"] == "modifier":
                modifier_preview.append(_preview_effect(effect, runtime_node))
            else:
                preview.append(_preview_effect(effect, runtime_node))
            if effect["kind"] == "building":
                effects.append(_asset_helper(node, effect))
                actual.append(f"{PREFIX}_build_{key}_{_asset_suffix(effect)} = yes")
            elif effect["kind"] == "unlock_decision" and node.get("offer"):
                continue
            else:
                actual.append(_apply_effect(effect, runtime_node))
        if any(effect.get("kind") == "transition_spirit" for effect in node.get("effects", [])):
            actual.append(f"set_country_flag = {PREFIX}_recovery_applied_{key}")
        if any(e["kind"] == "modifier" for e in node.get("effects", [])):
            mod_id = f"{PREFIX}_{runtime_node['modifier_pool']}_programme"
            preview.append(f"custom_effect_tooltip = {{ localization_key = modifies_dynamic_modifier_tt MODIFIER = {mod_id} }}")
            preview.extend(modifier_preview)
        if node.get("offer"):
            preview.append(f"COLDWAR_FRA2_offer_preview_{key} = yes")
            actual.append(f"COLDWAR_FRA2_offer_{key} = yes")
        else:
            actual.append(f"set_country_flag = {PREFIX}_earned_{key}")
        actual.append(f"{PREFIX}_sync_programmes = yes")
        helper = f"{PREFIX}_complete_{key}"
        effects.append(_block(helper, _block("if", _block("limit", *_node_guard(node)), *actual)))
        unlock_rows = [
            f"unlock_decision_tooltip = COLDWAR_FRA2_pressure_send_{tag}"
            for tag in pressure_unlocks.get(key, [])
        ]
        reward = _block("completion_reward", _block("effect_tooltip", *preview), *unlock_rows, f"hidden_effect = {{ {helper} = yes }}")
        has_setup_spending = any(e.get("kind") == "treasury_gdp" for e in node.get("effects", []))
        if node.get("offer"):
            has_setup_spending = has_setup_spending or any(
                e.get("kind") == "treasury_gdp" and e.get("once", False)
                for side in ("france", "recipient")
                for e in (node["offer"].get(side) or {}).get("effects", [])
            )
        ai_rows = ["base = 1"]
        if has_setup_spending:
            ai_rows.append(_block("modifier", "factor = 0", "has_active_mission = bankruptcy_incoming_collapse"))
        body += [reward, _block("ai_will_do", *ai_rows)]
        focus_nodes.append(_block("focus", *body))

    init_rows = []
    for spirit in design.get("starting_spirits", []):
        if spirit.get("days"):
            init_rows.append(_block("add_timed_idea", f"idea = {spirit['id']}", f"days = {int(spirit['days'])}"))
        else:
            init_rows.append(f"add_ideas = {spirit['id']}")
    effects.append(_block(f"{PREFIX}_initialize",
        _block("if", _block("limit", f"{PREFIX}_is_1970 = yes"),
            _block("if", _block("limit", f"NOT = {{ has_country_flag = {PREFIX}_initialized }}"),
                *init_rows, f"set_country_flag = {PREFIX}_initialized"),
            f"{PREFIX}_sync_programmes = yes",
            "COLDWAR_FRA2_sync_treaties = yes")))

    focus_rows = [
        f"id = {PREFIX}_1970_focus",
        "country = { factor = 0 modifier = { add = 30 original_tag = FRA IMP_is_1970_scenario = yes } }",
        "default = no", "reset_on_civilwar = no",
        f"initial_show_position = {{ x = {next(n['x'] for n in design['nodes'] if n['id'] == design.get('navigation', {}).get('initial_focus', PREFIX + '_nato_review'))} y = {next(n['y'] for n in design['nodes'] if n['id'] == design.get('navigation', {}).get('initial_focus', PREFIX + '_nato_review'))} }}",
        "continuous_focus_position = { x = 50 y = 1750 }",
    ]
    for group in design["groups"]:
        members = by_group[group["id"]]
        entry = next((n for n in members if not n.get("anchor")), members[0])
        label = group["title"] if group["id"] not in PARTY_NAMES else f"[{PARTY_NAMES[group['id']]}]"
        name = _loc(loc, f"{PREFIX}_shortcut_{group['id']}", label)
        focus_rows.append(f"shortcut = {{ name = {name} target = {entry['id']} scroll_wheel_factor = 0.80 }}")
    focus_rows.extend(focus_nodes)
    tree = _block("focus_tree", *focus_rows)

    on_actions = _block("on_actions",
        _block("on_startup", _block("effect", f"FRA = {{ {PREFIX}_initialize = yes }}")),
        _block("on_daily", _block("effect",
            _block("if", "limit = { tag = FRA IMP_is_1970_scenario = yes }",
                "COLDWAR_FRA2_sync_treaties = yes", f"{PREFIX}_sync_programmes = yes"),
            "COLDWAR_FRA2_cleanup_orphaned_recipient_ideas = yes")),
        _block("on_government_change", _block("effect", _block("if", "limit = { tag = FRA IMP_is_1970_scenario = yes }", f"{PREFIX}_sync_programmes = yes"))),
        _block("on_ruling_party_change", _block("effect", _block("if", "limit = { tag = FRA IMP_is_1970_scenario = yes }", f"{PREFIX}_sync_programmes = yes"))),
        _block("on_weekly", _block("effect", _block("if", "limit = { tag = FRA IMP_is_1970_scenario = yes }", "COLDWAR_FRA2_sync_treaties = yes", f"{PREFIX}_sync_programmes = yes"))),
    )
    decisions, decision_categories, decision_helpers, timed_ideas = _decision_file(design, loc)

    _file(files, "common/national_focus/COLDWAR_FRA2_1970_focus.txt", tree)
    _file(files, "common/scripted_effects/COLDWAR_FRA2_1970_effects.txt", "\n\n".join(effects + decision_helpers))
    _file(files, "common/scripted_triggers/COLDWAR_FRA2_1970_triggers.txt", "\n\n".join(triggers))
    _file(files, "common/dynamic_modifiers/COLDWAR_FRA2_1970_dynamic_modifiers.txt", "\n\n".join(dynamics))
    _file(files, "common/ideas/COLDWAR_FRA2_1970_ideas.txt", _block("ideas", _block("country", *(idea_blocks + timed_ideas))))
    _file(files, "common/on_actions/COLDWAR_FRA2_1970_on_actions.txt", on_actions)
    _file(files, "common/decisions/COLDWAR_FRA2_1970_decisions.txt", decisions)
    _file(files, "common/decisions/categories/COLDWAR_FRA2_1970_categories.txt", decision_categories)

    scripted_effects = files["common/scripted_effects/COLDWAR_FRA2_1970_effects.txt"]
    scripted_triggers = files["common/scripted_triggers/COLDWAR_FRA2_1970_triggers.txt"]
    provider_names = re.findall(r"^([A-Za-z0-9_]+) = \{", scripted_effects + "\n" + scripted_triggers, re.M)
    duplicates = sorted(name for name, count in Counter(provider_names).items() if count > 1)
    if duplicates:
        raise ValueError(f"Duplicate scripted effect/trigger provider IDs: {duplicates}")
    known_focus_ids = {n["id"] for n in nodes}
    emitted_scripts = "\n".join(
        value for path, value in files.items()
        if path.endswith((".txt", ".gui", ".gfx"))
    )
    unresolved_focus_refs = sorted({
        ref for ref in re.findall(r"\bhas_completed_focus\s*=\s*([A-Za-z0-9_]+)", emitted_scripts)
        if ref.startswith(PREFIX + "_") and ref not in known_focus_ids
    })
    if unresolved_focus_refs:
        raise ValueError(f"Unresolved generated focus IDs: {unresolved_focus_refs}")
    prose_conditions = {
        condition
        for node in nodes
        for condition in node.get("conditions", []) + node.get("activation_conditions", []) + node.get("reward_guards", [])
        if "=" not in condition
    }
    leaked_prose = sorted(condition for condition in prose_conditions if condition in emitted_scripts)
    if leaked_prose:
        raise ValueError(f"Authored prose leaked into executable script: {leaked_prose}")

    return {"files": files, "loc": loc}
