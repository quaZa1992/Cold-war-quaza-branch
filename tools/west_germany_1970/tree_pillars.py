# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""Focus content of the West Germany 1970 tree (see tree.py for the conventions)."""
from cw_lib import *
from tree import (F, ost_face, ROOT_KEY, core, unlock, state_build, state_mod, rail, infl, opinion, swap, remove_idea,
                  climate_base, sec_slots, bka, gsg9, gamevar)
from rivalry import kl, lever, channel_unlock, bop

SPD = "check_variable = { ruling_party = 3 }"
UNION = "check_variable = { ruling_party = 1 }"
NOT_UNION = "NOT = { check_variable = { ruling_party = 1 } }"
FDP_GOV = "is_in_array = { gov_coalition_array = 2 }"
from roster import requirement
GREEN_GOV = 'AND = { ' + requirement('greens') + ' OR = { check_variable = { ruling_party = 17 } is_in_array = { gov_coalition_array = 17 } } }'
ERA2 = f"OR = {{ date > 1981.12.31 has_country_flag = {P}_era2 }}"
WALL = f"has_global_flag = {P}_wall_open"
UNITY = f"has_global_flag = {P}_unity_achieved"
NO_UNITY = f"NOT = {{ has_global_flag = {P}_unity_achieved }}"
DDR_EX = "country_exists = DDR"
OPEN_OR_UNITY = f"OR = {{ {WALL} {UNITY} date > 1990.12.31 }}"

# states (MD map)
SH, NDS, NRW, RLP, HES, BW, BAY, FRK, KB, SAAR, HH, WB = 37, 38, 39, 40, 41, 42, 43, 964, 966, 967, 1080, 1251
EAST = [44, 45, 539, 545, 972, 1079]
# provinces of the main cities
P_HANNOVER, P_NUERNBERG, P_STUTTGART, P_FRANKFURT, P_KOELN, P_HAMBURG, P_MUENCHEN, P_BERLIN = 3326, 11544, 9517, 6488, 3547, 9347, 11653, 16536

# AI: the historical path unless a path flag says otherwise
AI_NO_WAR = "modifier = { factor = 0 is_ai = yes }"


def set_flag_era2():
    return f"set_country_flag = {P}_era2"


# =================================================================== ROOT
F(ROOT_KEY, None, 46, 0, cost=1, pillar="root", icon="chancellor", name="The Government Statement",
  desc="28 October 1969. Willy Brandt promises to 'dare more democracy', to seek a regulated coexistence with the other German state and to keep the Federal Republic firmly in the West. The coalition of SPD and FDP holds twelve seats more than the opposition. Everything else is still open.",
  reward=J(core("bonn", stab=0.02, pp=0.05), core("west", trade=0.05), pp(50),
           tt(f"{P}_tt_root", "Opens the eight pillars of the tree. Inner-German relations and internal security are run from their own windows on the top bar.")))

# =================================================================== I. THE CHANCELLERY
F("chancellery", ROOT_KEY, -39, 1, cost=1, icon="parliament", name="The Chancellery",
  desc="Horst Ehmke turns the Palais Schaumburg into a modern planning staff: computers, planning cells, a chief of staff who knows every file. The chancellor governs - if the coalition lets him.",
  reward=J(core("bonn", pp=0.05, bureau=-0.05), "add_political_power = 25"))
F("situation_centre", "chancellery", 0, 1, cost=2, icon="secret_meeting", name="The Situation Centre",
  desc="A room in the chancellery where the strands come together: BND reports, the Permanent Representation's cables, the crisis staff's telephones.",
  reward=J(unlock("cwgg_init_bonus", "a chance of §G+1§! initiative per month in the inner-German relations window"), core("bonn", stab=0.01)))
# --- social-liberal reforms
F("mehr_demokratie_wagen", "chancellery", -4, 1, cost=3, avail=SPD,
  reward=J(core("bonn", drift=0.05, stab=0.01), v("cwger_rechtsstaat", 3), party("spd", 0.006)))
F("voting_age_18", "mehr_demokratie_wagen", -2, 1, cost=2,
  reward=J(party("spd", 0.008), party("fdp", 0.003), v("cwger_raf_milieu", -2), core("bonn", drift=0.03)))
F("bafoeg", "voting_age_18", 0, 1, cost=3, filt="FOCUS_FILTER_RESEARCH",
  reward=J(money_gdp(-0.002), f"add_ideas = {P}_idea_student_aid", state_build(NRW, "offices"), state_build(BAY, "offices"),
           core("modell", prod=0.01), faction("dgb", 5)))
F("works_constitution", "mehr_demokratie_wagen", 0, 1, cost=3,
  reward=J(faction("dgb", 10), faction("bdi", -6), party("spd", 0.006), core("modell", social=0.03, prod=0.01)))
F("family_law_reform", "mehr_demokratie_wagen", 2, 1, cost=2,
  reward=J(v("cwger_rechtsstaat", 3), party("fdp", 0.004), party("cdu", -0.004), core("bonn", drift=0.02)))
F("pension_reform", "works_constitution", 0, 1, cost=3,
  reward=J(money_gdp(-0.003), party("spd", 0.008), core("bonn", stab=0.02), core("modell", social=0.05), v("cwger_bundesbank", 4)))
F("codetermination", "pension_reform", 0, 1, cost=5, avail=f"{SPD} {FDP_GOV}", pre=[["pension_reform"], ["family_law_reform", "bafoeg"]],
  reward=J(f"add_ideas = {P}_idea_codetermination", faction("dgb", 12), faction("bdi", -8), v("cwger_fdp_course", -10),
           core("modell", prod=0.02), core("bonn", stab=0.02)))
F("modell_deutschland", "codetermination", 0, 1, cost=5, avail=SPD,
  reward=J(core("modell", fac=0.03, tax=0.02), faction("bdi", 6), v("cwger_bundesbank", -5), party("spd", 0.008), pp(50)))
F("kanalarbeiter", "modell_deutschland", -1, 1, cost=3, mutex=["juso_left"], avail=SPD,
  reward=J(v("cwger_westbindung", 5), v("cwger_fdp_course", -5), faction("bdi", 5), core("west", ideo=0.05), v("cwger_peace_movement", 4)))
F("juso_left", "modell_deutschland", 1, 1, cost=3, mutex=["kanalarbeiter"], avail=SPD, ai=3,
  reward=J(v("cwger_peace_movement", -6), v("cwger_fdp_course", 12), faction("dgb", 6), party("spd", 0.005), party("greens", -0.004), core("ost", stab=0.01)))
# --- the FDP
F("freiburg_theses", "chancellery", 1, 1, cost=2, mutex=["kiel_theses"], avail=FDP_GOV,
  reward=J(v("cwger_fdp_course", -20), party("fdp", 0.004), v("cwger_rechtsstaat", 2), core("bonn", drift=0.02)))
F("kiel_theses", "chancellery", 3, 1, cost=2, mutex=["freiburg_theses"], avail=FDP_GOV, ai=4,
  reward=J(v("cwger_fdp_course", 20), faction("bdi", 6), faction("mittelstand", 6), core("modell", tax=0.01)))
F("genscher_foreign_office", "freiburg_theses", 1, 1, cost=3, pre=[["freiburg_theses", "kiel_theses"]], avail=f"{FDP_GOV} date > 1974.5.15",
  reward=J(core("west", opinion=0.1, trade=0.05), v("cwger_ostpolitik", 4), party("fdp", 0.003), infl("FRA", 2), infl("USA", 1)))
F("baum_liberal_interior", "genscher_foreign_office", 0, 1, cost=3, avail=FDP_GOV,
  reward=J(v("cwger_rechtsstaat", 5), v("cwger_security", -3), v("cwger_raf_milieu", -3), core("wehrhaft", police=-0.05)))
# --- the Union
F("union_opposition", "chancellery", 5, 1, cost=2, avail=NOT_UNION,
  reward=J(party("cdu", 0.004), core("bonn", stab=-0.01), v("cwger_csu_autonomy", 3)))
F("so_nicht", "union_opposition", -1, 1, cost=3, mutex=["joint_resolution"],
  reward=J(v("cwger_ostpolitik", -6), party("cdu", 0.006), v("cwger_csu_autonomy", 5), bop(-0.1)))
F("joint_resolution", "union_opposition", 1, 1, cost=3, mutex=["so_nicht"],
  reward=J(v("cwger_ostpolitik", 4), party("cdu", 0.002), core("bonn", stab=0.02), bop(0.05)))
F("party_reform_cdu", "so_nicht", 1, 1, cost=3, pre=[["so_nicht", "joint_resolution"]],
  reward=J(party("cdu", 0.008), core("bonn", pp=0.03)))
F("change_1982", "party_reform_cdu", 0, 1, cost=3, icon="confidence", name="The Change of Government",
  desc="When the FDP's economic liberals have had enough of the SPD's debts, a constructive vote of no confidence can bring the CDU/CSU to power without an election - as it did on 1 October 1982.",
  avail=f"{SPD} {FDP_GOV} check_variable = {{ cwger_fdp_course > 30 }}",
  reward=J("country_event = { id = COLDWAR_GER.26 days = 1 }", tt(f"{P}_tt_change_1982", "The FDP debates the §YLambsdorff paper§! - and whether to change sides.")),
  ai=5)
