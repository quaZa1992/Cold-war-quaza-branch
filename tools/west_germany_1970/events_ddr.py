# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""East German events, the inner-German crisis chain and the dynamic road to unity."""
from cw_lib import *
from events_lib import E, O, fire, ger, ddr, EXTRA_EFFECTS
from systems import DDR_LEADERS
from migration import transfer


def ddr_leader(key, n):
    name, pic, ideo = DDR_LEADERS[key]
    return f'kill_country_leader = yes\ncreate_country_leader = {{ name = "{name}" picture = "{pic}" expire = "2050.1.1" ideology = {ideo} }}\nset_variable = {{ cwddr_leader = {n} }}'


def gv(var, n):
    """GER variable change from DDR scope."""
    return ger(v(var, n))


EXTRA_EFFECTS.append(f"""
# DDR scope. The Chinese solution: works only while Moscow stands behind the SED and the
# security organs still obey. Otherwise the troops refuse and the border opens.
{P}_ddr_crackdown_roll = {{
	random_list = {{
		30 = {{
			modifier = {{ add = 25 check_variable = {{ cwddr_moscow_backing > 60 }} }}
			modifier = {{ add = 15 check_variable = {{ cwddr_sed_control > 55 }} }}
			modifier = {{ add = -20 check_variable = {{ cwddr_opposition > 60 }} }}
			modifier = {{ factor = 0.3 has_idea = {P}_idea_ddr_crackdown }}
			set_variable = {{ cwddr_wende_stage = 9 }}
			add_to_variable = {{ cwddr_sed_control = 15 }}
			add_to_variable = {{ cwddr_crisis = -25 }}
			add_to_variable = {{ cwddr_opposition = -20 }}
			clamp_variable = {{ var = cwddr_sed_control min = 0 max = 100 }}
			clamp_variable = {{ var = cwddr_crisis min = 0 max = 100 }}
			clamp_variable = {{ var = cwddr_opposition min = 0 max = 100 }}
			if = {{ limit = {{ NOT = {{ has_idea = {P}_idea_ddr_crackdown }} }} add_timed_idea = {{ idea = {P}_idea_ddr_crackdown days = 1825 }} }}
			country_event = {{ id = {EVD}.34 days = 1 }}
			if = {{ limit = {{ country_exists = GER }} GER = {{ country_event = {{ id = {EVG}.131 days = 2 }} }} }}
		}}
		40 = {{
			country_event = {{ id = {EVD}.39 days = 1 }}
		}}
	}}
}}

# GER scope: request unity under the chosen path (cwger_unity_path 1 = Art. 23, 2 = Art. 146).
{P}_request_two_plus_four = {{
	if = {{
		limit = {{ country_exists = SOV SOV = {{ is_ai = no }} }}
		SOV = {{ country_event = {{ id = {EVG}.140 days = 3 }} }}
	}}
	else_if = {{
		limit = {{ country_exists = SOV }}
		SOV = {{ country_event = {{ id = {EVG}.140 days = 10 }} }}
	}}
	else = {{
		country_event = {{ id = {EVG}.141 days = 5 }}
	}}
}}

# GER scope: carry out unity on the chosen path.
{P}_complete_unity = {{
	if = {{ limit = {{ check_variable = {{ cwger_unity_path = 2 }} }} {P}_unity_art146 = yes }}
	else = {{ {P}_unity_art23 = yes }}
	every_other_country = {{ limit = {{ is_ai = no }} country_event = {{ id = {EVG}.150 days = 1 }} }}
}}

# Monthly, GER scope: East German events that follow the GDR's own meters.
{P}_ddr_events_tick = {{
	if = {{
		limit = {{ country_exists = DDR DDR = {{ has_country_flag = {P}_ddr_initialized }} NOT = {{ has_global_flag = {P}_unity_achieved }} }}
		if = {{
			limit = {{ date > 1971.4.15 NOT = {{ has_global_flag = {P}_honecker_era }} }}
			set_global_flag = {P}_honecker_era
			DDR = {{ country_event = {{ id = {EVD}.1 days = 1 }} }}
		}}
		if = {{
			limit = {{ date > 1976.9.1 NOT = {{ has_global_flag = {P}_biermann_done }} DDR = {{ check_variable = {{ cwddr_opposition > 9 }} }} }}
			random_list = {{ 94 = {{ }} 6 = {{ set_global_flag = {P}_biermann_done DDR = {{ country_event = {{ id = {EVD}.6 days = 1 }} }} }} }}
		}}
		if = {{
			limit = {{ date > 1978.1.1 NOT = {{ has_global_flag = {P}_min_exchange_done }} DDR = {{ check_variable = {{ cwddr_hard_currency > 45 }} }} }}
			set_global_flag = {P}_min_exchange_done
			DDR = {{ country_event = {{ id = {EVD}.5 days = 2 }} }}
		}}
		# a hard-line coup in Moscow can put the Wende into reverse
		if = {{
			limit = {{
				has_global_flag = {P}_wall_open
				country_exists = SOV
				date > 1990.1.1
				NOT = {{ has_global_flag = {P}_moscow_coup_rolled }}
				NOT = {{ SOV = {{ has_completed_focus = COLDWAR_SOV_gor_the_sinatra_doctrine }} }}
			}}
			random_list = {{
				97 = {{ }}
				3 = {{
					set_global_flag = {P}_moscow_coup_rolled
					set_global_flag = {P}_moscow_coup_succeeded
					DDR = {{ add_to_variable = {{ cwddr_moscow_backing = 40 }} add_to_variable = {{ cwddr_sed_control = 15 }} clamp_variable = {{ var = cwddr_moscow_backing min = 0 max = 100 }} clamp_variable = {{ var = cwddr_sed_control min = 0 max = 100 }} }}
					{tension(8)}
					country_event = {{ id = {EVG}.145 days = 1 }}
				}}
			}}
		}}
	}}
}}
""")

