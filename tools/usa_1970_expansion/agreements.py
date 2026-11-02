# IMPERIA COLD WAR — USA recipient-approved agreement compiler.
"""Emit only this module's agreements, previews, recipient controls and manifest.

Importing is side-effect free. The approved proposal remains the terms source.
No focus, money-system, on-action or legacy US file is written here.
"""
from __future__ import annotations

import ast
import copy
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from usa_building_capacity import capacity_trigger, building_definitions

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent / "agreements"
SOURCE = ROOT / "docs/design/usa_1970_expansion_20261024/proposal.json"
P = "COLDWAR_USA_agreements"
STEM = "COLDWAR_USA_1970_agreements"
NAMESPACE = "COLDWAR_USA_agreements"
ORDER = ("germany_forward", "germany_sustain", "canada", "britain", "japan",
         "south_vietnam", "china", "soviet_exchange", "bahrain", "israel", "saudi",
         "mexico", "rogers", "atlantic_research", "canada_retool", "pacific_maintenance")

# Native keys, not new modifier aliases. Source anchors are recorded in the manifest.
MODIFIERS = {
    "Division organisation": ("army_org_factor", False),
    "Planning speed": ("planning_speed", False),
    "Personnel cost": ("personnel_cost_multiplier_modifier", True),
    "Organisation regain": ("army_org_regain", False),
    "Equipment cost": ("equipment_cost_multiplier_modifier", True),
    "Army experience gain": ("experience_gain_army_factor", False),
    "Supply consumption": ("supply_consumption_factor", True),
    "Factory output": ("industrial_capacity_factory", False),
    "Production efficiency retention": ("line_change_production_efficiency_factor", False),
    "Production efficiency growth": ("production_factory_efficiency_gain_factor", False),
    "Maximum production efficiency": ("production_factory_max_efficiency_factor", False),
    "Tax collection efficiency": ("tax_gain_multiplier_modifier", False),
    "Convoy escort efficiency": ("convoy_escort_efficiency", False),
    "Naval personnel cost": ("navy_personnel_cost_multiplier_modifier", True),
    "Naval organisation": ("navy_org_factor", False),
    "Political power gain": ("political_power_factor", False),
    "Training time": ("training_time_army_factor", True),
    "Research speed": ("research_speed_factor", False),
    "Encryption": ("encryption_factor", False),
    "Construction speed": ("production_speed_buildings_factor", False),
    "Stability": ("stability_factor", False),
    "Division defence": ("army_defence_factor", False),
    "Education cost": ("education_cost_multiplier_modifier", True),
    "War support": ("war_support_factor", False),
    "Consumer goods factor": ("consumer_goods_factor", True),
}

# Explicit source-checked locations. Each grant still rechecks current ownership,
# control, native capacity and, for the port, actual province control at ratification.
BUILDINGS = {
    ("germany_sustain", "GER"): (41, "arms_factory", 1, None),
    ("canada", "CAN"): (763, "industrial_complex", 1, None),
    ("bahrain", "BHR"): (624, "naval_base", 1, 11181),
    ("israel", "ISR"): (204, "arms_factory", 1, None),
    ("mexico", "MEX"): (830, "industrial_complex", 1, None),
    ("canada_retool", "USA"): (777, "industrial_complex", 1, None),
    ("canada_retool", "CAN"): (763, "industrial_complex", 1, None),
}
PARENTS = {
    "atlantic_research": ("germany_forward", "germany_sustain"),
    "canada_retool": ("canada",),
    "pacific_maintenance": ("japan",),
}
EARLY_FOLLOWUP_IDS = {"USA_X_israel", "USA_X_canada", "USA_X_mexico"}
PICTURES = {
    "germany_forward": "NATO_member", "germany_sustain": "NATO_member",
    "britain": "NATO_member", "japan": "department_of_defense",
    "south_vietnam": "department_of_defense", "bahrain": "trade",
    "israel": "department_of_defense", "soviet_exchange": "research_bonus",
    "atlantic_research": "research_bonus", "pacific_maintenance": "department_of_defense",
}
FOCUS_ICONS = {
    "germany_forward": "blr_nato_cooperation", "germany_sustain": "blr_nato_cooperation",
    "britain": "naval_doctrine", "japan": "blr_nato_cooperation",
    "south_vietnam": "examine_foreign_small_arms", "soviet_exchange": "diplomatic_treaty",
    "bahrain": "naval_dockyard", "israel": "examine_foreign_small_arms",
    "rogers": "diplomatic_treaty", "pacific_maintenance": "naval_upgrade",
}


def number(value) -> str:
    d = Decimal(str(value))
    return format(d.quantize(Decimal("0.00001")), "f").rstrip("0").rstrip(".") if d else "0"


def flag(s: str, kind: str) -> str:
    return f"{P}_{s}_{kind}"


def idea(s: str, tag: str) -> str:
    return f"{P}_{s}_{tag.lower()}"


def family(s: str) -> str:
    return "germany" if s.startswith("germany_") else s


def receipt(s: str, tag: str) -> str:
    return flag(family(s), f"grant_{tag.lower()}_received")


def block(name: str, rows: list[str]) -> str:
    return name + " = {\n" + "\n".join("\t" + row.replace("\n", "\n\t") for row in rows if row) + "\n}"


def scoped(tag: str, body: str) -> str:
    return f"{tag} = {{\n{body}\n}}"


def load_nodes() -> list[dict]:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    lookup = {n["id"].removeprefix("USA_X_"): n for n in source["nodes"] if n.get("offer")}
    assert set(lookup) == set(ORDER), "Approved agreement catalogue changed; review its terms explicitly."
    result = []
    for i, s in enumerate(ORDER):
        n = dict(lookup[s], suffix=s, index=i)
        n["partners"] = [tag for tag in n["offer"] if tag != "USA"]
        n["duration"] = int(re.match(r"\d+", n["lifetime"])[0]) if re.match(r"\d+", n["lifetime"]) else 0
        n["terms"] = {tag: parse_terms(s, tag, t) for tag, t in n["offer"].items()}
        result.append(n)
    return result


def parse_terms(s: str, tag: str, terms: dict) -> dict:
    out = dict(spirit=terms["spirit"], modifiers={}, setup=Decimal(0), income=Decimal(0), expense=Decimal(0), grants=[])
    for row in terms["effects"]:
        if row.startswith("Treasury:"):
            out["setup"] += Decimal(re.search(r"([+-])\$([\d.]+)", row)[1] + re.search(r"([+-])\$([\d.]+)", row)[2])
        elif row.startswith("Weekly"):
            m = re.search(r"([+-])\$([\d.]+)", row)
            out["income" if m[1] == "+" else "expense"] += Decimal(m[2])
        elif row in ("Naval experience: +20", "Army experience: +15", "Army experience: +20", "Political power: +25"):
            key = {"Naval": "navy_experience", "Army": "army_experience", "Political": "add_political_power"}[row.split()[0]]
            out["grants"].append(f"{key} = {row.rsplit('+', 1)[1]}")
        elif "doctrine cost reduction" in row:
            cat = "land_doctrine" if "land doctrine" in row else "naval_doctrine"
            out["grants"].append(f"add_doctrine_cost_reduction = {{ name = {P}_{s}_{tag}_doctrine cost_reduction = 0.5 uses = 1 category = {cat} }}")
        elif "industry research bonus" in row:
            out["grants"].append(f"add_tech_bonus = {{ name = {P}_{s}_{tag}_research bonus = 0.5 uses = 1 category = CAT_industry }}")
        elif "shared building slot" in row:
            assert (s, tag) in BUILDINGS, (s, tag, row)
            state, building, levels, province = BUILDINGS[(s, tag)]
            province_arg = f" province = {province}" if province else ""
            out["grants"].append(scoped(str(state), f"add_extra_state_shared_building_slots = {levels}\nadd_building_construction = {{ type = {building} level = {levels}{province_arg} instant_build = yes }}"))
        else:
            label, amount = row.split(": ", 1)
            native, _ = MODIFIERS[label]
            assert re.fullmatch(r"[+-][\d.]+%", amount), row
            out["modifiers"][native] = Decimal(amount[:-1]) / 100
    return out


def money(amount: Decimal) -> str:
    return f"set_temp_variable = {{ treasury_change = {number(amount)} }}\nmodify_treasury_effect = yes"


