# IMPERIA COLD WAR — Argentina 1970 political integration
"""Pure generator for the Argentina 1970 political integration hooks."""

from __future__ import annotations


# Party seats in the Argentina registry are the live ruling_party indices. Dates
# select historically eligible officeholders only after a real party transition.
_LEADER_CASES = [
    (0, "before_1970_06_01", "Pedro Eugenio Aramburu", "Western_Autocracy", None),
    (0, "after_1970_05_31", "UDELPA National Executive", "Western_Autocracy", None),
    (1, "always", "Francisco Gabrielli", "conservatism", None),
    (2, "before_1983_04", "Arturo Frondizi", "liberalism", None),
    (2, "after_1983_04", "Rogelio Frigerio", "liberalism", None),
    (3, "before_1981_09_10", "Ricardo Balbín", "socialism", None),
    (3, "after_1981_09_09", "Raúl Alfonsín", "socialism", "gfx/leaders/ARG/raul_alfonsin.dds"),
    (4, "before_1970_04", "Victorio Codovilla", "communist_state", None),
    (4, "before_1980_06_12", "Gerónimo Arnedo Álvarez", "communist_state", None),
    (4, "after_1980_06_11", "Communist Party Central Committee", "communist_state", None),
    (5, "always", "Mario Firmenich", "anarchist_communism", None),
    (6, "before_1983_03_19", "Mario Amadeo", "Conservative", None),
    (6, "after_1983_03_18", "Ateneo Republican Council", "Conservative", None),
    (13, "before_1974_07", "Juan Perón", "Neutral_Autocracy", "gfx/leaders/mdcw_historical_pool/ARG_juan_peron.dds"),
    (13, "before_1976_03", "Isabel Perón", "Neutral_Autocracy", None),
    (13, "before_1989_07", "Ítalo Luder", "Neutral_Autocracy", None),
    (13, "after_1989_07", "Carlos Menem", "Neutral_Autocracy", "gfx/leaders/mdcw_historical_pool/ARG_carlos_menem.dds"),
    (14, "before_1983_12", "Horacio Sueldo", "Neutral_conservatism", None),
    (14, "after_1983_12", "Carlos Auyero", "Neutral_conservatism", None),
    (15, "before_1978_01", "Celedonio Pereda", "oligarchism", None),
    (15, "after_1978_01", "Jorge Zorreguieta", "oligarchism", None),
    (16, "always", "Álvaro Alsogaray", "Neutral_Libertarian", None),
    (18, "psd", "Alfredo Bravo", "neutral_Social", "gfx/leaders/ARG/alfredo_bravo.dds"),
    (18, "cgta", "Raimundo Ongaro", "neutral_Social", None),
    (19, "before_1976_07", "Mario Roberto Santucho", "Neutral_Communism", None),
    (19, "after_1976_07", "Enrique Gorriarán Merlo", "Neutral_Communism", None),
    (20, "always", "Lorenzo Miguel", "Nat_Populism", None),
    (22, "before_1970_06", "Juan Carlos Ongania", "Nat_Autocracy", "gfx/leaders/ARG/ARG_Coldwar_Juan_Carlos_Ongania.dds"),
    (22, "before_1971_03", "Roberto Marcelo Levingston", "Nat_Autocracy", "gfx/leaders/mdcw_historical_pool/ARG_roberto_marcelo_levingston.dds"),
    (22, "before_1973_05", "Alejandro Agustín Lanusse", "Nat_Autocracy", None),
    (22, "always_after_1973", "General Staff of the Argentine Armed Forces", "Nat_Autocracy", "gfx/leaders/ARG/argentinian_armed_forces.dds"),
]


def _leader_key(name: str) -> str:
    import unicodedata
    return "COLDWAR_ARG_leader_" + "".join(c.lower() if c.isalnum() else "_" for c in unicodedata.normalize("NFKD", name) if not unicodedata.combining(c)).strip("_")


def _leader_triggers() -> str:
    result = []
    for _, _, name, _, _ in _LEADER_CASES:
        key = _leader_key(name)
        if any(line.startswith(key + " = {") for line in result):
            continue
        aliases = [name]
        if name == "Juan Carlos Ongania":
            aliases.append("Juan Carlos Ongánía")
        if name == "Alejandro Agustín Lanusse":
            aliases.append("Alejandro Agustin Lanusse")
        if name == "Juan Perón":
            aliases.extend(["Juan Domingo Perón", "Juan Domingo Peron"])
        if name == "Isabel Perón":
            aliases.extend(["María Estela Martínez de Perón", "Isabel Peron"])
        if name == "Raúl Alfonsín":
            aliases.append("Raul Alfonsin")
        checks = "\n".join(f'\t\thas_country_leader = {{ name = "{a}" ruling_only = yes }}' for a in aliases)
        result.append(f"{key} = {{\n\tOR = {{\n{checks}\n\t}}\n}}")
    return "\n".join(result) + "\n"


