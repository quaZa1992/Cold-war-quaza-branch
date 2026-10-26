# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""Decisions for West Germany 1970 (and a small GDR category for an East German player)."""
from cw_lib import *
from tooltips import nice, hide_vars

CATS = {}        # key -> dict
DECISIONS = {}   # cat -> list of script strings
USED_DEC_ICONS = set()

GER_VIS = "original_tag = GER IMP_is_1970_scenario = yes"
DDR_VIS = "original_tag = DDR IMP_is_1970_scenario = yes"


def C(key, name, desc, icon, visible, tag="GER", priority=150):
    cid = f"{P}_{key}_category"
    L(cid, name)
    L(cid + "_desc", desc)
    CATS[cid] = (icon, visible, tag, priority)
    DECISIONS[cid] = []
    return cid


def D(cat, key, name, desc, icon, visible="", available="", cost=50, effect="", ai=10, re_enable=None,
      once=False, targets=None, target_trigger="", remove_effect="", days_remove=None, ai_extra=""):
    did = f"{P}_dec_{key}"
    L(did, name)
    L(did + "_desc", desc)
    USED_DEC_ICONS.add(icon)
    out = [f"\t{did} = {{", f"\t\ticon = {icon}", f"\t\tcost = {cost}"]
    if targets:
        out.append(f"\t\ttargets = {{ {' '.join(targets)} }}")
        out.append(f"\t\ttarget_trigger = {{ FROM = {{ exists = yes {target_trigger} }} }}")
    if once:
        out.append("\t\tfire_only_once = yes")
    if re_enable:
        out.append(f"\t\tdays_re_enable = {re_enable}")
    out.append(f"\t\tvisible = {{ {visible} }}")
    if available:
        out.append(f"\t\tavailable = {{ {nice(available)} }}")
    if days_remove:
        out.append(f"\t\tdays_remove = {days_remove}")
        out.append("\t\tcomplete_effect = {\n" + fmt(hide_vars(effect), 3) + "\n\t\t}")
        out.append("\t\tremove_effect = {\n" + fmt(remove_effect, 3) + "\n\t\t}")
    else:
        out.append("\t\tcomplete_effect = {\n" + fmt(hide_vars(effect), 3) + "\n\t\t}")
    out.append(f"\t\tai_will_do = {{ base = {ai} {ai_extra} }}")
    out.append("\t}")
    DECISIONS[cat].append("\n".join(out))
    return did


def M(cat, key, name, desc, icon, activation, available, days, complete="", timeout="", cancel="", good=False):
    """A mission: starts by itself when `activation` is true, succeeds when `available`
    becomes true before the timer runs out, fails (timeout_effect) otherwise."""
    did = f"{P}_dec_{key}"
    L(did, name)
    L(did + "_desc", desc)
    USED_DEC_ICONS.add(icon)
    out = [f"\t{did} = {{", f"\t\ticon = {icon}", f"\t\tactivation = {{ {activation} }}",
           f"\t\tavailable = {{ {nice(available)} }}", f"\t\tdays_mission_timeout = {days}",
           f"\t\tis_good = {'yes' if good else 'no'}"]
    if cancel:
        out.append(f"\t\tcancel_trigger = {{ {cancel} }}")
    out.append("\t\tcomplete_effect = {\n" + fmt(hide_vars(complete), 3) + "\n\t\t}")
    out.append("\t\ttimeout_effect = {\n" + fmt(hide_vars(timeout), 3) + "\n\t\t}")
    out.append("\t\tai_will_do = { base = 1 }")
    out.append("\t}")
    DECISIONS[cat].append("\n".join(out))
    return did


def ddr_meters():
    return ("GDR crisis index: §Y[?DDR.cwddr_crisis|0]§! | exit pressure: §Y[?DDR.cwddr_exit_pressure|0]§! | hard-currency shortage: §Y[?DDR.cwddr_hard_currency|0]§!\n"
            "Dependence on Bonn: §Y[?DDR.cwddr_west_dependency|0]§! | SED control: §Y[?DDR.cwddr_sed_control|0]§! | Moscow's guarantee: §Y[?DDR.cwddr_moscow_backing|0]§!")


