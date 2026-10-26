# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""Internal security: the RAF as a visible cat-and-mouse game.

Builds on the terror model in systems.py (cwger_raf_*, cwger_terror_*, BKA and GSG 9 levels):

  wanted list     six cards per RAF generation; each card has a state (cwsec_w<i>_st: 0 at large,
                  1 traced, 2 arrested, 3 dead, 4 left the group) and a trace value (cwsec_w<i>_ort 0..100)
  targets         the RAF plans against six target categories (cwsec_plan_<c> 0..100); protection
                  details (cwsec_prot_<c>) slow the planning and foil most attacks
  prisons         prison regime (cwsec_haft 1 isolation, 2 normal, 3 association) and hunger strike (cwsec_hunger)
  crisis staff    a hostage crisis runs to a deadline (cwsec_ult_end, one scheduled event; extensions cwsec_ult_ext) with storm, raid, contact ban, stall, give in
  balance         security state against rule of law (existing cwger_security and cwger_rechtsstaat)
"""
from cw_lib import *
from events_lib import E, O

EVS = "COLDWAR_GSEC"
S = P + "_sec"

GEN_NAMES = {
    1: ["Andreas Baader", "Gudrun Ensslin", "Ulrike Meinhof", "Jan-Carl Raspe", "Holger Meins", "Brigitte Mohnhaupt"],
    2: ["Brigitte Mohnhaupt", "Christian Klar", "Knut Folkerts", "Peter-Jürgen Boock", "Stefan Wisniewski", "Adelheid Schulz"],
    3: ["Unidentified - commando level 1", "Unidentified - commando level 2", "Unidentified - commando level 3",
        "Unidentified - logistics", "Unidentified - courier", "Unidentified - explosives expert"],
}
TARGETS = [  # key, name, description, weights per generation (1, 2, 3)
    ("justice", "Justice", "Prosecutors, judges, prison staff.", (2, 4, 1)),
    ("business", "Business", "Bankers, industrialists, employers.", (2, 4, 5)),
    ("usforces", "US Forces", "US Army bases and commanders.", (3, 2, 4)),
    ("politics", "Politics", "Ministers and party headquarters.", (1, 1, 2)),
    ("infra", "Infrastructure", "Prison sites, publishers, computer centres.", (3, 1, 2)),
    ("embassy", "Embassies Abroad", "West German missions abroad.", (0, 3, 0)),
]
# Targets that only exist while something is actually in the game world (roleplay: the players decide).
TARGET_ACTIVE = {"usforces": "has_country_flag = cwsec_us_present"}
TARGET_INACTIVE_TEXT = {"usforces": "§gNo US troops stationed in the Federal Republic.§!"}
REGIMES = [(1, "isolation", "Isolation", "High-security isolation: the prisoners cannot organise - and the movement outside calls it torture. Milieu grows, hunger strikes come faster."),
           (2, "normal", "Normal Regime", "Ordinary rules for high-security prisoners."),
           (3, "association", "Association", "Held together in small groups, as the prisoners demand. The movement calms down - and the prisoners can coordinate with the commandos outside.")]

LOG = {}


def slog(key, text):
    if key not in LOG:
        LOG[key] = (len(LOG) + 1, text)
    return f"set_temp_variable = {{ cwsec_t_log = {LOG[key][0]} }}\n{S}_log = yes"


ACTS = []


def A(key, name, desc, pp_cost, cd, trig, eff, money_cost=None, short=None):
    ACTS.append(dict(key=key, name=name, desc=desc, pp=pp_cost, cd=cd, trig=trig, eff=eff, short=short or name))


ALL_CARDS_ORT = lambda n: "\n".join(f"if = {{ limit = {{ check_variable = {{ cwsec_w{i}_st < 2 }} }} add_to_variable = {{ cwsec_w{i}_ort = {n} }} }}" for i in range(1, 7)) + "\n" + \
    "\n".join(f"clamp_variable = {{ var = cwsec_w{i}_ort min = 0 max = 100 }}" for i in range(1, 7))


A("raster", "Computer Dragnet (Rasterfahndung)", "Run the BKA's computers in Wiesbaden against every database the state owns: electricity bills paid in cash, rented flats, car registrations.",
  50, 240, "check_variable = { cwger_bka_level > 2 } check_variable = { cwger_raf_cadre > 3 }",
  J(ALL_CARDS_ORT(10), v("cwger_rechtsstaat", -3), v("cwger_security", 2), slog("raster", "The dragnet runs through the databases.")), short="Dragnet")
A("reward", "Offer a Reward", "Hundreds of thousands of marks for information leading to an arrest.",
  0, 365, "check_variable = { cwger_raf_cadre > 0 }",
  J(money_gdp(-0.0002), ALL_CARDS_ORT(6), v("cwger_raf_milieu", 1), slog("reward", "A large reward is offered for information.")), short="Reward")
A("posters", "Wanted Posters", "Faces of the most wanted in every post office, every bank, every border crossing.",
  40, 180, "check_variable = { cwger_terror_left > 20 }",
  J(ALL_CARDS_ORT(4), v("cwger_raf_cadre", -1), v("cwger_raf_milieu", 1), v("cwger_security", 2), slog("posters", "New wanted posters go up across the country.")), short="Posters")
A("kronzeuge", "Recruit a Crown Witness", "Lower sentences for those who testify against their former comrades.",
  50, 365, "has_country_flag = cwsec_unlock_kronzeuge check_variable = { cwger_raf_prisoners > 1 }",
  J("set_temp_variable = { cwsec_t = 25 }", f"{S}_boost_best = yes", v("cwger_rechtsstaat", -1), v("cwger_raf_milieu", -2),
    slog("kronzeuge", "A former member testifies against the commando level.")), short="Witness")
A("informant", "Run an Informant", "An informant inside the RAF's logistics could lead the BKA to the commando level - if the operation goes right.",
  50, 720, "check_variable = { cwger_raf_gen = 3 } check_variable = { cwger_raf_cadre > 3 }",
  J("random_list = { 55 = { set_temp_variable = { cwsec_t = 30 } " + S + "_boost_best = yes } 45 = { country_event = { id = COLDWAR_GER.61 days = 1 } } }",
    tt(f"{P}_tt_sec_informant", "§G55%§!: a strong lead on one of the wanted. §R45%§!: the operation goes wrong.")), short="Informant")
A("forcefeed", "Force-Feeding", "Doctors under police protection keep the hunger strikers alive.",
  25, 120, "check_variable = { cwsec_hunger > 39 }",
  J("add_to_variable = { cwsec_hunger = -25 }", "clamp_variable = { var = cwsec_hunger min = 0 max = 100 }", v("cwger_rechtsstaat", -3), v("cwger_raf_milieu", 2),
    slog("forcefeed", "The hunger strikers are force-fed.")), short="Force-Feed")
A("dropout", "Exit Programme", "A quiet offer to members who want out: a new identity, reduced sentences, protection.",
  50, 365, "has_country_flag = cwsec_unlock_dropout check_variable = { cwger_raf_cadre > 2 }",
  J(v("cwger_raf_milieu", -5), v("cwger_raf_cadre", -2), f"{S}_dropout = yes", slog("dropout", "A member leaves the underground through the exit programme.")), short="Exit Offer")
A("kinkel", "Release Renouncing Prisoners", "Parole for RAF prisoners who have served long sentences and renounce violence.",
  40, 365, f"has_country_flag = {P}_kinkel_initiative check_variable = {{ cwger_raf_prisoners > 2 }}",
  J("subtract_from_variable = { cwger_raf_prisoners = 2 }", v("cwger_raf_milieu", -4), v("cwger_rechtsstaat", 2), party("cdu", -0.002),
    slog("kinkel", "Prisoners who renounce violence are released.")), short="Release")
A("ban_right", "Ban an Extremist Organisation", "Article 9 of the Basic Law lets the Interior Minister dissolve associations directed against the constitutional order.",
  60, 730, f"has_country_flag = {P}_ban_unlocked check_variable = {{ cwger_terror_right > 15 }}",
  J(f"set_country_flag = {{ flag = {P}_far_right_banned days = 1095 value = 1 }}", f"clr_country_flag = {P}_wsg_hoffmann_active",
    v("cwger_terror_right", -6), party("npd", -0.003), party("rep", -0.002), v("cwger_rechtsstaat", -1), slog("ban_right", "A right-wing extremist organisation is banned.")),
  short="Ban Group")
A("ban_pkk", "Ban the PKK", "Ban the Kurdistan Workers' Party and its front organisations.",
  50, 0, f"date > 1990.1.1 check_variable = {{ cwger_terror_foreign > 18 }} NOT = {{ has_country_flag = {P}_pkk_banned }}",
  J(f"set_country_flag = {P}_pkk_banned", v("cwger_terror_foreign", -6),
    "if = { limit = { country_exists = TUR } TUR = { add_opinion_modifier = { target = ROOT modifier = medium_increase } } }",
    slog("ban_pkk", "The PKK is banned.")), short="Ban PKK")
A("counterspy", "Counter-Espionage Campaign", "Unmask the 'Romeos' who court secretaries in Bonn ministries and the moles inside the BND.",
  75, 365, "always = yes",
  J(v("cwger_counterintel", 8), v("cwger_stasi_penetration", -6), v("cwger_rechtsstaat", -1), slog("counterspy", "A counter-espionage campaign sweeps the ministries.")),
  short="Counter-Spy")
A("vetting", "Vet the Chancellery", "Background checks for everyone with access to the chancellor's papers.",
  40, 365, "always = yes",
  J(v("cwger_counterintel", 6), v("cwger_stasi_penetration", -3), v("cwger_rechtsstaat", -1), slog("vetting", "The chancellery's staff are vetted.")), short="Vetting")
A("double", "Turn a Double Agent", "An HVA courier has been caught. Let him go home - and report what we want East Berlin to hear.",
  60, 365, "check_variable = { cwger_counterintel > 50 }",
  J(v("cwger_stasi_penetration", -8), dv("cwddr_sed_control", -2),
    "random_list = { 75 = { } 25 = { " + v("cwger_scandal", 8, show=False) + " } }",
    tt(f"{P}_tt_sec_double", "§R25%§!: the operation becomes public (scandal pressure §R+8§!)."), slog("double", "An HVA courier is turned.")), short="Double Agent")
# hostage crisis staff
A("storm", "Send In GSG 9", "The commandos are ready. Their chance of success depends on their training and on how well the hiding place is known.",
  25, 0, f"has_country_flag = {P}_hostage_ultimatum check_variable = {{ cwger_gsg9_tier > 0 }}",
  J(f"{P}_rescue_roll = yes", f"if = {{ limit = {{ has_country_flag = {P}_rescue_success }} country_event = {{ id = COLDWAR_GER.55 days = 1 }} }} else = {{ country_event = {{ id = COLDWAR_GER.56 days = 1 }} }}",
    f"clr_country_flag = {P}_hostage_ultimatum"), short="Storm")
A("safehouse", "Raid the Safe Houses", "Dragnet results, informants and door-to-door searches in the district where the hostage is thought to be.",
  50, 0, f"has_country_flag = {P}_hostage_ultimatum NOT = {{ has_country_flag = {P}_safehouse_raided }} check_variable = {{ cwger_bka_level > 0 }}",
  J(f"set_country_flag = {P}_safehouse_raided", v("cwger_rechtsstaat", -2),
    f"random_list = {{ 35 = {{ modifier = {{ add = 15 check_variable = {{ cwger_bka_level > 2 }} }} clr_country_flag = {P}_hostage_ultimatum country_event = {{ id = COLDWAR_GER.55 days = 2 }} }} 65 = {{ }} }}",
    tt(f"{P}_tt_sec_raid", "§G35%§! (50% with BKA level 3) to find the hostage alive. Once per crisis.")), short="Raid")
A("contactban", "Impose a Contact Ban", "Cut the imprisoned terrorists off from their lawyers and from each other while the hostage is held.",
  25, 60, f"has_country_flag = {P}_hostage_ultimatum has_country_flag = {P}_contact_ban_law",
  J(v("cwger_raf_cadre", -3), v("cwger_rechtsstaat", -4), "set_temp_variable = { cwsec_t_ext = 3 }", f"{S}_extend_deadline = yes",
    tt(f"{P}_tt_sec_cb", "The commando outside loses contact with its leaders; the deadline slips by §G3§! days.")), short="Contact Ban")
A("stall", "Play for Time", "Messages through the lawyers, a request for proof of life, a television statement that says nothing.",
  25, 0, f"has_country_flag = {P}_hostage_ultimatum check_variable = {{ cwsec_stalls < 2 }}",
  J("set_temp_variable = { cwsec_t_ext = 5 }", f"{S}_extend_deadline = yes", "add_to_variable = { cwsec_stalls = 1 }", v("cwger_raf_milieu", 1),
    "set_temp_variable = { cwsec_t = 10 }", f"{S}_boost_best = yes",
    tt(f"{P}_tt_sec_stall", "The deadline moves by §G5§! days and the hiding place comes into view. Twice per crisis.")), short="Stall")
A("givein", "Give In to the Demands", "Release the prisoners. The hostage comes home - and every terrorist learns that the Federal Republic can be blackmailed.",
  0, 0, f"has_country_flag = {P}_hostage_ultimatum",
  J(f"{P}_hostage_exchange = yes", f"clr_country_flag = {P}_hostage_ultimatum", stab(-0.03), pp(-50), v("cwger_rechtsstaat", -2),
    slog("givein", "The government gives in. Prisoners are flown out.")), short="Give In")


def effects():
    cards_reset = "\n".join(f"set_variable = {{ cwsec_w{i}_st = 0 }}\nset_variable = {{ cwsec_w{i}_ort = 10 }}" for i in range(1, 7))
    ort_tick = []
    for i in range(1, 7):
        ort_tick.append(f"""	if = {{ limit = {{ check_variable = {{ cwsec_w{i}_st < 2 }} }}
		add_to_variable = {{ cwsec_w{i}_ort = cwsec_t_gain }}
		random_list = {{ 50 = {{ add_to_variable = {{ cwsec_w{i}_ort = 1.5 }} }} 50 = {{ add_to_variable = {{ cwsec_w{i}_ort = -1.5 }} }} }}
		# a traced commando notices the surveillance and changes flats, cars and papers
		if = {{ limit = {{ check_variable = {{ cwsec_w{i}_st = 1 }} }}
			random_list = {{ 80 = {{ }} 20 = {{ modifier = {{ add = 10 check_variable = {{ cwger_raf_gen > 1 }} }} add_to_variable = {{ cwsec_w{i}_ort = -15 }} {slog("moved", "A traced suspect has moved to a new safe house. The trail goes cold.")} }} }}
		}}
		clamp_variable = {{ var = cwsec_w{i}_ort min = 0 max = 100 }}
		if = {{ limit = {{ check_variable = {{ cwsec_w{i}_ort > 59 }} check_variable = {{ cwsec_w{i}_st = 0 }} }} set_variable = {{ cwsec_w{i}_st = 1 }} {slog("traced", "The BKA has a trace on one of the most wanted.")} }}
		if = {{ limit = {{ check_variable = {{ cwsec_w{i}_ort < 50 }} check_variable = {{ cwsec_w{i}_st = 1 }} }} set_variable = {{ cwsec_w{i}_st = 0 }} }}
	}}""")
    arrest_best = []
    for i in range(1, 7):
        kw = "if" if i == 1 else "else_if"
        arrest_best.append(f"\t{kw} = {{ limit = {{ check_variable = {{ cwsec_w{i}_st < 2 }} check_variable = {{ cwsec_w{i}_ort = cwsec_t_best }} }} set_variable = {{ cwsec_w{i}_st = 2 }} set_variable = {{ cwsec_last_card = {i} }} }}")
    best = "\n".join(f"\tif = {{ limit = {{ check_variable = {{ cwsec_w{i}_st < 2 }} check_variable = {{ cwsec_w{i}_ort > cwsec_t_best }} }} set_temp_variable = {{ cwsec_t_best = cwsec_w{i}_ort }} }}" for i in range(1, 7))
    boost = []
    for i in range(1, 7):
        kw = "if" if i == 1 else "else_if"
        boost.append(f"\t{kw} = {{ limit = {{ check_variable = {{ cwsec_w{i}_st < 2 }} check_variable = {{ cwsec_w{i}_ort = cwsec_t_best }} }} add_to_variable = {{ cwsec_w{i}_ort = cwsec_t }} clamp_variable = {{ var = cwsec_w{i}_ort min = 0 max = 100 }} }}")
    access = []
    for i in range(1, 7):
        access.append(f"""{S}_access_{i} = {{
	set_country_flag = {{ flag = cwsec_access_cd days = 45 value = 1 }}
	add_political_power = -35
	set_variable = {{ cwsec_last_card = {i} }}
	random_list = {{
		30 = {{
			modifier = {{ add = 8 check_variable = {{ cwsec_w{i}_ort > 74 }} }}
			modifier = {{ add = 10 check_variable = {{ cwsec_w{i}_ort > 89 }} }}
			modifier = {{ add = 6 check_variable = {{ cwger_gsg9_tier > 0 }} }}
			modifier = {{ add = 6 check_variable = {{ cwger_gsg9_tier > 1 }} }}
			modifier = {{ add = 5 check_variable = {{ cwger_bka_level > 1 }} }}
			set_variable = {{ cwsec_w{i}_st = 2 }}
			add_to_variable = {{ cwger_raf_prisoners = 1 }}
			add_to_variable = {{ cwger_raf_cadre = -3 }}
			clamp_variable = {{ var = cwger_raf_cadre min = 0 max = 120 }}
			add_stability = 0.01
			country_event = {{ id = {EVS}.11 days = 1 }}
		}}
		45 = {{
			add_to_variable = {{ cwsec_w{i}_ort = -35 }}
			clamp_variable = {{ var = cwsec_w{i}_ort min = 0 max = 100 }}
			set_variable = {{ cwsec_w{i}_st = 0 }}
			country_event = {{ id = {EVS}.12 days = 1 }}
		}}
		15 = {{
			modifier = {{ factor = 0.5 check_variable = {{ cwger_gsg9_tier > 1 }} }}
			country_event = {{ id = {EVS}.14 days = 1 }}
		}}
	}}
	{S}_gui_refresh = yes
}}""")
    plan_tick = []
    for ci, (k, name, desc, wts) in enumerate(TARGETS):
        inactive = ""
        if k in TARGET_ACTIVE:
            inactive = (f"\n\t# nothing to plan against while the target does not exist; a protection detail there is released"
                        f"\n\tif = {{{{ limit = {{{{ NOT = {{{{ {TARGET_ACTIVE[k]} }}}} }}}} set_temp_variable = {{{{ cwsec_t_w = 0 }}}} set_variable = {{{{ cwsec_plan_{k} = 0 }}}}"
                        f" if = {{{{ limit = {{{{ check_variable = {{{{ cwsec_prot_{k} = 1 }}}} }}}} set_variable = {{{{ cwsec_prot_{k} = 0 }}}} add_to_variable = {{{{ cwsec_used = -1 }}}} }}}} }}}}")
            inactive = inactive.replace("{{", "{").replace("}}", "}")
        plan_tick.append(f"""	set_temp_variable = {{ cwsec_t_w = 0 }}
	if = {{ limit = {{ check_variable = {{ cwger_raf_gen = 1 }} }} set_temp_variable = {{ cwsec_t_w = {wts[0]} }} }}
	if = {{ limit = {{ check_variable = {{ cwger_raf_gen = 2 }} }} set_temp_variable = {{ cwsec_t_w = {wts[1]} }} }}
	if = {{ limit = {{ check_variable = {{ cwger_raf_gen = 3 }} }} set_temp_variable = {{ cwsec_t_w = {wts[2]} }} }}
	multiply_temp_variable = {{ cwsec_t_w = cwsec_t_speed }}
	if = {{ limit = {{ check_variable = {{ cwsec_prot_{k} = 1 }} }} multiply_temp_variable = {{ cwsec_t_w = 0.6 }} }}{inactive}
	add_to_variable = {{ cwsec_plan_{k} = cwsec_t_w }}
	clamp_variable = {{ var = cwsec_plan_{k} min = 0 max = 100 }}
	if = {{ limit = {{ check_variable = {{ cwsec_plan_{k} > 99 }} NOT = {{ has_country_flag = {P}_attack_cooldown }} NOT = {{ has_country_flag = cwsec_struck_this_month }} }}
		set_country_flag = {{ flag = cwsec_struck_this_month days = 20 value = 1 }}
		set_variable = {{ cwsec_plan_{k} = 0 }}
		set_variable = {{ cwsec_last_target = {ci + 1} }}
		if = {{ limit = {{ check_variable = {{ cwsec_prot_{k} = 1 }} }}
			random_list = {{
				55 = {{
					modifier = {{ add = 5 check_variable = {{ cwger_bka_level > 1 }} }}
					modifier = {{ add = 5 check_variable = {{ cwger_bka_level > 2 }} }}
					set_country_flag = {{ flag = {P}_attack_cooldown days = 60 value = 1 }}
					country_event = {{ id = {EVS}.10 days = 1 }}
					# the commando switches to a softer target
					{S}_shift_targets = yes
				}}
				45 = {{ {P}_raf_attack = yes }}
			}}
		}}
		else = {{ {P}_raf_attack = yes }}
	}}""")
    return f"""## Generated by tools/west_germany_1970/compile.py. Edit the generator, not this file.

