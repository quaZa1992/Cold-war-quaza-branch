# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Wire country-specific retirement into MD's existing button and dispatcher.

The temporary context distinguishes a manual retirement from authored elections
and scripted appointments. Nothing here runs at startup or changes history.
"""
from __future__ import annotations

import re
from collections import defaultdict

from dispatch import _find_block_end, _starter_name_aliases, _quote


GUI = 'common/scripted_guis/00_MD_politicsview_scripted_guis.txt'
SETUP = 'common/scripted_effects/00_leader_setup_scripted_effects.txt'
CONTEXT_BEGIN = '# MDCW NATIVE RETIREMENT CONTEXT BEGIN'
CONTEXT_END = '# MDCW NATIVE RETIREMENT CONTEXT END'
SYNC_BEGIN = '# MDCW SPECIAL RETIREMENT SYNC BEGIN'
SYNC_END = '# MDCW SPECIAL RETIREMENT SYNC END'
ROUTE_BEGIN = '# MDCW SOVIET RETIREMENT ROUTE BEGIN'
ROUTE_END = '# MDCW SOVIET RETIREMENT ROUTE END'
ENABLED_BEGIN = '# MDCW SOVIET RETIREMENT AVAILABILITY BEGIN'
ENABLED_END = '# MDCW SOVIET RETIREMENT AVAILABILITY END'


def alternative_trigger(root, ready, special_report, yeltsin_available=False):
    """A retirement must have someone other than the current sole candidate."""
    groups = defaultdict(dict)
    for row in ready:
        groups[(row['tag'], row['party_index'])].setdefault(row['name'].casefold(), row)
    for tag, report in special_report.get('countries', {}).items():
        for row in report.get('included', []):
            groups[(tag, row['family'])].setdefault(row['name'].casefold(),
                {'id': re.sub(r'[^a-z0-9]+', '_', row['name'].casefold()), 'name': row['name']})
    if yeltsin_available:
        groups[('SOV', 2)]['boris yeltsin'] = {'id': 'boris_yeltsin', 'name': 'Boris Yeltsin'}
    rows = {key: list(value.values()) for key, value in groups.items()}
    aliases = _starter_name_aliases(root, rows)
    blocked = []
    for (tag, index), people in sorted(rows.items()):
        if len(people) != 1:
            continue
        person = people[0]
        names = [person['name']]
        alias = aliases.get((tag, index, person['name']))
        if alias and alias not in names:
            names.append(alias)
        tests = ' '.join('has_country_leader = { name = ' + _quote(name) + ' ruling_only = yes }' for name in names)
        if len(names) > 1:
            tests = 'OR = { ' + tests + ' }'
        blocked.append('\t\tAND = { original_tag = ' + tag + ' check_variable = { ruling_party = ' + str(index) + ' } ' + tests + ' }')
    return ('# IMPERIA CW — Cold War: historical politics 1970 generated content.\n# Generated: prevent charging retirement for the same sole historical leader.\nMDCW_HP_retirement_has_alternative = {\n\tNOT = { OR = {\n'
            + '\n'.join(blocked) + '\n\t} }\n}\n')


def strip_region(text, begin, end, replacement=''):
    pattern = re.compile(r'(?ms)^[ \t]*' + re.escape(begin) + r'\n.*?^[ \t]*' + re.escape(end) + r'\n?')
    matches = list(pattern.finditer(text))
    if len(matches) > 1:
        raise ValueError('Repeated retirement marker: ' + begin)
    return pattern.sub(replacement, text)


def strip_setup(text):
    text = strip_region(text, SYNC_BEGIN, SYNC_END)
    text = strip_region(text, ROUTE_BEGIN, ROUTE_END)
    # The original CYP first branch becomes else_if after our early SOV route.
    text = re.sub(r'(?m)^(\t)else_if(?= = \{\n\t\tlimit = \{ original_tag = CYP IMP_is_1970_scenario = yes \})', r'\1if', text)
    return text


def strip_gui(text):
    text = strip_region(text, CONTEXT_BEGIN, CONTEXT_END, '\t\t\t\t\tset_leader = yes\n')
    text = strip_region(text, ENABLED_BEGIN, ENABLED_END)
    text = text.replace('NOT = { AND = { OR = { original_tag = DDR original_tag = PAK } IMP_is_1970_scenario = yes NOT = { MDCW_HP_has_native_pool = yes } } }',
                        'NOT = { AND = { OR = { original_tag = DDR original_tag = PAK } IMP_is_1970_scenario = yes } }')
    return text


def _region(text, name):
    match = re.search(r'(?m)^([ \t]*)' + re.escape(name) + r'\s*=\s*\{', text)
    if not match:
        raise ValueError('Missing native button block: ' + name)
    opening = text.find('{', match.start(), match.end())
    end = _find_block_end(text, opening)
    return opening + 1, end - 1


def wire_retirement(outputs):
    text = strip_setup(outputs[SETUP])
    sync_marker = '# MDCW HISTORICAL NATIVE COUNTER SYNC END\n'
    if text.count(sync_marker) != 1:
        raise ValueError('Native generic counter sync marker missing')
    sync = ('\t' + SYNC_BEGIN + '\n\t# IMPERIA CW — Cold War: Historical successor counter synchronisation.\n'
            '\tMDCW_HP_sync_special_counter = yes\n'
            '\tMDCW_HP_sync_sov_egy_counter = yes\n'
            '\t' + SYNC_END + '\n')
    text = text.replace(sync_marker, sync_marker + sync, 1)
    first = '\tif = {\n\t\tlimit = { original_tag = CYP IMP_is_1970_scenario = yes }'
    if text.count(first) != 1:
        raise ValueError('Native first CYP dispatch route changed')
    route = ('\t' + ROUTE_BEGIN + '\n\t# IMPERIA CW — Cold War: Soviet historical retirement routing.\n'
             '\tif = {\n'
             '\t\tlimit = { IMP_is_1970_scenario = yes original_tag = SOV is_dynamic_country = no '
             'check_variable = { ruling_party = 4 } check_variable = { MDCW_HP_native_retirement = 1 } }\n'
             '\t\tMDCW_HP_SOV_native_retirement = yes\n'
             '\t}\n'
             '\t' + ROUTE_END + '\n')
    text = text.replace(first, route + first.replace('\tif =', '\telse_if =', 1), 1)
    outputs[SETUP] = text

    text = strip_gui(outputs[GUI])
    start, end = _region(text, 'retire_leader_button_click')
    body = text[start:end]
    call = '\t\t\t\t\tset_leader = yes\n'
    if body.count(call) != 1:
        raise ValueError('Expected one unchanged native retire setter call')
    wrapped = ('\t\t\t\t\t' + CONTEXT_BEGIN + '\n\t\t\t\t\t# IMPERIA CW — Cold War: Historical leader retirement context.\n'
               '\t\t\t\t\tset_temp_variable = { MDCW_HP_native_retirement = 1 }\n'
               + call +
               '\t\t\t\t\tset_temp_variable = { MDCW_HP_native_retirement = 0 }\n'
               '\t\t\t\t\t' + CONTEXT_END + '\n')
    text = text[:start] + body.replace(call, wrapped, 1) + text[end:]
    start, end = _region(text, 'retire_leader_button_click_enabled')
    body = text[start:end]
    old_guard = 'NOT = { AND = { OR = { original_tag = DDR original_tag = PAK } IMP_is_1970_scenario = yes } }'
    new_guard = 'NOT = { AND = { OR = { original_tag = DDR original_tag = PAK } IMP_is_1970_scenario = yes NOT = { MDCW_HP_has_native_pool = yes } } }'
    if body.count(old_guard) == 1:
        body = body.replace(old_guard, new_guard, 1)
    elif body.count(new_guard) != 1:
        raise ValueError('DDR/PAK retirement guard changed unexpectedly')
    availability = ('\t\t\t\t' + ENABLED_BEGIN + '\n\t\t\t\t# IMPERIA CW — Cold War: Historical retirement availability.\n'
                    '\t\t\t\tif = {\n'
                    '\t\t\t\t\tlimit = { IMP_is_1970_scenario = yes }\n'
                    '\t\t\t\t\tcustom_trigger_tooltip = { tooltip = MDCW_HP_retirement_no_alternative_tt MDCW_HP_retirement_has_alternative = yes }\n'
                    '\t\t\t\t}\n'
                    '\t\t\t\tif = {\n'
                    '\t\t\t\t\tlimit = { IMP_is_1970_scenario = yes original_tag = SOV is_dynamic_country = no check_variable = { ruling_party = 4 } }\n'
                    '\t\t\t\t\tMDCW_HP_SOV_retirement_available = yes\n'
                    '\t\t\t\t}\n'
                    '\t\t\t\t' + ENABLED_END + '\n')
    if not body.startswith('\n'):
        raise ValueError('Native retirement availability lost its leading newline')
    outputs[GUI] = text[:start] + '\n' + availability + body[1:] + text[end:]
