# IMPERIA CW — Cold War: Soviet Union 1970 content generator.
# COLDWAR | Socialist Emulation of the Union republics (Enes, 19.10.2026), shown in the Politburo dossier (cw_pbgui.py):
#   - every month Moscow ranks the republics by growth, industry, output per head and plan targets;
#   - every quarter the four Transferable Red Banners pass to the leaders of the table (on a tie the holder keeps its banner);
#   - every January the best republic becomes the Pride of the Union; a second title in a row makes it a Hero of Socialist Labour
#     (and its First Secretary gets the Gold Star), three titles in one Five-Year Plan bring the Order of Lenin; the last one lags behind;
#   - Moscow may favour one republic a year (roleplay: everybody sees it);
#   - pripiski also polish a republic's emulation figures - only the republic knows, until the lie is uncovered;
#   - the Spartakiad of the Peoples of the USSR (1971, 1975, 1979, 1983, 1986).
# Multiplayer rule: ideas, traits and political power reach a country only through an event in its own scope. The effects in this
# file keep the books (variables and flags) and send those events.
from cw_common import *
import cw_effects as E
import cw_events as EV
import cw_decisions as D
import cw_misc as M

PB = f"{PFX}pb_"
SCRIPTED_LOC = []       # defined_text blocks (written with the dossier's scripted localisation)
EFFECTS = []            # scripted effect lines (written with the dossier's effects)
IN_UNION = f"{PFX}is_union_republic = yes"
OUT_OF_UNION = [f"NOT = {{ {IN_UNION} }}"]

# values Enes may want to tune after tests
INFL_GROWTH = 1.5       # pripiski: growth points added to the reported quarterly growth
INFL_FACTOR = 1.1       # pripiski: factories and output per head as reported
FAVOUR_PLACES = 3       # Moscow's favourite counts this many places better in the January judgement
FAVOUR_COST, FAVOUR_PP, FAVOUR_OPINION = 50, 25, -20
PRIDE_DAYS, LAG_DAYS = 365, 365


def dt(name, entries, fallback):
    """defined_text; entries = [(trigger lines, localization key)], fallback = key."""
    L_ = ["defined_text = {", f"name = {name}"]
    for trig, key in entries:
        L_ += ["text = {", "trigger = {"] + list(trig) + ["}", f"localization_key = {key}", "}"]
    L_ += ["text = {", f"localization_key = {fallback}", "}", "}"]
    SCRIPTED_LOC.extend(L_)


def loc(key, text):
    LOC[key] = text
    return key


def tt(key, text):
    return f"custom_effect_tooltip = {loc(f'{PB}{key}_tt', text)}"


def drop(idea):
    return f"if = {{ limit = {{ has_idea = {idea} }} remove_ideas = {idea} }}"


def tidea(idea, days):
    """a timed idea that starts again at its full duration if the country already has it"""
    return [f"if = {{ limit = {{ has_idea = {idea} }} hidden_effect = {{ remove_ideas = {idea} }} }}", f"add_timed_idea = {{ idea = {idea} days = {days} }}"]


def idea(key, name, pic, mods, desc, cancel=None):
    iid = PFX + key
    E.R.ideas[iid] = dict(name=name, mods=mods, days=0, desc=desc, cancel=cancel)
    M.PIC[key] = pic
    return iid


def pct(v):
    return f"{'+' if v > 0 else ''}{round(v * 100)}%"


def mods_txt(mods):
    return ", ".join(f"{M_EN(m)} {('§G' if (v > 0) != (m == 'consumer_goods_factor') else '§R')}{pct(v)}§!" for m, v in mods)


def M_EN(m):
    return {"production_speed_buildings_factor": "construction speed", "industrial_capacity_factory": "factory output",
            "consumer_goods_factor": "consumer goods", "stability_factor": "stability", "political_power_factor": "political power gain",
            "war_support_factor": "war support"}[m]


# ================================================================ the table
EMU = {  # key -> (row label, value lines (republic scope), value text of the leader, what is measured)
    "growth": ("Economic growth", [f"set_variable = {{ {PB}v_growth = last_quarter_gdp_growth_rate }}", f"multiply_variable = {{ {PB}v_growth = 100 }}"],
               "[?global.COLDWAR_SOV_pb_top_growth_val|+1]%", "GDP growth in the last quarter"),
    "industry": ("Industry", [f"set_variable = {{ {PB}v_industry = industrial_complex_total }}", f"add_to_variable = {{ {PB}v_industry = military_factory_total }}"],
                 "[?global.COLDWAR_SOV_pb_top_industry_val|0] factories", "civilian and military factories"),
    "output": ("Output per head", [f"set_variable = {{ {PB}v_output = gdp_per_capita }}"],
               "$[?global.COLDWAR_SOV_pb_top_output_val|2]k", "GDP per head"),
    "plan": ("Plan targets", [f"set_variable = {{ {PB}v_plan = 0 }}",
                              f"if = {{ limit = {{ check_variable = {{ COLDWAR_UNI_fp_plan = {PB}judge_plan }} }} set_variable = {{ {PB}v_plan = COLDWAR_UNI_fulfilled_plan }} }}"],
             "[?global.COLDWAR_SOV_pb_top_plan_val|0] fulfilled", "annual targets of the Union Plan fulfilled in this Five-Year Plan"),
}
KEYS = list(EMU)

EFFECTS += ["# ==== Socialist Emulation (cw_emulation.py) ======================================================",
            "# the monthly table: Moscow ranks the republics by the figures they report (THIS = any scope;",
            f"# temp {PB}judge_plan = the Five-Year Plan whose targets count, the running one unless the January judgement passes another)",
            f"{PB}update_board = {{", "hidden_effect = {",
            f"if = {{ limit = {{ check_variable = {{ {PB}judge_plan = 0 }} }} set_temp_variable = {{ {PB}judge_plan = global.{PFX}plan }} }}",
            f"set_variable = {{ global.{PB}ssr_count = 0 }}",
            "# a republic that has left the Union leaves the table",
            f"every_country = {{ limit = {{ has_variable = {PB}rank_growth NOT = {{ {IN_UNION} }} }} " + " ".join(f"clear_variable = {PB}rank_{k}" for k in KEYS) + " }",
            "every_country = {", f"limit = {{ {IN_UNION} }}", f"add_to_variable = {{ global.{PB}ssr_count = 1 }}"]
