# IMPERIA CW — Cold War: Export Imagegen masters and register category-matched selector badges.
from pathlib import Path
import argparse
import hashlib
import json
import re
import struct
import subprocess

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TEXTURES = ROOT / 'gfx/interface/ideas/COLDWAR_selector'
GFX = ROOT / 'interface/COLDWAR_IMPERIA_selector_icons.gfx'
MARKER = '# IMPERIA CW — Cold War: Generated badge matching this selector category.'


def entries(text):
    """Return named blocks at the idea-entry depth, ignoring comments and strings."""
    tokens = list(re.finditer(r'#[^\n]*|"(?:\\.|[^"\\])*"|[\w.]+|[{}=]', text))
    depth = 0
    stack = []
    for i, token in enumerate(tokens):
        value = token.group()
        if value == '{':
            name = tokens[i - 2].group() if i >= 2 and tokens[i - 1].group() == '=' else ''
            stack.append((name, token.end(), depth))
            depth += 1
        elif value == '}':
            depth -= 1
            name, start, level = stack.pop()
            if level == 2:
                yield name, start, token.start()


def write_if_changed(path, payload):
    if not path.exists() or path.read_bytes() != payload:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)


def register(assets):
    wanted = {a['id']: a for a in assets}
    located = set()
    for path in (ROOT / 'common/ideas').glob('*.txt'):
        text = path.read_text(encoding='utf-8-sig')
        edits = []
        for name, start, end in entries(text):
            if name not in wanted:
                continue
            assert name not in located, f'Duplicate idea {name}'
            located.add(name)
            block = text[start:end]
            picture = re.search(r'(?m)^([ \t]*)picture\s*=\s*\w+[^\S\n]*$', block)
            assert picture, name
            indent = picture.group(1)
            replacement = f'{indent}picture = {wanted[name]["picture"]}'
            if MARKER not in block[:picture.start()]:
                replacement = f'{indent}{MARKER}\n{replacement}'
            edits.append((start + picture.start(), start + picture.end(), replacement))
        # Keep the temporary country backlash spirit on the same recruitment artwork.
        if path.name == 'mdcw_guest_workers_ideas.txt':
            old = 'picture = mdcw_gw_recruitment'
            for match in re.finditer(re.escape(old) + r'\b', text):
                if not any(left <= match.start() < right for left, right, _ in edits):
                    edits.append((match.start(), match.end(), 'picture = ' + wanted['mdcw_ni_guest_worker_recruitment_programme']['picture']))
        for left, right, replacement in sorted(edits, reverse=True):
            text = text[:left] + replacement + text[right:]
        if edits:
            text = text.replace(MARKER + '\n\n', MARKER + '\n')
            write_if_changed(path, text.encode('utf-8'))
    assert located == set(wanted), sorted(set(wanted) - located)
    dynamic_path = ROOT / 'common/dynamic_modifiers/mdcw_guest_workers_dynamic_modifiers.txt'
    dynamic = dynamic_path.read_text(encoding='utf-8-sig')
    for old, idea in [('mdcw_gw_recruitment', 'mdcw_ni_guest_worker_recruitment_programme'),
                      ('mdcw_gw_overseas_employment', 'mdcw_ni_overseas_employment_programme')]:
        dynamic = re.sub(r'(?m)^([ \t]*)icon = GFX_idea_' + old + r'\b',
                         lambda m: m[1] + MARKER + '\n' + m[1] + 'icon = GFX_idea_' + wanted[idea]['picture'], dynamic)
    write_if_changed(dynamic_path, dynamic.encode('utf-8'))
    gfx = '# IMPERIA CW — Cold War: Imagegen badges for additional Imperia selector policies.\nspriteTypes = {\n'
    for asset in assets:
        gfx += ('\tspriteType = {\n'
                f'\t\tname = "GFX_idea_{asset["picture"]}"\n'
                f'\t\ttexturefile = "gfx/interface/ideas/COLDWAR_selector/{asset["id"]}.dds"\n'
                '\t}\n')
    write_if_changed(GFX, (gfx + '}\n').encode('utf-8'))


