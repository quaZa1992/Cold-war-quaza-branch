# IMPERIA CW — Cold War: uae 1970 — decision routes.
"""Keep the 1970 UAE resource investment programme in its focus tree."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
PATH = 'common/decisions/categories/00_resources_expansion.txt'
BEGIN = '# COLDWAR UAE FOCUS INVESTMENT BEGIN'
END = '# COLDWAR UAE FOCUS INVESTMENT END'


def build(data):
    text = (ROOT/PATH).read_text(encoding='utf-8-sig')
    text = re.sub(r'\n\t'+re.escape(BEGIN)+r'.*?'+re.escape(END), '', text, flags=re.S)
    anchor = 'resources_expansion_category = {'
    assert text.count(anchor) == 1
    rule = '\n\t'+BEGIN+'\n\t# IMPERIA CW — Cold War: UAE focus-owned resource investment.\n\tvisible = { NOT = { COLDWAR_UAE_1970_campaign = yes } }\n\t'+END
    return {PATH: text.replace(anchor, anchor+rule, 1)}