F("spiritual_moral_turn", "change_1982", 0, 1, cost=3, avail=UNION, pre=[["change_1982", "party_reform_cdu"]],
  reward=J(party("cdu", 0.006), core("bonn", stab=0.02, pp=0.03), core("modell", social=-0.03), faction("mittelstand", 8), set_flag_era2()))
F("kohl_machine", "spiritual_moral_turn", -1, 1, cost=3, avail=UNION,
  reward=J(f"add_ideas = {P}_idea_kohl_system", core("bonn", pp=0.05, drift=0.03)))
F("consolidation_course", "spiritual_moral_turn", 1, 1, cost=5, avail=UNION,
  reward=J("set_temp_variable = { corp_change = -1 }", "modify_corporate_tax_rate_effect = yes", core("modell", tax=-0.01, social=-0.04, prod=0.02),
           faction("bdi", 8), faction("dgb", -6)))
F("pflegeversicherung", "consolidation_course", -1, 1, cost=3, pre=[["kohl_machine"], ["consolidation_course"]], avail=f"{UNION} {ERA2}",
  reward=J(core("modell", social=0.03), core("bonn", stab=0.03), faction("dgb", 6), party("cdu", 0.004)))
F("bitburg", "kohl_machine", -1, 1, cost=2, avail=f"{UNION} {ERA2}",
  reward=J(opinion("USA", "medium_increase"), v("cwger_westbindung", 3), party("rep", 0.002), core("west", ideo=0.03)))
F("csu_bavaria", "union_opposition", 2, 1, cost=3,
  reward=J(v("cwger_csu_autonomy", 6), state_mod(BAY, "bavarian_model"), state_build(BAY, "industrial_complex"), bop(-0.05)))
# --- the Greens
F("greens_parliament", "chancellery", 0, 8, cost=3, pre=[],
  avail=f"{requirement('greens')} has_country_flag = {P}_greens_founded check_variable = {{ cwger_parliament_shares^17 > 0.0499 }}",
  reward=J(core("energie", renew=0.05), core("bonn", drift=0.02), v("cwger_peace_movement", -4)))
F("realos", "greens_parliament", -1, 1, cost=3, mutex=["fundis"],
  reward=J(f"set_country_flag = {P}_greens_realo", party("greens", 0.004), core("bonn", stab=0.01)))
F("fundis", "greens_parliament", 1, 1, cost=3, mutex=["realos"], ai=2,
  reward=J(party("greens", -0.003), v("cwger_peace_movement", 6), v("cwger_anti_nuclear", 6)))
F("red_green_hesse", "realos", 0, 1, cost=3,
  reward=J(state_mod(HES, "red_green_land"), party("greens", 0.003), core("energie", renew=0.05)))
F("red_green_federal", "red_green_hesse", 0, 1, cost=5, avail=f"{SPD} {GREEN_GOV}",
  reward=J(f"add_ideas = {P}_idea_red_green_project", core("energie", renew=0.1, nuclear=-0.1), core("bonn", drift=0.05)))
F("lebenspartnerschaft", "red_green_federal", 0, 1, cost=3,
  reward=J(v("cwger_rechtsstaat", 5), core("bonn", drift=0.03), party("greens", 0.003), party("cdu", -0.002)))
# --- institutions
F("bundesrat_bargaining", "chancellery", 8, 1, cost=2,
  reward=J(unlock(f"{P}_mediation_unlocked", "the §YPackage Deal with the Länder§! decision against an opposition Bundesrat"), core("bonn", pp=0.02)))
F("federal_president", "bundesrat_bargaining", 0, 1, cost=2,
  reward=J(core("bonn", stab=0.02, drift=0.02)))
F("weizsaecker_speech", "federal_president", 0, 1, cost=3, avail=ERA2,
  reward=J(core("bonn", stab=0.02), core("west", opinion=0.05), opinion("ISR", "medium_increase"), opinion("POL", "medium_increase"), opinion("FRA", "small_increase")))
F("berlin_capital", "weizsaecker_speech", 0, 1, cost=5, avail=UNITY,
  reward=J(state_mod(45, "capital_berlin"), state_build(45, "offices", 2), state_build(KB, "offices"), money_gdp(-0.004),
           core("bonn", stab=0.03), tt(f"{P}_tt_capital", "Parliament and government move to Berlin; Bonn keeps ministries as a 'federal city'.")))
F("asylum_compromise", "weizsaecker_speech", 0, 5, cost=3, pre=[["weizsaecker_speech", "pflegeversicherung"]], avail=f"has_country_flag = {P}_asylum_surge",
  reward=J(f"if = {{ limit = {{ has_idea = {P}_idea_asylum_crisis }} remove_ideas = {P}_idea_asylum_crisis }}", v("cwger_terror_right", -6), party("rep", -0.004),
           party("cdu", 0.003), v("cwger_rechtsstaat", -2), protest(5)))
F("vergangenheitsbewaeltigung", "federal_president", 1, 1, cost=3,
  reward=J(core("west", opinion=0.05), opinion("ISR", "medium_increase"), v("cwger_terror_right", -3), core("bonn", drift=0.02)))
# --- governments that only some histories produce
F("barzel_cabinet", "chancellery", -7, 13, cost=2, pre=[], avail=f"has_country_flag = {P}_barzel_government",
  reward=J(core("bonn", stab=0.02), party("cdu", 0.004)))
F("barzel_west_first", "barzel_cabinet", 0, 1, cost=3,
  reward=J(v("cwger_westbindung", 6), core("west", trade=0.05), v("cwger_ostpolitik", -5), bop(-0.1)))
F("barzel_social_market", "barzel_west_first", 0, 1, cost=3,
  reward=J(core("modell", prod=0.02, social=-0.02), faction("bdi", 6)))
F("csu_nationwide", "chancellery", -5, 13, cost=2, pre=[], avail=f"has_country_flag = {P}_csu_fourth_party",
  reward=J(v("cwger_csu_autonomy", 10), party("cdu", -0.004)))
F("cdu_centre_course", "csu_nationwide", 0, 1, cost=3,
  reward=J(party("cdu", 0.004), core("bonn", drift=0.02)))
F("schmidt_minority", "chancellery", -3, 13, cost=2, pre=[], avail=f"has_country_flag = {P}_schmidt_iii",
  reward=J(core("bonn", pp=0.05), pp(50)))
F("schmidt_snap_election", "schmidt_minority", 0, 1, cost=2,
  reward="country_event = { id = COLDWAR_GER.23 days = 1 }")
F("strauss_model", "chancellery", 1, 13, cost=3, pre=[],
  avail=f"{UNION} check_variable = {{ cwger_cdu_leader = 3 }}",
  reward=J(f"add_timed_idea = {{ idea = {P}_idea_strauss_government days = 1460 }}", state_mod(BAY, "bavarian_model"), core("armee", equip=-0.05)))
F("strauss_aerospace", "strauss_model", -1, 1, cost=3,
  reward=J(state_build(BAY, "arms_factory"), state_build(HH, "industrial_complex"), tech("CAT_air_engines", 0.5, 1), core("modell", fac=0.01)))
F("strauss_east_credit", "strauss_model", 1, 1, cost=3, avail=DDR_EX,
  reward=J(channel_unlock("koko", True), f"set_country_flag = {P}_credit_unlocked", lever("devisen", 1), kl(5)))
F("spaeth_high_tech", "chancellery", 4, 13, cost=3, pre=[],
  avail=f"{UNION} check_variable = {{ cwger_cdu_leader = 5 }}",
  reward=J(state_build(BW, "offices"), state_mod(BW, "high_tech"), core("modell", prod=0.02), tech("CAT_computing", 0.5, 1)))
F("spaeth_slow_unity", "spaeth_high_tech", 0, 1, cost=3,
  reward=J(v("cwger_unity", -5), v("cwger_east_burden", -5), core("modell", tax=0.01)))
F("lafontaine_keynes", "chancellery", 6, 13, cost=3, pre=[],
  avail=f"{SPD} check_variable = {{ cwger_spd_leader = 5 }}",
  reward=J(state_mod(SAAR, "steel_rescue"), core("modell", social=0.03, cg=-0.02), faction("dgb", 10), debt_gdp(0.004)))
F("lafontaine_cautious_unity", "lafontaine_keynes", 0, 1, cost=3,
  reward=J(v("cwger_unity", -5), v("cwger_east_burden", -8), party("spd", -0.004)))
F("grand_coalition", "chancellery", 7, 6, cost=3, pre=[],
  avail=f"{UNION} is_in_array = {{ gov_coalition_array = 3 }}",
  reward=J(core("bonn", stab=0.04, drift=0.03), party("rep", 0.002), party("greens", 0.002)))


# =================================================================== II. MODELL DEUTSCHLAND
F("social_market", ROOT_KEY, -24, 1, cost=1, icon="market",
  reward=J(core("modell", prod=0.01, cg=-0.01), faction("bdi", 3), faction("dgb", 3)))
F("concerted_action", "social_market", -2, 1, cost=2,
  reward=J(faction("dgb", 6), faction("bdi", 6), core("modell", prod=0.01), v("cwger_bundesbank", -3)))
F("public_sector_strike", "concerted_action", -1, 1, cost=3, avail="date > 1973.10.1",
  reward=J(faction("dgb", 8), core("modell", social=0.03), v("cwger_bundesbank", 6), core("bonn", stab=-0.01)))
