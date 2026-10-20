"""Peaceful unity through détente: the fifth tab of the inner-German relations window (multiplayer roleplay).

Not the collapse of the GDR (that path stays in events_ddr.py), but two German states that get on well
enough to negotiate one state. Hard by design:

  1. Détente first: a focus (A European Peace Order), the Basic Treaty, the Permanent Representations and
     the traffic agreements in force plus culture or the state visit, climate at least 70, the ladder at
     Modus Vivendi with no crisis, and three years of unbroken détente (cwgg_detente_m >= 36).
  2. Either German government proposes talks; the other one decides (a human player, or the AI by its
     regime, its dependence on Bonn and Moscow's line).
  3. Five chapters are negotiated one per round (a round = three months): constitution, economy, alliance,
     capital, borders. Each side picks a position - the Western line, a compromise or the Eastern line.
     Same position = agreed. Different = no agreement, a failed round. An AI GDR moves towards Bonn's
     position after every failed round; humans simply have to talk to each other. Eight failed rounds,
     a crisis at Confrontation, or either side breaking off ends the talks (three years' cooldown).
  4. The Four Powers (USA, USSR, UK, France) each consent or veto - a veto names its demand and reopens
     that chapter; three vetoes or an outright veto end the talks.
  5. Bundestag and Volkskammer ratify (a new constitution needs two thirds, or the opposition's price,
     or a referendum).
  6. The result follows the chapters: accession under the Basic Law, a new constitution, or - only if
     everybody, the Western Allies included, agrees - a socialist Germany built on the GDR; NATO,
     armed neutrality or the Warsaw Pact; market, mixed or planned economy; Bonn or Berlin; the border.

State lives on GER (prefix cwgg_u_ / cwgg_fp_ / cwgg_detente_m). The GDR player sees the same numbers in
the 'Policy Towards Bonn' decisions and answers every round by event.
"""
from cw_lib import *
from events_lib import E, O
from tree import F, core, climate_base, opinion, state_mod, unlock
from rivalry import kl, log, R
import decisions as dec
from foreign import news_all

U = P + "_uni"
EVU = "COLDWAR_GGU"
SPD = "check_variable = { ruling_party = 3 }"
UNION = "check_variable = { ruling_party = 1 }"

CHAPTERS = [  # n, key, name, description, (west, compromise, east) as (name, description)
    (1, "const", "The Constitution",
     "Under which constitution do the Germans live together?",
     (("The Basic Law (Article 23)", "The GDR's Länder accede to the Federal Republic. The Basic Law applies everywhere."),
      ("A New Constitution (Article 146)", "A constituent assembly from both states writes a new constitution for all Germans."),
      ("A Socialist Constitution", "The united Germany is built on the GDR's constitution: a people's republic with a leading party."))),
    (2, "econ", "The Economy",
     "Which economic order does the united state have?",
     (("Social Market Economy", "The Deutschmark, private property and free prices - the GDR's combines are privatised."),
      ("A Mixed Economy", "Key industries, banks and land stay public; the rest is market. A 'third way' between the systems."),
      ("Planned Economy", "Central planning, people's enterprises, prices set by the state - the Federal Republic's industry is nationalised."))),
    (3, "alliance", "The Alliance",
     "In which alliance - if any - does the united Germany stand?",
     (("In NATO", "The united Germany stays in NATO; Soviet troops leave the East."),
      ("Armed Neutrality", "Germany leaves both blocs: an army of its own, no foreign troops, guaranteed by the Four Powers."),
      ("In the Warsaw Pact", "The united Germany joins the Warsaw Treaty Organisation; American troops leave the West."))),
    (4, "capital", "The Capital",
     "Where does the united Germany govern from - and how centralised is it?",
     (("Bonn, Federal", "Government and parliament stay on the Rhine; the GDR is divided into Länder again."),
      ("Berlin, Federal", "Berlin becomes the capital of a federal Germany; the eastern Länder are restored."),
      ("Berlin, Centralised", "Berlin governs a centralised state; the Länder become administrative districts."))),
    (5, "borders", "The Borders",
     "What becomes of the Oder-Neisse line and of a peace treaty for Germany?",
     (("Reserve the Peace Treaty", "The border question stays open until a peace treaty - as the Federal Constitutional Court demands."),
      ("The Oder-Neisse Line, Final", "The united Germany recognises its eastern border for ever in a treaty with Poland."),
      ("Border and Peace Treaty", "A formal peace treaty with the Four Powers and recognition of every post-war border."))),
]
CH = {c[0]: c for c in CHAPTERS}
POS_SHORT = ["", "Western line", "Compromise", "Eastern line"]
POWERS = [("SOV", "sov", "the Soviet Union"), ("USA", "usa", "the United States"), ("ENG", "eng", "Britain"), ("FRA", "fra", "France")]
MAX_FAIL = 8

# ------------------------------------------------------------------ helpers
def ch_is(k, p):
    return f"check_variable = {{ cwgg_u_ch_{k} = {p} }}"


def ger_ch_is(k, p):
    return f"GER = {{ check_variable = {{ cwgg_u_ch_{k} = {p} }} }}"


def phase_is(n):
    return f"check_variable = {{ cwgg_u_phase = {n} }}"


def bias(k, p, n=25):
    """Focus effect: the GDR delegation leans towards position p in chapter k."""
    name = CH[k][4][p - 1][0]
    key = f"{P}_tt_ubias_{k}_{p}"
    L(key, f"Unity talks: the delegation from East Berlin will lean towards §Y{name}§! in the chapter §Y{CH[k][2]}§!.")
    return f"custom_effect_tooltip = {key}\nhidden_effect = {{ set_variable = {{ cwgg_u_bias_{k} = {p} }} }}"


def consent(tag_key, n):
    name = dict((k, nm) for _t, k, nm in POWERS)[tag_key]
    key = f"{P}_tt_ucons_{tag_key}_{n}"
    L(key, f"Unity talks: {name} grows more willing to accept one German state (§G+{n}§! goodwill).")
    return f"custom_effect_tooltip = {key}\nhidden_effect = {{ add_to_variable = {{ cwgg_fpb_{tag_key} = {n} }} }}"


_NEWS = [
    news_all("Unity Talks in Germany", "The two German states have opened negotiations on unity: a constitution, an economic order, an alliance, a capital and the borders. Every one of the Four Powers will have to agree to the result.", "GFX_handshake_black"),
    news_all("The German Unity Treaty Is Initialled", "Bonn and East Berlin have agreed on every chapter of a treaty on German unity. Washington, Moscow, London and Paris must now decide whether they accept it.", "GFX_treaty"),
    news_all("Germany Is United", "By treaty and with the consent of the Four Powers, the two German states have become one. No shot was fired, no wall fell - the diplomats simply finished their work.", "GFX_new_year_germany"),
]


# ------------------------------------------------------------------ triggers
def triggers():
    conds = [phase_is(0), "NOT = { has_country_flag = cwgg_unity_cd }", f"has_completed_focus = {P}_european_peace_order",
             "check_variable = { cwgg_klima > 69 }", "check_variable = { cwgg_stufe = 0 }", "check_variable = { cwgg_krise_typ = 0 }",
             "check_variable = { cwgg_detente_m > 35 }", "check_variable = { cwgg_vertrag_3 = 1 }", "check_variable = { cwgg_vertrag_5 = 1 }",
             "check_variable = { cwgg_vertrag_6 = 1 }", "OR = { check_variable = { cwgg_vertrag_7 = 1 } check_variable = { cwgg_vertrag_8 = 1 } }",
             "country_exists = DDR", f"NOT = {{ has_global_flag = {P}_unity_achieved }}", f"NOT = {{ has_global_flag = {P}_confederation }}",
             f"NOT = {{ has_country_flag = {P}_dark_regime }}", "NOT = { has_war_with = DDR }", "date > 1975.1.1"]
    out = [f"\n# ---------------------------------------------------------------- unity through détente",
           f"{U}_ready = {{\n\t" + "\n\t".join(conds) + "\n}\n",
           f"{U}_can_propose = {{\n\t{U}_ready = yes\n\tcheck_variable = {{ cwgg_init_brd > 2 }}\n\thas_political_power > 99\n}}\n",
           f"{U}_can_ddr_propose = {{\n\tGER = {{ {U}_ready = yes check_variable = {{ cwgg_init_ddr > 2 }} }}\n\thas_political_power > 99\n}}\n",
           f"{U}_talking = {{\n\tcheck_variable = {{ cwgg_u_phase > 1 }}\n}}\n"]
    for p in range(1, 4):
        out.append(f"{U}_can_pos_{p} = {{\n\t{phase_is(2)}\n\tNOT = {{ check_variable = {{ cwgg_u_pos = {p} }} }}\n}}\n")
    return "\n".join(out)


