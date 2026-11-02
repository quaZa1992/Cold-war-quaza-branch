# IMPERIA COLD WAR — France 1970 procurement pressure runtime generator.
"""Build recipient-approved neocolonial pressure decisions and their lifecycle."""
from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from textwrap import indent
from typing import Any

MARK = "# IMPERIA COLD WAR — France 1970 procurement pressure.\n"
PREFIX = "COLDWAR_FRA2_pressure"
TAG_PREFIX = "COLDWAR_FRA2_pressure_"
FINANCE_ENTRY = "fp_african_finance"
SECURITY_ENTRY = "fp_african_security"
FINANCE_FOCUS = "COLDWAR_FRA2_fp_african_finance"
SECURITY_FOCUS = "COLDWAR_FRA2_fp_african_security"


def _block(key: str, *children: str) -> str:
    rows = [f"{key} = {{"]
    rows.extend(indent(child, "\t") for child in children if child)
    rows.append("}")
    return "\n".join(rows)


def _pct(value: Any) -> Decimal:
    return Decimal(str(value)) / Decimal(100)


def _num(value: Decimal) -> str:
    rendered = format(value, "f").rstrip("0").rstrip(".")
    return rendered or "0"


def _read_contracts() -> dict:
    source = Path(__file__).with_name("pressure_contracts.json")
    data = json.loads(source.read_text(encoding="utf-8"))
    assert data["project"] == "IMPERIA COLD WAR"
    assert data["prefix"] == PREFIX
    return data


def pressure_unlocks_by_entry() -> dict[str, list[str]]:
    source = _read_contracts()
    result: dict[str, list[str]] = {}
    for row in source["partners"]:
        for focus in row["entry_focuses"]:
            result.setdefault(focus, []).append(row["tag"])
    return result


def _partner_data(design: dict) -> tuple[dict, dict[str, dict]]:
    source = _read_contracts()
    nodes = {node["key"]: node for node in design["nodes"]}
    offers: dict[str, dict] = {}
    partners: dict[str, dict] = {}
    for row in source["partners"]:
        tag = row["tag"]
        assert tag not in partners
        partners[tag] = row
        base_names = []
        for key in row["base_contracts"]:
            node = nodes.get(key)
            assert node and node.get("offer"), (tag, key)
            assert node["offer"]["partner"] == tag, (tag, key, node["offer"].get("partner"))
            offers[key] = node["offer"]
            base_names.append(node["offer"]["recipient"]["name"])
        row["base_spirit_names"] = base_names
        assert set(row["entry_focuses"]) <= {FINANCE_ENTRY, SECURITY_ENTRY}
    assert len(partners) == 6
    assert {tag for tag in partners} == {"NGR", "GAB", "SEN", "CAM", "CDI", "CHA"}
    return source, partners


def _aid_rows(design: dict, row: dict, source: dict) -> list[tuple[str, Decimal]]:
    result = []
    for node in design["nodes"]:
        offer = node.get("offer")
        if not offer or offer.get("partner") != row["tag"]:
            continue
        key = node["key"]
        france_effects = offer["france"]["effects"]
        for effect in france_effects:
            if effect.get("kind") == "weekly_transfer" and effect.get("flow") == "expense" and effect.get("payer") == "FRA":
                fraction = Decimal(str(effect["gdp_fraction"]))
                if fraction <= 0 or len(format(fraction, "f").split(".")[-1]) > 5:
                    raise ValueError(f"Unsupported France support share: {key}/{effect}")
                result.append((key, fraction))
    return result


def _base_trigger(tag: str, row: dict) -> str:
    active = "\n".join(f"COLDWAR_FRA2_offer_active_{key} = yes" for key in row["base_contracts"])
    return _block(f"{PREFIX}_base_active_{tag}", _block("OR", active))


