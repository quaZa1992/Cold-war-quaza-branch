"""Inner-German rivalry: a two-player mini-game between Bonn and East Berlin.

State lives in variables on GER (prefix cwgg_). East Berlin is played by a human or by a
scripted AI with the personality of the SED leader. The window in gui.py reads and drives everything here.

  climate      cwgg_klima    -100 (confrontation) .. +100 (interdependence)
  pressure     cwgg_druck    0..100, short-term escalation pressure, decays 10 % a month
  stage        cwgg_stufe    0 modus vivendi .. 5 war danger, 6 war
  initiative   cwgg_init_brd / cwgg_init_ddr   0..6 action points
  alert        cwgg_mob_brd / cwgg_mob_ddr     0..3 (Bundeswehr / NVA; mobilisation speed and war support per level)
  crisis       cwgg_krise_typ (0 = none), _int, _runde, _max, _monat (months into the current round, one round = 6 months),
               cwgg_haltung (Bonn's stance), cwgg_ddr_wahl (East Berlin's answer when the GDR is played by a human)

Built for multiplayer roleplay: no hidden 'standing' or 'backing' scores, both sides can be human, rounds
are resolved by the monthly tick every six months (no recurring hidden events).
  treaties     cwgg_vertrag_n (0 locked/none, 1 done, 2 suspended), cwgg_verh (treaty in negotiation), cwgg_verh_prog
  channels     cwgg_kanal_<k> 0 closed, 1 open, 2 strained; unlock flags cwgg_kanal_<k>_unlocked
  levers       cwgg_hebel_<k> 0..3 (Bonn); cwgg_dhebel_<k> 0..3 (East Berlin)
"""
from cw_lib import *
from events_lib import E, O, fire, EXTRA_EFFECTS

EVR = "COLDWAR_GGR"
R = P + "_rv"          # effect prefix

# ------------------------------------------------------------------ static tables
STANCES = [  # id, key, name, init cost, pp cost, description
    (1, "wait", "Wait and See", 0, 0, "Let the ministries handle it. Costs nothing and signals little - East Berlin sets the pace."),
    (2, "deescalate", "De-escalate", 1, 0, "Lower the temperature: conciliatory statements, a postponed visit, a quiet word in the ear of the Permanent Representation."),
    (3, "firm", "Stand Firm", 1, 10, "Make clear that Bonn will not give way - without adding new pressure of its own."),
    (4, "pressure", "Counter-Pressure", 2, 0, "Use the lever that hurts East Berlin most in this crisis. Strong if the lever is strong, a bluff if it is not."),
    (5, "allies", "Call in the Allies", 1, 0, "Ask Washington, London and Paris to speak for Berlin and Germany as a whole. Needs NATO membership - and if Moscow is called too, the crisis is no longer ours."),
    (6, "secret", "Secret Channel", 2, 0, "Settle it quietly through an open channel. Effective, but the Stasi listens on every line it can reach."),
    (7, "mobilise", "Prepare Mobilisation", 3, 0, "Raise readiness and say so. Deters escalation - and escalates."),
]
ANSWERS = [  # id, key, name
    (1, "yield", "Backs Down"),
    (2, "stall", "Stalls"),
    (3, "escalate", "Escalates"),
    (4, "moscow", "Calls on Moscow"),
    (5, "counter", "Makes a Counter-Offer"),
]
# change of crisis intensity for Bonn's stance x East Berlin's answer (one round = six months)
MATRIX = {
    1: {1: -8, 2: 0, 3: 15, 4: 15, 5: 0},
    2: {1: -30, 2: -15, 3: 8, 4: 0, 5: -22},
    3: {1: -15, 2: 8, 3: 22, 4: 22, 5: 8},
    4: {1: -15, 2: 8, 3: 38, 4: 38, 5: 15},
    5: {1: -22, 2: -8, 3: 8, 4: 15, 5: -8},
    6: {1: -38, 2: -22, 3: -8, 4: -15, 5: -30},
    7: {1: -22, 2: 15, 3: 45, 4: 45, 5: 22},
}
LEVERS = [  # key, name, description
    ("devisen", "Hard Currency", "The Swing, state-guaranteed credits and transit payments. East Berlin needs Deutschmarks more every year."),
    ("menschen", "People", "Häftlingsfreikauf and family reunification - quiet deals through lawyers and churches."),
    ("medien", "Media", "ARD and ZDF reach most of the GDR; RIAS and Deutsche Welle the rest."),
    ("recht", "Legal Position", "The sole-mandate claim, one German citizenship, the Salzgitter registry of the regime's crimes."),
    ("allianz", "Alliance", "The rights of the Three Powers in Berlin and the NATO guarantee."),
    ("handel", "Trade", "Inner-German trade and the GDR's back door into the Common Market."),
]
DLEVERS = [
    ("transit", "Transit Routes", "Harassment on the autobahns, closures of the access routes to West Berlin."),
    ("zwang", "Compulsory Exchange", "The minimum sum every Western visitor must change. Raise it and visits fall; lower it and Deutschmarks flow."),
    ("stasi", "Stasi and HVA", "Spies in Bonn's ministries, Romeos in its secretariats, ears on its channels."),
    ("grenze", "Border Regime", "Order to shoot, SM-70 spring guns, mines and dogs."),
]
CHANNELS = [  # key, name, description
    ("bahr", "Bahr - Kohl", "State secretaries Egon Bahr and Michael Kohl: the channel through which the treaties of the early 1970s were written."),
    ("sv", "Permanent Representation", "Not an embassy - the Federal Republic does not recognise the GDR as foreign - but a mission in East Berlin all the same."),
    ("vogel", "Vogel - Stange", "Lawyers Wolfgang Vogel and Jürgen Stange: the quiet market in prisoners and family reunions."),
    ("koko", "Schalck-Golodkowski", "Commercial Coordination: the GDR's hard-currency empire, a door to East Berlin's most pressing needs."),
    ("kirche", "Church Channel", "The Protestant churches of both states, still bound together in conferences and partnerships."),
    ("draht", "Hotline to Moscow", "A direct line between the chancellery and the Kremlin, opened by the Moscow Treaty."),
]
CRISES = [  # id, key, name, start intensity, best stance, max rounds, lever used by counter-pressure, picture, special action
    (1, "transit", "Transit Crisis", 40, 5, 4, "handel", "GFX_german_visa", "Prepare an Airlift"),
    (2, "border", "Border Incident", 35, 3, 3, "medien", "GFX_Polizeiabsperrung", "Take It to the UN"),
    (3, "spy", "Spy Affair", 45, 6, 3, "recht", "GFX_GER_MAD", "Exchange on the Glienicke Bridge"),
    (4, "embassy", "Embassy Refugees", 50, 6, 3, "devisen", "GFX_german_emmigration", "Negotiate Special Trains"),
    (5, "recognition", "Recognition Crisis", 30, 3, 3, "recht", "GFX_treaty", "Break Off Relations"),
    (6, "missiles", "Missile Crisis", 45, 5, 4, "allianz", "GFX_missiles_on_road", "Propose the Zero Option"),
    (7, "manoeuvre", "Manoeuvre Crisis", 55, 2, 2, "allianz", "GFX_GER_Panzer_strasse", "Cancel the Exercise"),
    (8, "dissident", "Dissident Crisis", 30, 4, 3, "medien", "GFX_politics_protest", "Offer Asylum"),
    (9, "elbe", "Elbe Border Dispute", 25, 3, 4, "recht", "GFX_politics_talks", "Joint Border Commission"),
    (10, "uprising", "Uprising in the GDR", 70, 6, 3, "medien", "GFX_german_riot", "Brotherly Help"),
]
CRISIS_BY_ID = {c[0]: c for c in CRISES}
STAGES = [
    ("Modus Vivendi", "Two states have settled into a working relationship: visits, credits, treaties and a border that is quieter than it has ever been."),
    ("Cool Coexistence", "Correct, cautious and transactional. Neither side expects much, neither side wants trouble."),
    ("Tensions", "Harsh words in Neues Deutschland and the Bundestag, incidents at the border, channels running cold."),
    ("Crisis", "A confrontation is under way. Every move is watched in Washington and Moscow."),
    ("Confrontation", "Both states treat each other as enemies. Trade has halved, the armies are watching the border."),
    ("War Danger", "Troops on alert on both sides of the Iron Curtain. One mistake could start a war in the middle of Europe."),
    ("War", "German soldiers are fighting Germans."),
]
STAGE_DM = [  # GER: stability, war support, consumer goods, factory output; tension per month
    (0.03, -0.05, -0.01, 0.0, -0.3),
    (0.01, 0.0, 0.0, 0.0, 0.0),
    (-0.02, 0.03, 0.0, 0.0, 0.2),
    (-0.04, 0.06, 0.0, 0.0, 0.5),
    (-0.06, 0.10, 0.02, 0.0, 1.0),
    (-0.08, 0.15, 0.02, -0.05, 2.0),
    (-0.05, 0.20, 0.0, 0.0, 0.0),
]
# Troops along the inner-German border (vanilla divisions_in_state, the data the engine also uses for
# border threat): Bonn's side and East Berlin's side, state ids from MD.
BORDER_BRD = [37, 38, 41, 964, 43, 1251]           # Schleswig-Holstein, Lower Saxony, Hesse, Franconia, Bavaria, West Berlin
BORDER_DDR = [539, 972, 545, 44, 1079, 45]          # Mecklenburg, Saxony-Anhalt, Thuringia, Saxony, Brandenburg, East Berlin
# divisions_in_state only answers "more than n?", so the count per state is built from steps:
# (threshold, divisions added) - exact up to 6 per state, approximate above, capped at 30.
BORDER_STEPS = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (8, 2), (10, 2), (12, 2), (15, 3), (20, 5), (25, 5), (30, 5)]
BORDER_LEVELS = (4, 10, 20)                          # divisions in all border states together for build-up level 1, 2, 3
BORDER_EFFECT = [(0, 0, 0), (3, -1, 0), (6, -2, 0.25), (10, -4, 0.5)]   # pressure, climate, Cold War world tension a month
ALERT_LEVELS = [(0.0, 0.0), (0.10, 0.02), (0.25, 0.05), (0.50, 0.10)]   # mobilisation speed, war support per alert level
STAGE_DM_DDR = [(0.02, -0.03, -0.02), (0.01, 0.0, 0.0), (-0.01, 0.03, 0.0), (-0.03, 0.06, 0.01), (-0.05, 0.10, 0.02),
                (-0.07, 0.15, 0.03), (-0.05, 0.20, 0.0)]

TREATIES = [
    # n, key, name, description, min climate, prerequisite treaties, extra trigger, unlock text, needs Bundestag ratification
    (1, "summit", "Meeting of the Heads of Government",
     "Willy Brandt and Willi Stoph met in Erfurt in March 1970 and in Kassel in May. Nothing was agreed - but for the first time the two German governments talked to each other.",
     -10, [], f"has_country_flag = cwgg_unlock_vertrag_1", "Needs the focus §YChange through Rapprochement§!.", False),
    (2, "berlin", "Berlin Settlement",
     "The Quadripartite Agreement of September 1971 and the transit agreement that followed: unhindered traffic between the Federal Republic and West Berlin, guaranteed by the Four Powers.",
     -5, [1], "NOT = { country_exists = SOV SOV = { has_war_with = GER } }", "", False),
    (3, "basic", "Basic Treaty",
     "The Grundlagenvertrag of December 1972: two German states, equal rights, good-neighbourly relations - and Bonn's letter on German unity, so that nothing is given up for ever.",
     0, [1, 2], "has_country_flag = cwgg_unlock_vertrag_3", "Needs the focus §YThe Basic Treaty§!.", True),
    (4, "un", "Both States in the United Nations",
     "In September 1973 the United Nations admitted the Federal Republic and the GDR on the same day.",
     0, [3], "always = yes", "", False),
    (5, "missions", "Permanent Representations",
     "Missions, not embassies: Günter Gaus moved into Hannoversche Straße in East Berlin in 1974, Michael Kohl into Godesberger Allee in Bonn.",
     5, [3], "always = yes", "", False),
    (6, "traffic", "Traffic, Post and Travel Agreements",
     "Telephone lines, new autobahn crossings, visits for pensioners and urgent family matters: the small steps of the 1970s and 1980s.",
     20, [3], "always = yes", "", False),
    (7, "culture", "Cultural Agreement and Town Twinning",
     "After thirteen years of talks the cultural agreement was signed in May 1986; Saarlouis and Eisenhüttenstadt became the first twinned towns.",
     30, [5], "date > 1979.12.31", "Available from 1980.", False),
    (8, "visit", "State Visit of the SED Leader",
     "In September 1987 Erich Honecker was received in Bonn with flags and anthems - and spoke of a border that would one day 'unite rather than divide'.",
     40, [5, 6], "has_country_flag = cwgg_unlock_vertrag_8", "Needs the focus §YCoalition of Reason§!.", False),
    (9, "confederation", "Treaty Community and Confederation",
     "A treaty community between the two German states, with joint commissions, a common market and, one day, confederal institutions.",
     70, [3, 5], f"OR = {{ DDR = {{ check_variable = {{ cwddr_wende_stage > 2 }} }} DDR = {{ check_variable = {{ cwddr_leader > 2 }} }} }}",
     "Needs an open border or a reform government in East Berlin.", True),
]

LOGS = {}   # key -> (code, text)


def log(key, text=None):
    """Push a line into the window's situation report."""
    if key not in LOGS:
        LOGS[key] = (len(LOGS) + 1, text)
    elif text and LOGS[key][1] != text:
        raise ValueError("log text conflict " + key)
    return f"set_temp_variable = {{ cwgg_t_log = {LOGS[key][0]} }}\n{R}_log = yes"


def kl(n, show=True):
    """Change the inner-German climate."""
    s = f"add_to_variable = {{ cwgg_klima = {n} }}\nclamp_variable = {{ var = cwgg_klima min = -100 max = 100 }}"
    if not show:
        return s
    key = f"{P}_tt_klima_{'up' if n > 0 else 'down'}_{abs(n)}"
    L(key, f"Inner-German climate: §{'G' if n > 0 else 'R'}{'+' if n > 0 else '-'}{abs(n)}§!")
    return f"custom_effect_tooltip = {key}\nhidden_effect = {{ {s} }}"


