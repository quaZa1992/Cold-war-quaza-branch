# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Country-specific party presentation, independent of leader appointments."""
from copy import deepcopy
import json
from pathlib import Path
import re
import unicodedata

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CUSTOM_PREFIX = r'(?:COLDWAR_|ISR70_|LBA_1970\.)'


def special_tag(key):
    match = re.match(r'COLDWAR_([A-Z]{3})_', key)
    if match:
        return match[1]
    if key.startswith('ISR70_'):
        return 'ISR'
    match = re.match(r'([A-Z]{3})_1970\.', key)
    return match[1] if match else None


def load_names():
    countries = {}
    for path in sorted(HERE.glob('data_party_names_*.json')):
        payload = json.loads(path.read_text(encoding='utf-8-sig'))
        for tag, country in payload['countries'].items():
            assert tag not in countries, ('duplicate party presentation', tag)
            assert len(country['labels']) == 24, (tag, 'expected 24 MD families')
            assert all(isinstance(name, str) and name.strip() for name in country['labels']), tag
            countries[tag] = country
        for key, display in payload.get('bespoke_names', {}).items():
            tag = special_tag(key)
            assert tag in countries, ('unowned regional name', key)
            countries[tag].setdefault('bespoke_names', {})[key] = display
    return countries


class PartyPresentation:
    def __init__(self, countries, manifest, icons):
        self._countries = countries
        self.names = load_names()
        assert not (set(countries) - set(self.names)), ('missing country names', sorted(set(countries) - set(self.names)))
        self.reference = json.loads((HERE / 'party_md_reference.json').read_text(encoding='utf-8'))
        self.manifest, self.icons = manifest, icons

    def parties(self, tag, parties):
        output = deepcopy(parties)
        names = self.names[tag].get('party_names', {})
        for row in output:
            row['source_name'] = row['name']
            row['name'] = names.get(row['name'], row['name'])
        return output

    def icon(self, tag, ideology, party):
        reviewed = self.manifest.get(party.get('icon_id', ''), {}).get('text_icon')
        if reviewed:
            return reviewed.replace('£GFX_', '£')
        original = party.get('source_name', party['name'])
        if any(row.get('tag') == tag and row.get('party_name_match') == original
               for row in self.manifest.values()):
            # Icon validity windows were already split into catalogue rows by
            # bind_icons.py. Never reintroduce a later emblem into an earlier
            # unbound segment (e.g. Congress's post-1978 hand in 1970).
            return self.icons[ideology]
        native = self.reference['icons'].get(tag, {}).get(original, {}).get('text_icon')
        if native:
            return native
        native = self.native_icon(tag, party['name'])
        if native:
            return native
        return self.icons[ideology]

    def native_icon(self, tag, name):
        """Match a local party name or an unambiguous country-local acronym."""
        def normalized(value):
            value = unicodedata.normalize('NFKD', value).casefold()
            return re.sub(r'[^a-z0-9]', '', value)
        plain = re.sub(r'\s*\([^)]*\)', '', name)
        exact, acronyms = set(), set()
        wanted = set(re.findall(r'\b[A-Z][A-Z0-9]{2,}\b', name))
        for candidate in self.reference.get('native_icons', {}).get(tag, []):
            if normalized(candidate['organization']) in {normalized(name), normalized(plain)}:
                exact.add(candidate['text_icon'])
            # Only read acronyms from the label's parentheses. Words in a
            # title such as USA must not bind an unrelated party's emblem.
            aliases = set(token for part in re.findall(r'\(([^)]*)\)', candidate['source_name'])
                          for token in re.findall(r'\b[A-Z][A-Z0-9]{2,}\b', part))
            if wanted & aliases:
                acronyms.add(candidate['text_icon'])
        choices = exact or acronyms
        return next(iter(choices)) if len(choices) == 1 else None

    def render(self, tag, ideology, party):
        members = party.get('members', [party])
        icons = [self.icon(tag, ideology, member) for member in members]
        label = ' / '.join(dict.fromkeys(icon + ' ' + member['name'] for icon, member in zip(icons, members)))
        return label, icons[0] if len(set(icons)) == 1 else self.icons[ideology]

    def family_loc(self, builder, index, ideology):
        family = self.reference['families'][ideology]
        builder.text(f'MDCW_HP_MD_{ideology}_desc', family['description'])
        builder.text(f'MDCW_HP_family_{index}_desc',
                     '(' + family['name'] + ')\\n\\n$MDCW_HP_MD_' + ideology + '_desc$')

    @staticmethod
    def description(index, historical=''):
        # Former generator prose described internal implementation rather than
        # the ideology. Keep authored historical context, discard boilerplate.
        if historical.startswith(('A historical political organization', 'Historical organizations represented')):
            historical = ''
        prefix = f'$MDCW_HP_family_{index}_desc$'
        return prefix + ('\\n\\n' + historical if historical else '')

    def bespoke(self, source, ideologies, registry=''):
        """Update the original regional localisation keys, not duplicate keys."""
        from validate import Validator
        entries, locations = {}, {}
        for path in sorted((ROOT / 'localisation/english').glob('*.yml')):
            text = path.read_text(encoding='utf-8-sig')
            for match in re.finditer(r'(?m)^\s+([^\s:]+):(?:\d+)?\s*"(.*)"[ \t]*$', text):
                entries[match[1]] = match[2]
                locations[match[1]] = path
        names = {}
        routes = {}
        combined = source + '\n' + registry
        route_seen = set()
        providers = {ideology + '_L': ideology for ideology in ideologies}
        providers.update({'MDCW_HP_' + ideology: ideology for ideology in ideologies})
        for kind, start, opening, end in Validator._parse_blocks(combined):
            if kind != 'defined_text':
                continue
            body = combined[opening + 1:end - 1]
            match = re.search(r'(?m)^[ \t]*name\s*=\s*(\w+)', body)
            if not match or match[1] not in providers:
                continue
            ideology = providers[match[1]]
            index = ideologies.index(ideology)
            for child, begin, child_open, child_end in Validator._parse_blocks(body):
                if child != 'text':
                    continue
                branch = body[begin:child_end]
                key_match = re.search(r'localization_key\s*=\s*"?(' + CUSTOM_PREFIX + r'[\w.-]+)', branch)
                if not key_match:
                    continue
                key = key_match[1]
                tag = special_tag(key)
                assert tag in self.names, ('missing special country', tag)
                names[key] = (tag, index, ideology)
                signature = (ideology, re.sub(r'\s+', ' ', branch).strip())
                if signature not in route_seen:
                    routes.setdefault(ideology, []).append(re.sub(
                        r'(localization_key\s*=\s*"?)' + re.escape(key) + r'\b', r'\g<1>' + key + '_icon', branch))
                    route_seen.add(signature)
        changes = {}
        generic_words = re.compile(r'Atlanticist Administrators|Atlanticist Independents|Conservative Independents|Liberal Independents|Libertarian Left|Eastern-Aligned|Reformist Shiite Circles|Shiite Clerical Circles|Religious Royalists|Caliphate Supporters|Islamist Circles|Non-Aligned Authoritarians|Non-Aligned Conservatives|Business Independents|Classical Liberals|Non-Aligned Social Democrats|Non-Aligned Marxists|National Populists|Ultranationalists|Military Officers')
        for key, (tag, index, ideology) in names.items():
            assert key in entries, ('missing regional party key', key)
            country = self.names[tag]
            old = entries[key]
            old_icon = re.search(r'£\w+', old)
            plain = re.sub(r'^£\w+\s*', '', old)
            display = country.get('bespoke_names', {}).get(key)
            display = display or country.get('party_names', {}).get(plain)
            if not display and (generic_words.search(plain) or entries.get(key + '_desc', '').startswith('A loosely organized alternate political current')):
                display = country['labels'][index]
            display = display or plain
            icon = old_icon[0] if old_icon else self.icons[ideology]
            # A regional logo is authoritative. Generic stars may be replaced
            # by the emblem of the exact historical organization.
            if not old_icon or icon.startswith(('£generic_', '£muslim_brotherhood')):
                native_names = country.get('party_names', {})
                candidates = [row for row in self._countries.get(tag, {}).get('parties', [])
                              if native_names.get(row['name'], row['name']) == display]
                for row in candidates:
                    candidate_icon = self.icon(tag, ideology, row)
                    if not candidate_icon.startswith(('£generic_', '£muslim_brotherhood')):
                        icon = candidate_icon
                        break
                if not candidates:
                    icon = self.native_icon(tag, display) or icon
            path = locations[key]
            changes.setdefault(path, {})[key] = icon + ' ' + display
            changes[path][key + '_icon'] = icon
            desc_key = key + '_desc'
            historical = entries.get(desc_key, '')
            if not historical.startswith(f'$MDCW_HP_family_{index}_desc$'):
                if 'without a documented named organization' in historical or 'not a documented historical party' in historical:
                    historical = ''
                desc_path = locations.get(desc_key, path)
                changes.setdefault(desc_path, {})[desc_key] = self.description(index, historical)
        # Extra dynamic name keys (e.g. Vietnam's 1976 change) are data-owned.
        for country in self.names.values():
            for key, display in country.get('bespoke_names', {}).items():
                if key in entries and key not in names:
                    original_icon = re.match(r'£\w+\s*', entries[key])
                    changes.setdefault(locations[key], {})[key] = (original_icon[0] if original_icon else '') + display
        files = {}
        for path, replacements in changes.items():
            text = path.read_text(encoding='utf-8-sig')
            for key, value in replacements.items():
                line = ' ' + key + ':0 "' + re.sub(r'(?<!\\)"', lambda _: '\\"', value) + '"'
                pattern = r'(?m)^[ \t]+' + re.escape(key) + r':(?:\d+)?[ \t]*".*"[ \t]*$'
                if re.search(pattern, text):
                    text = re.sub(pattern, lambda _: line, text)
                else:
                    text = text.rstrip() + '\n' + line + '\n'
            files[str(path.relative_to(ROOT)).replace('\\', '/')] = '\ufeff' + text
        # Mirror the exact name conditions into icon selectors. Previously the
        # DDR name could show one party while its icon came from another row.
        patches = []
        for kind, start, opening, end in Validator._parse_blocks(source):
            if kind != 'defined_text':
                continue
            body = source[opening + 1:end - 1]
            match = re.search(r'(?m)^[ \t]*name\s*=\s*(\w+)', body)
            if not match or not match[1].endswith('_L_icon'):
                continue
            ideology = match[1][:-7]
            if ideology not in routes:
                continue
            cuts = []
            for child, begin, child_open, child_end in Validator._parse_blocks(body):
                if child == 'text' and re.search(r'localization_key\s*=\s*"?' + CUSTOM_PREFIX, body[begin:child_end]):
                    cuts.append(_whole_line(body, begin, child_end))
            for begin, child_end in reversed(cuts):
                body = body[:begin] + body[child_end:]
            match = re.search(r'(?m)^[ \t]*name[^\n]*\n', body)
            body = body[:match.end()] + '\n'.join('\t' + route for route in routes[ideology]) + '\n' + body[match.end():]
            patches.append((opening + 1, end - 1, body))
        for begin, end, body in reversed(patches):
            source = source[:begin] + body + source[end:]
        return source, files