# ---------------------------------------------------------------- internal security window
{S}_setup = {{
	set_country_flag = cwsec_initialized
	set_variable = {{ cwsec_tab = 1 }}
	set_variable = {{ cwsec_gen_cards = 1 }}
	{cards_reset}
	{chr(10).join(f"set_variable = {{ cwsec_plan_{k} = 0 }}" for k, *_ in TARGETS)}
	{chr(10).join(f"set_variable = {{ cwsec_prot_{k} = 0 }}" for k, *_ in TARGETS)}
	set_variable = {{ cwsec_slots = 2 }}
	set_variable = {{ cwsec_used = 0 }}
	set_variable = {{ cwsec_haft = 2 }}
	set_variable = {{ cwsec_hunger = 0 }}
	set_variable = {{ cwsec_ult_days = 0 }}
	set_variable = {{ cwsec_ult_end = 0 }}
	set_variable = {{ cwsec_ult_ext = 0 }}
	set_variable = {{ cwsec_log_1 = 0 }}
	set_variable = {{ cwsec_log_2 = 0 }}
	set_variable = {{ cwsec_log_3 = 0 }}
	set_variable = {{ cwsec_w5_ort = 20 }}
	{slog("start", "The Baader-Meinhof group has gone underground after Baader's escape in May.")}
}}