for _k in KEYS:
    EFFECTS += EMU[_k][1]
EFFECTS += ["# pripiski: the republic's statisticians polish the figures Moscow reads - only the republic itself knows",
            "if = {", f"limit = {{ has_country_flag = {PB}inflated }}", f"add_to_variable = {{ {PB}v_growth = {INFL_GROWTH} }}",
            f"multiply_variable = {{ {PB}v_industry = {INFL_FACTOR} }}", f"multiply_variable = {{ {PB}v_output = {INFL_FACTOR} }}", "}",
            "# disqualified for false figures: last in every column",
            "if = {", f"limit = {{ has_country_flag = {PB}disqualified }}"] + [f"set_variable = {{ {PB}v_{k} = -1000 }}" for k in KEYS] + ["}", "}"]
for _k in KEYS:
    v = f"{PB}v_{_k}"
    EFFECTS += [f"set_variable = {{ global.{PB}top_{_k}_val = -1000 }}", f"set_variable = {{ global.{PB}top_{_k} = SOV }}",
                "every_country = {", f"limit = {{ {IN_UNION} }}",
                f"set_temp_variable = {{ pb_my = {v} }}", "set_temp_variable = { pb_rank = 1 }",
                "every_country = {", f"limit = {{ {IN_UNION} check_variable = {{ {v} > pb_my }} }}", "add_to_temp_variable = { pb_rank = 1 }", "}",
                f"set_variable = {{ {PB}rank_{_k} = pb_rank }}",
                f"if = {{ limit = {{ check_variable = {{ {PB}rank_{_k} = 1 }} }} set_variable = {{ global.{PB}top_{_k} = THIS }} set_variable = {{ global.{PB}top_{_k}_val = {v} }} }}",
                "}"]
EFFECTS += ["}", "}", ""]

# ================================================================ the four Transferable Red Banners (every quarter)
BANNERS = {   # key -> (short name, idea picture, modifiers; the Socialist Emulation focus of the Union tree doubles them)
    "growth": ("Growth", "sov_economic_all_idea", [("production_speed_buildings_factor", 0.05)]),
    "industry": ("Industry", "sov_planned_economy_idea", [("industrial_capacity_factory", 0.03)]),
    "output": ("Output per Head", "sov_invest_ben", [("consumer_goods_factor", -0.02)]),
    "plan": ("the Plan", "sov_five_year_idea", [("stability_factor", 0.03), ("political_power_factor", 0.05)]),
}
BANNER_IDEA = {}
for _k, (_n, _pic, _mods) in BANNERS.items():
    _d = (f"Every quarter the Central Committee hands its Transferable Red Banner for {EMU[_k][3]} to the republic that leads the "
          f"Socialist Emulation. This quarter it hangs in our House of Government.")
    BANNER_IDEA[_k] = (idea(f"banner_{_k}", f"Red Banner: {_n}", _pic, _mods, _d, cancel=OUT_OF_UNION),
                       idea(f"banner_{_k}_2", f"Red Banner: {_n} (Socialist Emulation)", _pic, [(m, round(v * 2, 4)) for m, v in _mods], _d, cancel=OUT_OF_UNION))
EV_GAIN = {k: 162 + i for i, k in enumerate(KEYS)}
EV_LOSE = {k: 166 + i for i, k in enumerate(KEYS)}
EV_TIER = 179

EFFECTS += ["# on_monthly_SOV: the dossier, the table, and every third month the Red Banners",
            f"{PB}monthly = {{", f"{PB}update_seats = yes", f"{PB}update_board = yes", "hidden_effect = {",
            f"add_to_variable = {{ global.{PB}month = 1 }}", f"set_temp_variable = {{ {PB}q = global.{PB}month }}", f"modulo_temp_variable = {{ {PB}q = 3 }}",
            f"if = {{ limit = {{ check_variable = {{ {PB}q = 0 }} check_variable = {{ global.{PB}ssr_count > 1 }} }} {PB}award_banners = yes }}",
            "}", "}", "",
            "# every quarter (SOV scope): each banner goes to the leader of its column; the holder keeps it on a tie, nobody wins it with nothing",
            f"{PB}award_banners = {{", "hidden_effect = {"]
for _k in KEYS:
    EFFECTS += [f"# {BANNERS[_k][0]}",
                f"every_country = {{ limit = {{ has_country_flag = {PB}banner_{_k} NOT = {{ {IN_UNION} }} }} country_event = {{ id = {NS}.{EV_LOSE[_k]} }} }}",
                "if = {", "limit = {", f"check_variable = {{ global.{PB}top_{_k}_val > 0 }}",
                f"NOT = {{ any_country = {{ has_country_flag = {PB}banner_{_k} {IN_UNION} check_variable = {{ {PB}rank_{_k} = 1 }} }} }}", "}",
                f"every_country = {{ limit = {{ has_country_flag = {PB}banner_{_k} {IN_UNION} }} country_event = {{ id = {NS}.{EV_LOSE[_k]} }} }}",
                f"var:global.{PB}top_{_k} = {{ country_event = {{ id = {NS}.{EV_GAIN[_k]} }} }}", "}"]
EFFECTS += ["# the Socialist Emulation focus (Union tree) doubles the banners: a holder from before the focus carries the new rank from this quarter",
            "if = {", "limit = { has_global_flag = COLDWAR_UNI_emulation }", "every_country = {",
            "limit = { OR = { " + " ".join(f"AND = {{ has_country_flag = {PB}banner_{k} NOT = {{ has_idea = {BANNER_IDEA[k][1]} }} }}" for k in KEYS) + " } }",
            f"country_event = {{ id = {NS}.{EV_TIER} }}", "}", "}", "}", "}", ""]


def banner_rank(k):
    t1, t2 = BANNER_IDEA[k]
    return [f"if = {{ limit = {{ has_global_flag = COLDWAR_UNI_emulation }} {drop(t1)} add_ideas = {t2} }}",
            f"else = {{ {drop(t2)} add_ideas = {t1} }}"]


