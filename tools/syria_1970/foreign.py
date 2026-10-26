# IMPERIA CW — Cold War: Syria 1970 content imported from quaZa.
"""Syria 1970: funded operations and recipient-controlled foreign contracts.

Called by the country compiler; this module owns only COLDWAR_SYR_foreign files.
Amounts passed to MD treasury/debt effects are billions of current dollars.
"""
from pathlib import Path
import importlib.util
import json
import re

PREFIX = "COLDWAR_SYR_"
DOMESTIC = {
    "officer_bargain", "cabinet_mediation", "corrective_vote", "succession_crisis",
    "guard_bargain", "front_offer", "citizenship_review", "arab_belt",
    "kurdish_coalition", "enterprise_audit", "tabqa_resettle", "irrigation_trial",
    "drought", "budget_review", "unrest_mediation", "security_response",
    "reopen_registers", "national_pact", "governing_mandate", "military_transfer",
}


def install(root, data):
    root = Path(root)
    loc, effects, triggers, events, decisions, ideas = {}, [], [], [], [], []
    event_bodies = {}
    foreign_outcomes = json.loads((Path(__file__).resolve().parent/'foreign_option_outcomes.json').read_text(encoding='utf-8'))
    spec = importlib.util.spec_from_file_location("syria_foreign_script_format", root / "tools/israel_1970/script_format.py")
    formatter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(formatter)

    def write(path, text, bom=False):
        p = root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        # IMPERIA CW — Cold War: Country output markers survive later rebuilds.
        marker = '# IMPERIA CW \u2014 Cold War: Syria 1970 content imported from quaZa.\n'
        if p.name.startswith('COLDWAR_SYR') and 'IMPERIA CW' not in text:
            text = text.replace('l_english:\n', 'l_english:\n'+marker, 1) if p.suffix == '.yml' else marker+text
        if p.suffix == ".txt":
            # A completed focus must have implemented its programme before follow-up contracts.
            text = re.sub(r"has_completed_focus\s*=\s*(COLDWAR_SYR_[A-Za-z0-9_]+)", r"has_country_flag = \1_implemented", text)
            text = formatter.format_script(text)
        p.write_text(text.rstrip() + "\n", encoding="utf-8-sig" if bom else "utf-8")

    def block(name, body):
        return name + " = {\n" + "\n".join("\t" + x for x in body.strip().splitlines()) + "\n}\n"

    def flag(name):
        return PREFIX + name

    def pay(amount):
        return f"set_temp_variable = {{ treasury_change = {amount} }}\nmodify_treasury_effect = yes"

    def cost_pay(var):
        return f"set_temp_variable = {{ treasury_change = {var} }}\nmultiply_temp_variable = {{ treasury_change = -1 }}\nmodify_treasury_effect = yes"

    def timed(idea, days):
        return f"add_timed_idea = {{ idea = {flag(idea)} days = {days} }}"

    def idea(name, title, description, modifiers, cancel=""):
        key = flag(name)
        loc[key], loc[key + "_desc"] = title, description
        body = "picture = political_establishment\nmodifier = {\n" + "\n".join(f"\t{k} = {v}" for k, v in modifiers.items()) + "\n}"
        if cancel:
            body += "\ncancel = { " + cancel + " }"
        ideas.append(block(key, body))

    def native_preview(code):
        material = {'modify_treasury_effect', 'modify_debt_effect', 'add_stability',
                    'add_war_support', 'add_political_power', 'add_ideas',
                    'remove_ideas', 'add_timed_idea'}

        def select(items):
            selected = []
            for name, operator, value in items:
                if name in material:
                    selected.append((name, operator, value))
                elif name in ('set_temp_variable', 'multiply_temp_variable'):
                    if isinstance(value, list) and value and value[0][0] in ('treasury_change', 'debt_change'):
                        selected.append((name, operator, value))
                elif name == 'limit':
                    selected.append((name, operator, [('hidden_trigger', '=', value)]))
                elif isinstance(value, list):
                    nested = select(value)
                    if name == 'hidden_effect':
                        selected.extend(nested)
                    elif nested or name in ('if', 'else_if', 'else'):
                        selected.append((name, operator, nested))
            return selected

        def emit(items):
            return '\n'.join(name if operator is None else name+' '+operator+' '+('{\n'+emit(value)+'\n}' if isinstance(value, list) else value) for name, operator, value in items)

        return emit(select(formatter.read(code)))

    def event(number, title, description, options, trigger="original_tag = SYR IMP_is_1970_scenario = yes", namespace="COLDWAR_SYR_WAR", immediate="", hidden=False):
        key = f"{namespace}.{number}"
        loc[key + ".t"], loc[key + ".d"] = title, description
        body = f"id = {key}\ntitle = {key}.t\ndesc = {key}.d\npicture = GFX_syrian_arab_army\nis_triggered_only = yes\ntimeout_days = 90\ntrigger = {{ {trigger} }}"
        if hidden:
            body += "\nhidden = yes"
        if immediate:
            body += "\nimmediate = {\n" + immediate + "\n}"
        # Inactive recipients default to refusing an offer, never to spending funds.
        safe = ("Decline", "Withdraw", "Cancel", "Defer", "Hold", "Return", "Stand down")
        options = sorted(options, key=lambda o: 0 if o[0].startswith(safe) else 1)
        for i, (label, code, condition) in enumerate(options):
            option_key = key + ".option_" + chr(97 + i)
            loc[option_key] = label
            assert option_key in foreign_outcomes, ('Unexplained foreign event choice', option_key)
            loc[option_key+'_outcome_tt'] = foreign_outcomes[option_key]
            obody = f"name = {option_key}\nai_chance = {{ base = {50 if i == 0 else 25} }}"
            if condition:
                obody += "\ntrigger = { " + condition + " }"
            if code:
                preview = native_preview(code)
                if preview:
                    obody += '\neffect_tooltip = {\n'+preview+'\n}'
                # A popup may remain open while money, war or the matching offer changes.
                obody += "\nhidden_effect = { if = {\nlimit = { " + trigger + " " + condition + " }\n" + code + "\n}\nelse = { custom_effect_tooltip = COLDWAR_SYR_offer_invalid_tt } }"
            obody += '\ncustom_effect_tooltip = '+option_key+'_outcome_tt'
            body += "\n" + block("option", obody)
        emitted = block("country_event", body)
        if key in event_bodies:
            if event_bodies[key] != emitted:
                raise ValueError("Conflicting Syrian event definitions: " + key)
            return
        event_bodies[key] = emitted
        events.append(emitted)

    goal_valid = "country_exists = ISR\nNOT = { is_in_faction_with = ISR }\nISR = { controls_state = 587 }\nNOT = { controls_state = 587 }"
    campaign_valid = goal_valid + "\nOR = { has_war_with = ISR has_wargoal_against = ISR }"
    triggers.append(block("COLDWAR_SYR_golan_objective_unresolved", goal_valid))
    triggers.append(block("COLDWAR_SYR_campaign_is_valid", campaign_valid))
    triggers.append(block("COLDWAR_SYR_training_can_request", """
country_exists = SOV
mdcw_cw_is_active = yes
has_country_flag = mdcw_cw_initialized
NOT = { has_war_with = SOV }
NOT = { has_country_flag = COLDWAR_SYR_training_request_pending }
SOV = {
    has_country_flag = mdcw_cw_initialized
    NOT = { check_variable = { mdcw_cw_p6_size@SYR > 0 } }
    NOT = { check_variable = { mdcw_cw_pend_type@SYR > 0 } }
}
"""))
    effects.append(block("COLDWAR_SYR_create_limited_wargoal", """
if = {
    limit = {
        COLDWAR_SYR_golan_objective_unresolved = yes
        NOT = { has_war_with = ISR }
        NOT = { has_wargoal_against = ISR }
    }
    set_temp_variable = { wargoal_on = ISR }
    set_temp_variable = { wargoal_by = THIS.id }
    if = {
        limit = { ISR = { owns_state = 587 } }
        set_temp_variable = { wargoal_type = 0 }
        add_threat_from_wargoal_effect = yes
        create_wargoal = { type = take_state_focus target = ISR generator = { 587 } expire = 365 }
    }
    else = {
        set_temp_variable = { wargoal_type = 2 }
        add_threat_from_wargoal_effect = yes
        create_wargoal = { type = annex_everything target = ISR expire = 365 }
    }
    set_country_flag = COLDWAR_SYR_goal_granted
    custom_effect_tooltip = COLDWAR_SYR_goal_scope_tt
}
"""))
    loc["COLDWAR_SYR_goal_scope_tt"] = "War goal against Israel: 365 days. Targets the Golan when Israel owns it. An Israeli occupation of Syrian-owned Golan instead permits a wider conquest and annexation in the peace settlement. War is declared manually."
    loc["COLDWAR_SYR_offer_invalid_tt"] = "The proposed terms are no longer available. No funds are committed and no agreement takes effect."
    effects.append(block("COLDWAR_SYR_update_operation_costs", "\n".join(
        f"set_variable = {{ {flag('cost_' + name + '_percent_gdp')} = gdp_total }}\nmultiply_variable = {{ {flag('cost_' + name + '_percent_gdp')} = {amount} }}"
        for name, amount in (("quarter", .0025), ("half", .005), ("three_quarter", .0075)))))
    operation_ideas = ["war_reserve_readiness", "war_supply_preparation", "war_joint_planning", "war_medical_service", "war_short_window", "war_sustained_window"]
    cleanup = "\n".join("remove_ideas = " + flag(k) for k in operation_ideas) + "\nclr_country_flag = COLDWAR_SYR_operational_mandate\nclr_country_flag = COLDWAR_SYR_operations_funded\nupdate_money_dirty_variable = yes"
    effects.append(block("COLDWAR_SYR_clear_campaign_effects", cleanup))
    active = "OR = { has_country_flag = COLDWAR_SYR_operational_mandate " + " ".join("has_idea = " + flag(k) for k in operation_ideas) + " }"
    effects.append(block("COLDWAR_SYR_foreign_init", "COLDWAR_SYR_update_operation_costs = yes"))
    weekly = f"""
COLDWAR_SYR_update_operation_costs = yes
if = {{
    limit = {{ {active} OR = {{ NOT = {{ has_country_flag = COLDWAR_SYR_operational_mandate }} NOT = {{ COLDWAR_SYR_campaign_is_valid = yes }} }} }}
    COLDWAR_SYR_clear_campaign_effects = yes
}}
if = {{
    limit = {{ has_country_flag = COLDWAR_SYR_lebanon_mission OR = {{ NOT = {{ country_exists = LEB }} has_war_with = LEB NOT = {{ LEB = {{ has_country_flag = COLDWAR_SYR_lebanon_invitation }} }} }} }}
    clr_country_flag = COLDWAR_SYR_lebanon_mission
    remove_ideas = COLDWAR_SYR_lebanon_deployment
}}
if = {{
    limit = {{ has_country_flag = COLDWAR_SYR_pipeline_operating OR = {{ NOT = {{ country_exists = IRQ }} has_war_with = IRQ NOT = {{ IRQ = {{ has_country_flag = COLDWAR_SYR_pipeline_operating }} }} }} }}
    clr_country_flag = COLDWAR_SYR_pipeline_operating
    remove_ideas = COLDWAR_SYR_pipeline_administration
    IRQ = {{ clr_country_flag = COLDWAR_SYR_pipeline_operating remove_ideas = COLDWAR_SYR_pipeline_access }}
}}
if = {{
    # IMPERIA CW — Cold War: credit the already-paid interval of older saves.
    limit = {{ has_country_flag = COLDWAR_SYR_pipeline_operating NOT = {{ OR = {{ has_country_flag = COLDWAR_SYR_pipeline_payment_week has_country_flag = COLDWAR_SYR_pipeline_payment_month }} }} }}
    set_country_flag = {{ flag = COLDWAR_SYR_pipeline_payment_week days = 7 }}
    if = {{
        limit = {{ IRQ = {{ exists = yes NOT = {{ has_war_with = SYR }} check_variable = {{ var = treasury value = 0.00093 compare = greater_than_or_equals }} }} }}
        IRQ = {{ {pay(-.00093)} }}
        {pay(.00093)}
    }}
    else = {{
        clr_country_flag = COLDWAR_SYR_pipeline_operating
        remove_ideas = COLDWAR_SYR_pipeline_administration
        IRQ = {{ clr_country_flag = COLDWAR_SYR_pipeline_operating remove_ideas = COLDWAR_SYR_pipeline_access }}
    }}
}}
PER = {{
    if = {{
        limit = {{ date > 1979.2.11 OR = {{ check_variable = {{ ruling_party = 8 }} check_variable = {{ ruling_party = 9 }} }} }}
        set_country_flag = COLDWAR_SYR_iranian_supply_counterparty
    }}
    else = {{ clr_country_flag = COLDWAR_SYR_iranian_supply_counterparty }}
}}
if = {{
    limit = {{
        date > 1980.1.1
        check_variable = {{ treasury < 0.05 }}
        check_variable = {{ debt > gdp_total }}
        NOT = {{ has_country_flag = COLDWAR_SYR_currency_crisis_cooldown }}
        NOT = {{ has_country_flag = COLDWAR_SYR_currency_package_active }}
        NOT = {{ has_country_flag = COLDWAR_SYR_credit_pending }}
    }}
    set_country_flag = COLDWAR_SYR_hard_currency_crisis
    set_country_flag = {{ flag = COLDWAR_SYR_currency_crisis_cooldown days = 365 }}
}}
"""
    effects.append(block("COLDWAR_SYR_foreign_weekly", weekly))
    effects.append(block("COLDWAR_SYR_request_sanctions_review", """
if = {
    limit = { country_exists = USA NOT = { has_country_flag = COLDWAR_SYR_security_scrutiny_requested } }
    set_country_flag = COLDWAR_SYR_security_scrutiny_requested
    USA = { country_event = { id = COLDWAR_SYR_FOREIGN.40 days = 1 } }
}
"""))

    cancel = "OR = { NOT = { has_country_flag = COLDWAR_SYR_operational_mandate } NOT = { COLDWAR_SYR_campaign_is_valid = yes } }"
    for name, title, duration, modifiers in [
        ("war_reserve_readiness", "Prepared Reserve Call-Up", 120, {"army_org_factor": .04, "army_personnel_cost_multiplier_modifier": .072, "industrial_capacity_factory": -.03}),
        ("war_supply_preparation", "Forward Supply Preparation", 120, {"supply_consumption_factor": -.05, "army_fuel_consumption_factor": -.025, "army_personnel_cost_multiplier_modifier": .03}),
        ("war_joint_planning", "Egyptian Joint Planning Mission", 180, {"max_planning_factor": .04, "army_org_factor": .02, "bureaucracy_cost_multiplier_modifier": .03}),
        ("war_medical_service", "Forward Medical Establishment", 120, {"army_org_factor": .02, "stability_factor": .01, "health_cost_multiplier_modifier": .072}),
        ("war_short_window", "Short Offensive Window", 60, {"army_attack_factor": .04, "max_planning_factor": .04, "supply_consumption_factor": .05, "army_personnel_cost_multiplier_modifier": .048}),
        ("war_sustained_window", "Sustained Operational Pressure", 120, {"army_defence_factor": .05, "army_org_factor": .03, "army_personnel_cost_multiplier_modifier": .072, "industrial_capacity_factory": -.02}),
    ]:
        this_cancel = "OR = { " + cancel + " has_idea = COLDWAR_EGY_october_coalition }" if name == "war_joint_planning" else cancel
        idea(name, title, f"A {duration}-day operational establishment. Its military advantages require additional personnel, administration or civilian resources. Benefits and burdens end together when the mandate or Golan objective lapses.", modifiers, this_cancel)
    idea("war_bridge_credit", "Emergency Campaign Credit", "A one-off $0.10 billion loan remains real public debt after demobilization. The emergency interest premium lasts 365 days.", {"interest_rate_multiplier_modifier": .2, "stability_factor": -.01})
    idea("lebanon_deployment", "Limited Lebanese Assistance Mission", "An invited 180-day mission imposes personnel and fuel commitments. Lebanon may revoke its invitation; withdrawal removes both operational benefits and sustainment burdens.", {"army_org_factor": .015, "army_personnel_cost_multiplier_modifier": .072, "army_fuel_consumption_factor": .03}, "OR = { NOT = { has_country_flag = COLDWAR_SYR_lebanon_mission } NOT = { LEB = { has_country_flag = COLDWAR_SYR_lebanon_invitation } } has_war_with = LEB }")
    idea("pipeline_administration", "Iraqi Pipeline Administration", "Agreed pipeline transit pays Syria $0.00093 billion per week while Iraq can pay and cooperation continues. Administration and maintenance increase bureaucracy spending.", {"bureaucracy_cost_multiplier_modifier": .024}, "NOT = { has_country_flag = COLDWAR_SYR_pipeline_operating }")
    idea("pipeline_access", "Agreed Syrian Pipeline Access", "Pipeline transit through Syria improves fuel acquisition in return for $0.00093 billion per week. The agreement ends if payment or cooperation fails.", {"fuel_gain_factor": .02}, "NOT = { has_country_flag = COLDWAR_SYR_pipeline_operating }")
    idea("peacetime_joint_planning", "Egyptian Staff Cooperation", "A separately accepted 180-day staff mission improves planning and organization while increasing bureaucracy spending. It cannot overlap with the operational planning package or the existing Egyptian coalition bonus.", {"max_planning_factor": .04, "army_org_factor": .02, "bureaucracy_cost_multiplier_modifier": .03}, "OR = { NOT = { country_exists = EGY } has_war_with = EGY has_idea = COLDWAR_EGY_october_coalition }")
    idea("import_compression", "Controlled Import Compression", "A 180-day reduction of imports conserves state expenditure but disrupts factories dependent on imported machinery and inputs.", {"bureaucracy_cost_multiplier_modifier": -.024, "industrial_capacity_factory": -.04, "stability_factor": -.02})
    idea("targeted_subsidy_cuts", "Emergency Subsidy Restraint", "A 180-day restraint programme reduces social expenditure while household costs and political opposition rise.", {"social_cost_multiplier_modifier": -.048, "stability_factor": -.03})

    decision_by_id = {d["id"].removeprefix("COLDWAR_SYR_decision_"): d for d in data["decisions"]}
    owned = [k for k in decision_by_id if k not in DOMESTIC and not k.startswith(("campaign_", "coalition_"))]
    handled = set()

    def decision(name, action, guard="", cost_var=None, cash=None, visible="", repeat=None):
        d = decision_by_id[name]
        handled.add(name)
        key = d["id"]
        loc[key], loc[key + "_desc"] = d["label"], d["effects"] + " The conditions and any GDP-based cost are checked again when preparations finish. Syrian expenditure is deducted from the treasury even if the balance becomes negative."
        unlocks = d.get("unlock_any", [d["unlock"]])
        gate = " ".join("has_completed_focus = " + value for value in unlocks)
        if len(unlocks) > 1:
            gate = "OR = { " + gate + " }"
        repeatable = d["repeatable"] if repeat is None else repeat
        done_guard = "" if repeatable else f"\nNOT = {{ has_country_flag = {key}_completed }}"
        common = "original_tag = SYR\nIMP_is_1970_scenario = yes\n" + gate + "\n" + guard + done_guard
        cost_guard = ""
        if cost_var:
            # Validate the charge itself; native MD handles a negative treasury as debt.
            cost_guard = f"check_variable = {{ gdp_total > 0 }}\ncheck_variable = {{ {cost_var} > 0 }}"
            action = cost_pay(cost_var) + "\n" + action
        elif cash:
            action = pay(-cash) + "\n" + action
        guard_full = common + "\n" + cost_guard
        body = f"icon = generic_prepare_civil_war_new\nallowed = {{ original_tag = SYR IMP_is_1970_scenario = yes }}\nvisible = {{ {gate} {visible} {done_guard} }}\navailable = {{ {guard_full} }}\ncost = {d['political_power_cost']}\nfire_only_once = no\ndays_remove = {max(1, d['duration_days'])}\ndays_re_enable = {max(30, d['cooldown_days']) if repeatable else 1}"
        on_success = "" if repeatable else f"\nset_country_flag = {key}_completed"
        body += f"\nremove_effect = {{\nCOLDWAR_SYR_update_operation_costs = yes\nif = {{\nlimit = {{ {guard_full} }}\n{action}{on_success}\nupdate_money_dirty_variable = yes\n}}\nelse = {{ add_political_power = {d['political_power_cost']} custom_effect_tooltip = COLDWAR_SYR_failed_preparations_tt }}\n}}"
        decisions.append(block(key, body))

    loc["COLDWAR_SYR_failed_preparations_tt"] = "Preparations failed because their requirements are no longer met or the GDP-based cost could not be calculated. Political power is returned; no payment or promised benefit is applied. A negative treasury does not prevent Syrian expenditure."
    cv = "COLDWAR_SYR_campaign_is_valid = yes"
    mandate = "has_country_flag = COLDWAR_SYR_operational_mandate\n" + cv
    costs = {n: flag("cost_" + n + "_percent_gdp") for n in ("quarter", "half", "three_quarter")}
    decision("war_appropriation", "set_country_flag = { flag = COLDWAR_SYR_operations_funded days = 365 }", cv + "\nNOT = { has_country_flag = COLDWAR_SYR_operations_funded }", cost_var=costs["three_quarter"])
    for name, idea_name, amount, duration in (("war_reserves", "war_reserve_readiness", "half", 120), ("war_stockpiles", "war_supply_preparation", "half", 120), ("war_medical", "war_medical_service", "quarter", 120)):
        decision(name, timed(idea_name, duration), mandate + f"\nNOT = {{ has_idea = {flag(idea_name)} }}", cost_var=costs[amount])
    decision("war_goal_armistice", "COLDWAR_SYR_create_limited_wargoal = yes", "COLDWAR_SYR_golan_objective_unresolved = yes\nNOT = { has_war_with = ISR }\nNOT = { has_wargoal_against = ISR }", cost_var=costs["quarter"])
    decision("war_reconvene", "country_event = { id = COLDWAR_SYR_WAR.3 days = 1 }", cv + "\nhas_country_flag = COLDWAR_SYR_operations_funded\nNOT = { has_country_flag = COLDWAR_SYR_operational_mandate }")
    decision("war_window", "set_country_flag = COLDWAR_SYR_window_authorization_pending\ncountry_event = { id = COLDWAR_SYR_WAR.6 days = 1 }", mandate + "\nOR = { has_completed_focus = COLDWAR_SYR_limited_war_rapid has_completed_focus = COLDWAR_SYR_limited_war_pressure }\nNOT = { has_country_flag = COLDWAR_SYR_window_committed }\nNOT = { has_country_flag = COLDWAR_SYR_window_authorization_pending }", cost_var=costs["half"])
    decision("war_credit", pay(.1) + "\nset_temp_variable = { debt_change = 0.1 }\nmodify_debt_effect = yes\nset_country_flag = COLDWAR_SYR_bridge_credit_taken\n" + timed("war_bridge_credit", 365), mandate + "\nNOT = { has_country_flag = COLDWAR_SYR_bridge_credit_taken }")
    decision("war_demobilize", "country_event = { id = COLDWAR_SYR_WAR.12 days = 1 }", "has_country_flag = COLDWAR_SYR_operational_mandate")

    def send_request(name, tag, number, pending, guard="", action=""):
        code = f"set_country_flag = {{ flag = {flag(pending)} days = 91 }}\n{tag} = {{ country_event = {{ id = COLDWAR_SYR_FOREIGN.{number} days = 1 }} }}\ncountry_event = {{ id = COLDWAR_SYR_FOREIGN.{number + 100} days = 90 }}\n" + action
        decision(name, code, f"country_exists = {tag}\nNOT = {{ has_war_with = {tag} }}\nNOT = {{ has_country_flag = {flag(pending)} }}\n" + guard)
        event(number + 100, "A Syrian Diplomatic Offer Expires", "The counterparty did not conclude the proposed contract within ninety days. No payment, project or treaty was activated.", [("Close the expired offer", f"clr_country_flag = {flag(pending)}", "")], f"original_tag = SYR has_country_flag = {flag(pending)}", "COLDWAR_SYR_FOREIGN")

    # The published WAR event IDs remain stable; every request has a bounded matching timeout.
    for name, tag, num, pending, guard in (
        ("war_egypt", "EGY", 4, "egypt_offer_pending", mandate + "\nNOT = { has_idea = COLDWAR_SYR_war_joint_planning }\nNOT = { has_idea = COLDWAR_SYR_peacetime_joint_planning }\nNOT = { has_idea = COLDWAR_EGY_october_coalition }"),
        ("war_warning", "ISR", 7, "notice_pending", "NOT = { has_country_flag = COLDWAR_SYR_notice_sent }"),
        ("war_mediation", "ISR", 8, "mediation_pending", mandate),
    ):
        # Israel is deliberately a war counterparty, so do not use the generic no-war sender guard.
        code = f"set_country_flag = {{ flag = {flag(pending)} days = 91 }}\n{tag} = {{ country_event = {{ id = COLDWAR_SYR_WAR.{num} days = 1 }} }}\ncountry_event = {{ id = COLDWAR_SYR_FOREIGN.{num + 200} days = 90 }}"
        if name == "war_warning":
            code += "\nset_country_flag = COLDWAR_SYR_notice_sent"
        decision(name, code, f"country_exists = {tag}\nNOT = {{ is_in_faction_with = ISR }}\nNOT = {{ has_country_flag = {flag(pending)} }}\n" + guard)
        event(num + 200, "A Diplomatic Offer Expires", "No matching answer arrived before the offer expired. There is no payment, operational bonus or change to the war.", [("Close this proposal", f"clr_country_flag = {flag(pending)}\ncountry_event = {{ id = COLDWAR_SYR_WAR.9 days = 1 }}", "")], f"original_tag = SYR has_country_flag = {flag(pending)}", "COLDWAR_SYR_FOREIGN")

    event(1, "A Limited War for the Golan", "Recovering the occupied Golan remains the cabinet’s stated objective. The General Staff must prepare for fighting while the presidency decides how far Syria can pursue its claims without closing the diplomatic channel.", [("Confirm the limited objective", "set_country_flag = COLDWAR_SYR_limited_war_route", ""), ("Keep the diplomatic channel open", "set_country_flag = COLDWAR_SYR_negotiating_channel", "")])
    event(2, "The Syrian War Cabinet", "Military plans require transport, trained reserves and a government willing to sustain their cost. Ministers must decide whether the General Staff should prepare an offensive proposal or concentrate on defending the existing front.", [("Submit the plan for appropriations", "set_country_flag = COLDWAR_SYR_war_budget_submitted", ""), ("Keep the staff on a defensive brief", "set_country_flag = COLDWAR_SYR_defensive_brief", "")])
    event(3, "The Price of Operational Readiness", "The army has received an appropriation for preparations. The cabinet must now decide whether to authorize an operational commitment or retain the money already spent as the cost of readiness without ordering further preparations.", [("Authorize preparations", "set_country_flag = COLDWAR_SYR_operational_mandate\nclr_country_flag = COLDWAR_SYR_defensive_brief", cv + "\nhas_country_flag = COLDWAR_SYR_operations_funded"), ("Hold the operational mandate", "", "")])
    event(4, "A Syrian Coordination Proposal", "Damascus proposes a joint planning mission to coordinate the two armies’ preparations. Syrian officers would fund and host the work, while Cairo retains authority over its own forces and any decision to enter a war.", [("Accept these coordination terms", "FROM = { set_country_flag = COLDWAR_SYR_egypt_offer_accepted country_event = { id = COLDWAR_SYR_WAR.5 days = 1 } }", "NOT = { has_war_with = FROM }"), ("Decline the proposal", "FROM = { clr_country_flag = COLDWAR_SYR_egypt_offer_pending country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", "")], "tag = EGY FROM = { original_tag = SYR has_country_flag = COLDWAR_SYR_egypt_offer_pending }")
    event(5, "Egypt Replies to the Operations Proposal", "Cairo has accepted the proposal for staff cooperation. Syrian ministers must decide whether to commit the required funding and carry the mission’s continuing administrative obligations alongside the country’s other military preparations.", [
        ("Fund the accepted arrangement", cost_pay(costs["quarter"]) + "\n" + timed("war_joint_planning", 180) + "\nclr_country_flag = COLDWAR_SYR_egypt_offer_pending\nclr_country_flag = COLDWAR_SYR_egypt_offer_accepted", mandate + f"\ncheck_variable = {{ gdp_total > 0 }}\ncheck_variable = {{ {costs['quarter']} > 0 }}\nNOT = {{ has_idea = COLDWAR_SYR_war_joint_planning }}\nNOT = {{ has_idea = COLDWAR_SYR_peacetime_joint_planning }}\nNOT = {{ has_idea = COLDWAR_EGY_october_coalition }}"),
        ("Use the existing Egyptian coalition", "clr_country_flag = COLDWAR_SYR_egypt_offer_pending\nclr_country_flag = COLDWAR_SYR_egypt_offer_accepted\nset_country_flag = COLDWAR_SYR_existing_egypt_coordination", "has_idea = COLDWAR_EGY_october_coalition"),
        ("Cancel the arrangement", "clr_country_flag = COLDWAR_SYR_egypt_offer_pending\nclr_country_flag = COLDWAR_SYR_egypt_offer_accepted", ""),
    ], "original_tag = SYR has_country_flag = COLDWAR_SYR_egypt_offer_pending has_country_flag = COLDWAR_SYR_egypt_offer_accepted", immediate="COLDWAR_SYR_update_operation_costs = yes")
    event(6, "Commit the Operational Window", "The General Staff offers two ways to use the preparations already made: a short offensive seeking an early decision, or sustained pressure intended to hold the front and wear down the opponent. Either course will place additional demands on the army.", [
        ("Commit the short offensive", "set_country_flag = COLDWAR_SYR_window_committed\nclr_country_flag = COLDWAR_SYR_window_authorization_pending\n" + timed("war_short_window", 60) + "\ncountry_event = { id = COLDWAR_SYR_WAR.11 days = 60 }", mandate + "\nhas_completed_focus = COLDWAR_SYR_limited_war_rapid"),
        ("Apply sustained pressure", "set_country_flag = COLDWAR_SYR_window_committed\nclr_country_flag = COLDWAR_SYR_window_authorization_pending\n" + timed("war_sustained_window", 120) + "\ncountry_event = { id = COLDWAR_SYR_WAR.11 days = 120 }", mandate + "\nhas_completed_focus = COLDWAR_SYR_limited_war_pressure"),
        ("Stand down the funded preparations", "clr_country_flag = COLDWAR_SYR_window_authorization_pending", ""),
    ], "original_tag = SYR has_country_flag = COLDWAR_SYR_window_authorization_pending NOT = { has_country_flag = COLDWAR_SYR_window_committed }")
    event(7, "Syria States Its War Aims", "Damascus states that recovery of the occupied Golan is the purpose of its military policy. Israel must decide whether to open a diplomatic channel or reject the Syrian position while the confrontation continues.", [("Offer a negotiating channel", "FROM = { set_country_flag = COLDWAR_SYR_negotiating_channel clr_country_flag = COLDWAR_SYR_notice_pending country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", ""), ("Reject the Syrian position", "FROM = { clr_country_flag = COLDWAR_SYR_notice_pending country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", "")], "tag = ISR FROM = { original_tag = SYR has_country_flag = COLDWAR_SYR_notice_pending }")
    event(8, "A Proposal for Disengagement", "Syria proposes talks on separation of forces, security guarantees and the future of the Golan. Accepting the discussion would give the governments a channel in which to examine a settlement of the confrontation.", [("Agree to discuss disengagement", "set_country_flag = COLDWAR_SYR_israeli_disengagement_consent\nFROM = { clr_country_flag = COLDWAR_SYR_mediation_pending set_country_flag = COLDWAR_SYR_negotiating_channel country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", ""), ("Decline these terms", "FROM = { clr_country_flag = COLDWAR_SYR_mediation_pending country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", "")], "tag = ISR FROM = { original_tag = SYR has_country_flag = COLDWAR_SYR_mediation_pending }")
    event(9, "The Diplomatic Channel Reports", "The foreign ministry has received the latest replies to its proposals. Ministers must consider which commitments the other governments have accepted and where Syrian policy must proceed without their cooperation.", [("Review our commitments", "", "")])
    event(10, "The Cabinet Reviews the Campaign", "The campaign has brought new demands for personnel, medical support and supplies. Ministers must weigh those commitments against the prospects of recovering the Golan, reaching a negotiated pause or returning the army to its normal establishment.", [("Maintain the limited objective", "set_country_flag = COLDWAR_SYR_campaign_review_completed", ""), ("Seek a negotiated pause", "set_country_flag = COLDWAR_SYR_campaign_review_completed\nset_country_flag = COLDWAR_SYR_seek_disengagement", ""), ("Begin demobilization", "set_country_flag = COLDWAR_SYR_campaign_review_completed\ncountry_event = { id = COLDWAR_SYR_WAR.12 days = 1 }", "")])
    event(11, "The Operational Window Closes", "The opening phase of the campaign has passed. Commanders must take stock of the front and the resources still committed to it before the cabinet decides whether to maintain the wider military effort.", [("Take stock of the campaign", "remove_ideas = COLDWAR_SYR_war_short_window\nremove_ideas = COLDWAR_SYR_war_sustained_window", ""), ("Review the wider commitments", "remove_ideas = COLDWAR_SYR_war_short_window\nremove_ideas = COLDWAR_SYR_war_sustained_window\ncountry_event = { id = COLDWAR_SYR_WAR.10 days = 1 }", "")])
    event(12, "Returning the Army to Its Establishment", "Returning the army to its normal establishment will release the reserves, supply services and medical resources committed to the campaign. The government must still service its loans and preserve the professional knowledge gained by the armed forces.", [("Stand down the campaign establishment", "COLDWAR_SYR_clear_campaign_effects = yes", "")])

    decision("soviet_training", "set_country_flag = { flag = COLDWAR_SYR_training_request_pending days = 91 }\nSOV = { country_event = { id = COLDWAR_SYR_WAR.13 days = 1 } }\ncountry_event = { id = COLDWAR_SYR_FOREIGN.213 days = 90 }", "COLDWAR_SYR_training_can_request = yes")
    training_guard = """
mdcw_cw_is_active = yes
has_country_flag = mdcw_cw_initialized
check_variable = { political_power > 24.999 }
NOT = { has_war_with = FROM }
NOT = { check_variable = { mdcw_cw_p6_size@SYR > 0 } }
NOT = { check_variable = { mdcw_cw_pend_type@SYR > 0 } }
FROM = { has_country_flag = mdcw_cw_initialized has_country_flag = COLDWAR_SYR_training_request_pending }
"""
    training_code = """
mdcw_cw_recalculate_capacity = yes
if = {
    limit = { check_variable = { mdcw_cw_cap_free > 0.999 } }
    FROM = {
        save_event_target_as = mdcw_cw_assistance_recipient
        ROOT = {
            add_political_power = -25
            set_variable = { mdcw_cw_pend_type@PREV = 6 }
            set_variable = { mdcw_cw_pend_size@PREV = 1 }
            set_variable = { mdcw_cw_pend_until@PREV = global.num_days }
            add_to_variable = { mdcw_cw_pend_until@PREV = 30 }
            mdcw_cw_start_pending_program = yes
            if = {
                limit = { check_variable = { mdcw_cw_p6_state@PREV = 1 } }
                PREV = {
                    set_temp_variable = { treasury_change = -0.06 }
                    modify_treasury_effect = yes
                    set_country_flag = COLDWAR_SYR_training_request_accepted
                }
            }
        }
        clr_country_flag = COLDWAR_SYR_training_request_pending
        country_event = { id = COLDWAR_SYR_WAR.14 days = 1 }
    }
}
else = { FROM = { clr_country_flag = COLDWAR_SYR_training_request_pending country_event = { id = COLDWAR_SYR_WAR.14 days = 1 } } }
"""
    event(13, "Syria Requests a Military Training Mission", "Syrian military schools have requested a Soviet training mission. Moscow must decide whether to commit instructors and assistance capacity, while Damascus would meet the agreed hosting costs and prepare its officers to receive the mission.", [("Accept under the assistance programme", training_code, training_guard), ("Decline the mission", "FROM = { clr_country_flag = COLDWAR_SYR_training_request_pending country_event = { id = COLDWAR_SYR_WAR.14 days = 1 } }", "")], "tag = SOV FROM = { original_tag = SYR has_country_flag = COLDWAR_SYR_training_request_pending }", immediate="mdcw_cw_recalculate_capacity = yes")
    event(14, "The Training-Mission Response", "Moscow has answered the request for a training mission. The Defence Ministry must review the agreement and organise its schools around the commitments the two governments have actually made.", [("Review the assistance agreement", "clr_country_flag = COLDWAR_SYR_training_request_pending", "")])
    event(213, "The Training Request Expires", "The training request has not resulted in an agreement. The Defence Ministry must review its plans for military education and decide whether a later approach to Moscow would be worthwhile.", [("Close the request", "clr_country_flag = COLDWAR_SYR_training_request_pending\ncountry_event = { id = COLDWAR_SYR_WAR.14 days = 1 }", "")], "original_tag = SYR has_country_flag = COLDWAR_SYR_training_request_pending", "COLDWAR_SYR_FOREIGN")
    event(40, "International Scrutiny of Syrian Security Operations", "Reports of Syrian emergency security operations have reached Washington. The American government must weigh a diplomatic sanctions response against its other interests in the region and the likely effect on relations with Damascus.", [
        ("Decline additional sanctions", "", ""),
        ("Impose diplomatic sanctions", "add_political_power = -35\nSYR = { IMP_sanctions_add_dip_from_prev = yes set_temp_variable = { mdcw_cw_t_sanc_type = 1 } mdcw_cw_on_sanction_imposed = yes }\nIMP_sanctions_refresh_world = yes", "check_variable = { political_power > 34.999 }\nSYR = { exists = yes NOT = { is_in_array = { array = imp_dip_sanc_on_us value = ROOT } } }"),
    ], "tag = USA FROM = { original_tag = SYR has_country_flag = COLDWAR_SYR_security_scrutiny_requested }", "COLDWAR_SYR_FOREIGN")

    _install_contracts(data, decision, send_request, event, idea, pay, timed, loc, effects, block)
    missing = set(owned) - handled
    if missing:
        raise ValueError("Unimplemented Syria foreign decisions: " + ", ".join(sorted(missing)))

    # Actual focus rewards are compiled from structured one_time entries, never prose comments.
    for node in data["nodes"]:
        if node["id"] == "COLDWAR_SYR_levant_02":
            node["one_time"] = [{"summary": loc["COLDWAR_SYR_goal_scope_tt"], "code": "set_country_flag = COLDWAR_SYR_limited_war_route\nCOLDWAR_SYR_create_limited_wargoal = yes\ncountry_event = { id = COLDWAR_SYR_WAR.1 days = 1 }"}]
    loc["COLDWAR_SYR_foreign_dossier"] = "Foreign Commitments and Golan Operations"
    loc["COLDWAR_SYR_foreign_dossier_desc"] = "Manage diplomatic offers, agreed missions and the costs of the Golan campaign. Loans, grants and transit contracts remain subject to the terms accepted by the governments concerned."
    write("common/scripted_effects/COLDWAR_SYR_foreign_effects.txt", "# Generated by tools/syria_1970/foreign.py\n\n" + "\n".join(effects))
    write("common/scripted_triggers/COLDWAR_SYR_foreign_triggers.txt", "# Generated by tools/syria_1970/foreign.py\n\n" + "\n".join(triggers))
    write("common/decisions/COLDWAR_SYR_foreign_decisions.txt", block("COLDWAR_SYR_foreign_dossier", "\n".join(decisions)))
    counterpart = ""
    for tag, key, title, guard, code in (
        ("LEB", "revoke_invitation", "Revoke the Syrian Assistance Invitation", "has_country_flag = COLDWAR_SYR_lebanon_invitation", "clr_country_flag = COLDWAR_SYR_lebanon_invitation\nSYR = { clr_country_flag = COLDWAR_SYR_lebanon_mission remove_ideas = COLDWAR_SYR_lebanon_deployment country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }"),
        ("IRQ", "suspend_pipeline", "Suspend the Syrian Pipeline Contract", "has_country_flag = COLDWAR_SYR_pipeline_operating", "clr_country_flag = COLDWAR_SYR_pipeline_operating\nremove_ideas = COLDWAR_SYR_pipeline_access\nSYR = { clr_country_flag = COLDWAR_SYR_pipeline_operating remove_ideas = COLDWAR_SYR_pipeline_administration country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }"),
    ):
        key = flag(key)
        loc[key] = title
        loc[key + "_desc"] = "End the accepted cooperation terms. The corresponding benefits, expenses and future payments cease together. Existing public debt remains payable."
        counterpart += block(key, f"icon = generic_prepare_civil_war_new\nallowed = {{ tag = {tag} IMP_is_1970_scenario = yes }}\nvisible = {{ {guard} }}\navailable = {{ {guard} }}\ncost = 0\nfire_only_once = no\ndays_re_enable = 7\ncomplete_effect = {{ if = {{ limit = {{ {guard} }} {code} }} }}")
    write("common/decisions/COLDWAR_SYR_foreign_decisions.txt", block("COLDWAR_SYR_foreign_dossier", "\n".join(decisions)) + block("COLDWAR_SYR_counterparty_dossier", counterpart))
    loc["COLDWAR_SYR_counterparty_dossier"] = "Syrian Bilateral Commitments"
    loc["COLDWAR_SYR_counterparty_dossier_desc"] = "Accepted assistance and transit arrangements remain subject to this government's consent."
    write("common/decisions/categories/COLDWAR_SYR_foreign_categories.txt", block("COLDWAR_SYR_foreign_dossier", "icon = generic_foreign_policy\nallowed = { original_tag = SYR }\nvisible = { original_tag = SYR IMP_is_1970_scenario = yes }") + block("COLDWAR_SYR_counterparty_dossier", "icon = generic_foreign_policy\nallowed = { OR = { tag = LEB tag = IRQ } }\nvisible = { IMP_is_1970_scenario = yes OR = { has_country_flag = COLDWAR_SYR_lebanon_invitation has_country_flag = COLDWAR_SYR_pipeline_operating } }"))
    write("common/opinion_modifiers/COLDWAR_SYR_foreign_opinions.txt", block("opinion_modifiers", block("COLDWAR_SYR_treaty_relations", "value = 25\ndays = 1825")))
    write("common/ideas/COLDWAR_SYR_foreign_ideas.txt", block("ideas", block("country", "\n".join(ideas))))
    write("events/COLDWAR_SYR_foreign_events.txt", "add_namespace = COLDWAR_SYR_WAR\nadd_namespace = COLDWAR_SYR_FOREIGN\n\n" + "\n".join(events))
    from english_ui import improve
    improve(loc)
    write("localisation/english/COLDWAR_SYR_foreign_l_english.yml", "l_english:\n" + "\n".join(f' {k}:0 "{v.replace(chr(34), chr(39)).replace(chr(10), chr(92)+"n")}"' for k, v in loc.items()), True)
    return {"decision_ids": [decision_by_id[k]["id"] for k in sorted(handled)], "hooks": ["COLDWAR_SYR_foreign_init", "COLDWAR_SYR_foreign_weekly"]}


