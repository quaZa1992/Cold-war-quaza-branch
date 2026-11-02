# IMPERIA COLD WAR — Reconstruct the emitted Israel V2 native focus layout.
"""Read emitted sources independently; never invoke or write runtime compilers.

Default input is the runtime manifest and its installed files. ``render(result)``
also accepts a root-owned in-memory compiler payload for a clearly staged view.
The approved proposal and its HTML are never overwritten.
"""
from copy import deepcopy
from decimal import Decimal
import base64
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'docs/israel_1970_v2'
VIS = Path('C:/Users/Enes/.codex/visualizations/2026/10/27/01a17ef9-3adf-7210-95e8-0788b3b5a632/israel-1970-runtime.html')
WRAPPER = Path('C:/Users/Enes/.codex/plugins/cache/openai-bundled/visualize/1.0.57/skills/visualize/scripts/render.py')
sys.path.insert(0, str(ROOT / 'tools/israel_1970'))
from script_format import read


def sha(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode('utf-8')).hexdigest()


def values(rows, key):
    return [value for name, op, value in rows if name == key]


def one(rows, key, default=None):
    return next(iter(values(rows, key)), default)


def reconstruct(data, source):
    """Resolve actual native anchors and compare every visible graph contract."""
    trees = values(read(source), 'focus_tree')
    assert len(trees) == 1 and one(trees[0], 'id') == 'ISR70_focus'
    rows = values(trees[0], 'focus')
    order = {one(row, 'id'): index for index, row in enumerate(rows)}
    emitted = {one(row, 'id'): row for row in rows}
    expected = {n['id']: n for n in data['nodes']}
    assert len(emitted) == len(rows) and set(emitted) == set(expected), 'Runtime focus IDs differ'
    resolved = {}
    def position(fid, trail=()):
        assert fid in emitted and fid not in trail, ('Missing or cyclic anchor', fid, trail)
        if fid in resolved:
            return resolved[fid]
        row = emitted[fid]
        xy = [int(one(row, axis)) for axis in ('x', 'y')]
        anchor = one(row, 'relative_position_id')
        if anchor:
            assert order[anchor] < order[fid], ('Native forward anchor', fid, anchor)
            base = position(anchor, (*trail, fid))
            xy = [xy[i] + base[i] for i in (0, 1)]
        resolved[fid] = xy
        return xy
    edges = exclusions = 0
    for fid, row in emitted.items():
        n = expected[fid]
        assert position(fid) == n['xy'], ('Resolved native coordinate mismatch', fid)
        prereqs = [values(group, 'focus') for group in values(row, 'prerequisite')]
        exclusive = [p for group in values(row, 'mutually_exclusive') for p in values(group, 'focus')]
        assert prereqs == n['pre'], ('Grouped prerequisites changed', fid)
        assert sorted(exclusive) == sorted(n['exclusive']), ('Exclusive alternatives changed', fid)
        assert one(row, 'icon') == n['icon'], ('Native sprite mismatch', fid)
        assert abs(Decimal(one(row, 'cost')) * 7 - Decimal(n['days'])) <= Decimal('.00005'), ('Native duration mismatch', fid)
        assert not values(row, 'allow_branch'), ('Branch is hidden by a load-time gate', fid)
        actual = values(row, 'completion_reward')
        assert len(actual) == 1 and values(actual[0], 'hidden_effect'), ('Missing actual reward guard', fid)
        assert values(actual[0], 'effect_tooltip'), ('Missing non-executing native effect preview', fid)
        action = n['runtime_action']
        reward = read(action['reward'])
        hidden = values(actual[0], 'hidden_effect')[0]
        assert hidden[:len(reward)] == reward, ('Native actual action differs from manifest', fid)
        preview = read(action['preview'])
        expected_preview = values(preview, 'effect_tooltip')[0] if len(preview) == 1 and preview[0][0] == 'effect_tooltip' else preview
        assert values(actual[0], 'effect_tooltip')[0] == expected_preview, ('Native numeric preview differs from manifest', fid)
        edges += sum(map(len, prereqs)); exclusions += len(exclusive)
    result = deepcopy(data)
    for n in result['nodes']:
        n['xy'] = resolved[n['id']]
    return result, dict(project='IMPERIA COLD WAR', status='PASS', nodes=len(rows),
        grouped_prerequisite_edges=edges, directed_exclusion_references=exclusions,
        positions_resolved_from_emitted_code=True, forward_anchors=0,
        native_source_sha256=sha(source), engine_routing_verified=False)