def dr(n, show=True):
    s = f"add_to_variable = {{ cwgg_druck = {n} }}\nclamp_variable = {{ var = cwgg_druck min = 0 max = 100 }}"
    if not show:
        return s
    key = f"{P}_tt_druck_{'up' if n > 0 else 'down'}_{abs(n)}"
    L(key, f"Escalation pressure: §{'R' if n > 0 else 'G'}{'+' if n > 0 else '-'}{abs(n)}§!")
    return f"custom_effect_tooltip = {key}\nhidden_effect = {{ {s} }}"


def lever(k, n, show=True, ddr=False):
    var = f"cwgg_{'d' if ddr else ''}hebel_{k}"
    s = f"add_to_variable = {{ {var} = {n} }}\nclamp_variable = {{ var = {var} min = 0 max = 3 }}"
    if not show:
        return s
    names = dict((a, b) for a, b, _ in (DLEVERS if ddr else LEVERS))
    key = f"{P}_tt_{'d' if ddr else ''}hebel_{k}_{'up' if n > 0 else 'down'}_{abs(n)}"
    who = "East Berlin's lever" if ddr else "Lever"
    L(key, f"{who} §Y{names[k]}§!: {'+' if n > 0 else '-'}{abs(n)} level")
    return f"custom_effect_tooltip = {key}\nhidden_effect = {{ {s} }}"


def bop(n):
    return f"add_power_balance_value = {{ id = {P}_deutschlandpolitik value = {n} }}"


def channel_unlock(k, open_it=False):
    s = f"set_country_flag = cwgg_kanal_{k}_unlocked"
    if open_it:
        s += f"\nset_variable = {{ cwgg_kanal_{k} = 1 }}"
    name = dict((a, b) for a, b, _ in CHANNELS)[k]
    key = f"{P}_tt_kanal_{k}_unlock{'_open' if open_it else ''}"
    L(key, f"Channel §Y{name}§! {'opens' if open_it else 'can be opened in the inner-German relations window'}.")
    return f"custom_effect_tooltip = {key}\nhidden_effect = {{ {s} }}"


def ddr_has(cond):
    return f"country_exists = DDR DDR = {{ {cond} }}"


# ------------------------------------------------------------------ scripted triggers
ACTIONS = []   # (key, name, desc, lever row, init, pp, cooldown days, trigger, effect)


def A(key, name, desc, row, init, pp, cd, trig, eff, once=False):
    ACTIONS.append(dict(key=key, name=name, desc=desc, row=row, init=init, pp=pp, cd=cd, trig=trig, eff=eff, once=once))


A("swing", "Raise the Swing", "Offer a larger interest-free overdraft in inner-German trade, delivered as an Imperia §YConsumer Supply Credits§! programme if East Berlin accepts.",
  "devisen", 1, 25, 1095,
  f"OR = {{ has_country_flag = {P}_swing_unlocked check_variable = {{ cwgg_hebel_devisen > 0 }} }} {ddr_has('check_variable = { cwddr_wende_stage < 3 }')}",
  J(f"DDR = {{ country_event = {{ id = COLDWAR_DDR.2 days = 3 }} }}", kl(5), lever("devisen", 1), log("swing", "Bonn offers a larger Swing.")))
A("credit", "The Milliardenkredit", "A state-guaranteed bank loan of one billion marks for a GDR close to insolvency - in exchange for gestures at the border.",
  "devisen", 2, 50, 0,
  f"OR = {{ check_variable = {{ ruling_party = 1 }} check_variable = {{ cwgg_kanal_koko = 1 }} }} {ddr_has('check_variable = { cwddr_hard_currency > 40 }')}",
  J(f"DDR = {{ country_event = {{ id = COLDWAR_DDR.3 days = 3 }} }}", kl(10), lever("grenze", -1, ddr=True), lever("devisen", 1),
    v("cwger_csu_autonomy", 5), log("credit", "A billion-mark credit for East Berlin. The spring guns come down.")), once=True)
A("freikauf", "Buy Prisoners Free", "Pay for the release of political prisoners through the lawyers' channel.",
  "menschen", 1, 0, 365, "check_variable = { cwgg_kanal_vogel = 1 } country_exists = DDR",
  J(money_gdp(-0.0004), "DDR = { country_event = { id = COLDWAR_DDR.4 days = 5 } }", kl(2), lever("menschen", 1), stab(0.01),
    log("freikauf", "Another bus with released prisoners crosses at Herleshausen.")))
A("transit", "Transit Lump Sum", "Pay East Berlin a fixed annual sum for unhindered transit to West Berlin.",
  "handel", 1, 0, 1825, "check_variable = { cwgg_vertrag_2 = 1 } country_exists = DDR",
  J(money_gdp(-0.0008), v("cwger_berlin_access", 10), dv("cwddr_hard_currency", -3), lever("transit", -1, ddr=True), kl(3),
    log("transit", "A new transit lump sum is agreed.")))
A("media", "Media Offensive", "More airtime for the GDR on RIAS and Deutsche Welle, more correspondents in East Berlin, more pictures of what happens at the border.",
  "medien", 1, 25, 365, "check_variable = { cwgg_hebel_medien > 0 } country_exists = DDR",
  J(dv("cwddr_west_media", 5), dv("cwddr_sed_control", -3), kl(-5), log("media", "A Western media offensive angers East Berlin.")))
A("church", "Aid for the Church Groups", "Money, paper and photocopiers for the peace and environment groups sheltering under the Protestant church in the East.",
  "medien", 1, 25, 540, "check_variable = { cwgg_kanal_kirche = 1 } country_exists = DDR",
  J(dv("cwddr_opposition", 4), dv("cwddr_sed_control", -2), kl(-3), log("church", "Bonn quietly supports the church groups in the GDR.")))
A("mandate", "Reassert the Sole Mandate", "Remind the world that only the Federal Republic speaks for Germany. Third states that recognise the GDR will hear from Bonn.",
  "recht", 1, 25, 365, "NOT = { check_variable = { cwgg_vertrag_3 = 1 } } country_exists = DDR",
  J(dv("cwddr_recognition", -5), kl(-8), bop(-0.1), log("mandate", "Bonn reasserts its claim to speak for all Germans.")))
A("freeze", "Freeze Credits and Deliveries", "Suspend credits and slow deliveries in inner-German trade until East Berlin moves.",
  "handel", 2, 25, 730, "check_variable = { cwgg_hebel_handel > 0 } country_exists = DDR",
  J(dv("cwddr_hard_currency", 10), dv("cwddr_west_dependency", -5), kl(-15), dr(10), log("freeze", "Bonn freezes credits to the GDR.")))
A("escape", "Tolerate Escape Helpers", "Look away while students and professional smugglers dig tunnels and fit out cars with hidden compartments.",
  "menschen", 1, 0, 365, "country_exists = DDR",
  J(dv("cwddr_exit_pressure", 4), dr(8), v("cwger_rechtsstaat", -1), "set_country_flag = { flag = cwgg_escape_helpers days = 180 value = 1 }",
    log("escape", "Escape helpers are active again. East Berlin protests.")))
A("manoeuvre", "Exercises Near the Border", "Large Bundeswehr and NATO exercises along the inner-German border: a signal to East Berlin and Moscow.",
  "allianz", 2, 25, 365, "has_country_flag = cwgg_unlock_manoeuvre country_exists = DDR check_variable = { cwgg_aufm_brd > 0 }",
  J("set_country_flag = { flag = cwgg_manoeuvre days = 180 value = 1 }", kl(-10), dr(15), tension(1),
    log("manoeuvre", "Bundeswehr exercises near the border.")))
A("raid", "Roll Up Stasi Networks", "A coordinated strike by the Federal Office for the Protection of the Constitution and the Federal Prosecutor against the HVA's networks.",
  "recht", 2, 50, 365, "country_exists = DDR",
  J(v("cwger_stasi_penetration", -10), v("cwger_counterintel", 5), kl(-5),
    *[f"if = {{ limit = {{ check_variable = {{ cwgg_kanal_{k} = 2 }} }} set_variable = {{ cwgg_kanal_{k} = 1 }} }}" for k, _, _ in CHANNELS],
    tt(f"{P}_tt_raid_channels", "Strained channels are §Gsecure§! again."),
    f"if = {{ limit = {{ has_global_flag = cwgg_raf_in_ddr NOT = {{ has_global_flag = cwgg_raf_in_ddr_found }} }} random_list = {{ 70 = {{ }} 30 = {{ set_global_flag = cwgg_raf_in_ddr_found country_event = {{ id = {EVR}.70 days = 5 }} }} }} }}",
    log("raid", "Arrests in Bonn: an HVA network is rolled up.")))
A("alert_up", "Raise Alert Level", "Put the Bundeswehr on a higher state of readiness. Each level speeds up mobilisation and hardens war support: level 1 §G+10%§! / §G+2%§!, level 2 §G+25%§! / §G+5%§!, level 3 §G+50%§! / §G+10%§!.",
  "allianz", 2, 0, 30,
  "country_exists = DDR OR = { AND = { check_variable = { cwgg_mob_brd = 0 } check_variable = { cwgg_stufe > 2 } } "
  "AND = { check_variable = { cwgg_mob_brd = 1 } check_variable = { cwgg_stufe > 3 } } "
  "AND = { check_variable = { cwgg_mob_brd = 2 } OR = { check_variable = { cwgg_stufe > 4 } has_country_flag = cwgg_unlock_alert3 } } }",
  J("add_to_variable = { cwgg_mob_brd = 1 }", f"{R}_set_stage_modifiers = yes", stab(-0.01), v("cwger_peace_movement", 3), dr(5),
    log("alert_up", "The Bundeswehr raises its alert level.")))
A("alert_down", "Lower Alert Level", "Stand the forces down by one level.",
  "allianz", 0, 0, 0, "check_variable = { cwgg_mob_brd > 0 }",
  J("add_to_variable = { cwgg_mob_brd = -1 }", f"{R}_set_stage_modifiers = yes", kl(2), log("alert_down", "The Bundeswehr lowers its alert level.")))


def trigger_file():
    out = ["## Generated by tools/west_germany_1970/compile.py. Edit the generator, not this file.\n"]
    for a in ACTIONS:
        conds = [a["trig"]]
        if a["init"]:
            conds.append(f"check_variable = {{ cwgg_init_brd > {a['init'] - 1} }}")
        if a["pp"]:
            conds.append(f"has_political_power > {a['pp'] - 1}")
        if a["cd"]:
            conds.append(f"NOT = {{ has_country_flag = cwgg_cd_{a['key']} }}")
        if a["once"]:
            conds.append(f"NOT = {{ has_country_flag = cwgg_done_{a['key']} }}")
        conds.append("NOT = { has_global_flag = " + P + "_unity_achieved }")
        out.append(f"{R}_can_{a['key']} = {{\n\t" + "\n\t".join(conds) + "\n}\n")
    for s in STANCES:
        sid, key, _n, init, pp, _d = s
        conds = ["check_variable = { cwgg_krise_typ > 0 }"]
        if init:
            conds.append(f"check_variable = {{ cwgg_init_brd > {init - 1} }}")
        if pp:
            conds.append(f"has_political_power > {pp - 1}")
        if key == "allies":
            conds.append("has_idea = NATO_member")
        if key == "secret":
            conds.append("OR = { " + " ".join(f"check_variable = {{ cwgg_kanal_{k} = 1 }} check_variable = {{ cwgg_kanal_{k} = 2 }}" for k, _, _ in CHANNELS) + " }")
        if key == "mobilise":
            conds.append("check_variable = { cwgg_stufe > 2 }")
        out.append(f"{R}_can_stance_{key} = {{\n\t" + "\n\t".join(conds) + "\n}\n")
    for t in TREATIES:
        n, key, name, desc, mink, pre, extra, _u, _rat = t
        conds = [f"check_variable = {{ cwgg_vertrag_{n} = 0 }}", "check_variable = { cwgg_verh = 0 }", f"check_variable = {{ cwgg_klima > {mink - 1} }}",
                 "check_variable = { cwgg_stufe < 3 }", "check_variable = { cwgg_init_brd > 1 }", "country_exists = DDR",
                 f"NOT = {{ has_global_flag = {P}_unity_achieved }}", extra]
        conds += [f"check_variable = {{ cwgg_vertrag_{p} = 1 }}" for p in pre]
        out.append(f"{R}_can_treaty_{n} = {{\n\t" + "\n\t".join(conds) + "\n}\n")
        out.append(f"{R}_shown_treaty_{n} = {{\n\t" + "\n\t".join([extra] + [f"check_variable = {{ cwgg_vertrag_{p} > 0 }}" for p in pre]) + "\n}\n")
    for k, name, _d in CHANNELS:
        out.append(f"{R}_can_open_{k} = {{\n\thas_country_flag = cwgg_kanal_{k}_unlocked\n\tcheck_variable = {{ cwgg_kanal_{k} = 0 }}\n\tcheck_variable = {{ cwgg_init_brd > 0 }}\n\tcountry_exists = DDR\n}}\n")
    out.append(f"{R}_hardline_moscow = {{\n\tOR = {{\n\t\thas_global_flag = {P}_moscow_coup_succeeded\n\t\tAND = {{ country_exists = SOV SOV = {{ has_completed_focus = COLDWAR_SOV_the_brezhnev_doctrine }} }}\n\t}}\n}}\n")
    out.append(f"{R}_active = {{\n\toriginal_tag = GER\n\tIMP_is_1970_scenario = yes\n\thas_country_flag = cwgg_initialized\n}}\n")
    return "\n".join(out)


