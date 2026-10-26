# IMPERIA CW — Cold War: event art — audit event pictures.
"""Audit visible Cold War events against actual registered picture assets.

Reads game data only; writes the review inventory and contact sheets under docs.
Dimension findings are technical facts. Keyword/theme findings require visual review.
"""
from pathlib import Path
import csv
import importlib.util
import json
import html
import re
from collections import Counter, defaultdict
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
MD = Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
OUT = ROOT / 'docs/event_art_review'
spec = importlib.util.spec_from_file_location('guest_worker_parser', ROOT/'tools/guest_workers/validate.py')
V = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = V
spec.loader.exec_module(V)


def clean(value):
    return value.strip('"') if isinstance(value, str) else ''


def write_review(summary, records):
    """Readable review; thumbnails never replace or modify runtime game assets."""
    findings = json.loads((ROOT/'tools/event_art/visual_review.json').read_text(encoding='utf-8'))
    grouped = defaultdict(list)
    for r in records:
        grouped[r['picture']].append(r)
    thumbs = OUT/'review_thumbnails'
    thumbs.mkdir(exist_ok=True)
    cards = []
    for finding in findings:
        rows = grouped.get(finding['picture'], [])
        if not rows:
            continue
        name = finding['picture'].removeprefix('GFX_')+'.png'
        image_html = '<div class="missing">No registered image</div>'
        if rows[0]['asset_path']:
            with Image.open(rows[0]['asset_path']) as im:
                im = im.convert('RGBA')
                im.thumbnail((217,163), Image.Resampling.LANCZOS)
                im.save(thumbs/name)
            image_html = f'<img src="review_thumbnails/{html.escape(name)}" alt="Current asset">'
        examples = ''.join(f'<li><code>{html.escape(r["event_id"])}</code> — {html.escape(r["title"])}</li>' for r in rows[:5])
        cards.append(f'<article class="card" data-search="{html.escape(finding["picture"]+" "+finding["reason"])}">'
                     f'<div class="thumb">{image_html}</div><div><span class="tag">{html.escape(finding["priority"])}</span>'
                     f'<h3>{html.escape(finding["picture"])}</h3><p>{html.escape(finding["reason"])}</p>'
                     f'<p><b>Recommended work:</b> {html.escape(finding["replacement"])}</p>'
                     f'<details><summary>{len(rows)} event definitions · {html.escape(rows[0]["dimensions"] or "no asset")}</summary><ul>{examples}</ul></details></div></article>')
    missing = Counter(r['file'] for r in records if 'missing_picture' in r['issues'])
    missing_rows = ''.join(f'<tr><td>{html.escape(k)}</td><td>{v}</td></tr>' for k,v in missing.most_common())
    issues = ''.join(f'<tr><td>{html.escape(k.replace("_"," "))}</td><td>{v}</td></tr>' for k,v in summary['issue_counts_by_event'].items())
    prompt = (ROOT/'tools/event_art/politburo_prompt.txt').read_text(encoding='utf-8')
    output = '''<!doctype html><html lang="en"><meta charset="utf-8"><title>Cold War event art review</title>
<meta name="viewport" content="width=device-width, initial-scale=1"><style>
body{margin:0;background:#161b20;color:#e5e8eb;font:16px/1.55 Segoe UI,Arial,sans-serif}main{max-width:1140px;margin:auto;padding:36px 24px 70px}h1{margin:0;font-size:34px}h2{margin-top:42px;color:#e8c58b}h3{font-size:16px;overflow-wrap:anywhere;margin:6px 0}p{max-width:940px}a{color:#91cef5}.muted{color:#a9b3bd}.panel,.card{background:#222b33;border:1px solid #3d4c58;border-radius:8px;padding:20px;margin:16px 0}.panel{display:flex;gap:28px;align-items:center}.panel img{width:217px;height:163px}.card{display:grid;grid-template-columns:230px 1fr;gap:22px}.thumb{min-height:163px;display:flex;align-items:center;justify-content:center;background:#31363b}.thumb img{max-width:217px;max-height:163px}.tag{font:12px monospace;text-transform:uppercase;color:#f2c28a}table{width:100%;border-collapse:collapse;margin:16px 0}td,th{padding:9px 12px;text-align:left;border-bottom:1px solid #3d4c58}code{color:#b9d5e8}details{margin-top:12px}summary{cursor:pointer;color:#b9d5e8}.missing{color:#edb18f}input{box-sizing:border-box;width:100%;padding:12px;background:#222b33;border:1px solid #687884;border-radius:5px;color:white;font:inherit}.sheets{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.sheets img{width:100%;height:auto}pre{white-space:pre-wrap;overflow-wrap:anywhere}@media(max-width:700px){.card{grid-template-columns:1fr}.panel{display:block}.sheets{grid-template-columns:repeat(2,1fr)}}
</style><main><h1>Cold War event art review</h1><p class="muted">19 October 2026 · Inventory and manual visual review · No gameplay changes in this review.</p>
<section class="panel"><img src="../../gfx/event_pictures/coldwar_1970/COLDWAR_SOV_politburo_session.png" alt="Installed Politburo session image"><div><h2 style="margin-top:0">Installed: Politburo session and vote</h2><p>The supplied photograph was restored with built-in ImageGen. It is now a 217 × 163 RGBA DDS with the exact native MD frame. Both <code>COLDWAR_SOV.10</code> and <code>COLDWAR_SOV.11</code> use it. The authoritative Soviet generator includes the sprite and binary.</p><p>The image inset is 180 × 150. Frame pixels match main MD exactly. No white mattes; no news-sized spill under event options.</p></div></section>
'''
    output += f'<h2>Scope and confirmed technical findings</h2><p>{summary["files_scanned"]} custom Cold War event files; {summary["visible_events"]:,} visible event definitions; {summary["hidden_events_excluded"]} hidden events excluded; {summary["unique_pictures"]} distinct picture keys. Many Gulf events are generated combinations, so event counts do not imply the same number of unique illustrations.</p>'
    output += '<p>Only the Politburo replacement above was installed in this artwork task. The findings below remain an explicit art backlog; this report does not claim they have been fixed.</p>'
    output += '<p>Legacy 209/210 × 176 polaroids are valid old HOI4 artwork, but differ from the requested MD frame. Both 397 × 153 and 400 × 150 are accepted native news sizes. Date-review findings require checking the actual event date; they are not automatically confirmed historical errors.</p>'
    output += '<table><tr><th>Finding</th><th>Event definitions</th></tr>'+issues+'</table>'
    output += '<p><a href="inventory.csv">Complete event inventory (CSV)</a> · <a href="inventory.json">Inventory and metadata (JSON)</a> · <a href="politburo_export.json">Installed asset validation</a></p>'
    output += '<h2>Event families with no assigned picture</h2><table><tr><th>File</th><th>Visible definitions</th></tr>'+missing_rows+'</table>'
    output += '<h2>Manually reviewed artwork backlog</h2><p>Each card shows the current art, the reason it needs work, and a concrete replacement brief. An existing photo that only needs packaging is marked separately.</p><input id="search" placeholder="Filter by picture name or finding…" aria-label="Filter artwork findings"><div id="cards">'+''.join(cards)+'</div>'
    output += '<h2>Full visual inventory</h2><p>All distinct current picture keys are shown once. Orange labels identify automatic technical findings. These sheets show existing assets, not replacement proposals.</p><div class="sheets">'+''.join(f'<a href="{p.name}"><img src="{p.name}" alt="Contact sheet {i+1}"></a>' for i,p in enumerate(sorted(OUT.glob('contact_sheet_*.jpg'))))+'</div>'
    output += '<details><summary>Politburo ImageGen prompt and source</summary><p>Tool: built-in <code>image_gen</code>. Source: the user-supplied voting photograph. Native frame: main MD <code>political_deal.dds</code>, outer frame pixels only. Colour restoration was generated; resizing and native frame packaging were exported with FFmpeg.</p><pre>'+html.escape(prompt)+'</pre></details>'
    output += '<p class="muted">The exporter verifies exact native frame pixels, DDS/PNG equality, sprite registration and event bindings. No fresh in-game screenshot or multiplayer test is claimed. The parser skipped one unrelated vanilla power-balance registry; no event picture in this inventory depends on it.</p></main><script>document.getElementById("search").addEventListener("input",e=>{const q=e.target.value.toLowerCase();document.querySelectorAll(".card").forEach(c=>c.hidden=!c.dataset.search.toLowerCase().includes(q));});</script></html>'
    (OUT/'review.html').write_text(output, encoding='utf-8')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sprites = defaultdict(list)
    parse_errors = []
    # Mod files replace same-name upstream files. Base registries remain usable.
    registries = {}
    for base in (GAME, MD, ROOT):
        for p in (base/'interface').glob('*.gfx'):
            registries[p.name] = p
    for p in registries.values():
        try:
            ast = V.parse(p.read_text(encoding='utf-8-sig', errors='replace'))
            for key, _, body in V.walk(ast):
                if key.lower() != 'spritetype' or not isinstance(body, list):
                    continue
                fields = {k.lower(): v for k, _, v in body}
                name, texture = clean(fields.get('name')), clean(fields.get('texturefile'))
                if name and texture:
                    sprites[name].append((texture, str(p)))
        except (AssertionError, IndexError) as exc:
            parse_errors.append({'file': str(p), 'error': str(exc)})
    loc = {}
    for p in (ROOT/'localisation/english').glob('*.yml'):
        for m in re.finditer(r'^\s*([\w.\-]+):(?:\d+)?\s+"(.*)"\s*$', p.read_text(encoding='utf-8-sig', errors='replace'), re.M):
            loc[m[1]] = m[2]
    records, hidden_count, files = [], 0, []
    metadata = {}
    for p in (ROOT/'events').glob('*.txt'):
        if not re.search(r'coldwar|mdcw|1970|1985|imperia', p.name, re.I):
            continue
        files.append(p.name)
        try:
            ast = V.parse(p.read_text(encoding='utf-8-sig'))
        except (AssertionError, IndexError) as exc:
            parse_errors.append({'file': str(p), 'error': str(exc)})
            continue
        for kind, _, body in ast:
            if kind not in ('country_event', 'news_event') or not isinstance(body, list):
                continue
            if V.first(body, 'hidden') == 'yes':
                hidden_count += 1
                continue
            event_id = clean(V.first(body, 'id'))
            pic = clean(V.first(body, 'picture'))
            title = loc.get(clean(V.first(body, 'title')), clean(V.first(body, 'title')))
            definitions = sprites.get(pic, [])
            texture = definitions[-1][0] if definitions else ''
            asset = next((b/texture for b in (ROOT, MD, GAME) if texture and (b/texture).is_file()), None)
            issues = []
            if not pic:
                issues.append('missing_picture')
            elif not definitions:
                issues.append('unregistered_sprite')
            if texture and not asset:
                issues.append('missing_texture')
            if len({t for t, _ in definitions}) > 1:
                issues.append('conflicting_sprite_definitions')
            info = {}
            if asset:
                if str(asset) not in metadata:
                    try:
                        with Image.open(asset) as im:
                            metadata[str(asset)] = {'size': list(im.size), 'mode': im.mode}
                    except Exception as exc:
                        metadata[str(asset)] = {'decode_error': str(exc)}
                info = metadata[str(asset)]
                if 'decode_error' in info:
                    issues.append('unreadable_texture')
                else:
                    w, h = info['size']
                    if kind == 'country_event' and (w, h) != (217, 163):
                        issues.append('country_picture_legacy_polaroid_style' if (w,h) in ((209,176),(210,176))
                                      else 'country_picture_oversized_or_news_asset')
                    if kind == 'news_event' and (w, h) not in ((400, 150),(397,153)):
                        issues.append('news_picture_dimensions_review')
            if re.search(r'biden|trump|zelensk|f35|f-35|covid|coronavirus|brexit|202[0-9]|obama', pic+' '+texture, re.I):
                issues.append('potential_period_mismatch_review')
            records.append({'file': str(p.relative_to(ROOT)), 'event_id': event_id, 'title': title,
                            'event_type': kind, 'picture': pic, 'texture': texture,
                            'asset_path': str(asset) if asset else '',
                            'dimensions': 'x'.join(map(str, info.get('size', []))),
                            'issues': issues})
    counts = Counter(i for r in records for i in r['issues'])
    per_picture = defaultdict(list)
    for r in records:
        per_picture[r['picture']].append(r)
    summary = {'scope': 'Event filenames containing coldwar, mdcw, 1970, 1985 or imperia; hidden events excluded.',
               'files_scanned': len(files), 'visible_events': len(records), 'hidden_events_excluded': hidden_count,
               'unique_pictures': len(per_picture), 'issue_counts_by_event': dict(counts), 'parse_errors': parse_errors,
               'picture_usage': [{'picture': k, 'events': len(v), 'dimensions': v[0]['dimensions'],
                                  'issues': sorted({i for r in v for i in r['issues']}),
                                  'sample_titles': list(dict.fromkeys(r['title'] for r in v))[:5]}
                                 for k, v in sorted(per_picture.items(), key=lambda x: -len(x[1]))]}
    (OUT/'inventory.json').write_text(json.dumps({'summary': summary, 'events': records}, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    with (OUT/'inventory.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows({**r, 'issues': ';'.join(r['issues'])} for r in records)
    # Full visual inventory, with each asset shown once. Native shape remains visible.
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 13)
    ordered = sorted(per_picture.values(), key=lambda v: (not any('SOV' in r['file'] or 'UNI' in r['file'] for r in v), -bool(v[0]['issues']), -len(v)))
    for page_start in range(0, len(ordered), 24):
        canvas = Image.new('RGB', (1200, 6*210), '#26282b')
        draw = ImageDraw.Draw(canvas)
        for index, rows in enumerate(ordered[page_start:page_start+24]):
            r = rows[0]
            x, y = (index % 4)*300, (index//4)*210
            if r['asset_path']:
                try:
                    with Image.open(r['asset_path']) as im:
                        im = im.convert('RGBA'); im.thumbnail((276, 153), Image.Resampling.LANCZOS)
                        canvas.paste(im, (x+(300-im.width)//2, y+2), im)
                except Exception:
                    pass
            lines = [r['picture'].removeprefix('GFX_')[:39], f"{r['dimensions']} | {len(rows)} events", r['title'][:42]]
            for line_i, line in enumerate(lines):
                draw.text((x+6, y+158+line_i*16), line, font=font, fill='#ffb36b' if r['issues'] else '#edf0f1')
        canvas.save(OUT/f'contact_sheet_{page_start//24+1:02}.jpg', quality=92)
    if (ROOT/'tools/event_art/visual_review.json').is_file():
        write_review(summary, records)
    print(json.dumps({k: v for k, v in summary.items() if k != 'picture_usage'}, indent=2))
    print('Contact sheets:', (len(ordered)+23)//24)


if __name__ == '__main__':
    main()
