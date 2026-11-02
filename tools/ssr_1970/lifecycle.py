# IMPERIA COLD WAR — Universal SSR lifecycle generator.
"""Emit status, party, spirit, transition, programme and specialisation lifecycle."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shared
import art

PREFIX = "COLDWAR_SSR_lifecycle_"
TAGS = shared.TAGS
PARTY = shared.data()["party_triggers"]

PREP = {
    "broken_supply": ("COLDWAR_SSR_diversify_orders_rewarded", "COLDWAR_SSR_{}_regional_diversify_rewarded"),
    "state_accounts": ("COLDWAR_SSR_civil_registers_rewarded",),
    "command_gap": ("COLDWAR_SSR_defence_records_rewarded",),
}
REPAIRS = {
    "broken_supply": (("COLDWAR_SSR_payment_register_rewarded",), ("COLDWAR_SSR_supplier_contracts_rewarded",), ("COLDWAR_SSR_industrial_conversion_rewarded",)),
    "state_accounts": (("COLDWAR_SSR_revenue_service_rewarded",), ("COLDWAR_SSR_registered_accounts_rewarded",), ("COLDWAR_SSR_budget_protection_rewarded", "COLDWAR_SSR_budget_consolidation_rewarded")),
    "command_gap": (("COLDWAR_SSR_defence_authority_rewarded",), ("COLDWAR_SSR_maintenance_command_rewarded",), ("COLDWAR_SSR_defence_settlement_rewarded",)),
}


def _var(group, key):
    return PREFIX + shared.slug(group) + "_" + key


def _mods(modifiers, indent="\t\t\t"):
    return "\n".join(f"{indent}{key} = {shared.number(value)}" for key, value in sorted(modifiers.items()))


def _idea(idea_id, name, description, modifiers=None, gear=None, picture="industrial_concern"):
    modifiers = modifiers or {}
    picture = art.picture_for_idea(idea_id)
    out = [f"\t\t{idea_id} = {{", f"\t\t\tpicture = {picture}", "\t\t\tallowed = { always = no }", "\t\t\tallowed_civil_war = { always = yes }"]
    if modifiers:
        out += ["\t\t\tmodifier = {", _mods(modifiers), "\t\t\t}"]
    if gear:
        out.append("\t\t\tequipment_bonus = {")
        for target, values in sorted(gear.items()):
            out.append(f"\t\t\t\t{target} = {{")
            for key, value in sorted(values.items()):
                if key == "instant":
                    continue
                out.append(f"\t\t\t\t\t{key} = {shared.number(value)}")
            out.append("\t\t\t\t\tinstant = yes")
            out.append("\t\t\t\t}")
        out.append("\t\t\t}")
    out.append("\t\t}")
    return "\n".join(out)


def _reachable_spec_states(spec_nodes):
    """Enumerate receipt sets closed under prerequisites and exclusive choices."""
    ordered = sorted(spec_nodes, key=lambda n: (n["y"], n["x"], n["key"]))
    states = {frozenset()}
    for node in ordered:
        next_states = set(states)
        for state in states:
            prereqs = node["prerequisites"]
            if any(not any(item in state for item in group) for group in prereqs):
                continue
            if any(item in state for item in node["exclusive"]):
                continue
            next_states.add(state | {node["id"]})
        states = next_states
    return sorted(states, key=lambda s: (len(s), tuple(sorted(s))))


def _equipment(node, legacy=False):
    field = "legacy_equipment_bonuses" if legacy else "equipment_bonuses"
    entries = node.get(field) or []
    out = {}
    for entry in entries:
        target = entry["target"]
        out.setdefault(target, {})
        for key, value in entry["modifiers"].items():
            out[target][key] = round(out[target].get(key, 0) + value, 5)
    return out


def _combine_gear(nodes, legacy=False):
    out = {}
    for node in nodes:
        for target, values in _equipment(node, legacy).items():
            out.setdefault(target, {})
            for key, value in values.items():
                out[target][key] = round(out[target].get(key, 0) + value, 5)
    return {target: values for target, values in out.items() if values}


def specialisation_catalog(models=None):
    """Return each reachable combined idea, its receipt gate, and full/legacy effects."""
    models = models or shared.models()
    result = {}
    for role in ("aircraft", "armour", "artillery", "army", "navy", "agriculture", "industry", "resources", "electronics"):
        spec_nodes = [n for n in models["UKR"]["nodes"] if n.get("specialisation") == role]
        root = next(n for n in spec_nodes if n["key"].endswith("_mandate"))
        variants = []
        for index, state in enumerate(_reachable_spec_states(spec_nodes)):
            included = [n for n in spec_nodes if n["id"] in state]
            full_mods, legacy_mods = {}, {}
            for node in included:
                for key, value in node["modifiers"].items():
                    full_mods[key] = round(full_mods.get(key, 0) + value, 5)
                for key, value in node.get("legacy_modifiers", {}).items():
                    legacy_mods[key] = round(legacy_mods.get(key, 0) + value, 5)
            variants.append({
                "index": index,
                "receipts": sorted(state),
                "full_idea": f"{PREFIX}special_{role}_full_{index}",
                "legacy_idea": f"{PREFIX}special_{role}_legacy_{index}",
                "full_name": root["spirit"],
                "legacy_name": root["legacy_spirit"],
                "full_modifiers": full_mods,
                "legacy_modifiers": legacy_mods,
                "full_equipment": _combine_gear(included),
                "legacy_equipment": _combine_gear(included, True),
            })
        result[role] = variants
    return result


def _special_ideas(models, loc):
    out = []
    for role in ("aircraft", "armour", "artillery", "army", "navy", "agriculture", "industry", "resources", "electronics"):
        spec_nodes = [n for n in models["UKR"]["nodes"] if n.get("specialisation") == role]
        root = next(n for n in spec_nodes if n["key"].endswith("_mandate"))
        for i, state in enumerate(_reachable_spec_states(spec_nodes)):
            included = [n for n in spec_nodes if n["id"] in state]
            mods_full, mods_legacy = {}, {}
            for n in included:
                for key, value in n["modifiers"].items():
                    mods_full[key] = round(mods_full.get(key, 0) + value, 5)
                for key, value in n.get("legacy_modifiers", {}).items():
                    mods_legacy[key] = round(mods_legacy.get(key, 0) + value, 5)
            full_gear = _combine_gear(included)
            legacy_gear = _combine_gear(included, True)
            full_id = f"{PREFIX}special_{role}_full_{i}"
            legacy_id = f"{PREFIX}special_{role}_legacy_{i}"
            loc[full_id] = root["spirit"]
            loc[legacy_id] = root["legacy_spirit"]
            picture = {"aircraft":"air_research", "armour":"army_tank_good", "artillery":"army_artillery_good", "army":"army_war_college", "navy":"coastal_navy", "agriculture":"agriculture", "industry":"industrial_concern", "resources":"industrial_concern", "electronics":"research_bonus"}[role]
            legacy_description = "The republic retains its national design, production and training institutions after separation. The remaining programme costs reflect the loss of common Union orders and supply arrangements."
            out.extend([_idea(full_id, loc[full_id], root["description"], mods_full, full_gear, picture),
                        _idea(legacy_id, loc[legacy_id], legacy_description, mods_legacy, legacy_gear, picture)])
    return out


def _transition_data(model, tag):
    abrupt = {item["id"]: item for item in model["initial_transition"]["abrupt"]}
    return abrupt


def _transition_values(model, tag, liability, prep_count, repair_count, negotiated):
    base = _transition_data(model, tag)[liability]["modifiers"]
    prep_factor = max(0, 1 - 0.25 * prep_count)
    repair_factor = max(0, (3 - repair_count) / 3)
    agreement_factor = 0.6 if negotiated else 1
    return {key: round(value * prep_factor * repair_factor * agreement_factor, 5)
            for key, value in base.items()}


def _repair_conditions(groups, count):
    from itertools import combinations
    out = []
    for selected_indices in combinations(range(len(groups)), count):
        selected = [groups[index] for index in selected_indices]
        unselected = [group for index, group in enumerate(groups) if index not in selected_indices]
        body = " ".join("OR = { " + " ".join(f"has_country_flag = {r}" for r in group) + " }" for group in selected)
        body += (" " if body else "") + " ".join("NOT = { OR = { " + " ".join(f"has_country_flag = {r}" for r in group) + " } }" for group in unselected)
        out.append(body)
    return out


def _next_repair_delta(model, tag, liability, prep_count, repair_count, negotiated):
    current = _transition_values(model, tag, liability, prep_count, repair_count, negotiated)
    following = _transition_values(model, tag, liability, prep_count, min(3, repair_count + 1), negotiated)
    return {key: round(following[key] - current[key], 5) for key in current}


def generate():
    models = shared.models()
    source = shared.data()
    nodes = shared.nodes()
    loc = {}
    ideas = ["ideas = {", "\tcountry = {"]
    effects = []
    triggers = []
    dynamic = []

    # Status predicates preserve historical identity across sovereignty changes.
    original_ssr = " ".join(f"{tag} = {{ has_country_flag = {PREFIX}scenario_identity COLDWAR_SOV_is_union_republic = yes }}" for tag in TAGS)
    triggers.append(f"""COLDWAR_SSR_is_participant = {{
\tAND = {{ IMP_is_1970_scenario = yes OR = {{ {' '.join(f'AND = {{ original_tag = {tag} has_country_flag = {PREFIX}scenario_identity }}' for tag in TAGS)} has_country_flag = {PREFIX}accepted_admission }} }}
}}
COLDWAR_SSR_is_ssr = {{
\tAND = {{ IMP_is_1970_scenario = yes OR = {{ AND = {{ original_tag = UKR has_country_flag = {PREFIX}scenario_identity is_subject_of = SOV }} AND = {{ original_tag = BLR has_country_flag = {PREFIX}scenario_identity is_subject_of = SOV }} AND = {{ original_tag = MLV has_country_flag = {PREFIX}scenario_identity is_subject_of = SOV }} AND = {{ original_tag = EST has_country_flag = {PREFIX}scenario_identity is_subject_of = SOV }} AND = {{ original_tag = LAT has_country_flag = {PREFIX}scenario_identity is_subject_of = SOV }} AND = {{ original_tag = LIT has_country_flag = {PREFIX}scenario_identity is_subject_of = SOV }} AND = {{ original_tag = GEO has_country_flag = {PREFIX}scenario_identity is_subject_of = SOV }} AND = {{ original_tag = ARM has_country_flag = {PREFIX}scenario_identity is_subject_of = SOV }} AND = {{ original_tag = AZE has_country_flag = {PREFIX}scenario_identity is_subject_of = SOV }} AND = {{ original_tag = KAZ has_country_flag = {PREFIX}scenario_identity is_subject_of = SOV }} AND = {{ original_tag = UZB has_country_flag = {PREFIX}scenario_identity is_subject_of = SOV }} AND = {{ original_tag = TRK has_country_flag = {PREFIX}scenario_identity is_subject_of = SOV }} AND = {{ original_tag = KYR has_country_flag = {PREFIX}scenario_identity is_subject_of = SOV }} AND = {{ original_tag = TAJ has_country_flag = {PREFIX}scenario_identity is_subject_of = SOV }} AND = {{ has_country_flag = {PREFIX}accepted_admission is_subject_of = SOV }} }} }}
}}
COLDWAR_SSR_is_independent = {{
\tAND = {{ IMP_is_1970_scenario = yes COLDWAR_SSR_is_participant = yes has_country_flag = {PREFIX}transition_recorded is_subject = no has_capitulated = no }}
}}""")

    # Dynamic modifier definitions for ordinary focus receipt groups.
    groups = {}
    for node in nodes:
        if node.get("specialisation") or node.get("replace") or node["phase"] == "party" and node["group_key"].startswith("spec_"):
            continue
        groups.setdefault(node["group_key"], {})
        for key in node["modifiers"]:
            groups[node["group_key"]][key] = _var(node["group_key"], key)
    for group, modifiers in groups.items():
        dyn_id = PREFIX + "group_" + shared.slug(group)
        picture = art.icon_for_idea(dyn_id)
        dynamic.append(f"{dyn_id} = {{\n\ticon = {picture}\n" + "\n".join(f"\t{key} = {variable}" for key, variable in sorted(modifiers.items())) + "\n}")
        loc[dyn_id] = group.replace("_", " ").title()

    # Transition liability dynamic modifiers, with frozen prep and live repairs.
    transition_mod_keys = sorted({key for model in models.values() for item in model["initial_transition"]["abrupt"] for key in item["modifiers"]})
    for liability in ("broken_supply", "state_accounts", "command_gap"):
        dyn_id = PREFIX + "transition_" + liability
        picture = art.icon_for_idea(dyn_id)
        dynamic.append(f"{dyn_id} = {{\n\ticon = {picture}\n" + "\n".join(f"\t{key} = {PREFIX}transition_{liability}_{key}" for key in transition_mod_keys if any(key in item["modifiers"] for item in models["UKR"]["initial_transition"]["abrupt"] if item["id"] == liability)) + "\n}")
        loc[dyn_id] = {"broken_supply":"Fractured Supply Chains","state_accounts":"Unsettled State Accounts","command_gap":"Unsettled Defence Administration"}[liability]

    # Starting and reformed spirits are country-specific because regional and initial values differ.
    start_rules = {
        "plan": ("Plan Targets and Shortages", {"production_factory_max_efficiency_factor": -0.1, "civilian_factories_productivity": -0.1}),
        "plan_revised": ("Revised Plan Targets", {"production_factory_max_efficiency_factor": -0.05, "civilian_factories_productivity": -0.05}),
        "plan_republican": ("Republican Production Standards", {"civilian_factories_productivity": 0.03}),
        "patronage": ("Republican Patronage Networks", {"political_power_factor": -0.1, "bureaucracy_cost_multiplier_modifier": 0.08}),
        "professional": ("Professional Appointments", {"bureaucracy_cost_multiplier_modifier": -0.03, "research_speed_factor": 0.03}),
        "discipline": ("Cadre Discipline", {"political_power_factor": 0.08, "stability_factor": -0.04}),
        "social": ("Soviet Social Guarantees", {"stability_factor": 0.08, "social_cost_multiplier_modifier": 0.1}),
        "social_republican": ("Republican Social Guarantees", {"stability_factor": 0.08, "social_cost_multiplier_modifier": 0.06}),
        "technical": ("Union Technical Network", {"research_speed_factor": 0.05, "supply_consumption_factor": -0.05}),
    }
    for tag, model in models.items():
        exposure_id = f"{PREFIX}{tag}_unconverted_orders"
        loc[exposure_id] = "Unconverted Union Orders"
        ideas.append(_idea(exposure_id, loc[exposure_id], "Union supply commitments remain unresolved until domestic suppliers or export conversion replace them.", {"tax_gain_multiplier_modifier": -0.04, "civilian_factories_productivity": -0.05}, picture="industrial_concern"))
        for key, (name, mods) in start_rules.items():
            if key == "plan_revised": mods = {"production_factory_max_efficiency_factor": -0.05, "civilian_factories_productivity": -0.05}
            idea_id = f"{PREFIX}{tag}_{key}"
            loc[idea_id] = name
            picture = "industrial_concern" if key.startswith("plan") else "political_reform" if key in {"patronage", "professional", "discipline"} else "research_bonus" if key == "technical" else "agriculture"
            ideas.append(_idea(idea_id, name, name + ".", mods, picture=picture))
        regional = model["profile"]["regional"]
        regional_node = next(n for n in model["nodes"] if n["key"] == "regional_standards")
        aftercare_node = next(n for n in model["nodes"] if n.get("regional_aftercare"))
        variants = (
            ("original", regional["name"], regional["modifiers"], regional["description"]),
            ("managed", regional_node["spirit"], regional_node["modifiers"], regional_node["description"]),
            ("aftercare", aftercare_node["regional_aftercare"]["new"], aftercare_node["regional_aftercare"]["modifiers"], aftercare_node["description"]),
        )
        for variant, name, values, description in variants:
            mods = dict(values)
            idea_id = f"{PREFIX}{tag}_regional_{variant}"
            loc[idea_id] = name
            picture = "agriculture" if "Agricultural" in regional["name"] else "industrial_concern" if any(w in regional["name"] for w in ("Industrial", "Energy", "Mining", "Resource")) else "research_bonus"
            ideas.append(_idea(idea_id, name, description, mods, picture=picture))

    # Dynamic programme modifiers and static specialisation stages.
    special_defs = _special_ideas(models, loc)
    ideas.extend(special_defs)

    # Transition idea names are attached to dynamic modifiers through add_dynamic_modifier.
    ideas.append("\t}")
    ideas.append("}")

    # A static idea exchange effect for starting reforms and specialisation receipt combinations.
    for tag, model in models.items():
        regional = model["profile"]["regional"]
        regional_node = next(n for n in model["nodes"] if n["key"] == "regional_standards")
        effects.append(f"""{PREFIX}starting_{tag} = {{
\tremove_ideas = {PREFIX}{tag}_plan
\tremove_ideas = {PREFIX}{tag}_plan_revised
\tremove_ideas = {PREFIX}{tag}_plan_republican
\tif = {{ limit = {{ has_country_flag = COLDWAR_SSR_plan_settlement_rewarded }} add_ideas = {PREFIX}{tag}_plan_republican }}
\telse_if = {{ limit = {{ has_country_flag = COLDWAR_SSR_industrial_conversion_rewarded }} }}
\telse_if = {{ limit = {{ has_country_flag = COLDWAR_SSR_enterprise_accounts_rewarded }} add_ideas = {PREFIX}{tag}_plan_revised }}
\telse = {{ add_ideas = {PREFIX}{tag}_plan }}
\tremove_ideas = {PREFIX}{tag}_patronage
\tremove_ideas = {PREFIX}{tag}_professional
\tremove_ideas = {PREFIX}{tag}_discipline
\tif = {{ limit = {{ has_country_flag = COLDWAR_SSR_audit_staff_rewarded }} add_ideas = {PREFIX}{tag}_professional }}
\telse_if = {{ limit = {{ has_country_flag = COLDWAR_SSR_discipline_campaign_rewarded }} add_ideas = {PREFIX}{tag}_discipline }}
\telse_if = {{ limit = {{ NOT = {{ OR = {{ has_country_flag = COLDWAR_SSR_court_review_rewarded has_country_flag = COLDWAR_SSR_executive_service_rewarded }} }} }} add_ideas = {PREFIX}{tag}_patronage }}
\tremove_ideas = {PREFIX}{tag}_social
\tremove_ideas = {PREFIX}{tag}_social_republican
\tif = {{ limit = {{ has_country_flag = COLDWAR_SSR_service_settlement_rewarded }} add_ideas = {PREFIX}{tag}_social_republican }}
\telse = {{ add_ideas = {PREFIX}{tag}_social }}
\tremove_ideas = {PREFIX}{tag}_technical
\tif = {{ limit = {{ COLDWAR_SSR_is_ssr = yes }} add_ideas = {PREFIX}{tag}_technical }}
\tremove_ideas = {PREFIX}{tag}_regional_original
\tremove_ideas = {PREFIX}{tag}_regional_managed
\tremove_ideas = {PREFIX}{tag}_regional_aftercare
\tif = {{ limit = {{ has_country_flag = COLDWAR_SSR_transition_settlement_rewarded }} add_ideas = {PREFIX}{tag}_regional_aftercare }}
\telse_if = {{ limit = {{ has_country_flag = {regional_node['receipt']} }} add_ideas = {PREFIX}{tag}_regional_managed }}
\telse = {{ add_ideas = {PREFIX}{tag}_regional_original }}
\tremove_ideas = {PREFIX}{tag}_unconverted_orders
\tif = {{ limit = {{ COLDWAR_SSR_is_independent = yes has_country_flag = COLDWAR_SSR_deepen_specialisation_rewarded NOT = {{ OR = {{ has_country_flag = COLDWAR_SSR_export_conversion_rewarded has_country_flag = COLDWAR_SSR_domestic_chains_rewarded }} }} }} add_ideas = {PREFIX}{tag}_unconverted_orders }}
}}""")

    # Receipt-driven ordinary programme groups. Their variables are recomputed only at reconciliation.
    effects.append(f"{PREFIX}rebuild_groups = {{")
    for group, modifiers in groups.items():
        for variable in modifiers.values():
            effects.append(f"\tclear_variable = {variable}")
        dyn_id = f"{PREFIX}group_{shared.slug(group)}"
        effects.append(f"\tif = {{ limit = {{ has_dynamic_modifier = {{ modifier = {dyn_id} }} }} remove_dynamic_modifier = {{ modifier = {dyn_id} }} }}")
    for node in nodes:
        if node.get("specialisation") or node.get("replace"):
            continue
        group = node["group_key"]
        if group not in groups:
            continue
        status = "COLDWAR_SSR_is_ssr = yes" if node["phase"] == "ssr" else "COLDWAR_SSR_is_independent = yes"
        if node["phase"] == "party":
            status += f" {PARTY[str(node['gate'][4:])]} = yes"
        if node.get("scope_tag"):
            status += f" original_tag = {node['scope_tag']}"
        conditions = f"{status} has_country_flag = {node['receipt']}"
        effects.append(f"\tif = {{ limit = {{ {conditions} }}")
        for key, value in node["modifiers"].items():
            effects.append(f"\t\tadd_to_variable = {{ {_var(group,key)} = {shared.number(value)} }}")
        effects.append("\t}")
    for group in groups:
        phase = next(n["phase"] for n in nodes if n["group_key"] == group)
        active = "COLDWAR_SSR_is_ssr = yes" if phase == "ssr" else "COLDWAR_SSR_is_independent = yes"
        group_nodes = [n for n in nodes if n["group_key"] == group and not n.get("specialisation") and not n.get("replace")]
        if phase == "party":
            node = group_nodes[0]
            active += f" {PARTY[str(node['gate'][4:])]} = yes original_tag = {node['scope_tag']}"
        receipts = " ".join(f"has_country_flag = {n['receipt']}" for n in group_nodes)
        active += f" AND = {{ OR = {{ {receipts} }} }}"
        effects.append(f"\tif = {{ limit = {{ {active} }} add_dynamic_modifier = {{ modifier = {PREFIX}group_{shared.slug(group)} }} }}")
    effects.append(f"\tforce_update_dynamic_modifier = yes\n}}")

    # Select one exact specialisation receipt stage and apply either full Union or scaled sovereign legacy.
    effects.append(f"{PREFIX}rebuild_specialisation = {{")
    for role in ("aircraft", "armour", "artillery", "army", "navy", "agriculture", "industry", "resources", "electronics"):
        spec_nodes = [n for n in models["UKR"]["nodes"] if n.get("specialisation") == role]
        role_states = _reachable_spec_states(spec_nodes)
        role_idea_ids = [f"{PREFIX}special_{role}_{kind}_{i}" for i in range(len(role_states)) for kind in ("full", "legacy")]
        for i, state in enumerate(role_states):
            if not any(n["key"].endswith("_mandate") and n["id"] in state for n in spec_nodes):
                continue
            cond = " ".join(f"has_country_flag = {n}_rewarded" for n in sorted(state))
            cond += (" " if cond else "") + " ".join(f"NOT = {{ has_country_flag = {n}_rewarded }}" for n in sorted({n["id"] for n in spec_nodes} - set(state)))
            full_id=f"{PREFIX}special_{role}_full_{i}";legacy_id=f"{PREFIX}special_{role}_legacy_{i}"
            effects.append(f"\tif = {{ limit = {{ COLDWAR_SSR_is_ssr = yes has_country_flag = COLDWAR_SSR_special_{role}_mandate_rewarded AND = {{ {cond} }} NOT = {{ has_idea = {full_id} }} }}")
            effects.extend(f"\t\tremove_ideas = {idea}" for idea in role_idea_ids)
            effects.append(f"\t\tadd_ideas = {full_id}")
            effects.append("\t}")
            effects.append(f"\tif = {{ limit = {{ COLDWAR_SSR_is_independent = yes has_country_flag = COLDWAR_SSR_special_{role}_mandate_rewarded AND = {{ {cond} }} NOT = {{ has_idea = {legacy_id} }} }}")
            effects.extend(f"\t\tremove_ideas = {idea}" for idea in role_idea_ids)
            effects.append(f"\t\tadd_ideas = {legacy_id}")
            effects.append("\t}")
        effects.append(f"\tif = {{ limit = {{ NOT = {{ COLDWAR_SSR_is_ssr = yes }} NOT = {{ COLDWAR_SSR_is_independent = yes }} }}")
        effects.extend(f"\t\tremove_ideas = {idea}" for idea in role_idea_ids)
        effects.append("\t}")
    effects.append("}")

    # Freeze preparation state exactly once when the tag first becomes sovereign.
    for tag, model in models.items():
        snap = []
        effects.append(f"{PREFIX}snapshot_preparation_{tag} = {{")
        for liability, receipts in PREP.items():
            possible = [r.format(tag) for r in receipts]
            from itertools import combinations
            for count in range(len(possible)+1):
                flag = f"{PREFIX}prep_snapshot_{liability}_{count}"
                loc[flag] = ""
                effects.append(f"\tclr_country_flag = {flag}")
                for selected in combinations(possible, count):
                    cond = " ".join(f"has_country_flag = {r}" for r in selected)
                    cond += (" " if cond else "") + " ".join(f"NOT = {{ has_country_flag = {r} }}" for r in sorted(set(possible) - set(selected)))
                    effects.append(f"\tif = {{ limit = {{ AND = {{ {cond} }} }} set_country_flag = {flag} }}")
                snap.append(flag)
        effects.append("}")

        # Recompute transition dynamic variables from original abrupt values, prep snapshot, live repair receipts and diplomacy settlement.
        effects.append(f"{PREFIX}update_transition_{tag} = {{")
        for liability in ("broken_supply", "state_accounts", "command_gap"):
            entry = _transition_data(model, tag)[liability]
            variables = {key: f"{PREFIX}transition_{liability}_{key}" for key in entry["modifiers"]}
            for var in variables.values(): effects.append(f"\tclear_variable = {var}")
            for prep_count in range(len(PREP[liability])+1):
                prep_flag = f"{PREFIX}prep_snapshot_{liability}_{prep_count}"
                for repair_count in range(4):
                    repair_groups = REPAIRS[liability]
                    from itertools import combinations
                    for selected_indices in combinations(range(len(repair_groups)), repair_count):
                        selected = [repair_groups[index] for index in selected_indices]
                        unselected = [group for index, group in enumerate(repair_groups) if index not in selected_indices]
                        repair_cond = " ".join("OR = { " + " ".join(f"has_country_flag = {r}" for r in group) + " }" for group in selected)
                        repair_cond += (" " if repair_cond else "") + " ".join("NOT = { OR = { " + " ".join(f"has_country_flag = {r}" for r in group) + " } }" for group in unselected)
                        for negotiated in (False, True):
                            value_map = _transition_values(model, tag, liability, prep_count, repair_count, negotiated)
                            cond = f"has_country_flag = {prep_flag} AND = {{ {repair_cond} }}"
                            cond += " COLDWAR_SSR_negotiated_transition_active = yes" if negotiated else " NOT = { COLDWAR_SSR_negotiated_transition_active = yes }"
                            effects.append(f"\tif = {{ limit = {{ {cond} }}")
                            for key, value in value_map.items():
                                effects.append(f"\t\tset_variable = {{ {variables[key]} = {shared.number(value)} }}")
                            effects.append("\t}")
            transition_modifier = f"{PREFIX}transition_{liability}"
            effects.append(f"\tif = {{ limit = {{ has_dynamic_modifier = {{ modifier = {transition_modifier} }} }} remove_dynamic_modifier = {{ modifier = {transition_modifier} }} }}")
            effects.append(f"\tif = {{ limit = {{ COLDWAR_SSR_is_independent = yes has_country_flag = {PREFIX}transition_recorded }} add_dynamic_modifier = {{ modifier = {PREFIX}transition_{liability} }} }}")
        effects.append("\tforce_update_dynamic_modifier = yes\n}")

    # Universal reconcile and public integration callbacks.
    effects.append(f"""COLDWAR_SSR_reconcile = {{
\tif = {{ limit = {{ COLDWAR_SSR_is_participant = yes has_country_flag = {PREFIX}ever_ssr is_subject = no has_capitulated = no NOT = {{ has_country_flag = {PREFIX}transition_recorded }} }}
\t\t{PREFIX}capture_transition = yes
\t\tset_country_flag = {PREFIX}transition_recorded
\t}}
\tif = {{ limit = {{ COLDWAR_SSR_is_participant = yes }}
\t\tif = {{ limit = {{ COLDWAR_SSR_is_ssr = yes }} set_country_flag = {PREFIX}ssr_active clr_country_flag = {PREFIX}independent_active }}
\t\telse_if = {{ limit = {{ COLDWAR_SSR_is_independent = yes }} clr_country_flag = {PREFIX}ssr_active set_country_flag = {PREFIX}independent_active }}
\t\telse = {{ clr_country_flag = {PREFIX}ssr_active clr_country_flag = {PREFIX}independent_active }}
\t\t{PREFIX}rebuild_groups = yes
\t\t{PREFIX}rebuild_specialisation = yes
\t\tif = {{ limit = {{ original_tag = UKR }} {PREFIX}starting_UKR = yes }}
\t\tif = {{ limit = {{ original_tag = BLR }} {PREFIX}starting_BLR = yes }}
\t\tif = {{ limit = {{ original_tag = MLV }} {PREFIX}starting_MLV = yes }}
\t\tif = {{ limit = {{ original_tag = EST }} {PREFIX}starting_EST = yes }}
\t\tif = {{ limit = {{ original_tag = LAT }} {PREFIX}starting_LAT = yes }}
\t\tif = {{ limit = {{ original_tag = LIT }} {PREFIX}starting_LIT = yes }}
\t\tif = {{ limit = {{ original_tag = GEO }} {PREFIX}starting_GEO = yes }}
\t\tif = {{ limit = {{ original_tag = ARM }} {PREFIX}starting_ARM = yes }}
\t\tif = {{ limit = {{ original_tag = AZE }} {PREFIX}starting_AZE = yes }}
\t\tif = {{ limit = {{ original_tag = KAZ }} {PREFIX}starting_KAZ = yes }}
\t\tif = {{ limit = {{ original_tag = UZB }} {PREFIX}starting_UZB = yes }}
\t\tif = {{ limit = {{ original_tag = TRK }} {PREFIX}starting_TRK = yes }}
\t\tif = {{ limit = {{ original_tag = KYR }} {PREFIX}starting_KYR = yes }}
\t\tif = {{ limit = {{ original_tag = TAJ }} {PREFIX}starting_TAJ = yes }}
\t\tif = {{ limit = {{ has_country_flag = {PREFIX}transition_recorded }}
\t\t\tif = {{ limit = {{ original_tag = UKR }} {PREFIX}update_transition_UKR = yes }}
\t\t\tif = {{ limit = {{ original_tag = BLR }} {PREFIX}update_transition_BLR = yes }}
\t\t\tif = {{ limit = {{ original_tag = MLV }} {PREFIX}update_transition_MLV = yes }}
\t\t\tif = {{ limit = {{ original_tag = EST }} {PREFIX}update_transition_EST = yes }}
\t\t\tif = {{ limit = {{ original_tag = LAT }} {PREFIX}update_transition_LAT = yes }}
\t\t\tif = {{ limit = {{ original_tag = LIT }} {PREFIX}update_transition_LIT = yes }}
\t\t\tif = {{ limit = {{ original_tag = GEO }} {PREFIX}update_transition_GEO = yes }}
\t\t\tif = {{ limit = {{ original_tag = ARM }} {PREFIX}update_transition_ARM = yes }}
\t\t\tif = {{ limit = {{ original_tag = AZE }} {PREFIX}update_transition_AZE = yes }}
\t\t\tif = {{ limit = {{ original_tag = KAZ }} {PREFIX}update_transition_KAZ = yes }}
\t\t\tif = {{ limit = {{ original_tag = UZB }} {PREFIX}update_transition_UZB = yes }}
\t\t\tif = {{ limit = {{ original_tag = TRK }} {PREFIX}update_transition_TRK = yes }}
\t\t\tif = {{ limit = {{ original_tag = KYR }} {PREFIX}update_transition_KYR = yes }}
\t\t\tif = {{ limit = {{ original_tag = TAJ }} {PREFIX}update_transition_TAJ = yes }}
\t\t}}
\t\tCOLDWAR_SSR_market_reconcile = yes
\t\tCOLDWAR_SSR_diplomacy_reconcile = yes
\t}}
}}""")

    # Transition capture and safe admission API.
    effects.append(f"""COLDWAR_SSR_lifecycle_check_status = {{
\tif = {{ limit = {{ IMP_is_1970_scenario = yes COLDWAR_SOV_is_union_republic = yes NOT = {{ has_country_flag = {PREFIX}scenario_identity }} }}
\t\tset_country_flag = {PREFIX}scenario_identity
\t\tset_country_flag = {PREFIX}ever_ssr
\t\tCOLDWAR_SSR_load_tree = yes
\t}}
\tif = {{ limit = {{ COLDWAR_SSR_is_ssr = yes }} set_country_flag = {PREFIX}ever_ssr }}
\tif = {{ limit = {{ COLDWAR_SSR_is_participant = yes has_country_flag = {PREFIX}ever_ssr is_subject = no has_capitulated = no NOT = {{ has_country_flag = {PREFIX}transition_recorded }} }}
\t\t{PREFIX}capture_transition = yes
\t\tset_country_flag = {PREFIX}transition_recorded
\t\tCOLDWAR_SSR_reconcile = yes
\t}}
\tif = {{ limit = {{ COLDWAR_SSR_is_independent = yes COLDWAR_SSR_negotiated_transition_active = yes NOT = {{ has_country_flag = {PREFIX}negotiated_cache }} }}
\t\tset_country_flag = {PREFIX}negotiated_cache
\t\tCOLDWAR_SSR_reconcile = yes
\t}}
\tif = {{ limit = {{ COLDWAR_SSR_is_independent = yes NOT = {{ COLDWAR_SSR_negotiated_transition_active = yes }} has_country_flag = {PREFIX}negotiated_cache }}
\t\tclr_country_flag = {PREFIX}negotiated_cache
\t\tCOLDWAR_SSR_reconcile = yes
\t}}
\tif = {{ limit = {{ COLDWAR_SSR_is_participant = yes }}
\t\tif = {{ limit = {{ NOT = {{ has_country_flag = {PREFIX}party_cache_initialized }} }} {PREFIX}cache_party = yes }}
\t\telse_if = {{ limit = {{ check_variable = {{ var = {PREFIX}ruling_party_slot value = ruling_party compare = not_equals }} }} {PREFIX}cache_party = yes COLDWAR_SSR_reconcile = yes }}
\t\tif = {{ limit = {{ COLDWAR_SSR_is_ssr = yes NOT = {{ has_country_flag = {PREFIX}ssr_active }} }} COLDWAR_SSR_reconcile = yes }}
\t\tif = {{ limit = {{ COLDWAR_SSR_is_independent = yes NOT = {{ has_country_flag = {PREFIX}independent_active }} }} COLDWAR_SSR_reconcile = yes }}
\t\tif = {{ limit = {{ NOT = {{ COLDWAR_SSR_is_ssr = yes }} has_country_flag = {PREFIX}ssr_active }} COLDWAR_SSR_reconcile = yes }}
\t\tif = {{ limit = {{ NOT = {{ COLDWAR_SSR_is_independent = yes }} has_country_flag = {PREFIX}independent_active }} COLDWAR_SSR_reconcile = yes }}
\t}}
}}
COLDWAR_SSR_record_admission = {{
\tif = {{ limit = {{ IMP_is_1970_scenario = yes is_subject_of = SOV has_country_flag = COLDWAR_SSR_admission_accepted NOT = {{ has_country_flag = {PREFIX}accepted_admission }} }}
\t\tset_country_flag = {PREFIX}accepted_admission
\t\tset_country_flag = {PREFIX}ever_ssr
\t\tclr_country_flag = COLDWAR_SSR_admission_accepted
\t\tCOLDWAR_SSR_load_tree = yes
\t\tCOLDWAR_SSR_reconcile = yes
\t}}
}}""")
    effects.append(f"""{PREFIX}cache_party = {{
\tset_variable = {{ {PREFIX}ruling_party_slot = ruling_party }}
\tset_country_flag = {PREFIX}party_cache_initialized
}}""")

    # Startup and daily status watcher. A country callback is cheap and limited to the approved roster.
    on_actions = ["on_actions = {", "\ton_startup = {", "\t\teffect = {", *[f"\t\t\t{tag} = {{ {PREFIX}initialize = yes }}" for tag in TAGS], "\t\t}", "\t}", "\ton_ruling_party_change = {", "\t\teffect = {", f"\t\t\tif = {{ limit = {{ COLDWAR_SSR_is_participant = yes }} {PREFIX}cache_party = yes COLDWAR_SSR_reconcile = yes }}", "\t\t}", "\t}"]
    effects.append(f"""{PREFIX}initialize = {{
\tif = {{ limit = {{ IMP_is_1970_scenario = yes COLDWAR_SOV_is_union_republic = yes }}
\t\tset_country_flag = {PREFIX}scenario_identity
\t\tset_country_flag = {PREFIX}ever_ssr
\t\t{PREFIX}cache_party = yes
\t\tCOLDWAR_SSR_load_tree = yes
\t\tCOLDWAR_SSR_reconcile = yes
\t}}
}}""")

    # Public numeric previews for the next liability repair. These are effect-tooltip rows only.
    from itertools import combinations
    for liability in ("broken_supply", "state_accounts", "command_gap"):
        preview_lines = [f"COLDWAR_SSR_preview_repair_{liability} = {{"]
        for tag, model in models.items():
            prep_receipts = [r.format(tag) for r in PREP[liability]]
            repair_groups = REPAIRS[liability]
            for prep_count in range(len(prep_receipts) + 1):
                prep_conditions = []
                for selected in combinations(prep_receipts, prep_count):
                    clause = " ".join(f"has_country_flag = {r}" for r in selected)
                    clause += (" " if clause else "") + " ".join(f"NOT = {{ has_country_flag = {r} }}" for r in sorted(set(prep_receipts)-set(selected)))
                    prep_conditions.append(f"AND = {{ NOT = {{ has_country_flag = {PREFIX}transition_recorded }} {clause} }}")
                prep_conditions.append(f"AND = {{ has_country_flag = {PREFIX}transition_recorded has_country_flag = {PREFIX}prep_snapshot_{liability}_{prep_count} }}")
                for repair_count in range(3):
                    for repair_cond in _repair_conditions(repair_groups, repair_count):
                        for negotiated in (False, True):
                            delta = _next_repair_delta(model, tag, liability, prep_count, repair_count, negotiated)
                            for prep_cond in prep_conditions:
                                status = "COLDWAR_SSR_negotiated_transition_active = yes" if negotiated else "NOT = { COLDWAR_SSR_negotiated_transition_active = yes }"
                                condition = f"original_tag = {tag} {prep_cond} AND = {{ {repair_cond} }} {status}"
                                preview_lines.append(f"\tif = {{ limit = {{ hidden_trigger = {{ AND = {{ {condition} }} }} }}")
                                for key, value in delta.items():
                                    tooltip = f"COLDWAR_SSR_stat_{key}_tt"
                                    preview_lines.append(f"\t\tadd_to_variable = {{ COLDWAR_SSR_preview_value = {shared.number(value)} tooltip = {tooltip} }}")
                                preview_lines.append("\t}")
        preview_lines.append("}")
        effects.append("\n".join(preview_lines))
    for tag in TAGS:
        on_actions.append(f"\ton_daily_{tag} = {{ effect = {{ {tag} = {{ {PREFIX}check_status = yes COLDWAR_SSR_market_reconcile = yes COLDWAR_SSR_diplomacy_reconcile = yes }} }} }}")
    on_actions.extend([
        "\ton_puppet = { effect = { ROOT = { COLDWAR_SSR_lifecycle_check_status = yes } } }",
        "\ton_subject_free = { effect = { ROOT = { COLDWAR_SSR_lifecycle_check_status = yes } } }",
        "\ton_release_as_free = { effect = { ROOT = { COLDWAR_SSR_lifecycle_check_status = yes } } }",
        "\ton_release_as_puppet = { effect = { ROOT = { COLDWAR_SSR_lifecycle_check_status = yes } } }",
        "}",
    ])

    # Every static idea needs a player-facing name and concise description.
    for k, name in list(loc.items()):
        if k not in {f"{PREFIX}group_{shared.slug(g)}" for g in groups} and "special_" not in k:
            loc.setdefault(k + "_desc", name + ".")
    for group in groups:
        k = PREFIX + "group_" + shared.slug(group)
        loc[k] = group.replace("_", " ").title()
        loc[k + "_desc"] = "Completed national programme measures currently in force."
    for role in ("aircraft", "armour", "artillery", "army", "navy", "agriculture", "industry", "resources", "electronics"):
        for i, _ in enumerate(_reachable_spec_states([n for n in models["UKR"]["nodes"] if n.get("specialisation") == role])):
            for suffix in ("full", "legacy"):
                k=f"{PREFIX}special_{role}_{suffix}_{i}"
                loc[k+"_desc"] = "National industrial and technical programme benefits currently active."
    loc["COLDWAR_SSR_lifecycle_weekly_expense"] = "Weekly Soviet republic programme costs"

    # Emit scripts with root-compatible callbacks. Do not define external loader/market/diplomacy effects.
    effbody = "\n\n".join(effects)
    # Weekly expenses for all receipt-backed focus programmes, with specialisation handled above.
    budget = [f"COLDWAR_SSR_lifecycle_refresh_budget = {{", "\tset_variable = { COLDWAR_SSR_lifecycle_weekly_expense = 0 }", "\tif = { limit = { COLDWAR_SSR_is_ssr = yes }"]
    for n in nodes:
        if n.get("specialisation") or n.get("market_course") or not n.get("weekly_gdp_cost"):
            continue
        if n["phase"] != "ssr":
            continue
        budget.append(f"\t\tif = {{ limit = {{ has_country_flag = {n['receipt']} }} add_to_variable = {{ COLDWAR_SSR_lifecycle_weekly_expense = {{ value = gdp_total multiply = {shared.number(n['weekly_gdp_cost'])} }} }} }}")
    budget.append("\t}")
    budget.append("\tif = { limit = { COLDWAR_SSR_is_independent = yes }")
    for n in nodes:
        if n.get("specialisation") or n.get("market_course") or not n.get("weekly_gdp_cost"):
            continue
        if n["phase"] in ("independent", "party"):
            share = n["weekly_gdp_cost"]
            budget.append(f"\t\tif = {{ limit = {{ has_country_flag = {n['receipt']}" + (f" {PARTY[str(n['gate'][4:])]} = yes original_tag = {n['scope_tag']}" if n["phase"] == "party" else "") + f" }} add_to_variable = {{ COLDWAR_SSR_lifecycle_weekly_expense = {{ value = gdp_total multiply = {shared.number(share)} }} }} }}")
    budget.append("\t}")
    for role in ("aircraft", "armour", "artillery", "army", "navy", "agriculture", "industry", "resources", "electronics"):
        root=next(n for n in models["UKR"]["nodes"] if n.get("specialisation")==role and n["key"].endswith("_mandate"))
        budget.append(f"\tif = {{ limit = {{ COLDWAR_SSR_is_ssr = yes has_country_flag = {root['receipt']} }} add_to_variable = {{ COLDWAR_SSR_lifecycle_weekly_expense = {{ value = gdp_total multiply = {shared.number(root['weekly_gdp_cost'])} }} }} }}")
        budget.append(f"\tif = {{ limit = {{ COLDWAR_SSR_is_independent = yes has_country_flag = {root['receipt']} }} add_to_variable = {{ COLDWAR_SSR_lifecycle_weekly_expense = {{ value = gdp_total multiply = {shared.number(root['legacy_weekly_gdp_cost'])} }} }} }}")
    budget.append("}")
    # Capture each original republic's own preparation receipts before the transition is recorded.
    capture = f"{PREFIX}capture_transition = {{\n"
    for tag in TAGS:
        capture += f"\tif = {{ limit = {{ original_tag = {tag} }} {PREFIX}snapshot_preparation_{tag} = yes }}\n"
    capture += "}"
    effbody += "\n\n" + capture + "\n\n" + "\n".join(budget)

    script_paths = [
        shared.write("common/ideas/COLDWAR_SSR_lifecycle_ideas.txt", "# Reuses local MD idea sprites defined in interface/MD_ideas.gfx.\n# Source textures: gfx/interface/ideas/air_force/air_research.dds, gfx/interface/ideas/army/army_tank_good.dds, gfx/interface/ideas/army/army_artillery_good.dds, gfx/interface/ideas/army/army_war_college.dds, gfx/interface/ideas/economy/agriculture.dds, gfx/interface/ideas/navy/coastal_navy.dds, gfx/interface/ideas/economy/industrial_concern.dds, gfx/interface/ideas/research/research_bonus.dds, gfx/interface/ideas/politics/political_reform.dds.\n# Original sprite authorship: unknown. Licence details: unknown. No art files were copied or modified.\n" + "\n".join(ideas)),
        shared.write("common/dynamic_modifiers/COLDWAR_SSR_lifecycle_dynamic_modifiers.txt", "\n\n".join(dynamic)),
        shared.write("common/scripted_effects/COLDWAR_SSR_lifecycle_effects.txt", effbody),
        shared.write("common/scripted_triggers/COLDWAR_SSR_lifecycle_triggers.txt", "\n\n".join(triggers)),
        shared.write("common/on_actions/COLDWAR_SSR_lifecycle_on_actions.txt", "\n".join(on_actions)),
        shared.write("localisation/english/COLDWAR_SSR_lifecycle_l_english.yml", shared.loc_text(loc), localisation=True),
    ]
    return script_paths


if __name__ == "__main__":
    print("\n".join(generate()))