{S}_log = {{
	set_variable = {{ cwsec_log_3 = cwsec_log_2 }}
	set_variable = {{ cwsec_log_y_3 = cwsec_log_y_2 }}
	set_variable = {{ cwsec_log_2 = cwsec_log_1 }}
	set_variable = {{ cwsec_log_y_2 = cwsec_log_y_1 }}
	set_variable = {{ cwsec_log_1 = cwsec_t_log }}
	set_variable = {{ cwsec_log_y_1 = cwgg_year }}
}}

# Monthly, GER scope, after the terror tick.
{S}_tick = {{
	if = {{ limit = {{ NOT = {{ has_country_flag = cwsec_initialized }} }} {S}_setup = yes }}
	# US forces count only while US divisions are actually stationed on West German soil
	clr_country_flag = cwsec_us_present
	if = {{ limit = {{ country_exists = USA any_owned_state = {{ USA = {{ divisions_in_state = {{ state = PREV size > 0 }} }} }} }}
		set_country_flag = cwsec_us_present
	}}
	# a new generation brings new faces
	if = {{ limit = {{ NOT = {{ check_variable = {{ cwsec_gen_cards = cwger_raf_gen }} }} check_variable = {{ cwger_raf_gen < 4 }} }}
		set_variable = {{ cwsec_gen_cards = cwger_raf_gen }}
		{cards_reset}
		{slog("newgen", "A new generation of the RAF: new names on the wanted list.")}
	}}
	if = {{ limit = {{ check_variable = {{ cwger_raf_gen > 3 }} }}
		{chr(10).join(f"if = {{ limit = {{ check_variable = {{ cwsec_w{i}_st < 2 }} }} set_variable = {{ cwsec_w{i}_st = 4 }} }}" for i in range(1, 7))}
	}}
	# trace gain: BKA, INPOL, rewards and witnesses against the milieu and the Stasi's shelter
	set_temp_variable = {{ cwsec_t_gain = 0.5 }}
	set_temp_variable = {{ cwsec_t = cwger_bka_level }}
	add_to_temp_variable = {{ cwsec_t_gain = cwsec_t }}
	if = {{ limit = {{ has_country_flag = cwsec_inpol }} add_to_temp_variable = {{ cwsec_t_gain = 2 }} }}
	if = {{ limit = {{ has_country_flag = cwsec_cd_raster }} add_to_temp_variable = {{ cwsec_t_gain = 1 }} }}
	set_temp_variable = {{ cwsec_t = cwger_raf_milieu }}
	divide_temp_variable = {{ cwsec_t = 15 }}
	subtract_from_temp_variable = {{ cwsec_t_gain = cwsec_t }}
	# each generation learned from the last one's arrests: conspiracy, no phone calls, no fingerprints
	if = {{ limit = {{ check_variable = {{ cwger_raf_gen = 2 }} }} add_to_temp_variable = {{ cwsec_t_gain = -1 }} }}
	if = {{ limit = {{ check_variable = {{ cwger_raf_gen = 3 }} }} add_to_temp_variable = {{ cwsec_t_gain = -2.5 }} }}
	if = {{ limit = {{ has_global_flag = cwgg_raf_in_ddr NOT = {{ has_global_flag = cwgg_raf_in_ddr_found }} }} add_to_temp_variable = {{ cwsec_t_gain = -1 }} }}
	set_temp_variable = {{ cwsec_t = modifier@terror_threat_detection_modifier }}
	multiply_temp_variable = {{ cwsec_t = 6 }}
	clamp_temp_variable = {{ var = cwsec_t min = 0 max = 2 }}
	add_to_temp_variable = {{ cwsec_t_gain = cwsec_t }}
{chr(10).join(ort_tick)}
	# the RAF plans its next attack
	if = {{ limit = {{ check_variable = {{ cwger_raf_gen < 4 }} NOT = {{ has_country_flag = {P}_raf_dissolved }} check_variable = {{ cwger_raf_cadre > 2 }} }}
		set_temp_variable = {{ cwsec_t_speed = cwger_raf_cadre }}
		divide_temp_variable = {{ cwsec_t_speed = 2 }}
		add_to_temp_variable = {{ cwsec_t_speed = 2 }}
		set_temp_variable = {{ cwsec_t = cwger_raf_milieu }}
		divide_temp_variable = {{ cwsec_t = 10 }}
		add_to_temp_variable = {{ cwsec_t_speed = cwsec_t }}
		set_temp_variable = {{ cwsec_t = cwger_bka_level }}
		multiply_temp_variable = {{ cwsec_t = -0.1 }}
		add_to_temp_variable = {{ cwsec_t = 1 }}
		multiply_temp_variable = {{ cwsec_t_speed = cwsec_t }}
		if = {{ limit = {{ check_variable = {{ cwsec_haft = 3 }} }} multiply_temp_variable = {{ cwsec_t_speed = 1.1 }} }}
		divide_temp_variable = {{ cwsec_t_speed = 3.3 }}
{chr(10).join(plan_tick)}
	}}
	# prisons
	if = {{ limit = {{ check_variable = {{ cwsec_haft = 1 }} }} add_to_variable = {{ cwger_raf_milieu = 0.3 }} }}
	if = {{ limit = {{ check_variable = {{ cwsec_haft = 3 }} }} add_to_variable = {{ cwger_raf_milieu = -0.3 }} }}
	clamp_variable = {{ var = cwger_raf_milieu min = 0 max = 100 }}
	if = {{ limit = {{ check_variable = {{ cwger_raf_prisoners > 2 }} check_variable = {{ cwger_raf_gen < 4 }} }}
		if = {{ limit = {{ check_variable = {{ cwsec_haft = 1 }} }} add_to_variable = {{ cwsec_hunger = 6 }} }}
		else_if = {{ limit = {{ check_variable = {{ cwsec_haft = 2 }} }} add_to_variable = {{ cwsec_hunger = 3 }} }}
		else = {{ add_to_variable = {{ cwsec_hunger = -3 }} }}
	}}
	else = {{ add_to_variable = {{ cwsec_hunger = -5 }} }}
	clamp_variable = {{ var = cwsec_hunger min = 0 max = 100 }}
	if = {{ limit = {{ check_variable = {{ cwsec_hunger > 79 }} NOT = {{ has_country_flag = cwsec_hunger_cd }} }}
		set_country_flag = {{ flag = cwsec_hunger_cd days = 720 value = 1 }}
		country_event = {{ id = {EVS}.13 days = 1 }}
	}}
	# protection details used
	set_variable = {{ cwsec_used = 0 }}
	{chr(10).join(f"add_to_variable = {{ cwsec_used = cwsec_prot_{k} }}" for k, *_ in TARGETS)}
	{S}_gui_refresh = yes
}}

