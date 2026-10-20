"""Systems for West Germany 1970: startup, monthly simulation, leaders and Imperia hooks."""
from cw_lib import *

# --------------------------------------------------------------------------
# Leaders: (key, display name, portrait path, ideology, traits)
PORT = "gfx/leaders/GER/1970/COLDWAR_GER_1970_{}.dds"
DPORT = "gfx/leaders/DDR/1970/COLDWAR_GER_1970_{}.dds"
SPD_LEADERS = {
    1: ("Willy Brandt", "gfx/Leaders/GER/GER_Coldwar_WillyBrandt.dds"),
    2: ("Helmut Schmidt", PORT.format("schmidt")),
    3: ("Hans-Jochen Vogel", PORT.format("vogel")),
    4: ("Johannes Rau", PORT.format("rau")),
    5: ("Oskar Lafontaine", PORT.format("lafontaine")),
    6: ("Björn Engholm", PORT.format("engholm")),
    7: ("Rudolf Scharping", PORT.format("scharping")),
    8: ("Gerhard Schröder", "gfx/Leaders/GER/Gerhard_Schroeder.dds"),
}
CDU_LEADERS = {
    1: ("Rainer Barzel", PORT.format("barzel")),
    2: ("Helmut Kohl", "gfx/Leaders/GER/kohl.dds"),
    3: ("Franz Josef Strauß", PORT.format("strauss")),
    4: ("Ernst Albrecht", PORT.format("albrecht")),
    5: ("Lothar Späth", PORT.format("spaeth")),
    6: ("Wolfgang Schäuble", "gfx/Leaders/GER/Wolfgang_Schauble.dds"),
}
FDP_LEADERS = {1: ("Walter Scheel", PORT.format("scheel")), 2: ("Hans-Dietrich Genscher", PORT.format("genscher")),
               3: ("Otto Graf Lambsdorff", PORT.format("lambsdorff"))}
GREEN_LEADERS = {1: ("Petra Kelly", PORT.format("kelly")), 2: ("Joschka Fischer", "gfx/Leaders/GER/Joschka_Fischer.dds")}
DDR_LEADERS = {
    "honecker": ("Erich Honecker", DPORT.format("honecker"), "communist_state"),
    "stoph": ("Willi Stoph", DPORT.format("stoph"), "communist_state"),
    "krenz": ("Egon Krenz", DPORT.format("krenz"), "communist_state"),
    "modrow": ("Hans Modrow", DPORT.format("modrow"), "communist_state"),
    "demaiziere": ("Lothar de Maizière", DPORT.format("demaiziere"), "conservatism"),
}


def leader(name, pic, ideology, traits=""):
    tr = f" traits = {{ {traits} }}" if traits else ""
    return f'create_country_leader = {{ name = "{name}" picture = "{pic}" expire = "2050.1.1" ideology = {ideology}{tr} }}'


def chain(var, table, ideology, traits):
    parts = []
    for i, (n, pic) in table.items():
        kw = "if" if i == min(table) else "else_if"
        parts.append(f"{kw} = {{ limit = {{ check_variable = {{ {var} = {i} }} }} {leader(n, pic, ideology, traits)} }}")
    first = list(table.values())[0]
    parts.append(f"else = {{ {leader(first[0], first[1], ideology, traits)} }}")
    return "\n".join(parts)


def set_leader_effect():
    return f"""
# Called from set_leader (00_leader_setup_scripted_effects.txt) for GER in the 1970 scenario.
{P}_set_leader = {{
	hidden_effect = {{ kill_country_leader = yes }}
	update_set_politics = yes
	if = {{ limit = {{ has_country_flag = {P}_dark_regime }}
		{leader("The National Directorate", "gfx/leaders/GER/GER_interim.dds", "Nat_Fascism")}
	}}
	else_if = {{ limit = {{ check_variable = {{ ruling_party = 3 }} }}
		{chain("cwger_spd_leader", SPD_LEADERS, "socialism", "western_socialism")}
	}}
	else_if = {{ limit = {{ check_variable = {{ ruling_party = 1 }} }}
		{chain("cwger_cdu_leader", CDU_LEADERS, "conservatism", "western_conservatism")}
	}}
	else_if = {{ limit = {{ check_variable = {{ ruling_party = 16 }} }}
		{chain("cwger_fdp_leader", FDP_LEADERS, "Neutral_Libertarian", "")}
	}}
	else_if = {{ limit = {{ check_variable = {{ ruling_party = 17 }} }}
		if = {{ limit = {{ date < 1990.1.1 }} {leader(*GREEN_LEADERS[1], "Neutral_green")} }}
		else = {{ {leader(*GREEN_LEADERS[2], "Neutral_green")} }}
	}}
	else_if = {{ limit = {{ check_variable = {{ ruling_party = 20 }} }}
		{leader("Franz Schönhuber", PORT.format("schoenhuber"), "Nat_Populism")}
	}}
	else_if = {{ limit = {{ check_variable = {{ ruling_party = 21 }} }}
		{leader("Adolf von Thadden", "gfx/leaders/GER/GER_interim.dds", "Nat_Fascism")}
	}}
	else_if = {{ limit = {{ check_variable = {{ ruling_party = 4 }} }}
		{leader("Herbert Mies", "gfx/leaders/GER/GER_interim.dds", "communist_state")}
	}}
	else = {{
		{leader("Bundesregierung (geschäftsführend)", "gfx/leaders/GER/GER_interim.dds", "conservatism")}
	}}
}}

# Re-create the head of government after a party leadership change.
{P}_refresh_leader = {{
	if = {{
		limit = {{ original_tag = GER IMP_is_1970_scenario = yes }}
		{P}_set_leader = yes
	}}
}}
"""


# --------------------------------------------------------------------------
STARTING_IDEAS = ["bonn_republic", "fading_miracle", "frontline_state", "nuclear_sharing",
                  "hallstein_legacy", "extraparliamentary_opposition", "strong_dmark", "guest_workers"]


