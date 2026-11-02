# IMPERIA COLD WAR — Accepted Swing and Milliardenkredit transactions.
"""Bounded source helpers for recipient-approved West German concessions."""

from cw_lib import P, dv_self, v


SWING_PENDING = f"{P}_balance_swing_pending"
SWING_ACCEPTED = f"{P}_balance_swing_accepted"
CREDIT_PENDING = f"{P}_balance_credit_pending"
CREDIT_ACCEPTED = f"{P}_balance_credit_accepted"
INTEL_COOLDOWN = "cwger_intel_operation_cd"
OFFENSIVE_COOLDOWN = "cwgg_balance_offensive_cd"

INTEL_OPERATIONS = {"raid", "counterspy", "vetting", "double"}
OFFENSIVE_ACTIONS = {"media", "church", "freeze", "escape", "manoeuvre"}


def triggers():
    return f"""
# IMPERIA COLD WAR — Shared intelligence, offensive-order and recipient-consent guards.
{P}_balance_intel_operation_ready = {{
    original_tag = GER
    IMP_is_1970_scenario = yes
    NOT = {{ has_country_flag = {INTEL_COOLDOWN} }}
}}

{P}_balance_offensive_ready = {{
    original_tag = GER
    IMP_is_1970_scenario = yes
    NOT = {{ has_country_flag = {OFFENSIVE_COOLDOWN} }}
}}

{P}_balance_can_respond_swing = {{
    original_tag = DDR
    tag = DDR
    country_exists = GER
    NOT = {{ has_war_with = GER }}
    NOT = {{ has_global_flag = {P}_unity_achieved }}
    GER = {{ original_tag = GER IMP_is_1970_scenario = yes NOT = {{ has_war_with = DDR }} has_country_flag = {SWING_PENDING} NOT = {{ has_country_flag = {SWING_ACCEPTED} }}}}
}}

{P}_balance_can_accept_swing = {{
    {P}_balance_can_respond_swing = yes
    has_global_flag = mdcw_cw_initialized
    has_country_flag = mdcw_cw_initialized
    GER = {{ has_country_flag = mdcw_cw_initialized check_variable = {{ mdcw_cw_cap_free > 1 }} check_variable = {{ mdcw_cw_p5_size@DDR = 0 }} OR = {{ has_country_flag = {P}_swing_unlocked check_variable = {{ cwgg_hebel_devisen > 0 }} }} }}
}}

{P}_balance_can_respond_credit = {{
    original_tag = DDR
    tag = DDR
    country_exists = GER
    NOT = {{ has_war_with = GER }}
    NOT = {{ has_global_flag = {P}_unity_achieved }}
    GER = {{ original_tag = GER IMP_is_1970_scenario = yes NOT = {{ has_war_with = DDR }} has_country_flag = cwgg_done_credit has_country_flag = {CREDIT_PENDING} NOT = {{ has_country_flag = {CREDIT_ACCEPTED} }}}}
}}

{P}_balance_can_accept_credit = {{
    {P}_balance_can_respond_credit = yes
    GER = {{ OR = {{ check_variable = {{ ruling_party = 1 }} check_variable = {{ cwgg_kanal_koko = 1 }} }} }}
    check_variable = {{ cwddr_hard_currency > 40 }}
}}
"""


