"""West German events: Bonn politics, terrorism, economy, society and scandals."""
from cw_lib import *
from events_lib import E, O, gov, fire, ddr, EXTRA_EFFECTS

SPD = "check_variable = { ruling_party = 3 }"
UNION = "check_variable = { ruling_party = 1 }"
FDP_IN = "is_in_array = { gov_coalition_array = 16 }"


def ruling_party_shift(pct):
    """Popularity change for whichever of SPD/CDU leads the government."""
    return (f"if = {{ limit = {{ {SPD} }} {party('spd', pct)} }}\n"
            f"else_if = {{ limit = {{ {UNION} }} {party('cdu', pct)} }}")


def bundesrat_shift(n):
    """Länder elections move the Bundesrat against the federal government (n > 0 = toward opposition)."""
    return (f"if = {{ limit = {{ {SPD} }} {v('cwger_bundesrat_union', n, show=False)} }}\n"
            f"else = {{ {v('cwger_bundesrat_union', -n, show=False)} }}")


# ---------------------------------------------------------------- helper effects
SLOTS = {"cdu": 1, "spd": 3, "pds": 5, "fdp": 16, "greens": 17, "rep": 20, "npd": 21}
math = [f"{P}_coalition_math = {{", "set_variable = { cwger_bt_total = 0 }"]
for n, s in SLOTS.items():
    math.append(f"set_variable = {{ cwger_bt_{n} = 0 }}")
    math.append(f"if = {{ limit = {{ check_variable = {{ party_pop_elect_array^{s} > 0.0499 }} }} set_variable = {{ cwger_bt_{n} = party_pop_elect_array^{s} }} }}")
    math.append(f"add_to_variable = {{ cwger_bt_total = cwger_bt_{n} }}")
math.append("if = { limit = { check_variable = { cwger_bt_total < 0.01 } } set_variable = { cwger_bt_total = 1 } }")
for q, (a, b) in {"sl": ("spd", "fdp"), "cl": ("cdu", "fdp"), "gc": ("cdu", "spd"), "rg": ("spd", "greens")}.items():
    math.append(f"set_variable = {{ cwger_q_{q} = cwger_bt_{a} }}")
    math.append(f"add_to_variable = {{ cwger_q_{q} = cwger_bt_{b} }}")
    math.append(f"divide_variable = {{ cwger_q_{q} = cwger_bt_total }}")
math.append("}")
EXTRA_EFFECTS.append("# Bundestag shares of the possible coalitions from the last election result (parties under 5% get no seats).\n" + "\n".join(math))

EXTRA_EFFECTS.append(f"""
# Hostage exchange: the state releases prisoners and becomes blackmailable.
{P}_hostage_exchange = {{
	clr_country_flag = {P}_hostage_crisis_active
	subtract_from_variable = {{ cwger_raf_prisoners = 3 }}
	clamp_variable = {{ var = cwger_raf_prisoners min = 0 max = 40 }}
	add_to_variable = {{ cwger_raf_cadre = 6 }}
	set_country_flag = {{ flag = {P}_state_blackmailable days = 1500 value = 1 }}
}}
""")

# ======================================================================= POLITICS
E(f"{EVG}.1", "The Social-Liberal Coalition",
  "Twenty years after its founding the Federal Republic has, for the first time, a chancellor from the Social Democrats. Willy Brandt governs with Walter Scheel's Free Democrats and a majority of twelve seats - a majority that defections could erase in a single afternoon.\n\n"
  "In the East stands a second German state that Bonn does not recognise. In the universities the revolt of 1968 is splitting into reform, sects and the first underground cells. And the economic miracle is slowing down.",
  "GFX_german_parliament_bundestag",
  imm=f"{P}_assert_1969_coalition = yes\n{P}_update_bundestag = yes",
  opts=[O("Dare more democracy.", J(pp(25),
     tt(f"{P}_tt_intro", "§YSystems of the Bonn Republic§!: Bundestag seat arithmetic and constructive votes of no confidence, the FDP's course, RAF generations and the security state, Deutschlandpolitik as a balance of power with the GDR's own crisis meters, and Imperia links for oil, tension, sanctions and assistance.")))])

E(f"{EVG}.20", "Constructive Vote of No Confidence",
  "The opposition has tabled a motion under Article 67 of the Basic Law: it does not merely want to bring down the chancellor, it names a successor. The government's majority has melted to almost nothing. Whips count, recount and visit wavering deputies at home.",
  "GFX_bundestag",
  [O("Fight for every vote.", J(pp(-50), """random_list = {
	55 = {
		modifier = { add = 15 check_variable = { cwger_margin > 0 } }
		modifier = { add = 10 check_variable = { cwger_stasi_penetration > 45 } """ + SPD + """ }
		modifier = { add = -15 check_variable = { cwger_margin < -2 } }
		""" + fire(f"{EVG}.21", 2) + """
	}
	45 = {
		""" + fire(f"{EVG}.22", 2) + """
	}
}""", tt(f"{P}_tt_vote", "The vote will decide whether the government survives.")), ai=80),
   O("Ask for confidence and lose it - let the voters decide.", J(pp(-25), fire(f"{EVG}.23", 3)), ai=20)])

E(f"{EVG}.21", "The Motion Fails",
  "The opposition candidate falls two votes short. Bonn whispers that the votes were not all found by persuasion alone - years later it will turn out that the Ministry for State Security paid at least one deputy. For now, the government survives.",
  "GFX_german_parliament_bundestag",
  [O("A narrow escape.", J(stab(0.02), pp(50), "set_variable = { cwger_defectors = 0 }",
     f"if = {{ limit = {{ {SPD} check_variable = {{ cwger_stasi_penetration > 45 }} }} {v('cwger_scandal', 8)} }}",
     f"{P}_update_bundestag = yes"))])

E(f"{EVG}.22", "A New Chancellor",
  "The motion carries. Without an election, without a coalition agreement worth the name, the Federal Republic has a new head of government - the first time Article 67 has worked as its authors intended.",
  "GFX_bundestag",
  [O("The opposition takes over.", J("set_variable = { cwger_defectors = 0 }",
     f"if = {{ limit = {{ {SPD} }} if = {{ limit = {{ date < 1976.1.1 check_variable = {{ cwger_cdu_leader = 1 }} }} set_country_flag = {P}_barzel_government }} {gov(1, [16])} }}",
     f"else = {{ {gov(3, [16])} }}", stab(-0.03)))])

E(f"{EVG}.23", "The Bundestag Is Dissolved",
  "The chancellor has asked for the confidence of the house and, as arranged, not received it. The Federal President dissolves the Bundestag. The campaign begins at once.",
  "GFX_election_day",
  [O("To the voters.", J("set_variable = { cwger_defectors = 0 }",
     "if = { limit = { NOT = { has_country_flag = generic_election_killswitch } NOT = { has_country_flag = elections_in_progress } } country_event = { id = MD4_election_campaign.0 days = 1 } }"))])

