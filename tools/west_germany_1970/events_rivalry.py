# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""Events of the inner-German rivalry (namespace COLDWAR_GGR)."""
from cw_lib import *
from events_lib import E, O
from rivalry import EVR, R, CRISES, TREATIES, ANSWERS, kl, dr, lever, log, channel_unlock

OPEN = "set_country_flag = cwgg_open\nset_variable = { cwgg_tab = 2 }\n" + f"{R}_gui_refresh = yes"
OPEN3 = "set_country_flag = cwgg_open\nset_variable = { cwgg_tab = 1 }\n" + f"{R}_gui_refresh = yes"

# Rounds, countdowns and the final resolution run on the monthly tick (no recurring hidden events).
DDR_ONLY_HUMAN = "is_ai = no"

# ---------------------------------------------------------------- crisis outbreak
OUTBREAK = {
    1: ("Trouble on the Transit Routes",
        "At Helmstedt and Dreilinden the East German border troops are taking every car apart. Lorries wait for twelve hours, coaches are turned back, a Bundestag deputy has been refused passage. East Berlin speaks of 'abuse of the transit routes'. West Berlin, a hundred and seventy kilometres inside the GDR, feels the noose tighten."),
    2: ("Shots at the Border",
        "A young man from Thuringia tried to cross the fence near the Werra last night. The border troops opened fire. He bled to death in the strip while West German customs officers watched from fifty metres away. The pictures are on every front page; East Berlin calls it the defence of the state border."),
    3: ("A Spy in Bonn",
        "The Federal Office for the Protection of the Constitution has arrested a man with access to secrets he should never have seen. The trail leads to the HVA in East Berlin - and the newspapers are asking how high up it goes."),
    4: ("Refugees in the Embassy",
        "Hundreds of East Germans have climbed the fence of the West German embassy and refuse to leave until they can go west. More arrive every hour. The host government wants the problem gone; East Berlin wants them back."),
    5: ("A State Recognises the GDR",
        "A government in the Third World has established diplomatic relations with the GDR. Under the doctrine Bonn has followed since 1955 that is an unfriendly act. If Bonn does nothing, others will follow; if it breaks off relations, it may lose another friend."),
    6: ("The Missiles of Europe",
        "Soviet SS-20 missiles can reach every capital in Western Europe. NATO answers with Pershing II and cruise missiles - to be stationed in the Federal Republic. East Berlin warns of an 'ice age' between the German states; hundreds of thousands march in the Hofgarten."),
    7: ("A Dangerous Exercise",
        "NATO is rehearsing nuclear release procedures. In Moscow and East Berlin the intelligence services report that the exercise may be cover for a real attack. Soviet aircraft are on strip alert in the GDR, the National People's Army has cancelled leave."),
    8: ("Expelled for His Songs",
        "East Berlin has stripped a dissident of his citizenship while he was on a concert tour in the West. Writers and artists in the GDR have signed a protest letter. Every Western camera wants an interview; every SED newspaper calls him a traitor."),
    9: ("The Elbe Question",
        "Where exactly does the border run along the Elbe - in the middle of the river, as East Berlin insists, or on its eastern bank, as the Allied protocols of 1944 say? GDR patrol boats have turned back West German fishermen."),
    10: ("The People Rise",
        "The crushed protests are back - bigger. Factories are on strike, crowds have occupied SED district offices, and in some towns the police have taken off their caps and joined the demonstrators. In the East there are calls for help from the West. In Bonn there are people who want to give it."),
}
for c in CRISES:
    cid, key, name = c[0], c[1], c[2]
    title, desc = OUTBREAK[cid]
    E(f"{EVR}.{100 + cid}", title,
      desc + f"\n\nA §Y{name}§! has begun. Its intensity starts at §Y{c[3]}§!. Every six months a round is resolved: both sides choose a course, and the crisis ends when its intensity falls to zero, reaches the brink at 100, or freezes after §Y{c[5]}§! rounds.",
      c[7],
      [O("Convene the crisis staff.", OPEN, ai=1), O("Let the ministries handle it for now.", "", ai=10)])

