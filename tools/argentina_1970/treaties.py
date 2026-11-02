# IMPERIA COLD WAR — Argentina bilateral agreements.
"""Generate recipient-consented Argentina 1970 treaty runtime from the approved design."""
from __future__ import annotations

import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'south_america_event_art'))
from sa_photo_catalogue import picture_for
from typing import Any
from budget import money,compensation,annual_share,own_weekly_weight,transfer,weekly_value

PREFIX = "COLDWAR_ARG_"
SANCTIONS = (
    "imp_dip_sanc_on_us", "imp_dip_sanc_by_us",
    "imp_fin_sanc_on_us", "imp_fin_sanc_by_us",
    "imp_eco_sanc_on_us", "imp_eco_sanc_by_us",
    "imp_mil_sanc_on_us", "imp_mil_sanc_by_us",
)


def _n(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.5f}".rstrip("0").rstrip(".") or "0"
    return str(value)


def _flag(a: dict[str, Any], suffix: str) -> str:
    return f"{PREFIX}treaty_{a['id']}_{suffix}"


def _idea(a: dict[str, Any], tag: str) -> str:
    side = "arg" if tag == "ARG" else "partner"
    return f"{PREFIX}treaty_{a['id']}_{side}"


def _modifier_loc(key: str) -> str:
    return f"{PREFIX}treaty_modifier_{key}"


def _player_text(value: str) -> str:
    return value.replace("–", "-").replace("—", ":")


def _pair_clear(a: dict[str, Any]) -> str:
    partner = a["partner"]
    sanc_arg = " ".join(f"is_in_array = {{ array = {ar} value = {partner} }}" for ar in SANCTIONS)
    sanc_partner = " ".join(f"is_in_array = {{ array = {ar} value = ARG }}" for ar in SANCTIONS)
    return f"""country_exists = {partner}
NOT = {{ has_war_with = {partner} }}
NOT = {{ is_embargoing = {partner} }}
NOT = {{ OR = {{ {sanc_arg} }} }}
{partner} = {{
  NOT = {{ has_war_with = ARG }}
  NOT = {{ is_embargoing = ARG }}
  NOT = {{ OR = {{ {sanc_partner} }} }}
}}"""


def _parent_active(a: dict[str, Any]) -> str:
    parent = a.get("parent")
    if not parent:
        return ""
    return "\n".join((
        f"ARG = {{ has_idea = {PREFIX}treaty_{parent}_arg COLDWAR_ARG_treaty_{parent}_active = yes }}",
        f"{a['partner']} = {{ has_idea = {PREFIX}treaty_{parent}_partner }}",
    ))


def _territory_guard(a: dict[str, Any]) -> str:
    if a["id"] not in ("uk_links", "uk_sovereignty"):
        return ""
    guard = "ENG = { owns_state = 26 controls_state = 26 26 = { is_owned_and_controlled_by = PREV } }"
    if a["id"] == "uk_sovereignty":
        guard += "\nARG = { NOT = { owns_state = 26 } }"
    return guard


def _war_history_guard(a: dict[str, Any]) -> str:
    # The design's post-war restoration requirements depend on the core's native war-history provider.
    if a["id"] in ("madrid_consular", "madrid_diplomatic"):
        return "COLDWAR_ARG_south_atlantic_peace = yes"
    return ""


def _building_guard(a: dict[str, Any]) -> str:
    lines: list[str] = []
    for b in a.get("buildings", []):
        tag = b["country"]
        state = int(b["state"])
        levels = int(b["levels"])
        # Main MD 2.0.2 common/buildings/00_buildings.txt sets infrastructure level_cap.state_max = 6.
        cap = 6 if b["type"] == "infrastructure" else 20 if b["type"] in ("industrial_complex", "arms_factory", "dockyard") else 10
        body = [
            f"is_owned_and_controlled_by = PREV",
            f"check_variable = {{ var = building_level@{b['type']} value = {cap - levels} compare = less_than_or_equals }}",
        ]
        if b["type"] not in ("infrastructure", "land_fort", "coastal_fort", "air_base", "radar_station", "nuclear_reactor", "rocket_site", "fuel_silo", "supply_node", "railway"):
            body.append(f"free_building_slots = {{ building = {b['type']} size > {levels - 1} include_locked = yes }}")
        lines.append(f"{tag} = {{ owns_state = {state} controls_state = {state} {state} = {{ {' '.join(body)} }} }}")
    return "\n".join(lines)


