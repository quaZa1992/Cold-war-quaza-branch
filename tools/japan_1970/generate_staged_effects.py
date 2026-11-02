# IMPERIA COLD WAR — Cold War: Japan 1970 staged general-policy focus effects.
"""Emit reviewable, non-loaded fragments for approved National life/Economy focuses."""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "staging"
DESIGN = json.loads((ROOT / "approved_design.json").read_text(encoding="utf-8"))["design"]
from reward_revision import effective_design, effective_inventory
DESIGN = effective_design(DESIGN)
INVENTORY = effective_inventory(json.loads((ROOT / "effect_inventory.json").read_text(encoding="utf-8")))
PREFIX = "COLDWAR_JAP_1970"
COUNTRY_GUARDS = ["original_tag = JAP", "IMP_is_1970_scenario = yes"]
FOCUS_GUARDS = {
    "national_4_licensed_production": ["has_idea = COLDWAR_ni_licensed_armaments_programme"],
    "microelectronics_capacity": ["OR = { has_tech = microchip_production_2 has_tech = microchip_production_3 }"],
}

# Verified from common/buildings/00_buildings.txt. `shares_slots` is true only
# where level_cap explicitly sets shares_slots = yes. Inventory buildings are
# all state-level; none use province_max. The two energy keystone types share
# group_by = infrastructure_keystone with state_max = 1.
BUILDING_LIMITS = {
    "industrial_complex": (50, True), "arms_factory": (35, True), "dockyard": (20, True),
    "offices": (50, True), "microchip_plant": (5, True),
    "energy_infrastructure": (1, True), "industrial_infrastructure": (1, True),
    "fossil_powerplant": (20, False), "fuel_silo": (5, False), "nuclear_reactor": (20, False),
    "renewable_energy_infra": (20, False), "infrastructure": (6, False),
    "internet_station": (11, False), "rail_terminal": (5, False),
}
BUILDING_GROUPS = {"energy_infrastructure": ("energy_infrastructure", "industrial_infrastructure"),
                   "industrial_infrastructure": ("energy_infrastructure", "industrial_infrastructure")}
BONUS_EFFECT_KEYS = ("add_tech_bonus", "add_doctrine_cost_reduction", "add_equipment_bonus")

SPECIAL_TO_POLLUTION = {"pollution_stability": "stability_factor", "pollution_health": "health_cost_multiplier_modifier"}
STATE_NAMES = {}
for p in (ROOT.parents[1] / "history" / "states").glob("*.txt"):
    m = re.match(r"(\d+)-(.+)\.txt$", p.name)
    if m: STATE_NAMES[int(m.group(1))] = m.group(2).replace("_", " ")