E(f"{EVG}.24", "Coalition Talks",
  "The votes are counted. In Bonn nobody governs alone: the parties above the five-percent hurdle sit down to divide ministries and principles. Who governs with whom depends on arithmetic - and on where the Free Democrats think their future lies.\n\n"
  "Seat shares: social-liberal §Y[?cwger_q_sl|%0]§!, Christian-liberal §Y[?cwger_q_cl|%0]§!, grand coalition §Y[?cwger_q_gc|%0]§!, red-green §Y[?cwger_q_rg|%0]§!.",
  "GFX_german_parliament_bundestag",
  [O("Keep the coalition the parties have agreed on.", "", ai=10),
   O("A social-liberal coalition.", gov(3, [16]), trig="check_variable = { cwger_q_sl > 0.5 }",
     ai="base = 20 modifier = { factor = 3 check_variable = { cwger_fdp_course < 20 } } modifier = { factor = 0.2 check_variable = { cwger_fdp_course > 40 } }"),
   O("A Christian-liberal coalition.", gov(1, [16]), trig="check_variable = { cwger_q_cl > 0.5 }",
     ai="base = 20 modifier = { factor = 3 check_variable = { cwger_fdp_course > 20 } } modifier = { factor = 0.2 check_variable = { cwger_fdp_course < -20 } }"),
   O("A grand coalition under the Union.", J(gov(1, [3]), stab(0.02), party("npd", 0.004)),
     trig="check_variable = { cwger_q_gc > 0.5 } check_variable = { cwger_bt_cdu > cwger_bt_spd }", ai=4),
   O("A grand coalition under the SPD.", J(gov(3, [1]), stab(0.02), party("npd", 0.004)),
     trig="check_variable = { cwger_q_gc > 0.5 } check_variable = { cwger_bt_spd > cwger_bt_cdu }", ai=4),
   O("Red-green.", J(gov(3, [17]), v("cwger_anti_nuclear", -5)), trig=f"has_country_flag = {P}_greens_founded check_variable = {{ cwger_q_rg > 0.5 }}",
     ai="base = 15 modifier = { factor = 2 has_country_flag = " + P + "_greens_realo }")],
  imm=J(f"{P}_coalition_math = yes", f"{P}_update_bundestag = yes",
        f"if = {{ limit = {{ NOT = {{ {UNION} }} NOT = {{ is_in_array = {{ gov_coalition_array = 1 }} }} date > 1976.6.1 check_variable = {{ cwger_csu_autonomy > 45 }} NOT = {{ has_country_flag = {P}_kreuth_seen }} }} "
        f"set_country_flag = {P}_kreuth_seen {fire(f'{EVG}.32', 20)} }}"))

E(f"{EVG}.25", "Landtag Elections",
  "A state election turns into a referendum on Bonn. The federal government's parties lose ground, as governing parties usually do between Bundestag elections - and with it, perhaps, a vote in the Bundesrat.",
  "GFX_election_day",
  [O("The Länder have spoken.", J("random_list = { 65 = { " + bundesrat_shift(4) + " } 35 = { " + bundesrat_shift(-3) + " } }",
     tt(f"{P}_tt_bundesrat", "The balance of the Bundesrat shifts. Union share now: §Y[?cwger_bundesrat_union|0]§!%."),
     "set_country_flag = { flag = " + P + "_landtag_cooldown days = 200 value = 1 }"))],
  trig=f"NOT = {{ has_country_flag = {P}_landtag_cooldown }} NOT = {{ has_country_flag = elections_in_progress }}")

E(f"{EVG}.26", "The Lambsdorff Paper",
  "The economics minister has put his demands in writing: cuts to welfare, lower taxes on business, less state. The SPD calls it a divorce letter. The Free Democrats are looking across the aisle.",
  "GFX_german_parliament_bundestag",
  [O("Let them go. We govern alone.", J(gov(3, []), f"set_country_flag = {P}_schmidt_iii", party("spd", 0.006), party("fdp", -0.008),
     "add_to_variable = { cwger_defectors = 0 }"), ai="base = 25 modifier = { factor = 0.3 check_variable = { cwger_fdp_course > 60 } }"),
   O("Concede on the budget.", J(v("cwger_fdp_course", -20), faction("dgb", -10), pp(-60), debt_gdp(-0.002)), ai=25),
   O("The FDP switches sides.", J(gov(1, [16]), f"set_country_flag = {P}_era2", f"set_country_flag = {P}_fdp_switched", party("fdp", -0.015), stab(-0.02),
     tt(f"{P}_tt_wende", "§YDie Wende§!: the Union and the FDP form a new government without an election.")),
     ai="base = 15 modifier = { factor = 4 check_variable = { cwger_fdp_course > 60 } }")])

E(f"{EVG}.28", "The Spy in the Chancellery",
  "Günter Guillaume, the chancellor's personal aide, has been arrested. He is an officer of the Ministry for State Security and has read everything that crossed the desk, including NATO papers on holiday in Norway. 'I am an officer of the National People's Army,' he tells the arresting officers.",
  "GFX_der_Spiegel",
  [O("The chancellor takes responsibility and resigns.", J("set_variable = { cwger_spd_leader = 2 }", f"{P}_refresh_leader = yes", v("cwger_stasi_penetration", -15),
     v("cwger_counterintel", 10), stab(-0.02), v("cwger_ostpolitik", -4)), ai=70),
   O("He stays. The spy was the security services' failure.", J(v("cwger_scandal", 25), pp(-100), party("spd", -0.01), v("cwger_stasi_penetration", -10)), ai=30)])

E(f"{EVG}.29", "A Spy Caught Early",
  "Counter-intelligence has identified an aide in the Chancellery who receives coded radio messages from the East. He is quietly removed months before he could read anything that matters.",
  "GFX_der_Spiegel",
  [O("Good work, Cologne.", J(v("cwger_stasi_penetration", -15), v("cwger_counterintel", 5), pp(40)))])

E(f"{EVG}.30", "A New Chairman for the CDU",
  "The Union has lost the 1972 election badly. Rainer Barzel resigns the chairmanship. The 43-year-old minister-president of Rhineland-Palatinate, Helmut Kohl, wants the party - but Franz Josef Strauß wants the candidacy.",
  "GFX_flag_cdu",
  [O("Helmut Kohl leads the party.", J(party("cdu", 0.004), v("cwger_csu_autonomy", 5)), ai=80),
   O("Strauß is the strongest man the Union has.", J("set_variable = { cwger_cdu_leader = 3 }", v("cwger_csu_autonomy", -20), party("cdu", -0.004), v("cwger_fdp_course", -8)), ai=20)])

