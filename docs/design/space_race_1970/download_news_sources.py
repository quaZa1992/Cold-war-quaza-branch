# IMPERIA CW — Cold War: retrieve explicitly selected NASA archive images for editing.
from pathlib import Path
import json
from urllib.request import Request, urlopen

assets = Path(__file__).resolve().parent / 'assets'
sources = json.loads((assets / 'news-sources.json').read_text(encoding='utf-8'))
for item in sources['images']:
    target = assets / item['sourceFile']
    if not target.exists() and item['downloadUrl']:
        request = Request(item['downloadUrl'], headers={'User-Agent': 'SpaceRaceDesignPreview/1.0'})
        with urlopen(request, timeout=30) as response:
            data = response.read(15_000_000)
        if not data.startswith(b'\xff\xd8'):
            raise ValueError('Expected a JPEG from the selected NASA URL')
        target.write_bytes(data)
    print(target.name, target.stat().st_size)
