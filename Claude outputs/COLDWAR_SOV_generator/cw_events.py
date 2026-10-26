# IMPERIA CW — Cold War: Soviet Union 1970 content generator.
# COLDWAR | Events of the Soviet Union 1970 tree (English texts): focus events, the Politburo of the Republics,
# party congresses, General Secretaries (deaths, plenum, retirement), crises, and the offers (cw_offers.py).
from cw_common import *
import cw_effects as E
from cw_sys_effects import KEYS, KIDX, alive, share_txt, BURDEN_DAYS, BURDEN_CG

P = {
    "kremlin": "GFX_news_event_SOV_supreme_soviet", "congress": "GFX_report_event_generic_communist_congress", "flag": "GFX_soviet_union_flag",
    "lenin": "GFX_LeninEvent", "funeral": "GFX_report_event_generic_funeral", "news_funeral": "GFX_news_event_generic_funeral",
    "trial": "GFX_report_event_soviet_purge_trial", "space": "GFX_buran_event_2_news_SOV", "rocket": "GFX_news_rocket_explosion",
    "reactor": "GFX_news_nuclear_plant", "grain": "GFX_generic_grain_silo", "strike": "GFX_imp_1985_eb_strike_wave",
    "referendum": "GFX_event_news_SOV_democratic_referendum", "afghan": "GFX_afghanistan_war", "china": "GFX_CHI_event_china_russian_flag",
    "olympics": "GFX_event_olympics", "writer": "GFX_news_event_generic_read_write", "speech": "GFX_report_event_journalists_speech",
    "nuclear": "GFX_news_nuclear_test", "pact": "GFX_warsaw1_ovd", "coup": "GFX_army_coup_event", "karabakh": "GFX_dashnak_artsakh_protest",
    "dissolve": "GFX_sov_russ_dissolved", "empire": "GFX_sov_empire_herb", "parliament": "GFX_report_event_generic_parliament",
    "construction": "GFX_report_event_generic_construction_site", "factory": "GFX_report_event_generic_factory", "desert": "GFX_report_event_generic_ruins",
    "handshake": "GFX_report_event_generic_handshake", "demo": "GFX_imp_1985_eb_mass_demonstrations", "tanks": "GFX_report_event_soviet_tank_parade",
    "kgb": "GFX_report_event_soviet_purge_politicians", "towers": "GFX_bashnya_kremlya_techncrats",
    # Brezhnev, Andropov and the Politburo at the table (MD frame 217x163; sprite written by cw_build.EVENT_PICTURES)
    "politburo": "GFX_report_event_COLDWAR_SOV_politburo_table",
    "politburo_session": "GFX_COLDWAR_SOV_politburo_session",
}

EVENTS = []   # dicts: n, pic, title, desc, options [(text, code, ai, trigger)], kind, hidden, trigger, mtth, immediate, major, once


def ev(n, pic, title, desc, options, **kw):
    EVENTS.append(dict(n=n, pic=P.get(pic, pic), title=title, desc=desc, options=options, **kw))


def o(text, code=(), ai=1, trig=None):
    return (text, list(code) if not isinstance(code, str) else [code], ai, trig)


def tt(key, text):
    LOC[f"{PFX}{key}_tt"] = text
    return f"custom_effect_tooltip = {PFX}{key}_tt"


def fac(f, v):
    return E.faction(f, v)


SSR_HOLDERS = "every_country = { limit = { has_country_flag = COLDWAR_SOV_seat } "
GS = {k: E.GENSEC[k][0] for k in KEYS}

# ================================================================ focus events (1-9)
ev(1, "kremlin", "January 1970: The Troika",
   "Six years after the fall of Khrushchev the Soviet Union is governed by a collective leadership. General Secretary Leonid Brezhnev holds the Party, "
   "Premier Alexei Kosygin the government and the economy, Nikolai Podgorny the Presidium of the Supreme Soviet. Behind them sit the ideologue Suslov, "
   "the ambitious Shelepin, and a Politburo of old comrades who have learned to fear sudden change.\n\n"
   "The balance between reformers and the orthodox decides what the Politburo will accept. The cohesion of the fifteen Union republics decides "
   "how much Moscow can ask of them, and three republican First Secretaries sit in the Politburo itself. The country is a superpower; "
   "its shops are half empty, its harvests uncertain and its army the largest on Earth.",
   [o("Stability of cadres. Continuity. Developed socialism.")])
ev(2, "lenin", "The Lenin Centenary",
   "On 22 April 1970 the Soviet Union celebrates the hundredth birthday of Vladimir Ilyich Lenin. Every worker receives a jubilee medal, "
   "every factory holds a rally, and television broadcasts the Leniniana around the clock. The jokes about Lenin-flavoured soap and triple beds "
   "for 'Lenin is with us' travel faster than the official speeches.",
   [o("Lenin lived, Lenin lives, Lenin will live!", ["add_political_power = 25"])])
ev(3, "parliament", "The Brezhnev Constitution",
   "The Supreme Soviet has adopted the new Constitution of the USSR. Article 6 enshrines the leading and guiding role of the Communist Party; "
   "the Soviet people is proclaimed a new historical community of nations. For the first time the rights of citizens are listed at length, "
   "and for the first time no one expects them to be enforced.",
   [o("A constitution of developed socialism.", ["add_stability = 0.02"])])
ev(4, "space", "A Soviet Footprint on the Moon",
   "A Soviet cosmonaut has stepped onto the surface of the Moon. Radio Moscow interrupts its programme, crowds gather on Red Square, "
   "and newspapers across the world print the photograph of the red flag in the grey dust. The space race has a second winner.",
   [o("Glory to the Soviet people!", ["add_war_support = 0.02"])])
ev(5, "writer", "Solzhenitsyn Expelled",
   "Aleksandr Solzhenitsyn has been arrested, stripped of his citizenship and put on a plane to Frankfurt. The Gulag Archipelago is being read "
   "on Western radio stations in Russian every night. The Politburo hopes that out of sight means out of mind.",
   [o("Let him write for the West.")])
