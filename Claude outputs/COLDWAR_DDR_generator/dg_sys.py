# IMPERIA CW — Cold War: German Democratic Republic 1970 content generator.
# COLDWAR | Scripted effects and triggers of the GDR tree: initialisation, money, factions, outlooks, Moscow's Trust,
# the Inner-German course, elections, the ladders, the First Secretaries (install, heirs, deaths, succession, the Central
# Committee and the Kremlin's say), Fraternal Assistance, accession, the garrison and the Warsaw Pact.
from dg_common import *
import dg_effects as E
from dg_load import C, FOCI, LADDERS, LEADER_NAME, LEADER_KEYS, FACTION, BYID, TRAITS
from dg_events import EV, SOV_HUMAN

SED = "emerging_communist_state_are_in_power = yes"
DEATHS = {"ulb", "lam", "hof"}
# the leader traits each First Secretary earns in his own tree (re-added when he takes the office again)
TRAIT_FOCI = {}
for f in FOCI:
    for e in f["eff"]:
        if e["k"] == "trait":
            TRAIT_FOCI.setdefault(short(f["id"]).split("_")[0], []).append((f["id"], e["trait"]))
PORTRAIT = {k: E.PORTRAIT.get(n) for k, n in LEADER_NAME.items()}
FACTIONS_USED = sorted(set(FACTION) | {e["f"] for f in FOCI for e in f["eff"] if e["k"] == "fac"})
DYN_START = {"mfs": {"intel_network_gain_factor": 0.10, "police_cost_multiplier_modifier": 0.05},
             "socialist_camp": {"opinion_gain_monthly_same_ideology_factor": 0.10, "mdcw_cw_support_effectiveness": 0.05}}
for g, mods in DYN_START.items():
    keys = E.R.dyn.setdefault(f"{PFX}{g}_modifier", [])
    for m in mods:
        if m not in keys:
            keys.append(m)
OUTLOOK_PARTY = {0: (0, 3, 1), 1: (4, 9, 4), 3: (12, 19, 18), 4: (20, 23, 20)}   # outlook -> (first, last, main GDR party)
WITHDRAWAL_DAYS = (730, 1095, 1825)


def T(key, text):
    LOC[f"{PFX}{key}_tt"] = text
    return f"{PFX}{key}_tt"


def ifelse(chain):
    out = []
    for n, (cond, body) in enumerate(chain):
        if cond is None:
            out += ["else = {"] + body + ["}"]
        else:
            out += [f"{'if' if n == 0 else 'else_if'} = {{", f"limit = {{ {cond} }}"] + body + ["}"]
    return out


def leader_create(k, name=None, pic=None):
    name = name or LEADER_NAME[k]
    pic = pic if pic is not None else PORTRAIT.get(k)
    p = f' picture = "{pic}"' if pic else ""
    return f'create_country_leader = {{ name = "{E.leader_key(name)}"{p} ideology = communist_state traits = {{ emerging_communist_state }} }}'