# ================================================================= DEUTSCHLANDPOLITIK
DP = C("deutschlandpolitik", "Deutschlandpolitik",
       "Two states, one nation. Every credit, every prisoner released and every transit agreement moves the balance between §YLegal Position§! and §YChange through Rapprochement§!.\n\n"
       "Inner-German rapprochement: §Y[?cwger_ostpolitik|0]§! | Berlin access: §Y[?cwger_berlin_access|0]§! | Unity momentum: §Y[?cwger_unity|0]§!\n"
       "Übersiedler from the GDR since 1970: §Y[?cwger_uebersiedler_k|0]§! thousand | Burden of the East: §Y[?cwger_east_burden|0]§!\n" + ddr_meters(),
       "GFX_decision_category_generic_political_actions",
       f"{GER_VIS} OR = {{ country_exists = DDR has_global_flag = {P}_unity_achieved }}", priority=200)

D(DP, "open_rivalry_window", "Open the Inner-German Relations Window",
  "Climate, escalation ladder, crises, levers, channels and treaties with the GDR are run from the §YInner-German Relations§! window (also on the top bar).",
  "GFX_decision_germany", visible="has_country_flag = cwgg_initialized", cost=0,
  effect=J("set_country_flag = cwgg_open", "set_variable = { cwgg_tab = 1 }", f"{P}_rv_gui_refresh = yes"), ai=0)
D(DP, "currency_one_to_one", "Conversion Rate: One to One",
  "Wages and savings converted one to one. The East Germans get the D-Mark at a price the East German economy cannot survive.",
  "GFX_decision_money_dec", visible=f"has_completed_focus = {P}_monetary_union_offer NOT = {{ has_country_flag = {P}_currency_rate_set }}",
  cost=50, once=True,
  effect=J(f"set_country_flag = {P}_currency_rate_set", v("cwger_unity", 10), v("cwger_east_burden", 15), v("cwger_bundesbank", 15),
           dv("cwddr_exit_pressure", -10), stab(0.03), party("cdu", 0.006)), ai=60)
D(DP, "currency_two_to_one", "Conversion Rate: Two to One",
  "The Bundesbank's proposal: two Ostmarks for one D-Mark. Sound money, angry crowds in Leipzig.",
  "GFX_decision_money_dec", visible=f"has_completed_focus = {P}_monetary_union_offer NOT = {{ has_country_flag = {P}_currency_rate_set }}",
  cost=50, once=True,
  effect=J(f"set_country_flag = {P}_currency_rate_set", v("cwger_unity", 4), v("cwger_east_burden", 5), v("cwger_bundesbank", -10),
           dv("cwddr_exit_pressure", 5), dv("cwddr_opposition", 4)), ai=40)
D(DP, "reopen_unity", "Reopen Unity Talks",
  "The moment has passed once. Try again: new proposals for East Berlin and the Four Powers.",
  "GFX_decision_germany", visible=f"has_country_flag = {P}_unity_postponed country_exists = DDR {f'NOT = {{ has_global_flag = {P}_unity_achieved }}'}",
  available=f"DDR = {{ check_variable = {{ cwddr_wende_stage > 3 }} check_variable = {{ cwddr_wende_stage < 9 }} }} OR = {{ NOT = {{ has_country_flag = {P}_soviets_refused }} DDR = {{ check_variable = {{ cwddr_moscow_backing < 30 }} }} }}",
  cost=75, re_enable=180,
  effect=J(f"clr_country_flag = {P}_unity_postponed", f"clr_country_flag = {P}_soviets_refused", f"country_event = {{ id = {EVG}.135 days = 1 }}"), ai=30)
D(DP, "aufbau_ost_programme", "Aufbau Ost Investment Programme",
  "Motorways, telephone lines and sewage works for the new Länder, paid for on credit.",
  "GFX_decision_generic_factory", visible=f"has_global_flag = {P}_unity_achieved",
  available="check_variable = { cwger_east_burden > 10 }", cost=50, re_enable=365,
  effect=J(debt_gdp(0.006), infra(2), build("industrial_complex", 1, 1), v("cwger_east_burden", -8), party("pds", -0.002)), ai=20)

# ===================================================================== POLITICS
PO = C("bonn_politics", "Bonn Politics",
       "Bundestag: government §Y[?cwger_seats_gov|0]§! of §Y[?cwger_seats_total|0]§! seats (majority §Y[?cwger_majority|0]§!).\n"
       "FDP course: §Y[?cwger_fdp_course|0]§! (negative = social-liberal, positive = market-liberal) | CSU autonomy: §Y[?cwger_csu_autonomy|0]§! | Union share of the Bundesrat: §Y[?cwger_bundesrat_union|0]§!%\n"
       "Scandal pressure: §Y[?cwger_scandal|0]§! | Bundesbank friction: §Y[?cwger_bundesbank|0]§!",
       "GFX_decisions_category_political", GER_VIS, priority=190)