# ====================================================================== GDR, 1970s
E(f"{EVD}.1", "Honecker Replaces Ulbricht",
  "With Moscow's blessing the Politburo forces Walter Ulbricht to resign 'for reasons of age'. Erich Honecker, the man who built the Wall in August 1961, promises 'the unity of economic and social policy': more flats, more consumer goods, more coffee - paid for with credits the GDR does not have.",
  "GFX_egon_krenz_ddr",
  [O("The unity of economic and social policy.", J(ddr_leader("honecker", 1), dv_self("cwddr_hard_currency", 6), dv_self("cwddr_sed_control", 3), "add_stability = 0.03"))],
  scope="DDR")

E(f"{EVD}.2", "Bonn Offers a Larger Swing",
  "The Federal Republic proposes to raise the interest-free overdraft in inner-German trade. More Western goods, fewer questions - and a little more dependence on the class enemy.",
  "GFX_treaty",
  [O("Accept the credit.", J(dv_self("cwddr_hard_currency", -6), dv_self("cwddr_west_dependency", 6), "set_global_flag = " + P + "_swing_high",
     ger(f"set_temp_variable = {{ cwger_t_prog = 5 }} set_temp_variable = {{ cwger_t_size = 2 }} {P}_start_programme = yes {v('cwger_ostpolitik', 3, show=False)}"),
     tt(f"{P}_tt_swing_prog", "Starts the Imperia §YConsumer Supply Credits§! programme from the Federal Republic to the GDR.")),
     ai="base = 70 modifier = { factor = 2 check_variable = { cwddr_hard_currency > 50 } }"),
   O("We do not need Bonn's charity.", J(dv_self("cwddr_sed_control", 2), dv_self("cwddr_hard_currency", 3), ger(v("cwger_ostpolitik", -3))), ai=30)],
  scope="DDR")