F("stimulus_1975", "public_sector_strike", -1, 1, cost=3, mutex=["austerity_1975"], pre=[["public_sector_strike", "concerted_action"]],
  reward=J(debt_gdp(0.006), core("modell", fac=0.02, build=0.05), faction("dgb", 6), v("cwger_bundesbank", 6)))
F("austerity_1975", "public_sector_strike", 1, 1, cost=3, mutex=["stimulus_1975"], pre=[["public_sector_strike", "concerted_action"]],
  reward=J(money_gdp(0.004), core("modell", social=-0.03, tax=0.01), faction("dgb", -6), faction("bdi", 6), v("cwger_bundesbank", -6)))
F("locomotive", "stimulus_1975", 1, 1, cost=3, pre=[["stimulus_1975", "austerity_1975"]], avail="date > 1977.6.1",
  reward=J(opinion("USA", "medium_increase"), core("modell", fac=0.02), debt_gdp(0.003), core("west", trade=0.05)))
F("bundesbank_independence", "social_market", 0, 1, cost=2,
  reward=J(f"add_ideas = {P}_idea_bundesbank_credibility", v("cwger_bundesbank", -10), core("modell", tax=0.01)))
F("end_bretton_woods", "bundesbank_independence", 0, 1, cost=3, avail="date > 1971.5.1",
  reward=J(swap("strong_dmark", "floating_dmark"), core("energie", fossil=-0.03), core("modell", prod=0.01)))
F("ems", "end_bretton_woods", 0, 1, cost=3, avail="date > 1978.1.1",
  reward=J(f"add_ideas = {P}_idea_ems", core("west", trade=0.05, europe=0.02), infl("FRA", 2), infl("ITA", 2)))
F("export_world_champion", "ems", -1, 2, cost=5, pre=[["locomotive"], ["ems"]],
  reward=J(swap("fading_miracle", "export_champion"), core("modell", fac=0.03), core("welt", market=0.05), state_build(HH, "dockyard"), state_build(NRW, "industrial_complex")))
F("working_time_385", "export_world_champion", -1, 1, cost=3, avail=ERA2,
  reward=J(f"add_ideas = {P}_idea_working_time_385", faction("dgb", 10), faction("bdi", -6), core("modell", prod=0.01)))
F("neue_heimat_cleanup", "working_time_385", 0, 1, cost=3,
  reward=J(corruption(False), faction("dgb", -6), core("bonn", stab=0.01)))
F("privatisation_wave", "export_world_champion", 1, 1, cost=3, avail=ERA2,
  reward=J(money_gdp(0.006), core("modell", prod=0.02, social=-0.02), faction("bdi", 8), faction("dgb", -6)))
F("postal_reform", "privatisation_wave", 0, 1, cost=3,
  reward=J(state_build(HES, "offices"), state_build(KB, "offices"), core("modell", prod=0.02), tech("CAT_information_technology", 0.5, 1)))
F("single_market", "neue_heimat_cleanup", 1, 1, cost=5, pre=[["neue_heimat_cleanup", "postal_reform"]],
  reward=J(f"add_ideas = {P}_idea_single_market", core("west", trade=0.1, europe=0.03), core("modell", fac=0.02)))
F("tax_reform_1990", "postal_reform", 1, 1, cost=3,
  reward=J("set_temp_variable = { pop_change = -2 }", "modify_population_tax_rate_effect = yes", core("bonn", stab=0.02), party("cdu", 0.003)))
F("monetary_union_offer", "single_market", -1, 1, cost=3, avail=f"{WALL} {DDR_EX} {NO_UNITY}",
  reward=J(v("cwger_unity", 10), dv("cwddr_exit_pressure", -10), dv("cwddr_west_dependency", 15),
           tt(f"{P}_tt_currency_dec", "§GUnlocks:§! the decisions on the §Yconversion rate§! for the currency union.")))
F("treuhand", "monetary_union_offer", 0, 1, cost=5, pre=[["monetary_union_offer", "single_market"]], avail=UNITY,
  reward=J(f"add_ideas = {P}_idea_treuhand", v("cwger_east_burden", -8), core("modell", prod=0.02), faction("dgb", -6)))
F("solidarity_pact", "treuhand", 0, 1, cost=3,
  reward=J(f"add_ideas = {P}_idea_soli", v("cwger_east_burden", -10), core("modell", tax=0.02)))
F("aufbau_ost", "solidarity_pact", 0, 1, cost=7,
  reward=J(*[f"if = {{ limit = {{ {s} = {{ is_owned_by = ROOT }} }} {state_build(s, 'infrastructure', 1, slot=False)} {state_build(s, 'industrial_complex')} }}" for s in (44, 545, 972, 1079, 539)],
           f"if = {{ limit = {{ 45 = {{ is_owned_by = ROOT }} }} {state_build(45, 'offices')} }}", rail(P_HANNOVER, P_BERLIN, 2),
           v("cwger_east_burden", -15), debt_gdp(0.01), core("modell", build=0.1)))
F("euro_founder", "single_market", 1, 1, cost=5, mutex=["dmark_bloc"], avail=OPEN_OR_UNITY,
  reward=J(f"add_ideas = {P}_idea_euro_founder", core("west", europe=0.05, trade=0.05), infl("FRA", 3), infl("ITA", 2), infl("HOL", 2)))
F("dmark_bloc", "single_market", 2, 1, cost=5, mutex=["euro_founder"], avail=OPEN_OR_UNITY, ai=2,
  reward=J(f"add_ideas = {P}_idea_dmark_bloc", core("modell", tax=0.02), core("west", europe=-0.05), infl("AUS", 3), infl("HOL", 3)))
F("agenda_reform", "euro_founder", 0, 2, cost=3, pre=[["euro_founder", "dmark_bloc", "treuhand"]],
  reward=J("set_temp_variable = { corp_change = -2 }", "modify_corporate_tax_rate_effect = yes", core("modell", prod=0.03, social=-0.03), faction("dgb", -8)))
F("petersberg_reform", "agenda_reform", 0, 1, cost=3, avail="date > 1996.1.1",
  reward=J("set_temp_variable = { corp_change = -2 }", "modify_corporate_tax_rate_effect = yes", core("modell", prod=0.02, tax=-0.01)))
# --- regions and research
F("steel_crisis", "social_market", 2, 4, cost=3, pre=[["stimulus_1975", "austerity_1975"]], avail="date > 1977.1.1",
  reward=J(state_mod(SAAR, "steel_rescue"), money_gdp(-0.002), faction("dgb", 6), core("modell", social=0.02)))
F("ruhr_structural_change", "steel_crisis", 0, 1, cost=5,
  reward=J(state_build(NRW, "offices"), state_build(NRW, "industrial_complex"), state_mod(NRW, "ruhr_change"), money_gdp(-0.003), core("modell", prod=0.02)))
F("shipyard_crisis", "ruhr_structural_change", 0, 1, cost=3, avail=ERA2,
  reward=J(state_build(HH, "industrial_complex"), state_build(SH, "dockyard"), money_gdp(-0.002), faction("dgb", 4)))
F("guest_worker_policy", "social_market", 3, 1, cost=3, mutex=["return_premium"], avail="date > 1973.6.1",
  reward=J(swap("guest_workers", "integration_policy"), core("modell", fac=0.01), party("rep", 0.002)))
F("return_premium", "social_market", 5, 1, cost=3, mutex=["guest_worker_policy"], avail="date > 1973.6.1", ai=3,
  reward=J(remove_idea("guest_workers"),
           "hidden_effect = { if = { limit = { is_ai = no } set_variable = { gw_ui_tab = 1 } clr_country_flag = gw_ui_show_abroad mdcw_gw_ledger_initialize = yes mdcw_gw_recount_ledger = yes mdcw_gw_refresh_dashboard = yes add_to_variable = { gw_ui_dirty = 1 } } }",
           tt(f"{P}_tt_return_premium_ministry", "Fund individual community return programmes through §YOverseas Labour§!. Residents leave only when their authorised programme is completed; public-service costs continue until departure."), core("modell", social=-0.02), party("rep", -0.002)))
F("research_policy", "guest_worker_policy", 1, 1, cost=3, pre=[["guest_worker_policy", "return_premium"]], filt="FOCUS_FILTER_RESEARCH",
  reward=J(core("west", research=0.03), state_build(BW, "offices"), tech("CAT_computing", 0.5, 1)))
F("airbus", "research_policy", 0, 1, cost=5, filt="FOCUS_FILTER_RESEARCH", icon="space",
  reward=J(state_build(HH, "industrial_complex"), state_build(BAY, "arms_factory"), infl("FRA", 2), opinion("FRA", "medium_increase"),
           tech("CAT_air_engines", 0.5, 1), core("west", research=0.02)))
F("microelectronics", "airbus", 0, 1, cost=3, avail=ERA2, filt="FOCUS_FILTER_RESEARCH",
  reward=J(state_build(BAY, "offices"), state_mod(BW, "high_tech"), tech("CAT_microchips", 0.5, 2), core("modell", prod=0.02)))