def _pressure_triggers(source: dict, partners: dict[str, dict]) -> str:
    out = []
    for row in partners.values():
        tag = row["tag"]
        base = f"{PREFIX}_base_active_{tag} = yes"
        paired_pending = f"{tag} = {{ has_country_flag = {TAG_PREFIX}pending_{tag} }}"
        paired_signed = f"{tag} = {{ has_country_flag = {TAG_PREFIX}charter_signed_{tag} }}"
        out.append(_base_trigger(tag, row))
        out.append(_block(f"{PREFIX}_can_send_{tag}", "\n".join((
            "tag = FRA",
            "IMP_is_1970_scenario = yes",
            "OR = { " + " ".join(f"has_completed_focus = COLDWAR_FRA2_{focus}" for focus in row["entry_focuses"]) + " }",
            f"country_exists = {tag}",
            base,
            f"NOT = {{ has_country_flag = {TAG_PREFIX}pending_{tag} }}",
            f"NOT = {{ {paired_pending} }}",
            f"NOT = {{ has_country_flag = {TAG_PREFIX}charter_signed_{tag} }}",
            f"NOT = {{ {paired_signed} }}",
            f"NOT = {{ has_country_flag = {TAG_PREFIX}cooldown_{tag} }}",
            "COLDWAR_FRA2_pair_" + tag + "_clear = yes",
            "check_variable = { gdp_total > 0 }",
            f"{tag} = {{ check_variable = {{ gdp_total > 0 }} }}",
        ))))
        out.append(_block(f"{PREFIX}_can_accept_{tag}", "\n".join((
            f"tag = {tag}",
            f"has_country_flag = {TAG_PREFIX}pending_{tag}",
            f"FRA = {{ has_country_flag = {TAG_PREFIX}pending_{tag} }}",
            f"NOT = {{ has_country_flag = {TAG_PREFIX}charter_signed_{tag} }}",
            f"FRA = {{ NOT = {{ has_country_flag = {TAG_PREFIX}charter_signed_{tag} }} }}",
            f"FRA = {{ {base} COLDWAR_FRA2_pair_{tag}_clear = yes check_variable = {{ gdp_total > 0 }} }}",
            "check_variable = { gdp_total > 0 }",
        ))))
        out.append(_block(f"{PREFIX}_can_resolve_{tag}", "\n".join((
            f"tag = {tag}",
            f"has_country_flag = {TAG_PREFIX}pending_{tag}",
            f"FRA = {{ has_country_flag = {TAG_PREFIX}pending_{tag} }}",
        ))))
        out.append(_block(f"{PREFIX}_can_timeout_{tag}", "\n".join((
            f"{PREFIX}_can_resolve_{tag} = yes",
            f"FRA = {{ {base} COLDWAR_FRA2_pair_{tag}_clear = yes check_variable = {{ gdp_total > 0 }} }}",
            "check_variable = { gdp_total > 0 }",
        ))))
        out.append(_block(f"{PREFIX}_refusal_qualifies_{tag}", "\n".join((
            f"country_exists = {tag}",
            base,
            f"COLDWAR_FRA2_pair_{tag}_clear = yes",
            "check_variable = { gdp_total > 0 }",
            f"{tag} = {{ check_variable = {{ gdp_total > 0 }} }}",
        ))))
        out.append(_block(f"{PREFIX}_active_{tag}", "\n".join((
            f"has_country_flag = {TAG_PREFIX}charter_signed_{tag}",
            f"{tag} = {{ has_country_flag = {TAG_PREFIX}charter_signed_{tag} }}",
            f"{base}",
            f"COLDWAR_FRA2_pair_{tag}_clear = yes",
        ))))
    return MARK + "\n\n".join(out) + "\n"


def _fee_preview(tag: str, fraction: Decimal) -> str:
    return "\n".join((
        f"set_temp_variable = {{ treasury_change = {{ value = gdp_total multiply = -{_num(fraction)} }} }}",
        "modify_treasury_effect = yes",
    ))


def _accept_preview_side(tag: str, source: dict, partner: dict) -> tuple[str, dict[str, str]]:
    setup = _pct(source["france_setup_gdp_percent"]) if tag == "FRA" else _pct(source["host_setup_gdp_percent"])
    loc = {}
    rows = [_fee_preview(tag, setup)]
    if tag == "FRA":
        variable = f"{PREFIX}_quote_preview_{partner['tag']}"
        rows.extend((
            f"set_temp_variable = {{ {variable} = {{ value = {partner['tag']}.gdp_total multiply = {_num(_pct(source['host_annual_gdp_levy_percent']))} divide = 52 }} }}",
            f"set_temp_variable = {{ {variable}_millions = {{ value = {variable} multiply = 1000 }} }}",
            f"custom_effect_tooltip = {PREFIX}_accept_income_preview_{partner['tag']}",
            f"give_guarantee = {partner['tag']}",
            f"add_ideas = {PREFIX}_charter_france_{partner['tag']}",
        ))
        loc[f"{PREFIX}_accept_income_preview_{partner['tag']}"] = (
            f"§YAdditional Income§! increases by $$[?{variable}_millions|G2] Million/week\n"
        )
    else:
        variable = f"{PREFIX}_levy_preview_{tag}"
        rows.extend((
            f"set_temp_variable = {{ {variable} = {{ value = gdp_total multiply = {_num(_pct(source['host_annual_gdp_levy_percent']))} divide = 52 }} }}",
            f"set_temp_variable = {{ {variable}_millions = {{ value = {variable} multiply = 1000 }} }}",
            f"custom_effect_tooltip = {PREFIX}_accept_expense_preview_{tag}",
            "add_ideas = " + f"{PREFIX}_charter_host_{tag}",
            f"give_military_access = FRA",
        ))
        loc[f"{PREFIX}_accept_expense_preview_{tag}"] = (
            f"§YAdditional Expenses§! increases by $$[?{variable}_millions|R2] Million/week\n"
        )
    return f"{tag} = {{\n{indent(chr(10).join(rows), chr(9))}\n}}", loc