def pair_clear(tag: str) -> str:
    def sanctions(counterpart):
        return " ".join(f"is_in_array = {{ array = imp_{kind}_sanc_{direction}_us value = {counterpart} }}" for kind in ("dip", "fin", "eco", "mil") for direction in ("on", "by"))
    return "\n".join([
        f"country_exists = {tag}", f"NOT = {{ has_war_with = {tag} }}", f"NOT = {{ is_embargoing = {tag} }}",
        f"NOT = {{ OR = {{ {sanctions(tag)} }} }}",
        scoped(tag, f"NOT = {{ has_war_with = USA }}\nNOT = {{ is_embargoing = USA }}\nNOT = {{ OR = {{ {sanctions('USA')} }} }}"),
    ])


def early_followup(n: dict) -> dict:
    """Read the user revision only for the three real advanced focus IDs.

    The private early-cooperation adapter reuses suffixes but has different IDs.
    Applying its own parent requirement there would make the founding contracts
    recursively depend on themselves.
    """
    if P != "COLDWAR_USA_agreements" or n["id"] not in EARLY_FOLLOWUP_IDS:
        return {}
    path = ROOT / "tools/usa_1970_expansion/early_cooperation/focus_specs.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    assert document["project"] == "IMPERIA COLD WAR"
    row = document["followups"][n["id"]]
    assert row["runtime_guard"] == f"COLDWAR_USA_early_active_{n['suffix']} = yes"
    assert set(row["parent_ideas"]) == set(n["terms"])
    return copy.deepcopy(row)


def requirements(n: dict) -> list[str]:
    s = n["suffix"]
    out = [f"{P}_pair_clear_{tag.lower()} = yes" for tag in n["partners"]]
    if s in ("germany_forward", "germany_sustain", "britain"):
        out.append("has_idea = NATO_member")
        out += [scoped(t, "has_idea = NATO_member") for t in n["partners"]]
    if s in PARENTS:
        options = [f"{P}_active_{parent} = yes" for parent in PARENTS[s]]
        out.append("OR = { " + " ".join(options) + " }" if len(options) > 1 else options[0])
    early = early_followup(n)
    if early:
        out.append(early["runtime_guard"])
    if s.startswith("germany_"):
        other = "germany_sustain" if s == "germany_forward" else "germany_forward"
        out += [f"NOT = {{ has_country_flag = {flag(other, 'signed')} }}", f"NOT = {{ has_country_flag = {flag(other, 'offer_open')} }}"]
    if s == "bahrain":
        out += ["NOT = { has_country_flag = COLDWAR_USA_bahrain_base_accepted }",
                "NOT = { has_country_flag = COLDWAR_USA_bahrain_base_pending }"]
    # The Saudi offer itself is the explicitly negotiated early commission.
    # No unilateral early exception or arbitrary date barrier is introduced.
    return out


def public_availability(n: dict) -> str:
    """Expose gameplay requirements while retaining the whole authoritative guard.

    Internal scenario/tag routing and signature bookkeeping remain hidden. Named
    membership/parent spirits use the native requirements, not substitute labels.
    """
    s = n["suffix"]
    rows = [f"hidden_trigger = {{ {P}_can_offer_{s} = yes }}"]
    for tag in n["partners"]:
        rows.append(f"custom_trigger_tooltip = {{ tooltip = {P}_relations_{tag.lower()}_tt {P}_pair_clear_{tag.lower()} = yes }}")
    if s in ("germany_forward", "germany_sustain", "britain"):
        rows.append("has_idea = NATO_member")
        rows.extend(scoped(t,"has_idea = NATO_member") for t in n["partners"])
    if s in PARENTS:
        parent_rows = []
        for parent in PARENTS[s]:
            tag = "GER" if s == "atlantic_research" else ("CAN" if s == "canada_retool" else "JAP")
            parent_rows.append(f"AND = {{ has_idea = {idea(parent,'USA')} {scoped(tag,'has_idea = '+idea(parent,tag))} }}")
        rows.append("OR = { " + " ".join(parent_rows) + " }" if len(parent_rows)>1 else parent_rows[0])
    early = early_followup(n)
    if early:
        rows.append(early["public_guard"])
    signatures = [f"NOT = {{ has_country_flag = {flag(s,'signed')} }}"]
    signatures += [scoped(t, f"NOT = {{ has_country_flag = {flag(s,'signed')} }}") for t in n["partners"]]
    rows.append(f"custom_trigger_tooltip = {{ tooltip = {P}_not_ratified_tt {' '.join(signatures)} }}")
    rows.append(f"custom_trigger_tooltip = {{ tooltip = {P}_no_pending_tt NOT = {{ has_country_flag = {flag(s,'offer_open')} }} }}")
    rows.append(f"custom_trigger_tooltip = {{ tooltip = {P}_consultation_interval_tt NOT = {{ has_country_flag = {flag(s,'cooldown')} }} }}")
    if s.startswith("germany_"):
        other = "germany_sustain" if s == "germany_forward" else "germany_forward"
        rows.append(f"custom_trigger_tooltip = {{ tooltip = {P}_bonn_terms_tt NOT = {{ has_country_flag = {flag(other,'signed')} }} NOT = {{ has_country_flag = {flag(other,'offer_open')} }} }}")
    if s == "bahrain":
        rows.append(f"custom_trigger_tooltip = {{ tooltip = {P}_bahrain_sovereignty_tt NOT = {{ has_country_flag = COLDWAR_USA_bahrain_base_accepted }} NOT = {{ has_country_flag = COLDWAR_USA_bahrain_base_pending }} }}")
    return "\n".join(rows)


def assets_available(n: dict, tag: str) -> str:
    s = n["suffix"]
    if (s, tag) not in BUILDINGS:
        return ""
    state, building, quantity, province = BUILDINGS[(s, tag)]
    rows = [f"owns_state = {state}", f"controls_state = {state}"]
    if province:
        rows += [f"controls_province = {province}"]
    # Conservative native capacity check is separate from the promised extra slot.
    rows.append(scoped(str(state), capacity_trigger(building,quantity,province)))
    return f"OR = {{ has_country_flag = {receipt(s, tag)} {scoped(tag, chr(10).join(rows))} }}"


def funds_available(n: dict) -> list[str]:
    s = n["suffix"]
    rows = []
    for tag, term in n["terms"].items():
        if term["setup"] < 0:
            rows.append(scoped(tag, "NOT = { has_country_flag = MD_skip_treasury_cost }\n"
                               f"check_variable = {{ var = treasury value = {number(-term['setup'])} compare = greater_than_or_equals }}"))
    return [f"OR = {{ has_country_flag = {flag(s, 'setup_paid')} AND = {{ {' '.join(rows)} }} }}"] if rows else []


def preview_body(n: dict, *, renewal=False) -> str:
    s = n["suffix"]
    rows = [f"custom_effect_tooltip = {P}_if_accept_tt"]
    for tag, t in n["terms"].items():
        unit = []
        if n["duration"]:
            unit.append(f"add_timed_idea = {{ idea = {idea(s,tag)} days = {n['duration']} }}")
        else:
            unit.append(f"add_ideas = {idea(s,tag)}")
        for key, value in t["modifiers"].items():
            unit.append(f"add_to_variable = {{ {P}_preview_{key} = {number(value)} tooltip = {P}_mod_{key}_tt }}")
        if t["setup"]:
            setup = f"add_to_variable = {{ {P}_preview_treasury = {number(t['setup'])} tooltip = {P}_treasury_tt }}"
            # Full initial focus terms remain visible regardless of eligibility.
            # Reopening controls accurately omit a previously paid setup cost.
            if renewal:
                unit.append(f"if = {{ limit = {{ USA = {{ NOT = {{ has_country_flag = {flag(s,'setup_paid')} }} }} }} {setup} }}")
            else:
                unit.append(setup)
        for kind in ("income", "expense"):
            if t[kind]:
                value = t[kind] if kind == "income" else -t[kind]
                unit.append(f"add_to_variable = {{ {P}_preview_weekly = {number(value)} tooltip = {P}_weekly_{kind}_tt }}")
        if t["grants"]:
            grant = "\n".join(t["grants"])
            if renewal:
                unit.append(f"if = {{ limit = {{ USA = {{ NOT = {{ has_country_flag = {receipt(s,tag)} }} }} }} {grant} }}")
            else:
                unit.append(grant)
        rows.append(scoped(tag, "\n".join(unit)))
    return "\n".join(rows)