D(PO, "mediation_committee", "The Mediation Committee",
  "The opposition controls the Bundesrat. Negotiate a package deal in the Vermittlungsausschuss.",
  "GFX_decision_negotiate_icon", visible=f"has_country_flag = {P}_mediation_unlocked",
  available="OR = { AND = { check_variable = { ruling_party = 3 } check_variable = { cwger_bundesrat_union > 50 } } AND = { check_variable = { ruling_party = 1 } check_variable = { cwger_bundesrat_union < 50 } } }",
  cost=40, re_enable=365, effect=J(pp(60), stab(0.01), faction("mittelstand", 3)), ai=15)
D(PO, "coalition_committee", "Coalition Committee",
  "A long night in the Chancellor's Bungalow to bind the Free Democrats to the government's course.",
  "GFX_decision_negotiate_icon", visible="is_in_array = { gov_coalition_array = 2 }", cost=50, re_enable=365,
  effect=J("if = { limit = { check_variable = { ruling_party = 3 } } " + v("cwger_fdp_course", -10, show=False) + " } else = { " + v("cwger_fdp_course", 10, show=False) + " }",
           tt(f"{P}_tt_coalition_committee", "The FDP course moves §Y10§! points towards the chancellor's party."), party("fdp", -0.002)), ai=20)
D(PO, "party_congress", "Party Congress",
  "Rally the chancellor's party behind the government.",
  "GFX_decision_elections_button", visible="OR = { check_variable = { ruling_party = 1 } check_variable = { ruling_party = 3 } }",
  available="NOT = { has_country_flag = elections_in_progress }", cost=75, re_enable=540,
  effect="if = { limit = { check_variable = { ruling_party = 3 } } " + party("spd", 0.008) + " } else = { " + party("cdu", 0.008) + " }", ai=10)
D(PO, "vote_of_confidence", "Ask for a Vote of Confidence",
  "Article 68: lose a vote of confidence on purpose and the Federal President can dissolve the Bundestag.",
  "GFX_decision_elections_button", visible="always = yes",
  available="NOT = { has_country_flag = elections_in_progress } NOT = { has_country_flag = generic_election_killswitch }",
  cost=100, re_enable=720, effect=f"country_event = {{ id = {EVG}.23 days = 1 }}", ai=1)
D(PO, "clean_house", "Clean House",
  "Parliamentary inquiries, a new code on party financing and a few resignations before the magazines force them.",
  "GFX_decisions_police", visible="check_variable = { cwger_scandal > 25 }", cost=60, re_enable=365,
  effect=J(v("cwger_scandal", -20), pp(-25), v("cwger_rechtsstaat", 2), corruption(False)), ai=15)
D(PO, "concerted_action", "Concerted Action",
  "Unions, employers, the Bundesbank and the government at one table: wage guidelines in return for jobs.",
  "GFX_decision_negotiate_icon", visible="always = yes", cost=50, re_enable=730,
  effect=J(faction("dgb", 5), faction("bdi", 5), v("cwger_bundesbank", -5), stab(0.01)), ai=12)

# ===================================================================== SECURITY
SE = C("internal_security", "Internal Security",
       "Security state: §Y[?cwger_security|0]§! | Rule-of-law credibility: §Y[?cwger_rechtsstaat|0]§!\n"
       "Terror threat - left: §Y[?cwger_terror_left|0]§! right: §Y[?cwger_terror_right|0]§! foreign: §Y[?cwger_terror_foreign|0]§!\n"
       "RAF generation §Y[?cwger_raf_gen|0]§!, active cadre §Y[?cwger_raf_cadre|0]§!, sympathiser milieu §Y[?cwger_raf_milieu|0]§!, prisoners §Y[?cwger_raf_prisoners|0]§!\n"
       "BKA capability §Y[?cwger_bka_level|0]§! | GSG 9 tier §Y[?cwger_gsg9_tier|0]§! | Counter-intelligence §Y[?cwger_counterintel|0]§! vs Stasi penetration §Y[?cwger_stasi_penetration|0]§!",
       "GFX_decision_category_generic_political_actions", GER_VIS, priority=185)
