# IMPERIA CW — Cold War: iraq 1970 — gulf module.
"""Fresh COLDWAR_IRQ Gulf finance and Kuwait crisis providers.

generate(root) returns owned runtime paths -> UTF-8 text; it never writes files.
Native weekly MD accounting remains the only recurring cash/debt charger.
This module deliberately has no dependency on retained/rejected 1985 content.
"""
from pathlib import Path
from textwrap import dedent
import json

P = "COLDWAR_IRQ_gulf_"
CREDITORS = (("KUW", "Kuwait", .08, 1), ("SAU", "Saudi Arabia", .08, 2),
             ("UAE", "the United Arab Emirates", .04, 3))
FOCUS_REWARDS = {
    "COLDWAR_IRQ_iran_gulf_credit": P + "unlock_credit = yes",
    "COLDWAR_IRQ_iran_operational_plan": P + "unlock_credit = yes",
    "COLDWAR_IRQ_war_credit_burden": P + "unlock_debt_policy = yes",
    "COLDWAR_IRQ_war_reintegration": P + "unlock_kuwait_integration = yes",
}
API = {
    "credit_unlock": P + "unlock_credit",
    "debt_policy_unlock": P + "unlock_debt_policy",
    "integration_unlock": P + "unlock_kuwait_integration",
    "kuwait_claim": P + "claim_kuwait",
    "kuwait_ultimatum": P + "kuwait_ultimatum",
    "daily": P + "daily",
    "attacker_record_global": P + "iraq_attacked_kuwait",
    "wartime_borrowing": P + "war_borrowing_frozen",
    "other_debt_change": P + "change_other_debt",
    "other_debt_change_input": P + "other_debt_change",
    "other_debt_change_applied": P + "other_debt_applied",
    "other_retirement_counter": P + "other_retirement_total",
}


def text(source):
    return dedent(source).strip() + "\n"


def block(key, source):
    body = text(source)
    return key + " = {\n" + "\n".join("\t" + x if x else "" for x in body.splitlines()) + "\n}\n\n"