def _deal_guard(a: dict[str, Any]) -> str:
    extra = "\n".join(x for x in (_parent_active(a), _territory_guard(a), _war_history_guard(a)) if x)
    return "\n".join(x for x in (_pair_clear(a), extra, _building_guard(a),f"hidden_trigger = {{ ARG = {{ check_variable = {{ gdp_total > 0 }} }} {a['partner']} = {{ check_variable = {{ gdp_total > 0 }} }} }}") if x)


def _active_trigger(a: dict[str, Any]) -> str:
    p = a["partner"]
    parent = _parent_active(a)
    # Only continuing political and economic relationship conditions suspend a ratified treaty.
    # Signature-time ownership, capacity, war-history and territory conditions never roll back assets.
    guard = _pair_clear(a)
    return f"""COLDWAR_ARG_treaty_{a['id']}_active = {{
  custom_trigger_tooltip = {{
  tooltip = COLDWAR_ARG_treaty_{a['id']}_active_tt
  hidden_trigger = {{
  country_exists = ARG
  ARG = {{
    has_country_flag = {_flag(a, 'signed')}
    {guard}
    {parent}
  }}
  {p} = {{ has_country_flag = {_flag(a, 'signed')} }}
  }}
  }}
}}"""


def _can_offer(a: dict[str, Any]) -> str:
    p = a["partner"]
    clauses = [
        f"hidden_trigger = {{ tag = ARG country_exists = {p} NOT = {{ has_country_flag = {_flag(a, 'signed')} }} check_variable = {{ gdp_total > 0 }} {p} = {{ check_variable = {{ gdp_total > 0 }} }} }}",
        f"custom_trigger_tooltip = {{ tooltip = COLDWAR_ARG_treaty_proposal_ready_tt hidden_trigger = {{ NOT = {{ has_country_flag = {_flag(a, 'pending')} }} NOT = {{ has_country_flag = {_flag(a, 'cooldown')} }} }} }}",
        f"custom_trigger_tooltip = {{ tooltip = COLDWAR_ARG_treaty_pair_clear_tt hidden_trigger = {{ {_pair_clear(a)} }} }}",
        _parent_active(a), _territory_guard(a), _war_history_guard(a), _building_guard(a),
    ]
    return f"COLDWAR_ARG_can_offer_treaty_{a['id']} = {{\n  " + "\n  ".join(x for x in clauses if x) + "\n}"


def _flow(a,side,kind,target,tooltip=None):
    """Compute a current-country stream, preserving one matching bilateral transfer."""
    tag='ARG' if side=='argentina' else a['partner']
    share=annual_share(own_weekly_weight(a,side)) if kind=='expense' else 0
    tr=transfer(a)
    transferred=tr[2] if tr and tag==tr[0 if kind=='expense' else 1] else 0
    if not share and not transferred:return ''
    v=PREFIX+'treaty_weekly_quote'
    rows=[f'set_temp_variable = {{ {v} = 0 }}']
    if share:rows.append(f'add_to_temp_variable = {{ {v} = {weekly_value(share)} }}')
    if transferred:rows.append(f'add_to_temp_variable = {{ {v} = {weekly_value(transferred,"ARG.gdp_total")} }}')
    if tooltip and kind=='expense':rows.append(f'multiply_temp_variable = {{ {v} = -1 }}')
    rows.append(f'add_to_variable = {{ {target} = {v}'+(f' tooltip = {tooltip}' if tooltip else '')+' }')
    return '\n'.join(rows)