MOD_LABELS = {
    "stability_factor": "stability factor", "bureaucracy_cost_multiplier_modifier": "bureaucracy expenditure",
    "social_cost_multiplier_modifier": "social expenditure", "health_cost_multiplier_modifier": "health spending",
    "education_cost_multiplier_modifier": "education spending", "army_personnel_cost_multiplier_modifier": "army personnel expenditure",
    "civilian_factories_productivity": "civilian-sector productivity", "industrial_capacity_factory": "military factory output",
    "political_power_factor": "political power gain", "consumer_goods_factor": "Tax Cost Factor",
    "tax_gain_multiplier_modifier": "tax income",
    "dockyard_productivity": "dockyard-sector productivity", "offices_productivity": "office-sector productivity",
    "agricolture_productivity_modifier": "agricultural productivity", "research_speed_factor": "research speed",
    "army_core_defence_factor": "army core defence", "army_defence_factor": "army defence", "army_attack_factor": "army attack",
    "training_time_factor": "army training time", "experience_gain_army_factor": "army experience gain factor",
    "experience_gain_air_factor": "air experience gain factor", "navy_org_factor": "navy organisation",
    "navy_submarine_detection_factor": "submarine detection", "navy_max_range_factor": "naval range",
    "air_detection": "air detection", "air_mission_efficiency": "air mission efficiency", "air_range_factor": "air range",
    "planning_speed": "planning speed", "recruitable_population_factor": "recruitable population factor",
    "industrial_capacity_dockyard": "dockyard output", "energy_use_modifier_mils": "military factory power consumption",
    "energy_use_modifier_dockyards": "dockyard power consumption", "energy_use_modifier_civs": "civilian factory power consumption",
    "energy_use_modifier_offices": "office power consumption", "non_electric_fuel_consumption_modifier": "non-electric fuel consumption",
    "fossil_pp_fuel_consumption_modifier": "fossil power-plant fuel consumption", "fossil_pp_energy_generation_modifier": "fossil power generation",
    "nuclear_fuel_consumption_modifier": "nuclear fuel consumption", "nuclear_energy_generation_modifier": "nuclear power generation",
    "renewable_energy_gain_multiplier": "renewable power generation factor", "energy_gain_multiplier": "electrical power generation factor",
    "max_fuel_factor": "maximum fuel capacity", "country_productivity_growth_modifier": "productivity growth",
    "production_speed_industrial_complex_factor": "civilian factory construction speed", "production_speed_dockyard_factor": "dockyard construction speed",
}
PREVIEW_TOOLTIP_OVERRIDES = {
    "air_range_factor": "COLDWAR_JAP_1970_air_range_factor_tt",
    "energy_use_modifier_dockyards": "COLDWAR_JAP_1970_energy_use_modifier_dockyards_tt",
    "experience_gain_air_factor": "COLDWAR_experience_gain_air_factor_tt",
    "experience_gain_army_factor": "COLDWAR_experience_gain_army_factor_tt",
    "max_fuel_factor": "COLDWAR_JAP_1970_max_fuel_factor_tt",
    "navy_max_range_factor": "COLDWAR_navy_max_range_factor_tt",
    "navy_org_factor": "COLDWAR_navy_org_factor_tt",
    "research_speed_factor": "COLDWAR_research_speed_factor_tt",
    "training_time_factor": "COLDWAR_training_time_factor_tt",
}
NEW_PREVIEW_TOOLTIP_LOCALISATION = {
    "COLDWAR_JAP_1970_air_range_factor_tt": "Air Range: $RIGHT|+=%1$",
    "COLDWAR_JAP_1970_energy_use_modifier_dockyards_tt": "Dockyard Energy Use: $RIGHT|-=%1$",
    "COLDWAR_JAP_1970_max_fuel_factor_tt": "Maximum Fuel Capacity: $RIGHT|+=%1$",
}


def ident(s): return re.sub(r"[^A-Za-z0-9_]", "_", s)
def fid(s): return f"{PREFIX}_{ident(s)}"
def section_var(section, key): return f"{PREFIX}_{ident(section)}_{ident(key)}"
def q(s): return '"' + s.replace('"', '\\"') + '"'

def capacity_conditions(building, level, awarded_slots):
    max_level, shares_slots = BUILDING_LIMITS[building]
    # building_level@X is the state's current built level. Requiring current <
    # max-level+1-level guarantees the immediate grant remains within state_max.
    conditions = [f"check_variable = {{ building_level@{building} < {max_level - level + 1} }}"]
    for group_building in BUILDING_GROUPS.get(building, ()):
        if group_building != building:
            conditions.append(f"check_variable = {{ building_level@{group_building} = 0 }}")
    # A focus grant provides one new shared slot for every granted level.
    # Check any remaining capacity separately; include_locked is supported
    # only for buildings that consume shared slots.
    existing_levels_needed = max(0, level - awarded_slots)
    if existing_levels_needed:
        size = existing_levels_needed - 1
        if shares_slots:
            conditions.append(f"free_building_slots = {{ building = {building} size > {size} include_locked = no }}")
        else:
            conditions.append(f"free_building_slots = {{ building = {building} size > {size} }}")
    return conditions

def state_building_guard(state_id, building, level, awarded_slots, include_technology=True):
    import sys
    sys.path.insert(0, str(ROOT.parents[1] / 'tools/reward_rework_20261027'))
    from building_technology import state_technology_guard
    conditions = ["is_owned_by = ROOT", "is_controlled_by = ROOT", *capacity_conditions(building, level, awarded_slots)]
    technology = state_technology_guard(building, level)
    if technology and include_technology:
        conditions.append(technology)
    return f"{state_id} = {{ {' '.join(conditions)} }}"

def expected_bonus_entry_counts(rec):
    return {
        "add_tech_bonus": sum(bonus.get("category") in ("CAT_industry", "CAT_agriculture")
                               for bonus in rec.get("bonuses", [])),
        "add_doctrine_cost_reduction": len(rec.get("doctrine_bonuses", [])),
        "add_equipment_bonus": len(rec.get("equipment_bonuses", [])),
    }

