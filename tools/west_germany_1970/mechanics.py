"""Player-facing mechanics for West Germany 1970.

Missions (timed decisions), the spy war, abuses of the security state, the flow of
Übersiedler from the GDR, the cost of the East, the Bundesrat and a Western-integration
crisis. Everything here runs on top of the meters in systems.py.
"""
from cw_lib import *
from events_lib import E, O, fire, EXTRA_EFFECTS
from decisions import D, M, DP, PO, SE, EC
from systems import DDR_LEADERS  # noqa: F401  (keeps import order stable)

# ============================================================== monthly tick
FLOW = [  # (minimum GDR exit pressure, people per month, thousands added to the counter)
    (70, 6000, 6), (50, 3000, 3), (30, 1500, 1.5), (0, 600, 0.6)]


def _flow_chain():
    """DDR scope: people leave every month; the West gains workers."""
    parts = []
    for i, (lim, people, k) in enumerate(FLOW):
        # half find work at once, the other half enters the Imperia refugee accounting
        # (reception costs and gradual integration through imp_refugee_cost_calc)
        body = (f"add_manpower = -{people} GER = {{ add_manpower = {people // 2} add_to_variable = {{ cwger_uebersiedler_k = {k} }} "
                f"add_to_variable = {{ imp_refugees_taken_k = {k / 2} }} }}")
        if i == 0:
            parts.append(f"if = {{ limit = {{ check_variable = {{ cwddr_exit_pressure > {lim - 1} }} }} {body} }}")
        elif lim:
            parts.append(f"else_if = {{ limit = {{ check_variable = {{ cwddr_exit_pressure > {lim - 1} }} }} {body} }}")
        else:
            parts.append(f"else = {{ {body} }}")
    return "DDR = {\n" + "\n".join(parts) + "\n}"


