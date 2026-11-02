# IMPERIA COLD WAR — France 1970 narrow shared-file integration.
"""Preserve the live shared providers and patch only France-owned entry points."""
from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from focus_prerequisite_ui import nodes

MARK = '# IMPERIA COLD WAR — France 1970 national programme integration.\n'


def _header(text: str) -> str:
    return text if text.startswith(MARK) else MARK + text


def _english_header(text: str) -> str:
    """Keep the mandatory YAML root first, then mark this narrow integration."""
    root = 'l_english:\n'
    marker = '# IMPERIA COLD WAR — France 1970 bilateral budget breakdown integration.\n'
    assert text.startswith(root), 'Shared English money localisation root changed.'
    if marker not in text.split(root, 1)[1][:160]:
        text = root + marker + text[len(root):]
    return text


def _append_effect(text: str, name: str, addition: str) -> str:
    effect = next(n for n in nodes(text) if n.key == name)
    return text[:effect.end - 1] + addition + text[effect.end - 1:]


def build_integrations() -> dict[str, str]:
    outputs = {}
    rel = 'history/countries/FRA - France.txt'
    text = (ROOT / rel).read_text(encoding='utf-8-sig')
    old = ('# IMPERIA COLD WAR — Previous France tree retired pending replacement approval.\n'
           '\t\tmdcw_load_1970_fallback_tree = yes')
    new = ('# IMPERIA COLD WAR — Approved France 1970 replacement.\n'
           '\t\tload_focus_tree = COLDWAR_FRA2_1970_focus\n'
           '\t\tCOLDWAR_FRA2_initialize = yes')
    if old in text:
        assert text.count(old) == 1
        text = text.replace(old, new)
    else:
        assert new in text, 'France history entry point changed; inspect before integration.'
    outputs[rel] = _header(text)

    rel = 'localisation/english/MD_money_l_english.yml'
    text = (ROOT / rel).read_text(encoding='utf-8-sig')
    income_key = ' ADDITIONAL_INCOME_REVENUES_TOOLTIP: '
    expense_key = ' ADDITIONAL_EXPENSES_TOOLTIP: '
    assert text.count(income_key) == 1 and text.count(expense_key) == 1
    income_line = next(line for line in text.splitlines() if line.startswith(income_key))
    expense_line = next(line for line in text.splitlines() if line.startswith(expense_key))
    income_token = '[COLDWAR_FRA2_cooperation_weekly_income_display]'
    expense_token = '[COLDWAR_FRA2_cooperation_weekly_expense_display]'
    if income_token not in income_line:
        end = income_line.rfind('"')
        income_new = income_line[:end] + income_token + income_line[end:]
        text = text.replace(income_line, '# IMPERIA COLD WAR — French cooperation income breakdown.\n' + income_new)
    else:
        assert income_line.count(income_token) == 1
    expense_line = next(line for line in text.splitlines() if line.startswith(expense_key))
    if expense_token not in expense_line:
        anchor = '[additional_expense_inflation]'
        end = expense_line.rfind('"')
        value = expense_line[:end]
        assert value.count(anchor) == 1
        expense_new = value.replace(anchor, expense_token + anchor, 1) + expense_line[end:]
        text = text.replace(expense_line, '# IMPERIA COLD WAR — French cooperation expense breakdown.\n' + expense_new)
    else:
        assert expense_line.count(expense_token) == 1
    outputs[rel] = _english_header(text)

    rel = 'common/scripted_effects/mdcw_1970_focus_tree_effects.txt'
    text = (ROOT / rel).read_text(encoding='utf-8-sig')
    route = ('\n\t# IMPERIA COLD WAR — France replacement routing BEGIN\n'
             '\tif = {\n\t\tlimit = { tag = FRA IMP_is_1970_scenario = yes '\
             'NOT = { has_focus_tree = COLDWAR_FRA2_1970_focus } }\n'
             '\t\tload_focus_tree = COLDWAR_FRA2_1970_focus\n'
             '\t\tCOLDWAR_FRA2_initialize = yes\n\t}\n'
             '\t# IMPERIA COLD WAR — France replacement routing END\n')
    if 'France replacement routing BEGIN' not in text:
        start = text.index('{', text.index('mdcw_load_1970_fallback_tree =')) + 1
        text = text[:start] + route + text[start:]
    exemption = '\t\t\t\t\tAND = { tag = FRA IMP_is_1970_scenario = yes } # COLDWAR_FRA2 authored tree\n'
    if exemption not in text:
        target = '\t\t\t\t\tAND = { tag = CUB IMP_is_1970_scenario = yes }'
        assert text.count(target) == 1
        text = text.replace(target, exemption + target)
    outputs[rel] = _header(text)

    rel = 'common/scripted_effects/99_FRA_scripted_effects.txt'
    text = (ROOT / rel).read_text(encoding='utf-8-sig')
    target = ('FRA_update_party_programmes = {\n'
              '\t# IMPERIA COLD WAR — Modern programme callback excludes the 1970 campaign.\n'
              '\tif = {\n\t\tlimit = { NOT = { IMP_is_1970_scenario = yes } }')
    replacement = ('FRA_update_party_programmes = {\n'
                   '\t# IMPERIA COLD WAR — Actual native subparty callback, including same-outlook changes.\n'
                   '\tif = {\n\t\tlimit = { IMP_is_1970_scenario = yes }\n'
                   '\t\tif = { limit = { tag = FRA } COLDWAR_FRA2_sync_programmes = yes }\n'
                   '\t}\n\telse = {')
    if target in text:
        assert text.count(target) == 1
        text = text.replace(target, replacement)
    else:
        assert replacement in text, 'Native French subparty callback changed.'
    outputs[rel] = _header(text)

    rel = 'common/scripted_effects/00_money_system.txt'
    text = (ROOT / rel).read_text(encoding='utf-8-sig')
    income_addition = ('\t# IMPERIA COLD WAR — France matched weekly income BEGIN\n'
                       '\t# The native aggregator runs in each payer or recipient country scope.\n'
                       '\tCOLDWAR_FRA2_add_weekly_income = yes\n'
                       '\t# IMPERIA COLD WAR — France matched weekly income END\n')
    if 'France matched weekly income BEGIN' not in text:
        text = _append_effect(text, 'calculate_additional_income_rate', income_addition)
    else:
        assert text.count('COLDWAR_FRA2_add_weekly_income = yes') == 1
    addition = ('\t# IMPERIA COLD WAR — France GDP programme expenses BEGIN\n'
                '\t# The native aggregator runs in each payer country, including every RP recipient.\n'
                '\tCOLDWAR_FRA2_add_weekly_expenses = yes\n'
                '\t# IMPERIA COLD WAR — France GDP programme expenses END\n')
    if 'France GDP programme expenses BEGIN' not in text:
        text = _append_effect(text, 'calculate_additional_expense_rate', addition)
    else:
        assert text.count('COLDWAR_FRA2_add_weekly_expenses = yes') == 1
    outputs[rel] = _header(text)
    return outputs
