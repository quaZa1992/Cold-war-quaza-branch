# IMPERIA CW — Cold War: Japan 1970 installed-content checks.
"""Check the installed Japan tree and its custom references; not an engine test."""
from collections import Counter
from pathlib import Path
import re
from check_script_grammar import main as check_grammar
from check_presentation import main as check_presentation

root = Path(__file__).resolve().parents[2]
tree_path = root / 'common/national_focus/COLDWAR_JAP_1970_focus.txt'
tree = tree_path.read_text(encoding='utf-8')
staged = (root / 'tools/japan_1970/staging/graph/focus_tree.txt').read_text(encoding='utf-8')
errors = []
if tree != staged:
    errors.append('Installed focus tree differs from the current staged graph')
focuses = [key for key in re.findall(r'(?m)^\s*id\s*=\s*(COLDWAR_JAP_1970_\w+)\s*$', tree)
           if key != 'COLDWAR_JAP_1970_focus']
if len(focuses) != 425 or len(set(focuses)) != 425:
    errors.append(f'Expected 425 unique focuses, found {len(focuses)}')
focus_blocks = tree.split('\n\tfocus = {')[1:]
for block in focus_blocks:
    name_match = re.search(r'(?m)^\s*id\s*=\s*(COLDWAR_JAP_1970_\w+)', block)
    reward = block.split('completion_reward = {', 1)
    if not name_match or len(reward) != 2:
        errors.append('Focus without identifiable completion reward')
    elif 'effect_tooltip = {' not in reward[1] and 'custom_effect_tooltip = ' not in reward[1]:
        errors.append('Focus lacks an unconditional reward preview: ' + name_match.group(1))
effects = list((root / 'common/scripted_effects').glob('COLDWAR_JAP*.txt'))
providers = set()
for path in effects:
    providers.update(re.findall(r'(?m)^([A-Za-z][A-Za-z0-9_]*)\s*=\s*\{', path.read_text(encoding='utf-8')))
calls = re.findall(r'hidden_effect\s*=\s*\{\s*(COLDWAR_JAP[A-Za-z0-9_]+)\s*=\s*yes\s*\}', tree)
if len(calls) != 425:
    errors.append(f'Expected 425 focus reward helpers, found {len(calls)}')
for call in calls:
    if call not in providers:
        errors.append('Missing scripted reward helper: ' + call)

loc_paths = list((root / 'localisation/english').glob('COLDWAR_JAP*_l_english.yml'))
loc_keys = Counter()
for path in loc_paths:
    raw = path.read_bytes()
    if not raw.startswith(b'\xef\xbb\xbf'):
        errors.append(f'Localization missing BOM: {path.name}')
    loc_keys.update(re.findall(r'(?m)^\s*([A-Za-z0-9_.-]+):(?:\d+)?\s*"', raw.decode('utf-8-sig')))
for key, count in loc_keys.items():
    if count > 1:
        errors.append(f'Duplicate Japan localization key {key}: {count}')
for focus in focuses:
    for key in (focus, focus + '_desc'):
        if key not in loc_keys:
            errors.append('Missing focus localization: ' + key)
for key in re.findall(r'custom_(?:effect|trigger)_tooltip\s*=\s*(COLDWAR_JAP\w+)', tree):
    if key not in loc_keys:
        errors.append('Missing focus tooltip localization: ' + key)

scripts = list((root / 'common').rglob('COLDWAR_JAP*.txt')) + list((root / 'events').glob('COLDWAR_JAP*.txt'))
for path in scripts:
    if path.read_bytes().startswith(b'\xef\xbb\xbf'):
        errors.append('Script has UTF-8 BOM: ' + str(path.relative_to(root)))
history = (root / 'history/countries/JAP - Japan.txt').read_text(encoding='utf-8')
fallback = (root / 'common/scripted_effects/mdcw_1970_focus_tree_effects.txt').read_text(encoding='utf-8')
for token in ('load_focus_tree = COLDWAR_JAP_1970_focus', 'COLDWAR_JAP_1970_article9_self_defence',
              'COLDWAR_JAP_1970_okinawa_and_the_bases', 'COLDWAR_JAP_1970_initialize_starting_modifiers',
              'COLDWAR_JAP_1970_party_modifiers_initialize'):
    if token not in history:
        errors.append('Missing Japan starting setup: ' + token)
if 'AND = { original_tag = JAP IMP_is_1970_scenario = yes }' not in fallback:
    errors.append('1970 generic fallback does not exempt the Japan tree')
if check_grammar():
    errors.append('Installed Japan scripts failed the grammar check')
if check_presentation():
    errors.append('Japan presentation or preserved gameplay failed its regression check')
print(f'Installed: {len(focuses)} focus IDs, {len(calls)} reward helpers, {len(loc_paths)} English localization files; {len(errors)} findings')
for error in errors:
    print('ERROR:', error)
raise SystemExit(bool(errors))