# ------------------------------------------------------------------ effects
def effects():
    # AI GDR chooses its position on the chapter on the table
    ddr_ai = []
    for k in range(1, 6):
        entries = []
        for p in range(1, 4):
            hard, mid, reform, free = (5, 25, 70)[p - 1], (10, 40, 50)[p - 1], (25, 55, 20)[p - 1], (50, 40, 10)[p - 1]
            entries.append(f"""			10 = {{
				modifier = {{ add = {hard} DDR = {{ check_variable = {{ cwddr_leader < 2 }} check_variable = {{ cwddr_wende_stage < 3 }} }} }}
				modifier = {{ add = {mid} DDR = {{ check_variable = {{ cwddr_leader = 2 }} check_variable = {{ cwddr_wende_stage < 3 }} }} }}
				modifier = {{ add = {reform} DDR = {{ check_variable = {{ cwddr_leader = 3 }} check_variable = {{ cwddr_wende_stage < 3 }} }} }}
				modifier = {{ add = {free} DDR = {{ OR = {{ check_variable = {{ cwddr_leader > 3 }} check_variable = {{ cwddr_wende_stage > 2 }} }} }} }}
				{"modifier = { add = 10 DDR = { check_variable = { cwddr_west_dependency > 60 } } }" if p < 3 else "modifier = { add = 10 DDR = { check_variable = { cwddr_sed_control > 70 } } }"}
				modifier = {{ add = 15 check_variable = {{ cwgg_u_pos = {p} }} check_variable = {{ cwgg_u_shift_{k} > 0 }} }}
				modifier = {{ add = 15 check_variable = {{ cwgg_u_pos = {p} }} check_variable = {{ cwgg_u_shift_{k} > 1 }} }}
				modifier = {{ add = 20 check_variable = {{ cwgg_u_pos = {p} }} check_variable = {{ cwgg_u_shift_{k} > 2 }} }}
				modifier = {{ add = 25 check_variable = {{ cwgg_u_bias_{k} = {p} }} }}
				set_variable = {{ cwgg_u_dpos = {p} }}
			}}""")
        ddr_ai.append(f"""	if = {{ limit = {{ check_variable = {{ cwgg_u_cur = {k} }} }}
		random_list = {{
{chr(10).join(entries)}
		}}
	}}""")
    next_open = "\n".join(f"\t{'if' if k == 1 else 'else_if'} = {{ limit = {{ check_variable = {{ cwgg_u_ch_{k} = 0 }} }} set_variable = {{ cwgg_u_cur = {k} }} }}" for k in range(1, 6))
    agree = "\n".join(f"\t\tif = {{ limit = {{ check_variable = {{ cwgg_u_cur = {k} }} }} set_variable = {{ cwgg_u_ch_{k} = cwgg_u_pos }} }}" for k in range(1, 6))
    shift = "\n".join(f"\t\tif = {{ limit = {{ check_variable = {{ cwgg_u_cur = {k} }} }} add_to_variable = {{ cwgg_u_shift_{k} = 1 }} }}" for k in range(1, 6))
    ddr_round_ev = "\n".join(f"\t\tif = {{ limit = {{ check_variable = {{ cwgg_u_cur = {k} }} }} DDR = {{ country_event = {{ id = {EVU}.{30 + k} days = 1 }} }} }}" for k in range(1, 6))
    reset = "\n".join(f"\tset_variable = {{ cwgg_u_ch_{k} = 0 }}\n\tset_variable = {{ cwgg_u_shift_{k} = 0 }}" for k in range(1, 6))
    reset_fp = "\n".join(f"\tset_variable = {{ cwgg_fp_{k} = 0 }}" for _t, k, _n in POWERS)
    ask_fp = "\n".join(f"""	if = {{ limit = {{ country_exists = {t} }} set_variable = {{ cwgg_fp_{k} = 1 }} {t} = {{ country_event = {{ id = {EVU}.{41 + i} days = 3 }} }} }}
	else = {{ set_variable = {{ cwgg_fp_{k} = 2 }} }}""" for i, (t, k, _n) in enumerate(POWERS))
    any_pending = " ".join(f"check_variable = {{ cwgg_fp_{k} = 1 }}" for _t, k, _n in POWERS)
    any_veto = " ".join(f"check_variable = {{ cwgg_fp_{k} = 3 }}" for _t, k, _n in POWERS)
    reopen = "\n".join(f"\t\tif = {{ limit = {{ check_variable = {{ cwgg_u_reopen_{k} = 1 }} }} set_variable = {{ cwgg_u_ch_{k} = 0 }} set_variable = {{ cwgg_u_reopen_{k} = 0 }} }}" for k in range(1, 6))
    return f"""
# ======================================================================== unity through détente
{U}_setup = {{
	set_country_flag = cwgg_u_initialized
	set_variable = {{ cwgg_u_phase = 0 }}
	set_variable = {{ cwgg_detente_m = 0 }}
	set_variable = {{ cwgg_u_cur = 1 }}
	set_variable = {{ cwgg_u_pos = 0 }}
	set_variable = {{ cwgg_u_dpos = 0 }}
	set_variable = {{ cwgg_u_m = 0 }}
	set_variable = {{ cwgg_u_fail = 0 }}
	set_variable = {{ cwgg_u_veto = 0 }}
{reset}
{reset_fp}
}}

# Monthly, GER scope, after the inner-German tick.
{U}_tick = {{
	if = {{ limit = {{ NOT = {{ has_country_flag = cwgg_u_initialized }} }} {U}_setup = yes }}
	# months of unbroken détente
	if = {{ limit = {{ check_variable = {{ cwgg_stufe = 0 }} check_variable = {{ cwgg_klima > 59 }} check_variable = {{ cwgg_krise_typ = 0 }} }}
		add_to_variable = {{ cwgg_detente_m = 1 }}
	}}
	else_if = {{ limit = {{ check_variable = {{ cwgg_stufe > 1 }} }} set_variable = {{ cwgg_detente_m = 0 }} }}
	else = {{ add_to_variable = {{ cwgg_detente_m = -1 }} }}
	clamp_variable = {{ var = cwgg_detente_m min = 0 max = 120 }}
	if = {{ limit = {{ check_variable = {{ cwgg_u_phase > 0 }} OR = {{ NOT = {{ country_exists = DDR }} has_global_flag = {P}_unity_achieved has_war_with = DDR }} }}
		set_variable = {{ cwgg_u_phase = 0 }}
	}}
	# negotiations: a crisis pauses them, a confrontation ends them
	if = {{ limit = {{ check_variable = {{ cwgg_u_phase > 1 }} check_variable = {{ cwgg_stufe > 3 }} }}
		{log("u_crisis_end", "The confrontation has buried the unity talks.")}
		{U}_collapse = yes
	}}
	else_if = {{ limit = {{ {phase_is(2)} check_variable = {{ cwgg_stufe < 3 }} }}
		add_to_variable = {{ cwgg_u_m = 1 }}
		if = {{ limit = {{ check_variable = {{ cwgg_u_m > 2 }} }} {U}_resolve_round = yes }}
	}}
	{R}_gui_refresh = yes
}}

{U}_propose = {{
	add_to_variable = {{ cwgg_init_brd = -3 }}
	add_political_power = -100
	set_variable = {{ cwgg_u_phase = 1 }}
	{log("u_proposed", "Bonn proposes talks on the unity of Germany.")}
	if = {{ limit = {{ DDR = {{ is_ai = no }} }} DDR = {{ country_event = {{ id = {EVU}.1 days = 1 }} }} }}
	else = {{
		random_list = {{
			10 = {{
				modifier = {{ add = 20 DDR = {{ check_variable = {{ cwddr_leader > 2 }} }} }}
				modifier = {{ add = 30 DDR = {{ check_variable = {{ cwddr_wende_stage > 2 }} }} }}
				modifier = {{ add = 15 DDR = {{ check_variable = {{ cwddr_west_dependency > 60 }} }} }}
				modifier = {{ add = 10 DDR = {{ check_variable = {{ cwddr_hard_currency > 60 }} }} }}
				modifier = {{ add = 10 DDR = {{ check_variable = {{ cwddr_moscow_backing < 40 }} }} }}
				modifier = {{ factor = 0.5 DDR = {{ check_variable = {{ cwddr_sed_control > 70 }} }} }}
				modifier = {{ factor = 0.5 DDR = {{ check_variable = {{ cwddr_leader = 0 }} }} }}
				{U}_start = yes
			}}
			40 = {{ country_event = {{ id = {EVU}.3 days = 1 }} }}
		}}
	}}
	{R}_gui_refresh = yes
}}

{U}_start = {{
	set_variable = {{ cwgg_u_phase = 2 }}
	set_variable = {{ cwgg_u_cur = 1 }}
	set_variable = {{ cwgg_u_pos = 0 }}
	set_variable = {{ cwgg_u_dpos = 0 }}
	set_variable = {{ cwgg_u_m = 0 }}
	set_variable = {{ cwgg_u_fail = 0 }}
	set_variable = {{ cwgg_u_veto = 0 }}
{reset}
{reset_fp}
	clr_country_flag = cwgg_u_rat_brd
	clr_country_flag = cwgg_u_rat_ddr
	country_event = {{ id = {EVU}.4 days = 1 }}
	if = {{ limit = {{ DDR = {{ is_ai = no }} }} DDR = {{ country_event = {{ id = {EVU}.31 days = 2 }} }} }}
	{_NEWS[0]}
	{log("u_started", "The unity talks open. First chapter: the constitution.")}
}}

{U}_resolve_round = {{
	set_variable = {{ cwgg_u_m = 0 }}
	# an AI Bonn takes the Western line and moves to the compromise after two failed rounds
	if = {{ limit = {{ is_ai = yes check_variable = {{ cwgg_u_pos = 0 }} }}
		set_variable = {{ cwgg_u_pos = 1 }}
{chr(10).join(f"		if = {{ limit = {{ check_variable = {{ cwgg_u_cur = {k} }} check_variable = {{ cwgg_u_shift_{k} > 1 }} }} set_variable = {{ cwgg_u_pos = 2 }} }}" for k in range(1, 6))}
	}}
	if = {{ limit = {{ DDR = {{ is_ai = yes }} }}
{chr(10).join(ddr_ai)}
	}}
	set_variable = {{ cwgg_u_last_pos = cwgg_u_pos }}
	set_variable = {{ cwgg_u_last_dpos = cwgg_u_dpos }}
	set_variable = {{ cwgg_u_last_ch = cwgg_u_cur }}
	if = {{ limit = {{ check_variable = {{ cwgg_u_pos > 0 }} check_variable = {{ cwgg_u_pos = cwgg_u_dpos }} }}
{agree}
		add_to_variable = {{ cwgg_klima = 3 }}
		clamp_variable = {{ var = cwgg_klima min = -100 max = 100 }}
		set_variable = {{ cwgg_u_last_ok = 1 }}
		{log("u_agreed", "A chapter of the unity treaty is agreed.")}
	}}
	else = {{
		add_to_variable = {{ cwgg_u_fail = 1 }}
{shift}
		add_to_variable = {{ cwgg_klima = -2 }}
		clamp_variable = {{ var = cwgg_klima min = -100 max = 100 }}
		set_variable = {{ cwgg_u_last_ok = 0 }}
		{log("u_failed", "No agreement in this round of the unity talks.")}
	}}
	set_variable = {{ cwgg_u_pos = 0 }}
	set_variable = {{ cwgg_u_dpos = 0 }}
	set_variable = {{ cwgg_u_cur = 0 }}
{next_open}
	country_event = {{ id = {EVU}.20 days = 1 }}
	if = {{ limit = {{ DDR = {{ is_ai = no }} }} DDR = {{ country_event = {{ id = {EVU}.21 days = 1 }} }} }}
	if = {{ limit = {{ check_variable = {{ cwgg_u_fail > {MAX_FAIL - 1} }} }}
		{log("u_exhausted", "After too many failed rounds the unity talks are broken off.")}
		{U}_collapse = yes
	}}
	else_if = {{ limit = {{ check_variable = {{ cwgg_u_cur = 0 }} }} {U}_initial = yes }}
	else = {{
		if = {{ limit = {{ DDR = {{ is_ai = no }} }}
{ddr_round_ev}
		}}
	}}
}}

# All five chapters agreed: the treaty is initialled and goes to the Four Powers.
{U}_initial = {{
	set_variable = {{ cwgg_u_phase = 3 }}
{reset_fp}
{ask_fp}
	{log("u_initialled", "The unity treaty is initialled. The Four Powers must now agree.")}
	{_NEWS[1]}
	{U}_powers_check = yes
}}

{U}_powers_check = {{
	if = {{ limit = {{ {phase_is(3)} NOT = {{ OR = {{ {any_pending} }} }} }}
		if = {{ limit = {{ has_country_flag = cwgg_u_outright }}
			clr_country_flag = cwgg_u_outright
			{log("u_outright", "One of the Four Powers vetoes German unity outright.")}
			{U}_collapse = yes
		}}
		else_if = {{ limit = {{ OR = {{ {any_veto} }} }}
			add_to_variable = {{ cwgg_u_veto = 1 }}
			if = {{ limit = {{ check_variable = {{ cwgg_u_veto > 2 }} }}
				{log("u_three_vetoes", "After the third veto the unity talks collapse.")}
				{U}_collapse = yes
			}}
			else = {{
{reopen}
				set_variable = {{ cwgg_u_phase = 2 }}
				set_variable = {{ cwgg_u_m = 0 }}
				set_variable = {{ cwgg_u_cur = 0 }}
{next_open}
				if = {{ limit = {{ check_variable = {{ cwgg_u_cur = 0 }} }} set_variable = {{ cwgg_u_cur = 3 }} set_variable = {{ cwgg_u_ch_3 = 0 }} }}
{reset_fp}
				country_event = {{ id = {EVU}.45 days = 1 }}
				if = {{ limit = {{ DDR = {{ is_ai = no }} }} DDR = {{ country_event = {{ id = {EVU}.45 days = 1 }} }} }}
				{log("u_veto", "A veto by the Four Powers reopens a chapter of the unity treaty.")}
			}}
		}}
		else = {{
			set_variable = {{ cwgg_u_phase = 4 }}
			{log("u_consent", "All Four Powers consent. The parliaments must ratify.")}
			country_event = {{ id = {EVU}.50 days = 2 }}
			if = {{ limit = {{ DDR = {{ is_ai = no }} }} DDR = {{ country_event = {{ id = {EVU}.51 days = 2 }} }} }}
			else = {{ set_country_flag = cwgg_u_rat_ddr }}
		}}
	}}
	{R}_gui_refresh = yes
}}

{U}_ratify_check = {{
	if = {{ limit = {{ {phase_is(4)} has_country_flag = cwgg_u_rat_brd has_country_flag = cwgg_u_rat_ddr }}
		{U}_execute = yes
	}}
}}

{U}_collapse = {{
	set_variable = {{ cwgg_u_phase = 0 }}
	set_country_flag = {{ flag = cwgg_unity_cd days = 1095 value = 1 }}
	set_variable = {{ cwgg_detente_m = 0 }}
	add_to_variable = {{ cwgg_klima = -15 }}
	clamp_variable = {{ var = cwgg_klima min = -100 max = 100 }}
	country_event = {{ id = {EVU}.60 days = 1 }}
	if = {{ limit = {{ country_exists = DDR DDR = {{ is_ai = no }} }} DDR = {{ country_event = {{ id = {EVU}.60 days = 1 }} }} }}
	{R}_gui_refresh = yes
}}

# The united Germany, as negotiated (GER scope).
{U}_execute = {{
	set_variable = {{ cwgg_u_phase = 5 }}
	set_global_flag = {P}_unity_by_detente
	{_NEWS[2]}
	if = {{ limit = {{ {ch_is(1, 3)} }}
		{U}_socialist_unity = yes
	}}
	else = {{
		if = {{ limit = {{ {ch_is(1, 2)} }} {P}_unity_art146 = yes }}
		else = {{ {P}_unity_art23 = yes }}
		set_global_flag = {P}_unity_by_treaty
		# the alliance
		if = {{ limit = {{ {ch_is(3, 2)} }} {U}_neutralise = yes }}
		else_if = {{ limit = {{ {ch_is(3, 3)} }}
			{U}_neutralise = yes
			if = {{ limit = {{ country_exists = SOV SOV = {{ is_faction_leader = yes }} }} SOV = {{ add_to_faction = GER }} }}
		}}
		# the economy
		if = {{ limit = {{ {ch_is(2, 2)} }} add_ideas = {P}_idea_mixed_economy }}
		else_if = {{ limit = {{ {ch_is(2, 3)} }} add_ideas = {P}_idea_planned_economy }}
		# the capital
		if = {{ limit = {{ check_variable = {{ cwgg_u_ch_4 > 1 }} 45 = {{ is_owned_by = ROOT }} }}
			set_capital = {{ state = 45 }}
			{state_mod(45, "capital_berlin")}
		}}
		if = {{ limit = {{ {ch_is(4, 3)} }} add_ideas = {P}_idea_centralised_state }}
		# the borders
		if = {{ limit = {{ {ch_is(5, 1)} }} {opinion("POL", "large_decrease")} set_global_flag = {P}_border_reserved }}
		else = {{ {opinion("POL", "large_increase")} }}
		if = {{ limit = {{ {ch_is(5, 3)} }} {opinion("SOV", "medium_increase")} }}
	}}
}}

{EXTRA}

# Neutrality: out of every bloc (GER scope).
{U}_neutralise = {{
	if = {{ limit = {{ has_idea = NATO_member }} NATO_leave = yes }}
	if = {{ limit = {{ is_in_faction = yes }} leave_faction = yes }}
	add_ideas = {P}_idea_neutral_germany
	if = {{
		limit = {{ has_global_flag = mdcw_cw_initialized }}
		set_temp_variable = {{ mdcw_cw_new_alignment = 0 }}
		set_temp_variable = {{ mdcw_cw_t_free = 1 }}
		mdcw_cw_change_alignment = yes
	}}
}}

# A socialist Germany built on the GDR (GER scope): East Berlin takes over the Federal Republic.
{U}_socialist_unity = {{
	set_global_flag = {P}_unity_achieved
	set_global_flag = {P}_unity_socialist
	every_state = {{ limit = {{ is_core_of = GER }} add_core_of = DDR }}
	DDR = {{
		add_ideas = {P}_idea_socialist_unity
		if = {{ limit = {{ GER = {{ check_variable = {{ cwgg_u_ch_3 < 3 }} }} is_in_faction = yes }} leave_faction = yes }}
		if = {{ limit = {{ GER = {{ check_variable = {{ cwgg_u_ch_4 > 1 }} }} 45 = {{ is_owned_by = DDR }} }} set_capital = {{ state = 45 }} }}
		annex_country = {{ target = GER transfer_troops = yes }}
	}}
}}
"""