F("high_speed_rail", "microelectronics", 0, 1, cost=5, icon="bahn", name="The New Lines",
  desc="Hannover - Würzburg and Mannheim - Stuttgart: the first new railways built in Germany since the Empire, ready for the InterCity Express in 1991.",
  avail="date > 1985.1.1",
  reward=J(rail(P_HANNOVER, P_NUERNBERG, 2), rail(P_FRANKFURT, P_STUTTGART, 2), rail(P_KOELN, P_FRANKFURT, 1), money_gdp(-0.004), core("modell", build=0.05)))
F("vocational_training", "social_market", 6, 1, cost=2,
  reward=J(f"add_timed_idea = {{ idea = {P}_idea_dual_system days = 3650 }}", core("modell", prod=0.01), faction("dgb", 3), faction("mittelstand", 5)))
F("housing_programme", "vocational_training", 0, 1, cost=3,
  reward=J(money_gdp(-0.003), core("modell", build=0.05), core("bonn", stab=0.01), party("spd", 0.003)))

# =================================================================== III. ENERGY
F("energy_programme", ROOT_KEY, -12, 1, cost=1, icon="power_plant",
  reward=J(core("energie", gain=0.03), tt(f"{P}_tt_energy_mission", "Prepares the §YEnergy Security§! mission for the first oil shock.")))
F("kohlepfennig", "energy_programme", -2, 1, cost=3,
  reward=J(f"add_ideas = {P}_idea_kohlepfennig", state_build(NRW, "fossil_powerplant"), faction("dgb", 6), core("energie", fossil=0.03, gain=0.03)))
F("century_contract", "kohlepfennig", 0, 1, cost=3, avail="date > 1977.1.1",
  reward=J(state_build(NRW, "fossil_powerplant"), state_build(SAAR, "fossil_powerplant"), core("energie", gain=0.03), money_gdp(-0.002)))
F("waldsterben", "century_contract", 0, 1, cost=3, avail=ERA2,
  reward=J(f"add_ideas = {P}_idea_flue_gas_law", core("energie", fossil=-0.05), v("cwger_anti_nuclear", -3), party("greens", -0.002)))
F("nuclear_buildout", "energy_programme", 0, 1, cost=5,
  reward=J(f"add_ideas = {P}_idea_nuclear_buildout", state_build(HES, "nuclear_reactor"), state_build(BW, "nuclear_reactor"), core("energie", nuclear=0.1),
           v("cwger_anti_nuclear", 6), protest(4)))
F("fast_breeder", "nuclear_buildout", -1, 1, cost=5, mutex=["nuclear_moratorium"],
  reward=J(state_build(NRW, "nuclear_reactor"), state_build(BAY, "nuclear_reactor"), core("energie", nuclear=0.1, fossil=-0.05), v("cwger_anti_nuclear", 10), protest(8),
           tech("CAT_electronics", 0.25, 1)))
F("nuclear_moratorium", "nuclear_buildout", 1, 1, cost=3, mutex=["fast_breeder"], ai=3,
  reward=J(v("cwger_anti_nuclear", -10), core("energie", nuclear=-0.05, renew=0.05), party("greens", -0.003), party("spd", 0.002)))
F("chernobyl_response", "fast_breeder", 1, 1, cost=3, pre=[["fast_breeder", "nuclear_moratorium"]], avail=f"has_country_flag = {P}_chernobyl",
  reward=J(core("energie", nuclear=-0.03, renew=0.05), v("cwger_anti_nuclear", -5), core("bonn", stab=0.02)))
F("gas_for_pipes", "energy_programme", 2, 1, cost=3,
  reward=J(f"add_ideas = {P}_idea_soviet_gas", core("energie", fossil=-0.03, gain=0.03), kl(4), bop(0.05),
           "if = { limit = { country_exists = SOV } SOV = { add_opinion_modifier = { target = ROOT modifier = medium_increase } } }",
           opinion("USA", "small_decrease")))
F("urengoy", "gas_for_pipes", 0, 1, cost=3, avail="date > 1980.6.1",
  reward=J("set_global_flag = COLDWAR_SOV_pipelines_to_europe_signed", state_build(BAY, "fossil_powerplant"), core("energie", gain=0.05), opinion("USA", "medium_decrease"), kl(3)))
F("energy_savings_act", "urengoy", 0, 1, cost=3, icon="green_projects", name="The Energy Savings Act",
  desc="Insulation standards for every new building, efficiency rules for boilers, a ministry that counts kilowatt-hours.",
  reward=J(core("energie", use=-0.05), money_gdp(-0.001)))
F("environment_ministry", "waldsterben", 2, 1, cost=3, pre=[["waldsterben", "fast_breeder", "nuclear_moratorium", "chernobyl_response"]],
  avail=f"OR = {{ has_country_flag = {P}_chernobyl date > 1985.12.31 }}",
  reward=J(core("energie", renew=0.05, use=-0.03), v("cwger_anti_nuclear", -4), party("greens", -0.003)))
F("green_dot", "environment_ministry", -1, 1, cost=3,
  reward=J(core("energie", use=-0.03), core("modell", prod=0.01), state_build(NDS, "industrial_complex")))
F("renewable_research", "green_dot", -1, 1, cost=3, filt="FOCUS_FILTER_RESEARCH",
  reward=J(state_build(SH, "renewable_energy_infra"), state_build(NDS, "renewable_energy_infra"), core("energie", renew=0.1)))
F("feed_in_law", "renewable_research", 0, 1, cost=3,
  reward=J(state_build(SH, "renewable_energy_infra"), state_build(BAY, "renewable_energy_infra"), core("energie", renew=0.1, fossil=-0.03), money_gdp(-0.002)))
F("eco_tax", "green_dot", 1, 1, cost=3, avail=GREEN_GOV,
  reward=J(f"add_ideas = {P}_idea_eco_tax", core("energie", use=-0.05, fossil=-0.03), core("modell", tax=0.01)))
F("atomkonsens", "environment_ministry", 1, 1, cost=3, avail=GREEN_GOV,
  reward=J(core("energie", nuclear=-0.1, renew=0.05), v("cwger_anti_nuclear", -15), protest(-6)))

# =================================================================== IV. MILITANT DEMOCRACY
F("internal_security", ROOT_KEY, -2, 1, cost=1, icon="interior",
  reward=J(core("wehrhaft", detect=0.05), bka(1),
           tt(f"{P}_tt_sec_window", "The §YInternal Security§! window on the top bar runs the manhunt, the protection details, the prisons and the crisis staff.")))
F("bka_expansion", "internal_security", -2, 1, cost=3, icon="police_funding",
  reward=J(bka(1), core("wehrhaft", detect=0.1, police=0.05), state_build(HES, "offices")))
F("inpol", "bka_expansion", 0, 1, cost=3, icon="cryptography",
  reward=J(unlock("cwsec_inpol", "§G+2§! trace per month on everyone on the wanted list"), core("wehrhaft", detect=0.05), v("cwger_rechtsstaat", -1)))
F("dragnet", "inpol", 0, 1, cost=3, icon="cryptography",
  reward=J(bka(1), unlock("cwsec_dragnet_doctrine", "the §YDragnet§! in the internal security window (needs BKA level 3)"), v("cwger_rechtsstaat", -2)))
F("security_group", "bka_expansion", 1, 1, cost=2, icon="policeman", name="The Security Group",
  desc="The BKA's Sicherungsgruppe guards the constitutional organs - and, after Ponto and Schleyer, everyone the RAF might pick.",
  reward=J(sec_slots(1), core("wehrhaft", defend=0.05)))
F("federal_property_protection", "security_group", 0, 2, cost=3, icon="border_guard", name="Protecting the Federal Republic",
  desc="The Federal Border Guard takes over the protection of federal buildings, airports and embassies.",
  reward=J(sec_slots(1), core("wehrhaft", defend=0.1, police=0.05)))
F("gsg9", "internal_security", 0, 1, cost=3, icon="gsg9", avail=f"OR = {{ has_country_flag = {P}_munich_happened date > 1972.9.25 }}",
  reward=J(gsg9(1), core("wehrhaft", defend=0.05)))
F("gsg9_training", "gsg9", 0, 1, cost=3, icon="gsg9",
  reward=J(gsg9(1), opinion("ENG", "small_increase"), opinion("ISR", "small_increase")))
F("gsg9_global", "gsg9_training", 0, 1, cost=3, icon="gsg9",
  reward=J(gsg9(1), core("wehrhaft", defend=0.05)))
F("contact_ban_law", "gsg9_global", 0, 1, cost=2,
  avail=f"OR = {{ has_country_flag = {P}_hostage_crisis_active has_country_flag = {P}_krisenstab_models date > 1977.9.1 }}",
  reward=J(unlock(f"{P}_contact_ban_law", "the §YContact Ban§! for the crisis staff"), v("cwger_rechtsstaat", -3)))
F("stammheim_trial", "bka_expansion", -1, 1, cost=3, avail="check_variable = { cwger_raf_prisoners > 1 }",
  reward=J(f"set_country_flag = {P}_stammheim", state_build(BW, "offices", 1), v("cwger_security", 4), v("cwger_raf_milieu", 2)))
F("paragraph_129a", "stammheim_trial", 0, 2, cost=3, pre=[["dragnet", "stammheim_trial"]],
  reward=J(v("cwger_raf_cadre", -4), v("cwger_rechtsstaat", -3), core("wehrhaft", detect=0.05)))