EXTRA_EFFECTS.append(f"""
# Monthly, GER scope: the mechanics the player interacts with through missions and decisions.
{P}_mechanics_tick = {{
	# --- Übersiedler: people leaving the GDR legally or through the cracks
	if = {{
		limit = {{ country_exists = DDR NOT = {{ has_global_flag = {P}_unity_achieved }} }}
		if = {{
			limit = {{ has_global_flag = {P}_wall_open NOT = {{ has_global_flag = {P}_confederation }} }}
			add_manpower = 15000
			add_to_variable = {{ cwger_uebersiedler_k = 30 }}
			add_to_variable = {{ imp_refugees_taken_k = 15 }}
			DDR = {{ add_manpower = -30000 }}
			{money_gdp(-0.0004).replace(chr(10), ' ')}
		}}
		else = {{
			{_flow_chain()}
		}}
	}}
	# --- the spy war: contacts with the East open doors, counter-intelligence decays without money
	add_to_variable = {{ cwger_stasi_penetration = 0.1 }}
	if = {{ limit = {{ check_variable = {{ cwger_ostpolitik > 50 }} }} add_to_variable = {{ cwger_stasi_penetration = 0.15 }} }}
	if = {{ limit = {{ has_global_flag = {P}_unity_achieved }} add_to_variable = {{ cwger_stasi_penetration = -1.5 }} }}
	add_to_variable = {{ cwger_counterintel = -0.15 }}
	clamp_variable = {{ var = cwger_stasi_penetration min = 0 max = 100 }}
	clamp_variable = {{ var = cwger_counterintel min = 0 max = 100 }}
	if = {{
		limit = {{ check_variable = {{ cwger_stasi_penetration > 30 }} NOT = {{ has_country_flag = {P}_spy_cooldown }} NOT = {{ has_global_flag = {P}_unity_achieved }} }}
		random_list = {{
			92 = {{ }}
			8 = {{
				modifier = {{ add = 4 check_variable = {{ cwger_stasi_penetration > 50 }} }}
				modifier = {{ add = 4 check_variable = {{ cwger_counterintel > 50 }} }}
				set_country_flag = {{ flag = {P}_spy_cooldown days = 270 value = 1 }}
				country_event = {{ id = {EVG}.70 days = 1 }}
			}}
		}}
	}}
	# --- MD protest system: mass movements put people on the streets
	if = {{ limit = {{ check_variable = {{ cwger_peace_movement > 50 }} }} {protest(0.5).replace(chr(10), ' ')} }}
	if = {{ limit = {{ check_variable = {{ cwger_anti_nuclear > 40 }} }} {protest(0.3).replace(chr(10), ' ')} }}
	# --- MD corruption: entrenched corruption keeps the scandal machine running
	if = {{ limit = {{ OR = {{ has_idea = corruption_level_04 has_idea = corruption_level_05 has_idea = corruption_level_06 has_idea = corruption_level_07 }} }} add_to_variable = {{ cwger_scandal = 0.4 }} }}
	# --- the euro: founded by a focus, introduced through the MD EU system once it exists
	if = {{
		limit = {{ has_completed_focus = {P}_euro_founder date > 1998.12.31 NOT = {{ has_country_flag = EU_joined_the_eurozone }} }}
		joining_the_euro = yes
	}}
	# --- the security state overreaches
	if = {{
		limit = {{ check_variable = {{ cwger_security > 64 }} NOT = {{ has_country_flag = {P}_abuse_cooldown }} }}
		random_list = {{
			94 = {{ }}
			6 = {{
				modifier = {{ add = 6 check_variable = {{ cwger_security > 80 }} }}
				set_country_flag = {{ flag = {P}_abuse_cooldown days = 540 value = 1 }}
				country_event = {{ id = {EVG}.75 days = 1 }}
			}}
		}}
	}}
	# --- the cost of the East: transfers paid every month, shrinking as the new Länder catch up
	if = {{
		limit = {{ check_variable = {{ cwger_east_burden > 0 }} }}
		set_temp_variable = {{ treasury_change = gdp_total }}
		multiply_temp_variable = {{ treasury_change = cwger_east_burden }}
		multiply_temp_variable = {{ treasury_change = -0.00002 }}
		modify_treasury_effect = yes
		add_to_variable = {{ cwger_east_burden = -0.25 }}
		clamp_variable = {{ var = cwger_east_burden min = 0 max = 100 }}
	}}
	# --- drifting away from the West
	if = {{
		limit = {{ check_variable = {{ cwger_westbindung < 30 }} NOT = {{ has_country_flag = {P}_westbindung_crisis_seen }} NOT = {{ has_global_flag = {P}_unity_neutral }} }}
		set_country_flag = {P}_westbindung_crisis_seen
		country_event = {{ id = {EVG}.79 days = 2 }}
	}}
	# --- the Soviet gas deal meets an American embargo
	if = {{
		limit = {{ OR = {{ has_idea = {P}_idea_soviet_gas has_idea = COLDWAR_SOV_soviet_gas has_global_flag = COLDWAR_SOV_pipelines_to_europe_signed }} date > 1981.12.1 date < 1984.1.1 NOT = {{ has_country_flag = {P}_pipeline_embargo_seen }} }}
		set_country_flag = {P}_pipeline_embargo_seen
		country_event = {{ id = {EVG}.86 days = 5 }}
	}}
	# --- Bielefeld: a pacifist party goes to war
	if = {{
		limit = {{ date > 1999.3.24 has_completed_focus = {P}_kosovo_decision is_in_array = {{ gov_coalition_array = 17 }} NOT = {{ has_country_flag = {P}_bielefeld_seen }} }}
		set_country_flag = {P}_bielefeld_seen
		country_event = {{ id = {EVG}.98 days = 10 }}
	}}
}}

# GER scope: count a vote won back (or bought) and recalculate the majority.
{P}_win_vote = {{
	add_to_variable = {{ cwger_defectors = -1 }}
	clamp_variable = {{ var = cwger_defectors min = -6 max = 20 }}
	{P}_update_bundestag = yes
}}
""")

# ============================================================== events
E(f"{EVG}.19", "The Majority Is Crumbling",
  "Deputies are leaving the coalition, or the arithmetic of the last election never quite worked. The opposition smells a constructive vote of no confidence. The whips have weeks, not months.\n\n"
  "Government §Y[?cwger_seats_gov|0]§! of §Y[?cwger_seats_total|0]§! seats, majority §Y[?cwger_majority|0]§!, defectors §Y[?cwger_defectors|0]§!.",
  "GFX_bundestag",
  [O("Count every vote.", tt(f"{P}_tt_majority_mission", "A §Ymission§! starts: restore a majority of at least three seats within 90 days, or the opposition calls the vote. Use the §YBonn Politics§! decisions."))])