def setup_effects():
    return f"""
# History file, 1970 snapshot: replaces the generic 1970 party profile with the 1969 Bundestag result.
{P}_setup_politics = {{
	set_popularities = {{ democratic = 89 communism = 1 fascism = 0 neutrality = 6 nationalist = 4 }}
	IMP_1970_clear_politics = yes
	set_variable = {{ party_pop_array^1 = 0.461 }} # CDU/CSU 46.1
	set_variable = {{ party_pop_array^3 = 0.427 }} # SPD 42.7
	set_variable = {{ party_pop_array^4 = 0.006 }} # DKP/ADF 0.6
	set_variable = {{ party_pop_array^16 = 0.058 }} # FDP 5.8
	set_variable = {{ party_pop_array^21 = 0.043 }} # NPD 4.3
	set_variable = {{ ruling_party = 3 }}
	add_to_array = {{ gov_coalition_array = 16 }}
	set_variable = {{ election_threshold = 0.05 }}
	startup_politics = yes
	set_politics = {{ ruling_party = democratic last_election = "1969.9.28" election_frequency = 48 elections_allowed = yes }}
}}

# on_startup, GER scope.
{P}_initialize = {{
	if = {{
		limit = {{ original_tag = GER IMP_is_1970_scenario = yes NOT = {{ has_country_flag = {P}_initialized }} }}
		set_country_flag = {P}_initialized
		# party leadership
		set_variable = {{ cwger_spd_leader = 1 }}
		set_variable = {{ cwger_cdu_leader = 1 }}
		set_variable = {{ cwger_fdp_leader = 1 }}
		# coalition arithmetic
		set_variable = {{ cwger_seats_total = 496 }}
		set_variable = {{ cwger_majority = 249 }}
		set_variable = {{ cwger_defectors = 0 }}
		set_variable = {{ cwger_fdp_course = -35 }}
		set_variable = {{ cwger_csu_autonomy = 30 }}
		set_variable = {{ cwger_bundesrat_union = 51 }}
		# inner-German and western policy
		set_variable = {{ cwger_ostpolitik = 30 }}
		set_variable = {{ cwger_berlin_access = 45 }}
		set_variable = {{ cwger_westbindung = 70 }}
		set_variable = {{ cwger_unity = 0 }}
		set_variable = {{ cwger_east_burden = 0 }}
		# internal security
		set_variable = {{ cwger_security = 40 }}
		set_variable = {{ cwger_rechtsstaat = 75 }}
		set_variable = {{ cwger_terror_left = 15 }}
		set_variable = {{ cwger_terror_right = 6 }}
		set_variable = {{ cwger_terror_foreign = 10 }}
		set_variable = {{ cwger_raf_gen = 1 }}
		set_variable = {{ cwger_raf_cadre = 12 }}
		set_variable = {{ cwger_raf_milieu = 22 }}
		set_variable = {{ cwger_raf_prisoners = 0 }}
		set_variable = {{ cwger_bka_level = 0 }}
		set_variable = {{ cwger_gsg9_tier = 0 }}
		set_variable = {{ cwger_counterintel = 35 }}
		set_variable = {{ cwger_stasi_penetration = 45 }}
		# society
		set_variable = {{ cwger_peace_movement = 15 }}
		set_variable = {{ cwger_anti_nuclear = 5 }}
		set_variable = {{ cwger_scandal = 10 }}
		set_variable = {{ cwger_bundesbank = 20 }}
		set_variable = {{ cwger_uebersiedler_k = 0 }}
		# starting spirits
		add_ideas = {{ {" ".join(f"{P}_idea_{i}" for i in STARTING_IDEAS)} }}
		# social partnership: DGB, BDI/BDA and the Mittelstand
		if = {{ limit = {{ NOT = {{ has_idea = labour_unions }} }} add_ideas = labour_unions }}
		if = {{ limit = {{ NOT = {{ has_idea = industrial_conglomerates }} }} add_ideas = industrial_conglomerates }}
		if = {{ limit = {{ NOT = {{ has_idea = small_medium_business_owners }} }} add_ideas = small_medium_business_owners }}
		set_variable = {{ labour_unions_opinion = 68 }}
		set_variable = {{ industrial_conglomerates_opinion = 58 }}
		set_variable = {{ small_medium_business_owners_opinion = 62 }}
		add_dynamic_modifier = {{ modifier = {P}_state_of_the_republic }}
		set_power_balance = {{ id = {P}_deutschlandpolitik left_side = {P}_bop_abgrenzung right_side = {P}_bop_annaeherung set_value = -0.4 }}
		if = {{ limit = {{ country_exists = DDR }} DDR = {{ {P}_initialize_ddr = yes }} }}
		{P}_assert_1969_coalition = yes
		{P}_update_bundestag = yes
		{P}_update_modifiers = yes
		{P}_rv_setup = yes
		{P}_sec_setup = yes
		{P}_core_setup = yes
		country_event = {{ id = {EVG}.1 days = 2 }}
	}}
}}

# The 1969 result is SPD + FDP. Other startup scripts must not leave the CDU/CSU in charge
# (the largest single party) - that would trigger a vote of no confidence in the first month.
{P}_assert_1969_coalition = {{
	if = {{
		limit = {{ date < 1970.3.1 OR = {{ NOT = {{ check_variable = {{ ruling_party = 3 }} }} NOT = {{ is_in_array = {{ gov_coalition_array = 16 }} }} }} }}
		log = "[GetDateText]: COLDWAR_GER_1970: restoring the 1969 SPD-FDP coalition (ruling party was [?ruling_party|0])"
		set_variable = {{ ruling_party = 3 }}
		clear_array = gov_coalition_array
		add_to_array = {{ gov_coalition_array = 16 }}
		update_government_coalition_strength = yes
	}}
}}

{P}_initialize_ddr = {{
	if = {{
		limit = {{ NOT = {{ has_country_flag = {P}_ddr_initialized }} }}
		set_country_flag = {P}_ddr_initialized
		set_variable = {{ cwddr_hard_currency = 30 }}
		set_variable = {{ cwddr_west_dependency = 10 }}
		set_variable = {{ cwddr_exit_pressure = 30 }}
		set_variable = {{ cwddr_west_media = 45 }}
		set_variable = {{ cwddr_opposition = 8 }}
		set_variable = {{ cwddr_sed_control = 85 }}
		set_variable = {{ cwddr_moscow_backing = 90 }}
		set_variable = {{ cwddr_recognition = 15 }}
		set_variable = {{ cwddr_crisis = 20 }}
		set_variable = {{ cwddr_wende_stage = 0 }}
		set_variable = {{ cwddr_min_exchange = 10 }}
		add_dynamic_modifier = {{ modifier = {P}_ddr_inner_german }}
	}}
}}
"""


def bundestag_effect():
    slots = [1, 3, 4, 5, 16, 17, 20, 21, 22]
    sum_lines = "\n".join(
        f"if = {{ limit = {{ check_variable = {{ party_pop_elect_array^{s} > 0.0499 }} }} add_to_temp_variable = {{ cwger_t_sum = party_pop_elect_array^{s} }} }}"
        for s in slots)
    return f"""
# Seat arithmetic from the LAST FEDERAL ELECTION RESULT (MD's party_pop_elect_array, written by
# hold_elections), not from today's polls: between elections the Bundestag only changes through
# coalition changes and defectors - as in a roleplay game where the vote has been counted.
# Parties above the 5% hurdle share the seats; defectors are subtracted from the government side.
{P}_update_bundestag = {{
	set_temp_variable = {{ cwger_t_sum = 0 }}
	{sum_lines}
	set_temp_variable = {{ cwger_t_gov = 0 }}
	if = {{ limit = {{ has_variable = ruling_party check_variable = {{ party_pop_elect_array^ruling_party > 0.0499 }} }}
		add_to_temp_variable = {{ cwger_t_gov = party_pop_elect_array^ruling_party }}
	}}
	for_each_loop = {{
		array = gov_coalition_array
		value = v
		if = {{ limit = {{ check_variable = {{ party_pop_elect_array^v > 0.0499 }} }} add_to_temp_variable = {{ cwger_t_gov = party_pop_elect_array^v }} }}
	}}
	if = {{ limit = {{ check_variable = {{ cwger_t_sum < 0.01 }} }} set_temp_variable = {{ cwger_t_sum = 1 }} }}
	set_variable = {{ cwger_seats_gov = cwger_t_gov }}
	divide_variable = {{ cwger_seats_gov = cwger_t_sum }}
	multiply_variable = {{ cwger_seats_gov = cwger_seats_total }}
	round_variable = cwger_seats_gov
	subtract_from_variable = {{ cwger_seats_gov = cwger_defectors }}
	set_variable = {{ cwger_seats_opp = cwger_seats_total }}
	subtract_from_variable = {{ cwger_seats_opp = cwger_seats_gov }}
	set_variable = {{ cwger_margin = cwger_seats_gov }}
	subtract_from_variable = {{ cwger_margin = cwger_majority }}
}}
"""


