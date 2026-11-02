# IMPERIA COLD WAR — Chile 1970 diplomatic agreements.
"""Build Chile 1970 consent-based diplomatic agreements from the frozen concept JSON."""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).resolve().parent / "approved_design.json"
sys.path.insert(0,str(SOURCE.parent))
from current_design import load_design
PREFIX = "COLDWAR_CHL_"
SANCTION_ARRAYS = ("imp_dip_sanc_on_us", "imp_dip_sanc_by_us", "imp_fin_sanc_on_us", "imp_fin_sanc_by_us", "imp_eco_sanc_on_us", "imp_eco_sanc_by_us", "imp_mil_sanc_on_us", "imp_mil_sanc_by_us")
MODIFIER_LABELS = {
    "production_factory_max_efficiency_factor": ("Production efficiency cap", "+="),
    "resource_export_multiplier_modifier": ("Resource export income", "+="),
    "foreign_influence_defense_modifier": ("Foreign influence defence", "+="),
    "corporate_tax_income_multiplier_modifier": ("Corporate tax income", "+="),
    "trade_opinion_factor": ("Trade opinion", "+="),
    "bureaucracy_cost_multiplier_modifier": ("Bureaucracy costs", "-="),
    "industrial_capacity_factory": ("Factory output", "+="),
    "foreign_influence_modifier": ("Foreign influence", "+="),
    "research_speed_factor": ("Research speed", "+="),
    "health_cost_multiplier_modifier": ("Health costs", "-="),
    "stability_factor": ("Stability", "+="),
    "supply_consumption_factor": ("Supply consumption", "-="),
    "education_cost_multiplier_modifier": ("Education costs", "-="),
}

def n(v):
    return f"{v:.5f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)

def mods_block(mods):
    return " ".join(f"{k} = {n(v)}" for k,v in mods.items())

def varid(a):
    return a["id"].removeprefix(PREFIX).replace("_", "_")

def focus_key(a):
    return "andean_admission" if is_collective(a) else varid(a)

def flag(k, tail):
    return f"{PREFIX}dip_{k}_{tail}"

def root_guard(a):
    partners=a.get("partners") or [a["partner"]]
    return " ".join([f"{PREFIX}is_scenario = yes"]+[f"country_exists = {p}" for p in partners])

def partner(a): return a["partner"]
def participants(a): return ["CHL"] + (a.get("partners") or [a["partner"]])
def is_collective(a): return bool(a.get("partners"))

def pair_clear(a, x, y):
    arr=" ".join(f"is_in_array = {{ array = {ar} value = {y} }}" for ar in SANCTION_ARRAYS)
    arr_y=" ".join(f"is_in_array = {{ array = {ar} value = {x} }}" for ar in SANCTION_ARRAYS)
    return f"""NOT = {{ has_war_with = {y} }} NOT = {{ is_embargoing = {y} }} NOT = {{ OR = {{ {arr} }} }}
{y} = {{ NOT = {{ has_war_with = {x} }} NOT = {{ is_embargoing = {x} }} NOT = {{ OR = {{ {arr_y} }} }} }}"""

def main_clear(a):
    # Keep this validity trigger independently safe when run from daily
    # reconciliation, after a participant has been annexed or otherwise removed.
    exists=" ".join(f"country_exists = {t}" for t in participants(a)[1:])
    if not is_collective(a):
        p=partner(a); return f"{exists} {pair_clear(a,'CHL',p)}"
    parts=participants(a); out=[]
    for i,x in enumerate(parts):
        for y in parts[i+1:]: out.append(f"{x} = {{ {pair_clear(a,x,y)} }}")
    return exists+"\n"+"\n".join(out)

def idea_id(a, tag):
    k=varid(a)
    return f"{PREFIX}dip_{k}_{tag.lower()}"

def deal_trigger(a):
    k=varid(a)
    if not is_collective(a):
        p=partner(a)
        return f"{PREFIX}dip_{k}_clear = {{ {main_clear(a)} }}"
    # Actual membership is separately required on every participant.
    member=" ".join(f"{t} = {{ has_idea = {PREFIX}cartagena_member }}" for t in participants(a))
    # The collective treaty runs only for five actual Cartagena members.
    return f"{PREFIX}dip_{k}_clear = {{ {member} {main_clear(a)} }}"

def accepted_conditions(a):
    k=varid(a)
    if not is_collective(a): return f"has_country_flag = {flag(k,'signed')}"
    return " ".join(f"has_country_flag = {flag(k,'signed_'+t.lower())}" for t in participants(a))