# ------------------------------------------------------------------ events
def events():
    yes_start = f"GER = {{ {U}_start = yes }}"
    E(f"{EVU}.1", "Bonn Proposes Unity Talks",
      "The Federal Chancellor has proposed formal negotiations on the unity of Germany - not as an annexation, Bonn insists, but as a treaty between equals. Five chapters would be on the table: the constitution, the economic order, the alliance, the capital and the borders. Every one of the Four Powers would have to agree.",
      "GFX_handshake_black",
      [O("We will negotiate - on equal terms.", J(yes_start, "add_political_power = 25"), ai=50),
       O("The GDR is a sovereign socialist state. No.", J(f"GER = {{ set_variable = {{ cwgg_u_phase = 0 }} set_country_flag = {{ flag = cwgg_unity_cd days = 730 value = 1 }} country_event = {{ id = {EVU}.3 days = 1 }} }}"), ai=50)],
      scope="DDR")
    E(f"{EVU}.2", "East Berlin Proposes Unity Talks",
      "The GDR's government has proposed formal negotiations on the unity of Germany. Some in Bonn call it a trap, some the chance of a century. If we accept, every chapter - the constitution, the economy, the alliance, the capital, the borders - is open.",
      "GFX_handshake_black",
      [O("We accept.", J(f"{U}_start = yes", "add_political_power = 25"), ai=70),
       O("Not under these conditions.", J("set_variable = { cwgg_u_phase = 0 }", "set_country_flag = { flag = cwgg_unity_cd days = 730 value = 1 }",
                                           "DDR = { add_political_power = -25 }"), ai=30)])
    E(f"{EVU}.3", "East Berlin Says No",
      "The GDR has rejected unity talks. 'Socialism and imperialism cannot be united, any more than fire and water,' says the Politburo's statement. For two years the subject is closed.",
      "GFX_egon_krenz_ddr",
      [O("Then we keep building trust.", J("set_variable = { cwgg_u_phase = 0 }", "set_country_flag = { flag = cwgg_unity_cd days = 730 value = 1 }"))])
    E(f"{EVU}.4", "The Unity Talks Begin",
      "Delegations from Bonn and East Berlin meet at a long table. First on the agenda: the constitution. One chapter is negotiated every three months; set our position in the §YUnity§! tab of the inner-German relations window.",
      "GFX_politics_talks", [O("To work.")])
    # round reports
    L(f"{P}_u_rr_ok", "§GAgreement.§! Both delegations accepted the same position.")
    L(f"{P}_u_rr_fail", "§RNo agreement.§! The delegations could not find common ground.")
    E(f"{EVU}.20", "A Round of Unity Talks",
      "", "GFX_politics_talks", [O("Next chapter.")],
      descs=[("check_variable = { cwgg_u_last_ok = 1 }", "Chapter: §Y[U_LastChapter]§!. We proposed §Y[U_LastPos]§!, East Berlin §Y[U_LastDPos]§!. $COLDWAR_GER_1970_u_rr_ok$\n\nAgreed so far: §Y[?cwgg_u_agreed|0]§! of five chapters. Failed rounds: §Y[?cwgg_u_fail|0]§!/8."),
             ("", "Chapter: §Y[U_LastChapter]§!. We proposed §Y[U_LastPos]§!, East Berlin §Y[U_LastDPos]§!. $COLDWAR_GER_1970_u_rr_fail$\n\nFailed rounds: §Y[?cwgg_u_fail|0]§!/8. A delegation that has failed on a chapter often enough tends to soften its line - but nothing obliges it to.")],
      imm=f"{U}_count_agreed = yes")
    E(f"{EVU}.21", "A Round of Unity Talks",
      "", "GFX_politics_talks", [O("Next chapter.")],
      descs=[("GER = { check_variable = { cwgg_u_last_ok = 1 } }", "Chapter: §Y[U_LastChapterG]§!. Bonn proposed §Y[U_LastPosG]§!, we §Y[U_LastDPosG]§!. $COLDWAR_GER_1970_u_rr_ok$"),
             ("", "Chapter: §Y[U_LastChapterG]§!. Bonn proposed §Y[U_LastPosG]§!, we §Y[U_LastDPosG]§!. $COLDWAR_GER_1970_u_rr_fail$\n\nFailed rounds: §Y[?GER.cwgg_u_fail|0]§!/8.")],
      scope="DDR")
    # the GDR's position on each chapter (human GDR)
    for k, key, name, desc, pos in CHAPTERS:
        E(f"{EVU}.{30 + k}", f"Unity Talks: {name}",
          f"{desc} The round is decided in three months. Bonn's delegation will state its own position; if both are the same, the chapter is agreed.\n\n"
          + "\n".join(f"§Y{pn}§!: {pd}" for pn, pd in pos),
          "GFX_politics_talks",
          [O(pos[p - 1][0], f"GER = {{ set_variable = {{ cwgg_u_dpos = {p} }} }}", ai=10) for p in (1, 2, 3)]
          + [O("We refuse to discuss this chapter now.", "GER = { set_variable = { cwgg_u_dpos = 0 } }", ai=1)],
          scope="DDR")
    # the Four Powers
    ally_nato = ch_is(3, 1)
    E(f"{EVU}.41", "The Germans Want to Unite",
      "Bonn and East Berlin have initialled a treaty on German unity. As one of the Four Powers responsible for Germany as a whole, the Soviet Union must agree - or say what it demands.\n\nThe treaty: constitution §Y[U_ChG1]§!, economy §Y[U_ChG2]§!, alliance §Y[U_ChG3]§!, capital §Y[U_ChG4]§!, borders §Y[U_ChG5]§!.",
      "GFX_gdratwarsov",
      [O("We consent.", "GER = { set_variable = { cwgg_fp_sov = 2 } " + U + "_powers_check = yes }",
         ai=("base = 20 modifier = { add = 30 " + ger_ch_is(3, 2) + " } modifier = { add = 60 " + ger_ch_is(3, 3) + " } modifier = { factor = 0.3 " + ger_ch_is(3, 1) + " } "
             "modifier = { add = 20 date > 1986.12.31 } modifier = { add = 30 " + ger_ch_is(1, 3) + " } modifier = { add = 20 GER = { check_variable = { cwgg_fpb_sov > 19 } } } "
             "modifier = { add = 10 has_global_flag = mdcw_cw_initialized check_variable = { global.mdcw_cw_tension < 40 } }")),
       O("Veto: a united Germany cannot stay in NATO.", "GER = { set_variable = { cwgg_fp_sov = 3 } set_variable = { cwgg_u_reopen_3 = 1 } " + U + "_powers_check = yes }",
         trig=ger_ch_is(3, 1), ai="base = 50 modifier = { factor = 0.4 date > 1986.12.31 } modifier = { factor = 0.5 GER = { check_variable = { cwgg_fpb_sov > 19 } } }"),
       O("Veto: we will not hand the GDR to capitalism.", "GER = { set_variable = { cwgg_fp_sov = 3 } set_variable = { cwgg_u_reopen_2 = 1 } set_variable = { cwgg_u_reopen_1 = 1 } " + U + "_powers_check = yes }",
         trig=f"OR = {{ {ger_ch_is(1, 1)} {ger_ch_is(2, 1)} }}", ai="base = 15 modifier = { factor = 0.3 date > 1986.12.31 }"),
       O("Veto outright: two German states, now and for ever.", "GER = { set_variable = { cwgg_fp_sov = 3 } set_country_flag = cwgg_u_outright " + U + "_powers_check = yes }", ai="base = 5")],
      scope="ANY", trig="original_tag = SOV")
    west_power = [("USA", "usa", 42, "GFX_decision_nato", "the United States"), ("ENG", "eng", 43, "GFX_politics_talks", "the United Kingdom"), ("FRA", "fra", 44, "GFX_politics_talks", "France")]
    for tag, k, n, pic, nm in west_power:
        opts = []
        base = {"usa": "base = 40 modifier = { add = 40 " + ger_ch_is(3, 1) + " } modifier = { factor = 0.5 " + ger_ch_is(3, 2) + " } modifier = { factor = 0.5 " + ger_ch_is(2, 3) + " }",
                "eng": "base = 40 modifier = { add = 20 GER = { check_variable = { cwgg_u_ch_5 > 1 } } } modifier = { factor = 0.5 " + ger_ch_is(5, 1) + " } modifier = { add = 15 " + ger_ch_is(3, 1) + " }",
                "fra": "base = 40 modifier = { add = 20 GER = { OR = { has_completed_focus = " + P + "_ems has_completed_focus = " + P + "_maastricht has_completed_focus = " + P + "_euro_founder } } } "
                       "modifier = { add = 10 GER = { check_variable = { cwgg_u_ch_5 > 1 } } } modifier = { add = 10 " + ger_ch_is(3, 1) + " }"}[k]
        base += f" modifier = {{ factor = 0.1 {ger_ch_is(3, 3)} }} modifier = {{ factor = 0.05 {ger_ch_is(1, 3)} }} modifier = {{ add = 20 GER = {{ check_variable = {{ cwgg_fpb_{k} > 19 }} }} }}"
        opts.append(O("We consent.", f"GER = {{ set_variable = {{ cwgg_fp_{k} = 2 }} {U}_powers_check = yes }}", ai=base))
        opts.append(O("Veto: Germany must stay in the Western alliance.", f"GER = {{ set_variable = {{ cwgg_fp_{k} = 3 }} set_variable = {{ cwgg_u_reopen_3 = 1 }} {U}_powers_check = yes }}",
                      trig="NOT = { " + ger_ch_is(3, 1) + " }", ai="base = 60" if k == "usa" else "base = 35"))
        if k == "usa":
            opts.append(O("Veto: no socialist Germany.", f"GER = {{ set_variable = {{ cwgg_fp_{k} = 3 }} set_variable = {{ cwgg_u_reopen_1 = 1 }} set_variable = {{ cwgg_u_reopen_2 = 1 }} {U}_powers_check = yes }}",
                          trig=f"OR = {{ {ger_ch_is(1, 3)} {ger_ch_is(2, 3)} }}", ai="base = 80"))
        else:
            opts.append(O("Veto: the border must be settled for good first.", f"GER = {{ set_variable = {{ cwgg_fp_{k} = 3 }} set_variable = {{ cwgg_u_reopen_5 = 1 }} {U}_powers_check = yes }}",
                          trig=ger_ch_is(5, 1), ai="base = 50" if k == "eng" else "base = 30"))
        opts.append(O("Veto outright: we prefer two Germanies.", f"GER = {{ set_variable = {{ cwgg_fp_{k} = 3 }} set_country_flag = cwgg_u_outright {U}_powers_check = yes }}", ai="base = 3"))
        E(f"{EVU}.{n}", "The Germans Want to Unite",
          f"Bonn and East Berlin have initialled a treaty on German unity. As one of the Four Powers that still hold rights for Germany as a whole and Berlin, {nm} must agree - or say what it demands.\n\n"
          "The treaty: constitution §Y[U_ChG1]§!, economy §Y[U_ChG2]§!, alliance §Y[U_ChG3]§!, capital §Y[U_ChG4]§!, borders §Y[U_ChG5]§!.",
          pic, opts, scope="ANY", trig=f"original_tag = {tag}")
    E(f"{EVU}.45", "The Powers Demand Changes",
      "One of the Four Powers has vetoed the treaty and named its price. The chapter it objects to is open again - the delegations must go back to the table. A third veto would end the talks.",
      "GFX_treaty", [O("Back to the table.")], scope="ANY")
    # ratification
    two_thirds = f"custom_trigger_tooltip = {{ tooltip = {P}_tt_two_thirds check_variable = {{ cwger_seats_gov > cwger_two_thirds }} }}"
    majority = f"OR = {{ AND = {{ {ch_is(1, 2)} {two_thirds} }} AND = {{ NOT = {{ {ch_is(1, 2)} }} check_variable = {{ cwger_margin > -1 }} }} }}"
    rat = J("set_country_flag = cwgg_u_rat_brd", f"{U}_ratify_check = yes")
    E(f"{EVU}.50", "The Bundestag and the Unity Treaty",
      "The Four Powers have agreed. Now the Bundestag must ratify the treaty - with a simple majority, or with two thirds if Germany is to receive a new constitution.",
      "GFX_german_parliament_bundestag",
      [O("The Bundestag ratifies.", rat, trig=majority, ai=90),
       O("Pay the opposition's price for its votes.", J("add_political_power = -75",
                                                         f"if = {{ limit = {{ {SPD} }} {party('cdu', 0.01)} }} else_if = {{ limit = {{ {UNION} }} {party('spd', 0.01)} }}", rat),
         trig=f"NOT = {{ {majority} }} has_political_power > 74", ai=60),
       O("Let the people decide: a referendum on unity.", J(stab(0.03), rat), trig=f"has_completed_focus = {P}_both_peoples_decide", ai=80),
       O("The Bundestag rejects the treaty.", f"{U}_collapse = yes", ai=1)])
    E(f"{EVU}.51", "The Volkskammer and the Unity Treaty",
      "The Four Powers have agreed. The People's Chamber must now ratify the treaty that ends the German Democratic Republic as a separate state.",
      "GFX_gdrfromexitsov",
      [O("The People's Chamber ratifies.", f"GER = {{ set_country_flag = cwgg_u_rat_ddr {U}_ratify_check = yes }}", ai=90),
       O("The People's Chamber rejects it.", f"GER = {{ {U}_collapse = yes }}", ai=10)],
      scope="DDR")
    E(f"{EVU}.60", "The Unity Talks Have Failed",
      "The negotiations on German unity have ended without a treaty. Both governments blame each other; the climate between the two states suffers. The subject is closed for at least three years.",
      "GFX_politics_talks", [O("History has not finished with us.")], scope="ANY")