F("strong_state", "paragraph_129a", 0, 1, cost=3, avail=f"NOT = {{ has_completed_focus = {P}_liberal_state }}", icon="shield", name="The Strong State",
  desc="Whoever attacks the state will meet all of it: more police, more powers, more computers - and less patience with critics.",
  reward=J(core("wehrhaft", detect=0.1, police=0.1), v("cwger_security", 8), v("cwger_rechtsstaat", -6), v("cwger_raf_milieu", 3), faction("mittelstand", 4)))
F("security_state", "strong_state", 0, 1, cost=3, avail=f"has_country_flag = {P}_krisenstab_models",
  reward=J(f"add_ideas = {P}_idea_security_state", bka(1), v("cwger_rechtsstaat", -4)))
F("radicals_decree", "internal_security", 2, 1, cost=2, mutex=["no_radicals_decree"],
  reward=J(f"add_ideas = {P}_idea_radicals_decree", core("wehrhaft", influence=0.1), v("cwger_rechtsstaat", -4), v("cwger_raf_milieu", 3), protest(3)))
F("no_radicals_decree", "internal_security", 3, 1, cost=2, mutex=["radicals_decree"], ai=3,
  reward=J(v("cwger_rechtsstaat", 4), v("cwger_raf_milieu", -2), core("wehrhaft", influence=-0.05)))
F("verfassungsschutz", "radicals_decree", 0, 1, cost=3, pre=[["radicals_decree", "no_radicals_decree"]], icon="secret_police",
  reward=J(v("cwger_counterintel", 10), v("cwger_stasi_penetration", -6), core("wehrhaft", influence=0.1)))
F("data_protection", "verfassungsschutz", 1, 1, cost=2, pre=[["no_radicals_decree", "verfassungsschutz"]],
  reward=J(v("cwger_rechtsstaat", 5), core("wehrhaft", police=-0.03), party("fdp", 0.002)))
F("liberal_state", "data_protection", 0, 1, cost=3, avail=f"NOT = {{ has_completed_focus = {P}_strong_state }}", icon="civil_rights", name="The Liberal Rule of Law",
  desc="Gerhart Baum's answer: a state that does not let its enemies dictate how unfree it becomes.",
  reward=J(v("cwger_rechtsstaat", 8), v("cwger_raf_milieu", -5), v("cwger_security", -4), core("wehrhaft", detect=0.03), party("fdp", 0.003)))
F("crown_witness", "liberal_state", -2, 1, cost=3, pre=[["dragnet"], ["verfassungsschutz"]], avail=ERA2,
  reward=J(unlock("cwsec_unlock_kronzeuge", "§YRecruit a Crown Witness§! in the internal security window"), v("cwger_rechtsstaat", -2)))
F("exit_programme", "liberal_state", 0, 1, cost=3, icon="truce", name="A Way Out",
  desc="The Verfassungsschutz's exit programme: new identities, work, protection for those who leave the underground.",
  reward=J(unlock("cwsec_unlock_dropout", "the §YExit Programme§! in the internal security window"), v("cwger_raf_milieu", -4)))
F("reconciliation_offer", "exit_programme", 0, 1, cost=3, pre=[["crown_witness", "exit_programme", "data_protection"]],
  avail=f"OR = {{ check_variable = {{ cwger_raf_gen > 2 }} date > 1990.1.1 }}",
  reward=J(unlock(f"{P}_kinkel_initiative", "§YRelease Renouncing Prisoners§! in the internal security window"), v("cwger_raf_milieu", -6), v("cwger_rechtsstaat", 3)))
F("militant_democracy", "internal_security", 5, 1, cost=2, icon="ban_npd",
  reward=J(unlock(f"{P}_ban_unlocked", "§YBan an Extremist Organisation§! in the internal security window"), core("wehrhaft", influence=0.05, detect=0.03)))
F("far_right_watch", "militant_democracy", 0, 1, cost=3,
  avail="OR = { check_variable = { cwger_terror_right > 15 } date > 1979.12.31 }",
  reward=J(f"set_country_flag = {P}_far_right_watch", v("cwger_terror_right", -4), core("wehrhaft", detect=0.05)))
F("ban_wsg", "far_right_watch", 0, 1, cost=2, avail=f"has_country_flag = {P}_wsg_hoffmann_active",
  reward=J(f"clr_country_flag = {P}_wsg_hoffmann_active", v("cwger_terror_right", -8), party("npd", -0.002)))
F("after_rostock", "ban_wsg", 0, 1, cost=3, pre=[["far_right_watch"]], avail=f"has_country_flag = {P}_asylum_surge",
  reward=J(f"set_country_flag = {{ flag = {P}_far_right_banned days = 1095 value = 1 }}", v("cwger_terror_right", -10), core("wehrhaft", defend=0.05), protest(-4)))
F("ban_pkk", "after_rostock", 0, 1, cost=2, avail="date > 1992.1.1",
  reward=J(f"set_country_flag = {P}_pkk_banned", v("cwger_terror_foreign", -6), opinion("TUR", "medium_increase")))

# =================================================================== V. BUNDESWEHR
F("citizen_in_uniform", ROOT_KEY, 10, 1, cost=1, icon="heer", filt="FOCUS_FILTER_MANPOWER",
  reward=J(core("armee", org=0.03, core=0.03), ws(0.02)))
F("army_structure_3", "citizen_in_uniform", -3, 1, cost=3, icon="army_reform", filt="FOCUS_FILTER_MANPOWER",
  reward=J(core("armee", org=0.03, plan=0.05), tech("CAT_infantry_fighting_vehicles", 0.5, 1)))
F("leber_modernisation", "army_structure_3", 0, 1, cost=3, icon="modernisation", filt="FOCUS_FILTER_MANPOWER",
  reward=J(core("armee", equip=-0.05, xp=0.02), faction("dgb", 3), tech("CAT_artillery", 0.5, 1)))
F("leopard_2", "leber_modernisation", 0, 1, cost=5, icon="leopard", avail="date > 1977.1.1", filt="FOCUS_FILTER_MANPOWER",
  reward=J(f"set_country_flag = {P}_leopard_2", tech("CAT_main_battle_tanks", 1, 2), state_build(BAY, "arms_factory"), state_build(HES, "arms_factory"), core("armee", core=0.05)))
F("army_structure_4", "leopard_2", 0, 1, cost=5, avail=ERA2, filt="FOCUS_FILTER_MANPOWER",
  reward=J(f"add_ideas = {P}_idea_army_structure_4", core("armee", org=0.05, core=0.05, consc=0.05)))
F("conscription_w15", "army_structure_4", -1, 1, cost=2, mutex=["conscription_w18"], icon="conscription",
  reward=J(core("armee", consc=0.03, xp=-0.01), v("cwger_peace_movement", -3), party("spd", 0.002)))
F("conscription_w18", "army_structure_4", 1, 1, cost=2, mutex=["conscription_w15"], icon="conscription", ai=4,
  reward=J(core("armee", consc=0.05, xp=0.02), v("cwger_peace_movement", 5), ws(0.02)))
F("home_defence", "conscription_w15", 1, 1, cost=3, pre=[["conscription_w15", "conscription_w18"]], icon="reserve",
  reward=J(f"add_ideas = {P}_idea_territorial_army", core("armee", core=0.05), core("armee", consc=0.02)))
F("army_of_unity", "home_defence", 0, 1, cost=3, avail=UNITY, icon="unified",
  reward=J(core("armee", org=0.03), "add_manpower = 50000", v("cwger_east_burden", -3)))
F("army_structure_5", "army_of_unity", 0, 1, cost=3,
  reward=J(f"add_ideas = {P}_idea_army_structure_5", core("armee", equip=-0.05, consc=-0.05, xp=0.03)))
F("tornado", "citizen_in_uniform", -1, 1, cost=3, icon="fighter", avail="date > 1974.1.1", filt="FOCUS_FILTER_AIR_XP",
  reward=J(tech("CAT_medium_aircraft", 0.5, 2), state_build(BAY, "arms_factory"), opinion("ENG", "medium_increase"), opinion("ITA", "medium_increase"), infl("ITA", 1)))
F("bundeswehr_universities", "tornado", 0, 1, cost=2, icon="education",
  reward=J(f"add_timed_idea = {{ idea = {P}_idea_officer_education days = 3650 }}", state_build(HH, "offices"), state_build(BAY, "offices"), core("armee", xp=0.02)))
F("jaeger_90", "bundeswehr_universities", 0, 1, cost=5, icon="fighter", avail=ERA2, filt="FOCUS_FILTER_AIR_XP",
  reward=J(tech("CAT_wing_designs", 0.5, 2), tech("CAT_air_engines", 0.5, 1), money_gdp(-0.003), infl("ENG", 1), infl("SPR", 1)))
F("patriot", "jaeger_90", 0, 1, cost=3, icon="radar",
  reward=J(tech("CAT_surface_to_air_missiles", 0.5, 2), state_build(NRW, "radar_station"), state_build(HES, "anti_air_building"), opinion("USA", "small_increase")))
F("baltic_navy", "citizen_in_uniform", 1, 1, cost=3, icon="marine", filt="FOCUS_FILTER_MANPOWER",
  reward=J(state_build(SH, "naval_base"), state_build(SH, "dockyard"), tech("CAT_frigates", 0.5, 1)))
