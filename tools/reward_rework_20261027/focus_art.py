# IMPERIA COLD WAR — Shared Cold War focus artwork for Korea and Japan.
"""Explicit per-focus artwork assignments; existing binary assets are unchanged."""
from functools import lru_cache
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = Path(__file__).with_name('focus_art.json')


@lru_cache(maxsize=1)
def catalogue():
    return json.loads(CATALOGUE.read_text(encoding='utf-8'))


def icon_for(tag, identifier, fallback):
    """Preserve the country's original icon outside the reviewed assignments."""
    if tag == 'JAP' and not identifier.startswith('COLDWAR_JAP_1970_'):
        identifier = 'COLDWAR_JAP_1970_' + identifier
    theme = catalogue()['assignments'].get(identifier)
    return 'GFX_goal_COLDWAR_EASTASIA_' + theme if theme else fallback


def gfx_source():
    data = catalogue()
    lines = ['# IMPERIA COLD WAR — Cold War focus artwork for Korea and Japan.',
             '# Existing artwork and upstream attribution: see IMPERIA_COLD_WAR_NOTICE.md.',
             'spriteTypes = {']
    for theme in sorted(set(data['assignments'].values())):
        texture = data['themes'][theme]
        assert (ROOT / texture).is_file(), texture
        name = 'GFX_goal_COLDWAR_EASTASIA_' + theme
        lines += ['\tspriteType = {', f'\t\tname = "{name}"',
                  f'\t\ttexturefile = "{texture}"', '\t}',
                  '\tspriteType = {', f'\t\tname = "{name}_shine"',
                  f'\t\ttexturefile = "{texture}"',
                  '\t\teffectFile = "gfx/FX/buttonstate.lua"']
        for rotation in (-90, 90):
            lines += ['\t\tanimation = {',
                      f'\t\t\tanimationmaskfile = "{texture}"',
                      '\t\t\tanimationtexturefile = "gfx/interface/goals/shine_overlay.dds"',
                      f'\t\t\tanimationrotation = {rotation}.0',
                      '\t\t\tanimationlooping = no', '\t\t\tanimationtime = 0.75',
                      '\t\t\tanimationdelay = 0', '\t\t\tanimationblendmode = "add"',
                      '\t\t\tanimationtype = "scrolling"',
                      '\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }',
                      '\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 }', '\t\t}']
        lines += ['\t\tlegacy_lazy_load = no', '\t}']
    return '\n'.join(lines + ['}', ''])


if __name__ == '__main__':
    target = ROOT / 'interface/COLDWAR_EASTASIA_1970_focus_icons.gfx'
    target.write_text(gfx_source(), encoding='utf-8')