E(f"{EVG}.31", "The K-Question",
  "Who will be the Union's candidate for chancellor? The CDU's young modernisers favour Ernst Albrecht of Lower Saxony. The CSU will accept no one but Franz Josef Strauß. Kohl, the chairman, waits.",
  "GFX_flag_cdu",
  [O("Strauß. The CSU gets its candidate.", J("set_variable = { cwger_cdu_leader = 3 }", v("cwger_csu_autonomy", -20), party("cdu", -0.008), party("spd", 0.004), v("cwger_fdp_course", -10)), ai=60),
   O("Albrecht. The CDU decides.", J("set_variable = { cwger_cdu_leader = 4 }", v("cwger_csu_autonomy", 15), party("cdu", 0.004)), ai=25),
   O("Kohl runs himself.", J(v("cwger_csu_autonomy", 8), pp(25)), ai=15)])

E(f"{EVG}.32", "Wildbad Kreuth",
  "After another lost election the CSU's deputies vote in Wildbad Kreuth to leave the joint parliamentary group. Strauß wants a fourth party that competes in every state. Kohl threatens to found a CDU branch in Bavaria.",
  "GFX_flag_cdu",
  [O("Reconcile. The joint group is restored.", J(v("cwger_csu_autonomy", -15), party("cdu", -0.003), pp(25)), ai=80),
   O("Let them go. A fourth party.", J(f"set_country_flag = {P}_csu_fourth_party", party("cdu", 0.008), stab(-0.02), v("cwger_csu_autonomy", 25)), ai=20)])

E(f"{EVG}.34", "The Chancellor Hands Over",
  "Willy Brandt has led the government through the treaties with the East. Tired, ill and increasingly isolated in his own party, he hands over to Helmut Schmidt, the manager the times seem to call for.",
  "GFX_german_parliament_bundestag",
  [O("Schmidt takes over.", J("set_variable = { cwger_spd_leader = 2 }", f"{P}_refresh_leader = yes", stab(0.01)))])

E(f"{EVG}.36", "The Candidate from Lower Saxony",
  "Oskar Lafontaine chairs the party, but Gerhard Schröder wins Lower Saxony with an absolute majority. Lafontaine steps aside: the SPD's candidate for chancellor is the man who once rattled the gates of the Chancellery and shouted 'I want in there!'",
  "GFX_election_day",
  [O("Innovation and justice.", J(party("spd", 0.01), faction("bdi", 4)))])

E(f"{EVG}.37", "Bremen Party Congress",
  "The Union is far behind in the polls. Heiner Geißler, Rita Süssmuth and Lothar Späth prepare to challenge Helmut Kohl at the Bremen party congress. Kohl has spent the summer on the telephone.",
  "GFX_flag_cdu",
  [O("Kohl fights back and dismisses Geißler.", J(pp(-25), party("cdu", 0.004), v("cwger_csu_autonomy", -5)), ai=75),
   O("Späth takes over.", J("set_variable = { cwger_cdu_leader = 5 }", f"{P}_refresh_leader = yes", party("cdu", 0.006), stab(-0.02)), ai=25)])

E(f"{EVG}.38", "Attack in Cologne",
  "At a campaign event in Cologne-Mülheim a mentally ill woman stabs Oskar Lafontaine in the neck with a knife. He survives by millimetres.",
  "GFX_Polizeiabsperrung",
  [O("He will return to the campaign.", J(party("spd", 0.006), stab(-0.01)), trig=f"NOT = {{ has_country_flag = {P}_lafontaine_badly_hurt }}"),
   O("Johannes Rau steps in as candidate.", J("set_variable = { cwger_spd_leader = 4 }", party("spd", 0.004), stab(-0.01)), trig=f"has_country_flag = {P}_lafontaine_badly_hurt")],
  imm=f"random_list = {{ 80 = {{ }} 20 = {{ set_country_flag = {P}_lafontaine_badly_hurt }} }}")

E(f"{EVG}.40", "Karlsruhe Rules on the Basic Treaty",
  "Bavaria has sued against the Basic Treaty. The Federal Constitutional Court upholds it - but declares that the German Reich continues to exist in law, that the Federal Republic is identical with it, and that the inner-German border is a border like that between Länder of the Federal Republic.",
  "GFX_Giese_Gericht",
  [O("The treaty stands, and so does the claim to unity.", J(v("cwger_westbindung", 3), v("cwger_ostpolitik", -2), v("cwger_unity", 3)), ai=70),
   O("Criticise Munich for the lawsuit.", J(v("cwger_csu_autonomy", 5), v("cwger_ostpolitik", 3), party("cdu", -0.003)), ai=30)])

# ===================================================================== TERRORISM
E(f"{EVG}.49", "Arrests in the Underground",
  "Police have raided a conspiratorial flat and arrested members of an armed group. Weapons, forged passports and plans for further attacks were found.\n\nRAF prisoners: §Y[?cwger_raf_prisoners|0]§! | active cadre: §Y[?cwger_raf_cadre|0]§!",
  "GFX_swat_polizei",
  [O("The search goes on.", J(stab(0.01), v("cwger_security", 1)))])

E(f"{EVG}.50", "The Second Generation",
  "The founders of the Red Army Faction are in prison. Outside, a new generation recruited from the support committees has one goal above all others: to free them.",
  "GFX_RAF_Schulz",
  [O("A high-security trial in Stammheim.", J(f"set_country_flag = {P}_stammheim", v("cwger_security", 5), v("cwger_rechtsstaat", -3), v("cwger_raf_milieu", 3),
     fire(f"{EVG}.59", 400)), ai=70),
   O("Ordinary prisons, ordinary courts.", J(v("cwger_rechtsstaat", 3), v("cwger_raf_milieu", -2), v("cwger_terror_left", 3)), ai=30)])

E(f"{EVG}.51", "Bomb Attack",
  "", "GFX_Brandanschlag_generic",
  [O("Find the perpetrators.", J(stab(-0.02), v("cwger_security", 3), v("cwger_rechtsstaat", -1)), ai=60),
   O("No panic. The state will not be provoked.", J(stab(-0.03), v("cwger_rechtsstaat", 2), v("cwger_raf_milieu", -1)), ai=40)],
  descs=[(f"check_variable = {{ cwger_raf_gen = 1 }}", "Bombs at a US Army headquarters, a police station and a publishing house. The 'May Offensive' of the Red Army Faction kills four people and injures dozens. A letter claims the attacks for the 'Commando Petra Schelm'."),
         (f"check_variable = {{ cwger_raf_gen > 1 }}", "An explosive device has gone off at a military installation used by the Americans. The commando's letter names the Federal Republic an 'outpost of US imperialism' and demands the release of the prisoners.")])