for _k in KEYS:
    _n = BANNERS[_k][0]
    EV.ev(EV_GAIN[_k], "congress", f"The Red Banner for {_n}",
          f"The Central Committee has reviewed the Socialist Emulation of the last quarter. In {EMU[_k][3]} no republic stands higher than ours, "
          f"and the Transferable Red Banner for {_n.lower() if _n != 'the Plan' else 'the plan'} passes to our republic. The workers' delegation brings it from Moscow "
          f"tomorrow; the banner hangs in our House of Government until another republic takes it from us.\n\n"
          f"Bonus while we hold it: {mods_txt(BANNERS[_k][2])}, twice as much once the Union has adopted §YSocialist Emulation§!.",
          [EV.o("We will not give it up.", banner_rank(_k))],
          immediate=[f"set_country_flag = {PB}banner_{_k}", f"set_variable = {{ global.{PB}banner_{_k} = THIS }}"])
    EV.ev(EV_LOSE[_k], "congress", f"The Red Banner for {_n} Passes On", "The banner passes to another republic.", [EV.o("Pass it on.")], hidden=True,
          immediate=[f"clr_country_flag = {PB}banner_{_k}", drop(BANNER_IDEA[_k][0]), drop(BANNER_IDEA[_k][1])])
EV.ev(EV_TIER, "congress", "Socialist Emulation", "The banners carry their new rank.", [EV.o("Raise them.")], hidden=True,
      immediate=[f"if = {{ limit = {{ has_country_flag = {PB}banner_{k} }} {' '.join(banner_rank(k))} }}" for k in KEYS])

# ================================================================ the January judgement: Pride, Hero, Order of Lenin, Lagging Behind
PRIDE_MODS = [("stability_factor", 0.05), ("political_power_factor", 0.10), ("production_speed_buildings_factor", 0.10), ("consumer_goods_factor", -0.05)]
HERO_MODS = [("stability_factor", 0.05), ("political_power_factor", 0.10), ("production_speed_buildings_factor", 0.15), ("consumer_goods_factor", -0.05),
             ("industrial_capacity_factory", 0.05)]
ORDER_MODS = [("stability_factor", 0.03), ("political_power_factor", 0.05), ("production_speed_buildings_factor", 0.05), ("industrial_capacity_factory", 0.03)]
LAG_MODS = [("stability_factor", -0.03), ("political_power_factor", -0.05)]
PRIDE = idea("pride_of_the_union", "Pride of the Union", "national_unity", PRIDE_MODS,
             "No republic served the Union better last year. Pravda prints our First Secretary's portrait, and every factory wants to keep the title.")
HERO = idea("hero_of_socialist_labour", "Hero of Socialist Labour", "SOV_stakhanovite_movement", HERO_MODS,
            "Two years in a row the best republic of the Union: our First Secretary wears the Gold Star of the Hammer and Sickle.")
ORDER = idea("order_of_lenin", "The Order of Lenin", "vladimir_lenin", ORDER_MODS,
             "Three times the best republic in one Five-Year Plan: the Order of Lenin is pinned to our republic's banner for as long as we remain in the Union.",
             cancel=OUT_OF_UNION)
LAG = idea("lagging_behind", "Lagging Behind", "stagnation", LAG_MODS,
           "Last in the Socialist Emulation. Pravda names us among the republics that lag behind, and Gosplan's inspectors read our figures twice.")
GOLD_STAR = f"{PFX}gold_star"
M.TRAIT_MODS["gold_star"] = [("political_power_factor", 0.05), ("stability_factor", 0.02)]
M.TRAITS[GOLD_STAR] = "Hero of Socialist Labour"
JUDGE = [("1971.6.1", 9), ("1976.6.1", 10), ("1981.6.1", 11), ("1986.6.1", 12)]   # the Five-Year Plan the judged year belonged to

EFFECTS += ["# the January session (SOV scope): the past year is judged by the sum of the four ranks; Moscow's favourite counts "
            f"{FAVOUR_PLACES} places better, a disqualified republic cannot win",
            f"{PB}award_pride = {{", f"set_temp_variable = {{ {PB}judge_plan = 8 }}"] + \
           [f"if = {{ limit = {{ date > {d} }} set_temp_variable = {{ {PB}judge_plan = {n} }} }}" for d, n in JUDGE] + \
           [f"{PB}update_board = yes", "if = {", f"limit = {{ check_variable = {{ global.{PB}ssr_count > 1 }} }}", "hidden_effect = {",
            f"clr_global_flag = {PB}order_new", f"clr_global_flag = {PB}lagging_named", f"set_temp_variable = {{ {PB}best = 1000 }}",
            "every_country = {", f"limit = {{ {IN_UNION} }}",
            f"set_variable = {{ {PB}score = {PB}rank_growth }}"] + [f"add_to_variable = {{ {PB}score = {PB}rank_{k} }}" for k in KEYS[1:]] + \
           [f"if = {{ limit = {{ has_country_flag = {PB}favoured }} add_to_variable = {{ {PB}score = -{FAVOUR_PLACES} }} }}",
            f"if = {{ limit = {{ NOT = {{ has_country_flag = {PB}disqualified }} check_variable = {{ {PB}score < {PB}best }} }} "
            f"set_temp_variable = {{ {PB}best = {PB}score }} set_variable = {{ global.{PB}pride = THIS }} }}", "}",
            "if = {", f"limit = {{ check_variable = {{ {PB}best < 1000 }} }}",
            "# a title in a row: last January's winner defends it",
            f"var:global.{PB}pride = {{", f"set_country_flag = {PB}new_pride",
            f"if = {{ limit = {{ has_country_flag = {PB}won_last }} add_to_variable = {{ {PB}streak = 1 }} }}", f"else = {{ set_variable = {{ {PB}streak = 1 }} }}", "}",
            f"every_country = {{ limit = {{ has_country_flag = {PB}won_last }} clr_country_flag = {PB}won_last }}",
            f"var:global.{PB}pride = {{", f"set_country_flag = {PB}won_last",
            "# three titles in one Five-Year Plan: the Order of Lenin",
            f"if = {{ limit = {{ NOT = {{ check_variable = {{ {PB}title_plan = {PB}judge_plan }} }} }} set_variable = {{ {PB}title_plan = {PB}judge_plan }} set_variable = {{ {PB}titles = 0 }} }}",
            f"add_to_variable = {{ {PB}titles = 1 }}",
            f"if = {{ limit = {{ check_variable = {{ {PB}titles > 2 }} NOT = {{ has_idea = {ORDER} }} }} set_country_flag = {PB}order_due set_global_flag = {PB}order_new }}",
            f"country_event = {{ id = {NS}.160 }}", "}",
            f"set_global_flag = {PB}pride_awarded",
            "# the last place: not the winner, not Moscow's favourite, not a republic already disqualified",
            f"set_temp_variable = {{ {PB}worst = -1 }}",
            "if = {", f"limit = {{ check_variable = {{ global.{PB}ssr_count > 2 }} }}", "every_country = {",
            f"limit = {{ {IN_UNION} NOT = {{ has_country_flag = {PB}new_pride }} NOT = {{ has_country_flag = {PB}favoured }} NOT = {{ has_country_flag = {PB}disqualified }} }}",
            f"if = {{ limit = {{ check_variable = {{ {PB}score > {PB}worst }} }} set_temp_variable = {{ {PB}worst = {PB}score }} set_variable = {{ global.{PB}lagging = THIS }} }}",
            "}",
            f"if = {{ limit = {{ check_variable = {{ {PB}worst > -1 }} }} set_global_flag = {PB}lagging_named var:global.{PB}lagging = {{ country_event = {{ id = {NS}.161 }} }} }}",
            "}",
            f"every_country = {{ limit = {{ has_country_flag = {PB}new_pride }} clr_country_flag = {PB}new_pride }}",
            "every_country = {", f"limit = {{ OR = {{ original_tag = SOV {IN_UNION} }} }}", f"news_event = {{ id = {NS}.38 hours = 12 }}", "}",
            "}", "}", "}", "}", ""]

