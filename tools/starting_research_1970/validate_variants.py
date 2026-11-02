# IMPERIA COLD WAR — Independent January 1970 historical equipment design validation.
"""Check regional evidence, native designer compatibility and bounded runtime behavior."""

import argparse
import collections
import itertools
import json
import math
import re
import sys
import traceback
import zipfile
from datetime import date, datetime, timezone
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlsplit

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GAME = Path("E:/SteamLibrary/steamapps/common/Hearts of Iron IV")
sys.path.insert(0, str(HERE))
from catalog import catalogue, first, parse
from tools.starting_research_1970.validate import (DLCS, State, condition, dlc_condition,
    extract_block as research_block, augment_rendered_technologies, scalar, sha)

PROJECT = "IMPERIA COLD WAR"
REGIONS = ("europe", "asia", "africa", "americas_oceania", "usa")
MARKER = "# IMPERIA COLD WAR — January 1970 historical equipment variants."
BEGIN, END = MARKER + " BEGIN", MARKER + " END"
GUN_BANDS = {
    "mdcw_tank_gun_1940": (37, 75), "mdcw_tank_gun_1943": (75, 85),
    "tank_small_cannon": (90, 95), "module_mdcw_90mm_tank_gun_1945": (90, 95),
    "tank_small_medium_cannon": (100, 105), "tank_medium_cannon": (115, 125),
}
PHYSICAL_SOURCES = {
    "tank_gun_bands": "localisation/english/tank_modules_l_english.yml",
    "MiG21_delta": "https://airandspace.si.edu/collection-objects/mikoyan-gurevich-mig-21f-13-fishbed-c/nasm_A19930354000",
    "MirageIII_delta_single_engine": "https://www.dassault-aviation.com/en/passion/aircraft/military-dassault-aircraft/mirage-iii/",
    "Tu95_swept_quad_prop": "https://uacrussia.ru/en/aircraft/lineup/special/tu-95ms/",
    "BMP1_steel": "https://www.army.mil/article/220341/ria_self_guided_tour_bmp_1_armored_personnel_carrier",
}
HISTORICAL_FRAME_IDS = {
    "mdcw_early_piston_attack_1940_model", "mdcw_early_jet_bomber_1950_model",
    "mdcw_early_carrier_attack_1950_model",
}


def historical_role_ids(equipment):
    source = ROOT / "common/units/equipment/MD_w_COLDWAR_1970_historical_role_frames.txt"
    if not source.is_file():
        return set()
    bases = {key for container, op, rows in parse(source.read_text(encoding="utf-8-sig"))
             if container == "equipments" for key, op, body in rows if isinstance(body, list)}
    native_roles = ROOT / "common/units/equipment/MD_x_plane_airframes.txt"
    return bases | {key for key, row in equipment.items() if row.get("generated_from") in bases
                    and Path(row["file"]) == native_roles}


def late_frame_reference_fields(rows):
    """Inheritance must be established before mission, module or statistic overrides."""
    metadata = {"year", "priority", "abbreviation", "derived_variant_name", "active"}
    references = [i for i, (key, op, value) in enumerate(rows) if key in {"archetype", "parent"}]
    dependent = [key for i, (key, op, value) in enumerate(rows)
                 if key not in metadata | {"archetype", "parent"}
                 and references and i < max(references)]
    return dependent


def frame_dependency_precedes(dependency_path, dependency_index, frame_path, frame_index):
    if dependency_path == frame_path:
        return dependency_index < frame_index
    return dependency_path.name.casefold() < frame_path.name.casefold()


def audit_native_frame_load_order(equipment, require):
    """Focused regression for the concrete malformed-reference native load failure.

    The engine failed when the custom file preceded the MD duplicate archetypes
    and its mdcw static donor. Follow their actual source definitions rather than
    treating an ID's presence in an unordered catalogue as sufficient.
    """
    files = list((ROOT / "common/units/equipment").glob("*COLDWAR_1970_historical_design_frames.txt"))
    require(len(files) == 1, "historical_frame_file_has_no_stale_duplicate", files=[p.name for p in files])

    @lru_cache(None)
    def declarations(filename):
        path = Path(filename)
        result = {}
        if not path.is_file():
            return result
        ordinal = 0
        for container, op, rows in parse(path.read_text(encoding="utf-8-sig")):
            if container in {"equipments", "duplicate_archetypes", "duplicate_equipments"}:
                for key, op, body in rows:
                    if isinstance(body, list):
                        result[key] = (ordinal, body)
                        ordinal += 1
        return result

    visited, edges = set(), []
    mission_source = ROOT / "common/units/equipment/MD_x_plane_airframes.txt"
    mission_reference = {}
    for donor in ("cas1", "strategic_bomber1"):
        entry = declarations(str(mission_source)).get(donor)
        tokens = members(first(entry[1], "allow_mission_type", [])) if entry else []
        require(bool(tokens), "historical_frame_native_mission_reference_present", donor=donor)
        mission_reference[donor] = tokens
    native_missions = set().union(*(set(tokens) for tokens in mission_reference.values()))

    def visit(typ, trail=()):
        if typ in visited:
            return
        if not require(typ not in trail, "historical_frame_inheritance_has_no_cycle", type=typ, trail=list(trail)):
            return
        if not require(typ in equipment, "historical_frame_dependency_exists", type=typ):
            return
        row = equipment[typ]
        path = Path(row["file"])
        entry = declarations(str(path)).get(typ)
        if not entry and row.get("generated_from"):
            origin = row["generated_from"]
            role = row.get("archetype")
            role_entry = declarations(str(path)).get(role)
            base = scalar(first(role_entry[1], "archetype")) if role_entry else None
            valid_duplication = bool(base and origin.startswith(base)
                                     and typ == role + origin[len(base):])
            require(valid_duplication, "generated_frame_has_actual_native_prefix_duplication",
                    type=typ, origin=origin, role=role, base=base)
            if valid_duplication:
                # Native for_each emits the role immediately after its actual
                # duplicate-archetype declaration has been established.
                entry = (role_entry[0] + 0.5,
                         [("archetype", "=", role), ("parent", "=", origin)])
        if not require(bool(entry), "historical_frame_dependency_has_actual_source_declaration", type=typ, file=str(path)):
            return
        ordinal, body = entry
        if typ in HISTORICAL_FRAME_IDS:
            require(not late_frame_reference_fields(body), "historical_frame_references_precede_stats_and_missions",
                    type=typ, premature_fields=late_frame_reference_fields(body))
            supplied_missions = members(first(body, "allow_mission_type", []))
            require(set(supplied_missions) <= native_missions,
                    "historical_frame_uses_actual_native_mission_names", type=typ,
                    unknown=sorted(set(supplied_missions)-native_missions),
                    references=mission_reference)
        for field in ("archetype", "parent"):
            reference = scalar(first(body, field))
            if not reference or reference == typ:
                continue
            if not require(reference in equipment, "historical_frame_dependency_exists", type=typ, field=field, dependency=reference):
                continue
            dependency_path = Path(equipment[reference]["file"])
            dependency = declarations(str(dependency_path)).get(reference)
            if not dependency and equipment[reference].get("generated_from"):
                generated = equipment[reference]
                role_entry = declarations(str(dependency_path)).get(generated.get("archetype"))
                base = scalar(first(role_entry[1], "archetype")) if role_entry else None
                origin = generated["generated_from"]
                if base and origin.startswith(base) and reference == generated["archetype"] + origin[len(base):]:
                    dependency = (role_entry[0] + 0.5, [])
            if not require(bool(dependency), "historical_frame_dependency_has_actual_source_declaration",
                           type=typ, dependency=reference, file=str(dependency_path)):
                continue
            require(frame_dependency_precedes(dependency_path, dependency[0], path, ordinal),
                    "historical_frame_dependency_loads_first", type=typ, field=field, dependency=reference,
                    dependency_file=dependency_path.name, frame_file=path.name)
            edges.append({"type": typ, "field": field, "dependency": reference,
                          "dependency_file": dependency_path.name, "frame_file": path.name})
            visit(reference, trail + (typ,))
        visited.add(typ)

    for typ in sorted(HISTORICAL_FRAME_IDS | historical_role_ids(equipment)):
        visit(typ)
    require(not frame_dependency_precedes(Path("MD_x_plane_airframes.txt"), 0,
                                         Path("COLDWAR_1970_historical_design_frames.txt"), 0),
            "negative_control_rejects_original_early_frame_filename")
    require(bool(late_frame_reference_fields(parse("air_range = 700 archetype = medium_plane_cas_airframe"))),
            "negative_control_rejects_stats_before_archetype")
    require(bool(late_frame_reference_fields(parse("archetype = heavy_tank_amphibious_chassis module_slots = inherit parent = mdcw_utility_helicopter_1955_model"))),
            "negative_control_rejects_slots_before_parent")
    require(not {"logistics_strike", "strategic_bombing"} & native_missions,
            "negative_control_rejects_engine_rejected_mission_aliases")
    return edges