def modifier_effect():
    return f"""
# Feeds the 'State of the Republic' and GDR dynamic modifiers from the system meters.
{P}_update_modifiers = {{
	# security state: order but at the price of liberal credibility
	set_variable = {{ cwger_dm_police = cwger_security }}
	subtract_from_variable = {{ cwger_dm_police = 40 }}
	multiply_variable = {{ cwger_dm_police = 0.004 }}
	set_variable = {{ cwger_dm_stab = cwger_rechtsstaat }}
	subtract_from_variable = {{ cwger_dm_stab = 60 }}
	multiply_variable = {{ cwger_dm_stab = 0.001 }}
	set_temp_variable = {{ cwger_t = cwger_terror_left }}
	add_to_temp_variable = {{ cwger_t = cwger_terror_right }}
	add_to_temp_variable = {{ cwger_t = cwger_terror_foreign }}
	multiply_temp_variable = {{ cwger_t = -0.0006 }}
	add_to_variable = {{ cwger_dm_stab = cwger_t }}
	set_variable = {{ cwger_dm_pp = cwger_scandal }}
	multiply_variable = {{ cwger_dm_pp = -0.002 }}
	add_to_variable = {{ cwger_dm_pp = 0.02 }}
	set_variable = {{ cwger_dm_interest = cwger_bundesbank }}
	subtract_from_variable = {{ cwger_dm_interest = 30 }}
	multiply_variable = {{ cwger_dm_interest = 0.004 }}
	set_variable = {{ cwger_dm_ideo = cwger_westbindung }}
	subtract_from_variable = {{ cwger_dm_ideo = 50 }}
	multiply_variable = {{ cwger_dm_ideo = 0.002 }}
	set_variable = {{ cwger_dm_trade = cwger_ostpolitik }}
	multiply_variable = {{ cwger_dm_trade = 0.002 }}
	# a hostile Bundesrat costs political capital until a package deal is struck
	if = {{
		limit = {{
			NOT = {{ has_country_flag = {P}_bundesrat_deal }}
			OR = {{
				AND = {{ check_variable = {{ ruling_party = 3 }} check_variable = {{ cwger_bundesrat_union > 50 }} }}
				AND = {{ check_variable = {{ ruling_party = 1 }} check_variable = {{ cwger_bundesrat_union < 50 }} }}
			}}
		}}
		subtract_from_variable = {{ cwger_dm_pp = 0.08 }}
		set_country_flag = {P}_bundesrat_hostile
	}}
	else = {{ clr_country_flag = {P}_bundesrat_hostile }}
	# the peace movement lowers war support, the burden of the East lowers tax income
	set_variable = {{ cwger_dm_ws = 0 }}
	if = {{ limit = {{ check_variable = {{ cwger_peace_movement > 30 }} }}
		set_variable = {{ cwger_dm_ws = cwger_peace_movement }}
		subtract_from_variable = {{ cwger_dm_ws = 30 }}
		multiply_variable = {{ cwger_dm_ws = -0.003 }}
	}}
	set_variable = {{ cwger_dm_tax = cwger_east_burden }}
	multiply_variable = {{ cwger_dm_tax = -0.0015 }}
	# Stasi penetration slows research: plans and prototypes end up in East Berlin
	set_variable = {{ cwger_dm_research = cwger_stasi_penetration }}
	subtract_from_variable = {{ cwger_dm_research = cwger_counterintel }}
	if = {{ limit = {{ check_variable = {{ cwger_dm_research < 0 }} }} set_variable = {{ cwger_dm_research = 0 }} }}
	multiply_variable = {{ cwger_dm_research = -0.001 }}
	# MD counter-terror system: BKA capability and GSG 9 feed the national detection and defence values
	set_variable = {{ cwger_dm_ct_detect = cwger_bka_level }}
	multiply_variable = {{ cwger_dm_ct_detect = 0.05 }}
	set_temp_variable = {{ cwger_t = cwger_counterintel }}
	multiply_temp_variable = {{ cwger_t = 0.001 }}
	add_to_variable = {{ cwger_dm_ct_detect = cwger_t }}
	set_variable = {{ cwger_dm_ct_defence = cwger_gsg9_tier }}
	multiply_variable = {{ cwger_dm_ct_defence = 0.05 }}
	if = {{
		limit = {{ country_exists = DDR }}
		DDR = {{
			set_variable = {{ cwddr_dm_stab = cwddr_crisis }}
			subtract_from_variable = {{ cwddr_dm_stab = 30 }}
			multiply_variable = {{ cwddr_dm_stab = -0.003 }}
			set_variable = {{ cwddr_dm_consumer = cwddr_hard_currency }}
			multiply_variable = {{ cwddr_dm_consumer = 0.0015 }}
			set_variable = {{ cwddr_dm_pp = cwddr_sed_control }}
			subtract_from_variable = {{ cwddr_dm_pp = 60 }}
			multiply_variable = {{ cwddr_dm_pp = 0.002 }}
			# people who leave are missing in the factories
			set_variable = {{ cwddr_dm_workforce = cwddr_exit_pressure }}
			multiply_variable = {{ cwddr_dm_workforce = -0.0008 }}
			force_update_dynamic_modifier = yes
		}}
	}}
	force_update_dynamic_modifier = yes
}}
"""


