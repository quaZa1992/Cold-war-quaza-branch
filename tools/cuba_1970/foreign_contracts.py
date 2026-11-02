# IMPERIA COLD WAR — Cuba 1970 foreign contract compiler.
"""Compile focus-selected, recipient-consented bilateral agreements.

The frozen 120-focus concept is the data source. The public helpers are used
by compile.py for focus availability, previews, and completion rewards.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
import event_art

ROOT = Path(__file__).resolve().parents[2]
CONCEPT = json.loads((ROOT / "tools/cuba_1970/revision_design.json").read_text(encoding="utf-8"))
NODES = [n for n in CONCEPT["nodes"] if n.get("group") == "foreign" and n.get("partner")]
PARTNER_NODES = {n["key"]: n for n in NODES}
PARTNER_TAGS = sorted({n["partner"] for n in NODES})
# Keep all already-published offer event IDs stable as new agreements are appended.
LEGACY_OFFER_EVENT_KEYS = (
    "foreign_soviet", "foreign_cmea", "foreign_specialisation", "foreign_sov_commodity",
    "foreign_sov_industry", "foreign_mex_fuel", "foreign_mex_agro", "foreign_spr_nickel",
    "foreign_spr_training", "foreign_can_rail", "foreign_can_fisheries", "foreign_ddr",
    "foreign_symbolic", "foreign_cession", "foreign_interests", "foreign_limited",
    "foreign_settlement", "foreign_caribbean", "foreign_angola", "foreign_ethiopia",
    "foreign_algeria",
)
OFFER_EVENT_IDS = {key: 400 + index for index, key in enumerate(LEGACY_OFFER_EVENT_KEYS)}
LEGACY_CONFLICTS = {
    "foreign_soviet": ("COLDWAR_CUB_soviet_assistance_signed",),
    "foreign_sov_commodity": ("COLDWAR_CUB_bilat_sov_commodity_signed",),
    "foreign_sov_industry": ("COLDWAR_CUB_bilat_sov_industry_signed",),
    "foreign_mex_fuel": ("COLDWAR_CUB_bilat_mex_energy_signed",),
    "foreign_mex_agro": ("COLDWAR_CUB_bilat_mex_agro_signed",),
    "foreign_spr_nickel": ("COLDWAR_CUB_bilat_spr_nickel_signed",),
    "foreign_spr_training": ("COLDWAR_CUB_bilat_spr_training_signed",),
    "foreign_can_rail": ("COLDWAR_CUB_bilat_can_rail_signed",),
    "foreign_symbolic": ("COLDWAR_CUB_symbolic_cooperation_signed",),
    "foreign_interests": ("COLDWAR_CUB_history_interests_sections_active",),
    "foreign_limited": ("COLDWAR_CUB_us_full_settlement", "COLDWAR_CUB_us_normalisation_signed"),
    "foreign_settlement": ("COLDWAR_CUB_us_full_settlement", "COLDWAR_CUB_us_normalisation_signed"),
}


def suffix(node: dict) -> str:
    key = node["key"]
    return key.removeprefix("foreign_")


def flag(node: dict, name: str) -> str:
    return f"COLDWAR_CUB_foreign_{suffix(node)}_{name}"


def _offer_event_id(node: dict) -> int:
    key = node["key"]
    if key in OFFER_EVENT_IDS:
        return OFFER_EVENT_IDS[key]
    appended = [n["key"] for n in NODES if n["key"] not in OFFER_EVENT_IDS]
    return 400 + len(LEGACY_OFFER_EVENT_KEYS) + appended.index(key)


def _event_picture(node: dict) -> str:
    if node["partner"] == "USA":
        return event_art.sprite("GFX_news_us_cuba")
    if node["partner"] == "SOV":
        return event_art.sprite("GFX_soviet_union_flag")
    return event_art.sprite("GFX_treaty")


def _legacy_conflict_guards(node: dict) -> list[str]:
    # IMPERIA COLD WAR — The new settlement's own permanent reform is not a legacy treaty.
    guards = []
    for legacy in LEGACY_CONFLICTS.get(node['key'], ()):
        if legacy == 'COLDWAR_CUB_us_full_settlement' and node['key'] == 'foreign_settlement':
            guards.append(f'OR = {{ NOT = {{ has_country_flag = {legacy} }} has_country_flag = {flag(node, "paid")} }}')
        else:
            guards.append(f'NOT = {{ has_country_flag = {legacy} }}')
    return guards


def idea_id(node: dict, side: str) -> str:
    if node["key"] == "foreign_cmea" and side == "cub":
        return "COLDWAR_CUB_cmea_member"
    return f"COLDWAR_CUB_foreign_{suffix(node)}_{side}"


def _number(value: float) -> str:
    return f"{value:.5f}".rstrip("0").rstrip(".") if value else "0"


def _modifier_preview(node: dict, side: str) -> str:
    mods = node.get("cub_modifiers" if side == "cub" else "partner_modifiers", {})
    out = [f"add_ideas = {idea_id(node, side)}"]
    for key, value in mods.items():
        special_tips = {
            "imp_sanction_resistance": "COLDWAR_imp_sanction_resistance_tt",
            "army_org_factor": "COLDWAR_army_org_factor_tt",
            "research_speed_factor": "COLDWAR_research_speed_factor_tt",
        }
        tip = special_tips.get(key, key + "_tt")
        var = f"COLDWAR_CUB_foreign_preview_{suffix(node)}_{side}_{key}"
        out.append(f"add_to_variable = {{ {var} = {_number(value)} tooltip = {tip} }}")
    return "\n".join(out)


def _treasury_preview(country: str, amount: float) -> str:
    if not amount:
        return ""
    return (f"{country} = {{ set_temp_variable = {{ treasury_change = -{_number(amount)} }} "
            "modify_treasury_effect = yes }")


def _direct_effect(effect: dict, node: dict | None = None) -> str:
    kind = effect["kind"]
    if kind == "building":
        state = int(effect["state"])
        level = int(effect.get("levels", effect.get("level", 1)))
        building = effect["building"]
        slots = int(effect.get("extra_slots", level))
        return (f"{state} = {{ add_extra_state_shared_building_slots = {slots}\n"
                f"add_building_construction = {{ type = {building} level = {level} instant_build = yes }} }}")
    if kind == "research":
        country = effect.get("country", "CUB")
        name = f"COLDWAR_CUB_foreign_{suffix(node)}_research" if node else "COLDWAR_CUB_air_defence_radar_bonus"
        return (f"{country} = {{ add_tech_bonus = {{ name = {name} bonus = {_number(effect['bonus'])} "
                f"uses = {int(effect['uses'])} category = {effect['category']} }} }}")
    if kind == "treasury":
        return f"{effect['country']} = {{ set_temp_variable = {{ treasury_change = {_number(effect['amount'])} }} modify_treasury_effect = yes }}"
    if kind == "experience":
        return f"{effect['country']} = {{ army_experience = {int(effect.get('army', 0))} }}"
    if kind == "transfer_state":
        state = int(effect["state"])
        return f"DDR = {{ transfer_state = {state} }}\nCUB = {{ add_state_core = {state} }}"
    if kind == "rename_state":
        state = int(effect["state"])
        name = str(effect["name"]).replace('"', "'")
        return f'{state} = {{ set_state_name = "{name}" }}'
    if kind == "lift_mutual_sanctions":
        if node is None:
            raise ValueError("sanctions effect needs its contract node")
        return f"COLDWAR_CUB_foreign_lift_sanctions_{suffix(node)} = yes"
    raise ValueError(f"Unsupported accepted effect: {effect}")


def _one_time_preview(node: dict) -> str:
    out = []
    for effect in node.get("accepted_effects", []):
        if effect["kind"] == "lift_mutual_sanctions":
            out.append(_sanctions_preview(node, effect["classes"]))
        else:
            out.append(_direct_effect(effect, node))
    if node['key'] == 'foreign_limited':
        out.append('CUB = { remove_ideas = COLDWAR_CUB_american_embargo add_ideas = COLDWAR_CUB_american_embargo_limited }')
    elif node['key'] == 'foreign_settlement':
        out.append('CUB = { remove_ideas = { COLDWAR_CUB_american_embargo COLDWAR_CUB_american_embargo_limited } }')
    return "\n".join(out)


def preview(node: dict, include_offer_rename: bool = True) -> str:
    """Return a side-effect-free effect_tooltip body for the full agreement."""
    if not node.get("partner"):
        return ""
    out = []
    if include_offer_rename and node.get("immediate_effects"):
        out.append("custom_effect_tooltip = COLDWAR_CUB_foreign_immediate_effects_heading_tt")
        out.extend(f"CUB = {{ {_direct_effect(effect, node)} }}" for effect in node["immediate_effects"])
    out += ["custom_effect_tooltip = COLDWAR_CUB_foreign_accept_heading_tt",
           "CUB = {", _modifier_preview(node, "cub"), "}",
           f"{node['partner']} = {{", _modifier_preview(node, "partner"), "}"]
    costs = node.get("setup_costs", [0, 0])
    if len(costs) >= 2:
        if costs[0]:
            out.append(_treasury_preview("CUB", float(costs[0])))
        if costs[1]:
            out.append(_treasury_preview(node["partner"], float(costs[1])))
    one_time = _one_time_preview(node)
    if one_time:
        out.append(one_time)
    return "\n".join(x for x in out if x)


def offer(node: dict) -> str:
    """Return the CUB-scope offer effect call for a partnered foreign focus."""
    if not node.get("partner"):
        return ""
    key = suffix(node)
    out = []
    for effect in node.get("immediate_effects", []):
        out.append(_direct_effect(effect, node))
    out.append(f"COLDWAR_CUB_foreign_offer_{key} = yes")
    return "\n".join(out)


def _agreement_idea(key: str) -> str | None:
    required = PARTNER_NODES.get(key.removeprefix("COLDWAR_CUB_"))
    return idea_id(required, "cub") if required else None


def _agreement_guards(node: dict) -> list[str]:
    guards = []
    required_any = node.get("required_agreements_any", [])
    if required_any:
        ideas = [idea for key in required_any if (idea := _agreement_idea(key))]
        if ideas:
            guards.append("OR = { " + " ".join(f"has_idea = {idea}" for idea in ideas) + " }")
    for key in node.get("required_agreements_all", []):
        idea = _agreement_idea(key)
        if idea:
            guards.append(f"has_idea = {idea}")
    return guards


def extra_guards(node: dict) -> list[str]:
    """Return meaningful CUB focus guards, excluding focus-tree predecessors."""
    if not node.get("partner"):
        return []
    key = node["key"]
    tag = node["partner"]
    out = [f"country_exists = {tag}",
           f"NOT = {{ has_war_with = {tag} }}",
           f"{tag} = {{ NOT = {{ has_war_with = CUB }} }}",
           f"NOT = {{ has_country_flag = {flag(node, 'signed')} }}",
           f"{tag} = {{ NOT = {{ has_country_flag = {flag(node, 'signed')} }} }}",
           f"NOT = {{ has_country_flag = {flag(node, 'offer_open')} }}",
           f"{tag} = {{ NOT = {{ has_country_flag = {flag(node, 'offer_pending')} }} }}"]
    out.extend(_legacy_conflict_guards(node))
    for excluded in node.get("mutually_exclusive", []):
        other_key = excluded.removeprefix("COLDWAR_CUB_")
        if other_key.startswith("foreign_"):
            other = PARTNER_NODES.get(other_key)
            if other:
                out += [f"NOT = {{ has_completed_focus = {excluded} }}",
                        f"NOT = {{ has_country_flag = {flag(other, 'signed')} }}",
                        f"NOT = {{ has_country_flag = {flag(other, 'offer_open')} }}"]
    if key == "foreign_cmea":
        out.append("NOT = { has_idea = COLDWAR_CUB_cmea_member }")
    if key == "foreign_specialisation":
        out.append("has_idea = COLDWAR_CUB_cmea_member")
    if key in ("foreign_caribbean", "foreign_algeria"):
        out.append("has_completed_focus = COLDWAR_CUB_medical_brigades")
    if key in ("foreign_limited", "foreign_settlement"):
        out.append("has_country_flag = COLDWAR_CUB_foreign_interests_signed")
    if key == "foreign_symbolic":
        out += ["date > 1972.6.18", "owns_state = 1252", "controls_state = 1252",
                "NOT = { has_country_flag = COLDWAR_CUB_island_cession_ratified }"]
    if key == "foreign_cession":
        out += ["date > 1972.6.18", "owns_state = 1252", "controls_state = 1252",
                "NOT = { has_completed_focus = COLDWAR_CUB_foreign_symbolic }",
                "NOT = { has_country_flag = COLDWAR_CUB_island_cession_ratified }"]
    if key == "foreign_angola":
        out.append("AGL = { is_subject = no }")
    if key == "foreign_ethiopia":
        out.append("ETH = { OR = { emerging_communist_state_are_in_power = yes neutrality_neutral_communism_are_in_power = yes nationalist_military_junta_are_in_power = yes } }")
    out.extend(_agreement_guards(node))
    # Do not promise a one-time state investment if Cuba has lost that state
    # before the focus is selected. These checks are repeated at acceptance.
    for effect in node.get("accepted_effects", []):
        if effect.get("kind") == "building":
            state = int(effect["state"])
            out += [f"owns_state = {state}", f"controls_state = {state}"]
    out.insert(0, "COLDWAR_CUB_is_1970 = yes")
    return list(dict.fromkeys(out))


def legacy_air_preview() -> str:
    """Native preview body for the retained Soviet radar agreement."""
    return "\n".join([
        _treasury_preview("CUB", 0.45), _treasury_preview("SOV", 0.15),
        "854 = { add_extra_state_shared_building_slots = 1 add_building_construction = { type = radar_station level = 1 instant_build = yes } }",
        "add_tech_bonus = { name = COLDWAR_CUB_air_defence_radar_bonus bonus = 0.25 uses = 1 technology = radar }",
    ])


def _safe(value: str) -> str:
    return re.sub(r"[^a-z0-9_]", "_", value.lower())


def _pair_trigger(node: dict) -> str:
    tag = node["partner"]
    arrays = []
    for cls in ("dip", "fin", "eco", "mil"):
        arrays += [f"is_in_array = {{ array = imp_{cls}_sanc_on_us value = {tag} }}",
                   f"is_in_array = {{ array = imp_{cls}_sanc_by_us value = {tag} }}"]
    partner_arrays = []
    for cls in ("dip", "fin", "eco", "mil"):
        partner_arrays += [f"is_in_array = {{ array = imp_{cls}_sanc_on_us value = CUB }}",
                           f"is_in_array = {{ array = imp_{cls}_sanc_by_us value = CUB }}"]
    return (f"COLDWAR_CUB_foreign_pair_clear_{suffix(node)} = {{\n"
            f"\tcountry_exists = {tag}\n\tNOT = {{ has_war_with = {tag} }}\n"
            f"\tNOT = {{ is_embargoing = {tag} }}\n"
            f"\tNOT = {{ OR = {{ {' '.join(arrays)} }} }}\n"
            f"\t{tag} = {{ NOT = {{ has_war_with = CUB }} NOT = {{ is_embargoing = CUB }} "
            f"NOT = {{ OR = {{ {' '.join(partner_arrays)} }} }} }}\n}}")


def _node_accept_requirements(node: dict) -> str:
    """Recipient-time requirements that must still hold when an offer is accepted."""
    key = node["key"]
    out = []
    if key == "foreign_specialisation":
        out.append("has_idea = COLDWAR_CUB_cmea_member")
    if key in ("foreign_symbolic", "foreign_cession"):
        out += ["date > 1972.6.18", "owns_state = 1252", "controls_state = 1252"]
    if key == "foreign_angola":
        out.append("AGL = { is_subject = no }")
    if key == "foreign_ethiopia":
        out.append("ETH = { OR = { emerging_communist_state_are_in_power = yes neutrality_neutral_communism_are_in_power = yes nationalist_military_junta_are_in_power = yes } }")
    out.extend(_agreement_guards(node))
    if key == "foreign_cmea":
        out.append("NOT = { has_idea = COLDWAR_CUB_cmea_member }")
    if key in ("foreign_limited", "foreign_settlement"):
        out.append("has_country_flag = COLDWAR_CUB_foreign_interests_signed")
    if key in ("foreign_caribbean", "foreign_algeria"):
        out.append("has_completed_focus = COLDWAR_CUB_medical_brigades")
    for effect in node.get("accepted_effects", []):
        if effect.get("kind") == "building":
            state = int(effect["state"])
            out += [f"owns_state = {state}", f"controls_state = {state}"]
    out.extend(_legacy_conflict_guards(node))
    for excluded in node.get("mutually_exclusive", []):
        other = PARTNER_NODES.get(excluded.removeprefix("COLDWAR_CUB_"))
        if other:
            out += [f"NOT = {{ has_completed_focus = {excluded} }}",
                    f"NOT = {{ has_country_flag = {flag(other, 'signed')} }}",
                    f"NOT = {{ has_country_flag = {flag(other, 'offer_open')} }}"]
    return " ".join(out)


def _valid_trigger(node: dict) -> str:
    tag = node["partner"]
    return (f"COLDWAR_CUB_foreign_accept_valid_{suffix(node)} = {{\n"
            f"\ttag = {tag}\n"
            f"\thas_country_flag = {flag(node, 'offer_pending')}\n"
            f"\tNOT = {{ has_country_flag = {flag(node, 'signed')} }}\n"
            f"\tCUB = {{ COLDWAR_CUB_is_1970 = yes has_country_flag = COLDWAR_CUB_foreign_{suffix(node)}_applied "
            f"country_exists = {tag} has_country_flag = {flag(node, 'offer_open')} "
            f"NOT = {{ has_country_flag = {flag(node, 'signed')} }} "
            f"{_node_accept_requirements(node)} }}\n}}")


def _offer_effect(node: dict, event_id: int) -> str:
    tag = node["partner"]
    return (f"COLDWAR_CUB_foreign_offer_{suffix(node)} = {{\n"
            f"\tif = {{\n\t\tlimit = {{ tag = CUB COLDWAR_CUB_is_1970 = yes has_country_flag = COLDWAR_CUB_foreign_{suffix(node)}_applied country_exists = {tag} "
            f"NOT = {{ has_country_flag = {flag(node, 'signed')} }} "
            f"NOT = {{ has_country_flag = {flag(node, 'offer_open')} }} "
            f"{tag} = {{ NOT = {{ has_country_flag = {flag(node, 'signed')} }} "
            f"NOT = {{ has_country_flag = {flag(node, 'offer_pending')} }} }} "
            f"{_node_accept_requirements(node)} {' '.join(extra_guards(node))} }}\n"
            f"\t\tset_country_flag = {{ flag = {flag(node, 'offer_open')} value = 1 days = 90 }}\n"
            f"\t\tset_country_flag = {flag(node, 'ever_offered')}\n"
            f"\t\t{tag} = {{ set_country_flag = {{ flag = {flag(node, 'offer_pending')} value = 1 days = 90 }} "
            f"set_country_flag = {flag(node, 'ever_offered')} country_event = {{ id = COLDWAR_CUB_foreign_contracts.{event_id} }} }}\n"
            f"\t}}\n}}")


def _cost_effect(country: str, cost: float, node: dict) -> str:
    paid = flag(node, "paid")
    return (f"if = {{ limit = {{ NOT = {{ has_country_flag = {paid} }} }} "
            f"set_temp_variable = {{ treasury_change = -{_number(cost)} }} modify_treasury_effect = yes "
            f"set_country_flag = {paid} }}") if cost else f"set_country_flag = {paid}"


def _accepted_effects(node: dict) -> str:
    out = []
    effects = node.get("accepted_effects", [])
    # USA settlement terms change the actual restriction arrays on acceptance,
    # including when a previously cancelled agreement is negotiated again.
    for e in effects:
        if e["kind"] == "lift_mutual_sanctions":
            out.append(_direct_effect(e, node))
    # IMPERIA COLD WAR — Ratified commercial terms replace Cuba's real embargo burden.
    if node['key'] == 'foreign_limited':
        out.append('CUB = { set_country_flag = COLDWAR_CUB_us_easing_limited COLDWAR_CUB_sync_embargo = yes }')
    elif node['key'] == 'foreign_settlement':
        out.append('CUB = { set_country_flag = COLDWAR_CUB_us_full_settlement clr_country_flag = COLDWAR_CUB_us_easing_limited COLDWAR_CUB_sync_embargo = yes }')
    receipt = flag(node, "grant_receipt")
    if effects:
        out.append(f"if = {{ limit = {{ NOT = {{ has_country_flag = {receipt} }} }}")
        for e in effects:
            if e["kind"] != "lift_mutual_sanctions":
                out.append(_direct_effect(e, node))
        out.append(f"set_country_flag = {receipt}\nCUB = {{ set_country_flag = {receipt} }}\n{node['partner']} = {{ set_country_flag = {receipt} }}\n}}")
    return "\n".join(out)


def _sanctions_effect(node: dict, classes: list[str]) -> str:
    tag = node["partner"]
    native_class = {"diplomatic": "dip", "financial": "fin", "economic": "eco", "military": "mil"}
    lines = []
    for cls in classes:
        cls = native_class.get(cls, cls)
        for direction in ("on_us", "by_us"):
            lines.append(f"if = {{ limit = {{ is_in_array = {{ array = imp_{cls}_sanc_{direction} value = {tag} }} }} remove_from_array = {{ array = imp_{cls}_sanc_{direction} value = {tag} }} }}")
    partner_lines = []
    for cls in classes:
        cls = native_class.get(cls, cls)
        for direction in ("on_us", "by_us"):
            partner_lines.append(f"if = {{ limit = {{ is_in_array = {{ array = imp_{cls}_sanc_{direction} value = CUB }} }} remove_from_array = {{ array = imp_{cls}_sanc_{direction} value = CUB }} }}")
    if "economic" in classes:
        lines.append(f"country_event = {{ id = COLDWAR_CUB_foreign_contracts.950 }}")
        partner_lines.append("country_event = { id = COLDWAR_CUB_foreign_contracts.951 }")
    body = ("CUB = {\n" + "\n".join(lines) + "\n}\n"
            + f"{tag} = {{\n" + "\n".join(partner_lines) + "\n}\n"
            + "CUB = { imp_sanctions_calculate = yes }\n"
            + f"{tag} = {{ imp_sanctions_calculate = yes }}")
    return f"COLDWAR_CUB_foreign_lift_sanctions_{suffix(node)} = {{\n{body}\n}}"


def _sanctions_preview(node: dict, classes: list[str]) -> str:
    """Inline the concrete reciprocal restriction removals into the non-executing preview."""
    tag = node["partner"]
    cub, partner = [], []
    native_class = {"diplomatic": "dip", "financial": "fin", "economic": "eco", "military": "mil"}
    for cls in classes:
        cls = native_class.get(cls, cls)
        for direction in ("on_us", "by_us"):
            cub.append(f"if = {{ limit = {{ is_in_array = {{ array = imp_{cls}_sanc_{direction} value = {tag} }} }} remove_from_array = {{ array = imp_{cls}_sanc_{direction} value = {tag} }} }}")
            partner.append(f"if = {{ limit = {{ is_in_array = {{ array = imp_{cls}_sanc_{direction} value = CUB }} }} remove_from_array = {{ array = imp_{cls}_sanc_{direction} value = CUB }} }}")
    if "economic" in classes:
        cub.append(f"if = {{ limit = {{ is_embargoing = {tag} }} break_embargo = {tag} }}")
        partner.append("if = { limit = { is_embargoing = CUB } break_embargo = CUB }")
    return "CUB = { " + " ".join(cub) + " imp_sanctions_calculate = yes } " + f"{tag} = {{ " + " ".join(partner) + " imp_sanctions_calculate = yes }"


def _accept_effect(node: dict) -> str:
    tag = node["partner"]
    costs = node.get("setup_costs", [0, 0])
    body = [f"if = {{ limit = {{ COLDWAR_CUB_foreign_accept_valid_{suffix(node)} = yes }}"]
    body.append(_cost_effect(tag, float(costs[1]), node))
    body.append(f"CUB = {{ {_cost_effect('CUB', float(costs[0]), node)} }}")
    one_time = _accepted_effects(node)
    if one_time:
        body.append(one_time)
    body += [f"set_country_flag = {flag(node, 'signed')}",
             f"CUB = {{ set_country_flag = {flag(node, 'signed')} }}",
             f"clr_country_flag = {flag(node, 'offer_pending')}",
             f"CUB = {{ clr_country_flag = {flag(node, 'offer_open')} COLDWAR_CUB_foreign_reconcile_all = yes "
             f"country_event = {{ id = COLDWAR_CUB_foreign_contracts.900 }} }}",
             "COLDWAR_CUB_foreign_reconcile_all = yes", "}"]
    return f"COLDWAR_CUB_foreign_accept_{suffix(node)} = {{\n" + "\n".join(body) + "\n}"


def _refuse_effect(node: dict) -> str:
    """Shared refusal transaction for the popup and recipient decision."""
    key = suffix(node)
    tag = node["partner"]
    return (f"COLDWAR_CUB_foreign_refuse_{key} = {{\n"
            f"\tif = {{ limit = {{ tag = {tag} has_country_flag = {flag(node, 'offer_pending')} "
            f"CUB = {{ has_country_flag = {flag(node, 'offer_open')} }} }}\n"
            f"\t\tclr_country_flag = {flag(node, 'offer_pending')} set_country_flag = {flag(node, 'refused')}\n"
            f"\t\tCUB = {{ clr_country_flag = {flag(node, 'offer_open')} set_country_flag = {flag(node, 'refused')} "
            f"country_event = {{ id = COLDWAR_CUB_foreign_contracts.901 }} }}\n"
            f"\t}}\n}}")


def _decision(node: dict, kind: str) -> str:
    key = suffix(node)
    tag = node["partner"]
    base = f"COLDWAR_CUB_foreign_{kind}_{key}"
    if kind == "accept":
        complete = (f"complete_effect = {{ effect_tooltip = {{ {preview(node, include_offer_rename=False)} }} hidden_effect = {{ "
                    f"COLDWAR_CUB_foreign_accept_{key} = yes }} }}")
        available = f"COLDWAR_CUB_foreign_accept_valid_{key} = yes"
    elif kind == "refuse":
        complete = f"complete_effect = {{ COLDWAR_CUB_foreign_refuse_{key} = yes }}"
        available = (f"tag = {tag} has_country_flag = {flag(node, 'offer_pending')} "
                     f"CUB = {{ has_country_flag = {flag(node, 'offer_open')} country_exists = CUB }}")
    elif kind == "reopen":
        complete = ("complete_effect = { if = { limit = { "
                    f"has_country_flag = {flag(node, 'ever_offered')} "
                    f"NOT = {{ has_country_flag = {flag(node, 'offer_pending')} }} "
                    f"NOT = {{ has_country_flag = {flag(node, 'signed')} }} "
                    f"CUB = {{ NOT = {{ has_country_flag = {flag(node, 'offer_open')} }} "
                    f"NOT = {{ has_country_flag = {flag(node, 'signed')} }} }} }} "
                    f"CUB = {{ COLDWAR_CUB_foreign_offer_{key} = yes }} }} }}")
        available = (f"has_country_flag = {flag(node, 'ever_offered')} "
                     f"tag = {tag} "
                     f"NOT = {{ has_country_flag = {flag(node, 'offer_pending')} }} "
                     f"NOT = {{ has_country_flag = {flag(node, 'signed')} }} "
                     f"CUB = {{ NOT = {{ has_country_flag = {flag(node, 'offer_open')} }} "
                     f"NOT = {{ has_country_flag = {flag(node, 'signed')} }} "
                     f"has_country_flag = COLDWAR_CUB_foreign_{key}_applied COLDWAR_CUB_is_1970 = yes {_node_accept_requirements(node)} }}")
    elif kind == "cancel":
        complete = (f"complete_effect = {{ CUB = {{ COLDWAR_CUB_foreign_cancel_{key} = yes }} }}")
        available = f"tag = {tag} has_country_flag = {flag(node, 'signed')} CUB = {{ has_country_flag = {flag(node, 'signed')} }}"
    else:
        raise ValueError(kind)
    visible_flag = f"has_country_flag = {flag(node, 'offer_pending')}" if kind in ("accept", "refuse") else (
        f"has_country_flag = {flag(node, 'ever_offered')}" if kind == "reopen" else f"has_country_flag = {flag(node, 'signed')}")
    return (f"\t{base} = {{ icon = generic_diplomacy visible = {{ {visible_flag} }} "
            f"available = {{ {available} }} cost = 0 days_remove = 1 {complete} "
            f"ai_will_do = {{ base = {4 if kind == 'accept' else 0 if kind in ('reopen','cancel') else 1} }} }}")


def _cancel_effect(node: dict) -> str:
    tag = node["partner"]
    return (f"COLDWAR_CUB_foreign_cancel_{suffix(node)} = {{\n"
            f"\tif = {{ limit = {{ has_country_flag = {flag(node, 'signed')} }}\n"
            f"\t\tclr_country_flag = {flag(node, 'signed')}\n"
            f"\t\tremove_ideas = {idea_id(node, 'cub')}\n"
            f"\t\tif = {{ limit = {{ country_exists = {tag} }} {tag} = {{ clr_country_flag = {flag(node, 'signed')} remove_ideas = {idea_id(node, 'partner')} }} }}\n"
            f"\t\tCOLDWAR_CUB_foreign_reconcile_all = yes\n\t}}\n}}")


def _reconcile_effect() -> str:
    blocks = ["COLDWAR_CUB_foreign_reconcile_all = {", "CUB = {", "if = { limit = { COLDWAR_CUB_is_1970 = yes }"]
    for node in NODES:
        s = suffix(node)
        tag = node["partner"]
        cubidea = idea_id(node, "cub")
        partneridea = idea_id(node, "partner")
        condition = (f"has_country_flag = {flag(node, 'signed')} {tag} = {{ has_country_flag = {flag(node, 'signed')} }} "
                     f"COLDWAR_CUB_foreign_pair_clear_{s} = yes")
        dependency_guards = _agreement_guards(node)
        if dependency_guards:
            condition += " " + " ".join(dependency_guards)
        if node["key"] == "foreign_specialisation":
            condition += " has_idea = COLDWAR_CUB_cmea_member"
        blocks.append(f"\tif = {{ limit = {{ {condition} }}")
        blocks.append(f"\t\tif = {{ limit = {{ NOT = {{ has_idea = {cubidea} }} }} add_ideas = {cubidea} }}")
        blocks.append(f"\t\t{tag} = {{ if = {{ limit = {{ NOT = {{ has_idea = {partneridea} }} }} add_ideas = {partneridea} }} }}")
        blocks.append("\t}")
        blocks.append("\telse = {")
        if node["key"] == "foreign_cmea":
            blocks.append(f"\t\tif = {{ limit = {{ has_country_flag = {flag(node, 'paid')} has_idea = {cubidea} }} remove_ideas = {cubidea} }}")
        else:
            blocks.append(f"\t\tif = {{ limit = {{ has_idea = {cubidea} }} remove_ideas = {cubidea} }}")
        blocks.append(f"\t\tif = {{ limit = {{ country_exists = {tag} {tag} = {{ has_idea = {partneridea} }} }} {tag} = {{ remove_ideas = {partneridea} }} }}")
        blocks.append("\t}")
    blocks.append("}")
    blocks += ["}", "}"]
    return "\n".join(blocks)


def _triggers() -> str:
    out = ["# IMPERIA COLD WAR — Cuba 1970 foreign contract triggers."]
    out += [_pair_trigger(n) for n in NODES]
    out += [_valid_trigger(n) for n in NODES]
    return "\n\n".join(out) + "\n"


def _effects() -> str:
    out = ["# IMPERIA COLD WAR — Cuba 1970 foreign contract lifecycle effects."]
    out += [_offer_effect(n, _offer_event_id(n)) for n in NODES]
    out += [_accept_effect(n) for n in NODES]
    out += [_refuse_effect(n) for n in NODES]
    for n in NODES:
        out.append(_cancel_effect(n))
    for n in NODES:
        effects = [e for e in n.get("accepted_effects", []) if e["kind"] == "lift_mutual_sanctions"]
        for e in effects:
            out.append(_sanctions_effect(n, e["classes"]))
    out.append(_reconcile_effect())
    return "\n\n".join(out) + "\n"


def _events() -> str:
    out = ["# IMPERIA COLD WAR — Cuba 1970 foreign contract notices.", "add_namespace = COLDWAR_CUB_foreign_contracts"]
    for n in NODES:
        eid = _offer_event_id(n)
        key = suffix(n)
        tag = n["partner"]
        pending_open = f"tag = {tag} has_country_flag = {flag(n, 'offer_pending')} CUB = {{ has_country_flag = {flag(n, 'offer_open')} }}"
        out.append(f"""country_event = {{
    id = COLDWAR_CUB_foreign_contracts.{eid}
    title = COLDWAR_CUB_foreign_contracts.{key}.t
    desc = COLDWAR_CUB_foreign_contracts.{key}.d
    picture = {_event_picture(n)}
    is_triggered_only = yes
    trigger = {{ {pending_open} }}
    immediate = {{ log = "COLDWAR_CUB_EVENT_DELIVERED {n['key']} {tag}" set_country_flag = COLDWAR_CUB_foreign_{key}_notified }}
    option = {{
        name = COLDWAR_CUB_foreign_contracts.{key}.accept
        trigger = {{ COLDWAR_CUB_foreign_accept_valid_{key} = yes }}
        effect_tooltip = {{ {preview(n, include_offer_rename=False)} }}
        hidden_effect = {{ COLDWAR_CUB_foreign_accept_{key} = yes }}
        ai_chance = {{ base = 0 }}
    }}
    option = {{
        name = COLDWAR_CUB_foreign_contracts.{key}.refuse
        trigger = {{ {pending_open} }}
        COLDWAR_CUB_foreign_refuse_{key} = yes
        ai_chance = {{ base = 0 }}
    }}
}}""")
    for number, suffix_text, picture in ((900, "accepted", "GFX_treaty"), (901, "refused", "GFX_treaty_rejected")):
        out.append(f"""country_event = {{
    id = COLDWAR_CUB_foreign_contracts.{number}
    title = COLDWAR_CUB_foreign_contracts.{suffix_text}.t
    desc = COLDWAR_CUB_foreign_contracts.{suffix_text}.d
    picture = {picture}
    is_triggered_only = yes
    option = {{ name = COLDWAR_CUB_foreign_contracts.review }}
}}""")
    out.append("""country_event = {
    id = COLDWAR_CUB_foreign_contracts.950
    hidden = yes
    is_triggered_only = yes
    immediate = { if = { limit = { tag = CUB is_embargoing = USA } break_embargo = USA imp_sanctions_calculate = yes } }
}""")
    out.append("""country_event = {
    id = COLDWAR_CUB_foreign_contracts.951
    hidden = yes
    is_triggered_only = yes
    immediate = { if = { limit = { tag = USA is_embargoing = CUB } break_embargo = CUB imp_sanctions_calculate = yes } }
}""")
    return "\n\n".join(out) + "\n"


def _ideas() -> str:
    out = ["# IMPERIA COLD WAR — Cuba 1970 foreign agreement spirits.", "ideas = {", "\tcountry = {"]
    for n in NODES:
        for side in ("cub", "partner"):
            if n["key"] == "foreign_cmea" and side == "cub":
                continue  # existing COLDWAR_CUB_cmea_member is the membership gate
            idea = idea_id(n, side)
            mods = n.get("cub_modifiers" if side == "cub" else "partner_modifiers", {})
            lines = [f"\t\t{idea} = {{", "\t\t\tpicture = communism3", "\t\t\tallowed = { always = no }", "\t\t\tallowed_civil_war = { always = yes }"]
            # IMPERIA COLD WAR — Native idea cleanup also covers Cuba ceasing to exist.
            lines.append(f'\t\t\tcancel = {{ OR = {{ NOT = {{ country_exists = CUB }} NOT = {{ country_exists = {n["partner"]} }} }} }}')
            if mods:
                lines.append("\t\t\tmodifier = { " + " ".join(f"{k} = {_number(v)}" for k, v in mods.items()) + " }")
            lines.append("\t\t}")
            out += lines
    out += ["\t}", "}"]
    return "\n".join(out) + "\n"


def _decision_files() -> tuple[str, str]:
    response = ["# IMPERIA COLD WAR — recipient consent and termination decisions.", "COLDWAR_CUB_foreign_responses = {"]
    cub = ["# IMPERIA COLD WAR — Cuban termination decisions, no offer selector.", "COLDWAR_CUB_foreign_cancellation = {"]
    for n in NODES:
        for kind in ("accept", "refuse", "reopen", "cancel"):
            response.append(_decision(n, kind))
        key = suffix(n)
        cub.append(f"\tCOLDWAR_CUB_foreign_cancel_{key}_as_cub = {{ icon = generic_diplomacy visible = {{ has_country_flag = {flag(n, 'signed')} }} available = {{ has_country_flag = {flag(n, 'signed')} }} cost = 0 days_remove = 1 complete_effect = {{ COLDWAR_CUB_foreign_cancel_{key} = yes }} ai_will_do = {{ base = 0 }} }}")
    response += ["}"]
    cub += ["}"]
    return "\n".join(response) + "\n", "\n".join(cub) + "\n"


def _categories() -> str:
    any_pending = " ".join(f"has_country_flag = {flag(n, 'offer_pending')}" for n in NODES)
    any_signed = " ".join(f"has_country_flag = {flag(n, 'signed')}" for n in NODES)
    cub_signed = " ".join(f"has_country_flag = {flag(n, 'signed')}" for n in NODES)
    return ("# IMPERIA COLD WAR — Cuba 1970 foreign contract decision categories.\n"
            "COLDWAR_CUB_foreign_responses = {\n\tallowed = { NOT = { tag = CUB } }\n\ticon = generic_diplomacy\n\tpriority = 210\n"
            f"\tvisible = {{ OR = {{ {any_pending} {any_signed} }} }}\n}}\n\n"
            "COLDWAR_CUB_foreign_cancellation = {\n\tallowed = { tag = CUB }\n\ticon = generic_diplomacy\n\tpriority = 205\n"
            f"\tvisible = {{ COLDWAR_CUB_is_1970 = yes OR = {{ {cub_signed} }} }}\n}}\n")


def _localisation() -> str:
    lines = ["l_english:", "# IMPERIA COLD WAR — Cuba 1970 foreign agreement localisation."]
    lines += [
        ' COLDWAR_CUB_cmea_member:0 "COMECON Membership"',
        ' COLDWAR_CUB_cmea_member_desc:0 "Cuba holds formal membership in the Council for Mutual Economic Assistance."',
        ' COLDWAR_CUB_foreign_accept_heading_tt:0 "If they accept:"',
        ' COLDWAR_CUB_foreign_immediate_effects_heading_tt:0 "On focus completion:"',
        ' COLDWAR_CUB_foreign_symbolic_offer_heading_tt:0 "Cuba renames the island upon completing the focus:"',
        ' COLDWAR_CUB_foreign_responses:0 "Cuban Agreements"',
        ' COLDWAR_CUB_foreign_cancellation:0 "Bilateral Agreements"',
        ' COLDWAR_CUB_foreign_contracts.review:0 "Review the agreement in national diplomatic decisions."',
        ' COLDWAR_CUB_foreign_contracts.accepted.t:0 "Agreement Ratified"',
        ' COLDWAR_CUB_foreign_contracts.accepted.d:0 "The recipient has accepted Cuba’s proposal. The agreed setup costs and one-time terms have been applied."',
        ' COLDWAR_CUB_foreign_contracts.refused.t:0 "Proposal Declined"',
        ' COLDWAR_CUB_foreign_contracts.refused.d:0 "The recipient has declined the proposal. Neither government has paid its setup cost, and the recipient may reopen the same terms later."',
    ]
    for n in NODES:
        key = suffix(n)
        desc = n.get("description", "A standing agreement between both governments.").replace('"', "'")
        partner_name = n.get("spirit") or n.get("title")
        cub_name = n.get("spirit") or n.get("title")
        other_name = n.get("partner_spirit") or (partner_name if partner_name.startswith('Cuban') else f"Cuban {partner_name}")
        for side, name in (("cub", cub_name), ("partner", other_name)):
            if n["key"] == "foreign_cmea" and side == "cub":
                continue
            idea = idea_id(n, side)
            lines.append(f' {idea}:0 "{name}"')
            lines.append(f' {idea}_desc:0 "{desc} The terms remain active while both governments are at peace and free of mutual sanctions. Either signatory may terminate the agreement."')
        lines += [
            f' COLDWAR_CUB_foreign_accept_{key}:0 "Accept {n["title"]}"',
            f' COLDWAR_CUB_foreign_refuse_{key}:0 "Decline {n["title"]}"',
            f' COLDWAR_CUB_foreign_reopen_{key}:0 "Reopen {n["title"]}"',
            f' COLDWAR_CUB_foreign_cancel_{key}:0 "Terminate {n["title"]}"',
            f' COLDWAR_CUB_foreign_cancel_{key}_as_cub:0 "Terminate {n["title"]}"',
            f' COLDWAR_CUB_foreign_contracts.{key}.t:0 "{n["title"]}"',
            f' COLDWAR_CUB_foreign_contracts.{key}.d:0 "Cuba has presented the {n["title"]} proposal. Accept or decline here, or review the terms in the recipient diplomatic decisions. The offer remains open for 90 days."',
            f' COLDWAR_CUB_foreign_contracts.{key}.accept:0 "Accept the Agreement"',
            f' COLDWAR_CUB_foreign_contracts.{key}.refuse:0 "Decline the Proposal"',
        ]
        for effect in n.get("accepted_effects", []):
            if effect["kind"] == "lift_mutual_sanctions":
                lines.append(f' COLDWAR_CUB_foreign_{key}_sanctions_tt:0 "Lift the agreed mutual sanctions and native embargo restrictions."')
        if any(effect['kind'] == 'research' for effect in n.get('accepted_effects', [])):
            lines.append(f' COLDWAR_CUB_foreign_{suffix(n)}_research:0 "{n["title"]}"')
    return "\n".join(lines) + "\n"


def generate() -> dict[str, str]:
    response, cub_cancel = _decision_files()
    out = {
        "common/scripted_effects/COLDWAR_CUB_1970_foreign_contracts.txt": _effects(),
        "common/scripted_triggers/COLDWAR_CUB_1970_foreign_contracts.txt": _triggers(),
        "common/ideas/COLDWAR_CUB_1970_foreign_contracts.txt": _ideas(),
        "common/decisions/COLDWAR_CUB_1970_foreign_contracts.txt": response,
        "common/decisions/COLDWAR_CUB_1970_foreign_cancel.txt": cub_cancel,
        "common/decisions/categories/COLDWAR_CUB_1970_foreign_contracts.txt": _categories(),
        "events/COLDWAR_CUB_1970_foreign_contracts.txt": _events(),
        "localisation/english/COLDWAR_CUB_1970_foreign_contracts_l_english.yml": _localisation(),
    }
    # Preserve the old recipient-owned replies and termination options while
    # removing every legacy Cuban contract picker and target-array offer menu.
    for rel, removed in (
        ("common/decisions/COLDWAR_CUB_1970_diplomacy.txt", {
            "COLDWAR_CUB_retry_soviet_assistance", "COLDWAR_CUB_propose_soviet_fuel_commitment",
            "COLDWAR_CUB_retry_cmea_admission", "COLDWAR_CUB_retry_us_normalisation",
            "COLDWAR_CUB_retry_ddr_commission", "COLDWAR_CUB_retry_symbolic_cooperation",
            "COLDWAR_CUB_retry_island_cession", "COLDWAR_CUB_medical_offer_target",
            "COLDWAR_CUB_overseas_offer_target", "COLDWAR_CUB_conduct_overseas_advisory",
        }),
        ("common/decisions/COLDWAR_CUB_1970_bilateral.txt", {
            "COLDWAR_CUB_medical_offer_target", "COLDWAR_CUB_overseas_offer_target",
            "COLDWAR_CUB_reopen_interests_sections",
        }),
    ):
        path = ROOT / rel
        if path.exists():
            text = path.read_text(encoding="utf-8-sig")
            text = _remove_decisions(text, removed)
            if rel.endswith("diplomacy.txt"):
                old_visible = "visible = { has_idea = COLDWAR_CUB_cmea_member }"
                old_available = "available = { has_idea = COLDWAR_CUB_cmea_member }"
                text = text.replace(old_visible, "visible = { has_idea = COLDWAR_CUB_cmea_member NOT = { has_country_flag = COLDWAR_CUB_foreign_cmea_signed } }")
                text = text.replace(old_available, "available = { has_idea = COLDWAR_CUB_cmea_member NOT = { has_country_flag = COLDWAR_CUB_foreign_cmea_signed } }")
            out[rel] = text
    # Legacy providers are retained for accepted agreements and replies, but
    # their old focus tree was replaced. Convert only focus checks for IDs no
    # longer present in the active Cuban tree to the permanent applied receipt
    # emitted by the new compiler. This preserves old-save behavior without
    # leaving invalid focus references in loaded script.
    compatibility_paths = (
        "common/decisions/COLDWAR_CUB_1970_diplomacy.txt",
        "common/decisions/COLDWAR_CUB_1970_bilateral.txt",
        "common/scripted_effects/COLDWAR_CUB_1970_diplomacy.txt",
        "common/scripted_triggers/COLDWAR_CUB_1970_diplomacy.txt",
        "events/COLDWAR_CUB_1970_diplomacy.txt",
        "common/decisions/categories/COLDWAR_CUB_1970_diplomacy.txt",
        "common/scripted_effects/COLDWAR_CUB_1970_bilateral.txt",
        "common/scripted_triggers/COLDWAR_CUB_1970_bilateral.txt",
        "events/COLDWAR_CUB_1970_bilateral.txt",
    )
    focus_tree = ROOT / "common/national_focus/COLDWAR_CUB_1970_focus.txt"
    active_focuses = set(re.findall(r"(?m)^\s*id\s*=\s*(COLDWAR_CUB_[A-Za-z0-9_]+)", focus_tree.read_text(encoding="utf-8-sig"))) if focus_tree.exists() else set()
    for rel in compatibility_paths:
        path = ROOT / rel
        if path.exists():
            text = out.get(rel, path.read_text(encoding="utf-8-sig"))
            out[rel] = _migrate_removed_focus_refs(text, active_focuses)
    categories = ROOT / "common/decisions/categories/COLDWAR_CUB_1970_bilateral.txt"
    if categories.exists():
        text = out.get("common/decisions/categories/COLDWAR_CUB_1970_bilateral.txt", categories.read_text(encoding="utf-8-sig"))
        old = "visible = { OR = { has_completed_focus = COLDWAR_CUB_island_diplomacy has_completed_focus = COLDWAR_CUB_moscow_guarantee has_country_flag = COLDWAR_CUB_medical_targeting_enabled has_country_flag = COLDWAR_CUB_history_interests_sections_active has_country_flag = COLDWAR_CUB_history_interests_sections_seen } }"
        legacy_receipts = " ".join(f"has_country_flag = COLDWAR_CUB_bilat_{p}_{t}_signed" for p, terms in (("sov", ("commodity", "industry")), ("mex", ("energy", "agro")), ("spr", ("nickel", "training")), ("can", ("rail", "industry"))) for t in terms)
        text = text.replace(old, f"visible = {{ OR = {{ {legacy_receipts} }} }}")
        out["common/decisions/categories/COLDWAR_CUB_1970_bilateral.txt"] = text
    # IMPERIA COLD WAR — Apply the same native photo-frame contract to retained replies.
    for rel in out:
        if rel.startswith('events/'):
            out[rel] = event_art.bind(out[rel])
    return out


def _migrate_removed_focus_refs(text: str, active_focuses: set[str]) -> str:
    """Use permanent applied receipts for references to removed CUB focuses."""
    pattern = re.compile(r"\bhas_completed_focus\s*=\s*(COLDWAR_CUB_[A-Za-z0-9_]+)")
    return pattern.sub(lambda match: match.group(0) if match.group(1) in active_focuses else f"has_country_flag = {match.group(1)}_applied", text)


def _remove_blocks(text: str, names: set[str]) -> str:
    """Remove named top-level blocks using brace matching that respects strings/comments."""
    for name in names:
        match = re.search(rf"(?m)^\s*{re.escape(name)}\s*=\s*\{{", text)
        if not match:
            continue
        start = match.start()
        open_at = text.find("{", match.start(), match.end())
        end = _matching_brace(text, open_at) + 1
        while end < len(text) and text[end] in " \t\r\n":
            end += 1
        text = text[:start] + text[end:]
    return text


def _matching_brace(text: str, open_at: int) -> int:
    depth, quoted, escaped, comment = 0, False, False, False
    for i in range(open_at, len(text)):
        ch = text[i]
        if comment:
            if ch == "\n":
                comment = False
            continue
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == '"':
            quoted = True
        elif ch == "#":
            comment = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("Unclosed script block while filtering old decision surface")


def _remove_decisions(text: str, names: set[str]) -> str:
    """Remove selected decision blocks without disturbing adjacent legacy replies."""
    for name in names:
        text = _remove_blocks(text, {name})
    # Old bilateral helper decisions are all Cuban proposals with this prefix.
    while True:
        match = re.search(r"(?m)^\s*COLDWAR_CUB_offer_[a-z0-9_]+\s*=\s*\{", text)
        if not match:
            break
        open_at = text.find("{", match.start(), match.end())
        end = _matching_brace(text, open_at) + 1
        while end < len(text) and text[end] in " \t\r\n":
            end += 1
        text = text[:match.start()] + text[end:]
    return text


def main() -> None:
    from file_headers import stamp
    for rel, text in generate().items():
        text = stamp(text, 'Cuba 1970 foreign agreement support.', localisation=rel.endswith('.yml'))
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == ".yml":
            path.write_text(text, encoding="utf-8-sig", newline="\n")
        else:
            path.write_text(text, encoding="utf-8", newline="\n")
    print(f"generated {len(generate())} foreign-contract runtime files for {len(NODES)} agreements")


if __name__ == "__main__":
    main()