# ------------------------------------------------------------------ effects
def setup():
    chan_init = "\n".join(f"set_variable = {{ cwgg_kanal_{k} = 0 }}" for k, _, _ in CHANNELS)
    treaties = "\n".join(f"set_variable = {{ cwgg_vertrag_{t[0]} = 0 }}" for t in TREATIES)
    return f"""
# ---------------------------------------------------------------- rivalry setup
{R}_setup = {{
	set_country_flag = cwgg_initialized
	set_variable = {{ cwgg_klima = -5 }}
	set_variable = {{ cwgg_druck = 10 }}
	set_variable = {{ cwgg_stufe = 2 }}
	set_variable = {{ cwgg_init_brd = 2 }}
	set_variable = {{ cwgg_init_ddr = 2 }}
	set_variable = {{ cwgg_mob_brd = 0 }}
	set_variable = {{ cwgg_mob_ddr = 0 }}
	set_variable = {{ cwgg_aufm_brd = 0 }}
	set_variable = {{ cwgg_aufm_ddr = 0 }}
	set_variable = {{ cwgg_aufm_brd_m = 0 }}
	set_variable = {{ cwgg_aufm_ddr_m = 0 }}
	set_variable = {{ cwgg_aufm_brd_div = 0 }}
	set_variable = {{ cwgg_aufm_ddr_div = 0 }}
	set_variable = {{ cwgg_krise_typ = 0 }}
	set_variable = {{ cwgg_krise_int = 0 }}
	set_variable = {{ cwgg_krise_monat = 0 }}
	set_variable = {{ cwgg_ddr_wahl = 0 }}
	set_variable = {{ cwgg_haltung = 1 }}
	set_variable = {{ cwgg_last_h = 0 }}
	set_variable = {{ cwgg_last_a = 0 }}
	set_variable = {{ cwgg_countdown = 0 }}
	set_variable = {{ cwgg_verh = 0 }}
	set_variable = {{ cwgg_verh_prog = 0 }}
	set_variable = {{ cwgg_months = 0 }}
	set_variable = {{ cwgg_year = 1970 }}
	set_variable = {{ cwgg_crises_total = 0 }}
	set_variable = {{ cwgg_crises_won = 0 }}
	set_variable = {{ cwgg_crises_lost = 0 }}
	set_variable = {{ cwgg_tab = 1 }}
	{treaties}
	{chan_init}
	# the lawyers' channel has existed since 1964, the first prisoners were bought free in 1963
	set_country_flag = cwgg_kanal_vogel_unlocked
	set_variable = {{ cwgg_kanal_vogel = 1 }}
	set_variable = {{ cwgg_hebel_devisen = 1 }}
	set_variable = {{ cwgg_hebel_menschen = 1 }}
	set_variable = {{ cwgg_hebel_medien = 2 }}
	set_variable = {{ cwgg_hebel_recht = 2 }}
	set_variable = {{ cwgg_hebel_allianz = 2 }}
	set_variable = {{ cwgg_hebel_handel = 1 }}
	set_variable = {{ cwgg_dhebel_transit = 2 }}
	set_variable = {{ cwgg_dhebel_zwang = 1 }}
	set_variable = {{ cwgg_dhebel_stasi = 2 }}
	set_variable = {{ cwgg_dhebel_grenze = 2 }}
	set_variable = {{ cwgg_ost_last = cwger_ostpolitik }}
	set_variable = {{ cwgg_log_1 = 0 }}
	set_variable = {{ cwgg_log_2 = 0 }}
	set_variable = {{ cwgg_log_3 = 0 }}
	set_variable = {{ cwgg_log_4 = 0 }}
	set_variable = {{ cwgg_log_5 = 0 }}
	add_dynamic_modifier = {{ modifier = {P}_dm_inner_german }}
	if = {{ limit = {{ country_exists = DDR }} DDR = {{ add_dynamic_modifier = {{ modifier = {P}_dm_inner_german_ddr }} }} }}
	{log("start", "Two German states, no treaty between them. Bonn does not recognise the GDR.")}
	{R}_set_stage_modifiers = yes
	{R}_gui_refresh = yes
}}

# Pushes temp cwgg_t_log into the five-line situation report.
{R}_log = {{
	set_variable = {{ cwgg_log_5 = cwgg_log_4 }}
	set_variable = {{ cwgg_log_y_5 = cwgg_log_y_4 }}
	set_variable = {{ cwgg_log_4 = cwgg_log_3 }}
	set_variable = {{ cwgg_log_y_4 = cwgg_log_y_3 }}
	set_variable = {{ cwgg_log_3 = cwgg_log_2 }}
	set_variable = {{ cwgg_log_y_3 = cwgg_log_y_2 }}
	set_variable = {{ cwgg_log_2 = cwgg_log_1 }}
	set_variable = {{ cwgg_log_y_2 = cwgg_log_y_1 }}
	set_variable = {{ cwgg_log_1 = cwgg_t_log }}
	set_variable = {{ cwgg_log_y_1 = cwgg_year }}
}}
"""


def stage_effects():
    # target stage from climate and crisis intensity; offsets give hysteresis
    def target(kv, iv):
        return f"""
	set_temp_variable = {{ cwgg_t_s = 3 }}
	if = {{ limit = {{ check_variable = {{ {kv} > 39 }} }} set_temp_variable = {{ cwgg_t_s = 0 }} }}
	else_if = {{ limit = {{ check_variable = {{ {kv} > 9 }} }} set_temp_variable = {{ cwgg_t_s = 1 }} }}
	else_if = {{ limit = {{ check_variable = {{ {kv} > -21 }} }} set_temp_variable = {{ cwgg_t_s = 2 }} }}
	if = {{ limit = {{ check_variable = {{ {iv} > 49 }} check_variable = {{ cwgg_t_s < 3 }} }} set_temp_variable = {{ cwgg_t_s = 3 }} }}
	if = {{ limit = {{ OR = {{ check_variable = {{ {kv} < -45 }} check_variable = {{ {iv} > 74 }} }} check_variable = {{ cwgg_t_s < 4 }} }} set_temp_variable = {{ cwgg_t_s = 4 }} }}
	if = {{ limit = {{ OR = {{ AND = {{ check_variable = {{ {iv} > 89 }} check_variable = {{ {kv} < -60 }} }} AND = {{ check_variable = {{ cwgg_mob_brd > 2 }} check_variable = {{ cwgg_mob_ddr > 2 }} }} AND = {{ check_variable = {{ cwgg_aufm_brd > 2 }} check_variable = {{ cwgg_aufm_ddr > 2 }} }} check_variable = {{ cwgg_countdown > 0 }} }} }} set_temp_variable = {{ cwgg_t_s = 5 }} }}
	# troops massed at the border: one side means crisis, both sides confrontation
	if = {{ limit = {{ OR = {{ check_variable = {{ cwgg_aufm_brd > 1 }} check_variable = {{ cwgg_aufm_ddr > 1 }} }} check_variable = {{ cwgg_t_s < 3 }} }} set_temp_variable = {{ cwgg_t_s = 3 }} }}
	if = {{ limit = {{ check_variable = {{ cwgg_aufm_brd > 1 }} check_variable = {{ cwgg_aufm_ddr > 1 }} check_variable = {{ cwgg_t_s < 4 }} }} set_temp_variable = {{ cwgg_t_s = 4 }} }}"""
    dm = []
    for i, (st, w, cg, fac, ten) in enumerate(STAGE_DM):
        d_st, d_w, d_cg = STAGE_DM_DDR[i]
        kw = "if" if i == 0 else "else_if"
        ten_s = f"set_temp_variable = {{ mdcw_cw_tension_delta = {ten} }} mdcw_cw_add_tension = yes" if ten else ""
        dm.append(f"""	{kw} = {{ limit = {{ check_variable = {{ cwgg_stufe = {i} }} }}
		set_variable = {{ cwgg_dm_stab = {st} }} set_variable = {{ cwgg_dm_ws = {w} }} set_variable = {{ cwgg_dm_cg = {cg} }} set_variable = {{ cwgg_dm_fac = {fac} }}
		if = {{ limit = {{ country_exists = DDR }} DDR = {{ set_variable = {{ cwgg_dm_stab = {d_st} }} set_variable = {{ cwgg_dm_ws = {d_w} }} set_variable = {{ cwgg_dm_cg = {d_cg} }} }} }}
		set_temp_variable = {{ cwgg_t_ten = {ten} }}
	}}""")
    def alert_rows(who):
        rows = []
        for lvl, (mob, w) in enumerate(ALERT_LEVELS):
            kw = "if" if lvl == 0 else "else_if"
            body = "set_variable = { cwgg_dm_mob = %s }" % mob + (" add_to_variable = { cwgg_dm_ws = %s }" % w if w else "")
            rows.append("%s = { limit = { check_variable = { GER.cwgg_mob_%s = %d } } %s }" % (kw, who, lvl, body))
        return "\n\t\t".join(rows)
    alerts = ("\t" + alert_rows("brd").replace("\n\t\t", "\n\t") +
              "\n\tif = { limit = { country_exists = DDR }\n\t\tDDR = {\n\t\t" + alert_rows("ddr") + "\n\t\t}\n\t}")
    return f"""
# ---------------------------------------------------------------- stages of the escalation ladder
{R}_update_stage = {{
	if = {{ limit = {{ NOT = {{ check_variable = {{ cwgg_stufe = 6 }} }} }}
		set_temp_variable = {{ cwgg_t_old = cwgg_stufe }}
		# going up needs the numbers to be clearly worse, going down clearly better
		set_temp_variable = {{ cwgg_t_k = cwgg_klima }}
		set_temp_variable = {{ cwgg_t_i = cwgg_krise_int }}
		add_to_temp_variable = {{ cwgg_t_k = 5 }}
		add_to_temp_variable = {{ cwgg_t_i = -5 }}
		{target("cwgg_t_k", "cwgg_t_i")}
		set_temp_variable = {{ cwgg_t_up = cwgg_t_s }}
		set_temp_variable = {{ cwgg_t_k = cwgg_klima }}
		set_temp_variable = {{ cwgg_t_i = cwgg_krise_int }}
		add_to_temp_variable = {{ cwgg_t_k = -5 }}
		add_to_temp_variable = {{ cwgg_t_i = 5 }}
		{target("cwgg_t_k", "cwgg_t_i")}
		set_temp_variable = {{ cwgg_t_down = cwgg_t_s }}
		if = {{ limit = {{ check_variable = {{ cwgg_t_up > cwgg_stufe }} }} set_variable = {{ cwgg_stufe = cwgg_t_up }} }}
		else_if = {{ limit = {{ check_variable = {{ cwgg_t_down < cwgg_stufe }} }} set_variable = {{ cwgg_stufe = cwgg_t_down }} }}
		if = {{ limit = {{ check_variable = {{ cwgg_stufe > cwgg_t_old }} }}
			{log("stage_up", "The inner-German relationship worsens.")}
			if = {{ limit = {{ check_variable = {{ cwgg_stufe > 3 }} }} country_event = {{ id = {EVR}.5 days = 1 }} }}
		}}
		if = {{ limit = {{ check_variable = {{ cwgg_stufe < cwgg_t_old }} }}
			{log("stage_down", "Relations between the two German states ease.")}
		}}
	}}
	{R}_set_stage_modifiers = yes
}}

{R}_set_stage_modifiers = {{
	set_temp_variable = {{ cwgg_t_ten = 0 }}
{chr(10).join(dm)}
	# alert levels: each step speeds up mobilisation and hardens war support (Bundeswehr on GER, NVA on the GDR)
{alerts}
}}

# Monthly world tension from the ladder (Imperia).
{R}_stage_tension = {{
	if = {{ limit = {{ has_global_flag = mdcw_cw_initialized NOT = {{ check_variable = {{ cwgg_t_ten = 0 }} }} }}
		set_temp_variable = {{ mdcw_cw_tension_delta = cwgg_t_ten }}
		mdcw_cw_add_tension = yes
	}}
	if = {{ limit = {{ has_global_flag = mdcw_cw_initialized check_variable = {{ cwgg_stufe = 5 }} check_variable = {{ global.mdcw_cw_tension < 70 }} }}
		set_temp_variable = {{ mdcw_cw_tension_delta = 70 }}
		subtract_from_temp_variable = {{ mdcw_cw_tension_delta = global.mdcw_cw_tension }}
		mdcw_cw_add_tension = yes
	}}
}}
"""


