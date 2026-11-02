# IMPERIA COLD WAR — Native diplomatic recognition and UN membership.
# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
# IMPERIA COLD WAR — Remove retired Western integration and Moscow backing mechanics.
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
        "Another government has recognised the GDR. Bonn's continuing sole-representation claim makes this a dispute over Germany's international position. The Foreign Office must weigh diplomatic pressure against the risk of losing a partner."),
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
# IMPERIA COLD WAR — Crisis event descriptions and mediation hints follow the two-month round clock.
for c in CRISES:
    cid, key, name = c[0], c[1], c[2]
    title, desc = OUTBREAK[cid]
    E(f"{EVR}.{100 + cid}", title,
      desc + f"\n\nA §Y{name}§! has begun. Its intensity starts at §Y{c[3]}§!. Every two months a round is resolved: both sides choose a course, and the crisis ends when its intensity falls to zero, reaches the brink at 100, or freezes after §Y{c[5]}§! rounds.",
      c[7],
      [O("Convene the crisis staff.", OPEN, ai=1), O("Let the ministries handle it for now.", "", ai=10)])

# ---------------------------------------------------------------- round report
E(f"{EVR}.3", "Crisis Report: Round [?cwgg_krise_runde|0]",
  "",
  "GFX_politics_talks",
  [O("Open the situation map.", OPEN), O("Noted.")],
  descs=[("", "[RV_RoundReport]\n\nCrisis intensity: §Y[?cwgg_krise_int|0]§! after §Y[?cwgg_krise_runde|0]§! of §Y[?cwgg_krise_max|0]§! rounds.\n\nBoth governments must submit an order in the §YInner-German Relations§! window. The round remains open until every human player has chosen.")])

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

# IMPERIA COLD WAR — Crisis war orders are explicit player choices with safe timeout defaults.
# ---------------------------------------------------------------- the brink
E(f"{EVR}.11", "At the Brink",
  "The crisis has reached its peak. In East Berlin the Politburo is in permanent session, in Bonn the cabinet meets in the bunker plan of the Ahr valley. One side has to give way - or the next step is no longer politics.",
  "GFX_missiles_on_road",
  [O("Keep the decision under review.", ai=0),
   O("Give way. Nothing is worth a war.",
     J("set_temp_variable = { cwgg_t_out = 4 }", f"{R}_end_crisis = yes", v("cwger_scandal", 8), party("cdu", 0.004)), ai=60),
   O("Show resolve. Let them blink.",
     J("set_variable = { cwgg_countdown = 3 }", "set_variable = { cwgg_krise_int = 100 }", "if = { limit = { check_variable = { cwgg_mob_brd < 3 } } add_to_variable = { cwgg_mob_brd = 1 } }",
       log("brink", "Bonn shows resolve. A three-month countdown has begun."), f"{R}_update_stage = yes",
       f"if = {{ limit = {{ DDR = {{ is_ai = no }} }} DDR = {{ country_event = {{ id = {EVR}.210 days = 1 }} }} }}", f"{R}_gui_refresh = yes",
       tt(f"{P}_tt_countdown", "§RA countdown of three months begins.§! Either government may give way. When it expires, a human government must explicitly choose whether to escalate; an unanswered window does not order war.")),
     ai="base = 25 modifier = { factor = 2 check_variable = { ruling_party = 1 } }"),
   O("Ask the superpowers to mediate.",
     J("set_variable = { cwgg_krise_int = 50 }", "set_variable = { cwgg_krise_monat = 0 }", tension(-2), f"{R}_ask_east_berlin = yes",
       log("mediation", "Washington and Moscow mediate. The crisis is defused, for now."), f"{R}_update_stage = yes", f"{R}_gui_refresh = yes",
       tt(f"{P}_tt_mediation", "Crisis intensity falls to §Y50§!; the next round is resolved in two months.")),
     trig="OR = { check_variable = { cwgg_kanal_draht = 1 } has_idea = NATO_member }", ai=40)])

E(f"{EVR}.14", "East Berlin Gives Way",
  "In the middle of the night the GDR news agency announced that 'the measures have served their purpose'. The border troops are back in their barracks, the access routes are open. Our nerve has held.",
  "GFX_handshake_black",
  [O("Do not gloat.", f"if = {{ limit = {{ check_variable = {{ cwgg_krise_typ > 0 }} }} set_temp_variable = {{ cwgg_t_out = 5 }} {R}_end_crisis = yes }}")])