E(f"{EVD}.3", "The Billion-Mark Credit",
  "Franz Josef Strauß himself has arranged a bank loan of one billion marks, guaranteed by the federal government. Schalck-Golodkowski brings the conditions: the self-firing devices on the border are to go, and the minimum exchange for children is to be dropped.",
  "GFX_treaty",
  [O("Take the money, dismantle the SM-70.", J(dv_self("cwddr_hard_currency", -15), dv_self("cwddr_west_dependency", 12), dv_self("cwddr_sed_control", -2), dv_self("cwddr_exit_pressure", 2),
     ger(f"{v('cwger_ostpolitik', 6, show=False)} {money_gdp(-0.001).replace(chr(10), ' ')}")),
     ai="base = 80 modifier = { factor = 0.3 check_variable = { cwddr_hard_currency < 30 } }"),
   O("No conditions on our border.", J(dv_self("cwddr_sed_control", 3), dv_self("cwddr_hard_currency", 4)), ai=20)],
  scope="DDR")

E(f"{EVD}.4", "Prisoners for Hard Currency",
  "The lawyer Wolfgang Vogel brings a new list from Bonn. Every political prisoner released to the West brings tens of thousands of D-Marks - in goods delivered through the churches.",
  "GFX_politics_negotiations",
  [O("Sell them.", J(dv_self("cwddr_hard_currency", -4), dv_self("cwddr_opposition", -2), dv_self("cwddr_west_dependency", 2), ger(v("cwger_ostpolitik", 2, show=False))), ai=85),
   O("Not this year.", J(dv_self("cwddr_sed_control", 1), ger("add_political_power = 25")), ai=15)],
  scope="DDR")

E(f"{EVD}.5", "Raise the Minimum Exchange?",
  "Every visitor from the West must exchange a fixed sum of D-Marks at a rate of one to one. Raising it would bring in hard currency - and keep pensioners from Hanover away from their relatives in Halle.",
  "GFX_euro",
  [O("Double it to 25 marks.", J(dv_self("cwddr_hard_currency", -5), dv_self("cwddr_west_media", -3), dv_self("cwddr_sed_control", 2), ger(v("cwger_ostpolitik", -5))), ai=70),
   O("Leave it as it is.", J(dv_self("cwddr_hard_currency", 2), ger(v("cwger_ostpolitik", 2))), ai=30)],
  scope="DDR")

E(f"{EVD}.6", "Biermann in Cologne",
  "The singer Wolf Biermann has been allowed to perform in Cologne - and the concert was broadcast by the WDR to the whole GDR. The Politburo considers withdrawing his citizenship.",
  "GFX_Good_bye_lenin",
  [O("Expatriate him.", J(dv_self("cwddr_opposition", 4), dv_self("cwddr_west_media", 3), dv_self("cwddr_sed_control", 2)), ai=80),
   O("Let him come home and sing.", J(dv_self("cwddr_opposition", 6), dv_self("cwddr_sed_control", -4)), ai=20)],
  scope="DDR")

E(f"{EVD}.8", "The General Secretary on the Rhine",
  "Erich Honecker is received in Bonn with military honours, the GDR flag and the GDR anthem. He visits his birthplace in the Saarland. Kohl's speech at the dinner speaks of unity and freedom - and is broadcast live in the East.",
  "GFX_handshake_black",
  [O("Promise travel relief in return.", J(dv_self("cwddr_exit_pressure", -3), dv_self("cwddr_west_media", 2), dv_self("cwddr_recognition", 10), dv_self("cwddr_hard_currency", -2)), ai=60),
   O("Recognition. Nothing else.", J(dv_self("cwddr_recognition", 15), dv_self("cwddr_sed_control", 3), ger(v("cwger_ostpolitik", -3))), ai=40)],
  scope="DDR")