def _preview(a: dict[str, Any]) -> str:
    k, p = a["id"], a["partner"]
    lines = [f"COLDWAR_ARG_preview_{k} = {{", f"custom_effect_tooltip = COLDWAR_ARG_treaty_if_they_accept_tt"]
    for tag, side in (("ARG", a["argentina"]), (p, a["recipient"])):
        amount = float(side.get("setup", 0))
        if amount:
            lines += [f"{tag} = {{", money(amount), "}"]
        if tag == p and float(side.get("grant", 0)):
            lines += [f"{tag} = {{", compensation(0.015), "}"]
        # Every signed modifier and recurring flow is rendered in its recipient scope.
        numeric = []
        for stat, value in side.get("modifiers", {}).items():
            if float(value) == 0:
                continue
            numeric.append(f"add_to_variable = {{ {PREFIX}treaty_preview_{k}_{tag.lower()}_{stat} = {_n(value)} tooltip = {_modifier_loc(stat)} }}")
        which='argentina' if tag=='ARG' else 'recipient'
        numeric.append(_flow(a,which,'expense',f'{PREFIX}treaty_preview_weekly_{k}_{tag.lower()}','COLDWAR_ARG_treaty_weekly_cost_tt'))
        numeric.append(_flow(a,which,'income',f'{PREFIX}treaty_preview_credit_{k}_{tag.lower()}','COLDWAR_ARG_treaty_weekly_income_tt'))
        numeric=[n for n in numeric if n]
        if numeric:
            lines += [f"{tag} = {{", *["  " + line for line in numeric], "}"]
        lines += [f"{tag} = {{ add_ideas = {_idea(a, tag)} }}"]
    for b in a.get("buildings", []):
        lines.append(f"{b['state']} = {{ add_extra_state_shared_building_slots = {b['levels']} add_building_construction = {{ type = {b['type']} level = {b['levels']} instant_build = yes }} }}")
    for research in a.get("research", []):
        lines.append(f"{research['country']} = {{ add_tech_bonus = {{ name = {PREFIX}treaty_{k}_{research['country'].lower()} category = {research['category']} bonus = {_n(research['bonus'])} uses = {int(research['uses'])} }} }}")
    if k == "uk_sovereignty":
        lines += ["# Transfer is shown as a prospective effect only; executed after British consent.", "ARG = { transfer_state = 26 }"]
    lines.append("}")
    return "\n".join(lines)


def _offer(a: dict[str, Any], index: int) -> str:
    p = a["partner"]
    f = _flag(a, "pending")
    return f"""COLDWAR_ARG_offer_{a['id']} = {{
  if = {{
    limit = {{ COLDWAR_ARG_can_offer_treaty_{a['id']} = yes }}
    set_country_flag = {_flag(a, 'initiated')}
    set_country_flag = {{ flag = {f} value = 1 days = 90 }}
    set_country_flag = {{ flag = {_flag(a, 'cooldown')} value = 1 days = 180 }}
    {p} = {{
      set_country_flag = {{ flag = {f} value = 1 days = 90 }}
      country_event = {{ id = COLDWAR_ARG_TREATY.{index} }}
    }}
  }}
}}"""