ev(6, "olympics", "The Moscow Olympics",
   "The Games of the XXII Olympiad open in the Lenin Stadium. Misha the bear smiles from every poster, the city has been cleared of dissidents "
   "and drunks, and the shops have been filled for the foreign guests. The invitations to the Western teams have been sent; each nation will decide "
   "for itself whether to come.",
   [o("Let the Games begin!", [tt("olympic_invitations", "The Western powers receive their invitations and decide for themselves whether to send a team."),
                                 "hidden_effect = {"] +
      [f"if = {{ limit = {{ country_exists = {t} NOT = {{ tag = ROOT }} }} {t} = {{ country_event = {{ id = {NS}.63 days = 1 }} }} }}"
       for t in ("USA", "ENG", "FRA", "GER", "ITA", "CAN", "JAP")] + ["}"])])
ev(7, "speech", "The Moscow Helsinki Group",
   "Yuri Orlov, Elena Bonner, Anatoly Shcharansky and their friends have founded a public group to monitor the Soviet Union's compliance with "
   "Basket Three of the Helsinki Final Act. Their reports reach Western embassies within days.",
   [o("Let them be watched.", fac("intelligence_community", 5)),
    o("A signature is a signature.", ["add_political_power = -25"] + E.bop(-0.03))])
ev(8, "nuclear", "The World Reacts",
   "Soviet strategic bombers have struck the Chinese nuclear installations at Lop Nur. Washington, New Delhi and Tokyo condemn the attack; "
   "the United Nations Security Council meets in emergency session; the communist parties of the world are divided as never before.",
   [o("The threat has been removed.")], kind="news", major=True)
ev(9, "pact", "Summoned to Moscow",
   "The Soviet leadership has summoned our Party leadership to Moscow to explain the unrest in the country and the 'right-wing deviations' "
   "in the press. Brezhnev speaks of the common responsibility of the socialist community. How we answer is our own decision.",
   [o("Promise discipline.", ["add_stability = 0.02", "add_political_power = -25",
                               "add_opinion_modifier = { target = SOV modifier = COLDWAR_SOV_brothers_in_arms }"], ai=3),
    o("Defend our own course.", ["add_political_power = 25", "SOV = { add_opinion_modifier = { target = ROOT modifier = COLDWAR_SOV_bloc_relations } }"], ai=1)])

# ================================================================ the Politburo of the Republics (10-37)
SESSION = (["# extra sessions do not move the calendar",
            "if = {", f"limit = {{ has_country_flag = {PFX}extra_session }}", f"clr_country_flag = {PFX}extra_session", "}",
            "else = {", "if = {", f"limit = {{ check_variable = {{ global.{PFX}session_half = 0 }} }}",
            f"set_variable = {{ global.{PFX}session_half = 1 }}", f"country_event = {{ id = {NS}.10 days = 184 }}", "}",
            "else = {", f"set_variable = {{ global.{PFX}session_half = 0 }}", f"country_event = {{ id = {NS}.10 days = 181 }}",
            "set_temp_variable = { COLDWAR_UNI_january = 1 }", "}"] +
           [f"if = {{ limit = {{ date > {y - 1}.12.20 date < {y}.1.20 check_variable = {{ global.{PFX}plan < {n} }} }} "
            f"set_variable = {{ global.{PFX}plan = {n} }} {PFX}start_plan = yes }}" for y, n in ((1971, 9), (1976, 10), (1981, 11), (1986, 12))] +
           ["# the Union plan (cw_union.py): settle the old year, publish the new one - after a new Five-Year Plan has begun",
            "if = { limit = { check_variable = { COLDWAR_UNI_january = 1 } check_variable = { global.COLDWAR_SOV_plan > 8 } } COLDWAR_UNI_january_session = yes }",
            "# Socialist Emulation (cw_pbgui.py): the best republic of the year becomes the Pride of the Union",
            "if = { limit = { check_variable = { COLDWAR_UNI_january = 1 } date > 1970.12.1 } COLDWAR_SOV_pb_award_pride = yes }",
            "}", "every_country = {", f"limit = {{ OR = {{ has_country_flag = {PFX}seat has_idea = {PFX}patron_in_moscow }} }}", f"clr_country_flag = {PFX}proposal_made",
            f"if = {{ limit = {{ has_country_flag = {PFX}seat }} country_event = {{ id = {NS}.15 }} }}", "}"])
ev(10, "politburo_session", "The Politburo in Session",
   "The Politburo of the Central Committee meets in its room on the third floor of the Senate building in the Kremlin. On the agenda: the reports of "
   "the ministries, the plan, cadre questions and the proposals of the republican members.\n\n"
   "Every republican seat holder may now submit one proposal for this session.",
   [o("Open the session.")], immediate=SESSION, hidden_if_ai=True)
# the ballot (Enes, 18.10.2026): players vote with the decisions "Vote in Favour" / "Vote Against" (category The Politburo Votes);
# this event only tells them. AI seat holders vote at once (COLDWAR_SOV_ai_ballot).
ev(11, "politburo_session", "The Politburo Votes",
   "The Politburo of the Central Committee votes on [COLDWAR_SOV_GetVoteSubject].\n\n"
   "[COLDWAR_SOV_GetVoteLeanFull] As one of the three republican members, our First Secretary holds a full vote.\n\n"
   "§YWe cast our vote in the decisions of The Politburo of the CPSU: in favour or against. The votes are counted ten days after the vote was called; "
   "if we have not voted by then, our vote counts as an abstention.§!",
   [o("To the vote.")])
ev(12, "kremlin", "The Count", "The votes are counted.", [o("Count.")], hidden=True, immediate=[f"{PFX}tally_vote = yes"])
ev(13, "kremlin", "The Politburo Has Voted",
   "The Politburo of the CPSU has voted on [COLDWAR_SOV_GetLastVoteSubject].\n\n§YResult: [COLDWAR_SOV_GetVoteResult]§!\n"
   "In favour: §Y[?global.COLDWAR_SOV_vote_yes]§! of §Y[?global.COLDWAR_SOV_vote_total]§! votes. [COLDWAR_SOV_GetMoscowVote]\n\nThe republican members:"
   + "".join(f"[{t}.COLDWAR_SOV_GetVoteLine]" for t in SSR),
   [o("So it is decided.")], kind="news", major=True)
