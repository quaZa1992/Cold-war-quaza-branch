# IMPERIA CW — Cold War: Japan focus sprite reference audit.
from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
tree = (root / 'tools/japan_1970/staging/graph/focus_tree.txt').read_text(encoding='utf-8')
used = set(re.findall(r'(?m)^\s*icon = (\w+)', tree))
available = set()
for path in (root / 'interface').glob('*.gfx'):
    data = path.read_text(encoding='utf-8-sig', errors='replace')
    available.update(re.findall(r'(?im)^\s*name\s*=\s*"([^"\n]+)"', data))
missing = sorted(used - available)
print(f'{len(used)} distinct focus sprites; {len(missing)} not declared in mod interface')
for icon in missing:
    print('REVIEW:', icon)
