# IMPERIA COLD WAR — Universal SSR diplomacy.
"""Generate the standing bilateral SSR agreements and consent workflow."""
from __future__ import annotations

import re
from pathlib import Path

import shared
import art


CONTRACTS = shared.data()["contracts"]
KEYS = tuple(CONTRACTS)
TAGS = tuple(shared.TAGS)
WATER_BASIN = {"KAZ", "UZB", "TRK", "KYR", "TAJ", "AFG"}
SANCTIONS = ("dip", "fin", "eco", "mil")
ACTIVITY_FLAG = "COLDWAR_SSR_dip_activity"


def _country_tags() -> tuple[str, ...]:
    """Read the real static map roster; dynamic civil-war tags are excluded."""
    found: set[str] = set()
    for rel in ("common/country_tags/00_countries.txt", "common/country_tags/01_countries.txt",
                "common/country_tags/mdcw_1970_historical_countries.txt"):
        path = shared.ROOT / rel
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            match = re.match(r"\s*([A-Z0-9]{3})\s*=", line)
            if match:
                found.add(match.group(1))
    return tuple(sorted(found))


PARTNERS = _country_tags()
PARTNER_PAGE_SIZE = 6
PARTNER_PAGES = [PARTNERS[i:i + PARTNER_PAGE_SIZE] for i in range(0, len(PARTNERS), PARTNER_PAGE_SIZE)]
ROOT_GROUP_PAGE_SIZE = 16
PARTNER_ROOT_GROUPS = [PARTNER_PAGES[i:i + ROOT_GROUP_PAGE_SIZE] for i in range(0, len(PARTNER_PAGES), ROOT_GROUP_PAGE_SIZE)]
SUBGROUP_PAGE_SIZE = 6
PARTNER_SUBGROUPS = [
    (root_index, local_index, root_pages[i:i + SUBGROUP_PAGE_SIZE])
    for root_index, root_pages in enumerate(PARTNER_ROOT_GROUPS)
    for local_index, i in enumerate(range(0, len(root_pages), SUBGROUP_PAGE_SIZE))
]
PAGE_SUBGROUP = {
    page_index: subgroup_index
    for subgroup_index, (_, _, pages) in enumerate(PARTNER_SUBGROUPS)
    for page in pages
    for page_index, source_page in enumerate(PARTNER_PAGES)
    if source_page is page
}


def _idea_id(key: str, side: str) -> str:
    return f"COLDWAR_SSR_diplomacy_{key}_{side}"


def _activity_conditions() -> str:
    flags = [f"has_country_flag = COLDWAR_SSR_dip_{key}_{state}" for key in KEYS for state in ("pending", "active")]
    flags.extend(
        f"has_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_{state}"
        for key in KEYS for origin in TAGS for state in ("pending", "active")
    )
    return "OR = { " + " ".join(flags) + " }"


def _refresh_activity_effect() -> str:
    return f"""COLDWAR_SSR_diplomacy_update_activity = {{
    if = {{ limit = {{ {_activity_conditions()} }} set_country_flag = {ACTIVITY_FLAG} }}
    else = {{ clr_country_flag = {ACTIVITY_FLAG} }}
}}"""


def _idea_effects(modifiers: dict) -> str:
    return " ".join(f"{key} = {shared.number(value)}" for key, value in modifiers.items())


def _standing_ready(from_tag: str, key: str, target_name: str) -> str:
    """Bilateral no-war/embargo/sanction guard for one named global target."""
    checks = [
        "exists = yes",
        f"NOT = {{ has_war_with = event_target:{target_name} }}",
        f"NOT = {{ is_embargoing = event_target:{target_name} }}",
    ]
    for cls in SANCTIONS:
        for direction in ("on_us", "by_us"):
            checks.append(
                f"NOT = {{ is_in_array = {{ array = imp_{cls}_sanc_{direction} "
                f"value = event_target:{target_name} }} }}"
            )
    other = [
        "exists = yes",
        f"NOT = {{ has_war_with = {from_tag} }}",
        f"NOT = {{ is_embargoing = {from_tag} }}",
    ]
    for cls in SANCTIONS:
        for direction in ("on_us", "by_us"):
            other.append(
                f"NOT = {{ is_in_array = {{ array = imp_{cls}_sanc_{direction} value = {from_tag} }} }}"
            )
    checks.append(f"event_target:{target_name} = {{ {' '.join(other)} }}")
    return "\n\t".join(checks)


def _candidate_trigger(key: str) -> str:
    if key == "clearing":
        return """AND = {
            is_subject = no
            any_owned_state = { always = yes }
            OR = {
            tag = SOV
            tag = event_target:COLDWAR_SSR_recognised_union_successor
            }
        }"""
    shared = "is_subject = no\n            any_owned_state = { always = yes }\n            NOT = { tag = ROOT }"
    capability = {
        "technical": "num_of_factories > 4",
        "training": "num_divisions > 5",
        "border": "is_neighbor_of = ROOT",
        "energy": "AND = { is_neighbor_of = ROOT OR = { oil > 0 ROOT = { oil > 0 } } }",
        "water": "OR = { tag = KAZ tag = UZB tag = TRK tag = KYR tag = TAJ tag = AFG }",
        "romanian": "tag = ROM",
    }[key]
    if key == "water":
        basin = "OR = { " + " ".join(f"tag = {tag}" for tag in sorted(WATER_BASIN)) + " }"
        return f"AND = {{ {shared} {capability} ROOT = {{ {basin} }} }}"
    if key == "romanian":
        return f"AND = {{ is_subject = no any_owned_state = {{ always = yes }} {capability} NOT = {{ tag = ROOT }} }}"
    return f"AND = {{ {shared} {capability} }}"