E(f"{EVD}.10", "'Willy Brandt ans Fenster!'",
  "When the West German chancellor arrives at the Erfurter Hof hotel, thousands break through the police lines and call for him to show himself at the window. The Stasi brings in trucks of loyal cadres for the next day.",
  "GFX_politics_protest",
  [O("Hold the crowds back.", J(dv_self("cwddr_sed_control", 2), dv_self("cwddr_opposition", 1)), ai=70),
   O("Let them cheer. It changes nothing.", J(dv_self("cwddr_exit_pressure", 3), dv_self("cwddr_west_media", 2)), ai=30)],
  scope="DDR")

E(f"{EVD}.11", "The Basic Treaty",
  "Two German states, good-neighbourly relations, permanent missions. The GDR wins the recognition it has wanted for twenty years - and opens its border a crack for journalists, visitors and the telephone.",
  "GFX_treaty",
  [O("Sign - and demarcate.", J(f"add_ideas = {P}_idea_ddr_abgrenzung", dv_self("cwddr_sed_control", 4), dv_self("cwddr_west_dependency", 3)), ai=70),
   O("Sign and open a little.", J(dv_self("cwddr_west_media", 4), dv_self("cwddr_exit_pressure", 2), dv_self("cwddr_west_dependency", 5), "add_stability = 0.02"), ai=30)],
  scope="DDR")

# ====================================================================== the crisis
E(f"{EVD}.30", "The Exit Wave",
  "Applications to leave the country pile up at the district councils. Thousands of young families who have nothing to lose have stopped hiding that they want to go. They gather in churches, wear white ribbons, and some climb the fences of West German embassies.",
  "GFX_gdrfromexitsov",
  [O("Open the valve: let the applicants go.", J(dv_self("cwddr_exit_pressure", -10), dv_self("cwddr_opposition", -3), dv_self("cwddr_recognition", -3), ger(transfer(15000))), ai=50),
   O("Seal the borders to the socialist neighbours.", J(dv_self("cwddr_sed_control", 5), dv_self("cwddr_opposition", 5), dv_self("cwddr_exit_pressure", 3)), ai=50)],
  scope="DDR")

E(f"{EVD}.31", "Monday Demonstrations",
  "", "GFX_politics_protest",
  [O("Dialogue. The old man must go.", J(f"if = {{ limit = {{ check_variable = {{ cwddr_leader < 2 }} }} {ddr_leader('krenz', 2)} }}",
     dv_self("cwddr_sed_control", -6), dv_self("cwddr_opposition", 5), fire(f"{EVD}.32", 25)),
     ai="base = 50 modifier = { factor = 2 check_variable = { cwddr_moscow_backing < 40 } }"),
   O("The Chinese solution.", J(f"{P}_ddr_crackdown_roll = yes", tt(f"{P}_tt_crackdown", "The outcome depends on §YMoscow's guarantee§!, §YSED control§! and the size of the §Yopposition§!.")),
     ai="base = 25 modifier = { factor = 3 check_variable = { cwddr_moscow_backing > 65 } } modifier = { factor = 0.2 check_variable = { cwddr_moscow_backing < 35 } }"),
   O("Open the border before it is opened for us.", f"{P}_wall_opens = yes", ai=10)],
  descs=[(None, "Leipzig, Monday evening, after the peace prayer in the Nikolaikirche: seventy thousand people walk around the ring road with candles. 'We are the people!' Combat groups and riot police wait in the side streets. Blood plasma has been delivered to the hospitals.\n\nMoscow's guarantee: §Y[?cwddr_moscow_backing|0]§! | SED control: §Y[?cwddr_sed_control|0]§! | Opposition: §Y[?cwddr_opposition|0]§!")],
  scope="DDR")

E(f"{EVD}.32", "The Press Conference",
  "Politburo member Günter Schabowski reads a note about new travel regulations to the international press. Asked when they take effect, he shuffles his papers: 'As far as I know... immediately, without delay.' By midnight, tens of thousands stand at Bornholmer Straße.",
  "GFX_egon_krenz_ddr",
  [O("Open the gates.", f"{P}_wall_opens = yes")],
  scope="DDR", trig=f"NOT = {{ has_global_flag = {P}_wall_open }}")