def audit_historical_frame_enum(require, equipment):
    relative = "common/script_enums.txt"
    path = ROOT / relative
    raw = path.read_bytes()
    source = raw.decode("utf-8")
    require(not raw.startswith(b"\xef\xbb\xbf"), "historical_frame_enum_utf8_without_bom")
    registrations = members(first(parse(source), "script_enum_equipment_bonus_type", []))
    registered_frames = HISTORICAL_FRAME_IDS | historical_role_ids(equipment)
    for typ in sorted(registered_frames):
        require(registrations.count(typ) == 1, "historical_frame_registered_exactly_once_in_native_enum",
                type=typ, count=registrations.count(typ))
    baselines = []
    for sidecar in sorted(HERE.glob("component_before_hashes*.json")):
        record = json.loads(sidecar.read_text(encoding="utf-8"))
        if relative in record.get("before_sha256", {}):
            baselines.append((sidecar, record))
    if not require(len(baselines) == 1, "historical_frame_enum_has_one_archived_original",
                   sidecars=[p.name for p, record in baselines]):
        return {"file": relative}
    sidecar, record = baselines[0]
    require(record.get("project") == PROJECT, "historical_frame_enum_archive_project_marker")
    with zipfile.ZipFile(record["archive"]) as archive:
        prior_raw = archive.read(relative)
    require(sha(prior_raw) == record["before_sha256"][relative], "historical_frame_enum_archive_hash_preserved")
    before = prior_raw.decode("utf-8-sig").replace("\r\n", "\n")
    actual_rows = parse(source)
    preserved_rows = [(key, op, [(k, o, v) for k, o, v in body
                              if not (k == "_bare" and scalar(v) in registered_frames)])
                      if key == "script_enum_equipment_bonus_type" else (key, op, body)
                      for key, op, body in actual_rows]
    require(preserved_rows == parse(before), "historical_frame_enum_preserves_every_original_registration")
    # The generator inserts one bounded list and a file-start notice; existing
    # MD notices and all unrelated source text must survive that insertion.
    stripped = re.sub(r"\A# IMPERIA COLD WAR — January 1970 equipment enum integration; existing MD registrations retained\.\n", "", source)
    role_marker = re.escape("# IMPERIA COLD WAR — Native role derivatives for historical early airframes.")
    stripped = re.sub(r"(?ms)^[ \t]*" + role_marker + r" BEGIN\n.*?^[ \t]*" + role_marker + r" END\n", "", stripped)
    frame_names = "(?:" + "|".join(re.escape(typ) for typ in sorted(HISTORICAL_FRAME_IDS)) + ")"
    stripped = re.sub(r"\n[ \t]*# IMPERIA COLD WAR — Historical January 1970 design frames\.\n(?:[ \t]*"
                      + frame_names + r"[ \t]*\n){3}", "", stripped)
    require(stripped == before, "historical_frame_enum_preserves_original_source_and_notice")
    return {"file": relative, "baseline_sidecar": sidecar.name, "archive": record["archive"],
            "before_sha256": sha(prior_raw), "current_sha256": sha(raw)}