def _pair_trigger(from_tag: str, key: str, toward: bool) -> str:
    origin_target = f"COLDWAR_SSR_dip_from_{key}_{from_tag}"
    recipient_target = f"COLDWAR_SSR_dip_to_{key}_{from_tag}"
    if toward:
        # This trigger is evaluated in the current recipient's country scope.
        # Delegate the bilateral checks to the origin-scoped trigger so both
        # mirrored sanction arrays and both embargo/war directions use the
        # actual named pair, then bind this scope to the saved recipient.
        return (
            f"exists = yes\n"
            f"is_subject = no\n"
            f"any_owned_state = {{ always = yes }}\n"
            f"tag = event_target:{recipient_target}\n"
            f"event_target:{origin_target} = {{ COLDWAR_SSR_dip_pair_{key}_{from_tag}_from = yes }}"
        )

    target_name = recipient_target
    trigger = _standing_ready(from_tag, key, target_name)
    trigger += "\n\tCOLDWAR_SSR_is_independent = yes"
    trigger += f"\n\tevent_target:{target_name} = {{ is_subject = no }}"
    if key == "border":
        trigger += f"\n\tis_neighbor_of = event_target:{target_name}"
    elif key == "water":
        basin = "OR = { " + " ".join(f"tag = {tag}" for tag in sorted(WATER_BASIN)) + " }"
        trigger += f"\n\tAND = {{ {basin} event_target:{target_name} = {{ {basin} }} }}"
    elif key == "energy":
        trigger += f"\n\tis_neighbor_of = event_target:{target_name}\n\tOR = {{ oil > 0 event_target:{target_name} = {{ oil > 0 }} }}"
    elif key == "technical":
        trigger += f"\n\tevent_target:{target_name} = {{ num_of_factories > 4 }}"
    elif key == "training":
        trigger += f"\n\tevent_target:{target_name} = {{ num_divisions > 5 }}"
    elif key == "romanian":
        trigger += f"\n\t{'tag = ROM' if toward else f'event_target:{target_name} = {{ tag = ROM }}'}"
    return trigger


def _preview_rows(key: str) -> str:
    contract = CONTRACTS[key]
    origin_idea = _idea_id(key, "origin")
    recipient_idea = _idea_id(key, "recipient")
    o = contract["origin"]
    r = contract["recipient"]
    return f"""effect_tooltip = {{
        custom_effect_tooltip = TT_IF_THEY_ACCEPT
        custom_effect_tooltip = COLDWAR_SSR_origin_scope_tt
        add_ideas = {origin_idea}
        add_to_variable = {{ COLDWAR_SSR_preview_setup_origin = {shared.number(o['gdp_cost'])} tooltip = COLDWAR_SSR_setup_origin_share_tt }}
        add_to_variable = {{ COLDWAR_SSR_preview_weekly_origin = {shared.number(o['weekly_gdp_cost'])} tooltip = COLDWAR_SSR_weekly_origin_share_tt }}
        custom_effect_tooltip = COLDWAR_SSR_prospective_partner_tt
        add_ideas = {recipient_idea}
        add_to_variable = {{ COLDWAR_SSR_preview_setup_recipient = {shared.number(r['gdp_cost'])} tooltip = COLDWAR_SSR_setup_recipient_share_tt }}
        add_to_variable = {{ COLDWAR_SSR_preview_weekly_recipient = {shared.number(r['weekly_gdp_cost'])} tooltip = COLDWAR_SSR_weekly_recipient_share_tt }}
    }}"""


def _option_preview(key: str, target: str) -> str:
    contract = CONTRACTS[key]
    recipient_idea = _idea_id(key, "recipient")
    marginal = f"if = {{ limit = {{ NOT = {{ has_idea = {recipient_idea} }} }} add_ideas = {recipient_idea} add_to_variable = {{ COLDWAR_SSR_preview_weekly_recipient = {shared.number(contract['recipient']['weekly_gdp_cost'])} tooltip = COLDWAR_SSR_weekly_recipient_share_tt }} }} else = {{ add_to_variable = {{ COLDWAR_SSR_preview_weekly_recipient = 0 tooltip = COLDWAR_SSR_weekly_recipient_zero_tt }} }}"
    return f"""effect_tooltip = {{
        custom_effect_tooltip = TT_IF_THEY_ACCEPT
        custom_effect_tooltip = COLDWAR_SSR_origin_scope_tt
        add_ideas = {_idea_id(key, 'origin')}
        add_to_variable = {{ COLDWAR_SSR_preview_setup_origin = {shared.number(contract['origin']['gdp_cost'])} tooltip = COLDWAR_SSR_setup_origin_share_tt }}
        add_to_variable = {{ COLDWAR_SSR_preview_weekly_origin = {shared.number(contract['origin']['weekly_gdp_cost'])} tooltip = COLDWAR_SSR_weekly_origin_share_tt }}
        custom_effect_tooltip = COLDWAR_SSR_prospective_partner_tt
        {target} = {{ {marginal} add_to_variable = {{ COLDWAR_SSR_preview_setup_recipient = {shared.number(contract['recipient']['gdp_cost'])} tooltip = COLDWAR_SSR_setup_recipient_share_tt }} }}
    }}"""


def _eligible_any(key: str, tags: tuple[str, ...] | list[str]) -> str:
    choices = " ".join(f"AND = {{ tag = {tag} {_candidate_trigger(key)} }}" for tag in tags)
    return f"any_country = {{ OR = {{ {choices} }} }}"


def _validate_origin_cash(key: str) -> str:
    return shared.number(CONTRACTS[key]["origin"]["gdp_cost"])


def _validate_recipient_cash(key: str) -> str:
    return shared.number(CONTRACTS[key]["recipient"]["gdp_cost"])