# the winner (own scope)
EFFECTS += ["# THIS = the winner of the January judgement (event COLDWAR_SOV.160)",
            f"{PB}receive_pride = {{", "if = {", f"limit = {{ check_variable = {{ {PB}streak > 1 }} }}", drop(PRIDE)] + tidea(HERO, PRIDE_DAYS) + [
            f"if = {{ limit = {{ NOT = {{ has_country_leader_with_trait = {GOLD_STAR} }} }} add_country_leader_trait = {GOLD_STAR} }}", "}",
            "else = {", drop(HERO)] + tidea(PRIDE, PRIDE_DAYS) + ["}",
            f"if = {{ limit = {{ has_country_flag = {PB}order_due }} hidden_effect = {{ clr_country_flag = {PB}order_due }} add_ideas = {ORDER} }}", "}", ""]
dt(f"{PB}GetAwardTitle", [([f"check_variable = {{ {PB}streak > 1 }}"], loc(f"{PB}award_title_hero", "Hero of Socialist Labour"))],
   loc(f"{PB}award_title_pride", "The Pride of the Union"))
dt(f"{PB}GetAwardLine", [([f"check_variable = {{ {PB}streak > 1 }}"],
                          loc(f"{PB}award_line_hero", "For the second year running we lead the Union. In the Sverdlov Hall the Chairman of the Presidium pins the "
                                                      "Gold Star of the Hammer and Sickle on our First Secretary: he is a §YHero of Socialist Labour§!, and so, "
                                                      "for a year, is our republic."))],
   loc(f"{PB}award_line_pride", "For a year our republic carries the title §YPride of the Union§!: Pravda prints our First Secretary's portrait, "
                                "and every factory wants to keep the title."))
dt(f"{PB}GetOrderLine", [([f"has_country_flag = {PB}order_due"],
                          loc(f"{PB}order_line", "\\n\\nIt is our third title in this Five-Year Plan: the republic is decorated with the §YOrder of Lenin§!, "
                                                 "for as long as it remains in the Union."))], loc(f"{PB}empty", ""))
EV.ev(160, "congress", f"[{PB}GetAwardTitle]",
      "The Central Committee has judged the Socialist Emulation of the past year: in growth, industry, output per head and the plan taken together, "
      f"no republic stood higher than ours. [{PB}GetAwardLine][{PB}GetOrderLine]",
      [EV.o("Glory to the workers of our republic!", [f"{PB}receive_pride = yes"])])
EV.ev(161, "factory", "Lagging Behind",
      "The Central Committee has judged the Socialist Emulation of the past year, and our republic stands at the bottom of the table. Pravda names us "
      "among those who \"lag behind\". Gosplan's inspectors will read our figures twice this year.",
      [EV.o("We will catch up.", tidea(LAG, LAG_DAYS) + [tt("lagging", "For a year an investigation of our republic is §R10%§! more likely to find something.")])])

# the news of the judgement (every republic and Moscow; scripted lines read the global holders)
dt(f"{PB}GetNewsTitleLine", [([f"var:global.{PB}pride = {{ check_variable = {{ {PB}streak > 1 }} }}"],
                              loc(f"{PB}news_hero", "For the second year running it leads the Union: its First Secretary, [?global.COLDWAR_SOV_pb_pride.GetLeader], "
                                                    "receives the Gold Star of the Hammer and Sickle as a §YHero of Socialist Labour§!."))],
   loc(f"{PB}news_pride", "Its First Secretary, [?global.COLDWAR_SOV_pb_pride.GetLeader], received the congratulations of the Politburo in the Kremlin. "
                          "For a year the republic carries the title §YPride of the Union§!."))
dt(f"{PB}GetNewsOrderLine", [([f"has_global_flag = {PB}order_new"],
                              loc(f"{PB}news_order", "\\n\\nWith its third title in this Five-Year Plan the republic is decorated with the §YOrder of Lenin§!."))],
   f"{PB}empty")
dt(f"{PB}GetNewsLagLine", [([f"has_global_flag = {PB}lagging_named"],
                            loc(f"{PB}news_lag", "\\n\\nAt the bottom of the table Pravda names §R[?global.COLDWAR_SOV_pb_lagging.GetNameDef]§!: "
                                                 "the republic is lagging behind."))], f"{PB}empty")
EV.ev(38, "speech", "Pravda: The Pride of the Union",
      "Moscow, January. The Central Committee has reviewed the Socialist Emulation of the Union republics in the past year. Growth, industry, "
      "output per head and the fulfilment of the plan were weighed against each other, and one republic stood above the rest: "
      f"[?global.COLDWAR_SOV_pb_pride.GetNameDef]. [{PB}GetNewsTitleLine][{PB}GetNewsOrderLine][{PB}GetNewsLagLine]\n\n"
      "The other First Secretaries applauded. Several of them have already asked Gosplan for their figures.",
      [EV.o("Glory to the workers of the republic!")], kind="news")