E(f"{EVD}.33", "The Wall Is Open",
  "The Party has lost the street, the border and its fear. Hans Modrow, the reformer from Dresden, becomes chairman of the Council of Ministers. At a round table in a Protestant community centre, the SED, the bloc parties and the new citizens' movements negotiate free elections.",
  "GFX_gdrfromexitsov",
  [O("Modrow forms a government.", J(ddr_leader("modrow", 3), f"add_ideas = {P}_idea_ddr_round_table", "set_variable = { cwddr_wende_stage = 4 }", fire(f"{EVD}.36", 120)), ai=80),
   O("Krenz holds on.", J(f"if = {{ limit = {{ check_variable = {{ cwddr_leader < 2 }} }} {ddr_leader('krenz', 2)} }}", dv_self("cwddr_opposition", 10), dv_self("cwddr_sed_control", -10),
     f"add_ideas = {P}_idea_ddr_round_table", "set_variable = { cwddr_wende_stage = 4 }", fire(f"{EVD}.36", 90)), ai=20)],
  scope="DDR")

E(f"{EVD}.34", "Order Restored",
  "Tanks on Karl-Marx-Platz. The demonstrators are dispersed; hundreds are arrested, an unknown number dead. The West German television teams are expelled. The SED has won the night and lost the country.",
  "GFX_gdratwarsov",
  [O("Socialism is safe.", J("add_stability = -0.05", dv_self("cwddr_recognition", -15), dv_self("cwddr_west_media", -5)))],
  scope="DDR")

E(f"{EVD}.35", "Bonn's Plan for Unity",
  "The federal government has published a plan: free elections in the GDR, then 'confederative structures', then a federation. Nobody in East Berlin was consulted.",
  "GFX_politics_talks",
  [O("A treaty community between two states - no more.", J(dv_self("cwddr_sed_control", 2), ger(f"set_country_flag = {P}_confederation_offered"),
     tt(f"{P}_tt_confed_ddr", "The Federal Republic may now choose a §Yconfederation§!.")), ai=60),
   O("The plan is the only way out.", J(dv_self("cwddr_sed_control", -5), ger(v("cwger_unity", 10))), ai=40)],
  scope="DDR")

E(f"{EVD}.36", "Free Elections to the Volkskammer",
  "", "GFX_election_day",
  [O("The Alliance for Germany governs.", J(ddr_leader("demaiziere", 4), "set_politics = { ruling_party = democratic elections_allowed = yes }",
     "set_popularities = { democratic = 75 communism = 17 fascism = 0 neutrality = 6 nationalist = 2 }", ger(v("cwger_unity", 15))), trig=f"has_country_flag = {P}_ddr_result_alliance"),
   O("The Social Democrats of the East govern.", J(ddr_leader("demaiziere", 4), "set_politics = { ruling_party = democratic elections_allowed = yes }",
     "set_popularities = { democratic = 70 communism = 20 fascism = 0 neutrality = 8 nationalist = 2 }", ger(v("cwger_unity", 8))), trig=f"has_country_flag = {P}_ddr_result_spd"),
   O("The citizens' movements and the reformed PDS govern.", J(ddr_leader("modrow", 3), "set_popularities = { democratic = 45 communism = 35 fascism = 0 neutrality = 18 nationalist = 2 }",
     ger(f"set_country_flag = {P}_confederation_offered"), ger(v("cwger_unity", -5))), trig=f"has_country_flag = {P}_ddr_result_civic")],
  descs=[(f"has_country_flag = {P}_ddr_result_alliance", "Ninety-three percent turnout. The conservative Alliance for Germany, promised the D-Mark and unity by Helmut Kohl's rallies, wins almost half the vote. Lothar de Maizière, a viola player and church lawyer, becomes the GDR's first and last freely elected prime minister."),
         (f"has_country_flag = {P}_ddr_result_spd", "The newly founded East German SPD wins in the old social-democratic heartlands of Saxony and Thuringia. A grand coalition under a Christian Democrat prime minister is formed - unity, but at a slower pace."),
         (f"has_country_flag = {P}_ddr_result_civic", "Neues Forum, Bündnis 90 and the PDS together hold a majority. The GDR's voters want democracy - but not, it seems, to be absorbed by the Federal Republic. A 'third way' government takes office.")],
  imm=f"""set_variable = {{ cwddr_wende_stage = 5 }}
	random_list = {{
		50 = {{ modifier = {{ add = 20 GER = {{ check_variable = {{ cwger_unity > 40 }} }} }} modifier = {{ add = 15 GER = {{ has_completed_focus = {P}_ten_point_plan }} }} set_country_flag = {P}_ddr_result_alliance }}
		30 = {{ set_country_flag = {P}_ddr_result_spd }}
		20 = {{ modifier = {{ add = 15 GER = {{ has_country_flag = {P}_confederation_offered }} }} modifier = {{ add = 10 check_variable = {{ cwddr_opposition > 70 }} }} set_country_flag = {P}_ddr_result_civic }}
	}}
	{fire(f"{EVG}.135", 10, target="GER")}""",
  scope="DDR")