def _visible_pair_requirements(key: str, origin: str) -> str:
    """Meaningful live terms shown directly in the recipient decision."""
    target_name = f"COLDWAR_SSR_dip_from_{key}_{origin}"
    current = [
        "is_subject = no",
        f"NOT = {{ has_war_with = event_target:{target_name} }}",
        f"NOT = {{ is_embargoing = event_target:{target_name} }}",
    ]
    for cls in SANCTIONS:
        for direction in ("on_us", "by_us"):
            current.append(f"NOT = {{ is_in_array = {{ array = imp_{cls}_sanc_{direction} value = event_target:{target_name} }} }}")
    source = [
        "is_subject = no",
        "COLDWAR_SSR_is_independent = yes",
        f"NOT = {{ has_war_with = ROOT }}",
        f"NOT = {{ is_embargoing = ROOT }}",
    ]
    for cls in SANCTIONS:
        for direction in ("on_us", "by_us"):
            source.append(f"NOT = {{ is_in_array = {{ array = imp_{cls}_sanc_{direction} value = ROOT }} }}")
    if key == "border":
        current.append(f"is_neighbor_of = event_target:{target_name}")
    elif key == "water":
        basin = "OR = { " + " ".join(f"tag = {tag}" for tag in sorted(WATER_BASIN)) + " }"
        current.append(f"AND = {{ {basin} event_target:{target_name} = {{ {basin} }} }}")
    elif key == "energy":
        current.extend((f"is_neighbor_of = event_target:{target_name}", f"OR = {{ oil > 0 event_target:{target_name} = {{ oil > 0 }} }}"))
    elif key == "romanian":
        current.append("tag = ROM")
    capability = {"technical": "num_of_factories > 4", "training": "num_divisions > 5"}.get(key)
    if capability:
        current.append(capability)
    if key == "romanian":
        source.append("original_tag = MLV")
    return " ".join(current) + f" {origin} = {{ {' '.join(source)} }}"


def _render_triggers() -> str:
    out: list[str] = []
    # Visible focus availability; the country list is kept to real static tags.
    for key in KEYS:
        candidate = _candidate_trigger(key)
        origin_guard = "tag = MLV\n    " if key == "romanian" else ""
        out.append(f"""COLDWAR_SSR_can_offer_{key} = {{
    {origin_guard}
    COLDWAR_SSR_is_independent = yes
    NOT = {{ has_country_flag = COLDWAR_SSR_dip_{key}_pending }}
    NOT = {{ has_country_flag = COLDWAR_SSR_dip_{key}_active }}
    any_country = {{ {candidate} }}
}}""")
    # Each stored bilateral target is checked from the origin and recipient scopes.
    for key in KEYS:
        for origin in TAGS:
            for toward in (False, True):
                name = f"COLDWAR_SSR_dip_pair_{key}_{origin}_{'to' if toward else 'from'}"
                out.append(f"{name} = {{\n    {_pair_trigger(origin, key, toward)}\n}}")
    # A negotiated transition is valid only while a standing clearing pair to the
    # Union centre or its recorded successor remains in force.
    clearing = []
    for origin in TAGS:
        target = f"COLDWAR_SSR_dip_to_clearing_{origin}"
        clearing.append(f"AND = {{ tag = {origin} has_country_flag = COLDWAR_SSR_dip_clearing_active COLDWAR_SSR_dip_pair_clearing_{origin}_from = yes OR = {{ event_target:{target} = {{ tag = SOV }} event_target:{target} = {{ tag = event_target:COLDWAR_SSR_recognised_union_successor }} }} }}")
    out.append("COLDWAR_SSR_negotiated_transition_active = { OR = { " + " ".join(clearing) + " } }")
    return "\n\n".join(out) + "\n"


def _render_ideas() -> str:
    ideas: list[str] = []
    for key, contract in CONTRACTS.items():
        for side in ("origin", "recipient"):
            idea = _idea_id(key, side)
            title = contract[side]["spirit"]
            ideas.append(f"""{idea} = {{
            picture = {art.picture_for_idea(idea)}
            allowed = {{ always = yes }}
            allowed_civil_war = {{ always = yes }}
            modifier = {{ {_idea_effects(contract[side]['modifiers'])} }}
        }}""")
    return "ideas = {\n    country = {\n        " + "\n\n        ".join(ideas) + "\n    }\n}\n"


def _dispatch_effect(key: str) -> str:
    branches = []
    for origin in TAGS:
        branches.append(f"""    if = {{
        limit = {{ tag = {origin} COLDWAR_SSR_can_offer_{key} = yes }}
        set_country_flag = COLDWAR_SSR_dip_{key}_pending
        set_country_flag = COLDWAR_SSR_dip_{key}_ever_offered
        set_country_flag = {ACTIVITY_FLAG}
        save_global_event_target_as = COLDWAR_SSR_dip_from_{key}_{origin}
        event_target:COLDWAR_SSR_dip_selected_partner = {{
            save_global_event_target_as = COLDWAR_SSR_dip_to_{key}_{origin}
            set_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_pending
            set_country_flag = {ACTIVITY_FLAG}
            country_event = {{ id = COLDWAR_SSR_DIP.{6001 + KEYS.index(key)} }}
        }}
    }}""")
    return f"COLDWAR_SSR_dip_dispatch_{key} = {{\n" + "\n".join(branches) + "\n}"


