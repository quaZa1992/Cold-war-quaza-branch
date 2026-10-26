# IMPERIA CW — Cold War: Soviet Union 1970 content generator.
# COLDWAR | Decision categories and decisions of the Soviet Union 1970 tree (Politburo balance, plenum, Five-Year Plans,
# the Union, grain imports, the seats of the republics for Moscow, and the republic's side of the Politburo).
from cw_common import *
import cw_effects as E
import cw_avail as A
from cw_layout import BYID
from cw_sys_effects import KEYS, KIDX, PLAN_PRIOS, share_txt

CATS = []        # (key, name, desc, icon, priority, allowed, visible, extra lines)
DECS = {}        # category -> [decision text blocks]
# Enes, 19.10.2026: Moscow's seat decisions, the republics' Politburo decisions and the ballot share ONE category,
# "The Politburo of the CPSU", with the Politburo dossier (cw_pbgui.py) on top. The old categories are only groups now:
# their allowed/visible conditions move into each of their decisions, so every country still sees only its own.
PBCAT = f"{PFX}politburo_cpsu_category"
MERGED = {}      # old category key -> (allowed lines, visible lines)
SOV_T = ["original_tag = SOV", "IMP_is_1970_scenario = yes"]
SYSTEM = [f"has_global_flag = {PFX}politburo_system", f"NOT = {{ has_global_flag = {PFX}federation_council }}"]


def cat(key, name, desc, icon, prio, allowed, visible, extra=(), merge_into=None):
    if merge_into:
        MERGED[key] = (list(allowed), list(visible), merge_into)
        DECS[key] = []
        return
    CATS.append((key, name, desc, icon, prio, allowed, visible, list(extra)))
    LOC[key] = name
    LOC[key + "_desc"] = desc
    DECS[key] = []


def dec(category, key, name, desc, icon, effect, cost=0, visible=(), available=(), ai="base = 0", re_enable=None, once=False,
        targets=None, target_trigger=(), remove=None, extra=()):
    k = PFX + key
    LOC[k] = name
    LOC[k + "_desc"] = desc
    L = [f"{k} = {{", f"icon = {icon}"]
    if category in MERGED:
        m_allowed, m_visible, category = MERGED[category]
        L += ["allowed = {"] + m_allowed + ["}"]
        visible = list(m_visible) + list(visible)
    if cost:
        L.append(f"cost = {cost}")
    if remove:
        L.append(f"days_remove = {remove}")
    if re_enable:
        L.append(f"days_re_enable = {re_enable}")
    L.append(f"fire_only_once = {'yes' if once else 'no'}")
    if targets:
        L += ["target_root_trigger = { always = yes }", "targets = { " + " ".join(targets) + " }", "target_non_existing = no",
              "target_trigger = {", "FROM = {"] + list(target_trigger) + ["}", "}"]
    L += list(extra)
    if visible:
        L += ["visible = {"] + list(visible) + ["}"]
    if available:
        L += ["available = {"] + list(available) + ["}"]
    L += ["complete_effect = {", f'log = "[GetDateText]: [Root.GetName]: Decision {k}"'] + list(effect) + ["}"]
    L += ["ai_will_do = {"] + ai.split("\n") + ["}", "}", ""]
    DECS[category].append(L)


def tt(key, text):
    LOC[f"{PFX}{key}_tt"] = text
    return f"custom_effect_tooltip = {PFX}{key}_tt"


def ttrig(key, text, body):
    LOC[f"{PFX}{key}_trig_tt"] = text
    return ["custom_trigger_tooltip = {", f"tooltip = {PFX}{key}_trig_tt"] + list(body) + ["}"]


def unlocked(key):
    LOC[f"{PFX}{key}_unlock_tt"] = f"Unlocks the decisions §Y{dict((c[0], c[1]) for c in CATS_PRE)[PFX + key]}§!."
    return f"has_country_flag = {PFX}{key}_unlocked"


CATS_PRE = [(f"{PFX}politburo_category", "The Politburo"), (f"{PFX}five_year_plan_category", "Five-Year Plans"),
            (f"{PFX}union_category", "The Union of Republics"), (f"{PFX}grain_import_decisions", "Grain Imports")]
for k, n in CATS_PRE:
    LOC[f"{k}_unlock_tt"] = f"Unlocks the decisions §Y{n}§!."
NO_VOTE = ttrig("no_vote_running", "No Politburo vote is running.", [f"NOT = {{ has_global_flag = {PFX}vote_running }}"])

# ================================================================ Moscow: the Politburo balance
cat(f"{PFX}politburo_category", "The Politburo",
    "Ten old men in the Kremlin decide the fate of a superpower. The §YPolitburo balance§! between reformers and the orthodox shapes every vote: "
    "a General Secretary who wants his way must cultivate both camps.",
    "GFX_decision_category_power_struggle", 190, SOV_T, [f"has_country_flag = {PFX}politburo_category_unlocked"])