E(f"{EVG}.70", "", "", "", [O("ok")], hidden=True,
  imm=f"""random_list = {{
	30 = {{ modifier = {{ add = 30 check_variable = {{ cwger_counterintel > cwger_stasi_penetration }} }} {fire(f"{EVG}.71", 1)} }}
	30 = {{ modifier = {{ add = 25 check_variable = {{ cwger_stasi_penetration > 55 }} }} modifier = {{ factor = 0.5 check_variable = {{ cwger_counterintel > 60 }} }} {fire(f"{EVG}.72", 1)} }}
	20 = {{ {fire(f"{EVG}.73", 1)} }}
	5 = {{ modifier = {{ add = 15 DDR = {{ check_variable = {{ cwddr_crisis > 40 }} }} }} modifier = {{ factor = 0 NOT = {{ country_exists = DDR }} }} {fire(f"{EVG}.74", 1)} }}
}}""")

E(f"{EVG}.71", "A Mole Unmasked",
  "The Federal Office for the Protection of the Constitution has arrested an official who has passed files to the Ministry for State Security for years. The radio messages, the microdots, the dead drops on the Rhine promenade - all in the arrest report.",
  "GFX_der_Spiegel",
  [O("A quiet trial and a quiet exchange later.", J(v("cwger_stasi_penetration", -8), v("cwger_counterintel", 3), pp(25)), ai=60),
   O("A public trial. Everyone should know.", J(v("cwger_stasi_penetration", -10), v("cwger_ostpolitik", -4), dv("cwddr_recognition", -3), tension(1)), ai=40)])

E(f"{EVG}.72", "NATO Plans in East Berlin",
  "Material from the defence ministry has turned up in the files of the Warsaw Pact: deployment plans, codes, the timetable of the next exercise. Somewhere in Bonn sits a source the services have not found.",
  "GFX_GER_MAD",
  [O("Damage control in Brussels.", J(pp(-50), v("cwger_westbindung", -3), v("cwger_counterintel", 4),
     "if = { limit = { country_exists = SOV } SOV = { add_tech_bonus = { name = " + P + "_bonus bonus = 0.5 uses = 1 category = CAT_command_and_control_equipment } } }"), ai=60),
   O("Blame the previous government.", J(v("cwger_scandal", 10), party("cdu", -0.003), party("spd", -0.003),
     "if = { limit = { country_exists = SOV } SOV = { add_tech_bonus = { name = " + P + "_bonus bonus = 0.5 uses = 1 category = CAT_command_and_control_equipment } } }"), ai=40)])

E(f"{EVG}.73", "The Romeo Affair",
  "A secretary in the Foreign Office has fallen in love with a charming man from Düsseldorf who turns out to be a captain of the HVA. Her lover has vanished; the magazines have the pictures.",
  "GFX_Der_stern",
  [O("Tighten the security vetting of staff.", J(v("cwger_stasi_penetration", -5), v("cwger_counterintel", 3), v("cwger_rechtsstaat", -1)), ai=60),
   O("Let the courts handle it.", J(v("cwger_stasi_penetration", -3), v("cwger_scandal", 6)), ai=40)])

E(f"{EVG}.74", "A Defector from the HVA",
  "An officer of the GDR's foreign intelligence has walked into a West German police station with two suitcases of files. Dozens of agents in the Federal Republic have names now.",
  "GFX_egon_krenz_ddr",
  [O("Roll up the network.", J(v("cwger_stasi_penetration", -18), v("cwger_counterintel", 8), dv("cwddr_sed_control", -3), pp(50)), ai=70),
   O("Keep him secret and feed the HVA false trails.", J(v("cwger_stasi_penetration", -10), v("cwger_counterintel", 14)), ai=30)])

E(f"{EVG}.75", "", "", "", [O("ok")], hidden=True,
  imm=f"""random_list = {{
	10 = {{ modifier = {{ factor = 0 has_country_flag = {P}_abuse_traube }} set_country_flag = {P}_abuse_traube {fire(f"{EVG}.76", 1)} }}
	10 = {{ modifier = {{ factor = 0 has_country_flag = {P}_abuse_celle }} set_country_flag = {P}_abuse_celle {fire(f"{EVG}.77", 1)} }}
	10 = {{ modifier = {{ factor = 0 has_country_flag = {P}_abuse_kiessling }} set_country_flag = {P}_abuse_kiessling {fire(f"{EVG}.78", 1)} }}
	2 = {{ {v("cwger_scandal", 8, show=False)} }}
}}""")

