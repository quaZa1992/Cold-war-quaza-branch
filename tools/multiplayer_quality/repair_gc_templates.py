# IMPERIA COLD WAR — Emit native concrete Security Council seat effects.
"""Expand the existing seat templates without changing the current seat roster."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/historical_politics_1970'))
from dispatch import _find_block_end


def main():
    path = ROOT / 'common/scripted_effects/COLDWAR_gc_unsc.txt'
    source = path.read_text(encoding='utf-8')
    seats = list(dict.fromkeys(re.findall(r'COLDWAR_gc_un_append_seat = \{ seat = ([a-z_]+) \}', source)))
    assert seats, 'No current seat roster'
    for name in ['append_seat', 'assign', 'clear']:
        key = 'COLDWAR_gc_un_' + name
        match = re.search(r'(?m)^' + key + r' = \{', source)
        assert match, key
        opening = source.find('{', match.start(), match.end())
        end = _find_block_end(source, opening)
        template = source[match.start():end]
        concrete = '\n\n'.join(template.replace(key + ' = {', key + '_' + seat + ' = {', 1).replace('$seat$', seat)
                               for seat in seats)
        source = source[:match.start()] + concrete + source[end:]
    source = re.sub(r'(COLDWAR_gc_un_(?:append_seat|assign|clear)) = \{ seat = ([a-z_]+) \}', r'\1_\2 = yes', source)
    path.write_text(source, encoding='utf-8', newline='\n')
    decisions = ROOT / 'common/decisions/COLDWAR_gc_unsc.txt'
    text = decisions.read_text(encoding='utf-8')
    text = re.sub(r'(COLDWAR_gc_un_(?:assign|clear)) = \{ seat = ([a-z_]+) \}', r'\1_\2 = yes', text)
    decisions.write_text(text, encoding='utf-8', newline='\n')
    print('Expanded native effects for', len(seats), 'current seats', flush=True)


if __name__ == '__main__':
    main()
