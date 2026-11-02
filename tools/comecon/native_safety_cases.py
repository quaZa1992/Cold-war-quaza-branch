# IMPERIA COLD WAR — COMECON native human authority and passive AI assertions
from build import MARK


def compile_checks(controller, assertion):
    host = 'DDR' if controller == 'HUN' else 'HUN'
    ai = host
    initial_receivers = 1 if controller == 'HUN' else 2
    a = assertion
    checks = ['log = "CC_NATIVE START"', 'cc_initialize = yes',
        a('is_ai = no cc_secretariat = yes check_variable = { global.cc_chair = THIS.id }', 'actual_human_presides'),
        a(f'{ai} = {{ is_ai = yes NOT = {{ cc_human_member = yes }} NOT = {{ cc_secretariat = yes }} }}', 'actual_ai_has_no_authority'),
        a('check_variable = { global.cc_members^num = 8 } UKR = { NOT = { cc_member_country = yes } }', 'eight_delegations_and_no_ssr_vote'),
        'for_each_scope_loop = { array = global.cc_members set_variable = { treasury = 10000 } }',
        f'set_variable = {{ global.cc_3_host = {host}.id }} set_variable = {{ global.cc_3_offer = 16 }} set_variable = {{ global.cc_3_tier = 1 }} set_variable = {{ cc_view_slot = 3 }}',
        f'{host} = {{ random_owned_state = {{ limit = {{ is_controlled_by = PREV free_building_slots = {{ building = industrial_complex size > 0 include_locked = no }} }} set_variable = {{ PREV.cc_3_site1 = THIS.id }} }} }} cc_3_revise = yes',
        a(f'check_variable = {{ cc_3_share = 100 }} check_variable = {{ global.cc_3_coverage = 100 }} check_variable = {{ global.cc_3_participants = 1 }} {host} = {{ cc_3_receiving_country = yes NOT = {{ cc_3_participant = yes }} cc_3_receiver_consent = yes }}', 'human_finances_passive_ai_host'),
        f'{ai} = {{ set_variable = {{ cc_view_slot = 3 }} cc_3_decrease_share = yes cc_3_fund_remainder = yes cc_3_open_review = yes cc_3_acknowledge = yes cc_3_approve = yes cc_3_ratify = yes }}',
        a(f'check_variable = {{ global.cc_3_phase = 0 }} {ai} = {{ check_variable = {{ cc_3_share = 0 }} check_variable = {{ treasury = 10000 }} NOT = {{ cc_3_signed = yes }} }}', 'ai_commands_cannot_offer_vote_ratify_or_pay'),
        'cc_3_ratify = yes', a('check_variable = { global.cc_3_phase = 0 } check_variable = { treasury = 10000 }', 'unreviewed_draft_cannot_charge'),
        'set_variable = { cc_view_slot = 4 } cc_3_decrease_share = yes',
        a('check_variable = { cc_3_share = 100 }', 'stale_file_contribution_command_rejected'),
        'set_variable = { cc_view_slot = 3 } cc_3_decrease_share = yes cc_3_fund_remainder = yes cc_3_open_review = yes',
        'log = "CC_NATIVE DETAILS coverage=[?global.cc_3_coverage] participants=[?global.cc_3_participants] invalid=[?global.cc_3_invalid] assets=[?global.cc_3_asset_invalid] phase=[?global.cc_3_phase]"',
        a('check_variable = { global.cc_3_phase = 1 } check_variable = { global.cc_3_payers^num = 1 } check_variable = { global.cc_3_receivers^num = 2 }', 'review_seals_one_payer_and_two_receivers'),
        'cc_3_preview_all = yes', a('check_variable = { treasury = 10000 } check_variable = { global.cc_3_phase = 1 } NOT = { has_country_flag = cc_3_beneficiary }', 'native_preview_does_not_charge_or_activate'),
        'set_variable = { cc_probe_quote = global.cc_3_cost } set_variable = { cc_probe_revision = global.cc_3_revision } cc_3_decrease_share = yes cc_3_fund_remainder = yes cc_3_approve = yes cc_3_ratify = yes',
        a('check_variable = { cc_3_share = 100 } check_variable = { global.cc_3_cost = cc_probe_quote } check_variable = { global.cc_3_revision = cc_probe_revision } check_variable = { global.cc_3_phase = 1 } NOT = { cc_3_signed = yes }', 'sealed_quote_and_explicit_review_required'),
        'cc_3_acknowledge = yes cc_3_approve = yes cc_3_reopen = yes cc_3_open_review = yes cc_3_approve = yes',
        a('check_variable = { global.cc_3_phase = 1 } NOT = { cc_3_signed = yes } NOT = { cc_3_seen_terms = yes }', 'reopened_terms_invalidate_old_review_and_signature'),
        'cc_3_acknowledge = yes cc_3_approve = yes cc_3_rebuild = yes',
        a('cc_3_can_ratify = yes', 'human_consent_suffices_without_ai_signature'),
        'cc_3_ratify = yes',
        a(f'check_variable = {{ global.cc_3_phase = 2 }} check_variable = {{ global.cc_3_period_left = 7 }} check_variable = {{ treasury < 10000 }} {host} = {{ check_variable = {{ treasury = 10000 }} has_country_flag = cc_3_beneficiary }}', 'first_invoice_human_only'),
        'set_variable = { cc_probe_after_first = treasury } cc_3_ratify = yes cc_3_prepay = yes',
        'cc_3_rebuild = yes',
        a('check_variable = { treasury = cc_probe_after_first } check_variable = { global.cc_3_cost = cc_probe_quote }', 'duplicate_ratify_and_prepay_do_not_charge'),
        ' '.join(['cc_3_daily = yes']*90),
        a(f'check_variable = {{ global.cc_3_phase = 3 }} check_variable = {{ global.cc_3_remaining = 90 }} has_idea = cc_research_CAT_industry_15 {host} = {{ var:cc_3_site1 = {{ industrial_complex > 0 }} check_variable = {{ treasury = 10000 }} check_variable = {{ cc_weekly_expenses = 0 }} }}', 'ai_receives_building_without_funding_or_service_bill'),
        'set_variable = { cc_probe_difference = cc_3_paid } subtract_from_variable = { cc_probe_difference = cc_3_liability }',
        a('check_variable = { cc_probe_difference > -0.001 } check_variable = { cc_probe_difference < 0.001 }', 'final_partial_invoice_exact_liability'),
        'cc_3_complete = yes', a('check_variable = { global.cc_3_remaining = 90 }', 'completion_replay_does_not_refill_services'),
        ' '.join(['cc_3_daily = yes']*90),
        a('check_variable = { global.cc_3_phase = 4 } NOT = { has_idea = cc_research_CAT_industry_15 }', 'ninety_day_services_expire'),
        'set_variable = { treasury = 10000 } set_variable = { global.cc_4_offer = 44 } cc_4_revise = yes cc_4_open_review = yes cc_4_acknowledge = yes cc_4_approve = yes cc_4_ratify = yes',
        a('check_variable = { global.cc_4_phase = 2 } check_variable = { global.cc_4_operating = 1 } has_idea = cc_research_CAT_computing_10', 'campaign_starts_on_funded_ratification'),
        'set_variable = { treasury = 0 } '+' '.join(['cc_4_daily = yes']*7),
        a(f'check_variable = {{ global.cc_4_period_left = 0 }} check_variable = {{ global.cc_4_operating = 0 }} check_variable = {{ global.cc_4_remaining = 173 }} NOT = {{ has_idea = cc_research_CAT_computing_10 }} {host} = {{ check_variable = {{ treasury = 10000 }} }}', 'unaffordable_week_pauses_without_ai_or_other_charge'),
        'set_variable = { treasury = 10000 } cc_4_resume = yes',
        a('check_variable = { global.cc_4_period_left = 7 } check_variable = { global.cc_4_operating = 1 }', 'human_prepayment_resumes_campaign'),
        ' '.join(['cc_4_daily = yes']*173),
        a(f'check_variable = {{ global.cc_4_phase = 4 }} check_variable = {{ global.cc_4_remaining = 0 }} NOT = {{ has_idea = cc_research_CAT_computing_10 }} {host} = {{ check_variable = {{ treasury = 10000 }} }}', 'exact_180_funded_days_no_ai_charge'),
        # A fixture legacy quote tests migration without pretending to change native human control.
        f'set_variable = {{ global.cc_2_phase = 2 }} set_variable = {{ global.cc_2_revision = 42 }} set_variable = {{ global.cc_2_cost = 99 }} set_variable = {{ global.cc_2_period_left = 5 }} set_variable = {{ global.cc_2_remaining = 85 }} clear_array = global.cc_2_payers {ai} = {{ add_to_array = {{ global.cc_2_payers = THIS }} set_variable = {{ cc_2_recipient = THIS.id }} set_variable = {{ cc_2_share = 50 }} set_variable = {{ cc_2_vote_revision = 42 }} set_variable = {{ cc_2_paid = 3 }} set_variable = {{ cc_2_liability = 49.5 }} }} set_variable = {{ global.cc_2_valid = 1 }} set_variable = {{ global.cc_2_operating = 1 }} cc_2_guard_controllers = yes cc_2_daily = yes',
        a('check_variable = { global.cc_2_valid = 0 } check_variable = { global.cc_2_operating = 0 } check_variable = { global.cc_2_remaining = 85 }', 'daily_controller_guard_stops_actual_ai_financier'),
        'clr_global_flag = cc_safety_v2 cc_migrate_safety = yes cc_2_guard_controllers = yes cc_2_daily = yes cc_2_prepay = yes',
        a(f'check_variable = {{ global.cc_2_cost = 99 }} check_variable = {{ global.cc_2_remaining = 85 }} check_variable = {{ global.cc_2_period_left = 5 }} check_variable = {{ global.cc_2_operating = 0 }} {ai} = {{ check_variable = {{ cc_2_paid = 3 }} check_variable = {{ cc_2_liability = 49.5 }} check_variable = {{ treasury = 10000 }} }}', 'legacy_ai_financier_paused_without_repricing_or_redistribution'),
        'set_country_flag = cc_open set_variable = { cc_view_slot = 1 } set_variable = { cc_view_tab = 0 } set_variable = { cc_sheet = 3 } set_variable = { cc_delegate_page = 99 } set_variable = { cc_recipient_page = 99 } cc_ui_refresh = yes',
        a(f'check_variable = {{ cc_ui_header_flags^num = 8 }} check_variable = {{ cc_ui_recipients^num = {initial_receivers} }} check_variable = {{ cc_recipient_page = 0 }} check_variable = {{ cc_delegate_page = 1 }}', 'passive_receiver_cards_and_bounded_pages'),
        f'{ai} = {{ set_variable = {{ cc_weekly_gdp = 0.01 }} set_variable = {{ cc_weekly_fixed = 5 }} cc_calculate_weekly_expense = yes }}',
        a(f'{ai} = {{ check_variable = {{ cc_weekly_expenses = 0 }} }}', 'native_fiscal_consumer_rejects_stale_ai_service_charge'),
        'log = "CC_NATIVE COMPLETE"']
    return '\n'.join(checks)