E(f"{EVG}.76", "The Traube Affair",
  "Der Spiegel reveals that the Office for the Protection of the Constitution broke into the flat of a nuclear scientist and bugged it - without a warrant, on the minister's say-so, because he once met a man who knew a terrorist.",
  "GFX_der_Spiegel",
  [O("The interior minister resigns.", J(v("cwger_security", -6), v("cwger_rechtsstaat", 3), v("cwger_scandal", 6), pp(-50)), ai=60),
   O("Security comes first.", J(v("cwger_rechtsstaat", -6), v("cwger_scandal", 12), v("cwger_raf_milieu", 3), party("fdp", -0.003)), ai=40)])

E(f"{EVG}.77", "The Celle Hole",
  "Eight years ago the secret service blew a hole in the wall of Celle prison and blamed the RAF - to smuggle an informant into the scene. Now a reporter has the files.",
  "GFX_Polizeiabsperrung",
  [O("A parliamentary inquiry.", J(v("cwger_rechtsstaat", -3), v("cwger_security", -4), v("cwger_scandal", 10), pp(-25)), ai=60),
   O("National security - no comment.", J(v("cwger_rechtsstaat", -8), v("cwger_scandal", 15), v("cwger_raf_milieu", 4)), ai=40)])

E(f"{EVG}.78", "The Kießling Affair",
  "The Military Counter-Intelligence Service has driven a four-star general out of office on the strength of rumours from a Cologne bar. The rumours were false. The defence minister offers to resign.",
  "GFX_GER_MAD",
  [O("Accept the resignation and rehabilitate the general.", J(v("cwger_scandal", 5), v("cwger_rechtsstaat", 2), "army_experience = -5", pp(-40)), ai=50),
   O("Keep the minister.", J(v("cwger_scandal", 14), v("cwger_rechtsstaat", -3), stab(-0.01)), ai=50)])

E(f"{EVG}.79", "Is Bonn Drifting?",
  "Washington asks whether the Federal Republic is still an ally. Paris worries about a German Rapallo. In Moscow, analysts write that Bonn can be pried loose from the West.\n\nWestern integration: §Y[?cwger_westbindung|0]§!",
  "GFX_Ami_go_home",
  [O("Reassure the allies.", J(v("cwger_westbindung", 15), v("cwger_peace_movement", 5), "USA = { add_opinion_modifier = { target = ROOT modifier = medium_increase } }"), ai=80),
   O("Equidistance between the blocs.", J(v("cwger_westbindung", -10), tension(-3), "USA = { add_opinion_modifier = { target = ROOT modifier = large_decrease } }",
     f"if = {{ limit = {{ has_global_flag = mdcw_cw_initialized }} set_temp_variable = {{ mdcw_cw_new_alignment = 0 }} set_temp_variable = {{ mdcw_cw_t_free = 1 }} mdcw_cw_change_alignment = yes }}",
     "if = { limit = { has_idea = NATO_member } NATO_leave = yes }", europe(-10),
     tt(f"{P}_tt_equidistance", "The Federal Republic leaves NATO and the Western bloc and becomes §Ynon-aligned§! in the Imperia Cold War system.")), ai=5)])

E(f"{EVG}.86", "The Pipeline Embargo",
  "Washington has banned American firms and their licensees from supplying the Siberian gas pipeline. AEG, Mannesmann and their subcontractors face sanctions in the United States if they deliver the turbines Bonn has promised Moscow.",
  "GFX_oil_refinery",
  [O("Deliver anyway. Treaties are kept.", J(v("cwger_westbindung", -6), v("cwger_ostpolitik", 4), faction("bdi", 6), "USA = { add_opinion_modifier = { target = ROOT modifier = medium_decrease } }"), ai=60),
   O("Bow to Washington.", J(v("cwger_westbindung", 5), faction("bdi", -8), money_gdp(-0.002), "SOV = { add_opinion_modifier = { target = ROOT modifier = medium_decrease } }"), ai=40)])

E(f"{EVG}.98", "Bielefeld",
  "The Greens' special congress on the Kosovo war. Outside, protesters scream 'warmonger'; inside, a paint bomb bursts the foreign minister's eardrum. Bleeding, he speaks anyway: 'Never again war - but also never again Auschwitz.'",
  "GFX_joschka_fischer_event",
  [O("The Realos carry the vote.", J(party("greens", -0.006), v("cwger_peace_movement", -4), v("cwger_westbindung", 4)), ai=70),
   O("The party leaves the coalition.", J(party("greens", 0.004), v("cwger_peace_movement", 6), "set_variable = { cwger_defectors = 8 }", f"{P}_update_bundestag = yes"), ai=30)])