def _refusal_preview_side(tag: str, partner: dict, source: dict, aid_rows: list[tuple[str, Decimal]]) -> tuple[str, dict[str, str]]:
    loc = {}
    rows = []
    if tag == "FRA":
        variable = f"{PREFIX}_aid_freeze_preview_{partner['tag']}"
        contribution_rows = [f"set_temp_variable = {{ {variable} = 0 }}"]
        for key, fraction in aid_rows:
            contribution_rows.append(_block("if", _block("limit", f"COLDWAR_FRA2_offer_active_{key} = yes"),
                f"set_temp_variable = {{ {variable}_row = {{ value = gdp_total multiply = {_num(fraction)} divide = 52 }} }}",
                f"add_to_variable = {{ {variable} = {variable}_row }}"))
        if aid_rows:
            contribution_rows.extend((
                f"set_temp_variable = {{ {variable}_millions = {{ value = {variable} multiply = 1000 }} }}",
                f"custom_effect_tooltip = {PREFIX}_refusal_france_{partner['tag']}",
            ))
            rows.append(_block("if", _block("limit", _block("OR", *(f"COLDWAR_FRA2_offer_active_{key} = yes" for key, _ in aid_rows))), *contribution_rows))
            loc[f"{PREFIX}_refusal_france_{partner['tag']}"] = (
                f"§YAdditional Expenses§! decrease by $$[?{variable}_millions|G2] Million/week for {int(source['french_aid_freeze_days'])} days\n"
            )
    else:
        variable = f"{PREFIX}_aid_freeze_preview_{tag}"
        contribution_rows = [f"set_temp_variable = {{ {variable} = 0 }}"]
        for key, fraction in aid_rows:
            contribution_rows.append(_block("if", _block("limit", f"FRA = {{ COLDWAR_FRA2_offer_active_{key} = yes }}"),
                f"set_temp_variable = {{ {variable}_row = {{ value = FRA.gdp_total multiply = {_num(fraction)} divide = 52 }} }}",
                f"add_to_variable = {{ {variable} = {variable}_row }}"))
        if aid_rows:
            contribution_rows.extend((
                f"set_temp_variable = {{ {variable}_millions = {{ value = {variable} multiply = 1000 }} }}",
                f"custom_effect_tooltip = {PREFIX}_refusal_host_{tag}",
            ))
            rows.append(_block("if", _block("limit", f"FRA = {{ {_block('OR', *(f'COLDWAR_FRA2_offer_active_{key} = yes' for key, _ in aid_rows))} }}"), *contribution_rows))
            loc[f"{PREFIX}_refusal_host_{tag}"] = (
                f"§YAdditional Income§! decreases by $$[?{variable}_millions|R2] Million/week for {int(source['french_aid_freeze_days'])} days\n"
            )
        rows.append(f"add_timed_idea = {{ idea = {PREFIX}_withdrawal_crisis days = {int(source['withdrawal_crisis_days'])} }}")
    return f"{tag} = {{\n{indent(chr(10).join(rows), chr(9))}\n}}", loc