def emit_triggers(nodes: list[dict]) -> str:
    rows = [f"# IMPERIA COLD WAR — USA agreement transaction and lifecycle triggers."]
    partners = sorted({t for n in nodes for t in n["partners"]})
    rows += [block(f"{P}_pair_clear_{tag.lower()}", pair_clear(tag).splitlines()) for tag in partners]
    for n in nodes:
        s = n["suffix"]
        ready = ["country_exists = USA", "IMP_is_1970_scenario = yes"] + requirements(n)
        rows.append(block(f"{P}_ready_{s}", ready))
        rows.append(block(f"{P}_can_offer_{s}", ["tag = USA", f"{P}_ready_{s} = yes",
             f"NOT = {{ has_country_flag = {flag(s,'signed')} }}", f"NOT = {{ has_country_flag = {flag(s,'offer_open')} }}",
             f"NOT = {{ has_country_flag = {flag(s,'cooldown')} }}",
             *[scoped(t, f"NOT = {{ has_country_flag = {flag(s,'signed')} }}") for t in n["partners"]]]))
        transaction = [f"{P}_ready_{s} = yes", f"has_country_flag = {flag(s,'offer_open')}",
                       f"NOT = {{ has_country_flag = {flag(s,'signed')} }}", *funds_available(n)]
        transaction += [assets_available(n, tag) for tag in n["terms"] if assets_available(n, tag)]
        rows.append(block(f"{P}_transaction_valid_{s}", transaction))
        for tag in n["partners"]:
            rows.append(block(f"{P}_accept_valid_{s}_{tag.lower()}", [f"tag = {tag}",
                f"has_country_flag = {flag(s,'offer_pending')}",
                scoped("USA", f"{P}_transaction_valid_{s} = yes\nNOT = {{ has_country_flag = {flag(s,'consent_'+tag.lower())} }}")]))
        active = [f"has_country_flag = {flag(s,'signed')}", f"{P}_ready_{s} = yes", f"has_idea = {idea(s,'USA')}"]
        if n["duration"]:
            active.append(f"has_country_flag = {flag(s,'term')}")
        active += [scoped(tag, f"has_country_flag = {flag(s,'signed')}\nhas_idea = {idea(s,tag)}") for tag in n["partners"]]
        rows.append(block(f"{P}_active_{s}", active))
    return "\n\n".join(rows) + "\n"


def emit_effects(nodes: list[dict]) -> str:
    rows = ["# IMPERIA COLD WAR — USA recipient-approved agreement lifecycle effects."]
    for n in nodes:
        s = n["suffix"]
        rows.append(block(f"{P}_preview_{s}", [scoped("effect_tooltip", preview_body(n))]))
        rows.append(block(f"{P}_renewal_preview_{s}", [scoped("effect_tooltip", preview_body(n, renewal=True))]))
        rows.append(block(f"{P}_complete_{s}", [f"{P}_preview_{s} = yes", scoped("hidden_effect",
            f"if = {{ limit = {{ {P}_can_offer_{s} = yes }} set_country_flag = {flag(s,'unlocked')} set_country_flag = {flag(s,'authorised')} {P}_send_{s} = yes }}")]))
        send = [f"set_country_flag = {{ flag = {flag(s,'offer_open')} value = 1 days = 90 }}", f"set_country_flag = {flag(s,'ever_offered')}"]
        for j, tag in enumerate(n["partners"]):
            send += [f"clr_country_flag = {flag(s,'consent_'+tag.lower())}", scoped(tag,
                f"set_country_flag = {{ flag = {flag(s,'offer_pending')} value = 1 days = 90 }}\nset_country_flag = {flag(s,'ever_offered')}\ncountry_event = {{ id = {NAMESPACE}.{100+n['index']*10+j} }}")]
        rows.append(block(f"{P}_send_{s}", [f"if = {{ limit = {{ tag = USA {P}_can_offer_{s} = yes has_country_flag = {flag(s,'authorised')} }}\n" + "\n".join(send) + "\n}"]))
        # Legacy access counter only: material legacy helpers are deliberately not called.
        first_accept = []
        if s not in PARENTS:
            # Early founding cooperation and its advanced industrial programme
            # represent the same bilateral partner for the legacy F10 gate.
            registered = f"COLDWAR_USA_early_{s}_legacy_registered" if early_followup(n) else flag(family(s),"legacy_registered")
            first_accept.append(f"if = {{ limit = {{ NOT = {{ has_country_flag = {registered} }} }} set_country_flag = {registered} USA_1970_register_theater_acceptance = yes }}")
        rows.append(block(f"{P}_on_first_accept_{s}", first_accept))
        ratify = []
        setup = [scoped(tag, money(t["setup"])) for tag, t in n["terms"].items() if t["setup"]]
        ratify.append(f"if = {{ limit = {{ NOT = {{ has_country_flag = {flag(s,'setup_paid')} }} }}\n" + "\n".join(setup) + f"\nset_country_flag = {flag(s,'setup_paid')}\n}}")
        for tag, t in n["terms"].items():
            if t["grants"]:
                ratify.append(f"if = {{ limit = {{ NOT = {{ has_country_flag = {receipt(s,tag)} }} }}\n{scoped(tag, chr(10).join(t['grants']))}\nset_country_flag = {receipt(s,tag)}\n}}")
            # Receipts persist even if this variant has no one-time asset, so a
            # German variant switch cannot award a second family package.
            else:
                ratify.append(f"set_country_flag = {receipt(s,tag)}")
        ratify += [f"set_country_flag = {flag(s,'signed')}", f"clr_country_flag = {flag(s,'offer_open')}"]
        if n["duration"]:
            ratify.append(f"set_country_flag = {{ flag = {flag(s,'term')} value = 1 days = {n['duration']} }}")
        for tag in n["partners"]:
            ratify += [scoped(tag, f"set_country_flag = {flag(s,'signed')}\nclr_country_flag = {flag(s,'offer_pending')}")]
        ratify += [f"{P}_on_first_accept_{s} = yes", f"{P}_reconcile_all = yes", f"country_event = {{ id = {NAMESPACE}.{500+n['index']} }}"]
        consent = " ".join(f"has_country_flag = {flag(s,'consent_'+t.lower())}" for t in n["partners"])
        rows.append(block(f"{P}_ratify_{s}", [f"if = {{ limit = {{ tag = USA {P}_transaction_valid_{s} = yes {consent} }}\n" + "\n".join(ratify) + "\n}"]))
        for tag in n["partners"]:
            rows.append(block(f"{P}_accept_{s}_{tag.lower()}", [f"if = {{ limit = {{ {P}_accept_valid_{s}_{tag.lower()} = yes }}\n" +
                scoped("USA", f"set_country_flag = {flag(s,'consent_'+tag.lower())}\n{P}_ratify_{s} = yes") + "\n}"]))
        refusal = [scoped("USA", f"clr_country_flag = {flag(s,'offer_open')}\nset_country_flag = {{ flag = {flag(s,'cooldown')} value = 1 days = 90 }}\ncountry_event = {{ id = {NAMESPACE}.{600+n['index']} }}")]
        refusal += [scoped(tag, f"clr_country_flag = {flag(s,'offer_pending')}") for tag in n["partners"]]
        refusal += [scoped("USA", "\n".join(f"clr_country_flag = {flag(s,'consent_'+tag.lower())}" for tag in n["partners"]))]
        allowed = " ".join(f"tag = {tag}" for tag in n["partners"])
        rows.append(block(f"{P}_refuse_{s}", [f"if = {{ limit = {{ OR = {{ {allowed} }} has_country_flag = {flag(s,'offer_pending')} USA = {{ has_country_flag = {flag(s,'offer_open')} }} }}\n" + "\n".join(refusal) + "\n}"]))
        ending = []
        for tag in n["terms"]:
            lines = [f"remove_ideas = {idea(s,tag)}", f"clr_country_flag = {flag(s,'signed')}", f"clr_country_flag = {flag(s,'offer_pending')}"]
            if tag == "USA":
                lines += [f"clr_country_flag = {flag(s,'offer_open')}", f"clr_country_flag = {flag(s,'authorised')}", f"clr_country_flag = {flag(s,'term')}", f"set_country_flag = {{ flag = {flag(s,'cooldown')} value = 1 days = 90 }}"]
                if s == "britain":
                    lines[-1] = f"set_country_flag = {{ flag = {flag(s,'cooldown')} value = 1 days = 365 }}"
            ending.append(f"if = {{ limit = {{ country_exists = {tag} }} {scoped(tag, chr(10).join(lines))} }}")
        rows.append(block(f"{P}_terminate_{s}", [f"if = {{ limit = {{ OR = {{ tag = USA {allowed} }} has_country_flag = {flag(s,'signed')} }}\n" + "\n".join(ending) + "\n}"]))
    reconcile = ["if = { limit = { tag = USA IMP_is_1970_scenario = yes }"]
    # Parents appear before dependants in ORDER, so their spirit state is current.
    for n in nodes:
        s = n["suffix"]
        if n["duration"]:
            reconcile.append(f"if = {{ limit = {{ has_country_flag = {flag(s,'signed')} NOT = {{ has_country_flag = {flag(s,'term')} }} }} {P}_terminate_{s} = yes }}")
        signed = [f"has_country_flag = {flag(s,'signed')}", f"{P}_ready_{s} = yes"]
        signed += [scoped(tag, f"has_country_flag = {flag(s,'signed')}") for tag in n["partners"]]
        if n["duration"]:
            signed += [f"has_country_flag = {flag(s,'term')}"]
        add = []
        remove = []
        for tag in n["terms"]:
            add.append(scoped(tag, f"if = {{ limit = {{ NOT = {{ has_idea = {idea(s,tag)} }} }} add_ideas = {idea(s,tag)} }}"))
            remove.append(f"if = {{ limit = {{ country_exists = {tag} }} {scoped(tag, f'remove_ideas = {idea(s,tag)}')} }}")
        reconcile.append("if = { limit = { " + " ".join(signed) + " }\n" + "\n".join(add) + "\n}\nelse = {\n" + "\n".join(remove) + "\n}")
        # Expired pending offers lose all partial consents without signing.
        cleanup = [f"clr_country_flag = {flag(s,'consent_'+tag.lower())}" for tag in n["partners"]]
        cleanup += [f"if = {{ limit = {{ country_exists = {tag} }} {scoped(tag, f'clr_country_flag = {flag(s,"offer_pending")}')} }}" for tag in n["partners"]]
        reconcile.append(f"if = {{ limit = {{ NOT = {{ has_country_flag = {flag(s,'offer_open')} }} }}\n" + "\n".join(cleanup) + "\n}")
    reconcile.append("}")
    rows.append(block(f"{P}_reconcile_all", reconcile))
    # Pure current-country aggregation: no reconciliation, events, fees or money refresh.
    streams = [f"set_variable = {{ {P}_weekly_income = 0 }}", f"set_variable = {{ {P}_weekly_expense = 0 }}", "if = { limit = { IMP_is_1970_scenario = yes country_exists = USA }"]
    for n in nodes:
        for tag, t in n["terms"].items():
            for kind in ("income", "expense"):
                if t[kind]:
                    streams.append(f"if = {{ limit = {{ tag = {tag} USA = {{ {P}_active_{n['suffix']} = yes }} }} add_to_variable = {{ {P}_weekly_{kind} = {number(t[kind])} }} }}")
    streams.append("}")
    rows.append(block(f"{P}_calculate_weekly_streams", streams))
    init = [f"set_variable = {{ {P}_weekly_income = 0 }}", f"set_variable = {{ {P}_weekly_expense = 0 }}", f"if = {{ limit = {{ country_exists = USA }} USA = {{ {P}_reconcile_all = yes }} }}"]
    rows.append(block(f"{P}_initialize", init))
    return "\n\n".join(rows) + "\n"