F("type_209", "baltic_navy", 0, 1, cost=3, icon="submarine",
  reward=J(f"set_country_flag = {P}_type209_exports", tech("CAT_submarines", 0.5, 2), state_build(SH, "dockyard"), core("welt", market=0.03)))
F("f122_frigates", "baltic_navy", 1, 1, cost=3, icon="frigates", avail="date > 1976.1.1",
  reward=J(tech("CAT_frigates", 0.5, 2), tech("CAT_naval_anti_ship_missiles", 0.5, 1), state_build(HH, "dockyard")))
F("arms_export_guidelines", "type_209", 0, 1, cost=2,
  reward=J(f"set_country_flag = {P}_export_guidelines", corruption(False), core("welt", support=0.05), v("cwger_rechtsstaat", 2)))
F("nato_awacs", "tornado", 1, 1, cost=3, icon="radar",
  reward=J(state_build(NRW, "radar_station"), state_build(NRW, "air_base"), core("armee", plan=0.05)))
F("nuclear_sharing_role", "citizen_in_uniform", 3, 1, cost=2, icon="nuclear",
  reward=J(core("armee", plan=0.05), core("west", ideo=0.03), v("cwger_peace_movement", 3)))
F("national_option", "nuclear_sharing_role", 0, 3, cost=5, icon="nuclear_science",
  avail=f"has_country_flag = {P}_nato_crisis has_completed_focus = {P}_fast_breeder NOT = {{ has_country_flag = {P}_npt_ratified }}", ai=0,
  reward=J(tech("CAT_intermediate_range_ballistic_missiles", 0.5, 1), v("cwger_westbindung", -15), opinion("USA", "large_decrease"), opinion("SOV", "large_decrease"),
           tension(5), protest(15)))
F("forward_defence", "citizen_in_uniform", 5, 1, cost=3, icon="tanks", name="Forward Defence",
  desc="Not a metre of German soil given up: the Bundeswehr's corps dig in at the inner-German border, and their exercises are meant to be seen from the other side.",
  reward=J(unlock("cwgg_unlock_manoeuvre", "§YExercises Near the Border§! in the inner-German relations window"), core("armee", core=0.05)))
F("prepare_defence_case", "forward_defence", 0, 1, cost=3, icon="home_stretch", name="Prepare the State of Defence",
  desc="Emergency laws, the Joint Committee, mobilisation plans for 1.3 million reservists - written in 1968, rehearsed in secret.",
  reward=J(unlock("cwgg_unlock_alert3", "the third alert level in the inner-German relations window, even before war danger"), core("armee", consc=0.05, plan=0.05), ws(0.03)))
F("civilian_service", "army_structure_4", 2, 1, cost=2, icon="pacifists",
  reward=J(v("cwger_peace_movement", -5), core("modell", social=-0.01), party("greens", -0.002)))
F("out_of_area_ruling", "army_of_unity", 1, 1, cost=3, icon="peacekeeping", avail=OPEN_OR_UNITY,
  reward=J(f"set_country_flag = {P}_deployments_allowed", core("armee", xp=0.03), core("welt", support=0.05)))
F("kosovo_decision", "out_of_area_ruling", 0, 1, cost=3, avail="date > 1998.6.1", icon="kosovo",
  reward=J(core("armee", xp=0.03), opinion("USA", "medium_increase"), v("cwger_peace_movement", 8), protest(6)))
F("tornado_ecr", "out_of_area_ruling", 1, 1, cost=3,
  reward=J(tech("CAT_medium_aircraft", 0.5, 1), core("armee", xp=0.02)))

# =================================================================== VI. WESTERN INTEGRATION
F("atlantic_anchor", ROOT_KEY, 21, 1, cost=1, icon="nato",
  reward=J(core("west", ideo=0.05), opinion("USA", "small_increase")))
F("elysee_revival", "atlantic_anchor", -2, 1, cost=3, icon="france",
  reward=J(infl("FRA", 3), opinion("FRA", "medium_increase", mutual=True), core("west", europe=0.02), europe(3)))
F("ec_enlargement", "elysee_revival", -1, 1, cost=3, icon="europe",
  reward=J(infl("ENG", 2), opinion("ENG", "medium_increase"), opinion("DEN", "small_increase"), core("west", trade=0.05)))
F("political_cooperation", "elysee_revival", 1, 1, cost=2, icon="western_europe",
  reward=J(core("west", opinion=0.05, europe=0.02), infl("BEL", 2), infl("HOL", 2)))
F("franco_german_brigade", "ec_enlargement", 1, 1, cost=3, pre=[["ec_enlargement", "political_cooperation"]], avail=ERA2, icon="france",
  reward=J(core("armee", org=0.02), infl("FRA", 3), state_mod(BW, "garrison"), opinion("FRA", "medium_increase")))
F("schengen", "franco_german_brigade", 0, 1, cost=3, avail="date > 1985.1.1", icon="borders",
  reward=J(f"add_timed_idea = {{ idea = {P}_idea_open_borders days = 3650 }}", core("west", trade=0.05), infl("HOL", 2), infl("BEL", 2), infl("LUX", 3)))
F("maastricht", "schengen", 0, 1, cost=5, avail=OPEN_OR_UNITY, icon="euro",
  reward=J("country_event = { id = COLDWAR_GER.110 days = 60 }", core("west", europe=0.05, opinion=0.05), infl("FRA", 3), infl("ITA", 2)))
F("uruguay_round", "maastricht", -1, 1, cost=3, avail="date > 1990.1.1", icon="trade_europe",
  reward=J(core("welt", market=0.05), core("west", trade=0.05)))
F("recognise_croatia", "maastricht", 1, 1, cost=2, pre=[["maastricht"]],
  avail="OR = { country_exists = CRO country_exists = SLV } date > 1991.6.1",
  reward=J(infl("CRO", 5), infl("SLV", 5), opinion("SER", "large_decrease"), opinion("FRA", "small_decrease")))
F("g7_bonn", "atlantic_anchor", 1, 1, cost=3, avail="date > 1977.1.1", icon="usa",
  reward=J(core("west", trade=0.05), core("welt", market=0.03), opinion("USA", "medium_increase"), opinion("JAP", "small_increase")))
F("double_track", "g7_bonn", 0, 1, cost=5, avail="date > 1978.6.1", icon="deployment",
  reward=J(f"set_country_flag = {P}_double_track", v("cwger_peace_movement", 10), core("armee", plan=0.05),
           tt(f"{P}_tt_missile_crisis", "East Berlin and Moscow answer with a §RMissile Crisis§! in the inner-German relations window.")))
F("deployment_vote", "double_track", -1, 1, cost=3, mutex=["no_deployment"], avail="date > 1983.6.1 check_variable = { cwger_margin > -1 }",
  reward=J(f"set_country_flag = {P}_pershing_deployed", opinion("USA", "large_increase"), v("cwger_peace_movement", 10), kl(-8)))
F("no_deployment", "double_track", 1, 1, cost=3, mutex=["deployment_vote"], avail=f"date > 1983.6.1 OR = {{ {SPD} {GREEN_GOV} }}", ai=2,
  reward=J(f"set_country_flag = {P}_nato_crisis", v("cwger_westbindung", -15), opinion("USA", "large_decrease"), v("cwger_peace_movement", -10), kl(8), bop(0.1)))
F("two_plus_four_west", "deployment_vote", 1, 1, cost=3, pre=[["deployment_vote", "no_deployment"]], avail=WALL, icon="unified",
  reward=J(opinion("USA", "medium_increase"), opinion("ENG", "small_increase"), opinion("FRA", "small_increase"), v("cwger_unity", 8)))
F("checkbook_diplomacy", "two_plus_four_west", -1, 1, cost=2, avail="date > 1990.8.1",
  reward=J(money_gdp(-0.004), opinion("USA", "medium_increase"), core("welt", support=0.05)))
F("nato_enlargement", "two_plus_four_west", 1, 1, cost=3, avail=f"{UNITY} date > 1993.1.1",
  reward=J(infl("POL", 5), infl("CZE", 4), infl("HUN", 4), opinion("SOV", "medium_decrease"), core("west", opinion=0.05)))
F("mbfr", "atlantic_anchor", 3, 1, cost=2, icon="truce",
  reward=J(tension(-2), core("armee", equip=-0.03), kl(2)))
F("offset_payments", "mbfr", 0, 1, cost=3, icon="usa", name="Offset Payments",
  desc="Bonn pays for American troops in Germany - with arms purchases, Bundesbank loans and a promise not to cash its dollars in for gold.",
  reward=J(money_gdp(-0.002), opinion("USA", "large_increase"), lever("allianz", 1), core("west", ideo=0.03)))

# =================================================================== VII. DEUTSCHLANDPOLITIK
OST = "FOCUS_FILTER_POLITICAL"
F("dp_hub", ROOT_KEY, 35, 1, cost=1, icon="east_germany", name="Rethinking Deutschlandpolitik",
  desc="Twenty years of non-recognition have made the Wall higher, not lower. Bonn must decide what it wants from the other German state - and how hard it is prepared to push.",
  reward=J(ost_face("neutral"), gamevar("cwgg_init_brd", 2, f"{P}_tt_init_2", "Initiative in the inner-German relations window: §G+2§!"),
           tt(f"{P}_tt_rv_window", "The §YInner-German Relations§! window runs the climate, crises, levers, channels and the treaty ladder.")))