def _accept_effect(key: str, origin: str) -> str:
    to_name = f"COLDWAR_SSR_dip_to_{key}_{origin}"
    active_origin = f"COLDWAR_SSR_dip_{key}_active"
    active_recipient = f"COLDWAR_SSR_dip_in_{key}_from_{origin}_active"
    valid = f"COLDWAR_SSR_dip_pair_{key}_{origin}_to = yes"
    capability = {"technical": "num_of_factories > 4", "training": "num_divisions > 5"}.get(key)
    capability_guard = capability or ""
    return f"""COLDWAR_SSR_dip_accept_{key}_{origin} = {{
    set_temp_variable = {{ COLDWAR_SSR_dip_setup = {{ value = gdp_total multiply = {_validate_recipient_cash(key)} }} }}
    {origin} = {{ set_temp_variable = {{ COLDWAR_SSR_dip_setup = {{ value = gdp_total multiply = {_validate_origin_cash(key)} }} }} }}
    if = {{
        limit = {{
            has_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_pending
            is_subject = no
            tag = event_target:{to_name}
            {valid}
            {origin} = {{ COLDWAR_SSR_is_independent = yes has_country_flag = COLDWAR_SSR_dip_{key}_pending }}
            {capability_guard}
            check_variable = {{ var = treasury value = COLDWAR_SSR_dip_setup compare = greater_than_or_equals }}
            {origin} = {{ check_variable = {{ var = treasury value = COLDWAR_SSR_dip_setup compare = greater_than_or_equals }} }}
        }}
        {origin} = {{
            set_temp_variable = {{ treasury_change = {{ value = COLDWAR_SSR_dip_setup multiply = -1 }} }}
            modify_treasury_effect = yes
            clr_country_flag = COLDWAR_SSR_dip_{key}_pending
            set_country_flag = {active_origin}
            add_ideas = {_idea_id(key, 'origin')}
        }}
        set_temp_variable = {{ treasury_change = {{ value = COLDWAR_SSR_dip_setup multiply = -1 }} }}
        modify_treasury_effect = yes
        clr_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_pending
        set_country_flag = {active_recipient}
        COLDWAR_SSR_diplomacy_reconcile = yes
        {origin} = {{ COLDWAR_SSR_diplomacy_reconcile = yes }}
    }}
    else = {{ country_event = {{ id = COLDWAR_SSR_DIP.{6001 + KEYS.index(key)} }} }}
}}"""


def _refuse_effect(key: str, origin: str) -> str:
    to_name = f"COLDWAR_SSR_dip_to_{key}_{origin}"
    return f"""COLDWAR_SSR_dip_refuse_{key}_{origin} = {{
    if = {{
        limit = {{ tag = event_target:{to_name} has_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_pending }}
        clr_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_pending
        {origin} = {{
            clr_country_flag = COLDWAR_SSR_dip_{key}_pending
            set_country_flag = {{ flag = COLDWAR_SSR_dip_{key}_retry_wait value = 1 days = 180 }}
            COLDWAR_SSR_diplomacy_update_activity = yes
        }}
        clear_global_event_target = COLDWAR_SSR_dip_to_{key}_{origin}
        clear_global_event_target = COLDWAR_SSR_dip_from_{key}_{origin}
        COLDWAR_SSR_diplomacy_update_activity = yes
    }}
}}"""


def _terminate_effect(key: str, origin: str) -> str:
    to_name = f"COLDWAR_SSR_dip_to_{key}_{origin}"
    return f"""COLDWAR_SSR_dip_terminate_{key}_{origin} = {{
    if = {{
        limit = {{ tag = event_target:{to_name} has_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_active }}
        {origin} = {{
            clr_country_flag = COLDWAR_SSR_dip_{key}_pending
            clr_country_flag = COLDWAR_SSR_dip_{key}_active
            COLDWAR_SSR_diplomacy_reconcile = yes
            COLDWAR_SSR_diplomacy_update_activity = yes
        }}
        clr_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_pending
        clr_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_active
        clear_global_event_target = COLDWAR_SSR_dip_to_{key}_{origin}
        clear_global_event_target = COLDWAR_SSR_dip_from_{key}_{origin}
        COLDWAR_SSR_diplomacy_reconcile = yes
        COLDWAR_SSR_diplomacy_update_activity = yes
    }}
}}"""


def _terminate_origin_effect(key: str, origin: str) -> str:
    to_name = f"COLDWAR_SSR_dip_to_{key}_{origin}"
    return f"""COLDWAR_SSR_dip_terminate_origin_{key}_{origin} = {{
    if = {{
        limit = {{ has_country_flag = COLDWAR_SSR_dip_{key}_active }}
        event_target:{to_name} = {{
            clr_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_active
            COLDWAR_SSR_diplomacy_reconcile = yes
            COLDWAR_SSR_diplomacy_update_activity = yes
        }}
        clr_country_flag = COLDWAR_SSR_dip_{key}_active
        remove_ideas = {_idea_id(key, 'origin')}
        COLDWAR_SSR_diplomacy_update_activity = yes
        clear_global_event_target = {to_name}
        clear_global_event_target = COLDWAR_SSR_dip_from_{key}_{origin}
        COLDWAR_SSR_diplomacy_reconcile = yes
    }}
}}"""