def compact(data):
    """Keep inspectable content; compress view images without changing native DDS.

    WebP keeps each image's 112 x 72 dimensions and exact alpha. Colour is a
    high-quality viewing approximation; DDS pixel fidelity is audited separately.
    """
    fields = ('project', 'title', 'revision', 'version', 'default_focus', 'groups', 'starting', 'sources')
    result = {key: deepcopy(data[key]) for key in fields if key in data}
    node_fields = ('id', 'group', 'label', 'full_label', 'xy', 'days', 'description', 'icon', 'pre', 'exclusive',
                   'effects', 'requirements', 'history', 'programme')
    result['nodes'] = [{key: deepcopy(n[key]) for key in node_fields if key in n} for n in data['nodes']]
    icons = {}
    for key in sorted({n['icon'] for n in data['nodes']}):
        raw = base64.b64decode(data['layout']['icons'][key].split(',', 1)[1])
        with Image.open(io.BytesIO(raw)) as original:
            original = original.convert('RGBA')
            assert original.size == (112, 72)
            stream = io.BytesIO()
            original.save(stream, format='WEBP', quality=90, method=6, exact=True)
            with Image.open(io.BytesIO(stream.getvalue())) as decoded:
                assert decoded.size == original.size and decoded.getchannel('A').tobytes() == original.getchannel('A').tobytes(), 'View derivative changed native alpha/geometry'
            icons[key] = 'data:image/webp;base64,' + base64.b64encode(stream.getvalue()).decode('ascii')
    result['layout'] = {key: deepcopy(value) for key, value in data['layout'].items() if key != 'icons'}
    result['layout']['icons'] = icons
    return result


def render(payload=None):
    staged = payload is not None
    if payload is None:
        data = json.loads((OUT / 'runtime_design.json').read_text(encoding='utf-8'))
        manifest = json.loads((OUT / 'runtime_manifest.json').read_text(encoding='utf-8'))
        path = 'common/national_focus/ISR70_focus.txt'
        content = (ROOT / path).read_bytes()
        assert sha(content) == manifest['artifacts'][path]['sha256'], 'Installed focus file is not this manifest revision'
    else:
        data, manifest = payload['data'], payload['manifest']
        content = payload['files']['common/national_focus/ISR70_focus.txt']
        if isinstance(content, str):
            content = content.encode('utf-8')
    data, proof = reconstruct(data, content.decode('utf-8-sig'))
    proof['source_state'] = 'Staged native runtime source' if staged else 'Installed native source reconstruction'
    proof['approved_design_sha256'] = manifest['approved_design_sha256']
    view = compact(data)
    template = (HERE / 'runtime_preview.html').read_text(encoding='utf-8')
    assert template.count('<!-- DESIGN_DATA -->') == 1
    inline = template.replace('<!-- DESIGN_DATA -->', '<script type="application/json" id="isr-runtime-data">' +
        json.dumps(view, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>')
    assert len(inline.encode('utf-8')) < 1_000_000, 'Runtime inline exceeds the visualization limit'
    assert not any(tag in inline.lower() for tag in ('<!doctype', '<html', '<head>', '<body'))
    OUT.mkdir(parents=True, exist_ok=True)
    VIS.write_text(inline, encoding='utf-8')
    subprocess.run([sys.executable, str(WRAPPER), str(VIS), str(OUT / 'runtime_preview.html'), '--force'], check=True)
    wrapper = OUT / 'runtime_preview.html'
    text = wrapper.read_text(encoding='utf-8').replace('<!doctype html>', '<!doctype html>\n<!-- IMPERIA COLD WAR — Israel native runtime source reconstruction. -->', 1)
    wrapper.write_text(text, encoding='utf-8')
    proof['preview_image_approximation'] = 'WebP quality 90; dimensions and alpha preserved exactly; native DDS files unchanged'
    proof['font_approximation'] = 'Georgia preview, native hoi_16mbs remains unchanged'
    proof['inline_bytes'] = len(inline.encode('utf-8'))
    proof['inline_sha256'] = sha(inline)
    (OUT / 'runtime_preview_source_check.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    return proof


if __name__ == '__main__':
    print(json.dumps(render(), indent=2))