# ============================================================== missions and decisions
GOV_SPD = "check_variable = { ruling_party = 3 }"

M(PO, "mission_majority", "Secure the Chancellor's Majority",
  "The government has lost its working majority. Win deputies back - by persuasion, by promises, or by less elegant means - before the opposition tables its motion.",
  "GFX_decision_elections_button", activation=f"has_country_flag = {P}_majority_crisis",
  available="check_variable = { cwger_margin > 2 }", days=90,
  complete=J(f"clr_country_flag = {P}_majority_crisis", pp(25), stab(0.01)),
  timeout=J(f"clr_country_flag = {P}_majority_crisis", fire(f"{EVG}.20", 1)),
  cancel="has_country_flag = elections_in_progress")
D(PO, "whip_waverers", "Win Back the Waverers",
  "Long evenings with the deputies who are thinking of crossing the floor: constituencies, committee chairs, a word from the chancellor.",
  "GFX_decision_negotiate_icon", visible=f"has_country_flag = {P}_majority_crisis", cost=40, re_enable=20,
  effect=J(f"{P}_win_vote = yes", tt(f"{P}_tt_win_vote", "The government gains §Gone vote§!.")), ai=40)
D(PO, "junior_partner_offer", "An Offer to the Junior Partner",
  "Another ministry, a pet project in the budget, a say in the next appointment - whatever keeps the coalition partner's deputies in line.",
  "GFX_decision_negotiate_icon", visible=f"has_country_flag = {P}_majority_crisis NOT = {{ check_variable = {{ gov_coalition_array^num = 0 }} }}",
  cost=60, re_enable=60,
  effect=J(f"{P}_win_vote = yes", f"{P}_win_vote = yes",
           f"if = {{ limit = {{ {GOV_SPD} }} {v('cwger_fdp_course', -8, show=False)} }} else = {{ {v('cwger_fdp_course', 8, show=False)} }}",
           tt(f"{P}_tt_win_two", "The government gains §Gtwo votes§!, and the FDP moves towards the chancellor's party.")), ai=30)
D(PO, "buy_a_deputy", "A Deputy From the Other Side",
  "Persuade an opposition deputy to abstain or cross over. If it ever comes out how, it will be a scandal.",
  "GFX_decision_money_dec", visible=f"has_country_flag = {P}_majority_crisis", cost=75, re_enable=45,
  effect=J(f"{P}_win_vote = yes", "random_list = { 70 = { } 30 = { " + v("cwger_scandal", 15, show=False) + " } }",
           tt(f"{P}_tt_buy_deputy", "The government gains §Gone vote§!. §R30%§!: it leaks (scandal pressure §R+15§!).")), ai=20)
D(PO, "bundesrat_package", "Package Deal with the Länder",
  "Money for the states' pet projects in exchange for their votes in the Bundesrat. The hostile Bundesrat stops blocking the government for a year.",
  "GFX_decision_negotiate_icon", visible=f"has_country_flag = {P}_bundesrat_hostile", cost=60, re_enable=365,
  effect=J(f"set_country_flag = {{ flag = {P}_bundesrat_deal days = 365 value = 1 }}", money_gdp(-0.001),
           tt(f"{P}_tt_bundesrat_deal", "The §RBundesrat blockade§! penalty to political power is lifted for a year.")), ai=25)
D(PO, "peace_dialogue", "Dialogue with the Peace Movement",
  "Invite the organisers of the marches to the chancellery. Listen, explain, give a little.",
  "GFX_decision_propaganda", visible="check_variable = { cwger_peace_movement > 40 }", cost=50, re_enable=365,
  effect=J(v("cwger_peace_movement", -8), v("cwger_westbindung", -2), party("greens", -0.002), protest(-8)), ai=15)

M(SE, "mission_manhunt", "Manhunt",
  "The RAF's underground is growing. Break the commando level before it strikes again.",
  "GFX_decision_generic_intelligence_operation",
  activation=f"check_variable = {{ cwger_terror_left > 45 }} NOT = {{ has_country_flag = {P}_manhunt_cooldown }} NOT = {{ has_country_flag = {P}_raf_dissolved }}",
  available="check_variable = { cwger_raf_cadre < 10 }", days=240,
  complete=J(f"set_country_flag = {{ flag = {P}_manhunt_cooldown days = 365 value = 1 }}", pp(50), v("cwger_security", 3), v("cwger_raf_milieu", -3)),
  timeout=J(f"set_country_flag = {{ flag = {P}_manhunt_cooldown days = 365 value = 1 }}", stab(-0.03),
            f"if = {{ limit = {{ NOT = {{ has_country_flag = {P}_attack_cooldown }} }} {P}_raf_attack = yes }}",
            tt(f"{P}_tt_manhunt_fail", "The commando strikes.")))