def _accept(a: dict[str, Any]) -> str:
    k, p = a["id"], a["partner"]
    g = _deal_guard(a)
    checks = [
        f"tag = {p}", f"has_country_flag = {_flag(a, 'pending')}",
        f"ARG = {{ has_country_flag = {_flag(a, 'pending')} }}",
        f"NOT = {{ has_country_flag = {_flag(a, 'signed')} }}",
        f"ARG = {{ NOT = {{ has_country_flag = {_flag(a, 'signed')} }} }}",
        f"ARG = {{ {g} }}",
    ]
    effects: list[str] = []
    for tag, side in (("ARG", a["argentina"]), (p, a["recipient"])):
        setup = float(side.get("setup", 0))
        # Compensation is a separate transfer from Argentina to Britain.
        if setup:
            effects += [f"{tag} = {{", money(setup), "}"]
    if k == "uk_sovereignty":
        comp = float(a["recipient"].get("grant", 0))
        if comp:
            effects += [f"{p} = {{", compensation(0.015), "}"]
    for b in a.get("buildings", []):
        effects.append(f"{b['state']} = {{ add_extra_state_shared_building_slots = {b['levels']} add_building_construction = {{ type = {b['type']} level = {b['levels']} instant_build = yes }} }}")
    for research in a.get("research", []):
        effects.append(f"{research['country']} = {{ add_tech_bonus = {{ name = {PREFIX}treaty_{k}_{research['country'].lower()} category = {research['category']} bonus = {_n(research['bonus'])} uses = {int(research['uses'])} }} }}")
    if k == "uk_sovereignty":
        effects.append("ARG = { transfer_state = 26 }")
    effects += [
        f"set_country_flag = {_flag(a, 'signed')}",
        f"ARG = {{ set_country_flag = {_flag(a, 'signed')} clr_country_flag = {_flag(a, 'pending')} add_ideas = {_idea(a, 'ARG')} }}",
        f"clr_country_flag = {_flag(a, 'pending')}",
        f"add_ideas = {_idea(a, p)}",
        "COLDWAR_ARG_refresh_treaties = yes",
    ]
    return f"""COLDWAR_ARG_execute_treaty_{k} = {{
  if = {{
    limit = {{ {' '.join(x for x in checks if x)} }}
    {' '.join(effects)}
  }}
}}"""


def _decisions(agreements: list[dict[str, Any]]) -> tuple[str, str]:
    categories = ["# IMPERIA COLD WAR — Argentina agreement decision categories."]
    decisions = ["# IMPERIA COLD WAR — Argentina agreement response decisions."]
    partners = sorted({a["partner"] for a in agreements})
    country_allow = " ".join(f"tag = {tag}" for tag in ["ARG", *partners])
    categories.append(f"COLDWAR_ARG_contracts = {{ allowed = {{ OR = {{ {country_allow} }} }} icon = generic_foreign_policy priority = 150 visible = {{ always = yes }} }}")
    entries: list[str] = []
    for a in agreements:
        k, p = a["id"], a["partner"]
        pending = _flag(a, "pending")
        parent = _parent_active(a)
        g = _deal_guard(a)
        accepted_visible = f"tag = {p} has_country_flag = {pending}"
        accept_available = f"tag = {p} has_country_flag = {pending} ARG = {{ has_country_flag = {pending} NOT = {{ has_country_flag = {_flag(a, 'signed')} }} {g} }}"
        entries += [
            f"""COLDWAR_ARG_accept_treaty_{k} = {{
  icon = generic_political_discourse
  visible = {{ {accepted_visible} }}
  available = {{ {accept_available} }}
  cost = 0
  days_remove = 90
  complete_effect = {{ effect_tooltip = {{ COLDWAR_ARG_preview_{k} = yes }} hidden_effect = {{ COLDWAR_ARG_execute_treaty_{k} = yes }} }}
  ai_will_do = {{ base = 0 }}
}}""",
            f"""COLDWAR_ARG_decline_treaty_{k} = {{
  icon = generic_political_discourse
  visible = {{ {accepted_visible} }}
  available = {{ {accepted_visible} ARG = {{ has_country_flag = {pending} }} }}
  cost = 0
  days_remove = 90
  complete_effect = {{
    hidden_effect = {{ ARG = {{ clr_country_flag = {pending} }} clr_country_flag = {pending} }}
  }}
  ai_will_do = {{ base = 0 }}
}}""",
            f"""COLDWAR_ARG_reoffer_treaty_{k} = {{
  icon = generic_political_discourse
  visible = {{ tag = ARG has_completed_focus = {a['focus']} has_country_flag = {_flag(a, 'initiated')} NOT = {{ has_country_flag = {_flag(a, 'signed')} }} NOT = {{ has_country_flag = {pending} }} NOT = {{ has_country_flag = {_flag(a, 'cooldown')} }} }}
  available = {{ tag = ARG has_completed_focus = {a['focus']} has_country_flag = {_flag(a, 'initiated')} COLDWAR_ARG_can_offer_treaty_{k} = yes }}
  cost = 0
  complete_effect = {{ hidden_effect = {{ if = {{ limit = {{ tag = ARG has_completed_focus = {a['focus']} has_country_flag = {_flag(a, 'initiated')} COLDWAR_ARG_can_offer_treaty_{k} = yes }} COLDWAR_ARG_offer_{k} = yes }} }} }}
  ai_will_do = {{ base = 0 }}
}}""",
        ]
    # Argentine re-offers are retry decisions only; the distinct national focus initiates each first offer.
    decisions.append("COLDWAR_ARG_contracts = {\n" + "\n\n".join("  " + entry.replace("\n", "\n  ") for entry in entries) + "\n}")
    return "\n\n".join(categories), "\n\n".join(decisions)


