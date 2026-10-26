# IMPERIA CW — Cold War: uae 1970 — validate.
"""Source, reference and approved-layout checks for installed UAE content."""
from pathlib import Path
import hashlib
import json
import re
import sys
from revision import current_design
from presentation import native_tooltip_key, POLITICAL
from focus_only import RETAINED_DECISIONS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first, values, walk

D = current_design()
M = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))
errors, count = [], 0
def check(ok, message):
    global count
    count += 1
    if not ok:
        errors.append(message)

asts, loc, sprites = {}, {}, {}
for rel, expected in M['outputs'].items():
    path = ROOT / rel
    check(path.exists(), 'Missing installed file: ' + rel)
    if not path.exists():
        continue
    raw = path.read_bytes()
    check(hashlib.sha256(raw).hexdigest() == expected, 'Output differs from compiler manifest: ' + rel)
    if path.suffix == '.yml':
        check(raw.startswith(b'\xef\xbb\xbf') and not raw.startswith(b'\xef\xbb\xbf\xef\xbb\xbf'), 'English localisation BOM: ' + rel)
        text = raw.decode('utf-8-sig')
        check(text.startswith('l_english:'), 'Wrong localisation language: ' + rel)
        for line in text.splitlines()[1:]:
            match = re.fullmatch(r'\s+([^\s:]+):\d+\s+"((?:[^"\\]|\\.)*)"\s*', line)
            check(bool(match) or not line.strip() or line.lstrip().startswith('#'), 'Malformed localisation: ' + rel + ': ' + line[:100])
            if match:
                check(match[1] not in loc, 'Duplicate English key in generated outputs: ' + match[1])
                loc[match[1]] = match[2]
    elif path.suffix in {'.txt', '.gfx'}:
        try:
            asts[rel] = parse(raw.decode('utf-8-sig'))
            check(not any(op in {'>=', '<=', '!='} for _, op, _ in walk(asts[rel])), 'Unsupported authored comparison operator: ' + rel)
        except ValueError as exc:
            errors.append(rel + ': ' + str(exc))
        if path.suffix == '.gfx':
            for key, _, body in walk(asts.get(rel, [])):
                if key.lower() == 'spritetype':
                    name = str(first(body, 'name')).strip('"')
                    check(name not in sprites, 'Duplicate generated sprite: ' + name)
                    sprites[name] = body

tree = first(asts['common/national_focus/COLDWAR_UAE_1970_focus.txt'], 'focus_tree')
focuses = values(tree, 'focus')
by = {first(f, 'id'): f for f in focuses}
approved = {n['id']: n for n in D['nodes']}
check(set(by) == set(approved) and len(focuses) == 114, 'Focus IDs differ from revised 114')
resolved = {}
def resolve(key, seen=frozenset()):
    if key in resolved:
        return resolved[key]
    check(key not in seen, 'Relative anchor cycle: ' + key)
    f = by[key]
    x, y = float(first(f, 'x')), float(first(f, 'y'))
    parent = first(f, 'relative_position_id')
    if parent:
        check(parent in by, 'Missing relative anchor: ' + key)
        px, py = resolve(parent, seen | {key})
        x, y = x + px, y + py
    resolved[key] = (x, y)
    return resolved[key]

for key, n in approved.items():
    f = by[key]
    check(resolve(key) == tuple(n['xy']), 'Position changed: ' + key)
    check(float(first(f, 'cost')) * 7 == n['days'], 'Duration changed: ' + key)
    check([values(p, 'focus') for p in values(f, 'prerequisite')] == n['prerequisites'], 'AND/OR prerequisites changed: ' + key)
    check([p for row in values(f, 'mutually_exclusive') for p in values(row, 'focus')] == n['mutually_exclusive'], 'Exclusive paths changed: ' + key)
    check(key in loc and loc[key] == n['title'], 'Focus English title changed: ' + key)
    check(bool(loc.get(key + '_desc')), 'Missing focus description: ' + key)
    check(first(f, 'icon') in sprites, 'Missing registered focus sprite: ' + key)
    reward = first(f, 'completion_reward', [])
    check([k for k, _, _ in reward] == ['effect_tooltip', 'hidden_effect'], 'Reward must preview and execute once: ' + key)
    check(first(first(reward, 'hidden_effect'), 'COLDWAR_UAE_apply_' + key.removeprefix('COLDWAR_UAE_')) == 'yes', 'Wrong actual reward helper: ' + key)
check(len(set(resolved.values())) == 114, 'Overlapping focus coordinates')

effects, triggers, dynamics, ideas, events, decisions = {}, {}, {}, {}, {}, {}
for rel, ast in asts.items():
    if '/scripted_effects/' in rel:
        effects.update({k: v for k, _, v in ast})
    if '/scripted_triggers/' in rel:
        triggers.update({k: v for k, _, v in ast})
    if '/dynamic_modifiers/' in rel:
        dynamics.update({k: v for k, _, v in ast})
    if '/ideas/' in rel:
        for _, _, category in first(ast, 'ideas', []):
            if isinstance(category, list):
                ideas.update({k: v for k, _, v in category if isinstance(v, list)})
    if rel.startswith('events/'):
        for event in values(ast, 'country_event'):
            eid = first(event, 'id')
            check(eid not in events, 'Duplicate event ID: ' + str(eid))
            events[eid] = event
    if rel.startswith('common/decisions/') and '/categories/' not in rel:
        for _, _, body in ast:
            if isinstance(body, list):
                decisions.update({k: v for k, _, v in body if isinstance(v, list)})