def emit_ideas(nodes: list[dict]) -> str:
    ideas = []
    for n in nodes:
        for tag, t in n["terms"].items():
            absent = " ".join(f"NOT = {{ country_exists = {c} }}" for c in n["terms"])
            mods = " ".join(f"{k} = {number(v)}" for k,v in t["modifiers"].items())
            ideas.append(block(idea(n["suffix"],tag), [f"picture = {PICTURES.get(n['suffix'],'trade')}", "allowed = { always = no }", "allowed_civil_war = { always = no }", f"cancel = {{ OR = {{ NOT = {{ tag = {tag} }} {absent} }} }}", f"modifier = {{ {mods} }}"]))
    return "# IMPERIA COLD WAR — USA bilateral agreement national spirits.\n" + block("ideas", [block("country", ideas)]) + "\n"


def emit_events(nodes: list[dict]) -> str:
    out = [f"# IMPERIA COLD WAR — USA diplomatic proposals and ratification notices.\nadd_namespace = {NAMESPACE}"]
    for n in nodes:
        s = n["suffix"]
        for j, tag in enumerate(n["partners"]):
            out.append(block("country_event", [f"id = {NAMESPACE}.{100+n['index']*10+j}", f"title = {P}_{s}_title", f"desc = {P}_{s}_offer_desc", "picture = GFX_political_deal", "is_triggered_only = yes",
                f"trigger = {{ tag = {tag} has_country_flag = {flag(s,'offer_pending')} USA = {{ has_country_flag = {flag(s,'offer_open')} }} }}",
                block("option", [f"name = {P}_accept", f"trigger = {{ {P}_accept_valid_{s}_{tag.lower()} = yes }}", f"{P}_renewal_preview_{s} = yes", f"hidden_effect = {{ {P}_accept_{s}_{tag.lower()} = yes }}", "ai_chance = { base = 70 }"]),
                block("option", [f"name = {P}_decline", f"hidden_effect = {{ {P}_refuse_{s} = yes }}", "ai_chance = { base = 30 }"]),
                block("option", [f"name = {P}_review", "ai_chance = { base = 0 }"])]))
        for base, kind in ((500,"ratified"),(600,"declined")):
            out.append(block("country_event", [f"id = {NAMESPACE}.{base+n['index']}", f"title = {P}_{s}_title", f"desc = {P}_{kind}_desc", "picture = GFX_political_deal", "is_triggered_only = yes", "trigger = { tag = USA }", block("option", [f"name = {P}_acknowledge"])]))
    return "\n\n".join(out) + "\n"


def emit_decisions(nodes: list[dict]) -> tuple[str,str]:
    tags = sorted({tag for n in nodes for tag in n["terms"]})
    category = "# IMPERIA COLD WAR — USA bilateral agreement decision category.\n" + block(STEM, ["icon = generic_diplomacy", "priority = 205", "allowed = { OR = { " + " ".join(f"tag = {t}" for t in tags) + " } }", "visible = { IMP_is_1970_scenario = yes }"]) + "\n"
    decisions = []
    for n in nodes:
        s = n["suffix"]
        for tag in n["partners"]:
            decisions.append(block(f"{P}_accept_{s}_{tag.lower()}", ["icon = generic_diplomacy", f"visible = {{ tag = {tag} has_country_flag = {flag(s,'offer_pending')} USA = {{ has_country_flag = {flag(s,'offer_open')} NOT = {{ has_country_flag = {flag(s,'consent_'+tag.lower())} }} }} }}", f"available = {{ {P}_accept_valid_{s}_{tag.lower()} = yes }}", "cost = 0", "days_remove = 1", block("complete_effect", [f"{P}_renewal_preview_{s} = yes", f"hidden_effect = {{ {P}_accept_{s}_{tag.lower()} = yes }}"]), "ai_will_do = { base = 4 }"]))
            decisions.append(block(f"{P}_refuse_{s}_{tag.lower()}", ["icon = generic_diplomacy", f"visible = {{ tag = {tag} has_country_flag = {flag(s,'offer_pending')} USA = {{ has_country_flag = {flag(s,'offer_open')} }} }}", "cost = 0", "days_remove = 1", f"complete_effect = {{ {P}_refuse_{s} = yes }}", "ai_will_do = { base = 1 }"]))
            decisions.append(block(f"{P}_reopen_{s}_{tag.lower()}", ["icon = generic_diplomacy", f"visible = {{ tag = {tag} has_country_flag = {flag(s,'ever_offered')} NOT = {{ has_country_flag = {flag(s,'signed')} }} NOT = {{ has_country_flag = {flag(s,'offer_pending')} }} }}", f"available = {{ country_exists = USA USA = {{ {P}_can_offer_{s} = yes has_country_flag = {flag(s,'authorised')} }} }}", "cost = 0", "days_remove = 1", f"complete_effect = {{ hidden_effect = {{ if = {{ limit = {{ tag = {tag} country_exists = USA }} USA = {{ {P}_send_{s} = yes }} }} }} }}", "ai_will_do = { base = 0 }"]))
        decisions.append(block(f"{P}_renew_{s}", ["icon = generic_diplomacy", f"visible = {{ tag = USA has_country_flag = {flag(s,'unlocked')} NOT = {{ has_country_flag = {flag(s,'signed')} }} NOT = {{ has_country_flag = {flag(s,'offer_open')} }} }}", f"available = {{ {P}_can_offer_{s} = yes }}", "cost = 0", "days_remove = 1", block("complete_effect", [f"{P}_renewal_preview_{s} = yes", f"hidden_effect = {{ if = {{ limit = {{ tag = USA {P}_can_offer_{s} = yes }} set_country_flag = {flag(s,'authorised')} {P}_send_{s} = yes }} }}"]), "ai_will_do = { base = 0 }"]))
        allowed = " ".join(f"tag = {tag}" for tag in n["terms"])
        decisions.append(block(f"{P}_terminate_{s}", ["icon = generic_diplomacy", f"visible = {{ OR = {{ {allowed} }} has_country_flag = {flag(s,'signed')} }}", "cost = 0", "days_remove = 1", f"complete_effect = {{ {P}_terminate_{s} = yes }}", "ai_will_do = { base = 0 }"]))
    return category, "# IMPERIA COLD WAR — Recipient consent and individual agreement renewal/termination.\n" + block(STEM, decisions) + "\n"


