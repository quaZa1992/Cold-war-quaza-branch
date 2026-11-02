# IMPERIA COLD WAR — Bounded Greek and Vietnamese queue-contract adaptation.
"""Patch five reviewed contracts only. No country compiler or asset generation.

Canonical country constructors emit the same contracts. This migration updates
the current loaded files without rebuilding or replacing another chat's work.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from focus_prerequisite_ui import nodes, field
from building_grants.grants import rewrite_queries, normal

VIE = {'kiet_transport': (523, 'infrastructure'), 'industry_roads': (524, 'infrastructure'),
       'farm_dykes': (522, 'infrastructure'), 'army_airdefence': (522, 'anti_air_building')}


def walk(rows):
    for n in rows:
        yield n
        yield from walk(n.children())


def get(text, key, focus=False):
    if focus:
        return next(n for n in walk(nodes(text)) if n.key == 'focus' and field(n.children(), 'id') == key)
    return next(n for n in walk(nodes(text)) if n.key == key)


def replace(text, node, new):
    prefix = text[text.rfind('\n', 0, node.start) + 1:node.start]
    if prefix.strip():prefix = ''
    formatted = normal(new).replace('\n', '\n' + prefix)
    return text[:node.start] + formatted + text[node.end:]


def body(text, node):
    opening = text.index('{', node.start, node.end)
    return text[opening + 1:node.end - 1].strip()


def block(key, content):
    return key + ' = {\n' + content + '\n}'


def child(text, parent, key, value):
    target = next(n for n in parent.children() if n.key == key)
    return replace(text, target, block(key, value))


def slots(text, kind):
    """Only the selected payload; native slot precedes its one queued level."""
    target = next(n for n in walk(nodes(text)) if n.key == 'add_building_construction' and field(n.children(), 'type') == kind)
    parent = next(n for n in walk(nodes(text)) if target in n.children())
    if any(n.key == 'add_extra_state_shared_building_slots' for n in parent.children()):
        return text
    return text[:target.start] + 'add_extra_state_shared_building_slots = 1\n' + text[target.start:]


def viet_outputs(current):
    output = current.copy()
    effrel = 'common/scripted_effects/COLDWAR_VIE_1970_effects.txt'
    focusrel = 'common/national_focus/COLDWAR_VIE_1970_focus.txt'
    decrel = 'common/decisions/COLDWAR_VIE_1970_decisions.txt'
    for suffix, (state, kind) in VIE.items():
        fid = 'COLDWAR_VIE_' + suffix
        text = output[effrel]
        helper = get(text, 'COLDWAR_VIE_apply_' + suffix)
        source = text[helper.start:helper.end]
        assert 'COLDWAR_QUEUE_' not in source, 'Unapproved permission prototype in runtime'
        outer = next(n for n in helper.children() if n.key == 'if')
        transaction = next(n for n in outer.children() if n.key == 'if')
        limit = next(n for n in transaction.children() if n.key == 'limit')
        payload = slots(text[limit.end:transaction.end - 1].strip(), kind)
        payload = payload.replace('instant_build = no', 'instant_build = yes')
        adapted = block('if', rewrite_queries(text[limit.start:limit.end], buildings={kind}) + '\n' + payload)
        output[effrel] = replace(text, transaction, adapted)
        # Preserve actual current rewards rather than recreating modifiers or fees.
        helper = get(output[effrel], 'COLDWAR_VIE_apply_' + suffix)
        outer = next(n for n in helper.children() if n.key == 'if')
        queue_if = next(n for n in outer.children() if n.key == 'if')
        lim = next(n for n in queue_if.children() if n.key == 'limit')
        prospective = output[effrel][lim.end:queue_if.end - 1].strip()
        prospective = '\n'.join(prospective[n.start:n.end] for n in nodes(prospective)
                                if n.key not in ('set_country_flag', 'clr_country_flag'))
        for rel, key, isfocus, rewardkey in ((focusrel, fid, True, 'completion_reward'),
                                             (decrel, fid + '_retry', False, 'complete_effect')):
            text = output[rel]
            parent = get(text, key, isfocus)
            available = next(n for n in parent.children() if n.key == 'available')
            text = replace(text, available, rewrite_queries(text[available.start:available.end], buildings={kind}))
            parent = get(text, key, isfocus)
            reward = block('effect_tooltip', prospective) + '\n' + block('hidden_effect', 'COLDWAR_VIE_apply_' + suffix + ' = yes')
            output[rel] = child(text, parent, rewardkey, reward)
    return output


def greek_outputs(current):
    """Run only the single canonical pure reward constructor, never main()."""
    sys.path.insert(0, str(ROOT / 'tools/greece_1970'))
    spec = importlib.util.spec_from_file_location('queue_greek_compile', ROOT / 'tools/greece_1970/compile.py')
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    target = g.BY['economy_18']
    g.NODES = [target]
    g.EFFECTS.clear(); g.DECISIONS.clear()
    g.compile_rewards()
    output = current.copy()
    effrel = 'common/scripted_effects/COLDWAR_GRE_1970_tree_effects.txt'
    for source in g.EFFECTS:
        source = g.native_compatibility(source, effrel)
        node = nodes(source)[0]
        text = output[effrel]
        output[effrel] = replace(text, get(text, node.key), source)
    for rel, key, isfocus, rewardkey in (
        ('common/national_focus/COLDWAR_GRE_1970_focus.txt', target['id'], True, 'completion_reward'),
        ('common/decisions/COLDWAR_GRE_1970_tree_decisions.txt', g.P + 'retry_economy_18', False, 'complete_effect')):
        text = output[rel]; parent = get(text, key, isfocus)
        available = next(n for n in parent.children() if n.key == 'available')
        text = replace(text, available, rewrite_queries(text[available.start:available.end], buildings={'infrastructure'}))
        output[rel] = child(text, get(text, key, isfocus), rewardkey, g.infrastructure_reward(target, g.P + 'complete_economy_18 = yes'))
    return output


def outputs():
    paths = [f'common/{folder}/COLDWAR_{country}_1970{suffix}.txt' for country in ('GRE', 'VIE')
             for folder, suffix in (('national_focus', '_focus'), ('scripted_effects', '_tree_effects' if country == 'GRE' else '_effects'),
                                     ('decisions', '_tree_decisions' if country == 'GRE' else '_decisions'))]
    paths += ['localisation/english/COLDWAR_GRE_1970_tree_l_english.yml',
              'localisation/english/COLDWAR_VIE_1970_l_english.yml']
    current = {rel: (ROOT / rel).read_bytes().decode('utf-8-sig') for rel in paths}
    result = greek_outputs(viet_outputs(current))
    for rel in paths:
        if rel.endswith('.yml'):
            if not result[rel].splitlines()[1].startswith('# IMPERIA COLD WAR —'):
                first, _, remaining = result[rel].partition('\n')
                newline = '\r\n' if first.endswith('\r') else '\n'
                result[rel] = first + '\n# IMPERIA COLD WAR — National programme English localisation.' + newline + remaining
    for rel, source in result.items():
        if rel.endswith('.txt'):
            if not source.startswith('# IMPERIA COLD WAR —'):
                source = '# IMPERIA COLD WAR — Reviewed national construction programmes.\n' + source
                result[rel] = source
    return current, result


def apply():
    before, result = outputs()
    snapshots = {rel: source.encode('utf-8-sig' if rel.endswith('.yml') else 'utf-8') for rel, source in before.items()}
    def preflight():
        for rel, raw in snapshots.items():
            assert (ROOT / rel).read_bytes() == raw, 'Concurrent edit: ' + rel
    staged = {}
    preflight()  # Check every owned source before staging any output.
    try:
        for rel, text in result.items():
            raw = text.encode('utf-8-sig' if rel.endswith('.yml') else 'utf-8')
            if raw == snapshots[rel]:continue
            path = ROOT / rel
            with tempfile.NamedTemporaryFile(mode='wb', dir=path.parent, prefix='.icw_capacity_', suffix='.tmp', delete=False) as stream:
                staged[rel] = Path(stream.name)
                stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        preflight()  # A later-file concurrent edit cannot cause an earlier write.
        for rel, temporary in staged.items():
            assert (ROOT / rel).read_bytes() == snapshots[rel], 'Concurrent edit: ' + rel
            os.replace(temporary, ROOT / rel)
    finally:
        for temporary in staged.values():
            if temporary.exists():temporary.unlink()
    return {rel: hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() for rel in result}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    if args.apply:
        print(json.dumps({'project': 'IMPERIA COLD WAR', 'bounded_outputs': apply()}, indent=2))
    else:
        old, new = outputs()
        print(json.dumps({'project': 'IMPERIA COLD WAR', 'changed': [rel for rel, text in new.items() if old.get(rel) != text]}, indent=2))