def _install_contracts(data, decision, send_request, event, idea, pay, timed, loc, effects, block):
    """Independent requests use a single matching pending flag, donor and expiry."""
    # A funded loan is a real lender transfer and an equal Syrian debt liability.
    send_request("development_credit", "SOV", 1, "credit_pending", "NOT = { has_country_flag = COLDWAR_SYR_credit_drawn_recently }")
    loan = """
set_temp_variable = { treasury_change = -0.2 }
modify_treasury_effect = yes
FROM = {
    set_temp_variable = { treasury_change = 0.2 }
    modify_treasury_effect = yes
    set_temp_variable = { debt_change = 0.2 }
    modify_debt_effect = yes
    set_country_flag = { flag = COLDWAR_SYR_credit_drawn_recently days = 730 }
    clr_country_flag = COLDWAR_SYR_credit_pending
    clr_country_flag = COLDWAR_SYR_hard_currency_crisis
    country_event = { id = COLDWAR_SYR_WAR.9 days = 1 }
}
"""
    event(1, "Syria Requests Development Credit", "Damascus seeks development credit to support its economic programme. Moscow must decide whether the proposed loan serves Soviet interests and whether it is prepared to commit the funds while Syria assumes responsibility for repayment.", [("Fund the $0.20 billion loan", loan, "check_variable = { var = treasury value = 0.2 compare = greater_than_or_equals } NOT = { has_war_with = FROM } FROM = { NOT = { has_country_flag = COLDWAR_SYR_credit_drawn_recently } }"), ("Decline the loan", "FROM = { clr_country_flag = COLDWAR_SYR_credit_pending country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", "")], "tag = SOV FROM = { original_tag = SYR has_country_flag = COLDWAR_SYR_credit_pending }", "COLDWAR_SYR_FOREIGN")

    # A friendship treaty is a bilateral political commitment, not an uncosted aid programme.
    send_request("friendship_treaty", "SOV", 2, "friendship_pending")
    event(2, "A Syrian Friendship Treaty", "Damascus proposes a treaty of consultation and respect for sovereignty. The agreement would provide a lasting diplomatic framework for cooperation while leaving military assistance and other financial commitments to negotiations on their own terms.", [("Sign the consultation treaty", "set_country_flag = { flag = COLDWAR_SYR_friendship_treaty days = 1825 }\nadd_opinion_modifier = { target = FROM modifier = COLDWAR_SYR_treaty_relations }\nFROM = { set_country_flag = { flag = COLDWAR_SYR_friendship_treaty days = 1825 } clr_country_flag = COLDWAR_SYR_friendship_pending add_opinion_modifier = { target = ROOT modifier = COLDWAR_SYR_treaty_relations } country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", "NOT = { has_war_with = FROM }"), ("Decline the treaty", "FROM = { clr_country_flag = COLDWAR_SYR_friendship_pending country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", "")], "tag = SOV FROM = { original_tag = SYR has_country_flag = COLDWAR_SYR_friendship_pending }", "COLDWAR_SYR_FOREIGN")

    # Three entry decisions share one project contract, preventing duplicate donations.
    project_gate = "NOT = { has_country_flag = COLDWAR_SYR_project_pending }\nNOT = { has_country_flag = COLDWAR_SYR_project_selection_pending }\nNOT = { has_country_flag = COLDWAR_SYR_foreign_project_completed }"
    for name in ("gulf_project", "gulf_finance", "funded_project"):
        decision(name, "set_country_flag = { flag = COLDWAR_SYR_project_selection_pending days = 90 }\ncountry_event = { id = COLDWAR_SYR_FOREIGN.20 days = 1 }", project_gate + "\nOR = { country_exists = SAU country_exists = KUW country_exists = SOV }")
    selections = []
    for tag, country in (("SAU", "Saudi Arabia"), ("KUW", "Kuwait"), ("SOV", "the Soviet Union")):
        code = f"clr_country_flag = COLDWAR_SYR_project_selection_pending\nset_country_flag = {{ flag = COLDWAR_SYR_project_pending days = 91 }}\nset_variable = {{ COLDWAR_SYR_project_donor = {tag}.id }}\n{tag} = {{ country_event = {{ id = COLDWAR_SYR_FOREIGN.21 days = 1 }} }}\ncountry_event = {{ id = COLDWAR_SYR_FOREIGN.121 days = 90 }}"
        condition = f"{tag} = {{ exists = yes NOT = {{ has_war_with = SYR }} }}"
        if tag == "SOV":
            condition += " has_completed_focus = COLDWAR_SYR_great_powers_10"
        selections.append(("Submit the $0.20 billion proposal to " + country, code, condition))
    selections.append(("Withdraw the project proposal", "clr_country_flag = COLDWAR_SYR_project_selection_pending", ""))
    event(20, "Choose a Project Partner", "The cabinet intends to seek external funding for a civil project. Its delegation must choose which government to approach and present a proposal that offers the prospective donor a reason to support Syrian development.", selections, "original_tag = SYR has_country_flag = COLDWAR_SYR_project_selection_pending", "COLDWAR_SYR_FOREIGN")
    project_accept = """
set_temp_variable = { treasury_change = -0.2 }
modify_treasury_effect = yes
FROM = {
    clr_country_flag = COLDWAR_SYR_project_pending
    set_country_flag = COLDWAR_SYR_project_escrow
    country_event = { id = COLDWAR_SYR_FOREIGN.22 days = 1 }
}
"""
    event(21, "A Syrian Civil Project Proposal", "Damascus requests a grant for a civil project. The prospective donor must decide whether to finance construction in Syria, with the funds committed to the agreed work or returned if the project cannot proceed.", [("Fund the civil project", project_accept, "check_variable = { var = treasury value = 0.2 compare = greater_than_or_equals } NOT = { has_war_with = FROM } FROM = { NOT = { has_country_flag = COLDWAR_SYR_foreign_project_completed } }"), ("Decline the proposal", "FROM = { clr_country_flag = COLDWAR_SYR_project_pending country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", "")], "FROM = { original_tag = SYR has_country_flag = COLDWAR_SYR_project_pending check_variable = { COLDWAR_SYR_project_donor = ROOT.id } }", "COLDWAR_SYR_FOREIGN")
    refresh = "update_state_variables = yes\nif = { limit = { has_country_flag = energy_state_bases_initialized } calculate_energy_use = yes }\nupdate_money_dirty_variable = yes"
    close = "clr_country_flag = COLDWAR_SYR_project_escrow\nset_country_flag = COLDWAR_SYR_foreign_project_completed\n"
    options = []
    for title, state, building in (("Build one civilian workshop in Damascus", 186, "industrial_complex"), ("Improve the Latakia road network", 189, "infrastructure")):
        condition = f"owns_state = {state} controls_state = {state} {state} = {{ free_building_slots = {{ building = {building} size > 0 }} }}"
        code = close + f"{state} = {{ add_building_construction = {{ type = {building} level = 1 instant_build = yes }} }}\n" + refresh
        options.append((title, code, condition))
    options.append(("Return the reserved grant to the donor", "clr_country_flag = COLDWAR_SYR_project_escrow\nvar:COLDWAR_SYR_project_donor = { set_temp_variable = { treasury_change = 0.2 } modify_treasury_effect = yes }", ""))
    event(22, "Allocate the Funded Civil Project", "The donor has provided funding for a civil project. Ministers must choose between a civilian workshop in Damascus and improvements to the Latakia road network, or return the grant if the agreed construction cannot proceed.", options, "original_tag = SYR has_country_flag = COLDWAR_SYR_project_escrow NOT = { has_country_flag = COLDWAR_SYR_foreign_project_completed }", "COLDWAR_SYR_FOREIGN")
    event(121, "The Civil Project Offer Expires", "The prospective donor has not agreed to fund the civil project within the consultation period. The cabinet must decide how its development programme can proceed without that commitment.", [("Close the proposal", "clr_country_flag = COLDWAR_SYR_project_pending", "")], "original_tag = SYR has_country_flag = COLDWAR_SYR_project_pending", "COLDWAR_SYR_FOREIGN")

    # IMPERIA CW — Cold War: one consent-based transit contract; $0.00093bn per week.
    # Weekly rate converts the former $0.004bn/30 days within five decimal places.
    for name in ("pipeline", "iraq_transit"):
        send_request(name, "IRQ", 3, "pipeline_pending", "NOT = { has_country_flag = COLDWAR_SYR_pipeline_operating }")
    pipeline_code = """
set_country_flag = { flag = COLDWAR_SYR_pipeline_operating days = 365 }
add_timed_idea = { idea = COLDWAR_SYR_pipeline_access days = 365 }
FROM = {
    clr_country_flag = COLDWAR_SYR_pipeline_pending
    set_country_flag = { flag = COLDWAR_SYR_pipeline_operating days = 365 }
    add_timed_idea = { idea = COLDWAR_SYR_pipeline_administration days = 365 }
    country_event = { id = COLDWAR_SYR_WAR.9 days = 1 }
}
"""
    event(3, "Proposed Syrian Pipeline Transit Terms", "Damascus offers Iraq a one-year agreement for pipeline transit through Syria. Baghdad would obtain improved access to fuel and pay a weekly transit fee; Syria would maintain the administration needed to keep the route operating.", [("Accept the one-year operating contract", pipeline_code, "NOT = { has_war_with = FROM } check_variable = { var = treasury value = 0.00093 compare = greater_than_or_equals } NOT = { has_country_flag = COLDWAR_SYR_pipeline_operating }"), ("Decline the transit contract", "FROM = { clr_country_flag = COLDWAR_SYR_pipeline_pending country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", "")], "tag = IRQ FROM = { original_tag = SYR has_country_flag = COLDWAR_SYR_pipeline_pending }", "COLDWAR_SYR_FOREIGN")

    # Federal consultation offers go separately to both governments; no automatic integration.
    federation_code = "set_country_flag = { flag = COLDWAR_SYR_federal_offer_pending days = 91 }\n"
    for tag in ("EGY", "LBA"):
        federation_code += f"if = {{ limit = {{ {tag} = {{ exists = yes NOT = {{ has_war_with = SYR }} }} }} {tag} = {{ country_event = {{ id = COLDWAR_SYR_FOREIGN.4 days = 1 }} }} }}\n"
    federation_code += "country_event = { id = COLDWAR_SYR_FOREIGN.104 days = 90 }"
    decision("federation", federation_code, "NOT = { has_country_flag = COLDWAR_SYR_federal_offer_pending }\nOR = { EGY = { exists = yes NOT = { has_war_with = SYR } } LBA = { exists = yes NOT = { has_war_with = SYR } } }")
    event(4, "A Proposed Arab Federal Consultation", "Damascus proposes a framework for consultation and voluntary Arab cooperation. Each government must decide whether regular political coordination will serve its interests and how far it is prepared to support closer relations with Syria.", [("Sign the consultation framework", "set_country_flag = { flag = COLDWAR_SYR_federal_signatory days = 1825 }\nadd_opinion_modifier = { target = FROM modifier = COLDWAR_SYR_treaty_relations }\nFROM = { add_opinion_modifier = { target = ROOT modifier = COLDWAR_SYR_treaty_relations } set_country_flag = COLDWAR_SYR_federal_partner_accepted country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", "NOT = { has_war_with = FROM }"), ("Decline the framework", "FROM = { country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", "")], "OR = { tag = EGY tag = LBA } FROM = { original_tag = SYR has_country_flag = COLDWAR_SYR_federal_offer_pending }", "COLDWAR_SYR_FOREIGN")
    event(104, "Federal Consultations Close", "The consultation period has ended. Damascus must now frame its Arab policy around the governments that accepted the proposed cooperation and the partners that chose to remain outside it.", [("Record the partners' positions", "clr_country_flag = COLDWAR_SYR_federal_offer_pending", "")], "original_tag = SYR has_country_flag = COLDWAR_SYR_federal_offer_pending", "COLDWAR_SYR_FOREIGN")

    # Diplomatic Golan offer can be sent during war; agreement opens real negotiations only.
    decision("golan", "set_country_flag = { flag = COLDWAR_SYR_golan_offer_pending days = 91 }\nISR = { country_event = { id = COLDWAR_SYR_FOREIGN.5 days = 1 } }\ncountry_event = { id = COLDWAR_SYR_FOREIGN.105 days = 90 }", "COLDWAR_SYR_golan_objective_unresolved = yes\nNOT = { has_country_flag = COLDWAR_SYR_golan_offer_pending }")
    event(5, "A Golan Negotiating Package", "Syria proposes staged disengagement, security guarantees and discussion of the Golan. The Israeli government must decide whether these terms offer a basis for negotiations with Damascus and the other governments involved in the conflict.", [("Accept talks on the package", "set_country_flag = COLDWAR_SYR_israeli_disengagement_consent\nFROM = { clr_country_flag = COLDWAR_SYR_golan_offer_pending set_country_flag = COLDWAR_SYR_negotiating_channel country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", ""), ("Decline these terms", "FROM = { clr_country_flag = COLDWAR_SYR_golan_offer_pending country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", "")], "tag = ISR FROM = { original_tag = SYR has_country_flag = COLDWAR_SYR_golan_offer_pending }", "COLDWAR_SYR_FOREIGN")
    event(105, "The Golan Proposal Expires", "The Golan proposal has not produced an agreement. The cabinet must consider whether to return to talks later or rely on its other means of pursuing the Syrian position.", [("Close the offer", "clr_country_flag = COLDWAR_SYR_golan_offer_pending", "")], "original_tag = SYR has_country_flag = COLDWAR_SYR_golan_offer_pending", "COLDWAR_SYR_FOREIGN")
    joint_guard = "NOT = { has_idea = COLDWAR_SYR_war_joint_planning }\nNOT = { has_idea = COLDWAR_SYR_peacetime_joint_planning }\nNOT = { has_idea = COLDWAR_EGY_october_coalition }\ncheck_variable = { gdp_total > 0 }\ncheck_variable = { COLDWAR_SYR_cost_quarter_percent_gdp > 0 }"
    send_request("joint_plan", "EGY", 9, "joint_plan_pending", joint_guard)
    joint_code = """
FROM = {
    COLDWAR_SYR_update_operation_costs = yes
    if = {
        limit = {
            check_variable = { gdp_total > 0 }
            check_variable = { COLDWAR_SYR_cost_quarter_percent_gdp > 0 }
            NOT = { has_idea = COLDWAR_SYR_war_joint_planning }
            NOT = { has_idea = COLDWAR_SYR_peacetime_joint_planning }
            NOT = { has_idea = COLDWAR_EGY_october_coalition }
        }
        set_temp_variable = { treasury_change = COLDWAR_SYR_cost_quarter_percent_gdp }
        multiply_temp_variable = { treasury_change = -1 }
        modify_treasury_effect = yes
        add_timed_idea = { idea = COLDWAR_SYR_peacetime_joint_planning days = 180 }
    }
    clr_country_flag = COLDWAR_SYR_joint_plan_pending
    country_event = { id = COLDWAR_SYR_WAR.9 days = 1 }
}
"""
    event(9, "A Syrian Staff-Cooperation Offer", "Damascus proposes a joint staff mission to improve the two armies’ planning and organisation. Syria would fund the mission and maintain its administrative establishment, while Egypt would retain command of its forces and its own military policy.", [("Accept the staff cooperation", joint_code, "NOT = { has_war_with = FROM }"), ("Decline the mission", "FROM = { clr_country_flag = COLDWAR_SYR_joint_plan_pending country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", "")], "tag = EGY FROM = { original_tag = SYR has_country_flag = COLDWAR_SYR_joint_plan_pending }", "COLDWAR_SYR_FOREIGN")

    # Lebanese invitation and deployment are distinct, separately consenting stages.
    send_request("lebanon", "LEB", 6, "lebanon_pending", "NOT = { LEB = { has_country_flag = COLDWAR_SYR_lebanon_invitation } }")
    event(6, "Syria Offers Limited Security Assistance", "Damascus seeks a revocable Lebanese invitation for limited security assistance. The Lebanese government must weigh the proposed mission against its authority over internal affairs, while Syria would bear the cost of any deployment it subsequently authorizes.", [("Issue the revocable invitation", "set_country_flag = { flag = COLDWAR_SYR_lebanon_invitation days = 365 }\nFROM = { clr_country_flag = COLDWAR_SYR_lebanon_pending country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", "NOT = { has_war_with = FROM }"), ("Decline the mission", "FROM = { clr_country_flag = COLDWAR_SYR_lebanon_pending country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", "")], "tag = LEB FROM = { original_tag = SYR has_country_flag = COLDWAR_SYR_lebanon_pending }", "COLDWAR_SYR_FOREIGN")
    decision("authorize_mission", "set_country_flag = { flag = COLDWAR_SYR_lebanon_mission days = 180 }\n" + timed("lebanon_deployment", 180), "LEB = { exists = yes has_country_flag = COLDWAR_SYR_lebanon_invitation NOT = { has_war_with = SYR } }\nNOT = { has_country_flag = COLDWAR_SYR_lebanon_mission }", cash=.08)
    decision("regional_withdrawal", "clr_country_flag = COLDWAR_SYR_lebanon_mission\nremove_ideas = COLDWAR_SYR_lebanon_deployment\nLEB = { clr_country_flag = COLDWAR_SYR_lebanon_invitation }", "OR = { has_country_flag = COLDWAR_SYR_lebanon_mission has_idea = COLDWAR_SYR_lebanon_deployment }")

    # Foreign-currency crisis choices are exclusive for the current 180-day relief period.
    decision("hard_currency", "country_event = { id = COLDWAR_SYR_FOREIGN.7 days = 1 }", "has_country_flag = COLDWAR_SYR_hard_currency_crisis\nNOT = { has_country_flag = COLDWAR_SYR_currency_package_active }")
    event(7, "A Hard-Currency Emergency", "Foreign exchange is running short as the government struggles to maintain essential imports and its domestic commitments. Ministers must choose between reducing subsidies, compressing imported inputs or seeking a Soviet loan to ease the immediate pressure.", [("Restrain subsidies", "set_country_flag = { flag = COLDWAR_SYR_currency_package_active days = 180 }\nclr_country_flag = COLDWAR_SYR_hard_currency_crisis\n" + timed("targeted_subsidy_cuts", 180), ""), ("Compress imported inputs", "set_country_flag = { flag = COLDWAR_SYR_currency_package_active days = 180 }\nclr_country_flag = COLDWAR_SYR_hard_currency_crisis\n" + timed("import_compression", 180), ""), ("Request a $0.20 billion loan", "set_country_flag = { flag = COLDWAR_SYR_credit_pending days = 91 }\nSOV = { country_event = { id = COLDWAR_SYR_FOREIGN.1 days = 1 } }\ncountry_event = { id = COLDWAR_SYR_FOREIGN.101 days = 90 }", "country_exists = SOV NOT = { has_war_with = SOV } NOT = { has_country_flag = COLDWAR_SYR_credit_pending } NOT = { has_country_flag = COLDWAR_SYR_credit_drawn_recently }"), ("Defer the package", "", "")], "original_tag = SYR has_country_flag = COLDWAR_SYR_hard_currency_crisis NOT = { has_country_flag = COLDWAR_SYR_currency_package_active }", "COLDWAR_SYR_FOREIGN")

    # Supply credit after the actual Iranian political transformation, never an automatic oil gift.
    idea("iranian_supply_credit", "Iranian Supply Credit", "A one-year supply credit improves fuel acquisition. The $0.10 billion principal remains Syrian public debt; an additional 0.15 percentage-point interest premium applies while the arrangement lasts.", {"fuel_gain_factor": .03, "interest_rate_multiplier_modifier": .15}, "OR = { has_war_with = PER NOT = { PER = { has_country_flag = COLDWAR_SYR_iranian_supply_counterparty } } }")
    send_request("iran_oil", "PER", 8, "iran_supply_pending", "date > 1979.2.11\nPER = { has_country_flag = COLDWAR_SYR_iranian_supply_counterparty has_opinion = { target = SYR value > -1 } }\nNOT = { has_idea = COLDWAR_SYR_iranian_supply_credit }")
    event(8, "A Syrian Supply and Credit Request", "Damascus seeks an Iranian credit advance to support fuel supplies for the coming year. Tehran must decide whether to finance the arrangement, while Syria would assume the resulting debt and the agreed borrowing premium.", [("Approve the financed supply arrangement", "set_temp_variable = { treasury_change = -0.1 }\nmodify_treasury_effect = yes\nFROM = { set_temp_variable = { treasury_change = 0.1 } modify_treasury_effect = yes set_temp_variable = { debt_change = 0.1 } modify_debt_effect = yes clr_country_flag = COLDWAR_SYR_iran_supply_pending add_timed_idea = { idea = COLDWAR_SYR_iranian_supply_credit days = 365 } country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", "has_country_flag = COLDWAR_SYR_iranian_supply_counterparty NOT = { has_war_with = FROM } check_variable = { var = treasury value = 0.1 compare = greater_than_or_equals } FROM = { NOT = { has_idea = COLDWAR_SYR_iranian_supply_credit } }"), ("Decline the request", "FROM = { clr_country_flag = COLDWAR_SYR_iran_supply_pending country_event = { id = COLDWAR_SYR_WAR.9 days = 1 } }", "")], "tag = PER FROM = { original_tag = SYR has_country_flag = COLDWAR_SYR_iran_supply_pending }", "COLDWAR_SYR_FOREIGN")

    # Additional recipient withdrawal controls are generated separately by install().
    loc["COLDWAR_SYR_treaty_relations"] = "Syrian Consultation Agreement"
