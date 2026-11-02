# IMPERIA COLD WAR — Cyprus 1970 recipient-approved agreements.
"""Pure generator for Cyprus bilateral agreements."""
from __future__ import annotations

import re
from collections.abc import Mapping

P = "COLDWAR_CYP_R2_"
NS = "COLDWAR_CYP_R2_deal"
EEC = ("GER", "FRA", "ITA", "BEL", "HOL", "LUX")
LABEL = {
    "GRE": "Greece", "SER": "Yugoslavia", "ENG": "United Kingdom",
    "CZE": "Czechoslovakia", "TUR": "Turkey", "GER": "West Germany",
    "FRA": "France", "ITA": "Italy", "BEL": "Belgium",
    "HOL": "The Netherlands", "LUX": "Luxembourg",
}
MODS = {
    "army_org_factor": "Division organization",
    "training_time_factor": "Unit training time",
    "foreign_influence_defense_modifier": "Foreign influence defence",
    "research_speed_factor": "Research speed",
    "education_cost_multiplier_modifier": "Education cost",
    "office_park_income_tax_modifier": "Office sector tax income",
    "bureaucracy_cost_multiplier_modifier": "Bureaucracy cost",
    "army_attack_factor": "Army attack",
    "stability_factor": "Stability",
    "production_speed_industrial_complex_factor": "Civilian factory construction",
}


def _b(key, body, indent=0):
    pad = "\t" * (indent + 1)
    return key + " = {\n" + "\n".join(pad + x if x else "" for x in body.splitlines()) + "\n" + "\t" * indent + "}\n"


def _flag(key, suffix):
    return f"{P}{key}_{suffix}"


def _spirit(key, side):
    suffix = "cyp" if side == "CYP" else side.lower()
    return f"{P}{key}_{suffix}"


def _pct(value):
    return round(float(value) / 100.0, 5)


def _n(value):
    """Format fixed-point script literals without exponent notation."""
    return f"{float(value):.5f}".rstrip("0").rstrip(".") or "0"


def _other_value(side, label):
    for text in side.get("other", []):
        m = re.match(r"\s*" + re.escape(label) + r"\s*([+-]?\d+(?:\.\d+)?)\b", text, re.I)
        if m:
            return float(m.group(1))
    return None


def _income_rate(side):
    for text in side.get("other", []):
        m = re.search(r"Income\s*\+\s*(\d+(?:\.\d+)?)%\s+of Cyprus GDP per week", text, re.I)
        if m:
            return _pct(m.group(1))
    return 0.0


def _modifier_preview(key, values, loc):
    out = []
    for name, value in values.items():
        if name not in MODS:
            raise ValueError(f"Missing preview label for modifier {name!r} in {key!r}")
        lkey = f"{P}deal_mod_{name}_tt"
        loc.setdefault(lkey, MODS[name] + ": $RIGHT|+=%1$")
        out.append(f"add_to_variable = {{ {P}preview_{key}_{name} = {_n(value)} tooltip = {lkey} }}")
    return "\n".join(out)


def _other_effects(side, loc):
    out = []
    xp = _other_value(side, "Army experience")
    pen = _other_value(side, "Officer penetration")
    if xp is not None:
        out.append(f"army_experience = {_n(xp)}")
    if pen is not None:
        loc[f"{P}deal_officer_penetration_tt"] = "Officer penetration: $RIGHT|+=0$"
        out.append(f"add_to_variable = {{ COLDWAR_CYP_R2_officer_penetration = {_n(pen)} tooltip = {P}deal_officer_penetration_tt }}")
    return "\n".join(out)


def _side_preview(key, side_tag, side, loc, suffix=None):
    spirit = _spirit(key, suffix or side_tag)
    out = [f"add_ideas = {spirit}", _modifier_preview(key, side.get("values", {}), loc)]
    if side.get("research"):
        for i, r in enumerate(side["research"], 1):
            if r.get("type") != "research":
                raise ValueError(f"Unsupported research reward in {key}: {r}")
            loc[f"{spirit}_research_{i}"] = side["spirit"]
            out.append(f"add_tech_bonus = {{ name = {spirit}_research_{i} bonus = {_n(r['bonus'])} uses = {int(r['uses'])} category = {r['category']} }}")
    out.append(_other_effects(side, loc))
    rate = _income_rate(side)
    if rate:
        loc[f"{P}deal_weekly_income_tt"] = "Weekly agreement income: $RIGHT|+=5$ billion/week"
        out.append(f"set_temp_variable = {{ {P}preview_{key}_income = CYP.gdp_total }}")
        out.append(f"multiply_temp_variable = {{ {P}preview_{key}_income = {_n(rate)} }}")
        out.append(f"add_to_variable = {{ {P}preview_{key}_income = 0 tooltip = {P}deal_weekly_income_tt }}")
    return "\n".join(x for x in out if x)