# ---------------------------------------------------------------- round report
E(f"{EVR}.3", "Crisis Report: Round [?cwgg_krise_runde|0]",
  "",
  "GFX_politics_talks",
  [O("Open the situation map.", OPEN), O("Noted.")],
  descs=[("", "[RV_RoundReport]\n\nCrisis intensity: §Y[?cwgg_krise_int|0]§! after §Y[?cwgg_krise_runde|0]§! of §Y[?cwgg_krise_max|0]§! rounds.\n\nChoose a course for the next round in the §YInner-German Relations§! window; it is resolved in six months. Without a choice, Bonn waits and sees.")])

E(f"{EVR}.5", "The Inner-German Relationship Escalates",
  "", "GFX_missiles_on_road", [O("Open the situation map.", OPEN3), O("Noted.")],
  descs=[("check_variable = { cwgg_stufe = 4 }", "Relations with the GDR have reached the stage of §RConfrontation§!. Trade is halved, the armies watch each other along the border and every incident could turn into a crisis that neither side controls."),
         ("check_variable = { cwgg_stufe > 4 }", "§RWar danger.§! Both German armies are on alert, the superpowers are on the telephone and the newspapers are printing maps of the Fulda Gap. Every decision in the next weeks can decide between peace and war.")])

# ---------------------------------------------------------------- outcome
E(f"{EVR}.10", "The Crisis Is Over",
  "", "GFX_treaty", [O("Back to business.", "", ai=10), O("Open the situation map.", OPEN3, ai=0)],
  descs=[("check_variable = { cwgg_last_out = 1 }", "East Berlin has given way. In Bonn the government speaks of steadiness, in Neues Deutschland of 'provocations repelled'. The opposition has one argument fewer."),
         ("check_variable = { cwgg_last_out = 2 }", "East Berlin has had its way. The SED celebrates a victory over 'revanchism', the opposition in Bonn speaks of weakness, and in Washington people ask whether Bonn can be relied on."),
         ("check_variable = { cwgg_last_out = 3 }", "The crisis has not been settled - it has frozen. Nobody gave way, nobody won, and the issue is still there. It may flare up again."),
         ("check_variable = { cwgg_last_out = 4 }", "We gave way at the brink. The world breathes again, and the opposition sharpens its knives. East Berlin will remember that pressure works."),
         ("check_variable = { cwgg_last_out = 5 }", "East Berlin blinked first. Its troops stand down and its press falls silent. It is a victory - and the GDR leadership will not forgive the humiliation soon."),
         ("check_variable = { cwgg_last_out = 6 }", "Moscow has reined in its ally. The Soviet ambassador visited the SED leadership at night; by morning the crisis was over. Bonn has won - but the decision was taken in the Kremlin."),
         ("check_variable = { cwgg_last_out = 7 }", "Both sides have moved. Nobody calls it a victory, both governments call it a success - and the communiqué is long enough that everyone can find a sentence they like.")])

# ---------------------------------------------------------------- the brink
E(f"{EVR}.11", "At the Brink",
  "The crisis has reached its peak. In East Berlin the Politburo is in permanent session, in Bonn the cabinet meets in the bunker plan of the Ahr valley. One side has to give way - or the next step is no longer politics.",
  "GFX_missiles_on_road",
  [O("Give way. Nothing is worth a war.",
     J("set_temp_variable = { cwgg_t_out = 4 }", f"{R}_end_crisis = yes", v("cwger_scandal", 8), party("cdu", 0.004)), ai=60),
   O("Show resolve. Let them blink.",
     J("set_variable = { cwgg_countdown = 3 }", "set_variable = { cwgg_krise_int = 100 }", "if = { limit = { check_variable = { cwgg_mob_brd < 3 } } add_to_variable = { cwgg_mob_brd = 1 } }",
       log("brink", "Bonn shows resolve. A three-month countdown has begun."), f"{R}_update_stage = yes",
       f"if = {{ limit = {{ DDR = {{ is_ai = no }} }} DDR = {{ country_event = {{ id = {EVR}.210 days = 1 }} }} }}", f"{R}_gui_refresh = yes",
       tt(f"{P}_tt_countdown", "§RA countdown of three months begins.§! Every month East Berlin may give way - or we may. If nobody does, the Kremlin will usually pull its ally back from the edge - unless East Berlin or Moscow decide that the time for patience is over. Then it is war.")),
     ai="base = 25 modifier = { factor = 2 check_variable = { ruling_party = 1 } }"),
   O("Ask the superpowers to mediate.",
     J("set_variable = { cwgg_krise_int = 50 }", "set_variable = { cwgg_krise_monat = 0 }", tension(-2), f"{R}_ask_east_berlin = yes",
       log("mediation", "Washington and Moscow mediate. The crisis is defused, for now."), f"{R}_update_stage = yes", f"{R}_gui_refresh = yes",
       tt(f"{P}_tt_mediation", "Crisis intensity falls to §Y50§!; the next round is resolved in six months.")),
     trig="OR = { check_variable = { cwgg_kanal_draht = 1 } has_idea = NATO_member }", ai=40)])