def monthly():
    leak = []
    for k, _, _ in CHANNELS:
        leak.append(f"""	if = {{ limit = {{ check_variable = {{ cwgg_kanal_{k} = 1 }} }}
		random_list = {{
			100 = {{ }}
			1 = {{
				modifier = {{ add = 1 check_variable = {{ cwger_stasi_penetration > 30 }} }}
				modifier = {{ add = 2 check_variable = {{ cwger_stasi_penetration > 50 }} }}
				modifier = {{ add = 3 check_variable = {{ cwger_stasi_penetration > 70 }} }}
				modifier = {{ factor = 0.5 check_variable = {{ cwger_counterintel > 60 }} }}
				set_variable = {{ cwgg_kanal_{k} = 2 }}
				set_country_flag = {{ flag = cwgg_strained_{k} days = 365 value = 1 }}
				{log(f"leak_{k}", "The BfV suspects the Stasi is listening on one of Bonn's channels.")}
			}}
		}}
	}}
	if = {{ limit = {{ check_variable = {{ cwgg_kanal_{k} = 2 }} NOT = {{ has_country_flag = cwgg_strained_{k} }} }} set_variable = {{ cwgg_kanal_{k} = 1 }} }}""")
    basis_ch = "\n".join(
        f"\tif = {{ limit = {{ check_variable = {{ cwgg_kanal_{k} = 1 }} }} add_to_temp_variable = {{ cwgg_t_b = 2 }} }}\n"
        f"\tif = {{ limit = {{ check_variable = {{ cwgg_kanal_{k} = 2 }} }} add_to_temp_variable = {{ cwgg_t_b = 1 }} }}" for k, _, _ in CHANNELS)
    basis_tr = "\n".join(f"\tif = {{ limit = {{ check_variable = {{ cwgg_vertrag_{t[0]} = 1 }} }} add_to_temp_variable = {{ cwgg_t_b = 4 }} }}" for t in TREATIES)
    return f"""
# ---------------------------------------------------------------- monthly tick (GER scope)
{R}_tick = {{
	if = {{ limit = {{ NOT = {{ has_country_flag = cwgg_initialized }} }} {R}_setup = yes }}
	add_to_variable = {{ cwgg_months = 1 }}
	if = {{ limit = {{ check_variable = {{ cwgg_months > 11 }} }}
		set_variable = {{ cwgg_months = 0 }}
		add_to_variable = {{ cwgg_year = 1 }}
	}}
	if = {{ limit = {{ NOT = {{ country_exists = DDR }} }}
		set_variable = {{ cwgg_krise_typ = 0 }}
		set_variable = {{ cwgg_krise_int = 0 }}
		if = {{ limit = {{ NOT = {{ check_variable = {{ cwgg_stufe = 6 }} }} }} set_variable = {{ cwgg_stufe = 0 }} }}
	}}
	if = {{ limit = {{ country_exists = DDR NOT = {{ has_global_flag = {P}_unity_achieved }} }}
		# events and focuses written for the old 'rapprochement' meter still move the climate
		set_temp_variable = {{ cwgg_t = cwger_ostpolitik }}
		subtract_from_temp_variable = {{ cwgg_t = cwgg_ost_last }}
		multiply_temp_variable = {{ cwgg_t = 2 }}
		add_to_variable = {{ cwgg_klima = cwgg_t }}
		{R}_initiative = yes
{chr(10).join(leak)}
		{R}_climate = yes
		{R}_negotiation_tick = yes
		# East Berlin's AI only acts for an AI GDR; a human GDR uses its decisions
		if = {{ limit = {{ DDR = {{ is_ai = yes }} }} {R}_ddr_ai = yes }}
		if = {{ limit = {{ is_ai = yes }} {R}_bonn_ai = yes }}
		{R}_border_watch = yes
		{R}_crisis_clock = yes
		{R}_crisis_roll = yes
		{R}_war_watch = yes
		{R}_update_stage = yes
		{R}_stage_tension = yes
		# the old meter now follows the climate
		set_variable = {{ cwger_ostpolitik = cwgg_klima }}
		add_to_variable = {{ cwger_ostpolitik = 100 }}
		divide_variable = {{ cwger_ostpolitik = 2 }}
		set_variable = {{ cwgg_ost_last = cwger_ostpolitik }}
	}}
	if = {{ limit = {{ check_variable = {{ cwgg_stufe = 6 }} }} {R}_war_watch = yes }}
	{R}_gui_refresh = yes
}}

{R}_initiative = {{
	add_to_variable = {{ cwgg_init_brd = 1 }}
	if = {{ limit = {{ check_variable = {{ cwgg_kanal_sv = 1 }} }} add_to_variable = {{ cwgg_init_brd = 1 }} }}
	if = {{ limit = {{ has_country_flag = cwgg_init_bonus }} random_list = {{ 50 = {{ add_to_variable = {{ cwgg_init_brd = 1 }} }} 50 = {{ }} }} }}
	if = {{ limit = {{ check_variable = {{ cwgg_stufe > 2 }} }} add_to_variable = {{ cwgg_init_brd = 1 }} }}
	clamp_variable = {{ var = cwgg_init_brd min = 0 max = 6 }}
	add_to_variable = {{ cwgg_init_ddr = 1 }}
	if = {{ limit = {{ check_variable = {{ cwgg_stufe > 2 }} }} add_to_variable = {{ cwgg_init_ddr = 1 }} }}
	if = {{ limit = {{ DDR = {{ check_variable = {{ cwddr_sed_control > 70 }} }} }} random_list = {{ 50 = {{ add_to_variable = {{ cwgg_init_ddr = 1 }} }} 50 = {{ }} }} }}
	clamp_variable = {{ var = cwgg_init_ddr min = 0 max = 6 }}
}}

# Climate drifts towards a base set by treaties, world tension, the SED leader, Moscow,
# the Deutschlandpolitik balance, the government in Bonn and the open channels.
{R}_climate = {{
	set_temp_variable = {{ cwgg_t_b = 0 }}
{basis_tr}
{basis_ch}
	if = {{ limit = {{ has_global_flag = mdcw_cw_initialized }}
		set_temp_variable = {{ cwgg_t = global.mdcw_cw_tension }}
		subtract_from_temp_variable = {{ cwgg_t = 50 }}
		divide_temp_variable = {{ cwgg_t = 4 }}
		subtract_from_temp_variable = {{ cwgg_t_b = cwgg_t }}
	}}
	if = {{ limit = {{ DDR = {{ check_variable = {{ cwddr_leader = 0 }} }} }} add_to_temp_variable = {{ cwgg_t_b = -5 }} }}
	else_if = {{ limit = {{ DDR = {{ check_variable = {{ cwddr_leader = 1 }} }} date > 1979.12.31 date < 1983.1.1 }} add_to_temp_variable = {{ cwgg_t_b = -5 }} }}
	else_if = {{ limit = {{ DDR = {{ check_variable = {{ cwddr_leader = 1 }} }} date > 1982.12.31 }} add_to_temp_variable = {{ cwgg_t_b = 5 }} }}
	else_if = {{ limit = {{ DDR = {{ check_variable = {{ cwddr_leader = 2 }} }} }} add_to_temp_variable = {{ cwgg_t_b = -5 }} }}
	else_if = {{ limit = {{ DDR = {{ check_variable = {{ cwddr_leader = 3 }} }} }} add_to_temp_variable = {{ cwgg_t_b = 15 }} }}
	else_if = {{ limit = {{ DDR = {{ check_variable = {{ cwddr_leader > 3 }} }} }} add_to_temp_variable = {{ cwgg_t_b = 20 }} }}
	if = {{ limit = {{ has_global_flag = {P}_moscow_coup_succeeded }} add_to_temp_variable = {{ cwgg_t_b = -25 }} }}
	else_if = {{ limit = {{ country_exists = SOV SOV = {{ has_completed_focus = COLDWAR_SOV_gor_the_sinatra_doctrine }} }} add_to_temp_variable = {{ cwgg_t_b = 15 }} }}
	else_if = {{ limit = {{ country_exists = SOV SOV = {{ OR = {{ has_completed_focus = COLDWAR_SOV_gor_new_thinking has_completed_focus = COLDWAR_SOV_gor_glasnost_first }} }} }} add_to_temp_variable = {{ cwgg_t_b = 10 }} }}
	else_if = {{ limit = {{ country_exists = SOV SOV = {{ has_completed_focus = COLDWAR_SOV_the_brezhnev_doctrine }} }} add_to_temp_variable = {{ cwgg_t_b = -10 }} }}
	if = {{ limit = {{ check_variable = {{ ruling_party = 1 }} }} add_to_temp_variable = {{ cwgg_t_b = -5 }} }}
	if = {{ limit = {{ OR = {{ check_variable = {{ ruling_party = 17 }} is_in_array = {{ gov_coalition_array = 17 }} }} }} add_to_temp_variable = {{ cwgg_t_b = 3 }} }}
	if = {{ limit = {{ has_country_flag = {P}_double_track }} add_to_temp_variable = {{ cwgg_t_b = -5 }} }}
	if = {{ limit = {{ has_country_flag = cwgg_zero_option }} add_to_temp_variable = {{ cwgg_t_b = 5 }} }}
	if = {{ limit = {{ has_country_flag = cwgg_policy_strength }} add_to_temp_variable = {{ cwgg_t_b = -10 }} }}
	if = {{ limit = {{ has_country_flag = cwgg_policy_rapprochement }} add_to_temp_variable = {{ cwgg_t_b = 5 }} }}
	add_to_temp_variable = {{ cwgg_t_b = cwgg_basis_bonus }}
	clamp_temp_variable = {{ var = cwgg_t_b min = -100 max = 100 }}
	set_variable = {{ cwgg_basis = cwgg_t_b }}
	# drift 5 % towards the base, minus a share of the escalation pressure
	set_temp_variable = {{ cwgg_t = cwgg_basis }}
	subtract_from_temp_variable = {{ cwgg_t = cwgg_klima }}
	multiply_temp_variable = {{ cwgg_t = 0.05 }}
	set_temp_variable = {{ cwgg_t2 = cwgg_druck }}
	multiply_temp_variable = {{ cwgg_t2 = 0.03 }}
	subtract_from_temp_variable = {{ cwgg_t = cwgg_t2 }}
	add_to_variable = {{ cwgg_klima = cwgg_t }}
	clamp_variable = {{ var = cwgg_klima min = -100 max = 100 }}
	multiply_variable = {{ cwgg_druck = 0.9 }}
	clamp_variable = {{ var = cwgg_druck min = 0 max = 100 }}
}}

"""


def border_watch():
    def count(side, states):
        lines = [f"\tset_variable = {{ cwgg_aufm_{side}_div = 0 }}"]
        for st in states:
            for n, add in BORDER_STEPS:
                cond = f"divisions_in_state = {{ state = {st} size > {n - 1} }}"
                if side == "ddr":
                    cond = f"DDR = {{ {cond} }}"
                lines.append(f"\tif = {{ limit = {{ {cond} }} add_to_variable = {{ cwgg_aufm_{side}_div = {add} }} }}")
        lines.append(f"\tset_variable = {{ cwgg_aufm_{side} = 0 }}")
        for lvl, n in enumerate(BORDER_LEVELS, start=1):
            lines.append(f"\tif = {{ limit = {{ check_variable = {{ cwgg_aufm_{side}_div > {n - 1} }} }} set_variable = {{ cwgg_aufm_{side} = {lvl} }} }}")
        return "\n".join(lines)

    def effects(side):
        eff = []
        for lvl, (dp, dk, ten) in enumerate(BORDER_EFFECT):
            if not lvl:
                continue
            ten_s = f" if = {{ limit = {{ has_global_flag = mdcw_cw_initialized }} set_temp_variable = {{ mdcw_cw_tension_delta = {ten} }} mdcw_cw_add_tension = yes }}" if ten else ""
            eff.append(f"\tif = {{ limit = {{ check_variable = {{ cwgg_aufm_{side} = {lvl} }} }} add_to_variable = {{ cwgg_druck = {dp} }} add_to_variable = {{ cwgg_klima = {dk} }}{ten_s} }}")
        return "\n".join(eff)
    who = {"brd": "The Bundeswehr", "ddr": "The National People's Army"}
    return f"""
# ---------------------------------------------------------------- troops at the inner-German border
# Counts the divisions both sides have in their border states (vanilla divisions_in_state).
# Called monthly by the tick and whenever the window is refreshed, so the display is always current.
{R}_border_count = {{
	if = {{ limit = {{ country_exists = DDR }}
{count("brd", BORDER_BRD)}
{count("ddr", BORDER_DDR)}
	}}
	else = {{
		set_variable = {{ cwgg_aufm_brd = 0 }} set_variable = {{ cwgg_aufm_brd_div = 0 }}
		set_variable = {{ cwgg_aufm_ddr = 0 }} set_variable = {{ cwgg_aufm_ddr_div = 0 }}
	}}
}}

# Monthly: massed troops raise escalation pressure and Cold War world tension, cost climate and push the
# ladder; the other side is told when the build-up grows.
{R}_border_watch = {{
	if = {{ limit = {{ country_exists = DDR NOT = {{ check_variable = {{ cwgg_stufe = 6 }} }} }}
	set_temp_variable = {{ cwgg_t_old_brd = cwgg_aufm_brd_m }}
	set_temp_variable = {{ cwgg_t_old_ddr = cwgg_aufm_ddr_m }}
	{R}_border_count = yes
	set_variable = {{ cwgg_aufm_brd_m = cwgg_aufm_brd }}
	set_variable = {{ cwgg_aufm_ddr_m = cwgg_aufm_ddr }}
{effects("brd")}
{effects("ddr")}
	if = {{ limit = {{ check_variable = {{ cwgg_aufm_brd > cwgg_t_old_brd }} }}
		{log("aufm_brd", who["brd"] + " masses troops along the inner-German border.")}
		if = {{ limit = {{ DDR = {{ is_ai = no }} }} DDR = {{ country_event = {{ id = {EVR}.241 days = 1 }} }} }}
	}}
	if = {{ limit = {{ check_variable = {{ cwgg_aufm_ddr > cwgg_t_old_ddr }} }}
		{log("aufm_ddr", who["ddr"] + " masses troops along the inner-German border.")}
		if = {{ limit = {{ is_ai = no }} country_event = {{ id = {EVR}.240 days = 1 }} }}
	}}
	clamp_variable = {{ var = cwgg_druck min = 0 max = 100 }}
	clamp_variable = {{ var = cwgg_klima min = -100 max = 100 }}
	}}
}}
"""


def negotiation():
    starts, ends = [], []
    for t in TREATIES:
        n, key, name, desc, mink, pre, extra, _u, rat = t
        starts.append(f"""{R}_start_treaty_{n} = {{
	add_to_variable = {{ cwgg_init_brd = -2 }}
	add_political_power = -25
	set_variable = {{ cwgg_verh = {n} }}
	set_variable = {{ cwgg_verh_prog = 0 }}
	{log(f"nego_{n}", f"Negotiations open: {name}.")}
	{R}_gui_refresh = yes
}}""")
    return f"""
# ---------------------------------------------------------------- treaty negotiations
{chr(10).join(starts)}

{R}_negotiation_tick = {{
	if = {{ limit = {{ check_variable = {{ cwgg_verh > 0 }} }}
		if = {{ limit = {{ check_variable = {{ cwgg_stufe > 3 }} }}
			set_variable = {{ cwgg_verh = 0 }}
			set_variable = {{ cwgg_verh_prog = 0 }}
			{log("nego_broken", "The crisis has broken off the negotiations.")}
		}}
		else_if = {{ limit = {{ check_variable = {{ cwgg_stufe < 3 }} }}
			set_temp_variable = {{ cwgg_t = 12 }}
			if = {{ limit = {{ check_variable = {{ cwgg_kanal_bahr = 1 }} }} add_to_temp_variable = {{ cwgg_t = 4 }} }}
			if = {{ limit = {{ check_variable = {{ cwgg_kanal_sv = 1 }} }} add_to_temp_variable = {{ cwgg_t = 4 }} }}
			if = {{ limit = {{ check_variable = {{ cwgg_kanal_draht = 1 }} check_variable = {{ cwgg_verh < 3 }} }} add_to_temp_variable = {{ cwgg_t = 3 }} }}
			set_temp_variable = {{ cwgg_t2 = cwgg_klima }}
			divide_temp_variable = {{ cwgg_t2 = 10 }}
			add_to_temp_variable = {{ cwgg_t = cwgg_t2 }}
			set_temp_variable = {{ cwgg_t2 = cwgg_hebel_devisen }}
			multiply_temp_variable = {{ cwgg_t2 = 2 }}
			add_to_temp_variable = {{ cwgg_t = cwgg_t2 }}
			if = {{ limit = {{ has_country_flag = cwgg_policy_rapprochement }} multiply_temp_variable = {{ cwgg_t = 1.25 }} }}
			if = {{ limit = {{ DDR = {{ check_variable = {{ cwddr_leader = 0 }} }} check_variable = {{ cwgg_verh > 2 }} }} multiply_temp_variable = {{ cwgg_t = 0.5 }} }}
			clamp_temp_variable = {{ var = cwgg_t min = 2 max = 30 }}
			add_to_variable = {{ cwgg_verh_prog = cwgg_t }}
			if = {{ limit = {{ check_variable = {{ cwgg_verh_prog > 99 }} }}
				set_variable = {{ cwgg_verh_prog = 100 }}
				country_event = {{ id = {EVR}.50 days = 1 }}
			}}
		}}
	}}
}}
"""