def _preview_effect(tag: str, source: dict, partner: dict, aid_rows: list[tuple[str, Decimal]]) -> tuple[str, dict[str, str]]:
    accept_fra, loc_a_fra = _accept_preview_side("FRA", source, partner)
    accept_host, loc_a_host = _accept_preview_side(tag, source, partner)
    refuse_fra, loc_r_fra = _refusal_preview_side("FRA", partner, source, aid_rows)
    refuse_host, loc_r_host = _refusal_preview_side(tag, partner, source, aid_rows)
    rows = [
        "custom_effect_tooltip = TT_IF_THEY_ACCEPT",
        f"custom_effect_tooltip = {PREFIX}_france_heading",
        accept_fra,
        f"custom_effect_tooltip = {PREFIX}_host_heading_{tag}",
        accept_host,
        "custom_effect_tooltip = " + PREFIX + "_if_they_refuse",
        f"custom_effect_tooltip = {PREFIX}_france_heading",
        refuse_fra,
        f"custom_effect_tooltip = {PREFIX}_host_heading_{tag}",
        refuse_host,
    ]
    loc = {**loc_a_fra, **loc_a_host, **loc_r_fra, **loc_r_host}
    return _block(f"{PREFIX}_preview_{tag}", "\n".join(rows)), loc


