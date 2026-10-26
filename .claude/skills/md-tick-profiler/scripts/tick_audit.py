#!/usr/bin/env python3
"""Static tick audit for an HOI4 mod: what the recurring on_action hooks run.

Builds a call tree from the clock hooks (on_daily, on_weekly, on_monthly and their
_TAG variants) through scripted effects, scripted triggers and fired events, sized by
script statements ("ops"). It is a proxy for cost, never measured time.

Standard library only. Run from the mod root:

    python -X utf8 .claude/skills/md-tick-profiler/scripts/tick_audit.py
    python -X utf8 .claude/skills/md-tick-profiler/scripts/tick_audit.py --cadence daily --top 15
    python -X utf8 .claude/skills/md-tick-profiler/scripts/tick_audit.py --tag ICE
    python -X utf8 .claude/skills/md-tick-profiler/scripts/tick_audit.py --spot-check
    python -X utf8 .claude/skills/md-tick-profiler/scripts/tick_audit.py --json out.json --html out.html
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

CLOCK = re.compile(r'^on_(daily|weekly|monthly)(?:_([A-Z][A-Z0-9]{2}))?$')
EVENT_KINDS = ('country_event', 'news_event', 'state_event', 'unit_leader_event',
               'operative_leader_event')
TOKEN = re.compile(r'#[^\n]*|"(?:\\.|[^"\\])*"|[{}]|[<>!]=|[<>=]|[^\s{}=<>#"]+')
LOOP_SCOPES = {
    'every_country': 'all countries', 'all_country': 'all countries',
    'random_country': 'all countries (until hit)', 'any_country': 'all countries',
    'every_other_country': 'all countries', 'any_other_country': 'all countries',
    'every_state': 'all states', 'all_state': 'all states', 'any_state': 'all states',
    'random_state': 'all states (until hit)',
    'every_owned_state': 'owned states', 'any_owned_state': 'owned states',
    'random_owned_state': 'owned states (until hit)',
    'every_controlled_state': 'controlled states', 'every_core_state': 'core states',
    'every_neighbor_country': 'neighbours', 'any_neighbor_country': 'neighbours',
    'every_enemy_country': 'enemies', 'every_allied_country': 'allies',
    'every_subject_country': 'subjects', 'every_unit_leader': 'unit leaders',
    'every_character': 'characters', 'every_country_with_original_tag': 'tag copies',
    'for_each_loop': 'array', 'for_each_scope_loop': 'array', 'for_loop_effect': 'counter',
    'while_loop_effect': 'while', 'every_possible_country': 'all possible countries',
}
GLOBAL_LOOPS = {'all countries', 'all states', 'all possible countries',
                'all countries (until hit)', 'all states (until hit)'}
HEAVY_EFFECTS = {
    'create_country_leader': 'creates a leader every run',
    'force_update_dynamic_modifier': 'forces a modifier refresh',
    'add_dynamic_modifier': 'adds a dynamic modifier',
    'set_politics': 'changes politics',
    'update_party_name': 'refreshes party names',
    'set_cosmetic_tag': 'changes cosmetic tag',
}
CADENCE_WEIGHT = {'daily': 30, 'weekly': 4, 'monthly': 1}


class Stmt:
    __slots__ = ('key', 'op', 'value', 'line')

    def __init__(self, key, op, value, line):
        self.key, self.op, self.value, self.line = key, op, value, line


def tokenize(text):
    line = 1
    pos = 0
    for m in TOKEN.finditer(text):
        line += text.count('\n', pos, m.start())
        pos = m.start()
        tok = m.group(0)
        if tok.startswith('#'):
            continue
        yield tok, line


def parse(text):
    """Return a list of Stmt; values are str or list[Stmt]. Tolerates stray braces."""
    toks = list(tokenize(text))
    i = 0

    def block():
        nonlocal i
        out = []
        while i < len(toks):
            tok, line = toks[i]
            if tok == '}':
                i += 1
                return out
            if tok == '{':
                i += 1
                out.append(Stmt('', None, block(), line))
                continue
            i += 1
            if i < len(toks) and toks[i][0] in ('=', '<', '>', '<=', '>=', '!='):
                op = toks[i][0]
                i += 1
                if i < len(toks) and toks[i][0] == '{':
                    i += 1
                    out.append(Stmt(tok, op, block(), line))
                elif i < len(toks):
                    out.append(Stmt(tok, op, toks[i][0].strip('"'), line))
                    i += 1
            else:
                out.append(Stmt(tok, None, None, line))
        return out

    result = []
    while i < len(toks):
        result.extend(block())
    return result


def read(path):
    try:
        return path.read_text(encoding='utf-8-sig', errors='replace')
    except OSError:
        return ''


def files(root, sub):
    base = root / sub
    return sorted(base.rglob('*.txt')) if base.is_dir() else []


class Mod:
    def __init__(self, root):
        self.root = root
        self.effects, self.triggers, self.events, self.hooks = {}, {}, {}, []
        for path in files(root, 'common/scripted_effects'):
            for st in parse(read(path)):
                if isinstance(st.value, list) and st.key:
                    self.effects[st.key] = (st.value, self.rel(path), st.line)
        for path in files(root, 'common/scripted_triggers'):
            for st in parse(read(path)):
                if isinstance(st.value, list) and st.key:
                    self.triggers[st.key] = (st.value, self.rel(path), st.line)
        for path in files(root, 'events'):
            for st in parse(read(path)):
                if st.key in EVENT_KINDS and isinstance(st.value, list):
                    eid = next((s.value for s in st.value if s.key == 'id'), None)
                    if isinstance(eid, str):
                        self.events[eid] = (st.value, self.rel(path), st.line)
        for path in files(root, 'common/on_actions'):
            for top in parse(read(path)):
                if top.key != 'on_actions' or not isinstance(top.value, list):
                    continue
                for hook in top.value:
                    m = CLOCK.match(hook.key or '')
                    if m and isinstance(hook.value, list):
                        self.hooks.append((m.group(1), m.group(2), hook, self.rel(path)))

    def rel(self, path):
        return path.relative_to(self.root).as_posix()


def count_ops(block):
    n = 0
    for st in block:
        n += 1
        if isinstance(st.value, list):
            n += count_ops(st.value)
    return n


class Builder:
    def __init__(self, mod):
        self.mod = mod
        self.unresolved = set()

    def node(self, kind, name, where, own=0):
        return {'kind': kind, 'name': name, 'where': where, 'own': own, 'total': own,
                'children': [], 'notes': []}

    def walk(self, block, parent, path, stack, loops):
        """Add ops of block to parent and attach calls as children."""
        for st in block:
            parent['own'] += 1
            where = f"{path}:{st.line}"
            if st.key in LOOP_SCOPES and isinstance(st.value, list):
                scope = LOOP_SCOPES[st.key]
                child = self.node('loop', f'{st.key} ({scope})', where)
                child['scope'] = scope
                self.walk(st.value, child, path, stack, loops + [scope])
                self.attach(parent, child)
                continue
            if st.key in HEAVY_EFFECTS:
                parent['notes'].append(f"{st.key} at {where}: {HEAVY_EFFECTS[st.key]}"
                                       + (f" inside {' > '.join(loops)}" if loops else ''))
            if st.key in EVENT_KINDS:
                self.event_call(st, parent, path, stack, loops)
                continue
            if st.key == 'random_events' and isinstance(st.value, list):
                for entry in st.value:
                    if isinstance(entry.value, str) and entry.value in self.mod.events:
                        child = self.event_node(entry.value, stack, f'weight {entry.key}')
                        self.attach(parent, child)
                continue
            if st.key == 'meta_effect' and isinstance(st.value, list):
                text = next((s for s in st.value if s.key == 'text'), None)
                if text and isinstance(text.value, list):
                    for inner in text.value:
                        if '[' in (inner.key or ''):
                            pat = re.compile('^' + re.sub(r'\\\[[^\]]*\\\]', '.+', re.escape(inner.key)) + '$')
                            hits = [k for k in self.mod.effects if pat.match(k)]
                            parent['notes'].append(
                                f"meta_effect {inner.key} at {where}: dynamic call, "
                                f"{len(hits)} candidate effects, not counted")
                    parent['own'] += count_ops(text.value)
                continue
            name = st.key
            if st.op == '=' and st.value in ('yes', 'no') and name:
                table = (self.mod.effects if name in self.mod.effects else
                         self.mod.triggers if name in self.mod.triggers else None)
                if table is not None:
                    kind = 'effect' if table is self.mod.effects else 'trigger'
                    self.attach(parent, self.def_node(kind, name, table, stack, loops))
                    continue
            if isinstance(st.value, list):
                self.walk(st.value, parent, path, stack, loops)

    def def_node(self, kind, name, table, stack, loops):
        body, path, line = table[name]
        child = self.node(kind, name, f'{path}:{line}')
        if name in stack:
            child['notes'].append('recursion, not expanded')
            return child
        self.walk(body, child, path, stack | {name}, loops)
        return child

    def event_call(self, st, parent, path, stack, loops):
        eid, days = None, None
        if isinstance(st.value, str):
            eid = st.value
        elif isinstance(st.value, list):
            for s in st.value:
                if s.key == 'id':
                    eid = s.value
                elif s.key in ('days', 'hours', 'random_days', 'random_hours', 'random'):
                    days = s.value
        if not isinstance(eid, str):
            return
        label = 'fired' + (f' after {days}' if days else '')
        if eid not in self.mod.events:
            self.unresolved.add(eid)
            return
        child = self.event_node(eid, stack, label)
        if loops:
            child['notes'].append(f"fired inside {' > '.join(loops)}")
        self.attach(parent, child)

    def event_node(self, eid, stack, label):
        body, path, line = self.mod.events[eid]
        child = self.node('event', f'{eid} ({label})', f'{path}:{line}')
        if eid in stack:
            child['notes'].append('self-rescheduling loop')
            return child
        for st in body:
            if st.key in ('trigger', 'immediate', 'mean_time_to_happen') and isinstance(st.value, list):
                self.walk(st.value, child, path, stack | {eid}, [])
        options = [st for st in body if st.key == 'option' and isinstance(st.value, list)]
        if options:
            opt = self.node('options', f'{len(options)} option(s), heaviest counted', child['where'])
            heaviest = max(options, key=lambda o: count_ops(o.value))
            self.walk(heaviest.value, opt, path, stack | {eid}, [])
            self.attach(child, opt)
        return child

    @staticmethod
    def attach(parent, child):
        Builder.total(child)
        parent['children'].append(child)

    @staticmethod
    def total(node):
        node['total'] = node['own'] + sum(c['total'] for c in node['children'])
        node['children'].sort(key=lambda c: -c['total'])
        return node['total']

    def build(self, tag=None):
        root = self.node('root', 'all clock hooks', '')
        cadences = {}
        for cadence, htag, hook, path in self.mod.hooks:
            if tag and htag not in (None, tag):
                continue
            cad = cadences.setdefault(cadence, self.node('cadence', cadence, ''))
            scope = htag or 'GLOBAL'
            node = self.node('hook', f'{hook.key} [{scope}]', f'{path}:{hook.line}')
            node['scope'] = scope
            self.walk(hook.value, node, path, frozenset(), [])
            self.attach(cad, node)
        for name in ('daily', 'weekly', 'monthly'):
            if name in cadences:
                self.attach(root, cadences[name])
        self.total(root)
        return root


def iter_nodes(node, depth=0, path=()):
    yield node, depth, path
    for c in node['children']:
        yield from iter_nodes(c, depth + 1, path + (node,))


def spot_checks(root):
    findings = []
    for node, _, path in iter_nodes(root):
        cadence = next((p['name'] for p in path if p['kind'] == 'cadence'), None)
        if not cadence:
            continue
        hook = next((p for p in path if p['kind'] == 'hook'), node if node['kind'] == 'hook' else None)
        scope = hook.get('scope', '?') if hook else '?'
        weight = CADENCE_WEIGHT[cadence] * (200 if scope == 'GLOBAL' else 1)
        if node['kind'] == 'loop' and node.get('scope') in GLOBAL_LOOPS:
            sev = 'high' if cadence == 'daily' and scope == 'GLOBAL' else 'medium'
            findings.append((weight * 100, sev, cadence, scope,
                             f"{node['name']} ({node['total']} ops per pass)", node['where']))
        for note in node['notes']:
            if 'create_country_leader' in note or 'force_update' in note:
                findings.append((weight * 50, 'high' if cadence != 'monthly' else 'medium',
                                 cadence, scope, note, node['where']))
            elif 'self-rescheduling' in note or 'meta_effect' in note:
                findings.append((weight, 'low', cadence, scope, note, node['where']))
        if node['kind'] == 'event' and cadence == 'daily' and scope == 'GLOBAL':
            findings.append((weight * 10, 'medium', cadence, scope,
                             f"event {node['name']} wired into a global daily hook", node['where']))
    rank = {'high': 0, 'medium': 1, 'low': 2}
    findings.sort(key=lambda f: (rank[f[1]], -f[0]))
    return findings


def print_children(node, depth, max_depth, top):
    if depth > max_depth:
        return
    kids = node['children']
    for child in kids[:top]:
        print(f"  {child['total']:>7}  {'  ' * depth}{child['kind']}: {child['name']}  {child['where']}")
        print_children(child, depth + 1, max_depth, top)
    if len(kids) > top:
        rest = sum(c['total'] for c in kids[top:])
        print(f"  {rest:>7}  {'  ' * depth}... {len(kids) - top} more")


def to_json(node):
    return {k: (v if k != 'children' else [to_json(c) for c in v]) for k, v in node.items()}


def to_html(root):
    def render(node):
        notes = ''.join(f'<li class="note">{html.escape(n)}</li>' for n in node['notes'])
        kids = ''.join(render(c) for c in node['children'])
        width = 100 * node['total'] / max(root['total'], 1)
        label = (f'<span class="bar" style="width:{width:.2f}%"></span>'
                 f'<b>{html.escape(node["name"])}</b> <i>{node["kind"]}</i> '
                 f'total {node["total"]} / own {node["own"]} '
                 f'<code>{html.escape(node["where"])}</code>')
        inner = f'<ul>{notes}{kids}</ul>' if notes or kids else ''
        return f'<li data-s="{html.escape(node["name"].lower() + " " + node["where"].lower())}"><details><summary>{label}</summary>{inner}</details></li>'
    return ('<!doctype html><meta charset="utf-8"><title>Tick audit</title><style>'
            'body{font:13px system-ui;margin:16px;background:#fff;color:#111}'
            '@media(prefers-color-scheme:dark){body{background:#111;color:#eee}}'
            'ul{list-style:none;padding-left:18px}summary{cursor:pointer;position:relative}'
            '.bar{position:absolute;left:0;top:0;bottom:0;background:#4a90e233;z-index:-1}'
            'code{opacity:.7}.note{color:#c60}</style>'
            '<input id=f placeholder="filter (tag, file, effect)" style="width:100%;margin-bottom:8px">'
            f'<ul id=t>{render(root)}</ul><script>'
            'f.oninput=()=>{const q=f.value.toLowerCase();document.querySelectorAll("#t li").forEach(li=>{'
            'li.style.display=!q||li.dataset.s.includes(q)||li.querySelector("[data-s*=\'"+CSS.escape(q)+"\']")?"":"none"})}'
            '</script>')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', default='.', help='mod root (default: current directory)')
    ap.add_argument('--cadence', choices=['daily', 'weekly', 'monthly'])
    ap.add_argument('--tag', help='only global hooks plus this TAG\'s own hooks')
    ap.add_argument('--top', type=int, default=10, help='children listed per hook')
    ap.add_argument('--depth', type=int, default=2, help='tree depth printed below each hook')
    ap.add_argument('--spot-check', action='store_true', help='list static hotspots')
    ap.add_argument('--json', help='write the full call tree as JSON')
    ap.add_argument('--html', help='write a collapsible HTML call tree')
    a = ap.parse_args(argv)
    root_dir = Path(a.root).resolve()
    if not (root_dir / 'common' / 'on_actions').is_dir():
        ap.error(f'no common/on_actions under {root_dir}')
    mod = Mod(root_dir)
    builder = Builder(mod)
    tree = builder.build(a.tag)
    print(f'Parsed {len(mod.hooks)} clock hooks, {len(mod.effects)} scripted effects, '
          f'{len(mod.triggers)} scripted triggers, {len(mod.events)} events.')
    print('ops = script statements reachable per run of a hook; a proxy, not time.\n')
    for cad in tree['children']:
        if a.cadence and cad['name'] != a.cadence:
            continue
        print(f"== {cad['name']}: {cad['total']} ops across {len(cad['children'])} hook blocks")
        for hook in cad['children']:
            print(f"  {hook['total']:>7}  {hook['name']}  {hook['where']}")
            print_children(hook, 1, a.depth, a.top)
        print()
    if a.spot_check:
        print('== spot checks (ranked by cadence x scope x pattern)')
        found = spot_checks(tree)
        for _, sev, cad, scope, msg, where in found:
            print(f'  [{sev}] {cad}/{scope}: {msg}  {where}')
        if not found:
            print('  none')
        print()
    if builder.unresolved:
        print(f'{len(builder.unresolved)} fired event ids not found in events/: '
              + ', '.join(sorted(builder.unresolved)[:15])
              + (' ...' if len(builder.unresolved) > 15 else ''))
    if a.json:
        Path(a.json).write_text(json.dumps(to_json(tree), indent=1), encoding='utf-8')
        print(f'Wrote {a.json}')
    if a.html:
        Path(a.html).write_text(to_html(tree), encoding='utf-8')
        print(f'Wrote {a.html}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