E(f"{EVD}.37", "Accession to the Federal Republic",
  "The Federal Republic proposes that the GDR's Länder accede to the area of the Basic Law. The Volkskammer must vote. A yes means the end of the state; a no means another winter of uncertainty.",
  "GFX_german_parliament",
  [O("The Volkskammer votes for accession.", J(ger(f"{P}_request_two_plus_four = yes"), tt(f"{P}_tt_accession", "The Four Powers must now agree in §YTwo Plus Four§! talks.")),
     ai="base = 80 modifier = { factor = 0.25 has_country_flag = " + P + "_ddr_result_civic }"),
   O("Not like this.", fire(f"{EVG}.137", 2, target="GER"), ai="base = 20 modifier = { factor = 3 has_country_flag = " + P + "_ddr_result_civic }")],
  scope="DDR")

E(f"{EVD}.38", "The Second Wave",
  "The fear has worn off. After years of silence the churches are full again, and on Mondays people walk around the ring road once more - more of them than before the massacre.",
  "GFX_politics_protest",
  [O("Here we go again.", J(dv_self("cwddr_opposition", 5), fire(f"{EVD}.31", 10)))],
  scope="DDR")

E(f"{EVD}.39", "The Troops Refuse",
  "The order to clear the ring road was given - and not carried out. Officers of the National People's Army refused to fire on their own people; the Soviet garrison stayed in its barracks. The Politburo has run out of options.",
  "GFX_gdratwarsov",
  [O("Then the border must open.", J(dv_self("cwddr_sed_control", -15), f"{P}_wall_opens = yes"))],
  scope="DDR")

# ====================================================================== Bonn's side
# IMPERIA CW — Cold War: reception costs follow a completed population transfer.
EXODUS_SUCCESS = J(money_gdp(-0.001), v("cwger_unity", 5), dv("cwddr_exit_pressure", 5))
E(f"{EVG}.130", "The Exodus",
  "East Germans are leaving through every crack in the Iron Curtain: through Hungary, through the embassy in Prague, through the permanent mission in East Berlin. Reception camps in Gießen and Marienfelde overflow.\n\nGDR crisis index: §Y[?DDR.cwddr_crisis|0]§!",
  "GFX_German_migrant",
  [O("Take them all in. They are Germans.", J(transfer(20000), f"if = {{ limit = {{ check_variable = {{ cwger_ue_arrived > 0 }} }} {EXODUS_SUCCESS} }}"), ai=60),
   O("Quiet diplomacy. Do not destabilise the East.", J(v("cwger_ostpolitik", 3), v("cwger_unity", -2), dv("cwddr_exit_pressure", -3)), ai=40)])

