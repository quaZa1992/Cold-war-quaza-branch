# IMPERIA COLD WAR — Atomic native naval construction snippets.
"""Pure country-scope snippets for the country naval adaptation compiler.

No file is written. The caller owns quotations, country focus receipts and
pending retries. The ordinary yard quote is one level; yard_2_quote is its
separately derived two-level package price. Refresh prices before execution.
The preview selects the same first feasible target as execution, with the first
declared target as its unconditional fallback when all candidates are blocked.
"""
from __future__ import annotations

from collections.abc import Mapping
import importlib.util
from pathlib import Path
import re
from textwrap import indent

ROOT = Path(__file__).resolve().parents[2]


def _capacity_api():
    path = ROOT / 'tools/usa_1970_expansion/usa_building_capacity.py'
    spec = importlib.util.spec_from_file_location('naval_native_building_capacity', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _block(key: str, content: str) -> str:
    return key + ' = {\n' + indent(content.strip(), '\t') + '\n}'


def _quote(tag: str, kind: str, count: int) -> str:
    field = 'yard_2' if kind == 'yard' and count == 2 else kind
    return f'COLDWAR_NAVY_{tag}_{field}_quote'


def asset_package(profile: Mapping, kind: str, count: int = 1) -> dict[str, str]:
    """Return authoritative ready/execution and a nonexecuting native preview.

    Candidate order is explicit priority. A whole two-yard package uses one
    state with capacity for both levels; there is no partial two-state grant.
    Port transactions also require the current ROOT to control the real port
    province. The caller should execute the country helper with that country's
    ROOT, as its focus/daily retry does; foreign roots fail closed.
    """
    assert isinstance(profile, Mapping)
    tag = profile['country'];variant = profile['variant'].replace('_', '')
    assert re.fullmatch(r'[A-Z]{3}', tag), tag
    assert variant in ('bluewater', 'coastal'), variant
    assert kind in ('port', 'yard', 'arms'), kind
    assert type(count) is int and count in (1, 2)
    assert kind == 'yard' or count == 1
    capacity = _capacity_api()
    building = {'port': 'naval_base', 'yard': 'dockyard', 'arms': 'arms_factory'}[kind]
    candidates = list(profile['port_targets' if kind == 'port' else 'yard_targets'])
    assert candidates, (tag, kind, 'No declared construction target')
    assert len({(int(c['state']), int(c.get('province', 0))) for c in candidates}) == len(candidates)
    quote = _quote(tag, kind, count)
    paid = kind != 'arms'
    # The user's existing UAE national-focus policy permits deficit finance.
    # This explicit country opt-in never weakens another profile's invoice.
    allow_deficit = tag == 'UAE' and profile.get('allow_deficit') is True
    common = [f'tag = {tag}', 'controls_a_coastal_state = yes', 'NOT = { has_country_flag = MD_skip_treasury_cost }']
    if paid:
        common += [f'check_variable = {{ {quote} > 0 }}']
        if variant == 'coastal':
            common.append('check_variable = { gdp_total > 0 }')
        if not allow_deficit:
            common.append(f'check_variable = {{ var = treasury value = {quote} compare = greater_than_or_equals }}')
    gates = [];grants = []
    for candidate in candidates:
        sid = int(candidate['state']);assert sid > 0
        province = int(candidate['province']) if kind == 'port' else None
        if province is not None:assert province > 0
        state_gate = [f'is_owned_and_controlled_by = {tag}']
        if kind != 'arms':state_gate.append('is_coastal = yes')
        state_gate.append(capacity.capacity_trigger(building, count, province))
        country_gate = [f'owns_state = {sid}', f'controls_state = {sid}']
        if province is not None:
            country_gate += [f'controls_province = {province}', _block('ROOT', f'controls_province = {province}')]
        country_gate.append(_block(str(sid), '\n'.join(state_gate)))
        gates.append('\n'.join(country_gate))
        province_arg = f' province = {province}' if province is not None else ''
        grants.append(_block(str(sid), f'add_extra_state_shared_building_slots = {count}\nadd_building_construction = {{ type = {building} level = {count}{province_arg} instant_build = yes }}'))
    readiness = '\n'.join(common + [_block('OR', '\n'.join(_block('AND', gate) for gate in gates))])
    payment = '' if not paid else (f'set_temp_variable = {{ treasury_change = {quote} }}\n'
        'multiply_temp_variable = { treasury_change = -1 }\nmodify_treasury_effect = yes\n')
    branches = []
    for i, (gate, grant) in enumerate(zip(gates, grants)):
        branches.append(_block('if' if i == 0 else 'else_if', _block('limit', gate) + '\n' + payment + grant))
    execute = _block('if', _block('limit', readiness) + '\n' + '\n'.join(branches))
    preview_plan = [
        _block('if' if i == 0 else 'else_if', _block('limit', gate) + '\n' + grant)
        for i, (gate, grant) in enumerate(zip(gates, grants))
    ]
    preview_plan.append(_block('else', grants[0]))
    preview = _block('effect_tooltip', payment + '\n'.join(preview_plan))
    return {'ready': readiness, 'execute': execute, 'preview': preview}