D(SE, "open_security_window", "Open the Internal Security Window",
  "The wanted list, the RAF's targets and protection details, the prisons and the crisis staff are run from the §YInternal Security§! window (also on the top bar).",
  "GFX_decisions_police", visible="has_country_flag = cwsec_initialized", cost=0,
  effect=J("set_country_flag = cwsec_open", "set_variable = { cwsec_tab = 1 }", f"{P}_sec_gui_refresh = yes"), ai=0)
# ===================================================================== ECONOMY / DEFENCE
EC = C("economy_defence", "Economy and Defence",
       "Imperia Arms Demand: §Y[?global.mdcw_cw_arms|0]§! | Cold War world tension: §Y[?global.mdcw_cw_tension|0]§! | Western integration: §Y[?cwger_westbindung|0]§! | Peace movement: §Y[?cwger_peace_movement|0]§!",
       "GFX_decisions_category_dept", GER_VIS, priority=180)
D(EC, "approve_arms_export", "Approve an Arms Export",
  "Leopards, Type 209 submarines, frigates: the Federal Security Council meets in secret. Revenue follows Imperia Arms Demand.",
  "GFX_decision_military_plan", visible=f"has_country_flag = {P}_export_guidelines", cost=25, re_enable=365,
  effect=J("set_temp_variable = { cwger_t_mic = global.IMP_military_industrial_complex_total_bonus }",
           "multiply_temp_variable = { cwger_t_mic = 4 }", "add_to_temp_variable = { cwger_t_mic = 1 }",
           "clamp_temp_variable = { var = cwger_t_mic min = 0.6 max = 2.6 }",
           "set_temp_variable = { treasury_change = gdp_total }", "multiply_temp_variable = { treasury_change = 0.0012 }",
           "multiply_temp_variable = { treasury_change = cwger_t_mic }", "modify_treasury_effect = yes",
           tt(f"{P}_tt_arms_demand", "Revenue follows the Imperia §Yarms market§! (Arms Demand and wars): between §Y60%§! and §Y260%§! of the base sale."),
           v("cwger_scandal", 4), v("cwger_peace_movement", 2)), ai=20)
D(EC, "bundestag_mandate", "Bundestag Mandate for a Deployment",
  "Ask the Bundestag to approve an armed mission under a UN or NATO mandate.",
  "GFX_decision_nato", visible=f"has_country_flag = {P}_deployments_allowed", cost=50, re_enable=730,
  effect=J("army_experience = 10", v("cwger_westbindung", 4), v("cwger_peace_movement", 4), money_gdp(-0.0008)), ai=10)
D(EC, "energy_security", "Strategic Oil Reserve",
  "Fill the salt caverns of Etzel with crude oil against the next embargo.",
  "GFX_decision_oil", visible=f"has_country_flag = {P}_oil_shock_seen", cost=40, once=True,
  effect=J(money_gdp(-0.001), f"add_timed_idea = {{ idea = {P}_idea_car_free_sundays days = 30 }}",
           f"if = {{ limit = {{ has_idea = {P}_idea_stagflation }} remove_ideas = {P}_idea_stagflation }}"), ai=15)
for tag, name in [("POL", "Poland"), ("HUN", "Hungary"), ("ROM", "Romania"), ("BUL", "Bulgaria")]:
    D(EC, f"lift_cocom_{tag.lower()}", f"Ease COCOM Restrictions on {name}",
      f"Allow dual-use machinery to be exported to {name}. Washington will grumble; Krupp and Siemens will not.",
      "GFX_decision_attract_foreign_investor", visible=f"country_exists = {tag} {tag} = {{ is_in_array = {{ imp_mil_sanc_on_us = ROOT }} }}",
      available="check_variable = { cwger_ostpolitik > 45 }", cost=50, once=True,
      effect=J(f"{tag} = {{ ROOT = {{ {P}_lift_mil_sanction_on_prev = yes }} add_opinion_modifier = {{ target = ROOT modifier = medium_increase }} }}",
               "USA = { add_opinion_modifier = { target = ROOT modifier = small_decrease } }", v("cwger_westbindung", -2), faction("bdi", 4)), ai=10)

# ===================================================================== FOREIGN
FO = C("foreign_policy", "Germany in the World",
       "Party foundations and development aid make the Federal Republic a power without an army abroad. Campaigns use Imperia §YPublic Political Support§!, aid uses Imperia §Yassistance programmes§!.",
       "GFX_decision_category_generic_political_actions", GER_VIS, priority=170)