E(f"{EVR}.15", "Countdown: [?cwgg_countdown|0] Months",
  "East Berlin has not given way. The Soviet divisions in the GDR are on alert, NATO's commanders want instructions. Every day we hold our course, the risk grows - and so does the price of giving way.\n\nBundeswehr alert level: §Y[?cwgg_mob_brd|0]§! | NVA alert level: §Y[?cwgg_mob_ddr|0]§!",
  "GFX_GER_Panzer_strasse",
  [O("Hold our course.", "", ai=50, tt="The countdown continues. Next month: another decision."),
   O("Give way after all.", J("set_variable = { cwgg_countdown = 0 }", "set_temp_variable = { cwgg_t_out = 4 }", f"{R}_end_crisis = yes",
                              v("cwger_scandal", 12)), ai=50, trig="check_variable = { cwgg_krise_typ > 0 }"),
   O("Strike first.", J("set_country_flag = cwgg_strike_ordered", f"country_event = {{ id = {EVR}.19 days = 1 }}"),
     trig="has_country_flag = cwgg_liberation_doctrine check_variable = { cwgg_mob_brd > 2 } check_variable = { cwgg_klima < -79 } check_variable = { cwgg_aufm_brd > 1 }", ai=0)])

E(f"{EVR}.19", "The Order",
  "The Inspector General is waiting for a signature. Once it is given, the Bundeswehr crosses the inner-German border at dawn. Other governments decide whether to join through their existing alliance arrangements.",
  "GFX_news_german_army",
  [O("Tear up the order.", "if = { limit = { has_country_flag = cwgg_strike_ordered } clr_country_flag = cwgg_strike_ordered }", ai=100, tt="The countdown continues."),
   O("Sign.", f"if = {{ limit = {{ has_country_flag = cwgg_strike_ordered check_variable = {{ cwgg_krise_typ > 0 }} check_variable = {{ cwgg_countdown > 0 }} }} set_variable = {{ cwgg_countdown = 0 }} {R}_final_resolution = yes }}",
     ai=0, trig="has_country_flag = cwgg_strike_ordered check_variable = { cwgg_krise_typ > 0 } check_variable = { cwgg_countdown > 0 }",
     tt=tt(f"{P}_tt_strike", "§RWar with the GDR begins.§!"))],
  trig="has_country_flag = cwgg_strike_ordered")

E(f"{EVR}.18", "Brotherly Help?",
  "The rising in the East is being crushed. The insurgents are asking the Federal Republic for help - the same help that Hungary in 1956 hoped for in vain. The Bundeswehr could be at the Elbe in two days. The question is who else would be.",
  "GFX_german_riot",
  [O("Defer the decision.", f"country_event = {{ id = {EVR}.18 days = 30 }}", ai=0,
     trig=f"{R}_can_special_10 = yes check_variable = {{ cwgg_krise_typ = 10 }}"),
   O("Open the border to everyone who flees instead.", J("add_to_variable = { cwgg_krise_int = -20 }", dv("cwddr_exit_pressure", 8), stab(-0.02)), ai=100),
   O("Send the Bundeswehr.", f"if = {{ limit = {{ {R}_can_special_10 = yes check_variable = {{ cwgg_krise_typ = 10 }} check_variable = {{ cwgg_aufm_brd > 0 }} }} set_temp_variable = {{ cwgg_t_path = 3 }} {R}_war_start = yes }}",
     ai=0, trig=f"{R}_can_special_10 = yes check_variable = {{ cwgg_krise_typ = 10 }} check_variable = {{ cwgg_aufm_brd > 0 }}",
     tt=tt(f"{P}_tt_brotherly", "§RWar with the GDR begins.§! Other governments decide whether to join through their existing alliance arrangements.")),
   ])