def _render_effects() -> str:
    effects: list[str] = []
    for key in KEYS:
        event_id = 700 + KEYS.index(key)
        effects.append(f"COLDWAR_SSR_offer_{key} = {{ if = {{ limit = {{ COLDWAR_SSR_can_offer_{key} = yes }} set_country_flag = COLDWAR_SSR_dip_{key}_ever_offered country_event = {{ id = COLDWAR_SSR_DIP.{event_id} }} }} }}")
        effects.append(f"COLDWAR_SSR_dip_cancel_selection_{key} = {{ set_country_flag = COLDWAR_SSR_dip_{key}_ever_offered }}")
        effects.append(f"COLDWAR_SSR_preview_offer_{key} = {{ {_preview_rows(key)} }}")
        effects.append(_dispatch_effect(key))
        for origin in TAGS:
            effects.extend((_accept_effect(key, origin), _refuse_effect(key, origin), _terminate_effect(key, origin), _terminate_origin_effect(key, origin)))
    effects.append(_refresh_activity_effect())
    # Reconciliation is idempotent and only evaluates the fixed fourteen origins
    # plus this country's seven outgoing contracts, never scans the world.
    rec: list[str] = [f"COLDWAR_SSR_diplomacy_reconcile = {{\n    if = {{\n        limit = {{ has_country_flag = {ACTIVITY_FLAG} }}"]
    for key in KEYS:
        for origin in TAGS:
            recipient_idea = _idea_id(key, "recipient")
            rec.append(f"""    if = {{
        limit = {{ has_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_active COLDWAR_SSR_dip_pair_{key}_{origin}_to = yes NOT = {{ has_idea = {recipient_idea} }} }}
        add_ideas = {recipient_idea}
    }}""")
        rec.append(f"""    if = {{
        limit = {{ NOT = {{ OR = {{ {' '.join(f'AND = {{ has_country_flag = COLDWAR_SSR_dip_in_{key}_from_{t}_active COLDWAR_SSR_dip_pair_{key}_{t}_to = yes }}' for t in TAGS)} }} }} has_idea = {_idea_id(key, 'recipient')} }}
        remove_ideas = {_idea_id(key, 'recipient')}
    }}""")
    for key in KEYS:
        for origin in TAGS:
            recipient_target = f"COLDWAR_SSR_dip_to_{key}_{origin}"
            recipient_reconcile = f"event_target:{recipient_target} = {{ COLDWAR_SSR_diplomacy_reconcile = yes }}"
            rec.append(f"""    if = {{
        limit = {{ tag = {origin} has_country_flag = COLDWAR_SSR_dip_{key}_active }}
        if = {{
            limit = {{ COLDWAR_SSR_dip_pair_{key}_{origin}_from = yes NOT = {{ has_idea = {_idea_id(key, 'origin')} }} }}
            add_ideas = {_idea_id(key, 'origin')}
            {recipient_reconcile}
        }}
        else_if = {{
            limit = {{ COLDWAR_SSR_dip_pair_{key}_{origin}_from = no has_idea = {_idea_id(key, 'origin')} }}
            remove_ideas = {_idea_id(key, 'origin')}
            {recipient_reconcile}
        }}
    }}
    if = {{ limit = {{ tag = {origin} NOT = {{ has_country_flag = COLDWAR_SSR_dip_{key}_active }} has_idea = {_idea_id(key, 'origin')} }} remove_ideas = {_idea_id(key, 'origin')} }}""")
    rec.extend(("    }", "}"))
    effects.append("\n".join(rec))
    budget: list[str] = [
        "COLDWAR_SSR_diplomacy_refresh_budget = {",
        "    set_variable = { COLDWAR_SSR_diplomacy_weekly_expense = 0 }",
        "    set_temp_variable = { COLDWAR_SSR_dip_weekly_fraction = 0 }",
        f"    if = {{",
        f"        limit = {{ has_country_flag = {ACTIVITY_FLAG} }}",
        "        COLDWAR_SSR_diplomacy_reconcile = yes",
    ]
    for key in KEYS:
        budget.append(f"    set_temp_variable = {{ COLDWAR_SSR_dip_seen_{key} = 0 }}")
        for origin in TAGS:
            frac = shared.number(CONTRACTS[key]["recipient"]["weekly_gdp_cost"])
            budget.append(f"""    if = {{
        limit = {{ check_variable = {{ COLDWAR_SSR_dip_seen_{key} = 0 }} has_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_active COLDWAR_SSR_dip_pair_{key}_{origin}_to = yes }}
        add_to_temp_variable = {{ COLDWAR_SSR_dip_weekly_fraction = {frac} }}
        set_temp_variable = {{ COLDWAR_SSR_dip_seen_{key} = 1 }}
    }}""")
        for origin in TAGS:
            budget.append(f"""    if = {{
        limit = {{ tag = {origin} has_country_flag = COLDWAR_SSR_dip_{key}_active COLDWAR_SSR_dip_pair_{key}_{origin}_from = yes }}
        add_to_temp_variable = {{ COLDWAR_SSR_dip_weekly_fraction = {shared.number(CONTRACTS[key]['origin']['weekly_gdp_cost'])} }}
    }}""")
    budget.append("        set_variable = { COLDWAR_SSR_diplomacy_weekly_expense = { value = gdp_total multiply = COLDWAR_SSR_dip_weekly_fraction } }\n    }\n}")
    effects.append("\n".join(budget))
    return "\n\n".join(effects) + "\n"


