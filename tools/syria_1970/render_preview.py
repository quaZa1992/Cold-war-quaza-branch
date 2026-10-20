"""Render the installed Syria tree after independently resolving its output.

The display uses reviewed native assets from the manifest. Positions, graph,
availability and executable reward inspection are read from loaded game files.
Connectors and eligibility coloring remain external-preview approximations.
"""
from pathlib import Path
import argparse
import base64
import gzip
import hashlib
import json
import re
from validate_content import parse, first, vals

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def emit(items):
    return '\n'.join(str(v) if k == '_bare' else '{ '+emit(v)+' }' if k == '_list' else k+' '+op+' '+('{ '+emit(v)+' }' if isinstance(v, list) else v) for k, op, v in items)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    data = json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
    english = {}
    for path in (ROOT/'localisation/english').glob('COLDWAR_SYR*.yml'):
        for key, value in re.findall(r'^\s+([\w.]+):\d+\s+(".*")\s*$', path.read_text(encoding='utf-8-sig'), re.M):
            english[key] = json.loads(value)
    for spirit in data['starting_spirits']:
        spirit['treatment'] = english[spirit['id']+'_desc']
    source = ROOT/'common/national_focus/COLDWAR_SYR_1970_focus.txt'
    tree = first(parse(source.read_text(encoding='utf-8-sig')), 'focus_tree')
    focuses = {first(n, 'id'): n for n in vals(tree, 'focus')}
    effects = {}
    for path in (ROOT/'common/scripted_effects').glob('COLDWAR_SYR*.txt'):
        effects.update({k: v for k, _, v in parse(path.read_text(encoding='utf-8-sig')) if isinstance(v, list)})
    decisions, events = {}, {}
    for path in (ROOT/'common/decisions').glob('COLDWAR_SYR*.txt'):
        if path.stem == 'COLDWAR_SYR_deferred_projects':
            continue
        for _, _, category in parse(path.read_text(encoding='utf-8-sig')):
            for ident, _, body in category:
                if isinstance(body, list):
                    decisions[ident] = body
    for path in (ROOT/'events').glob('COLDWAR_SYR*.txt'):
        for body in vals(parse(path.read_text(encoding='utf-8-sig')), 'country_event'):
            ident = first(body, 'id')
            if ident.startswith('COLDWAR_SYR_'):
                events[ident] = body
    for decision in data['decisions']:
        body = decisions[decision['id']]
        decision['conditions'] = emit(first(body, 'available', []))
        decision['completion_reward_code'] = emit([clause for clause in body if clause[0] in ('complete_effect', 'remove_effect')])
        decision['effects'] = english[decision['id']+'_desc']
        decision['note'] = ''
    data['actual_decision_count'] = len(decisions)
    data['actual_event_count'] = len(events)
    domestic_groups = {
        1: ['opening'], 2: ['opening'], 3: ['opening', 'atassi', 'jadid'],
        4: ['parliament'], 5: ['citizenship'], 6: ['citizenship', 'darwish', 'badr'],
        7: ['fiscal'], 8: ['citizenship', 'brotherhood'], 9: ['hafez', 'rifaat'],
        10: ['rifaat'], 11: ['hafez'], 12: ['agriculture'], 28: ['baath'],
        30: ['qudsi', 'dawalibi'], 31: ['bakdash', 'faisal'],
        32: ['jamal', 'safwan'], 33: ['attar', 'saadeddin'], 34: ['military_council'],
    }
    data['events'] = []
    for ident, body in sorted(events.items()):
        number = int(ident.split('.')[-1])
        if ident.startswith('COLDWAR_SYR_POL.'):
            groups = ['outlooks'] if 20 <= number <= 27 else domestic_groups.get(number, ['opening'])
        elif ident.startswith('COLDWAR_SYR_WAR.'):
            groups = ['great_powers'] if number in (13, 14) else ['levant', 'limited_war']
        else:
            groups = ['great_powers', 'arab_world', 'levant', 'limited_war']
        options = []
        for option in vals(body, 'option'):
            option_key = first(option, 'name')
            options.append({'title': english.get(option_key, option_key),
                            'effect': english.get(option_key+'_outcome_tt', ''),
                            'conditions': emit(first(option, 'trigger', []))})
        data['events'].append({'id': ident, 'title': english[first(body, 'title')],
                               'groups': groups, 'trigger': '', 'options': options})
    positions = {}

    def resolve(key):
        if key in positions:
            return positions[key]
        node = focuses[key]
        x, y = int(first(node, 'x')), int(first(node, 'y'))
        anchor = first(node, 'relative_position_id')
        if anchor:
            ax, ay = resolve(anchor)
            x, y = x+ax, y+ay
        positions[key] = [x, y]
        return [x, y]

    for node in data['nodes']:
        key = node['id']
        if node.get('description'):
            node['note'] = node['description']
        compiled = focuses[key]
        assert resolve(key) == node['xy'], key
        assert [vals(row, 'focus') for row in vals(compiled, 'prerequisite')] == node['prerequisites'], key
        node['xy'] = resolve(key)
        node['available'] = emit(first(compiled, 'available'))
        node['icon'] = first(compiled, 'icon')
        body = effects[key+'_implement']
        # Include actual implementation and directly called country helpers so
        # the war-goal adapter is reviewable without inventing a second mapping.
        def helper_calls(items):
            found = set()
            for k, _, v in items:
                if v == 'yes' and k in effects and k not in ('COLDWAR_SYR_refresh_programmes',):
                    found.add(k)
                if isinstance(v, list):
                    found.update(helper_calls(v))
            return found
        called = helper_calls(body)
        node['executed_effect_code'] = key+'_implement = {\n'+emit(body)+'\n}'
        for helper in sorted(called):
            node['executed_effect_code'] += '\n\n'+helper+' = {\n'+emit(effects[helper])+'\n}'
        for k in ('completion_reward_code', 'reference', 'approved_previous_cost_bn', 'treasury_cost_before_revision_bn'):
            node.pop(k, None)
    data['layout']['preview_section'] = 'opening'
    data['layout']['preview_focus'] = 'COLDWAR_SYR_opening_entry'
    source_files = [source]
    for folder in ('common/scripted_effects', 'common/decisions', 'events', 'localisation/english'):
        source_files.extend((ROOT/folder).glob('COLDWAR_SYR*'))
    data['sources'] = [{'file': p.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                       for p in sorted(source_files) if p.is_file()]
    (HERE/'preview_source_hashes.json').write_text(json.dumps(data['sources'], indent=2)+'\n', encoding='utf-8')
    data['revision'] = {}
    raw = json.dumps(data, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    encoded = base64.b64encode(gzip.compress(raw, mtime=0)).decode('ascii')
    template = (HERE/'tree_fragment.html').read_text(encoding='utf-8')
    template = template.replace('Proposed Syria national focus tree', 'Installed Syria national focus tree')
    template = template.replace('CONCEPT · APPROVAL PENDING', 'IMPLEMENTED · SOURCE PREVIEW')
    template = template.replace('<!-- DESIGN_DATA -->', '<script type="application/octet-stream" id="syr70-data">'+encoded+'</script>')
    template = template.replace('(()=>{', '(async()=>{', 1)
    expression = "JSON.parse(document.getElementById('syr70-data').textContent)"
    packed = "JSON.parse(await new Response(new Blob([Uint8Array.from(atob(document.getElementById('syr70-data').textContent),c=>c.charCodeAt(0))]).stream().pipeThrough(new DecompressionStream('gzip'))).text())"
    assert expression in template
    template = template.replace(expression, packed, 1)
    template = re.sub(r'function effectCode\(n\)\{.*?(?=function paint\()', 'function effectCode(n){return n.executed_effect_code;}\n', template, count=1, flags=re.S)
    template = template.replace('Proposed rewards and costs', 'Implemented rewards and costs').replace('Exact proposed MD effect mapping', 'Installed MD effect code')
    template = template.replace('COLDWAR_SYR adapters and variables are new proposed script. Native modifier keys and APIs are source-checked; these focus effects are not installed.', 'Read from installed scripts. Native effect providers are source-checked; HOI4 runtime behavior remains untested.')
    template = template.replace('proposed tree', 'installed tree').replace('Entire proposed tree', 'Entire installed tree')
    template = template.replace('Proposed decision or offer handoff', 'Design contract for decision or offer')
    template = re.sub(r'function renderEvents\(group\)\{.*?(?=function update\()', '''function renderEvents(group){
 const relevant=(D.events||[]).filter(e=>(e.groups||[]).includes(group));
 root.querySelector('#syr70-events').innerHTML=relevant.length?relevant.map(e=>`<details><summary>${esc(e.title)}</summary><ul>${e.options.map(o=>`<li>${esc(o.title)} — ${esc(o.effect)}</li>`).join('')}</ul></details>`).join(''):'<p>No events are assigned to this section.</p>';
}
''', template, count=1, flags=re.S)
    template = template.replace('${D.decisions.length} decisions · ${(D.events||[]).length} new events', '${D.actual_decision_count} decisions · ${D.actual_event_count} new events')
    assert len(template.encode('utf-8')) < 1_000_000
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(template, encoding='utf-8')
    print(json.dumps({'fragment_bytes': len(template.encode()), 'focuses': len(focuses), 'output': str(args.output)}))


if __name__ == '__main__':
    main()
