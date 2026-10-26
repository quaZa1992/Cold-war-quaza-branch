# IMPERIA CW — Cold War: jerusalem landmarks — materials.
"""Original weathered limestone atlas; archival photos are reference only.

Surface detail is baked into the existing 4-by-4 atlas, leaving geometry,
material count, texture dimensions and the native packed channel layout intact.
"""
from pathlib import Path
import importlib.util
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT/'gfx/models/buildings/landmarks'
PREFIX = 'mdcw_jerusalem_western_wall'
CELL = 256
spec = importlib.util.spec_from_file_location('western_wall_dds', ROOT/'tools/warsaw_landmarks/materials.py')
dds = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dds)


def noise(rng, size, amplitude):
    """Correlated luminance only: no independent RGB or rainbow variation."""
    a = rng.uniform(-1, 1, (size, size)).astype(np.float32)
    field = np.asarray(Image.fromarray(a, mode='F').resize((CELL, CELL), Image.Resampling.BICUBIC))
    return field*amplitude


def surface(rng, base, roughness=1.):
    broad = noise(rng, 5, 10) + noise(rng, 14, 5)
    grain = noise(rng, 43, 3.4) + rng.normal(0, 1.25, (CELL, CELL))
    tone = broad + grain*roughness
    # The limestone's grey-cream hue stays stable across all grain scales.
    pixels = np.asarray(base, dtype=np.float32)[None, None, :] + tone[:, :, None]
    height = 128 + noise(rng, 17, 3)*roughness + noise(rng, 58, 2.8)*roughness
    return pixels, height


def pitting(rng, pixels, height, strength=1., count=220):
    """Fine pores, shallow fractured flakes and grey weathered depressions."""
    pit = Image.new('L', (CELL, CELL), 0)
    d = ImageDraw.Draw(pit)
    for _ in range(count):
        x, y = rng.integers(5, 251, 2)
        rx = int(rng.choice([1, 1, 1, 1, 1, 2]))
        ry = max(1, int(rx*rng.uniform(.4, 1.2)))
        d.ellipse((x-rx, y-ry, x+rx, y+ry), fill=int(rng.integers(8, 34)))
    mask = np.asarray(pit.filter(ImageFilter.GaussianBlur(.45)), dtype=np.float32)*strength
    pixels -= mask[:, :, None]*.48
    height -= mask*.42
    flakes = Image.new('L', (CELL, CELL), 0)
    f = ImageDraw.Draw(flakes)
    for _ in range(8):
        cx, cy = rng.integers(9, 247, 2)
        radius = rng.uniform(9, 33)
        angles = np.linspace(0, 2*np.pi, 10, endpoint=False)
        points = [(cx+np.cos(a)*radius*rng.uniform(.55, 1.1),
                   cy+np.sin(a)*radius*rng.uniform(.3, .7)) for a in angles]
        f.polygon(points, fill=int(rng.integers(6, 18)))
    loss = np.asarray(flakes.filter(ImageFilter.GaussianBlur(1.2)), dtype=np.float32)*strength
    pixels -= loss[:, :, None]*.62
    height -= loss*.4


