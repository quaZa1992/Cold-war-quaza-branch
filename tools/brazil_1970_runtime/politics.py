# IMPERIA COLD WAR — Brazil 1970 party identity runtime generator.
"""Build the Brazil political identity layer from frozen runtime templates.

The MD election model still elects among its established 24 outlook slots.
The approved Brazil-specific organizations are registered separately and the
selected organization controls the native party name and leader callback.
This module returns files to the main Brazil builder and never writes shared
MD files itself.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = Path(__file__).resolve().parent / "politics_templates"
APPROVED_SHA256 = "0b14031fbad84b84ad72a1599e47cf444a3b52523bcc26070c8f7fd94bc55875"
CONCEPT = ROOT / "docs/brazil_1970_concept/concept.json"
UNKNOWN_PORTRAIT = "gfx/interface/coldwar_politburo/portrait_unknown.dds"

# Registered identity -> actual political leader used after a native election.
# Portraits are included only for matching assets already in the project.
LEADERS = {
    (1, 1): ("José Sarney", "conservatism", None),
    (1, 2): ("Paulo Salim Maluf", "conservatism", None),
    (1, 3): ("Jorge Bornhausen", "conservatism", "gfx/Leaders/BRA/Jorge_Bornhausen.dds"),
    (2, 1): ("Ulysses Guimarães", "liberalism", None),
    (2, 2): ("Tancredo Neves", "liberalism", None),
    (2, 3): ("Fernando Henrique Cardoso", "liberalism", "gfx/Leaders/BRA/Fernando_Henrique_Cardoso.dds"),
    (3, 1): ("João Goulart", "socialism", None),
    (3, 2): ("Ivete Vargas", "socialism", None),
    (3, 3): ("Leonel Brizola", "socialism", None),
    (3, 4): ("Luiz Inácio Lula da Silva", "socialism", "gfx/Leaders/BRA/luiz_inacio_lula_da_silva.dds"),
    (4, "pcb"): ("Luís Carlos Prestes", "communist_state", None),
    (19, "pcdob"): ("João Amazonas", "Neutral_Communism", None),
    (20, 1): ("Carlos Lacerda", "Nat_Populism", None),
    (20, 2): ("Fernando Collor de Mello", "Nat_Populism", None),
}
LEADER_TIMELINES = {
    (2, 2): [
        ("date < 1985.4.22", "Tancredo Neves", "liberalism", None),
        ("date > 1985.4.21", "Ulysses Guimarães", "liberalism", None),
    ],
    (3, 1): [
        ("date < 1976.12.7", "João Goulart", "socialism", None),
        ("date > 1976.12.6", "Leonel Brizola", "socialism", None),
    ],
    (3, 2): [
        ("date < 1984.1.4", "Ivete Vargas", "socialism", None),
        ("date > 1984.1.3", "Jânio Quadros", "socialism", None),
    ],
    (4, "pcb"): [
        ("date < 1980.1.1", "Luís Carlos Prestes", "communist_state", None),
        ("date > 1979.12.31 date < 1987.6.17", "Giocondo Dias", "communist_state", None),
        ("date > 1987.6.16 date < 1991.6.1", "Salomão Malina", "communist_state", None),
        ("date > 1991.5.31", "Roberto Freire", "communist_state", "gfx/Leaders/BRA/Roberto_Freire.dds"),
    ],
}
REGISTRATION_FLAGS = {
    (1, 1): "COLDWAR_BRA_1970_party_arena_registered",
    (1, 2): "COLDWAR_BRA_1970_party_pds_registered",
    (1, 3): "COLDWAR_BRA_1970_party_pfl_registered",
    (2, 1): "COLDWAR_BRA_1970_party_mdb_registered",
    (2, 2): "COLDWAR_BRA_1970_party_pmdb_registered",
    (2, 3): "COLDWAR_BRA_1970_party_psdb_registered",
    (3, 1): "COLDWAR_BRA_1970_party_historic_ptb_restored",
    (3, 2): "COLDWAR_BRA_1970_party_ptb_late_registered",
    (3, 3): "COLDWAR_BRA_1970_party_pdt_registered",
    (3, 4): "COLDWAR_BRA_1970_party_pt_registered",
    (20, 1): "COLDWAR_BRA_1970_lacerdist_movement_active",
    (20, 2): "COLDWAR_BRA_1970_party_prn_registered",
}


def _leader_effect() -> str:
    rows = [
        "COLDWAR_BRA_1970_install_party_leader = {",
        "\tif = { limit = { original_tag = BRA IMP_is_1970_scenario = yes }",
        "\t\t# Map the numeric MD slot to its native ideology group before appointing this party identity.",
        "\t\t# Suppress the global leader failsafe during the group remap; preserve an existing caller guard.",
        "\t\tif = { limit = { NOT = { has_country_flag = no_leader_change } }",
        "\t\t\tset_country_flag = no_leader_change",
        "\t\t\tupdate_set_politics = yes",
        "\t\t\tclr_country_flag = no_leader_change",
        "\t\t}",
        "\t\telse = { update_set_politics = yes }",
        '\t\tif = { limit = { check_variable = { ruling_party = 22 } date < 1974.3.15 NOT = { has_country_leader = { name = "Emilio Garrastazu Medici" ruling_only = yes } } }',
        '\t\t\tcreate_country_leader = { name = "Emilio Garrastazu Medici" picture = "gfx/Leaders/BRA/BRA_Coldwar_Emilio_Garrastazu_Medici.dds" ideology = Nat_Autocracy traits = { } }',
        "\t\t\tset_correct_ideology_trait = yes",
        "\t\t}",
        '\t\tif = { limit = { check_variable = { ruling_party = 22 } date > 1974.3.14 date < 1979.3.15 NOT = { has_country_leader = { name = "Ernesto Geisel" ruling_only = yes } } }',
        '\t\t\tcreate_country_leader = { name = "Ernesto Geisel" picture = "'+UNKNOWN_PORTRAIT+'" ideology = Nat_Autocracy traits = { } }',
        "\t\t\tset_correct_ideology_trait = yes",
        "\t\t}",
        '\t\tif = { limit = { check_variable = { ruling_party = 22 } date > 1979.3.14 NOT = { has_country_leader = { name = "João Figueiredo" ruling_only = yes } } }',
        '\t\t\tcreate_country_leader = { name = "João Figueiredo" picture = "gfx/leaders/mdcw_historical_pool/BRA_joao_figueiredo.dds" ideology = Nat_Autocracy traits = { } }',
        "\t\t\tset_correct_ideology_trait = yes",
        "\t\t}",
    ]
    for (slot, identity), base_person in LEADERS.items():
        versions = LEADER_TIMELINES.get((slot, identity), [(None, *base_person)])
        for date_guard, name, ideology, picture in versions:
            guard = []
            if date_guard:
                guard.extend(date_guard.split())
            if isinstance(identity, int):
                registration_flag = REGISTRATION_FLAGS[(slot, identity)]
                guard.extend([f"check_variable = {{ ruling_party = {slot} }}",
                              f"check_variable = {{ COLDWAR_BRA_1970_party_identity_{slot} = {identity} }}",
                              f"has_country_flag = {registration_flag}"])
            else:
                guard.extend([f"check_variable = {{ ruling_party = {slot} }}",
                              "OR = {",
                              f"\thas_country_flag = COLDWAR_BRA_1970_party_{identity}_legalized",
                              f"\thas_country_flag = COLDWAR_BRA_1970_{identity}_alternative_accession",
                              "}"])
            if name == "Carlos Lacerda":
                guard.extend(["has_country_flag = COLDWAR_BRA_1970_party_reform_open", "date < 1977.5.22"])
            if name == "Sandra Cavalcanti":
                guard.append("has_country_flag = COLDWAR_BRA_1970_lacerdist_successor_authorized")
            if name == "Fernando Collor de Mello":
                guard.extend(["has_country_flag = COLDWAR_BRA_1970_prn_leader_available",
                              "has_country_flag = COLDWAR_BRA_1970_party_prn_registered"])
            guard.append(f'NOT = {{ has_country_leader = {{ name = "{name}" ruling_only = yes }} }}')
            rows += ["\t\tif = { limit = { " + " ".join(guard) + " }",
                     "\t\t\tcreate_country_leader = {",
                     f'\t\t\t\tname = "{name}"',
                     f"\t\t\t\tideology = {ideology}"]
            rows.append(f'\t\t\t\tpicture = "{picture or UNKNOWN_PORTRAIT}"')
            rows += ["\t\t\t\ttraits = { }", "\t\t\t}",
                     "\t\t\tset_correct_ideology_trait = yes", "\t\t}"]
    rows += [
        '\t\tif = { limit = { check_variable = { ruling_party = 20 } check_variable = { COLDWAR_BRA_1970_party_identity_20 = 1 } has_country_flag = COLDWAR_BRA_1970_lacerdist_successor_authorized date > 1977.5.21 NOT = { has_country_leader = { name = "Sandra Cavalcanti" ruling_only = yes } } }',
        '\t\t\tcreate_country_leader = { name = "Sandra Cavalcanti" picture = "'+UNKNOWN_PORTRAIT+'" ideology = Nat_Populism traits = { } }',
        "\t\t\tset_correct_ideology_trait = yes", "\t\t}",
        '\t\tif = { limit = { has_dlc = "Trial of Allegiance" has_country_leader = { name = "Luís Carlos Prestes" ruling_only = yes } }',
        '\t\t\tset_country_leader_portrait = { portrait = GFX_portrait_BRA_luis_carlos_prestes }',
        '\t\t}',
    ]
    rows += ["\t}", "}"]
    return "\n".join(rows)


def _route_trigger() -> str:
    rows = [
        "COLDWAR_BRA_1970_party_leader_route_supported = {",
        "\toriginal_tag = BRA",
        "\tIMP_is_1970_scenario = yes",
        "\tOR = {",
        "\t\tcheck_variable = { ruling_party = 22 }",
    ]
    for (slot, identity), (name, _, _) in LEADERS.items():
        if isinstance(identity, int):
            registered = REGISTRATION_FLAGS[(slot, identity)]
            guard = [f"check_variable = {{ ruling_party = {slot} }}",
                     f"check_variable = {{ COLDWAR_BRA_1970_party_identity_{slot} = {identity} }}",
                     f"has_country_flag = {registered}"]
            if name == "Carlos Lacerda":
                guard += ["has_country_flag = COLDWAR_BRA_1970_party_reform_open", "date < 1977.5.22"]
            if name == "Sandra Cavalcanti":
                guard += ["has_country_flag = COLDWAR_BRA_1970_lacerdist_successor_authorized"]
            if name == "Fernando Collor de Mello":
                guard += ["has_country_flag = COLDWAR_BRA_1970_prn_leader_available",
                          "has_country_flag = COLDWAR_BRA_1970_party_prn_registered"]
        else:
            suffix = "pcb" if identity == "pcb" else "pcdob"
            guard = [f"check_variable = {{ ruling_party = {slot} }}",
                     f"OR = {{ has_country_flag = COLDWAR_BRA_1970_party_{suffix}_legalized has_country_flag = COLDWAR_BRA_1970_{suffix}_alternative_accession }}"]
        if name == "Carlos Lacerda":
            rows.append("\t\tAND = { " + " ".join(guard) + " }")
        else:
            rows.append("\t\tAND = { " + " ".join(guard) + " }")
    rows.append('\t\tAND = { check_variable = { ruling_party = 20 } check_variable = { COLDWAR_BRA_1970_party_identity_20 = 1 } has_country_flag = COLDWAR_BRA_1970_lacerdist_successor_authorized date > 1977.5.21 }')
    rows += ["\t}", "}"]
    return "\n".join(rows)


def _initial_nomination_effects() -> str:
    entries = [
        (1, 1, "arena", "COLDWAR_BRA_1970_party_arena_registered"),
        (2, 1, "mdb", "COLDWAR_BRA_1970_party_mdb_registered"),
        (20, 1, "lacerdist", "COLDWAR_BRA_1970_lacerdist_movement_active"),
    ]
    blocks = []
    for slot, identity, key, registered in entries:
        blocks.append("\n".join([
            f"COLDWAR_BRA_1970_nominate_{key} = {{",
            "\tif = {",
            f"\t\tlimit = {{ original_tag = BRA IMP_is_1970_scenario = yes has_country_flag = COLDWAR_BRA_1970_party_reform_open has_country_flag = {registered} }}",
            f"\t\tset_variable = {{ COLDWAR_BRA_1970_party_identity_{slot} = {identity} }}",
            "\t\tupdate_party_name = yes",
            "\t}",
            "}",
        ]))
    return "\n\n".join(blocks)


def _parse_localisation(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8-sig")
    loc: dict[str, str] = {}
    for line in text.splitlines()[2:]:
        match = re.match(r'^\s*([^:]+):0 "(.*)"\s*$', line)
        if match:
            value = match.group(2).replace("\\n", "\n").replace('\\"', '"').replace("\\\\", "\\")
            loc[match.group(1)] = value
    return loc


def get_build_politics(design: dict) -> dict:
    """Return generated path contents, localisation and shared splice hooks."""
    if hashlib.sha256(CONCEPT.read_bytes()).hexdigest() != APPROVED_SHA256:
        raise RuntimeError("Approved Brazil 1970 political design hash changed")
    group_ids = {g["id"] for g in design.get("groups", [])}
    required = {"military", "arena", "mdb", "ptb", "pdt", "pt", "pfl", "psdb", "pcb", "pcdob", "populist", "prn", "ptb_late"}
    if not required.issubset(group_ids):
        raise ValueError(f"Brazil political template groups missing: {sorted(required - group_ids)}")

    effects = (TEMPLATES / "effects.txt").read_text(encoding="utf-8")
    effects = re.sub(
        r"# Call when a posthumous political opening permits the Lacerdist movement to continue\.\nCOLDWAR_BRA_1970_mark_lacerdist_successor = \{.*?\n\}\n\nCOLDWAR_BRA_1970_mark_prn_leader_available = \{.*?\n\}",
        """# Record authorization; only the native callback creates Sandra after she actually governs.