# ================================================================ disqualification (pripiski uncovered)
EFFECTS += ["# THIS = a republic whose false figures are uncovered (COLDWAR_UNI_pripiski_exposed, COLDWAR_SOV_investigate_republic)",
            f"{PB}disqualify = {{",
            tt("disqualified", "The republic is §Rdisqualified§! from the Socialist Emulation for a year: last in every column, and its "
                               "Pride of the Union, Red Banners and Order of Lenin are withdrawn."),
            "hidden_effect = {", f"clr_country_flag = {PB}inflated", f"set_country_flag = {{ flag = {PB}disqualified days = 365 }}",
            f"country_event = {{ id = {NS}.178 }}", "}", "}", ""]
EV.ev(178, "trial", "Disqualified", "Our honours are withdrawn.", [EV.o("Hand them back.")], hidden=True,
      immediate=[drop(PRIDE), drop(HERO), drop(ORDER)] +
                [f"if = {{ limit = {{ has_country_flag = {PB}banner_{k} }} clr_country_flag = {PB}banner_{k} {drop(BANNER_IDEA[k][0])} {drop(BANNER_IDEA[k][1])} }}" for k in KEYS] +
                [f"clr_country_flag = {PB}won_last", f"clr_country_flag = {PB}order_due", f"set_variable = {{ {PB}streak = 0 }}", f"set_variable = {{ {PB}titles = 0 }}"])

# ================================================================ pripiski: the private confirmation (the decision is in cw_decisions.py)
PRIPISKI_TT = ("Our statisticians also polish the figures Moscow reads in the §YSocialist Emulation§! for a year (growth §Y+1.5§! points, "
               "factories and output per head §Y+10%§!). Nobody outside our leadership knows. If the lie is uncovered, we are "
               "§Rdisqualified§! from the emulation for a year and lose its honours.")
loc(f"{PB}pripiski_emu", PRIPISKI_TT)      # shown in the tooltip of "Report the Plan Overfulfilled" (cw_decisions.py)
EV.ev(16, "factory", "108 Percent",
      "The figures have gone to Moscow: 108 percent of the plan. The cotton, the grain and the meat are all there - on paper. Pravda will print them, "
      "and the Socialist Emulation will rank us by them.\n\nOnly a handful of men know the truth: the First Secretary, the chairman of our "
      "statistics board and two heads of department. The inspectors of the People's Control and the KGB must never find the gap.",
      [EV.o("Who will count the cotton?")])

# ================================================================ Moscow's favourite (one a year; everybody sees it)
FAV_TT = (f"Moscow favours one republic a year ({FAVOUR_COST} political power, Union cohesion §R-1§!): the republic gains §G{FAVOUR_PP}§! political power "
          f"and counts §Y{FAVOUR_PLACES}§! places better in the January judgement of the Socialist Emulation; the other republics resent it "
          f"(their opinion of it §R{FAVOUR_OPINION}§!).")
D.dec(f"{PFX}politburo_seats_category", "pb_favour_republic", "Favour [FROM.GetNameDef]",
      "A word from the General Secretary, a delegation in Pravda, a new factory in the right oblast: everybody understands which republic Moscow prefers this year.",
      "GFX_decision_russia_star",
      [f"hidden_effect = {{ set_global_flag = {{ flag = {PB}favour_active days = 365 }} set_variable = {{ global.{PB}favourite = FROM }} }}"] + E.cohesion(-1) +
      [D.tt("pb_favour", FAV_TT), f"FROM = {{ country_event = {{ id = {NS}.176 days = 1 }} }}"],
      cost=FAVOUR_COST, targets=SSR, target_trigger=[IN_UNION, f"NOT = {{ has_country_flag = {PB}disqualified }}"],
      available=D.ttrig("pb_favour_free", "Moscow has not favoured another republic in the last year.", [f"NOT = {{ has_global_flag = {PB}favour_active }}"]),
      ai="base = 0")
E.R.opinions[f"{PFX}moscows_favourite"] = FAVOUR_OPINION
LOC[f"{PFX}moscows_favourite"] = "Moscow's Favourite"
EV.ev(176, "kremlin", "Moscow's Favourite",
      "The General Secretary has let it be known: this year our republic is the example for the Union. Pravda prints our figures on its front page, "
      "Gosplan answers our letters at once - and every other First Secretary has noticed.",
      [EV.o("Moscow knows its friends.", [f"add_political_power = {FAVOUR_PP}",
                                          tt("favoured", f"For a year we count §Y{FAVOUR_PLACES}§! places better in the January judgement of the Socialist Emulation.")])],
      immediate=[f"set_country_flag = {{ flag = {PB}favoured days = 365 }}",
                 "every_country = {", f"limit = {{ OR = {{ original_tag = SOV {IN_UNION} }} NOT = {{ has_country_flag = {PB}favoured }} }}",
                 f"news_event = {{ id = {NS}.177 hours = 6 }}", "}"])
EV.ev(177, "kremlin", "Moscow Has a Favourite",
      "Pravda calls [?global.COLDWAR_SOV_pb_favourite.GetNameDef] \"an example for the whole Union\", and the General Secretary has praised its First "
      "Secretary by name. For a year Moscow's favourite counts three places better in the Socialist Emulation.",
      [EV.o("Some republics are more equal than others.",
            ["hidden_effect = {", f"var:global.{PB}favourite = {{ reverse_add_opinion_modifier = {{ target = PREV modifier = {PFX}moscows_favourite }} }}", "}",
             tt("favourite_resent", f"Our opinion of [?global.COLDWAR_SOV_pb_favourite.GetNameDef]: §R{FAVOUR_OPINION}§!.")], trig=[IN_UNION]),
       EV.o("The republics will understand.", trig=["original_tag = SOV"])], kind="news")

# ================================================================ the Spartakiad of the Peoples of the USSR
SPART = [(5, "V", 1971, "1971.7.24"), (6, "VI", 1975, "1975.7.12"), (7, "VII", 1979, "1979.7.21"), (8, "VIII", 1983, "1983.6.18"), (9, "IX", 1986, "1986.7.12")]
SP_PREP = 90
SP_TRAIN, SP_STADIUM, SP_SPECIAL = 3, 4, 6
SP_GDP = 0.0015
CHAMP = idea("spartakiad_champions", "Champions of the Spartakiad", "olympics_idea",
             [("stability_factor", 0.03), ("war_support_factor", 0.05), ("political_power_factor", 0.05)],
             "Our athletes won the Spartakiad of the Peoples of the USSR. The medals are on show in every school of the republic.")