def assert_bonus_entry_counts(focus_id, lines, rec, source):
    expected = expected_bonus_entry_counts(rec)
    actual = {key: sum(line.strip() == f"{key} = {{" for line in lines) for key in BONUS_EFFECT_KEYS}
    if actual != expected:
        raise ValueError(f"{focus_id}: {source} bonus entry counts {actual} do not match design record {expected}")

def effect_preview_body(section, node, rec, loc):
    """Build a native, display-only effect_tooltip body matching the payout."""
    lines = []
    if rec.get("cost_gdp_share", 0):
        lines += [
            f"set_temp_variable = {{ treasury_change = {{ value = gdp_total multiply = -{rec['cost_gdp_share']:.5f} }} }}",
            "modify_treasury_effect = yes",
        ]
    elif rec["treasury_cost"]:
        lines += [f"set_temp_variable = {{ treasury_change = -{rec['treasury_cost']:g} }}", "modify_treasury_effect = yes"]

    dynamic_changes = []
    section_mod = f"{PREFIX}_{ident(section['name'])}_permanent"
    for key, amount in sorted(rec["modifiers"].items()):
        dynamic_changes.append((section_mod, section_var(section["name"], key), key, amount))
    for special, amount in sorted(rec["special"].items()):
        if special == "energy_use_civs":
            dynamic_changes.append((f"{PREFIX}_energy_intensity_modifier", f"{PREFIX}_energy_use_civs", "energy_use_modifier_civs", amount))
        elif special in SPECIAL_TO_POLLUTION:
            native_key = SPECIAL_TO_POLLUTION[special]
            variable = f"{PREFIX}_pollution_stability" if native_key == "stability_factor" else f"{PREFIX}_pollution_health_cost"
            dynamic_changes.append((f"{PREFIX}_industrial_pollution_modifier", variable, native_key, amount))

    seen_modifiers = set()
    for modifier_id, variable, native_key, amount in dynamic_changes:
        if modifier_id not in seen_modifiers:
            lines += ["custom_effect_tooltip = {", "\tlocalization_key = modifies_dynamic_modifier_tt", f"\tMODIFIER = {modifier_id}", "}"]
            seen_modifiers.add(modifier_id)
        tooltip_key = PREVIEW_TOOLTIP_OVERRIDES.get(native_key, f"{native_key}_tt")
        lines.append(f"add_to_variable = {{ {variable} = {amount:.5f} tooltip = {tooltip_key} }}")

    for bonus in rec["bonuses"]:
        if bonus["category"] not in ("CAT_industry", "CAT_agriculture"):
            continue
        bonus_id = f"{fid(node['id'])}_research"
        lines += ["add_tech_bonus = {", f"\tname = {bonus_id}", f"\tbonus = {bonus['bonus']:.2f}", f"\tuses = {bonus['uses']}", f"\tcategory = {bonus['category']}", "}"]

    for index, bonus in enumerate(rec.get("doctrine_bonuses", [])):
        bonus_id = f"{fid(node['id'])}_doctrine_{index}"
        loc.append(f" {bonus_id}:0 {q(node['name'])}")
        lines += ["add_doctrine_cost_reduction = {", f"\tname = {bonus_id}",
                  f"\tcost_reduction = {bonus['cost_reduction']:.2f}", f"\tuses = {bonus['uses']}",
                  f"\tcategory = {bonus['category']}", "}"]
    for index, equipment_bonus in enumerate(rec.get("equipment_bonuses", [])):
        bonus_id = f"{fid(node['id'])}_equipment_{index}"
        loc.append(f" {bonus_id}:0 {q(node['name'])}")
        lines += ["add_equipment_bonus = {", f"\tname = {bonus_id}", "\tbonus = {"]
        for equipment_type, modifiers in equipment_bonus["types"].items():
            lines.append(f"\t\t{equipment_type} = {{")
            lines.extend(f"\t\t\t{key} = {value:.2f}" for key, value in modifiers.items())
            lines.append("\t\t}")
        lines += ["\t}", "}"]

    for state_id, building, level, _recorded_slots in rec["buildings"]:
        lines.append(f"{state_id} = {{")
        lines.append(f"\tadd_extra_state_shared_building_slots = {level}")
        lines.append(f"\tadd_building_construction = {{ type = {building} level = {level} instant_build = yes }}")
        lines.append("}")
    return lines

