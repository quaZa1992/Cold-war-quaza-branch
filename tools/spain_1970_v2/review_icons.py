# IMPERIA CW — Cold War: audit approved focus-goal icon references.
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MD = Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
DESIGN = ROOT / 'tools' / 'spain_1970_v2' / 'approved_design.json'
SPRITES = {}
for base in (ROOT / 'interface', MD / 'interface', GAME / 'interface'):
    if not base.exists():
        continue
    for path in base.rglob('*.gfx'):
        text = path.read_text(encoding='utf-8-sig', errors='replace')
        names = re.findall(r'\bname\s*=\s*["\']?([^\s"\']+)', text)
        textures = re.findall(r'\btexturefile\s*=\s*["\']([^"\']+)', text)
        for name in names:
            SPRITES.setdefault(name, []).append((path, textures))
icons = sorted({node['icon'] for node in json.loads(DESIGN.read_text(encoding='utf-8'))['nodes']})
missing = {icon: [candidate for candidate in (icon, 'GFX_goal_' + icon, 'GFX_' + icon) if candidate in SPRITES]
           for icon in icons}
missing = [icon for icon, candidates in missing.items() if not candidates]
print(f'Unique approved icons: {len(icons)}; goal sprite definitions found: {len(icons)-len(missing)}; missing: {missing}')
