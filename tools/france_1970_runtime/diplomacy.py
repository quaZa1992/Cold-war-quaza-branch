# IMPERIA COLD WAR — France 1970 bilateral diplomacy generator.
"""Emit fixed-partner French offers and durable paired treaty runtime.

The generator is deliberately pure: build_diplomacy(design) returns the files
and English localisation for the root integration to install. It does not edit
the loaded mod. Treaty signatures are permanent; current eligibility controls
paired spirit and weekly-expense activation only.
"""
from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path
import re
from textwrap import indent


MARK = "# IMPERIA COLD WAR — France 1970 bilateral diplomacy.\n"
PAIR_TAGS = {
    "GER", "ENG", "USA", "SOV", "ALG", "PER", "SEN", "ITA", "SER", "AUS", "ARG",
    "NGR", "GAB", "CDI", "CAM", "CHA", "LBA", "IRQ", "SAU", "EGY", "RAJ", "VIE", "MRT", "DJI", "LEB",
}
BUILDING_CAPS = {
    "infrastructure": 6,
    "industrial_complex": 50,
    "offices": 50,
    "arms_factory": 35,
    "agriculture_district": 10,
    "dockyard": 20,
    "air_base": 10,
    "internet_station": 11,
}
BUILDING_LABELS = {
    "infrastructure": "Infrastructure",
    "industrial_complex": "Industrial Complex",
    "offices": "Office",
    "arms_factory": "Arms Factory",
    "agriculture_district": "Agriculture District",
    "dockyard": "Dockyard",
    "air_base": "Air Base",
    "internet_station": "Network Infrastructure",
}


def _pressure_partner_tags() -> set[str]:
    """Read the bounded pressure cleanup tags from their source contract."""
    source = Path(__file__).with_name("pressure_contracts.json")
    payload = json.loads(source.read_text(encoding="utf-8"))
    return {row["tag"] for row in payload["partners"]}


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
CATEGORY_LABELS = {
    "CAT_aircraft": "Aircraft",
    "CAT_electronics": "Electronics",
    "CAT_industry": "Industry",
    "CAT_armor": "Armour",
    "CAT_naval": "Naval",
    "CAT_nuclear_reactors": "Nuclear Reactors",
    "CAT_energy": "Energy",
    "CAT_infrastructure": "Infrastructure",
}
IDENTITY_DATE_PREDICATES = {
    "CID identity": "date < 1972.10.5",
    "FN identity": "date > 1972.10.4",
}
MODIFIER_LABELS = {
    "research_speed_factor": "Research Speed",
    "civilian_factories_productivity": "Civilian Factory Productivity",
    "military_factories_productivity": "Military Factory Productivity",
    "dockyard_productivity": "Dockyard Productivity",
    "army_org_factor": "Army Organisation",
    "army_org_regain": "Army Organisation Regain",
    "army_core_defence_factor": "Army Core Defence",
    "army_personnel_cost_multiplier_modifier": "Army Personnel Cost",
    "navy_personnel_cost_multiplier_modifier": "Navy Personnel Cost",
    "airforce_personnel_cost_multiplier_modifier": "Air Force Personnel Cost",
    "equipment_cost_multiplier_modifier": "Equipment Cost",
    "bureaucracy_cost_multiplier_modifier": "Bureaucracy Cost",
    "social_cost_multiplier_modifier": "Social Programme Cost",
    "education_cost_multiplier_modifier": "Education Cost",
    "production_factory_efficiency_gain_factor": "Factory Efficiency Growth",
    "industrial_capacity_factory": "Factory Capacity",
    "industrial_capacity_dockyard": "Dockyard Capacity",
    "foreign_influence_modifier": "Foreign Influence Growth",
    "foreign_influence_defense_modifier": "Foreign Influence Defence",
    "energy_gain_multiplier": "Energy Generation",
    "energy_use_modifier_civs": "Civilian Factory Energy Use",
    "supply_consumption_factor": "Supply Consumption",
    "naval_accidents_chance": "Naval Accident Chance",
    "air_training_xp_gain_factor": "Air Training Experience Gain",
    "tax_gain_multiplier_modifier": "Tax Revenue",
    "corporate_tax_income_multiplier_modifier": "Corporate Tax Income",
    "agricolture_productivity_modifier": "Agricultural Productivity",
    "training_time_army_factor": "Army Training Time",
    "max_planning": "Maximum Planning",
}


def _block(name: str, body: str, *extra: str) -> str:
    body = "\n".join((body, *extra))
    body = body.strip("\n")
    return f"{name} = {{\n{indent(body, chr(9))}\n}}"


def _decimal(value: object) -> Decimal:
    return Decimal(str(value))


def _script_number(value: object) -> str:
    number = _decimal(value)
    rendered = format(number, ".5f").rstrip("0").rstrip(".")
    return rendered if rendered not in ("", "-0") else "0"


def _money_fraction(effect: dict) -> Decimal:
    fraction = _decimal(effect["gdp_fraction"])
    if len(format(fraction.copy_abs(), "f").split(".")[-1]) > 5:
        raise ValueError(f"GDP share exceeds five fractional digits: {effect}")
    if "runtime_share_literal" in effect:
        literal = _decimal(effect["runtime_share_literal"])
        if literal != fraction:
            raise ValueError(f"runtime_share_literal does not match gdp_fraction: {effect}")
    return fraction


def _weekly_transfer_fraction(effect: dict) -> Decimal:
    if effect.get("base") != "gdp_total" or effect.get("valuation") != "weekly_recalculation" or effect.get("divisor") != 52:
        raise ValueError(f"Invalid matched weekly transfer contract: {effect}")
    fraction = _decimal(effect["gdp_fraction"])
    if fraction <= 0 or len(format(fraction, "f").split(".")[-1]) > 5:
        raise ValueError(f"Weekly transfer GDP share must be positive and at most five decimals: {effect}")
    if _decimal(effect.get("annual_gdp_percent", 0)) != fraction * 100:
        raise ValueError(f"Annual GDP percent differs from its fraction: {effect}")
    if "runtime_share_literal" in effect and _decimal(effect["runtime_share_literal"]) != fraction:
        raise ValueError(f"Weekly transfer runtime literal differs from its GDP fraction: {effect}")
    if effect.get("flow") not in {"expense", "income"}:
        raise ValueError(f"Unknown weekly transfer flow: {effect}")
    return fraction


def _offer_transfers(offer: dict) -> list[dict]:
    """Validate and return the mirrored expense/income records once each."""
    partner = offer["partner"]
    france_rows = [e for e in offer["france"]["effects"] if e["kind"] == "weekly_transfer"]
    recipient_rows = [e for e in offer["recipient"]["effects"] if e["kind"] == "weekly_transfer"]
    if len(france_rows) != len(recipient_rows):
        raise ValueError(f"Unpaired weekly transfers: {offer}")
    used: set[int] = set()
    result = []
    for france_effect in france_rows:
        base = {k: v for k, v in france_effect.items() if k != "flow"}
        matches = [i for i, row in enumerate(recipient_rows) if i not in used and {k: v for k, v in row.items() if k != "flow"} == base]
        if len(matches) != 1:
            raise ValueError(f"Weekly transfer has no exact counterpart: {france_effect}")
        index = matches[0]
        recipient_effect = recipient_rows[index]
        used.add(index)
        if {france_effect.get("flow"), recipient_effect.get("flow")} != {"expense", "income"}:
            raise ValueError(f"Matched transfer needs one expense and one income record: {france_effect}/{recipient_effect}")
        if france_effect.get("payer") not in {"FRA", partner} or france_effect.get("recipient") not in {"FRA", partner} or france_effect.get("payer") == france_effect.get("recipient"):
            raise ValueError(f"Weekly transfer names an invalid signatory pair: {france_effect}")
        for side, tag, effect in (("france", "FRA", france_effect), ("recipient", partner, recipient_effect)):
            _weekly_transfer_fraction(effect)
            owner = effect["payer"] if effect["flow"] == "expense" else effect["recipient"]
            if owner != tag:
                raise ValueError(f"Weekly transfer {effect['flow']} must be recorded on its country side: {side}/{effect}")
        if france_effect["payer"] != recipient_effect["payer"] or france_effect["recipient"] != recipient_effect["recipient"]:
            raise ValueError("Mirrored transfer sides disagree on payer or recipient")
        result.append(france_effect if france_effect["flow"] == "expense" else recipient_effect)
        result.append(france_effect if france_effect["flow"] == "income" else recipient_effect)
    return result