def _offer_decisions(source: dict, partners: dict[str, dict], design: dict) -> tuple[list[str], str, str, dict[str, str]]:
    send_rows, response_rows, effect_rows, loc = [], [], [], {}
    for index, partner in enumerate(partners.values(), start=1):
        tag, name = partner["tag"], partner["name"]
        aid_rows = _aid_rows(design, partner, source)
        preview, preview_loc = _preview_effect(tag, source, partner, aid_rows)
        event_call = f"{tag} = {{ country_event = {{ id = COLDWAR_FRA2_pressure.{index} days = {int(source['pending_days'])} }} }}"
        start_body = _block("if", _block("limit", f"{PREFIX}_can_send_{tag} = yes"),
            f"set_country_flag = {TAG_PREFIX}pending_{tag}",
            f"{tag} = {{ set_country_flag = {TAG_PREFIX}pending_{tag} }}",
            f"set_country_flag = {{ flag = {TAG_PREFIX}cooldown_{tag} value = 1 days = {int(source['pressure_cooldown_days'])} }}",
            event_call)
        accept_body = _block("if", _block("limit", f"{PREFIX}_can_accept_{tag} = yes"),
            f"set_country_flag = {TAG_PREFIX}charter_signed_{tag}",
            f"FRA = {{ set_country_flag = {TAG_PREFIX}charter_signed_{tag} clr_country_flag = {TAG_PREFIX}pending_{tag} set_temp_variable = {{ treasury_change = {{ value = gdp_total multiply = -{_num(_pct(source['france_setup_gdp_percent']))} }} }} modify_treasury_effect = yes update_money_dirty_variable = yes }}",
            f"clr_country_flag = {TAG_PREFIX}pending_{tag}",
            f"set_temp_variable = {{ treasury_change = {{ value = gdp_total multiply = -{_num(_pct(source['host_setup_gdp_percent']))} }} }}",
            "modify_treasury_effect = yes",
            "update_money_dirty_variable = yes",
            f"FRA = {{ COLDWAR_FRA2_pressure_sync_all = yes }}")
        resolve = _block("if", _block("limit", f"{PREFIX}_can_resolve_{tag} = yes"),
            f"COLDWAR_FRA2_pressure_register_refusal_{tag} = yes")
        cancel = "\n".join((
            _block("if", _block("limit", f"has_country_flag = {TAG_PREFIX}pending_{tag}"), f"clr_country_flag = {TAG_PREFIX}pending_{tag}"),
            f"FRA = {{ clr_country_flag = {TAG_PREFIX}pending_{tag} update_money_dirty_variable = yes }}",
            "update_money_dirty_variable = yes",
        ))
        active_refusal = _block("if", _block("limit", f"FRA = {{ {PREFIX}_refusal_qualifies_{tag} = yes }}"),
            f"FRA = {{ set_country_flag = {{ flag = {TAG_PREFIX}aid_freeze_{tag} value = 1 days = {int(source['french_aid_freeze_days'])} }} set_country_flag = {TAG_PREFIX}aid_freeze_refresh_{tag} update_money_dirty_variable = yes }}",
            f"add_timed_idea = {{ idea = {PREFIX}_withdrawal_crisis days = {int(source['withdrawal_crisis_days'])} }}",
            "update_money_dirty_variable = yes")
        refusal = _block("if", _block("limit", f"{PREFIX}_can_resolve_{tag} = yes"),
            f"clr_country_flag = {TAG_PREFIX}pending_{tag}",
            f"FRA = {{ clr_country_flag = {TAG_PREFIX}pending_{tag} }}",
            active_refusal,
            f"FRA = {{ update_money_dirty_variable = yes }}",
            "update_money_dirty_variable = yes")
        send_rows.append(_block(f"{PREFIX}_send_{tag}", "\n".join((
            "icon = europe",
            f"visible = {{ tag = FRA IMP_is_1970_scenario = yes OR = {{ {' '.join(f'has_completed_focus = COLDWAR_FRA2_{f}' for f in partner['entry_focuses'])} }} }}",
            f"available = {{ custom_trigger_tooltip = {{ tooltip = {PREFIX}_send_requirement_{tag} {PREFIX}_can_send_{tag} = yes }} }}",
            f"custom_cost_text = {PREFIX}_send_cost_35_pp",
            "cost = 35",
            "days_remove = 1",
            f"complete_effect = {{ effect_tooltip = {{ {PREFIX}_preview_{tag} = yes }} hidden_effect = {{ {PREFIX}_start_{tag} = yes }} }}",
            "ai_will_do = { base = 0 }",
        ))))
        response_rows.extend((
            _block(f"{PREFIX}_accept_decision_{tag}", "\n".join((
                "icon = europe",
                f"visible = {{ tag = {tag} has_country_flag = {TAG_PREFIX}pending_{tag} }}",
                f"available = {{ custom_trigger_tooltip = {{ tooltip = {PREFIX}_accept_requirement_{tag} {PREFIX}_can_accept_{tag} = yes }} }}",
                "cost = 0", "days_remove = 1",
                f"complete_effect = {{ effect_tooltip = {{ {PREFIX}_preview_{tag} = yes }} hidden_effect = {{ {PREFIX}_accept_{tag} = yes }} }}",
                "ai_will_do = { base = 0 }",
            ))),
            _block(f"{PREFIX}_refuse_decision_{tag}", "\n".join((
                "icon = europe",
                f"visible = {{ tag = {tag} has_country_flag = {TAG_PREFIX}pending_{tag} }}",
                "available = { always = yes }",
                "cost = 0", "days_remove = 1",
                f"complete_effect = {{ effect_tooltip = {{ {PREFIX}_preview_{tag} = yes }} hidden_effect = {{ {PREFIX}_refuse_{tag} = yes }} }}",
                "ai_will_do = { base = 0 }",
            ))),
        ))
        effect_rows.extend((
            _block(f"{PREFIX}_start_{tag}", start_body),
            _block(f"{PREFIX}_accept_{tag}", accept_body),
            _block(f"{PREFIX}_refuse_{tag}", resolve),
            _block(f"{PREFIX}_cancel_{tag}", cancel),
            _block(f"{PREFIX}_register_refusal_{tag}", refusal),
            preview,
        ))
        loc.update(preview_loc)
        loc.update({
            f"{PREFIX}_send_{tag}": f"Demand {name}'s Procurement Charter",
            f"{PREFIX}_send_{tag}_desc": f"France uses its existing leverage through {', '.join(partner['base_spirit_names'])} to demand a permanent procurement charter. Paris requires an answer within {int(source['pending_days'])} days. Refusal brings a {int(source['withdrawal_crisis_days'])}-day crisis and pauses France-paid cash support for {int(source['french_aid_freeze_days'])} days where such payments exist.",
            f"{PREFIX}_send_requirement_{tag}": f"At least one agreement must remain active: {' or '.join(partner['base_spirit_names'])}. Relations must be peaceful and the 365-day ultimatum interval must have elapsed.",
            f"{PREFIX}_accept_requirement_{tag}": "The offer must remain pending and its qualifying agreement must stay active while both countries remain at peace.",
            f"{PREFIX}_accept_decision_{tag}": f"Ratify the French Procurement Charter",
            f"{PREFIX}_accept_decision_{tag}_desc": f"The charter trades procurement and financial autonomy for French security guarantees and military access. Paris requires an answer within {int(source['pending_days'])} days.",
            f"{PREFIX}_refuse_decision_{tag}": "Refuse the French Procurement Ultimatum",
            f"{PREFIX}_refuse_decision_{tag}_desc": f"Rejecting preserves existing agreement rights but brings a {int(source['withdrawal_crisis_days'])}-day withdrawal crisis and pauses France-paid cash support for {int(source['french_aid_freeze_days'])} days where applicable. Paris requires an answer within {int(source['pending_days'])} days.",
            f"{PREFIX}_charter_host_{tag}": f"Procurement Charter under French Protection: {name}",
            f"{PREFIX}_charter_host_{tag}_desc": "French procurement privileges shape domestic industry and military costs, while the government accepts a recurring payment and receives security support.",
            f"{PREFIX}_charter_france_{tag}": f"French Protection Costs: {name}",
            f"{PREFIX}_charter_france_{tag}_desc": "France guarantees the partner's security and pays the personnel costs of its military commitment.",
            f"{PREFIX}_withdrawal_crisis": "Withdrawal of French Support",
            f"{PREFIX}_withdrawal_crisis_desc": "French advisers, funding, and contractors are withdrawn after the procurement ultimatum is refused.",
            f"{PREFIX}_host_heading_{tag}": f"§Y[{tag}.GetName]§!",
        })
    categories, decisions = _decision_file(source, partners, send_rows, response_rows)
    return effect_rows, categories, decisions, loc