def _date_limit(label: str) -> str:
    ranges = {
        "always": "",
        "psd": "",
        "cgta": "",
        "before_1983_04": "date < 1983.4.18",
        "after_1983_04": "date > 1983.4.17",
        "before_1970_06_01": "date < 1970.6.1",
        "after_1970_05_31": "date > 1970.5.31",
        "before_1983_12": "date < 1983.12.10",
        "after_1983_12": "date > 1983.12.9",
        "before_1981_09_10": "date < 1981.9.10",
        "after_1981_09_09": "date > 1981.9.9",
        "before_1970_04": "date < 1970.4.15",
        "after_1970_04": "date > 1970.4.14",
        "before_1980_06_12": "date < 1980.6.12",
        "after_1980_06_11": "date > 1980.6.11",
        "before_1983_03_19": "date < 1983.3.19",
        "after_1983_03_18": "date > 1983.3.18",
        "before_1974_07": "date < 1974.7.1",
        "before_1976_03": "date < 1976.3.24",
        "before_1989_07": "date < 1989.7.8",
        "after_1989_07": "date > 1989.7.7",
        "before_1978_01": "date < 1978.1.1",
        "after_1978_01": "date > 1977.12.31",
        "before_1976_07": "date < 1976.7.19",
        "after_1976_07": "date > 1976.7.18",
        "before_1970_06": "date < 1970.6.9",
        "before_1971_03": "date < 1971.3.26",
        "before_1973_05": "date < 1973.5.25",
        "always_after_1973": "date > 1973.5.24",
    }
    return ranges[label]


def _leader_selection_effect() -> str:
    rows = [
        "# Selects an actual political officeholder only after a lawful party transition.",
        "COLDWAR_ARG_select_leader_for_current_party = {",
        "\tif = {",
        "\t\tlimit = { original_tag = ARG IMP_is_1970_scenario = yes has_country_flag = COLDWAR_ARG_leader_transition_authorized }",
    ]
    for index, (party, when, name, ideology, picture) in enumerate(_LEADER_CASES):
        key = _leader_key(name)
        clauses = [f"check_variable = {{ ruling_party = {party} }}"]
        date_clause = _date_limit(when)
        if date_clause:
            clauses.append(date_clause)
        if when == "psd":
            clauses.append("has_country_flag = COLDWAR_ARG_slot18_psd_candidate")
        if when == "cgta":
            clauses.append("NOT = { has_country_flag = COLDWAR_ARG_slot18_psd_candidate }")
        if party == 22 and when == "before_1971_03":
            clauses.append("has_country_flag = COLDWAR_ARG_command_crisis_resolved")
        if party == 22 and when == "before_1973_05":
            clauses.append("has_country_flag = COLDWAR_ARG_lanusse_appointed")
        condition = " ".join(clauses)
        branch = "if" if index == 0 else "else_if"
        rows.append(f"\t\t{branch} = {{")
        rows.append(f"\t\t\tlimit = {{ {condition} }}")
        rows.append(f"\t\t\tif = {{ limit = {{ NOT = {{ {key} = yes }} }}")
        rows.append("\t\t\t\thidden_effect = { retire_country_leader = yes }")
        rows.append("\t\t\t\tcreate_country_leader = {")
        rows.append(f'\t\t\t\t\tname = "{name}"')
        rows.append(f'\t\t\t\t\tpicture = "{picture or "gfx/interface/coldwar_politburo/portrait_unknown.dds"}"')
        rows.append(f"\t\t\t\t\tideology = {ideology}")
        rows.append("\t\t\t\t\ttraits = { }")
        rows.append("\t\t\t\t}")
        rows.append("\t\t\t\tset_correct_ideology_trait = yes")
        rows.append("\t\t\t}")
        if party == 18:
            rows.append("\t\t\tCOLDWAR_ARG_mark_psd_incumbent = yes" if when == "psd" else "\t\t\tCOLDWAR_ARG_mark_cgta_incumbent = yes")
        rows.append("\t\t}")
    rows.extend([
        "\t\tset_variable = { COLDWAR_ARG_leader_routed_party = ruling_party }",
        "\t\tclr_country_flag = COLDWAR_ARG_leader_transition_authorized",
        "\t}",
        "\telse_if = { limit = { original_tag = ARG IMP_is_1970_scenario = yes NOT = { has_variable = COLDWAR_ARG_leader_routed_party } } set_variable = { COLDWAR_ARG_leader_routed_party = ruling_party } }",
        "}",
    ])
    return "\n".join(rows) + "\n"


