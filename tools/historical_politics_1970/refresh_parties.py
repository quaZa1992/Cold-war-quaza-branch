# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Rebuild only party display files; never regenerate leader pools/history."""
import argparse
import hashlib
import json
from pathlib import Path
import re

from build import Builder, ROOT, load_catalog, loc_quote


def assemble():
    builder = Builder(load_catalog())
    builder.parties()
    path = 'localisation/english/mdcw_historical_politics_1970_l_english.yml'
    source = (ROOT / path).read_text(encoding='utf-8-sig')
    generated = re.compile(r'MDCW_HP_(?:[A-Z0-9]{3}_(?:party|current)_\d|generic_\d|family_\d|MD_).*')
    preserved = []
    for line in source.splitlines():
        match = re.match(r'\s+([^\s:]+):', line)
        if match and not generated.fullmatch(match[1]):
            preserved.append(line)
    builder.outputs[path] = '\ufeffl_english:\n# IMPERIA CW — Cold War: historical politics 1970 English localisation.\n' + '\n'.join(preserved + [
        ' ' + key + ':0 ' + loc_quote(value) for key, value in builder.loc.items()]) + '\n'
    return builder.outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True,
                        help='Staging directory; also stores original files when installing.')
    parser.add_argument('--install', action='store_true')
    args = parser.parse_args()
    outputs = assemble()
    report = {'files': {}, 'scope': 'Party names, ideology explanations and text-icon routing only.'}
    for relative, text in outputs.items():
        original = (ROOT / relative).read_bytes() if (ROOT / relative).exists() else None
        target = args.output / 'staged' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8', newline='\n')
        if original is not None:
            backup = args.output / 'before' / relative
            # Preserve the original review baseline across retries.
            if not backup.exists():
                backup.parent.mkdir(parents=True, exist_ok=True)
                backup.write_bytes(original)
        encoded = text.encode('utf-8')
        report['files'][relative] = {'before_sha256': hashlib.sha256(original).hexdigest() if original else None,
                                    'after_sha256': hashlib.sha256(encoded).hexdigest(),
                                    'changed': original != encoded}
        if args.install and original != encoded:
            (ROOT / relative).write_bytes(encoded)
    (args.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'files': len(outputs), 'changed': sum(row['changed'] for row in report['files'].values()),
                      'installed': args.install, 'report': str(args.output / 'report.json')}))


if __name__ == '__main__':
    main()