def _preview(key, deal, loc, quoted=False):
    rows = [f"custom_effect_tooltip = {P}if_accept_tt"]
    for tag, side in deal["sides"].items():
        if tag == "each_recipient":
            continue
        rows.append(f"{tag} = {{\n{_side_preview(key, tag, side, loc)}\n}}")
        if tag != "CYP":
            loc[f"{P}deal_treasury_tt"] = "Treasury: $RIGHT|+=5$ billion"
            loc[f"{P}deal_weekly_expense_tt"] = "Weekly agreement expenditure: $RIGHT|+=5$ billion/week"
            rows.append(f"{tag} = {{ add_to_variable = {{ {P}preview_{key}_{tag.lower()}_treasury = 0 tooltip = {P}deal_treasury_tt }} add_to_variable = {{ {P}preview_{key}_{tag.lower()}_expense = 0 tooltip = {P}deal_weekly_expense_tt }} }}")
        else:
            loc[f"{P}deal_weekly_income_tt"] = "Weekly agreement income: $RIGHT|+=5$ billion/week"
            rows.append(f"CYP = {{ add_to_variable = {{ {P}preview_{key}_income = 0 tooltip = {P}deal_weekly_income_tt }} }}")
    if key == "eec":
        side = deal["sides"]["each_recipient"]
        for tag in EEC:
            rows.append(f"{tag} = {{\n{_side_preview(key, tag, side, loc, tag)}\n}}")
            loc[f"{P}deal_treasury_tt"] = "Treasury: $RIGHT|+=5$ billion"
            loc[f"{P}deal_weekly_expense_tt"] = "Weekly agreement expenditure: $RIGHT|+=5$ billion/week"
            loc[f"{P}deal_weekly_income_tt"] = "Weekly agreement income: $RIGHT|+=5$ billion/week"
            rows.append(f"{tag} = {{ add_to_variable = {{ {P}preview_eec_{tag.lower()}_treasury = 0 tooltip = {P}deal_treasury_tt }} add_to_variable = {{ {P}preview_eec_{tag.lower()}_expense = 0 tooltip = {P}deal_weekly_expense_tt }} add_to_variable = {{ {P}preview_eec_{tag.lower()}_income = 0 tooltip = {P}deal_weekly_income_tt }} }}")
    setup = _pct(deal.get("setup", {}).get("CYP", 0))
    if setup and quoted:
        rows.append(f"CYP = {{ set_temp_variable = {{ treasury_change = {P}quote_{key}_setup }} multiply_temp_variable = {{ treasury_change = -1 }} modify_treasury_effect = yes }}")
    elif setup:
        rows.append(f"CYP = {{ set_temp_variable = {{ treasury_change = gdp_total }} multiply_temp_variable = {{ treasury_change = -{_n(setup)} }} modify_treasury_effect = yes }}")
    else:
        loc[f"{P}deal_treasury_tt"] = "Treasury: $RIGHT|+=5$ billion"
        rows.append(f"CYP = {{ add_to_variable = {{ {P}preview_{key}_treasury = 0 tooltip = {P}deal_treasury_tt }} }}")
    weekly = _pct(deal.get("weekly", {}).get("CYP", 0))
    loc[f"{P}deal_weekly_expense_tt"] = "Weekly agreement expenditure: $RIGHT|+=5$ billion/week"
    if weekly:
        rows.append(f"CYP = {{ set_temp_variable = {{ {P}preview_{key}_expense = gdp_total }} multiply_temp_variable = {{ {P}preview_{key}_expense = {_n(weekly)} }} add_to_variable = {{ {P}preview_{key}_expense = 0 tooltip = {P}deal_weekly_expense_tt }} }}")
    else:
        rows.append(f"CYP = {{ add_to_variable = {{ {P}preview_{key}_expense = 0 tooltip = {P}deal_weekly_expense_tt }} }}")
    if key == "eec":
        loc[f"{P}deal_weekly_income_tt"] = "Weekly agreement income: $RIGHT|+=5$ billion/week"
        rows.append(f"CYP = {{ add_to_variable = {{ {P}preview_eec_income = 0 tooltip = {P}deal_weekly_income_tt }} }}")
    return "effect_tooltip = {\n" + "\n".join(rows) + "\n}"


def _pair_clear(tag):
    lines = [f"country_exists = {tag}", f"NOT = {{ has_war_with = {tag} }}", f"NOT = {{ is_embargoing = {tag} }}"]
    lines.append("NOT = { OR = { " + " ".join(f"is_in_array = {{ array = imp_{kind}_sanc_{way} value = {tag} }}" for kind in ("dip", "fin", "eco", "mil") for way in ("on_us", "by_us")) + " } }")
    lines.append(f"{tag} = {{ NOT = {{ has_war_with = CYP }} NOT = {{ is_embargoing = CYP }} NOT = {{ OR = {{ " + " ".join(f"is_in_array = {{ array = imp_{kind}_sanc_{way} value = CYP }}" for kind in ("dip", "fin", "eco", "mil") for way in ("on_us", "by_us")) + " } } }")
    return _b(f"{P}pair_clear_{tag.lower()}", "\n".join(lines))


