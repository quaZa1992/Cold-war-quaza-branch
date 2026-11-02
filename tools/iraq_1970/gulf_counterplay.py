# IMPERIA COLD WAR — Local Iraqi counterplay for the northern Gulf programme.
"""Pure overlay for usa_module's in-memory definitions. Never writes files.

The existing 45-day warning and native core-group revolt coordination remain
owned by usa_module. This overlay owns paid security operations and their local
stationed-force requirements, readiness, one-time reductions and target effects.
"""
from __future__ import annotations

import re
from textwrap import dedent, indent

P = "COLDWAR_USA_gulf_"
NORTH = ((164, "KUR"), (633, "KUR"), (630, "KUR"), (1078, "PUK"))
OP = P + "security_operation"
AGE = P + "security_local_days"
RECEIPT = P + "security_local_reduced_operation"
MIGRATED = P + "security_local_migrated"


def block(key: str, body: str) -> str:
    return key + " = {\n" + indent(dedent(body).strip(), "\t") + "\n}\n"


def _troops(sid: int, count: int) -> str:
    return f"IRQ = {{ num_divisions_in_states = {{ count > {count - 1} states = {{ {sid} }} }} }}"


def _state_legal(sid: int, tag: str) -> str:
    return f"is_owned_and_controlled_by = IRQ\nis_core_of = {tag}" + (f"\n{P}puk_formed = yes" if tag == "PUK" else "")


def _paid() -> str:
    return f"IRQ = {{ {P}security_active = yes check_variable = {{ {OP} > 0 }} }}"


