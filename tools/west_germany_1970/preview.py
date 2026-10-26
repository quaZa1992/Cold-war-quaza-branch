# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""Render the focus tree as PNGs (whole tree and one per pillar) to check layout and lines by eye.

    python3 preview.py <out_dir>
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

import tree
import tree_pillars  # noqa: F401
import foreign  # noqa: F401
import dark_path  # noqa: F401
import domestic  # noqa: F401
import unity  # noqa: F401
import branches  # noqa: F401
import civilian  # noqa: F401
import guestworkers  # noqa: F401
import flavor  # noqa: F401

CW, CH = 96, 74
COLS = {"chancellery": (90, 60, 60), "social_market": (60, 90, 60), "energy_programme": (90, 90, 40), "internal_security": (60, 60, 100),
        "citizen_in_uniform": (70, 80, 60), "atlantic_anchor": (50, 70, 110), "dp_hub": (110, 60, 40), "cultural_diplomacy": (60, 100, 100),
        "root": (120, 120, 120)}


def main(out):
    os.makedirs(out, exist_ok=True)
    tree.mutex_symmetric()
    if os.environ.get('NOAUTO') is None:
        tree.auto_layout()
    F, B = tree.FOCUSES, tree.BY_KEY
    W = (max(f["ax"] for f in F) + 2) * CW
    H = (max(f["ay"] for f in F) + 2) * CH
    im = Image.new("RGB", (W, H), (30, 30, 36))
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)

    def c(f):
        return f["ax"] * CW + CW // 2 + 20, f["ay"] * CH + CH // 2 + 10
    for f in F:
        for g in f["pre"]:
            for k in g:
                a, b = c(B[k]), c(f)
                mid = (a[1] + b[1]) // 2
                d.line([a, (a[0], mid), (b[0], mid), b], fill=(150, 150, 150) if len(g) == 1 else (200, 170, 60), width=1)
        for m in f["mutex"]:
            d.line([c(B[m]), c(f)], fill=(220, 60, 60), width=1)
    for f in F:
        x, y = c(f)
        d.rectangle([x - 44, y - 24, x + 44, y + 24], fill=COLS[f["pillar"]], outline=(220, 220, 220))
        lines, cur = [], ""
        for w in f["name"].split():
            if d.textlength(cur + " " + w, font=font) > 84 and cur:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        for i, ln in enumerate(lines[:3]):
            d.text((x - 42, y - 22 + i * 11), ln, font=font, fill=(255, 255, 255))
        d.text((x + 30, y + 12), str(f["cost"]), font=font, fill=(255, 230, 120))
    im.save(os.path.join(out, "tree_full.png"))
    for p in COLS:
        fs = [f for f in F if f["pillar"] == p]
        x0 = min(f["ax"] for f in fs) * CW
        x1 = (max(f["ax"] for f in fs) + 1) * CW + 40
        y1 = (max(f["ay"] for f in fs) + 1) * CH + 20
        im.crop((x0, 0, x1, y1)).save(os.path.join(out, f"tree_{p}.png"))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "preview")