def export(asset):
    source = HERE / 'masters' / (asset['id'] + '.png')
    output = TEXTURES / (asset['id'] + '.png')
    TEXTURES.mkdir(parents=True, exist_ok=True)
    # Generated art is only resized and format-converted. Premultiplied filtering
    # prevents hidden RGB pixels from producing a grey fringe on the alpha edge.
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
                    '-vf', 'format=gbrap,premultiply=inplace=1,scale=64:64:flags=lanczos,unpremultiply=inplace=1,format=rgba',
                    '-frames:v', '1', str(output)], check=True)
    with Image.open(output) as decoded:
        im = decoded.convert('RGBA')
        assert im.size == (64, 64)
        assert im.getchannel('A').getextrema() == (0, 255), asset['id']
        for corner in [(0, 0), (63, 0), (0, 63), (63, 63)]:
            assert im.getpixel(corner)[3] == 0, (asset['id'], 'opaque corner')
        pixels = im.tobytes()
    header = [124, 4111, 64, 64, 256, 0, 0] + [0] * 11 + [32, 65, 0, 32, 255, 65280, 16711680, 4278190080, 4096, 0, 0, 0, 0]
    dds = output.with_suffix('.dds')
    write_if_changed(dds, b'DDS ' + struct.pack('<31I', *header) + pixels)
    assert Image.open(dds).convert('RGBA').tobytes() == pixels
    return dict(id=asset['id'], category=asset['category'], color=asset['color'],
                master=str(source.relative_to(ROOT)), texture=str(dds.relative_to(ROOT)),
                source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                dds_sha256=hashlib.sha256(dds.read_bytes()).hexdigest(),
                size=[64, 64], format='RGBA32 DDS', alpha_preserved=True)


def preview(assets):
    font_path = Path('C:/Windows/Fonts/arial.ttf')
    font = ImageFont.truetype(str(font_path), 13)
    title = ImageFont.truetype(str(font_path), 19)
    rows = sum((sum(a['category'] == c for a in assets) + 5) // 6 for c in (1, 2, 3))
    sheet = Image.new('RGB', (1104, rows * 124 + 140), (35, 38, 34))
    draw = ImageDraw.Draw(sheet)
    y = 12
    for category, label in [(1, 'POLITICAL INSTITUTIONS'), (2, 'ECONOMIC POLICY'), (3, 'MILITARY POLICY')]:
        draw.text((16, y), label, font=title, fill=(230, 225, 208))
        y += 30
        group = [a for a in assets if a['category'] == category]
        for i, asset in enumerate(group):
            x = (i % 6) * 184
            top = y + (i // 6) * 124
            im = Image.open(TEXTURES / (asset['id'] + '.png')).convert('RGBA')
            sheet.paste(im, (x + 14, top + 10), im)
            # Enlarged companion exposes edge quality; the left badge is native size.
            large = im.resize((86, 86), Image.Resampling.NEAREST)
            sheet.paste(large, (x + 86, top), large)
            words = asset['label'].split()
            lines = ['']
            for word in words:
                if len(lines[-1] + word) > 23:
                    lines.append('')
                lines[-1] += (' ' if lines[-1] else '') + word
            draw.multiline_text((x + 7, top + 89), '\n'.join(lines), font=font, fill=(233, 231, 221), spacing=1)
        y += ((len(group) + 5) // 6) * 124 + 10
    sheet.save(HERE / 'preview.png')
    overview = Image.new('RGB', (1024, 600), (35, 38, 34))
    draw = ImageDraw.Draw(overview)
    font = ImageFont.truetype(str(font_path), 12)
    title = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 17)
    y = 12
    for category, label in [(1, 'POLITICAL INSTITUTIONS'), (2, 'ECONOMIC POLICY'), (3, 'MILITARY POLICY')]:
        draw.text((16, y), label, font=title, fill=(235, 230, 212))
        y += 28
        group = [a for a in assets if a['category'] == category]
        for i, asset in enumerate(group):
            x = i % 8 * 128
            top = y + i // 8 * 112
            im = Image.open(TEXTURES / (asset['id'] + '.png')).convert('RGBA')
            overview.paste(im, (x + 32, top), im)
            lines = ['']
            for word in asset['label'].split():
                if len(lines[-1] + word) > 19:
                    lines.append('')
                lines[-1] += (' ' if lines[-1] else '') + word
            for j, line in enumerate(lines):
                length = draw.textlength(line, font=font)
                draw.text((x + (128 - length) / 2, top + 69 + j * 14), line,
                          font=font, fill=(231, 230, 221))
        y += ((len(group) + 7) // 8) * 112 + 12
    overview.save(HERE / 'overview.png')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--register-only', action='store_true')
    args = parser.parse_args()
    assets = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))['assets']
    register(assets)
    if args.register_only:
        print(f'Registered {len(assets)} policy badges.')
        return
    report = [export(asset) for asset in assets]
    preview(assets)
    (HERE / 'validation.json').write_text(json.dumps(dict(comment='IMPERIA CW — Cold War: Built-in Imagegen asset export.',
        engine_tested=False, assets=report), indent=2) + '\n', encoding='utf-8')
    print(f'Exported and verified {len(report)} native 64x64 RGBA32 DDS badges.')


if __name__ == '__main__':
    main()
