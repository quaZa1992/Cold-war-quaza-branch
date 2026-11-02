# IMPERIA COLD WAR — Isolated Chile 1970 native engine probe.
"""Explicit prepare/run runner for a private HOI4 profile under E:.

Preparation freezes game-facing files without traversing reparse points and
creates a private fixture overlay. Importing this module performs no I/O.
Only the subprocess launched by ``--run`` may be stopped by this runner.
"""
from __future__ import annotations

from pathlib import Path, PurePosixPath
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
GAME_CANDIDATES = (
    Path(r"E:/SteamLibrary/steamapps/common/Hearts of Iron IV"),
    Path(r"C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV"),
)
GAME = next((p for p in GAME_CANDIDATES if (p / "hoi4.exe").is_file()), GAME_CANDIDATES[-1])
RUNTIME = Path(r"E:/HOI4_Mod_Tools/mdcoldwar/runtime/chile_1970")
HERE = Path(__file__).resolve().parent
PREFIX = "ICW_CHL_NATIVE"
MARK = "# IMPERIA COLD WAR — Private Chile 1970 engine probe fixture.\n"
# Native defines this MD build at 80 shared slots. 82 covers the known
# neighbouring build cap while keeping the count exact for this state.
MAX_SHARED_SLOTS = 82
COPY_DIRS = ("common", "events", "history", "interface", "localisation", "map", "portraits", "tutorial", "descriptions", "scenario_tests")
KNOWN_LINK_DIRS = ("gfx", "music", "sound")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def assert_private(path: Path) -> Path:
    base = RUNTIME.resolve()
    resolved = path.resolve()
    if resolved == base or not resolved.is_relative_to(base):
        raise ValueError(f"Expected a child of the private Chile runtime root: {path}")
    return resolved


def destination(base: Path, relative: str | PurePosixPath) -> Path:
    key = PurePosixPath(str(relative).replace("\\", "/"))
    if key.is_absolute() or ".." in key.parts or ":" in str(key):
        raise ValueError(f"Unsafe relative fixture path: {relative}")
    result = base.joinpath(*key.parts)
    if not result.resolve().is_relative_to(base.resolve()):
        raise ValueError(f"Fixture path leaves private root: {relative}")
    return result


def write(base: Path, relative: str, value: str | bytes) -> Path:
    target = destination(base, relative)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(value if isinstance(value, bytes) else value.encode("utf-8"))
    return target