E(f"{EVG}.52", "Assassination",
  "", "GFX_Polizeiabsperrung",
  [O("A state funeral. The republic will not bow.", J(stab(-0.03), ws(0.03), v("cwger_security", 4)), ai=60),
   O("Give the crisis staff what it needs.", J(stab(-0.02), v("cwger_security", 8), v("cwger_rechtsstaat", -4), v("cwger_raf_milieu", 2)), ai=40)],
  descs=[(f"check_variable = {{ cwger_raf_gen = 2 }}", "A motorcycle pulls alongside a car at a traffic light. The Federal Prosecutor General and his driver die in a burst of automatic fire. The RAF calls it an 'execution'."),
         (f"check_variable = {{ cwger_raf_gen > 2 }}", "A sophisticated bomb triggered by a light barrier has killed one of the country's leading managers on his way to work. The third generation of the RAF strikes rarely - and with terrible precision. Investigators find almost nothing.")])

E(f"{EVG}.53", "Kidnapping",
  "A convoy has been ambushed, the escorts shot, a prominent figure dragged into a car. The kidnappers demand the release of imprisoned comrades and an aircraft to a country of their choosing. The government forms a crisis staff.",
  "GFX_GER_hostage1",
  [O("Exchange the prisoners.", J(f"{P}_hostage_exchange = yes", stab(-0.03), v("cwger_rechtsstaat", -2), pp(-25),
     tt(f"{P}_tt_blackmail", "The state has shown it can be blackmailed. Future kidnappings become §Rmore likely§!.")),
     ai="base = 30 modifier = { factor = 0.2 has_country_flag = " + P + "_state_blackmailable }"),
   O("The state does not yield.", J(f"set_country_flag = {P}_krisenstab_models", v("cwger_security", 5), fire(f"{EVG}.54", 2),
     f"if = {{ limit = {{ has_country_flag = {P}_contact_ban_law }} {v('cwger_raf_cadre', -2)} }}"), ai=70)])

E(f"{EVG}.54", "The Ultimatum",
  "", "GFX_GER_hostage3",
  [O("The crisis staff takes over.", J(f"set_country_flag = {P}_hostage_ultimatum", f"{P}_sec_start_ultimatum = yes",
     tt(f"{P}_tt_ultimatum", "The deadline is §Y21§! days. Run the crisis from the §YInternal Security§! window (crisis staff): storm with GSG 9, raid the safe houses, impose a contact ban, play for time - or give in.")))],
  descs=[(f"check_variable = {{ cwger_raf_gen = 2 }}", "A commando of the Popular Front for the Liberation of Palestine has hijacked a Lufthansa jet with 86 passengers to support the kidnappers' demands. The aircraft is hopping across the Mediterranean towards the Horn of Africa. The captain will be shot if the deadline passes."),
         (f"NOT = {{ check_variable = {{ cwger_raf_gen = 2 }} }}", "The kidnappers have set a final deadline. Investigators believe they know the district where the hostage is held, but not the house.")])

E(f"{EVG}.55", "The Rescue",
  "Shortly after midnight the commandos storm. Within minutes it is over: the hostages are free, the kidnappers dead or captured. 'Die Arbeit ist erledigt' - the job is done.",
  "GFX_swat_polizei2",
  [O("The state has proven itself.", J(f"clr_country_flag = {P}_hostage_crisis_active", f"clr_country_flag = {P}_hostage_ultimatum", stab(0.05), ws(0.05), pp(100), v("cwger_raf_cadre", -6), v("cwger_security", 3),
     f"if = {{ limit = {{ check_variable = {{ cwger_raf_gen = 2 }} NOT = {{ has_country_flag = {P}_deutscher_herbst_over }} }} {fire(f'{EVG}.57', 1)} }}"))])

E(f"{EVG}.56", "The Hostage Is Dead",
  "The body is found in the boot of a car. The commando's letter is three lines long. The crisis staff's strategy of firmness has cost a life, as everyone knew it might.",
  "GFX_GER_hostage5",
  [O("The state could not yield.", J(f"clr_country_flag = {P}_hostage_crisis_active", f"clr_country_flag = {P}_hostage_ultimatum", stab(-0.05), pp(-75), v("cwger_security", 4),
     f"if = {{ limit = {{ check_variable = {{ cwger_raf_gen = 2 }} NOT = {{ has_country_flag = {P}_deutscher_herbst_over }} }} {fire(f'{EVG}.57', 2)} }}"))])

E(f"{EVG}.57", "Death Night in Stammheim",
  "The morning after, the leaders of the first generation are found dead or dying in their cells on the seventh floor of Stammheim prison. The authorities speak of suicide; the sympathisers of murder. The German Autumn is over - but it has changed the republic.",
  "GFX_RAF_Schulz",
  [O("The official account stands.", J(v("cwger_rechtsstaat", -3), v("cwger_raf_milieu", 6)), ai=60),
   O("An independent inquiry.", J(v("cwger_rechtsstaat", 4), pp(-50), v("cwger_raf_milieu", 2)), ai=40)],
  imm=J(f"set_country_flag = {P}_deutscher_herbst_over", "subtract_from_variable = { cwger_raf_prisoners = 3 }",
        "clamp_variable = { var = cwger_raf_prisoners min = 0 max = 40 }", f"add_timed_idea = {{ idea = {P}_idea_deutscher_herbst days = 365 }}"))

E(f"{EVG}.58", "The Third Generation",
  "Nobody knows who they are. They leave no fingerprints, use no flats the police know, and strike the representatives of what they call the 'military-industrial complex'. The RAF has become a phantom.",
  "GFX_RAF_Schulz",
  [O("Rebuild the dragnet.", J(f"set_country_flag = {P}_j2m_dissolved", v("cwger_security", 5), v("cwger_rechtsstaat", -2), "add_to_variable = { cwger_bka_level = 0 }"), ai=60),
   O("Offer a way out to those who want one.", J(f"set_country_flag = {P}_j2m_dissolved", v("cwger_raf_milieu", -4), v("cwger_rechtsstaat", 2)), ai=40)])

E(f"{EVG}.59", "Hunger Strike",
  "The prisoners demand to be held together as prisoners of war. They refuse food. Holger Meins weighed 39 kilos when he died in 1974. Each day of the strike brings new sympathisers onto the streets.",
  "GFX_Demo_Generic",
  [O("Force-feeding. The law will be enforced.", J(f"set_country_flag = {{ flag = {P}_hunger_strike days = 300 value = 1 }}", v("cwger_rechtsstaat", -3), v("cwger_security", 2)), ai=60),
   O("Small concessions: shared yards, visits.", J(v("cwger_raf_milieu", -3), v("cwger_security", -2), party("cdu", 0.002)), ai=40)],
  trig="check_variable = { cwger_raf_prisoners > 2 } check_variable = { cwger_raf_gen < 4 }")

