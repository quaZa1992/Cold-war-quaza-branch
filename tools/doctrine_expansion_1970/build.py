# IMPERIA COLD WAR — Native land doctrine expansion generator.
"""Emit the approved doctrine packages without modifying unrelated MD content."""
from pathlib import Path
import argparse
import json
from design import GRANDS, SUBS, PROJECT, FEATURE
from balance_revision import legacy_outputs
from coverage_revision import outputs as coverage_outputs

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MARKER = f'# {PROJECT} — {FEATURE}.\n'
GRAND_PATH = 'common/doctrines/grand_doctrines/mdcw_land_doctrine_expansion.txt'
SUB_PATH = 'common/doctrines/subdoctrines/land/mdcw_land_doctrine_expansion.txt'
LOC_PATH = 'localisation/english/mdcw_land_doctrine_expansion_l_english.yml'
GFX_PATH = 'interface/mdcw_land_doctrine_expansion.gfx'
TRIGGERS = 'common/scripted_triggers/00_doctrines_scripted_triggers.txt'


def number(value):
    return format(value, '.5f').rstrip('0').rstrip('.') if isinstance(value, float) else str(value)


def emit(values, depth=1):
    lines = []
    prefix = '\t' * depth
    for key, value in values.items():
        if isinstance(value, dict):
            lines += [prefix + key + ' = {', *emit(value, depth + 1), prefix + '}']
        else:
            lines.append(prefix + key + ' = ' + number(value))
    return lines


def loc_key(item, grand=False):
    return ('GRAND_DOCTRINE_' if grand else 'SUBDOCTRINE_') + item['id'].upper()


def ai_lines(item):
    ai = item['ai']
    return ['\tai_will_do = {', f'\t\tbase = {ai["base"]}', '\t\tmodifier = {',
            f'\t\t\tadd = {ai["country_weight"]}', '\t\t\tOR = {',
            *[f'\t\t\t\toriginal_tag = {tag}' for tag in ai['countries']],
            '\t\t\t}', '\t\t}', '\t}']


def header(item, grand=False):
    key = loc_key(item, grand)
    lines = [item['id'] + ' = {', '\tfolder = land' if grand else '\ttrack = ' + item['track'],
             '\tname = ' + key, '\tdescription = ' + key + '_DESC',
             '\ticon = GFX_doctrine_' + item['id'], '\txp_cost = ' + ('100' if grand else '75'),
             '\txp_type = army', '\tavailable = {']
    if grand:
        lines.append('\t\talways = yes')
    else:
        for excluded in [item['id'], *item.get('excludes', [])]:
            lines.append('\t\tNOT = { has_doctrine = ' + excluded + ' }')
    return [*lines, '\t}', *ai_lines(item), '']


def outputs():
    grands, subs = [MARKER.rstrip()], [MARKER.rstrip()]
    localisation = ['l_english:', MARKER.rstrip()]
    graphics = [MARKER.rstrip(), 'spriteTypes = {']
    for item in GRANDS:
        lines = header(item, True)
        lines += ['\ttracks = {', *['\t\t' + track for track in item['tracks']], '\t}', '']
        lines += emit(item['effects']) + ['', '\tmilestones = {']
        for title, effects in item['milestones']:
            lines += ['\t\t{', '\t\t\t# ' + title, *emit(effects, 3), '\t\t}']
        grands += ['', *lines, '\t}', '}']
    for item in SUBS:
        lines = header(item)
        lines += emit(item['effects']) + ['', '\trewards = {']
        for stage in item['rewards']:
            lines += ['\t\t' + stage['key'] + ' = {', *emit(stage['effects'], 3), '\t\t}']
        subs += ['', *lines, '\t}', '}']
    for item in [*GRANDS, *SUBS]:
        key = loc_key(item, item in GRANDS)
        localisation += [f' {key}:0 {json.dumps(item["name"], ensure_ascii=False)}',
                         f' {key}_DESC:0 {json.dumps(item["description"], ensure_ascii=False)}']
        for stage in item.get('rewards', []):
            reward_key = item['id'] + '_' + stage['key']
            localisation += [f' {reward_key}:0 {json.dumps(stage["name"], ensure_ascii=False)}',
                             f' {reward_key}_desc:0 {json.dumps(stage["description"], ensure_ascii=False)}']
        graphics += ['\tSpriteType = {', '\t\tname = "GFX_doctrine_' + item['id'] + '"',
                     '\t\ttexturefile = "gfx/interface/doctrines/icons/land/mdcw_expansion/' + item['id'] + '.dds"',
                     '\t\talwaystransparent = yes', '\t}']
    graphics.append('}')
    return {GRAND_PATH: '\n'.join(grands) + '\n', SUB_PATH: '\n'.join(subs) + '\n',
            LOC_PATH: '\n'.join(localisation) + '\n', GFX_PATH: '\n'.join(graphics) + '\n'}


def integrated_triggers(source):
    """Retain MD triggers and add the reciprocal approved identity exclusion."""
    needle = 'does_not_have_mdcw_territorial_defence_doctrine = {'
    addition = ('\n\t# IMPERIA COLD WAR — Key Zone Defence and Territorial Defence are alternatives.\n'
                '\tNOT = { has_doctrine = mdcw_key_zone_defence }')
    start = source.index(needle)
    end = source.index('\nhas_selected_land_grand_doctrine', start)
    if 'has_doctrine = mdcw_key_zone_defence' not in source[start:end]:
        line_end = source.index('\n', start)
        source = source[:line_end] + addition + source[line_end:]
    if not source.startswith('# IMPERIA COLD WAR —'):
        source = '# IMPERIA COLD WAR — Key Zone Defence integration with native MD doctrine triggers.\n' + source
    return source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare generated text without writing it')
    args = parser.parse_args()
    expected = outputs()
    expected.update(legacy_outputs(ROOT))
    expected.update(coverage_outputs(ROOT, expected))
    trigger_file = ROOT / TRIGGERS
    expected[TRIGGERS] = integrated_triggers(trigger_file.read_text(encoding='utf-8-sig'))
    differences = []
    for relative, text in expected.items():
        path = ROOT / relative
        encoded = text.encode('utf-8-sig' if path.suffix == '.yml' else 'utf-8')
        if args.check:
            if not path.exists() or path.read_bytes() != encoded:
                differences.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(encoded)
    if args.check:
        print(json.dumps({'project': PROJECT, 'generator_drift': differences}, indent=2))
        raise SystemExit(bool(differences))
    print(json.dumps({'project': PROJECT, 'written': list(expected), 'grand_doctrines': len(GRANDS),
                      'subdoctrines': len(SUBS), 'mastery_rewards': sum(len(item['rewards']) for item in SUBS)}, indent=2))


if __name__ == '__main__':
    main()