def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def is_reparse(path: Path, entry_stat=None) -> bool:
    metadata = entry_stat if entry_stat is not None else path.stat(follow_symlinks=False)
    return bool(getattr(metadata, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT) or path.is_symlink()


def copy_tree(source: Path, target: Path, hashes: dict[str, str], last_progress: list[float]) -> None:
    if is_reparse(source):
        raise ValueError("Refusing to traverse a reparse point: " + str(source))
    target.mkdir(parents=True, exist_ok=True)
    with os.scandir(source) as entries:
        for entry in entries:
            src = Path(entry.path)
            meta = entry.stat(follow_symlinks=False)
            if is_reparse(src, meta):
                raise ValueError("Refusing to traverse a reparse point: " + str(src))
            dst = target / entry.name
            if entry.is_dir(follow_symlinks=False):
                copy_tree(src, dst, hashes, last_progress)
            elif entry.is_file(follow_symlinks=False):
                original = src.read_bytes()
                shutil.copy2(src, dst)
                if sha(dst.read_bytes()) != sha(original) or sha(src.read_bytes()) != sha(original):
                    raise ValueError("Source changed while freezing: " + str(src))
                hashes[src.relative_to(ROOT).as_posix()] = sha(original)
            if time.monotonic() - last_progress[0] >= 20:
                last_progress[0] = time.monotonic()
                print(json.dumps({"phase": "snapshot", "files": len(hashes), "directory": str(source)}), flush=True)


def walk_files(source: Path, prefix: str = ""):
    if is_reparse(source):
        raise ValueError("Refusing to inventory a reparse point: " + str(source))
    with os.scandir(source) as entries:
        for entry in entries:
            src = Path(entry.path)
            meta = entry.stat(follow_symlinks=False)
            if is_reparse(src, meta):
                raise ValueError("Refusing to inventory a reparse point: " + str(src))
            rel = f"{prefix}/{entry.name}" if prefix else entry.name
            if entry.is_dir(follow_symlinks=False):
                yield from walk_files(src, rel)
            elif entry.is_file(follow_symlinks=False):
                yield src, rel


def inventory_tree(source: Path, hashes: dict[str, str]) -> None:
    for path, rel in walk_files(source):
        hashes[rel] = sha(path.read_bytes())


def drift(base: Path, hashes: dict[str, str]) -> list[str]:
    changed = []
    for relative, digest in hashes.items():
        path = destination(base, relative)
        if not path.is_file() or sha(path.read_bytes()) != digest:
            changed.append(relative)
    return changed


def link_known_asset(snapshot: Path, name: str, links: list[dict[str, str]]) -> None:
    source = ROOT / name
    target = snapshot / name
    if not source.is_dir() or target.exists() or is_reparse(source):
        raise ValueError("Known asset link is not a plain source directory: " + str(source))
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cmd.exe", "/c", "mklink", "/J", str(target), str(source)], check=True,
                   capture_output=True, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    links.append({"path": name, "source": str(source), "target": str(target), "purpose": "read-only game asset directory"})


def game_processes() -> list[str]:
    if os.name != "nt":
        return []
    p = subprocess.run(["tasklist.exe", "/FI", "IMAGENAME eq hoi4.exe", "/FO", "CSV", "/NH"],
                       capture_output=True, text=True, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    return [line.strip() for line in p.stdout.splitlines() if '"hoi4.exe"' in line.lower()]


def base_descriptor(snapshot: Path) -> str:
    raw = (ROOT / "descriptor.mod").read_text(encoding="utf-8-sig")
    raw = re.sub(r'(?m)^\s*path\s*=.*\n?', "", raw)
    return raw.rstrip() + '\npath="' + snapshot.as_posix() + '"\n'


def smoke_fixture() -> tuple[str, list[str]]:
    checks = ["scenario_date_1970", "country_frei_start", "core_initialized", "scenario_route_active"]
    body = [
        f'log = "{PREFIX} STARTUP tag=[THIS.GetTag] date=[GetDateText]"',
        'if = { limit = { has_start_date > 1969.12.31 has_start_date < 1970.1.2 } log = "' + PREFIX + ' PASS scenario_date_1970" } else = { log = "' + PREFIX + ' FAIL scenario_date_1970" }',
        'if = { limit = { has_country_leader = { name = "Eduardo Frei Montalva" ruling_only = yes } } log = "' + PREFIX + ' PASS country_frei_start" } else = { log = "' + PREFIX + ' FAIL country_frei_start" }',
        'if = { limit = { has_country_flag = COLDWAR_CHL_initialized } log = "' + PREFIX + ' PASS core_initialized" } else = { log = "' + PREFIX + ' FAIL core_initialized" }',
        'if = { limit = { COLDWAR_CHL_is_scenario = yes } log = "' + PREFIX + ' PASS scenario_route_active" } else = { log = "' + PREFIX + ' FAIL scenario_route_active" }',
        f'log = "{PREFIX} COMPLETE date=[GetDateText]"',
    ]
    event = (MARK + 'add_namespace = ' + PREFIX + '\ncountry_event = {\n id = ' + PREFIX + '.1\n hidden = yes\n is_triggered_only = yes\n immediate = {\n' + '\n'.join(body) + '\n }\n}\n')
    on_actions = (MARK + 'on_actions = { on_startup = { effect = { if = { limit = { country_exists = CHL } CHL = { COLDWAR_CHL_initialize = yes COLDWAR_CHL_refresh_all = yes country_event = { id = ' + PREFIX + '.1 } } } } } }\n')
    return event, on_actions


def compiled_payload() -> dict[str, str]:
    import importlib.util
    spec = importlib.util.spec_from_file_location("chile_1970_probe_compile", HERE / "compile.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load the Chile 1970 compiler")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build()


def ast_api():
    sys.path.insert(0, str(ROOT / "tools/vietnam_1970"))
    from script_ast import parse, first, emit
    return parse, first, emit


def find_block(ast, wanted: str):
    for key, _, value in ast:
        if key == wanted and isinstance(value, list):
            return value
        if isinstance(value, list):
            found = find_block(value, wanted)
            if found is not None:
                return found
    return None


def transaction_probe(payload: dict[str, str]) -> tuple[list[str], str]:
    """Run a borrowed building focus twice plus a PDC party revalidation cycle."""
    parse, first, _ = ast_api()
    sys.path.insert(0,str(HERE))
    from current_design import load_design
    design = load_design()
    by_id = {n["id"]: n for n in design["nodes"]}
    target = by_id["COLDWAR_CHL_central_corridor"]
    order: list[str] = []
    seen: set[str] = set()

    def ancestors(focus: str) -> None:
        node = by_id[focus]
        for alternatives in node["prerequisites"]:
            if alternatives:
                ancestors(alternatives[0])
        if focus not in seen:
            seen.add(focus)
            order.append(focus)

    for alternatives in target["prerequisites"]:
        if alternatives:
            ancestors(alternatives[0])
    if not order:
        raise ValueError("The building transaction fixture has no prerequisites to complete")
    focus_tree = parse(payload["common/national_focus/COLDWAR_CHL_1970_focus.txt"])
    ids = {first(body, "id") for key, _, body in focus_tree if key == "focus_tree" for k, _, body in body if k == "focus"}
    if not set(order).issubset(ids):
        raise ValueError("A transaction prerequisite is missing from the emitted focus tree")

    smoke_checks = ["scenario_date_1970", "country_frei_start", "core_initialized", "scenario_route_active"]
    rows = [f'log = "{PREFIX} STARTUP tag=[THIS.GetTag] date=[GetDateText]"',
            'if = { limit = { has_start_date > 1969.12.31 has_start_date < 1970.1.2 } log = "' + PREFIX + ' PASS scenario_date_1970" } else = { log = "' + PREFIX + ' FAIL scenario_date_1970" }',
            'if = { limit = { has_country_leader = { name = "Eduardo Frei Montalva" ruling_only = yes } } log = "' + PREFIX + ' PASS country_frei_start" } else = { log = "' + PREFIX + ' FAIL country_frei_start" }',
            'if = { limit = { has_country_flag = COLDWAR_CHL_initialized } log = "' + PREFIX + ' PASS core_initialized" } else = { log = "' + PREFIX + ' FAIL core_initialized" }',
            'if = { limit = { COLDWAR_CHL_is_scenario = yes } log = "' + PREFIX + ' PASS scenario_route_active" } else = { log = "' + PREFIX + ' FAIL scenario_route_active" }',
            f'log = "{PREFIX} PHASE FOCUS_TRANSACTION"',
            'set_variable = { treasury = 1000 }']
    rows += [f'complete_national_focus = {{ focus = {focus} }}' for focus in order]
    # The selected build grants infrastructure, which does not consume shared
    # building slots; free industrial slots therefore expose its one-slot grant.
    state = target["buildings"][0]["state"]
    building = target["buildings"][0]["type"]
    level_key = "building_level@" + building
    for label in ("building_before", "building_after_first", "building_after_replay"):
        if label == "building_before":
            rows.append(f'{state} = {{ set_variable = {{ {PREFIX}_{label} = {level_key} }} }}')
    def count_shared_slots(save_as: str) -> list[str]:
        lines = [f"set_variable = {{ {save_as} = 0 }}"]
        # Count up to the native slot cap instead of assuming a low ceiling.
        for threshold in range(MAX_SHARED_SLOTS):
            lines.append(f'if = {{ limit = {{ {state} = {{ free_building_slots = {{ building = industrial_complex size > {threshold} include_locked = yes }} }} }} add_to_variable = {{ {save_as} = 1 }} }}')
        return lines

    rows += count_shared_slots(PREFIX + "_slots_before")
    rows += [
        'set_variable = { treasury = 0 }',
        f'set_variable = {{ {PREFIX}_cash_before = treasury }}',
        f'set_variable = {{ {PREFIX}_production_before = COLDWAR_CHL_development_production_speed_infrastructure_factor }}',
        f'set_variable = {{ {PREFIX}_supply_before = COLDWAR_CHL_development_supply_consumption_factor }}',
        f'set_variable = {{ {PREFIX}_production_expected = {PREFIX}_production_before }}',
        f'add_to_variable = {{ {PREFIX}_production_expected = 0.08 }}',
        f'set_variable = {{ {PREFIX}_supply_expected = {PREFIX}_supply_before }}',
        f'add_to_variable = {{ {PREFIX}_supply_expected = -0.03 }}',
        f'set_variable = {{ {PREFIX}_slots_expected = {PREFIX}_slots_before }}',
        f'add_to_variable = {{ {PREFIX}_slots_expected = 1 }}',
        f'{state} = {{ set_variable = {{ {PREFIX}_building_expected = {level_key} }} add_to_variable = {{ {PREFIX}_building_expected = 1 }} }}',
        'COLDWAR_CHL_apply_central_corridor = yes',
        f'set_variable = {{ {PREFIX}_cash_after_first = treasury }}',
        f'set_variable = {{ {PREFIX}_production_after_first = COLDWAR_CHL_development_production_speed_infrastructure_factor }}',
        f'set_variable = {{ {PREFIX}_supply_after_first = COLDWAR_CHL_development_supply_consumption_factor }}',
        f'{state} = {{ set_variable = {{ {PREFIX}_building_after_first = {level_key} }} }}',
    ]
    rows += count_shared_slots(PREFIX + "_slots_after_first")
    checks = [
        ("native_borrowing_and_focus_execution", f'has_country_flag = COLDWAR_CHL_central_corridor_applied check_variable = {{ var = {PREFIX}_cash_after_first value = {-target["money"]:.5f} compare = equals }} {state} = {{ check_variable = {{ var = {level_key} value = {PREFIX}_building_before compare = greater_than }} }} check_variable = {{ var = {PREFIX}_slots_after_first value = {PREFIX}_slots_before compare = greater_than }}'),
        ("guarded_focus_receipt", "has_country_flag = COLDWAR_CHL_central_corridor_applied"),
        ("guarded_focus_cash_cost", f'check_variable = {{ var = {PREFIX}_cash_after_first value = {-target["money"]:.5f} compare = equals }}'),
        ("building_grant_once", f'{state} = {{ check_variable = {{ var = {level_key} value = {PREFIX}_building_expected compare = equals }} }}'),
        ("shared_slot_grant_once", f'check_variable = {{ var = {PREFIX}_slots_after_first value = {PREFIX}_slots_expected compare = equals }}'),
        ("modifier_production_delta", f'check_variable = {{ var = {PREFIX}_production_after_first value = {PREFIX}_production_expected compare = equals }}'),
        ("modifier_supply_delta", f'check_variable = {{ var = {PREFIX}_supply_after_first value = {PREFIX}_supply_expected compare = equals }}'),
    ]
    rows += [f'if = {{ limit = {{ {trigger} }} log = "{PREFIX} PASS {name}" }} else = {{ log = "{PREFIX} FAIL {name}" }}' for name, trigger in checks]
    rows += [
        'COLDWAR_CHL_apply_central_corridor = yes',
        f'set_variable = {{ {PREFIX}_cash_after_replay = treasury }}',
        f'set_variable = {{ {PREFIX}_production_after_replay = COLDWAR_CHL_development_production_speed_infrastructure_factor }}',
        f'set_variable = {{ {PREFIX}_supply_after_replay = COLDWAR_CHL_development_supply_consumption_factor }}',
        f'{state} = {{ set_variable = {{ {PREFIX}_building_after_replay = {level_key} }} }}',
    ]
    rows += count_shared_slots(PREFIX + "_slots_after_replay")
    replay_checks = [
        ("replay_no_cash", f'check_variable = {{ var = {PREFIX}_cash_after_replay value = {PREFIX}_cash_after_first compare = equals }}'),
        ("replay_no_building", f'{state} = {{ check_variable = {{ var = {PREFIX}_building_after_replay value = {PREFIX}_building_after_first compare = equals }} }}'),
        ("replay_no_slot", f'check_variable = {{ var = {PREFIX}_slots_after_replay value = {PREFIX}_slots_after_first compare = equals }}'),
        ("replay_no_modifier_change", f'check_variable = {{ var = {PREFIX}_production_after_replay value = {PREFIX}_production_after_first compare = equals }} check_variable = {{ var = {PREFIX}_supply_after_replay value = {PREFIX}_supply_after_first compare = equals }}'),
    ]
    rows += [f'if = {{ limit = {{ {trigger} }} log = "{PREFIX} PASS {name}" }} else = {{ log = "{PREFIX} FAIL {name}" }}' for name, trigger in replay_checks]

    pdc = by_id["COLDWAR_CHL_pdc_social"]
    rows += [
        f'set_variable = {{ {PREFIX}_weekly_base = COLDWAR_CHL_domestic_weekly }}',
        f'set_variable = {{ {PREFIX}_weekly_expected = {PREFIX}_weekly_base }}',
        f'add_to_variable = {{ {PREFIX}_weekly_expected = {pdc["weekly"]:.5f} }}',
        'COLDWAR_CHL_apply_pdc_social = yes',
        f'set_variable = {{ {PREFIX}_pdc_weekly = COLDWAR_CHL_domestic_weekly }}',
        f'if = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_CHL_pdc_programme }} check_variable = {{ COLDWAR_CHL_pdc_stability_factor = 0.04 }} check_variable = {{ var = COLDWAR_CHL_domestic_weekly value = {PREFIX}_weekly_expected compare = equals }} }} log = "{PREFIX} PASS pdc_programme_active" }} else = {{ log = "{PREFIX} FAIL pdc_programme_active" }}',
        'set_variable = { rul_party_temp = 22 }', 'set_variable = { change_leader_temp = 0 }', 'change_ruling_party_effect = yes',
        'COLDWAR_CHL_refresh_programmes = yes',
        f'if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = COLDWAR_CHL_pdc_programme }} }} check_variable = {{ COLDWAR_CHL_pdc_stability_factor = 0.04 }} check_variable = {{ COLDWAR_CHL_pdc_social_cost_multiplier_modifier = 0.03 }} has_country_flag = COLDWAR_CHL_pdc_social_applied check_variable = {{ var = COLDWAR_CHL_domestic_weekly value = {PREFIX}_weekly_base compare = equals }} }} log = "{PREFIX} PASS pdc_inactive_receipts_retained_weekly_baseline" }} else = {{ log = "{PREFIX} FAIL pdc_inactive_receipts_retained_weekly_baseline" }}',
        'set_variable = { rul_party_temp = 1 }', 'set_variable = { change_leader_temp = 0 }', 'change_ruling_party_effect = yes',
        'COLDWAR_CHL_refresh_programmes = yes',
        f'if = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_CHL_pdc_programme }} check_variable = {{ COLDWAR_CHL_pdc_stability_factor = 0.04 }} check_variable = {{ var = COLDWAR_CHL_domestic_weekly value = {PREFIX}_weekly_expected compare = equals }} }} log = "{PREFIX} PASS pdc_restored_on_return" }} else = {{ log = "{PREFIX} FAIL pdc_restored_on_return" }}',
        f'set_variable = {{ {PREFIX}_pdc_cash_before_replay = treasury }}',
        'COLDWAR_CHL_apply_pdc_social = yes',
        f'set_variable = {{ {PREFIX}_pdc_cash_after_replay = treasury }}',
        f'if = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_CHL_pdc_programme }} check_variable = {{ COLDWAR_CHL_pdc_stability_factor = 0.04 }} check_variable = {{ COLDWAR_CHL_pdc_social_cost_multiplier_modifier = 0.03 }} has_country_flag = COLDWAR_CHL_pdc_social_applied check_variable = {{ var = COLDWAR_CHL_domestic_weekly value = {PREFIX}_weekly_expected compare = equals }} check_variable = {{ var = {PREFIX}_pdc_cash_after_replay value = {PREFIX}_pdc_cash_before_replay compare = equals }} }} log = "{PREFIX} PASS pdc_reactivation_no_repeat" }} else = {{ log = "{PREFIX} FAIL pdc_reactivation_no_repeat" }}',
    ]
    checks = smoke_checks + [name for name, _ in checks] + [name for name, _ in replay_checks]
    checks += ["pdc_programme_active", "pdc_inactive_receipts_retained_weekly_baseline", "pdc_restored_on_return", "pdc_reactivation_no_repeat"]
    event = MARK + 'add_namespace = ' + PREFIX + '\ncountry_event = { id = ' + PREFIX + '.1 hidden = yes is_triggered_only = yes immediate = {\n' + '\n'.join(rows) + '\nlog = "' + PREFIX + ' COMPLETE date=[GetDateText]"\n} }\n'
    return checks, event


def foreign_probe(payload: dict[str, str]) -> tuple[list[str], str]:
    """Simulate the USA recipient's emitted accept decision and reconcile it."""
    parse, first, emit = ast_api()
    decision_path = "common/decisions/COLDWAR_CHL_1970_diplomacy.txt"
    ast = parse(payload[decision_path])
    decision = find_block(ast, "COLDWAR_CHL_DIP_accept_usa_mines")
    if decision is None:
        raise ValueError("USA mines recipient acceptance decision not found")
    accept = first(decision, "complete_effect")
    if not isinstance(accept, list):
        raise ValueError("USA mines recipient decision has no complete effect")
    acceptance_code = emit(accept)
    helper = re.search(r"COLDWAR_CHL_dip_accept_([A-Za-z0-9_]+)\s*=", acceptance_code)
    if helper is None:
        raise ValueError("USA acceptance decision does not call a current Chile diplomacy helper")
    idea_prefix = "COLDWAR_CHL_dip_" + helper.group(1) + "_"
    idea_source = payload.get("common/ideas/COLDWAR_CHL_1970_diplomacy.txt", "")
    idea_ids = re.findall(r"(?m)^\s*(COLDWAR_CHL_dip_[A-Za-z0-9_]+)\s*=\s*\{", idea_source)
    chile_idea = next((key for key in idea_ids if key == idea_prefix + "chl"), None)
    usa_idea = next((key for key in idea_ids if key == idea_prefix + "usa"), None)
    if chile_idea is None or usa_idea is None:
        raise ValueError("The emitted diplomacy module lacks both current recipient and Chile spirits for " + helper.group(1))
    # Capture the generated agreement key from the live acceptance helper so
    # future diplomacy renames do not leave this fixture checking stale ideas.
    agreement_key = helper.group(1)
    checks = ["scenario_date_1970", "country_frei_start", "core_initialized", "scenario_route_active",
              "recipient_offer_pending", "both_signatures_recorded", "both_spirits_granted", "setup_fees_once", "agreement_reconciles_active"]
    rows = [
        f'log = "{PREFIX} STARTUP tag=[THIS.GetTag] date=[GetDateText]"',
        'if = { limit = { has_start_date > 1969.12.31 has_start_date < 1970.1.2 } log = "' + PREFIX + ' PASS scenario_date_1970" } else = { log = "' + PREFIX + ' FAIL scenario_date_1970" }',
        'if = { limit = { has_country_leader = { name = "Eduardo Frei Montalva" ruling_only = yes } } log = "' + PREFIX + ' PASS country_frei_start" } else = { log = "' + PREFIX + ' FAIL country_frei_start" }',
        'if = { limit = { has_country_flag = COLDWAR_CHL_initialized } log = "' + PREFIX + ' PASS core_initialized" } else = { log = "' + PREFIX + ' FAIL core_initialized" }',
        'if = { limit = { COLDWAR_CHL_is_scenario = yes } log = "' + PREFIX + ' PASS scenario_route_active" } else = { log = "' + PREFIX + ' FAIL scenario_route_active" }',
        f'log = "{PREFIX} PHASE FOREIGN_ACCEPTANCE"',
        'clr_country_flag = MD_skip_treasury_cost',
        'set_variable = { treasury = 100 }',
        'USA = { clr_country_flag = MD_skip_treasury_cost set_variable = { treasury = 100 } }',
        'COLDWAR_CHL_offer_usa_mines = yes',
        f'if = {{ limit = {{ has_country_flag = COLDWAR_CHL_dip_usa_mines_pending USA = {{ has_country_flag = COLDWAR_CHL_dip_usa_mines_pending }} }} log = "{PREFIX} PASS recipient_offer_pending" }} else = {{ log = "{PREFIX} FAIL recipient_offer_pending" }}',
        'USA = { ' + acceptance_code + ' }',
        f'if = {{ limit = {{ has_country_flag = COLDWAR_CHL_dip_usa_mines_signed USA = {{ has_country_flag = COLDWAR_CHL_dip_usa_mines_signed }} }} log = "{PREFIX} PASS both_signatures_recorded" }} else = {{ log = "{PREFIX} FAIL both_signatures_recorded" }}',
        f'if = {{ limit = {{ has_idea = {chile_idea} USA = {{ has_idea = {usa_idea} }} }} log = "{PREFIX} PASS both_spirits_granted" }} else = {{ log = "{PREFIX} FAIL both_spirits_granted" }}',
        f'if = {{ limit = {{ check_variable = {{ var = treasury value = 96 compare = equals }} USA = {{ check_variable = {{ var = treasury value = 99 compare = equals }} }} }} log = "{PREFIX} PASS setup_fees_once" }} else = {{ log = "{PREFIX} FAIL setup_fees_once" }}',
        'COLDWAR_CHL_diplomacy_daily = yes',
        f'if = {{ limit = {{ has_idea = {chile_idea} USA = {{ has_idea = {usa_idea} }} }} log = "{PREFIX} PASS agreement_reconciles_active" }} else = {{ log = "{PREFIX} FAIL agreement_reconciles_active" }}',
        f'log = "{PREFIX} COMPLETE date=[GetDateText]"',
    ]
    event = MARK + 'add_namespace = ' + PREFIX + '\ncountry_event = { id = ' + PREFIX + '.1 hidden = yes is_triggered_only = yes immediate = {\n' + '\n'.join(rows) + '\n} }\n'
    return checks, event


def prepare(mode: str = "smoke") -> Path:
    if os.name != "nt":
        raise RuntimeError("The isolated native profile preparer requires Windows")
    if mode not in ("smoke", "transactions", "foreign"):
        raise ValueError("Unknown probe mode: " + mode)
    if not (GAME / "hoi4.exe").is_file():
        raise FileNotFoundError("HOI4 executable not found at " + str(GAME / "hoi4.exe"))
    if not RUNTIME.parent.parent.parent.exists():
        raise FileNotFoundError("Required E: runtime root is unavailable: " + str(RUNTIME.parent.parent.parent))
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    run = RUNTIME / stamp
    assert_private(run)
    run.mkdir(parents=True, exist_ok=False)
    snapshot, profile = run / "snapshot", run / "profile"
    snapshot.mkdir(); profile.mkdir()
    hashes: dict[str, str] = {}
    links: list[dict[str, str]] = []
    last = [time.monotonic()]
    for dirname in COPY_DIRS:
        source = ROOT / dirname
        if source.is_dir():
            copy_tree(source, snapshot / dirname, hashes, last)
    for dirname in KNOWN_LINK_DIRS:
        if (ROOT / dirname).is_dir():
            link_known_asset(snapshot, dirname, links)
    descriptor_bytes = (ROOT / "descriptor.mod").read_bytes()
    (snapshot / "descriptor.mod").write_bytes(descriptor_bytes)
    hashes["descriptor.mod"] = sha(descriptor_bytes)
    snapshot_hashes = dict(hashes)
    fixture = profile / "fixture"
    payload = compiled_payload()
    payload_hashes = {}
    for relative, value in payload.items():
        encoded = value.encode("utf-8-sig" if relative.endswith(".yml") else "utf-8")
        write(fixture, relative, encoded)
        payload_hashes[relative] = sha(encoded)
    event, on_actions = smoke_fixture()
    checks = ["scenario_date_1970", "country_frei_start", "core_initialized", "scenario_route_active"]
    if mode == "transactions":
        checks, event = transaction_probe(payload)
    elif mode == "foreign":
        checks, event = foreign_probe(payload)
    write(fixture, "events/COLDWAR_CHL_NATIVE.txt", event)
    write(fixture, "common/on_actions/zzzzzzzz_COLDWAR_CHL_NATIVE.txt", on_actions)
    name_match = re.search(r'(?m)^\s*name\s*=\s*"([^"]+)"', base_descriptor(snapshot))
    if not name_match:
        raise ValueError("Base descriptor does not define a mod name")
    base_name = name_match.group(1)
    write(profile, "mod/mdcoldwar.mod", base_descriptor(snapshot))
    addon = MARK + 'name="IMPERIA Chile 1970 Native Fixture"\ndependencies={ "' + base_name + '" }\npath="' + fixture.as_posix() + '"\n'
    write(profile, "mod/chile_probe.mod", addon)
    write(fixture, "descriptor.mod", addon)
    write(profile, "dlc_load.json", json.dumps({"enabled_mods": ["mod/mdcoldwar.mod", "mod/chile_probe.mod"], "disabled_dlcs": []}))
    write(profile, "settings.txt", MARK + 'language="l_english"\ngraphics={size={x=1280 y=900} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n')
    # Hash only immutable fixture input. HOI may rewrite private user settings.
    fixture_hashes = {p.relative_to(fixture).as_posix(): sha(p.read_bytes()) for p in fixture.rglob("*") if p.is_file()}
    generator_files = list(HERE.glob("*.py")) + list(HERE.glob("*.json"))
    generator_hashes = {p.relative_to(ROOT).as_posix(): sha(p.read_bytes()) for p in generator_files if p.is_file()}
    limitations = {
        "smoke": ["Focus transactions and foreign consent are not exercised by smoke mode.", "No screenshot or player-driven UI test is generated."],
        "transactions": ["Scripted focus apply helpers are invoked from a private hidden event; no focus is selected through the player UI.", "No screenshot or multiplayer test is generated."],
        "foreign": ["The recipient decision's complete effect is executed in recipient country scope; no player clicks the decision UI.", "No multiplayer test is generated."],
    }[mode]
    report = {
        "project": "IMPERIA COLD WAR", "status": "PREPARED_NOT_RUN", "mode": mode,
        "run": str(run), "profile": str(profile), "snapshot": str(snapshot), "fixture": str(fixture),
        "game": str(GAME), "source_root": str(ROOT), "source_hashes": hashes, "snapshot_hashes": snapshot_hashes,
        "fixture_hashes": fixture_hashes, "payload_hashes": payload_hashes, "generator_hashes": generator_hashes,
        "known_read_only_asset_links": links, "checks": checks,
        "native_gameplay_tested": False, "limitations": limitations,
    }
    dump(run / "probe_manifest.json", report)
    dump(run / "native_report.json", {"project": "IMPERIA COLD WAR", "status": "PREPARED_NOT_RUN", "mode": mode, "native_test_executed": False, "passed": [], "failed": [], "unrun": report["checks"], "run": str(run)})
    print(json.dumps({"phase": "prepared", "run": str(run), "mode": mode, "frozen_files": len(hashes), "links": links}, ensure_ascii=False), flush=True)
    return run


def hidden_startup():
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    return startup


def run_probe(run: Path, timeout: int = 900) -> int:
    run = assert_private(run)
    manifest = json.loads((run / "probe_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("status") != "PREPARED_NOT_RUN":
        raise ValueError("Only a fresh PREPARED_NOT_RUN directory can be launched")
    if game_processes():
        dump(run / "native_report.json", {"project": "IMPERIA COLD WAR", "status": "NOT_RUN_EXISTING_HOI4", "native_test_executed": False, "unrun": manifest["checks"]})
        return 2
    source_drift = drift(ROOT, manifest["source_hashes"])
    generator_drift = drift(ROOT, manifest["generator_hashes"])
    snapshot_drift = drift(Path(manifest["snapshot"]), manifest["snapshot_hashes"])
    fixture = Path(manifest["fixture"])
    fixture_drift = drift(fixture, manifest["fixture_hashes"])
    if source_drift or generator_drift or snapshot_drift or fixture_drift:
        dump(run / "native_report.json", {"project": "IMPERIA COLD WAR", "status": "NOT_RUN_PREPARED_INPUT_DRIFT", "native_test_executed": False,
              "source_drift": source_drift, "generator_drift": generator_drift, "snapshot_drift": snapshot_drift,
              "fixture_drift": fixture_drift, "unrun": manifest["checks"]})
        return 2
    args = [str(GAME / "hoi4.exe"), "-debug", "-noasserts", "-assertsdialog=no", "-userdir=" + manifest["profile"], "-start_tag=CHL", "-start_speed=3", "-hands_off"]
    if game_processes():
        return 2
    started = time.monotonic()
    try:
        process = subprocess.Popen(args, cwd=GAME, startupinfo=hidden_startup(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError as exc:
        dump(run / "native_report.json", {"project": "IMPERIA COLD WAR", "status": "NOT_RUN_LAUNCH_FAILED", "native_test_executed": False, "error": str(exc), "unrun": manifest["checks"]})
        return 2
    manifest["status"] = "RUN_STARTED"; manifest["pid"] = process.pid; dump(run / "probe_manifest.json", manifest)
    print(json.dumps({"phase": "native_start", "pid": process.pid, "profile": manifest["profile"]}), flush=True)
    log_path = Path(manifest["profile"]) / "logs/game.log"
    error_path = Path(manifest["profile"]) / "logs/error.log"
    log = ""; stopped = False; last = started
    try:
        while process.poll() is None and time.monotonic() - started < timeout:
            time.sleep(1)
            log = log_path.read_text(encoding="utf-8-sig", errors="replace") if log_path.is_file() else ""
            if PREFIX + " COMPLETE" in log:
                break
            if time.monotonic() - last >= 20:
                last = time.monotonic(); print(json.dumps({"phase": "native_wait", "seconds": int(last - started), "startup_seen": PREFIX + " STARTUP" in log}), flush=True)
    finally:
        stopped = process.poll() is None
        if stopped:
            process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill(); process.wait()
    log = log_path.read_text(encoding="utf-8-sig", errors="replace") if log_path.is_file() else log
    errors = error_path.read_text(encoding="utf-8-sig", errors="replace") if error_path.is_file() else ""
    passed = [key for key in manifest["checks"] if PREFIX + " PASS " + key in log]
    failed = [key for key in manifest["checks"] if PREFIX + " FAIL " + key in log]
    unrun = [key for key in manifest["checks"] if key not in passed and key not in failed]
    complete = PREFIX + " COMPLETE" in log
    crashes = list((Path(manifest["profile"]) / "crashes").glob("*/exception.txt")) if (Path(manifest["profile"]) / "crashes").exists() else []
    generated_names = [PurePosixPath(rel).name for rel in manifest.get("payload_hashes", {})]
    relevant_errors = [line for line in errors.splitlines()
                       if re.search(r"CHL_NATIVE|COLDWAR_CHL_", line, re.I)
                       or any(name and name in line for name in generated_names)]
    result = complete and not failed and not unrun and not crashes and not relevant_errors and (stopped or process.returncode == 0)
    pass_status = {"smoke": "PASS_SMOKE", "transactions": "PASS_TRANSACTIONS", "foreign": "PASS_FOREIGN"}[manifest["mode"]]
    status = pass_status if result else ("FAIL_ENGINE_CRASH_OR_EXIT" if crashes or (process.returncode not in (0, None) and not stopped) else "FAIL_INCOMPLETE_OR_DIAGNOSTICS")
    dump(run / "native_report.json", {
        "project": "IMPERIA COLD WAR", "status": status, "mode": manifest["mode"], "native_test_executed": True,
        "success": result, "passed": passed, "failed": failed, "unrun": unrun, "complete_checkpoint": complete,
        "profile": manifest["profile"], "game_log": str(log_path), "error_log": str(error_path),
        "relevant_errors": relevant_errors,
        "crash_exceptions": [str(p) for p in crashes], "elapsed_seconds": round(time.monotonic() - started, 1),
        "returncode": process.returncode, "expected_termination_after_complete": bool(complete and stopped),
        "stopped_own_pid": process.pid if stopped else None,
        "limitations": manifest["limitations"],
    })
    print(json.dumps({"phase": "native_result", "status": status, "passed": passed, "failed": failed, "unrun": unrun}, ensure_ascii=False), flush=True)
    return 0 if result else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prepare", action="store_true", help="Freeze the installed mod and prepare a private E: fixture without launching HOI4")
    group.add_argument("--run", type=Path, metavar="PREPARED_DIRECTORY", help="Launch only the specified prepared private fixture")
    parser.add_argument("--mode", choices=("smoke", "transactions", "foreign"), default="smoke")
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()
    if args.prepare:
        prepare(args.mode)
        return 0
    return run_probe(args.run, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