def _pressure_effect_file(source: dict, partners: dict[str, dict], decision_effects: list[str]) -> str:
    effects = list(decision_effects)
    effects.extend(_charter_effects(source, partners))
    effects.append(_pressure_sync(source, partners))
    effects.extend(_weekly_stream_effects(source, partners))
    return MARK + "\n\n".join(effects) + "\n"


def _charter_effects(source: dict, partners: dict[str, dict]) -> list[str]:
    out = []
    for tag in partners:
        fraction = _num(_pct(source["host_annual_gdp_levy_percent"]))
        quote = f"{PREFIX}_levy_quote_{tag}"
        fresh = f"{PREFIX}_levy_quote_fresh_{tag}"
        out.append(_block(f"{PREFIX}_cache_levy_quote_{tag}",
            _block("if", _block("limit", f"NOT = {{ has_country_flag = {fresh} }}"),
                f"set_variable = {{ {quote} = {{ value = {tag}.gdp_total multiply = {fraction} divide = 52 }} }}",
                f"set_country_flag = {{ flag = {fresh} value = 1 days = 7 }}")))
    return out


def _pressure_sync(source: dict, partners: dict[str, dict]) -> str:
    bodies = []
    for tag in partners:
        active = f"{PREFIX}_active_{tag} = yes"
        host_idea = f"{PREFIX}_charter_host_{tag}"
        france_idea = f"{PREFIX}_charter_france_{tag}"
        signed = f"{TAG_PREFIX}charter_signed_{tag}"
        access_owned = f"{TAG_PREFIX}access_owned_{tag}"
        guarantee_owned = f"{TAG_PREFIX}guarantee_owned_{tag}"
        stream_active = f"{TAG_PREFIX}stream_active_{tag}"
        quote_fresh = f"{PREFIX}_levy_quote_fresh_{tag}"
        active_rows = [
            f"if = {{ limit = {{ NOT = {{ has_idea = {france_idea} }} }} add_ideas = {france_idea} }}",
            f"{tag} = {{ if = {{ limit = {{ NOT = {{ has_idea = {host_idea} }} }} add_ideas = {host_idea} }} }}",
            f"if = {{ limit = {{ NOT = {{ has_guaranteed = {tag} }} }} give_guarantee = {tag} set_country_flag = {guarantee_owned} }}",
            f"if = {{ limit = {{ NOT = {{ has_military_access_to = {tag} }} }} {tag} = {{ give_military_access = FRA set_country_flag = {access_owned} }} }}",
            f"if = {{ limit = {{ NOT = {{ has_country_flag = {stream_active} }} }} set_country_flag = {stream_active} clr_country_flag = {quote_fresh} update_money_dirty_variable = yes {tag} = {{ update_money_dirty_variable = yes }} }}",
        ]
        inactive_rows = [
            f"if = {{ limit = {{ has_idea = {france_idea} }} remove_ideas = {france_idea} }}",
            f"{tag} = {{ if = {{ limit = {{ has_idea = {host_idea} }} remove_ideas = {host_idea} }} }}",
            f"if = {{ limit = {{ has_country_flag = {guarantee_owned} }} diplomatic_relation = {{ country = {tag} relation = guarantee active = no }} clr_country_flag = {guarantee_owned} }}",
            f"if = {{ limit = {{ {tag} = {{ has_country_flag = {access_owned} }} }} "
            f"if = {{ limit = {{ has_military_access_to = {tag} }} diplomatic_relation = {{ country = {tag} relation = military_access active = no }} }} "
            f"{tag} = {{ clr_country_flag = {access_owned} }} }}",
            f"if = {{ limit = {{ has_country_flag = {stream_active} }} clr_country_flag = {stream_active} clr_country_flag = {quote_fresh} update_money_dirty_variable = yes {tag} = {{ update_money_dirty_variable = yes }} }}",
        ]
        reconcile = _block("if", _block("limit", active), *active_rows) + "\nelse = {\n" + indent("\n".join(inactive_rows), "\t") + "\n}"
        refresh = _block("if", _block("limit", f"has_country_flag = {TAG_PREFIX}aid_freeze_refresh_{tag} NOT = {{ has_country_flag = {TAG_PREFIX}aid_freeze_{tag} }}"),
            f"clr_country_flag = {TAG_PREFIX}aid_freeze_refresh_{tag}",
            "update_money_dirty_variable = yes",
            f"{tag} = {{ update_money_dirty_variable = yes }}")
        pending_inconsistent = _block("if", _block("limit",
            f"has_country_flag = {TAG_PREFIX}pending_{tag} {tag} = {{ NOT = {{ has_country_flag = {TAG_PREFIX}pending_{tag} }} }}"),
            f"clr_country_flag = {TAG_PREFIX}pending_{tag}")
        recipient_pending_inconsistent = _block("if", _block("limit",
            f"NOT = {{ has_country_flag = {TAG_PREFIX}pending_{tag} }} {tag} = {{ has_country_flag = {TAG_PREFIX}pending_{tag} }}"),
            f"{tag} = {{ clr_country_flag = {TAG_PREFIX}pending_{tag} }}")
        pending_ineligible = _block("if", _block("limit",
            f"has_country_flag = {TAG_PREFIX}pending_{tag} {tag} = {{ has_country_flag = {TAG_PREFIX}pending_{tag} }} NOT = {{ {PREFIX}_base_active_{tag} = yes COLDWAR_FRA2_pair_{tag}_clear = yes }}"),
            f"clr_country_flag = {TAG_PREFIX}pending_{tag}",
            f"{tag} = {{ clr_country_flag = {TAG_PREFIX}pending_{tag} }}",
            "update_money_dirty_variable = yes",
            f"{tag} = {{ update_money_dirty_variable = yes }}")
        orphan_pending = _block("if", _block("limit", f"has_country_flag = {TAG_PREFIX}pending_{tag} NOT = {{ country_exists = {tag} }}"),
            f"clr_country_flag = {TAG_PREFIX}pending_{tag}")
        bodies.extend((reconcile, refresh, pending_inconsistent, recipient_pending_inconsistent, pending_ineligible, orphan_pending))
    return _block(f"{PREFIX}_sync_all", _block("if", _block("limit", "tag = FRA"), *bodies))