def apply_counterplay(effects: dict[str, str], triggers: dict[str, str],
                      loc: dict[str, str], decisions: list[str]) -> None:
    """Install local counterplay in supplied definitions without filesystem I/O."""
    assert all(P + key in effects for key in ("usa_daily", "irq_daily", "start_security", "start_major_operation", "end_security"))
    triggers[P + "security_preparation_crisis"] = (
        f"tag = IRQ\n{P}campaign = yes\n{P}northern_grievance = yes\n"
        f"OR = {{ {P}insurgency = yes has_war_with = KUW }}"
    )
    for sid, tag in NORTH:
        legal = _state_legal(sid, tag)
        triggers[P + f"security_stationed_{sid}"] = legal + "\n" + (
            f"IRQ = {{ OR = {{ AND = {{ has_idea = {P}security_small "
            f"num_divisions_in_states = {{ count > 1 states = {{ {sid} }} }} }} "
            f"AND = {{ has_idea = {P}security_major num_divisions_in_states = {{ count > 2 states = {{ {sid} }} }} }} }} }}"
        )
        triggers[P + f"security_local_effective_{sid}"] = (
            f"{P}security_stationed_{sid} = yes\n{_paid()}\n"
            f"check_variable = {{ {AGE} > 29 }}\n"
            f"check_variable = {{ var = {RECEIPT} value = IRQ.{OP} compare = equals }}"
        )
    # The old pooled-two-divisions trigger remains a compatibility provider;
    # new prices and deliveries use an actual local state predicate instead.
    for key, minimum in (("security", 2), ("major_operation", 3)):
        candidates = "\n".join(f"{sid} = {{ {_state_legal(sid, tag)} {_troops(sid, minimum)} }}" for sid, tag in NORTH)
        triggers[P + "security_can_start_" + key] = (
            f"{P}security_preparation_crisis = yes\ncheck_variable = {{ gdp_total > 0 }}\n"
            f"NOT = {{ has_country_flag = MD_skip_treasury_cost }}\n"
            f"NOT = {{ has_country_flag = {P}security_cooldown }}\n"
            f"NOT = {{ {P}security_active = yes }}\nOR = {{ {candidates} }}"
        )

    # Historical operations delivered their reduction to all eligible states
    # at once. Preserve that receipt conservatively instead of delivering again.
    old_completed = "\n".join(
        f"{sid} = {{ set_variable = {{ {RECEIPT} = IRQ.{OP} }} set_variable = {{ {AGE} = 30 }} }}"
        for sid, _ in NORTH
    )
    effects[P + "security_migrate_local"] = block("if", f"""
        limit = {{ tag = IRQ {P}campaign = yes NOT = {{ has_country_flag = {MIGRATED} }} }}
        set_country_flag = {MIGRATED}
        if = {{ limit = {{ {P}security_active = yes }}
            if = {{ limit = {{ NOT = {{ check_variable = {{ {OP} > 0 }} }} }} set_variable = {{ {OP} = 1 }} }}
            if = {{ limit = {{ NOT = {{ has_country_flag = {P}security_delivery }} }}
                {old_completed}
            }}
        }}
    """)

    # Per-state readiness is continuous, even after a delivered reduction. A
    # withdrawal removes that state's target immediately on the next observer.
    # Returning troops must rebuild readiness, but cannot repeat the reduction.
    local_rows = []
    for sid, tag in NORTH:
        local_rows.append(block(str(sid), f"""
            if = {{ limit = {{ {_paid()} {P}security_stationed_{sid} = yes }}
                if = {{ limit = {{ check_variable = {{ {AGE} < 30 }} IRQ = {{ NOT = {{ has_country_flag = {P}security_observed_today }} }} }} add_to_variable = {{ {AGE} = 1 }} }}
                if = {{ limit = {{ check_variable = {{ {AGE} > 29 }} has_resistance = yes occupied_country_tag = {tag} }}
                    if = {{ limit = {{ NOT = {{ check_variable = {{ var = {RECEIPT} value = IRQ.{OP} compare = equals }} }} }}
                        add_resistance = -15
                        if = {{ limit = {{ IRQ = {{ has_idea = {P}security_major }} }} add_resistance = -10 }}
                        set_variable = {{ {RECEIPT} = IRQ.{OP} }}
                    }}
                    remove_resistance_target = 19709102
                    add_resistance_target = {{ id = 19709102 amount = IRQ.{P}security_target occupier = IRQ occupied = {tag} days = 2 tooltip = {P}target_security }}
                }} else = {{ remove_resistance_target = 19709102 }}
            }} else = {{ set_variable = {{ {AGE} = 0 }} remove_resistance_target = 19709102 }}
        """))
    effects[P + "security_reconcile_local"] = block("if", f"limit = {{ tag = IRQ {P}campaign = yes }}\n{P}security_migrate_local = yes\n" + "\n".join(local_rows) + f"\nif = {{ limit = {{ NOT = {{ has_country_flag = {P}security_observed_today }} }} set_country_flag = {{ flag = {P}security_observed_today value = 1 days = 1 }} }}")
    # Compatibility calls cannot bypass local readiness or replay the reduction.
    effects[P + "security_reduce"] = P + "security_reconcile_local = yes\n"

    for key, share, reduction, target in (("security", "0.02", 15, 20), ("major_operation", "0.04", 25, 35)):
        idea = P + ("security_small" if key == "security" else "security_major")
        reset = "\n".join(f"{sid} = {{ set_variable = {{ {AGE} = 0 }} remove_resistance_target = 19709102 }}" for sid, _ in NORTH)
        effects[P + "start_" + key] = block("if", f"""
            limit = {{ tag = IRQ {P}campaign = yes }}
            set_temp_variable = {{ {P}invoice = gdp_total }}
            multiply_temp_variable = {{ {P}invoice = {share} }}
            if = {{ limit = {{ {P}security_can_start_{key} = yes check_variable = {{ var = {P}invoice value = 0 compare = greater_than }} check_variable = {{ var = treasury value = {P}invoice compare = greater_than_or_equals }} }}
                set_temp_variable = {{ treasury_change = {P}invoice }}
                multiply_temp_variable = {{ treasury_change = -1 }}
                modify_treasury_effect = yes
                set_country_flag = {MIGRATED}
                add_to_variable = {{ {OP} = 1 }}
                remove_ideas = {P}security_small
                remove_ideas = {P}security_major
                add_timed_idea = {{ idea = {idea} days = 90 }}
                set_country_flag = {{ flag = {P}security_cooldown value = 1 days = 90 }}
                set_country_flag = {{ flag = {P}security_delivery value = 1 days = 90 }}
                set_variable = {{ {P}security_reduction = {reduction} }}
                set_variable = {{ {P}security_target = -{target} }}
                {reset}
            }}
        """)
    effects[P + "end_security"] = block("if", f"limit = {{ tag = IRQ {P}campaign = yes }}\nremove_ideas = {P}security_small\nremove_ideas = {P}security_major\nclr_country_flag = {P}security_delivery\n" + "\n".join(f"{sid} = {{ set_variable = {{ {AGE} = 0 }} remove_resistance_target = 19709102 }}" for sid, _ in NORTH))

    # Keep the original native warning observer byte-for-byte after its opening
    # settlement check. Only its former global security preparation is replaced.
    marker = f"if = {{ limit = {{ {P}settlement_respected = yes }}"
    old_irq = effects[P + "irq_daily"]
    assert old_irq.count(marker) == 1
    effects[P + "irq_daily"] = (
        (P + "observe_kuwait_crisis = yes\n" if P + "observe_kuwait_crisis" in effects else "") +
        f"set_variable = {{ {P}security_quote = gdp_total }}\nmultiply_variable = {{ {P}security_quote = .02 }}\n"
        f"set_variable = {{ {P}major_quote = gdp_total }}\nmultiply_variable = {{ {P}major_quote = .04 }}\n"
        f"{P}security_reconcile_local = yes\n" + old_irq[old_irq.index(marker):]
    )

    # The USA observer must never stop all four pulses merely because Baghdad
    # purchased a national idea. Its individual state conditions are live.
    us = effects[P + "usa_daily"]
    global_veto = f"NOT = {{ {P}security_active = yes }}"
    assert us.count(global_veto) == 1
    us = us.replace(global_veto, "always = yes", 1)
    for sid, tag in NORTH:
        old = f"has_state_flag = {P}seeded {P}eligible_{sid} = yes occupied_country_tag = {tag} resistance < 80"
        assert us.count(old) == 1, sid
        us = us.replace(old, old + f" NOT = {{ {P}security_local_effective_{sid} = yes }}", 1)
    effects[P + "usa_daily"] = us

    replacements = {}
    for did, key, title, quote, idea, minimum, reduction, target in (
        ("COLDWAR_IRQ_northern_security", "security", "Emergency Security Appropriation", "security_quote", "security_small", 2, 15, 20),
        ("COLDWAR_IRQ_northern_major_operation", "major_operation", "Major Northern Operation", "major_quote", "security_major", 3, 25, 35),
    ):
        desc = (f"Pay {'2' if minimum == 2 else '4'}% of current annual GDP for a 90-day operation. "
                f"Station at least {minimum} Iraqi divisions in each state to be secured for 30 consecutive days. "
                f"Each prepared state receives one {reduction}-point resistance reduction per paid operation. "
                f"Its {target}-point target reduction and protection against foreign mobilisation pulses require those local troops to remain. "
                "Withdrawal forfeits local readiness. The national military overhead and consultation interval last for the original term.")
        loc[did] = title;loc[did + "_desc"] = desc
        preview_rows = [f"set_temp_variable = {{ treasury_change = {P}{quote} }}", "multiply_temp_variable = { treasury_change = -1 }", "modify_treasury_effect = yes", f"add_timed_idea = {{ idea = {P}{idea} days = 90 }}"]
        for sid, tag in NORTH:
            preview_rows.append(block(str(sid), f"add_resistance = -{reduction}\nadd_resistance_target = {{ id = 19709102 amount = -{target} occupier = IRQ occupied = {tag} days = 2 tooltip = {P}target_security }}"))
        available = f"hidden_trigger = {{ {P}security_can_start_{key} = yes }}\n" + (
            f"custom_trigger_tooltip = {{ tooltip = {P}security_{key}_troops_tt OR = {{ "
            + " ".join(f"{sid} = {{ {_state_legal(sid, tag)} {_troops(sid, minimum)} }}" for sid, tag in NORTH) + " } }\n"
            f"custom_trigger_tooltip = {{ tooltip = {P}security_cooldown_tt NOT = {{ has_country_flag = {P}security_cooldown }} }}\n"
            f"check_variable = {{ {P}{quote} > 0 }}\ncheck_variable = {{ var = treasury value = {P}{quote} compare = greater_than_or_equals }}"
        )
        replacements[did] = block(did, "icon = generic_decision\n" + block("visible", f"tag = IRQ {P}campaign = yes {P}northern_grievance = yes OR = {{ {P}insurgency = yes has_war_with = KUW }}") + block("available", available) + "cost = 0\n" + block("complete_effect", block("effect_tooltip", "\n".join(preview_rows)) + block("hidden_effect", P + "start_" + key + " = yes")) + "ai_will_do = { factor = 1 }")
        loc[P + f"security_{key}_troops_tt"] = f"At least {minimum} Iraqi divisions are stationed in an eligible northern state. Each secured state requires its own local force."
    loc[P + "security_cooldown_tt"] = "The previous northern operation's 90-day consultation interval has ended."
    for did, definition in replacements.items():
        matches = [i for i, text in enumerate(decisions) if re.match(re.escape(did) + r"\s*=", text)]
        assert len(matches) == 1, (did, matches)
        decisions[matches[0]] = definition