def ashlar(rng, base, variant):
    pixels, height = surface(rng, base, 1.2)
    pitting(rng, pixels, height, 1.15, [170, 250, 230, 190][variant])
    # Weathered bedding and chisel striations are long, broken horizontal
    # features rather than a field of round, terrazzo-like dots.
    a = rng.uniform(-1, 1, (57, 9)).astype(np.float32)
    striae = np.asarray(Image.fromarray(a, mode='F').resize((CELL, CELL), Image.Resampling.BICUBIC))
    weather = np.clip(-noise(rng, 7, 12)-1.5, 0, 11)
    pixels += (striae*(4 if variant in {1, 2} else 2.5)-weather)[:, :, None]
    height += striae*3
    yy, xx = np.mgrid[:CELL, :CELL]
    # Geometry already makes the drafted boss. Texture adds uneven, abraded
    # dressing, with no bright continuous frame that would look like toy bricks.
    edge = np.minimum.reduce([xx-8, 247-xx, yy-8, 247-yy]).astype(float)
    uneven = noise(rng, 22, 2.3)
    margin = np.clip((13-edge+uneven)/8, 0, 1)
    pixels -= margin[:, :, None]*3.5
    height -= margin*3
    # Irregular surviving tooling lines and chips in the dressed margins.
    scars = Image.new('L', (CELL, CELL), 0)
    d = ImageDraw.Draw(scars)
    for _ in range(42):
        horizontal = bool(rng.integers(2))
        along = int(rng.integers(16, 238)); side = int(rng.choice([12, 14, 239, 243]))
        length = int(rng.integers(2, 10))
        if horizontal: d.line((along, side, along+length, side+int(rng.integers(-1, 2))), fill=int(rng.integers(8, 25)))
        else: d.line((side, along, side+int(rng.integers(-1, 2)), along+length), fill=int(rng.integers(8, 25)))
    # A few thin, branching cracks, never a regular repeated diagonal cross.
    for _ in range(2 if variant in {1, 3} else 1):
        x, y = rng.integers(20, 230, 2); points = [(int(x), int(y))]
        for _ in range(int(rng.integers(3, 6))):
            x = np.clip(x+rng.integers(-6, 7), 9, 247)
            y = np.clip(y+rng.integers(4, 13), 9, 247)
            points.append((int(x), int(y)))
        d.line(points, fill=35, width=1)
    loss = np.asarray(scars, dtype=np.float32)
    pixels -= loss[:, :, None]*.38
    height -= loss*.24
    # Soft deposits collect near the block bottom without outlining all edges.
    deposit = np.clip((yy-191)/56, 0, 1)*(3+noise(rng, 10, 3))
    pixels -= deposit[:, :, None]
    return pixels, height


def masonry(rng, base, cols, rows, rough=False):
    pixels, height = surface(rng, base, 1.3 if rough else .8)
    block_tone = np.zeros((CELL, CELL), dtype=np.float32)
    mask = Image.new('L', (CELL, CELL), 0)
    md = ImageDraw.Draw(mask)
    tone = Image.new('F', (CELL, CELL), 0)
    td = ImageDraw.Draw(tone)
    cell_w, cell_h = 240/cols, 240/rows
    for row in range(rows):
        y0 = 8+row*cell_h; y1 = 8+(row+1)*cell_h
        x = 8-cell_w*(.5 if row%2 else rng.uniform(.05, .3))
        while x < 248:
            width = cell_w*rng.uniform(.65, 1.4)
            xa, xb = max(8, x), min(248, x+width)
            # Uneven ashlar edges; narrow dark joints remain visible in mips.
            gap = .75 if rough else .6
            poly = [(xa+gap, y0+gap+rng.uniform(-.35,.35)),
                    (xb-gap, y0+gap+rng.uniform(-.35,.35)),
                    (xb-gap, y1-gap+rng.uniform(-.35,.35)),
                    (xa+gap, y1-gap+rng.uniform(-.35,.35))]
            md.polygon(poly, fill=255)
            td.polygon(poly, fill=float(rng.uniform(-8, 8)))
            x += width
    block_tone[:] = np.asarray(tone)
    coverage = np.asarray(mask, dtype=np.float32)/255
    smooth = np.asarray(mask.filter(ImageFilter.GaussianBlur(.6)), dtype=np.float32)/255
    pixels += block_tone[:, :, None]
    # Recessed brown-grey joints, with no painted white highlights.
    joint = (1-coverage)*31 + np.clip(coverage-smooth, 0, 1)*10
    pixels -= joint[:, :, None]
    height += coverage*11-(1-coverage)*7
    pitting(rng, pixels, height, .7 if rough else .45, 220 if rough else 120)
    # Soft grey staining breaks the computer-perfect running bond.
    stain = np.clip(-noise(rng, 7, 12)-2, 0, 14)
    pixels -= stain[:, :, None]
    return pixels, height