def terror_effects():
    return f"""
# ----------------------------------------------------------------- terrorism
{P}_terror_tick = {{
	# RAF sympathiser milieu: repression and a weak rule of law feed it, integration drains it
	if = {{ limit = {{ check_variable = {{ cwger_security > 60 }} }} add_to_variable = {{ cwger_raf_milieu = 0.5 }} }}
	if = {{ limit = {{ check_variable = {{ cwger_rechtsstaat < 50 }} }} add_to_variable = {{ cwger_raf_milieu = 0.4 }} }}
	if = {{ limit = {{ has_country_flag = {P}_kinkel_initiative }} add_to_variable = {{ cwger_raf_milieu = -0.8 }} }}
	if = {{ limit = {{ has_country_flag = {P}_hunger_strike }} add_to_variable = {{ cwger_raf_milieu = 0.6 }} }}
	add_to_variable = {{ cwger_raf_milieu = -0.15 }}
	clamp_variable = {{ var = cwger_raf_milieu min = 0 max = 100 }}
	# recruitment and attrition of the underground
	if = {{ limit = {{ check_variable = {{ cwger_raf_gen < 4 }} }}
		set_temp_variable = {{ cwger_t = cwger_raf_milieu }}
		multiply_temp_variable = {{ cwger_t = 0.018 }}
		add_to_variable = {{ cwger_raf_cadre = cwger_t }}
	}}
	# national counter-terror detection from the MD counter-terror system helps every manhunt
	set_temp_variable = {{ cwger_t_ct = modifier@terror_threat_detection_modifier }}
	random_list = {{
		94 = {{ }}
		6 = {{
			modifier = {{ add = 3 check_variable = {{ cwger_t_ct > 0.1 }} }}
			modifier = {{ add = 3 check_variable = {{ cwger_t_ct > 0.25 }} }}
			modifier = {{ add = 4 check_variable = {{ cwger_bka_level > 0 }} }}
			modifier = {{ add = 4 check_variable = {{ cwger_bka_level > 1 }} }}
			modifier = {{ add = 3 check_variable = {{ cwger_bka_level > 2 }} }}
			modifier = {{ add = 3 check_variable = {{ cwger_security > 60 }} }}
			modifier = {{ factor = 0.6 check_variable = {{ cwger_raf_gen = 3 }} }}
			modifier = {{ factor = 0 check_variable = {{ cwger_raf_cadre < 3 }} }}
			{P}_raf_arrests = yes
		}}
	}}
	clamp_variable = {{ var = cwger_raf_cadre min = 0 max = 120 }}
	# threat values
	set_variable = {{ cwger_terror_left = cwger_raf_cadre }}
	multiply_variable = {{ cwger_terror_left = 0.9 }}
	set_temp_variable = {{ cwger_t = cwger_raf_milieu }}
	multiply_temp_variable = {{ cwger_t = 0.35 }}
	add_to_variable = {{ cwger_terror_left = cwger_t }}
	if = {{ limit = {{ NOT = {{ has_country_flag = {P}_j2m_dissolved }} date < 1980.6.2 }} add_to_variable = {{ cwger_terror_left = 5 }} }}
	if = {{ limit = {{ NOT = {{ has_country_flag = {P}_rz_dissolved }} date > 1973.1.1 date < 1995.1.1 }} add_to_variable = {{ cwger_terror_left = 4 }} }}
	clamp_variable = {{ var = cwger_terror_left min = 0 max = 100 }}
	# right-wing threat: far-right vote, refugee arrivals, unemployment-driven anger
	set_variable = {{ cwger_terror_right = party_pop_array^21 }}
	add_to_variable = {{ cwger_terror_right = party_pop_array^20 }}
	add_to_variable = {{ cwger_terror_right = party_pop_array^22 }}
	multiply_variable = {{ cwger_terror_right = 220 }}
	add_to_variable = {{ cwger_terror_right = 4 }}
	if = {{ limit = {{ has_country_flag = {P}_wsg_hoffmann_active }} add_to_variable = {{ cwger_terror_right = 8 }} }}
	if = {{ limit = {{ has_country_flag = {P}_asylum_surge }} add_to_variable = {{ cwger_terror_right = 14 }} }}
	if = {{ limit = {{ has_country_flag = {P}_far_right_banned }} add_to_variable = {{ cwger_terror_right = -6 }} }}
	clamp_variable = {{ var = cwger_terror_right min = 0 max = 100 }}
	# foreign and state-linked threat follows world tension and the Middle East
	set_variable = {{ cwger_terror_foreign = 8 }}
	if = {{ limit = {{ has_global_flag = mdcw_cw_initialized }}
		set_temp_variable = {{ cwger_t = global.mdcw_cw_tension }}
		multiply_temp_variable = {{ cwger_t = 0.15 }}
		add_to_variable = {{ cwger_terror_foreign = cwger_t }}
	}}
	if = {{ limit = {{ date > 1983.1.1 date < 1990.1.1 }} add_to_variable = {{ cwger_terror_foreign = 6 }} }}
	if = {{ limit = {{ date > 1992.1.1 date < 2000.1.1 NOT = {{ has_country_flag = {P}_pkk_banned }} }} add_to_variable = {{ cwger_terror_foreign = 8 }} }}
	clamp_variable = {{ var = cwger_terror_foreign min = 0 max = 100 }}
	# attack rolls (one vector per month at most)
	if = {{
		limit = {{ NOT = {{ has_country_flag = {P}_attack_cooldown }} }}
		random_list = {{
			100 = {{ }}
			# RAF attacks come from the planning model in the internal security window ({P}_sec_tick)
			1 = {{
				modifier = {{ add = 3 check_variable = {{ cwger_terror_right > 25 }} }}
				modifier = {{ add = 4 check_variable = {{ cwger_terror_right > 45 }} }}
				set_country_flag = {{ flag = {P}_attack_cooldown days = 60 value = 1 }}
				country_event = {{ id = {EVG}.62 days = 1 }}
			}}
			1 = {{
				modifier = {{ add = 2 check_variable = {{ cwger_terror_foreign > 20 }} }}
				modifier = {{ add = 3 check_variable = {{ cwger_terror_foreign > 35 }} }}
				set_country_flag = {{ flag = {P}_attack_cooldown days = 60 value = 1 }}
				country_event = {{ id = {EVG}.65 days = 1 }}
			}}
		}}
	}}
	# generation changes of the RAF
	if = {{
		limit = {{ check_variable = {{ cwger_raf_gen = 1 }} check_variable = {{ cwger_raf_prisoners > 3 }} date > 1972.6.1 }}
		set_variable = {{ cwger_raf_gen = 2 }}
		country_event = {{ id = {EVG}.50 days = 3 }}
	}}
	if = {{
		limit = {{ check_variable = {{ cwger_raf_gen = 2 }} has_country_flag = {P}_deutscher_herbst_over }}
		set_variable = {{ cwger_raf_gen = 3 }}
		country_event = {{ id = {EVG}.58 days = 120 }}
	}}
	if = {{
		limit = {{ check_variable = {{ cwger_raf_gen = 3 }} check_variable = {{ cwger_raf_milieu < 10 }} check_variable = {{ cwger_raf_cadre < 6 }} date > 1990.1.1 }}
		set_variable = {{ cwger_raf_gen = 4 }}
		country_event = {{ id = {EVG}.60 days = 5 }}
	}}
}}

{P}_raf_arrests = {{
	set_temp_variable = {{ cwger_t = cwger_raf_cadre }}
	multiply_temp_variable = {{ cwger_t = 0.2 }}
	add_to_temp_variable = {{ cwger_t = 1 }}
	subtract_from_variable = {{ cwger_raf_cadre = cwger_t }}
	add_to_variable = {{ cwger_raf_prisoners = 1 }}
	{P}_sec_arrest_best = yes
	if = {{ limit = {{ check_variable = {{ cwger_bka_level > 2 }} }} random_list = {{ 50 = {{ }} 50 = {{ add_to_variable = {{ cwger_raf_prisoners = 1 }} {P}_sec_arrest_best = yes }} }} }}
	if = {{ limit = {{ NOT = {{ has_country_flag = {P}_arrest_news_cooldown }} }}
		set_country_flag = {{ flag = {P}_arrest_news_cooldown days = 300 value = 1 }}
		country_event = {{ id = {EVG}.49 days = 1 }}
	}}
}}

# Chooses the kind of RAF action from the generation, the number of prisoners and
# whether the state has already shown itself open to blackmail.
{P}_raf_attack = {{
	set_country_flag = {{ flag = {P}_attack_cooldown days = 75 value = 1 }}
	random_list = {{
		40 = {{
			modifier = {{ factor = 0.5 check_variable = {{ cwger_raf_gen > 1 }} }}
			country_event = {{ id = {EVG}.51 days = 1 }}
		}}
		25 = {{
			modifier = {{ factor = 0 check_variable = {{ cwger_raf_gen = 1 }} }}
			modifier = {{ factor = 1.5 check_variable = {{ cwger_raf_gen = 3 }} }}
			country_event = {{ id = {EVG}.52 days = 1 }}
		}}
		30 = {{
			modifier = {{ factor = 0 check_variable = {{ cwger_raf_prisoners < 3 }} }}
			modifier = {{ factor = 0 has_country_flag = {P}_hostage_crisis_active }}
			modifier = {{ factor = 2 has_country_flag = {P}_state_blackmailable }}
			modifier = {{ factor = 0.3 check_variable = {{ cwger_raf_gen = 3 }} }}
			set_country_flag = {P}_hostage_crisis_active
			country_event = {{ id = {EVG}.53 days = 1 }}
		}}
	}}
}}

# GSG 9 rescue roll. Sets {P}_rescue_success or {P}_rescue_failure for the calling event.
{P}_rescue_roll = {{
	clr_country_flag = {P}_rescue_success
	clr_country_flag = {P}_rescue_failure
	random_list = {{
		35 = {{
			modifier = {{ add = 20 check_variable = {{ cwger_gsg9_tier > 0 }} }}
			modifier = {{ add = 15 check_variable = {{ cwger_gsg9_tier > 1 }} }}
			modifier = {{ add = 15 check_variable = {{ cwger_gsg9_tier > 2 }} }}
			modifier = {{ add = 5 check_variable = {{ cwger_bka_level > 1 }} }}
			set_country_flag = {P}_rescue_success
		}}
		45 = {{
			set_country_flag = {P}_rescue_failure
		}}
	}}
}}
"""