def append_effect_side(lines, tag, side, ideaname, setup=True):
    lines.append(f"{tag} = {{")
    if setup and side.get("setup",0):
        lines.append(f"set_temp_variable = {{ treasury_change = -{n(side['setup'])} }}")
        lines.append("modify_treasury_effect = yes")
    if ideaname:
        lines.append(f"add_ideas = {ideaname}")
        lines.append(f"add_to_variable = {{ {ideaname}_weekly_payment = -{n(round(side['weekly']*1000,5))} tooltip = COLDWAR_CHL_weekly_payment_tt }}")
    lines.append("}")

def preview(a):
    lines=[f"COLDWAR_CHL_preview_{focus_key(a)} = {{", "effect_tooltip = {", "custom_effect_tooltip = COLDWAR_CHL_dip_if_they_accept_tt"]
    sides=[("CHL",a['chile'])]
    if is_collective(a):
        sides += [(t,{**a['recipient'],"spirit":a['recipient_spirits'][t]}) for t in participants(a)[1:]]
    else: sides.append((partner(a),a['recipient']))
    for t,side in sides:
        append_effect_side(lines,t,side,idea_id(a,t),True)
        for stat,value in side.get('modifiers',{}).items():
            if stat not in MODIFIER_LABELS:
                raise ValueError(f"Missing numeric preview label for treaty modifier {stat}")
            lines.append(f"add_to_variable = {{ COLDWAR_CHL_dip_preview_{varid(a)}_{t.lower()}_{stat} = {n(value)} tooltip = COLDWAR_CHL_mod_{stat}_tt }}")
    for b in a.get('buildings',[]):
        lines.append(f"{b['state']} = {{ add_extra_state_shared_building_slots = {b['slots']} add_building_construction = {{ type = {b['type']} level = {b['levels']} instant_build = yes }} }}")
    for r in a.get('research',[]): lines.append(f"{r['country']} = {{ add_tech_bonus = {{ name = {PREFIX}dip_{varid(a)}_{r['country'].lower()} category = {r['category']} bonus = {n(r['bonus'])} uses = {r['uses']} }} }}")
    lines += ["}", "}"]
    return "\n".join(lines)

def mod_num(mods): return " ".join(f"{key} = {n(val)}" for key,val in mods.items())

def percent(value):
    return f"{value*100:+.2f}".rstrip("0").rstrip(".")+"%"

def accepted_setup(a):
    """Return the complete one-time transaction, guarded before its first mutation."""
    k=varid(a); lines=[]
    if not is_collective(a):
        p=partner(a)
        lines += [f"set_temp_variable = {{ treasury_change = -{n(a['chile']['setup'])} }}", "modify_treasury_effect = yes", f"{p} = {{ set_temp_variable = {{ treasury_change = -{n(a['recipient']['setup'])} }} modify_treasury_effect = yes }}"]
        for b in a.get('buildings',[]):
            lines.append(f"{b['state']} = {{ add_extra_state_shared_building_slots = {b['levels']} add_building_construction = {{ type = {b['type']} level = {b['levels']} instant_build = yes }} }}")
        for r in a.get('research',[]):
            lines.append(f"{r['country']} = {{ add_tech_bonus = {{ name = {PREFIX}dip_{k}_{r['country'].lower()} category = {r['category']} bonus = {n(r['bonus'])} uses = {r['uses']} }} }}")
        lines += [f"set_country_flag = {flag(k,'signed')}", f"{p} = {{ set_country_flag = {flag(k,'signed')} clr_country_flag = {flag(k,'pending')} }}", f"clr_country_flag = {flag(k,'pending')}"]
    else:
        lines += [f"set_temp_variable = {{ treasury_change = -{n(a['chile']['setup'])} }}", "modify_treasury_effect = yes"]
        for t in participants(a)[1:]:
            lines.append(f"{t} = {{ set_temp_variable = {{ treasury_change = -{n(a['recipient']['setup'])} }} modify_treasury_effect = yes }}")
        for t in participants(a):
            lines.append(f"set_country_flag = {flag(k,'signed_'+t.lower())}")
            lines.append(f"{t} = {{ set_country_flag = {flag(k,'signed_'+t.lower())} clr_country_flag = {flag(k,'pending')} }}")
        lines += [f"set_country_flag = {flag(k,'signed')}", f"clr_country_flag = {flag(k,'pending')}"]
    lines += [f"set_country_flag = {flag(k,'paid')}", f"clr_country_flag = {flag(k,'awaiting')}", "COLDWAR_CHL_diplomacy_daily = yes", f"country_event = {{ id = COLDWAR_CHL_DIP.{104 if is_collective(a) else 100} }}"]
    guard=["tag = CHL", f"NOT = {{ has_country_flag = {flag(k,'paid')} }}", f"has_country_flag = {flag(k,'pending')}", f"has_country_flag = {flag(k,'awaiting')}", f"{PREFIX}dip_{k}_clear = yes"]
    if is_collective(a):
        guard += [f"has_country_flag = {flag(k,'ratified_'+t.lower())}" for t in participants(a)[1:]]
        guard += [f"country_exists = {t}" for t in participants(a)]
    else:
        p=partner(a)
        guard += [f"country_exists = {p}", f"{p} = {{ has_country_flag = {flag(k,'pending')} }}", asset_guards(a)]
    return f"COLDWAR_CHL_dip_execute_{k} = {{ if = {{ limit = {{ {' '.join(guard)} }} {' '.join(lines)} }} }}"