def build():
    out = [HEADER]
    add = out.append

    # ------------------------------------------------------------------ init
    laws = [l for l, _ in C["start_laws"]]
    facs = [(f, v) for f, _, v in C["start_factions"]]
    spirits = [s["id"] for s in C["start_spirits"]]
    pop = {int(k): v for k, v in C["start_pop"].items()}
    outl = {o: round(sum(v for i, v in pop.items() if a <= i <= b) * 100) for o, (a, b, _) in OUTLOOK_PARTY.items()}
    assert sum(outl.values()) == 100, outl
    L = ["# called from the 1970 history of the GDR (history/countries/DDR - East Germany.txt)",
         "COLDWAR_DDR_initialize_1970 = {", "if = {", f"limit = {{ NOT = {{ has_country_flag = {PFX}initialized }} }}",
         f"set_country_flag = {PFX}initialized", f"set_country_flag = {PFX}first_sec_ulb",
         "# laws, internal factions and the seven starting spirits", "add_ideas = {"] + laws + [f for f, _ in facs] + spirits + ["}"]
    L += [f"set_variable = {{ {f}_opinion = {v} }}" for f, v in facs]
    L += ["initialize_internal_faction_dynamic_modifiers = yes",
          f"# Moscow's Trust (0-100) and the Inner-German course (shadow of the balance of power, -1 Demarcation .. +1 Rapprochement)",
          f"set_variable = {{ {PFX}moscow_trust = {C['trust']['start']} }}",
          f"set_variable = {{ {PFX}course = {fmt(C['course']['initial'])} }}",
          f"set_power_balance = {{ id = {E.COURSE_BOP} left_side = {E.COURSE_BOP}_left_side right_side = {E.COURSE_BOP}_right_side set_value = {fmt(C['course']['initial'])} }}"]
    for g, mods in DYN_START.items():
        L += [f"set_variable = {{ {PFX}{g}_{m} = {fmt(v)} }}" for m, v in mods.items()]
    from dg_manual import DYN_ORDER
    L += ["# the five country modifiers (MD: base modifiers at the start; the foci of each area strengthen them)"]
    L += [f"add_dynamic_modifier = {{ modifier = {PFX}{g}_modifier }}" for g in DYN_ORDER]
    L += [f"add_dynamic_modifier = {{ modifier = {PFX}trust_{t} }}" for t, *_ in TRUST_TIERS]
    L += ["# the parties of the republic (design start popularities)",
          "set_popularities = { " + " ".join(f"{g} = {outl[o]}" for o, g in ((0, "democratic"), (1, "communism"), (3, "neutrality"), (4, "nationalist")))
          + " fascism = 0 }", "set_politics = { ruling_party = communism elections_allowed = no }", "IMP_1970_clear_politics = yes"]
    L += [f"set_variable = {{ party_pop_array^{i} = {fmt(v)} }}" for i, v in sorted(pop.items()) if v > 0]
    L += ["set_variable = { ruling_party = 4 }", "startup_politics = yes", "}", "}"]
    add("\n".join(block(L)) + "\n")

    # ------------------------------------------------------------------ money between two treasuries (offers); one-sided money is written in MD form
    add(f"""# THIS pays a share of its GDP to the country in temp {PFX}transfer_target (temp {PFX}gdp_share, positive)
{PFX}transfer_gdp_share = {{
	set_temp_variable = {{ {PFX}amount = gdp_total }}
	multiply_temp_variable = {{ {PFX}amount = {PFX}gdp_share }}
	set_temp_variable = {{ treasury_change = {PFX}amount }}
	multiply_temp_variable = {{ treasury_change = -1 }}
	modify_treasury_effect = yes
	var:{PFX}transfer_target = {{
		set_temp_variable = {{ treasury_change = {PFX}amount }}
		modify_treasury_effect = yes
	}}
}}
""")
    s = ["# ---- outlook popularity: the ruling party if it belongs to the outlook, otherwise the outlook's main GDR party",
         f"{PFX}change_outlook_popularity = {{"]
    for oid, (a, b, d) in OUTLOOK_PARTY.items():
        s += ["if = {", f"limit = {{ check_variable = {{ {PFX}outlook_id = {oid} }} }}", "if = {",
              f"limit = {{ check_variable = {{ ruling_party > {a - 1} }} check_variable = {{ ruling_party < {b + 1} }} }}",
              "set_temp_variable = { party_index = ruling_party }", "}", f"else = {{ set_temp_variable = {{ party_index = {d} }} }}", "}"]
    s += [f"set_temp_variable = {{ party_popularity_increase = {PFX}outlook_amount }}",
          f"set_temp_variable = {{ temp_outlook_increase = {PFX}outlook_amount }}", "change_relative_party_popularity = yes", "}"]
    add("\n".join(block(s)) + "\n")

    # ------------------------------------------------------------------ Moscow's Trust
    add(f"""# ---- Moscow's Trust (0-100; temp {PFX}trust_delta). The tooltip is shown by the caller. ----------
{PFX}change_trust = {{
	add_to_variable = {{ {PFX}moscow_trust = {PFX}trust_delta }}
	clamp_variable = {{ var = {PFX}moscow_trust min = 0 max = 100 }}
	force_update_dynamic_modifier = yes
}}

# monthly (on_monthly_DDR): -1 at Rapprochement 0.4 or more, -1 while a non-Emerging government rules,
# +1 at Demarcation -0.4 or less while the SED governs (only up to 70); the Ambassador calls below 25
{PFX}monthly = {{
	if = {{ limit = {{ has_country_flag = {PFX}cc_pending NOT = {{ country_exists = SOV }} }} clr_country_flag = {PFX}cc_pending }}
	# Moscow's Trust only matters while the republic is in the Soviet orbit (a subject of Moscow or in the Warsaw Pact)
	if = {{
		limit = {{ {PFX}in_soviet_orbit = yes }}
		{PFX}monthly_trust = yes
	}}
}}

{PFX}monthly_trust = {{
	set_temp_variable = {{ {PFX}trust_delta = 0 }}
	if = {{ limit = {{ check_variable = {{ {PFX}course > 0.39 }} }} add_to_temp_variable = {{ {PFX}trust_delta = -1 }} }}
	if = {{ limit = {{ NOT = {{ has_government = communism }} }} add_to_temp_variable = {{ {PFX}trust_delta = -1 }} }}
	if = {{
		limit = {{ check_variable = {{ {PFX}course < -0.39 }} {SED} check_variable = {{ {PFX}moscow_trust < 70 }} }}
		add_to_temp_variable = {{ {PFX}trust_delta = 1 }}
	}}
	if = {{ limit = {{ NOT = {{ check_variable = {{ {PFX}trust_delta = 0 }} }} }} {PFX}change_trust = yes }}
	if = {{
		limit = {{
			check_variable = {{ {PFX}moscow_trust < 25 }}
			country_exists = SOV
			NOT = {{ has_country_flag = {PFX}ambassador_cooldown }}
		}}
		set_country_flag = {{ flag = {PFX}ambassador_cooldown days = 365 }}
		country_event = {{ id = {NS}.{EV[PFX + 'ambassador_calls']} days = 1 }}
	}}
	# a computer-led Soviet Union courts a rival when trust is low (a human one decides itself, with a decision)
	if = {{
		limit = {{
			check_variable = {{ {PFX}moscow_trust < 31 }}
			{SED}
			country_exists = SOV
			SOV = {{ is_ai = yes }}
			NOT = {{ has_country_flag = {PFX}soviet_endorses_change }}
		}}
		{PFX}soviet_endorses_change = yes
	}}
}}

{PFX}soviet_endorses_change = {{
	country_event = {{ id = {NS}.{EV[PFX + 'soviet_endorses']} days = 1 }}
}}

# ---- the Kremlin's say: a human Soviet Union hears of key steps and may endorse (+5) or object (-5)
{PFX}notify_kremlin_first_sec = {{
	if = {{ limit = {{ {SOV_HUMAN} has_country_flag = {PFX}initialized }} SOV = {{ country_event = {{ id = {NS}.{EV[PFX + 'kremlin_notice_first_sec']} days = 1 }} }} }}
}}
{PFX}notify_kremlin_western_credit = {{
	if = {{ limit = {{ {SOV_HUMAN} }} SOV = {{ country_event = {{ id = {NS}.{EV[PFX + 'kremlin_notice_western_credit']} days = 1 }} }} }}
}}
{PFX}notify_kremlin_basic_treaty = {{
	if = {{ limit = {{ {SOV_HUMAN} }} SOV = {{ country_event = {{ id = {NS}.{EV[PFX + 'kremlin_notice_basic_treaty']} days = 1 }} }} }}
}}
{PFX}kremlin_endorses = {{
	set_temp_variable = {{ {PFX}trust_delta = 5 }}
	{PFX}change_trust = yes
	country_event = {{ id = {NS}.{EV[PFX + 'kremlin_endorsed']} days = 1 }}
}}
{PFX}kremlin_objects = {{
	set_temp_variable = {{ {PFX}trust_delta = -5 }}
	{PFX}change_trust = yes
	country_event = {{ id = {NS}.{EV[PFX + 'kremlin_objected']} days = 1 }}
}}

# ---- Fraternal Assistance: the Soviet Union may decide to intervene (its decision, Moscow category of the Soviet side)
{PFX}open_fraternal_assistance = {{
	custom_effect_tooltip = {T('fraternal_open', 'The Soviet Union may now decide on §RFraternal Assistance§! against the republic - its own decision.')}
	set_country_flag = {{ flag = {PFX}fraternal_assistance_open days = 365 }}
}}

{PFX}bow_to_moscow = {{
	add_stability = -0.10
	custom_effect_tooltip = {T('bow_to_moscow', "Moscow's Trust rises to at least §Y50§!; a government of the SED returns if another party rules.")}
	hidden_effect = {{
		if = {{ limit = {{ check_variable = {{ {PFX}moscow_trust < 50 }} }} set_variable = {{ {PFX}moscow_trust = 50 }} force_update_dynamic_modifier = yes }}
		clr_country_flag = {PFX}fraternal_assistance_open
	}}
	if = {{ limit = {{ NOT = {{ {SED} }} }} {PFX}restore_party_rule = yes }}
}}

{PFX}resist_fraternal_assistance = {{
	add_war_support = 0.10
	custom_effect_tooltip = {T('resist', 'The republic leaves the Warsaw Pact. The Soviet Union goes to war to topple our government.')}
	hidden_effect = {{
		if = {{ limit = {{ is_subject_of = SOV }} SOV = {{ end_puppet = PREV }} }}
		{PFX}leave_warsaw_pact = yes
		if = {{ limit = {{ country_exists = SOV NOT = {{ has_war_with = SOV }} }} SOV = {{ declare_war_on = {{ target = PREV type = topple_government }} }} }}
	}}
}}

# ---- the Warsaw Pact, the garrison, accession ----------------------------------------------------
{PFX}leave_warsaw_pact = {{
	custom_effect_tooltip = {T('leave_wp', 'The republic leaves the §YWarsaw Pact§! and its treaty ties with the Soviet Union.')}
	hidden_effect = {{
		# MD's own exit (array, idea, tech sharing, faction, news); called from our own events, so ROOT is the republic
		if = {{ limit = {{ has_idea = Warsaw_Pact_member }} Warsaw_Pact_leave = yes }}
		if = {{ limit = {{ is_in_faction = yes }} leave_faction = yes }}
	}}
}}
""")
    for d in WITHDRAWAL_DAYS:
        add(f"""{PFX}start_garrison_withdrawal_{d} = {{
	custom_effect_tooltip = {T(f'withdrawal_{d}', f'The Soviet garrison withdraws: the national spirit §YThe Group of Soviet Forces in Germany§! ends in §Y{d} days§!.')}
	hidden_effect = {{
		if = {{
			limit = {{ NOT = {{ has_country_flag = {PFX}garrison_withdrawing }} has_idea = {PFX}the_soviet_garrison }}
			set_country_flag = {PFX}garrison_withdrawing
			country_event = {{ id = {NS}.{EV[PFX + 'garrison_leaves']} days = {d} }}
		}}
	}}
}}
""")
    add(f"""# THIS = the republic (called in Bonn's answer). While it is Moscow's subject, the Soviet Union decides first (Two Plus Four).
{PFX}start_accession = {{
	if = {{
		limit = {{ is_subject_of = SOV }}
		custom_effect_tooltip = {T('accession_moscow', 'The republic is bound to Moscow: the §YSoviet Union decides§! whether it lets the republic go (Two Plus Four). If it agrees, the transition year begins.')}
		hidden_effect = {{ SOV = {{ country_event = {{ id = {NS}.{EV[PFX + 'two_plus_four']} days = 1 }} }} }}
	}}
	else = {{ {PFX}begin_transition = yes }}
}}

{PFX}begin_transition = {{
	custom_effect_tooltip = {T('accession', 'After a §Ytransition year§! the republic joins the Federal Republic of Germany peacefully.')}
	add_timed_idea = {{ idea = {PFX}accession_transition days = 365 }}
	hidden_effect = {{
		set_country_flag = {PFX}accession_pending
		country_event = {{ id = {NS}.{EV[PFX + 'accession_complete']} days = 365 }}
	}}
}}

{PFX}complete_accession = {{
	clr_country_flag = {PFX}accession_pending
	{PFX}leave_warsaw_pact = yes
	if = {{
		limit = {{ has_country_flag = {PFX}social_charter }}
		GER = {{ add_timed_idea = {{ idea = {PFX}eastern_social_charter days = 1825 }} }}
	}}
	GER = {{ annex_country = {{ target = PREV transfer_troops = yes }} }}
}}

# ---- elections ----------------------------------------------------------------------------------
{PFX}allow_elections = {{
	custom_effect_tooltip = {T('allow_elections', '§GElections are allowed.§!')}
	set_variable = {{ disable_elections = 0 }}
	hidden_effect = {{
		if = {{ limit = {{ has_government = democratic }} set_politics = {{ ruling_party = democratic elections_allowed = yes }} }}
		if = {{ limit = {{ has_government = communism }} set_politics = {{ ruling_party = communism elections_allowed = yes }} }}
		if = {{ limit = {{ has_government = fascism }} set_politics = {{ ruling_party = fascism elections_allowed = yes }} }}
		if = {{ limit = {{ has_government = neutrality }} set_politics = {{ ruling_party = neutrality elections_allowed = yes }} }}
		if = {{ limit = {{ has_government = nationalist }} set_politics = {{ ruling_party = nationalist elections_allowed = yes }} }}
	}}
}}

{PFX}suspend_elections = {{
	custom_effect_tooltip = {T('suspend_elections', '§RElections are abolished.§!')}
	set_variable = {{ disable_elections = 1 }}
	hidden_effect = {{
		if = {{ limit = {{ has_government = democratic }} set_politics = {{ ruling_party = democratic elections_allowed = no }} }}
		if = {{ limit = {{ has_government = communism }} set_politics = {{ ruling_party = communism elections_allowed = no }} }}
		if = {{ limit = {{ has_government = fascism }} set_politics = {{ ruling_party = fascism elections_allowed = no }} }}
		if = {{ limit = {{ has_government = neutrality }} set_politics = {{ ruling_party = neutrality elections_allowed = no }} }}
		if = {{ limit = {{ has_government = nationalist }} set_politics = {{ ruling_party = nationalist elections_allowed = no }} }}
	}}
}}
""")

    # ------------------------------------------------------------------ ladders
    s = ["# ==== ladders: one active form at a time (steps get lighter with 'down'; 'clear' ends every form) ====="]
    for name, op in sorted({(n, "clear") for n, _ in E.R.ladder_ops} | E.R.ladder_ops):
        ids = E.ladder_ids(name)
        if op in ("clear", "remove", "replace", "up"):
            if f"{PFX}ladder_{name}_clear = {{" in "\n".join(s):
                continue
            s += [f"{PFX}ladder_{name}_clear = {{"] + [f"if = {{ limit = {{ has_idea = {i} }} remove_ideas = {i} }}" for i in ids] + ["}", ""]
        elif op == "down":
            steps = [PFX + x for x in LADDERS[name]["steps"]]
            chain = [(f"has_idea = {a}", [f"swap_ideas = {{ remove_idea = {a} add_idea = {b} }}"]) for a, b in zip(steps, steps[1:])]
            if name != "recognition":   # the last step eases away; the recognised state stays recognised
                chain.append((f"has_idea = {steps[-1]}", [f"remove_ideas = {steps[-1]}"]))
            s += [f"{PFX}ladder_{name}_down = {{"] + ifelse(chain) + ["}", ""]
    add("\n".join(block(s)) + "\n")

    # ------------------------------------------------------------------ First Secretaries
    s = ["# ==== First Secretaries of the SED ===============================================================",
         f"{PFX}clear_first_sec = {{"] + [f"clr_country_flag = {PFX}first_sec_{k}" for k in LEADER_KEYS] + [f"clr_country_flag = {PFX}kessler_leads", "}", "",
         f"{PFX}clear_heirs = {{"] + [f"clr_country_flag = {PFX}heir_{k}" for k in LEADER_KEYS] + ["}", ""]
    for k in LEADER_KEYS:
        name = LEADER_NAME[k]
        LOC[f"{PFX}install_{k}_tt"] = f"§Y{name}§! becomes First Secretary of the SED. The tree of his predecessor closes; his own opens."
        traits = [f"if = {{ limit = {{ has_completed_focus = {fid} }} add_country_leader_trait = {tr} }}" for fid, tr in TRAIT_FOCI.get(k, [])]
        s += [f"{PFX}install_first_sec_{k} = {{", f"custom_effect_tooltip = {PFX}install_{k}_tt", "hidden_effect = {",
              f"{PFX}clear_first_sec = yes", f"{PFX}clear_heirs = yes", f"clr_country_flag = {PFX}ulb_retiring", f"clr_country_flag = {PFX}cc_pending",
              f"set_country_flag = {PFX}first_sec_{k}", "if = {", f"limit = {{ {SED} }}", "retire_country_leader = yes", leader_create(k)] + traits + \
             [f"news_event = {{ id = {NS}.{EV[PFX + 'new_first_secretary']} hours = 6 }}", "}", f"{PFX}notify_kremlin_first_sec = yes",
              "force_update_dynamic_modifier = yes", "}", "}", ""]
        LOC[f"{PFX}heir_{k}_tt"] = f"Designated heir: §Y{name}§!. When the First Secretary dies or retires, the Central Committee elects him."
        s += [f"{PFX}set_heir_{k} = {{", f"{PFX}clear_heirs = yes", f"set_country_flag = {PFX}heir_{k}", f"custom_effect_tooltip = {PFX}heir_{k}_tt",
              f"if = {{ limit = {{ has_country_flag = {PFX}ulb_retiring has_country_flag = {PFX}first_sec_ulb }} "
              f"hidden_effect = {{ country_event = {{ id = {NS}.{EV[PFX + 'heir_elected']} days = 7 }} }} }}", "}", ""]
    # Keßler carries Hoffmann's course (the flag of Hoffmann stays, so his tree stays open)
    LOC[f"{PFX}install_kessler_tt"] = "§YHeinz Keßler§! becomes First Secretary of the SED and carries on Hoffmann's course."
    s += [f"{PFX}install_kessler = {{", f"custom_effect_tooltip = {PFX}install_kessler_tt", "hidden_effect = {", f"{PFX}clear_heirs = yes",
          f"set_country_flag = {PFX}kessler_leads",
          "if = {", f"limit = {{ {SED} }}", "retire_country_leader = yes",
          leader_create("hof", "Heinz Keßler", "gfx/leaders/DDR/DDR_Heinz_Kessler.dds"), f"add_country_leader_trait = {PFX}hof_army_general",
          f"news_event = {{ id = {NS}.{EV[PFX + 'new_first_secretary']} hours = 6 }}", "}", f"{PFX}notify_kremlin_first_sec = yes", "}", "}", ""]
    # succession: the designated heir first, otherwise the Central Committee chooses
    chain = [(f"has_country_flag = {PFX}heir_{k} {PFX}alive_{k} = yes NOT = {{ has_country_flag = {PFX}first_sec_{k} }}",
              [f"{PFX}install_first_sec_{k} = yes"]) for k in LEADER_KEYS]
    chain.append((None, [f"country_event = {{ id = {NS}.{EV[PFX + 'succession_plenum']} days = 1 }}"]))
    s += ["# the designated heir is elected; otherwise the Central Committee chooses among the living (event)",
          f"{PFX}succession = {{"] + ifelse(chain) + ["}", ""]
    for k in sorted(DEATHS):
        body = [f"set_country_flag = {PFX}dead_{k}"]
        if k == "hof":
            body += ["if = {", f"limit = {{ has_country_flag = {PFX}first_sec_hof }}",
                     "if = {", f"limit = {{ has_country_flag = {PFX}hof_kessler_junta_option NOT = {{ has_country_flag = {PFX}kessler_refused }} }}",
                     f"country_event = {{ id = {NS}.{EV[PFX + 'kessler_succession']} days = 1 }}", "}", f"else = {{ {PFX}succession = yes }}", "}"]
        else:
            body += [f"if = {{ limit = {{ has_country_flag = {PFX}first_sec_{k} }} {PFX}succession = yes }}"]
        body += [f"if = {{ limit = {{ has_country_flag = {PFX}heir_{k} }} clr_country_flag = {PFX}heir_{k} }}"]
        LOC[f"{PFX}dies_{k}_tt"] = f"§Y{LEADER_NAME[k]}§! is dead. If he led the party, the Central Committee elects a successor."
        s += [f"{PFX}leader_dies_{k} = {{", f"custom_effect_tooltip = {PFX}dies_{k}_tt", "hidden_effect = {"] + body + ["}", "}", ""]
    # back to party rule from another party's tree: the living First Secretary takes over the state again
    kes = [(f"has_country_flag = {PFX}kessler_leads", ["retire_country_leader = yes", leader_create("hof", "Heinz Keßler", "gfx/leaders/DDR/DDR_Heinz_Kessler.dds"),
                                                       f"add_country_leader_trait = {PFX}hof_army_general"])]
    chain = kes + [(f"has_country_flag = {PFX}first_sec_{k} {PFX}alive_{k} = yes",
              ["retire_country_leader = yes", leader_create(k)] + [f"if = {{ limit = {{ has_completed_focus = {fid} }} add_country_leader_trait = {tr} }}"
                                                                    for fid, tr in TRAIT_FOCI.get(k, [])]) for k in LEADER_KEYS]
    chain.append((None, [f"{PFX}succession = yes"]))
    s += [f"{PFX}restore_party_rule = {{", "set_temp_variable = { rul_party_temp = 4 }", "change_ruling_party_effect = yes", "hidden_effect = {"] + \
         ifelse(chain) + ["}", "}", ""]
    # the Central Committee: the candidate of a running convention (global.COLDWAR_DDR_cc_candidate = index in LEADER_KEYS + 1)
    approve = [(f"check_variable = {{ global.{PFX}cc_candidate = {i + 1} }} {PFX}alive_{k} = yes NOT = {{ has_country_flag = {PFX}first_sec_{k} }}",
                [f"{PFX}install_first_sec_{k} = yes"]) for i, k in enumerate(LEADER_KEYS)]
    veto = [(f"check_variable = {{ global.{PFX}cc_candidate = {i + 1} }}", [f"set_country_flag = {{ flag = {PFX}cc_failed_{k} days = 180 }}"])
            for i, k in enumerate(LEADER_KEYS)]
    s += ["# THIS = GDR; the Kremlin (human Soviet Union) has answered",
          f"{PFX}cc_approved = {{", f"clr_country_flag = {PFX}cc_pending"] + ifelse(approve) + ["}", "",
          f"{PFX}cc_vetoed = {{", f"clr_country_flag = {PFX}cc_pending"] + ifelse(veto) + [
          f"country_event = {{ id = {NS}.{EV[PFX + 'kremlin_veto']} days = 1 }}", "}", ""]
    add("\n".join(block(s)) + "\n")
    return "\n".join(out) + "\n"