def _offer_relation_effects(offer: dict, kind: str) -> list[dict]:
    """Return one copy of each mirrored treaty relation effect after checking parity."""
    left = [e for e in offer["france"]["effects"] if e["kind"] == kind]
    right = [e for e in offer["recipient"]["effects"] if e["kind"] == kind]
    if left != right:
        raise ValueError(f"Mirrored {kind} effects differ between signatories: {left}/{right}")
    partner = offer["partner"]
    for effect in left:
        if effect.get("lifecycle") != "standing_agreement":
            raise ValueError(f"Unreviewed {kind} lifecycle: {effect}")
        if effect.get("grantor") not in {"FRA", partner} or effect.get("beneficiary") not in {"FRA", partner} or effect["grantor"] == effect["beneficiary"]:
            raise ValueError(f"{kind} effect must connect the named signatories: {effect}")
        if kind == "access" and effect.get("relation") != "military_access":
            raise ValueError(f"Only source-verified military access is supported: {effect}")
        if kind == "resource_rights" and not (
            effect.get("grantor") == "NGR" and effect.get("beneficiary") == "FRA"
            and int(effect.get("state", -1)) == 329 and effect.get("resources") == ["uranium"]
        ):
            raise ValueError(f"Only the reviewed Niger uranium-rights contract is supported: {effect}")
    return left


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def _mod_percent(value: object) -> str:
    amount = _decimal(value) * 100
    sign = "+" if amount >= 0 else "−"
    amount = abs(amount)
    rendered = format(amount, "f").rstrip("0").rstrip(".")
    return sign + (rendered or "0") + "%"


def _locale_key(key: str, part: str) -> str:
    return f"COLDWAR_FRA2_offer_{key}_{part}"


def _family_flags(family: str) -> tuple[str, str]:
    name = _slug(family)
    return (
        f"COLDWAR_FRA2_family_pending_{name}",
        f"COLDWAR_FRA2_family_signed_{name}",
    )


def _proposal_party_trigger(offer: dict, group: dict | None = None) -> str | None:
    """Return the approved current-ruling-party trigger for a party offer."""
    party = offer.get("proposal_party")
    raw = offer.get("proposal_party_trigger")
    if not party:
        if raw:
            raise ValueError(f"Party trigger without proposal_party: {offer}")
        return None
    expected = PARTY_TRIGGERS.get(party)
    if expected is None or raw != expected:
        raise ValueError(f"Unverified party/trigger mapping: {party}/{raw}")
    if group and group.get("trigger") != raw:
        raise ValueError(f"Party trigger differs from focus-group trigger: {party}/{raw}/{group.get('trigger')}")
    return raw


def _activation_checks(offer: dict) -> list[str]:
    checks: list[str] = []
    rights = _offer_relation_effects(offer, "resource_rights")
    for raw in offer.get("activation_conditions", []):
        compact = re.sub(r"\s+", " ", raw).strip()
        idea = re.fullmatch(r"(FRA|[A-Z]{3}) = \{ has_idea = ([A-Za-z0-9_]+) \}", compact)
        subject = re.fullmatch(r"(FRA|[A-Z]{3}) = \{ is_subject = no \}", compact)
        grantor_state = re.fullmatch(r"(FRA|[A-Z]{3}) = \{ (?:is_subject = no )?owns_state = (\d+) controls_state = (\d+) has_full_control_of_state = (\d+) \}", compact)
        known_deposit = re.fullmatch(r"(\d+) = \{ check_variable = \{ imp_uranium_deposit_kt > 0 \} \}", compact)
        if idea:
            tag, idea_id = idea.groups()
            checks.append(f"{tag} = {{ has_idea = {idea_id} }}")
        elif subject and subject.group(1) == offer["partner"]:
            checks.append(f"{subject.group(1)} = {{ is_subject = no }}")
        elif grantor_state:
            tag, first, second, third = grantor_state.groups()
            declared_right = any(effect["grantor"] == tag and str(effect["state"]) == first == second == third for effect in rights)
            declared_asset = tag == offer['partner'] and first == second == third and any(
                effect['kind'] == 'building' and str(effect['state']) == first for effect in offer['recipient']['effects'])
            if not (declared_right or declared_asset):
                raise ValueError(f"Unreviewed state-control activation condition: {raw}")
            checks.append(compact)
        elif known_deposit:
            state = known_deposit.group(1)
            if not any(str(effect["state"]) == state for effect in rights):
                raise ValueError(f"Unreviewed uranium-deposit activation condition: {raw}")
            checks.append(f"{state} = {{ check_variable = {{ imp_uranium_deposit_kt > 0 }} }}")
        else:
            raise ValueError(f"Unreviewed activation condition: {raw}")
    return checks


def _relation_preflight_checks(offer: dict) -> list[str]:
    """Protect foreign access/assets the contract does not own at signature."""
    rows = []
    for effect in _offer_relation_effects(offer, "resource_rights"):
        state = int(effect["state"])
        # The native removal effect revokes by state, not by resource. Keep the
        # transaction out when France already holds any resource right there.
        rows.append(f"NOT = {{ FRA = {{ has_resources_rights = {{ state = {state} }} }} }}")
    return rows


def _node_tech_checks(node: dict, offer: dict) -> list[str]:
    checks: list[str] = []
    seen: set[tuple[str, str]] = set()
    for raw in node.get("conditions", []):
        identity_date = IDENTITY_DATE_PREDICATES.get(raw.strip())
        if identity_date and identity_date not in checks:
            checks.append(identity_date)
        for tag, tech in re.findall(r"(?:(FRA|[A-Z]{3})\s*=\s*\{\s*)?has_tech\s*=\s*([A-Za-z0-9_]+)", raw):
            item = (tag or "FRA", tech)
            if item in seen:
                continue
            seen.add(item)
            if item[0] == "FRA":
                checks.append(f"has_tech = {tech}")
            else:
                checks.append(f"{item[0]} = {{ has_tech = {tech} }}")
    for raw in offer.get("acceptance_conditions", []):
        for tag, tech in re.findall(r"(?:(FRA|[A-Z]{3})\s*=\s*\{\s*)?has_tech\s*=\s*([A-Za-z0-9_]+)", raw):
            item = (tag or "FRA", tech)
            if item in seen:
                continue
            seen.add(item)
            checks.append(f"has_tech = {tech}" if item[0] == "FRA" else f"{item[0]} = {{ has_tech = {tech} }}")
    return checks


def _asset_state_check(tag: str, effect: dict) -> str:
    building = effect["building"]
    amount = int(effect["amount"])
    cap = BUILDING_CAPS.get(building)
    if cap is None:
        raise ValueError(f"No verified physical capacity for offer asset {building}")
    condition = [
        f"owns_state = {effect['state']}",
        f"controls_state = {effect['state']}",
        f"has_full_control_of_state = {effect['state']}",
        f"{effect['state']} = {{ check_variable = {{ var = building_level@{building} value = {cap - amount} compare = less_than_or_equals }} }}",
    ]
    province = effect.get("province")
    if province is not None:
        # HOI4 numeric province selectors are not a valid nested province scope.
        # This generator currently supports only state-level bilateral assets.
        raise ValueError(f"Province asset requires an explicitly reviewed province-control trigger: {effect}")
    return f"{tag} = {{\n{indent(chr(10).join(condition), chr(9))}\n}}"