E(f"{EVR}.14", "East Berlin Gives Way",
  "In the middle of the night the GDR news agency announced that 'the measures have served their purpose'. The border troops are back in their barracks, the access routes are open. Our nerve has held.",
  "GFX_handshake_black",
  [O("Do not gloat.", f"if = {{ limit = {{ check_variable = {{ cwgg_krise_typ > 0 }} }} set_temp_variable = {{ cwgg_t_out = 5 }} {R}_end_crisis = yes }}")])

E(f"{EVR}.15", "Countdown: [?cwgg_countdown|0] Months",
  "East Berlin has not given way. The Soviet divisions in the GDR are on alert, NATO's commanders want instructions. Every day we hold our course, the risk grows - and so does the price of giving way.\n\nBundeswehr alert level: §Y[?cwgg_mob_brd|0]§! | NVA alert level: §Y[?cwgg_mob_ddr|0]§! | Moscow's guarantee for the GDR: §Y[?DDR.cwddr_moscow_backing|0]§!",
  "GFX_GER_Panzer_strasse",
  [O("Hold our course.", "", ai=50, tt="The countdown continues. Next month: another decision."),
   O("Give way after all.", J("set_variable = { cwgg_countdown = 0 }", "set_temp_variable = { cwgg_t_out = 4 }", f"{R}_end_crisis = yes",
                              v("cwger_scandal", 12)), ai=50, trig="check_variable = { cwgg_krise_typ > 0 }"),
   O("Strike first.", J("set_country_flag = cwgg_strike_ordered", f"country_event = {{ id = {EVR}.19 days = 1 }}"),
     trig="has_country_flag = cwgg_liberation_doctrine check_variable = { cwgg_mob_brd > 2 } check_variable = { cwgg_klima < -79 } check_variable = { cwgg_aufm_brd > 1 }", ai=0)])

E(f"{EVR}.19", "The Order",
  "The Inspector General is waiting for a signature. Once it is given, the Bundeswehr crosses the inner-German border at dawn. Whether NATO follows depends on how much Washington still trusts us; whether the Soviet Union fights depends on how much it still needs the GDR.",
  "GFX_news_german_army",
  [O("Sign.", J("set_variable = { cwgg_countdown = 0 }", f"{R}_final_resolution = yes",
                tt(f"{P}_tt_strike", "§RWar with the GDR begins.§!")), ai=0),
   O("Tear it up.", "clr_country_flag = cwgg_strike_ordered", ai=100, tt="The countdown continues.")])

E(f"{EVR}.18", "Brotherly Help?",
  "The rising in the East is being crushed. The insurgents are asking the Federal Republic for help - the same help that Hungary in 1956 hoped for in vain. The Bundeswehr could be at the Elbe in two days. The question is who else would be.",
  "GFX_german_riot",
  [O("Send the Bundeswehr.", J("set_temp_variable = { cwgg_t_path = 3 }", f"{R}_war_start = yes",
                               tt(f"{P}_tt_brotherly", "§RWar with the GDR begins.§! The Soviet Union joins if its guarantee for the GDR is still at least §Y50§!.")), ai=0,
     trig="check_variable = { cwgg_aufm_brd > 0 }"),
   O("Open the border to everyone who flees instead.", J("add_to_variable = { cwgg_krise_int = -20 }", dv("cwddr_exit_pressure", 8), stab(-0.02)), ai=100)])