def inner_german_effects():
    return f"""
# --------------------------------------------------------- inner-German dynamics
# Monthly, called in GER scope. Moves the GDR meters and checks the stages of a GDR crisis.
# Nothing here is dated: the crisis comes when the numbers say so, or never.
{P}_inner_german_tick = {{
	if = {{
		limit = {{ country_exists = DDR DDR = {{ has_country_flag = {P}_ddr_initialized }} NOT = {{ has_global_flag = {P}_unity_achieved }} }}
		set_temp_variable = {{ cwger_t_ost = cwger_ostpolitik }}
		DDR = {{
			# hard currency: the plan economy runs deeper into Western debt every year
			add_to_variable = {{ cwddr_hard_currency = 0.17 }}
			if = {{ limit = {{ date > 1979.6.1 }} add_to_variable = {{ cwddr_hard_currency = 0.08 }} }}
			if = {{ limit = {{ has_global_flag = {P}_swing_high }} add_to_variable = {{ cwddr_hard_currency = -0.06 }} }}
			# Western television and radio
			add_to_variable = {{ cwddr_west_media = 0.03 }}
			if = {{ limit = {{ check_variable = {{ cwger_t_ost > 60 }} }} add_to_variable = {{ cwddr_west_media = 0.04 }} }}
			# exit pressure
			add_to_variable = {{ cwddr_exit_pressure = 0.03 }}
			set_temp_variable = {{ t = cwddr_west_media }}
			subtract_from_temp_variable = {{ t = 50 }}
			multiply_temp_variable = {{ t = 0.002 }}
			add_to_variable = {{ cwddr_exit_pressure = t }}
			set_temp_variable = {{ t = cwddr_hard_currency }}
			subtract_from_temp_variable = {{ t = 50 }}
			multiply_temp_variable = {{ t = 0.002 }}
			add_to_variable = {{ cwddr_exit_pressure = t }}
			set_temp_variable = {{ t = cwger_t_ost }}
			subtract_from_temp_variable = {{ t = 50 }}
			multiply_temp_variable = {{ t = 0.0015 }}
			add_to_variable = {{ cwddr_exit_pressure = t }}
			# civic opposition grows when people want out and the Party cannot answer
			add_to_variable = {{ cwddr_opposition = 0.02 }}
			if = {{ limit = {{ check_variable = {{ cwddr_exit_pressure > 50 }} }}
				set_temp_variable = {{ t = cwddr_exit_pressure }}
				subtract_from_temp_variable = {{ t = 50 }}
				multiply_temp_variable = {{ t = 0.004 }}
				add_to_variable = {{ cwddr_opposition = t }}
			}}
			if = {{ limit = {{ check_variable = {{ cwddr_sed_control > 80 }} }} add_to_variable = {{ cwddr_opposition = -0.05 }} }}
			# Moscow's guarantee follows the Soviet course
			if = {{ limit = {{ country_exists = SOV SOV = {{ has_completed_focus = COLDWAR_SOV_gor_the_sinatra_doctrine }} }} add_to_variable = {{ cwddr_moscow_backing = -1.5 }} }}
			else_if = {{ limit = {{ country_exists = SOV SOV = {{ OR = {{ has_completed_focus = COLDWAR_SOV_gor_new_thinking has_completed_focus = COLDWAR_SOV_gor_glasnost_first }} }} }} add_to_variable = {{ cwddr_moscow_backing = -0.6 }} }}
			else_if = {{ limit = {{ country_exists = SOV SOV = {{ has_completed_focus = COLDWAR_SOV_the_brezhnev_doctrine }} }} add_to_variable = {{ cwddr_moscow_backing = 0.2 }} }}
			if = {{ limit = {{ date > 1986.6.1 }} add_to_variable = {{ cwddr_moscow_backing = -0.25 }} }}
			if = {{ limit = {{ NOT = {{ country_exists = SOV }} }} add_to_variable = {{ cwddr_moscow_backing = -5 }} }}
			# SED control relaxes towards a level set by Moscow and the opposition
			set_temp_variable = {{ t = cwddr_moscow_backing }}
			multiply_temp_variable = {{ t = 0.4 }}
			add_to_temp_variable = {{ t = 55 }}
			set_temp_variable = {{ t2 = cwddr_opposition }}
			multiply_temp_variable = {{ t2 = 0.4 }}
			subtract_from_temp_variable = {{ t = t2 }}
			subtract_from_temp_variable = {{ t = cwddr_sed_control }}
			multiply_temp_variable = {{ t = 0.05 }}
			add_to_variable = {{ cwddr_sed_control = t }}
			clamp_variable = {{ var = cwddr_hard_currency min = 0 max = 100 }}
			clamp_variable = {{ var = cwddr_west_media min = 0 max = 95 }}
			clamp_variable = {{ var = cwddr_exit_pressure min = 0 max = 100 }}
			clamp_variable = {{ var = cwddr_opposition min = 0 max = 100 }}
			clamp_variable = {{ var = cwddr_moscow_backing min = 0 max = 100 }}
			clamp_variable = {{ var = cwddr_sed_control min = 0 max = 100 }}
			# crisis index
			set_variable = {{ cwddr_crisis = cwddr_exit_pressure }}
			multiply_variable = {{ cwddr_crisis = 0.3 }}
			set_temp_variable = {{ t = cwddr_opposition }}
			multiply_temp_variable = {{ t = 0.25 }}
			add_to_variable = {{ cwddr_crisis = t }}
			set_temp_variable = {{ t = cwddr_hard_currency }}
			multiply_temp_variable = {{ t = 0.2 }}
			add_to_variable = {{ cwddr_crisis = t }}
			set_temp_variable = {{ t = cwddr_west_media }}
			multiply_temp_variable = {{ t = 0.1 }}
			add_to_variable = {{ cwddr_crisis = t }}
			set_temp_variable = {{ t = 100 }}
			subtract_from_temp_variable = {{ t = cwddr_sed_control }}
			multiply_temp_variable = {{ t = 0.15 }}
			add_to_variable = {{ cwddr_crisis = t }}
			if = {{ limit = {{ check_variable = {{ cwddr_moscow_backing < 50 }} }}
				set_temp_variable = {{ t = 50 }}
				subtract_from_temp_variable = {{ t = cwddr_moscow_backing }}
				multiply_temp_variable = {{ t = 0.6 }}
				add_to_variable = {{ cwddr_crisis = t }}
			}}
			clamp_variable = {{ var = cwddr_crisis min = 0 max = 100 }}
		}}
		{P}_check_wende = yes
	}}
}}

# Stages of a GDR crisis. 0 calm, 1 exit wave, 2 street protests, 3 open border,
# 4 transition, 5 unity negotiations, 9 crushed (Chinese solution), 10 settled.
{P}_check_wende = {{
	if = {{
		limit = {{ DDR = {{ check_variable = {{ cwddr_wende_stage = 0 }} check_variable = {{ cwddr_crisis > 49 }} }} date > 1974.1.1 }}
		DDR = {{ set_variable = {{ cwddr_wende_stage = 1 }} }}
		country_event = {{ id = {EVG}.130 days = 2 }}
		DDR = {{ country_event = {{ id = {EVD}.30 days = 2 }} }}
	}}
	else_if = {{
		limit = {{ DDR = {{ check_variable = {{ cwddr_wende_stage = 1 }} check_variable = {{ cwddr_crisis > 59 }} }} }}
		DDR = {{ set_variable = {{ cwddr_wende_stage = 2 }} country_event = {{ id = {EVD}.31 days = 3 }} }}
	}}
	else_if = {{
		limit = {{ DDR = {{ check_variable = {{ cwddr_wende_stage = 9 }} check_variable = {{ cwddr_crisis > 74 }} }} }}
		DDR = {{ set_variable = {{ cwddr_wende_stage = 2 }} country_event = {{ id = {EVD}.38 days = 3 }} }}
	}}
	else_if = {{
		limit = {{ DDR = {{ check_variable = {{ cwddr_wende_stage = 1 }} check_variable = {{ cwddr_crisis < 35 }} }} }}
		DDR = {{ set_variable = {{ cwddr_wende_stage = 0 }} }}
	}}
}}

# Stage 3: the border opens.
{P}_wall_opens = {{
	set_global_flag = {P}_wall_open
	DDR = {{
		set_variable = {{ cwddr_wende_stage = 3 }}
		add_to_variable = {{ cwddr_sed_control = -25 }}
		add_to_variable = {{ cwddr_exit_pressure = 15 }}
		clamp_variable = {{ var = cwddr_sed_control min = 0 max = 100 }}
		clamp_variable = {{ var = cwddr_exit_pressure min = 0 max = 100 }}
		country_event = {{ id = {EVD}.33 days = 1 }}
	}}
	GER = {{ country_event = {{ id = {EVG}.133 days = 1 }} }}
}}
"""


def unity_effects():
    return f"""
# ---------------------------------------------------------------------- unity
# Transfers the GDR's states and armed forces to the Federal Republic.
{P}_absorb_ddr = {{
	if = {{
		limit = {{ country_exists = DDR }}
		set_global_flag = {P}_unity_achieved
		annex_country = {{ target = DDR transfer_troops = yes }}
		every_state = {{
			limit = {{ is_core_of = DDR }}
			add_core_of = GER
		}}
		set_variable = {{ cwger_seats_total = 662 }}
		set_variable = {{ cwger_majority = 332 }}
		set_variable = {{ cwger_east_burden = 70 }}
		add_ideas = {P}_idea_aufbau_ost
		if = {{ limit = {{ has_idea = {P}_idea_hallstein_legacy }} remove_ideas = {P}_idea_hallstein_legacy }}
		if = {{ limit = {{ has_idea = {P}_idea_frontline_state }} remove_ideas = {P}_idea_frontline_state }}
		# the eastern electorate brings the PDS and the eastern civic movement
		set_temp_variable = {{ party_index = 5 }}
		set_temp_variable = {{ party_popularity_increase = 0.024 }}
		set_temp_variable = {{ temp_outlook_increase = 0.024 }}
		change_relative_party_popularity = yes
		{P}_update_bundestag = yes
	}}
}}

{P}_unity_art23 = {{
	{P}_absorb_ddr = yes
	set_global_flag = {P}_unity_art23
	add_ideas = {P}_idea_two_plus_four
	add_stability = 0.05
	add_political_power = 150
}}

{P}_unity_art146 = {{
	{P}_absorb_ddr = yes
	set_global_flag = {P}_unity_art146
	add_ideas = {P}_idea_new_constitution
	add_stability = 0.08
}}

{P}_unity_neutral = {{
	{P}_absorb_ddr = yes
	set_global_flag = {P}_unity_neutral
	add_ideas = {P}_idea_neutral_germany
	if = {{ limit = {{ has_idea = NATO_member }} NATO_leave = yes }}
	if = {{ limit = {{ is_in_faction = yes }} leave_faction = yes }}
	set_temp_variable = {{ modify_europeanism = -10 }}
	set_temp_variable = {{ modify_europeanism_target = ROOT.id }}
	europeanism_change = yes
	if = {{
		limit = {{ has_global_flag = mdcw_cw_initialized }}
		set_temp_variable = {{ mdcw_cw_new_alignment = 0 }}
		set_temp_variable = {{ mdcw_cw_t_free = 1 }}
		mdcw_cw_change_alignment = yes
	}}
}}

# Confederation: the GDR remains a state but becomes bound to the Federal Republic.
{P}_confederation = {{
	set_global_flag = {P}_confederation
	every_other_country = {{ limit = {{ DDR = {{ is_subject_of = PREV }} }} end_puppet = DDR }}
	DDR = {{ if = {{ limit = {{ is_in_faction = yes }} leave_faction = yes }} }}
	set_autonomy = {{ target = DDR autonomy_state = autonomy_puppet_state }}
	DDR = {{ set_variable = {{ cwddr_wende_stage = 10 }} }}
	add_ideas = {P}_idea_german_confederation
}}
"""