def _render_events() -> str:
    out = ["add_namespace = COLDWAR_SSR_DIP"]
    # Four-stage paging keeps every popup within the native event-button grid.
    for key_index, key in enumerate(KEYS):
        category_options = []
        for root_index, root_pages in enumerate(PARTNER_ROOT_GROUPS):
            tags = tuple(tag for page in root_pages for tag in page)
            category_options.append(f"""    option = {{
        name = COLDWAR_SSR_select_{key}_group_{root_index}
        trigger = {{ {_eligible_any(key, tags)} }}
        country_event = {{ id = COLDWAR_SSR_DIP.{1000 + key_index * len(PARTNER_ROOT_GROUPS) + root_index} }}
    }}""")
        category_options.append(f"option = {{ name = COLDWAR_SSR_select_cancel COLDWAR_SSR_dip_cancel_selection_{key} = yes }}")
        out.append(f"""country_event = {{
    id = COLDWAR_SSR_DIP.{700 + key_index}
    title = COLDWAR_SSR_select_{key}_root_title
    desc = COLDWAR_SSR_select_{key}_root_desc
    picture = GFX_message_signing
    is_triggered_only = yes
    trigger = {{ COLDWAR_SSR_can_offer_{key} = yes }}
{chr(10).join(category_options)}
}}""")
        for root_index, root_pages in enumerate(PARTNER_ROOT_GROUPS):
            subgroup_options = []
            subgroup_ids = [i for i, (group, _, _) in enumerate(PARTNER_SUBGROUPS) if group == root_index]
            for subgroup_index in subgroup_ids:
                _, _, pages = PARTNER_SUBGROUPS[subgroup_index]
                tags = tuple(tag for page in pages for tag in page)
                subgroup_options.append(f"""    option = {{
        name = COLDWAR_SSR_select_{key}_subgroup_{subgroup_index}
        trigger = {{ {_eligible_any(key, tags)} }}
        country_event = {{ id = COLDWAR_SSR_DIP.{2000 + key_index * len(PARTNER_SUBGROUPS) + subgroup_index} }}
    }}""")
            subgroup_options.append(f"option = {{ name = COLDWAR_SSR_select_back country_event = {{ id = COLDWAR_SSR_DIP.{700 + key_index} }} }}")
            subgroup_options.append(f"option = {{ name = COLDWAR_SSR_select_cancel COLDWAR_SSR_dip_cancel_selection_{key} = yes }}")
            page_event_id = 1000 + key_index * len(PARTNER_ROOT_GROUPS) + root_index
            out.append(f"""country_event = {{
    id = COLDWAR_SSR_DIP.{page_event_id}
    title = COLDWAR_SSR_select_{key}_subgroups_title
    desc = COLDWAR_SSR_select_{key}_subgroups_desc
    picture = GFX_message_signing
    is_triggered_only = yes
    trigger = {{ COLDWAR_SSR_can_offer_{key} = yes }}
{chr(10).join(subgroup_options)}
}}""")
        for subgroup_index, (root_index, _, subgroup_pages) in enumerate(PARTNER_SUBGROUPS):
            page_options = []
            for page in subgroup_pages:
                page_index = PARTNER_PAGES.index(page)
                page_options.append(f"""    option = {{
        name = COLDWAR_SSR_select_{key}_page_{page_index}
        trigger = {{ {_eligible_any(key, page)} }}
        country_event = {{ id = COLDWAR_SSR_DIP.{4000 + key_index * len(PARTNER_PAGES) + page_index} }}
    }}""")
            page_options.append(f"option = {{ name = COLDWAR_SSR_select_back country_event = {{ id = COLDWAR_SSR_DIP.{1000 + key_index * len(PARTNER_ROOT_GROUPS) + root_index} }} }}")
            page_options.append(f"option = {{ name = COLDWAR_SSR_select_cancel COLDWAR_SSR_dip_cancel_selection_{key} = yes }}")
            subgroup_event_id = 2000 + key_index * len(PARTNER_SUBGROUPS) + subgroup_index
            out.append(f"""country_event = {{
    id = COLDWAR_SSR_DIP.{subgroup_event_id}
    title = COLDWAR_SSR_select_{key}_pages_title
    desc = COLDWAR_SSR_select_{key}_pages_desc
    picture = GFX_message_signing
    is_triggered_only = yes
    trigger = {{ COLDWAR_SSR_can_offer_{key} = yes }}
{chr(10).join(page_options)}
}}""")
        for page_index, page in enumerate(PARTNER_PAGES):
            country_options = []
            for target in page:
                country_options.append(f"""    option = {{
        name = COLDWAR_SSR_select_{key}_{target}
        trigger = {{ {target} = {{ {_candidate_trigger(key)} }} }}
        {_option_preview(key, target)}
        {target} = {{ save_event_target_as = COLDWAR_SSR_dip_selected_partner }}
        COLDWAR_SSR_dip_dispatch_{key} = yes
    }}""")
            subgroup_index = PAGE_SUBGROUP[page_index]
            country_options.append(f"option = {{ name = COLDWAR_SSR_select_back country_event = {{ id = COLDWAR_SSR_DIP.{2000 + key_index * len(PARTNER_SUBGROUPS) + subgroup_index} }} }}")
            country_options.append(f"option = {{ name = COLDWAR_SSR_select_cancel COLDWAR_SSR_dip_cancel_selection_{key} = yes }}")
            page_event_id = 4000 + key_index * len(PARTNER_PAGES) + page_index
            out.append(f"""country_event = {{
    id = COLDWAR_SSR_DIP.{page_event_id}
    title = COLDWAR_SSR_select_{key}_partner_title
    desc = COLDWAR_SSR_select_{key}_partner_desc
    picture = GFX_message_signing
    is_triggered_only = yes
    trigger = {{ COLDWAR_SSR_can_offer_{key} = yes }}
{chr(10).join(country_options)}
}}""")
    # Each named recipient sees a notice; consent is expressed later in their
    # ordinary national Decisions panel, never by this event.
    for key_index, key in enumerate(KEYS):
        inbound = " ".join(f"has_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_pending" for origin in TAGS)
        out.append(f"""country_event = {{
    id = COLDWAR_SSR_DIP.{6001 + key_index}
    title = COLDWAR_SSR_dip_notice_title
    desc = COLDWAR_SSR_dip_notice_desc
    picture = GFX_message_signing
    is_triggered_only = yes
    trigger = {{ OR = {{ {inbound} }} }}
    option = {{ name = COLDWAR_SSR_dip_notice_review }}
}}""")
    return "\n\n".join(out) + "\n"