def emit_localisation(nodes: list[dict]) -> str:
    caption_path = HERE.parent / "focus_titles.json"
    captions = json.loads(caption_path.read_text(encoding="utf-8"))["titles"] if caption_path.exists() else {}
    loc = {
        STEM: "American Bilateral Agreements",
        P+"_if_accept_tt": "If they accept:",
        P+"_treasury_tt": "Treasury: $RIGHT|+=2$ billion",
        P+"_weekly_income_tt": "Weekly agreement income: $RIGHT|+=2$ billion/week",
        P+"_weekly_expense_tt": "Weekly agreement expenditure: $RIGHT|+=2$ billion/week",
        P+"_accept": "Ratify the proposed terms.", P+"_decline": "Decline the proposed terms.",
        P+"_review": "Continue consultations in diplomatic decisions.", P+"_acknowledge": "Acknowledged.",
        P+"_ratified_desc": "The participating governments have ratified the agreement. Its institutions and financial terms now take effect.",
        P+"_declined_desc": "A participating government has declined the proposed terms. Further consultations remain possible.",
        P+"_not_ratified_tt": "This agreement has not already been ratified.",
        P+"_no_pending_tt": "No proposal for this agreement is awaiting a response.",
        P+"_consultation_interval_tt": "The required interval between diplomatic consultations has elapsed.",
        P+"_bonn_terms_tt": "No conflicting Bonn agreement has been ratified or proposed.",
        P+"_bahrain_sovereignty_tt": "No Bahraini territorial cession to the United States is in force or awaiting a response.",
    }
    for tag in sorted({t for n in nodes for t in n["partners"]}):
        loc[f"{P}_relations_{tag.lower()}_tt"] = f"At peace with [{tag}.GetNameDef], with no mutual embargo or diplomatic, financial, economic or military sanctions."
    for label, (key, bad) in MODIFIERS.items():
        loc[f"{P}_mod_{key}_tt"] = label + ": $RIGHT|" + ("-=" if bad else "+=") + "%1$"
    for n in nodes:
        s = n["suffix"]
        # Only the small native focus caption is shortened. Agreement, decision,
        # event and spirit names retain their full approved institutional titles.
        loc[n["id"]] = captions.get(n["id"], n["name"])
        loc[n["id"]+"_desc"] = n["description"]
        loc[f"{P}_{s}_title"] = n["name"]
        loc[f"{P}_{s}_offer_desc"] = n["description"] + " The proposal remains open for 90 days."
        for tag, t in n["terms"].items():
            ident = idea(s,tag)
            loc[ident] = t["spirit"]
            lifespan = f"The agreed mandate ends {n['duration']} days after ratification." if n["duration"] else "Either signatory may terminate the standing agreement."
            if s == "rogers":
                lifespan = "The mediation mandate ends 180 days after all three governments ratify it. Talks impose no ceasefire or territorial settlement."
            loc[ident+"_desc"] = n["description"] + " " + lifespan
            for reward in ("research", "doctrine"):
                loc[f"{P}_{s}_{tag}_{reward}"] = n["name"]
        for tag in n["partners"]:
            for action, title in (("accept","Ratify "),("refuse","Decline "),("reopen","Reopen talks: ")):
                ident = f"{P}_{action}_{s}_{tag.lower()}"
                loc[ident] = title + n["name"]
                loc[ident+"_desc"] = n["description"] + (" The terms require the approval of every participating government." if action == "accept" else "")
        for action, title in (("renew","Propose again: "),("terminate","Terminate ")):
            ident = f"{P}_{action}_{s}"
            loc[ident] = title + n["name"]
            loc[ident+"_desc"] = n["description"]
    assert not any("\u2013" in v or "\u2014" in v for v in loc.values()), "Unsupported dash in player text."
    return "l_english:\n# IMPERIA COLD WAR — USA agreement English localisation.\n" + "\n".join(f" {k}:0 {json.dumps(v,ensure_ascii=False)}" for k,v in loc.items()) + "\n"


def focus_specs(nodes: list[dict]) -> dict:
    return {
        "project": "IMPERIA COLD WAR", "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "hooks": {"initialize": P+"_initialize", "reconcile": P+"_reconcile_all", "streams": P+"_calculate_weekly_streams", "income_variable": P+"_weekly_income", "expense_variable": P+"_weekly_expense", "reconcile_scope": "USA", "streams_scope": "current country; pure and idempotent", "recommended_reconcile_cadence": "daily, and after relevant diplomacy/government changes"},
        "focuses": {n["id"]: {"available": public_availability(n), "completion_reward": f"{P}_complete_{n['suffix']} = yes", "completion_preview": f"{P}_preview_{n['suffix']} = yes", "helper": f"{P}_complete_{n['suffix']}", "icon": FOCUS_ICONS.get(n["suffix"], "diplomacy"), "on_first_accept": f"{P}_on_first_accept_{n['suffix']}", "ratify": f"{P}_ratify_{n['suffix']}", "accept_helpers": {t: f"{P}_accept_{n['suffix']}_{t.lower()}" for t in n["partners"]}, "ideas": {t: idea(n["suffix"],t) for t in n["terms"]}, "duration_days": n["duration"], "buildings": {t: BUILDINGS[(n["suffix"],t)] for t in n["terms"] if (n["suffix"],t) in BUILDINGS}, **early_followup(n)} for n in nodes},
        "legacy_consolidation": "Parent owns old generic material-offer dispatch removal; this module calls only USA_1970_register_theater_acceptance once per base family, never its material-registration wrappers.",
        "native_anchors": {"retention": "common/technologies/industry.txt:339 line_change_production_efficiency_factor", "money_costs": "common/scripted_effects/00_money_system.txt:3207-3212,3401", "NATO": "common/ideas/Factions.txt:5 NATO_member", "industry_research": "common/technology_tags/00_technology.txt CAT_industry", "idea_art": "interface/MD_ideas.gfx trade, NATO_member, department_of_defense, research_bonus; actual ideas textures, not focus aliases", "event_donor": "217x163 native political_deal.dds, eventwindow.gui full bottom window inspected"},
    }


