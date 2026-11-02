# IMPERIA COLD WAR — January 1970 UN membership and independent German recognition
"""Emit the scenario-specific contract; native MD arrays remain authoritative."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / 'tools'))
from multiplayer_quality.native_compat import startup_country_once
MARK = '# IMPERIA COLD WAR — January 1970 diplomacy\n'
# Contemporary 1969-70 GA list, with China represented by the ROC and the
# historical predecessors of the modern MD tags. No future admissions.
MEMBERS = '''AFG ALB ALG ARG AST AUS BAR BEL BOL BOT BRA ENG BUL BRM BUR BLR CBD CAM CAN CAR SRI
CHA CHL TAI COL CNG DRC COS CUB CYP CZE BEN DEN DOM ECU ELS EGU ETH FIN FRA GAB GAM
GAH GRE GUA GUI GUY HAI HON HUN ICE RAJ IND PER IRQ IRE ISR ITA CDI JAM JAP JOR KEN
KUW LAO LEB LES LIB LBA LUX MAD MLW MAY MLD MAL MLT MAU MRT MEX MON MOR NEP HOL NZL
NIC NGR NIG NRY PAK PAN PAR PRU PHI POL POR ROM RWA SAU SEN SIE SIN SOM SAF SYE SOV
SPR SUD SWA SWE SYR TNZ SIA TOG TRI TUN TUR UGA UKR EGY USA BFA URG VEN YEM SER ZAM'''.split()
DEPARTING_1970 = 'COL FIN NEP SPR ZAM'.split()
HELD_1971 = 'BUR NIC POL SIE SYR'.split()
PERMANENT = 'TAI FRA SOV USA ENG'.split()
# The 13 communist recognisers and six additional governments by 1 Jan 1970.
# The PRG of South Vietnam has no separate tag. SVN is Saigon, not the PRG.
DDR_RECOGNISERS = 'ALB BUL CHI CUB CZE HUN MON NKO POL ROM SOV VIE SER CBD IRQ SUD SYR SYE EGY'.split()
# Recognition of statehood is distinct from diplomatic relations or an embassy.
# Soviet recognition dates to 1955; Romania to 1967. Yugoslav ties resumed in 1968.
BRD_NON_RECOGNISERS = set('ALB BUL CHI CUB CZE HUN MON POL'.split())


def block(name, body):
    return name + ' = {\n' + body + '\n}\n'


def iff(gate, body):
    return block('if', 'limit = { ' + gate + ' }\n' + body)


def files():
    assert len(MEMBERS) == len(set(MEMBERS)) == 126
    trigger = block('COLDWAR_UN_1970_start_member', 'OR = {\n' + '\n'.join('tag = '+t for t in MEMBERS) + '\n}')
    trigger += block('COLDWAR_Germany_recognition_subject', 'IMP_is_1970_scenario = yes\nOR = { tag = GER tag = DDR }')
    # IMPERIA COLD WAR — Retain additional recognition subjects when rebuilding the original diplomacy files.
    trigger += block('COLDWAR_recognition_subject', '# IMPERIA COLD WAR — Recognition disputes are separate from UN membership and economic isolation.\nOR = { has_idea = lacks_international_recognition COLDWAR_Germany_recognition_subject = yes ICW_1970_additional_recognition_subject = yes }')
    trigger += block('COLDWAR_UN_can_apply', '''NOT = { is_in_array = { global.UN_general_assembly = THIS } }
NOT = { has_dynamic_modifier = { modifier = united_nations_member } }
NOT = { has_country_flag = recent_un_ascension_attempt }
has_civil_war = no''')
    trigger += block('COLDWAR_Germany_can_campaign', '''COLDWAR_Germany_recognition_subject = yes
NOT = { has_country_flag = recent_global_recog_request_campaign }
has_civil_war = no''')
    # IMPERIA COLD WAR — Refresh only the two existing views on explicit UN transactions.
    effect = block('COLDWAR_Germany_un_status_changed', '''if = {
 limit = { IMP_is_1970_scenario = yes }
 if = { limit = { country_exists = GER GER = { has_country_flag = cwgg_initialized } }
  GER = { COLDWAR_GER_1970_rv_sync_views = yes }
 }
 else_if = { limit = { country_exists = DDR }
  DDR = { COLDWAR_GER_1970_east_gui_refresh = yes }
 }
}''')
    effect += block('COLDWAR_Germany_recount_recognition', '''if = {
 limit = { COLDWAR_Germany_recognition_subject = yes }
 set_variable = { Granted_Recognition = 0 }
 every_country = {
  limit = { NOT = { tag = PREV } }
  if = { limit = { is_in_array = { recognised_countries = PREV } }
   PREV = { add_to_variable = { Granted_Recognition = 1 } }
  }
  # IMPERIA COLD WAR — Observe actual ledger transitions in the existing recount, not a second world scan.
  if = { limit = { PREV = { tag = DDR } } COLDWAR_Germany_observe_DDR_recognition = yes }
 }
 if = { limit = { tag = DDR } set_country_flag = COLDWAR_DDR_recognition_watch_initialized }
 if = { limit = { country_exists = GER GER = { has_country_flag = cwgg_initialized } }
  GER = { COLDWAR_GER_1970_rv_sync_views = yes }
 }
}''')
    effect += block('COLDWAR_Germany_seed_recognition_pp', '''# IMPERIA COLD WAR — Baseline the live recognition ledger once; old recognitions never generate retroactive political power.
if = {
 limit = { COLDWAR_Germany_recognition_subject = yes NOT = { has_country_flag = COLDWAR_Germany_recognition_pp_seeded } }
 every_country = {
  limit = { NOT = { tag = PREV } is_in_array = { recognised_countries = PREV } }
  PREV = { add_to_array = { cwgg_recognition_pp_paid = PREV } }
 }
 set_country_flag = COLDWAR_Germany_recognition_pp_seeded
}''')
    effect += block('COLDWAR_Germany_recognition_pp_once', '''# IMPERIA COLD WAR — A distinct live recogniser pays once per German state, even after withdrawal and restoration.
if = {
 limit = { COLDWAR_Germany_recognition_subject = yes IMP_is_1970_scenario = yes }
 if = { limit = { NOT = { has_country_flag = COLDWAR_Germany_recognition_pp_seeded } }
  # IMPERIA COLD WAR — A hot-loaded save safely baselines its current ledger before any award.
  COLDWAR_Germany_seed_recognition_pp = yes
 }
 if = { limit = {
  PREV = { exists = yes NOT = { tag = PREV } is_in_array = { recognised_countries = PREV } }
  NOT = { is_in_array = { cwgg_recognition_pp_paid = PREV } }
 }
  add_to_array = { cwgg_recognition_pp_paid = PREV }
  if = { limit = { PREV = { has_idea = non_power } } add_political_power = 5 }
  else_if = { limit = { PREV = { has_idea = minor_power } } add_political_power = 10 }
  else_if = { limit = { PREV = { has_idea = regional_power } } add_political_power = 15 }
  else_if = { limit = { PREV = { has_idea = large_power } } add_political_power = 25 }
  else_if = { limit = { PREV = { has_idea = great_power } } add_political_power = 50 }
  else_if = { limit = { PREV = { has_idea = super_power } } add_political_power = 100 }
 }
}''')
    effect += block('COLDWAR_Germany_observe_DDR_recognition', '''# IMPERIA COLD WAR — THIS is the recognising country; PREV is DDR in the recount.
if = { limit = { is_in_array = { recognised_countries = DDR } }
 if = { limit = { NOT = { has_country_flag = COLDWAR_DDR_recognition_observed } }
  set_country_flag = COLDWAR_DDR_recognition_observed
  if = { limit = {
   DDR = { has_country_flag = COLDWAR_DDR_recognition_watch_initialized }
   NOT = { has_global_flag = COLDWAR_DDR_recognition_seeding }
  }
   save_event_target_as = COLDWAR_Germany_recogniser
   if = { limit = { country_exists = GER }
    GER = { country_event = { id = COLDWAR_GERMAN_RECOGNITION.1 } }
    # A withdrawal/regrant still produces a truthful notice, but cannot farm new crises.
    if = { limit = { NOT = { tag = GER } NOT = { has_country_flag = COLDWAR_DDR_recognition_ever_observed } }
     GER = {
      if = { limit = {
       has_country_flag = cwgg_initialized
       has_idea = COLDWAR_GER_1970_idea_hallstein_legacy
       check_variable = { cwgg_vertrag_3 = 0 }
       check_variable = { cwgg_hebel_recht > 1 }
       check_variable = { cwgg_krise_typ = 0 }
       NOT = { has_country_flag = cwgg_crisis_cd }
       NOT = { has_country_flag = cwgg_strike_ordered }
       NOT = { DDR = { has_country_flag = cwgg_ddr_countdown_dialogue_open } }
       NOT = { has_war_with = DDR }
       NOT = { has_global_flag = COLDWAR_GER_1970_unity_achieved }
      }
       # IMPERIA COLD WAR — Preserve the actual recognising state only when a new type-5 crisis starts.
       clear_array = cwgg_recognition_country
       event_target:COLDWAR_Germany_recogniser = { GER = { add_to_array = { cwgg_recognition_country = PREV } } }
       set_temp_variable = { cwgg_t_typ = 5 }
       COLDWAR_GER_1970_rv_start_crisis = yes
      }
     }
    }
   }
  }
  set_country_flag = COLDWAR_DDR_recognition_ever_observed
 }
}
else_if = { limit = { has_country_flag = COLDWAR_DDR_recognition_observed }
 clr_country_flag = COLDWAR_DDR_recognition_observed
 if = { limit = {
  DDR = { has_country_flag = COLDWAR_DDR_recognition_watch_initialized }
  NOT = { has_global_flag = COLDWAR_DDR_recognition_seeding }
  country_exists = GER
 }
  save_event_target_as = COLDWAR_Germany_recogniser
  GER = { country_event = { id = COLDWAR_GERMAN_RECOGNITION.2 } }
 }
}''')
    effect += block('COLDWAR_Germany_campaign_recognition', '''custom_effect_tooltip = campaign_attempt_tt
hidden_effect = { if = {
 limit = { COLDWAR_Germany_can_campaign = yes }
 set_country_flag = { flag = recent_global_recog_request_campaign days = 365 }
 country_event = recognition.17
 international_systems_force_update = yes
} }''')
    effect += block('COLDWAR_UN_submit_application', '''if = {
 limit = { COLDWAR_UN_can_apply = yes }
 set_country_flag = { flag = recent_un_ascension_attempt days = 365 }
 set_temp_variable = { sc_new_vote_type = 5 }
 set_temp_variable = { sc_new_vote_nation = THIS }
 update_sc_vote = yes
}''')
    effect += block('COLDWAR_Germany_joint_un_applications', '''custom_effect_tooltip = COLDWAR_Germany_joint_un_applications_tt
hidden_effect = {
if = { limit = { IMP_is_1970_scenario = yes tag = GER country_exists = DDR }
COLDWAR_UN_submit_application = yes
if = { limit = { country_exists = DDR } DDR = { COLDWAR_UN_submit_application = yes } }
}
}''')
    effect += block('COLDWAR_Germany_recognise_DDR', '''custom_effect_tooltip = COLDWAR_Germany_recognise_DDR_tt
hidden_effect = { if = {
 limit = { IMP_is_1970_scenario = yes country_exists = DDR NOT = { tag = DDR } NOT = { is_in_array = { recognised_countries = DDR } } }
 add_to_array = { recognised_countries = DDR }
 DDR = { recognition_grant_increment = yes }
 international_systems_force_update = yes
} }''')
    effect += block('COLDWAR_Germany_mutual_recognition', '''custom_effect_tooltip = COLDWAR_Germany_mutual_recognition_tt
hidden_effect = { if = {
 limit = { IMP_is_1970_scenario = yes country_exists = GER country_exists = DDR }
 GER = { if = { limit = { NOT = { is_in_array = { recognised_countries = DDR } } } add_to_array = { recognised_countries = DDR } } }
 DDR = { if = { limit = { NOT = { is_in_array = { recognised_countries = GER } } } add_to_array = { recognised_countries = GER } } }
 GER = { COLDWAR_Germany_recount_recognition = yes }
 DDR = { COLDWAR_Germany_recount_recognition = yes }
 international_systems_force_update = yes
} }''')
    effect += block('COLDWAR_Germany_retire_recognition_points', '''if = {
 limit = { IMP_is_1970_scenario = yes OR = { tag = GER tag = DDR } }
 clear_variable = cwddr_recognition
 clr_country_flag = COLDWAR_GER_1970_un_member
 remove_ideas = COLDWAR_GER_1970_idea_un_member
 remove_ideas = COLDWAR_GER_1970_idea_unsc_member
 COLDWAR_Germany_recount_recognition = yes
}''')
    # No new monthly world scan: only setup and explicit player transactions.
    init = '''if = {
 limit = { IMP_is_1970_scenario = yes NOT = { has_global_flag = COLDWAR_UN_1970_initialized } }
 set_global_flag = COLDWAR_UN_1970_initialized
 set_global_flag = COLDWAR_DDR_recognition_seeding
 # Remove inherited MD membership before assembling the historical roster.
 every_country = {
  if = { limit = { has_idea = p5_member } remove_ideas = p5_member }
  if = { limit = { has_dynamic_modifier = { modifier = united_nations_member } } remove_dynamic_modifier = { modifier = united_nations_member } }
 }
 clear_array = global.UN_general_assembly
 clear_array = global.security_council_members
 clear_array = global.p5_sc_members
 clear_array = global.new_council_members
 clear_array = global.confirmed_new_council_members
 if = { limit = { country_exists = TAI } TAI = { remove_ideas = lacks_international_recognition remove_ideas = non_state_actor } }
 # IMPERIA COLD WAR — An upstream startup may already have removed Taiwan from this ledger.
 if = { limit = { is_in_array = { global.Unrecognised_States = TAI } } remove_from_array = { global.Unrecognised_States = TAI } }
'''
    for t in MEMBERS:
        init += iff('country_exists = '+t, t+' = { add_to_array = { global.UN_general_assembly = THIS } add_dynamic_modifier = { modifier = united_nations_member } }')
    # Native January rotation consumes slots 0-4 first. P5 must stay at 10-14.
    for t in DEPARTING_1970 + HELD_1971 + PERMANENT:
        init += 'add_to_array = { global.security_council_members = '+t+' }\n'
    for t in PERMANENT:
        init += t+' = { add_ideas = p5_member }\n'
    # Keep existing foreign-state recognition intact, including dual recognition.
    for subject,recognisers in [('DDR', DDR_RECOGNISERS), ('GER',[t for t in MEMBERS if t not in BRD_NON_RECOGNISERS] + ['SWI','KOR','SVN'])]:
        for t in recognisers:
            init += iff('country_exists = '+subject+' country_exists = '+t, t+' = { if = { limit = { NOT = { is_in_array = { recognised_countries = '+subject+' } } } add_to_array = { recognised_countries = '+subject+' } } }')
    init += '''if = { limit = { country_exists = GER } GER = { COLDWAR_Germany_recount_recognition = yes } }
if = { limit = { country_exists = DDR } DDR = { COLDWAR_Germany_recount_recognition = yes } }
if = { limit = { country_exists = GER } GER = { COLDWAR_Germany_seed_recognition_pp = yes } }
if = { limit = { country_exists = DDR } DDR = { COLDWAR_Germany_seed_recognition_pp = yes } }
clr_global_flag = COLDWAR_DDR_recognition_seeding
recompute_un_2_3_number = yes
recompute_un_sc_required_yes = yes
international_systems_force_update = yes
}'''
    effect += block('COLDWAR_UN_1970_initialize', init)
    loc = r'''l_english:
# IMPERIA COLD WAR — Native German diplomatic recognition
 COLDWAR_Germany_recognition_count:0 "Recognising states"
 COLDWAR_Germany_mutual_recognition_tt:0 "Mutual diplomatic recognition: §YFederal Republic of Germany§! and §YGerman Democratic Republic§!."
 COLDWAR_Germany_joint_un_applications_tt:0 "UN membership applications: §YFederal Republic of Germany§! and §YGerman Democratic Republic§!."
 COLDWAR_Germany_campaign_tt:0 "Recognition requests to §YUN member states§!."
 COLDWAR_Germany_recognise_DDR_tt:0 "Diplomatic recognition: §Y[DDR.GetName]§!."
 COLDWAR_Germany_un_applications_status:0 "[COLDWAR_Germany_UN_pair_status]"
 COLDWAR_Germany_UN_both:0 "§GUN members: both German states§!"
 COLDWAR_Germany_UN_GER_only:0 "§YUN member: Federal Republic only§!"
 COLDWAR_Germany_UN_DDR_only:0 "§YUN member: German Democratic Republic only§!"
 COLDWAR_Germany_UN_neither:0 "§YUN members: neither German state§!"
 COLDWAR_Germany_UN_permanent:0 "Permanent Security Council member"
 COLDWAR_Germany_UN_elected:0 "Elected Security Council member"
 COLDWAR_Germany_UN_assembly:0 "General Assembly member"
 COLDWAR_Germany_UN_outside:0 "Outside the United Nations"
 COLDWAR_Germany_UN_absent:0 "State no longer exists"
 COLDWAR_GERMAN_RECOGNITION.1.t:0 "[COLDWAR_Germany_recogniser.GetName] Recognises East Germany"
 COLDWAR_GERMAN_RECOGNITION.1.d:0 "[COLDWAR_Germany_recogniser.GetName] has recognised the German Democratic Republic. The Foreign Office has updated the inner-German dossier.\n\nGovernments recognising East Germany: §Y[?DDR.Granted_Recognition|0]§!."
 COLDWAR_GERMAN_RECOGNITION.2.t:0 "[COLDWAR_Germany_recogniser.GetName] Withdraws Recognition"
 COLDWAR_GERMAN_RECOGNITION.2.d:0 "[COLDWAR_Germany_recogniser.GetName] has withdrawn its recognition of the German Democratic Republic. The Foreign Office has updated the inner-German dossier.\n\nGovernments recognising East Germany: §Y[?DDR.Granted_Recognition|0]§!."
 COLDWAR_GERMAN_RECOGNITION.acknowledge:0 "Inform the Federal Chancellery."
'''
    # IMPERIA COLD WAR — Treaty receipts are distinct from actual membership and current council seats.
    member = 'has_dynamic_modifier = { modifier = united_nations_member }'
    def dt(name, choices, default):
        return 'defined_text = {\n\tname = '+name+'\n'+''.join(
            '\ttext = {\n\t\ttrigger = { '+gate+' }\n\t\tlocalization_key = '+key+'\n\t}\n' for gate,key in choices)+\
            '\ttext = {\n\t\tlocalization_key = '+default+'\n\t}\n}\n'
    status = dt('COLDWAR_Germany_UN_pair_status', [
        ('GER = { '+member+' } DDR = { '+member+' }', 'COLDWAR_Germany_UN_both'),
        ('GER = { '+member+' }', 'COLDWAR_Germany_UN_GER_only'),
        ('DDR = { '+member+' }', 'COLDWAR_Germany_UN_DDR_only')], 'COLDWAR_Germany_UN_neither')
    for tag in ('GER','DDR'):
        status += dt('COLDWAR_'+tag+'_UN_status', [
            ('NOT = { country_exists = '+tag+' }', 'COLDWAR_Germany_UN_absent'),
            (tag+' = { '+member+' is_in_array = { global.p5_sc_members = THIS } }', 'COLDWAR_Germany_UN_permanent'),
            (tag+' = { '+member+' is_on_un_sec_council = yes }', 'COLDWAR_Germany_UN_elected'),
            (tag+' = { '+member+' }', 'COLDWAR_Germany_UN_assembly')], 'COLDWAR_Germany_UN_outside')
    hook_body = '''if = { limit = { IMP_is_1970_scenario = yes }
   if = { limit = { country_exists = GER } GER = { COLDWAR_Germany_retire_recognition_points = yes COLDWAR_Germany_seed_recognition_pp = yes } }
   if = { limit = { country_exists = DDR } DDR = { COLDWAR_Germany_retire_recognition_points = yes COLDWAR_Germany_seed_recognition_pp = yes } }
  }
'''
    hook = 'on_actions = {\n on_startup = { effect = {\n' + startup_country_once(hook_body, 'german_recognition') + '\n } }\n}'
    return {'common/scripted_triggers/COLDWAR_diplomacy_1970.txt': MARK+trigger,
            'common/scripted_effects/COLDWAR_diplomacy_1970.txt': MARK+effect,
            'common/on_actions/COLDWAR_diplomacy_1970.txt': MARK+hook,
            'common/scripted_localisation/COLDWAR_diplomacy_1970.txt': MARK+status,
            'localisation/english/COLDWAR_diplomacy_1970_l_english.yml':loc,
            'events/COLDWAR_German_recognition_1970.txt': MARK + '''add_namespace = COLDWAR_GERMAN_RECOGNITION
country_event = {
 id = COLDWAR_GERMAN_RECOGNITION.1
 title = COLDWAR_GERMAN_RECOGNITION.1.t
 desc = COLDWAR_GERMAN_RECOGNITION.1.d
 picture = GFX_political_deal
 is_triggered_only = yes
 option = { name = COLDWAR_GERMAN_RECOGNITION.acknowledge }
}
country_event = {
 id = COLDWAR_GERMAN_RECOGNITION.2
 title = COLDWAR_GERMAN_RECOGNITION.2.t
 desc = COLDWAR_GERMAN_RECOGNITION.2.d
 picture = GFX_political_deal
 is_triggered_only = yes
 option = { name = COLDWAR_GERMAN_RECOGNITION.acknowledge }
}
'''}


if __name__ == '__main__':
    for rel,text in files().items():
        (ROOT/rel).write_text(text,encoding='utf-8-sig' if rel.endswith('.yml') else 'utf-8',newline='\n')
    from native_hooks import apply_recognition_hooks
    apply_recognition_hooks(ROOT)
    (Path(__file__).parent/'roster.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',date='1970-01-01',general_assembly=MEMBERS,security_council=DEPARTING_1970+HELD_1971+PERMANENT,permanent_members=PERMANENT,ddr_recognisers=DDR_RECOGNISERS),indent=2)+'\n',encoding='utf-8')
    print('Written historical UN roster and native recognition helpers.')