def _render_decisions() -> str:
    out = ["COLDWAR_SSR_diplomacy_responses = {"]
    for origin in TAGS:
        for key in KEYS:
            to_name = f"COLDWAR_SSR_dip_to_{key}_{origin}"
            recipient_idea = _idea_id(key, "recipient")
            recipient_marginal = f"if = {{ limit = {{ NOT = {{ has_idea = {recipient_idea} }} }} add_ideas = {recipient_idea} add_to_variable = {{ COLDWAR_SSR_preview_weekly_recipient = {shared.number(CONTRACTS[key]['recipient']['weekly_gdp_cost'])} tooltip = COLDWAR_SSR_weekly_recipient_share_tt }} }} else = {{ add_to_variable = {{ COLDWAR_SSR_preview_weekly_recipient = 0 tooltip = COLDWAR_SSR_weekly_recipient_zero_tt }} }}"
            out.append(f"""    COLDWAR_SSR_dip_accept_{key}_{origin} = {{
        icon = generic_diplomacy
        visible = {{ has_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_pending }}
        available = {{ hidden_trigger = {{ tag = event_target:{to_name} has_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_pending {origin} = {{ has_country_flag = COLDWAR_SSR_dip_{key}_pending }} }} {_visible_pair_requirements(key, origin)} }}
        cost = 0
        days_remove = 1
        complete_effect = {{ effect_tooltip = {{ custom_effect_tooltip = TT_IF_THEY_ACCEPT custom_effect_tooltip = COLDWAR_SSR_origin_scope_tt {origin} = {{ add_ideas = {_idea_id(key,'origin')} add_to_variable = {{ COLDWAR_SSR_preview_setup_origin = {shared.number(CONTRACTS[key]['origin']['gdp_cost'])} tooltip = COLDWAR_SSR_setup_origin_share_tt }} add_to_variable = {{ COLDWAR_SSR_preview_weekly_origin = {shared.number(CONTRACTS[key]['origin']['weekly_gdp_cost'])} tooltip = COLDWAR_SSR_weekly_origin_share_tt }} }} custom_effect_tooltip = COLDWAR_SSR_prospective_partner_tt add_to_variable = {{ COLDWAR_SSR_preview_setup_recipient = {shared.number(CONTRACTS[key]['recipient']['gdp_cost'])} tooltip = COLDWAR_SSR_setup_recipient_share_tt }} {recipient_marginal} }} COLDWAR_SSR_dip_accept_{key}_{origin} = yes }}
        ai_will_do = {{ base = 0 }}
    }}
    COLDWAR_SSR_dip_refuse_{key}_{origin} = {{
        icon = generic_diplomacy
        visible = {{ has_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_pending }}
        available = {{ hidden_trigger = {{ tag = event_target:COLDWAR_SSR_dip_to_{key}_{origin} }} has_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_pending {origin} = {{ has_country_flag = COLDWAR_SSR_dip_{key}_pending }} }}
        cost = 0
        days_remove = 1
        complete_effect = {{ COLDWAR_SSR_dip_refuse_{key}_{origin} = yes }}
        ai_will_do = {{ base = 0 }}
    }}
    COLDWAR_SSR_dip_end_{key}_{origin} = {{
        icon = generic_diplomacy
        visible = {{ has_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_active }}
        available = {{ hidden_trigger = {{ tag = event_target:COLDWAR_SSR_dip_to_{key}_{origin} }} has_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_active }}
        cost = 0
        days_remove = 1
        complete_effect = {{ COLDWAR_SSR_dip_terminate_{key}_{origin} = yes }}
        ai_will_do = {{ base = 0 }}
    }}""")
    for key in KEYS:
        out.append(f"""    COLDWAR_SSR_dip_retry_{key} = {{
        icon = generic_diplomacy
        visible = {{ has_country_flag = COLDWAR_SSR_dip_{key}_ever_offered }}
        available = {{ COLDWAR_SSR_is_independent = yes has_country_flag = COLDWAR_SSR_dip_{key}_ever_offered NOT = {{ has_country_flag = COLDWAR_SSR_dip_{key}_retry_wait }} COLDWAR_SSR_can_offer_{key} = yes }}
        cost = 0
        days_remove = 1
        complete_effect = {{ COLDWAR_SSR_offer_{key} = yes }}
        ai_will_do = {{ base = 0 }}
    }}""")
        out.append(f"""    COLDWAR_SSR_dip_end_origin_{key} = {{
        icon = generic_diplomacy
        visible = {{ has_country_flag = COLDWAR_SSR_dip_{key}_active }}
        available = {{ has_country_flag = COLDWAR_SSR_dip_{key}_active }}
        cost = 0
        days_remove = 1
        complete_effect = {{ {' '.join(f'if = {{ limit = {{ tag = {tag} }} COLDWAR_SSR_dip_terminate_origin_{key}_{tag} = yes }}' for tag in TAGS)} }}
        ai_will_do = {{ base = 0 }}
    }}""")
    out.append("}\n")
    return "\n".join(out)