def physical_fit(key, model, module_definitions, require):
    """Independent physical facts, beyond syntactically valid native slots."""
    fitted, specs = model.get("modules", {}), model.get("historical_specs", {})
    # Source measurements remain separate from abstract native designer levels.
    # Reject malformed/contradictory measurements without manufacturing missing
    # historical numbers or equating millimetres with in-game armor points.
    for field in ("engine_power_hp", "road_speed_kmh", "combat_mass_t", "hull_front_mm",
                  "turret_front_mm", "armor_min_mm", "armor_max_mm"):
        if field in specs:
            number = specs[field]
            require(isinstance(number, (int, float)) and not isinstance(number, bool)
                    and math.isfinite(number) and number > 0,
                    "physical_measurement_is_positive_finite_number", model=key, field=field, actual=number)
    if all(isinstance(specs.get(field), (int, float)) for field in ("armor_min_mm", "armor_max_mm")):
        require(specs["armor_min_mm"] <= specs["armor_max_mm"],
                "physical_minimum_protection_not_above_maximum", model=key)
    calibrated = {k for k in model.get("upgrades", {})
                  if k in {"tank_nsb_armor_upgrade", "tank_nsb_engine_upgrade"}}
    if calibrated:
        explanation = str(specs.get("native_mapping_rationale", "")) + " ".join(model.get("notes", []))
        require(len(explanation.strip()) >= 80,
                "calibrated_native_levels_have_mapping_rationale", model=key, fields=sorted(calibrated))
    actual_gun = specs.get("gun_mm")
    gun_module = fitted.get("main_armament_slot")
    if isinstance(actual_gun, (int, float)) and gun_module in GUN_BANDS:
        def distance(band):
            return max(band[0]-actual_gun, 0, actual_gun-band[1])
        difference = distance(GUN_BANDS[gun_module])
        closest = min(distance(band) for band in GUN_BANDS.values())
        require(difference <= closest + 1, "physical_tank_gun_uses_closest_historical_calibre_band",
                model=key, actual_mm=actual_gun, module=gun_module, module_band=GUN_BANDS[gun_module])
    engine = fitted.get("engine_type_slot", fitted.get("fixed_ship_engine_slot"))
    if engine in module_definitions:
        description = str(specs.get("engine", "")).lower()
        category = module_definitions[engine].get("category") or ""
        if any(term in description for term in ("petrol", "gasoline")):
            require("gasoline" in category or "gasoline" in engine, "physical_original_petrol_engine", model=key, module=engine)
        if "diesel" in description:
            require("diesel" in category or "diesel" in engine, "physical_original_diesel_engine", model=key, module=engine)
        if "piston" in description or "radial" in description:
            require("piston" in category or "prop" in category, "physical_original_piston_engine", model=key, module=engine)
        if "turbojet" in description or "jet" in description and "jet ranger" not in description:
            require("jet" in category or "light" in category, "physical_original_jet_propulsion", model=key, module=engine)
        if "prop" in description and "propulsion" not in description:
            require("prop" in category, "physical_original_propeller_propulsion", model=key, module=engine)
        expected_count = None
        for pattern, count in [(r"\b(?:quad|four)\b", 4), (r"\b(?:double|two|twin)\b", 2),
                               (r"\b(?:single|one)\b", 1), (r"^\s*([124])\s+(?:small\s+)?turbo", None)]:
            found = re.search(pattern, description)
            if found:
                expected_count = count if count else int(found.group(1))
                break
        actual_count = next((number for token, number in [("single", 1), ("double", 2), ("twin", 2), ("quad", 4), ("six", 6), ("eight", 8)] if token in category), None)
        if actual_count is None and category.startswith("helicopter_") and any(token in category for token in ("piston", "turbine")):
            actual_count = 1
        if expected_count and actual_count:
            require(expected_count == actual_count, "physical_actual_aircraft_engine_count", model=key,
                    expected=expected_count, fitted=actual_count, module=engine)
    armor = fitted.get("armor_type_slot")
    if armor and armor != "empty":
        material = str(specs.get("armor", "")).lower()
        material = re.sub(r"\b(?:no|without)\s+(?:composite|aluminium|aluminum|era)\b", "", material)
        if "composite" in armor:
            require("composite" in material, "physical_composite_only_when_actual", model=key, module=armor, actual=material)
        if "alum" in armor:
            require("alum" in material, "physical_aluminium_only_when_actual", model=key, module=armor, actual=material)
        if "steel" in material and "alum" not in material and "composite" not in material:
            require("steel" in armor or armor in {"tank_cast_armor", "tank_welded_armor", "tank_riveted_armor"},
                    "physical_steel_vehicle_uses_steel", model=key, module=armor)
    wing = fitted.get("wingform_type_slot")
    name = model.get("name", "")
    if wing:
        expected = None
        if re.search(r"MiG[- ]?21|Mirage III|\bJ[- ]?7\b|Vulcan|Draken|Delta Dart|Delta Dagger", name, re.I):
            expected = "wing_delta"
        elif re.search(r"Tu[- ]?95|Tu[- ]?16|\bH[- ]?6[A-Z]?\b", name, re.I):
            expected = "wing_swept"
        elif re.search(r"Canberra|\bB[- ]?57|Il[- ]?28|\bH[- ]?5\b|Vampire|Jet Provost|Fouga|MB[- ]?326|Impala|Texan|Trojan|Nomad", name, re.I):
            expected = "wing_straight"
        if expected:
            require(wing == expected, "physical_known_aircraft_wing_planform", model=key, aircraft=name,
                    expected=expected, fitted=wing)
    calibres = specs.get("gun_calibres_mm") or ([actual_gun] if isinstance(actual_gun, (int, float)) else [])
    optional_gun = fitted.get("fixed_gun_slot")
    if optional_gun == "module_mdcw_mixed_aircraft_cannons_1945" and calibres:
        require(23 in calibres and 37 in calibres or max(calibres) == 37,
                "physical_mixed_23_37mm_fit", model=key, actual_calibres=calibres)
    if optional_gun and optional_gun.startswith("module_mdcw_aircraft_"):
        if calibres and max(calibres) <= 15:
            require(optional_gun == "module_mdcw_aircraft_machine_guns_1940", "physical_aircraft_machine_gun_fit", model=key)
        elif calibres and max(calibres) <= 23:
            require(optional_gun == "module_mdcw_aircraft_cannon_20mm", "physical_aircraft_20_23mm_fit", model=key)
        elif calibres and max(calibres) <= 30:
            require(optional_gun == "module_mdcw_aircraft_cannon_30mm", "physical_aircraft_30mm_fit", model=key)


def members(value):
    if isinstance(value, list):
        return [scalar(v) for k, op, v in value if k == "_bare"]
    return [scalar(value)] if value else []


def extract_block(source):
    if source.count(BEGIN) != 1 or source.count(END) != 1:
        raise ValueError("Expected exactly one bounded historical variant block")
    start, end = source.index(BEGIN), source.index(END)
    if end <= start:
        raise ValueError("Variant markers reversed")
    return source[source.index("\n", start) + 1:end], source[:start] + source[end + len(END):]


def all_combinations():
    for bits in itertools.product((False, True), repeat=3):
        yield {name for name, bit in zip(DLCS, bits) if bit}


def selected(model, dlcs):
    if set(model.get("requires_dlc", [])) <= dlcs:
        return model
    fallback = model.get("fallback")
    if not fallback:
        return None
    result = dict(model)
    result.update(fallback)
    result["modules"] = fallback.get("modules", {})
    return result