def can_offer_trigger(a):
    k=varid(a)
    relation=f"custom_trigger_tooltip = {{ tooltip = {PREFIX}dip_{k}_relations_tt {PREFIX}dip_{k}_clear = yes }}"
    checks=[root_guard(a), f"NOT = {{ has_country_flag = {flag(k,'signed')} }}",f"NOT = {{ has_country_flag = {flag(k,'pending')} }}",f"NOT = {{ has_country_flag = {flag(k,'cooldown')} }}",relation]
    checks.append(asset_guards(a))
    if is_collective(a):
        checks += [f"{t} = {{ has_idea = {PREFIX}cartagena_member }}" for t in participants(a)]
        checks += [f"{t} = {{ NOT = {{ has_country_flag = {flag(k,'signed_'+t.lower())} }} }}" for t in participants(a)]
    if k=="cuba_clinics": checks.append("custom_trigger_tooltip = { tooltip = COLDWAR_CHL_cuba_relations_tt has_opinion = { target = CUB value > -25 } }")
    return "\n".join(checks)

def asset_guards(a):
    return " ".join(f"{PREFIX}can_build_{b['state']}_{b['type']}_{b['levels']} = yes" for b in a.get("buildings", []))

def build():
    data=load_design(SOURCE)
    agreements=data['agreements']
    effects=["# IMPERIA COLD WAR — Chile 1970 diplomacy effects."]
    triggers=["# IMPERIA COLD WAR — Chile 1970 diplomacy triggers."]
    ideas=["# IMPERIA COLD WAR — Chile 1970 standing agreement ideas.","ideas = {", " country = {"]
    decision_entries=[]
    offer_entries=[]
    categories=["# IMPERIA COLD WAR — Chile 1970 treaty decision categories.","COLDWAR_CHL_diplomacy_offers = { allowed = { tag = CHL COLDWAR_CHL_is_scenario = yes } icon = generic_foreign_policy priority = 209 visible = { has_country_flag = COLDWAR_CHL_diplomacy_receipt } }"]
    response_vis=[]
    loc=["l_english:","# IMPERIA COLD WAR — Chile 1970 diplomatic agreement text."," COLDWAR_CHL_dip_if_they_accept_tt:0 \"If they accept:\"", " COLDWAR_CHL_weekly_payment_tt:0 \"Recurring weekly payment: $RIGHT|+=3$ million per week\"", " COLDWAR_CHL_cuba_relations_tt:0 \"Relations with Cuba exceed -25.\"", " COLDWAR_CHL_cuba_relations_tt_NOT:0 \"Relations with Cuba do not exceed -25.\""]
    # reusable pair triggers
    loc += [' COLDWAR_CHL_wait_over_tt:0 "The 180-day diplomatic waiting period has ended."',' COLDWAR_CHL_wait_over_tt_NOT:0 "The 180-day diplomatic waiting period is still in effect."']
    for a in agreements:
        k=varid(a)
        text=("All five participants are at peace, with no mutual embargoes or sanctions." if is_collective(a) else f"At peace with [{partner(a)}.GetNameDef], with no mutual embargoes or sanctions.")
        inverse=("A participant is absent, outside the agreement, at war, embargoed or sanctioned." if is_collective(a) else f"Relations with [{partner(a)}.GetNameDef] do not meet the peace, embargo and sanctions requirements.")
        loc += [f' {PREFIX}dip_{k}_relations_tt:0 '+json.dumps(text),f' {PREFIX}dip_{k}_relations_tt_NOT:0 '+json.dumps(inverse)]
        triggers.append(deal_trigger(a))
        triggers.append(f"COLDWAR_CHL_can_offer_{focus_key(a)} = {{ {can_offer_trigger(a)} }}")
        # Focus reward opens a persistent awaiting-reply record and timed 90-day decisions.
        effects.append(preview(a))
        effects.append(accepted_setup(a))
        event_number = len([x for x in agreements[:agreements.index(a)] if not is_collective(x)]) + 1
        p=partner(a)
        effects.append(f"""COLDWAR_CHL_offer_{focus_key(a)} = {{
if = {{ limit = {{ COLDWAR_CHL_can_offer_{focus_key(a)} = yes }}
set_country_flag = COLDWAR_CHL_diplomacy_receipt
set_country_flag = {flag(k,'receipt')}
set_country_flag = {flag(k,'awaiting')}
set_country_flag = {{ flag = {flag(k,'pending')} value = 1 days = 90 }}
""" + ("\n".join(f"clr_country_flag = {flag(k,'ratified_'+t.lower())}" for t in participants(a)[1:])+"\n" if is_collective(a) else "") +
("\n".join(f"{t} = {{ set_country_flag = {{ flag = {flag(k,'pending')} value = 1 days = 90 }} country_event = {{ id = COLDWAR_CHL_DIP.{20+i} }} }}" for i,t in enumerate(participants(a)[1:])) if is_collective(a) else f"{p} = {{ set_country_flag = {{ flag = {flag(k,'pending')} value = 1 days = 90 }} country_event = {{ id = COLDWAR_CHL_DIP.{event_number} }} }}") + "\n}\n}")
        response_vis.append(f"has_country_flag = {flag(k,'pending')}")
        if not is_collective(a):
            accept=f"COLDWAR_CHL_DIP_accept_{k}"; refuse=f"COLDWAR_CHL_DIP_refuse_{k}"
            accept_guard=f"tag = {p} has_country_flag = {flag(k,'pending')} CHL = {{ has_country_flag = {flag(k,'pending')} has_country_flag = {flag(k,'awaiting')} COLDWAR_CHL_dip_{k}_clear = yes {asset_guards(a)} NOT = {{ has_country_flag = {flag(k,'paid')} }} }}"
            effects.append(f"COLDWAR_CHL_dip_accept_{k} = {{ if = {{ limit = {{ {accept_guard} }} CHL = {{ COLDWAR_CHL_dip_execute_{k} = yes }} if = {{ limit = {{ CHL = {{ has_country_flag = {flag(k,'signed')} }} }} clr_country_flag = {flag(k,'pending')} }} }} }}")
            effects.append(f"COLDWAR_CHL_dip_refuse_{k} = {{ if = {{ limit = {{ tag = {p} has_country_flag = {flag(k,'pending')} CHL = {{ has_country_flag = {flag(k,'pending')} has_country_flag = {flag(k,'awaiting')} }} }} clr_country_flag = {flag(k,'pending')} set_country_flag = {{ flag = {flag(k,'cooldown')} value = 1 days = 180 }} CHL = {{ clr_country_flag = {flag(k,'pending')} clr_country_flag = {flag(k,'awaiting')} set_country_flag = {{ flag = {flag(k,'cooldown')} value = 1 days = 180 }} COLDWAR_CHL_diplomacy_daily = yes country_event = {{ id = COLDWAR_CHL_DIP.101 }} }} }} }}")
            decisions=f"""{accept} = {{ icon = generic_political_discourse visible = {{ tag = {p} has_country_flag = {flag(k,'pending')} }} available = {{ tag = {p} has_country_flag = {flag(k,'pending')} CHL = {{ has_country_flag = {flag(k,'pending')} has_country_flag = {flag(k,'awaiting')} COLDWAR_CHL_dip_{k}_clear = yes {asset_guards(a)} NOT = {{ has_country_flag = {flag(k,'paid')} }} }} }} cost = 0 days_remove = 90 complete_effect = {{ effect_tooltip = {{ COLDWAR_CHL_preview_{focus_key(a)} = yes }} hidden_effect = {{ COLDWAR_CHL_dip_accept_{k} = yes }} }} ai_will_do = {{ base = 0 }} }}
{refuse} = {{ icon = generic_political_discourse visible = {{ tag = {p} has_country_flag = {flag(k,'pending')} }} available = {{ tag = {p} has_country_flag = {flag(k,'pending')} CHL = {{ has_country_flag = {flag(k,'pending')} has_country_flag = {flag(k,'awaiting')} }} }} cost = 0 days_remove = 90 complete_effect = {{ COLDWAR_CHL_dip_refuse_{k} = yes }} ai_will_do = {{ base = 0 }} }}"""
            decision_entries.append(decisions)
        else:
            # Every vote is written only by that named member's guarded helper.
            for p in participants(a)[1:]:
                acc=f"COLDWAR_CHL_DIP_accept_{k}_{p.lower()}"; ref=f"COLDWAR_CHL_DIP_refuse_{k}_{p.lower()}"
                accept_guard=f"tag = {p} has_country_flag = {flag(k,'pending')} CHL = {{ has_country_flag = {flag(k,'pending')} has_country_flag = {flag(k,'awaiting')} COLDWAR_CHL_dip_{k}_clear = yes NOT = {{ has_country_flag = {flag(k,'ratified_'+p.lower())} }} NOT = {{ has_country_flag = {flag(k,'paid')} }} }}"
                others=" ".join(f"has_country_flag = {flag(k,'ratified_'+t.lower())}" for t in participants(a)[1:] if t!=p)
                effects.append(f"COLDWAR_CHL_dip_accept_{k}_{p.lower()} = {{ if = {{ limit = {{ {accept_guard} }} CHL = {{ set_country_flag = {flag(k,'ratified_'+p.lower())} if = {{ limit = {{ {others} }} COLDWAR_CHL_dip_execute_{k} = yes }} else = {{ country_event = {{ id = COLDWAR_CHL_DIP.102 }} }} }} clr_country_flag = {flag(k,'pending')} }} }}")
                cancel=" ".join(f"{t} = {{ clr_country_flag = {flag(k,'pending')} set_country_flag = {{ flag = {flag(k,'cooldown')} value = 1 days = 180 }} }}" for t in participants(a))
                cancel += " CHL = { clr_country_flag = "+flag(k,'awaiting')+" " + " ".join(f"clr_country_flag = {flag(k,'ratified_'+t.lower())}" for t in participants(a)[1:]) + " COLDWAR_CHL_diplomacy_daily = yes country_event = { id = COLDWAR_CHL_DIP.101 } }"
                effects.append(f"COLDWAR_CHL_dip_refuse_{k}_{p.lower()} = {{ if = {{ limit = {{ tag = {p} has_country_flag = {flag(k,'pending')} CHL = {{ has_country_flag = {flag(k,'pending')} has_country_flag = {flag(k,'awaiting')} }} }} {cancel} }} }}")
                decisions=f"""{acc} = {{ icon = generic_political_discourse visible = {{ tag = {p} has_country_flag = {flag(k,'pending')} }} available = {{ tag = {p} has_country_flag = {flag(k,'pending')} CHL = {{ has_country_flag = {flag(k,'pending')} has_country_flag = {flag(k,'awaiting')} COLDWAR_CHL_dip_{k}_clear = yes NOT = {{ has_country_flag = {flag(k,'ratified_'+p.lower())} }} NOT = {{ has_country_flag = {flag(k,'paid')} }} }} }} cost = 0 days_remove = 90 complete_effect = {{ effect_tooltip = {{ COLDWAR_CHL_preview_{focus_key(a)} = yes }} hidden_effect = {{ COLDWAR_CHL_dip_accept_{k}_{p.lower()} = yes }} }} ai_will_do = {{ base = 0 }} }}
{ref} = {{ icon = generic_political_discourse visible = {{ tag = {p} has_country_flag = {flag(k,'pending')} }} available = {{ tag = {p} has_country_flag = {flag(k,'pending')} CHL = {{ has_country_flag = {flag(k,'pending')} has_country_flag = {flag(k,'awaiting')} }} }} cost = 0 days_remove = 90 complete_effect = {{ COLDWAR_CHL_dip_refuse_{k}_{p.lower()} = yes }} ai_will_do = {{ base = 0 }} }}"""
                decision_entries.append(decisions)
        offer_entries.append(f"COLDWAR_CHL_resubmit_{k} = {{ icon = generic_political_discourse visible = {{ has_country_flag = {flag(k,'receipt')} NOT = {{ has_country_flag = {flag(k,'signed')} }} NOT = {{ has_country_flag = {flag(k,'pending')} }} NOT = {{ has_country_flag = {flag(k,'awaiting')} }} }} available = {{ has_country_flag = {flag(k,'receipt')} NOT = {{ has_country_flag = {flag(k,'awaiting')} }} NOT = {{ has_country_flag = {flag(k,'pending')} }} custom_trigger_tooltip = {{ tooltip = COLDWAR_CHL_wait_over_tt NOT = {{ has_country_flag = {flag(k,'cooldown')} }} }} NOT = {{ has_country_flag = {flag(k,'signed')} }} COLDWAR_CHL_can_offer_{focus_key(a)} = yes }} cost = 0 days_re_enable = 1 complete_effect = {{ COLDWAR_CHL_offer_{focus_key(a)} = yes }} ai_will_do = {{ base = 0 }} }}")
        # paired and collective static ideas
        sides=[("CHL",a['chile'])]
        if is_collective(a): sides += [(t,{**a['recipient'],"spirit":a['recipient_spirits'][t]}) for t in participants(a)[1:]]
        else: sides += [(partner(a),a['recipient'])]
        for t,side in sides:
            iid=idea_id(a,t)
            ideas.append(f"  {iid} = {{ picture = international_treaty allowed = {{ always = no }} allowed_civil_war = {{ always = yes }} modifier = {{ {mod_num(side['modifiers'])} }} }}")
            label=side['spirit']
            detail=a['description']
            loc += [f" {iid}:0 \"{label}\"",f" {iid}_desc:0 \"{detail}\""]
        # Variables are reset/rebuilt on daily invocation; only active valid pairs carry weekly expense and ideas.
        if not is_collective(a):
            p=partner(a); cond=f"has_country_flag = {flag(k,'signed')} {p} = {{ has_country_flag = {flag(k,'signed')} }} COLDWAR_CHL_dip_{k}_clear = yes"
            reconciliation=f"""if = {{ limit = {{ {cond} }}
if = {{ limit = {{ NOT = {{ has_idea = {idea_id(a,'CHL')} }} }} add_ideas = {idea_id(a,'CHL')} }}
{p} = {{ if = {{ limit = {{ NOT = {{ has_idea = {idea_id(a,p)} }} }} add_ideas = {idea_id(a,p)} }} add_to_variable = {{ COLDWAR_CHL_diplomacy_weekly = {n(a['recipient']['weekly'])} }} }}
add_to_variable = {{ COLDWAR_CHL_diplomacy_weekly = {n(a['chile']['weekly'])} }}
}} else = {{ remove_ideas = {idea_id(a,'CHL')} {p} = {{ remove_ideas = {idea_id(a,p)} }} }}"""
        else:
            cond=f"{accepted_conditions(a)} {PREFIX}dip_{k}_clear = yes"
            body=[]
            for t,side in sides:
                body += [f"{t} = {{ if = {{ limit = {{ NOT = {{ has_idea = {idea_id(a,t)} }} }} add_ideas = {idea_id(a,t)} }} add_to_variable = {{ COLDWAR_CHL_diplomacy_weekly = {n(side['weekly'])} }} }}"]
            off=" ".join(f"{t} = {{ remove_ideas = {idea_id(a,t)} }}" for t,_ in sides)
            reconciliation=f"if = {{ limit = {{ {cond} }} {' '.join(body)} }} else = {{ {off} }}"
        effects.append(f"COLDWAR_CHL_dip_sync_{k} = {{ {reconciliation} }}")
    # Daily update runs in CHL scope. Clear all per-country costs then re-add only active treaty flows.
    daily=["COLDWAR_CHL_diplomacy_daily = {", "every_country = { set_variable = { COLDWAR_CHL_diplomacy_weekly = 0 } }", "if = { limit = { COLDWAR_CHL_is_scenario = yes }"]
    for a in agreements: daily.append(f"COLDWAR_CHL_dip_sync_{varid(a)} = yes")
    # Convert expired pending offers into 180-day resubmission wait. No setup transaction is replayed.
    for a in agreements:
        k=varid(a)
        if is_collective(a):
            cleanup=" ".join(f"clr_country_flag = {flag(k,'ratified_'+t.lower())}" for t in participants(a)[1:])
            cleanup += " " + " ".join(f"{t} = {{ clr_country_flag = {flag(k,'pending')} set_country_flag = {{ flag = {flag(k,'cooldown')} value = 1 days = 180 }} }}" for t in participants(a))
        else:
            cleanup=f"{partner(a)} = {{ clr_country_flag = {flag(k,'pending')} set_country_flag = {{ flag = {flag(k,'cooldown')} value = 1 days = 180 }} }}"
        daily.append(f"if = {{ limit = {{ has_country_flag = {flag(k,'awaiting')} NOT = {{ has_country_flag = {flag(k,'pending')} }} NOT = {{ has_country_flag = {flag(k,'cooldown')} }} NOT = {{ has_country_flag = {flag(k,'signed')} }} }} set_country_flag = {{ flag = {flag(k,'cooldown')} value = 1 days = 180 }} clr_country_flag = {flag(k,'awaiting')} {cleanup} country_event = {{ id = COLDWAR_CHL_DIP.103 }} }}")
    daily += ["}", "}"]
    # Correct stable, scenario-wide receipt and cooldown transaction uses authorization receipt per offer.
    # A focus's offer effect owns that receipt; cooldown starts at refusal/expiry.
    effects.extend(daily)
    cleanup_ideas=[]
    for a in agreements:
        for t in participants(a): cleanup_ideas.append(f"remove_ideas = {idea_id(a,t)}")
    # Clear active costs, spirits and orphaned replies once per Chile-presence
    # transition. Keep signed and paid receipts so a returning Chile can restore
    # standing agreements without replaying setup costs or one-time assets.
    gone_cleanup=["set_variable = { COLDWAR_CHL_diplomacy_weekly = 0 }", *cleanup_ideas]
    for a in agreements:
        k=varid(a)
        gone_cleanup += [f"clr_country_flag = {flag(k,'pending')}", f"clr_country_flag = {flag(k,'awaiting')}"]
        if is_collective(a):
            gone_cleanup += [f"clr_country_flag = {flag(k,'ratified_'+t.lower())}" for t in participants(a)[1:]]
    effects.append(
        "COLDWAR_CHL_diplomacy_world_daily = {\n"
        "if = { limit = { country_exists = CHL } clr_global_flag = COLDWAR_CHL_diplomacy_chl_absent_cleaned CHL = { COLDWAR_CHL_diplomacy_daily = yes } }\n"
        "else = { if = { limit = { NOT = { has_global_flag = COLDWAR_CHL_diplomacy_chl_absent_cleaned } } "
        "set_global_flag = COLDWAR_CHL_diplomacy_chl_absent_cleaned every_country = { "
        + " ".join(gone_cleanup)
        + " } } }\n}"
    )
    # Response visibility/category
    categories.append("COLDWAR_CHL_diplomacy_responses = { allowed = { NOT = { tag = CHL } } icon = generic_foreign_policy priority = 212 visible = { OR = { " + " ".join(response_vis) + " } } }")
    # complete player-facing previews in focus tooltip are provided by effect_tooltip API.
    for a in agreements:
        k=varid(a)
        loc += [f" COLDWAR_CHL_dip_{k}_name:0 \"{a['title']}\"",f" COLDWAR_CHL_dip_{k}_desc:0 \"{a['description']}\"",f" COLDWAR_CHL_DIP_{k}_title:0 \"{a['title']}\"",f" COLDWAR_CHL_DIP_{k}_desc:0 \"{a['description']}\"",f" COLDWAR_CHL_DIP_{k}_accept:0 \"Ratify the agreement\"",f" COLDWAR_CHL_DIP_{k}_refuse:0 \"Decline the agreement\""]
    loc += [" COLDWAR_CHL_diplomacy_offers:0 \"Chile: Diplomatic Agreements\"", " COLDWAR_CHL_diplomacy_responses:0 \"Treaty Proposals\""]
    for a in agreements:
        k=varid(a)
        for p in [a['partner']] if not is_collective(a) else a['partners']:
            loc += [f" COLDWAR_CHL_DIP_accept_{k}{('_'+p.lower()) if is_collective(a) else ''}:0 \"Ratify: {a['title']}\"",f" COLDWAR_CHL_DIP_refuse_{k}{('_'+p.lower()) if is_collective(a) else ''}:0 \"Decline: {a['title']}\""]
        loc.append(f" COLDWAR_CHL_resubmit_{k}:0 \"Resubmit: {a['title']}\"")
        loc.append(f" COLDWAR_CHL_resubmit_{k}_desc:0 \"A declined or unanswered proposal may be resubmitted after a 180-day waiting period.\"")
    events=["# IMPERIA COLD WAR — Chile 1970 treaty notices.","add_namespace = COLDWAR_CHL_DIP"]
    for i,a in enumerate([x for x in agreements if not is_collective(x)],1):
        k=varid(a)
        loc += [f" COLDWAR_CHL_DIP.{i}.t:0 \"{a['title']}\"",f" COLDWAR_CHL_DIP.{i}.d:0 \"{a['description']}\"",f" COLDWAR_CHL_DIP.{i}.a:0 \"Review recipient decisions\""]
        events.append(f"country_event = {{ id = COLDWAR_CHL_DIP.{i} title = COLDWAR_CHL_DIP.{i}.t desc = COLDWAR_CHL_DIP.{i}.d picture = GFX_treaty is_triggered_only = yes option = {{ name = COLDWAR_CHL_DIP.{i}.a effect_tooltip = {{ COLDWAR_CHL_preview_{focus_key(a)} = yes }} }} }}")
    collective=next(a for a in agreements if is_collective(a))
    for i,tag in enumerate(participants(collective)[1:],20):
        loc += [f" COLDWAR_CHL_DIP.{i}.t:0 \"{collective['title']}\"",f" COLDWAR_CHL_DIP.{i}.d:0 \"{collective['description']}\"",f" COLDWAR_CHL_DIP.{i}.a:0 \"Review recipient decisions\""]
        events.append(f"country_event = {{ id = COLDWAR_CHL_DIP.{i} title = COLDWAR_CHL_DIP.{i}.t desc = COLDWAR_CHL_DIP.{i}.d picture = GFX_treaty is_triggered_only = yes option = {{ name = COLDWAR_CHL_DIP.{i}.a effect_tooltip = {{ COLDWAR_CHL_preview_{focus_key(collective)} = yes }} }} }}")
    events += ["country_event = { id = COLDWAR_CHL_DIP.100 title = COLDWAR_CHL_DIP.result.t desc = COLDWAR_CHL_DIP.accepted.d picture = GFX_treaty is_triggered_only = yes option = { name = COLDWAR_CHL_DIP.result.a } }", "country_event = { id = COLDWAR_CHL_DIP.101 title = COLDWAR_CHL_DIP.result.t desc = COLDWAR_CHL_DIP.refused.d picture = GFX_treaty is_triggered_only = yes option = { name = COLDWAR_CHL_DIP.result.a } }", "country_event = { id = COLDWAR_CHL_DIP.102 title = COLDWAR_CHL_DIP.result.t desc = COLDWAR_CHL_DIP.ratified.d picture = GFX_treaty is_triggered_only = yes option = { name = COLDWAR_CHL_DIP.result.a } }", "country_event = { id = COLDWAR_CHL_DIP.103 title = COLDWAR_CHL_DIP.result.t desc = COLDWAR_CHL_DIP.expired.d picture = GFX_treaty is_triggered_only = yes option = { name = COLDWAR_CHL_DIP.result.a } }", "country_event = { id = COLDWAR_CHL_DIP.104 title = COLDWAR_CHL_DIP.result.t desc = COLDWAR_CHL_DIP.finalized.d picture = GFX_treaty is_triggered_only = yes option = { name = COLDWAR_CHL_DIP.result.a } }"]
    loc += [" COLDWAR_CHL_DIP.result.t:0 \"Agreement response\"", " COLDWAR_CHL_DIP.accepted.d:0 \"The recipient has ratified the standing agreement.\"", " COLDWAR_CHL_DIP.refused.d:0 \"The recipient declined the agreement. It may be resubmitted after the waiting period.\"", " COLDWAR_CHL_DIP.ratified.d:0 \"A member has ratified the Andean protocol. The remaining participants must also ratify before it takes effect.\"", " COLDWAR_CHL_DIP.expired.d:0 \"The proposal expired without ratification. It may be resubmitted after the waiting period.\"", " COLDWAR_CHL_DIP.finalized.d:0 \"All five participants have ratified the Andean protocol. Its standing terms are now in force.\"", " COLDWAR_CHL_DIP.result.a:0 \"Acknowledge\""]
    # Files emitted exactly within owned namespace.
    return {
      "common/scripted_effects/COLDWAR_CHL_1970_diplomacy.txt": "\n\n".join(effects)+"\n",
      "common/scripted_triggers/COLDWAR_CHL_1970_diplomacy.txt": "\n\n".join(["# IMPERIA COLD WAR — Chile 1970 treaty offer and validity triggers."]+triggers)+"\n",
      "common/decisions/COLDWAR_CHL_1970_diplomacy.txt": "# IMPERIA COLD WAR — Chile 1970 treaty consent decisions.\nCOLDWAR_CHL_diplomacy_offers = {\n"+"\n".join(offer_entries)+"\n}\nCOLDWAR_CHL_diplomacy_responses = {\n"+"\n".join(decision_entries)+"\n}\n",
      "common/decisions/categories/COLDWAR_CHL_1970_diplomacy.txt": "\n".join(categories)+"\n",
      "common/ideas/COLDWAR_CHL_1970_diplomacy.txt": "\n".join(ideas+[" }", "}"])+"\n",
      "events/COLDWAR_CHL_1970_diplomacy.txt": "\n".join(events)+"\n",
      "localisation/english/COLDWAR_CHL_1970_diplomacy_l_english.yml": "\n".join(loc)+"\n",
    }

if __name__ == "__main__":
    for rel, text in build().items():
        path=ROOT/rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8-sig" if rel.endswith(".yml") else "utf-8")
        print(rel)