def build(design: Mapping) -> dict:
    """Return native text files, English localisation and integration metadata."""
    raw = design.get("offers")
    if not isinstance(raw, Mapping):
        raise ValueError("Design offers must be a mapping")
    keys = ("greek_training", "yugoslavia", "britain", "czechoslovakia", "eec", "greek_civil", "turkey")
    missing = set(keys) - set(raw)
    if missing:
        raise ValueError(f"Missing approved offer records: {sorted(missing)}")
    offers = {key: raw[key] for key in keys}
    loc = {
        f"{P}if_accept_tt": "If they accept:",
        f"{P}accept": "Accept the proposal",
        f"{P}decline": "Decline the proposal",
        f"{P}acknowledge": "Acknowledge.",
        f"{P}accepted_desc": "The recipient has approved the agreement. Its paired terms operate while the bilateral relationship remains eligible.",
        f"{P}declined_desc": "The recipient has declined the proposed agreement.",
        f"{P}agreement_accepted_t": "Agreement Ratified",
        f"{P}agreement_declined_t": "Agreement Declined",
    }
    effects = ["# IMPERIA COLD WAR — Cyprus 1970 bilateral agreement effects."]
    triggers = ["# IMPERIA COLD WAR — Cyprus 1970 bilateral agreement triggers."]
    events = [f"# IMPERIA COLD WAR — Cyprus 1970 recipient-approved agreement events.\nadd_namespace = {NS}"]
    ideas = ["# IMPERIA COLD WAR — Cyprus 1970 bilateral agreement spirits.\nideas = {\n\tcountry = {"]
    recipients = {}
    event_num = 101

    for key, deal in offers.items():
        rcp = tuple(deal["recipients"])
        if key == "eec" and rcp != EEC:
            raise ValueError(f"EEC partners must be {EEC}, got {rcp}")
        if key != "eec" and (len(rcp) != 1 or rcp[0] not in LABEL):
            raise ValueError(f"Offer {key} needs one registered recipient")
        recipients[key] = rcp
        loc[f"{NS}.{key}.t"] = f"Cyprus Agreement: {deal['name']}"
        if key == "eec":
            loc[f"{NS}.{key}.d"] = "Cyprus proposes an association protocol to the six Community governments. It takes effect only if all six approve."
        else:
            loc[f"{NS}.{key}.d"] = f"The Republic of Cyprus proposes the terms of the {deal['name']} to {LABEL[rcp[0]]}."
        loc[f"{P}{key}_accept"] = f"Accept the {deal['name']}"
        loc[f"{P}{key}_decline"] = f"Decline the {deal['name']}"
        setup = _pct(deal.get("setup", {}).get("CYP", 0))

        # Create exact paired spirits and their English names.
        for side_tag, side in deal["sides"].items():
            if side_tag == "each_recipient":
                continue
            sp = _spirit(key, side_tag)
            values = " ".join(f"{m} = {_n(v)}" for m, v in side.get("values", {}).items())
            ideas.append(f"\t\t{sp} = {{ picture = international_treaty allowed = {{ always = no }} allowed_civil_war = {{ always = yes }} modifier = {{ {values} }} }}")
            loc[sp] = side["spirit"]
            loc[sp + "_desc"] = f"A standing, recipient-approved {deal['name']} agreement with its bilateral conditions in force."
            for modifier in side.get("values", {}):
                if modifier not in MODS:
                    raise ValueError(f"Missing native effect-preview label for {modifier}")
                loc.setdefault(f"{P}deal_mod_{modifier}_tt", MODS[modifier] + ": $RIGHT|+=%1$")
        if key == "eec":
            side = deal["sides"]["each_recipient"]
            for tag in EEC:
                sp = _spirit(key, tag)
                values = " ".join(f"{m} = {_n(v)}" for m, v in side.get("values", {}).items())
                ideas.append(f"\t\t{sp} = {{ picture = international_treaty allowed = {{ always = no }} allowed_civil_war = {{ always = yes }} modifier = {{ {values} }} }}")
                loc[sp] = f"Cyprus Association Protocol: {LABEL[tag]}"
                loc[sp + "_desc"] = "A standing Community-approved association term, active while all six partners and Cyprus remain eligible."
                for modifier in side.get("values", {}):
                    loc.setdefault(f"{P}deal_mod_{modifier}_tt", MODS[modifier] + ": $RIGHT|+=%1$")

        effects.append(_b(f"COLDWAR_CYP_R2_offer_{key}_preview", _preview(key, deal, loc)))
        effects.append(_b(f"{P}quote_{key}_setup_at_offer",
                          f"set_variable = {{ {P}quote_{key}_setup = gdp_total }}\n"
                          f"multiply_variable = {{ {P}quote_{key}_setup = {_n(setup)} }}"))

        if key == "eec":
            lines = ["tag = CYP original_tag = CYP IMP_is_1970_scenario = yes",
                     "NOT = { has_country_flag = COLDWAR_CYP_R2_eec_signed has_country_flag = COLDWAR_CYP_R2_eec_offer_open has_country_flag = COLDWAR_CYP_R2_eec_declined has_country_flag = COLDWAR_CYP_R2_eec_terminated }",
                     f"{P}eec_membership_and_relations_clear = yes",
                     f"{P}quote_{key}_setup_at_offer = yes",
                     "set_country_flag = { flag = COLDWAR_CYP_R2_eec_offer_open value = 1 days = 90 }",
                     "set_country_flag = COLDWAR_CYP_R2_eec_ever_offered"]
            for i, tag in enumerate(EEC):
                n = 110 + i
                lines.append(f"{tag} = {{ set_country_flag = {{ flag = COLDWAR_CYP_R2_eec_offer_pending value = 1 days = 90 }} country_event = {{ id = {NS}.{n} }} }}")
            effects.append(_b("COLDWAR_CYP_R2_offer_eec", "if = { limit = {\n" + "\n".join("\t" + x for x in lines[:3]) + "\n} \n" + "\n".join(lines[3:]) + "\n}"))
        else:
            tag = rcp[0]
            n = event_num
            event_num += 1
            send = (f"if = {{ limit = {{ tag = CYP original_tag = CYP IMP_is_1970_scenario = yes country_exists = {tag} "
                    f"{P}pair_clear_{tag.lower()} = yes NOT = {{ has_country_flag = {_flag(key, 'signed')} "
                    f"has_country_flag = {_flag(key, 'offer_open')} has_country_flag = {_flag(key, 'declined')} has_country_flag = {_flag(key, 'terminated')} }} }}\n"
                    f"set_country_flag = {{ flag = {_flag(key, 'offer_open')} value = 1 days = 90 }}\n"
                    f"set_country_flag = {_flag(key, 'ever_offered')}\n"
                    f"{P}quote_{key}_setup_at_offer = yes\n"
                    f"{tag} = {{ set_country_flag = {{ flag = {_flag(key, 'offer_pending')} value = 1 days = 90 }} "
                    f"country_event = {{ id = {NS}.{n} }} }}\n}}")
            effects.append(_b(f"COLDWAR_CYP_R2_offer_{key}", send))

        if key != "eec":
            tag = rcp[0]
            valid = (f"tag = {tag} has_country_flag = {_flag(key, 'offer_pending')} "
                     f"CYP = {{ has_country_flag = {_flag(key, 'offer_open')} NOT = {{ has_country_flag = {_flag(key, 'signed')} }} "
                     f"{P}pair_clear_{tag.lower()} = yes check_variable = {{ var = treasury value = {P}quote_{key}_setup compare = greater_than_or_equals }} }}")
            triggers.append(_b(f"{P}{key}_accept_valid_{tag.lower()}", valid))
            triggers.append(_b(f"{P}{key}_active", f"has_country_flag = {_flag(key, 'active')}"))
            effects.append(_b(f"{P}event_preview_{key}", _preview(key, deal, loc, quoted=True)))
            event_body = (f"id = {NS}.{n}\ntitle = {NS}.{key}.t\ndesc = {NS}.{key}.d\n"
                          f"picture = GFX_COLDWAR_CYP_R2_agreement\nis_triggered_only = yes\n"
                          f"trigger = {{ tag = {tag} has_country_flag = {_flag(key, 'offer_pending')} CYP = {{ has_country_flag = {_flag(key, 'offer_open')} }} }}\n"
                          f"option = {{ name = {P}{key}_accept trigger = {{ {P}{key}_accept_valid_{tag.lower()} = yes }} "
                          f"{P}event_preview_{key} = yes hidden_effect = {{ COLDWAR_CYP_R2_accept_{key} = yes }} ai_chance = {{ base = 0 }} }}\n"
                          f"option = {{ name = {P}{key}_decline hidden_effect = {{ COLDWAR_CYP_R2_decline_{key} = yes }} ai_chance = {{ base = 0 }} }}")
            events.append(_b("country_event", event_body))
            effects.append(_b(f"COLDWAR_CYP_R2_accept_{key}",
                f"if = {{ limit = {{ tag = {tag} has_country_flag = {_flag(key, 'offer_pending')} "
                f"CYP = {{ has_country_flag = {_flag(key, 'offer_open')} {P}pair_clear_{tag.lower()} = yes "
                f"NOT = {{ has_country_flag = {_flag(key, 'signed')} }} "
                f"check_variable = {{ var = treasury value = {P}quote_{key}_setup compare = greater_than_or_equals }} }} }}\n"
                f"CYP = {{ set_temp_variable = {{ treasury_change = {P}quote_{key}_setup }} "
                f"multiply_temp_variable = {{ treasury_change = -1 }} modify_treasury_effect = yes "
                f"set_country_flag = {_flag(key, 'signed')} {P}apply_once_{key} = yes }}\n"
                f"set_country_flag = {_flag(key, 'signed')} clr_country_flag = {_flag(key, 'offer_pending')} "
                f"CYP = {{ clr_country_flag = {_flag(key, 'offer_open')} {P}agreements_reconcile = yes country_event = {{ id = {NS}.500 }} }}\n}}"))
            actual = []
            for side_tag, side in deal["sides"].items():
                actual.append(f"{side_tag} = {{\n{_actual(side_tag, side, key)}\n}}")
            effects.append(_b(f"{P}apply_once_{key}", "if = { limit = { NOT = { has_country_flag = " + _flag(key, "assets_paid") + " } }\n" +
                            "\n".join(actual) + f"\nset_country_flag = {_flag(key, 'assets_paid')}\n}}"))
            effects.append(_b(f"COLDWAR_CYP_R2_decline_{key}",
                f"if = {{ limit = {{ tag = {tag} has_country_flag = {_flag(key, 'offer_pending')} CYP = {{ has_country_flag = {_flag(key, 'offer_open')} }} }}\n"
                f"clr_country_flag = {_flag(key, 'offer_pending')} set_country_flag = {_flag(key, 'declined')}\n"
                f"CYP = {{ clr_country_flag = {_flag(key, 'offer_open')} set_country_flag = {_flag(key, 'declined')} country_event = {{ id = {NS}.600 }} }}\n}}"))
            effects.append(_b(f"COLDWAR_CYP_R2_terminate_{key}",
                f"if = {{ limit = {{ tag = CYP has_country_flag = {_flag(key, 'signed')} }}\n"
                f"clr_country_flag = {_flag(key, 'signed')} clr_country_flag = {_flag(key, 'active')} set_country_flag = {_flag(key, 'terminated')} remove_ideas = {_spirit(key, 'CYP')}\n"
                f"{tag} = {{ clr_country_flag = {_flag(key, 'signed')} clr_country_flag = {_flag(key, 'active')} set_country_flag = {_flag(key, 'terminated')} remove_ideas = {_spirit(key, tag)} }}\n"
                f"{P}agreements_reconcile = yes\n}}"))
        else:
            effects.append(_b(f"{P}event_preview_eec", _preview(key, deal, loc, quoted=True)))
            for i, tag in enumerate(EEC):
                n = 110 + i
                triggers.append(_b(f"{P}eec_accept_valid_{tag.lower()}",
                    f"tag = {tag} has_country_flag = COLDWAR_CYP_R2_eec_offer_pending CYP = {{ has_country_flag = COLDWAR_CYP_R2_eec_offer_open "
                    f"{P}eec_membership_and_relations_clear = yes NOT = {{ has_country_flag = COLDWAR_CYP_R2_eec_signed }} "
                    f"check_variable = {{ var = treasury value = {P}quote_eec_setup compare = greater_than_or_equals }} }}"))
                events.append(_b("country_event",
                    f"id = {NS}.{n}\ntitle = {NS}.eec.t\ndesc = {NS}.eec.d\npicture = GFX_COLDWAR_CYP_R2_agreement\n"
                    f"is_triggered_only = yes\ntrigger = {{ tag = {tag} has_country_flag = COLDWAR_CYP_R2_eec_offer_pending CYP = {{ has_country_flag = COLDWAR_CYP_R2_eec_offer_open }} }}\n"
                    f"option = {{ name = {P}eec_accept trigger = {{ {P}eec_accept_valid_{tag.lower()} = yes }} "
                    f"{P}event_preview_eec = yes hidden_effect = {{ COLDWAR_CYP_R2_accept_eec_{tag.lower()} = yes }} ai_chance = {{ base = 0 }} }}\n"
                    f"option = {{ name = {P}eec_decline hidden_effect = {{ COLDWAR_CYP_R2_decline_eec = yes }} ai_chance = {{ base = 0 }} }}"))
                accepted_flags = " ".join(f"has_country_flag = {_flag('eec', 'consent_' + t.lower())}" for t in EEC)
                effects.append(_b(f"COLDWAR_CYP_R2_accept_eec_{tag.lower()}",
                    f"if = {{ limit = {{ tag = {tag} has_country_flag = COLDWAR_CYP_R2_eec_offer_pending CYP = {{ has_country_flag = COLDWAR_CYP_R2_eec_offer_open "
                    f"{P}eec_membership_and_relations_clear = yes NOT = {{ has_country_flag = COLDWAR_CYP_R2_eec_signed }} }} }}\n"
                    f"set_country_flag = {{ flag = {_flag('eec', 'consent')} value = 1 days = 90 }}\n"
                    f"CYP = {{ set_country_flag = {{ flag = {_flag('eec', 'consent_' + tag.lower())} value = 1 days = 90 }}\n"
                    f"if = {{ limit = {{ {accepted_flags} check_variable = {{ var = treasury value = {P}quote_eec_setup compare = greater_than_or_equals }} }}\n"
                    f"set_temp_variable = {{ treasury_change = {P}quote_eec_setup }} multiply_temp_variable = {{ treasury_change = -1 }} modify_treasury_effect = yes\n"
                    f"set_country_flag = COLDWAR_CYP_R2_eec_signed\n" +
                    "\n".join(f"{t} = {{ set_country_flag = COLDWAR_CYP_R2_eec_signed }}" for t in EEC) + "\n" +
                    f"{P}apply_once_eec = yes country_event = {{ id = {NS}.500 }} {P}agreements_reconcile = yes\n}} }}\n"
                    f"clr_country_flag = COLDWAR_CYP_R2_eec_offer_pending\n}}"))
            effects.append(_b(f"{P}apply_once_eec",
                f"if = {{ limit = {{ NOT = {{ has_country_flag = {_flag('eec', 'assets_paid')} }} }}\n"
                f"CYP = {{\n{_actual('CYP', deal['sides']['CYP'], 'eec')}\n}}\n" +
                "\n".join(f"{tag} = {{\n{_actual(tag, deal['sides']['each_recipient'], 'eec')}\n}}" for tag in EEC) +
                f"\nset_country_flag = {_flag('eec', 'assets_paid')}\n}}"))
            effects.append(_b(f"COLDWAR_CYP_R2_decline_eec",
                "if = { limit = { has_country_flag = COLDWAR_CYP_R2_eec_offer_pending CYP = { has_country_flag = COLDWAR_CYP_R2_eec_offer_open } }\n" +
                "\n".join(f"{tag} = {{ clr_country_flag = COLDWAR_CYP_R2_eec_offer_pending clr_country_flag = COLDWAR_CYP_R2_eec_consent }}" for tag in EEC) +
                "CYP = { clr_country_flag = COLDWAR_CYP_R2_eec_offer_open set_country_flag = COLDWAR_CYP_R2_eec_declined " +
                " ".join(f"clr_country_flag = COLDWAR_CYP_R2_eec_consent_{t.lower()}" for t in EEC) +
                f" country_event = {{ id = {NS}.600 }} }}\n}}"))
            effects.append(_b("COLDWAR_CYP_R2_terminate_eec",
                "if = { limit = { tag = CYP has_country_flag = COLDWAR_CYP_R2_eec_signed }\n"
                "clr_country_flag = COLDWAR_CYP_R2_eec_signed clr_country_flag = COLDWAR_CYP_R2_eec_active set_country_flag = COLDWAR_CYP_R2_eec_terminated remove_ideas = COLDWAR_CYP_R2_eec_cyp\n" +
                "\n".join(f"{tag} = {{ clr_country_flag = COLDWAR_CYP_R2_eec_signed clr_country_flag = COLDWAR_CYP_R2_eec_active set_country_flag = COLDWAR_CYP_R2_eec_terminated remove_ideas = {_spirit('eec', tag)} }}" for tag in EEC) +
                "\n}"))
            triggers.append(_b(f"{P}eec_active", "has_country_flag = COLDWAR_CYP_R2_eec_active"))

    # Paired agreement reconciliation is called monthly and through targeted transitions.
    reconcile = ["if = { limit = { tag = CYP original_tag = CYP IMP_is_1970_scenario = yes }"]
    for key, rcp in recipients.items():
        if key == "eec":
            all_signed = " ".join(f"{tag} = {{ has_country_flag = COLDWAR_CYP_R2_eec_signed }}" for tag in EEC)
            add = "\n".join(f"{tag} = {{ set_country_flag = COLDWAR_CYP_R2_eec_active if = {{ limit = {{ NOT = {{ has_idea = {_spirit('eec', tag)} }} }} add_ideas = {_spirit('eec', tag)} }} }}" for tag in EEC)
            remove = "\n".join(f"if = {{ limit = {{ country_exists = {tag} }} {tag} = {{ clr_country_flag = COLDWAR_CYP_R2_eec_active remove_ideas = {_spirit('eec', tag)} }} }}" for tag in EEC)
            reconcile.append(
                f"if = {{ limit = {{ has_country_flag = COLDWAR_CYP_R2_eec_signed {P}eec_membership_and_relations_clear = yes {all_signed} }}\n"
                f"set_country_flag = COLDWAR_CYP_R2_eec_active if = {{ limit = {{ NOT = {{ has_idea = {_spirit('eec', 'CYP')} }} }} add_ideas = {_spirit('eec', 'CYP')} }}\n{add}\n"
                f"}} else = {{ clr_country_flag = COLDWAR_CYP_R2_eec_active remove_ideas = {_spirit('eec', 'CYP')} {remove} }}")
        else:
            tag = rcp[0]
            ok = f"has_country_flag = {_flag(key, 'signed')} {P}pair_clear_{tag.lower()} = yes {tag} = {{ has_country_flag = {_flag(key, 'signed')} }}"
            reconcile.append(
                f"if = {{ limit = {{ {ok} }}\nset_country_flag = {_flag(key, 'active')} if = {{ limit = {{ NOT = {{ has_idea = {_spirit(key, 'CYP')} }} }} add_ideas = {_spirit(key, 'CYP')} }}\n"
                f"{tag} = {{ set_country_flag = {_flag(key, 'active')} if = {{ limit = {{ NOT = {{ has_idea = {_spirit(key, tag)} }} }} add_ideas = {_spirit(key, tag)} }} }}\n"
                f"}} else = {{ clr_country_flag = {_flag(key, 'active')} remove_ideas = {_spirit(key, 'CYP')} "
                f"if = {{ limit = {{ country_exists = {tag} }} {tag} = {{ clr_country_flag = {_flag(key, 'active')} remove_ideas = {_spirit(key, tag)} }} }} }}")
    reconcile.append("}")
    effects.append(_b(f"{P}agreements_reconcile", "\n".join(reconcile)))

    # Weekly stream recalculation reads cached active flags only.
    stream = [
        f"set_variable = {{ {P}deal_weekly_income = 0 }}",
        f"set_variable = {{ {P}deal_weekly_expenses = 0 }}",
        "if = { limit = { IMP_is_1970_scenario = yes }",
    ]
    for key, deal in offers.items():
        rate = _pct(deal.get("weekly", {}).get("CYP", 0))
        if rate:
            stream.append(f"if = {{ limit = {{ tag = CYP has_country_flag = {_flag(key, 'active')} }} set_temp_variable = {{ {P}stream_amount = gdp_total }} multiply_temp_variable = {{ {P}stream_amount = {_n(rate)} }} add_to_variable = {{ {P}deal_weekly_expenses = {P}stream_amount }} }}")
        if key != "eec":
            tag = deal["recipients"][0]
            income = _income_rate(deal["sides"].get(tag, {}))
            if income:
                stream.append(f"if = {{ limit = {{ tag = {tag} CYP = {{ has_country_flag = {_flag(key, 'active')} }} }} set_temp_variable = {{ {P}stream_amount = CYP.gdp_total }} multiply_temp_variable = {{ {P}stream_amount = {_n(income)} }} add_to_variable = {{ {P}deal_weekly_income = {P}stream_amount }} }}")
    stream.append("}")
    effects.append(_b(f"{P}agreements_weekly_streams", "\n".join(stream)))

    # Eleven fixed pairs only: GRE is shared by two offers, plus the six Community states.
    pair_tags = ("GRE", "SER", "ENG", "CZE", "TUR", *EEC)
    triggers.extend(_pair_clear(tag) for tag in pair_tags)
    eec_clear = ["country_exists = CYP"] + [f"{tag} = {{ COLDWAR_EC_is_member = yes }}" for tag in EEC] + [f"{P}pair_clear_{tag.lower()} = yes" for tag in EEC]
    triggers.append(_b(f"{P}eec_membership_and_relations_clear", "\n".join(eec_clear)))

    # Event-local final notices let Cyprus see the recipient's real response.
    for n, title, desc in ((500, f"{P}agreement_accepted_t", f"{P}accepted_desc"),
                           (600, f"{P}agreement_declined_t", f"{P}declined_desc")):
        events.append(_b("country_event", f"id = {NS}.{n}\ntitle = {title}\ndesc = {desc}\npicture = GFX_COLDWAR_CYP_R2_agreement\nis_triggered_only = yes\ntrigger = {{ tag = CYP }}\noption = {{ name = {P}acknowledge }}"))
    loc[f"{P}agreement_accepted_t"] = "Agreement Ratified"
    loc[f"{P}agreement_declined_t"] = "Agreement Declined"

    # Clear timed proposal state after flags expire. This does not poll relations.
    cleanup = ["if = { limit = { tag = CYP }"]
    for key, rcp in recipients.items():
        if key == "eec":
            cleanup.append("if = { limit = { NOT = { has_country_flag = COLDWAR_CYP_R2_eec_offer_open } } " +
                           "if = { limit = { has_country_flag = COLDWAR_CYP_R2_eec_ever_offered NOT = { has_country_flag = COLDWAR_CYP_R2_eec_signed } } set_country_flag = COLDWAR_CYP_R2_eec_declined } " +
                           " ".join(f"{tag} = {{ clr_country_flag = COLDWAR_CYP_R2_eec_offer_pending clr_country_flag = COLDWAR_CYP_R2_eec_consent if = {{ limit = {{ CYP = {{ has_country_flag = COLDWAR_CYP_R2_eec_declined }} }} set_country_flag = COLDWAR_CYP_R2_eec_declined }} }}" for tag in EEC) + " }")
        else:
            tag = rcp[0]
            cleanup.append(f"if = {{ limit = {{ NOT = {{ has_country_flag = {_flag(key, 'offer_open')} }} }} "
                           f"if = {{ limit = {{ has_country_flag = {_flag(key, 'ever_offered')} NOT = {{ has_country_flag = {_flag(key, 'signed')} }} }} set_country_flag = {_flag(key, 'declined')} }} "
                           f"{tag} = {{ clr_country_flag = {_flag(key, 'offer_pending')} if = {{ limit = {{ CYP = {{ has_country_flag = {_flag(key, 'declined')} }} }} set_country_flag = {_flag(key, 'declined')} }} }} }}")
    cleanup.append("}")
    effects.append(_b(f"{P}agreements_clear_expired_offers", "\n".join(cleanup)))

    ideas.append("\t}\n}")
    gfx = ("# IMPERIA COLD WAR — Cyprus 1970 agreement country-event picture registration.\n"
           "spriteTypes = {\n\tspriteType = {\n"
           "\t\tname = \"GFX_COLDWAR_CYP_R2_agreement\"\n"
           "\t\ttexturefile = \"gfx/event_pictures/generic/elections/political_deal.dds\"\n"
           "\t}\n}\n")
    files = {
        "common/scripted_effects/COLDWAR_CYP_R2_agreements.txt": "\n".join(effects).rstrip() + "\n",
        "common/scripted_triggers/COLDWAR_CYP_R2_agreements.txt": "\n".join(triggers).rstrip() + "\n",
        "events/COLDWAR_CYP_R2_agreements.txt": "\n".join(events).rstrip() + "\n",
        "common/ideas/COLDWAR_CYP_R2_agreement_ideas.txt": "\n".join(ideas).rstrip() + "\n",
        "interface/COLDWAR_CYP_R2_eventpictures.gfx": gfx,
    }
    return {
        "files": files,
        "loc": loc,
        "meta": {
            "project": "IMPERIA COLD WAR",
            "namespace": NS,
            "offers": list(offers),
            "recipients": {k: list(v) for k, v in recipients.items()},
            "offer_effects": {k: f"COLDWAR_CYP_R2_offer_{k}" for k in offers},
            "preview_effects": {k: f"COLDWAR_CYP_R2_offer_{k}_preview" for k in offers},
            "active_triggers": {k: f"{P}{k}_active" for k in offers},
            "termination_effects": {k: f"COLDWAR_CYP_R2_terminate_{k}" for k in offers},
            "event_picture_sprite": "GFX_COLDWAR_CYP_R2_agreement",
            "core_event_picture": "GFX_COLDWAR_CYP_R2_agreement",
            "event_picture_texture": "gfx/event_pictures/generic/elections/political_deal.dds",
            "event_picture_size": [217, 163],
            "event_picture_inset": [19, 6, 180, 150],
            "native_event_window": {
                "size": [581, 427],
                "image_position_in_bottom_window": [5, 5],
                "options_origin_in_bottom_window": [215, -1],
                "option_slot": [300, 47],
                "options_per_offer": 2,
                "visible_option_stack_height": 94,
                "bottom_window_height": 206,
            },
            "event_picture_note": "Reuses the loaded native MD political-deal composite without modification. Original image authorship and licence are unknown in the local snapshot.",
            "reconcile_effect": f"{P}agreements_reconcile",
            "expired_offer_cleanup_effect": f"{P}agreements_clear_expired_offers",
            "weekly_streams_effect": f"{P}agreements_weekly_streams",
            "weekly_income_variable": f"{P}deal_weekly_income",
            "weekly_expenses_variable": f"{P}deal_weekly_expenses",
            "relationship_schedule": "CYP-scoped fixed pairs; parent wiring calls monthly and on targeted transitions. Weekly streams read active cache flags only.",
            "setup_cost_basis": "Committed Cyprus GDP quote calculated at offer, checked against treasury and paid once on ratification.",
            "weekly_cost_basis": "JSON weekly percentages divided by 100 into GDP multipliers; no division by 52.",
            "eec_membership_gate": "All six named recipients must be members of the European Communities (COLDWAR_EC_is_member). Cyprus remains an associate and is not made a member or given CYP_eu_membership.",
        },
    }


def _actual(tag, side, key):
    out = [f"add_ideas = {_spirit(key, tag)}"]
    for i, r in enumerate(side.get("research", []), 1):
        out.append(f"add_tech_bonus = {{ name = {_spirit(key, tag)}_research_{i} bonus = {_n(r['bonus'])} uses = {int(r['uses'])} category = {r['category']} }}")
    xp = _other_value(side, "Army experience")
    pen = _other_value(side, "Officer penetration")
    if xp is not None:
        out.append(f"army_experience = {_n(xp)}")
    if pen is not None:
        out.append(f"add_to_variable = {{ COLDWAR_CYP_R2_officer_penetration = {_n(pen)} }}")
    return "\n".join(out)
