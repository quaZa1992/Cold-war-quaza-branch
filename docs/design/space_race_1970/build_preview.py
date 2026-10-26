# IMPERIA CW — Cold War: assemble the self-contained Space Race design preview.
from pathlib import Path
import base64
import re
import json
from PIL import Image

SOURCE = Path(__file__).resolve().parent
OUTPUT = Path('C:/Users/Enes/.codex/visualizations/2026/10/20/01a15b45-9d1a-70e0-bfe5-9e3ecc289124')
OUTPUT.mkdir(parents=True, exist_ok=True)
art = base64.b64encode((SOURCE / 'assets/earth-moon-map-v1.jpg').read_bytes()).decode('ascii')
base_template = (SOURCE / 'space-race-map.template.html').read_text(encoding='utf-8')
base_styles = re.search(r'<style>(.*?)</style>', base_template, flags=re.S).group(1)
fragment = (SOURCE / 'space-race-expanded.template.html').read_text(encoding='utf-8')
fragment = fragment.replace('%%BASE_STYLES%%', base_styles)
fragment = fragment.replace('%%COMMAND_STYLE%%', (SOURCE / 'space-race-command-v3.css').read_text(encoding='utf-8'))
fragment = fragment.replace('%%CATALOGUE_SCRIPT%%', (SOURCE / 'space-race-catalogue-v2.js').read_text(encoding='utf-8'))
fragment = fragment.replace('%%ENGINE_SCRIPT%%', (SOURCE / 'space-race-engine-v2.js').read_text(encoding='utf-8'))
# IMPERIA CW — Cold War: embed small derivatives, preserving all archive originals and AI edits.
news_sources = json.loads((SOURCE / 'assets/news-sources.json').read_text(encoding='utf-8'))
image_inputs = {'mars': 'viking-first-surface-colourised-v1.png',
                'mission-control': 'apollo13-mission-control-colourised-v1.png',
                'station': 'skylab-original.jpg',
                'us-mars-landing': 'us-mars-landing-user-v1.png',
                'soviet-lunar-landing': 'soviet-lunar-landing-user-v1.png',
                'soviet-mars-landing': 'soviet-mars-landing-user-v1.png',
                'french-lunar-landing': 'french-lunar-landing-user-v1.png'}
news_media = {}
for item in news_sources['images']:
    image_id = item['id']
    preview_file = SOURCE / 'assets' / ('news-' + image_id + '-v1.jpg')
    with Image.open(SOURCE / 'assets' / image_inputs[image_id]) as picture:
        picture = picture.convert('RGB')
        picture.thumbnail((640, 420))
        picture.save(preview_file, quality=72, optimize=True)
    # Credits and provenance stay in news-sources.json, outside the player-facing event.
    news_media[image_id] = {}
    news_media[image_id]['src'] = 'data:image/jpeg;base64,' + base64.b64encode(preview_file.read_bytes()).decode('ascii')
fragment = fragment.replace('%%NEWS_MEDIA_SCRIPT%%', 'globalThis.SpaceRaceNewsMedia=' + json.dumps(news_media, ensure_ascii=False) + ';')
fragment = fragment.replace('font-size:10px', 'font-size:11px').replace('font-size:9px', 'font-size:11px').replace('%%SPACE_MAP_DATA%%', 'data:image/jpeg;base64,' + art)
if re.search(r'%%[A-Z_]+%%', fragment):
    raise ValueError('Unresolved preview template placeholder')
if len(fragment.encode('utf-8')) >= 1_000_000:
    raise ValueError('Inline preview exceeds 1 MB')
target = OUTPUT / 'space-race-map.html'
target.write_text(fragment, encoding='utf-8')
scripts = re.findall(r'<script>(.*?)</script>', fragment, flags=re.S)
(SOURCE / 'preview-script.check.js').write_text('// IMPERIA CW — Cold War: extracted preview script for syntax verification.\n'+'\n'.join(scripts), encoding='utf-8')
qa = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Space Race design review</title><style>body{margin:0;background:#070d11;padding:24px}main.review{max-width:1440px;margin:0 auto}@media(max-width:800px){body{padding:0}}</style><main class="review">' + fragment + '</main></html>'
(SOURCE / 'preview-review.html').write_text(qa, encoding='utf-8')
print(str(target))
print('Fragment bytes:', target.stat().st_size)