C = f"{PFX}politburo_category"
dec(C, "rally_the_reformers", "Rally the Reformers",
    "Kosygin's economists, the institutes of the Academy and the younger regional secretaries are invited to the Kremlin. The old apparatus watches with suspicion.",
    "GFX_decision_generic_political_discourse", E.bop(-0.10) + E.faction("communist_cadres", -5), cost=50, re_enable=90)
dec(C, "rally_the_orthodox", "Rally the Orthodox",
    "Suslov's ideological commission, the Main Political Directorate of the army and the veterans of the Party are given the floor.",
    "GFX_decision_generic_political_rally", E.bop(0.10) + [f"add_timed_idea = {{ idea = {PFX}ideological_campaign days = 180 }}"], cost=50, re_enable=90)
dec(C, "retire_a_veteran", "Retire a Veteran",
    "One of the old men is persuaded to retire with honours, a dacha and a state pension. His seat goes to a man of the middle.",
    "GFX_decision_generic_speech", [f"{PFX}bop_toward_centre_05 = yes"] + E.faction("communist_cadres", -10), cost=75, re_enable=180)
dec(C, "promote_regional_cadres", "Promote Regional Cadres",
    "First Secretaries from the republics and the oblasts are brought to Moscow as ministers and department heads. The republics feel heard; "
    "the networks of patronage grow.",
    "GFX_decision_generic_nationalism", E.cohesion(3) + E.dyn_change(f"{PFX}party_state_modifier", f"{PFX}party_state", {"corruption_cost_factor": 0.03}),
    cost=50, re_enable=180)

# ================================================================ Moscow: the plenum (change of General Secretary)
cat(f"{PFX}plenum_category", "The Plenum of the Central Committee",
    "A General Secretary is not overthrown, he is relieved by the Plenum. Every candidacy opened in the focus tree can be put to the Politburo here: "
    "Moscow casts §Y3§! votes for its candidate, every republic with a seat in the Politburo has §Y1§! vote (AI republics vote in favour, players decide "
    "in §YThe Politburo of the CPSU§!). The candidate takes over unless all three republican members vote against; then stability falls and he must wait 180 days.",
    "GFX_decision_category_generic_communism", 191, SOV_T,
    ["OR = {"] + [f"has_country_flag = {PFX}candidate_{k}" for k in KEYS if k != "bre"] + ["}"])
C = f"{PFX}plenum_category"
for k in KEYS:
    if k == "bre":
        continue
    f = BYID[f"{PFX}ple_{k}"] if f"{PFX}ple_{k}" in BYID else None
    av = A.convert(f) if f else ""
    lean = E.GENSEC_LEAN[k]
    name = E.GENSEC[k][0]
    people = [(f"convene_plenum_{k}", name, [f"{PFX}alive_{k} = yes"])]
    if k in E.STANDIN:   # the candidate has died: his stand-in asks the Plenum in his place (Enes, 17.10.2026)
        people.append((f"convene_plenum_{k}_standin", E.STANDIN[k][0], [f"{PFX}standin_{k} = yes"]))
    for did, who, alive_t in people:
        extra = "" if who == name else f" {name} is dead; {who} carries his course."
        dec(C, did, f"Convene the Plenum: {who}",
            f"The Politburo is asked to propose §Y{who}§! to the Plenum as General Secretary.{extra} "
            f"Moscow casts §Y3§! votes for him, every republican member has §Y1§!: only if all three republican members vote against is he rejected.",
            "GFX_decision_generic_political_discourse",
            [tt(f"plenum_vote_{did}", f"The Politburo votes on §Y{who}§! within 10 days."),
             f"set_temp_variable = {{ {PFX}vt = 3 }}", f"set_temp_variable = {{ {PFX}vs = {KIDX[k]} }}", f"set_temp_variable = {{ {PFX}vl = {lean} }}",
             f"set_temp_variable = {{ {PFX}vu = 0 }}", f"set_variable = {{ global.{PFX}vote_succession = 0 }}", f"{PFX}start_vote = yes"],
            cost=50,
            visible=[f"has_country_flag = {PFX}candidate_{k}", f"NOT = {{ has_country_flag = {PFX}gensec_{k} }}"] + alive_t,
            available=["emerging_communist_state_are_in_power = yes"] + NO_VOTE +
                      ttrig(f"plenum_wait_{k}", f"The Plenum has not rejected §Y{name}§! in the last 180 days.",
                            [f"NOT = {{ has_country_flag = {PFX}plenum_failed_{k} }}"]) +
                      [l for l in av.split("\n") if l.strip() and l.strip() != "emerging_communist_state_are_in_power = yes"])