COLDWAR_BRA_1970_mark_lacerdist_successor = {
\tif = { limit = { original_tag = BRA IMP_is_1970_scenario = yes has_country_flag = COLDWAR_BRA_1970_party_reform_open date > 1977.5.21 has_country_flag = COLDWAR_BRA_1970_lacerdist_movement_active NOT = { has_country_flag = COLDWAR_BRA_1970_lacerdist_successor_authorized } }
\t\tset_country_flag = COLDWAR_BRA_1970_lacerdist_successor_authorized
\t\tif = { limit = { check_variable = { ruling_party = 20 } check_variable = { COLDWAR_BRA_1970_party_identity_20 = 1 } } set_leader = yes }
\t}
}

COLDWAR_BRA_1970_mark_prn_leader_available = {
\tif = { limit = { original_tag = BRA IMP_is_1970_scenario = yes has_country_flag = COLDWAR_BRA_1970_party_reform_open has_country_flag = COLDWAR_BRA_1970_prn_formation_open date > 1988.12.31 NOT = { has_country_flag = COLDWAR_BRA_1970_prn_leader_available } }
\t\tset_country_flag = COLDWAR_BRA_1970_prn_leader_available
\t}
}""",
        effects, flags=re.S)
    effects = effects.replace("\t\tCOLDWAR_BRA_init_politics = yes\n", "\t\tCOLDWAR_BRA_init_politics = yes\n\t\tCOLDWAR_BRA_1970_mark_prn_leader_available = yes\n", 1)
    if "COLDWAR_BRA_1970_install_party_leader = {" not in effects:
        effects = effects.rstrip() + "\n\n" + _leader_effect() + "\n"
    if "COLDWAR_BRA_1970_nominate_arena = {" not in effects:
        marker = "COLDWAR_BRA_1970_install_party_leader = {"
        effects = effects.replace(marker, _initial_nomination_effects() + "\n\n" + marker, 1)
    if "COLDWAR_BRA_1970_open_party_system =" not in effects:
        marker = "COLDWAR_BRA_1970_reconcile_politics = {"
        effects = effects.replace(marker, "COLDWAR_BRA_1970_open_party_system = { COLDWAR_BRA_1970_open_party_reform = yes }\n\n" + marker, 1)
    if "COLDWAR_BRA_reconcile_politics =" not in effects:
        marker = "COLDWAR_BRA_1970_monthly_politics_reconcile ="
        effects = effects.replace(marker, "COLDWAR_BRA_reconcile_politics = { COLDWAR_BRA_1970_reconcile_politics = yes }\n" + marker, 1)

    triggers = (TEMPLATES / "triggers.txt").read_text(encoding="utf-8")
    triggers = triggers.replace("COLDWAR_BRA_1970_lacerdist_successor_installed", "COLDWAR_BRA_1970_lacerdist_successor_authorized")
    if "COLDWAR_BRA_1970_party_leader_route_supported = {" not in triggers:
        triggers = triggers.rstrip() + "\n\n" + _route_trigger() + "\n"
    files = {
        "common/scripted_effects/COLDWAR_BRA_1970_politics.txt": effects,
        "common/scripted_triggers/COLDWAR_BRA_1970_politics.txt": triggers,
        "common/decisions/categories/COLDWAR_BRA_1970_politics_categories.txt": (TEMPLATES / "categories.txt").read_text(encoding="utf-8"),
        "common/decisions/COLDWAR_BRA_1970_politics.txt": (TEMPLATES / "decisions.txt").read_text(encoding="utf-8"),
        "common/scripted_localisation/COLDWAR_BRA_1970_politics.txt": (TEMPLATES / "scripted_localisation.txt").read_text(encoding="utf-8"),
    }
    # The main builder merges this localised key map into its BOM-prefixed YAML.
    loc = _parse_localisation(TEMPLATES / "localisation.yml")
    integrations = {
        "leader_callback": {
            "shared_file": "common/scripted_effects/BRA_political_leaders.txt",
            "scripted_effect": "set_leader_BRA",
            "call": "COLDWAR_BRA_1970_install_party_leader = yes",
            "position": "before the generic and Chile leader branches, with an early if/else_if guard",
            "supported_trigger": "COLDWAR_BRA_1970_party_leader_route_supported = yes",
            "guards_inside_helper": "original_tag = BRA and IMP_is_1970_scenario = yes",
        },
        "event_effects": [
            "COLDWAR_BRA_init_politics = yes",
            "COLDWAR_BRA_1970_open_party_reform = yes",
            "COLDWAR_BRA_reconcile_politics = yes",
        ],
        "party_registry": {
            "native_party_slots_changed": False,
            "identity_variables": {
                "1": {"1": "ARENA", "2": "PDS", "3": "PFL"},
                "2": {"1": "MDB", "2": "PMDB", "3": "PSDB"},
                "3": {"1": "historic PTB alternate", "2": "registered PTB successor", "3": "PDT", "4": "PT"},
                "4": {"pcb": "PCB"},
                "19": {"pcdob": "PCdoB"},
                "20": {"1": "Lacerdist movement", "2": "PRN"},
                "22": {"native": "Armed Forces, including Medici / Geisel / Figueiredo succession"},
            },
            "party_name_callbacks": [
                "COLDWAR_BRA_1970_party_slot_1",
                "COLDWAR_BRA_1970_party_slot_2",
                "COLDWAR_BRA_1970_party_slot_3",
                "COLDWAR_BRA_1970_party_slot_20",
            ],
            "registration_and_selection": "Each registered identity has a native decision and a native congress nomination decision. Nomination sets the corresponding approved identity variable and calls update_party_name; it does not change ruling_party.",
            "political_event_hooks": [
                "Party reform event: COLDWAR_BRA_1970_open_party_reform = yes",
                "PDS / PMDB split choice: set the corresponding *_split_authorized flag before the existing formation decisions.",
                "Labourist restoration, reorganization, and communist legalization choices: set their existing *_open flags before the corresponding formation decisions.",
                "Late PRN opening: set COLDWAR_BRA_1970_prn_formation_open; weekly reconcile registers Collor's candidacy flag after 1988 without creating a leader.",
            ],
        },
        "decision_categories": ["COLDWAR_BRA_1970_party_organization"],
        "leader_succession": {
            "never_kill_country_leader": True,
            "lacerdist_authorization_decision": "COLDWAR_BRA_1970_authorize_lacerdist_continuity",
            "prn_candidate_registration": "COLDWAR_BRA_1970_mark_prn_leader_available only sets a candidacy flag; Collor is created by the native leader callback only after PRN identity 20/2 governs.",
            "install_guard": "Only creates a matching candidate when its actual registered identity is currently ruling and the named candidate is not already the ruling leader.",
        },
            "historical_sources": [
            {"url": "https://cpdoc.fgv.br/sites/default/files/brasilia/trabalhos/MarlyMotta_CarlosLacerda.pdf",
             "finding": "FGV's study identifies Sandra Cavalcanti as personally linked to Lacerda and among the politicians most closely associated with Lacerdismo; it does not claim formal succession."},
            {"url": "https://repositorio.fgv.br/bitstreams/fd40702d-dcf7-479b-be0e-09756343ffb9/download",
             "finding": "FGV's research records Cavalcanti's later political activity, Arena affiliation and subsequent attempts to organize her own party."},
            {"url": "https://presidentes.an.gov.br/index.php/centro-de-referencia-de-acervos-presidenciais/assuntos/biografias/183-ernesto-geisel",
             "finding": "Brazil's National Archives records Geisel's 15 March 1974 to March 1979 presidential term."},
            {"url": "https://atlas.fgv.br/verbete/5807",
             "finding": "FGV Atlas records Figueiredo's 15 March 1979 inauguration and succession from Geisel."},
            {"url": "https://cpdoc.fgv.br/biografias/golpe-1964",
             "finding": "FGV CPDOC records Goulart's death in 1976; the restored historic PTB route moves to living labour leader Leonel Brizola."},
            {"url": "https://cpdoc.fgv.br/biografias/janio-quadros",
             "finding": "FGV CPDOC records Jânio Quadros joining the PTB in 1980 and standing as its São Paulo gubernatorial candidate in 1981."},
            {"url": "https://cpdoc.fgv.br/biografias/tancredo-neves",
             "finding": "FGV CPDOC records Tancredo Neves's death in April 1985; the PMDB timeline continues with Ulysses Guimarães."},
            {"url": "https://cpdoc.fgv.br/biografias/luis-carlos-prestes",
             "finding": "FGV CPDOC records Giocondo Dias succeeding Prestes as PCB secretary-general and Prestes leaving the party."},
            {"url": "https://atlas.fgv.br/verbete/6069",
             "finding": "FGV Atlas records Salomão Malina as PCB president and Roberto Freire as vice-president at the 1987 congress."},
            {"url": "https://pcb.org.br/portal2/24421",
             "finding": "The PCB's own history records Giocondo Dias as secretary-general from 1980 to 1987, Salomão Malina as leader from 1987 to 1991, and Roberto Freire taking the party direction in 1991."},
        ],
    }
    return {
        "files": files,
        "loc": loc,
        "categories": ["COLDWAR_BRA_1970_party_organization"],
        "integrations": integrations,
    }


def main() -> None:
    """Standalone regeneration from the frozen template package."""
    import json
    design = json.loads((ROOT / "docs/brazil_1970_concept/concept.json").read_text(encoding="utf-8"))
    result = get_build_politics(design)
    for rel, body in result["files"].items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8", newline="\n")
    loc_path = ROOT / "localisation/english/COLDWAR_BRA_1970_politics_l_english.yml"
    loc_rows = ["l_english:", " # IMPERIA COLD WAR — Brazil 1970 party identity localisation."]
    loc_rows.extend(f' {key}:0 "{value.replace(chr(10), chr(92) + "n")}"' for key, value in result["loc"].items())
    loc_path.write_text("\n".join(loc_rows) + "\n", encoding="utf-8-sig", newline="\n")


if __name__ == "__main__":
    main()