DOPING = idea("doping_scandal", "A Doping Scandal", "arm_sport", [("stability_factor", -0.05), ("political_power_factor", -0.05)],
              "The doctors of our team have been caught. The sports committee in Moscow speaks of a disgrace for Soviet sport.")
BASE_T = EV.BASE_T

SP_TT = loc(f"{PB}sp_tt", f"§YThe Spartakiad of the Peoples of the USSR§! (1971, 1975, 1979, 1983, 1986): {SP_PREP} days before the games every republic "
                          f"prepares its team in the decisions of The Politburo of the CPSU. The result weighs the preparation, the size of the republic and "
                          f"luck. Gold: §YChampions of the Spartakiad§! for two years (stability +3%, war support +5%, political power gain +5%); "
                          f"silver: 50 political power; bronze: 25 political power. The games strengthen the Union (cohesion +2).")
dt(f"{PB}GetSpEdition", [([f"check_variable = {{ global.{PB}sp_edition = {n} }}"], loc(f"{PB}sp_ed_{n}", f"{r} Spartakiad of the Peoples of the USSR ({y})"))
                         for n, r, y, d in SPART], loc(f"{PB}sp_ed_none", "the Spartakiad of the Peoples of the USSR"))
_spl = []
for n, r, y, d in SPART:
    _spl.append(([f"has_global_flag = {PB}sp_open", f"check_variable = {{ global.{PB}sp_edition = {n} }}", IN_UNION],
                 loc(f"{PB}sp_prep_own_{n}", f"{r} Spartakiad, summer {y}: §Ypreparations§! - our team [?COLDWAR_SOV_pb_sp_pts|0] points")))
    _spl.append(([f"has_global_flag = {PB}sp_open", f"check_variable = {{ global.{PB}sp_edition = {n} }}"],
                 loc(f"{PB}sp_prep_{n}", f"{r} Spartakiad, summer {y}: the republics §Yprepare their teams§!")))
    _spl.append(([f"has_global_flag = {PB}sp_held", f"check_variable = {{ global.{PB}sp_edition = {n} }}"],
                 loc(f"{PB}sp_held_{n}", f"{r} Spartakiad {y}: champions §Y[?global.COLDWAR_SOV_pb_sp_gold.GetName]§!")))
dt(f"{PB}GetSpartakiad", _spl, loc(f"{PB}sp_next", "V Spartakiad of the Peoples of the USSR: summer 1971"))

PREP_OPEN = [f"has_global_flag = {PB}sp_open"]
for i, (n, r, y, d) in enumerate(SPART):
    EV.ev(180 + i, "olympics", f"The {r} Spartakiad Is Announced", "Preparations open.", [EV.o("Open.")], hidden=True, once=True, mtth=1,
          trigger=BASE_T + [f"date > {EV.minus(d, SP_PREP)}", f"date < {d}"],   # a window: a late start skips an edition instead of stacking it
          immediate=[f"set_variable = {{ global.{PB}sp_edition = {n} }}", f"set_global_flag = {PB}sp_open", f"clr_global_flag = {PB}sp_held",
                     f"every_country = {{ limit = {{ has_variable = {PB}sp_pts }} clear_variable = {PB}sp_pts }}",
                     f"every_country = {{ limit = {{ OR = {{ has_country_flag = {PB}sp_trained has_country_flag = {PB}sp_built has_country_flag = {PB}sp_special }} }} "
                     f"clr_country_flag = {PB}sp_trained clr_country_flag = {PB}sp_built clr_country_flag = {PB}sp_special }}",
                     "every_country = {", f"limit = {{ OR = {{ original_tag = SOV {IN_UNION} }} }}", f"news_event = {{ id = {NS}.170 hours = 6 }}", "}"])
    medal = []
    for m, evn in (("gold", 172), ("silver", 174), ("bronze", 175)):
        medal += [f"set_temp_variable = {{ {PB}top = -1 }}", f"clear_variable = global.{PB}sp_{m}",
                  "every_country = {", f"limit = {{ {IN_UNION} NOT = {{ has_country_flag = {PB}sp_medal }} }}",
                  f"if = {{ limit = {{ check_variable = {{ {PB}sp_score > {PB}top }} }} set_temp_variable = {{ {PB}top = {PB}sp_score }} set_variable = {{ global.{PB}sp_{m} = THIS }} }}",
                  "}",
                  f"if = {{ limit = {{ check_variable = {{ {PB}top > -1 }} }} var:global.{PB}sp_{m} = {{ set_country_flag = {PB}sp_medal country_event = {{ id = {NS}.{evn} }} }} }}"]
    EV.ev(185 + i, "olympics", f"The {r} Spartakiad", "The games are held.", [EV.o("Hold them.")], hidden=True, once=True, mtth=1,
          trigger=BASE_T + [f"date > {d}", f"check_variable = {{ global.{PB}sp_edition = {n} }}", f"has_global_flag = {PB}sp_open"],
          immediate=[f"clr_global_flag = {PB}sp_open", f"set_variable = {{ global.{PB}sp_edition = {n} }}",
                     "every_country = {", f"limit = {{ {IN_UNION} }}", "COLDWAR_UNI_weight_of = yes",
                     f"set_variable = {{ {PB}sp_score = COLDWAR_UNI_w }}", f"multiply_variable = {{ {PB}sp_score = 2 }}",
                     f"add_to_variable = {{ {PB}sp_score = {PB}sp_pts }}",
                     f"set_temp_variable_to_random = {{ var = {PB}luck min = 0 max = 7 }}", f"add_to_variable = {{ {PB}sp_score = {PB}luck }}", "}"] +
                    medal +
                    [f"every_country = {{ limit = {{ has_country_flag = {PB}sp_medal }} clr_country_flag = {PB}sp_medal }}",
                     f"set_global_flag = {PB}sp_held"] + E.cohesion(2) +
                    ["every_country = {", f"limit = {{ OR = {{ original_tag = SOV {IN_UNION} }} }}", f"news_event = {{ id = {NS}.171 hours = 6 }}", "}"])