E(f"{EVG}.60", "The RAF Dissolves",
  "A typed letter of eight pages arrives at Reuters: 'Almost 28 years ago, on 14 May 1970, the RAF was born in a liberation action. Today we end this project.' The Red Army Faction is history.",
  "GFX_der_Spiegel",
  [O("History will judge them.", J("set_variable = { cwger_raf_cadre = 0 }", f"set_country_flag = {P}_rz_dissolved", stab(0.03), v("cwger_security", -5), v("cwger_rechtsstaat", 3), f"set_country_flag = {P}_raf_dissolved"))])

E(f"{EVG}.61", "Bad Kleinen",
  "An operation at a railway station in Mecklenburg was supposed to arrest two RAF members betrayed by an informant. A GSG 9 officer and a suspect are dead. Witnesses say the suspect was executed on the tracks. The Interior Minister and the Federal Prosecutor resign.",
  "GFX_swat_polizei",
  [O("A catastrophe for the security services.", J(v("cwger_rechtsstaat", -5), v("cwger_security", -4), v("cwger_raf_milieu", 3), pp(-50), v("cwger_scandal", 12)))])

E(f"{EVG}.62", "Right-Wing Terror",
  "", "GFX_Brandanschlag_generic",
  [O("Ban the organisations behind it.", J(f"set_country_flag = {P}_far_right_banned", f"clr_country_flag = {P}_wsg_hoffmann_active", v("cwger_security", 3), party("npd", -0.003), stab(-0.02)), ai=60),
   O("The work of isolated individuals.", J(f"set_country_flag = {{ flag = {P}_wsg_hoffmann_active days = 1500 value = 1 }}", v("cwger_terror_right", 5), stab(-0.02), v("cwger_rechtsstaat", -2)), ai=40)],
  descs=[(f"NOT = {{ has_global_flag = {P}_unity_achieved }}", "A pipe bomb in a crowd. The perpetrator was a member of a 'military sports group' that trained in the woods with Wehrmacht surplus while the authorities spoke of hobbyists."),
         (f"has_global_flag = {P}_unity_achieved", "Petrol bombs through the window of a house where Turkish families live. Three dead, among them children. In other towns crowds applaud as hostels for asylum seekers burn.")])

E(f"{EVG}.65", "International Terrorism",
  "", "GFX_terrorist_attack",
  [O("Hunt down the network.", J(v("cwger_security", 4), v("cwger_terror_foreign", -4), stab(-0.02)), ai=60),
   O("Quiet diplomacy with the sponsors.", J(v("cwger_terror_foreign", -2), v("cwger_rechtsstaat", -2), v("cwger_westbindung", -2)), ai=40)],
  descs=[("date < 1983.1.1", "Palestinian and international commandos use West German soil as a battlefield: an attack at an airport, a bomb in a Jewish community centre. The trail leads to Beirut, Baghdad and Damascus."),
         ("date > 1982.12.31 date < 1991.1.1", "A bomb in a Berlin discotheque frequented by American soldiers. Intercepted cables from the Libyan People's Bureau in East Berlin speak of a 'joyful event'."),
         ("date > 1990.12.31", "PKK militants occupy consulates and set fire to Turkish businesses across the country. Ankara demands a ban.")])

E(f"{EVG}.66", "Massacre in Munich",
  "Members of Black September have broken into the Israeli team's quarters in the Olympic Village. Two athletes are dead, nine are hostages. The night ends at Fürstenfeldbruck airfield with all nine hostages dead after a botched rescue by Bavarian police with no special training and no radios.\n\n'The Games must go on,' says Avery Brundage.",
  "GFX_event_olympics",
  [O("This must never happen again.", J(f"set_country_flag = {P}_munich_happened", stab(-0.05), v("cwger_terror_foreign", 10), v("cwger_security", 5),
     "if = { limit = { country_exists = ISR } ISR = { add_opinion_modifier = { target = ROOT modifier = medium_decrease } } }",
     tt(f"{P}_tt_gsg9_unlock", "The §YGSG 9§! focus becomes available.")))])

E(f"{EVG}.67", "A Plot Foiled",
  "Plain-clothes officers in the Olympic Village notice men in tracksuits climbing the fence at four in the morning. The attack on the Israeli team is stopped before it begins.",
  "GFX_event_olympics",
  [O("Security planning paid off.", J(f"set_country_flag = {P}_munich_happened", stab(0.03), pp(50),
     "if = { limit = { country_exists = ISR } ISR = { add_opinion_modifier = { target = ROOT modifier = medium_increase } } }"))])

# ===================================================================== ECONOMY
E(f"{EVG}.80", "The Oil Shock",
  "The Arab oil producers have cut their output and the price of crude has quadrupled. The Federal Republic imports almost all of its oil. The government orders car-free Sundays; children ride their bicycles down the empty Autobahn.",
  "GFX_oil_refinery",
  [O("Car-free Sundays and a speed limit.", J(f"add_timed_idea = {{ idea = {P}_idea_car_free_sundays days = 120 }}", stab(-0.01), pp(25)), ai=40),
   O("An energy programme: coal and nuclear.", J(v("cwger_anti_nuclear", 4), faction("bdi", 5), money_gdp(-0.002),
     tt(f"{P}_tt_energy_prog", "The energy pillar of the focus tree becomes more urgent.")), ai=40),
   O("Let prices do the work.", J(v("cwger_bundesbank", 10), f"add_timed_idea = {{ idea = {P}_idea_stagflation days = 365 }}", faction("dgb", -5)), ai=20)])

E(f"{EVG}.81", "The Second Oil Shock",
  "Revolution in Iran, war between Iran and Iraq: the oil price doubles again. Unemployment passes one million for the first time since the fifties, and the deficit grows.",
  "GFX_burning_oil_refinery",
  [O("Austerity.", J(v("cwger_bundesbank", -10), faction("dgb", -8), v("cwger_fdp_course", 8), debt_gdp(-0.003)), ai=50),
   O("A stimulus programme.", J(debt_gdp(0.008), v("cwger_bundesbank", 15), faction("dgb", 6), v("cwger_fdp_course", 12)), ai=50)],
  imm=f"add_timed_idea = {{ idea = {P}_idea_stagflation days = 540 }}")

E(f"{EVG}.82", "Strike for the 35-Hour Week",
  "IG Metall has called the biggest industrial action in the Federal Republic's history. The employers answer with lockouts. 'Work for all, shorter hours' against 'the German model is being destroyed'.",
  "GFX_IG_metall",
  [O("Mediate: 38.5 hours, flexibly arranged.", J(f"add_ideas = {P}_idea_working_time_385", faction("dgb", 10), faction("bdi", -6), stab(0.01)), ai=60),
   O("Support the lockouts.", J(faction("bdi", 8), faction("dgb", -15), stab(-0.03), party("spd", 0.005)), ai=40)])