def _events(agreements: list[dict[str, Any]]) -> str:
    lines = ["# IMPERIA COLD WAR — Argentina treaty offer notifications.", "add_namespace = COLDWAR_ARG_TREATY"]
    for i, a in enumerate(agreements, 1):
        lines += [f"""country_event = {{
  id = COLDWAR_ARG_TREATY.{i}
  title = COLDWAR_ARG_TREATY.{i}.t
  desc = COLDWAR_ARG_TREATY.{i}.d
  picture = {picture_for('COLDWAR_ARG_TREATY.'+str(i))}
  is_triggered_only = yes
  option = {{ name = COLDWAR_ARG_TREATY.{i}.a }}
}}"""]
    return "\n\n".join(lines)


def _ideas(agreements: list[dict[str, Any]]) -> str:
    lines = ["# IMPERIA COLD WAR — Argentina bilateral standing agreement spirits.", "ideas = {", "  country = {"]
    for a in agreements:
        for tag, side in (("ARG", a["argentina"]), (a["partner"], a["recipient"])):
            lines += [f"    {_idea(a, tag)} = {{", "      picture = generic_trade", "      allowed = { always = yes }", "      removal_cost = -1", "      modifier = {"]
            for stat, value in side.get("modifiers", {}).items():
                lines.append(f"        {stat} = {_n(value)}")
            lines += ["      }", "    }"]
    lines += ["  }", "}"]
    return "\n".join(lines)


def _effects(agreements: list[dict[str, Any]]) -> str:
    lines = ["# IMPERIA COLD WAR — Argentina bilateral agreement runtime effects."]
    for i, a in enumerate(agreements, 1):
        lines += [_preview(a), _offer(a, i), _accept(a)]
    lines += ["COLDWAR_ARG_refresh_treaties = {"]
    # Reconcile both signatories even after ARG disappears, parents before dependents.
    ordered=[]
    def add(a):
        if a in ordered:return
        if a.get('parent'):add(next(p for p in agreements if p['id']==a['parent']))
        ordered.append(a)
    for a in agreements:add(a)
    for a in ordered:
        lines.append(f"  if = {{ limit = {{ COLDWAR_ARG_treaty_{a['id']}_active = yes }}")
        for tag in ('ARG',a['partner']):
            lines.append(f"    {tag} = {{ if = {{ limit = {{ NOT = {{ has_idea = {_idea(a,tag)} }} }} add_ideas = {_idea(a,tag)} }} }}")
        lines.append('  } else = {')
        for tag in ('ARG',a['partner']):
            lines.append(f"    {tag} = {{ if = {{ limit = {{ has_idea = {_idea(a,tag)} }} remove_ideas = {_idea(a,tag)} }} }}")
        lines.append('  }')
    lines += ["}"]
    lines += ["COLDWAR_ARG_add_treaty_income = {", "  if = { limit = { tag = ARG }"]
    for a in agreements:
        amount = float(a["argentina"].get("credit", 0))
        if amount:
            lines.append(f"    if = {{ limit = {{ COLDWAR_ARG_treaty_{a['id']}_active = yes }} {_flow(a,'argentina','income','additional_income_rate')} }}")
    lines += ["  }", "  else = {"]
    for a in agreements:
        amount = float(a["recipient"].get("credit", 0))
        if amount:
            lines.append(f"    if = {{ limit = {{ tag = {a['partner']} has_country_flag = {_flag(a, 'signed')} ARG = {{ COLDWAR_ARG_treaty_{a['id']}_active = yes }} }} {_flow(a,'recipient','income','additional_income_rate')} }}")
    lines += ["  }", "}"]
    lines += ["COLDWAR_ARG_add_treaty_expenses = {", "  if = { limit = { tag = ARG }"]
    for a in agreements:
        amount = float(a["argentina"].get("weekly", 0))
        if amount:
            lines.append(f"    if = {{ limit = {{ COLDWAR_ARG_treaty_{a['id']}_active = yes }} {_flow(a,'argentina','expense','additional_expenses_rate')} }}")
    lines += ["  }", "  else = {"]
    for a in agreements:
        amount = float(a["recipient"].get("weekly", 0))
        if amount:
            lines.append(f"    if = {{ limit = {{ tag = {a['partner']} has_country_flag = {_flag(a, 'signed')} ARG = {{ COLDWAR_ARG_treaty_{a['id']}_active = yes }} }} {_flow(a,'recipient','expense','additional_expenses_rate')} }}")
    lines += ["  }", "}"]
    return "\n\n".join(lines)