EV.ev(170, "olympics", f"[{PB}GetSpEdition]",
      "The Committee for Physical Culture and Sport has announced the dates: this summer the best athletes of every republic meet in Luzhniki for the "
      f"[{PB}GetSpEdition]. For three months the republics prepare their teams - in the gyms, on new stadiums, and, some say, in the laboratories.\n\n"
      "§YEvery republic prepares its team in the decisions of The Politburo of the CPSU.§!",
      [EV.o("Our athletes will be ready.", ["hidden_effect = {", "if = {", "limit = { is_ai = yes }",
                                            f"set_temp_variable_to_random = {{ var = {PB}luck min = 0 max = 10 }}", f"round_temp_variable = {PB}luck",
                                            f"add_to_variable = {{ {PB}sp_pts = {PB}luck }}", "}", "}"], trig=[IN_UNION]),
       EV.o("Faster, higher, stronger - and Soviet.", trig=["original_tag = SOV"])], kind="news")
EV.ev(171, "olympics", f"The Closing of the [{PB}GetSpEdition]",
      "The flame in Luzhniki has gone out. In the table of the Union republics:\n\n"
      "  Gold: §Y[?global.COLDWAR_SOV_pb_sp_gold.GetNameDef]§!\n  Silver: §Y[?global.COLDWAR_SOV_pb_sp_silver.GetNameDef]§!\n"
      "  Bronze: §Y[?global.COLDWAR_SOV_pb_sp_bronze.GetNameDef]§!\n\nThe Central Committee congratulates the athletes of all fifteen republics: "
      "the games have shown the friendship of the peoples of the Union.",
      [EV.o("Glory to Soviet sport!")], kind="news")
EV.ev(172, "olympics", "Champions of the Spartakiad",
      "Our athletes have won the table of the Spartakiad of the Peoples of the USSR. The team returns to a parade in the capital of our republic.",
      [EV.o("Champions!", tidea(CHAMP, 730))])
EV.ev(174, "olympics", "Silver at the Spartakiad",
      "Our athletes finished second among the Union republics at the Spartakiad. A fine result - next time, gold.", [EV.o("Well done.", ["add_political_power = 50"])])
EV.ev(175, "olympics", "Bronze at the Spartakiad",
      "Our athletes finished third among the Union republics at the Spartakiad and bring medals home.", [EV.o("A place on the podium.", ["add_political_power = 25"])])
EV.ev(173, "trial", "A Doping Scandal",
      "The control commission of the sports committee has found what our team doctors were giving the athletes. Moscow speaks of a disgrace for "
      "Soviet sport, and the points our team had earned with the special preparation are struck from the record.",
      [EV.o("Blame the doctors.", [f"if = {{ limit = {{ has_global_flag = {PB}sp_open }} add_to_variable = {{ {PB}sp_pts = -{SP_SPECIAL} }} "
                                   f"clamp_variable = {{ var = {PB}sp_pts min = 0 }} }}"] + tidea(DOPING, 180))])

SPC = f"{PFX}republic_politburo_category"   # the republics' group of The Politburo of the CPSU
SP_VIS = PREP_OPEN


def sp_points(pts, flag):
    return [f"hidden_effect = {{ add_to_variable = {{ {PB}sp_pts = {pts} }} set_country_flag = {PB}{flag} }}",
            D.tt(f"pb_sp_{flag}", f"Our team gains §G{pts}§! points for the Spartakiad (now [?COLDWAR_SOV_pb_sp_pts|0]).")]


D.dec(SPC, "pb_sp_train", "Train the Republic's Team",
      "Training camps on the Black Sea, the best coaches of the republic, and leave from work for every athlete of the team.",
      "GFX_decision_cuba_sports_button", sp_points(SP_TRAIN, "sp_trained"), cost=25,
      visible=SP_VIS, available=D.ttrig("pb_sp_not_trained", "Our team has not been sent to the training camps yet.", [f"NOT = {{ has_country_flag = {PB}sp_trained }}"]), ai="base = 0")
D.dec(SPC, "pb_sp_stadiums", "Build Stadiums and Sports Schools",
      "A new stadium in the capital and a sports school in every district: the republic's athletes need more than enthusiasm.",
      "GFX_decision_generic_construction", E.gdp("pay_gdp_share", SP_GDP) + sp_points(SP_STADIUM, "sp_built"),
      visible=SP_VIS, available=D.ttrig("pb_sp_not_built", "We have not built for this Spartakiad yet.", [f"NOT = {{ has_country_flag = {PB}sp_built }}"]),
      ai="base = 0")
D.dec(SPC, "pb_sp_special", "Special Preparation of the Athletes",
      "The team doctors have a programme of their own. Nobody asks what is in the injections, and nobody will - unless the control commission does.",
      "GFX_decision_nko_medicine_relief_button",
      sp_points(SP_SPECIAL, "sp_special") +
      [D.tt("pb_sp_doping_risk", "§RIn one case of four the doctors are caught§!: §RA Doping Scandal§! (stability -5%, political power gain -5% for 180 days) "
                                 "and the points are struck from the record."),
       "hidden_effect = {", f"set_temp_variable_to_random = {{ var = {PB}roll min = 0 max = 100 }}",
       f"if = {{ limit = {{ check_variable = {{ {PB}roll < 25 }} }} country_event = {{ id = {NS}.173 days = 14 random_days = 30 }} }}", "}"],
      visible=SP_VIS, available=D.ttrig("pb_sp_not_special", "Our doctors have not started their programme yet.", [f"NOT = {{ has_country_flag = {PB}sp_special }}"]), cost=25, ai="base = 0")

# ================================================================ the dossier's honour roll (scripted localisation)
EMU_TT = loc(f"{PB}emu_tt", "§YSocialist Emulation§!: every month Moscow ranks the Union republics by growth, industry, output per head and the "
                            "fulfilled targets of the Union Plan, using the figures the republics report.\n\n"
                            "§YEvery quarter§! a §YTransferable Red Banner§! goes to the leader of each column (the holder keeps it on a tie):\n"
                            + "".join(f"  {BANNERS[k][0]}: {mods_txt(BANNERS[k][2])}\n" for k in KEYS) +
                            "§YSocialist Emulation§! (Union tree) doubles the banners.\n\n"
                            "§YEvery January§! the best republic overall becomes the §YPride of the Union§! for a year: "
                            f"{mods_txt(PRIDE_MODS)}.\nA second title in a row: §YHero of Socialist Labour§! instead ({mods_txt(HERO_MODS)}) and the "
                            "Gold Star for the First Secretary.\nThree titles in one Five-Year Plan: the §YOrder of Lenin§! for as long as the republic stays "
                            f"in the Union ({mods_txt(ORDER_MODS)}).\nThe last republic is §RLagging Behind§! for a year ({mods_txt(LAG_MODS)}, "
                            "investigations +10%).\n\nHolders of the Order of Lenin:[COLDWAR_SOV_pb_GetOrderList]")