def _asset_apply(tag: str, effects: list[dict]) -> str:
    chunks: list[str] = []
    for effect in effects:
        if effect["kind"] != "building":
            continue
        if effect["amount"] != effect["slots"] or not effect.get("slots_before_construction") or not effect.get("once"):
            raise ValueError(f"Building transaction missing once-only slot contract: {effect}")
        add = [f"add_extra_state_shared_building_slots = {effect['slots']}"]
        construct = [
            f"type = {effect['building']}",
            f"level = {effect['amount']}",
            "instant_build = yes",
        ]
        if effect.get("province") is not None:
            construct.append(f"province = {{ id = {effect['province']} }}")
        add.append("add_building_construction = {\n" + indent("\n".join(construct), "\t") + "\n}")
        chunks.append(f"{effect['state']} = {{\n{indent(chr(10).join(add), chr(9))}\n}}")
    return f"{tag} = {{\n{indent(chr(10).join(chunks), chr(9))}\n}}" if chunks else ""


def _fee_apply(tag: str, effects: list[dict]) -> str:
    fees = [e for e in effects if e["kind"] == "treasury_gdp"]
    if not fees:
        return ""
    if len(fees) != 1:
        raise ValueError(f"Expected one setup charge per signatory, got {fees}")
    fraction = _money_fraction(fees[0])
    if fraction >= 0:
        raise ValueError(f"Setup payment must be a signed cost: {fees[0]}")
    body = (
        "set_temp_variable = { treasury_change = { value = gdp_total multiply = "
        + _script_number(fraction)
        + " } }\nmodify_treasury_effect = yes"
    )
    return f"{tag} = {{\n{indent(body, chr(9))}\n}}"


def _once_awards(tag: str, key: str, effects: list[dict], suffix: str) -> str:
    rows: list[str] = []
    for index, effect in enumerate(effects):
        if effect["kind"] == "research":
            name = f"COLDWAR_FRA2_{key}_{suffix}_research_{index}"
            rows.append(
                "add_tech_bonus = { name = " + name + " category = " + effect["category"]
                + " bonus = " + _script_number(effect["bonus"])
                + " uses = " + str(effect["uses"]) + " }"
            )
        elif effect["kind"] == "doctrine":
            name = f"COLDWAR_FRA2_{key}_{suffix}_doctrine_{index}"
            rows.append(
                "add_doctrine_cost_reduction = { name = " + name + " category = " + effect["category"]
                + " cost_reduction = " + _script_number(effect["reduction"])
                + " uses = " + str(effect["uses"]) + " }"
            )
        elif effect["kind"] == "experience":
            command = {"army": "army_experience", "navy": "navy_experience", "air": "air_experience"}.get(effect["service"])
            if command is None:
                raise ValueError(f"Unreviewed experience service: {effect}")
            rows.append(f"{command} = {effect['amount']}")
        elif effect["kind"] == "faction_opinion":
            provider = effect.get("provider")
            if provider not in {
                "change_industrial_conglomerates_opinion",
                "change_labour_unions_opinion",
                "change_farmers_opinion",
            }:
                raise ValueError(f"Unreviewed opinion helper: {effect}")
            rows.append(
                f"set_temp_variable = {{ temp_opinion = {_script_number(effect['value'])} }}\n{provider} = yes"
            )
    return f"{tag} = {{\n{indent(chr(10).join(rows), chr(9))}\n}}" if rows else ""


def _idea_definition(idea: str, effects: list[dict]) -> str:
    modifiers = [e for e in effects if e["kind"] == "modifier"]
    body = [
        f"picture = foreign_capital",
        "allowed = { always = no }",
        "allowed_civil_war = { always = yes }",
    ]
    if modifiers:
        lines = [f"{e['key']} = {_script_number(e['value'])}" for e in modifiers]
        body.append("modifier = {\n" + indent("\n".join(lines), "\t") + "\n}")
    return f"{idea} = {{\n{indent(chr(10).join(body), chr(9))}\n}}"


def _quote_vars(key: str, side: str, effects: list[dict]) -> tuple[str, str, str]:
    setup = next(e for e in effects if e["kind"] == "treasury_gdp")
    weekly = next(e for e in effects if e["kind"] == "weekly_gdp_expense")
    setup_fraction = abs(_money_fraction(setup))
    annual_fraction = _money_fraction(weekly)
    if annual_fraction <= 0 or weekly.get("divisor") != 52:
        raise ValueError(f"Invalid weekly GDP stream: {weekly}")
    weekly_var = f"COLDWAR_FRA2_{key}_quote_weekly_{side}"
    body = (
        f"set_temp_variable = {{ {weekly_var} = {{ value = gdp_total multiply = {_script_number(annual_fraction)} divide = 52 }} }}\n"
        # MD's native additional-expense row uses a red numeric money formatter.
        # Display these small weekly flows in millions: |R2 has the same money
        # precision as the old billions |5, without a long decimal or formula.
        f"set_temp_variable = {{ {weekly_var}_millions = {{ value = {weekly_var} multiply = 1000 }} }}\n"
        f"set_temp_variable = {{ treasury_change = {{ value = gdp_total multiply = {_script_number(-setup_fraction)} }} }}\n"
        "modify_treasury_effect = yes"
    )
    return body, weekly_var, format(annual_fraction * 100, "f").rstrip("0").rstrip(".")


def _preview_side(key: str, side: str, tag: str, data: dict) -> tuple[str, dict[str, str]]:
    effects = data["effects"]
    body, weekly_var, _ = _quote_vars(key, side, effects)
    rows = [
        body,
        f"custom_effect_tooltip = {_locale_key(key, side + '_weekly_share')}",
    ]
    transfer_rows, transfer_loc = _preview_transfer_rows(key, side, tag, effects)
    rows.extend(transfer_rows)
    rows.append(f"add_ideas = {data['spirit']}")
    rows.extend(x for x in (_preview_awards(tag, key, effects, side),) if x)
    loc = {
        _locale_key(key, side + "_weekly_share"): (
            f"§YAdditional Expenses§! increases by $$[?{weekly_var}_millions|R2] Million/week\n"
        ),
    }
    loc.update(transfer_loc)
    return f"{tag} = {{\n{indent(chr(10).join(rows), chr(9))}\n}}", loc


def _preview_transfer_rows(key: str, side: str, tag: str, effects: list[dict]) -> tuple[list[str], dict[str, str]]:
    rows = []
    loc = {}
    for index, effect in enumerate(e for e in effects if e["kind"] == "weekly_transfer"):
        fraction = _weekly_transfer_fraction(effect)
        target_tag = effect["payer"] if effect["flow"] == "expense" else effect["recipient"]
        if target_tag != tag:
            raise ValueError(f"Weekly transfer preview is in the wrong signatory scope: {key}/{side}/{effect}")
        var = f"COLDWAR_FRA2_{key}_quote_transfer_{side}_{index}"
        rows.append(
            f"set_temp_variable = {{ {var} = {{ value = {effect['payer']}.gdp_total multiply = {_script_number(fraction)} divide = 52 }} }}\n"
            f"set_temp_variable = {{ {var}_millions = {{ value = {var} multiply = 1000 }} }}\n"
            f"custom_effect_tooltip = {_locale_key(key, side + '_weekly_transfer_' + str(index))}"
        )
        amount_label = "Additional Expenses" if effect["flow"] == "expense" else "Additional Income"
        color = "R2" if effect["flow"] == "expense" else "G2"
        loc[_locale_key(key, side + "_weekly_transfer_" + str(index))] = (
            f"§Y{amount_label}§! changes by $$[?{var}_millions|{color}] Million/week\n"
        )
    return rows, loc