def treaty_effects():
    eff = {
        1: J(channel_unlock("bahr", True), kl(10), "if = { limit = { country_exists = DDR } DDR = { country_event = { id = COLDWAR_DDR.10 days = 2 } } }", stab(0.01), party("spd", 0.004), set_flag("cwgg_unlock_vertrag_2"),
             log("t1", "Brandt and Stoph meet. 'Willy, Willy!' in front of the Erfurter Hof.")),
        2: J(f"set_country_flag = {P}_berlin_agreement", "set_global_flag = COLDWAR_SOV_berlin_agreement", v("cwger_berlin_access", 20),
             lever("transit", -1, ddr=True), lever("handel", 1), kl(8), tension(-2), channel_unlock("draht"),
             log("t2", "The Berlin settlement is signed. Transit becomes routine.")),
        3: J(dv("cwddr_recognition", 15), kl(10), f"if = {{ limit = {{ has_idea = {P}_idea_hallstein_legacy }} remove_ideas = {P}_idea_hallstein_legacy }}",
             f"set_country_flag = {P}_basic_treaty", bop(0.15), f"set_country_flag = {P}_treaties_ratified",
             "if = { limit = { country_exists = DDR } DDR = { country_event = { id = COLDWAR_DDR.11 days = 3 } } }",
             "country_event = { id = COLDWAR_GER.40 days = 200 }", log("t3", "The Basic Treaty is ratified. Two states, one nation.")),
        4: J(dv("cwddr_recognition", 10), tension(-2), kl(4), f"set_country_flag = {P}_un_member", f"add_ideas = {P}_idea_un_member",
             log("t4", "Both German states take their seats in the United Nations.")),
        5: J(channel_unlock("sv", True), kl(6), log("t5", "Permanent Representations open in Bonn and East Berlin.")),
        6: J(dv("cwddr_west_media", 5), dv("cwddr_exit_pressure", 3), kl(6), stab(0.01),
             log("t6", "New crossings, telephone lines and visits for pensioners.")),
        7: J(dv("cwddr_opposition", 3), kl(6), channel_unlock("kirche"), log("t7", "Cultural agreement signed; the first towns are twinned.")),
        8: J(dv("cwddr_sed_control", -5), kl(8), "if = { limit = { country_exists = DDR } DDR = { country_event = { id = COLDWAR_DDR.8 days = 2 } } }", v("cwger_csu_autonomy", 5), party("cdu", -0.003),
             log("t8", "The SED leader is received in Bonn with flags and anthems.")),
        9: J(f"set_country_flag = {P}_confederation_offered", v("cwger_unity", 15), kl(10),
             log("t9", "A treaty community between the two German states is agreed.")),
    }
    out = []
    for t in TREATIES:
        n = t[0]
        out.append(f"{R}_treaty_{n} = {{\n\tset_variable = {{ cwgg_vertrag_{n} = 1 }}\n{fmt(hide_vars_local(eff[n]), 1)}\n}}")
    return "\n# ---------------------------------------------------------------- treaty effects\n" + "\n\n".join(out) + "\n"


def set_flag(f):
    return f"set_country_flag = {f}"


def hide_vars_local(s):
    from tooltips import hide_vars
    return hide_vars(s)


def ddr_ai():
    return f"""
# ---------------------------------------------------------------- East Berlin's moves between crises
{R}_ddr_ai = {{
	if = {{ limit = {{ check_variable = {{ cwgg_krise_typ = 0 }} check_variable = {{ cwgg_init_ddr > 1 }} NOT = {{ has_country_flag = cwgg_ddr_ai_cd }} }}
		random_list = {{
			60 = {{ }}
			40 = {{
				add_to_variable = {{ cwgg_init_ddr = -2 }}
				set_country_flag = {{ flag = cwgg_ddr_ai_cd days = 45 value = 1 }}
				random_list = {{
					10 = {{
						modifier = {{ add = 15 DDR = {{ check_variable = {{ cwddr_hard_currency > 50 }} }} }}
						modifier = {{ factor = 0 check_variable = {{ cwgg_dhebel_zwang > 2 }} }}
						modifier = {{ factor = 0.3 DDR = {{ check_variable = {{ cwddr_leader > 2 }} }} }}
						{lever("zwang", 1, ddr=True, show=False)}
						{kl(-6, False)}
						DDR = {{ {dv_self("cwddr_hard_currency", -3, show=False)} {dv_self("cwddr_exit_pressure", 1, show=False)} }}
						country_event = {{ id = {EVR}.121 days = 1 }}
					}}
					10 = {{
						modifier = {{ factor = 0.2 check_variable = {{ cwgg_vertrag_2 = 1 }} }}
						modifier = {{ factor = 0 check_variable = {{ cwgg_dhebel_transit = 0 }} }}
						modifier = {{ factor = 0.3 DDR = {{ check_variable = {{ cwddr_leader > 2 }} }} }}
						{kl(-5, False)}
						{dr(12, False)}
						{v("cwger_berlin_access", -5, show=False)}
						{log("ddr_transit", "Hours of checks on the transit autobahn to Berlin.")}
					}}
					15 = {{
						add_to_variable = {{ cwger_stasi_penetration = 4 }}
						clamp_variable = {{ var = cwger_stasi_penetration min = 0 max = 100 }}
						if = {{ limit = {{ check_variable = {{ cwger_counterintel > 40 }} }} {log("ddr_stasi", "The BfV reports increased HVA activity in Bonn.")} }}
					}}
					10 = {{
						modifier = {{ factor = 0 check_variable = {{ cwgg_vertrag_3 = 1 }} }}
						modifier = {{ factor = 0 DDR = {{ check_variable = {{ cwddr_recognition > 79 }} }} }}
						DDR = {{ {dv_self("cwddr_recognition", 4, show=False)} }}
						{kl(-3, False)}
						{log("ddr_recog", "Another state in the Third World recognises the GDR.")}
						if = {{ limit = {{ check_variable = {{ cwgg_hebel_recht > 1 }} }}
							random_list = {{ 70 = {{ }} 30 = {{ set_temp_variable = {{ cwgg_t_typ = 5 }} {R}_start_crisis = yes }} }}
						}}
					}}
					8 = {{
						modifier = {{ add = 15 DDR = {{ check_variable = {{ cwddr_exit_pressure > 50 }} }} }}
						modifier = {{ factor = 0 check_variable = {{ cwgg_dhebel_grenze > 2 }} }}
						modifier = {{ factor = 0.2 DDR = {{ check_variable = {{ cwddr_leader > 2 }} }} }}
						{lever("grenze", 1, ddr=True, show=False)}
						{dr(8, False)}
						DDR = {{ {dv_self("cwddr_exit_pressure", -3, show=False)} }}
						country_event = {{ id = {EVR}.122 days = 1 }}
					}}
					0 = {{
						modifier = {{ add = 25 DDR = {{ check_variable = {{ cwddr_hard_currency > 55 }} }} }}
						modifier = {{ factor = 0 has_country_flag = cwgg_credit_asked }}
						set_country_flag = {{ flag = cwgg_credit_asked days = 720 value = 1 }}
						country_event = {{ id = {EVR}.60 days = 2 }}
					}}
					5 = {{
						modifier = {{ add = 10 DDR = {{ check_variable = {{ cwddr_leader = 1 }} }} }}
						modifier = {{ add = 10 DDR = {{ check_variable = {{ cwddr_leader = 1 }} }} date > 1982.12.31 }}
						modifier = {{ add = 25 DDR = {{ check_variable = {{ cwddr_leader > 2 }} }} }}
						modifier = {{ add = 10 check_variable = {{ cwgg_klima > 0 }} }}
						{kl(6, False)}
						if = {{ limit = {{ check_variable = {{ cwgg_dhebel_grenze > 0 }} }} {lever("grenze", -1, ddr=True, show=False)} }}
						if = {{ limit = {{ check_variable = {{ cwgg_dhebel_zwang > 0 }} }} {lever("zwang", -1, ddr=True, show=False)} }}
						country_event = {{ id = {EVR}.123 days = 1 }}
					}}
				}}
			}}
		}}
	}}
}}
"""


def bonn_ai():
    """Bonn as AI: the historical path is rapprochement under the SPD, continuity under Kohl."""
    tre = "\n".join(
        f"\t\t\t{'if' if i == 0 else 'else_if'} = {{ limit = {{ {R}_can_treaty_{t[0]} = yes }} {R}_start_treaty_{t[0]} = yes }}"
        for i, t in enumerate(TREATIES))
    return f"""
{R}_bonn_ai = {{
	if = {{ limit = {{ check_variable = {{ cwgg_verh = 0 }} check_variable = {{ cwgg_krise_typ = 0 }} }}
		random_list = {{
			50 = {{ }}
			50 = {{
{tre}
			}}
		}}
	}}
	if = {{ limit = {{ check_variable = {{ cwgg_kanal_sv = 0 }} {R}_can_open_sv = yes }} {R}_open_sv = yes }}
	if = {{ limit = {{ check_variable = {{ cwgg_kanal_bahr = 0 }} {R}_can_open_bahr = yes }} {R}_open_bahr = yes }}
	if = {{ limit = {{ check_variable = {{ cwgg_kanal_draht = 0 }} {R}_can_open_draht = yes }} {R}_open_draht = yes }}
	if = {{ limit = {{ {R}_can_freikauf = yes }} random_list = {{ 70 = {{ }} 30 = {{ {R}_act_freikauf = yes }} }} }}
	if = {{ limit = {{ {R}_can_swing = yes check_variable = {{ ruling_party = 3 }} }} random_list = {{ 80 = {{ }} 20 = {{ {R}_act_swing = yes }} }} }}
	if = {{ limit = {{ {R}_can_credit = yes }} random_list = {{ 80 = {{ }} 20 = {{ {R}_act_credit = yes }} }} }}
	if = {{ limit = {{ {R}_can_transit = yes }} {R}_act_transit = yes }}
	if = {{ limit = {{ {R}_can_alert_down = yes check_variable = {{ cwgg_stufe < 4 }} }} {R}_act_alert_down = yes }}
}}
"""


def actions_effects():
    out = ["\n# ---------------------------------------------------------------- Bonn's actions (window buttons)"]
    for a in ACTIONS:
        pre = []
        if a["init"]:
            pre.append(f"add_to_variable = {{ cwgg_init_brd = -{a['init']} }}")
        if a["pp"]:
            pre.append(f"add_political_power = -{a['pp']}")
        if a["cd"]:
            pre.append(f"set_country_flag = {{ flag = cwgg_cd_{a['key']} days = {a['cd']} value = 1 }}")
        if a["once"]:
            pre.append(f"set_country_flag = cwgg_done_{a['key']}")
        body = J(*pre, a["eff"], f"{R}_gui_refresh = yes")
        out.append(f"{R}_act_{a['key']} = {{\n{fmt(hide_vars_local(body), 1)}\n}}")
    for k, name, _d in CHANNELS:
        out.append(f"""{R}_open_{k} = {{
	add_to_variable = {{ cwgg_init_brd = -1 }}
	set_variable = {{ cwgg_kanal_{k} = 1 }}
	{log(f"open_{k}", f"Channel opened: {name}.")}
	{R}_gui_refresh = yes
}}
{R}_close_{k} = {{
	set_variable = {{ cwgg_kanal_{k} = 0 }}
	{kl(-3, False)}
	{log(f"close_{k}", f"Bonn closes the channel {name}. East Berlin takes note.")}
	{R}_gui_refresh = yes
}}""")
    return "\n\n".join(out) + "\n"