E(f"{EVG}.131", "Massacre in Leipzig",
  "The pictures smuggled out are blurred but unmistakable: armoured vehicles, water cannon, men with truncheons in front of the opera house. The GDR has chosen the Chinese solution.",
  "GFX_gdratwarsov",
  [O("Sanctions against the regime.", J("if = { limit = { country_exists = DDR } DDR = { ROOT = { " + P + "_sanction_prev_economic = yes } } }", tension(4), v("cwger_ostpolitik", -10),
     dv("cwddr_hard_currency", 8), f"add_ideas = {P}_idea_second_cold_war"), ai=50),
   O("Keep the channels open - for the prisoners' sake.", J(v("cwger_ostpolitik", -4), stab(-0.03), party("greens", 0.003)), ai=50)])

E(f"{EVG}.133", "The Wall Has Fallen",
  "People dance on the Wall at the Brandenburg Gate. Trabants queue at the crossing points, West Berliners hand out bananas and champagne, strangers embrace. 'Now what belongs together will grow together,' says Willy Brandt.",
  "GFX_new_year_germany",
  [O("'We are one people!'", J(v("cwger_unity", 20), v("cwger_berlin_access", 40), stab(0.05), "add_political_power = 100", party("cdu", 0.006)), ai=70),
   O("Step by step. Nobody must feel overrun.", J(v("cwger_unity", 8), v("cwger_berlin_access", 40), v("cwger_ostpolitik", 5), stab(0.04), party("spd", 0.004)), ai=30)],
  imm="every_other_country = { limit = { is_ai = no NOT = { original_tag = DDR } } country_event = { id = " + EVG + ".134 days = 1 } }")

E(f"{EVG}.134", "The Berlin Wall Falls",
  "The border between the two German states is open. The world watches crowds with hammers and chisels chip away at the most famous wall in the world.",
  "GFX_new_year_germany", [O("A new era.")], scope="ANY")

E(f"{EVG}.135", "The Road to German Unity",
  "The GDR has a freely elected government. Now the questions that were theoretical for forty years need answers within months: accession under Article 23 or a new constitution under Article 146? Unity inside NATO, or neutrality? Or two states under one roof?\n\nUnity momentum: §Y[?cwger_unity|0]§!",
  "GFX_germany_flag",
  [O("Accession under Article 23.", J("set_variable = { cwger_unity_path = 1 }", fire(f"{EVD}.37", 3, target="DDR")),
     ai="base = 60 modifier = { factor = 2 check_variable = { cwger_unity > 50 } }"),
   O("A constitution for all Germans (Article 146).", J("set_variable = { cwger_unity_path = 2 }", fire(f"{EVD}.37", 3, target="DDR")),
     trig=f"has_country_flag = {P}_art146_prepared", ai=25),
   O("A German confederation.", f"{P}_confederation = yes", trig=f"has_country_flag = {P}_confederation_offered",
     ai="base = 10 modifier = { factor = 4 check_variable = { cwger_unity < 30 } }"),
   O("Unity in neutrality.", f"{P}_unity_neutral = yes", trig=f"has_country_flag = {P}_neutrality_accepted", ai=10),
   O("Not yet.", J(f"set_country_flag = {P}_unity_postponed",
     tt(f"{P}_tt_postponed", "The §YReopen Unity Talks§! decision becomes available.")), ai=1)])

E(f"{EVG}.137", "The Volkskammer Says No",
  "East Berlin will not simply accede. The new government wants negotiations between equals, a currency union on its own terms and protection for East German property.",
  "GFX_german_parliament",
  [O("Then a confederation.", J(f"{P}_confederation = yes"), ai=40),
   O("We will try again.", J(f"set_country_flag = {P}_unity_postponed", v("cwger_unity", -5)), ai=60)])

