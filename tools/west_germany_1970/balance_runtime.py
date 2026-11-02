# IMPERIA COLD WAR — Targeted German diplomacy and consent-based war settlements.
"""Native MD/Imperia transactions. No automatic government, faction or annexation changes."""
from cw_lib import P, L

MARK = '# IMPERIA COLD WAR — German diplomacy and negotiated settlements\n'
S = P + '_settlement'
B = P + '_recognition'
NS = 'COLDWAR_GER_BALANCE'


def block(key, body):
    return key + ' = {\n' + body + '\n}\n'


def iff(gate, body):
    return block('if', 'limit = { ' + gate + ' }\n' + body)


def files():
    # The one-entry country array is frozen when the real recognition crisis starts.
    target = 'var:cwgg_recognition_country^0'
    recognition_gate = '''tag = GER
IMP_is_1970_scenario = yes
country_exists = DDR
check_variable = { cwgg_krise_typ = 5 }
check_variable = { cwgg_special_used = 0 }
check_variable = { cwgg_countdown = 0 }
has_idea = COLDWAR_GER_1970_idea_hallstein_legacy
check_variable = { cwgg_vertrag_3 = 0 }
check_variable = { cwgg_recognition_country^num = 1 }
''' + target + ''' = {
 exists = yes
 NOT = { tag = GER }
 NOT = { tag = DDR }
 is_in_array = { recognised_countries = DDR }
 NOT = { is_in_array = { array = imp_dip_sanc_on_us value = GER } }
}
has_political_power > 34
'''
    triggers = block(B + '_can_sanction', recognition_gate)
    # Match the current native diplomatic-sanctions price and both mirrored ledgers.
    effects = block(B + '_sanction', iff(B + '_can_sanction = yes', '''add_political_power = -35
set_variable = { cwgg_special_used = 1 }
add_to_variable = { cwgg_krise_int = -20 }
clamp_variable = { var = cwgg_krise_int min = 0 max = 100 }
add_to_variable = { cwgg_klima = -5 }
clamp_variable = { var = cwgg_klima min = -100 max = 100 }
''' + target + ''' = {
 IMP_sanctions_add_dip_from_prev = yes
 if = { limit = { has_global_flag = mdcw_cw_initialized }
  set_temp_variable = { mdcw_cw_t_sanc_type = 1 }
  mdcw_cw_on_sanction_imposed = yes
 }
 imp_sanctions_calculate = yes
 country_event = { id = COLDWAR_GER_BALANCE.10 }
}
imp_sanctions_calculate = yes
COLDWAR_GER_1970_rv_sync_views = yes
'''))

    # Every government actually fighting either German country is a signatory.
    # This also covers non-faction allies; neutral faction members are not coerced.
    participant = '''OR = {
 tag = GER
 tag = DDR
 has_war_with = GER
 has_war_with = DDR
}'''
    triggers += block(S + '_belligerent', participant)
    triggers += block(S + '_war_live', '''IMP_is_1970_scenario = yes
country_exists = GER
country_exists = DDR
has_global_flag = cwgg_german_war
GER = { has_war_with = DDR }
''')
    triggers += block(S + '_can_propose', S + '''_war_live = yes
OR = { tag = GER tag = DDR }
NOT = { has_country_flag = cwgg_settlement_proposal_cd }
GER = { NOT = { has_country_flag = cwgg_settlement_pending } }
''')
    triggers += block(S + '_can_sign', S + '''_war_live = yes
has_country_flag = cwgg_settlement_invited
COLDWAR_GER_1970_settlement_belligerent = yes
GER = { has_country_flag = cwgg_settlement_pending }
is_in_array = { array = GER.cwgg_settlement_participants value = THIS }
NOT = { is_in_array = { array = GER.cwgg_settlement_signatures value = THIS } }
''')
    triggers += block(S + '_terms_valid', S + '''_war_live = yes
OR = {
 GER = { check_variable = { cwgg_settlement_kind = 1 } }
 AND = {
  GER = { check_variable = { cwgg_settlement_kind = 2 } has_capitulated = yes }
  DDR = { has_capitulated = no }
  1251 = { is_owned_by = GER }
 }
 AND = {
  GER = { check_variable = { cwgg_settlement_kind = 3 } has_capitulated = no }
  DDR = { has_capitulated = yes check_variable = { var = treasury compare = greater_than_or_equals value = 0.2 } }
 }
}
''')
    effects += block(S + '_clear', '''for_each_scope_loop = {
 array = cwgg_settlement_participants
 clr_country_flag = cwgg_settlement_invited
}
clr_country_flag = cwgg_settlement_pending
clear_array = cwgg_settlement_participants
clear_array = cwgg_settlement_signatures
set_variable = { cwgg_settlement_kind = 0 }
''')
    effects += block(S + '_open', iff('OR = { tag = GER tag = DDR }\n' + S + '_war_live = yes', 'country_event = { id = ' + NS + '.1 }'))

    # Called in GER scope with the original proposing country preserved in ROOT.
    effects += block(S + '_begin', iff('tag = GER\n' + S + '''_war_live = yes
NOT = { has_country_flag = cwgg_settlement_pending }
ROOT = { OR = { tag = GER tag = DDR } NOT = { has_country_flag = cwgg_settlement_proposal_cd } }
''', S + '''_clear = yes
set_variable = { cwgg_settlement_kind = cwgg_settlement_new_kind }
set_country_flag = cwgg_settlement_pending
ROOT = { set_country_flag = { flag = cwgg_settlement_proposal_cd days = 60 } }
every_country = {
 limit = { COLDWAR_GER_1970_settlement_belligerent = yes }
 GER = { add_to_array = { cwgg_settlement_participants = PREV } }
}
add_to_array = { cwgg_settlement_signatures = ROOT }
for_each_scope_loop = {
 array = cwgg_settlement_participants
 set_country_flag = cwgg_settlement_invited
 if = { limit = { NOT = { tag = ROOT } }
  if = { limit = { GER = { check_variable = { cwgg_settlement_kind = 1 } } } country_event = { id = COLDWAR_GER_BALANCE.2 } }
  else_if = { limit = { GER = { check_variable = { cwgg_settlement_kind = 2 } } } country_event = { id = COLDWAR_GER_BALANCE.3 } }
  else_if = { limit = { GER = { check_variable = { cwgg_settlement_kind = 3 } } } country_event = { id = COLDWAR_GER_BALANCE.4 } }
 }
}
'''))
    for kind, extra in ((1, ''), (2, 'GER = { has_capitulated = yes } DDR = { has_capitulated = no } 1251 = { is_owned_by = GER }'),
                        (3, 'GER = { has_capitulated = no } DDR = { has_capitulated = yes check_variable = { var = treasury compare = greater_than_or_equals value = 0.2 } }')):
        effects += block(S + '_propose_' + str(kind), iff(S + '_can_propose = yes\n' + extra,
            'GER = { set_temp_variable = { cwgg_settlement_new_kind = ' + str(kind) + ' } ' + S + '_begin = yes }'))

    # Recheck terms and the complete live belligerent set at every signature.
    validate = '''set_variable = { cwgg_settlement_invalid = 0 }
if = { limit = { COLDWAR_GER_1970_settlement_terms_valid = no } set_variable = { cwgg_settlement_invalid = 1 } }
every_country = {
 limit = {
  COLDWAR_GER_1970_settlement_belligerent = yes
  NOT = { is_in_array = { array = GER.cwgg_settlement_participants value = THIS } }
 }
 GER = { set_variable = { cwgg_settlement_invalid = 1 } }
}
for_each_scope_loop = {
 array = cwgg_settlement_participants
 if = { limit = { OR = { exists = no COLDWAR_GER_1970_settlement_belligerent = no } } GER = { set_variable = { cwgg_settlement_invalid = 1 } } }
}
'''
    effects += block(S + '_validate', validate)
    effects += block(S + '_accept', iff(S + '_can_sign = yes', '''GER = { COLDWAR_GER_1970_settlement_validate = yes }
if = { limit = { GER = { check_variable = { cwgg_settlement_invalid = 0 } } }
 GER = {
  add_to_array = { cwgg_settlement_signatures = PREV }
  COLDWAR_GER_1970_settlement_try_apply = yes
 }
}
else = { GER = { COLDWAR_GER_1970_settlement_fail = yes } }
'''))
    effects += block(S + '_refuse', iff(S + '_can_sign = yes', 'GER = { ' + S + '_fail = yes }'))
    effects += block(S + '_cancel', iff('OR = { tag = GER tag = DDR } GER = { has_country_flag = cwgg_settlement_pending }',
        'GER = { ' + S + '_fail = yes }'))
    effects += block(S + '_fail', '''if = { limit = { has_country_flag = cwgg_settlement_pending }
 for_each_scope_loop = { array = cwgg_settlement_participants country_event = { id = COLDWAR_GER_BALANCE.6 } }
 COLDWAR_GER_1970_settlement_clear = yes
}
''')
    effects += block(S + '_try_apply', '''COLDWAR_GER_1970_settlement_validate = yes
set_variable = { cwgg_settlement_unsigned = 0 }
for_each_scope_loop = {
 array = cwgg_settlement_participants
 if = { limit = { NOT = { is_in_array = { array = GER.cwgg_settlement_signatures value = THIS } } }
  GER = { set_variable = { cwgg_settlement_unsigned = 1 } }
 }
}
if = { limit = { check_variable = { cwgg_settlement_invalid = 0 } check_variable = { cwgg_settlement_unsigned = 0 } has_country_flag = cwgg_settlement_pending }
 COLDWAR_GER_1970_settlement_apply = yes
}
else_if = { limit = { check_variable = { cwgg_settlement_invalid > 0 } } COLDWAR_GER_1970_settlement_fail = yes }
''')
    # A final guard protects direct/stale helper calls too, not only event buttons.
    effects += block(S + '_apply', '''COLDWAR_GER_1970_settlement_validate = yes
set_variable = { cwgg_settlement_unsigned = 0 }
for_each_scope_loop = {
 array = cwgg_settlement_participants
 if = { limit = { NOT = { is_in_array = { array = GER.cwgg_settlement_signatures value = THIS } } }
  GER = { set_variable = { cwgg_settlement_unsigned = 1 } }
 }
}
if = { limit = {
 tag = GER
 has_country_flag = cwgg_settlement_pending
 check_variable = { cwgg_settlement_participants^num > 1 }
 COLDWAR_GER_1970_settlement_terms_valid = yes
 check_variable = { cwgg_settlement_invalid = 0 }
 check_variable = { cwgg_settlement_unsigned = 0 }
}
 if = { limit = { check_variable = { cwgg_settlement_kind = 2 } } DDR = { transfer_state = 1251 } }
 if = { limit = { check_variable = { cwgg_settlement_kind = 3 } }
  DDR = { set_temp_variable = { treasury_change = -0.2 } modify_treasury_effect = yes }
  set_temp_variable = { treasury_change = 0.2 }
  modify_treasury_effect = yes
 }
 # Only expressly consenting belligerents can be released from their wars.
 # Leave wars between third countries intact, even if both signed this proposal.
 for_each_scope_loop = {
  array = cwgg_settlement_participants
  if = { limit = { has_war_with = GER } white_peace = GER }
  if = { limit = { has_war_with = DDR } white_peace = DDR }
 }
 clr_country_flag = cwgg_war_active
 clr_country_flag = cwgg_war_victory_ddr
 clr_global_flag = cwgg_german_war
 for_each_scope_loop = { array = cwgg_settlement_participants country_event = { id = COLDWAR_GER_BALANCE.5 } }
 COLDWAR_GER_1970_settlement_clear = yes
 COLDWAR_GER_1970_rv_cold_peace = yes
 COLDWAR_GER_1970_rv_sync_views = yes
}
''')
    # Called only by the established GER monthly owner and by explicit proposals.
    effects += block(S + '_maintenance', '''if = { limit = { has_country_flag = cwgg_settlement_pending }
 COLDWAR_GER_1970_settlement_validate = yes
 if = { limit = { check_variable = { cwgg_settlement_invalid > 0 } } COLDWAR_GER_1970_settlement_fail = yes }
}
''')

    peace_preview = '''every_country = {
 limit = { COLDWAR_GER_1970_settlement_belligerent = yes }
 if = { limit = { has_war_with = GER } white_peace = GER }
 if = { limit = { has_war_with = DDR } white_peace = DDR }
}'''
    previews = {
        1: peace_preview,
        2: 'DDR = { transfer_state = 1251 } ' + peace_preview,
        3: 'DDR = { set_temp_variable = { treasury_change = -0.2 } modify_treasury_effect = yes } GER = { set_temp_variable = { treasury_change = 0.2 } modify_treasury_effect = yes } ' + peace_preview,
    }
    for kind, preview in previews.items():
        effects += block(S + '_preview_' + str(kind), 'effect_tooltip = { ' + preview + ' }')

    events = 'add_namespace = ' + NS + '\n'
    def event(number, title, desc, options):
        eid = NS + '.' + str(number)
        L(eid + '.t', title)
        L(eid + '.d', desc)
        return block('country_event', 'id = ' + eid + '\ntitle = ' + eid + '.t\ndesc = ' + eid + '.d\npicture = GFX_political_deal\nis_triggered_only = yes\n' + options)
    menu = ''
    for kind, name in ((1, 'Propose a Return to the Status Quo'), (2, 'Propose the West Berlin Settlement'), (3, 'Propose a Reparations Settlement')):
        key = NS + '.1.' + str(kind)
        L(key, name)
        extra = '' if kind == 1 else 'GER = { has_capitulated = yes } DDR = { has_capitulated = no } 1251 = { is_owned_by = GER }' if kind == 2 else 'GER = { has_capitulated = no } DDR = { has_capitulated = yes check_variable = { var = treasury compare = greater_than_or_equals value = 0.2 } }'
        menu += block('option', 'name = ' + key + '\ntrigger = { ' + S + '_can_propose = yes ' + extra + ' }\nai_chance = { base = 10 }\n' + S + '_preview_' + str(kind) + ' = yes\n' + S + '_propose_' + str(kind) + ' = yes')
    L(NS + '.close', 'Continue consultations.')
    menu += block('option', 'name = ' + NS + '.close\nai_chance = { base = 30 }')
    events += event(1, 'A German Peace Settlement', 'The German governments can offer a return to the pre-war position or negotiate limited settlement terms. Every belligerent must approve before the agreement enters into force.', menu)
    for kind, number, title in ((1, 2, 'Return to the Status Quo'), (2, 3, 'The West Berlin Settlement'), (3, 4, 'A German Reparations Settlement')):
        key = NS + '.' + str(number)
        L(key + '.accept', 'Approve the proposed terms.')
        L(key + '.refuse', 'Reject the proposed terms.')
        gate = S + '_can_sign = yes GER = { check_variable = { cwgg_settlement_kind = ' + str(kind) + ' } }'
        opts = block('option', 'name = ' + key + '.accept\ntrigger = { ' + gate + ' }\nai_chance = { base = 70 }\n' + S + '_preview_' + str(kind) + ' = yes\n' + S + '_accept = yes')
        opts += block('option', 'name = ' + key + '.refuse\ntrigger = { ' + gate + ' }\nai_chance = { base = 20 }\n' + S + '_refuse = yes')
        opts += block('option', 'name = ' + NS + '.close\nai_chance = { base = 10 }')
        events += event(number, title, 'A settlement of the German conflict has been submitted for approval. Each belligerent retains its government and alliance membership. The agreement takes effect only after all signatures are received.', opts)
    ack = NS + '.ack'
    L(ack, 'Inform the government.')
    events += event(5, 'German Settlement Concluded', 'All participating governments have approved the settlement. The agreed terms enter into force.', block('option', 'name = ' + ack))
    events += event(6, 'German Settlement Talks End', 'The proposal has been withdrawn, rejected or overtaken by changed conditions. No settlement has entered into force.', block('option', 'name = ' + ack))
    events += event(10, 'Bonn Imposes Diplomatic Sanctions', 'The Federal Republic has imposed diplomatic sanctions in response to our recognition of East Germany.', block('option', 'name = ' + ack))

    category = S + '_category'
    L(category, 'German Settlement Negotiations')
    L(category + '_desc', 'Review peace proposals, consult the belligerents and decide whether to approve the current terms. Each government retains its own signature.')
    categories = block(category, 'icon = GFX_decision_category_generic_political_actions\nallowed = { IMP_is_1970_scenario = yes }\nvisible = { OR = { AND = { OR = { tag = GER tag = DDR } ' + S + '_war_live = yes } has_country_flag = cwgg_settlement_invited } }')
    decisions = ''
    actions = [('review', 'Review Settlement Terms', 'OR = { tag = GER tag = DDR } ' + S + '_war_live = yes', S + '_open = yes'),
               ('accept', 'Approve the Current Proposal', S + '_can_sign = yes',
                ''.join(iff('GER = { check_variable = { cwgg_settlement_kind = ' + str(k) + ' } }', S + '_preview_' + str(k) + ' = yes') for k in (1, 2, 3)) + S + '_accept = yes'),
               ('reject', 'Reject the Current Proposal', S + '_can_sign = yes', S + '_refuse = yes'),
               ('cancel', 'Withdraw the Current Proposal', 'OR = { tag = GER tag = DDR } GER = { has_country_flag = cwgg_settlement_pending }', S + '_cancel = yes')]
    for key, name, gate, reward in actions:
        did = S + '_' + key
        L(did, name)
        decisions += block(did, 'icon = GFX_decision_negotiate_icon\ncost = 0\nvisible = { ' + gate + ' }\navailable = { ' + gate + ' }\ncomplete_effect = { ' + reward + ' }\nai_will_do = { base = 0 }')
    return {
        'common/scripted_effects/' + P + '_balance_diplomacy.txt': MARK + effects,
        'common/scripted_triggers/' + P + '_balance_diplomacy.txt': MARK + triggers,
        'events/' + P + '_balance_diplomacy.txt': MARK + events,
        'common/decisions/' + P + '_balance_diplomacy.txt': MARK + block(category, decisions),
        'common/decisions/categories/' + P + '_balance_diplomacy.txt': MARK + categories,
    }
