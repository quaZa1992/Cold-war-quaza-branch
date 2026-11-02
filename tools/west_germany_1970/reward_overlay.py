# IMPERIA COLD WAR — West German national programme reward revision.
"""Apply bounded, one-time GER programme investments to the canonical tree."""

import re
import sys
from pathlib import Path

from cw_lib import P, LOC, money_gdp, tech
from tree import FOCUSES, core
from script_ast import emit, first, parse, values

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/german_reward_revision_20261027"))
import programme_assets


# Each entry is a decision-scale package, not a generic per-focus increment.
# Buildings are explicit named-state investments. Research and equipment bonuses
# use the installed Millennium Dawn APIs and are finite, one-use rewards.
PROGRAMMES = {
    # Bonn government and social-liberal institutional programme.
    "chancellery": dict(cost=.001, builds=[(39, "offices", 1)], tech=[("CAT_computing", .5, 1)], cores=[("bonn", {"pp": .02})]),
    "situation_centre": dict(cost=.001, tech=[("CAT_command_and_control_equipment", .5, 1)], cores=[("bonn", {"bureau": -.02})]),
    "bafoeg": dict(cost=.002, builds=[(39, "offices", 1), (43, "offices", 1)], tech=[("CAT_computing", .5, 1)], cores=[("west", {"research": .01})]),
    "works_constitution": dict(cost=.001, builds=[(39, "industrial_complex", 1)], tech=[("CAT_industry", .5, 1)], cores=[("modell", {"prod": .01, "social": .01})]),
    "codetermination": dict(cost=.002, builds=[(42, "industrial_complex", 1)], tech=[("CAT_industry", .5, 1)], cores=[("modell", {"fac": .02, "prod": .01})]),
    "modell_deutschland": dict(cost=.002, builds=[(39, "industrial_complex", 1), (42, "offices", 1)], tech=[("CAT_industry", .5, 1)], cores=[("modell", {"fac": .02, "tax": .01})]),
    "pension_reform": dict(cost=.002, builds=[(41, "offices", 1)], cores=[("modell", {"social": .01, "prod": .01})]),
    "grand_coalition": dict(cost=.002, builds=[(41, "industrial_complex", 1), (43, "offices", 1)], tech=[("CAT_industry", .5, 1)], cores=[("bonn", {"stab": .01})]),
    "barzel_social_market": dict(cost=.002, builds=[(43, "industrial_complex", 1)], tech=[("CAT_industry", .5, 1)], cores=[("modell", {"tax": .02, "prod": .01})]),

    # Growth policy, adjustment and the export economy.
    "social_market": dict(cost=.002, builds=[(39, "industrial_complex", 1), (42, "industrial_complex", 1)], tech=[("CAT_industry", .5, 1)], cores=[("modell", {"fac": .02, "tax": .01})]),
    "stimulus_1975": dict(cost=.003, builds=[(38, "industrial_complex", 1), (41, "offices", 1)], tech=[("CAT_industry", .5, 1)], cores=[("modell", {"prod": .02, "social": .01})]),
    "austerity_1975": dict(cost=.001, builds=[(41, "industrial_complex", 1)], tech=[("CAT_industry", .5, 1)], cores=[("modell", {"tax": .02, "social": -.01})]),
    "export_world_champion": dict(cost=.002, builds=[(42, "industrial_complex", 1), (39, "offices", 1)], tech=[("CAT_industry", .5, 1)], cores=[("modell", {"fac": .02, "tax": .01})]),
    "steel_crisis": dict(cost=.002, builds=[(39, "industrial_complex", 1)], tech=[("CAT_industry", .5, 1)], cores=[("modell", {"prod": .01, "fac": .01})]),
    "ruhr_structural_change": dict(cost=.002, builds=[(39, "offices", 1), (41, "offices", 1)], tech=[("CAT_computing", .5, 1)], cores=[("modell", {"prod": .01, "build": .02})]),
    "research_policy": dict(cost=.002, builds=[(42, "offices", 1), (41, "offices", 1)], tech=[("CAT_computing", .5, 1), ("CAT_electronics", .5, 1)], cores=[("west", {"research": .02})]),
    "airbus": dict(cost=.003, builds=[(40, "industrial_complex", 1), (42, "industrial_complex", 1)], tech=[("CAT_aircraft", .5, 1)], cores=[("modell", {"fac": .01})]),
    "microelectronics": dict(cost=.005, builds=[(42, "microchip_plant", 1)], tech=[("CAT_computing", .5, 1), ("CAT_electronics", .5, 1), ("CAT_microchip_production", .5, 1)], visible_tech=["microchip_production_1"], cores=[("west", {"research": .02}), ("modell", {"prod": .01, "social": .01})]),
    "vocational_training": dict(cost=.001, builds=[(38, "offices", 1)], tech=[("CAT_industry", .5, 1)], cores=[("modell", {"prod": .02})]),
    "single_market": dict(cost=.002, builds=[(39, "industrial_complex", 1)], tech=[("CAT_industry", .5, 1)], cores=[("west", {"trade": .02}), ("modell", {"fac": .01})]),

    # Energy security versus imports, coal costs, nuclear risk and conservation.
    "energy_programme": dict(cost=.002, tech=[("CAT_nuclear_reactors", .5, 1), ("CAT_construction", .5, 1)], cores=[("energie", {"gain": .02, "use": -.01})]),
    "kohlepfennig": dict(cost=.003, builds=[(39, "fossil_powerplant", 1)], tech=[("CAT_industry", .5, 1)], cores=[("energie", {"gain": .02, "fossil": .03, "use": .02})]),
    "century_contract": dict(cost=.002, builds=[(967, "fossil_powerplant", 1)], cores=[("energie", {"gain": .02, "fossil": .02, "use": .01})]),
    "nuclear_buildout": dict(cost=.005, builds=[(41, "nuclear_reactor", 1), (42, "nuclear_reactor", 1)], tech=[("CAT_nuclear_reactors", .5, 1)], cores=[("energie", {"nuclear": .05, "fossil": -.02, "use": -.01})]),
    "fast_breeder": dict(cost=.006, builds=[(39, "nuclear_reactor", 2)], tech=[("CAT_nuclear_reactors", .5, 1)], cores=[("energie", {"nuclear": .05, "use": .03})]),
    "nuclear_moratorium": dict(cost=.003, builds=[(37, "renewable_energy_infra", 1)], tech=[("CAT_electronics", .5, 1)], visible_tech=["fuel_silos"], cores=[("energie", {"renew": .04, "nuclear": -.02, "use": -.03})]),
    "gas_for_pipes": dict(cost=.002, builds=[(39, "industrial_complex", 1)], tech=[("CAT_industry", .5, 1)], cores=[("energie", {"gain": .02, "fossil": .02})]),
    "urengoy": dict(cost=.003, builds=[(39, "industrial_complex", 1), (42, "industrial_complex", 1)], tech=[("CAT_industry", .5, 1)], cores=[("energie", {"gain": .03, "fossil": .04})]),
    "energy_savings_act": dict(cost=.001, builds=[(41, "offices", 1)], tech=[("CAT_industry", .5, 1)], cores=[("energie", {"use": -.04})]),
    "renewable_research": dict(cost=.003, builds=[(37, "renewable_energy_infra", 1), (38, "renewable_energy_infra", 1)], tech=[("CAT_electronics", .5, 1)], visible_tech=["fuel_silos"], cores=[("energie", {"renew": .05, "fossil": -.02, "use": -.01})]),
    "feed_in_law": dict(cost=.003, builds=[(42, "renewable_energy_infra", 1)], tech=[("CAT_electronics", .5, 1)], visible_tech=["fuel_silos"], cores=[("energie", {"renew": .05, "use": -.02})]),
    "eco_tax": dict(cost=.001, builds=[(38, "offices", 1)], cores=[("energie", {"use": -.02}), ("modell", {"tax": .01})]),
    "atomkonsens": dict(cost=.001, builds=[(38, "offices", 1)], cores=[("energie", {"nuclear": -.04, "renew": .03, "use": -.02})]),

    # Alliance force design, education, readiness and arms family choices.
    "citizen_in_uniform": dict(cost=.002, builds=[(41, "arms_factory", 1)], cores=[("armee", {"org": .02, "equip": -.02}), ("modell", {"fac": .01})]),
    "army_structure_3": dict(cost=.002, builds=[(38, "arms_factory", 1)], tech=[("CAT_artillery", .5, 1)], equipment=[("artillery_equipment", -.05)], cores=[("armee", {"org": .02}), ("modell", {"fac": .01})]),
    "leber_modernisation": dict(cost=.003, builds=[(41, "arms_factory", 1)], tech=[("CAT_industry", .5, 1)], equipment=[("infantry_weapons_type", -.05)], cores=[("armee", {"org": .02, "equip": -.02}), ("modell", {"fac": .01})]),
    "leopard_2": dict(cost=.004, builds=[(42, "arms_factory", 1)], tech=[("CAT_tanks", .5, 1)], equipment=[("medium_tank_chassis", -.08)], cores=[("armee", {"org": .02, "equip": -.02}), ("modell", {"fac": .01})]),
    "army_structure_4": dict(cost=.002, builds=[(38, "offices", 1)], tech=[("CAT_command_and_control_equipment", .5, 1)], cores=[("armee", {"plan": .03, "xp": .01})]),
    "conscription_w15": dict(cost=.002, builds=[(38, "arms_factory", 1)], equipment=[("infantry_weapons_type", -.04)], cores=[("armee", {"org": .01, "xp": -.01, "equip": .01})]),
    "conscription_w18": dict(cost=.003, builds=[(38, "arms_factory", 1)], tech=[("CAT_infantry", .5, 1)], equipment=[("infantry_weapons_type", -.06)], cores=[("armee", {"org": .02, "xp": .01, "equip": .02})]),
    "home_defence": dict(cost=.002, builds=[(41, "arms_factory", 1)], tech=[("CAT_artillery", .5, 1)], equipment=[("artillery_equipment", -.04)], cores=[("armee", {"core": .02, "plan": .02})]),
    "army_of_unity": dict(cost=.003, builds=[(43, "arms_factory", 1)], tech=[("CAT_tanks", .5, 1)], equipment=[("medium_tank_chassis", -.05)], cores=[("armee", {"org": .02, "core": .02})]),
    "army_structure_5": dict(cost=.002, builds=[(41, "offices", 1)], tech=[("CAT_command_and_control_equipment", .5, 1)], cores=[("armee", {"org": .02, "xp": .01})]),
    "tornado": dict(cost=.004, builds=[(42, "arms_factory", 1)], tech=[("CAT_aircraft", .5, 1)], equipment=[("medium_plane_airframe", -.04)], cores=[("armee", {"plan": .02, "equip": .01}), ("modell", {"fac": .01})]),
    "bundeswehr_universities": dict(cost=.002, builds=[(1080, "offices", 1)], tech=[("CAT_command_and_control_equipment", .5, 1)], cores=[("armee", {"xp": .02, "org": .01})]),
    "jaeger_90": dict(cost=.004, builds=[(42, "arms_factory", 1)], tech=[("CAT_aircraft", .5, 1)], equipment=[("medium_plane_airframe", -.04)], cores=[("armee", {"org": .02, "plan": .02}), ("modell", {"fac": .01})]),
    "patriot": dict(cost=.003, builds=[(41, "arms_factory", 1)], tech=[("CAT_anti_air", .5, 1)], equipment=[("AA_Equipment", -.05)], cores=[("armee", {"core": .02, "equip": -.01})]),
    "type_209": dict(cost=.003, builds=[(1080, "dockyard", 1)], tech=[("CAT_submarines", .5, 1)], equipment=[("submarine", -.06)], cores=[("armee", {"equip": -.01})]),
    "f122_frigates": dict(cost=.003, builds=[(1080, "dockyard", 1)], tech=[("CAT_frigates", .5, 1)], equipment=[("frigate", -.06)], cores=[("armee", {"equip": .01})]),
    "nato_awacs": dict(cost=.003, builds=[(38, "offices", 1)], tech=[("CAT_aircraft", .5, 1), ("CAT_electronics", .5, 1)], cores=[("armee", {"plan": .02}), ("west", {"research": .01})]),
    "nuclear_sharing_role": dict(cost=.002, builds=[(41, "arms_factory", 1)], tech=[("CAT_nuclear_weapons", .5, 1)], cores=[("armee", {"plan": .02, "equip": .01})]),
    "forward_defence": dict(cost=.003, builds=[(39, "arms_factory", 1)], tech=[("CAT_tanks", .5, 1), ("CAT_artillery", .5, 1)], equipment=[("medium_tank_chassis", -.04), ("artillery_equipment", -.04)], cores=[("armee", {"org": .02, "plan": .02})]),
    "civil_defence": dict(cost=.002, builds=[(41, "offices", 1)], tech=[("CAT_construction", .5, 1)], cores=[("armee", {"core": .03}), ("bonn", {"stab": .01})]),
    "peace_dividend_defence": dict(cost=.001, builds=[(41, "offices", 1)], tech=[("CAT_industry", .5, 1)], cores=[("armee", {"core": .03, "equip": -.02}), ("modell", {"tax": .01})]),
}