E(f"{EVR}.20", "East Berlin Names a Price",
  "Through the channel the other side has made an offer: the crisis ends quietly - for money. A credit, a transit payment, a few hundred million for 'humanitarian matters'.",
  "GFX_politics_negotiations",
  [O("Defer our response.", ai=0),
   O("Pay. Quiet is worth it.", J(money_gdp(-0.0006), dv("cwddr_hard_currency", -5), "add_to_variable = { cwgg_krise_int = -30 }",
                                  "clamp_variable = { var = cwgg_krise_int min = 0 max = 100 }", f"{R}_gui_refresh = yes"), ai=60),
   O("We do not pay for good behaviour.", J("add_to_variable = { cwgg_krise_int = 5 }", "clamp_variable = { var = cwgg_krise_int min = 0 max = 100 }"), ai=40)])

E(f"{EVR}.21", "Launch Warning",
  "03:12. The early-warning radars of the Warsaw Pact report missiles in the air. The National People's Army has gone to combat readiness; in the GDR's air defence bunkers the officers are waiting for orders. Our own screens show nothing. In twenty minutes the question will answer itself.",
  "GFX_missiles_on_road",
  [O("Verify the warning before issuing new orders.", ai=0),
   O("Call Moscow on the hotline.", J("add_to_variable = { cwgg_krise_int = -40 }", f"{R}_set_stage_modifiers = yes",
                                      log("hotline", "A false alarm is cleared up on the hotline."), f"{R}_gui_refresh = yes"),
     trig="check_variable = { cwgg_kanal_draht = 1 }", ai=100),
   O("Stand down our own forces and hope they see it.", J("set_variable = { cwgg_mob_brd = 1 }", f"{R}_set_stage_modifiers = yes", "add_to_variable = { cwgg_krise_int = -20 }", "clamp_variable = { var = cwgg_krise_int min = 0 max = 100 }", log("alarm_ok", "The alarm is treated as a warning; the Bundeswehr stands down."), f"{R}_gui_refresh = yes", tt(f"{P}_tt_alarm", "The Bundeswehr stands down and crisis intensity falls by §G20§!. A false alarm never orders either country to war.")), ai=50)])

# ---------------------------------------------------------------- war
E(f"{EVR}.30", "The State of Defence",
  "The Bundestag and Bundesrat have declared the state of defence under Article 115a of the Basic Law. Command of the armed forces passes to the Chancellor. The Joint Committee stands ready to replace a parliament that may no longer be able to meet.",
  "GFX_news_german_army",
  [O("Defend the free part of Germany.", J(ws(0.15), stab(-0.05), v("cwger_peace_movement", 15), protest(10)))],
  descs=[("check_variable = { cwgg_war_path = 1 }", "We have attacked. The Bundestag and Bundesrat have declared the state of defence under Article 115a of the Basic Law - a constitution written for a defensive war now carries an offensive one. Command of the armed forces passes to the Chancellor."),
         ("check_variable = { cwgg_war_path = 2 }", "The National People's Army has crossed the border. West Berlin is under fire. The Bundestag and Bundesrat have declared the state of defence under Article 115a of the Basic Law; command of the armed forces passes to the Chancellor."),
         ("check_variable = { cwgg_war_path = 3 }", "The Bundeswehr is crossing the Elbe to help the rising in the East. The Bundestag has declared the state of defence; command passes to the Chancellor. Whether the Soviet Union will stand aside is the only question that matters now."),
         ("check_variable = { cwgg_war_path = 4 }", "A false alarm became a real war. Nobody in Bonn or East Berlin wanted it; both armies are now fighting it. The Bundestag has declared the state of defence under Article 115a.")])

# IMPERIA COLD WAR — Armistices require the other German government's consent.
E(f"{EVR}.31", "The Threshold",
  "The fighting continues. The federal cabinet may propose an armistice on the current lines. East Berlin decides whether to accept.",
  "GFX_missiles_on_road",
  [O("Keep the question under review.", ai=0),
   O("Propose an armistice.", f"if = {{ limit = {{ has_war_with = DDR country_exists = DDR NOT = {{ DDR = {{ has_country_flag = cwgg_armistice_request }} }} }} DDR = {{ set_country_flag = cwgg_armistice_request country_event = {{ id = {EVR}.260 days = 1 }} }} }}", ai=60,
     trig="has_war_with = DDR country_exists = DDR NOT = { DDR = { has_country_flag = cwgg_armistice_request } }"),
   O("Continue operations.", ai=40)],
  trig="has_global_flag = cwgg_german_war has_war_with = DDR")