E(f"{EVR}.20", "East Berlin Names a Price",
  "Through the channel the other side has made an offer: the crisis ends quietly - for money. A credit, a transit payment, a few hundred million for 'humanitarian matters'.",
  "GFX_politics_negotiations",
  [O("Pay. Quiet is worth it.", J(money_gdp(-0.0006), dv("cwddr_hard_currency", -5), "add_to_variable = { cwgg_krise_int = -30 }",
                                  "clamp_variable = { var = cwgg_krise_int min = 0 max = 100 }", f"{R}_gui_refresh = yes"), ai=60),
   O("We do not pay for good behaviour.", J("add_to_variable = { cwgg_krise_int = 5 }", "clamp_variable = { var = cwgg_krise_int min = 0 max = 100 }"), ai=40)])

E(f"{EVR}.21", "Launch Warning",
  "03:12. The early-warning radars of the Warsaw Pact report missiles in the air. The National People's Army has gone to combat readiness; in the GDR's air defence bunkers the officers are waiting for orders. Our own screens show nothing. In twenty minutes the question will answer itself.",
  "GFX_missiles_on_road",
  [O("Call Moscow on the hotline.", J("add_to_variable = { cwgg_krise_int = -40 }", "add_to_variable = { cwgg_mob_ddr = -1 }", f"{R}_set_stage_modifiers = yes",
                                      log("hotline", "A false alarm is cleared up on the hotline."), f"{R}_gui_refresh = yes"),
     trig="check_variable = { cwgg_kanal_draht = 1 }", ai=100),
   O("Stand down our own forces and hope they see it.", J("set_variable = { cwgg_mob_brd = 1 }", f"{R}_set_stage_modifiers = yes", f"""random_list = {{
	75 = {{ add_to_variable = {{ cwgg_krise_int = -20 }} {log("alarm_ok", "The alarm was a sensor fault. Both armies stand down.")} }}
	25 = {{ set_temp_variable = {{ cwgg_t_path = 4 }} {R}_war_start = yes }}
}}""", tt(f"{P}_tt_alarm", "§G75%§!: the alarm is recognised as an error. §R25%§!: war.")), ai=50)])

# ---------------------------------------------------------------- war
E(f"{EVR}.30", "The State of Defence",
  "The Bundestag and Bundesrat have declared the state of defence under Article 115a of the Basic Law. Command of the armed forces passes to the Chancellor. The Joint Committee stands ready to replace a parliament that may no longer be able to meet.",
  "GFX_news_german_army",
  [O("Defend the free part of Germany.", J(ws(0.15), stab(-0.05), v("cwger_peace_movement", 15), protest(10)))],
  descs=[("check_variable = { cwgg_war_path = 1 }", "We have attacked. The Bundestag and Bundesrat have declared the state of defence under Article 115a of the Basic Law - a constitution written for a defensive war now carries an offensive one. Command of the armed forces passes to the Chancellor."),
         ("check_variable = { cwgg_war_path = 2 }", "The National People's Army has crossed the border. West Berlin is under fire. The Bundestag and Bundesrat have declared the state of defence under Article 115a of the Basic Law; command of the armed forces passes to the Chancellor."),
         ("check_variable = { cwgg_war_path = 3 }", "The Bundeswehr is crossing the Elbe to help the rising in the East. The Bundestag has declared the state of defence; command passes to the Chancellor. Whether the Soviet Union will stand aside is the only question that matters now."),
         ("check_variable = { cwgg_war_path = 4 }", "A false alarm became a real war. Nobody in Bonn or East Berlin wanted it; both armies are now fighting it. The Bundestag has declared the state of defence under Article 115a.")])

E(f"{EVR}.31", "The Threshold",
  "Six weeks of war in the middle of Europe. NATO's planners are asking whether conventional defence can hold, and the word nobody wants to say is on every desk. There is still a way back: a ceasefire on the present lines.",
  "GFX_missiles_on_road",
  [O("Offer a ceasefire.", f"""if = {{ limit = {{ OR = {{ DDR = {{ surrender_progress > 0.25 }} DDR = {{ check_variable = {{ cwddr_moscow_backing < 50 }} }} surrender_progress > 0.35 }} }}
	white_peace = DDR
	if = {{ limit = {{ country_exists = SOV has_war_with = SOV }} white_peace = SOV }}
}}
else = {{
	{log("ceasefire_no", "East Berlin rejects a ceasefire.")}
	country_event = {{ id = {EVR}.31 days = 60 }}
}}""" + "\n" + tt(f"{P}_tt_ceasefire", "East Berlin accepts if the war is going badly for one side or Moscow's guarantee has weakened below §Y50§!."), ai=60),
   O("Fight on.", J(ws(-0.05), f"country_event = {{ id = {EVR}.31 days = 90 }}"), ai=40)])