def imperia_effects():
    return f"""
# ------------------------------------------------------------- Imperia hooks
# THIS = GER, PREV = target. Lifts the Imperia military (COCOM) sanction on the target.
{P}_lift_mil_sanction_on_prev = {{
	PREV = {{
		if = {{
			limit = {{ is_in_array = {{ imp_mil_sanc_on_us = ROOT }} }}
			remove_from_array = {{ array = imp_mil_sanc_on_us value = ROOT }}
			remove_opinion_modifier = {{ target = ROOT modifier = opinion_mil_sanctioned_us }}
			ROOT = {{ remove_from_array = {{ array = imp_mil_sanc_by_us value = PREV }} }}
			set_temp_variable = {{ mdcw_cw_t_sanc_type = 4 }}
			if = {{ limit = {{ has_global_flag = mdcw_cw_initialized }} mdcw_cw_on_sanction_lifted = yes }}
		}}
	}}
}}

# THIS = GER (ROOT), PREV = target. Imposes Imperia economic and financial sanctions.
{P}_sanction_prev_economic = {{
	PREV = {{
		IMP_sanctions_add_eco_from_prev = yes
		IMP_sanctions_add_fin_from_prev = yes
		set_temp_variable = {{ mdcw_cw_t_sanc_type = 3 }}
		if = {{ limit = {{ has_global_flag = mdcw_cw_initialized }} mdcw_cw_on_sanction_imposed = yes }}
	}}
}}

{P}_lift_eco_sanction_on_prev = {{
	PREV = {{
		if = {{
			limit = {{ is_in_array = {{ imp_eco_sanc_on_us = ROOT }} }}
			remove_from_array = {{ array = imp_eco_sanc_on_us value = ROOT }}
			remove_opinion_modifier = {{ target = ROOT modifier = opinion_eco_sanctioned_us }}
			ROOT = {{ remove_from_array = {{ array = imp_eco_sanc_by_us value = PREV }} }}
			set_temp_variable = {{ mdcw_cw_t_sanc_type = 3 }}
			if = {{ limit = {{ has_global_flag = mdcw_cw_initialized }} mdcw_cw_on_sanction_lifted = yes }}
		}}
		if = {{
			limit = {{ is_in_array = {{ imp_fin_sanc_on_us = ROOT }} }}
			remove_from_array = {{ array = imp_fin_sanc_on_us value = ROOT }}
			remove_opinion_modifier = {{ target = ROOT modifier = opinion_fin_sanctioned_us }}
			ROOT = {{ remove_from_array = {{ array = imp_fin_sanc_by_us value = PREV }} }}
			set_temp_variable = {{ mdcw_cw_t_sanc_type = 2 }}
			if = {{ limit = {{ has_global_flag = mdcw_cw_initialized }} mdcw_cw_on_sanction_lifted = yes }}
		}}
	}}
}}

# THIS = sponsor (GER), PREV = target. Starts Imperia Public Political Support for the party
# slot in temp cwger_t_party (a party foundation campaign, e.g. Friedrich-Ebert-Stiftung).
{P}_start_foundation_campaign = {{
	if = {{
		limit = {{
			has_global_flag = mdcw_cw_initialized
			has_country_flag = mdcw_cw_initialized
			PREV = {{ has_country_flag = mdcw_cw_initialized }}
		}}
		set_variable = {{ mdcw_cw_send_party = cwger_t_party }}
		mdcw_cw_start_pps = yes
	}}
}}

# THIS = donor (GER), PREV = target. Starts an Imperia assistance programme of type
# temp cwger_t_prog (1-8) and size temp cwger_t_size if capacity allows; otherwise refunds.
{P}_start_programme = {{
	if = {{
		limit = {{ has_global_flag = mdcw_cw_initialized has_country_flag = mdcw_cw_initialized PREV = {{ has_country_flag = mdcw_cw_initialized }} }}
		mdcw_cw_recalculate_capacity = yes
		set_temp_variable = {{ mdcw_cw_t_size = cwger_t_size }}
		if = {{
			limit = {{ check_variable = {{ mdcw_cw_cap_free < cwger_t_size }} }}
			add_political_power = 25
			set_country_flag = {{ flag = {P}_programme_failed days = 5 value = 1 }}
		}}
		else_if = {{ limit = {{ check_variable = {{ cwger_t_prog = 1 }} check_variable = {{ mdcw_cw_p1_size@PREV = 0 }} }} mdcw_cw_start_program_1 = yes }}
		else_if = {{ limit = {{ check_variable = {{ cwger_t_prog = 2 }} check_variable = {{ mdcw_cw_p2_size@PREV = 0 }} }} mdcw_cw_start_program_2 = yes }}
		else_if = {{ limit = {{ check_variable = {{ cwger_t_prog = 3 }} check_variable = {{ mdcw_cw_p3_size@PREV = 0 }} }} mdcw_cw_start_program_3 = yes }}
		else_if = {{ limit = {{ check_variable = {{ cwger_t_prog = 4 }} check_variable = {{ mdcw_cw_p4_size@PREV = 0 }} }} mdcw_cw_start_program_4 = yes }}
		else_if = {{ limit = {{ check_variable = {{ cwger_t_prog = 5 }} check_variable = {{ mdcw_cw_p5_size@PREV = 0 }} }} mdcw_cw_start_program_5 = yes }}
		else_if = {{ limit = {{ check_variable = {{ cwger_t_prog = 6 }} check_variable = {{ mdcw_cw_p6_size@PREV = 0 }} }} mdcw_cw_start_program_6 = yes }}
		else_if = {{ limit = {{ check_variable = {{ cwger_t_prog = 7 }} check_variable = {{ mdcw_cw_p7_size@PREV = 0 }} }} mdcw_cw_start_program_7 = yes }}
		else_if = {{ limit = {{ check_variable = {{ cwger_t_prog = 8 }} check_variable = {{ mdcw_cw_p8_size@PREV = 0 }} }} mdcw_cw_start_program_8 = yes }}
		else = {{ add_political_power = 25 }}
	}}
}}

# Reads Imperia/Cold War states each month and turns them into German consequences.
{P}_imperia_tick = {{
	if = {{
		limit = {{ has_global_flag = mdcw_cw_initialized }}
		# oil shocks reach the Federal Republic through the Imperia oil market
		if = {{
			limit = {{ check_variable = {{ mdcw_cw_oil_crisis_tier > 1 }} NOT = {{ has_country_flag = {P}_oil_shock_seen }} }}
			set_country_flag = {P}_oil_shock_seen
			country_event = {{ id = {EVG}.80 days = 1 }}
		}}
		if = {{
			limit = {{ check_variable = {{ mdcw_cw_oil_crisis_tier > 1 }} has_country_flag = {P}_oil_shock_seen NOT = {{ has_country_flag = {P}_second_oil_shock_seen }} date > 1978.1.1 }}
			set_country_flag = {P}_second_oil_shock_seen
			country_event = {{ id = {EVG}.81 days = 1 }}
		}}
		# high world tension mobilises the peace movement
		if = {{ limit = {{ check_variable = {{ global.mdcw_cw_tension > 59 }} }} add_to_variable = {{ cwger_peace_movement = 0.4 }} }}
		if = {{ limit = {{ check_variable = {{ global.mdcw_cw_tension < 35 }} }} add_to_variable = {{ cwger_peace_movement = -0.2 }} }}
		clamp_variable = {{ var = cwger_peace_movement min = 0 max = 100 }}
		# a war scare at the very top of the tension scale
		if = {{
			limit = {{
				check_variable = {{ global.mdcw_cw_tension > 79 }}
				date > 1979.1.1
				NOT = {{ has_global_flag = {P}_war_scare_seen }}
			}}
			set_global_flag = {P}_war_scare_seen
			country_event = {{ id = {EVG}.92 days = 3 }}
		}}
		# leaving the Western bloc without a plan: estrangement weakens Westbindung
		if = {{ limit = {{ has_country_flag = mdcw_cw_estranged }} add_to_variable = {{ cwger_westbindung = -0.5 }} }}
		if = {{ limit = {{ check_variable = {{ mdcw_cw_alignment = 1 }} NOT = {{ has_country_flag = mdcw_cw_estranged }} }} add_to_variable = {{ cwger_westbindung = 0.05 }} }}
		clamp_variable = {{ var = cwger_westbindung min = 0 max = 100 }}
	}}
	# Soviet tree compatibility: the Quadripartite Agreement is one fact for both sides
	if = {{ limit = {{ has_global_flag = COLDWAR_SOV_berlin_agreement NOT = {{ has_country_flag = {P}_berlin_agreement }} }}
		set_country_flag = {P}_berlin_agreement
		{v("cwger_berlin_access", 15, show=False)}
	}}
}}
"""