dt(f"{PB}GetOrderList", [([f"any_country = {{ has_idea = {ORDER} }}"], loc(f"{PB}order_list", "".join(f"[{t}.COLDWAR_SOV_pb_GetOrderHolder]" for t in SSR)))],
   loc(f"{PB}order_none", " none yet."))
dt(f"{PB}GetOrderHolder", [([f"original_tag = {t}", f"has_idea = {ORDER}"], loc(f"{PB}order_{t}", "\\n  " + SSR_NAME[t])) for t in SSR], f"{PB}empty")

dt(f"{PB}GetPride", [([f"has_global_flag = {PB}pride_awarded", f"var:global.{PB}pride = {{ has_country_flag = {PB}disqualified }}"],
                      loc(f"{PB}pride_withdrawn", "Pride of the Union: §R[?global.COLDWAR_SOV_pb_pride.GetName] - title withdrawn§!")),
                     ([f"has_global_flag = {PB}pride_awarded", f"var:global.{PB}pride = {{ check_variable = {{ {PB}streak > 1 }} }}"],
                      loc(f"{PB}pride_hero", "Pride of the Union: §Y[?global.COLDWAR_SOV_pb_pride.GetName]§! - Hero of Socialist Labour")),
                     ([f"has_global_flag = {PB}pride_awarded"], loc(f"{PB}pride_holder", "Pride of the Union: §Y[?global.COLDWAR_SOV_pb_pride.GetName]§!"))],
   loc(f"{PB}pride_none", "Pride of the Union: first awarded at the January session of 1971"))
dt(f"{PB}GetLagging", [([f"has_global_flag = {PB}lagging_named"], loc(f"{PB}lag_holder", "Last place: §R[?global.COLDWAR_SOV_pb_lagging.GetName]§!"))],
   loc(f"{PB}lag_none", "Last place: nobody named yet"))
dt(f"{PB}GetFavourite", [([f"has_global_flag = {PB}favour_active"], loc(f"{PB}fav_holder", "Moscow favours: §Y[?global.COLDWAR_SOV_pb_favourite.GetName]§!"))],
   loc(f"{PB}fav_none", "Moscow favours: no republic"))
LAG_TT = loc(f"{PB}lag_tt", "Every January the republic with the worst overall standing - not Moscow's favourite, not one already disqualified - is "
                            f"§RLagging Behind§! for a year: {mods_txt(LAG_MODS)}, and an investigation is §R10%§! more likely to find something.")
FAV_GUI_TT = loc(f"{PB}fav_tt", FAV_TT)
for k in KEYS:
    loc(f"{PB}banner_{k}_tt", f"§YTransferable Red Banner: {BANNERS[k][0]}§! - held by §Y[?global.COLDWAR_SOV_pb_banner_{k}.GetName]§!.\n"
                              f"Bonus: {mods_txt(BANNERS[k][2])} (doubled by §YSocialist Emulation§!). Every quarter it passes to the leader of this column; "
                              "on a tie the holder keeps it.")


def banner_holder(k):
    return f"any_country = {{ has_country_flag = {PB}banner_{k} }}"


def leader_holds(k):
    return f"var:global.{PB}top_{k} = {{ has_country_flag = {PB}banner_{k} }}"


# ================================================================ readable names of the dossier's flags and variables (cw_names.py layer)
import cw_names as N
N.FLAG_TEXT.update({
    **{f"pb_banner_{k}": f"Holds the Transferable Red Banner: {BANNERS[k][0]}" for k in KEYS},
    "pb_disqualified": "Disqualified from the Socialist Emulation", "pb_favour_active": "Moscow has favoured a republic this year",
    "pb_favoured": "Moscow's favourite in the Socialist Emulation", "pb_inflated": "Reports polished figures to Moscow",
    "pb_lagging_named": "A republic has been named Lagging Behind", "pb_new_pride": "Has just been named the Pride of the Union",
    "pb_order_due": "Is due the Order of Lenin", "pb_order_new": "A republic has just received the Order of Lenin",
    "pb_pride_awarded": "The Pride of the Union has been awarded", "pb_won_last": "Won the last Socialist Emulation",
    "pb_sp_open": "The republics are preparing for the Spartakiad", "pb_sp_held": "The Spartakiad has been held",
    "pb_sp_trained": "Has sent its team to the training camps", "pb_sp_built": "Has built stadiums for the Spartakiad",
    "pb_sp_special": "Its team doctors run a special programme", "pb_sp_medal": "Has won a medal at the Spartakiad",
})
N.VAR_TEXT.update({
    "pb_month": "Months of Socialist Emulation", "pb_score": "Socialist Emulation score (sum of the ranks)", "pb_ssr_count": "Union republics in the table",
    "pb_streak": "Titles in a row (Pride of the Union)", "pb_titles": "Titles in this Five-Year Plan", "pb_title_plan": "Five-Year Plan of the titles",
    "pb_lagging": "The republic lagging behind", "pb_favourite": "Moscow's favourite", "pb_pride": "The Pride of the Union",
    "pb_sp_edition": "Spartakiad of the Peoples of the USSR", "pb_sp_pts": "Spartakiad preparation (points)", "pb_sp_score": "Spartakiad result",
    "pb_sp_gold": "Spartakiad champions", "pb_sp_silver": "Spartakiad silver", "pb_sp_bronze": "Spartakiad bronze",
    "pb_slot": "Seat in the dossier", **{f"pb_slot_{n}_on": f"Seat {'I' * n} is taken" for n in (1, 2, 3)},
    **{f"pb_seat_{n}": f"Holder of seat {'I' * n}" for n in (1, 2, 3)},
    **{f"pb_rank_{k}": f"Rank in the Socialist Emulation: {EMU[k][0].lower()}" for k in KEYS},
    **{f"pb_v_{k}": f"Reported figure: {EMU[k][0].lower()}" for k in KEYS},
    **{f"pb_top_{k}": f"Leader of the Socialist Emulation: {EMU[k][0].lower()}" for k in KEYS},
    **{f"pb_top_{k}_val": f"Leading figure: {EMU[k][0].lower()}" for k in KEYS},
})