def _triggers(agreements: list[dict[str, Any]]) -> str:
    lines = ["# IMPERIA COLD WAR — Argentina bilateral agreement triggers."]
    for a in agreements:
        lines += [_active_trigger(a), _can_offer(a)]
    return "\n\n".join(lines)


def _localisation(agreements: list[dict[str, Any]], labels: dict[str,str]) -> str:
    rows = [
        "l_english:",
        "# IMPERIA COLD WAR — Argentina bilateral agreement text.",
        ' COLDWAR_ARG_treaty_if_they_accept_tt:0 "If they accept:"',
        ' COLDWAR_ARG_treaty_weekly_cost_tt:0 "Recurring weekly payment: $RIGHT|+=5$ billion per week"',
        ' COLDWAR_ARG_treaty_weekly_income_tt:0 "Recurring weekly income: $RIGHT|+=5$ billion per week"',
        ' COLDWAR_ARG_contracts:0 "Bilateral Agreements"',
        ' COLDWAR_ARG_contracts_desc:0 "Review proposals and pending bilateral commitments."',
        ' COLDWAR_ARG_treaty_pair_clear_tt:0 "Both countries exist, are at peace with one another and impose no mutual embargo or sanctions."',
        ' COLDWAR_ARG_treaty_pair_clear_tt_NOT:0 "A signatory no longer exists, or the countries are at war or impose a mutual embargo or sanctions."',
        ' COLDWAR_ARG_treaty_proposal_ready_tt:0 "No pending proposal and the 180-day proposal interval has elapsed."',
        ' COLDWAR_ARG_treaty_proposal_ready_tt_NOT:0 "A proposal is pending or the 180-day proposal interval has not elapsed."',
    ]
    modifiers: dict[str, str] = {}
    for a in agreements:
        rows += [
            f' COLDWAR_ARG_accept_treaty_{a["id"]}:0 "Accept the agreement"',
            f' COLDWAR_ARG_decline_treaty_{a["id"]}:0 "Decline the agreement"',
            f' COLDWAR_ARG_reoffer_treaty_{a["id"]}:0 "Renew the proposal"',
            f' COLDWAR_ARG_accept_treaty_{a["id"]}_desc:0 "Accept the complete agreement as offered."',
            f' COLDWAR_ARG_decline_treaty_{a["id"]}_desc:0 "Decline the proposed terms."',
            f' COLDWAR_ARG_reoffer_treaty_{a["id"]}_desc:0 "Renew the proposal after the waiting period."',
            f' COLDWAR_ARG_treaty_{a["id"]}_arg:0 "{_player_text(a["argentina"]["spirit"])}"',
            f' COLDWAR_ARG_treaty_{a["id"]}_partner:0 "{_player_text(a["recipient"]["spirit"])}"',
            f' COLDWAR_ARG_treaty_{a["id"]}_arg_desc:0 "{_player_text(a["description"])}"',
            f' COLDWAR_ARG_treaty_{a["id"]}_partner_desc:0 "{_player_text(a["description"])}"',
            f' COLDWAR_ARG_treaty_{a["id"]}_active_tt:0 "The ${PREFIX}treaty_{a["id"]}_arg$ agreement is active."',
            f' COLDWAR_ARG_treaty_{a["id"]}_active_tt_NOT:0 "The ${PREFIX}treaty_{a["id"]}_arg$ agreement is inactive."',
        ]
        i = agreements.index(a) + 1
        rows += [
            f' COLDWAR_ARG_TREATY.{i}.t:0 "{_player_text(a["title"])}"',
            f' COLDWAR_ARG_TREATY.{i}.d:0 "{_player_text(a["description"])} The recipient government may accept or decline the proposed terms."',
            f' COLDWAR_ARG_TREATY.{i}.a:0 "Review the terms"',
        ]
        for side in (a["argentina"], a["recipient"]):
            for key in side.get("modifiers", {}):
                modifiers.setdefault(key, labels.get(key,key.replace("_", " ").capitalize()))
    for key, label in sorted(modifiers.items()):
        inverse=any(x in key for x in ('cost_multiplier','supply_consumption','training_time','interest_rate'))
        fmt='$RIGHT|-=%1$' if inverse else '$RIGHT|+=%1$'
        if key=='interest_rate_multiplier_modifier':fmt='$RIGHT|-=2$ pp'
        rows.append(f' {_modifier_loc(key)}:0 "{label}: {fmt}"')
    return "\n".join(rows)


