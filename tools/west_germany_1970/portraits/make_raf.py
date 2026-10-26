# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""Wanted-card photos of the RAF for the Manhunt tab.

Sources (Wikimedia Commons, attached by the user):
  poster1972.jpg  File:Baader Meinhof Bander Poster.jpg  (BKA wanted poster 1972, photo by Coldupnorth, CC BY-SA 4.0)
  folkerts.jpg    File:KnutFolkerts.jpg                   (CC BY 4.0)
  klar1992.jpg    File:Christian Klar.jpg                 (public domain)
  boock.jpg, wisniewski.jpg, schulz.jpg                    (wanted photos supplied by the user, source not recorded)

Each face is cropped 3:4, cleaned of print grain, hand-tint colourised in Lab space and then graded
like a modern smartphone snapshot: warm auto white balance, lifted shadows, punchy midtone contrast,
over-sharpening and fine sensor noise. Output: 240x320 PNG masters in portraits/raf/ (gui_sprites
scales them into the wanted-card photo strip).
"""
import json, os, sys
import numpy as np
import cv2
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/portraits/raf_src"
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "raf")
W, H = 240, 320
S72 = 1932 / 1500  # poster boxes were measured on a 1500 px wide view

# key: source, crop box (x0, y0, x1, y1) in source px, face box (x, y, w, h) in the 240x320 output,
#      hair, clothes, already in colour?
PEOPLE = {
    "meinhof":   ("poster1972.jpg", tuple(int(v * S72) for v in (272, 464, 423, 653)), (53, 118, 128, 160), "darkbrown", "black", False),
    "baader":    ("poster1972.jpg", tuple(int(v * S72) for v in (463, 464, 616, 653)), (28, 70, 135, 180), "darkbrown", "leather", False),
    "ensslin":   ("poster1972.jpg", tuple(int(v * S72) for v in (662, 464, 811, 653)), (75, 75, 98, 175), "ashblonde", "black", False),
    "meins":     ("poster1972.jpg", tuple(int(v * S72) for v in (856, 464, 1008, 653)), (60, 90, 128, 175), "darkbrown", "charcoal", False),
    "raspe":     ("poster1972.jpg", tuple(int(v * S72) for v in (1062, 448, 1203, 636)), (48, 75, 130, 195), "brown", "black", False),
    "mohnhaupt": ("poster1972.jpg", tuple(int(v * S72) for v in (663, 942, 806, 1126)), (66, 62, 114, 160), "strawberry", "brownknit", False),
    "folkerts":  ("folkerts.jpg", (170, 40, 830, 920), (50, 70, 120, 180), "darkbrown", "navyknit", False),
    "klar":      ("klar1992.jpg", (215, 40, 575, 520), None, None, None, True),
    "boock":      ("boock.jpg", (0, 0, 450, 600), (40, 70, 170, 230), "brown", "white", False),
    "wisniewski": ("wisniewski.jpg", (3, 0, 318, 420), (63, 69, 133, 182), "darkbrown", "black", False),
    "schulz":     ("schulz.jpg", (0, 20, 320, 447), (52, 82, 143, 200), "darkbrown", "black", False),
}
HAIR_AB = {"darkbrown": (6, 11), "brown": (8, 17), "ashblonde": (4, 16), "strawberry": (13, 24)}
CLOTH_AB = {"black": (0, -2), "leather": (7, 9), "charcoal": (0, -5), "brownknit": (9, 15), "navyknit": (2, -13), "white": (0, -2)}


def soft(mask, sigma):
    return cv2.GaussianBlur(mask.astype(np.float32), (0, 0), sigma)


def clean_gray(bgr):
    """Neutralise the paper cast, remove print grain, normalise levels, add local contrast."""
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    g = cv2.resize(g, (W, H), interpolation=cv2.INTER_AREA if g.shape[1] > W else cv2.INTER_LANCZOS4)
    g = cv2.fastNlMeansDenoising(g, None, h=4, templateWindowSize=7, searchWindowSize=21)
    lo, hi = np.percentile(g, 0.4), np.percentile(g, 99.8)
    g = np.clip((g.astype(np.float32) - lo) / max(1.0, hi - lo) * 255.0, 0, 255).astype(np.uint8)
    c = cv2.createCLAHE(clipLimit=1.2, tileGridSize=(4, 4)).apply(g)
    g = cv2.addWeighted(g, 0.6, c, 0.4, 0)
    # print photos crush both ends: open the shadows, pull the paper white down to a real-world highlight
    x = g.astype(np.float32) / 255.0
    x = 0.06 + 0.86 * np.power(x, 0.86)
    g = (x * 255).astype(np.uint8)
    return g


def colourise(gray, face, hair, cloth):
    h, w = gray.shape
    L = gray.astype(np.float32) / 255.0
    fx, fy, fw, fh = face
    cx, cy = fx + fw / 2, fy + fh / 2
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    face_e = ((xx - cx) / (fw * 0.52)) ** 2 + ((yy - (cy + fh * 0.06)) / (fh * 0.70)) ** 2 <= 1
    head_e = ((xx - cx) / (fw * 0.66)) ** 2 + ((yy - cy) / (fh * 0.86)) ** 2 <= 1
    neck = (np.abs(xx - cx) < fw * 0.30) & (yy > cy + fh * 0.35) & (yy < fy + fh * 1.40)
    skin = ((face_e | neck) & (L > 0.20)) | (head_e & (L > 0.48) & (yy > fy + fh * 0.15))
    hair_e = ((xx - cx) / (fw * 0.95)) ** 2 + ((yy - (cy - fh * 0.05)) / (fh * 1.15)) ** 2 <= 1
    hair_m = hair_e & ~skin & (yy < fy + fh * 1.9) & ~((yy > fy + fh * 1.05) & (np.abs(xx - cx) < fw * 0.55))
    torso = (yy > fy + fh * 1.08) & ~neck & ~hair_m
    person = face_e | neck | hair_m | torso | head_e
    bg = ~person

    sig = max(1.5, fw * 0.06)
    m_skin, m_hair, m_cloth, m_bg = soft(skin, sig), soft(hair_m, sig * 1.5), soft(torso, sig), soft(bg, sig * 2.5)
    a = np.zeros_like(L); b = np.zeros_like(L)
    mid = np.clip(1.0 - np.abs(L - 0.6) / 0.5, 0.25, 1.0)
    a += m_skin * 13.5 * mid; b += m_skin * 15.5 * mid
    cheeks = soft(((xx - cx) / (fw * 0.34)) ** 2 + ((yy - (cy + fh * 0.16)) / (fh * 0.22)) ** 2 <= 1, sig * 2)
    a += cheeks * 3.5 * mid
    lips = soft(((xx - cx) / (fw * 0.16)) ** 2 + ((yy - (cy + fh * 0.33)) / (fh * 0.06)) ** 2 <= 1, sig * 0.8)
    a += lips * 7.0 * mid; b += lips * 1.0 * mid
    ha, hb = HAIR_AB[hair]
    hk = np.clip(0.2 + L, 0.3, 0.9) * 0.8
    a += m_hair * ha * hk; b += m_hair * hb * hk
    ca, cb = CLOTH_AB[cloth]
    a += m_cloth * ca * 0.8; b += m_cloth * cb * 0.8
    # the kind of beige-grey office wall phone cameras love to warm up
    bk = np.clip(L * 1.2, 0.2, 1.0)
    a += m_bg * -1.0 * bk; b += m_bg * -1.5 * bk
    # real colour dies in deep shadow and in blown highlights
    keep = np.clip((L - 0.08) / 0.25, 0, 1) * np.clip((0.98 - L) / 0.2, 0.3, 1)
    a *= keep; b *= keep
    lab = np.dstack([L * 100.0, a, b]).astype(np.float32)
    rgb = cv2.cvtColor(lab, cv2.COLOR_Lab2RGB)
    return np.clip(rgb * 255.0, 0, 255).astype(np.uint8)


def phone_grade(rgb, seed):
    """Smartphone look: auto-WB warmth, HDR-ish lifted shadows, midtone punch, chroma boost, sharpening, noise."""
    x = rgb.astype(np.float32) / 255.0
    # lifted shadows / slightly rolled highlights (tone-mapped HDR look)
    x = 0.02 + 0.97 * x
    x = x + 0.15 * x * (1 - x) * (x - 0.4)          # gentle S around the midtones
    lab = cv2.cvtColor(np.clip(x, 0, 1).astype(np.float32), cv2.COLOR_RGB2Lab)
    lab[..., 1] = lab[..., 1] * 1.08 + 0.5           # vivid + a touch of magenta
    lab[..., 2] = lab[..., 2] * 1.06 + 1.5           # warm auto white balance
    lab[..., 0] = np.clip(lab[..., 0] * 1.02 + 1.5, 0, 100)
    x = np.clip(cv2.cvtColor(lab, cv2.COLOR_Lab2RGB), 0, 1)
    # computational over-sharpening
    blur = cv2.GaussianBlur(x, (0, 0), 1.1)
    x = np.clip(x + 0.55 * (x - blur), 0, 1)
    # sensor noise: luminance grain plus a little chroma
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 0.012, x.shape[:2])[..., None] + rng.normal(0, 0.004, x.shape)
    x = np.clip(x + n, 0, 1)
    # light lens vignette
    h, w = x.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    v = 1.0 - 0.16 * (((xx - w / 2) / (w * 0.7)) ** 2 + ((yy - h * 0.45) / (h * 0.7)) ** 2)
    x = np.clip(x * np.clip(v, 0.78, 1.0)[..., None], 0, 1)
    return (x * 255).astype(np.uint8)


def main():
    os.makedirs(OUT, exist_ok=True)
    faces = {}
    for i, (key, (src, box, face, hair, cloth, colour)) in enumerate(PEOPLE.items()):
        img = cv2.imread(os.path.join(SRC, src))
        x0, y0, x1, y1 = box
        crop = img[y0:y1, x0:x1]
        if colour:
            rgb = cv2.cvtColor(cv2.resize(crop, (W, H), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2RGB)
            rgb = cv2.fastNlMeansDenoisingColored(rgb, None, 4, 4, 7, 21)
        else:
            g = clean_gray(crop)
            faces[key] = face
            rgb = colourise(g, face, hair, cloth)
        out = phone_grade(rgb, seed=1970 + i)
        Image.fromarray(out).save(os.path.join(OUT, f"{key}.png"))
        print(key, "face", faces.get(key))
    json.dump(faces, open(os.path.join(OUT, "faces.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