def generate(root: Path) -> dict[str, str]:
    """Generate only the files owned by this module; no shared-file mutation."""
    root = Path(root)
    effects, triggers, events, decisions = [], [], [], []
    loc = {}

    def L(key, name, description=None):
        loc[key] = name
        if description is not None:
            loc[key + "_desc"] = description

    def E(name, body):
        # Public helpers reject foreign countries and later-scenario callers,
        # including before reconciliation can mutate their accounting variables.
        guarded = "if = {\n\tlimit = { " + P + "actor = yes }\n" + text(body) + "}\n"
        effects.append(block(P + name, guarded))

    def T(name, body):
        triggers.append(block(P + name, body))

    def D(name, body):
        decisions.append(block(P + name, body))

    T("actor", "tag = IRQ\nexists = yes\nCOLDWAR_IRQ_campaign_active = yes")
    T("owns_kuwait", "172 = { is_owned_by = IRQ is_controlled_by = IRQ }\n488 = { is_owned_by = IRQ is_controlled_by = IRQ }")
    T("controls_kuwait", "172 = { is_controlled_by = IRQ }\n488 = { is_controlled_by = IRQ }")
    T("postwar", f"{P}actor = yes\nhas_country_flag = {P}iran_war_seen\nNOT = {{ has_war_with = PER }}")
    T("can_integrate", f"""
        {P}actor = yes
        {P}owns_kuwait = yes
        has_war = no
        has_stability > 0.50
        has_country_flag = {P}integration_unlocked
        has_country_flag = {{ flag = {P}stable_kuwait days > 179 }}
        NOT = {{ has_country_flag = {P}kuwait_integrated }}
        NOT = {{ has_country_flag = MD_skip_treasury_cost }}
        check_variable = {{ gdp_total > 0 }}
    """)
    T("can_ultimatum", f"""
        {P}postwar = yes
        country_exists = KUW
        is_subject = no
        NOT = {{ has_war_with = KUW }}
        NOT = {{ is_in_faction_with = KUW }}
        NOT = {{ has_non_aggression_pact_with = KUW }}
        NOT = {{ has_country_flag = {P}ultimatum_issued }}
        NOT = {{ has_country_flag = {P}arbitration_window }}
        has_country_flag = {P}kuwait_claimed
        OR = {{
            has_country_flag = {P}kuwait_refused_forgiveness
            has_country_flag = {P}oil_dispute_rejected
        }}
    """)
    E("initialize", f"""
        if = {{
            limit = {{ {P}actor = yes NOT = {{ has_country_flag = {P}initialized }} }}
            set_country_flag = {P}initialized
            set_variable = {{ {P}debt_snapshot = debt }}
            set_variable = {{ {P}other_debt = debt }}
            set_variable = {{ {P}other_retirement_total = 0 }}
            set_variable = {{ {P}cost_tier = 0 }}
        }}
    """)
    E("unlock_credit", f"if = {{ limit = {{ {P}actor = yes }} set_country_flag = {P}credit_unlocked }}")
    E("unlock_debt_policy", f"if = {{ limit = {{ {P}actor = yes }} set_country_flag = {P}debt_policy_unlocked }}")
    E("unlock_kuwait_integration", f"if = {{ limit = {{ {P}actor = yes }} set_country_flag = {P}integration_unlocked }}")

    # Conservative reconciliation of aggregate native debt. Unknown reductions
    # retire the named Gulf principal first; no automatic creditor cash grant.
    reconcile = f"""
        {P}initialize = yes
        set_temp_variable = {{ {P}debt_delta = debt }}
        subtract_from_temp_variable = {{ {P}debt_delta = {P}debt_snapshot }}
        if = {{
            limit = {{ check_variable = {{ {P}debt_delta > 0 }} }}
            add_to_variable = {{ {P}other_debt = {P}debt_delta }}
        }}
        else_if = {{
            limit = {{ check_variable = {{ {P}debt_delta < 0 }} }}
            set_temp_variable = {{ {P}unassigned_reduction = {P}debt_delta }}
            multiply_temp_variable = {{ {P}unassigned_reduction = -1 }}
    """
    for tag, _, _, _ in CREDITORS:
        reconcile += f"""
            set_temp_variable = {{ {P}retire = {P}unassigned_reduction }}
            if = {{ limit = {{ check_variable = {{ {P}retire > {P}principal_{tag} }} }}
                set_temp_variable = {{ {P}retire = {P}principal_{tag} }}
            }}
            subtract_from_variable = {{ {P}principal_{tag} = {P}retire }}
            subtract_from_temp_variable = {{ {P}unassigned_reduction = {P}retire }}
        """
    reconcile += f"""
            # Export only an actual unknown retirement of protected other debt.
            # The decisions module consumes each cumulative delta once to retire
            # its own named non-Gulf balances, without inventing creditor cash.
            set_temp_variable = {{ {P}retire = {P}unassigned_reduction }}
            if = {{ limit = {{ check_variable = {{ {P}retire > {P}other_debt }} }}
                set_temp_variable = {{ {P}retire = {P}other_debt }}
            }}
            add_to_variable = {{ {P}other_retirement_total = {P}retire }}
            subtract_from_variable = {{ {P}other_debt = {P}retire }}
            clamp_variable = {{ var = {P}other_debt min = 0 }}
        }}
        set_variable = {{ {P}debt_snapshot = debt }}
    """
    E("reconcile_debt", reconcile)

    # Known non-Gulf contracts must not look like an unattributed repayment:
    # that would retire a Gulf receivable despite paying a different creditor.
    # Input/output are signed temporary amounts; this helper changes native debt
    # only. The caller owns the matching guarded cash/principal transaction.
    # Reconcile before computing a repayment and include other_debt in its caps.
    E("change_other_debt", f"""
        {P}reconcile_debt = yes
        set_temp_variable = {{ {P}other_debt_applied = {P}other_debt_change }}
        if = {{
            limit = {{ check_variable = {{ {P}other_debt_applied < 0 }} }}
            multiply_temp_variable = {{ {P}other_debt_applied = -1 }}
            if = {{ limit = {{ check_variable = {{ {P}other_debt_applied > {P}other_debt }} }}
                set_temp_variable = {{ {P}other_debt_applied = {P}other_debt }}
            }}
            if = {{ limit = {{ check_variable = {{ {P}other_debt_applied > debt }} }}
                set_temp_variable = {{ {P}other_debt_applied = debt }}
            }}
            multiply_temp_variable = {{ {P}other_debt_applied = -1 }}
        }}
        if = {{ limit = {{ NOT = {{ check_variable = {{ {P}other_debt_applied = 0 }} }} }}
            set_temp_variable = {{ debt_change = {P}other_debt_applied }}
            modify_debt_effect = yes
            add_to_variable = {{ {P}other_debt = {P}other_debt_applied }}
            clamp_variable = {{ var = {P}other_debt min = 0 }}
            set_variable = {{ {P}debt_snapshot = debt }}
        }}
    """)

    E("clear_costs", "\n".join(f"if = {{ limit = {{ has_idea = {P}iran_cost_{i} }} remove_ideas = {P}iran_cost_{i} }}" for i in (1, 2, 3)) + f"\nset_variable = {{ {P}cost_tier = 0 }}")
    # No cash, debt or resource grants occur in refresh. Tier modifiers replace.
    E("refresh_war_costs", f"""
        set_temp_variable = {{ {P}desired_tier = 0 }}
        if = {{ limit = {{ has_war_with = PER }}
            set_temp_variable = {{ {P}desired_tier = 1 }}
            if = {{ limit = {{ has_country_flag = {{ flag = {P}iran_war_start days > 179 }} }}
                set_temp_variable = {{ {P}desired_tier = 2 }}
            }}
            if = {{ limit = {{ has_country_flag = {{ flag = {P}iran_war_start days > 364 }} }}
                set_temp_variable = {{ {P}desired_tier = 3 }}
            }}
        }}
        if = {{ limit = {{ NOT = {{ check_variable = {{ {P}cost_tier = {P}desired_tier }} }} }}
            {P}clear_costs = yes
            if = {{ limit = {{ check_variable = {{ {P}desired_tier = 1 }} }} add_ideas = {P}iran_cost_1 }}
            else_if = {{ limit = {{ check_variable = {{ {P}desired_tier = 2 }} }} add_ideas = {P}iran_cost_2 }}
            else_if = {{ limit = {{ check_variable = {{ {P}desired_tier = 3 }} }} add_ideas = {P}iran_cost_3 }}
            set_variable = {{ {P}cost_tier = {P}desired_tier }}
            ingame_update_setup = yes
        }}
    """)
    E("audit_war_borrowing", f"""
        # Net new native debt relative to this war's entry balance; never a loan grant.
        set_variable = {{ {P}war_borrowing_live = debt }}
        subtract_from_variable = {{ {P}war_borrowing_live = {P}war_entry_debt }}
        clamp_variable = {{ var = {P}war_borrowing_live min = 0 }}
    """)
    E("war_observer", f"""
        if = {{ limit = {{ has_war_with = PER }}
            if = {{ limit = {{ NOT = {{ has_country_flag = {P}iran_war_active }} }}
                set_country_flag = {P}iran_war_active
                set_country_flag = {P}iran_war_seen
                set_country_flag = {P}iran_war_start
                set_variable = {{ {P}war_entry_debt = debt }}
                set_variable = {{ {P}war_entry_gdp = gdp_total }}
                set_variable = {{ {P}war_threshold = gdp_total }}
                multiply_variable = {{ {P}war_threshold = 0.25 }}
                set_variable = {{ {P}war_borrowing_live = 0 }}
            }}
            {P}audit_war_borrowing = yes
        }}
        else_if = {{ limit = {{ has_country_flag = {P}iran_war_active }}
            {P}audit_war_borrowing = yes
            set_variable = {{ {P}war_borrowing_frozen = {P}war_borrowing_live }}
            if = {{ limit = {{
                has_country_flag = {{ flag = {P}iran_war_start days > 179 }}
                check_variable = {{ var = {P}war_borrowing_frozen value = {P}war_threshold compare = greater_than_or_equals }}
                check_variable = {{ debt > 0 }}
            }}
                add_ideas = {P}price_of_victory
                set_country_flag = {P}debt_policy_unlocked
                country_event = {{ id = COLDWAR_IRQ_gulf.10 }}
            }}
            clr_country_flag = {P}iran_war_active
            clr_country_flag = {P}iran_war_start
        }}
        {P}refresh_war_costs = yes
    """)

    # Bilateral transfers: offer identity is once-only per creditor in a campaign.
    for tag, label, fraction, event_id in CREDITORS:
        T("can_offer_" + tag, f"""
            {P}actor = yes
            has_country_flag = {P}credit_unlocked
            has_war_with = PER
            country_exists = {tag}
            is_subject = no
            NOT = {{ has_war_with = {tag} }}
            NOT = {{ has_country_flag = {P}offered_{tag} }}
            NOT = {{ has_country_flag = MD_skip_treasury_cost }}
            {tag} = {{ is_subject = no NOT = {{ has_capitulated = yes }} NOT = {{ has_country_flag = MD_skip_treasury_cost }} }}
            check_variable = {{ gdp_total > 0 }}
        """)
        T("can_accept_" + tag, f"""
            {P}actor = yes
            has_country_flag = {P}pending_{tag}
            NOT = {{ has_country_flag = {P}consumed_{tag} }}
            NOT = {{ has_country_flag = MD_skip_treasury_cost }}
            has_war_with = PER
            is_subject = no
            country_exists = {tag}
            NOT = {{ has_war_with = {tag} }}
            check_variable = {{ {P}offer_{tag} > 0 }}
            {tag} = {{
                is_subject = no
                NOT = {{ has_capitulated = yes }}
                NOT = {{ has_country_flag = MD_skip_treasury_cost }}
                check_variable = {{ var = treasury value = IRQ.{P}offer_{tag} compare = greater_than_or_equals }}
            }}
        """)
        E("offer_" + tag, f"""
            if = {{ limit = {{ {P}can_offer_{tag} = yes }}
                {P}reconcile_debt = yes
                set_variable = {{ {P}offer_{tag} = gdp_total }}
                multiply_variable = {{ {P}offer_{tag} = {fraction} }}
                set_country_flag = {P}offered_{tag}
                set_country_flag = {{ flag = {P}pending_{tag} days = 30 }}
                {tag} = {{ country_event = {{ id = COLDWAR_IRQ_gulf.{event_id} }} }}
            }}
        """)
        E("accept_" + tag, f"""
            if = {{ limit = {{ {P}can_accept_{tag} = yes }}
                {P}reconcile_debt = yes
                # Stamp the exact recipient-owned contract before native money effects.
                set_country_flag = {P}consumed_{tag}
                clr_country_flag = {P}pending_{tag}
                set_variable = {{ {P}principal_{tag} = {P}offer_{tag} }}
                {tag} = {{
                    set_temp_variable = {{ treasury_change = IRQ.{P}offer_{tag} }}
                    multiply_temp_variable = {{ treasury_change = -1 }}
                    modify_treasury_effect = yes
                }}
                set_temp_variable = {{ treasury_change = {P}offer_{tag} }}
                modify_treasury_effect = yes
                set_temp_variable = {{ debt_change = {P}offer_{tag} }}
                modify_debt_effect = yes
                set_variable = {{ {P}debt_snapshot = debt }}
                ingame_update_setup = yes
                country_event = {{ id = COLDWAR_IRQ_gulf.11 }}
            }}
        """)
        E("reject_" + tag, f"""
            if = {{ limit = {{ {P}actor = yes has_country_flag = {P}pending_{tag} }}
                clr_country_flag = {P}pending_{tag}
                set_country_flag = {P}refused_{tag}
                country_event = {{ id = COLDWAR_IRQ_gulf.12 }}
            }}
        """)
        T("can_repay_" + tag, f"""
            {P}actor = yes
            country_exists = {tag}
            NOT = {{ has_war_with = {tag} }}
            NOT = {{ has_country_flag = MD_skip_treasury_cost }}
            {tag} = {{ NOT = {{ has_country_flag = MD_skip_treasury_cost }} }}
            check_variable = {{ {P}principal_{tag} > 0 }}
            check_variable = {{ var = treasury value = {P}principal_{tag} compare = greater_than_or_equals }}
            check_variable = {{ var = debt value = {P}principal_{tag} compare = greater_than_or_equals }}
        """)
        E("repay_" + tag, f"""
            {P}reconcile_debt = yes
            if = {{ limit = {{ {P}can_repay_{tag} = yes }}
                set_variable = {{ {P}repayment_{tag} = {P}principal_{tag} }}
                set_variable = {{ {P}principal_{tag} = 0 }}
                set_country_flag = {P}repaid_{tag}
                set_temp_variable = {{ treasury_change = {P}repayment_{tag} }}
                multiply_temp_variable = {{ treasury_change = -1 }}
                modify_treasury_effect = yes
                set_temp_variable = {{ debt_change = {P}repayment_{tag} }}
                multiply_temp_variable = {{ debt_change = -1 }}
                modify_debt_effect = yes
                {tag} = {{
                    set_temp_variable = {{ treasury_change = IRQ.{P}repayment_{tag} }}
                    modify_treasury_effect = yes
                }}
                set_variable = {{ {P}debt_snapshot = debt }}
                ingame_update_setup = yes
            }}
        """)
        events.append(block("country_event", f"""
            id = COLDWAR_IRQ_gulf.{event_id}
            title = {P}loan_{tag}_title
            desc = {P}loan_{tag}_desc
            picture = GFX_report_event_generic_diplomacy
            is_triggered_only = yes
            option = {{
                name = {P}loan_accept
                trigger = {{ tag = {tag} FROM = {{ tag = IRQ }} IRQ = {{ {P}can_accept_{tag} = yes }} }}
                ai_chance = {{ factor = 50 }}
                custom_effect_tooltip = {P}loan_accept_tt
                IRQ = {{ {P}accept_{tag} = yes }}
            }}
            option = {{
                name = {P}loan_decline
                ai_chance = {{ factor = 50 }}
                if = {{ limit = {{ tag = {tag} FROM = {{ tag = IRQ }} }} IRQ = {{ {P}reject_{tag} = yes }} }}
            }}
        """))
        D("request_" + tag, f"""
            icon = generic_economic_policy
            cost = 25
            visible = {{ {P}can_offer_{tag} = yes }}
            available = {{ {P}can_offer_{tag} = yes }}
            complete_effect = {{ {P}offer_{tag} = yes }}
            ai_will_do = {{ factor = 1 }}
        """)
        D("repay_" + tag, f"""
            icon = generic_economic_policy
            cost = 0
            visible = {{ check_variable = {{ {P}principal_{tag} > 0 }} }}
            available = {{ {P}can_repay_{tag} = yes }}
            complete_effect = {{ {P}repay_{tag} = yes }}
            ai_will_do = {{ factor = 1 }}
        """)
        L(P + "request_" + tag, f"Request Wartime Credit from {label}", f"Offer a single bilateral loan of {fraction:.0%} of current Iraqi GDP. The amount is frozen when dispatched and expires after 30 days. {label} must accept and have the entire amount in its treasury. Acceptance transfers real funds and adds equal native Iraqi debt; it never grants equipment. Refusal leaves the Iranian war route open. One offer per creditor in this campaign.")
        L(P + "repay_" + tag, f"Repay {label}", f"Pay the remaining named principal to {label} and remove exactly that amount from native Iraqi debt. The recipient receives the treasury transfer once. Unassigned native debt reductions conservatively retire named Gulf principal first; they cannot create a second repayment or cancellation.")
        L(P + "loan_" + tag + "_title", f"Iraq Requests Credit from {label}")
        loc[P + "loan_" + tag + "_desc"] = f"Baghdad requests $[?IRQ.{P}offer_{tag}|3] billion for its actual war against Iran. Acceptance immediately debits our treasury, credits Iraq, and records an equal Iraqi debt principal. This is a loan, not a grant. The frozen offer expires after 30 days; duplicates and lost eligibility cannot transfer funds."

    E("forgive_kuwait_principal", f"""
        {P}reconcile_debt = yes
        set_variable = {{ {P}kuwait_cancelled = {P}principal_KUW }}
        if = {{ limit = {{ check_variable = {{ {P}kuwait_cancelled > 0 }} }}
            set_variable = {{ {P}principal_KUW = 0 }}
            set_temp_variable = {{ debt_change = {P}kuwait_cancelled }}
            multiply_temp_variable = {{ debt_change = -1 }}
            modify_debt_effect = yes
            set_variable = {{ {P}debt_snapshot = debt }}
            ingame_update_setup = yes
        }}
    """)
    E("request_kuwait_forgiveness", f"""
        {P}reconcile_debt = yes
        if = {{ limit = {{
            {P}postwar = yes country_exists = KUW
            NOT = {{ has_war_with = KUW }}
            NOT = {{ has_country_flag = {P}forgiveness_requested }}
            check_variable = {{ {P}principal_KUW > 0 }}
        }}
            set_country_flag = {P}forgiveness_requested
            set_country_flag = {{ flag = {P}forgiveness_pending days = 30 }}
            KUW = {{ country_event = {{ id = COLDWAR_IRQ_gulf.20 }} }}
        }}
    """)
    E("raise_oil_dispute", f"""
        if = {{ limit = {{
            {P}postwar = yes country_exists = KUW
            NOT = {{ has_war_with = KUW }}
            NOT = {{ has_country_flag = {P}oil_dispute_sent }}
        }}
            set_country_flag = {P}oil_dispute_sent
            set_country_flag = {{ flag = {P}oil_dispute_pending days = 30 }}
            KUW = {{ country_event = {{ id = COLDWAR_IRQ_gulf.21 }} }}
        }}
    """)
    E("claim_kuwait", f"""
        if = {{ limit = {{ {P}postwar = yes NOT = {{ has_country_flag = {P}kuwait_claimed }} }}
            add_state_claim = 172
            add_state_claim = 488
            add_war_support = 0.05
            set_country_flag = {P}kuwait_claimed
        }}
    """)
    E("kuwait_ultimatum", f"""
        if = {{ limit = {{ {P}can_ultimatum = yes }}
            set_country_flag = {P}ultimatum_issued
            set_temp_variable = {{ wargoal_on = KUW }}
            set_temp_variable = {{ wargoal_type = 2 }}
            add_threat_from_wargoal_effect = yes
            create_wargoal = {{ type = take_state_focus target = KUW generator = {{ 172 488 }} expire = 180 }}
            custom_effect_tooltip = {P}ultimatum_tt
        }}
    """)
    E("seize_kuwait_treasury", f"""
        # Actual accessible treasury only; no sovereign fund or oil wealth is invented.
        if = {{ limit = {{
            {P}actor = yes
            has_country_flag = {P}invaded_kuwait
            {P}controls_kuwait = yes
            country_exists = KUW
            NOT = {{ has_country_flag = {P}treasury_seizure_consumed }}
            NOT = {{ has_country_flag = MD_skip_treasury_cost }}
            KUW = {{ NOT = {{ has_country_flag = MD_skip_treasury_cost }} }}
        }}
            set_country_flag = {P}treasury_seizure_consumed
            set_variable = {{ {P}seizure_amount = KUW.treasury }}
            multiply_variable = {{ {P}seizure_amount = 0.25 }}
            clamp_variable = {{ var = {P}seizure_amount min = 0 }}
            set_temp_variable = {{ {P}seizure_cap = gdp_total }}
            multiply_temp_variable = {{ {P}seizure_cap = 0.10 }}
            if = {{ limit = {{ check_variable = {{ {P}seizure_amount > {P}seizure_cap }} }}
                set_variable = {{ {P}seizure_amount = {P}seizure_cap }}
            }}
            if = {{ limit = {{ check_variable = {{ {P}seizure_amount > 0 }} }}
                KUW = {{
                    set_temp_variable = {{ treasury_change = IRQ.{P}seizure_amount }}
                    multiply_temp_variable = {{ treasury_change = -1 }}
                    modify_treasury_effect = yes
                }}
                set_temp_variable = {{ treasury_change = {P}seizure_amount }}
                modify_treasury_effect = yes
            }}
        }}
    """)
    E("kuwait_conquest_relief", f"""
        if = {{ limit = {{
            {P}actor = yes {P}owns_kuwait = yes
            has_country_flag = {P}invaded_kuwait
            NOT = {{ has_country_flag = {P}conquest_relief_consumed }}
        }}
            set_country_flag = {P}conquest_relief_consumed
            {P}forgive_kuwait_principal = yes
            if = {{ limit = {{ has_idea = {P}price_of_victory }} remove_ideas = {P}price_of_victory }}
            add_timed_idea = {{ idea = {P}captured_assets_repair days = 180 }}
            # Existing controlled state resources return through native rules.
            # No add_resource, free oil, factory or third-party debt cancellation.
            country_event = {{ id = COLDWAR_IRQ_gulf.30 }}
            ingame_update_setup = yes
        }}
    """)
    E("integrate_kuwait", f"""
        set_temp_variable = {{ {P}integration_invoice = gdp_total }}
        multiply_temp_variable = {{ {P}integration_invoice = 0.05 }}
        if = {{ limit = {{
            {P}can_integrate = yes
            NOT = {{ has_political_power < 100 }}
            check_variable = {{ var = treasury value = {P}integration_invoice compare = greater_than_or_equals }}
        }}
            set_country_flag = {P}kuwait_integrated
            add_political_power = -100
            set_temp_variable = {{ treasury_change = {P}integration_invoice }}
            multiply_temp_variable = {{ treasury_change = -1 }}
            modify_treasury_effect = yes
            172 = {{ add_core_of = IRQ }}
            488 = {{ add_core_of = IRQ }}
            custom_effect_tooltip = {P}integration_tt
            ingame_update_setup = yes
        }}
    """)
    E("fund_recovery", f"""
        set_temp_variable = {{ {P}recovery_invoice = gdp_total }}
        multiply_temp_variable = {{ {P}recovery_invoice = 0.02 }}
        set_temp_variable = {{ {P}recovery_debt_cap = gdp_total }}
        multiply_temp_variable = {{ {P}recovery_debt_cap = 0.20 }}
        if = {{ limit = {{
            {P}postwar = yes has_war = no has_idea = {P}price_of_victory
            NOT = {{ has_country_flag = MD_skip_treasury_cost }}
            NOT = {{ has_political_power < 50 }}
            check_variable = {{ var = debt value = {P}recovery_debt_cap compare = less_than_or_equals }}
            check_variable = {{ var = treasury value = {P}recovery_invoice compare = greater_than_or_equals }}
        }}
            set_temp_variable = {{ treasury_change = {P}recovery_invoice }}
            multiply_temp_variable = {{ treasury_change = -1 }}
            modify_treasury_effect = yes
            add_political_power = -50
            remove_ideas = {P}price_of_victory
            ingame_update_setup = yes
        }}
    """)
    E("daily", f"""
        if = {{ limit = {{ {P}actor = yes }}
            {P}initialize = yes
            set_variable = {{ {P}integration_cost_display = gdp_total }}
            multiply_variable = {{ {P}integration_cost_display = 0.05 }}
            set_variable = {{ {P}recovery_cost_display = gdp_total }}
            multiply_variable = {{ {P}recovery_cost_display = 0.02 }}
            set_variable = {{ {P}recovery_debt_cap_display = gdp_total }}
            multiply_variable = {{ {P}recovery_debt_cap_display = 0.20 }}
            {P}reconcile_debt = yes
            {P}war_observer = yes
            if = {{ limit = {{
                {P}owns_kuwait = yes has_war = no has_stability > 0.50
            }}
                if = {{ limit = {{ NOT = {{ has_country_flag = {P}stable_kuwait }} }}
                    set_country_flag = {P}stable_kuwait
                }}
            }}
            else = {{ clr_country_flag = {P}stable_kuwait }}
            {P}seize_kuwait_treasury = yes
            {P}kuwait_conquest_relief = yes
        }}
    """)

    D("forgiveness", f"""
        icon = generic_economic_policy
        cost = 50
        visible = {{ {P}postwar = yes country_exists = KUW check_variable = {{ {P}principal_KUW > 0 }} NOT = {{ has_country_flag = {P}forgiveness_requested }} }}
        available = {{ NOT = {{ has_war_with = KUW }} }}
        complete_effect = {{ {P}request_kuwait_forgiveness = yes }}
        ai_will_do = {{ factor = 1 }}
    """)
    D("oil_dispute", f"""
        icon = generic_economic_policy
        cost = 50
        visible = {{ {P}postwar = yes country_exists = KUW NOT = {{ has_country_flag = {P}oil_dispute_sent }} }}
        available = {{ NOT = {{ has_war_with = KUW }} }}
        complete_effect = {{ {P}raise_oil_dispute = yes }}
        ai_will_do = {{ factor = 1 }}
    """)
    D("claim", f"""
        icon = generic_prepare_civil_war
        cost = 50
        visible = {{ {P}postwar = yes has_country_flag = {P}debt_policy_unlocked NOT = {{ has_country_flag = {P}kuwait_claimed }} }}
        available = {{ country_exists = KUW is_subject = no NOT = {{ has_war_with = KUW }} }}
        complete_effect = {{ {P}claim_kuwait = yes }}
        ai_will_do = {{ factor = 0.2 }}
    """)
    D("ultimatum", f"""
        icon = generic_prepare_civil_war
        cost = 75
        visible = {{ has_country_flag = {P}kuwait_claimed NOT = {{ has_country_flag = {P}ultimatum_issued }} }}
        available = {{ {P}can_ultimatum = yes }}
        complete_effect = {{ {P}kuwait_ultimatum = yes }}
        ai_will_do = {{ factor = 0.2 }}
    """)
    D("integration", f"""
        icon = generic_political_reform
        cost = 0
        custom_cost_text = {P}integration_cost
        custom_cost_trigger = {{ NOT = {{ has_political_power < 100 }} }}
        visible = {{ has_country_flag = {P}integration_unlocked {P}owns_kuwait = yes NOT = {{ has_country_flag = {P}kuwait_integrated }} }}
        available = {{
            {P}can_integrate = yes
            check_variable = {{ var = treasury value = {P}integration_cost_display compare = greater_than_or_equals }}
        }}
        complete_effect = {{ {P}integrate_kuwait = yes }}
        ai_will_do = {{ factor = 1 }}
    """)
    D("recovery", f"""
        icon = generic_economic_policy
        cost = 0
        custom_cost_text = {P}recovery_cost
        custom_cost_trigger = {{ NOT = {{ has_political_power < 50 }} }}
        visible = {{ {P}postwar = yes has_idea = {P}price_of_victory }}
        available = {{
            has_war = no
            NOT = {{ has_country_flag = MD_skip_treasury_cost }}
            check_variable = {{ var = debt value = {P}recovery_debt_cap_display compare = less_than_or_equals }}
            check_variable = {{ var = treasury value = {P}recovery_cost_display compare = greater_than_or_equals }}
        }}
        complete_effect = {{ {P}fund_recovery = yes }}
        ai_will_do = {{ factor = 1 }}
    """)

    events.append(block("country_event", f"""
        id = COLDWAR_IRQ_gulf.20
        title = {P}forgiveness_title
        desc = {P}forgiveness_desc
        picture = GFX_report_event_generic_diplomacy
        is_triggered_only = yes
        option = {{
            name = {P}forgive_accept
            trigger = {{ tag = KUW FROM = {{ tag = IRQ }} IRQ = {{ {P}postwar = yes has_country_flag = {P}forgiveness_pending NOT = {{ has_war_with = KUW }} check_variable = {{ {P}principal_KUW > 0 }} }} }}
            ai_chance = {{ factor = 15 }}
            if = {{ limit = {{
                tag = KUW FROM = {{ tag = IRQ }}
                IRQ = {{
                    {P}postwar = yes
                    has_country_flag = {P}forgiveness_pending
                    NOT = {{ has_war_with = KUW }}
                    check_variable = {{ {P}principal_KUW > 0 }}
                }}
            }}
                IRQ = {{
                    clr_country_flag = {P}forgiveness_pending
                    {P}forgive_kuwait_principal = yes
                    set_country_flag = {P}kuwait_forgave
                }}
            }}
        }}
        option = {{
            name = {P}forgive_reject
            ai_chance = {{ factor = 85 }}
            if = {{ limit = {{ tag = KUW FROM = {{ tag = IRQ }} IRQ = {{ has_country_flag = {P}forgiveness_pending }} }}
                IRQ = {{ clr_country_flag = {P}forgiveness_pending set_country_flag = {P}kuwait_refused_forgiveness }}
            }}
        }}
    """))
    events.append(block("country_event", f"""
        id = COLDWAR_IRQ_gulf.21
        title = {P}oil_title
        desc = {P}oil_desc
        picture = GFX_report_event_generic_diplomacy
        is_triggered_only = yes
        option = {{
            name = {P}oil_reject
            ai_chance = {{ factor = 75 }}
            if = {{ limit = {{ tag = KUW FROM = {{ tag = IRQ }} IRQ = {{ has_country_flag = {P}oil_dispute_pending }} }}
                IRQ = {{ clr_country_flag = {P}oil_dispute_pending set_country_flag = {P}oil_dispute_rejected }}
            }}
        }}
        option = {{
            name = {P}oil_arbitrate
            ai_chance = {{ factor = 25 }}
            if = {{ limit = {{ tag = KUW FROM = {{ tag = IRQ }} IRQ = {{ has_country_flag = {P}oil_dispute_pending }} }}
                IRQ = {{
                    clr_country_flag = {P}oil_dispute_pending
                    set_country_flag = {P}oil_dispute_rejected
                    set_country_flag = {{ flag = {P}arbitration_window days = 90 }}
                }}
            }}
        }}
    """))
    for number, label in ((10, "price_notice"), (11, "credit_notice"), (12, "refusal_notice"), (30, "conquest_notice")):
        events.append(block("country_event", f"""
            id = COLDWAR_IRQ_gulf.{number}
            title = {P}{label}_title
            desc = {P}{label}_desc
            picture = GFX_report_event_generic_diplomacy
            is_triggered_only = yes
            option = {{ name = {P}acknowledge }}
        """))

    idea_entries = []
    for i, (personnel, equipment) in enumerate(((1, .5), (1.75, 1), (2.5, 1.5)), 1):
        idea_entries.append(block(P + f"iran_cost_{i}", f"""
            picture = gulf_war_dam
            allowed = {{ always = no }}
            modifier = {{
                army_personnel_cost_multiplier_modifier = {personnel}
                equipment_cost_multiplier_modifier = {equipment}
            }}
        """))
        L(P + f"iran_cost_{i}", ("The Iranian War Bill", "A War of Replacement", "The Third Campaign Season")[i-1], f"The war against Iran adds {personnel:.0%} to the native army-personnel cost component and {equipment:.0%} to the native equipment operating-cost component, including deployed land equipment and discounted stockpiles. These are additional additive MD component modifiers, not the total military budget multiplier. Exactly one tier applies; peace with Iran removes it. The normal weekly economy charges the cost and uses native deficit borrowing.")
    idea_entries.append(block(P + "price_of_victory", """
        picture = gulf_war_dam
        allowed = { always = no }
        modifier = {
            production_speed_buildings_factor = -0.30
            tax_gain_multiplier_modifier = -0.20
            stability_factor = -0.10
            interest_rate_multiplier_modifier = 2
            consumer_goods_factor = 0.20
        }
    """))
    idea_entries.append(block(P + "captured_assets_repair", """
        picture = embargo
        allowed = { always = no }
        modifier = { industry_repair_factor = 0.50 }
    """))

    L(P + "category", "War Finance and the Gulf", "Iranian war costs flow through the native weekly MD budget. Named Gulf loans require the creditor's acceptance and real funds. Outstanding principal is reconciled against actual native debt before repayment or cancellation. Territorial claims do not transfer land or resources.")
    L(P + "price_of_victory", "The Price of Victory", "A war against Iran lasting at least 180 days left net new native debt of at least 25% of entry GDP. The frozen audit excludes pre-war debt. Construction -30%; tax gains -20%; stability -10 percentage points; interest-rate premium +2 percentage points before native clamps; Tax Cost Factor (Consumer Goods) +20% relative to its native base. Fund recovery after debt falls to 20% of GDP, or pursue the hazardous Kuwaiti crisis route. This burden does not grant anyone a forced peace.")
    L(P + "captured_assets_repair", "Reorganising Captured Assets", "For 180 days, building repair speed increases by 50%. This national repair modifier creates no oil, buildings, GDP, treasury or resources; existing territorial assets remain subject to native ownership, control and damage rules.")
    L(P + "forgiveness", "Demand Kuwaiti Debt Forgiveness", "Ask Kuwait to cancel only its remaining named wartime loan. Kuwait may refuse. Neither refusal nor silence transfers any money or cancels other creditors' debt. A historical grievance can escalate into an ultimatum; it does not make invasion inevitable.")
    L(P + "oil_dispute", "Press the Kuwaiti Oil Dispute", "Accuse Kuwait of using oil policy against Iraqi recovery. Kuwait can reject the accusation or seek a 90-day arbitration interval. This diplomatic grievance does not fabricate oil production changes or oblige another player to accept Iraqi claims.")
    L(P + "claim", "Assert the Kuwaiti Claim", "Gain Iraqi claims on Kuwait (172) and the Kuwaiti naval coast (488), and 5 percentage points of war support. This alternative escalation grants no cores, ownership, oil, money or immediate war.")
    L(P + "ultimatum", "Deliver the Kuwaiti Ultimatum", "After an actual rejection and outside a live arbitration interval, obtain a 180-day conquest war goal for states 172 and 488. The Iraqi player chooses whether to declare. Native tension, treaties and coalition responses still apply.")
    L(P + "integration", "Integrate the Kuwaiti Provinces", "Requires the integration programme, legal ownership and control of both Kuwaiti states, peace and stability above 50% continuously for 180 days. Pay 5% of live Iraqi GDP and 100 political power. Then grant cores to states 172 and 488 once. Any loss of control, ownership, peace or sufficient stability resets the observation period. This is an alternative-history consolidation, not a claim of automatic historical consent.")
    L(P + "recovery", "Fund Postwar Recovery", "At peace, after native debt falls to 20% of current GDP or less, pay 2% of current GDP and remove The Price of Victory. No debt is forgiven by this decision.")
    L(P + "loan_accept", "Approve the loan and transfer the funds.")
    L(P + "loan_decline", "Decline the request.")
    L(P + "loan_accept_tt", "Transfer the entire frozen principal to Iraq once. Iraq records equal native debt and a named repayable principal. The sender, pending offer, expiry, treasury, war and recipient are checked again before execution.")
    L(P + "forgiveness_title", "Baghdad Demands Debt Forgiveness")
    loc[P + "forgiveness_desc"] = f"Iraq demands cancellation of its remaining Kuwaiti wartime principal: $[?IRQ.{P}principal_KUW|3] billion before live reconciliation. Cancellation removes only the actual surviving named principal; other native Iraqi debt remains. Kuwait receives no cash for writing off its claim."
    L(P + "forgive_accept", "Write off the surviving Kuwaiti principal.")
    L(P + "forgive_reject", "The loan remains repayable.")
    L(P + "oil_title", "Iraq Challenges Kuwaiti Oil Policy")
    loc[P + "oil_desc"] = "Baghdad blames Kuwaiti oil policy for its financial difficulties. These are Iraqi political accusations, not an automatic finding of fact. Rejecting them gives Iraq an escalation pretext; seeking arbitration postpones its ultimatum for 90 days. Neither response changes oil resources or obliges acceptance of territorial claims."
    L(P + "oil_reject", "Reject Baghdad's accusations.")
    L(P + "oil_arbitrate", "Seek a ninety-day arbitration interval.")
    L(P + "price_notice_title", "The Price of Victory")
    loc[P + "price_notice_desc"] = f"The war with Iran has ended, but native debt rose by $[?{P}war_borrowing_frozen|3] billion above its entry balance. The long-war threshold was $[?{P}war_threshold|3] billion. The frozen audit now applies The Price of Victory. This is actual net borrowing during the war, not a scripted historical debt grant or a claim that every debt transaction was caused solely by the fighting."
    L(P + "credit_notice_title", "Gulf Credit Has Arrived")
    loc[P + "credit_notice_desc"] = "A creditor accepted the frozen request and transferred actual treasury funds. Equal debt and a named principal are recorded in Iraq. This brings liquidity, not free income, equipment or guaranteed victory."
    L(P + "refusal_notice_title", "A Gulf Creditor Refuses")
    loc[P + "refusal_notice_desc"] = "The requested loan was refused. No treasury or debt changed. Its refusal does not block Iraq's independent military decisions."
    L(P + "conquest_notice_title", "The Kuwaiti Accounts")
    loc[P + "conquest_notice_desc"] = f"Iraq legally owns and controls both Kuwaiti states. Only the remaining Kuwaiti principal was cancelled: $[?{P}kuwait_cancelled|3] billion. Other debt survives. A separate, one-use seizure can transfer only 25% of accessible Kuwaiti treasury, capped at 10% of Iraqi GDP, while Kuwait still exists and both states are occupied. No missing reserve is invented. The Price of Victory is removed and a 180-day building-repair programme begins. Existing oil follows native ownership and control; no extra resource deposit appears. International opposition to the invasion remains."
    L(P + "acknowledge", "Acknowledge the position.")
    L(P + "ultimatum_tt", "Gain a conquest war goal for Kuwait and its naval coast, valid for 180 days. Declaration remains a separate player action.")
    L(P + "integration_tt", "Kuwait and its naval coast become Iraqi cores after the paid 180-day consolidation. No other states are affected.")
    L(P + "integration_cost", "100 £pol_power + 5% GDP")
    L(P + "recovery_cost", "50 £pol_power + 2% GDP")

    on_actions = text(f"""
        on_actions = {{
            on_startup = {{ effect = {{ IRQ = {{ if = {{ limit = {{ {P}actor = yes }} {P}initialize = yes }} }} }} }}
            on_daily = {{ effect = {{ if = {{ limit = {{ {P}actor = yes }} {P}daily = yes }} }} }}
            on_war_relation_added = {{ effect = {{
                if = {{ limit = {{
                    OR = {{
                        AND = {{ ROOT = {{ tag = IRQ }} FROM = {{ tag = PER }} }}
                        AND = {{ ROOT = {{ tag = PER }} FROM = {{ tag = IRQ }} }}
                    }}
                }} IRQ = {{ {P}war_observer = yes }} }}
            }} }}
            on_peaceconference_ended = {{ effect = {{ IRQ = {{ {P}war_observer = yes }} }} }}
            # Native contract: ROOT attacker; FROM defender. The record persists
            # after a fast occupation, annexation, peace or save/reload.
            on_declare_war = {{ effect = {{
                if = {{ limit = {{ ROOT = {{ {P}actor = yes }} FROM = {{ tag = KUW }} }}
                    ROOT = {{ set_country_flag = {P}invaded_kuwait }}
                    set_global_flag = {P}iraq_attacked_kuwait
                }}
            }} }}
            # ROOT capitulated country; FROM winning country. A late daily
            # observation retries only while real Kuwaiti funds remain accessible.
            on_capitulation_immediate = {{ effect = {{
                if = {{ limit = {{ ROOT = {{ tag = KUW }} FROM = {{ {P}actor = yes }} }}
                    FROM = {{ {P}seize_kuwait_treasury = yes }}
                }}
            }} }}
            # ROOT annexer; FROM annexed. Do not bypass legal ownership guards.
            on_annex = {{ effect = {{
                if = {{ limit = {{ ROOT = {{ {P}actor = yes }} FROM = {{ tag = KUW }} }}
                    ROOT = {{ {P}seize_kuwait_treasury = yes {P}kuwait_conquest_relief = yes }}
                }}
            }} }}
        }}
    """)
    header = '# IMPERIA CW — Cold War: iraq 1970 generated content.\n# COLDWAR IRQ | Fresh 1970 campaign Gulf module. Generated by tools/iraq_1970/gulf_module.py.\n# No retained 1985 helpers are used.\n\n'
    result = {
        "common/scripted_effects/COLDWAR_IRQ_gulf_effects.txt": header + "".join(effects),
        "common/scripted_triggers/COLDWAR_IRQ_gulf_triggers.txt": header + "".join(triggers),
        "common/ideas/COLDWAR_IRQ_gulf_ideas.txt": header + block("ideas", block("country", "".join(idea_entries))),
        "common/decisions/COLDWAR_IRQ_gulf_decisions.txt": header + block(P + "category", "".join(decisions)),
        "common/decisions/categories/COLDWAR_IRQ_gulf_categories.txt": header + block(P + "category", f"icon = generic_economic_policy\nallowed = {{ tag = IRQ }}\nvisible = {{ {P}actor = yes }}"),
        "events/COLDWAR_IRQ_gulf_events.txt": header + "add_namespace = COLDWAR_IRQ_gulf\n\n" + "".join(events),
        "common/on_actions/COLDWAR_IRQ_gulf_on_actions.txt": header + on_actions,
        "localisation/english/COLDWAR_IRQ_gulf_l_english.yml": '\ufeffl_english:\n# IMPERIA CW — Cold War: iraq 1970 English localisation.\n' + "\n".join(" " + key + ":0 " + json.dumps(value, ensure_ascii=False) for key, value in loc.items()) + "\n",
    }
    # Decision icons and event pictures use verified native sprite names.
    # The category's generic_economic_policy sprite is separately registered.
    result["common/decisions/COLDWAR_IRQ_gulf_decisions.txt"] = result["common/decisions/COLDWAR_IRQ_gulf_decisions.txt"].replace("icon = generic_economic_policy", "icon = money_dec").replace("icon = generic_prepare_civil_war", "icon = war").replace("icon = generic_political_reform", "icon = politics")
    result["events/COLDWAR_IRQ_gulf_events.txt"] = result["events/COLDWAR_IRQ_gulf_events.txt"].replace("GFX_report_event_generic_diplomacy", "GFX_politics_demands")
    return result