# ================================================================ Moscow: Five-Year Plans
cat(f"{PFX}five_year_plan_category", "Five-Year Plans",
    "Gosplan drafts, the Party Congress approves, the Supreme Soviet makes it law. At the start of every Five-Year Plan the leadership sets one priority; "
    "the Politburo votes on it. A plan that the Politburo rejects still applies, but the General Secretary carries the defeat.\n\nCurrent plan: §Y[COLDWAR_SOV_GetPlanName]§!",
    "GFX_decision_category_generic_economy", 192, SOV_T, [f"has_country_flag = {PFX}five_year_plan_category_unlocked"])
C = f"{PFX}five_year_plan_category"
PDESC = {"plan_group_a": "Steel, machine tools and power stations first: the old Soviet recipe for growth.",
         "plan_group_b": "Refrigerators, televisions, clothes and housing: a plan for the Soviet consumer.",
         "plan_armaments": "Parity with the United States must be held at any price: the defence industry receives the best of everything.",
         "plan_agriculture": "Fertiliser, tractors, irrigation and storage: the Party promises to end the grain imports."}
for i, (k, n, m) in enumerate(PLAN_PRIOS, start=1):
    dec(C, f"set_{k}", f"Priority: {n.split(': ')[-1]}", PDESC[k], ["GFX_decision_generic_industry", "GFX_decision_generic_consumer_goods",
                                                                     "GFX_decision_generic_military", "GFX_decision_generic_construction"][i - 1],
        [f"add_ideas = {PFX}{k}", f"set_country_flag = {PFX}plan_priority_chosen",
         tt("plan_vote", "The Politburo votes on the priority within 10 days (majority: §G+50§! political power; otherwise §RDefying the Politburo§!). "
                         "The priority applies until the end of the plan."),
         f"set_temp_variable = {{ {PFX}vt = 2 }}", f"set_temp_variable = {{ {PFX}vs = {i} }}", f"set_temp_variable = {{ {PFX}vl = 0 }}",
         f"set_temp_variable = {{ {PFX}vu = 0 }}", f"{PFX}start_vote = yes"],
        cost=150,
        available=ttrig("plan_open", "A new Five-Year Plan has begun and no priority has been set for it yet.",
                        [f"check_variable = {{ global.{PFX}plan > 8 }}", f"NOT = {{ has_country_flag = {PFX}plan_priority_chosen }}"]) + NO_VOTE,
        ai=f"base = {[3, 1, 4, 2][i - 1]}")

# ================================================================ Moscow: the Union
cat(f"{PFX}union_category", "The Union of Republics",
    "Fifteen republics, more than a hundred nationalities, one Party. §YUnion cohesion§! ([?COLDWAR_SOV_union_cohesion|0] of 100) decides how much Moscow "
    "can ask of the republics, and how much they will ask of Moscow.",
    "GFX_decision_category_union_state", 193, SOV_T, [f"has_country_flag = {PFX}union_category_unlocked"])
C = f"{PFX}union_category"
dec(C, "development_fund", "The Development Fund of the Republics",
    "Money from the Union budget for schools, hospitals and factories in the poorer republics of Central Asia and the Caucasus.",
    "GFX_decision_generic_construction", E.gdp("pay_gdp_share", 0.005) + E.cohesion(5), re_enable=365, ai="base = 2")
dec(C, "cadre_rotation", "Rotate the Republican Cadres",
    "Second Secretaries from Moscow, Russians as KGB chiefs, outsiders as heads of the republican ministries: the local clans lose their grip.",
    "GFX_decision_generic_arrest", E.cohesion(-3) + ["decrease_corruption = yes"], cost=50, re_enable=365, ai="base = 1")
dec(C, "russification_campaign", "The Russian Language Campaign",
    "Russian from the first school year, Russian in the army, Russian in the universities: the language of interethnic communication for all.",
    "GFX_decision_propaganda",
    E.cohesion(-4) + E.dyn_change(f"{PFX}armed_forces_modifier", f"{PFX}armed_forces", {"training_time_factor": -0.03}) +
    [f"add_to_variable = {{ {PFX}russification_count = 1 }}"],
    cost=25, re_enable=365, available=ttrig("russification_max", "Used fewer than three times.", [f"check_variable = {{ {PFX}russification_count < 3 }}"]),
    ai="base = 1")
dec(C, "sovereign_rights", "Sovereign Rights for the Republics",
    "The republics receive more control over their own budgets, languages and cadres. Moscow governs less and is resented less.",
    "GFX_decision_generic_independence", E.cohesion(8) + [f"add_timed_idea = {{ idea = {PFX}sovereign_rights days = 365 }}"], cost=100, re_enable=730,
    ai="base = 1\nmodifier = { factor = 5 check_variable = { COLDWAR_SOV_union_cohesion < 40 } }")