E(f"{EVR}.260", "Bonn Proposes an Armistice",
  "The Federal Republic proposes an end to the fighting on the present lines. The decision rests with our government.",
  "GFX_treaty",
  [O("Keep the proposal under review.", f"if = {{ limit = {{ has_country_flag = cwgg_armistice_request has_war_with = GER }} country_event = {{ id = {EVR}.260 days = 30 }} }} else = {{ clr_country_flag = cwgg_armistice_request }}", ai=0),
   O("Accept the armistice.", "if = { limit = { has_country_flag = cwgg_armistice_request has_war_with = GER } clr_country_flag = cwgg_armistice_request white_peace = GER }", ai="base = 20 modifier = { add = 60 surrender_progress > 0.25 }",
     trig="has_country_flag = cwgg_armistice_request has_war_with = GER"),
   O("Reject the proposal.", "if = { limit = { has_country_flag = cwgg_armistice_request } clr_country_flag = cwgg_armistice_request }", ai=40)],
  scope="DDR", trig="has_country_flag = cwgg_armistice_request has_war_with = GER")

DDR_CORE_STATES = (44, 45, 539, 545, 972, 1079)
WAR_VICTORY_DDR = "has_global_flag = cwgg_german_war has_country_flag = cwgg_war_victory_ddr OR = { AND = { country_exists = DDR has_war_with = DDR DDR = { has_capitulated = yes } } AND = { NOT = { country_exists = DDR } " + " ".join(f"{state} = {{ is_owned_by = GER }}" for state in DDR_CORE_STATES) + " } }"

# IMPERIA COLD WAR — Military defeat opens negotiations; it grants no automatic annexation.
E(f"{EVR}.40", "The Eastern Front Falls Silent",
  "The East German armed forces have capitulated. The military result leaves the governments and their allies to negotiate the terms of peace.",
  "GFX_political_deal",
  [O("Open settlement consultations.", f"{P}_settlement_open = yes DDR = {{ {P}_settlement_open = yes }}", ai=90, trig=WAR_VICTORY_DDR),
   O("Continue consultations.", "", ai=10)],
  scope="GER", trig=WAR_VICTORY_DDR)

E(f"{EVR}.41", "The Western Front Falls Silent",
  "The Federal Republic's armed forces have capitulated. East Berlin can propose terms, while Bonn and every belligerent retain their own decision on the settlement.",
  "GFX_political_deal",
  [O("Open settlement consultations.", f"{P}_settlement_open = yes DDR = {{ {P}_settlement_open = yes }}", ai=90,
     trig="has_global_flag = cwgg_german_war has_war_with = DDR has_capitulated = yes"),
   O("Continue consultations.", "", ai=10)],
  scope="GER", trig="has_global_flag = cwgg_german_war has_war_with = DDR has_capitulated = yes")

E(f"{EVR}.42", "An Armistice",
  "The guns along the inner-German border have fallen silent. Nothing has been won; the dead are counted on both sides. The two German states remain - and hate each other more than at any time since 1961.",
  "GFX_treaty",
  [O("Never again.", f"if = {{ limit = {{ has_global_flag = cwgg_german_war country_exists = DDR NOT = {{ has_war_with = DDR }} }} {R}_cold_peace = yes {stab(-0.03)} }}", ai=0,
     trig="has_global_flag = cwgg_german_war country_exists = DDR NOT = { has_war_with = DDR }")],
  scope="GER", trig="has_global_flag = cwgg_german_war country_exists = DDR NOT = { has_war_with = DDR }")

# IMPERIA COLD WAR — Recipient-controlled bilateral treaty ratification.
# ---------------------------------------------------------------- treaties
def _ratify_guard(t):
    return f"{R}_can_ratify_{t[0]} = yes check_variable = {{ cwgg_tr_ready = {t[0]} }} check_variable = {{ cwgg_tr_invalid = 0 }} check_variable = {{ cwgg_tr_sender > 0 }}"