EXTRA = f"""
{U}_count_agreed = {{
	set_variable = {{ cwgg_u_agreed = 0 }}
{chr(10).join(f"	if = {{ limit = {{ check_variable = {{ cwgg_u_ch_{k} > 0 }} }} add_to_variable = {{ cwgg_u_agreed = 1 }} }}" for k in range(1, 6))}
}}
"""


# ------------------------------------------------------------------ decisions for an East German player
def ddr_decisions():
    L(f"{P}_tt_u_ddr_ready", "Three years of unbroken détente, a climate of at least §Y70§!, Modus Vivendi without a crisis, the treaties in force, Bonn's focus §YA European Peace Order§!, §Y3§! initiative and §Y100§! political power")
    dec.D(dec.WP, "ddr_propose_unity", "Propose Unity Talks",
          "Offer Bonn formal negotiations on the unity of Germany - on equal terms, with every chapter open. Needs three years of unbroken détente, a climate of at least 70, the Basic Treaty, the Permanent Representations and the traffic agreements in force, and culture or the state visit.\n\n"
          "Détente months: §Y[?GER.cwgg_detente_m|0]§!/36 | climate: §Y[?GER.cwgg_klima|0]§!",
          "GFX_decision_negotiate_icon", visible=f"GER = {{ {phase_is(0)} }} NOT = {{ has_global_flag = {P}_unity_achieved }}",
          available=f"custom_trigger_tooltip = {{ tooltip = {P}_tt_u_ddr_ready {U}_can_ddr_propose = yes }}", cost=100,
          effect=J("GER = { add_to_variable = { cwgg_init_ddr = -3 } set_variable = { cwgg_u_phase = 1 } }",
                   f"GER = {{ country_event = {{ id = {EVU}.2 days = 1 }} }}"), ai=0)
    dec.D(dec.WP, "ddr_unity_position", "Our Position in the Unity Talks",
          "Restate East Berlin's position on the chapter now on the table. Chapter §Y[?GER.cwgg_u_cur|0]§! of five; agreed so far §Y[?GER.cwgg_u_agreed|0]§!; failed rounds §Y[?GER.cwgg_u_fail|0]§!/8.",
          "GFX_decision_negotiate_icon", visible=f"GER = {{ {phase_is(2)} }}", cost=0, re_enable=30,
          effect="\n".join(f"if = {{ limit = {{ GER = {{ check_variable = {{ cwgg_u_cur = {k} }} }} }} country_event = {{ id = {EVU}.{30 + k} }} }}" for k in range(1, 6)), ai=0)
    dec.D(dec.WP, "ddr_moscow_blessing", "Seek Moscow's Blessing",
          "Send the Prime Minister to the Kremlin to argue for the treaty. The Soviet Union becomes more willing to consent.",
          "GFX_decision_negotiate_icon", visible=f"GER = {{ check_variable = {{ cwgg_u_phase > 1 }} }}", cost=75, once=True,
          effect=J("GER = { add_to_variable = { cwgg_fpb_sov = 20 } }", "add_stability = -0.02",
                   tt(f"{P}_tt_ddr_moscow_bless", "Unity talks: the Kremlin grows more willing to accept one German state (§G+20§! goodwill).")), ai=0)
    dec.D(dec.WP, "ddr_break_unity", "Break Off the Unity Talks",
          "End the negotiations. The climate suffers, and the subject is closed for three years.",
          "GFX_decision_negotiate_icon", visible=f"GER = {{ check_variable = {{ cwgg_u_phase > 1 }} check_variable = {{ cwgg_u_phase < 5 }} }}", cost=0,
          effect=J(f"GER = {{ {U}_collapse = yes }}", "add_political_power = 25"), ai=0)
    dec.D(dec.DP, "unity_status", "The Unity Talks",
          "Phase: §Y[U_Phase]§! | détente months §Y[?cwgg_detente_m|0]§!/36 | chapters agreed §Y[?cwgg_u_agreed|0]§!/5 | failed rounds §Y[?cwgg_u_fail|0]§!/8\n"
          "Everything is run from the §YUnity§! tab of the inner-German relations window.",
          "GFX_decision_negotiate_icon", visible=f"has_completed_focus = {P}_european_peace_order NOT = {{ has_global_flag = {P}_unity_achieved }}", cost=0,
          effect=J("set_country_flag = cwgg_open", "set_variable = { cwgg_tab = 5 }", f"{R}_gui_refresh = yes"), ai=0)