# ================================================================ Moscow: grain
cat(f"{PFX}grain_import_decisions", "Grain Imports",
    "Since 1972 the Soviet Union has bought grain abroad in every bad year: from the United States, Canada, Argentina and Australia, paid in gold and oil money.",
    "GFX_decision_category_generic_industry", 194, SOV_T, [f"has_country_flag = {PFX}grain_import_decisions_unlocked"])
dec(f"{PFX}grain_import_decisions", "buy_grain_abroad", "Buy Grain Abroad",
    "Exportkhleb sends its buyers to the grain exchanges of the West. The shops stay full; the gold reserve shrinks.",
    "GFX_decision_oil", E.gdp("pay_gdp_share", 0.005) + [f"set_country_flag = {{ flag = {PFX}grain_bought days = 150 }}",
                                                       tt("grain_bought", "The poor harvest no longer costs us §Y5%§! stability.")],
    available=ttrig("poor_harvest", "The harvest has failed this year.", [f"has_country_flag = {PFX}poor_harvest", f"NOT = {{ has_country_flag = {PFX}grain_bought }}"]),
    ai="base = 5")

# ================================================================ the shared category with the Politburo dossier (cw_pbgui.py)
cat(PBCAT, "The Politburo of the CPSU",
    "The Political Bureau of the Central Committee: eleven men in Moscow and three First Secretaries of the Union republics. "
    "Its file lies open to the Kremlin and to every republic.\n\n[COLDWAR_SOV_GetSessionState]",
    "GFX_decision_category_power_struggle", 189,
    ["OR = {", "AND = { original_tag = SOV IMP_is_1970_scenario = yes }", f"{PFX}is_union_republic = yes", "}"],
    SYSTEM + ["OR = {", "original_tag = SOV", f"{PFX}is_union_republic = yes", "}"],   # a republic that has left the Union loses the file
    extra=[f"scripted_gui = {PFX}politburo_gui"])

# ================================================================ Moscow: the seats of the republics
cat(f"{PFX}politburo_seats_category", "Seats of the Republics",
    "Three seats in the Politburo belong to the Union republics. At a §YParty Congress§! Moscow fills them freely; between congresses only an extraordinary "
    "plenum can change them. Seats taken: §Y[?global.COLDWAR_SOV_seat_count]§! of 3.\n\n[COLDWAR_SOV_GetSessionState]",
    "GFX_decision_category_generic_political_actions", 195, SOV_T, SYSTEM, merge_into=PBCAT)
C = f"{PFX}politburo_seats_category"
REP = [f"{PFX}is_union_republic = yes"]
FREE_SEAT = ttrig("seat_free", "A republican seat is free.", [f"check_variable = {{ global.{PFX}seat_count < 3 }}"])
CONGRESS = ttrig("congress_open", "A Party Congress is in session (or a rotation left a seat to fill).",
                 ["OR = {", f"has_global_flag = {PFX}congress_open", f"has_country_flag = {PFX}free_appointment", "}"])
NOT_CONGRESS = ttrig("no_congress", "No Party Congress is in session.", [f"NOT = {{ has_global_flag = {PFX}congress_open }}"])
NO_BARONS = ttrig("no_barons", "We have not promised the local barons stability (§YTrust the Local Barons§!).", [f"NOT = {{ has_country_flag = {PFX}local_barons }}"])
BID_PAY = [f"if = {{ limit = {{ FROM = {{ has_country_flag = {PFX}bid_25 }} }} add_political_power = 25 }}",
           f"if = {{ limit = {{ FROM = {{ has_country_flag = {PFX}bid_50 }} }} add_political_power = 50 }}",
           f"if = {{ limit = {{ FROM = {{ has_country_flag = {PFX}bid_100 }} }} add_political_power = 100 }}",
           tt("bid_received", "We receive the political power that [FROM.GetNameDef] offered with its application."),
           f"FROM = {{ clr_country_flag = {PFX}bid_25 clr_country_flag = {PFX}bid_50 clr_country_flag = {PFX}bid_100 }}"]
dec(C, "appoint_seat", "Appoint [FROM.GetNameDef] to the Politburo",
    "The First Secretary of [FROM.GetNameDef] becomes a full member of the Politburo. [FROM.COLDWAR_SOV_GetBid]",
    "GFX_decision_generic_political_rally", ["FROM = { COLDWAR_SOV_grant_seat = yes }"] + BID_PAY + [f"clr_country_flag = {PFX}free_appointment"],
    targets=SSR, target_trigger=REP + [f"NOT = {{ has_country_flag = {PFX}seat }}", f"NOT = {{ has_idea = {PFX}in_disgrace }}"],
    available=FREE_SEAT + CONGRESS, ai="base = 0")