def effects(swing_log, credit_log):
    swing_ddr = "\n".join((
        dv_self("cwddr_hard_currency", -6, show=False),
        dv_self("cwddr_west_dependency", 6, show=False),
    ))
    credit_ddr = "\n".join((
        dv_self("cwddr_hard_currency", -15, show=False),
        dv_self("cwddr_west_dependency", 12, show=False),
        dv_self("cwddr_sed_control", -2, show=False),
        dv_self("cwddr_exit_pressure", 2, show=False),
    ))
    swing_ger = "\n".join((
        "clr_country_flag = " + SWING_PENDING,
        "set_country_flag = " + SWING_ACCEPTED,
        f"set_global_flag = {P}_swing_high",
        "add_to_variable = { cwgg_klima = 5 }",
        "clamp_variable = { var = cwgg_klima min = -100 max = 100 }",
        "add_to_variable = { cwgg_hebel_devisen = 1 }",
        "clamp_variable = { var = cwgg_hebel_devisen min = 0 max = 3 }",
        v("cwger_ostpolitik", 3, show=False),
        "set_temp_variable = { cwger_t_prog = 5 }",
        "set_temp_variable = { cwger_t_size = 2 }",
        f"{P}_start_programme = yes",
        swing_log,
    ))
    credit_ger = "\n".join((
        "clr_country_flag = " + CREDIT_PENDING,
        "set_country_flag = " + CREDIT_ACCEPTED,
        "add_to_variable = { cwgg_klima = 10 }",
        "clamp_variable = { var = cwgg_klima min = -100 max = 100 }",
        "add_to_variable = { cwgg_dhebel_grenze = -1 }",
        "clamp_variable = { var = cwgg_dhebel_grenze min = 0 max = 3 }",
        "add_to_variable = { cwgg_hebel_devisen = 1 }",
        "clamp_variable = { var = cwgg_hebel_devisen min = 0 max = 3 }",
        v("cwger_csu_autonomy", 5, show=False),
        v("cwger_ostpolitik", 6, show=False),
        "set_temp_variable = { treasury_change = gdp_total }",
        "multiply_temp_variable = { treasury_change = -0.001 }",
        "modify_treasury_effect = yes",
        credit_log,
    ))
    return f"""
# IMPERIA COLD WAR — Apply Swing and credit rewards once, only after the DDR's valid acceptance.
{P}_balance_accept_swing = {{
    if = {{
        limit = {{ {P}_balance_can_respond_swing = yes }}
        GER = {{ mdcw_cw_recalculate_capacity = yes }}
    }}
    if = {{
        limit = {{ {P}_balance_can_accept_swing = yes }}
        {swing_ddr}
        GER = {{ {swing_ger} }}
        {P}_rv_sync_views = yes
    }}
}}

{P}_balance_refuse_swing = {{
    if = {{ limit = {{ {P}_balance_can_respond_swing = yes }} GER = {{ clr_country_flag = {SWING_PENDING} }} {P}_rv_sync_views = yes }}
}}

{P}_balance_accept_credit = {{
    if = {{
        limit = {{ {P}_balance_can_accept_credit = yes }}
        {credit_ddr}
        GER = {{
            {credit_ger}
        }}
        {P}_rv_sync_views = yes
    }}
}}

{P}_balance_refuse_credit = {{
    if = {{ limit = {{ {P}_balance_can_respond_credit = yes }} GER = {{ clr_country_flag = {CREDIT_PENDING} }} {P}_rv_sync_views = yes }}
}}
"""


def acceptance_previews(kl, lever):
    """Native, non-executing effect previews for the two negotiated packages."""
    swing_rows = "\n".join((
        dv_self("cwddr_hard_currency", -6),
        dv_self("cwddr_west_dependency", 6),
        "GER = {",
        kl(5),
        lever("devisen", 1),
        v("cwger_ostpolitik", 3),
        # Use the real Imperia provider so the prospective programme matches its live implementation.
        "set_temp_variable = { cwger_t_prog = 5 }",
        "set_temp_variable = { cwger_t_size = 2 }",
        f"{P}_start_programme = yes",
        "}",
    ))
    credit_rows = "\n".join((
        dv_self("cwddr_hard_currency", -15),
        dv_self("cwddr_west_dependency", 12),
        dv_self("cwddr_sed_control", -2),
        dv_self("cwddr_exit_pressure", 2),
        "GER = {",
        kl(10),
        lever("grenze", -1, ddr=True),
        lever("devisen", 1),
        v("cwger_csu_autonomy", 5),
        v("cwger_ostpolitik", 6),
        "set_temp_variable = { treasury_change = gdp_total }",
        "multiply_temp_variable = { treasury_change = -0.001 }",
        "modify_treasury_effect = yes",
        "}",
    ))
    return swing_rows, credit_rows


def mark_intel_operation():
    return f"set_country_flag = {{ flag = {INTEL_COOLDOWN} days = 180 value = 1 }}"


def mark_offensive_action():
    return f"set_country_flag = {{ flag = {OFFENSIVE_COOLDOWN} days = 60 value = 1 }}"