# ------------------------------------------------------------------ window tab
def gui_tab(w, DT):
    T = 5
    L("cwgg_rv_tab_5", "Unity")
    w.section("u", 138, "cwgg_u_h", T, right="cwgg_u_h_r")
    L("cwgg_u_h", "THE ROAD TO UNITY")
    L("cwgg_u_h_r", "[U_Phase]")
    DT("U_Phase", [(phase_is(1), "cwgg_u_ph_1"), (phase_is(2), "cwgg_u_ph_2"), (phase_is(3), "cwgg_u_ph_3"), (phase_is(4), "cwgg_u_ph_4"),
                   (phase_is(5), "cwgg_u_ph_5"), ("has_country_flag = cwgg_unity_cd", "cwgg_u_ph_cd")], "cwgg_u_ph_0")
    for k, t in [("0", "§gno talks§!"), ("1", "§Yproposal sent§!"), ("2", "§Gnegotiating§!"), ("3", "§Ywith the Four Powers§!"), ("4", "§Yratification§!"),
                 ("5", "§Gunited§!"), ("cd", "§Rtalks failed - closed for now§!")]:
        L(f"cwgg_u_ph_{k}", t)
    # conditions (phase 0) / status (phase >0)
    lines = [
        ("c1", "Unbroken détente: §Y[?cwgg_detente_m|0]§!/§Y36§! months (Modus Vivendi, climate 60+, no crisis)"),
        ("c2", "Climate now §Y[?cwgg_klima|0]§! (needs §Y70§!) · stage [RV_StageColored] (needs §G0§!)"),
        ("c3", "In force: Basic Treaty, Representations, Traffic, Culture or Visit"),
        ("c4", "Focus §YA European Peace Order§! · §Y3§! initiative · §Y100§! political power"),
    ]
    for i, (k, text) in enumerate(lines):
        w.text(f"u_{k}", f"cwgg_u_{k}", 36, 172 + i * 22, 540, tab=T, vis=phase_is(0))
        L(f"cwgg_u_{k}", text)
    w.button("u_propose", "GFX_mdcw_cw_button_160", 590, 186, "cwgg_u_propose", f"{U}_propose = yes", tab=T, vis=phase_is(0),
             enabled=f"{U}_can_propose = yes", tip="cwgg_u_propose_tt")
    L("cwgg_u_propose", "Propose Talks")
    L("cwgg_u_propose_tt", "§YPropose Unity Talks§!\nOffer East Berlin formal negotiations on one German state. The Politburo will weigh its own survival, its dependence on Bonn's money and Moscow's line - a hardline leadership will almost certainly refuse.\n\n"
                           "Needs: three years of unbroken détente, climate 70, Modus Vivendi without a crisis, the Basic Treaty, the Permanent Representations and the traffic agreements in force plus culture or the state visit, the focus §YA European Peace Order§!, 3 initiative and 100 political power. After failed talks: three years' pause.")
    st = [("s1", "Chapter on the table: §Y[U_CurName]§! · next round in §Y[?cwgg_g_u_left|3]§! month(s)", phase_is(2)),
          ("s2", "Agreed §Y[?cwgg_u_agreed|0]§!/5 · failed rounds §Y[?cwgg_u_fail|0]§!/8 · vetoes §Y[?cwgg_u_veto|0]§!/3 · East Berlin: [RV_DdrPlayer]", "check_variable = { cwgg_u_phase > 0 }"),
          ("s3", "A crisis pauses the talks; a confrontation ends them. The climate rises with every agreed chapter and falls with every failed round.", "check_variable = { cwgg_u_phase > 0 }")]
    for i, (k, text, vis) in enumerate(st):
        w.text(f"u_{k}", f"cwgg_u_{k}", 36, 172 + i * 24, 540, h=22 if i < 2 else 40, tab=T, vis=vis)
        L(f"cwgg_u_{k}", text)
    w.refresh.append("set_variable = { cwgg_g_u_left = 3 }\nsubtract_from_variable = { cwgg_g_u_left = cwgg_u_m }")
    w.refresh.append(f"{U}_count_agreed = yes")
    w.button("u_break", "GFX_mdcw_cw_button_160", 590, 186, "cwgg_u_break", f"{U}_collapse = yes", tab=T,
             vis="check_variable = { cwgg_u_phase > 1 } check_variable = { cwgg_u_phase < 5 }", tip="cwgg_u_break_tt")
    L("cwgg_u_break", "Break Off")
    L("cwgg_u_break_tt", "§YBreak Off the Talks§!\nEnd the unity negotiations. The climate falls by 15 and the subject is closed for three years.")
    # chapters
    w.section("uch", 270, "cwgg_u_hch", T)
    L("cwgg_u_hch", "THE FIVE CHAPTERS")
    for k, key, name, desc, pos in CHAPTERS:
        y = 304 + (k - 1) * 30
        w.text(f"u_ch_{k}_n", f"cwgg_u_ch_{k}_n", 36, y, 230, font="hoi_18mbs", tab=T, tip=f"cwgg_u_ch_{k}_tt")
        w.text(f"u_ch_{k}_s", f"cwgg_u_ch_{k}_s", 270, y + 2, 480, tab=T, tip=f"cwgg_u_ch_{k}_tt")
        L(f"cwgg_u_ch_{k}_n", f"{k}. {name}")
        L(f"cwgg_u_ch_{k}_s", f"[U_Ch{k}]")
        L(f"cwgg_u_ch_{k}_tt", f"§Y{name}§!\n{desc}\n\n" + "\n".join(f"§Y{pn}§! ({POS_SHORT[i + 1].lower()}): {pd}" for i, (pn, pd) in enumerate(pos)))
        DT(f"U_Ch{k}", [(f"check_variable = {{ cwgg_u_ch_{k} = {p} }}", f"cwgg_u_ch_{k}_ok_{p}") for p in (1, 2, 3)]
           + [(f"{phase_is(2)} check_variable = {{ cwgg_u_cur = {k} }}", "cwgg_u_ontable")], "cwgg_u_open")
        for p in (1, 2, 3):
            L(f"cwgg_u_ch_{k}_ok_{p}", f"§GAgreed:§! {pos[p - 1][0]}")
    L("cwgg_u_ontable", "§Yon the table§!")
    L("cwgg_u_open", "§gopen§!")
    # positions on the current chapter (phase 2)
    w.section("ulow", 462, "cwgg_u_hlow", T)
    L("cwgg_u_hlow", "[U_Low]")
    DT("U_Low", [(phase_is(2), "cwgg_u_hpos"), ("check_variable = { cwgg_u_phase > 2 }", "cwgg_u_hpow")], "cwgg_u_hnone")
    L("cwgg_u_hpos", "OUR POSITION ON THE CHAPTER")
    L("cwgg_u_hnone", "BEFORE THE TALKS")
    for p in (1, 2, 3):
        y = 494 + (p - 1) * 36
        w.button(f"u_pos_{p}", "GFX_mdcw_cw_button_96", 30, y, "cwgg_u_choose", f"set_variable = {{ cwgg_u_pos = {p} }}\n{R}_gui_refresh = yes", tab=T,
                 vis=phase_is(2), enabled=f"{U}_can_pos_{p} = yes", tip=f"cwgg_u_pos_{p}_tt")
        w.text(f"u_pos_{p}_t", f"cwgg_u_pos_{p}_t", 136, y + 6, 600, tab=T, vis=phase_is(2), tip=f"cwgg_u_pos_{p}_tt")
        L(f"cwgg_u_pos_{p}_t", f"[U_Mark{p}]{POS_SHORT[p]}: §Y[U_PosName{p}]§!")
        L(f"cwgg_u_pos_{p}_tt", f"§Y[U_PosName{p}]§!\n[U_PosDesc{p}]\n\nIf East Berlin takes the same position at the end of the round, the chapter is agreed.")
        DT(f"U_PosName{p}", [(f"check_variable = {{ cwgg_u_cur = {k} }}", f"cwgg_u_pn_{k}_{p}") for k in range(1, 6)], "cwgg_u_none")
        DT(f"U_PosDesc{p}", [(f"check_variable = {{ cwgg_u_cur = {k} }}", f"cwgg_u_pd_{k}_{p}") for k in range(1, 6)], "cwgg_u_none")
        DT(f"U_Mark{p}", [(f"check_variable = {{ cwgg_u_pos = {p} }}", "cwgg_u_mark")], "cwgg_u_nomark")
        for k in range(1, 6):
            L(f"cwgg_u_pn_{k}_{p}", CH[k][4][p - 1][0])
            L(f"cwgg_u_pd_{k}_{p}", CH[k][4][p - 1][1])
    L("cwgg_u_mark", "§G> §!")
    L("cwgg_u_nomark", "")
    L("cwgg_u_none", "-")
    L("cwgg_u_choose", "Propose")
    w.text("u_pos_hint", "cwgg_u_pos_hint", 36, 604, 700, h=40, tab=T, vis=phase_is(2))
    L("cwgg_u_pos_hint", "Our position: §Y[U_OurPos]§!. East Berlin's delegation reveals its own only when the round closes - guided by its leadership, its instructions from Moscow and how often this chapter has already failed.")
    DT("U_OurPos", [(f"check_variable = {{ cwgg_u_pos = {p} }}", f"cwgg_u_our_{p}") for p in (1, 2, 3)], "cwgg_u_our_0")
    for p in (1, 2, 3):
        L(f"cwgg_u_our_{p}", "[U_PosName" + str(p) + "]")
    L("cwgg_u_our_0", "§Rnone yet - a round without a position fails§!")
    # the Four Powers (phase 3/4)
    L("cwgg_u_hpow", "THE FOUR POWERS")
    w.text("u_before", "cwgg_u_before", 36, 494, 700, h=110, tab=T, vis=phase_is(0))
    L("cwgg_u_before", "Unity by treaty is the hardest road in this game. Both German governments must want it and must agree on five chapters, one every three months. "
                       "Then the United States, the Soviet Union, Britain and France each consent or veto - a veto reopens the chapter it objects to. "
                       "Finally the Bundestag and the Volkskammer ratify.\n\nThe existing unity focuses only become available when relations are at §YCool Coexistence§! or better with a climate above §Y40§!; during the talks they move East Berlin and the Four Powers.")
    for i, (tag, k, nm) in enumerate(POWERS):
        y = 494 + i * 28
        w.text(f"u_fp_{k}", f"cwgg_u_fp_{k}", 36, y, 700, tab=T, vis="check_variable = { cwgg_u_phase > 2 }")
        L(f"cwgg_u_fp_{k}", f"{nm[0].upper() + nm[1:]}: [U_Fp_{k}]")
        DT(f"U_Fp_{k}", [(f"check_variable = {{ cwgg_fp_{k} = 1 }}", "cwgg_u_fp_pending"), (f"check_variable = {{ cwgg_fp_{k} = 2 }}", "cwgg_u_fp_yes"),
                         (f"check_variable = {{ cwgg_fp_{k} = 3 }}", "cwgg_u_fp_no")], "cwgg_u_fp_none")
    L("cwgg_u_fp_pending", "§Ydeciding§!")
    L("cwgg_u_fp_yes", "§Gconsents§!")
    L("cwgg_u_fp_no", "§Rvetoes§!")
    L("cwgg_u_fp_none", "§gnot yet asked§!")
    w.text("u_rat", "cwgg_u_rat", 36, 612, 700, h=40, tab=T, vis=phase_is(4))
    L("cwgg_u_rat", "§YRatification:§! the Bundestag [U_RatB], the Volkskammer [U_RatD].")
    DT("U_RatB", [("has_country_flag = cwgg_u_rat_brd", "cwgg_u_rat_yes")], "cwgg_u_rat_wait")
    DT("U_RatD", [("has_country_flag = cwgg_u_rat_ddr", "cwgg_u_rat_yes")], "cwgg_u_rat_wait")
    L("cwgg_u_rat_yes", "§Ghas ratified§!")
    L("cwgg_u_rat_wait", "§Yhas still to vote§!")
    # names for events and the window
    DT("U_CurName", [(f"check_variable = {{ cwgg_u_cur = {k} }}", f"cwgg_u_chn_{k}") for k in range(1, 6)], "cwgg_u_none")
    DT("U_LastChapter", [(f"check_variable = {{ cwgg_u_last_ch = {k} }}", f"cwgg_u_chn_{k}") for k in range(1, 6)], "cwgg_u_none", persistent=True)
    DT("U_LastChapterG", [(f"GER = {{ check_variable = {{ cwgg_u_last_ch = {k} }} }}", f"cwgg_u_chn_{k}") for k in range(1, 6)], "cwgg_u_none", persistent=True)
    for k in range(1, 6):
        L(f"cwgg_u_chn_{k}", CH[k][2])
    for nm, var, scope in [("U_LastPos", "cwgg_u_last_pos", ""), ("U_LastDPos", "cwgg_u_last_dpos", ""),
                           ("U_LastPosG", "cwgg_u_last_pos", "GER"), ("U_LastDPosG", "cwgg_u_last_dpos", "GER")]:
        entries = []
        for k in range(1, 6):
            for p in (1, 2, 3):
                c = f"check_variable = {{ cwgg_u_last_ch = {k} }} check_variable = {{ {var} = {p} }}"
                entries.append((f"GER = {{ {c} }}" if scope else c, f"cwgg_u_pn_{k}_{p}"))
        DT(nm, entries, "cwgg_u_nopos", persistent=True)
    L("cwgg_u_nopos", "§Rno position§!")
    for k in range(1, 6):
        DT(f"U_ChG{k}", [(f"GER = {{ check_variable = {{ cwgg_u_ch_{k} = {p} }} }}", f"cwgg_u_pn_{k}_{p}") for p in (1, 2, 3)], "cwgg_u_none", persistent=True)