def signature(record):
    return (record["name"], record["type"],
            tuple(sorted(record.get("modules", {}).items())),
            tuple(sorted(record.get("upgrades", {}).items())))


def native_module_slots(typ, equipment, seen=()):
    """Resolve explicit native inheritance without inventing slots on static parents."""
    if typ not in equipment or typ in seen:
        return []
    row = equipment[typ]
    slots = first(row["direct_rows"], "module_slots")
    if isinstance(slots, list):
        return slots
    parent = row.get("parent")
    if slots == "inherit":
        return native_module_slots(parent or row.get("archetype"), equipment, seen + (typ,))
    if parent:
        return native_module_slots(parent, equipment, seen + (typ,))
    return []


def modular_type(typ, equipment, seen=()):
    """An inherit token without a designable parent does not create a designer."""
    return bool(native_module_slots(typ, equipment, seen))


def module_type_effect(module, modules, field, seen=()):
    if module not in modules or module in seen:
        return set()
    row = modules[module]
    direct = first(row["direct_rows"], field)
    if direct is not None:
        return set(members(direct))
    return module_type_effect(row.get("parent"), modules, field, seen + (module,))


def is_component_bundle(record):
    return (not record.get("folders") and record.get("allow") == [("always", "=", "no")]
            and record.get("year") == 1969
            and bool(record.get("enable_equipment_modules") or record.get("enable_equipments"))
            and not record.get("special_projects"))


def type_enablers(typ, equipment):
    """Exact bare type or its usable generated role parent, never its archetype."""
    if typ not in equipment:
        return set()
    row = equipment[typ]
    result = set(row.get("enable_techs", []))
    parent = row.get("generated_from")
    if parent in equipment:
        inherited = set(equipment[parent].get("enable_techs", []))
        if typ.startswith("heavy_tank_amphibious_chassis"):
            inherited = {t for t in inherited if not t.startswith("nsb_attack_helicopter_tech_")}
        result.update(inherited)
    return result


@lru_cache(None)
def native_folder_availability():
    result = {}
    for base in (GAME, ROOT):
        for path in sorted((base / "common/technology_tags").glob("*.txt")):
            for container, op, rows in parse(path.read_text(encoding="utf-8-sig")):
                if container == "technology_folders":
                    for folder, op, block in rows:
                        if isinstance(block, list):
                            result[folder] = first(block, "available", [])
    return result


def active_technology(record, dlcs):
    if dlc_condition(record.get("allow_branch", []), dlcs) is False:
        return False
    folders = record.get("folders", [])
    availability = native_folder_availability()
    return not folders or any(dlc_condition(availability.get(folder, []), dlcs) is not False
                              for folder in folders)


def active_enablers(candidates, technologies, dlcs):
    """Both technology branch and native research-folder DLC gates must be active."""
    return {t for t in candidates if t in technologies and active_technology(technologies[t], dlcs)}


def ordinary_pre1970_enablers(typ, equipment, technologies, dlcs, bundles):
    active = active_enablers(type_enablers(typ, equipment)-bundles, technologies, dlcs)
    frame_year = int(float(equipment[typ].get("year") or 9999))
    return {t for t in active if (technologies[t].get("year") is not None
                                 and technologies[t]["year"] <= 1969)
            or (technologies[t].get("year") is None and frame_year <= 1969)}


def load_data(require):
    models, countries, hashes = {}, {}, {}
    for region in REGIONS:
        path = HERE / (region + "_variants.json")
        if not require(path.is_file(), "regional_file_present", file=path.name):
            continue
        raw = path.read_bytes()
        hashes[path.name] = sha(raw)
        require(not raw.startswith(b"\xef\xbb\xbf"), "input_utf8_without_bom", file=path.name)
        data = json.loads(raw.decode("utf-8"))
        require(data.get("project") == PROJECT and data.get("cutoff") == "1970-01-01",
                "input_metadata", file=path.name)
        for key, model in data["models"].items():
            require(key not in models, "unique_model_id", model=key, file=path.name)
            models[key] = dict(model, _file=path.name)
        for tag, ids in data["countries"].items():
            require(tag not in countries, "unique_country_assignment", tag=tag, file=path.name)
            countries[tag] = ids
        source = HERE / (region + "_variants_sources.md")
        require(source.is_file() and source.read_text(encoding="utf-8-sig").startswith(PROJECT),
                "regional_provenance_record", file=source.name)
    return models, countries, hashes