# --- change through rapprochement
F("wandel_durch_annaeherung", "dp_hub", -4, 1, cost=3, mutex=["confrontation_course"], icon="negotiations", name="Change through Rapprochement",
  desc="Egon Bahr's formula from Tutzing in 1963: accept the realities in order to change them. Small steps for people instead of big words about unity.",
  reward=J(ost_face("rapprochement"),
           "set_country_flag = cwgg_policy_rapprochement", core("ost", stab=0.02, cg=-0.01), climate_base(3), bop(0.15),
           unlock("cwgg_unlock_vertrag_1", "the treaty §YMeeting of the Heads of Government§!")))
F("bahr_paper", "wandel_durch_annaeherung", -1, 1, cost=2, icon="secret_meeting", name="The Bahr Paper",
  desc="Ten points, written in Moscow by a state secretary who negotiated as if he were foreign minister. Leaked to the press, it becomes the programme.",
  reward=J(channel_unlock("bahr"), kl(3), party("cdu", 0.002)))
F("erfurt_kassel", "wandel_durch_annaeherung", 1, 1, cost=2,
  reward=J(kl(5), party("spd", 0.004), core("ost", stab=0.01),
           tt(f"{P}_tt_erfurt", "Makes the treaty §YMeeting of the Heads of Government§! faster to conclude.") , "add_to_variable = { cwgg_basis_bonus = 1 }"))
F("moscow_treaty", "bahr_paper", -1, 1, cost=5, icon="soviet",
  reward=J(channel_unlock("draht"), tension(-3), kl(5), core("ost", sanc=0.1),
           "if = { limit = { country_exists = SOV } SOV = { add_opinion_modifier = { target = ROOT modifier = medium_increase } } }", core("welt", market=0.02)))
F("warsaw_treaty", "bahr_paper", 1, 1, cost=5, icon="poland",
  reward=J(infl("POL", 4), opinion("POL", "large_increase", mutual=True), kl(3), party("cdu", 0.003), v("cwger_csu_autonomy", 4)))
F("ratification", "moscow_treaty", 1, 1, cost=3, pre=[["moscow_treaty"], ["warsaw_treaty"]], icon="parliament", avail="check_variable = { cwger_margin > 0 }",
  reward=J(f"set_country_flag = {P}_treaties_ratified", core("ost", stab=0.02), climate_base(2), party("spd", 0.006), pp(25)))
F("basic_treaty", "ratification", 2, 1, cost=3, avail=f"has_completed_focus = {P}_erfurt_kassel", icon="treaty",
  reward=J(unlock("cwgg_unlock_vertrag_3", "the §YBasic Treaty§! in the treaty ladder"), kl(3), core("ost", cg=-0.01)))
F("prague_treaty", "ratification", -1, 1, cost=3, icon="czechia",
  reward=J(infl("CZE", 4), opinion("CZE", "large_increase", mutual=True), "if = { limit = { country_exists = CZE } CZE = { " + f"{P}_lift_mil_sanction_on_prev = yes" + " } }", kl(2)))
F("helsinki", "ratification", 1, 2, cost=5, avail="date > 1974.6.1", icon="diplomacy",
  reward=J(f"set_country_flag = {P}_helsinki", tension(-4), climate_base(2), dv("cwddr_west_media", 4), dv("cwddr_opposition", 3), core("west", opinion=0.05)))
F("prisoner_buyouts", "basic_treaty", 0, 1, cost=3, icon="refugees", name="Buying Freedom",
  reward=J(f"set_country_flag = {P}_freikauf_unlocked", lever("menschen", 1), core("bonn", stab=0.01)))
F("swing_credit", "prisoner_buyouts", -1, 1, cost=3, icon="trade_europe",
  reward=J(f"set_country_flag = {P}_swing_unlocked", lever("devisen", 1), lever("handel", 1), core("ost", cg=-0.01)))
F("church_contacts", "prisoner_buyouts", 1, 1, cost=2, icon="speech",
  reward=J(f"set_country_flag = {P}_church_contacts", channel_unlock("kirche"), dv("cwddr_opposition", 2)))
F("west_media_strategy", "helsinki", -1, 1, cost=3, pre=[["helsinki"]], icon="television",
  reward=J(lever("medien", 1), dv("cwddr_west_media", 6), state_mod(WB, "showcase")))
F("coalition_of_reason", "swing_credit", 0, 1, cost=3, icon="negotiations", name="The Coalition of Reason",
  desc="Two German leaders who agree on one thing: that no war must ever again start from German soil. Missiles or not, they keep talking.",
  avail=ERA2,
  reward=J(unlock("cwgg_unlock_vertrag_8", "the treaty §YState Visit of the SED Leader§!"), climate_base(4), tension(-2)))
F("community_of_responsibility", "church_contacts", 0, 1, cost=3, icon="truce", name="A Community of Responsibility",
  desc="The two German states share responsibility for peace in Europe: a phrase East Berlin and Bonn both use - for very different reasons.",
  reward=J(climate_base(3), core("ost", stab=0.02), lever("menschen", 1)))
F("embassy_refugees", "coalition_of_reason", 0, 1, cost=2, pre=[["coalition_of_reason", "community_of_responsibility"]],
  avail=f"{DDR_EX} DDR = {{ check_variable = {{ cwddr_wende_stage > 0 }} }}",
  reward=J(dv("cwddr_exit_pressure", 5), money_gdp(-0.001), core("bonn", stab=0.01)))
# --- the legal position (combinable with rapprochement)
F("rechtsposition", "dp_hub", 6, 1, cost=2, icon="constitution", name="The Legal Position",
  desc="The Basic Law's preamble, one German citizenship, the Reich in its 1937 borders in law: Bonn may talk to East Berlin, but it gives nothing away.",
  reward=J(lever("recht", 1), core("ost", ws=0.02), bop(-0.1)))
F("letter_on_unity", "rechtsposition", -1, 1, cost=2, icon="speech", name="The Letter on German Unity",
  desc="Handed over with every treaty: the Federal Republic's goal remains a state of peace in Europe in which the German people regain their unity in free self-determination.",
  reward=J(v("cwger_unity", 5), dv("cwddr_recognition", -3), core("ost", stab=0.01)))
F("billion_credit", "rechtsposition", 1, 1, cost=3, avail=f"OR = {{ {UNION} has_country_flag = cwgg_kanal_koko_unlocked }} {ERA2}",
  reward=J(f"set_country_flag = {P}_credit_unlocked", channel_unlock("koko"), lever("devisen", 1), v("cwger_csu_autonomy", 4)))
F("salzgitter", "letter_on_unity", 0, 1, cost=2, icon="policeman", name="The Salzgitter Registry",
  desc="Since 1961 a public prosecutor's office in Lower Saxony has recorded every shot at the border and every political sentence in the GDR - for the day they can be tried.",
  reward=J(lever("recht", 1), dv("cwddr_sed_control", -2), state_build(NDS, "offices", 1)))
F("magnet_theory", "billion_credit", 0, 1, cost=3, icon="west_germany",
  reward=J(lever("medien", 1), dv("cwddr_exit_pressure", 4), core("modell", cg=-0.01)))
F("csce_human_rights", "salzgitter", 1, 1, cost=3, pre=[["salzgitter", "magnet_theory"]], icon="civil_rights", name="Human Rights at the CSCE",
  desc="Basket Three of Helsinki, quoted back at the SED at every follow-up conference in Belgrade, Madrid and Vienna.",
  reward=J(dv("cwddr_opposition", 4), dv("cwddr_sed_control", -2), lever("recht", 1), core("west", opinion=0.03)))
# --- confrontation
F("confrontation_course", "dp_hub", 1, 1, cost=3, mutex=["wandel_durch_annaeherung"], icon="border_guard",
  name="The Policy of Strength",
  desc="No recognition, no credits, no illusions: the GDR is a Soviet satrapy that will collapse if it is pressed hard enough - and Bonn will press.",
  reward=J(ost_face("strength"),
           "set_country_flag = cwgg_policy_strength", core("ost", ws=0.05, stab=-0.01), climate_base(-5), lever("allianz", 1), bop(-0.2)),
  ai=1, ai_mod="modifier = { factor = 0 is_ai = yes }")
F("renegotiate_treaties", "confrontation_course", -1, 1, cost=3,
  reward=J(f"set_country_flag = {P}_treaties_with_reservations", f"set_country_flag = {P}_treaties_ratified", lever("recht", 1), kl(-5), party("cdu", 0.004)))
F("sole_mandate_renewed", "confrontation_course", 1, 1, cost=3, icon="coat_of_arms", name="Renew the Sole Mandate",
  desc="Bonn alone speaks for Germany. Any state that recognises the GDR will lose its West German aid - the Hallstein Doctrine, revived.",
  reward=J(lever("recht", 1), dv("cwddr_recognition", -10), kl(-8), core("welt", support=-0.05)))
F("economic_war", "renegotiate_treaties", 1, 1, cost=3, pre=[["renegotiate_treaties", "sole_mandate_renewed"]], icon="embargo", name="Economic Warfare",
  desc="Close the back door into the Common Market, freeze the Swing, end the credits: let the GDR's planners discover what the Deutschmark was worth to them.",
  reward=J(lever("handel", 1), dv("cwddr_hard_currency", 10), dv("cwddr_west_dependency", -10), kl(-10), "if = { limit = { country_exists = DDR } DDR = { " + f"{P}_sanction_prev_economic = yes" + " } }",
           core("ost", sanc=0.1)))
