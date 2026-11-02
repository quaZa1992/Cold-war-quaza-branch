# IMPERIA COLD WAR — Israel V2 legacy callback isolation and reservation refunds.
"""Pure, freshly read patch emitter. Never write game files from this module.

Known unfinished reservations are refundable, but focus progress and completed
legacy projects are deliberately not migrated. Egypt's independent canal
callback ISR70P.1160 remains byte-for-byte unchanged inside its event block.
"""
from __future__ import annotations

from pathlib import Path
from textwrap import indent
import ast
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[2]
TOOLS = str(ROOT / 'tools')
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from focus_prerequisite_ui import nodes, field

MARK = '# IMPERIA COLD WAR — Israel V2 legacy event isolation and reservation refunds.\n'
OCC_MARK = '# IMPERIA COLD WAR — Israel V2 legacy occupation scope integration.\n'
BLOCK_MARK = '# IMPERIA COLD WAR — Retired Israel callback guard.'
EVENT_PATHS = ('events/ISR70_events.txt', 'events/ISR70_policy_events.txt')
EFFECT_PATHS = ('common/scripted_effects/ISR70_effects.txt',
                'common/scripted_effects/ISR70_policy_effects.txt')
OCCUPATION_PATHS = ('common/dynamic_modifiers/ISR70_policy_dynamic_modifiers.txt',
                    'tools/israel_1970/occupation_profiles.py')
EXEMPT = 'ISR70P.1160'
ACTOR_ENABLED = 'ISR = { tag = ISR has_country_flag = ISR2_enabled }'
ENABLED = 'OR = { has_global_flag = ISR2_legacy_replaced ' + ACTOR_ENABLED + ' }'
ALLOWED = 'NOT = { ' + ENABLED + ' }'
DISMISS = 'ISR2_legacy_dismiss'
OPTION_METADATA = {'name', 'trigger', 'ai_chance', 'highlight', 'default_hide_option',
                   'original_recipient_only', 'is_ai', 'ai_will_do'}


def block(key, body):
    return key + ' = {\n' + indent(body.strip(), '\t') + '\n}'


def walk(rows):
    for row in rows:
        yield row
        yield from walk(row.children())


def semantic(rows):
    return tuple((n.key, n.op, semantic(n.children()) if n.children() else n.value) for n in rows)


GUARD_FORM = semantic(nodes(ALLOWED))
ENABLED_FORM = semantic(nodes(ENABLED))
OLD_GUARD_FORM = semantic(nodes('NOT = { ' + ACTOR_ENABLED + ' }'))
OLD_ENABLED_FORM = semantic(nodes(ACTOR_ENABLED))


def guarded_body(rows):
    if len(rows) != 1 or rows[0].key != 'if':
        return False
    limit = next((n for n in rows[0].children() if n.key == 'limit'), None)
    return limit is not None and semantic(limit.children()) == GUARD_FORM


def contains_guard(rows):
    return any(semantic([row]) == GUARD_FORM for row in rows)


def _upgrade_actor_guards(source):
    """Upgrade an earlier private-beta patch without growing nested guards."""
    edits = []
    for event in nodes(source):
        if field(event.children(), 'id') == EXEMPT:
            continue
        for row in walk(event.children()):
            if semantic([row]) == OLD_GUARD_FORM:
                edits.append((row.start, row.end, ALLOWED))
            elif row.key == 'trigger' and semantic(row.children()) == OLD_ENABLED_FORM:
                # This is the old effect-free closing option's condition.
                prefix = _indent_at(source, row.start)
                replacement = block('trigger', ENABLED).replace('\n', '\n' + prefix)
                edits.append((row.start, row.end, replacement))
    for start, end, replacement in sorted(edits, reverse=True):
        source = source[:start] + replacement + source[end:]
    return source


def _indent_at(source, position):
    start = source.rfind('\n', 0, position) + 1
    prefix = source[start:position]
    assert not prefix.strip(), ('Expected a standalone generated effect field', prefix)
    return prefix