E(f"{EVG}.84", "The Steel Crisis",
  "Asian competition and overcapacity hit the Ruhr. Krupp wants to close Rheinhausen; workers occupy the Rhine bridge.",
  "GFX_steel_mill",
  [O("Subsidise the steel works.", J(money_gdp(-0.002), faction("dgb", 8), faction("bdi", -3)), ai=50),
   O("Restructure the Ruhr.", J(faction("bdi", 6), faction("dgb", -8), stab(-0.02), tech("CAT_production_lines", 0.5, 1)), ai=50)])

E(f"{EVG}.85", "The Bundesbank Says No",
  "The Central Bank Council in Frankfurt has raised the discount rate against the express wishes of the government. Inflation, says the Bundesbank president, is the most unsocial tax of all.",
  "GFX_stock_market",
  [O("Accept the independence of the Bundesbank.", J(v("cwger_bundesbank", -30), stab(-0.02),
     f"if = {{ limit = {{ NOT = {{ has_idea = {P}_idea_bundesbank_credibility }} }} add_timed_idea = {{ idea = {P}_idea_bundesbank_credibility days = 730 }} }}"), ai=80),
   O("A public quarrel with Frankfurt.", J(v("cwger_bundesbank", -10), pp(-50), v("cwger_scandal", 5), faction("dgb", 4)), ai=20)])

# ===================================================================== SOCIETY
E(f"{EVG}.90", "The Hofgarten Demonstration",
  "Three hundred thousand people fill the Bonn Hofgarten against the stationing of new American missiles. Heinrich Böll speaks, Petra Kelly speaks, so do SPD deputies. The chancellor's own party is marching against his policy.",
  "GFX_peace_demonstration_berlin",
  [O("Dialogue with the movement.", J(v("cwger_peace_movement", -5), v("cwger_westbindung", -2), party("greens", 0.002), protest(-5)), ai=40),
   O("Security policy is not made on the street.", J(protest(10), f"add_timed_idea = {{ idea = {P}_idea_peace_movement_idea days = 365 }}", v("cwger_peace_movement", 5), v("cwger_westbindung", 3), party("greens", 0.004)), ai=60)])

E(f"{EVG}.91", "Brokdorf",
  "Tens of thousands march to the planned reactor site on the Elbe. Water cannon, helicopters, barbed wire. A 'civil war around a building site', the newspapers write.",
  "GFX_polizei_riot",
  [O("Clear the site.", J(protest(8), v("cwger_security", 3), v("cwger_anti_nuclear", 6), v("cwger_rechtsstaat", -2), faction("bdi", 3)), ai=60),
   O("Halt construction until the courts decide.", J(v("cwger_anti_nuclear", -6), faction("bdi", -6), party("greens", -0.002)), ai=40)])

E(f"{EVG}.92", "War Scare",
  "A NATO command exercise has been followed by alarming Soviet reactions: aircraft on alert in East Germany, intelligence officers ordered to look for signs of a surprise attack. In Bonn the cabinet meets at night.",
  "GFX_missiles_on_road",
  [O("Open the line to Moscow.", J(tension(-5), v("cwger_westbindung", -3), v("cwger_ostpolitik", 4)), ai=50),
   O("Stand firm with the alliance.", J(ws(0.05), v("cwger_peace_movement", 10), v("cwger_westbindung", 3)), ai=50)])

E(f"{EVG}.93", "The Greens Are Founded",
  "In Karlsruhe, environmentalists, pacifists, feminists, former Maoists and a few conservatives found a federal party: 'Die Grünen'. 'We are neither left nor right, we are in front.'",
  "GFX_Demo_Generic",
  [O("A new force in German politics.", J(f"set_country_flag = {P}_greens_founded", party("greens", 0.015), v("cwger_anti_nuclear", 3)))])

E(f"{EVG}.94", "Die Republikaner",
  "Two CSU deputies, disgusted by the billion-mark credit for the GDR, found a party to the right of the Union. Franz Schönhuber, a former Waffen-SS man and television presenter, soon takes it over.",
  "GFX_npd_flag",
  [O("A new party on the right.", J(f"set_country_flag = {P}_rep_founded", party("rep", 0.01), party("cdu", -0.004)))])

E(f"{EVG}.95", "The Asylum Debate",
  "More than four hundred thousand people apply for asylum in a single year - from Yugoslavia, Romania, Turkey and Africa. Municipalities run out of beds; tabloids run out of restraint. The right to asylum in Article 16 is unconditional - for now.",
  "GFX_German_migrant",
  [O("Seek an asylum compromise.", J(v("cwger_terror_right", -5), party("rep", -0.005), v("cwger_rechtsstaat", -3), party("cdu", 0.003)), ai=60),
   O("Article 16 is not negotiable.", J(v("cwger_rechtsstaat", 3), v("cwger_terror_right", 5), party("rep", 0.004), party("greens", 0.002)), ai=40)],
  imm=J(f"set_country_flag = {P}_asylum_surge", f"add_timed_idea = {{ idea = {P}_idea_asylum_crisis days = 730 }}"))

E(f"{EVG}.96", "Chernobyl",
  "A reactor has exploded in the Ukraine. A radioactive cloud drifts over Bavaria; children are kept out of sandpits, lettuce is ploughed under, and the government takes days to give clear advice.",
  "GFX_nuclear_power_plant",
  [O("Create an environment ministry.", J(v("cwger_anti_nuclear", -5), pp(-25), party("cdu", 0.002)), ai=60),
   O("German reactors are safe.", J(v("cwger_anti_nuclear", 8), party("greens", 0.005)), ai=40)],
  imm=J(f"set_country_flag = {P}_chernobyl", v("cwger_anti_nuclear", 20, show=False)))

E(f"{EVG}.97", "Forest Dieback",
  "The forests are dying, says Der Spiegel: acid rain from coal power plants has damaged a third of the trees. The fear unites conservationists and conservative foresters.",
  "GFX_der_Spiegel",
  [O("Filters for every power plant.", J(f"add_ideas = {P}_idea_flue_gas_law", faction("bdi", -4), party("greens", -0.003)), ai=70),
   O("More research is needed.", J(party("greens", 0.005), v("cwger_anti_nuclear", 3)), ai=30)])

E(f"{EVG}.120", "Trouble on the Transit Routes",
  "East German border guards hold up lorries for hours on the Helmstedt autobahn; a family is arrested for 'transit abuse'. The road to West Berlin is again a lever in someone else's hand.",
  "GFX_Polizeiabsperrung",
  [O("Protest through the Western Allies.", J(v("cwger_westbindung", 2), v("cwger_berlin_access", -3), tension(1)), ai=50),
   O("Pay a higher transit lump sum.", J(money_gdp(-0.0008), v("cwger_berlin_access", 6), dv("cwddr_hard_currency", -3), v("cwger_ostpolitik", 2)), ai=50)])