E(f"{EVR}.40", "Germany Under One Government",
  "The GDR has fallen. The Bundeswehr stands on the Oder, the SED leadership has fled or been arrested, and in the East the flags of the Federal Republic hang next to white sheets. Germany is united - by force of arms, against the will of half of Europe and with a debt to the East that will take a generation to pay.",
  "GFX_germany_flag",
  [O("Now we must win the peace.", J(f"if = {{ limit = {{ country_exists = DDR }} {P}_absorb_ddr = yes }}",
                                     f"set_global_flag = {P}_unity_achieved", f"set_global_flag = {P}_unity_by_force",
                                     v("cwger_east_burden", 25), stab(-0.05),
                                     "if = { limit = { country_exists = SOV } SOV = { add_opinion_modifier = { target = ROOT modifier = large_decrease } } }",
                                     "set_variable = { cwgg_stufe = 0 }", "clr_global_flag = cwgg_german_war", f"{R}_set_stage_modifiers = yes"))])

E(f"{EVR}.41", "Defeat",
  "The front has broken. West Berlin is lost, and in Moscow the terms are being written: a neutral Federal Republic, outside NATO, with an army the Warsaw Pact can count.",
  "GFX_gdratwarsov",
  [O("Accept the terms.", J("if = { limit = { country_exists = DDR } DDR = { transfer_state = 1251 } white_peace = DDR }",
                            "if = { limit = { country_exists = SOV has_war_with = SOV } white_peace = SOV }",
                            "if = { limit = { has_idea = NATO_member } NATO_leave = yes }", "if = { limit = { is_in_faction = yes } leave_faction = yes }",
                            stab(-0.15), f"{R}_cold_peace = yes"))])

E(f"{EVR}.42", "An Armistice",
  "The guns along the inner-German border have fallen silent. Nothing has been won; the dead are counted on both sides. The two German states remain - and hate each other more than at any time since 1961.",
  "GFX_treaty",
  [O("Never again.", J(f"{R}_cold_peace = yes", stab(-0.03)))])

# ---------------------------------------------------------------- treaties
E(f"{EVR}.50", "A Treaty Is Ready",
  "", "GFX_treaty",
  [O("Sign it.", f"""if = {{ limit = {{ OR = {{ {" ".join(f"check_variable = {{ cwgg_verh = {t[0]} }}" for t in TREATIES if t[8])} }} check_variable = {{ cwger_margin < 1 }} }}
	country_event = {{ id = {EVR}.51 days = 7 }}
}}
else = {{
{chr(10).join(f"	{'if' if i == 0 else 'else_if'} = {{ limit = {{ check_variable = {{ cwgg_verh = {t[0]} }} }} {R}_treaty_{t[0]} = yes }}" for i, t in enumerate(TREATIES))}
	set_variable = {{ cwgg_verh = 0 }}
	set_variable = {{ cwgg_verh_prog = 0 }}
}}
{R}_gui_refresh = yes""" + "\n" + tt(f"{P}_tt_ratify", "Treaties that change the legal position need a majority in the Bundestag; without it, ratification fails."), ai=95),
   O("Not yet - renegotiate the details.", J("set_variable = { cwgg_verh_prog = 60 }"), ai=5)],
  descs=[(f"check_variable = {{ cwgg_verh = {t[0]} }}", f"§Y{t[2]}§!\n\n{t[3]}\n\nThe negotiators have finished their work. The treaty is ready for signature.") for t in TREATIES])

E(f"{EVR}.51", "Ratification Fails",
  "The government no longer has a majority for the treaty. The opposition calls it a sell-out of German unity, and enough deputies of the coalition agree. The treaty stays unsigned.",
  "GFX_german_parliament_bundestag",
  [O("We will try again with a new majority.", J("set_variable = { cwgg_verh = 0 }", "set_variable = { cwgg_verh_prog = 0 }", kl(-5),
                                                 log("ratify_fail", "The Bundestag refuses to ratify a treaty with the GDR.")))])