ev(55, "kremlin", "The Next Item", "The next item on the agenda.", [o("Next.")], hidden=True,
   immediate=[f"if = {{ limit = {{ NOT = {{ has_global_flag = {PFX}vote_running }} }} {PFX}next_queued_vote = yes }}"])
ev(15, "kremlin", "A Seat at the Table",
   "The Politburo has met. As a republican member our First Secretary may submit one proposal for this session: a Union project for our republic, "
   "relief from the plan, or protection of our cadres. Moscow decides first; if it refuses, we can take the matter before the Politburo.",
   [o("We know what our republic needs.")])
# 16: the private confirmation of pripiski (only the republic sees it) is written in cw_emulation.py
ev(17, "trial", "A Dossier from the Republics",
   "[FROM.GetNameDefCap] has sent the Central Committee a dossier on the First Secretary of the [COLDWAR_SOV_GetAccused]: "
   "bribes, falsified reports, relatives in high places. If even half of it is true, he cannot stay in the Politburo. "
   "If it is slander, the accuser will pay for it.",
   [o("Let the Party Control Committee investigate. (25 political power)",
      [f"clr_global_flag = {PFX}kompromat_pending", "add_political_power = -25", f"set_temp_variable = {{ {PFX}acc = global.{PFX}accused_id }}", f"var:{PFX}acc = {{ {PFX}investigate_republic = yes }}",
       "if = {", f"limit = {{ NOT = {{ has_global_flag = {PFX}kompromat_proven }} }}", f"set_temp_variable = {{ {PFX}acc = global.{PFX}accuser_id }}",
       f"var:{PFX}acc = {{ add_ideas = {PFX}slanderer }}", "}"], ai=0,
      trig=["has_political_power > 24"]),
    o("Put it in the drawer.", [f"clr_global_flag = {PFX}kompromat_pending", "FROM = { add_political_power = 25 }",
                                 tt("kompromat_ignored", "The accuser gets half of the 50 political power back.")], ai=1)])
ev(18, "trial", "The Party Control Committee Reports",
   "The Party Control Committee has examined the accusations against the First Secretary of the [COLDWAR_SOV_GetAccused].\n\n[COLDWAR_SOV_GetKompromatResult]",
   [o("The Party cleanses itself.")], kind="news", major=True)
ev(19, "towers", "A Call to Moscow",
   "The General Secretary has offered our First Secretary a post in Moscow: a chair in the Council of Ministers and a place among the leadership of the Union. "
   "It is the career of a lifetime. But our republic would need a new First Secretary, and our seat in the Politburo would become free at once.\n\n"
   "In return the republic would keep a patron in Moscow.",
   [o("He goes to Moscow.", [tt("promotion_accept", "Our First Secretary moves to Moscow and a new one is elected. Our Politburo seat becomes free; "
                                                   "we gain §YPatron in Moscow§! (one proposal a year even without a seat)."),
                             "hidden_effect = { retire_country_leader = yes }", f"{PFX}leave_seat = yes", f"add_ideas = {PFX}patron_in_moscow",
                             f"FROM = {{ country_event = {{ id = {NS}.900 days = 1 }} }}"], ai=1),
    o("He is needed here.", [f"FROM = {{ country_event = {{ id = {NS}.901 days = 1 }} }}"], ai=3)])
PROP = (" A §Ycivilian factory§!", " New §Yinfrastructure§!", " A §Ypower station§!", " An §Yagriculture district§!", " A §Ymilitary factory§!")
ev(20, "kremlin", "A Proposal from the Republics",
   "[FROM.GetNameDefCap] has submitted a proposal to the Central Committee: [FROM.COLDWAR_SOV_GetProposal]\n\n"
   "If we refuse, the republic can take the matter before the Politburo, where the republican members may outvote us.",
   [o("Approve the proposal.", [f"FROM = {{ {PFX}execute_proposal = yes clr_country_flag = {PFX}proposal_rejected clr_country_flag = {PFX}proposal_locked country_event = {{ id = {NS}.21 days = 1 }} }}"] + E.cohesion(1),
      ai=f"base = 6\nmodifier = {{ factor = 0.5 check_variable = {{ {PFX}republic_burden > 0 }} FROM = {{ check_variable = {{ {PFX}prop_type = 1 }} }} }}\n"
         f"modifier = {{ factor = 0.3 check_variable = {{ {PFX}republic_burden > 1 }} FROM = {{ check_variable = {{ {PFX}prop_type = 1 }} }} }}"),
    o("Refuse.", [f"FROM = {{ set_country_flag = {{ flag = {PFX}proposal_rejected days = 90 }} country_event = {{ id = {NS}.34 days = 1 }} }}"], ai=4)],
)
ev(21, "kremlin", "Moscow Agrees",
   "The Central Committee has approved our proposal. The ministries in Moscow have been instructed to carry it out.",
   [o("The Union keeps its word.")])
ev(22, "kremlin", "The Politburo Has Overruled Us",
   "The Politburo has adopted the proposal of the [COLDWAR_SOV_GetLastProposer] against our wishes. The decision of the Politburo binds the government. "
   "We can carry it out, or ignore the majority and bear the consequences.",
   [o("Carry out the decision.", [f"set_temp_variable = {{ {PFX}tp = global.{PFX}last_proposer }}", f"var:{PFX}tp = {{ {PFX}execute_proposal = yes clr_country_flag = {PFX}proposal_locked }}"] + E.cohesion(1), ai=5),
    o("Ignore the majority.", [f"add_timed_idea = {{ idea = {PFX}defying_the_politburo days = 180 }}", f"set_temp_variable = {{ {PFX}tp = global.{PFX}last_proposer }}",
                               f"var:{PFX}tp = {{ clr_country_flag = {PFX}proposal_locked }}"] + E.cohesion(-2), ai=1)])
ev(23, "handshake", "A Request for Patronage",
   "[FROM.GetNameDefCap] has no seat in the Politburo and asks for our help: our next Union project should be built in their republic. "
   "A favour given is a favour owed.",
   [o("Take them under our wing.", [f"set_variable = {{ {PFX}prop_benef = FROM.id }}",
                                     tt("client_accept", "Our next approved §YUnion project§! is built in [FROM.GetNameDef]."),
                                     f"FROM = {{ country_event = {{ id = {NS}.900 days = 1 }} }}"], ai=1),
    o("We have our own needs.", [f"FROM = {{ country_event = {{ id = {NS}.901 days = 1 }} }}"], ai=3)])
