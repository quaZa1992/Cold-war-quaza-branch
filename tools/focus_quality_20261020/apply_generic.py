# IMPERIA CW — Cold War: focus quality 20261020 — apply generic.
"""Targeted live installation of the approved generic office transactions."""
import re
import sys
from source_edit import ROOT, write, focus_span

sys.path.insert(0, str(ROOT / 'Claude outputs/COLDWAR_GEN_generator'))
from gen_quality import OFFICE_PROJECTS, prefix, runtime_files, patch_base_office_focus


def apply():
    path = ROOT / 'common/national_focus/mdcw_1970_generic_focus.txt'
    text = path.read_text(encoding='utf-8-sig')
    for fid, (share, _) in OFFICE_PROJECTS.items():
        if share is None:
            continue
        a, b = focus_span(text, fid)
        body = text[a:b]
        if prefix(fid) + '_open = yes' in body:
            continue
        extra = 'one_random_infrastructure = yes' if fid == 'GEN_1970_nlib_free_enterprise_zones' else ''
        total_share = share + (0.005 if extra else 0)
        pattern = (r'set_temp_variable = \{ skip_payment = 1 \}\s*'
                   r'two_office_construction = yes\s*' + (re.escape(extra) + r'\s*' if extra else '') +
                   r'set_temp_variable = \{ skip_payment = 0 \}\s*'
                   r'set_temp_variable = \{ treasury_change = \{ value = gdp_total multiply = -' + f'{total_share:.3f}' + r' \} \}\s*'
                   r'modify_treasury_effect = yes')
        replacement = prefix(fid) + '_open = yes'
        if extra:
            replacement += '\n\t\t\tset_temp_variable = { skip_payment = 1 }\n\t\t\t' + extra + '\n\t\t\tset_temp_variable = { skip_payment = 0 }\n\t\t\tset_temp_variable = { treasury_change = { value = gdp_total multiply = -0.005 } }\n\t\t\tmodify_treasury_effect = yes'
        body, count = re.subn(pattern, replacement, body)
        assert count == 1, fid
        text = text[:a] + body + text[b:]
    text = patch_base_office_focus(text)
    write(path, text)
    for relative, payload in runtime_files().items():
        write(ROOT / relative, payload.strip() + '\n')


if __name__ == '__main__':
    apply()