M(DP, "mission_reception", "Reception Camps",
  "The GDR is emptying through every crack in the Iron Curtain. Gießen, Marienfelde and Friedland need beds, food and work offices - or the welcome will turn sour.",
  "GFX_decision_germany",
  activation=f"country_exists = DDR DDR = {{ check_variable = {{ cwddr_wende_stage > 0 }} check_variable = {{ cwddr_wende_stage < 4 }} }} NOT = {{ has_country_flag = {P}_reception_done }}",
  available=f"has_country_flag = {P}_reception_ready", days=180,
  complete=J(f"set_country_flag = {P}_reception_done", stab(0.03), v("cwger_unity", 5)),
  timeout=J(f"set_country_flag = {P}_reception_done", stab(-0.04), party("rep", 0.004), v("cwger_terror_right", 4)), good=True)
D(DP, "build_reception", "Expand the Reception Camps",
  "Barracks, schools and gyms turned into dormitories; job centres open on Sundays.",
  "GFX_decision_generic_factory",
  visible=f"country_exists = DDR NOT = {{ has_country_flag = {P}_reception_done }} NOT = {{ has_country_flag = {P}_reception_ready }}",
  cost=50, once=True, effect=J(money_gdp(-0.002), f"set_country_flag = {P}_reception_ready", "add_manpower = 5000"), ai=40)
D(DP, "integration_programme", "Integration Programme for Übersiedler",
  "Housing credits, recognition of East German qualifications, language for those who came via Hungary with nothing but a bag.",
  "GFX_decision_generic_factory", visible="check_variable = { cwger_uebersiedler_k > 40 }", cost=50, re_enable=730,
  effect=J(money_gdp(-0.001), stab(0.02), v("cwger_terror_right", -3), party("rep", -0.002)), ai=15)
D(DP, "solidarity_pact", "The Solidarity Pact",
  "A tax surcharge for everyone and a long-term financing deal between Bund and Länder for the new states.",
  "GFX_decision_money_dec", visible=f"has_global_flag = {P}_unity_achieved", available="check_variable = { cwger_east_burden > 20 }", cost=75, once=True,
  effect=J(f"add_ideas = {P}_idea_soli", v("cwger_east_burden", -15), faction("mittelstand", -5)), ai=30)

M(EC, "mission_energy", "Energy Security",
  "The oil shock has shown how vulnerable an economy without its own oil is. Save energy, diversify supply - before the next embargo.",
  "GFX_decision_oil", activation=f"has_country_flag = {P}_oil_shock_seen NOT = {{ has_country_flag = {P}_energy_mission_done }}",
  available=f"OR = {{ has_completed_focus = {P}_energy_programme has_country_flag = {P}_energy_saving }}", days=365,
  complete=J(f"set_country_flag = {P}_energy_mission_done", f"if = {{ limit = {{ has_idea = {P}_idea_stagflation }} remove_ideas = {P}_idea_stagflation }}", stab(0.02)),
  timeout=J(f"set_country_flag = {P}_energy_mission_done", f"add_timed_idea = {{ idea = {P}_idea_stagflation days = 365 }}"), good=True)
D(EC, "energy_saving", "Energy-Saving Campaign",
  "'Energy saving is our best energy source': insulation grants, a speed limit, thermostat adverts on television.",
  "GFX_decision_oil", visible=f"has_country_flag = {P}_oil_shock_seen NOT = {{ has_country_flag = {P}_energy_saving }}", cost=40, once=True,
  effect=J(f"set_country_flag = {P}_energy_saving", money_gdp(-0.0008)), ai=30)
D(EC, "nato_summit", "NATO Summit Diplomacy",
  "Host the allies, sign the communiqué, be photographed with the American president.",
  "GFX_decision_nato", visible="always = yes", available="check_variable = { cwger_westbindung < 80 }", cost=50, re_enable=365,
  effect=J(v("cwger_westbindung", 6), v("cwger_peace_movement", 2), tension(1)), ai=12)