def _render_localisation() -> str:
    loc: dict[str, str] = {}
    loc["COLDWAR_SSR_prospective_partner_tt"] = "Prospective partner:"
    loc["COLDWAR_SSR_origin_scope_tt"] = "Origin:"
    loc["COLDWAR_SSR_setup_origin_share_tt"] = "Setup contribution: [?COLDWAR_SSR_preview_setup_origin|%] of current GDP."
    loc["COLDWAR_SSR_setup_recipient_share_tt"] = "Setup contribution: [?COLDWAR_SSR_preview_setup_recipient|%] of current GDP."
    loc["COLDWAR_SSR_weekly_origin_share_tt"] = "Weekly allocation: [?COLDWAR_SSR_preview_weekly_origin|%] of current GDP."
    loc["COLDWAR_SSR_weekly_recipient_share_tt"] = "Weekly allocation: [?COLDWAR_SSR_preview_weekly_recipient|%] of current GDP."
    loc["COLDWAR_SSR_weekly_recipient_zero_tt"] = "Additional weekly allocation: [?COLDWAR_SSR_preview_weekly_recipient|%] of current GDP."
    loc["COLDWAR_SSR_diplomacy_responses"] = "Bilateral agreements"
    loc["COLDWAR_SSR_dip_notice_title"] = "A bilateral convention is offered"
    loc["COLDWAR_SSR_dip_notice_desc"] = "A named partner has submitted terms for review. The convention takes effect only if you accept it in Decisions."
    loc["COLDWAR_SSR_dip_notice_review"] = "Review the terms"
    loc["COLDWAR_SSR_select_back"] = "Return to the previous choices"
    loc["COLDWAR_SSR_select_cancel"] = "Cancel this offer"
    for key, contract in CONTRACTS.items():
        title = contract["title"]
        loc[f"COLDWAR_SSR_select_{key}_root_title"] = f"Choose a partner range for the {title}"
        loc[f"COLDWAR_SSR_select_{key}_root_desc"] = "Choose the range containing the country you intend to approach."
        loc[f"COLDWAR_SSR_select_{key}_subgroups_title"] = f"Narrow the partner range for the {title}"
        loc[f"COLDWAR_SSR_select_{key}_subgroups_desc"] = "Choose the smaller range containing the country you intend to approach."
        loc[f"COLDWAR_SSR_select_{key}_pages_title"] = f"Choose a partner range for the {title}"
        loc[f"COLDWAR_SSR_select_{key}_pages_desc"] = "Choose the range containing the country you intend to approach."
        loc[f"COLDWAR_SSR_select_{key}_partner_title"] = f"Select a named partner for the {title}"
        loc[f"COLDWAR_SSR_select_{key}_partner_desc"] = "The selected country receives the complete terms and decides whether to accept."
        for group_index, page_group in enumerate(PARTNER_ROOT_GROUPS):
            tags = tuple(tag for page in page_group for tag in page)
            loc[f"COLDWAR_SSR_select_{key}_group_{group_index}"] = f"Countries from [{tags[0]}.GetName] through [{tags[-1]}.GetName]"
        for subgroup_index, (_, _, pages) in enumerate(PARTNER_SUBGROUPS):
            tags = tuple(tag for page in pages for tag in page)
            loc[f"COLDWAR_SSR_select_{key}_subgroup_{subgroup_index}"] = f"Countries from [{tags[0]}.GetName] through [{tags[-1]}.GetName]"
        for page_index, page in enumerate(PARTNER_PAGES):
            loc[f"COLDWAR_SSR_select_{key}_page_{page_index}"] = f"Countries from [{page[0]}.GetName] through [{page[-1]}.GetName]"
        for tag in PARTNERS:
            loc[f"COLDWAR_SSR_select_{key}_{tag}"] = f"Offer the {title} to [{tag}.GetName]"
        for side in ("origin", "recipient"):
            loc[_idea_id(key, side)] = contract[side]["spirit"]
            loc[_idea_id(key, side) + "_desc"] = "A standing bilateral convention with scheduled national funding."
            loc[f"COLDWAR_SSR_dip_accept_{key}_heading"] = "Accept the convention"
            loc[f"COLDWAR_SSR_dip_refuse_{key}_heading"] = "Decline the convention"
    for tag in TAGS:
        for key, contract in CONTRACTS.items():
            loc[f"COLDWAR_SSR_dip_notice_{key}_{tag}_title"] = f"{contract['title']} from [{tag}.GetName]"
            loc[f"COLDWAR_SSR_dip_notice_{key}_{tag}_desc"] = "Review the complete terms and decide in the Diplomacy Decisions."
    for key, contract in CONTRACTS.items():
        loc[f"COLDWAR_SSR_dip_retry_{key}"] = f"Renegotiate the {contract['title']}"
        loc[f"COLDWAR_SSR_dip_end_origin_{key}"] = f"Terminate the {contract['title']}"
        loc[f"COLDWAR_SSR_dip_end_{key}_title"] = f"Terminate the {contract['title']}"
        for origin in TAGS:
            loc[f"COLDWAR_SSR_dip_accept_{key}_{origin}"] = f"Accept the {contract['title']} from [{origin}.GetName]"
            loc[f"COLDWAR_SSR_dip_refuse_{key}_{origin}"] = f"Decline the {contract['title']} from [{origin}.GetName]"
            loc[f"COLDWAR_SSR_dip_end_{key}_{origin}"] = f"Terminate the {contract['title']} with [{origin}.GetName]"
    return shared.loc_text(loc)


def _render_decision_category() -> str:
    outbound = " ".join(
        f"has_country_flag = COLDWAR_SSR_dip_{key}_{suffix}"
        for key in KEYS for suffix in ("ever_offered", "pending", "active", "retry_wait")
    )
    inbound = " ".join(
        f"has_country_flag = COLDWAR_SSR_dip_in_{key}_from_{origin}_{suffix}"
        for key in KEYS for origin in TAGS for suffix in ("pending", "active")
    )
    return f"""COLDWAR_SSR_diplomacy_responses = {{
    allowed = {{ always = yes }}
    icon = generic_diplomacy
    priority = 210
    visible = {{ OR = {{ OR = {{ {outbound} }} OR = {{ {inbound} }} }} }}
}}
"""


def generate() -> list[str]:
    """Write this module's runtime and English files; return repo-relative paths."""
    return [
        shared.write("common/ideas/COLDWAR_SSR_diplomacy.txt", _render_ideas()),
        shared.write("common/scripted_triggers/COLDWAR_SSR_diplomacy.txt", _render_triggers()),
        shared.write("common/scripted_effects/COLDWAR_SSR_diplomacy.txt", _render_effects()),
        shared.write("events/COLDWAR_SSR_diplomacy.txt", _render_events()),
        shared.write("common/decisions/COLDWAR_SSR_diplomacy.txt", _render_decisions()),
        shared.write("common/decisions/categories/COLDWAR_SSR_diplomacy.txt", _render_decision_category()),
        shared.write("localisation/english/COLDWAR_SSR_diplomacy_l_english.yml", _render_localisation(), localisation=True),
    ]


if __name__ == "__main__":
    for path in generate():
        print(path)