for d in D['decisions']:
    check(d['id'] in decisions, 'Missing approved decision: ' + d['id'])
expected_decisions = {'COLDWAR_UAE_decision_'+key for key in RETAINED_DECISIONS}
check({d['id'] for d in D['decisions']} == expected_decisions,
      'Current design must retain exactly the three approved oil/reserve decisions')
check({key for key in decisions if key.startswith('COLDWAR_UAE_decision_')} == expected_decisions,
      'Installed UAE decision catalogue contains a retired domestic/foreign action')

# Every new scripted helper, event and decision unlock has an installed provider.
for rel, ast in asts.items():
    for key, op, value in walk(ast):
        if key.startswith('COLDWAR_UAE_') and value in ('yes', 'no'):
            check(key in effects or key in triggers, 'Unresolved UAE helper: ' + key + ' in ' + rel)
        if key == 'country_event' and isinstance(value, list):
            eid = first(value, 'id')
            if str(eid).startswith('COLDWAR_UAE_'):
                check(eid in events, 'Unresolved UAE event: ' + eid)
        if key == 'unlock_decision_tooltip' and str(value).startswith('COLDWAR_UAE_'):
            check(value in decisions, 'Unresolved UAE decision unlock: ' + value)
        if key in {'add_dynamic_modifier', 'remove_dynamic_modifier'}:
            if isinstance(value, list):
                modifier = first(value, 'modifier')
            else:
                modifier = value
            if str(modifier).startswith('COLDWAR_UAE_'):
                check(isinstance(value, list), 'Dynamic modifier API needs a modifier block: ' + str(modifier))
                check(modifier in dynamics, 'Unresolved UAE dynamic modifier: ' + str(modifier))
        if key in {'custom_effect_tooltip', 'custom_trigger_tooltip'}:
            text_key = first(value, 'tooltip') if key == 'custom_trigger_tooltip' and isinstance(value, list) else first(value, 'localization_key') if isinstance(value, list) else value
            if str(text_key).startswith('COLDWAR_UAE_'):
                check(text_key in loc, 'Unresolved UAE tooltip: ' + str(text_key))

# Custom providers are real dynamic mappings, with explicit native scope gates.
programme = effects['COLDWAR_UAE_refresh_programmes']
check(not any(k in {'modify_treasury_effect', 'add_building_construction', 'add_resource', 'army_experience', 'flat_productivity_change_effect'} for k, _, _ in walk(programme)), 'Refresh must not replay one-time rewards')
for n in D['nodes']:
    key = n['id'].removeprefix('COLDWAR_UAE_')
    application = effects.get('COLDWAR_UAE_apply_' + key, [])
    check(bool(application), 'Missing application helper: ' + key)
    check(('has_country_flag', '=', 'COLDWAR_UAE_done_' + key) in list(walk(first(first(application, 'if'), 'limit'))), 'Missing replay guard: ' + key)
    for modifier, value in n['modifiers'].items():
        mapping = 'COLDWAR_UAE_' + n['group'] + '_' + modifier
        check(first(dynamics['COLDWAR_UAE_' + n['group'] + '_programme'], modifier) == mapping, 'Missing modifier consumer: ' + key + '/' + modifier)
        display = list(walk(first(first(by[n['id']], 'completion_reward'), 'effect_tooltip')))
        amount = 'COLDWAR_UAE_preview_positive_stability_delta' if n['group'] in POLITICAL and modifier == 'stability_factor' and value > 0 else f'{value:g}'
        if key in {'trading_coast', 'port_planning'} and modifier in {
                'agricolture_productivity_modifier', 'offices_productivity', 'social_cost_multiplier_modifier'}:
            amount = 'COLDWAR_UAE_preview_maritime_'+modifier
        if modifier == 'monthly_population':
            amount = 'COLDWAR_UAE_preview_population_delta'
        check(any(k == 'add_to_variable' and first(v, mapping) == amount and first(v, 'tooltip') == native_tooltip_key(modifier, D, {}) for k, _, v in display if isinstance(v, list)), 'Missing numeric native modifier preview: ' + key + '/' + modifier)

for name, body in sprites.items():
    texture = first(body, 'texturefile', first(body, 'textureFile'))
    if texture:
        relative = str(texture).strip('"').replace('\\\\', '/')
        check(any((root / relative).exists() for root in [ROOT, Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV'), Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')]), 'Missing sprite texture: ' + name)

report = {'checks': count, 'errors': errors, 'focuses': len(focuses), 'decisions': len(D['decisions']),
          'events': len(events), 'dynamic_modifiers': len(dynamics), 'sprites': len(sprites),
          'limits': 'Static source/reference validation; not an HOI4 load or multiplayer test.'}
(HERE / 'validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report))
if errors:
    raise SystemExit(1)