# Arrests from the existing terror model take the best-traced card.
{S}_arrest_best = {{
	set_temp_variable = {{ cwsec_t_best = -1 }}
{best}
	if = {{ limit = {{ check_variable = {{ cwsec_t_best > -1 }} }}
{chr(10).join(arrest_best)}
	}}
}}

# Raises the trace of the best-traced card by temp cwsec_t.
{S}_boost_best = {{
	set_temp_variable = {{ cwsec_t_best = -1 }}
{best}
	if = {{ limit = {{ check_variable = {{ cwsec_t_best > -1 }} }}
{chr(10).join(boost)}
	}}
}}

# A member leaves the group; after 1979 the Stasi may take them in.
{S}_dropout = {{
	random_list = {{
		{" ".join(f"10 = {{ modifier = {{ factor = 0 NOT = {{ check_variable = {{ cwsec_w{i}_st < 2 }} }} }} set_variable = {{ cwsec_w{i}_st = 4 }} }}" for i in range(1, 7))}
	}}
	if = {{ limit = {{ date > 1979.12.31 country_exists = DDR NOT = {{ has_global_flag = cwgg_raf_in_ddr }} }}
		random_list = {{ 40 = {{ }} 60 = {{ set_global_flag = cwgg_raf_in_ddr }} }}
	}}
}}

{chr(10).join(access)}

# Hostage deadline: one scheduled event at the deadline (no polling). Extensions bought by the crisis staff are
# stored in cwsec_ult_ext and re-schedule the deadline in steps of five and three days when it arrives.
{S}_ultimatum_deadline = {{
	if = {{ limit = {{ has_country_flag = {P}_hostage_ultimatum }}
		if = {{ limit = {{ check_variable = {{ cwsec_ult_ext > 4 }} }}
			add_to_variable = {{ cwsec_ult_ext = -5 }}
			country_event = {{ id = {EVS}.1 days = 5 }}
		}}
		else_if = {{ limit = {{ check_variable = {{ cwsec_ult_ext > 0 }} }}
			set_variable = {{ cwsec_ult_ext = 0 }}
			country_event = {{ id = {EVS}.1 days = 3 }}
		}}
		else = {{
			clr_country_flag = {P}_hostage_ultimatum
			clr_country_flag = {P}_safehouse_raided
			country_event = {{ id = COLDWAR_GER.56 days = 1 }}
		}}
		{S}_gui_refresh = yes
	}}
}}

# Extends the deadline by temp cwsec_t_ext days (3 or 5).
{S}_extend_deadline = {{
	add_to_variable = {{ cwsec_ult_ext = cwsec_t_ext }}
	add_to_variable = {{ cwsec_ult_end = cwsec_t_ext }}
}}

{S}_start_ultimatum = {{
	set_variable = {{ cwsec_ult_end = global.num_days }}
	add_to_variable = {{ cwsec_ult_end = 21 }}
	set_variable = {{ cwsec_ult_ext = 0 }}
	set_variable = {{ cwsec_stalls = 0 }}
	set_country_flag = cwsec_open
	set_variable = {{ cwsec_tab = 4 }}
	country_event = {{ id = {EVS}.1 days = 21 }}
	{slog("ultimatum", "A hostage is held. The crisis staff meets in the chancellery.")}
	{S}_gui_refresh = yes
}}

# Protection details: toggle for target temp cwsec_t_c.
{chr(10).join(f'''{S}_protect_{k} = {{
	if = {{ limit = {{ check_variable = {{ cwsec_prot_{k} = 1 }} }} set_variable = {{ cwsec_prot_{k} = 0 }} add_to_variable = {{ cwsec_used = -1 }} }}
	else = {{ set_variable = {{ cwsec_prot_{k} = 1 }} add_to_variable = {{ cwsec_used = 1 }} add_political_power = -10 }}
	{S}_gui_refresh = yes
}}''' for k, *_ in TARGETS)}

{chr(10).join(f'''{S}_regime_{key} = {{
	set_variable = {{ cwsec_haft = {rid} }}
	add_political_power = -25
	set_country_flag = {{ flag = cwsec_regime_cd days = 180 value = 1 }}
	{"add_to_variable = { cwger_rechtsstaat = -2 } add_to_variable = { cwger_security = 2 }" if rid == 1 else ("add_to_variable = { cwger_rechtsstaat = 2 } add_to_variable = { cwsec_hunger = -20 }" if rid == 3 else "")}
	clamp_variable = {{ var = cwsec_hunger min = 0 max = 100 }}
	{slog("regime_" + key, "The prison regime for the RAF prisoners changes: " + name.lower() + ".")}
	{S}_gui_refresh = yes
}}''' for rid, key, name, _d in REGIMES)}

# After a foiled attack the commando turns to whatever is not protected.
{S}_shift_targets = {{
	if = {{ limit = {{ check_variable = {{ cwsec_prot_justice = 0 }} }} add_to_variable = {{ cwsec_plan_justice = 15 }} clamp_variable = {{ var = cwsec_plan_justice min = 0 max = 100 }} }}
	if = {{ limit = {{ check_variable = {{ cwsec_prot_business = 0 }} }} add_to_variable = {{ cwsec_plan_business = 15 }} clamp_variable = {{ var = cwsec_plan_business min = 0 max = 100 }} }}
	if = {{ limit = {{ check_variable = {{ cwsec_prot_usforces = 0 }} }} add_to_variable = {{ cwsec_plan_usforces = 15 }} clamp_variable = {{ var = cwsec_plan_usforces min = 0 max = 100 }} }}
	if = {{ limit = {{ check_variable = {{ cwsec_prot_politics = 0 }} }} add_to_variable = {{ cwsec_plan_politics = 15 }} clamp_variable = {{ var = cwsec_plan_politics min = 0 max = 100 }} }}
	if = {{ limit = {{ check_variable = {{ cwsec_prot_infra = 0 }} }} add_to_variable = {{ cwsec_plan_infra = 15 }} clamp_variable = {{ var = cwsec_plan_infra min = 0 max = 100 }} }}
	if = {{ limit = {{ check_variable = {{ cwsec_prot_embassy = 0 }} }} add_to_variable = {{ cwsec_plan_embassy = 15 }} clamp_variable = {{ var = cwsec_plan_embassy min = 0 max = 100 }} }}
}}