def _preview_awards(tag: str, key: str, effects: list[dict], suffix: str) -> str:
    rows: list[str] = []
    for index, effect in enumerate(effects):
        if effect["kind"] == "building":
            rows.append(_asset_apply(tag, [effect]))
        elif effect["kind"] == "research":
            name = f"COLDWAR_FRA2_{key}_{suffix}_research_{index}"
            rows.append(
                "add_tech_bonus = { name = " + name + " category = " + effect["category"]
                + " bonus = " + _script_number(effect["bonus"]) + " uses = " + str(effect["uses"]) + " }"
            )
        elif effect["kind"] == "doctrine":
            name = f"COLDWAR_FRA2_{key}_{suffix}_doctrine_{index}"
            rows.append(
                "add_doctrine_cost_reduction = { name = " + name + " category = " + effect["category"]
                + " cost_reduction = " + _script_number(effect["reduction"]) + " uses = " + str(effect["uses"]) + " }"
            )
        elif effect["kind"] == "experience":
            command = {"army": "army_experience", "navy": "navy_experience", "air": "air_experience"}[effect["service"]]
            rows.append(f"{command} = {effect['amount']}")
        elif effect["kind"] == "access" and effect["beneficiary"] == tag:
            rows.append(f"{effect['grantor']} = {{ give_military_access = {effect['beneficiary']} }}")
        elif effect["kind"] == "resource_rights" and effect["beneficiary"] == tag:
            resources = " ".join(effect["resources"])
            rows.append(
                f"{effect['grantor']} = {{ give_resource_rights = {{ receiver = {effect['beneficiary']} state = {int(effect['state'])} resources = {{ {resources} }} }} }}"
            )
        elif effect["kind"] == "faction_opinion":
            provider = effect.get("provider")
            if provider not in {
                "change_industrial_conglomerates_opinion",
                "change_labour_unions_opinion",
                "change_farmers_opinion",
            }:
                raise ValueError(f"Unreviewed opinion helper: {effect}")
            rows.append(f"set_temp_variable = {{ temp_opinion = {_script_number(effect['value'])} }}\n{provider} = yes")
    return "\n".join(rows)


def _pair_trigger(tag: str) -> str:
    sanc = []
    for family in ("dip", "fin", "eco", "mil"):
        sanc.extend(
            f"is_in_array = {{ array = imp_{family}_sanc_{direction}_us value = {tag} }}"
            for direction in ("on", "by")
        )
    other_sanc = []
    for family in ("dip", "fin", "eco", "mil"):
        other_sanc.extend(
            f"is_in_array = {{ array = imp_{family}_sanc_{direction}_us value = FRA }}"
            for direction in ("on", "by")
        )
    body = [
        "country_exists = FRA",
        f"country_exists = {tag}",
        f"NOT = {{ has_war_with = {tag} }}",
        f"NOT = {{ is_embargoing = {tag} }}",
        "NOT = { OR = { " + " ".join(sanc) + " } }",
        f"{tag} = {{",
        "\tNOT = { has_war_with = FRA }",
        "\tNOT = { is_embargoing = FRA }",
        "\tNOT = { OR = { " + " ".join(other_sanc) + " } }",
        "}",
    ]
    return _block(f"COLDWAR_FRA2_pair_{tag}_clear", "\n".join(body))


def _acceptance_conditions(
    key: str, node: dict, offer: dict, partner: str, group: dict | None
) -> str:
    family_pending, family_signed = _family_flags(offer["family"])
    terms = [
        f"COLDWAR_FRA2_pair_{partner}_clear = yes",
        f"NOT = {{ has_country_flag = {family_signed} }}",
        f"has_country_flag = {family_pending}",
        f"NOT = {{ has_country_flag = COLDWAR_FRA2_signed_{key} }}",
        "check_variable = { gdp_total > 0 }",
        f"{partner} = {{ check_variable = {{ gdp_total > 0 }} }}",
    ]
    if group and group.get("trigger"):
        terms.append(group["trigger"] + " = yes")
    party_trigger = _proposal_party_trigger(offer, group)
    if party_trigger and (not group or party_trigger != group.get("trigger")):
        terms.append(party_trigger + " = yes")
    terms.extend(_node_tech_checks(node, offer))
    terms.extend(_activation_checks(offer))
    terms.extend(_relation_preflight_checks(offer))
    for side, tag in (("france", "FRA"), ("recipient", partner)):
        assets = [e for e in offer[side]["effects"] if e["kind"] == "building"]
        seen_assets: set[tuple[int, str, object]] = set()
        for asset in assets:
            asset_key = (int(asset["state"]), asset["building"], asset.get("province"))
            if asset_key in seen_assets:
                raise ValueError(f"Repeated asset in one state needs aggregated capacity preflight: {key}/{side}/{asset_key}")
            seen_assets.add(asset_key)
            terms.append(_asset_state_check(tag, asset))
    return _block(f"COLDWAR_FRA2_offer_can_accept_{key}", "\n".join(terms))


def _send_conditions(key: str, node: dict, offer: dict, partner: str, group: dict | None) -> str:
    family_pending, family_signed = _family_flags(offer["family"])
    terms = [
        f"country_exists = {partner}",
        f"COLDWAR_FRA2_pair_{partner}_clear = yes",
        f"NOT = {{ has_country_flag = {family_signed} }}",
        f"NOT = {{ has_country_flag = {family_pending} }}",
        f"NOT = {{ has_country_flag = COLDWAR_FRA2_offer_cooldown_{key} }}",
        "check_variable = { gdp_total > 0 }",
        f"{partner} = {{ check_variable = {{ gdp_total > 0 }} }}",
    ]
    if group and group.get("trigger"):
        terms.append(group["trigger"] + " = yes")
    party_trigger = _proposal_party_trigger(offer, group)
    if party_trigger and (not group or party_trigger != group.get("trigger")):
        terms.append(party_trigger + " = yes")
    terms.extend(_node_tech_checks(node, offer))
    terms.extend(_activation_checks(offer))
    terms.extend(_relation_preflight_checks(offer))
    return _block(f"COLDWAR_FRA2_offer_can_send_{key}", "\n".join(terms))


def _signed_active_trigger(key: str, offer: dict, partner: str) -> str:
    terms = [
        f"has_country_flag = COLDWAR_FRA2_signed_{key}",
        f"{partner} = {{ has_country_flag = COLDWAR_FRA2_signed_{key} }}",
        f"COLDWAR_FRA2_pair_{partner}_clear = yes",
    ]
    terms.extend(_activation_checks(offer))
    return _block(f"COLDWAR_FRA2_offer_active_{key}", "\n".join(terms))


def _scope_previews(key: str, offer: dict) -> tuple[str, dict[str, str]]:
    blocks = [
        "custom_effect_tooltip = TT_IF_THEY_ACCEPT",
        "custom_effect_tooltip = COLDWAR_FRA2_france_accept_heading",
    ]
    loc = {}
    for side, tag in (("france", "FRA"), ("recipient", offer["partner"])):
        if side == "recipient":
            blocks.append(f"custom_effect_tooltip = COLDWAR_FRA2_{key}_recipient_heading")
        block, strings = _preview_side(key, side, tag, offer[side])
        blocks.append(block)
        loc.update(strings)
    loc["COLDWAR_FRA2_france_accept_heading"] = "[FRA.GetName]"
    loc[f"COLDWAR_FRA2_{key}_recipient_heading"] = f"[{offer['partner']}.GetName]"
    return "\n".join(blocks), loc