def _human_ratify_offer(t):
    n = t[0]
    return f"""if = {{ limit = {{ {_ratify_guard(t)} check_variable = {{ cwgg_tr_sender = 1 }} DDR = {{ is_ai = no }} check_variable = {{ cwgg_tr_pending = 0 }} }}
	set_variable = {{ cwgg_tr_pending = {n} }}
	DDR = {{ set_country_flag = cwgg_tr_ddr_dialogue_open country_event = {{ id = {EVR}.{250 + n} days = 1 }} }}
}}
else_if = {{ limit = {{ {_ratify_guard(t)} check_variable = {{ cwgg_tr_pending = 0 }} }}
	set_variable = {{ cwgg_tr_pending = {n} }}
	{R}_ratify_{n} = yes
}}"""


E(f"{EVR}.50", "A Treaty Is Ready",
  "", "GFX_treaty",
  [O("Review this offer later.", "clr_country_flag = cwgg_tr_brd_dialogue_open", ai=0),
   O("Sign it.", f"clr_country_flag = cwgg_tr_brd_dialogue_open\n" + "\n".join(
        [f"{'if' if i == 0 else 'else_if'} = {{ limit = {{ check_variable = {{ cwgg_tr_ready = {t[0]} }} check_variable = {{ cwgg_tr_invalid = 0 }} }} {_human_ratify_offer(t)} }}" for i, t in enumerate(TREATIES)] +
        [f"else_if = {{ limit = {{ {_ratify_guard(t)} check_variable = {{ cwger_margin < 1 }} }} country_event = {{ id = {EVR}.51 days = 7 }} }}" for t in TREATIES if t[8]] +
        ["else = { set_variable = { cwgg_tr_invalid = 1 } }"]),
        ai=95,
        trig="check_variable = { cwgg_tr_ready > 0 } check_variable = { cwgg_tr_pending = 0 } check_variable = { cwgg_tr_invalid = 0 }"),
   O("This proposal has lapsed.", f"{R}_decline_treaty = yes",
     trig="check_variable = { cwgg_tr_invalid = 1 } check_variable = { cwgg_tr_pending = 0 }"),
   # IMPERIA COLD WAR — Bonn may reject a ready proposal without signing it.
   O("Decline the proposal.", f"{R}_decline_treaty = yes", ai=5,
     trig="check_variable = { cwgg_tr_ready > 0 } check_variable = { cwgg_tr_pending = 0 }")],
  descs=[(f"check_variable = {{ cwgg_tr_ready = {t[0]} }}", f"§Y{t[2]}§!\n\n{t[3]}\n\nThe negotiators have finished their work. Bonn must sign, then a human East Berlin must accept or refuse.") for t in TREATIES])


# IMPERIA COLD WAR — Each human recipient receives a treaty-specific, guarded consent event.
for _t in TREATIES:
    _n = _t[0]
    E(f"{EVR}.{250 + _n}", f"Bonn Signs: {_t[2]}",
      f"The Federal Government has signed the proposed {_t[2]}. The agreement takes effect only if East Berlin accepts while its terms remain eligible. The treaty's existing negotiation costs have already been paid by its initiator.",
      "GFX_treaty",
      [O("Review this offer later.", "clr_country_flag = cwgg_tr_ddr_dialogue_open", ai=0,
         trig=f"GER = {{ check_variable = {{ cwgg_tr_pending = {_n} }} }}"),
       O("Accept the treaty.", f"""clr_country_flag = cwgg_tr_ddr_dialogue_open
if = {{ limit = {{ GER = {{ {_ratify_guard(_t)} check_variable = {{ cwgg_tr_pending = {_n} }} }} }}
	GER = {{ {R}_ratify_{_n} = yes }}
}}
else = {{ GER = {{ set_variable = {{ cwgg_tr_invalid = 1 }} }} }}""",
         trig=f"GER = {{ {_ratify_guard(_t)} check_variable = {{ cwgg_tr_pending = {_n} }} }}", ai=0),
       O("Refuse the treaty.", f"clr_country_flag = cwgg_tr_ddr_dialogue_open GER = {{ if = {{ limit = {{ check_variable = {{ cwgg_tr_pending = {_n} }} }} set_variable = {{ cwgg_verh = 0 }} set_variable = {{ cwgg_verh_prog = 0 }} set_variable = {{ cwgg_tr_ready = 0 }} set_variable = {{ cwgg_tr_pending = 0 }} set_variable = {{ cwgg_tr_invalid = 0 }} set_variable = {{ cwgg_tr_sender = 0 }} {R}_gui_refresh = yes }} }}", ai=0,
         trig=f"GER = {{ check_variable = {{ cwgg_tr_pending = {_n} }} }}"),
       O("The proposal has lapsed.", f"clr_country_flag = cwgg_tr_ddr_dialogue_open GER = {{ if = {{ limit = {{ check_variable = {{ cwgg_tr_pending = {_n} }} check_variable = {{ cwgg_tr_invalid = 1 }} }} set_variable = {{ cwgg_verh = 0 }} set_variable = {{ cwgg_verh_prog = 0 }} set_variable = {{ cwgg_tr_ready = 0 }} set_variable = {{ cwgg_tr_pending = 0 }} set_variable = {{ cwgg_tr_invalid = 0 }} set_variable = {{ cwgg_tr_sender = 0 }} {R}_gui_refresh = yes }} }}", ai=0,
         trig=f"GER = {{ check_variable = {{ cwgg_tr_pending = {_n} }} check_variable = {{ cwgg_tr_invalid = 1 }} }}")],
      scope="DDR", trig=f"GER = {{ check_variable = {{ cwgg_tr_pending = {_n} }} }}")