_APPLIED = False
NEW_LOC_KEYS = set()
PARTY_GATES = {
    "bafoeg": "western_social_democrats_are_in_power = yes",
    "works_constitution": "western_social_democrats_are_in_power = yes",
    "barzel_social_market": "western_conservatism_are_in_power = yes",
}
LEGACY_BUILDINGS = {
    "nuclear_buildout": [(41, "nuclear_reactor"), (42, "nuclear_reactor")],
    "fast_breeder": [(39, "nuclear_reactor"), (43, "nuclear_reactor")],
    "renewable_research": [(37, "renewable_energy_infra"), (38, "renewable_energy_infra")],
}



def _repair_state_slots(effect):
    """Add one shared slot per original fixed-state building level, before construction."""
    rows = parse(effect)
    repairs = []

    def repair_state(body, state):
        builds = values(body, "add_building_construction")
        levels = sum(int(first(build, "level", 0)) for build in builds if isinstance(build, list))
        slots = [(i, int(value)) for i, (key, _op, value) in enumerate(body)
                 if key == "add_extra_state_shared_building_slots"]
        granted = sum(value for _i, value in slots)
        if levels > granted:
            missing = levels - granted
            first_build = next(i for i, (key, _op, _value) in enumerate(body)
                               if key == "add_building_construction")
            if slots:
                slot_index, amount = slots[0]
                key, op, _value = body[slot_index]
                body[slot_index] = (key, op, str(amount + missing))
            else:
                body.insert(first_build, ("add_extra_state_shared_building_slots", "=", str(missing)))
            repairs.append({"state": int(state), "building_levels": levels,
                            "building_types": [str(first(build, "type")) for build in builds if isinstance(build, list)],
                            "slots_added": missing})
        for key, _op, child in body:
            if not isinstance(child, list):
                continue
            if key.isdigit():
                repair_state(child, key)
            else:
                visit(child)

    def visit(block):
        for key, _op, child in block:
            if not isinstance(child, list):
                continue
            if key.isdigit():
                repair_state(child, key)
            else:
                visit(child)

    visit(rows)
    return emit(rows), repairs