E(f"{EVR}.60", "East Berlin Needs Money",
  "Through the Schalck-Golodkowski channel East Berlin lets it be known that the GDR's hard-currency position is 'tight'. A credit would be received with gratitude - and with gestures in return.",
  "GFX_stock_market",
  [O("Grant it - for humanitarian concessions.", J(money_gdp(-0.0006), lever("devisen", 1), kl(6), dv("cwddr_hard_currency", -8), dv("cwddr_west_dependency", 5),
                                                     log("credit_granted", "Bonn grants a credit. East Berlin eases travel rules.")), ai=60),
   O("Let them stew.", J(kl(-4), dv("cwddr_hard_currency", 3)), ai=40)])

E(f"{EVR}.70", "RAF Fugitives in the GDR",
  "The arrests of the HVA network have brought out something nobody expected: since 1980 the Stasi has given new identities to members of the Red Army Faction who wanted to leave the underground - and has trained others. East Berlin denies everything.",
  "GFX_RAF_Schulz",
  [O("Make it public.", J(kl(-15), dv("cwddr_recognition", -5), "add_to_variable = { cwger_raf_prisoners = 2 }", "add_to_variable = { cwger_raf_cadre = -3 }",
                          "clamp_variable = { var = cwger_raf_cadre min = 0 max = 120 }", stab(0.02))),
   O("Use it quietly.", J(lever("recht", 1), "add_to_variable = { cwger_raf_cadre = -3 }", "clamp_variable = { var = cwger_raf_cadre min = 0 max = 120 }"))])

# ---------------------------------------------------------------- East Berlin's moves
E(f"{EVR}.121", "The Compulsory Exchange Is Raised",
  "Every visitor from the West must now change more Deutschmarks into Ostmarks per day. Fewer pensioners will visit their sisters in Leipzig; more hard currency will flow to East Berlin.",
  "GFX_stock_market", [O("A wall made of money.", log("ddr_zwang", "East Berlin raises the compulsory exchange."))])
E(f"{EVR}.122", "The Border Is Tightened",
  "New fences, new mines, new SM-70 spring guns along the inner-German border. East Berlin calls it the protection of the state border; in the West it is called the death strip.",
  "GFX_Polizeiabsperrung", [O("The world must see this.", log("ddr_grenze", "East Berlin tightens the border regime."))])
E(f"{EVR}.123", "A Gesture from East Berlin",
  "East Berlin has quietly lowered the compulsory exchange for pensioners and dismantled a stretch of spring guns. Its press says nothing; its diplomats say a great deal.",
  "GFX_politics_talks", [O("Small steps.", log("ddr_gesture", "East Berlin makes a gesture of goodwill."))])

# ================================================================ East Berlin as a human player (multiplayer)
from gui import DT
from rivalry import STANCES

DT("RV_DDR_BonnLast", [(f"GER = {{ check_variable = {{ cwgg_last_h = {s_[0]} }} }}", f"cwgg_stance_{s_[1]}") for s_ in STANCES], "cwgg_rv_ddr_none", persistent=True)
L("cwgg_rv_ddr_none", "nothing yet")
DT("RV_DDR_Crisis", [(f"GER = {{ check_variable = {{ cwgg_krise_typ = {c[0]} }} }}", f"cwgg_crisis_{c[1]}") for c in CRISES], "cwgg_rv_ddr_none", persistent=True)

DDR_STATUS = ("§Y[RV_DDR_Crisis]§! | intensity §Y[?GER.cwgg_krise_int|0]§! | round §Y[?GER.cwgg_krise_runde|0]§! of §Y[?GER.cwgg_krise_max|0]§!\n"
              "Bonn's course in the last round: §Y[RV_DDR_BonnLast]§! | our initiative §Y[?GER.cwgg_init_ddr|0]§!\n"
              "Bundeswehr alert §Y[?GER.cwgg_mob_brd|0]§! | NVA alert §Y[?GER.cwgg_mob_ddr|0]§! | Moscow's guarantee §Y[?cwddr_moscow_backing|0]§!")