E(f"{EVG}.110", "France Votes on Maastricht",
  "", "GFX_european_parliament",
  [O("The road to the euro is open.", J(f"set_country_flag = {P}_maastricht_signed", v("cwger_westbindung", 5)), trig=f"has_country_flag = {P}_maastricht_yes"),
   O("Europe stalls. The D-Mark remains.", J(f"set_country_flag = {P}_maastricht_failed", v("cwger_westbindung", -3), v("cwger_bundesbank", -10)), trig=f"NOT = {{ has_country_flag = {P}_maastricht_yes }}")],
  descs=[(f"has_country_flag = {P}_maastricht_yes", "Fifty-one percent. France has said yes to the Treaty on European Union by the narrowest margin. The single currency will come - and the Bundesbank's rules will come with it."),
         (f"NOT = {{ has_country_flag = {P}_maastricht_yes }}", "Non. French voters have rejected the Maastricht Treaty. Mitterrand's European project is in ruins; in Frankfurt, nobody is entirely unhappy.")],
  imm=J(f"random_list = {{ 70 = {{ modifier = {{ add = 10 check_variable = {{ cwger_westbindung > 70 }} }} set_country_flag = {P}_maastricht_yes }} 30 = {{ modifier = {{ add = 10 check_variable = {{ cwger_bundesbank > 50 }} }} }} }}"))

# ===================================================================== SCANDALS
scandal_opts = [O("Accept the resignations.", J(v("cwger_scandal", -25), pp(-50), ruling_party_shift(-0.004)), ai=60),
                O("Sit it out.", J(v("cwger_scandal", 5), ruling_party_shift(-0.01), stab(-0.02), corruption(True, 40)), ai=40)]
E(f"{EVG}.100", "", "", "", [O("ok")], hidden=True,
  imm="""random_list = {
	10 = { """ + fire(f"{EVG}.106", 1) + """ }
	20 = { modifier = { factor = 0 date < 1975.1.1 } modifier = { factor = 0 date > 1979.1.1 } """ + fire(f"{EVG}.102", 1) + """ }
	25 = { modifier = { factor = 0 date < 1981.1.1 } modifier = { factor = 0 date > 1987.1.1 } """ + fire(f"{EVG}.101", 1) + """ }
	20 = { modifier = { factor = 0 date < 1981.1.1 } modifier = { factor = 0 date > 1986.1.1 } """ + fire(f"{EVG}.104", 1) + """ }
	20 = { modifier = { factor = 0 date < 1986.6.1 } modifier = { factor = 0 date > 1990.1.1 } """ + fire(f"{EVG}.103", 1) + """ }
	25 = { modifier = { factor = 0 date < 1993.1.1 } """ + fire(f"{EVG}.105", 1) + """ }
}""")
E(f"{EVG}.101", "The Flick Affair",
  "The Flick concern has paid millions to the parties through 'charitable' channels - and received tax relief on the sale of its Daimler shares. An accountant's notes say 'cultivating the political landscape'. The economics minister is indicted.",
  "GFX_der_Spiegel", scandal_opts)
E(f"{EVG}.102", "The Lockheed Affair",
  "Lockheed is said to have paid bribes across the Western world to sell its aircraft - in Bonn, the name of the defence ministry of the Starfighter years keeps appearing.",
  "GFX_Der_stern", scandal_opts)
E(f"{EVG}.103", "Waterkant Gate",
  "A Land campaign has been run with a spy, a detective and an anonymous tax complaint against the opposition candidate. The minister-president gives his 'word of honour' - and is found dead in a Geneva hotel bathtub a few weeks later.",
  "GFX_der_Spiegel", scandal_opts)
E(f"{EVG}.104", "Neue Heimat",
  "The trade unions' housing company, the largest in Europe, has been run by managers who enriched themselves at the tenants' expense. The DGB's credibility is in tatters.",
  "GFX_Der_stern", [O("The unions must clean house.", J(v("cwger_scandal", -15), faction("dgb", -12), party("spd", -0.006)), ai=60),
                    O("A matter for the courts.", J(v("cwger_scandal", 5), faction("dgb", -6), party("spd", -0.01)), ai=40)])
E(f"{EVG}.105", "Black Accounts",
  "Cash in suitcases, accounts in Switzerland, donors whose names the former chancellor refuses to reveal because he has given his 'word of honour'. The party donations affair shakes the Union to its foundations.",
  "GFX_investigation_schreiber_kiep", scandal_opts)
E(f"{EVG}.106", "A Bonn Affair",
  "A minister's travel expenses, a state secretary's consultancy contracts, a party treasurer's memory gaps: Bonn has another affair. The magazines are delighted.",
  "GFX_der_Spiegel", scandal_opts)

