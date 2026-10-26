# IMPERIA CW — Cold War: art — preview.
# COLDWAR | Mock-up of the Politburo dossier with sample content (for review only; the game fills the same slots).
import os, sys, glob
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pb_layout as L

HERE = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(HERE, "png")
LEAD = "/mnt/user-data/uploads/mdcoldwar/gfx/leaders"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/pbgui/preview/politburo_preview.png"
FONTDIR = "/home/claude/pbgui/fonts_ttf"
TW16 = ImageFont.truetype(os.path.join(FONTDIR, "CourierPrime-Bold.ttf"), 12)
TW22 = ImageFont.truetype(os.path.join(FONTDIR, "CourierPrime-Bold.ttf"), 17)
SMALL = ImageFont.truetype(os.path.join(FONTDIR, "CourierPrime-Bold.ttf"), 10)
INK = (35, 30, 26, 255)


def im(name):
    return Image.open(os.path.join(PNG, name + ".png")).convert("RGBA")


def portrait(path, scale):
    p = Image.open(os.path.join(LEAD, path)).convert("RGBA")
    return p.resize((round(156 * scale), round(210 * scale)), Image.LANCZOS)


def flag(colours, w=41, h=26):
    f = Image.new("RGBA", (w, h), colours[0])
    d = ImageDraw.Draw(f)
    if len(colours) > 1:
        d.rectangle([0, int(h * .66), w, h], fill=colours[1])
    d.text((3, 1), "☭", fill=(240, 200, 80), font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9))
    d.rectangle([0, 0, w - 1, h - 1], outline=(40, 30, 20))
    return f


def main():
    bg = im("politburo_dossier")
    d = ImageDraw.Draw(bg)
    # General Secretary
    gx, gy = L.GS_PHOTO
    bg.alpha_composite(portrait("SOV/SOV_Coldwar_Brezhnev.dds", L.GS_SCALE), (gx, gy))
    bg.alpha_composite(im("photo_corners_large"), (gx - 4, gy - 4))
    vals = {"office": "General Secretary of the CC CPSU", "heir": "none designated",
            "cohesion": "62 - Stable", "session": "1 July 1970", "congress": "XXIV Congress, 30 March 1971"}
    for k, v in vals.items():
        d.text((L.VALUE_X, L.ROWS[k] + 3), v, fill=INK, font=TW16)
    d.text((L.VALUE_X, L.ROWS["name"] + 3), "Leonid Brezhnev", fill=INK, font=TW22)
    bx, by, bw, bh = L.BAR
    m = im("balance_marker")
    fw = bw + 2 * L.BAR_PAD
    frame = 11 + 2  # +0.15 -> between 11 and 12
    bg.alpha_composite(m.crop((fw * frame, 0, fw * (frame + 1), 24)), (bx - L.BAR_PAD, by - 7))
    d.text((bx + bw + 8, by - 1), "+0.15", fill=INK, font=TW16)
    # seats
    seats = [("UKR/UKR_Coldwar_Petro_Shelest.dds", "Petro Shelest", "First Secretary of the\nCP of Ukraine", [(200, 30, 30), (40, 90, 200)], "stamp_for"),
             ("KAZ/KAZ_Coldwar_Dinmukhamed_Kunaev.dds", "Dinmukhamed Kunaev", "First Secretary of the\nCP of Kazakhstan", [(200, 30, 30), (50, 140, 200)], "stamp_pending"),
             (None, "", "", None, "stamp_vacant")]
    for i, (p, name, title, fl, st) in enumerate(seats):
        x = L.SEAT_X[i]
        px, py = x + L.SEAT_PHOTO_DX, L.SEAT_Y + L.SEAT_PHOTO_DY
        if p:
            bg.alpha_composite(portrait(p, L.SEAT_SCALE), (px, py))
            bg.alpha_composite(im("photo_corners_small"), (px - 4, py - 4))
            bg.alpha_composite(flag(fl), (x + L.SEAT_FLAG_DX, L.SEAT_Y + L.SEAT_FLAG_DY))
            d.text((x, L.SEAT_NAME_Y + 2), name, fill=INK, font=TW16)
            d.multiline_text((x, L.SEAT_TITLE_Y + 2), title, fill=INK, font=SMALL, spacing=1)
        s = im(st)
        s = s.resize((round(s.size[0] * .72), round(s.size[1] * .72)), Image.LANCZOS)
        bg.alpha_composite(s, (px + 26, py + 58) if st != 'stamp_vacant' else (x + 2, L.SEAT_Y + 30))
    # ballot
    d.text((82, L.BALLOT_Y + 4), "Vote in progress on Yuri Andropov as General Secretary.", fill=INK, font=SMALL)
    d.text((82, L.BALLOT_Y + 17), "Moscow casts 3 votes in favour; fails only if all three vote against.", fill=INK, font=SMALL)
    # emulation
    rows = [("Ukrainian SSR", "+1.4%", "3rd of 14"), ("Ukrainian SSR", "412 factories", "1st of 14"), ("Estonian SSR", "$2.10k", "6th of 14"), ("Kazakh SSR", "3 fulfilled", "2nd of 14")]
    c = L.EMU_COLS
    for i, (lead, val, rank) in enumerate(rows):
        y = L.EMU_ROW_Y + i * L.EMU_ROW_H
        bg.alpha_composite(flag([(200, 30, 30), (40, 90, 200)], 20, 17), (c["flag"] + 3, y + 1))
        d.text((c["leader"], y + 3), lead, fill=INK, font=TW16)
        d.text((c["value"], y + 3), val, fill=INK, font=TW16)
        d.text((c["rank"], y + 3), rank, fill=INK, font=TW16)
        if i < 3:
            bg.alpha_composite(im("banner_held" if i != 2 else "banner_away"), (c["banner"], y + 1))
    x0 = L.HONOUR_TEXT_X
    d.text((x0, L.PRIDE_Y + 2), "Pride of the Union: Ukrainian SSR - Hero of Socialist Labour", fill=INK, font=TW16)
    d.text((x0, L.LAG_Y + 2), "Last place: Tajik SSR", fill=INK, font=TW16)
    d.text((L.FAV_X + 22, L.LAG_Y + 2), "Moscow favours: Byelorussian SSR", fill=INK, font=TW16)
    d.text((x0, L.SPART_Y + 2), "VI Spartakiad, summer 1975: preparations - our team 7 points", fill=INK, font=TW16)
    big = bg.resize((L.W * 2, L.H * 2), Image.LANCZOS)
    big.save(OUT)
    bg.save(OUT.replace(".png", "_1x.png"))


if __name__ == "__main__":
    main()
