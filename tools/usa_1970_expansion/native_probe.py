# IMPERIA COLD WAR — Isolated hidden USA native-engine smoke probe.
"""Prepare an immutable runtime snapshot; launch only after the final freeze.

Every generated file is under this module's native_probe directory. Existing
user profiles, existing hoi4 processes and the shared multiplayer probe are
never modified. A successful fixture is a single-process script observation,
not a human recipient, live multiplayer, hover or save/reload test.
"""
from __future__ import annotations

import argparse
import ctypes
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import threading
import time

ROOT = Path(__file__).resolve().parents[2]
OWN = Path(__file__).resolve().parent / 'native_probe'
ASSET_PROVIDER = Path(__file__).resolve().parent / 'a'
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
RUNTIME = ('common', 'events', 'history', 'interface', 'localisation', 'portraits', 'descriptions', 'tutorial')
ASSETS = ('gfx', 'map', 'sound', 'music')
MARKER = '# IMPERIA COLD WAR — Isolated USA native-engine smoke fixture.\n'
NAMESPACE = 'ICW_USA_NATIVE'


def owned(path):
    result = Path(path).absolute()
    # Every writable parent is an ordinary directory in this task's workspace.
    assert result.is_relative_to(OWN.absolute()) or result.is_relative_to(ASSET_PROVIDER.absolute()), result
    return result


def write(path, text):
    path = owned(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def ps_quote(text):
    return "'" + str(text).replace("'", "''") + "'"


def powershell(command):
    return subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-WindowStyle', 'Hidden', '-Command', command],
                          check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)


def files_in(folder):
    """Scan large asset trees without redundant stat calls per directory entry."""
    with os.scandir(folder) as entries:
        for entry in entries:
            if entry.is_dir(follow_symlinks=False):
                yield from files_in(Path(entry.path))
            elif entry.is_file(follow_symlinks=False):
                yield Path(entry.path), entry.stat(follow_symlinks=False)


def prepare_assets(run_id):
    assert re.fullmatch(r'[a-zA-Z0-9_-]{1,80}', run_id), run_id
    provider = owned(ASSET_PROVIDER)
    provider.mkdir(parents=True, exist_ok=True)
    inventory = [(path, stat) for name in ASSETS for path, stat in files_in(ROOT / name)]
    total = sum(stat.st_size for _, stat in inventory)
    existing_bytes = sum((provider / path.relative_to(ROOT)).stat().st_size for path, _ in inventory if (provider / path.relative_to(ROOT)).is_file())
    free = shutil.disk_usage(provider).free
    reserve = 10 * 1024 ** 3
    required = max(0, total - existing_bytes)
    if required + reserve > free:
        raise RuntimeError(f'Asset copy requires {required} bytes plus 10 GiB reserve; only {free} bytes free.')
    print(json.dumps(dict(project='IMPERIA COLD WAR', asset_copy_started=True, files=len(inventory), source_bytes=total, remaining_copy_bytes=required, free_bytes=free, reserve_bytes=reserve)), flush=True)
    copy_codes = {}
    for name in ASSETS:
        destination = owned(provider / name)
        destination.mkdir(parents=True, exist_ok=True)
        assert destination.resolve().is_relative_to(ASSET_PROVIDER.resolve())
        # /E copies and resumes without purging or deleting anything. /MT keeps
        # 78k small textures practical. No junction/hardlink or source write.
        result = subprocess.run(['robocopy.exe', str(ROOT / name), str(destination), '/E', '/COPY:DAT', '/DCOPY:DAT', '/R:0', '/W:0', '/MT:16', '/XJ', '/NFL', '/NDL', '/NJH', '/NJS', '/NP'],
                                capture_output=True, text=True, encoding='utf-8', errors='replace', creationflags=subprocess.CREATE_NO_WINDOW)
        copy_codes[name] = result.returncode
        write(provider / ('copy_' + name + '.log'), 'IMPERIA COLD WAR: native asset-copy diagnostics.\n' + result.stdout + result.stderr)
        if result.returncode >= 8:
            raise RuntimeError('Asset copy failed for ' + name + '; resumable copies retained. Native exit=' + str(result.returncode))
        print(json.dumps(dict(project='IMPERIA COLD WAR', asset_directory_complete=name, robocopy_exit=result.returncode)), flush=True)
    maximum_path = max(len(str(provider / source.relative_to(ROOT))) for source, _ in inventory)
    assert maximum_path <= 259, ('Native asset path exceeds Windows limit', maximum_path)
    cached = json.loads((provider / 'asset_manifest.json').read_text())['assets'] if (provider / 'asset_manifest.json').exists() else {}
    def verify_pair(item):
        source, stat = item
        relative = source.relative_to(ROOT).as_posix()
        destination = provider / relative
        assert destination.is_file() and destination.stat().st_size == stat.st_size, ('Incomplete asset copy', relative)
        old = cached.get(relative, {})
        source_hash = old.get('sha256') if old.get('bytes') == stat.st_size and old.get('source_mtime_ns') == stat.st_mtime_ns else None
        source_hash = source_hash or digest(source)
        destination_hash = digest(destination)
        assert source_hash == destination_hash, ('Asset bytes differ', relative)
        return relative, dict(bytes=stat.st_size, source_mtime_ns=stat.st_mtime_ns, sha256=destination_hash)
    records = {}
    with ThreadPoolExecutor(max_workers=16) as pool:
        for index, (relative, record) in enumerate(pool.map(verify_pair, inventory), 1):
            records[relative] = record
            if index % 10000 == 0:
                print(json.dumps(dict(project='IMPERIA COLD WAR', asset_hashes_verified=index, total=len(inventory))), flush=True)
    descriptor_source = (ROOT / 'descriptor.mod').read_text(encoding='utf-8-sig')
    masks = [mask for mask in re.findall(r'^\s*replace_path\s*=\s*"([^"]+)"', descriptor_source, re.M) if mask.strip('/').split('/')[0] in ASSETS]
    descriptor = MARKER + 'name="IMPERIA USA native asset provider"\nsupported_version="1.19.*"\n' + ''.join('replace_path="' + mask + '"\n' for mask in masks) + 'path="' + provider.as_posix() + '"\n'
    write(provider / 'descriptor.mod', descriptor)
    samples = ['gfx/interface/ideas/research/research_bonus.dds', 'map/definition.csv']
    for name in ('sound', 'music'):
        choices = [(p, s) for p, s in inventory if p.relative_to(ROOT).parts[0] == name]
        if choices:
            samples.append(min(choices, key=lambda item: item[1].st_size)[0].relative_to(ROOT).as_posix())
    hashes = {}
    for relative in samples:
        if (ROOT / relative).is_file():
            hashes[relative] = digest(provider / relative)
            assert hashes[relative] == digest(ROOT / relative), relative
    manifest = dict(project='IMPERIA COLD WAR', asset_mode='actual copies in isolated assets-only provider; no links', provider=str(provider), source=str(ROOT),
                    files=len(records), source_bytes=total, original_asset_masks=masks, copy_exit_codes=copy_codes,
                    sample_sha256=hashes, maximum_native_path_characters=maximum_path,
                    verification='Every copied asset SHA-256 matched its source; source hashes may be cached only when source size and modification time are unchanged. Copied payload hashes are always recalculated.', assets=records)
    write(provider / 'asset_manifest.json', json.dumps(manifest, indent=2) + '\n')
    write(provider / 'NOTICE.md', 'IMPERIA COLD WAR: isolated asset provider for native testing.\n\nSource: the existing local IMPERIA COLD WAR gfx, map, sound and music directories, identified in asset_manifest.json. Original authors, individual credits, applicable licences and permissions have not been audited for every asset and are unknown where the existing source records do not establish them. Existing notices copied with the source remain applicable. Files are copied unchanged solely as a local native-test fixture; no new ownership or licence is asserted. No source content is written and no runtime code directories are included. NTFS junctions and hardlinks were unavailable under standard permissions, so this reversible task-owned copy is used.\n')
    assert all(not (provider / name).exists() for name in RUNTIME), 'Runtime directory leaked into asset provider.'
    return dict(project='IMPERIA COLD WAR', provider=str(provider), files=len(records), bytes=total, descriptor_sha256=digest(provider / 'descriptor.mod'), manifest_sha256=digest(provider / 'asset_manifest.json'), asset_mode=manifest['asset_mode'], engine_launched=False)


