# IMPERIA CW — Cold War: gulf 1970 — repair region starters.
"""Repair direct 1970 ruler snapshots without regenerating regional mechanics.

Native country selection requires dated, direct ruler/outlook entries. Keep
the existing scripted regional initialization and all later history intact.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import runpy
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/historical_politics_1970'))
from build import IDEOLOGIES
from validate import Validator

API = runpy.run_path(str(ROOT / 'tools/gulf_1970/validate.py'))
parse, first, values, walk = (API[key] for key in ('parse', 'first', 'values', 'walk'))
TAGS = 'BHR KUW OMA QAT SAU UAE YEM SYE IRQ PER JOR LEB SYR EGY ISR PAL TUR GRE CYP NCY LBA ALG MOR TUN SUD'.split()
SPECIAL = {
    'ISR': {'name': 'Golda Meir', 'picture': 'gfx/leaders/ISR/ISR_Coldwar_Golda_Meir.dds',
            'ideology': 'socialism', 'profile_source': 'common/scripted_effects/ISR70_effects.txt',
            'profile': 'ISR70_apply_starting_politics'},
    'NCY': {'name': 'Fazıl Küçük', 'picture': 'gfx/leaders/NCY/1970/COLDWAR_NCY_1970_kucuk.dds',
            'ideology': 'conservatism', 'profile_source': 'common/scripted_effects/IMP_1970_world_politics_effects.txt',
            'profile': 'IMP_1970_profile_democratic_conservative'},
}


def scalar(value):
    return value.strip('"')


def flat(key, fields):
    return '\t' + key + ' = { ' + ' '.join(k + ' ' + op + ' ' + v for k, op, v in fields) + ' }\n'


def date_blocks(source):
    for match in re.finditer(r'(?m)^1970\.1\.1\s*=\s*\{', source):
        opening = source.index('{', match.start())
        end = Validator._brace_end(source, opening, len(source))
        yield opening, end


def digest(data):
    return hashlib.sha256(data).hexdigest()


def apply(backup_root):
    report_path = ROOT / 'docs/regional_starting_rulers_1970_20261019.json'
    previous = json.loads(report_path.read_text(encoding='utf-8')) if report_path.exists() else {}
    old_rows = {row['tag']: row for row in previous.get('countries', [])}
    report = {'scope': '1970 Middle East, Arabian Peninsula, North Africa and eastern Mediterranean',
              'native_game_runtime_tested': False, 'countries': [], 'repaired_setters': [],
              'source_notes': [
                  'Existing authored history and regional providers supply identities, portraits and native ideology assignments.',
                  'Golda Meir: https://main.knesset.gov.il/EN/About/Lexicon/Pages/Meir_Golda.aspx',
                  'Northern Cyprus remains a potential tag. Adding a ruler does not transfer states or create a country.'],
              'backup_root': str(backup_root)}
    gulf_roster = json.loads((ROOT / 'docs/gulf_start_1970_portraits_20261019.json').read_text(encoding='utf-8'))['items']
    gulf_by_token = {row['token']: row for row in gulf_roster}
    def write(relative, old, new):
        if old == new:
            return False
        target = ROOT / relative
        backup = backup_root / relative
        if not backup.exists():
            backup.parent.mkdir(parents=True, exist_ok=True)
            backup.write_bytes(old)
        target.write_bytes(new)
        return True

    for tag in TAGS:
        path = next((ROOT / 'history/countries').glob(tag + ' - *.txt'))
        original = path.read_bytes()
        boundary = re.search(rb'(?m)^2000\.1\.1[ \t]*=', original)
        assert boundary or tag == 'SYE', ('missing later history boundary', tag)
        prefix_bytes, later = (original[:boundary.start()], original[boundary.start():]) if boundary else (original, b'')
        prefix = prefix_bytes.decode('utf-8-sig').replace('\r\n', '\n')
        parsed = parse(prefix)
        starts = values(parsed, '1970.1.1')
        direct = [(node, first(node, 'create_country_leader')) for node in starts
                  if first(node, 'create_country_leader') is not None]
        for node in starts:
            promotion = first(node, 'promote_character')
            if promotion is None:
                continue
            token = first(promotion, 'character')
            assert first(node, 'recruit_character') == token, ('unrecruited promoted starter', tag)
            row = gulf_by_token[token]
            direct.append((node, [('name', '=', json.dumps(row['name'], ensure_ascii=False)),
                                  ('picture', '=', json.dumps(row['portrait'])),
                                  ('ideology', '=', row['ideology'])]))
        if direct:
            node, leader = direct[0]
        else:
            candidates = [v for node in starts for k, op, v in walk(node) if k == 'create_country_leader']
            if candidates:
                assert len(candidates) == 1, ('ambiguous starting ruler', tag)
                leader = candidates[0]
            else:
                assert tag in SPECIAL, ('missing authored ruler', tag)
                leader = [('name', '=', json.dumps(SPECIAL[tag]['name'], ensure_ascii=False)),
                          ('picture', '=', json.dumps(SPECIAL[tag]['picture'])),
                          ('ideology', '=', SPECIAL[tag]['ideology'])]
            node = starts[0]
        ideology = first(leader, 'ideology')
        index = IDEOLOGIES.index(ideology)
        if not direct:
            special = SPECIAL.get(tag)
            if special:
                profile_path = ROOT / special['profile_source']
                profile_name = special['profile']
            else:
                profile_path = ROOT / 'common/scripted_effects/IMP_1970_world_politics_effects.txt'
                profile_name = re.search(r'\b(IMP_1970_profile_\w+)\s*=\s*yes', prefix)[1]
            profile = first(parse(profile_path.read_text(encoding='utf-8-sig')), profile_name)
            politics = next((v for k, op, v in walk(node) if k == 'set_politics'), None) or first(profile, 'set_politics')
            popularity = first(profile, 'set_popularities')
            assert politics and popularity, ('missing political snapshot', tag)
            first_opening, first_end = next(date_blocks(prefix))
            body = prefix[first_opening + 1:first_end - 1]
            # Move only the historical incumbent; scripted initialization stays.
            for key, begin, opening, end in Validator._parse_blocks(body):
                if key != 'create_country_leader':
                    continue
                line_begin = body.rfind('\n', 0, begin) + 1
                line_end = body.find('\n', end)
                line_end = len(body) if line_end < 0 else line_end + 1
                assert not body[line_begin:begin].strip() and not body[end:line_end].strip(), tag
                body = body[:line_begin] + body[line_end:]
                break
            snapshot = ('\n\t# Native 1970 ruler/outlook snapshot for country-selection preview.\n'
                        + flat('set_popularities', popularity) + flat('set_politics', politics)
                        + f'\tset_variable = {{ ruling_party = {index} }}\n'
                        + '\tcreate_country_leader = {\n')
            for key, op, value in leader:
                assert not isinstance(value, list) or not value, (tag, key)
                snapshot += '\t\t' + key + ' ' + op + ' ' + ('{ }' if isinstance(value, list) else value) + '\n'
            snapshot += '\t}\n'
            prefix = prefix[:first_opening + 1] + body.rstrip() + '\n' + snapshot + prefix[first_end - 1:]
        # South Yemen already had a direct ruler in a second same-date block.
        # Add its MD slot there rather than creating a competing ruler.
        parsed = parse(prefix)
        for opening, end in date_blocks(prefix):
            body = prefix[opening + 1:end - 1]
            tree = parse(body)
            if first(tree, 'create_country_leader') is None:
                continue
            variables = values(tree, 'set_variable')
            if not any(first(variable, 'ruling_party') is not None for variable in variables):
                prefix = prefix[:end - 1] + f'\tset_variable = {{ ruling_party = {index} }}\n' + prefix[end - 1:]
            break
        # Preserve exact later-bookmark bytes, including original CRLF endings.
        changed = False
        if prefix != prefix_bytes.decode('utf-8-sig').replace('\r\n', '\n'):
            changed = write(path.relative_to(ROOT), original, b'\xef\xbb\xbf' + prefix.encode('utf-8') + later)
        baseline_path = backup_root / path.relative_to(ROOT)
        originally_direct = bool(direct)
        if baseline_path.exists():
            baseline = parse(baseline_path.read_text(encoding='utf-8-sig'))
            originally_direct = any(first(block, 'create_country_leader') is not None for block in values(baseline, '1970.1.1'))
        row = {'tag': tag, 'name': scalar(first(leader, 'name')), 'ideology': ideology, 'party_index': index,
               'portrait': scalar(first(leader, 'picture')), 'history': path.relative_to(ROOT).as_posix(),
               'later_history_sha256': digest(later),
               'new_direct_snapshot': old_rows.get(tag, {}).get('new_direct_snapshot', not originally_direct),
               'changed_this_run': changed}
        assert (ROOT / row['portrait']).is_file(), ('missing portrait', row)
        report['countries'].append(row)
        setter_path = ROOT / 'common/scripted_effects' / (tag + '_political_leaders.txt')
        if setter_path.exists():
            old = setter_path.read_bytes()
            needle = ('# MDCW HISTORICAL NATIVE POOL END ' + tag + '}').encode()
            if needle in old:
                new = old.replace(needle, ('# MDCW HISTORICAL NATIVE POOL END ' + tag + '\n}').encode())
                parse(new.decode('utf-8-sig'))
                write(setter_path.relative_to(ROOT), old, new)
                report['repaired_setters'].append(tag)
            elif tag in previous.get('repaired_setters', []):
                report['repaired_setters'].append(tag)
            elif (backup_root / setter_path.relative_to(ROOT)).exists() and needle in (backup_root / setter_path.relative_to(ROOT)).read_bytes():
                report['repaired_setters'].append(tag)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--backup-root', type=Path, required=True)
    args = cli.parse_args()
    result = apply(args.backup_root)
    print(json.dumps({'countries_audited': len(result['countries']),
                      'histories_changed': sum(row['changed_this_run'] for row in result['countries']),
                      'new_direct_snapshots': sum(row['new_direct_snapshot'] for row in result['countries']),
                      'repaired_setters': result['repaired_setters']}))