# ------------------------------------------------------------------ focuses
_TALK = f"check_variable = {{ cwgg_u_phase > 1 }} check_variable = {{ cwgg_u_phase < 5 }}"
F("european_peace_order", "community_of_responsibility", 0, 2, cost=3, pre=[["community_of_responsibility", "coalition_of_reason"]], icon="national_unity",
  name="A European Peace Order",
  desc="Not reunification against the East, but a peace order in Europe in which the German question can be solved by consent - the old dream of Brandt and Bahr. It needs years of trust, treaties that work and four powers that let it happen.",
  avail=f"check_variable = {{ cwgg_klima > 59 }} check_variable = {{ cwgg_stufe < 2 }} check_variable = {{ cwgg_vertrag_6 = 1 }} NOT = {{ has_global_flag = {P}_unity_achieved }}",
  reward=J(climate_base(2), tension(-2), core("ost", stab=0.02),
           unlock("cwgg_unity_unlocked", "§YUnity Talks§! in the new §YUnity§! tab of the inner-German relations window (after three years of unbroken détente)")))
F("social_union", "european_peace_order", -1, 1, cost=3, avail=_TALK, icon="unions", name="A Social Union",
  desc="Pensions, health insurance and unemployment benefit for all Germans on the same terms: the offer that makes a mixed economy acceptable to East German workers - and expensive for West German taxpayers.",
  reward=J(bias(2, 2), faction("dgb", 6), money_gdp(-0.002), core("modell", social=0.02)))
