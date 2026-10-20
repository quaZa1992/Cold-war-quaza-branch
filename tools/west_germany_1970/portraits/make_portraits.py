"""Crop, colourise and export the 1970-2000 German leader portraits.

Sources are Wikimedia Commons photos (mostly Bundesarchiv, see credits.json).
Black-and-white photos are hand-tint colourised in Lab space: the original
luminance is kept and colour is painted through soft masks for skin, hair,
shirt, suit and backdrop that are built from a Haar face detection.
Output: 156x210 HOI4 leader portraits as uncompressed 32-bit DDS plus PNG previews.
"""
import json, os, struct, sys
import numpy as np
import cv2
from PIL import Image, ImageFilter, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/portraits/src"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/home/claude/portraits/out"
CASCADE = sys.argv[3] if len(sys.argv) > 3 else "/home/claude/portraits/cascades/cv2/data/haarcascade_frontalface_default.xml"
W, H = 156, 210

# key: (source file, output name, manual face box override (x, y, w) in source px or None, colourise?)
PEOPLE = {
    "schmidt":     ("schmidt", None),
    "barzel":      ("barzel", None),
    "strauss":     ("strauss", None),
    "scheel":      ("scheel", None),
    "genscher":    ("genscher", None),
    "vogel":       ("vogel", None),
    "rau":         ("rau", None),
    "lafontaine":  ("lafontaine", None),
    "engholm":     ("engholm", None),
    "scharping":   ("scharping_hi", None),
    "albrecht":    ("albrecht", None),
    "spaeth":      ("spaeth", None),
    "kelly":       ("kelly", None),
    "honecker":    ("honecker", None),
    "krenz":       ("krenz", None),
    "modrow":      ("modrow", None),
    "demaiziere":  ("demaiziere_hi", None),
    "schoenhuber": ("schoenhuber", None),
    "lambsdorff":  ("lambsdorff", None),
    "stoph":       ("stoph", None),
}

# Hair tone per person: (a, b, lightness-bias). Grey/white hair gets near-neutral.
HAIR = {
    "schmidt": "grey", "barzel": "dark", "strauss": "dark", "scheel": "grey",
    "genscher": "dark", "vogel": "grey", "rau": "grey", "lafontaine": "brown",
    "engholm": "grey", "scharping": "dark", "albrecht": "grey", "spaeth": "dark",
    "kelly": "brown", "lambsdorff": "dark", "stoph": "grey", "demaiziere": "grey",
}
# Suit tone: navy, charcoal, brown
SUIT = {"schmidt": "navy", "barzel": "grey", "scheel": "charcoal", "genscher": "charcoal",
        "vogel": "charcoal", "rau": "beige", "lafontaine": "charcoal", "engholm": "navy",
        "spaeth": "charcoal", "kelly": "black", "lambsdorff": "navy", "stoph": "charcoal",
        "demaiziere": "charcoal", "scharping": "navy"}
SUIT_AB = {"navy": (2, -14), "charcoal": (0, -4), "grey": (0, -3), "beige": (3, 14),
           "black": (0, -2), "brown": (6, 12)}
HAIR_AB = {"grey": (0, 2), "dark": (4, 9), "brown": (8, 16)}