def _wrap_effect_span(source, effect_rows):
    first, last = effect_rows[0], effect_rows[-1]
    prefix = _indent_at(source, first.start)
    lines = source[first.start:last.end].splitlines()
    original = '\n'.join([lines[0]] + [line[len(prefix):] if line.startswith(prefix) else line for line in lines[1:]])
    guarded = BLOCK_MARK + '\n' + block('if', block('limit', ALLOWED) + '\n' + original)
    return first.start, last.end, guarded.replace('\n', '\n' + prefix)


def patch_events(source):
    """Guard both registration and executable bodies, preserving unrelated text."""
    edits, protected, options, immediates, dismissals = [], [], 0, 0, 0
    exempt = next((n for n in nodes(source) if field(n.children(), 'id') == EXEMPT), None)
    exempt_before = source[exempt.start:exempt.end] if exempt else None
    source = _upgrade_actor_guards(source)
    for event in nodes(source):
        if not event.children():
            continue
        assert event.key == 'country_event', ('Unexpected event schema', event.key)
        body = event.children()
        event_id = field(body, 'id')
        if event_id == EXEMPT:
            continue
        assert event_id and str(event_id).startswith(('ISR70.', 'ISR70P.')), event_id
        protected.append(event_id)
        trigger = next((n for n in body if n.key == 'trigger'), None)
        if trigger is None:
            addition = '\n\t' + block('trigger', ALLOWED).replace('\n', '\n\t') + '\n'
            edits.append((event.end-1, event.end-1, addition))
        elif not contains_guard(trigger.children()):
            prefix = _indent_at(source, trigger.start)
            addition = '\n' + prefix + '\t' + BLOCK_MARK + '\n'
            addition += indent(ALLOWED, prefix + '\t') + '\n' + prefix
            edits.append((trigger.end-1, trigger.end-1, addition))

        for child in body:
            if child.key == 'immediate':
                effect_rows = child.children()
                if effect_rows and not guarded_body(effect_rows):
                    edits.append(_wrap_effect_span(source, effect_rows))
                immediates += 1
            if child.key != 'option':
                continue
            if field(child.children(), 'name') == DISMISS:
                dismiss_trigger = next((n for n in child.children() if n.key == 'trigger'), None)
                assert dismiss_trigger and semantic(dismiss_trigger.children()) == ENABLED_FORM
                assert all(n.key in OPTION_METADATA for n in child.children())
                continue
            option_trigger = next((n for n in child.children() if n.key == 'trigger'), None)
            if option_trigger is None:
                prefix = _indent_at(source, child.start)
                addition = '\n' + prefix + '\t' + block('trigger', ALLOWED).replace('\n', '\n' + prefix + '\t') + '\n' + prefix
                edits.append((child.end-1, child.end-1, addition))
            elif not contains_guard(option_trigger.children()):
                prefix = _indent_at(source, option_trigger.start)
                addition = '\n' + prefix + '\t' + BLOCK_MARK + '\n'
                addition += indent(ALLOWED, prefix + '\t') + '\n' + prefix
                edits.append((option_trigger.end-1, option_trigger.end-1, addition))
            # The original compiler sometimes places an AI weight between a
            # prospective effect preview and the actual transaction. Preserve
            # that metadata in place and guard each contiguous effect run.
            runs, current = [], []
            for entry in child.children():
                if entry.key in OPTION_METADATA:
                    if current:
                        runs.append(current); current = []
                else:
                    current.append(entry)
            if current:
                runs.append(current)
            for run in runs:
                assert run[0].key not in ('else', 'else_if'), ('Split conditional option metadata', event_id)
                if not guarded_body(run):
                    edits.append(_wrap_effect_span(source, run))
            if runs:
                options += 1
        if field(body, 'hidden') != 'yes' and not any(n.key == 'option' and field(n.children(), 'name') == DISMISS for n in body):
            addition = '\n\t' + block('option', 'name = ' + DISMISS + '\n' +
                block('trigger', ENABLED) + '\nai_chance = { base = 100 }').replace('\n', '\n\t') + '\n'
            edits.append((event.end-1, event.end-1, addition))
            dismissals += 1
    for start, end, replacement in sorted(edits, key=lambda row: (row[0], row[1]), reverse=True):
        source = source[:start] + replacement + source[end:]
    if not source.startswith(MARK):
        source = MARK + source
    if exempt_before is not None:
        event = next(n for n in nodes(source) if field(n.children(), 'id') == EXEMPT)
        assert source[event.start:event.end] == exempt_before, 'Egyptian canal event changed'
    return source, dict(protected_events=protected, guarded_option_bodies=options,
                       guarded_immediates=immediates, new_dismissals=dismissals)


