# IMPERIA CW — Cold War: Soviet Union 1970 content generator.
# COLDWAR | Hand-written code for the free-text design lines (notes and `custom` effects).
import re
from cw_common import *

INFO = re.compile(r"gegenseitig exklusiv|Gegenseitig exklusiv|^Zwei Antworten|^Drei Wege|^Richtungswahl|Weiche|^Wer |^Welche|"
                  r"^Welcher|^Damanski|^Alt-Hist|^Nachfolge|^Gretschko stirbt|^Breschnew ist zum Start|^Bei Mehrheit|^Ohne Mehrheit|"
                  r"^Öffnet „The Ninth|^„Plan der Effizienz|^Wird automatisch erfüllt|^Antwortet auf Ägyptens")
LEAN = {"reformerisch": -1, "neutral": 0, "orthodox": 1}


def tt(key, text):
    LOC[f"{PFX}{key}_tt"] = text
    return f"custom_effect_tooltip = {PFX}{key}_tt"


def clergy(op):
    return [f"if = {{ limit = {{ NOT = {{ has_idea = the_clergy }} }}", "add_ideas = the_clergy", f"set_variable = {{ the_clergy_opinion = {op} }}",
            "hidden_effect = { initialize_internal_faction_dynamic_modifiers = yes }", "}",
            tt("clergy_faction", "The §YMoscow Patriarchate§! becomes an internal faction.")]


def republic_offer(kind, tags=None):
    """the Soviet republics receive an offer; each (player or AI) decides itself"""
    lim = "" if not tags else "OR = { " + " ".join(f"original_tag = {t}" for t in tags) + " }"
    texts = {"independence": "Every Union republic is offered §Yindependence§!. Each republic decides for itself.",
             "secession": "The Union republics are offered the §Yright to secede§!. Each republic decides for itself.",
             "treaty": "Every Union republic is offered the §YNew Union Treaty§!: more autonomy, no one is forced to leave.",
             "release": "The Baltic, Caucasian and Central Asian republics are offered §Yindependence§!. Each decides for itself."}
    ev = {"independence": 60, "secession": 60, "treaty": 61, "release": 60}[kind]
    return [tt(f"republic_offer_{kind}", texts[kind]), "hidden_effect = {",
            f"every_subject_country = {{ limit = {{ {PFX}is_union_republic = yes {lim} }} country_event = {{ id = {NS}.{ev} days = 2 }} }}", "}"]