class VariantState(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.designs, self.creation_log = [], []


def execute(rows, state, equipment, modules, technologies, require):
    """Interpret only the generated monotonic initialization language, in source order."""
    previous_if = None
    for key, operator, value in rows:
        if key == "limit":
            continue
        if key == "if":
            previous_if = condition(first(value, "limit", []), state)
            if previous_if:
                execute(value, state, equipment, modules, technologies, require)
        elif key == "else_if":
            if previous_if is None:
                raise ValueError("else_if without if")
            if not previous_if and condition(first(value, "limit", []), state):
                execute(value, state, equipment, modules, technologies, require)
                previous_if = True
        elif key == "else":
            if previous_if is None:
                raise ValueError("else without if")
            if not previous_if:
                execute(value, state, equipment, modules, technologies, require)
            previous_if = None
        elif key == "set_country_flag":
            state.flags.add(scalar(value))
            previous_if = None
        elif key == "set_technology":
            for tech, assignment, level in value:
                if tech == "popup":
                    require(level == "no", "technology_popup_suppressed", tag=state.tag)
                    continue
                require(assignment == "=" and level == "1", "monotonic_technology_assignment",
                        tag=state.tag, technology=tech)
                require(tech in technologies, "runtime_technology_exists", tag=state.tag, technology=tech)
                state.techs.add(tech)
            previous_if = None
        elif key == "create_equipment_variant":
            fields = {k: v for k, op, v in value}
            allowed = {"name", "type", "modules", "upgrades", "parent_version", "icon", "obsolete",
                       "allow_without_tech", "mark_older_equipment_obsolete", "version_name"}
            require(set(fields) <= allowed, "only_reviewed_variant_fields", tag=state.tag,
                    fields=sorted(set(fields)-allowed))
            typ, name = scalar(fields.get("type")), scalar(fields.get("name"))
            fitted = {slot: scalar(mod) for slot, op, mod in fields.get("modules", [])}
            upgrades = {upgrade: int(level) for upgrade, op, level in fields.get("upgrades", [])}
            if typ in equipment:
                frame = equipment[typ]
                enablers = active_enablers(type_enablers(typ, equipment), technologies, state.dlcs)
                if modular_type(typ, equipment):
                    require(fields.get("allow_without_tech") != "yes", "no_modular_allow_without_tech",
                            tag=state.tag, name=name, type=typ)
                if modular_type(typ, equipment) or fields.get("allow_without_tech") != "yes":
                    require(bool(enablers & state.techs), "bare_hull_researched_before_creation",
                            tag=state.tag, name=name, type=typ, dlcs=sorted(state.dlcs),
                            active_possible_enablers=sorted(enablers))
                for mod in fitted.values():
                    if mod == "empty" or mod not in modules:
                        continue
                    possible = set(modules[mod].get("enable_techs", []))
                    enabling = active_enablers(possible, technologies, state.dlcs)
                    require(not possible or bool(enabling & state.techs), "fitted_module_known_before_creation",
                            tag=state.tag, name=name, module=mod, possible_enablers=sorted(enabling))
            state.designs.append(signature({"name": name, "type": typ, "modules": fitted, "upgrades": upgrades}))
            state.creation_log.append({"name": name, "type": typ, "known_technologies": sorted(state.techs)})
            previous_if = None
        else:
            raise ValueError("Unexpected generated variant effect: " + key)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", action="store_true", help="Use rendered compiler output")
    parser.add_argument("--data-only", action="store_true", help="Validate design inputs while compiler integration is being written")
    args = parser.parse_args(argv)
    diagnostics, counts = [], collections.Counter()
    report = {"project": PROJECT, "feature": "Independent worldwide historical variant validation",
              "mode": "data-only" if args.data_only else "preview" if args.preview else "installed",
              "created_utc": datetime.now(timezone.utc).isoformat(),
              "evidence_level": "Native source compatibility, documented dates and bounded interpreter; no live engine or save-load test.",
              "bare_type_policy": "Every creation requires a known enabler active under both native technology branch and research-folder DLC gates. Exact service bundles may enable the native MD frame of a documented pre1970 operated model without granting the later general research generation. Legacy fixed types without a native-contract mapping still require no usable ordinary unlock. A common receipt for the same shared static model is additionally permitted only when ordinary native coverage has a genuine gap in at least one applicable DLC configuration; fully mirrored ordinary unlocks must be used instead. Nominal later hull years still require specific pre1970 model evidence."}

    def require(test, category, **details):
        counts[category] += 1
        if not test:
            diagnostics.append({"severity": "error", "category": category, **details})
        return bool(test)

    try:
        models, countries, hashes = load_data(require)
        equipment = json.loads((HERE / "equipment_catalog.json").read_text(encoding="utf-8"))["equipment"]
        report["historical_frame_dependency_edges"] = audit_native_frame_load_order(equipment, require)
        report["historical_frame_enum_provenance"] = audit_historical_frame_enum(require, equipment)
        modules = json.loads((HERE / "module_catalog.json").read_text(encoding="utf-8"))["modules"]
        technologies, duplicates = catalogue()
        require(not duplicates, "unique_native_technologies", duplicates=duplicates)
        # Negative controls establish that the interpreter cannot quietly accept
        # stockpile effects or create an unresearched modular bare hull.
        rejected = False
        try:
            execute(parse("add_equipment_to_stockpile = { type = infantry_weapons_1 amount = 1 }"),
                    VariantState("EGY", DLCS), equipment, modules, technologies, require)
        except ValueError:
            rejected = True
        require(rejected, "negative_control_rejects_unreviewed_asset_effect")
        negative_diagnostics = []
        execute(parse('create_equipment_variant = { name = "Validator negative control" type = medium_tank_chassis_mdcw_1955 }'),
                VariantState("EGY", DLCS), equipment, modules, technologies,
                lambda test, category, **details: negative_diagnostics.append(category) if not test else None)
        require("bare_hull_researched_before_creation" in negative_diagnostics,
                "negative_control_detects_missing_bare_hull_research")
        # Static towed guns and transport models also need an active unlock.
        # A known legacy technology cannot satisfy an NSB/BBA branch merely
        # because its ID appears in the same global catalogue.
        inactive_equipment = {"__inactive_bare_type__": {
            "enable_techs": ["__inactive_unlock__"], "direct_rows": [],
            "generated_from": None, "parent": None}}
        inactive_technologies = {"__inactive_unlock__": {
            "allow_branch": [("NOT", "=", [("has_dlc", "=", '"No Step Back"')])]}}
        inactive_diagnostics = []
        execute(parse('create_equipment_variant = { name = "Inactive branch negative control" type = __inactive_bare_type__ }'),
                VariantState("EGY", {"No Step Back"}, techs={"__inactive_unlock__"}),
                inactive_equipment, {}, inactive_technologies,
                lambda test, category, **details: inactive_diagnostics.append(category) if not test else None)
        require("bare_hull_researched_before_creation" in inactive_diagnostics,
                "negative_control_rejects_inactive_dlc_static_unlock")
        require(not active_technology({"allow_branch": [], "folders": ["bomber_folder"]},
                                      {"By Blood Alone"}),
                "negative_control_rejects_inactive_native_research_folder")
        static_parent_control = {
            "__archetype__": {"direct_rows": [("module_slots", "=", [("test_slot", "=", [])])]},
            "__static_parent__": {"direct_rows": [], "archetype": "__archetype__"},
            "__invalid_inherit__": {"direct_rows": [("module_slots", "=", "inherit")],
                                    "parent": "__static_parent__", "archetype": "__archetype__"},
        }
        require(not modular_type("__invalid_inherit__", static_parent_control),
                "negative_control_rejects_static_parent_designer_inheritance")
        require(module_type_effect("module_mdcw_unguided_bombs_1945", modules, "add_equipment_type") == {"cas"}
                and set(equipment["mdcw_small_plane_airframe_gen1"]["type"]) != {"cas"},
                "negative_control_detects_original_cas_primary_role_mismatch")
        guarded = parse('if = { limit = { IMP_is_1970_scenario = yes NOT = { has_country_flag = receipt } } set_country_flag = receipt }')
        outside_control = VariantState("EGY", DLCS, scenario=False)
        execute(guarded, outside_control, equipment, modules, technologies, require)
        require(not outside_control.flags, "negative_control_respects_scenario_gate")
        history = {p.stem[:3]: p for p in (ROOT / "history/countries").glob("*.txt")}
        require(len(history) == len(countries) == 400 and set(history) == set(countries),
                "exact_400_country_coverage", missing=sorted(set(history)-set(countries)), extra=sorted(set(countries)-set(history)))
        bundles = {t for t, v in technologies.items() if is_component_bundle(v)}
        upgrade_defs = {}
        for base in (GAME, ROOT):
            for path in (base / "common/units/equipment/upgrades").glob("*.txt"):
                for container, op, rows in parse(path.read_text(encoding="utf-8-sig")):
                    if container == "upgrades":
                        for key, op, block in rows:
                            if isinstance(block, list):
                                upgrade_defs[key] = first(block, "max_level")

        @lru_cache(None)
        def merged(typ):
            row = equipment[typ]
            parent = row.get("parent") or row.get("archetype")
            before = merged(parent) if parent in equipment and parent != typ else []
            direct = {k for k, op, v in row["direct_rows"] if v != "inherit"}
            return [entry for entry in before if entry[0] not in direct] + [entry for entry in row["direct_rows"] if entry[2] != "inherit"]

        @lru_cache(None)
        def live_rows(filename):
            path = Path(filename)
            rows = parse(path.read_text(encoding="utf-8-sig"))
            return {key: block for container, op, children in rows
                    if container in {"equipments", "equipment_modules", "duplicate_archetypes"}
                    for key, op, block in children if isinstance(block, list)}

        @lru_cache(None)
        def module_load_gate(module):
            native = modules[module]
            matches = [first(children, "limit", []) for container, op, children in
                       parse(Path(native["file"]).read_text(encoding="utf-8-sig"))
                       if container == "equipment_modules" and any(k == module for k, op, v in children)]
            return matches[-1] if matches else []

        def fresh_record(key, record, generated=False):
            native = live_rows(record["file"])
            if generated:
                require(record.get("generated_from") in equipment and record.get("archetype") in equipment,
                        "generated_role_has_native_bare_and_archetype", type=key)
            else:
                require(key in native and json.loads(json.dumps(native[key])) == record["direct_rows"],
                        "catalogue_matches_live_native_definition", id=key, file=record["file"])

        def fit_check(key, record, original):
            typ = record["type"]
            if not require(typ in equipment, "valid_equipment_id", model=key, type=typ):
                return
            frame = equipment[typ]
            fresh_record(typ, frame, bool(frame.get("generated_from")))
            year = frame.get("year")
            require(not year or int(float(year)) <= 1969 or bool(original.get("type_year_exception")),
                    "equipment_not_future", model=key, type=typ, year=year)
            allowed_upgrades = set(members(first(merged(typ), "upgrades", [])))
            for upgrade, level in record.get("upgrades", {}).items():
                require(upgrade in upgrade_defs, "native_upgrade_id", model=key, upgrade=upgrade)
                maximum = upgrade_defs.get(upgrade)
                require(isinstance(level, int) and not isinstance(level, bool) and level >= 0 and
                        (maximum is None or level <= int(float(maximum))), "native_upgrade_range",
                        model=key, upgrade=upgrade, level=level, maximum=maximum)
                require(not allowed_upgrades or upgrade in allowed_upgrades, "upgrade_allowed_on_type",
                        model=key, type=typ, upgrade=upgrade)
            fitted = {s: m for s, m in record.get("modules", {}).items() if m != "empty"}
            is_modular = modular_type(typ, equipment)
            slots = {name: {"categories": members(first(block, "allowed_module_categories", [])),
                            "required": first(block, "required"), "default_module": first(block, "default_module")}
                     for name, op, block in native_module_slots(typ, equipment) if isinstance(block, list)}
            require(is_modular or not fitted, "static_equipment_has_no_modules", model=key, type=typ)
            override = scalar(first(merged(typ), "type_override"))
            if is_modular and override == "fixed_main_weapon_slot" and override in fitted:
                primary_module = fitted[override]
                primary_types = module_type_effect(primary_module, modules, "add_equipment_type")
                # Native plane archetypes override the equipment category from
                # this primary slot. Slot-category legality alone does not make
                # an interceptor frame with a CAS primary module buildable.
                require(not primary_types or primary_types == set(frame.get("type", [])),
                        "primary_air_module_matches_selected_native_role", model=key, type=typ,
                        primary_module=primary_module, required_role=sorted(primary_types),
                        selected_role=frame.get("type", []))
            if not is_modular and "plane" in (typ + str(frame.get("archetype", ""))):
                declared = first(frame["direct_rows"], "allow_mission_type")
                if declared is not None:
                    require(set(members(declared)) != {"training"},
                            "static_historical_plane_has_operational_missions", model=key, type=typ)
            dynamic = collections.defaultdict(set)
            for module in fitted.values():
                if module in modules:
                    for slot, categories in modules[module].get("allowed_module_categories", {}).items():
                        dynamic[slot].update(categories)
            flags = set(frame.get("type", []))
            archetype = equipment.get(frame.get("archetype"), {})
            flags.update(archetype.get("type", []))
            exact = flags - {"armor"}
            exact = exact or ({"armor"} if "armor" in flags else flags)
            for slot, module in fitted.items():
                if not require(slot in slots, "native_module_slot", model=key, type=typ, slot=slot):
                    continue
                if not require(module in modules, "native_module_id", model=key, module=module):
                    continue
                native = modules[module]
                fresh_record(module, native)
                allowed_categories = set(slots[slot]["categories"]) | dynamic[slot]
                require(bool(({native.get("category")} | set(native.get("categories", []))) & allowed_categories),
                        "module_category_fits_slot", model=key, slot=slot, module=module,
                        module_category=native.get("category"), allowed=sorted(allowed_categories))
                allowed_types = set(members(native.get("allow_equipment_type", [])))
                forbidden = set(members(native.get("forbid_equipment_type", [])))
                forbidden_exact = set(members(native.get("forbid_equipment_type_exact_match")))
                # allow_equipment_type adds special roles to the normal armor role;
                # native standard tank cannons explicitly add anti_tank this way.
                require(not allowed_types or bool(allowed_types & flags) or "armor" in flags, "module_allows_equipment_type",
                        model=key, module=module, frame_types=sorted(flags), allowed_types=sorted(allowed_types))
                require(not (forbidden & flags), "module_no_forbidden_type", model=key, module=module, forbidden=sorted(forbidden & flags))
                require(not (forbidden_exact & exact), "module_no_forbidden_exact_type", model=key, module=module, forbidden=sorted(forbidden_exact & exact))
                restrictions = first(native.get("direct_rows", []), "forbid_equipment_type_exact_match_for_category", [])
                fitted_categories = {modules[m].get("category") for m in fitted.values() if m in modules}
                for category_name, op, forbidden_type in restrictions:
                    require(category_name not in fitted_categories or scalar(forbidden_type) not in exact,
                            "module_no_forbidden_exact_type_for_fitted_category", model=key, module=module,
                            module_category=category_name, forbidden_type=forbidden_type)
                # Hidden module knowledge must not conceal a genuinely later physical component.
                years = [y for tech, y in native.get("tech_years", {}).items() if tech not in bundles and isinstance(y, int)]
                exception = original.get("module_exceptions", {}).get(module)
                require(not years or min(years) <= 1969 or isinstance(exception, str) and len(exception.strip()) >= 20,
                        "component_not_future_or_specific_documented_exception", model=key, module=module,
                        earliest_original_research_year=min(years) if years else None, exception=exception)
            for slot, spec in slots.items():
                require(spec.get("required") != "yes" or slot in fitted or spec.get("default_module") not in (None, "empty"),
                        "required_designer_slot_filled", model=key, type=typ, slot=slot)
            if slots and any("plane" in value for value in (typ, frame.get("archetype") or "")):
                require("By Blood Alone" in original.get("requires_dlc", []), "air_designer_dlc_gate", model=key)
            if slots and "tank" in typ:
                require("No Step Back" in original.get("requires_dlc", []), "land_designer_dlc_gate", model=key)

        used = set()
        for key, model in models.items():
            require(bool(model.get("name")) and not re.search("[\u2013\u2014]", model.get("name", "")), "valid_design_name", model=key)
            require(model.get("origin_tag") in history, "valid_original_producer_tag", model=key, origin=model.get("origin_tag"))
            try:
                require(date.fromisoformat(model.get("service_by", "")) < date(1970, 1, 1), "documented_service_before_cutoff", model=key, date=model.get("service_by"))
            except ValueError:
                require(False, "valid_service_date", model=key, date=model.get("service_by"))
            sources = model.get("sources", [])
            require(bool(sources) and all(urlsplit(s).scheme in {"http", "https"} and urlsplit(s).netloc for s in sources), "model_has_source_references", model=key)
            require(bool(model.get("historical_specs")) and isinstance(model.get("notes", []), list), "model_has_historical_fitting_record", model=key)
            require(set(model.get("requires_dlc", [])) <= set(DLCS), "supported_dlc_requirement", model=key)
            fit_check(key, model, model)
            physical_fit(key, model, modules, require)
            if "fallback" in model:
                fallback = selected(model, set())
                if not model.get("requires_dlc"):
                    fallback = dict(model)
                    fallback.update(model["fallback"])
                    fallback["modules"] = model["fallback"].get("modules", {})
                fit_check(key + ":fallback", fallback, model)
        for tag, ids in countries.items():
            require(len(ids) == len(set(ids)), "no_duplicate_model_assignment", tag=tag)
            for key in ids:
                require(key in models, "assigned_model_exists", tag=tag, model=key)
                used.add(key)
            for dlcs in all_combinations():
                chosen = [selected(models[k], dlcs) for k in ids if k in models]
                identities = [(v["name"], v["type"]) for v in chosen if v]
                require(len(identities) == len(set(identities)), "unique_name_per_country_type_dlc", tag=tag, dlcs=sorted(dlcs))
        require(set(models) == used, "all_model_records_have_operators", unused=sorted(set(models)-used))

        runtime_counts = {}
        if not args.data_only:
            from tools.starting_research_1970 import build, variants as variant_compiler
            outputs, manifest = build.outputs()
            augment_rendered_technologies(outputs, technologies, require)
            bundles = {t for t, v in technologies.items() if is_component_bundle(v)}
            # Pending source output, rather than stale on-disk catalogues, defines
            # which exact components are known when creating preview variants.
            for tech, record in technologies.items():
                for module in record.get("enable_equipment_modules", []):
                    if module in modules and tech not in modules[module]["enable_techs"]:
                        modules[module]["enable_techs"].append(tech)
                for typ in record.get("enable_equipments", []):
                    if typ in equipment and tech not in equipment[typ]["enable_techs"]:
                        equipment[typ]["enable_techs"].append(tech)
            require(callable(getattr(variant_compiler, "load_variants", None)), "compiler_variant_export_exists")
            if callable(getattr(variant_compiler, "load_variants", None)):
                compiled_models, compiled_countries = variant_compiler.load_variants()
                require(set(compiled_models) == set(models) and compiled_countries == countries,
                        "compiler_reads_exact_regional_assignments")
            for tag, ids in sorted(countries.items()):
                path = history[tag]
                source = outputs[path] if args.preview else path.read_text(encoding="utf-8")
                require(source == outputs[path], "variant_runtime_matches_compiler", tag=tag)
                own, stripped = extract_block(source)
                research, ignored = research_block(source)
                own_rows = parse(own)
                require(source.index(BEGIN) > source.index("researched national technology baseline. END"), "research_precedes_variant_block", tag=tag)
                require(len(own_rows) == 1 and own_rows[0][0] == "if", "single_guarded_variant_transaction", tag=tag)
                rows_1970 = [v for k, op, v in parse(source) if k == "1970.1.1"]
                require(bool(rows_1970) and parse(research) + own_rows == rows_1970[0][:len(parse(research))+len(own_rows)],
                        "both_new_blocks_precede_legacy_initializers", tag=tag)
                design_counts = []
                for dlcs in all_combinations():
                    state = VariantState(tag, dlcs)
                    execute(parse(research), state, equipment, modules, technologies, require)
                    research_flags = set(state.flags)
                    execute(own_rows, state, equipment, modules, technologies, require)
                    require(state.flags == research_flags | {"COLDWAR_1970_historical_variants_assigned"},
                            "only_historical_variant_receipt_flag_set", tag=tag, dlcs=sorted(dlcs))
                    wanted = collections.Counter(signature(v) for k in ids if (v := selected(models[k], dlcs)))
                    require(collections.Counter(state.designs) == wanted, "independent_variant_interpreter",
                            tag=tag, dlcs=sorted(dlcs), actual=len(state.designs), expected=sum(wanted.values()))
                    before = (set(state.techs), set(state.flags), list(state.designs))
                    execute(own_rows, state, equipment, modules, technologies, require)
                    require((state.techs, state.flags, state.designs) == before, "variant_replay_idempotent", tag=tag, dlcs=sorted(dlcs))
                    state.techs.add("__later_research_sentinel__")
                    execute(own_rows, state, equipment, modules, technologies, require)
                    require(state.techs == before[0] | {"__later_research_sentinel__"} and state.designs == before[2],
                            "variant_replay_preserves_saved_progress", tag=tag, dlcs=sorted(dlcs))
                    outside = VariantState(tag, dlcs, scenario=False, flags={"__old_flag__"}, techs={"__old_tech__"})
                    execute(own_rows, outside, equipment, modules, technologies, require)
                    require(not outside.designs and outside.flags == {"__old_flag__"} and outside.techs == {"__old_tech__"},
                            "later_scenarios_receive_no_variant_grants", tag=tag, dlcs=sorted(dlcs))
                    for tech in state.techs - {"__later_research_sentinel__"}:
                        record = technologies[tech]
                        require(record["year"] is None or record["year"] <= 1969, "runtime_no_future_research", tag=tag, technology=tech)
                        require(active_technology(record, dlcs), "runtime_native_dlc_branch_and_folder", tag=tag, technology=tech, dlcs=sorted(dlcs))
                        if tech in bundles:
                            for module in record.get("enable_equipment_modules", []):
                                require(module in modules and dlc_condition(module_load_gate(module), dlcs) is not False,
                                        "service_module_definition_loaded_for_dlc", tag=tag, technology=tech,
                                        module=module, dlcs=sorted(dlcs))
                            evidenced = {}
                            for key in ids:
                                design = selected(models[key], dlcs)
                                if not design:
                                    continue
                                typ = design["type"]
                                evidenced[typ] = models[key]
                                # Native role duplication needs its own raw
                                # prefix-correct base as well as the role hull.
                                # Permit only this immediate related copied
                                # base, never a generic parent/archetype family.
                                origin = equipment.get(typ, {}).get("generated_from")
                                if origin in equipment and Path(equipment[origin]["file"]).name == "MD_w_COLDWAR_1970_historical_role_frames.txt":
                                    base = equipment[origin].get("archetype")
                                    role = equipment[typ].get("archetype")
                                    related = bool(base and role and origin.startswith(base)
                                                   and typ == role + origin[len(base):])
                                    require(related, "service_related_base_has_exact_native_role_model_evidence",
                                            tag=tag, type=typ, base=origin, model=key)
                                    if related:
                                        evidenced[origin] = models[key]
                            for typ in record.get("enable_equipments", []):
                                if not require(typ in evidenced and typ in equipment, "service_bare_type_has_country_model_evidence", tag=tag, technology=tech, type=typ):
                                    continue
                                model = evidenced[typ]
                                year = equipment[typ].get("year")
                                require(not year or int(float(year)) <= 1969 or bool(model.get("type_year_exception")), "service_bare_type_is_historically_pre1970", tag=tag, technology=tech, type=typ, year=year)
                                usable = ordinary_pre1970_enablers(typ, equipment, technologies, dlcs, bundles)
                                native_service = (typ == model['type'] and model.get('native_md_contract') in {
                                    'modular_aircraft','modular_ground','modular_ship','fixed_transport_helicopter'})
                                if native_service:
                                    # Native MD dates generic physical frames later than many actual
                                    # imported designs. An exact operated frame is not evidence that
                                    # its operator developed the whole national research generation.
                                    require(Path(equipment[typ]['file']).name.startswith('MD_'),
                                            'service_import_uses_native_md_production_type',tag=tag,type=typ)
                                    require(bool(model.get('native_md_original_type')) and model.get('service_by','9999') < '1970-01-01',
                                            'service_import_has_preserved_historical_mapping',tag=tag,type=typ)
                                    require(is_component_bundle(record),
                                            'service_import_has_no_industry_or_broad_technology_effect',tag=tag,type=typ)
                                else:
                                    if record.get("allow_branch"):
                                        require(not usable, "service_bare_type_only_when_no_existing_pre1970_unlock", tag=tag, type=typ, existing_options=sorted(usable))
                                    else:
                                        # Explicit reviewed policy for a shared static
                                        # model: one exact common bare-type receipt is
                                        # permitted if ordinary unlock coverage has a
                                        # real gap in at least one applicable DLC set.
                                        coverage = [(combination, ordinary_pre1970_enablers(
                                            typ, equipment, technologies, combination, bundles))
                                            for combination in all_combinations()]
                                        missing = [sorted(combination) for combination, options in coverage if not options]
                                        # A genuinely dead/unlinked evidenced frame
                                        # already satisfies the original policy in
                                        # every branch, including modular ships.
                                        # Only partially covered common types need
                                        # the later static-model exception.
                                        if any(options for combination, options in coverage):
                                            shared = [models[k] for k in ids if models[k]["type"] == typ
                                                      and not models[k].get("requires_dlc")]
                                            require(bool(shared) and not modular_type(typ, equipment),
                                                    "common_bare_type_is_same_evidenced_static_model", tag=tag, type=typ)
                                        require(bool(missing), "common_bare_type_has_native_dlc_unlock_gap",
                                                tag=tag, type=typ, current_options=sorted(usable))
                    design_counts.append(len(before[2]))
                runtime_counts[tag] = {"min_designs": min(design_counts), "max_designs": max(design_counts)}
        report.update({"countries": len(countries), "models": len(models), "assignments": sum(map(len, countries.values())),
                       "countries_with_designs": sum(bool(v) for v in countries.values()), "input_sha256": hashes,
                       "native_component_bundles": sorted(bundles), "runtime_countries_checked": runtime_counts,
                       "physical_audit_reference_points": PHYSICAL_SOURCES,
                       "native_files_sha256": {filename: sha(Path(filename).read_bytes()) for filename in sorted({equipment[v["type"]]["file"] for v in models.values() if v["type"] in equipment} | {modules[m]["file"] for v in models.values() for m in v.get("modules", {}).values() if m in modules})}})
    except Exception as error:
        require(False, "validator_exception", error_type=type(error).__name__, message=str(error), traceback=traceback.format_exc())
    errors = len(diagnostics)
    diagnostics.append({"severity": "warning", "category": "native_engine_not_run", "detail": "Static and bounded behavior checks cannot establish live designer acceptance, gameplay balance or multiplayer/save-load behavior."})
    report.update({"status": "failed" if errors else "passed_data_checks" if args.data_only else "passed",
                   "error_count": errors, "warning_count": 1, "check_counts": dict(sorted(counts.items())),
                   "diagnostics": diagnostics, "finished_utc": datetime.now(timezone.utc).isoformat()})
    (HERE / "variant_validation.json").write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps({k: report.get(k) for k in ("project", "mode", "status", "countries", "models", "assignments", "error_count", "warning_count")}))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