def patch_occupation_register(source):
    """Change only four demonstrated invalid enable scopes, never their values."""
    edits, found = [], []
    for definition in nodes(source):
        targets = {f'ISR70_policy_occupation_{s}_local': s for s in (208, 209, 213, 587)}
        if definition.key not in targets:
            continue
        state = targets[definition.key]
        found.append(state)
        enable = next(n for n in definition.children() if n.key == 'enable')
        expected = nodes('is_controlled_by = ISR NOT = { is_core_of = ISR }')
        bare = [n for n in enable.children() if n.key == 'is_controlled_by' or
                (n.key == 'NOT' and any(c.key == 'is_core_of' for c in n.children()))]
        if not bare:
            wrapper = next((n for n in enable.children() if n.key == str(state)), None)
            assert wrapper and semantic(wrapper.children()) == semantic(expected), definition.key
            continue
        assert semantic(bare) == semantic(expected), definition.key
        assert all(not(bare[0].start < n.start < bare[-1].end) or n in bare for n in enable.children()), definition.key
        prefix = _indent_at(source, bare[0].start)
        lines = source[bare[0].start:bare[-1].end].splitlines()
        body = '\n'.join([lines[0]] + [line[len(prefix):] if line.startswith(prefix) else line for line in lines[1:]])
        replacement = '# IMPERIA COLD WAR — Explicit state scope for legacy occupation.\n' + block(str(state), body)
        replacement = replacement.replace('\n', '\n' + prefix)
        edits.append((bare[0].start, bare[-1].end, replacement))
    assert sorted(found) == [208, 209, 213, 587], found
    for start, end, replacement in sorted(edits, reverse=True):
        source = source[:start] + replacement + source[end:]
    return source if source.startswith(OCC_MARK) else OCC_MARK + source


def patch_occupation_template(source):
    """Repair the owning state_gate expression without rebuilding old content."""
    assignments = [n for n in ast.walk(ast.parse(source)) if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'state_gate' for t in n.targets)]
    assert len(assignments) == 1, len(assignments)
    assignment = assignments[0]
    desired = ("state_gate = (f'{state} = {{ is_controlled_by = ISR NOT = {{ is_core_of = ISR }} }}\\n'\n"
               "                      'ISR = { tag = ISR ISR70_is_scenario = yes }')")
    wanted = ast.parse(desired).body[0]
    if ast.dump(assignment.value) != ast.dump(wanted.value):
        assert isinstance(assignment.value, ast.Constant) and assignment.value.value == (
            'is_controlled_by = ISR\nNOT = { is_core_of = ISR }\n'
            'ISR = { tag = ISR ISR70_is_scenario = yes }'), 'Unexpected occupation state_gate template'
        lines = source.splitlines(keepends=True)
        start = sum(map(len, lines[:assignment.lineno-1])) + assignment.col_offset
        end = sum(map(len, lines[:assignment.end_lineno-1])) + assignment.end_col_offset
        source = source[:start] + desired + source[end:]
    return source if source.startswith(OCC_MARK) else OCC_MARK + source