# ------------------------------------------------------------------ crises
def crisis_effects():
    starts = []
    for c in CRISES:
        cid, key, name, si, best, mx, lev, pic, special = c
        kw = "if" if cid == 1 else "else_if"
        starts.append(f"\t{kw} = {{ limit = {{ check_variable = {{ cwgg_t_typ = {cid} }} }} set_variable = {{ cwgg_krise_int = {si} }} set_variable = {{ cwgg_krise_max = {mx} }} country_event = {{ id = {EVR}.{100 + cid} days = 1 }} }}")
    cells = []
    first = True
    for h, row in MATRIX.items():
        for a, di in row.items():
            kw = "if" if first else "else_if"
            first = False
            cells.append(f"\t{kw} = {{ limit = {{ check_variable = {{ cwgg_h = {h} }} check_variable = {{ cwgg_a = {a} }} }} set_temp_variable = {{ cwgg_d_int = {di} }} }}")
    best = "\n".join(f"\tif = {{ limit = {{ check_variable = {{ cwgg_krise_typ = {c[0]} }} check_variable = {{ cwgg_h = {c[4]} }} }} add_to_temp_variable = {{ cwgg_d_int = -10 }} }}" for c in CRISES)
    levsel = "\n".join(f"\tif = {{ limit = {{ check_variable = {{ cwgg_krise_typ = {c[0]} }} }} set_temp_variable = {{ cwgg_t_lev = cwgg_hebel_{c[6]} }} }}" for c in CRISES)
    stance_cost = "\n".join(
        f"\t{'if' if s[0] == 1 else 'else_if'} = {{ limit = {{ check_variable = {{ cwgg_h = {s[0]} }} }} "
        + (f"if = {{ limit = {{ {R}_can_stance_{s[1]} = yes }} " + (f"add_to_variable = {{ cwgg_init_brd = -{s[3]} }} " if s[3] else "")
           + (f"add_political_power = -{s[4]} " if s[4] else "") + "} else = { set_temp_variable = { cwgg_h = 1 } } }" if s[0] != 1 else "}")
        for s in STANCES)
    return f"""
# ---------------------------------------------------------------- crises
# Starts a crisis of type temp cwgg_t_typ unless one is running.
{R}_start_crisis = {{
	if = {{ limit = {{ check_variable = {{ cwgg_krise_typ = 0 }} country_exists = DDR NOT = {{ has_global_flag = {P}_unity_achieved }} }}
		set_variable = {{ cwgg_krise_typ = cwgg_t_typ }}
		set_variable = {{ cwgg_krise_runde = 0 }}
		set_variable = {{ cwgg_krise_monat = 0 }}
		set_variable = {{ cwgg_haltung = 1 }}
		set_variable = {{ cwgg_ddr_wahl = 0 }}
		set_variable = {{ cwgg_last_h = 0 }}
		set_variable = {{ cwgg_last_a = 0 }}
		set_variable = {{ cwgg_special_used = 0 }}
		add_to_variable = {{ cwgg_crises_total = 1 }}
{chr(10).join(starts)}
		add_to_variable = {{ cwgg_druck = 10 }}
		clamp_variable = {{ var = cwgg_druck min = 0 max = 100 }}
		{R}_ask_east_berlin = yes
		{R}_update_stage = yes
		{R}_gui_refresh = yes
	}}
}}

# A human East Berlin chooses its course for the coming round by event.
{R}_ask_east_berlin = {{
	if = {{ limit = {{ country_exists = DDR DDR = {{ is_ai = no }} }}
		DDR = {{ country_event = {{ id = {EVR}.200 days = 1 }} }}
	}}
}}

# Monthly: a round is resolved every six months; a countdown advances every month.
{R}_crisis_clock = {{
	if = {{ limit = {{ check_variable = {{ cwgg_krise_typ > 0 }} }}
		if = {{ limit = {{ check_variable = {{ cwgg_countdown > 0 }} }}
			{R}_countdown_step = yes
		}}
		else = {{
			add_to_variable = {{ cwgg_krise_monat = 1 }}
			if = {{ limit = {{ check_variable = {{ cwgg_krise_monat > 5 }} }}
				set_variable = {{ cwgg_krise_monat = 0 }}
				{R}_round = yes
			}}
		}}
	}}
}}

# Monthly chance of a new crisis: 1 % plus more for a bad climate and high pressure.
{R}_crisis_roll = {{
	if = {{ limit = {{ check_variable = {{ cwgg_krise_typ = 0 }} NOT = {{ has_country_flag = cwgg_crisis_cd }} DDR = {{ check_variable = {{ cwddr_wende_stage < 3 }} }} }}
		random_list = {{
			1000 = {{ }}
			18 = {{
				modifier = {{ add = 15 check_variable = {{ cwgg_klima < -10 }} }}
				modifier = {{ add = 15 check_variable = {{ cwgg_klima < -25 }} }}
				modifier = {{ add = 15 check_variable = {{ cwgg_klima < -40 }} }}
				modifier = {{ add = 15 check_variable = {{ cwgg_klima < -60 }} }}
				modifier = {{ add = 15 check_variable = {{ cwgg_druck > 20 }} }}
				modifier = {{ add = 25 check_variable = {{ cwgg_druck > 45 }} }}
				modifier = {{ add = 20 has_country_flag = cwgg_escape_helpers }}
				modifier = {{ add = 25 OR = {{ check_variable = {{ cwgg_aufm_brd > 1 }} check_variable = {{ cwgg_aufm_ddr > 1 }} }} }}
				modifier = {{ factor = 0.5 check_variable = {{ cwgg_klima > 30 }} }}
				{R}_pick_crisis = yes
			}}
		}}
	}}
	# a frozen crisis flares up again
	if = {{ limit = {{ check_variable = {{ cwgg_krise_typ = 0 }} check_variable = {{ cwgg_relapse_typ > 0 }} NOT = {{ has_country_flag = cwgg_relapse }} }}
		set_temp_variable = {{ cwgg_t_typ = cwgg_relapse_typ }}
		set_variable = {{ cwgg_relapse_typ = 0 }}
		{R}_start_crisis = yes
		{log("relapse", "The frozen crisis flares up again.")}
	}}
	# crises with fixed causes
	if = {{ limit = {{ check_variable = {{ cwgg_krise_typ = 0 }} has_country_flag = {P}_double_track NOT = {{ has_country_flag = cwgg_missiles_done }} }}
		set_country_flag = cwgg_missiles_done
		set_temp_variable = {{ cwgg_t_typ = 6 }} {R}_start_crisis = yes
	}}
	if = {{ limit = {{ check_variable = {{ cwgg_krise_typ = 0 }} has_global_flag = mdcw_cw_initialized check_variable = {{ global.mdcw_cw_tension > 79 }} date > 1975.1.1 NOT = {{ has_country_flag = cwgg_manoeuvre_cd }} }}
		set_country_flag = {{ flag = cwgg_manoeuvre_cd days = 3650 value = 1 }}
		set_temp_variable = {{ cwgg_t_typ = 7 }} {R}_start_crisis = yes
	}}
	if = {{ limit = {{ check_variable = {{ cwgg_krise_typ = 0 }} DDR = {{ check_variable = {{ cwddr_wende_stage > 0 }} check_variable = {{ cwddr_wende_stage < 3 }} }} NOT = {{ has_country_flag = cwgg_embassy_done }} }}
		set_country_flag = cwgg_embassy_done
		set_temp_variable = {{ cwgg_t_typ = 4 }} {R}_start_crisis = yes
	}}
	if = {{ limit = {{ check_variable = {{ cwgg_krise_typ = 0 }} DDR = {{ check_variable = {{ cwddr_wende_stage = 9 }} check_variable = {{ cwddr_crisis > 74 }} }} NOT = {{ has_country_flag = cwgg_uprising_done }} }}
		set_country_flag = cwgg_uprising_done
		set_temp_variable = {{ cwgg_t_typ = 10 }} {R}_start_crisis = yes
	}}
}}

{R}_pick_crisis = {{
	random_list = {{
		20 = {{ modifier = {{ factor = 0.15 check_variable = {{ cwgg_vertrag_2 = 1 }} }} modifier = {{ factor = 2 check_variable = {{ cwgg_dhebel_transit > 1 }} }} set_temp_variable = {{ cwgg_t_typ = 1 }} }}
		20 = {{ modifier = {{ factor = 1.5 check_variable = {{ cwgg_dhebel_grenze > 2 }} }} modifier = {{ factor = 2 has_country_flag = cwgg_escape_helpers }} set_temp_variable = {{ cwgg_t_typ = 2 }} }}
		10 = {{ modifier = {{ factor = 2 check_variable = {{ cwger_stasi_penetration > 50 }} }} set_temp_variable = {{ cwgg_t_typ = 3 }} }}
		8 = {{ modifier = {{ factor = 0 check_variable = {{ cwgg_vertrag_3 = 1 }} }} modifier = {{ factor = 0 check_variable = {{ cwgg_hebel_recht < 2 }} }} set_temp_variable = {{ cwgg_t_typ = 5 }} }}
		10 = {{ modifier = {{ factor = 0 date < 1976.1.1 }} modifier = {{ factor = 0 date > 1989.12.31 }} set_temp_variable = {{ cwgg_t_typ = 8 }} }}
		8 = {{ modifier = {{ factor = 0 date > 1989.12.31 }} set_temp_variable = {{ cwgg_t_typ = 9 }} }}
	}}
	{R}_start_crisis = yes
}}

# One round of a crisis (every six months). Bonn's course is cwgg_haltung, East Berlin's is chosen now
# (by its AI, or by the human player through event {EVR}.200).
{R}_round = {{
	if = {{ limit = {{ check_variable = {{ cwgg_krise_typ > 0 }} check_variable = {{ cwgg_countdown = 0 }} }}
		if = {{ limit = {{ is_ai = yes }} {R}_bonn_stance_ai = yes }}
		set_temp_variable = {{ cwgg_h = cwgg_haltung }}
{stance_cost}
		{R}_ddr_answer = yes
		set_temp_variable = {{ cwgg_d_int = 0 }}
{chr(10).join(cells)}
		# the right answer for this kind of crisis
{best}
		# counter-pressure is only as strong as the lever behind it
		if = {{ limit = {{ check_variable = {{ cwgg_h = 4 }} }}
			set_temp_variable = {{ cwgg_t_lev = 0 }}
{levsel}
			if = {{ limit = {{ check_variable = {{ cwgg_t_lev = 0 }} }} add_to_temp_variable = {{ cwgg_d_int = 8 }} }}
			if = {{ limit = {{ check_variable = {{ cwgg_t_lev > 1 }} check_variable = {{ cwgg_a = 1 }} }} add_to_temp_variable = {{ cwgg_d_int = -5 }} }}
		}}
		# the alliance lever adds weight when the Allies are called
		if = {{ limit = {{ check_variable = {{ cwgg_h = 5 }} check_variable = {{ cwgg_hebel_allianz > 1 }} }} add_to_temp_variable = {{ cwgg_d_int = -8 }} }}
		if = {{ limit = {{ check_variable = {{ cwgg_h = 5 }} check_variable = {{ cwgg_a = 4 }} }}
			set_country_flag = {{ flag = cwgg_superpower days = 365 value = 1 }}
			if = {{ limit = {{ has_global_flag = mdcw_cw_initialized }} set_temp_variable = {{ mdcw_cw_tension_delta = 3 }} mdcw_cw_add_tension = yes }}
			{log("superpower", "Washington and Moscow take over the crisis.")}
		}}
		# the secret channel: halved through a strained line, and the Stasi may be listening
		if = {{ limit = {{ check_variable = {{ cwgg_h = 6 }} }}
			set_temp_variable = {{ cwgg_t_good = 0 }}
			{" ".join(f"if = {{ limit = {{ check_variable = {{ cwgg_kanal_{k} = 1 }} }} set_temp_variable = {{ cwgg_t_good = 1 }} }}" for k, _, _ in CHANNELS)}
			if = {{ limit = {{ check_variable = {{ cwgg_t_good = 0 }} }} multiply_temp_variable = {{ cwgg_d_int = 0.5 }} }}
			random_list = {{
				90 = {{ }}
				4 = {{
					modifier = {{ add = 4 check_variable = {{ cwger_stasi_penetration > 40 }} }}
					modifier = {{ add = 6 check_variable = {{ cwger_stasi_penetration > 65 }} }}
					modifier = {{ factor = 0.5 check_variable = {{ cwger_counterintel > 60 }} }}
					add_to_temp_variable = {{ cwgg_d_int = 15 }}
					{log("leak_secret", "The secret talks are leaked to Neues Deutschland.")}
				}}
			}}
		}}
		# Moscow's guarantee hardens East Berlin's escalation
		if = {{ limit = {{ OR = {{ check_variable = {{ cwgg_a = 3 }} check_variable = {{ cwgg_a = 4 }} }} }}
			set_temp_variable = {{ cwgg_t = DDR.cwddr_moscow_backing }}
			subtract_from_temp_variable = {{ cwgg_t = 50 }}
			divide_temp_variable = {{ cwgg_t = 7 }}
			add_to_temp_variable = {{ cwgg_d_int = cwgg_t }}
		}}
		# deterrence: readiness and exercises blunt escalation
		if = {{ limit = {{ check_variable = {{ cwgg_a = 3 }} OR = {{ check_variable = {{ cwgg_mob_brd > 1 }} has_country_flag = cwgg_manoeuvre }} }} add_to_temp_variable = {{ cwgg_d_int = -8 }} }}
		if = {{ limit = {{ check_variable = {{ cwgg_a = 3 }} check_variable = {{ cwgg_mob_brd > 2 }} }} add_to_temp_variable = {{ cwgg_d_int = -8 }} }}
		# an AI East Berlin mobilises when it escalates hard with Soviet backing, or when Bonn mobilises against Moscow
		if = {{ limit = {{ DDR = {{ is_ai = yes }} OR = {{ AND = {{ check_variable = {{ cwgg_a = 3 }} check_variable = {{ cwgg_krise_int > 59 }} DDR = {{ check_variable = {{ cwddr_moscow_backing > 59 }} }} }} AND = {{ check_variable = {{ cwgg_h = 7 }} check_variable = {{ cwgg_a = 4 }} }} }} check_variable = {{ cwgg_mob_ddr < 3 }} }}
			add_to_variable = {{ cwgg_mob_ddr = 1 }}
			{log("ddr_alert", "The National People's Army raises its alert level.")}
		}}
		if = {{ limit = {{ check_variable = {{ cwgg_h = 7 }} check_variable = {{ cwgg_mob_brd < 3 }} }} add_to_variable = {{ cwgg_mob_brd = 1 }} }}
		# apply
		add_to_variable = {{ cwgg_krise_int = cwgg_d_int }}
		clamp_variable = {{ var = cwgg_krise_int min = 0 max = 100 }}
		if = {{ limit = {{ check_variable = {{ cwgg_d_int > 0 }} }}
			set_temp_variable = {{ cwgg_t = cwgg_d_int }}
			divide_temp_variable = {{ cwgg_t = 2 }}
			add_to_variable = {{ cwgg_druck = cwgg_t }}
			divide_temp_variable = {{ cwgg_t = 2.5 }}
			subtract_from_variable = {{ cwgg_klima = cwgg_t }}
		}}
		if = {{ limit = {{ check_variable = {{ cwgg_d_int < 0 }} }}
			set_temp_variable = {{ cwgg_t = cwgg_d_int }}
			divide_temp_variable = {{ cwgg_t = -10 }}
			add_to_variable = {{ cwgg_klima = cwgg_t }}
		}}
		clamp_variable = {{ var = cwgg_druck min = 0 max = 100 }}
		clamp_variable = {{ var = cwgg_klima min = -100 max = 100 }}
		set_variable = {{ cwgg_last_h = cwgg_h }}
		set_variable = {{ cwgg_last_a = cwgg_a }}
		set_variable = {{ cwgg_last_dint = cwgg_d_int }}
		add_to_variable = {{ cwgg_krise_runde = 1 }}
		set_variable = {{ cwgg_haltung = 1 }}
		set_temp_variable = {{ cwgg_t_log = 900 }}
		add_to_temp_variable = {{ cwgg_t_log = cwgg_a }}
		{R}_log = yes
		# counter-offers can be taken up when Bonn was talking anyway
		if = {{ limit = {{ check_variable = {{ cwgg_a = 5 }} OR = {{ check_variable = {{ cwgg_h = 2 }} check_variable = {{ cwgg_h = 6 }} }} }}
			country_event = {{ id = {EVR}.20 days = 1 }}
		}}
		{R}_update_stage = yes
		if = {{ limit = {{ check_variable = {{ cwgg_krise_int < 1 }} }}
			{R}_settle_crisis = yes
		}}
		else_if = {{ limit = {{ check_variable = {{ cwgg_krise_int > 99 }} }}
			country_event = {{ id = {EVR}.11 days = 1 }}
		}}
		else_if = {{ limit = {{ check_variable = {{ cwgg_krise_runde > cwgg_krise_max }} }}
			# exhausted: below 50 the sides settle, above it the crisis freezes
			if = {{ limit = {{ check_variable = {{ cwgg_krise_int < 50 }} }} {R}_settle_crisis = yes }}
			else = {{ set_temp_variable = {{ cwgg_t_out = 3 }} {R}_end_crisis = yes }}
		}}
		else = {{
			{R}_ask_east_berlin = yes
			if = {{ limit = {{ is_ai = no NOT = {{ has_country_flag = cwgg_quiet }} }} country_event = {{ id = {EVR}.3 }} }}
		}}
		{R}_gui_refresh = yes
	}}
}}

# Who gave way decides the outcome of a settled crisis.
{R}_settle_crisis = {{
	if = {{ limit = {{ check_variable = {{ cwgg_last_a = 1 }} NOT = {{ check_variable = {{ cwgg_last_h = 2 }} }} }} set_temp_variable = {{ cwgg_t_out = 1 }} }}
	else_if = {{ limit = {{ check_variable = {{ cwgg_last_h = 2 }} NOT = {{ check_variable = {{ cwgg_last_a = 1 }} }} NOT = {{ check_variable = {{ cwgg_last_a = 2 }} }} }} set_temp_variable = {{ cwgg_t_out = 2 }} }}
	else = {{ set_temp_variable = {{ cwgg_t_out = 7 }} }}
	{R}_end_crisis = yes
}}

# East Berlin's answer: the human player's choice, or the AI weighted by the SED leader,
# money, Moscow and the balance of force.
{R}_ddr_answer = {{
	set_temp_variable = {{ cwgg_a = 2 }}
	if = {{ limit = {{ country_exists = DDR DDR = {{ is_ai = no }} }}
		if = {{ limit = {{ check_variable = {{ cwgg_ddr_wahl > 0 }} }} set_temp_variable = {{ cwgg_a = cwgg_ddr_wahl }} }}
		if = {{ limit = {{ check_variable = {{ cwgg_a > 2 }} check_variable = {{ cwgg_init_ddr < 1 }} }} set_temp_variable = {{ cwgg_a = 2 }} }}
	}}
	else = {{
		random_list = {{
			10 = {{
				modifier = {{ factor = 3 DDR = {{ check_variable = {{ cwddr_leader > 2 }} }} }}
				modifier = {{ factor = 1.5 DDR = {{ check_variable = {{ cwddr_moscow_backing < 40 }} }} }}
				modifier = {{ factor = 2 DDR = {{ check_variable = {{ cwddr_sed_control < 40 }} }} }}
				modifier = {{ factor = 0.5 DDR = {{ check_variable = {{ cwddr_leader = 0 }} }} }}
				set_temp_variable = {{ cwgg_a = 1 }}
			}}
			30 = {{
				modifier = {{ factor = 1.5 DDR = {{ OR = {{ check_variable = {{ cwddr_leader = 1 }} check_variable = {{ cwddr_leader = 2 }} }} }} }}
				set_temp_variable = {{ cwgg_a = 2 }}
			}}
			20 = {{
				modifier = {{ factor = 0 check_variable = {{ cwgg_init_ddr < 1 }} }}
				modifier = {{ factor = 1.5 DDR = {{ check_variable = {{ cwddr_leader = 0 }} }} }}
				modifier = {{ factor = 0.3 DDR = {{ check_variable = {{ cwddr_leader > 2 }} }} }}
				modifier = {{ factor = 1.5 DDR = {{ check_variable = {{ cwddr_moscow_backing > 69 }} }} }}
				modifier = {{ factor = 0.5 DDR = {{ check_variable = {{ cwddr_moscow_backing < 40 }} }} }}
				modifier = {{ factor = 0.6 check_variable = {{ cwgg_mob_brd > 1 }} }}
				modifier = {{ factor = 0.5 check_variable = {{ cwgg_mob_brd > 2 }} }}
				modifier = {{ factor = 1.3 {R}_hardline_moscow = yes }}
				set_temp_variable = {{ cwgg_a = 3 }}
			}}
			10 = {{
				modifier = {{ factor = 0 check_variable = {{ cwgg_init_ddr < 1 }} }}
				modifier = {{ factor = 0 NOT = {{ country_exists = SOV }} }}
				modifier = {{ factor = 1.5 DDR = {{ check_variable = {{ cwddr_moscow_backing > 69 }} }} }}
				modifier = {{ factor = 0.3 DDR = {{ check_variable = {{ cwddr_moscow_backing < 40 }} }} }}
				modifier = {{ factor = 0.3 DDR = {{ check_variable = {{ cwddr_leader > 2 }} }} }}
				modifier = {{ factor = 2 check_variable = {{ cwgg_last_h = 5 }} }}
				set_temp_variable = {{ cwgg_a = 4 }}
			}}
			10 = {{
				modifier = {{ factor = 0 check_variable = {{ cwgg_init_ddr < 1 }} }}
				modifier = {{ factor = 2 DDR = {{ check_variable = {{ cwddr_hard_currency > 60 }} }} }}
				modifier = {{ factor = 2 DDR = {{ check_variable = {{ cwddr_leader = 1 }} }} date > 1980.12.31 }}
				modifier = {{ factor = 2 DDR = {{ check_variable = {{ cwddr_leader > 2 }} }} }}
				modifier = {{ factor = 0.5 DDR = {{ check_variable = {{ cwddr_leader = 0 }} }} }}
				set_temp_variable = {{ cwgg_a = 5 }}
			}}
		}}
	}}
	set_variable = {{ cwgg_ddr_wahl = 0 }}
	if = {{ limit = {{ check_variable = {{ cwgg_a > 2 }} }} add_to_variable = {{ cwgg_init_ddr = -1 }} }}
	clamp_variable = {{ var = cwgg_init_ddr min = 0 max = 6 }}
}}

# Bonn as AI picks a stance in character with the government.
{R}_bonn_stance_ai = {{
	random_list = {{
		10 = {{ set_variable = {{ cwgg_haltung = 1 }} }}
		25 = {{ modifier = {{ factor = 2 check_variable = {{ ruling_party = 3 }} }} modifier = {{ factor = 0 NOT = {{ {R}_can_stance_deescalate = yes }} }} set_variable = {{ cwgg_haltung = 2 }} }}
		25 = {{ modifier = {{ factor = 2 check_variable = {{ ruling_party = 1 }} }} modifier = {{ factor = 0 NOT = {{ {R}_can_stance_firm = yes }} }} set_variable = {{ cwgg_haltung = 3 }} }}
		10 = {{ modifier = {{ factor = 0 NOT = {{ {R}_can_stance_pressure = yes }} }} set_variable = {{ cwgg_haltung = 4 }} }}
		15 = {{ modifier = {{ factor = 0 NOT = {{ {R}_can_stance_allies = yes }} }} set_variable = {{ cwgg_haltung = 5 }} }}
		25 = {{ modifier = {{ factor = 0 NOT = {{ {R}_can_stance_secret = yes }} }} set_variable = {{ cwgg_haltung = 6 }} }}
	}}
}}

# Ends the crisis with outcome temp cwgg_t_out: 1 Bonn has its way, 2 East Berlin has its way, 3 frozen,
# 4 Bonn gives way at the brink, 5 East Berlin gives way at the brink, 6 Moscow reins East Berlin in, 7 compromise.
{R}_end_crisis = {{
	set_variable = {{ cwgg_last_out = cwgg_t_out }}
	set_variable = {{ cwgg_last_typ = cwgg_krise_typ }}
	if = {{ limit = {{ OR = {{ check_variable = {{ cwgg_t_out = 1 }} check_variable = {{ cwgg_t_out = 5 }} check_variable = {{ cwgg_t_out = 6 }} }} }}
		add_to_variable = {{ cwgg_crises_won = 1 }}
		add_stability = 0.02
		DDR = {{ {dv_self("cwddr_sed_control", -3, show=False)} {dv_self("cwddr_recognition", -2, show=False)} add_stability = -0.02 }}
		{log("won", "Bonn comes out of the crisis stronger.")}
	}}
	if = {{ limit = {{ OR = {{ check_variable = {{ cwgg_t_out = 2 }} check_variable = {{ cwgg_t_out = 4 }} }} }}
		add_to_variable = {{ cwgg_crises_lost = 1 }}
		add_stability = -0.02
		DDR = {{ {dv_self("cwddr_sed_control", 3, show=False)} {dv_self("cwddr_recognition", 4, show=False)} add_stability = 0.02 }}
		{log("lost", "East Berlin has had its way. The opposition attacks the government.")}
	}}
	if = {{ limit = {{ check_variable = {{ cwgg_t_out = 7 }} }}
		{kl(5, False)}
		{log("compromise", "The crisis ends in a compromise both sides can sell at home.")}
	}}
	if = {{ limit = {{ check_variable = {{ cwgg_t_out = 3 }} }}
		{kl(-5, False)}
		{dr(10, False)}
		{log("stalemate", "The crisis freezes without a result.")}
		random_list = {{ 50 = {{ }} 50 = {{ set_country_flag = {{ flag = cwgg_relapse days = 180 value = 1 }} set_variable = {{ cwgg_relapse_typ = cwgg_krise_typ }} }} }}
	}}
	if = {{ limit = {{ check_variable = {{ cwgg_t_out = 5 }} }} {kl(-10, False)} }}
	if = {{ limit = {{ check_variable = {{ cwgg_t_out = 4 }} }} {kl(10, False)} }}
	set_variable = {{ cwgg_krise_typ = 0 }}
	set_variable = {{ cwgg_krise_int = 0 }}
	set_variable = {{ cwgg_countdown = 0 }}
	set_variable = {{ cwgg_haltung = 1 }}
	set_country_flag = {{ flag = cwgg_crisis_cd days = 365 value = 1 }}
	clamp_variable = {{ var = cwgg_klima min = -100 max = 100 }}
	country_event = {{ id = {EVR}.10 days = 1 }}
	if = {{ limit = {{ country_exists = DDR DDR = {{ is_ai = no }} }} DDR = {{ country_event = {{ id = {EVR}.201 days = 1 }} }} }}
	{R}_update_stage = yes
	{R}_gui_refresh = yes
}}

# Choose a stance from the window (temp cwgg_t_h).
{R}_set_stance = {{
	set_variable = {{ cwgg_haltung = cwgg_t_h }}
	{R}_gui_refresh = yes
}}
"""