def _weekly_stream_effects(source: dict, partners: dict[str, dict]) -> list[str]:
    expenses, income = [], []
    for tag in partners:
        active = f"FRA = {{ {PREFIX}_active_{tag} = yes }}"
        quote = f"FRA.{PREFIX}_levy_quote_{tag}"
        expenses.append(_block("if", _block("limit", f"tag = {tag} {active}"),
            f"FRA = {{ {PREFIX}_cache_levy_quote_{tag} = yes }}",
            f"add_to_variable = {{ additional_expenses_rate = {quote} }}",
            f"add_to_variable = {{ COLDWAR_FRA2_cooperation_weekly_expenses = {quote} }}"))
        income.append(_block("if", _block("limit", f"tag = FRA {PREFIX}_active_{tag} = yes"),
            f"{PREFIX}_cache_levy_quote_{tag} = yes",
            f"add_to_variable = {{ additional_income_rate = {PREFIX}_levy_quote_{tag} }}",
            f"add_to_variable = {{ COLDWAR_FRA2_cooperation_weekly_income = {PREFIX}_levy_quote_{tag} }}"))
    return [
        _block(f"{PREFIX}_add_weekly_expenses", "\n".join(expenses)),
        _block(f"{PREFIX}_add_weekly_income", "\n".join(income)),
    ]


def _decision_file(source: dict, partners: dict[str, dict], send_rows: list[str], response_rows: list[str]) -> tuple[str, str]:
    send_category = _block(f"{PREFIX}_send_category", "\n".join((
        "icon = GFX_decision_category_generic_foreign_policy",
        "allowed = { original_tag = FRA IMP_is_1970_scenario = yes }",
        "visible = { original_tag = FRA IMP_is_1970_scenario = yes OR = { "
        + " ".join(f"has_completed_focus = COLDWAR_FRA2_{focus}" for focus in (FINANCE_ENTRY, SECURITY_ENTRY)) + " } }",
        "priority = 146",
    )))
    response_visibility = "\n".join(
        _block("AND", f"tag = {row['tag']}", f"has_country_flag = {TAG_PREFIX}pending_{row['tag']}")
        for row in partners.values()
    )
    response_category = _block(f"{PREFIX}_response_category", "\n".join((
        "icon = GFX_decision_category_generic_foreign_policy",
        "allowed = { always = yes }",
        "visible = { OR = {\n" + indent(response_visibility, "\t\t") + "\n\t} }",
        "priority = 146",
    )))
    category_file = MARK + "\n\n".join((send_category, response_category)) + "\n"
    decisions_file = MARK + "\n\n".join((
        _block(f"{PREFIX}_send_category", "\n\n".join(send_rows)),
        _block(f"{PREFIX}_response_category", "\n\n".join(response_rows)),
    )) + "\n"
    return category_file, decisions_file


