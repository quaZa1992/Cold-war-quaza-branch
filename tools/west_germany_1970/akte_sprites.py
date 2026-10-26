# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""File-folder ("Akte") skin for the West Germany 1970 windows.

Both windows look like government files from Bonn: a dark khaki cardboard folder with a printed label
field, punched filing holes, register tabs, typed section strips and rubber-stamp buttons. The rivalry
window carries the Bundesadler on the left and the emblem of the GDR on the right; the security window
is a grey-green file of the Federal Criminal Police Office with a GEHEIM stamp.

All pieces are drawn with Pillow (no external artwork) and registered through gui_sprites.reg().
Text in the game stays light, so every surface that carries text is dark.
"""
import os
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

RNG = np.random.default_rng(1970)

# ------------------------------------------------------------------ palette
KHAKI = (82, 74, 50)          # folder cardboard
KHAKI_D = (54, 48, 32)
KHAKI_L = (112, 101, 70)
LINE = (196, 180, 134)        # printed rules, label frames
LINE_D = (150, 136, 98)
INK = (28, 25, 18)
RED = (176, 40, 34)           # stamp ink
GREEN_FOLDER = (62, 72, 60)   # BKA file
GREEN_D = (40, 48, 40)
GREEN_L = (88, 100, 84)
GOLD = (232, 192, 48)
BLACK = (22, 22, 22)
EAGLE_RED = (204, 34, 30)

FONTS = {
    "mono": "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
    "monob": "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf",
    "sansb": "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf",
    "serifb": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
}


def F(kind, size):
    try:
        return ImageFont.truetype(FONTS[kind], size)
    except OSError:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)


# ------------------------------------------------------------------ textures
def cardboard(w, h, base, grain=7.0, streak=0.5):
    """Folder cardboard: base colour, fibre noise, faint horizontal streaks and a soft vignette."""
    a = np.zeros((h, w, 3), np.float32)
    a[:] = base
    noise = RNG.normal(0, grain, (h, w, 1)).astype(np.float32)
    a += noise
    # fibres: short horizontal smears
    fib = RNG.normal(0, 1, (h, w // 6 + 1)).astype(np.float32)
    fib = np.array(Image.fromarray(fib, "F").resize((w, h), Image.BILINEAR), np.float32)
    a += (fib * 3.0 * streak)[..., None]
    # vignette
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a *= (1.0 - 0.16 * np.clip(d - 0.55, 0, 1))[..., None]
    a = np.clip(a, 0, 255).astype(np.uint8)
    out = np.dstack([a, np.full((h, w, 1), 255, np.uint8)])
    return Image.fromarray(out, "RGBA")


def ink_wear(im, strength=0.22, seed=0):
    """Rubber-stamp ink: knock random holes into the alpha channel."""
    rng = np.random.default_rng(seed)
    a = np.asarray(im).copy()
    m = rng.random(a.shape[:2]) < strength
    blur = np.array(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))) / 255.0
    a[..., 3] = (a[..., 3] * (1 - 0.75 * blur)).astype(np.uint8)
    return Image.fromarray(a, "RGBA")


def rounded_mask(w, h, r):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    return m


# ------------------------------------------------------------------ emblems (drawn at 8x, downsampled)
def _eagle(d, s, ox=0, oy=0, col=BLACK, red=EAGLE_RED):
    """A stylised heraldic eagle (head to the viewer's left) in a 100x100 box scaled by s."""
    P = lambda pts: [(ox + x * s, oy + y * s) for x, y in pts]
    for side in (-1, 1):
        cx = 50
        # wing: top edge rising outwards, five feather tips stepping back to the body
        wing = [(cx + side * 6, 34), (cx + side * 20, 27), (cx + side * 36, 20), (cx + side * 44, 22),
                (cx + side * 46, 34), (cx + side * 46, 56), (cx + side * 44, 64),
                (cx + side * 39, 58), (cx + side * 37, 68), (cx + side * 31, 61), (cx + side * 28, 71),
                (cx + side * 23, 63), (cx + side * 19, 72), (cx + side * 14, 62), (cx + side * 8, 66)]
        d.polygon(P(wing), fill=col)
        # inner feather lines in the background colour are left out at this size
        # legs and claws
        leg = [(cx + side * 6, 70), (cx + side * 10, 70), (cx + side * 13, 82), (cx + side * 9, 82)]
        d.polygon(P(leg), fill=col)
        for k in range(3):
            tx = cx + side * (8 + k * 3)
            d.polygon(P([(tx - 1.2, 81), (tx + 1.2, 81), (tx + side * 1.5, 88)]), fill=red)
    # body
    d.ellipse(P([(39, 30), (61, 76)]), fill=col)
    # tail fan
    d.polygon(P([(42, 72), (58, 72), (64, 90), (57, 87), (50, 93), (43, 87), (36, 90)]), fill=col)
    # neck and head (turned to the viewer's left)
    d.polygon(P([(44, 36), (56, 36), (52, 22), (44, 20)]), fill=col)
    d.ellipse(P([(36, 12), (54, 30)]), fill=col)
    # beak and tongue
    d.polygon(P([(37, 18), (28, 21), (31, 24), (37, 24)]), fill=red)
    d.line(P([(30, 23), (26, 27)]), fill=red, width=max(1, int(1.2 * s)))
    # eye
    d.ellipse(P([(41.5, 17.5), (44.5, 20.5)]), fill=GOLD)


EMBLEM_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "emblems")