# A raid that ends in a shootout (card temp: cwsec_last_card).
{S}_shootout = {{
	if = {{ limit = {{ check_variable = {{ cwsec_last_card = 1 }} }}
		random_list = {{
			50 = {{ set_variable = {{ cwsec_w1_st = 3 }} add_to_variable = {{ cwger_raf_milieu = 5 }} add_to_variable = {{ cwger_raf_cadre = -2 }} }}
			50 = {{ set_variable = {{ cwsec_w1_st = 0 }} add_to_variable = {{ cwsec_w1_ort = -40 }} clamp_variable = {{ var = cwsec_w1_ort min = 0 max = 100 }} }}
		}}
	}}
	if = {{ limit = {{ check_variable = {{ cwsec_last_card = 2 }} }}
		random_list = {{
			50 = {{ set_variable = {{ cwsec_w2_st = 3 }} add_to_variable = {{ cwger_raf_milieu = 5 }} add_to_variable = {{ cwger_raf_cadre = -2 }} }}
			50 = {{ set_variable = {{ cwsec_w2_st = 0 }} add_to_variable = {{ cwsec_w2_ort = -40 }} clamp_variable = {{ var = cwsec_w2_ort min = 0 max = 100 }} }}
		}}
	}}
	if = {{ limit = {{ check_variable = {{ cwsec_last_card = 3 }} }}
		random_list = {{
			50 = {{ set_variable = {{ cwsec_w3_st = 3 }} add_to_variable = {{ cwger_raf_milieu = 5 }} add_to_variable = {{ cwger_raf_cadre = -2 }} }}
			50 = {{ set_variable = {{ cwsec_w3_st = 0 }} add_to_variable = {{ cwsec_w3_ort = -40 }} clamp_variable = {{ var = cwsec_w3_ort min = 0 max = 100 }} }}
		}}
	}}
	if = {{ limit = {{ check_variable = {{ cwsec_last_card = 4 }} }}
		random_list = {{
			50 = {{ set_variable = {{ cwsec_w4_st = 3 }} add_to_variable = {{ cwger_raf_milieu = 5 }} add_to_variable = {{ cwger_raf_cadre = -2 }} }}
			50 = {{ set_variable = {{ cwsec_w4_st = 0 }} add_to_variable = {{ cwsec_w4_ort = -40 }} clamp_variable = {{ var = cwsec_w4_ort min = 0 max = 100 }} }}
		}}
	}}
	if = {{ limit = {{ check_variable = {{ cwsec_last_card = 5 }} }}
		random_list = {{
			50 = {{ set_variable = {{ cwsec_w5_st = 3 }} add_to_variable = {{ cwger_raf_milieu = 5 }} add_to_variable = {{ cwger_raf_cadre = -2 }} }}
			50 = {{ set_variable = {{ cwsec_w5_st = 0 }} add_to_variable = {{ cwsec_w5_ort = -40 }} clamp_variable = {{ var = cwsec_w5_ort min = 0 max = 100 }} }}
		}}
	}}
	if = {{ limit = {{ check_variable = {{ cwsec_last_card = 6 }} }}
		random_list = {{
			50 = {{ set_variable = {{ cwsec_w6_st = 3 }} add_to_variable = {{ cwger_raf_milieu = 5 }} add_to_variable = {{ cwger_raf_cadre = -2 }} }}
			50 = {{ set_variable = {{ cwsec_w6_st = 0 }} add_to_variable = {{ cwsec_w6_ort = -40 }} clamp_variable = {{ var = cwsec_w6_ort min = 0 max = 100 }} }}
		}}
	}}
	add_to_variable = {{ cwger_raf_milieu = 3 }}
	add_to_variable = {{ cwger_rechtsstaat = -3 }}
	clamp_variable = {{ var = cwger_raf_milieu min = 0 max = 100 }}
	clamp_variable = {{ var = cwger_rechtsstaat min = 0 max = 100 }}
	clamp_variable = {{ var = cwger_raf_cadre min = 0 max = 120 }}
	{S}_gui_refresh = yes
}}
""" + actions_effects()


def actions_effects():
    out = ["\n# ---------------------------------------------------------------- actions"]
    for a in ACTS:
        pre = []
        if a["pp"]:
            pre.append(f"add_political_power = -{a['pp']}")
        if a["cd"]:
            pre.append(f"set_country_flag = {{ flag = cwsec_cd_{a['key']} days = {a['cd']} value = 1 }}")
        body = J(*pre, a["eff"], f"{S}_gui_refresh = yes")
        from tooltips import hide_vars
        out.append(f"{S}_act_{a['key']} = {{\n{fmt(hide_vars(body), 1)}\n}}")
    return "\n\n".join(out) + "\n"


def triggers():
    out = ["\n# ---------------------------------------------------------------- internal security"]
    for a in ACTS:
        conds = [a["trig"]]
        if a["pp"]:
            conds.append(f"has_political_power > {a['pp'] - 1}")
        if a["cd"]:
            conds.append(f"NOT = {{ has_country_flag = cwsec_cd_{a['key']} }}")
        out.append(f"{S}_can_{a['key']} = {{\n\t" + "\n\t".join(conds) + "\n}\n")
    for i in range(1, 7):
        out.append(f"{S}_can_access_{i} = {{\n\tcheck_variable = {{ cwsec_w{i}_st = 1 }}\n\thas_political_power > 34\n\tNOT = {{ has_country_flag = cwsec_access_cd }}\n}}\n")
    for k, *_ in TARGETS:
        act = f"\n\t{TARGET_ACTIVE[k]}" if k in TARGET_ACTIVE else ""
        out.append(f"{S}_can_protect_{k} = {{\n\tOR = {{ check_variable = {{ cwsec_prot_{k} = 1 }} check_variable = {{ cwsec_used < cwsec_slots }} }}\n\thas_political_power > 9{act}\n}}\n")
    for rid, key, *_ in REGIMES:
        out.append(f"{S}_can_regime_{key} = {{\n\tNOT = {{ check_variable = {{ cwsec_haft = {rid} }} }}\n\tNOT = {{ has_country_flag = cwsec_regime_cd }}\n\thas_political_power > 24\n\tcheck_variable = {{ cwger_raf_prisoners > 0 }}\n}}\n")
    return "\n".join(out)


def events():
    E(f"{EVS}.1", "", "", "", [O("ok")], hidden=True, imm=f"{S}_ultimatum_deadline = yes")
    E(f"{EVS}.10", "Attack Foiled",
      "", "GFX_swat_polizei",
      [O("The protection details have earned their pay.", J(stab(0.01), v("cwger_raf_cadre", -1), "set_temp_variable = { cwsec_t = 15 }", f"{S}_boost_best = yes",
                                                            slog("foiled", "An RAF attack is foiled by a protection detail.")))],
      descs=[(f"check_variable = {{ cwsec_last_target = {i + 1} }}", t) for i, t in enumerate([
          "A commando was waiting outside the home of a senior judge. The protection detail noticed the parked van an hour too early for the attackers; the suspects fled, leaving weapons and a target file behind.",
          "The car of a bank chairman took a different route this morning. Where it would have passed, the police found a bomb wired to a light barrier.",
          "Military police at a US Army depot stopped a car with forged papers. In the boot: explosives and the plan of the officers' mess.",
          "A minister's convoy was ready for the ambush its escorts had trained for. Shots were exchanged; the commando escaped, but the minister is unhurt.",
          "Guards at the building site of a new prison surprised a group carrying explosives over the fence at night.",
          "The embassy in a neighbouring capital had been warned by the BKA. When armed men tried to enter, the doors were locked and the local police waiting."])])
    E(f"{EVS}.11", "Arrested",
      "Special commandos have arrested §Y[SEC_LastName]§!, one of the most wanted members of the Red Army Faction. Weapons, forged papers and a list of possible targets were found in the flat.",
      "GFX_swat_polizei2", [O("One fewer.", slog("arrest", "One of the most wanted is arrested."))])
    E(f"{EVS}.12", "The Trap Closes on Nothing",
      "The flat was empty, or the shooting started too early. The suspect has escaped - and a raid that went wrong is on every front page. Whose fault was it?",
      "GFX_Polizeiabsperrung",
      [O("Defend the officers.", J(v("cwger_rechtsstaat", -2), v("cwger_raf_milieu", 2), slog("raid_failed", "A raid goes wrong. The suspect escapes."))),
       O("Order an inquiry.", J(pp(-25), v("cwger_rechtsstaat", 1), slog("raid_inquiry", "An inquiry into a failed raid is opened.")))])
    E(f"{EVS}.14", "Shots in the Stairwell",
      "The commando opened fire the moment the door gave way. When the smoke cleared, a police officer lay dead on the landing - and the suspect was either dead too or gone over the rooftops. By the evening there are two versions of what happened, and the sympathisers believe only one.",
      "GFX_Polizeiabsperrung",
      [O("Order a full inquiry.", J(f"{S}_shootout = yes", pp(-25), v("cwger_rechtsstaat", 2), slog("shootout", "A raid ends in a shootout. An officer is dead."))),
       O("The officers acted in self-defence.", J(f"{S}_shootout = yes", v("cwger_raf_milieu", 3), v("cwger_security", 2), slog("shootout2", "A raid ends in a shootout; the government backs the commando.")))])
    E(f"{EVS}.13", "A Hunger Striker Dies",
      "A prisoner has died after weeks without food. Thousands march in Berlin, Frankfurt and Hamburg; on the walls of the universities new slogans appear overnight. The movement has a martyr.",
      "GFX_Demo_Generic",
      [O("The state could not prevent it.", J(v("cwger_raf_milieu", 15), v("cwger_raf_cadre", 3), "add_to_variable = { cwger_raf_prisoners = -1 }",
                                               "clamp_variable = { var = cwger_raf_prisoners min = 0 max = 40 }", "set_variable = { cwsec_hunger = 30 }", v("cwger_rechtsstaat", -3),
                                               protest(6), slog("hunger_death", "A hunger striker dies in prison.")))])


def window(Window, DT):
    w = Window("cwgg_sec", "cwsec_open", "cwsec_tab", ["cwgg_sec_tab_1", "cwgg_sec_tab_2", "cwgg_sec_tab_3", "cwgg_sec_tab_4"],
               "cwgg_sec_title", "cwgg_sec_subtitle", "GFX_cwgg_emblem_bka", "cwgg_sec_right_label", "cwgg_sec_right_value",
               dict(x=1760, sprite="GFX_cwgg_topbar_security"), skin="bka")
    L("cwgg_sec_tab_1", "Situation")
    L("cwgg_sec_tab_2", "Manhunt")
    L("cwgg_sec_tab_3", "Protection")
    L("cwgg_sec_tab_4", "Prisons & Crisis Staff")
    L("cwgg_sec_title", "Internal Security")
    L("cwgg_sec_subtitle", "Federal Criminal Police Office · Wiesbaden")
    L("cwgg_sec_right_label", "Rote Armee Fraktion")
    L("cwgg_sec_right_value", "[SEC_ThreatColored]")
    L("cwgg_sec_right_value_tt", "§YRote Armee Fraktion§!\nThe threat from the Red Army Faction and the wider left-wing underground. It grows with the RAF's active cadre and its sympathiser milieu - the students who lend a flat, the lawyers who carry a message, the professors who sign the open letters - and with the Movement 2 June and the Revolutionary Cells while they still exist.")
    L("cwgg_sec_topbar_value", "[?cwger_terror_left|0]")
    L("cwgg_sec_topbar_tt", "§YInternal Security§!\nLeft-wing terror threat §Y[?cwger_terror_left|0]§! · right §Y[?cwger_terror_right|0]§! · foreign §Y[?cwger_terror_foreign|0]§!\n[SEC_HostageLine]\n\nClick to open the window.")
    DT("SEC_ThreatColored", [("check_variable = { cwger_terror_left > 59 }", "cwgg_sec_thr_r"), ("check_variable = { cwger_terror_left > 29 }", "cwgg_sec_thr_y")], "cwgg_sec_thr_g")
    L("cwgg_sec_thr_r", "§R[?cwger_terror_left|0]§!")
    L("cwgg_sec_thr_y", "§Y[?cwger_terror_left|0]§!")
    L("cwgg_sec_thr_g", "§G[?cwger_terror_left|0]§!")
    DT("SEC_HostageLine", [(f"has_country_flag = {P}_hostage_ultimatum", "cwgg_sec_hostage_on")], "cwgg_sec_hostage_off")
    L("cwgg_sec_hostage_on", "§RA hostage is held - [?cwsec_ult_days|0] days to the deadline.§!")
    L("cwgg_sec_hostage_off", "No hostage crisis.")
    acts = {a["key"]: a for a in ACTS}

    def act_button(key, x, y, tab, wide=False, vis=""):
        a = acts[key]
        cd = f" Can be repeated after {round(a['cd'] / 30)} months." if a["cd"] else ""
        cost = f"§Y{a['pp']}§! political power." if a["pp"] else "No political power."
        L(f"cwgg_sec_btn_{key}", a["short"])
        L(f"cwgg_sec_btn_{key}_tt", f"§Y{a['name']}§!\n{a['desc']}\n\nCost: {cost}{cd}\n[SEC_Avail_{key}]")
        DT(f"SEC_Avail_{key}", [(f"{S}_can_{key} = yes", "cwgg_rv_avail_yes")] + ([(f"has_country_flag = cwsec_cd_{key}", "cwgg_rv_avail_cd")] if a["cd"] else []), "cwgg_rv_avail_no")
        w.button(f"btn_{key}", "GFX_mdcw_cw_button_160" if wide else "GFX_mdcw_cw_button_96", x, y, f"cwgg_sec_btn_{key}", f"{S}_act_{key} = yes", tab=tab,
                 enabled=f"{S}_can_{key} = yes", tip=f"cwgg_sec_btn_{key}_tt", vis=vis)

    # ------------------------------------------------ tab 1: situation
    T = 1
    w.section("threat", 138, "cwgg_sec_h_threat", T)
    L("cwgg_sec_h_threat", "THREAT ASSESSMENT")
    for j, (key, name, var, col, tip) in enumerate([
            ("left", "Left-wing terror", "cwger_terror_left", "red", "RAF cadre, sympathiser milieu, Movement 2 June and Revolutionary Cells."),
            ("right", "Right-wing terror", "cwger_terror_right", "purple", "Far-right votes, asylum pressure and paramilitary groups like the Wehrsportgruppe Hoffmann."),
            ("foreign", "Foreign terror", "cwger_terror_foreign", "teal", "Palestinian, Libyan and later Kurdish groups; rises with world tension.")]):
        y = 172 + j * 28
        w.text(f"t_{key}", f"cwgg_sec_t_{key}", 36, y, 170, tab=T, tip=f"cwgg_sec_t_{key}_tt")
        L(f"cwgg_sec_t_{key}", name)
        L(f"cwgg_sec_t_{key}_tt", f"§Y{name}§!: [?{var}|0]\n{tip}")
        w.bar(f"t_{key}", 210, y, var, 0, 100, col, tab=T)
        w.text(f"t_{key}_v", f"cwgg_sec_t_{key}_v", 520, y, 60, tab=T)
        L(f"cwgg_sec_t_{key}_v", f"§Y[?{var}|0]§!")
    w.section("raf", 262, "cwgg_sec_h_raf", T, right="cwgg_sec_h_raf_r")
    L("cwgg_sec_h_raf", "RED ARMY FACTION")
    L("cwgg_sec_h_raf_r", "[SEC_Generation]")
    DT("SEC_Generation", [(f"check_variable = {{ cwger_raf_gen = {g} }}", f"cwgg_sec_gen_{g}") for g in (1, 2, 3, 4)])
    for g, t in {1: "First generation: §YBaader-Meinhof§!", 2: "Second generation: §Y'Free the prisoners'§!", 3: "Third generation: §Ythe phantom§!", 4: "§GThe RAF has dissolved§!"}.items():
        L(f"cwgg_sec_gen_{g}", t)
    for j, (key, name, var, hi, col) in enumerate([("cadre", "Active cadre", "cwger_raf_cadre", 60, "red"), ("milieu", "Sympathiser milieu", "cwger_raf_milieu", 100, "gold"),
                                                    ("prisoners", "Prisoners", "cwger_raf_prisoners", 40, "grey")]):
        y = 296 + j * 28
        w.text(f"r_{key}", f"cwgg_sec_r_{key}", 36, y, 170, tab=T, tip="cwgg_sec_raf_tt")
        L(f"cwgg_sec_r_{key}", name)
        w.bar(f"r_{key}", 210, y, var, 0, hi, col, tab=T)
        w.text(f"r_{key}_v", f"cwgg_sec_r_{key}_v", 520, y, 60, tab=T)
        L(f"cwgg_sec_r_{key}_v", f"§Y[?{var}|0]§!")
    L("cwgg_sec_raf_tt", "§YThe RAF§!\nThe §Yactive cadre§! recruits from the §Ysympathiser milieu§!; repression and a weak rule of law feed the milieu, exit offers and calm drain it. Kidnappings need §Yprisoners§! to free. A generation ends when its leaders are in prison - the next one fights to free them.")
    w.text("capab", "cwgg_sec_capab", 600, 296, 150, h=90, tab=T, tip="cwgg_sec_capab_tt")
    L("cwgg_sec_capab", "BKA level §Y[?cwger_bka_level|0]§!/3\nGSG 9 tier §Y[?cwger_gsg9_tier|0]§!/3\nCounter-intel §Y[?cwger_counterintel|0]§!")
    L("cwgg_sec_capab_tt", "§YCapabilities§!\nThe BKA level speeds up the manhunt, slows the RAF's planning and improves foiled attacks. GSG 9 decides raids and rescues. Both are built through the focus tree.")
    w.section("bal", 388, "cwgg_sec_h_balance", T)
    L("cwgg_sec_h_balance", "SECURITY STATE AND RULE OF LAW")
    w.icon("scales", "GFX_cwgg_scales", 240, 424, tab=T, frame="cwgg_g_scales", tip="cwgg_sec_bal_tt")
    w.text("bal_l", "cwgg_sec_bal_l", 36, 432, 200, h=40, tab=T, tip="cwgg_sec_bal_tt")
    w.text("bal_r", "cwgg_sec_bal_r", 548, 432, 200, h=40, fmt_="right", tab=T, tip="cwgg_sec_bal_tt")
    L("cwgg_sec_bal_l", "Security state\n§R[?cwger_security|0]§!")
    L("cwgg_sec_bal_r", "Rule of law\n§G[?cwger_rechtsstaat|0]§!")
    L("cwgg_sec_bal_tt", "§YThe balance§!\nEvery hard measure - dragnet, contact ban, isolation, force-feeding - strengthens the security state and weakens the credibility of the rule of law. A security state above 65 invites abuses (Traube affair, Celle Hole, Kießling affair); a weak rule of law feeds the sympathiser milieu.")
    w.refresh.insert(0, f"if = {{ limit = {{ has_country_flag = {P}_hostage_ultimatum }} set_variable = {{ cwsec_ult_days = cwsec_ult_end }} subtract_from_variable = {{ cwsec_ult_days = global.num_days }} clamp_variable = {{ var = cwsec_ult_days min = 0 max = 99 }} }}")
    w.refresh.append("set_variable = { cwgg_g_scales = cwger_security }\nsubtract_from_variable = { cwgg_g_scales = cwger_rechtsstaat }\ndivide_variable = { cwgg_g_scales = 10 }\nadd_to_variable = { cwgg_g_scales = 11 }\nround_variable = cwgg_g_scales\nclamp_variable = { var = cwgg_g_scales min = 1 max = 21 }")
    w.section("slog", 506, "cwgg_sec_h_log", T)
    L("cwgg_sec_h_log", "SITUATION REPORT")
    for i in range(3):
        w.text(f"log_{i + 1}", f"cwgg_sec_log_{i + 1}", 36, 540 + i * 24, 700, tab=T, vis=f"check_variable = {{ cwsec_log_{i + 1} > 0 }}")
        L(f"cwgg_sec_log_{i + 1}", f"§Y[?cwsec_log_y_{i + 1}|0]§!  [SEC_Log{i + 1}]")
    w.text("hostage_line", "cwgg_sec_hostage_line", 36, 620, 520, tab=T)
    L("cwgg_sec_hostage_line", "[SEC_HostageLine]")
    w.button("to_staff", "GFX_mdcw_cw_button_160", 590, 640, "cwgg_sec_to_staff", "set_variable = { cwsec_tab = 4 }", tab=T, vis=f"has_country_flag = {P}_hostage_ultimatum")
    L("cwgg_sec_to_staff", "Crisis staff")

    # ------------------------------------------------ tab 2: manhunt
    T = 2
    w.section("wanted", 138, "cwgg_sec_h_wanted", T, right="cwgg_sec_h_wanted_r")
    L("cwgg_sec_h_wanted", "WANTED")
    L("cwgg_sec_h_wanted_r", "Trace gain per month: §Y[?cwsec_g_gain|0]§!")
    for i in range(1, 7):
        x = 20 + ((i - 1) % 3) * 248
        y = 172 + ((i - 1) // 3) * 196
        w.icon(f"w{i}_bg", "GFX_cwgg_panel_wanted", x, y, tab=T)
        w.icon(f"w{i}_card", "GFX_cwgg_wanted", x + 30, y + 8, tab=T, frame=f"cwgg_g_w{i}", tip=f"cwgg_sec_w{i}_tt")
        w.icon(f"w{i}_photo", "GFX_cwgg_wanted_photo", x + 36, y + 28, tab=T, frame=f"cwgg_g_wp{i}", tip=f"cwgg_sec_w{i}_tt")
        w.icon(f"w{i}_stamp", "GFX_cwgg_wanted_stamp", x + 36, y + 28, tab=T, frame=f"cwgg_g_w{i}")
        w.text(f"w{i}_name", f"cwgg_sec_w{i}_name", x + 8, y + 122, 220, tab=T)
        w.text(f"w{i}_state", f"cwgg_sec_w{i}_state", x + 8, y + 144, 220, tab=T)
        w.bar(f"w{i}_ort", x + 38, y + 168, f"cwsec_w{i}_ort", 0, 100, "gold", small=True, tab=T)
        w.button(f"w{i}_go", "GFX_mdcw_cw_button_96", x + 104, y + 74, "cwgg_sec_access", f"{S}_access_{i} = yes", tab=T,
                 vis=f"check_variable = {{ cwsec_w{i}_st < 2 }}", enabled=f"{S}_can_access_{i} = yes", tip="cwgg_sec_access_tt")
        w.text(f"w{i}_tag", f"cwgg_sec_w{i}_tag", x + 30, y + 10, 176, fmt_="center", tab=T)
        L(f"cwgg_sec_w{i}_tag", f"[SEC_Tag{i}]")
        L(f"cwgg_sec_w{i}_name", f"§Y[SEC_Name{i}]§!")
        L(f"cwgg_sec_w{i}_state", f"[SEC_State{i}] · trace §Y[?cwsec_w{i}_ort|0]§!")
        L(f"cwgg_sec_w{i}_tt", f"§Y[SEC_Name{i}]§!\nTrace §Y[?cwsec_w{i}_ort|0]§!/100. From 60 the BKA knows enough for an §Yaccess§!.")
        DT(f"SEC_Name{i}", [(f"check_variable = {{ cwsec_gen_cards = {g} }}", f"cwgg_sec_name_{g}_{i}") for g in (1, 2, 3)], "cwgg_sec_name_3_1")
        for g in (1, 2, 3):
            L(f"cwgg_sec_name_{g}_{i}", GEN_NAMES[g][i - 1])
        DT(f"SEC_State{i}", [(f"check_variable = {{ cwsec_w{i}_st = {s} }}", f"cwgg_sec_state_{s}") for s in range(5)])
        DT(f"SEC_Tag{i}", [(f"check_variable = {{ cwsec_w{i}_st = {s} }}", f"cwgg_sec_tag_{s}") for s in range(5)])
        w.refresh.append(f"set_variable = {{ cwgg_g_w{i} = cwsec_w{i}_st }}\nadd_to_variable = {{ cwgg_g_w{i} = 1 }}")
        # photo frame: generation 1 -> 1-6, generation 2 -> 7-12, otherwise (or an empty slot) 13
        w.refresh.append(f"set_variable = {{ cwgg_g_wp{i} = cwsec_gen_cards }}\nsubtract_from_variable = {{ cwgg_g_wp{i} = 1 }}\nmultiply_variable = {{ cwgg_g_wp{i} = 6 }}\nadd_to_variable = {{ cwgg_g_wp{i} = {i} }}\n"
                         f"if = {{ limit = {{ OR = {{ check_variable = {{ cwsec_gen_cards > 2 }} check_variable = {{ cwsec_gen_cards < 1 }} check_variable = {{ cwsec_w{i}_st = 5 }} }} }} set_variable = {{ cwgg_g_wp{i} = 13 }} }}")
    for s, (st, tag) in enumerate([("§Rat large§!", "WANTED"), ("§Ytraced§!", "TRACED"), ("§Garrested§!", "ARRESTED"), ("§gdead§!", "DEAD"), ("§Bleft the group§!", "LEFT THE GROUP")]):
        L(f"cwgg_sec_state_{s}", st)
        L(f"cwgg_sec_tag_{s}", tag)
    DT("SEC_LastName", [(f"check_variable = {{ cwsec_last_card = {i} }}", f"cwgg_sec_lastname_{i}") for i in range(1, 7)])
    for i in range(1, 7):
        L(f"cwgg_sec_lastname_{i}", f"[SEC_Name{i}]")
    L("cwgg_sec_access", "Access")
    L("cwgg_sec_access_tt", "§YAccess§!\nSend the special commando. Costs §Y35§! political power; one access every 45 days.\nBase chance about §Y1 in 3§!; better with the trace (§G+8§! from 75, §G+10§! from 90), the GSG 9 tier and BKA level 2.\n§RFailure§! (most likely): the suspect escapes and the trace falls by 35. §RShootout§! (rarer with a trained GSG 9): the suspect dies or escapes - and the movement gets a martyr.\nA traced suspect may also notice the surveillance and move on before you act.")
    w.refresh.append("set_variable = { cwsec_g_gain = cwger_bka_level }\nmultiply_variable = { cwsec_g_gain = 1.5 }\nadd_to_variable = { cwsec_g_gain = 1 }\nset_temp_variable = { cwsec_t = cwger_raf_milieu }\ndivide_temp_variable = { cwsec_t = 25 }\nsubtract_from_variable = { cwsec_g_gain = cwsec_t }")
    for j, key in enumerate(["raster", "reward", "posters", "kronzeuge", "informant", "dropout"]):
        act_button(key, 20 + j * 124, 568, T)
    w.text("hunt_txt", "cwgg_sec_hunt_txt", 36, 604, 700, h=60, tab=T)
    L("cwgg_sec_hunt_txt", "Every month the BKA gains trace on everyone still at large; the sympathiser milieu and the Stasi's shelter work against it. Arrests also happen by themselves when the BKA is strong. When a generation's leaders are behind bars, the next generation forms - and fights to free them.")

    # ------------------------------------------------ tab 3: protection
    T = 3
    w.section("prot", 138, "cwgg_sec_h_prot", T, right="cwgg_sec_h_prot_r")
    L("cwgg_sec_h_prot", "THE RAF'S TARGETS")
    L("cwgg_sec_h_prot_r", "Protection details: §Y[?cwsec_used|0]§! of §Y[?cwsec_slots|0]§!")
    for ci, (k, name, desc, wts) in enumerate(TARGETS):
        y = 172 + ci * 64
        w.icon(f"tg_{k}_bg", "GFX_cwgg_panel_740", 20, y, tab=T)
        w.icon(f"tg_{k}_icon", "GFX_cwgg_targets", 26, y + 3, tab=T, frame=f"cwgg_g_tgi_{k}")
        w.refresh.append(f"set_variable = {{ cwgg_g_tgi_{k} = {ci + 1} }}")
        w.text(f"tg_{k}_name", f"cwgg_sec_tg_{k}", 76, y + 4, 230, font="hoi_18mbs", tab=T, tip=f"cwgg_sec_tg_{k}_tt")
        if k in TARGET_ACTIVE:
            w.text(f"tg_{k}_desc", f"cwgg_sec_tg_{k}_d", 76, y + 25, 300, tab=T, vis=TARGET_ACTIVE[k])
            w.text(f"tg_{k}_off", f"cwgg_sec_tg_{k}_off", 76, y + 25, 480, tab=T, vis=f"NOT = {{ {TARGET_ACTIVE[k]} }}")
            L(f"cwgg_sec_tg_{k}_off", TARGET_INACTIVE_TEXT[k])
        else:
            w.text(f"tg_{k}_desc", f"cwgg_sec_tg_{k}_d", 76, y + 25, 300, tab=T)
        L(f"cwgg_sec_tg_{k}", name)
        L(f"cwgg_sec_tg_{k}_d", desc)
        L(f"cwgg_sec_tg_{k}_tt", f"§Y{name}§!\n{desc}\n\nPreferred by generation 1 / 2 / 3: {wts[0]} / {wts[1]} / {wts[2]}.\nA protection detail halves the RAF's planning speed here and foils §G65%§! of attacks (§G+5%§! each for BKA levels 2 and 3)."
          + ("\n\n§YOnly a target while US divisions are stationed in a West German state§! (checked every month). Without them the RAF plans nothing here and a protection detail is released." if k == "usforces" else ""))
        act = TARGET_ACTIVE.get(k, "")
        w.bar(f"tg_{k}_plan", 390, y + 14, f"cwsec_plan_{k}", 0, 100, "red", small=True, tab=T, vis=("check_variable = { cwger_bka_level > 1 } " + act).strip())
        w.text(f"tg_{k}_plan_v", f"cwgg_sec_tg_{k}_pv", 390, y + 26, 200, tab=T, vis=act)
        L(f"cwgg_sec_tg_{k}_pv", f"[SEC_Plan_{k}]")
        DT(f"SEC_Plan_{k}", [("check_variable = { cwger_bka_level > 1 }", f"cwgg_sec_plan_exact_{k}"),
                             (f"check_variable = {{ cwger_bka_level = 1 }} check_variable = {{ cwsec_plan_{k} > 49 }}", "cwgg_sec_plan_high"),
                             ("check_variable = { cwger_bka_level = 1 }", "cwgg_sec_plan_low")], "cwgg_sec_plan_unknown")
        L(f"cwgg_sec_plan_exact_{k}", f"Planning §R[?cwsec_plan_{k}|0]%§!")
        w.icon(f"tg_{k}_shield", "GFX_cwgg_shield", 580, y + 10, tab=T, frame=f"cwgg_g_sh_{k}")
        w.refresh.append(f"set_variable = {{ cwgg_g_sh_{k} = cwsec_prot_{k} }}\nadd_to_variable = {{ cwgg_g_sh_{k} = 1 }}")
        w.button(f"tg_{k}_btn", "GFX_mdcw_cw_button_96", 640, y + 10, f"cwgg_sec_prot_btn_{k}", f"{S}_protect_{k} = yes", tab=T,
                 enabled=f"{S}_can_protect_{k} = yes", tip="cwgg_sec_prot_tt")
        L(f"cwgg_sec_prot_btn_{k}", f"[SEC_ProtBtn_{k}]")
        DT(f"SEC_ProtBtn_{k}", [(f"check_variable = {{ cwsec_prot_{k} = 1 }}", "cwgg_sec_prot_off")], "cwgg_sec_prot_on")
    L("cwgg_sec_plan_high", "§RIntelligence: an attack is being prepared§!")
    L("cwgg_sec_plan_low", "§GIntelligence: no sign of preparations§!")
    L("cwgg_sec_plan_unknown", "§gUnknown - needs BKA level 1§!")
    L("cwgg_sec_prot_on", "Protect")
    L("cwgg_sec_prot_off", "Withdraw")
    L("cwgg_sec_prot_tt", "Assign or withdraw a protection detail (§Y10§! political power to assign). Details: §Y[?cwsec_used|0]§! of §Y[?cwsec_slots|0]§!. More come from the focus tree.")
    w.text("prot_txt", "cwgg_sec_prot_txt", 36, 560, 700, h=100, tab=T)
    L("cwgg_sec_prot_txt", "The RAF picks its targets by generation: the first fought the 'imperialist' Americans and the Springer press, the second the justice system and business to free its prisoners, the third the 'military-industrial complex'. Planning speed grows with the active cadre and the milieu and falls with every BKA level. With BKA level 1 we know where an attack is coming; from level 2 we see how far it has got.")

    # ------------------------------------------------ tab 4: prisons and crisis staff
    T = 4
    w.section("prison", 138, "cwgg_sec_h_prison", T, right="cwgg_sec_h_prison_r")
    L("cwgg_sec_h_prison", "PRISON REGIME")
    L("cwgg_sec_h_prison_r", "RAF prisoners: §Y[?cwger_raf_prisoners|0]§!")
    for j, (rid, key, name, desc) in enumerate(REGIMES):
        x = 36 + j * 180
        L(f"cwgg_sec_reg_{key}", name)
        L(f"cwgg_sec_reg_{key}_tt", f"§Y{name}§!\n{desc}\n\nChanging the regime costs §Y25§! political power and is possible every six months.")
        w.button(f"reg_{key}", "GFX_mdcw_cw_button_160", x, 176, f"cwgg_sec_reg_{key}", f"{S}_regime_{key} = yes", tab=T,
                 enabled=f"{S}_can_regime_{key} = yes", tip=f"cwgg_sec_reg_{key}_tt")
    w.icon("reg_hl", "GFX_cwgg_select_160", 34, 174, tab=T, xprop="cwgg_g_reg")
    w.refresh.append("set_variable = { cwgg_g_reg = cwsec_haft }\nadd_to_variable = { cwgg_g_reg = -1 }\nmultiply_variable = { cwgg_g_reg = 180 }\nadd_to_variable = { cwgg_g_reg = 34 }")
    w.text("hunger_lbl", "cwgg_sec_hunger_lbl", 36, 216, 170, tab=T, tip="cwgg_sec_hunger_tt")
    w.bar("hunger", 210, 216, "cwsec_hunger", 0, 100, "red", tab=T)
    L("cwgg_sec_hunger_lbl", "Hunger strike §Y[?cwsec_hunger|0]§!")
    L("cwgg_sec_hunger_tt", "§YHunger strike§!\nGrows while three or more leaders are in prison - fast in isolation, slowly under the normal regime; association ends it. At §R80§! a prisoner may die, which hands the movement a martyr.")
    act_button("forcefeed", 540, 212, T)
    w.section("staff", 252, "cwgg_sec_h_staff", T, right="cwgg_sec_h_staff_r")
    L("cwgg_sec_h_staff", "CRISIS STAFF")
    L("cwgg_sec_h_staff_r", "[SEC_HostageLine]")
    H = f"has_country_flag = {P}_hostage_ultimatum"
    w.text("staff_none", "cwgg_sec_staff_none", 36, 290, 700, h=40, tab=T, vis=f"NOT = {{ {H} }}")
    L("cwgg_sec_staff_none", "No hostage is held. When the RAF kidnaps someone and the government refuses to exchange prisoners, the crisis staff runs the ultimatum from here.")
    w.text("staff_cd", "cwgg_sec_staff_cd", 36, 288, 700, font="hoi_24header", tab=T, vis=H)
    L("cwgg_sec_staff_cd", "§RDEADLINE IN [?cwsec_ult_days|0] DAYS§!")
    w.text("staff_odds", "cwgg_sec_staff_odds", 36, 322, 700, h=40, tab=T, vis=H)
    L("cwgg_sec_staff_odds", "GSG 9 tier §Y[?cwger_gsg9_tier|0]§!, BKA level §Y[?cwger_bka_level|0]§!. A storm succeeds in about §Y[?cwsec_g_storm|0]%§! of cases. Each day bought brings the hiding place closer.")
    w.refresh.append("set_variable = { cwsec_g_storm = cwger_gsg9_tier }\nmultiply_variable = { cwsec_g_storm = 16.7 }\nadd_to_variable = { cwsec_g_storm = 43.75 }\nif = { limit = { check_variable = { cwger_bka_level > 1 } } add_to_variable = { cwsec_g_storm = 6 } }\nif = { limit = { check_variable = { cwger_gsg9_tier = 0 } } set_variable = { cwsec_g_storm = 0 } }\nround_variable = cwsec_g_storm")
    for j, key in enumerate(["storm", "safehouse", "contactban", "stall", "givein"]):
        act_button(key, 20 + j * 148, 366, T, wide=False, vis=H)
    w.section("policy", 420, "cwgg_sec_h_policy", T)
    L("cwgg_sec_h_policy", "POLICY")
    for j, key in enumerate(["kinkel", "ban_right", "ban_pkk", "counterspy", "vetting", "double"]):
        act_button(key, 20 + (j % 3) * 248, 456 + (j // 3) * 40, T, wide=True)
    w.text("policy_txt", "cwgg_sec_policy_txt", 36, 548, 700, h=110, tab=T)
    L("cwgg_sec_policy_txt", "Counter-espionage protects Bonn's channels to East Berlin as much as its secrets. The exit programme, the crown witness rule and the Kinkel initiative drain the milieu - the road that led to the RAF's declaration of 1992 and its dissolution in 1998.")
    # scripted loc for the log
    for line in (1, 2, 3):
        DT(f"SEC_Log{line}", [(f"check_variable = {{ cwsec_log_{line} = {code} }}", f"cwsec_log_{code}") for code, _t in sorted(LOG.values())], "cwgg_rv_none")
    for k, (code, text) in LOG.items():
        L(f"cwsec_log_{code}", text)
    return w