def monthly_effects():
    return f"""
# ------------------------------------------------------------------ monthly
{P}_monthly = {{
	if = {{
		limit = {{ original_tag = GER IMP_is_1970_scenario = yes has_country_flag = {P}_initialized }}
		{P}_update_bundestag = yes
		log = "[GetDateText]: COLDWAR_GER_1970 Bundestag: ruling party [?ruling_party|0], government [?cwger_seats_gov|0] of [?cwger_seats_total|0] seats, margin [?cwger_margin|0], defectors [?cwger_defectors|0]; last election CDU [?party_pop_elect_array^1|%1] SPD [?party_pop_elect_array^3|%1] FDP [?party_pop_elect_array^16|%1] Greens [?party_pop_elect_array^17|%1]; coalition partners [?gov_coalition_array^num|0]"
		{P}_terror_tick = yes
		{P}_sec_tick = yes
		{P}_inner_german_tick = yes
		{P}_rv_tick = yes
		{P}_uni_tick = yes
		{P}_imperia_tick = yes
		{P}_politics_tick = yes
		{P}_dark_tick = yes
		{P}_dom_tick = yes
		{P}_bomb_watch = yes
		{P}_gw_tick = yes
		{P}_events_tick = yes
		{P}_mechanics_tick = yes
		{P}_update_modifiers = yes
	}}
}}

{P}_politics_tick = {{
	# scandals surface when pressure has built up
	add_to_variable = {{ cwger_scandal = -0.25 }}
	clamp_variable = {{ var = cwger_scandal min = 0 max = 100 }}
	if = {{
		limit = {{ check_variable = {{ cwger_scandal > 39 }} NOT = {{ has_country_flag = {P}_scandal_cooldown }} }}
		random_list = {{
			80 = {{ }}
			20 = {{
				modifier = {{ add = 15 check_variable = {{ cwger_scandal > 60 }} }}
				set_country_flag = {{ flag = {P}_scandal_cooldown days = 360 value = 1 }}
				country_event = {{ id = {EVG}.100 days = 1 }}
			}}
		}}
	}}
	# Länder elections act as mid-term referendums on Bonn
	random_list = {{
		85 = {{ }}
		15 = {{ country_event = {{ id = {EVG}.25 days = 1 }} }}
	}}
	# the peace and anti-nuclear movements feed the Greens once they exist
	if = {{
		limit = {{ has_country_flag = {P}_greens_founded }}
		if = {{ limit = {{ check_variable = {{ cwger_peace_movement > 50 }} }} {party("greens", 0.0008)} }}
		if = {{ limit = {{ check_variable = {{ cwger_anti_nuclear > 50 }} }} {party("greens", 0.0008)} }}
	}}
	# a shrinking majority invites defections and a constructive vote of no confidence
	if = {{
		limit = {{
			check_variable = {{ cwger_margin < 3 }}
			OR = {{ check_variable = {{ cwger_defectors > 0 }} date > 1971.1.1 }}
			OR = {{ check_variable = {{ ruling_party = 1 }} check_variable = {{ ruling_party = 3 }} }}
			NOT = {{ has_country_flag = {P}_no_confidence_cooldown }}
			NOT = {{ has_country_flag = elections_in_progress }}
		}}
		set_country_flag = {{ flag = {P}_no_confidence_cooldown days = 540 value = 1 }}
		set_country_flag = {P}_majority_crisis
		country_event = {{ id = {EVG}.19 days = 1 }}
	}}
	# FDP drifts with its electorate
	if = {{ limit = {{ check_variable = {{ ruling_party = 1 }} is_in_array = {{ gov_coalition_array = 16 }} }} add_to_variable = {{ cwger_fdp_course = 0.1 }} }}
	clamp_variable = {{ var = cwger_fdp_course min = -100 max = 100 }}
	# the Bundesbank watches inflation (Imperia/MD monetary variables)
	if = {{ limit = {{ check_variable = {{ inflation_rate_var > 0.05 }} }} add_to_variable = {{ cwger_bundesbank = 1 }} }}
	else = {{ add_to_variable = {{ cwger_bundesbank = -0.5 }} }}
	clamp_variable = {{ var = cwger_bundesbank min = 0 max = 100 }}
	if = {{ limit = {{ check_variable = {{ cwger_bundesbank > 70 }} NOT = {{ has_country_flag = {P}_bundesbank_cooldown }} }}
		set_country_flag = {{ flag = {P}_bundesbank_cooldown days = 540 value = 1 }}
		country_event = {{ id = {EVG}.85 days = 1 }}
	}}
	# party leadership succession in opposition
	{P}_leadership_tick = yes
}}

{P}_leadership_tick = {{
	if = {{
		limit = {{ check_variable = {{ cwger_cdu_leader = 1 }} date > 1973.6.12 NOT = {{ check_variable = {{ ruling_party = 1 }} }} }}
		set_variable = {{ cwger_cdu_leader = 2 }}
		country_event = {{ id = {EVG}.30 days = 1 }}
	}}
	if = {{
		limit = {{ NOT = {{ check_variable = {{ ruling_party = 3 }} }} check_variable = {{ cwger_spd_leader < 3 }} date > 1982.12.1 }}
		set_variable = {{ cwger_spd_leader = 3 }}
	}}
	if = {{
		limit = {{ NOT = {{ check_variable = {{ ruling_party = 3 }} }} check_variable = {{ cwger_spd_leader = 3 }} date > 1986.8.25 }}
		set_variable = {{ cwger_spd_leader = 4 }}
	}}
	if = {{
		limit = {{ NOT = {{ check_variable = {{ ruling_party = 3 }} }} check_variable = {{ cwger_spd_leader = 4 }} date > 1990.3.19 }}
		set_variable = {{ cwger_spd_leader = 5 }}
	}}
	if = {{
		limit = {{ NOT = {{ check_variable = {{ ruling_party = 3 }} }} check_variable = {{ cwger_spd_leader = 5 }} date > 1991.5.29 date < 1995.11.1 }}
		set_variable = {{ cwger_spd_leader = 6 }}
	}}
	if = {{
		limit = {{ NOT = {{ check_variable = {{ ruling_party = 3 }} }} check_variable = {{ cwger_spd_leader = 6 }} date > 1993.6.25 }}
		set_variable = {{ cwger_spd_leader = 7 }}
	}}
	if = {{
		limit = {{ NOT = {{ check_variable = {{ ruling_party = 3 }} }} check_variable = {{ cwger_spd_leader = 7 }} date > 1995.11.16 }}
		set_variable = {{ cwger_spd_leader = 5 }}
		set_country_flag = {P}_lafontaine_mannheim
	}}
	if = {{
		limit = {{ NOT = {{ check_variable = {{ ruling_party = 3 }} }} has_country_flag = {P}_lafontaine_mannheim check_variable = {{ cwger_spd_leader = 5 }} date > 1998.3.2 }}
		set_variable = {{ cwger_spd_leader = 8 }}
		country_event = {{ id = {EVG}.36 days = 1 }}
	}}
	# FDP chairmanship
	if = {{ limit = {{ check_variable = {{ cwger_fdp_leader = 1 }} date > 1974.10.1 }} set_variable = {{ cwger_fdp_leader = 2 }} }}
	if = {{ limit = {{ check_variable = {{ cwger_fdp_leader = 2 }} date > 1992.5.18 }} set_variable = {{ cwger_fdp_leader = 3 }} }}
}}
"""