# Moscow's Trust tiers (dynamic modifiers with enable conditions; 45-64 'Under Observation' has no effect)
ORBIT = f"{PFX}in_soviet_orbit = yes"
TRUST_TIERS = [
    ("brothers_in_arms", "Moscow's Trust: Brothers in Arms", f"{ORBIT} check_variable = {{ {PFX}moscow_trust > 84 }}",
     [("political_power_factor", 0.05), ("stability_factor", 0.03), ("tax_gain_multiplier_modifier", 0.03)]),
    ("garrison_relief", "Brothers in Arms: The Garrison Is Ours", f"{ORBIT} check_variable = {{ {PFX}moscow_trust > 84 }} has_idea = {PFX}the_soviet_garrison",
     [("political_power_factor", 0.05)]),
    ("reliable_ally", "Moscow's Trust: Reliable Ally", f"{ORBIT} check_variable = {{ {PFX}moscow_trust > 64 }} check_variable = {{ {PFX}moscow_trust < 85 }}",
     [("political_power_factor", 0.03), ("stability_factor", 0.02)]),
    ("displeasure", "Moscow's Trust: Moscow's Displeasure", f"{ORBIT} check_variable = {{ {PFX}moscow_trust > 24 }} check_variable = {{ {PFX}moscow_trust < 45 }}",
     [("political_power_factor", -0.05), ("stability_factor", -0.03), ("production_speed_buildings_factor", -0.05)]),
    ("brezhnev_doctrine", "Moscow's Trust: The Brezhnev Doctrine", f"{ORBIT} check_variable = {{ {PFX}moscow_trust < 25 }}",
     [("political_power_factor", -0.10), ("stability_factor", -0.10)]),
]