MANUAL = {
    ("the_collective_leadership", "Aktiviert die fünf"):
        [f"add_dynamic_modifier = {{ modifier = {PFX}{g}_modifier }}" for g in ("party_state", "gosplan", "armed_forces", "union", "commonwealth")],
    ("steel_cities", "Ressource: +8 Stahl"):
        ["675 = { add_resource = { type = steel amount = 8 } }"],
    ("samotlor", "Ressource: +10 Öl"):
        ["678 = { add_resource = { type = oil amount = 10 } }"],
    ("the_tyumen_complex", "Ressource: +8 Öl"):
        ["679 = { add_resource = { type = oil amount = 8 } }"],
    ("the_tenth_five_year_plan", "„Plan der Effizienz"):
        [tt("tenth_plan", "The §YTenth Five-Year Plan§! (1976-1980), the 'plan of efficiency and quality', opens a new priority choice in §YFive-Year Plans§!.")],
    ("bam_open_to_traffic", "Bonus für „The Chinese Question“"):
        [tt("bam_supply", "Supply in the Far East improves for the §YChinese Question§!.")],
    ("the_karabakh_petitions", "Status quo"):
        [f"country_event = {{ id = {NS}.40 days = 1 }}"],
    ("accord_with_the_patriarchate", "Fügt die Fraktion"): clergy(45),
    ("nts_the_solidarists_return", "Fügt die Fraktion"): clergy(60),
    ("lnl_live_not_by_lies", "Fügt die Fraktion"): clergy(65),
    ("rp_orthodox_nationalism", "Fügt die Fraktion"): clergy(60),
    ("rom_the_church_and_the_crown", "Fügt die Fraktion"): clergy(75),
    ("rd_the_directors_take_over", "Fügt die Fraktion"):
        ["if = { limit = { NOT = { has_idea = oligarchs } }", "add_ideas = oligarchs", "set_variable = { oligarchs_opinion = 70 }",
         "hidden_effect = { initialize_internal_faction_dynamic_modifiers = yes }", "}",
         tt("oligarch_faction", "The §Yshadow economy§! becomes an internal faction.")],
    ("the_amur_fortified_districts", "Bunker in zwei Grenzstaaten"):
        sum(([f"if = {{ limit = {{ {s} = {{ is_owned_and_controlled_by = ROOT }} }}",
              f"{s} = {{ add_building_construction = {{ type = bunker level = 2 instant_build = yes province = {{ all_provinces = yes limit_to_border = yes }} }} }}",
              f"set_temp_variable = {{ {PFX}gdp_share = 0.002 }}", f"{PFX}pay_gdp_share = yes", "}"] for s in (692, 687)), []) +
        [tt("amur_bunkers", "Bunkers along the border of §YPrimorye§! and §YKhabarovsk§!, each paid with §R0.2%§! of GDP.")],
    ("plan_lop_nur", "Kriegsziel gegen CHI"):
        ["if = { limit = { country_exists = CHI NOT = { has_war_with = CHI } } create_wargoal = { type = topple_government target = CHI } }",
         tt("lop_nur_wargoal", "We gain a wargoal against §YChina§!. Whether to strike remains our decision.")],
    ("the_eastern_front_secured", "Mit „BAM Open to Traffic“"):
        [f"if = {{ limit = {{ has_country_flag = {PFX}bam_open }}", f"custom_effect_tooltip = {{ localization_key = modifies_dynamic_modifier_tt MODIFIER = {PFX}armed_forces_modifier }}",
         f"add_to_variable = {{ {PFX}armed_forces_supply_consumption_factor = -0.02 tooltip = {mod_tt_key('supply_consumption_factor')} }}", "hidden_effect = { force_update_dynamic_modifier = yes }", "}"],
    ("the_comprehensive_programme", "Cold War: Decision"):
        [tt("comprehensive_programme", "The Cold War decision §YComecon Integration Programme§! refunds §G25§! of its political power cost.")],
    ("world_market_prices", "Meinung −10 bei allen RGW-Partnern"):
        [f"every_country = {{ limit = {{ OR = {{ tag = DDR tag = POL tag = CZE tag = HUN tag = ROM tag = BUL }} }} add_opinion_modifier = {{ target = ROOT modifier = {PFX}world_market_prices }} }}",
         tt("world_market_prices", "Every Comecon partner (§YDDR, Poland, Czechoslovakia, Hungary, Romania, Bulgaria§!) thinks less of us (§R-10§!).")],
    ("na_dissolve_the_pact", "Löst unsere Fraktion auf"):
        ["every_country = { limit = { is_in_faction_with = ROOT NOT = { tag = ROOT } } country_event = { id = COLDWAR_SOV.41 days = 1 } }",
         "dismantle_faction = yes"],
    ("nt_the_imperial_question", "Im Event"):
        [f"country_event = {{ id = {NS}.42 days = 1 }}"],
    ("bre_balance_the_troika", "Politbüro-Balance 0,10 Richtung Mitte"):
        [f"{PFX}bop_toward_centre_10 = yes"],
    ("pod_a_federal_union", "Politbüro der Republiken"): [f"set_country_flag = {PFX}federal_union",
        tt("federal_union", "In the Politburo the republican seats count §Ytwice§! on Union questions (language, Union treaty, proposals of the republics).")],
    ("pod_the_treaty_signer", "Freundschaftsverträge"): [f"set_country_flag = {PFX}treaty_signer",
        tt("treaty_signer", "The friendship treaties with §YEgypt§!, §YIraq§! and §YIndia§! each refund §G25§! political power.")],
    ("trust_the_local_barons", "Politbüro der Republiken"): [f"set_country_flag = {PFX}local_barons",
        tt("local_barons", "Politburo seats can only change at a §YParty Congress§! (no extraordinary plenum). Kompromat chance §G-10%§!.")],
    ("rotate_the_cadres", "Politbüro der Republiken"): [f"set_country_flag = {PFX}rotate_cadres",
        tt("rotate_cadres", "At every §YParty Congress§! at least one republican seat must change hands.")],
    ("she_purge_the_brezhnevites", "Politbüro der Republiken"): [f"set_country_flag = {PFX}free_dismissal",
        tt("free_dismissal", "Once, we may remove a republican seat holder without the cost of an extraordinary plenum.")],
    ("and_the_discipline_campaign", "Politbüro der Republiken"): [f"set_country_flag = {PFX}discipline_campaign",
        tt("discipline_campaign", "Kompromat chance §G+20%§!. The §YKGB§! may investigate a seat holder without an accuser (50 PP).")],
    ("and_the_cotton_affair_exposed", "Politbüro der Republiken"):
        [f"every_subject_country = {{ limit = {{ has_country_flag = {PFX}pripiski }} {PFX}investigate_republic = yes }}",
         tt("cotton_affair_all", "Every republic that has falsified its plan reports (§Ypripiski§!) is investigated at once.")],
    ("gro_iron_discipline", "Politbüro der Republiken"): [f"set_country_flag = {PFX}iron_discipline",
        tt("iron_discipline", "A republic that falsifies its plan report loses §R3%§! stability.")],
    ("gor_the_presidency", "Politbüro der Republiken"): [f"{PFX}federation_council = yes"],
    ("and_a_way_out_of_afghanistan", "Wenn „The Afghan Burden“"):
        [f"if = {{ limit = {{ has_idea = {PFX}afghan_burden }} {PFX}withdraw_from_afghanistan = yes }}",
         tt("afghan_withdrawal", "If §YThe Afghan Burden§! is active, we offer the Afghan government a plan for our withdrawal.")],
    ("gor_leave_afghanistan", "Beendet „The Afghan Burden“"):
        [f"if = {{ limit = {{ has_idea = {PFX}afghan_burden }} {PFX}withdraw_from_afghanistan = yes }}",
         tt("afghan_withdrawal_gor", "§YThe Afghan Burden§! ends; the Afghan government receives our withdrawal plan.")],
    ("nts_a_russian_federation", "Jede Republik erhält"): republic_offer("independence"),
    ("chr_the_right_of_secession", "Republiken erhalten"): republic_offer("secession"),
    ("lnl_release_the_republics", "Baltikum, Kaukasus"): republic_offer("release", ["EST", "LAT", "LIT", "ARM", "AZE", "GEO", "KAZ", "KYR", "TAJ", "TRK", "UZB"]),
    ("usr_the_new_union_treaty", "Jede Unionsrepublik"): republic_offer("treaty"),
    ("fob_the_rbmk_question", "Entfernt das RBMK"): [f"clr_country_flag = {PFX}rbmk"],
    ("the_harvest_of_1972", "Dürre und Frost"): [f"set_country_flag = {{ flag = {PFX}poor_harvest days = 365 }}",
        tt("harvest_1972", "Drought and frost: the grain harvest falls §R13%§! short of the plan.")],
}


def manual(f, e):
    sid = short(f["id"])
    t = e["t"]
    for (fid, start), code in MANUAL.items():
        if fid == sid and t.startswith(start):
            return list(code)
    m = re.match(r"^Politbüro-Beschluss \((\w+)\)", t)
    if m:
        from cw_effects import R
        R.resolutions[sid] = LEAN[m.group(1)]
        LOC[f"{PFX}resolution_tt"] = ("§YPolitburo resolution:§! the Politburo votes on this decision 10 days from now. "
                                    "A majority gives a §Gmandate§! (+25 political power, +2% stability); without one, Moscow carries "
                                    "§RDefying the Politburo§! and Union cohesion falls by 2.")
        return [f"custom_effect_tooltip = {PFX}resolution_tt", f"set_temp_variable = {{ {PFX}queue_subject = {RES_INDEX[sid]} }}",
                f"{PFX}queue_resolution = yes"]
    if INFO.search(t):
        return []
    raise KeyError((sid, t))


RES_INDEX = {}
