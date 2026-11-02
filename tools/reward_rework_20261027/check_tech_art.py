# IMPERIA COLD WAR — Emitted technology gates and focus artwork checks.
"""Check loaded helpers/trigger closure, recipient sites and registered sprites."""
from collections import Counter
import json
from pathlib import Path
import sys

from building_technology import TECH_LOCKED_BUILDINGS, unlocks, state_technology_guard
from focus_art import catalogue, icon_for

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'docs/tech_art_review_20261027'
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first, values, walk


def main():
    import verify
    verify.REPORT = REPORT
    original_paths = verify.live_paths
    verify.live_paths = lambda: sorted(set(original_paths()) | {'interface/COLDWAR_EASTASIA_1970_focus_icons.gfx'})
    assert not verify.main(), 'Emitted source/API/graph check failed'
    definitions = {}
    for folder in ('scripted_triggers', 'scripted_effects'):
        for path in (ROOT / 'common' / folder).glob('COLDWAR_*.txt'):
            if path.name.startswith(('COLDWAR_NKO', 'COLDWAR_KOR', 'COLDWAR_JAP')):
                for key, operator, body in parse(path.read_text(encoding='utf-8')):
                    definitions[key] = body

    def expand(rows, seen=()):
        result = []
        for key, operator, body in rows:
            if key in definitions and body == 'yes' and key not in seen:
                result.extend(expand(definitions[key], seen + (key,)))
            elif isinstance(body, list):
                result.append((key, operator, expand(body, seen)))
            else:
                result.append((key, operator, body))
        return result

    checked = []
    counts = Counter()
    for tag in ('NKO', 'KOR', 'JAP'):
        tree = first(parse((ROOT / f'common/national_focus/COLDWAR_{tag}_1970_focus.txt').read_text(encoding='utf-8')), 'focus_tree')
        for node in values(tree, 'focus'):
            identifier = first(node, 'id')
            if identifier in catalogue()['assignments']:
                assert first(node, 'icon') == icon_for(tag, identifier, ''), identifier
                counts[tag] += 1
            reward = first(node, 'completion_reward', [])
            preview = first(reward, 'effect_tooltip', [])
            special = {first(body, 'type') for key, operator, body in walk(preview)
                       if key == 'add_building_construction'} & TECH_LOCKED_BUILDINGS
            if not special:
                continue
            available = expand(first(node, 'available', []))
            hidden = first(reward, 'hidden_effect', [])
            call = next(key for key, operator, body in hidden if key in definitions)
            limit = expand(first(first(definitions[call], 'if', []), 'limit', []))
            visible_techs = {body for key, operator, body in walk(available) if key == 'has_tech'}
            paid_techs = {body for key, operator, body in walk(limit) if key == 'has_tech'}
            for building in special:
                providers = {name for name, maximum in unlocks()[building]}
                assert providers & visible_techs, (identifier, building, 'Missing availability technology')
                assert providers & paid_techs, (identifier, building, 'Missing paid-transaction technology')
            checked.append({'focus': identifier, 'special_buildings': sorted(special), 'helper': call})
    assert sum(counts.values()) == len(catalogue()['assignments'])
    projects = parse((ROOT / 'common/decisions/COLDWAR_JAP70_foreign_project_decisions.txt').read_text(encoding='utf-8'))
    recipient_projects = []
    for category, operator, decisions in projects:
        for identifier, operator, decision in decisions:
            transaction = first(first(first(decision, 'complete_effect', []), 'hidden_effect', []), 'if', [])
            grants = first(transaction, 'FROM', [])
            for grant in values(grants, 'add_building_construction'):
                building, level = first(grant, 'type'), int(first(grant, 'level'))
                required = state_technology_guard(building, level)
                if not required:
                    continue
                required_rows = parse(required)
                target = first(first(decision, 'target_trigger', []), 'FROM', [])
                guard = first(first(transaction, 'limit', []), 'FROM', [])
                assert all(row in target and row in guard for row in required_rows), identifier
                recipient_projects.append(identifier)
    gfx = first(parse((ROOT / 'interface/COLDWAR_EASTASIA_1970_focus_icons.gfx').read_text(encoding='utf-8')), 'spriteTypes')
    sprites = {first(body, 'name').strip('"'): body for key, operator, body in gfx if key == 'spriteType'}
    for theme in set(catalogue()['assignments'].values()):
        texture = catalogue()['themes'][theme]
        assert (ROOT / texture).is_file(), texture
        for suffix in ('', '_shine'):
            sprite = sprites['GFX_goal_COLDWAR_EASTASIA_' + theme + suffix]
            assert first(sprite, 'texturefile').strip('"') == texture
    result = {'project': 'IMPERIA COLD WAR', 'success': True, 'focus_art_assignments': dict(counts),
              'specialised_building_focuses': checked, 'recipient_project_checks': recipient_projects,
              'building_unlock_providers': unlocks(), 'unique_art_themes': len(set(catalogue()['assignments'].values())),
              'scope': 'Actual emitted availability and paid-helper trigger closure, recipient-owned site checks and sprite assets. Native execution recorded separately.'}
    (REPORT / 'TECH_ART_CHECKS.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'success': True, 'art': dict(counts), 'technology_focuses': len(checked), 'recipient_projects': len(recipient_projects)}))


if __name__ == '__main__':
    main()