ev(24, "referendum", "The Referendum",
   "[FROM.GetNameDefCap] has held a referendum on independence, and the result is unambiguous. The republic's leaders now ask Moscow to respond.\n\n"
   "We can negotiate a new Union treaty, recognise the result, or refuse. Force would mean war, and war must be declared openly.",
   [o("Negotiate a new Union treaty.", [f"FROM = {{ country_event = {{ id = {NS}.61 days = 1 }} }}"], ai=4),
    o("Recognise the result.", ["end_puppet = FROM"] + E.cohesion(-5), ai=1),
    o("The Union is indivisible.", ["add_stability = -0.03"] + E.cohesion(-3) + [f"FROM = {{ country_event = {{ id = {NS}.901 days = 1 }} }}"], ai=2)])
LOC[f"{PFX}free_project_tt"] = (f"Moscow pays for the building (§Y{share_txt(1)}§! of its GDP, §Y{share_txt(2)}§! for infrastructure or an agriculture district, "
                                f"§Y{share_txt(5)}§! for a military factory, more while other Union projects still weigh on its budget).")
ev(25, "construction", "A New Five-Year Plan",
   "The [COLDWAR_SOV_GetPlanName] begins. As a member of the Politburo our republic may choose one Union project, built at Moscow's expense.",
   [o(f"Build{PROP[i - 1].lower().replace('§y', '§Y')} in our republic.",
      [f"custom_effect_tooltip = {PFX}free_project_tt", f"set_temp_variable = {{ {PFX}prop_building = {i} }}", f"{PFX}build_union_project = yes"], ai=[5, 3, 2, 2, 1][i - 1])
    for i in range(1, 6)])
ev(27, "trial", "Removed from the Politburo",
   "The Central Committee has relieved the First Secretary of the [COLDWAR_SOV_GetLastSeat] of his duties as a member of the Politburo. "
   "No reason was given; none was needed.",
   [o("Cadres decide everything.")], kind="news", major=True)
ev(28, "parliament", "The Federation Council",
   "The President of the USSR has created the Federation Council. The leaders of all fifteen republics now advise the head of state directly; "
   "the three republican seats in the Politburo have lost their meaning, and the Politburo itself is no longer the centre of power.",
   [o("A new Union is being born.")], kind="news", major=True)
AI_PETITION = ("base = 2\nmodifier = { factor = 0.4 check_variable = { COLDWAR_SOV_republic_burden > 0 } }\n"
               "modifier = { factor = 0 check_variable = { COLDWAR_SOV_republic_burden > 1 } }\n"
               "modifier = { factor = 0 check_variable = { treasury < 0 } }")
ev(29, "politburo", "A Petition from the Republics",
   "[FROM.GetNameDefCap] has no seat in the Politburo, but its First Secretary has written to the Central Committee: the republic needs investment, "
   "and it asks the Union to help.\n\nEvery rouble Gosplan sends to the republics is a rouble missing in Moscow's own budget. "
   f"A Union project costs us §Y{share_txt(1)}§! of our GDP for a factory and §Y{share_txt(2)}§! for infrastructure, half as much again for every "
   f"project that still weighs on the budget, and raises our consumer goods tax by §R{BURDEN_CG * 100:g}%§! for {BURDEN_DAYS} days. "
   "Several petitions granted at once add up quickly.",
   [o("Build a civilian factory there.", [f"FROM = {{ set_temp_variable = {{ {PFX}prop_building = 1 }} {PFX}build_union_project = yes }}"], ai=AI_PETITION),
    o("Improve their infrastructure.", [f"FROM = {{ set_temp_variable = {{ {PFX}prop_building = 2 }} {PFX}build_union_project = yes }}"], ai=AI_PETITION),
    o("File it away.", [], ai=5)])
ev(30, "politburo", "The Investment Burden Eases",
   "One of the Union projects no longer weighs on Moscow's budget.",
   [o("Good.")], hidden=True,
   immediate=[f"add_to_variable = {{ {PFX}republic_burden = -1 }}", f"{PFX}update_republic_burden = yes"])
ev(34, "kremlin", "Moscow Refuses",
   "The Central Committee has refused our proposal. As a member of the Politburo we can still take the matter before the Politburo: "
   "the seven Moscow members are sceptical, but three of them will usually support a republic, and the votes of the republics may decide.\n\n"
   "The decision §YBring It before the Politburo§! is available for 90 days.",
   [o("We will see.")])
ev(35, "trial", "A New First Secretary?",
   "The Party Control Committee has found our First Secretary guilty. We have lost our seat and are in disgrace in Moscow. "
   "The Central Committee lets it be known that a new First Secretary would shorten our exile from the corridors of power.",
   [o("Elect a new First Secretary.", ["hidden_effect = { retire_country_leader = yes }", "add_stability = -0.03", f"set_variable = {{ {PFX}disgrace_left = 1 }}",
                                       tt("disgrace_shortened", "§YIn Disgrace§! ends at the next Party Congress.")], ai=1),
    o("He stays.", [], ai=2)])
ev(36, "congress", "The Party Congress Opens",
   "The [COLDWAR_SOV_GetCongress] of the Communist Party of the Soviet Union has opened in the Kremlin Palace of Congresses. Five thousand delegates "
   "applaud the report of the Central Committee. Behind the scenes the new Central Committee and the new Politburo are being formed: "
   "for thirty days Moscow may change the republican seats without the cost of an extraordinary plenum.",
   [o("Long live the Party!")], kind="news", major=True)
ev(37, "congress", "The New Politburo",
   "The [COLDWAR_SOV_GetCongress] has closed. The new Central Committee has elected the Politburo. The republican members:"
   + "".join(f"[{t}.COLDWAR_SOV_GetSeatLine]" for t in SSR),
   [o("Forward to the decisions of the Congress!")], kind="news", major=True)

