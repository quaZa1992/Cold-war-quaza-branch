# IMPERIA COLD WAR — previews generated from the production event localisation.
from pathlib import Path
import html
import json
import re
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'gfx/event_pictures/coldwar_nuclear_intelligence'
OUT = ROOT / 'docs/nuclear_intelligence/preview'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    source = (ROOT / 'localisation/english/COLDWAR_nuclear_intelligence_l_english.yml').read_text(encoding='utf-8-sig')
    loc = {m.group(1): json.loads(m.group(2)) for m in re.finditer(r'^ ([\w.]+): (".*")$', source, re.M)}
    for name, filename in [('enrichment', 'COLDWAR_NI_enrichment_color.dds'), ('weapons', 'COLDWAR_NI_weapons_color.dds')]:
        Image.open(ART / filename).convert('RGBA').save(OUT / (name + '.png'))
    def font(size, bold=False):
        return ImageFont.truetype('C:/Windows/Fonts/' + ('georgiab.ttf' if bold else 'georgia.ttf'), size)
    canvas = Image.new('RGB', (1600, 1820), '#171e22')
    draw = ImageDraw.Draw(canvas)
    def wrap(text, ft, width):
        lines = []
        for paragraph in text.split('\n'):
            if not paragraph:
                lines.append('')
                continue
            line = ''
            for word in paragraph.split():
                trial = (line + ' ' + word).strip()
                if draw.textlength(trial, font=ft) > width and line:
                    lines.append(line)
                    line = word
                else:
                    line = trial
            lines.append(line)
        return lines
    draw.text((44, 26), 'IMPERIA COLD WAR — NUCLEAR INTELLIGENCE', font=font(30, True), fill='#e6d5b0')
    draw.text((44, 76), 'English game text • example target: Iran • layout preview, not an in-game screenshot', font=font(17), fill='#b5bec1')
    cards = []
    for i in range(1, 5):
        x = 36 + ((i - 1) % 2) * 785
        y = 122 + ((i - 1) // 2) * 838
        w, h = 743, 804
        draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill='#293137', outline='#7c725d', width=2)
        title = loc[f'COLDWAR_NI.{i}.t'].replace('[From.GetName]', 'Iran')
        body = loc[f'COLDWAR_NI.{i}.d'].replace('[From.GetName]', 'Iran')
        option = loc[f'COLDWAR_NI.{i}.a']
        draw.text((x + 24, y + 22), f'COLDWAR_NI.{i}', font=font(15), fill='#a6b0b3')
        ty = y + 52
        for line in wrap(title, font(25, True), w - 48):
            draw.text((x + 24, ty), line, font=font(25, True), fill='#ede0c4')
            ty += 32
        category = 'enrichment' if i < 3 else 'weapons'
        picture = Image.open(OUT / (category + '.png')).convert('RGBA')
        picture = picture.resize((picture.width * 2, picture.height * 2), Image.Resampling.LANCZOS)
        canvas.paste(picture, (x + int((w - picture.width) / 2), y + 130), picture)
        lines = wrap(body, font(18), w - 52)
        step = min(24, int((h - 92 - 502) / max(1, len(lines))))
        if step < 20:
            raise ValueError(f'Event {i} body needs a larger card')
        ty = y + 502
        for line in lines:
            draw.text((x + 26, ty), line, font=font(18), fill='#d8dcda')
            ty += step
        draw.rounded_rectangle((x + 22, y + h - 66, x + w - 22, y + h - 22), radius=3, fill='#424c50', outline='#a18e65')
        tw = draw.textlength(option, font=font(18))
        draw.text((x + (w - tw) / 2, y + h - 54), option, font=font(18), fill='#eee1c5')
        cards.append(f'<article><small>COLDWAR_NI.{i}</small><h2>{html.escape(title)}</h2><img src="{category}.png" alt="Historical {category} photograph"><p>{html.escape(body).replace(chr(10), "<br>")}</p><footer>{html.escape(option)}</footer></article>')
    canvas.save(OUT / 'events.png')
    style = 'body{background:#171e22;color:#d8dcda;font:18px Georgia,serif;margin:30px}header{max-width:1100px;margin:auto}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:24px;max-width:1300px;margin:25px auto}article{background:#293137;border:1px solid #7c725d;padding:24px;border-radius:6px}h1,h2{color:#ede0c4}small{color:#a6b0b3}img{display:block;width:auto;height:176px;margin:24px auto}p{line-height:1.5;min-height:300px}footer{border:1px solid #a18e65;padding:15px;text-align:center;background:#424c50}'
    (OUT / 'events.html').write_text(f'<!doctype html><!-- IMPERIA COLD WAR — nuclear intelligence event previews --><html lang="en"><meta charset="utf-8"><title>IMPERIA COLD WAR — Nuclear intelligence event previews</title><style>{style}</style><header><h1>IMPERIA COLD WAR — Nuclear intelligence</h1><p>English localisation preview; example target: Iran. This is a layout preview, not an in-game screenshot.</p></header><main>' + ''.join(cards) + '</main></html>', encoding='utf-8')
    print(OUT / 'events.png')


if __name__ == '__main__':
    main()