def _effects() -> str:
    body = '''# IMPERIA COLD WAR — Argentina1970 political integration
COLDWAR_ARG_initialize_politics = {
	if = {
		limit = { original_tag = ARG IMP_is_1970_scenario = yes }
		if = {
			limit = { NOT = { has_country_flag = COLDWAR_ARG_politics_initialized } }
			set_country_flag = COLDWAR_ARG_politics_initialized
			set_variable = { COLDWAR_ARG_current_junta_leader = 0 }
			set_variable = { COLDWAR_ARG_leader_routed_party = ruling_party }
		}
		COLDWAR_ARG_refresh_politics = yes
	}
}

# Reconcile only identity metadata. This effect never creates, kills, or selects a leader.
COLDWAR_ARG_refresh_politics = {
	if = {
		limit = { original_tag = ARG IMP_is_1970_scenario = yes }
		COLDWAR_ARG_resolve_native_election = yes
		update_set_politics = yes
		if = { limit = { NOT = { check_variable = { ruling_party = 18 } } }
			clr_country_flag = COLDWAR_ARG_incumbent_psd
			clr_country_flag = COLDWAR_ARG_incumbent_cgta
		}
		else_if = { limit = { has_country_flag = COLDWAR_ARG_incumbent_psd }
			clr_country_flag = COLDWAR_ARG_incumbent_cgta
		}
		else_if = { limit = { has_country_flag = COLDWAR_ARG_incumbent_cgta }
			clr_country_flag = COLDWAR_ARG_incumbent_psd
		}
		else = {
			# Native slot 18 currently identifies CGTA. A PSD government must be marked by
			# the real election or a lawful party reorganization before this refresh runs.
			set_country_flag = COLDWAR_ARG_incumbent_cgta
		}
		if = {
			limit = { COLDWAR_ARG_is_psd_incumbent = yes }
			set_party_name = { ideology = neutrality name = COLDWAR_ARG_party_18_psd long_name = COLDWAR_ARG_party_18_psd }
		}
		else_if = {
			limit = { COLDWAR_ARG_is_cgta_incumbent = yes }
			set_party_name = { ideology = neutrality name = COLDWAR_ARG_party_18_cgta long_name = COLDWAR_ARG_party_18_cgta }
		}
		if = {
			limit = { COLDWAR_ARG_is_ucede_incumbent = yes }
			set_party_name = { ideology = neutrality name = COLDWAR_ARG_party_16_ucede long_name = COLDWAR_ARG_party_16_ucede }
		}
	}
}

# The approved UCeDe focus may call this only after the real post-1982 organization
# exists. It changes the identity within slot 16's PCI tradition; it never renames PD.
COLDWAR_ARG_form_ucede_identity = {
	if = {
		limit = {
			original_tag = ARG
			IMP_is_1970_scenario = yes
			date > 1982.1.1
			check_variable = { ruling_party = 16 }
			has_elections = yes
			NOT = { has_country_flag = COLDWAR_ARG_ucede_formed }
		}
		set_country_flag = COLDWAR_ARG_ucede_formed
		set_party_name = { ideology = neutrality name = COLDWAR_ARG_party_16_ucede long_name = COLDWAR_ARG_party_16_ucede }
	}
}

COLDWAR_ARG_mark_psd_incumbent = {
	if = { limit = { original_tag = ARG check_variable = { ruling_party = 18 } }
		clr_country_flag = COLDWAR_ARG_incumbent_cgta
		set_country_flag = COLDWAR_ARG_incumbent_psd
		set_country_flag = COLDWAR_ARG_slot18_psd_candidate
		clr_country_flag = COLDWAR_ARG_slot18_cgta_candidate
		set_party_name = { ideology = neutrality name = COLDWAR_ARG_party_18_psd long_name = COLDWAR_ARG_party_18_psd }
	}
}

COLDWAR_ARG_mark_cgta_incumbent = {
	if = { limit = { original_tag = ARG check_variable = { ruling_party = 18 } }
		clr_country_flag = COLDWAR_ARG_incumbent_psd
		set_country_flag = COLDWAR_ARG_incumbent_cgta
		set_country_flag = COLDWAR_ARG_slot18_cgta_candidate
		clr_country_flag = COLDWAR_ARG_slot18_psd_candidate
		set_party_name = { ideology = neutrality name = COLDWAR_ARG_party_18_cgta long_name = COLDWAR_ARG_party_18_cgta }
	}
}

COLDWAR_ARG_check_lanusse_succession = {
	if = {
		limit = {
			COLDWAR_ARG_lanusse_succession_due = yes
			NOT = { has_country_flag = COLDWAR_ARG_lanusse_succession_pending }
		}
		set_country_flag = COLDWAR_ARG_lanusse_succession_pending
		country_event = { id = COLDWAR_ARG_politics.2 }
	}
}

COLDWAR_ARG_install_ongania = {
	if = {
		limit = {
			original_tag = ARG
			IMP_is_1970_scenario = yes
			check_variable = { ruling_party = 22 }
			COLDWAR_ARG_is_leader_ongania = yes
			has_country_flag = COLDWAR_ARG_event_commanders_seen
		}
		set_variable = { COLDWAR_ARG_current_junta_leader = 0 }
		set_variable = { Nat_Autocracy_leader = 0 }
		set_country_flag = COLDWAR_ARG_command_crisis_resolved
	}
}

COLDWAR_ARG_install_levingston = {
	if = {
		limit = {
			original_tag = ARG
			IMP_is_1970_scenario = yes
			check_variable = { ruling_party = 22 }
			COLDWAR_ARG_is_leader_ongania = yes
			has_country_flag = COLDWAR_ARG_event_commanders_seen
			NOT = { has_country_flag = COLDWAR_ARG_command_crisis_resolved }
		}
		hidden_effect = { retire_country_leader = yes }
		create_country_leader = {
			name = "Roberto Marcelo Levingston"
			picture = "gfx/leaders/mdcw_historical_pool/ARG_roberto_marcelo_levingston.dds"
			ideology = Nat_Autocracy
			traits = { }
		}
		set_variable = { COLDWAR_ARG_current_junta_leader = 1 }
		set_variable = { Nat_Autocracy_leader = 1 }
		set_variable = { COLDWAR_ARG_leader_routed_party = 22 }
		set_country_flag = COLDWAR_ARG_command_crisis_resolved
		COLDWAR_ARG_refresh_politics = yes
	}
}

COLDWAR_ARG_authorize_early_lanusse = {
	if = {
		limit = {
			original_tag = ARG
			IMP_is_1970_scenario = yes
			check_variable = { ruling_party = 22 }
			COLDWAR_ARG_is_leader_ongania = yes
			has_country_flag = COLDWAR_ARG_event_commanders_seen
			NOT = { has_country_flag = COLDWAR_ARG_command_crisis_resolved }
		}
		set_country_flag = COLDWAR_ARG_early_lanusse_authorized
	}
}

COLDWAR_ARG_install_lanusse = {
	if = {
		limit = {
			original_tag = ARG
			IMP_is_1970_scenario = yes
			check_variable = { ruling_party = 22 }
			OR = {
				AND = { COLDWAR_ARG_is_leader_ongania = yes has_country_flag = COLDWAR_ARG_event_commanders_seen has_country_flag = COLDWAR_ARG_early_lanusse_authorized NOT = { has_country_flag = COLDWAR_ARG_command_crisis_resolved } }
				AND = { COLDWAR_ARG_is_leader_levingston = yes date > 1971.3.21 }
			}
		}
		hidden_effect = { retire_country_leader = yes }
		create_country_leader = {
			name = "Alejandro Agustín Lanusse"
			picture = "gfx/interface/coldwar_politburo/portrait_unknown.dds"
			ideology = Nat_Autocracy
			traits = { }
		}
		set_variable = { COLDWAR_ARG_current_junta_leader = 2 }
		set_variable = { Nat_Autocracy_leader = 2 }
		set_variable = { COLDWAR_ARG_leader_routed_party = 22 }
		set_country_flag = COLDWAR_ARG_command_crisis_resolved
		set_country_flag = COLDWAR_ARG_lanusse_appointed
		set_country_flag = COLDWAR_ARG_lanusse_succession_resolved
		clr_country_flag = COLDWAR_ARG_early_lanusse_authorized
		COLDWAR_ARG_refresh_politics = yes
	}
}

# Called by the authorized constitutional-election decision after the political
# programme has legalized competition and published its timetable. The native MD
# election calculation selects and records the winner; installation is a later step.
COLDWAR_ARG_open_constitutional_election = {
	if = {
		limit = {
			original_tag = ARG
			IMP_is_1970_scenario = yes
			has_country_flag = COLDWAR_ARG_party_organization_legalized
			has_country_flag = COLDWAR_ARG_electoral_timetable_published
			has_country_flag = COLDWAR_ARG_election_framework_ready
			NOT = { has_country_flag = COLDWAR_ARG_native_election_pending }
			has_elections = no
		}
		# Keep the incumbent outlook while opening the ballot. Native MD's helper
		# protects the current leader during the political-view update.
		set_temp_variable = { election_year_param = global.year }
		set_temp_variable = { election_month_param = global.month }
		set_temp_variable = { election_freq = 48 }
		set_elections_with_frequency = yes
		set_country_flag = COLDWAR_ARG_native_election_pending
		set_country_flag = elections_in_progress
		clr_country_flag = COLDWAR_ARG_native_government_resolved
		clr_country_flag = COLDWAR_ARG_decision_civilian_handover_done
		clr_country_flag = COLDWAR_ARG_elected_handover_completed
		clr_country_flag = COLDWAR_ARG_elected_incumbent_installed
		clear_variable = COLDWAR_ARG_last_election_winner
		# Enter MD's election resolver once. The result is captured after its native
		# hold_elections call by the shared MD4_election.0 integration.
		country_event = { id = MD4_election.0 }
	}
}

# Called immediately after MD's hold_elections in MD4_election.0. This starts the
# pending-result lifecycle; MD's native event chain remains responsible for choosing
# and installing the government, including coalition outcomes.
COLDWAR_ARG_record_native_election = {
	if = {
		limit = {
			original_tag = ARG
			IMP_is_1970_scenario = yes
			has_country_flag = COLDWAR_ARG_party_organization_legalized
			has_country_flag = COLDWAR_ARG_electoral_timetable_published
			has_country_flag = COLDWAR_ARG_election_framework_ready
			has_elections = yes
		}
		set_country_flag = COLDWAR_ARG_real_election_held
		set_country_flag = COLDWAR_ARG_native_election_pending
		clr_country_flag = COLDWAR_ARG_native_government_resolved
		clr_country_flag = COLDWAR_ARG_slot18_identity_event_pending
		clr_country_flag = COLDWAR_ARG_decision_civilian_handover_done
		clr_country_flag = COLDWAR_ARG_elected_handover_completed
		clr_country_flag = COLDWAR_ARG_elected_incumbent_installed
		clear_variable = COLDWAR_ARG_last_election_winner
	}
}

# Observe MD's completed result only after its native election event clears the
# in-progress flag. ruling_party now reflects the actual single-party or coalition
# outcome; max_index_1 is never used as a substitute for the governing party.
COLDWAR_ARG_resolve_native_election = {
	if = {
		limit = {
			original_tag = ARG
			IMP_is_1970_scenario = yes
			has_country_flag = COLDWAR_ARG_native_election_pending
			NOT = { has_country_flag = COLDWAR_ARG_native_government_resolved }
			NOT = { has_country_flag = elections_in_progress }
			NOT = { has_country_flag = coalition_forming }
		}
		set_variable = { COLDWAR_ARG_last_election_winner = ruling_party }
		if = {
			limit = {
				check_variable = { COLDWAR_ARG_last_election_winner > -1 }
				check_variable = { COLDWAR_ARG_last_election_winner < 24 }
			}
			set_country_flag = COLDWAR_ARG_native_government_resolved
			if = {
				limit = {
					check_variable = { COLDWAR_ARG_last_election_winner = 18 }
					NOT = { has_country_flag = COLDWAR_ARG_slot18_identity_selected }
			}
				set_country_flag = COLDWAR_ARG_slot18_identity_event_pending
				country_event = { id = COLDWAR_ARG_politics.1 }
			}
		}
	}
}

# The native winner is installed only after the recorded election is handed over.
COLDWAR_ARG_transfer_to_elected_government = {
	if = {
		limit = {
			original_tag = ARG
			IMP_is_1970_scenario = yes
			has_country_flag = COLDWAR_ARG_native_election_pending
			has_country_flag = COLDWAR_ARG_native_government_resolved
			NOT = { has_country_flag = COLDWAR_ARG_elected_handover_completed }
			check_variable = { COLDWAR_ARG_last_election_winner = ruling_party }
			check_variable = { COLDWAR_ARG_last_election_winner > -1 }
			check_variable = { COLDWAR_ARG_last_election_winner < 24 }
			OR = {
				NOT = { check_variable = { COLDWAR_ARG_last_election_winner = 18 } }
				has_country_flag = COLDWAR_ARG_slot18_identity_selected
			}
		}
		set_country_flag = COLDWAR_ARG_elected_handover_completed
		if = {
			limit = {
				check_variable = { ruling_party = 18 }
				has_country_flag = COLDWAR_ARG_slot18_psd_candidate
			}
			COLDWAR_ARG_mark_psd_incumbent = yes
		}
		else_if = { limit = { check_variable = { ruling_party = 18 } } COLDWAR_ARG_mark_cgta_incumbent = yes }
		COLDWAR_ARG_install_elected_incumbent = yes
		COLDWAR_ARG_refresh_politics = yes
		clr_country_flag = COLDWAR_ARG_native_election_pending
	}
}

# The native election chooses the party. These historical officeholders are installed
# only after that recorded winner actually takes office; no focus silently changes a
# national leader.
COLDWAR_ARG_install_elected_incumbent = {
	if = {
		limit = {
			original_tag = ARG
			IMP_is_1970_scenario = yes
			has_country_flag = COLDWAR_ARG_elected_handover_completed
			NOT = { has_country_flag = COLDWAR_ARG_elected_incumbent_installed }
		}
		set_country_flag = COLDWAR_ARG_leader_transition_authorized
		COLDWAR_ARG_select_leader_for_current_party = yes
		set_country_flag = COLDWAR_ARG_elected_incumbent_installed
	}
}
'''
    return body + _leader_selection_effect()


