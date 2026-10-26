# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Offline routing and content checks for the party-only presentation update."""
import argparse
import ast
from datetime import date
import json
from pathlib import Path
import re
from unittest.mock import patch

from build import Builder, IDEOLOGIES, ROOT, load_catalog
from party_presentation import PartyPresentation, hook_native, load_names
from refresh_parties import assemble


# Reuse the strict parser without executing the unrelated Israel content audit.
module = ast.parse((ROOT / 'tools/israel_1970/validate_content.py').read_text(encoding='utf-8'))
functions = [node for node in module.body if isinstance(node, ast.FunctionDef)
             and node.name in {'tokens', 'parse', 'values', 'first', 'walk'}]
namespace = {'re': re}
exec(compile(ast.Module(body=functions, type_ignores=[]), 'hoi4_parser', 'exec'), namespace)
parse, values, first, walk = (namespace[key] for key in ('parse', 'values', 'first', 'walk'))


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--report', type=Path)
    args = cli.parse_args()
    checks = 0

    def check(ok, message):
        nonlocal checks
        checks += 1
        assert ok, message

    countries, names = load_catalog(), load_names()
    check(set(countries) <= set(names), 'Missing historical country presentation')
    for tag, record in names.items():
        check(len(record['labels']) == 24, tag + ': family count')
        check(len(set(record['labels'])) == 24, tag + ': duplicate local family names')
        for value in record['labels'] + list(record.get('party_names', {}).values()) + list(record.get('bespoke_names', {}).values()):
            check('\ufffd' not in value and not re.search(r'[\r\n"£]', value), (tag, value))
    outputs = assemble()
    native_path = 'common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt'
    registry_path = 'common/scripted_localisation/mdcw_historical_parties.txt'
    definitions = {}
    for path in (native_path, registry_path):
        tree = parse(outputs[path])
        for definition in values(tree, 'defined_text'):
            key = first(definition, 'name')
            if key.startswith('MDCW_HP_') or key in {ideology + '_L' + suffix for ideology in IDEOLOGIES for suffix in ('', '_desc', '_icon')}:
                check(key not in definitions, 'Duplicate defined_text: ' + key)
            definitions[key] = definition
    parse(outputs['common/scripted_triggers/mdcw_historical_party_countries.txt'])
    loc = {}
    for path in (ROOT / 'localisation/english').glob('*.yml'):
        relative = path.relative_to(ROOT).as_posix()
        source = outputs.get(relative, path.read_text(encoding='utf-8-sig')).lstrip('\ufeff')
        for key, value in re.findall(r'^\s+([^\s:]+):(?:\d+)?\s*"(.*)"[ \t]*$', source, re.M):
            loc[key] = value
    for path, source in outputs.items():
        if path.endswith('.yml'):
            check(source.startswith('\ufeffl_english:'), path + ': UTF-8 BOM/language header')
            check('\ufffd' not in source, path + ': replacement character')
            check('without a documented named organization' not in source, path + ': old placeholder')
            for key, value in re.findall(r'^\s+([^\s:]+):(?:\d+)?\s*"(.*)"[ \t]*$', source, re.M):
                loc[key] = value
    def scalar(value):
        return value.strip('"')
    def day(value):
        return tuple(map(int, value.split('.')))
    def trigger(block, tag, today, flags=frozenset(), scenario=True):
        results = []
        for key, op, value in block:
            if key in {'OR', 'AND', 'NOT', 'NOR'}:
                if key == 'OR': result = any(trigger([entry], tag, today, flags, scenario) for entry in value)
                elif key == 'AND': result = trigger(value, tag, today, flags, scenario)
                else: result = not any(trigger([entry], tag, today, flags, scenario) for entry in value)
            elif key == 'original_tag': result = scalar(value) == tag
            elif key == 'date': result = {'>': day(today) > day(value), '<': day(today) < day(value), '=': day(today) == day(value)}[op]
            elif key == 'IMP_is_1970_scenario': result = scenario
            elif key == 'MDCW_HP_has_country': result = scenario and tag in names and day(today) < (2001, 1, 1)
            elif key == 'has_country_flag': result = scalar(value) in flags
            elif key == 'ISR70_is_scenario': result = scenario and tag == 'ISR'
            elif key == 'COLDWAR_IRQ_campaign_active': result = scenario and tag == 'IRQ'
            else: result = False
            results.append(result)
        return all(results)
    def resolve(name, tag, today, flags=frozenset(), scenario=True, depth=0):
        check(depth < 8, 'Recursive party route: ' + name)
        for branch in values(definitions[name], 'text'):
            limit = first(branch, 'trigger')
            if limit is None or trigger(limit, tag, today, flags, scenario):
                key = scalar(first(branch, 'localization_key'))
                if key.startswith('[') and key.endswith(']') and key[1:-1] in definitions:
                    return resolve(key[1:-1], tag, today, flags, scenario, depth + 1)
                check(key in loc, 'Missing localisation: ' + key)
                return key, loc[key]
        raise AssertionError(('Unresolved party route', name, tag, today))
    icons = set()
    selected_labels = {}
    for tag in names:
        for today in ('1970.1.1', '1976.12.31', '1985.1.1', '1995.1.1', '2000.12.31'):
            for index, ideology in enumerate(IDEOLOGIES):
                key, label = resolve(ideology + '_L', tag, today)
                check(not key.startswith('MDCW_HP_generic_'), (tag, today, ideology, 'generic party'))
                desc_key, desc = resolve(ideology + '_L_desc', tag, today)
                check(desc.startswith(f'$MDCW_HP_family_{index}_desc$'), (tag, today, ideology, 'missing MD ideology description', desc_key))
                icon_key, icon = resolve(ideology + '_L_icon', tag, today)
                check(re.fullmatch(r'£\w+', icon) is not None, (tag, ideology, 'malformed text icon', icon))
                check(label.startswith('£'), (tag, ideology, 'missing inline icon', key))
                if key.startswith(('COLDWAR_', 'ISR70_', 'LBA_1970.')):
                    check(icon_key == key + '_icon', (tag, ideology, 'name/icon disagreement', key, icon_key))
                icons.update(re.findall(r'£(\w+)', label + ' ' + icon))
                if today == '1970.1.1': selected_labels.setdefault(tag, {})[ideology] = label
    # Main MD definitions must be restored verbatim, not paraphrased.
    reference = json.loads((Path(__file__).parent / 'party_md_reference.json').read_text(encoding='utf-8'))
    for index, ideology in enumerate(IDEOLOGIES):
        check(loc['MDCW_HP_MD_' + ideology + '_desc'] == reference['families'][ideology]['description'], ideology + ': altered MD description')
    # All emitted icons resolve to native sprites and real texture files.
    sprites = {}
    for path in (ROOT / 'interface').glob('*.gfx'):
        text = path.read_text(encoding='utf-8-sig', errors='replace')
        for name, texture in re.findall(r'name\s*=\s*"(GFX_\w+)"\s+texturefile\s*=\s*"([^"]+)"', text):
            sprites[name] = texture
    for icon in icons:
        check('GFX_' + icon in sprites, 'Missing sprite: ' + icon)
        check((ROOT / sprites['GFX_' + icon]).is_file(), 'Missing party texture: ' + icon)
    # Prefix branches before name must never outrank the historical router.
    source = outputs[native_path]
    check(hook_native(source, IDEOLOGIES, '# MDCW HISTORICAL PARTY REGISTRY') == source,
          'Native hook regeneration is not stable')
    pp = PartyPresentation(countries, Builder(countries).party_icons, Builder(countries).icons)
    source2, regional2 = pp.bespoke(source, IDEOLOGIES, outputs[registry_path])
    check(source2 == source, 'Icon route regeneration is not stable')
    # Confirm the actual generator is repeatable against its own proposed files.
    original_read = Path.read_text
    def proposed_read(path, *args, **kwargs):
        try: relative = path.relative_to(ROOT).as_posix()
        except ValueError: relative = ''
        value = outputs.get(relative)
        if value is None: return original_read(path, *args, **kwargs)
        return value.lstrip('\ufeff') if kwargs.get('encoding') == 'utf-8-sig' else value
    with patch.object(Path, 'read_text', proposed_read):
        repeated = assemble()
    check(repeated == outputs, 'Full party-only generation is not idempotent')
    report = {'checks': checks, 'countries': len(names), 'families_per_country': 24,
              'sample_dates': 5, 'unique_text_icons': len(icons),
              'native_game_runtime_tested': False, 'examples_1970': selected_labels}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if key != 'examples_1970'}))


if __name__ == '__main__':
    main()