# ================================================================ General Secretaries (31-33, 90-97)
CAND = [k for k in KEYS if k != "bre"]
AI_SUCC = {"and": "date > 1982.10.1 date < 1984.2.9", "che": "date > 1984.1.1 date < 1985.3.10", "gor": "date > 1985.2.1",
           "sus": "date < 1973.4.26", "kos": "date < 1973.4.26"}
ev(31, "kremlin", "The Succession Plenum",
   "The Central Committee has been summoned to an extraordinary plenum. The Politburo must propose a new General Secretary, and the plenum will elect him. "
   "Who will lead the Party now?",
   [o(f"{GS[k]}.", [f"{PFX}install_gensec_{k} = yes"], ai=(f"base = 1 modifier = {{ add = 30 {AI_SUCC[k]} }}" if k in AI_SUCC else 1),
      trig=[f"{PFX}alive_{k} = yes"]) for k in CAND] +
   [o(f"{E.STANDIN[k][0]}, in the place of {GS[k]}.", [f"{PFX}install_gensec_{k} = yes"], ai=1,
      trig=[f"{PFX}standin_{k} = yes"]) for k in CAND if k in E.STANDIN])
ev(32, "kremlin", "A Dignified Retirement",
   "Leonid Ilyich Brezhnev has asked the Central Committee to relieve him of his duties for reasons of health. The Plenum thanks him for his "
   "outstanding services; the Politburo will now put his designated heir to the vote.",
   [o("The Party thanks Leonid Ilyich.", [f"set_global_flag = {PFX}dead_bre", f"clr_country_flag = {PFX}bre_retiring", f"{PFX}succession = yes"])],
   ttrigger=[f"has_country_flag = {PFX}gensec_bre", f"has_country_flag = {PFX}bre_retiring", f"NOT = {{ has_global_flag = {PFX}dead_bre }}"])
ev(33, "flag", "A New General Secretary",
   "The Plenum of the Central Committee of the CPSU has unanimously elected §Y[SOV.GetLeader]§! General Secretary. Foreign governments study "
   "his biography; Kremlinologists study the order of the leaders on the Lenin Mausoleum.",
   [o("The Party is united.")], kind="news", major=True)

DEATHS = {"bre": (90, "Leonid Ilyich Brezhnev, General Secretary since 1964, has died in his sleep at his dacha in Zarechye."),
          "kos": (91, "Alexei Nikolayevich Kosygin, the reformer of 1965 and for fourteen years Chairman of the Council of Ministers, has died of a heart attack."),
          "pod": (92, "Nikolai Viktorovich Podgorny, former Chairman of the Presidium of the Supreme Soviet, has died in Moscow."),
          "sus": (93, "Mikhail Andreyevich Suslov, the grey cardinal and chief ideologue of the Party for three decades, has died after a stroke."),
          "and": (94, "Yuri Vladimirovich Andropov has died of kidney failure. For months he had governed from a hospital bed in Kuntsevo."),
          "gre": (95, "Marshal of the Soviet Union Andrei Antonovich Grechko, Minister of Defence, has died suddenly at his dacha."),
          "ust": (96, "Marshal of the Soviet Union Dmitry Fyodorovich Ustinov, the armourer of the Soviet state, has died after a short illness."),
          "che": (97, "Konstantin Ustinovich Chernenko has died of emphysema and heart failure after thirteen months in office.")}
for k, (n, text) in DEATHS.items():
    d = E.GENSEC[k][2]
    if k == "bre":
        trig = [f"OR = {{ AND = {{ NOT = {{ has_country_flag = {PFX}kremlin_doctors }} date > 1982.11.9 }} "
                f"AND = {{ has_country_flag = {PFX}kremlin_doctors date > 1984.11.9 }} }}"]
    else:
        trig = [f"date > {d}"]
    if k in E.STANDIN:
        text += f" In the Politburo §Y{E.STANDIN[k][0]}§! now speaks for his camp: his plenum and his course pass to him."
    ev(n, "funeral", f"Death of {GS[k]}",
       text + " The Hall of Columns of the House of the Unions is draped in black; the funeral will take place on Red Square.",
       [o("The Party mourns its General Secretary.", [f"{PFX}succession = yes"], trig=[f"has_country_flag = {PFX}gensec_{k}", "emerging_communist_state_are_in_power = yes"]),
        o("He will be buried at the Kremlin Wall.", [f"if = {{ limit = {{ has_country_flag = {PFX}gensec_{k} }} clr_country_flag = {PFX}gensec_{k} }}"],
          trig=[f"NOT = {{ AND = {{ has_country_flag = {PFX}gensec_{k} emerging_communist_state_are_in_power = yes }} }}"])],
       trigger=["original_tag = SOV", f"has_country_flag = {PFX}initialized", f"NOT = {{ has_global_flag = {PFX}dead_{k} }}"] + trig,
       mtth=30, once=True,
       immediate=[f"set_global_flag = {PFX}dead_{k}"] + ([] if k in E.STANDIN else [f"clr_country_flag = {PFX}candidate_{k}"]) +   # a stand-in keeps the candidacy
                 [f"if = {{ limit = {{ has_country_flag = {PFX}heir_{k} }} clr_country_flag = {PFX}heir_{k} }}"])

# ================================================================ party congresses (70-81)
CONGRESSES = [(24, "1971.3.30"), (25, "1976.2.24"), (26, "1981.2.23"), (27, "1986.2.25"), (28, "1990.7.2")]
import datetime


def minus(d, days):
    y, m, dd = [int(x) for x in d.split(".")]
    t = datetime.date(y, m, dd) - datetime.timedelta(days=days)
    return f"{t.year}.{t.month}.{t.day}"