for tag, name, slot, fname in [("POR", "Portugal", 3, "Friedrich Ebert"), ("SPR", "Spain", 3, "Friedrich Ebert"),
                               ("GRE", "Greece", 3, "Friedrich Ebert"), ("CHL", "Chile", 1, "Konrad Adenauer"), ("NIC", "Nicaragua", 1, "Konrad Adenauer")]:
    D(FO, f"foundation_{tag.lower()}", f"{fname} Foundation in {name}",
      f"Money, seminars and printing presses for the sister party in {name}.",
      "GFX_decision_propaganda", visible=f"has_country_flag = {P}_foundations_unlocked country_exists = {tag}",
      available=f"{tag} = {{ has_country_flag = mdcw_cw_initialized }}", cost=50, re_enable=730,
      effect=J(f"set_temp_variable = {{ cwger_t_party = {slot} }}", f"{tag} = {{ ROOT = {{ {P}_start_foundation_campaign = yes }} }}",
               tt(f"{P}_tt_foundation_{slot}", f"Starts Imperia §YPublic Political Support§! for party slot {slot} ({'social democrats' if slot == 3 else 'Christian democrats'}).")), ai=10)
DEV_TARGETS = ["TUR", "EGY", "IND", "PAK", "BRA", "TNZ", "KEN", "NIG", "SEN", "JOR", "TUN", "MOR", "PHI", "COL", "PER", "BOT", "ZAM", "ETH", "SUD", "POR", "GRE"]
for prog, pname, icon in [(1, "Construction Assistance", "GFX_decision_generic_factory"), (2, "Technical Mission", "GFX_decision_attract_foreign_investor"),
                          (4, "Productivity Mission", "GFX_decision_steel")]:
    D(FO, f"dev_programme_{prog}", f"Development Partnership: {pname}",
      f"Start a medium-sized German {pname.lower()} programme in a partner country (an Imperia assistance programme).",
      icon, visible=f"OR = {{ has_idea = {P}_idea_bmz has_idea = {P}_idea_development_partner }}", cost=40, re_enable=180,
      targets=DEV_TARGETS, target_trigger="NOT = { has_war_with = ROOT } has_country_flag = mdcw_cw_initialized NOT = { check_variable = { mdcw_cw_alignment = 2 } }",
      effect=J(f"set_temp_variable = {{ cwger_t_prog = {prog} }}", "set_temp_variable = { cwger_t_size = 2 }",
               f"FROM = {{ ROOT = {{ {P}_start_programme = yes }} }}",
               tt(f"{P}_tt_dev_{prog}", f"Starts an Imperia §Y{pname}§! programme if assistance capacity allows; otherwise the political power is refunded.")), ai=8)

# ===================================================================== GDR (for an East German player)
DR = C("ddr_state", "The Workers' and Peasants' State",
       ddr_meters().replace("DDR.", ""), "GFX_decision_category_coms_cat", f"{DDR_VIS} has_country_flag = {P}_ddr_initialized",
       tag="DDR", priority=200)
D(DR, "ddr_intershop", "Expand the Intershops",
  "Western goods for Western money: let citizens with D-Marks from relatives shop in special stores.",
  "GFX_decision_money_dec", visible="always = yes", cost=40, re_enable=365,
  effect=J(dv_self("cwddr_hard_currency", -4), dv_self("cwddr_west_media", 2), dv_self("cwddr_opposition", 1)), ai=15)
D(DR, "ddr_koko", "Commercial Coordination",
  "Schalck-Golodkowski's empire: arms trading, art sales, waste imports - anything for hard currency.",
  "GFX_decision_negotiate_icon", visible="always = yes", cost=50, re_enable=540,
  effect=J(dv_self("cwddr_hard_currency", -6), dv_self("cwddr_west_dependency", 3)), ai=15)
D(DR, "ddr_border_regime", "Tighten the Border Regime",
  "More mines, more dogs, more watchtowers - and an order to shoot.",
  "GFX_decision_break_treaty", visible="always = yes", available="check_variable = { cwddr_wende_stage < 3 }", cost=50, re_enable=365,
  effect=J(dv_self("cwddr_exit_pressure", -5), dv_self("cwddr_sed_control", 3), dv_self("cwddr_recognition", -4)), ai=15)