def _offer_effects(key: str, node: dict, offer: dict, group: dict | None) -> tuple[str, str, dict[str, str]]:
    partner = offer["partner"]
    party_trigger = _proposal_party_trigger(offer, group)
    family_pending, family_signed = _family_flags(offer["family"])
    preview_scopes, preview_loc = _scope_previews(key, offer)

    open_body = "\n".join(
        [
            f"if = {{",
            f"\tlimit = {{ COLDWAR_FRA2_offer_can_send_{key} = yes }}",
            f"\tset_country_flag = {{ flag = COLDWAR_FRA2_pending_{key} value = 1 days = 90 }}",
            f"\tset_country_flag = {{ flag = {family_pending} value = 1 days = 90 }}",
            f"\tset_country_flag = COLDWAR_FRA2_offer_ever_sent_{key}",
            f"\tset_country_flag = {{ flag = COLDWAR_FRA2_offer_cooldown_{key} value = 1 days = 180 }}",
            f"\t{partner} = {{ set_country_flag = {{ flag = COLDWAR_FRA2_pending_{key} value = 1 days = 90 }} }}",
            f"}}",
        ]
    )
    open_effect = _block(f"COLDWAR_FRA2_offer_{key}", open_body)

    accept_body = [
        "if = {",
        "\tlimit = {",
        f"\t\thas_country_flag = COLDWAR_FRA2_pending_{key}",
        f"\t\tFRA = {{ has_country_flag = COLDWAR_FRA2_pending_{key} COLDWAR_FRA2_offer_can_accept_{key} = yes }}",
        "\t}",
        f"\tset_country_flag = COLDWAR_FRA2_signed_{key}",
        f"\tFRA = {{ set_country_flag = COLDWAR_FRA2_signed_{key} set_country_flag = {family_signed} clr_country_flag = {family_pending} clr_country_flag = COLDWAR_FRA2_offer_cooldown_{key} clr_country_flag = COLDWAR_FRA2_pending_{key} }}",
        f"\tclr_country_flag = COLDWAR_FRA2_pending_{key}",
        f"\tclr_country_flag = COLDWAR_FRA2_offer_cooldown_{key}",
        f"\t{_fee_apply('FRA', offer['france']['effects'])}",
        f"\t{_fee_apply(partner, offer['recipient']['effects'])}",
        f"\t{_asset_apply('FRA', offer['france']['effects'])}",
        f"\t{_asset_apply(partner, offer['recipient']['effects'])}",
        f"\t{_once_awards('FRA', key, offer['france']['effects'], 'france')}",
        f"\t{_once_awards(partner, key, offer['recipient']['effects'], 'recipient')}",
        "\tFRA = { COLDWAR_FRA2_sync_treaties = yes }",
        "}",
    ]
    # No part of this helper runs when the paired pending flags or any final
    # acceptance condition have changed. Receipts precede all one-time rewards.
    accept_effect = _block(f"COLDWAR_FRA2_accept_{key}", "\n".join(x for x in accept_body if x.strip()))

    preview = _block(f"COLDWAR_FRA2_offer_preview_{key}", preview_scopes)

    decline_body = "\n".join(
        [
            f"if = {{ limit = {{ has_country_flag = COLDWAR_FRA2_pending_{key} FRA = {{ has_country_flag = COLDWAR_FRA2_pending_{key} }} }}",
            f"\tclr_country_flag = COLDWAR_FRA2_pending_{key}",
            f"\tset_country_flag = {{ flag = COLDWAR_FRA2_offer_cooldown_{key} value = 1 days = 180 }}",
            f"\tFRA = {{ clr_country_flag = COLDWAR_FRA2_pending_{key} clr_country_flag = {family_pending} set_country_flag = {{ flag = COLDWAR_FRA2_offer_cooldown_{key} value = 1 days = 180 }} }}",
            "}",
        ]
    )
    decline_effect = _block(f"COLDWAR_FRA2_decline_{key}", decline_body)

    reissue_body = "\n".join(
        [
            f"if = {{ limit = {{ has_completed_focus = COLDWAR_FRA2_{key} {' '.join([party_trigger + ' = yes'] if party_trigger else [])} NOT = {{ has_country_flag = COLDWAR_FRA2_offer_cooldown_{key} }} NOT = {{ has_country_flag = {family_signed} }} NOT = {{ has_country_flag = {family_pending} }} NOT = {{ has_country_flag = COLDWAR_FRA2_pending_{key} }} }}",
            f"\tCOLDWAR_FRA2_offer_{key} = yes",
            "}",
        ]
    )
    reissue_effect = _block(f"COLDWAR_FRA2_reissue_{key}", reissue_body)

    category = _family_flags(offer["family"])[0]
    loc = dict(preview_loc)
    loc.update(
        {
            f"COLDWAR_FRA2_accept_{key}": f"Accept: {node['title']}",
            f"COLDWAR_FRA2_accept_{key}_desc": "Accept the fixed-partner programme. The complete prospective terms and both countries' costs are shown below.",
            f"COLDWAR_FRA2_decline_{key}": f"Decline: {node['title']}",
            f"COLDWAR_FRA2_decline_{key}_desc": "Declining starts no programme and charges neither country.",
            f"COLDWAR_FRA2_reissue_{key}": f"Renew the proposal to {offer['partner_name']}",
            f"COLDWAR_FRA2_reissue_{key}_desc": f"Send a fresh proposal for {node['title']} to {offer['partner_name']}. The terms are unchanged and require the recipient's consent.",
        }
    )
    return "\n\n".join([open_effect, accept_effect, preview, decline_effect, reissue_effect]), "\n".join(
        [
            _send_conditions(key, node, offer, partner, group),
            _acceptance_conditions(key, node, offer, partner, group),
            _signed_active_trigger(key, offer, partner),
        ]
    ), loc


def _decision_category(offers: list[tuple[str, dict]]) -> str:
    pending = "\n".join(
        f"{offer['partner']} = {{ has_country_flag = COLDWAR_FRA2_pending_{key} }}"
        for key, offer in offers
    )
    reissuable = "\n".join(
        _block(
            "AND",
            "\n".join(
                [
                    f"has_completed_focus = COLDWAR_FRA2_{key}",
                    *([_proposal_party_trigger(offer) + " = yes"] if _proposal_party_trigger(offer) else []),
                    f"NOT = {{ has_country_flag = {_family_flags(offer['family'])[1]} }}",
                    f"NOT = {{ has_country_flag = {_family_flags(offer['family'])[0]} }}",
                    f"NOT = {{ has_country_flag = COLDWAR_FRA2_pending_{key} }}",
                    f"NOT = {{ has_country_flag = COLDWAR_FRA2_offer_cooldown_{key} }}",
                ]
            ),
        )
        for key, offer in offers
    )
    body = [
        _block(
            "COLDWAR_FRA2_recipient_agreements_category",
            "allowed = { always = yes }\nicon = GFX_decision_category_generic_foreign_policy\npriority = 145\nvisible = {\n\tOR = {\n"
            + indent(pending, "\t\t")
            + "\n\t}\n}",
        ),
        _block(
            "COLDWAR_FRA2_reissue_category",
            "allowed = { original_tag = FRA }\nicon = GFX_decision_category_generic_foreign_policy\npriority = 145\nvisible = {\n\tOR = {\n"
            + indent(reissuable, "\t\t")
            + "\n\t}\n}",
        ),
    ]
    return MARK + "\n\n".join(body) + "\n"