BASE_T = ["original_tag = SOV", f"has_global_flag = {PFX}politburo_system", f"NOT = {{ has_global_flag = {PFX}federation_council }}"]
for i, (c, d) in enumerate(CONGRESSES):
    ai_apply = ["every_country = {", f"limit = {{ is_ai = yes {PFX}can_apply = yes has_political_power > 50 }}",
                "random = {", "chance = 50", "add_political_power = -25", f"set_country_flag = {PFX}applied", f"set_country_flag = {PFX}bid_25", "}", "}"]
    ev(70 + i, "congress", f"Applications for the {c}th Congress", "Applications open.", [o("Open.")], hidden=True, once=True, mtth=1,
       trigger=BASE_T + [f"date > {minus(d, 91)}"],
       immediate=[f"set_variable = {{ global.{PFX}congress = {c} }}", f"set_global_flag = {PFX}applications_open"] + ai_apply)
    ai_sov = []
    if c == 24:
        ai_sov = ["if = {", f"limit = {{ is_ai = yes check_variable = {{ global.{PFX}seat_count < 3 }} country_exists = BLR BLR = {{ {PFX}is_union_republic = yes NOT = {{ has_country_flag = {PFX}seat }} }} }}",
                  f"BLR = {{ {PFX}grant_seat = yes }}", "}"]
    if c == 26:
        ai_sov = ["if = {", f"limit = {{ is_ai = yes country_exists = AZE AZE = {{ {PFX}is_union_republic = yes NOT = {{ has_country_flag = {PFX}seat }} }} }}",
                  f"if = {{ limit = {{ BLR = {{ has_country_flag = {PFX}seat }} }} BLR = {{ {PFX}leave_seat = yes }} }}",
                  f"if = {{ limit = {{ check_variable = {{ global.{PFX}seat_count < 3 }} }} AZE = {{ {PFX}grant_seat = yes }} }}", "}"]
    ev(75 + i, "congress", f"The {c}th Congress Opens", "The congress opens.", [o("Open.")], hidden=True, once=True, mtth=1,
       trigger=BASE_T + [f"date > {minus(d, 1)}"],
       immediate=[f"set_variable = {{ global.{PFX}congress = {c} }}", f"clr_global_flag = {PFX}applications_open",
                  f"set_global_flag = {PFX}congress_open", f"clr_global_flag = {PFX}seat_changed_this_congress",
                  f"news_event = {{ id = {NS}.36 hours = 6 }}"] + ai_sov + [f"country_event = {{ id = {NS}.80 days = 30 }}"])
CLOSE = [f"clr_global_flag = {PFX}congress_open",
         "every_country = {", f"limit = {{ {PFX}is_union_republic = yes }}",
         "if = {", f"limit = {{ has_country_flag = {PFX}applied NOT = {{ has_country_flag = {PFX}seat }} }}",
         f"if = {{ limit = {{ has_country_flag = {PFX}bid_25 }} add_political_power = 12 }}",
         f"if = {{ limit = {{ has_country_flag = {PFX}bid_50 }} add_political_power = 25 }}",
         f"if = {{ limit = {{ has_country_flag = {PFX}bid_100 }} add_political_power = 50 }}", "}",
         f"clr_country_flag = {PFX}applied", f"clr_country_flag = {PFX}bid_25", f"clr_country_flag = {PFX}bid_50", f"clr_country_flag = {PFX}bid_100",
         f"clr_country_flag = {PFX}cadre_protection",
         f"if = {{ limit = {{ has_idea = {PFX}slanderer }} remove_ideas = {PFX}slanderer }}",
         "if = {", f"limit = {{ has_idea = {PFX}in_disgrace }}", f"add_to_variable = {{ {PFX}disgrace_left = -1 }}",
         f"if = {{ limit = {{ check_variable = {{ {PFX}disgrace_left < 1 }} }} remove_ideas = {PFX}in_disgrace }}", "}",
         "}",
         "if = {", f"limit = {{ has_country_flag = {PFX}rotate_cadres NOT = {{ has_global_flag = {PFX}seat_changed_this_congress }} check_variable = {{ global.{PFX}seat_count > 0 }} }}",
         f"country_event = {{ id = {NS}.81 days = 1 }}", "}",
         f"news_event = {{ id = {NS}.37 hours = 6 }}"]
ev(80, "congress", "The Congress Closes", "The congress closes.", [o("Close.")], hidden=True, immediate=CLOSE)
ev(81, "congress", "The Rotation of Cadres",
   "Our own rule demands it: at every Party Congress at least one republican seat must change hands. The Congress is over and no seat has changed. "
   "Which republic must give up its seat? We may then appoint a successor without the cost of an extraordinary plenum.",
   [o(f"The {SSR_NAME[t]} gives up its seat.", [f"{t} = {{ {PFX}dismiss_seat = yes }}", f"set_country_flag = {{ flag = {PFX}free_appointment days = 30 }}"],
      ai=1, trig=[f"{t} = {{ has_country_flag = {PFX}seat }}"]) for t in SSR])

# ================================================================ crises and history (40-63)
ev(40, "karabakh", "The Karabakh Petitions",
   "Tens of thousands of Armenians have signed petitions asking Moscow to transfer the Nagorno-Karabakh Autonomous Oblast from Azerbaijan to Armenia. "
   "In Stepanakert the regional soviet has voted for the transfer; in Baku the streets answer with anger.",
   [o("The borders of the republics are not to be changed.", E.cohesion(2), ai=3),
    o("Ask Baku to cede Nagorno-Karabakh to Armenia.", E.cohesion(-4) +
      [tt("karabakh_request", "§YAzerbaijan decides§! whether to hand over Nagorno-Karabakh."),
       f"if = {{ limit = {{ country_exists = AZE }} AZE = {{ country_event = {{ id = {NS}.62 days = 1 }} }} }}"], ai=1)])
ev(62, "karabakh", "Moscow Asks for Karabakh",
   "The Central Committee asks the Azerbaijani leadership to agree to the transfer of Nagorno-Karabakh to the Armenian SSR. "
   "Refusing Moscow has its price; agreeing would cost the government in Baku its standing at home.",
   [o("Agree to hand over the oblast.", [tt("karabakh_armenia", "§YArmenia decides§! whether to take over Nagorno-Karabakh."), "add_stability = -0.05",
                                        f"if = {{ limit = {{ country_exists = ARM }} ARM = {{ country_event = {{ id = {NS}.64 days = 1 }} }} }}",
                                        f"FROM = {{ country_event = {{ id = {NS}.900 days = 1 }} }}"], ai=1),
    o("Karabakh is Azerbaijan.", ["add_stability = 0.02", f"FROM = {{ country_event = {{ id = {NS}.901 days = 1 }} }}"], ai=4)])