def _triggers() -> str:
    body = '''# IMPERIA COLD WAR — Argentina1970 political integration
COLDWAR_ARG_june_command_crisis_due = {
	original_tag = ARG
	IMP_is_1970_scenario = yes
	check_variable = { ruling_party = 22 }
	COLDWAR_ARG_is_leader_ongania = yes
	date > 1970.6.8
	NOT = { has_country_flag = COLDWAR_ARG_event_commanders_seen }
}
COLDWAR_ARG_lanusse_succession_due = {
	original_tag = ARG
	IMP_is_1970_scenario = yes
	check_variable = { ruling_party = 22 }
	COLDWAR_ARG_is_leader_levingston = yes
	date > 1971.3.25
	NOT = { has_country_flag = COLDWAR_ARG_lanusse_succession_resolved }
}
COLDWAR_ARG_is_leader_ongania = {
	OR = {
		has_country_leader = { name = "Juan Carlos Ongania" ruling_only = yes }
		has_country_leader = { name = "Juan Carlos Ongánía" ruling_only = yes }
	}
}
COLDWAR_ARG_is_leader_levingston = {
	has_country_leader = { name = "Roberto Marcelo Levingston" ruling_only = yes }
}
COLDWAR_ARG_is_leader_lanusse = {
	OR = {
		has_country_leader = { name = "Alejandro Agustín Lanusse" ruling_only = yes }
		has_country_leader = { name = "Alejandro Agustin Lanusse" ruling_only = yes }
	}
}
COLDWAR_ARG_is_leader_peron = {
	OR = {
		has_country_leader = { name = "Juan Perón" ruling_only = yes }
		has_country_leader = { name = "Juan Domingo Perón" ruling_only = yes }
	}
}
COLDWAR_ARG_is_leader_alfonsin = {
	OR = {
		has_country_leader = { name = "Raúl Alfonsín" ruling_only = yes }
		has_country_leader = { name = "Raul Alfonsin" ruling_only = yes }
	}
}
COLDWAR_ARG_is_leader_menem = {
	has_country_leader = { name = "Carlos Menem" ruling_only = yes }
}
COLDWAR_ARG_is_leader_ricardo_balbin = {
	has_country_leader = { name = "Ricardo Balbín" ruling_only = yes }
}
COLDWAR_ARG_is_leader_isabel_peron = {
	OR = {
		has_country_leader = { name = "María Estela Martínez de Perón" ruling_only = yes }
		has_country_leader = { name = "Isabel Perón" ruling_only = yes }
	}
}
COLDWAR_ARG_is_psd_incumbent = {
	custom_trigger_tooltip = {
		tooltip = COLDWAR_ARG_party_18_psd_in_power_tt
		not_tooltip = COLDWAR_ARG_party_18_psd_in_power_tt_NOT
		hidden_trigger = {
			original_tag = ARG
			neutrality_neutral_social_are_in_power = yes
			has_country_flag = COLDWAR_ARG_incumbent_psd
			NOT = { has_country_flag = COLDWAR_ARG_incumbent_cgta }
		}
	}
}
COLDWAR_ARG_is_cgta_incumbent = {
	custom_trigger_tooltip = {
		tooltip = COLDWAR_ARG_party_18_cgta_in_power_tt
		not_tooltip = COLDWAR_ARG_party_18_cgta_in_power_tt_NOT
		hidden_trigger = {
			original_tag = ARG
			neutrality_neutral_social_are_in_power = yes
			has_country_flag = COLDWAR_ARG_incumbent_cgta
			NOT = { has_country_flag = COLDWAR_ARG_incumbent_psd }
		}
	}
}
COLDWAR_ARG_is_party_18_incumbent = {
	original_tag = ARG
	check_variable = { ruling_party = 18 }
	OR = {
		has_country_flag = COLDWAR_ARG_incumbent_psd
		has_country_flag = COLDWAR_ARG_incumbent_cgta
	}
}
COLDWAR_ARG_is_ucede_incumbent = {
	custom_trigger_tooltip = {
		tooltip = COLDWAR_ARG_party_16_ucede_in_power_tt
		not_tooltip = COLDWAR_ARG_party_16_ucede_in_power_tt_NOT
		hidden_trigger = {
			original_tag = ARG
			neutrality_neutral_libertarians_are_in_power = yes
			has_country_flag = COLDWAR_ARG_ucede_formed
		}
	}
}
COLDWAR_ARG_can_run_menem_programme = {
	original_tag = ARG
	IMP_is_1970_scenario = yes
	check_variable = { ruling_party = 13 }
	COLDWAR_ARG_is_leader_menem = yes
	date > 1989.7.7
}
COLDWAR_ARG_can_run_alfonsin_programme = {
	original_tag = ARG
	IMP_is_1970_scenario = yes
	check_variable = { ruling_party = 3 }
	COLDWAR_ARG_is_leader_alfonsin = yes
	date > 1981.9.9
}
COLDWAR_ARG_has_recorded_election_winner = {
	custom_trigger_tooltip = {
		tooltip = COLDWAR_ARG_elected_government_formed_tt
		not_tooltip = COLDWAR_ARG_elected_government_formed_tt_NOT
		hidden_trigger = {
			original_tag = ARG
			has_country_flag = COLDWAR_ARG_native_election_pending
			has_country_flag = COLDWAR_ARG_native_government_resolved
			check_variable = { COLDWAR_ARG_last_election_winner > -1 }
			check_variable = { COLDWAR_ARG_last_election_winner < 24 }
			check_variable = { COLDWAR_ARG_last_election_winner = ruling_party }
			OR = {
				NOT = { check_variable = { COLDWAR_ARG_last_election_winner = 18 } }
				has_country_flag = COLDWAR_ARG_slot18_identity_selected
			}
		}
	}
}
COLDWAR_ARG_slot18_election_choice_ready = {
	original_tag = ARG
	has_country_flag = COLDWAR_ARG_native_election_pending
	has_country_flag = COLDWAR_ARG_native_government_resolved
	has_country_flag = COLDWAR_ARG_slot18_identity_event_pending
	check_variable = { COLDWAR_ARG_last_election_winner > -1 }
	check_variable = { COLDWAR_ARG_last_election_winner < 24 }
	check_variable = { COLDWAR_ARG_last_election_winner = 18 }
	NOT = { has_country_flag = COLDWAR_ARG_slot18_identity_selected }
}
'''
    return body + _leader_triggers()