F("berlin_pledge", "european_peace_order", 1, 1, cost=2, avail=_TALK, icon="brandenburg_gate", name="Berlin, Capital of Germany",
  desc="Bonn was always meant to be provisional. A pledge that the united Germany will govern from Berlin wins hearts in the East - and loses some on the Rhine.",
  reward=J(bias(4, 2), party("cdu", -0.002), core("bonn", stab=0.01)))
F("withdrawal_fund", "social_union", 0, 1, cost=3, avail=f"{_TALK} date > 1979.12.31", icon="soviet", name="A Fund for the Soviet Withdrawal",
  desc="Barracks, flats and pensions for the soldiers of the Group of Soviet Forces - paid by Bonn, in advance. A price for Moscow's signature.",
  reward=J(money_gdp(-0.004), consent("sov", 20), opinion("SOV", "medium_increase")))
F("four_power_conference", "berlin_pledge", 0, 1, cost=3, avail=_TALK, icon="diplomacy", name="A Conference of the Four Powers",
  desc="Bonn invites the foreign ministers of the Four Powers to sit with both German states: two plus four, before anything is signed.",
  reward=J(consent("usa", 10), consent("eng", 10), consent("fra", 10), consent("sov", 10), tension(-2)))
F("both_peoples_decide", "withdrawal_fund", 1, 1, cost=3, pre=[["withdrawal_fund", "four_power_conference"]], avail="check_variable = { cwgg_u_phase > 2 } check_variable = { cwgg_u_phase < 5 }",
  icon="election", name="Let Both Peoples Decide",
  desc="A referendum on the same day in both states: if the Germans themselves vote for the treaty, no parliament and no opposition can stand in its way.",
  reward=J(unlock(f"{P}_unity_referendum", "the Bundestag can ratify the unity treaty by §Yreferendum§! instead of a two-thirds majority"), stab(0.02)))


