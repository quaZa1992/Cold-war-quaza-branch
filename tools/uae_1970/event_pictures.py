# IMPERIA CW — Cold War: uae 1970 — event pictures.
"""COLDWAR: narrowly route the user-supplied colourised rulers photograph."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PICTURE = 'GFX_COLDWAR_UAE_rulers_meeting_colour'
TEXTURE = 'gfx/event_pictures/COLDWAR_UAE/COLDWAR_UAE_rulers_colour.dds'
GFX = 'interface/COLDWAR_UAE_1970_eventpictures.gfx'
# Rulers' settlement, federal dispute, executive delegation, cabinet bargain,
# Bahrain/Qatar federal representation and UAE-origin Gulf Charter invitations.
UAE_FAMILIES = {5, 6}


def uae_picture(number, default='GFX_political_deal'):
    return PICTURE if number//1000 in UAE_FAMILIES else default


def gfx_output():
    assert (ROOT/TEXTURE).is_file(), 'Export the colourised DDS before compiling'
    return {GFX: '# IMPERIA CW — Cold War: uae 1970 generated content.\n# COLDWAR | user-supplied rulers photograph, colourised with ImageGen.\nspriteTypes = {\n\tspriteType = {\n\t\tname = "'+PICTURE+'"\n'
            '\t\ttexturefile = "'+TEXTURE+'"\n\t}\n}\n'}


def install():
    """Update only image fields and the dedicated registry, preserving gameplay."""
    outputs = gfx_output()
    counts = {}
    for relative in ['events/COLDWAR_UAE_1970_contracts.txt','events/COLDWAR_GCC_1970.txt']:
        original = (ROOT/relative).read_bytes()
        text = original.decode('utf-8-sig')
        count = 0
        def replace(match):
            nonlocal count
            eid, old = match['id'], match['picture']
            number = int(eid.rsplit('.',1)[1])
            chosen = (uae_picture(number, old) if 'UAE_1970_contracts.' in eid else
                      PICTURE if 6001 <= number <= 6032 else old)
            if chosen == PICTURE:
                count += 1
                assert old in {'GFX_political_deal',PICTURE}, 'Do not overwrite unrelated art'
            return match['prefix']+chosen
        pattern = r'(?ms)(?P<prefix>^country_event = \{\r?\n\s*id = (?P<id>[^\r\n]+).*?^\tpicture = )(?P<picture>[^\r\n]+)'
        outputs[relative] = re.sub(pattern, replace, text)
        without_picture = lambda value: re.sub(r'(?m)^\tpicture = [^\r\n]+', '\tpicture = IMAGE_ONLY', value)
        assert without_picture(outputs[relative]) == without_picture(text), 'Gameplay changed during image routing'
        counts[relative] = count
        assert count == (256 if 'UAE' in relative else 32), counts
    changed = []
    for relative,text in outputs.items():
        path = ROOT/relative
        before = path.read_bytes() if path.exists() else None
        after = text.encode('utf-8')
        if before != after:
            path.write_bytes(after)
            changed.append(relative)
    # Keep the canonical output manifests truthful without rebuilding other
    # modules or touching their ownership in this artwork-only task.
    for manifest_path,event_file in [(HERE/'manifest.json','events/COLDWAR_UAE_1970_contracts.txt'),
                                     (ROOT/'tools/gcc_1970/manifest.json','events/COLDWAR_GCC_1970.txt')]:
        record = json.loads(manifest_path.read_text())
        record['outputs'][event_file] = hashlib.sha256((ROOT/event_file).read_bytes()).hexdigest()
        if manifest_path.parent == HERE:
            record['outputs'][GFX] = hashlib.sha256((ROOT/GFX).read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'changed':changed,'photo_event_instances':counts}))


if __name__ == '__main__':
    install()