def validate_outputs(files: dict[str,str], specs: dict) -> dict:
    # Reuse only the pure parser definitions, not the country's executing validator.
    ns = {"re": re}
    parser_path = ROOT / "tools/israel_1970/validate_content.py"
    module = ast.parse(parser_path.read_text(encoding="utf-8"))
    definitions = [n for n in module.body if isinstance(n, ast.FunctionDef) and n.name in {"tokens","parse","first","values","walk"}]
    exec(compile(ast.Module(body=definitions,type_ignores=[]),str(parser_path),"exec"),ns)
    parsed = {p: ns["parse"](s) for p,s in files.items() if p.endswith(".txt")}
    effects = parsed[f"common/scripted_effects/{STEM}.txt"]
    for name, _, body in effects:
        if name.startswith(P+"_preview_") or name.startswith(P+"_renewal_preview_"):
            assert [k for k,_,_ in body] == ["effect_tooltip"], ("Executing preview",name)
        for key,_,val in ns["walk"](body):
            if key == "set_country_flag" and isinstance(val,list):
                assert ns["first"](val,"value") == "1", ("Structured flags must specify their native value",name,val)
    assert len(specs["focuses"]) == 16
    goals = (ROOT/"interface/goals.gfx").read_text(encoding="utf-8-sig")
    for focus in specs["focuses"].values():
        assert f'name = "{focus["icon"]}"' in goals, ("Missing focus sprite",focus["icon"])
        available = ns["parse"](focus["available"])
        assert available[0][0] == "hidden_trigger" and len(available[0][2]) == 1
        for key,_,value in available[1:]:
            assert key in {"custom_trigger_tooltip","has_idea","OR","AND","GER","CAN","ENG","JAP","ISR","MEX"}, ("Visible internal condition",key)
    art = (ROOT/"interface/MD_ideas.gfx").read_text(encoding="utf-8-sig")
    for name in set(PICTURES.values()) | {"trade"}:
        match=re.search(r'name\s*=\s*"GFX_idea_'+re.escape(name)+r'"\s+texturefile\s*=\s*"([^"]+)"',art)
        assert match and match[1].startswith("gfx/interface/ideas/") and (ROOT/match[1]).exists(), ("Invalid spirit artwork",name)
    for p, source in files.items():
        assert not source.startswith("\ufeff")
        assert source.startswith("l_english:\n# IMPERIA COLD WAR") if p.endswith(".yml") else source.startswith("# IMPERIA COLD WAR")
        for value in re.findall(r"(?:treasury_change|weekly_(?:income|expense)) = (-?\d+\.\d+)",source):
            assert len(value.split(".")[1]) <= 5, (p,value)
    # The stream function must have no mutation of gameplay receipts, money or UI.
    stream = next(body for name,_,body in effects if name == P+"_calculate_weekly_streams")
    forbidden = {"modify_treasury_effect","set_country_flag","country_event","add_ideas","ingame_update_setup",P+"_reconcile_all"}
    assert not any(k in forbidden for k,_,_ in ns["walk"](stream))
    defined = {k for tree in parsed.values() for k,_,_ in tree}
    for path, tree in parsed.items():
        for key,_,val in ns["walk"](tree):
            if key.startswith(P+"_") and val == "yes":
                assert key in defined, ("Unresolved custom effect/trigger",path,key)
    model_checks = exercise_model(parsed,ns,nodes=load_nodes())
    return {"project":"IMPERIA COLD WAR","status":"Source and generated-AST model checks passed; native engine and network checks not performed","agreements":16,"parsed_files":len(parsed),"preview_functions_nonexecuting":32,"model_checks":model_checks,"checks":["Strict parser","File-start markers","Numeric precision","Pure weekly accumulator","Preview execution boundary","Custom helper closure","Approved offer count"]}