def effect_preview_registry_entry(section, node, rec, loc, body=None):
    if body is None:
        body = effect_preview_body(section, node, rec, loc)
    return {
        "focus": node["id"],
        "name": node["name"],
        "effect_tooltip": "\n".join(body),
        "preview_independent_of_availability": True,
    }

def main():
    OUT.mkdir(exist_ok=True)
    sections = [s for s in DESIGN["sections"] if s["category"] in ("National life", "Economy")]
    records = [(s, n, INVENTORY[n["id"]]) for s in sections for n in s["nodes"] if n["id"] in INVENTORY]
    section_keys = {}
    for section, node, rec in records:
        keys = section_keys.setdefault(section["name"], set())
        keys.update(rec["modifiers"])
        for special in rec["special"]:
            if special == "energy_use_civs": keys.add("energy_use_modifier_civs")
    helpers, calls, dynmods, ideas, loc, availability, report = [], [], [], [], [], [], ["# IMPERIA COLD WAR — Japan staged effects implementation review", "", f"Generated from {len(records)} National life/Economy records.", "", "These fragments are staging only; they are not game-loaded.", ""]
    preview_registry = []
    for section, keys in section_keys.items():
        mod_id = f"{PREFIX}_{ident(section)}_permanent"
        dynmods += [f"{mod_id} = {{", "\ticon = GFX_idea_JAP_japanese_economy"]
        for key in sorted(keys): dynmods.append(f"\t{key} = {section_var(section, key)}")
        dynmods += ["}", ""]
        loc.append(f" {mod_id}:0 {q(section)}")
    loc.extend(f" {key}:0 {q(value)}" for key, value in NEW_PREVIEW_TOOLTIP_LOCALISATION.items())

    # Initialize durable pollution and energy spirits once. All focus helpers call this idempotent initializer.
    pollution_id = f"{PREFIX}_industrial_pollution_modifier"
    energy_id = f"{PREFIX}_energy_intensity_modifier"
    dynmods += [f"{pollution_id} = {{", "\ticon = GFX_idea_JAP_japanese_economy", f"\tstability_factor = {PREFIX}_pollution_stability", f"\thealth_cost_multiplier_modifier = {PREFIX}_pollution_health_cost", "}", ""]
    dynmods += [f"{energy_id} = {{", "\ticon = GFX_idea_JAP_japanese_economy", f"\tenergy_use_modifier_civs = {PREFIX}_energy_use_civs", f"\tcivilian_factories_productivity = {PREFIX}_energy_civilian_productivity", "}", ""]
    loc += [f" {pollution_id}:0 {q('Industrial Pollution Burden')}", f" {pollution_id}_desc:0 {q('Industrial pollution increases public health costs and places pressure on national stability.')}", f" {energy_id}:0 {q('Energy-Intensive Economy')}", f" {energy_id}_desc:0 {q('Japan’s industrial structure places additional demands on civilian electricity use while constraining factory productivity.')}"]
    init = [f"{PREFIX}_initialize_starting_modifiers = {{", f"\tif = {{ limit = {{ {' '.join(COUNTRY_GUARDS)} NOT = {{ has_country_flag = {PREFIX}_starting_modifiers_initialized }} }}", f"\t\tset_variable = {{ {PREFIX}_pollution_stability = -0.05 }}", f"\t\tset_variable = {{ {PREFIX}_pollution_health_cost = 0.08 }}", f"\t\tset_variable = {{ {PREFIX}_energy_use_civs = 0.10 }}", f"\t\tset_variable = {{ {PREFIX}_energy_civilian_productivity = -0.03 }}", f"\t\tadd_dynamic_modifier = {{ modifier = {pollution_id} }}", f"\t\tadd_dynamic_modifier = {{ modifier = {energy_id} }}", f"\t\tset_country_flag = {PREFIX}_starting_modifiers_initialized", "\t}", "}", ""]
    helpers += init
    unsupported = []
    special_energy_consumed = False
    for section, node, rec in records:
        focus_id = fid(node["id"])
        helper = f"{focus_id}_apply"
        receipt = f"{focus_id}_receipt"
        helper_start = len(helpers)
        guards = []
        for state_id, building, level, _recorded_slots in rec["buildings"]:
            guards.append(state_building_guard(state_id, building, level, level))
        focus_specific_guards = FOCUS_GUARDS.get(node["id"], [])
        limit_parts = [f"NOT = {{ has_country_flag = {receipt} }}", *COUNTRY_GUARDS, *focus_specific_guards, *guards]
        if rec.get("cost_gdp_share", 0):
            limit_parts.append("check_variable = { gdp_total > 0 }")
        limit = " ".join(limit_parts)
        helpers += [f"{helper} = {{", "\tif = {", f"\t\tlimit = {{ {limit} }}", f"\t\t{PREFIX}_initialize_starting_modifiers = yes"]
        if rec.get("cost_gdp_share", 0):
            helpers += [f"\t\tset_temp_variable = {{ treasury_change = {{ value = gdp_total multiply = -{rec['cost_gdp_share']:.5f} }} }}", "\t\tmodify_treasury_effect = yes"]
        elif rec["treasury_cost"]:
            helpers += [f"\t\tset_temp_variable = {{ treasury_change = -{rec['treasury_cost']:g} }}", "\t\tmodify_treasury_effect = yes"]
        # Permanent section modifier rewards.
        persistent = dict(rec["modifiers"])
        if rec["special"].get("energy_use_civs") is not None:
            helpers.append(f"\t\tadd_to_variable = {{ {PREFIX}_energy_use_civs = {rec['special']['energy_use_civs']:.5f} }}")
            special_energy_consumed = True
        for special, amount in rec["special"].items():
            key = SPECIAL_TO_POLLUTION.get(special)
            if key:
                target = f"{PREFIX}_pollution_stability" if key == "stability_factor" else f"{PREFIX}_pollution_health_cost"
                helpers.append(f"\t\tadd_to_variable = {{ {target} = {amount:.5f} }}")
            elif special != "energy_use_civs": unsupported.append((node["id"], f"special {special}={amount}"))
        for key, amount in persistent.items():
            secvar = section_var(section["name"], key)
            helpers.append(f"\t\tadd_to_variable = {{ {secvar} = {amount:.5f} }}")
        if persistent:
            mod_id = f"{PREFIX}_{ident(section['name'])}_permanent"
            helpers.append(f"\t\tif = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {mod_id} }} }} }} add_dynamic_modifier = {{ modifier = {mod_id} }} }}")
        if rec["special"].get("pollution_stability") or rec["special"].get("pollution_health"):
            helpers.append(f"\t\tif = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {pollution_id} }} }} }} add_dynamic_modifier = {{ modifier = {pollution_id} }} }}")
        if "energy_use_civs" in rec["special"]:
            helpers.append(f"\t\tif = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {energy_id} }} }} }} add_dynamic_modifier = {{ modifier = {energy_id} }} }}")
        for bonus in rec["bonuses"]:
            if bonus["category"] not in ("CAT_industry", "CAT_agriculture"):
                unsupported.append((node["id"], f"unverified research category {bonus['category']}"))
                continue
            bonus_id = f"{focus_id}_research"
            if not any(entry.startswith(f" {bonus_id}:0 ") for entry in loc):
                loc.append(f" {bonus_id}:0 {q(node['name'])}")
            helpers += ["\t\tadd_tech_bonus = {", f"\t\t\tname = {bonus_id}", f"\t\t\tbonus = {bonus['bonus']:.2f}", f"\t\t\tuses = {bonus['uses']}", f"\t\t\tcategory = {bonus['category']}", "\t\t}"]
        for index, bonus in enumerate(rec.get("doctrine_bonuses", [])):
            helpers += ["\t\tadd_doctrine_cost_reduction = {", f"\t\t\tname = {focus_id}_doctrine_{index}",
                        f"\t\t\tcost_reduction = {bonus['cost_reduction']:.2f}", f"\t\t\tuses = {bonus['uses']}",
                        f"\t\t\tcategory = {bonus['category']}", "\t\t}"]
        for index, equipment_bonus in enumerate(rec.get("equipment_bonuses", [])):
            helpers += ["\t\tadd_equipment_bonus = {", f"\t\t\tname = {focus_id}_equipment_{index}", "\t\t\tbonus = {"]
            for equipment_type, modifiers in equipment_bonus["types"].items():
                helpers.append(f"\t\t\t\t{equipment_type} = {{")
                helpers.extend(f"\t\t\t\t\t{key} = {value:.2f}" for key, value in modifiers.items())
                helpers.append("\t\t\t\t}")
            helpers += ["\t\t\t}", "\t\t}"]
        for state_id, building, level, slots in rec["buildings"]:
            helpers.append(f"\t\t{state_id} = {{")
            helpers.append(f"\t\t\tadd_extra_state_shared_building_slots = {level}")
            helpers.append(f"\t\t\tadd_building_construction = {{ type = {building} level = {level} instant_build = yes }}")
            helpers.append("\t\t}")
        helpers += [f"\t\tset_country_flag = {receipt}", "\t}", "}", ""]
        assert_bonus_entry_counts(node["id"], helpers[helper_start:], rec, "executor")
        preview_body = effect_preview_body(section, node, rec, loc)
        assert_bonus_entry_counts(node["id"], preview_body, rec, "focus preview")
        preview_registry.append(effect_preview_registry_entry(section, node, rec, loc, preview_body))
        calls += [f"# {node['name']} — staging snippet", "completion_reward = {", "\teffect_tooltip = {", *[f"\t\t{x}" for x in preview_body], "\t}", f"\thidden_effect = {{ {helper} = yes }}", "}", ""]
        visible_guards = [*focus_specific_guards]
        visible_guards.extend(state_building_guard(state_id, building, level, level)
                              for state_id, building, level, _recorded_slots in rec["buildings"])
        availability += [f"# {node['name']} — add inside this focus's availability", "available = {", "\thidden_trigger = {", *[f"\t\t{g}" for g in COUNTRY_GUARDS], "\t}"]
        if rec.get("cost_gdp_share", 0):
            availability += ["\thidden_trigger = { check_variable = { gdp_total > 0 } }"]
        availability += [*[f"\t{g}" for g in visible_guards], "}", ""]

    for rec in INVENTORY.values():
        if rec["matched"] == 0 and not rec["buildings"] and not rec["treasury_cost"] and not rec["special"] and not rec["bonuses"]:
            unsupported.append((rec["id"], "no executable effect was mapped"))
    zero_match = [r["id"] for r in INVENTORY.values() if r["matched"] == 0]
    report += [f"Emitted {len(records)} per-focus helpers and native display previews.", "", "## Implemented", "", "- Every focus preview is an unconditional native `effect_tooltip` sibling to the independently guarded `hidden_effect` payout. Preview bodies contain the same treasury changes, modifier-variable deltas, research bonuses, shared slots, and buildings as the payout without receipt or availability guards.", "- `national_economy_focus_effect_previews.json` is the machine-readable mapping for root focus-graph integration; its `effect_tooltip` value is the inner body keyed by design focus ID.", "- Treasury deductions use MD's `treasury_change` temporary variable and `modify_treasury_effect`; new domestic programme prices use a GDP share, a positive-GDP guard, and a computed numeric preview. No cash-on-hand affordability gate or direct debt manipulation is added.", "- Research bonuses use Japan's native `add_tech_bonus` shape for one `CAT_industry` or `CAT_agriculture` technology.", "- Four pollution focus improvements adjust the initialized persistent pollution modifier, which starts at stability −5% and health spending +8%.", "- The initialized energy modifier starts at civilian factory energy use +10% and civilian productivity −3%. The `efficient_factories` focus's −5% energy-use special modifies this same modifier variable.", "- Building caps and `shares_slots` behavior are transcribed from `common/buildings/00_buildings.txt`. All 14 inventory building types are state-level and use `state_max`; none use `province_max`.", "- Every granted building level adds one state shared building slot in the same state before construction, including infrastructure and other non-shared building types. This appears in both the display preview and guarded executor.", "- Every building helper and availability fragment separately checks current state ownership/control, the native `state_max` level cap, and any shared infrastructure keystone cap. `free_building_slots` is needed only for levels not covered by the slot grant; `include_locked = no` appears only for shared-slot building types.", "- Licensed Production requires `has_idea = COLDWAR_ni_licensed_armaments_programme`; Expand Microelectronics Capacity requires `has_tech = microchip_production_1`. Both requirements appear in availability and helper reward guards.", "- Technical `original_tag = JAP` and `IMP_is_1970_scenario = yes` checks are hidden in focus availability and retained in reward guards. Receipt flags are set after all scenario, focus-specific, ownership/control, and capacity guards pass.", "- Source audits reconciled all 353 percent tokens against 350 mapped modifiers and 3 tech bonuses; the four percentage-point pollution specials are mapped separately. All 37 building entries match their state names and quantities in the effect text.", "- Five `air_detection` rewards and three `planning_speed` rewards use percentage-valued native modifiers. `documentation/modifiers_documentation.md` lists these values, and `localisation/english/MD_dm_modifiers_l_english.yml` displays each with percent formatting.", "- Explicit building quantities are sourced from `common/buildings/00_buildings.txt`: fossil plants 2 GW / 3,360 fuel per week; fuel silos 200,000 fuel and 500 storage per level; reactors 4 GW / 40 nuclear fuel per week; renewable plants 0.5 GW.", "- Section modifiers and two starting modifiers have existing MD icons and English name keys.", "", "## Unsupported or unverified", f"- Inventory `matched = 0` (no ordinary modifier phrase matched) for: {', '.join('`' + i + '`' for i in zero_match)}. Each is emitted through its inventory cost, building, pollution special, or research bonus entry.", ""]
    if unsupported:
        report += [f"- `{node}`: {effect}." for node, effect in unsupported]
    else: report.append("- No unsupported special effects or research categories remain. Static emission does not establish engine validity.")
    report += ["", "## Source audit references", "", "- Installed HOI4 `documentation/triggers_documentation.md` says `free_building_slots` checks available construction levels and that `include_locked` is an optional parameter for buildings using shared slots.", "- Installed HOI4 `documentation/effects_documentation.md` defines `add_extra_state_shared_building_slots` as a STATE effect that adds shared slots. Native focus examples in `common/national_focus/05_japan.txt`, `05_china.txt`, and `05_belarus.txt` add slots before construction.", "- Installed HOI4 `documentation/dynamic_variables_documentation.md` defines `building_level@<building>` as the current level of that building in a state. `common/scripted_triggers/00_investment_scripted_triggers.txt` also uses this dynamic variable in `check_variable`.", "", "## Limits", "", "- Article 9 amendment focuses are outside the 212-record `effect_inventory.json`; their timed 365/730-day effects are not generated here.", "- The scripts pass source-level checks but were not parsed or exercised in a live HOI4 run.", "- The pollution/energy starting initializer must be called at country setup to show the starting spirits at game start. Each generated focus helper also calls it idempotently as a fallback.", "- Outputs remain staging fragments; no game-loaded file was changed."]

    localization_keys = [match.group(1) for entry in loc
                         if (match := re.match(r"\s*([A-Za-z0-9_.-]+):0\s+", entry))]
    duplicates = [key for key, count in Counter(localization_keys).items() if count != 1]
    if duplicates:
        raise ValueError("Duplicate generated national localization definitions: " + ", ".join(duplicates))

    (OUT / "national_economy_focus_effects_scripted_effects.txt").write_text("# IMPERIA COLD WAR — Cold War: Japan 1970 national policy rewards.\n" + "\n".join(helpers), encoding="utf-8")
    (OUT / "national_economy_focus_effects_dynamic_modifiers.txt").write_text("# IMPERIA COLD WAR — Cold War: Japan 1970 national policy modifiers.\n" + "\n".join(dynmods), encoding="utf-8")
    (OUT / "national_economy_focus_effects_timed_ideas.txt").write_text("# IMPERIA COLD WAR — Cold War: Japan 1970 staged timed ideas.\nideas = {\n}\n", encoding="utf-8")
    (OUT / "national_economy_focus_effect_calls.txt").write_text("# IMPERIA COLD WAR — Cold War: Japan 1970 staged focus snippets.\n" + "\n".join(calls), encoding="utf-8")
    (OUT / "national_economy_focus_availability_building_guards.txt").write_text("# IMPERIA COLD WAR — Cold War: Japan 1970 staged availability guards.\n" + "\n".join(availability), encoding="utf-8")
    (OUT / "starting_modifier_initialization_call.txt").write_text("# Add to Japan's game-start initialization to display both starting modifiers from day one.\n" + PREFIX + "_initialize_starting_modifiers = yes\n", encoding="utf-8")
    (OUT / "national_economy_focus_effects_l_english.yml").write_text("l_english:\n# IMPERIA COLD WAR — Japan national policy effect localization.\n" + "\n".join(loc) + "\n", encoding="utf-8-sig")
    (OUT / "national_economy_focus_effect_previews.json").write_text(json.dumps(preview_registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / "effects_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Staged {len(records)} focus records in {OUT}; {len(unsupported)} effects require follow-up.")

if __name__ == "__main__": main()