dec(C, "appoint_seat_extraordinary", "Extraordinary Plenum: Appoint [FROM.GetNameDef]",
    "Between congresses a seat can only be filled by an extraordinary plenum of the Central Committee. It costs authority.",
    "GFX_decision_generic_political_discourse", ["add_stability = -0.03", "FROM = { COLDWAR_SOV_grant_seat = yes }"], cost=100,
    targets=SSR, target_trigger=REP + [f"NOT = {{ has_country_flag = {PFX}seat }}", f"NOT = {{ has_idea = {PFX}in_disgrace }}"],
    available=FREE_SEAT + NOT_CONGRESS + NO_BARONS)
dec(C, "dismiss_seat", "Remove [FROM.GetNameDef] from the Politburo",
    "The Congress elects a new Politburo. The First Secretary of [FROM.GetNameDef] is not on the list.",
    "GFX_decision_generic_arrest", ["FROM = { COLDWAR_SOV_dismiss_seat = yes }"],
    targets=SSR, target_trigger=[f"has_country_flag = {PFX}seat"], available=CONGRESS)
dec(C, "dismiss_seat_extraordinary", "Extraordinary Plenum: Remove [FROM.GetNameDef]",
    "Between congresses a member of the Politburo can only be removed by an extraordinary plenum of the Central Committee.",
    "GFX_decision_generic_arrest", ["add_stability = -0.03", "FROM = { COLDWAR_SOV_dismiss_seat = yes }"], cost=100,
    targets=SSR, target_trigger=[f"has_country_flag = {PFX}seat"], available=NOT_CONGRESS + NO_BARONS)
dec(C, "purge_a_seat", "Purge [FROM.GetNameDef] from the Politburo",
    "Shelepin's purge of the Brezhnevites reaches the republics: one republican member can be removed without a plenum.",
    "GFX_decision_generic_arrest", ["FROM = { COLDWAR_SOV_dismiss_seat = yes }", f"clr_country_flag = {PFX}free_dismissal"],
    targets=SSR, target_trigger=[f"has_country_flag = {PFX}seat"], visible=[f"has_country_flag = {PFX}free_dismissal"])
dec(C, "call_a_session", "Call an Extra Session of the Politburo",
    "The General Secretary summons the Politburo outside the regular calendar. Every republican member may submit a new proposal.",
    "GFX_decision_generic_speech", [f"set_country_flag = {PFX}extra_session", f"country_event = {{ id = {NS}.10 }}"], cost=50, re_enable=90)
dec(C, "promote_to_moscow", "Promote the First Secretary of [FROM.GetNameDef] to Moscow",
    "A post in Moscow for a deserving First Secretary - and a free seat in the Politburo. Aliyev went this way in 1982, Shevardnadze in 1985. "
    "§YThe republic decides§! whether to accept.",
    "GFX_decision_generic_political_discourse", [f"FROM = {{ country_event = {{ id = {NS}.19 days = 1 }} }}",
                                                 tt("promotion_offer", "[FROM.GetNameDefCap] receives the offer and decides.")],
    cost=25, re_enable=365, targets=SSR, target_trigger=[f"has_country_flag = {PFX}seat"])
dec(C, "kgb_investigation", "KGB Investigation: [FROM.GetNameDef]",
    "Andropov's discipline campaign does not need an accuser. The KGB examines the First Secretary of [FROM.GetNameDef].",
    "GFX_decision_generic_intelligence_operation", ["FROM = { COLDWAR_SOV_investigate_republic = yes }"], cost=50, re_enable=180,
    targets=SSR, target_trigger=[f"has_country_flag = {PFX}seat"], visible=[f"has_country_flag = {PFX}discipline_campaign"])

# ================================================================ the republics: their side of the Politburo
REPCAT = f"{PFX}republic_politburo_category"
cat(REPCAT, "The Republic and the Politburo",
    "Three seats in the Politburo, fourteen republics. A seat brings authority, money and a voice in Moscow; it also binds the republic to the centre. "
    "Applications, proposals, patronage and kompromat: the game is played in the corridors of the Central Committee.\n\n[COLDWAR_SOV_GetSessionState]",
    "GFX_decision_category_generic_communism", 196, [f"{PFX}is_union_republic = yes"], SYSTEM, merge_into=PBCAT)
