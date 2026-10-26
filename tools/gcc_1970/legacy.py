# IMPERIA CW — Cold War: gcc 1970 — legacy.
"""Bounded 1970 adapters for native GCC decisions and startup membership.

The existing package charges the dominant member $25bn through a later news
event without that payer choosing an acceptance option. Keep it available to
modern MD scenarios, but hide it in the 1970 scenario. All other native GCC
decisions and all original arms-package conditions/effects remain unchanged.
Only the six-member native GCC startup seed is wrapped: modern starts retain
the original list, while 1970 delegates to actual-membership reconciliation.
"""
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RELATIVE = 'common/decisions/Gulf.txt'
MARKER = '# COLDWAR GCC: modern $25bn arms package is outside the 1970 council programme.'
INSERT = '\n\t\t\t' + MARKER + '\n\t\t\tNOT = { IMP_is_1970_scenario = yes }'
STARTUP_RELATIVE = 'common/scripted_effects/00_startup_effects.txt'
STARTUP_BEGIN = '# COLDWAR GCC MEMBERSHIP ARRAY BEGIN'
STARTUP_END = '# COLDWAR GCC MEMBERSHIP ARRAY END'
STARTUP_TAGS = ('SAU','QAT','UAE','BHR','KUW','OMA')
STARTUP_ORIGINAL = '\t#Starting GCC Member States\n' + ''.join(
    '\tadd_to_array = { global.gcc_member_state = '+tag+' }\n' for tag in STARTUP_TAGS)


def startup_region(text):
    """Locate only the original six-member seed or our exact marked wrapper."""
    anchor = '\t#Starting GCC Member States'
    assert text.count(anchor) == 1, 'Native GCC startup seed anchor changed'
    begin = text.index(anchor)
    newline = '\r\n' if text[begin+len(anchor):].startswith('\r\n') else '\n'
    if STARTUP_BEGIN in text:
        assert text.count(STARTUP_BEGIN) == text.count(STARTUP_END) == 1
        end = text.index('\t'+STARTUP_END, begin) + len('\t'+STARTUP_END+newline)
    else:
        native = STARTUP_ORIGINAL.replace('\n', newline)
        assert text[begin:].startswith(native), 'Native GCC startup membership seed changed'
        end = begin + len(native)
    return begin, end, newline


def patch_startup(text):
    """Keep modern seeding intact; 1970 uses real sovereign membership only."""
    begin, end, newline = startup_region(text)
    native_rows = '\n'.join('\t'+line for line in STARTUP_ORIGINAL.splitlines()[1:])
    actual = '\n'.join('\t\t'+tag+' = { COLDWAR_GCC_refresh_membership_array = yes }' for tag in STARTUP_TAGS)
    replacement = ('\t#Starting GCC Member States\n\t'+STARTUP_BEGIN+'\n\t# IMPERIA CW — Cold War: Scenario-specific GCC membership.\n'
                   '\tif = {\n\t\tlimit = { NOT = { IMP_is_1970_scenario = yes } }\n'
                   +native_rows+'\n\t}\n\telse = {\n'+actual+'\n\t}\n\t'+STARTUP_END+'\n')
    return text[:begin]+replacement.replace('\n',newline)+text[end:]


def patch(text):
    """Insert only inside the existing decision's visible block, idempotently."""
    match = re.search(r'(?m)^\s*GCC_request_bloc_arms_sales\s*=\s*\{', text)
    if not match:
        raise AssertionError('Native GCC bloc arms decision is missing')
    visible = re.search(r'\bvisible\s*=\s*\{', text[match.end():])
    if not visible:
        raise AssertionError('Native GCC bloc arms visibility block is missing')
    position = match.end() + visible.end()
    if text[position:].startswith(INSERT):
        return text
    if MARKER in text:
        raise AssertionError('Existing GCC arms guard changed; inspect instead of duplicating it')
    return text[:position] + INSERT + text[position:]


def install(root=ROOT):
    changed = []
    for relative, adapter in ((RELATIVE,patch),(STARTUP_RELATIVE,patch_startup)):
        path = Path(root) / relative
        original = path.read_bytes()
        adapted = adapter(original.decode('utf-8-sig'))
        payload = (b'\xef\xbb\xbf' if original.startswith(b'\xef\xbb\xbf') else b'') + adapted.encode('utf-8')
        if payload != original:
            path.write_bytes(payload)
            changed.append(relative)
    return changed


if __name__ == '__main__':
    print(install())