# ------------------------------------------------------------------ the existing unity focuses depend on the mini-game
GATE = "check_variable = { cwgg_stufe < 2 } check_variable = { cwgg_klima > 39 }"
import tree as _tree
for _k in ("ten_point_plan", "support_round_table", "treaty_community", "art146_debate", "neutral_offer", "oder_neisse_final",
           "monetary_union_offer", "two_plus_four_west"):
    _fc = _tree.BY_KEY[_k]
    _old = _fc["avail"].strip()
    if _k in ("ten_point_plan", "support_round_table", "treaty_community", "art146_debate", "neutral_offer", "oder_neisse_final",
              "monetary_union_offer", "two_plus_four_west"):
        _fc["avail"] = (f"OR = {{ AND = {{ {_old} }} AND = {{ {_TALK} }} }} " if _old else "") + GATE
    else:
        _fc["avail"] = (_old + " " + GATE).strip()
_EXTRA_REWARD = {
    "art146_debate": bias(1, 2),
    "neutral_offer": J(bias(3, 2), consent("sov", 20)),
    "oder_neisse_final": J(bias(5, 2), consent("eng", 15), consent("fra", 5)),
    "monetary_union_offer": bias(2, 1),
    "two_plus_four_west": J(consent("usa", 15), consent("eng", 15), consent("fra", 15)),
    "treaty_community": J(bias(1, 2), bias(4, 2)),
}
for _k, _r in _EXTRA_REWARD.items():
    _fc = _tree.BY_KEY[_k]
    _fc["reward"] = J(_fc["reward"], f"if = {{ limit = {{ {_TALK} }} {_r} }}")

events()
ddr_decisions()

import ideas as _ideas
_ideas.IDEAS.update({
    "mixed_economy": ("A Mixed Economy", "The unity treaty kept key industries, banks and land in public hands: a German 'third way' between the systems.", "industrial_concern",
                      {"stability_factor": 0.03, "consumer_goods_factor": 0.02, "production_factory_efficiency_gain_factor": -0.03}),
    "planned_economy": ("A Planned Economy for All Germany", "The unity treaty nationalised the West's industry. The planners in Berlin now run Siemens and Daimler.", "industrial_concern",
                        {"stability_factor": -0.05, "consumer_goods_factor": -0.03, "research_speed_factor": -0.05, "production_speed_buildings_factor": 0.05}),
    "centralised_state": ("A Centralised State", "The Länder are administrative districts; Berlin decides.", "political_power_bonus",
                          {"political_power_factor": 0.05, "stability_factor": -0.03}),
})
_ideas.DDR_IDEAS.update({
    "socialist_unity": ("The Socialist Unity of Germany", "By treaty and with the consent of all Four Powers, the German Democratic Republic has become the state of all Germans.", "anti_soviet_pact",
                        {"stability_factor": -0.05, "political_power_factor": 0.1, "war_support_factor": 0.05}),
})