def triggers():
    s = [HEADER, "# ---- AI paths (MD Russia: SOV_ai_historical_path); read in the ai_will_do of the foci"]
    import dg_focus as FO
    for name, body in FO.AI_TRIGGERS.items():
        s += [f"{name} = {{"] + body + ["}", ""]
    for k in LEADER_KEYS:
        s += [f"{PFX}alive_{k} = {{"] + ([f"NOT = {{ has_country_flag = {PFX}dead_{k} }}"] if k in DEATHS else ["always = yes"]) + ["}", ""]
    s += ["# the republic is in the Soviet orbit: a subject of Moscow or a member of the Warsaw Pact",
          f"{PFX}in_soviet_orbit = {{", "OR = {", "is_subject_of = SOV", "has_idea = Warsaw_Pact_member", "}", "}", ""]
    for name in sorted({n for n, _ in E.R.ladder_ops}):
        s += [f"{PFX}ladder_{name}_active = {{", "OR = {"] + [f"has_idea = {i}" for i in E.ladder_ids(name)] + ["}", "}", ""]
    s += ["# the GDR exists, plays the 1970 tree and the SED governs", f"{PFX}sed_governs = {{", "original_tag = DDR", f"has_country_flag = {PFX}initialized",
          SED, "}", ""]
    return "\n".join(block(s)) + "\n"