def _events() -> str:
    return '''# IMPERIA COLD WAR — Argentina1970 political integration
add_namespace = COLDWAR_ARG_politics
country_event = {
	id = COLDWAR_ARG_politics.1
	title = COLDWAR_ARG_politics.1.t
	desc = COLDWAR_ARG_politics.1.d
	picture = GFX_ICW_SA_arg_labor
	is_triggered_only = yes
	trigger = {
		original_tag = ARG
		IMP_is_1970_scenario = yes
		COLDWAR_ARG_slot18_election_choice_ready = yes
		check_variable = { COLDWAR_ARG_last_election_winner = 18 }
	}
	option = {
		name = COLDWAR_ARG_politics.1.a
		ai_chance = { factor = 50 }
		set_country_flag = COLDWAR_ARG_slot18_psd_candidate
		clr_country_flag = COLDWAR_ARG_slot18_cgta_candidate
		set_country_flag = COLDWAR_ARG_slot18_identity_selected
		clr_country_flag = COLDWAR_ARG_slot18_identity_event_pending
	}
	option = {
		name = COLDWAR_ARG_politics.1.b
		ai_chance = { factor = 50 }
		set_country_flag = COLDWAR_ARG_slot18_cgta_candidate
		clr_country_flag = COLDWAR_ARG_slot18_psd_candidate
		set_country_flag = COLDWAR_ARG_slot18_identity_selected
		clr_country_flag = COLDWAR_ARG_slot18_identity_event_pending
	}
}

country_event = {
	id = COLDWAR_ARG_politics.2
	title = COLDWAR_ARG_politics.2.t
	desc = COLDWAR_ARG_politics.2.d
	picture = GFX_ICW_SA_arg_commanders
	is_triggered_only = yes
	trigger = {
		COLDWAR_ARG_lanusse_succession_due = yes
		has_country_flag = COLDWAR_ARG_lanusse_succession_pending
	}
	option = {
		name = COLDWAR_ARG_politics.2.a
		ai_chance = { factor = 80 }
		COLDWAR_ARG_install_lanusse = yes
		clr_country_flag = COLDWAR_ARG_lanusse_succession_pending
	}
	option = {
		name = COLDWAR_ARG_politics.2.b
		ai_chance = { factor = 20 }
		set_country_flag = COLDWAR_ARG_lanusse_succession_resolved
		set_variable = { COLDWAR_ARG_current_junta_leader = 1 }
		clr_country_flag = COLDWAR_ARG_lanusse_succession_pending
	}
}
'''


