"""Sprites for the West Germany 1970 windows (inner-German relations, internal security).

Drawn with Pillow in the palette of a government file ("Akte"): dark khaki cardboard, printed
khaki rules, brass accents and red stamp ink (see akte_sprites.py for the window skin), and written
as uncompressed 32-bit DDS.

    SPRITES: name -> (relative texture path, frames)
"""
import os
import struct

import numpy as np
from PIL import Image, ImageDraw, ImageFont

DIR = "gfx/interface/cwger_1970"
SPRITES = {}

GOLD = (206, 182, 120, 255)      # brass / printed khaki
GOLD_D = (150, 132, 88, 255)
NAVY = (30, 27, 19, 255)         # ink
PANEL = (38, 34, 24, 225)        # a darker card clipped into the folder
PANEL_L = (56, 50, 36, 235)
EDGE = (128, 114, 80, 255)
GREY = (84, 78, 64, 255)
WHITE = (230, 232, 236, 255)
STAGE_COL = [(66, 160, 98), (120, 168, 84), (196, 178, 70), (222, 140, 52), (214, 92, 44), (190, 40, 40), (120, 10, 16)]
BAR_COL = {"red": (196, 52, 44), "green": (72, 168, 96), "gold": (226, 168, 52), "blue": (64, 124, 200),
           "grey": (132, 140, 152), "purple": (136, 92, 180), "teal": (52, 160, 160)}


def write_dds(path, im):
    rgba = np.asarray(im.convert("RGBA"))
    h, w, _ = rgba.shape
    bgra = rgba[..., [2, 1, 0, 3]].copy()
    header = struct.pack("<4sIIIIIII44sIIIIIIIIIIIII",
                         b"DDS ", 124, 0x1 | 0x2 | 0x4 | 0x1000 | 0x8, h, w, w * 4, 0, 1, b"\0" * 44,
                         32, 0x41, 0, 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000,
                         0x1000, 0, 0, 0, 0)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(header)
        f.write(bgra.tobytes())


def font(size, bold=True):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


IMAGES = {}   # name -> PIL image (all frames side by side)


def reg(name, im, frames=1):
    SPRITES[name] = (f"{DIR}/{name}.dds", frames)
    IMAGES[name] = im


def frames(ims):
    w, h = ims[0].size
    sheet = Image.new("RGBA", (w * len(ims), h), (0, 0, 0, 0))
    for i, im in enumerate(ims):
        sheet.paste(im, (i * w, 0))
    return sheet


def panel(w, h, fill=PANEL, edge=EDGE, accent=None, clip=True):
    """A card clipped into the file: dark card stock, printed frame, a paper clip on the top edge."""
    from akte_sprites import cardboard
    im = cardboard(w, h, fill[:3], grain=4, streak=0.3)
    a = np.asarray(im).copy()
    a[..., 3] = fill[3]
    im = Image.fromarray(a, "RGBA")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=edge)
    d.rectangle([2, 2, w - 3, h - 3], outline=edge[:3] + (70,))
    if accent:
        d.rectangle([0, 0, 3, h - 1], fill=accent)
    if clip and w > 120:
        cx = w - 26
        d.rounded_rectangle([cx, -2, cx + 9, 14], radius=4, outline=(176, 180, 182, 255), width=2)
        d.rounded_rectangle([cx + 2, 1, cx + 7, 10], radius=2, outline=(130, 134, 136, 255), width=1)
    return im


def bar(w, h, col):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    a = np.zeros((h, w, 4), np.uint8)
    for y in range(h):
        k = 1.15 - 0.45 * (y / max(1, h - 1))
        a[y, :, :3] = np.clip(np.array(col[:3]) * k, 0, 255)
        a[y, :, 3] = 255
    a[0, :, :3] = np.clip(a[0, :, :3].astype(int) + 40, 0, 255)
    a[:, -2:, :3] = (250, 236, 200)   # bright leading edge, as in the mod's bars
    return Image.fromarray(a)