def emblem_from_file(name, size=44):
    """Fit a supplied coat of arms into the size x size emblem slot (transparent, centred, lightly sharpened)."""
    from PIL import ImageFilter
    src = Image.open(os.path.join(EMBLEM_DIR, name)).convert("RGBA")
    bbox = src.getbbox()
    if bbox:
        src = src.crop(bbox)
    scale = min(size / src.width, size / src.height)
    w, h = max(1, round(src.width * scale)), max(1, round(src.height * scale))
    small = src.resize((w, h), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=0.6, percent=60, threshold=1))
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    im.paste(small, ((size - w) // 2, (size - h) // 2), small)
    return im


def emblem_brd(size=44):
    k = 8
    S = size * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([0, 0, S - 1, S - 1], fill=(30, 28, 22, 255))
    d.ellipse([S * 0.05, S * 0.05, S * 0.95, S * 0.95], fill=GOLD + (255,))
    d.ellipse([S * 0.05, S * 0.05, S * 0.95, S * 0.95], outline=(120, 92, 20, 255), width=k)
    _eagle(d, S * 0.0078, ox=S * 0.11, oy=S * 0.1)
    return im.resize((size, size), Image.LANCZOS)


def emblem_ddr(size=44):
    """Hammer and compass in a wreath of rye, bound with a black-red-gold ribbon."""
    k = 8
    S = size * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([0, 0, S - 1, S - 1], fill=(30, 28, 22, 255))
    d.ellipse([S * 0.05, S * 0.05, S * 0.95, S * 0.95], fill=(150, 26, 24, 255))
    cx, cy, r = S / 2, S / 2, S * 0.34
    # wreath: ears of rye on both sides
    for side in (-1, 1):
        for i in range(9):
            t = math.radians(110 + i * 17)
            x = cx + side * r * math.cos(t) * -1
            y = cy + r * math.sin(t) * -1 + S * 0.02
            ang = (t if side == 1 else math.pi - t)
            ex, ey = S * 0.05, S * 0.026
            box = Image.new("RGBA", (int(ex * 2.4), int(ex * 2.4)), (0, 0, 0, 0))
            ImageDraw.Draw(box).ellipse([box.width / 2 - ex, box.height / 2 - ey, box.width / 2 + ex, box.height / 2 + ey], fill=GOLD + (255,))
            box = box.rotate(math.degrees(ang) + 90 * side, resample=Image.BICUBIC)
            im.alpha_composite(box, (int(x - box.width / 2), int(y - box.height / 2)))
    d = ImageDraw.Draw(im)
    # ribbon at the bottom
    for i, c in enumerate([BLACK, (210, 30, 30), GOLD]):
        y0 = S * 0.74 + i * S * 0.035
        d.rectangle([S * 0.30, y0, S * 0.70, y0 + S * 0.035], fill=c + (255,))
    # hammer: handle and head
    hx = cx
    d.polygon([(hx - S * 0.02, S * 0.36), (hx + S * 0.02, S * 0.36), (hx + S * 0.02, S * 0.70), (hx - S * 0.02, S * 0.70)], fill=GOLD + (255,))
    d.rectangle([hx - S * 0.10, S * 0.28, hx + S * 0.10, S * 0.37], fill=GOLD + (255,))
    # compass: two legs from a hinge and the arc
    lw = int(S * 0.035)
    top = (cx, S * 0.22)
    d.line([top, (cx - S * 0.17, S * 0.66)], fill=(232, 228, 214, 255), width=lw)
    d.line([top, (cx + S * 0.17, S * 0.66)], fill=(232, 228, 214, 255), width=lw)
    d.ellipse([cx - S * 0.035, S * 0.19, cx + S * 0.035, S * 0.26], fill=(232, 228, 214, 255))
    d.arc([cx - S * 0.22, S * 0.30, cx + S * 0.22, S * 0.72], 20, 160, fill=(232, 228, 214, 255), width=lw)
    return im.resize((size, size), Image.LANCZOS)


def emblem_bka(size=44):
    k = 8
    S = size * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([0, 0, S - 1, S - 1], fill=(26, 32, 26, 255))
    # eight-pointed police star in green
    pts = []
    for i in range(16):
        a = -math.pi / 2 + i * math.pi / 8
        rr = S * (0.47 if i % 2 == 0 else 0.36)
        pts.append((S / 2 + rr * math.cos(a), S / 2 + rr * math.sin(a)))
    d.polygon(pts, fill=(52, 120, 76, 255))
    d.ellipse([S * 0.18, S * 0.18, S * 0.82, S * 0.82], fill=(214, 210, 196, 255))
    _eagle(d, S * 0.0058, ox=S * 0.21, oy=S * 0.2)
    return im.resize((size, size), Image.LANCZOS)


# ------------------------------------------------------------------ round seal stamp (watermark)
def seal(diam, text, col=RED, alpha=0.22, seed=3):
    k = 3
    S = diam * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = col + (255,)
    d.ellipse([k, k, S - k, S - k], outline=c, width=3 * k)
    d.ellipse([S * 0.16, S * 0.16, S * 0.84, S * 0.84], outline=c, width=2 * k)
    f = F("sansb", int(S * 0.085))
    n = len(text)
    for i, ch in enumerate(text):
        a = -math.pi / 2 + (i - n / 2) * (2 * math.pi / (n + 2))
        r = S * 0.41
        x, y = S / 2 + r * math.cos(a), S / 2 + r * math.sin(a)
        g = Image.new("RGBA", (int(S * 0.12), int(S * 0.12)), (0, 0, 0, 0))
        ImageDraw.Draw(g).text((g.width / 2, g.height / 2), ch, font=f, fill=c, anchor="mm")
        g = g.rotate(-math.degrees(a) - 90, resample=Image.BICUBIC)
        im.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    _eagle(ImageDraw.Draw(im), S * 0.0052, ox=S * 0.24, oy=S * 0.23, col=c, red=c)
    im = im.resize((diam, diam), Image.LANCZOS)
    im = ink_wear(im, 0.3, seed)
    a = np.asarray(im).copy()
    a[..., 3] = (a[..., 3] * alpha).astype(np.uint8)
    return Image.fromarray(a, "RGBA")


def box_stamp(text, size, col=RED, alpha=0.5, angle=-7, seed=5):
    f = F("sansb", size)
    tw = int(f.getlength(text)) + size
    th = int(size * 1.7)
    im = Image.new("RGBA", (tw + 8, th + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([3, 3, tw + 4, th + 4], outline=col + (255,), width=max(2, size // 8))
    d.text(((tw + 8) / 2, (th + 8) / 2), text, font=f, fill=col + (255,), anchor="mm")
    im = ink_wear(im, 0.28, seed).rotate(angle, expand=True, resample=Image.BICUBIC)
    a = np.asarray(im).copy()
    a[..., 3] = (a[..., 3] * alpha).astype(np.uint8)
    return Image.fromarray(a, "RGBA")


# ------------------------------------------------------------------ window backgrounds
def folder_bg(kind, w=780, h=700):
    base, dark, light = (KHAKI, KHAKI_D, KHAKI_L) if kind == "brd" else (GREEN_FOLDER, GREEN_D, GREEN_L)
    im = cardboard(w, h, base)
    d = ImageDraw.Draw(im)
    # header band: a shade darker, closed by a printed double rule
    hb = Image.new("RGBA", (w, 86), dark + (110,))
    im.alpha_composite(hb, (0, 0))
    d.line([14, 84, w - 15, 84], fill=LINE + (200,), width=1)
    d.line([14, 87, w - 15, 87], fill=LINE_D + (150,), width=1)
    # printed label field behind the title ("Aktenschild")
    d.rectangle([76, 14, 476, 77], outline=LINE + (150,), width=1)
    d.rectangle([79, 17, 473, 74], outline=LINE_D + (90,), width=1)
    # tab rail under the register tabs
    d.line([14, 127, w - 15, 127], fill=dark + (255,), width=2)
    # punched filing holes on the left margin
    for y in (300, 404):
        d.ellipse([3, y - 6, 15, y + 6], fill=(14, 12, 8, 255), outline=light + (255,))
        d.arc([3, y - 6, 15, y + 6], 200, 340, fill=(0, 0, 0, 255), width=2)
    # inner sheet edge on the right: a paper sheet peeking out of the folder
    sheet = Image.new("RGBA", (5, h - 150), (190, 178, 146, 70))
    im.alpha_composite(sheet, (w - 9, 132))
    # watermark stamps and the classification marking, printed top and bottom centre as on every page
    if kind == "brd":
        im.alpha_composite(seal(150, "BUNDESKANZLERAMT · BONN · ", alpha=0.13), (w - 196, h - 214))
        mark = "VS - NUR FÜR DEN DIENSTGEBRAUCH"
        foot_l = "Az.: II/2 - 30100 - Ge 5/70"
        foot_r = "Bundeskanzleramt · Bonn"
    else:
        im.alpha_composite(seal(150, "BUNDESKRIMINALAMT · WIESBADEN · ", col=RED, alpha=0.13, seed=9), (w - 196, h - 214))
        im.alpha_composite(box_stamp("GEHEIM", 64, alpha=0.12, angle=-11, seed=11), (60, 470))
        mark = "GEHEIM"
        foot_l = "Tgb.-Nr. TE 11 - 4/70 geh."
        foot_r = "Bundeskriminalamt · Wiesbaden"
    d = ImageDraw.Draw(im)
    fs = F("mono", 11)
    fmk = F("monob", 11)
    d.text((w / 2, 1), mark, font=fmk, fill=(196, 52, 44, 255), anchor="ma")
    d.text((w / 2, h - 15), mark, font=fmk, fill=(196, 52, 44, 255), anchor="ma")
    d.text((22, h - 15), foot_l, font=fs, fill=LINE + (120,))
    d.text((w - 22, h - 15), foot_r, font=fs, fill=LINE + (120,), anchor="ra")
    # outer edge: dark frame, slightly worn corners
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=9, outline=(20, 18, 12, 255), width=2)
    d.rounded_rectangle([3, 3, w - 4, h - 4], radius=7, outline=light + (120,), width=1)
    im.putalpha(Image.fromarray(np.minimum(np.asarray(im)[..., 3], np.asarray(rounded_mask(w, h, 9)))))
    return im


# ------------------------------------------------------------------ pieces
def register_tab(w=181, h=34, kind="brd"):
    base = KHAKI_L if kind == "brd" else GREEN_L
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    card = cardboard(w, h, base, grain=5)
    m = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(m)
    # a register tab: slanted shoulders and rounded top
    md.rounded_rectangle([0, 0, w - 1, h + 8], radius=7, fill=255)
    md.polygon([(0, h), (0, 6), (6, 0)], fill=255)
    im.paste(card, (0, 0), m)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h + 8], radius=7, outline=(28, 24, 16, 255), width=1)
    d.line([6, 3, w - 7, 3], fill=LINE + (110,), width=1)
    d.line([0, h - 1, w - 1, h - 1], fill=(28, 24, 16, 255), width=1)
    return im


def register_tab_active(w=181, h=34):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h + 8], radius=7, outline=LINE + (230,), width=2)
    d.rectangle([2, h - 4, w - 3, h - 1], fill=RED + (230,))
    d.rectangle([2, 2, w - 3, h - 5], fill=(230, 214, 170, 26))
    return im


def stamp_button(w, h=26, kind="ink"):
    """A rubber-stamp impression: dark field, worn double frame."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fill = (58, 50, 34, 255) if kind == "ink" else (104, 30, 26, 255)
    edge = LINE if kind == "ink" else (232, 196, 170)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], fill=fill)
    tex = cardboard(w, h, fill[:3], grain=6)
    im.alpha_composite(tex)
    frame = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fd = ImageDraw.Draw(frame)
    fd.rectangle([1, 1, w - 2, h - 2], outline=edge + (235,), width=2)
    fd.rectangle([4, 4, w - 5, h - 5], outline=edge + (120,), width=1)
    frame = ink_wear(frame, 0.18, seed=w)
    im.alpha_composite(frame)
    ImageDraw.Draw(im).rectangle([0, 0, w - 1, h - 1], outline=(18, 16, 10, 255), width=1)
    return im


def section_strip(w=740, h=28, kind="brd"):
    """A typed section label: dark strip with a red file-ribbon block and a printed underline."""
    base = (44, 40, 28) if kind == "brd" else (36, 42, 36)
    im = cardboard(w, h, base, grain=4)
    a = np.asarray(im).copy()
    fade = np.clip(1.25 - np.linspace(0, 1, w) * 0.55, 0.62, 1.0)
    a[..., 3] = (a[..., 3] * fade[None, :]).astype(np.uint8)
    im = Image.fromarray(a, "RGBA")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 6, h - 1], fill=RED + (255,))
    d.line([8, h - 1, w - 1, h - 1], fill=LINE + (170,), width=1)
    d.line([8, 0, w - 1, 0], fill=(20, 18, 12, 200), width=1)
    return im


def bar_track(w, h):
    im = Image.new("RGBA", (w, h), (24, 21, 15, 255))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=LINE_D + (220,))
    for i in range(1, 10):
        x = round(i * (w - 1) / 10)
        d.line([x, h - (5 if h > 12 else 3), x, h - 2], fill=LINE_D + (150,))
    return im


def topbar_box(w=56, h=26):
    im = cardboard(w, h, KHAKI, grain=5)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=(18, 16, 10, 255))
    d.rectangle([1, 1, w - 2, h - 2], outline=LINE_D + (200,))
    d.rectangle([w - 4, 1, w - 2, h - 2], fill=RED + (255,))
    return im


def build(reg):
    reg("cwgg_akte_bg_brd", folder_bg("brd"))
    reg("cwgg_akte_bg_bka", folder_bg("bka"))
    reg("cwgg_akte_tab", register_tab())
    reg("cwgg_akte_tab_bka", register_tab(kind="bka"))
    reg("cwgg_akte_tab_active", register_tab_active())
    reg("cwgg_akte_tab_s", register_tab(w=144))
    reg("cwgg_akte_tab_bka_s", register_tab(w=144, kind="bka"))
    reg("cwgg_akte_tab_active_s", register_tab_active(w=144))
    reg("cwgg_akte_button_160", stamp_button(160))
    reg("cwgg_akte_button_96", stamp_button(96))
    reg("cwgg_akte_section", section_strip())
    reg("cwgg_akte_section_bka", section_strip(kind="bka"))
    reg("cwgg_akte_track_300", bar_track(300, 18))
    reg("cwgg_akte_track_160", bar_track(160, 10))
    reg("cwgg_akte_topbar", topbar_box())
    reg("cwgg_emblem_brd", emblem_from_file("brd_bundesadler.png") if os.path.exists(os.path.join(EMBLEM_DIR, "brd_bundesadler.png")) else emblem_brd())
    reg("cwgg_emblem_ddr", emblem_from_file("ddr_staatswappen.png") if os.path.exists(os.path.join(EMBLEM_DIR, "ddr_staatswappen.png")) else emblem_ddr())
    reg("cwgg_emblem_bka", emblem_from_file("bka_bundesadler.png") if os.path.exists(os.path.join(EMBLEM_DIR, "bka_bundesadler.png")) else emblem_bka())


CORNERED = {"cwgg_akte_bg_brd": (780, 700), "cwgg_akte_bg_bka": (780, 700)}
BUTTONS = {"cwgg_akte_tab", "cwgg_akte_tab_bka", "cwgg_akte_tab_s", "cwgg_akte_tab_bka_s", "cwgg_akte_button_160", "cwgg_akte_button_96", "cwgg_akte_topbar"}