def special_effects():
    """One special action per crisis type, usable once per crisis."""
    sp = {
        1: (J(money_gdp(-0.001), "add_to_variable = { cwgg_krise_int = -25 }", tension(1),
              log("sp_airlift", "Bonn and the Allies prepare an airlift. East Berlin reconsiders.")),
            "check_variable = { cwgg_hebel_allianz > 0 }", "Costs money. Crisis intensity §G-25§!, Cold War world tension §R+1§!."),
        2: (J("add_to_variable = { cwgg_krise_int = -10 }", kl(-3), dv("cwddr_recognition", -4),
              log("sp_un", "Bonn raises the shootings at the border before the UN Commission on Human Rights.")),
            "check_variable = { cwgg_vertrag_4 = 1 }", "Needs UN membership. Intensity §G-10§!, GDR recognition §G-4§!, climate §R-3§!."),
        3: ("add_to_variable = { cwgg_krise_int = -30 }\n" + log("sp_exchange", "Agents are exchanged on the Glienicke Bridge at dawn."),
            "check_variable = { cwgg_kanal_vogel = 1 }", "Needs the Vogel channel. Intensity §G-30§!."),
        4: (J(money_gdp(-0.0008), "add_to_variable = { cwgg_krise_int = -35 }", dv("cwddr_exit_pressure", 6),
              log("sp_trains", "Special trains carry the embassy refugees west - through the GDR.")),
            "check_variable = { cwgg_init_brd > 0 }", "Costs money. Intensity §G-35§!, GDR exit pressure §R+6§!."),
        5: (J("add_to_variable = { cwgg_krise_int = -20 }", kl(-5), dv("cwddr_recognition", -3),
              log("sp_hallstein", "Bonn breaks off relations with a state that recognised the GDR.")),
            "NOT = { check_variable = { cwgg_vertrag_3 = 1 } }", "Intensity §G-20§!, climate §R-5§!. Only before the Basic Treaty."),
        6: (J("add_to_variable = { cwgg_krise_int = -25 }", "set_country_flag = cwgg_zero_option", tension(-3), v("cwger_peace_movement", -6),
              log("sp_zero", "Bonn backs the zero option: no Pershings if there are no SS-20s.")),
            "has_idea = NATO_member", "Needs NATO membership. Intensity §G-25§!, peace movement §G-6§!, a permanently better climate base."),
        7: (J("add_to_variable = { cwgg_krise_int = -30 }", ws(-0.02),
              log("sp_cancel", "NATO scales back the exercise. Moscow stands its forces down.")),
            "always = yes", "Intensity §G-30§!, war support §R-2%§!."),
        8: (J("add_to_variable = { cwgg_krise_int = -15 }", dv("cwddr_opposition", 3),
              log("sp_asylum", "The dissidents are given a home in the West - and a microphone.")),
            "always = yes", "Intensity §G-15§!, GDR opposition §Y+3§!."),
        9: ("add_to_variable = { cwgg_krise_int = -20 }\n" + kl(3) + "\n" + log("sp_commission", "A joint border commission takes up the Elbe question."),
            "check_variable = { cwgg_vertrag_3 = 1 }", "Needs the Basic Treaty. Intensity §G-20§!, climate §G+3§!."),
        10: (f"country_event = {{ id = {EVR}.18 days = 1 }}", "has_country_flag = cwgg_unlock_brotherly_help",
             "Needs the focus §YThe Liberation Doctrine§!. Opens the path to war."),
    }
    out = ["\n# ---------------------------------------------------------------- special actions in a crisis"]
    trig = ["\n"]
    for cid, (eff, cond, _tt) in sp.items():
        out.append(f"{R}_special_{cid} = {{\n\tset_variable = {{ cwgg_special_used = 1 }}\n\tclamp_variable = {{ var = cwgg_krise_int min = 0 max = 100 }}\n{fmt(hide_vars_local(eff), 1)}\n\tclamp_variable = {{ var = cwgg_krise_int min = 0 max = 100 }}\n\t{R}_gui_refresh = yes\n}}")
        trig.append(f"{R}_can_special_{cid} = {{\n\tcheck_variable = {{ cwgg_krise_typ = {cid} }}\n\tcheck_variable = {{ cwgg_special_used = 0 }}\n\tcheck_variable = {{ cwgg_countdown = 0 }}\n\t{cond}\n}}\n")
        L(f"cwgg_special_tt_{cid}", _tt)
    return "\n\n".join(out) + "\n", "\n".join(trig)


