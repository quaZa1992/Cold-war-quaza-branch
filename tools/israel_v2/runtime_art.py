# IMPERIA COLD WAR — Israel 2.2 native focus-art packaging.
"""Package existing artwork without repainting it or writing loaded files.

``build(data)`` resolves the original registered textures, crops transparent
padding, proportionally fits each motif and returns native DDS/GFX outputs.
It preserves the catalogue and all source artwork. The caller emits the files.
"""
import base64
import hashlib
import io
import json
from pathlib import Path
import re
import struct

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
CANVAS = (112, 72)
PADDING = 2
MARKER = '# IMPERIA COLD WAR — Israel 2.2 normalized native focus artwork.'
_TOKENS = re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}=]|[^\s{}=#"]+')


def _sha(content):
    return hashlib.sha256(content).hexdigest()


def _parse_gfx(text):
    """Read complete GFX scopes rather than regex-pairing adjacent sprites."""
    tokens = [match[0] for match in _TOKENS.finditer(text)
              if not match[0].startswith('#')]
    cursor = 0

    def scope(nested=False):
        nonlocal cursor
        result = []
        while cursor < len(tokens):
            key = tokens[cursor]
            cursor += 1
            if key == '}':
                assert nested, 'Unexpected GFX closing brace'
                return result
            if cursor >= len(tokens) or tokens[cursor] != '=':
                continue
            cursor += 1
            assert cursor < len(tokens), 'Missing GFX value'
            value = tokens[cursor]
            cursor += 1
            if value == '{':
                value = scope(True)
            elif value.startswith('"'):
                value = value[1:-1]
            result.append((key, value))
        assert not nested, 'Unclosed GFX scope'
        return result

    return scope()


def _sprite_blocks(scope):
    for key, value in scope:
        if isinstance(value, list):
            if key.lower() == 'spritetype':
                yield value
            else:
                yield from _sprite_blocks(value)


def _sources(root, wanted):
    found = {name: [] for name in wanted}
    # The existing focus registrations are root-level interface GFX files, as
    # are the other native donor registrations. No asset junction is walked.
    for path in sorted((root / 'interface').glob('*.gfx')):
        raw = path.read_bytes()
        text = raw.decode('utf-8-sig')
        if not any(name in text for name in wanted):
            continue
        for block in _sprite_blocks(_parse_gfx(text)):
            fields = {key.lower(): value for key, value in block
                      if not isinstance(value, list)}
            name = fields.get('name')
            if name in found:
                assert 'texturefile' in fields, ('Sprite has no direct texture', name, path)
                found[name].append({
                    'registration_file': path.relative_to(root).as_posix(),
                    'registration_sha256': _sha(raw),
                    'texture_file': fields['texturefile'].replace('\\', '/'),
                })
    for name, sources in found.items():
        assert sources, ('Missing native sprite registration', name)
        textures = {source['texture_file'].lower() for source in sources}
        assert len(textures) == 1, ('Ambiguous sprite texture registrations', name, sources)
    return found


def _normalize(source):
    rgba = source.convert('RGBA')
    original_bounds = rgba.getchannel('A').getbbox()
    assert original_bounds, 'Source motif is completely transparent'
    cropped = rgba.crop(original_bounds)
    available = (CANVAS[0] - PADDING * 2, CANVAS[1] - PADDING * 2)
    scale = min(available[0] / cropped.width, available[1] / cropped.height, 1.0)
    target = (max(1, round(cropped.width * scale)),
              max(1, round(cropped.height * scale)))
    if target != cropped.size:
        cropped = cropped.resize(target, Image.Resampling.LANCZOS)
    offset = ((CANVAS[0] - target[0]) // 2, (CANVAS[1] - target[1]) // 2)
    normalized = Image.new('RGBA', CANVAS, (0, 0, 0, 0))
    normalized.paste(cropped, offset)
    alpha = normalized.getchannel('A')
    bounds = alpha.getbbox()
    assert bounds and bounds[0] >= PADDING and bounds[1] >= PADDING
    assert bounds[2] <= CANVAS[0] - PADDING and bounds[3] <= CANVAS[1] - PADDING
    assert alpha.crop((0, 0, CANVAS[0], PADDING)).getbbox() is None
    assert alpha.crop((0, CANVAS[1] - PADDING, CANVAS[0], CANVAS[1])).getbbox() is None
    assert alpha.crop((0, 0, PADDING, CANVAS[1])).getbbox() is None
    assert alpha.crop((CANVAS[0] - PADDING, 0, CANVAS[0], CANVAS[1])).getbbox() is None
    return normalized, {
        'source_size': list(rgba.size),
        'source_alpha_bounds': list(original_bounds),
        'source_decoded_rgba_sha256': _sha(rgba.tobytes()),
        'cropped_size': list(rgba.crop(original_bounds).size),
        'resized_size': list(target),
        'scale': scale,
        'offset': list(offset),
        'canvas_size': list(CANVAS),
        'output_alpha_bounds': list(bounds),
        'transparent_border_pixels': PADDING,
        'upscaling': False,
        'resampling': 'Pillow LANCZOS, proportional fit without repainting',
    }


def _dds(image):
    stream = io.BytesIO()
    image.save(stream, format='DDS')
    content = stream.getvalue()
    assert content[:4] == b'DDS ', 'Incorrect DDS magic'
    assert struct.unpack_from('<I', content, 4)[0] == 124, 'Incorrect DDS header'
    assert struct.unpack_from('<2I', content, 12) == (CANVAS[1], CANVAS[0])
    pixel = struct.unpack_from('<8I', content, 76)
    assert pixel == (32, 65, 0, 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000), ('DDS must use native uncompressed RGBA8 masks', pixel)
    assert len(content) == 128 + CANVAS[0] * CANVAS[1] * 4
    with Image.open(io.BytesIO(content)) as decoded:
        assert decoded.size == CANVAS and decoded.convert('RGBA').tobytes() == image.tobytes(), 'DDS pixel roundtrip differs'
    return content


def _registration(sprite, texture):
    rows = ['\tspriteType = {', f'\t\tname = "{sprite}"',
            f'\t\ttexturefile = "{texture}"', '\t}', '\tspriteType = {',
            f'\t\tname = "{sprite}_shine"', f'\t\ttexturefile = "{texture}"',
            '\t\teffectFile = "gfx/FX/buttonstate.lua"']
    # Native MD's shader alias and the existing two opposing shine animations.
    for rotation in (-90, 90):
        rows += ['\t\tanimation = {', f'\t\t\tanimationmaskfile = "{texture}"',
                 '\t\t\tanimationtexturefile = "gfx/interface/goals/shine_overlay.dds"',
                 f'\t\t\tanimationrotation = {rotation}.0',
                 '\t\t\tanimationlooping = no', '\t\t\tanimationtime = 0.75',
                 '\t\t\tanimationdelay = 0', '\t\t\tanimationblendmode = "add"',
                 '\t\t\tanimationtype = "scrolling"',
                 '\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }',
                 '\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 }', '\t\t}']
    return rows + ['\t\tlegacy_lazy_load = no', '\t}']


def build(data, root=ROOT):
    """Return native files and mappings while preserving all input/source data.

    ``root`` is injectable for isolated tests. Reading original registrations
    and textures is required; this function never creates or changes a file.
    """
    root = Path(root)
    before = json.dumps(data, sort_keys=True, separators=(',', ':'))
    wanted = sorted({node['icon'] for node in data['nodes']})
    sources = _sources(root, wanted)
    files, sprite_map, preview_icons, records = {}, {}, {}, []
    gfx = [MARKER, '# Existing artwork: crop, proportional scale and transparent padding only.',
           'spriteTypes = {']
    used_names = set()
    for original in wanted:
        source = sources[original][0]
        path = root / source['texture_file']
        raw = path.read_bytes()
        with Image.open(io.BytesIO(raw)) as image:
            normalized, details = _normalize(image)
        stem = original.removeprefix('GFX_ISR70_focus_')
        assert re.fullmatch(r'[A-Za-z0-9_]+', stem), ('Unsafe native sprite stem', original)
        sprite = 'GFX_ISR2_focus_' + stem
        assert sprite not in used_names, ('Duplicate normalized sprite', sprite)
        used_names.add(sprite)
        texture = f'gfx/interface/goals/ISR2/{stem}.dds'
        native = _dds(normalized)
        files[texture] = native
        sprite_map[original] = sprite
        gfx += _registration(sprite, texture)
        png = io.BytesIO()
        normalized.save(png, format='PNG', optimize=True)
        preview_icons[sprite] = 'data:image/png;base64,' + base64.b64encode(png.getvalue()).decode('ascii')
        record = {
            'project': 'IMPERIA COLD WAR',
            'feature': 'Israel 2.2 normalized native focus artwork',
            'original_sprite': original,
            'source_registrations': sources[original],
            'source_texture': source['texture_file'],
            'source_file_sha256': _sha(raw),
            'original_author': 'Unknown individual artist in the inherited source records',
            'source_credit': 'Existing Millennium Dawn / Imperia / Cold War project asset; retain upstream attribution',
            'licence_or_permission': 'Unknown separate asset licence or redistribution permission; inherited source rights remain applicable',
            'notice': 'IMPERIA_COLD_WAR_NOTICE.md',
            'modifications': 'Transparent alpha crop, proportional downscale where needed, transparent padding and native DDS encoding. No motif repainted.',
            'normalization': details,
            'output_sprite': sprite,
            'output_shine_sprite': sprite + '_shine',
            'output_texture': texture,
            'output_dds_sha256': _sha(native),
            'output_decoded_rgba_sha256': _sha(normalized.tobytes()),
            'dds': {'format': 'Uncompressed RGBA8', 'channel_storage': 'BGRA bytes with explicit RGBA masks',
                    'alpha': 'Straight alpha, transparent border', 'size': list(CANVAS),
                    'pixel_roundtrip_equal': True},
        }
        records.append(record)
        files[texture.removesuffix('.dds') + '.provenance.json'] = json.dumps(record, indent=2) + '\n'
    gfx += ['}']
    files['interface/ISR2_focus.gfx'] = '\n'.join(gfx) + '\n'
    files['gfx/interface/goals/ISR2/NOTICE.md'] = (
        '# IMPERIA COLD WAR: Israel 2.2 native focus artwork packaging\n\n'
        'These are technical copies of existing registered focus artwork. Each DDS has a companion '
        '`.provenance.json` recording its exact source registration, source file and pixel hashes, '
        'dimensions, alpha bounds, crop, proportional downscale, padding and output hashes. '
        'No source image is overwritten and no motif is repainted.\n\n'
        'Original individual artists and separate asset licences or redistribution permissions are '
        'unknown where the inherited source records do not identify them. Existing Millennium Dawn, '
        'Imperia, Cold War and applicable native asset credits and rights remain separate. '
        'See the root `IMPERIA_COLD_WAR_NOTICE.md`. Project identification establishes no new rights.\n\n'
        'The GFX packaging follows the existing Israel focus-art generator and native MD shine '
        'pattern, including its `gfx/FX/buttonstate.lua` native shader alias. The two opposing '
        'shine animations reuse `gfx/interface/goals/shine_overlay.dds`. Runtime rendering and '
        'shine behaviour still require an engine check.\n')
    assert json.dumps(data, sort_keys=True, separators=(',', ':')) == before, 'Art packaging mutated the catalogue'
    return {
        'files': files, 'sprite_map': sprite_map, 'preview_icons': preview_icons,
        'metadata': {
            'project': 'IMPERIA COLD WAR', 'motifs': len(wanted), 'canvas_size': list(CANVAS),
            'transparent_border_pixels': PADDING, 'records': records,
            'source_images_overwritten': False, 'catalogue_mutated': False,
            'native_rgba_roundtrip_checked': True, 'native_engine_tested': False,
        },
    }