ev(64, "karabakh", "Karabakh Comes to Armenia",
   "Baku has agreed to hand over the Nagorno-Karabakh Autonomous Oblast. Taking it means taking responsibility for its people - and for the anger "
   "of our neighbour.",
   [o("Miatsum! Unification!", ["if = { limit = { AZE = { owns_state = 710 } } transfer_state = 710 }", "add_stability = 0.03"], ai=3),
    o("Leave it as it is.", [], ai=1)])
ev(41, "pact", "The Warsaw Pact Is Dissolved",
   "Moscow has announced the dissolution of the Warsaw Treaty Organisation. The Soviet troops will go home; every former member is free to choose "
   "its own alliances.",
   [o("We will go our own way.")])
ev(42, "empire", "The Imperial Question",
   "The Russian Party must answer the question that has haunted Russia since 1917: is Russia the Union, or is the Union a burden on Russia? "
   "Some want to hold every republic, by force if need be; others want a smaller, Russian Union of those who wish to stay.",
   [o("Hold the Union together.", E.cohesion(5) + E.dyn_change(f"{PFX}party_state_modifier", f"{PFX}party_state", {"police_cost_multiplier_modifier": 0.10}), ai=3),
    o("A smaller Russian Union.", [tt("imperial_release", "Every Union republic is offered §Yindependence§!. Each republic decides for itself."), "hidden_effect = {",
                                   f"every_subject_country = {{ limit = {{ {PFX}is_union_republic = yes }} country_event = {{ id = {NS}.60 days = 2 }} }}", "}"], ai=1)])
ev(43, "grain", "A Poor Harvest",
   "Drought in the Volga region and an early frost in Kazakhstan: the grain harvest has fallen far short of the plan. Unless we find grain, "
   "the shops will be empty by spring.\n\nThe decision §YBuy Grain Abroad§! can prevent the worst for 120 days.",
   [o("The kolkhozes must deliver.")], once=False, mtth=900,
   trigger=["original_tag = SOV", f"has_country_flag = {PFX}initialized", "date > 1974.6.1", f"has_idea = {PFX}agrarian_problem",
            f"NOT = {{ has_country_flag = {PFX}harvest_cooldown }}", f"NOT = {{ has_country_flag = {PFX}poor_harvest }}"],
   immediate=[f"set_country_flag = {{ flag = {PFX}harvest_cooldown days = 1460 }}", f"set_country_flag = {{ flag = {PFX}poor_harvest days = 120 }}",
              f"country_event = {{ id = {NS}.53 days = 120 }}"])
ev(53, "grain", "Empty Shelves", "The harvest shortfall reaches the shops.", [o("Endure.")], hidden=True,
   immediate=[f"if = {{ limit = {{ NOT = {{ has_country_flag = {PFX}grain_bought }} }} add_stability = -0.05 }}"])
ev(44, "dissolve", "The Union Is Breaking Apart",
   "Union cohesion has collapsed. Republican parliaments ignore the laws of the Union, the ministries in Moscow no longer reach the provinces, "
   "and national fronts march in every capital from Tallinn to Dushanbe.",
   [o("We must save what can be saved.", ["add_stability = -0.05"])], once=False, mtth=30,
   trigger=["original_tag = SOV", f"has_global_flag = {PFX}politburo_system", f"check_variable = {{ {PFX}union_cohesion < 15 }}",
            f"NOT = {{ has_country_flag = {PFX}disintegration_cooldown }}"],
   immediate=[f"set_country_flag = {{ flag = {PFX}disintegration_cooldown days = 365 }}",
              "every_subject_country = {", f"limit = {{ {PFX}is_union_republic = yes NOT = {{ has_country_flag = {PFX}seat }} }}",
              f"if = {{ limit = {{ is_ai = yes NOT = {{ has_idea = {PFX}declaration_of_sovereignty }} }} add_ideas = {PFX}declaration_of_sovereignty }}",
              f"else_if = {{ limit = {{ is_ai = no }} country_event = {{ id = {NS}.54 days = 1 }} }}", "}"])
ev(54, "demo", "The Union Is Breaking Apart",
   "Moscow has lost control. The Union ministries no longer reach our republic and the national front fills the squares. "
   "What our republic does now is our own decision.",
   [o("Our time has come.", [tt("disintegration_free", "Our national decisions (§YPopular Front§!, §YDeclaration of Sovereignty§!, §YReferendum§!) are open to us.")])])
ev(45, "reactor", "Accident at the Nuclear Power Plant",
   "An explosion has destroyed the reactor of an RBMK unit. A cloud of radioactive dust drifts over the republics and towards Scandinavia, where "
   "measuring stations raise the alarm before Moscow says a word.",
   [o("Evacuate the zone and say nothing.", ["add_stability = -0.05"] + E.cohesion(-3) + [f"set_temp_variable = {{ {PFX}gdp_share = 0.01 }}", f"{PFX}pay_gdp_share = yes"], ai=2),
    o("Tell the world the truth.", ["add_stability = -0.03"] + E.cohesion(-2) + ["add_political_power = -50",
                                     f"set_temp_variable = {{ {PFX}gdp_share = 0.01 }}", f"{PFX}pay_gdp_share = yes"], ai=1)],
   once=True, mtth=3650, trigger=["original_tag = SOV", f"has_country_flag = {PFX}rbmk", "date > 1975.1.1"],
   mtth_mods=[f"modifier = {{ factor = 2 has_completed_focus = {PFX}vver_reactors }}"],
   immediate=[f"clr_country_flag = {PFX}rbmk"])
ev(46, "desert", "The Dying Sea",
   "The Aral Sea is shrinking. The rivers that fed it now water the cotton fields of Uzbekistan and Turkmenistan; the fishing fleets of Muynak lie in the sand, "
   "and salt storms carry poison across Karakalpakstan.",
   [o("Divert the Siberian rivers to the south.", ["add_political_power = -50"] + E.cohesion(2), ai=1),
    o("The cotton plan comes first.", E.cohesion(-3) + ["add_stability = -0.02"], ai=2)],
   once=True, mtth=365, trigger=["original_tag = SOV", f"has_country_flag = {PFX}aral_disaster", "date > 1980.1.1"])
