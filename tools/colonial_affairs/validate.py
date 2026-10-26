# IMPERIA CW — Cold War: independent installed Colonial Affairs source checks.
"""Inspect generated providers and native contracts; this is not an engine test."""
from pathlib import Path
from collections import defaultdict
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools/spain_1970_v2'))
from script_ast import parse, first, walk
from PIL import Image


def check_click_geometry(parsed, errors):
    """Use native sprite frame sizes, not the texture strip's full width."""
    gui = parsed['interface/COLDWAR_colonial_affairs.gui']
    gfx = parsed['interface/COLDWAR_colonial_affairs.gfx']
    sprites = {}
    for kind, _, node in first(gfx, 'spriteTypes'):
        if kind != 'spriteType':
            continue
        with Image.open(ROOT / first(node, 'texturefile').strip('"')) as texture:
            sprites[first(node, 'name').strip('"')] = (texture.width / int(first(node, 'noOfFrames', 1)), texture.height)
    buttons = 0
    windows=[]
    for kind, _, window in first(gui, 'guiTypes'):
        if kind != 'containerWindowType':
            continue
        name = first(window, 'name').strip('"')
        size = first(window, 'size')
        width, height = float(first(size, 'width')), float(first(size, 'height'))
        windows.append(dict(name=name,width=width,height=height))
        boxes = []
        for widget, _, node in window:
            if widget != 'buttonType':
                continue
            button = first(node, 'name').strip('"')
            sprite = first(node, 'quadTextureSprite').strip('"')
            # Native country flag is decorative and supplied by the engine.
            if sprite == 'GFX_flag_small':
                continue
            w, h = sprites[sprite]
            position = first(node, 'position')
            x, y = float(first(position, 'x')), float(first(position, 'y'))
            box = (x, y, x+w, y+h)
            if x < 0 or y < 0 or x+w > width or y+h > height:
                errors.append('Button exceeds window ' + button)
            for other, previous in boxes:
                if max(x, previous[0]) < min(x+w, previous[2]) and max(y, previous[1]) < min(y+h, previous[3]):
                    errors.append('Overlapping buttons ' + button + ' / ' + other)
            boxes.append((button, box))
            buttons += 1
        if name == 'COLDWAR_colonial_affairs_window':
            sheet = next(node for widget, _, node in window if widget == 'iconType' and first(node, 'name') == '"COLDWAR_COL_policy_sheet"')
            position = first(sheet, 'position')
            sheet_bottom = float(first(position, 'y')) + sprites[first(sheet, 'spriteType').strip('"')][1]
            review = next(box for button, box in boxes if button == 'COLDWAR_COL_review_policy')
            if sheet_bottom > review[1]:
                errors.append('Policy sheet covers its close button')
    report=dict(windows=windows,clickable_buttons_checked=buttons,button_overlap_errors=[e for e in errors if 'button' in e.lower()],engine_tested=False)
    (HERE/'ui_geometry_review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return buttons


def check():
    errors = []
    registry = json.loads((HERE / 'registry.json').read_text(encoding='utf-8'))['administrations']
    manifest = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))
    parsed, loc, textures = {}, {}, []
    for rel, digest in manifest['generated'].items():
        path = ROOT / rel
        if not path.is_file():
            errors.append('Missing output ' + rel)
            continue
        blob = path.read_bytes()
        if hashlib.sha256(blob).hexdigest() != digest:
            errors.append('Stale generated hash ' + rel)
        if rel.endswith('.yml'):
            if not blob.startswith(b'\xef\xbb\xbf'):
                errors.append('Localisation requires BOM ' + rel)
            for key, value in re.findall(r'^\s*([^\s:#]+):\d*\s*"(.*)"\s*$', blob.decode('utf-8-sig'), re.M):
                if key in loc:
                    errors.append('Duplicate localisation ' + key)
                loc[key] = value
        elif rel.endswith(('.txt', '.gfx', '.gui')):
            if blob.startswith(b'\xef\xbb\xbf'):
                errors.append('Forbidden script BOM ' + rel)
            text = blob.decode('utf-8')
            if not text.startswith('# IMPERIA CW'):
                errors.append('Missing Cold War source marker ' + rel)
            if re.search(r'(?<!\w)\d+\.\d{6,}(?!\w)', text):
                errors.append('Native fixed-point precision ' + rel)
            try:
                parsed[rel] = parse(text)
            except ValueError as exc:
                errors.append(rel + ': ' + str(exc))
        elif rel.endswith('.dds'):
            if not blob.startswith(b'DDS '):
                errors.append('Invalid DDS header ' + rel)
    definitions, declared = set(), defaultdict(list)
    for folder in ('common/scripted_effects', 'common/scripted_triggers', 'common/dynamic_modifiers'):
        for path in (ROOT / folder).glob('*.txt'):
            for name in re.findall(r'^([^\s#{}=]+)\s*=\s*\{', path.read_text(encoding='utf-8-sig'), re.M):
                definitions.add(name)
                declared[(folder, name)].append(path.name)
    graphics = {}
    for path in (ROOT / 'interface').glob('*.gfx'):
        text = path.read_text(encoding='utf-8-sig')
        for name in re.findall(r'\bname\s*=\s*"([^"\n]+)"', text):
            graphics[name] = path.name
    defined_loc = set()
    for path in (ROOT / 'common/scripted_localisation').glob('*.txt'):
        defined_loc.update(re.findall(r'\bname\s*=\s*"?([\w]+)"?', path.read_text(encoding='utf-8-sig')))
    events = set()
    for rel, ast in parsed.items():
        if rel.startswith('events/'):
            events.update(first(v, 'id') for k, op, v in ast if k == 'country_event')
        for key, op, value in walk(ast):
            if isinstance(value, str) and key.startswith('COLDWAR_COL_') and value in ('yes', 'no'):
                if key not in definitions:
                    errors.append('Missing scripted provider ' + key + ' in ' + rel)
            if key in ('transfer_state', 'set_state_owner', 'set_state_controller', 'set_autonomy', 'declare_war_on'):
                errors.append('Unapproved sovereignty/war change ' + key + ' in ' + rel)
            if key == 'texturefile' and isinstance(value, str):
                asset = value.strip('"')
                textures.append(asset)
                if not (ROOT / asset).is_file():
                    errors.append('Missing texture ' + asset)
            if key in ('spriteType', 'quadTextureSprite', 'icon') and isinstance(value, str):
                name = value.strip('"')
                if name.startswith('GFX_') and name not in graphics:
                    errors.append('Missing sprite ' + name)
            if key in ('text', 'tooltip', 'pdx_tooltip', 'custom_effect_tooltip', 'title', 'desc', 'localization_key') and isinstance(value, str):
                name = value.strip('"')
                if name.startswith('COLDWAR_COL_') and name not in loc:
                    errors.append('Missing English text ' + name + ' in ' + rel)
    for key, value in loc.items():
        for name in re.findall(r'\[(COLDWAR_COL_[\w]+)\]', value):
            if name not in defined_loc:
                errors.append('Missing scripted localisation ' + name + ' in ' + key)
    for (folder, name), files in declared.items():
        if name.startswith('COLDWAR_COL_') and len(files) != 1:
            errors.append('Duplicate provider ' + name + ': ' + str(files))
    from retire_ira import DEDICATED, OLD
    for rel in DEDICATED:
        if (ROOT/rel).exists():errors.append('Old IRA module still loaded '+rel)
    migrated_files=0
    for rel in manifest.get('retired_ira_changes',[]):
        path=ROOT/rel
        if not path.exists() or path.suffix!='.txt':continue
        blob=path.read_bytes()
        if blob.startswith(b'\xef\xbb\xbf'):errors.append('Migrated script has BOM '+rel)
        migrated_files+=1
        for key,op,value in walk(parse(blob.decode('utf-8'))):
            if key in OLD or (isinstance(value,str) and value in OLD):errors.append('Old IRA simulation still referenced '+rel+': '+key)
            if key=='custom_effect_tooltip' and isinstance(value,str) and value.startswith('COLDWAR_COL_') and value not in loc:errors.append('Missing migrated tooltip '+value)
            if key.startswith('COLDWAR_COL_') and value=='yes' and key not in definitions:errors.append('Missing migrated provider '+key)
    contacts=parsed['common/scripted_effects/COLDWAR_colonial_contacts.txt']
    for package,weights in [('political',[90,10]),('funding',[75,25]),('arms',[60,40])]:
        branches=first(first(contacts,'COLDWAR_COL_disclose_'+package),'random_list')
        if [int(k) for k,o,v in branches]!=weights:errors.append('Disclosure probability mismatch '+package)
    hooks=first(parsed['common/on_actions/COLDWAR_colonial_contacts.txt'],'on_actions')
    if first(first(hooks,'on_monthly'),'effect')!=[('COLDWAR_COL_contacts_monthly','=','yes')]:errors.append('Monthly hook must update its current country exactly once')
    money = (ROOT / 'common/scripted_effects/00_money_system.txt').read_bytes()
    if money.startswith(b'\xef\xbb\xbf'):
        errors.append('Native economy BOM')
    money_text = money.decode('utf-8')
    if money_text.count('# COLDWAR COLONIAL EXPENSE BEGIN') != 1:
        errors.append('Colonial expense hook must exist exactly once')
    if 'add_to_variable = { additional_expenses_rate = COLDWAR_COL_total_weekly_cost }' not in money_text:
        errors.append('No actual native weekly-expense consumer')
    clickable_buttons = check_click_geometry(parsed, errors)
    seen_states, seen_provinces = {}, {}
    for row in registry:
        if not row['source_urls']:
            errors.append('Missing historical source ' + row['id'])
        for state_id in row['states']:
            paths = list((ROOT / 'history/states').glob(str(state_id) + '-*.txt'))
            if len(paths) != 1:
                errors.append('Unknown/ambiguous state ' + str(state_id))
                continue
            if state_id in seen_states:
                errors.append('Two administrations charge one state ' + str(state_id))
            seen_states[state_id] = row['id']
            state = first(parse(paths[0].read_text(encoding='utf-8-sig')), 'state')
            for key, op, province in first(state, 'provinces', []):
                if province in seen_provinces:
                    errors.append('Province overlap ' + province)
                seen_provinces[province] = state_id
    report = dict(
        status='failed' if errors else 'passed', administrations=len(registry),
        powers=manifest['powers'], states=len(seen_states), provinces=len(seen_provinces),
        parsed_files=len(parsed), localisation_keys=len(loc), texture_references=len(textures),
        clickable_buttons_checked=clickable_buttons,
        retired_ira_files_checked=migrated_files,
        errors=sorted(set(errors)), engine_tested=False,
    )
    (HERE / 'validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    check()