def reservations(event_sources, effect_sources):
    """Derive exact paid/active/done pairs from live callback and start effects."""
    effects = [n for source in effect_sources.values() for n in nodes(source) if n.children()]
    records = {}
    for source in event_sources.values():
        for event in nodes(source):
            event_id = field(event.children(), 'id')
            if not event_id or event_id == EXEMPT:
                continue
            body = list(walk(event.children()))
            paid = {n.value for n in body if n.key == 'clear_variable' and isinstance(n.value, str)
                    and n.value.startswith(('ISR70_policy_project_', 'ISR70_project_')) and n.value.endswith('_paid')}
            for value in paid:
                stem = value[:-5]
                active, done = stem + '_active', stem + '_done'
                assert any(n.key == 'has_country_flag' and n.value == active for n in body), (event_id, active)
                assert any(n.key == 'set_country_flag' and n.value == done for n in body), (event_id, done)
                assert any(n.key == 'treasury_change' and n.value == value for n in body), (event_id, value)
                witnesses = []
                for effect in effects:
                    descendants = list(walk(effect.children()))
                    assigned = any(n.key == 'set_variable' and field(n.children(), value) is not None for n in descendants)
                    activated = any(n.key == 'set_country_flag' and n.value == active for n in descendants)
                    scheduled = any(n.key == 'country_event' and field(n.children(), 'id') == event_id for n in descendants)
                    if assigned and activated and scheduled:
                        witnesses.append(effect.key)
                assert witnesses, ('No actual paid start transaction for callback', event_id, value)
                assert value not in records, ('Duplicate reservation callback', value)
                records[value] = dict(paid=value, active=active, done=done,
                                      callback=event_id, start_effects=witnesses)
    assert len(records) == 40, ('Unexpected legacy reservation inventory', len(records))
    return list(sorted(records.values(), key=lambda row: row['paid']))


def refund_effect(records):
    lines = []
    for record in records:
        eligibility = 'has_country_flag = ' + record['active'] + '\n'
        eligibility += 'NOT = { has_country_flag = ' + record['done'] + ' }\n'
        eligibility += 'has_variable = ' + record['paid']
        # Clear the proven claim before native payment, so a fiscal refresh
        # cannot replay the same balance. MD_skip is checked before any mutation.
        transaction = 'set_variable = { ISR2_legacy_pending_refund = ' + record['paid'] + ' }\n'
        transaction += 'clear_variable = ' + record['paid'] + '\nclr_country_flag = ' + record['active'] + '\n'
        transaction += 'set_temp_variable = { treasury_change = ISR2_legacy_pending_refund }\n'
        transaction += 'modify_treasury_effect = yes\nclear_variable = ISR2_legacy_pending_refund'
        positive = block('if', block('limit', 'check_variable = { ' + record['paid'] + ' > 0 }') + '\n' + transaction)
        lines.append(block('if', block('limit', eligibility) + '\n' + positive))
    guard = 'tag = ISR\nhas_country_flag = ISR2_enabled\nNOT = { has_country_flag = MD_skip_treasury_cost }'
    return MARK + block('ISR2_legacy_refund_pending', block('if', block('limit', guard) + '\n' + '\n'.join(lines))) + '\n'


def build(root=None, *, sources=None):
    """Read current sources, returning patches and one exact reservation helper."""
    root = Path(root) if root else ROOT
    overrides = sources or {}
    def read(path):
        return overrides[path] if path in overrides else (root / path).read_bytes().decode('utf-8-sig')
    event_sources = {path: read(path) for path in EVENT_PATHS}
    effect_sources = {path: read(path) for path in EFFECT_PATHS}
    occupation_sources = {path: read(path) for path in OCCUPATION_PATHS}
    records = reservations(event_sources, effect_sources)
    files, inventory = {}, {}
    for path, source in event_sources.items():
        files[path], inventory[path] = patch_events(source)
    files['common/scripted_effects/ISR2_legacy_effects.txt'] = refund_effect(records)
    files[OCCUPATION_PATHS[0]] = patch_occupation_register(occupation_sources[OCCUPATION_PATHS[0]])
    files[OCCUPATION_PATHS[1]] = patch_occupation_template(occupation_sources[OCCUPATION_PATHS[1]])
    call = 'ISR2_legacy_refund_pending = yes'
    return dict(files=files, loc={DISMISS: 'Close the withdrawn proposal.'}, refund=call,
        helpers={'refund': call}, init=call, refresh=call,
        metadata=dict(project='IMPERIA COLD WAR', protected_events=sum(len(x['protected_events']) for x in inventory.values()),
            exempt_event=EXEMPT, reservations=records, inventory=inventory,
            source_sha256={path: hashlib.sha256(source.encode('utf-8')).hexdigest()
                           for path, source in (event_sources | effect_sources | occupation_sources).items()},
            permanent_event_marker='ISR2_legacy_replaced',
            occupation_scope_states=[208, 209, 213, 587],
            native_gameplay_tested=False,
            scope='Event isolation and proven unpaid delivery reservations only; no focus-progress migration.'))
