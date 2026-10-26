# IMPERIA CW — Cold War: vietnam 1970 — validate campaigns.
"""Independent, read-only review of the approved military expansion.

Reads installed Clausewitz AST, never imports either compiler. Native card and
connector bounds are a documented external approximation, not an engine render.
The original 239-focus approval and the 68-focus expansion are separate inputs.
Reports JSON to stdout and exits nonzero on a failed assertion; writes no files.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
from itertools import product
import hashlib
import json
import re
import copy

from PIL import Image
from script_ast import parse, first, values, walk

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
P = 'COLDWAR_VIE_'
BASE_GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')


def read(rel):
    return parse((ROOT / rel).read_text(encoding='utf-8-sig'))


def overlap(a, b):
    return max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3])


def main():
    old = json.loads((HERE / 'approved_design.json').read_text(encoding='utf-8'))
    raw_new = json.loads((HERE / 'approved_campaigns.json').read_text(encoding='utf-8'))
    new = copy.deepcopy(raw_new)
    errors, checks = [], 0

    def check(ok, message):
        nonlocal checks
        checks += 1
        if not ok:
            errors.append(message)

    # Later timing request: seventy days, with nine explicitly recorded exceptions.
    timing=json.loads((HERE/'focus_timing.json').read_text(encoding='utf-8'))
    ids={n['id'] for n in old['nodes']+new['nodes']}
    short_durations = {
        P + 'army_root': 42,
        P + 'chinh_handover': 35, P + 'guerrilla_review': 35,
        P + 'guerrilla_record': 35, P + 'cambodia_mandate': 35,
        P + 'cambodia_verify': 35, P + 'china_crisis': 35,
        P + 'china_twofront': 35,
    }
    check(timing['default_days']==70,'Default focus duration is not seventy days')
    check(len(timing['exceptions'])==8 and set(timing['exceptions'])<=ids,'Unknown or excess short-focus exceptions')
    check({k: v['days'] for k, v in timing['exceptions'].items()} == short_durations, 'Short-focus IDs/durations differ from the authorized timing policy')
    check(all(v.get('reason', '').strip() for v in timing['exceptions'].values()), 'Short-focus exception has no recorded rationale')
    for node in old['nodes']+new['nodes']:
        node['days']=timing['exceptions'].get(node['id'],{}).get('days',70)
        check(node['days'] in (35,42,70),'Unexpected focus duration: '+node['id'])

    # Independently interpret only the explicitly authorized four-policy overlay.
    # Do not use the generator's loader to construct expected values.
    override = json.loads((HERE / 'campaign_defence_overrides.json').read_text(encoding='utf-8'))
    matrix = {
        P + 'china_survey': {'max_dig_in': 1, 'dig_in_speed_factor': .10},
        P + 'china_liaison': {'max_dig_in': 2, 'dig_in_speed_factor': .15, 'army_core_defence_factor': .03},
        P + 'china_hold': {'max_dig_in': 3, 'dig_in_speed_factor': .20, 'army_core_defence_factor': .05, 'max_planning_factor': -.03},
        P + 'china_depth': {'max_dig_in': 5, 'dig_in_speed_factor': .25, 'army_core_defence_factor': .08, 'max_planning_factor': -.05},
    }
    check(hashlib.sha256((HERE / 'approved_campaigns.json').read_bytes()).hexdigest() == 'ddce90a402e021c24693adf1eb61c3c92eab2cd49f2c2b0005de8a9f25e4e7d3', 'Immutable campaign approval was rewritten')
    check(override.get('schema') == 1 and set(override.get('policies', {})) == set(matrix), 'Defence overlay exceeds four approved IDs/schema')
    for key, patch in override['policies'].items():
        check(set(patch) <= {'description', 'conditions', 'modifiers', 'terrain_training'}, 'Unexpected override field: ' + key)
        check(patch['modifiers'] == matrix[key], 'Authorized defensive modifier values differ: ' + key)
        if key.endswith(('hold', 'depth')):
            t = patch.get('terrain_training', {})
            check(set(t) == {'id', 'label', 'defence'}, 'Unexpected terrain-training overlay fields: ' + key)
            check(t.get('id') == key + '_terrain_training' and t.get('defence') == (.05 if key.endswith('hold') else .10), 'Wrong terrain training ID/value: ' + key)
        else:
            check('terrain_training' not in patch, 'Preparatory posture received unapproved terrain training: ' + key)
    for node in new['nodes']:
        patch = override['policies'].get(node['id'])
        if not patch: continue
        node['description'] = patch['description']
        node['conditions'] = node['availability_code'] = patch['conditions']
        policy = next(e for e in node['effects'] if e['type'] == 'idea')
        policy['modifiers'] = patch['modifiers'].copy()
        policy['target'], policy['targeted_modifiers'] = None, {}
        terrain = patch.get('terrain_training')
        if terrain: node['terrain_training'] = terrain.copy()
        entries = '\n'.join(f'    {k} = {v}' for k, v in patch['modifiers'].items())
        if terrain: entries += '\n    custom_modifier_tooltip = ' + node['id'] + '_terrain_tt'
        node['idea_definitions'] = node['id'] + '_policy = {\n  picture = national_defenders\n  modifier = {\n' + entries + '\n  }\n}'
    for decision in new['decisions']:
        if decision['id'] == P + 'china_decision_renew_readiness': decision['cost_risk'] = override['renewal_cost_risk']
    for node in new['nodes']:
        for decision in node.get('decisions', []):
            if decision['id'] == P + 'china_decision_renew_readiness': decision['cost_risk'] = override['renewal_cost_risk']
    from runtime_design import load_campaign_design,load_design
    if (HERE/'reward_rework.json').exists():
        revision=json.loads((HERE/'reward_rework.json').read_text(encoding='utf-8'))
        check(revision['schema']==1 and len(revision['focuses'])==239 and len(revision['campaigns'])==68,'Whole-tree reward revision lacks complete coverage')
        old=load_design();new=load_campaign_design()
        for node in new['nodes']:
            if node['id'] in matrix:
                policy=next(e for e in node['effects'] if e['type']=='idea')
                check(policy['modifiers']==matrix[node['id']],'Reward revision changed protected defensive values: '+node['id'])
    else:check(load_campaign_design() == new, 'Runtime overlay loader changed data beyond the independently authorized transformation')
    approved = {n['id']: n for n in old['nodes'] + new['nodes']}

    focus_rel = 'common/national_focus/COLDWAR_VIE_1970_focus.txt'
    tree = first(read(focus_rel), 'focus_tree')
    focus_list = values(tree, 'focus')
    focuses = {first(n, 'id'): n for n in focus_list}
    check(len(old['nodes']) == 239 and len(new['nodes']) == 68, 'Approval input cardinality differs')
    check(len(new['decisions']) == 30 and len(new['burdens']) == 5, 'Expansion action/burden count differs')
    check(len(focus_list) == len(focuses) == 307 and set(focuses) == set(approved), 'Installed focus union differs')
    duration_counts = Counter(float(first(f, 'cost')) * 7 for f in focus_list)
    check(duration_counts == {70: 299, 35: 7, 42: 1}, 'Installed duration distribution differs from 299x70, 7x35, 1x42')
    check(first(first(tree, 'initial_show_position'), 'focus') == new['layout']['initial_camera_unchanged'], 'Initial camera moved')
    continuous = first(tree, 'continuous_focus_position')
    check([int(first(continuous, k)) for k in ('x', 'y')] == [50, 1750], 'Continuous-focus gutter differs')

    @lru_cache(None)
    def xy(key, trail=()):
        if key in trail:
            raise ValueError('Relative anchor cycle: ' + key)
        node = focuses[key]
        x, y = float(first(node, 'x')), float(first(node, 'y'))
        anchor = first(node, 'relative_position_id')
        if anchor:
            ax, ay = xy(anchor, trail + (key,))
            x, y = x + ax, y + ay
        return x, y

    for key, n in approved.items():
        if key not in focuses:
            continue
        actual = focuses[key]
        check(xy(key) == (n['x'], n['y']), 'Approved coordinates changed: ' + key)
        check(float(first(actual, 'cost')) * 7 == n['days'], 'Approved duration changed: ' + key)
        check([values(g, 'focus') for g in values(actual, 'prerequisite')] == n['prerequisites'], 'AND/OR grouping changed: ' + key)
        check([q for g in values(actual, 'mutually_exclusive') for q in values(g, 'focus')] == n['exclusive'], 'Exclusivity changed: ' + key)
        check(first(actual, 'icon') == 'GFX_' + key, 'Unexpected focus art registration: ' + key)
        reward = first(actual, 'completion_reward', [])
        check([k for k, _, _ in reward] == ['log', 'effect_tooltip', 'hidden_effect'], 'Visible preview can execute/double-pay: ' + key)
        check(not any(k == 'load_focus_tree' for k, _, _ in walk(reward)), 'Completion reloads the focus tree: ' + key)
        if key in {n['id'] for n in old['nodes']}:
            check(first(reward, 'effect_tooltip') == parse(n['raw_reward_code']), 'Original focus reward preview changed: ' + key)
            check(first(reward, 'hidden_effect') == parse(n['completion_reward_code']), 'Original guarded completion changed: ' + key)
        else:
            preview=n['raw_reward_code']
            if n.get('reserve_first_term'):preview='custom_effect_tooltip = '+key+'_prepared_plan_tt\n'+preview
            check(first(reward, 'effect_tooltip') == parse(preview), 'Expansion reward preview changed: ' + key)
            check(first(reward, 'hidden_effect') == [(P + 'campaign_apply_' + key.removeprefix(P), '=', 'yes')], 'Expansion bypasses its guarded helper: ' + key)
            check(first(actual, 'relative_position_id') == n['anchor'], 'Expansion anchor changed: ' + key)
            check((float(first(actual, 'x')), float(first(actual, 'y'))) == (n['emitted_x'], n['emitted_y']), 'Emitted relative offsets changed: ' + key)
        for group in n['prerequisites']:
            check(all(parent in approved for parent in group), 'Unknown prerequisite: ' + key)
            check(all(approved[parent]['y'] < n['y'] for parent in group), 'Upward/same-row prerequisite: ' + key)

    # A focus is structurally reachable only if at least one compatible history
    # satisfies EVERY prerequisite group, with ONE member per OR group.
    @lru_cache(None)
    def histories(key):
        n = approved[key]
        alternatives = []
        for group in n['prerequisites']:
            alternatives.append([h for p in group for h in histories(p)])
        output = set()
        for selected in product(*alternatives):
            history = frozenset({key}).union(*selected)
            if not any(set(approved[k]['exclusive']) & history for k in history):
                output.add(history)
        return tuple(output)

    for key in approved:
        check(bool(histories(key)), 'No compatible prerequisite history: ' + key)
    for key in ('COLDWAR_VIE_cambodia_talks', 'COLDWAR_VIE_cambodia_limits'):
        limited = [h for h in histories(key) if P + 'cambodia_limited_commitment' in h]
        check(bool(limited), 'Limited Cambodian settlement cannot reach ' + key)
        check(any(P + 'cambodia_intervene' not in h and P + 'cambodia_aftermath' not in h for h in limited), 'Limited settlement requires military victory: ' + key)

    # Register source textures independently of the compiler's art mapping.
    sprites = {}
    shine = {}
    for rel, dest in [('interface/COLDWAR_VIE_1970_goals.gfx', sprites), ('interface/COLDWAR_VIE_1970_goals_shine.gfx', shine)]:
        for entry in values(first(read(rel), 'spriteTypes'), 'spriteType'):
            name = first(entry, 'name').strip('"')
            check(name not in dest, 'Duplicate sprite ' + name)
            dest[name] = entry
    native = {first(entry, 'name').strip('"'): first(entry, 'texturefile').strip('"')
              for entry in values(first(read('interface/goals.gfx'), 'spriteTypes'), 'spriteType')
              if first(entry, 'name') and first(entry, 'texturefile')}
    for n in new['nodes']:
        source = native.get(n['icon'], native.get('GFX_' + n['icon']))
        check(source is not None, 'Approved native source icon unresolved: ' + n['id'])
        actual = first(sprites.get('GFX_' + n['id'], []), 'texturefile', '""').strip('"')
        check(source == actual, 'Focus icon differs from approved native source: ' + n['id'])
    bounds = {}
    for key, n in approved.items():
        name = 'GFX_' + key
        check(name in sprites and name + '_shine' in shine, 'Missing registered art/shine: ' + key)
        if name not in sprites:
            continue
        texture = first(sprites[name], 'texturefile').strip('"')
        path = ROOT / texture
        check(path.exists(), 'Missing focus texture ' + texture)
        if not path.exists():
            continue
        with Image.open(path) as im:
            w, h = im.size
            box = im.convert('RGBA').getbbox() or (0, 0, w, h)
        x, y = n['x'] * 96, n['y'] * 130
        bounds[key] = [(x - w / 2 + box[0], y - h / 2 + box[1], x - w / 2 + box[2], y - h / 2 + box[3]), (x - 82, y + 20, x + 82, y + 70)]
        s = shine.get(name + '_shine', [])
        check(first(s, 'texturefile') == first(sprites[name], 'texturefile'), 'Shine texture differs: ' + key)
        check([float(first(a, 'animationrotation')) for a in values(s, 'animation')] == [-90, 90], 'Native shine rotation differs: ' + key)
        check(all(first(a, 'animationtime') == '0.75' and first(a, 'animationblendmode') == '"add"' for a in values(s, 'animation')), 'Native shine timing differs: ' + key)
    collisions = []
    for i, (a, ab) in enumerate(bounds.items()):
        for b, bb in list(bounds.items())[i + 1:]:
            if any(overlap(x, y) for x in ab for y in bb):
                collisions.append([a, b])
    check(not collisions, 'Native card collisions: ' + str(collisions))
    panel = (50, 1750, 820, 2130)
    check(not any(overlap(panel, box) for boxes in bounds.values() for box in boxes), 'Continuous-focus panel overlaps a card')

    # Full connector routing remains engine-specific. This checks the same
    # orthogonal centerline approximation as the approved native preview.
    connector_hits = []
    for n in new['nodes']:
        for parent in {p for group in n['prerequisites'] for p in group}:
            x1, y1 = approved[parent]['x'] * 96, approved[parent]['y'] * 130 + 70
            x2, y2 = n['x'] * 96, n['y'] * 130 - 40
            middle = (y1 + y2) / 2
            segments = [(x1, y1, x1, middle), (x1, middle, x2, middle), (x2, middle, x2, y2)]
            for other, cards in bounds.items():
                if other in (n['id'], parent):
                    continue
                for xa, ya, xb, yb in segments:
                    line = (min(xa, xb) - .5, min(ya, yb) - .5, max(xa, xb) + .5, max(ya, yb) + .5)
                    if any(overlap(line, box) for box in cards):
                        connector_hits.append([parent, n['id'], other])
                        break
    check(not connector_hits, 'Approximate connectors cross unrelated cards: ' + str(connector_hits))

    locpath = ROOT / 'localisation/english/COLDWAR_VIE_1970_l_english.yml'
    rawloc = locpath.read_bytes()
    check(rawloc.startswith(b'\xef\xbb\xbf'), 'English localisation BOM missing')
    loc = {k: json.loads(v) for k, v in re.findall(r'^ ([^ :]+):0 (".*")$', rawloc.decode('utf-8-sig'), re.M)}
    glyphs, kern = {}, {}
    font = BASE_GAME / 'gfx/fonts/hoi_16mbs.fnt'
    for line in font.read_text(encoding='utf-8-sig').splitlines():
        d = {k: int(v) for k, v in re.findall(r'(\w+)=(-?\d+)', line)}
        if line.startswith('char '): glyphs[d['id']] = d['xadvance']
        elif line.startswith('kerning '): kern[d['first'], d['second']] = d['amount']
    widths = {}
    for n in new['nodes']:
        key = n['id']
        check(key in loc and key + '_desc' in loc, 'Missing English focus text: ' + key)
        label = loc.get(key, '')
        width, prior = 0, None
        for char in label:
            code = ord(char)
            width += glyphs.get(code, glyphs.get(63, 8)) + kern.get((prior, code), 0)
            prior = code
        widths[key] = width
        check(width <= 147, 'Native title width exceeds 147: ' + key + ' ' + str(width))

    # Dedicated campaign outputs must parse and must never use Cameroon CAM
    # for the Cambodian recipient. Assets are checked transitively below.
    dedicated = sorted(p for folder in ('common', 'events') for p in (ROOT / folder).rglob('COLDWAR_VIE_campaign*.txt'))
    check(bool(dedicated), 'Dedicated campaign outputs missing')
    campaign_asts = {str(p.relative_to(ROOT)).replace('\\', '/'): parse(p.read_text(encoding='utf-8-sig')) for p in dedicated}
    expected_files = {
        'common/ideas/COLDWAR_VIE_campaign_ideas.txt',
        'common/technologies/COLDWAR_VIE_campaign_terrain.txt',
        'common/scripted_effects/COLDWAR_VIE_campaign_effects.txt',
        'common/scripted_triggers/COLDWAR_VIE_campaign_triggers.txt',
        'common/decisions/categories/COLDWAR_VIE_campaign_categories.txt',
        'common/decisions/COLDWAR_VIE_campaign_decisions.txt',
        'events/COLDWAR_VIE_campaign_events.txt',
        'common/on_actions/COLDWAR_VIE_campaign_on_actions.txt',
    }
    check(set(campaign_asts) == expected_files, 'Dedicated campaign output set differs')
    ideas = {}
    effects = {}
    triggers = {}
    technologies = {}
    for rel, ast in campaign_asts.items():
        check(not any(k == 'CAM' or v == 'CAM' for k, _, v in walk(ast) if isinstance(v, str)), 'Cameroon CAM used in campaign output: ' + rel)
        if rel.startswith('common/ideas/'):
            ideas.update({k: v for k, _, v in first(first(ast, 'ideas', []), 'country', [])})
        elif rel.startswith('common/scripted_effects/'):
            effects.update({k: v for k, _, v in ast})
        elif rel.startswith('common/scripted_triggers/'):
            triggers.update({k: v for k, _, v in ast})
        elif rel.startswith('common/technologies/'):
            technologies.update({k: v for k, _, v in first(ast, 'technologies', [])})

    decision_ast = campaign_asts.get('common/decisions/COLDWAR_VIE_campaign_decisions.txt', [])
    action_rows = first(decision_ast, P + 'campaign_programmes', [])
    retry_rows = first(decision_ast, P + 'campaign_deferred', [])
    actions, retries = {k: v for k, _, v in action_rows}, {k: v for k, _, v in retry_rows}
    check(len(action_rows) == len(actions) == 30 and set(actions) == {q['id'] for q in new['decisions']}, 'Actual campaign action blocks differ from approval')
    check(len(retry_rows) == len(retries) == 68 and set(retries) == {n['id'] + '_retry' for n in new['nodes']}, 'Actual deferred campaign projects differ')
    for q in new['decisions']:
        key = q['id']; action = actions.get(key, []); helper = key + '_execute'
        check(first(action, 'complete_effect') == [(helper, '=', 'yes')], 'Action does not call its own execution guard: ' + key)
        check(helper in effects, 'Action helper missing: ' + key)
        helper_rows = effects.get(helper, [])
        check([k for k, _, _ in helper_rows] == ['if'], 'Action has effects outside its execution guard: ' + key)
        guard = first(first(helper_rows, 'if', []), 'limit', [])
        check(guard == first(action, 'available', []), 'Action execution/availability guards differ: ' + key)
        check((P + 'campaign_eligible', '=', 'yes') in list(walk(guard)), 'Action misses current VIE/scenario gate: ' + key)
        check(('has_country_flag', '=', q['focus'] + '_reward_applied') in list(walk(guard)), 'Action lacks its earned provider: ' + key)
        substantive = [k for k, _, _ in walk(first(helper_rows, 'if', [])) if k not in ('limit', 'AND', 'OR', 'NOT', 'custom_effect_tooltip') and not k.startswith('has_') and not k.startswith('check_') and not k.endswith('_eligible')]
        check(any(k in ('country_event', 'set_country_flag', 'set_variable', 'clr_country_flag', 'modify_treasury_effect', 'army_experience') or k.endswith(('_send', '_activate')) for k in substantive), 'Action has no substantive programme/transaction: ' + key)
    for n in new['nodes']:
        key = n['id']; retry = retries.get(key + '_retry', [])
        check(first(retry, 'complete_effect') == [(P + 'campaign_apply_' + key.removeprefix(P), '=', 'yes')], 'Deferred project calls wrong helper: ' + key)
        check(('has_country_flag', '=', key + '_pending') in list(walk(first(retry, 'visible', []))), 'Deferred project is not tied to its own pending state: ' + key)
        check(('NOT', '=', [('has_country_flag', '=', key + '_reward_applied')]) in first(retry, 'available', []), 'Deferred project can replay applied rewards: ' + key)

    events_ast = campaign_asts.get('events/COLDWAR_VIE_campaign_events.txt', [])
    event_list = values(events_ast, 'country_event')
    event_map = {first(e, 'id'): e for e in event_list}
    check(len(event_list) == len(event_map), 'Duplicate campaign event IDs')
    for eid, event in event_map.items():
        options = values(event, 'option')
        check(bool(options), 'Campaign event has no options: ' + eid)
        check(first(event, 'is_triggered_only') == 'yes', 'Campaign choice can fire without explicit trigger: ' + eid)
        for option in options:
            check(first(option, 'name') in loc, 'Campaign option lacks English text: ' + eid)
            if first(option, 'trigger') is not None and first(option, 'if') is not None:
                check(first(option, 'trigger') == first(first(option, 'if'), 'limit'), 'Event visible option/execution guards differ: ' + eid)
    forbidden = {'declare_war_on', 'white_peace', 'annex_country', 'transfer_state', 'set_politics', 'add_equipment_to_stockpile', 'create_unit'}
    for rel, ast in campaign_asts.items():
        for k, _, v in walk(ast):
            check(k not in forbidden, 'Unapproved automatic war/territory/equipment/population effect: ' + rel + '/' + k)
            if k == 'country_event' and isinstance(v, list) and first(v, 'id'):
                check(first(v, 'id') in event_map, 'Campaign event target missing: ' + str(first(v, 'id')))
            if k.startswith(P) and k.endswith(('_execute', '_activate', '_accept', '_decline', '_send')) and not isinstance(v, list):
                check(k in effects, 'Campaign execution reference missing: ' + k)

    def expanded(rows, trail=()):
        output = []
        for k, o, v in rows:
            if k in effects:
                check(k not in trail, 'Recursive campaign effect: ' + k)
                if k not in trail:
                    output.extend(expanded(effects[k], trail + (k,)))
            else:
                output.append((k, o, v))
                if isinstance(v, list): output.extend(expanded(v, trail))
        return output

    for n in new['nodes']:
        key = n['id']
        helper = P + 'campaign_apply_' + key.removeprefix(P)
        check(helper in effects, 'Missing guarded expansion helper: ' + key)
        rows = effects.get(helper, [])
        flattened = expanded(rows)
        outer = first(rows, 'if', [])
        check(('has_country_flag', '=', key + '_reward_applied') in list(walk(first(outer, 'limit', []))), 'Missing focus replay guard: ' + key)
        check(('set_country_flag', '=', key + '_reward_applied') in flattened, 'Missing focus reward stamp: ' + key)
        check(('clr_country_flag', '=', key + '_pending') in flattened, 'Missing deferred focus cleanup: ' + key)
        for payload in parse(n['raw_reward_code']):
            check(payload in flattened, 'Approved executable payload absent: ' + key + ' / ' + payload[0])
        for idea_key, _, wanted in parse(n['idea_definitions']):
            check(idea_key in ideas, 'Approved policy idea missing: ' + idea_key)
            actual = ideas.get(idea_key, [])
            check(first(actual, 'modifier', []) == first(wanted, 'modifier', []), 'Approved policy modifiers changed: ' + idea_key)
            check(values(actual, 'targeted_modifier') == values(wanted, 'targeted_modifier'), 'Opponent-specific policy changed: ' + idea_key)
            if n['effects']:
                family = next((e['family'] for e in n['effects'] if e['type'] == 'idea'), None)
                others = [q['id'] + '_policy' for q in new['nodes'] if q['id'] != key and any(e['type'] == 'idea' and e['family'] == family for e in q['effects'])]
                check(all(('remove_ideas', '=', other) in flattened for other in others), 'Policy family replacement incomplete: ' + idea_key)
    for burden in new['burdens']:
        body = ideas.get(burden['id'], [])
        check(bool(body), 'Approved burden missing: ' + burden['id'])
        check({k: float(v) for k, _, v in first(body, 'modifier', [])} == burden['modifiers'], 'Approved burden values changed: ' + burden['id'])

    wanted_techs = {key + '_terrain_training' for key in (P + 'china_hold', P + 'china_depth')}
    check(set(technologies) == wanted_techs, 'Unexpected or missing temporary terrain technology')
    for key, amount in ((P + 'china_hold', .05), (P + 'china_depth', .10)):
        tid = key + '_terrain_training'; iid = key + '_policy'
        tech = technologies.get(tid, [])
        check([k for k, _, _ in tech] == ['allow', 'category_army'], 'Terrain bonus escaped hidden army-training scope: ' + tid)
        check(first(tech, 'allow') == [('always', '=', 'no')], 'Policy terrain bonus became researchable: ' + tid)
        check(first(tech, 'category_army') == [('forest', '=', [('defence', '=', str(amount))]), ('jungle', '=', [('defence', '=', str(amount))])], 'Terrain training values/scope differ: ' + tid)
        check(first(ideas.get(iid, []), 'on_remove') == [('hidden_effect', '=', [('set_technology', '=', [(tid, '=', '0'), ('popup', '=', 'no')])])], 'Temporary idea does not remove its own terrain technology: ' + iid)
        activate = effects.get(key + '_activate', [])
        grant = ('hidden_effect', '=', [('set_technology', '=', [(tid, '=', '1'), ('popup', '=', 'no')])])
        conditional=first(activate,'if',[])
        check(grant in conditional, 'Policy activation fails to attach its terrain training: ' + key)
        add_index = next((i for i, r in enumerate(conditional) if r[0] == 'add_timed_idea'), -1)
        removals = [i for i, r in enumerate(activate) if r[0] == 'remove_ideas']
        if_index=next((i for i,r in enumerate(activate) if r[0]=='if'),-1)
        check(bool(removals) and max(removals) < if_index and 0 < add_index < (conditional.index(grant) if grant in conditional else -1), 'Terrain activation/removal ordering can clear the newly selected posture: ' + key)
        check(tid in loc and tid + '_desc' in loc and key + '_terrain_tt' in loc, 'Temporary terrain training has no truthful English text: ' + tid)
    daily = effects.get(P + 'campaign_daily_update', [])
    for tid in wanted_techs:
        flat_daily = list(walk(daily))
        check(('has_tech', '=', tid) in flat_daily, 'Existing-save terrain reconciliation absent: ' + tid)
        check(('set_technology', '=', [(tid, '=', '0'), ('popup', '=', 'no')]) in flat_daily, 'Orphaned save terrain technology is never removed: ' + tid)
        check(('set_technology', '=', [(tid, '=', '1'), ('popup', '=', 'no')]) in flat_daily, 'Existing live paid idea cannot reconcile its terrain technology: ' + tid)
    hooks = first(campaign_asts.get('common/on_actions/COLDWAR_VIE_campaign_on_actions.txt', []), 'on_actions', [])
    for hook in ('on_startup', 'on_daily'):
        check((P + 'campaign_daily_update', '=', 'yes') in list(walk(first(hooks, hook, []))), 'Terrain reconciliation lacks lifecycle hook: ' + hook)
    for rel, ast in campaign_asts.items():
        for k, _, v in walk(ast):
            check(k != 'terrain_bonus', 'Unsupported country-idea terrain_bonus syntax emitted: ' + rel)
            if k == 'set_technology':
                check(all(tid in wanted_techs for tid, _, _ in v if tid != 'popup'), 'Campaign altered an unrelated research technology: ' + rel)
    for key, body in ideas.items():
        name = 'GFX_idea_' + first(body, 'picture')
        check(name in sprites, 'Unresolved small idea sprite: ' + key)
        if name not in sprites: continue
        texture = first(sprites[name], 'texturefile').strip('"')
        check(texture.startswith('gfx/interface/ideas/'), 'Idea uses focus-sized art: ' + key)
        with Image.open(ROOT / texture) as im:
            check(im.width <= 68 and im.height <= 68, 'Idea exceeds native small-icon bounds: ' + key)
        check(key in loc and key + '_desc' in loc, 'Missing English idea text: ' + key)

    # Native hidden_trigger suppresses implementation gates without bypassing
    # their semantics; funding is deliberately rendered with an exact amount.
    legacy_triggers = {k: v for k, _, v in read('common/scripted_triggers/COLDWAR_VIE_1970_triggers.txt')}
    all_triggers = dict(legacy_triggers, **triggers)
    check([k for k, _, _ in triggers.get(P + 'campaign_eligible', [])] == ['hidden_trigger'], 'Campaign scenario gate still exposes a custom label')
    check([k for k, _, _ in legacy_triggers.get(P + 'is_1970', [])] == ['hidden_trigger'], 'Legacy scenario gate is visible')

    def visible_rows(rows, trail=()):
        output = []
        for k, o, v in rows:
            if k == 'hidden_trigger': continue
            if k in all_triggers and k not in trail:
                output.extend(visible_rows(all_triggers[k], trail + (k,)))
            else:
                output.append((k, o, v))
                if isinstance(v, list): output.extend(visible_rows(v, trail))
        return output

    def treasury_checks(rows, label=None):
        output = []
        for k, _, v in rows:
            current = first(v, 'tooltip') if k == 'custom_trigger_tooltip' and isinstance(v, list) else label
            if k == 'check_variable' and isinstance(v, list) and first(v, 'var') == 'treasury':
                output.append((float(first(v, 'value')), first(v, 'compare'), current))
            if isinstance(v, list): output.extend(treasury_checks(v, current))
        return output

    funding_count = 0
    positive_focuses = 0
    scope_asts = dict(campaign_asts)
    scope_asts[focus_rel] = [('focus_tree', '=', tree)]
    for rel in ('common/scripted_effects/COLDWAR_VIE_1970_effects.txt',
                'common/scripted_triggers/COLDWAR_VIE_1970_triggers.txt',
                'common/decisions/COLDWAR_VIE_1970_decisions.txt',
                'events/COLDWAR_VIE_1970_events.txt'):
        scope_asts[rel] = read(rel)
    for rel, ast in scope_asts.items():
        for amount, comparison, label in treasury_checks(ast):
            funding_count += 1
            text = re.sub(r'§.', '', loc.get(label, ''))
            check(comparison == 'greater_than_or_equals', 'Funding comparison changed: ' + rel)
            check(label is not None and label in loc, 'Treasury requirement has no localized visible native tooltip: ' + rel)
            check('Treasury is at least' in text and 'billion' in text and '[?treasury|3]' in text,
                  'Treasury label lacks a concrete English threshold/current amount: ' + str(label))
            check(bool(re.search(r'(?<![\d.])' + re.escape(f'{amount:g}') + r'(?![\d.])', text)),
                  'Treasury label displays a different required amount: ' + str(label))
    for key, node in approved.items():
        available = first(focuses[key], 'available', [])
        visible = visible_rows(available)
        check(not any(k in (P + 'campaign_eligible', P + 'is_1970', 'IMP_is_1970_scenario') for k, _, _ in visible), 'Internal scenario condition remains visible: ' + key)
        check(not any(k == 'tooltip' and v == P + 'campaign_eligible_tt' for k, _, v in visible), 'Scenario custom label remains visible: ' + key)
        if node.get('cash'):
            positive_focuses += 1
            thresholds = treasury_checks(available)
            check(any(amount == node['cash'] and label in loc for amount, _, label in thresholds), 'Focus hides or changes its actual contribution condition: ' + key)

    hashes = {str(p.relative_to(ROOT)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest() for p in dedicated}
    hashes[focus_rel] = hashlib.sha256((ROOT / focus_rel).read_bytes()).hexdigest()
    report = dict(status='fail' if errors else 'pass', checks=checks, errors=errors,
                  legacy_focuses=len(old['nodes']), campaign_focuses=len(new['nodes']),
                  actions=len(new['decisions']), burdens=len(new['burdens']),
                  installed_actions=len(actions), installed_retries=len(retries), campaign_events=len(event_map),
                  card_collisions=collisions, approximate_connector_hits=connector_hits,
                  max_new_title_width=max(widths.values()), campaign_ideas=len(ideas),
                  defensive_overrides=len(matrix), temporary_terrain_technologies=len(technologies),
                  duration_distribution={str(int(k)): v for k, v in sorted(duration_counts.items())},
                  localized_funding_checks=funding_count, funded_focuses=positive_focuses,
                  approved_campaigns_sha256=hashlib.sha256((HERE / 'approved_campaigns.json').read_bytes()).hexdigest(),
                  defence_override_sha256=hashlib.sha256((HERE / 'campaign_defence_overrides.json').read_bytes()).hexdigest(),
                  hashes=hashes, engine_tested=False,
                  limits='Read-only AST, approval equality and native-asset/card-bound checks. Actual connector routing, clipping, focus UI and engine effect execution are not proven. Focused transaction tests are separate.')
    print(json.dumps(report, indent=2))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