def _original_buildings(effect):
    """Read fixed-state building grants so the combined transaction is gated."""
    pattern = re.compile(
        r"(?P<state>\d+)\s*=\s*\{\s*(?:add_extra_state_shared_building_slots\s*=\s*\d+\s*)?"
        r"add_building_construction\s*=\s*\{\s*type\s*=\s*(?P<type>[A-Za-z0-9_]+)"
        r"\s+level\s*=\s*(?P<level>\d+)", re.S)
    found = [(int(m.group("state")), m.group("type"), int(m.group("level")))
             for m in pattern.finditer(effect)]
    count = len(re.findall(r"add_building_construction\s*=\s*\{", effect))
    if count != len(found):
        raise ValueError(f"Could not scope every original fixed-state building grant: {count} found, {len(found)} mapped")
    return found


def _equipment_effects(key, entries):
    return "\n".join(
        f"add_equipment_bonus = {{ name = {P}_{key}_{i} bonus = {{ {family} = {{ build_cost_ic = {value} }} }} }}"
        for i, (family, value) in enumerate(entries, 1)
    )


def _display(key, package):
    rows = [money_gdp(-package["cost"]), programme_assets.bundle_effects(package.get("builds", []))]
    rows += [tech(category, bonus, uses, name=f"{P}_{key}_bonus_{i}")
             for i, (category, bonus, uses) in enumerate(package.get("tech", []), 1)]
    rows += [_equipment_effects(key, package["equipment"])] if package.get("equipment") else []
    rows += [core(name, **mods) for name, mods in package.get("cores", [])]
    return "\n".join(row for row in rows if row)