def _decision_groups(offers: list[tuple[str, dict]]) -> str:
    recipient: list[str] = []
    reissue: list[str] = []
    for key, offer in offers:
        partner = offer["partner"]
        recipient.extend(
            [
                _block(
                    f"COLDWAR_FRA2_accept_{key}",
                    "\n".join(
                        [
                            "icon = europe",
                            f"visible = {{ tag = {partner} has_country_flag = COLDWAR_FRA2_pending_{key} }}",
                            "available = {",
                            f"\ttag = {partner}",
                            f"\thas_country_flag = COLDWAR_FRA2_pending_{key}",
                            f"\tFRA = {{ has_country_flag = COLDWAR_FRA2_pending_{key} COLDWAR_FRA2_offer_can_accept_{key} = yes }}",
                            "}",
                            "cost = 0",
                            "days_remove = 1",
                            "complete_effect = {",
                            f"\teffect_tooltip = {{ COLDWAR_FRA2_offer_preview_{key} = yes }}",
                            f"\tCOLDWAR_FRA2_accept_{key} = yes",
                            "}",
                            "ai_will_do = { factor = 0 }",
                        ]
                    ),
                ),
                _block(
                    f"COLDWAR_FRA2_decline_{key}",
                    "\n".join(
                        [
                            "icon = europe",
                            f"visible = {{ tag = {partner} has_country_flag = COLDWAR_FRA2_pending_{key} }}",
                            "available = {",
                            f"\ttag = {partner}",
                            f"\thas_country_flag = COLDWAR_FRA2_pending_{key}",
                            f"\tFRA = {{ has_country_flag = COLDWAR_FRA2_pending_{key} }}",
                            "}",
                            "cost = 0",
                            "days_remove = 1",
                            f"complete_effect = {{ COLDWAR_FRA2_decline_{key} = yes }}",
                            "ai_will_do = { factor = 0 }",
                        ]
                    ),
                ),
            ]
        )
        reissue.extend(
            [
                _block(
                    f"COLDWAR_FRA2_reissue_{key}",
                    "\n".join(
                        [
                            "icon = europe",
                            f"visible = {{ original_tag = FRA has_completed_focus = COLDWAR_FRA2_{key} {' '.join([_proposal_party_trigger(offer) + ' = yes'] if _proposal_party_trigger(offer) else [])} NOT = {{ has_country_flag = {_family_flags(offer['family'])[1]} }} NOT = {{ has_country_flag = {_family_flags(offer['family'])[0]} }} NOT = {{ has_country_flag = COLDWAR_FRA2_pending_{key} }} NOT = {{ has_country_flag = COLDWAR_FRA2_offer_cooldown_{key} }} }}",
                            "available = {",
                            "\toriginal_tag = FRA",
                            f"\thas_completed_focus = COLDWAR_FRA2_{key}",
                            *([f"\t{_proposal_party_trigger(offer)} = yes"] if _proposal_party_trigger(offer) else []),
                            f"\tNOT = {{ has_country_flag = COLDWAR_FRA2_offer_cooldown_{key} }}",
                            f"\tNOT = {{ has_country_flag = {_family_flags(offer['family'])[0]} }}",
                            f"\tNOT = {{ has_country_flag = {_family_flags(offer['family'])[1]} }}",
                            f"\tNOT = {{ has_country_flag = COLDWAR_FRA2_pending_{key} }}",
                            f"\t{offer['partner']} = {{ NOT = {{ has_country_flag = COLDWAR_FRA2_pending_{key} }} }}",
                            f"\tCOLDWAR_FRA2_offer_can_send_{key} = yes",
                            "}",
                            "cost = 0",
                            "days_remove = 1",
                            "complete_effect = {",
                            f"\teffect_tooltip = {{ COLDWAR_FRA2_offer_preview_{key} = yes }}",
                            f"\tCOLDWAR_FRA2_reissue_{key} = yes",
                            "}",
                            "ai_will_do = { factor = 0 }",
                        ]
                    ),
                )
            ]
        )
    return MARK + "\n\n".join(
        [
            _block("COLDWAR_FRA2_recipient_agreements_category", "\n".join(recipient)),
            _block("COLDWAR_FRA2_reissue_category", "\n".join(reissue)),
        ]
    ) + "\n"


def _all_pair_triggers(offers: list[tuple[str, dict]]) -> str:
    tags = sorted({offer["partner"] for _, offer in offers})
    return MARK + "\n\n".join(_pair_trigger(tag) for tag in tags) + "\n"