F("escape_as_policy", "economic_war", -1, 1, cost=3, icon="refugees", name="Escape as Reason of State",
  desc="Tunnels, forged passports, cars with hidden compartments: what was tolerated becomes encouraged - and East Berlin calls it 'trafficking in human beings'.",
  reward=J(dv("cwddr_exit_pressure", 8), lever("menschen", 1), kl(-6), "set_country_flag = { flag = cwgg_escape_helpers days = 720 value = 1 }"))
F("radio_war", "economic_war", 1, 1, cost=2, icon="television", name="The Airwaves War",
  desc="New transmitters on the Brocken's western side, RIAS on full power, programmes made for the East.",
  reward=J(lever("medien", 1), dv("cwddr_west_media", 6), dv("cwddr_sed_control", -3), kl(-4)))
F("liberation_doctrine", "escape_as_policy", 1, 1, cost=5, pre=[["escape_as_policy"], ["radio_war"]], icon="tank_wall", name="The Liberation Doctrine",
  desc="If the GDR breaks apart, Bonn will not stand by as in 1953 and 1956. A doctrine for the day after - and, if needed, for the day before.",
  avail="check_variable = { cwgg_klima < -49 } check_variable = { cwgg_stufe > 3 }", ai=0,
  wargoal="DDR",
  reward=J(unlock("cwgg_liberation_doctrine", "§RStrike first§! in a countdown at the brink (war path A)"),
           unlock("cwgg_unlock_brotherly_help", "§RBrotherly Help§! in an uprising in the GDR (war path C)"),
           core("armee", plan=0.1, org=0.03), ws(0.05), tension(5), opinion("SOV", "large_decrease"),
           tt(f"{P}_tt_liberation", "§RThis opens two paths to war with the GDR. Whether NATO's governments follow is their own decision; whether the Soviet Union fights depends on its guarantee for the GDR.§!")))
F("crackdown_response", "confrontation_course", 3, 1, cost=2, pre=[["dp_hub"]],
  avail=f"{DDR_EX} DDR = {{ check_variable = {{ cwddr_wende_stage = 9 }} }}",
  reward=J("if = { limit = { country_exists = DDR } DDR = { " + f"{P}_sanction_prev_economic = yes" + " } }", kl(-15), v("cwger_westbindung", 4)))
F("second_cold_war", "crackdown_response", 0, 1, cost=2,
  avail=f"OR = {{ has_country_flag = {P}_soviets_refused has_global_flag = {P}_moscow_coup_succeeded }}",
  reward=J(f"add_ideas = {P}_idea_second_cold_war", ws(0.05)))
# --- unity
F("ten_point_plan", "dp_hub", -1, 10, cost=3, pre=[],
  avail=f"{WALL} {NO_UNITY} {DDR_EX}", icon="national_unity",
  reward=J("DDR = { country_event = { id = COLDWAR_GER_DDR.35 days = 3 } }", v("cwger_unity", 15), party("cdu", 0.004)))
F("support_round_table", "ten_point_plan", 1, 1, cost=2, avail=f"{WALL} {DDR_EX}",
  reward=J(dv("cwddr_opposition", 8), v("cwger_unity", 5), money_gdp(-0.001)))
F("treaty_community", "ten_point_plan", -1, 1, cost=3, avail=f"{WALL} {DDR_EX}",
  reward=J(f"set_country_flag = {P}_confederation_offered", v("cwger_unity", 5)))
F("art146_debate", "treaty_community", -1, 1, cost=3, avail=f"{WALL} {NO_UNITY}",
  reward=J(f"set_country_flag = {P}_art146_prepared", v("cwger_rechtsstaat", 2), party("greens", 0.002)))
F("neutral_offer", "support_round_table", 0, 1, cost=3, avail=f"has_country_flag = {P}_soviets_want_neutrality", ai=1,
  reward=J(f"set_country_flag = {P}_neutrality_accepted", v("cwger_westbindung", -10)))
F("oder_neisse_final", "treaty_community", 0, 1, cost=3, avail=OPEN_OR_UNITY,
  reward=J(opinion("POL", "large_increase", mutual=True), infl("POL", 3), party("rep", 0.002)))
F("unity_treaty", "oder_neisse_final", 0, 1, cost=5, avail=UNITY, icon="unified",
  reward=J(f"add_ideas = {P}_idea_inner_unity", v("cwger_east_burden", -5), core("bonn", stab=0.03)))
F("soviet_withdrawal", "unity_treaty", 1, 1, cost=3, avail=UNITY,
  reward=J(f"set_country_flag = {P}_soviets_paid", money_gdp(-0.004), opinion("SOV", "large_increase"), tension(-3)))
F("stasi_files", "unity_treaty", 0, 1, cost=3, icon="secret_police",
  reward=J(v("cwger_rechtsstaat", 4), v("cwger_stasi_penetration", -20), v("cwger_scandal", 6),
           "if = { limit = { has_global_flag = cwgg_raf_in_ddr NOT = { has_global_flag = cwgg_raf_in_ddr_found } } set_global_flag = cwgg_raf_in_ddr_found country_event = { id = COLDWAR_GGR.70 days = 10 } }"))

# =================================================================== VIII. CIVILIAN POWER
F("cultural_diplomacy", ROOT_KEY, 49, 1, cost=1, icon="diplomacy",
  reward=J(f"add_timed_idea = {{ idea = {P}_idea_cultural_diplomacy days = 3650 }}", core("welt", support=0.05)))
# --- the great events: one chain; a focus whose date window has passed is bypassed, so the chain never blocks
F("munich_olympics", "cultural_diplomacy", -2, 1, cost=2, avail="date < 1972.9.1", bypass="date > 1972.8.31", icon="republic",
  reward=J(f"set_country_flag = {P}_olympic_security", state_build(BAY, "infrastructure", 1, slot=False), state_mod(BAY, "olympic_city"), core("bonn", stab=0.02)))
F("world_cup_1974", "munich_olympics", 0, 1, cost=2, avail="date > 1974.6.1 date < 1974.8.1", bypass="date > 1974.7.31",
  reward=J(core("bonn", stab=0.03), ws(0.02)))
F("olympic_boycott", "world_cup_1974", 0, 1, cost=2, avail="date > 1979.12.1 date < 1980.7.1", bypass="date > 1980.6.30",
  reward=J(opinion("USA", "medium_increase"), opinion("SOV", "medium_decrease"), kl(-3)))
F("world_cup_1990", "olympic_boycott", 0, 1, cost=2, avail="date > 1990.6.1 date < 1990.8.1", bypass="date > 1990.7.31",
  reward=J(core("bonn", stab=0.03)))
F("expo_2000", "world_cup_1990", 0, 1, cost=2, avail="date > 1995.1.1",
  reward=J(state_build(NDS, "offices"), state_mod(NDS, "expo"), core("bonn", stab=0.01)))
F("development_ministry", "cultural_diplomacy", 0, 1, cost=3, icon="trade_europe",
  reward=J(f"add_ideas = {P}_idea_bmz", core("welt", cap=1, eff=0.05)))
F("party_foundations", "development_ministry", 0, 1, cost=3, icon="socdem",
  reward=J(unlock(f"{P}_foundations_unlocked", "party foundation campaigns (Imperia political support) in Portugal, Spain, Greece, Chile and Nicaragua"), core("welt", support=0.1)))
F("brandt_commission", "party_foundations", 0, 1, cost=3, avail="date > 1977.9.1", icon="un",
  reward=J(f"add_timed_idea = {{ idea = {P}_idea_north_south days = 1825 }}", core("welt", eff=0.05), infl("RAJ", 2), infl("BRA", 2)))
F("africa_development", "development_ministry", 1, 1, cost=3, icon="trade_europe",
  reward=J(f"add_timed_idea = {{ idea = {P}_idea_development_partner days = 3650 }}", core("welt", cap=1), infl("TNZ", 3), infl("KEN", 3), infl("SEN", 2)))
F("brazil_nuclear_deal", "africa_development", 1, 1, cost=3, avail="date > 1974.6.1", icon="nuclear_plant",
  reward=J(infl("BRA", 5), opinion("BRA", "large_increase"), opinion("USA", "medium_decrease"), core("welt", market=0.03)))
F("middle_east_balance", "brandt_commission", 1, 1, cost=3, icon="oil",
  reward=J(infl("EGY", 3), infl("JOR", 3), infl("SAU", 2), core("energie", fossil=-0.02)))
F("israel_relations", "middle_east_balance", -1, 1, cost=2, icon="diplomacy",
  reward=J(opinion("ISR", "large_increase", mutual=True), infl("ISR", 3), core("west", opinion=0.03)))
F("critical_dialogue", "middle_east_balance", 1, 1, cost=2, avail="date > 1990.1.1",
  reward=J(infl("PER", 3), opinion("USA", "small_decrease"), core("welt", market=0.03)))
F("un_security_council", "brandt_commission", -1, 1, cost=3, pre=[["brandt_commission"]], icon="un",
  avail=f"has_country_flag = {P}_un_member",
  reward=J(f"add_timed_idea = {{ idea = {P}_idea_unsc_member days = 730 }}", core("welt", support=0.05)))