E(f"{EVG}.140", "Two Plus Four",
  "The two German states have agreed on unity. Now the victors of 1945 must give up their rights over Germany as a whole. Washington wants a united Germany in NATO. Our generals want the GDR. Bonn offers money - a great deal of money.\n\nThe GDR's dependence on our guarantee: §Y[?DDR.cwddr_moscow_backing|0]§!",
  "GFX_treaty",
  [O("Agree - for the price of the withdrawal.", J("FROM = { country_event = { id = " + EVG + ".141 days = 2 } }", money(5), tension(-4)),
     ai="base = 40 modifier = { factor = 3 has_completed_focus = COLDWAR_SOV_gor_the_sinatra_doctrine } modifier = { factor = 2 has_completed_focus = COLDWAR_SOV_gor_new_thinking } modifier = { factor = 0.3 DDR = { check_variable = { cwddr_moscow_backing > 60 } } }"),
   O("Only a neutral Germany.", J("FROM = { set_country_flag = " + P + "_soviets_want_neutrality country_event = { id = " + EVG + ".142 days = 2 } }"), ai=35),
   O("Nyet.", J("FROM = { set_country_flag = " + P + "_soviets_refused country_event = { id = " + EVG + ".143 days = 2 } }", tension(5)),
     ai="base = 15 modifier = { factor = 4 has_global_flag = " + P + "_moscow_coup_succeeded } modifier = { factor = 3 has_completed_focus = COLDWAR_SOV_the_brezhnev_doctrine } modifier = { factor = 0 has_completed_focus = COLDWAR_SOV_gor_the_sinatra_doctrine }")],
  scope="SOV")

E(f"{EVG}.141", "The Treaty on the Final Settlement",
  "Moscow agrees. Germany will be united and fully sovereign, inside NATO, with an army of no more than 370,000, no nuclear, biological or chemical weapons, and the Oder-Neisse border for ever. The Soviet troops will leave by 1994 - and Bonn will pay for their new barracks.",
  "GFX_treaty",
  [O("The 3rd of October will be German Unity Day.", J(money_gdp(-0.006), f"{P}_complete_unity = yes"))])

E(f"{EVG}.142", "Moscow Demands Neutrality",
  "The Soviet foreign minister's message is plain: a united Germany, yes - but outside the alliances, like Austria. Washington warns that neutrality would mean the end of NATO in Europe.",
  "GFX_politics_talks",
  [O("Accept. Unity matters more than the alliance.", J(f"set_country_flag = {P}_neutrality_accepted", f"{P}_unity_neutral = yes",
     "USA = { add_opinion_modifier = { target = ROOT modifier = large_decrease } }"), ai=20),
   O("A confederation instead.", f"{P}_confederation = yes", trig="country_exists = DDR", ai=30),
   O("Refuse and wait.", J(f"set_country_flag = {P}_unity_postponed", v("cwger_westbindung", 4)), ai=50)])

E(f"{EVG}.143", "Moscow Says No",
  "The Soviet Union will not give up the GDR. Its troops stay, its veto stands. The Wall is open, but the border of the blocs runs on through Germany.",
  "GFX_missiles_on_road",
  [O("A confederation the Soviets can tolerate.", f"{P}_confederation = yes", trig="country_exists = DDR", ai=50),
   O("Wait for a better moment.", J(f"set_country_flag = {P}_unity_postponed", v("cwger_westbindung", 5), tension(2)), ai=50)])

E(f"{EVG}.145", "Coup in Moscow",
  "Tanks in the streets of Moscow, a state of emergency, the general secretary 'unwell' at his dacha. The hardliners have taken power - and they have announced that the 'counter-revolution' in the GDR will not be allowed to stand.",
  "GFX_missiles_on_road",
  [O("The window is closing.", J(v("cwger_westbindung", 6), stab(-0.04), ws(0.05)))])

E(f"{EVG}.150", "Germany Is United",
  "At midnight the flag of the Federal Republic rises in front of the Reichstag. Germany, divided since 1945, is a single state again - and the largest country in Western Europe.",
  "GFX_germany_flag", [O("A new Germany in Europe.")], scope="ANY")