D(DR, "ddr_stasi_sweep", "Operation Against the Groups",
  "The Ministry for State Security infiltrates and decomposes ('Zersetzung') the peace and environment groups.",
  "GFX_decision_generic_intelligence_operation", visible="always = yes", cost=50, re_enable=365,
  effect=J(dv_self("cwddr_opposition", -5), dv_self("cwddr_sed_control", 2), dv_self("cwddr_west_media", 1)), ai=15)
D(DR, "ddr_consumer_imports", "Import Consumer Goods",
  "Jeans, coffee and VW Golfs bought in the West to quiet the people - on credit.",
  "GFX_decision_attract_foreign_investor", visible="always = yes", cost=30, re_enable=365,
  effect=J(dv_self("cwddr_exit_pressure", -3), dv_self("cwddr_hard_currency", 5), "add_stability = 0.02"), ai=10)
D(DR, "ddr_reform_course", "A Socialist Glasnost",
  "Follow Moscow's new course: open the press a little, let the dissidents speak.",
  "GFX_decision_propaganda", visible="date > 1985.1.1", available="check_variable = { cwddr_moscow_backing < 60 }", cost=75, once=True,
  effect=J(dv_self("cwddr_opposition", 3), dv_self("cwddr_sed_control", -6), dv_self("cwddr_exit_pressure", -6), dv_self("cwddr_west_media", 3)), ai=5)


# ===================================================================== GDR: policy towards Bonn (multiplayer)
# A human East Berlin plays the inner-German rivalry through these decisions and the events COLDWAR_GGR.200-230.
# All state lives on GER (cwgg_*); an AI GDR is run by the rivalry's own AI instead.
from rivalry import R as _R, EVR as _EVR, kl as _kl, dr as _dr, lever as _lever, log as _log


def _ger(*parts):
    return "GER = {\n" + fmt(J(*parts, f"{_R}_gui_refresh = yes"), 1) + "\n}"


_INIT2 = "GER = { check_variable = { cwgg_init_ddr > 1 } }"
WP = C("ddr_westpolitik", "Policy Towards Bonn",
       "The other German state: crises, pressure, money and the border.\n\n"
       "Climate: §Y[?GER.cwgg_klima|0]§! | escalation pressure: §Y[?GER.cwgg_druck|0]§! | our initiative: §Y[?GER.cwgg_init_ddr|0]§!\n"
       "Bundeswehr alert level: §Y[?GER.cwgg_mob_brd|0]§! | NVA alert level: §Y[?GER.cwgg_mob_ddr|0]§!\n"
       "Crisis intensity: §Y[?GER.cwgg_krise_int|0]§! (0 = no crisis) | treaties signed: see the events of the Federal Republic.",
       "GFX_decision_category_coms_cat",
       f"{DDR_VIS} is_ai = no country_exists = GER GER = {{ has_country_flag = cwgg_initialized }} NOT = {{ has_global_flag = {P}_unity_achieved }}",
       tag="DDR", priority=210)
D(WP, "ddr_crisis_course", "Set Our Course in the Crisis",
  "Decide how East Berlin answers in the next round of the crisis. Rounds are resolved every six months.",
  "GFX_decision_negotiate_icon",
  visible="GER = { check_variable = { cwgg_krise_typ > 0 } }", available="GER = { check_variable = { cwgg_countdown = 0 } }",
  cost=0, re_enable=30, effect=f"country_event = {{ id = {_EVR}.200 }}", ai=0)
_ALERT_UP = ("GER = { OR = { AND = { check_variable = { cwgg_mob_ddr = 0 } check_variable = { cwgg_stufe > 2 } } "
             "AND = { check_variable = { cwgg_mob_ddr = 1 } check_variable = { cwgg_stufe > 3 } } "
             "AND = { check_variable = { cwgg_mob_ddr = 2 } OR = { check_variable = { cwgg_stufe > 4 } check_variable = { cwgg_countdown > 0 } check_variable = { cwgg_mob_brd > 2 } } } } }")
D(WP, "ddr_nva_alert_up", "Raise the NVA Alert Level",
  "Put the National People's Army on a higher state of readiness. Each level speeds up mobilisation and hardens war support: "
  "level 1 §G+10%§! / §G+2%§!, level 2 §G+25%§! / §G+5%§!, level 3 §G+50%§! / §G+10%§!. Needs the escalation ladder at §YCrisis§! (level 1), §YConfrontation§! (2), or §YWar Danger§!, a countdown or a fully alerted Bundeswehr (3).",
  "GFX_decision_generic_military", visible="GER = { check_variable = { cwgg_mob_ddr < 3 } }", available=_ALERT_UP,
  cost=0, re_enable=30,
  effect=J(_ger("add_to_variable = { cwgg_mob_ddr = 1 }", _dr(5, False), f"{_R}_set_stage_modifiers = yes",
                _log("ddr_alert", "The National People's Army raises its alert level.")),
           "add_stability = -0.01",
           tt(f"{P}_tt_nva_up", "NVA alert level §R+1§!, escalation pressure §R+5§!.")), ai=0)