def _all_runtime_effects(design: dict, offers: list[tuple[str, dict]]) -> tuple[str, str]:
    node_by_key = {n["key"]: n for n in design["nodes"]}
    group_by_id = {g["id"]: g for g in design["groups"]}
    effects: list[str] = []
    triggers: list[str] = []
    ideas: list[str] = []
    for key, offer in offers:
        node = node_by_key[key]
        if key not in node_by_key:
            raise ValueError(f"Offer source focus missing: {key}")
        for side in ("france", "recipient"):
            entries = offer[side]["effects"]
            for effect in entries:
                if effect["kind"] in ("treasury_gdp", "weekly_gdp_expense"):
                    _money_fraction(effect)
                elif effect["kind"] == "weekly_transfer":
                    _weekly_transfer_fraction(effect)
                elif effect["kind"] == "building":
                    if effect["building"] not in BUILDING_CAPS:
                        raise ValueError(f"Missing capacity source for building: {effect}")
                elif effect["kind"] not in {"modifier", "research", "doctrine", "experience", "faction_opinion", "access", "resource_rights"}:
                    raise ValueError(f"Unreviewed offer effect: {effect}")
            ideas.append(_idea_definition(offer[side]["spirit"], entries))
        _offer_transfers(offer)
        _offer_relation_effects(offer, "access")
        _offer_relation_effects(offer, "resource_rights")
        group = group_by_id.get(node["group"])
        open_eff, trig, _ = _offer_effects(key, node, offer, group)
        effects.append(open_eff)
        triggers.append(trig)

    # The country-scope callback is called once from the rebuilt native expense
    # aggregate for every country. It contributes only that signatory's own GDP.
    weekly_rows: list[str] = []
    income_rows: list[str] = []
    transfer_cache_effects: list[str] = []
    for key, offer in offers:
        partner = offer["partner"]
        for side, tag in (("france", "FRA"), ("recipient", partner)):
            weekly = next(e for e in offer[side]["effects"] if e["kind"] == "weekly_gdp_expense")
            fraction = _money_fraction(weekly)
            if fraction <= 0 or weekly.get("divisor") != 52:
                raise ValueError(f"Invalid annual-GDP stream for {key}/{side}")
            var = f"COLDWAR_FRA2_weekly_{key}_{side}"
            body = [
                "set_temp_variable = { " + var + " = 0 }",
                "if = {",
                "\tlimit = {",
                f"\t\ttag = {tag}",
                f"\t\thas_country_flag = COLDWAR_FRA2_signed_{key}",
                f"\t\t{'COLDWAR_FRA2_offer_active_' + key + ' = yes' if tag == 'FRA' else 'FRA = { COLDWAR_FRA2_offer_active_' + key + ' = yes }'}",
                "\t}",
                f"\tset_temp_variable = {{ {var} = {{ value = gdp_total multiply = {_script_number(fraction)} divide = 52 }} }}",
                f"\tadd_to_variable = {{ additional_expenses_rate = {var} }}",
                f"\tadd_to_variable = {{ COLDWAR_FRA2_cooperation_weekly_expenses = {var} }}",
                "}",
            ]
            weekly_rows.append("\n".join(body))
        transfer_rows = _offer_transfers(offer)
        for index, offset in enumerate(range(0, len(transfer_rows), 2)):
            pair = transfer_rows[offset:offset + 2]
            expense_transfer = next(row for row in pair if row["flow"] == "expense")
            income_transfer = next(row for row in pair if row["flow"] == "income")
            var = f"COLDWAR_FRA2_transfer_quote_{key}_{index}"
            cache_flag = f"COLDWAR_FRA2_transfer_quote_fresh_{key}_{index}"
            cache_effect_name = f"COLDWAR_FRA2_cache_transfer_quote_{key}_{index}"
            payer = expense_transfer["payer"]
            payer_tag = "FRA" if payer == "FRA" else payer
            fraction = _weekly_transfer_fraction(expense_transfer)
            cache_effect = _block(cache_effect_name,
                _block("if", _block("limit", f"NOT = {{ has_country_flag = {cache_flag} }}"),
                    f"set_variable = {{ {var} = {{ value = {payer_tag}.gdp_total multiply = {_script_number(fraction)} divide = 52 }} }}",
                    f"set_country_flag = {{ flag = {cache_flag} value = 1 days = 7 }}"))
            if cache_effect not in transfer_cache_effects:
                transfer_cache_effects.append(cache_effect)
            quote_ref = f"FRA.{var}"
            for transfer, row_tag, rate, total in (
                (expense_transfer, expense_transfer["payer"], "additional_expenses_rate", "expenses"),
                (income_transfer, income_transfer["recipient"], "additional_income_rate", "income"),
            ):
                active_check = f"COLDWAR_FRA2_offer_active_{key} = yes" if row_tag == "FRA" else f"FRA = {{ COLDWAR_FRA2_offer_active_{key} = yes }}"
                cache_call = f"{cache_effect_name} = yes" if row_tag == "FRA" else f"FRA = {{ {cache_effect_name} = yes }}"
                freeze_guard = (
                    f"FRA = {{ NOT = {{ has_country_flag = COLDWAR_FRA2_pressure_aid_freeze_{partner} }} }}"
                    if expense_transfer["payer"] == "FRA" else ""
                )
                body = [
                    "if = {",
                    "\tlimit = {",
                    f"\t\ttag = {row_tag}",
                    f"\t\thas_country_flag = COLDWAR_FRA2_signed_{key}",
                    f"\t\t{active_check}",
                    *([f"\t\t{freeze_guard}"] if freeze_guard else []),
                    "\t}",
                    f"\t{cache_call}",
                    f"\tadd_to_variable = {{ {rate} = {quote_ref} }}",
                    f"\tadd_to_variable = {{ COLDWAR_FRA2_cooperation_weekly_{total} = {quote_ref} }}",
                    "}",
                ]
                (weekly_rows if total == "expenses" else income_rows).append("\n".join(body))
    reconcile_rows: list[str] = []
    for key, offer in offers:
        partner = offer["partner"]
        active_relations = []
        inactive_relations = []
        for access in _offer_relation_effects(offer, "access"):
            receipt = f"COLDWAR_FRA2_access_owned_{key}_{access['grantor']}"
            grantor = access["grantor"]
            beneficiary = access["beneficiary"]
            active_relations.append(
                f"if = {{ limit = {{ {beneficiary} = {{ NOT = {{ has_military_access_to = {grantor} }} }} }} "
                f"{grantor} = {{ give_military_access = {beneficiary} set_country_flag = {receipt} }} }}"
            )
            inactive_relations.append(
                f"if = {{ limit = {{ {grantor} = {{ has_country_flag = {receipt} }} }} "
                f"{beneficiary} = {{ if = {{ limit = {{ has_military_access_to = {grantor} }} "
                f"diplomatic_relation = {{ country = {grantor} relation = military_access active = no }} }} }} "
                f"{grantor} = {{ clr_country_flag = {receipt} }} }}"
            )
        for resource in _offer_relation_effects(offer, "resource_rights"):
            state = int(resource["state"])
            resources = " ".join(resource["resources"])
            receipt = f"COLDWAR_FRA2_resource_rights_owned_{key}_{state}"
            right_check = f"has_resources_rights = {{ state = {state} resources = {{ {resources} }} }}"
            active_relations.append(
                f"if = {{ limit = {{ NOT = {{ has_resources_rights = {{ state = {state} }} }} }} "
                f"{resource['grantor']} = {{ give_resource_rights = {{ receiver = {resource['beneficiary']} state = {state} resources = {{ {resources} }} }} }} "
                f"set_country_flag = {receipt} }}"
            )
            inactive_relations.append(
                f"if = {{ limit = {{ has_country_flag = {receipt} {right_check} }} remove_resource_rights = {state} }}"
            )
        if _offer_transfers(offer):
            stream_state = f"COLDWAR_FRA2_transfer_active_{key}"
            quote_flags = " ".join(
                f"clr_country_flag = COLDWAR_FRA2_transfer_quote_fresh_{key}_{index}"
                for index, _ in enumerate(range(0, len(_offer_transfers(offer)), 2))
            )
            add.append(
                f"if = {{ limit = {{ NOT = {{ has_country_flag = {stream_state} }} }} "
                f"set_country_flag = {stream_state} {quote_flags} update_money_dirty_variable = yes "
                f"{partner} = {{ update_money_dirty_variable = yes }} }}"
            )
            remove.append(
                f"if = {{ limit = {{ has_country_flag = {stream_state} }} "
                f"clr_country_flag = {stream_state} update_money_dirty_variable = yes "
                f"{partner} = {{ update_money_dirty_variable = yes }} }}"
            )
        add = [
            f"if = {{ limit = {{ NOT = {{ has_idea = {offer['france']['spirit']} }} }} add_ideas = {offer['france']['spirit']} }}",
            f"{partner} = {{ if = {{ limit = {{ NOT = {{ has_idea = {offer['recipient']['spirit']} }} }} add_ideas = {offer['recipient']['spirit']} }} }}",
            *active_relations,
        ]
        remove = [
            f"if = {{ limit = {{ has_idea = {offer['france']['spirit']} }} remove_ideas = {offer['france']['spirit']} }}",
            f"if = {{ limit = {{ country_exists = {partner} {partner} = {{ has_idea = {offer['recipient']['spirit']} }} }} {partner} = {{ remove_ideas = {offer['recipient']['spirit']} }} }}",
            *inactive_relations,
        ]
        reconcile_rows.append(
            "if = {\n"
            + indent(
                f"limit = {{ has_country_flag = COLDWAR_FRA2_signed_{key} {partner} = {{ has_country_flag = COLDWAR_FRA2_signed_{key} }} COLDWAR_FRA2_offer_active_{key} = yes }}\n"
                + "\n".join(add),
                "\t",
            )
            + "\n}\nelse = {\n"
            + indent("\n".join(remove), "\t")
            + "\n}"
        )
    reconcile_rows.append("set_country_flag = COLDWAR_FRA2_treaties_initialized")
    reconcile_rows.append("COLDWAR_FRA2_pressure_sync_all = yes")
    sync_body = "if = {\n\tlimit = { tag = FRA }\n" + indent("\n".join(reconcile_rows), "\t\t") + "\n}"
    sync = _block("COLDWAR_FRA2_sync_treaties", sync_body)
    initialize = _block("COLDWAR_FRA2_treaties_initialize", "if = { limit = { tag = FRA } COLDWAR_FRA2_sync_treaties = yes }")
    orphan_rows: list[str] = []
    pressure_tags = _pressure_partner_tags()
    for partner in sorted({offer["partner"] for _, offer in offers}):
        partner_spirits = [offer["recipient"]["spirit"] for _, offer in offers if offer["partner"] == partner]
        orphan_cleanup_rows = [*(f"remove_ideas = {spirit}" for spirit in partner_spirits)]
        for key, offer in offers:
            if offer["partner"] != partner:
                continue
            for access in _offer_relation_effects(offer, "access"):
                if access["grantor"] == partner:
                    receipt = f"COLDWAR_FRA2_access_owned_{key}_{partner}"
                    orphan_cleanup_rows.append(f"clr_country_flag = {receipt}")
        if partner in pressure_tags:
            orphan_cleanup_rows.extend((
                f"remove_ideas = COLDWAR_FRA2_pressure_charter_host_{partner}",
                f"clr_country_flag = COLDWAR_FRA2_pressure_access_owned_{partner}",
                f"clr_country_flag = COLDWAR_FRA2_pressure_pending_{partner}",
                "update_money_dirty_variable = yes",
            ))
        orphan_rows.append(_block(
            "if",
            "\n".join((
                _block("limit", f"tag = {partner}\nNOT = {{ country_exists = FRA }}"),
                *orphan_cleanup_rows,
            )),
        ))
    orphan_cleanup = _block("COLDWAR_FRA2_cleanup_orphaned_recipient_ideas", "\n".join(orphan_rows))
    relevant_tags = " ".join(f"tag = {tag}" for tag in ("FRA", *sorted({o["partner"] for _, o in offers})))
    weekly_body = (
        "if = {\n"
        + indent(
            "limit = { OR = { " + relevant_tags + " } }\n"
            "set_variable = { COLDWAR_FRA2_cooperation_weekly_expenses = 0 }\n"
            + "if = { limit = { tag = FRA } COLDWAR_FRA2_add_domestic_weekly_expenses = yes }\n"
            + "\n".join(weekly_rows)
            + "\nCOLDWAR_FRA2_pressure_add_weekly_expenses = yes",
            "\t",
        )
        + "\n\tset_variable = { COLDWAR_FRA2_cooperation_weekly_expenses_millions = { value = COLDWAR_FRA2_cooperation_weekly_expenses multiply = 1000 } }\n}"
    )
    effects.append(
        _block(
            "COLDWAR_FRA2_add_weekly_expenses",
            weekly_body,
        )
    )
    income_body = (
        "if = {\n"
        + indent(
            "limit = { OR = { " + " ".join(f"tag = {tag}" for tag in sorted(
                {"FRA", *(transfer["recipient"] for _, offer in offers for transfer in _offer_transfers(offer))}
            )) + " } }\n"
            + "set_variable = { COLDWAR_FRA2_cooperation_weekly_income = 0 }\n"
            + "\n".join(income_rows)
            + "\nCOLDWAR_FRA2_pressure_add_weekly_income = yes"
            + "\nset_variable = { COLDWAR_FRA2_cooperation_weekly_income_millions = { value = COLDWAR_FRA2_cooperation_weekly_income multiply = 1000 } }",
            "\t",
        )
        + "\n}"
    ) if income_rows else "if = { limit = { always = no } }"
    effects.append(_block("COLDWAR_FRA2_add_weekly_income", income_body))
    effects.extend(transfer_cache_effects)
    effects.extend([sync, initialize, orphan_cleanup])

    # Each agreement side gets exactly one idea provider with its own
    # source-defined modifier set.
    unique_ideas = list(dict.fromkeys(ideas))
    idea_file = MARK + "ideas = {\n\tcountry = {\n" + indent("\n".join(unique_ideas), "\t\t") + "\n\t}\n}\n"
    trigger_file = MARK + "\n\n".join(triggers) + "\n"
    effect_file = MARK + "\n\n".join(effects) + "\n"
    budget_defined_text = MARK + "\n\n".join((
        "defined_text = {\n\tname = COLDWAR_FRA2_cooperation_weekly_income_display\n"
        "\ttext = {\n\t\ttrigger = { check_variable = { COLDWAR_FRA2_cooperation_weekly_income > 0.00001 } }\n"
        "\t\tlocalization_key = COLDWAR_FRA2_cooperation_weekly_income_display_tt\n\t}\n}",
        "defined_text = {\n\tname = COLDWAR_FRA2_cooperation_weekly_expense_display\n"
        "\ttext = {\n\t\ttrigger = { check_variable = { COLDWAR_FRA2_cooperation_weekly_expenses > 0.00001 } }\n"
        "\t\tlocalization_key = COLDWAR_FRA2_cooperation_weekly_expense_display_tt\n\t}\n}",
    )) + "\n"
    return effect_file, trigger_file, idea_file, budget_defined_text


