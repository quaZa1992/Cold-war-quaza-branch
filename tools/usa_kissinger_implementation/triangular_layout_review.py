# IMPERIA COLD WAR — Independent installed triangular-diplomacy layout review.
"""Parse the loaded USA tree, compare its agreed geometry, and compose native-art evidence.

Only compact review records and images are written. This does not compile or
modify gameplay. Native cards, bitmap glyphs and source textures are reused;
orthogonal connectors and locked-state treatment approximate the game.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/design/usa_triangular_20261029'
P = 'COLDWAR_USA_KS_'
EXPECTED = {
    'triangular': (43, 2), 'beijing': (41, 3), 'moscow': (45, 3),
    'china_exchange': (41, 4), 'soviet_exchange': (45, 4),
    'china_priority': (41, 5), 'soviet_priority': (45, 5),
    'china_industry': (40, 6), 'china_security': (42, 6),
    'soviet_trade': (44, 6), 'soviet_arms': (46, 6),
    'signal_moscow': (41, 7), 'wider_settlement': (45, 7),
    'linkage': (43, 8), 'balance': (43, 9),
    'irq_contacts': (75, 5), 'irq_transit': (73, 6), 'irq_anatolia': (77, 6),
    'irq_fund': (75, 7), 'irq_autonomy': (73, 8), 'irq_front': (77, 8),
    'irq_settlement': (73, 9), 'irq_independence': (77, 9), 'angola': (73, 5),
}
NEW = set(EXPECTED) - {'triangular', 'beijing', 'moscow', 'angola'} - {
    key for key in EXPECTED if key.startswith('irq_')}
PROTECTED = {'kurds': (55, 3), 'covert': (55, 2), 'irn_dossier': (51, 5),
             'tur_dossier': (59, 5), 'syr_contacts': (67, 5), 'clients': (73, 3),
             'political': (77, 3), 'chile': (77, 4), 'guarantees': (81, 2), 'shuttle': (81, 3)}
EXPECTED_PARENTS = {
    'china_exchange': [['beijing']], 'soviet_exchange': [['moscow']],
    'china_priority': [['china_exchange']], 'soviet_priority': [['soviet_exchange']],
    'china_industry': [['china_priority']], 'china_security': [['china_priority']],
    'soviet_trade': [['soviet_priority']], 'soviet_arms': [['soviet_priority']],
    'signal_moscow': [['china_industry', 'china_security']],
    'wider_settlement': [['soviet_trade', 'soviet_arms']],
    'linkage': [['signal_moscow', 'wider_settlement']], 'balance': [['linkage']],
}


def load_renderer():
    spec = importlib.util.spec_from_file_location('icw_triangular_review_renderer', ROOT / 'tools/iraq_1970/render_installed.py')
    renderer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(renderer)
    renderer.OUT = OUT
    return renderer


def segment_hits(a, b, rect):
    x1, y1 = a
    x2, y2 = b
    left, top, right, bottom = rect
    return (x1 == x2 and left < x1 < right and min(y1, y2) < bottom and max(y1, y2) > top) or (
        y1 == y2 and top < y1 < bottom and min(x1, x2) < right and max(x1, x2) > left)


def painted_rect(renderer, node):
    x, y = node['xy'][0] * 96, node['xy'][1] * 130
    icon = renderer.icon(node['icon'])
    alpha = icon.getchannel('A').getbbox() or (0, 0, 0, 0)
    ix, iy = round(x + 87.5 - icon.width / 2), round(y + 20 - icon.height / 2)
    return (min(x + 5, ix + alpha[0]), min(y + 40, iy + alpha[1]),
            max(x + 170, ix + alpha[2]), max(y + 78, iy + alpha[3]))


def link_hits(renderer, nodes):
    rectangles = {key: painted_rect(renderer, node) for key, node in nodes.items()}
    result = set()
    for key, node in nodes.items():
        x, y = node['xy'][0] * 96, node['xy'][1] * 130
        for group in node['prerequisites']:
            for parent in group:
                px, py = nodes[parent]['xy'][0] * 96, nodes[parent]['xy'][1] * 130
                a, d = (px + 80, py + 64), (x + 80, y)
                mid = (a[1] + d[1]) // 2
                b, c = (a[0], mid), (d[0], mid)
                for other, rect in rectangles.items():
                    if other not in (key, parent) and any(segment_hits(u, v, rect) for u, v in ((a, b), (b, c), (c, d))):
                        result.add((parent, key, other))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture-baseline', action='store_true')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    renderer = load_renderer()
    nodes = renderer.read_tree('common/national_focus/USA_1970.txt')
    source = ROOT / 'common/national_focus/USA_1970.txt'
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    baseline_path = OUT / 'layout_baseline.json'
    if args.capture_baseline:
        if baseline_path.exists():
            raise SystemExit('The independent baseline already exists; it is not overwritten.')
        baseline = dict(project='IMPERIA COLD WAR', source='common/national_focus/USA_1970.txt',
                        sha256=source_hash, visible_focuses=len(nodes), nodes=nodes,
                        approximate_link_intersections=sorted(link_hits(renderer, nodes)))
        baseline_path.write_text(json.dumps(baseline, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(dict(project='IMPERIA COLD WAR', baseline=str(baseline_path), visible_focuses=len(nodes))))
        return
    baseline = json.loads(baseline_path.read_text(encoding='utf-8'))
    findings = []
    for key, expected in {**EXPECTED, **PROTECTED}.items():
        actual = nodes.get(P + key, {}).get('xy')
        if actual != list(expected):
            findings.append(dict(type='position', id=P + key, expected=expected, actual=actual))
    if len(nodes) != baseline['visible_focuses'] + len(NEW):
        findings.append(dict(type='count', expected=baseline['visible_focuses'] + len(NEW), actual=len(nodes)))
    for key in NEW:
        node = nodes.get(P + key)
        if node and renderer.width(node['title']) > 147:
            findings.append(dict(type='title_overflow', id=P + key, pixels=renderer.width(node['title']), title=node['title']))
        if node:
            expected_groups = [[P + parent for parent in group] for group in EXPECTED_PARENTS[key]]
            if node['prerequisites'] != expected_groups:
                findings.append(dict(type='prerequisite_groups', id=P + key, expected=expected_groups, actual=node['prerequisites']))
            expected_excludes = [P + ('soviet_priority' if key == 'china_priority' else 'china_priority')] if key in ('china_priority', 'soviet_priority') else []
            if node['excludes'] != expected_excludes:
                findings.append(dict(type='exclusions', id=P + key, expected=expected_excludes, actual=node['excludes']))
    for key, old in baseline['nodes'].items():
        current = nodes.get(key)
        if not current:
            findings.append(dict(type='removed_existing_focus', id=key))
        elif current['prerequisites'] != old['prerequisites'] or current['excludes'] != old['excludes']:
            findings.append(dict(type='existing_graph_changed', id=key))
    affected = {P + key for key in EXPECTED}
    overlaps = set()
    for key in affected & nodes.keys():
        x, y = nodes[key]['xy']
        a = (x * 96, y * 130, x * 96 + 165, y * 130 + 128)
        for other, node in nodes.items():
            if other == key:
                continue
            ox, oy = node['xy']
            b = (ox * 96, oy * 130, ox * 96 + 165, oy * 130 + 128)
            if min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1]):
                overlaps.add(tuple(sorted((key, other))))
    findings.extend(dict(type='card_overlap', ids=pair) for pair in sorted(overlaps))
    current_links = link_hits(renderer, nodes)
    prior_links = {tuple(row) for row in baseline['approximate_link_intersections']}
    new_intersections = sorted(current_links - prior_links)
    findings.extend(dict(type='approximate_link_intersection', parent=par, child=child, card=card) for par, child, card in new_intersections)
    for key, node in nodes.items():
        anchor = node.get('anchor')
        if anchor and list(nodes).index(anchor) > list(nodes).index(key):
            findings.append(dict(type='forward_anchor', id=key, anchor=anchor))
    renderer.render('USA_FULL_TRIANGULAR_INSTALLED', nodes, overview=True)
    views = {
        'USA_STATECRAFT_INSTALLED': (37, 83, -1, 11),
        'USA_TRIANGULAR_INSTALLED': (34, 49, 0, 10),
        'USA_IRQ_NEIGHBOURS_INSTALLED': (63, 83, 2, 11),
    }
    for name, (left, right, top, bottom) in views.items():
        selected = {key for key, node in nodes.items() if left <= node['xy'][0] <= right and top <= node['xy'][1] <= bottom}
        renderer.render(name, nodes, selected=selected, bounds=(left * 96 - 35, top * 130 - 115, right * 96 + 205, bottom * 130 + 140))
    report = dict(project='IMPERIA COLD WAR', status='PASS' if not findings else 'REVIEW', source_sha256=source_hash,
                  scope='Independent installed USA coordinates, native icons/titlebars/bitmap glyphs; approximate locked-state links. No engine test.',
                  visible_focuses=len(nodes), additional_visible_focuses=len(nodes) - baseline['visible_focuses'],
                  conditional_offsets=sum(node['offsets'] for node in nodes.values()), findings=findings,
                  baseline_approximate_link_intersections=len(prior_links), new_approximate_link_intersections=new_intersections,
                  max_title_width_new=max(renderer.width(nodes[P + key]['title']) for key in NEW if P + key in nodes),
                  expected_positions=EXPECTED, protected_positions=PROTECTED,
                  renders=renderer.REPORT['renders'], sources=renderer.REPORT['sources'],
                  credits='Existing Paradox Interactive, Millennium Dawn and project assets; individual asset authors unknown.',
                  licence_or_permission='Existing upstream conditions apply; separate redistribution permission unknown.',
                  modifications='Native textures and bitmap glyphs composed without repainting; only the full-tree overview is downsampled.')
    report['native_focus_art'] = []
    for sprite in sorted({node['icon'] for node in nodes.values()}):
        relative, definition = renderer.SPRITES[sprite]
        texture = next(base / relative for base in (renderer.ROOT, renderer.MD, renderer.GAME) if (base / relative).exists())
        asset = renderer.icon(sprite)
        report['native_focus_art'].append(dict(sprite=sprite, registration=definition, source=str(texture),
                                              sha256=hashlib.sha256(texture.read_bytes()).hexdigest(), dimensions=list(asset.size),
                                              author='Existing upstream/project author; individual credit unknown.',
                                              licence_or_permission='Existing upstream conditions apply; separate redistribution permission unknown.'))
    event_donor = ROOT / 'gfx/event_pictures/generic/elections/political_deal.dds'
    if event_donor.exists():
        donor = renderer.Image.open(event_donor)
        donor.save(OUT / 'MD_POLITICAL_DEAL_DONOR.png')
        report['event_donor'] = dict(source=event_donor.relative_to(ROOT).as_posix(),
                                    sha256=hashlib.sha256(event_donor.read_bytes()).hexdigest(),
                                    dimensions=list(donor.size), mode=donor.mode,
                                    author='Unknown individual Millennium Dawn / upstream author.',
                                    licence_or_permission='Existing upstream conditions apply; separate redistribution permission unknown.',
                                    modifications='Lossless PNG decoding for review only; source frame and alpha pixels unchanged.')
    report['native_reference_profile'] = dict(
        upstream='Millennium Dawn 2.0.3, supported game 1.19.*, workshop 2777392649',
        gui='interface/nationalfocusview.gui: spacing 96x130, container 165x128, title 147x20.',
        science='05_germany.txt: GER_scientific_exchanges, cost 6.5 weeks, scientific_exchange art, reciprocal influence +1.5 and two 50% Internet research bonuses.',
        trade='05_russia.txt: SOV_freind_uzb, cost 7 weeks, reciprocal named opinion, influence +3, native improved-trade agreement and investment +1.',
        narrative='MD_focus_GER_l_english.yml: GER_scientific_exchanges_desc names German institutions and foreign experts; MD_focus_SOV_l_english.yml: SOV_stabilisation_fund_desc explains the national purpose and stakes.',
        adaptation='Native presentation and geometry examples only. Approved USA values and real recipient consent are retained; modern policy or counterpart identities are not copied.')
    (OUT / 'layout_review.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    (OUT / 'NOTICE.md').write_text('IMPERIA COLD WAR\n\nInstalled-source USA triangular-diplomacy previews. These are native-asset composites, not live game screenshots. Existing Paradox Interactive, Millennium Dawn and project contributors retain their rights. Individual authors and separate redistribution permissions are unknown. Source bindings, geometry, transformations and approximation limits are recorded in layout_review.json.\n', encoding='utf-8')
    print(json.dumps(dict(project='IMPERIA COLD WAR', status=report['status'], visible_focuses=len(nodes), findings=findings, renders=list(renderer.REPORT['renders']))))
    sys.exit(bool(findings))


if __name__ == '__main__':
    main()