def _whole_line(body, begin, end):
    start = body.rfind('\n', 0, begin) + 1
    finish = body.find('\n', end)
    finish = len(body) if finish < 0 else finish + 1
    if not body[start:begin].strip() and re.fullmatch(r'[ \t]*(?:#[^\n]*)?\n?', body[end:finish]):
        return start, finish
    return begin, end


def retained_branches(source):
    """Keep the hand-authored DDR/Vietnam/Iraq variants on regeneration."""
    branches, name = {}, None
    for line in source.splitlines():
        match = re.match(r'\s*name\s*=\s*(MDCW_HP_\w+)', line)
        if match:
            name = match[1]
        if name and re.match(r'\s*text\s*=\s*\{.*# COLDWAR', line):
            branches.setdefault(name, []).append(line)
    return branches


def restore_branches(source, branches):
    for name, lines in branches.items():
        needle = '\tname = ' + name + '\n'
        assert needle in source, name
        source = source.replace(needle, needle + '\n'.join(lines) + '\n', 1)
    return source


def hook_native(source, ideologies, marker):
    """Authored historical variants, then world registry, then vanilla MD.

    Regional providers only cover some families. Excluding their whole tag
    used to leak modern/generic names in every other family.
    """
    from validate import Validator
    source = '\n'.join(line for line in source.splitlines() if marker not in line) + '\n'
    changes = []
    wanted = {ideology + '_L' + suffix: ideology + suffix
              for ideology in ideologies for suffix in ('', '_desc', '_icon')}
    wanted['show_ruling_party'] = 'ruling_party'
    for key, start, opening, end in Validator._parse_blocks(source):
        if key != 'defined_text':
            continue
        body = source[opening + 1:end - 1]
        match = re.search(r'(?m)^\s*name\s*=\s*(\w+)\s*$', body)
        if not match or match[1] not in wanted:
            continue
        name = match[1]
        retained = []
        cuts = []
        for child, begin, child_open, child_end in Validator._parse_blocks(body):
            if child != 'text':
                continue
            text = body[begin:child_end]
            if re.search(r'localization_key\s*=\s*"?' + CUSTOM_PREFIX, text):
                line_start = body.rfind('\n', 0, begin) + 1
                line_end = body.find('\n', child_end)
                line_end = len(body) if line_end < 0 else line_end + 1
                # Include the line's comment so repeated builds are stable.
                if not body[line_start:begin].strip() and re.fullmatch(r'[ \t]*(?:#[^\n]*)?\n?', body[child_end:line_end]):
                    retained.append(body[begin:line_end].rstrip())
                    cuts.append((line_start, line_end))
                else:
                    retained.append(text)
                    cuts.append((begin, child_end))
        for begin, child_end in reversed(cuts):
            body = body[:begin] + body[child_end:]
        match = re.search(r'(?m)^[ \t]*name[ \t]*=[ \t]*(\w+)[ \t]*\n', body)
        assert match, name
        body = body[:match.start()] + body[match.end():]
        hook = '\ttext = { trigger = { MDCW_HP_has_country = yes } localization_key = "[MDCW_HP_' + wanted[name] + ']" } ' + marker
        insert = '\n'.join('\t' + text for text in retained) + ('\n' if retained else '') + hook + '\n'
        # Native MD sometimes puts date/cosmetic text before its name field.
        # The registry must still precede those modern/1985 alternatives.
        body = '\n\tname = ' + name + '\n' + insert + body.lstrip('\n')
        changes.append((opening + 1, end - 1, body))
    assert len(changes) == 73, ('native family hooks', len(changes))
    for begin, end, body in reversed(changes):
        source = source[:begin] + body + source[end:]
    return source