def core_setup_effect():
    import tree
    return f"\n# core spirits of the focus tree\n{P}_core_setup = {{\n" + fmt(tree.core_setup(), 1) + "\n}\n"


def all_effects():
    from tooltips import hide_vars
    return "\n".join([core_setup_effect(), 
        "## Generated by tools/west_germany_1970/compile.py. Edit the generator, not this file.\n",
        setup_effects(), bundestag_effect(), modifier_effect(), terror_effects(), inner_german_effects(),
        unity_effects(), imperia_effects(), monthly_effects(), set_leader_effect(),
    ])


# --------------------------------------------------------------------------
def on_actions():
    return f"""## Generated by tools/west_germany_1970/compile.py. Edit the generator, not this file.

on_actions = {{
	on_startup = {{
		effect = {{
			if = {{
				limit = {{ country_exists = GER GER = {{ IMP_is_1970_scenario = yes }} }}
				GER = {{ {P}_initialize = yes }}
			}}
		}}
	}}
	on_monthly_GER = {{
		effect = {{
			{P}_monthly = yes
		}}
	}}
	on_new_term_election = {{
		effect = {{
			if = {{
				limit = {{ original_tag = GER IMP_is_1970_scenario = yes has_country_flag = {P}_initialized }}
				{P}_update_bundestag = yes
				country_event = {{ id = {EVG}.24 days = 20 }}
			}}
		}}
	}}
	on_ruling_party_change = {{
		effect = {{
			if = {{
				limit = {{ original_tag = GER IMP_is_1970_scenario = yes has_country_flag = {P}_initialized }}
				{P}_update_bundestag = yes
			}}
		}}
	}}
}}
"""


def dynamic_modifiers():
    return f"""## Generated by tools/west_germany_1970/compile.py. Edit the generator, not this file.

{P}_state_of_the_republic = {{
	icon = GFX_idea_german_advisors
	enable = {{ always = yes }}
	police_cost_multiplier_modifier = cwger_dm_police
	stability_factor = cwger_dm_stab
	political_power_factor = cwger_dm_pp
	interest_rate_multiplier_modifier = cwger_dm_interest
	mdcw_cw_ideological_defence = cwger_dm_ideo
	trade_opinion_factor = cwger_dm_trade
	war_support_factor = cwger_dm_ws
	tax_gain_multiplier_modifier = cwger_dm_tax
	research_speed_factor = cwger_dm_research
	terror_threat_detection_modifier = cwger_dm_ct_detect
	terror_threat_base_defense_modifier = cwger_dm_ct_defence
}}

{P}_ddr_inner_german = {{
	icon = GFX_idea_soviet_advisors
	enable = {{ always = yes }}
	stability_factor = cwddr_dm_stab
	consumer_goods_factor = cwddr_dm_consumer
	political_power_factor = cwddr_dm_pp
	total_workforce_modifier = cwddr_dm_workforce
}}
"""


def bop():
    return f"""## Generated by tools/west_germany_1970/compile.py. Edit the generator, not this file.

{P}_deutschlandpolitik = {{
	initial_value = -0.4
	left_side = {P}_bop_abgrenzung
	right_side = {P}_bop_annaeherung
	decision_category = {P}_deutschlandpolitik_category

	range = {{
		id = {P}_bop_treaty_policy
		min = -0.2
		max = 0.2
		modifier = {{
			stability_factor = 0.02
			political_power_factor = 0.02
		}}
	}}
	side = {{
		id = {P}_bop_abgrenzung
		icon = GFX_bop_GER_militarism
		range = {{
			id = {P}_bop_cold_front
			min = -1
			max = -0.6
			modifier = {{
				mdcw_cw_ideological_defence = 0.1
				war_support_factor = 0.05
				trade_opinion_factor = -0.1
				stability_factor = -0.02
			}}
		}}
		range = {{
			id = {P}_bop_legal_position
			min = -0.6
			max = -0.2
			modifier = {{
				mdcw_cw_ideological_defence = 0.05
				drift_defence_factor = 0.1
			}}
		}}
	}}
	side = {{
		id = {P}_bop_annaeherung
		icon = GFX_bop_GER_pacifism
		range = {{
			id = {P}_bop_change_through_rapprochement
			min = 0.2
			max = 0.6
			modifier = {{
				trade_opinion_factor = 0.1
				political_power_factor = 0.03
				mdcw_cw_ideological_defence = -0.03
			}}
		}}
		range = {{
			id = {P}_bop_community_of_responsibility
			min = 0.6
			max = 1
			modifier = {{
				trade_opinion_factor = 0.2
				stability_factor = 0.03
				war_support_factor = -0.05
				mdcw_cw_ideological_defence = -0.06
			}}
		}}
	}}
}}
"""


def localise_systems():
    L(f"{P}_state_of_the_republic", "State of the Bonn Republic")
    L(f"{P}_state_of_the_republic_desc",
      "The balance of security and liberty, the threat of terrorism, the pressure of scandals, the Bundesbank's patience and the depth of Western integration, all at once.\n"
      "Security state: §Y[?cwger_security|0]§! | Rule of law: §Y[?cwger_rechtsstaat|0]§!\n"
      "Peace movement: §Y[?cwger_peace_movement|0]§! | Burden of the East: §Y[?cwger_east_burden|0]§! | Stasi penetration §Y[?cwger_stasi_penetration|0]§! vs counter-intelligence §Y[?cwger_counterintel|0]§!\n"
      "Terror threat (left/right/foreign): §Y[?cwger_terror_left|0]§! / §Y[?cwger_terror_right|0]§! / §Y[?cwger_terror_foreign|0]§!\n"
      "Bundestag: government §Y[?cwger_seats_gov|0]§! of §Y[?cwger_seats_total|0]§! seats (majority §Y[?cwger_majority|0]§!).")
    L(f"{P}_ddr_inner_german", "The German Question")
    L(f"{P}_ddr_inner_german_desc",
      "How deeply the Republic depends on West German money and how much its people want to leave.\n"
      "Crisis index: §Y[?cwddr_crisis|0]§! | Exit pressure: §Y[?cwddr_exit_pressure|0]§! | Hard-currency shortage: §Y[?cwddr_hard_currency|0]§!\n"
      "SED control: §Y[?cwddr_sed_control|0]§! | Moscow's guarantee: §Y[?cwddr_moscow_backing|0]§! | Opposition: §Y[?cwddr_opposition|0]§!")
    L(f"{P}_deutschlandpolitik", "Deutschlandpolitik")
    L(f"{P}_bop_abgrenzung", "Legal Position")
    L(f"{P}_bop_annaeherung", "Change through Rapprochement")
    L(f"{P}_bop_treaty_policy", "Treaty Policy")
    L(f"{P}_bop_cold_front", "Cold Front")
    L(f"{P}_bop_legal_position", "Insisting on the Legal Position")
    L(f"{P}_bop_change_through_rapprochement", "Wandel durch Annäherung")
    L(f"{P}_bop_community_of_responsibility", "Community of Responsibility")