def gradient_track(w, h):
    a = np.zeros((h, w, 4), np.uint8)
    left, mid, right = np.array((176, 40, 36)), np.array((86, 92, 104)), np.array((52, 150, 86))
    for x in range(w):
        t = x / (w - 1)
        c = left + (mid - left) * (t / 0.5) if t < 0.5 else mid + (right - mid) * ((t - 0.5) / 0.5)
        a[:, x, :3] = c
    for y in range(h):
        a[y, :, :3] = np.clip(a[y, :, :3] * (1.1 - 0.35 * y / (h - 1)), 0, 255)
    a[..., 3] = 255
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=EDGE)
    for i in range(1, 8):
        x = round(i * (w - 1) / 8)
        d.line([x, h - 5, x, h - 1], fill=(230, 230, 230, 160))
    d.line([w // 2, 0, w // 2, h - 1], fill=(240, 240, 240, 220))
    return im


def marker(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(0, 0), (w - 1, 0), (w // 2, 5)], fill=GOLD)
    d.rectangle([w // 2 - 1, 4, w // 2 + 1, h - 6], fill=GOLD)
    d.polygon([(0, h - 1), (w - 1, h - 1), (w // 2, h - 6)], fill=GOLD)
    return im


def stage_box(i, on, w=96, h=40):
    col = STAGE_COL[i]
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if on:
        for y in range(h):
            k = 1.15 - 0.5 * y / (h - 1)
            d.line([0, y, w, y], fill=tuple(int(min(255, c * k)) for c in col) + (255,))
        d.rectangle([0, 0, w - 1, h - 1], outline=(240, 220, 170, 255))
        txtc = WHITE
    else:
        d.rectangle([0, 0, w - 1, h - 1], fill=(36, 32, 22, 240), outline=EDGE)
        d.rectangle([0, h - 4, w - 1, h - 1], fill=col + (200,))
        txtc = (164, 152, 120, 255)
    f = font(20)
    t = str(i)
    tw = d.textlength(t, font=f)
    d.text(((w - tw) / 2, 7), t, font=f, fill=txtc)
    return im


def highlight(w, h, col=GOLD, thick=2):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k in range(thick):
        d.rectangle([k, k, w - 1 - k, h - 1 - k], outline=col)
    return im


def dots(n, filled, size=12, gap=4, col=(226, 186, 92)):
    w = n * size + (n - 1) * gap
    im = Image.new("RGBA", (w, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i in range(n):
        x = i * (size + gap)
        if i < filled:
            d.ellipse([x, 0, x + size - 1, size - 1], fill=col + (255,), outline=(255, 240, 200, 255))
        else:
            d.ellipse([x, 0, x + size - 1, size - 1], fill=(34, 30, 21, 255), outline=(120, 108, 78, 255))
    return im


def status_icon(kind, s=20):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cols = {"locked": (90, 96, 108), "closed": (190, 56, 48), "open": (70, 176, 98), "strained": (224, 150, 48),
            "done": (70, 176, 98), "nego": (226, 186, 72), "avail": (96, 150, 220), "susp": (190, 56, 48), "off": (60, 66, 78)}
    c = cols[kind]
    if kind == "locked":
        d.rectangle([4, 9, s - 5, s - 3], fill=c + (255,))
        d.arc([6, 2, s - 7, 14], 180, 360, fill=c + (255,), width=2)
    elif kind in ("done", "open"):
        d.ellipse([1, 1, s - 2, s - 2], fill=c + (255,))
        d.line([(5, 10), (9, 14), (15, 6)], fill=WHITE, width=2)
    elif kind in ("closed", "susp"):
        d.ellipse([1, 1, s - 2, s - 2], fill=c + (255,))
        d.line([(6, 6), (14, 14)], fill=WHITE, width=2)
        d.line([(14, 6), (6, 14)], fill=WHITE, width=2)
    elif kind == "strained":
        d.polygon([(s // 2, 1), (s - 2, s - 2), (1, s - 2)], fill=c + (255,))
        d.rectangle([s // 2 - 1, 7, s // 2 + 1, 12], fill=NAVY)
        d.rectangle([s // 2 - 1, 14, s // 2 + 1, 16], fill=NAVY)
    elif kind == "nego":
        d.ellipse([1, 1, s - 2, s - 2], fill=c + (255,))
        d.ellipse([5, 9, 7, 11], fill=NAVY)
        d.ellipse([9, 9, 11, 11], fill=NAVY)
        d.ellipse([13, 9, 15, 11], fill=NAVY)
    elif kind == "avail":
        d.ellipse([1, 1, s - 2, s - 2], outline=c + (255,), width=3)
    else:
        d.ellipse([3, 3, s - 4, s - 4], outline=c + (255,), width=2)
    return im


def topbar_icon(kind):
    """30x26 topbar button in the style of mdcw_cw_topbar_box."""
    w, h = 30, 26
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=4, fill=(52, 46, 31, 255), outline=(150, 134, 94, 255))
    if kind == "rivalry":
        # two halves: black-red-gold and the GDR's hammer-and-compass blue-grey, split by a gold line
        for i, c in enumerate([(20, 20, 20), (200, 30, 30), (230, 190, 40)]):
            d.rectangle([5, 5 + i * 5, 13, 9 + i * 5], fill=c + (255,))
        for i, c in enumerate([(20, 20, 20), (200, 30, 30), (230, 190, 40)]):
            d.rectangle([17, 5 + i * 5, 25, 9 + i * 5], fill=c + (255,))
        d.ellipse([18, 8, 24, 14], outline=(110, 170, 90, 255), width=2)
        d.line([15, 3, 15, 22], fill=GOLD, width=2)
    else:
        # a five-pointed police star with a magnifier hint
        import math
        cx, cy, r1, r2 = 15, 13, 10, 4.2
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            r = r1 if k % 2 == 0 else r2
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=(64, 140, 92, 255), outline=(230, 220, 170, 255))
        d.ellipse([12, 10, 18, 16], fill=(230, 220, 170, 255))
    return im


def portrait_frame(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=GOLD_D, width=2)
    return im


PHOTO_BOX = (6, 20, 66, 100)   # x0, y0, x1, y1 of the photo on the wanted card (60x80)
RAF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "portraits", "raf")
# photo frames: 1-6 generation 1, 7-12 generation 2, 13 = no photo (the card's silhouette shows through)
RAF_PHOTOS = ["baader", "ensslin", "meinhof", "raspe", "meins", "mohnhaupt",
              "mohnhaupt", "klar", "folkerts", "boock", "wisniewski", "schulz", None]


def wanted_card(state, w=176, h=104):
    """Wanted-list card background. state: 0 at large, 1 traced, 2 arrested, 3 dead, 4 left the group, 5 unknown slot."""
    cols = [(150, 44, 40), (214, 150, 48), (70, 140, 92), (60, 60, 64), (84, 110, 150), (40, 46, 58)]
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], fill=(222, 214, 190, 255) if state != 5 else (44, 40, 28, 220), outline=(80, 70, 50, 255))
    d.rectangle([0, 0, w - 1, 16], fill=cols[state] + (255,))
    # silhouette in a photo box (covered by the photo when there is one)
    x0, y0, x1, y1 = PHOTO_BOX
    d.rectangle([x0, y0, x1, y1], fill=(70, 70, 74, 255) if state != 5 else (62, 56, 40, 255))
    if state != 5:
        d.ellipse([x0 + 17, y0 + 10, x0 + 43, y0 + 38], fill=(30, 30, 34, 255))
        d.pieslice([x0 + 6, y0 + 36, x0 + 54, y0 + 100], 180, 360, fill=(30, 30, 34, 255))
    return im


def wanted_photo(key):
    """60x80 smartphone-look photo with a thin print border, or an empty frame."""
    x0, y0, x1, y1 = PHOTO_BOX
    pw, ph = x1 - x0, y1 - y0
    im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    path = os.path.join(RAF_DIR, f"{key}.png") if key else ""
    if key and os.path.exists(path):
        p = Image.open(path).convert("RGB").resize((pw, ph), Image.LANCZOS)
        im.paste(p, (0, 0))
        ImageDraw.Draw(im).rectangle([0, 0, pw - 1, ph - 1], outline=(250, 248, 240, 255), width=1)
    return im


def wanted_stamp(state):
    """Overlay on the photo: crossed out when arrested, a mourning band when dead, washed out when gone."""
    x0, y0, x1, y1 = PHOTO_BOX
    pw, ph = x1 - x0, y1 - y0
    im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if state == 1:
        d.rectangle([0, 0, pw - 1, ph - 1], outline=(214, 150, 48, 255), width=2)
    elif state == 2:
        d.line([(1, 1), (pw - 2, ph - 2)], fill=(40, 120, 70, 255), width=3)
        d.line([(pw - 2, 1), (1, ph - 2)], fill=(40, 120, 70, 255), width=3)
    elif state == 3:
        d.rectangle([0, 0, pw - 1, ph - 1], fill=(0, 0, 0, 70), outline=(10, 10, 10, 255), width=3)
        d.polygon([(pw - 22, 0), (pw - 1, 0), (pw - 1, 21)], fill=(10, 10, 10, 255))
    elif state == 4:
        d.rectangle([0, 0, pw - 1, ph - 1], fill=(200, 210, 230, 120), outline=(84, 110, 150, 255), width=2)
    return im


def target_icon(i, s=40):
    """Six target categories of the RAF: justice, business, US forces, politics, infrastructure, embassies."""
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=6, fill=(40, 36, 25, 255), outline=EDGE)
    c = (226, 196, 120, 255)
    if i == 0:   # scales
        d.line([20, 8, 20, 32], fill=c, width=2); d.line([9, 12, 31, 12], fill=c, width=2)
        d.polygon([(9, 13), (5, 22), (13, 22)], outline=c); d.polygon([(31, 13), (27, 22), (35, 22)], outline=c)
        d.line([13, 32, 27, 32], fill=c, width=2)
    elif i == 1:  # factory/briefcase
        d.rectangle([8, 14, 32, 30], outline=c, width=2); d.rectangle([15, 9, 25, 14], outline=c, width=2)
        d.line([8, 21, 32, 21], fill=c, width=2)
    elif i == 2:  # star
        import math
        pts = [(20 + (11 if k % 2 == 0 else 4.5) * math.cos(-math.pi / 2 + k * math.pi / 5),
                21 + (11 if k % 2 == 0 else 4.5) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)]
        d.polygon(pts, outline=c, fill=(60, 80, 130, 255))
    elif i == 3:  # parliament dome
        d.pieslice([10, 8, 30, 28], 180, 360, outline=c, width=2); d.rectangle([8, 18, 32, 31], outline=c, width=2)
        for x in (13, 18, 23, 28):
            d.line([x, 20, x, 30], fill=c)
    elif i == 4:  # pylon / prison bars
        d.rectangle([9, 9, 31, 31], outline=c, width=2)
        for x in (14, 20, 26):
            d.line([x, 9, x, 31], fill=c, width=2)
    else:          # globe
        d.ellipse([8, 8, 32, 32], outline=c, width=2); d.line([8, 20, 32, 20], fill=c); d.ellipse([15, 8, 25, 32], outline=c)
    return im


def shield(on, s=26):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(3, 3), (s - 4, 3), (s - 4, 12), (s // 2, s - 2), (3, 12)]
    if on:
        d.polygon(pts, fill=(64, 140, 200, 255), outline=(220, 230, 250, 255))
    else:
        d.polygon(pts, fill=(36, 32, 22, 255), outline=(120, 108, 78, 255))
    return im


def scales(pos, w=300, h=40):
    """Security state vs rule of law balance; 21 frames for -100..100 in steps of 10."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    import math
    ang = math.radians(pos * 0.12)  # ±12 degrees
    cx, cy, L = w // 2, 12, w // 2 - 30
    dx, dy = L * math.cos(ang), L * math.sin(ang)
    d.polygon([(cx - 8, h - 2), (cx + 8, h - 2), (cx, cy)], fill=GOLD_D)
    d.line([cx - dx, cy - dy, cx + dx, cy + dy], fill=GOLD, width=3)
    for sx, sy, col in ((cx - dx, cy - dy, (190, 70, 60, 255)), (cx + dx, cy + dy, (80, 140, 210, 255))):
        d.line([sx, sy, sx - 10, sy + 14], fill=GOLD_D)
        d.line([sx, sy, sx + 10, sy + 14], fill=GOLD_D)
        d.pieslice([sx - 14, sy + 6, sx + 14, sy + 24], 0, 180, fill=col)
    return im


def build_all():
    import akte_sprites
    akte_sprites.build(reg)
    reg("cwgg_topbar_rivalry", topbar_icon("rivalry"))
    reg("cwgg_topbar_security", topbar_icon("security"))
    reg("cwgg_climate_track", gradient_track(560, 18))
    reg("cwgg_marker", marker(12, 30))
    reg("cwgg_marker_small", marker(8, 18))
    for i in range(7):
        reg(f"cwgg_stage_{i}", frames([stage_box(i, False), stage_box(i, True)]), 2)
    reg("cwgg_stage_frame", highlight(100, 44, GOLD, 3))
    reg("cwgg_select_160", highlight(164, 30, GOLD, 2))
    reg("cwgg_initiative", frames([dots(6, k) for k in range(7)]), 7)
    reg("cwgg_level", frames([dots(3, k, size=11, gap=3) for k in range(4)]), 4)
    reg("cwgg_level5", frames([dots(5, k, size=10, gap=3, col=(214, 92, 60)) for k in range(6)]), 6)
    reg("cwgg_channel", frames([status_icon(k) for k in ("locked", "closed", "open", "strained")]), 4)
    reg("cwgg_treaty", frames([status_icon(k) for k in ("locked", "avail", "nego", "done", "susp")]), 5)
    for name, col in BAR_COL.items():
        reg(f"cwgg_bar_{name}", bar(300, 18, col))
        reg(f"cwgg_bar_small_{name}", bar(160, 10, col))
    reg("cwgg_track_small_bipolar", gradient_track(160, 10))
    reg("cwgg_panel_360", panel(360, 56))
    reg("cwgg_panel_740", panel(740, 46))
    reg("cwgg_panel_crisis", panel(740, 214, fill=(34, 30, 21, 240), edge=GOLD_D))
    reg("cwgg_panel_card", panel(236, 100))
    reg("cwgg_panel_wanted", panel(236, 188))
    reg("cwgg_portrait_frame", portrait_frame(108, 146))
    # security window
    reg("cwgg_wanted", frames([wanted_card(k) for k in range(6)]), 6)
    reg("cwgg_wanted_photo", frames([wanted_photo(k) for k in RAF_PHOTOS]), len(RAF_PHOTOS))
    reg("cwgg_wanted_stamp", frames([wanted_stamp(k) for k in range(6)]), 6)
    reg("cwgg_targets", frames([target_icon(k) for k in range(6)]), 6)
    reg("cwgg_shield", frames([shield(False), shield(True)]), 2)
    reg("cwgg_scales", frames([scales(p) for p in range(-100, 101, 10)]), 21)
    return SPRITES


def write_all(root):
    build_all()
    out = []
    for name, (rel, _n) in SPRITES.items():
        write_dds(os.path.join(root, rel), IMAGES[name])
        out.append(rel)
    return out


def gfx_file(header):
    build_all()
    import akte_sprites
    lines = [header, "spriteTypes = {"]
    for name, (rel, n) in SPRITES.items():
        if name in akte_sprites.CORNERED:
            w, h = akte_sprites.CORNERED[name]
            lines.append(f'\tcorneredTileSpriteType = {{\n\t\tname = "GFX_{name}"\n\t\tsize = {{ x = {w} y = {h} }}\n\t\ttexturefile = "{rel}"\n'
                         f'\t\ttilingCenter = yes\n\t\teffectFile = "gfx/FX/buttonstate_nodowneffect.lua"\n\t}}')   # corneredTileSpriteType has no legacy_lazy_load
            continue
        extra = f"\n\t\tnoOfFrames = {n}" if n > 1 else ""
        fx = "\n\t\teffectFile = \"gfx/FX/buttonstate.lua\"" if name.startswith("cwgg_topbar") or name in akte_sprites.BUTTONS else ""
        lines.append(f'\tspriteType = {{\n\t\tname = "GFX_{name}"\n\t\ttexturefile = "{rel}"{extra}{fx}\n\t\tlegacy_lazy_load = no\n\t}}')
    lines.append("}")
    return "\n".join(lines) + "\n"