def exercise_model(parsed: dict, parser: dict, nodes: list[dict]) -> list[str]:
    """Interpret the emitted AST for transaction/lifecycle checks.

    Native finance, construction, research and country identity have explicit small
    models here. These checks do not represent engine scope/UI/network execution.
    """
    first, walk = parser["first"], parser["walk"]
    functions = {k:v for k,_,v in parsed[f"common/scripted_effects/{STEM}.txt"]}
    triggers = {k:v for k,_,v in parsed[f"common/scripted_triggers/{STEM}.txt"]}
    # Read the actual external provider. Parent requirements are never replaced
    # with a model-only true predicate or a completed-focus approximation.
    early_stem = "COLDWAR_USA_1970_early_cooperation"
    for folder, target in (("scripted_triggers", triggers), ("scripted_effects", functions)):
        path = ROOT / f"common/{folder}/{early_stem}.txt"
        external = {k:v for k,_,v in parser["parse"](path.read_text(encoding="utf-8"))}
        assert not set(external) & set(target), ("Duplicate early/advanced provider", folder)
        target.update(external)
    catalogue = {n["suffix"]:n for n in nodes}

    class Model:
        def __init__(self):
            self.day = 0
            self.events = []
            self.countries = {t:dict(tag=t,vars={"treasury":Decimal(1000)},flags={},ideas={"NATO_member"},wars=set(),embargo=set(),arrays={},grants=[]) for n in nodes for t in n["terms"]}
            if P == "COLDWAR_USA_agreements":
                # Baseline fixture represents separately consented, signed early
                # parents with both actual spirits. Tests remove each condition.
                for suffix, tag in (("israel", "ISR"), ("canada", "CAN"), ("mexico", "MEX")):
                    for signatory in ("USA", tag):
                        self.countries[signatory]["flags"][f"COLDWAR_USA_early_{suffix}_signed"] = None
                        self.countries[signatory]["ideas"].add(f"COLDWAR_USA_early_{suffix}_{signatory.lower()}")
            self.states = {}
            for (s,t),(state,kind,_,province) in BUILDINGS.items():
                self.states.setdefault(str(state),dict(owner=t,controller=t,slots=8,levels={"industrial_complex":1,"arms_factory":1,"naval_base":5},province=province))

        def tick(self, days):
            self.day += days
            for c in self.countries.values():
                c["flags"] = {k:v for k,v in c["flags"].items() if v is None or v > self.day}

        def target(self, name):
            return self.countries.get(name) or self.states.get(name)

        def num(self, value, scope):
            try:
                return Decimal(value)
            except Exception:
                return scope["vars"].get(value,Decimal(0))

        def condition(self, conditions, scope):
            for key,op,val in conditions:
                if key == "OR": ok = any(self.condition([x],scope) for x in val)
                elif key == "AND": ok = self.condition(val,scope)
                elif key == "NOT": ok = not self.condition(val,scope)
                elif key == "hidden_trigger": ok = self.condition(val,scope)
                elif key == "custom_trigger_tooltip": ok = self.condition([x for x in val if x[0]!="tooltip"],scope)
                elif key in triggers: ok = self.condition(triggers[key],scope) == (val == "yes")
                elif key == "IMP_is_1970_scenario": ok = val == "yes"
                elif key == "country_exists": ok = val in self.countries
                elif key == "tag": ok = scope.get("tag") == val
                elif key == "has_country_flag": ok = val in scope["flags"]
                elif key == "has_idea": ok = val in scope["ideas"]
                elif key == "has_war_with": ok = val in scope["wars"]
                elif key == "is_embargoing": ok = val in scope["embargo"]
                elif key == "is_in_array": ok = first(val,"value") in scope["arrays"].get(first(val,"array"),set())
                elif key == "check_variable":
                    assert first(val,"compare") == "greater_than_or_equals"
                    ok = self.num(first(val,"var"),scope) >= self.num(first(val,"value"),scope)
                elif key == "owns_state": ok = self.states[val]["owner"] == scope["tag"]
                elif key == "controls_state": ok = self.states[val]["controller"] == scope["tag"]
                elif key == "controls_province": ok = any(st["province"] == int(val) and st["controller"] == scope["tag"] for st in self.states.values())
                elif key == "free_building_slots":
                    kind=first(val,"building");definition=building_definitions()[kind]
                    if not definition['shares_slots']:
                        assert first(val,'include_locked') is None, 'include_locked is only native for shared-slot buildings'
                    cap=int(definition['province_max'] or definition['state_max'])
                    ok = scope["levels"][kind] < cap and (not definition['shares_slots'] or scope["slots"]>0)
                elif self.target(key) is not None: ok = self.condition(val,self.target(key))
                elif re.fullmatch(r"[A-Z]{3}",key): ok = False
                else: raise AssertionError(("Unmodeled trigger",key,op,val))
                if not ok: return False
            return True

        def execute(self, statements, scope):
            branch = False
            for key,_,val in statements:
                if key == "if":
                    branch = self.condition(first(val,"limit",[]),scope)
                    if branch:self.execute([x for x in val if x[0]!="limit"],scope)
                elif key == "else":
                    if not branch:self.execute(val,scope)
                    branch=True
                elif key in ("effect_tooltip","custom_effect_tooltip"): pass
                elif key == "hidden_effect":self.execute(val,scope)
                elif key in functions:self.execute(functions[key],scope)
                elif self.target(key) is not None:self.execute(val,self.target(key))
                elif key == "set_country_flag":
                    ident=first(val,"flag") if isinstance(val,list) else val
                    days=first(val,"days") if isinstance(val,list) else None
                    if isinstance(val,list):
                        assert first(val,"value") == "1", "Model refuses to assume a native default for a structured flag"
                    scope["flags"][ident]=self.day+int(days) if days else None
                elif key == "clr_country_flag":scope["flags"].pop(val,None)
                elif key == "add_ideas":scope["ideas"].add(val)
                elif key == "remove_ideas":scope["ideas"].discard(val)
                elif key in ("set_variable","set_temp_variable","add_to_variable"):
                    ident,_,amount=val[0]
                    scope["vars"][ident]=(scope["vars"].get(ident,Decimal(0)) if key=="add_to_variable" else Decimal(0))+self.num(amount,scope)
                elif key == "modify_treasury_effect":
                    assert "MD_skip_treasury_cost" not in scope["flags"]
                    scope["vars"]["treasury"] += scope["vars"]["treasury_change"]
                elif key == "add_extra_state_shared_building_slots":scope["slots"]+=int(val)
                elif key == "add_building_construction":
                    kind=first(val,"type");amount=int(first(val,"level"))
                    if kind!="naval_base":assert scope["slots"]>=amount;scope["slots"]-=amount
                    scope["levels"][kind]+=amount
                    assert scope["levels"][kind]<={"industrial_complex":50,"arms_factory":35,"naval_base":10}[kind]
                elif key in ("army_experience","navy_experience","add_political_power","add_tech_bonus","add_doctrine_cost_reduction"):
                    scope["grants"].append((key,copy.deepcopy(val)))
                elif key == "country_event":self.events.append((scope["tag"],first(val,"id")))
                elif key == "USA_1970_register_theater_acceptance":
                    scope["vars"]["USA_1970_theater_acceptances"]=scope["vars"].get("USA_1970_theater_acceptances",Decimal(0))+1
                    scope["flags"]["USA_1970_any_theater_accept"]=None
                    if scope["vars"]["USA_1970_theater_acceptances"]>1:scope["flags"]["USA_1970_two_theater_accepts"]=None
                else:raise AssertionError(("Unmodeled effect",key,val))

        def call(self,name,tag="USA"):
            self.execute(functions[name],self.countries[tag])

        def prepare(self,s):
            for parent in PARENTS.get(s,()):
                self.sign(parent)
                break

        def offer(self,s):self.call(P+"_complete_"+s)

        def sign(self,s):
            self.prepare(s)
            self.offer(s)
            for tag in catalogue[s]["partners"]:self.call(f"{P}_accept_{s}_{tag.lower()}",tag)
            assert flag(s,"signed") in self.countries["USA"]["flags"],s

        def streams(self):
            for tag in self.countries:self.call(P+"_calculate_weekly_streams",tag)

    checked=[]
    for n in nodes:
        s=n["suffix"];m=Model();m.prepare(s);available=parser["parse"](public_availability(n))
        def compare_public_guard():
            assert m.condition(available,m.countries["USA"]) == m.condition(triggers[P+"_can_offer_"+s],m.countries["USA"]),("Public availability changed eligibility",s)
        compare_public_guard()
        for kind in ("signed","offer_open","cooldown"):
            m.countries["USA"]["flags"][flag(s,kind)]=None;compare_public_guard();m.countries["USA"]["flags"].pop(flag(s,kind))
        partner=n["partners"][0]
        m.countries["USA"]["wars"].add(partner);compare_public_guard();m.countries["USA"]["wars"].clear()
        m.countries[partner]["embargo"].add("USA");compare_public_guard();m.countries[partner]["embargo"].clear()
        m.countries[partner]["ideas"].clear();compare_public_guard()
    checked.append("All 16 public availability wrappers preserve authoritative eligibility while hiding routing/receipts")
    for suffix, partner in (("israel", "ISR"), ("canada", "CAN"), ("mexico", "MEX")):
        early = "COLDWAR_USA_early_"
        n = catalogue[suffix]
        assert early_followup(n)["runtime_guard"] in requirements(n)
        # Each actual signatory receipt and spirit is necessary. A unilateral
        # spirit or a completed founding focus cannot stand in for the pair.
        for tag in ("USA", partner):
            for field in ("flags", "ideas"):
                m = Model()
                key = early + suffix + ("_signed" if field == "flags" else "_" + tag.lower())
                if field == "flags":m.countries[tag][field].pop(key)
                else:m.countries[tag][field].discard(key)
                before = copy.deepcopy((m.countries, m.states, m.events))
                m.offer(suffix)
                assert (m.countries, m.states, m.events) == before, ("Missing early parent allowed offer", suffix, tag, field)
                assert not m.condition(parser["parse"](public_availability(n)), m.countries["USA"])
        # Parent loss after sending is rechecked in the actual acceptance path.
        m = Model();m.offer(suffix)
        m.countries[partner]["ideas"].discard(early + suffix + "_" + partner.lower())
        before = copy.deepcopy((m.countries, m.states))
        m.call(f"{P}_accept_{suffix}_{partner.lower()}", partner)
        assert (m.countries, m.states) == before, ("Parent race charged or granted", suffix)
        # Restore only the standing parent through its real emitted reconciler.
        m.call(early + "base_reconcile_all")
        m.call(f"{P}_accept_{suffix}_{partner.lower()}", partner)
        assert all(idea(suffix, t) in m.countries[t]["ideas"] for t in n["terms"])
        paid = {t:m.countries[t]["vars"]["treasury"] for t in n["terms"]}
        assets = copy.deepcopy(m.states)
        grants = {t:copy.deepcopy(c["grants"]) for t,c in m.countries.items()}
        # A standing parent's missing paired spirit suspends the child, and
        # the parent's source reconciliation restores it without new receipts.
        m.countries["USA"]["ideas"].discard(early + suffix + "_usa")
        m.call(P + "_reconcile_all");m.streams()
        assert all(idea(suffix, t) not in m.countries[t]["ideas"] for t in n["terms"])
        assert all(m.countries[t]["vars"][P+"_weekly_expense"] == 0 for t in n["terms"])
        m.call(early + "base_reconcile_all");m.call(P + "_reconcile_all");m.streams()
        assert all(idea(suffix, t) in m.countries[t]["ideas"] for t in n["terms"])
        assert assets == m.states and paid == {t:m.countries[t]["vars"]["treasury"] for t in n["terms"]}
        assert grants == {t:c["grants"] for t,c in m.countries.items()}
        # Execute the real recipient cancellation. Routine parent and child
        # reconciliation must not recreate a cancelled agreement or its child.
        m.call(early + "terminate_" + suffix, partner)
        m.call(early + "base_reconcile_all");m.call(P + "_reconcile_all");m.streams()
        assert all(idea(suffix, t) not in m.countries[t]["ideas"] for t in n["terms"])
        assert all(m.countries[t]["vars"][P+"_weekly_expense"] == 0 for t in n["terms"])
        assert not m.condition(triggers[early + "active_" + suffix], m.countries["USA"])
        assert assets == m.states and paid == {t:m.countries[t]["vars"]["treasury"] for t in n["terms"]}
        assert grants == {t:c["grants"] for t,c in m.countries.items()}
        checked.append(suffix + ": real early signed-pair requirement, missing receipt/spirit, acceptance race, suspension/restoration without replay, persistent recipient cancellation")
        m = Model();m.call(early + "on_first_accept_" + suffix)
        assert m.countries["USA"]["vars"]["USA_1970_theater_acceptances"] == 1
        m.sign(suffix);m.call(P + "_on_first_accept_" + suffix)
        assert m.countries["USA"]["vars"]["USA_1970_theater_acceptances"] == 1
        assert "USA_1970_two_theater_accepts" not in m.countries["USA"]["flags"]
        checked.append(suffix + ": early and advanced acceptance share one actual partner counter receipt")
    for n in nodes:
        s=n["suffix"];m=Model();m.prepare(s)
        before=copy.deepcopy((m.countries,m.states,m.events))
        m.call(P+"_preview_"+s)
        assert (m.countries,m.states,m.events)==before,("Preview executed",s)
        m.offer(s)
        assert all(idea(s,t) not in m.countries[t]["ideas"] for t in n["terms"])
        cash={t:m.countries[t]["vars"]["treasury"] for t in n["terms"]}
        for tag in n["partners"]:m.call(f"{P}_accept_{s}_{tag.lower()}",tag)
        assert all(idea(s,t) in m.countries[t]["ideas"] for t in n["terms"]),s
        assert all(m.countries[t]["vars"]["treasury"]==cash[t]+terms["setup"] for t,terms in n["terms"].items()),s
        paid=copy.deepcopy((m.countries,m.states))
        for tag in n["partners"]:m.call(f"{P}_accept_{s}_{tag.lower()}",tag)
        assert (m.countries,m.states)==paid,("Duplicate acceptance",s)
        m.streams();totals={t:(c["vars"][P+"_weekly_income"],c["vars"][P+"_weekly_expense"]) for t,c in m.countries.items()}
        m.streams();assert totals=={t:(c["vars"][P+"_weekly_income"],c["vars"][P+"_weekly_expense"]) for t,c in m.countries.items()}
        target=n["partners"][0];m.countries[target]["embargo"].add("USA");m.call(P+"_reconcile_all")
        assert all(idea(s,t) not in m.countries[t]["ideas"] for t in n["terms"])
        money_after={t:m.countries[t]["vars"]["treasury"] for t in n["terms"]}
        assets_after=copy.deepcopy(m.states);grants_after={t:copy.deepcopy(c["grants"]) for t,c in m.countries.items()}
        m.countries[target]["embargo"].clear();m.call(P+"_reconcile_all")
        assert all(idea(s,t) in m.countries[t]["ideas"] for t in n["terms"])
        assert m.states==assets_after and grants_after=={t:c["grants"] for t,c in m.countries.items()}
        assert money_after=={t:m.countries[t]["vars"]["treasury"] for t in n["terms"]}
        if n["duration"]:
            m.tick(n["duration"]);m.call(P+"_reconcile_all")
            assert all(idea(s,t) not in m.countries[t]["ideas"] for t in n["terms"]),("Expiry",s)
        checked.append(s+": preview, pending, correct payer/recipient, duplicate, streams, suspension/restoration, expiry")
    # Refusal, funds race, country authority and matched budget edges.
    m=Model();m.offer("canada");m.call(P+"_refuse_canada","CAN")
    before=copy.deepcopy(m.countries);m.call(P+"_accept_canada_can","CAN");assert before==m.countries
    assert not m.condition(triggers[P+"_can_offer_canada"],m.countries["USA"])
    m.tick(90);m.call(P+"_send_canada");m.countries["USA"]["vars"]["treasury"]=Decimal(0)
    before=copy.deepcopy(m.countries);m.call(P+"_accept_canada_can","CAN");assert before==m.countries
    m=Model();m.offer("rogers");m.call(P+"_accept_rogers_egy","EGY")
    assert all(idea("rogers",t) not in m.countries[t]["ideas"] for t in ("USA","EGY","ISR"))
    m.countries["EGY"]["wars"].add("ISR");m.countries["ISR"]["embargo"].add("EGY")
    m.call(P+"_accept_rogers_isr","ISR");assert idea("rogers","USA") in m.countries["USA"]["ideas"]
    m=Model();m.sign("germany_forward");m.streams()
    assert m.countries["USA"]["vars"][P+"_weekly_income"]==m.countries["GER"]["vars"][P+"_weekly_expense"]==Decimal("0.02")
    assert m.countries["USA"]["vars"][P+"_weekly_expense"]==Decimal("0.04")
    for tag,other in (("USA","GER"),("GER","USA")):
        for kind in ("dip","fin","eco","mil"):
            for direction in ("on","by"):
                arr=f"imp_{kind}_sanc_{direction}_us";m.countries[tag]["arrays"][arr]={other};m.call(P+"_reconcile_all");m.streams()
                assert all(idea("germany_forward",t) not in m.countries[t]["ideas"] for t in ("USA","GER"))
                assert all(m.countries[t]["vars"][P+"_weekly_expense"]==0 for t in ("USA","GER"))
                m.countries[tag]["arrays"][arr]=set();m.call(P+"_reconcile_all")
    m=Model();m.sign("canada_retool");m.call(P+"_terminate_canada","CAN");m.call(P+"_reconcile_all")
    assert all(idea("canada_retool",t) not in m.countries[t]["ideas"] for t in ("USA","CAN"))
    m=Model();m.sign("bahrain");assets=copy.deepcopy(m.states);grants=copy.deepcopy(m.countries["BHR"]["grants"]);cash=m.countries["USA"]["vars"]["treasury"]
    m.call(P+"_terminate_bahrain","BHR");m.tick(90)
    m.countries["USA"]["flags"][flag("bahrain","authorised")]=None;m.call(P+"_send_bahrain");m.call(P+"_accept_bahrain_bhr","BHR")
    assert assets==m.states and grants==m.countries["BHR"]["grants"] and cash==m.countries["USA"]["vars"]["treasury"]
    m=Model();m.offer("canada");m.tick(90);before=copy.deepcopy((m.countries,m.states));m.call(P+"_accept_canada_can","CAN");assert before==(m.countries,m.states)
    m=Model();m.offer("canada");m.states["763"]["controller"]="MEX";before=copy.deepcopy((m.countries,m.states));m.call(P+"_accept_canada_can","CAN");assert before==(m.countries,m.states)
    m=Model();m.offer("bahrain");m.states["624"]["levels"]["naval_base"]=10;before=copy.deepcopy((m.countries,m.states));m.call(P+"_accept_bahrain_bhr","BHR");assert before==(m.countries,m.states)
    m=Model();m.sign("canada");del m.countries["USA"];m.call(P+"_terminate_canada","CAN");m.streams()
    assert idea("canada","CAN") not in m.countries["CAN"]["ideas"] and flag("canada","signed") not in m.countries["CAN"]["flags"]
    assert m.countries["CAN"]["vars"][P+"_weekly_income"]==0
    m=Model();m.sign("britain");m.countries["USA"]["wars"].add("ENG");m.call(P+"_reconcile_all");m.tick(365);m.call(P+"_reconcile_all");m.countries["USA"]["wars"].clear();m.call(P+"_reconcile_all")
    assert idea("britain","USA") not in m.countries["USA"]["ideas"]
    m=Model();m.sign("germany_forward");grants=copy.deepcopy(m.countries["GER"]["grants"]);states=copy.deepcopy(m.states);m.call(P+"_terminate_germany_forward","GER");m.tick(90);m.sign("germany_sustain")
    assert grants==m.countries["GER"]["grants"] and states==m.states
    assert m.countries["USA"]["vars"]["USA_1970_theater_acceptances"]==1
    checked += ["Refusal and 90-day retry guard", "Funds changed after proposal: no partial transaction", "Rogers first response grants nothing; second response activates all three despite EGY-ISR conflict", "Matched German 0.02 transfer separate from 0.04 gross cost", "All four sanction classes, both mirrored directions and both countries", "Active parent termination suspends child", "Bahrain termination/reoffer does not repeat fee, transfer, slots or construction", "Expired pending offer cannot be accepted", "Lost state control blocks transaction without fees or assets", "Capped port blocks transaction without fees or slots", "Recipient can terminate after USA disappearance", "War suspension does not pause the British calendar", "German variant switch does not repeat family grants or theater counter"]
    return checked