ESC = "GER = { check_variable = { cwgg_init_ddr > 0 } }"
ANSWER_TEXT = {
    1: ("Back down. The matter is not worth it.", "We give way this round. Intensity falls - and Bonn will say it won."),
    2: ("Stall. Time is on our side.", "Neither yield nor push. If we choose nothing, this is what happens."),
    3: ("Escalate. Bonn must learn what pressure means.", "Costs §Y1§! initiative. Raises intensity, more so against a soft Bonn; blunted by a Bundeswehr on alert."),
    4: ("Call on Moscow.", "Costs §Y1§! initiative. The stronger Moscow's guarantee, the harder it hits. If Bonn calls the Allies at the same time, the superpowers take over."),
    5: ("Name a price.", "Costs §Y1§! initiative. If Bonn is talking, it may pay for quiet."),
}
E(f"{EVR}.200", "Our Course in the Crisis",
  "The Politburo meets in the Central Committee building on Werderscher Markt. The next round of the crisis with Bonn is decided in six months; until then we hold the course we set now.\n\n" + DDR_STATUS,
  "GFX_politics_talks",
  [O(ANSWER_TEXT[a[0]][0], f"GER = {{ set_variable = {{ cwgg_ddr_wahl = {a[0]} }} {R}_gui_refresh = yes }}", ai=10,
     trig=(ESC if a[0] > 2 else ""), tt=ANSWER_TEXT[a[0]][1]) for a in ANSWERS],
  scope="DDR", trig="GER = { check_variable = { cwgg_krise_typ > 0 } }")

E(f"{EVR}.201", "The Crisis with Bonn Is Over",
  "", "GFX_treaty", [O("Noted.")],
  descs=[("GER = { OR = { check_variable = { cwgg_last_out = 1 } check_variable = { cwgg_last_out = 5 } } }", "We have given way. Neues Deutschland speaks of 'provocations repelled'; in the Politburo nobody believes it, and the hard-liners are counting the cost."),
         ("GER = { OR = { check_variable = { cwgg_last_out = 2 } check_variable = { cwgg_last_out = 4 } } }", "Bonn has given way. The Republic has defended its sovereignty, and the world has seen that the Federal Republic can be made to move."),
         ("GER = { check_variable = { cwgg_last_out = 3 } }", "The crisis has frozen. Nobody gave way, nobody won - and the issue may flare up again."),
         ("GER = { check_variable = { cwgg_last_out = 6 } }", "The Soviet ambassador came at night. By morning the crisis was over: Moscow has decided for us."),
         ("GER = { check_variable = { cwgg_last_out = 7 } }", "A compromise. Both sides have moved, both governments call it a success, and the communiqué is long enough for everyone to find a sentence they like.")],
  scope="DDR")

E(f"{EVR}.210", "Countdown: [?GER.cwgg_countdown|0] Months",
  "Bonn will not give way. The Soviet divisions are on alert, the National People's Army waits for orders and the border troops have been told to expect anything. Every month we hold, the risk grows - and so does the price of giving way.\n\nWhen the countdown runs out and nobody has blinked, we decide between restraint and war.\n\n" + DDR_STATUS,
  "GFX_GER_Panzer_strasse",
  [O("Hold firm.", "", ai=50, tt="The countdown continues."),
   O("Give way. The Republic will survive this.", J("GER = { set_variable = { cwgg_countdown = 0 } country_event = { id = " + EVR + ".14 days = 1 } }",
                                                 "add_stability = -0.03"), ai=50,
     trig="GER = { check_variable = { cwgg_countdown > 0 } check_variable = { cwgg_krise_typ > 0 } }")],
  scope="DDR")

E(f"{EVR}.211", "The Countdown Has Run Out",
  "Nobody has given way. Moscow's ambassador waits in the antechamber with a message from the Kremlin: the Soviet Union wants the crisis ended. Our generals have a different plan - West Berlin, in seventy-two hours.\n\n" + DDR_STATUS,
  "GFX_missiles_on_road",
  [O("Accept Moscow's restraint.", f"GER = {{ set_temp_variable = {{ cwgg_t_out = 6 }} {R}_end_crisis = yes }}", ai=90,
     tt="The crisis ends. Bonn has won - but the decision was taken in the Kremlin."),
   O("Order the attack on West Berlin.", f"GER = {{ set_temp_variable = {{ cwgg_t_path = 2 }} {R}_war_start = yes }}", ai=10,
     trig="check_variable = { cwddr_moscow_backing > 59 } GER = { check_variable = { cwgg_mob_ddr > 1 } check_variable = { cwgg_aufm_ddr > 0 } }",
     tt="§RWar with the Federal Republic begins.§! Needs Moscow's guarantee of at least §Y60§!, the NVA on alert level 2 and troops massed at the border.")],
  scope="DDR")