# ---------------------------------------------------------------- monthly checks
EXTRA_EFFECTS.append(f"""
# Monthly event triggers for West Germany. None of them is dated to the day: each needs
# a window and the right conditions, and some never happen at all.
{P}_events_tick = {{
	# Brandt's successor: the spy affair, or a later hand-over
	if = {{
		limit = {{ {SPD} check_variable = {{ cwger_spd_leader = 1 }} date > 1973.9.1 NOT = {{ has_country_flag = {P}_guillaume_done }} check_variable = {{ cwger_stasi_penetration > 39 }} }}
		random_list = {{
			92 = {{ }}
			8 = {{
				set_country_flag = {P}_guillaume_done
				if = {{ limit = {{ check_variable = {{ cwger_counterintel > 55 }} }} country_event = {{ id = {EVG}.29 days = 1 }} }}
				else = {{ country_event = {{ id = {EVG}.28 days = 1 }} }}
			}}
		}}
	}}
	if = {{
		limit = {{ {SPD} check_variable = {{ cwger_spd_leader = 1 }} date > 1976.12.1 NOT = {{ has_country_flag = {P}_brandt_handover }} }}
		set_country_flag = {P}_brandt_handover
		country_event = {{ id = {EVG}.34 days = 3 }}
	}}
	# the FDP looks for a new partner
	if = {{
		limit = {{ {SPD} {FDP_IN} check_variable = {{ cwger_fdp_course > 40 }} date > 1976.6.1 NOT = {{ has_country_flag = {P}_fdp_switch_cooldown }} NOT = {{ has_country_flag = elections_in_progress }} }}
		set_country_flag = {{ flag = {P}_fdp_switch_cooldown days = 720 value = 1 }}
		country_event = {{ id = {EVG}.26 days = 5 }}
	}}
	# Union leadership
	if = {{
		limit = {{ NOT = {{ {UNION} }} date > 1979.5.1 date < 1983.1.1 NOT = {{ has_country_flag = {P}_kfrage_done }} }}
		set_country_flag = {P}_kfrage_done
		country_event = {{ id = {EVG}.31 days = 2 }}
	}}
	if = {{
		limit = {{ NOT = {{ {UNION} }} OR = {{ check_variable = {{ cwger_cdu_leader = 3 }} check_variable = {{ cwger_cdu_leader = 4 }} }} date > 1981.1.1 date < 1990.1.1 }}
		set_variable = {{ cwger_cdu_leader = 2 }}
	}}
	if = {{
		limit = {{ {UNION} check_variable = {{ cwger_cdu_leader = 2 }} date > 1989.6.1 date < 1989.10.1 check_variable = {{ party_pop_array^1 < 0.37 }} NOT = {{ has_country_flag = {P}_bremen_done }} }}
		set_country_flag = {P}_bremen_done
		country_event = {{ id = {EVG}.37 days = 3 }}
	}}
	if = {{
		limit = {{ NOT = {{ {UNION} }} check_variable = {{ cwger_cdu_leader = 2 }} date > 1998.11.1 }}
		set_variable = {{ cwger_cdu_leader = 6 }}
	}}
	if = {{
		limit = {{ NOT = {{ {SPD} }} check_variable = {{ cwger_spd_leader = 5 }} date > 1990.3.1 date < 1990.6.1 NOT = {{ has_country_flag = {P}_cologne_attack_done }} }}
		random_list = {{ 70 = {{ }} 30 = {{ set_country_flag = {P}_cologne_attack_done country_event = {{ id = {EVG}.38 days = 1 }} }} }}
	}}
	# Munich 1972
	if = {{
		limit = {{ date > 1972.8.26 date < 1972.9.11 NOT = {{ has_country_flag = {P}_munich_happened }} NOT = {{ has_country_flag = {P}_munich_rolled }} }}
		set_country_flag = {P}_munich_rolled
		random_list = {{
			60 = {{ modifier = {{ factor = 0.4 has_country_flag = {P}_olympic_security }} country_event = {{ id = {EVG}.66 days = 1 }} }}
			40 = {{ modifier = {{ factor = 0 NOT = {{ has_country_flag = {P}_olympic_security }} }} country_event = {{ id = {EVG}.67 days = 1 }} }}
			10 = {{ modifier = {{ factor = 0 has_country_flag = {P}_olympic_security }} }}
		}}
	}}
	# the German Autumn ends one way or another
	if = {{
		limit = {{ check_variable = {{ cwger_raf_gen = 2 }} date > 1982.1.1 NOT = {{ has_country_flag = {P}_deutscher_herbst_over }} }}
		set_country_flag = {P}_deutscher_herbst_over
	}}
	# economy and society
	if = {{
		limit = {{ date > 1982.1.1 NOT = {{ has_country_flag = {P}_strike_done }} check_variable = {{ labour_unions_opinion < 60 }} }}
		random_list = {{ 97 = {{ }} 3 = {{ set_country_flag = {P}_strike_done country_event = {{ id = {EVG}.82 days = 1 }} }} }}
	}}
	if = {{
		limit = {{ date > 1980.1.1 NOT = {{ has_country_flag = {P}_steel_done }} }}
		random_list = {{ 98 = {{ }} 2 = {{ set_country_flag = {P}_steel_done country_event = {{ id = {EVG}.84 days = 1 }} }} }}
	}}
	if = {{
		limit = {{ check_variable = {{ cwger_peace_movement > 50 }} date > 1979.6.1 NOT = {{ has_country_flag = {P}_peace_demo_cooldown }} }}
		set_country_flag = {{ flag = {P}_peace_demo_cooldown days = 900 value = 1 }}
		country_event = {{ id = {EVG}.90 days = 4 }}
	}}
	if = {{
		limit = {{ check_variable = {{ cwger_anti_nuclear > 25 }} NOT = {{ has_country_flag = {P}_brokdorf_cooldown }} }}
		set_country_flag = {{ flag = {P}_brokdorf_cooldown days = 1200 value = 1 }}
		country_event = {{ id = {EVG}.91 days = 4 }}
	}}
	if = {{
		limit = {{ NOT = {{ has_country_flag = {P}_greens_founded }} date > 1979.1.1 OR = {{ date > 1980.1.1 check_variable = {{ cwger_anti_nuclear > 30 }} check_variable = {{ cwger_peace_movement > 40 }} }} }}
		random_list = {{ 70 = {{ }} 30 = {{ country_event = {{ id = {EVG}.93 days = 2 }} }} }}
	}}
	if = {{
		limit = {{ NOT = {{ has_country_flag = {P}_rep_founded }} date > 1983.10.1 OR = {{ {UNION} has_completed_focus = {P}_billion_credit has_completed_focus = {P}_strauss_east_credit }} }}
		random_list = {{ 90 = {{ }} 10 = {{ country_event = {{ id = {EVG}.94 days = 2 }} }} }}
	}}
	if = {{
		limit = {{ NOT = {{ has_country_flag = {P}_asylum_seen }} OR = {{ date > 1991.6.1 AND = {{ has_global_flag = {P}_wall_open date > 1990.6.1 }} AND = {{ date > 1985.1.1 check_variable = {{ imp_refugee_pressure > 0.15 }} }} }} }}
		random_list = {{ 85 = {{ }} 15 = {{ set_country_flag = {P}_asylum_seen country_event = {{ id = {EVG}.95 days = 2 }} }} }}
	}}
	if = {{
		limit = {{ date > 1986.4.20 date < 1986.7.1 country_exists = SOV NOT = {{ has_country_flag = {P}_chernobyl_rolled }} }}
		set_country_flag = {P}_chernobyl_rolled
		random_list = {{ 65 = {{ country_event = {{ id = {EVG}.96 days = 3 }} }} 35 = {{ }} }}
	}}
	if = {{
		limit = {{ date > 1981.1.1 NOT = {{ has_country_flag = {P}_waldsterben_done }} }}
		random_list = {{ 96 = {{ }} 4 = {{ set_country_flag = {P}_waldsterben_done country_event = {{ id = {EVG}.97 days = 2 }} }} }}
	}}
	if = {{
		limit = {{ country_exists = DDR check_variable = {{ cwger_berlin_access < 40 }} NOT = {{ has_country_flag = {P}_transit_cooldown }} has_global_flag = mdcw_cw_initialized check_variable = {{ global.mdcw_cw_tension > 50 }} }}
		set_country_flag = {{ flag = {P}_transit_cooldown days = 720 value = 1 }}
		country_event = {{ id = {EVG}.120 days = 2 }}
	}}
	{P}_ddr_events_tick = yes
}}
""")