def build_diplomacy(design: dict) -> dict:
    """Return generated runtime files and English localisation for France offers."""
    offers: list[tuple[str, dict]] = []
    for node in design["nodes"]:
        if "offer" in node:
            offers.append((node["key"], node["offer"]))
    node_by_key = {n["key"]: n for n in design["nodes"]}
    added_keys = set(design.get("foreign_policy_revision", {}).get(
        "added_focus_keys", design.get("foreign_policy_added_keys", [])
    ))
    expected_offer_count = 35 + sum(1 for key in added_keys if key in node_by_key and node_by_key[key].get("offer"))
    if len(offers) != expected_offer_count:
        raise ValueError(f"Expected {expected_offer_count} France focus-origin offers from the applied revisions, found {len(offers)}")
    families: dict[str, list[str]] = {}
    for key, offer in offers:
        families.setdefault(offer["family"], []).append(key)
        if offer["partner"] not in PAIR_TAGS:
            raise ValueError(f"Partner tag is outside the bounded France contract set: {offer['partner']}")
        if node_by_key[key].get("foreign_policy_change") != "new" and not all(offer.get(field) for field in ("acceptance_conditions", "acceptance_transaction", "payment_contract", "asset_execution")):
            raise ValueError(f"Offer {key} is missing its accepted transaction contract")
        if not offer.get("partner_name"):
            raise ValueError(f"Offer {key} has no fixed recipient display name")
    node_by_key = {n["key"]: n for n in design["nodes"]}
    group_by_id = {g["id"]: g for g in design["groups"]}
    for key, offer in offers:
        node = node_by_key[key]
        _proposal_party_trigger(offer, group_by_id.get(node["group"]))
    effects, triggers, ideas, budget_defined_text = _all_runtime_effects(design, offers)
    loc: dict[str, str] = {
        "COLDWAR_FRA2_recipient_agreements_category": "Bilateral Programme Proposals",
        "COLDWAR_FRA2_recipient_agreements_category_desc": "Review and answer fixed-partner programme proposals.",
        "COLDWAR_FRA2_reissue_category": "Renew Bilateral Proposals",
        "COLDWAR_FRA2_reissue_category_desc": "Renew proposals to their original named partners after the waiting period.",
        "COLDWAR_FRA2_france_accept_heading": "[FRA.GetName]",
    }
    for key, offer in offers:
        node = node_by_key[key]
        if node["group"] not in group_by_id:
            raise ValueError(f"Offer focus group missing: {node['group']}")
        _, _, strings = _offer_effects(key, node, offer, group_by_id[node["group"]])
        loc.update(strings)
    loc.update({
        "COLDWAR_FRA2_cooperation_weekly_income_display_tt": "$$[?COLDWAR_FRA2_cooperation_weekly_income_millions|G2] Million/week from France's bilateral programmes\\n",
        "COLDWAR_FRA2_cooperation_weekly_expense_display_tt": "$$[?COLDWAR_FRA2_cooperation_weekly_expenses_millions|R2] Million/week for France's bilateral programmes\\n",
    })

    files = {
        "common/scripted_triggers/COLDWAR_FRA2_diplomacy_triggers.txt": _all_pair_triggers(offers) + "\n" + triggers,
        "common/scripted_effects/COLDWAR_FRA2_diplomacy_effects.txt": effects,
        "common/ideas/COLDWAR_FRA2_diplomacy_ideas.txt": ideas,
        "common/decisions/categories/COLDWAR_FRA2_diplomacy_categories.txt": _decision_category(offers),
        "common/decisions/COLDWAR_FRA2_diplomacy_decisions.txt": _decision_groups(offers),
        "common/scripted_localisation/COLDWAR_FRA2_cooperation_budget.txt": budget_defined_text,
    }
    return {"files": files, "loc": loc}