C = REPCAT
HAS_SEAT = ttrig("has_seat", "Our republic has a seat in the Politburo.", [f"has_country_flag = {PFX}seat"])
NO_SEAT = ttrig("no_seat", "Our republic has no seat in the Politburo (Moscow's eye is not on us).", [f"NOT = {{ has_country_flag = {PFX}seat }}"])
for bid, ai in ((25, "base = 0"), (50, "base = 0"), (100, "base = 0")):
    dec(C, f"apply_{bid}", f"Apply for a Seat ({bid} political power)",
        f"Our First Secretary applies for a seat in the Politburo at the coming Party Congress, with a gift of §Y{bid}§! political power for Moscow. "
        "If Moscow chooses another republic, half of it comes back.",
        "GFX_decision_generic_political_rally", [f"set_country_flag = {PFX}applied", f"set_country_flag = {PFX}bid_{bid}",
                                                tt(f"apply_{bid}", f"Moscow sees our offer of §Y{bid}§! political power.")],
        cost=bid, visible=[f"has_global_flag = {PFX}applications_open", f"NOT = {{ has_country_flag = {PFX}seat }}"],
        available=ttrig("can_apply", "Applications for the coming Party Congress are open, we have no seat and have not applied yet, "
                                     "and we are neither in disgrace nor branded slanderers.", [f"{PFX}can_apply = yes"]), ai=ai)
BUILD_N = ["a Civilian Factory", "Infrastructure", "a Power Station", "an Agriculture District", "a Military Factory"]
PROPOSER = ["OR = {", f"has_country_flag = {PFX}seat", f"has_idea = {PFX}patron_in_moscow", "}"]
PROP_AV = ttrig("proposal_free", "We have not submitted a proposal in this session (a patron without a seat: one a year), and no earlier proposal is still open.",
                [f"NOT = {{ has_country_flag = {PFX}proposal_made }}", f"NOT = {{ has_country_flag = {PFX}patron_cooldown }}",
                 f"NOT = {{ has_country_flag = {PFX}proposal_locked }}"])
PROP_DONE = [f"set_country_flag = {PFX}proposal_made", f"clr_country_flag = {PFX}proposal_rejected",
             f"set_country_flag = {{ flag = {PFX}proposal_locked days = 120 }}",
             f"if = {{ limit = {{ NOT = {{ has_country_flag = {PFX}seat }} }} set_country_flag = {{ flag = {PFX}patron_cooldown days = 365 }} }}",
             f"if = {{ limit = {{ is_ai = yes }} set_country_flag = {{ flag = {PFX}ai_proposal_cooldown days = 730 }} }}",
             f"SOV = {{ country_event = {{ id = {NS}.20 days = 1 }} }}",
             tt("proposal_sent", "The proposal goes to §YMoscow§!. If Moscow refuses, we can take it before the Politburo.")]
AI_PROP = "base = 1\nmodifier = { factor = 0 has_country_flag = COLDWAR_SOV_ai_proposal_cooldown }"
for i, b in enumerate(BUILD_N, start=1):
    dec(C, f"propose_project_{i}", f"Propose a Union Project: {b}",
        f"We ask the Union to build {b.lower()} in our republic. Moscow pays §Y{share_txt(i)}§! of its GDP, more while other Union projects "
        f"still weigh on its budget, and its consumer goods tax rises for 90 days.",
        ["GFX_decision_generic_factory", "GFX_decision_generic_train", "GFX_decision_generic_industry", "GFX_decision_generic_construction",
         "GFX_decision_generic_military"][i - 1],
        [f"set_variable = {{ {PFX}prop_type = 1 }}", f"set_variable = {{ {PFX}prop_building = {i} }}"] + PROP_DONE,
        visible=PROPOSER, available=PROP_AV, ai=AI_PROP if i in (1, 2) else "base = 0")
dec(C, "propose_plan_relief", "Propose Plan Relief",
    "Our republic asks to be relieved of part of its plan targets for two years. Moscow would have to make up the shortfall.",
    "GFX_decision_generic_welfare", [f"set_variable = {{ {PFX}prop_type = 2 }}"] + PROP_DONE, visible=PROPOSER, available=PROP_AV)
dec(C, "propose_cadre_protection", "Propose Cadre Protection",
    "Our First Secretary asks for a guarantee that no investigation will be opened against our cadres until the next Party Congress.",
    "GFX_decision_generic_protection", [f"set_variable = {{ {PFX}prop_type = 3 }}"] + PROP_DONE, visible=PROPOSER, available=PROP_AV)
dec(C, "bring_before_politburo", "Bring It before the Politburo",
    "Moscow has refused our proposal. We put it to the Politburo: three of the seven Moscow members will usually support a republic, "
    "and with the other republican members we may have a majority.",
    "GFX_decision_generic_political_discourse",
    [tt("bring_vote", "The Politburo votes on our proposal within 10 days. If it passes, Moscow must carry it out or face §RDefying the Politburo§!."),
     f"{PFX}propose_to_politburo = yes"],
    visible=[f"has_country_flag = {PFX}proposal_rejected"], available=HAS_SEAT + NO_VOTE, ai="base = 1")