def war_effects():
    return f"""
# ---------------------------------------------------------------- the brink and war
# Countdown after 'Show resolve' at the peak of a crisis: three monthly steps, driven by the monthly tick.
# A human East Berlin decides itself (event {EVR}.210); an AI East Berlin may blink.
{R}_countdown_step = {{
	if = {{ limit = {{ check_variable = {{ cwgg_countdown > 0 }} check_variable = {{ cwgg_krise_typ > 0 }} }}
		add_to_variable = {{ cwgg_countdown = -1 }}
		if = {{ limit = {{ DDR = {{ is_ai = yes }} }}
			random_list = {{
				70 = {{
					modifier = {{ factor = 1.3 DDR = {{ check_variable = {{ cwddr_moscow_backing > 69 }} }} }}
					modifier = {{ factor = 1.5 {R}_hardline_moscow = yes }}
					modifier = {{ factor = 0.7 check_variable = {{ cwgg_mob_brd > 2 }} }}
					modifier = {{ factor = 1.2 check_variable = {{ cwgg_mob_ddr > 2 }} }}
				}}
				30 = {{
					modifier = {{ factor = 1.5 DDR = {{ check_variable = {{ cwddr_moscow_backing < 50 }} }} }}
					modifier = {{ factor = 1.5 DDR = {{ check_variable = {{ cwddr_leader > 0 }} }} date > 1980.12.31 }}
					modifier = {{ factor = 3 DDR = {{ check_variable = {{ cwddr_leader > 2 }} }} }}
					set_variable = {{ cwgg_countdown = 0 }}
					set_country_flag = {{ flag = cwgg_east_blinked days = 30 value = 1 }}
					country_event = {{ id = {EVR}.14 days = 1 }}
				}}
			}}
		}}
		if = {{ limit = {{ check_variable = {{ cwgg_countdown > 0 }} }}
			country_event = {{ id = {EVR}.15 days = 1 }}
			if = {{ limit = {{ DDR = {{ is_ai = no }} }} DDR = {{ country_event = {{ id = {EVR}.210 days = 1 }} }} }}
		}}
		else_if = {{ limit = {{ check_variable = {{ cwgg_krise_typ > 0 }} NOT = {{ has_country_flag = cwgg_east_blinked }} }}
			{R}_final_resolution = yes
		}}
		{R}_gui_refresh = yes
	}}
}}

# The countdown has run out and nobody gave way. Only a human may order the attack on West Berlin:
# Bonn's signed strike order, a human East Berlin (event {EVR}.211) or, for an AI East Berlin,
# a human Soviet Union (event {EVR}.212). Otherwise Moscow always reins East Berlin in.
{R}_final_resolution = {{
	if = {{ limit = {{ has_country_flag = cwgg_strike_ordered }}
		clr_country_flag = cwgg_strike_ordered
		set_temp_variable = {{ cwgg_t_path = 1 }}
		{R}_war_start = yes
	}}
	else_if = {{ limit = {{ DDR = {{ is_ai = no }} }}
		DDR = {{ country_event = {{ id = {EVR}.211 days = 1 }} }}
	}}
	else_if = {{ limit = {{ country_exists = SOV SOV = {{ is_ai = no }} }}
		SOV = {{ country_event = {{ id = {EVR}.212 days = 1 }} }}
	}}
	else = {{
		set_temp_variable = {{ cwgg_t_out = 6 }}
		{R}_end_crisis = yes
	}}
}}

# War: temp cwgg_t_path 1 Bonn strikes first, 2 East Berlin attacks, 3 brotherly help for an uprising, 4 false alarm.
{R}_war_start = {{
	set_variable = {{ cwgg_stufe = 6 }}
	set_variable = {{ cwgg_war_path = cwgg_t_path }}
	set_country_flag = cwgg_war_active
	set_global_flag = cwgg_german_war
	set_variable = {{ cwgg_countdown = 0 }}
	set_variable = {{ cwgg_krise_typ = 0 }}
	set_variable = {{ cwgg_krise_int = 0 }}
	set_variable = {{ cwgg_klima = -100 }}
	set_variable = {{ cwgg_mob_brd = 3 }}
	set_variable = {{ cwgg_mob_ddr = 3 }}
	if = {{ limit = {{ has_global_flag = mdcw_cw_initialized }}
		set_temp_variable = {{ mdcw_cw_tension_delta = 100 }}
		mdcw_cw_add_tension = yes
	}}
	{log("war", "War between the two German states.")}
	if = {{ limit = {{ OR = {{ check_variable = {{ cwgg_t_path = 1 }} check_variable = {{ cwgg_t_path = 3 }} }} }}
		# an AI GDR without Moscow's guarantee leaves the Warsaw Pact faction; a human GDR decides that itself
		if = {{ limit = {{ DDR = {{ is_ai = yes is_in_faction = yes check_variable = {{ cwddr_moscow_backing < 40 }} }} }}
			DDR = {{ leave_faction = yes }}
		}}
		declare_war_on = {{ target = DDR type = annex_everything }}
		# no automatic call to the alliance: NATO governments decide for themselves
	}}
	else = {{
		DDR = {{ declare_war_on = {{ target = GER type = take_state_focus generator = {{ 1251 }} }} }}
		# a Soviet Union that ordered the attack, or an AI one that still guarantees the GDR, joins; a human one otherwise decides itself
		if = {{ limit = {{ country_exists = SOV SOV = {{ NOT = {{ has_war_with = GER }} }}
				OR = {{ has_global_flag = cwgg_sov_ordered_attack AND = {{ SOV = {{ is_ai = yes }} DDR = {{ check_variable = {{ cwddr_moscow_backing > 39 }} }} }} }} }}
			SOV = {{ add_to_war = {{ targeted_alliance = DDR enemy = GER hostility_reason = asked_to_join }} }}
		}}
	}}
	if = {{ limit = {{ country_exists = DDR DDR = {{ is_ai = no }} }} DDR = {{ country_event = {{ id = {EVR}.230 days = 1 }} }} }}
	country_event = {{ id = {EVR}.30 days = 1 }}
	country_event = {{ id = {EVR}.31 days = 45 }}
	{R}_set_stage_modifiers = yes
	{R}_gui_refresh = yes
}}

# Watches a running crisis on the brink (false alarm, only if one side is AI) and a running war.
{R}_war_watch = {{
	# path D: a false alarm while both armies are on the highest alert and no line is open
	if = {{ limit = {{
			check_variable = {{ cwgg_stufe = 5 }} check_variable = {{ cwgg_krise_typ = 7 }}
			check_variable = {{ cwgg_mob_brd > 2 }} check_variable = {{ cwgg_mob_ddr > 2 }}
			NOT = {{ has_country_flag = cwgg_war_active }} NOT = {{ has_country_flag = cwgg_false_alarm_cd }}
		}}
		random_list = {{
			82 = {{ }}
			18 = {{
				modifier = {{ factor = 0.25 check_variable = {{ cwgg_kanal_draht = 1 }} }}
				modifier = {{ factor = 0.5 check_variable = {{ cwgg_kanal_bahr = 1 }} }}
				set_country_flag = {{ flag = cwgg_false_alarm_cd days = 180 value = 1 }}
				country_event = {{ id = {EVR}.21 days = 1 }}
			}}
		}}
	}}
	if = {{ limit = {{ has_country_flag = cwgg_war_active }}
		if = {{ limit = {{ NOT = {{ country_exists = DDR }} }}
			clr_country_flag = cwgg_war_active
			country_event = {{ id = {EVR}.40 days = 1 }}
		}}
		else_if = {{ limit = {{ DDR = {{ has_capitulated = yes }} has_war_with = DDR }}
			clr_country_flag = cwgg_war_active
			country_event = {{ id = {EVR}.40 days = 1 }}
		}}
		else_if = {{ limit = {{ has_capitulated = yes has_war_with = DDR }}
			clr_country_flag = cwgg_war_active
			country_event = {{ id = {EVR}.41 days = 1 }}
		}}
		else_if = {{ limit = {{ NOT = {{ has_war_with = DDR }} }}
			clr_country_flag = cwgg_war_active
			country_event = {{ id = {EVR}.42 days = 1 }}
		}}
	}}
}}

# Cold peace after a war or a stand-off that nobody won.
{R}_cold_peace = {{
	set_variable = {{ cwgg_stufe = 4 }}
	set_variable = {{ cwgg_klima = -60 }}
	set_variable = {{ cwgg_mob_brd = 1 }}
	set_variable = {{ cwgg_mob_ddr = 1 }}
	clr_global_flag = cwgg_german_war
	{R}_set_stage_modifiers = yes
}}
"""


def all_effects():
    sp, _ = special_effects()
    body = "\n".join([
        "## Generated by tools/west_germany_1970/compile.py. Edit the generator, not this file.\n",
        setup(), stage_effects(), monthly(), border_watch(), negotiation(), treaty_effects(), ddr_ai(), bonn_ai(), actions_effects(),
        crisis_effects(), sp, war_effects(),
    ])
    from tooltips import hide_vars
    return body


def triggers_all():
    _, sp_trig = special_effects()
    return trigger_file() + sp_trig


def dynamic_modifiers():
    return f"""
{P}_dm_inner_german = {{
	icon = GFX_idea_german_advisors
	enable = {{ always = yes }}
	stability_factor = cwgg_dm_stab
	war_support_factor = cwgg_dm_ws
	consumer_goods_factor = cwgg_dm_cg
	industrial_capacity_factory = cwgg_dm_fac
	mobilization_speed = cwgg_dm_mob
}}

{P}_dm_inner_german_ddr = {{
	icon = GFX_idea_soviet_advisors
	enable = {{ always = yes }}
	stability_factor = cwgg_dm_stab
	war_support_factor = cwgg_dm_ws
	consumer_goods_factor = cwgg_dm_cg
	mobilization_speed = cwgg_dm_mob
}}
"""


def localise():
    L(f"{P}_dm_inner_german", "Inner-German Relations")
    L(f"{P}_dm_inner_german_ddr", "Relations with the Federal Republic")
    for k, (code, text) in LOGS.items():
        L(f"cwgg_log_{code}", text)
    for a_id, key, name in ANSWERS:
        L(f"cwgg_log_{900 + a_id}", f"Crisis round: East Berlin {name.lower()}.")
    for s in STANCES:
        L(f"cwgg_stance_{s[1]}", s[2])
        L(f"cwgg_stance_{s[1]}_desc", s[5])
    for a in ANSWERS:
        L(f"cwgg_answer_{a[1]}", a[2])
    for i, (n, d) in enumerate(STAGES):
        L(f"cwgg_stage_{i}", n)
        L(f"cwgg_stage_{i}_desc", d)
    for c in CRISES:
        L(f"cwgg_crisis_{c[1]}", c[2])
        L(f"cwgg_special_{c[0]}", c[8])
    for k, n, d in LEVERS:
        L(f"cwgg_lever_{k}", n)
        L(f"cwgg_lever_{k}_desc", d)
    for k, n, d in DLEVERS:
        L(f"cwgg_dlever_{k}", n)
        L(f"cwgg_dlever_{k}_desc", d)
    for k, n, d in CHANNELS:
        L(f"cwgg_channel_{k}", n)
        L(f"cwgg_channel_{k}_desc", d)
    for t in TREATIES:
        L(f"cwgg_treaty_{t[0]}", t[2])
        L(f"cwgg_treaty_{t[0]}_desc", t[3])
        if t[7]:
            L(f"cwgg_treaty_{t[0]}_unlock", t[7])
    for a in ACTIONS:
        L(f"cwgg_act_{a['key']}", a["name"])
