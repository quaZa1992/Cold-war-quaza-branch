# IMPERIA COLD WAR — Disposable native observer assertions and dossier inspection
from runtime import COLS


def source():
    def test(condition,name):return f'if = {{ limit = {{ {condition} }} log = "ICSD_NATIVE PASS {name}" }} else = {{ log = "ICSD_NATIVE FAIL {name}" }}'
    def packet(**data):
        return 'icsd_reset_observation = yes\n'+'\n'.join(f'set_variable = {{ global.icsd_t_{k} = {v} }}' for k,v in data.items())
    clear='\n'.join(f'clear_array = icsd_mail_{c}' for c in COLS)
    c=['log = "ICSD_NATIVE START"','icsd_initialize = yes',test('check_variable = { global.icsd_version = 2 }','initialized_schema_v2'),
       'set_variable = { icsd_probe_money = treasury }','SOV = { set_variable = { icsd_probe_money = treasury } }','EGY = { set_variable = { icsd_probe_money = treasury } }',
       clear,'SOV = { '+clear+' }','set_variable = { gift_size = 0.5 }','EGY = { icsd_note_money_sent = yes }',
       test('check_variable = { icsd_mail_kind^num = 1 } check_variable = { icsd_mail_actor^0 = USA.id } check_variable = { icsd_mail_target^0 = EGY.id } check_variable = { icsd_mail_amount^0 = 0.5 }','native_money_callback_sender_recipient_amount'),
       test('SOV = { check_variable = { icsd_mail_kind^num = 0 } }','foreign_proposal_not_disclosed'),
       'SOV = { icsd_note_money_accepted = yes }',
       test('SOV = { check_variable = { icsd_mail_kind^num = 1 } check_variable = { icsd_mail_amount^0 = 0.5 } }','direct_recipient_receives_accepted_transfer'),
       test('NOT = { has_variable = global.icsd_t_actor }','packet_cleared_after_both_observers'),
       'set_variable = { icsd_probe_counter = 0 }','while_loop_effect = { limit = { check_variable = { icsd_probe_counter < 30 } } EGY = { icsd_note_money_sent = yes } add_to_variable = { icsd_probe_counter = 1 } }',
       test('check_variable = { icsd_mail_kind^num = 24 } check_variable = { icsd_mail_amount^num = 24 } check_variable = { icsd_mail_key^num = 24 }','observer_journal_bounded_at_24'),
       'set_variable = { icsd_tab = 2 }','icsd_build_view = yes',
       test('check_variable = { icsd_view_count = 24 } check_variable = { icsd_row_count = 5 }','five_row_journal_page'),
       'icsd_select_0 = yes','set_variable = { icsd_probe_selected_key = icsd_selected_key }','EGY = { icsd_note_money_sent = yes }','icsd_build_view = yes',
       test('check_variable = { icsd_selected_key = icsd_probe_selected_key }','stable_selection_after_journal_insertion'),
       'set_variable = { icsd_offset = 6000 }','icsd_build_view = yes',test('check_variable = { icsd_offset = 0 }','invalid_page_recovers'),
       'icsd_clear_live = yes','SOV = { icsd_clear_live = yes set_variable = { icsd_civ_usa = 0 } set_variable = { icsd_network@EGY = 0 } }',
       'EGY = { capital_scope = { set_variable = { global.icsd_probe_place = THIS.id } } }',
       packet(actor='USA.id',target='EGY.id',kind=8,place='global.icsd_probe_place',type=1,size=2,amount=12,key=1),'icsd_publish_live = yes',
       test('check_variable = { icsd_live_amount^0 = 12 } SOV = { check_variable = { icsd_live_kind^num = 1 } check_variable = { icsd_live_detail^0 = 0 } check_variable = { icsd_live_amount^0 = 0 } check_variable = { icsd_live_place^0 = 0 } check_variable = { icsd_live_type^0 = 0 } }','investor_full_rival_redacted'),
       packet(actor='USA.id',target='EGY.id',kind=13,amount=0.2),'icsd_publish_live = yes',
       test('SOV = { check_variable = { icsd_live_kind^num = 1 } }','unknown_subsidy_has_no_row'),
       packet(actor='USA.id',target='EGY.id',kind=10,type=4,left=200),'icsd_publish_live = yes',
       test('SOV = { check_variable = { icsd_live_kind^num = 2 } check_variable = { icsd_live_type^1 = 4 } }','public_party_slot_always_available'),
       'SOV = { set_variable = { icsd_network@EGY = 1 } }',packet(actor='USA.id',target='EGY.id',kind=8,place='global.icsd_probe_place',type=1,size=2,amount=12,key=2),'icsd_publish_live = yes',
       test('SOV = { check_variable = { icsd_live_detail^2 = 1 } check_variable = { icsd_live_amount^2 = 12 } }','cached_network_releases_ongoing_details'),
       'set_variable = { icsd_tab = 1 }','clear_variable = icsd_offset','icsd_build_view = yes','icsd_select_0 = yes','icsd_clear_live = yes','icsd_build_view = yes',
       test('NOT = { icsd_has_selection = yes } NOT = { has_variable = icsd_selected_amount }','removed_commitment_clears_sensitive_detail'),
       'CHI = { clear_variable = icsd_tab icsd_build_view = yes }',test('CHI = { NOT = { has_variable = icsd_tab } }','third_country_rejected'),
       test('check_variable = { treasury = icsd_probe_money } SOV = { check_variable = { treasury = icsd_probe_money } } EGY = { check_variable = { treasury = icsd_probe_money } }','all_observers_leave_treasuries_unchanged'),
       # Exercise the real native intelligence predicates directly, without injecting their result.
       packet(actor='SOV.id',target='EGY.id',kind=7,state=2,amount=0.25),
       'if = { limit = { icsd_event_access = yes } log = "ICSD_NATIVE INFO actual_financial_access_yes" } else = { log = "ICSD_NATIVE INFO actual_financial_access_no" }',
       'icsd_clear_observation = yes',
       # A clear, fixed inspection page. These are disposable fixture records, never game claims.
       'icsd_clear_live = yes','SOV = { icsd_clear_live = yes set_variable = { icsd_civ_usa = 0 } set_variable = { icsd_network@EGY = 0 } }',
       packet(actor='USA.id',target='EGY.id',kind=8,place='global.icsd_probe_place',type=1,size=2,amount=12,key=1),'icsd_publish_live = yes',
       'set_variable = { icsd_civ_sov = 0 }','EGY = { PREV = { set_variable = { icsd_network@PREV = 0 } } }',
       packet(actor='SOV.id',target='EGY.id',kind=9,type=1,size=3,left=300,key=1),'icsd_publish_live = yes',
       packet(actor='SOV.id',target='EGY.id',kind=10,type=4,left=200),'icsd_publish_live = yes',
       'clear_variable = icsd_offset','set_variable = { icsd_tab = 1 }','icsd_open = yes','icsd_select_0 = yes',
       'SOV = { clear_variable = icsd_offset set_variable = { icsd_tab = 1 } icsd_open = yes }','log = "ICSD_NATIVE COMPLETE"']
    return 'icsd_probe_run = {\n'+'\n'.join(c)+'\n}\n'