E(f"{EVR}.230", "War with the Federal Republic",
  "", "GFX_news_german_army", [O("For the socialist fatherland.", J("add_war_support = 0.10", "add_stability = -0.05"))],
  descs=[("GER = { OR = { check_variable = { cwgg_war_path = 1 } check_variable = { cwgg_war_path = 3 } } }", "The Bundeswehr has crossed the state border. The National People's Army is fighting on the Werra and the Elbe. Whether Moscow stands with us is decided in Moscow."),
         ("GER = { check_variable = { cwgg_war_path = 2 } }", "Our divisions are moving on West Berlin. There is no way back now."),
         ("GER = { check_variable = { cwgg_war_path = 4 } }", "A false alarm has become a real war. Nobody in East Berlin wanted it; the National People's Army is now fighting it.")],
  scope="DDR")

E(f"{EVR}.212", "Brinkmanship in Germany",
  "The countdown between Bonn and East Berlin has run out and neither side has blinked. Honecker's government asks the Kremlin for a decision: hold the GDR back - or let the National People's Army and the Group of Soviet Forces in Germany move on West Berlin.\n\n"
  "Moscow's guarantee for the GDR: §Y[?DDR.cwddr_moscow_backing|0]§! | NVA alert level §Y[?GER.cwgg_mob_ddr|0]§! | Bundeswehr alert level §Y[?GER.cwgg_mob_brd|0]§!",
  "GFX_missiles_on_road",
  [O("Rein in East Berlin.", f"GER = {{ if = {{ limit = {{ check_variable = {{ cwgg_krise_typ > 0 }} }} set_temp_variable = {{ cwgg_t_out = 6 }} {R}_end_crisis = yes }} }}", ai=100,
     tt="The crisis ends. Bonn has its way - but everyone knows the decision was taken in the Kremlin."),
   O("Let them move on West Berlin.", f"set_global_flag = cwgg_sov_ordered_attack GER = {{ if = {{ limit = {{ check_variable = {{ cwgg_krise_typ > 0 }} }} set_temp_variable = {{ cwgg_t_path = 2 }} {R}_war_start = yes }} }}", ai=0,
     trig="DDR = { is_ai = yes } GER = { check_variable = { cwgg_mob_ddr > 1 } check_variable = { cwgg_aufm_ddr > 0 } }",
     tt="§RThe GDR attacks the Federal Republic, and the Soviet Union stands with it.§! Needs the NVA on alert level 2 and troops massed at the border.")],
  scope="SOV")

# ---------------------------------------------------------------- troops at the border
AUFM = {1: "a concentration of troops", 2: "a deployment in force", 3: "a massive deployment"}
E(f"{EVR}.240", "Troops on the Other Side of the Border",
  "", "GFX_GER_Panzer_strasse",
  [O("Watch them closely.", "set_variable = { cwgg_tab = 1 }", ai=10),
   O("Open the situation map.", OPEN3, ai=0)],
  descs=[(f"check_variable = {{ cwgg_aufm_ddr = {l} }}",
          f"BND and the border police report {t} of the National People's Army along the inner-German border. Escalation pressure and Cold War world tension rise every month the troops stay."
          + (" The ladder will not fall below §RCrisis§! while they are there." if l > 1 else ""))
         for l, t in AUFM.items()])
E(f"{EVR}.241", "The Bundeswehr at the Border",
  "", "GFX_GER_Panzer_strasse",
  [O("The Republic will not be intimidated.", "", ai=10)],
  descs=[(f"GER = {{ check_variable = {{ cwgg_aufm_brd = {l} }} }}",
          f"Our border troops report {t} of the Bundeswehr and NATO along the state border. Escalation pressure and Cold War world tension rise every month the troops stay."
          + (" The ladder will not fall below §RCrisis§! while they are there." if l > 1 else ""))
         for l, t in AUFM.items()],
  scope="DDR")