def archive_attempt(run):
    if not (run / 'freeze.json').exists():
        return None
    running = powershell("Get-Process -ErrorAction Stop | Where-Object { $_.ProcessName -eq 'hoi4' } | Select-Object Id,Path | ConvertTo-Json").stdout.strip()
    assert not running, 'A running HOI4 process must remain untouched: ' + running
    index = 1
    while (run / ('bounded_loading_attempt_' + str(index))).exists():
        index += 1
    archive = owned(run / ('bounded_loading_attempt_' + str(index)))
    archive.mkdir()
    for relative in ('freeze.json', 'snapshot/descriptor.mod', 'profile/mod/usa_native_assets.mod', 'profile/mod/usa_native_snapshot.mod', 'profile/mod/usa_native_fixture.mod', 'profile/dlc_load.json'):
        source = owned(run / relative)
        if source.exists():
            target = owned(archive / relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    log_source, log_target = run / 'profile/logs', archive / 'profile_logs'
    if log_source.exists():
        assert log_source.resolve().is_relative_to(OWN.resolve()) and log_target.resolve().is_relative_to(OWN.resolve())
        log_source.rename(log_target)
    for name in ('native_result.json', 'native_error.log', 'native_game.log'):
        source = owned(run / name)
        if source.exists():
            target = owned(archive / name)
            assert source.resolve().is_relative_to(OWN.resolve()) and target.resolve().is_relative_to(OWN.resolve())
            source.rename(target)
    write(archive / 'NOTICE.md', 'IMPERIA COLD WAR: preserved bounded native loading attempt.\n\nThe original freeze, descriptors, complete logs and any result are preserved before refreshing the test snapshot. Loading messages or absent fixture checkpoints do not establish gameplay success. Changed prior runtime files are preserved separately during resume.\n')
    return archive


def assertion(label, conditions):
    return ('if = { limit = { ' + conditions + ' } log = "' + NAMESPACE + ' PASS_' + label + '" }\n'
            'else = { log = "' + NAMESPACE + ' FAIL_' + label + '" add_to_variable = { ICW_USA_NATIVE_failures = 1 } }\n')


def diagnostic(label, conditions):
    """Observe a native predicate without assuming its semantic default."""
    return ('if = { limit = { ' + conditions + ' } log = "' + NAMESPACE + ' DIAG_' + label + '=yes" }\n'
            'else = { log = "' + NAMESPACE + ' DIAG_' + label + '=no" }\n')


def fixture_sources(focus_ids):
    first_hour = ['log = "ICW_USA_NATIVE FIRST_HOUR"',
        'country_event = { id = ICW_USA_OVERRIDE.1 }',
        'log = "ICW_USA_NATIVE GULF_PRORATION support=[?COLDWAR_USA_gulf_prorated_005_daily_cost] relief=[?COLDWAR_USA_gulf_prorated_0025_daily_cost] limited=[?COLDWAR_USA_gulf_prorated_002_daily_cost]"',
        assertion('USA_TREE', 'has_focus_tree = USA_1970_focus'),
        assertion('USA_SYSTEMS', 'has_country_flag = USA_1970_systems_initialized'),
        assertion('EXPANSION_INITIALIZED', 'has_country_flag = COLDWAR_USA_expansion_initialized'),
        assertion('TAX_MODEL_CALIBRATED', 'has_country_flag = COLDWAR_USA_1970_tax_model_calibrated check_variable = { corporate_tax_rate = 20 }'),
        'set_variable = { ICW_USA_NATIVE_focus_references = 0 }']
    # The engine parses actual references to every compiled ID. The numeric
    # count is a source inventory, not a fictitious native focus enumeration.
    for focus in focus_ids:
        first_hour.append('if = { limit = { has_completed_focus = ' + focus + ' } add_to_variable = { ICW_USA_NATIVE_focus_references = 1 } }')
    first_hour += ['log = "ICW_USA_NATIVE SOURCE_FOCUS_REFERENCES=' + str(len(focus_ids)) + ' tree=USA_1970_focus"',
        'set_variable = { treasury = 1000 }', 'clr_country_flag = MD_skip_treasury_cost',
        'CAN = { set_variable = { treasury = 1000 } clr_country_flag = MD_skip_treasury_cost }',
        'ENG = { set_variable = { treasury = 1000 } clr_country_flag = MD_skip_treasury_cost }',
        '763 = { set_variable = { ICW_USA_NATIVE_can_factory_before = building_level@industrial_complex } set_variable = { ICW_USA_NATIVE_can_factory_expected = { value = building_level@industrial_complex add = 1 } } }',
        assertion('PRE_CAN_TAG_USA', 'tag = USA'),
        assertion('PRE_CAN_1970_SCENARIO', 'IMP_is_1970_scenario = yes'),
        assertion('PRE_CAN_USA_EXISTS', 'country_exists = USA'),
        assertion('PRE_CAN_EXISTS', 'country_exists = CAN'),
        assertion('CAN_PAIR_CLEAR', 'COLDWAR_USA_agreements_pair_clear_can = yes'),
        # Establish the newly required basic parent through its production
        # offer and recipient acceptance, before testing the paid expansion.
        'COLDWAR_USA_early_complete_root_trade = yes',
        assertion('EARLY_CAN_PENDING', 'has_country_flag = COLDWAR_USA_early_canada_offer_open CAN = { has_country_flag = COLDWAR_USA_early_canada_offer_pending }'),
        'CAN = { COLDWAR_USA_early_accept_canada_can = yes }',
        assertion('EARLY_CAN_ACCEPTED_PAIR', 'COLDWAR_USA_early_active_canada = yes'),
        assertion('PRE_CAN_READY', 'COLDWAR_USA_agreements_ready_canada = yes'),
        assertion('PRE_CAN_CAN_OFFER', 'COLDWAR_USA_agreements_can_offer_canada = yes'),
        assertion('PRE_CAN_USA_NOT_SIGNED', 'NOT = { has_country_flag = COLDWAR_USA_agreements_canada_signed }'),
        assertion('PRE_CAN_USA_NOT_OPEN', 'NOT = { has_country_flag = COLDWAR_USA_agreements_canada_offer_open }'),
        assertion('PRE_CAN_USA_NOT_COOLDOWN', 'NOT = { has_country_flag = COLDWAR_USA_agreements_canada_cooldown }'),
        assertion('PRE_CAN_RECIPIENT_NOT_SIGNED', 'CAN = { NOT = { has_country_flag = COLDWAR_USA_agreements_canada_signed } }'),
        'clr_country_flag = ICW_USA_NATIVE_timed_omitted_value',
        'clr_country_flag = ICW_USA_NATIVE_timed_explicit_value',
        'set_country_flag = { flag = ICW_USA_NATIVE_timed_omitted_value days = 90 }',
        'set_country_flag = { flag = ICW_USA_NATIVE_timed_explicit_value value = 1 days = 90 }',
        'log = "ICW_USA_NATIVE DIAG_TIMED_FORMS A=flag+days90 B=flag+value1+days90"',
        diagnostic('TIMED_OMITTED_VALUE_HAS_FLAG', 'has_country_flag = ICW_USA_NATIVE_timed_omitted_value'),
        diagnostic('TIMED_EXPLICIT_VALUE1_HAS_FLAG', 'has_country_flag = ICW_USA_NATIVE_timed_explicit_value'),
        'set_country_flag = COLDWAR_USA_agreements_canada_authorised',
        assertion('PRE_CAN_AUTHORISED', 'has_country_flag = COLDWAR_USA_agreements_canada_authorised'),
        'COLDWAR_USA_agreements_send_canada = yes',
        diagnostic('CAN_POST_SEND_USA_COOLDOWN', 'has_country_flag = COLDWAR_USA_agreements_canada_cooldown'),
        diagnostic('CAN_POST_SEND_USA_SIGNED', 'has_country_flag = COLDWAR_USA_agreements_canada_signed'),
        diagnostic('CAN_POST_SEND_RECIPIENT_EVER_OFFERED', 'CAN = { has_country_flag = COLDWAR_USA_agreements_canada_ever_offered }'),
        assertion('CAN_SENT_USA_OPEN', 'has_country_flag = COLDWAR_USA_agreements_canada_offer_open'),
        assertion('CAN_SENT_RECIPIENT_PENDING', 'CAN = { has_country_flag = COLDWAR_USA_agreements_canada_offer_pending }'),
        assertion('CAN_SENT_USA_EVER_OFFERED', 'has_country_flag = COLDWAR_USA_agreements_canada_ever_offered'),
        assertion('CAN_PENDING', 'has_country_flag = COLDWAR_USA_agreements_canada_offer_open CAN = { has_country_flag = COLDWAR_USA_agreements_canada_offer_pending }'),
        assertion('CAN_PENDING_NO_SPIRITS', 'NOT = { has_idea = COLDWAR_USA_agreements_canada_usa } CAN = { NOT = { has_idea = COLDWAR_USA_agreements_canada_can } }'),
        assertion('CAN_PENDING_NO_PAYMENT', 'check_variable = { treasury = 1000 } CAN = { check_variable = { treasury = 1000 } }'),
        assertion('CAN_PENDING_NO_BUILDING', '763 = { check_variable = { ICW_USA_NATIVE_can_factory_before = building_level@industrial_complex } }'),
        diagnostic('CAN_TRANSACTION_VALID', 'COLDWAR_USA_agreements_transaction_valid_canada = yes'),
        diagnostic('CAN_RECIPIENT_ACCEPT_VALID', 'CAN = { COLDWAR_USA_agreements_accept_valid_canada_can = yes }'),
        diagnostic('CAN_USA_FUNDS_GE6', 'check_variable = { var = treasury value = 6 compare = greater_than_or_equals }'),
        diagnostic('CAN_RECIPIENT_FUNDS_GE4', 'CAN = { check_variable = { var = treasury value = 4 compare = greater_than_or_equals } }'),
        diagnostic('CAN_USA_SKIP_COST_FLAG', 'has_country_flag = MD_skip_treasury_cost'),
        diagnostic('CAN_RECIPIENT_SKIP_COST_FLAG', 'CAN = { has_country_flag = MD_skip_treasury_cost }'),
        diagnostic('CAN_ASSET_STATE_OWNED', 'CAN = { owns_state = 763 }'),
        diagnostic('CAN_ASSET_STATE_CONTROLLED', 'CAN = { controls_state = 763 }'),
        diagnostic('CAN_ASSET_NATIVE_FREE_SLOT', '763 = { free_building_slots = { building = industrial_complex size > 0 include_locked = no } }'),
        diagnostic('CAN_ASSET_GRANT_RECEIPT', 'has_country_flag = COLDWAR_USA_agreements_canada_grant_can_received'),
        'log = "ICW_USA_NATIVE DIAG_CAN_USA_TREASURY=[?treasury]"',
        'CAN = { log = "ICW_USA_NATIVE DIAG_CAN_RECIPIENT_TREASURY=[?treasury]" }',
        # Actual recipient-owned production helper, deliberately called by the
        # isolated fixture rather than pretending a human clicked an option.
        'CAN = { COLDWAR_USA_agreements_accept_canada_can = yes }',
        assertion('CAN_ACCEPTED_PAIR', 'COLDWAR_USA_agreements_active_canada = yes'),
        assertion('CAN_SETUP_ONCE', 'check_variable = { treasury = 994 } CAN = { check_variable = { treasury = 996 } }'),
        assertion('CAN_BUILDING_ONCE', '763 = { check_variable = { ICW_USA_NATIVE_can_factory_expected = building_level@industrial_complex } }'),
        'CAN = { COLDWAR_USA_agreements_accept_canada_can = yes }',
        'COLDWAR_USA_agreements_ratify_canada = yes',
        'COLDWAR_USA_agreements_send_canada = yes',
        'COLDWAR_USA_agreements_reconcile_all = yes',
        assertion('CAN_DUPLICATE_NO_PAYMENT', 'check_variable = { treasury = 994 } CAN = { check_variable = { treasury = 996 } }'),
        assertion('CAN_DUPLICATE_NO_BUILDING', '763 = { check_variable = { ICW_USA_NATIVE_can_factory_expected = building_level@industrial_complex } }')]
    for holder, partner in [('USA', 'CAN'), ('CAN', 'USA')]:
        for kind in ('dip', 'fin', 'eco', 'mil'):
            for direction in ('by_us', 'on_us'):
                array = 'imp_' + kind + '_sanc_' + direction
                label = holder + '_' + kind.upper() + '_' + direction.upper()
                first_hour += [holder + ' = { add_to_array = { array = ' + array + ' value = ' + partner + ' } }',
                    'COLDWAR_USA_agreements_reconcile_all = yes',
                    assertion('SUSPEND_' + label, 'NOT = { has_idea = COLDWAR_USA_agreements_canada_usa } CAN = { NOT = { has_idea = COLDWAR_USA_agreements_canada_can } }'),
                    holder + ' = { remove_from_array = { array = ' + array + ' value = ' + partner + ' } }',
                    'COLDWAR_USA_agreements_reconcile_all = yes',
                    assertion('RESTORE_' + label, 'COLDWAR_USA_agreements_active_canada = yes'),
                    assertion('RESTORE_ONCE_' + label, 'check_variable = { treasury = 994 } CAN = { check_variable = { treasury = 996 } } 763 = { check_variable = { ICW_USA_NATIVE_can_factory_expected = building_level@industrial_complex } }')]
    first_hour += [assertion('ENG_NATO_REAL_START', 'has_idea = NATO_member ENG = { has_idea = NATO_member }'),
        assertion('PRE_ENG_READY', 'COLDWAR_USA_agreements_ready_britain = yes'),
        assertion('PRE_ENG_CAN_OFFER', 'COLDWAR_USA_agreements_can_offer_britain = yes'),
        diagnostic('ENG_USA_SIGNED_BLOCKER', 'has_country_flag = COLDWAR_USA_agreements_britain_signed'),
        diagnostic('ENG_USA_OPEN_BLOCKER', 'has_country_flag = COLDWAR_USA_agreements_britain_offer_open'),
        diagnostic('ENG_USA_COOLDOWN_BLOCKER', 'has_country_flag = COLDWAR_USA_agreements_britain_cooldown'),
        diagnostic('ENG_RECIPIENT_SIGNED_BLOCKER', 'ENG = { has_country_flag = COLDWAR_USA_agreements_britain_signed }'),
        'set_country_flag = COLDWAR_USA_agreements_britain_authorised',
        assertion('PRE_ENG_AUTHORISED', 'has_country_flag = COLDWAR_USA_agreements_britain_authorised'),
        'COLDWAR_USA_agreements_send_britain = yes',
        diagnostic('ENG_POST_SEND_USA_COOLDOWN', 'has_country_flag = COLDWAR_USA_agreements_britain_cooldown'),
        diagnostic('ENG_POST_SEND_USA_SIGNED', 'has_country_flag = COLDWAR_USA_agreements_britain_signed'),
        assertion('ENG_SENT_USA_OPEN', 'has_country_flag = COLDWAR_USA_agreements_britain_offer_open'),
        assertion('ENG_SENT_RECIPIENT_PENDING', 'ENG = { has_country_flag = COLDWAR_USA_agreements_britain_offer_pending }'),
        assertion('ENG_SENT_USA_EVER_OFFERED', 'has_country_flag = COLDWAR_USA_agreements_britain_ever_offered'),
        assertion('ENG_PENDING_NO_SPIRITS', 'NOT = { has_idea = COLDWAR_USA_agreements_britain_usa } ENG = { NOT = { has_idea = COLDWAR_USA_agreements_britain_eng } }'),
        diagnostic('ENG_TRANSACTION_VALID', 'COLDWAR_USA_agreements_transaction_valid_britain = yes'),
        diagnostic('ENG_RECIPIENT_ACCEPT_VALID', 'ENG = { COLDWAR_USA_agreements_accept_valid_britain_eng = yes }'),
        diagnostic('ENG_USA_FUNDS_GE3', 'check_variable = { var = treasury value = 3 compare = greater_than_or_equals }'),
        diagnostic('ENG_RECIPIENT_FUNDS_GE2', 'ENG = { check_variable = { var = treasury value = 2 compare = greater_than_or_equals } }'),
        'ENG = { COLDWAR_USA_agreements_accept_britain_eng = yes }',
        assertion('ENG_ACCEPTED_PAIR', 'COLDWAR_USA_agreements_active_britain = yes'),
        'COLDWAR_USA_agreements_calculate_weekly_streams = yes',
        assertion('ENG_WEEKLY_STREAM', 'check_variable = { COLDWAR_USA_agreements_weekly_expense = 0.01 }'),
        'set_variable = { ICW_USA_NATIVE_treasury_fiscal_before = treasury }',
        'calculate_additional_income_rate = yes', 'calculate_additional_expense_rate = yes',
        'set_variable = { ICW_USA_NATIVE_income_first = additional_income_rate }',
        'set_variable = { ICW_USA_NATIVE_expense_first = additional_expenses_rate }',
        'calculate_additional_income_rate = yes', 'calculate_additional_expense_rate = yes',
        assertion('NATIVE_RATE_PURE', 'check_variable = { ICW_USA_NATIVE_treasury_fiscal_before = treasury } check_variable = { ICW_USA_NATIVE_income_first = additional_income_rate } check_variable = { ICW_USA_NATIVE_expense_first = additional_expenses_rate }'),
        # Fixture precondition for the rate consumer, not an earned focus claim.
        'add_ideas = COLDWAR_USA_dom_nuclear_priority_s0',
        'calculate_additional_expense_rate = yes',
        'set_variable = { ICW_USA_NATIVE_nuclear_delta = { value = additional_expenses_rate subtract = ICW_USA_NATIVE_expense_first } }',
        assertion('NUCLEAR_NATIVE_RATE', 'check_variable = { COLDWAR_USA_domestic_weekly_expense = 0.03 } check_variable = { ICW_USA_NATIVE_nuclear_delta = 0.03 } check_variable = { ICW_USA_NATIVE_treasury_fiscal_before = treasury }'),
        'remove_ideas = COLDWAR_USA_dom_nuclear_priority_s0',
        'calculate_additional_expense_rate = yes',
        assertion('NUCLEAR_NATIVE_CLEAR', 'check_variable = { COLDWAR_USA_domestic_weekly_expense = 0 } check_variable = { ICW_USA_NATIVE_expense_first = additional_expenses_rate }'),
        # Shorten only the isolated fixture's approved term receipt after real
        # ratification, so native calendar expiry can be observed in two days.
        'clr_country_flag = COLDWAR_USA_agreements_britain_term',
        'set_country_flag = { flag = COLDWAR_USA_agreements_britain_term value = 1 days = 1 }',
        assertion('ENG_ACCELERATED_TERM_INITIAL_PRESENT', 'has_country_flag = COLDWAR_USA_agreements_britain_term'),
        'set_country_flag = ICW_USA_NATIVE_first_hour_done',
        'country_event = { id = ICW_USA_NATIVE.2 days = 2 }',
        'log = "ICW_USA_NATIVE FIRST_HOUR_COMPLETE"']
    expiry = ['log = "ICW_USA_NATIVE ACCELERATED_EXPIRY_CHECK"',
        'COLDWAR_USA_agreements_reconcile_all = yes',
        assertion('ENG_ACCELERATED_TERM_EXPIRED', 'NOT = { has_country_flag = COLDWAR_USA_agreements_britain_term } NOT = { has_country_flag = COLDWAR_USA_agreements_britain_signed } NOT = { has_idea = COLDWAR_USA_agreements_britain_usa } ENG = { NOT = { has_country_flag = COLDWAR_USA_agreements_britain_signed } NOT = { has_idea = COLDWAR_USA_agreements_britain_eng } }'),
        assertion('CAN_STANDING_REMAINS', 'COLDWAR_USA_agreements_active_canada = yes'),
        'COLDWAR_USA_agreements_calculate_weekly_streams = yes',
        assertion('EXPIRED_STREAM_CLEARED', 'check_variable = { COLDWAR_USA_agreements_weekly_expense = 0 }'),
        'set_country_flag = ICW_USA_NATIVE_expiry_done',
        'log = "ICW_USA_NATIVE EXPIRY_COMPLETE"']
    events = MARKER + 'add_namespace = ICW_USA_NATIVE\n'
    events += 'country_event = { id = ICW_USA_NATIVE.1 hidden = yes is_triggered_only = yes immediate = {\n' + '\n'.join(first_hour) + '\n} }\n'
    events += 'country_event = { id = ICW_USA_NATIVE.2 hidden = yes is_triggered_only = yes immediate = {\n' + '\n'.join(expiry) + '\n} }\n'
    on_actions = MARKER + '''on_actions = {
 on_startup = { effect = {
  log = "ICW_USA_NATIVE STARTUP"
  USA = { country_event = { id = ICW_USA_NATIVE.1 hours = 1 } }
 } }
 on_daily_USA = { effect = {
  if = { limit = { has_country_flag = ICW_USA_NATIVE_first_hour_done NOT = { has_country_flag = ICW_USA_NATIVE_first_day } }
   set_country_flag = ICW_USA_NATIVE_first_day
   log = "ICW_USA_NATIVE FIRST_DAY"
  }
 } }
 on_weekly_USA = { effect = {
  if = { limit = { has_country_flag = ICW_USA_NATIVE_first_hour_done has_country_flag = ICW_USA_NATIVE_expiry_done NOT = { has_country_flag = ICW_USA_NATIVE_complete } }
   log = "ICW_USA_NATIVE FIRST_WEEK treasury=[?treasury] agreement_expense=[?COLDWAR_USA_agreements_weekly_expense]"
   set_country_flag = ICW_USA_NATIVE_complete
   log = "ICW_USA_NATIVE COMPLETE failures=[?ICW_USA_NATIVE_failures]"
  }
 } }
}
'''
    return events, on_actions


def deterministic_offer_events(snapshot, profile):
    """Only six AI weights change; production guards/effects/art stay byte exact."""
    relative = Path('events/COLDWAR_USA_1970_agreements.txt')
    original = (snapshot / relative).read_bytes().decode('utf-8')
    changed = original
    evidence = []
    for ident in ('120', '130'):
        position = changed.index('id = COLDWAR_USA_agreements.' + ident + '\n')
        start = changed.rfind('country_event', 0, position)
        opening = changed.index('{', start)
        depth, quoted, escaped, comment, end = 0, False, False, False, None
        for cursor in range(opening, len(changed)):
            char = changed[cursor]
            if comment:
                comment = char != '\n'
                continue
            if quoted:
                if escaped:
                    escaped = False
                elif char == '\\':
                    escaped = True
                elif char == '"':
                    quoted = False
                continue
            if char == '#':
                comment = True
            elif char == '"':
                quoted = True
            elif char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    end = cursor + 1
                    break
        assert end is not None
        source_event = changed[start:end]
        pattern = r'(ai_chance\s*=\s*\{\s*base\s*=\s*)(\d+)(\s*\})'
        before = [m[1] for m in re.findall(pattern, source_event)]
        assert before == ['70', '30', '0'], (ident, before)
        replacements = iter(('0', '0', '100'))
        revised = re.sub(pattern, lambda match: match[1] + next(replacements) + match[3], source_event)
        normalise = lambda text: re.sub(pattern, lambda match: match[1] + '<AI_WEIGHT>' + match[3], text)
        assert normalise(source_event) == normalise(revised), 'Non-AI event byte changed.'
        changed = changed[:start] + revised + changed[end:]
        evidence += [dict(event='COLDWAR_USA_agreements.' + ident, option=option, old=int(old), new=new) for option, old, new in zip(('accept', 'decline', 'review'), before, (0, 0, 100))]
    # Removing the six intended numeric replacements reconstructs the exact
    # original event source. No guards, option effects, previews or pictures vary.
    all_pattern = r'(ai_chance\s*=\s*\{\s*base\s*=\s*)(\d+)(\s*\})'
    normalise_all = lambda text: re.sub(all_pattern, lambda match: match[1] + '<AI_WEIGHT>' + match[3], text)
    assert normalise_all(original) == normalise_all(changed)
    old_weights = re.findall(all_pattern, original)
    new_weights = re.findall(all_pattern, changed)
    assert len(old_weights) == len(new_weights)
    assert sum(a != b for a, b in zip(old_weights, new_weights)) == 6
    target = owned(profile / 'fixture' / relative)
    target.parent.mkdir(parents=True, exist_ok=True)
    prefix_hash = hashlib.sha256(changed.encode('utf-8')).hexdigest()
    proof = ('\n# IMPERIA COLD WAR — Fixture-only event override load marker.\n'
             'add_namespace = ICW_USA_OVERRIDE\n'
             'country_event = { id = ICW_USA_OVERRIDE.1 hidden = yes is_triggered_only = yes immediate = {\n'
             ' log = "ICW_USA_NATIVE DIAG_EVENT_OVERRIDE_MARKER_LOADED=yes"\n'
             '} }\n')
    target.write_bytes((changed + proof).encode('utf-8'))
    return dict(project='IMPERIA COLD WAR', path=relative.as_posix(), runtime_sha256=digest(snapshot / relative), fixture_sha256=digest(target), original_prefix_fixture_sha256=prefix_hash, numeric_changes=evidence,
                comparison_scope='Original event-source prefix before the appended fixture-only diagnostic event.',
                non_weight_bytes_identical=True, option_effects_guards_previews_art_unchanged=True,
                appended_proof_event='ICW_USA_OVERRIDE.1', proof_log='ICW_USA_NATIVE DIAG_EVENT_OVERRIDE_MARKER_LOADED=yes',
                purpose='CAN and ENG AI choose Review in this fixture. Acceptance is exercised through unchanged production recipient helpers, not an AI choice or human click.')


def source_files():
    for name in RUNTIME:
        folder = ROOT / name
        if folder.is_dir():
            for path in folder.rglob('*'):
                if path.is_file():
                    yield path
    yield ROOT / 'descriptor.mod'


def plan():
    files = list(source_files())
    manifest = json.loads((Path(__file__).parent / 'manifest.json').read_text())
    result = dict(project='IMPERIA COLD WAR', mode='preparation plan; engine not launched',
                  runtime_directories=list(RUNTIME), asset_mode='isolated assets-only copy plus frozen runtime overlay',
                  source_assets={name: str(ROOT / name) for name in ASSETS},
                  source_files=len(files), source_bytes=sum(p.stat().st_size for p in files),
                  compiled_focuses=manifest['focuses'], executable=str(GAME / 'hoi4.exe'),
                  outputs=['runs/<unique>/snapshot', 'runs/<unique>/profile', 'runs/<unique>/freeze.json', 'runs/<unique>/native_result.json', 'runs/<unique>/native_error.log', 'runs/<unique>/native_game.log'],
                  no_launch_before_parent_final_freeze=True, maximum_launch_seconds=900,
                  tests=['actual USA1970 tree and all compiled focus-ID references', 'CAN send pending without payment/assets/spirits', 'actual CAN acceptance helper', 'duplicate ratification without repeated fees/buildings', 'all four sanction classes with both mirrored array directions on either country', 'ENG real ratification and accelerated one-day native term expiry', 'native additional income/expense consumer idempotence and nuclear 0.03 weekly delta', 'first hour, day and weekly checkpoint'],
                  excluded_evidence=['human recipient approval', 'live multiplayer', 'hover rendering', 'save/reload', 'actual 365-day endurance'])
    write(OWN / 'plan.json', json.dumps(result, indent=2) + '\n')
    return result


def profile_metadata(run, source_descriptor):
    """Retain the original mod's exact vanilla/DLC inheritance boundary."""
    snapshot, profile = run / 'snapshot', run / 'profile'
    base_name = 'IMPERIA USA native asset provider'
    frozen_name = 'IMPERIA USA frozen runtime'
    provider = owned(ASSET_PROVIDER)
    assert (provider / 'asset_manifest.json').is_file(), 'Prepare the isolated assets-only provider first.'
    assert all(not (provider / name).exists() for name in RUNTIME), 'Asset provider contains runtime code.'
    write(profile / 'mod/usa_native_assets.mod', (provider / 'descriptor.mod').read_text(encoding='utf-8-sig'))
    original_masks = re.findall(r'^\s*replace_path\s*=\s*"([^"]+)"', source_descriptor, re.M)
    # Asset masks are already applied by the first provider. Repeating map/gfx
    # masks in an overlay without those assets would hide its own asset donor.
    runtime_masks = [mask for mask in original_masks if mask.strip('/').split('/')[0] in RUNTIME]
    assert runtime_masks and all(mask in original_masks for mask in runtime_masks)
    assert all(mask.strip('/') not in {'common', 'interface', 'localisation', 'history'} for mask in runtime_masks), 'Unexpected broad source mask: review before applying.'
    frozen_descriptor = MARKER + 'name="' + frozen_name + '"\nsupported_version="1.19.*"\ndependencies={ "' + base_name + '" }\n'
    frozen_descriptor += ''.join('replace_path="' + mask + '"\n' for mask in runtime_masks)
    frozen_descriptor += 'path="' + snapshot.as_posix() + '"\n'
    write(snapshot / 'descriptor.mod', frozen_descriptor)
    write(profile / 'mod/usa_native_snapshot.mod', frozen_descriptor)
    addon = MARKER + 'name="IMPERIA USA isolated smoke fixture"\ndependencies={ "' + frozen_name + '" }\npath="' + (profile / 'fixture').as_posix() + '"\n'
    write(profile / 'mod/usa_native_fixture.mod', addon)
    write(profile / 'fixture/descriptor.mod', addon)
    write(profile / 'dlc_load.json', json.dumps({'enabled_mods': ['mod/usa_native_assets.mod', 'mod/usa_native_snapshot.mod', 'mod/usa_native_fixture.mod'], 'disabled_dlcs': []}))
    write(profile / 'settings.txt', MARKER + 'language="l_english"\ngraphics={size={x=1024 y=720} fullScreen=no borderless=no}\nmaster_volume=0\n')
    return runtime_masks


def refresh_metadata(run_id):
    assert re.fullmatch(r'[a-zA-Z0-9_-]{1,80}', run_id), run_id
    run = owned(OWN / 'runs' / run_id)
    freeze = json.loads((run / 'freeze.json').read_text())
    snapshot, profile = owned(freeze['snapshot']), owned(freeze['profile'])
    running = powershell("Get-Process -ErrorAction Stop | Where-Object { $_.ProcessName -eq 'hoi4' } | Select-Object Id,Path | ConvertTo-Json").stdout.strip()
    assert not running, 'An existing HOI4 process must remain untouched: ' + running
    assert digest(snapshot / 'descriptor.mod') == freeze['runtime_hashes']['descriptor.mod']
    assert digest(ROOT / 'descriptor.mod') == freeze['origin_runtime_hashes']['descriptor.mod'], 'Source descriptor changed since snapshot.'
    assert all(digest(profile / p) == h for p, h in freeze['fixture_hashes'].items()), 'Fixture changed since snapshot.'
    index = 1
    while (run / ('invalid_isolation_attempt_' + str(index))).exists():
        index += 1
    archive = owned(run / ('invalid_isolation_attempt_' + str(index)))
    archive.mkdir()
    for relative in ('freeze.json', 'snapshot/descriptor.mod', 'profile/mod/usa_native_assets.mod', 'profile/mod/usa_native_snapshot.mod', 'profile/mod/usa_native_fixture.mod', 'profile/dlc_load.json'):
        source = owned(run / relative)
        if source.exists():
            target = owned(archive / relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    log_source, log_target = profile / 'logs', archive / 'profile_logs'
    if log_source.exists():
        assert log_source.resolve().is_relative_to(OWN.resolve())
        assert log_target.resolve().is_relative_to(OWN.resolve())
        log_source.rename(log_target)
    for name in ('native_result.json', 'native_error.log', 'native_game.log'):
        source = owned(run / name)
        if source.exists():
            target = owned(archive / name)
            assert source.resolve().is_relative_to(OWN.resolve()) and target.resolve().is_relative_to(OWN.resolve())
            source.rename(target)
    write(archive / 'NOTICE.md', 'IMPERIA COLD WAR: invalid isolation configuration attempt.\n\nThe broad overlay replacement paths masked vanilla/DLC fallback definitions. These preserved logs are loading evidence for the invalid profile and do not establish gameplay success or a content defect. No first-hour or multiplayer result is claimed.\n')
    masks = profile_metadata(run, (ROOT / 'descriptor.mod').read_text(encoding='utf-8-sig'))
    freeze['runtime_hashes']['descriptor.mod'] = digest(snapshot / 'descriptor.mod')
    freeze['fixture_hashes'] = {p.relative_to(profile).as_posix(): digest(p) for p in (profile / 'fixture').rglob('*') if p.is_file()}
    freeze['loader_hashes'] = {p.relative_to(profile).as_posix(): digest(p) for p in [profile / 'dlc_load.json', profile / 'settings.txt', *sorted((profile / 'mod').glob('*.mod'))]}
    freeze['metadata_only_differences']['descriptor.mod']['snapshot_sha256'] = freeze['runtime_hashes']['descriptor.mod']
    provider = owned(ASSET_PROVIDER)
    freeze['asset_mode'] = 'isolated assets-only copy plus frozen runtime overlay with original targeted runtime masks'
    freeze['isolated_asset_provider'] = str(provider)
    freeze['asset_provider_manifest_sha256'] = digest(provider / 'asset_manifest.json')
    freeze['asset_provider_descriptor_sha256'] = digest(provider / 'descriptor.mod')
    freeze.pop('read_only_asset_provider', None)
    freeze['frozen_replace_paths'] = masks
    freeze['preserved_invalid_attempt'] = str(archive)
    freeze['metadata_refreshed_utc'] = datetime.now(timezone.utc).isoformat()
    freeze['runtime_verification'] = 'Original frozen runtime hashes retained; full file validation occurs before next launch. Only descriptor metadata changed.'
    write(run / 'freeze.json', json.dumps(freeze, indent=2) + '\n')
    write(run / 'NOTICE.md', 'IMPERIA COLD WAR: isolated native-engine test snapshot.\n\nRuntime scripts retain the original byte-frozen hashes. Only snapshot descriptor metadata is changed. The overlay inherits the original descriptor runtime replacement paths, preserving vanilla/DLC inheritance elsewhere. The first enabled provider supplies unchanged local assets and the original asset replacement masks. Previous invalid broad-mask logs are preserved separately. No junctions or source gameplay edits are involved.\n')
    return dict(project='IMPERIA COLD WAR', run_id=run_id, freeze_sha256=digest(run / 'freeze.json'), asset_mode=freeze['asset_mode'], targeted_runtime_masks=len(masks), runtime_files=len(freeze['runtime_hashes']), metadata_only=True, recopy_runtime=False, invalid_attempt_archive=str(archive), engine_launched=False)


def prepare(run_id, resume=False):
    assert re.fullmatch(r'[a-zA-Z0-9_-]{1,80}', run_id), run_id
    run = owned(OWN / 'runs' / run_id)
    run.mkdir(parents=True, exist_ok=resume)
    archive = archive_attempt(run) if resume else None
    snapshot, profile = run / 'snapshot', run / 'profile'
    snapshot.mkdir(exist_ok=resume)
    hashes, origin_hashes = {}, {}
    copied, unchanged = 0, 0
    for source in source_files():
        relative = source.relative_to(ROOT)
        target = snapshot / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        source_hash = digest(source)
        origin_hashes[relative.as_posix()] = source_hash
        target_hash = digest(target) if resume and target.is_file() else None
        if target_hash == source_hash:
            unchanged += 1
        else:
            if archive and target.is_file():
                previous = owned(archive / 'changed_runtime' / relative)
                previous.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target, previous)
            shutil.copy2(source, target)
            copied += 1
            target_hash = digest(target)
        hashes[relative.as_posix()] = target_hash
        if source_hash != hashes[relative.as_posix()]:
            raise RuntimeError('Source changed while snapshotting: ' + str(relative))
    # The first enabled mod supplies existing assets. Exact original targeted
    # runtime masks preserve vanilla and DLC inheritance in the frozen overlay.
    source_descriptor = (ROOT / 'descriptor.mod').read_text(encoding='utf-8-sig')
    masks = profile_metadata(run, source_descriptor)
    hashes['descriptor.mod'] = digest(snapshot / 'descriptor.mod')
    source = (snapshot / 'common/national_focus/USA_1970.txt').read_text(encoding='utf-8-sig')
    # One loaded national tree with no nested unrelated id declarations.
    focus_ids = re.findall(r'\bfocus\s*=\s*\{\s*id\s*=\s*(\S+)', source)
    expected = json.loads((Path(__file__).parent / 'manifest.json').read_text())['focuses']
    assert len(focus_ids) == len(set(focus_ids)) == expected, (len(focus_ids), expected)
    events, on_actions = fixture_sources(focus_ids)
    write(profile / 'fixture/events/ICW_USA_NATIVE.txt', events)
    write(profile / 'fixture/common/on_actions/zzzzzzzz_ICW_USA_NATIVE.txt', on_actions)
    event_override = deterministic_offer_events(snapshot, profile)
    write(run / 'NOTICE.md', 'IMPERIA COLD WAR: isolated native-engine test snapshot.\n\nRuntime scripts are byte-preserving copies of the current mod. Only descriptor metadata differs. The frozen overlay uses original targeted runtime masks and preserves vanilla/DLC fallback definitions. A first enabled provider supplies unchanged existing local assets. No junctions or source gameplay edits are involved.\n')
    fixture_hashes = {p.relative_to(profile).as_posix(): digest(p) for p in (profile / 'fixture').rglob('*') if p.is_file()}
    validation = json.loads((Path(__file__).parent / 'validation.json').read_text(encoding='utf-8'))
    task_hashes = validation.get('source_hashes', validation.get('hashes', {}))
    task_paths = [p.replace('\\', '/') for p in task_hashes]
    for path, expected_hash in task_hashes.items():
        assert digest(snapshot / path) == expected_hash, 'Frozen file does not match focused validation: ' + path
    freeze = dict(project='IMPERIA COLD WAR', run_id=run_id, snapshot=str(snapshot), profile=str(profile),
                  compiled_focuses=len(focus_ids), runtime_hashes=hashes, origin_runtime_hashes=origin_hashes, fixture_hashes=fixture_hashes,
                  loader_hashes={p.relative_to(profile).as_posix(): digest(p) for p in [profile / 'dlc_load.json', profile / 'settings.txt', *sorted((profile / 'mod').glob('*.mod'))]},
                  asset_mode='isolated assets-only copy plus frozen runtime overlay with original targeted runtime masks', frozen_replace_paths=masks,
                  isolated_asset_provider=str(ASSET_PROVIDER),
                  asset_provider_manifest_sha256=digest(ASSET_PROVIDER / 'asset_manifest.json'),
                  asset_provider_descriptor_sha256=digest(ASSET_PROVIDER / 'descriptor.mod'),
                  metadata_only_differences={'descriptor.mod': {'source_sha256': origin_hashes['descriptor.mod'], 'snapshot_sha256': hashes['descriptor.mod']}},
                  resumed=resume, copied_source_files=copied, reused_unchanged_files=unchanged,
                  previous_attempt_archive=str(archive) if archive else None,
                  task_runtime_paths=task_paths,
                  fixture_event_overrides=[event_override],
                  focused_validation_sha256=digest(Path(__file__).parent / 'validation.json'),
                  created_utc=datetime.now(timezone.utc).isoformat(), engine_launched=False)
    write(run / 'freeze.json', json.dumps(freeze, indent=2) + '\n')
    return dict(project='IMPERIA COLD WAR', prepared=str(run), freeze_sha256=digest(run / 'freeze.json'), compiled_focuses=len(focus_ids), runtime_files=len(hashes), asset_mode=freeze['asset_mode'], resumed=resume, copied_source_files=copied, reused_unchanged_files=unchanged, engine_launched=False)


def launch(run_id, freeze_sha256, duration, stop_on_failure=False):
    assert 1 <= duration <= 900, 'The native smoke launch is bounded to 900 seconds.'
    assert re.fullmatch(r'[a-zA-Z0-9_-]{1,80}', run_id), run_id
    run = owned(OWN / 'runs' / run_id)
    freeze_path = run / 'freeze.json'
    assert digest(freeze_path) == freeze_sha256, 'Freeze manifest differs from the reviewed snapshot.'
    freeze = json.loads(freeze_path.read_text())
    snapshot, profile = owned(freeze['snapshot']), owned(freeze['profile'])
    assert not (run / 'native_result.json').exists(), 'Create a new isolated run instead of reusing logs.'
    running = powershell("Get-Process -ErrorAction Stop | Where-Object { $_.ProcessName -eq 'hoi4' } | Select-Object Id,Path | ConvertTo-Json").stdout.strip()
    if running:
        raise RuntimeError('An existing HOI4 process is running. It will not be touched: ' + running)
    assert all(digest(snapshot / relative) == value for relative, value in freeze['runtime_hashes'].items()), 'Snapshot modified after freeze.'
    assert all(digest(profile / relative) == value for relative, value in freeze['fixture_hashes'].items()), 'Fixture modified after freeze.'
    assert all(digest(profile / relative) == value for relative, value in freeze.get('loader_hashes', {}).items()), 'Loader metadata modified after freeze.'
    provider = owned(freeze['isolated_asset_provider'])
    assert digest(provider / 'asset_manifest.json') == freeze['asset_provider_manifest_sha256']
    assert digest(provider / 'descriptor.mod') == freeze['asset_provider_descriptor_sha256']
    assert all(not (provider / name).exists() for name in RUNTIME), 'Asset provider contains runtime code.'
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0  # SW_HIDE
    arguments = [str(GAME / 'hoi4.exe'), '-noasserts', '-assertsdialog=no', '-userdir=' + str(profile), '-start_tag=USA', '-start_speed=5', '-hands_off']
    began = time.monotonic()
    process = subprocess.Popen(arguments, cwd=GAME, startupinfo=startup, creationflags=subprocess.CREATE_NO_WINDOW)
    stop_hiding = threading.Event()
    def hide_own_windows():
        user32 = ctypes.windll.user32
        callback_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
        def hide(hwnd, _):
            owner = ctypes.c_ulong()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(owner))
            if owner.value == process.pid:
                user32.ShowWindow(hwnd, 0)
            return True
        callback = callback_type(hide)
        while not stop_hiding.wait(0.2):
            user32.EnumWindows(callback, 0)
    hider = threading.Thread(target=hide_own_windows, daemon=True)
    hider.start()
    print(json.dumps(dict(project='IMPERIA COLD WAR', launched_pid=process.pid, profile=str(profile), hidden=True)), flush=True)
    game_log, error_log = profile / 'logs/game.log', profile / 'logs/error.log'
    observed = ''
    first_hour_failure_stop = False
    try:
        while process.poll() is None and time.monotonic() - began < duration:
            time.sleep(0.5)
            if game_log.exists():
                observed = game_log.read_text(encoding='utf-8-sig', errors='replace')
            if 'ICW_USA_NATIVE COMPLETE' in observed:
                break
            if (stop_on_failure and 'ICW_USA_NATIVE FIRST_HOUR_COMPLETE' in observed
                    and re.search(r'ICW_USA_NATIVE FAIL_', observed)):
                first_hour_failure_stop = True
                break
    finally:
        stopped_by_probe = process.poll() is None
        if stopped_by_probe:
            process.terminate()  # Only the handle created by this launch.
        try:
            process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
        stop_hiding.set()
        hider.join(timeout=1)
    if game_log.exists():
        observed = game_log.read_text(encoding='utf-8-sig', errors='replace')
    errors = error_log.read_text(encoding='utf-8-sig', errors='replace') if error_log.exists() else ''
    write(run / 'native_game.log', 'IMPERIA COLD WAR: native engine checkpoints, isolated single process.\n' + observed)
    write(run / 'native_error.log', 'IMPERIA COLD WAR: complete native diagnostics for this isolated run.\n' + errors)
    checks = [line for line in observed.splitlines() if 'ICW_USA_NATIVE' in line]
    failed = sorted(set(re.findall(r'ICW_USA_NATIVE FAIL_([A-Za-z0-9_]+)', observed)))
    passed = sorted(set(re.findall(r'ICW_USA_NATIVE PASS_([A-Za-z0-9_]+)', observed)))
    basenames = {Path(path).name.lower() for path in freeze.get('task_runtime_paths', [])}
    def task_diagnostic(line):
        lower = line.lower().replace('\\', '/')
        return (any(name in lower for name in basenames)
                or bool(re.search(r'COLDWAR_USA_1970_(programmes|agreements|expansion)|USA_X_|ICW_USA_NATIVE', line)))
    report = dict(project='IMPERIA COLD WAR', run_id=run_id, elapsed_seconds=round(time.monotonic() - began, 2),
                  stop_on_failure_requested=stop_on_failure, stopped_after_first_hour_failure=first_hour_failure_stop,
                  process_return_code=process.returncode, stopped_by_probe=stopped_by_probe,
                  first_hour_observed='ICW_USA_NATIVE FIRST_HOUR_COMPLETE' in observed,
                  accelerated_term_expiry_observed='ICW_USA_NATIVE EXPIRY_COMPLETE' in observed,
                  weekly_observed='ICW_USA_NATIVE FIRST_WEEK' in observed,
                  complete='ICW_USA_NATIVE COMPLETE' in observed, passed_checks=passed, failed_checks=failed,
                  checkpoint_lines=checks, compiled_source_focus_references=freeze['compiled_focuses'],
                  diagnostic_lines=[line for line in checks if ' DIAG_' in line],
                  task_diagnostics=[line for line in errors.splitlines() if task_diagnostic(line)],
                  task_diagnostic_scope=freeze.get('task_runtime_paths', []),
                  total_native_diagnostic_lines=len(errors.splitlines()),
                  snapshot_unchanged=all(digest(snapshot / p) == h for p, h in freeze['runtime_hashes'].items()),
                  fixture_unchanged=all(digest(profile / p) == h for p, h in freeze['fixture_hashes'].items()),
                  native_fixture_direct_acceptance=True, accelerated_term_days=1,
                  human_recipient_tested=False, live_multiplayer_tested=False, hover_tested=False, save_reload_tested=False,
                  actual_365_day_endurance_tested=False, snapshot=str(snapshot), profile=str(profile))
    report['fixture_event_overrides'] = freeze.get('fixture_event_overrides', [])
    report['asset_mode'] = freeze['asset_mode']
    report['task_diagnostic_lines'] = len(report['task_diagnostics'])
    report['external_diagnostic_lines'] = report['total_native_diagnostic_lines'] - report['task_diagnostic_lines']
    report['native_smoke_passed'] = (report['complete'] and bool(passed) and not failed
                                     and not report['task_diagnostics']
                                     and report['snapshot_unchanged'] and report['fixture_unchanged'])
    write(run / 'native_result.json', json.dumps(report, indent=2) + '\n')
    return report


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    mode = cli.add_mutually_exclusive_group(required=True)
    mode.add_argument('--plan', action='store_true')
    mode.add_argument('--prepare', action='store_true')
    mode.add_argument('--launch', action='store_true')
    mode.add_argument('--refresh-metadata', action='store_true')
    mode.add_argument('--prepare-assets', action='store_true')
    cli.add_argument('--run-id', default=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S'))
    cli.add_argument('--freeze-sha256')
    cli.add_argument('--resume', action='store_true', help='Reuse verified copies in the same task-owned run; do not delete or recreate its snapshot.')
    cli.add_argument('--duration', type=int, default=150)
    cli.add_argument('--stop-on-failure', action='store_true', help='Stop only after the complete first-hour fixture if a FAIL checkpoint was observed; preserve diagnostics and a failed result.')
    args = cli.parse_args()
    OWN.mkdir(parents=True, exist_ok=True)
    if args.plan:
        result = plan()
    elif args.prepare:
        result = prepare(args.run_id, resume=args.resume)
    elif args.prepare_assets:
        result = prepare_assets(args.run_id)
    elif args.refresh_metadata:
        result = refresh_metadata(args.run_id)
    else:
        if not args.freeze_sha256:
            cli.error('--launch requires the reviewed --freeze-sha256; prepare after the final source freeze first.')
        result = launch(args.run_id, args.freeze_sha256, args.duration, stop_on_failure=args.stop_on_failure)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