def tile(i, rng):
    # All stone colours share a restrained neutral limestone palette.
    colors = [(168,163,150), (177,171,156), (158,154,143), (172,167,153),
              (166,160,146), (157,152,139), (172,167,153), (32,32,27),
              (170,165,151), (91,74,51), (53,64,35), (40,40,33),
              (133,122,100), (172,166,151), (86,78,62), (173,167,152)]
    if i < 4: return ashlar(rng, colors[i], i)
    if i == 4: return masonry(rng, colors[i], 16, 17)
    if i == 5: return masonry(rng, colors[i], 16, 30, True)
    if i in {6, 13, 15}: return masonry(rng, colors[i], 6, 5)
    if i == 8: return masonry(rng, colors[i], 5, 9)
    pixels, height = surface(rng, colors[i])
    if i == 9:
        yy, xx = np.mgrid[:CELL, :CELL]
        grain = np.sin(xx*.63+noise(rng, 5, 2))*2
        pixels += grain[:, :, None]
        for x in range(14, 249, 24):
            pixels[8:248, x:x+1] -= 17
            height[8:248, x:x+1] -= 5
    elif i == 10:
        # Opaque plant clumps have natural tonal foliage variation only.
        leaves = Image.new('L', (CELL, CELL), 0); d = ImageDraw.Draw(leaves)
        for _ in range(420):
            x,y = rng.integers(5,251,2); r = int(rng.integers(1,5))
            d.ellipse((x-r,y-r,x+r,y+r),fill=int(rng.integers(15,38)))
        field = np.asarray(leaves,dtype=np.float32)-12
        pixels += field[:, :, None]*np.asarray([.65,.8,.4])[None,None,:]
    elif i == 11:
        # Dark interior and sparse iron grille, without any emissive channel.
        for x in range(18,249,27):
            pixels[8:248,x:x+3] = [103,100,85];height[8:248,x:x+3] += 12
        for y in range(22,249,48):
            pixels[y:y+3,8:248] = [103,100,85];height[y:y+3,8:248] += 12
    elif i == 12:
        pitting(rng,pixels,height,1.4,430)
        pixels += noise(rng,15,9)[:, :, None]
    return pixels, height


def create():
    rng = np.random.default_rng(1970)
    diffuse = np.zeros((1024,1024,4), dtype=np.uint8)
    normal = np.zeros_like(diffuse)
    specular = np.zeros_like(diffuse)
    for i in range(16):
        pixels, relief = tile(i, rng)
        # Pad each tile from its sampled region so atlas neighbours cannot leak
        # into the normal slopes or the first mip levels at polygon boundaries.
        pixels[:8] = pixels[8];pixels[248:] = pixels[247]
        pixels[:,:8] = pixels[:,8:9];pixels[:,248:] = pixels[:,247:248]
        relief[:8] = relief[8];relief[248:] = relief[247]
        relief[:,:8] = relief[:,8:9];relief[:,248:] = relief[:,247:248]
        gy,gx = np.gradient(relief.astype(np.float32)/255)
        packed = np.zeros((CELL,CELL,4), dtype=np.uint8)
        # PdxMeshAdvanced: green = normal X, alpha = normal Y, blue = emission.
        nx = np.clip(128-gx*390,48,208).astype(np.uint8)
        ny = np.clip(128+gy*390,48,208).astype(np.uint8)
        packed[:,:,0] = nx;packed[:,:,1] = nx;packed[:,:,3] = ny
        # Blue remains exactly zero: aged exterior masonry is not emissive.
        # The native improved Blinn-Phong shader reads alpha as glossiness.
        # Low values keep weathered limestone matte in the game as well.
        matte = np.empty_like(packed);matte[:] = [23,27,0,30]
        glossiness = np.clip(30+noise(rng,13,5),20,43).astype(np.uint8)
        matte[:,:,3] = glossiness
        row,col = divmod(i,4);y,x = row*CELL,col*CELL
        diffuse[y:y+CELL,x:x+CELL,:3] = np.clip(pixels,0,255).astype(np.uint8)
        diffuse[y:y+CELL,x:x+CELL,3] = 255
        normal[y:y+CELL,x:x+CELL] = packed
        specular[y:y+CELL,x:x+CELL] = matte
    OUT.mkdir(parents=True, exist_ok=True)
    for kind,pixels,codec in [('diffuse',diffuse,'DXT1'),('normal',normal,'DXT5'),('specular',specular,'DXT5')]:
        dds.save_mipmapped_dds(Image.fromarray(pixels), OUT/f'{PREFIX}_{kind}.dds',codec)


if __name__ == '__main__':
    create()