D(WP, "ddr_nva_alert_down", "Lower the NVA Alert Level",
  "Stand the National People's Army down by one level.",
  "GFX_decision_generic_military", visible="GER = { check_variable = { cwgg_mob_ddr > 0 } }", cost=0, re_enable=30,
  effect=J(_ger("add_to_variable = { cwgg_mob_ddr = -1 }", _kl(2, False), f"{_R}_set_stage_modifiers = yes",
                _log("ddr_alert_down", "The National People's Army lowers its alert level.")),
           tt(f"{P}_tt_nva_down", "NVA alert level §G-1§!, climate §G+2§!.")), ai=0)
D(WP, "ddr_raise_exchange", "Raise the Compulsory Exchange",
  "Every Western visitor must change more D-Marks a day. Fewer visits, more hard currency.",
  "GFX_decision_money_dec", visible="always = yes", available=_INIT2 + " GER = { check_variable = { cwgg_dhebel_zwang < 3 } }", cost=25, re_enable=365,
  effect=J(_ger("add_to_variable = { cwgg_init_ddr = -2 }", _lever("zwang", 1, ddr=True, show=False), _kl(-6, False),
                f"country_event = {{ id = {_EVR}.121 days = 1 }}"),
           dv_self("cwddr_hard_currency", -3), dv_self("cwddr_exit_pressure", 1),
           tt(f"{P}_tt_ddr_zwang", "Costs §Y2§! initiative. Our lever §YCompulsory Exchange§! §G+1§!, climate §R-6§!.")), ai=0)
D(WP, "ddr_transit_checks", "Harass the Transit Routes",
  "Hours of checks at Helmstedt and Dreilinden. West Berlin should remember whose territory it lies in.",
  "GFX_decision_break_treaty", visible="always = yes", available=_INIT2 + " GER = { check_variable = { cwgg_dhebel_transit > 0 } }", cost=25, re_enable=180,
  effect=J(_ger("add_to_variable = { cwgg_init_ddr = -2 }", _kl(-5, False), _dr(12, False),
                "add_to_variable = { cwger_berlin_access = -5 } clamp_variable = { var = cwger_berlin_access min = 0 max = 100 }",
                _log("ddr_transit", "Hours of checks on the transit autobahn to Berlin.")),
           tt(f"{P}_tt_ddr_transit", "Costs §Y2§! initiative. Climate §R-5§!, escalation pressure §R+12§!, West Berlin's access §R-5§!.")), ai=0)
D(WP, "ddr_tighten_border", "Strengthen the Border Installations",
  "New fences, mines and SM-70 spring guns along the state border.",
  "GFX_decision_break_treaty", visible="always = yes", available=_INIT2 + " GER = { check_variable = { cwgg_dhebel_grenze < 3 } } check_variable = { cwddr_wende_stage < 3 }", cost=25, re_enable=365,
  effect=J(_ger("add_to_variable = { cwgg_init_ddr = -2 }", _lever("grenze", 1, ddr=True, show=False), _dr(8, False),
                f"country_event = {{ id = {_EVR}.122 days = 1 }}"),
           dv_self("cwddr_exit_pressure", -3),
           tt(f"{P}_tt_ddr_grenze", "Costs §Y2§! initiative. Our lever §YBorder Regime§! §G+1§!, escalation pressure §R+8§!.")), ai=0)
D(WP, "ddr_hva_offensive", "HVA Offensive in Bonn",
  "Markus Wolf's Main Directorate for Reconnaissance sends more agents, more Romeos and more money west.",
  "GFX_decision_generic_intelligence_operation", visible="always = yes", available=_INIT2, cost=25, re_enable=180,
  effect=J(_ger("add_to_variable = { cwgg_init_ddr = -2 }", "add_to_variable = { cwger_stasi_penetration = 5 }",
                "clamp_variable = { var = cwger_stasi_penetration min = 0 max = 100 }"),
           tt(f"{P}_tt_ddr_hva", "Costs §Y2§! initiative. Stasi penetration of Bonn §R+5§!.")), ai=0)