dec(C, "seek_a_patron", "Seek the Patronage of [FROM.GetNameDef]",
    "We have no seat, but [FROM.GetNameDef] has one. We ask its First Secretary to propose his next Union project for our republic. "
    "§Y[FROM.GetNameDefCap] decides.§!",
    "GFX_decision_generic_political_discourse", [f"FROM = {{ country_event = {{ id = {NS}.23 days = 1 }} }}"], cost=10, re_enable=365,
    targets=SSR, target_trigger=[f"has_country_flag = {PFX}seat"], visible=[f"NOT = {{ has_country_flag = {PFX}seat }}"])
dec(C, "kompromat", "Kompromat against [FROM.GetNameDef]",
    "We send the Party Control Committee a dossier on the First Secretary of [FROM.GetNameDef]. If Moscow investigates and finds something, "
    "he loses his seat. If not, we are branded slanderers.",
    "GFX_decision_generic_intelligence_operation",
    [f"set_global_flag = {PFX}kompromat_pending", f"set_variable = {{ global.{PFX}accuser_id = ROOT.id }}", f"set_variable = {{ global.{PFX}accused_id = FROM.id }}",
     f"every_country = {{ limit = {{ has_country_flag = {PFX}accused }} clr_country_flag = {PFX}accused }}",
     f"FROM = {{ set_country_flag = {PFX}accused }}", f"SOV = {{ country_event = {{ id = {NS}.17 days = 1 }} }}",
     tt("kompromat_sent", "§YMoscow decides§! whether to investigate. Chance of success: 15% + 5% per corruption level of the accused, "
                          "+25% if it falsified its plan report; never with cadre protection or against Moscow's Man.")],
    cost=50, re_enable=180, targets=SSR, target_trigger=[f"has_country_flag = {PFX}seat", "NOT = { tag = ROOT }"],
    available=[f"NOT = {{ has_idea = {PFX}slanderer }}"] + ttrig("kompromat_free", "Moscow is not examining another dossier right now.",
                                                                  [f"NOT = {{ has_global_flag = {PFX}kompromat_pending }}"]))
dec(C, "report_overfulfilment", "Report the Plan Overfulfilled",
    "The figures are good. On paper they are excellent: 108 percent. Moscow rewards success, and who will count the cotton?",
    "GFX_decision_generic_consumer_goods",
    ["add_political_power = 50", "increase_corruption = yes", f"set_country_flag = {PFX}pripiski", f"set_variable = {{ {PFX}pripiski_plan = global.{PFX}plan }}",
     f"if = {{ limit = {{ SOV = {{ has_country_flag = {PFX}iron_discipline }} }} add_stability = -0.03 }}",
     tt("pripiski", "Our false report (§Ypripiski§!) makes us an easy target for kompromat until it is uncovered."),
     # the Union plan (cw_union): the same false report fulfils a running plan mission
     "if = { limit = { has_country_flag = COLDWAR_UNI_target_active } set_country_flag = COLDWAR_UNI_t_reported }",
     "if = { limit = { has_country_flag = COLDWAR_UNI_directive_active } set_country_flag = COLDWAR_UNI_d_reported }",
     tt("pripiski_union", "A running §YUnion plan mission§! counts as fulfilled at once, with its full reward. If the lie is uncovered "
                          "(kompromat, a KGB investigation, or the January audit of the People's Control), the reward is taken away and the failure counts twice."),
     # Socialist Emulation (cw_emulation.py): the figures Moscow ranks are polished too; nobody but this republic is told
     tt("pripiski_emulation", "$COLDWAR_SOV_pb_pripiski_emu$"),
     f"hidden_effect = {{ set_country_flag = {{ flag = {PFX}pb_inflated days = 365 }} country_event = {{ id = {NS}.16 }} }}"],
    available=ttrig("pripiski_once", "We have not reported this Five-Year Plan yet.",
                    [f"check_variable = {{ global.{PFX}plan > 8 }}", f"NOT = {{ check_variable = {{ {PFX}pripiski_plan = global.{PFX}plan }} }}"]))
dec(C, "petition_moscow", "Petition Moscow",
    "Without a seat we can still write to the Central Committee and ask for investment. Moscow may ignore the letter.",
    "GFX_decision_generic_welfare", [f"SOV = {{ country_event = {{ id = {NS}.29 days = 1 }} }}"], re_enable=365,
    visible=[f"NOT = {{ has_country_flag = {PFX}seat }}"], ai="base = 1")
dec(C, "popular_front", "Found a Popular Front",
    "Writers, scientists and young party members found a popular front in support of perestroika - and of our nation.",
    "GFX_decision_generic_nationalism", E.party_pop(20, 0.05, 0.05) + E.cohesion(-2), cost=50, re_enable=365,
    available=NO_SEAT, ai="base = 0\nmodifier = { add = 1 SOV = { check_variable = { COLDWAR_SOV_union_cohesion < 15 } } }")