E(f"{EVR}.51", "Ratification Fails",
  "The government no longer has a majority for the treaty. The opposition calls it a sell-out of German unity, and enough deputies of the coalition agree. The treaty stays unsigned.",
  "GFX_german_parliament_bundestag",
  [O("We will try again with a new majority.", J("set_variable = { cwgg_verh = 0 }", "set_variable = { cwgg_verh_prog = 0 }", "set_variable = { cwgg_tr_ready = 0 }", "set_variable = { cwgg_tr_pending = 0 }", "set_variable = { cwgg_tr_invalid = 0 }", "set_variable = { cwgg_tr_sender = 0 }", kl(-5),
                                                 log("ratify_fail", "The Bundestag refuses to ratify a treaty with the GDR.")))])

E(f"{EVR}.60", "East Berlin Needs Money",
  "Through the Schalck-Golodkowski channel East Berlin lets it be known that the GDR's hard-currency position is 'tight'. A credit would be received with gratitude - and with gestures in return.",
  "GFX_stock_market",
  [O("Leave the request under review.", ai=0),
   O("Grant it - for humanitarian concessions.", J(money_gdp(-0.0006), lever("devisen", 1), kl(6), dv("cwddr_hard_currency", -8), dv("cwddr_west_dependency", 5),
                                                     log("credit_granted", "Bonn grants a credit. East Berlin eases travel rules.")), ai=60),
   O("Let them stew.", J(kl(-4), dv("cwddr_hard_currency", 3)), ai=40)])