def build(root: str | Path, design: dict[str, Any]) -> dict[str, str]:
    """Return generated paths and UTF-8 text; caller owns writes and encoding policy."""
    agreements = design.get("agreements")
    if len(agreements or []) != 20:
        raise ValueError(f"Expected the approved 20 Argentina agreements; got {len(agreements or [])}")
    ids = [a["id"] for a in agreements]
    if len(set(ids)) != 20:
        raise ValueError("Agreement IDs must be unique")
    by_id = {a["id"]: a for a in agreements}
    for a in agreements:
        if len(str(a.get("id", ""))) == 0 or not a.get("partner"):
            raise ValueError("Every agreement needs an id and named recipient")
        for side in (a["argentina"], a["recipient"]):
            for field in ("weekly", "credit"):
                value = float(side.get(field, 0))
                if len(_n(value).partition(".")[2]) > 5:
                    raise ValueError(f"{a['id']} {field} exceeds five fractional digits")
        parent = a.get("parent")
        if parent and (parent not in by_id or by_id[parent]["partner"] != a["partner"]):
            raise ValueError(f"{a['id']} must name an existing parent agreement with the same recipient")
    cats, decisions = _decisions(agreements)
    return {
        "common/scripted_effects/COLDWAR_ARG_1970_treaties.txt": _effects(agreements),
        "common/scripted_triggers/COLDWAR_ARG_1970_treaties.txt": _triggers(agreements),
        "common/ideas/COLDWAR_ARG_1970_treaties.txt": _ideas(agreements),
        "common/decisions/COLDWAR_ARG_1970_treaties.txt": decisions,
        "common/decisions/categories/COLDWAR_ARG_1970_treaties.txt": cats,
        "events/COLDWAR_ARG_1970_treaties.txt": _events(agreements),
        "localisation/english/COLDWAR_ARG_1970_treaties_l_english.yml": _localisation(agreements,{k:v for k,v in design['stats'].values()}),
    }


def load_design(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))