def main() -> None:
    nodes = load_nodes()
    category, decisions = emit_decisions(nodes)
    files = {
        f"common/scripted_effects/{STEM}.txt": emit_effects(nodes),
        f"common/scripted_triggers/{STEM}.txt": emit_triggers(nodes),
        f"common/ideas/{STEM}.txt": emit_ideas(nodes),
        f"events/{STEM}.txt": emit_events(nodes),
        f"common/decisions/categories/{STEM}.txt": category,
        f"common/decisions/{STEM}.txt": decisions,
        f"localisation/english/{STEM}_l_english.yml": emit_localisation(nodes),
    }
    specs = focus_specs(nodes)
    report = validate_outputs(files,specs)
    for path, contents in files.items():
        target = ROOT / path
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(contents,encoding="utf-8-sig" if path.endswith(".yml") else "utf-8",newline="\n")
    HERE.mkdir(parents=True,exist_ok=True)
    (HERE/"focus_specs.json").write_text(json.dumps(specs,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (HERE/"validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    (HERE/"NOTICE.md").write_text("IMPERIA COLD WAR\n\nUSA agreement module: authored for this project from its approved 24 October 2026 proposal. No third-party source code was copied. The local Cuba agreement architecture was consulted. Existing Millennium Dawn national-spirit art and the unchanged GFX_political_deal event photograph are reused by reference. Original artwork authors and individual image licences: unknown; project integration does not establish ownership. Native image source: gfx/event_pictures/generic/elections/political_deal.dds, 217 x 163 RGBA, unchanged outer frame and alpha. Native bottom event window and adjacent option grid were inspected. native_event_donor.png is a decoded review copy, not a live game screenshot or new game asset.\n",encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
