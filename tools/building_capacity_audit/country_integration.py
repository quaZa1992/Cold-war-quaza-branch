# IMPERIA COLD WAR — Scoped country building-grant installation and preservation proof.
"""Apply reviewed overlays to loaded files without invoking country builders."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from focus_prerequisite_ui import nodes, field
from building_grants import grants

SSR_PATHS = (
    'common/national_focus/COLDWAR_SSR_1970_focus.txt',
    'common/scripted_effects/COLDWAR_SSR_focus_rewards.txt',
)
MARK = '# IMPERIA COLD WAR — Physical capacity for existing national building grants.\n'
COUNTRIES = ('SOV', 'DDR', 'EGY')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def walk(rows):
    for node in rows:
        yield node
        yield from walk(node.children())


def ssr_output(text):
    return grants.rewrite_queries(text, buildings={'infrastructure'})


def semantics(rows):
    return [(node.key, node.op, semantics(node.children())
             if isinstance(node.value, list) else node.value) for node in rows]


def country_preservation(tag, before, after):
    """Verify complete previews and every original country condition and price."""
    selected = set(grants.scope()[tag]['focuses'])
    old_tree = next(node for node in nodes(before) if node.key == 'focus_tree')
    new_tree = next(node for node in nodes(after) if node.key == 'focus_tree')
    old = {field(node.children(), 'id'): node for node in old_tree.children() if node.key == 'focus'}
    new = {field(node.children(), 'id'): node for node in new_tree.children() if node.key == 'focus'}
    assert old.keys() == new.keys()
    assert semantics([node for node in old_tree.children() if node.key != 'focus']) == semantics(
        [node for node in new_tree.children() if node.key != 'focus'])
    calls = 0
    for fid, previous in old.items():
        current = new[fid]
        if fid not in selected:
            assert semantics([previous]) == semantics([current]), ('Unreviewed focus changed', tag, fid)
            continue
        changed = {'available', 'completion_reward', 'cancel_if_invalid', 'continue_if_invalid'}
        assert semantics([node for node in previous.children() if node.key not in changed]) == semantics(
            [node for node in current.children() if node.key not in changed]), (tag, fid, 'Focus metadata changed')
        old_available = next((node for node in previous.children() if node.key == 'available'), None)
        new_available = next(node for node in current.children() if node.key == 'available')
        original = old_available.children() if old_available else []
        assert semantics(new_available.children()[:len(original)]) == semantics(original), (tag, fid, 'Original requirements changed')
        assert len(new_available.children()) == len(original) + 2, (tag, fid, 'Unexpected new requirements')
        prior_reward = next(node for node in previous.children() if node.key == 'completion_reward')
        reward = next(node for node in current.children() if node.key == 'completion_reward')
        assert [node.key for node in reward.children()] == ['effect_tooltip', 'hidden_effect']
        expected = before[before.index('{', prior_reward.start) + 1:prior_reward.end - 1].strip()
        expected = grants.add_missing_slots(grants.rewrite_queries(grants.rewrite_native_calls(expected)))
        assert semantics(nodes(expected)) == semantics(reward.children()[0].children()), (tag, fid, 'Original payload or price changed')
        execution = reward.children()[1].children()
        assert len(execution) == 1 and execution[0].key == grants.PREFIX + 'complete_' + fid and execution[0].value == 'yes'
        calls += sum(node.key in grants.helpers() and node.value == 'yes' for node in walk(prior_reward.children()))
    return dict(focuses=len(old), adapted_focuses=len(selected), adapted_helper_calls=calls,
                original_requirements_preserved=True, original_payload_and_prices_preserved=True,
                all_other_focus_metadata_preserved=True)


def ssr_preservation(before, after):
    """Require that each exact physical-cap substitution is the only AST change."""
    counts = Counter()

    def normalized(node, previous):
        children = node.children()
        if node.key == 'free_building_slots' and field(children, 'building') == 'infrastructure':
            assert previous, 'A manual infrastructure query survived the overlay'
            assert len(children) == 2 and field(children, 'province') is None
            size = next(child for child in children if child.key == 'size')
            assert size.op == '>' and size.value == '0'
            counts['before'] += 1
            return ('PHYSICAL_INFRASTRUCTURE_CAP', '5')
        if node.key == 'custom_trigger_tooltip' and field(children, 'tooltip') == grants.cap_key('infrastructure', 1):
            assert not previous
            assert len(children) == 2 and children[1].key == 'check_variable'
            value = children[1].children()
            assert len(value) == 3
            assert field(value, 'var') == 'building_level@infrastructure'
            assert field(value, 'value') == '5'
            assert field(value, 'compare') == 'less_than_or_equals'
            counts['after'] += 1
            return ('PHYSICAL_INFRASTRUCTURE_CAP', '5')
        return (node.key, node.op, tuple(normalized(child, previous) for child in children)
                if isinstance(node.value, list) else node.value)

    old = [normalized(node, True) for node in nodes(before)]
    new = [normalized(node, False) for node in nodes(after)]
    assert old == new, 'An unrelated scope, price, reward, party gate or receipt changed'
    assert counts['before'] == counts['after']
    return counts['after']


def install_ssr():
    report = []
    for relative in SSR_PATHS:
        path = ROOT / relative
        original = path.read_bytes()
        assert not original.startswith(b'\xef\xbb\xbf'), relative
        before = original.decode('utf-8')
        after = ssr_output(before)
        replaced = ssr_preservation(before, after) if before != after else 0
        if before != after and not after.startswith(MARK):
            after = MARK + after
        result = after.encode('utf-8')
        assert ssr_output(after) == after, relative
        if result != original:
            assert path.read_bytes() == original, 'Concurrent edit detected: ' + relative
            path.write_bytes(result)
        report.append(dict(path=relative, replaced_queries=replaced,
                           before_sha256=digest(original), after_sha256=digest(result),
                           protected_ast_preserved=True, idempotent=True))
    return report


def install_countries():
    report = []
    for tag in COUNTRIES:
        relative = grants.scope()[tag]['tree']
        path = ROOT / relative
        original = path.read_bytes()
        assert not original.startswith(b'\xef\xbb\xbf'), relative
        before = original.decode('utf-8')
        after = grants.repair_focus_tree(tag, before)
        assert grants.repair_focus_tree(tag, after) == after, (tag, 'Not idempotent')
        proof = country_preservation(tag, before, after) if before != after else dict(already_installed=True)
        result = after.encode('utf-8')
        if result != original:
            assert path.read_bytes() == original, 'Concurrent edit detected: ' + relative
            path.write_bytes(result)
        report.append(dict(country=tag, path=relative, before_sha256=digest(original),
                           after_sha256=digest(result), idempotent=True, **proof))
    return report


if __name__ == '__main__':
    assert sys.argv[1:] in (['--install-ssr'], ['--install-countries'])
    result = install_ssr() if sys.argv[1] == '--install-ssr' else install_countries()
    print(json.dumps(dict(project='IMPERIA COLD WAR', runtime=result,
                          broad_generator_run=False), indent=2))