def self_test(root: Path) -> dict:
    """Execute the emitted transaction/observer AST in a strict bounded model.

    This does not emulate engine UI, real dates, war creation, weekly native
    economy accrual, savegame serialization, native tension or MP event queues.
    Unknown authored statements fail; only listed native refresh hooks are stubs.
    """
    import importlib.util
    from copy import deepcopy
    root = Path(root)
    spec = importlib.util.spec_from_file_location("irq_gulf_ast", root / "tools/vietnam_1970/script_ast.py")
    parser = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parser)
    parse, first, values, walk = parser.parse, parser.first, parser.values, parser.walk
    out = generate(root)
    asts = {p: parse(s) for p, s in out.items() if p.endswith(".txt")}
    e = dict((k, v) for k, _, v in asts["common/scripted_effects/COLDWAR_IRQ_gulf_effects.txt"])
    t = dict((k, v) for k, _, v in asts["common/scripted_triggers/COLDWAR_IRQ_gulf_triggers.txt"])
    event_rows = {first(v, "id"): v for v in values(asts["events/COLDWAR_IRQ_gulf_events.txt"], "country_event")}
    native_budget = {k: v for k, _, v in parse((root / "common/scripted_effects/00_budget_effects.txt").read_text(encoding="utf-8-sig"))}
    e.update({k: native_budget[k] for k in ("modify_treasury_effect", "modify_debt_effect")})
    checks = []

    def check(value, label):
        if not value:
            raise AssertionError(label)
        checks.append(label)

    class World:
        def __init__(self):
            self.day = 0
            self.c = {tag: dict(tag=tag, variables={"gdp_total": 100., "debt": 10., "treasury": 20., "political_power": 200.}, flags={}, ideas={}, wars=set(), exists=True, subject=False, stability=.6, factions=set(), pacts=set(), campaign=True, capitulated=False) for tag in ("IRQ", "PER", "KUW", "SAU", "UAE", "USA")}
            self.states = {i: dict(owner="KUW", controller="KUW", cores={"KUW"}, claims=set()) for i in (172, 488)}
            self.events, self.goals = [], []
            self.event_from = "IRQ"
            self.call("initialize")

        def number(self, value, scope):
            try:
                return float(value)
            except (ValueError, TypeError):
                if "." in value and value.split(".", 1)[0] in self.c:
                    tag, var = value.split(".", 1)
                    return self.c[tag]["variables"].get(var, 0.)
                return self.c[scope]["variables"].get(value, 0.)

        def flag(self, scope, key):
            item = self.c[scope]["flags"].get(key)
            return item is not None and (item[1] is None or self.day < item[0] + item[1])

        def test(self, rows, scope="IRQ"):
            return all(self.condition(k, o, v, scope) for k, o, v in rows)

        def condition(self, key, op, value, scope):
            if key in ("AND", "limit"):
                return self.test(value, scope)
            if key == "NOT":
                return not self.test(value, scope)
            if key == "OR":
                return any(self.condition(k, o, v, scope) for k, o, v in value)
            if key in self.c:
                return self.test(value, key)
            if key == "FROM":
                return self.test(value, self.event_from)
            if key.isdigit():
                state = self.states[int(key)]
                return all(state[{"is_owned_by": "owner", "is_controlled_by": "controller"}[k]] == v for k, _, v in value)
            if key in t:
                return self.test(t[key], scope) == (value == "yes")
            c = self.c[scope]
            if key == "COLDWAR_IRQ_campaign_active":
                return c["campaign"] == (value == "yes")
            if key == "tag":
                return scope == value
            if key == "exists":
                return c["exists"] == (value == "yes")
            if key == "has_country_flag":
                if isinstance(value, list):
                    flag = first(value, "flag")
                    rule = next(r for r in value if r[0] == "days")
                    return self.flag(scope, flag) and self.compare(self.day - c["flags"][flag][0], rule[1], float(rule[2]))
                return self.flag(scope, value)
            if key == "has_idea":
                return value in c["ideas"] and (c["ideas"][value] is None or c["ideas"][value] > self.day)
            if key == "has_war_with":
                return value in c["wars"]
            if key == "has_war":
                return bool(c["wars"]) == (value == "yes")
            if key == "is_subject":
                return c["subject"] == (value == "yes")
            if key == "has_capitulated":
                return c["capitulated"] == (value == "yes")
            if key == "country_exists":
                return self.c[value]["exists"]
            if key == "has_stability":
                return self.compare(c["stability"], op, float(value))
            if key == "has_political_power":
                return self.compare(c["variables"]["political_power"], op, float(value))
            if key == "is_in_faction_with":
                return value in c["factions"]
            if key == "has_non_aggression_pact_with":
                return value in c["pacts"]
            if key == "check_variable":
                if first(value, "var"):
                    operations = {"greater_than_or_equals": ">=", "less_than_or_equals": "<=", "equals": "="}
                    return self.compare(self.number(first(value, "var"), scope), operations[first(value, "compare")], self.number(first(value, "value"), scope))
                a, operation, b = value[0]
                return self.compare(self.number(a, scope), operation, self.number(b, scope))
            raise AssertionError("Unsupported condition: " + key)

        @staticmethod
        def compare(a, op, b):
            return {"=": a == b, ">": a > b, "<": a < b, ">=": a >= b, "<=": a <= b}[op]

        def execute(self, rows, scope="IRQ"):
            previous_taken = False
            for key, _, value in rows:
                if key in ("if", "else_if", "else"):
                    if key == "if":
                        previous_taken = False
                    take = not previous_taken and (key == "else" or self.test(first(value, "limit", []), scope))
                    if take:
                        self.execute([r for r in value if r[0] != "limit"], scope)
                        previous_taken = True
                    continue
                previous_taken = False
                if key in self.c:
                    self.execute(value, key)
                elif key.isdigit():
                    for k, _, v in value:
                        if k != "add_core_of":
                            raise AssertionError("Unsupported state effect: " + k)
                        self.states[int(key)]["cores"].add(v)
                elif key in e:
                    self.execute(e[key], scope)
                elif key in ("set_variable", "set_temp_variable", "add_to_variable", "add_to_temp_variable", "subtract_from_variable", "subtract_from_temp_variable", "multiply_variable", "multiply_temp_variable"):
                    var, _, operand = value[0]
                    operand = self.number(operand, scope)
                    old = self.c[scope]["variables"].get(var, 0.)
                    self.c[scope]["variables"][var] = operand if key.startswith("set_") else old + operand if key.startswith("add_") else old - operand if key.startswith("subtract_") else old * operand
                elif key == "clamp_variable":
                    var = first(value, "var")
                    low, high = first(value, "min"), first(value, "max")
                    result = self.c[scope]["variables"].get(var, 0.)
                    if low is not None:
                        result = max(result, self.number(low, scope))
                    if high is not None:
                        result = min(result, self.number(high, scope))
                    self.c[scope]["variables"][var] = result
                elif key == "set_country_flag":
                    flag = first(value, "flag") if isinstance(value, list) else value
                    duration = int(first(value, "days")) if isinstance(value, list) and first(value, "days") else None
                    self.c[scope]["flags"][flag] = (self.day, duration)
                elif key == "clr_country_flag":
                    self.c[scope]["flags"].pop(value, None)
                elif key == "add_ideas":
                    self.c[scope]["ideas"][value] = None
                elif key == "remove_ideas":
                    self.c[scope]["ideas"].pop(value, None)
                elif key == "add_timed_idea":
                    self.c[scope]["ideas"][first(value, "idea")] = self.day + int(first(value, "days"))
                elif key == "country_event":
                    self.events.append((scope, first(value, "id")))
                elif key == "create_wargoal":
                    self.goals.append((scope, first(value, "target")))
                elif key == "add_state_claim":
                    self.states[int(value)]["claims"].add(scope)
                elif key == "add_war_support":
                    self.c[scope]["variables"]["test_war_support"] = self.c[scope]["variables"].get("test_war_support", 0.) + float(value)
                elif key == "add_political_power":
                    self.c[scope]["variables"]["political_power"] += float(value)
                elif key in ("ingame_update_setup", "update_money_dirty_variable", "custom_effect_tooltip", "add_threat_from_wargoal_effect"):
                    pass
                else:
                    raise AssertionError("Unsupported effect: " + key)

        def call(self, name, scope="IRQ"):
            self.execute(e[P + name], scope)

        def war(self):
            self.c["IRQ"]["wars"].add("PER")
            self.call("war_observer")

        def offer(self, tag="KUW"):
            self.war()
            self.call("unlock_credit")
            self.call("offer_" + tag)

        def money(self):
            return tuple((tag, c["variables"]["treasury"], c["variables"]["debt"]) for tag, c in self.c.items())

    for path, rows in asts.items():
        check(not any(op in (">=", "<=", "!=") for _, op, _ in walk(rows)), "Native comparison syntax: " + path)
    check(out["localisation/english/COLDWAR_IRQ_gulf_l_english.yml"].startswith("\ufeffl_english:"), "English localization BOM")
    w = World(); w.offer(); w.c["KUW"]["variables"]["treasury"] = 7.999
    before = w.money(); w.call("accept_KUW")
    check(w.money() == before, "Insufficient creditor treasury causes no transfer or debt")
    w.c["KUW"]["variables"]["treasury"] = 8.; w.call("accept_KUW")
    check(w.c["IRQ"]["variables"]["treasury"] == 28. and w.c["IRQ"]["variables"]["debt"] == 18. and w.c["KUW"]["variables"]["treasury"] == 0., "Exact-funds accepted loan conserves cash and adds principal once")
    before = w.money(); w.call("accept_KUW"); w.call("offer_KUW")
    check(w.money() == before and w.c["IRQ"]["variables"][P + "principal_KUW"] == 8., "Duplicate acceptance or offer cannot duplicate money")
    before = deepcopy(w.c["SAU"]); w.call("accept_KUW", "SAU")
    check(w.c["SAU"] == before, "Wrong actor cannot mutate funds or ledger")
    w.call("repay_KUW"); before = w.money(); w.call("repay_KUW")
    check(w.money() == before and w.c["IRQ"]["variables"]["debt"] == 10. and w.c["KUW"]["variables"]["treasury"] == 8., "Dedicated repayment pays creditor and removes only principal once")
    for scenario in ("expiry", "peace", "missing_recipient", "skip_payer"):
        w = World(); w.offer()
        if scenario == "expiry": w.day = 30
        if scenario == "peace": w.c["IRQ"]["wars"].clear()
        if scenario == "missing_recipient": w.c["KUW"]["exists"] = False
        if scenario == "skip_payer": w.c["KUW"]["flags"]["MD_skip_treasury_cost"] = (0, None)
        before = w.money(); w.call("accept_KUW")
        check(w.money() == before, "Offer fails safely after " + scenario)
    w = World(); w.offer(); w.call("accept_KUW")
    w.c["IRQ"]["variables"]["debt"] += 20.; w.call("reconcile_debt")
    w.c["IRQ"]["variables"]["debt"] -= 5.; w.call("reconcile_debt")
    check(w.c["IRQ"]["variables"][P + "principal_KUW"] == 3., "Unattributed native repayment retires named principal conservatively")
    w.call("forgive_kuwait_principal")
    check(w.c["IRQ"]["variables"]["debt"] == 30., "Kuwait cancellation preserves all other recorded debt")
    before = w.money(); w.call("forgive_kuwait_principal")
    check(w.money() == before, "Duplicate cancellation has no effect")
    w = World(); w.offer(); w.call("accept_KUW")
    w.c["IRQ"]["variables"][P + "other_debt_change"] = 5.; w.call("change_other_debt")
    check(w.c["IRQ"]["variables"][P + "other_debt"] == 15. and w.c["IRQ"]["variables"]["debt"] == 23. and w.c["IRQ"]["variables"][P + "principal_KUW"] == 8., "Known non-Gulf loan adds native and protected other debt without touching Gulf principal")
    w.c["IRQ"]["variables"][P + "other_debt_change"] = -2.; w.call("change_other_debt"); w.call("reconcile_debt")
    check(w.c["IRQ"]["variables"][P + "other_debt"] == 13. and w.c["IRQ"]["variables"]["debt"] == 21. and w.c["IRQ"]["variables"][P + "principal_KUW"] == 8., "Known repayment to another creditor cannot retire Kuwaiti principal")
    before = tuple(c["variables"]["treasury"] for c in w.c.values())
    w.c["IRQ"]["variables"][P + "other_debt_change"] = -100.; w.call("change_other_debt")
    check(w.c["IRQ"]["variables"][P + "other_debt_applied"] == -13. and w.c["IRQ"]["variables"]["debt"] == 8. and w.c["IRQ"]["variables"][P + "principal_KUW"] == 8., "Oversized known-other repayment is bounded by actual protected non-Gulf debt")
    check(tuple(c["variables"]["treasury"] for c in w.c.values()) == before, "Known-other debt API never invents a cash transfer")
    before = deepcopy(w.c["IRQ"])
    w.c["IRQ"]["variables"][P + "other_debt_change"] = 0.; w.call("change_other_debt")
    check(w.c["IRQ"]["variables"]["debt"] == before["variables"]["debt"] and w.c["IRQ"]["variables"][P + "debt_snapshot"] == before["variables"][P + "debt_snapshot"], "Zero known-other debt request cannot replay a preceding repayment")
    w = World(); w.offer(); w.call("accept_KUW")
    w.c["IRQ"]["variables"]["debt"] += 4.
    w.c["IRQ"]["variables"][P + "other_debt_change"] = -2.; w.call("change_other_debt")
    check(w.c["IRQ"]["variables"][P + "other_debt"] == 12. and w.c["IRQ"]["variables"]["debt"] == 20. and w.c["IRQ"]["variables"][P + "principal_KUW"] == 8., "Known repayment first reconciles intervening native borrowing")
    w = World(); w.offer(); w.call("accept_KUW")
    w.c["IRQ"]["variables"][P + "other_debt_change"] = 5.; w.call("change_other_debt")
    w.c["IRQ"]["variables"]["debt"] -= 11.; w.call("reconcile_debt")
    check(w.c["IRQ"]["variables"][P + "principal_KUW"] == 0. and w.c["IRQ"]["variables"][P + "other_debt"] == 12. and w.c["IRQ"]["variables"][P + "other_retirement_total"] == 3., "Unknown retirement exports only the residual actual non-Gulf reduction after Gulf principal")
    w.call("reconcile_debt")
    check(w.c["IRQ"]["variables"][P + "other_retirement_total"] == 3., "Repeated reconciliation cannot duplicate the unknown-other retirement audit")
    w.c["IRQ"]["variables"][P + "other_debt_change"] = -2.; w.call("change_other_debt")
    check(w.c["IRQ"]["variables"][P + "other_retirement_total"] == 3., "Known named non-Gulf repayment is not exported again as an unknown retirement")
    w.c["IRQ"]["variables"]["debt"] += 7.; w.call("reconcile_debt")
    check(w.c["IRQ"]["variables"][P + "other_retirement_total"] == 3. and w.c["IRQ"]["variables"][P + "other_debt"] == 17., "Later native borrowing cannot erase or inflate the cumulative retirement audit")
    w = World(); w.war()
    for day, tier in ((0, 1), (179, 1), (180, 2), (364, 2), (365, 3)):
        w.day = day; w.call("war_observer")
        active = [i for i in (1, 2, 3) if P + "iran_cost_" + str(i) in w.c["IRQ"]["ideas"]]
        check(active == [tier], "Exactly one war-cost tier at day " + str(day))
    w.c["IRQ"]["wars"].clear(); w.call("war_observer")
    check(not any(P + "iran_cost_" + str(i) in w.c["IRQ"]["ideas"] for i in (1, 2, 3)), "Iran peace removes all war-cost tiers")
    for days, debt, expect in ((179, 50, False), (180, 34.999, False), (180, 35, True), (365, 10, False)):
        w = World(); w.war(); w.day = days; w.c["IRQ"]["variables"]["debt"] = debt
        w.c["IRQ"]["wars"].clear(); w.call("war_observer")
        check((P + "price_of_victory" in w.c["IRQ"]["ideas"]) == expect, f"Genuine net-debt and duration threshold: {days}/{debt}")
        frozen = w.c["IRQ"]["variables"][P + "war_borrowing_frozen"]
        w.c["IRQ"]["variables"]["debt"] += 50.; w.call("war_observer")
        check(w.c["IRQ"]["variables"][P + "war_borrowing_frozen"] == frozen, "Audit remains frozen after peace")
    w = World(); w.c["IRQ"]["flags"][P + "invaded_kuwait"] = (0, None)
    for state in w.states.values(): state["controller"] = "IRQ"
    w.c["KUW"]["variables"]["treasury"] = 100.; before = w.money(); w.call("seize_kuwait_treasury")
    check(w.c["KUW"]["variables"]["treasury"] == 90. and w.c["IRQ"]["variables"]["treasury"] == 30., "Seizure is a bounded transfer of actual Kuwaiti funds")
    after = w.money(); w.call("seize_kuwait_treasury")
    check(w.money() == after, "Occupied treasury cannot be farmed repeatedly")
    w.c["IRQ"]["ideas"][P + "price_of_victory"] = None; w.call("kuwait_conquest_relief")
    check(P + "price_of_victory" in w.c["IRQ"]["ideas"], "Occupation alone cannot trigger legal-conquest relief")
    for state in w.states.values(): state["owner"] = "IRQ"
    w.call("kuwait_conquest_relief")
    check(P + "price_of_victory" not in w.c["IRQ"]["ideas"], "Legal ownership and control permit one-time crisis relief")
    w.call("unlock_kuwait_integration"); w.call("daily"); w.day = 179; w.call("integrate_kuwait")
    check(all("IRQ" not in state["cores"] for state in w.states.values()), "Integration cannot run before 180 stable days")
    w.day = 180; w.c["IRQ"]["variables"]["treasury"] = 4.999; w.call("integrate_kuwait")
    check(all("IRQ" not in state["cores"] for state in w.states.values()), "Insufficient integration funds cannot grant cores")
    w.c["IRQ"]["variables"]["treasury"] = 5.; w.call("integrate_kuwait")
    check(all("IRQ" in state["cores"] for state in w.states.values()) and w.c["IRQ"]["variables"]["treasury"] == 0., "Exact integration payment cores only both designated states")
    before = w.money(); w.call("integrate_kuwait")
    check(w.money() == before, "Integration cannot replay its charge or reward")
    w = World()
    for state in w.states.values(): state.update(owner="IRQ", controller="IRQ")
    w.call("daily"); w.day = 179; w.states[488]["controller"] = "KUW"; w.call("daily")
    check(not w.flag("IRQ", P + "stable_kuwait"), "Loss of one state resets the consolidation clock")
    w.states[488]["controller"] = "IRQ"; w.day = 180; w.call("daily")
    check(w.c["IRQ"]["flags"][P + "stable_kuwait"][0] == 180, "Recovered control starts a fresh 180-day clock")
    w = World(); w.c["IRQ"]["campaign"] = False; before = deepcopy(w.c["IRQ"]); w.call("daily")
    check(w.c["IRQ"] == before, "Later scenario is outside the entire module")
    w = World(); w.c["IRQ"]["exists"] = False; before = deepcopy(w.c["IRQ"]); w.call("daily")
    check(w.c["IRQ"] == before, "An absent Iraqi country cannot refresh or grant rewards")
    for tag, _, fraction, _ in CREDITORS:
        w = World(); w.offer(tag); w.call("accept_" + tag)
        check(w.c["IRQ"]["variables"][P + "principal_" + tag] == 100 * fraction, "Correct recipient-specific principal: " + tag)
    w = World(); w.offer(); w.call("accept_KUW"); w.c["IRQ"]["wars"].clear(); w.c["IRQ"]["ideas"][P + "price_of_victory"] = None
    w.c["IRQ"]["variables"]["treasury"] = 1.999; before = deepcopy(w.c["IRQ"]); w.call("fund_recovery")
    check(w.c["IRQ"]["variables"]["political_power"] == before["variables"]["political_power"] and P + "price_of_victory" in w.c["IRQ"]["ideas"], "Unaffordable recovery charges neither cash nor political power")
    w.c["IRQ"]["variables"]["treasury"] = 2.; w.c["IRQ"]["variables"]["political_power"] = 50.; w.call("fund_recovery")
    check(w.c["IRQ"]["variables"]["treasury"] == 0. and w.c["IRQ"]["variables"]["political_power"] == 0. and P + "price_of_victory" not in w.c["IRQ"]["ideas"], "Exact-funds recovery charges its real two-part invoice once")
    w = World(); w.c["IRQ"]["flags"][P + "iran_war_seen"] = (0, None); w.call("claim_kuwait"); w.call("kuwait_ultimatum")
    check(not w.goals, "Claims alone do not create a Kuwaiti war goal")
    w.c["IRQ"]["flags"][P + "oil_dispute_rejected"] = (0, None); w.c["IRQ"]["flags"][P + "arbitration_window"] = (0, 90); w.call("kuwait_ultimatum")
    check(not w.goals, "Live arbitration prevents the Kuwaiti ultimatum")
    w.day = 90; w.call("kuwait_ultimatum"); w.call("kuwait_ultimatum")
    check(w.goals == [("IRQ", "KUW")], "Rejected demands yield one concrete Kuwaiti war goal after arbitration")
    forgive_option = values(event_rows["COLDWAR_IRQ_gulf.20"], "option")[0]
    forgive_payload = [r for r in forgive_option if r[0] not in ("name", "trigger", "ai_chance")]
    for case in ("valid", "expired", "new_iran_war", "new_kuwait_war", "wrong_recipient", "wrong_sender"):
        w = World(); w.offer(); w.call("accept_KUW"); w.c["IRQ"]["wars"].clear(); w.call("war_observer"); w.call("request_kuwait_forgiveness")
        recipient = "KUW"
        if case == "expired": w.day = 30
        if case == "new_iran_war": w.c["IRQ"]["wars"].add("PER")
        if case == "new_kuwait_war": w.c["IRQ"]["wars"].add("KUW")
        if case == "wrong_recipient": recipient = "SAU"
        if case == "wrong_sender": w.event_from = "USA"
        before = w.money(); w.execute(forgive_payload, recipient)
        if case == "valid":
            check(w.c["IRQ"]["variables"]["debt"] == 10. and w.flag("IRQ", P + "kuwait_forgave"), "Live Kuwait-owned forgiveness cancels only its surviving principal")
            before = w.money(); w.execute(forgive_payload, recipient)
            check(w.money() == before, "Duplicate forgiveness option payload cannot cancel twice")
        else:
            check(w.money() == before and not w.flag("IRQ", P + "kuwait_forgave"), "Queued forgiveness acceptance rechecks " + case)
    money_source = (root / "common/scripted_effects/00_money_system.txt").read_text(encoding="utf-8-sig")
    native_weekly = (root / "common/on_actions/MD_on_actions.txt").read_text(encoding="utf-8-sig")
    native_borrowing = (root / "common/scripted_effects/00_economic_system_utilities.txt").read_text(encoding="utf-8-sig")
    check("add = modifier@army_personnel_cost_multiplier_modifier" in money_source and "add = modifier@equipment_cost_multiplier_modifier" in money_source, "Native military reader consumes both cost components")
    check("add = modifier@interest_rate_multiplier_modifier" in money_source and "add = modifier@consumer_goods_factor" in money_source, "Native interest and consumer-goods readers exist")
    check("add_to_variable = { treasury = treasury_rate_gain }" in native_weekly and "automated_debt_taker = yes" in native_weekly and "add_to_variable = { debt = debt_temp }" in native_borrowing, "Real weekly balance and native deficit borrowing remain the single cash/debt charger")
    check(not any("add_resource" == k for rows in asts.values() for k, _, _ in walk(rows)), "No fictional extra oil deposits")
    return {"passed": len(checks), "checks": checks, "limitations": "Bounded emitted-AST tests; native weekly accrual, engine/UI/save/MP behavior untested."}


if __name__ == "__main__":
    print(json.dumps(self_test(Path(__file__).resolve().parents[2]), indent=2))