E(f"{EVR}.70", "RAF Fugitives in the GDR",
  "The arrests of the HVA network have brought out something nobody expected: since 1980 the Stasi has given new identities to members of the Red Army Faction who wanted to leave the underground - and has trained others. East Berlin denies everything.",
  "GFX_RAF_Schulz",
  [O("Make it public.", J(kl(-15), "add_to_variable = { cwger_raf_prisoners = 2 }", "add_to_variable = { cwger_raf_cadre = -3 }",
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
              "Bundeswehr alert §Y[?GER.cwgg_mob_brd|0]§! | NVA alert §Y[?GER.cwgg_mob_ddr|0]§!")
ESC = "GER = { check_variable = { cwgg_init_ddr > 0 } }"
ANSWER_TEXT = {
    1: ("Back down. The matter is not worth it.", "We give way this round. Intensity falls - and Bonn will say it won."),
    2: ("Stall. Time is on our side.", "Neither yield nor push. This instruction must be submitted explicitly."),
    3: ("Escalate. Bonn must learn what pressure means.", "Costs §Y1§! initiative. Raises intensity, more so against a soft Bonn; blunted by a Bundeswehr on alert."),
    4: ("Call on Moscow.", "Costs §Y1§! initiative. If Bonn calls the Allies at the same time, the superpowers take over."),
    5: ("Name a price.", "Costs §Y1§! initiative. If Bonn is talking, it may pay for quiet."),
}
# IMPERIA COLD WAR — Crisis answers are explicit player orders kept private until resolution.
E(f"{EVR}.200", "Our Course in the Crisis",
  "The Politburo meets in the Central Committee building on Werderscher Markt. Submit an explicit order for this round; it will remain confidential until the round resolves. The clock waits until every human player has chosen.\n\n" + DDR_STATUS,
  "GFX_politics_talks",
  [O("Defer our order.", f"country_event = {{ id = {EVR}.200 days = 30 }}", ai=0,
     trig="GER = { check_variable = { cwgg_krise_typ > 0 } check_variable = { cwgg_countdown = 0 } check_variable = { cwgg_ddr_order_ready = 0 } }"),
   *[O(ANSWER_TEXT[a[0]][0], f"{P}_east_act_answer_{a[0]} = yes", ai=10,
     trig=f"{P}_east_can_answer_{a[0]} = yes", tt=ANSWER_TEXT[a[0]][1]) for a in ANSWERS],
  ],
  scope="DDR", trig="is_ai = no GER = { check_variable = { cwgg_krise_typ > 0 } check_variable = { cwgg_countdown = 0 } check_variable = { cwgg_ddr_order_ready = 0 } }")

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
  [O("Defer our decision.", f"country_event = {{ id = {EVR}.211 days = 30 }}", ai=0,
     trig="has_country_flag = cwgg_ddr_countdown_dialogue_open"),
   O("Accept Moscow's restraint.", f"if = {{ limit = {{ has_country_flag = cwgg_ddr_countdown_dialogue_open GER = {{ check_variable = {{ cwgg_krise_typ > 0 }} check_variable = {{ cwgg_countdown = 0 }} }} }} clr_country_flag = cwgg_ddr_countdown_dialogue_open GER = {{ set_temp_variable = {{ cwgg_t_out = 6 }} {R}_end_crisis = yes }} }}", ai=90,
     trig="has_country_flag = cwgg_ddr_countdown_dialogue_open GER = { check_variable = { cwgg_krise_typ > 0 } check_variable = { cwgg_countdown = 0 } }",
     tt="The crisis ends. Bonn has won - but the decision was taken in the Kremlin."),
   O("Order the attack on West Berlin.", f"if = {{ limit = {{ has_country_flag = cwgg_ddr_countdown_dialogue_open GER = {{ check_variable = {{ cwgg_krise_typ > 0 }} check_variable = {{ cwgg_countdown = 0 }} check_variable = {{ cwgg_mob_ddr > 1 }} check_variable = {{ cwgg_aufm_ddr > 0 }} }} is_in_faction_with = SOV }} clr_country_flag = cwgg_ddr_countdown_dialogue_open GER = {{ set_temp_variable = {{ cwgg_t_path = 2 }} {R}_war_start = yes }} }}", ai=0,
     trig="has_country_flag = cwgg_ddr_countdown_dialogue_open is_in_faction_with = SOV GER = { check_variable = { cwgg_krise_typ > 0 } check_variable = { cwgg_countdown = 0 } check_variable = { cwgg_mob_ddr > 1 } check_variable = { cwgg_aufm_ddr > 0 } }",
     tt="§RWar with the Federal Republic begins.§! Needs the GDR to remain in the Soviet-led alliance, the NVA on alert level 2 and troops massed at the border."),
   O("The order has lapsed. Return to the situation map.", "if = { limit = { has_country_flag = cwgg_ddr_countdown_dialogue_open } clr_country_flag = cwgg_ddr_countdown_dialogue_open }", ai=0,
     trig="has_country_flag = cwgg_ddr_countdown_dialogue_open GER = { check_variable = { cwgg_krise_typ = 0 } }")],
  scope="DDR", trig="is_ai = no has_country_flag = cwgg_ddr_countdown_dialogue_open")

# IMPERIA COLD WAR — War news follows an actual player-authorised war path.
E(f"{EVR}.230", "War with the Federal Republic",
  "", "GFX_news_german_army", [O("For the socialist fatherland.", J("add_war_support = 0.10", "add_stability = -0.05"))],
  descs=[("GER = { OR = { check_variable = { cwgg_war_path = 1 } check_variable = { cwgg_war_path = 3 } } }", "The Bundeswehr has crossed the state border. The National People's Army is fighting on the Werra and the Elbe. Whether Moscow stands with us is decided in Moscow."),
         ("GER = { check_variable = { cwgg_war_path = 2 } }", "Our divisions are moving on West Berlin. There is no way back now."),
         ],
  scope="DDR")

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