def apply():
    """Add each package once to both its always-visible preview and guarded payout."""
    global _APPLIED
    if _APPLIED:
        return
    before_loc = set(LOC)
    by_key = {focus["key"]: focus for focus in FOCUSES}
    missing = set(PROGRAMMES) - by_key.keys()
    if missing:
        raise KeyError("Reward overlay references missing focus IDs: " + ", ".join(sorted(missing)))
    for key, package in PROGRAMMES.items():
        focus = by_key[key]
        party_gate = PARTY_GATES.get(key)
        if party_gate and party_gate not in focus["avail"]:
            focus["avail"] = " ".join(part for part in (focus["avail"], party_gate) if part)
        flag = f"{P}_{key}_reward_receipt"
        builds = programme_assets.coalesce(package.get("builds", []))
        asset_gate = programme_assets.bundle_guards(builds)
        required_techs = list(package.get("visible_tech", []))
        explicit_tech_gate = " ".join(f"has_tech = {tech_id}" for tech_id in required_techs)
        visible_parts = [part for part in (asset_gate, explicit_tech_gate) if part]
        focus["visible_avail"] = " ".join(visible_parts)
        # GDP and internal routing remain hidden. Sites, native caps, and enabling
        # technology are visible and are repeated in the all-or-nothing execution gate.
        gdp_gate = "check_variable = { gdp_total > 0 }"
        focus["hidden_avail"] = gdp_gate
        original = focus["reward"]
        for state, building in LEGACY_BUILDINGS.get(key, []):
            clause = (f"if = {{ limit = {{ {state} = {{ is_owned_by = ROOT }} }} {state} = {{ "
                      f"add_extra_state_shared_building_slots = 1 add_building_construction = "
                      f"{{ type = {building} level = 1 instant_build = yes }} }} }}")
            if clause not in original:
                raise ValueError(f"Expected legacy building clause missing for {key}/{state}/{building}")
            original = original.replace(clause, "")
        original, slot_repairs = _repair_state_slots(original)
        if slot_repairs:
            focus["overlay_slot_repairs"] = slot_repairs
        original_builds = _original_buildings(original)
        all_builds = programme_assets.coalesce(original_builds + package.get("builds", []))
        asset_gate = programme_assets.bundle_guards(all_builds)
        focus["visible_avail"] = " ".join(part for part in (asset_gate, explicit_tech_gate) if part)
        display = _display(key, package)
        payout = "\n".join(part for part in (original, display) if part)
        execution_gates = ["original_tag = GER", "IMP_is_1970_scenario = yes", focus["avail"], gdp_gate, asset_gate, explicit_tech_gate,
                           f"NOT = {{ has_country_flag = {flag} }}"]
        focus["reward"] = (f"effect_tooltip = {{\n{payout}\n}}\n"
                            f"hidden_effect = {{ if = {{ limit = {{ {' '.join(execution_gates)} }} "
                            f"set_country_flag = {flag} hidden_effect = {{ {payout} }} }} }}")
    _APPLIED = True
    NEW_LOC_KEYS.update(set(LOC) - before_loc)