def detect_face(gray, cascade):
    faces = cascade.detectMultiScale(gray, scaleFactor=1.07, minNeighbors=5,
                                     minSize=(gray.shape[1] // 8, gray.shape[1] // 8))
    if len(faces) == 0:
        faces = cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3,
                                         minSize=(gray.shape[1] // 12, gray.shape[1] // 12))
    if len(faces) == 0:
        return None
    return max(faces, key=lambda f: f[2] * f[3])


def is_colour(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return float(np.mean(hsv[..., 1])) > 28


def soft(mask, sigma):
    return cv2.GaussianBlur(mask.astype(np.float32), (0, 0), sigma)


def colourise(img, face, name):
    """img: BGR uint8 (already cropped), face: (x, y, w, h) in img coords."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    L = gray.astype(np.float32) / 255.0
    fx, fy, fw, fh = face
    cx, cy = fx + fw / 2, fy + fh / 2
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

    # skin: face ellipse + neck + ears
    face_e = ((xx - cx) / (fw * 0.50)) ** 2 + ((yy - (cy + fh * 0.05)) / (fh * 0.68)) ** 2 <= 1
    head_e = ((xx - cx) / (fw * 0.62)) ** 2 + ((yy - (cy + fh * 0.02)) / (fh * 0.80)) ** 2 <= 1
    neck = (np.abs(xx - cx) < fw * 0.32) & (yy > cy + fh * 0.35) & (yy < fy + fh * 1.42)
    # bright, non-hair pixels in the wider head area count as skin too (turned heads)
    skin = ((face_e | neck) & (L > 0.18)) | (head_e & (L > 0.42) & (yy > fy + fh * 0.12))
    # hair: band above and around the face
    hair_e = ((xx - cx) / (fw * 0.68)) ** 2 + ((yy - (cy - fh * 0.12)) / (fh * 0.78)) ** 2 <= 1
    hair = hair_e & ~face_e & (yy < cy + fh * 0.15) & ~((L > 0.42) & head_e & (yy > fy + fh * 0.12))
    # torso below the chin
    torso = (yy > fy + fh * 1.05) & ~neck
    shirt = torso & (L > 0.62) & (np.abs(xx - cx) < fw * 0.75)
    suit = torso & ~shirt
    person = face_e | neck | hair | torso
    backdrop = ~person

    sig = max(1.5, fw * 0.06)
    m_skin, m_hair = soft(skin, sig), soft(hair, sig * 1.4)
    m_shirt, m_suit = soft(shirt, sig), soft(suit, sig)
    m_bg = soft(backdrop, sig * 2.0)

    a = np.zeros_like(L); b = np.zeros_like(L)
    # skin tone, strongest in midtones
    mid = np.clip(1.0 - np.abs(L - 0.58) / 0.5, 0.25, 1.0)
    a += m_skin * 16.0 * mid; b += m_skin * 20.0 * mid
    # lips/cheeks warmth in the lower face
    cheeks = soft(((xx - cx) / (fw * 0.33)) ** 2 + ((yy - (cy + fh * 0.18)) / (fh * 0.22)) ** 2 <= 1, sig * 2)
    a += cheeks * 4.0 * mid
    ha, hb = HAIR_AB[HAIR.get(name, "dark")]
    hair_mid = np.clip(1.0 - L, 0.3, 1.0) if HAIR.get(name) != "grey" else 0.6
    a += m_hair * ha * hair_mid; b += m_hair * hb * hair_mid
    sa, sb = SUIT_AB[SUIT.get(name, "charcoal")]
    a += m_suit * sa * 0.9; b += m_suit * sb * 0.9
    a += m_shirt * -1.0; b += m_shirt * -4.0
    # muted studio backdrop: cool blue-grey that fades in the shadows
    bgk = np.clip(L * 1.3, 0.2, 1.0)
    a += m_bg * -3.0 * bgk; b += m_bg * -9.0 * bgk

    lab = np.dstack([L * 100.0, a, b]).astype(np.float32)
    rgb = cv2.cvtColor(lab, cv2.COLOR_Lab2RGB)
    rgb = np.clip(rgb * 255.0, 0, 255).astype(np.uint8)
    return rgb


def crop_box(iw, ih, face):
    fx, fy, fw, fh = face
    cw = fw * 2.25
    ch = cw * H / W
    cx = fx + fw / 2
    top = fy - fh * 0.62
    x0 = int(round(cx - cw / 2)); y0 = int(round(top))
    x1 = int(round(x0 + cw)); y1 = int(round(y0 + ch))
    # clamp, preserving size when possible
    if x0 < 0: x1 -= x0; x0 = 0
    if x1 > iw: x0 -= x1 - iw; x1 = iw
    if y0 < 0: y1 -= y0; y0 = 0
    if y1 > ih: y0 -= y1 - ih; y1 = ih
    x0, y0 = max(0, x0), max(0, y0)
    return x0, y0, min(iw, x1), min(ih, y1)


def write_dds(path, rgba):
    """Uncompressed 32-bit A8R8G8B8 DDS (HOI4 reads this directly)."""
    h, w, _ = rgba.shape
    bgra = rgba[..., [2, 1, 0, 3]].copy()
    header = struct.pack("<4sIIIIIII44sIIIIIIIIIIIII",
                         b"DDS ", 124, 0x1 | 0x2 | 0x4 | 0x1000 | 0x8, h, w, w * 4, 0, 1, b"\0" * 44,
                         32, 0x41, 0, 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000,
                         0x1000, 0, 0, 0, 0)
    with open(path, "wb") as f:
        f.write(header); f.write(bgra.tobytes())


def finish(rgb):
    im = Image.fromarray(rgb).resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    arr = np.asarray(im).astype(np.float32)
    # soft vignette in keeping with MD portraits
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = 1.0 - 0.22 * (((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.42) / (H * 0.68)) ** 2)
    arr = np.clip(arr * np.clip(v, 0.7, 1.0)[..., None], 0, 255).astype(np.uint8)
    return arr


def main():
    os.makedirs(OUT, exist_ok=True)
    cascade = cv2.CascadeClassifier(CASCADE)
    overrides = json.load(open(os.path.join(HERE, "face_overrides.json"))) if os.path.exists(os.path.join(HERE, "face_overrides.json")) else {}
    report = {}
    for name, (src, _) in PEOPLE.items():
        img = cv2.imread(os.path.join(SRC, src + ".jpg"))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = tuple(overrides[name]) if name in overrides else detect_face(gray, cascade)
        if face is None:
            report[name] = "NO FACE"; continue
        x0, y0, x1, y1 = crop_box(img.shape[1], img.shape[0], face)
        crop = img[y0:y1, x0:x1]
        fx, fy, fw, fh = face
        local = (fx - x0, fy - y0, fw, fh)
        coloured = is_colour(img)
        rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB) if coloured else colourise(crop, local, name)
        arr = finish(rgb)
        rgba = np.dstack([arr, np.full(arr.shape[:2], 255, np.uint8)])
        Image.fromarray(arr).save(os.path.join(OUT, f"COLDWAR_GER_1970_{name}.png"))
        write_dds(os.path.join(OUT, f"COLDWAR_GER_1970_{name}.dds"), rgba)
        report[name] = {"face": [int(v) for v in face], "crop": [x0, y0, x1, y1], "colourised": not coloured}
    json.dump(report, open(os.path.join(OUT, "report.json"), "w"), indent=1)
    print(json.dumps(report))


if __name__ == "__main__":
    main()