def _decisions() -> str:
    return ""


def _localisation() -> str:
    rows = [
        "l_english:",
        "# IMPERIA COLD WAR — Argentina 1970 political integration",
        " COLDWAR_ARG_politics_initialized:0 \"Argentine Political Transition\"",
        " COLDWAR_ARG_incumbent_psd:0 \"Democratic Socialist Government\"",
        " COLDWAR_ARG_incumbent_cgta:0 \"CGT of the Argentines Government\"",
        " COLDWAR_ARG_real_election_held:0 \"Constitutional Election Held\"",
        " COLDWAR_ARG_elected_handover_completed:0 \"Elected Government Takes Office\"",
        " COLDWAR_ARG_event_commanders_seen:0 \"Command Crisis Convened\"",
        " COLDWAR_ARG_option_commander_retain:0 \"Back the presidential project\"",
        " COLDWAR_ARG_option_commander_levingston:0 \"Appoint a nationalist-developmental cabinet\"",
        " COLDWAR_ARG_option_commander_lanusse:0 \"Authorize a negotiated opening\"",
        " COLDWAR_ARG_party_18_psd:0 \"Democratic Socialist Party\"",
        " COLDWAR_ARG_party_18_cgta:0 \"CGT of the Argentines\"",
        " COLDWAR_ARG_party_18_psd_in_power_tt:0 \"$COLDWAR_ARG_party_18_psd$ is in power.\"",
        " COLDWAR_ARG_party_18_psd_in_power_tt_NOT:0 \"The $COLDWAR_ARG_party_18_psd$ is not in power.\"",
        " COLDWAR_ARG_party_18_cgta_in_power_tt:0 \"$COLDWAR_ARG_party_18_cgta$ is in power.\"",
        " COLDWAR_ARG_party_18_cgta_in_power_tt_NOT:0 \"The $COLDWAR_ARG_party_18_cgta$ is not in power.\"",
        " COLDWAR_ARG_party_16_ucede_in_power_tt:0 \"$COLDWAR_ARG_party_16_ucede$ is in power.\"",
        " COLDWAR_ARG_party_16_ucede_in_power_tt_NOT:0 \"The $COLDWAR_ARG_party_16_ucede$ is not in power.\"",
        " COLDWAR_ARG_elected_government_formed_tt:0 \"The elected government has completed its formation.\"",
        " COLDWAR_ARG_elected_government_formed_tt_NOT:0 \"The elected government has not completed its formation.\"",
        " COLDWAR_ARG_party_16_ucede:0 \"Union of the Democratic Centre\"",
        " COLDWAR_ARG_politics.1.t:0 \"The Socialist Representation\"",
        " COLDWAR_ARG_politics.1.d:0 \"The ballot has returned the neutral-social list. Its political identity must now be established openly between the Democratic Socialist Party and the CGT of the Argentines.\"",
        " COLDWAR_ARG_politics.1.a:0 \"Register the Democratic Socialist Party\"",
        " COLDWAR_ARG_politics.1.b:0 \"Recognize the CGT of the Argentines\"",
        " COLDWAR_ARG_politics.2.t:0 \"A Change in the Command\"",
        " COLDWAR_ARG_politics.2.d:0 \"The commanders have lost confidence in the Levingston government. They may transfer the presidency to General Alejandro Agustín Lanusse or preserve the developmental cabinet.\"",
        " COLDWAR_ARG_politics.2.a:0 \"Appoint Alejandro Agustín Lanusse\"",
        " COLDWAR_ARG_politics.2.b:0 \"Retain Roberto Marcelo Levingston\"",
    ]
    return "\ufeff" + "\n".join(rows) + "\n"


def build(root, design):
    """Return only this generator's owned outputs; never writes during import/build."""
    if design.get("project") != "IMPERIA COLD WAR" or design.get("feature") != "Argentina 1970-1990":
        raise ValueError("Expected the approved IMPERIA COLD WAR Argentina 1970-1990 design")
    return {
        "common/scripted_effects/COLDWAR_ARG_1970_politics.txt": _effects(),
        "common/scripted_triggers/COLDWAR_ARG_1970_politics.txt": _triggers(),
        "events/COLDWAR_ARG_1970_politics.txt": _events(),
        "localisation/english/COLDWAR_ARG_1970_politics_l_english.yml": _localisation(),
    }