def _idea_file(source: dict, partners: dict[str, dict]) -> str:
    ideas = []
    for tag in partners:
        host_modifiers = source["host_charter_modifiers"]
        france_modifiers = source["france_charter_modifiers"]
        ideas.append(_idea_block(f"{PREFIX}_charter_host_{tag}", host_modifiers))
        ideas.append(_idea_block(f"{PREFIX}_charter_france_{tag}", france_modifiers))
    ideas.append(_idea_block(f"{PREFIX}_withdrawal_crisis", source["withdrawal_crisis_modifiers"]))
    return MARK + "ideas = {\n\tcountry = {\n" + indent("\n".join(ideas), "\t\t") + "\n\t}\n}\n"


def _idea_block(idea_id: str, modifiers: dict[str, Any]) -> str:
    lines = [f"{key} = {_num(Decimal(str(value)))}" for key, value in modifiers.items()]
    return _block(idea_id, "picture = foreign_capital", "allowed = { always = no }",
        "allowed_civil_war = { always = yes }", _block("modifier", "\n".join(lines)))


def _event_file(source: dict, partners: dict[str, dict]) -> str:
    rows = ["add_namespace = COLDWAR_FRA2_pressure"]
    for index, row in enumerate(partners.values(), start=1):
        tag = row["tag"]
        rows.append(_block("country_event", "\n".join((
            f"id = COLDWAR_FRA2_pressure.{index}",
            "is_triggered_only = yes",
            "hidden = yes",
            f"trigger = {{ has_country_flag = {TAG_PREFIX}pending_{tag} FRA = {{ has_country_flag = {TAG_PREFIX}pending_{tag} }} }}",
            "immediate = {",
            f"\tif = {{ limit = {{ {PREFIX}_can_timeout_{tag} = yes }} {PREFIX}_refuse_{tag} = yes }}",
            f"\telse = {{ {PREFIX}_cancel_{tag} = yes }}",
            "}",
        ))))
    return MARK + "\n\n".join(rows) + "\n"


def _pressure_loc(source: dict) -> dict[str, str]:
    return {
        f"{PREFIX}_send_cost_35_pp": "35 £pol_power",
        f"{PREFIX}_france_heading": "§Y[FRA.GetName]§!",
        f"{PREFIX}_if_they_refuse": "§YIf they refuse§!",
        f"{PREFIX}_send_category": "French Procurement Ultimatums",
        f"{PREFIX}_send_category_desc": "Present negotiated procurement charters to governments tied to active French agreements.",
        f"{PREFIX}_response_category": "French Procurement Charter Responses",
        f"{PREFIX}_response_category_desc": "Review and answer pending French procurement ultimatums.",
    }


def build_pressure(design: dict) -> dict[str, dict[str, str]]:
    """Return generated pressure runtime files and English localisation."""
    source, partners = _partner_data(design)
    effect_rows, categories, decisions, loc = _offer_decisions(source, partners, design)
    loc.update(_pressure_loc(source))
    effects = _pressure_effect_file(source, partners, effect_rows)
    ideas = _idea_file(source, partners)
    events = _event_file(source, partners)
    triggers = _pressure_triggers(source, partners)
    files = {
        "common/scripted_effects/COLDWAR_FRA2_pressure_effects.txt": effects,
        "common/scripted_triggers/COLDWAR_FRA2_pressure_triggers.txt": triggers,
        "common/ideas/COLDWAR_FRA2_pressure_ideas.txt": ideas,
        "common/decisions/categories/COLDWAR_FRA2_pressure_categories.txt": categories,
        "common/decisions/COLDWAR_FRA2_pressure_decisions.txt": decisions,
        "events/COLDWAR_FRA2_pressure_events.txt": events,
    }
    return {"files": files, "loc": loc}