dec(C, "declare_sovereignty", "Declare Sovereignty",
    "The Supreme Soviet of our republic declares that the laws of the republic take precedence over the laws of the Union.",
    "GFX_decision_generic_independence",
    [f"add_ideas = {PFX}declaration_of_sovereignty", "COLDWAR_UNI_leave_union = yes"] + E.cohesion(-8) +
    ["SOV = {"] + E.dyn_change(f"{PFX}union_modifier", f"{PFX}union", {"tax_gain_multiplier_modifier": -0.01}) + ["}"],
    cost=75, once=True, visible=[f"NOT = {{ has_idea = {PFX}declaration_of_sovereignty }}"],
    available=NO_SEAT + ttrig("cohesion_below_55", "§YUnion cohesion§! is below §Y55§!.", [f"SOV = {{ check_variable = {{ {PFX}union_cohesion < 55 }} }}"]),   # no date gate (Enes)
    ai="base = 0\nmodifier = { add = 1 SOV = { check_variable = { COLDWAR_SOV_union_cohesion < 15 } } }")
dec(C, "independence_referendum", "Hold an Independence Referendum",
    "The people of our republic are asked whether they want to remain in the Soviet Union. §YMoscow will have to respond.§!",
    "GFX_decision_generic_independence", E.cohesion(-10) + [f"SOV = {{ country_event = {{ id = {NS}.24 days = 1 }} }}"], cost=100, re_enable=730,
    available=NO_SEAT + [f"has_idea = {PFX}declaration_of_sovereignty"] +
              ttrig("cohesion_below_35", "§YUnion cohesion§! is below §Y35§!.", [f"SOV = {{ check_variable = {{ {PFX}union_cohesion < 35 }} }}"]),
    ai="base = 0\nmodifier = { add = 1 SOV = { check_variable = { COLDWAR_SOV_union_cohesion < 15 } } }")


# ================================================================ the republics: the ballot (Enes, 18.10.2026)
# Every seat holder votes with a decision instead of an event; AI seat holders vote at once (COLDWAR_SOV_ai_ballot).
VOTECAT = f"{PFX}politburo_vote_category"
cat(VOTECAT, "The Politburo Votes",
    "The Politburo of the Central Committee votes on [COLDWAR_SOV_GetVoteSubject].\n\n[COLDWAR_SOV_GetVoteLeanFull]\n\n"
    "Our First Secretary holds one full vote. The votes are counted ten days after the vote was called; if we have not voted by then, "
    "our vote counts as an abstention.\n\n[COLDWAR_SOV_GetOwnVote]",
    "GFX_decision_category_power_struggle", 197, [f"{PFX}is_union_republic = yes"],
    [f"has_global_flag = {PFX}vote_running", f"has_country_flag = {PFX}in_vote"], merge_into=PBCAT)
BALLOT_OPEN = [f"has_global_flag = {PFX}vote_running", f"has_country_flag = {PFX}vote_pending"]
dec(VOTECAT, "ballot_yes", "Vote in Favour",
    "Our First Secretary raises his hand: the republic votes §Gin favour§! of [COLDWAR_SOV_GetVoteSubject].\n\n[COLDWAR_SOV_GetVoteLeanFull]",
    "GFX_decision_generic_political_rally",
    ["set_temp_variable = { COLDWAR_SOV_ballot = 1 }", f"{PFX}cast_vote = yes", tt("ballot_yes", "Our vote counts §Gin favour§!.")],
    visible=BALLOT_OPEN)
dec(VOTECAT, "ballot_no", "Vote Against",
    "Our First Secretary takes up the fight: the republic votes §Ragainst§! [COLDWAR_SOV_GetVoteSubject].\n\n[COLDWAR_SOV_GetVoteLeanFull]",
    "GFX_decision_weapon_on_tabel_dont_use_as_goal_icon",
    ["set_temp_variable = { COLDWAR_SOV_ballot = 2 }", f"{PFX}cast_vote = yes", tt("ballot_no", "Our vote counts §Ragainst§!.")],
    visible=BALLOT_OPEN)


def categories_file():
    L = [HEADER]
    for key, name, desc, icon, prio, allowed, visible, extra in CATS:
        L += [f"{key} = {{", f"icon = {icon}", f"priority = {prio}", "visible_when_empty = yes"] + extra + ["allowed = {"] + list(allowed) + ["}",
              "visible = {"] + list(visible) + ["}", "}", ""]
    return "\n".join(block(L)) + "\n"


def decisions_file():
    L = [HEADER]
    for key, *_ in CATS:
        L += [f"{key} = {{"]
        ds = DECS[key]
        if key == PBCAT:   # the ballot first: during a vote it is what the seat holder needs
            ds = sorted(ds, key=lambda d: 0 if "_ballot_" in d[0] else 1)
        for d in ds:
            L += d
        L += ["}", ""]
    return "\n".join(block(L)) + "\n"