ev(47, "coup", "The Orthodox Conspire",
   "The reformers dominate the Politburo, and the old guard has had enough. Generals, KGB officers and regional secretaries meet at dachas outside Moscow; "
   "the word 'Hungary' is heard more and more often.",
   [o("Make concessions to the orthodox.", E.bop(0.15) + fac("communist_cadres", 10), ai=2),
    o("Purge the conspirators.", ["add_stability = -0.05"] + fac("the_military", -10) + fac("intelligence_community", -10), ai=1)])
ev(48, "coup", "The Reformers Call on the Army",
   "Reaction rules the Politburo. Reform-minded ministers and economists warn that the country is heading for ruin, and some of them have begun "
   "to sound out the generals.",
   [o("Step back.", E.bop(-0.15) + fac("communist_cadres", -5), ai=2),
    o("Show a firm hand.", ["add_stability = -0.05", "add_war_support = 0.03"] + fac("the_military", 10), ai=1)])
ev(49, "afghan", "The Soviet Withdrawal",
   "Moscow has informed our government that the limited contingent will leave Afghanistan. The last Soviet columns will cross the Amu Darya; "
   "from now on our army stands alone.",
   [o("We will defend ourselves.", [f"if = {{ limit = {{ has_idea = {PFX}limited_contingent }} remove_ideas = {PFX}limited_contingent }}"])])
ev(50, "strike", "Gdansk, December 1970",
   "Strikes have broken out in the shipyards of Gdansk, Gdynia and Szczecin after a sudden rise in food prices. The Polish militia has opened fire; "
   "Gomulka has fallen and Edward Gierek takes over. Warsaw waits to hear what Moscow thinks.",
   [o("Help Gierek with credits.", [f"set_temp_variable = {{ {PFX}gdp_share = 0.002 }}", f"{PFX}pay_gdp_share = yes",
                                     "if = { limit = { country_exists = POL } POL = { add_opinion_modifier = { target = ROOT modifier = COLDWAR_SOV_economic_partners } } }"], ai=2),
    o("Order calm and discipline.", E.bop(0.05) + ["add_stability = 0.01"], ai=1)],
   once=True, mtth=1, trigger=["original_tag = SOV", f"has_country_flag = {PFX}initialized", "date > 1970.12.14", "date < 1971.6.1"])
ev(51, "writer", "A Nobel Prize for Solzhenitsyn",
   "The Swedish Academy has awarded the Nobel Prize in Literature to Aleksandr Solzhenitsyn. The writer asks whether he will be allowed to return "
   "if he travels to Stockholm.",
   [o("If he goes, he stays there.", fac("intelligence_community", 5) + E.bop(0.03), ai=2),
    o("Let him collect his prize.", ["add_political_power = -25"] + fac("communist_cadres", -5) + E.bop(-0.03), ai=1)],
   once=True, mtth=1, trigger=["original_tag = SOV", f"has_country_flag = {PFX}initialized", "date > 1970.10.7", "date < 1971.6.1"])
ev(52, "rocket", "Soyuz 11",
   "The crew of Soyuz 11 - Georgy Dobrovolsky, Vladislav Volkov and Viktor Patsayev - has been found dead in their capsule after landing. "
   "A valve opened during the separation of the modules. The first space station, Salyut 1, has lost its first crew.",
   [o("Their names will live in the stars.", ["add_stability = -0.02"])],
   once=True, mtth=1, trigger=["original_tag = SOV", f"has_country_flag = {PFX}initialized", "date > 1971.6.29", "date < 1971.12.1"])
ev(60, "referendum", "Moscow Offers Independence",
   "The government of the Union has offered our republic the right to leave the Soviet Union. Independence would be ours, with all its promises "
   "and all its dangers.",
   [o("Declare independence.", [f"if = {{ limit = {{ has_country_flag = {PFX}seat }} {PFX}leave_seat = yes }}", "SOV = { end_puppet = ROOT }"] + E.cohesion(-3) +
      [tt("union_subsidies_saved", "Moscow no longer pays our Union subsidies: the Soviet Union gains §G0.3%§! of its GDP."),
       f"hidden_effect = {{ SOV = {{ set_temp_variable = {{ {PFX}gdp_share = 0.003 }} {PFX}receive_gdp_share = yes }} }}"], ai=1),
    o("We stay in the Union.", E.cohesion(1), ai=2)])
ev(61, "parliament", "The New Union Treaty",
   "Moscow offers our republic a new Union treaty: broad autonomy, our own budget and laws, and a voice in the Union that no longer depends on the Politburo. "
   "No one will be forced to stay - or to leave.",
   [o("Sign the treaty.", [f"add_ideas = {PFX}union_treaty_member"] + E.cohesion(2) + [f"SOV = {{ country_event = {{ id = {NS}.900 days = 1 }} }}"], ai=3),
    o("Not yet.", [f"SOV = {{ country_event = {{ id = {NS}.901 days = 1 }} }}"], ai=1)])
ev(63, "olympics", "An Invitation to Moscow",
   "The organising committee of the Moscow Olympics has invited our national team. Some in our government want to boycott the Games "
   "in protest against Soviet policy; our athletes want to compete.",
   [o("Our athletes will go to Moscow.", ["add_opinion_modifier = { target = SOV modifier = COLDWAR_SOV_olympic_guest }",
                                           "reverse_add_opinion_modifier = { target = SOV modifier = COLDWAR_SOV_olympic_guest }"], ai=2),
    o("We boycott the Games.", ["SOV = { add_opinion_modifier = { target = ROOT modifier = COLDWAR_SOV_olympic_boycott } }"],
      ai="base = 1 modifier = { add = 2 check_variable = { global.mdcw_cw_tension > 60 } }")])

for n, t, d, a in [(900, "[From.GetNameDefCap] Accepts", "Our envoys report that [From.GetNameDef] has accepted our proposal. The agreed terms now take effect.", "Excellent."),
                   (901, "[From.GetNameDefCap] Declines", "[From.GetNameDefCap] has turned down our proposal. We will have to find another way.", "Unfortunate.")]:
    ev(n, "handshake", t, d, [o(a)])