D(WP, "ddr_recognition_drive", "Win Another Recognition",
  "Credits, advisers and solidarity: persuade another state in the Third World to recognise the GDR.",
  "GFX_decision_hol_draw_up_staff_plans", visible="GER = { NOT = { check_variable = { cwgg_vertrag_3 = 1 } } }",
  available=_INIT2 + " check_variable = { cwddr_recognition < 80 }", cost=50, re_enable=365,
  effect=J(_ger("add_to_variable = { cwgg_init_ddr = -2 }", _kl(-3, False),
                _log("ddr_recog", "Another state in the Third World recognises the GDR."),
                f"if = {{ limit = {{ check_variable = {{ cwgg_hebel_recht > 1 }} }} set_temp_variable = {{ cwgg_t_typ = 5 }} {_R}_start_crisis = yes }}"),
           dv_self("cwddr_recognition", 4),
           tt(f"{P}_tt_ddr_recog", "Costs §Y2§! initiative. Our recognition §G+4§!, climate §R-3§!. While Bonn still insists on its legal position, this starts a §YRecognition Crisis§!.")), ai=0)
D(WP, "ddr_goodwill", "A Gesture of Goodwill",
  "Lower the compulsory exchange for pensioners, dismantle a stretch of spring guns - and let the diplomats talk about it.",
  "GFX_decision_negotiate_icon", visible="always = yes", available=_INIT2, cost=25, re_enable=180,
  effect=J(_ger("add_to_variable = { cwgg_init_ddr = -2 }", _kl(6, False),
                "if = { limit = { check_variable = { cwgg_dhebel_grenze > 0 } } add_to_variable = { cwgg_dhebel_grenze = -1 } }",
                "if = { limit = { check_variable = { cwgg_dhebel_zwang > 0 } } add_to_variable = { cwgg_dhebel_zwang = -1 } }",
                f"country_event = {{ id = {_EVR}.123 days = 1 }}"),
           tt(f"{P}_tt_ddr_goodwill", "Costs §Y2§! initiative. Climate §G+6§!; our levers §YBorder Regime§! and §YCompulsory Exchange§! §R-1§!.")), ai=0)
D(WP, "ddr_ask_credit", "Ask Bonn for a Credit",
  "Through Schalck-Golodkowski, let Bonn know that the Republic's hard-currency position is 'tight'. Bonn decides.",
  "GFX_decision_money_dec", visible="always = yes", available="check_variable = { cwddr_hard_currency > 40 }", cost=25, re_enable=720,
  effect=J(f"GER = {{ country_event = {{ id = {_EVR}.60 days = 1 }} }}", tt(f"{P}_tt_ddr_credit", "The Federal Government decides whether to grant a credit.")), ai=0)
D(WP, "ddr_close_transit", "Close the Access Routes",
  "Close the transit routes to West Berlin 'for repairs'. A crisis is the point.",
  "GFX_decision_break_treaty", visible="always = yes",
  available="GER = { check_variable = { cwgg_krise_typ = 0 } check_variable = { cwgg_init_ddr > 2 } check_variable = { cwgg_dhebel_transit > 1 } NOT = { has_country_flag = cwgg_crisis_cd } }",
  cost=50, re_enable=730,
  effect=J(_ger("add_to_variable = { cwgg_init_ddr = -3 }", "set_temp_variable = { cwgg_t_typ = 1 }", f"{_R}_start_crisis = yes"),
           tt(f"{P}_tt_ddr_close", "Costs §Y3§! initiative. Starts a §RTransit Crisis§! with the Federal Republic.")), ai=0)


def categories_file():
    out = ["## Generated by tools/west_germany_1970/compile.py. Edit the generator, not this file.\n"]
    for cid, (icon, vis, tag, prio) in CATS.items():
        out.append(f"{cid} = {{\n\ticon = {icon}\n\tpriority = {prio}\n\tallowed = {{ original_tag = {tag} }}\n\tvisible = {{ {vis} }}\n}}\n")
    return "\n".join(out)


def decisions_file():
    out = ["## Generated by tools/west_germany_1970/compile.py. Edit the generator, not this file.\n"]
    for cid, items in DECISIONS.items():
        out.append(f"{cid} = {{")
        out.extend(items)
        out.append("}\n")
    return "\n".join(out)
